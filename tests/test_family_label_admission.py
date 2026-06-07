from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cli import build_parser
from catalytic_earth.family_label_admission import (
    ADMISSION_STATES,
    build_family_label_admission_pipeline,
    classify_admission_state,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FamilyLabelAdmissionTests(unittest.TestCase):
    def test_classifier_covers_contract_states(self) -> None:
        cases = [
            (
                "countable_candidate",
                {"entry_id": "a", "ready_for_label_factory_gate": True},
                {},
                None,
            ),
            (
                "review_only_evidence",
                {
                    "entry_id": "b",
                    "primary_blocker_class": "completed_source_check_review_only_no_promotion",
                },
                {},
                None,
            ),
            (
                "oos_hard_negative",
                {"entry_id": "c", "oos_hard_negative": True},
                {},
                None,
            ),
            (
                "blocked_locator",
                {
                    "entry_id": "d",
                    "primary_blocker_class": "source_free_locator_or_primary_channel_missing",
                    "locator_decision_class": "nonlabel_locator_strategy_or_alternate_source_required",
                },
                {},
                None,
            ),
            (
                "blocked_coordinate",
                {
                    "entry_id": "e",
                    "primary_blocker_class": "source_free_locator_or_primary_channel_missing",
                    "locator_decision_class": "accession_equivalence_or_matching_coordinate_required",
                },
                {},
                None,
            ),
            (
                "blocked_family_decision",
                {
                    "entry_id": "f",
                    "primary_blocker_class": "expert_family_admission_decision_required",
                },
                {},
                None,
            ),
            (
                "reject_preserve_signal",
                {"entry_id": "g", "primary_blocker_class": "unknown"},
                {"decision": "reject_family_panel_import_candidate"},
                None,
            ),
        ]

        observed = {
            classify_admission_state(
                row,
                expert_stub=expert_stub,
                locator_row=locator_row,
            )["state"]
            for _, row, expert_stub, locator_row in cases
        }

        self.assertEqual(observed, ADMISSION_STATES)

    def test_build_preserves_source_hashes_and_row_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            blocker_gate = root / "blocker_gate.json"
            expert_packet = root / "expert_packet.json"
            locator_matrix = root / "locator_matrix.json"
            evidence_packet = root / "evidence_packet.json"
            countability = root / "countability.json"
            source_check = root / "source_check.json"
            source_check_detail = root / "source_check_detail.json"

            _write_json(
                blocker_gate,
                {
                    "row_blockers": [
                        {
                            "entry_id": "mh_065",
                            "panel_id": "panel_a",
                            "primary_blocker_class": "source_free_locator_or_primary_channel_missing",
                            "locator_decision_class": "accession_equivalence_or_matching_coordinate_required",
                            "locator_resolution_status": "blocked_accession_mismatch",
                            "gate_blockers": ["source_free_locator_human_or_policy_decision_required"],
                            "ready_for_import_preview": False,
                            "ready_for_label_factory_gate": False,
                            "countable_label_candidate": False,
                            "research_gate_status": "not_score_complete_for_primary_channel",
                        }
                    ]
                },
            )
            _write_json(
                expert_packet,
                {
                    "expert_import_decision_stubs": [
                        {
                            "entry_id": "mh_065",
                            "decision_context_sha256": "a" * 64,
                            "default_decision": "pending_review",
                            "allowed_decisions": [
                                "explicit_accept_family_panel_import_candidate",
                                "reject_family_panel_import_candidate",
                            ],
                            "import_preview_candidate_if_accepted_now": False,
                            "required_actions_before_import_preview": [
                                "resolve_source_free_locator_or_coordinate_policy"
                            ],
                        }
                    ]
                },
            )
            _write_json(
                locator_matrix,
                {
                    "row_decisions": [
                        {
                            "entry_id": "mh_065",
                            "resolution_class": "accession_equivalence_or_matching_coordinate_required",
                            "resolution_status": "blocked_accession_mismatch",
                            "next_action": "Provide a frozen matching coordinate.",
                            "source_accession": "uniprot:Q79MP6",
                        }
                    ]
                },
            )
            _write_json(
                evidence_packet,
                {
                    "panel": {
                        "candidate_family": "panel_a",
                        "candidate_rows": ["mh_065"],
                        "candidate_sources": ["source"],
                    },
                    "row_evidence": [
                        {
                            "entry_id": "mh_065",
                            "benchmark_role": None,
                            "evidence_role": "cofactor-confounded OOS control",
                            "predicted_geometry_status": "missing",
                            "predicted_structure_fold_channel": {
                                "nearest_atlas_tm_score": 0.94
                            },
                        }
                    ],
                },
            )
            _write_json(
                countability,
                {
                    "row_gate_status": [
                        {
                            "entry_id": "mh_065",
                            "primary_score_complete": False,
                            "locator_resolution_class": "accession_equivalence_or_matching_coordinate_required",
                        }
                    ]
                },
            )
            _write_json(
                source_check,
                {
                    "reconciliation_rows": [
                        {
                            "entry_id": "mh_065",
                            "next_action": "Keep review-only until coordinate policy clears.",
                        }
                    ],
                    "source_check_artifact_records": [
                        {
                            "entry_id": "mh_065",
                            "path": str(source_check_detail),
                            "sha256": "",
                        }
                    ],
                },
            )
            _write_json(
                source_check_detail,
                {
                    "row": {"entry_id": "mh_065", "source_accession": "uniprot:Q79MP6"},
                    "local_source_evidence": {
                        "approved_source_free_locator_summary": {
                            "locator_policy": "human_approved_structure_local_ligand_geometry_without_source_text",
                            "residue_locator_count": 3,
                        },
                        "mechanism_locus_assessment": {
                            "row_specific_bond_change_sidecar_status": "not_extracted"
                        },
                    },
                    "source_check_decision": {
                        "source_check_result": "hold_review_only"
                    },
                },
            )
            source_check_payload = json.loads(source_check.read_text(encoding="utf-8"))
            source_check_payload["source_check_artifact_records"][0][
                "sha256"
            ] = _sha256(source_check_detail)
            _write_json(source_check, source_check_payload)

            artifact = build_family_label_admission_pipeline(
                import_preview_blocker_gate_path=blocker_gate,
                expert_import_decision_packet_path=expert_packet,
                countability_gate_preflight_path=countability,
                locator_human_decision_matrix_path=locator_matrix,
                source_check_completion_reconciliation_path=source_check,
                family_panel_evidence_packet_paths=[evidence_packet],
                created_utc="2026-06-07T00:00:00Z",
            )
            expected_blocker_hash = _sha256(blocker_gate)

        row = artifact["row_admission_table"][0]
        self.assertEqual(row["admission_state"], "blocked_coordinate")
        self.assertEqual(
            artifact["source_artifacts"][blocker_gate.stem]["sha256"],
            expected_blocker_hash,
        )
        self.assertEqual(
            row["human_decision_provenance"]["decision_context_sha256"],
            "a" * 64,
        )
        self.assertEqual(
            row["locator_provenance"]["source_accession"],
            "uniprot:Q79MP6",
        )
        self.assertEqual(
            row["evidence_preserved"]["predicted_structure_fold_channel"][
                "nearest_atlas_tm_score"
            ],
            0.94,
        )
        self.assertTrue(
            row["source_check_provenance"]["detail_preserved"][
                "sha256_matches_record"
            ]
        )
        self.assertEqual(
            row["source_check_provenance"]["detail_preserved"][
                "approved_source_free_locator_summary"
            ]["residue_locator_count"],
            3,
        )

    def test_guardrails_and_fail_closed_missing_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            blocker_gate = root / "blocker_gate.json"
            expert_packet = root / "expert_packet.json"
            _write_json(
                blocker_gate,
                {
                    "row_blockers": [
                        {
                            "entry_id": "m_csa:30",
                            "panel_id": "panel_a",
                            "primary_blocker_class": "expert_family_admission_decision_required",
                        }
                    ]
                },
            )
            _write_json(
                expert_packet,
                {
                    "expert_import_decision_stubs": [
                        {
                            "entry_id": "m_csa:30",
                            "default_decision": "pending_review",
                        }
                    ]
                },
            )
            artifact = build_family_label_admission_pipeline(
                import_preview_blocker_gate_path=blocker_gate,
                expert_import_decision_packet_path=expert_packet,
                created_utc="2026-06-07T00:00:00Z",
            )

            self.assertFalse(artifact["guardrails"]["imports_or_promotions_performed"])
            self.assertFalse(artifact["guardrails"]["model_weights_fit_or_refit"])
            self.assertEqual(
                artifact["row_admission_table"][0]["admission_state"],
                "blocked_family_decision",
            )

            _write_json(blocker_gate, {"row_blockers": []})
            with self.assertRaisesRegex(ValueError, "non-empty `row_blockers`"):
                build_family_label_admission_pipeline(
                    import_preview_blocker_gate_path=blocker_gate,
                    expert_import_decision_packet_path=expert_packet,
                )

    def test_cli_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-family-label-admission-pipeline"])

        self.assertIn("family_label_admission_pipeline", args.out)
        self.assertIn("import_preview_blocker_gate", args.import_preview_blocker_gate)
        self.assertIn("expert_import_decision_packet", args.expert_import_decision_packet)
        self.assertGreaterEqual(len(args.family_panel_evidence_packets), 7)


if __name__ == "__main__":
    unittest.main()
