from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_offmcsa_fold_abstention_readout import (
    best_fold_nn_by_query,
    build_external_offmcsa_fold_abstention_readout,
    write_external_offmcsa_fold_abstention_readout,
)


def _mcsa_readout(inscope: list[float], oos: list[float]) -> dict:
    return {
        "artifact_id": "mcsa_fold_readout",
        "rows": {
            "calibration_inscope": [
                {"entry_id": f"in{i}", "fold_nn_scored": True, "fold_nn_alntmscore": v}
                for i, v in enumerate(inscope)
            ],
            "calibration_oos": [
                {"entry_id": f"oos{i}", "fold_nn_scored": True, "fold_nn_alntmscore": v}
                for i, v in enumerate(oos)
            ],
        },
    }


def _tsv(rows: list[tuple[str, str, float]]) -> str:
    # query, target, qtm, ttm, alntm, prob, bits
    return "\n".join(
        f"afdb_{q}\tafdb_{t}_v6\t{a}\t{a}\t{a}\t0.5\t50" for q, t, a in rows
    )


class OffMcsaFoldAbstentionReadoutTests(unittest.TestCase):
    def test_best_fold_nn_takes_max_per_query(self) -> None:
        best = best_fold_nn_by_query(
            _tsv([("E1", "T1", 0.4), ("E1", "T2", 0.7), ("E2", "T1", 0.55)])
        )
        self.assertAlmostEqual(best["E1"], 0.7)
        self.assertAlmostEqual(best["E2"], 0.55)

    def test_generalizes_when_external_tracks_oos_below_inscope(self) -> None:
        # external median ~0.57 ~ OOS median 0.57, both << inscope 0.75
        external = {f"E{i}": v for i, v in enumerate([0.50, 0.57, 0.60, 0.55, 0.58])}
        readout = build_external_offmcsa_fold_abstention_readout(
            external_best_fold_nn=external,
            mcsa_fold_readout=_mcsa_readout(
                inscope=[0.72, 0.75, 0.78, 0.74, 0.80],
                oos=[0.52, 0.57, 0.60, 0.55, 0.58],
            ),
        )
        self.assertEqual(
            readout["status"], "fold_nn_abstention_signal_generalizes_off_mcsa"
        )
        test = readout["generalization_test"]
        self.assertTrue(test["external_tracks_mcsa_oos"])
        self.assertTrue(test["external_below_mcsa_inscope"])
        self.assertTrue(test["abstention_signal_generalizes_off_mcsa"])

    def test_does_not_generalize_when_external_looks_like_inscope(self) -> None:
        # external median high (~0.75), like in-scope -> no abstention separation
        external = {f"E{i}": v for i, v in enumerate([0.72, 0.75, 0.78, 0.74, 0.80])}
        readout = build_external_offmcsa_fold_abstention_readout(
            external_best_fold_nn=external,
            mcsa_fold_readout=_mcsa_readout(
                inscope=[0.72, 0.75, 0.78, 0.74, 0.80],
                oos=[0.52, 0.57, 0.60, 0.55, 0.58],
            ),
        )
        self.assertEqual(
            readout["status"],
            "fold_nn_abstention_signal_does_not_generalize_off_mcsa",
        )
        self.assertFalse(
            readout["generalization_test"]["abstention_signal_generalizes_off_mcsa"]
        )

    def test_frontier_reports_external_and_inscope_tradeoff(self) -> None:
        external = {f"E{i}": v for i, v in enumerate([0.50, 0.57, 0.72])}
        readout = build_external_offmcsa_fold_abstention_readout(
            external_best_fold_nn=external,
            mcsa_fold_readout=_mcsa_readout(
                inscope=[0.72, 0.75, 0.78], oos=[0.52, 0.57, 0.60]
            ),
            fold_threshold_grid=(0.60, 0.70),
        )
        frontier = {p["fold_threshold"]: p for p in readout["abstention_recovery_frontier"]}
        self.assertEqual(frontier[0.70]["external_negatives_not_abstained"], 1)
        self.assertEqual(frontier[0.70]["mcsa_inscope_retained"], 3)

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tsv = root / "ext.tsv"
            mcsa = root / "mcsa.json"
            out = root / "readout.json"
            report = root / "readout.md"
            tsv.write_text(
                _tsv([("E1", "T1", 0.55), ("E2", "T1", 0.58)]), encoding="utf-8"
            )
            mcsa.write_text(
                json.dumps(_mcsa_readout(inscope=[0.74, 0.78], oos=[0.55, 0.58])),
                encoding="utf-8",
            )
            readout = write_external_offmcsa_fold_abstention_readout(
                external_tsv_path=tsv,
                mcsa_fold_readout_path=mcsa,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], readout["artifact_id"]
            )
            self.assertIn("Abstention / Recovery Frontier", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", readout)


if __name__ == "__main__":
    unittest.main()
