from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_annotation_anchored_import import (
    apply_external_annotation_anchored_import_to_registry,
    build_external_annotation_anchored_import,
    classify_row,
    cofactor_classes,
)
from catalytic_earth.labels import MechanismLabel


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


class ApplyToSeparateRegistryTests(unittest.TestCase):
    def test_writes_expansion_registry_and_leaves_benchmark_untouched(self) -> None:
        preview_rows = [
            _row("metal hydrolase", cofactors=["Zn(2+)"], accession="P00001"),
            _row("glycoside/nucleoside", accession="P00002"),
        ]
        frozen = [
            {
                "confidence": "medium",
                "entry_id": "m_csa:1",
                "evidence": {"sources": ["curator_rationale"]},
                "evidence_score": 0.65,
                "fingerprint_id": None,
                "label_type": "out_of_scope",
                "ontology_version_at_decision": "label_factory_v1_8fp",
                "rationale": "frozen benchmark label kept stable for the contract.",
                "review_status": "automation_curated",
                "tier": "bronze",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            preview_artifact = build_external_annotation_anchored_import(
                preview=preview_rows, registry=frozen
            )
            preview_path = tmp / "preview.json"
            preview_path.write_text(json.dumps(preview_artifact), encoding="utf-8")
            frozen_path = tmp / "frozen.json"
            frozen_bytes_before = json.dumps(frozen)
            frozen_path.write_text(frozen_bytes_before, encoding="utf-8")
            expansion_path = tmp / "expansion.json"

            summary = apply_external_annotation_anchored_import_to_registry(
                preview_path=preview_path,
                expansion_registry_path=expansion_path,
                frozen_benchmark_registry_path=frozen_path,
            )

            # Frozen benchmark file is never written.
            self.assertFalse(summary["frozen_benchmark_registry_written"])
            self.assertEqual(frozen_path.read_text(encoding="utf-8"), frozen_bytes_before)

            # Expansion registry holds the 2 importable labels; combined total = 3.
            self.assertEqual(summary["appended"], 2)
            self.assertEqual(summary["expansion_registry_after"], 2)
            self.assertEqual(summary["combined_total_labels"], 3)
            expansion = json.loads(expansion_path.read_text(encoding="utf-8"))
            # Every written label validates through the canonical schema.
            for label in expansion:
                MechanismLabel.from_dict(label)
                self.assertTrue(label["entry_id"].startswith("uniprot:"))
                self.assertEqual(label["tier"], "bronze")

            # Re-applying dedups (idempotent on entry_id), no double-count.
            summary2 = apply_external_annotation_anchored_import_to_registry(
                preview_path=preview_path,
                expansion_registry_path=expansion_path,
                frozen_benchmark_registry_path=frozen_path,
            )
            self.assertEqual(summary2["appended"], 0)
            self.assertEqual(summary2["duplicate_skipped"], 2)
            self.assertEqual(summary2["expansion_registry_after"], 2)


class SourceTimeSequenceProvenanceTests(unittest.TestCase):
    def test_build_label_records_deploy_input_sequence_when_row_carries_it(self) -> None:
        # A canonical ingestion-pilot row that carries the raw sequence (the deploy
        # input). _build_label records it under evidence.sequence_provenance natively.
        sequence = "M" + "Q" * 80
        row = _row("metal hydrolase", cofactors=["Zn(2+)"], accession="P12345")
        row.update(
            {
                "sequence": sequence,
                "sequence_length": len(sequence),
                "reviewed_status": "reviewed",
                "source_provenance": {"query_timestamp_utc": "2026-06-11T00:00:00Z"},
                "source_hashes": {"source_query_sha256": "deadbeef"},
            }
        )
        audit = build_external_annotation_anchored_import(preview=[row], registry=[])
        label = audit["applied_labels"][0]
        provenance = label["evidence"]["sequence_provenance"]
        self.assertEqual(provenance["sequence"], sequence)
        self.assertEqual(provenance["sequence_length"], len(sequence))
        self.assertEqual(provenance["source_accession"], "P12345")
        self.assertEqual(provenance["source"], "reviewed_uniprot")
        self.assertEqual(len(provenance["sequence_sha256"]), 64)
        # Sequence is stored data only; the leakage channels are unchanged.
        self.assertEqual(label["evidence"]["predictive_evidence"], [])
        self.assertNotIn(
            "sequence_provenance", label["evidence"]["excluded_context"]
        )
        # Round-trips through the canonical (leakage-aware) schema.
        MechanismLabel.from_dict(label)

    def test_build_label_omits_sequence_provenance_when_row_has_no_sequence(self) -> None:
        row = _row("metal hydrolase", cofactors=["Zn(2+)"], accession="P54321")
        audit = build_external_annotation_anchored_import(preview=[row], registry=[])
        label = audit["applied_labels"][0]
        self.assertNotIn("sequence_provenance", label["evidence"])


if __name__ == "__main__":
    unittest.main()
