from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.fingerprints import (
    build_mechanism_demo,
    completeness_score,
    load_fingerprints,
)


class FingerprintRegistryTests(unittest.TestCase):
    def test_load_fingerprints(self) -> None:
        fingerprints = load_fingerprints()
        self.assertGreaterEqual(len(fingerprints), 5)
        self.assertEqual(len({fingerprint.id for fingerprint in fingerprints}), len(fingerprints))

    def test_completeness(self) -> None:
        for fingerprint in load_fingerprints():
            self.assertEqual(completeness_score(fingerprint), 1.0)

    def test_demo_indexes_operations(self) -> None:
        demo = build_mechanism_demo(load_fingerprints())
        self.assertIn("nucleophilic acyl substitution", demo["chemical_operation_index"])
        self.assertIn("flavin-mediated redox transfer", demo["chemical_operation_index"])
        self.assertIn("FAD", demo["cofactor_index"])
        self.assertIn("adenosylcobalamin", demo["cofactor_index"])


if __name__ == "__main__":
    unittest.main()
