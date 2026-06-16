from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.bronze_preview_row_guardrails import (
    audit_bronze_preview_rows,
    write_bronze_preview_row_guardrails,
)


def _label(**overrides):
    label = {
        "entry_id": "uniprot:PDE001",
        "fingerprint_id": "metal_independent_phosphodiesterase",
        "tier": "bronze",
        "review_status": "automation_curated",
        "evidence": {
            "excluded_context": [
                "protein_name",
                "ec_label",
                "uniprot_prose",
                "source_annotation",
                "target_family_lane",
            ],
            "import_gate_evidence": [
                "current702_accession_sequence_duplicate_screen_clear",
                "mechanism_axis:domain_or_family_profile",
                "mechanism_axis:rhea_reaction_or_participant_pattern",
            ],
            "predictive_evidence": [],
            "source_trust_tier": {
                "source_tier": "source_tier_0",
                "meets_n_of_m": True,
                "mechanism_corroborator_axes_present": [
                    "domain_or_family_profile",
                    "rhea_reaction_or_participant_pattern",
                ],
            },
        },
    }
    label.update(overrides)
    return label


class BronzePreviewRowGuardrailTests(unittest.TestCase):
    def test_valid_preview_passes(self):
        audit = audit_bronze_preview_rows(
            {"applied_labels": [_label()]},
            expected_fingerprint="metal_independent_phosphodiesterase",
            expected_source_tier="source_tier_0",
            created_utc="2026-06-16T01:30:00Z",
        )
        self.assertEqual(audit["status"], "row_guardrail_audit_passed")
        self.assertEqual(audit["counts"]["problem_rows"], 0)
        self.assertEqual(
            audit["counts"]["fingerprint_counts"],
            {"metal_independent_phosphodiesterase": 1},
        )
        self.assertTrue(audit["guardrails"]["ec_name_query_handles_scope_admission_only"])

    def test_leakage_and_namespace_problems_fail(self):
        bad = _label(entry_id="PDE001")
        bad["evidence"]["predictive_evidence"] = ["protein_name:phosphodiesterase"]
        bad["evidence"]["source_trust_tier"]["mechanism_corroborator_axes_present"] = [
            "ec_scope_hint"
        ]

        audit = audit_bronze_preview_rows({"applied_labels": [bad]})

        self.assertEqual(audit["status"], "row_guardrail_audit_failed")
        fields = {row["field"] for row in audit["problem_rows"]}
        self.assertIn("entry_id", fields)
        self.assertIn("predictive_evidence", fields)
        self.assertIn("source_trust_tier", fields)

    def test_writer_emits_json_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview = root / "preview.json"
            out = root / "audit.json"
            report = root / "audit.md"
            preview.write_text(json.dumps({"applied_labels": [_label()]}), encoding="utf-8")

            audit = write_bronze_preview_row_guardrails(
                preview_path=preview,
                out_path=out,
                report_path=report,
                expected_fingerprint="metal_independent_phosphodiesterase",
            )

            self.assertEqual(audit["counts"]["problem_rows"], 0)
            self.assertTrue(out.exists())
            self.assertIn("Bronze Preview Row Guardrail Audit", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
