from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class GeometryArtifactRegressionTests(unittest.TestCase):
    def test_125_entry_geometry_artifacts_remain_clean(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_125.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_125.json")
        margins = _load_json(ROOT / "artifacts" / "v3_geometry_score_margins_125.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_125.json"
        )

        self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope_evaluable"], 1.0)
        self.assertEqual(evaluation["metadata"]["top3_accuracy_in_scope_evaluable"], 1.0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 1.0)
        self.assertEqual(
            evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"],
            0,
        )
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
            ]
        )
        self.assertGreater(margins["metadata"]["score_separation_gap"], 0.0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 0)

    def test_regression_slices_have_no_hard_negatives(self) -> None:
        for suffix in ["", "_30", "_40", "_50", "_60", "_75", "_100"]:
            with self.subTest(suffix=suffix or "_20"):
                hard_negatives = _load_json(
                    ROOT / "artifacts" / f"v3_hard_negative_controls{suffix}.json"
                )
                evaluation = _load_json(
                    ROOT / "artifacts" / f"v3_geometry_label_eval{suffix}.json"
                )
                self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
                self.assertEqual(
                    evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"],
                    0,
                )
                self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope_evaluable"], 1.0)

    def test_150_entry_geometry_artifacts_hold_out_of_scope_line(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_150.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_150.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_150.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_150.json")
        cofactor_policy = _load_json(ROOT / "artifacts" / "v3_cofactor_policy_150.json")
        seed_family = _load_json(ROOT / "artifacts" / "v3_seed_family_performance_150.json")
        margins = _load_json(ROOT / "artifacts" / "v3_geometry_score_margins_150.json")

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 44)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(
            in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1
        )
        self.assertEqual(in_scope_failures["metadata"]["top1_mismatch_count"], 1)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_count"], 2)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_retained_count"], 1)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_abstained_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["expected_absent_retained_entry_ids"],
            ["m_csa:41"],
        )
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_retained_entry_ids"],
            ["m_csa:41", "m_csa:108"],
        )
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132"],
        )
        self.assertEqual(
            cofactor_policy["metadata"]["audit_evidence_limited_retained_positive_entry_ids"],
            ["m_csa:41", "m_csa:108"],
        )
        self.assertEqual(
            cofactor_policy["metadata"]["lossless_decision_changing_policy_count"],
            0,
        )
        self.assertEqual(
            cofactor_policy["metadata"]["minimum_evidence_limited_retained_margin"],
            0.0277,
        )
        self.assertEqual(
            cofactor_policy["metadata"]["recommendation"],
            "audit_only_or_separate_stratum",
        )
        self.assertEqual(seed_family["metadata"]["in_scope_family_count"], 7)
        self.assertEqual(seed_family["metadata"]["out_of_scope_retained_family_count"], 0)
        self.assertEqual(
            seed_family["metadata"]["weakest_retained_in_scope_family"],
            "flavin_monooxygenase",
        )
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope"
            ]
        )

    def test_175_entry_geometry_artifacts_expose_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_175.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_175.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_175.json"
        )
        cofactor_policy = _load_json(ROOT / "artifacts" / "v3_cofactor_policy_175.json")
        seed_family = _load_json(ROOT / "artifacts" / "v3_seed_family_performance_175.json")

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 59)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9831)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["near_miss_top1_fingerprint_counts"],
            {},
        )
        self.assertEqual(
            hard_negatives["metadata"]["near_miss_cofactor_evidence_counts"],
            {},
        )
        self.assertIsNone(hard_negatives["metadata"]["closest_near_miss_entry_id"])
        self.assertIsNone(hard_negatives["metadata"]["minimum_near_miss_score_gap_to_floor"])
        self.assertEqual(hard_negatives["near_miss_groups"], [])
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(
            cofactor_policy["metadata"]["recommendation"],
            "audit_only_or_separate_stratum",
        )
        self.assertEqual(seed_family["metadata"]["largest_in_scope_family"], "metal_dependent_hydrolase")
        self.assertEqual(seed_family["metadata"]["largest_in_scope_family_count"], 28)

    def test_200_entry_geometry_artifacts_clear_new_hard_negatives(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_200.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_200.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_200.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_200.json"
        )
        mapping_issues = _load_json(
            ROOT / "artifacts" / "v3_structure_mapping_issues_200.json"
        )

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 225)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 65)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 135)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9846)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["closest_below_floor_entry_id"],
            "m_csa:134",
        )
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(label_candidates["metadata"]["ready_for_label_review_count"], 0)
        self.assertEqual(mapping_issues["metadata"]["issue_count"], 3)

    def test_225_entry_geometry_artifacts_clear_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_225.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_225.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_225.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_225.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_225.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_225.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 225)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 71)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 153)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9859)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["closest_below_floor_entry_id"],
            "m_csa:134",
        )
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132"],
        )
        alanine_racemase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:213"
        )
        self.assertIn("plp", alanine_racemase["ligand_context"]["cofactor_families"])
        self.assertEqual(
            alanine_racemase["top_fingerprints"][0]["fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertGreaterEqual(alanine_racemase["top_fingerprints"][0]["score"], 0.4145)
        self.assertEqual(label_candidates["metadata"]["ready_for_label_review_count"], 0)


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
