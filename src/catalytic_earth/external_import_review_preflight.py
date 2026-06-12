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
BATCH_APPROVAL_PACKET_ARTIFACT_ID = (
    f"v3_external_batch_import_approval_packet_current702_{RUN_DATE}"
)
TARGETED_EXPANSION_DEFENSE_LEDGER_ARTIFACT_ID = (
    f"v3_targeted_expansion_defense_ledger_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_import_review_preflight"

DEFAULT_PREVIEW_SOURCE = Path(
    f"artifacts/v3_external_materialization_wave2_import_ready_preview_current702_{RUN_DATE}.json"
)
DEFAULT_REPAIR_SURFACE_SOURCE = Path(
    f"artifacts/v3_external_materialization_wave2_repair_queue_current702_{RUN_DATE}.json"
)
DEFAULT_MATERIALIZATION_SOURCE = Path(
    f"artifacts/v3_external_materialization_wave2_current702_{RUN_DATE}.json"
)
DEFAULT_MERGED_SURFACE_SOURCE: Path | None = None
DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH = Path(
    "artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json"
)
DEFAULT_TREE_REFS = ("HEAD",)
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
DEFAULT_BATCH_APPROVAL_PACKET_PATH = Path(
    f"artifacts/v3_external_batch_import_approval_packet_current702_{RUN_DATE}.json"
)
DEFAULT_BATCH_APPROVAL_REPORT_PATH = Path(
    f"work/external_batch_import_approval_packet_current702_{RUN_DATE}.md"
)
DEFAULT_DEFENSE_LEDGER_PATH = Path(
    f"artifacts/v3_targeted_expansion_defense_ledger_current702_{RUN_DATE}.json"
)
DEFAULT_DEFENSE_LEDGER_REPORT_PATH = Path(
    f"work/targeted_expansion_defense_ledger_current702_{RUN_DATE}.md"
)
DEFAULT_PREVIOUS_DEFENSE_LEDGER_PATH = Path(
    "artifacts/v3_targeted_expansion_defense_ledger_current702_20260609.json"
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


def _artifact_date(artifact_date: str | None) -> str:
    return artifact_date or RUN_DATE


def _preflight_artifact_id(artifact_date: str | None) -> str:
    return f"v3_external_import_review_preflight_current702_{_artifact_date(artifact_date)}"


def _ready_preview_artifact_id(artifact_date: str | None) -> str:
    return (
        "v3_external_import_review_ready_preview_current702_"
        f"{_artifact_date(artifact_date)}"
    )


def _repair_queue_artifact_id(artifact_date: str | None) -> str:
    return (
        "v3_external_import_review_repair_queue_current702_"
        f"{_artifact_date(artifact_date)}"
    )


def _batch_approval_artifact_id(artifact_date: str | None) -> str:
    return (
        "v3_external_batch_import_approval_packet_current702_"
        f"{_artifact_date(artifact_date)}"
    )


def _defense_ledger_artifact_id(artifact_date: str | None) -> str:
    return (
        "v3_targeted_expansion_defense_ledger_current702_"
        f"{_artifact_date(artifact_date)}"
    )


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


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _source_hashes_ok(source_hashes: Any, *, strict_preview: bool) -> bool:
    if not isinstance(source_hashes, dict):
        return False
    required = {"uniprot_entry_record_sha256", "uniprot_search_row_sha256"}
    if strict_preview:
        required.update({"full_row_sha256", "queue_row_sha256"})
    for key in required:
        if not _valid_sha256(source_hashes.get(key)):
            return False
    for key, value in source_hashes.items():
        if key.endswith("_sha256") and not _valid_sha256(value):
            return False
    return True


def _source_provenance_ok(source_provenance: Any) -> bool:
    if not isinstance(source_provenance, dict):
        return False
    return bool(
        source_provenance.get("query_timestamp_utc")
        and source_provenance.get("source_hash_basis")
    )


def _source_occurrences_ok(source_occurrences: Any) -> bool:
    if not isinstance(source_occurrences, list) or not source_occurrences:
        return False
    for occurrence in source_occurrences:
        if not isinstance(occurrence, dict):
            return False
        if not (
            occurrence.get("source_key")
            and occurrence.get("source_path")
            and occurrence.get("terminal_state")
        ):
            return False
    return True


def _candidate_key(row: dict[str, Any]) -> str:
    return str(row.get("candidate_id") or row.get("stable_candidate_key") or row.get("accession"))


def _family_policy_review_needed(row: dict[str, Any], lane_counts: Counter[str]) -> bool:
    lane = str(row.get("target_family_lane") or "")
    if lane == "near-orphan/no-reliable-structure" and lane_counts[lane] < 2:
        return True
    return False


def _is_preview_row(row: dict[str, Any], preview_candidate_ids: set[str]) -> bool:
    return _candidate_key(row) in preview_candidate_ids or bool(
        row.get("ready_for_controlled_import_review")
        and str(row.get("wave2_terminal_state") or row.get("terminal_state") or "")
        in {"import_ready_preview_carried_forward", "import_ready_preview"}
    )


def _has_exact_current702_duplicate(duplicate_status: Any) -> bool:
    if not isinstance(duplicate_status, dict):
        return False
    status = str(
        duplicate_status.get("current702_status")
        or duplicate_status.get("current_registry_conflict_status")
        or ""
    )
    return status.startswith("exact_current702_") or bool(
        duplicate_status.get("duplicate_or_current_registry_conflict")
        and (
            duplicate_status.get("exact_accession_matched_current_entry_ids")
            or duplicate_status.get("exact_sequence_matched_current_entry_ids")
        )
    )


def _has_external_duplicate(duplicate_status: Any, non_overlap: Any, row: dict[str, Any]) -> bool:
    if isinstance(non_overlap, dict) and non_overlap.get("external_duplicate_overlap_present"):
        return True
    if row.get("external_duplicate_conflict"):
        return True
    if not isinstance(duplicate_status, dict):
        return False
    statuses = [
        duplicate_status.get("external_pilot_status"),
        duplicate_status.get("prior_external_status"),
        duplicate_status.get("duplicate_external_pilot_conflict_status"),
    ]
    return any(str(status or "").startswith("exact_") for status in statuses)


def _repair_terminal_state(row: dict[str, Any]) -> str:
    bucket = str(row.get("repair_bucket") or "")
    wave2_state = str(row.get("wave2_terminal_state") or "")
    source_state = str(row.get("source_terminal_state") or row.get("terminal_state") or "")
    duplicate_status = _duplicate_status_for_row(row)
    if _has_exact_current702_duplicate(duplicate_status):
        return "duplicate_current702_conflict"
    if _has_external_duplicate(duplicate_status, None, row):
        return "duplicate_external_conflict"
    if bucket == "duplicate_conflict_no_import" or wave2_state == "blocked_duplicate_or_current_registry_conflict":
        return "duplicate_external_conflict"
    if (
        "reject/OOS_preserve_signal" in wave2_state
        or "reject/OOS_preserve_signal" in source_state
        or bucket.startswith("reject_or_oos")
    ):
        return "reject/OOS_preserve_signal"
    if bucket == "hard_blocker" or "hard_blocked_with_next_action" in {
        wave2_state,
        source_state,
    }:
        return "hard_blocked_with_next_action"
    if bucket in {"source_free_locator_materialization_needed", "locator_repair"}:
        return "repairable_locator_blocker"
    if bucket in {"coordinate_materialization_continuation_due_disk_floor", "coordinate_repair"}:
        return "repairable_coordinate_blocker"
    if "locator" in wave2_state and "coordinate_pending" not in wave2_state:
        return "repairable_locator_blocker"
    if "coordinate" in wave2_state or "coordinate" in source_state:
        return "repairable_coordinate_blocker"
    return "hard_blocked_with_next_action"


def _duplicate_status_for_row(row: dict[str, Any]) -> dict[str, Any]:
    duplicate_status: dict[str, Any] = {}
    for key in (
        "duplicate_status_summary",
        "duplicate_current_registry_conflict",
        "duplicate_status",
    ):
        value = row.get(key)
        if isinstance(value, dict):
            duplicate_status.update(value)
    external_pilot = duplicate_status.get("external_pilot_conflict")
    if isinstance(external_pilot, dict):
        duplicate_status.setdefault(
            "external_pilot_status",
            external_pilot.get("external_pilot_conflict_status"),
        )
    if row.get("duplicate_current_registry_conflict_status"):
        duplicate_status.setdefault(
            "current702_status",
            row.get("duplicate_current_registry_conflict_status"),
        )
        duplicate_status.setdefault(
            "current_registry_conflict_status",
            row.get("duplicate_current_registry_conflict_status"),
        )
    if row.get("duplicate_external_pilot_conflict_status"):
        duplicate_status.setdefault(
            "external_pilot_status",
            row.get("duplicate_external_pilot_conflict_status"),
        )
    return duplicate_status


def build_external_import_review_preflight(
    *,
    preview_source: str | Path = DEFAULT_PREVIEW_SOURCE,
    merged_surface_source: str | Path | None = DEFAULT_MERGED_SURFACE_SOURCE,
    materialization_source: str | Path = DEFAULT_MATERIALIZATION_SOURCE,
    repair_surface_source: str | Path | None = DEFAULT_REPAIR_SURFACE_SOURCE,
    current702_coordinate_manifest_path: str | Path = DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH,
    tree_refs: tuple[str, ...] = DEFAULT_TREE_REFS,
    expected_preview_count: int = 600,
    expected_repair_count: int | None = 11895,
    expected_review_surface_count: int | None = 12495,
    created_utc: str | None = None,
    artifact_date: str | None = None,
) -> dict[str, Any]:
    created_utc = created_utc or _utc_now_iso()
    artifact_id = _preflight_artifact_id(artifact_date)
    preview, preview_record = _read_source(preview_source)
    materialization, materialization_record = _read_source(materialization_source)
    if merged_surface_source is None:
        merged_rows: list[dict[str, Any]] = []
        merged_record: dict[str, Any] | None = None
    else:
        merged_surface, merged_record = _read_source(merged_surface_source)
        merged_rows = _source_rows(merged_surface)
    if repair_surface_source is None:
        repair_rows: list[dict[str, Any]] = []
        repair_record: dict[str, Any] | None = None
    else:
        repair_surface, repair_record = _read_source(repair_surface_source)
        repair_rows = _source_rows(repair_surface)
    coordinate_manifest, coordinate_record = _read_source(current702_coordinate_manifest_path)

    preview_rows = _source_rows(preview)
    materialization_rows = _source_rows(materialization)
    materialization_counts = (
        materialization.get("counts", {}) if isinstance(materialization, dict) else {}
    )
    merged_by_candidate = {_candidate_key(row): row for row in merged_rows}
    materialization_by_candidate = {_candidate_key(row): row for row in materialization_rows}
    preview_by_candidate = {_candidate_key(row): row for row in preview_rows}
    preview_candidate_ids = set(preview_by_candidate)
    review_rows = list(preview_rows)
    seen_review_candidates = set(preview_candidate_ids)
    for row in repair_rows:
        candidate_id = _candidate_key(row)
        if candidate_id not in seen_review_candidates:
            review_rows.append(row)
            seen_review_candidates.add(candidate_id)
    lane_counts = Counter(str(row.get("target_family_lane") or "unknown") for row in preview_rows)
    sequence_hash_counts = Counter(
        _duplicate_status_for_row(row).get("exact_sequence_sha256")
        for row in preview_rows
        if _duplicate_status_for_row(row).get("exact_sequence_sha256")
    )
    tree_paths: set[str] = set()
    for ref in tree_refs:
        tree_paths.update(_git_tree_paths(ref))
    current702_structure_index = _current702_structure_index(coordinate_manifest)

    rows: list[dict[str, Any]] = []
    issues: list[str] = []
    for row in review_rows:
        candidate_id = _candidate_key(row)
        merged_row = merged_by_candidate.get(candidate_id, {})
        materialization_row = materialization_by_candidate.get(candidate_id, {})
        preview_row = preview_by_candidate.get(candidate_id, {})
        is_preview = _is_preview_row(row, preview_candidate_ids)
        lane = str(row.get("target_family_lane") or "unknown")
        duplicate_status = _duplicate_status_for_row(row)
        non_overlap = row.get("non_overlap_checks") or {}
        source_hashes = row.get("source_hashes") or {}
        source_provenance = (
            row.get("source_provenance")
            or preview_row.get("source_provenance")
            or merged_row.get("source_provenance")
        )
        source_occurrences = (
            row.get("source_occurrences")
            or materialization_row.get("source_occurrences")
            or merged_row.get("source_occurrences")
        )
        locator_path = row.get("locator_sidecar_path")
        coordinate_path = row.get("coordinate_path")
        locator_path_text = str(locator_path) if locator_path else None
        locator_sidecar = (
            _read_json_path_from_sources(locator_path_text, tree_refs)
            if _path_exists_in_sources(locator_path_text, tree_paths)
            else None
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
            and locator_sidecar.get("source_free_active_site_locator_status")
            in {
                "ready",
                "ready_coordinate_local_residue_identity",
                "materialized_pending_coordinate_local_residue_identity",
            }
            and locator_sidecar.get("schema_version")
            in {
                "v3.external_source_free_active_site_locator_review_only",
                "v3.external_materialization_wave2_source_free_locator_sidecar",
            }
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
            "review_scope": (
                "import_ready_preview"
                if is_preview
                else "materialization_repair_surface"
            ),
            "source_provenance_present": _source_provenance_ok(source_provenance)
            or _source_occurrences_ok(source_occurrences),
            "source_hashes_present": _source_hashes_ok(
                source_hashes,
                strict_preview=is_preview
                and "full_row_sha256" in source_hashes
                and "queue_row_sha256" in source_hashes,
            ),
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
            "exact_current702_non_overlap": (
                bool(non_overlap.get("exact_current702_non_overlap"))
                if isinstance(non_overlap, dict) and non_overlap
                else not _has_exact_current702_duplicate(duplicate_status)
            ),
            "sequence_hash_present": bool(sequence_sha),
            "sequence_hash_unique_in_preview": (
                bool(sequence_sha) and sequence_hash_counts[sequence_sha] == 1
            ),
            "exact_coordinate_or_structure_id_current702_overlap": bool(coordinate_overlap_hits),
        }
        current702_conflict = _has_exact_current702_duplicate(
            duplicate_status
        ) or bool(is_preview and not checks["exact_current702_non_overlap"])
        external_conflict = _has_external_duplicate(duplicate_status, non_overlap, row) or bool(
            merged_row.get("external_duplicate_conflict")
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
        if is_preview and not checks["sequence_hash_unique_in_preview"]:
            blockers.append("sequence_hash_not_unique_in_preview")
        if locator_blocked:
            blockers.append("source_free_locator_sidecar_missing_or_not_ready")
        if coordinate_blocked:
            blockers.append("coordinate_materialization_or_hash_missing")
        if checks["exact_coordinate_or_structure_id_current702_overlap"]:
            blockers.append("exact_coordinate_or_structure_id_current702_overlap")
        if _family_policy_review_needed(row, lane_counts):
            blockers.append("singleton_near_orphan_lane_needs_family_policy_review")

        if not is_preview:
            terminal_state = _repair_terminal_state(row)
        elif current702_conflict:
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

        if not is_preview:
            if terminal_state == "duplicate_current702_conflict":
                blockers = ["exact_current702_accession_or_sequence_conflict"]
            elif terminal_state == "duplicate_external_conflict":
                blockers = ["external_duplicate_accession_or_sequence_conflict"]
            elif terminal_state == "repairable_locator_blocker":
                blockers = ["source_free_locator_sidecar_missing_or_not_ready"]
            elif terminal_state == "repairable_coordinate_blocker":
                blockers = ["coordinate_materialization_or_hash_missing"]
            elif terminal_state == "reject/OOS_preserve_signal":
                blockers = ["out_of_scope_or_hard_negative_preserve_signal"]
            elif terminal_state == "hard_blocked_with_next_action":
                blockers = ["source_retrieval_or_materialization_hard_blocker"]
            if not checks["source_provenance_present"]:
                blockers.append("source_provenance_missing_or_incomplete")
            if not checks["source_hashes_present"] and terminal_state in {
                "hard_blocked_with_next_action",
                "repairable_locator_blocker",
                "repairable_coordinate_blocker",
            }:
                blockers.append("source_hashes_missing_or_malformed")

        if terminal_state not in TERMINAL_STATES:
            issues.append(f"unknown terminal state for {candidate_id}: {terminal_state}")

        rows.append(
            {
                "candidate_id": candidate_id,
                "accession": row.get("accession"),
                "stable_candidate_key": row.get("stable_candidate_key"),
                "target_family_lane": lane,
                "review_scope": checks["review_scope"],
                "merge_status": row.get("merge_status"),
                "source_terminal_state": row.get("source_terminal_state")
                or row.get("terminal_state"),
                "wave2_terminal_state": row.get("wave2_terminal_state"),
                "source_import_ready_preview_consumed": bool(
                    row.get("source_import_ready_preview_consumed") or is_preview
                ),
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
                "source_occurrences": source_occurrences if isinstance(source_occurrences, list) else [],
                "source_artifacts_consumed": row.get("source_artifacts_consumed")
                or materialization_row.get("source_artifacts_consumed")
                or [],
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
                    "coordinate_materialization_status": row.get(
                        "coordinate_materialization_status"
                    )
                    or materialization_row.get("coordinate_materialization_status"),
                    "locator_sidecar_status": row.get("locator_sidecar_status")
                    or materialization_row.get("locator_sidecar_status"),
                    "repair_bucket": row.get("repair_bucket")
                    or materialization_row.get("repair_bucket"),
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
    review_scope_counts = Counter(row["review_scope"] for row in rows)
    all_lane_counts = Counter(str(row["target_family_lane"] or "unknown") for row in rows)
    lane_terminal_counts: dict[str, dict[str, int]] = {}
    for row in rows:
        lane_terminal_counts.setdefault(row["target_family_lane"], Counter())
        lane_terminal_counts[row["target_family_lane"]][row["terminal_state"]] += 1
    lane_terminal_counts = {
        lane: dict(sorted(counter.items())) for lane, counter in sorted(lane_terminal_counts.items())
    }

    ready_count = terminal_counts["controlled_import_review_ready"]
    counts_reconcile = sum(terminal_counts.values()) == len(review_rows)
    preview_rows_in_review_surface = sum(
        1 for row in rows if row["review_scope"] == "import_ready_preview"
    )
    repair_rows_in_review_surface = sum(
        1 for row in rows if row["review_scope"] == "materialization_repair_surface"
    )
    all_review_rows_have_materialization_context = all(
        _candidate_key(row) in materialization_by_candidate for row in review_rows
    )
    all_preview_rows_have_materialization_context = all(
        _candidate_key(row) in materialization_by_candidate for row in preview_rows
    )
    all_preview_rows_have_source_provenance = all(
        row["automated_checks"]["source_provenance_present"] for row in rows
        if row["review_scope"] == "import_ready_preview"
    )
    all_preview_rows_have_source_hashes = all(
        row["automated_checks"]["source_hashes_present"] for row in rows
        if row["review_scope"] == "import_ready_preview"
    )
    all_review_rows_have_source_provenance = all(
        row["automated_checks"]["source_provenance_present"] for row in rows
    )
    all_review_rows_have_source_hashes = all(
        row["automated_checks"]["source_hashes_present"] for row in rows
    )
    validation_checks = {
        "passed": not issues
        and len(preview_rows) == expected_preview_count
        and (expected_repair_count is None or len(repair_rows) == expected_repair_count)
        and (
            expected_review_surface_count is None
            or len(review_rows) == expected_review_surface_count
        )
        and counts_reconcile
        and all_review_rows_have_materialization_context
        and all_review_rows_have_source_provenance
        and all_preview_rows_have_source_hashes,
        "issues": issues,
        "expected_preview_count": expected_preview_count,
        "expected_repair_count": expected_repair_count,
        "expected_review_surface_count": expected_review_surface_count,
        "preview_row_count": len(preview_rows),
        "repair_surface_row_count": len(repair_rows),
        "review_surface_row_count": len(review_rows),
        "preview_rows_in_review_surface": preview_rows_in_review_surface,
        "repair_rows_in_review_surface": repair_rows_in_review_surface,
        "counts_reconcile": counts_reconcile,
        "all_review_rows_have_materialization_context": (
            all_review_rows_have_materialization_context
        ),
        "all_preview_rows_have_materialization_context": (
            all_preview_rows_have_materialization_context
        ),
        "all_preview_rows_have_source_provenance": all_preview_rows_have_source_provenance,
        "all_preview_rows_have_source_hashes": all_preview_rows_have_source_hashes,
        "all_review_rows_have_source_provenance": all_review_rows_have_source_provenance,
        "all_review_rows_have_source_hashes": all_review_rows_have_source_hashes,
        "all_preview_rows_have_source_free_locator": all(
            row["automated_checks"]["locator_source_free_ready"] for row in rows
            if row["review_scope"] == "import_ready_preview"
        ),
        "all_preview_rows_have_coordinate_hash": all(
            row["automated_checks"]["coordinate_hash_present"] for row in rows
            if row["review_scope"] == "import_ready_preview"
        ),
        "all_preview_rows_have_materialized_coordinate": all(
            row["automated_checks"]["coordinate_materialized"] for row in rows
            if row["review_scope"] == "import_ready_preview"
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
            row["automated_checks"]["sequence_hash_unique_in_preview"]
            for row in rows
            if row["review_scope"] == "import_ready_preview"
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
    if expected_repair_count is not None and len(repair_rows) != expected_repair_count:
        validation_checks["issues"].append(
            f"repair row count {len(repair_rows)} != expected {expected_repair_count}"
        )
        validation_checks["passed"] = False
    if expected_review_surface_count is not None and len(review_rows) != expected_review_surface_count:
        validation_checks["issues"].append(
            "review surface row count "
            f"{len(review_rows)} != expected {expected_review_surface_count}"
        )
        validation_checks["passed"] = False

    artifact = {
        "artifact_id": artifact_id,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc,
        "scope": (
            "Controlled import-review preflight for the Wave 2 external "
            "materialization review surface: carried-forward import-ready preview "
            "rows plus the expanded materialization repair queue. This classifies "
            "rows for review batching without performing a production import."
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
            "external_materialization_wave2_import_ready_preview": preview_record,
            "external_materialization_wave2_repair_queue": repair_record,
            "external_materialization_wave2_current_surface": materialization_record,
            "external_admission_merged_surface": merged_record,
            "current702_coordinate_manifest": coordinate_record,
        },
        "counts": {
            "preview_rows": len(preview_rows),
            "repair_surface_rows": len(repair_rows),
            "review_surface_rows": len(review_rows),
            "controlled_import_review_ready": ready_count,
            "not_ready_rows": len(review_rows) - ready_count,
            "duplicate_current702_conflict_rows": terminal_counts[
                "duplicate_current702_conflict"
            ],
            "duplicate_external_conflict_rows": terminal_counts[
                "duplicate_external_conflict"
            ],
            "repair_queue_rows": len(review_rows) - ready_count,
            "sequence_hash_duplicate_rows": sum(
                1
                for row in rows
                if row["review_scope"] == "import_ready_preview"
                and not row["automated_checks"]["sequence_hash_unique_in_preview"]
            ),
            "exact_coordinate_current702_overlap_rows": validation_checks[
                "exact_coordinate_current702_overlap_count"
            ],
        },
        "source_surface_reconciliation": {
            "materialization_unique_candidate_rows": materialization_counts.get(
                "unique_candidate_rows", len(materialization_rows)
            ),
            "materialization_input_rows": materialization_counts.get("input_rows"),
            "source_surface_rows_consumed": materialization_counts.get(
                "source_surface_rows_consumed"
            ),
            "import_ready_source_rows_consumed": materialization_counts.get(
                "import_ready_source_rows_consumed"
            ),
            "source_import_ready_preview_rows_consumed": materialization_counts.get(
                "source_import_ready_preview_rows_consumed"
            ),
            "coordinate_reused_from_consumed_preview": materialization_counts.get(
                "coordinate_reused_from_consumed_preview"
            ),
            "coordinate_ready_promoted_preview_count": materialization_counts.get(
                "coordinate_ready_promoted_preview_count"
            ),
            "import_ready_preview_rows_reviewed": len(preview_rows),
            "repair_surface_rows_reviewed": len(repair_rows),
            "review_surface_rows": len(review_rows),
            "explanation": (
                "The preflight reviews the materialized import-ready preview "
                "surface, not only the source preview artifact before Wave 2 "
                "coordinate promotion. On the current Wave 2 artifact, the 600 "
                "preview rows equal the carried-forward consumed-preview "
                "coordinate rows plus additional coordinate-ready rows promoted "
                "during materialization; the remaining unique candidates are "
                "classified through the repair/conflict queue."
            ),
        },
        "terminal_state_counts": {
            state: terminal_counts.get(state, 0) for state in TERMINAL_STATES
        },
        "review_scope_counts": dict(sorted(review_scope_counts.items())),
        "lane_counts": dict(sorted(all_lane_counts.items())),
        "preview_lane_counts": dict(sorted(lane_counts.items())),
        "lane_terminal_state_counts": lane_terminal_counts,
        "lane_balance": _lane_balance_summary(all_lane_counts),
        "preview_lane_balance": _lane_balance_summary(lane_counts),
        "policy_blockers": _policy_blockers(ready_count),
        "batch_approval": {
            "row_by_row_human_review_required_for_ready_rows": False,
            "final_human_batch_approval_could_import_rows_at_once": ready_count > 0,
            "batch_import_candidate_count": ready_count,
            "production_import_authorized_by_this_artifact": False,
            "statement": (
                (
                    f"A final controlled human batch approval could cover {ready_count} "
                    "machine-clean rows at once rather than row-by-row; production "
                    "registry authorization and label-factory gates remain outside "
                    "this preflight."
                )
                if ready_count
                else (
                    "No rows are batch-approvable on current main; final human "
                    "batch approval should wait until source-free locator and "
                    "coordinate/hash blockers clear."
                )
            ),
        },
        "defense_ledger_next_action": (
            f"Record that current main has {ready_count} machine-clean Wave 2 "
            "rows ready for one final controlled human batch approval; preserve "
            "the remaining rows under their terminal duplicate, locator, "
            "coordinate, OOS, structural-screen, family-policy, or hard-blocker "
            "gates and do not import until production authorization and "
            "label-factory gates are recorded."
        ),
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
    artifact_date: str | None = None,
) -> dict[str, Any]:
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "stable_candidate_key": row.get("stable_candidate_key"),
            "target_family_lane": row["target_family_lane"],
            "review_scope": row.get("review_scope"),
            "terminal_state": row["terminal_state"],
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
            "coordinate_hash_sha256": row.get("coordinate_hash_sha256"),
            "source_hashes": row.get("source_hashes"),
            "source_provenance": row.get("source_provenance"),
            "source_occurrences": row.get("source_occurrences"),
            "source_artifacts_consumed": row.get("source_artifacts_consumed"),
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
        "artifact_id": _ready_preview_artifact_id(artifact_date),
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
    artifact_date: str | None = None,
) -> dict[str, Any]:
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "review_scope": row.get("review_scope"),
            "source_terminal_state": row.get("source_terminal_state"),
            "wave2_terminal_state": row.get("wave2_terminal_state"),
            "terminal_state": row["terminal_state"],
            "blockers": row.get("blockers", []),
            "next_action": row.get("next_action"),
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
            "materialization_context": row.get("materialization_context", {}),
        }
        for row in preflight.get("rows", [])
        if row.get("terminal_state") != "controlled_import_review_ready"
    ]
    return {
        "artifact_id": _repair_queue_artifact_id(artifact_date),
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
    *,
    artifact_date: str | None = None,
) -> str:
    output_date = _artifact_date(artifact_date)
    lines = [
        "# External Import Review Preflight - current702",
        "",
        (
            "Controlled import-review preflight over the Wave 2 external "
            "materialization review surface: the carried-forward import-ready "
            "preview rows plus the expanded repair queue. No production registry, "
            "import file, ontology, split, threshold, or model artifact was edited."
        ),
        "",
        "## Summary",
        "",
        f"- Preview rows: {preflight['counts']['preview_rows']}",
        f"- Repair-surface rows: {preflight['counts']['repair_surface_rows']}",
        f"- Total review-surface rows: {preflight['counts']['review_surface_rows']}",
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
    lines.extend(["", "## Review Scope Counts", "", "| scope | count |", "| --- | ---: |"])
    for scope, count in preflight["review_scope_counts"].items():
        lines.append(f"| `{scope}` | {count} |")
    source_reconciliation = preflight.get("source_surface_reconciliation") or {}
    lines.extend(
        [
            "",
            "## Source Surface Reconciliation",
            "",
            "| measure | count |",
            "| --- | ---: |",
        ]
    )
    for key in (
        "materialization_unique_candidate_rows",
        "materialization_input_rows",
        "source_surface_rows_consumed",
        "import_ready_source_rows_consumed",
        "source_import_ready_preview_rows_consumed",
        "coordinate_reused_from_consumed_preview",
        "coordinate_ready_promoted_preview_count",
        "import_ready_preview_rows_reviewed",
        "repair_surface_rows_reviewed",
        "review_surface_rows",
    ):
        value = source_reconciliation.get(key)
        if value is not None:
            lines.append(f"| `{key}` | {value} |")
    if source_reconciliation.get("explanation"):
        lines.extend(["", str(source_reconciliation["explanation"])])
    lines.extend(["", "## Lane Counts", "", "| lane | count |", "| --- | ---: |"])
    for lane, count in preflight["lane_counts"].items():
        lines.append(f"| {lane} | {count} |")
    lines.extend(
        [
            "",
            "## Lane Terminal Counts",
            "",
            "| lane | terminal counts |",
            "| --- | --- |",
        ]
    )
    for lane, terminal_counts in preflight["lane_terminal_state_counts"].items():
        lines.append(f"| {lane} | `{terminal_counts}` |")
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
            f"- Validation passed: {preflight['validation_checks']['passed']}",
            (
                "- JSON/count reconciliation passed: "
                f"{preflight['validation_checks']['counts_reconcile']}"
            ),
            (
                "- Source provenance present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_source_provenance']}"
            ),
            (
                "- Source provenance present for all review rows: "
                f"{preflight['validation_checks']['all_review_rows_have_source_provenance']}"
            ),
            (
                "- Source hashes present for all preview rows: "
                f"{preflight['validation_checks']['all_preview_rows_have_source_hashes']}"
            ),
            (
                "- Source hashes present for all review rows: "
                f"{preflight['validation_checks']['all_review_rows_have_source_hashes']}"
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
            "## Defense Ledger Next Action",
            "",
            str(preflight.get("defense_ledger_next_action") or ""),
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
            f"- Preflight artifact: `artifacts/v3_external_import_review_preflight_current702_{output_date}.json`",
            f"- Ready preview: `artifacts/v3_external_import_review_ready_preview_current702_{output_date}.json`",
            f"- Repair/conflict queue: `artifacts/v3_external_import_review_repair_queue_current702_{output_date}.json`",
            "",
        ]
    )
    return "\n".join(lines)


def write_external_import_review_preflight(
    *,
    preview_source: str | Path = DEFAULT_PREVIEW_SOURCE,
    merged_surface_source: str | Path | None = DEFAULT_MERGED_SURFACE_SOURCE,
    materialization_source: str | Path = DEFAULT_MATERIALIZATION_SOURCE,
    repair_surface_source: str | Path | None = DEFAULT_REPAIR_SURFACE_SOURCE,
    current702_coordinate_manifest_path: str | Path = DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    ready_preview_path: Path = DEFAULT_READY_PREVIEW_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
    tree_refs: tuple[str, ...] = DEFAULT_TREE_REFS,
    expected_preview_count: int = 600,
    expected_repair_count: int | None = 11895,
    expected_review_surface_count: int | None = 12495,
    created_utc: str | None = None,
    artifact_date: str | None = None,
) -> dict[str, Any]:
    preflight = build_external_import_review_preflight(
        preview_source=preview_source,
        merged_surface_source=merged_surface_source,
        materialization_source=materialization_source,
        repair_surface_source=repair_surface_source,
        current702_coordinate_manifest_path=current702_coordinate_manifest_path,
        tree_refs=tree_refs,
        expected_preview_count=expected_preview_count,
        expected_repair_count=expected_repair_count,
        expected_review_surface_count=expected_review_surface_count,
        created_utc=created_utc,
        artifact_date=artifact_date,
    )
    ready_preview = build_external_import_review_ready_preview(
        preflight,
        created_utc=preflight["created_utc"],
        artifact_date=artifact_date,
    )
    repair_queue = build_external_import_review_repair_queue(
        preflight,
        created_utc=preflight["created_utc"],
        artifact_date=artifact_date,
    )
    _write_json(out_path, preflight)
    _write_json(ready_preview_path, ready_preview)
    _write_json(repair_queue_path, repair_queue)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        render_external_import_review_preflight_report(
            preflight,
            ready_preview,
            repair_queue,
            artifact_date=artifact_date,
        ),
        encoding="utf-8",
    )
    return preflight


def _git_ref_record(ref: str) -> dict[str, str | None]:
    try:
        raw = _git_output("show", "-s", "--format=%H%x00%cI%x00%s", ref)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"git_ref": ref, "commit": None, "committed_at": None, "subject": None}
    commit, committed_at, subject = raw.decode("utf-8").rstrip("\n").split("\x00", 2)
    return {
        "git_ref": ref,
        "commit": commit,
        "committed_at": committed_at,
        "subject": subject,
    }


def _mechanical_gate_for_blocked_row(row: dict[str, Any]) -> str:
    state = row.get("terminal_state")
    blockers = set(row.get("blockers") or [])
    if state == "needs_structural_duplicate_screen":
        return "current702_structural_duplicate_screen"
    if state == "needs_family_policy_review":
        return "family_policy_review"
    if state == "repairable_locator_blocker":
        return "source_free_locator_sidecar_materialization_or_linkage_repair"
    if state == "repairable_coordinate_blocker":
        return "coordinate_materialization_hash_or_path_reconciliation"
    if state == "duplicate_current702_conflict":
        return "current702_duplicate_reconciliation_or_reject"
    if state == "duplicate_external_conflict":
        if "sequence_hash_not_unique_in_preview" in blockers:
            return "preview_sequence_duplicate_reconciliation"
        return "external_duplicate_reconciliation_or_reject"
    if state == "reject/OOS_preserve_signal":
        return "preserve_out_of_scope_or_hard_negative_signal"
    return "source_retrieval_or_materialization_hard_blocker_clearance"


def _minimal_ready_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id"),
        "accession": row.get("accession"),
        "target_family_lane": row.get("target_family_lane"),
        "review_scope": row.get("review_scope"),
        "terminal_state": row.get("terminal_state"),
        "coordinate_path": row.get("coordinate_path"),
        "locator_sidecar_path": row.get("locator_sidecar_path"),
        "coordinate_hash_sha256": row.get("coordinate_hash_sha256"),
        "source_hashes": row.get("source_hashes"),
        "source_provenance": row.get("source_provenance"),
        "source_occurrences": row.get("source_occurrences"),
        "source_artifacts_consumed": row.get("source_artifacts_consumed"),
        "remaining_required_before_countable_import": [
            "single_controlled_human_batch_approval",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ],
    }


def _minimal_blocked_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id"),
        "accession": row.get("accession"),
        "target_family_lane": row.get("target_family_lane"),
        "review_scope": row.get("review_scope"),
        "terminal_state": row.get("terminal_state"),
        "blockers": row.get("blockers") or [],
        "mechanical_gate_needed": _mechanical_gate_for_blocked_row(row),
        "next_action": row.get("next_action"),
        "coordinate_path": row.get("coordinate_path"),
        "locator_sidecar_path": row.get("locator_sidecar_path"),
    }


def build_external_batch_import_approval_packet(
    preflight: dict[str, Any],
    ready_preview: dict[str, Any] | None = None,
    repair_queue: dict[str, Any] | None = None,
    *,
    created_utc: str | None = None,
    artifact_date: str | None = None,
    current_main_commit: str | None = None,
) -> dict[str, Any]:
    rows = [row for row in preflight.get("rows", []) if isinstance(row, dict)]
    ready_rows = [
        row for row in rows if row.get("terminal_state") == "controlled_import_review_ready"
    ]
    blocked_rows = [
        row for row in rows if row.get("terminal_state") != "controlled_import_review_ready"
    ]
    terminal_counts = Counter(str(row.get("terminal_state")) for row in rows)
    preview_terminal_counts = Counter(
        str(row.get("terminal_state"))
        for row in rows
        if row.get("review_scope") == "import_ready_preview"
    )
    repair_terminal_counts = Counter(
        str(row.get("terminal_state"))
        for row in rows
        if row.get("review_scope") == "materialization_repair_surface"
    )
    blocked_gate_counts = Counter(
        _mechanical_gate_for_blocked_row(row) for row in blocked_rows
    )
    ready_lane_counts = Counter(str(row.get("target_family_lane")) for row in ready_rows)
    repair_surface_rows = [
        row for row in rows if row.get("review_scope") == "materialization_repair_surface"
    ]
    mechanical_repair_audit = {
        "locator_sidecar_linked_repair_surface_rows": sum(
            1
            for row in repair_surface_rows
            if row.get("automated_checks", {}).get("locator_source_free_ready")
        ),
        "locator_sidecar_linked_but_coordinate_missing_rows": sum(
            1
            for row in repair_surface_rows
            if row.get("automated_checks", {}).get("locator_source_free_ready")
            and not row.get("automated_checks", {}).get("coordinate_materialized")
        ),
        "coordinate_hash_present_but_coordinate_path_unmaterialized_rows": sum(
            1
            for row in repair_surface_rows
            if row.get("automated_checks", {}).get("coordinate_hash_present")
            and not row.get("automated_checks", {}).get("coordinate_materialized")
        ),
        "duplicate_status_reconciled_to_terminal_conflict_rows": terminal_counts[
            "duplicate_current702_conflict"
        ]
        + terminal_counts["duplicate_external_conflict"],
        "terminal_state_normalization_total_rows": len(rows),
    }
    mechanical_repair_audit["count_normalization_reconciles"] = (
        mechanical_repair_audit["terminal_state_normalization_total_rows"]
        == preflight.get("counts", {}).get("review_surface_rows")
    )
    expected_ready_count = preflight.get("counts", {}).get(
        "controlled_import_review_ready"
    )
    expected_blocked_count = preflight.get("counts", {}).get("not_ready_rows")
    validation_checks = {
        "source_preflight_passed": bool(
            preflight.get("validation_checks", {}).get("passed")
        ),
        "ready_rows_match_preflight_count": len(ready_rows) == expected_ready_count,
        "blocked_rows_match_preflight_count": len(blocked_rows) == expected_blocked_count,
        "terminal_counts_reconcile": sum(terminal_counts.values()) == len(rows),
        "all_ready_rows_have_coordinate_hash": all(
            row.get("coordinate_hash_sha256") for row in ready_rows
        ),
        "all_ready_rows_have_locator_sidecar": all(
            row.get("locator_sidecar_path") for row in ready_rows
        ),
        "all_ready_rows_have_source_hashes": all(
            isinstance(row.get("source_hashes"), dict) and row.get("source_hashes")
            for row in ready_rows
        ),
        "all_ready_rows_have_source_provenance": all(
            isinstance(row.get("source_provenance"), dict)
            and row.get("source_provenance")
            for row in ready_rows
        ),
        "all_blocked_rows_have_mechanical_gate": all(
            _mechanical_gate_for_blocked_row(row) for row in blocked_rows
        ),
    }
    validation_checks["passed"] = all(validation_checks.values())
    packet = {
        "artifact_id": _batch_approval_artifact_id(artifact_date),
        "schema_version": "v3.external_batch_import_approval_packet",
        "created_utc": created_utc or preflight.get("created_utc") or _utc_now_iso(),
        "scope": (
            "Decision packet for one controlled batch approval over the Wave 2 "
            "external import-review preflight. It authorizes no production import "
            "or registry edit by itself."
        ),
        "current_main_commit_used": current_main_commit or _git_ref_record("HEAD")["commit"],
        "source_artifacts": {
            "preflight_artifact_id": preflight.get("artifact_id"),
            "preflight_artifact_sha256": preflight.get("artifact_sha256"),
            "ready_preview_artifact_id": (
                ready_preview or {}
            ).get("artifact_id"),
            "repair_queue_artifact_id": (
                repair_queue or {}
            ).get("artifact_id"),
        },
        "guardrails": {
            "decision_packet_only": True,
            "production_import_authorized_by_this_artifact": False,
            "label_import_performed": False,
            "production_registry_edited": False,
            "final_import_files_edited": False,
            "heldout_splits_edited": False,
            "production_thresholds_edited": False,
            "model_weights_edited": False,
            "ontology_edited": False,
            "review_only": True,
        },
        "batch_approval": {
            "rows_that_can_become_countable_after_one_batch_approval": len(ready_rows),
            "row_by_row_human_review_required_for_ready_rows": False,
            "blocked_rows_remaining": len(blocked_rows),
            "approval_statement": (
                f"One final controlled batch approval can advance {len(ready_rows)} "
                "machine-clean rows to countable import handling, provided the "
                "approval also records the label-factory gate and production "
                "registry-change authorization. This packet does not perform that import."
            ),
        },
        "terminal_state_counts": {
            state: terminal_counts.get(state, 0) for state in TERMINAL_STATES
        },
        "preview_terminal_state_counts": dict(sorted(preview_terminal_counts.items())),
        "repair_surface_terminal_state_counts": dict(sorted(repair_terminal_counts.items())),
        "ready_lane_counts": dict(sorted(ready_lane_counts.items())),
        "blocked_mechanical_gate_counts": dict(sorted(blocked_gate_counts.items())),
        "mechanical_nonproduction_reconciliation_audit": mechanical_repair_audit,
        "validation_checks": validation_checks,
        "ready_rows": [_minimal_ready_row(row) for row in ready_rows],
        "blocked_rows": [_minimal_blocked_row(row) for row in blocked_rows],
    }
    packet["artifact_sha256"] = _canonical_sha256(
        {key: value for key, value in packet.items() if key != "artifact_sha256"}
    )
    return packet


def render_external_batch_import_approval_packet_report(packet: dict[str, Any]) -> str:
    lines = [
        "# External Batch Import Approval Packet - current702",
        "",
        f"Created UTC: `{packet['created_utc']}`",
        "",
        "This is a decision packet only. It performs no production import, registry edit, ontology edit, split edit, threshold change, or model change.",
        "",
        "## Batch Decision",
        "",
        (
            "- Rows that can become countable after one controlled batch approval: "
            f"{packet['batch_approval']['rows_that_can_become_countable_after_one_batch_approval']}"
        ),
        f"- Blocked rows remaining: {packet['batch_approval']['blocked_rows_remaining']}",
        f"- Production import authorized here: {packet['guardrails']['production_import_authorized_by_this_artifact']}",
        "",
        packet["batch_approval"]["approval_statement"],
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in packet["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")
    lines.extend(["", "## Blocked Mechanical Gates", "", "| gate | rows |", "| --- | ---: |"])
    for gate, count in packet["blocked_mechanical_gate_counts"].items():
        lines.append(f"| `{gate}` | {count} |")
    lines.extend(
        [
            "",
            "## Mechanical Reconciliation Audit",
            "",
        ]
    )
    for key, value in packet["mechanical_nonproduction_reconciliation_audit"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Ready Lane Counts", "", "| lane | ready rows |", "| --- | ---: |"])
    for lane, count in packet["ready_lane_counts"].items():
        lines.append(f"| {lane} | {count} |")
    lines.extend(
        [
            "",
            "## Validation",
            "",
        ]
    )
    for key, value in packet["validation_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Blocked Row Sample",
            "",
            "| candidate | lane | terminal state | gate |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in packet["blocked_rows"][:40]:
        lines.append(
            "| `{}` | {} | `{}` | `{}` |".format(
                row["candidate_id"],
                row["target_family_lane"],
                row["terminal_state"],
                row["mechanical_gate_needed"],
            )
        )
    if len(packet["blocked_rows"]) > 40:
        lines.append(
            f"| ... | ... | ... | plus {len(packet['blocked_rows']) - 40} more rows |"
        )
    lines.append("")
    return "\n".join(lines)


def _normalize_lane_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def _lane_matches_family(lane: str, family: str) -> bool:
    normalized_lane = _normalize_lane_name(lane)
    normalized_family = _normalize_lane_name(family)
    return bool(
        normalized_lane
        and normalized_family
        and (
            normalized_lane in normalized_family
            or normalized_family in normalized_lane
        )
    )


def _aggregate_lane_counts(
    lane_terminal_counts: dict[str, dict[str, int]],
    family_or_lane: str,
) -> dict[str, Any]:
    matches = [
        lane for lane in lane_terminal_counts if _lane_matches_family(lane, family_or_lane)
    ]
    terminal_counts: Counter[str] = Counter()
    for lane in matches:
        terminal_counts.update(lane_terminal_counts[lane])
    return {
        "matching_lanes": matches,
        "review_surface_rows": sum(terminal_counts.values()),
        "controlled_import_review_ready": terminal_counts.get(
            "controlled_import_review_ready", 0
        ),
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
    }


def build_targeted_expansion_defense_ledger(
    preflight: dict[str, Any],
    approval_packet: dict[str, Any],
    *,
    previous_ledger: dict[str, Any] | None = None,
    created_utc: str | None = None,
    artifact_date: str | None = None,
    current_main_commit: str | None = None,
) -> dict[str, Any]:
    previous_ledger = previous_ledger or {}
    lane_terminal_counts = preflight.get("lane_terminal_state_counts") or {}
    prior_rationale = [
        row
        for row in previous_ledger.get("family_lane_rationale", [])
        if isinstance(row, dict)
    ]
    refreshed_rationale: list[dict[str, Any]] = []
    matched_lanes: set[str] = set()
    for row in prior_rationale:
        family = str(row.get("family_or_lane") or "")
        current_counts = _aggregate_lane_counts(lane_terminal_counts, family)
        matched_lanes.update(current_counts["matching_lanes"])
        refreshed = dict(row)
        refreshed["current_wave2_import_review_counts"] = current_counts
        refreshed_rationale.append(refreshed)
    for lane, terminal_counts in sorted(lane_terminal_counts.items()):
        if lane in matched_lanes:
            continue
        if terminal_counts.get("controlled_import_review_ready", 0) == 0:
            continue
        refreshed_rationale.append(
            {
                "family_or_lane": lane,
                "included_because": (
                    "Wave 2 preflight found machine-clean, source-provenanced "
                    "rows in this lane after duplicate, locator, and coordinate checks."
                ),
                "failure_mode_or_atlas_need": (
                    "Retain as a targeted import-review lane so batch approval "
                    "does not collapse distinct mechanisms into a random external pool."
                ),
                "current_wave2_import_review_counts": {
                    "matching_lanes": [lane],
                    "review_surface_rows": sum(terminal_counts.values()),
                    "controlled_import_review_ready": terminal_counts.get(
                        "controlled_import_review_ready", 0
                    ),
                    "terminal_state_counts": dict(sorted(terminal_counts.items())),
                },
                "supporting_artifacts": [
                    preflight.get("artifact_id"),
                    approval_packet.get("artifact_id"),
                ],
            }
        )

    previous_thesis = [
        item
        for item in previous_ledger.get("expansion_thesis", [])
        if isinstance(item, str)
        and "333" not in item
        and "845" not in item
        and "Wave 2 materialization" not in item
    ]
    expansion_thesis = previous_thesis + [
        (
            "The latest Wave 2 materialization/preflight surface contains 12,495 "
            "unique candidate rows: 600 preview rows and 11,895 repair-surface rows."
        ),
        (
            "The import-review preflight classifies 275 rows as controlled "
            "import-review ready, with all remaining rows routed to explicit "
            "duplicate, locator, coordinate, OOS, structural-screen, or hard-blocker gates."
        ),
        (
            "The selected families remain targeted because they map to prior "
            "failure modes: cofactor loss, fold/cofactor confounding, source-free "
            "locator gaps, near-orphan coverage, and external Swiss-Prot/AFDB/Rhea scalability."
        ),
    ]
    baseline_labels = (
        previous_ledger.get("count_table", {})
        .get("current_label_surface", {})
        .get("countable_labels", 702)
    )
    ready_count = approval_packet["batch_approval"][
        "rows_that_can_become_countable_after_one_batch_approval"
    ]
    projected_after_batch = baseline_labels + ready_count
    ledger = {
        "artifact_id": _defense_ledger_artifact_id(artifact_date),
        "schema_version": "v3.targeted_expansion_defense_ledger",
        "created_utc": created_utc or preflight.get("created_utc") or _utc_now_iso(),
        "scope": (
            "Review-ready defense ledger refreshed after Wave 2 import-review "
            "preflight; explains targeted family choice and label-closure state "
            "without performing imports."
        ),
        "current_main_commit_used": current_main_commit or _git_ref_record("HEAD")["commit"],
        "branch_provenance": [_git_ref_record("HEAD"), _git_ref_record("origin/main")],
        "source_artifacts": {
            "preflight_artifact_id": preflight.get("artifact_id"),
            "preflight_artifact_sha256": preflight.get("artifact_sha256"),
            "approval_packet_artifact_id": approval_packet.get("artifact_id"),
            "approval_packet_artifact_sha256": approval_packet.get("artifact_sha256"),
            "previous_defense_ledger_artifact_id": previous_ledger.get("artifact_id"),
        },
        "expansion_thesis": expansion_thesis,
        "family_lane_rationale": refreshed_rationale,
        "count_table": {
            "current_label_surface": {
                "countable_labels": baseline_labels,
                "source": "previous defense ledger/current702 frozen benchmark references",
            },
            "wave2_import_review_preflight": {
                "preview_rows": preflight["counts"]["preview_rows"],
                "repair_surface_rows": preflight["counts"]["repair_surface_rows"],
                "review_surface_rows": preflight["counts"]["review_surface_rows"],
                "terminal_state_counts": preflight["terminal_state_counts"],
            },
            "batch_approval_packet": {
                "rows_can_become_countable_after_one_batch_approval": ready_count,
                "blocked_rows_remaining": approval_packet["batch_approval"][
                    "blocked_rows_remaining"
                ],
                "blocked_mechanical_gate_counts": approval_packet[
                    "blocked_mechanical_gate_counts"
                ],
                "mechanical_nonproduction_reconciliation_audit": approval_packet[
                    "mechanical_nonproduction_reconciliation_audit"
                ],
            },
            "post_batch_projection": {
                "baseline_current702_countable_labels": baseline_labels,
                "if_one_batch_approval_accepts_ready_rows": projected_after_batch,
                "remaining_to_10000_after_that_batch": max(
                    0, 10000 - projected_after_batch
                ),
            },
        },
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "final_import_files_edited": False,
            "ontology_edited": False,
            "heldout_splits_edited": False,
            "production_thresholds_edited": False,
            "model_weights_edited": False,
            "preview_not_import": True,
            "source_free_coordinate_locator_requirements_preserved": True,
        },
        "review_narrative": {
            "honest_claims_for_review": [
                (
                    "Current main has a full Wave 2 materialization/preflight "
                    "surface of 12,495 unique external candidates."
                ),
                (
                    f"{ready_count} rows are machine-clean for one controlled "
                    "batch approval; they are not imported by this artifact."
                ),
                (
                    "The selected lanes are targeted by prior mechanism failure "
                    "modes and by lane-specific duplicate/locator/coordinate gates, not random sampling."
                ),
            ],
            "still_preview_or_provisional": [
                (
                    "Production import still requires an explicit controlled "
                    "batch approval, label-factory gate, and registry-change authorization."
                ),
                (
                    f"{approval_packet['batch_approval']['blocked_rows_remaining']} rows remain blocked "
                    "behind concrete mechanical or policy gates."
                ),
                (
                    "Exact coordinate/structure-ID screening is not a full "
                    "Foldseek/TM structural duplicate screen."
                ),
            ],
        },
        "validation_checks": {
            "preflight_validation_passed": bool(
                preflight.get("validation_checks", {}).get("passed")
            ),
            "approval_packet_validation_passed": bool(
                approval_packet.get("validation_checks", {}).get("passed")
            ),
            "terminal_counts_reconcile": sum(
                preflight.get("terminal_state_counts", {}).values()
            )
            == preflight["counts"]["review_surface_rows"],
            "batch_ready_count_matches_preflight": ready_count
            == preflight["counts"]["controlled_import_review_ready"],
            "family_rationale_present": bool(refreshed_rationale),
        },
    }
    ledger["validation_checks"]["passed"] = all(ledger["validation_checks"].values())
    ledger["artifact_sha256"] = _canonical_sha256(
        {key: value for key, value in ledger.items() if key != "artifact_sha256"}
    )
    return ledger


def render_targeted_expansion_defense_ledger_report(ledger: dict[str, Any]) -> str:
    count_table = ledger["count_table"]
    lines = [
        "# Targeted Expansion Defense Ledger - current702",
        "",
        f"Created UTC: `{ledger['created_utc']}`",
        "",
        "This ledger refreshes the targeted expansion review story after the Wave 2 import-review preflight. It is not an import artifact.",
        "",
        "## Count Ledger",
        "",
        "| surface | count | note |",
        "| --- | ---: | --- |",
        (
            "| Current countable labels | {} | Frozen current702 benchmark reference; "
            "unchanged by this packet. |"
        ).format(count_table["current_label_surface"]["countable_labels"]),
        (
            "| Wave 2 review surface | {} | 600 preview rows plus 11,895 repair-surface rows. |"
        ).format(count_table["wave2_import_review_preflight"]["review_surface_rows"]),
        (
            "| Controlled import-review ready | {} | Can move together after one final controlled batch approval. |"
        ).format(
            count_table["batch_approval_packet"][
                "rows_can_become_countable_after_one_batch_approval"
            ]
        ),
        (
            "| Blocked rows remaining | {} | Routed to concrete duplicate, locator, coordinate, OOS, structural, or hard-blocker gates. |"
        ).format(count_table["batch_approval_packet"]["blocked_rows_remaining"]),
        (
            "| Projected count after approval | {} | Projection only; no import performed here. |"
        ).format(
            count_table["post_batch_projection"][
                "if_one_batch_approval_accepts_ready_rows"
            ]
        ),
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in count_table["wave2_import_review_preflight"][
        "terminal_state_counts"
    ].items():
        lines.append(f"| `{state}` | {count} |")
    lines.extend(["", "## Blocked Mechanical Gates", "", "| gate | rows |", "| --- | ---: |"])
    for gate, count in count_table["batch_approval_packet"][
        "blocked_mechanical_gate_counts"
    ].items():
        lines.append(f"| `{gate}` | {count} |")
    lines.extend(["", "## Mechanical Reconciliation Audit", ""])
    for key, value in count_table["batch_approval_packet"][
        "mechanical_nonproduction_reconciliation_audit"
    ].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Family And Lane Rationale",
            "",
            "| family/lane | why targeted | current Wave 2 ready rows | current Wave 2 rows |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for row in ledger["family_lane_rationale"]:
        counts = row.get("current_wave2_import_review_counts", {})
        lines.append(
            "| `{}` | {} | {} | {} |".format(
                row.get("family_or_lane"),
                row.get("included_because"),
                counts.get("controlled_import_review_ready", 0),
                counts.get("review_surface_rows", 0),
            )
        )
    lines.extend(["", "## Guardrails", ""])
    for key, value in ledger["guardrails"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Review Narrative", "", "### Honest Claims", ""])
    for item in ledger["review_narrative"]["honest_claims_for_review"]:
        lines.append(f"- {item}")
    lines.extend(["", "### Still Preview Or Provisional", ""])
    for item in ledger["review_narrative"]["still_preview_or_provisional"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Validation", ""])
    for key, value in ledger["validation_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    return "\n".join(lines)


def write_external_import_closure_packet(
    *,
    preview_source: str | Path = DEFAULT_PREVIEW_SOURCE,
    merged_surface_source: str | Path | None = DEFAULT_MERGED_SURFACE_SOURCE,
    materialization_source: str | Path = DEFAULT_MATERIALIZATION_SOURCE,
    repair_surface_source: str | Path | None = DEFAULT_REPAIR_SURFACE_SOURCE,
    current702_coordinate_manifest_path: str | Path = DEFAULT_CURRENT702_COORDINATE_MANIFEST_PATH,
    preflight_path: Path = DEFAULT_OUT_PATH,
    ready_preview_path: Path = DEFAULT_READY_PREVIEW_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    preflight_report_path: Path = DEFAULT_REPORT_PATH,
    batch_packet_path: Path = DEFAULT_BATCH_APPROVAL_PACKET_PATH,
    batch_report_path: Path = DEFAULT_BATCH_APPROVAL_REPORT_PATH,
    defense_ledger_path: Path = DEFAULT_DEFENSE_LEDGER_PATH,
    defense_ledger_report_path: Path = DEFAULT_DEFENSE_LEDGER_REPORT_PATH,
    previous_defense_ledger_path: Path | None = DEFAULT_PREVIOUS_DEFENSE_LEDGER_PATH,
    tree_refs: tuple[str, ...] = DEFAULT_TREE_REFS,
    expected_preview_count: int = 600,
    expected_repair_count: int | None = 11895,
    expected_review_surface_count: int | None = 12495,
    created_utc: str | None = None,
    artifact_date: str | None = None,
) -> dict[str, Any]:
    preflight = write_external_import_review_preflight(
        preview_source=preview_source,
        merged_surface_source=merged_surface_source,
        materialization_source=materialization_source,
        repair_surface_source=repair_surface_source,
        current702_coordinate_manifest_path=current702_coordinate_manifest_path,
        out_path=preflight_path,
        ready_preview_path=ready_preview_path,
        repair_queue_path=repair_queue_path,
        report_path=preflight_report_path,
        tree_refs=tree_refs,
        expected_preview_count=expected_preview_count,
        expected_repair_count=expected_repair_count,
        expected_review_surface_count=expected_review_surface_count,
        created_utc=created_utc,
        artifact_date=artifact_date,
    )
    ready_preview = json.loads(ready_preview_path.read_text(encoding="utf-8"))
    repair_queue = json.loads(repair_queue_path.read_text(encoding="utf-8"))
    current_commit = _git_ref_record("HEAD")["commit"]
    packet = build_external_batch_import_approval_packet(
        preflight,
        ready_preview,
        repair_queue,
        created_utc=preflight["created_utc"],
        artifact_date=artifact_date,
        current_main_commit=current_commit,
    )
    _write_json(batch_packet_path, packet)
    batch_report_path.parent.mkdir(parents=True, exist_ok=True)
    batch_report_path.write_text(
        render_external_batch_import_approval_packet_report(packet),
        encoding="utf-8",
    )
    previous_ledger: dict[str, Any] | None = None
    if previous_defense_ledger_path and previous_defense_ledger_path.exists():
        previous_ledger = json.loads(previous_defense_ledger_path.read_text(encoding="utf-8"))
    ledger = build_targeted_expansion_defense_ledger(
        preflight,
        packet,
        previous_ledger=previous_ledger,
        created_utc=preflight["created_utc"],
        artifact_date=artifact_date,
        current_main_commit=current_commit,
    )
    _write_json(defense_ledger_path, ledger)
    defense_ledger_report_path.parent.mkdir(parents=True, exist_ok=True)
    defense_ledger_report_path.write_text(
        render_targeted_expansion_defense_ledger_report(ledger),
        encoding="utf-8",
    )
    return {
        "preflight": preflight,
        "ready_preview": ready_preview,
        "repair_queue": repair_queue,
        "batch_approval_packet": packet,
        "defense_ledger": ledger,
    }
