from __future__ import annotations

import hashlib
import re
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
        or "artifact_producer_consumer_manifest" in stem
        or "artifact_migration_readiness_plan" in stem
        or "artifact_admission_guard" in stem
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


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slice_id_from_path(path: str) -> int | None:
    stem = Path(path).stem
    match = re.search(r"_(\d+)(?:_|$)", stem)
    if not match:
        return None
    return int(match.group(1))


def _large_noncanonical_rows(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    metadata = inventory.get("metadata", {})
    threshold = int(
        metadata.get("large_file_threshold_bytes", DEFAULT_LARGE_FILE_THRESHOLD_BYTES)
    )
    rows = inventory.get("rows", [])
    if not isinstance(rows, list):
        return []
    selected = [
        row
        for row in rows
        if isinstance(row, dict)
        and int(row.get("size_bytes", 0)) >= threshold
        and row.get("category") in {"regenerable_intermediate", "raw_cache"}
    ]
    return sorted(selected, key=lambda row: (-int(row["size_bytes"]), row["path"]))


def _previous_geometry_path(slice_id: int | None) -> str | None:
    if slice_id is None or slice_id <= 25:
        return None
    previous = slice_id - 25
    return f"artifacts/v3_geometry_features_{previous}.json"


def _producer_consumer_profile(row: dict[str, Any]) -> dict[str, Any]:
    path = str(row["path"])
    stem = Path(path).stem
    slice_id = _slice_id_from_path(path)
    canonical_summaries = [
        "README.md",
        "work/status.md",
        "work/handoff.md",
        "docs/artifact_storage.md",
    ]
    base: dict[str, Any] = {
        "source_inputs": [],
        "parameter_assumptions": [],
        "likely_producer_cli_commands": [],
        "downstream_consumers": [],
        "canonical_summary_preserves_conclusion": True,
        "canonical_summary_artifacts": canonical_summaries,
        "producer_command_status": "unknown",
        "migration_blockers": [],
    }

    if stem.startswith("v1_graph_") and slice_id is not None:
        base.update(
            {
                "producer_command_status": "known",
                "likely_producer_cli_commands": [
                    (
                        "PYTHONPATH=src python -m catalytic_earth.cli "
                        f"build-v1-graph --max-mcsa {slice_id} --page-size 100 "
                        f"--out {path}"
                    )
                ],
                "source_inputs": [
                    "data/source_registry.json",
                    "live/public M-CSA records at generation time",
                    "live/public Rhea and UniProt references reached by graph ingestion",
                ],
                "parameter_assumptions": [
                    f"max_mcsa={slice_id}",
                    "page_size=100 for current large-slice regeneration",
                    "network source payloads may drift; preserve current SHA-256 before migration",
                ],
                "downstream_consumers": [
                    f"artifacts/v3_geometry_features_{slice_id}.json",
                    f"artifacts/v2_benchmark_{slice_id}.json",
                    f"artifacts/v3_sequence_cluster_proxy_{slice_id}.json",
                    "label-factory, source-scale, geometry, and review-debt workflows for the same slice",
                ],
            }
        )
        return base

    if stem.startswith("v3_geometry_features") and slice_id is not None:
        command = (
            "PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features "
            f"--graph artifacts/v1_graph_{slice_id}.json --max-entries {slice_id} "
        )
        reuse_path = _previous_geometry_path(slice_id)
        status = "known"
        assumptions = [
            f"max_entries={slice_id}",
            "PDB/mmCIF structure availability and selected-PDB choices match the recorded artifact",
        ]
        inputs = [
            f"artifacts/v1_graph_{slice_id}.json",
            "PDB mmCIF coordinate records fetched or cached at generation time",
            "data/registries/curated_mechanism_labels.json for countable/review context",
        ]
        if "selected_pdb_override" in stem:
            command += (
                "--reuse-existing artifacts/v3_geometry_features_1000.json "
                "--selected-pdb-overrides artifacts/v3_selected_pdb_override_plan_700.json "
            )
            inputs.append("artifacts/v3_selected_pdb_override_plan_700.json")
            assumptions.append("selected PDB override rows are repair evidence, not count growth")
        elif reuse_path is not None:
            command += f"--reuse-existing {reuse_path} "
            status = "partially_inferred"
            assumptions.append(
                "exact historical reuse source can vary; adjacent prior slice is the documented pattern"
            )
        command += f"--out {path}"
        base.update(
            {
                "producer_command_status": status,
                "likely_producer_cli_commands": [command],
                "source_inputs": inputs,
                "parameter_assumptions": assumptions,
                "downstream_consumers": [
                    path.replace("v3_geometry_features", "v3_geometry_retrieval"),
                    "geometry evaluation, abstention calibration, hard-negative controls, label-factory gates",
                    "structure-mapping issue analysis and review-debt remediation",
                ],
            }
        )
        return base

    if stem.startswith("v3_geometry_retrieval") and slice_id is not None:
        geometry_path = path.replace("v3_geometry_retrieval", "v3_geometry_features")
        base.update(
            {
                "producer_command_status": "known",
                "likely_producer_cli_commands": [
                    (
                        "PYTHONPATH=src python -m catalytic_earth.cli "
                        f"run-geometry-retrieval --geometry {geometry_path} "
                        f"--top-k 5 --out {path}"
                    )
                ],
                "source_inputs": [
                    geometry_path,
                    "data/registries/mechanism_fingerprints.json",
                    "data/registries/mechanism_ontology.json",
                ],
                "parameter_assumptions": [
                    "top_k=5",
                    "geometry retrieval scoring policy excludes positive mechanism text",
                    "active abstention floor for current guards is 0.4115",
                ],
                "downstream_consumers": [
                    "geometry evaluation and abstention calibration artifacts",
                    "hard-negative, in-scope failure, cofactor coverage, and label-expansion analyses",
                    "label-factory audit, active-learning queue, family guardrails, and batch gates",
                ],
            }
        )
        return base

    if "/v3_foldseek_coordinates_1000/" in path:
        base.update(
            {
                "producer_command_status": "partially_inferred",
                "likely_producer_cli_commands": [
                    (
                        "PYTHONPATH=src python -m catalytic_earth.cli "
                        "build-foldseek-coordinate-readiness --slice-id 1000 "
                        "--retrieval artifacts/v3_geometry_retrieval_1000.json "
                        "--labels data/registries/curated_mechanism_labels.json "
                        "--geometry artifacts/v3_geometry_features_1000.json "
                        "--foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek "
                        "--coordinate-dir artifacts/v3_foldseek_coordinates_1000 "
                        "--max-coordinate-files 25 "
                        "--out artifacts/v3_foldseek_coordinate_readiness_1000.json"
                    )
                ],
                "source_inputs": [
                    "artifacts/v3_geometry_retrieval_1000.json",
                    "artifacts/v3_geometry_features_1000.json",
                    "data/registries/curated_mechanism_labels.json",
                    "public PDB mmCIF coordinate source for the sidecar PDB id",
                ],
                "parameter_assumptions": [
                    "slice_id=1000",
                    "coordinate_dir=artifacts/v3_foldseek_coordinates_1000",
                    "initial readiness staged 25 selected PDB coordinate files",
                ],
                "downstream_consumers": [
                    "artifacts/v3_foldseek_coordinate_readiness_1000.json",
                    "artifacts/v3_foldseek_tm_score_signal_1000_staged25.json",
                    "later descriptive Foldseek/TM signal artifacts and duplicate-screen workflows",
                ],
                "canonical_summary_preserves_conclusion": True,
                "canonical_summary_artifacts": [
                    "README.md",
                    "work/handoff.md",
                    "artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json",
                    "docs/artifact_storage.md",
                ],
                "migration_blockers": [
                    "replacement object-storage location is not approved",
                    "restage/refetch procedure must preserve the recorded PDB id, path, size, and SHA-256",
                ],
            }
        )
        return base

    base["migration_blockers"] = [
        "producer command is unknown; migration must wait for explicit provenance"
    ]
    return base


def build_artifact_producer_consumer_manifest(
    inventory: dict[str, Any],
    *,
    inventory_path: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _utc_timestamp()
    rows: list[dict[str, Any]] = []
    for row in _large_noncanonical_rows(inventory):
        profile = _producer_consumer_profile(row)
        rows.append(
            {
                "path": row["path"],
                "size_bytes": row["size_bytes"],
                "sha256": row["sha256"],
                "category": row["category"],
                "git_policy": row["git_policy"],
                **profile,
            }
        )

    status_counts = Counter(row["producer_command_status"] for row in rows)
    category_counts = Counter(row["category"] for row in rows)
    blocker_rows = [
        row
        for row in rows
        if row["producer_command_status"] != "known"
        or row.get("migration_blockers")
    ]
    return {
        "metadata": {
            "method": "artifact_producer_consumer_manifest",
            "policy_version": ARTIFACT_STORAGE_POLICY_VERSION,
            "generated_at": generated_at,
            "source_inventory": inventory_path,
            "large_file_threshold_bytes": inventory.get("metadata", {}).get(
                "large_file_threshold_bytes", DEFAULT_LARGE_FILE_THRESHOLD_BYTES
            ),
            "included_file_count": len(rows),
            "included_total_bytes": sum(int(row["size_bytes"]) for row in rows),
            "category_counts": dict(sorted(category_counts.items())),
            "producer_command_status_counts": dict(sorted(status_counts.items())),
            "migration_blocker_count": len(blocker_rows),
            "deletion_authorized_count": 0,
            "scope": (
                "All current large raw_cache and regenerable_intermediate rows from "
                "the storage inventory. Unknown or partially inferred provenance is "
                "kept explicit and blocks migration."
            ),
        },
        "rows": rows,
    }


def _migration_decision(row: dict[str, Any]) -> dict[str, Any]:
    path = str(row["path"])
    stem = Path(path).stem
    slice_id = _slice_id_from_path(path)
    tests = [
        "PYTHONPATH=src python -m unittest discover -s tests",
        "PYTHONPATH=src python -m catalytic_earth.cli validate",
        (
            "PYTHONPATH=src python -m catalytic_earth.cli "
            "check-artifact-storage-policy --inventory "
            "artifacts/v3_artifact_storage_inventory_1025.json --out "
            "artifacts/v3_artifact_storage_policy_check_1025.json"
        ),
        (
            "PYTHONPATH=src python -m catalytic_earth.cli "
            "check-artifact-admission-guard --inventory "
            "artifacts/v3_artifact_storage_inventory_1025.json "
            "--producer-consumer-manifest "
            "artifacts/v3_artifact_producer_consumer_manifest_1025.json "
            "--out artifacts/v3_artifact_admission_guard_1025.json"
        ),
    ]

    if row["category"] == "raw_cache":
        return {
            "recommended_storage_class": "candidate_object_storage_later",
            "required_preconditions": [
                "explicit human approval for external object-storage migration",
                "replacement storage URI and checksum manifest committed before any Git removal",
                "restage/refetch workflow documented for source-only checkouts and automation",
                "downstream Foldseek/TM consumers can resolve sidecars from the replacement location",
            ],
            "rollback_expectations": [
                "restore the exact path from object storage using the recorded SHA-256",
                "rerun Foldseek readiness or duplicate-screen checks that consume the sidecar",
            ],
            "tests_to_run": tests,
            "canonical_summary_preserving_conclusion": [
                "artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json",
                "README.md",
                "work/handoff.md",
            ],
        }

    if stem.startswith("v1_graph_"):
        storage_class = (
            "candidate_git_lfs_later"
            if slice_id in {1000, 1025}
            else "candidate_release_asset_later"
        )
        return {
            "recommended_storage_class": storage_class,
            "required_preconditions": [
                "committed producer/consumer manifest row with SHA-256 and source assumptions",
                "explicit human approval for Git LFS or release-asset migration",
                "source-only checkout documentation confirms graph payload is not required for import validation",
                "canonical graph conclusions are summarized outside the large JSON payload",
            ],
            "rollback_expectations": [
                "restore the exact graph JSON path and SHA-256 before rerunning downstream slice artifacts",
                "rerun graph summary, geometry feature generation, tests, and validate",
            ],
            "tests_to_run": tests,
            "canonical_summary_preserving_conclusion": [
                "README.md",
                "work/status.md",
                "artifacts/v3_source_scale_limit_audit_1025.json",
            ],
        }

    if stem.startswith("v3_geometry_features") or stem.startswith("v3_geometry_retrieval"):
        storage_class = (
            "candidate_git_lfs_later"
            if slice_id in {1000, 1025} or "selected_pdb_override" in stem
            else "candidate_release_asset_later"
        )
        return {
            "recommended_storage_class": storage_class,
            "required_preconditions": [
                "committed producer/consumer manifest row with source graph, parameters, and consumers",
                "explicit human approval for Git LFS or release-asset migration",
                "canonical decision/gate artifacts retain the scientific conclusion without the large slice payload",
                "label, leakage, transfer, and performance regressions stay green after payload restoration",
            ],
            "rollback_expectations": [
                "restore the exact geometry/retrieval JSON path and SHA-256",
                "rerun geometry evaluation, label-factory gates, tests, and validate for affected slices",
            ],
            "tests_to_run": tests,
            "canonical_summary_preserving_conclusion": [
                "README.md",
                "work/status.md",
                "artifacts/v3_label_factory_batch_summary.json",
                "artifacts/v3_label_summary.json",
            ],
        }

    return {
        "recommended_storage_class": "keep_in_git",
        "required_preconditions": [
            "unknown artifact family; keep in Git until producer and consumer provenance are explicit"
        ],
        "rollback_expectations": [
            "not eligible for migration, so rollback plan is intentionally unavailable"
        ],
        "tests_to_run": tests,
        "canonical_summary_preserving_conclusion": ["docs/artifact_storage.md"],
    }


def build_artifact_migration_readiness_plan(
    inventory: dict[str, Any],
    producer_consumer_manifest: dict[str, Any],
    *,
    inventory_path: str,
    manifest_path: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _utc_timestamp()
    manifest_rows = {
        row.get("path"): row
        for row in producer_consumer_manifest.get("rows", [])
        if isinstance(row, dict)
    }
    rows: list[dict[str, Any]] = []
    for row in _large_noncanonical_rows(inventory):
        manifest_row = manifest_rows.get(row["path"])
        decision = _migration_decision(row)
        blockers = []
        if manifest_row is None:
            blockers.append("missing producer/consumer manifest row")
        elif manifest_row.get("producer_command_status") != "known":
            blockers.append(
                "producer command is not fully known; confirm provenance before migration"
            )
        blockers.extend(manifest_row.get("migration_blockers", []) if manifest_row else [])
        rows.append(
            {
                "path": row["path"],
                "size_bytes": row["size_bytes"],
                "sha256": row["sha256"],
                "category": row["category"],
                "git_policy": row["git_policy"],
                "producer_command_status": (
                    manifest_row.get("producer_command_status")
                    if manifest_row
                    else "unknown"
                ),
                "migration_ready_now": False,
                "migration_blockers": blockers
                or ["explicit human migration approval has not been granted"],
                **decision,
            }
        )

    class_counts = Counter(row["recommended_storage_class"] for row in rows)
    return {
        "metadata": {
            "method": "artifact_migration_readiness_plan",
            "policy_version": ARTIFACT_STORAGE_POLICY_VERSION,
            "generated_at": generated_at,
            "source_inventory": inventory_path,
            "producer_consumer_manifest": manifest_path,
            "planned_file_count": len(rows),
            "planned_total_bytes": sum(int(row["size_bytes"]) for row in rows),
            "storage_class_counts": dict(sorted(class_counts.items())),
            "migration_ready_now_count": sum(1 for row in rows if row["migration_ready_now"]),
            "deletion_authorized_count": 0,
            "policy": "No migration, deletion, or Git history rewrite is authorized by this plan.",
        },
        "rows": rows,
    }


def check_artifact_admission_guard(
    inventory: dict[str, Any],
    producer_consumer_manifest: dict[str, Any],
) -> dict[str, Any]:
    metadata = inventory.get("metadata", {})
    threshold = int(metadata.get("large_file_threshold_bytes", DEFAULT_LARGE_FILE_THRESHOLD_BYTES))
    rows = inventory.get("rows", [])
    manifest_paths = {
        row.get("path")
        for row in producer_consumer_manifest.get("rows", [])
        if isinstance(row, dict)
    }
    blockers: list[dict[str, Any]] = []
    covered_paths: list[str] = []

    if not isinstance(rows, list):
        blockers.append({"reason": "inventory rows are missing or invalid"})
        rows = []

    for row in rows:
        if not isinstance(row, dict):
            blockers.append({"reason": "inventory contains a non-object row"})
            continue
        if int(row.get("size_bytes", 0)) < threshold:
            continue
        path = row.get("path")
        category = row.get("category")
        if row.get("deletion_authorized") is not False:
            blockers.append(
                {"path": path, "reason": "admission guard forbids deletion authorization"}
            )
        if category == "canonical_evidence":
            covered_paths.append(str(path))
            continue
        if category in {"regenerable_intermediate", "raw_cache"} and path in manifest_paths:
            covered_paths.append(str(path))
            continue
        blockers.append(
            {
                "path": path,
                "category": category,
                "size_bytes": row.get("size_bytes"),
                "reason": (
                    "large noncanonical artifact needs a producer/consumer manifest "
                    "row before it can be accepted; do not delete it"
                ),
            }
        )

    return {
        "metadata": {
            "method": "artifact_admission_guard",
            "policy_version": metadata.get("policy_version", ARTIFACT_STORAGE_POLICY_VERSION),
            "source_inventory_method": metadata.get("method"),
            "source_file_count": metadata.get("file_count"),
            "large_file_threshold_bytes": threshold,
            "large_file_count": sum(
                1
                for row in rows
                if isinstance(row, dict) and int(row.get("size_bytes", 0)) >= threshold
            ),
            "covered_large_file_count": len(covered_paths),
            "blocker_count": len(blockers),
            "deletion_authorized_count": sum(
                1
                for row in rows
                if isinstance(row, dict) and row.get("deletion_authorized")
            ),
            "status": "passed" if not blockers else "blocked",
        },
        "blockers": blockers,
    }
