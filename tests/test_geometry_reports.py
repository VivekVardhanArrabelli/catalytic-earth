from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.geometry_reports import summarize_geometry_slices


class GeometryReportTests(unittest.TestCase):
    def test_summarize_geometry_slices(self) -> None:
        summary = summarize_geometry_slices(ROOT / "artifacts")
        self.assertEqual(summary["metadata"]["slice_count"], 14)
        self.assertEqual(summary["metadata"]["largest_slice"], "275")
        self.assertTrue(summary["metadata"]["all_zero_hard_negatives"])
        self.assertTrue(summary["metadata"]["all_zero_false_non_abstentions"])
        self.assertFalse(summary["metadata"]["all_zero_in_scope_failures"])
        self.assertTrue(summary["metadata"]["all_zero_ready_label_candidates"])
        self.assertTrue(summary["metadata"]["all_zero_actionable_in_scope_failures"])
        self.assertEqual(
            summary["metadata"]["slices_with_in_scope_failures"],
            ["150", "175", "200", "225", "250", "275"],
        )
        self.assertEqual(summary["metadata"]["max_in_scope_failure_count"], 1)
        self.assertEqual(summary["metadata"]["total_in_scope_failure_count"], 6)
        self.assertEqual(summary["metadata"]["max_actionable_in_scope_failure_count"], 0)
        self.assertEqual(summary["metadata"]["total_actionable_in_scope_failure_count"], 0)
        self.assertEqual(summary["metadata"]["max_cofactor_expected_absent_count"], 3)
        self.assertIn("150", summary["metadata"]["slices_with_absent_expected_cofactors"])
        self.assertEqual(
            summary["metadata"]["max_cofactor_evidence_limited_retained_count"],
            3,
        )
        self.assertIn(
            "150",
            summary["metadata"]["slices_with_limited_retained_cofactor_evidence"],
        )
        self.assertEqual(summary["metadata"]["slices_with_lossless_cofactor_penalty"], [])
        self.assertEqual(summary["metadata"]["minimum_evidence_limited_retained_margin"], 0.013)
        self.assertEqual(summary["metadata"]["max_out_of_scope_retained_seed_family_count"], 0)
        self.assertEqual(summary["metadata"]["slices_with_near_misses"], [])
        self.assertIsNone(summary["metadata"]["minimum_near_miss_score_gap_to_floor"])
        self.assertEqual(summary["metadata"]["minimum_below_floor_score_gap"], 0.0131)
        self.assertEqual(summary["metadata"]["closest_below_floor_slice"], "175")
        self.assertEqual(summary["metadata"]["closest_below_floor_entry_id"], "m_csa:65")
        self.assertEqual(
            summary["metadata"]["closest_below_floor_top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertIn(
            "150",
            summary["metadata"]["slices_recommending_audit_only_cofactor_policy"],
        )
        row_20 = summary["rows"][0]
        self.assertEqual(row_20["slice"], "20")
        self.assertEqual(row_20["mapping_issue_count"], 0)
        self.assertEqual(row_20["ready_label_candidate_count"], 0)
        row_125 = next(row for row in summary["rows"] if row["slice"] == "125")
        self.assertEqual(row_125["slice"], "125")
        self.assertEqual(row_125["hard_negative_count"], 0)
        self.assertEqual(row_125["in_scope_failure_count"], 0)
        self.assertGreater(row_125["score_separation_gap"], 0.0)
        row_150 = next(row for row in summary["rows"] if row["slice"] == "150")
        self.assertEqual(row_150["slice"], "150")
        self.assertEqual(row_150["hard_negative_count"], 0)
        self.assertEqual(row_150["entries_with_structure_ligands"], 135)
        self.assertEqual(row_150["entries_with_structure_inferred_cofactors"], 92)
        self.assertEqual(row_150["in_scope_failure_count"], 1)
        self.assertEqual(row_150["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_150["evidence_limited_abstention_count"], 1)
        self.assertEqual(row_150["cofactor_expected_absent_count"], 2)
        self.assertEqual(row_150["cofactor_expected_absent_abstained_count"], 1)
        self.assertEqual(row_150["cofactor_expected_absent_retained_count"], 1)
        self.assertEqual(row_150["cofactor_structure_only_retained_count"], 1)
        self.assertEqual(row_150["cofactor_evidence_limited_retained_count"], 2)
        self.assertEqual(row_150["cofactor_evidence_limited_abstained_count"], 1)
        self.assertEqual(row_150["cofactor_policy_recommendation"], "audit_only_or_separate_stratum")
        self.assertEqual(row_150["cofactor_policy_lossless_decision_changing_policy_count"], 0)
        self.assertEqual(row_150["cofactor_policy_guardrail_passing_policy_count"], 24)
        self.assertEqual(row_150["cofactor_policy_minimum_evidence_limited_retained_margin"], 0.0307)
        self.assertEqual(row_150["seed_family_count"], 7)
        self.assertEqual(row_150["largest_seed_family"], "flavin_dehydrogenase_reductase")
        self.assertEqual(row_150["largest_seed_family_count"], 18)
        self.assertEqual(row_150["weakest_retained_seed_family"], "flavin_monooxygenase")
        self.assertEqual(row_150["out_of_scope_retained_seed_family_count"], 0)
        self.assertEqual(row_150["ready_label_candidate_count"], 0)
        self.assertGreater(row_150["top1_accuracy_in_scope_evaluable"], 0.97)
        row_175 = next(row for row in summary["rows"] if row["slice"] == "175")
        self.assertEqual(row_175["slice"], "175")
        self.assertEqual(row_175["hard_negative_count"], 0)
        self.assertEqual(row_175["near_miss_count"], 0)
        self.assertEqual(
            row_175["near_miss_top1_fingerprint_counts"],
            {},
        )
        self.assertIsNone(row_175["closest_near_miss_entry_id"])
        self.assertIsNone(row_175["closest_near_miss_top1_fingerprint_id"])
        self.assertIsNone(row_175["closest_near_miss_score_gap_to_floor"])
        self.assertEqual(row_175["closest_below_floor_entry_id"], "m_csa:65")
        self.assertEqual(
            row_175["closest_below_floor_top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(row_175["minimum_below_floor_score_gap"], 0.0131)
        self.assertEqual(row_175["in_scope_failure_count"], 1)
        self.assertEqual(row_175["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_175["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(row_175["cofactor_policy_recommendation"], "audit_only_or_separate_stratum")
        self.assertEqual(row_175["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_175["largest_seed_family_count"], 28)
        row_200 = next(row for row in summary["rows"] if row["slice"] == "200")
        self.assertEqual(row_200["slice"], "200")
        self.assertEqual(row_200["evaluated_count"], 200)
        self.assertEqual(row_200["evaluable_count"], 197)
        self.assertEqual(row_200["in_scope_count"], 65)
        self.assertEqual(row_200["hard_negative_count"], 0)
        self.assertEqual(row_200["near_miss_count"], 0)
        self.assertEqual(row_200["in_scope_failure_count"], 1)
        self.assertEqual(row_200["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_200["cofactor_expected_absent_count"], 3)
        self.assertEqual(row_200["cofactor_evidence_limited_abstained_count"], 1)
        self.assertEqual(row_200["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_200["largest_seed_family_count"], 31)
        self.assertEqual(row_200["ready_label_candidate_count"], 0)
        row_225 = next(row for row in summary["rows"] if row["slice"] == "225")
        self.assertEqual(row_225["slice"], "225")
        self.assertEqual(row_225["evaluated_count"], 224)
        self.assertEqual(row_225["evaluable_count"], 221)
        self.assertEqual(row_225["in_scope_count"], 71)
        self.assertEqual(row_225["hard_negative_count"], 0)
        self.assertEqual(row_225["near_miss_count"], 0)
        self.assertEqual(row_225["in_scope_failure_count"], 1)
        self.assertEqual(row_225["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_225["cofactor_expected_absent_count"], 3)
        self.assertEqual(row_225["cofactor_evidence_limited_abstained_count"], 1)
        self.assertEqual(row_225["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_225["largest_seed_family_count"], 32)
        self.assertEqual(row_225["ready_label_candidate_count"], 0)
        row_250 = next(row for row in summary["rows"] if row["slice"] == "250")
        self.assertEqual(row_250["slice"], "250")
        self.assertEqual(row_250["evaluated_count"], 249)
        self.assertEqual(row_250["evaluable_count"], 246)
        self.assertEqual(row_250["in_scope_count"], 78)
        self.assertEqual(row_250["hard_negative_count"], 0)
        self.assertEqual(row_250["near_miss_count"], 0)
        self.assertEqual(row_250["in_scope_failure_count"], 1)
        self.assertEqual(row_250["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_250["cofactor_expected_absent_count"], 3)
        self.assertEqual(row_250["cofactor_evidence_limited_abstained_count"], 1)
        self.assertEqual(row_250["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_250["largest_seed_family_count"], 34)
        self.assertEqual(row_250["ready_label_candidate_count"], 0)
        row_275 = summary["rows"][-1]
        self.assertEqual(row_275["slice"], "275")
        self.assertEqual(row_275["evaluated_count"], 274)
        self.assertEqual(row_275["evaluable_count"], 271)
        self.assertEqual(row_275["in_scope_count"], 81)
        self.assertEqual(row_275["hard_negative_count"], 0)
        self.assertEqual(row_275["near_miss_count"], 0)
        self.assertEqual(row_275["in_scope_failure_count"], 1)
        self.assertEqual(row_275["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_275["cofactor_expected_absent_count"], 3)
        self.assertEqual(row_275["cofactor_evidence_limited_abstained_count"], 1)
        self.assertEqual(row_275["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_275["largest_seed_family_count"], 35)
        self.assertEqual(row_275["ready_label_candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
