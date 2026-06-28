from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.june9_router_fold_fusion_readout import (
    build_june9_router_fold_fusion_readout,
    write_june9_router_fold_fusion_readout,
)


def _row(entry_id: str, *, true_fp: str | None, called: str, score: float) -> dict:
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": true_fp,
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _pinned(inscope: list[dict], oos: list[dict]) -> dict:
    return {
        "artifact_id": "v3_june9_router_pinned_rowdetail_operating_point",
        "pin_provenance": {"registry_pinned_to_commit": "d567ee0d"},
        "row_details_by_split": {
            "calibration": {"inscope_rows": inscope, "oos_rows": oos},
        },
    }


def _fold(scores: dict[str, float], *, inscope_ids, oos_ids) -> dict:
    return {
        "artifact_id": "fold_readout",
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


class June9RouterFoldFusionReadoutTests(unittest.TestCase):
    def test_no_pareto_improvement_when_oos_fp_are_high_fold(self) -> None:
        # 2 in-scope correct, 1 OOS FP with HIGH fold (structurally similar) ->
        # fold gate cannot reject it without dropping in-scope.
        inscope = [
            _row("in1", true_fp="fpA", called="fpA", score=0.6),
            _row("in2", true_fp="fpB", called="fpB", score=0.6),
        ]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.6)]
        scores = {"in1": 0.70, "in2": 0.72, "oos1": 0.71}
        readout = build_june9_router_fold_fusion_readout(
            pinned_june9=_pinned(inscope, oos),
            fold_readout=_fold(scores, inscope_ids=["in1", "in2"], oos_ids=["oos1"]),
            dial_threshold=0.44,
        )
        self.assertEqual(
            readout["status"],
            "june9_router_fold_gate_no_pareto_improvement_precision_recall_tradeoff_only",
        )
        self.assertFalse(readout["fold_gate_assessment"]["fold_gate_helps"])
        self.assertIsNone(
            readout["fold_gate_assessment"]["pareto_improvement_over_dial_baseline"]
        )

    def test_pareto_improvement_when_oos_fp_is_low_fold(self) -> None:
        # OOS FP has LOW fold -> a fold gate rejects it while holding both in-scope.
        inscope = [
            _row("in1", true_fp="fpA", called="fpA", score=0.6),
            _row("in2", true_fp="fpB", called="fpB", score=0.6),
        ]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.6)]
        scores = {"in1": 0.70, "in2": 0.72, "oos1": 0.30}
        readout = build_june9_router_fold_fusion_readout(
            pinned_june9=_pinned(inscope, oos),
            fold_readout=_fold(scores, inscope_ids=["in1", "in2"], oos_ids=["oos1"]),
            dial_threshold=0.44,
        )
        self.assertEqual(
            readout["status"],
            "june9_router_fold_gate_pareto_improves_operating_point",
        )
        self.assertTrue(readout["fold_gate_assessment"]["fold_gate_helps"])
        point = readout["fold_gate_assessment"]["pareto_improvement_over_dial_baseline"]
        self.assertEqual(point["inscope_correct"], 2)
        self.assertEqual(point["oos_false_positives"], 0)

    def test_baseline_and_frontier_and_residual_characterization(self) -> None:
        inscope = [_row("in1", true_fp="fpA", called="fpA", score=0.6)]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.6)]
        scores = {"in1": 0.70, "oos1": 0.71}
        readout = build_june9_router_fold_fusion_readout(
            pinned_june9=_pinned(inscope, oos),
            fold_readout=_fold(scores, inscope_ids=["in1"], oos_ids=["oos1"]),
        )
        baseline = readout["june9_baseline_fold_gate_off"]["dial_0p44_threshold"]
        self.assertEqual(baseline["inscope_correct"], 1)
        self.assertEqual(baseline["oos_false_positives"], 1)
        self.assertTrue(readout["fold_coverage"]["coverage_complete"])
        self.assertFalse(readout["guardrails"]["live_registry_mutated"])
        residual = readout["fold_gate_assessment"][
            "residual_oos_false_positives_at_dial"
        ]
        self.assertEqual(residual[0]["entry_id"], "oos1")

    def test_writer_emits_json_and_report(self) -> None:
        inscope = [_row("in1", true_fp="fpA", called="fpA", score=0.6)]
        oos = [_row("oos1", true_fp=None, called="fpA", score=0.6)]
        scores = {"in1": 0.70, "oos1": 0.30}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pinned = root / "pinned.json"
            fold = root / "fold.json"
            out = root / "readout.json"
            report = root / "readout.md"
            pinned.write_text(json.dumps(_pinned(inscope, oos)), encoding="utf-8")
            fold.write_text(
                json.dumps(_fold(scores, inscope_ids=["in1"], oos_ids=["oos1"])),
                encoding="utf-8",
            )
            readout = write_june9_router_fold_fusion_readout(
                pinned_june9_path=pinned,
                fold_readout_path=fold,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], readout["artifact_id"]
            )
            self.assertIn("Precision/Recall Frontier", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", readout)


if __name__ == "__main__":
    unittest.main()
