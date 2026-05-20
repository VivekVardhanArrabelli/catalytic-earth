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
        self.assertEqual(metadata["lane_json_file_count"], 54)
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
            "fresh_folded_role_identity_stress_abstained_fail_closed",
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
            "policy_frozen_review_only_and_fresh_stress_abstains",
        )
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


if __name__ == "__main__":
    unittest.main()
