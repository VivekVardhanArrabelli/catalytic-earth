from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_STORAGE_POLICY_VERSION = "artifact_storage_policy_v1_2026_05_17"
DEFAULT_LARGE_FILE_THRESHOLD_BYTES = 5 * 1024 * 1024
HASH_CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(HASH_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_artifact_path(
    relative_path: str,
    *,
    size_bytes: int,
    large_file_threshold_bytes: int = DEFAULT_LARGE_FILE_THRESHOLD_BYTES,
) -> dict[str, Any]:
    path = Path(relative_path)
    name = path.name.lower()
    stem = path.stem.lower()
    suffix = path.suffix.lower()
    normalized = relative_path.replace("\\", "/").lower()

    category = "compact_artifact"
    git_policy = "keep_in_git"
    reason = "small artifact; keep in git until a later reviewed migration"

    if (
        "/v3_foldseek_coordinates_" in normalized
        or suffix in {".cif", ".pdb", ".bcif"}
    ):
        category = "raw_cache"
        git_policy = "external_cache_candidate"
        reason = "structure coordinate sidecar or raw structural cache"
    elif suffix in {".tsv", ".fasta", ".faa", ".m8", ".npz"}:
        category = "raw_cache"
        git_policy = "external_cache_candidate"
        reason = "raw backend/search/embedding sidecar"
    elif stem.startswith("v1_graph_"):
        category = "regenerable_intermediate"
        git_policy = "manifest_then_externalize_candidate"
        reason = "slice graph can be regenerated from source records and code"
    elif stem.startswith("v3_geometry_features") or stem.startswith(
        "v3_geometry_retrieval"
    ):
        category = "regenerable_intermediate"
        git_policy = "manifest_then_externalize_candidate"
        reason = "geometry feature/retrieval slice is generated from registry inputs"
    elif (
        "label_factory_audit" in stem
        or "label_factory_applied_labels" in stem
        or "label_factory_preview_summary" in stem
        or "label_preview_promotion_readiness" in stem
        or "structure_mapping_issues" in stem
        or "seed_family_performance" in stem
    ):
        category = "regenerable_intermediate"
        git_policy = "manifest_then_externalize_candidate"
        reason = "repeated generated slice artifact; preserve manifest before pruning"
    elif (
        "terminal_decisions" in stem
        or "terminal_review_decisions" in stem
        or "factory_import_gate" in stem
        or "single_import_cycle_gate" in stem
        or "preregistration" in stem
        or "threshold_policy" in stem
        or "ontology_reaudit" in stem
        or "leakage_closure" in stem
        or "review_context_separation" in stem
        or "label_summary" in stem
        or "mcsa_tm_holdout_feasibility_adjudication" in stem
        or "success_criteria" in stem
        or "gate_check" in stem
        or "batch_acceptance_check" in stem
    ):
        category = "canonical_evidence"
        git_policy = "keep_in_git"
        reason = "decision, gate, policy, or regression evidence artifact"
    elif "foldseek" in stem and size_bytes >= large_file_threshold_bytes:
        category = "raw_cache"
        git_policy = "external_cache_candidate"
        reason = "large Foldseek-derived cache/signal; preserve manifest before pruning"
    elif size_bytes >= large_file_threshold_bytes:
        category = "large_unclassified"
        git_policy = "block_until_classified"
        reason = "large artifact lacks a known storage category"

    preservation_requirements = [
        "sha256_recorded",
        "do_not_delete_without_committed_manifest_or_canonical_summary",
    ]
    if category == "raw_cache":
        preservation_requirements.extend(
            [
                "external_storage_location_required_before_git_removal",
                "producer_command_or_source_artifact_required_before_git_removal",
            ]
        )
    elif category == "regenerable_intermediate":
        preservation_requirements.extend(
            [
                "producer_command_inputs_required_before_git_removal",
                "downstream_consumers_required_before_git_removal",
            ]
        )
    elif category == "large_unclassified":
        preservation_requirements.append("manual_classification_required")

    return {
        "category": category,
        "git_policy": git_policy,
        "reason": reason,
        "preservation_requirements": preservation_requirements,
        "deletion_authorized": False,
    }


def build_artifact_storage_inventory(
    artifact_dir: Path,
    *,
    repo_root: Path | None = None,
    generated_at: str | None = None,
    large_file_threshold_bytes: int = DEFAULT_LARGE_FILE_THRESHOLD_BYTES,
    top_n: int = 50,
) -> dict[str, Any]:
    repo_root = repo_root or artifact_dir.parent
    generated_at = generated_at or datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    rows: list[dict[str, Any]] = []
    for path in sorted(artifact_dir.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(repo_root).as_posix()
        size_bytes = path.stat().st_size
        classification = classify_artifact_path(
            relative_path,
            size_bytes=size_bytes,
            large_file_threshold_bytes=large_file_threshold_bytes,
        )
        rows.append(
            {
                "path": relative_path,
                "size_bytes": size_bytes,
                "sha256": sha256_file(path),
                **classification,
            }
        )

    category_counts = Counter(row["category"] for row in rows)
    category_bytes: defaultdict[str, int] = defaultdict(int)
    git_policy_counts = Counter(row["git_policy"] for row in rows)
    git_policy_bytes: defaultdict[str, int] = defaultdict(int)
    for row in rows:
        category_bytes[row["category"]] += int(row["size_bytes"])
        git_policy_bytes[row["git_policy"]] += int(row["size_bytes"])

    large_rows = [
        row for row in rows if int(row["size_bytes"]) >= large_file_threshold_bytes
    ]
    blockers = [
        {
            "path": row["path"],
            "reason": "large artifact must be classified before storage migration",
            "category": row["category"],
            "size_bytes": row["size_bytes"],
        }
        for row in rows
        if row["category"] == "large_unclassified"
    ]
    missing_hash_rows = [row["path"] for row in rows if not row.get("sha256")]
    for path in missing_hash_rows:
        blockers.append(
            {
                "path": path,
                "reason": "artifact manifest row is missing sha256",
            }
        )

    total_bytes = sum(int(row["size_bytes"]) for row in rows)
    deletion_authorized_count = sum(1 for row in rows if row["deletion_authorized"])

    return {
        "metadata": {
            "method": "artifact_storage_inventory",
            "policy_version": ARTIFACT_STORAGE_POLICY_VERSION,
            "generated_at": generated_at,
            "artifact_dir": artifact_dir.as_posix(),
            "file_count": len(rows),
            "total_bytes": total_bytes,
            "total_gib": round(total_bytes / (1024**3), 4),
            "large_file_threshold_bytes": large_file_threshold_bytes,
            "large_file_count": len(large_rows),
            "category_counts": dict(sorted(category_counts.items())),
            "category_bytes": dict(sorted(category_bytes.items())),
            "git_policy_counts": dict(sorted(git_policy_counts.items())),
            "git_policy_bytes": dict(sorted(git_policy_bytes.items())),
            "deletion_authorized_count": deletion_authorized_count,
            "information_loss_guard": (
                "This inventory authorizes no deletion. Any artifact removal or "
                "externalization first requires a committed manifest row with "
                "sha256, producer/provenance, downstream-consumer notes, and a "
                "canonical summary of the scientific conclusion."
            ),
            "policy_blocker_count": len(blockers),
        },
        "policy_findings": {
            "status": "passed" if not blockers and deletion_authorized_count == 0 else "blocked",
            "blockers": blockers,
            "warnings": [
                {
                    "type": "large_regenerable_or_cache_artifacts_present",
                    "count": sum(
                        1
                        for row in large_rows
                        if row["git_policy"]
                        in {
                            "manifest_then_externalize_candidate",
                            "external_cache_candidate",
                        }
                    ),
                    "message": (
                        "Large artifacts remain in git for now. They are candidates "
                        "for later externalization, not deletion."
                    ),
                }
            ],
        },
        "largest_files": sorted(
            rows, key=lambda row: int(row["size_bytes"]), reverse=True
        )[:top_n],
        "rows": rows,
    }


def check_artifact_storage_policy(inventory: dict[str, Any]) -> dict[str, Any]:
    metadata = inventory.get("metadata", {})
    rows = inventory.get("rows", [])
    blockers: list[dict[str, Any]] = []
    if not isinstance(metadata, dict):
        blockers.append({"reason": "inventory metadata is missing or invalid"})
    if not isinstance(rows, list):
        blockers.append({"reason": "inventory rows are missing or invalid"})
        rows = []

    for row in rows:
        if not isinstance(row, dict):
            blockers.append({"reason": "inventory contains a non-object row"})
            continue
        if row.get("deletion_authorized") is not False:
            blockers.append(
                {
                    "path": row.get("path"),
                    "reason": "inventory row must not authorize deletion",
                }
            )
        if not row.get("sha256"):
            blockers.append(
                {"path": row.get("path"), "reason": "inventory row missing sha256"}
            )
        if row.get("category") == "large_unclassified":
            blockers.append(
                {
                    "path": row.get("path"),
                    "reason": "large artifact requires manual category before migration",
                }
            )

    return {
        "metadata": {
            "method": "artifact_storage_policy_check",
            "policy_version": metadata.get(
                "policy_version", ARTIFACT_STORAGE_POLICY_VERSION
            ),
            "source_inventory_method": metadata.get("method"),
            "source_file_count": metadata.get("file_count"),
            "source_total_bytes": metadata.get("total_bytes"),
            "deletion_authorized_count": sum(
                1 for row in rows if isinstance(row, dict) and row.get("deletion_authorized")
            ),
            "blocker_count": len(blockers),
            "status": "passed" if not blockers else "blocked",
        },
        "blockers": blockers,
    }
