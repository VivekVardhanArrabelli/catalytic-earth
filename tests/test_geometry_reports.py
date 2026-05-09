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
        self.assertEqual(summary["metadata"]["slice_count"], 9)
        self.assertEqual(summary["metadata"]["largest_slice"], "150")
        self.assertTrue(summary["metadata"]["all_zero_hard_negatives"])
        self.assertTrue(summary["metadata"]["all_zero_false_non_abstentions"])
        self.assertFalse(summary["metadata"]["all_zero_in_scope_failures"])
        self.assertTrue(summary["metadata"]["all_zero_ready_label_candidates"])
        self.assertEqual(summary["metadata"]["slices_with_in_scope_failures"], ["150"])
        self.assertEqual(summary["metadata"]["max_in_scope_failure_count"], 3)
        row_20 = summary["rows"][0]
        self.assertEqual(row_20["slice"], "20")
        self.assertEqual(row_20["mapping_issue_count"], 0)
        self.assertEqual(row_20["ready_label_candidate_count"], 0)
        row_125 = next(row for row in summary["rows"] if row["slice"] == "125")
        self.assertEqual(row_125["slice"], "125")
        self.assertEqual(row_125["hard_negative_count"], 0)
        self.assertEqual(row_125["in_scope_failure_count"], 0)
        self.assertGreater(row_125["score_separation_gap"], 0.0)
        row_150 = summary["rows"][-1]
        self.assertEqual(row_150["slice"], "150")
        self.assertEqual(row_150["hard_negative_count"], 0)
        self.assertEqual(row_150["in_scope_failure_count"], 3)
        self.assertEqual(row_150["ready_label_candidate_count"], 0)
        self.assertGreater(row_150["top1_accuracy_in_scope_evaluable"], 0.93)


if __name__ == "__main__":
    unittest.main()
