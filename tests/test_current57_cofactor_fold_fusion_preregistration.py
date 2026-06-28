from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.current57_cofactor_fold_fusion_preregistration import (
    build_current57_cofactor_fold_fusion_preregistration,
    write_current57_cofactor_fold_fusion_preregistration,
)


def _row(entry_id: str, *, true_fp: str | None, called: str, score: float) -> dict:
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": true_fp,
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _operating_point(inscope: list[dict], oos: list[dict]) -> dict:
    return {
        "artifact_id": "current57_rerun",
        "row_details_by_split": {
            "calibration": {"inscope_rows": inscope, "oos_rows": oos},
        },
    }


def _fold_readout(scores: dict[str, float], *, inscope_ids, oos_ids) -> dict:
    return {
        "artifact_id": "fold_readout",
        "schema_version": "current57_fold_tm_recompute_readout.v1",
        "rows": {
            "calibration_inscope": [
                {"entry_id": i, "fold_nn_alntmscore": scores.get(i)}
                for i in inscope_ids
            ],
            "calibration_oos": [
                {"entry_id": i, "fold_nn_alntmscore": scores.get(i)} for i in oos_ids
            ],
        },
    }


def _trusted(min_correct: int, max_fp: int) -> dict:
    return {
        "artifact_id": "trusted_june9",
        "operating_points_by_split": {
            "calibration": {
                "fused_frozen_threshold": {
                    "inscope_correct": min_correct,
                    "inscope_total": 4,
                    "oos_false_positives": max_fp + 1,
                    "oos_total": 4,
                }
            }
        },
        "dial_comparison": {
            "threshold_dial_matching_suppression_precision": {
                "inscope_correct": min_correct,
                "inscope_total": 4,
                "oos_false_positives": max_fp,
                "oos_total": 4,
                "threshold": 0.44,
            }
        },
    }


class FusionPreregistrationTests(unittest.TestCase):
    def test_fold_gate_rejects_oos_and_recovers_eligibility(self) -> None:
        # 2 in-scope correct calls (high cofactor + high fold), 2 OOS with high
        # cofactor but LOW fold so the fold gate rejects them.
        inscope = [
            _row("in1", true_fp="fpA", called="fpA", score=0.8),
            _row("in2", true_fp="fpB", called="fpB", score=0.8),
        ]
        oos = [
            _row("oos1", true_fp=None, called="fpA", score=0.8),
            _row("oos2", true_fp=None, called="fpB", score=0.8),
        ]
        scores = {"in1": 0.80, "in2": 0.80, "oos1": 0.30, "oos2": 0.30}
        prereg = build_current57_cofactor_fold_fusion_preregistration(
            current_operating_point=_operating_point(inscope, oos),
            fold_readout=_fold_readout(
                scores, inscope_ids=["in1", "in2"], oos_ids=["oos1", "oos2"]
            ),
            trusted_precision=_trusted(min_correct=2, max_fp=0),
        )
        self.assertEqual(
            prereg["status"],
            "eligible_current57_cofactor_fold_fusion_contract_found",
        )
        selected = prereg["selection_rule"]["selected_point"]
        self.assertEqual(selected["inscope_correct"], 2)
        self.assertEqual(selected["oos_false_positives"], 0)
        self.assertTrue(prereg["fold_coverage"]["coverage_complete"])

    def test_blocks_when_recovery_ceiling_below_bar(self) -> None:
        # Only 1 in-scope call is even compatible-correct, but the bar needs 2.
        inscope = [
            _row("in1", true_fp="fpA", called="fpA", score=0.8),
            _row("in2", true_fp="fpB", called="fpC", score=0.8),  # wrong call
        ]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.3)]
        scores = {"in1": 0.80, "in2": 0.80, "oos1": 0.20}
        prereg = build_current57_cofactor_fold_fusion_preregistration(
            current_operating_point=_operating_point(inscope, oos),
            fold_readout=_fold_readout(
                scores, inscope_ids=["in1", "in2"], oos_ids=["oos1"]
            ),
            trusted_precision=_trusted(min_correct=2, max_fp=0),
        )
        self.assertEqual(
            prereg["status"],
            "blocked_current57_cofactor_fold_fusion_not_deployable",
        )
        self.assertEqual(
            prereg["recovery_ceiling"]["compatible_recovery_ceiling"], 1
        )
        self.assertEqual(prereg["selection_rule"]["eligible_points"], [])

    def test_reports_fold_marginal_value_over_cofactor_only(self) -> None:
        # Cofactor-only cannot separate (an OOS shares the same cofactor score as
        # an in-scope row); the fold gate cuts the OOS while keeping the in-scope.
        inscope = [
            _row("in1", true_fp="fpA", called="fpA", score=0.6),
            _row("in2", true_fp="fpB", called="fpB", score=0.6),
        ]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.6)]
        scores = {"in1": 0.80, "in2": 0.80, "oos1": 0.30}
        prereg = build_current57_cofactor_fold_fusion_preregistration(
            current_operating_point=_operating_point(inscope, oos),
            fold_readout=_fold_readout(
                scores, inscope_ids=["in1", "in2"], oos_ids=["oos1"]
            ),
            trusted_precision=_trusted(min_correct=2, max_fp=0),
        )
        marginal = prereg["fold_marginal_value"]
        cofactor_only = marginal["cofactor_only_best_under_trusted_oos_fp"]
        fusion = marginal["fusion_best_under_trusted_oos_fp"]
        # Cofactor-only at FP<=0 must drop both in-scope (score 0.6 == OOS 0.6),
        # while fusion keeps both via the fold gate.
        self.assertEqual(fusion["inscope_correct"], 2)
        self.assertEqual(fusion["oos_false_positives"], 0)
        self.assertGreaterEqual(
            marginal["fold_recovery_gain_at_oos_fp_ceiling"],
            2 - (cofactor_only["inscope_correct"] if cofactor_only else 0),
        )

    def test_writer_emits_json_and_report(self) -> None:
        inscope = [_row("in1", true_fp="fpA", called="fpA", score=0.8)]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.3)]
        scores = {"in1": 0.80, "oos1": 0.30}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            op = root / "op.json"
            fr = root / "fold.json"
            tr = root / "trusted.json"
            out = root / "prereg.json"
            report = root / "prereg.md"
            op.write_text(json.dumps(_operating_point(inscope, oos)), encoding="utf-8")
            fr.write_text(
                json.dumps(
                    _fold_readout(scores, inscope_ids=["in1"], oos_ids=["oos1"])
                ),
                encoding="utf-8",
            )
            tr.write_text(json.dumps(_trusted(min_correct=1, max_fp=0)), encoding="utf-8")

            prereg = write_current57_cofactor_fold_fusion_preregistration(
                current_operating_point_path=op,
                fold_readout_path=fr,
                trusted_precision_path=tr,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], prereg["artifact_id"]
            )
            self.assertIn("Fold-NN Marginal Value", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", prereg)


if __name__ == "__main__":
    unittest.main()
