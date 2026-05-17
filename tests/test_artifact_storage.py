from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.artifact_storage import (
    ARTIFACT_POINTER_SCHEMA_VERSION,
    build_artifact_migration_execution_manifest,
    build_artifact_pointer_record,
    build_artifact_producer_consumer_manifest,
    build_artifact_storage_inventory,
    check_artifact_admission_guard,
    check_artifact_storage_policy,
    classify_artifact_path,
    restore_artifacts_from_manifest,
    validate_artifact_migration_manifest,
    validate_artifact_pointer_record,
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

    def test_execution_manifest_is_fail_closed_for_phase_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "artifacts").mkdir()
            source = root / "artifacts" / "large.json"
            source.write_text("payload", encoding="utf-8")
            (root / "README.md").write_text("summary", encoding="utf-8")
            digest = "239f59ed55e737c77147cf55ad0c1b030b6d7ee748a7426952f9b852d5a935e5"
            readiness = {
                "metadata": {"method": "artifact_migration_readiness_plan"},
                "rows": [
                    {
                        "path": "artifacts/large.json",
                        "size_bytes": 7,
                        "sha256": digest,
                        "category": "regenerable_intermediate",
                        "producer_command_status": "known",
                        "recommended_storage_class": "candidate_release_asset_later",
                        "canonical_summary_preserving_conclusion": ["README.md"],
                        "migration_blockers": [
                            "explicit human migration approval has not been granted"
                        ],
                    }
                ],
            }
            producer = {
                "metadata": {"method": "artifact_producer_consumer_manifest"},
                "rows": [
                    {
                        "path": "artifacts/large.json",
                        "producer_command_status": "partially_inferred",
                        "downstream_consumers": ["tests"],
                        "canonical_summary_artifacts": ["README.md"],
                    }
                ],
            }

            manifest = build_artifact_migration_execution_manifest(
                readiness,
                producer,
                readiness_plan_path="readiness.json",
                producer_consumer_manifest_path="producer.json",
                execution_manifest_path="execution.json",
                repo_root=root,
                commit_sha="abc123",
                generated_at="2026-05-17T00:00:00Z",
            )

        row = manifest["rows"][0]
        self.assertEqual(
            manifest["metadata"]["manifest_schema_version"],
            "artifact_migration_execution.v1",
        )
        self.assertEqual(manifest["metadata"]["baseline"], "current_main_three_external_hard_negatives")
        self.assertEqual(manifest["metadata"]["slice_id"], 1025)
        self.assertEqual(manifest["metadata"]["canonical_countable_label_count"], 682)
        self.assertEqual(row["producer_status"], "unknown_blocking")
        self.assertEqual(row["storage_class"], "git")
        self.assertEqual(row["target_uri"], "git:artifacts/large.json@abc123")
        self.assertFalse(row["migration_ready"])
        self.assertFalse(row["remote_sha256_verified"])
        self.assertFalse(row["removal_allowed"])
        self.assertEqual(manifest["metadata"]["removal_allowed_count"], 0)
        validation = validate_artifact_migration_manifest(manifest)
        self.assertEqual(validation["metadata"]["status"], "passed")

    def test_validator_recomputes_removal_allowed_and_blocks_unsafe_rows(self) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "0" * 64,
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "noncanonical",
            "producer_status": "unknown_blocking",
            "downstream_consumers": ["consumer"],
            "canonical_summary_path": "README.md",
            "storage_class": "object_storage",
            "target_uri": "file:///tmp/raw.tsv",
            "restore_command": "restore",
            "restore_verification": "sha256",
            "removal_allowed": True,
            "migration_ready": True,
            "remote_sha256_verified": True,
            "restore_test_passed": True,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": True,
            "migration_blockers": [],
        }
        manifest = {
            "metadata": {
                "manifest_schema_version": "artifact_migration_execution.v1"
            },
            "rows": [row],
        }

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("stored removal_allowed disagrees with derived value", reasons)
        self.assertIn(
            "removal cannot use producer_status=unknown_blocking",
            reasons,
        )

    def test_restore_artifacts_supports_local_targets_and_hash_quarantine(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            payload = root / "payload.bin"
            payload.write_bytes(b"restore me")
            expected_sha = (
                "a004c3be1590e7da7f146849ecb3beacd481139ce557de89"
                "aee428243707b490"
            )
            manifest = {
                "rows": [
                    {
                        "source_path": "artifacts/restored.bin",
                        "sha256": expected_sha,
                        "target_uri": payload.as_posix(),
                    }
                ]
            }

            dry = restore_artifacts_from_manifest(
                manifest,
                repo_root=root,
                paths=["artifacts/restored.bin"],
                dry_run=True,
            )
            restored = restore_artifacts_from_manifest(
                manifest,
                repo_root=root,
                paths=["artifacts/restored.bin"],
                dry_run=False,
            )
            bad = restore_artifacts_from_manifest(
                {
                    "rows": [
                        {
                            "source_path": "artifacts/bad.bin",
                            "sha256": "0" * 64,
                            "target_uri": payload.as_posix(),
                        }
                    ]
                },
                repo_root=root,
                paths=["artifacts/bad.bin"],
                dry_run=False,
                quarantine_dir=root / "quarantine",
            )

        self.assertEqual(dry["actions"][0]["action"], "would_restore")
        self.assertEqual(restored["metadata"]["status"], "passed")
        self.assertEqual(restored["metadata"]["restored_count"], 1)
        self.assertEqual(bad["metadata"]["status"], "blocked")
        self.assertEqual(
            bad["actions"][0]["action"],
            "failed_sha256_mismatch_quarantined",
        )

    def test_restore_artifacts_does_not_partially_write_on_later_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            good_payload = root / "good.bin"
            bad_payload = root / "bad.bin"
            good_payload.write_bytes(b"good")
            bad_payload.write_bytes(b"bad")
            manifest = {
                "rows": [
                    {
                        "source_path": "artifacts/good.bin",
                        "sha256": (
                            "770e607624d689265ca6c44884d0807d9b054d23c473c106"
                            "c72be9de08b7376c"
                        ),
                        "target_uri": good_payload.as_uri(),
                    },
                    {
                        "source_path": "artifacts/bad.bin",
                        "sha256": "0" * 64,
                        "target_uri": bad_payload.as_uri(),
                    },
                ]
            }

            result = restore_artifacts_from_manifest(
                manifest,
                repo_root=root,
                paths=["artifacts/good.bin", "artifacts/bad.bin"],
                dry_run=False,
                quarantine_dir=root / "quarantine",
            )

            self.assertEqual(result["metadata"]["status"], "blocked")
            self.assertFalse((root / "artifacts" / "good.bin").exists())
            self.assertFalse((root / "artifacts" / "bad.bin").exists())

    def test_artifact_pointer_record_preserves_restore_contract(self) -> None:
        pointer = build_artifact_pointer_record(
            original_path="artifacts/raw.tsv",
            sha256="a" * 64,
            size_bytes=12,
            storage_class="object_storage",
            target_uri="s3://not-yet-supported/raw.tsv",
            restore_manifest="artifacts/v3_artifact_migration_execution_1025.json",
            canonical_summary="README.md",
        )

        self.assertEqual(
            pointer["artifact_pointer_schema_version"],
            ARTIFACT_POINTER_SCHEMA_VERSION,
        )
        self.assertEqual(pointer["original_path"], "artifacts/raw.tsv")
        self.assertEqual(validate_artifact_pointer_record(pointer), [])


if __name__ == "__main__":
    unittest.main()
