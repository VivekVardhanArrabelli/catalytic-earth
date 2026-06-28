from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.router_reconciliation_diagnostic import (
    build_router_reconciliation_diagnostic,
    documented_compatibility_from_ontology,
    write_router_reconciliation_diagnostic,
)


def _row(true_fp, called, score):
    return {
        "true_fingerprint_id": true_fp,
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _current57(rows):
    return {"row_details_by_split": {"calibration": {"inscope_rows": rows}}}


def _june9(correct, total):
    return {
        "operating_points_by_split": {
            "calibration": {
                "fused_frozen_threshold": {
                    "inscope_correct": correct,
                    "inscope_total": total,
                    "oos_false_positives": 9,
                    "oos_total": 26,
                }
            }
        }
    }


_COMPAT = {"metal_dependent_hydrolase": ["metal_dependent_hydrolase", "metallopeptidase"]}


class RouterReconciliationDiagnosticTests(unittest.TestCase):
    def test_classifies_exact_compatible_and_misroute(self) -> None:
        rows = [
            _row("fpA", "fpA", 0.8),  # exact
            _row("metal_dependent_hydrolase", "metallopeptidase", 0.8),  # documented split
            _row("flavin", "metallopeptidase", 0.8),  # genuine misroute
            _row("fpB", "fpC", 0.1),  # below threshold
        ]
        diag = build_router_reconciliation_diagnostic(
            current57_operating_point=_current57(rows),
            june9_trusted=_june9(3, 4),
            compatibility_map=_COMPAT,
            threshold=0.4115,
        )
        cc = diag["calibration_classification"]
        self.assertEqual(cc["exact_correct"], 1)
        self.assertEqual(cc["documented_compatible_correct"], 1)
        self.assertEqual(cc["incompatible_misroute"], 1)
        self.assertEqual(cc["below_threshold_abstain"], 1)

    def test_not_reconcilable_when_misroutes_create_gap(self) -> None:
        rows = [
            _row("fpA", "fpA", 0.8),
            _row("flavin", "metallopeptidase", 0.8),  # genuine misroute
        ]
        diag = build_router_reconciliation_diagnostic(
            current57_operating_point=_current57(rows),
            june9_trusted=_june9(2, 2),  # June 9 got both right
            compatibility_map=_COMPAT,
        )
        self.assertEqual(
            diag["status"],
            "fine_router_drift_includes_genuine_misrouting_not_just_relabeling",
        )
        self.assertFalse(
            diag["recovery_comparison"]["reconcilable_by_documented_relabeling"]
        )
        self.assertEqual(diag["recovery_comparison"]["recovery_gap_beyond_relabeling"], 1)
        self.assertEqual(
            diag["drift_mechanism"]["nonmetal_enzymes_misrouted_into_metal_subclasses"], 1
        )

    def test_reconcilable_when_relabeling_meets_bar(self) -> None:
        rows = [
            _row("metal_dependent_hydrolase", "metallopeptidase", 0.8),
            _row("fpA", "fpA", 0.8),
        ]
        diag = build_router_reconciliation_diagnostic(
            current57_operating_point=_current57(rows),
            june9_trusted=_june9(2, 2),
            compatibility_map=_COMPAT,
        )
        self.assertEqual(
            diag["status"], "fine_router_reconcilable_by_documented_relabeling"
        )
        self.assertTrue(
            diag["recovery_comparison"]["reconcilable_by_documented_relabeling"]
        )

    def test_compatibility_map_from_ontology_includes_metal_umbrella(self) -> None:
        ontology = {
            "families": [
                {
                    "id": "hydrolysis",
                    "v2_split_note": "metal_dependent_hydrolase is the coarse v1 umbrella",
                    "fingerprint_ids": [
                        "metal_dependent_hydrolase",
                        "metallopeptidase",
                    ],
                }
            ]
        }
        m = documented_compatibility_from_ontology(ontology)
        self.assertIn("metal_dependent_hydrolase", m)
        self.assertIn("metallopeptidase", m["metal_dependent_hydrolase"])

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cur = root / "cur.json"
            j9 = root / "j9.json"
            ont = root / "ont.json"
            cur.write_text(
                json.dumps(_current57([_row("fpA", "fpA", 0.8)])), encoding="utf-8"
            )
            j9.write_text(json.dumps(_june9(1, 1)), encoding="utf-8")
            ont.write_text(json.dumps({"families": []}), encoding="utf-8")
            out = root / "diag.json"
            report = root / "diag.md"
            diag = write_router_reconciliation_diagnostic(
                current57_operating_point_path=cur,
                june9_trusted_path=j9,
                ontology_path=ont,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertIn("Fork", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", diag)


if __name__ == "__main__":
    unittest.main()
