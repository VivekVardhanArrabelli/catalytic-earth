from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas_selection import load_atlas3_selection
from catalytic_earth.atlas_sources import validate_atlas3_source_manifest


ROOT = Path(__file__).resolve().parents[2]
SELECTION_PATH = ROOT / "data/atlas/atlas3_selection.json"
MANIFEST_PATH = ROOT / "data/atlas/atlas3/source_manifest.json"


class AtlasSourceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selection = load_atlas3_selection(SELECTION_PATH)
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_manifest_covers_the_frozen_bounded_source_set(self) -> None:
        summary = validate_atlas3_source_manifest(
            self.manifest,
            repo_root=ROOT,
            selection=self.selection,
        )
        self.assertEqual(summary["handles"], 18)
        self.assertEqual(summary["bundled_snapshots"], 13)
        self.assertEqual(summary["reference_only_handles"], 5)
        self.assertEqual(summary["snapshot_bytes"], 1_223_884)

    def test_article_content_remains_reference_only(self) -> None:
        literature = [
            record
            for record in self.manifest["records"]
            if record["source_id"] in {"DOI", "PMCID"}
        ]
        self.assertEqual(len(literature), 5)
        self.assertTrue(all(record["snapshot_path"] is None for record in literature))
        self.assertTrue(all(record["snapshot_sha256"] is None for record in literature))

    def test_snapshot_hash_tampering_fails_closed(self) -> None:
        changed = copy.deepcopy(self.manifest)
        bundled = next(
            record for record in changed["records"] if record["snapshot_sha256"] is not None
        )
        bundled["snapshot_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "snapshot_sha256 differs"):
            validate_atlas3_source_manifest(
                changed,
                repo_root=ROOT,
                selection=self.selection,
            )


if __name__ == "__main__":
    unittest.main()
