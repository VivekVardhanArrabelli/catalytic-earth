from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.current57_fold_tm_recompute_readout import (
    build_current57_fold_tm_recompute_readout,
    parse_foldseek_rows,
    write_current57_fold_tm_recompute_readout,
)


def _manifest() -> dict:
    return {
        "artifact_id": "manifest",
        "schema_version": "current57_fold_tm_recompute_input_manifest.v1",
        "status": "current57_fold_tm_recompute_input_manifest_ready_foldseek_missing",
        "foldseek_command": "foldseek easy-search q t out tmp",
        "rows": {
            "calibration_queries": [
                {
                    "entry_id": "cal_in_1",
                    "accession": "P00001",
                    "row_class": "inscope",
                    "role": "calibration_query_in_scope_primary",
                    "true_fingerprint_id": "fpA",
                    "current57_fused_top1_fingerprint_id": "fpA",
                    "current57_fused_top1_score": 0.7,
                },
                {
                    "entry_id": "cal_in_2",
                    "accession": "P00002",
                    "row_class": "inscope",
                    "role": "calibration_query_in_scope_primary",
                    "true_fingerprint_id": "fpB",
                    "current57_fused_top1_fingerprint_id": "fpA",
                    "current57_fused_top1_score": 0.5,
                },
                {
                    "entry_id": "cal_oos_1",
                    "accession": "P00003",
                    "row_class": "oos",
                    "role": "calibration_query_oos_negative",
                    "true_fingerprint_id": None,
                    "current57_fused_top1_fingerprint_id": "fpA",
                    "current57_fused_top1_score": 0.45,
                },
            ],
            "train_in_scope_targets": [
                {"entry_id": "tr_1", "accession": "P10001", "true_fingerprint_id": "fpA"},
                {"entry_id": "tr_2", "accession": "P10002", "true_fingerprint_id": "fpB"},
            ],
        },
    }


def _foldseek_tsv() -> str:
    # cal_in_1 best to fpA target (match); cal_in_2 best to fpA target (mismatch);
    # cal_oos_1 has only a low-TM hit.
    return "\n".join(
        [
            "afdb_P00001_v6\tafdb_P10001_v6\t0.80\t0.80\t0.85\t0.9\t90",
            "afdb_P00001_v6\tafdb_P10002_v6\t0.60\t0.60\t0.65\t0.5\t60",
            "afdb_P00002_v6\tafdb_P10001_v6\t0.70\t0.70\t0.75\t0.6\t70",
            "afdb_P00002_v6\tafdb_P10002_v6\t0.50\t0.50\t0.55\t0.3\t50",
            "afdb_P00003_v6\tafdb_P10001_v6\t0.40\t0.40\t0.45\t0.2\t40",
        ]
    )


class Current57FoldTmRecomputeReadoutTests(unittest.TestCase):
    def test_parse_foldseek_rows_extracts_accessions_and_scores(self) -> None:
        rows = parse_foldseek_rows(_foldseek_tsv())
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["query_accession"], "P00001")
        self.assertEqual(rows[0]["target_accession"], "P10001")
        self.assertAlmostEqual(rows[0]["alntmscore"], 0.85)

    def test_readout_is_row_aligned_with_abstention_separation(self) -> None:
        readout = build_current57_fold_tm_recompute_readout(
            manifest=_manifest(),
            foldseek_rows=parse_foldseek_rows(_foldseek_tsv()),
        )
        self.assertEqual(
            readout["status"], "current57_fold_tm_recompute_readout_row_aligned"
        )
        self.assertEqual(
            readout["coverage"]["calibration_inscope"]["rows_with_fold_score"], 2
        )
        self.assertEqual(
            readout["coverage"]["calibration_oos"]["rows_with_fold_score"], 1
        )
        self.assertTrue(readout["alignment_resolution"]["resolves_alignment_blocker"])
        # in-scope median (0.85, 0.75) -> 0.80 vs OOS 0.45 -> gap >= margin
        self.assertTrue(
            readout["fold_nn_distribution"]["separation"]["abstention_signal_present"]
        )
        self.assertFalse(readout["guardrails"]["heldout_rows_scored"])
        self.assertTrue(readout["guardrails"]["new_foldseek_or_tm_scores_computed"])

    def test_best_hit_picks_highest_alntmscore_and_fingerprint_match(self) -> None:
        readout = build_current57_fold_tm_recompute_readout(
            manifest=_manifest(),
            foldseek_rows=parse_foldseek_rows(_foldseek_tsv()),
        )
        inscope = {row["entry_id"]: row for row in readout["rows"]["calibration_inscope"]}
        # cal_in_1: best target P10001 (fpA) matches true fpA.
        self.assertEqual(inscope["cal_in_1"]["fold_nn_target_accession"], "P10001")
        self.assertTrue(inscope["cal_in_1"]["fold_nn_fingerprint_match"])
        # cal_in_2: best target P10001 (fpA) does NOT match true fpB.
        self.assertFalse(inscope["cal_in_2"]["fold_nn_fingerprint_match"])
        self.assertEqual(
            readout["fold_nn_fingerprint_consistency"][
                "inscope_fold_nn_true_fingerprint_match"
            ],
            1,
        )

    def test_blocks_when_coverage_incomplete(self) -> None:
        # Drop all foldseek hits for the OOS query -> coverage below threshold.
        partial = "\n".join(
            [
                "afdb_P00001_v6\tafdb_P10001_v6\t0.80\t0.80\t0.85\t0.9\t90",
                "afdb_P00002_v6\tafdb_P10001_v6\t0.70\t0.70\t0.75\t0.6\t70",
            ]
        )
        readout = build_current57_fold_tm_recompute_readout(
            manifest=_manifest(),
            foldseek_rows=parse_foldseek_rows(partial),
        )
        self.assertEqual(
            readout["status"],
            "blocked_current57_fold_tm_recompute_readout_incomplete_coverage",
        )
        self.assertFalse(
            readout["alignment_resolution"]["resolves_alignment_blocker"]
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "manifest.json"
            tsv_path = root / "result.tsv"
            out = root / "readout.json"
            report = root / "readout.md"
            manifest_path.write_text(json.dumps(_manifest()), encoding="utf-8")
            tsv_path.write_text(_foldseek_tsv(), encoding="utf-8")

            readout = write_current57_fold_tm_recompute_readout(
                manifest_path=manifest_path,
                foldseek_tsv_path=tsv_path,
                out_path=out,
                report_path=report,
                foldseek_version="testver",
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], readout["artifact_id"]
            )
            self.assertEqual(readout["foldseek_provenance"]["version"], "testver")
            self.assertIn("Fold-NN TM Separation", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", readout)


if __name__ == "__main__":
    unittest.main()
