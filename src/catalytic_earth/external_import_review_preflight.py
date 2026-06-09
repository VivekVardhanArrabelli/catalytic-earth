from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_DATE = "20260609"
ARTIFACT_ID = f"v3_external_import_review_preflight_current702_{RUN_DATE}"
READY_PREVIEW_ARTIFACT_ID = (
    f"v3_external_import_review_ready_preview_current702_{RUN_DATE}"
)
REPAIR_QUEUE_ARTIFACT_ID = (
    f"v3_external_import_review_repair_queue_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_import_review_preflight"

DEFAULT_PREVIEW_SOURCE = (
    "origin/ce-external-admission-qa-merger-20260609:"
    "artifacts/v3_external_admission_import_ready_preview_current702_20260609.json"
)
DEFAULT_MERGED_SURFACE_SOURCE = (
    "origin/ce-external-admission-qa-merger-20260609:"
    "artifacts/v3_external_admission_merged_surface_current702_20260609.json"
)
DEFAULT_MATERIALIZATION_SOURCE = (
    "origin/ce-external-materialization-admission-batch-20260608:"
    "artifacts/v3_external_materialization_admission_batch_current702_20260608.json"
)
DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH = Path(
    "artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json"
)
DEFAULT_TREE_REFS = (
    "origin/ce-external-materialization-admission-batch-20260608",
    "origin/ce-external-admission-qa-merger-20260609",
)
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_external_import_review_preflight_current702_{RUN_DATE}.json"
)
DEFAULT_READY_PREVIEW_PATH = Path(
    f"artifacts/v3_external_import_review_ready_preview_current702_{RUN_DATE}.json"
)
DEFAULT_REPAIR_QUEUE_PATH = Path(
    f"artifacts/v3_external_import_review_repair_queue_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/external_import_review_preflight_current702_{RUN_DATE}.md"
)

TERMINAL_STATES = (
    "controlled_import_review_ready",
    "needs_structural_duplicate_screen",
    "needs_family_policy_review",
    "repairable_locator_blocker",
    "repairable_coordinate_blocker",
    "duplicate_current702_conflict",
    "duplicate_external_conflict",
    "reject/OOS_preserve_signal",
    "hard_blocked_with_next_action",
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_git_source(source: str | Path) -> bool:
    text = str(source)
    if Path(text).exists():
        return False
    return ":" in text and not text.startswith(("http://", "https://"))


def _split_git_source(source: str | Path) -> tuple[str, str]:
    ref, path = str(source).split(":", 1)
    return ref, path


def _git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def _read_source(source: str | Path) -> tuple[Any, dict[str, Any]]:
    if _is_git_source(source):
        ref, path = _split_git_source(source)
        raw = _git_output("show", f"{ref}:{path}")
        commit = _git_output("rev-parse", ref).decode("utf-8").strip()
        return json.loads(raw), {
            "source": str(source),
            "kind": "git_ref_path",
            "git_ref": ref,
            "git_commit": commit,
            "path": path,
            "sha256": _sha256_bytes(raw),
            "bytes": len(raw),
        }
    path = Path(source)
    raw = path.read_bytes()
    return json.loads(raw), {
        "source": str(source),
        "kind": "file",
        "path": str(path),
        "sha256": _sha256_bytes(raw),
        "bytes": len(raw),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _source_rows(payload: Any) -> list[dict[str, Any]]:
    rows = payload.get("rows") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _git_tree_paths(ref: str) -> set[str]:
    try:
        raw = _git_output("ls-tree", "-r", "--name-only", ref)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()
    return {line for line in raw.decode("utf-8").splitlines() if line}


def _path_exists_in_sources(path: str | None, tree_paths: set[str]) -> bool:
    if not path:
        return False
    return Path(path).exists() or path in tree_paths


def _read_json_path_from_sources(path: str | None, tree_refs: tuple[str, ...]) -> Any | None:
    if not path:
        return None
    local_path = Path(path)
    if local_path.exists():
        return json.loads(local_path.read_text(encoding="utf-8"))
    for ref in tree_refs:
        try:
            return json.loads(_git_output("show", f"{ref}:{path}"))
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            continue
    return None


def _normalize_structure_id(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).split("/")[-1].strip()
    text = re.sub(r"\.cif$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^pdb[_-]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^afdb[_-]", "", text, flags=re.IGNORECASE)
    match = re.match(r"AF-([A-Z0-9]+)-F\d(?:-model_v\d+)?$", text, flags=re.IGNORECASE)
    if match:
        return match.group(1).upper()
    text = re.sub(r"_v\d+$", "", text, flags=re.IGNORECASE)
    if len(text) == 4 and text.isalnum():
        return text.upper()
    return text.upper()


def _current702_structure_index(manifest: Any) -> dict[str, list[dict[str, str]]]:
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    if not isinstance(manifest, dict):
        return index
    for row in manifest.get("rows") or []:
        if not isinstance(row, dict):
            continue
        for field in ("selected_structure_id", "selected_structure_key", "coordinate_path"):
            normalized = _normalize_structure_id(row.get(field))
            if normalized:
                index[normalized].append(
                    {
                        "entry_id": str(row.get("entry_id") or ""),
                        "field": field,
                        "value": str(row.get(field) or ""),
                    }
                )
    for structure in manifest.get("structures") or []:
        if not isinstance(structure, dict):
            continue
        entry_ids = structure.get("entry_ids") or []
        entry_text = ",".join(str(entry_id) for entry_id in entry_ids)
        for field in ("structure_id", "structure_key", "coordinate_path"):
            normalized = _normalize_structure_id(structure.get(field))
            if normalized:
                index[normalized].append(
                    {
                        "entry_id": entry_text,
                        "field": field,
                        "value": str(structure.get(field) or ""),
                    }
                )
    return index


def _source_hashes_ok(source_hashes: Any) -> bool:
    if not isinstance(source_hashes, dict):
        return False
    required = {
        "full_row_sha256",
        "queue_row_sha256",
        "uniprot_entry_record_sha256",
        "uniprot_search_row_sha256",
    }
    for key in required:
        value = source_hashes.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            return False
    return True


def _source_provenance_ok(source_provenance: Any) -> bool:
    if not isinstance(source_provenance, dict):
        return False
    return bool(
        source_provenance.get("query_timestamp_utc")
        and source_provenance.get("source_hash_basis")
    )


def _candidate_key(row: dict[str, Any]) -> str:
    return str(row.get("candidate_id") or row.get("stable_candidate_key") or row.get("accession"))


def _family_policy_review_needed(row: dict[str, Any], lane_counts: Counter[str]) -> bool:
    lane = str(row.get("target_family_lane") or "")
    if lane == "near-orphan/no-reliable-structure" and lane_counts[lane] < 2:
        return True
    return False


def build_external_import_review_preflight(
    *,
    preview_source: str | Path = DEFAULT_PREVIEW_SOURCE,
    merged_surface_source: str | Path = DEFAULT_MERGED_SURFACE_SOURCE,
    materialization_source: str | Path = DEFAULT_MATERIALIZATION_SOURCE,
    current702_coordinate_manifest_path: str | Path = DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH,
    tree_refs: tuple[str, ...] = DEFAULT_TREE_REFS,
    expected_preview_count: int = 333,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created_utc = created_utc or _utc_now_iso()
    preview, preview_record = _read_source(preview_source)
    merged_surface, merged_record = _read_source(merged_surface_source)
    materialization, materialization_record = _read_source(materialization_source)
    coordinate_manifest, coordinate_record = _read_source(current702_coordinate_manifest_path)

    preview_rows = _source_rows(preview)
    merged_rows = _source_rows(merged_surface)
    materialization_rows = _source_rows(materialization)
    merged_by_candidate = {_candidate_key(row): row for row in merged_rows}
    materialization_by_candidate = {_candidate_key(row): row for row in materialization_rows}
    lane_counts = Counter(str(row.get("target_family_lane") or "unknown") for row in preview_rows)
    sequence_hash_counts = Counter(
        ((row.get("duplicate_status") or {}).get("exact_sequence_sha256"))
        for row in preview_rows
        if (row.get("duplicate_status") or {}).get("exact_sequence_sha256")
    )
    tree_paths: set[str] = set()
    for ref in tree_refs:
        tree_paths.update(_git_tree_paths(ref))
    current702_structure_index = _current702_structure_index(coordinate_manifest)

    rows: list[dict[str, Any]] = []
    issues: list[str] = []
    for row in preview_rows:
        candidate_id = _candidate_key(row)
        merged_row = merged_by_candidate.get(candidate_id, {})
        materialization_row = materialization_by_candidate.get(candidate_id, {})
        lane = str(row.get("target_family_lane") or "unknown")
        duplicate_status = row.get("duplicate_status") or {}
        non_overlap = row.get("non_overlap_checks") or {}
        source_hashes = row.get("source_hashes") or {}
        source_provenance = row.get("source_provenance") or merged_row.get("source_provenance")
        locator_path = row.get("locator_sidecar_path")
        coordinate_path = row.get("coordinate_path")
        locator_sidecar = _read_json_path_from_sources(
            str(locator_path) if locator_path else None, tree_refs
        )

        sequence_sha = duplicate_status.get("exact_sequence_sha256")
        coordinate_keys = {
            key
            for key in (
                _normalize_structure_id(coordinate_path),
                _normalize_structure_id(merged_row.get("coordinate_path")),
                _normalize_structure_id(merged_row.get("afdb_or_pdb_identifier")),
            )
            if key
        }
        coordinate_overlap_hits: list[dict[str, Any]] = []
        for key in sorted(coordinate_keys):
            for hit in current702_structure_index.get(key, [])[:5]:
                coordinate_overlap_hits.append({"matched_key": key, **hit})

        locator_coordinate_provenance = (
            locator_sidecar.get("coordinate_provenance")
            if isinstance(locator_sidecar, dict)
            else {}
        )
        locator_guardrails = locator_sidecar.get("guardrails") if isinstance(locator_sidecar, dict) else {}
        locator_rows = locator_sidecar.get("residue_locators") if isinstance(locator_sidecar, dict) else []
        locator_source_free_ok = bool(
            isinstance(locator_sidecar, dict)
            and locator_sidecar.get("source_free_active_site_locator_status") == "ready"
            and locator_sidecar.get("schema_version")
            == "v3.external_source_free_active_site_locator_review_only"
            and isinstance(locator_guardrails, dict)
            and locator_guardrails.get("production_registry_edited") is False
            and locator_guardrails.get("label_import_performed") is False
            and locator_guardrails.get("review_only") is True
        )
        locator_coordinate_hash_present = bool(
            isinstance(locator_coordinate_provenance, dict)
            and re.fullmatch(
                r"[0-9a-f]{64}",
                str(locator_coordinate_provenance.get("coordinate_sha256") or ""),
            )
        )

        checks = {
            "source_provenance_present": _source_provenance_ok(source_provenance),
            "source_hashes_present": _source_hashes_ok(source_hashes),
            "locator_sidecar_path_present": bool(locator_path),
            "locator_sidecar_exists": _path_exists_in_sources(
                str(locator_path) if locator_path else None, tree_paths
            ),
            "locator_sidecar_parseable": isinstance(locator_sidecar, dict),
            "locator_source_free_ready": locator_source_free_ok,
            "locator_residue_count": len(locator_rows) if isinstance(locator_rows, list) else 0,
            "coordinate_path_present": bool(coordinate_path),
            "coordinate_materialized": _path_exists_in_sources(
                str(coordinate_path) if coordinate_path else None, tree_paths
            ),
            "coordinate_hash_present": locator_coordinate_hash_present,
            "exact_current702_non_overlap": bool(non_overlap.get("exact_current702_non_overlap")),
            "sequence_hash_present": bool(sequence_sha),
            "sequence_hash_unique_in_preview": (
                bool(sequence_sha) and sequence_hash_counts[sequence_sha] == 1
            ),
            "exact_coordinate_or_structure_id_current702_overlap": bool(coordinate_overlap_hits),
        }
        current702_conflict = bool(
            duplicate_status.get("duplicate_or_current_registry_conflict")
            or not checks["exact_current702_non_overlap"]
        )
        external_conflict = bool(
            non_overlap.get("external_duplicate_overlap_present")
            or merged_row.get("external_duplicate_conflict")
        )
        locator_blocked = not (
            checks["locator_sidecar_path_present"]
            and checks["locator_sidecar_exists"]
            and checks["locator_sidecar_parseable"]
            and checks["locator_source_free_ready"]
            and checks["locator_residue_count"] > 0
        )
        coordinate_blocked = not (
            checks["coordinate_path_present"]
            and checks["coordinate_materialized"]
            and checks["coordinate_hash_present"]
        )
        blockers: list[str] = []
        if not checks["source_provenance_present"]:
            blockers.append("source_provenance_missing_or_incomplete")
        if not checks["source_hashes_present"]:
            blockers.append("source_hashes_missing_or_malformed")
        if current702_conflict:
            blockers.append("exact_current702_accession_or_sequence_conflict")
        if external_conflict:
            blockers.append("external_duplicate_accession_or_sequence_conflict")
        if not checks["sequence_hash_unique_in_preview"]:
            blockers.append("sequence_hash_not_unique_in_preview")
        if locator_blocked:
            blockers.append("source_free_locator_sidecar_missing_or_not_ready")
        if coordinate_blocked:
            blockers.append("coordinate_materialization_or_hash_missing")
        if checks["exact_coordinate_or_structure_id_current702_overlap"]:
            blockers.append("exact_coordinate_or_structure_id_current702_overlap")
        if _family_policy_review_needed(row, lane_counts):
            blockers.append("singleton_near_orphan_lane_needs_family_policy_review")

        if current702_conflict:
            terminal_state = "duplicate_current702_conflict"
        elif external_conflict or not checks["sequence_hash_unique_in_preview"]:
            terminal_state = "duplicate_external_conflict"
        elif not checks["source_provenance_present"] or not checks["source_hashes_present"]:
            terminal_state = "hard_blocked_with_next_action"
        elif locator_blocked:
            terminal_state = "repairable_locator_blocker"
        elif coordinate_blocked:
            terminal_state = "repairable_coordinate_blocker"
        elif checks["exact_coordinate_or_structure_id_current702_overlap"]:
            terminal_state = "needs_structural_duplicate_screen"
        elif _family_policy_review_needed(row, lane_counts):
            terminal_state = "needs_family_policy_review"
        else:
            terminal_state = "controlled_import_review_ready"

        if terminal_state not in TERMINAL_STATES:
            issues.append(f"unknown terminal state for {candidate_id}: {terminal_state}")

        rows.append(
            {
                "candidate_id": candidate_id,
                "accession": row.get("accession"),
                "stable_candidate_key": row.get("stable_candidate_key"),
                "target_family_lane": lane,
                "merge_status": row.get("merge_status"),
                "terminal_state": terminal_state,
                "automated_checks": checks,
                "blockers": sorted(set(blockers)),
                "coordinate_overlap_hits": coordinate_overlap_hits,
                "duplicate_status": {
                    "current702_conflict": current702_conflict,
                    "external_duplicate_conflict": external_conflict,
                    "current702_status": duplicate_status.get(
                        "current_registry_conflict_status"
                    )
                    or merged_row.get("duplicate_current_registry_conflict_status"),
                    "external_status": merged_row.get(
                        "duplicate_external_pilot_conflict_status"
                    ),
                    "exact_sequence_sha256": sequence_sha,
                },
                "source_provenance": {
                    "query_timestamp_utc": (
                        source_provenance.get("query_timestamp_utc")
                        if isinstance(source_provenance, dict)
                        else None
                    ),
                    "source_hash_basis": (
                        source_provenance.get("source_hash_basis")
                        if isinstance(source_provenance, dict)
                        else None
                    ),
                },
                "source_hashes": source_hashes,
                "locator_sidecar_path": locator_path,
                "coordinate_path": coordinate_path,
                "coordinate_hash_sha256": (
                    locator_coordinate_provenance.get("coordinate_sha256")
                    if isinstance(locator_coordinate_provenance, dict)
                    else None
                ),
                "materialization_context": {
                    "queue_name": materialization_row.get("queue_name")
                    or merged_row.get("materialization_queue_name"),
                    "row_sha256": materialization_row.get("row_sha256")
                    or merged_row.get("row_sha256"),
                    "coordinate_materialized_now": materialization_row.get(
                        "coordinate_materialized_now"
                    )
                    or merged_row.get("coordinate_materialized_now"),
                    "locator_sidecar_materialized_now": materialization_row.get(
                        "locator_sidecar_materialized_now"
                    )
                    or merged_row.get("locator_sidecar_materialized_now"),
                },
                "structural_duplicate_screen_status": (
                    "exact_coordinate_identifier_overlap_screen_clean_full_tm_screen_not_run"
                    if not coordinate_overlap_hits
                    else "exact_coordinate_identifier_overlap_requires_structural_screen"
                ),
                "ready_for_production_label_import": False,
                "next_action": _next_action_for_terminal_state(terminal_state),
            }
        )

    terminal_counts = Counter(row["terminal_state"] for row in rows)
    lane_terminal_counts: dict[str, dict[str, int]] = {}
    for row in rows:
        lane_terminal_counts.setdefault(row["target_family_lane"], Counter())
        lane_terminal_counts[row["target_family_lane"]][row["terminal_state"]] += 1
    lane_terminal_counts = {
        lane: dict(sorted(counter.items())) for lane, counter in sorted(lane_terminal_counts.items())
    }

    ready_count = terminal_counts["controlled_import_review_ready"]
    counts_reconcile = sum(terminal_counts.values()) == len(preview_rows)
    all_preview_rows_have_merged_context = all(
        _candidate_key(row) in merged_by_candidate for row in preview_rows
    )
    all_preview_rows_have_source_provenance = all(
        row["automated_checks"]["source_provenance_present"] for row in rows
    )
    all_preview_rows_have_source_hashes = all(
        row["automated_checks"]["source_hashes_present"] for row in rows
    )
    validation_checks = {
        "passed": not issues
        and len(preview_rows) == expected_preview_count
        and counts_reconcile
        and all_preview_rows_have_merged_context
        and all_preview_rows_have_source_provenance
        and all_preview_rows_have_source_hashes,
        "issues": issues,
        "expected_preview_count": expected_preview_count,
        "preview_row_count": len(preview_rows),
        "counts_reconcile": counts_reconcile,
        "all_preview_rows_have_merged_context": all_preview_rows_have_merged_context,
        "all_preview_rows_have_source_provenance": all_preview_rows_have_source_provenance,
        "all_preview_rows_have_source_hashes": all_preview_rows_have_source_hashes,
        "all_preview_rows_have_source_free_locator": all(
            row["automated_checks"]["locator_source_free_ready"] for row in rows
        ),
        "all_preview_rows_have_coordinate_hash": all(
            row["automated_checks"]["coordinate_hash_present"] for row in rows
        ),
        "all_preview_rows_have_materialized_coordinate": all(
            row["automated_checks"]["coordinate_materialized"] for row in rows
        ),
        "all_ready_rows_have_source_provenance": all(
            row["automated_checks"]["source_provenance_present"]
            for row in rows
            if row["terminal_state"] == "controlled_import_review_ready"
        ),
        "all_ready_rows_have_source_free_locator": all(
            row["automated_checks"]["locator_source_free_ready"]
            for row in rows
            if row["terminal_state"] == "controlled_import_review_ready"
        ),
        "all_ready_rows_have_coordinate_hash": all(
            row["automated_checks"]["coordinate_hash_present"]
            for row in rows
            if row["terminal_state"] == "controlled_import_review_ready"
        ),
        "sequence_hashes_unique": all(
            row["automated_checks"]["sequence_hash_unique_in_preview"] for row in rows
        ),
        "exact_coordinate_current702_overlap_count": sum(
            row["automated_checks"]["exact_coordinate_or_structure_id_current702_overlap"]
            for row in rows
        ),
    }
    if len(preview_rows) != expected_preview_count:
        validation_checks["issues"].append(
            f"preview row count {len(preview_rows)} != expected {expected_preview_count}"
        )
        validation_checks["passed"] = False

    artifact = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc,
        "scope": (
            "Controlled import-review preflight for the 333 external import-ready "
            "preview rows. This classifies rows for review batching without "
            "performing a production import."
        ),
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "final_import_files_edited": False,
            "heldout_splits_edited": False,
            "production_thresholds_edited": False,
            "model_weights_edited": False,
            "review_only": True,
        },
        "source_artifacts": {
            "external_admission_import_ready_preview": preview_record,
            "external_admission_merged_surface": merged_record,
            "external_materialization_admission_batch": materialization_record,
            "current702_coordinate_manifest": coordinate_record,
        },
        "counts": {
            "preview_rows": len(preview_rows),
            "controlled_import_review_ready": ready_count,
            "not_ready_rows": len(preview_rows) - ready_count,
            "duplicate_current702_conflict_rows": terminal_counts[
                "duplicate_current702_conflict"
            ],
            "duplicate_external_conflict_rows": terminal_counts[
                "duplicate_external_conflict"
            ],
            "repair_queue_rows": len(preview_rows) - ready_count,
            "sequence_hash_duplicate_rows": sum(
                1
                for row in rows
                if not row["automated_checks"]["sequence_hash_unique_in_preview"]
            ),
            "exact_coordinate_current702_overlap_rows": validation_checks[
                "exact_coordinate_current702_overlap_count"
            ],
        },
        "terminal_state_counts": {
            state: terminal_counts.get(state, 0) for state in TERMINAL_STATES
        },
        "lane_counts": dict(sorted(lane_counts.items())),
        "lane_terminal_state_counts": lane_terminal_counts,
        "lane_balance": _lane_balance_summary(lane_counts),
        "policy_blockers": _policy_blockers(ready_count),
        "batch_approval": {
            "row_by_row_human_review_required_for_ready_rows": False,
            "final_human_batch_approval_could_import_rows_at_once": ready_count > 0,
            "batch_import_candidate_count": ready_count,
            "production_import_authorized_by_this_artifact": False,
            "statement": (
                f"A final controlled human batch approval could cover {ready_count} "
                "machine-clean rows at once rather than row-by-row; production "
                "registry authorization and label-factory gates remain outside "
                "this preflight."
            ),
        },
        "validation_checks": validation_checks,
        "rows": rows,
    }
    artifact["artifact_sha256"] = _canonical_sha256(
        {key: value for key, value in artifact.items() if key != "artifact_sha256"}
    )
    return artifact


def _next_action_for_terminal_state(terminal_state: str) -> str:
    if terminal_state == "controlled_import_review_ready":
        return (
            "Batch with other machine-clean rows for final controlled human import "
            "review; do not import without explicit production authorization."
        )
    if terminal_state == "duplicate_external_conflict":
        return "Resolve external duplicate provenance before any batch approval."
    if terminal_state == "duplicate_current702_conflict":
        return "Reject as current702 duplicate unless a reviewer records a distinct mechanism."
    if terminal_state == "repairable_locator_blocker":
        return "Repair or rematerialize the source-free locator sidecar."
    if terminal_state == "repairable_coordinate_blocker":
        return "Repair coordinate materialization or coordinate hash provenance."
    if terminal_state == "needs_structural_duplicate_screen":
        return "Run current702 structural duplicate screening before import review."
    if terminal_state == "needs_family_policy_review":
        return "Record family/lane policy before batch import approval."
    if terminal_state == "reject/OOS_preserve_signal":
        return "Preserve as out-of-scope signal; do not import."
    return "Resolve hard blocker and rerun preflight."


def _lane_balance_summary(lane_counts: Counter[str]) -> dict[str, Any]:
    if not lane_counts:
        return {"status": "empty", "min_lane_count": 0, "max_lane_count": 0}
    min_lane, min_count = min(lane_counts.items(), key=lambda item: item[1])
    max_lane, max_count = max(lane_counts.items(), key=lambda item: item[1])
    return {
        "status": "skewed_but_batchable_by_lane" if max_count > max(1, min_count) * 10 else "balanced",
        "min_lane": min_lane,
        "min_lane_count": min_count,
        "max_lane": max_lane,
        "max_lane_count": max_count,
        "lane_count": len(lane_counts),
    }


def _policy_blockers(ready_count: int) -> list[dict[str, Any]]:
    blockers = [
        {
            "blocker": "production_registry_change_authorization_not_present",
            "scope": "production_import",
            "ready_rows_affected": ready_count,
        },
        {
            "blocker": "label_factory_gate_and_explicit_review_decision_not_run_here",
            "scope": "production_import",
            "ready_rows_affected": ready_count,
        },
        {
            "blocker": "full_foldseek_tm_current702_structural_duplicate_screen_not_computed",
            "scope": "caveat",
            "ready_rows_affected": ready_count,
            "evidence_available_here": "exact coordinate/structure-id overlap screen only",
        },
    ]
    return blockers


def build_external_import_review_ready_preview(
    preflight: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "stable_candidate_key": row.get("stable_candidate_key"),
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
            "coordinate_hash_sha256": row.get("coordinate_hash_sha256"),
            "source_hashes": row.get("source_hashes"),
            "ready_for_controlled_import_review": True,
            "ready_for_production_label_import": False,
            "remaining_required_before_import": [
                "label_factory_gate_and_explicit_review_decision",
                "controlled_import_review_lane_approval",
                "production_registry_change_authorization",
            ],
        }
        for row in preflight.get("rows", [])
        if row.get("terminal_state") == "controlled_import_review_ready"
    ]
    return {
        "artifact_id": READY_PREVIEW_ARTIFACT_ID,
        "schema_version": "v3.external_import_review_ready_preview",
        "created_utc": created_utc or preflight.get("created_utc") or _utc_now_iso(),
        "candidate_count": len(rows),
        "source_artifact_id": preflight.get("artifact_id"),
        "source_artifact_sha256": preflight.get("artifact_sha256"),
        "guardrails": {
            "preview_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
            "ready_for_production_label_import": False,
        },
        "rows": rows,
    }


def build_external_import_review_repair_queue(
    preflight: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "blockers": row.get("blockers", []),
            "next_action": row.get("next_action"),
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
        }
        for row in preflight.get("rows", [])
        if row.get("terminal_state") != "controlled_import_review_ready"
    ]
    return {
        "artifact_id": REPAIR_QUEUE_ARTIFACT_ID,
        "schema_version": "v3.external_import_review_repair_queue",
        "created_utc": created_utc or preflight.get("created_utc") or _utc_now_iso(),
        "candidate_count": len(rows),
        "source_artifact_id": preflight.get("artifact_id"),
        "source_artifact_sha256": preflight.get("artifact_sha256"),
        "guardrails": {
            "queue_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
        },
        "terminal_state_counts": dict(Counter(row["terminal_state"] for row in rows)),
        "rows": rows,
    }


def render_external_import_review_preflight_report(
    preflight: dict[str, Any],
    ready_preview: dict[str, Any],
    repair_queue: dict[str, Any],
) -> str:
    lines = [
        "# External Import Review Preflight - current702",
        "",
        (
            "Controlled import-review preflight over the 333 external "
            "import-ready preview rows. No production registry, import file, "
            "ontology, split, threshold, or model artifact was edited."
        ),
        "",
        "## Summary",
        "",
        f"- Preview rows: {preflight['counts']['preview_rows']}",
        f"- Controlled import-review ready rows: {preflight['counts']['controlled_import_review_ready']}",
        f"- Repair/conflict queue rows: {repair_queue['candidate_count']}",
        (
            "- Final human batch approval: "
            + preflight["batch_approval"]["statement"]
        ),
        "- Production import authorized here: False",
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in preflight["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")
    lines.extend(["", "## Lane Counts", "", "| lane | count |", "| --- | ---: |"])
    for lane, count in preflight["lane_counts"].items():
        lines.append(f"| {lane} | {count} |")
    lines.extend(
        [
            "",
            "## Policy Blockers",
            "",
            "| blocker | scope | ready rows affected |",
            "| --- | --- | ---: |",
        ]
    )
    for blocker in preflight["policy_blockers"]:
        lines.append(
            "| `{}` | `{}` | {} |".format(
                blocker["blocker"],
                blocker["scope"],
                blocker["ready_rows_affected"],
            )
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            f"- JSON/count reconciliation passed: {preflight['validation_checks']['passed']}",
            (
                "- Source provenance present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_source_provenance']}"
            ),
            (
                "- Source hashes present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_source_hashes']}"
            ),
            (
                "- Source-free locators present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_source_free_locator']}"
            ),
            (
                "- Coordinate hashes present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_coordinate_hash']}"
            ),
            (
                "- Sequence hashes unique across preview: "
                f"{preflight['validation_checks']['sequence_hashes_unique']}"
            ),
            (
                "- Exact current702 coordinate/structure-ID overlaps: "
                f"{preflight['validation_checks']['exact_coordinate_current702_overlap_count']}"
            ),
            "",
            "## Review Queue",
            "",
            "| candidate | lane | terminal state | blockers | next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in repair_queue["rows"][:40]:
        lines.append(
            "| `{}` | {} | `{}` | {} | {} |".format(
                row["candidate_id"],
                row["target_family_lane"],
                row["terminal_state"],
                ", ".join(f"`{blocker}`" for blocker in row.get("blockers", [])),
                row.get("next_action") or "",
            )
        )
    if repair_queue["candidate_count"] > 40:
        lines.append(
            f"| ... | ... | ... | ... | plus {repair_queue['candidate_count'] - 40} more rows |"
        )
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Preflight artifact: `artifacts/v3_external_import_review_preflight_current702_{RUN_DATE}.json`",
            f"- Ready preview: `artifacts/v3_external_import_review_ready_preview_current702_{RUN_DATE}.json`",
            f"- Repair/conflict queue: `artifacts/v3_external_import_review_repair_queue_current702_{RUN_DATE}.json`",
            "",
        ]
    )
    return "\n".join(lines)


def write_external_import_review_preflight(
    *,
    preview_source: str | Path = DEFAULT_PREVIEW_SOURCE,
    merged_surface_source: str | Path = DEFAULT_MERGED_SURFACE_SOURCE,
    materialization_source: str | Path = DEFAULT_MATERIALIZATION_SOURCE,
    current702_coordinate_manifest_path: str | Path = DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    ready_preview_path: Path = DEFAULT_READY_PREVIEW_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
    tree_refs: tuple[str, ...] = DEFAULT_TREE_REFS,
    expected_preview_count: int = 333,
    created_utc: str | None = None,
) -> dict[str, Any]:
    preflight = build_external_import_review_preflight(
        preview_source=preview_source,
        merged_surface_source=merged_surface_source,
        materialization_source=materialization_source,
        current702_coordinate_manifest_path=current702_coordinate_manifest_path,
        tree_refs=tree_refs,
        expected_preview_count=expected_preview_count,
        created_utc=created_utc,
    )
    ready_preview = build_external_import_review_ready_preview(
        preflight, created_utc=preflight["created_utc"]
    )
    repair_queue = build_external_import_review_repair_queue(
        preflight, created_utc=preflight["created_utc"]
    )
    _write_json(out_path, preflight)
    _write_json(ready_preview_path, ready_preview)
    _write_json(repair_queue_path, repair_queue)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        render_external_import_review_preflight_report(
            preflight, ready_preview, repair_queue
        ),
        encoding="utf-8",
    )
    return preflight
