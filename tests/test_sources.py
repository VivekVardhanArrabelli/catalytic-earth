from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.sources import build_source_ledger, load_sources


class SourceRegistryTests(unittest.TestCase):
    def test_load_sources(self) -> None:
        sources = load_sources()
        self.assertGreaterEqual(len(sources), 10)
        self.assertEqual(len({source.id for source in sources}), len(sources))

    def test_build_source_ledger(self) -> None:
        ledger = build_source_ledger(load_sources())
        self.assertIn("reaction_knowledgebase", ledger["by_category"])
        self.assertIn("mechanism_active_site", ledger["by_category"])
        self.assertIn("protein_sequences", ledger["by_role"])


if __name__ == "__main__":
    unittest.main()
