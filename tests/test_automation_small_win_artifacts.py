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


if __name__ == "__main__":
    unittest.main()
