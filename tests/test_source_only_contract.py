from __future__ import annotations

import importlib
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run_source_only_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        check=True,
        capture_output=True,
        text=True,
    )


class SourceOnlyContractTests(unittest.TestCase):
    def test_source_tree_compiles(self) -> None:
        result = _run_source_only_command("-m", "compileall", "src")
        self.assertEqual(result.returncode, 0)

    def test_transfer_scope_imports_from_source_checkout(self) -> None:
        result = _run_source_only_command(
            "-c",
            "import catalytic_earth.transfer_scope",
        )
        self.assertEqual(result.returncode, 0)

    def test_cli_help_and_validate_work_from_source_checkout(self) -> None:
        help_result = _run_source_only_command("-m", "catalytic_earth.cli", "--help")
        validate_result = _run_source_only_command("-m", "catalytic_earth.cli", "validate")
        self.assertIn("validate", help_result.stdout)
        self.assertIn("Validated 682 curated mechanism labels", validate_result.stdout)

    def test_transfer_scope_public_contract_symbols_are_importable(self) -> None:
        module = importlib.import_module("catalytic_earth.transfer_scope")
        for symbol in (
            "check_external_source_transfer_gates",
            "validate_external_transfer_artifact_path_lineage",
            "build_external_hard_negative_next_candidate_factory_import_gate",
            "build_external_hard_negative_later_single_import_cycle_gate",
        ):
            self.assertTrue(callable(getattr(module, symbol)))


if __name__ == "__main__":
    unittest.main()
