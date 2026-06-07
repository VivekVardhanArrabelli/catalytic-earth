from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.family_label_admission import (
    ADMISSION_STATES,
    build_family_label_admission_pipeline,
    classify_family_label_admission_row,
    sha256_path,
    write_family_label_admission_pipeline,
)
from catalytic_earth.northstar_next_levers import (
    build_fold_augmented_family_panel_expert_import_decision_application,
)


def _write(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path


class FamilyLabelAdmissionTests(unittest.TestCase):
    def test_row_state_classification(self) -> None:
        cases = [
            (
                "countable_candidate",
                {
                    "countability_gate": {
                        "countable_label_candidate": True,
                    }
                },
            ),
            (
                "review_only_evidence",
                {
                    "accepted_import_preview": {
                        "entry_id": "row_review",
                    }
                },
            ),
            (
                "review_only_evidence",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "expert_family_admission_decision_required"
                        ),
                    },
                    "expert_application": {
                        "decision": (
                            "explicit_accept_family_panel_import_candidate"
                        ),
                        "critical_violations": [],
                    },
                },
            ),
            (
                "review_only_evidence",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "expert_family_admission_decision_required"
                        ),
                    },
                    "expert_application": {
                        "decision": (
                            "keep_family_panel_review_only_require_more_evidence"
                        ),
                        "critical_violations": [],
                    },
                },
            ),
            (
                "oos_hard_negative",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "completed_source_check_review_only_no_promotion"
                        ),
                    }
                },
            ),
            (
                "blocked_locator",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "source_free_locator_or_primary_channel_missing"
                        ),
                        "locator_decision_class": (
                            "accession_equivalence_or_matching_coordinate_required"
                        ),
                        "locator_resolution_status": (
                            "blocked_accession_mismatch_requested_afdb_position_mismatch"
                        ),
                    }
                },
            ),
            (
                "blocked_coordinate",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "source_free_locator_or_primary_channel_missing"
                        ),
                        "locator_decision_class": (
                            "alternate_coordinate_fetch_approval_required"
                        ),
                    }
                },
            ),
            (
                "blocked_family_decision",
                {
                    "import_preview_blocker": {
                        "primary_blocker_class": (
                            "expert_family_admission_decision_required"
                        ),
                    }
                },
            ),
            (
                "reject_preserve_signal",
                {
                    "expert_application": {
                        "decision": "reject_family_panel_import_candidate",
                    }
                },
            ),
        ]

        for expected, row in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    classify_family_label_admission_row(row)["state"],
                    expected,
                )

    def test_build_pipeline_preserves_hashes_and_guardrails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family = _write(
                root / "family.json",
                {
                    "candidate_families": [
                        {
                            "candidate_family": "panel_a",
                            "candidate_rows": ["row_family", "row_oos", "row_coord"],
                            "candidate_sources": ["review packet"],
                            "priority_bins": ["cofactor_confounded_oos"],
                            "required_human_validation": "expert decision",
                        }
                    ]
                },
            )
            preflight = _write(
                root / "preflight.json",
                {
                    "row_gate_status": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "gate_blockers": ["review_packet_not_expert_import_decision"],
                            "research_gate_status": "abstained_at_research_threshold",
                        },
                        {
                            "entry_id": "row_oos",
                            "panel_id": "panel_a",
                            "gate_blockers": [
                                "completed_source_check_not_family_promotion_ready"
                            ],
                            "source_check_completion_status": (
                                "completed_review_only_no_label_change"
                            ),
                            "source_check_family_promotion_ready": False,
                        },
                        {
                            "entry_id": "row_coord",
                            "panel_id": "panel_a",
                            "gate_blockers": ["primary_channel_score_missing"],
                        },
                    ]
                },
            )
            blocker = _write(
                root / "blocker.json",
                {
                    "row_blockers": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "primary_blocker_class": (
                                "expert_family_admission_decision_required"
                            ),
                            "research_gate_status": "abstained_at_research_threshold",
                        },
                        {
                            "entry_id": "row_oos",
                            "panel_id": "panel_a",
                            "primary_blocker_class": (
                                "completed_source_check_review_only_no_promotion"
                            ),
                            "source_check_completion_status": (
                                "completed_review_only_no_label_change"
                            ),
                            "source_check_family_promotion_ready": False,
                        },
                        {
                            "entry_id": "row_coord",
                            "panel_id": "panel_a",
                            "primary_blocker_class": (
                                "source_free_locator_or_primary_channel_missing"
                            ),
                            "locator_decision_class": (
                                "alternate_coordinate_fetch_approval_required"
                            ),
                            "locator_decision_needed": "Approve frozen alternate coordinate.",
                        },
                    ]
                },
            )
            packet = _write(
                root / "packet.json",
                {
                    "expert_import_decision_stubs": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "review_status": "pending_expert_import_decision",
                            "decision_context_sha256": "a" * 64,
                            "allowed_decisions": [
                                "explicit_accept_family_panel_import_candidate",
                                "reject_family_panel_import_candidate",
                                "keep_family_panel_review_only_require_more_evidence",
                            ],
                        }
                    ]
                },
            )
            scenario = _write(
                root / "scenario.json",
                {
                    "acceptance_scenario_rows": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "would_enter_import_preview_if_accepted": True,
                        }
                    ]
                },
            )
            application = _write(
                root / "application.json",
                {
                    "row_decisions": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "decision": "pending_review",
                            "review_status": "pending_expert_import_decision",
                            "critical_violations": [],
                        }
                    ]
                },
            )
            preview = _write(root / "preview.json", {"accepted_import_preview_rows": []})
            readiness = _write(root / "readiness.json", {"label_factory_gate_input_rows": []})
            research = _write(
                root / "research.json",
                {
                    "row_scores": [
                        {
                            "entry_id": "row_family",
                            "panel_id": "panel_a",
                            "primary_threshold": 0.44155,
                            "research_gate_status": "abstained_at_research_threshold",
                        }
                    ]
                },
            )
            locator = _write(
                root / "locator.json",
                {
                    "row_decisions": [
                        {
                            "entry_id": "row_coord",
                            "resolution_class": (
                                "alternate_coordinate_fetch_approval_required"
                            ),
                            "next_action": "approve coordinate",
                        }
                    ]
                },
            )
            retrieval = _write(
                root / "retrieval.json",
                {
                    "row_scores": [
                        {
                            "entry_id": "row_coord",
                            "predicted_geometry_status": "blocked",
                        }
                    ]
                },
            )
            evidence = _write(
                root / "evidence.json",
                {
                    "panel": {"candidate_family": "panel_a"},
                    "row_evidence": [
                        {
                            "entry_id": "row_family",
                            "evidence_role": "review decision candidate",
                            "selected_organic_cofactor_max": 0.7,
                        },
                        {
                            "entry_id": "row_oos",
                            "evidence_role": "boundary OOS signal",
                        },
                    ],
                },
            )

            out = root / "out.json"
            report = root / "report.md"
            decision_template = root / "decision_template.json"
            audit = write_family_label_admission_pipeline(
                family_set_expansion_targets_path=family,
                countability_gate_preflight_path=preflight,
                import_preview_blocker_gate_path=blocker,
                expert_import_decision_packet_path=packet,
                acceptance_scenario_plan_path=scenario,
                expert_import_decision_application_path=application,
                accepted_import_preview_path=preview,
                label_factory_gate_readiness_path=readiness,
                research_readout_path=research,
                locator_human_decision_matrix_path=locator,
                source_free_predicted_geometry_retrieval_path=retrieval,
                evidence_packet_paths=[evidence],
                out_path=out,
                report_path=report,
                expert_decision_template_path=decision_template,
                created_utc="2026-06-07T22:22:55Z",
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertTrue(decision_template.exists())
            self.assertEqual(audit["created_utc"], "2026-06-07T22:22:55Z")
            self.assertEqual(audit["counts"]["candidate_rows_evaluated"], 3)
            self.assertEqual(
                audit["counts"]["admission_state_counts"]["blocked_family_decision"],
                1,
            )
            self.assertEqual(
                audit["counts"]["admission_state_counts"]["oos_hard_negative"],
                1,
            )
            self.assertEqual(
                audit["counts"]["admission_state_counts"]["blocked_coordinate"],
                1,
            )
            self.assertFalse(audit["guardrails"]["imports_or_promotions_performed"])
            self.assertFalse(
                audit["guardrails"]["labels_registries_ontologies_changed"]
            )
            self.assertTrue(audit["state_assignment_audit"]["passed"])
            self.assertEqual(
                audit["state_assignment_audit"]["rows_with_exactly_one_state"],
                3,
            )
            action_queue = audit["family_expansion_action_queue"]
            self.assertEqual(action_queue["queue_status"], "ready")
            self.assertEqual(action_queue["recommended_next_item"]["entry_id"], "row_family")
            self.assertEqual(
                action_queue["recommended_next_item"]["action_class"],
                "expert_family_admission_decision",
            )
            self.assertEqual(
                action_queue["recommended_next_item"]["evidence_summary"][
                    "decision_context_sha256"
                ],
                "a" * 64,
            )
            self.assertIn(
                "family_panel_accepted_import_preview",
                action_queue["recommended_next_item"][
                    "machinery_to_rerun_after_resolution"
                ],
            )
            self.assertEqual(
                action_queue["counts_by_action_class"][
                    "coordinate_or_coordinate_policy_resolution"
                ],
                1,
            )
            decision_intake = audit["expert_decision_intake_packet"]
            self.assertEqual(
                decision_intake["status"],
                "awaiting_expert_family_decisions",
            )
            self.assertEqual(decision_intake["counts"]["template_rows"], 1)
            self.assertEqual(
                decision_intake["counts"]["previewable_if_accepted_rows"],
                1,
            )
            template_row = decision_intake["template_rows"][0]
            self.assertEqual(template_row["entry_id"], "row_family")
            self.assertEqual(template_row["decision_context_sha256"], "a" * 64)
            self.assertEqual(
                template_row["required_decision_record"],
                {
                    "entry_id": "row_family",
                    "decision_context_sha256": "a" * 64,
                    "decision": "<one of allowed_decisions>",
                    "review_status": "reviewed_expert_import_decision",
                },
            )
            self.assertFalse(template_row["validation_blockers"])
            self.assertIn(
                "apply-fold-augmented-family-panel-expert-import-decision",
                decision_intake["application_commands_after_review"][0],
            )
            self.assertEqual(
                audit["counts"]["expert_decision_review_template_rows"],
                1,
            )
            self.assertEqual(
                audit["operational_output_paths"][
                    "expert_decision_review_template"
                ],
                str(decision_template),
            )
            template_payload = json.loads(
                decision_template.read_text(encoding="utf-8")
            )
            self.assertEqual(
                template_payload["status"],
                "expert_decision_template_pending_review",
            )
            self.assertEqual(
                template_payload["counts"],
                {
                    "decision_rows": 1,
                    "pending_review_rows": 1,
                    "previewable_if_accepted_rows": 1,
                    "reviewed_rows": 0,
                },
            )
            template_decision = template_payload["expert_import_decisions"][0]
            self.assertEqual(template_decision["entry_id"], "row_family")
            self.assertEqual(template_decision["decision"], "pending_review")
            self.assertEqual(
                template_decision["review_status"],
                "pending_expert_import_decision",
            )
            self.assertEqual(
                template_decision["decision_context_sha256"],
                "a" * 64,
            )
            self.assertEqual(
                template_decision["source_hashes"],
                template_row["source_hashes"],
            )
            self.assertEqual(
                template_decision["evidence_summary"],
                template_row["evidence_summary"],
            )
            application_from_template = (
                build_fold_augmented_family_panel_expert_import_decision_application(
                    expert_import_decision_packet_path=packet,
                    expert_decisions_path=decision_template,
                )
            )
            self.assertEqual(
                application_from_template["status"],
                "family_panel_expert_import_decision_application_blocked",
            )
            self.assertEqual(
                application_from_template["counts"][
                    "accepted_import_preview_candidate_rows"
                ],
                0,
            )
            self.assertEqual(
                application_from_template["counts"]["pending_decision_rows"],
                1,
            )
            self.assertEqual(
                audit["source_artifacts"]["family_set_expansion_targets"]["sha256"],
                sha256_path(family),
            )
            for row in audit["row_admission_table"]:
                self.assertIn(row["admission_state"], ADMISSION_STATES)
                self.assertEqual(len(row["row_context_sha256"]), 64)
                self.assertIn("family_set_expansion_targets", row["source_hashes"])
                if row["entry_id"] == "row_family":
                    self.assertIn("acceptance_scenario_plan", row["source_hashes"])

    def test_accepted_expert_decision_routes_to_import_preview_build(self) -> None:
        row = {
            "import_preview_blocker": {
                "primary_blocker_class": "expert_family_admission_decision_required",
            },
            "expert_application": {
                "decision": "explicit_accept_family_panel_import_candidate",
                "review_status": "reviewed_expert_import_decision",
                "critical_violations": [],
            },
        }
        classification = classify_family_label_admission_row(row)
        self.assertEqual(classification["state"], "review_only_evidence")
        self.assertEqual(
            classification["blocker_class"],
            "accepted_expert_decision_waiting_import_preview",
        )
        self.assertIn("accepted import-preview", classification["allowed_next_action"])

    def test_missing_required_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            missing = root / "missing.json"
            existing = _write(root / "existing.json", {})
            with self.assertRaises(FileNotFoundError):
                build_family_label_admission_pipeline(
                    family_set_expansion_targets_path=missing,
                    countability_gate_preflight_path=existing,
                    import_preview_blocker_gate_path=existing,
                    expert_import_decision_packet_path=existing,
                    acceptance_scenario_plan_path=existing,
                    expert_import_decision_application_path=existing,
                    accepted_import_preview_path=existing,
                    label_factory_gate_readiness_path=existing,
                    research_readout_path=existing,
                    locator_human_decision_matrix_path=existing,
                    source_free_predicted_geometry_retrieval_path=existing,
                    evidence_packet_paths=[existing],
                )


if __name__ == "__main__":
    unittest.main()
