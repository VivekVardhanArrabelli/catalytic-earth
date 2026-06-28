from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.fold_nn_mechanism_recovery_readout import (
    atlas_fingerprints_from_manifest,
    best_nn_by_query,
    build_fold_nn_mechanism_recovery_readout,
    positives_from_manifest_group,
    write_fold_nn_mechanism_recovery_readout,
)


def _manifest() -> dict:
    return {
        "artifact_id": "manifest",
        "rows": {
            "calibration_queries": [
                {
                    "entry_id": "in1",
                    "accession": "Q1",
                    "row_class": "inscope",
                    "true_fingerprint_id": "fpA",
                },
                {
                    "entry_id": "in2",
                    "accession": "Q2",
                    "row_class": "inscope",
                    "true_fingerprint_id": "fpB",
                },
                {
                    "entry_id": "oos1",
                    "accession": "Q3",
                    "row_class": "oos",
                    "true_fingerprint_id": None,
                },
            ],
            "train_in_scope_targets": [
                {"entry_id": "t1", "accession": "T1", "true_fingerprint_id": "fpA"},
                {"entry_id": "t2", "accession": "T2", "true_fingerprint_id": "fpB"},
            ],
        },
    }


def _tsv() -> str:
    # Q1 best -> T1 (fpA) at 0.8 (recovered); Q2 best -> T1 (fpA) at 0.7 (NOT recovered)
    return "\n".join(
        [
            "afdb_Q1_v6\tafdb_T1_v6\t0.8\t0.8\t0.80\t0.9\t90",
            "afdb_Q1_v6\tafdb_T2_v6\t0.6\t0.6\t0.60\t0.5\t60",
            "afdb_Q2_v6\tafdb_T1_v6\t0.7\t0.7\t0.70\t0.6\t70",
            "afdb_Q2_v6\tafdb_T2_v6\t0.5\t0.5\t0.50\t0.3\t50",
        ]
    )


class FoldNnMechanismRecoveryReadoutTests(unittest.TestCase):
    def test_helpers_extract_maps_and_positives(self) -> None:
        manifest = _manifest()
        self.assertEqual(
            atlas_fingerprints_from_manifest(manifest), {"T1": "fpA", "T2": "fpB"}
        )
        positives = positives_from_manifest_group(
            manifest, "calibration_queries", "inscope"
        )
        self.assertEqual([p["accession"] for p in positives], ["Q1", "Q2"])
        best = best_nn_by_query(_tsv())
        self.assertEqual(best["Q1"]["target_accession"], "T1")
        self.assertAlmostEqual(best["Q1"]["alntmscore"], 0.80)

    def test_recovery_and_curve(self) -> None:
        manifest = _manifest()
        readout = build_fold_nn_mechanism_recovery_readout(
            positives=positives_from_manifest_group(
                manifest, "calibration_queries", "inscope"
            ),
            best_nn=best_nn_by_query(_tsv()),
            atlas_fingerprints=atlas_fingerprints_from_manifest(manifest),
            surface_label="unit",
        )
        # Q1 recovered (T1 fpA == fpA); Q2 not (T1 fpA != fpB).
        self.assertEqual(readout["recovery"]["fold_nn_recovered"], 1)
        self.assertEqual(readout["recovery"]["fold_nn_scored"], 2)
        self.assertEqual(readout["recovery"]["recovery_rate_no_abstention"], 0.5)
        # at fold >= 0.75 only Q1 retained (0.80) and it is recovered -> precision 1.0
        curve = {p["fold_threshold"]: p for p in readout["recovery_abstention_curve"]}
        self.assertEqual(curve[0.7]["retained"], 2)
        self.assertEqual(curve[0.74]["retained"], 1)
        self.assertEqual(curve[0.74]["retained_recovered"], 1)
        self.assertEqual(curve[0.74]["precision_on_retained"], 1.0)

    def test_unscored_positive_is_counted_in_coverage(self) -> None:
        manifest = _manifest()
        positives = positives_from_manifest_group(
            manifest, "calibration_queries", "inscope"
        ) + [{"entry_id": "in3", "accession": "Q9", "true_fingerprint_id": "fpA"}]
        readout = build_fold_nn_mechanism_recovery_readout(
            positives=positives,
            best_nn=best_nn_by_query(_tsv()),
            atlas_fingerprints=atlas_fingerprints_from_manifest(manifest),
            surface_label="unit",
        )
        self.assertEqual(readout["coverage"]["positives_total"], 3)
        self.assertEqual(readout["coverage"]["positives_with_fold_hit"], 2)

    def test_writer_baseline_from_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "manifest.json"
            tsv_path = root / "result.tsv"
            out = root / "readout.json"
            report = root / "readout.md"
            manifest_path.write_text(json.dumps(_manifest()), encoding="utf-8")
            tsv_path.write_text(_tsv(), encoding="utf-8")
            readout = write_fold_nn_mechanism_recovery_readout(
                atlas_manifest_path=manifest_path,
                foldseek_tsv_path=tsv_path,
                out_path=out,
                report_path=report,
                surface_label="baseline",
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(readout["recovery"]["fold_nn_scored"], 2)
            self.assertIn("Recovery / Abstention Curve", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", readout)


if __name__ == "__main__":
    unittest.main()
