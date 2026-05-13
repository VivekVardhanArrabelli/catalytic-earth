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
        failure_mode_audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_source_failure_mode_audit_1025.json"
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
        self.assertEqual(structure_mapping_sample["metadata"]["candidate_count"], 4)
        self.assertEqual(
            structure_mapping_sample["metadata"]["mapped_candidate_count"], 4
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
        self.assertEqual(heuristic_control_scores["metadata"]["candidate_count"], 4)
        self.assertEqual(
            heuristic_control_scores["metadata"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 4},
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
        self.assertEqual(external_transfer_gate["metadata"]["gate_count"], 22)
        self.assertEqual(external_transfer_gate["metadata"]["passed_gate_count"], 22)
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
            4,
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
            4,
        )
        self.assertTrue(
            external_transfer_gate["gates"]["external_failure_mode_audit_review_only"]
        )
        self.assertEqual(
            external_transfer_gate["metadata"]["external_failure_mode_count"], 5
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
        self.assertEqual(reaction_evidence["metadata"]["candidate_count"], 6)
        self.assertEqual(
            reaction_evidence["metadata"]["candidate_with_reaction_context_count"], 6
        )
        self.assertEqual(
            reaction_evidence["metadata"]["broad_or_incomplete_ec_count"], 3
        )
        self.assertEqual(
            reaction_evidence["metadata"]["broad_or_incomplete_ec_numbers"],
            ["1.1.1.-", "1.11.1.-", "1.8.-.-"],
        )
        self.assertEqual(reaction_evidence["metadata"]["fetch_failure_count"], 0)
        self.assertGreater(reaction_evidence["metadata"]["reaction_record_count"], 0)
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
            reaction_evidence_audit["metadata"]["broad_ec_context_row_count"], 6
        )
        self.assertEqual(reaction_evidence_audit["blockers"], [])
        self.assertTrue(lane_balance["metadata"]["guardrail_clean"])
        self.assertEqual(lane_balance["metadata"]["lane_count"], 6)
        self.assertEqual(lane_balance["metadata"]["dominant_lane_fraction"], 0.1667)
        self.assertEqual(lane_balance["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(lane_balance["blockers"], [])


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
