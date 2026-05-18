from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.artifact_storage import (
    ARTIFACT_POINTER_SCHEMA_VERSION,
    CURRENT_MAIN_ARTIFACT_BASELINE,
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

    def test_current_execution_manifest_is_phase_one_fail_closed(self) -> None:
        execution_path = (
            ROOT / "artifacts" / "v3_artifact_migration_execution_1025.json"
        )
        with execution_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "passed")
        self.assertEqual(manifest["metadata"]["manifest_schema_version"], "artifact_migration_execution.v1")
        self.assertEqual(manifest["metadata"]["baseline"], "current_main_three_external_hard_negatives")
        self.assertEqual(manifest["metadata"]["canonical_countable_label_count"], 682)
        self.assertEqual(manifest["metadata"]["row_count"], 108)
        self.assertEqual(manifest["metadata"]["migration_ready_count"], 0)
        self.assertEqual(manifest["metadata"]["remote_sha256_verified_count"], 0)
        self.assertEqual(manifest["metadata"]["removal_allowed_count"], 0)
        self.assertEqual(
            manifest["metadata"]["producer_status_counts"],
            {"known": 68, "unavailable_with_reason": 11, "unknown_blocking": 29},
        )
        self.assertEqual(manifest["metadata"]["unknown_blocking_count"], 29)
        commit = manifest["metadata"]["current_main_commit"]
        for row in manifest["rows"]:
            self.assertEqual(row["storage_class"], "git")
            self.assertEqual(
                row["target_uri"],
                f"git:{row['source_path']}@{commit}",
            )
            self.assertIsInstance(row["producer_commands"], list)
            self.assertIsInstance(row["source_inputs"], list)
            self.assertIsInstance(row["parameter_assumptions"], list)
            self.assertIsInstance(row["producer_provenance_recovery_steps"], list)
            if row["producer_status"] == "unknown_blocking":
                self.assertGreater(len(row["producer_provenance_recovery_steps"]), 0)
            self.assertFalse(row["removal_allowed"])
        unavailable_paths = {
            row["source_path"]
            for row in manifest["rows"]
            if row["producer_status"] == "unavailable_with_reason"
        }
        self.assertIn("artifacts/v3_geometry_features_1000.json", unavailable_paths)
        self.assertIn("artifacts/v3_geometry_features_1025.json", unavailable_paths)

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
        self.assertEqual(row["source_producer_command_status"], "partially_inferred")
        self.assertIn("fail-closed", row["producer_status_reason"])
        self.assertEqual(row["producer_commands"], [])
        self.assertEqual(row["source_inputs"], [])
        self.assertEqual(row["parameter_assumptions"], [])
        self.assertGreater(len(row["producer_provenance_recovery_steps"]), 0)
        self.assertEqual(row["storage_class"], "git")
        self.assertEqual(row["target_uri"], "git:artifacts/large.json@abc123")
        self.assertFalse(row["migration_ready"])
        self.assertFalse(row["remote_sha256_verified"])
        self.assertFalse(row["removal_allowed"])
        self.assertEqual(manifest["metadata"]["removal_allowed_count"], 0)
        self.assertEqual(
            manifest["metadata"]["unknown_blocking_summary"]["by_artifact_category"],
            {"regenerable_intermediate": 1},
        )
        self.assertEqual(
            manifest["metadata"]["unknown_blocking_summary"]["source_paths"],
            ["artifacts/large.json"],
        )
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
            "source_producer_command_status": "unknown",
            "producer_status": "unknown_blocking",
            "producer_status_reason": "source status maps fail-closed",
            "producer_commands": [],
            "source_inputs": [],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": ["recover provenance"],
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
        self.assertIn(
            "migration_ready cannot use producer_status=unknown_blocking",
            reasons,
        )

    def test_validator_blocks_stale_baseline_and_metadata_counts(self) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "0" * 64,
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "noncanonical",
            "source_producer_command_status": "known",
            "producer_status": "known",
            "producer_status_reason": "producer command provenance is recorded as known",
            "producer_commands": ["cmd"],
            "source_inputs": ["input"],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": [],
            "downstream_consumers": ["consumer"],
            "canonical_summary_path": "README.md",
            "storage_class": "git",
            "target_uri": "git:artifacts/raw.tsv@abc123",
            "restore_command": "restore",
            "restore_verification": "sha256",
            "removal_allowed": False,
            "migration_ready": False,
            "remote_sha256_verified": False,
            "restore_test_passed": False,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": True,
            "migration_blockers": ["phase_3_removal_not_authorized"],
        }
        metadata = {
            "manifest_schema_version": "artifact_migration_execution.v1",
            **CURRENT_MAIN_ARTIFACT_BASELINE,
            "row_count": 1,
            "migration_ready_count": 0,
            "unknown_blocking_count": 0,
            "removal_allowed_count": 0,
            "remote_sha256_verified_count": 0,
            "producer_status_counts": {"known": 1},
            "unknown_blocking_summary": {
                "row_count": 0,
                "by_artifact_category": {},
                "by_planned_storage_class": {},
                "by_source_producer_command_status": {},
                "source_paths": [],
            },
        }
        manifest = {"metadata": metadata, "rows": [row]}
        stale_manifest = json.loads(json.dumps(manifest))
        stale_manifest["metadata"]["baseline"] = "older_baseline"
        stale_manifest["metadata"]["removal_allowed_count"] = 1
        stale_manifest["metadata"]["producer_status_counts"] = {"unknown_blocking": 1}
        stale_manifest["metadata"]["unknown_blocking_summary"] = {
            "row_count": 1,
            "by_artifact_category": {"raw_cache": 1},
            "by_planned_storage_class": {},
            "by_source_producer_command_status": {"known": 1},
            "source_paths": ["artifacts/raw.tsv"],
        }

        self.assertEqual(
            validate_artifact_migration_manifest(manifest)["metadata"]["status"],
            "passed",
        )
        validation = validate_artifact_migration_manifest(stale_manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("metadata baseline invariant mismatch", reasons)
        self.assertIn("metadata status count mismatch", reasons)
        self.assertIn("metadata producer_status_counts mismatch", reasons)
        self.assertIn("metadata unknown_blocking_summary mismatch", reasons)

    def test_validator_blocks_git_target_identity_drift(self) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "0" * 64,
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "noncanonical",
            "source_producer_command_status": "known",
            "producer_status": "known",
            "producer_status_reason": "producer command provenance is recorded as known",
            "producer_commands": ["cmd"],
            "source_inputs": ["input"],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": [],
            "downstream_consumers": ["consumer"],
            "canonical_summary_path": "README.md",
            "storage_class": "git",
            "target_uri": "git:artifacts/other.tsv@stale123",
            "restore_command": "restore",
            "restore_verification": "sha256",
            "removal_allowed": False,
            "migration_ready": False,
            "remote_sha256_verified": False,
            "restore_test_passed": False,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": True,
            "migration_blockers": ["phase_3_removal_not_authorized"],
        }
        manifest = {
            "metadata": {
                "manifest_schema_version": "artifact_migration_execution.v1",
                "current_main_commit": "abc123",
                **CURRENT_MAIN_ARTIFACT_BASELINE,
                "row_count": 1,
                "migration_ready_count": 0,
                "unknown_blocking_count": 0,
                "removal_allowed_count": 0,
                "remote_sha256_verified_count": 0,
                "producer_status_counts": {"known": 1},
                "unknown_blocking_summary": {
                    "row_count": 0,
                    "by_artifact_category": {},
                    "by_planned_storage_class": {},
                    "by_source_producer_command_status": {},
                    "source_paths": [],
                },
            },
            "rows": [row],
        }

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("git target_uri source path mismatch", reasons)
        self.assertIn("git target_uri commit mismatch", reasons)

    def test_validator_blocks_migration_ready_git_rows(self) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "0" * 64,
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "noncanonical",
            "source_producer_command_status": "known",
            "producer_status": "known",
            "producer_status_reason": "producer command provenance is recorded as known",
            "producer_commands": ["cmd"],
            "source_inputs": ["input"],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": [],
            "downstream_consumers": ["consumer"],
            "canonical_summary_path": "README.md",
            "storage_class": "git",
            "target_uri": "git:artifacts/raw.tsv@abc123",
            "restore_command": "restore",
            "restore_verification": "sha256",
            "removal_allowed": False,
            "migration_ready": True,
            "remote_sha256_verified": False,
            "restore_test_passed": False,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": True,
            "migration_blockers": ["phase_3_removal_not_authorized"],
        }
        manifest = {
            "metadata": {
                "manifest_schema_version": "artifact_migration_execution.v1",
                "current_main_commit": "abc123",
                **CURRENT_MAIN_ARTIFACT_BASELINE,
                "row_count": 1,
                "migration_ready_count": 1,
                "unknown_blocking_count": 0,
                "removal_allowed_count": 0,
                "remote_sha256_verified_count": 0,
                "producer_status_counts": {"known": 1},
                "unknown_blocking_summary": {
                    "row_count": 0,
                    "by_artifact_category": {},
                    "by_planned_storage_class": {},
                    "by_source_producer_command_status": {},
                    "source_paths": [],
                },
            },
            "rows": [row],
        }

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("migration_ready requires non-git target storage", reasons)

    def test_validator_blocks_externalized_rows_without_target_uri_and_bad_hash(
        self,
    ) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "not-a-sha",
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "noncanonical",
            "source_producer_command_status": "known",
            "producer_status": "known",
            "producer_status_reason": "producer command provenance is recorded as known",
            "producer_commands": ["cmd"],
            "source_inputs": ["input"],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": [],
            "downstream_consumers": ["consumer"],
            "canonical_summary_path": "README.md",
            "storage_class": "object_storage",
            "target_uri": "",
            "restore_command": "restore",
            "restore_verification": "sha256",
            "removal_allowed": False,
            "migration_ready": False,
            "remote_sha256_verified": False,
            "restore_test_passed": False,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": True,
            "migration_blockers": ["phase_2_remote_target_uri_not_uploaded_or_verified"],
        }
        manifest = {
            "metadata": {
                "manifest_schema_version": "artifact_migration_execution.v1",
                **CURRENT_MAIN_ARTIFACT_BASELINE,
                "row_count": 1,
                "migration_ready_count": 0,
                "unknown_blocking_count": 0,
                "removal_allowed_count": 0,
                "remote_sha256_verified_count": 0,
                "producer_status_counts": {"known": 1},
                "unknown_blocking_summary": {
                    "row_count": 0,
                    "by_artifact_category": {},
                    "by_planned_storage_class": {},
                    "by_source_producer_command_status": {},
                    "source_paths": [],
                },
            },
            "rows": [row],
        }

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("malformed SHA-256", reasons)
        self.assertIn("externalized storage requires target_uri", reasons)

    def test_validator_blocks_unsafe_removal_contract_drift(self) -> None:
        row = {
            "source_path": "artifacts/raw.tsv",
            "file_exists": True,
            "size_bytes": 1,
            "sha256": "",
            "artifact_category": "raw_cache",
            "canonical_or_noncanonical": "canonical",
            "source_producer_command_status": "known",
            "producer_status": "invalid_status",
            "producer_status_reason": "producer command provenance is recorded as known",
            "producer_commands": ["cmd"],
            "source_inputs": ["input"],
            "parameter_assumptions": [],
            "producer_provenance_recovery_steps": [],
            "downstream_consumers": [],
            "storage_class": "invalid_storage",
            "target_uri": "",
            "restore_command": "",
            "restore_verification": "sha256",
            "removal_allowed": True,
            "migration_ready": True,
            "remote_sha256_verified": True,
            "restore_test_passed": True,
            "downstream_consumers_accounted_for": True,
            "canonical_summary_present": False,
            "migration_blockers": [],
        }
        manifest = {
            "metadata": {
                "manifest_schema_version": "artifact_migration_execution.v1",
                **CURRENT_MAIN_ARTIFACT_BASELINE,
                "row_count": 1,
                "migration_ready_count": 1,
                "unknown_blocking_count": 0,
                "removal_allowed_count": 1,
                "remote_sha256_verified_count": 1,
                "producer_status_counts": {"invalid_status": 1},
                "unknown_blocking_summary": {
                    "row_count": 0,
                    "by_artifact_category": {},
                    "by_planned_storage_class": {},
                    "by_source_producer_command_status": {},
                    "source_paths": [],
                },
            },
            "rows": [row],
        }

        validation = validate_artifact_migration_manifest(manifest)

        self.assertEqual(validation["metadata"]["status"], "blocked")
        reasons = {blocker["reason"] for blocker in validation["blockers"]}
        self.assertIn("malformed SHA-256", reasons)
        self.assertIn(
            "row must include canonical_summary_path or canonical_summary_not_required_reason",
            reasons,
        )
        self.assertIn("invalid producer_status", reasons)
        self.assertIn("invalid storage_class", reasons)
        self.assertIn("externalized storage requires target_uri", reasons)
        self.assertIn(
            "downstream_consumers_accounted_for disagrees with downstream_consumers",
            reasons,
        )
        self.assertIn("stored removal_allowed disagrees with derived value", reasons)
        self.assertIn("canonical artifacts cannot be marked for removal", reasons)
        self.assertIn("removal requires restore_command", reasons)
        self.assertIn("removal requires canonical summary or explicit reason", reasons)
        self.assertIn("removal requires target_uri", reasons)

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

    def test_restore_artifacts_blocks_existing_mismatch_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            payload = root / "payload.bin"
            payload.write_bytes(b"good")
            artifact_path = root / "artifacts" / "existing.bin"
            artifact_path.parent.mkdir()
            artifact_path.write_bytes(b"wrong")
            manifest = {
                "rows": [
                    {
                        "source_path": "artifacts/existing.bin",
                        "sha256": (
                            "770e607624d689265ca6c44884d0807d9b054d23c473c106"
                            "c72be9de08b7376c"
                        ),
                        "target_uri": payload.as_uri(),
                    }
                ]
            }

            dry = restore_artifacts_from_manifest(
                manifest,
                repo_root=root,
                paths=["artifacts/existing.bin"],
                dry_run=True,
            )
            restored = restore_artifacts_from_manifest(
                manifest,
                repo_root=root,
                paths=["artifacts/existing.bin"],
                dry_run=False,
            )
            observed_existing = artifact_path.read_bytes()

        self.assertEqual(dry["metadata"]["status"], "blocked")
        self.assertEqual(dry["actions"][0]["action"], "failed_existing_mismatch")
        self.assertEqual(restored["metadata"]["status"], "blocked")
        self.assertEqual(restored["actions"][0]["action"], "failed_existing_mismatch")
        self.assertEqual(observed_existing, b"wrong")

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

    def test_artifact_pointer_validator_rejects_empty_restore_contract(self) -> None:
        pointer = {
            "artifact_pointer_schema_version": ARTIFACT_POINTER_SCHEMA_VERSION,
            "original_path": "",
            "sha256": "bad",
            "size_bytes": 0,
            "storage_class": "missing",
            "target_uri": "",
            "restore_manifest": "",
            "canonical_summary": "",
            "restore_verification": "none",
        }

        blockers = validate_artifact_pointer_record(pointer)

        self.assertIn("missing original_path", blockers)
        self.assertIn("malformed sha256", blockers)
        self.assertIn("invalid size_bytes", blockers)
        self.assertIn("invalid storage_class", blockers)
        self.assertIn("missing target_uri", blockers)
        self.assertIn("missing restore_manifest", blockers)
        self.assertIn("missing canonical_summary", blockers)
        self.assertIn("restore_verification must be sha256", blockers)


if __name__ == "__main__":
    unittest.main()
