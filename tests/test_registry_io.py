from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.registry_io import (
    SHARDED_REGISTRY_SCHEMA,
    load_json,
    load_registry,
    write_registry_payload,
)


class RegistryIoTests(unittest.TestCase):
    def test_small_registry_stays_plain_json_list(self) -> None:
        rows = [{"entry_id": "uniprot:A0", "tier": "bronze"}]
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "external_bronze_labels.json"
            result = write_registry_payload(path, rows)

            self.assertEqual(result["format"], "single_json_list")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), rows)
            self.assertEqual(load_registry(path), rows)

    def test_large_registry_writes_manifest_and_loads_in_order(self) -> None:
        rows = [
            {"entry_id": f"uniprot:A{i}", "tier": "bronze", "payload": "x" * 80}
            for i in range(9)
        ]
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "external_bronze_labels.json"
            result = write_registry_payload(
                path,
                rows,
                shard_threshold_bytes=100,
                target_shard_bytes=250,
            )

            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(result["format"], "sharded_registry_manifest")
            self.assertEqual(manifest["schema_version"], SHARDED_REGISTRY_SCHEMA)
            self.assertGreater(manifest["shard_count"], 1)
            self.assertEqual(load_json(path), rows)
            self.assertEqual(load_registry(path), rows)

    def test_shard_hash_mismatch_fails_closed(self) -> None:
        rows = [
            {"entry_id": f"uniprot:B{i}", "tier": "bronze", "payload": "y" * 80}
            for i in range(4)
        ]
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "external_bronze_labels.json"
            write_registry_payload(
                path,
                rows,
                shard_threshold_bytes=100,
                target_shard_bytes=250,
            )
            manifest = json.loads(path.read_text(encoding="utf-8"))
            shard_path = path.parent / manifest["shards"][0]["path"]
            shard_path.write_text("[]\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "sha256 mismatch"):
                load_registry(path)


if __name__ == "__main__":
    unittest.main()
