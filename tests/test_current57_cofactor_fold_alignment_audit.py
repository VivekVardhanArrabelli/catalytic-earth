from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.current57_cofactor_fold_alignment_audit import (
    build_current57_cofactor_fold_alignment_audit,
    write_current57_cofactor_fold_alignment_audit,
)


def _inscope(entry_id: str, *, true: str, called: str, score: float) -> dict:
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": true,
        "row_class": "in_scope",
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _oos(entry_id: str, *, called: str, score: float) -> dict:
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": None,
        "row_class": "out_of_scope",
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _current(inscope: list[dict], oos: list[dict]) -> dict:
    return {
        "artifact_id": "current57",
        "row_details_by_split": {
            "calibration": {"inscope_rows": inscope, "oos_rows": oos},
            "train": {"inscope_rows": inscope, "oos_rows": oos},
        },
    }


def _fold_inscope(rows: list[dict]) -> dict:
    return {
        "artifact_id": "fold_inscope",
        "status": "complete",
        "primary_channel_readout": {
            "selected_at_90pct_calibration_in_scope_retention": {
                "threshold": 0.44155
            }
        },
        "calibration_row_scores": rows,
    }


def _fold_oos(rows: list[dict]) -> dict:
    return {
        "artifact_id": "fold_oos",
        "status": "complete",
        "calibration_oos_negative_row_scores": rows,
    }


def _fold_row(entry_id: str, score: float) -> dict:
    return {
        "entry_id": entry_id,
        "channel_scores": {"combined_mean_geometry_fold": score},
    }


class Current57CofactorFoldAlignmentAuditTests(unittest.TestCase):
    def test_audit_fail_closes_when_cached_fold_rows_do_not_cover_current57_surface(
        self,
    ) -> None:
        audit = build_current57_cofactor_fold_alignment_audit(
            current57_operating_point=_current(
                [
                    _inscope(
                        "in1",
                        true="metal_dependent_hydrolase",
                        called="metallo_amidohydrolase_deaminase",
                        score=0.9,
                    ),
                    _inscope(
                        "in2",
                        true="ser_his_acid_hydrolase",
                        called="ser_his_acid_hydrolase",
                        score=0.8,
                    ),
                ],
                [
                    _oos("oo1", called="metallo_amidohydrolase_deaminase", score=0.9),
                    _oos("oo2", called="metallophosphomonoesterase", score=0.8),
                ],
            ),
            fold_inscope_contract=_fold_inscope([_fold_row("in1", 0.6)]),
            fold_oos_contract=_fold_oos([]),
        )

        self.assertEqual(
            audit["status"],
            "blocked_cached_fold_surface_not_row_aligned_with_current57_cofactor_surface",
        )
        self.assertFalse(audit["alignment_gate"]["passed"])
        self.assertEqual(
            audit["calibration_overlap"]["inscope"]["overlap_fraction"], 0.5
        )
        self.assertEqual(audit["calibration_overlap"]["oos"]["overlap_fraction"], 0.0)
        self.assertFalse(audit["guardrails"]["cached_surface_fusion_authorized"])
        self.assertFalse(audit["overlap_only_fixed_gate_probe"]["interpretable"])

    def test_audit_passes_only_when_calibration_inscope_and_oos_are_aligned(
        self,
    ) -> None:
        audit = build_current57_cofactor_fold_alignment_audit(
            current57_operating_point=_current(
                [
                    _inscope(
                        "in1",
                        true="metal_dependent_hydrolase",
                        called="metallo_amidohydrolase_deaminase",
                        score=0.9,
                    ),
                    _inscope(
                        "in2",
                        true="ser_his_acid_hydrolase",
                        called="ser_his_acid_hydrolase",
                        score=0.8,
                    ),
                ],
                [
                    _oos("oo1", called="metallo_amidohydrolase_deaminase", score=0.9),
                    _oos("oo2", called="metallophosphomonoesterase", score=0.8),
                ],
            ),
            fold_inscope_contract=_fold_inscope(
                [_fold_row("in1", 0.6), _fold_row("in2", 0.3)]
            ),
            fold_oos_contract=_fold_oos(
                [_fold_row("oo1", 0.2), _fold_row("oo2", 0.7)]
            ),
        )

        self.assertEqual(
            audit["status"], "current57_cofactor_fold_cached_surface_aligned_ready"
        )
        self.assertTrue(audit["alignment_gate"]["passed"])
        self.assertTrue(audit["guardrails"]["cached_surface_fusion_authorized"])
        probe = audit["overlap_only_fixed_gate_probe"]
        self.assertTrue(probe["interpretable"])
        self.assertEqual(probe["compatible_inscope_correct_retained_on_overlap"], 1)
        self.assertEqual(probe["oos_false_positives_retained_on_overlap"], 1)

    def test_writer_emits_report_and_source_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = root / "current.json"
            inscope = root / "fold_inscope.json"
            oos = root / "fold_oos.json"
            out = root / "out.json"
            report = root / "report.md"
            current.write_text(
                json.dumps(_current([_inscope("in1", true="x", called="x", score=0.8)], [])),
                encoding="utf-8",
            )
            inscope.write_text(json.dumps(_fold_inscope([])), encoding="utf-8")
            oos.write_text(json.dumps(_fold_oos([])), encoding="utf-8")

            audit = write_current57_cofactor_fold_alignment_audit(
                current57_operating_point_path=current,
                fold_inscope_contract_path=inscope,
                fold_oos_contract_path=oos,
                out_path=out,
                report_path=report,
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], audit["artifact_id"]
            )
            self.assertIn("No heldout rows", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", audit)


if __name__ == "__main__":
    unittest.main()
