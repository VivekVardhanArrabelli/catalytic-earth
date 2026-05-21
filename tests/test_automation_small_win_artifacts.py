import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class AutomationSmallWinArtifactsTest(unittest.TestCase):
    def test_epk_subagent_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(ARTIFACTS / "v3_epk_subagent_synthesis_20260520.json")
        metadata = synthesis["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_files_edited"])

        self.assertEqual(
            synthesis["synthesis_conclusion"]["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(
            synthesis["synthesis_conclusion"]["substrate_role_axis"],
            "not_freeze_ready",
        )
        self.assertEqual(
            synthesis["synthesis_conclusion"]["ligand_state_policy"],
            "freeze_as_review_only_future_tranche_policy_only",
        )
        self.assertEqual(len(synthesis["input_packet_validation"]), 4)
        self.assertTrue(
            all(row["json_valid"] for row in synthesis["input_packet_validation"])
        )

    def test_epk_research_lane_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_research_lane_synthesis_20260520.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_files_edited"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])
        self.assertEqual(metadata["lane_count"], 4)
        self.assertEqual(metadata["lane_json_validation_error_count"], 0)
        self.assertTrue(metadata["fresh_lane_outputs_since_prior_synthesis"])
        self.assertTrue(metadata["integrates_uncommitted_sibling_worktree_outputs"])
        self.assertEqual(metadata["lane_json_file_count"], 143)
        self.assertEqual(metadata["lane_jsonl_file_count"], 4)

        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["terminal_main_loop_decision"],
            "do_not_resume_epk_as_default_main_loop_task",
        )
        self.assertEqual(
            conclusion["policy_harness_lane"],
            "terminal_gamma_geometry_lead_sibling_control_stress_abstained_fail_closed",
        )

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            set(lanes),
            {
                "epk_positive_evidence",
                "epk_false_positive_hunter",
                "epk_sibling_controls",
                "epk_policy_harness",
            },
        )
        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "evidence_against_fresh_folded_protein_positive",
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["primary_outcome"],
            "counterexample_found",
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["primary_outcome"],
            "policy_frozen_review_only_and_terminal_gamma_sibling_stress_abstains",
        )
        self.assertFalse(
            synthesis["next_exact_experiment_if_epk_is_reopened"][
                "decision_to_start_now"
            ]
        )

    def test_late_epk_research_lane_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_late_research_lane_synthesis_20260520.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_remote_branch_outputs_integrated"])
        self.assertTrue(metadata["integrates_uncommitted_sibling_worktree_outputs"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_files_edited"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])
        self.assertEqual(metadata["input_json_validated_file_count"], 27)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validated_file_count"], 3)

        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["main_loop_decision"],
            "do_not_resume_epk_as_default_main_loop_task",
        )
        self.assertFalse(conclusion["decision_to_start_now"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            set(lanes),
            {
                "epk_positive_evidence",
                "epk_substrate_role_identity",
                "epk_false_positive_hunter",
                "epk_sibling_controls",
                "epk_policy_harness",
            },
        )
        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "evidence_for_review_only_peptide_positive_and_against_fresh_folded_positive",
        )
        self.assertEqual(
            lanes["epk_positive_evidence"]["scout_unique_rows_reviewed_sum"],
            300,
        )
        self.assertIn(
            "2CCI", lanes["epk_positive_evidence"]["local_metal_candidate_pdb_ids"]
        )
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["orientation_summary"][
                "hard_counterexample"
            ],
            "9UW4",
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["false_positive_summary"][
                "primary_outcome"
            ],
            "counterexample_found",
        )
        self.assertEqual(
            len(
                lanes["epk_false_positive_hunter"]["false_positive_summary"][
                    "topology_clear_non_epk_counterexample_pdb_ids"
                ]
            ),
            13,
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["sibling_control_summary"]["case_count"],
            91,
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["policy_harness_summary"][
                "expected_decision_mismatch_count"
            ],
            0,
        )

    def test_post_late_dirty_epk_lane_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_post_late_dirty_lane_synthesis_20260520.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["integrates_uncommitted_sibling_worktree_outputs"])
        self.assertEqual(metadata["input_json_validated_file_count"], 20)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validated_file_count"], 3)
        self.assertEqual(metadata["input_jsonl_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["counterexample_pdb_ids"],
            ["9I3I"],
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"][
                "current_rule_counterexample_residual_after_v4_count"
            ],
            0,
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"][
                "known_epk_positive_lost_to_v4_count"
            ],
            0,
        )
        self.assertEqual(lanes["epk_sibling_controls"]["case_count"], 91)
        self.assertEqual(
            lanes["epk_policy_harness"]["decision_counts"],
            {"review_only_abstain": 8},
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["expected_decision_mismatch_count"], 0
        )
        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertFalse(conclusion["decision_to_start_now"])

    def test_overnight_epk_lane_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_overnight_research_lane_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["integrates_uncommitted_sibling_worktree_outputs"])
        self.assertEqual(metadata["input_json_validated_file_count"], 11)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validated_file_count"], 4)
        self.assertEqual(metadata["input_jsonl_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "review_only_positive_style_evidence_but_no_clean_folded_protein_positive",
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["primary_outcome"],
            "bounded_v4_overblock_stress_diagnostic_only",
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["primary_outcome"],
            "expected_block_oracle_ready_review_only",
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["primary_outcome"],
            "adp_product_and_repair_tripwire_freezes_fail_closed_policy_context",
        )
        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertFalse(conclusion["decision_to_start_now"])
        self.assertFalse(
            synthesis["next_exact_experiment_if_epk_research_lane_continues"][
                "decision_to_start_now"
            ]
        )

    def test_post_overnight_remote_epk_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS
            / "v3_epk_post_overnight_remote_lane_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_remote_branch_outputs_integrated"])
        self.assertEqual(metadata["lane_count"], 3)
        self.assertEqual(metadata["input_json_validated_file_count"], 9)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validated_file_count"], 3)
        self.assertEqual(metadata["input_jsonl_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "evidence_against_clean_folded_protein_positive",
        )
        self.assertEqual(lanes["epk_positive_evidence"]["current_day_surface_returned_rows"], 0)
        self.assertIn("23FC", lanes["epk_positive_evidence"]["short_or_peptide_positive_style_rows"])
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["primary_outcome"],
            "blocker_not_cleared_biology_ambiguity",
        )
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["confusion_matrix"],
            {"false_negative": 6, "false_positive": 0, "true_negative": 34, "true_positive": 14},
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["decision_counts"],
            {"review_only_abstain": 10},
        )
        self.assertTrue(
            lanes["epk_policy_harness"]["already_reflected_by_overnight_dirty_synthesis"]
        )

        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["main_loop_decision"],
            "do_not_resume_epk_as_default_main_loop_task",
        )
        self.assertFalse(conclusion["decision_to_start_now"])
        self.assertFalse(
            synthesis["next_exact_experiment_if_epk_is_reopened"][
                "decision_to_start_now"
            ]
        )

    def test_prospective_external_minicampaign_records_blocker_without_import(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_prospective_external_minicampaign_decision_packet_20260520.json"
        )
        metadata = packet["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["candidate_count"], 12)
        self.assertEqual(
            metadata["normalized_terminal_decision_counts"]["terminal_rejection"], 1
            + 11
        )
        self.assertEqual(
            metadata["current_countable_structural_screen_status"],
            "completed_current_countable_structural_duplicate_signals",
        )
        self.assertTrue(metadata["foldseek_binary_available"])
        self.assertTrue(metadata["foldseek_pair_cache_complete"])
        self.assertEqual(metadata["coordinate_sidecar_missing_count"], 0)
        self.assertEqual(metadata["coordinate_materialized_or_reused_count"], 11)
        self.assertEqual(metadata["structurally_screened_candidate_count"], 11)
        self.assertEqual(
            metadata["current_countable_structural_screen_status_counts"],
            {"current_countable_structural_duplicate_signal": 11},
        )
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertEqual(metadata["abstain_threshold"], 0.4115)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in packet["rows"])
        )

    def test_modern_baseline_comparison_makes_no_superiority_claim(self) -> None:
        comparison = _load_json(ARTIFACTS / "v3_modern_baseline_comparison_20260520.json")
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertEqual(metadata["frozen_row_count"], 12)
        self.assertFalse(metadata["ready_for_label_import"])

        geometry = metrics["geometry_retrieval_triage"]
        self.assertEqual(geometry["row_count"], 12)
        self.assertEqual(geometry["non_abstention_count_at_0_4115"], 0)
        self.assertEqual(geometry["text_or_label_fields_used_for_score_count"], 0)
        self.assertEqual(geometry["top1_fingerprint_counts"]["metal_dependent_hydrolase"], 9)

        self.assertEqual(
            metrics["deterministic_kmer_nearest_neighbor"][
                "representation_near_duplicate_alert_count"
            ],
            1,
        )
        self.assertEqual(
            metrics["esm2_8m_representation"]["representation_near_duplicate_alert_count"],
            3,
        )
        self.assertTrue(
            metrics["foldseek_structural_sidecar"]["all_vs_all_pair_cache_complete"]
        )

    def test_minicampaign_coordinate_materialization_is_review_only(self) -> None:
        materialization = _load_json(
            ARTIFACTS
            / "v3_prospective_external_minicampaign_coordinate_materialization_20260520.json"
        )
        metadata = materialization["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["candidate_count"], 11)
        self.assertEqual(metadata["coordinate_materialized_or_reused_count"], 11)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["coordinate_status_counts"],
            {"coordinate_sidecar_materialized": 11},
        )
        self.assertTrue(
            all(row["coordinate_digest_sha256"] for row in materialization["rows"])
        )

    def test_methyltransferase_minicampaign_is_terminal_pre_scoring(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_methyltransferase_minicampaign_freeze_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_methyltransferase_minicampaign_decision_packet_20260520.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_methyltransferase_minicampaign_baseline_comparison_20260520.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_methyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(
            metadata["normalized_terminal_decision_counts"],
            {"terminal_rejection": 20},
        )
        self.assertEqual(metadata["scored_candidate_count"], 0)
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["terminal_decision"]
                == "terminal_rejection_uncovered_mechanism_lane"
                for row in decisions["rows"]
            )
        )

        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 20)
        self.assertEqual(
            baseline["metrics"]["ec_keyword_lane_router"][
                "methyltransferase_keyword_or_ec_hits"
            ],
            20,
        )
        self.assertEqual(
            baseline["metrics"]["current_geometry_retrieval_triage"]["scored_row_count"],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"]["computed_row_count"],
            20,
        )
        self.assertFalse(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "terminal_decision_changed_by_sequence_baseline"
            ]
        )
        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertFalse(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_glycosyltransferase_minicampaign_is_terminal_pre_scoring(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_glycosyltransferase_minicampaign_freeze_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_glycosyltransferase_minicampaign_decision_packet_20260520.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_glycosyltransferase_minicampaign_baseline_comparison_20260520.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_glycosyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(freeze["metadata"]["primary_ec_cap"], 2)
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(
            metadata["normalized_terminal_decision_counts"],
            {"terminal_rejection": 20},
        )
        self.assertEqual(metadata["scored_candidate_count"], 0)
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["terminal_decision"]
                == "terminal_rejection_uncovered_mechanism_lane"
                for row in decisions["rows"]
            )
        )

        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 20)
        self.assertEqual(
            baseline["metrics"]["ec_keyword_lane_router"]["glycosyltransferase_ec_hits"],
            20,
        )
        self.assertEqual(
            baseline["metrics"]["current_geometry_retrieval_triage"]["scored_row_count"],
            0,
        )
        self.assertEqual(
            baseline["metadata"]["sequence_baseline_diagnostic_artifact"],
            "artifacts/v3_glycosyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json",
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "computed_row_count"
            ],
            20,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "near_neighbor_alert_count"
            ],
            1,
        )
        self.assertFalse(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "terminal_decision_changed_by_sequence_baseline"
            ]
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 1)
        self.assertFalse(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_sulfotransferase_minicampaign_is_terminal_pre_scoring(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_sulfotransferase_minicampaign_freeze_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_sulfotransferase_minicampaign_decision_packet_20260520.json"
        )
        baseline = _load_json(
            ARTIFACTS / "v3_sulfotransferase_minicampaign_baseline_comparison_20260520.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_sulfotransferase_minicampaign_sequence_baseline_diagnostic_20260520.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 16)
        self.assertEqual(freeze["metadata"]["primary_ec_cap"], 2)
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 16)
        self.assertEqual(
            metadata["normalized_terminal_decision_counts"],
            {"terminal_rejection": 16},
        )
        self.assertEqual(metadata["scored_candidate_count"], 0)
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["terminal_decision"]
                == "terminal_rejection_uncovered_mechanism_lane"
                for row in decisions["rows"]
            )
        )

        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 16)
        self.assertEqual(
            baseline["metrics"]["ec_keyword_lane_router"]["sulfotransferase_ec_hits"],
            16,
        )
        self.assertEqual(
            baseline["metrics"]["current_geometry_retrieval_triage"][
                "scored_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "computed_row_count"
            ],
            16,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "near_neighbor_alert_count"
            ],
            1,
        )
        self.assertFalse(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "terminal_decision_changed_by_sequence_baseline"
            ]
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 16)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 1)
        self.assertFalse(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_plp_aminotransferase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_plp_aminotransferase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_plp_aminotransferase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(freeze["metadata"]["target_current_fingerprint_lane"], "plp_dependent_enzyme")
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(
            metadata["normalized_terminal_decision_counts"],
            {"needs_review": 18, "terminal_rejection": 2},
        )
        self.assertEqual(metadata["scored_candidate_count"], 0)
        self.assertEqual(metadata["production_fingerprint_scored_candidate_count"], 0)
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertEqual(metadata["target_current_fingerprint_lane"], "plp_dependent_enzyme")
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        terminal_rows = {
            row["accession"]
            for row in decisions["rows"]
            if row["normalized_terminal_decision"] == "terminal_rejection"
        }
        self.assertEqual(terminal_rows, {"P12995", "P19938"})
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in decisions["rows"])
        )

        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 20)
        self.assertEqual(
            baseline["metrics"]["ec_keyword_lane_router"][
                "target_current_fingerprint_lane"
            ],
            "plp_dependent_enzyme",
        )
        self.assertEqual(
            baseline["metrics"]["current_geometry_retrieval_triage"][
                "scored_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "computed_row_count"
            ],
            20,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "exact_current_reference_sequence_match_count"
            ],
            2,
        )
        self.assertFalse(
            baseline["metrics"]["deterministic_kmer_nearest_neighbor"][
                "superiority_claim_supported"
            ]
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 2)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 2
        )
        self.assertTrue(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_flavin_monooxygenase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_flavin_monooxygenase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_flavin_monooxygenase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_flavin_monooxygenase_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "flavin_monooxygenase",
        )
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 19, "terminal_rejection": 1},
        )
        self.assertEqual(metadata["target_current_fingerprint_lane"], "flavin_monooxygenase")
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        terminal_rows = {
            row["accession"]
            for row in decisions["rows"]
            if row["terminal_decision"] == "terminal_rejection"
        }
        self.assertEqual(terminal_rows, {"P15245"})
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in decisions["rows"])
        )

        self.assertTrue(baseline["metadata"]["review_only"])
        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["candidate_count"], 20)
        self.assertEqual(
            baseline["metrics"]["terminal_decision_counts"],
            {"needs_review": 19, "terminal_rejection": 1},
        )
        self.assertEqual(
            baseline["metrics"]["ec_keyword_baseline"][
                "routed_to_existing_current_fingerprint_lane_count"
            ],
            20,
        )
        self.assertFalse(
            baseline["metrics"]["ec_keyword_baseline"][
                "supports_mechanism_match_claim"
            ]
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_sequence_baseline"][
                "exact_current_reference_sequence_match_count"
            ],
            1,
        )
        self.assertFalse(
            baseline["metrics"]["geometry_retrieval_baseline"][
                "supports_superiority_claim"
            ]
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 2)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 1
        )
        self.assertTrue(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

        register_rows = {row["item_id"]: row for row in register["rows"]}
        self.assertTrue(register["metadata"]["review_only"])
        self.assertEqual(
            register_rows["flavin_monooxygenase_minicampaign"][
                "terminal_decision_counts"
            ],
            {"needs_review": 19, "terminal_rejection": 1},
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_heme_peroxidase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_heme_peroxidase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_heme_peroxidase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS / "v3_heme_peroxidase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 19)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "heme_peroxidase_oxidase",
        )
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 19)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 15, "terminal_rejection": 4},
        )
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in decisions["rows"])
        )

        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["candidate_count"], 19)
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_sequence_baseline"][
                "exact_current_reference_sequence_match_count"
            ],
            4,
        )
        self.assertFalse(
            baseline["metrics"]["geometry_retrieval_baseline"][
                "supports_superiority_claim"
            ]
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 19)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 4
        )
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 4)
        self.assertTrue(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_serine_hydrolase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_serine_hydrolase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_serine_hydrolase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 19)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )
        self.assertTrue(
            all(row["ser_his_acid_source_context_present"] for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 19)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 18, "terminal_rejection": 1},
        )
        self.assertEqual(metadata["target_current_fingerprint_lane"], "ser_his_acid_hydrolase")
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        terminal_rows = {
            row["accession"]
            for row in decisions["rows"]
            if row["terminal_decision"] == "terminal_rejection"
        }
        self.assertEqual(terminal_rows, {"P94388"})
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in decisions["rows"])
        )

        self.assertTrue(baseline["metadata"]["review_only"])
        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 19)
        self.assertEqual(
            baseline["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_review": 18, "terminal_rejection": 1},
        )
        self.assertEqual(
            baseline["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_nearest_neighbor"][
                "exact_current_reference_sequence_match_count"
            ],
            1,
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 19)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 1
        )
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 1)
        self.assertTrue(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_metal_phosphatase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_metal_phosphatase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_metal_phosphatase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 17)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )
        self.assertTrue(
            all(row["metal_dependent_phosphatase_source_context_present"] for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 17)
        self.assertEqual(metadata["terminal_decision_counts"], {"needs_review": 17})
        self.assertEqual(metadata["target_current_fingerprint_lane"], "metal_dependent_hydrolase")
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(row["terminal_decision"] == "needs_review" for row in decisions["rows"])
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in decisions["rows"])
        )

        self.assertTrue(baseline["metadata"]["review_only"])
        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 17)
        self.assertEqual(
            baseline["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_review": 17},
        )
        self.assertEqual(
            baseline["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_nearest_neighbor"][
                "near_neighbor_alert_count"
            ],
            0,
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 17)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 0
        )
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 0)
        self.assertFalse(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_metal_phosphatase_deep_packet_records_exact_geometry_blocker(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_metal_phosphatase_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_coordinate_materialization_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_current_countable_structural_screen_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_geometry_scores_20260521.json"
        )
        blocker = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_foldseek_runtime_blocker_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_terminal_decision_packet_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(
            selection["metadata"]["target_current_fingerprint_lane"],
            "metal_dependent_hydrolase",
        )
        self.assertTrue(
            all(
                row["score_status_at_selection"]
                == "not_scored_at_deep_packet_selection"
                for row in selection["rows"]
            )
        )
        self.assertTrue(
            all(row["sequence_baseline_signal"] == "no_sequence_neighbor_alert" for row in selection["rows"])
        )

        self.assertTrue(coordinates["metadata"]["review_only"])
        self.assertEqual(coordinates["metadata"]["candidate_count"], 7)
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertTrue(
            all(row["coordinate_digest_sha256"] for row in coordinates["rows"])
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertFalse(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["expected_query_target_pair_count"], 4704)
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {"current_countable_structural_screen_not_completed": 7},
        )
        self.assertFalse(screen["metadata"]["ready_for_label_import"])

        self.assertTrue(blocker["metadata"]["review_only"])
        self.assertEqual(blocker["metadata"]["candidate_count"], 7)
        self.assertEqual(blocker["metadata"]["attempted_pair_count"], 4704)
        self.assertIn(
            "completed current-countable structural duplicate/leakage screen",
            blocker["metadata"]["exact_missing_evidence"],
        )
        self.assertFalse(blocker["metadata"]["ready_for_label_import"])

        self.assertTrue(mapping["metadata"]["review_only"])
        self.assertEqual(mapping["metadata"]["candidate_count"], 7)
        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 7)
        self.assertTrue(
            all(
                row["geometry_mapping_status"] == "mapped_for_geometry_score"
                for row in mapping["rows"]
            )
        )

        self.assertTrue(scores["metadata"]["review_only_rule"])
        self.assertEqual(scores["metadata"]["candidate_count"], 7)
        self.assertEqual(
            scores["metadata"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 6, "ser_his_acid_hydrolase": 1},
        )
        self.assertEqual(
            scores["metadata"]["text_or_label_fields_used_for_score_count"], 0
        )
        self.assertFalse(scores["metadata"]["ready_for_label_import"])

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["candidate_count"], 7)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        allowed = set(packet["metadata"]["allowed_terminal_decisions"])
        self.assertLessEqual({row["terminal_decision"] for row in packet["rows"]}, allowed)
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal_or_import_ready"]
                == "completed_current_countable_structural_duplicate_screen_missing_after_bounded_exact_foldseek_attempt"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["nearest_current_reference_id"]
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                not row["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in packet["rows"])
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            7,
        )
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "text_or_label_fields_used_for_score_count"
            ],
            0,
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_sidecar"]["status"],
            "blocked_exact_foldseek_screen_incomplete",
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar"]["status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(
            benchmark["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_new_extractor_or_structure": 7},
        )

    def test_metal_phosphatase_chunked_duplicate_screen_terminally_rejects_rows(
        self,
    ) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_chunked_current_countable_structural_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertTrue(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["candidate_count"], 7)
        self.assertEqual(screen["metadata"]["current_countable_coordinate_count"], 672)
        self.assertEqual(screen["metadata"]["expected_query_target_pair_count"], 4704)
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 4704)
        self.assertEqual(screen["metadata"]["query_target_pair_coverage"], 1.0)
        self.assertEqual(screen["metadata"]["raw_name_mapping_unmapped_count"], 0)
        self.assertEqual(
            screen["metadata"]["foldseek_query_run_status_counts"], {"completed": 7}
        )
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {"current_countable_structural_duplicate_signal": 7},
        )
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 7)
        self.assertFalse(screen["metadata"]["ready_for_label_import"])
        self.assertFalse(screen["metadata"]["curated_label_registry_edited"])
        self.assertFalse(screen["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(screen["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(screen["metadata"]["removal_allowed_set_true"])
        self.assertTrue(all(row["pair_cache_complete"] for row in screen["rows"]))
        self.assertTrue(
            all(
                row["current_countable_structural_screen_status"]
                == "current_countable_structural_duplicate_signal"
                for row in screen["rows"]
            )
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in screen["rows"]
            )
        )
        self.assertTrue(
            all(
                row["nearest_current_countable_hit"]["max_pair_tm_score"] >= 0.7
                for row in screen["rows"]
            )
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertTrue(packet["metadata"]["pair_cache_complete"])
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        allowed = set(packet["metadata"]["allowed_terminal_decisions"])
        self.assertLessEqual({row["terminal_decision"] for row in packet["rows"]}, allowed)
        self.assertEqual(
            {row["terminal_decision"] for row in packet["rows"]},
            {"terminal_rejection_duplicate_or_leakage"},
        )
        self.assertTrue(
            all(row["exact_blocker_if_not_terminal"] is None for row in packet["rows"])
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                not row["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
                for row in packet["rows"]
            )
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(benchmark["metrics"]["frozen_row_count"], 7)
        self.assertTrue(
            benchmark["metrics"]["foldseek_current_countable_pair_cache_complete"]
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_high_tm_candidate_count"],
            7,
        )
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_post_metal_epk_research_lane_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_post_metal_research_lane_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_remote_branch_outputs_integrated"])
        self.assertTrue(metadata["integrates_uncommitted_sibling_worktree_outputs"])
        self.assertEqual(metadata["lane_count"], 5)
        self.assertEqual(metadata["input_json_validated_file_count"], 401)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validated_record_count"], 167)
        self.assertEqual(metadata["input_jsonl_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        self.assertEqual(
            conclusion["overall"],
            "fresh_epk_lane_deltas_reinforce_no_go_production_decision",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["main_loop_decision"],
            "return_to_external_decision_deepening_ladder",
        )
        self.assertFalse(conclusion["decision_to_start_now"])
        self.assertFalse(conclusion["label_import_authorized"])
        self.assertFalse(conclusion["production_scoring_authorized"])
        self.assertFalse(conclusion["registry_or_fingerprint_change_authorized"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            set(lanes),
            {
                "epk_positive_evidence",
                "epk_false_positive_hunter",
                "epk_sibling_controls",
                "epk_policy_harness",
                "epk_substrate_role_identity",
            },
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["counterexample_pdb_ids"],
            ["5UJ7"],
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["entry_level_guard_residual_count"],
            0,
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["primary_outcome"],
            "candidate_evidence_regression_rows_emitted_review_only",
        )
        self.assertEqual(lanes["epk_sibling_controls"]["fixture_case_count"], 91)
        self.assertEqual(lanes["epk_sibling_controls"]["regression_row_count"], 103)
        self.assertEqual(lanes["epk_sibling_controls"]["unsafe_nonabstention_count"], 0)
        self.assertEqual(
            lanes["epk_policy_harness"]["decision_counts"],
            {"review_only_abstain": 213},
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["expected_decision_mismatch_count"], 0
        )
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["blocker_counts"]["topology_ambiguity"],
            109,
        )

    def test_serine_hydrolase_deep_packet_records_duplicate_screen_blocker(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_serine_hydrolase_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_coordinate_materialization_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS / "v3_serine_hydrolase_deep_packet_geometry_scores_20260521.json"
        )
        probe = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_current_countable_structural_probe_20260521.json"
        )
        blocker = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_duplicate_screen_blocker_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_terminal_decision_packet_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_modern_baseline_benchmark_20260521.json"
        )

        selected_accessions = {row["accession"] for row in selection["rows"]}
        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(
            selection["metadata"]["excluded_exact_current_reference_duplicates"],
            ["P94388"],
        )
        self.assertEqual(
            selected_accessions,
            {"P54317", "Q9BV23", "P07098", "Q99685", "P04180", "P31614", "E9LVH9"},
        )
        self.assertTrue(
            all(
                row["score_status"] == "not_scored_at_deep_packet_selection"
                for row in selection["rows"]
            )
        )
        self.assertTrue(
            all(row["pdb_cross_reference_present"] for row in selection["rows"])
        )

        self.assertTrue(coordinates["metadata"]["review_only"])
        self.assertEqual(coordinates["metadata"]["candidate_count"], 7)
        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 6
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 1)
        coordinate_rows = {row["accession"]: row for row in coordinates["rows"]}
        self.assertEqual(
            coordinate_rows["P31614"]["coordinate_status"], "coordinate_fetch_failed"
        )
        self.assertTrue(
            all(
                row["coordinate_digest_sha256"]
                for row in coordinates["rows"]
                if row["accession"] != "P31614"
            )
        )

        self.assertTrue(mapping["metadata"]["review_only"])
        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 6)
        self.assertEqual(
            mapping["metadata"]["status_counts"],
            {"ok": 6, "structure_fetch_failed": 1},
        )
        mapped_rows = {row["accession"]: row for row in mapping["entries"]}
        self.assertEqual(mapped_rows["P31614"]["status"], "structure_fetch_failed")
        self.assertTrue(
            all(
                row["status"] == "ok" and row["resolved_residue_count"] == 3
                for accession, row in mapped_rows.items()
                if accession != "P31614"
            )
        )

        self.assertTrue(scores["metadata"]["review_only_rule"])
        self.assertEqual(scores["metadata"]["candidate_count"], 7)
        self.assertEqual(
            scores["metadata"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 1, "ser_his_acid_hydrolase": 6},
        )
        self.assertEqual(
            scores["metadata"]["text_or_label_fields_used_for_score_count"], 0
        )
        abstain_threshold = scores["metadata"]["abstain_threshold"]
        for row in scores["results"]:
            target_score = next(
                item["score"]
                for item in row["top_fingerprints"]
                if item["fingerprint_id"] == "ser_his_acid_hydrolase"
            )
            self.assertLess(target_score, abstain_threshold)
            self.assertTrue(
                all(
                    not item["text_or_label_fields_used_for_score"]
                    for item in row["top_fingerprints"]
                )
            )

        self.assertTrue(probe["metadata"]["review_only"])
        self.assertFalse(probe["metadata"]["pair_cache_complete"])
        self.assertFalse(probe["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(probe["metadata"]["screened_candidate_count"], 0)
        self.assertEqual(
            probe["metadata"]["targeted_duplicate_probe_status_counts"],
            {
                "not_run_full_current_countable_screen_required": 6,
                "structure_coordinate_materialization_failed_before_foldseek_probe": 1,
            },
        )
        self.assertTrue(
            all(not row["duplicate_clear_established"] for row in probe["rows"])
        )

        self.assertTrue(blocker["metadata"]["review_only"])
        self.assertEqual(blocker["metadata"]["blocked_candidate_count"], 7)
        self.assertIn(
            "completed current-countable structural duplicate/leakage screen",
            blocker["metadata"]["exact_missing_evidence"],
        )
        self.assertFalse(blocker["metadata"]["ready_for_label_import"])

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["candidate_count"], 7)
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertNotIn(
            "needs_review", {row["terminal_decision"] for row in packet["rows"]}
        )
        allowed = set(packet["metadata"]["allowed_terminal_decisions"])
        self.assertLessEqual({row["terminal_decision"] for row in packet["rows"]}, allowed)
        self.assertTrue(
            all(row["exact_blocker_if_not_terminal_import_ready"] for row in packet["rows"])
        )
        self.assertTrue(
            all(
                not row["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in packet["rows"])
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            7,
        )
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "text_or_label_fields_used_for_score_count"
            ],
            0,
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_sidecar"]["status"],
            "blocked_not_run_pair_cache_required",
        )
        self.assertFalse(
            benchmark["metrics"]["foldseek_current_countable_sidecar"][
                "pair_cache_complete"
            ]
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar"]["status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(
            benchmark["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_new_extractor_or_structure": 7},
        )

    def test_serine_hydrolase_chunked_duplicate_screen_records_timeout_blocker(
        self,
    ) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_chunked_current_countable_structural_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertEqual(screen["metadata"]["candidate_count"], 7)
        self.assertEqual(screen["metadata"]["screened_candidate_count"], 6)
        self.assertEqual(screen["metadata"]["coordinate_missing_candidate_count"], 1)
        self.assertFalse(screen["metadata"]["materialized_pair_cache_complete"])
        self.assertFalse(screen["metadata"]["all_selected_pair_cache_complete"])
        self.assertEqual(
            screen["metadata"]["foldseek_query_run_status_counts"],
            {"foldseek_run_timeout": 6, "not_run_coordinate_missing": 1},
        )
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {
                "current_countable_structural_screen_incomplete": 6,
                "structure_coordinate_materialization_failed_before_foldseek_probe": 1,
            },
        )
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 0)
        self.assertFalse(screen["metadata"]["ready_for_label_import"])
        self.assertFalse(screen["metadata"]["curated_label_registry_edited"])
        self.assertFalse(screen["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(screen["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(screen["metadata"]["removal_allowed_set_true"])

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 0)
        self.assertFalse(packet["metadata"]["materialized_pair_cache_complete"])
        self.assertFalse(packet["metadata"]["all_selected_pair_cache_complete"])
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(
            {row["terminal_decision"] for row in packet["rows"]},
            {"needs_new_extractor_or_structure"},
        )
        self.assertTrue(
            all(row["exact_blocker_if_not_terminal"] for row in packet["rows"])
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in packet["rows"]
            )
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertFalse(
            benchmark["metrics"][
                "foldseek_current_countable_materialized_pair_cache_complete"
            ]
        )
        self.assertEqual(benchmark["metrics"]["coordinate_missing_candidate_count"], 1)
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_flavin_dehydrogenase_deep_selection_is_frozen_before_scoring(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_coordinate_materialization_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_geometry_scores_20260521.json"
        )
        blocker = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_duplicate_screen_blocker_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_terminal_decision_packet_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_modern_baseline_benchmark_20260521.json"
        )
        metadata = selection["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["source_frozen_candidate_count"], 20)
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(
            metadata["target_current_fingerprint_lane"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertEqual(metadata["source_free_geometry_scored_count"], 0)
        self.assertEqual(metadata["structural_duplicate_screened_count"], 0)
        self.assertEqual(
            metadata["excluded_exact_current_reference_duplicates"],
            ["P15559", "P0AEZ1", "P38489", "P42593"],
        )
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"P30043", "Q9BRQ8", "Q9NX74", "P42898", "Q652L6", "P94424", "P0AGE6"},
        )
        self.assertTrue(
            all(
                row["selection_frozen_before_geometry_or_duplicate_scoring"]
                for row in selection["rows"]
            )
        )
        self.assertTrue(
            all(
                row["score_status"] == "not_scored_at_deep_packet_selection"
                for row in selection["rows"]
            )
        )
        self.assertTrue(
            all(
                row["sequence_baseline_signal"] == "no_sequence_neighbor_alert"
                for row in selection["rows"]
            )
        )
        self.assertTrue(
            all(
                row["flavin_source_context_present"]
                and row["dehydrogenase_reductase_source_context_present"]
                and row["pdb_cross_reference_present"]
                for row in selection["rows"]
            )
        )
        self.assertEqual(
            selection["next_exact_experiment"]["id"],
            "flavin_dehydrogenase_deep_packet_coordinate_mapping_and_duplicate_screen_v1",
        )

        self.assertTrue(coordinates["metadata"]["review_only"])
        self.assertEqual(coordinates["metadata"]["candidate_count"], 7)
        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(coordinates["metadata"]["source_free_geometry_scored_count"], 0)
        self.assertEqual(coordinates["metadata"]["structural_duplicate_screened_count"], 0)
        self.assertFalse(coordinates["metadata"]["ready_for_production_scoring"])
        self.assertFalse(coordinates["metadata"]["ready_for_label_import"])
        self.assertEqual(
            coordinates["metadata"]["coordinate_status_counts"],
            {"coordinate_sidecar_materialized": 7},
        )
        self.assertTrue(
            all(row["coordinate_digest_sha256"] for row in coordinates["rows"])
        )

        self.assertTrue(mapping["metadata"]["review_only"])
        self.assertEqual(mapping["metadata"]["candidate_count"], 7)
        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 7)
        self.assertEqual(mapping["metadata"]["status_counts"], {"ok": 7})
        self.assertEqual(mapping["metadata"]["source_free_geometry_scored_count"], 0)
        self.assertEqual(mapping["metadata"]["structural_duplicate_screened_count"], 0)
        self.assertFalse(mapping["metadata"]["ready_for_production_scoring"])
        self.assertFalse(mapping["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(entry["status"] == "ok" for entry in mapping["entries"])
        )
        self.assertTrue(
            all(entry["resolved_residue_count"] >= 1 for entry in mapping["entries"])
        )
        self.assertTrue(
            all(
                entry["source_context_not_counted_as_predictive_score"]
                for entry in mapping["entries"]
            )
        )

        self.assertTrue(scores["metadata"]["review_only"])
        self.assertEqual(scores["metadata"]["candidate_count"], 7)
        self.assertEqual(
            scores["metadata"]["top1_fingerprint_counts"],
            {"flavin_dehydrogenase_reductase": 6, "heme_peroxidase_oxidase": 1},
        )
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 4)
        self.assertEqual(
            scores["metadata"]["text_or_label_fields_used_for_score_count"], 0
        )
        self.assertEqual(scores["metadata"]["structural_duplicate_screened_count"], 0)
        self.assertFalse(scores["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(not row["text_or_label_fields_used_for_score"] for row in scores["results"])
        )

        self.assertTrue(blocker["metadata"]["review_only"])
        self.assertFalse(blocker["metadata"]["pair_cache_complete"])
        self.assertFalse(blocker["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(blocker["metadata"]["screened_candidate_count"], 0)
        self.assertEqual(blocker["metadata"]["blocked_candidate_count"], 7)
        self.assertFalse(blocker["metadata"]["ready_for_label_import"])

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["candidate_count"], 7)
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(packet["metadata"]["target_lane_at_or_above_floor_count"], 4)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertTrue(
            all(
                row["terminal_decision"] == "needs_new_extractor_or_structure"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                not row["duplicate_leakage_screen"]["duplicate_clear_established"]
                for row in packet["rows"]
            )
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "target_lane_score_at_or_above_0_4115_count"
            ],
            4,
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_sidecar"]["status"],
            "blocked_not_run_pair_cache_required",
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar"]["status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(
            benchmark["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_new_extractor_or_structure": 7},
        )

    def test_flavin_dehydrogenase_chunked_duplicate_screen_rejects_leakage(
        self,
    ) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_chunked_current_countable_structural_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertEqual(screen["metadata"]["candidate_count"], 7)
        self.assertEqual(screen["metadata"]["screened_candidate_count"], 7)
        self.assertTrue(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 4704)
        self.assertEqual(
            screen["metadata"]["foldseek_query_run_status_counts"],
            {"completed": 7},
        )
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {"current_countable_structural_duplicate_signal": 7},
        )
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 7)
        self.assertGreaterEqual(
            screen["metadata"]["max_external_vs_current_countable_tm_score"],
            0.9,
        )
        self.assertFalse(screen["metadata"]["ready_for_label_import"])
        self.assertFalse(screen["metadata"]["curated_label_registry_edited"])
        self.assertFalse(screen["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(screen["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(screen["metadata"]["removal_allowed_set_true"])
        self.assertTrue(
            all(row["pair_cache_complete"] for row in screen["rows"])
        )
        self.assertTrue(
            all(
                row["current_countable_high_tm_hit_count"] >= 1
                for row in screen["rows"]
            )
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(
            {row["terminal_decision"] for row in packet["rows"]},
            {"terminal_rejection_duplicate_or_leakage"},
        )
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal_import_ready"] is None
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                "current_countable_structural_duplicate_screen_incomplete"
                not in row["counterevidence"]
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                "current_countable_high_tm_duplicate_or_leakage_signal"
                in row["counterevidence"]
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in packet["rows"]
            )
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertTrue(
            benchmark["metrics"]["foldseek_current_countable_pair_cache_complete"]
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_high_tm_candidate_count"],
            7,
        )
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_heme_peroxidase_deep_packet_records_geometry_and_duplicate_blockers(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_heme_peroxidase_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_coordinate_materialization_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS / "v3_heme_peroxidase_deep_packet_geometry_scores_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_chunked_current_countable_structural_screen_20260521.json"
        )
        rescue = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_targeted_current_heme_rescue_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"Q939D2", "P04040", "I2DBY1", "Q02567", "Q9UR19", "P06181", "P13029"},
        )
        self.assertTrue(
            all(not row["exact_current_reference_duplicate"] for row in selection["rows"])
        )

        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertTrue(
            all(row["coordinate_digest_sha256"] for row in coordinates["rows"])
        )

        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 7)
        self.assertEqual(mapping["metadata"]["status_counts"], {"ok": 7})
        self.assertTrue(
            all(
                entry["source_context_not_counted_as_predictive_score"]
                for entry in mapping["entries"]
            )
        )

        self.assertEqual(
            scores["metadata"]["top1_fingerprint_counts"],
            {"heme_peroxidase_oxidase": 7},
        )
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 7)
        self.assertEqual(scores["metadata"]["text_or_label_fields_used_for_score_count"], 0)

        self.assertFalse(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["foldseek_result_available_candidate_count"], 3)
        self.assertEqual(
            screen["metadata"]["targeted_current_fingerprint_rescue_high_tm_candidate_count"],
            3,
        )
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 6)
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {
                "current_countable_structural_duplicate_signal": 6,
                "foldseek_query_timeout": 1,
            },
        )
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 2016)
        self.assertLessEqual(
            screen["metadata"]["max_external_vs_current_countable_tm_score"], 1.0
        )
        self.assertTrue(
            all(
                hit["max_pair_tm_score"] >= screen["metadata"]["tm_score_threshold"]
                for row in screen["rows"]
                for hit in row["top_current_countable_hits"]
            )
        )
        self.assertFalse(rescue["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(rescue["metadata"]["target_subset_count"], 20)
        self.assertEqual(rescue["metadata"]["high_tm_candidate_count"], 3)

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        duplicate_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
        ]
        self.assertEqual(len(duplicate_rows), 6)
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in duplicate_rows
            )
        )
        unresolved = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "needs_new_extractor_or_structure"
        ]
        self.assertEqual([row["accession"] for row in unresolved], ["I2DBY1"])
        self.assertEqual(
            unresolved[0]["exact_blocker_if_not_terminal_import_ready"],
            "complete_current_countable_structural_duplicate_leakage_screen",
        )
        self.assertFalse(
            unresolved[0]["duplicate_leakage_screen"]["duplicate_clear_established"]
        )
        self.assertEqual(
            unresolved[0]["duplicate_leakage_screen"][
                "current_countable_structural_screen_status"
            ],
            "foldseek_query_timeout",
        )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["geometry_retrieval_triage"][
                "target_lane_score_at_or_above_0_4115_count"
            ],
            7,
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_current_countable_high_tm_candidate_count"],
            6,
        )
        self.assertEqual(
            benchmark["metrics"]["targeted_current_fingerprint_rescue_high_tm_candidate_count"],
            3,
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_flavin_dehydrogenase_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_flavin_dehydrogenase_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_flavin_dehydrogenase_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )
        self.assertTrue(
            all(row["dehydrogenase_reductase_source_context_present"] for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 16, "terminal_rejection": 4},
        )
        self.assertEqual(
            metadata["target_current_fingerprint_lane"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        terminal_rows = {
            row["accession"]
            for row in decisions["rows"]
            if row["terminal_decision"] == "terminal_rejection"
        }
        self.assertEqual(terminal_rows, {"P15559", "P0AEZ1", "P38489", "P42593"})

        self.assertTrue(baseline["metadata"]["review_only"])
        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 20)
        self.assertEqual(
            baseline["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_review": 16, "terminal_rejection": 4},
        )
        self.assertEqual(
            baseline["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_nearest_neighbor"][
                "exact_current_reference_sequence_match_count"
            ],
            4,
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 4
        )
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 4)
        self.assertTrue(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_cobalamin_radical_minicampaign_blocker_is_review_only(self) -> None:
        blocker = _load_json(
            ARTIFACTS
            / "v3_prospective_external_cobalamin_radical_minicampaign_blocker_review_20260521.json"
        )
        metadata = blocker["metadata"]
        conclusion = blocker["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertFalse(metadata["campaign_opened"])
        self.assertEqual(
            metadata["blocker_status"],
            "blocked_insufficient_new_prior_pool_clean_rows",
        )
        self.assertEqual(metadata["target_current_fingerprint_lane"], "cobalamin_radical_rearrangement")
        self.assertEqual(metadata["minimum_campaign_size"], 10)
        self.assertEqual(
            metadata["eligible_new_candidate_count_after_prior_pool_exclusion_and_caps"],
            1,
        )
        self.assertLess(
            metadata["eligible_new_candidate_count_after_prior_pool_exclusion_and_caps"],
            metadata["minimum_campaign_size"],
        )
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(
            conclusion["terminal_decision"],
            "terminal_rejection_insufficient_new_source_surface_for_campaign",
        )
        self.assertFalse(conclusion["production_scoring_authorized"])
        self.assertFalse(conclusion["label_import_authorized"])

    def test_radical_sam_minicampaign_stays_review_only(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_radical_sam_minicampaign_freeze_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_prospective_external_radical_sam_minicampaign_decision_packet_20260521.json"
        )
        baseline = _load_json(
            ARTIFACTS / "v3_radical_sam_minicampaign_baseline_comparison_20260521.json"
        )
        sequence = _load_json(
            ARTIFACTS
            / "v3_radical_sam_minicampaign_sequence_baseline_diagnostic_20260521.json"
        )

        self.assertTrue(freeze["metadata"]["review_only"])
        self.assertTrue(
            freeze["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(freeze["metadata"]["candidate_count"], 20)
        self.assertEqual(
            freeze["metadata"]["target_current_fingerprint_lane"],
            "radical_sam_enzyme",
        )
        self.assertEqual(freeze["metadata"]["production_fingerprint_count"], 8)
        self.assertFalse(freeze["metadata"]["ready_for_label_import"])
        self.assertFalse(freeze["metadata"]["ready_for_production_scoring"])
        self.assertTrue(
            all(row["score_status"] == "not_scored_at_freeze" for row in freeze["rows"])
        )
        self.assertTrue(
            all(row["radical_sam_source_context_present"] for row in freeze["rows"])
        )
        self.assertTrue(
            all(row["fe_s_or_sam_source_context_present"] for row in freeze["rows"])
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_count"], 20)
        self.assertEqual(metadata["terminal_decision_counts"], {"needs_review": 20})
        self.assertEqual(
            metadata["target_current_fingerprint_lane"], "radical_sam_enzyme"
        )
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(row["terminal_decision"] == "needs_review" for row in decisions["rows"])
        )
        self.assertFalse(
            decisions["synthesis_conclusion"]["production_scoring_authorized"]
        )
        self.assertFalse(
            decisions["synthesis_conclusion"][
                "registry_or_fingerprint_change_authorized"
            ]
        )

        self.assertTrue(baseline["metadata"]["review_only"])
        self.assertFalse(baseline["metadata"]["superiority_claim_permitted"])
        self.assertEqual(baseline["metadata"]["frozen_row_count"], 20)
        self.assertEqual(
            baseline["metrics"]["review_only_terminal_decisions"][
                "terminal_decision_counts"
            ],
            {"needs_review": 20},
        )
        self.assertEqual(
            baseline["metrics"]["geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            0,
        )
        self.assertEqual(
            baseline["metrics"]["deterministic_5mer_nearest_neighbor"][
                "exact_current_reference_sequence_match_count"
            ],
            0,
        )

        self.assertTrue(sequence["metadata"]["review_only"])
        self.assertEqual(sequence["metadata"]["candidate_count"], 20)
        self.assertEqual(sequence["metadata"]["reference_sequence_count"], 737)
        self.assertEqual(
            sequence["metadata"]["exact_current_reference_sequence_match_count"], 0
        )
        self.assertEqual(sequence["metadata"]["near_neighbor_alert_count"], 0)
        self.assertFalse(
            sequence["metadata"]["terminal_decision_changed_by_sequence_baseline"]
        )
        self.assertFalse(sequence["metadata"]["ready_for_label_import"])

    def test_external_minicampaign_modern_baseline_rollup_stays_review_only(self) -> None:
        rollup = _load_json(
            ARTIFACTS / "v3_external_minicampaign_modern_baseline_rollup_20260521.json"
        )
        metadata = rollup["metadata"]
        metrics = rollup["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 2)
        self.assertEqual(metadata["frozen_row_count"], 40)
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(
            metrics["terminal_decision_counts"],
            {"needs_review": 37, "terminal_rejection": 3},
        )
        self.assertEqual(
            metrics["ec_keyword_baseline"][
                "campaign_rows_routed_to_existing_lane_count"
            ],
            40,
        )
        self.assertFalse(
            metrics["ec_keyword_baseline"]["supports_mechanism_match_claim"]
        )
        self.assertEqual(
            metrics["deterministic_sequence_baseline"][
                "exact_current_reference_sequence_match_count"
            ],
            3,
        )
        self.assertEqual(
            metrics["deterministic_sequence_baseline"]["near_neighbor_alert_count"],
            4,
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"]["scored_row_count"],
            0,
        )
        self.assertFalse(
            metrics["esm_foldseek_sidecar_sample"]["supports_superiority_claim"]
        )

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(
            campaigns["plp_aminotransferase"]["terminal_decision_counts"],
            {"needs_review": 18, "terminal_rejection": 2},
        )
        self.assertEqual(
            campaigns["flavin_monooxygenase"]["terminal_decision_counts"],
            {"needs_review": 19, "terminal_rejection": 1},
        )
        self.assertEqual(
            rollup["synthesis_conclusion"]["overall"],
            "modern_baseline_rollup_is_review_only_and_no_superiority_claim",
        )

    def test_external_minicampaign_modern_baseline_rollup_post_heme(self) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_modern_baseline_rollup_post_heme_20260521.json"
        )
        metadata = rollup["metadata"]
        metrics = rollup["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 3)
        self.assertEqual(metadata["frozen_row_count"], 59)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(
            metrics["terminal_decision_counts"],
            {"needs_review": 52, "terminal_rejection": 7},
        )
        self.assertEqual(
            metrics["deterministic_sequence_baseline"][
                "exact_current_reference_sequence_match_count"
            ],
            7,
        )
        self.assertEqual(
            metrics["deterministic_sequence_baseline"]["near_neighbor_alert_count"],
            8,
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"]["scored_row_count"],
            0,
        )
        self.assertFalse(
            metrics["esm_foldseek_sidecar_sample"]["supports_superiority_claim"]
        )

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(
            campaigns["heme_peroxidase"]["terminal_decision_counts"],
            {"needs_review": 15, "terminal_rejection": 4},
        )
        self.assertEqual(
            rollup["synthesis_conclusion"]["overall"],
            "modern_baseline_rollup_post_heme_is_review_only_and_no_superiority_claim",
        )

    def test_external_minicampaign_modern_baseline_rollup_post_serine_hydrolase(
        self,
    ) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_modern_baseline_rollup_post_serine_hydrolase_20260521.json"
        )
        metadata = rollup["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 4)
        self.assertEqual(metadata["frozen_row_count"], 78)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 70, "terminal_rejection": 8},
        )
        self.assertEqual(metadata["exact_current_reference_sequence_match_count"], 8)
        self.assertEqual(metadata["near_neighbor_alert_count"], 9)
        self.assertEqual(metadata["geometry_scored_external_row_count"], 0)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(
            set(campaigns),
            {
                "plp_aminotransferase",
                "flavin_monooxygenase",
                "heme_peroxidase",
                "serine_hydrolase",
            },
        )
        self.assertEqual(
            campaigns["serine_hydrolase"]["terminal_decision_counts"],
            {"needs_review": 18, "terminal_rejection": 1},
        )
        self.assertFalse(rollup["task_definition"]["positive_claim_allowed"])

    def test_external_minicampaign_modern_baseline_rollup_post_metal_phosphatase(
        self,
    ) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_modern_baseline_rollup_post_metal_phosphatase_20260521.json"
        )
        metadata = rollup["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 5)
        self.assertEqual(metadata["frozen_row_count"], 95)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 87, "terminal_rejection": 8},
        )
        self.assertEqual(metadata["exact_current_reference_sequence_match_count"], 8)
        self.assertEqual(metadata["near_neighbor_alert_count"], 9)
        self.assertEqual(metadata["geometry_scored_external_row_count"], 0)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(
            campaigns["metal_phosphatase"]["terminal_decision_counts"],
            {"needs_review": 17},
        )
        self.assertEqual(
            campaigns["metal_phosphatase"]["target_current_fingerprint_lane"],
            "metal_dependent_hydrolase",
        )
        self.assertFalse(rollup["task_definition"]["positive_claim_allowed"])

    def test_external_minicampaign_modern_baseline_rollup_post_flavin_dehydrogenase(
        self,
    ) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_modern_baseline_rollup_post_flavin_dehydrogenase_20260521.json"
        )
        metadata = rollup["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 6)
        self.assertEqual(metadata["frozen_row_count"], 115)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 103, "terminal_rejection": 12},
        )
        self.assertEqual(metadata["exact_current_reference_sequence_match_count"], 12)
        self.assertEqual(metadata["near_neighbor_alert_count"], 13)
        self.assertEqual(metadata["geometry_scored_external_row_count"], 0)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(
            campaigns["flavin_dehydrogenase"]["terminal_decision_counts"],
            {"needs_review": 16, "terminal_rejection": 4},
        )
        self.assertEqual(
            campaigns["flavin_dehydrogenase"]["target_current_fingerprint_lane"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertFalse(rollup["task_definition"]["positive_claim_allowed"])

    def test_external_minicampaign_modern_baseline_rollup_post_radical_sam(
        self,
    ) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_modern_baseline_rollup_post_radical_sam_20260521.json"
        )
        metadata = rollup["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["campaign_count"], 7)
        self.assertEqual(metadata["frozen_row_count"], 135)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 123, "terminal_rejection": 12},
        )
        self.assertEqual(metadata["exact_current_reference_sequence_match_count"], 12)
        self.assertEqual(metadata["near_neighbor_alert_count"], 13)
        self.assertEqual(metadata["geometry_scored_external_row_count"], 0)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        campaigns = {row["campaign_id"]: row for row in rollup["campaigns"]}
        self.assertEqual(len(campaigns), 7)
        self.assertEqual(
            campaigns["radical_sam"]["terminal_decision_counts"],
            {"needs_review": 20},
        )
        self.assertEqual(
            campaigns["radical_sam"]["target_current_fingerprint_lane"],
            "radical_sam_enzyme",
        )
        self.assertFalse(rollup["task_definition"]["positive_claim_allowed"])

    def test_current_fingerprint_external_minicampaign_benchmark_is_no_claim(
        self,
    ) -> None:
        benchmark = _load_json(
            ARTIFACTS
            / "v3_current_fingerprint_external_minicampaign_baseline_benchmark_20260521.json"
        )
        metadata = benchmark["metadata"]
        metrics = benchmark["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertEqual(metadata["campaign_fingerprint_lane_count"], 7)
        self.assertEqual(metadata["blocker_fingerprint_lane_count"], 1)
        self.assertEqual(metadata["frozen_row_count"], 135)
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            metrics["coverage"],
            {
                "fingerprint_lanes_with_external_minicampaign": 7,
                "fingerprint_lanes_with_terminal_source_surface_blocker": 1,
                "fingerprint_lanes_without_campaign_or_blocker": 0,
                "production_fingerprint_count": 8,
            },
        )
        self.assertEqual(
            metrics["review_only_terminal_decisions"]["terminal_decision_counts"],
            {"needs_review": 123, "terminal_rejection": 12},
        )
        self.assertEqual(
            metrics["review_only_terminal_decisions"][
                "terminal_decision_counts_including_cobalamin_blocker"
            ],
            {"needs_review": 123, "terminal_rejection": 13},
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"][
                "geometry_scored_external_row_count"
            ],
            0,
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["supports_mechanism_match_claim"]
        )
        self.assertFalse(
            metrics["deterministic_5mer_nearest_neighbor"][
                "supports_superiority_claim"
            ]
        )
        self.assertFalse(
            metrics["esm_foldseek_sidecar_sample"]["supports_superiority_claim"]
        )

        coverage_rows = {
            row["fingerprint_id"]: row for row in benchmark["coverage_rows"]
        }
        self.assertEqual(set(coverage_rows), set(metadata["production_fingerprint_universe"]))
        self.assertEqual(
            coverage_rows["cobalamin_radical_rearrangement"]["coverage_status"],
            "blocked_insufficient_new_prior_pool_clean_rows",
        )
        self.assertEqual(len(benchmark["frozen_rows"]), 135)
        self.assertFalse(benchmark["task_definition"]["positive_claim_allowed"])
        self.assertFalse(
            benchmark["synthesis_conclusion"]["production_scoring_authorized"]
        )
        self.assertFalse(benchmark["synthesis_conclusion"]["label_import_authorized"])

    def test_external_minicampaign_source_free_geometry_preregistration_is_frozen(
        self,
    ) -> None:
        preregistration = _load_json(
            ARTIFACTS
            / "v3_external_minicampaign_source_free_geometry_preregistration_20260521.json"
        )
        metadata = preregistration["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_next_experiment_scoring"])
        self.assertEqual(metadata["candidate_count"], 14)
        self.assertEqual(metadata["campaign_count"], 7)
        self.assertEqual(metadata["fingerprint_lane_count"], 7)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(
            set(metadata["candidate_count_per_campaign"].values()),
            {2},
        )

        rows = preregistration["rows"]
        self.assertEqual(len(rows), 14)
        self.assertTrue(
            all(row["prior_normalized_terminal_decision"] == "needs_review" for row in rows)
        )
        self.assertTrue(
            all(row["sequence_baseline_signal"] == "no_sequence_neighbor_alert" for row in rows)
        )
        self.assertTrue(
            all(row["source_free_geometry_status"] == "not_materialized" for row in rows)
        )
        self.assertTrue(
            all(
                row["foldseek_current_countable_screen_status"]
                == "not_run_preregistered_future_step"
                for row in rows
            )
        )
        self.assertTrue(all(not row["ready_for_label_import"] for row in rows))
        self.assertTrue(all(not row["countable_label_candidate"] for row in rows))
        self.assertFalse(preregistration["task_definition"]["positive_claim_allowed"])
        self.assertFalse(
            preregistration["synthesis_conclusion"][
                "production_scoring_authorized_now"
            ]
        )
        self.assertFalse(
            preregistration["synthesis_conclusion"]["label_import_authorized_now"]
        )

    def test_external_minicampaign_terminal_decision_index_is_review_only(
        self,
    ) -> None:
        index = _load_json(
            ARTIFACTS / "v3_external_minicampaign_terminal_decision_index_20260521.json"
        )
        metadata = index["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 136)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_review": 123, "terminal_rejection": 13},
        )
        self.assertEqual(metadata["campaign_count"], 7)
        self.assertTrue(metadata["includes_cobalamin_source_surface_blocker"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        allowed = set(index["task_definition"]["allowed_decisions"])
        self.assertLessEqual({row["terminal_decision"] for row in index["rows"]}, allowed)
        self.assertTrue(all(not row["ready_for_label_import"] for row in index["rows"]))
        self.assertTrue(all(not row["countable_label_candidate"] for row in index["rows"]))
        blocker_rows = [
            row for row in index["rows"] if row["campaign_id"] == "cobalamin_radical_blocker"
        ]
        self.assertEqual(len(blocker_rows), 1)
        self.assertEqual(
            blocker_rows[0]["target_current_fingerprint_lane"],
            "cobalamin_radical_rearrangement",
        )
        self.assertFalse(index["task_definition"]["positive_claim_allowed"])
        self.assertEqual(index["synthesis_conclusion"]["import_ready_candidate_count"], 0)
        self.assertFalse(index["synthesis_conclusion"]["label_import_authorized"])

    def test_current_external_small_wins_preserve_label_registry_invariants(
        self,
    ) -> None:
        labels = _load_json(ROOT / "data/registries/curated_mechanism_labels.json")
        by_type: dict[str, int] = {}
        for label in labels:
            by_type[label["label_type"]] = by_type.get(label["label_type"], 0) + 1

        self.assertEqual(len(labels), 682)
        self.assertEqual(by_type, {"out_of_scope": 470, "seed_fingerprint": 212})

        labels_by_entry = {label["entry_id"]: label for label in labels}
        self.assertEqual(
            {
                entry_id
                for entry_id in labels_by_entry
                if entry_id.startswith("uniprot:")
            },
            {"uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"},
        )
        for entry_id in ("uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"):
            label = labels_by_entry[entry_id]
            self.assertEqual(label["label_type"], "out_of_scope")
            self.assertIsNone(label["fingerprint_id"])
            self.assertEqual(
                label["ontology_version_at_decision"],
                "label_factory_v1_8fp",
            )

    def test_epk_dirty_sibling_followup_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_dirty_sibling_followup_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["dirty_sibling_worktrees_read"])
        self.assertFalse(metadata["production_scoring_authorized"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(set(synthesis["input_validation"]), {
            "epk_false_positive_hunter",
            "epk_policy_harness",
            "epk_positive_evidence",
            "epk_sibling_controls",
        })
        for validation in synthesis["input_validation"].values():
            self.assertEqual(validation["parse_error_count"], 0)
            self.assertGreater(validation["json_file_count"], 0)
            self.assertGreater(validation["jsonl_record_count"], 0)

        self.assertEqual(
            conclusion["overall"],
            "dirty_sibling_followups_reinforce_epk_no_go_production_decision",
        )
        self.assertFalse(conclusion["positive_universe_expansion_ready"])
        self.assertFalse(conclusion["substrate_role_axis_freeze_ready"])
        self.assertFalse(conclusion["production_scoring_authorized"])
        self.assertFalse(conclusion["label_import_authorized"])
        self.assertFalse(conclusion["registry_or_fingerprint_change_authorized"])
        self.assertEqual(
            conclusion["main_loop_action"],
            "do_not_resume_epk_as_main_loop_task; continue external mini-campaign geometry follow-up or non-ePK small wins",
        )

    def test_epk_fresh_lane_followup_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_fresh_lane_followup_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        decision = synthesis["synthesis_decision"]
        lanes = {row["lane"]: row for row in synthesis["lane_summaries"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_lane_output_since_post_metal_synthesis"])
        self.assertEqual(metadata["source_lane_count"], 5)
        self.assertEqual(
            metadata["main_loop_decision"], "do_not_resume_epk_as_main_loop_task"
        )
        self.assertFalse(metadata["production_claim_allowed"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["threshold_calibrated"])

        self.assertEqual(
            lanes["epk_positive_evidence"]["candidate_rows_reviewed"], 84
        )
        self.assertEqual(
            lanes["epk_positive_evidence"]["source_supported_review_only_rows"], 39
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"][
                "biological_assembly_split_counterexamples"
            ],
            ["5UJ7:biological_assembly_1"],
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"][
                "unsafe_nonabstention_after_expected_policy_count"
            ],
            0,
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["regression_rows_pinned"], 119
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["contract_assertions_passed"], 13
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["forbidden_source_leakage_count"], 0
        )
        self.assertEqual(
            decision["terminal_review_recommendation"],
            "continue_review_only_no_go_for_epk_production_activation",
        )
        self.assertIn("label import", decision["forbidden_in_main_loop"])

    def test_epk_remote_lane_followup_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_remote_lane_followup_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]
        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_remote_branch_outputs_integrated"])
        self.assertTrue(metadata["fresh_outputs_since_prior_synthesis"])
        self.assertEqual(metadata["input_lane_count"], 5)
        self.assertEqual(metadata["lanes_with_fresh_remote_push_count"], 4)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "search_surface_exhausted",
        )
        self.assertEqual(
            lanes["epk_positive_evidence"]["candidate_evidence_rows_emitted"], 0
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["unsafe_nonabstention_count"], 0
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["pinned_residual_counterexample"],
            "5UJ7:biological_assembly_1",
        )
        self.assertTrue(lanes["epk_policy_harness"]["scoreboard_gate_pass"])
        self.assertEqual(lanes["epk_policy_harness"]["forbidden_source_leakage_count"], 0)
        self.assertEqual(
            lanes["epk_substrate_role_identity"][
                "mixed_unblocked_none_blocker_signature_group_count"
            ],
            0,
        )
        self.assertIn("9UW4", lanes["epk_substrate_role_identity"]["decisive_collision"])

        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["main_loop_decision"],
            "return_to_non_epk_external_decision_deepening",
        )
        self.assertFalse(conclusion["decision_to_start_now"])

    def test_sdr_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(ARTIFACTS / "v3_sdr_family_readiness_packet_20260520.json")
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "O14756")
        self.assertEqual(
            readiness["positive_like_rows"][0]["normalized_decision_status_after_repair"],
            "needs_review",
        )
        self.assertEqual(
            readiness["sdr_ec_1_1_1_consistency_surface"][
                "sdr_false_non_abstention_count"
            ],
            0,
        )
        self.assertTrue(
            any(mode["id"] == "single_positive_like_row" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])

    def test_akr_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(ARTIFACTS / "v3_akr_family_readiness_packet_20260520.json")
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "C9JRZ8")
        self.assertEqual(
            readiness["positive_like_rows"][0]["normalized_decision_status_after_repair"],
            "needs_review",
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["nadp_binding_axis"][
                "direct_local_nadp_ligand_geometry_ready"
            ]
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["active_site_tyr_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertIn(
            "broader_duplicate_screening_required",
            readiness["import_and_duplicate_blockers"]["remaining_import_blockers"],
        )
        self.assertTrue(
            any(mode["id"] == "single_positive_like_row" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])

    def test_askha_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_askha_family_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["positive_like_boundary_row_count"], 4)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertGreaterEqual(
            packet["sibling_control_context"]["weak_rule_counterexample_count"],
            47,
        )

    def test_askha_control_tranche_preregistration_freezes_rows(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_askha_vs_atp_family_control_tranche_preregistration_20260520.json"
        )
        metadata = prereg["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(metadata["askha_boundary_row_count"], 4)
        self.assertEqual(metadata["current_hydrolase_control_count"], 4)
        self.assertEqual(metadata["atp_family_control_count"], 6)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        roles = {}
        row_ids = set()
        for row in prereg["rows"]:
            roles[row["row_role"]] = roles.get(row["row_role"], 0) + 1
            row_ids.add(row["row_id"])
            self.assertEqual(row["score_status"], "not_scored_in_this_preregistration")
            self.assertFalse(row["ready_for_label_import_at_freeze"])
        self.assertEqual(
            roles,
            {
                "askha_positive_like_boundary": 4,
                "current_production_hydrolase_control": 4,
                "atp_family_countercontrol": 6,
            },
        )
        self.assertEqual(
            {"m_csa:592", "m_csa:643", "m_csa:651", "m_csa:696"},
            {
                row["row_id"]
                for row in prereg["rows"]
                if row["row_role"] == "askha_positive_like_boundary"
            },
        )
        self.assertIn("m_csa:310", row_ids)
        self.assertIn("m_csa:637", row_ids)
        self.assertIn(
            "No new geometry",
            prereg["frozen_before_scoring_statement"],
        )

    def test_askha_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_askha_vs_atp_family_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]
        conclusion = decisions["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {
                "mechanism_match": 4,
                "needs_review": 3,
                "out_of_scope": 6,
                "terminal_rejection": 1,
            },
        )
        self.assertEqual(metadata["source_free_askha_axis_ready_count"], 0)
        self.assertEqual(metadata["askha_positive_like_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:592"]["terminal_decision"], "needs_review")
        self.assertEqual(rows["m_csa:651"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:310"]["terminal_decision"], "out_of_scope")
        self.assertEqual(rows["m_csa:15"]["terminal_decision"], "mechanism_match")
        self.assertTrue(all(row["selection_frozen_before_axis_scoring"] for row in rows.values()))
        self.assertTrue(
            all(
                not row["source_free_askha_axis"]["axis_ready_for_threshold_calibration"]
                for row in rows.values()
            )
        )
        self.assertEqual(
            conclusion["overall"],
            "askha_remains_review_only_and_not_production_ready",
        )

    def test_askha_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_askha_vs_atp_family_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {
                "mechanism_match": 4,
                "needs_review": 3,
                "out_of_scope": 6,
                "terminal_rejection": 1,
            },
        )
        self.assertEqual(
            metrics["review_only_axis_triage"]["source_free_askha_axis_ready_count"],
            0,
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 12, "ser_his_acid_hydrolase": 2},
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"][
                "askha_boundary_non_abstention_count_at_0_4115"
            ],
            2,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"][
                "false_positive_atp_family_countercontrol_keyword_hits"
            ],
            4,
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["detects_source_free_axis_gap"]
        )

    def test_atp_grasp_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_atp_grasp_family_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["positive_like_boundary_row_count"], 2)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        self.assertEqual(
            {row["entry_id"] for row in readiness["positive_like_boundary_rows"]},
            {"m_csa:310", "m_csa:498"},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertTrue(
            any(mode["id"] == "hydrolase_top1_collapse" for mode in packet["likely_failure_modes"])
        )

    def test_atp_grasp_control_tranche_preregistration_freezes_rows(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_atp_grasp_vs_neighbor_family_control_tranche_preregistration_20260520.json"
        )
        metadata = prereg["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 12)
        self.assertEqual(metadata["atp_grasp_boundary_row_count"], 2)
        self.assertEqual(metadata["current_hydrolase_control_count"], 4)
        self.assertEqual(metadata["askha_countercontrol_count"], 2)
        self.assertEqual(metadata["neighbor_atp_family_countercontrol_count"], 4)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        roles = {}
        for row in prereg["rows"]:
            roles[row["row_role"]] = roles.get(row["row_role"], 0) + 1
            self.assertEqual(row["score_status"], "not_scored_in_this_preregistration")
            self.assertFalse(row["ready_for_label_import_at_freeze"])
        self.assertEqual(
            roles,
            {
                "askha_countercontrol": 2,
                "atp_grasp_positive_like_boundary": 2,
                "current_production_hydrolase_control": 4,
                "phosphohistidine_or_nucleoside_kinase_countercontrol": 2,
                "small_molecule_kinase_countercontrol": 2,
            },
        )
        self.assertEqual(
            {row["row_id"] for row in prereg["rows"] if row["row_role"] == "atp_grasp_positive_like_boundary"},
            {"m_csa:310", "m_csa:498"},
        )
        self.assertIn("No new geometry", prereg["frozen_before_scoring_statement"])

    def test_atp_grasp_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_atp_grasp_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 12)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 4, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(metadata["source_free_atp_grasp_axis_ready_count"], 0)
        self.assertEqual(metadata["atp_grasp_positive_like_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:310"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:498"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:592"]["terminal_decision"], "out_of_scope")
        self.assertEqual(rows["m_csa:15"]["terminal_decision"], "mechanism_match")
        self.assertTrue(all(row["selection_frozen_before_axis_scoring"] for row in rows.values()))
        self.assertTrue(
            all(
                not row["source_free_atp_grasp_axis"][
                    "axis_ready_for_threshold_calibration"
                ]
                for row in rows.values()
            )
        )
        self.assertEqual(
            decisions["synthesis_conclusion"]["overall"],
            "atp_grasp_remains_review_only_and_not_production_ready",
        )

    def test_atp_grasp_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_atp_grasp_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 12)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {"mechanism_match": 4, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(
            metrics["review_only_axis_triage"][
                "source_free_atp_grasp_axis_ready_count"
            ],
            0,
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 10, "ser_his_acid_hydrolase": 2},
        )
        self.assertEqual(
            metrics["current_geometry_retrieval_triage"][
                "atp_grasp_boundary_non_abstention_count_at_0_4115"
            ],
            0,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"]["target_atp_grasp_rows_hit"],
            2,
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["detects_source_free_axis_gap"]
        )

    def test_ghkl_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_ghkl_family_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(readiness["positive_like_boundary_row_count"], 2)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        self.assertEqual(
            {row["entry_id"] for row in readiness["positive_like_boundary_rows"]},
            {"m_csa:327", "m_csa:603"},
        )
        self.assertTrue(
            all(
                row["local_metal_context"]
                for row in readiness["positive_like_boundary_rows"]
            )
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertTrue(
            any(mode["id"] == "generic_atp_mg_leakage" for mode in packet["likely_failure_modes"])
        )

    def test_ghkl_control_tranche_closes_review_only(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_ghkl_vs_neighbor_family_control_tranche_preregistration_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_ghkl_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_ghkl_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_ghkl_20260520.json"
        )

        self.assertTrue(prereg["metadata"]["review_only"])
        self.assertTrue(prereg["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(prereg["metadata"]["frozen_row_count"], 10)
        self.assertEqual(prereg["metadata"]["ghkl_boundary_row_count"], 2)
        self.assertEqual(prereg["metadata"]["current_hydrolase_control_count"], 2)
        self.assertEqual(prereg["metadata"]["atp_grasp_countercontrol_count"], 2)
        self.assertFalse(prereg["metadata"]["ready_for_production_scoring"])
        self.assertFalse(prereg["metadata"]["ready_for_label_import"])
        self.assertFalse(prereg["metadata"]["curated_label_registry_edited"])
        self.assertFalse(prereg["metadata"]["fingerprint_registry_edited"])
        self.assertIn("No new geometry", prereg["frozen_before_scoring_statement"])

        roles = {}
        for row in prereg["rows"]:
            roles[row["row_role"]] = roles.get(row["row_role"], 0) + 1
            self.assertEqual(row["score_status"], "not_scored_in_this_preregistration")
            self.assertFalse(row["ready_for_label_import_at_freeze"])
        self.assertEqual(
            roles,
            {
                "askha_countercontrol": 1,
                "atp_grasp_countercontrol": 2,
                "current_production_hydrolase_control": 2,
                "ghkl_positive_like_boundary": 2,
                "ghmp_countercontrol": 1,
                "ndk_countercontrol": 1,
                "pfkb_countercontrol": 1,
            },
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["frozen_row_count"], 10)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 2, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(metadata["source_free_ghkl_axis_ready_count"], 0)
        self.assertEqual(metadata["ghkl_positive_like_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:327"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:603"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:15"]["terminal_decision"], "mechanism_match")
        self.assertEqual(rows["m_csa:310"]["terminal_decision"], "out_of_scope")
        self.assertTrue(
            all(
                not row["source_free_ghkl_axis"]["axis_ready_for_threshold_calibration"]
                for row in rows.values()
            )
        )
        self.assertEqual(
            decisions["synthesis_conclusion"]["overall"],
            "ghkl_remains_review_only_and_not_production_ready",
        )

        self.assertTrue(comparison["metadata"]["review_only"])
        self.assertFalse(comparison["metadata"]["superiority_claim_permitted"])
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            comparison["metrics"]["review_only_terminal_axis_decisions"][
                "terminal_decision_counts"
            ],
            {"mechanism_match": 2, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(
            comparison["metrics"]["review_only_terminal_axis_decisions"][
                "source_free_ghkl_axis_ready_count"
            ],
            0,
        )

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 3)
        self.assertEqual(index["metadata"]["research_lane_only_count"], 1)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["ghkl"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "dnk")

    def test_dnk_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_dnk_family_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["positive_like_boundary_row_count"], 2)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        rows = {
            row["entry_id"]: row
            for row in readiness["positive_like_boundary_rows"]
        }
        self.assertEqual(set(rows), {"m_csa:588", "m_csa:615"})
        self.assertEqual(
            rows["m_csa:615"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
            3.232,
        )
        self.assertIn(
            "selected_structure_state_gap",
            {mode["id"] for mode in packet["likely_failure_modes"]},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertFalse(packet["safety_summary"]["registry_or_fingerprint_edit_performed"])

    def test_atp_family_readiness_index_post_dnk_packet_updates_queue(self) -> None:
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_dnk_packet_20260520.json"
        )
        metadata = index["metadata"]
        rows = {row["family_id"]: row for row in index["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["closed_review_only_no_go_count"], 3)
        self.assertEqual(metadata["packet_ready_not_frozen_count"], 1)
        self.assertEqual(metadata["packet_not_started_count"], 4)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(
            rows["dnk"]["production_readiness_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            rows["dnk"]["readiness_artifact"],
            "artifacts/v3_dnk_family_readiness_packet_20260520.json",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "dnk")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "dnk_packet_is_review_only_and_not_production_ready",
        )

    def test_dnk_control_tranche_closes_review_only(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_dnk_vs_neighbor_family_control_tranche_preregistration_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_dnk_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_dnk_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_dnk_tranche_20260520.json"
        )

        self.assertTrue(prereg["metadata"]["review_only"])
        self.assertTrue(prereg["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(prereg["metadata"]["frozen_row_count"], 10)
        self.assertEqual(prereg["metadata"]["dnk_boundary_row_count"], 2)
        self.assertEqual(prereg["metadata"]["current_hydrolase_control_count"], 2)
        self.assertEqual(prereg["metadata"]["ndk_countercontrol_count"], 1)
        self.assertFalse(prereg["metadata"]["ready_for_production_scoring"])
        self.assertFalse(prereg["metadata"]["ready_for_label_import"])
        self.assertFalse(prereg["metadata"]["curated_label_registry_edited"])
        self.assertFalse(prereg["metadata"]["fingerprint_registry_edited"])
        self.assertIn("No new geometry", prereg["frozen_before_scoring_statement"])

        roles = {}
        for row in prereg["rows"]:
            roles[row["row_role"]] = roles.get(row["row_role"], 0) + 1
            self.assertEqual(row["score_status"], "not_scored_in_this_preregistration")
            self.assertFalse(row["ready_for_label_import_at_freeze"])
        self.assertEqual(
            roles,
            {
                "askha_countercontrol": 1,
                "atp_grasp_countercontrol": 1,
                "current_production_hydrolase_control": 2,
                "dnk_positive_like_boundary": 2,
                "ghmp_countercontrol": 1,
                "ndk_countercontrol": 1,
                "pfka_countercontrol": 1,
                "pfkb_countercontrol": 1,
            },
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["frozen_row_count"], 10)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 2, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(metadata["source_free_dnk_axis_ready_count"], 0)
        self.assertEqual(metadata["dnk_positive_like_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:588"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:615"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["m_csa:15"]["terminal_decision"], "mechanism_match")
        self.assertEqual(rows["m_csa:637"]["terminal_decision"], "out_of_scope")
        self.assertTrue(
            all(
                not row["source_free_dnk_axis"]["axis_ready_for_threshold_calibration"]
                for row in rows.values()
            )
        )
        self.assertEqual(
            decisions["synthesis_conclusion"]["overall"],
            "dnk_remains_review_only_and_not_production_ready",
        )

        self.assertTrue(comparison["metadata"]["review_only"])
        self.assertFalse(comparison["metadata"]["superiority_claim_permitted"])
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            comparison["metrics"]["review_only_terminal_axis_decisions"][
                "terminal_decision_counts"
            ],
            {"mechanism_match": 2, "out_of_scope": 6, "terminal_rejection": 2},
        )
        self.assertEqual(
            comparison["metrics"]["review_only_terminal_axis_decisions"][
                "source_free_dnk_axis_ready_count"
            ],
            0,
        )

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 4)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["dnk"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "pfkb")

    def test_pfkb_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_pfkb_family_readiness_packet_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_pfkb_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["positive_like_boundary_row_count"], 2)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        rows = {
            row["entry_id"]: row
            for row in readiness["positive_like_boundary_rows"]
        }
        self.assertEqual(set(rows), {"m_csa:663", "m_csa:670"})
        self.assertEqual(rows["m_csa:663"]["structure_cofactor_families"], ["metal_ion"])
        self.assertEqual(rows["m_csa:670"]["top1_score"], 0.3474)
        self.assertIn(
            "pfka_askha_sugar_kinase_confusion",
            {mode["id"] for mode in packet["likely_failure_modes"]},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertFalse(packet["safety_summary"]["registry_or_fingerprint_edit_performed"])

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 4)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 1)
        self.assertEqual(index["metadata"]["packet_not_started_count"], 3)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["pfkb"]["production_readiness_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            index_rows["pfkb"]["readiness_artifact"],
            "artifacts/v3_pfkb_family_readiness_packet_20260520.json",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "pfkb")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "pfkb_packet_is_review_only_and_not_production_ready",
        )

    def test_pfkb_control_tranche_closes_review_only(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_pfkb_vs_neighbor_family_control_tranche_preregistration_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_pfkb_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_pfkb_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_pfkb_tranche_20260520.json"
        )

        self.assertTrue(prereg["metadata"]["review_only"])
        self.assertTrue(prereg["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(prereg["metadata"]["frozen_row_count"], 11)
        self.assertEqual(prereg["metadata"]["pfkb_boundary_row_count"], 2)
        self.assertFalse(prereg["metadata"]["ready_for_label_import"])

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["terminal_decision_counts"], {
            "needs_review": 2,
            "mechanism_match": 2,
            "out_of_scope": 7,
        })
        self.assertEqual(metadata["source_free_pfkb_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:663"]["terminal_decision"], "needs_review")
        self.assertEqual(rows["m_csa:670"]["terminal_decision"], "needs_review")
        self.assertTrue(
            rows["m_csa:663"]["source_free_pfkb_axis"][
                "local_nucleotide_plus_metal_context"
            ]
        )
        self.assertFalse(
            any(
                row["source_free_pfkb_axis"]["axis_ready_for_threshold_calibration"]
                for row in decisions["rows"]
            )
        )

        self.assertTrue(comparison["metadata"]["review_only"])
        self.assertFalse(comparison["metadata"]["superiority_claim_permitted"])
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            comparison["metrics"]["current_8_fingerprint_geometry_retrieval"][
                "top1_fingerprint_counts"
            ],
            {"metal_dependent_hydrolase": 11},
        )
        self.assertEqual(
            comparison["metrics"]["current_8_fingerprint_geometry_retrieval"][
                "non_abstention_count_at_0_4115"
            ],
            3,
        )

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 5)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 0)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["pfkb"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "ghmp")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "pfkb_tranche_is_review_only_and_not_production_ready",
        )

    def test_ghmp_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_ghmp_family_readiness_packet_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_ghmp_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["positive_like_boundary_row_count"], 1)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        rows = {
            row["entry_id"]: row
            for row in readiness["positive_like_boundary_rows"]
        }
        self.assertEqual(set(rows), {"m_csa:654"})
        self.assertEqual(rows["m_csa:654"]["top1_score"], 0.3581)
        self.assertIn(
            "single_boundary_row_fragility",
            {mode["id"] for mode in packet["likely_failure_modes"]},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertFalse(packet["safety_summary"]["registry_or_fingerprint_edit_performed"])

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 5)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 1)
        self.assertEqual(index["metadata"]["packet_not_started_count"], 2)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["ghmp"]["production_readiness_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            index_rows["ghmp"]["readiness_artifact"],
            "artifacts/v3_ghmp_family_readiness_packet_20260520.json",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "ghmp")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "ghmp_packet_is_review_only_and_not_production_ready",
        )

    def test_ghmp_control_tranche_closes_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_ghmp_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_ghmp_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_ghmp_tranche_20260520.json"
        )

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 10)
        self.assertEqual(metadata["terminal_decision_counts"], {
            "needs_review": 1,
            "mechanism_match": 2,
            "out_of_scope": 7,
        })
        self.assertEqual(metadata["source_free_ghmp_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:654"]["terminal_decision"], "needs_review")
        self.assertFalse(
            any(
                row["source_free_ghmp_axis"]["axis_ready_for_threshold_calibration"]
                for row in decisions["rows"]
            )
        )

        self.assertTrue(comparison["metadata"]["review_only"])
        self.assertFalse(comparison["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            comparison["metrics"]["current_8_fingerprint_geometry_retrieval"][
                "top1_fingerprint_counts"
            ],
            {"metal_dependent_hydrolase": 10},
        )
        self.assertEqual(
            comparison["metrics"]["current_8_fingerprint_geometry_retrieval"][
                "non_abstention_count_at_0_4115"
            ],
            3,
        )

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 6)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 0)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["ghmp"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "ndk")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "ghmp_tranche_is_review_only_and_not_production_ready",
        )

    def test_ndk_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_ndk_family_readiness_packet_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_ndk_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["boundary_row_count"], 1)
        self.assertEqual(readiness["positive_like_boundary_row_count"], 0)
        self.assertEqual(readiness["homolog_counteraxis_row_count"], 4)
        self.assertEqual(readiness["countable_positive_seed_count"], 0)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        rows = {row["entry_id"]: row for row in readiness["boundary_rows"]}
        self.assertEqual(set(rows), {"m_csa:637"})
        self.assertEqual(rows["m_csa:637"]["top1_score"], 0.4066)
        homologs = {
            row["pdb_id"]: row
            for row in readiness["homolog_counteraxis_rows"]
        }
        self.assertEqual(set(homologs), {"1WKL", "3Q86", "9OAN", "9PFY"})
        self.assertEqual(
            homologs["3Q86"]["nearest_gamma_to_mapped_histidine_distance_angstrom"],
            2.899,
        )
        self.assertIn(
            "histidine_vs_hydroxyl_axis_confusion",
            {mode["id"] for mode in packet["likely_failure_modes"]},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertFalse(packet["safety_summary"]["registry_or_fingerprint_edit_performed"])

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 6)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 1)
        self.assertEqual(index["metadata"]["packet_not_started_count"], 1)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["ndk"]["production_readiness_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            index_rows["ndk"]["readiness_artifact"],
            "artifacts/v3_ndk_family_readiness_packet_20260520.json",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "ndk")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "ndk_packet_is_review_only_and_not_production_ready",
        )

    def test_ndk_control_tranche_closes_review_only(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_ndk_vs_neighbor_family_control_tranche_preregistration_20260520.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_ndk_vs_neighbor_family_control_tranche_axis_decisions_20260520.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_ndk_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_ndk_tranche_20260520.json"
        )

        self.assertTrue(prereg["metadata"]["review_only"])
        self.assertTrue(prereg["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(prereg["metadata"]["frozen_row_count"], 14)
        self.assertEqual(prereg["metadata"]["ndk_homolog_countercontrol_count"], 4)
        self.assertFalse(prereg["metadata"]["ready_for_label_import"])

        metadata = decisions["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["terminal_decision_counts"], {
            "terminal_rejection": 1,
            "mechanism_match": 2,
            "out_of_scope": 11,
        })
        self.assertEqual(metadata["source_free_ndk_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:637"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["1WKL"]["terminal_decision"], "out_of_scope")
        self.assertTrue(
            rows["3Q86"]["source_free_ndk_axis"][
                "mapped_catalytic_histidine_context"
            ]
        )
        self.assertFalse(
            any(
                row["source_free_ndk_axis"]["axis_ready_for_threshold_calibration"]
                for row in decisions["rows"]
            )
        )

        self.assertTrue(comparison["metadata"]["review_only"])
        self.assertFalse(comparison["metadata"]["superiority_claim_permitted"])
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            comparison["metrics"]["review_only_terminal_axis_decisions"][
                "terminal_decision_counts"
            ],
            {"terminal_rejection": 1, "mechanism_match": 2, "out_of_scope": 11},
        )
        self.assertEqual(
            comparison["metrics"]["homolog_histidine_axis_counterdiagnostic"][
                "gamma_to_mapped_histidine_distance_min_angstrom"
            ],
            2.899,
        )

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 7)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 0)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["ndk"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "pfka")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "ndk_tranche_is_review_only_and_not_production_ready",
        )

    def test_pfka_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_pfka_family_readiness_packet_20260520.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_pfka_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(readiness["boundary_row_count"], 1)
        self.assertEqual(readiness["positive_like_boundary_row_count"], 0)
        self.assertEqual(readiness["measured_homolog_counteraxis_row_count"], 5)
        self.assertEqual(readiness["blocked_homolog_mapping_row_count"], 5)
        self.assertEqual(readiness["source_free_axis_ready_count"], 0)
        rows = {row["entry_id"]: row for row in readiness["boundary_rows"]}
        self.assertEqual(set(rows), {"m_csa:365"})
        self.assertEqual(rows["m_csa:365"]["top1_score"], 0.3999)
        homologs = {
            row["pdb_id"]: row
            for row in readiness["measured_homolog_counteraxis_rows"]
        }
        self.assertEqual(set(homologs), {"3F5M", "4XYJ", "5XZ8", "8W2H", "8W2J"})
        self.assertEqual(
            homologs["4XYJ"]["nearest_gamma_to_same_chain_hydroxyl_distance_angstrom"],
            3.221,
        )
        self.assertIn(
            "pfka_pfkb_sugar_kinase_confusion",
            {mode["id"] for mode in packet["likely_failure_modes"]},
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])
        self.assertFalse(packet["safety_summary"]["registry_or_fingerprint_edit_performed"])

        self.assertTrue(index["metadata"]["review_only"])
        self.assertEqual(index["metadata"]["closed_review_only_no_go_count"], 7)
        self.assertEqual(index["metadata"]["packet_ready_not_frozen_count"], 1)
        self.assertEqual(index["metadata"]["packet_not_started_count"], 0)
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            index_rows["pfka"]["production_readiness_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            index_rows["pfka"]["readiness_artifact"],
            "artifacts/v3_pfka_family_readiness_packet_20260520.json",
        )
        self.assertEqual(index["recommended_next_main_loop_items"][0]["family_id"], "pfka")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "pfka_packet_is_review_only_and_not_production_ready",
        )

    def test_pfka_control_tranche_closes_review_only(self) -> None:
        preregistration = _load_json(
            ARTIFACTS
            / "v3_pfka_vs_neighbor_family_control_tranche_preregistration_20260521.json"
        )
        decisions = _load_json(
            ARTIFACTS
            / "v3_pfka_vs_neighbor_family_control_tranche_axis_decisions_20260521.json"
        )
        comparison = _load_json(
            ARTIFACTS
            / "v3_pfka_vs_neighbor_family_control_tranche_baseline_comparison_20260521.json"
        )
        index = _load_json(
            ARTIFACTS / "v3_atp_family_readiness_index_post_pfka_tranche_20260521.json"
        )
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_pfka_tranche_20260521.json"
        )

        prereg_metadata = preregistration["metadata"]
        self.assertTrue(prereg_metadata["review_only"])
        self.assertTrue(
            prereg_metadata["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(prereg_metadata["frozen_row_count"], 15)
        self.assertEqual(prereg_metadata["pfka_homolog_countercontrol_count"], 5)
        self.assertFalse(prereg_metadata["ready_for_label_import"])

        decision_metadata = decisions["metadata"]
        self.assertTrue(decision_metadata["review_only"])
        self.assertEqual(
            decision_metadata["terminal_decision_counts"],
            {"mechanism_match": 2, "out_of_scope": 12, "terminal_rejection": 1},
        )
        self.assertEqual(decision_metadata["source_free_pfka_axis_ready_count"], 0)
        self.assertFalse(decision_metadata["ready_for_label_import"])
        self.assertFalse(decision_metadata["ready_for_production_scoring"])
        self.assertFalse(
            decision_metadata["ready_to_expand_positive_fingerprint_universe"]
        )
        self.assertFalse(decision_metadata["curated_label_registry_edited"])
        self.assertFalse(decision_metadata["fingerprint_registry_edited"])
        self.assertFalse(decision_metadata["mechanism_fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["m_csa:365"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["4XYJ"]["terminal_decision"], "out_of_scope")
        self.assertTrue(
            all(
                not row["source_free_pfka_axis"][
                    "axis_ready_for_threshold_calibration"
                ]
                for row in rows.values()
            )
        )

        comparison_metadata = comparison["metadata"]
        comparison_metrics = comparison["metrics"]
        self.assertTrue(comparison_metadata["review_only"])
        self.assertFalse(comparison_metadata["superiority_claim_permitted"])
        self.assertEqual(
            comparison_metrics["review_only_terminal_axis_decisions"][
                "terminal_decision_counts"
            ],
            {"mechanism_match": 2, "out_of_scope": 12, "terminal_rejection": 1},
        )
        self.assertEqual(
            comparison_metrics["current_8_fingerprint_geometry_retrieval"][
                "non_abstention_count_at_0_4115"
            ],
            3,
        )
        self.assertTrue(
            comparison_metrics["current_8_fingerprint_geometry_retrieval"][
                "all_m_csa_rows_top1_metal_hydrolase"
            ]
        )
        self.assertEqual(
            comparison_metrics["pfka_homolog_hydroxyl_axis_counterdiagnostic"][
                "gamma_to_same_chain_hydroxyl_distance_min_angstrom"
            ],
            3.221,
        )
        self.assertEqual(
            comparison_metrics["pfka_homolog_hydroxyl_axis_counterdiagnostic"][
                "gamma_to_same_chain_hydroxyl_distance_max_angstrom"
            ],
            6.152,
        )

        index_metadata = index["metadata"]
        index_rows = {row["family_id"]: row for row in index["rows"]}
        self.assertTrue(index_metadata["review_only"])
        self.assertEqual(index_metadata["closed_review_only_no_go_count"], 8)
        self.assertEqual(index_metadata["packet_ready_not_frozen_count"], 0)
        self.assertEqual(index_metadata["packet_not_started_count"], 0)
        self.assertEqual(
            index_rows["pfka"]["production_readiness_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "pfka_tranche_is_review_only_and_not_production_ready",
        )

        register_rows = {row["item_id"]: row for row in register["rows"]}
        self.assertTrue(register["metadata"]["review_only"])
        self.assertTrue(register["rollup"]["atp_family_non_epk_slots_closed_review_only"])
        self.assertEqual(
            register_rows["pfka_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            register_rows["pfka_control_tranche"]["terminal_decision_counts"],
            {"mechanism_match": 2, "out_of_scope": 12, "terminal_rejection": 1},
        )

    def test_main_loop_small_win_register_rolls_up_post_atp_readiness(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_atp_readiness_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["late_epk_research_lane_synthesis"]["decision_status"],
            "research_lane_only_no_go",
        )
        self.assertEqual(
            rows["glycosyltransferase_sequence_baseline_diagnostic"][
                "decision_status"
            ],
            "terminal_uncovered_lane_rejection_unchanged",
        )
        self.assertEqual(
            rows["ghkl_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            rows["dnk_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            rows["pfkb_readiness_packet"]["decision_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 4)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 1)
        self.assertFalse(register["rollup"]["registry_label_count_changed"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "pfkb_control_tranche",
        )

    def test_main_loop_register_rolls_up_post_pfkb_tranche(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_pfkb_tranche_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["post_late_dirty_epk_research_lane_synthesis"]["decision_status"],
            "research_lane_only_no_go",
        )
        self.assertEqual(
            rows["pfkb_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            rows["pfkb_control_tranche"]["terminal_decision_counts"],
            {"needs_review": 2, "mechanism_match": 2, "out_of_scope": 7},
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 5)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 0)
        self.assertFalse(register["rollup"]["registry_label_count_changed"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "prospective_external_minicampaign",
        )

    def test_main_loop_register_rolls_up_sulfotransferase_win(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_sulfotransferase_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["sulfotransferase_external_minicampaign"]["decision_status"],
            "terminal_review_only_rejections_preserved",
        )
        self.assertEqual(
            rows["sulfotransferase_external_minicampaign"][
                "terminal_decision_counts"
            ],
            {"terminal_rejection": 16},
        )
        self.assertTrue(register["rollup"]["external_minicampaign_terminal_rejection_preserved"])
        self.assertEqual(register["rollup"]["external_minicampaign_candidate_count"], 16)
        self.assertFalse(register["rollup"]["registry_label_count_changed"])
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_main_loop_register_rolls_up_ghmp_packet(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_ghmp_packet_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["ghmp_readiness_packet"]["decision_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            rows["ghmp_readiness_packet"]["primary_artifact"],
            "artifacts/v3_ghmp_family_readiness_packet_20260520.json",
        )
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 1)
        self.assertTrue(register["rollup"]["ghmp_packet_ready_not_frozen"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "ghmp_control_tranche",
        )
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_and_ghmp_packet_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_main_loop_register_rolls_up_ghmp_tranche(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_ghmp_tranche_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["ghmp_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            rows["ghmp_control_tranche"]["terminal_decision_counts"],
            {"needs_review": 1, "mechanism_match": 2, "out_of_scope": 7},
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 6)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 0)
        self.assertTrue(register["rollup"]["ghmp_control_tranche_closed"])
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_and_ghmp_tranche_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_main_loop_register_rolls_up_ndk_packet(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_ndk_packet_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["ndk_readiness_packet"]["decision_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            rows["ndk_readiness_packet"]["primary_artifact"],
            "artifacts/v3_ndk_family_readiness_packet_20260520.json",
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 6)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 1)
        self.assertTrue(register["rollup"]["ndk_packet_ready_not_frozen"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "ndk_control_tranche",
        )
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_and_ndk_packet_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_main_loop_register_rolls_up_ndk_tranche(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_ndk_tranche_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["ndk_control_tranche"]["decision_status"],
            "closed_review_only_no_go",
        )
        self.assertEqual(
            rows["ndk_control_tranche"]["terminal_decision_counts"],
            {"terminal_rejection": 1, "mechanism_match": 2, "out_of_scope": 11},
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 7)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 0)
        self.assertTrue(register["rollup"]["ndk_control_tranche_closed"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "pfka_readiness_packet",
        )
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_and_ndk_tranche_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_main_loop_register_rolls_up_pfka_packet(self) -> None:
        register = _load_json(
            ARTIFACTS
            / "v3_main_loop_small_win_register_post_pfka_packet_20260520.json"
        )
        metadata = register["metadata"]
        rows = {row["item_id"]: row for row in register["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            rows["pfka_readiness_packet"]["decision_status"],
            "readiness_packet_no_go",
        )
        self.assertEqual(
            rows["pfka_readiness_packet"]["primary_artifact"],
            "artifacts/v3_pfka_family_readiness_packet_20260520.json",
        )
        self.assertEqual(register["rollup"]["closed_review_only_no_go_family_count"], 7)
        self.assertEqual(register["rollup"]["packet_ready_not_frozen_family_count"], 1)
        self.assertEqual(register["rollup"]["packet_not_started_family_count"], 0)
        self.assertTrue(register["rollup"]["pfka_packet_ready_not_frozen"])
        self.assertEqual(
            register["recommended_next_main_loop_items"][0]["item_id"],
            "pfka_control_tranche",
        )
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_and_pfka_packet_closed_without_production_mutation",
        )
        self.assertFalse(register["synthesis_conclusion"]["superiority_claim_permitted"])

    def test_atp_family_readiness_index_keeps_queue_review_only(self) -> None:
        index = _load_json(ARTIFACTS / "v3_atp_family_readiness_index_20260520.json")
        metadata = index["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["family_count"], 9)
        self.assertEqual(metadata["closed_review_only_no_go_count"], 2)
        self.assertEqual(metadata["research_lane_only_count"], 1)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(rows["askha"]["production_readiness_status"], "closed_review_only_no_go")
        self.assertEqual(rows["atp_grasp"]["production_readiness_status"], "closed_review_only_no_go")
        self.assertEqual(rows["ghkl"]["production_readiness_status"], "readiness_packet_no_go")
        self.assertEqual(rows["epk"]["production_readiness_status"], "research_lane_only_no_go")
        self.assertEqual(index["recommended_main_loop_queue"][0]["family_id"], "ghkl")
        self.assertEqual(
            index["synthesis_conclusion"]["overall"],
            "atp_family_readiness_index_supports_more_review_only_small_wins_but_no_production_promotion",
        )

    def test_main_loop_small_win_decision_register_is_review_only(self) -> None:
        register = _load_json(
            ARTIFACTS / "v3_main_loop_small_win_decision_register_20260520.json"
        )
        metadata = register["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["decision_count"], 7)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["decision_id"]: row for row in register["rows"]}
        self.assertEqual(
            set(rows),
            {
                "epk_research_lane_synthesis_refresh",
                "epk_policy_harness_late_dirty_receipt",
                "epk_fresh_research_lane_push_synthesis",
                "methyltransferase_external_minicampaign",
                "methyltransferase_baseline_comparison",
                "askha_family_readiness",
                "askha_control_tranche_preregistration",
            },
        )
        self.assertEqual(
            rows["methyltransferase_external_minicampaign"]["decision_status"],
            "terminal_review_only_rejections_preserved",
        )
        self.assertEqual(
            rows["askha_control_tranche_preregistration"]["decision_status"],
            "frozen_before_scoring",
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in register["rows"])
        )
        self.assertEqual(
            register["synthesis_conclusion"]["overall"],
            "visible_small_wins_closed_without_production_mutation",
        )
        self.assertFalse(
            register["synthesis_conclusion"]["superiority_claim_permitted"]
        )

    def test_epk_policy_harness_late_dirty_receipt_is_non_decisional(self) -> None:
        receipt = _load_json(
            ARTIFACTS / "v3_epk_policy_harness_late_dirty_output_receipt_20260520.json"
        )
        metadata = receipt["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["source_outputs_committed_or_pushed"])
        self.assertFalse(metadata["decision_change_from_latest_main_synthesis"])
        self.assertEqual(metadata["late_dirty_json_file_count"], 15)
        self.assertEqual(metadata["json_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(len(receipt["late_dirty_files"]), 15)
        self.assertTrue(all(row["json_valid"] for row in receipt["late_dirty_files"]))
        findings = {row["finding_id"]: row for row in receipt["findings"]}
        self.assertEqual(
            findings["cross_ligand_sibling_control_contract_stress"][
                "decision_counts"
            ],
            {"review_only_abstain": 8},
        )
        self.assertEqual(
            receipt["synthesis_conclusion"]["main_loop_decision"],
            "no_decision_change_do_not_resume_epk_as_default_task",
        )
        self.assertEqual(
            receipt["synthesis_conclusion"]["production_activation_decision"],
            "no_go",
        )

    def test_epk_counterexample_push_synthesis_stays_review_only(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_counterexample_push_synthesis_20260520.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["json_validated_file_count"], 8)
        self.assertEqual(metadata["json_validation_error_count"], 0)
        self.assertEqual(metadata["fresh_remote_commits_since_prior_fresh_synthesis"], 2)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertTrue(
            all(row["json_valid"] for row in synthesis["input_validation"])
        )
        self.assertEqual(
            synthesis["lane_findings"][0]["primary_outcome"],
            "counterexample_found",
        )
        self.assertEqual(
            synthesis["counterexample_summary"]["fresh_counterexample"],
            "7ZDT",
        )
        self.assertEqual(
            synthesis["positive_anchor_summary"][
                "fresh_clean_folded_protein_positive_count"
            ],
            0,
        )
        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")

    def test_epk_fresh_research_lane_push_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_fresh_research_lane_push_synthesis_20260520.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["fresh_remote_commits_since_latest_main_synthesis"], 4)
        self.assertEqual(metadata["json_validation_error_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["primary_outcome"],
            "counterexample_found",
        )
        self.assertEqual(
            synthesis["substrate_role_identity_probe_summary"][
                "folded_tyr_rescue_counterexample"
            ],
            "9UW4",
        )
        self.assertEqual(
            conclusion["overall"],
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["next_exact_research_lane_experiment"],
            "epk_local_burial_solvent_exposure_probe_v1_review_only",
        )

    def test_glycoside_hydrolase_family_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_glycoside_hydrolase_family_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "Q6NSJ0")
        self.assertEqual(
            readiness["positive_like_rows"][0]["family_axis_status"],
            "review_only_glycoside_hydrolase_boundary_ready",
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["acidic_dyad_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(
            readiness["cofactor_and_active_site_evidence"]["metal_or_cofactor_context"][
                "metal_ligand_context_absent"
            ]
        )
        self.assertTrue(
            readiness["import_and_duplicate_blockers"][
                "control_not_integrated_into_import_safety_adjudication"
            ]
        )
        self.assertTrue(
            any(mode["id"] == "metal_hydrolase_collapse_risk" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])

    def test_sugar_phosphate_isomerase_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_sugar_phosphate_isomerase_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "P34949")
        self.assertEqual(
            readiness["positive_like_rows"][0]["family_axis_status"],
            "review_only_sugar_phosphate_isomerase_scope_ready",
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["basic_active_site_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(
            readiness["cofactor_and_active_site_evidence"]["flavin_or_cofactor_context"][
                "flavin_ligand_context_absent"
            ]
        )
        self.assertEqual(
            readiness["import_and_duplicate_blockers"]["heuristic_top1_fingerprint_id"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertTrue(
            any(mode["id"] == "weak_flavin_top1_scope_risk" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])

    def test_mechanism_family_readiness_index_prioritizes_review_only_next_step(self) -> None:
        index = _load_json(
            ARTIFACTS / "v3_mechanism_family_readiness_index_20260520.json"
        )
        metadata = index["metadata"]
        conclusion = index["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["family_packet_count"], 4)

        self.assertEqual(
            conclusion["overall"],
            "all_family_packets_review_only_not_freeze_ready",
        )
        self.assertTrue(conclusion["do_not_promote_any_family_now"])
        self.assertEqual(
            conclusion["recommended_next_family_experiment"],
            "glycoside_hydrolase_vs_metal_hydrolase_control_tranche_v1_review_only",
        )

        rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            set(rows),
            {
                "sdr_nad_p_redox",
                "akr_nadp_redox",
                "glycoside_hydrolase",
                "sugar_phosphate_isomerase",
            },
        )
        self.assertEqual(rows["glycoside_hydrolase"]["priority_rank"], 1)
        self.assertTrue(
            all(row["selection_freeze_required_before_scoring"] for row in rows.values())
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )

    def test_glycoside_hydrolase_control_tranche_preregistration_freezes_rows(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_glycoside_hydrolase_control_tranche_preregistration_20260520.json"
        )
        metadata = prereg["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertEqual(metadata["external_candidate_count"], 5)
        self.assertEqual(metadata["current_control_count"], 10)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        roles = {}
        for row in prereg["rows"]:
            roles[row["row_role"]] = roles.get(row["row_role"], 0) + 1
            self.assertEqual(row["score_status"], "not_scored_in_this_preregistration")
        self.assertEqual(
            roles,
            {
                "external_glycan_or_glycoside_candidate": 5,
                "current_production_hydrolase_control": 10,
            },
        )
        self.assertIn("Q6NSJ0", {row.get("accession") for row in prereg["rows"]})
        self.assertIn(
            "No new geometry",
            prereg["frozen_before_scoring_statement"],
        )

    def test_glycoside_hydrolase_control_tranche_decisions_stay_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_glycoside_hydrolase_control_tranche_axis_decisions_20260520.json"
        )
        metadata = packet["metadata"]
        conclusion = packet["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertEqual(metadata["external_candidate_count"], 5)
        self.assertEqual(metadata["current_control_count"], 10)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {
                "ambiguous": 2,
                "mechanism_match": 10,
                "needs_review": 1,
                "terminal_rejection": 2,
            },
        )
        self.assertEqual(metadata["external_sequence_no_signal_count"], 5)
        self.assertEqual(metadata["external_all_vs_all_structural_no_signal_count"], 5)
        self.assertEqual(metadata["current_countable_structural_duplicate_signal_count"], 1)
        self.assertEqual(metadata["source_free_glycoside_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(rows["uniprot:Q6NSJ0"]["terminal_decision"], "needs_review")
        self.assertEqual(rows["uniprot:P33025"]["terminal_decision"], "terminal_rejection")
        self.assertEqual(rows["uniprot:O60568"]["terminal_decision"], "terminal_rejection")
        self.assertTrue(
            all(
                row["terminal_decision"] == "mechanism_match"
                for row in rows.values()
                if row["row_id"].startswith("m_csa:")
            )
        )
        self.assertEqual(
            conclusion["production_fingerprint_decision"],
            "do_not_promote_glycoside_hydrolase_fingerprint",
        )
        self.assertEqual(conclusion["label_import_decision"], "no_import_ready_rows")
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])

    def test_glycoside_hydrolase_tranche_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_glycoside_hydrolase_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertEqual(metadata["external_row_count"], 5)
        self.assertEqual(metadata["current_control_row_count"], 10)

        self.assertEqual(
            metrics["terminal_axis_packet"],
            {
                "ambiguous": 2,
                "mechanism_match": 10,
                "needs_review": 1,
                "terminal_rejection": 2,
            },
        )
        self.assertFalse(metrics["ec_keyword_baseline"]["predictive_use_allowed"])
        self.assertEqual(
            metrics["deterministic_kmer5_nearest_neighbor"]["near_neighbor_alert_count"],
            0,
        )
        self.assertEqual(
            metrics["foldseek_external_all30_sidecar"][
                "no_external_structural_neighbor_above_threshold_count"
            ],
            5,
        )
        self.assertEqual(metrics["esm2_sidecars"]["esm2_8m_available_row_count"], 2)
        self.assertTrue(
            any("does not replace current-countable" in caveat for caveat in comparison["caveats"])
        )

    def test_minicampaign_sequence_baseline_diagnostic_is_non_import_evidence(self) -> None:
        diagnostic = _load_json(
            ARTIFACTS
            / "v3_prospective_external_minicampaign_sequence_baseline_diagnostic_20260520.json"
        )
        metadata = diagnostic["metadata"]
        metrics = diagnostic["metrics"]["deterministic_kmer5_nearest_neighbor"]
        by_accession = {row["accession"]: row for row in diagnostic["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["candidate_count"], 12)
        self.assertEqual(
            metadata["normalized_diagnostic_decision_counts"]["terminal_rejection"],
            12,
        )
        self.assertEqual(
            metadata["current_countable_structural_screen_status"],
            "completed_current_countable_structural_duplicate_signals",
        )
        self.assertTrue(metadata["foldseek_binary_available"])
        self.assertTrue(metadata["foldseek_pair_cache_complete"])
        self.assertEqual(metadata["coordinate_sidecar_missing_count"], 0)
        self.assertEqual(metadata["coordinate_materialized_or_reused_count"], 11)
        self.assertEqual(metadata["structural_duplicate_signal_count"], 11)

        self.assertEqual(metrics["exact_reference_holdout_count"], 1)
        self.assertEqual(metrics["borderline_sequence_neighbor_count"], 1)
        self.assertEqual(metrics["no_near_neighbor_signal_count"], 10)
        self.assertEqual(
            diagnostic["metrics"]["current_countable_foldseek_structural_screen"][
                "structural_duplicate_signal_count"
            ],
            11,
        )
        self.assertEqual(
            by_accession["P31040"]["deterministic_kmer5_status"],
            "kmer_borderline_sequence_neighbor",
        )
        self.assertEqual(
            by_accession["P31040"]["terminal_decision_from_existing_packet"],
            "rejected_current_countable_structural_duplicate_signal",
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in diagnostic["rows"])
        )

    def test_source_gap_minicampaign_freeze_is_pre_scoring(self) -> None:
        freeze = _load_json(
            ARTIFACTS
            / "v3_prospective_external_source_gap_minicampaign_freeze_20260520.json"
        )
        metadata = freeze["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["candidate_count"], 18)
        self.assertEqual(
            metadata["selection_bucket_counts"],
            {
                "active_site_source_missing": 6,
                "source_specificity_or_sampling_gap": 6,
                "uncovered_mechanism_lane": 6,
            },
        )
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        prior_accessions = set(metadata["prior_minicampaign_excluded_accessions"])
        imported_accessions = set(metadata["imported_external_hard_negative_excluded_accessions"])
        rows = freeze["rows"]
        self.assertEqual(len(rows), 18)
        self.assertTrue(all(row["score_status"] == "not_scored_in_this_freeze" for row in rows))
        self.assertTrue(all(row["accession"] not in prior_accessions for row in rows))
        self.assertTrue(all(row["accession"] not in imported_accessions for row in rows))
        self.assertIn("No geometry", freeze["frozen_before_scoring_statement"])

    def test_source_gap_minicampaign_decisions_are_terminal_rejections(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_prospective_external_source_gap_minicampaign_decision_packet_20260520.json"
        )
        metadata = packet["metadata"]
        conclusion = packet["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["candidate_count"], 18)
        self.assertEqual(metadata["terminal_decision_counts"], {"terminal_rejection": 18})
        self.assertEqual(
            metadata["terminal_decision_reason_counts"],
            {
                "terminal_rejection_missing_active_site_source_evidence": 6,
                "terminal_rejection_source_specificity_or_sampling_blocker": 6,
                "terminal_rejection_uncovered_mechanism_lane": 6,
            },
        )
        self.assertEqual(metadata["inverse_gate_scored_candidate_count"], 0)
        self.assertEqual(metadata["sequence_screened_candidate_count"], 0)
        self.assertEqual(metadata["foldseek_screened_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(
            metadata["separates_predictive_import_evidence_from_review_only_context"]
        )

        self.assertEqual(conclusion["label_import_decision"], "no_import_ready_rows")
        self.assertTrue(
            all(row["terminal_decision"] == "terminal_rejection" for row in packet["rows"])
        )
        self.assertTrue(
            all(
                row["production_fingerprint_scoring_status"]
                == "not_run_pre_scoring_source_gap_terminal_rejection"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all("protein_name" in row["excluded_context_from_positive_scoring"] for row in packet["rows"])
        )

    def test_source_gap_minicampaign_baseline_diagnostic_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS / "v3_source_gap_minicampaign_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 18)
        self.assertEqual(comparison["task_definition"]["task_id"], "pre_scoring_external_source_gap_triage_v1")
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])

        self.assertEqual(
            metrics["terminal_source_gap_triage"]["terminal_decision_counts"],
            {"terminal_rejection": 18},
        )
        self.assertEqual(
            metrics["source_completeness_gate"]["terminal_blocker_detection_count"],
            18,
        )
        self.assertFalse(metrics["ec_keyword_lane_proxy"]["detects_source_gap_blockers"])
        self.assertEqual(metrics["geometry_retrieval_triage"]["scored_row_count"], 0)
        self.assertEqual(metrics["deterministic_kmer_nearest_neighbor"]["evaluated_row_count"], 0)
        self.assertEqual(metrics["esm2_sidecars"]["available_row_count"], 0)
        self.assertEqual(metrics["foldseek_sidecars"]["available_row_count"], 0)

    def test_schiff_base_lyase_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_schiff_base_lyase_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "Q9BXD5")
        self.assertEqual(
            readiness["positive_like_rows"][0]["family_axis_status"],
            "review_only_schiff_base_lyase_scope_ready",
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["schiff_base_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(
            readiness["cofactor_and_active_site_evidence"]["heme_or_cofactor_context"][
                "heme_ligand_context_absent"
            ]
        )
        self.assertEqual(
            readiness["import_and_duplicate_blockers"]["representation_control_status"],
            "representation_near_duplicate_holdout",
        )
        self.assertTrue(
            any(mode["id"] == "heme_peroxidase_collapse_risk" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])

    def test_dna_glycosylase_lyase_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_dna_glycosylase_lyase_readiness_packet_20260520.json"
        )
        metadata = packet["metadata"]
        readiness = packet["family_readiness"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            readiness["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(len(readiness["positive_like_rows"]), 1)
        self.assertEqual(readiness["positive_like_rows"][0]["accession"], "P06746")
        self.assertEqual(
            readiness["positive_like_rows"][0]["family_axis_status"],
            "review_only_dna_pol_x_lyase_axis_contrast_ready",
        )
        self.assertFalse(
            readiness["cofactor_and_active_site_evidence"]["dna_pol_x_lyase_axis"][
                "source_free_geometry_axis_ready"
            ]
        )
        self.assertEqual(
            readiness["cofactor_and_active_site_evidence"]["dna_pol_x_lyase_axis"][
                "source_active_site_lys_positions"
            ],
            [72],
        )
        self.assertEqual(
            readiness["import_and_duplicate_blockers"]["broader_duplicate_screening_status"],
            "broader_duplicate_screening_required",
        )
        self.assertTrue(
            any(mode["id"] == "representation_conflict_holdout" for mode in packet["likely_failure_modes"])
        )
        self.assertTrue(packet["next_experiment"]["selection_freeze_required_before_scoring"])
        self.assertFalse(packet["next_experiment"]["decision_to_start_now"])

    def test_family_readiness_refresh_adds_schiff_base_without_promotion(self) -> None:
        index = _load_json(
            ARTIFACTS / "v3_mechanism_family_readiness_index_refresh_20260520.json"
        )
        metadata = index["metadata"]
        conclusion = index["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["family_packet_count"], 6)

        rows = {row["family_id"]: row for row in index["rows"]}
        self.assertEqual(
            set(rows),
            {
                "sdr_nad_p_redox",
                "akr_nadp_redox",
                "glycoside_hydrolase",
                "sugar_phosphate_isomerase",
                "schiff_base_lyase",
                "dna_glycosylase_lyase",
            },
        )
        self.assertEqual(rows["glycoside_hydrolase"]["priority_rank"], 1)
        self.assertEqual(rows["schiff_base_lyase"]["priority_rank"], 2)
        self.assertEqual(rows["dna_glycosylase_lyase"]["priority_rank"], 3)
        self.assertEqual(rows["schiff_base_lyase"]["positive_like_row_count"], 1)
        self.assertEqual(rows["dna_glycosylase_lyase"]["positive_like_row_count"], 1)
        self.assertTrue(
            all(row["selection_freeze_required_before_scoring"] for row in rows.values())
        )
        self.assertTrue(all(not row["ready_for_label_import"] for row in rows.values()))
        self.assertTrue(conclusion["do_not_promote_any_family_now"])

    def test_source_complete_external_surface_is_not_reused_as_prospective(self) -> None:
        review = _load_json(
            ARTIFACTS
            / "v3_source_complete_external_minicampaign_blocker_review_20260520.json"
        )
        metadata = review["metadata"]
        decision = review["decision"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["candidate_selection_before_outcome_scoring"])
        self.assertFalse(decision["can_reuse_as_new_prospective_external_minicampaign"])
        self.assertEqual(metadata["source_complete_surface_candidate_count"], 6)
        self.assertEqual(metadata["source_complete_sequence_no_signal_count"], 6)
        self.assertEqual(metadata["source_complete_terminal_rejection_count"], 6)
        self.assertEqual(
            metadata["terminal_decision_status_counts"],
            {"rejected_current_countable_structural_duplicate_signal": 6},
        )
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(
            all(
                row["terminal_decision"]
                == "rejected_current_countable_structural_duplicate_signal"
                for row in review["rows"]
            )
        )

    def test_schiff_base_control_tranche_is_frozen_before_scoring(self) -> None:
        tranche = _load_json(
            ARTIFACTS
            / "v3_schiff_base_lyase_control_tranche_preregistration_20260520.json"
        )
        metadata = tranche["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertEqual(metadata["external_candidate_count"], 1)
        self.assertEqual(metadata["current_control_count"], 14)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["control_role_counts"],
            {
                "current_heme_peroxidase_oxidase_control": 5,
                "current_metal_dependent_hydrolase_non_lyase_control": 2,
                "current_plp_dependent_enzyme_control": 5,
                "current_ser_his_acid_hydrolase_non_lyase_control": 2,
                "external_schiff_base_lyase_positive_like_candidate": 1,
            },
        )

        rows = tranche["rows"]
        self.assertEqual(rows[0]["row_id"], "uniprot:Q9BXD5")
        self.assertEqual(
            rows[0]["row_role"],
            "external_schiff_base_lyase_positive_like_candidate",
        )
        self.assertTrue(
            all(row["score_status"] == "not_scored_in_this_preregistration" for row in rows)
        )
        self.assertIn("frozen", tranche["next_step"].lower())

    def test_schiff_base_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_schiff_base_lyase_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]
        conclusion = decisions["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 14, "needs_review": 1},
        )
        self.assertEqual(metadata["source_free_schiff_base_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = decisions["rows"]
        q9bxd5 = next(row for row in rows if row["row_id"] == "uniprot:Q9BXD5")
        self.assertEqual(q9bxd5["terminal_decision"], "needs_review")
        self.assertFalse(
            q9bxd5["source_traced_schiff_base_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(q9bxd5["heme_plp_cofactor_axis"]["heme_ligand_context_absent"])
        self.assertTrue(
            all(row["selection_frozen_before_axis_scoring"] for row in rows)
        )
        self.assertEqual(
            conclusion["overall"],
            "schiff_base_lyase_remains_review_only_and_not_production_ready",
        )

    def test_schiff_base_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_schiff_base_lyase_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 15)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {"mechanism_match": 14, "needs_review": 1},
        )
        self.assertEqual(
            metrics["review_only_axis_triage"]["source_free_schiff_base_axis_ready_count"],
            0,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"]["keyword_status_counts"],
            {"no_target_keyword_hit": 13, "target_keyword_hit": 2},
        )
        self.assertFalse(metrics["ec_keyword_name_proxy"]["detects_source_free_axis_gap"])
        self.assertEqual(
            metrics["bounded_sequence_nearest_neighbor"][
                "q9bxd5_sequence_import_safety_status"
            ],
            "bounded_current_reference_no_near_duplicate_signal",
        )
        self.assertFalse(
            metrics["esm_sidecar_representation"]["superiority_claim_supported"]
        )
        self.assertFalse(
            metrics["foldseek_current_countable_sidecar"]["available_for_q9bxd5_in_this_tranche"]
        )

    def test_dna_glycosylase_control_tranche_is_frozen_before_scoring(self) -> None:
        tranche = _load_json(
            ARTIFACTS
            / "v3_dna_glycosylase_lyase_control_tranche_preregistration_20260520.json"
        )
        metadata = tranche["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertEqual(metadata["external_candidate_count"], 1)
        self.assertEqual(metadata["current_control_count"], 10)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["control_role_counts"],
            {
                "current_flavin_dehydrogenase_reductase_control": 5,
                "current_out_of_scope_representation_control": 5,
                "external_dna_glycosylase_lyase_positive_like_candidate": 1,
            },
        )
        self.assertEqual(tranche["rows"][0]["row_id"], "uniprot:P06746")
        self.assertTrue(
            all(row["score_status"] == "not_scored_in_this_preregistration" for row in tranche["rows"])
        )

    def test_dna_glycosylase_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_dna_glycosylase_lyase_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]
        conclusion = decisions["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 5, "needs_review": 1, "out_of_scope": 5},
        )
        self.assertEqual(metadata["source_free_dna_lyase_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        p06746 = next(row for row in decisions["rows"] if row["row_id"] == "uniprot:P06746")
        self.assertEqual(p06746["terminal_decision"], "needs_review")
        self.assertFalse(
            p06746["source_traced_dna_lyase_axis"]["source_free_geometry_axis_ready"]
        )
        self.assertEqual(
            p06746["source_traced_dna_lyase_axis"]["source_active_site_lys_positions"],
            [72],
        )
        self.assertEqual(
            conclusion["overall"],
            "dna_glycosylase_lyase_remains_review_only_and_not_production_ready",
        )

    def test_dna_glycosylase_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_dna_glycosylase_lyase_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {"mechanism_match": 5, "needs_review": 1, "out_of_scope": 5},
        )
        self.assertEqual(
            metrics["review_only_axis_triage"]["source_free_dna_lyase_axis_ready_count"],
            0,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"]["keyword_status_counts"],
            {"no_target_keyword_hit": 10, "target_keyword_hit": 1},
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["detects_source_free_geometry_axis_gap"]
        )
        self.assertEqual(
            metrics["bounded_sequence_nearest_neighbor"][
                "p06746_sequence_import_safety_status"
            ],
            "bounded_current_reference_no_near_duplicate_signal",
        )
        self.assertFalse(
            metrics["esm_sidecar_representation"]["superiority_claim_supported"]
        )
        self.assertFalse(
            metrics["foldseek_current_countable_sidecar"]["available_for_p06746_in_this_tranche"]
        )

    def test_post_tranche_family_index_keeps_all_families_no_go(self) -> None:
        index = _load_json(
            ARTIFACTS
            / "v3_mechanism_family_readiness_index_post_tranche_refresh_20260520.json"
        )
        metadata = index["metadata"]
        conclusion = index["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["family_packet_count"], 6)
        self.assertEqual(metadata["closed_review_tranche_count"], 5)
        self.assertEqual(metadata["remaining_packet_only_family_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["next_recommended_tranche_frozen"])

        closed = {row["family_id"]: row for row in index["closed_review_tranches"]}
        self.assertEqual(
            set(closed),
            {
                "glycoside_hydrolase",
                "schiff_base_lyase",
                "dna_glycosylase_lyase",
                "sdr_akr_nadp_redox_boundary",
                "sugar_phosphate_isomerase",
            },
        )
        self.assertTrue(
            all(row["source_free_axis_ready_count"] == 0 for row in closed.values())
        )
        remaining = {row["family_id"] for row in index["remaining_packet_only_families"]}
        self.assertEqual(remaining, set())
        self.assertEqual(
            index["recommended_next_main_loop_experiment"]["id"],
            "new_source_complete_external_minicampaign_or_new_family_readiness_packet",
        )
        self.assertEqual(
            index["recommended_next_main_loop_experiment"]["status"],
            "queue_exhausted_pending_new_source",
        )
        self.assertTrue(conclusion["do_not_promote_any_family_now"])

    def test_sdr_akr_control_tranche_is_frozen_before_scoring(self) -> None:
        tranche = _load_json(
            ARTIFACTS / "v3_sdr_akr_nadp_control_tranche_preregistration_20260520.json"
        )
        metadata = tranche["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(metadata["external_candidate_count"], 6)
        self.assertEqual(metadata["current_control_count"], 8)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["control_role_counts"],
            {
                "current_flavin_redox_control": 4,
                "current_heme_redox_control": 4,
                "external_akr_nadp_positive_like_candidate": 1,
                "external_sdr_ec_1_1_1_clean_abstention_control": 4,
                "external_sdr_positive_like_candidate": 1,
            },
        )
        self.assertEqual(tranche["rows"][0]["row_id"], "uniprot:O14756")
        self.assertEqual(tranche["rows"][1]["row_id"], "uniprot:C9JRZ8")
        self.assertTrue(
            all(row["score_status"] == "not_scored_in_this_preregistration" for row in tranche["rows"])
        )

    def test_sugar_phosphate_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_sugar_phosphate_isomerase_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]
        conclusion = decisions["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"mechanism_match": 6, "needs_review": 1, "out_of_scope": 4},
        )
        self.assertEqual(metadata["source_free_sugar_phosphate_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["uniprot:P34949"]["terminal_decision"], "needs_review")
        self.assertFalse(
            rows["uniprot:P34949"]["source_traced_sugar_phosphate_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(rows["uniprot:P34949"]["flavin_contrast_axis"]["flavin_ligand_context_absent"])
        self.assertTrue(all(row["selection_frozen_before_axis_scoring"] for row in rows.values()))
        self.assertEqual(
            conclusion["overall"],
            "sugar_phosphate_isomerase_remains_review_only_and_not_production_ready",
        )

    def test_sugar_phosphate_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_sugar_phosphate_isomerase_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {"mechanism_match": 6, "needs_review": 1, "out_of_scope": 4},
        )
        self.assertEqual(
            metrics["review_only_axis_triage"][
                "source_free_sugar_phosphate_axis_ready_count"
            ],
            0,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"]["keyword_status_counts"],
            {"no_target_keyword_hit": 10, "target_keyword_hit": 1},
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["detects_source_free_axis_gap"]
        )
        self.assertFalse(
            metrics["foldseek_current_countable_sidecar"][
                "available_for_p34949_in_this_tranche"
            ]
        )

    def test_sdr_akr_control_tranche_decisions_stay_review_only(self) -> None:
        decisions = _load_json(
            ARTIFACTS
            / "v3_sdr_akr_nadp_control_tranche_axis_decisions_20260520.json"
        )
        metadata = decisions["metadata"]
        conclusion = decisions["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"ambiguous": 4, "mechanism_match": 8, "needs_review": 2},
        )
        self.assertEqual(metadata["source_free_sdr_akr_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in decisions["rows"]}
        self.assertEqual(rows["uniprot:O14756"]["terminal_decision"], "needs_review")
        self.assertEqual(rows["uniprot:C9JRZ8"]["terminal_decision"], "needs_review")
        self.assertFalse(
            rows["uniprot:O14756"]["source_traced_sdr_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertFalse(
            rows["uniprot:C9JRZ8"]["source_traced_akr_axis"][
                "source_free_position_policy_ready"
            ]
        )
        self.assertTrue(all(row["selection_frozen_before_axis_scoring"] for row in rows.values()))
        self.assertEqual(
            conclusion["overall"],
            "sdr_akr_nadp_redox_boundary_remains_review_only_and_not_production_ready",
        )

    def test_sdr_akr_baseline_comparison_makes_no_claim(self) -> None:
        comparison = _load_json(
            ARTIFACTS
            / "v3_sdr_akr_nadp_control_tranche_baseline_comparison_20260520.json"
        )
        metadata = comparison["metadata"]
        metrics = comparison["metrics"]

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["superiority_claim_permitted"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertFalse(comparison["task_definition"]["positive_claim_allowed"])
        self.assertEqual(
            metrics["review_only_axis_triage"]["terminal_decision_counts"],
            {"ambiguous": 4, "mechanism_match": 8, "needs_review": 2},
        )
        self.assertEqual(
            metrics["review_only_axis_triage"]["source_free_sdr_akr_axis_ready_count"],
            0,
        )
        self.assertEqual(
            metrics["ec_keyword_name_proxy"]["keyword_status_counts"],
            {"no_target_keyword_hit": 3, "target_keyword_hit": 11},
        )
        self.assertFalse(
            metrics["ec_keyword_name_proxy"]["detects_source_free_axis_gap"]
        )
        self.assertEqual(
            metrics["bounded_sequence_nearest_neighbor"][
                "o14756_sequence_import_safety_status"
            ],
            "bounded_current_reference_no_near_duplicate_signal",
        )
        self.assertFalse(
            metrics["foldseek_current_countable_sidecar"][
                "available_for_external_positive_like_rows_in_this_tranche"
            ]
        )

    def test_sugar_phosphate_control_tranche_is_frozen_before_scoring(self) -> None:
        tranche = _load_json(
            ARTIFACTS
            / "v3_sugar_phosphate_isomerase_control_tranche_preregistration_20260520.json"
        )
        metadata = tranche["metadata"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_before_outcome_scoring"])
        self.assertEqual(metadata["frozen_row_count"], 11)
        self.assertEqual(metadata["external_candidate_count"], 1)
        self.assertEqual(metadata["current_control_count"], 10)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["control_role_counts"],
            {
                "current_flavin_dehydrogenase_reductase_control": 4,
                "current_flavin_monooxygenase_control": 2,
                "current_out_of_scope_control": 4,
                "external_sugar_phosphate_isomerase_positive_like_candidate": 1,
            },
        )
        self.assertEqual(tranche["rows"][0]["row_id"], "uniprot:P34949")
        self.assertEqual(
            {row["row_id"] for row in tranche["rows"] if row["row_role"].startswith("current_")},
            {
                "m_csa:1",
                "m_csa:2",
                "m_csa:3",
                "m_csa:4",
                "m_csa:6",
                "m_csa:7",
                "m_csa:20",
                "m_csa:68",
                "m_csa:131",
                "m_csa:132",
            },
        )
        self.assertTrue(
            all(row["score_status"] == "not_scored_in_this_preregistration" for row in tranche["rows"])
        )


if __name__ == "__main__":
    unittest.main()
