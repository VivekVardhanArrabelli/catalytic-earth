from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cofactor_fusion_operating_point import (
    _dial_comparison,
    _fp_called_distribution,
    _inscope_correct,
    _lever2_complementary_summary,
    _operating_points_by_split,
    _oos_false_positive,
    _point,
    _row_details_by_split,
    _suppressed_inscope_correct,
    _suppressed_oos_fp,
    _threshold_sweep_by_split,
    multi_dir_staged_cif_fetcher,
)


def _inscope(entry_id, *, score, top1, true, split):
    return {
        "entry_id": entry_id,
        "predicted_geometry_joined": True,
        "top1_score": score,
        "top1_fingerprint_id": top1,
        "true_fingerprint_id": true,
        "abstained": score < 0.4115,
    }


def _oos(entry_id, *, score, top1, split, abstained=None):
    return {
        "entry_id": entry_id,
        "predicted_geometry_joined": True,
        "top1_score": score,
        "top1_fingerprint_id": top1,
        "true_fingerprint_id": None,
        "abstained": (score < 0.4115) if abstained is None else abstained,
    }


class MultiDirFetcherTests(unittest.TestCase):
    def test_reads_first_matching_dir_and_excludes_missing(self) -> None:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            da, db = Path(a), Path(b)
            (db / "afdb_P0_v6.cif").write_text("data_b\n", encoding="utf-8")
            (da / "afdb_P1_v6.cif").write_text("data_a\n", encoding="utf-8")
            fetch = multi_dir_staged_cif_fetcher([da, db])
            self.assertEqual(fetch("P1")[0], "data_a\n")  # found in first dir
            self.assertEqual(fetch("P0")[0], "data_b\n")  # falls through to second
            with self.assertRaises(RuntimeError):
                fetch("MISSING")


class ScoringPrimitiveTests(unittest.TestCase):
    def test_inscope_correct_requires_retained_true_class(self) -> None:
        retained = _inscope("m_csa:1", score=0.6, top1="plp", true="plp", split="train")
        self.assertTrue(_inscope_correct(retained, 0.4115))
        self.assertFalse(_inscope_correct(retained, 0.7))  # below threshold -> abstain
        wrong = _inscope("m_csa:2", score=0.6, top1="heme", true="plp", split="train")
        self.assertFalse(_inscope_correct(wrong, 0.4115))

    def test_oos_false_positive_is_any_nonabstained_call(self) -> None:
        fp = _oos("m_csa:9", score=0.6, top1="metal_dependent_hydrolase", split="train")
        self.assertTrue(_oos_false_positive(fp, 0.4115))
        self.assertFalse(_oos_false_positive(fp, 0.7))  # raising threshold abstains it

    def test_suppression_helpers_use_abstained_flag(self) -> None:
        kept = {
            "abstained": False,
            "top1_fingerprint_id": "plp",
            "true_fingerprint_id": "plp",
        }
        self.assertTrue(_suppressed_inscope_correct(kept))
        self.assertTrue(_suppressed_oos_fp({"abstained": False}))
        self.assertFalse(_suppressed_oos_fp({"abstained": True}))

    def test_point_rates(self) -> None:
        p = _point(inscope_correct=3, inscope_total=4, oos_fp=1, oos_total=8)
        self.assertEqual(p["inscope_recall"], 0.75)
        self.assertEqual(p["oos_false_positive_rate"], 0.125)


class ThresholdSweepAndDialTests(unittest.TestCase):
    def test_threshold_dial_dominates_suppression_when_recall_higher_at_same_fp(
        self,
    ) -> None:
        # Build a calibration surface where raising the threshold removes the OOS
        # FP at no recall cost, so the threshold dial dominates suppression.
        split_by = {"in1": "calibration", "in2": "calibration", "oo1": "calibration"}
        inscope_fused = [
            _inscope("in1", score=0.9, top1="plp", true="plp", split="calibration"),
            _inscope("in2", score=0.9, top1="heme", true="heme", split="calibration"),
        ]
        # One OOS row scores just above the frozen threshold (a FP) but below 0.45.
        oos_fused = [
            _oos("oo1", score=0.43, top1="metal_dependent_hydrolase", split="calibration")
        ]
        sweep = _threshold_sweep_by_split(
            inscope_fused=inscope_fused,
            oos_fused=oos_fused,
            split_by=split_by,
            splits=("train", "calibration"),
            threshold_grid=(0.4115, 0.45),
        )
        cal = {p["threshold"]: p for p in sweep["calibration"]}
        self.assertEqual(cal[0.4115]["oos_false_positives"], 1)
        self.assertEqual(cal[0.45]["oos_false_positives"], 0)
        self.assertEqual(cal[0.45]["inscope_correct"], 2)  # recall unchanged

        # Suppression dial reaches FP 0 but only by also dropping an in-scope row.
        inscope = {
            "apo": [],
            "fused": inscope_fused,
            "fused_suppressed": [
                dict(inscope_fused[0], abstained=False),
                dict(inscope_fused[1], abstained=True),  # suppressed -> recall lost
            ],
        }
        oos = {
            "apo": [],
            "fused": oos_fused,
            "fused_suppressed": [dict(oos_fused[0], abstained=True)],
        }
        op = _operating_points_by_split(
            inscope=inscope,
            oos=oos,
            split_by=split_by,
            splits=("calibration",),
            threshold=0.4115,
        )
        dc = _dial_comparison(op, sweep)
        self.assertEqual(dc["suppression_dial"]["oos_false_positives"], 0)
        self.assertEqual(dc["suppression_dial"]["inscope_correct"], 1)
        # Threshold dial reaches FP 0 at recall 2 > suppression recall 1.
        self.assertTrue(dc["threshold_dial_dominates_suppression_dial"])
        self.assertEqual(
            dc["threshold_dial_matching_suppression_precision"]["threshold"], 0.45
        )

    def test_row_details_expose_train_cal_flags(self) -> None:
        split_by = {"in1": "calibration", "oo1": "calibration"}
        inscope = {
            "apo": [
                _inscope("in1", score=0.3, top1="heme", true="plp", split="calibration")
            ],
            "fused": [
                _inscope("in1", score=0.8, top1="plp", true="plp", split="calibration")
            ],
            "fused_suppressed": [
                dict(
                    _inscope("in1", score=0.8, top1="plp", true="plp", split="calibration"),
                    abstained=False,
                )
            ],
        }
        oos = {
            "apo": [
                _oos("oo1", score=0.2, top1="metal_dependent_hydrolase", split="calibration")
            ],
            "fused": [
                _oos("oo1", score=0.5, top1="metal_dependent_hydrolase", split="calibration")
            ],
            "fused_suppressed": [
                dict(
                    _oos(
                        "oo1",
                        score=0.5,
                        top1="metal_dependent_hydrolase",
                        split="calibration",
                    ),
                    abstained=True,
                )
            ],
        }
        details = _row_details_by_split(
            inscope=inscope,
            oos=oos,
            split_by=split_by,
            splits=("calibration",),
            threshold=0.4115,
        )["calibration"]
        self.assertTrue(details["is_out_of_sample_for_channel"])
        self.assertTrue(details["inscope_rows"][0]["fused_correct_at_threshold"])
        self.assertFalse(details["inscope_rows"][0]["apo_correct_at_threshold"])
        self.assertTrue(details["oos_rows"][0]["fused_false_positive_at_threshold"])
        self.assertFalse(details["oos_rows"][0]["suppressed_false_positive"])


class FpDistributionAndLever2Tests(unittest.TestCase):
    def test_fp_called_distribution_counts_only_nonabstained(self) -> None:
        rows = [
            _oos("a", score=0.6, top1="metal_dependent_hydrolase", split="train"),
            _oos("b", score=0.6, top1="metal_dependent_hydrolase", split="train"),
            _oos("c", score=0.6, top1="plp_dependent_enzyme", split="train"),
            _oos("d", score=0.30, top1="heme_peroxidase_oxidase", split="train"),
        ]
        dist = _fp_called_distribution(rows, 0.4115)
        self.assertEqual(dist["metal_dependent_hydrolase"], 2)
        self.assertEqual(dist["plp_dependent_enzyme"], 1)
        self.assertNotIn("heme_peroxidase_oxidase", dist)  # abstained, not a FP

    def test_lever2_summary_picks_full_overlay_not_smoke(self) -> None:
        readout = {
            "artifact_id": "lever2_x",
            "measured_readout": {
                "fixed_operating_point_variants": [
                    {
                        "direct_source_free_electron_flow_fields_used": False,
                        "calibration_oos_abstain_recall": 0.466667,
                    },
                    {
                        "direct_source_free_electron_flow_fields_used": True,
                        "calibration_oos_abstain_recall": 0.48,
                        "incremental_oos_abstain_recall_vs_current_geometry_fold": 0.0133,
                        "primary_retain_recall": 1.0,
                    },
                    {
                        "direct_source_free_electron_flow_fields_used": True,
                        "calibration_oos_abstain_recall": 0.506667,
                        "incremental_oos_abstain_recall_vs_current_geometry_fold": 0.04,
                        "primary_retain_recall": 1.0,
                    },
                ]
            },
        }
        summary = _lever2_complementary_summary(readout)
        self.assertEqual(
            summary["measured_incremental_oos_abstain_recall_vs_geometry_fold"], 0.04
        )
        self.assertEqual(summary["with_electron_flow_oos_abstain_recall"], 0.506667)
        self.assertEqual(summary["primary_retain_recall"], 1.0)

    def test_lever2_summary_without_readout_is_documented_fallback(self) -> None:
        summary = _lever2_complementary_summary(None)
        self.assertIn("documented", str(summary[
            "measured_incremental_oos_abstain_recall_vs_geometry_fold"
        ]))


if __name__ == "__main__":
    unittest.main()
