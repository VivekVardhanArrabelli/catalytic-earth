from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "run_test_tier", ROOT / "scripts/run_test_tier.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestTierTests(unittest.TestCase):
    def test_all_tests_have_exact_tier(self) -> None:
        grouped = MODULE.classify_tests()
        paths = [path for tier_paths in grouped.values() for path in tier_paths]

        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("tests/core/test_core_cli.py", grouped["core/unit"])
        self.assertIn("tests/test_geometry_artifact_regression.py", grouped["artifact-regression"])
        self.assertTrue(all(grouped.values()))


if __name__ == "__main__":
    unittest.main()
