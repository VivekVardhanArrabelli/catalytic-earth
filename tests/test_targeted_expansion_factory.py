from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cli import build_parser
from catalytic_earth.targeted_expansion_factory import (
    build_targeted_expansion_factory_batch,
    render_targeted_expansion_report,
    write_targeted_expansion_factory_batch,
)


def _source_records(*names: str) -> dict[str, dict[str, object]]:
    return {
        name: {
            "path": f"artifacts/{name}.json",
            "sha256": f"{index + 1:064x}",
            "bytes": 10,
        }
        for index, name in enumerate(names)
    }


class TargetedExpansionFactoryTests(unittest.TestCase):
    def test_routes_dedupes_and_preserves_source_hashes(self) -> None:
        source_payloads = {
            "active_learning_1025_preview": {
                "rows": [
                    {
                        "entry_id": "m_csa:10",
                        "entry_name": "architecture default row",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "recommended_action": "expert_label_decision_needed",
                    },
                    {
                        "entry_id": "m_csa:200",
                        "entry_name": "locator gap row",
                        "readiness_blockers": ["fewer_than_three_resolved_residues"],
                        "top1_fingerprint_id": "plp_dependent_enzyme",
                    },
                    {
                        "entry_id": "m_csa:201",
                        "entry_name": "hard negative row",
                        "current_label_type": "out_of_scope",
                        "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                    },
                ]
            },
            "external_panel_router_queue": {
                "queue_rows": [
                    {
                        "candidate_id": "uniprot:P00001",
                        "display_name": "external glycan candidate",
                        "source_panels": ["glycoside_carbohydrate"],
                        "panel_roles": ["positive"],
                        "ready_for_label_import": False,
                    }
                ]
            },
            "external_hard_negative_next_sourcing": {
                "rows": [
                    {
                        "entry_id": "uniprot:P00001",
                        "accession": "P00001",
                        "lane_id": "external_source:glycan_chemistry",
                        "sourcing_status": (
                            "sourced_pending_sequence_structure_distance_screens"
                        ),
                        "active_site_evidence_status": (
                            "explicit_active_site_and_catalytic_activity_source_present"
                        ),
                        "next_required_screens": [
                            "current_reference_backend_sequence_search",
                            "current_countable_foldseek_structural_screen",
                        ],
                    }
                ]
            },
            "architecture_default_decisions": {"expert_import_decisions": []},
        }
        source_records = _source_records(*source_payloads)

        artifact = build_targeted_expansion_factory_batch(
            source_payloads=source_payloads,
            source_records=source_records,
            created_utc="2026-06-08T00:00:00Z",
            min_target_candidates=3,
        )

        self.assertTrue(artifact["state_assignment_audit"]["passed"])
        self.assertEqual(artifact["candidate_count"], 4)
        rows = {row["candidate_id"]: row for row in artifact["candidate_rows"]}
        self.assertEqual(
            rows["m_csa:10"]["admission_state"],
            "reject/OOS_preserve_signal",
        )
        self.assertEqual(
            rows["m_csa:10"]["admission_route_basis"],
            "architecture_default_non_counting_disposition_reused",
        )
        self.assertIn(
            "architecture_default_decisions",
            rows["m_csa:10"]["source_hashes"],
        )
        self.assertEqual(rows["m_csa:200"]["admission_state"], "blocked_locator")
        self.assertEqual(
            rows["m_csa:201"]["family_axis"],
            "redox_oxygen_transfer_and_sulfur_lipoamide",
        )
        self.assertEqual(
            rows["uniprot:P00001"]["admission_state"],
            "acquisition_needed",
        )
        self.assertEqual(
            rows["uniprot:P00001"]["family_axis"],
            "glycoside_or_nucleoside_hydrolase_controls",
        )
        self.assertEqual(
            rows["uniprot:P00001"]["mechanical_unblock_requirements"][
                "next_required_screens"
            ],
            [
                "current_countable_foldseek_structural_screen",
                "current_reference_backend_sequence_search",
            ],
        )
        self.assertEqual(
            set(rows["uniprot:P00001"]["source_hashes"]),
            {
                "external_panel_router_queue",
                "external_hard_negative_next_sourcing",
            },
        )
        self.assertTrue(
            artifact["target_policy"][
                "human_review_required_only_for_countable_promotion"
            ]
        )
        self.assertEqual(artifact["evidence_coverage"]["source_hashes_present"], 4)
        self.assertGreaterEqual(len(artifact["action_queues"]), 3)
        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertEqual(
            artifact["validation_checks"]["source_hash_violation_count"],
            0,
        )
        self.assertEqual(
            artifact["validation_checks"]["row_hash_violation_count"],
            0,
        )
        self.assertEqual(
            artifact["validation_checks"]["forbidden_field_violation_count"],
            0,
        )
        self.assertEqual(
            artifact["acquisition_plan"]["required_screen_counts"],
            {
                "current_countable_foldseek_structural_screen": 1,
                "current_reference_backend_sequence_search": 1,
            },
        )
        report = render_targeted_expansion_report(artifact)
        self.assertIn("Architecture Defaults Reused", report)
        self.assertIn("Screen-ready acquisition rows", report)
        self.assertIn(
            "`uniprot:P00001` via `glycoside_or_nucleoside_hydrolase_controls`",
            report,
        )

    def test_write_batch_materializes_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_paths = {
                "active_learning_1025_preview": root / "active.json",
                "external_panel_router_queue": root / "external.json",
                "architecture_default_decisions": root / "architecture.json",
            }
            source_paths["active_learning_1025_preview"].write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:9999",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "cofactor_evidence_level": "ligand_supported",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            source_paths["external_panel_router_queue"].write_text(
                json.dumps({"queue_rows": []}),
                encoding="utf-8",
            )
            source_paths["architecture_default_decisions"].write_text(
                json.dumps({"expert_import_decisions": []}),
                encoding="utf-8",
            )
            out = root / "batch.json"
            report = root / "batch.md"

            artifact = write_targeted_expansion_factory_batch(
                out_path=out,
                report_path=report,
                source_paths=source_paths,
                created_utc="2026-06-08T00:00:01Z",
                min_target_candidates=1,
            )

            self.assertEqual(artifact["candidate_count"], 1)
            self.assertTrue(out.exists())
            self.assertIn(
                "Targeted Expansion Factory Batch",
                report.read_text(encoding="utf-8"),
            )

    def test_materializes_architecture_default_rows_as_carryover(self) -> None:
        source_payloads = {
            "architecture_default_decisions": {
                "expert_import_decisions": [
                    {
                        "entry_id": "m_csa:448",
                        "architecture_default": True,
                        "architecture_policy_name": (
                            "family_admission_architecture_default_v1"
                        ),
                        "decision": (
                            "keep_family_panel_review_only_require_more_evidence"
                        ),
                        "decision_context_sha256": "a" * 64,
                        "panel_id": "lipoamide_or_sulfur_transfer_redox_boundary",
                        "review_status": "reviewed_expert_import_decision",
                        "row_context_sha256": "b" * 64,
                    }
                ]
            }
        }
        source_records = _source_records(*source_payloads)

        artifact = build_targeted_expansion_factory_batch(
            source_payloads=source_payloads,
            source_records=source_records,
            created_utc="2026-06-08T00:00:02Z",
            min_target_candidates=1,
        )

        self.assertEqual(artifact["candidate_count"], 1)
        row = artifact["candidate_rows"][0]
        self.assertEqual(row["candidate_id"], "m_csa:448")
        self.assertEqual(row["admission_state"], "review_only_evidence")
        self.assertEqual(
            row["family_axis"],
            "redox_oxygen_transfer_and_sulfur_lipoamide",
        )
        self.assertEqual(row["sources"], ["architecture_default_decisions"])
        self.assertIn(
            "Architecture/source panel: lipoamide_or_sulfur_transfer_redox_boundary.",
            row["rationale"],
        )

    def test_cli_command_is_registered(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            [
                "build-targeted-expansion-factory-batch",
                "--source-path",
                "active_learning_1025_preview=/tmp/active.json",
            ]
        )

        self.assertEqual(
            args.func.__name__,
            "cmd_build_targeted_expansion_factory_batch",
        )
        self.assertEqual(
            args.source_path,
            ["active_learning_1025_preview=/tmp/active.json"],
        )


if __name__ == "__main__":
    unittest.main()
