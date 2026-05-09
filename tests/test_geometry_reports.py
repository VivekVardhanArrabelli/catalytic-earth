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
        self.assertEqual(summary["metadata"]["slice_count"], 10)
        self.assertEqual(summary["metadata"]["largest_slice"], "175")
        self.assertTrue(summary["metadata"]["all_zero_hard_negatives"])
        self.assertTrue(summary["metadata"]["all_zero_false_non_abstentions"])
        self.assertFalse(summary["metadata"]["all_zero_in_scope_failures"])
        self.assertTrue(summary["metadata"]["all_zero_ready_label_candidates"])
        self.assertTrue(summary["metadata"]["all_zero_actionable_in_scope_failures"])
        self.assertEqual(summary["metadata"]["slices_with_in_scope_failures"], ["150", "175"])
        self.assertEqual(summary["metadata"]["max_in_scope_failure_count"], 1)
        self.assertEqual(summary["metadata"]["max_actionable_in_scope_failure_count"], 0)
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
        self.assertEqual(summary["metadata"]["minimum_evidence_limited_retained_margin"], 0.0009)
        self.assertEqual(summary["metadata"]["max_out_of_scope_retained_seed_family_count"], 0)
        self.assertEqual(summary["metadata"]["slices_with_near_misses"], ["175"])
        self.assertEqual(summary["metadata"]["minimum_near_miss_score_gap_to_floor"], 0.001)
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
        self.assertEqual(row_150["cofactor_policy_guardrail_passing_policy_count"], 30)
        self.assertEqual(row_150["cofactor_policy_minimum_evidence_limited_retained_margin"], 0.1029)
        self.assertEqual(row_150["seed_family_count"], 7)
        self.assertEqual(row_150["largest_seed_family"], "flavin_dehydrogenase_reductase")
        self.assertEqual(row_150["largest_seed_family_count"], 18)
        self.assertEqual(row_150["weakest_retained_seed_family"], "flavin_monooxygenase")
        self.assertEqual(row_150["out_of_scope_retained_seed_family_count"], 0)
        self.assertEqual(row_150["ready_label_candidate_count"], 0)
        self.assertGreater(row_150["top1_accuracy_in_scope_evaluable"], 0.97)
        row_175 = summary["rows"][-1]
        self.assertEqual(row_175["slice"], "175")
        self.assertEqual(row_175["hard_negative_count"], 0)
        self.assertEqual(row_175["near_miss_count"], 17)
        self.assertEqual(
            row_175["near_miss_top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 17},
        )
        self.assertEqual(row_175["closest_near_miss_entry_id"], "m_csa:65")
        self.assertEqual(row_175["closest_near_miss_top1_fingerprint_id"], "metal_dependent_hydrolase")
        self.assertEqual(row_175["closest_near_miss_score_gap_to_floor"], 0.001)
        self.assertEqual(row_175["in_scope_failure_count"], 1)
        self.assertEqual(row_175["actionable_in_scope_failure_count"], 0)
        self.assertEqual(row_175["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(row_175["cofactor_policy_recommendation"], "audit_only_or_separate_stratum")
        self.assertEqual(row_175["largest_seed_family"], "metal_dependent_hydrolase")
        self.assertEqual(row_175["largest_seed_family_count"], 28)


if __name__ == "__main__":
    unittest.main()
