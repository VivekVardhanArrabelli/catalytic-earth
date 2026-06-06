from __future__ import annotations

import json
import unittest

from catalytic_earth.cofactor_presence_calibration import (
    MOTIF_FEATURE_SPECS,
    _augment_with_motifs,
    _motif_feature_vector,
    build_cofactor_presence_calibration,
)


def _embedding(metal_positive: bool, index: int) -> list[float]:
    # Linearly separable 2-D embedding with a tiny per-row jitter so the points
    # are not perfectly degenerate; metal-positive rows load on the first axis.
    if metal_positive:
        return [1.0 + 0.01 * index, 0.0 + 0.005 * index]
    return [0.0 + 0.005 * index, 1.0 + 0.01 * index]


def _make_inputs(*, heldout_metal: bool):
    rows = []
    geometry_entries = []
    embeddings = []
    split_records = []

    def add(entry_id, split_assignment, embedding_split, label_metal, embed_metal, index):
        rows.append(
            {
                "entry_id": entry_id,
                "split_assignment": split_assignment,
                "sequence_id": entry_id,
                "fingerprint_id": None,
            }
        )
        geometry_entries.append(
            {
                "entry_id": entry_id,
                "status": "ok",
                "ligand_context": {
                    "cofactor_families": ["metal_ion"] if label_metal else []
                },
            }
        )
        embeddings.append(
            {"entry_id": entry_id, "raw_embedding": _embedding(embed_metal, index)}
        )
        if embedding_split is not None:
            split_records.append(
                {"entry_id": entry_id, "assigned_embedding_split": embedding_split}
            )

    # 8 train rows (4 metal-positive, 4 negative)
    for i in range(4):
        add(f"m_csa:{i+1}", "in_distribution", "train", True, True, i)
    for i in range(4):
        add(f"m_csa:{i+5}", "in_distribution", "train", False, False, i)
    # 4 calibration rows (2 positive, 2 negative)
    add("m_csa:9", "in_distribution", "calibration", True, True, 0)
    add("m_csa:10", "in_distribution", "calibration", True, True, 1)
    add("m_csa:11", "in_distribution", "calibration", False, False, 0)
    add("m_csa:12", "in_distribution", "calibration", False, False, 1)
    # 2 heldout rows with FIXED embeddings; only their LABELS are flipped between
    # the two builds, to prove the labels are never read for fit/threshold/prediction.
    add("m_csa:13", "heldout", None, heldout_metal, True, 0)
    add("m_csa:14", "heldout", None, not heldout_metal, False, 1)

    label_manifest = {"rows": rows}
    geometry_features = {"entries": geometry_entries}
    split_manifest = {"split_records": split_records}
    embedding_sidecars = {"esm2_test": embeddings}
    return label_manifest, geometry_features, split_manifest, embedding_sidecars


class CofactorPresenceCalibrationTests(unittest.TestCase):
    def test_builds_train_cal_only_channel(self) -> None:
        lm, gf, sm, sidecars = _make_inputs(heldout_metal=True)
        audit = build_cofactor_presence_calibration(
            label_manifest=lm,
            geometry_features=gf,
            split_manifest=sm,
            embedding_sidecars=sidecars,
            min_calibration_positive=2,
        )
        self.assertEqual(audit["status"], "complete")
        guardrails = audit["guardrails"]
        self.assertFalse(guardrails["heldout_labels_read"])
        self.assertTrue(guardrails["heads_fit_on_train_split_only"])
        self.assertTrue(guardrails["thresholds_selected_on_calibration_split_only"])
        self.assertTrue(guardrails["supervision_is_structural_ligand_context_only"])
        self.assertFalse(guardrails["mechanism_fingerprint_used_for_labels"])

        # Coverage reflects the synthetic split (8 train + 4 calibration covered).
        coverage = audit["split_coverage"]
        self.assertEqual(coverage["covered_split_counts"], {"calibration": 4, "train": 8})
        self.assertEqual(coverage["heldout_clean_count"], 2)

        metal = audit["selected_sources"]["metal_ion"]
        self.assertEqual(metal["backend"], "esm2_test")
        self.assertIsNotNone(metal["selected_threshold"])
        head = audit["trained_calibrated_heads"]["esm2_test"]["class_results"]["metal_ion"]
        self.assertEqual(head["status"], "complete")
        # Separable calibration -> the operating point should retain the positives.
        self.assertGreaterEqual(head["selected_operating_point"]["recall"], 0.5)

        # Predictions are emitted for the heldout entries without reading truth.
        by_entry = {row["entry_id"]: row for row in audit["channel_predictions"]}
        self.assertIn("m_csa:13", by_entry)
        self.assertEqual(by_entry["m_csa:13"]["split_assignment"], "heldout")

    def test_heldout_labels_never_affect_fit_threshold_or_predictions(self) -> None:
        lm_a, gf_a, sm_a, side_a = _make_inputs(heldout_metal=True)
        lm_b, gf_b, sm_b, side_b = _make_inputs(heldout_metal=False)
        audit_a = build_cofactor_presence_calibration(
            label_manifest=lm_a,
            geometry_features=gf_a,
            split_manifest=sm_a,
            embedding_sidecars=side_a,
            min_calibration_positive=2,
        )
        audit_b = build_cofactor_presence_calibration(
            label_manifest=lm_b,
            geometry_features=gf_b,
            split_manifest=sm_b,
            embedding_sidecars=side_b,
            min_calibration_positive=2,
        )
        # Flipping every heldout label must leave the fitted heads, the
        # calibration-selected sources, and the per-entry predictions identical.
        for key in ("trained_calibrated_heads", "selected_sources", "channel_predictions"):
            self.assertEqual(
                json.dumps(audit_a[key], sort_keys=True),
                json.dumps(audit_b[key], sort_keys=True),
                msg=f"heldout labels leaked into {key}",
            )

    def test_low_calibration_support_is_flagged(self) -> None:
        lm, gf, sm, sidecars = _make_inputs(heldout_metal=True)
        audit = build_cofactor_presence_calibration(
            label_manifest=lm,
            geometry_features=gf,
            split_manifest=sm,
            embedding_sidecars=sidecars,
            min_calibration_positive=3,  # 2 calibration positives < 3 -> low support
        )
        head = audit["trained_calibrated_heads"]["esm2_test"]["class_results"]["metal_ion"]
        self.assertTrue(head["low_calibration_support"])


class MotifFeatureTests(unittest.TestCase):
    def test_motif_vector_fires_on_known_motifs(self) -> None:
        names = [name for name, _ in MOTIF_FEATURE_SPECS]
        rossmann_idx = names.index("rossmann_gxgxxg")
        heme_idx = names.index("heme_cxxch")
        # GAGVVG matches G.G..G; CAACH matches C..CH.
        with_rossmann = _motif_feature_vector("MKGAGVVGAAA")
        self.assertEqual(with_rossmann[rossmann_idx], 1)
        with_heme = _motif_feature_vector("AAACAACHAAA")
        self.assertEqual(with_heme[heme_idx], 1)
        none = _motif_feature_vector("AAAAAAAAAA")
        self.assertEqual(none[rossmann_idx], 0)
        self.assertEqual(none[heme_idx], 0)

    def test_augment_appends_motif_dimensions(self) -> None:
        embeddings = {"m_csa:1": [0.1, 0.2]}
        sequences = {"m_csa:1": "MKGAGVVGAAA"}
        augmented = _augment_with_motifs(embeddings, sequences)
        self.assertEqual(len(augmented["m_csa:1"]), 2 + len(MOTIF_FEATURE_SPECS))
        # missing sequence -> zero motif block, still appended
        augmented_missing = _augment_with_motifs(embeddings, {})
        self.assertEqual(len(augmented_missing["m_csa:1"]), 2 + len(MOTIF_FEATURE_SPECS))
        self.assertEqual(augmented_missing["m_csa:1"][2:], [0.0] * len(MOTIF_FEATURE_SPECS))


if __name__ == "__main__":
    unittest.main()
