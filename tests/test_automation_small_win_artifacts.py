import hashlib
import csv
import json
from collections import Counter
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

    def test_late_handoff_only_epk_synthesis_keeps_main_loop_off_epk(self) -> None:
        synthesis = _load_json(
            ARTIFACTS
            / "v3_epk_late_handoff_only_research_lane_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_lane_handoffs_since_prior_synthesis"])
        self.assertEqual(metadata["lane_count"], 5)
        self.assertEqual(metadata["input_json_validation_error_count"], 0)
        self.assertEqual(metadata["input_jsonl_validation_error_count"], 0)
        self.assertFalse(metadata["production_scoring_authorized"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["main_loop_should_continue_epk_by_default"])

        self.assertEqual(
            conclusion["overall"],
            "fresh_late_epk_handoffs_reinforce_review_only_no_go_and_define_research_lane_next_experiments",
        )
        self.assertEqual(
            conclusion["five_uj7_status"],
            "already_synthesized_and_now_pinned_as_biological_assembly_1_context_v4_only_split_failure",
        )
        self.assertEqual(
            conclusion["main_loop_action"],
            "do_not_resume_epk_as_default_main_loop_task; continue external terminal decision deepening",
        )
        lanes = {row["lane_id"]: row for row in synthesis["lane_findings"]}
        self.assertEqual(
            lanes["epk_positive_evidence"]["primary_outcome"],
            "review_only_source_site_row_without_active_donor",
        )
        self.assertEqual(
            lanes["epk_substrate_role_identity"]["primary_outcome"],
            "acid_base_proximity_review_feature_not_promotion_rule",
        )
        self.assertEqual(
            lanes["epk_false_positive_hunter"]["primary_outcome"],
            "regression_rows_emitted_without_new_unsafe_nonabstention",
        )
        self.assertEqual(
            lanes["epk_policy_harness"]["next_exact_experiment"],
            "epk_real_lane_metal_absent_candidate_evidence_v10_review_only",
        )
        self.assertEqual(
            lanes["epk_sibling_controls"]["primary_outcome"],
            "surface_certified_for_future_source_free_active_state_candidate_attempt",
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

    def test_second_metal_phosphatase_packet_converts_more_frozen_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_coordinate_materialization_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_current_countable_structural_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_terminal_decision_packet_second_selection_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_metal_20260521.json"
        )
        rescue = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_timeout_targeted_rescue_screen_20260521.json"
        )
        final_packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_terminal_decision_packet_second_after_timeout_rescue_20260521.json"
        )
        final_benchmark = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_second_after_timeout_rescue_modern_baseline_benchmark_20260521.json"
        )
        final_rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_metal_timeout_rescue_20260521.json"
        )
        q99504_probe = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_q99504_current_metal_target_probe_20260521.json"
        )
        q99504_nonmetal_probe = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_q99504_current_nonmetal_chunk000_probe_20260521.json"
        )
        q99504_nonmetal_probe_001 = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_q99504_current_nonmetal_chunk001_probe_20260521.json"
        )
        q99504_nonmetal_followups = [
            _load_json(
                ARTIFACTS
                / (
                    "v3_metal_phosphatase_q99504_current_nonmetal_"
                    f"chunk{chunk_index:03d}_probe_20260521.json"
                )
            )
            for chunk_index in range(2, 8)
        ]
        q99504_closure = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_q99504_full_current_countable_"
                "duplicate_closure_20260521.json"
            )
        )
        q99504_final_packet = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_terminal_decision_packet_second_"
                "after_q99504_duplicate_closure_20260521.json"
            )
        )
        q99504_final_benchmark = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_packet_second_after_q99504_"
                "duplicate_closure_modern_baseline_benchmark_20260521.json"
            )
        )
        q99504_final_rollup = _load_json(
            ARTIFACTS
            / (
                "v3_external_deep_terminal_decision_rollup_post_q99504_"
                "duplicate_closure_20260521.json"
            )
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertFalse(
            selection["metadata"]["foldseek_current_countable_screen_run_at_selection"]
        )
        self.assertTrue(
            all(
                row["score_status_at_selection"]
                == "not_scored_at_second_deep_packet_selection"
                for row in selection["rows"]
            )
        )

        self.assertTrue(coordinates["metadata"]["review_only"])
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            coordinates["metadata"]["coordinate_status_counts"],
            {"coordinate_sidecar_materialized": 7},
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertEqual(screen["metadata"]["candidate_count"], 7)
        self.assertEqual(
            screen["metadata"]["foldseek_query_run_status_counts"],
            {"completed": 5, "foldseek_run_timeout": 2},
        )
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {
                "current_countable_structural_duplicate_signal": 5,
                "current_countable_structural_screen_incomplete": 2,
            },
        )
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 5)
        self.assertFalse(screen["metadata"]["pair_cache_complete"])
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(screen["metadata"]["raw_name_mapping_unmapped_count"], 0)
        self.assertFalse(screen["metadata"]["ready_for_label_import"])
        completed_rows = [
            row for row in screen["rows"] if row["foldseek_run_status"] == "completed"
        ]
        self.assertEqual(len(completed_rows), 5)
        self.assertTrue(all(row["pair_cache_complete"] for row in completed_rows))
        self.assertTrue(
            all(row["current_countable_high_tm_hit_count"] > 0 for row in completed_rows)
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 5)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        allowed = set(packet["metadata"]["allowed_terminal_decisions"])
        self.assertLessEqual({row["terminal_decision"] for row in packet["rows"]}, allowed)
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in packet_rows.items()
                if row["terminal_decision"] == "needs_new_extractor_or_structure"
            },
            {"Q99504", "P05186"},
        )
        self.assertEqual(
            {
                accession
                for accession, row in packet_rows.items()
                if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
            },
            {"O14595", "O15194", "P0AF24", "Q42546", "P0A8Y3"},
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
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )
        self.assertEqual(
            benchmark["metrics"]["deterministic_sequence_kmer_nearest_neighbor"][
                "exact_current_reference_sequence_match_count"
            ],
            0,
        )
        self.assertFalse(
            benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported"
            ]
        )
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

        self.assertTrue(rollup["metadata"]["review_only"])
        self.assertEqual(rollup["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(rollup["metadata"]["deep_packet_count"], 7)
        self.assertEqual(rollup["metadata"]["candidate_count"], 49)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 45,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(
            rollup["synthesis"]["non_needs_review_terminal_candidate_count"],
            47,
        )
        self.assertFalse(rollup["metadata"]["ready_for_label_import"])
        self.assertFalse(rollup["metadata"]["curated_label_registry_edited"])
        self.assertFalse(rollup["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(rollup["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(rollup["metadata"]["removal_allowed_set_true"])

        self.assertTrue(rescue["metadata"]["review_only"])
        self.assertEqual(rescue["metadata"]["candidate_count"], 2)
        self.assertEqual(
            rescue["metadata"]["foldseek_query_run_status_counts"],
            {"completed": 2},
        )
        self.assertEqual(
            rescue["metadata"]["targeted_current_subset_screen_status_counts"],
            {
                "current_countable_targeted_duplicate_signal": 1,
                "targeted_current_subset_no_duplicate_signal_detected": 1,
            },
        )
        self.assertFalse(rescue["metadata"]["duplicate_clear_claim_permitted"])
        self.assertFalse(rescue["metadata"]["ready_for_label_import"])

        self.assertTrue(final_packet["metadata"]["review_only"])
        self.assertEqual(
            final_packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        final_rows = {row["accession"]: row for row in final_packet["rows"]}
        self.assertEqual(
            final_rows["P05186"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertEqual(
            final_rows["Q99504"]["terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertFalse(final_packet["metadata"]["ready_for_label_import"])
        self.assertFalse(final_packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(final_packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(final_packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(final_packet["metadata"]["removal_allowed_set_true"])

        self.assertFalse(final_benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            final_benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertFalse(
            final_benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported"
            ]
        )

        self.assertTrue(final_rollup["metadata"]["review_only"])
        self.assertEqual(final_rollup["metadata"]["candidate_count"], 49)
        self.assertEqual(final_rollup["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            final_rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 46,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(
            final_rollup["synthesis"]["non_needs_review_terminal_candidate_count"],
            48,
        )
        self.assertFalse(final_rollup["metadata"]["ready_for_label_import"])
        self.assertFalse(final_rollup["metadata"]["curated_label_registry_edited"])
        self.assertFalse(final_rollup["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(final_rollup["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(final_rollup["metadata"]["removal_allowed_set_true"])

        self.assertTrue(q99504_probe["metadata"]["review_only"])
        self.assertEqual(q99504_probe["metadata"]["candidate_count"], 1)
        self.assertEqual(q99504_probe["metadata"]["foldseek_run_status"], "completed")
        self.assertEqual(q99504_probe["metadata"]["target_subset_coordinate_count"], 67)
        self.assertEqual(q99504_probe["metadata"]["unique_query_target_pair_count"], 67)
        self.assertEqual(q99504_probe["metadata"]["high_tm_hit_count"], 0)
        self.assertFalse(q99504_probe["metadata"]["duplicate_clear_claim_permitted"])
        self.assertFalse(q99504_probe["metadata"]["ready_for_label_import"])
        self.assertEqual(
            q99504_probe["rows"][0]["terminal_decision_after_probe"],
            "needs_new_extractor_or_structure",
        )
        self.assertIsNotNone(q99504_probe["rows"][0]["exact_blocker_if_not_terminal"])

        self.assertTrue(q99504_nonmetal_probe["metadata"]["review_only"])
        self.assertEqual(q99504_nonmetal_probe["metadata"]["candidate_count"], 1)
        self.assertEqual(
            q99504_nonmetal_probe["metadata"]["foldseek_run_status"],
            "completed",
        )
        self.assertEqual(
            q99504_nonmetal_probe["metadata"]["target_subset_coordinate_count"],
            80,
        )
        self.assertEqual(
            q99504_nonmetal_probe["metadata"]["unique_query_target_pair_count"],
            80,
        )
        self.assertEqual(q99504_nonmetal_probe["metadata"]["high_tm_hit_count"], 0)
        self.assertFalse(
            q99504_nonmetal_probe["metadata"]["duplicate_clear_claim_permitted"]
        )
        self.assertFalse(q99504_nonmetal_probe["metadata"]["ready_for_label_import"])
        self.assertEqual(
            q99504_nonmetal_probe["rows"][0]["terminal_decision_after_probe"],
            "needs_new_extractor_or_structure",
        )
        self.assertIsNotNone(
            q99504_nonmetal_probe["rows"][0]["exact_blocker_if_not_terminal"]
        )
        self.assertTrue(q99504_nonmetal_probe_001["metadata"]["review_only"])
        self.assertEqual(q99504_nonmetal_probe_001["metadata"]["candidate_count"], 1)
        self.assertEqual(
            q99504_nonmetal_probe_001["metadata"]["foldseek_run_status"],
            "completed",
        )
        self.assertEqual(
            q99504_nonmetal_probe_001["metadata"]["target_subset_coordinate_count"],
            80,
        )
        self.assertEqual(
            q99504_nonmetal_probe_001["metadata"]["unique_query_target_pair_count"],
            80,
        )
        self.assertEqual(q99504_nonmetal_probe_001["metadata"]["high_tm_hit_count"], 0)
        self.assertFalse(
            q99504_nonmetal_probe_001["metadata"]["duplicate_clear_claim_permitted"]
        )
        self.assertFalse(q99504_nonmetal_probe_001["metadata"]["ready_for_label_import"])

        expected_followup_counts = [80, 80, 80, 80, 80, 43]
        for followup, expected_count in zip(
            q99504_nonmetal_followups, expected_followup_counts
        ):
            self.assertTrue(followup["metadata"]["review_only"])
            self.assertEqual(followup["metadata"]["candidate_count"], 1)
            self.assertEqual(followup["metadata"]["foldseek_run_status"], "completed")
            self.assertEqual(
                followup["metadata"]["target_subset_coordinate_count"],
                expected_count,
            )
            self.assertEqual(
                followup["metadata"]["unique_query_target_pair_count"],
                expected_count,
            )
            self.assertEqual(followup["metadata"]["high_tm_hit_count"], 0)
            self.assertFalse(followup["metadata"]["ready_for_label_import"])
            self.assertFalse(followup["metadata"]["removal_allowed_set_true"])

        self.assertTrue(q99504_closure["metadata"]["review_only"])
        self.assertEqual(q99504_closure["metadata"]["candidate_count"], 1)
        self.assertEqual(q99504_closure["metadata"]["current_countable_target_count"], 672)
        self.assertEqual(
            q99504_closure["metadata"]["unique_query_target_pair_count"],
            672,
        )
        self.assertEqual(q99504_closure["metadata"]["query_target_pair_coverage"], 1.0)
        self.assertTrue(
            q99504_closure["metadata"][
                "pair_cache_complete_for_bounded_current_countable_screen"
            ]
        )
        self.assertEqual(q99504_closure["metadata"]["high_tm_hit_count"], 0)
        self.assertTrue(
            q99504_closure["metadata"][
                "bounded_current_countable_duplicate_clear_claim_permitted"
            ]
        )
        self.assertEqual(
            q99504_closure["metadata"]["probe_decision"],
            "terminal_rejection_insufficient_evidence",
        )
        self.assertFalse(q99504_closure["metadata"]["ready_for_label_import"])
        self.assertFalse(q99504_closure["metadata"]["curated_label_registry_edited"])
        self.assertFalse(q99504_closure["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(
            q99504_closure["metadata"]["artifact_upload_or_removal_performed"]
        )
        self.assertFalse(q99504_closure["metadata"]["removal_allowed_set_true"])
        self.assertEqual(
            q99504_closure["rows"][0]["current_geometry_retrieval_score_summary"][
                "target_lane_score"
            ],
            0.3742,
        )
        self.assertFalse(
            q99504_closure["rows"][0]["current_geometry_retrieval_score_summary"][
                "target_lane_at_or_above_floor"
            ]
        )
        self.assertEqual(
            q99504_closure["rows"][0]["duplicate_leakage_screen"][
                "current_countable_high_tm_hit_count"
            ],
            0,
        )
        self.assertEqual(
            q99504_closure["rows"][0]["terminal_decision_after_full_current_probe"],
            "terminal_rejection_insufficient_evidence",
        )
        self.assertIsNone(q99504_closure["rows"][0]["exact_blocker_if_not_terminal"])

        self.assertEqual(
            q99504_final_packet["metadata"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 6,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(
            q99504_final_packet["metadata"]["non_needs_review_terminal_count"],
            7,
        )
        q99504_final_rows = {
            row["accession"]: row for row in q99504_final_packet["rows"]
        }
        self.assertEqual(
            q99504_final_rows["Q99504"]["terminal_decision"],
            "terminal_rejection_insufficient_evidence",
        )
        self.assertTrue(
            q99504_final_rows["Q99504"]["duplicate_leakage_screen"][
                "pair_cache_complete"
            ]
        )
        self.assertFalse(q99504_final_packet["metadata"]["ready_for_label_import"])
        self.assertFalse(q99504_final_packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(q99504_final_packet["metadata"]["fingerprint_registry_edited"])

        self.assertEqual(
            q99504_final_benchmark["metrics"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 6,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertFalse(q99504_final_benchmark["metrics"]["superiority_claim"])
        self.assertTrue(
            q99504_final_benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported_for_q99504_current_countable_scope"
            ]
        )

        self.assertEqual(q99504_final_rollup["metadata"]["candidate_count"], 49)
        self.assertEqual(
            q99504_final_rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 46,
                "terminal_rejection_insufficient_evidence": 2,
            },
        )
        self.assertEqual(
            q99504_final_rollup["synthesis"][
                "non_needs_review_terminal_candidate_count"
            ],
            49,
        )
        self.assertFalse(q99504_final_rollup["metadata"]["ready_for_label_import"])

    def test_remaining_metal_phosphatase_rows_get_targeted_screen_packet(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_packet_remaining_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_packet_remaining_coordinate_"
                "materialization_20260521.json"
            )
        )
        screen = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_packet_remaining_targeted_current_"
                "metal_screen_20260521.json"
            )
        )
        packet = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_terminal_decision_packet_remaining_"
                "after_targeted_metal_screen_20260521.json"
            )
        )
        benchmark = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_packet_remaining_targeted_metal_"
                "modern_baseline_benchmark_20260521.json"
            )
        )
        rollup = _load_json(
            ARTIFACTS
            / (
                "v3_external_deep_terminal_decision_rollup_post_remaining_"
                "metal_targeted_screen_20260521.json"
            )
        )
        nonmetal_chunks = [
            _load_json(
                ARTIFACTS
                / (
                    "v3_metal_phosphatase_remaining_nonmetal_"
                    f"chunk{chunk_index:03d}_probe_20260521.json"
                )
            )
            for chunk_index in range(8)
        ]
        full_closure = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_remaining_full_current_countable_"
                "duplicate_closure_20260521.json"
            )
        )
        final_packet = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_terminal_decision_packet_remaining_"
                "after_full_current_duplicate_closure_20260521.json"
            )
        )
        final_benchmark = _load_json(
            ARTIFACTS
            / (
                "v3_metal_phosphatase_deep_packet_remaining_after_full_current_"
                "duplicate_closure_modern_baseline_benchmark_20260521.json"
            )
        )
        final_rollup = _load_json(
            ARTIFACTS
            / (
                "v3_external_deep_terminal_decision_rollup_post_remaining_"
                "metal_full_current_duplicate_closure_20260521.json"
            )
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertEqual(selection["metadata"]["candidate_count"], 3)
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"P75792", "P77247", "P0A8Y5"},
        )

        self.assertEqual(
            coordinates["metadata"]["coordinate_status_counts"],
            {"coordinate_sidecar_materialized": 3},
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertFalse(coordinates["metadata"]["ready_for_label_import"])

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertEqual(screen["metadata"]["foldseek_run_status"], "completed")
        self.assertEqual(screen["metadata"]["target_subset_coordinate_count"], 67)
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 201)
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 1)
        self.assertEqual(
            screen["metadata"]["status_counts"],
            {
                "current_metal_target_duplicate_signal": 1,
                "targeted_current_metal_no_duplicate_signal_detected": 2,
            },
        )
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertFalse(screen["metadata"]["ready_for_label_import"])

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 1,
            },
        )
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            packet_rows["P77247"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertEqual(
            packet_rows["P77247"]["duplicate_leakage_screen"][
                "current_metal_high_tm_hit_count"
            ],
            1,
        )
        self.assertEqual(
            packet_rows["P75792"]["terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertEqual(
            packet_rows["P0A8Y5"]["terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])

        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 1,
            },
        )
        self.assertFalse(
            benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported"
            ]
        )

        self.assertEqual(rollup["metadata"]["candidate_count"], 52)
        self.assertEqual(rollup["metadata"]["deep_packet_count"], 8)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 47,
                "terminal_rejection_insufficient_evidence": 2,
            },
        )
        self.assertFalse(rollup["metadata"]["ready_for_label_import"])

        expected_nonmetal_target_counts = [80, 80, 80, 80, 80, 80, 80, 45]
        expected_nonmetal_pair_counts = [160, 160, 160, 160, 160, 160, 160, 90]
        for chunk, target_count, pair_count in zip(
            nonmetal_chunks,
            expected_nonmetal_target_counts,
            expected_nonmetal_pair_counts,
        ):
            self.assertTrue(chunk["metadata"]["review_only"])
            self.assertEqual(chunk["metadata"]["candidate_count"], 2)
            self.assertEqual(chunk["metadata"]["foldseek_run_status"], "completed")
            self.assertEqual(
                chunk["metadata"]["target_subset_coordinate_count"],
                target_count,
            )
            self.assertEqual(
                chunk["metadata"]["unique_query_target_pair_count"],
                pair_count,
            )
            self.assertEqual(chunk["metadata"]["high_tm_candidate_count"], 0)
            self.assertFalse(chunk["metadata"]["ready_for_label_import"])
            self.assertFalse(chunk["metadata"]["removal_allowed_set_true"])

        self.assertTrue(full_closure["metadata"]["review_only"])
        self.assertEqual(full_closure["metadata"]["candidate_count"], 2)
        self.assertEqual(
            full_closure["metadata"]["current_countable_target_count_per_candidate"],
            672,
        )
        self.assertEqual(
            full_closure["metadata"]["unique_query_target_pair_count"],
            1344,
        )
        self.assertEqual(full_closure["metadata"]["query_target_pair_coverage"], 1.0)
        self.assertTrue(
            full_closure["metadata"][
                "pair_cache_complete_for_bounded_current_countable_screen"
            ]
        )
        self.assertTrue(
            full_closure["metadata"][
                "bounded_current_countable_duplicate_clear_claim_permitted"
            ]
        )
        self.assertEqual(full_closure["metadata"]["high_tm_hit_count"], 0)
        self.assertEqual(full_closure["metadata"]["max_completed_tm_score"], 0.6855)
        self.assertEqual(
            full_closure["metadata"]["probe_decision_counts"],
            {"needs_new_extractor_or_structure": 2},
        )
        self.assertFalse(full_closure["metadata"]["ready_for_label_import"])
        self.assertFalse(full_closure["metadata"]["curated_label_registry_edited"])
        self.assertFalse(full_closure["metadata"]["fingerprint_registry_edited"])
        closure_rows = {row["accession"]: row for row in full_closure["rows"]}
        for accession in {"P75792", "P0A8Y5"}:
            row = closure_rows[accession]
            self.assertEqual(
                row["terminal_decision_after_full_current_duplicate_closure"],
                "needs_new_extractor_or_structure",
            )
            self.assertEqual(
                row["exact_blocker_if_not_terminal"],
                "source_free_geometry_scoring_missing_for_pdb_active_site_features_after_bounded_duplicate_clearance",
            )
            self.assertEqual(
                row["duplicate_leakage_screen"][
                    "current_countable_high_tm_hit_count"
                ],
                0,
            )
            self.assertTrue(row["duplicate_leakage_screen"]["pair_cache_complete"])
            self.assertFalse(
                row["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
            )

        self.assertEqual(
            final_packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 1,
            },
        )
        self.assertEqual(final_packet["metadata"]["non_needs_review_terminal_count"], 3)
        self.assertEqual(
            final_packet["metadata"][
                "bounded_current_countable_duplicate_clear_candidate_count"
            ],
            2,
        )
        final_rows = {row["accession"]: row for row in final_packet["rows"]}
        self.assertEqual(
            final_rows["P77247"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        for accession in {"P75792", "P0A8Y5"}:
            self.assertEqual(
                final_rows[accession]["terminal_decision"],
                "needs_new_extractor_or_structure",
            )
            self.assertEqual(
                final_rows[accession]["exact_blocker_if_not_terminal"],
                "source_free_geometry_scoring_missing_for_pdb_active_site_features_after_bounded_duplicate_clearance",
            )
            self.assertTrue(
                final_rows[accession]["duplicate_leakage_screen"][
                    "bounded_current_countable_duplicate_clear_claim_permitted"
                ]
            )
        self.assertFalse(final_packet["metadata"]["ready_for_label_import"])
        self.assertFalse(final_packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(final_packet["metadata"]["fingerprint_registry_edited"])

        self.assertFalse(final_benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            final_benchmark["metrics"][
                "full_current_countable_duplicate_clear_candidate_count"
            ],
            2,
        )
        self.assertTrue(
            final_benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported_for_no_hit_rows"
            ]
        )
        self.assertEqual(
            final_benchmark["metrics"]["current_countable_high_tm_candidate_count"],
            1,
        )

        self.assertEqual(final_rollup["metadata"]["candidate_count"], 52)
        self.assertEqual(final_rollup["metadata"]["deep_packet_count"], 8)
        self.assertEqual(
            final_rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 47,
                "terminal_rejection_insufficient_evidence": 2,
            },
        )
        self.assertEqual(
            final_rollup["metadata"]["non_needs_review_terminal_candidate_count"],
            52,
        )
        self.assertFalse(final_rollup["metadata"]["ready_for_label_import"])

    def test_serine_hydrolase_targeted_rescue_converts_materialized_rows(self) -> None:
        rescue = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_targeted_current_ser_his_rescue_screen_20260521.json"
        )
        p31614_rescue = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_p31614_pdb_replacement_coordinate_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_pdb_replacement_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_post_p31614_pdb_replacement_modern_baseline_benchmark_20260521.json"
        )

        metadata = rescue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["duplicate_clear_claim_permitted"])
        self.assertEqual(metadata["target_subset_fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertEqual(metadata["target_subset_count"], 40)
        self.assertEqual(metadata["high_tm_candidate_count"], 6)
        self.assertEqual(
            metadata["status_counts"], {"current_ser_his_target_duplicate_signal": 6}
        )
        self.assertGreaterEqual(metadata["max_target_subset_tm_score"], 0.7)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["current_ser_his_high_tm_hit_count"] > 0
                and row["evidence_role"]
                == "targeted_import_gate_duplicate_leakage_evidence_not_predictive_mechanism_evidence"
                for row in rescue["rows"]
            )
        )
        self.assertEqual(
            p31614_rescue["metadata"]["pdb_replacement_coordinate_count"], 2
        )
        self.assertEqual(p31614_rescue["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            p31614_rescue["metadata"]["high_tm_replacement_coordinate_count"], 0
        )
        self.assertLess(p31614_rescue["metadata"]["max_target_subset_tm_score"], 0.7)
        self.assertFalse(p31614_rescue["metadata"]["duplicate_clear_claim_permitted"])

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(
            packet["metadata"]["targeted_current_fingerprint_rescue_high_tm_candidate_count"],
            6,
        )
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        rows = {row["accession"]: row for row in packet["rows"]}
        for accession in {"P54317", "Q9BV23", "P07098", "Q99685", "P04180", "E9LVH9"}:
            self.assertEqual(
                rows[accession]["terminal_decision"],
                "terminal_rejection_duplicate_or_leakage",
            )
            self.assertEqual(
                rows[accession]["duplicate_leakage_screen"][
                    "current_countable_structural_screen_status"
                ],
                "current_countable_structural_duplicate_signal",
            )
            self.assertIsNone(rows[accession]["exact_blocker_if_not_terminal"])
        self.assertEqual(
            rows["P31614"]["terminal_decision"], "needs_new_extractor_or_structure"
        )
        self.assertEqual(
            rows["P31614"]["duplicate_leakage_screen"][
                "current_countable_structural_screen_status"
            ],
            "pdb_replacement_targeted_ser_his_screen_no_high_tm_hit_full_current_screen_incomplete",
        )
        self.assertIn(
            "map UniProt active-site residues onto a PDB replacement coordinate",
            rows["P31614"]["exact_blocker_if_not_terminal"],
        )

        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(
            benchmark["metrics"]["targeted_current_fingerprint_rescue_high_tm_candidate_count"],
            6,
        )
        self.assertEqual(
            benchmark["metrics"]["p31614_pdb_replacement_coordinate_screen"][
                "high_tm_replacement_coordinate_count"
            ],
            0,
        )
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_serine_hydrolase_p31614_pdb_mapping_blocker_is_source_separated(
        self,
    ) -> None:
        blocker = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_p31614_pdb_active_site_mapping_blocker_20260521.json"
        )
        terminal_packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_active_site_mapping_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_post_p31614_active_site_mapping_modern_baseline_benchmark_20260521.json"
        )

        metadata = blocker["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_frozen_before_mapping"])
        self.assertFalse(metadata["p31614_direct_struct_ref_present"])
        self.assertEqual(metadata["resolved_clean_catalytic_residue_count"], 0)
        self.assertEqual(
            metadata["observed_engineered_ser45_to_ala_structure_count"], 2
        )
        self.assertEqual(
            metadata["charge_relay_positions_missing_from_atom_site_count"], 4
        )
        self.assertFalse(metadata["duplicate_clear_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertIn(
            "not text-derived predictive scoring",
            metadata["source_separation_guardrail"],
        )

        row = blocker["row"]
        self.assertEqual(row["accession"], "P31614")
        self.assertEqual(row["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(
            row["active_site_mapping_summary"]["clean_triad_mapping_status"],
            "not_resolved",
        )
        self.assertFalse(
            row["active_site_mapping_summary"]["text_or_label_fields_used_for_predictive_score"]
        )
        self.assertEqual(
            row["duplicate_leakage_screen"]["target_subset_fingerprint_id"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(
            row["duplicate_leakage_screen"]["high_tm_replacement_coordinate_count"], 0
        )
        self.assertFalse(
            row["duplicate_leakage_screen"]["duplicate_clear_claim_permitted"]
        )
        self.assertIn(
            "engineered Ser-to-Ala mutant", row["exact_blocker_if_not_terminal"]
        )
        self.assertIn(
            "positions 342/345 are absent", row["exact_blocker_if_not_terminal"]
        )

        self.assertEqual(
            {structure["structure_id"] for structure in blocker["structures"]},
            {"4C7L", "4C7W"},
        )
        for structure in blocker["structures"]:
            self.assertFalse(structure["p31614_direct_struct_ref_present"])
            self.assertEqual(structure["struct_ref_db_accessions"], ["O55252"])
            position_rows = {
                position["source_position"]: position
                for position in structure["active_site_position_mappings"]
            }
            self.assertEqual(
                position_rows[45]["clean_catalytic_residue_mapping_status"],
                "observed_engineered_ser_to_ala_mutation_not_countable",
            )
            self.assertTrue(position_rows[45]["atom_site_auth_seq_id_found"])
            self.assertGreaterEqual(
                len(position_rows[45]["struct_ref_seq_dif_rows_at_source_position"]),
                1,
            )
            for source_position in (342, 345):
                self.assertFalse(
                    position_rows[source_position]["atom_site_auth_seq_id_found"]
                )
                self.assertEqual(
                    position_rows[source_position]["clean_catalytic_residue_mapping_status"],
                    "missing_from_atom_site_auth_seq_id_scan",
                )

        self.assertEqual(
            terminal_packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(
            terminal_packet["metadata"]["p31614_active_site_mapping_blocker_artifact"],
            "artifacts/v3_serine_hydrolase_p31614_pdb_active_site_mapping_blocker_20260521.json",
        )
        packet_rows = {
            candidate["accession"]: candidate for candidate in terminal_packet["rows"]
        }
        self.assertEqual(
            packet_rows["P31614"]["terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertEqual(
            packet_rows["P31614"]["catalytic_residue_triad_evidence"][
                "clean_triad_mapping_status"
            ],
            "not_resolved",
        )
        self.assertEqual(
            packet_rows["P31614"]["catalytic_residue_triad_evidence"][
                "resolved_clean_active_site_residue_count"
            ],
            0,
        )
        self.assertIn(
            "source_position_45_engineered_SER_to_ALA_mutation",
            packet_rows["P31614"]["counterevidence"],
        )
        self.assertFalse(packet_rows["P31614"]["ready_for_label_import"])

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(
            benchmark["metrics"]["p31614_terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertEqual(
            benchmark["metrics"]["active_site_atom_mapping"][
                "clean_triad_mapping_status"
            ],
            "not_resolved",
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(benchmark["metrics"]["geometry_superiority_claim"], "not_made")
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

    def test_serine_hydrolase_p31614_full_current_probe_is_terminal_leakage(
        self,
    ) -> None:
        probe = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_p31614_full_current_alignment_duplicate_probe_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_full_current_probe_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_deep_packet_post_p31614_full_current_probe_modern_baseline_benchmark_20260521.json"
        )

        metadata = probe["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_frozen_before_scoring"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertTrue(metadata["pair_cache_complete"])
        self.assertEqual(metadata["unique_query_target_pair_count"], 1344)
        self.assertEqual(metadata["expected_query_target_pair_count"], 1344)
        self.assertEqual(metadata["current_countable_coordinate_count"], 672)
        self.assertEqual(metadata["high_tm_replacement_coordinate_count"], 1)
        self.assertEqual(metadata["high_tm_replacement_structure_ids"], ["4C7L"])
        self.assertGreaterEqual(
            metadata["max_external_vs_current_countable_tm_score"], 0.7
        )
        self.assertFalse(metadata["duplicate_clear_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertFalse(
            metadata["ec_keyword_name_source_prose_counted_as_predictive_evidence"]
        )

        structure_rows = {
            row["structure_id"]: row for row in probe["structure_rows"]
        }
        self.assertEqual(
            structure_rows["4C7L"]["current_countable_structural_screen_status"],
            "current_countable_structural_duplicate_signal",
        )
        self.assertEqual(
            structure_rows["4C7W"]["current_countable_structural_screen_status"],
            "no_current_countable_structural_duplicate_signal",
        )
        self.assertEqual(
            structure_rows["4C7L"]["nearest_current_countable_hit"][
                "current_selected_structure_key"
            ],
            "pdb:1IR3",
        )
        self.assertGreaterEqual(
            structure_rows["4C7L"]["nearest_current_countable_hit"][
                "max_pair_tm_score"
            ],
            0.7,
        )

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(packet["metadata"]["needs_new_extractor_or_structure_count"], 0)
        p31614 = next(row for row in packet["rows"] if row["accession"] == "P31614")
        self.assertEqual(
            p31614["terminal_decision"], "terminal_rejection_duplicate_or_leakage"
        )
        self.assertIsNone(p31614["exact_blocker_if_not_terminal"])
        self.assertTrue(
            p31614["duplicate_leakage_screen"]["terminal_rejection_claim_permitted"]
        )
        self.assertFalse(
            p31614["duplicate_leakage_screen"]["duplicate_clear_claim_permitted"]
        )
        self.assertEqual(
            p31614["catalytic_residue_triad_evidence"][
                "clean_triad_mapping_status"
            ],
            "not_resolved",
        )
        self.assertFalse(p31614["ready_for_label_import"])

        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["p31614_terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertEqual(
            benchmark["metrics"]["foldseek_full_current_status"],
            "completed_full_current_replacement_coordinate_duplicate_signal",
        )
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

    def test_plp_aminotransferase_deep_blocker_requires_extractor(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_packet_selection_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_blocker_packet_after_pdb_cofactor_probe_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_blocker_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_frozen_before_scoring"]
        )
        self.assertEqual(selection["metadata"]["selected_candidate_count"], 7)
        self.assertEqual(
            selection["metadata"]["excluded_exact_current_reference_accessions"],
            ["P12995", "P19938"],
        )
        self.assertEqual(
            selection["metadata"]["target_current_fingerprint_lane"],
            "plp_dependent_enzyme",
        )
        self.assertFalse(selection["metadata"]["ready_for_label_import"])
        self.assertFalse(selection["metadata"]["curated_label_registry_edited"])
        self.assertFalse(selection["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(selection["metadata"]["removal_allowed_set_true"])

        metadata = packet["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["candidate_selection_frozen_before_scoring"])
        self.assertEqual(metadata["selected_candidate_count"], 7)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(metadata["mechanism_match_review_ready_count"], 0)
        self.assertEqual(metadata["full_current_duplicate_screen_candidate_count"], 0)
        self.assertEqual(metadata["production_fingerprint_scored_candidate_count"], 0)
        self.assertEqual(
            metadata["plp_like_coordinate_probe_status_counts"],
            {
                "plp_like_coordinate_token_not_observed": 1,
                "plp_like_coordinate_token_observed": 6,
            },
        )
        self.assertFalse(metadata["pdb_coordinate_raw_files_written"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        for row in packet["rows"]:
            self.assertEqual(row["terminal_decision"], "needs_new_extractor_or_structure")
            self.assertIn(
                "source_free_plp_covalent_anchor_extractor_missing",
                row["counterevidence"],
            )
            self.assertEqual(
                row["current_geometry_retrieval_score_summary"]["geometry_score_status"],
                "not_scored_pending_source_free_plp_active_site_extractor",
            )
            self.assertFalse(
                row["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
            )
            self.assertEqual(
                row["duplicate_leakage_screen"]["current_countable_structural_screen_status"],
                "not_run_pending_source_free_plp_active_site_extractor",
            )
            self.assertFalse(row["duplicate_leakage_screen"]["duplicate_clear_established"])
            self.assertFalse(row["ready_for_label_import"])

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"needs_new_extractor_or_structure": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["current_geometry_retrieval_triage"]["scored_row_count"],
            0,
        )
        self.assertEqual(
            benchmark["metrics"]["deterministic_sequence_5mer_baseline"][
                "exact_current_reference_duplicate_count"
            ],
            0,
        )
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

    def test_plp_aminotransferase_source_free_anchor_packet_is_terminal(self) -> None:
        geometry = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_packet_source_free_active_site_geometry_scores_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_packet_targeted_current_plp_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_packet_post_source_free_anchor_modern_baseline_benchmark_20260521.json"
        )

        geometry_meta = geometry["metadata"]
        self.assertTrue(geometry_meta["review_only"])
        self.assertTrue(geometry_meta["candidate_selection_frozen_before_scoring"])
        self.assertEqual(geometry_meta["coordinate_sidecar_count"], 7)
        self.assertEqual(geometry_meta["source_free_active_site_ready_count"], 6)
        self.assertEqual(geometry_meta["target_lane_at_or_above_floor_count"], 6)
        self.assertEqual(geometry_meta["production_fingerprint_scored_candidate_count"], 0)
        self.assertFalse(geometry_meta["text_or_label_fields_used_for_score_any"])
        self.assertFalse(geometry_meta["ready_for_label_import"])
        self.assertFalse(geometry_meta["curated_label_registry_edited"])
        self.assertFalse(geometry_meta["fingerprint_registry_edited"])
        self.assertFalse(geometry_meta["removal_allowed_set_true"])
        self.assertEqual(
            geometry_meta["plp_active_site_extraction_status_counts"],
            {
                "plp_like_cofactor_absent": 1,
                "source_free_plp_active_site_ready": 6,
            },
        )
        q9nz45_geometry = {row["accession"]: row for row in geometry["rows"]}[
            "Q9NZ45"
        ]
        self.assertEqual(
            q9nz45_geometry["source_free_active_site_extraction"]["status"],
            "plp_like_cofactor_absent",
        )
        for row in geometry["rows"]:
            summary = row["current_geometry_retrieval_score_summary"]
            self.assertFalse(summary["text_or_label_fields_used_for_score"])
            if row["accession"] != "Q9NZ45":
                self.assertEqual(summary["top1_fingerprint_id"], "plp_dependent_enzyme")
                self.assertGreaterEqual(summary["target_lane_score"], 0.4115)

        screen_meta = screen["metadata"]
        self.assertTrue(screen_meta["review_only"])
        self.assertEqual(screen_meta["target_subset_count"], 30)
        self.assertEqual(screen_meta["high_tm_candidate_count"], 6)
        self.assertFalse(screen_meta["duplicate_clear_claim_permitted"])
        self.assertEqual(
            screen_meta["foldseek_query_run_status_counts"],
            {"completed": 6, "not_run": 1},
        )
        screen_rows = {row["accession"]: row for row in screen["rows"]}
        self.assertEqual(
            screen_rows["Q9NZ45"]["current_plp_structural_screen_status"],
            "not_run_source_free_plp_active_site_not_ready",
        )
        for accession, row in screen_rows.items():
            if accession == "Q9NZ45":
                continue
            self.assertEqual(
                row["current_plp_structural_screen_status"],
                "current_plp_structural_duplicate_signal",
            )
            self.assertGreaterEqual(
                row["nearest_current_plp_hit"]["max_pair_tm_score"],
                0.7,
            )

        packet_meta = packet["metadata"]
        self.assertTrue(packet_meta["review_only"])
        self.assertTrue(packet_meta["source_separation_enforced"])
        self.assertEqual(
            packet_meta["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 6,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(packet_meta["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet_meta["import_ready_candidate_count"], 0)
        self.assertFalse(packet_meta["ready_for_label_import"])
        self.assertFalse(packet_meta["curated_label_registry_edited"])
        self.assertFalse(packet_meta["fingerprint_registry_edited"])
        self.assertFalse(packet_meta["removal_allowed_set_true"])
        allowed = set(packet_meta["terminal_decision_vocabulary"])
        self.assertLessEqual({row["terminal_decision"] for row in packet["rows"]}, allowed)
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            packet_rows["Q9NZ45"]["terminal_decision"],
            "terminal_rejection_insufficient_evidence",
        )
        self.assertIn(
            "selected_pdb_lacks_source_free_plp_like_active_site_evidence",
            packet_rows["Q9NZ45"]["counterevidence"],
        )
        self.assertIsNotNone(
            packet_rows["Q9NZ45"]["exact_blocker_if_not_terminal_import_ready"]
        )
        for accession, row in packet_rows.items():
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(
                row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
            )
            self.assertFalse(
                row["predictive_evidence"][
                    "uniprot_prose_or_plp_annotation_counted_as_predictive_evidence"
                ]
            )
            if accession == "Q9NZ45":
                continue
            self.assertEqual(row["terminal_decision"], "terminal_rejection_duplicate_or_leakage")
            self.assertEqual(
                row["duplicate_leakage_screen"]["current_plp_structural_screen_status"],
                "current_plp_structural_duplicate_signal",
            )
            self.assertGreater(row["duplicate_leakage_screen"]["high_tm_hit_count"], 0)

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 6,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertTrue(
            benchmark["metrics"]["current_geometry_retrieval_triage"][
                "geometry_signal_added_beyond_ec_sequence_on_frozen_rows"
            ]
        )
        self.assertFalse(
            benchmark["metrics"]["foldseek_structural_sidecar"][
                "duplicate_clear_claim_supported"
            ]
        )
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

    def test_external_deep_terminal_rollup_post_plp_stays_review_only(self) -> None:
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_plp_20260521.json"
        )
        metadata = rollup["metadata"]
        synthesis = rollup["synthesis"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["deep_packet_count"], 6)
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["terminal_candidate_count"], 42)
        self.assertEqual(
            metadata["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 40,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(synthesis["non_needs_review_terminal_candidate_count"], 42)
        self.assertEqual(
            synthesis["aggregate_count_method"],
            "derived_from_terminal_decision_counts_to_avoid_stale_source_packet_summary_counts",
        )
        self.assertEqual(synthesis["mechanism_match_review_ready_count"], 1)
        self.assertEqual(synthesis["import_ready_candidate_count"], 0)
        self.assertEqual(synthesis["countable_label_candidate_count"], 0)
        self.assertEqual(
            synthesis["dominant_terminal_outcome"],
            "terminal_rejection_duplicate_or_leakage",
        )

        rows = {row["lane_id"]: row for row in rollup["rows"]}
        self.assertEqual(
            set(rows),
            {
                "metal_phosphatase",
                "serine_hydrolase",
                "flavin_dehydrogenase_reductase",
                "flavin_monooxygenase",
                "heme_peroxidase_oxidase",
                "plp_dependent_enzyme",
            },
        )
        self.assertEqual(
            rows["plp_dependent_enzyme"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 6,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(
            rows["heme_peroxidase_oxidase"]["mechanism_match_review_ready_count"],
            1,
        )
        self.assertEqual(
            rows["serine_hydrolase"]["derived_non_needs_review_terminal_count"],
            7,
        )
        consistency = rollup["source_packet_consistency_checks"]
        self.assertEqual(consistency["summary_count_mismatch_count"], 1)
        self.assertEqual(
            consistency["mismatch_findings"][0]["lane_id"],
            "serine_hydrolase",
        )
        self.assertEqual(
            consistency["aggregate_count_policy"],
            "derive_from_terminal_decision_counts_not_optional_packet_summary_fields",
        )
        self.assertTrue(all(row["source_separation_flag"] for row in rows.values()))
        self.assertTrue(
            all(row["import_ready_candidate_count"] == 0 for row in rows.values())
        )
        self.assertTrue(all(not row["ready_for_label_import"] for row in rows.values()))

        caveats = rollup["source_separation_and_baseline_caveats"]
        self.assertFalse(caveats["ec_keyword_protein_name_counted_as_predictive_evidence"])
        self.assertFalse(caveats["superiority_claim"])
        self.assertFalse(caveats["superiority_claim_permitted"])
        self.assertTrue(
            rollup["next_main_loop_guidance"]["do_not_start_broad_external_minicampaign"]
        )
        self.assertFalse(rollup["safety_and_scope"]["label_import_attempted"])
        self.assertFalse(rollup["safety_and_scope"]["production_fingerprint_added"])

    def test_default_label_factory_gate_check_does_not_authorize_import(self) -> None:
        gate_check = _load_json(ARTIFACTS / "v3_label_factory_gate_check.json")
        metadata = gate_check["metadata"]

        self.assertEqual(metadata["method"], "label_factory_gate_check")
        self.assertEqual(metadata["label_count"], 682)
        self.assertEqual(metadata["gate_count"], 17)
        self.assertLess(metadata["passed_gate_count"], metadata["gate_count"])
        self.assertFalse(metadata["automation_ready_for_next_label_batch"])
        self.assertEqual(
            metadata["review_only_import_safety_audit_total_new_countable_label_count"],
            0,
        )
        self.assertEqual(metadata["artifact_lineage"]["slice_id"], 500)
        self.assertEqual(
            metadata["artifact_lineage"]["method"],
            "label_factory_gate_cli_lineage_validation",
        )

    def test_heme_peroxidase_i2dby1_subchunk_screen_resolves_timeout(self) -> None:
        subchunk = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_i2dby1_full_current_subchunk_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_terminal_decision_packet_after_i2dby1_subchunk_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_deep_packet_post_i2dby1_subchunk_modern_baseline_benchmark_20260521.json"
        )

        metadata = subchunk["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["pair_cache_complete"])
        self.assertTrue(metadata["duplicate_clear_established"])
        self.assertEqual(metadata["expected_query_target_pair_count"], 672)
        self.assertEqual(metadata["unique_query_target_pair_count"], 672)
        self.assertEqual(metadata["current_countable_high_tm_hit_count"], 0)
        self.assertEqual(
            metadata["current_countable_structural_screen_status"],
            "no_current_countable_structural_duplicate_signal",
        )
        self.assertEqual(metadata["foldseek_chunk_run_status_counts"], {"completed": 14})
        self.assertLess(metadata["max_external_vs_current_countable_tm_score"], 0.7)
        self.assertEqual(metadata["text_or_label_fields_used_for_score_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 1)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        i2dby1 = next(row for row in packet["rows"] if row["accession"] == "I2DBY1")
        self.assertEqual(i2dby1["terminal_decision"], "mechanism_match_review_ready")
        self.assertIsNone(i2dby1["exact_blocker_if_not_terminal_import_ready"])
        self.assertTrue(i2dby1["duplicate_leakage_screen"]["duplicate_clear_established"])
        self.assertEqual(
            i2dby1["duplicate_leakage_screen"]["full_current_subchunk_screen"][
                "unique_query_target_pair_count"
            ],
            672,
        )
        self.assertEqual(
            i2dby1["duplicate_leakage_screen"]["evidence_role"],
            "import_gate_evidence_not_predictive_mechanism_evidence",
        )
        self.assertFalse(i2dby1["ready_for_label_import"])

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["i2dby1_full_current_subchunk_duplicate_screen"][
                "current_countable_high_tm_hit_count"
            ],
            0,
        )
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 6,
            },
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_flavin_monooxygenase_deep_packet_freezes_and_screens_subset(self) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_flavin_monooxygenase_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_coordinate_materialization_20260521.json"
        )
        rescue = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_targeted_current_fmo_rescue_screen_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_structure_mapping_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_terminal_decision_packet_after_structure_mapping_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_post_structure_mapping_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"O94851", "O15229", "Q7RTP6", "P25535", "O88867", "H3JQW0", "Q6F4M8"},
        )
        self.assertTrue(
            all(
                row["sequence_baseline_signal"] != "exact_current_reference_duplicate"
                for row in selection["rows"]
            )
        )
        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(rescue["metadata"]["target_subset_fingerprint_id"], "flavin_monooxygenase")
        self.assertEqual(rescue["metadata"]["target_subset_count"], 2)
        self.assertEqual(rescue["metadata"]["high_tm_candidate_count"], 3)
        self.assertFalse(rescue["metadata"]["duplicate_clear_claim_permitted"])
        self.assertTrue(mapping["metadata"]["review_only"])
        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 7)
        self.assertEqual(mapping["metadata"]["status_counts"], {"ok": 7})
        self.assertEqual(mapping["metadata"]["source_free_geometry_scored_count"], 0)
        self.assertFalse(mapping["metadata"]["ready_for_label_import"])
        self.assertFalse(mapping["metadata"]["curated_label_registry_edited"])
        self.assertFalse(mapping["metadata"]["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["resolved_residue_count"] > 0
                and row["ready_for_geometry_scoring_after_review"]
                and row["source_context_not_counted_as_predictive_score"]
                for row in mapping["entries"]
            )
        )

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 4,
                "terminal_rejection_duplicate_or_leakage": 3,
            },
        )
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        self.assertEqual(packet["metadata"]["structure_mapped_candidate_count"], 7)
        duplicate_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
        ]
        self.assertEqual(len(duplicate_rows), 3)
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in duplicate_rows
            )
        )
        blocker_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "needs_new_extractor_or_structure"
        ]
        self.assertEqual(len(blocker_rows), 4)
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal"]
                == "run source-free FMO geometry scoring from mapped flavin/cofactor features and complete full current-countable duplicate/leakage screening"
                for row in blocker_rows
            )
        )
        self.assertTrue(
            all(
                row["structure_mapping_evidence"][
                    "source_free_coordinate_mapping_status"
                ]
                == "ok"
                for row in blocker_rows
            )
        )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(benchmark["metrics"]["mapped_candidate_count"], 7)
        self.assertEqual(benchmark["metrics"]["source_free_geometry_scored_count"], 0)
        self.assertEqual(
            benchmark["metrics"]["targeted_current_fingerprint_rescue_high_tm_candidate_count"],
            3,
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

    def test_latest_epk_lane_regression_synthesis_stays_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_latest_lane_regression_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        conclusion = synthesis["synthesis_conclusion"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["fresh_remote_branch_outputs_integrated"])
        self.assertTrue(metadata["captures_5uj7_biological_assembly_residual"])
        self.assertEqual(metadata["lane_count"], 5)
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
            "epk_remains_review_only_and_not_production_ready",
        )
        self.assertEqual(conclusion["production_activation_decision"], "no_go")
        self.assertEqual(
            conclusion["terminal_main_loop_decision"],
            "do_not_resume_epk_as_default_main_loop_task",
        )
        self.assertFalse(conclusion["decision_to_start_now"])

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
            lanes["epk_false_positive_hunter"]["regression_rows_emitted"], 343
        )
        self.assertIn(
            "5UJ7:biological_assembly_1",
            lanes["epk_false_positive_hunter"]["latest_evidence"],
        )
        self.assertIn(
            "eight entries",
            lanes["epk_policy_harness"]["latest_evidence"],
        )
        self.assertIn(
            "mixed 9UUR/9UUX/9UW4 and 3TM0/6NOO collisions",
            lanes["epk_substrate_role_identity"]["latest_evidence"],
        )
        self.assertTrue(
            all(not row["production_claim_allowed"] for row in lanes.values())
        )

    def test_late_epk_lane_decision_synthesis_preserves_no_go(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_late_lane_decision_synthesis_20260521.json"
        )
        metadata = synthesis["metadata"]
        decision = synthesis["integrated_decision"]
        lanes = {row["lane_id"]: row for row in synthesis["lane_summaries"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["production_claim_allowed"])
        self.assertFalse(metadata["labels_or_fingerprints_changed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_migration_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertFalse(metadata["ePK_main_loop_resume_recommended"])
        self.assertEqual(
            metadata["decision_change"],
            "ePK_no_go_preserved_with_sharper_harness_and_source_free_modality_boundaries",
        )
        self.assertEqual(decision["production_readiness"], "no_go_review_only")
        self.assertEqual(
            decision["main_loop_boundary"],
            "Do not resume ePK as default main-loop task; continue visible non-ePK external terminal decision packets.",
        )
        self.assertIn(
            "5UJ7:biological_assembly_1 remains the pinned context-v4-only biological-assembly split residual",
            decision["pinned_counterexamples_or_controls"],
        )
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
        self.assertTrue(
            all(not row["production_claim_allowed"] for row in lanes.values())
        )
        self.assertIn(
            "343-row regression gate",
            lanes["epk_false_positive_hunter"]["decision_relevance"],
        )
        self.assertIn(
            "119-row runtime row oracle",
            lanes["epk_sibling_controls"]["decision_relevance"],
        )
        self.assertIn(
            "product_state and split_state",
            lanes["epk_policy_harness"]["decision_relevance"],
        )
        self.assertIn(
            "blocker_not_cleared_biology_ambiguity",
            lanes["epk_substrate_role_identity"]["decision_relevance"],
        )

    def test_flavin_monooxygenase_geometry_full_current_screen_terminals(
        self,
    ) -> None:
        geometry = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_geometry_scores_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_full_current_subchunk_screen_20260521.json"
        )
        timeout_probe = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_timeout_chunk000_rescue_probe_20260521.json"
        )
        size2_probe = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_timeout_chunk000_size2_rescue_probe_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_terminal_decision_packet_after_geometry_and_full_current_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_post_geometry_full_current_modern_baseline_benchmark_20260521.json"
        )

        self.assertTrue(geometry["metadata"]["review_only"])
        self.assertEqual(geometry["metadata"]["candidate_count"], 7)
        self.assertEqual(geometry["metadata"]["source_free_geometry_scored_count"], 7)
        self.assertEqual(geometry["metadata"]["target_lane_at_or_above_floor_count"], 1)
        self.assertEqual(geometry["metadata"]["top1_target_lane_count"], 0)
        self.assertEqual(geometry["metadata"]["text_or_label_fields_used_for_score_count"], 0)
        self.assertFalse(geometry["metadata"]["ready_for_label_import"])
        self.assertFalse(geometry["metadata"]["curated_label_registry_edited"])
        self.assertFalse(geometry["metadata"]["fingerprint_registry_edited"])
        self.assertTrue(
            all(
                row["status"] == "ok"
                and row["target_lane_summary"]["geometry_score_status"]
                == "scored_all_current_fingerprints"
                and not row["text_or_label_fields_used_for_score"]
                and row["target_lane_summary"]["top1_fingerprint_id"]
                == "flavin_dehydrogenase_reductase"
                for row in geometry["rows"]
            )
        )

        screen_metadata = screen["metadata"]
        self.assertTrue(screen_metadata["review_only"])
        self.assertEqual(screen_metadata["candidate_count"], 4)
        self.assertEqual(
            screen_metadata["current_countable_structural_screen_status_counts"],
            {
                "current_countable_structural_duplicate_signal": 2,
                "current_countable_structural_screen_incomplete": 2,
            },
        )
        self.assertEqual(screen_metadata["foldseek_chunk_run_status_counts"], {"completed": 28, "foldseek_run_timeout": 2})
        self.assertFalse(screen_metadata["pair_cache_complete"])
        self.assertEqual(screen_metadata["query_target_pair_coverage"], 0.5)
        self.assertEqual(screen_metadata["duplicate_clear_candidate_count"], 0)
        self.assertFalse(screen_metadata["duplicate_clear_claim_permitted"])
        self.assertEqual(screen_metadata["high_tm_candidate_count"], 2)
        self.assertEqual(
            screen_metadata["duplicate_leakage_evidence_role"],
            "import_gate_evidence_not_predictive_mechanism_evidence",
        )
        self.assertFalse(screen_metadata["ready_for_label_import"])
        self.assertFalse(screen_metadata["curated_label_registry_edited"])
        self.assertFalse(screen_metadata["fingerprint_registry_edited"])
        screen_rows = {row["accession"]: row for row in screen["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in screen_rows.items()
                if row["current_countable_structural_screen_status"]
                == "current_countable_structural_screen_incomplete"
            },
            {"O94851", "Q7RTP6"},
        )
        self.assertEqual(
            {
                accession
                for accession, row in screen_rows.items()
                if row["current_countable_structural_screen_status"]
                == "current_countable_structural_duplicate_signal"
            },
            {"H3JQW0", "Q6F4M8"},
        )

        probe_metadata = timeout_probe["metadata"]
        self.assertTrue(probe_metadata["review_only"])
        self.assertEqual(probe_metadata["candidate_count"], 2)
        self.assertEqual(probe_metadata["probe_subchunk_size"], 6)
        self.assertEqual(probe_metadata["expected_subchunk_count_per_candidate"], 8)
        self.assertEqual(
            probe_metadata["foldseek_chunk_run_status_counts"],
            {"completed": 12, "foldseek_run_timeout": 4},
        )
        self.assertEqual(probe_metadata["chunk000_complete_candidate_count"], 0)
        self.assertEqual(probe_metadata["chunk000_timeout_persists_candidate_count"], 2)
        self.assertEqual(probe_metadata["high_tm_candidate_count"], 0)
        self.assertFalse(probe_metadata["duplicate_clear_claim_permitted"])
        self.assertFalse(probe_metadata["ready_for_label_import"])
        self.assertFalse(probe_metadata["curated_label_registry_edited"])
        self.assertFalse(probe_metadata["fingerprint_registry_edited"])
        probe_rows = {row["accession"]: row for row in timeout_probe["rows"]}
        self.assertEqual(probe_rows["O94851"]["completed_subchunk_count"], 7)
        self.assertEqual(probe_rows["O94851"]["timeout_subchunk_count"], 1)
        self.assertEqual(probe_rows["Q7RTP6"]["completed_subchunk_count"], 5)
        self.assertEqual(probe_rows["Q7RTP6"]["timeout_subchunk_count"], 3)
        self.assertTrue(
            all(row["decision_impact"] == "chunk000_timeout_persists" for row in probe_rows.values())
        )
        self.assertTrue(
            all(row["high_tm_hit_count"] == 0 for row in probe_rows.values())
        )

        size2_metadata = size2_probe["metadata"]
        self.assertTrue(size2_metadata["review_only"])
        self.assertEqual(size2_metadata["candidate_count"], 2)
        self.assertEqual(size2_metadata["probe_retry_subchunk_size"], 2)
        self.assertEqual(
            size2_metadata["foldseek_chunk_run_status_counts"],
            {"completed": 11, "foldseek_run_timeout": 1},
        )
        self.assertEqual(size2_metadata["timeout_parent_subchunks_resolved_candidate_count"], 1)
        self.assertEqual(size2_metadata["timeout_parent_subchunks_persist_candidate_count"], 1)
        self.assertEqual(size2_metadata["high_tm_candidate_count"], 0)
        self.assertFalse(size2_metadata["duplicate_clear_claim_permitted"])
        self.assertFalse(size2_metadata["ready_for_label_import"])
        self.assertFalse(size2_metadata["curated_label_registry_edited"])
        self.assertFalse(size2_metadata["fingerprint_registry_edited"])
        size2_rows = {row["accession"]: row for row in size2_probe["rows"]}
        self.assertEqual(
            size2_rows["O94851"]["decision_impact"],
            "timeout_parent_subchunks_resolved",
        )
        self.assertEqual(size2_rows["O94851"]["timeout_retry_subchunk_count"], 0)
        self.assertEqual(
            size2_rows["Q7RTP6"]["decision_impact"],
            "timeout_parent_subchunks_persist",
        )
        self.assertEqual(size2_rows["Q7RTP6"]["timeout_retry_subchunk_count"], 1)
        self.assertTrue(
            all(row["high_tm_hit_count"] == 0 for row in size2_rows.values())
        )

        packet_metadata = packet["metadata"]
        self.assertTrue(packet_metadata["review_only"])
        self.assertTrue(packet_metadata["source_separation_enforced"])
        self.assertEqual(packet_metadata["source_free_geometry_scored_count"], 7)
        self.assertEqual(
            packet_metadata["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )
        self.assertEqual(packet_metadata["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet_metadata["import_ready_candidate_count"], 0)
        self.assertFalse(packet_metadata["ready_for_label_import"])
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in packet_rows.items()
                if row["terminal_decision"] == "needs_new_extractor_or_structure"
            },
            {"O94851", "Q7RTP6"},
        )
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal"]
                == "complete full current-countable duplicate/leakage screening after subchunk timeout or pair-cache gap"
                for accession, row in packet_rows.items()
                if accession in {"O94851", "Q7RTP6"}
            )
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for row in packet_rows.values()
            )
        )
        self.assertTrue(
            all(
                not row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
                and not row["ready_for_label_import"]
                for row in packet_rows.values()
            )
        )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["foldseek_sidecar_status"],
            "partial_full_current_countable_subchunk_screen_two_rows_completed_two_rows_timed_out",
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(benchmark["metrics"]["geometry_superiority_claim"], "not_made")
        self.assertFalse(benchmark["metrics"]["full_current_pair_cache_complete"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )

    def test_flavin_monooxygenase_chunk002_rescue_keeps_blocker_precise(
        self,
    ) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_chunk000_chunk002_rescue_and_remaining_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk002_rescue_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_chunk002_rescue_modern_baseline_benchmark_20260521.json"
        )

        metadata = screen["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["source_separation_enforced"])
        self.assertTrue(metadata["q7rtp6_chunk000_remaining_retry_resolved"])
        self.assertEqual(metadata["chunk001_complete_candidate_count"], 2)
        self.assertEqual(metadata["chunk002_complete_candidate_count"], 2)
        self.assertEqual(metadata["new_high_tm_hit_count"], 0)
        self.assertEqual(metadata["new_completed_query_target_pair_count"], 288)
        self.assertFalse(metadata["duplicate_clear_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        rows = {row["accession"]: row for row in screen["rows"]}
        self.assertEqual(set(rows), {"O94851", "Q7RTP6"})
        self.assertTrue(
            all(
                row["chunk000_status_after_followup"]
                == "complete_no_high_tm_signal"
                and row["chunk001_status_after_followup"]
                == "complete_no_high_tm_signal"
                and row["chunk002_status_after_followup"]
                == "complete_no_high_tm_signal"
                and row["chunks003_013_status_after_followup"] == "not_run"
                and row["new_high_tm_hit_count"] == 0
                for row in rows.values()
            )
        )

        packet_metadata = packet["metadata"]
        self.assertEqual(
            packet_metadata["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )
        self.assertEqual(packet_metadata["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet_metadata["import_ready_candidate_count"], 0)
        self.assertFalse(packet_metadata["ready_for_label_import"])
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertTrue(
            all(
                packet_rows[accession]["terminal_decision"]
                == "needs_new_extractor_or_structure"
                and packet_rows[accession]["duplicate_leakage_screen"][
                    "followup_chunk001_status"
                ]
                == "complete_no_high_tm_signal"
                and packet_rows[accession]["duplicate_leakage_screen"][
                    "followup_chunk002_status"
                ]
                == "complete_no_high_tm_signal"
                and not packet_rows[accession]["duplicate_leakage_screen"][
                    "duplicate_clear_established"
                ]
                and packet_rows[accession]["duplicate_leakage_screen"][
                    "evidence_role"
                ]
                == "import_gate_evidence_not_predictive_mechanism_evidence"
                for accession in {"O94851", "Q7RTP6"}
            )
        )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(benchmark["metrics"]["new_high_tm_hit_count"], 0)
        self.assertEqual(
            benchmark["metrics"]["foldseek_sidecar_status"],
            "chunks000_002_resolved_for_O94851_Q7RTP6_no_high_tm_signal_chunks003_013_unrun",
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(benchmark["metrics"]["geometry_superiority_claim"], "not_made")
        self.assertFalse(benchmark["metrics"]["full_current_pair_cache_complete"])

    def test_flavin_monooxygenase_chunk004_followup_closes_remaining_rows(
        self,
    ) -> None:
        chunk3 = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_chunk003_followup_screen_20260521.json"
        )
        chunk4 = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_chunk004_followup_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk004_followup_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_monooxygenase_deep_packet_chunk004_followup_modern_baseline_benchmark_20260521.json"
        )

        chunk3_metadata = chunk3["metadata"]
        self.assertTrue(chunk3_metadata["review_only"])
        self.assertTrue(chunk3_metadata["source_separation_enforced"])
        self.assertEqual(chunk3_metadata["foldseek_chunk_run_status_counts"], {"completed": 16})
        self.assertEqual(chunk3_metadata["terminal_duplicate_signal_candidate_count"], 2)
        self.assertEqual(chunk3_metadata["new_high_tm_hit_count"], 2)
        self.assertEqual(chunk3_metadata["max_completed_followup_tm_score"], 0.725)
        self.assertEqual(
            chunk3_metadata["max_pair_tm_score_definition"],
            "max(qtmscore, ttmscore, alntmscore); exact TM-score output retained separately",
        )
        self.assertFalse(chunk3_metadata["duplicate_clear_claim_permitted"])
        self.assertTrue(chunk3_metadata["terminal_rejection_claim_permitted_for_high_tm_rows"])
        self.assertFalse(chunk3_metadata["ready_for_label_import"])
        self.assertFalse(chunk3_metadata["curated_label_registry_edited"])
        self.assertFalse(chunk3_metadata["fingerprint_registry_edited"])
        self.assertFalse(chunk3_metadata["removal_allowed_set_true"])
        chunk3_rows = {row["accession"]: row for row in chunk3["rows"]}
        self.assertEqual(set(chunk3_rows), {"O94851", "Q7RTP6"})
        for row in chunk3_rows.values():
            self.assertEqual(row["decision_impact"], "terminal_duplicate_leakage_signal_found")
            self.assertEqual(row["chunk003_status_after_followup"], "high_tm_signal_found")
            self.assertEqual(row["chunks004_013_status_after_followup"], "not_run_not_needed_for_terminal_duplicate_rejection")
            self.assertIsNone(row["exact_remaining_blocker"])
            self.assertEqual(row["new_high_tm_hit_count"], 1)
            self.assertGreaterEqual(row["max_pair_tm_score"], 0.7)
            self.assertEqual(row["top_current_countable_hits"][0]["target_structure_id"], "1DOC")
            self.assertEqual(row["top_current_countable_hits"][0]["target_entry_ids"], ["m_csa:131"])
            self.assertEqual(
                row["top_current_countable_hits"][0]["target_fingerprint_ids"],
                ["flavin_monooxygenase"],
            )

        chunk4_metadata = chunk4["metadata"]
        self.assertTrue(chunk4_metadata["review_only"])
        self.assertEqual(
            chunk4_metadata["foldseek_chunk_run_status_counts"],
            {"completed": 10, "foldseek_run_timeout": 6},
        )
        self.assertEqual(chunk4_metadata["terminal_duplicate_signal_candidate_count"], 2)
        self.assertEqual(chunk4_metadata["new_high_tm_hit_count"], 2)
        self.assertFalse(chunk4_metadata["duplicate_clear_claim_permitted"])
        self.assertTrue(chunk4_metadata["terminal_rejection_claim_permitted_for_high_tm_rows"])
        chunk4_rows = {row["accession"]: row for row in chunk4["rows"]}
        for row in chunk4_rows.values():
            self.assertEqual(row["decision_impact"], "terminal_duplicate_leakage_signal_found")
            self.assertEqual(row["chunk004_status_after_followup"], "high_tm_signal_found")
            self.assertEqual(row["chunks005_013_status_after_followup"], "not_run_not_needed_for_terminal_duplicate_rejection")
            self.assertGreaterEqual(row["max_pair_tm_score"], 0.7)
            self.assertEqual(row["top_current_countable_hits"][0]["target_structure_id"], "1EHK")

        packet_metadata = packet["metadata"]
        self.assertTrue(packet_metadata["review_only"])
        self.assertTrue(packet_metadata["source_separation_enforced"])
        self.assertEqual(
            packet_metadata["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(packet_metadata["terminal_rejection_duplicate_or_leakage_count"], 7)
        self.assertEqual(packet_metadata["mechanism_match_review_ready_count"], 0)
        self.assertEqual(packet_metadata["import_ready_candidate_count"], 0)
        self.assertFalse(packet_metadata["ready_for_label_import"])
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertTrue(
            all(
                row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
                for row in packet_rows.values()
            )
        )
        for accession in {"O94851", "Q7RTP6"}:
            row = packet_rows[accession]
            screen = row["duplicate_leakage_screen"]
            self.assertIsNone(row["exact_blocker_if_not_terminal"])
            self.assertEqual(screen["current_countable_structural_screen_status"], "current_countable_structural_duplicate_signal")
            self.assertEqual(screen["evidence_role"], "import_gate_evidence_not_predictive_mechanism_evidence")
            self.assertFalse(screen["duplicate_clear_established"])
            self.assertFalse(screen["pair_cache_complete"])
            self.assertFalse(screen["pair_cache_complete_required_for_terminal_rejection"])
            self.assertEqual(screen["followup_chunk003_status"], "high_tm_signal_found")
            self.assertEqual(screen["followup_chunks005_013_status"], "not_run_not_needed_for_terminal_duplicate_rejection")
            self.assertGreaterEqual(screen["primary_terminal_hit"]["max_pair_tm_score"], 0.7)
            self.assertEqual(screen["primary_terminal_hit"]["target_structure_id"], "1DOC")
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(
                row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
            )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )
        self.assertEqual(benchmark["metrics"]["geometry_superiority_claim"], "not_made")
        self.assertFalse(benchmark["metrics"]["full_current_pair_cache_complete"])
        self.assertFalse(
            benchmark["metrics"]["full_current_pair_cache_complete_required_for_terminal_rejection"]
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

    def test_flavin_dehydrogenase_second_packet_targeted_fdr_screen_rejects_leakage(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_coordinate_materialization_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_geometry_scores_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_targeted_current_fdr_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_terminal_decision_packet_after_targeted_fdr_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_second_deep_packet_after_targeted_fdr_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_flavin_dehydrogenase_targeted_screen_20260521.json"
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"P77258", "P41407", "Q8LAH7", "P0AEN1", "Q07923", "P21375", "Q9FUP0"},
        )
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            selection["metadata"]["target_current_fingerprint_lane"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertFalse(selection["metadata"]["ready_for_label_import"])

        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
        self.assertTrue(
            all(row["coordinate_digest_sha256"] for row in coordinates["rows"])
        )
        self.assertEqual(mapping["metadata"]["feature_fetch_failure_count"], 0)
        self.assertEqual(mapping["metadata"]["mapped_candidate_count"], 5)
        self.assertTrue(
            all(
                entry["source_context_not_counted_as_predictive_score"]
                for entry in mapping["entries"]
            )
        )

        self.assertEqual(scores["metadata"]["text_or_label_fields_used_for_score_count"], 0)
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 0)
        self.assertFalse(scores["metadata"]["ready_for_label_import"])

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertTrue(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["current_fdr_target_coordinate_count"], 49)
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 343)
        self.assertEqual(screen["metadata"]["expected_query_target_pair_count"], 343)
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 7)
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(
            screen["metadata"]["targeted_current_fdr_screen_status_counts"],
            {"current_fdr_structural_duplicate_signal": 7},
        )
        self.assertTrue(
            all(
                row["targeted_current_fdr_high_tm_hit_count"] >= 1
                for row in screen["rows"]
            )
        )

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        self.assertTrue(
            all(
                row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "targeted_import_gate_duplicate_leakage_evidence_not_predictive_mechanism_evidence"
                for row in packet["rows"]
            )
        )
        self.assertTrue(
            all(
                not row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
                for row in packet["rows"]
            )
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {"terminal_rejection_duplicate_or_leakage": 7},
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

        self.assertEqual(rollup["metadata"]["candidate_count"], 64)
        self.assertEqual(rollup["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(rollup["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 3,
                "terminal_rejection_duplicate_or_leakage": 58,
                "terminal_rejection_insufficient_evidence": 3,
            },
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

    def test_heme_peroxidase_second_packet_targeted_heme_screen_records_terminals_and_blockers(
        self,
    ) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_heme_peroxidase_second_deep_packet_selection_20260521.json"
        )
        coordinates = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_coordinate_materialization_20260521.json"
        )
        mapping = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_structure_mapping_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_geometry_scores_20260521.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_targeted_current_heme_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_terminal_decision_packet_after_targeted_heme_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_after_targeted_heme_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_heme_peroxidase_targeted_screen_20260521.json"
        )

        self.assertTrue(selection["metadata"]["review_only"])
        self.assertTrue(
            selection["metadata"]["candidate_selection_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["candidate_count"], 7)
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"P11678", "P39597", "P31545", "Q39034", "K7N5M8", "Q47KB1", "P49012"},
        )

        self.assertEqual(
            coordinates["metadata"]["coordinate_materialized_or_reused_count"], 7
        )
        self.assertEqual(coordinates["metadata"]["fetch_failure_count"], 0)
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

        self.assertTrue(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["current_heme_target_coordinate_count"], 20)
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 140)
        self.assertEqual(screen["metadata"]["expected_query_target_pair_count"], 140)
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 4)
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(
            screen["metadata"]["targeted_current_heme_screen_status_counts"],
            {
                "current_heme_structural_duplicate_signal": 4,
                "no_current_heme_structural_duplicate_signal": 3,
            },
        )

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 3,
                "terminal_rejection_duplicate_or_leakage": 4,
            },
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 4)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        duplicate_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
        ]
        blocker_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "needs_new_extractor_or_structure"
        ]
        self.assertEqual(len(duplicate_rows), 4)
        self.assertEqual(len(blocker_rows), 3)
        self.assertTrue(
            all(
                row["duplicate_leakage_screen"]["evidence_role"]
                == "targeted_import_gate_duplicate_leakage_evidence_not_predictive_mechanism_evidence"
                for row in packet["rows"]
            )
        )
        self.assertEqual(
            {
                row["exact_blocker_if_not_terminal_import_ready"]
                for row in blocker_rows
            },
            {"full_current_countable_duplicate_screen_missing_after_targeted_current_heme_screen"},
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metrics"]["superiority_claim"])
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 3,
                "terminal_rejection_duplicate_or_leakage": 4,
            },
        )
        self.assertEqual(
            benchmark["metrics"]["esm_sidecar_status"],
            "not_available_for_this_deep_packet",
        )

        self.assertEqual(rollup["metadata"]["candidate_count"], 71)
        self.assertEqual(rollup["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(rollup["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(rollup["metadata"]["exact_blocker_candidate_count"], 3)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 3,
                "needs_new_extractor_or_structure": 3,
                "terminal_rejection_duplicate_or_leakage": 62,
                "terminal_rejection_insufficient_evidence": 3,
            },
        )

    def test_heme_peroxidase_second_full_current_screen_closes_exact_blockers(
        self,
    ) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_full_current_countable_screen_20260521.json"
        )
        independent_rerun = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_full_current_countable_duplicate_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_terminal_decision_packet_after_full_current_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_second_deep_packet_after_full_current_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_heme_full_current_screen_20260521.json"
        )
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_second_heme_full_current_screen_20260521.json"
        )

        self.assertTrue(screen["metadata"]["review_only"])
        self.assertTrue(screen["metadata"]["pair_cache_complete"])
        self.assertEqual(screen["metadata"]["candidate_count"], 3)
        self.assertEqual(screen["metadata"]["current_countable_target_count"], 672)
        self.assertEqual(screen["metadata"]["expected_query_target_pair_count"], 2016)
        self.assertEqual(screen["metadata"]["unique_query_target_pair_count"], 2016)
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 1)
        self.assertEqual(
            screen["metadata"]["current_countable_structural_screen_status_counts"],
            {
                "current_countable_structural_duplicate_signal": 1,
                "no_current_countable_structural_duplicate_signal": 2,
            },
        )
        rows = {row["accession"]: row for row in screen["rows"]}
        self.assertEqual(set(rows), {"P39597", "P31545", "K7N5M8"})
        self.assertTrue(rows["P39597"]["duplicate_clear_established"])
        self.assertTrue(rows["K7N5M8"]["duplicate_clear_established"])
        self.assertFalse(rows["P31545"]["duplicate_clear_established"])
        self.assertEqual(rows["P31545"]["current_countable_high_tm_hit_count"], 1)
        self.assertEqual(
            rows["P31545"]["nearest_current_countable_hit"]["target_structure_key"],
            "pdb:1IR3",
        )
        self.assertGreaterEqual(
            rows["P31545"]["nearest_current_countable_hit"]["max_pair_tm_score"],
            0.7,
        )
        self.assertEqual(independent_rerun["metadata"]["candidate_count"], 3)
        self.assertEqual(
            independent_rerun["metadata"]["expected_query_target_pair_count"], 2016
        )
        self.assertEqual(
            independent_rerun["metadata"][
                "current_countable_structural_screen_status_counts"
            ],
            screen["metadata"]["current_countable_structural_screen_status_counts"],
        )
        self.assertEqual(
            independent_rerun["metadata"]["candidate_with_high_tm_count"], 1
        )
        self.assertEqual(
            independent_rerun["metadata"]["candidate_duplicate_clear_count"], 2
        )
        rerun_rows = {row["accession"]: row for row in independent_rerun["rows"]}
        self.assertFalse(rerun_rows["P31545"]["duplicate_clear_established"])
        self.assertTrue(rerun_rows["P39597"]["duplicate_clear_established"])
        self.assertTrue(rerun_rows["K7N5M8"]["duplicate_clear_established"])

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 2,
                "terminal_rejection_duplicate_or_leakage": 5,
            },
        )
        packet_rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in packet_rows.items()
                if row["terminal_decision"] == "mechanism_match_review_ready"
            },
            {"P39597", "K7N5M8"},
        )
        self.assertEqual(
            packet_rows["P31545"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal_import_ready"] is None
                for row in packet["rows"]
            )
        )
        self.assertFalse(packet["metadata"]["ready_for_label_import"])

        self.assertEqual(
            benchmark["metrics"]["full_current_countable_unique_query_target_pair_count"],
            2016,
        )
        self.assertEqual(
            benchmark["metrics"]["full_current_countable_high_tm_candidate_count"],
            1,
        )
        self.assertEqual(
            benchmark["metrics"]["full_current_countable_duplicate_clear_candidate_count"],
            2,
        )
        self.assertFalse(benchmark["metrics"]["superiority_claim"])

        self.assertEqual(rollup["metadata"]["candidate_count"], 71)
        self.assertEqual(rollup["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertEqual(rollup["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 5,
                "terminal_rejection_duplicate_or_leakage": 63,
                "terminal_rejection_insufficient_evidence": 3,
            },
        )

        self.assertTrue(readiness["metadata"]["review_only"])
        self.assertEqual(readiness["metadata"]["candidate_count"], 71)
        self.assertEqual(readiness["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertTrue(all(readiness["invariant_checks"].values()))
        self.assertNotIn(
            "three_second_heme_targeted_clear_rows_need_full_current_countable_duplicate_screen",
            readiness["import_gate_readiness"]["blockers"],
        )
        self.assertTrue(
            readiness["invariant_checks"][
                "second_heme_full_current_screen_closed_exact_duplicate_blockers"
            ]
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

        self.assertEqual(len(labels), 702)
        self.assertEqual(by_type, {"out_of_scope": 472, "seed_fingerprint": 230})

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

        imported_clean9 = {
            "m_csa:599": "ser_his_acid_hydrolase",
            "m_csa:623": "metal_dependent_hydrolase",
            "m_csa:636": "metal_dependent_hydrolase",
            "m_csa:706": "metal_dependent_hydrolase",
            "m_csa:812": "metal_dependent_hydrolase",
            "m_csa:865": "plp_dependent_enzyme",
            "m_csa:892": "flavin_dehydrogenase_reductase",
            "m_csa:917": "metal_dependent_hydrolase",
            "m_csa:998": "metal_dependent_hydrolase",
        }
        for entry_id, fingerprint_id in imported_clean9.items():
            label = labels_by_entry[entry_id]
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertEqual(label["fingerprint_id"], fingerprint_id)
            self.assertEqual(label["tier"], "silver")
            self.assertEqual(label["review_status"], "expert_reviewed")

        imported_post_clean9 = {
            "m_csa:577": ("metal_dependent_hydrolase", "bronze", "automation_curated"),
            "m_csa:641": ("metal_dependent_hydrolase", "bronze", "automation_curated"),
            "m_csa:771": ("ser_his_acid_hydrolase", "silver", "expert_reviewed"),
            "m_csa:897": ("metal_dependent_hydrolase", "bronze", "automation_curated"),
        }
        for entry_id, (fingerprint_id, tier, review_status) in imported_post_clean9.items():
            label = labels_by_entry[entry_id]
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertEqual(label["fingerprint_id"], fingerprint_id)
            self.assertEqual(label["tier"], tier)
            self.assertEqual(label["review_status"], review_status)

    def test_post_clean9_followup_summary_pins_exact_import_boundaries(
        self,
    ) -> None:
        summary = _load_json(
            ARTIFACTS / "v3_mcsa_positive_post_clean9_followup_import_summary_20260524.json"
        )
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_remaining_13_decision_matrix_post_import_20260524.json"
        )
        stress = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_nucleotide_product_counterevidence_rule_stress_panel_20260524.json"
        )

        metadata = summary["metadata"]
        self.assertEqual(metadata["baseline_clean9_label_count"], 691)
        self.assertEqual(metadata["post_holo_label_count"], 694)
        self.assertEqual(metadata["final_label_count"], 695)
        self.assertEqual(metadata["m_csa_label_count"], 692)
        self.assertEqual(metadata["external_seed_fingerprint_import_count"], 0)
        self.assertEqual(
            metadata["external_out_of_scope_entry_ids"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        batches = {batch["batch_id"]: batch for batch in summary["import_batches"]}
        self.assertEqual(
            batches["holo_override_accept3"]["accepted_new_label_entry_ids"],
            ["m_csa:577", "m_csa:641", "m_csa:897"],
        )
        self.assertEqual(
            batches["m_csa771_2d0d_vivek"]["accepted_new_label_entry_ids"],
            ["m_csa:771"],
        )
        for batch in batches.values():
            self.assertTrue(batch["factory_gate_ready"])
            self.assertTrue(batch["batch_accepted_for_counting"])
            self.assertEqual(batch["gate_passed_count"], 21)
            self.assertEqual(batch["gate_count"], 21)
            self.assertEqual(
                batch["accepted_new_label_count"],
                len(batch["accepted_new_label_entry_ids"]),
            )

        stress_metadata = stress["metadata"]
        self.assertFalse(stress_metadata["production_rule_activated"])
        self.assertFalse(stress_metadata["production_scoring_changed"])
        self.assertFalse(stress_metadata["rule_promotion_ready"])
        self.assertEqual(stress_metadata["product_context_exception_candidate_count"], 2)
        self.assertEqual(stress_metadata["retain_counterevidence_control_count"], 33)
        self.assertIn(
            "production_rule_not_implemented_or_unit_tested_in_this_run",
            stress_metadata["rule_promotion_blockers"],
        )

        statuses = {row["entry_id"]: row for row in matrix["rows"]}
        for entry_id in ("m_csa:577", "m_csa:641", "m_csa:771", "m_csa:897"):
            self.assertEqual(statuses[entry_id]["status"], "imported")
            self.assertTrue(statuses[entry_id]["canonical_label_present"])
        for entry_id in (
            "m_csa:777",
            "m_csa:784",
            "m_csa:904",
            "m_csa:836",
            "m_csa:996",
            "m_csa:611",
            "m_csa:657",
            "m_csa:1001",
            "m_csa:737",
        ):
            self.assertEqual(statuses[entry_id]["status"], "blocked")
            self.assertFalse(statuses[entry_id]["canonical_label_present"])

    def test_loose_cofactor_locality_policy_decision_is_terminal_no_go(
        self,
    ) -> None:
        policy = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_loose_cofactor_locality_policy_decision_3_20260524.json"
        )
        metadata = policy["metadata"]
        decision = policy["decision"]

        self.assertTrue(metadata["policy_class_decided"])
        self.assertTrue(metadata["terminal_no_go_for_current_evidence"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["still_blocked_count"], 3)
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            decision["policy_decision"],
            "conditionally_countable_but_current_rows_still_blocked",
        )
        self.assertTrue(
            decision[
                "can_loose_interdomain_or_cofactor_locality_exemplars_ever_be_countable"
            ]
        )
        self.assertIn(
            "dedicated import preview",
            " ".join(decision["minimum_structural_evidence_for_future_counting"]),
        )
        self.assertIn(
            "structure-wide metal or cofactor hits without local active-site support",
            decision["not_allowed_as_counting_evidence"],
        )

        rows = {row["entry_id"]: row for row in policy["rows"]}
        self.assertEqual(set(rows), {"m_csa:611", "m_csa:657", "m_csa:1001"})
        self.assertEqual(rows["m_csa:611"]["policy_class"], "loose_open_conformation")
        self.assertEqual(
            rows["m_csa:657"]["policy_class"],
            "acid_base_plus_metal_cofactor_locality",
        )
        self.assertEqual(
            rows["m_csa:1001"]["policy_class"],
            "oligomeric_or_role_pair_locality",
        )
        for row in rows.values():
            self.assertEqual(row["current_status"], "still_blocked")
            self.assertFalse(row["import_gate_eligible"])
            self.assertTrue(row["terminal_current_evidence_no_go"])
            self.assertTrue(row["countable_under_policy_if_evidence_is_supplied"])

    def test_apo_holo_terminal_no_go_keeps_current_rows_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_apo_holo_terminal_no_go_m_csa836_996_20260524.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]

        self.assertTrue(metadata["terminal_no_go_for_current_evidence"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["local_remapped_holo_evidence_found_count"], 0)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["still_blocked_count"], 2)
        self.assertFalse(metadata["selected_pdb_override_evidence_artifact_created"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            decision["new_status"],
            "terminal_current_evidence_still_blocked",
        )
        self.assertEqual(decision["canonical_count_movement"], "695 -> 695")
        self.assertFalse(packet["search_scope"]["new_override_artifact_found"])
        self.assertFalse(
            packet["search_scope"]["new_local_remapped_holo_candidate_found"]
        )

        rows = {row["entry_id"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), {"m_csa:836", "m_csa:996"})
        self.assertEqual(
            rows["m_csa:836"]["metal_containing_alternate_pdb_ids"],
            ["3SLP", "3SM4", "4WUZ"],
        )
        self.assertEqual(
            rows["m_csa:996"]["metal_containing_alternate_pdb_ids"],
            ["5O6Y"],
        )
        for row in rows.values():
            self.assertEqual(row["current_status"], "still_blocked")
            self.assertFalse(row["import_gate_eligible"])
            self.assertTrue(row["terminal_current_evidence_no_go"])
            self.assertEqual(row["alternate_pdb_with_remapped_positions_count"], 0)
            self.assertFalse(row["selected_active_site_has_expected_family"])

    def test_amp_product_terminal_no_go_keeps_rule_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_amp_product_terminal_no_go_m_csa784_904_20260524.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]

        self.assertTrue(metadata["terminal_no_go_for_current_evidence"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["product_context_exception_candidate_count"], 2)
        self.assertEqual(metadata["retain_counterevidence_control_count"], 33)
        self.assertFalse(metadata["production_rule_activated"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["production_rule_implemented_or_unit_tested"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["still_blocked_count"], 2)
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(
            decision["new_status"],
            "terminal_current_evidence_still_blocked",
        )
        self.assertEqual(decision["rule_promotion_decision"], "no_go_current_evidence")
        self.assertIn(
            "production_rule_not_implemented_or_unit_tested",
            decision["rule_promotion_blockers"],
        )
        self.assertEqual(decision["canonical_count_movement"], "695 -> 695")

        rows = {row["entry_id"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), {"m_csa:784", "m_csa:904"})
        self.assertEqual(rows["m_csa:784"]["top1_score_current"], 0.4082)
        self.assertEqual(rows["m_csa:904"]["top1_score_current"], 0.405)
        for row in rows.values():
            self.assertEqual(row["current_status"], "still_blocked")
            self.assertFalse(row["score_clears_current_threshold"])
            self.assertFalse(row["production_rule_activated"])
            self.assertFalse(row["import_gate_eligible"])
            self.assertTrue(row["terminal_current_evidence_no_go"])

    def test_plp_threshold_terminal_no_go_does_not_lower_threshold(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_plp_threshold_terminal_no_go_m_csa777_20260524.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]
        row = packet["row"]

        self.assertTrue(metadata["terminal_no_go_for_current_evidence"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertFalse(metadata["stronger_local_plp_evidence_found"])
        self.assertFalse(metadata["threshold_lowered"])
        self.assertFalse(metadata["explicit_gate_override_used"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["still_blocked_count"], 1)
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(
            decision["new_status"],
            "terminal_current_evidence_still_blocked",
        )
        self.assertEqual(decision["canonical_count_movement"], "695 -> 695")
        self.assertEqual(row["entry_id"], "m_csa:777")
        self.assertEqual(row["current_1025_score_for_import_gate"], 0.4107)
        self.assertEqual(row["abstain_threshold"], 0.4115)
        self.assertEqual(row["margin_to_threshold"], -0.0008)
        self.assertEqual(row["prior_score_excluded_from_1025_gate"], 0.5307)
        self.assertFalse(row["score_clears_current_threshold"])
        self.assertTrue(row["selected_active_site_has_expected_family"])
        self.assertEqual(row["matching_structure_ligands"][0]["code"], "LLP")
        self.assertEqual(row["missing_positions"], 1)
        self.assertFalse(row["import_gate_eligible"])
        self.assertTrue(row["terminal_current_evidence_no_go"])
        self.assertIn(
            "do not lower the 0.4115 threshold by 0.001 to import this row",
            row["do_not_repeat"],
        )

    def test_m_csa737_schema_decision_is_review_only_family_proposal(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_schema_decision_m_csa737_coupled_plp_cobalamin_proposal_20260524.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]
        row = packet["row"]

        self.assertTrue(metadata["schema_decision_recorded"])
        self.assertTrue(metadata["review_only_new_family_proposed"])
        self.assertTrue(metadata["terminal_no_go_for_current_production_universe"])
        self.assertFalse(metadata["multi_target_countable_label_proposed"])
        self.assertFalse(metadata["production_fingerprint_promotion_authorized"])
        self.assertFalse(metadata["production_fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["still_blocked_count"], 1)

        self.assertEqual(
            decision["schema_decision"],
            "review_only_new_coupled_cofactor_family_proposal",
        )
        self.assertEqual(
            decision["proposed_review_only_family_id"],
            "coupled_plp_adenosylcobalamin_aminomutase",
        )
        self.assertEqual(
            decision["production_decision"],
            "no_import_no_fingerprint_edit_current_run",
        )
        self.assertEqual(decision["canonical_count_movement"], "695 -> 695")

        self.assertEqual(row["entry_id"], "m_csa:737")
        self.assertEqual(row["current_status"], "still_blocked")
        self.assertFalse(row["import_gate_eligible"])
        self.assertTrue(row["terminal_current_production_universe_no_go"])
        self.assertEqual(row["current_target_fingerprint"], "cobalamin_radical_rearrangement")
        self.assertEqual(
            set(row["observed_cofactor_context"]["hetatms_in_structure"]),
            {"5AD", "B12", "PLP"},
        )
        self.assertIn("plain_cobalamin_radical_rearrangement", row["not_counted_as"])
        self.assertIn("plain_plp_dependent_enzyme", row["not_counted_as"])

    def test_remaining_nine_terminal_blocker_summary_has_no_import_path(self) -> None:
        summary = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_remaining_9_terminal_blocker_summary_20260524.json"
        )
        metadata = summary["metadata"]
        decision = summary["decision"]

        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["m_csa_countable_label_count_invariant"], 692)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["remaining_rows_evaluated_count"], 9)
        self.assertEqual(metadata["terminal_current_evidence_blocked_count"], 9)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertEqual(metadata["dedicated_import_previews_run_count"], 0)
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            decision["new_status"],
            "all_nine_have_terminal_current_evidence_no_go_artifacts",
        )
        self.assertEqual(decision["canonical_count_movement"], "695 -> 695")
        self.assertEqual(
            decision["import_decision"],
            "no_rows_imported_no_dedicated_import_preview_run",
        )

        rows = {row["entry_id"]: row for row in summary["rows"]}
        self.assertEqual(
            set(rows),
            {
                "m_csa:611",
                "m_csa:657",
                "m_csa:1001",
                "m_csa:836",
                "m_csa:996",
                "m_csa:784",
                "m_csa:904",
                "m_csa:777",
                "m_csa:737",
            },
        )
        for row in rows.values():
            self.assertFalse(row["import_gate_eligible"])
            self.assertTrue(row["terminal_artifact"].startswith("artifacts/v3_mcsa_positive_"))
            self.assertIn("still_blocked_terminal", row["new_status"])

    def test_post_clean9_decision_trace_preserves_row_signal_without_import(self) -> None:
        trace = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_post_clean9_decision_trace_22_20260524.json"
        )
        metadata = trace["metadata"]

        self.assertEqual(metadata["post_clean9_review_row_count"], 22)
        self.assertEqual(metadata["terminal_blocker_source_row_count"], 9)
        self.assertEqual(metadata["unique_trace_row_count"], 22)
        self.assertEqual(metadata["current_imported_countable_row_count"], 13)
        self.assertEqual(metadata["current_terminal_blocked_row_count"], 9)
        self.assertEqual(metadata["current_rejected_row_count"], 0)
        self.assertEqual(metadata["historical_import_gate_eligible_or_imported_count"], 13)
        self.assertEqual(metadata["new_import_gate_eligible_count_from_trace"], 0)
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["m_csa_countable_label_count_invariant"], 692)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["canonical_count_movement_this_artifact"], "695 -> 695")
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertTrue(metadata["decision_signal_preserved"])

        groups = trace["row_groups"]
        self.assertEqual(
            groups["imported_clean9"],
            [
                "m_csa:599",
                "m_csa:623",
                "m_csa:636",
                "m_csa:706",
                "m_csa:812",
                "m_csa:865",
                "m_csa:892",
                "m_csa:917",
                "m_csa:998",
            ],
        )
        self.assertEqual(
            groups["imported_holo_override_accept3"],
            ["m_csa:577", "m_csa:641", "m_csa:897"],
        )
        self.assertEqual(groups["imported_m_csa771_2d0d_vivek"], ["m_csa:771"])
        self.assertEqual(
            groups["terminal_current_evidence_blocked"],
            [
                "m_csa:611",
                "m_csa:657",
                "m_csa:1001",
                "m_csa:836",
                "m_csa:996",
                "m_csa:784",
                "m_csa:904",
                "m_csa:777",
                "m_csa:737",
            ],
        )
        self.assertEqual(groups["rejected"], [])

        required_fields = set(trace["trace_contract"]["required_row_fields"])
        rows = {row["entry_id"]: row for row in trace["rows"]}
        self.assertEqual(len(rows), 22)
        for row in rows.values():
            self.assertTrue(required_fields.issubset(row))
            self.assertTrue(row["evidence_for"])
            self.assertTrue(row["allowed_evidence"])
            self.assertTrue(row["forbidden_or_review_only_evidence"])
            self.assertTrue(row["reviewer_source"]["source_review_artifact"])
            self.assertTrue(row["structure_pdb_state"]["selected_pdb"])
            self.assertIsNotNone(row["tier_confidence"]["review_confidence"])
            self.assertTrue(row["would_unblock_if"])

        self.assertEqual(
            rows["m_csa:577"]["decision"]["current_decision"],
            "imported_by_holo_override_accept3_dedicated_gate",
        )
        self.assertEqual(
            rows["m_csa:577"]["structure_pdb_state"]["alternate_or_override_pdb"],
            "1AWB",
        )
        self.assertEqual(
            rows["m_csa:771"]["decision"]["current_decision"],
            "imported_by_m_csa771_2d0d_vivek_dedicated_gate",
        )
        self.assertTrue(
            rows["m_csa:771"]["structure_pdb_state"][
                "catalytic_ser103_maps_to_m_csa_nucleophile"
            ]
        )
        self.assertEqual(
            rows["m_csa:777"]["blocker_class"],
            "plp_threshold_local_evidence",
        )
        self.assertIn(
            "do not lower the 0.4115 threshold by 0.001 to import this row",
            rows["m_csa:777"]["forbidden_or_review_only_evidence"],
        )
        self.assertEqual(
            rows["m_csa:737"]["blocker_class"],
            "coupled_plp_adenosylcobalamin_schema",
        )

    def test_pymol_exact_mapping_terminal_no_go_keeps_tranche_non_countable(
        self,
    ) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_exact_mapping_terminal_no_go_23_20260524.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]

        self.assertTrue(metadata["terminal_current_evidence_no_go"])
        self.assertEqual(metadata["row_count"], 23)
        self.assertEqual(metadata["blocker_class"], "exact_ca_atom_pair_distance_mapping")
        self.assertEqual(metadata["structure_id_mapping_subblocker_count"], 2)
        self.assertEqual(metadata["terminal_nine_rows_reopened_count"], 0)
        self.assertEqual(metadata["next_structure_materialization_candidate_count"], 0)
        self.assertEqual(metadata["pymol_ready_count_in_source"], 298)
        self.assertEqual(metadata["rows_with_verified_focus_atoms_in_source"], 298)
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["canonical_count_movement"], "695 -> 695")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(decision["rows_changed"], 23)
        self.assertEqual(decision["rows_still_blocked"], 23)
        self.assertEqual(decision["rows_imported"], 0)
        self.assertIn("m_csa:946", decision["exact_next_target"])
        self.assertIn("m_csa:930", decision["exact_next_target"])

        terminal_nine = {
            "m_csa:611",
            "m_csa:657",
            "m_csa:1001",
            "m_csa:836",
            "m_csa:996",
            "m_csa:784",
            "m_csa:904",
            "m_csa:777",
            "m_csa:737",
        }
        rows = {row["entry_id"]: row for row in packet["rows"]}
        self.assertEqual(len(rows), 23)
        self.assertFalse(terminal_nine.intersection(rows))
        self.assertEqual(
            {
                entry_id
                for entry_id, row in rows.items()
                if row["blocker_class"] == "structure_id_plus_exact_ca_atom_pair_mapping"
            },
            {"m_csa:946", "m_csa:930"},
        )
        for row in rows.values():
            self.assertEqual(
                row["decision"],
                "terminal_current_evidence_no_go_for_pymol_readiness_and_import",
            )
            self.assertEqual(
                row["new_status"],
                "still_blocked_terminal_current_mapping_evidence",
            )
            self.assertIn("missing_exact_ca_atom_pair", row["missing_fields"])
            self.assertIn("missing_exact_distance", row["missing_fields"])
            self.assertFalse(row["import_gate_eligible"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertTrue(row["allowed_evidence"])
            self.assertTrue(row["forbidden_or_review_only_evidence"])
            self.assertTrue(row["would_unblock_if"])

    def test_exact_66_ai_visual_triage_matrix_pins_review_hold_rows(self) -> None:
        source = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json"
        )
        manifest = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_source_manifest_20260524.json"
        )
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )

        source_counts = {}
        for item in source["review_items"]:
            source_counts[item["decision"]] = source_counts.get(item["decision"], 0) + 1
        expected_counts = {"accepted": 22, "rejected": 210, "needs_more_evidence": 66}
        self.assertEqual(len(source["review_items"]), 298)
        self.assertEqual(source_counts, expected_counts)
        self.assertEqual(manifest["decision_counts"], expected_counts)
        self.assertEqual(manifest["exact_next_target"]["row_count"], 66)

        rows = matrix["rows"]
        self.assertEqual(len(rows), 66)
        target_ids = [row["entry_id"] for row in rows]
        self.assertEqual(target_ids, manifest["exact_next_target"]["ids"])

        accepted_ids = {
            row["entry_id"]
            for row in source["review_items"]
            if row["decision"] == "accepted"
        }
        rejected_ids = {
            row["entry_id"]
            for row in source["review_items"]
            if row["decision"] == "rejected"
        }
        self.assertFalse(accepted_ids.intersection(target_ids))
        self.assertFalse(rejected_ids.intersection(target_ids))

        metadata = matrix["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)

        integrity = matrix["source_integrity"]
        self.assertEqual(integrity["source_total_rows"], 298)
        self.assertEqual(integrity["source_decision_counts"], expected_counts)
        self.assertEqual(integrity["target_row_count"], 66)
        self.assertEqual(integrity["accepted_source_rows_excluded_count"], 22)
        self.assertEqual(integrity["rejected_source_rows_excluded_count"], 210)
        self.assertEqual(integrity["accepted_target_overlap"], [])
        self.assertEqual(integrity["rejected_target_overlap"], [])
        self.assertEqual(integrity["post_clean9_trace_overlap"], [])
        self.assertEqual(integrity["terminal_exact_mapping_overlap"], [])
        self.assertTrue(integrity["broad_review_debt_used_only_for_enrichment"])

        required_fields = set(matrix["triage_contract"]["required_row_fields"])
        allowed_buckets = set(matrix["triage_contract"]["allowed_blocker_buckets"])
        by_bucket = {bucket: 0 for bucket in allowed_buckets}
        by_confidence = {"high": 0, "medium": 0, "low": 0}
        for row in rows:
            self.assertTrue(required_fields.issubset(row))
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertIn(row["blocker_bucket"], allowed_buckets)
            self.assertIn(row["confidence"], by_confidence)
            self.assertTrue(row["preserve_for_learning"])
            self.assertTrue(row["evidence_for"])
            self.assertTrue(row["evidence_against"])
            self.assertTrue(row["visual_evidence_summary"])
            self.assertTrue(row["forbidden_or_review_only_evidence"])
            self.assertTrue(row["required_human_or_expert_action"])
            self.assertTrue(row["expected_import_potential"])
            self.assertTrue(row["would_unblock_if"])
            by_bucket[row["blocker_bucket"]] += 1
            by_confidence[row["confidence"]] += 1

        self.assertEqual(
            matrix["summary_counts"]["by_bucket"],
            {
                "clean_likely_positive": 10,
                "residue_mapping_issue": 0,
                "apo_or_holo_missing_cofactor": 14,
                "loose_open_or_interdomain_geometry": 4,
                "amp_or_nucleotide_nontransfer_context": 5,
                "coupled_or_missing_schema_family": 0,
                "wrong_fingerprint_or_future_ontology_family": 18,
                "true_reject": 9,
                "needs_manual_visual_review": 1,
                "needs_expert_biochemistry_review": 5,
                "already_terminal_no_go": 0,
                "already_imported_or_resolved": 0,
            },
        )
        self.assertEqual(
            matrix["summary_counts"]["by_confidence_tier"],
            {"high": 20, "medium": 40, "low": 6},
        )
        self.assertEqual(
            sum(matrix["summary_counts"]["by_bucket"].values()),
            66,
        )
        self.assertEqual(
            sum(matrix["summary_counts"]["by_confidence_tier"].values()),
            66,
        )

        plan = matrix["recommended_human_review_plan"]
        clean_ids = [
            row["entry_id"]
            for row in rows
            if row["blocker_bucket"] == "clean_likely_positive"
        ]
        low_confidence_ids = [
            row["entry_id"] for row in rows if row["confidence"] == "low"
        ]
        self.assertEqual(plan["review_all_clean_likely_positive_ids"], clean_ids)
        self.assertEqual(plan["review_all_low_confidence_ids"], low_confidence_ids)
        self.assertEqual(
            len(set(plan["unique_recommended_review_ids"])),
            plan["estimated_maximum_human_rows_to_review"],
        )
        self.assertEqual(plan["estimated_maximum_human_rows_to_review"], 40)
        for entry_id in clean_ids + low_confidence_ids:
            self.assertIn(entry_id, plan["unique_recommended_review_ids"])

        reps_by_bucket = plan["representative_ids_by_blocker_bucket"]
        for bucket, bucket_count in by_bucket.items():
            reps = reps_by_bucket[bucket]
            self.assertTrue(set(reps).issubset(target_ids))
            if bucket_count == 0:
                self.assertEqual(reps, [])
            elif bucket == "clean_likely_positive":
                self.assertEqual(reps, clean_ids)
            elif bucket_count == 1:
                self.assertEqual(len(reps), 1)
            else:
                self.assertGreaterEqual(len(reps), 2)
                self.assertLessEqual(len(reps), 5)

    def test_exact40_ai_visual_human_review_packets_are_review_only(self) -> None:
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json"
        )
        clean = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_clean10_review_first_packet_20260524.json"
        )
        template = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json"
        )
        pymol_index = _load_json(
            ARTIFACTS
            / "review_pymol"
            / "mcsa_ai_visual_exact40_20260524"
            / "index.json"
        )

        exact40 = matrix["recommended_human_review_plan"][
            "unique_recommended_review_ids"
        ]
        clean10 = matrix["recommended_human_review_plan"][
            "review_all_clean_likely_positive_ids"
        ]
        required_row_fields = {
            "entry_id",
            "entry_name",
            "structure_id",
            "structure_path",
            "target_fingerprint_id",
            "blocker_bucket",
            "confidence",
            "sample_review_priority",
            "expected_import_potential",
            "current_decision",
            "source_review_row_index",
            "source_artifact",
            "original_expert_note",
            "routing_evidence",
            "visual_evidence",
            "mcsa_structured_evidence",
            "evidence_for",
            "evidence_against",
            "counterevidence",
            "required_human_or_expert_action",
            "forbidden_or_review_only_evidence",
            "would_unblock_if",
            "allowed_reviewer_actions",
            "reviewer_question",
        }
        base_actions = {
            "accept_current_target",
            "reject_current_target",
            "needs_more_evidence",
            "route_future_family",
        }

        self.assertEqual(len(exact40), 40)
        self.assertEqual(packet["metadata"]["row_count"], 40)
        self.assertEqual([row["entry_id"] for row in packet["rows"]], exact40)
        self.assertTrue(packet["metadata"]["review_only"])
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertFalse(packet["metadata"]["default_accept_decisions"])
        self.assertFalse(packet["metadata"]["dedicated_import_preview_run"])
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["production_scoring_changed"])
        self.assertEqual(packet["metadata"]["canonical_label_count_invariant"], 695)
        self.assertEqual(
            packet["metadata"]["production_fingerprint_universe_count_invariant"],
            8,
        )
        self.assertEqual(
            packet["metadata"]["source_universe_counts"],
            {"accepted": 22, "rejected": 210, "needs_more_evidence": 66},
        )

        special_by_bucket = {
            "clean_likely_positive": "inspect_pymol",
            "needs_manual_visual_review": "inspect_pymol",
            "needs_expert_biochemistry_review": "expert_biochemistry_needed",
            "apo_or_holo_missing_cofactor": "find_holo_alternate",
            "loose_open_or_interdomain_geometry": "inspect_pymol",
            "amp_or_nucleotide_nontransfer_context": "expert_biochemistry_needed",
            "wrong_fingerprint_or_future_ontology_family": "schema_needed",
            "true_reject": "keep_review_only",
        }
        for row in packet["rows"]:
            self.assertTrue(required_row_fields.issubset(row))
            self.assertTrue(base_actions.issubset(row["allowed_reviewer_actions"]))
            self.assertIn(
                special_by_bucket[row["blocker_bucket"]],
                row["allowed_reviewer_actions"],
            )
            self.assertTrue(row["reviewer_question"])
            self.assertEqual(row["current_decision"], "needs_more_evidence")

        self.assertEqual(clean["metadata"]["row_count"], 10)
        self.assertEqual([row["entry_id"] for row in clean["rows"]], clean10)
        self.assertEqual(clean10, exact40[:10])
        self.assertFalse(clean["metadata"]["default_accept_decisions"])
        self.assertTrue(
            all(
                row["blocker_bucket"] == "clean_likely_positive"
                for row in clean["rows"]
            )
        )

        self.assertEqual(template["metadata"]["row_count"], 40)
        self.assertEqual([row["entry_id"] for row in template["rows"]], exact40)
        self.assertEqual(
            template["metadata"]["allowed_decisions"],
            ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
        )
        for row in template["rows"]:
            self.assertIsNone(row["decision"])
            self.assertIsNone(row["reviewer"])
            self.assertIsNone(row["reviewed_at"])
            self.assertEqual(row["expert_note"], "")
            self.assertIsNone(row["confidence_override"])

        self.assertEqual(pymol_index["metadata"]["clean_likely_positive_row_count"], 10)
        self.assertEqual(pymol_index["metadata"]["pymol_script_count"], 10)
        self.assertEqual(pymol_index["metadata"]["missing_structure_path_count"], 0)
        self.assertEqual([row["entry_id"] for row in pymol_index["rows"]], clean10)
        for row in pymol_index["rows"]:
            self.assertTrue((ROOT / row["pml_script_path"]).exists())

    def test_mcsa_ai_visual_learning_signal_manifest_is_leakage_aware(self) -> None:
        source = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json"
        )
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )
        manifest = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_learning_signal_manifest_20260524.json"
        )

        expected_counts = {"accepted": 22, "needs_more_evidence": 66, "rejected": 210}
        source_ids = [row["entry_id"] for row in source["review_items"]]
        matrix_ids = [row["entry_id"] for row in matrix["rows"]]
        exact40 = matrix["recommended_human_review_plan"][
            "unique_recommended_review_ids"
        ]
        clean10 = matrix["recommended_human_review_plan"][
            "review_all_clean_likely_positive_ids"
        ]

        metadata = manifest["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["source_row_count"], 298)
        self.assertEqual(metadata["emitted_row_count"], 298)
        self.assertEqual(metadata["source_universe_decision_counts"], expected_counts)

        rows = manifest["rows"]
        self.assertEqual(len(rows), 298)
        self.assertEqual([row["entry_id"] for row in rows], source_ids)
        self.assertEqual(
            Counter(row["decision_signal"] for row in rows),
            Counter(expected_counts),
        )
        self.assertEqual(
            manifest["summary_counts"]["learning_signal_partition"],
            {
                "current_target_hard_negative": 210,
                "positive_review_signal_review_only": 22,
                "unresolved_review_hold": 66,
            },
        )
        self.assertEqual(
            manifest["summary_counts"]["current_target_training_use"],
            {
                "exclude_pending_human_review": 66,
                "hard_negative_for_current_target_only": 210,
                "positive_review_signal_not_countable_label": 22,
            },
        )
        self.assertEqual(
            manifest["summary_counts"]["future_family_route_class_by_decision"],
            {
                "accepted": {
                    "named_future_family_route": 4,
                    "unrepresented_future_family_route": 18,
                },
                "needs_more_evidence": {
                    "named_future_family_route": 27,
                    "unrepresented_future_family_route": 39,
                },
                "rejected": {
                    "named_future_family_route": 154,
                    "unrepresented_future_family_route": 56,
                },
            },
        )
        self.assertEqual(
            manifest["summary_counts"]["review_hold_triage_bucket"],
            matrix["summary_counts"]["by_bucket"],
        )
        self.assertEqual(
            manifest["summary_counts"]["review_hold_triage_confidence"],
            matrix["summary_counts"]["by_confidence_tier"],
        )
        self.assertEqual(
            manifest["summary_counts"]["exact40_human_review_packet_overlap_count"],
            40,
        )
        self.assertEqual(
            manifest["summary_counts"]["clean10_review_first_overlap_count"],
            10,
        )

        hold_ids = [
            row["entry_id"]
            for row in rows
            if row["decision_signal"] == "needs_more_evidence"
        ]
        self.assertEqual(hold_ids, matrix_ids)
        exact40_manifest_ids = [
            row["entry_id"]
            for row in rows
            if row["unresolved_review_hold_context"]
            and row["unresolved_review_hold_context"][
                "exact40_human_review_packet_member"
            ]
        ]
        clean10_manifest_ids = [
            row["entry_id"]
            for row in rows
            if row["unresolved_review_hold_context"]
            and row["unresolved_review_hold_context"][
                "clean10_review_first_member"
            ]
        ]
        self.assertEqual(set(exact40_manifest_ids), set(exact40))
        self.assertEqual(len(exact40_manifest_ids), 40)
        self.assertEqual(set(clean10_manifest_ids), set(clean10))
        self.assertEqual(len(clean10_manifest_ids), 10)

        forbidden = set(
            manifest["prediction_leakage_contract"]["forbidden_for_prediction_fields"]
        )
        for field in [
            "decision_signal",
            "learning_signal_partition",
            "future_family_route",
            "review_signal_reason_codes",
            "expert_note",
            "reviewer",
            "reviewed_at",
            "review_context",
            "routing_evidence",
        ]:
            self.assertIn(field, forbidden)

        for row in rows:
            self.assertTrue(row["review_only_signal"])
            self.assertFalse(row["countable_training_label"])
            self.assertTrue(row["leakage_control"]["not_import_ready"])
            self.assertEqual(
                row["leakage_control"]["prediction_feature_status"],
                "do_not_train_directly_without_dropping_forbidden_fields",
            )
            self.assertNotIn("expert_note", row)
            self.assertNotIn("reviewer", row)
            self.assertNotIn("reviewed_at", row)
            self.assertNotIn("review_context", row)
            self.assertNotIn("routing_evidence", row)
            if row["decision_signal"] == "rejected":
                self.assertEqual(
                    row["current_target_training_use"],
                    "hard_negative_for_current_target_only",
                )
                self.assertTrue(row["current_target_rejected_not_global_negative"])
            elif row["decision_signal"] == "accepted":
                self.assertEqual(
                    row["current_target_training_use"],
                    "positive_review_signal_not_countable_label",
                )
            else:
                self.assertEqual(
                    row["current_target_training_use"],
                    "exclude_pending_human_review",
                )
                self.assertIsNotNone(row["unresolved_review_hold_context"])

    def test_mcsa_ai_visual_rejected_signal_taxonomy_stays_current_target_only(
        self,
    ) -> None:
        source = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json"
        )
        taxonomy = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_rejected_signal_taxonomy_20260524.json"
        )

        rejected_ids = [
            row["entry_id"]
            for row in source["review_items"]
            if row["decision"] == "rejected"
        ]
        accepted_or_hold_ids = {
            row["entry_id"]
            for row in source["review_items"]
            if row["decision"] != "rejected"
        }

        metadata = taxonomy["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["source_universe_row_count"], 298)
        self.assertEqual(metadata["rejected_row_count"], 210)
        self.assertEqual(
            metadata["source_universe_decision_counts"],
            {"accepted": 22, "needs_more_evidence": 66, "rejected": 210},
        )

        rows = taxonomy["rows"]
        self.assertEqual(len(rows), 210)
        self.assertEqual([row["entry_id"] for row in rows], rejected_ids)
        self.assertFalse(accepted_or_hold_ids.intersection(row["entry_id"] for row in rows))
        self.assertEqual(
            Counter(row["current_decision"] for row in rows),
            Counter({"rejected": 210}),
        )
        self.assertEqual(
            Counter(row["learning_manifest_partition"] for row in rows),
            Counter({"current_target_hard_negative": 210}),
        )
        self.assertEqual(
            taxonomy["summary_counts"]["target_fingerprint"],
            {
                "cobalamin_radical_rearrangement": 1,
                "flavin_dehydrogenase_reductase": 17,
                "flavin_monooxygenase": 9,
                "heme_peroxidase_oxidase": 28,
                "metal_dependent_hydrolase": 138,
                "plp_dependent_enzyme": 5,
                "ser_his_acid_hydrolase": 12,
            },
        )
        self.assertEqual(
            taxonomy["summary_counts"]["future_family_route_bucket"],
            {
                "cys_his_asp_protease_route": 3,
                "glycoside_hydrolase_route": 14,
                "heme_peroxide_chemistry_route": 3,
                "isomerase_mutase_route": 12,
                "lyase_dehydratase_or_schiff_base_route": 19,
                "oxidoreductase_redox_route": 34,
                "phosphoryl_transfer_kinase_route": 36,
                "plp_dependent_route": 2,
                "transferase_thioester_route": 31,
                "unrepresented_future_family_route": 56,
            },
        )
        self.assertEqual(
            sum(taxonomy["summary_counts"]["future_family_route_bucket"].values()),
            210,
        )
        self.assertEqual(
            sum(taxonomy["summary_counts"]["current_target_rejection_axis"].values()),
            210,
        )

        contract = taxonomy["taxonomy_contract"]
        self.assertIn("never global negatives", contract["negative_scope_rule"])
        self.assertIn("not acceptance decisions", contract["future_family_route_rule"])
        self.assertIn("forbidden as model features", contract["prediction_leakage_rule"])
        for row in rows:
            self.assertEqual(row["negative_scope"], "hard_negative_for_current_target_only")
            self.assertTrue(row["not_global_negative"])
            self.assertTrue(
                row["recommended_future_reuse"][
                    "use_as_current_target_hard_negative"
                ]
            )
            self.assertFalse(row["recommended_future_reuse"]["use_as_global_negative"])
            self.assertFalse(
                row["recommended_future_reuse"][
                    "use_for_future_family_positive_seed"
                ]
            )
            self.assertEqual(
                row["recommended_future_reuse"]["prediction_feature_status"],
                "review_derived_taxonomy_forbidden_as_model_feature",
            )
            self.assertNotIn("expert_note", row)
            self.assertNotIn("reviewer", row)
            self.assertNotIn("reviewed_at", row)

    def test_mcsa_ai_visual_nonclean_exact40_strategy_presorts_without_decisions(
        self,
    ) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json"
        )
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )
        strategy = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_nonclean30_exact40_strategy_20260524.json"
        )

        clean10 = set(
            matrix["recommended_human_review_plan"][
                "review_all_clean_likely_positive_ids"
            ]
        )
        nonclean_packet_rows = [
            row for row in packet["rows"] if row["entry_id"] not in clean10
        ]

        metadata = strategy["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["exact40_source_row_count"], 40)
        self.assertEqual(metadata["clean10_excluded_fast_path_count"], 10)
        self.assertEqual(metadata["nonclean_strategy_row_count"], 30)

        rows = strategy["rows"]
        self.assertEqual(len(rows), 30)
        self.assertEqual(
            [row["entry_id"] for row in rows],
            [row["entry_id"] for row in nonclean_packet_rows],
        )
        self.assertFalse(clean10.intersection(row["entry_id"] for row in rows))
        self.assertEqual(
            strategy["summary_counts"]["by_recommended_workflow"],
            {
                "expert_biochemistry_boundary_review": 10,
                "future_family_or_schema_route_review": 5,
                "reject_confirmation_review": 5,
                "structure_or_holo_alternate_resolution": 5,
                "structure_or_pymol_geometry_resolution": 5,
            },
        )
        self.assertEqual(
            strategy["summary_counts"]["by_blocker_bucket"],
            {
                "amp_or_nucleotide_nontransfer_context": 5,
                "apo_or_holo_missing_cofactor": 5,
                "loose_open_or_interdomain_geometry": 4,
                "needs_expert_biochemistry_review": 5,
                "needs_manual_visual_review": 1,
                "true_reject": 5,
                "wrong_fingerprint_or_future_ontology_family": 5,
            },
        )
        self.assertEqual(
            strategy["summary_counts"]["by_review_group"],
            {"low_confidence_review": 6, "representative_blocker_review": 24},
        )

        contract = strategy["strategy_contract"]
        self.assertIn("pre-sorts review workflows only", contract["decision_rule"])
        self.assertIn("Do not import labels", contract["no_import_rule"])
        self.assertEqual(
            contract["allowed_reviewer_decisions"],
            ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
        )

        for row in rows:
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertEqual(row["decision_status"], "blank_no_decision_made")
            self.assertNotEqual(row["blocker_bucket"], "clean_likely_positive")
            self.assertIn("needs_more_evidence", row["allowed_reviewer_actions"])
            self.assertTrue(row["reviewer_question"])
            self.assertTrue(row["primary_next_action"])
            self.assertTrue(row["required_human_or_expert_action"])

    def test_mcsa_ai_visual_clean10_fast_review_cards_join_local_scripts(
        self,
    ) -> None:
        clean = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_clean10_review_first_packet_20260524.json"
        )
        template = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json"
        )
        pymol_index = _load_json(
            ARTIFACTS
            / "review_pymol"
            / "mcsa_ai_visual_exact40_20260524"
            / "index.json"
        )
        cards = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_clean10_fast_review_cards_20260524.json"
        )

        clean_ids = [row["entry_id"] for row in clean["rows"]]
        template_by_id = {row["entry_id"]: row for row in template["rows"]}
        pymol_by_id = {row["entry_id"]: row for row in pymol_index["rows"]}

        metadata = cards["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["card_count"], 10)
        self.assertEqual(metadata["missing_structure_path_count"], 0)
        self.assertEqual(metadata["missing_pymol_script_count"], 0)
        self.assertEqual(metadata["blank_decision_count"], 10)

        self.assertEqual(
            cards["card_contract"]["allowed_decisions"],
            ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
        )
        self.assertIn("do not pre-fill", cards["card_contract"]["decision_rule"])
        self.assertIn("No label import", cards["card_contract"]["no_import_rule"])

        card_rows = cards["cards"]
        self.assertEqual([row["entry_id"] for row in card_rows], clean_ids)
        for row in card_rows:
            self.assertTrue(row["structure_path_exists"])
            self.assertTrue(row["pymol_script_exists"])
            self.assertTrue((ROOT / row["pymol_script_path"]).exists())
            self.assertEqual(
                row["decision_template_row"],
                template_by_id[row["entry_id"]]["review_order"],
            )
            self.assertIsNone(row["decision_template_current_decision"])
            self.assertEqual(row["decision_status"], "blank_no_decision_made")
            self.assertEqual(
                row["pymol_script_path"],
                pymol_by_id[row["entry_id"]]["pml_script_path"],
            )
            self.assertTrue(row["fast_path_checklist"])
            self.assertTrue(row["stop_conditions"])
            self.assertTrue(row["reviewer_question"])
            self.assertTrue(row["evidence_for_summary"])
            self.assertTrue(row["evidence_against_summary"])
            self.assertTrue(row["visual_focus"])

    def test_mcsa_ai_visual_review_support_index_links_current_surface(
        self,
    ) -> None:
        source = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json"
        )
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )
        template = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json"
        )
        workqueue = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json"
        )
        worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv"
        )
        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            worksheet_rows = list(csv.DictReader(handle, delimiter="\t"))
        index = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_review_support_index_20260524.json"
        )

        metadata = index["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)

        source_counts = Counter(row["decision"] for row in source["review_items"])
        self.assertEqual(
            dict(source_counts),
            {"accepted": 22, "rejected": 210, "needs_more_evidence": 66},
        )
        self.assertEqual(metadata["source_universe_row_count"], 298)
        self.assertEqual(metadata["accepted_review_signal_count"], 22)
        self.assertEqual(metadata["rejected_current_target_count"], 210)
        self.assertEqual(metadata["unresolved_review_hold_count"], 66)
        self.assertEqual(metadata["exact40_review_count"], 40)
        self.assertEqual(metadata["clean10_fast_path_count"], 10)
        self.assertEqual(metadata["nonclean30_strategy_count"], 30)
        self.assertEqual(metadata["deferred_hold_outside_exact40_count"], 26)
        self.assertEqual(metadata["deferred26_after_exact40_backlog_count"], 26)
        self.assertEqual(metadata["exact40_review_workqueue_worksheet_count"], 40)
        self.assertEqual(metadata["exact40_review_compact_worksheet_count"], 40)
        self.assertEqual(metadata["deferred26_after_exact40_worksheet_count"], 26)
        self.assertEqual(metadata["review_surface_readme_count"], 1)
        self.assertEqual(index["source_universe"]["decision_counts"], source_counts)

        exact40 = matrix["recommended_human_review_plan"][
            "unique_recommended_review_ids"
        ]
        clean10 = matrix["recommended_human_review_plan"][
            "review_all_clean_likely_positive_ids"
        ]
        navigation = index["review_navigation"]
        self.assertEqual(
            navigation["recommended_order"],
            [
                "exact40_review_workqueue",
                "exact40_review_workqueue_worksheet",
                "exact40_review_compact_worksheet",
                "clean10_fast_review_cards",
                "nonclean30_strategy",
                "exact40_decision_template",
                "deferred_holds_outside_exact40",
                "deferred26_after_exact40_backlog",
                "deferred26_after_exact40_worksheet",
            ],
        )
        self.assertEqual(
            navigation["exact40_review_workqueue"]["entry_ids"],
            exact40,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue"]["blank_decision_count"],
            40,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue"]["clean10_fast_path_count"],
            10,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue"]["nonclean30_strategy_count"],
            30,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue_worksheet"]["entry_ids"],
            exact40,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue_worksheet"]["blank_decision_count"],
            40,
        )
        self.assertEqual(
            navigation["exact40_review_workqueue_worksheet"]["guardrail"],
            "review_only_not_import_ready_no_automation_decision",
        )
        self.assertEqual([row["entry_id"] for row in worksheet_rows], exact40)
        self.assertEqual(
            navigation["clean10_fast_review_cards"]["entry_ids"],
            clean10,
        )
        self.assertEqual(
            navigation["nonclean30_strategy"]["entry_ids"],
            [entry_id for entry_id in exact40 if entry_id not in set(clean10)],
        )
        self.assertEqual(
            navigation["exact40_decision_template"]["entry_ids"],
            exact40,
        )
        self.assertEqual(
            navigation["exact40_decision_template"]["blank_decision_count"],
            40,
        )
        self.assertEqual(
            [row["decision"] for row in template["rows"]],
            [None] * 40,
        )
        self.assertEqual(workqueue["metadata"]["row_count"], 40)
        self.assertEqual(
            workqueue["metadata"]["schema_version"],
            "mcsa_ai_visual_exact40_review_workqueue.v1",
        )
        self.assertEqual(workqueue["metadata"]["blank_decision_count"], 40)
        self.assertEqual(workqueue["metadata"]["pymol_script_exists_count"], 10)
        self.assertEqual(
            [row["entry_id"] for row in workqueue["rows"]],
            exact40,
        )
        self.assertEqual(
            [row["decision_template_current_decision"] for row in workqueue["rows"]],
            [None] * 40,
        )
        self.assertEqual(
            [row["decision_template_expert_note"] for row in workqueue["rows"]],
            [""] * 40,
        )
        self.assertEqual(
            workqueue["summary_counts"]["by_recommended_workflow"],
            {
                "clean10_fast_visual_review": 10,
                "expert_biochemistry_boundary_review": 10,
                "structure_or_pymol_geometry_resolution": 5,
                "structure_or_holo_alternate_resolution": 5,
                "future_family_or_schema_route_review": 5,
                "reject_confirmation_review": 5,
            },
        )
        self.assertEqual(
            workqueue["summary_counts"]["by_workqueue_phase"],
            {"clean10_fast_path": 10, "nonclean30_strategy": 30},
        )
        self.assertEqual(
            [row["recommended_workflow"] for row in workqueue["rows"][:10]],
            ["clean10_fast_visual_review"] * 10,
        )
        self.assertTrue(
            all(
                row["decision_status"] == "blank_no_decision_made"
                for row in workqueue["rows"]
            )
        )
        self.assertEqual(
            navigation["deferred_holds_outside_exact40"]["by_blocker_bucket"],
            {
                "apo_or_holo_missing_cofactor": 9,
                "true_reject": 4,
                "wrong_fingerprint_or_future_ontology_family": 13,
            },
        )
        self.assertEqual(
            navigation["deferred_holds_outside_exact40"]["by_confidence"],
            {"high": 4, "medium": 22},
        )
        deferred_matrix_rows = [
            row for row in matrix["rows"] if row["entry_id"] not in set(exact40)
        ]
        deferred = navigation["deferred_holds_outside_exact40"]
        self.assertEqual(
            deferred["entry_ids"],
            [row["entry_id"] for row in deferred_matrix_rows],
        )
        self.assertEqual(len(deferred["rows"]), 26)
        self.assertFalse(set(deferred["entry_ids"]).intersection(exact40))
        self.assertFalse(set(deferred["entry_ids"]).intersection(clean10))
        self.assertEqual(
            deferred["by_defer_lane"],
            {
                "defer_future_family_or_schema_route": 13,
                "defer_holo_or_local_cofactor_evidence": 9,
                "defer_reject_confirmation_after_representative_review": 4,
            },
        )
        for row in deferred["rows"]:
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertEqual(row["decision_status"], "blank_no_decision_made")
            self.assertFalse(row["exact40_member"])
            self.assertFalse(row["clean10_member"])
            self.assertNotEqual(row["confidence"], "low")
            self.assertNotEqual(row["blocker_bucket"], "clean_likely_positive")
            self.assertTrue(row["representative_exact40_ids_for_bucket"])
            self.assertTrue(row["defer_reason"])
            self.assertTrue(row["open_after"])
            self.assertTrue(row["safe_next_action_if_reopened"])

        learning = index["learning_navigation"]
        self.assertEqual(
            learning["learning_signal_manifest"]["partition_counts"],
            {
                "current_target_hard_negative": 210,
                "positive_review_signal_review_only": 22,
                "unresolved_review_hold": 66,
            },
        )
        self.assertEqual(
            learning["rejected_signal_taxonomy"]["negative_scope"],
            "hard_negative_for_current_target_only",
        )
        self.assertIn(
            "decision_signal",
            learning["learning_signal_manifest"]["forbidden_for_prediction_fields"],
        )

        self.assertEqual(
            metadata["schema_version"], "mcsa_ai_visual_review_support_index.v1"
        )
        next_actions = index["next_recommended_actions"]
        self.assertEqual(
            [row["action"] for row in next_actions],
            [
                "human_review_clean10_first",
                "human_review_nonclean30_by_strategy_workflow",
                "automation_may_only_maintain_review_support_consistency",
            ],
        )
        self.assertEqual(
            [row["requires_human_decision"] for row in next_actions],
            [True, True, False],
        )
        self.assertEqual(
            [row["blocked_while_vivek_away"] for row in next_actions],
            [True, True, False],
        )

        consistency = index["cross_artifact_consistency"]
        for key, value in consistency.items():
            if key.endswith("_count"):
                self.assertGreaterEqual(value, 0)
            else:
                self.assertTrue(value, key)
        self.assertEqual(consistency["deferred_holds_outside_exact40_count"], 26)
        self.assertEqual(consistency["clean10_pymol_script_existing_count"], 10)
        self.assertEqual(consistency["exact40_structure_path_exists_count"], 40)
        self.assertEqual(consistency["blank_template_decision_count"], 40)
        self.assertEqual(consistency["workqueue_blank_decision_count"], 40)
        self.assertEqual(consistency["workqueue_pymol_script_existing_count"], 10)
        self.assertTrue(consistency["workqueue_matches_exact40_template"])
        self.assertTrue(consistency["deferred26_backlog_matches_deferred_holds"])
        self.assertTrue(consistency["workqueue_worksheet_matches_workqueue"])
        self.assertEqual(consistency["workqueue_worksheet_blank_decision_count"], 40)
        self.assertEqual(consistency["workqueue_worksheet_guardrail_count"], 40)
        self.assertTrue(consistency["exact40_compact_worksheet_matches_workqueue"])
        self.assertEqual(
            consistency["exact40_compact_worksheet_blank_decision_count"], 40
        )
        self.assertEqual(consistency["exact40_compact_worksheet_guardrail_count"], 40)
        self.assertTrue(consistency["deferred26_worksheet_matches_backlog"])
        self.assertEqual(consistency["deferred26_worksheet_blank_decision_count"], 26)
        self.assertEqual(consistency["deferred26_worksheet_guardrail_count"], 26)
        self.assertTrue(consistency["review_surface_readme_exists"])

        artifact_paths = metadata["source_artifacts"].values()
        for artifact_path in artifact_paths:
            self.assertTrue((ROOT / artifact_path).exists(), artifact_path)
        for catalog_row in index["artifact_catalog"]:
            self.assertTrue((ROOT / catalog_row["path"]).exists())
            self.assertTrue(catalog_row["do_not_use_for"])

        self.assertIn("do_not_import_labels", index["forbidden_operations"])
        self.assertIn("do_not_run_label_import_previews", index["forbidden_operations"])
        self.assertIn(
            "do_not_make_biological_accept_reject_calls_without_human_decision",
            index["forbidden_operations"],
        )

    def test_mcsa_ai_visual_review_surface_readme_points_at_safe_artifacts(
        self,
    ) -> None:
        readme_path = (
            ARTIFACTS / "v3_mcsa_ai_visual_review_surface_readme_20260524.md"
        )
        text = readme_path.read_text(encoding="utf-8")

        for snippet in [
            "298 rows",
            "22 accepted review signals",
            "210 current-target-only",
            "66 unresolved",
            "40 rows, all with blank decisions",
            "10 clean-likely-positive",
            "26 rows outside exact40",
            "695 curated labels",
            "8 production",
            "does not authorize label imports",
            "v3_mcsa_ai_visual_review_support_index_20260524.json",
            "v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv",
            "v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv",
        ]:
            self.assertIn(snippet, text)

    def test_mcsa_ai_visual_exact40_workqueue_worksheet_is_blank_review_only(
        self,
    ) -> None:
        workqueue = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json"
        )
        worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv"
        )
        compact_worksheet_path = (
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_worksheet_20260524.tsv"
        )
        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        with compact_worksheet_path.open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            compact_rows = list(csv.DictReader(handle, delimiter="\t"))

        self.assertEqual(len(rows), 40)
        self.assertEqual(
            [row["entry_id"] for row in rows],
            [row["entry_id"] for row in workqueue["rows"]],
        )
        self.assertEqual(
            Counter(row["queue_lane"] for row in rows),
            Counter(workqueue["summary_counts"]["by_queue_lane"]),
        )
        self.assertEqual(
            Counter(row["workqueue_phase"] for row in rows),
            Counter({"clean10_fast_path": 10, "nonclean30_strategy": 30}),
        )
        self.assertEqual([row["decision"] for row in rows], [""] * 40)
        self.assertEqual([row["reviewer"] for row in rows], [""] * 40)
        self.assertEqual([row["reviewed_at"] for row in rows], [""] * 40)
        self.assertEqual([row["expert_note"] for row in rows], [""] * 40)
        self.assertEqual([row["confidence_override"] for row in rows], [""] * 40)
        self.assertEqual(
            Counter(row["pymol_script_exists"] for row in rows),
            Counter({"true": 10, "false": 30}),
        )
        self.assertEqual(
            Counter(row["review_only_guardrail"] for row in rows),
            Counter({"review_only_not_import_ready_no_automation_decision": 40}),
        )
        self.assertEqual(
            [row["entry_id"] for row in compact_rows],
            [row["entry_id"] for row in workqueue["rows"]],
        )
        self.assertEqual([row["decision"] for row in compact_rows], [""] * 40)
        self.assertEqual(
            Counter(row["no_import_guard"] for row in compact_rows),
            Counter(
                {
                    "review_only_no_label_import_no_import_preview_no_registry_or_fingerprint_edit": 40
                }
            ),
        )
        for row in rows:
            self.assertEqual(
                row["allowed_decisions"],
                "accepted|rejected|needs_more_evidence|route_future_family",
            )
            self.assertTrue(row["primary_next_action"])
            self.assertTrue(row["required_human_or_expert_action"])

    def test_mcsa_ai_visual_deferred26_worksheet_waits_for_exact40(
        self,
    ) -> None:
        backlog = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_deferred26_after_exact40_backlog_20260524.json"
        )
        worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv"
        )
        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))

        self.assertEqual(len(rows), 26)
        self.assertEqual(
            [row["entry_id"] for row in rows],
            [row["entry_id"] for row in backlog["rows"]],
        )
        self.assertEqual(
            Counter(row["review_timing"] for row in rows),
            Counter({"review_after_exact40_packet_or_new_bounded_plan": 26}),
        )
        self.assertEqual(
            Counter(row["blocker_bucket"] for row in rows),
            Counter(backlog["summary_counts"]["by_blocker_bucket"]),
        )
        self.assertEqual([row["decision"] for row in rows], [""] * 26)
        self.assertEqual([row["reviewer"] for row in rows], [""] * 26)
        self.assertEqual([row["reviewed_at"] for row in rows], [""] * 26)
        self.assertEqual([row["expert_note"] for row in rows], [""] * 26)
        self.assertEqual(
            Counter(row["review_only_guardrail"] for row in rows),
            Counter({"deferred_review_only_after_exact40_not_import_ready": 26}),
        )
        for row in rows:
            self.assertEqual(
                row["allowed_future_reviewer_decisions"],
                "accepted|rejected|needs_more_evidence|route_future_family",
            )
            self.assertTrue(row["next_review_only_action"])
            self.assertTrue(row["required_human_or_expert_action"])

    def test_mcsa_ai_visual_deferred26_backlog_waits_for_exact40(
        self,
    ) -> None:
        matrix = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json"
        )
        backlog = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_deferred26_after_exact40_backlog_20260524.json"
        )
        worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv"
        )
        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            worksheet_rows = list(csv.DictReader(handle, delimiter="\t"))

        exact40 = set(
            matrix["recommended_human_review_plan"]["unique_recommended_review_ids"]
        )
        deferred_matrix_rows = [
            row for row in matrix["rows"] if row["entry_id"] not in exact40
        ]
        deferred_ids = [row["entry_id"] for row in deferred_matrix_rows]

        metadata = backlog["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["source_universe_row_count"], 298)
        self.assertEqual(metadata["triage_matrix_row_count"], 66)
        self.assertEqual(metadata["exact40_excluded_review_packet_count"], 40)
        self.assertEqual(metadata["deferred_backlog_row_count"], 26)
        self.assertEqual(
            metadata["schema_version"],
            "mcsa_ai_visual_deferred26_after_exact40_backlog.v1",
        )

        rows = backlog["rows"]
        self.assertEqual(len(rows), 26)
        self.assertEqual([row["entry_id"] for row in rows], deferred_ids)
        self.assertEqual(len(worksheet_rows), 26)
        self.assertEqual([row["entry_id"] for row in worksheet_rows], deferred_ids)
        self.assertFalse(exact40.intersection(row["entry_id"] for row in rows))
        self.assertEqual(
            Counter(row["current_decision"] for row in rows),
            Counter({"needs_more_evidence": 26}),
        )
        self.assertEqual(
            Counter(row["decision_status"] for row in rows),
            Counter({"deferred_no_decision_made": 26}),
        )
        self.assertEqual(
            Counter(row["review_timing"] for row in rows),
            Counter({"review_after_exact40_packet_or_new_bounded_plan": 26}),
        )

        self.assertEqual(
            backlog["summary_counts"]["by_blocker_bucket"],
            {
                "apo_or_holo_missing_cofactor": 9,
                "true_reject": 4,
                "wrong_fingerprint_or_future_ontology_family": 13,
            },
        )
        self.assertEqual(
            backlog["summary_counts"]["by_confidence"],
            {"high": 4, "medium": 22},
        )
        self.assertEqual(
            backlog["summary_counts"]["by_expected_import_potential"],
            {
                "low_for_current_fingerprint_possible_future_ontology_signal": 13,
                "medium_if_local_holo_or_cofactor_evidence_is_found": 9,
                "none_for_current_fingerprint": 4,
            },
        )
        self.assertEqual(
            backlog["summary_counts"]["by_sample_review_priority"],
            {"low": 17, "medium": 9},
        )

        contract = backlog["backlog_contract"]
        self.assertIn("makes no biological accept/reject calls", contract["decision_rule"])
        self.assertIn("after the exact40 packet", contract["review_timing_rule"])
        self.assertIn("Do not import labels", contract["no_import_rule"])
        self.assertEqual(
            contract["allowed_future_reviewer_decisions"],
            ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
        )

        for row in rows:
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertEqual(row["why_deferred"], "outside_exact40_recommended_human_review_plan_current_run")
            self.assertTrue(row["required_human_or_expert_action"])
            self.assertTrue(row["next_review_only_action"])
            self.assertTrue(row["would_unblock_if"])
            self.assertTrue(row["evidence_for_summary"])
            self.assertTrue(row["evidence_against_summary"])
            self.assertEqual(
                row["allowed_future_reviewer_decisions"],
                ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
            )
        for row in worksheet_rows:
            self.assertEqual(row["decision"], "")
            self.assertEqual(row["reviewer"], "")
            self.assertEqual(row["reviewed_at"], "")
            self.assertEqual(row["expert_note"], "")
            self.assertEqual(
                row["review_only_guardrail"],
                "deferred_review_only_after_exact40_not_import_ready",
            )

        worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv"
        )
        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            worksheet_rows = list(csv.DictReader(handle, delimiter="\t"))

        self.assertEqual(len(worksheet_rows), 26)
        self.assertEqual([row["entry_id"] for row in worksheet_rows], deferred_ids)
        self.assertEqual(
            Counter(row["review_timing"] for row in worksheet_rows),
            Counter({"review_after_exact40_packet_or_new_bounded_plan": 26}),
        )
        self.assertEqual(
            Counter(row["blocker_bucket"] for row in worksheet_rows),
            Counter(
                {
                    "apo_or_holo_missing_cofactor": 9,
                    "true_reject": 4,
                    "wrong_fingerprint_or_future_ontology_family": 13,
                }
            ),
        )
        for row in worksheet_rows:
            self.assertEqual(row["decision"], "")
            self.assertEqual(row["reviewer"], "")
            self.assertEqual(row["reviewed_at"], "")
            self.assertEqual(row["expert_note"], "")
            self.assertEqual(
                row["allowed_future_reviewer_decisions"],
                "accepted|rejected|needs_more_evidence|route_future_family",
            )
            self.assertEqual(
                row["review_only_guardrail"],
                "deferred_review_only_after_exact40_not_import_ready",
            )

    def test_mcsa_ai_visual_exact40_workqueue_keeps_decisions_blank(
        self,
    ) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json"
        )
        clean_cards = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_clean10_fast_review_cards_20260524.json"
        )
        nonclean = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_nonclean30_exact40_strategy_20260524.json"
        )
        template = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json"
        )
        workqueue = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json"
        )

        metadata = workqueue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["review_only_source_artifacts_mutated"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["row_count"], 40)
        self.assertEqual(metadata["clean10_fast_path_count"], 10)
        self.assertEqual(metadata["nonclean30_strategy_count"], 30)
        self.assertEqual(metadata["blank_decision_count"], 40)
        self.assertEqual(metadata["pymol_script_exists_count"], 10)
        self.assertEqual(metadata["structure_path_exists_count"], 40)

        rows = workqueue["rows"]
        packet_ids = [row["entry_id"] for row in packet["rows"]]
        clean_ids = [row["entry_id"] for row in clean_cards["cards"]]
        nonclean_ids = [row["entry_id"] for row in nonclean["rows"]]
        self.assertEqual(len(rows), 40)
        self.assertEqual([row["entry_id"] for row in rows], packet_ids)
        self.assertEqual([row["entry_id"] for row in rows[:10]], clean_ids)
        self.assertEqual([row["entry_id"] for row in rows[10:]], nonclean_ids)
        self.assertEqual(
            [row["decision"] for row in template["rows"]],
            [None] * 40,
        )

        self.assertEqual(
            workqueue["summary_counts"]["by_workqueue_phase"],
            {"clean10_fast_path": 10, "nonclean30_strategy": 30},
        )
        self.assertEqual(
            workqueue["summary_counts"]["by_decision_status"],
            {"blank_no_decision_made": 40},
        )
        self.assertEqual(
            workqueue["summary_counts"]["by_recommended_workflow"],
            {
                "clean10_fast_visual_review": 10,
                "expert_biochemistry_boundary_review": 10,
                "future_family_or_schema_route_review": 5,
                "reject_confirmation_review": 5,
                "structure_or_holo_alternate_resolution": 5,
                "structure_or_pymol_geometry_resolution": 5,
            },
        )

        contract = workqueue["review_contract"]
        self.assertIn("every decision field remains blank", contract["decision_rule"])
        self.assertIn("Do not import labels", contract["no_import_rule"])
        self.assertEqual(
            contract["allowed_decisions"],
            ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
        )

        for artifact_key, artifact_path in metadata["source_artifacts"].items():
            path = ROOT / artifact_path
            self.assertTrue(path.exists(), artifact_path)
            with path.open("rb") as handle:
                digest = hashlib.sha256(handle.read()).hexdigest()
            self.assertEqual(digest, metadata["source_sha256"][artifact_key])

        for row in rows:
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertEqual(row["decision_status"], "blank_no_decision_made")
            self.assertIsNone(row["decision_template_current_decision"])
            self.assertEqual(row["decision_template_expert_note"], "")
            self.assertEqual(
                row["allowed_decisions"],
                ["accepted", "rejected", "needs_more_evidence", "route_future_family"],
            )
            self.assertTrue(row["primary_next_action"])
            self.assertTrue(row["required_human_or_expert_action"])
            self.assertTrue(row["reviewer_question"])
            self.assertTrue(row["would_unblock_if"])

    def test_mcsa_ai_visual_exact40_review_worksheet_is_blank_tsv(
        self,
    ) -> None:
        workqueue = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json"
        )
        worksheet_path = (
            ARTIFACTS / "v3_mcsa_ai_visual_exact40_review_worksheet_20260524.tsv"
        )

        with worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))

        expected_columns = [
            "workqueue_order",
            "workqueue_phase",
            "entry_id",
            "entry_name",
            "target_fingerprint_id",
            "structure_id",
            "structure_path",
            "pymol_script_path",
            "recommended_workflow",
            "blocker_bucket",
            "confidence",
            "current_decision",
            "decision",
            "reviewer",
            "reviewed_at",
            "expert_note",
            "confidence_override",
            "reviewer_question",
            "primary_next_action",
            "allowed_decisions",
            "stop_conditions",
            "no_import_guard",
        ]
        self.assertEqual(rows[0].keys(), dict.fromkeys(expected_columns).keys())
        self.assertEqual(len(rows), 40)
        self.assertEqual(
            [row["entry_id"] for row in rows],
            [row["entry_id"] for row in workqueue["rows"]],
        )
        self.assertEqual(
            Counter(row["workqueue_phase"] for row in rows),
            Counter({"clean10_fast_path": 10, "nonclean30_strategy": 30}),
        )
        self.assertEqual(
            Counter(row["recommended_workflow"] for row in rows),
            Counter(workqueue["summary_counts"]["by_recommended_workflow"]),
        )

        blank_columns = [
            "decision",
            "reviewer",
            "reviewed_at",
            "expert_note",
            "confidence_override",
        ]
        for row in rows:
            for column in blank_columns:
                self.assertEqual(row[column], "")
            self.assertEqual(row["current_decision"], "needs_more_evidence")
            self.assertEqual(
                row["allowed_decisions"],
                "accepted | rejected | needs_more_evidence | route_future_family",
            )
            self.assertEqual(
                row["no_import_guard"],
                "review_only_no_label_import_no_import_preview_no_registry_or_fingerprint_edit",
            )
            self.assertTrue(row["reviewer_question"])
            self.assertTrue(row["primary_next_action"])

        self.assertEqual(
            sum(1 for row in rows if row["pymol_script_path"]),
            10,
        )

        rich_worksheet_path = (
            ARTIFACTS
            / "v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv"
        )
        with rich_worksheet_path.open("r", encoding="utf-8", newline="") as handle:
            rich_rows = list(csv.DictReader(handle, delimiter="\t"))

        rich_expected_columns = [
            "workqueue_order",
            "queue_lane",
            "workqueue_phase",
            "decision_template_row",
            "entry_id",
            "entry_name",
            "target_fingerprint_id",
            "structure_id",
            "structure_path",
            "structure_path_exists",
            "pymol_script_path",
            "pymol_script_exists",
            "confidence",
            "blocker_bucket",
            "sample_review_priority",
            "reviewer_question",
            "primary_next_action",
            "required_human_or_expert_action",
            "would_unblock_if",
            "decision",
            "reviewer",
            "reviewed_at",
            "expert_note",
            "confidence_override",
            "allowed_decisions",
            "review_only_guardrail",
        ]
        self.assertEqual(
            rich_rows[0].keys(),
            dict.fromkeys(rich_expected_columns).keys(),
        )
        self.assertEqual(len(rich_rows), 40)
        self.assertEqual(
            [row["entry_id"] for row in rich_rows],
            [row["entry_id"] for row in workqueue["rows"]],
        )
        self.assertEqual(
            Counter(row["queue_lane"] for row in rich_rows),
            Counter(workqueue["summary_counts"]["by_recommended_workflow"]),
        )
        self.assertEqual(
            Counter(row["workqueue_phase"] for row in rich_rows),
            Counter({"clean10_fast_path": 10, "nonclean30_strategy": 30}),
        )
        for row in rich_rows:
            for column in blank_columns:
                self.assertEqual(row[column], "")
            self.assertEqual(
                row["allowed_decisions"],
                "accepted|rejected|needs_more_evidence|route_future_family",
            )
            self.assertEqual(
                row["review_only_guardrail"],
                "review_only_not_import_ready_no_automation_decision",
            )
            self.assertTrue(row["reviewer_question"])
            self.assertTrue(row["primary_next_action"])
            self.assertTrue(row["required_human_or_expert_action"])

        self.assertEqual(
            sum(1 for row in rich_rows if row["pymol_script_exists"] == "true"),
            10,
        )

    def test_structure_id_mapping_probe_finds_one_repair_candidate_only(self) -> None:
        probe = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_structure_id_mapping_repair_probe_m_csa930_946_20260524.json"
        )
        metadata = probe["metadata"]
        decision = probe["decision"]

        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 2)
        self.assertEqual(metadata["mapping_repair_candidate_ready_count"], 1)
        self.assertEqual(metadata["still_blocked_count"], 1)
        self.assertEqual(metadata["canonical_label_count_invariant"], 695)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)
        self.assertEqual(metadata["canonical_count_movement"], "695 -> 695")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_gate_eligible_count"], 0)
        self.assertFalse(metadata["dedicated_import_preview_run"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["coordinate_sidecars_committed"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(decision["rows_changed"], 2)
        self.assertEqual(decision["rows_still_blocked"], 1)
        self.assertEqual(decision["rows_imported"], 0)
        self.assertIn("m_csa:946", decision["exact_next_target"])
        self.assertIn("m_csa:930", decision["exact_next_target"])

        rows = {row["entry_id"]: row for row in probe["rows"]}
        self.assertEqual(set(rows), {"m_csa:930", "m_csa:946"})
        self.assertEqual(
            rows["m_csa:930"]["decision"],
            "still_blocked_terminal_current_source_mapping",
        )
        self.assertEqual(
            rows["m_csa:930"]["blocker_class"],
            "candidate_pdb_reference_uniprot_mismatch",
        )
        self.assertIsNone(rows["m_csa:930"]["recommended_candidate_pdb_id"])
        two_pia = rows["m_csa:930"]["candidate_pdb_results"][0]
        self.assertEqual(two_pia["pdb_id"], "2PIA")
        self.assertEqual(two_pia["observed_uniprot_accessions"], ["P33164"])
        self.assertFalse(two_pia["all_requested_residues_mapped_to_ca"])

        self.assertEqual(
            rows["m_csa:946"]["decision"],
            "mapping_repair_candidate_ready_for_review_queue_rerun",
        )
        self.assertEqual(rows["m_csa:946"]["recommended_candidate_pdb_id"], "5XD7")
        ready_candidates = [
            result
            for result in rows["m_csa:946"]["candidate_pdb_results"]
            if result["all_requested_residues_mapped_to_ca"]
        ]
        self.assertGreaterEqual(len(ready_candidates), 2)
        five_xd7 = next(
            result
            for result in rows["m_csa:946"]["candidate_pdb_results"]
            if result["pdb_id"] == "5XD7"
        )
        self.assertEqual(five_xd7["observed_uniprot_accessions"], ["H2IFX0"])
        self.assertEqual(five_xd7["mapped_residue_count"], 6)
        self.assertEqual(five_xd7["requested_residue_count"], 6)
        self.assertTrue(five_xd7["all_requested_residues_mapped_to_ca"])
        self.assertEqual(
            five_xd7["longest_ca_pair"]["left_residue_node_id"],
            "m_csa:946:residue:2",
        )
        self.assertEqual(
            five_xd7["longest_ca_pair"]["right_residue_node_id"],
            "m_csa:946:residue:6",
        )
        self.assertAlmostEqual(
            five_xd7["longest_ca_pair"]["distance_angstrom"],
            18.663,
            places=3,
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

    def test_sdr_post_plp_readiness_recheck_stays_existing_evidence_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_sdr_family_readiness_post_plp_terminal_review_packet_20260521.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]
        caveats = packet["modern_baseline_caveats"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertEqual(metadata["source_free_sdr_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            decision["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertIn(
            "source_free_nad_p_ligand_or_cofactor_proxy_geometry_axis_missing",
            decision["exact_missing_evidence"],
        )
        self.assertIn(
            "broader_duplicate_screening_unresolved_for_positive_like_rows",
            decision["exact_missing_evidence"],
        )

        evidence = packet["evidence_summary"]["active_site_and_cofactor_evidence"]
        self.assertEqual(evidence["current_status"], "source_traced_not_source_free")
        self.assertFalse(evidence["direct_local_nad_p_ligand_geometry_ready"])
        self.assertFalse(
            evidence["predictive_evidence_separation"][
                "ec_keyword_or_protein_name_counted_as_predictive_evidence"
            ]
        )
        self.assertEqual(
            packet["evidence_summary"]["current_eight_fingerprint_context"][
                "sdr_false_non_abstention_count"
            ],
            0,
        )

        self.assertFalse(caveats["superiority_claim"])
        self.assertFalse(caveats["superiority_claim_permitted"])
        self.assertEqual(caveats["esm_sidecar"], "not_available_for_this_readiness_recheck")
        self.assertFalse(packet["next_exact_experiment"]["decision_to_start_now"])
        self.assertTrue(
            packet["next_exact_experiment"]["selection_freeze_required_before_scoring"]
        )
        self.assertIn(
            "source active-site residue annotations",
            packet["next_exact_experiment"]["excluded_predictive_inputs"],
        )
        self.assertFalse(packet["safety_and_scope"]["label_import_attempted"])
        self.assertFalse(packet["safety_and_scope"]["production_fingerprint_added"])

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

    def test_akr_post_q99504_readiness_recheck_keeps_no_go_decision(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_akr_family_readiness_post_q99504_terminal_recheck_20260521.json"
        )
        metadata = packet["metadata"]
        decision = packet["decision"]
        evidence = packet["evidence_summary"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["production_fingerprint_count"], 8)
        self.assertEqual(metadata["source_free_akr_axis_ready_count"], 0)
        self.assertEqual(metadata["positive_like_row_count"], 1)
        self.assertEqual(metadata["control_tranche_row_count"], 14)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(
            decision["current_decision"],
            "do_not_promote_production_fingerprint",
        )
        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertIn(
            "source_free_local_nadp_ligand_or_proxy_geometry_axis_missing",
            decision["exact_missing_evidence"],
        )
        self.assertIn(
            "broader_duplicate_screening_unresolved_for_c9jrz8_or_fresh_akr_rows",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(evidence["positive_like_rows"][0]["accession"], "C9JRZ8")
        self.assertFalse(
            evidence["positive_like_rows"][0]["direct_local_nadp_ligand_geometry_ready"]
        )
        self.assertFalse(
            evidence["positive_like_rows"][0]["source_free_position_policy_ready"]
        )
        self.assertEqual(
            evidence["control_tranche"]["terminal_decision_counts"],
            {"ambiguous": 4, "mechanism_match": 8, "needs_review": 2},
        )
        self.assertEqual(
            evidence["control_tranche"]["source_free_sdr_akr_axis_ready_count"],
            0,
        )
        self.assertFalse(evidence["counterfamilies"]["baseline_superiority_claim"])
        self.assertTrue(
            evidence["external_deepening_context"][
                "q99504_current_countable_duplicate_closure_complete"
            ]
        )
        self.assertFalse(
            evidence["predictive_evidence_separation"][
                "source_active_site_annotations_counted_as_predictive_evidence"
            ]
        )
        self.assertFalse(packet["next_exact_experiment"]["decision_to_start_now"])
        self.assertTrue(
            packet["next_exact_experiment"]["selection_freeze_required_before_scoring"]
        )
        self.assertIn(
            "source active-site residue annotations",
            packet["next_exact_experiment"]["excluded_predictive_inputs"],
        )
        self.assertFalse(packet["safety_and_scope"]["label_import_attempted"])
        self.assertFalse(packet["safety_and_scope"]["production_fingerprint_added"])

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

    def test_remaining_metal_phosphatase_source_free_packet_closes_blockers(self) -> None:
        scores = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_remaining_source_free_geometry_scores_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_source_free_geometry_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_remaining_metal_source_free_geometry_20260521.json"
        )

        self.assertTrue(scores["metadata"]["review_only"])
        self.assertEqual(scores["metadata"]["candidate_count"], 3)
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 3)
        self.assertEqual(scores["metadata"]["text_or_label_fields_used_for_score_count"], 0)
        self.assertFalse(scores["metadata"]["ready_for_label_import"])
        self.assertFalse(scores["metadata"]["curated_label_registry_edited"])
        self.assertFalse(scores["metadata"]["fingerprint_registry_edited"])

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(packet["metadata"]["terminal_decision_counts"], {
            "mechanism_match_review_ready": 2,
            "terminal_rejection_duplicate_or_leakage": 1,
        })
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 0)
        for row_id in ("uniprot:P75792", "uniprot:P0A8Y5"):
            self.assertEqual(rows[row_id]["terminal_decision"], "mechanism_match_review_ready")
            self.assertEqual(rows[row_id]["exact_blocker_if_not_terminal"], None)
            self.assertTrue(
                rows[row_id]["current_geometry_retrieval_score_summary"][
                    "target_lane_at_or_above_floor"
                ]
            )
            self.assertFalse(
                rows[row_id]["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
            )
            self.assertEqual(
                rows[row_id]["duplicate_leakage_screen"][
                    "current_countable_high_tm_hit_count"
                ],
                0,
            )
            self.assertEqual(
                rows[row_id]["catalytic_residue_metal_phosphate_evidence"][
                    "phosphate_like_site_count"
                ],
                0,
            )
        self.assertEqual(
            rows["uniprot:P77247"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )

        self.assertEqual(rollup["metadata"]["candidate_count"], 52)
        self.assertEqual(rollup["metadata"]["terminal_decision_counts"], {
            "mechanism_match_review_ready": 3,
            "terminal_rejection_duplicate_or_leakage": 47,
            "terminal_rejection_insufficient_evidence": 2,
        })
        self.assertEqual(
            rollup["synthesis"]["needs_new_extractor_or_structure_candidate_count"], 0
        )
        self.assertFalse(rollup["metadata"]["ready_for_label_import"])

    def test_second_serine_hydrolase_packet_records_exact_duplicate_gate_blocker(self) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_serine_hydrolase_second_deep_packet_selection_20260521.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_packet_source_free_triad_scores_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_terminal_decision_packet_after_source_free_triad_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_packet_after_source_free_triad_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_serine_source_free_triad_20260521.json"
        )

        self.assertTrue(selection["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(selection["metadata"]["candidate_count"], 5)
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 4)
        self.assertEqual(scores["metadata"]["text_or_label_fields_used_for_score_count"], 0)
        self.assertEqual(
            scores["metadata"]["source_free_active_site_status_counts"],
            {
                "no_source_free_ser_his_acid_triad": 1,
                "ser_his_acid_triad_resolved": 4,
            },
        )
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 4,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 4)
        blocked_rows = [
            row
            for row in packet["rows"]
            if row["terminal_decision"] == "needs_new_extractor_or_structure"
        ]
        self.assertTrue(blocked_rows)
        self.assertTrue(
            all(
                row["exact_blocker_if_not_terminal"]
                == "bounded_current_countable_duplicate_leakage_screen_missing_for_second_serine_selection"
                for row in blocked_rows
            )
        )
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertFalse(
            benchmark["metrics"]["foldseek_current_countable_sidecar"]["available"]
        )
        self.assertEqual(rollup["metadata"]["candidate_count"], 57)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 3,
                "needs_new_extractor_or_structure": 4,
                "terminal_rejection_duplicate_or_leakage": 47,
                "terminal_rejection_insufficient_evidence": 3,
            },
        )
        self.assertEqual(rollup["synthesis"]["new_external_rows_frozen"], 0)

    def test_second_serine_targeted_screen_converts_blockers_to_duplicate_rejections(self) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_packet_targeted_current_ser_his_screen_20260521.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_terminal_decision_packet_after_targeted_ser_his_screen_20260521.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_second_deep_packet_after_targeted_ser_his_modern_baseline_benchmark_20260521.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_second_serine_targeted_screen_20260521.json"
        )

        self.assertEqual(screen["metadata"]["candidate_count"], 4)
        self.assertEqual(screen["metadata"]["status_counts"], {
            "current_ser_his_target_duplicate_signal": 4
        })
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(packet["metadata"]["terminal_decision_counts"], {
            "terminal_rejection_duplicate_or_leakage": 4,
            "terminal_rejection_insufficient_evidence": 1,
        })
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertTrue(
            all(row["exact_blocker_if_not_terminal"] is None for row in packet["rows"])
        )
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(rollup["metadata"]["candidate_count"], 57)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 3,
                "terminal_rejection_duplicate_or_leakage": 51,
                "terminal_rejection_insufficient_evidence": 3,
            },
        )
        self.assertEqual(
            rollup["synthesis"]["needs_new_extractor_or_structure_candidate_count"], 0
        )

    def test_third_serine_packet_deepens_remaining_frozen_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_serine_hydrolase_third_deep_packet_selection_20260522.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_packet_source_free_triad_scores_20260522.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_packet_targeted_current_ser_his_screen_20260522.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_terminal_decision_packet_after_targeted_ser_his_screen_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_packet_modern_baseline_benchmark_20260522.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_third_serine_targeted_screen_20260522.json"
        )
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_third_serine_20260522.json"
        )

        self.assertTrue(selection["metadata"]["candidate_selection_before_outcome_scoring"])
        self.assertEqual(selection["metadata"]["candidate_count"], 6)
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            {row["accession"] for row in selection["rows"]},
            {"Q9UL19", "P13001", "A0A0B5LB55", "F7IX06", "Q09LX1", "P15776"},
        )

        self.assertEqual(
            scores["metadata"]["source_free_active_site_status_counts"],
            {
                "no_source_free_ser_his_acid_triad": 1,
                "ser_his_acid_triad_resolved": 5,
            },
        )
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 5)
        self.assertEqual(scores["metadata"]["text_or_label_fields_used_for_score_count"], 0)

        self.assertEqual(screen["metadata"]["candidate_count"], 5)
        self.assertEqual(
            screen["metadata"]["status_counts"],
            {
                "current_ser_his_target_duplicate_signal": 4,
                "current_ser_his_target_screen_clear": 1,
            },
        )
        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 4,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 1)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])

        rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            rows["Q9UL19"]["terminal_decision"],
            "terminal_rejection_insufficient_evidence",
        )
        self.assertEqual(rows["P15776"]["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(
            rows["P15776"]["exact_blocker_if_not_terminal"],
            "full_current_countable_duplicate_leakage_screen_missing_for_third_serine_selection",
        )
        for accession in ("P13001", "A0A0B5LB55", "F7IX06", "Q09LX1"):
            self.assertEqual(
                rows[accession]["terminal_decision"],
                "terminal_rejection_duplicate_or_leakage",
            )
            self.assertGreater(
                rows[accession]["duplicate_leakage_screen"][
                    "current_ser_his_high_tm_hit_count"
                ],
                0,
            )
            self.assertFalse(
                rows[accession]["current_geometry_retrieval_score_summary"][
                    "text_or_label_fields_used_for_score"
                ]
            )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertFalse(benchmark["metrics"]["esm_sidecar_available"])
        self.assertEqual(benchmark["metrics"]["sequence_exact_current_reference_duplicate_count"], 0)
        self.assertEqual(benchmark["metrics"]["targeted_foldseek_high_tm_candidate_count"], 4)

        self.assertEqual(rollup["metadata"]["candidate_count"], 88)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 6,
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 77,
                "terminal_rejection_insufficient_evidence": 4,
            },
        )
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertEqual(readiness["registry_invariants"]["label_count"], 682)
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_seed_fingerprint_labels"],
            [],
        )
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )

    def test_third_serine_p15776_full_current_screen_closes_exact_blocker(self) -> None:
        screen = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_p15776_full_current_countable_duplicate_screen_20260522.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_terminal_decision_packet_after_p15776_full_current_screen_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_serine_hydrolase_third_deep_packet_after_p15776_full_current_modern_baseline_benchmark_20260522.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_decision_rollup_post_third_serine_full_current_20260522.json"
        )
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_third_serine_full_current_20260522.json"
        )

        self.assertEqual(screen["metadata"]["candidate_count"], 1)
        self.assertEqual(screen["metadata"]["target_subset_count"], 672)
        self.assertEqual(screen["metadata"]["high_tm_candidate_count"], 0)
        self.assertEqual(screen["metadata"]["max_current_countable_tm_score"], 0.626)
        row = screen["rows"][0]
        self.assertEqual(row["accession"], "P15776")
        self.assertEqual(row["current_countable_structural_screen_status"], "current_countable_screen_clear")
        self.assertTrue(row["pair_cache_complete"])
        self.assertEqual(row["current_countable_high_tm_hit_count"], 0)
        self.assertEqual(row["foldseek_run_status"], "completed")

        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 4,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        p15776 = next(row for row in packet["rows"] if row["accession"] == "P15776")
        self.assertEqual(p15776["terminal_decision"], "mechanism_match_review_ready")
        self.assertIsNone(p15776["exact_blocker_if_not_terminal"])
        self.assertEqual(
            p15776["duplicate_leakage_screen"]["current_countable_structural_screen_status"],
            "current_countable_screen_clear",
        )

        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertTrue(benchmark["metrics"]["full_current_countable_pair_cache_complete"])
        self.assertEqual(benchmark["metrics"]["full_current_countable_high_tm_candidate_count"], 0)
        self.assertEqual(
            benchmark["metrics"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 4,
                "terminal_rejection_insufficient_evidence": 1,
            },
        )

        self.assertEqual(rollup["metadata"]["candidate_count"], 88)
        self.assertEqual(rollup["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 7,
                "terminal_rejection_duplicate_or_leakage": 77,
                "terminal_rejection_insufficient_evidence": 4,
            },
        )
        self.assertEqual(
            rollup["synthesis"]["needs_new_extractor_or_structure_candidate_count"], 0
        )
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertEqual(readiness["metadata"]["needs_new_extractor_or_structure_count"], 0)
        self.assertEqual(readiness["registry_invariants"]["label_count"], 682)
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_seed_fingerprint_labels"],
            [],
        )

    def test_p15776_uniref_and_seven_review_ready_import_readiness_stay_closed(
        self,
    ) -> None:
        p15776_uniref = _load_json(
            ARTIFACTS / "v3_external_p15776_uniref_current_reference_screen_20260522.json"
        )
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_review_ready_import_gate_readiness_20260522.json"
        )

        self.assertTrue(p15776_uniref["metadata"]["review_only"])
        self.assertEqual(p15776_uniref["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(p15776_uniref["metadata"]["candidate_count"], 1)
        self.assertEqual(
            p15776_uniref["metadata"]["target_current_fingerprint_lane"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(
            p15776_uniref["metadata"]["current_countable_reference_entry_count"],
            682,
        )
        self.assertEqual(
            p15776_uniref["metadata"]["current_countable_reference_accession_count"],
            735,
        )
        self.assertEqual(p15776_uniref["metadata"]["fetched_uniref_cluster_count"], 2)
        self.assertEqual(p15776_uniref["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            p15776_uniref["metadata"]["uniref_current_reference_clear_count"], 1
        )
        self.assertEqual(
            p15776_uniref["metadata"][
                "uniref_current_reference_overlap_holdout_count"
            ],
            0,
        )
        row = p15776_uniref["rows"][0]
        self.assertEqual(row["accession"], "P15776")
        self.assertEqual(
            row["uniref_current_reference_screen_status"],
            "uniref_current_reference_screen_no_current_reference_overlap",
        )
        self.assertEqual(
            row["candidate_uniref90_ids"], ["UniRef90_P15776"]
        )
        self.assertEqual(
            row["candidate_uniref50_ids"], ["UniRef50_P15776"]
        )
        self.assertFalse(row["overlapping_current_reference_accessions"])
        self.assertFalse(row["source_context_counted_as_predictive"])
        self.assertIn(
            "mechanism_match_review_ready_is_not_label_import_ready",
            row["remaining_import_blockers"],
        )
        self.assertFalse(row["ready_for_label_import"])
        self.assertFalse(row["countable_label_candidate"])

        self.assertTrue(readiness["metadata"]["review_only"])
        self.assertEqual(readiness["metadata"]["candidate_count"], 7)
        self.assertEqual(readiness["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            readiness["metadata"]["target_current_fingerprint_lanes"],
            {
                "heme_peroxidase_oxidase": 4,
                "metal_dependent_hydrolase": 2,
                "ser_his_acid_hydrolase": 1,
            },
        )
        self.assertEqual(
            readiness["metadata"]["source_context_counted_as_predictive_count"], 0
        )
        self.assertEqual(readiness["metadata"]["source_free_geometry_above_floor_count"], 7)
        self.assertEqual(readiness["metadata"]["uniref_current_reference_clear_count"], 7)
        self.assertEqual(readiness["metadata"]["uniref_current_reference_missing_count"], 0)
        self.assertEqual(readiness["metadata"]["mechanism_match_review_ready_count"], 7)
        self.assertEqual(readiness["metadata"]["label_factory_payload_gate_count"], 21)
        self.assertEqual(readiness["metadata"]["label_factory_payload_gate_passed_count"], 20)
        self.assertEqual(
            readiness["metadata"]["label_factory_payload_gate_blockers"],
            ["applied_label_actions_ready"],
        )
        self.assertFalse(
            readiness["metadata"]["label_factory_payload_gate_rerun_for_seven_row_payload"]
        )
        self.assertEqual(readiness["metadata"]["external_source_transfer_gate_count"], 68)
        self.assertEqual(
            readiness["metadata"]["external_source_transfer_gate_passed_count"], 68
        )
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(readiness["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(readiness["metadata"]["curated_label_registry_edited"])
        self.assertFalse(readiness["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(readiness["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(readiness["metadata"]["removal_allowed_set_true"])
        self.assertEqual(readiness["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            readiness["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            readiness["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(readiness["metadata"]["external_imported_seed_fingerprint_labels"], [])
        self.assertEqual(
            readiness["metadata"]["remaining_import_blocker_counts"][
                "external_seed_fingerprint_payload_adapter_for_current_682_registry_required"
            ],
            7,
        )
        self.assertEqual(
            readiness["metadata"]["remaining_import_blocker_counts"][
                "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity"
            ],
            2,
        )
        self.assertEqual(
            readiness["decision"]["payload_gate_readiness_status"],
            "blocked_no_import",
        )
        self.assertIn(
            "P15776 now has UniRef90/50 current-reference clearance",
            readiness["decision"]["exact_gate_blocker"],
        )
        self.assertEqual(
            readiness["policy_preregistration"]["import_authorization"],
            "none_review_only_readiness_packet",
        )

        rows = {row["row_id"]: row for row in readiness["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P0A8Y5",
                "uniprot:P14532",
                "uniprot:P15776",
                "uniprot:P39597",
                "uniprot:P75792",
            },
        )
        p15776 = rows["uniprot:P15776"]
        self.assertEqual(
            p15776["draft_label_payload"]["fingerprint_id_if_ever_imported"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(
            p15776["duplicate_leakage_gate"]["uniref90_50_current_reference_status"],
            "uniref_current_reference_screen_no_current_reference_overlap",
        )
        self.assertEqual(
            p15776["duplicate_leakage_gate"]["current_countable_high_tm_hit_count"], 0
        )
        self.assertFalse(
            p15776["predictive_evidence_gate"]["text_or_label_fields_used_for_score"]
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in rows.values())
        )

    def test_external_seed_payload_currentregistry_gate_rerun_is_no_import(
        self,
    ) -> None:
        adapter = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_applied_labels_1000_currentregistry_payload_adapter.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_payload_gate_check_1000_currentregistry_adapter.json"
        )
        decision = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_payload_gate_rerun_no_import_decision_20260522.json"
        )

        self.assertEqual(adapter["metadata"]["input_label_count"], 682)
        self.assertEqual(adapter["metadata"]["output_label_count"], 682)
        self.assertEqual(
            adapter["metadata"]["output_summary"]["by_type"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            sorted(
                label["entry_id"]
                for label in adapter["labels"]
                if label["entry_id"].startswith("uniprot:")
            ),
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )

        self.assertEqual(gate["metadata"]["label_count"], 682)
        self.assertEqual(gate["metadata"]["gate_count"], 21)
        self.assertEqual(gate["metadata"]["passed_gate_count"], 21)
        self.assertFalse(gate["blockers"])
        self.assertTrue(gate["gates"]["applied_label_actions_ready"])
        self.assertTrue(gate["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(
            gate["metadata"]["artifact_lineage"]["artifact_paths"][
                "applied_label_factory"
            ],
            "artifacts/v3_external_seed_fingerprint_applied_labels_1000_currentregistry_payload_adapter.json",
        )

        metadata = decision["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(metadata["mechanism_match_review_ready_count"], 7)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(metadata["source_free_geometry_above_floor_count"], 7)
        self.assertEqual(metadata["uniref_current_reference_clear_count"], 7)
        self.assertEqual(metadata["applied_label_adapter_input_label_count"], 682)
        self.assertEqual(metadata["applied_label_adapter_output_label_count"], 682)
        self.assertEqual(metadata["label_factory_payload_gate_count"], 21)
        self.assertEqual(metadata["label_factory_payload_gate_passed_count"], 21)
        self.assertFalse(metadata["label_factory_payload_gate_blockers"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            metadata["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])
        self.assertNotIn(
            "external_seed_fingerprint_payload_adapter_for_current_682_registry_required",
            metadata["remaining_import_blocker_counts"],
        )
        self.assertNotIn(
            "label_factory_payload_gate_failed_applied_label_actions_ready",
            metadata["remaining_import_blocker_counts"],
        )
        self.assertEqual(
            metadata["remaining_import_blocker_counts"][
                "human_label_action_not_requested"
            ],
            7,
        )
        self.assertEqual(
            metadata["remaining_import_blocker_counts"][
                "mechanism_match_review_ready_is_not_label_import_ready"
            ],
            7,
        )
        self.assertEqual(
            metadata["remaining_import_blocker_counts"][
                "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity"
            ],
            2,
        )
        self.assertTrue(all(decision["invariant_checks"].values()))
        self.assertEqual(
            decision["decision"]["payload_adapter_blocker_status"],
            "resolved_for_current_682_no_import_gate_rerun",
        )
        self.assertEqual(
            decision["decision"]["payload_gate_dry_run_status"],
            "passed_no_import_gate_only",
        )
        self.assertFalse(decision["decision"]["label_import_authorized"])
        self.assertFalse(decision["decision"]["registry_or_fingerprint_change_authorized"])

        rows = {row["row_id"]: row for row in decision["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P0A8Y5",
                "uniprot:P14532",
                "uniprot:P15776",
                "uniprot:P39597",
                "uniprot:P75792",
            },
        )
        self.assertTrue(
            all(
                row["full_label_factory_payload_gate"]["status"]
                == "passed_currentregistry_adapter_no_import"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in rows.values())
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P0A8Y5"]["remaining_import_blockers"],
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P75792"]["remaining_import_blockers"],
        )
        self.assertNotIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P15776"]["remaining_import_blockers"],
        )

    def test_nonmetal_review_ready_packet_is_human_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_nonmetal_human_review_packet_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["source_candidate_count"], 7)
        self.assertEqual(packet["metadata"]["candidate_count"], 5)
        self.assertEqual(packet["metadata"]["excluded_metal_specificity_blocked_count"], 2)
        self.assertEqual(
            packet["metadata"]["target_current_fingerprint_lanes"],
            {"heme_peroxidase_oxidase": 4, "ser_his_acid_hydrolase": 1},
        )
        self.assertEqual(
            packet["metadata"]["source_context_counted_as_predictive_count"], 0
        )
        self.assertEqual(packet["metadata"]["source_free_geometry_above_floor_count"], 5)
        self.assertEqual(packet["metadata"]["uniref_current_reference_clear_count"], 5)
        self.assertEqual(packet["metadata"]["label_factory_payload_gate_count"], 21)
        self.assertEqual(packet["metadata"]["label_factory_payload_gate_passed_count"], 21)
        self.assertFalse(packet["metadata"]["label_factory_payload_gate_blockers"])
        self.assertEqual(packet["metadata"]["ready_for_human_review_count"], 5)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["human_label_action_requested"])
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertEqual(packet["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            packet["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            packet["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(packet["metadata"]["external_imported_seed_fingerprint_labels"], [])
        self.assertTrue(all(packet["invariant_checks"].values()))
        self.assertEqual(
            packet["decision"]["packet_status"],
            "nonmetal_human_review_ready_but_no_import_authorized",
        )
        self.assertFalse(packet["decision"]["label_import_authorized"])
        self.assertFalse(packet["decision"]["registry_or_fingerprint_change_authorized"])

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P15776",
                "uniprot:P39597",
            },
        )
        self.assertTrue(
            all(
                row["review_packet_status"] == "human_review_ready_not_import_ready"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["terminal_decision"] == "mechanism_match_review_ready"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["label_factory_payload_gate"]["status"]
                == "passed_currentregistry_adapter_no_import"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["source_free_predictive_evidence"][
                    "text_or_label_fields_used_for_score"
                ]
                is False
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in rows.values())
        )

    def test_seven_row_post_gate_benchmark_makes_no_superiority_claim(self) -> None:
        benchmark = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_post_gate_modern_baseline_benchmark_20260522.json"
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertEqual(benchmark["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(benchmark["metadata"]["candidate_count"], 7)
        self.assertEqual(
            benchmark["metadata"]["target_current_fingerprint_lanes"],
            {
                "heme_peroxidase_oxidase": 4,
                "metal_dependent_hydrolase": 2,
                "ser_his_acid_hydrolase": 1,
            },
        )
        self.assertEqual(
            benchmark["metadata"]["source_context_counted_as_predictive_count"], 0
        )
        self.assertEqual(benchmark["metadata"]["geometry_available_count"], 7)
        self.assertEqual(benchmark["metadata"]["geometry_above_floor_count"], 7)
        self.assertEqual(
            benchmark["metadata"]["deterministic_sequence_baseline_available_count"],
            7,
        )
        self.assertEqual(benchmark["metadata"]["uniref_current_reference_clear_count"], 7)
        self.assertEqual(benchmark["metadata"]["foldseek_tm_screen_available_count"], 7)
        self.assertEqual(benchmark["metadata"]["foldseek_duplicate_clear_count"], 7)
        self.assertEqual(
            benchmark["metadata"]["esm_or_learned_embedding_sidecar_available_count"],
            0,
        )
        self.assertFalse(benchmark["metadata"]["geometry_superiority_claim"])
        self.assertFalse(benchmark["metadata"]["ready_for_label_import"])
        self.assertEqual(benchmark["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(benchmark["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(benchmark["metrics"]["geometry_above_floor_fraction"], 1.0)
        self.assertEqual(
            benchmark["metrics"]["uniref_current_reference_clear_fraction"], 1.0
        )
        self.assertEqual(benchmark["metrics"]["foldseek_duplicate_clear_fraction"], 1.0)
        self.assertEqual(benchmark["metrics"]["esm_sidecar_available_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["import_ready_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["countable_label_candidate_fraction"], 0.0)
        self.assertFalse(
            benchmark["baseline_comparisons"]["ec_keyword_routing"][
                "counted_as_predictive_evidence"
            ]
        )
        self.assertFalse(
            benchmark["baseline_comparisons"][
                "deterministic_sequence_or_kmer_nearest_neighbor"
            ]["counted_as_predictive_evidence"]
        )
        self.assertTrue(benchmark["baseline_comparisons"]["foldseek_tm_screen"]["available"])
        self.assertFalse(
            benchmark["baseline_comparisons"]["esm_or_learned_embedding_sidecar"][
                "available"
            ]
        )
        self.assertFalse(
            benchmark["baseline_comparisons"]["geometry_retrieval"].get(
                "superiority_claim", False
            )
        )

        rows = {row["row_id"]: row for row in benchmark["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P0A8Y5",
                "uniprot:P14532",
                "uniprot:P15776",
                "uniprot:P39597",
                "uniprot:P75792",
            },
        )
        self.assertTrue(
            all(
                row["current_geometry_retrieval_triage"][
                    "text_or_label_fields_used_for_score"
                ]
                is False
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                not row["ec_keyword_routing_baseline"][
                    "counted_as_predictive_evidence"
                ]
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["esm_or_learned_embedding_sidecar"]["available"] is False
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )

    def test_external_deep_terminal_import_gate_readiness_stays_closed(self) -> None:
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_second_serine_20260521.json"
        )

        self.assertTrue(readiness["metadata"]["review_only"])
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertFalse(readiness["metadata"]["curated_label_registry_edited"])
        self.assertFalse(readiness["metadata"]["fingerprint_registry_edited"])
        self.assertEqual(readiness["metadata"]["candidate_count"], 57)
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(readiness["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(readiness["registry_invariants"]["label_count"], 682)
        self.assertEqual(
            readiness["registry_invariants"]["label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_seed_fingerprint_labels"],
            [],
        )
        self.assertTrue(all(readiness["invariant_checks"].values()))
        self.assertEqual(
            readiness["import_gate_readiness"]["status"],
            "blocked_no_import_ready_candidates",
        )
        self.assertEqual(
            readiness["import_gate_readiness"]["decision"],
            "do_not_import_any_current_deep_packet_candidate",
        )
        self.assertTrue(
            readiness["import_gate_readiness"][
                "mechanism_match_review_ready_is_not_import_ready"
            ]
        )

    def test_external_deep_terminal_import_gate_readiness_post_second_heme_stays_closed(
        self,
    ) -> None:
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_second_heme_20260521.json"
        )

        self.assertTrue(readiness["metadata"]["review_only"])
        self.assertFalse(readiness["metadata"]["ready_for_label_import"])
        self.assertFalse(readiness["metadata"]["curated_label_registry_edited"])
        self.assertFalse(readiness["metadata"]["fingerprint_registry_edited"])
        self.assertEqual(readiness["metadata"]["candidate_count"], 71)
        self.assertEqual(readiness["metadata"]["deep_packet_count"], 11)
        self.assertEqual(readiness["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(readiness["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(readiness["metadata"]["exact_blocker_candidate_count"], 3)
        self.assertEqual(
            readiness["metadata"]["needs_new_extractor_or_structure_candidate_count"],
            3,
        )
        self.assertEqual(
            readiness["registry_invariants"]["label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            readiness["registry_invariants"]["external_imported_seed_fingerprint_labels"],
            [],
        )
        self.assertTrue(all(readiness["invariant_checks"].values()))
        self.assertEqual(
            readiness["import_gate_readiness"]["status"],
            "blocked_no_import_ready_candidates",
        )
        self.assertEqual(
            readiness["import_gate_readiness"]["decision"],
            "do_not_import_any_current_deep_packet_candidate",
        )
        self.assertIn(
            "three_second_heme_targeted_clear_rows_need_full_current_countable_duplicate_screen",
            readiness["import_gate_readiness"]["blockers"],
        )
        second_heme = {
            row["lane_id"]: row for row in readiness["lane_summaries"]
        }["heme_peroxidase_oxidase_second_selection_after_targeted_heme_screen"]
        self.assertEqual(
            second_heme["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 3,
                "terminal_rejection_duplicate_or_leakage": 4,
            },
        )
        self.assertEqual(second_heme["exact_blocker_candidate_count"], 3)
        self.assertEqual(
            second_heme["exact_blocker"],
            "full_current_countable_duplicate_screen_missing_after_targeted_current_heme_screen",
        )

    def test_mechanism_match_review_ready_import_blocker_matrix_stays_review_only(
        self,
    ) -> None:
        matrix = _load_json(
            ARTIFACTS
            / "v3_external_mechanism_match_review_ready_import_blocker_matrix_20260522.json"
        )

        self.assertTrue(matrix["metadata"]["review_only"])
        self.assertEqual(matrix["metadata"]["candidate_count"], 5)
        self.assertEqual(matrix["metadata"]["new_external_rows_frozen"], 0)
        self.assertFalse(matrix["metadata"]["ready_for_label_import"])
        self.assertEqual(matrix["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(
            matrix["metadata"]["target_current_fingerprint_lanes"],
            {"heme_peroxidase_oxidase": 3, "metal_dependent_hydrolase": 2},
        )
        self.assertEqual(
            matrix["registry_invariants"]["label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            matrix["registry_invariants"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertTrue(all(matrix["invariant_checks"].values()))
        self.assertEqual(
            {row["terminal_decision"] for row in matrix["rows"]},
            {"mechanism_match_review_ready"},
        )
        self.assertTrue(
            all(
                "full_label_factory_import_payload_not_constructed_or_gated"
                in row["import_gate_blockers"]
                for row in matrix["rows"]
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in matrix["rows"])
        )

    def test_epk_post_late_decision_synthesis_keeps_main_loop_off_epk(self) -> None:
        synthesis = _load_json(
            ARTIFACTS / "v3_epk_post_late_decision_synthesis_20260522.json"
        )

        self.assertTrue(synthesis["metadata"]["review_only"])
        self.assertFalse(synthesis["metadata"]["main_loop_should_continue_epk_by_default"])
        self.assertFalse(synthesis["metadata"]["production_scoring_authorized"])
        self.assertFalse(synthesis["metadata"]["ready_for_label_import"])
        self.assertFalse(synthesis["metadata"]["ready_to_expand_positive_fingerprint_universe"])
        self.assertEqual(synthesis["metadata"]["lane_count"], 5)
        self.assertEqual(
            synthesis["synthesis_conclusion"]["five_uj7_status"],
            "pinned_as_biological_assembly_1_context_v4_only_split_failure",
        )
        self.assertEqual(
            synthesis["synthesis_conclusion"]["eight_uyh_status"],
            "review_only_clean_active_state_candidate_for_policy_harness_adjudication",
        )
        self.assertEqual(
            {row["lane_id"] for row in synthesis["lane_findings"]},
            {
                "epk_false_positive_hunter",
                "epk_policy_harness",
                "epk_positive_evidence",
                "epk_sibling_controls",
                "epk_substrate_role_identity",
            },
        )
        self.assertTrue(
            all(value is False for value in synthesis["safety_rails"].values())
        )

    def test_review_ready_uniref_payload_plan_remains_non_importing(self) -> None:
        plan = _load_json(
            ARTIFACTS
            / "v3_external_mechanism_match_review_ready_uniref_payload_plan_20260522.json"
        )

        self.assertTrue(plan["metadata"]["review_only"])
        self.assertEqual(plan["metadata"]["candidate_count"], 5)
        self.assertEqual(plan["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(plan["metadata"]["uniref_current_reference_clear_count"], 5)
        self.assertEqual(plan["metadata"]["uniref_current_reference_overlap_holdout_count"], 0)
        self.assertEqual(plan["metadata"]["uniref_current_reference_incomplete_count"], 0)
        self.assertEqual(plan["metadata"]["fetch_failure_count"], 0)
        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            plan["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            plan["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            {row["uniref_current_reference_screen_status"] for row in plan["rows"]},
            {"uniref_current_reference_screen_no_current_reference_overlap"},
        )
        self.assertTrue(
            all(not row["uniref_current_reference_blockers"] for row in plan["rows"])
        )
        self.assertTrue(
            all(
                "full_label_factory_gate_not_run" in row["remaining_import_blockers"]
                for row in plan["rows"]
            )
        )
        self.assertTrue(
            all(
                row["label_factory_payload_plan"]["predictive_evidence"][
                    "source_context_counted_as_predictive"
                ]
                is False
                for row in plan["rows"]
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in plan["rows"])
        )

    def test_heme_third_sequence_duplicate_closure_packet_is_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_third_deep_packet_sequence_duplicate_closure_modern_baseline_benchmark_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["candidate_count"], 5)
        self.assertEqual(packet["metadata"]["duplicate_or_leakage_rejection_count"], 4)
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 1)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 1,
                "terminal_rejection_duplicate_or_leakage": 4,
            },
        )
        rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
            },
            {"P00431", "P04963", "P21179", "P48534"},
        )
        self.assertEqual(
            rows["P14532"]["terminal_decision"],
            "needs_new_extractor_or_structure",
        )
        self.assertIn(
            "source_free_heme_active_site_geometry_scoring",
            rows["P14532"]["exact_blocker_if_not_terminal_import_ready"],
        )
        self.assertTrue(
            all(
                row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
                is False
                for row in packet["rows"]
            )
        )
        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["rows_closed_by_exact_sequence_duplicate"], 4
        )
        self.assertEqual(benchmark["metrics"]["rows_with_precise_remaining_blocker"], 1)
        self.assertFalse(
            benchmark["baseline_comparisons"]["current_geometry_retrieval"][
                "available"
            ]
        )
        self.assertFalse(
            benchmark["baseline_comparisons"]["esm_or_learned_embedding_sidecar"][
                "available"
            ]
        )

    def test_fdr_third_sequence_duplicate_closure_packet_is_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_flavin_dehydrogenase_third_deep_packet_sequence_duplicate_closure_modern_baseline_benchmark_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["candidate_count"], 6)
        self.assertEqual(packet["metadata"]["duplicate_or_leakage_rejection_count"], 4)
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 2)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "needs_new_extractor_or_structure": 2,
                "terminal_rejection_duplicate_or_leakage": 4,
            },
        )
        rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
            },
            {"P0AEZ1", "P15559", "P38489", "P42593"},
        )
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "needs_new_extractor_or_structure"
            },
            {"P32340", "P33371"},
        )
        self.assertTrue(
            all(
                "source_free_flavin_dehydrogenase_active_site_geometry_scoring"
                in rows[accession]["exact_blocker_if_not_terminal_import_ready"]
                for accession in ["P32340", "P33371"]
            )
        )
        self.assertTrue(
            all(
                row["predictive_evidence"][
                    "ec_keyword_protein_name_counted_as_predictive_evidence"
                ]
                is False
                for row in packet["rows"]
            )
        )
        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(
            benchmark["metrics"]["rows_closed_by_exact_sequence_duplicate"], 4
        )
        self.assertEqual(benchmark["metrics"]["rows_with_precise_remaining_blocker"], 2)
        self.assertFalse(
            benchmark["baseline_comparisons"]["current_geometry_retrieval"][
                "available"
            ]
        )
        self.assertFalse(
            benchmark["baseline_comparisons"]["foldseek_tm_screen"]["available"]
        )

    def test_external_deep_remaining_blocker_queue_is_non_importing(self) -> None:
        queue = _load_json(
            ARTIFACTS / "v3_external_deep_remaining_blocker_queue_20260522.json"
        )

        self.assertTrue(queue["metadata"]["review_only"])
        self.assertEqual(queue["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(queue["metadata"]["candidate_count"], 8)
        self.assertEqual(queue["metadata"]["review_ready_import_gate_blocker_count"], 5)
        self.assertEqual(
            queue["metadata"]["source_free_geometry_or_structure_blocker_count"], 3
        )
        self.assertFalse(queue["metadata"]["ready_for_label_import"])
        self.assertEqual(queue["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(queue["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(queue["metadata"]["curated_label_registry_edited"])
        self.assertFalse(queue["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(queue["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(queue["metadata"]["removal_allowed_set_true"])

        blocker_classes = {row["blocker_class"]: row for row in queue["blocker_classes"]}
        self.assertEqual(
            set(blocker_classes),
            {
                "review_ready_import_gate_blocker",
                "source_free_geometry_or_structure_blocker",
            },
        )
        self.assertIn(
            "full_label_factory_payload_gate_not_run",
            blocker_classes["review_ready_import_gate_blocker"]["exact_missing_evidence"],
        )
        self.assertIn(
            "source_free_active_site_geometry_score_missing",
            blocker_classes["source_free_geometry_or_structure_blocker"][
                "exact_missing_evidence"
            ],
        )
        self.assertIn(
            "coordinate_sidecar_materialization_missing_for_blocker_rows",
            blocker_classes["source_free_geometry_or_structure_blocker"][
                "exact_missing_evidence"
            ],
        )

        rows = {row["row_id"]: row for row in queue["rows"]}
        self.assertEqual(
            {
                row_id
                for row_id, row in rows.items()
                if row["blocker_class"] == "source_free_geometry_or_structure_blocker"
            },
            {"uniprot:P14532", "uniprot:P33371", "uniprot:P32340"},
        )
        self.assertEqual(
            {
                row["structure_sidecar_status"]
                for row in queue["rows"]
                if row["blocker_class"] == "source_free_geometry_or_structure_blocker"
            },
            {"not_staged_in_existing_deep_packet_coordinate_dirs"},
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in queue["rows"])
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in queue["rows"])
        )
        self.assertTrue(
            all(
                "source_prose" in row["review_context_excluded_from_predictive_evidence"]
                for row in queue["rows"]
            )
        )
        self.assertTrue(queue["next_main_loop_recommendation"]["do_not_add_broad_external_rows"])

    def test_redox_third_blocker_terminal_packet_is_source_separated(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_redox_third_blocker_terminal_decision_packet_after_source_free_geometry_and_screens_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_external_redox_third_blocker_modern_baseline_benchmark_20260522.json"
        )
        full_current = _load_json(
            ARTIFACTS
            / "v3_heme_peroxidase_p14532_full_current_countable_duplicate_screen_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_external_deep_remaining_blocker_queue_post_redox_third_closure_20260522.json"
        )
        readiness = _load_json(
            ARTIFACTS
            / "v3_external_deep_terminal_import_gate_readiness_check_post_redox_third_closure_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["candidate_count"], 3)
        self.assertTrue(packet["metadata"]["source_separation_enforced"])
        self.assertEqual(packet["metadata"]["source_free_active_site_ready_count"], 3)
        self.assertEqual(packet["metadata"]["target_lane_at_or_above_floor_count"], 3)
        self.assertEqual(packet["metadata"]["full_current_countable_duplicate_clear_count"], 1)
        self.assertEqual(packet["metadata"]["targeted_current_lane_high_tm_candidate_count"], 2)
        self.assertEqual(packet["metadata"]["duplicate_or_leakage_rejection_count"], 2)
        self.assertEqual(packet["metadata"]["exact_blocker_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 1,
                "terminal_rejection_duplicate_or_leakage": 2,
            },
        )

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), {"uniprot:P14532", "uniprot:P33371", "uniprot:P32340"})
        self.assertEqual(
            rows["uniprot:P14532"]["terminal_decision"],
            "mechanism_match_review_ready",
        )
        self.assertIn(
            "full_label_factory_gate_not_run",
            rows["uniprot:P14532"]["exact_blocker_if_not_terminal_import_ready"],
        )
        self.assertTrue(
            rows["uniprot:P14532"]["duplicate_leakage_screen"][
                "full_current_countable"
            ]["duplicate_clear_established"]
        )
        self.assertEqual(
            rows["uniprot:P33371"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertEqual(
            rows["uniprot:P32340"]["terminal_decision"],
            "terminal_rejection_duplicate_or_leakage",
        )
        self.assertTrue(
            all(
                row["catalytic_residue_metal_or_cofactor_evidence"][
                    "text_or_label_fields_used_for_score"
                ]
                is False
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["current_geometry_retrieval_score_summary"][
                    "target_lane_at_or_above_floor"
                ]
                for row in rows.values()
            )
        )
        self.assertEqual(
            {
                row_id
                for row_id, row in rows.items()
                if row["duplicate_leakage_screen"]["targeted_current_lane"]["status"]
                == "current_lane_structural_duplicate_signal"
            },
            {"uniprot:P33371", "uniprot:P32340"},
        )
        self.assertTrue(full_current["metadata"]["pair_cache_complete"])
        self.assertEqual(full_current["metadata"]["unique_query_target_pair_count"], 672)
        self.assertLess(
            full_current["metadata"]["max_external_vs_current_countable_tm_score"],
            0.7,
        )

        self.assertTrue(benchmark["metadata"]["review_only"])
        self.assertFalse(benchmark["metadata"]["superiority_claim_permitted"])
        self.assertEqual(benchmark["metrics"]["source_free_geometry_scored_count"], 3)
        self.assertEqual(benchmark["metrics"]["targeted_foldseek_current_lane_high_tm_candidate_count"], 2)
        self.assertEqual(benchmark["metrics"]["full_current_countable_duplicate_clear_candidate_count"], 1)
        self.assertEqual(benchmark["metrics"]["deterministic_sequence_exact_duplicate_count"], 0)
        self.assertTrue(
            benchmark["baseline_comparisons"]["current_geometry_retrieval"][
                "available"
            ]
        )
        self.assertTrue(
            benchmark["baseline_comparisons"]["foldseek_tm_screen"]["available"]
        )
        self.assertFalse(
            benchmark["baseline_comparisons"]["esm_or_learned_embedding_sidecar"][
                "available"
            ]
        )
        self.assertEqual(
            queue["metadata"]["source_free_geometry_or_structure_blocker_count"], 0
        )
        self.assertEqual(queue["metadata"]["review_ready_import_gate_blocker_count"], 5)
        self.assertEqual(readiness["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            readiness["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            readiness["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertTrue(all(readiness["invariant_checks"].values()))

    def test_review_ready_seed_fingerprint_payload_dry_run_is_blocked(self) -> None:
        dry_run = _load_json(
            ARTIFACTS
            / "v3_external_mechanism_match_review_ready_seed_fingerprint_payload_dry_run_20260522.json"
        )

        self.assertTrue(dry_run["metadata"]["review_only"])
        self.assertEqual(dry_run["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(dry_run["metadata"]["candidate_count"], 6)
        self.assertEqual(
            dry_run["metadata"]["target_current_fingerprint_lanes"],
            {"heme_peroxidase_oxidase": 4, "metal_dependent_hydrolase": 2},
        )
        self.assertEqual(
            dry_run["metadata"]["source_context_counted_as_predictive_count"], 0
        )
        self.assertEqual(dry_run["metadata"]["uniref_current_reference_clear_count"], 6)
        self.assertEqual(dry_run["metadata"]["uniref_current_reference_missing_count"], 0)
        self.assertFalse(dry_run["metadata"]["ready_for_label_import"])
        self.assertEqual(dry_run["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(dry_run["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(dry_run["metadata"]["curated_label_registry_edited"])
        self.assertFalse(dry_run["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(dry_run["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(dry_run["metadata"]["removal_allowed_set_true"])
        self.assertEqual(dry_run["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            dry_run["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            dry_run["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(dry_run["decision"]["payload_dry_run_status"], "blocked_no_import")

        rows = {row["row_id"]: row for row in dry_run["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P0A8Y5",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P75792",
            },
        )
        self.assertEqual(
            rows["uniprot:P14532"]["import_gate_evidence"][
                "uniref90_50_current_reference_status"
            ],
            "uniref_current_reference_screen_no_current_reference_overlap",
        )
        self.assertNotIn(
            "p14532_uniref90_50_current_reference_screen_not_run",
            rows["uniprot:P14532"]["remaining_import_blockers"],
        )
        self.assertTrue(
            all(
                row["draft_label_payload"]["payload_status"]
                == "draft_review_only_not_imported"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["draft_label_payload"]["label_type_if_ever_imported"]
                == "seed_fingerprint"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in rows.values())
        )

        p14532_uniref = _load_json(
            ARTIFACTS / "v3_external_p14532_uniref_current_reference_screen_20260522.json"
        )
        self.assertTrue(p14532_uniref["metadata"]["review_only"])
        self.assertEqual(
            p14532_uniref["metadata"]["uniref_current_reference_clear_count"], 1
        )
        self.assertEqual(
            p14532_uniref["rows"][0]["uniref_current_reference_screen_status"],
            "uniref_current_reference_screen_no_current_reference_overlap",
        )
        self.assertFalse(p14532_uniref["rows"][0]["overlapping_current_reference_accessions"])

    def test_external_seed_fingerprint_payload_gate_dry_run_has_exact_blocker(
        self,
    ) -> None:
        gate_check = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_label_factory_payload_gate_check_20260522.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_policy_preregistration_and_payload_gate_dry_run_20260522.json"
        )

        self.assertEqual(gate_check["metadata"]["gate_count"], 21)
        self.assertEqual(gate_check["metadata"]["passed_gate_count"], 20)
        self.assertEqual(gate_check["blockers"], ["applied_label_actions_ready"])

        self.assertTrue(dry_run["metadata"]["review_only"])
        self.assertEqual(dry_run["metadata"]["new_external_rows_frozen"], 0)
        self.assertTrue(dry_run["metadata"]["policy_preregistered"])
        self.assertFalse(dry_run["metadata"]["policy_authorizes_import_in_this_run"])
        self.assertEqual(dry_run["metadata"]["candidate_count"], 6)
        self.assertEqual(dry_run["metadata"]["source_free_geometry_above_floor_count"], 6)
        self.assertEqual(dry_run["metadata"]["uniref_current_reference_clear_count"], 6)
        self.assertEqual(dry_run["metadata"]["label_factory_payload_gate_count"], 21)
        self.assertEqual(dry_run["metadata"]["label_factory_payload_gate_passed_count"], 20)
        self.assertEqual(
            dry_run["metadata"]["label_factory_payload_gate_blockers"],
            ["applied_label_actions_ready"],
        )
        self.assertEqual(dry_run["metadata"]["external_source_transfer_gate_count"], 68)
        self.assertEqual(
            dry_run["metadata"]["external_source_transfer_gate_passed_count"], 68
        )
        self.assertFalse(dry_run["metadata"]["external_source_transfer_gate_blockers"])
        self.assertFalse(dry_run["metadata"]["ready_for_label_import"])
        self.assertEqual(dry_run["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(dry_run["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(dry_run["metadata"]["curated_label_registry_edited"])
        self.assertFalse(dry_run["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(dry_run["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(dry_run["metadata"]["removal_allowed_set_true"])
        self.assertEqual(dry_run["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            dry_run["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            dry_run["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(dry_run["metadata"]["external_imported_seed_fingerprint_labels"], [])

        self.assertEqual(
            dry_run["decision"]["payload_gate_dry_run_status"], "blocked_no_import"
        )
        self.assertEqual(
            dry_run["decision"]["full_label_factory_payload_gate_dry_run_status"],
            "failed_with_exact_registry_adapter_blocker",
        )
        self.assertIn(
            "external seed-fingerprint payload adapter",
            dry_run["decision"]["exact_gate_blocker"],
        )
        self.assertTrue(
            any(
                "full label-factory payload gate passes against the current 682-label registry"
                in gate
                for gate in dry_run["policy_preregistration"][
                    "required_pre_count_gates"
                ]
            )
        )
        self.assertEqual(
            dry_run["policy_preregistration"]["import_authorization"],
            "none_review_only_dry_run",
        )

        rows = {row["row_id"]: row for row in dry_run["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P0A8Y5",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P75792",
            },
        )
        self.assertTrue(
            all(
                row["predictive_evidence_gate"]["text_or_label_fields_used_for_score"]
                is False
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["full_label_factory_payload_gate"]["status"]
                == "failed_exact_adapter_blocker"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in rows.values())
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P0A8Y5"]["remaining_import_blockers"],
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P75792"]["remaining_import_blockers"],
        )

    def test_metal_review_ready_phosphate_specificity_blocker_is_exact(
        self,
    ) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_metal_phosphatase_review_ready_phosphate_specificity_blocker_packet_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertTrue(
            packet["metadata"]["candidate_selection_frozen_before_outcome_scoring"]
        )
        self.assertEqual(packet["metadata"]["candidate_count"], 2)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 2)
        self.assertEqual(
            packet["metadata"]["blocked_with_exact_missing_evidence_count"], 2
        )
        self.assertEqual(packet["metadata"]["source_free_phosphate_specificity_ready_count"], 0)
        self.assertEqual(packet["metadata"]["phosphate_like_site_count_total"], 0)
        self.assertEqual(
            packet["metadata"]["source_context_counted_as_predictive_count"], 0
        )
        self.assertEqual(
            packet["metadata"]["text_or_label_fields_used_for_predictive_score_count"],
            0,
        )
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertEqual(packet["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            packet["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            packet["decision"]["packet_status"],
            "phosphatase_specific_import_blocked_with_exact_missing_evidence",
        )

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), {"uniprot:P0A8Y5", "uniprot:P75792"})
        self.assertTrue(
            all(
                row["phosphatase_specific_import_status"]
                == "blocked_with_exact_missing_evidence"
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                row["current_geometry_retrieval_score_summary"][
                    "target_lane_at_or_above_floor"
                ]
                for row in rows.values()
            )
        )
        self.assertTrue(
            all(
                not row["source_free_phosphate_specificity_scan"][
                    "source_free_phosphate_or_substrate_ligand_detected"
                ]
                for row in rows.values()
            )
        )
        self.assertIn(
            "coordinate holo structure or alternate structure with a phosphate-like substrate/product/transition-state analog within the source-free metal active-site radius",
            rows["uniprot:P0A8Y5"]["exact_missing_evidence_to_resolve"],
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P75792"]["remaining_import_blockers"],
        )

    def test_metal_phosphatase_phosphate_specificity_blocker_packet(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_metal_phosphatase_review_ready_phosphate_specificity_blocker_packet_20260522.json"
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["candidate_count"], 2)
        self.assertEqual(packet["metadata"]["structure_scan_count"], 5)
        self.assertEqual(packet["metadata"]["committed_coordinate_sidecar_count"], 2)
        self.assertEqual(packet["metadata"]["rcsb_fetch_for_review_scan_not_saved_count"], 3)
        self.assertEqual(packet["metadata"]["phosphate_like_site_count_total"], 0)
        self.assertEqual(packet["metadata"]["structures_with_phosphate_like_ligand_count"], 0)
        self.assertEqual(packet["metadata"]["source_free_phosphate_specificity_ready_count"], 0)
        self.assertEqual(packet["metadata"]["blocked_with_exact_missing_evidence_count"], 2)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 2)
        self.assertEqual(packet["metadata"]["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(
            packet["metadata"]["text_or_label_fields_used_for_predictive_score_count"],
            0,
        )
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["geometry_superiority_claim"])
        self.assertEqual(packet["metadata"]["esm_sidecar_available_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertEqual(packet["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            packet["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            packet["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(packet["metadata"]["external_imported_seed_fingerprint_labels"], [])
        self.assertEqual(
            packet["decision"]["packet_status"],
            "phosphatase_specific_import_blocked_with_exact_missing_evidence",
        )
        self.assertFalse(packet["decision"]["label_import_authorized"])
        self.assertFalse(packet["decision"]["registry_or_fingerprint_change_authorized"])

        rows = {row["row_id"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), {"uniprot:P0A8Y5", "uniprot:P75792"})
        self.assertEqual(
            rows["uniprot:P75792"]["source_free_phosphate_specificity_scan"][
                "pdb_ids_scanned"
            ],
            ["1RLM", "1RLO", "1RLT", "2HF2"],
        )
        self.assertEqual(
            rows["uniprot:P0A8Y5"]["source_free_phosphate_specificity_scan"][
                "pdb_ids_scanned"
            ],
            ["1RKQ"],
        )
        for row in rows.values():
            self.assertEqual(row["terminal_decision"], "mechanism_match_review_ready")
            self.assertEqual(
                row["phosphatase_specific_import_status"],
                "blocked_with_exact_missing_evidence",
            )
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(
                row["source_free_phosphate_specificity_scan"][
                    "source_free_phosphate_or_substrate_ligand_detected"
                ]
            )
            self.assertEqual(
                row["source_free_phosphate_specificity_scan"][
                    "phosphate_like_site_count_total"
                ],
                0,
            )
            self.assertIn(
                "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
                row["remaining_import_blockers"],
            )
            self.assertTrue(
                any(
                    "coordinate holo structure" in missing
                    for missing in row["exact_missing_evidence_to_resolve"]
                )
            )
            self.assertEqual(
                row["modern_baseline_comparison"]["superiority_claim"], "none"
            )
            self.assertFalse(
                row["modern_baseline_comparison"]["esm_sidecar"]["available"]
            )
            for scan in row["source_free_phosphate_specificity_scan"]["structure_scans"]:
                self.assertEqual(scan["phosphate_like_site_count"], 0)
                self.assertFalse(scan["selected_site_phosphate_like_ligand_detected"])
                self.assertFalse(scan["text_or_label_fields_used_for_predictive_score"])

    def test_seven_row_seed_payload_adapter_and_human_packet_are_no_import(
        self,
    ) -> None:
        decision = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_payload_gate_rerun_no_import_decision_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_payload_gate_check_1000_currentregistry_adapter.json"
        )
        human_packet = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_nonmetal_human_review_packet_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_seven_row_post_gate_modern_baseline_benchmark_20260522.json"
        )

        self.assertEqual(gate["metadata"]["gate_count"], 21)
        self.assertEqual(gate["metadata"]["passed_gate_count"], 21)
        self.assertFalse(gate["blockers"])

        self.assertTrue(decision["metadata"]["review_only"])
        self.assertEqual(decision["metadata"]["candidate_count"], 7)
        self.assertEqual(decision["metadata"]["mechanism_match_review_ready_count"], 7)
        self.assertEqual(decision["metadata"]["source_free_geometry_above_floor_count"], 7)
        self.assertEqual(decision["metadata"]["uniref_current_reference_clear_count"], 7)
        self.assertFalse(decision["metadata"]["ready_for_label_import"])
        self.assertEqual(decision["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(decision["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(decision["metadata"]["external_imported_seed_fingerprint_labels"], [])
        self.assertEqual(
            decision["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            decision["metadata"]["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )
        self.assertEqual(
            decision["decision"]["payload_gate_dry_run_status"],
            "passed_no_import_gate_only",
        )
        self.assertFalse(decision["decision"]["label_import_authorized"])
        self.assertIn(
            "human_label_action_not_requested",
            decision["decision"]["exact_remaining_blockers"],
        )

        rows = {row["row_id"]: row for row in decision["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P0A8Y5",
                "uniprot:P75792",
                "uniprot:P15776",
            },
        )
        for row in rows.values():
            self.assertEqual(row["terminal_decision"], "mechanism_match_review_ready")
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_separation"]["source_context_counted_as_predictive"])
            self.assertEqual(
                row["full_label_factory_payload_gate"]["status"],
                "passed_currentregistry_adapter_no_import",
            )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P0A8Y5"]["remaining_import_blockers"],
        )
        self.assertIn(
            "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            rows["uniprot:P75792"]["remaining_import_blockers"],
        )

        self.assertEqual(human_packet["metadata"]["candidate_count"], 5)
        self.assertEqual(human_packet["metadata"]["excluded_metal_specificity_blocked_count"], 2)
        self.assertEqual(human_packet["metadata"]["ready_for_human_review_count"], 5)
        self.assertFalse(human_packet["metadata"]["ready_for_label_import"])
        self.assertEqual(
            human_packet["metadata"]["families"],
            {
                "heme_peroxidase_oxidase": [
                    "uniprot:I2DBY1",
                    "uniprot:K7N5M8",
                    "uniprot:P14532",
                    "uniprot:P39597",
                ],
                "ser_his_acid_hydrolase": ["uniprot:P15776"],
            },
        )
        self.assertTrue(all(human_packet["invariant_checks"].values()))
        self.assertFalse(human_packet["decision"]["label_import_authorized"])

        self.assertFalse(benchmark["metadata"]["geometry_superiority_claim"])
        self.assertEqual(
            benchmark["metadata"]["esm_or_learned_embedding_sidecar_available_count"],
            0,
        )
        self.assertEqual(benchmark["metrics"]["geometry_above_floor_fraction"], 1.0)
        self.assertEqual(benchmark["metrics"]["import_ready_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["countable_label_candidate_fraction"], 0.0)

    def test_second_plp_deep_packet_is_terminal_and_source_separated(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_second_deep_packet_selection_20260522.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_second_deep_packet_source_free_active_site_geometry_scores_20260522.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_second_deep_packet_targeted_current_plp_screen_20260522.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_second_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_second_deep_packet_modern_baseline_benchmark_20260522.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_terminal_decision_rollup_post_second_plp_20260522.json"
        )

        expected_accessions = {
            "Q96255",
            "Q56YA5",
            "P22256",
            "Q93ZN9",
            "P42588",
            "H8WR05",
            "Q988B8",
        }
        self.assertTrue(
            selection["metadata"]["candidate_selection_frozen_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(
            set(selection["metadata"]["selected_accessions"]), expected_accessions
        )
        self.assertEqual(
            set(selection["metadata"]["excluded_prior_deep_packet_accessions"]),
            {"Q8TD30", "Q9NZ45", "Q9Y617", "O07566", "P53555", "Q9S7N2", "P50457"},
        )
        self.assertEqual(
            selection["metadata"]["excluded_exact_current_reference_accessions"],
            ["P12995", "P19938"],
        )

        self.assertTrue(scores["metadata"]["review_only"])
        self.assertEqual(scores["metadata"]["source_free_active_site_ready_count"], 4)
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 4)
        self.assertEqual(scores["metadata"]["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(scores["metadata"]["text_or_label_fields_used_for_score_any"])
        self.assertEqual(
            scores["metadata"]["plp_active_site_extraction_status_counts"],
            {
                "plp_anchor_not_resolved": 2,
                "plp_like_cofactor_absent": 1,
                "source_free_plp_active_site_ready": 4,
            },
        )

        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(screen["metadata"]["targeted_current_plp_high_tm_candidate_count"], 4)
        self.assertEqual(
            screen["metadata"]["screen_status_counts"],
            {
                "current_plp_structural_duplicate_signal": 4,
                "not_run_source_free_plp_active_site_not_ready": 3,
            },
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["candidate_count"], 7)
        self.assertEqual(packet["metadata"]["source_free_active_site_ready_count"], 4)
        self.assertEqual(packet["metadata"]["target_lane_at_or_above_floor_count"], 4)
        self.assertEqual(packet["metadata"]["targeted_current_plp_high_tm_candidate_count"], 4)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 4,
                "terminal_rejection_insufficient_evidence": 3,
            },
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 7)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertFalse(packet["metadata"]["geometry_superiority_claim"])
        self.assertEqual(packet["metadata"]["esm_sidecar_available_count"], 0)

        rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), expected_accessions)
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
            },
            {"Q96255", "P22256", "Q93ZN9", "H8WR05"},
        )
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_insufficient_evidence"
            },
            {"Q56YA5", "P42588", "Q988B8"},
        )
        for accession, row in rows.items():
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_separation"]["source_context_counted_as_predictive"])
            self.assertEqual(row["modern_baseline_comparison"]["superiority_claim"], "none")
            self.assertFalse(
                row["modern_baseline_comparison"]["esm_or_learned_embedding_sidecar"][
                    "available"
                ]
            )
            if accession in {"Q96255", "P22256", "Q93ZN9", "H8WR05"}:
                self.assertTrue(
                    row["current_geometry_retrieval_score_summary"][
                        "target_lane_at_or_above_floor"
                    ]
                )
                self.assertGreater(
                    row["duplicate_leakage_screen"]["high_tm_hit_count"], 0
                )
            else:
                self.assertFalse(
                    row["current_geometry_retrieval_score_summary"][
                        "target_lane_at_or_above_floor"
                    ]
                )
                self.assertEqual(row["duplicate_leakage_screen"]["high_tm_hit_count"], 0)

        self.assertFalse(benchmark["metadata"]["geometry_superiority_claim"])
        self.assertEqual(benchmark["metadata"]["esm_or_learned_embedding_sidecar_available_count"], 0)
        self.assertEqual(benchmark["metrics"]["import_ready_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["countable_label_candidate_fraction"], 0.0)

        self.assertEqual(rollup["metadata"]["candidate_count"], 14)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 10,
                "terminal_rejection_insufficient_evidence": 4,
            },
        )
        self.assertFalse(rollup["metadata"]["ready_for_label_import"])
        self.assertEqual(rollup["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            rollup["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(rollup["metadata"]["external_imported_seed_fingerprint_labels"], [])

    def test_third_plp_deep_packet_closes_remaining_nonduplicate_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_third_deep_packet_selection_20260522.json"
        )
        scores = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_third_deep_packet_source_free_active_site_geometry_scores_20260522.json"
        )
        screen = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_third_deep_packet_targeted_current_plp_screen_20260522.json"
        )
        packet = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_third_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260522.json"
        )
        benchmark = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_third_deep_packet_modern_baseline_benchmark_20260522.json"
        )
        rollup = _load_json(
            ARTIFACTS
            / "v3_plp_aminotransferase_deep_terminal_decision_rollup_post_third_plp_20260522.json"
        )

        expected_accessions = {"Q72LL6", "O50131", "Q8NTR2", "P96060"}
        self.assertTrue(
            selection["metadata"]["candidate_selection_frozen_before_outcome_scoring"]
        )
        self.assertEqual(selection["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(set(selection["metadata"]["selected_accessions"]), expected_accessions)
        self.assertEqual(selection["metadata"]["excluded_exact_current_reference_accessions"], ["P12995", "P19938"])
        self.assertEqual(len(selection["metadata"]["excluded_prior_deep_packet_accessions"]), 14)

        self.assertTrue(scores["metadata"]["review_only"])
        self.assertEqual(scores["metadata"]["source_free_active_site_ready_count"], 2)
        self.assertEqual(scores["metadata"]["target_lane_at_or_above_floor_count"], 2)
        self.assertEqual(scores["metadata"]["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(scores["metadata"]["text_or_label_fields_used_for_score_any"])
        self.assertEqual(
            scores["metadata"]["plp_active_site_extraction_status_counts"],
            {
                "plp_anchor_not_resolved": 2,
                "source_free_plp_active_site_ready": 2,
            },
        )

        self.assertFalse(screen["metadata"]["duplicate_clear_claim_permitted"])
        self.assertEqual(screen["metadata"]["targeted_current_plp_high_tm_candidate_count"], 2)
        self.assertEqual(
            screen["metadata"]["screen_status_counts"],
            {
                "current_plp_structural_duplicate_signal": 2,
                "not_run_source_free_plp_active_site_not_ready": 2,
            },
        )

        self.assertTrue(packet["metadata"]["review_only"])
        self.assertEqual(packet["metadata"]["candidate_count"], 4)
        self.assertEqual(packet["metadata"]["new_external_rows_frozen"], 0)
        self.assertEqual(packet["metadata"]["source_free_active_site_ready_count"], 2)
        self.assertEqual(packet["metadata"]["target_lane_at_or_above_floor_count"], 2)
        self.assertEqual(
            packet["metadata"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 2,
                "terminal_rejection_insufficient_evidence": 2,
            },
        )
        self.assertEqual(packet["metadata"]["non_needs_review_terminal_count"], 4)
        self.assertEqual(packet["metadata"]["mechanism_match_review_ready_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        self.assertEqual(packet["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["curated_label_registry_edited"])
        self.assertFalse(packet["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(packet["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(packet["metadata"]["removal_allowed_set_true"])
        self.assertFalse(packet["metadata"]["geometry_superiority_claim"])
        self.assertEqual(packet["metadata"]["esm_sidecar_available_count"], 0)

        rows = {row["accession"]: row for row in packet["rows"]}
        self.assertEqual(set(rows), expected_accessions)
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_duplicate_or_leakage"
            },
            {"Q72LL6", "O50131"},
        )
        self.assertEqual(
            {
                accession
                for accession, row in rows.items()
                if row["terminal_decision"] == "terminal_rejection_insufficient_evidence"
            },
            {"Q8NTR2", "P96060"},
        )
        for accession, row in rows.items():
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_separation"]["source_context_counted_as_predictive"])
            self.assertEqual(row["modern_baseline_comparison"]["superiority_claim"], "none")
            self.assertFalse(
                row["modern_baseline_comparison"]["esm_or_learned_embedding_sidecar"][
                    "available"
                ]
            )
            if accession in {"Q72LL6", "O50131"}:
                self.assertTrue(
                    row["current_geometry_retrieval_score_summary"][
                        "target_lane_at_or_above_floor"
                    ]
                )
                self.assertGreater(row["duplicate_leakage_screen"]["high_tm_hit_count"], 0)
            else:
                self.assertFalse(
                    row["current_geometry_retrieval_score_summary"][
                        "target_lane_at_or_above_floor"
                    ]
                )
                self.assertEqual(row["duplicate_leakage_screen"]["high_tm_hit_count"], 0)

        self.assertFalse(benchmark["metadata"]["geometry_superiority_claim"])
        self.assertEqual(benchmark["metadata"]["esm_or_learned_embedding_sidecar_available_count"], 0)
        self.assertEqual(benchmark["metrics"]["sequence_exact_duplicate_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["import_ready_fraction"], 0.0)
        self.assertEqual(benchmark["metrics"]["countable_label_candidate_fraction"], 0.0)

        self.assertEqual(rollup["metadata"]["candidate_count"], 18)
        self.assertEqual(
            rollup["metadata"]["terminal_decision_counts"],
            {
                "terminal_rejection_duplicate_or_leakage": 12,
                "terminal_rejection_insufficient_evidence": 6,
            },
        )
        self.assertFalse(rollup["metadata"]["ready_for_label_import"])
        self.assertEqual(rollup["metadata"]["registry_invariant_label_count"], 682)
        self.assertEqual(
            rollup["metadata"]["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(rollup["metadata"]["external_imported_seed_fingerprint_labels"], [])

    def test_post_third_plp_remaining_blocker_queue_stays_no_breadth(self) -> None:
        queue = _load_json(
            ARTIFACTS
            / "v3_external_remaining_blocker_queue_post_third_plp_closure_20260522.json"
        )

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["remaining_source_free_geometry_or_structure_blocker_count"], 0)
        self.assertEqual(metadata["remaining_mechanism_match_review_ready_rows"], 7)
        self.assertEqual(metadata["remaining_nonmetal_human_review_rows"], 5)
        self.assertEqual(metadata["remaining_metal_phosphate_specificity_blocker_rows"], 2)
        self.assertEqual(metadata["plp_non_exact_reference_rows_terminal_count"], 18)
        self.assertEqual(metadata["plp_remaining_non_exact_reference_rows_not_deepened"], 0)
        self.assertEqual(
            metadata["plp_exact_current_reference_sequence_duplicates_excluded"],
            ["P12995", "P19938"],
        )
        self.assertEqual(metadata["label_factory_payload_gate_status"], "passed_currentregistry_adapter_no_import")
        self.assertEqual(metadata["label_factory_payload_gate_blockers"], [])
        self.assertEqual(metadata["external_source_transfer_gate_status"], "passed")
        self.assertEqual(metadata["external_source_transfer_gate_blockers"], [])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])

        rows = {row["row_id"]: row for row in queue["rows"]}
        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P15776",
                "uniprot:P0A8Y5",
                "uniprot:P75792",
            },
        )
        self.assertEqual(
            {
                row_id
                for row_id, row in rows.items()
                if row["blocker_class"] == "metal_phosphate_specificity_evidence_missing"
            },
            {"uniprot:P0A8Y5", "uniprot:P75792"},
        )
        self.assertTrue(
            all(not row["source_context_counted_as_predictive"] for row in rows.values())
        )
        self.assertFalse(queue["decision"]["start_new_broad_external_minicampaign"])
        self.assertFalse(queue["decision"]["label_import_authorized"])
        self.assertEqual(queue["decision"]["countable_label_candidates_created"], 0)

    def test_akr_family_readiness_post_third_plp_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_akr_family_readiness_post_third_plp_no_breadth_packet_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        readiness = packet["family_readiness"]
        baseline = packet["baseline_comparison_caveats"]
        external_context = packet["external_deepening_context"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["family_id"], "akr_nadp_redox")
        self.assertEqual(metadata["positive_like_row_count"], 1)
        self.assertEqual(metadata["source_free_akr_axis_ready_count"], 0)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )

        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "source_free_local_nadp_ligand_or_proxy_geometry_axis_missing",
            decision["exact_missing_evidence"],
        )
        self.assertIn(
            "source_free_catalytic_tyr_lys_his_environment_policy_missing",
            decision["exact_missing_evidence"],
        )

        positives = readiness["positive_like_rows"]
        self.assertEqual(len(positives), 1)
        self.assertEqual(positives[0]["row_id"], "uniprot:C9JRZ8")
        self.assertFalse(positives[0]["ready_for_label_import"])
        self.assertFalse(positives[0]["countable_label_candidate"])
        self.assertFalse(
            readiness["active_site_evidence"][
                "source_active_site_annotations_counted_as_predictive_evidence"
            ]
        )
        self.assertFalse(readiness["cofactors"]["direct_local_nadp_ligand_geometry_ready"])
        self.assertIn("sdr_nad_p_redox_sibling_controls", readiness["counterfamilies"])

        self.assertFalse(baseline["geometry_superiority_claim"])
        self.assertFalse(baseline["foldseek_sidecar"]["available_for_akr_positive_like_row"])
        self.assertFalse(external_context["start_new_broad_external_minicampaign"])
        self.assertEqual(
            external_context["remaining_source_free_geometry_or_structure_blocker_count"],
            0,
        )
        self.assertFalse(packet["next_exact_experiment"]["decision_to_start_now"])
        self.assertTrue(
            packet["next_exact_experiment"]["selection_freeze_required_before_scoring"]
        )

    def test_nonmetal_human_review_checklist_is_no_import(self) -> None:
        checklist = _load_json(
            ARTIFACTS
            / "v3_external_nonmetal_human_review_acceptance_checklist_post_plp_closure_20260522.json"
        )

        metadata = checklist["metadata"]
        decision = checklist["decision"]
        policy = checklist["review_policy"]
        rows = {row["row_id"]: row for row in checklist["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 5)
        self.assertEqual(metadata["source_free_geometry_above_floor_count"], 5)
        self.assertEqual(metadata["uniref_current_reference_clear_count"], 5)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])
        self.assertEqual(
            metadata["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )

        self.assertTrue(decision["human_action_required"])
        self.assertFalse(decision["label_import_authorized"])
        self.assertEqual(decision["countable_label_candidates_created"], 0)
        self.assertIn(
            "mechanism_match_review_ready",
            decision["allowed_terminal_outcomes_after_human_review"],
        )
        self.assertFalse(policy["source_separation"]["source_context_counted_as_predictive"])
        self.assertIn(
            "source-free target-lane geometry remains above the current floor with rank 1",
            policy["accept_requires_all"],
        )

        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P15776",
            },
        )
        self.assertEqual(
            {
                row_id
                for row_id, row in rows.items()
                if row["target_current_fingerprint_lane"] == "heme_peroxidase_oxidase"
            },
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
            },
        )
        self.assertEqual(
            rows["uniprot:P15776"]["target_current_fingerprint_lane"],
            "ser_his_acid_hydrolase",
        )
        for row in rows.values():
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertEqual(
                row["acceptance_status_before_human_review"],
                "ready_for_human_review_not_import_ready",
            )
            self.assertEqual(
                row["terminal_decision_before_human_review"],
                "mechanism_match_review_ready",
            )
            self.assertFalse(
                row["source_free_geometry"]["text_or_label_fields_used_for_score"]
            )
            self.assertEqual(row["source_free_geometry"]["target_lane_rank"], 1)
            self.assertEqual(
                row["uniref_current_reference_status"],
                "uniref_current_reference_screen_no_current_reference_overlap",
            )

    def test_metal_phosphate_specificity_extractor_preregistration_is_bounded(self) -> None:
        prereg = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_phosphate_specificity_extractor_preregistration_20260522.json"
        )

        metadata = prereg["metadata"]
        decision = prereg["decision"]
        extractor = prereg["preregistered_extractor"]
        rows = {row["row_id"]: row for row in prereg["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_rows_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 2)
        self.assertEqual(metadata["target_current_fingerprint_lane"], "metal_dependent_hydrolase")
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])
        self.assertEqual(
            metadata["external_imported_out_of_scope_labels"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )

        self.assertEqual(decision["current_terminal_status"], "blocked_with_exact_missing_evidence")
        self.assertFalse(decision["decision_to_run_now"])
        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_scoring_authorized"])
        self.assertTrue(extractor["candidate_selection_freeze"]["frozen_before_outcome_scoring"])
        self.assertEqual(
            extractor["candidate_selection_freeze"]["row_ids"],
            ["uniprot:P0A8Y5", "uniprot:P75792"],
        )
        self.assertIn("mmCIF atom coordinates", extractor["allowed_predictive_inputs"])
        self.assertIn("EC labels", extractor["excluded_predictive_inputs"])
        self.assertTrue(
            extractor["phosphate_like_atom_pattern"][
                "reject_if_only_generic_polyol_or_buffer"
            ]
        )
        self.assertIn("PO4", extractor["phosphate_like_ligand_codes_review_only_seed"])
        self.assertTrue(extractor["review_only_threshold_policy"]["no_threshold_calibration_from_outcomes"])
        self.assertEqual(extractor["review_only_threshold_policy"]["initial_radius_angstrom"], 6.0)
        self.assertIn(
            "no EC/name/UniProt prose/source annotation is used to infer phosphatase specificity",
            extractor["positive_requirements_all"],
        )

        self.assertEqual(set(rows), {"uniprot:P0A8Y5", "uniprot:P75792"})
        self.assertEqual(rows["uniprot:P0A8Y5"]["pdb_ids_scanned"], ["1RKQ"])
        self.assertEqual(
            rows["uniprot:P75792"]["pdb_ids_scanned"],
            ["1RLM", "1RLO", "1RLT", "2HF2"],
        )
        for row in rows.values():
            self.assertEqual(row["phosphate_like_site_count_total"], 0)
            self.assertFalse(row["ready_for_label_import"])
            self.assertEqual(
                row["current_blocker"],
                "source_free_phosphate_or_substrate_ligand_absent_for_phosphatase_specificity",
            )
            self.assertEqual(
                row["source_free_metal_geometry_status"],
                "target_lane_rank1_above_floor",
            )

    def test_metal_phosphate_pocket_proxy_extractor_test_stays_review_only(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_phosphate_pocket_proxy_extractor_test_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        extractor = packet["extractor"]
        rows = {row["row_id"]: row for row in packet["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_rows_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 2)
        self.assertEqual(metadata["source_free_phosphate_pocket_proxy_detected_count"], 2)
        self.assertEqual(metadata["phosphatase_specific_review_ready_count"], 2)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])

        self.assertEqual(
            decision["packet_status"],
            "metal_phosphate_specificity_blocker_resolved_to_review_only_pocket_proxy",
        )
        self.assertFalse(decision["label_import_authorized"])
        self.assertTrue(decision["human_action_required_before_any_label_action"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)

        self.assertEqual(
            extractor["extractor_id"],
            "metal_phosphatase_source_free_phosphate_pocket_v1_review_only",
        )
        self.assertEqual(extractor["radius_angstrom"], 6.0)
        self.assertTrue(extractor["review_only_not_production_score"])
        self.assertIn("EC labels", extractor["excluded_predictive_inputs"])

        self.assertEqual(set(rows), {"uniprot:P0A8Y5", "uniprot:P75792"})
        for row in rows.values():
            proxy = row["source_free_phosphate_pocket_proxy"]
            self.assertEqual(row["terminal_decision"], "mechanism_match_review_ready")
            self.assertEqual(
                row["phosphatase_specific_review_status"],
                "source_free_phosphate_pocket_proxy_resolved_review_only",
            )
            self.assertTrue(proxy["proxy_detected"])
            self.assertEqual(proxy["radius_angstrom"], 6.0)
            self.assertGreaterEqual(proxy["non_metal_ligand_contact_count"], 2)
            self.assertGreaterEqual(
                proxy["polar_or_basic_non_metal_contact_count"], 2
            )
            self.assertFalse(
                proxy["text_or_label_fields_used_for_predictive_score"]
            )
            self.assertFalse(row["source_separation"]["source_context_counted_as_predictive"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])

    def test_metal_phosphate_pocket_proxy_benchmark_has_caveats(self) -> None:
        benchmark = _load_json(
            ARTIFACTS
            / "v3_metal_phosphatase_phosphate_pocket_proxy_modern_baseline_benchmark_20260522.json"
        )

        metadata = benchmark["metadata"]
        metrics = benchmark["metrics"]
        rows = {row["row_id"]: row for row in benchmark["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["geometry_superiority_claim"])
        self.assertFalse(metadata["representation_superiority_claim"])
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(metrics["frozen_row_count"], 2)
        self.assertEqual(metrics["source_free_phosphate_pocket_proxy_detected_count"], 2)
        self.assertEqual(metrics["ec_keyword_route_hit_count"], 2)
        self.assertEqual(metrics["sequence_exact_current_reference_alert_count"], 0)
        self.assertEqual(metrics["foldseek_current_countable_high_tm_hit_count"], 0)
        self.assertEqual(metrics["esm_or_learned_embedding_sidecar_available_count"], 0)
        self.assertFalse(metrics["geometry_superiority_claim"])
        self.assertEqual(set(rows), {"uniprot:P0A8Y5", "uniprot:P75792"})
        for row in rows.values():
            self.assertTrue(
                row["geometry_pipeline"][
                    "source_free_phosphate_pocket_proxy_detected"
                ]
            )
            self.assertFalse(
                row["geometry_pipeline"][
                    "text_or_label_fields_used_for_predictive_score"
                ]
            )
            self.assertTrue(row["ec_keyword_routing_baseline"]["keyword_hit"])
            self.assertIsNone(
                row["deterministic_sequence_kmer_baseline"][
                    "exact_current_reference_id"
                ]
            )
            self.assertFalse(row["esm_sidecar"]["available"])

    def test_all_review_ready_human_packet_includes_metal_proxy_rows(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_seed_fingerprint_all_review_ready_human_packet_after_metal_proxy_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        policy = packet["review_policy"]
        rows = {row["row_id"]: row for row in packet["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(metadata["source_free_geometry_above_floor_count"], 7)
        self.assertEqual(metadata["uniref_current_reference_clear_count"], 7)
        self.assertEqual(metadata["foldseek_current_countable_high_tm_hit_count"], 0)
        self.assertEqual(metadata["metal_phosphate_pocket_proxy_resolved_count"], 2)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])

        self.assertTrue(decision["human_action_required"])
        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(
            decision["remaining_blocker_class_counts"],
            {
                "explicit_human_expert_label_action_required": 7,
                "metal_phosphate_specificity_evidence_missing": 0,
                "source_free_geometry_or_structure_missing": 0,
            },
        )
        self.assertFalse(policy["source_separation"]["source_context_counted_as_predictive"])
        self.assertIn(
            "metal rows retain the review-only phosphate-pocket proxy or receive stronger source-free phosphate/substrate evidence",
            policy["accept_requires_all"],
        )

        self.assertEqual(
            set(rows),
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P15776",
                "uniprot:P0A8Y5",
                "uniprot:P75792",
            },
        )
        metal_rows = {row_id: rows[row_id] for row_id in ["uniprot:P0A8Y5", "uniprot:P75792"]}
        for row in rows.values():
            self.assertEqual(
                row["terminal_decision_before_human_review"],
                "mechanism_match_review_ready",
            )
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_context_counted_as_predictive"])
            self.assertTrue(row["source_free_geometry"]["target_lane_at_or_above_floor"])
            self.assertEqual(
                row["uniref_current_reference_status"],
                "uniref_current_reference_screen_no_current_reference_overlap",
            )
        for row in metal_rows.values():
            self.assertEqual(
                row["phosphate_pocket_proxy_status"],
                "source_free_phosphate_pocket_proxy_resolved_review_only",
            )
            self.assertTrue(row["phosphate_pocket_proxy"]["proxy_detected"])
            self.assertEqual(row["phosphate_pocket_proxy"]["radius_angstrom"], 6.0)

    def test_mcsa_pymol_review_queue_is_review_only_and_fail_closed(self) -> None:
        queue = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_expert_review_queue_1025.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_manual_dry_run_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_manual_dry_run_validation_20260522.json"
        )

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["method"], "mcsa_pymol_expert_review_queue")
        self.assertEqual(metadata["total_review_rows_scanned"], 321)
        self.assertEqual(metadata["pymol_ready_count"], 1)
        self.assertEqual(metadata["ready_entry_ids"], ["m_csa:939"])
        self.assertEqual(metadata["rows_with_structure_paths"], 1)
        self.assertEqual(metadata["missing_field_counts"]["missing_structure_path"], 318)
        self.assertEqual(queue["pml_script_manifest"]["metadata"]["script_count"], 1)

        ready_rows = [row for row in queue["rows"] if row["pymol_ready"]]
        self.assertEqual(len(ready_rows), 1)
        ready = ready_rows[0]
        self.assertEqual(ready["entry_id"], "m_csa:939")
        self.assertTrue(ready["structure_path"].endswith("pdb_3CMM.cif"))
        self.assertEqual(ready["focus_atom_pair"]["left"]["atom_name"], "CA")
        self.assertEqual(ready["focus_atom_pair"]["right"]["atom_name"], "CA")
        self.assertFalse(ready["countable_import_ready"])
        self.assertIn("label_factory_gates_not_run", ready["countable_import_blockers"])

        structure_text = (ROOT / ready["structure_path"]).read_text(encoding="utf-8")
        for side in ("left", "right"):
            atom = ready["focus_atom_pair"][side]
            expected = (
                f" {atom['residue_name']} {atom['chain_name']} 1 "
                f"{atom['residue_number']} "
            )
            self.assertIn(expected, structure_text)
            self.assertIn(f" {atom['residue_name']} {atom['chain_name']} CA ", structure_text)

        blocked = [row for row in queue["rows"] if not row["pymol_ready"]]
        self.assertTrue(blocked)
        self.assertTrue(
            all(
                row["missing_fields"]
                for row in blocked
            )
        )

        self.assertTrue(dry_run["metadata"]["review_only"])
        self.assertTrue(dry_run["metadata"]["dry_run"])
        self.assertEqual(dry_run["metadata"]["countable_import_ready_count"], 0)
        self.assertEqual(dry_run["review_items"][0]["decision"], "skipped")
        self.assertFalse(dry_run["review_items"][0]["countable_import_ready"])
        self.assertTrue(validation["metadata"]["valid"])
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)

    def test_mcsa_pymol_materialized_tranche_expands_ready_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_materialization_tranche_selection_20260522.json"
        )
        materialization = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_materialization_tranche_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_expert_review_queue_1025_materialized_tranche_20260522.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_materialized_tranche_dry_run_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_materialized_tranche_dry_run_validation_20260522.json"
        )
        blockers = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_remaining_blocker_report_after_materialization_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_pymol_materialization_review_only_zero_import_gate_20260522.json"
        )

        self.assertEqual(selection["metadata"]["selected_row_count"], 25)
        self.assertEqual(materialization["metadata"]["materialized_count"], 25)
        self.assertEqual(materialization["metadata"]["failed_count"], 0)
        self.assertFalse(materialization["metadata"]["ready_for_label_import"])
        self.assertFalse(materialization["metadata"]["curated_label_registry_edited"])
        self.assertFalse(materialization["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(materialization["metadata"]["artifact_upload_or_removal_performed"])
        self.assertFalse(materialization["metadata"]["removal_allowed"])

        for row in materialization["rows"]:
            self.assertEqual(row["materialization_status"], "materialized")
            self.assertEqual(len(row["sha256"]), 64)
            path = ROOT / row["local_structure_path"]
            self.assertTrue(path.exists(), row["local_structure_path"])
            self.assertGreater(row["size_bytes"], 0)
            self.assertTrue(row["first_line"].startswith("data_"))

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["total_review_rows_scanned"], 321)
        self.assertEqual(metadata["pymol_ready_count"], 26)
        self.assertEqual(metadata["rows_with_structure_paths"], 26)
        self.assertEqual(metadata["rows_with_verified_focus_atoms"], 26)
        self.assertEqual(metadata["missing_field_counts"]["missing_structure_path"], 293)
        self.assertEqual(queue["pml_script_manifest"]["metadata"]["script_count"], 26)
        self.assertIn("m_csa:939", metadata["ready_entry_ids"])
        for entry_id in materialization["metadata"]["materialized_entry_ids"]:
            self.assertIn(entry_id, metadata["ready_entry_ids"])
        for row in queue["rows"]:
            if row["pymol_ready"]:
                self.assertTrue(row["focus_atom_selection_verified"])

        self.assertTrue(dry_run["metadata"]["dry_run"])
        self.assertEqual(dry_run["metadata"]["review_item_count"], 26)
        self.assertEqual(dry_run["metadata"]["decision_counts"], {"skipped": 26})
        self.assertEqual(dry_run["metadata"]["countable_import_ready_count"], 0)
        self.assertTrue(validation["metadata"]["valid"])
        self.assertEqual(validation["metadata"]["review_item_count"], 26)
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)

        blocker_metadata = blockers["metadata"]
        self.assertTrue(blocker_metadata["review_only"])
        self.assertEqual(blocker_metadata["pymol_ready_count"], 26)
        self.assertEqual(blocker_metadata["rows_with_verified_focus_atoms"], 26)
        self.assertEqual(blocker_metadata["blocked_count"], 295)
        self.assertEqual(blocker_metadata["next_tranche_candidate_count"], 25)
        self.assertEqual(blocker_metadata["missing_structure_id_count"], 2)
        self.assertEqual(blocker_metadata["missing_exact_pair_or_distance_count"], 23)
        self.assertTrue(blockers["next_structure_materialization_candidates"])
        self.assertTrue(blockers["structure_id_mapping_blockers"])
        self.assertTrue(blockers["exact_atom_pair_mapping_blockers_sample"])

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 6)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_mcsa_pymol_second_materialized_tranche_expands_ready_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_second_materialization_tranche_selection_20260522.json"
        )
        materialization = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_second_materialization_tranche_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_expert_review_queue_1025_second_materialized_tranche_20260522.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_second_materialized_tranche_dry_run_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_second_materialized_tranche_dry_run_validation_20260522.json"
        )
        blockers = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_remaining_blocker_report_after_second_materialization_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_pymol_second_materialization_review_only_zero_import_gate_20260522.json"
        )

        self.assertEqual(selection["metadata"]["selected_row_count"], 25)
        self.assertEqual(materialization["metadata"]["materialized_count"], 25)
        self.assertEqual(materialization["metadata"]["failed_count"], 0)
        self.assertFalse(materialization["metadata"]["ready_for_label_import"])
        for row in materialization["rows"]:
            self.assertEqual(row["materialization_status"], "materialized")
            self.assertEqual(len(row["sha256"]), 64)
            self.assertTrue((ROOT / row["local_structure_path"]).exists())
            self.assertTrue(row["first_line"].startswith("data_"))

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["total_review_rows_scanned"], 321)
        self.assertEqual(metadata["pymol_ready_count"], 51)
        self.assertEqual(metadata["rows_with_structure_paths"], 51)
        self.assertEqual(metadata["rows_with_verified_focus_atoms"], 51)
        self.assertEqual(metadata["missing_field_counts"]["missing_structure_path"], 268)
        self.assertEqual(queue["pml_script_manifest"]["metadata"]["script_count"], 51)
        for entry_id in materialization["metadata"]["materialized_entry_ids"]:
            self.assertIn(entry_id, metadata["ready_entry_ids"])

        self.assertEqual(dry_run["metadata"]["review_item_count"], 51)
        self.assertEqual(dry_run["metadata"]["decision_counts"], {"skipped": 51})
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)

        blocker_metadata = blockers["metadata"]
        self.assertEqual(blocker_metadata["pymol_ready_count"], 51)
        self.assertEqual(blocker_metadata["rows_with_verified_focus_atoms"], 51)
        self.assertEqual(blocker_metadata["blocked_count"], 270)
        self.assertEqual(blocker_metadata["next_tranche_candidate_count"], 25)

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 6)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_mcsa_pymol_third_materialized_tranche_expands_ready_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_third_materialization_tranche_selection_20260522.json"
        )
        materialization = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_third_materialization_tranche_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_expert_review_queue_1025_third_materialized_tranche_20260522.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_third_materialized_tranche_dry_run_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_third_materialized_tranche_dry_run_validation_20260522.json"
        )
        blockers = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_remaining_blocker_report_after_third_materialization_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_pymol_third_materialization_review_only_zero_import_gate_20260522.json"
        )

        self.assertEqual(selection["metadata"]["selected_row_count"], 25)
        self.assertEqual(materialization["metadata"]["materialized_count"], 25)
        self.assertEqual(materialization["metadata"]["failed_count"], 0)
        self.assertFalse(materialization["metadata"]["ready_for_label_import"])
        self.assertFalse(materialization["metadata"]["removal_allowed"])
        for row in materialization["rows"]:
            self.assertEqual(row["materialization_status"], "materialized")
            self.assertEqual(len(row["sha256"]), 64)
            self.assertTrue((ROOT / row["local_structure_path"]).exists())
            self.assertTrue(row["first_line"].startswith("data_"))

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["total_review_rows_scanned"], 321)
        self.assertEqual(metadata["pymol_ready_count"], 76)
        self.assertEqual(metadata["rows_with_structure_paths"], 76)
        self.assertEqual(metadata["rows_with_verified_focus_atoms"], 76)
        self.assertEqual(metadata["missing_field_counts"]["missing_structure_path"], 243)
        self.assertEqual(queue["pml_script_manifest"]["metadata"]["script_count"], 76)
        for entry_id in materialization["metadata"]["materialized_entry_ids"]:
            self.assertIn(entry_id, metadata["ready_entry_ids"])

        self.assertEqual(dry_run["metadata"]["review_item_count"], 76)
        self.assertEqual(dry_run["metadata"]["decision_counts"], {"skipped": 76})
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)

        blocker_metadata = blockers["metadata"]
        self.assertEqual(blocker_metadata["pymol_ready_count"], 76)
        self.assertEqual(blocker_metadata["rows_with_verified_focus_atoms"], 76)
        self.assertEqual(blocker_metadata["blocked_count"], 245)
        self.assertEqual(blocker_metadata["next_tranche_candidate_count"], 25)

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 6)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_mcsa_pymol_fourth_materialized_tranche_expands_ready_rows(self) -> None:
        selection = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_fourth_materialization_tranche_selection_20260522.json"
        )
        materialization = _load_json(
            ARTIFACTS / "v3_mcsa_pymol_fourth_materialization_tranche_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_expert_review_queue_1025_fourth_materialized_tranche_20260522.json"
        )
        dry_run = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_fourth_materialized_tranche_dry_run_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_expert_review_decision_batch_pymol_fourth_materialized_tranche_dry_run_validation_20260522.json"
        )
        blockers = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_remaining_blocker_report_after_fourth_materialization_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_pymol_fourth_materialization_review_only_zero_import_gate_20260522.json"
        )

        self.assertEqual(selection["metadata"]["selected_row_count"], 25)
        self.assertEqual(materialization["metadata"]["materialized_count"], 25)
        self.assertEqual(materialization["metadata"]["failed_count"], 0)
        self.assertFalse(materialization["metadata"]["ready_for_label_import"])
        self.assertFalse(materialization["metadata"]["removal_allowed"])
        for row in materialization["rows"]:
            self.assertEqual(row["materialization_status"], "materialized")
            self.assertEqual(len(row["sha256"]), 64)
            self.assertTrue((ROOT / row["local_structure_path"]).exists())
            self.assertTrue(row["first_line"].startswith("data_"))

        metadata = queue["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["total_review_rows_scanned"], 321)
        self.assertEqual(metadata["pymol_ready_count"], 101)
        self.assertEqual(metadata["rows_with_structure_paths"], 101)
        self.assertEqual(metadata["rows_with_verified_focus_atoms"], 101)
        self.assertEqual(metadata["missing_field_counts"]["missing_structure_path"], 218)
        self.assertEqual(queue["pml_script_manifest"]["metadata"]["script_count"], 101)
        for entry_id in materialization["metadata"]["materialized_entry_ids"]:
            self.assertIn(entry_id, metadata["ready_entry_ids"])

        self.assertEqual(dry_run["metadata"]["review_item_count"], 101)
        self.assertEqual(dry_run["metadata"]["decision_counts"], {"skipped": 101})
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)

        blocker_metadata = blockers["metadata"]
        self.assertEqual(blocker_metadata["pymol_ready_count"], 101)
        self.assertEqual(blocker_metadata["rows_with_verified_focus_atoms"], 101)
        self.assertEqual(blocker_metadata["blocked_count"], 220)
        self.assertEqual(blocker_metadata["next_tranche_candidate_count"], 25)

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 6)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_mcsa_pymol_all_materializable_structure_paths_are_closed(self) -> None:
        closure = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_all_materializable_structure_path_closure_20260522.json"
        )
        queue = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_expert_review_queue_1025_all_materialized_20260522.json"
        )
        blockers = _load_json(
            ARTIFACTS
            / "v3_mcsa_pymol_remaining_blocker_report_after_all_materialization_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_pymol_all_materializable_closure_review_only_zero_import_gate_20260522.json"
        )

        metadata = closure["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["pymol_ready_count"], 298)
        self.assertEqual(metadata["rows_with_verified_focus_atoms"], 298)
        self.assertEqual(metadata["remaining_blocked_count"], 23)
        self.assertEqual(metadata["next_tranche_candidate_count"], 0)
        self.assertEqual(metadata["materialized_sidecar_count"], 317)
        self.assertEqual(metadata["failed_materialization_count"], 0)

        self.assertEqual(queue["metadata"]["pymol_ready_count"], 298)
        self.assertEqual(queue["metadata"]["rows_with_verified_focus_atoms"], 298)
        self.assertEqual(blockers["metadata"]["next_tranche_candidate_count"], 0)
        self.assertEqual(blockers["metadata"]["blocked_count"], 23)
        self.assertNotIn(
            "missing_structure_path",
            blockers["metadata"]["missing_field_counts"],
        )
        self.assertIn(
            "needs resolved focus CA atom pair/distance for 23 rows",
            closure["decision"]["exact_missing_evidence"],
        )
        self.assertFalse(closure["decision"]["label_import_authorized"])
        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)

    def test_glycoside_hydrolase_post_pymol_packet_stays_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_glycoside_hydrolase_family_readiness_post_pymol_bridge_packet_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        control = packet["control_surface"]
        baseline = packet["modern_baseline_caveats"]
        row = packet["positive_like_rows"][0]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            decision["family_status"], "blocked_with_exact_missing_evidence"
        )
        self.assertFalse(decision["label_import_authorized"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "source-free acidic-dyad local geometry policy frozen before scoring",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(control["frozen_row_count"], 15)
        self.assertEqual(control["source_free_glycoside_axis_ready_count"], 0)
        self.assertEqual(control["terminal_decision_counts"]["needs_review"], 1)
        self.assertFalse(baseline["ec_keyword_predictive_use_allowed"])
        self.assertFalse(baseline["geometry_superiority_claim"])
        self.assertEqual(baseline["mmseqs_current_reference_no_near_duplicate_count"], 5)

        self.assertEqual(row["entry_id"], "uniprot:Q6NSJ0")
        self.assertEqual(row["terminal_decision"], "needs_review")
        self.assertEqual(row["inverse_gate_status_against_current_8"], "passed")
        self.assertFalse(row["ready_for_label_import"])
        self.assertFalse(row["countable_label_candidate"])
        self.assertIn("review_decision_not_terminal", row["remaining_import_blockers"])

    def test_sugar_phosphate_isomerase_post_pymol_packet_stays_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_sugar_phosphate_isomerase_family_readiness_post_pymol_bridge_packet_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        control = packet["control_surface"]
        baseline = packet["modern_baseline_caveats"]
        row = packet["positive_like_rows"][0]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            decision["family_status"], "blocked_with_exact_missing_evidence"
        )
        self.assertFalse(decision["label_import_authorized"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "source-free sugar-phosphate pocket or substrate geometry where available",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(control["frozen_row_count"], 15)
        self.assertEqual(control["source_free_sugar_phosphate_axis_ready_count"], 0)
        self.assertFalse(baseline["ec_keyword_predictive_use_allowed"])
        self.assertFalse(baseline["geometry_superiority_claim"])
        self.assertEqual(baseline["esm_sidecar_available_row_count"], 0)
        self.assertEqual(baseline["mmseqs_current_reference_no_near_duplicate_count"], 5)

        self.assertEqual(row["entry_id"], "uniprot:P34949")
        self.assertEqual(row["terminal_decision"], "needs_review")
        self.assertTrue(row["flavin_ligand_context_absent"])
        self.assertTrue(row["flavin_scope_conflict_repaired"])
        self.assertFalse(row["ready_for_label_import"])
        self.assertFalse(row["countable_label_candidate"])
        self.assertIn("review_decision_not_terminal", row["remaining_import_blockers"])

    def test_schiff_base_lyase_post_pymol_packet_stays_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_schiff_base_lyase_family_readiness_post_pymol_bridge_packet_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        control = packet["control_surface"]
        baseline = packet["modern_baseline_caveats"]
        row = packet["positive_like_rows"][0]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            decision["family_status"], "blocked_with_exact_missing_evidence"
        )
        self.assertFalse(decision["label_import_authorized"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "source-free Tyr/Lys or Schiff-base local-geometry axis frozen before scoring",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(control["frozen_row_count"], 15)
        self.assertEqual(control["source_free_schiff_base_axis_ready_count"], 0)
        self.assertFalse(baseline["ec_keyword_predictive_use_allowed"])
        self.assertFalse(baseline["geometry_superiority_claim"])
        self.assertEqual(baseline["esm_sidecar_available_row_count"], 1)
        self.assertEqual(
            baseline["ec_keyword_false_target_like_control_rows"], ["m_csa:186"]
        )

        self.assertEqual(row["entry_id"], "uniprot:Q9BXD5")
        self.assertEqual(row["terminal_decision"], "needs_review")
        self.assertEqual(
            row["schiff_base_axis_status"],
            "source_traced_tyr_lys_pair_present_not_source_free",
        )
        self.assertFalse(row["ready_for_label_import"])
        self.assertFalse(row["countable_label_candidate"])
        self.assertIn("review_decision_not_terminal", row["remaining_import_blockers"])

    def test_dna_glycosylase_lyase_post_pymol_packet_stays_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_dna_glycosylase_lyase_family_readiness_post_pymol_bridge_packet_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        control = packet["control_surface"]
        baseline = packet["modern_baseline_caveats"]
        row = packet["positive_like_rows"][0]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertEqual(
            decision["family_status"], "blocked_with_exact_missing_evidence"
        )
        self.assertFalse(decision["label_import_authorized"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "source-free catalytic Lys and DNA-lyase local-geometry axis frozen before scoring",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(control["frozen_row_count"], 11)
        self.assertEqual(control["source_free_dna_lyase_axis_ready_count"], 0)
        self.assertFalse(baseline["ec_keyword_predictive_use_allowed"])
        self.assertFalse(baseline["geometry_superiority_claim"])
        self.assertEqual(baseline["esm_sidecar_available_row_count"], 1)
        self.assertEqual(baseline["ec_keyword_false_target_like_control_rows"], [])

        self.assertEqual(row["entry_id"], "uniprot:P06746")
        self.assertEqual(row["terminal_decision"], "needs_review")
        self.assertEqual(
            row["source_traced_axis_status"],
            "source_traced_catalytic_lys_present_not_source_free_geometry",
        )
        self.assertFalse(row["ready_for_label_import"])
        self.assertFalse(row["countable_label_candidate"])
        self.assertIn("review_decision_not_terminal", row["remaining_import_blockers"])

    def test_non_epk_family_readiness_index_post_pymol_stays_no_import(self) -> None:
        index = _load_json(
            ARTIFACTS
            / "v3_non_epk_family_readiness_index_post_pymol_bridge_20260522.json"
        )

        metadata = index["metadata"]
        decision = index["decision"]
        policy = index["source_separation_policy"]
        families = {row["family_id"]: row for row in index["families"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["production_fingerprint_count"], 8)

        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertEqual(
            decision["family_status_counts"],
            {
                "blocked_with_exact_missing_evidence": 4,
                "needs_new_extractor_or_structure": 1,
            },
        )

        self.assertFalse(policy["ec_keyword_or_name_counted_as_predictive"])
        self.assertFalse(policy["source_or_uniprot_prose_counted_as_predictive"])
        self.assertTrue(
            policy["predictive_import_evidence_separated_from_review_context"]
        )
        self.assertEqual(
            set(families),
            {
                "akr_nadp_redox",
                "glycoside_hydrolase",
                "sugar_phosphate_isomerase",
                "schiff_base_lyase",
                "dna_glycosylase_lyase",
            },
        )
        for row in families.values():
            self.assertEqual(row["source_free_axis_ready_count"], 0)
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)

    def test_external_review_ready_human_action_checklist_stays_review_only(self) -> None:
        checklist = _load_json(
            ARTIFACTS
            / "v3_external_review_ready_human_action_checklist_post_pymol_bridge_20260522.json"
        )

        metadata = checklist["metadata"]
        policy = checklist["source_separation_policy"]
        rows = checklist["rows"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(metadata["human_action_required_count"], 7)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

        self.assertFalse(policy["ec_keyword_or_name_counted_as_predictive"])
        self.assertFalse(policy["source_or_uniprot_prose_counted_as_predictive"])
        self.assertTrue(
            policy["predictive_import_evidence_separated_from_review_context"]
        )

        self.assertEqual(
            {row["row_id"] for row in rows},
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P15776",
                "uniprot:P0A8Y5",
                "uniprot:P75792",
            },
        )
        for row in rows:
            self.assertEqual(
                row["terminal_decision_before_human_review"],
                "mechanism_match_review_ready",
            )
            self.assertEqual(
                row["human_action"], "accept_or_reject_mechanism_match_review_ready"
            )
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_context_counted_as_predictive"])
            self.assertEqual(
                row["uniref_current_reference_status"],
                "uniref_current_reference_screen_no_current_reference_overlap",
            )

    def test_post_pymol_review_only_zero_import_gate_passes(self) -> None:
        gate = _load_json(
            ARTIFACTS / "v3_post_pymol_review_only_zero_import_gate_20260522.json"
        )

        metadata = gate["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(metadata["valid"])
        self.assertEqual(metadata["artifact_count"], 9)
        self.assertEqual(metadata["valid_artifact_count"], 9)
        self.assertEqual(metadata["blocker_count"], 0)
        self.assertFalse(metadata["artifact_migration_files_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        for row in gate["rows"]:
            self.assertTrue(row["valid"])
            self.assertTrue(row["review_only"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)
            self.assertFalse(row["curated_label_registry_edited"])
            self.assertFalse(row["fingerprint_registry_edited"])
            self.assertFalse(row["artifact_upload_or_removal_performed"])

    def test_sdr_source_free_axis_probe_converts_to_exact_blocker(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_sdr_source_free_axis_probe_post_pymol_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        rows = {row["row_id"]: row for row in packet["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(metadata["structure_available_count"], 12)
        self.assertEqual(metadata["source_free_catalytic_axis_resolved_count"], 5)
        self.assertEqual(metadata["source_free_full_sdr_axis_ready_count"], 0)
        self.assertEqual(metadata["nad_p_like_ligand_site_present_count"], 0)
        self.assertEqual(
            metadata["non_sdr_control_with_resolved_yxxxk_geometry_count"], 2
        )
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )

        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["family_status"], "blocked_with_exact_missing_evidence")
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertIn(
            "coordinate_nad_p_like_ligand_or_preregistered_cofactor_proxy_absent_on_all_available_structures",
            decision["exact_missing_evidence"],
        )
        self.assertIn(
            "motif_only_yxxxk_geometry_has_non_sdr_control_hits",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(rows["uniprot:O14756"]["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(
            rows["uniprot:O14756"]["source_free_axis_status"],
            "source_free_sdr_catalytic_axis_without_nad_p_ligand",
        )
        self.assertTrue(rows["uniprot:O14756"]["source_free_catalytic_axis_resolved"])
        self.assertFalse(rows["uniprot:O14756"]["source_free_full_sdr_axis_ready"])
        self.assertEqual(
            rows["uniprot:O14756"]["selected_source_free_candidate"]["motif"],
            "YCVSK",
        )
        self.assertFalse(rows["uniprot:O14756"]["source_context_counted_as_predictive"])
        self.assertFalse(
            rows["uniprot:O14756"]["text_or_label_fields_used_for_predictive_score"]
        )

        self.assertEqual(
            rows["m_csa:208"]["terminal_decision"], "terminal_rejection_wrong_scope"
        )
        self.assertTrue(rows["m_csa:208"]["source_free_catalytic_axis_resolved"])
        self.assertEqual(rows["m_csa:208"]["nad_p_like_ligand_site_count"], 0)
        self.assertEqual(
            rows["uniprot:O75911"]["source_free_axis_status"],
            "coordinate_sidecar_missing_for_source_free_sdr_axis_probe",
        )

        for row in rows.values():
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_context_counted_as_predictive"])

    def test_sdr_source_free_axis_benchmark_makes_no_superiority_claim(self) -> None:
        benchmark = _load_json(
            ARTIFACTS
            / "v3_sdr_source_free_axis_probe_modern_baseline_benchmark_20260522.json"
        )

        metadata = benchmark["metadata"]
        metrics = benchmark["metrics"]
        rows = {row["row_id"]: row for row in benchmark["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["geometry_superiority_claim"])
        self.assertFalse(metadata["representation_superiority_claim"])
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(metrics["frozen_row_count"], 14)
        self.assertEqual(metrics["structure_available_count"], 12)
        self.assertEqual(metrics["source_free_yxxxk_geometry_resolved_count"], 5)
        self.assertEqual(metrics["source_free_full_sdr_axis_ready_count"], 0)
        self.assertEqual(metrics["nad_p_like_ligand_present_count"], 0)
        self.assertEqual(metrics["deterministic_sequence_motif_hit_count"], 8)
        self.assertEqual(metrics["non_sdr_control_with_resolved_yxxxk_geometry_count"], 2)
        self.assertEqual(metrics["foldseek_duplicate_screen_available_count"], 0)
        self.assertEqual(metrics["esm_or_learned_embedding_sidecar_available_count"], 0)
        self.assertFalse(metrics["geometry_superiority_claim"])

        self.assertFalse(
            rows["uniprot:O14756"]["deterministic_sequence_motif_baseline"][
                "motif_only_sufficient_for_sdr_claim"
            ]
        )
        self.assertFalse(
            rows["uniprot:O14756"]["ec_keyword_routing_baseline"][
                "predictive_use_allowed"
            ]
        )
        self.assertFalse(
            rows["uniprot:O14756"]["source_free_geometry_probe"][
                "full_sdr_axis_ready"
            ]
        )
        self.assertFalse(rows["uniprot:O14756"]["esm_or_learned_embedding_sidecar"]["available"])

    def test_non_epk_family_readiness_index_post_sdr_probe_stays_no_import(self) -> None:
        index = _load_json(
            ARTIFACTS
            / "v3_non_epk_family_readiness_index_post_sdr_axis_probe_20260522.json"
        )

        metadata = index["metadata"]
        decision = index["decision"]
        families = {row["family_id"]: row for row in index["families"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["family_count"], 6)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])

        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertEqual(
            decision["family_status_counts"],
            {
                "blocked_with_exact_missing_evidence": 5,
                "needs_new_extractor_or_structure": 1,
            },
        )

        self.assertEqual(
            set(families),
            {
                "sdr_nad_p_redox",
                "akr_nadp_redox",
                "glycoside_hydrolase",
                "sugar_phosphate_isomerase",
                "schiff_base_lyase",
                "dna_glycosylase_lyase",
            },
        )
        self.assertEqual(
            families["sdr_nad_p_redox"]["packet"],
            "artifacts/v3_sdr_source_free_axis_probe_post_pymol_20260522.json",
        )
        self.assertEqual(families["sdr_nad_p_redox"]["source_free_axis_ready_count"], 0)
        for row in families.values():
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)

    def test_post_sdr_axis_probe_review_only_zero_import_gate_passes(self) -> None:
        gate = _load_json(
            ARTIFACTS
            / "v3_post_sdr_axis_probe_review_only_zero_import_gate_20260522.json"
        )

        metadata = gate["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(metadata["valid"])
        self.assertEqual(metadata["artifact_count"], 5)
        self.assertEqual(metadata["valid_artifact_count"], 5)
        self.assertEqual(metadata["blocker_count"], 0)
        self.assertFalse(metadata["artifact_migration_files_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        for row in gate["rows"]:
            self.assertTrue(row["valid"])
            self.assertTrue(row["review_only"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)
            self.assertFalse(row["curated_label_registry_edited"])
            self.assertFalse(row["fingerprint_registry_edited"])
            self.assertFalse(row["artifact_upload_or_removal_performed"])

    def test_external_human_decision_template_preserves_review_only_state(self) -> None:
        template = _load_json(
            ARTIFACTS
            / "v3_external_review_ready_human_decision_batch_template_post_sdr_20260522.json"
        )
        validation = _load_json(
            ARTIFACTS
            / "v3_external_review_ready_human_decision_batch_template_validation_post_sdr_20260522.json"
        )

        metadata = template["metadata"]
        policy = template["decision_batch_policy"]
        decision = template["decision"]
        rows = template["rows"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(metadata["pending_human_review_count"], 7)
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertTrue(policy["all_rows_default_to_pending"])
        self.assertTrue(policy["human_acceptance_is_not_label_import"])
        self.assertFalse(policy["label_import_authorized"])
        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)

        self.assertEqual(
            {row["row_id"] for row in rows},
            {
                "uniprot:I2DBY1",
                "uniprot:K7N5M8",
                "uniprot:P14532",
                "uniprot:P39597",
                "uniprot:P15776",
                "uniprot:P0A8Y5",
                "uniprot:P75792",
            },
        )
        for row in rows:
            self.assertEqual(row["human_decision_status"], "pending_human_review")
            self.assertIn("mechanism_match_review_ready", row["allowed_terminal_decisions"])
            self.assertIn(
                "terminal_rejection_duplicate_or_leakage",
                row["allowed_terminal_decisions"],
            )
            self.assertFalse(
                row["source_free_evidence_summary"][
                    "source_context_counted_as_predictive"
                ]
            )
            self.assertFalse(row["ready_for_label_import_after_human_decision"])
            self.assertFalse(row["countable_label_candidate_after_human_decision"])

        self.assertTrue(validation["metadata"]["valid"])
        self.assertEqual(validation["metadata"]["blocker_count"], 0)
        self.assertEqual(validation["metadata"]["pending_human_review_count"], 7)
        self.assertTrue(all(row["valid"] for row in validation["row_validation"]))

    def test_nadp_redox_cofactor_blocker_queue_preserves_source_separation(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_nadp_redox_family_source_free_cofactor_blocker_queue_post_sdr_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        families = {row["family_id"]: row for row in packet["families"]}
        preregistration = packet["extractor_preregistration"]
        baselines = packet["modern_baseline_comparison"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["family_count"], 2)
        self.assertEqual(metadata["source_free_nadp_or_proxy_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["registry_invariant_label_type_counts"],
            {"out_of_scope": 470, "seed_fingerprint": 212},
        )

        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["family_status"], "blocked_with_exact_missing_evidence")
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(decision["source_free_nadp_or_proxy_axis_ready_count"], 0)
        self.assertIn(
            "source_free_nadp_pocket_proxy_pressure_test_not_specificity_sufficient",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(
            set(families),
            {"sdr_nad_p_redox", "akr_nadp_redox"},
        )
        self.assertEqual(
            families["sdr_nad_p_redox"]["source_free_catalytic_axis_resolved_count"],
            5,
        )
        self.assertEqual(
            families["sdr_nad_p_redox"]["source_free_nadp_or_proxy_axis_ready_count"],
            0,
        )
        self.assertEqual(
            families["sdr_nad_p_redox"]["non_target_control_geometry_hit_count"],
            2,
        )
        self.assertEqual(
            families["akr_nadp_redox"]["source_free_akr_axis_ready_count"],
            0,
        )
        self.assertEqual(
            families["akr_nadp_redox"]["cofactor_evidence"][
                "source_traced_proxy_motif_hits_not_predictive"
            ][0]["motif"],
            "VGLG",
        )

        self.assertEqual(
            preregistration["experiment_id"],
            "nadp_redox_cofactor_pocket_proxy_extractor_v1_review_only",
        )
        self.assertEqual(
            preregistration["status"],
            "preregistered_and_pressure_tested_review_only",
        )
        self.assertEqual(
            preregistration["pressure_test_result"],
            "strict_proxy_resolved_positive_like_and_control_rows_not_specificity_sufficient",
        )
        self.assertTrue(preregistration["selection_freeze_required_before_scoring"])
        self.assertIn(
            "UniProt or source prose",
            preregistration["excluded_predictive_inputs"],
        )
        self.assertFalse(baselines["ec_keyword_routing"]["predictive_use_allowed"])
        self.assertFalse(
            baselines["deterministic_sequence_or_motif_baseline"][
                "predictive_use_allowed"
            ]
        )
        self.assertFalse(baselines["foldseek_sidecar"]["available_for_same_frozen_rows"])
        self.assertFalse(
            baselines["esm_or_learned_embedding_sidecar"][
                "available_for_same_frozen_rows"
            ]
        )
        self.assertFalse(baselines["geometry_superiority_claim_supported"])

    def test_sdr_nadp_pocket_proxy_pressure_test_remains_blocked(self) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_sdr_nadp_pocket_proxy_pressure_test_post_blocker_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        rows = {row["row_id"]: row for row in packet["rows"]}
        proxy_rule = packet["proxy_rule"]

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["frozen_row_count"], 14)
        self.assertEqual(metadata["source_free_nad_p_pocket_proxy_resolved_count"], 2)
        self.assertEqual(metadata["positive_like_proxy_resolved_count"], 1)
        self.assertEqual(metadata["non_positive_control_proxy_resolved_count"], 1)
        self.assertEqual(metadata["proxy_axis_ready_for_threshold_calibration_count"], 0)
        self.assertEqual(metadata["source_free_full_sdr_axis_ready_count"], 0)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["family_status"], "blocked_with_exact_missing_evidence")
        self.assertEqual(decision["source_free_nad_p_pocket_proxy_resolved_count"], 2)
        self.assertEqual(decision["non_positive_control_proxy_resolved_count"], 1)
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertIn(
            "strict_sdr_nadp_pocket_proxy_resolves_positive_like_o14756_but_also_external_sdr_control_o75828",
            decision["exact_missing_evidence"],
        )

        self.assertEqual(
            rows["uniprot:O14756"]["pocket_proxy_status"],
            "source_free_sdr_catalytic_axis_with_nad_p_pocket_proxy_review_only",
        )
        self.assertEqual(rows["uniprot:O14756"]["selected_pocket_proxy"]["motif"], "TGCDSGFG")
        self.assertTrue(rows["uniprot:O14756"]["source_free_nad_p_pocket_proxy_resolved"])
        self.assertEqual(rows["uniprot:O75828"]["selected_pocket_proxy"]["motif"], "TGANRGIG")
        self.assertTrue(rows["uniprot:O75828"]["source_free_nad_p_pocket_proxy_resolved"])
        self.assertFalse(rows["m_csa:208"]["source_free_nad_p_pocket_proxy_resolved"])
        self.assertEqual(
            rows["m_csa:208"]["pocket_proxy_status"],
            "source_free_sdr_catalytic_axis_without_nad_p_pocket_proxy",
        )
        self.assertFalse(proxy_rule["threshold_calibration_authorized"])
        self.assertFalse(proxy_rule["production_scoring_authorized"])
        self.assertIn("source active-site annotations", proxy_rule["excluded_predictive_inputs"])

    def test_nadp_redox_source_request_queue_names_exact_resolution_options(self) -> None:
        queue = _load_json(
            ARTIFACTS
            / "v3_nadp_redox_holo_or_specificity_source_request_queue_post_proxy_20260522.json"
        )

        metadata = queue["metadata"]
        decision = queue["decision"]
        rows = {row["row_id"]: row for row in queue["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["request_count"], 3)
        self.assertEqual(metadata["source_free_nadp_or_proxy_axis_ready_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertEqual(decision["terminal_decision"], "needs_new_extractor_or_structure")
        self.assertEqual(decision["family_status"], "blocked_with_exact_missing_evidence")
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(decision["request_count"], 3)
        self.assertIn(
            "o75828_needs_specificity_adjudication_before_strict_sdr_proxy_can_support_any_claim",
            decision["exact_missing_evidence"],
        )

        self.assertTrue(
            rows["uniprot:O14756"]["current_source_free_evidence"][
                "strict_pocket_proxy_resolved"
            ]
        )
        self.assertEqual(
            rows["uniprot:O14756"]["current_source_free_evidence"][
                "selected_proxy_motif"
            ],
            "TGCDSGFG",
        )
        self.assertTrue(
            rows["uniprot:O75828"]["current_source_free_evidence"][
                "strict_pocket_proxy_resolved"
            ]
        )
        self.assertEqual(
            rows["uniprot:O75828"]["request_type"],
            "strict_proxy_specificity_control_adjudication",
        )
        self.assertFalse(
            rows["uniprot:C9JRZ8"]["current_source_free_evidence"][
                "source_traced_vglg_motif_predictive_use_allowed"
            ]
        )
        for row in rows.values():
            self.assertFalse(row["ready_for_label_import_after_resolution"])
            self.assertFalse(row["countable_label_candidate_after_resolution"])

    def test_non_epk_family_index_post_nadp_blocker_keeps_no_breadth_queue(self) -> None:
        index = _load_json(
            ARTIFACTS
            / "v3_non_epk_family_readiness_index_post_nadp_cofactor_blocker_20260522.json"
        )

        metadata = index["metadata"]
        decision = index["decision"]
        blockers = {row["blocker_id"]: row for row in index["cross_family_blockers"]}
        next_items = {row["item"]: row for row in index["recommended_next_main_loop_items"]}

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["family_count"], 6)
        self.assertEqual(metadata["cross_family_blocker_count"], 1)
        self.assertEqual(metadata["source_free_nadp_or_proxy_axis_ready_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])

        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(decision["import_ready_candidate_count"], 0)
        self.assertEqual(decision["countable_label_candidate_count"], 0)
        self.assertEqual(
            decision["cross_family_blocker_status_counts"],
            {"blocked_with_exact_missing_evidence": 1},
        )

        self.assertEqual(
            blockers["nadp_redox_source_free_cofactor_axis"]["families"],
            ["sdr_nad_p_redox", "akr_nadp_redox"],
        )
        self.assertEqual(
            blockers["nadp_redox_source_free_cofactor_axis"][
                "source_free_nadp_or_proxy_axis_ready_count"
            ],
            0,
        )
        self.assertEqual(
            blockers["nadp_redox_source_free_cofactor_axis"]["next_exact_experiment"],
            "source_free_nadp_proxy_specificity_or_holo_structure_review_only",
        )
        self.assertEqual(
            next_items["broad_external_minicampaign"]["status"],
            "do_not_start_by_default",
        )
        self.assertEqual(
            next_items["nadp_redox_source_free_cofactor_proxy"]["status"],
            "proxy_pressure_test_done_source_request_queue_ready",
        )

    def test_post_nadp_cofactor_blocker_zero_import_gate_passes(self) -> None:
        gate = _load_json(
            ARTIFACTS
            / "v3_post_nadp_cofactor_blocker_review_only_zero_import_gate_20260522.json"
        )

        metadata = gate["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(metadata["valid"])
        self.assertEqual(metadata["artifact_count"], 4)
        self.assertEqual(metadata["valid_artifact_count"], 4)
        self.assertEqual(metadata["blocker_count"], 0)
        self.assertFalse(metadata["artifact_migration_files_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        for row in gate["rows"]:
            self.assertTrue(row["valid"])
            self.assertTrue(row["review_only"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)
            self.assertEqual(row["new_external_rows_frozen"], 0)
            self.assertFalse(row["curated_label_registry_edited"])
            self.assertFalse(row["fingerprint_registry_edited"])
            self.assertFalse(row["artifact_upload_or_removal_performed"])

    def test_external_review_ready_terminal_stop_packet_closes_automation_queue(
        self,
    ) -> None:
        packet = _load_json(
            ARTIFACTS
            / "v3_external_review_ready_automation_terminal_stop_packet_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_external_review_ready_automation_terminal_stop_packet_zero_import_gate_20260522.json"
        )

        metadata = packet["metadata"]
        decision = packet["decision"]
        families = {
            row["target_current_fingerprint_lane"]: row
            for row in packet["family_readiness_packets"]
        }

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["candidate_count"], 7)
        self.assertEqual(metadata["family_count"], 3)
        self.assertEqual(metadata["mechanism_match_review_ready_count"], 7)
        self.assertEqual(metadata["pending_human_review_count"], 7)
        self.assertEqual(metadata["automation_actionable_evidence_blocker_count"], 0)
        self.assertEqual(metadata["source_free_geometry_above_floor_count"], 7)
        self.assertEqual(metadata["foldseek_current_countable_high_tm_hit_count"], 0)
        self.assertEqual(metadata["uniref_current_reference_clear_count"], 7)
        self.assertEqual(metadata["source_context_counted_as_predictive_count"], 0)
        self.assertEqual(metadata["esm_or_learned_embedding_sidecar_available_count"], 0)
        self.assertFalse(metadata["geometry_superiority_claim"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["registry_invariant_label_count"], 682)
        self.assertEqual(
            metadata["registry_invariant_label_type_counts"],
            {"seed_fingerprint": 212, "out_of_scope": 470},
        )
        self.assertEqual(metadata["external_imported_seed_fingerprint_labels"], [])

        self.assertEqual(
            decision["packet_status"],
            "automation_terminal_external_review_ready_queue_closed_no_import",
        )
        self.assertEqual(
            decision["terminal_decision_counts"],
            {
                "mechanism_match_review_ready": 7,
                "ambiguous_needs_expert_review": 0,
                "needs_new_extractor_or_structure": 0,
                "terminal_rejection_duplicate_or_leakage": 0,
                "terminal_rejection_wrong_scope": 0,
                "terminal_rejection_insufficient_evidence": 0,
            },
        )
        self.assertTrue(decision["human_action_required"])
        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertIn("explicit_human_expert", decision["exact_blocker"])

        self.assertEqual(
            set(families),
            {
                "heme_peroxidase_oxidase",
                "metal_dependent_hydrolase",
                "ser_his_acid_hydrolase",
            },
        )
        self.assertEqual(families["heme_peroxidase_oxidase"]["row_count"], 4)
        self.assertEqual(families["metal_dependent_hydrolase"]["row_count"], 2)
        self.assertEqual(families["ser_his_acid_hydrolase"]["row_count"], 1)
        self.assertEqual(
            families["metal_dependent_hydrolase"][
                "metal_phosphate_pocket_proxy_resolved_count"
            ],
            2,
        )
        for family in families.values():
            self.assertEqual(
                family["family_status"],
                "source_free_mechanism_match_review_ready_pending_human_action",
            )
            self.assertEqual(family["terminal_decision"], "mechanism_match_review_ready")
            self.assertEqual(family["foldseek_current_countable_high_tm_hit_count"], 0)
            self.assertEqual(family["import_ready_candidate_count"], 0)
            self.assertEqual(family["countable_label_candidate_count"], 0)
            self.assertFalse(family["source_context_counted_as_predictive"])

        for row in packet["rows"]:
            self.assertEqual(row["terminal_decision"], "mechanism_match_review_ready")
            self.assertEqual(row["human_decision_status"], "pending_human_review")
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["source_context_counted_as_predictive"])
            self.assertFalse(
                row["modern_baseline_snapshot"][
                    "ec_keyword_routing_counted_as_predictive"
                ]
            )
            self.assertFalse(
                row["modern_baseline_snapshot"][
                    "deterministic_sequence_or_kmer_counted_as_predictive"
                ]
            )
            self.assertFalse(
                row["modern_baseline_snapshot"][
                    "esm_or_learned_embedding_sidecar_available"
                ]
            )
            self.assertFalse(
                row["modern_baseline_snapshot"]["geometry_superiority_claim_made"]
            )

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 1)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 1)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_non_epk_family_index_post_external_stop_is_no_breadth(self) -> None:
        index = _load_json(
            ARTIFACTS
            / "v3_non_epk_family_readiness_index_post_external_stop_20260522.json"
        )
        gate = _load_json(
            ARTIFACTS / "v3_post_external_stop_review_only_zero_import_gate_20260522.json"
        )

        metadata = index["metadata"]
        decision = index["decision"]
        rows = {row["family_id"]: row for row in index["rows"]}
        next_items = {
            row["item"]: row for row in decision["recommended_next_main_loop_items"]
        }

        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["uses_existing_artifacts_only"])
        self.assertEqual(metadata["new_external_rows_frozen"], 0)
        self.assertEqual(metadata["family_count"], 17)
        self.assertEqual(
            metadata["family_group_counts"],
            {
                "external_mechanism_match_review_ready": 3,
                "non_atp_non_epk_family_readiness": 6,
                "atp_phosphoryl_transfer_non_epk": 8,
            },
        )
        self.assertEqual(metadata["human_action_blocked_family_count"], 3)
        self.assertEqual(metadata["closed_review_only_no_go_family_count"], 8)
        self.assertEqual(metadata["blocked_with_exact_missing_evidence_family_count"], 5)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])

        self.assertFalse(decision["label_import_authorized"])
        self.assertFalse(decision["production_fingerprint_promotion_authorized"])
        self.assertFalse(decision["start_new_broad_external_minicampaign"])
        self.assertEqual(
            next_items["external_mechanism_match_rows"]["status"],
            "blocked_on_human_accept_reject_or_ambiguous_action",
        )
        self.assertEqual(
            next_items["broad_external_minicampaign"]["status"],
            "do_not_start_by_default",
        )

        for family_id in (
            "askha",
            "atp_grasp",
            "dnk",
            "ghkl",
            "ghmp",
            "ndk",
            "pfka",
            "pfkb",
        ):
            self.assertEqual(rows[family_id]["readiness_status"], "closed_review_only_no_go")
            self.assertEqual(rows[family_id]["source_free_axis_ready_count"], 0)
            self.assertFalse(rows[family_id]["ready_for_label_import"])
            self.assertFalse(rows[family_id]["ready_for_production_scoring"])
            self.assertFalse(
                rows[family_id]["ready_to_expand_positive_fingerprint_universe"]
            )

        for family_id in (
            "heme_peroxidase_oxidase",
            "metal_dependent_hydrolase",
            "ser_his_acid_hydrolase",
        ):
            self.assertEqual(
                rows[family_id]["readiness_status"],
                "source_free_mechanism_match_review_ready_pending_human_action",
            )
            self.assertEqual(
                rows[family_id]["next_exact_action"],
                "human_accept_reject_or_ambiguous_action_before_any_label_path",
            )

        self.assertEqual(rows["sdr_nad_p_redox"]["readiness_status"], "blocked_with_exact_missing_evidence")
        self.assertEqual(rows["akr_nadp_redox"]["readiness_status"], "needs_new_extractor_or_structure")

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 2)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 2)
        self.assertEqual(gate["metadata"]["blocker_count"], 0)
        for row in gate["rows"]:
            self.assertEqual(row["import_ready_candidate_count"], 0)
            self.assertEqual(row["countable_label_candidate_count"], 0)

    def test_mcsa_positive_accepted_import_readiness_preserves_caveats(self) -> None:
        readiness = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_accepted_import_gate_readiness_12_20260523.json"
        )

        metadata = readiness["metadata"]
        decision = readiness["decision"]
        rows = {row["entry_id"]: row for row in readiness["rows"]}

        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(metadata["accepted_candidate_count"], 12)
        self.assertEqual(metadata["mechanically_can_enter_import_preview_now_count"], 9)
        self.assertEqual(metadata["blocked_by_acceptance_caveat_count"], 3)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["canonical_countable_label_count_invariant"], 682)
        self.assertEqual(metadata["production_fingerprint_universe_count_invariant"], 8)

        self.assertEqual(
            decision["ready_entry_ids"],
            [
                "m_csa:599",
                "m_csa:623",
                "m_csa:636",
                "m_csa:706",
                "m_csa:812",
                "m_csa:865",
                "m_csa:892",
                "m_csa:917",
                "m_csa:998",
            ],
        )
        self.assertEqual(
            decision["blocked_by_caveat_entry_ids"],
            ["m_csa:777", "m_csa:784", "m_csa:904"],
        )
        self.assertFalse(rows["m_csa:777"]["mechanically_can_enter_import_preview_now"])
        self.assertEqual(rows["m_csa:777"]["current_1025_score"], 0.4107)
        self.assertEqual(rows["m_csa:777"]["prior_score_excluded_from_1025_gate"], 0.5307)
        self.assertIn(
            "prior_1000_score_must_not_be_used_for_1025_gate",
            rows["m_csa:777"]["caveat_blockers"],
        )
        self.assertFalse(rows["m_csa:784"]["score_clears_current_threshold"])
        self.assertFalse(rows["m_csa:904"]["score_clears_current_threshold"])

    def test_mcsa_positive_followup_artifacts_resolve_or_block_holds(self) -> None:
        apo_scan = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_hold_apo_alternate_structure_scan_5_20260523.json"
        )
        apo_plan = _load_json(
            ARTIFACTS / "v3_mcsa_positive_hold_apo_holo_override_plan_5_20260523.json"
        )
        geometry = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_hold_geometry_locality_resolution_3_20260523.json"
        )
        residue = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_residue_mapping_resolution_m_csa_771_20260523.json"
        )
        schema = _load_json(
            ARTIFACTS / "v3_mcsa_positive_schema_decision_note_m_csa_737_20260523.json"
        )
        gate = _load_json(
            ARTIFACTS
            / "v3_post_mcsa_positive_followup_review_only_zero_import_gate_20260523.json"
        )

        self.assertTrue(apo_scan["metadata"]["review_only"])
        self.assertEqual(apo_scan["metadata"]["scanned_structure_count"], 62)
        self.assertEqual(apo_scan["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            apo_scan["metadata"]["local_expected_family_hit_entry_ids"],
            ["m_csa:577", "m_csa:641", "m_csa:897"],
        )

        plan_rows = {row["entry_id"]: row for row in apo_plan["rows"]}
        self.assertEqual(apo_plan["decision"]["selected_pdb_replacement_candidate_count"], 3)
        self.assertEqual(apo_plan["decision"]["blocked_no_local_remapped_holo_alternate_count"], 2)
        self.assertEqual(plan_rows["m_csa:577"]["recommended_replacement_pdb"], "1AWB")
        self.assertEqual(plan_rows["m_csa:641"]["recommended_replacement_pdb"], "1J7N")
        self.assertEqual(plan_rows["m_csa:897"]["recommended_replacement_pdb"], "1H56")
        self.assertIsNone(plan_rows["m_csa:836"]["recommended_replacement_pdb"])
        self.assertIn("3SLP/3SM4/4WUZ", plan_rows["m_csa:836"]["exact_blocker"])
        self.assertIsNone(plan_rows["m_csa:996"]["recommended_replacement_pdb"])
        self.assertIn("5O6Y", plan_rows["m_csa:996"]["exact_blocker"])

        geometry_rows = {row["entry_id"]: row for row in geometry["rows"]}
        self.assertEqual(
            geometry_rows["m_csa:657"]["resolution_status"],
            "resolved_hold_cofactor_locality_not_both_scored_residues_direct_ligands",
        )
        self.assertIn("Glu131", geometry_rows["m_csa:657"]["exact_reason"])
        self.assertEqual(
            geometry_rows["m_csa:611"]["resolution_status"],
            "kept_hold_open_or_loose_conformation",
        )
        self.assertEqual(
            geometry_rows["m_csa:1001"]["resolution_status"],
            "kept_hold_oligomer_or_role_pair_geometry",
        )

        self.assertEqual(
            residue["decision"]["alternate_structure_candidate_with_ser103"],
            ["2D0D"],
        )
        self.assertEqual(
            residue["rows"][0]["recommended_alternate_structure_request"],
            "2D0D",
        )
        self.assertFalse(residue["decision"]["promote_now"])

        self.assertEqual(
            schema["decision"]["schema_decision"],
            "keep_held_as_dual_plp_adenosylcobalamin_schema_gap",
        )
        self.assertTrue(schema["decision"]["do_not_create_production_fingerprint"])
        self.assertFalse(schema["decision"]["production_fingerprint_promotion_authorized"])

        self.assertTrue(gate["metadata"]["valid"])
        self.assertEqual(gate["metadata"]["artifact_count"], 6)
        self.assertEqual(gate["metadata"]["valid_artifact_count"], 6)
        self.assertEqual(gate["metadata"]["import_ready_candidate_count"], 0)
        self.assertEqual(gate["metadata"]["countable_label_candidate_count"], 0)

    def test_mcsa_positive_clean9_import_preview_records_gated_import(self) -> None:
        preview = _load_json(
            ARTIFACTS / "v3_mcsa_positive_clean9_import_preview_20260523.json"
        )

        metadata = preview["metadata"]
        decision = preview["decision"]
        rows = {row["entry_id"]: row for row in preview["rows"]}

        expected_ids = [
            "m_csa:599",
            "m_csa:623",
            "m_csa:636",
            "m_csa:706",
            "m_csa:812",
            "m_csa:865",
            "m_csa:892",
            "m_csa:917",
            "m_csa:998",
        ]
        self.assertEqual(metadata["exact_entry_ids"], expected_ids)
        self.assertEqual(metadata["baseline_countable_label_count"], 682)
        self.assertEqual(metadata["preview_countable_label_count"], 691)
        self.assertEqual(metadata["canonical_countable_label_count_after_import"], 691)
        self.assertEqual(metadata["actual_label_count_delta"], 9)
        self.assertTrue(metadata["canonical_registry_import_performed"])
        self.assertTrue(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["artifact_upload_or_removal_performed"])
        self.assertFalse(metadata["removal_allowed_set_true"])
        self.assertEqual(metadata["external_seed_fingerprint_label_count"], 0)
        self.assertEqual(metadata["production_fingerprint_universe_count"], 8)
        self.assertEqual(metadata["gate_summary"]["label_factory_passed_gate_count"], 21)
        self.assertEqual(metadata["gate_summary"]["label_factory_gate_count"], 21)
        self.assertEqual(metadata["gate_summary"]["hard_negative_count"], 0)
        self.assertEqual(metadata["gate_summary"]["near_miss_count"], 0)
        self.assertEqual(metadata["gate_summary"]["out_of_scope_false_non_abstentions"], 0)

        self.assertTrue(decision["ready_for_label_import"])
        self.assertTrue(decision["label_import_authorized_by_gates"])
        self.assertEqual(decision["label_import_executed_for_exact_entry_ids"], expected_ids)
        self.assertEqual(set(rows), set(expected_ids))
        for row in rows.values():
            self.assertTrue(row["eligible_for_actual_label_import"])
            self.assertTrue(row["actual_label_imported_to_canonical_registry"])
            self.assertTrue(row["preview_label_matches_canonical_label"])

    def test_mcsa_positive_holo_override_preview_stays_separate(self) -> None:
        preview = _load_json(
            ARTIFACTS / "v3_mcsa_positive_holo_override_import_preview_20260523.json"
        )

        metadata = preview["metadata"]
        decision = preview["decision"]
        rows = {row["entry_id"]: row for row in preview["rows"]}

        self.assertEqual(metadata["post_clean9_registry_label_count"], 691)
        self.assertEqual(
            metadata["exact_entry_ids"],
            ["m_csa:577", "m_csa:641", "m_csa:897"],
        )
        self.assertTrue(metadata["separate_from_clean9_import"])
        self.assertEqual(metadata["selected_pdb_override_applied_count"], 3)
        self.assertEqual(metadata["hard_negative_count"], 0)
        self.assertEqual(metadata["near_miss_count"], 0)
        self.assertEqual(metadata["out_of_scope_false_non_abstentions"], 0)
        self.assertEqual(metadata["actionable_in_scope_failure_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(
            metadata["preserved_blocked_hold_apo_entry_ids"],
            ["m_csa:836", "m_csa:996"],
        )

        self.assertTrue(decision["gate_preview_passed_for_selected_pdb_geometry"])
        self.assertFalse(decision["label_import_authorized_now"])
        self.assertTrue(decision["do_not_mix_with_clean9_import"])
        self.assertEqual(rows["m_csa:577"]["override_pdb_id"], "1AWB")
        self.assertEqual(rows["m_csa:641"]["override_pdb_id"], "1J7N")
        self.assertEqual(rows["m_csa:897"]["override_pdb_id"], "1H56")
        for row in rows.values():
            self.assertEqual(row["top1_fingerprint_id"], "metal_dependent_hydrolase")
            self.assertGreaterEqual(row["top1_score"], 0.59)
            self.assertFalse(row["eligible_for_actual_label_import"])
            self.assertFalse(row["actual_label_imported_to_canonical_registry"])

    def test_mcsa_positive_holo_override_accept_decision_is_gate_input_only(
        self,
    ) -> None:
        decision = _load_json(
            ARTIFACTS / "v3_mcsa_positive_holo_override_accept_decision_3_20260523.json"
        )

        metadata = decision["metadata"]
        rows = {row["entry_id"]: row for row in decision["rows"]}
        review_items = {item["entry_id"]: item for item in decision["review_items"]}
        expected_ids = ["m_csa:577", "m_csa:641", "m_csa:897"]

        self.assertEqual(metadata["exact_entry_ids"], expected_ids)
        self.assertEqual(metadata["baseline_canonical_countable_label_count"], 691)
        self.assertEqual(metadata["expected_preview_countable_label_count_if_gates_pass"], 694)
        self.assertEqual(metadata["decision_counts"], {"accept_label": 3})
        self.assertTrue(metadata["ready_for_dedicated_import_gate"])
        self.assertTrue(metadata["not_new_human_expert_review"])
        self.assertFalse(metadata["post_preview_human_confirmation_required_before_dedicated_gate"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])

        self.assertEqual(set(rows), set(expected_ids))
        self.assertEqual(set(review_items), set(expected_ids))
        self.assertEqual(rows["m_csa:577"]["override_pdb_id"], "1AWB")
        self.assertEqual(rows["m_csa:641"]["override_pdb_id"], "1J7N")
        self.assertEqual(rows["m_csa:897"]["override_pdb_id"], "1H56")
        for entry_id in expected_ids:
            row = rows[entry_id]
            item = review_items[entry_id]
            item_decision = item["decision"]
            self.assertTrue(row["eligible_for_dedicated_import_gate"])
            self.assertEqual(row["post_preview_accept_decision"], "accept_label")
            self.assertTrue(row["not_new_human_expert_review"])
            self.assertEqual(item_decision["action"], "accept_label")
            self.assertEqual(item_decision["review_status"], "automation_curated")
            self.assertEqual(
                item_decision["reviewer"],
                "automation_post_preview_synthesis_from_prior_vivek_review",
            )
            self.assertEqual(item_decision["fingerprint_id"], "metal_dependent_hydrolase")
            self.assertEqual(item_decision["label_type"], "seed_fingerprint")
            self.assertIn("holo_override_resolves", item_decision["local_evidence_resolution"])

    def test_mcsa771_2d0d_review_resolves_ser103_without_import(self) -> None:
        review = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_m_csa771_2d0d_noncanonical_review_20260523.json"
        )
        plan = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_m_csa771_2d0d_gate_preview_plan_20260523.json"
        )

        metadata = review["metadata"]
        row = review["rows"][0]
        ser103 = row["catalytic_ser103_evidence"]

        self.assertEqual(metadata["entry_id"], "m_csa:771")
        self.assertEqual(metadata["alternate_pdb_id"], "2D0D")
        self.assertTrue(metadata["catalytic_ser103_present"])
        self.assertTrue(metadata["catalytic_ser103_maps_to_m_csa_nucleophile"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(row["target_fingerprint_preview"], "ser_his_acid_hydrolase")
        self.assertEqual(row["top1_score"], 0.8933)
        self.assertEqual(ser103["code"], "SER")
        self.assertEqual(ser103["resid"], "103")
        self.assertIn("nucleophile", ser103["roles"])
        self.assertTrue(ser103["maps_to_catalytic_nucleophile"])
        self.assertFalse(row["eligible_for_actual_label_import"])

        self.assertTrue(plan["decision"]["gate_preview_passed_for_noncanonical_geometry"])
        self.assertTrue(plan["decision"]["do_not_import_in_same_step"])
        self.assertFalse(plan["decision"]["label_import_authorized_now"])
        self.assertEqual(plan["metadata"]["hard_negative_count"], 0)
        self.assertEqual(plan["metadata"]["near_miss_count"], 0)
        self.assertEqual(plan["metadata"]["out_of_scope_false_non_abstentions"], 0)
        self.assertEqual(plan["metadata"]["actionable_in_scope_failure_count"], 0)

    def test_mcsa771_2d0d_vivek_accept_decision_is_gate_input_only(self) -> None:
        decision = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_m_csa771_2d0d_vivek_accept_decision_20260523.json"
        )

        metadata = decision["metadata"]
        item = decision["review_items"][0]
        review_decision = item["decision"]
        context = item["queue_context"]

        self.assertEqual(metadata["entry_id"], "m_csa:771")
        self.assertEqual(metadata["reviewer"], "vivek")
        self.assertEqual(metadata["decision_counts"], {"accept_label": 1})
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(metadata["dedicated_gates_required_before_import"])
        self.assertTrue(decision["decision"]["do_not_import_without_dedicated_gates"])

        self.assertEqual(item["entry_id"], "m_csa:771")
        self.assertEqual(review_decision["action"], "accept_label")
        self.assertEqual(review_decision["reviewer"], "vivek")
        self.assertEqual(review_decision["review_status"], "expert_reviewed")
        self.assertEqual(review_decision["fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertEqual(review_decision["label_type"], "seed_fingerprint")
        self.assertEqual(review_decision["tier"], "silver")
        self.assertEqual(context["alternate_pdb_id"], "2D0D")
        self.assertEqual(context["top1_score"], 0.8933)
        self.assertEqual(context["top1_counterevidence_reasons"], [])
        self.assertEqual(
            context["pyMOL_distance_observations"][
                "Ser103_OG_to_His252_NE2_angstrom"
            ],
            "~2.6-3.1",
        )
        self.assertEqual(
            context["pyMOL_distance_observations"][
                "His252_ND1_to_Asp224_OD_angstrom"
            ],
            "~3.2",
        )

    def test_nucleotide_product_counterevidence_probe_is_general_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ARTIFACTS
            / "v3_mcsa_positive_nucleotide_product_counterevidence_rule_probe_20260523.json"
        )

        metadata = probe["metadata"]
        decision = probe["decision"]
        rows = {row["entry_id"]: row for row in probe["rows"]}

        self.assertTrue(metadata["candidate_rule_general_not_candidate_specific"])
        self.assertFalse(metadata["production_rule_activated"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["product_context_exception_candidate_entry_ids"],
            ["m_csa:784", "m_csa:904"],
        )
        self.assertEqual(
            metadata["retain_counterevidence_control_entry_ids"],
            ["m_csa:603", "m_csa:640", "m_csa:647"],
        )
        self.assertFalse(decision["unblock_m_csa_784_now"])
        self.assertFalse(decision["unblock_m_csa_904_now"])

        for entry_id in ("m_csa:784", "m_csa:904"):
            row = rows[entry_id]
            self.assertEqual(
                row["stress_panel_expected_decision"],
                "product_context_exception_candidate",
            )
            self.assertTrue(
                row[
                    "would_suppress_nucleotide_transfer_counterevidence_under_candidate_rule"
                ]
            )
            self.assertIn("AMP", row["product_or_partial_nucleotide_codes"])
            self.assertEqual(row["gamma_or_transfer_nucleotide_codes"], [])

        for entry_id in ("m_csa:603", "m_csa:640", "m_csa:647"):
            row = rows[entry_id]
            self.assertEqual(
                row["stress_panel_expected_decision"],
                "retain_nucleotide_transfer_counterevidence",
            )
            self.assertFalse(
                row[
                    "would_suppress_nucleotide_transfer_counterevidence_under_candidate_rule"
                ]
            )

    def test_mcsa_ai_visual_amp_nontransfer_discriminator_exact5_review_only(
        self,
    ) -> None:
        discriminator = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_amp_nontransfer_discriminator_eval_20260525.json"
        )

        metadata = discriminator["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["production_rule_activated"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["exact_entry_ids"],
            ["m_csa:751", "m_csa:564", "m_csa:833", "m_csa:780", "m_csa:656"],
        )
        self.assertEqual(metadata["row_count"], 5)
        self.assertEqual(metadata["control_assertion_count"], 9)

        contract = discriminator["discriminator_contract"]
        self.assertTrue(contract["scope_requires_mcsa_annotated_catalytic_pocket"])
        self.assertTrue(contract["regulatory_or_allosteric_amp_excluded"])
        self.assertEqual(
            set(contract["required_transfer_controls"]),
            {
                "aminoacyl-tRNA synthetase",
                "DNA/RNA ligase including covalent AMP-Lys autoadenylation without PPi",
                "ANL/acyl-CoA synthetase or NRPS A-domain",
                "NMNAT",
                "asparagine synthetase or related ATP-dependent amide ligase",
            },
        )
        self.assertEqual(
            set(contract["required_edge_or_out_of_scope_controls"]),
            {
                "adenylate kinase EC 2.7.4.3",
                "Nudix Ap4A hydrolase",
                "allosteric/regulatory AMP",
                "aaRS editing-site AMP",
            },
        )
        self.assertIn("review-only/ambiguous", contract["terminal_ambiguity_rule"])

        controls = {row["control_id"]: row for row in discriminator["control_evaluation"]}
        self.assertEqual(set(controls), {
            "aminoacyl_tRNA_synthetase_synthetic_site",
            "dna_rna_ligase_covalent_amp_lys_without_ppi",
            "anl_acyl_coa_synthetase_or_nrps_a_domain",
            "nmnat",
            "asparagine_synthetase_or_atp_dependent_amide_ligase",
            "adenylate_kinase_ec_2_7_4_3",
            "nudix_ap4a_hydrolase",
            "allosteric_or_regulatory_amp",
            "aars_editing_site_amp",
        })
        for control_id in [
            "aminoacyl_tRNA_synthetase_synthetic_site",
            "dna_rna_ligase_covalent_amp_lys_without_ppi",
            "anl_acyl_coa_synthetase_or_nrps_a_domain",
            "nmnat",
            "asparagine_synthetase_or_atp_dependent_amide_ligase",
        ]:
            self.assertEqual(
                controls[control_id]["expected_action"],
                "retain_nucleotide_transfer_ligand_context",
            )
        self.assertEqual(
            controls["allosteric_or_regulatory_amp"]["expected_action"],
            "do_not_classify_as_catalytic_nontransfer",
        )

        rows = {row["entry_id"]: row for row in discriminator["rows"]}
        self.assertEqual(
            discriminator["summary"]["import_candidate_entry_ids"],
            [],
        )
        self.assertEqual(
            discriminator["summary"]["true_reject_entry_ids"],
            ["m_csa:751", "m_csa:833", "m_csa:780", "m_csa:656"],
        )
        self.assertEqual(discriminator["summary"]["review_only_entry_ids"], ["m_csa:564"])
        self.assertEqual(
            discriminator["summary"]["classification_counts"],
            {
                "ambiguous_review_only": 1,
                "true_transfer_atpase_helicase_kinase_counterevidence": 4,
            },
        )

        self.assertEqual(
            rows["m_csa:564"]["discriminator_classification"],
            "ambiguous_review_only",
        )
        self.assertIn(
            "selected structure has no local/structure metal cofactor evidence",
            rows["m_csa:564"]["terminal_reason"],
        )
        for entry_id in ("m_csa:751", "m_csa:833", "m_csa:780", "m_csa:656"):
            row = rows[entry_id]
            self.assertEqual(
                row["discriminator_classification"],
                "true_transfer_atpase_helicase_kinase_counterevidence",
            )
            self.assertEqual(
                row["row_decision"],
                "true_reject_current_target_route_future_family",
            )
            self.assertFalse(row["is_import_candidate"])
            self.assertTrue(row["future_family_route"])
            self.assertTrue(row["preserve_for_learning"])

    def test_mcsa_ai_visual_apo_holo_exact5_scan_finds_no_local_holo_swaps(
        self,
    ) -> None:
        remediation = _load_json(
            ARTIFACTS / "v3_mcsa_ai_visual_apo_holo_exact5_remediation_20260525.json"
        )
        scan = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_apo_holo_exact5_alternate_structure_scan_20260525.json"
        )
        audit = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_apo_holo_exact5_holo_preference_audit_20260525.json"
        )
        overrides = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_apo_holo_exact5_selected_pdb_overrides_20260525.json"
        )

        exact_ids = ["m_csa:952", "m_csa:794", "m_csa:671", "m_csa:644", "m_csa:832"]
        self.assertTrue(remediation["metadata"]["review_only"])
        self.assertFalse(remediation["metadata"]["ready_for_label_import"])
        self.assertEqual(remediation["metadata"]["exact_entry_ids"], exact_ids)
        self.assertEqual([row["entry_id"] for row in remediation["rows"]], exact_ids)
        self.assertTrue(
            all(
                row["remediation_bucket"] == "alternate_pdb_ligand_scan"
                for row in remediation["rows"]
            )
        )

        scan_meta = scan["metadata"]
        self.assertEqual(scan_meta["source_method"], "exact_row_review_debt_remediation_filter")
        self.assertEqual(scan_meta["scanned_entry_count"], 5)
        self.assertEqual(scan_meta["candidate_entry_count"], 5)
        self.assertEqual(scan_meta["scanned_structure_count"], 37)
        self.assertEqual(scan_meta["unscanned_structure_count"], 0)
        self.assertTrue(scan_meta["all_candidate_structures_scanned"])
        self.assertEqual(scan_meta["fetch_failure_count"], 0)
        self.assertEqual(scan_meta["expected_family_hit_entry_ids"], ["m_csa:644"])
        self.assertEqual(scan_meta["local_expected_family_hit_entry_ids"], [])
        self.assertEqual(
            scan_meta["local_expected_family_hit_from_remap_entry_ids"],
            [],
        )
        self.assertEqual(
            scan_meta["structure_wide_hit_without_local_support_entry_ids"],
            ["m_csa:644"],
        )
        self.assertEqual(
            scan_meta["scan_outcome_counts"],
            {
                "alternate_structure_has_expected_cofactor_candidate": 1,
                "no_expected_cofactor_in_scanned_structures": 4,
            },
        )

        scan_rows = {row["entry_id"]: row for row in scan["rows"]}
        self.assertTrue(scan_rows["m_csa:644"]["alternate_structure_expected_family_observed"])
        self.assertFalse(scan_rows["m_csa:644"]["local_active_site_expected_family_observed"])
        self.assertEqual(scan_rows["m_csa:644"]["alternate_pdb_with_remapped_positions_count"], 18)
        for entry_id in ("m_csa:952", "m_csa:794", "m_csa:671", "m_csa:832"):
            self.assertFalse(
                scan_rows[entry_id]["alternate_structure_expected_family_observed"]
            )
            self.assertFalse(
                scan_rows[entry_id]["local_active_site_expected_family_observed"]
            )

        audit_meta = audit["metadata"]
        self.assertEqual(audit_meta["audited_entry_count"], 5)
        self.assertEqual(audit_meta["swap_recommended_count"], 0)
        self.assertEqual(audit_meta["already_holo_entry_count"], 0)
        self.assertEqual(audit_meta["no_holo_alternate_entry_count"], 5)
        self.assertEqual(
            audit_meta["no_holo_alternate_entry_ids"],
            ["m_csa:644", "m_csa:671", "m_csa:794", "m_csa:832", "m_csa:952"],
        )
        for row in audit["rows"]:
            self.assertEqual(row["recommendation"], "no_swap_no_holo_alternate")
            self.assertIsNone(row["recommended_pdb_id"])
            self.assertEqual(row["alternative_holo_candidate_count"], 0)
            self.assertIn("no scanned alternate PDB provides it", row["recommendation_rationale"])

        override_meta = overrides["metadata"]
        self.assertEqual(override_meta["ready_to_apply_count"], 0)
        self.assertEqual(override_meta["ready_to_apply_entry_ids"], [])
        self.assertEqual(override_meta["blocked_entry_count"], 0)
        self.assertEqual(override_meta["countable_label_candidate_count"], 0)
        self.assertEqual(overrides["rows"], [])

    def test_mcsa_ai_visual_loose_geometry_policy_exact4_stays_review_only(
        self,
    ) -> None:
        policy = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_loose_geometry_policy_exact4_20260525.json"
        )

        metadata = policy["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["production_policy_activated"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertEqual(
            metadata["exact_entry_ids"],
            ["m_csa:976", "m_csa:847", "m_csa:642", "m_csa:844"],
        )
        self.assertEqual(metadata["row_count"], 4)

        contract = policy["policy_contract"]
        self.assertIn("cannot authorize countable labels", contract["no_import_rule"])
        self.assertIn("dedicated label-factory gates", contract["admissible_future_use"])
        self.assertIn("exact-row current-target", contract["broad_call_guardrail"])

        self.assertEqual(policy["summary"]["import_candidate_entry_ids"], [])
        self.assertEqual(policy["summary"]["countable_label_candidate_entry_ids"], [])
        self.assertEqual(
            policy["summary"]["policy_call_counts"],
            {
                "ambiguous_review_only_current_metal_hydrolase_target": 2,
                "reject_current_metal_hydrolase_geometry; route_ATPase_family": 1,
                "reject_current_ser_his_seed_geometry; route_future_glycoside_or_unrepresented_family": 1,
            },
        )

        rows = {row["entry_id"]: row for row in policy["rows"]}
        expected_distances = {
            "m_csa:976": 20.114,
            "m_csa:847": 22.31,
            "m_csa:642": 31.492,
            "m_csa:844": 26.739,
        }
        for entry_id, distance in expected_distances.items():
            row = rows[entry_id]
            self.assertEqual(row["blocker_bucket"], "loose_open_or_interdomain_geometry")
            self.assertEqual(row["visual_focus_distance_angstrom"], distance)
            self.assertFalse(row["import_candidate"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertTrue(row["preserve_for_learning"])
            self.assertTrue(row["terminal_reason"])
            self.assertTrue(row["future_family_route"])

        self.assertIn(
            "ATPase",
            rows["m_csa:642"]["future_family_route"],
        )
        self.assertIn(
            "glycoside hydrolase",
            rows["m_csa:976"]["future_family_route"],
        )

    def test_mcsa_ai_visual_future_family_backlog_exact5_does_not_edit_schema(
        self,
    ) -> None:
        backlog = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_future_family_ontology_backlog_exact5_20260525.json"
        )

        metadata = backlog["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ontology_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertEqual(
            metadata["exact_entry_ids"],
            ["m_csa:793", "m_csa:755", "m_csa:817", "m_csa:597", "m_csa:729"],
        )
        self.assertEqual(metadata["row_count"], 5)

        contract = backlog["backlog_contract"]
        self.assertIn("Exact current-target mismatch", contract["scope"])
        self.assertIn("does not create labels", contract["no_import_rule"])
        self.assertIn("review-derived", contract["prediction_leakage_rule"])

        self.assertEqual(backlog["summary"]["import_candidate_entry_ids"], [])
        self.assertEqual(backlog["summary"]["countable_label_candidate_entry_ids"], [])
        self.assertEqual(backlog["summary"]["ontology_edit_candidate_count_now"], 0)
        self.assertEqual(backlog["summary"]["fingerprint_edit_candidate_count_now"], 0)
        self.assertEqual(
            backlog["summary"]["ontology_backlog_route_counts"],
            {
                "cysteine_protease_Cys_His_Asp_hydrolase_family": 2,
                "glycoside_hydrolase_GH18_or_substrate_assisted_family": 1,
                "glycoside_hydrolase_family": 1,
                "transferase_or_thioester_transfer_family": 1,
            },
        )

        rows = {row["entry_id"]: row for row in backlog["rows"]}
        for row in rows.values():
            self.assertEqual(
                row["blocker_bucket"],
                "wrong_fingerprint_or_future_ontology_family",
            )
            self.assertEqual(row["route_status"], "future_family_schema_needed")
            self.assertFalse(row["import_candidate"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["ontology_edited"])
            self.assertFalse(row["fingerprint_edited"])
            self.assertTrue(row["preserve_for_learning"])
            self.assertTrue(row["terminal_reason"])

        self.assertEqual(
            rows["m_csa:597"]["ontology_backlog_route"],
            "cysteine_protease_Cys_His_Asp_hydrolase_family",
        )
        self.assertEqual(
            rows["m_csa:793"]["ontology_backlog_route"],
            "glycoside_hydrolase_family",
        )

    def test_mcsa_ai_visual_true_reject_hard_negatives_are_current_target_only(
        self,
    ) -> None:
        hard = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_true_reject_hard_negative_signal_exact5_20260525.json"
        )

        metadata = hard["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertEqual(
            metadata["exact_entry_ids"],
            ["m_csa:841", "m_csa:658", "m_csa:827", "m_csa:774", "m_csa:831"],
        )
        self.assertEqual(metadata["row_count"], 5)

        contract = hard["hard_negative_contract"]
        self.assertIn("current target only", contract["negative_scope_rule"])
        self.assertIn("not positive seeds", contract["future_family_rule"])
        self.assertIn("forbidden as direct model input", contract["prediction_leakage_rule"])
        self.assertIn("No true-reject row", contract["import_rule"])

        self.assertEqual(
            hard["summary"]["current_target_hard_negative_entry_ids"],
            ["m_csa:841", "m_csa:658", "m_csa:827", "m_csa:774", "m_csa:831"],
        )
        self.assertEqual(hard["summary"]["global_negative_entry_ids"], [])
        self.assertEqual(hard["summary"]["import_candidate_entry_ids"], [])
        self.assertEqual(hard["summary"]["countable_label_candidate_entry_ids"], [])
        self.assertEqual(
            hard["summary"]["target_fingerprint_counts"],
            {"metal_dependent_hydrolase": 1, "ser_his_acid_hydrolase": 4},
        )

        rows = {row["entry_id"]: row for row in hard["rows"]}
        for row in rows.values():
            self.assertEqual(row["blocker_bucket"], "true_reject")
            self.assertEqual(
                row["current_target_negative_scope"],
                "hard_negative_for_current_target_only",
            )
            self.assertTrue(row["not_global_negative"])
            self.assertFalse(row["use_as_global_negative"])
            self.assertFalse(row["use_for_future_family_positive_seed"])
            self.assertFalse(row["import_candidate"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertTrue(row["preserve_for_learning"])
            self.assertIn("forbidden", row["prediction_feature_status"])
            self.assertTrue(row["terminal_reason"])

        self.assertEqual(
            rows["m_csa:774"]["counterevidence_reasons"],
            ["glycosidase_not_metal_hydrolase_seed"],
        )
        self.assertEqual(
            rows["m_csa:658"]["target_fingerprint_id"],
            "ser_his_acid_hydrolase",
        )

    def test_representation_baseline_shootout_plan_is_leakage_guarded(self) -> None:
        plan = _load_json(
            ARTIFACTS / "v3_representation_baseline_shootout_plan_20260525.json"
        )
        manifest = _load_json(
            ARTIFACTS
            / "v3_learned_retrieval_manifest_1025_current702_full_20260525.json"
        )

        metadata = plan["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["current_label_registry_count"], 702)
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["ontology_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertFalse(metadata["large_model_training_performed"])
        self.assertFalse(metadata["learned_superiority_claimed"])

        registry = plan["benchmark_spec"]["registry_scope"]
        self.assertEqual(registry["current_label_count"], 702)
        self.assertEqual(registry["entry_scope_counts"], {"external": 3, "m_csa": 699})
        self.assertEqual(registry["learned_manifest_covered_entry_count"], 698)
        self.assertEqual(
            registry["labels_missing_from_learned_manifest_entry_ids"],
            ["m_csa:204", "uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            plan["benchmark_spec"]["role_counts"],
            {
                "high_trust_evaluation_calibration_anchor": 17,
                "negative_ood_calibration": 470,
                "weak_supervision_only": 215,
            },
        )
        self.assertEqual(manifest["metadata"]["labeled_entry_count"], 698)
        self.assertEqual(manifest["metadata"]["eligible_entry_count"], 635)

        contract = plan["prediction_leakage_contract"]
        self.assertIn("mechanism_text", contract["forbidden_for_prediction_fields"])
        self.assertIn("entry_name", contract["forbidden_for_prediction_fields"])
        self.assertIn("ec_labels", contract["forbidden_for_prediction_fields"])

        baselines = {row["baseline_id"]: row for row in plan["baseline_matrix"]}
        geometry = baselines["current_heuristic_geometry"]
        self.assertEqual(
            geometry["status"],
            "computed_on_current_sequence_holdout",
        )
        self.assertEqual(geometry["artifact_label_registry_count"], 702)
        self.assertEqual(
            geometry["heldout_metrics"]["out_of_scope_false_non_abstentions"], 0
        )

        kmer = baselines["deterministic_3mer_jaccard_nearest_neighbor_smoke"]
        self.assertEqual(
            kmer["status"],
            "computed_current_sequence_holdout",
        )
        self.assertEqual(kmer["predictive_inputs"], ["amino_acid_sequence_only"])
        self.assertEqual(kmer["forbidden_inputs_used"], [])
        self.assertEqual(kmer["metrics"]["exact_label_accuracy_all"], 0.5441)
        self.assertEqual(kmer["metrics"]["exact_label_accuracy_in_scope"], 0.1136)
        self.assertEqual(
            kmer["metrics"]["out_of_scope_false_positive_rate_no_threshold"], 0.25
        )

        hybrid = baselines["hybrid_representation_plus_geometry"]
        self.assertEqual(
            hybrid["status"], "blocked_until_current_split_and_embeddings_exist"
        )
        self.assertIn(
            "full_current_702_embedding_artifact_missing", hybrid["blockers"]
        )
        self.assertEqual(
            plan["next_exact_compute_step"]["status"],
            "blocked_by_current_sequence_coverage_gap",
        )
        self.assertEqual(
            plan["next_exact_compute_step"]["missing_sequence_entry_count"], 20
        )
        self.assertIn(
            "build-sequence-distance-holdout-eval",
            plan["next_exact_compute_step"]["rerun_after_sequence_supplement_command"],
        )

        sequence = _load_json(
            ARTIFACTS / "v3_sequence_distance_holdout_eval_1025_current702_20260525.json"
        )
        sequence_meta = sequence["metadata"]
        self.assertEqual(sequence_meta["label_registry_count"], 702)
        self.assertEqual(sequence_meta["evaluated_count"], 698)
        self.assertEqual(sequence_meta["heldout_count"], 140)
        self.assertEqual(sequence_meta["sequence_missing_entry_count"], 20)
        self.assertFalse(sequence_meta["sequence_identity_target_achieved"])

    def test_mcsa_ai_visual_remaining_manual_expert_holds_are_explicit(self) -> None:
        holds = _load_json(
            ARTIFACTS
            / "v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json"
        )

        metadata = holds["metadata"]
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 6)
        self.assertEqual(metadata["manual_visual_hold_count"], 1)
        self.assertEqual(metadata["expert_biochemistry_hold_count"], 5)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["label_import_performed"])
        self.assertFalse(metadata["canonical_registry_import_performed"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["ontology_registry_edited"])
        self.assertFalse(metadata["production_scoring_changed"])
        self.assertEqual(
            metadata["exact_entry_ids"],
            [
                "m_csa:591",
                "m_csa:951",
                "m_csa:986",
                "m_csa:927",
                "m_csa:650",
                "m_csa:886",
            ],
        )

        self.assertEqual(holds["summary"]["import_candidate_entry_ids"], [])
        self.assertEqual(holds["summary"]["countable_label_candidate_entry_ids"], [])
        self.assertEqual(
            holds["summary"]["hold_bucket_counts"],
            {
                "needs_expert_biochemistry_review": 5,
                "needs_manual_visual_review": 1,
            },
        )
        self.assertIn("makes no biochemical", holds["hold_contract"]["decision_rule"])
        self.assertIn("forbidden", holds["hold_contract"]["prediction_leakage_rule"])

        rows = {row["entry_id"]: row for row in holds["rows"]}
        self.assertEqual(rows["m_csa:650"]["blocker_bucket"], "needs_manual_visual_review")
        self.assertEqual(
            rows["m_csa:650"]["target_fingerprint_id"], "ser_his_acid_hydrolase"
        )
        self.assertEqual(
            rows["m_csa:886"]["target_fingerprint_id"], "plp_dependent_enzyme"
        )
        for row in rows.values():
            self.assertFalse(row["import_candidate"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertIn("forbidden", row["prediction_feature_status"])

    def test_mechanism_fingerprint_v1_coherence_audit_freezes_primary_target(self) -> None:
        audit = _load_json(
            ARTIFACTS / "v3_mechanism_fingerprint_v1_coherence_audit_702.json"
        )

        self.assertEqual(
            audit["schema_version"], "mechanism_fingerprint_v1_coherence_audit.v1"
        )
        self.assertEqual(audit["baseline_label_count"], 702)
        self.assertEqual(
            audit["mechanism_fingerprint_version"], "label_factory_v1_8fp"
        )
        self.assertEqual(audit["audit_scope"]["fingerprint_count"], 8)
        self.assertFalse(audit["audit_scope"]["registry_edit_performed"])
        self.assertFalse(audit["audit_scope"]["label_import_performed"])
        self.assertFalse(audit["audit_scope"]["ontology_edit_performed"])
        self.assertFalse(audit["audit_scope"]["production_scoring_change_performed"])

        fingerprints = {row["fingerprint_id"]: row for row in audit["fingerprints"]}
        self.assertEqual(
            set(fingerprints),
            {
                "ser_his_acid_hydrolase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "radical_sam_enzyme",
                "cobalamin_radical_rearrangement",
                "flavin_monooxygenase",
                "flavin_dehydrogenase_reductase",
                "heme_peroxidase_oxidase",
            },
        )
        self.assertEqual(
            audit["fingerprints_kept_for_primary_metric"],
            [
                "ser_his_acid_hydrolase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "flavin_dehydrogenase_reductase",
                "heme_peroxidase_oxidase",
            ],
        )
        self.assertEqual(
            audit["freeze_decision_summary"]["primary_metric_seed_label_count"], 224
        )
        self.assertEqual(
            audit["freeze_decision_summary"]["secondary_only_seed_label_count"], 6
        )
        self.assertEqual(
            fingerprints["metal_dependent_hydrolase"]["evaluation_status"],
            "coarse_but_acceptable_v1",
        )
        self.assertEqual(
            fingerprints["radical_sam_enzyme"]["evaluation_status"],
            "singleton_underpowered",
        )
        self.assertEqual(
            fingerprints["cobalamin_radical_rearrangement"]["v1_freeze_decision"],
            "split_later_do_not_edit_now",
        )
        self.assertIn(
            "Win condition is conjunctive",
            " ".join(audit["downstream_benchmark_rules"]),
        )

        labels_path = ROOT / "data" / "registries" / "curated_mechanism_labels.json"
        labels = _load_json(labels_path)
        self.assertEqual(len(labels), audit["baseline_label_count"])
        self.assertEqual(
            "sha256:" + hashlib.sha256(labels_path.read_bytes()).hexdigest(),
            audit["label_registry_digest"],
        )

    def test_mechanism_prediction_eval_contract_freezes_oos_diversity_policy(self) -> None:
        contract = _load_json(
            ARTIFACTS
            / "v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json"
        )

        self.assertEqual(
            contract["schema_version"],
            "mechanism_prediction_oos_and_diversity_eval_contract.v1",
        )
        self.assertEqual(contract["baseline_label_count"], 702)
        self.assertEqual(
            contract["mechanism_fingerprint_version"], "label_factory_v1_8fp"
        )
        self.assertFalse(
            contract["contract_scope"]["model_training_or_benchmark_results_created"]
        )

        self.assertEqual(
            contract["primary_fingerprints"],
            [
                "ser_his_acid_hydrolase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "flavin_dehydrogenase_reductase",
                "heme_peroxidase_oxidase",
            ],
        )
        secondary = {
            row["fingerprint_id"]: row
            for row in contract["secondary_ood_probe_fingerprints"]
        }
        self.assertEqual(
            set(secondary),
            {
                "radical_sam_enzyme",
                "cobalamin_radical_rearrangement",
                "flavin_monooxygenase",
            },
        )
        self.assertEqual(
            secondary["radical_sam_enzyme"]["probe_role"],
            "far_oos_tail_diagnostic",
        )
        self.assertEqual(
            secondary["cobalamin_radical_rearrangement"]["oos_tier"],
            "boundary_oos",
        )
        self.assertEqual(
            secondary["flavin_monooxygenase"]["primary_metric_status"],
            "excluded_from_primary_supervised_metrics",
        )

        required_sources = [
            "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json",
            "artifacts/v3_representation_baseline_shootout_plan_20260525.json",
            "data/registries/curated_mechanism_labels.json",
            "data/registries/mechanism_fingerprints.json",
        ]
        for source in required_sources:
            self.assertIn(source, contract["source_artifacts"])
            source_path = ROOT / source
            self.assertEqual(
                hashlib.sha256(source_path.read_bytes()).hexdigest(),
                contract["source_artifacts"][source]["sha256"],
            )

        tiering = contract["oos_tiering_policy"]["tier_definitions"]
        self.assertIn("no cofactor overlap", tiering["far_oos"]["deterministic_rule"])
        self.assertIn(
            "shares a cofactor or metal",
            tiering["near_oos"]["deterministic_rule"],
        )
        self.assertEqual(
            tiering["boundary_oos"]["criteria_type"], "curated_list"
        )
        self.assertEqual(tiering["unknown_oos"]["criteria_type"], "fail_closed")

        assignment = contract["frozen_oos_tier_assignments_summary"]
        self.assertFalse(assignment["complete_oos_assignment"])
        self.assertFalse(
            assignment["partial_assignment_status"]["full_470_out_of_scope_assigned"]
        )
        self.assertEqual(
            assignment["partial_representative_assignment_counts"][
                "secondary_probe_seed_rows_assigned_in_this_contract"
            ],
            6,
        )
        self.assertIn(
            "artifacts/v3_mechanism_prediction_oos_tier_assignments_702.json",
            assignment["partial_assignment_status"]["next_exact_task"],
        )

        diversity = contract["diversity_stratified_accuracy_policy"]
        self.assertEqual(
            diversity["default_subfamily_clustering"],
            {
                "applies_where": "amino-acid sequences exist",
                "cluster_source_rule": (
                    "Clusters must be generated from train-only data for any split "
                    "that uses cluster-derived thresholds or bins"
                ),
                "coverage": 0.8,
                "method": "MMseqs",
                "sequence_identity": 0.3,
            },
        )
        self.assertIn("macro-F1 is not sufficient", diversity["headline_rule"])
        self.assertEqual(
            contract["support_threshold_policy"]["quantitative_reporting_thresholds"][
                "accuracy_or_recall_cell_min_n"
            ],
            30,
        )
        self.assertEqual(
            contract["support_threshold_policy"]["quantitative_reporting_thresholds"][
                "ece_or_calibration_cell_min_n"
            ],
            50,
        )

        canaries = contract["canary_examples"]
        self.assertTrue(canaries["canary_expansion_needed"])
        self.assertEqual(len(canaries["examples"]), 42)
        self.assertEqual(
            canaries["primary_canary_count_by_fingerprint"][
                "ser_his_acid_hydrolase"
            ],
            5,
        )
        self.assertEqual(
            contract["active_site_pooling_contract"][
                "primary_benchmark_pooling_mode"
            ],
            "whole_sequence",
        )
        self.assertEqual(
            contract["next_allowed_benchmark_step"]["status"],
            "contract_frozen_stop_before_model_results",
        )

    def test_packet1_wave1_followthrough_addenda_lock_cells(self) -> None:
        lockdown = _load_json(
            ARTIFACTS / "v3_packet1_wave1_lockdown_addendum_702_20260527.json"
        )
        closure = _load_json(
            ARTIFACTS / "v3_packet1_wave1_decision_closure_702_20260527.json"
        )
        hydride_demotion = _load_json(
            ARTIFACTS
            / "v3_v2_sublabel_audit_702_flavin_hydride_transfer_demotion_20260527.json"
        )
        card_addendum = _load_json(
            ARTIFACTS
            / "v3_wave1_representation_shootout_result_card_702_20260527_addendum.json"
        )
        metric_impact = _load_json(
            ARTIFACTS / "v3_m_csa497_wave1_metric_impact_702_20260527.json"
        )

        self.assertTrue(lockdown["review_only"])
        self.assertFalse(lockdown["guardrails"]["label_registry_changed_by_this_artifact"])
        cells = lockdown["locked_packet1_eval_cells"]
        self.assertEqual(
            cells["tm_pair_verified_fold_conflict_oos_anchors"]["rows"],
            ["m_csa:217", "m_csa:477"],
        )
        self.assertEqual(
            cells["partial_fold_conflict_with_caveat"]["rows"], ["m_csa:428"]
        )
        self.assertIn(
            "incidental-primary-hit",
            cells["partial_fold_conflict_with_caveat"]["eval_use"],
        )
        self.assertEqual(
            cells["near_orphan_oos_router_abstention_diagnostic"]["rows"],
            ["m_csa:440"],
        )
        self.assertEqual(
            cells["excluded_after_oos_relabel"]["current_label_state"], "out_of_scope"
        )
        self.assertIn(
            "primary flavin_dehydrogenase_reductase support and metrics",
            cells["excluded_after_oos_relabel"]["exclude_from"],
        )
        closure_rows = {
            row["entry_id"]: row["closure_state"]
            for row in closure["row_closures"]
        }
        self.assertEqual(closure_rows["m_csa:217"], "verified_anchor")
        self.assertEqual(closure_rows["m_csa:477"], "verified_anchor")
        self.assertEqual(closure_rows["m_csa:428"], "caveated_partial")
        self.assertEqual(closure_rows["m_csa:440"], "near_orphan_oos")
        self.assertEqual(
            closure_rows["m_csa:497"],
            "excluded_from_primary_flavin_metrics",
        )

        demotion = hydride_demotion["field_demotion"]
        self.assertEqual(
            demotion["sublabel"],
            "flavin.dehydrogenase_oxidase_hydride_transfer",
        )
        self.assertEqual(
            demotion["new_state"]["list"],
            "readiness_summary.expert_review_needed_candidates",
        )
        self.assertFalse(hydride_demotion["guardrails"]["production_scoring_changed"])

        self.assertEqual(metric_impact["entry_id"], "m_csa:497")
        for track in metric_impact["tracks"]:
            self.assertEqual(track["primary_support_before"], 45)
            self.assertEqual(track["primary_support_after"], 44)
        self.assertIn(
            "low_structure_neighborhood_near_orphan",
            card_addendum["stale_fields_in_result_card"]["per_bin_metrics"][0][
                "field_path_pattern"
            ],
        )
        self.assertEqual(
            card_addendum["source_artifacts"][
                "artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json"
            ]["sha256"],
            hashlib.sha256(
                (ARTIFACTS / "v3_m_csa497_wave1_metric_impact_702_20260527.json").read_bytes()
            ).hexdigest(),
        )

    def test_wave1_tm_pair_signal_expansion_is_exactly_blocked(self) -> None:
        blocker = _load_json(
            ARTIFACTS
            / "v3_wave1_tm_pair_signal_expansion_blocker_702_20260527.json"
        )

        self.assertEqual(
            blocker["status"],
            "blocked_runtime_unbounded_foldseek_attempt_running_without_result",
        )
        self.assertTrue(blocker["guardrails"]["review_only"])
        self.assertFalse(blocker["guardrails"]["canonical_label_registry_changed"])
        self.assertEqual(
            blocker["readiness_stage"]["available_staged_coordinate_count"],
            692,
        )
        self.assertEqual(
            blocker["existing_signal_before_this_attempt"]["max_reported_pair_rows"],
            200,
        )
        self.assertEqual(
            blocker["attempted_expansion"]["target_reported_pair_rows"],
            5000,
        )
        self.assertFalse(
            blocker["attempted_expansion"]["observed_result_files"][
                "repo_output_artifact_exists"
            ]
        )
        self.assertIn(
            "--max-runtime-seconds 1800",
            blocker["minimal_next_commands"][0]["command"],
        )
        claim_status = blocker["packet1_fold_neighborhood_claim_status"]
        self.assertEqual(
            claim_status["m_csa:217"]["full_fold_neighborhood_support"],
            "still_capped_by_prior_200_row_retention",
        )
        self.assertEqual(
            claim_status["m_csa:428"]["current_decision"],
            "caveated_partial_anchor",
        )

    def test_m_csa750_packet_and_mismatch_audit_are_fail_closed(self) -> None:
        packet = _load_json(
            ARTIFACTS / "v3_m_csa750_review_packet_702_20260527.json"
        )
        revision = _load_json(
            ARTIFACTS / "v3_m_csa750_label_revision_702_20260527.json"
        )
        metric_impact = _load_json(
            ARTIFACTS / "v3_m_csa750_wave1_metric_canary_impact_702_20260527.json"
        )
        audit = _load_json(
            ARTIFACTS
            / "v3_label_factory_review_import_mechanism_mismatch_audit_702_20260527.json"
        )
        close_read = _load_json(
            ARTIFACTS
            / "v3_label_factory_review_import_mechanism_mismatch_close_read_702_20260527.json"
        )
        labels = _load_json(ROOT / "data" / "registries" / "curated_mechanism_labels.json")
        label_by_entry = {row["entry_id"]: row for row in labels}

        self.assertEqual(packet["status"], "review_blocked_no_canonical_relabel")
        self.assertFalse(packet["guardrails"]["canonical_label_changed"])
        self.assertEqual(
            packet["review_decision"]["mechanism_class"],
            "flavin_radical_fe_s_dehydratase",
        )
        self.assertFalse(
            packet["review_decision"]["ordinary_flavin_dehydrogenase_reductase_fit"]
        )
        self.assertIn("future_radical_flavin_fe_s_dehydratase", packet["review_decision"]["likely_resolution"])
        self.assertTrue(
            packet["wave1_eval_effect"][
                "unsafe_for_top_foldseek_success_learned_failure_canary"
            ]
        )
        evidence_text = json.dumps(packet["decisive_mechanism_evidence"])
        self.assertIn("semiquinone", evidence_text)
        self.assertIn("Fe-S", evidence_text)
        self.assertEqual(revision["decision"], "relabel_out_of_scope")
        self.assertEqual(
            revision["revised_label_state"]["label_type"],
            "out_of_scope",
        )
        self.assertTrue(
            revision["evaluation_policy_effect"]["pull_from_wave1_primary_flavin_metrics"]
        )
        self.assertEqual(label_by_entry["m_csa:750"]["label_type"], "out_of_scope")
        self.assertIsNone(label_by_entry["m_csa:750"]["fingerprint_id"])
        self.assertEqual(label_by_entry["m_csa:750"]["review_status"], "expert_reviewed")
        self.assertIn(
            "label_factory_review_import",
            label_by_entry["m_csa:750"]["evidence"]["sources"],
        )
        self.assertTrue(metric_impact["canary_impact"]["removed_from_canary_use"])
        self.assertEqual(
            metric_impact["canary_impact"]["canary_set_status"],
            "underpowered_after_m_csa750_removal",
        )

        self.assertTrue(audit["review_only"])
        self.assertEqual(
            audit["population"]["label_factory_review_import_bronze_row_count"], 210
        )
        self.assertEqual(audit["guardrails"]["automatic_relabels"], 0)
        self.assertFalse(audit["guardrails"]["manual_reviewed_all_rows"])
        rule_ids = {row["rule_id"] for row in audit["rules"]}
        self.assertEqual(
            rule_ids,
            {
                "flavin_metal_radical_conflict",
                "ser_his_cys_nucleophile_conflict",
                "heme_nonheme_or_mixed_metal_oxidase_signal",
                "plp_cobalamin_radical_coupling_conflict",
            },
        )
        rows = {row["entry_id"]: row for row in audit["shortlist_rows"]}
        self.assertIn("m_csa:750", rows)
        self.assertEqual(rows["m_csa:750"]["heuristic_priority"], "high")
        self.assertEqual(
            audit["shortlist_summary"]["already_resolved_prior_revision_entry_ids"],
            ["m_csa:497"],
        )
        close_read_rows = {row["entry_id"]: row for row in close_read["rows"]}
        self.assertEqual(close_read_rows["m_csa:750"]["disposition"], "relabel_out_of_scope")
        self.assertEqual(close_read_rows["m_csa:506"]["disposition"], "keep_current_label")
        self.assertEqual(
            close_read_rows["m_csa:714"]["disposition"],
            "move_to_secondary_or_future_family_blocker",
        )
        self.assertFalse(close_read["guardrails"]["ontology_registry_changed"])
        self.assertEqual(close_read["summary"]["relabel_out_of_scope_count"], 1)

    def test_fmo_acquisition_and_m_csa43_canary_checks_are_review_only(self) -> None:
        fmo = _load_json(
            ARTIFACTS / "v3_flavin_monooxygenase_acquisition_packet_702_20260527.json"
        )
        fmo_closure = _load_json(
            ARTIFACTS / "v3_flavin_monooxygenase_acquisition_closure_702_20260527.json"
        )
        canary = _load_json(
            ARTIFACTS / "v3_m_csa43_wave1_canary_mechanism_check_702_20260527.json"
        )
        canary_closure = _load_json(
            ARTIFACTS / "v3_m_csa43_wave1_canary_closure_702_20260527.json"
        )

        self.assertTrue(fmo["review_only"])
        self.assertFalse(fmo["guardrails"]["primary_promotion_reconsidered_now"])
        self.assertEqual(
            fmo["current_state"]["m_csa_131_role"],
            "secondary_ood_probe::flavin_monooxygenase",
        )
        self.assertEqual(fmo["current_state"]["current_support_count"], 2)
        self.assertEqual(
            fmo["current_state"]["target_additional_clean_rows_before_reconsideration"],
            4,
        )
        self.assertEqual(
            fmo["current_state"]["goal_total_support_before_primary_promotion_reconsideration"],
            6,
        )
        self.assertEqual(
            set(fmo["decision_vocabulary"]),
            {"clean_FMO_candidate", "not_FMO", "insufficient_evidence", "overlaps_flavin_reductase"},
        )
        local_decisions = {
            row["entry_id"]: row["decision"] for row in fmo["local_m_csa_review_candidates"]
        }
        self.assertEqual(local_decisions["m_csa:551"], "clean_FMO_candidate")
        self.assertEqual(local_decisions["m_csa:973"], "clean_FMO_candidate")
        self.assertEqual(local_decisions["m_csa:128"], "not_FMO")
        self.assertEqual(
            fmo_closure["current_counts"][
                "clean_acquisition_count_if_candidates_are_counted_for_readiness"
            ],
            4,
        )
        self.assertEqual(
            fmo_closure["current_counts"]["missing_clean_count_to_n6_after_this_closure"],
            2,
        )
        self.assertFalse(
            fmo_closure["primary_promotion_decision"]["promote_fmo_primary_now"]
        )
        target_decisions = {
            row["target_family"]: row["decision"]
            for row in fmo_closure["named_target_family_search"]
        }
        self.assertEqual(
            target_decisions["cyclohexanone_monooxygenase_or_BVMO"],
            "missing_local_clean_row",
        )

        self.assertTrue(canary["review_only"])
        self.assertFalse(canary["guardrails"]["label_registry_changed"])
        self.assertEqual(canary["entry"]["current_fingerprint_id"], "metal_dependent_hydrolase")
        self.assertTrue(canary["canary_decision"]["remains_valid_wave1_canary"])
        self.assertFalse(canary["canary_decision"]["label_review_needed"])
        self.assertTrue(
            canary_closure["canary_decision"][
                "m_csa43_remains_valid_wave1_top_foldseek_success_learned_failure_canary"
            ]
        )
        self.assertEqual(
            canary_closure["canary_set_after_m_csa750"]["status"],
            "underpowered_singleton_canary_set",
        )


if __name__ == "__main__":
    unittest.main()
