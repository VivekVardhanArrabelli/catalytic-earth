from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_validate_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "catalytic_earth.cli", "validate"],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src")},
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Validated", result.stdout)

    def test_artifact_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "source_ledger.json"
            demo = Path(tmpdir) / "mechanism_demo.json"
            score_margins = Path(tmpdir) / "score_margins.json"
            hard_negatives = Path(tmpdir) / "hard_negatives.json"
            in_scope_failures = Path(tmpdir) / "in_scope_failures.json"
            cofactor_coverage = Path(tmpdir) / "cofactor_coverage.json"
            cofactor_policy = Path(tmpdir) / "cofactor_policy.json"
            seed_family_performance = Path(tmpdir) / "seed_family_performance.json"
            label_candidates = Path(tmpdir) / "label_candidates.json"
            mapping_issues = Path(tmpdir) / "mapping_issues.json"
            calibration = Path(tmpdir) / "calibration.json"
            slice_summary = Path(tmpdir) / "slice_summary.json"
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "build-ledger", "--out", str(ledger)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "fingerprint-demo", "--out", str(demo)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-geometry-score-margins",
                    "--out",
                    str(score_margins),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-seed-family-performance",
                    "--out",
                    str(seed_family_performance),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-cofactor-policy",
                    "--out",
                    str(cofactor_policy),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-cofactor-coverage",
                    "--out",
                    str(cofactor_coverage),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-hard-negative-controls",
                    "--out",
                    str(hard_negatives),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-in-scope-failures",
                    "--out",
                    str(in_scope_failures),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-label-expansion-candidates",
                    "--out",
                    str(label_candidates),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-structure-mapping-issues",
                    "--out",
                    str(mapping_issues),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-geometry-slices",
                    "--artifact-dir",
                    "artifacts",
                    "--out",
                    str(slice_summary),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "calibrate-abstention",
                    "--out",
                    str(calibration),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(ledger.exists())
            self.assertTrue(demo.exists())
            self.assertIn("score_separation_gap", json.loads(score_margins.read_text())["metadata"])
            self.assertIn("hard_negative_count", json.loads(hard_negatives.read_text())["metadata"])
            self.assertIn(
                "target_fingerprint_counts",
                json.loads(in_scope_failures.read_text())["metadata"],
            )
            self.assertIn(
                "coverage_status_counts",
                json.loads(cofactor_coverage.read_text())["metadata"],
            )
            self.assertIn(
                "recommendation",
                json.loads(cofactor_policy.read_text())["metadata"],
            )
            self.assertIn(
                "in_scope_family_count",
                json.loads(seed_family_performance.read_text())["metadata"],
            )
            self.assertIn(
                "ready_for_label_review_count",
                json.loads(label_candidates.read_text())["metadata"],
            )
            self.assertIn("status_counts", json.loads(mapping_issues.read_text())["metadata"])
            self.assertEqual(json.loads(slice_summary.read_text())["metadata"]["largest_slice"], "225")
            self.assertGreater(json.loads(calibration.read_text())["metadata"]["threshold_count"], 21)


if __name__ == "__main__":
    unittest.main()
