from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Scaling1025ArtifactTests(unittest.TestCase):
    def test_1025_preview_is_clean_but_not_promotable(self) -> None:
        gate = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_1025_preview.json")
        acceptance = _load_json(
            ROOT / "artifacts" / "v3_label_batch_acceptance_check_1025_preview.json"
        )
        scaling_quality = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_1025_preview.json"
        )
        review_debt = _load_json(
            ROOT / "artifacts" / "v3_review_debt_summary_1025_preview.json"
        )
        deferral = _load_json(
            ROOT
            / "artifacts"
            / "v3_accepted_review_debt_deferral_audit_1025_preview.json"
        )

        self.assertTrue(gate["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(gate["blockers"], [])
        self.assertFalse(acceptance["metadata"]["accepted_for_counting"])
        self.assertEqual(
            acceptance["metadata"]["artifact_lineage"]["method"],
            "label_batch_acceptance_cli_lineage_validation",
        )
        self.assertEqual(
            acceptance["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_label_batch_acceptance",
        )
        self.assertEqual(acceptance["metadata"]["artifact_lineage"]["slice_id"], 1025)
        self.assertEqual(acceptance["metadata"]["accepted_new_label_count"], 0)
        self.assertEqual(acceptance["metadata"]["countable_label_count"], 679)
        self.assertEqual(acceptance["metadata"]["pending_review_count"], 329)
        self.assertEqual(acceptance["metadata"]["hard_negative_count"], 0)
        self.assertEqual(acceptance["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            acceptance["metadata"]["out_of_scope_false_non_abstentions"], 0
        )
        self.assertEqual(
            acceptance["metadata"]["actionable_in_scope_failure_count"], 0
        )
        self.assertEqual(acceptance["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance["blockers"], ["accepted_labels_added"])
        self.assertEqual(
            scaling_quality["metadata"]["audit_recommendation"], "do_not_promote"
        )
        self.assertEqual(
            scaling_quality["metadata"]["artifact_lineage"]["method"],
            "label_scaling_quality_cli_lineage_validation",
        )
        self.assertEqual(
            scaling_quality["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_label_scaling_quality",
        )
        self.assertEqual(
            scaling_quality["metadata"]["artifact_lineage"]["slice_id"], 1025
        )
        self.assertEqual(scaling_quality["blockers"], [])
        self.assertEqual(review_debt["metadata"]["new_review_debt_count"], 3)
        self.assertEqual(
            review_debt["metadata"]["new_review_debt_entry_ids"],
            ["m_csa:1003", "m_csa:1004", "m_csa:1005"],
        )
        self.assertEqual(deferral["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(deferral["metadata"]["accepted_review_debt_overlap_count"], 0)

    def test_source_limit_and_transfer_manifests_block_m_csa_only_scaling(self) -> None:
        source_limit = _load_json(
            ROOT / "artifacts" / "v3_source_scale_limit_audit_1025.json"
        )
        transfer = _load_json(
            ROOT / "artifacts" / "v3_external_source_transfer_manifest_1025.json"
        )
        queries = _load_json(
            ROOT / "artifacts" / "v3_external_source_query_manifest_1025.json"
        )
        ood_plan = _load_json(
            ROOT / "artifacts" / "v3_external_ood_calibration_plan_1025.json"
        )
        sample = _load_json(
            ROOT / "artifacts" / "v3_external_source_candidate_sample_1025.json"
        )
        sample_audit = _load_json(
            ROOT / "artifacts" / "v3_external_source_candidate_sample_audit_1025.json"
        )
        candidate_manifest = _load_json(
            ROOT / "artifacts" / "v3_external_source_candidate_manifest_1025.json"
        )
        candidate_manifest_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_candidate_manifest_audit_1025.json"
        )
        evidence_plan = _load_json(
            ROOT / "artifacts" / "v3_external_source_evidence_plan_1025.json"
        )
        evidence_export = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_evidence_request_export_1025.json"
        )
        active_site_queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_evidence_queue_1025.json"
        )
        active_site_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_evidence_sample_1025.json"
        )
        active_site_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_evidence_sample_audit_1025.json"
        )
        heuristic_control_queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_heuristic_control_queue_1025.json"
        )
        heuristic_control_queue_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_heuristic_control_queue_audit_1025.json"
        )
        structure_mapping_plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_structure_mapping_plan_1025.json"
        )
        structure_mapping_plan_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_structure_mapping_plan_audit_1025.json"
        )
        structure_mapping_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_structure_mapping_sample_1025.json"
        )
        structure_mapping_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_structure_mapping_sample_audit_1025.json"
        )
        heuristic_control_scores = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_heuristic_control_scores_1025.json"
        )
        heuristic_control_scores_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_heuristic_control_scores_audit_1025.json"
        )
        self.assertTrue(heuristic_control_scores_audit["metadata"]["guardrail_clean"])
        for result in heuristic_control_scores["results"]:
            for hit in result["top_fingerprints"]:
                self.assertFalse(hit["text_or_label_fields_used_for_score"])
        failure_mode_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_failure_mode_audit_1025.json"
        )
        control_repair_plan = _load_json(
            ROOT / "artifacts" / "v3_external_source_control_repair_plan_1025.json"
        )
        control_repair_plan_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_control_repair_plan_audit_1025.json"
        )
        representation_control = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_control_manifest_1025.json"
        )
        representation_control_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_control_manifest_audit_1025.json"
        )
        representation_comparison = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_control_comparison_1025.json"
        )
        representation_comparison_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_control_comparison_audit_1025.json"
        )
        representation_backend = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_plan_1025.json"
        )
        representation_backend_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_plan_audit_1025.json"
        )
        representation_backend_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_sample_1025.json"
        )
        representation_backend_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_sample_audit_1025.json"
        )
        broad_ec_disambiguation = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_broad_ec_disambiguation_audit_1025.json"
        )
        active_site_gap_sources = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_gap_source_requests_1025.json"
        )
        binding_context_repair = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_binding_context_repair_plan_1025.json"
        )
        binding_context_repair_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_binding_context_repair_plan_audit_1025.json"
        )
        binding_context_mapping = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_binding_context_mapping_sample_1025.json"
        )
        binding_context_mapping_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_binding_context_mapping_sample_audit_1025.json"
        )
        sequence_holdout_audit = _load_json(
            ROOT / "artifacts" / "v3_external_source_sequence_holdout_audit_1025.json"
        )
        sequence_neighborhood = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_neighborhood_plan_1025.json"
        )
        sequence_neighborhood_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_neighborhood_sample_1025.json"
        )
        sequence_neighborhood_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_neighborhood_sample_audit_1025.json"
        )
        sequence_alignment = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_alignment_verification_1025.json"
        )
        sequence_alignment_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_alignment_verification_audit_1025.json"
        )
        sequence_reference_screen_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_reference_screen_audit_1025.json"
        )
        sequence_search_export = _load_json(
            ROOT / "artifacts" / "v3_external_source_sequence_search_export_1025.json"
        )
        sequence_search_export_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_sequence_search_export_audit_1025.json"
        )
        backend_sequence_search = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_backend_sequence_search_1025.json"
        )
        backend_sequence_search_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_backend_sequence_search_audit_1025.json"
        )
        import_readiness = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_import_readiness_audit_1025.json"
        )
        active_site_sourcing = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_queue_1025.json"
        )
        active_site_sourcing_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_queue_audit_1025.json"
        )
        active_site_sourcing_export = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_export_1025.json"
        )
        active_site_sourcing_export_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_export_audit_1025.json"
        )
        active_site_sourcing_resolution = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_resolution_1025.json"
        )
        active_site_sourcing_resolution_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_active_site_sourcing_resolution_audit_1025.json"
        )
        transfer_blocker_matrix = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_transfer_blocker_matrix_1025.json"
        )
        transfer_blocker_matrix_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_transfer_blocker_matrix_audit_1025.json"
        )
        pilot_priority = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_candidate_priority_1025.json"
        )
        pilot_review_export = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_review_decision_export_1025.json"
        )
        pilot_evidence_packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_evidence_packet_1025.json"
        )
        pilot_representation_plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_plan_1025.json"
        )
        pilot_representation_plan_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_plan_audit_1025.json"
        )
        pilot_representation_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_sample_1025.json"
        )
        pilot_representation_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_sample_audit_1025.json"
        )
        pilot_evidence_dossiers = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_evidence_dossiers_1025.json"
        )
        pilot_active_site_decisions = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_active_site_evidence_decisions_1025.json"
        )
        pilot_representation_adjudication = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_adjudication_1025.json"
        )
        pilot_success_criteria = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_success_criteria_1025.json"
        )
        external_import_safety = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_review_only_import_safety_audit_1025.json"
        )
        external_transfer_gate = _load_json(
            ROOT / "artifacts" / "v3_external_source_transfer_gate_check_1025.json"
        )
        reaction_evidence = _load_json(
            ROOT / "artifacts" / "v3_external_source_reaction_evidence_sample_1025.json"
        )
        reaction_evidence_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_reaction_evidence_sample_audit_1025.json"
        )
        lane_balance = _load_json(
            ROOT / "artifacts" / "v3_external_source_lane_balance_audit_1025.json"
        )

        self.assertTrue(source_limit["metadata"]["source_limit_reached"])
        self.assertEqual(source_limit["metadata"]["observed_source_entries"], 1003)
        self.assertEqual(source_limit["metadata"]["source_entry_gap"], 22)
        self.assertEqual(source_limit["metadata"]["countable_label_count"], 679)
        self.assertEqual(
            source_limit["metadata"]["recommendation"],
            "stop_m_csa_only_tranche_growth_and_scope_external_source_transfer",
        )
        self.assertFalse(transfer["metadata"]["ready_for_label_import"])
        self.assertEqual(transfer["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            transfer["metadata"]["manifest_recommendation"],
            "prototype_external_source_transfer_before_next_count_growth",
        )
        self.assertFalse(queries["metadata"]["ready_for_label_import"])
        self.assertEqual(queries["metadata"]["countable_label_candidate_count"], 0)
        self.assertGreaterEqual(queries["metadata"]["lane_count"], 5)
        self.assertFalse(ood_plan["metadata"]["ready_for_label_import"])
        self.assertEqual(ood_plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            ood_plan["metadata"]["lane_count"], queries["metadata"]["lane_count"]
        )
        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["fetch_failure_count"], 0)
        self.assertGreater(sample["metadata"]["candidate_count"], 0)
        self.assertTrue(sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(sample_audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample_audit["blockers"], [])
        self.assertFalse(candidate_manifest["metadata"]["ready_for_label_import"])
        self.assertTrue(candidate_manifest["metadata"]["ready_for_external_review"])
        self.assertEqual(
            candidate_manifest["metadata"]["candidate_count"],
            sample["metadata"]["candidate_count"],
        )
        self.assertEqual(
            candidate_manifest["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertTrue(candidate_manifest["metadata"]["heuristic_control_required"])
        self.assertEqual(candidate_manifest["metadata"]["missing_ood_lane_count"], 0)
        self.assertEqual(candidate_manifest["metadata"]["duplicate_accession_count"], 0)
        self.assertEqual(candidate_manifest["metadata"]["structure_supported_count"], 30)
        self.assertEqual(candidate_manifest["metadata"]["exact_reference_overlap_count"], 2)
        exact_overlap_rows = {
            row["accession"]: row["external_source_controls"][
                "sequence_similarity_control"
            ]["matched_m_csa_entry_ids"]
            for row in candidate_manifest["rows"]
            if row["external_source_controls"]["sequence_similarity_control"][
                "exact_reference_overlap"
            ]
        }
        self.assertEqual(
            exact_overlap_rows,
            {"O15527": ["m_csa:185"], "P42126": ["m_csa:341"]},
        )
        self.assertEqual(
            candidate_manifest["metadata"]["sequence_failure_set_overlap_count"], 0
        )
        self.assertTrue(candidate_manifest_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            candidate_manifest_audit["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(
            candidate_manifest_audit["metadata"]["import_ready_row_count"], 0
        )
        self.assertEqual(candidate_manifest_audit["blockers"], [])
        self.assertFalse(evidence_plan["metadata"]["ready_for_label_import"])
        self.assertTrue(evidence_plan["metadata"]["ready_for_evidence_collection"])
        self.assertEqual(evidence_plan["metadata"]["candidate_count"], 30)
        self.assertEqual(
            evidence_plan["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            evidence_plan["metadata"]["active_site_evidence_required_count"], 30
        )
        self.assertEqual(
            evidence_plan["metadata"]["exact_reference_overlap_holdout_count"], 2
        )
        self.assertEqual(
            evidence_plan["metadata"]["broad_or_incomplete_ec_candidate_count"], 7
        )
        self.assertEqual(
            evidence_plan["metadata"]["broad_or_incomplete_ec_only_candidate_count"],
            3,
        )
        self.assertEqual(
            evidence_plan["metadata"]["broad_or_incomplete_ec_numbers"],
            [
                "1.1.1.-",
                "1.11.1.-",
                "1.8.-.-",
                "2.1.1.-",
                "2.7.1.-",
                "3.2.2.-",
                "4.2.99.-",
            ],
        )
        self.assertEqual(
            evidence_plan["metadata"]["next_action_counts"][
                "collect_active_site_and_mechanism_evidence"
            ],
            25,
        )
        self.assertEqual(
            evidence_plan["metadata"]["next_action_counts"][
                "resolve_broad_or_incomplete_ec_before_active_site_mapping"
            ],
            3,
        )
        self.assertEqual(
            evidence_plan["metadata"]["next_action_counts"][
                "route_exact_reference_overlap_to_holdout_control"
            ],
            2,
        )
        self.assertEqual(
            evidence_plan["metadata"]["required_evidence_counts"][
                "specific_reaction_disambiguation_for_broad_ec"
            ],
            7,
        )
        self.assertTrue(evidence_export["metadata"]["external_source_review_only"])
        self.assertFalse(evidence_export["metadata"]["ready_for_label_import"])
        self.assertEqual(evidence_export["metadata"]["exported_count"], 30)
        self.assertEqual(
            evidence_export["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            evidence_export["metadata"]["decision_counts"], {"no_decision": 30}
        )
        self.assertFalse(active_site_queue["metadata"]["ready_for_label_import"])
        self.assertEqual(
            active_site_queue["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(active_site_queue["metadata"]["candidate_count"], 30)
        self.assertEqual(active_site_queue["metadata"]["ready_candidate_count"], 25)
        self.assertEqual(active_site_queue["metadata"]["deferred_candidate_count"], 5)
        self.assertEqual(
            active_site_queue["metadata"]["queue_status_counts"],
            {
                "defer_broad_ec_disambiguation": 3,
                "defer_exact_reference_overlap_holdout": 2,
                "ready_for_active_site_evidence": 25,
            },
        )
        self.assertTrue(
            all(
                row["countable_label_candidate"] is False
                for row in active_site_queue["rows"]
            )
        )
        self.assertFalse(active_site_sample["metadata"]["ready_for_label_import"])
        self.assertEqual(
            active_site_sample["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(active_site_sample["metadata"]["candidate_count"], 25)
        self.assertEqual(
            active_site_sample["metadata"][
                "candidate_with_active_site_feature_count"
            ],
            15,
        )
        self.assertEqual(
            active_site_sample["metadata"]["candidate_with_catalytic_activity_count"],
            25,
        )
        self.assertEqual(active_site_sample["metadata"]["fetch_failure_count"], 0)
        self.assertTrue(
            all(
                row["countable_label_candidate"] is False
                and row["ready_for_label_import"] is False
                for row in active_site_sample["candidate_summaries"]
            )
        )
        self.assertTrue(active_site_sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            active_site_sample_audit["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(
            active_site_sample_audit["metadata"]["active_site_feature_gap_count"],
            10,
        )
        self.assertFalse(
            heuristic_control_queue["metadata"]["ready_for_label_import"]
        )
        self.assertTrue(
            heuristic_control_queue["metadata"][
                "ready_for_heuristic_control_execution"
            ]
        )
        self.assertEqual(
            heuristic_control_queue["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(heuristic_control_queue["metadata"]["candidate_count"], 25)
        self.assertEqual(
            heuristic_control_queue["metadata"]["ready_candidate_count"], 12
        )
        self.assertEqual(
            heuristic_control_queue["metadata"]["deferred_candidate_count"], 13
        )
        self.assertEqual(
            heuristic_control_queue["metadata"]["queue_status_counts"],
            {
                "defer_active_site_feature_gap": 10,
                "defer_broad_ec_disambiguation": 3,
                "ready_for_heuristic_control_prototype": 12,
            },
        )
        self.assertTrue(heuristic_control_queue_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            heuristic_control_queue_audit["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertFalse(structure_mapping_plan["metadata"]["ready_for_label_import"])
        self.assertTrue(
            structure_mapping_plan["metadata"]["ready_for_structure_mapping"]
        )
        self.assertEqual(
            structure_mapping_plan["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(structure_mapping_plan["metadata"]["candidate_count"], 25)
        self.assertEqual(
            structure_mapping_plan["metadata"]["ready_mapping_candidate_count"], 12
        )
        self.assertEqual(
            structure_mapping_plan["metadata"]["deferred_mapping_candidate_count"], 13
        )
        self.assertTrue(structure_mapping_plan_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            structure_mapping_plan_audit["metadata"][
                "ready_rows_missing_position_count"
            ],
            0,
        )
        self.assertFalse(
            structure_mapping_sample["metadata"]["ready_for_label_import"]
        )
        self.assertTrue(
            structure_mapping_sample["metadata"][
                "ready_for_heuristic_control_scoring"
            ]
        )
        self.assertEqual(
            structure_mapping_sample["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(structure_mapping_sample["metadata"]["candidate_count"], 12)
        self.assertEqual(
            structure_mapping_sample["metadata"]["mapped_candidate_count"], 12
        )
        self.assertEqual(
            structure_mapping_sample["metadata"]["fetch_failure_count"], 0
        )
        self.assertTrue(structure_mapping_sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            structure_mapping_sample_audit["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertFalse(
            heuristic_control_scores["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            heuristic_control_scores["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(heuristic_control_scores["metadata"]["candidate_count"], 12)
        self.assertEqual(
            heuristic_control_scores["metadata"]["top1_fingerprint_counts"],
            {
                "flavin_dehydrogenase_reductase": 1,
                "heme_peroxidase_oxidase": 2,
                "metal_dependent_hydrolase": 9,
            },
        )
        self.assertTrue(heuristic_control_scores_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            heuristic_control_scores_audit["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            heuristic_control_scores_audit["control_findings"],
            [
                "heuristic_control_top1_fingerprint_collapse",
                "heuristic_control_metal_hydrolase_collapse",
                "heuristic_control_scope_top1_mismatch",
            ],
        )
        self.assertEqual(
            heuristic_control_scores_audit["metadata"]["dominant_top1_fingerprint"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(
            heuristic_control_scores_audit["metadata"]["dominant_top1_fraction"],
            0.75,
        )
        self.assertEqual(
            heuristic_control_scores_audit["metadata"]["scope_top1_mismatch_count"],
            9,
        )
        self.assertFalse(failure_mode_audit["metadata"]["ready_for_label_import"])
        self.assertEqual(
            failure_mode_audit["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(failure_mode_audit["metadata"]["failure_mode_count"], 5)
        self.assertEqual(
            [row["failure_mode"] for row in failure_mode_audit["rows"]],
            [
                "external_active_site_feature_gap",
                "external_broad_ec_disambiguation_needed",
                "heuristic_control_top1_fingerprint_collapse",
                "heuristic_control_metal_hydrolase_collapse",
                "heuristic_control_scope_top1_mismatch",
            ],
        )
        self.assertFalse(control_repair_plan["metadata"]["ready_for_label_import"])
        self.assertEqual(
            control_repair_plan["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(control_repair_plan["metadata"]["repair_row_count"], 25)
        self.assertEqual(
            control_repair_plan["metadata"]["active_site_gap_repair_count"], 10
        )
        self.assertEqual(
            control_repair_plan["metadata"]["broad_ec_disambiguation_repair_count"], 3
        )
        self.assertEqual(
            control_repair_plan["metadata"]["heuristic_control_repair_count"], 12
        )
        self.assertEqual(
            control_repair_plan["metadata"]["scope_top1_mismatch_repair_count"], 9
        )
        self.assertTrue(
            control_repair_plan["metadata"][
                "repair_plan_complete_for_observed_failures"
            ]
        )
        self.assertEqual(control_repair_plan["metadata"]["uncovered_failure_modes"], [])
        self.assertTrue(control_repair_plan_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            control_repair_plan_audit["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertFalse(representation_control["metadata"]["ready_for_label_import"])
        self.assertEqual(
            representation_control["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(representation_control["metadata"]["candidate_count"], 12)
        self.assertEqual(
            representation_control["metadata"]["eligible_control_count"], 12
        )
        self.assertEqual(
            representation_control["metadata"]["scope_top1_mismatch_count"], 9
        )
        self.assertTrue(representation_control_audit["metadata"]["guardrail_clean"])
        self.assertFalse(representation_comparison["metadata"]["ready_for_label_import"])
        self.assertEqual(
            representation_comparison["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(representation_comparison["metadata"]["candidate_count"], 12)
        self.assertEqual(
            representation_comparison["metadata"]["scope_top1_mismatch_count"], 9
        )
        self.assertEqual(
            representation_comparison["metadata"][
                "metal_hydrolase_collapse_flag_count"
            ],
            7,
        )
        self.assertEqual(
            representation_comparison["metadata"]["boundary_case_count"], 2
        )
        self.assertTrue(representation_comparison_audit["metadata"]["guardrail_clean"])
        self.assertFalse(representation_backend["metadata"]["ready_for_label_import"])
        self.assertEqual(
            representation_backend["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(representation_backend["metadata"]["candidate_count"], 12)
        self.assertEqual(
            representation_backend["metadata"]["embedding_status"],
            "backend_plan_only_not_computed",
        )
        self.assertEqual(
            representation_backend["metadata"]["heuristic_contrast_required_count"], 9
        )
        self.assertEqual(
            representation_backend["metadata"]["sequence_search_blocked_count"], 0
        )
        self.assertTrue(representation_backend_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            representation_backend_audit["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertTrue(broad_ec_disambiguation["metadata"]["guardrail_clean"])
        self.assertFalse(
            broad_ec_disambiguation["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            broad_ec_disambiguation["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(broad_ec_disambiguation["metadata"]["candidate_count"], 3)
        self.assertEqual(
            broad_ec_disambiguation["metadata"][
                "specific_context_available_count"
            ],
            3,
        )
        self.assertEqual(
            broad_ec_disambiguation["metadata"]["multiple_specific_context_count"],
            2,
        )
        self.assertFalse(active_site_gap_sources["metadata"]["ready_for_label_import"])
        self.assertEqual(
            active_site_gap_sources["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(active_site_gap_sources["metadata"]["candidate_count"], 10)
        self.assertEqual(
            active_site_gap_sources["metadata"][
                "mapped_binding_context_request_count"
            ],
            7,
        )
        self.assertEqual(
            active_site_gap_sources["metadata"][
                "binding_context_missing_request_count"
            ],
            3,
        )
        self.assertFalse(binding_context_repair["metadata"]["ready_for_label_import"])
        self.assertEqual(
            binding_context_repair["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(binding_context_repair["metadata"]["candidate_count"], 10)
        self.assertEqual(
            binding_context_repair["metadata"][
                "ready_binding_context_candidate_count"
            ],
            7,
        )
        self.assertEqual(
            binding_context_repair["metadata"][
                "deferred_binding_context_candidate_count"
            ],
            3,
        )
        self.assertEqual(binding_context_repair["metadata"]["binding_position_count"], 70)
        self.assertTrue(binding_context_repair_audit["metadata"]["guardrail_clean"])
        self.assertFalse(binding_context_mapping["metadata"]["ready_for_label_import"])
        self.assertEqual(
            binding_context_mapping["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(binding_context_mapping["metadata"]["candidate_count"], 7)
        self.assertEqual(binding_context_mapping["metadata"]["mapped_candidate_count"], 7)
        self.assertTrue(binding_context_mapping_audit["metadata"]["guardrail_clean"])
        self.assertTrue(sequence_holdout_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            sequence_holdout_audit["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            sequence_holdout_audit["metadata"][
                "exact_reference_overlap_holdout_count"
            ],
            2,
        )
        self.assertEqual(
            sequence_holdout_audit["metadata"][
                "near_duplicate_search_candidate_count"
            ],
            28,
        )
        self.assertFalse(sequence_neighborhood["metadata"]["ready_for_label_import"])
        self.assertEqual(
            sequence_neighborhood["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(sequence_neighborhood["metadata"]["candidate_count"], 30)
        self.assertEqual(
            sequence_neighborhood["metadata"][
                "exact_reference_overlap_holdout_count"
            ],
            2,
        )
        self.assertEqual(
            sequence_neighborhood["metadata"]["near_duplicate_search_request_count"],
            28,
        )
        self.assertFalse(
            sequence_neighborhood_sample["metadata"]["ready_for_label_import"]
        )
        self.assertTrue(
            sequence_neighborhood_sample["metadata"][
                "complete_near_duplicate_search_required"
            ]
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"]["candidate_count"], 30
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"]["external_sequence_fetched_count"],
            30,
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"]["reference_entry_count"], 679
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"]["reference_sequence_count"], 735
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "reference_sequence_record_count"
            ],
            737,
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "expected_reference_accession_count"
            ],
            735,
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "missing_reference_sequence_count"
            ],
            0,
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "missing_reference_sequence_accessions"
            ],
            [],
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "inactive_reference_accession_resolutions"
            ],
            {
                "P03176": ["P0DTH5", "Q9QNF7"],
                "Q05489": ["P0DUB8", "P0DUB9"],
            },
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"]["top_hit_row_count"], 90
        )
        self.assertEqual(
            sequence_neighborhood_sample["metadata"][
                "high_similarity_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            sequence_neighborhood_sample_audit["metadata"]["guardrail_clean"]
        )
        self.assertFalse(sequence_alignment["metadata"]["ready_for_label_import"])
        self.assertTrue(
            sequence_alignment["metadata"][
                "complete_near_duplicate_search_required"
            ]
        )
        self.assertEqual(
            sequence_alignment["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(sequence_alignment["metadata"]["candidate_count"], 30)
        self.assertEqual(sequence_alignment["metadata"]["verified_pair_count"], 90)
        self.assertEqual(
            sequence_alignment["metadata"]["alignment_alert_candidate_count"], 2
        )
        self.assertEqual(
            sequence_alignment["metadata"]["verification_status_counts"],
            {
                "alignment_near_duplicate_candidate_holdout": 2,
                "alignment_no_near_duplicate_signal": 88,
            },
        )
        self.assertTrue(sequence_alignment_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            sequence_alignment_audit["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            sequence_reference_screen_audit["metadata"]["guardrail_clean"]
        )
        self.assertEqual(
            sequence_reference_screen_audit["metadata"]["blocker_target"],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertEqual(
            sequence_reference_screen_audit["metadata"]["blocker_removed"],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertTrue(
            sequence_reference_screen_audit["metadata"][
                "current_reference_screen_complete"
            ]
        )
        self.assertEqual(
            sequence_reference_screen_audit["metadata"][
                "missing_reference_sequence_accessions"
            ],
            [],
        )
        self.assertEqual(sequence_reference_screen_audit["blockers"], [])
        self.assertEqual(
            sequence_reference_screen_audit["metadata"]["screen_status_counts"],
            {
                "current_reference_top_hits_aligned_no_alert": 28,
                "preexisting_sequence_holdout_retained": 2,
            },
        )
        self.assertFalse(sequence_search_export["metadata"]["ready_for_label_import"])
        self.assertTrue(
            sequence_search_export["metadata"][
                "complete_near_duplicate_search_required"
            ]
        )
        self.assertEqual(
            sequence_search_export["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(sequence_search_export["metadata"]["candidate_count"], 30)
        self.assertEqual(
            sequence_search_export["metadata"]["decision_status_counts"],
            {"no_decision": 30},
        )
        self.assertEqual(
            sequence_search_export["metadata"]["near_duplicate_search_request_count"],
            28,
        )
        self.assertEqual(
            sequence_search_export["metadata"][
                "current_reference_screen_complete_candidate_count"
            ],
            28,
        )
        self.assertEqual(
            sequence_search_export["metadata"]["blocker_removed"],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertEqual(
            sequence_search_export["metadata"][
                "source_sequence_reference_screen_audit_method"
            ],
            "external_source_sequence_reference_screen_audit",
        )
        self.assertNotIn(
            "complete_near_duplicate_reference_search_not_completed",
            sequence_search_export["rows"][0]["blockers"],
        )
        self.assertNotIn(
            "complete_near_duplicate_reference_search_not_completed",
            sequence_search_export["blockers"],
        )
        self.assertIn(
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
            sequence_search_export["rows"][0]["blockers"],
        )
        self.assertEqual(
            sequence_search_export["metadata"]["blocker_counts"][
                "complete_uniref_or_all_vs_all_near_duplicate_search_required"
            ],
            28,
        )
        self.assertEqual(
            sequence_search_export["rows"][0]["current_reference_screen"]["status"],
            "current_reference_top_hits_aligned_no_alert",
        )
        self.assertEqual(
            sequence_search_export["metadata"]["sequence_holdout_task_count"], 2
        )
        self.assertTrue(sequence_search_export_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            sequence_search_export_audit["metadata"]["completed_decision_count"], 0
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["method"],
            "external_source_backend_sequence_search",
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["backend_name"],
            "mmseqs2_easy_search",
        )
        self.assertTrue(backend_sequence_search["metadata"]["backend_succeeded"])
        self.assertEqual(
            backend_sequence_search["metadata"]["blocker_removed"],
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
        )
        self.assertEqual(backend_sequence_search["metadata"]["candidate_count"], 30)
        self.assertEqual(
            backend_sequence_search["metadata"]["external_sequence_count"], 30
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["current_reference_accession_count"],
            735,
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["current_reference_sequence_count"],
            737,
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["exact_reference_row_count"], 2
        )
        self.assertEqual(
            backend_sequence_search["metadata"]["near_duplicate_row_count"], 0
        )
        self.assertEqual(backend_sequence_search["metadata"]["no_signal_row_count"], 28)
        self.assertEqual(backend_sequence_search["metadata"]["failure_row_count"], 0)
        self.assertEqual(
            sorted(row["accession"] for row in backend_sequence_search["exact_reference_rows"]),
            ["O15527", "P42126"],
        )
        self.assertTrue(
            all(
                not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                for row in backend_sequence_search["rows"]
            )
        )
        self.assertTrue(backend_sequence_search_audit["metadata"]["guardrail_clean"])
        self.assertTrue(backend_sequence_search_audit["metadata"]["real_backend"])
        self.assertTrue(import_readiness["metadata"]["guardrail_clean"])
        self.assertFalse(import_readiness["metadata"]["ready_for_label_import"])
        self.assertEqual(
            import_readiness["metadata"]["artifact_lineage"]["method"],
            "external_transfer_artifact_path_lineage_validation",
        )
        self.assertEqual(
            import_readiness["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_external_import_readiness",
        )
        self.assertEqual(
            import_readiness["metadata"]["artifact_lineage"]["slice_id"],
            1025,
        )
        self.assertTrue(
            import_readiness["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertEqual(
            import_readiness["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(import_readiness["metadata"]["label_import_ready_count"], 0)
        self.assertEqual(import_readiness["metadata"]["candidate_count"], 30)
        self.assertEqual(import_readiness["metadata"]["active_site_gap_count"], 10)
        self.assertEqual(
            import_readiness["metadata"]["sequence_holdout_or_search_count"], 2
        )
        self.assertEqual(import_readiness["metadata"]["backend_sequence_no_signal_count"], 28)
        self.assertNotIn(
            "complete_near_duplicate_search_required",
            import_readiness["metadata"]["blocker_counts"],
        )
        self.assertEqual(
            import_readiness["metadata"]["sequence_alignment_alert_count"], 2
        )
        self.assertEqual(
            import_readiness["metadata"]["sequence_alignment_incomplete_count"], 0
        )
        self.assertEqual(
            import_readiness["metadata"]["heuristic_scope_mismatch_count"], 9
        )
        self.assertEqual(
            import_readiness["metadata"]["representation_control_issue_count"], 29
        )
        self.assertFalse(active_site_sourcing["metadata"]["ready_for_label_import"])
        self.assertEqual(
            active_site_sourcing["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(active_site_sourcing["metadata"]["candidate_count"], 10)
        self.assertEqual(
            active_site_sourcing["metadata"]["ready_sourcing_candidate_count"], 7
        )
        self.assertEqual(
            active_site_sourcing["metadata"]["text_source_candidate_count"], 3
        )
        self.assertEqual(
            active_site_sourcing["metadata"]["sequence_holdout_deferred_count"], 0
        )
        self.assertTrue(active_site_sourcing_audit["metadata"]["guardrail_clean"])
        self.assertFalse(
            active_site_sourcing_export["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            active_site_sourcing_export["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            active_site_sourcing_export["metadata"]["candidate_count"], 10
        )
        self.assertEqual(
            active_site_sourcing_export["metadata"]["decision_status_counts"],
            {"no_decision": 10},
        )
        self.assertEqual(
            active_site_sourcing_export["metadata"]["source_task_counts"],
            {
                "curate_active_site_positions_from_mapped_binding_context": 7,
                "find_primary_active_site_or_residue_role_source": 3,
            },
        )
        self.assertEqual(
            active_site_sourcing_export["metadata"]["source_target_count"], 72
        )
        self.assertTrue(
            active_site_sourcing_export_audit["metadata"]["guardrail_clean"]
        )
        self.assertEqual(
            active_site_sourcing_export_audit["metadata"]["completed_decision_count"],
            0,
        )
        self.assertFalse(transfer_blocker_matrix["metadata"]["ready_for_label_import"])
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["artifact_lineage"]["method"],
            "external_transfer_artifact_path_lineage_validation",
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_external_blocker_matrix",
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["artifact_lineage"]["slice_id"],
            1025,
        )
        self.assertTrue(
            transfer_blocker_matrix["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertEqual(transfer_blocker_matrix["metadata"]["candidate_count"], 30)
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "active_site_sourcing_export_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "active_site_sourcing_resolution_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["sequence_search_export_candidate_count"],
            30,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "backend_sequence_search_candidate_count"
            ],
            30,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "backend_sequence_search_no_signal_count"
            ],
            28,
        )
        self.assertNotIn(
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
            transfer_blocker_matrix["metadata"]["blocker_counts"],
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "representation_backend_plan_candidate_count"
            ],
            12,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "representation_backend_sample_candidate_count"
            ],
            12,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["prioritized_action_counts"],
            {
                "compute_or_attach_real_representation_control": 6,
                "curate_primary_literature_or_pdb_active_site_sources": 7,
                "find_primary_active_site_or_residue_role_source": 3,
                "keep_representation_near_duplicate_out_of_import_batch": 3,
                "keep_sequence_holdout_out_of_import_batch": 2,
                "select_and_run_real_representation_backend": 9,
            },
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["blocker_counts"][
                "explicit_active_site_residue_sources_absent"
            ],
            10,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["blocker_counts"][
                "representation_near_duplicate_control_holdout"
            ],
            3,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"][
                "dominant_prioritized_action_fraction"
            ],
            0.3,
        )
        self.assertEqual(
            transfer_blocker_matrix["metadata"]["dominant_lane_fraction"], 0.1667
        )
        self.assertTrue(transfer_blocker_matrix_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "completed_active_site_decision_count"
            ],
            0,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "completed_sequence_decision_count"
            ],
            0,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "missing_review_only_status_row_count"
            ],
            0,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "dominant_prioritized_action_fraction"
            ],
            0.3,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"]["dominant_lane_fraction"], 0.1667
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "active_site_resolution_row_count"
            ],
            10,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "representation_sample_row_count"
            ],
            12,
        )
        self.assertEqual(
            transfer_blocker_matrix_audit["metadata"][
                "representation_near_duplicate_alert_count"
            ],
            3,
        )
        self.assertEqual(
            pilot_priority["metadata"]["method"],
            "external_source_pilot_candidate_priority",
        )
        self.assertEqual(
            pilot_priority["metadata"]["blocker_removed"],
            "external_pilot_candidate_ranking",
        )
        self.assertFalse(
            pilot_priority["metadata"]["leakage_policy"][
                "text_or_label_fields_used_for_priority"
            ]
        )
        self.assertIn(
            "representation_near_duplicate_alert",
            pilot_priority["metadata"]["predictive_feature_sources"],
        )
        self.assertFalse(pilot_priority["metadata"]["ready_for_label_import"])
        self.assertEqual(
            pilot_priority["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(pilot_priority["metadata"]["candidate_count"], 30)
        self.assertEqual(pilot_priority["metadata"]["selected_candidate_count"], 10)
        self.assertEqual(pilot_priority["metadata"]["eligible_candidate_count"], 25)
        self.assertEqual(
            pilot_priority["metadata"]["holdout_or_near_duplicate_deferred_count"],
            5,
        )
        self.assertEqual(
            pilot_priority["metadata"]["selected_accessions"],
            [
                "O14756",
                "P06746",
                "C9JRZ8",
                "P55263",
                "P34949",
                "Q9BXD5",
                "Q6NSJ0",
                "O60568",
                "O95050",
                "P51580",
            ],
        )
        self.assertTrue(
            all(row["eligible_for_review_pilot"] for row in pilot_priority["rows"])
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in pilot_priority["rows"])
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in pilot_priority["rows"])
        )
        self.assertTrue(
            all(not row["pilot_priority_blockers"] for row in pilot_priority["rows"])
        )
        self.assertTrue(
            all(
                not row["leakage_provenance"][
                    "text_or_label_fields_used_for_priority"
                ]
                for row in pilot_priority["rows"]
            )
        )
        self.assertNotIn(
            "exact_sequence_holdout",
            {
                blocker
                for row in pilot_priority["rows"]
                for blocker in row["blockers"]
            },
        )
        self.assertNotIn(
            "complete_near_duplicate_search_required",
            {
                blocker
                for row in pilot_priority["rows"]
                for blocker in row["blockers"]
            },
        )
        self.assertNotIn(
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
            {
                blocker
                for row in pilot_priority["rows"]
                for blocker in row["blockers"]
            },
        )
        self.assertLessEqual(
            max(pilot_priority["metadata"]["selected_lane_counts"].values()),
            2,
        )
        self.assertEqual(
            pilot_review_export["metadata"]["method"],
            "external_source_pilot_review_decision_export",
        )
        self.assertEqual(
            pilot_review_export["metadata"]["blocker_removed"],
            "external_pilot_review_decision_export_scaffold",
        )
        self.assertFalse(pilot_review_export["metadata"]["ready_for_label_import"])
        self.assertEqual(
            pilot_review_export["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(pilot_review_export["metadata"]["candidate_count"], 10)
        self.assertEqual(pilot_review_export["metadata"]["completed_decision_count"], 0)
        self.assertEqual(
            pilot_review_export["metadata"]["decision_status_counts"],
            {"no_decision": 10},
        )
        self.assertEqual(
            [row["accession"] for row in pilot_review_export["review_items"]],
            pilot_priority["metadata"]["selected_accessions"],
        )
        self.assertTrue(
            all(
                row["decision"]["decision_status"] == "no_decision"
                for row in pilot_review_export["review_items"]
            )
        )
        self.assertTrue(
            all(
                not row["decision"]["ready_for_label_import"]
                for row in pilot_review_export["review_items"]
            )
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["method"],
            "external_source_pilot_evidence_packet",
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["blocker_removed"],
            "external_pilot_source_packet_consolidation",
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["artifact_lineage"]["method"],
            "external_transfer_artifact_path_lineage_validation",
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_external_pilot_packet",
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["artifact_lineage"]["slice_id"],
            1025,
        )
        self.assertTrue(
            pilot_evidence_packet["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertTrue(pilot_evidence_packet["metadata"]["guardrail_clean"])
        self.assertEqual(pilot_evidence_packet["metadata"]["candidate_count"], 10)
        self.assertEqual(
            pilot_evidence_packet["metadata"]["selected_accessions"],
            pilot_priority["metadata"]["selected_accessions"],
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["sequence_search_packet_count"], 10
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"][
                "backend_sequence_search_packet_count"
            ],
            10,
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"][
                "backend_sequence_search_no_signal_count"
            ],
            10,
        )
        self.assertGreaterEqual(
            pilot_evidence_packet["metadata"]["active_site_sourcing_packet_count"], 1
        )
        self.assertGreater(
            pilot_evidence_packet["metadata"]["source_target_count"], 0
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"]["missing_sequence_export_accessions"],
            [],
        )
        self.assertEqual(
            pilot_evidence_packet["metadata"][
                "missing_required_active_site_export_accessions"
            ],
            [],
        )
        self.assertFalse(pilot_evidence_packet["metadata"]["ready_for_label_import"])
        self.assertEqual(
            pilot_evidence_packet["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertTrue(
            all(
                row["review_status"] == "external_pilot_evidence_packet_review_only"
                and not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                and row["source_targets"]
                and row["sequence_search"]["backend_search_status"]
                == "no_near_duplicate_signal"
                for row in pilot_evidence_packet["rows"]
            )
        )
        self.assertEqual(
            pilot_representation_plan["metadata"]["blocker_removed"],
            "external_pilot_representation_sample_coverage",
        )
        self.assertEqual(pilot_representation_plan["metadata"]["candidate_count"], 10)
        self.assertEqual(
            pilot_representation_plan["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertTrue(pilot_representation_plan_audit["metadata"]["guardrail_clean"])
        self.assertEqual(pilot_representation_sample["metadata"]["candidate_count"], 10)
        self.assertTrue(
            pilot_representation_sample["metadata"]["embedding_backend_available"]
        )
        self.assertEqual(
            pilot_representation_sample["metadata"]["embedding_vector_dimension"],
            320,
        )
        self.assertEqual(
            pilot_representation_sample["metadata"][
                "representation_near_duplicate_alert_count"
            ],
            1,
        )
        self.assertEqual(
            pilot_representation_sample["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertFalse(
            pilot_representation_sample["metadata"]["ready_for_label_import"]
        )
        self.assertTrue(pilot_representation_sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["blocker_removed"],
            "external_pilot_per_candidate_evidence_dossier_assembly",
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["artifact_lineage"]["method"],
            "external_transfer_artifact_path_lineage_validation",
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["artifact_lineage"]["blocker_removed"],
            "artifact_graph_consistency_for_external_pilot_dossiers",
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["artifact_lineage"]["slice_id"],
            1025,
        )
        self.assertTrue(
            pilot_evidence_dossiers["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertEqual(pilot_evidence_dossiers["metadata"]["candidate_count"], 10)
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertFalse(
            pilot_evidence_dossiers["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"]["candidate_with_remaining_blocker_count"],
            10,
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"][
                "pilot_explicit_active_site_evidence_missing_count"
            ],
            3,
        )
        self.assertEqual(
            pilot_evidence_dossiers["metadata"][
                "pilot_specific_reaction_context_missing_count"
            ],
            0,
        )
        self.assertTrue(
            all(
                row["review_status"]
                == "external_pilot_evidence_dossier_review_only"
                and not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                and row["reaction_evidence"]["reaction_record_count"] > 0
                and row["sequence_evidence"]["backend_search_status"]
                == "no_near_duplicate_signal"
                for row in pilot_evidence_dossiers["rows"]
            )
        )
        self.assertFalse(
            any(
                blocker
                in {
                    "complete_near_duplicate_search_required",
                    "complete_uniref_or_all_vs_all_near_duplicate_search_required",
                }
                for row in pilot_evidence_dossiers["rows"]
                for blocker in row["remaining_blockers"]
            )
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"]["method"],
            "external_source_pilot_active_site_evidence_decisions",
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"]["blocker_removed"],
            "external_pilot_active_site_source_status_ambiguity",
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"]["artifact_lineage"][
                "blocker_removed"
            ],
            "external_pilot_active_site_source_status_ambiguity",
        )
        self.assertFalse(
            pilot_active_site_decisions["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(pilot_active_site_decisions["metadata"]["candidate_count"], 10)
        self.assertEqual(
            pilot_active_site_decisions["metadata"]["decision_status_counts"],
            {
                "binding_context_only": 3,
                "explicit_active_site_source_present": 7,
            },
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"][
                "broader_duplicate_screening_required_count"
            ],
            10,
        )
        self.assertEqual(
            pilot_active_site_decisions["metadata"]["import_ready_row_count"], 0
        )
        self.assertTrue(
            all(
                row["review_status"]
                == "external_pilot_active_site_evidence_decision_review_only"
                and not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                and row["broader_duplicate_screening_status"]
                == "broader_duplicate_screening_required"
                and row["import_readiness_blockers"]
                for row in pilot_active_site_decisions["rows"]
            )
        )
        self.assertEqual(
            {
                row["active_site_evidence_decision_status"]
                for row in pilot_active_site_decisions["rows"]
                if row["active_site_evidence_source_category"] == "binding_context_only"
            },
            {"binding_context_only"},
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"]["method"],
            "external_source_pilot_representation_adjudication",
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"][
                "representation_control_adjudication_status_counts"
            ],
            {
                "representation_control_adjudicated_review_only": 3,
                "representation_near_duplicate_holdout": 4,
                "representation_stability_changed_requires_review": 3,
            },
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"][
                "representation_control_unresolved_count"
            ],
            3,
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"][
                "representation_control_concrete_evidence_count"
            ],
            10,
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"][
                "comparison_blocker_not_removed"
            ],
            "requested_650m_or_larger_representation_backend_not_computed",
        )
        self.assertEqual(
            pilot_representation_adjudication["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertFalse(
            pilot_representation_adjudication["metadata"]["ready_for_label_import"]
        )
        self.assertTrue(
            all(
                row["review_status"]
                == "external_pilot_representation_adjudication_review_only"
                and not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                for row in pilot_representation_adjudication["rows"]
            )
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["method"],
            "external_source_pilot_success_criteria",
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["blocker_removed"],
            "external_pilot_success_criteria_defined",
        )
        self.assertFalse(pilot_success_criteria["metadata"]["operational_success"])
        self.assertFalse(
            pilot_success_criteria["metadata"]["scientific_import_success"]
        )
        self.assertTrue(pilot_success_criteria["metadata"]["needs_more_work"])
        self.assertEqual(
            pilot_success_criteria["metadata"]["pilot_status"], "needs_more_work"
        )
        self.assertEqual(pilot_success_criteria["metadata"]["candidate_count"], 10)
        self.assertEqual(
            pilot_success_criteria["metadata"]["terminal_decision_count"], 0
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["import_ready_row_count"], 0
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            pilot_success_criteria["metadata"][
                "explicit_active_site_source_resolution_counts"
            ],
            {
                "explicit_active_site_source_resolved": 7,
                "unresolved_binding_context_only": 3,
            },
        )
        self.assertEqual(
            pilot_success_criteria["metadata"][
                "broader_duplicate_screening_status_counts"
            ],
            {"broader_duplicate_screening_required": 10},
        )
        self.assertEqual(
            pilot_success_criteria["metadata"][
                "representation_control_adjudication_counts"
            ],
            {
                "representation_control_adjudicated_review_only": 3,
                "representation_near_duplicate_holdout": 4,
                "representation_stability_changed_requires_review": 3,
            },
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["review_decision_status_counts"],
            {"no_decision": 10},
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["full_label_factory_gate_status_counts"],
            {"not_run": 10},
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["failure_explanation_status_counts"],
            {"missing_process": 10},
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["criteria_blocker_counts"][
                "review_decision_not_terminal"
            ],
            10,
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["criteria_blocker_counts"][
                "representation_control_unresolved"
            ],
            3,
        )
        self.assertEqual(
            pilot_success_criteria["metadata"]["artifact_lineage"]["slice_id"], 1025
        )
        self.assertTrue(
            all(
                row["review_status"] == "external_pilot_success_criteria_review_only"
                and not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                for row in pilot_success_criteria["rows"]
            )
        )
        self.assertTrue(external_import_safety["metadata"]["countable_import_safe"])
        self.assertEqual(
            external_import_safety["metadata"]["total_new_countable_label_count"], 0
        )
        self.assertEqual(
            external_import_safety["rows"][0]["review_only_flags"][
                "external_source_review_only"
            ],
            True,
        )
        self.assertEqual(external_transfer_gate["blockers"], [])
        self.assertEqual(external_transfer_gate["metadata"]["gate_count"], 68)
        self.assertEqual(external_transfer_gate["metadata"]["passed_gate_count"], 68)
        self.assertEqual(
            external_transfer_gate["metadata"]["gate_input_contract"],
            "ExternalSourceTransferGateInputs.v1",
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_transfer_candidate_lineage_consistent"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_pilot_candidate_priority_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_pilot_review_decision_export_no_decision"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"]["external_pilot_evidence_packet_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_pilot_evidence_dossiers_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_pilot_active_site_evidence_decisions_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_pilot_representation_sample_review_only"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["external_pilot_selected_candidate_count"],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_pilot_representation_sample_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_pilot_review_completed_decision_count"
            ],
            0,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_pilot_active_site_decision_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_pilot_active_site_decision_no_explicit_source_count"
            ],
            3,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_pilot_evidence_packet_source_target_count"
            ],
            79,
        )
        self.assertTrue(
            external_transfer_gate["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertTrue(
            external_transfer_gate["metadata"]["artifact_lineage"][
                "artifact_path_lineage"
            ]["guardrail_clean"]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["artifact_lineage"][
                "artifact_path_lineage"
            ]["slice_id"],
            1025,
        )
        self.assertIn(
            "pilot_candidate_priority",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "pilot_review_decision_export",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "pilot_evidence_packet",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "pilot_evidence_dossiers",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "pilot_active_site_evidence_decisions",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "pilot_representation_backend_sample",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "sequence_holdout_audit",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertIn(
            "sequence_backend_search",
            external_transfer_gate["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        self.assertFalse(external_transfer_gate["metadata"]["ready_for_label_import"])
        self.assertTrue(
            external_transfer_gate["metadata"][
                "ready_for_external_evidence_collection"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["active_site_ready_candidate_count"],
            25,
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["active_site_deferred_candidate_count"],
            5,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["active_site_evidence_queue_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"]["active_site_evidence_sample_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_evidence_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_evidence_sampled_candidate_count"
            ],
            25,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_feature_supported_candidate_count"
            ],
            15,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["heuristic_control_queue_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "heuristic_control_queue_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "heuristic_control_ready_candidate_count"
            ],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["structure_mapping_plan_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "structure_mapping_plan_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "structure_mapping_ready_candidate_count"
            ],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["structure_mapping_sample_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "structure_mapping_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "structure_mapping_sample_mapped_candidate_count"
            ],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["heuristic_control_scores_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "heuristic_control_scores_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "heuristic_control_scored_candidate_count"
            ],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["external_failure_mode_audit_review_only"]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["external_failure_mode_count"], 5
        )
        self.assertTrue(
            external_transfer_gate["gates"]["external_control_repair_plan_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_control_repair_plan_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["external_control_repair_row_count"],
            25,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_control_manifest_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_control_manifest_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["representation_control_eligible_count"],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_control_comparison_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_control_comparison_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "representation_control_comparison_metal_collapse_count"
            ],
            7,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["representation_backend_plan_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_backend_plan_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "representation_backend_plan_candidate_count"
            ],
            12,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "representation_backend_plan_contrast_required_count"
            ],
            9,
        )
        self.assertFalse(representation_backend_sample["metadata"]["ready_for_label_import"])
        self.assertEqual(
            representation_backend_sample["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            representation_backend_sample["metadata"]["candidate_count"], 12
        )
        self.assertEqual(
            representation_backend_sample["metadata"]["embedding_status"],
            "computed_review_only",
        )
        self.assertEqual(
            representation_backend_sample["metadata"][
                "representation_near_duplicate_alert_count"
            ],
            3,
        )
        self.assertTrue(representation_backend_sample_audit["metadata"]["guardrail_clean"])
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_backend_sample_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "representation_backend_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "representation_backend_sample_candidate_count"
            ],
            12,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "representation_backend_sample_near_duplicate_alert_count"
            ],
            3,
        )

        self.assertTrue(
            external_transfer_gate["gates"][
                "broad_ec_disambiguation_audit_review_only"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "broad_ec_specific_context_available_count"
            ],
            3,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_gap_source_requests_review_only"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["active_site_gap_source_request_count"],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_gap_mapped_binding_context_request_count"
            ],
            7,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["sequence_neighborhood_plan_review_only"]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_neighborhood_near_duplicate_search_request_count"
            ],
            28,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["sequence_neighborhood_sample_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "sequence_neighborhood_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_neighborhood_sample_candidate_count"
            ],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_neighborhood_reference_sequence_count"
            ],
            735,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "sequence_alignment_verification_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "sequence_alignment_verification_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_alignment_verified_pair_count"
            ],
            90,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_alignment_alert_candidate_count"
            ],
            2,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_alignment_deferred_pair_count"
            ],
            0,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "sequence_reference_screen_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_reference_screen_candidate_count"
            ],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_reference_screened_reference_sequence_count"
            ],
            735,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_reference_screen_blocker_removed"
            ],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertTrue(
            external_transfer_gate["gates"]["sequence_search_export_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "sequence_search_export_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["sequence_search_export_candidate_count"],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_search_export_near_duplicate_request_count"
            ],
            28,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["sequence_backend_search_review_only"]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_backend_search_candidate_count"
            ],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_backend_search_no_signal_count"
            ],
            28,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_backend_search_exact_reference_count"
            ],
            2,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_backend_search_backend_name"
            ],
            "mmseqs2_easy_search",
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_import_readiness_audit_blocks_label_import"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_import_readiness_candidate_count"
            ],
            30,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["active_site_sourcing_queue_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_sourcing_queue_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_queue_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_ready_candidate_count"
            ],
            7,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_text_source_candidate_count"
            ],
            3,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["active_site_sourcing_export_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_sourcing_export_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_export_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_export_source_target_count"
            ],
            72,
        )
        self.assertFalse(
            active_site_sourcing_resolution["metadata"]["ready_for_label_import"]
        )
        self.assertEqual(
            active_site_sourcing_resolution["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            active_site_sourcing_resolution["metadata"]["candidate_count"], 10
        )
        self.assertEqual(
            active_site_sourcing_resolution["metadata"][
                "explicit_active_site_source_count"
            ],
            0,
        )
        self.assertEqual(
            active_site_sourcing_resolution["metadata"][
                "binding_context_only_count"
            ],
            7,
        )
        self.assertEqual(
            active_site_sourcing_resolution["metadata"][
                "primary_source_required_count"
            ],
            3,
        )
        self.assertTrue(
            active_site_sourcing_resolution_audit["metadata"]["guardrail_clean"]
        )
        self.assertEqual(
            active_site_sourcing_resolution_audit["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_sourcing_resolution_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "active_site_sourcing_resolution_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_resolution_candidate_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "active_site_sourcing_resolution_explicit_source_count"
            ],
            0,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_transfer_blocker_matrix_review_only"
            ]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_transfer_blocker_matrix_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_candidate_count"
            ],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_active_site_count"
            ],
            10,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_transfer_blocker_matrix_active_site_resolution_integrated"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_active_site_resolution_count"
            ],
            10,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_sequence_count"
            ],
            30,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_representation_count"
            ],
            12,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_transfer_blocker_matrix_representation_sample_integrated"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_representation_sample_count"
            ],
            12,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "external_transfer_blocker_matrix_completed_decision_count"
            ],
            0,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["binding_context_repair_plan_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "binding_context_repair_plan_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["binding_context_ready_candidate_count"],
            7,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["binding_context_mapping_sample_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "binding_context_mapping_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "binding_context_mapping_mapped_candidate_count"
            ],
            7,
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "external_sequence_holdout_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["sequence_holdout_exact_overlap_count"],
            2,
        )
        self.assertEqual(
            external_transfer_gate["metadata"][
                "sequence_holdout_near_duplicate_search_count"
            ],
            28,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["reaction_evidence_sample_review_only"]
        )
        self.assertTrue(
            external_transfer_gate["gates"][
                "reaction_evidence_sample_audit_guardrail_clean"
            ]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["reaction_evidence_candidate_count"], 30
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["reaction_evidence_record_count"], 64
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["reaction_broad_ec_context_row_count"],
            16,
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(external_transfer_gate["metadata"]["external_lane_count"], 6)
        self.assertEqual(
            external_transfer_gate["metadata"]["external_dominant_lane_fraction"],
            0.1667,
        )
        self.assertFalse(reaction_evidence["metadata"]["ready_for_label_import"])
        self.assertEqual(
            reaction_evidence["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(reaction_evidence["metadata"]["candidate_count"], 30)
        self.assertEqual(
            reaction_evidence["metadata"]["candidate_with_reaction_context_count"], 29
        )
        self.assertEqual(
            reaction_evidence["metadata"]["broad_or_incomplete_ec_count"], 7
        )
        self.assertEqual(
            reaction_evidence["metadata"]["broad_or_incomplete_ec_numbers"],
            [
                "1.1.1.-",
                "1.11.1.-",
                "1.8.-.-",
                "2.1.1.-",
                "2.7.1.-",
                "3.2.2.-",
                "4.2.99.-",
            ],
        )
        self.assertEqual(reaction_evidence["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(reaction_evidence["metadata"]["reaction_record_count"], 64)
        self.assertTrue(
            all(
                row["evidence_status"] == "reaction_context_only"
                and row["countable_label_candidate"] is False
                for row in reaction_evidence["rows"]
            )
        )
        self.assertTrue(reaction_evidence_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            reaction_evidence_audit["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(
            reaction_evidence_audit["metadata"]["broad_ec_context_row_count"], 16
        )
        self.assertEqual(reaction_evidence_audit["blockers"], [])
        self.assertTrue(lane_balance["metadata"]["guardrail_clean"])
        self.assertEqual(lane_balance["metadata"]["lane_count"], 6)
        self.assertEqual(lane_balance["metadata"]["dominant_lane_fraction"], 0.1667)
        self.assertEqual(lane_balance["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(lane_balance["blockers"], [])

    def test_learned_representation_backend_sample_is_computed_and_review_only(self) -> None:
        sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_sample_1025.json"
        )
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_sample_audit_1025.json"
        )

        self.assertEqual(sample["metadata"]["embedding_backend"], "esm2_t6_8m_ur50d")
        self.assertTrue(sample["metadata"]["embedding_backend_available"])
        self.assertEqual(sample["metadata"]["embedding_vector_dimension"], 320)
        self.assertEqual(sample["metadata"]["candidate_count"], 12)
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            sample["metadata"]["representation_near_duplicate_alert_count"], 3
        )
        self.assertEqual(
            sample["metadata"]["learned_vs_heuristic_disagreement_count"], 12
        )
        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertTrue(
            all(row["countable_label_candidate"] is False for row in sample["rows"])
        )

    def test_650m_representation_backend_sidecars_use_largest_feasible_esm2(
        self,
    ) -> None:
        sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_1025.json"
        )
        sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_audit_1025.json"
        )
        pilot_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json"
        )
        pilot_sample_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_audit_1025.json"
        )
        stability = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json"
        )
        pilot_stability = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json"
        )

        for artifact in (sample, pilot_sample):
            metadata = artifact["metadata"]
            self.assertEqual(metadata["embedding_backend"], "esm2_t30_150m_ur50d")
            self.assertEqual(
                metadata["requested_embedding_backend"], "esm2_t33_650m_ur50d"
            )
            self.assertEqual(
                metadata["computed_embedding_backend"], "esm2_t30_150m_ur50d"
            )
            self.assertEqual(
                metadata["model_name"], "facebook/esm2_t30_150M_UR50D"
            )
            self.assertEqual(
                metadata["requested_model_name"], "facebook/esm2_t33_650M_UR50D"
            )
            self.assertTrue(metadata["local_files_only"])
            self.assertTrue(metadata["embedding_backend_available"])
            self.assertFalse(metadata["requested_embedding_backend_available"])
            self.assertEqual(metadata["embedding_vector_dimension"], 640)
            self.assertEqual(metadata["expected_embedding_vector_dimension"], 640)
            self.assertEqual(
                metadata["requested_expected_embedding_vector_dimension"], 1280
            )
            self.assertEqual(metadata["embedding_failure_count"], 0)
            self.assertEqual(
                metadata["requested_embedding_failure_count"],
                metadata["requested_accession_count"],
            )
            self.assertEqual(metadata["model_load_status"], "loaded")
            self.assertEqual(
                metadata["requested_model_load_status"],
                "not_attempted_cache_missing",
            )
            self.assertEqual(
                metadata["requested_model_load_failure_type"],
                "ModelWeightsNotCached",
            )
            self.assertIsInstance(metadata["requested_model_load_failure"], str)
            self.assertEqual(
                metadata["backend_feasibility_status"],
                "fallback_computed_requested_model_unavailable_locally",
            )
            self.assertEqual(
                metadata["attempted_embedding_backend"], "esm2_t33_650m_ur50d"
            )
            self.assertEqual(
                metadata["requested_backend_feasibility_status"],
                "model_unavailable_locally",
            )
            self.assertEqual(
                metadata["requested_backend_local_cache_status"], "not_cached"
            )
            self.assertFalse(metadata["requested_backend_weights_cached"])
            self.assertEqual(
                metadata["requested_backend_smoke_status"],
                "not_attempted_weights_not_cached",
            )
            self.assertEqual(
                metadata["largest_supported_embedding_backend"],
                "esm2_t33_650m_ur50d",
            )
            self.assertEqual(
                metadata["largest_feasible_embedding_backend"], "esm2_t30_150m_ur50d"
            )
            self.assertIsNone(metadata["fallback_not_computed_reason"])
            self.assertTrue(metadata["fallback_used"])
            self.assertEqual(
                metadata["fallback_selected_backend"], "esm2_t30_150m_ur50d"
            )
            self.assertEqual(
                metadata["fallback_reason"],
                "requested_backend_uncached_local_files_only",
            )
            self.assertGreaterEqual(len(metadata["fallback_attempts"]), 1)
            self.assertEqual(
                metadata["blocker_not_removed"],
                "requested_650m_or_larger_representation_backend_not_computed",
            )
            self.assertIsInstance(metadata["embedding_elapsed_seconds"], float)
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            self.assertFalse(metadata["ready_for_label_import"])
            self.assertEqual(len(artifact["rows"]), metadata["candidate_count"])
            self.assertEqual(
                artifact["metadata"]["predictive_feature_sources"],
                ["sequence_embedding_cosine", "sequence_length_coverage"],
            )
            self.assertIsInstance(
                artifact["learned_vs_heuristic_disagreements"], list
            )
            self.assertTrue(
                all(
                    row["embedding_backend"] == "esm2_t30_150m_ur50d"
                    and row["requested_embedding_backend"] == "esm2_t33_650m_ur50d"
                    and row["fallback_used"] is True
                    and row["countable_label_candidate"] is False
                    and row["ready_for_label_import"] is False
                    and row["predictive_feature_sources"]
                    == ["sequence_embedding_cosine", "sequence_length_coverage"]
                    and row["larger_model_readiness_status"]
                    == "requested_backend_unavailable_fallback_used"
                    for row in artifact["rows"]
                )
            )

        self.assertTrue(sample_audit["metadata"]["guardrail_clean"])
        self.assertTrue(pilot_sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(
            sample_audit["metadata"]["fallback_selected_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(
            pilot_sample_audit["metadata"]["fallback_selected_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(stability["metadata"]["stability_status"], "fallback_changed")
        self.assertEqual(stability["metadata"]["comparison_fallback_used"], True)
        self.assertEqual(
            stability["metadata"]["comparison_embedding_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(
            stability["metadata"]["comparison_fallback_selected_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(
            stability["metadata"]["comparison_requested_embedding_backend"],
            "esm2_t33_650m_ur50d",
        )
        self.assertEqual(
            stability["metadata"][
                "comparison_requested_expected_embedding_vector_dimension"
            ],
            1280,
        )
        self.assertEqual(
            stability["metadata"]["comparison_expected_embedding_vector_dimension"], 640
        )
        self.assertEqual(
            stability["metadata"][
                "comparison_embedding_backend_unavailable_row_count"
            ],
            0,
        )
        self.assertEqual(stability["metadata"]["nearest_reference_changed_count"], 3)
        self.assertEqual(
            stability["metadata"]["heuristic_disagreement_status_changed_count"], 4
        )
        self.assertTrue(stability["metadata"]["guardrail_clean"])
        self.assertEqual(
            pilot_stability["metadata"]["stability_status"], "fallback_changed"
        )
        self.assertEqual(pilot_stability["metadata"]["comparison_fallback_used"], True)
        self.assertEqual(
            pilot_stability["metadata"]["comparison_embedding_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(
            pilot_stability["metadata"]["comparison_fallback_selected_backend"],
            "esm2_t30_150m_ur50d",
        )
        self.assertEqual(
            pilot_stability["metadata"][
                "comparison_embedding_backend_unavailable_row_count"
            ],
            0,
        )
        self.assertEqual(
            pilot_stability["metadata"]["nearest_reference_changed_count"], 4
        )
        self.assertEqual(
            pilot_stability["metadata"][
                "heuristic_disagreement_status_changed_count"
            ],
            3,
        )
        self.assertTrue(pilot_stability["metadata"]["guardrail_clean"])


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
