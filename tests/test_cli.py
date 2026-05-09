from __future__ import annotations

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
            self.assertTrue(ledger.exists())
            self.assertTrue(demo.exists())


if __name__ == "__main__":
    unittest.main()
