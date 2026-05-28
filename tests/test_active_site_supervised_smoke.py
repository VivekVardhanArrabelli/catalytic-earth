from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "research_lanes"
    / "active_site_supervised_smoke"
    / "run_active_site_supervised_smoke.py"
)
SPEC = importlib.util.spec_from_file_location("active_site_supervised_smoke", MODULE_PATH)
assert SPEC is not None
smoke = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(smoke)


class ActiveSiteSupervisedSmokeTests(unittest.TestCase):
    def test_toy_smoke_writes_review_only_predictions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cache = root / "cache.jsonl"
            feasibility = root / "feasibility.json"
            audit = root / "audit.json"
            diagnostic = root / "diagnostic.jsonl"
            out = root / "predictions.jsonl"
            summary = root / "summary.json"
            report = root / "report.md"
            _write_jsonl(cache, [_row("train_a", "A", 0.0), _row("train_oos", None, 5.0), _row("cal_a", "A", 0.2), _row("cal_oos", None, 5.2)])
            _write_jsonl(diagnostic, [_row("diag_a", "A", 0.1)])
            feasibility.write_text(json.dumps(_feasibility()), encoding="utf-8")
            audit.write_text(json.dumps(_audit()), encoding="utf-8")

            exit_code = smoke.main(
                [
                    "--train-cal-cache",
                    str(cache),
                    "--train-cal-feasibility",
                    str(feasibility),
                    "--diagnostic-cache",
                    str(diagnostic),
                    "--leakage-audit",
                    str(audit),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--report-out",
                    str(report),
                    "--no-production-claims",
                ]
            )

            self.assertEqual(exit_code, 0)
            summary_payload = json.loads(summary.read_text(encoding="utf-8"))
            self.assertTrue(summary_payload["review_only"])
            self.assertTrue(summary_payload["no_production_claims"])
            self.assertEqual(summary_payload["train_count"], 2)
            self.assertEqual(summary_payload["calibration_count"], 2)
            predictions = [
                json.loads(line)
                for line in out.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(predictions), 5)
            self.assertIn("diagnostic_eval_only", {row["split"] for row in predictions})

    def test_forbidden_predictive_key_is_rejected(self) -> None:
        row = _row("bad", "A", 1.0)
        row["predictive_features"]["mechanism_text"] = "leaky"

        with self.assertRaisesRegex(ValueError, "forbidden predictive keys"):
            smoke.assert_no_forbidden_predictive_keys([row])

    def test_leakage_audit_must_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cache = root / "cache.jsonl"
            feasibility = root / "feasibility.json"
            audit = root / "audit.json"
            _write_jsonl(cache, [_row("train_a", "A", 0.0), _row("cal_a", "A", 0.2)])
            feasibility.write_text(json.dumps(_feasibility()), encoding="utf-8")
            audit.write_text(
                json.dumps({"training_preflight_status": "block", "summary": {"blocker_count": 1}}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "leakage audit did not pass"):
                smoke.run_smoke(
                    train_cal_cache_path=cache,
                    train_cal_feasibility_path=feasibility,
                    diagnostic_cache_paths=[],
                    leakage_audit_path=audit,
                    seed=20260528,
                )


def _row(entry_id: str, fingerprint: str | None, x_value: float) -> dict:
    return {
        "metadata": {
            "entry_id": entry_id,
            "current_fingerprint_id": fingerprint,
            "source_group": "toy",
            "split_assignment": "toy",
        },
        "predictive_features": {
            "active_site_residue_count": 2,
            "distance_summary": {"mean": x_value},
            "cofactor_family_presence": ["metal_ion"] if fingerprint == "A" else [],
            "nodes": [
                {"node_index": 0, "residue_type": "HIS", "roles": ["metal ligand"], "atom_count_clipped": 8},
                {"node_index": 1, "residue_type": "GLU", "roles": ["acid"], "atom_count_clipped": 9},
            ],
        },
    }


def _feasibility() -> dict:
    rows = []
    for entry_id, split, target in [
        ("train_a", "train", "A"),
        ("train_oos", "train", "None"),
        ("cal_a", "calibration", "A"),
        ("cal_oos", "calibration", "None"),
    ]:
        rows.append(
            {
                "entry_id": entry_id,
                "train_cal_use_group": "train_cal_eligible_parent_v1_or_oos",
                "proposed_train_cal_split": split,
                "target_group_metadata_only": target,
            }
        )
    return {"rows": rows}


def _audit() -> dict:
    return {
        "training_preflight_status": "pass",
        "summary": {"blocker_count": 0},
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
