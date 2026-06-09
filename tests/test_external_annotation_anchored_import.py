from __future__ import annotations

import unittest

from catalytic_earth.external_annotation_anchored_import import (
    build_external_annotation_anchored_import,
    classify_row,
    cofactor_classes,
)


def _row(lane, *, cofactors=(), dup="no_exact_current702_accession_or_sequence_sha_overlap",
         accession="P00001", ec=("3.4.24.10",), codes=("ECO:0000269",)):
    return {
        "accession": accession,
        "target_family_lane": lane,
        "duplicate_current_registry_conflict_status": dup,
        "cofactor_provenance": [{"name": n} for n in cofactors],
        "rhea_ec_provenance": {"ec_numbers": list(ec), "rhea_record_count": 1},
        "source_evidence_codes": list(codes),
        "afdb_or_pdb_identifier": "AF-P00001-F1",
    }


class CofactorDetectionTests(unittest.TestCase):
    def test_metal_plp_flavin_heme_detected_by_name(self) -> None:
        self.assertEqual(cofactor_classes(_row("x", cofactors=["Zn(2+)"])), {"metal"})
        self.assertEqual(
            cofactor_classes(_row("x", cofactors=["pyridoxal 5'-phosphate"])), {"plp"}
        )
        self.assertEqual(cofactor_classes(_row("x", cofactors=["FAD"])), {"flavin"})
        self.assertEqual(cofactor_classes(_row("x", cofactors=["heme b"])), {"heme"})
        self.assertEqual(cofactor_classes(_row("x", cofactors=[])), set())


class ClassifyRowTests(unittest.TestCase):
    def test_primary_lane_with_cofactor_imports_positive(self) -> None:
        d = classify_row(_row("metal hydrolase", cofactors=["Zn(2+)"]))
        self.assertEqual(d["decision"], "import")
        self.assertEqual(d["label_type"], "seed_fingerprint")
        self.assertEqual(d["fingerprint_id"], "metal_dependent_hydrolase")

    def test_primary_lane_without_cofactor_is_held(self) -> None:
        d = classify_row(_row("metal hydrolase", cofactors=[]))
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "primary_lane_without_cofactor_corroboration")

    def test_wrong_cofactor_for_lane_is_held(self) -> None:
        # PLP lane but only a metal cofactor -> no corroboration for plp -> hold.
        d = classify_row(_row("PLP children", cofactors=["Mg(2+)"]))
        self.assertEqual(d["decision"], "hold")

    def test_out_of_scope_lane_imports_negative(self) -> None:
        d = classify_row(_row("glycoside/nucleoside"))
        self.assertEqual(d["decision"], "import")
        self.assertEqual(d["label_type"], "out_of_scope")
        self.assertIsNone(d["fingerprint_id"])

    def test_ambiguous_lane_is_held(self) -> None:
        self.assertEqual(classify_row(_row("redox oxygen/sulfur"))["decision"], "hold")
        self.assertEqual(classify_row(_row("radical-SAM/cobalamin"))["decision"], "hold")

    def test_unconfirmed_duplicate_screen_is_skipped(self) -> None:
        d = classify_row(_row("metal hydrolase", cofactors=["Zn(2+)"], dup="pending"))
        self.assertEqual(d["decision"], "skip")


class BuildImportTests(unittest.TestCase):
    def test_non_destructive_preview_with_guardrails_and_dedup(self) -> None:
        preview = [
            _row("metal hydrolase", cofactors=["Zn(2+)"], accession="P00001"),
            _row("glycoside/nucleoside", accession="P00002"),
            _row("redox oxygen/sulfur", accession="P00003"),
            _row("metal hydrolase", cofactors=["Mn(2+)"], accession="P00004"),
            # already in registry -> must be skipped, not double-imported
            _row("metal hydrolase", cofactors=["Zn(2+)"], accession="P09999"),
        ]
        registry = [{"entry_id": "uniprot:P09999"}, {"entry_id": "m_csa:1"}]
        audit = build_external_annotation_anchored_import(preview=preview, registry=registry)

        self.assertFalse(audit["guardrails"]["curated_registry_written"])
        self.assertFalse(
            audit["guardrails"]["predictive_features_use_ec_name_or_prose"]
        )
        c = audit["counts"]
        # P00001, P00004 (positives) + P00002 (oos) = 3; P00003 held; P09999 skipped.
        self.assertEqual(c["importable_new_labels"], 3)
        self.assertEqual(c["label_type_counts"]["seed_fingerprint"], 2)
        self.assertEqual(c["label_type_counts"]["out_of_scope"], 1)
        self.assertEqual(c["current_registry_labels"], 2)
        self.assertEqual(c["projected_registry_labels_if_merged"], 5)

        # Every new label is bronze, automation_curated, uniprot, with EC excluded.
        for label in audit["applied_labels"]:
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertIn("ec_label", label["evidence"]["excluded_context"])
            self.assertEqual(
                label["evidence"]["evidence_basis"],
                "reviewed_swissprot_ec_rhea_cofactor_annotation",
            )
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            self.assertEqual(set(label.keys()), {
                "confidence", "entry_id", "evidence", "evidence_score",
                "fingerprint_id", "label_type", "ontology_version_at_decision",
                "rationale", "review_status", "tier",
            })

        # The already-registered accession was not re-imported.
        self.assertNotIn(
            "uniprot:P09999", {l["entry_id"] for l in audit["applied_labels"]}
        )


if __name__ == "__main__":
    unittest.main()
