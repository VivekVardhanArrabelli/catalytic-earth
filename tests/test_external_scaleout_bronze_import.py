from __future__ import annotations

import unittest

from catalytic_earth.external_scaleout_bronze_import import (
    build_current702_reference_index,
    build_scaleout_bronze_import,
    classify_scaleout_row,
    rerun_current702_duplicate_screen,
    _synthesize_plp_cofactor_provenance,
)
from catalytic_earth.labels import MechanismLabel

_NO_EXACT = "no_exact_current702_accession_or_sequence_sha_overlap"


def _index(*, current_acc=(), current_sha=(), registry_acc=()):
    return {
        "current_accessions": set(current_acc),
        "current_sequence_shas": set(current_sha),
        "registry_accessions": set(registry_acc),
    }


def _shard_row(lane, *, accession="P00001", cofactors=(), plp_flag=False,
               upstream=_NO_EXACT, seq_sha=None, ec=("4.1.1.81",), screened=_NO_EXACT):
    row = {
        "accession": accession,
        "target_family_lane": lane,
        "cofactor_provenance": [{"name": n} for n in cofactors],
        "cofactor_family_flags": {"plp_evidence_present": plp_flag},
        "duplicate_status_summary": {"current702_status": upstream},
        # Pre-set the normalized top-level screen field the classifier reads;
        # build_scaleout_bronze_import re-derives this via _normalize_row.
        "duplicate_current_registry_conflict_status": screened,
        "rhea_ec_provenance": {"ec_numbers": list(ec), "rhea_record_count": 1},
        "residue_locators": [],
        "afdb_or_pdb_identifier": "AF-%s-F1" % accession,
    }
    if seq_sha is not None:
        row["duplicate_status"] = {
            "current_registry_conflict_status": upstream,
            "exact_sequence_sha256": seq_sha,
        }
    return row


class DuplicateScreenRerunTests(unittest.TestCase):
    def test_clean_row_clears(self) -> None:
        row = _shard_row("metal hydrolase", accession="P11111")
        out = rerun_current702_duplicate_screen(row, index=_index())
        self.assertEqual(
            out["duplicate_current_registry_conflict_status"], _NO_EXACT
        )

    def test_accession_overlap_with_current702_is_flagged(self) -> None:
        row = _shard_row("metal hydrolase", accession="P22222")
        out = rerun_current702_duplicate_screen(
            row, index=_index(current_acc=["P22222"])
        )
        self.assertEqual(
            out["duplicate_current_registry_conflict_status"],
            "exact_current702_or_expansion_accession_overlap",
        )

    def test_accession_overlap_with_expansion_registry_is_flagged(self) -> None:
        # Dedup against BOTH registries: an accession already in the expansion
        # bronze registry must not clear.
        row = _shard_row("metal hydrolase", accession="P33333")
        out = rerun_current702_duplicate_screen(
            row, index=_index(registry_acc=["P33333"])
        )
        self.assertEqual(
            out["duplicate_current_registry_conflict_status"],
            "exact_current702_or_expansion_accession_overlap",
        )

    def test_sequence_sha_overlap_is_flagged(self) -> None:
        row = _shard_row("metal hydrolase", accession="P44444", seq_sha="deadbeef")
        out = rerun_current702_duplicate_screen(
            row, index=_index(current_sha=["deadbeef"])
        )
        self.assertEqual(
            out["duplicate_current_registry_conflict_status"],
            "exact_current702_sequence_sha_overlap",
        )

    def test_unconfirmed_upstream_screen_does_not_clear(self) -> None:
        row = _shard_row("metal hydrolase", accession="P55555", upstream="pending")
        out = rerun_current702_duplicate_screen(row, index=_index())
        self.assertEqual(
            out["duplicate_current_registry_conflict_status"],
            "upstream_current702_screen_not_confirmed",
        )


class ClassifyScaleoutRowTests(unittest.TestCase):
    def test_plp_catalytic_lane_with_flag_imports_positive(self) -> None:
        row = _shard_row("PLP decarboxylase", plp_flag=True)
        row["cofactor_provenance"] = _synthesize_plp_cofactor_provenance(row)
        d = classify_scaleout_row(row, pool="plp_radical_cobalamin")
        self.assertEqual(d["decision"], "import")
        self.assertEqual(d["fingerprint_id"], "plp_dependent_enzyme")

    def test_plp_lane_without_corroboration_is_held(self) -> None:
        row = _shard_row("PLP decarboxylase", plp_flag=False)
        d = classify_scaleout_row(row, pool="plp_radical_cobalamin")
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "primary_lane_without_cofactor_corroboration")

    def test_metal_hydrolase_with_metal_imports_positive(self) -> None:
        row = _shard_row("metal hydrolase", cofactors=["Zn(2+)"])
        d = classify_scaleout_row(row, pool="metal_phosphoryl_glycoside")
        self.assertEqual(d["fingerprint_id"], "metal_dependent_hydrolase")

    def test_near_orphan_lane_imports_out_of_scope(self) -> None:
        row = _shard_row("terpene synthase/lyase")
        d = classify_scaleout_row(row, pool="near_orphan_diversity")
        self.assertEqual(d["decision"], "import")
        self.assertEqual(d["label_type"], "out_of_scope")
        self.assertIsNone(d["fingerprint_id"])

    def test_whole_redox_pool_is_held(self) -> None:
        # Even a flavin-corroborated flavin lane is held inside the
        # cofactor-confounded redox pool -- do not guess.
        row = _shard_row("flavin redox boundary", cofactors=["FAD"])
        d = classify_scaleout_row(row, pool="redox_cofactor_confounded")
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(
            d["reason"], "cofactor_confounded_redox_pool_held_for_disambiguation"
        )

    def test_radical_cobalamin_lane_is_held(self) -> None:
        row = _shard_row("B12 adenosylcobalamin enzymes")
        d = classify_scaleout_row(row, pool="plp_radical_cobalamin")
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "unmapped_lane")

    def test_broad_plp_context_lane_is_held(self) -> None:
        row = _shard_row("PLP broad cofactor context", plp_flag=True)
        d = classify_scaleout_row(row, pool="plp_radical_cobalamin")
        self.assertEqual(d["decision"], "hold")

    def test_unconfirmed_screen_is_skipped(self) -> None:
        row = _shard_row("metal hydrolase", cofactors=["Zn(2+)"], upstream="pending")
        row["duplicate_current_registry_conflict_status"] = (
            "upstream_current702_screen_not_confirmed"
        )
        d = classify_scaleout_row(row, pool="metal_phosphoryl_glycoside")
        self.assertEqual(d["decision"], "skip")


class BuildScaleoutImportTests(unittest.TestCase):
    def test_end_to_end_preview_guardrails_dedup_and_leakage(self) -> None:
        index = build_current702_reference_index(
            current_manifest_payload={
                "rows": [{"entry_id": "m_csa:1", "accession": "P70000",
                          "sequence_sha256": "abc"}]
            },
            frozen_benchmark_payload=[{"entry_id": "m_csa:1"}],
            expansion_payload=[{"entry_id": "uniprot:P09999"}],
        )
        pools = [
            {
                "pool": "metal_phosphoryl_glycoside",
                "schema": "shard",
                "path": "artifacts/metal.json",
                "rows": [
                    _shard_row("metal hydrolase", accession="P00001",
                               cofactors=["Zn(2+)"]),
                    _shard_row("glycoside/nucleoside", accession="P00002"),
                    # already in current702 by accession -> skipped by screen
                    _shard_row("metal hydrolase", accession="P70000",
                               cofactors=["Zn(2+)"]),
                    # already in expansion registry -> skipped
                    _shard_row("metal hydrolase", accession="P09999",
                               cofactors=["Zn(2+)"]),
                ],
            },
            {
                "pool": "plp_radical_cobalamin",
                "schema": "shard",
                "path": "artifacts/plp.json",
                "rows": [
                    _shard_row("PLP decarboxylase", accession="P00003",
                               plp_flag=True),
                    _shard_row("B12 adenosylcobalamin enzymes", accession="P00004"),
                ],
            },
            {
                "pool": "redox_cofactor_confounded",
                "schema": "shard",
                "path": "artifacts/redox.json",
                "rows": [
                    _shard_row("flavin redox boundary", accession="P00005",
                               cofactors=["FAD"]),
                ],
            },
        ]
        audit = build_scaleout_bronze_import(
            pools=pools, registry=[{"entry_id": "uniprot:P09999"}], index=index
        )

        c = audit["counts"]
        # P00001 (metal seed), P00002 (oos), P00003 (plp seed) = 3 importable.
        self.assertEqual(c["importable_new_labels"], 3)
        self.assertEqual(c["label_type_counts"]["seed_fingerprint"], 2)
        self.assertEqual(c["label_type_counts"]["out_of_scope"], 1)
        self.assertEqual(c["fingerprint_counts"]["plp_dependent_enzyme"], 1)
        self.assertEqual(c["fingerprint_counts"]["metal_dependent_hydrolase"], 1)
        # Redox pool fully held; B12 held; P70000/P09999 screened/deduped out.
        self.assertFalse(audit["guardrails"]["curated_registry_written"])
        self.assertFalse(
            audit["guardrails"]["predictive_features_use_ec_name_or_prose"]
        )
        self.assertTrue(audit["guardrails"]["cofactor_confounded_redox_pool_held"])

        for label in audit["applied_labels"]:
            MechanismLabel.from_dict(label)
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            self.assertIn("ec_label", label["evidence"]["excluded_context"])
            self.assertEqual(
                label["evidence"]["sources"], ["external_scaleout_bronze_import"]
            )

        # The redox accession was never imported.
        self.assertNotIn(
            "uniprot:P00005", {l["entry_id"] for l in audit["applied_labels"]}
        )


if __name__ == "__main__":
    unittest.main()
