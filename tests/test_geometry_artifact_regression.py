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
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope"
            ]
        )


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
