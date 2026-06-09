from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_DATE = "20260608"
ARTIFACT_ID = f"v3_external_admission_merged_surface_current702_{RUN_DATE}"
IMPORT_READY_ARTIFACT_ID = (
    f"v3_external_admission_import_ready_preview_current702_{RUN_DATE}"
)
REPAIR_QUEUE_ARTIFACT_ID = (
    f"v3_external_admission_repair_queue_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_admission_merged_surface"
IMPORT_READY_SCHEMA_VERSION = "v3.external_admission_import_ready_preview"
REPAIR_QUEUE_SCHEMA_VERSION = "v3.external_admission_repair_queue"

DEFAULT_VALIDATION_PATH = Path(
    "artifacts/v3_external_source_admission_validation_16_current702_20260608.json"
)
DEFAULT_BULK_SCOUT_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json"
)
DEFAULT_BULK_PREVIEW_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json"
)
DEFAULT_SCALEOUT_MERGED_PATH = Path(
    "artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json"
)
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_external_admission_merged_surface_current702_{RUN_DATE}.json"
)
DEFAULT_IMPORT_READY_PATH = Path(
    f"artifacts/v3_external_admission_import_ready_preview_current702_{RUN_DATE}.json"
)
DEFAULT_REPAIR_QUEUE_PATH = Path(
    f"artifacts/v3_external_admission_repair_queue_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/external_admission_qa_merger_current702_{RUN_DATE}.md"
)

REPAIRABLE_TERMINAL_STATES = {
    "admission_ready_pending_coordinate_materialization",
    "admission_ready_pending_locator_materialization",
    "coordinate_repair_candidate",
    "locator_repair_candidate",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": sha256_path(path),
        "bytes": path.stat().st_size,
    }


def _normalize_accession(value: Any) -> str:
    text = str(value or "").strip()
    return text.split(":", 1)[1] if text.startswith("uniprot:") else text


def _normalize_key(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    return text or None


def _build_scaleout_index(scaleout_payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for canonical in scaleout_payload.get("canonical_records", []) or []:
        canonical_key = str(canonical.get("canonical_key") or "")
        canonical_terminal_state = str(canonical.get("canonical_terminal_state") or "")
        for member in canonical.get("source_members", []) or []:
            if not isinstance(member, dict):
                continue
            for raw_value in (
                member.get("accession"),
                member.get("candidate_id"),
                member.get("entry_id"),
            ):
                key = _normalize_key(_normalize_accession(raw_value))
                if not key:
                    continue
                index[key].append(
                    {
                        "canonical_key": canonical_key,
                        "canonical_terminal_state": canonical_terminal_state,
                    }
                )
    return {key: value for key, value in index.items()}


def _watch_status(label: str, pattern: str) -> dict[str, Any]:
    matches = sorted(str(path) for path in Path("artifacts").glob(pattern))
    return {
        "automation_id": label,
        "status": "present_in_current_main_state" if matches else "missing_in_current_main_state",
        "artifact_paths": matches,
    }


def _current_registry_conflict(row: dict[str, Any]) -> bool:
    duplicate_status = row.get("duplicate_status")
    if isinstance(duplicate_status, dict):
        recomputed = duplicate_status.get("recomputed_current_registry_duplicate_status")
        if isinstance(recomputed, dict):
            return bool(recomputed.get("duplicate_or_current_registry_conflict"))
        artifact = duplicate_status.get("artifact_duplicate_status")
        if isinstance(artifact, dict):
            return bool(artifact.get("duplicate_or_current_registry_conflict"))
    duplicate_summary = row.get("duplicate_status_summary")
    if isinstance(duplicate_summary, dict):
        return bool(duplicate_summary.get("blocked_by_duplicate_or_current_registry_conflict"))
    blocker_basis = row.get("blocker_basis")
    if isinstance(blocker_basis, dict):
        return bool(blocker_basis.get("duplicate_or_current_registry_conflict"))
    return False


def _remaining_requirements(row: dict[str, Any]) -> list[str]:
    terminal_state = row["terminal_state"]
    if terminal_state == "admission_ready_external_label_candidate":
        return [
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state == "admission_ready_pending_coordinate_materialization":
        return [
            "coordinate_materialization_or_hash_match",
            "source_free_locator_materialization",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state == "admission_ready_pending_locator_materialization":
        return [
            "source_free_locator_materialization",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state == "provisional_external_countable_preflight_candidate":
        return [
            "scaled_external_admission_validation",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state == "locator_ready_candidate":
        return [
            "coordinate_materialization_or_hash_match",
            "scaled_external_admission_validation",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state == "coordinate_ready_pending_locator":
        return [
            "source_free_locator_materialization",
            "scaled_external_admission_validation",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    if terminal_state in {"coordinate_repair_candidate", "locator_repair_candidate"}:
        return [
            "explicit_repair_lane",
            "scaled_external_admission_validation",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    return []


def _repair_bucket(row: dict[str, Any]) -> str | None:
    terminal_state = row["terminal_state"]
    if terminal_state == "admission_ready_pending_coordinate_materialization":
        return "coordinate_materialization"
    if terminal_state == "admission_ready_pending_locator_materialization":
        return "locator_materialization"
    if terminal_state == "coordinate_repair_candidate":
        return "coordinate_repair"
    if terminal_state == "locator_repair_candidate":
        return "locator_repair"
    return None


def _merge_validation_row(
    validation_row: dict[str, Any],
    bulk_row: dict[str, Any],
    scaleout_hits: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    for key in ("stable_candidate_key", "accession", "lane_id", "target_family_lane"):
        if validation_row.get(key) != bulk_row.get(key):
            issues.append(f"validation_bulk_{key}_mismatch")
    for key in (
        "uniprot_search_row_sha256",
        "uniprot_entry_record_sha256",
        "rhea_records_sha256",
    ):
        if validation_row.get("source_hashes", {}).get(key) != bulk_row.get("source_hashes", {}).get(key):
            issues.append(f"validation_bulk_{key}_mismatch")

    merged = dict(validation_row)
    merged["merge_status"] = "validated_upgrade_from_bulk_provisional"
    merged["bulk_terminal_state"] = bulk_row.get("terminal_state")
    merged["bulk_duplicate_status_summary"] = bulk_row.get("duplicate_status_summary")
    merged["bulk_exact_next_action"] = bulk_row.get("exact_next_action")
    merged["remaining_required_before_import"] = _remaining_requirements(merged)
    merged["ready_for_import_preview"] = (
        merged["terminal_state"] == "admission_ready_external_label_candidate"
        and not _current_registry_conflict(merged)
        and not merged["remaining_required_before_import"]
    )
    merged["repair_bucket"] = _repair_bucket(merged)
    merged["provenance_audit"] = {
        "validation_bulk_crosscheck_passed": not issues,
        "validation_bulk_crosscheck_issues": issues,
        "bulk_row_sha256": _canonical_sha256(bulk_row),
        "validation_row_sha256": _canonical_sha256(validation_row),
    }
    merged["scaleout_overlap"] = {
        "overlap_count": len(scaleout_hits),
        "overlaps_current_main_scaleout_surface": bool(scaleout_hits),
        "records": scaleout_hits[:10],
    }
    return merged, issues


def _merge_bulk_only_row(
    bulk_row: dict[str, Any], scaleout_hits: list[dict[str, Any]]
) -> dict[str, Any]:
    merged = dict(bulk_row)
    merged["merge_status"] = "bulk_only_candidate"
    merged["remaining_required_before_import"] = _remaining_requirements(merged)
    merged["ready_for_import_preview"] = False
    merged["repair_bucket"] = _repair_bucket(merged)
    merged["scaleout_overlap"] = {
        "overlap_count": len(scaleout_hits),
        "overlaps_current_main_scaleout_surface": bool(scaleout_hits),
        "records": scaleout_hits[:10],
    }
    return merged


def build_external_admission_merged_surface(
    *,
    validation_payload: dict[str, Any],
    bulk_scout_payload: dict[str, Any],
    bulk_preview_payload: dict[str, Any],
    scaleout_merged_payload: dict[str, Any],
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    validation_rows = validation_payload.get("rows", []) or []
    bulk_rows = bulk_scout_payload.get("rows", []) or []
    bulk_preview_rows = bulk_preview_payload.get("rows", []) or []
    scaleout_index = _build_scaleout_index(scaleout_merged_payload)
    validation_by_id = {row["candidate_id"]: row for row in validation_rows}
    bulk_preview_ids = {row["candidate_id"] for row in bulk_preview_rows}

    merged_rows: list[dict[str, Any]] = []
    issues: list[str] = []
    validation_upgrades = 0
    bulk_only_rows = 0

    seen_candidate_ids: set[str] = set()
    seen_stable_keys: set[str] = set()

    for bulk_row in bulk_rows:
        candidate_id = str(bulk_row["candidate_id"])
        stable_key = str(bulk_row["stable_candidate_key"])
        if candidate_id in seen_candidate_ids:
            issues.append(f"duplicate_candidate_id:{candidate_id}")
            continue
        if stable_key in seen_stable_keys:
            issues.append(f"duplicate_stable_candidate_key:{stable_key}")
            continue
        seen_candidate_ids.add(candidate_id)
        seen_stable_keys.add(stable_key)

        accession_key = _normalize_key(_normalize_accession(bulk_row.get("accession")))
        scaleout_hits = scaleout_index.get(accession_key or "", [])

        if candidate_id in validation_by_id:
            validation_upgrades += 1
            merged_row, row_issues = _merge_validation_row(
                validation_by_id[candidate_id],
                bulk_row,
                scaleout_hits,
            )
            issues.extend(f"{candidate_id}:{issue}" for issue in row_issues)
        else:
            bulk_only_rows += 1
            merged_row = _merge_bulk_only_row(bulk_row, scaleout_hits)
        merged_rows.append(merged_row)

    missing_validation_ids = sorted(set(validation_by_id) - seen_candidate_ids)
    if missing_validation_ids:
        issues.extend(f"validation_row_missing_from_bulk:{candidate_id}" for candidate_id in missing_validation_ids)

    provisional_ids = {
        row["candidate_id"]
        for row in bulk_rows
        if row.get("terminal_state") == "provisional_external_countable_preflight_candidate"
    }
    if not bulk_preview_ids.issubset(provisional_ids):
        issues.append("bulk_preview_candidate_ids_not_subset_of_bulk_provisional_rows")
    if len(bulk_preview_ids) != bulk_preview_payload.get("candidate_count"):
        issues.append("bulk_preview_candidate_count_mismatch")

    terminal_state_counts = dict(
        sorted(Counter(row["terminal_state"] for row in merged_rows).items())
    )
    lane_terminal_state_counts: dict[str, dict[str, int]] = {}
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in merged_rows:
        grouped[str(row["target_family_lane"])][str(row["terminal_state"])] += 1
    for lane, counts in sorted(grouped.items()):
        lane_terminal_state_counts[lane] = dict(sorted(counts.items()))

    repair_queue_rows = [
        row for row in merged_rows if row["terminal_state"] in REPAIRABLE_TERMINAL_STATES
    ]
    import_ready_rows = [row for row in merged_rows if row["ready_for_import_preview"]]
    blocked_rows = [
        row
        for row in merged_rows
        if row["terminal_state"] == "blocked_duplicate_or_current_registry_conflict"
    ]
    scaleout_overlap_rows = [
        row for row in merged_rows if row["scaleout_overlap"]["overlaps_current_main_scaleout_surface"]
    ]

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "counts": {
            "merged_rows": len(merged_rows),
            "validation_upgrade_rows": validation_upgrades,
            "bulk_only_rows": bulk_only_rows,
            "import_ready_rows": len(import_ready_rows),
            "repair_queue_rows": len(repair_queue_rows),
            "blocked_duplicate_or_current_registry_conflict_rows": len(blocked_rows),
            "scaleout_overlap_rows": len(scaleout_overlap_rows),
        },
        "terminal_state_counts": terminal_state_counts,
        "lane_terminal_state_counts": lane_terminal_state_counts,
        "producer_watch": {
            "ce_external_materialization_admission_batch": _watch_status(
                "ce-external-materialization-admission-batch",
                "v3_external*materialization*admission*batch*.json",
            ),
            "ce_external_bulk_pagination_scaleout": _watch_status(
                "ce-external-bulk-pagination-scaleout",
                "v3_external*bulk*pagination*scaleout*.json",
            ),
        },
        "validation_checks": {
            "passed": not issues,
            "issues": issues,
            "bulk_candidate_count_matches_rows": bulk_scout_payload.get("candidate_count")
            == len(bulk_rows),
            "validation_candidate_count_matches_rows": validation_payload.get("counts", {}).get("validated_rows")
            == len(validation_rows),
            "bulk_preview_candidate_count_matches_rows": bulk_preview_payload.get("candidate_count")
            == len(bulk_preview_rows),
        },
        "source_artifact_reconciliation": {
            "validation_rows": len(validation_rows),
            "bulk_rows": len(bulk_rows),
            "bulk_preview_rows": len(bulk_preview_rows),
            "validation_ids_missing_from_bulk": missing_validation_ids,
            "bulk_preview_ids_outside_bulk_provisional_rows": sorted(bulk_preview_ids - provisional_ids),
        },
        "guardrails": {
            "production_registry_edited": False,
            "label_import_performed": False,
            "final_import_files_edited": False,
        },
        "rows": merged_rows,
    }


def build_external_admission_import_ready_preview(
    merged_surface: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or merged_surface.get("created_utc") or _utc_now_iso()
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "stable_candidate_key": row["stable_candidate_key"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "ready_for_production_label_import": False,
            "remaining_required_before_import": row["remaining_required_before_import"],
            "source_hashes": row.get("source_hashes"),
            "source_provenance": row.get("source_provenance"),
            "merge_status": row["merge_status"],
            "scaleout_overlap": row["scaleout_overlap"],
        }
        for row in merged_surface.get("rows", [])
        if row.get("ready_for_import_preview")
    ]
    return {
        "artifact_id": IMPORT_READY_ARTIFACT_ID,
        "schema_version": IMPORT_READY_SCHEMA_VERSION,
        "created_utc": created,
        "candidate_count": len(rows),
        "source_artifact_id": merged_surface.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(merged_surface),
        "guardrails": {
            "preview_only": True,
            "production_registry_edited": False,
            "label_import_performed": False,
        },
        "rows": rows,
    }


def build_external_admission_repair_queue(
    merged_surface: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or merged_surface.get("created_utc") or _utc_now_iso()
    rows = [
        {
            "candidate_id": row["candidate_id"],
            "stable_candidate_key": row["stable_candidate_key"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "repair_bucket": row["repair_bucket"],
            "exact_next_action": row.get("exact_next_action"),
            "remaining_required_before_import": row["remaining_required_before_import"],
            "merge_status": row["merge_status"],
            "source_hashes": row.get("source_hashes"),
            "source_provenance": row.get("source_provenance"),
        }
        for row in merged_surface.get("rows", [])
        if row.get("repair_bucket")
    ]
    return {
        "artifact_id": REPAIR_QUEUE_ARTIFACT_ID,
        "schema_version": REPAIR_QUEUE_SCHEMA_VERSION,
        "created_utc": created,
        "candidate_count": len(rows),
        "source_artifact_id": merged_surface.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(merged_surface),
        "guardrails": {
            "queue_only": True,
            "production_registry_edited": False,
            "label_import_performed": False,
        },
        "rows": rows,
    }


def render_external_admission_qa_merger_report(
    merged_surface: dict[str, Any],
    import_ready_preview: dict[str, Any],
    repair_queue: dict[str, Any],
) -> str:
    counts = merged_surface["counts"]
    lines = [
        "# External Admission QA Merger - current702",
        "",
        "Merged the durable external admission surfaces by upgrading the 16-row "
        "validated admission slice over the bulk scout baseline, auditing "
        "provenance/hash continuity, and separating repairable rows into an "
        "explicit queue without touching production registries or final import files.",
        "",
        "## Summary",
        "",
        f"- Merged rows: {counts['merged_rows']}",
        f"- Validation upgrades: {counts['validation_upgrade_rows']}",
        f"- Bulk-only rows: {counts['bulk_only_rows']}",
        f"- Import-ready preview rows: {import_ready_preview['candidate_count']}",
        f"- Repair-queue rows: {repair_queue['candidate_count']}",
        f"- Scaleout-overlap audit rows: {counts['scaleout_overlap_rows']}",
        f"- Validation passed: {merged_surface['validation_checks']['passed']}",
        "",
        "## Producer Watch",
        "",
    ]
    for value in merged_surface["producer_watch"].values():
        lines.append(
            f"- `{value['automation_id']}`: `{value['status']}` "
            f"({len(value['artifact_paths'])} artifact(s))"
        )

    lines.extend(["", "## Terminal State Counts", "", "| terminal state | count |", "| --- | ---: |"])
    for state, count in merged_surface["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    lines.extend(["", "## Lane Counts", "", "| family/lane | terminal state | count |", "| --- | --- | ---: |"])
    for lane, lane_counts in merged_surface["lane_terminal_state_counts"].items():
        for state, count in lane_counts.items():
            lines.append(f"| {lane} | `{state}` | {count} |")

    lines.extend(
        [
            "",
            "## Import-Ready Preview",
            "",
            f"- Candidate rows: `{import_ready_preview['candidate_count']}`",
        ]
    )
    if import_ready_preview["candidate_count"] == 0:
        lines.append(
            "- No row is import-ready yet. The validated rows still need "
            "coordinate and/or locator materialization, and bulk-only rows still "
            "need scaled admission validation plus downstream duplicate and review gates."
        )

    lines.extend(
        [
            "",
            "## Repair Queue",
            "",
            "| candidate | lane | terminal state | repair bucket | next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in repair_queue["rows"][:25]:
        next_action = str(row.get("exact_next_action") or "").replace("|", "\\|")
        lines.append(
            f"| `{row['candidate_id']}` | {row['target_family_lane']} | "
            f"`{row['terminal_state']}` | `{row['repair_bucket']}` | {next_action} |"
        )
    if len(repair_queue["rows"]) > 25:
        lines.append(
            f"| ... | ... | ... | ... | plus {len(repair_queue['rows']) - 25} more repair rows |"
        )

    return "\n".join(lines) + "\n"


def write_external_admission_qa_merger(
    *,
    validation_path: Path = DEFAULT_VALIDATION_PATH,
    bulk_scout_path: Path = DEFAULT_BULK_SCOUT_PATH,
    bulk_preview_path: Path = DEFAULT_BULK_PREVIEW_PATH,
    scaleout_merged_path: Path = DEFAULT_SCALEOUT_MERGED_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    import_ready_path: Path = DEFAULT_IMPORT_READY_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    created_utc: str | None = None,
) -> dict[str, Any]:
    merged_surface = build_external_admission_merged_surface(
        validation_payload=_read_json(validation_path),
        bulk_scout_payload=_read_json(bulk_scout_path),
        bulk_preview_payload=_read_json(bulk_preview_path),
        scaleout_merged_payload=_read_json(scaleout_merged_path),
        created_utc=created_utc,
    )
    merged_surface["source_artifacts"] = {
        "external_source_admission_validation": _source_record(validation_path),
        "external_bulk_ingestion_scout": _source_record(bulk_scout_path),
        "external_bulk_ingestion_provisional_import_preview": _source_record(
            bulk_preview_path
        ),
        "scaleout_merged_acceptance_surface": _source_record(scaleout_merged_path),
    }
    import_ready_preview = build_external_admission_import_ready_preview(merged_surface)
    repair_queue = build_external_admission_repair_queue(merged_surface)
    import_ready_preview["source_artifacts"] = {
        "external_admission_merged_surface": _source_record(out_path)
        if out_path.exists()
        else None
    }
    repair_queue["source_artifacts"] = {
        "external_admission_merged_surface": _source_record(out_path)
        if out_path.exists()
        else None
    }
    _write_json(out_path, merged_surface)
    import_ready_preview["source_artifacts"] = {
        "external_admission_merged_surface": _source_record(out_path)
    }
    repair_queue["source_artifacts"] = {
        "external_admission_merged_surface": _source_record(out_path)
    }
    _write_json(import_ready_path, import_ready_preview)
    _write_json(repair_queue_path, repair_queue)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_admission_qa_merger_report(
                merged_surface,
                import_ready_preview,
                repair_queue,
            ),
            encoding="utf-8",
        )
    return merged_surface
