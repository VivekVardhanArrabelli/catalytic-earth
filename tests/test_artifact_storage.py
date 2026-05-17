from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.artifact_storage import (
    build_artifact_producer_consumer_manifest,
    build_artifact_storage_inventory,
    check_artifact_admission_guard,
    check_artifact_storage_policy,
    classify_artifact_path,
)

ROOT = Path(__file__).resolve().parents[1]


class ArtifactStorageTests(unittest.TestCase):
    def test_classification_separates_evidence_from_regenerable_cache(self) -> None:
        factory_gate = classify_artifact_path(
            "artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json",
            size_bytes=12_000,
        )
        geometry = classify_artifact_path(
            "artifacts/v3_geometry_retrieval_1025.json",
            size_bytes=30_000_000,
        )
        coordinate = classify_artifact_path(
            "artifacts/v3_foldseek_coordinates_1000/pdb_1ABC.cif",
            size_bytes=6_000_000,
        )
        storage_manifest = classify_artifact_path(
            "artifacts/v3_artifact_producer_consumer_manifest_1025.json",
            size_bytes=1000,
        )

        self.assertEqual(factory_gate["category"], "canonical_evidence")
        self.assertEqual(factory_gate["git_policy"], "keep_in_git")
        self.assertEqual(storage_manifest["category"], "canonical_evidence")
        self.assertEqual(geometry["category"], "regenerable_intermediate")
        self.assertEqual(geometry["git_policy"], "manifest_then_externalize_candidate")
        self.assertEqual(coordinate["category"], "raw_cache")
        self.assertEqual(coordinate["git_policy"], "external_cache_candidate")
        self.assertFalse(factory_gate["deletion_authorized"])
        self.assertFalse(geometry["deletion_authorized"])
        self.assertFalse(coordinate["deletion_authorized"])

    def test_inventory_records_hashes_without_authorizing_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            artifact_dir = root / "artifacts"
            artifact_dir.mkdir()
            (artifact_dir / "v3_label_summary.json").write_text(
                json.dumps({"label_count": 682}),
                encoding="utf-8",
            )
            (artifact_dir / "v3_geometry_retrieval_1025.json").write_text(
                "generated",
                encoding="utf-8",
            )

            inventory = build_artifact_storage_inventory(
                artifact_dir,
                repo_root=root,
                generated_at="2026-05-17T00:00:00Z",
                large_file_threshold_bytes=5,
            )

        self.assertEqual(inventory["metadata"]["method"], "artifact_storage_inventory")
        self.assertEqual(inventory["metadata"]["file_count"], 2)
        self.assertEqual(inventory["metadata"]["deletion_authorized_count"], 0)
        rows = {row["path"]: row for row in inventory["rows"]}
        self.assertIn("sha256", rows["artifacts/v3_label_summary.json"])
        self.assertFalse(rows["artifacts/v3_label_summary.json"]["deletion_authorized"])
        self.assertEqual(
            rows["artifacts/v3_geometry_retrieval_1025.json"]["category"],
            "regenerable_intermediate",
        )

        check = check_artifact_storage_policy(inventory)
        self.assertEqual(check["metadata"]["status"], "passed")
        self.assertEqual(check["blockers"], [])

    def test_policy_check_blocks_deletion_authorization(self) -> None:
        inventory = {
            "metadata": {
                "method": "artifact_storage_inventory",
                "file_count": 1,
                "total_bytes": 1,
            },
            "rows": [
                {
                    "path": "artifacts/raw.tsv",
                    "sha256": "abc",
                    "category": "raw_cache",
                    "deletion_authorized": True,
                }
            ],
        }

        check = check_artifact_storage_policy(inventory)

        self.assertEqual(check["metadata"]["status"], "blocked")
        self.assertEqual(check["metadata"]["deletion_authorized_count"], 1)
        self.assertIn("must not authorize deletion", check["blockers"][0]["reason"])

    def test_current_storage_inventory_is_non_lossy(self) -> None:
        inventory_path = ROOT / "artifacts" / "v3_artifact_storage_inventory_1025.json"
        policy_path = ROOT / "artifacts" / "v3_artifact_storage_policy_check_1025.json"
        manifest_path = (
            ROOT / "artifacts" / "v3_artifact_producer_consumer_manifest_1025.json"
        )
        plan_path = (
            ROOT / "artifacts" / "v3_artifact_migration_readiness_plan_1025.json"
        )
        guard_path = ROOT / "artifacts" / "v3_artifact_admission_guard_1025.json"
        with inventory_path.open("r", encoding="utf-8") as handle:
            inventory = json.load(handle)
        with policy_path.open("r", encoding="utf-8") as handle:
            policy = json.load(handle)
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        with plan_path.open("r", encoding="utf-8") as handle:
            plan = json.load(handle)
        with guard_path.open("r", encoding="utf-8") as handle:
            guard = json.load(handle)

        self.assertEqual(inventory["metadata"]["method"], "artifact_storage_inventory")
        self.assertGreaterEqual(inventory["metadata"]["file_count"], 2500)
        self.assertGreaterEqual(inventory["metadata"]["large_file_count"], 100)
        self.assertEqual(inventory["metadata"]["deletion_authorized_count"], 0)
        self.assertEqual(inventory["metadata"]["policy_blocker_count"], 0)
        self.assertIn("canonical_evidence", inventory["metadata"]["category_counts"])
        self.assertIn("regenerable_intermediate", inventory["metadata"]["category_counts"])
        self.assertIn("raw_cache", inventory["metadata"]["category_counts"])
        self.assertEqual(policy["metadata"]["status"], "passed")
        self.assertEqual(policy["metadata"]["deletion_authorized_count"], 0)
        self.assertEqual(policy["blockers"], [])
        self.assertEqual(
            manifest["metadata"]["method"], "artifact_producer_consumer_manifest"
        )
        self.assertEqual(manifest["metadata"]["included_file_count"], 108)
        self.assertEqual(manifest["metadata"]["deletion_authorized_count"], 0)
        self.assertIn("partially_inferred", manifest["metadata"]["producer_command_status_counts"])
        self.assertEqual(plan["metadata"]["method"], "artifact_migration_readiness_plan")
        self.assertEqual(plan["metadata"]["planned_file_count"], 108)
        self.assertEqual(plan["metadata"]["migration_ready_now_count"], 0)
        self.assertEqual(plan["metadata"]["deletion_authorized_count"], 0)
        self.assertEqual(guard["metadata"]["method"], "artifact_admission_guard")
        self.assertEqual(guard["metadata"]["status"], "passed")
        self.assertEqual(guard["metadata"]["covered_large_file_count"], 108)
        self.assertEqual(guard["blockers"], [])

    def test_large_artifact_manifest_feeds_admission_guard(self) -> None:
        inventory = {
            "metadata": {
                "method": "artifact_storage_inventory",
                "policy_version": "artifact_storage_policy_v1_2026_05_17",
                "large_file_threshold_bytes": 5,
                "file_count": 2,
            },
            "rows": [
                {
                    "path": "artifacts/v3_geometry_retrieval_1025.json",
                    "size_bytes": 10,
                    "sha256": "abc",
                    "category": "regenerable_intermediate",
                    "git_policy": "manifest_then_externalize_candidate",
                    "deletion_authorized": False,
                },
                {
                    "path": "artifacts/new_large_cache.tsv",
                    "size_bytes": 10,
                    "sha256": "def",
                    "category": "raw_cache",
                    "git_policy": "external_cache_candidate",
                    "deletion_authorized": False,
                },
            ],
        }
        manifest = build_artifact_producer_consumer_manifest(
            inventory,
            inventory_path="artifacts/v3_artifact_storage_inventory_1025.json",
            generated_at="2026-05-17T00:00:00Z",
        )
        covered = check_artifact_admission_guard(inventory, manifest)

        self.assertEqual(manifest["metadata"]["included_file_count"], 2)
        self.assertEqual(covered["metadata"]["status"], "passed")
        self.assertEqual(covered["blockers"], [])

        manifest["rows"] = [
            row
            for row in manifest["rows"]
            if row["path"] != "artifacts/new_large_cache.tsv"
        ]
        blocked = check_artifact_admission_guard(inventory, manifest)

        self.assertEqual(blocked["metadata"]["status"], "blocked")
        self.assertEqual(blocked["blockers"][0]["path"], "artifacts/new_large_cache.tsv")


if __name__ == "__main__":
    unittest.main()
