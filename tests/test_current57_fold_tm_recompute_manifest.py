from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.current57_fold_tm_recompute_manifest import (
    build_current57_fold_tm_recompute_manifest,
    write_current57_fold_tm_recompute_manifest,
)


def _row(entry_id: str, *, split: str, row_class: str, fp: str | None = "fp") -> dict:
    return {
        "entry_id": entry_id,
        "embedding_split": split,
        "row_class": row_class,
        "true_fingerprint_id": fp if row_class == "in_scope" else None,
        "fused": {"top1_fingerprint_id": fp or "called", "top1_score": 0.7},
    }


def _current() -> dict:
    return {
        "artifact_id": "current57",
        "row_details_by_split": {
            "calibration": {
                "inscope_rows": [_row("cal_in", split="calibration", row_class="in_scope")],
                "oos_rows": [
                    _row("cal_oos", split="calibration", row_class="oos", fp=None)
                ],
            },
            "train": {
                "inscope_rows": [_row("train_in", split="train", row_class="in_scope")],
                "oos_rows": [_row("train_oos", split="train", row_class="oos", fp=None)],
            },
        },
    }


def _labels() -> dict:
    return {
        "artifact_id": "labels",
        "rows": [
            {
                "entry_id": "cal_in",
                "label_type": "primary",
                "sequence_id": "P00001",
                "real_sequence_accessions": ["P00001"],
            },
            {
                "entry_id": "cal_oos",
                "label_type": "out_of_scope",
                "sequence_id": "P00002",
                "real_sequence_accessions": ["P00002"],
            },
            {
                "entry_id": "train_in",
                "label_type": "primary",
                "sequence_id": "P00003",
                "real_sequence_accessions": ["P00003"],
            },
            {
                "entry_id": "train_oos",
                "label_type": "out_of_scope",
                "sequence_id": "P00004",
                "real_sequence_accessions": ["P00004"],
            },
        ],
    }


def _stage(root: Path, *accessions: str) -> None:
    safe = root / "confounded_proxy_train_cal_tranche_queries"
    safe.mkdir(parents=True)
    (root / "atlas_in_distribution").mkdir(parents=True)
    for accession in accessions:
        (safe / f"afdb_{accession}_v6.cif").write_text("data\n", encoding="utf-8")


class Current57FoldTmRecomputeManifestTests(unittest.TestCase):
    def test_manifest_is_ready_when_calibration_queries_and_train_targets_have_cifs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _stage(root, "P00001", "P00002", "P00003", "P00004")
            manifest = build_current57_fold_tm_recompute_manifest(
                current57_operating_point=_current(),
                label_manifest=_labels(),
                coordinate_root=root,
            )

        self.assertEqual(
            manifest["status"],
            "current57_fold_tm_recompute_input_manifest_ready_foldseek_missing",
        )
        self.assertEqual(
            manifest["coverage"]["calibration_queries"][
                "staged_train_cal_safe_cif_found"
            ],
            2,
        )
        self.assertEqual(
            manifest["coverage"]["train_in_scope_targets"][
                "staged_train_cal_safe_cif_found"
            ],
            1,
        )
        self.assertIn("foldseek easy-search", manifest["foldseek_command"])
        self.assertFalse(manifest["guardrails"]["heldout_rows_scored"])

    def test_manifest_blocks_when_required_cif_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _stage(root, "P00001", "P00003")
            manifest = build_current57_fold_tm_recompute_manifest(
                current57_operating_point=_current(),
                label_manifest=_labels(),
                coordinate_root=root,
            )

        self.assertEqual(
            manifest["status"],
            "blocked_current57_fold_tm_recompute_input_manifest_missing_inputs",
        )
        self.assertEqual(
            manifest["coverage"]["calibration_queries"]["missing_train_cal_safe_cif"],
            1,
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coord = root / "coords"
            _stage(coord, "P00001", "P00002", "P00003", "P00004")
            current = root / "current.json"
            labels = root / "labels.json"
            out = root / "manifest.json"
            report = root / "manifest.md"
            current.write_text(json.dumps(_current()), encoding="utf-8")
            labels.write_text(json.dumps(_labels()), encoding="utf-8")

            manifest = write_current57_fold_tm_recompute_manifest(
                current57_operating_point_path=current,
                label_manifest_path=labels,
                coordinate_root=coord,
                out_path=out,
                report_path=report,
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], manifest["artifact_id"]
            )
            self.assertIn("Foldseek Command", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", manifest)


if __name__ == "__main__":
    unittest.main()
