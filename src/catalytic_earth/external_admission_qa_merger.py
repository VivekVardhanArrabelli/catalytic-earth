from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_DATE = "20260609"
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

DEFAULT_MATERIALIZATION_BATCH_SPEC = (
    "origin/ce-external-materialization-admission-batch-20260608:"
    "artifacts/v3_external_materialization_admission_batch_current702_20260608.json"
)
DEFAULT_MATERIALIZATION_PREVIEW_SPEC = (
    "origin/ce-external-materialization-admission-batch-20260608:"
    "artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json"
)
DEFAULT_BULK_SCALEOUT_SPEC = (
    "origin/ce-external-bulk-pagination-scaleout-20260609:"
    "artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json"
)
DEFAULT_BULK_PREVIEW_SPEC = (
    "origin/ce-external-bulk-pagination-scaleout-20260609:"
    "artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_current702_20260609.json"
)
DEFAULT_PREVIOUS_MERGED_SURFACE_SPEC = (
    "origin/ce-external-admission-qa-merger-20260608:"
    "artifacts/v3_external_admission_merged_surface_current702_20260608.json"
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
    "coordinate_repair_candidate",
    "locator_repair_candidate",
    "repairable_locator_blocker",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_json_source(source_spec: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    if isinstance(source_spec, Path):
        path = source_spec
        text = path.read_text(encoding="utf-8")
        return json.loads(text), {
            "source_type": "local_path",
            "path": str(path),
            "bytes": len(text.encode("utf-8")),
            "sha256": _sha256_text(text),
        }

    spec_text = str(source_spec)
    local_path = Path(spec_text)
    if local_path.exists():
        text = local_path.read_text(encoding="utf-8")
        return json.loads(text), {
            "source_type": "local_path",
            "path": str(local_path),
            "bytes": len(text.encode("utf-8")),
            "sha256": _sha256_text(text),
        }

    if ":" not in spec_text:
        raise FileNotFoundError(f"unsupported source spec: {spec_text}")

    git_ref, artifact_path = spec_text.split(":", 1)
    text = subprocess.check_output(["git", "show", spec_text], text=True)
    commit = subprocess.check_output(["git", "rev-parse", git_ref], text=True).strip()
    return json.loads(text), {
        "source_type": "git_ref_path",
        "git_ref": git_ref,
        "git_commit": commit,
        "artifact_path": artifact_path,
        "spec": spec_text,
        "bytes": len(text.encode("utf-8")),
        "sha256": _sha256_text(text),
    }


def _current702_conflict_from_bulk(row: dict[str, Any]) -> bool:
    summary = row.get("duplicate_status_summary", {})
    return (
        summary.get("current702_status")
        != "no_exact_current702_accession_or_sequence_sha_overlap"
    )


def _external_duplicate_from_bulk(row: dict[str, Any]) -> bool:
    summary = row.get("duplicate_status_summary", {})
    return (
        summary.get("external_pilot_status")
        != "no_exact_external_pilot_accession_or_sequence_sha_overlap"
    )


def _current702_conflict_from_materialization(row: dict[str, Any]) -> bool:
    duplicate_status = row.get("duplicate_status", {})
    return bool(duplicate_status.get("duplicate_or_current_registry_conflict"))


def _repair_bucket(row: dict[str, Any]) -> str | None:
    terminal_state = str(row.get("terminal_state") or "")
    if terminal_state == "coordinate_repair_candidate":
        return "coordinate_repair"
    if terminal_state in {"locator_repair_candidate", "repairable_locator_blocker"}:
        return "locator_repair"
    return None


def _remaining_required_before_import(row: dict[str, Any]) -> list[str]:
    terminal_state = str(row.get("terminal_state") or "")
    if terminal_state == "import_ready_preview":
        return [
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    if terminal_state == "repairable_locator_blocker":
        return [
            "locator_sidecar_materialization_repair",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    if terminal_state == "provisional_external_countable_preflight_candidate":
        return [
            "materialization_lane",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    if terminal_state == "coordinate_ready_pending_locator":
        return [
            "locator_sidecar_materialization",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    if terminal_state == "locator_ready_candidate":
        return [
            "coordinate_materialization",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    if terminal_state in {"coordinate_repair_candidate", "locator_repair_candidate"}:
        return [
            "explicit_repair_lane",
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "controlled_import_review_lane_approval",
            "production_registry_change_authorization",
        ]
    return []


def _materialization_queue_name(row: dict[str, Any]) -> str:
    return str(row.get("queue_name") or "")


def _merge_materialized_row(
    bulk_row: dict[str, Any],
    materialization_row: dict[str, Any],
) -> dict[str, Any]:
    merged = dict(bulk_row)
    merged.update(materialization_row)
    queue_name = _materialization_queue_name(materialization_row)
    merged["bulk_terminal_state"] = bulk_row.get("terminal_state")
    merged["bulk_duplicate_status_summary"] = bulk_row.get("duplicate_status_summary")
    merged["bulk_exact_next_action"] = bulk_row.get("exact_next_action")
    merged["materialization_queue_name"] = queue_name
    merged["merge_status"] = (
        "materialized_from_validated_queue"
        if queue_name == "validated_ready_preview"
        else "materialized_from_provisional_queue"
    )
    merged["repair_bucket"] = _repair_bucket(merged)
    merged["remaining_required_before_import"] = _remaining_required_before_import(merged)
    merged["current702_conflict"] = _current702_conflict_from_materialization(merged)
    merged["external_duplicate_conflict"] = _external_duplicate_from_bulk(bulk_row)
    merged["ready_for_import_preview"] = (
        merged["terminal_state"] == "import_ready_preview"
        and not merged["current702_conflict"]
    )
    merged["controlled_import_review_lane_ready"] = merged["ready_for_import_preview"]
    merged["provenance_audit"] = {
        "source_provenance_present": bool(merged.get("source_provenance")),
        "source_hashes_present": bool(merged.get("source_hashes")),
        "bulk_row_sha256": _canonical_sha256(bulk_row),
        "materialization_row_sha256": _canonical_sha256(materialization_row),
        "input_preview_terminal_state": materialization_row.get(
            "input_preview_terminal_state"
        ),
    }
    return merged


def _merge_bulk_only_row(bulk_row: dict[str, Any]) -> dict[str, Any]:
    merged = dict(bulk_row)
    merged["merge_status"] = "scaleout_bulk_only_candidate"
    merged["repair_bucket"] = _repair_bucket(merged)
    merged["remaining_required_before_import"] = _remaining_required_before_import(merged)
    merged["current702_conflict"] = _current702_conflict_from_bulk(merged)
    merged["external_duplicate_conflict"] = _external_duplicate_from_bulk(merged)
    merged["ready_for_import_preview"] = False
    merged["controlled_import_review_lane_ready"] = False
    merged["provenance_audit"] = {
        "source_provenance_present": bool(merged.get("source_provenance")),
        "source_hashes_present": bool(merged.get("source_hashes")),
        "bulk_row_sha256": _canonical_sha256(bulk_row),
    }
    return merged


def build_external_admission_merged_surface(
    *,
    materialization_payload: dict[str, Any],
    materialization_preview_payload: dict[str, Any],
    bulk_scaleout_payload: dict[str, Any],
    bulk_preview_payload: dict[str, Any],
    previous_merged_surface_payload: dict[str, Any] | None = None,
    source_artifacts: dict[str, Any] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    bulk_rows = bulk_scaleout_payload.get("rows", []) or []
    materialization_rows = materialization_payload.get("rows", []) or []
    materialization_by_id = {
        str(row["candidate_id"]): row for row in materialization_rows if isinstance(row, dict)
    }
    previous_ids = {
        str(row["candidate_id"])
        for row in (previous_merged_surface_payload or {}).get("rows", []) or []
        if isinstance(row, dict) and row.get("candidate_id")
    }

    merged_rows: list[dict[str, Any]] = []
    seen_candidate_ids: set[str] = set()
    issues: list[str] = []
    merge_status_counts: Counter[str] = Counter()
    materialized_from_queue_counts: Counter[str] = Counter()

    for bulk_row in bulk_rows:
        candidate_id = str(bulk_row["candidate_id"])
        if candidate_id in seen_candidate_ids:
            issues.append(f"duplicate_candidate_id:{candidate_id}")
            continue
        seen_candidate_ids.add(candidate_id)
        materialization_row = materialization_by_id.get(candidate_id)
        if materialization_row is not None:
            merged_row = _merge_materialized_row(bulk_row, materialization_row)
            materialized_from_queue_counts[merged_row["materialization_queue_name"]] += 1
        else:
            merged_row = _merge_bulk_only_row(bulk_row)
        merge_status_counts[merged_row["merge_status"]] += 1
        merged_rows.append(merged_row)

    materialization_only_ids = sorted(set(materialization_by_id) - seen_candidate_ids)
    if materialization_only_ids:
        issues.extend(
            f"materialization_row_missing_from_bulk_scaleout:{candidate_id}"
            for candidate_id in materialization_only_ids
        )

    terminal_state_counts = dict(
        sorted(Counter(str(row["terminal_state"]) for row in merged_rows).items())
    )
    lane_terminal_state_counts: dict[str, dict[str, int]] = {}
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in merged_rows:
        grouped[str(row["target_family_lane"])][str(row["terminal_state"])] += 1
    for lane, counts in sorted(grouped.items()):
        lane_terminal_state_counts[lane] = dict(sorted(counts.items()))

    import_ready_rows = [row for row in merged_rows if row["ready_for_import_preview"]]
    repair_queue_rows = [row for row in merged_rows if row["repair_bucket"]]
    duplicate_blocked_rows = [
        row
        for row in merged_rows
        if row["terminal_state"] == "blocked_duplicate_or_current_registry_conflict"
    ]
    current702_conflict_rows = [row for row in merged_rows if row["current702_conflict"]]
    external_duplicate_rows = [
        row for row in merged_rows if row["external_duplicate_conflict"]
    ]
    newly_added_by_scaleout = [
        row for row in merged_rows if row["candidate_id"] not in previous_ids
    ]
    controlled_import_review_ready = [
        row for row in merged_rows if row["controlled_import_review_lane_ready"]
    ]

    preview_candidate_ids = {
        str(row["candidate_id"])
        for row in materialization_preview_payload.get("rows", []) or []
        if isinstance(row, dict) and row.get("candidate_id")
    }
    import_ready_candidate_ids = {str(row["candidate_id"]) for row in import_ready_rows}
    preview_provenance_ok = all(
        row["provenance_audit"]["source_provenance_present"] for row in import_ready_rows
    )
    preview_non_overlap_ok = all(not row["current702_conflict"] for row in import_ready_rows)

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "counts": {
            "merged_rows": len(merged_rows),
            "import_ready_rows": len(import_ready_rows),
            "repair_queue_rows": len(repair_queue_rows),
            "blocked_duplicate_or_current_registry_conflict_rows": len(
                duplicate_blocked_rows
            ),
            "current702_conflict_rows": len(current702_conflict_rows),
            "external_duplicate_conflict_rows": len(external_duplicate_rows),
            "rows_newly_added_by_scaleout": len(newly_added_by_scaleout),
            "rows_retained_from_previous_qa_surface": len(merged_rows)
            - len(newly_added_by_scaleout),
            "materialized_from_validated_queue_rows": materialized_from_queue_counts.get(
                "validated_ready_preview", 0
            ),
            "materialized_from_provisional_queue_rows": materialized_from_queue_counts.get(
                "provisional_bulk_preview", 0
            ),
            "controlled_import_review_lane_ready_rows": len(
                controlled_import_review_ready
            ),
        },
        "terminal_state_counts": terminal_state_counts,
        "lane_terminal_state_counts": lane_terminal_state_counts,
        "merge_status_counts": dict(sorted(merge_status_counts.items())),
        "source_artifact_reconciliation": {
            "materialization_rows": len(materialization_rows),
            "bulk_scaleout_rows": len(bulk_rows),
            "materialization_rows_missing_from_bulk_scaleout": materialization_only_ids,
            "materialization_preview_candidate_count": len(preview_candidate_ids),
            "import_ready_candidate_count": len(import_ready_candidate_ids),
            "materialization_preview_matches_import_ready_rows": preview_candidate_ids
            == import_ready_candidate_ids,
        },
        "validation_checks": {
            "passed": not issues
            and materialization_payload.get("counts", {}).get("input_rows")
            == len(materialization_rows)
            and bulk_scaleout_payload.get("candidate_count") == len(bulk_rows)
            and bulk_preview_payload.get("candidate_count")
            == len(bulk_preview_payload.get("rows", []) or [])
            and materialization_preview_payload.get("candidate_count")
            == len(materialization_preview_payload.get("rows", []) or [])
            and preview_provenance_ok
            and preview_non_overlap_ok,
            "issues": issues,
            "materialization_input_rows_match": materialization_payload.get(
                "counts", {}
            ).get("input_rows")
            == len(materialization_rows),
            "bulk_scaleout_candidate_count_matches_rows": bulk_scaleout_payload.get(
                "candidate_count"
            )
            == len(bulk_rows),
            "bulk_preview_candidate_count_matches_rows": bulk_preview_payload.get(
                "candidate_count"
            )
            == len(bulk_preview_payload.get("rows", []) or []),
            "materialization_preview_candidate_count_matches_rows": (
                materialization_preview_payload.get("candidate_count")
                == len(materialization_preview_payload.get("rows", []) or [])
            ),
            "import_ready_rows_have_source_provenance": preview_provenance_ok,
            "import_ready_rows_clear_current702_non_overlap_check": (
                preview_non_overlap_ok
            ),
        },
        "controlled_import_review_lane": {
            "ready": bool(controlled_import_review_ready),
            "ready_row_count": len(controlled_import_review_ready),
            "basis": (
                "preview-only external import lane is populated with materialized rows "
                "that carry source provenance and clear exact current702 non-overlap checks"
                if controlled_import_review_ready
                else "no row currently clears the preview-only import-review prerequisites"
            ),
            "production_import_authorized": False,
        },
        "guardrails": {
            "production_registry_edited": False,
            "label_import_performed": False,
            "final_import_files_edited": False,
            "heldout_splits_edited": False,
            "model_weights_edited": False,
            "production_thresholds_edited": False,
        },
        "source_artifacts": source_artifacts or {},
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
            "merge_status": row["merge_status"],
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
            "next_action": row.get("next_action"),
            "ready_for_controlled_import_review": True,
            "ready_for_production_label_import": False,
            "remaining_required_before_import": row["remaining_required_before_import"],
            "source_hashes": row.get("source_hashes"),
            "source_provenance": row.get("source_provenance"),
            "duplicate_status": row.get("duplicate_status"),
            "non_overlap_checks": {
                "exact_current702_non_overlap": not row["current702_conflict"],
                "external_duplicate_overlap_present": row["external_duplicate_conflict"],
            },
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
            "merge_status": row["merge_status"],
            "next_action": row.get("next_action") or row.get("exact_next_action"),
            "remaining_required_before_import": row["remaining_required_before_import"],
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
    source_artifacts = merged_surface.get("source_artifacts", {})
    lines = [
        "# External Admission QA Merger - current702",
        "",
        "Merged the completed producer outputs by overlaying the 370-row "
        "materialization admission batch onto the 845-row bulk pagination "
        "scaleout surface, preserving preview-only guardrails and leaving all "
        "production registries, imports, ontologies, heldout splits, thresholds, "
        "and model weights untouched.",
        "",
        "## Summary",
        "",
        f"- Merged candidate count: {counts['merged_rows']}",
        f"- Import-ready preview count: {import_ready_preview['candidate_count']}",
        f"- Repair queue count: {repair_queue['candidate_count']}",
        f"- Blocked duplicate/current702 conflict rows: {counts['blocked_duplicate_or_current_registry_conflict_rows']}",
        f"- Exact current702 conflict rows: {counts['current702_conflict_rows']}",
        f"- Rows newly added by scaleout vs 20260608 QA surface: {counts['rows_newly_added_by_scaleout']}",
        f"- Rows materialized from validated queue: {counts['materialized_from_validated_queue_rows']}",
        f"- Rows materialized from provisional queue: {counts['materialized_from_provisional_queue_rows']}",
        f"- Controlled import-review lane ready: {merged_surface['controlled_import_review_lane']['ready']}",
        "",
        "## Source Artifact Hashes",
        "",
    ]
    for label, metadata in source_artifacts.items():
        location = metadata.get("spec") or metadata.get("path") or metadata.get(
            "artifact_path", "unknown"
        )
        commit = metadata.get("git_commit")
        if commit:
            lines.append(
                f"- `{label}`: `{location}` @ `{commit[:8]}` "
                f"(sha256 `{metadata['sha256']}`)"
            )
        else:
            lines.append(
                f"- `{label}`: `{location}` (sha256 `{metadata['sha256']}`)"
            )

    lines.extend(["", "## Terminal State Counts", "", "| terminal state | count |", "| --- | ---: |"])
    for state, count in merged_surface["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    lines.extend(["", "## Lane Counts", "", "| lane | terminal state | count |", "| --- | --- | ---: |"])
    for lane, lane_counts in merged_surface["lane_terminal_state_counts"].items():
        for state, count in lane_counts.items():
            lines.append(f"| {lane} | `{state}` | {count} |")

    lines.extend(
        [
            "",
            "## Import Review Readiness",
            "",
            f"- Import-ready rows have source provenance: `{merged_surface['validation_checks']['import_ready_rows_have_source_provenance']}`",
            f"- Import-ready rows clear exact current702 non-overlap: `{merged_surface['validation_checks']['import_ready_rows_clear_current702_non_overlap_check']}`",
            f"- Production import authorized here: `{merged_surface['controlled_import_review_lane']['production_import_authorized']}`",
            f"- Lane basis: {merged_surface['controlled_import_review_lane']['basis']}",
            "",
            "## Repair Queue",
            "",
            "| candidate | lane | terminal state | repair bucket | next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in repair_queue["rows"][:25]:
        next_action = str(row.get("next_action") or "").replace("|", "\\|")
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
    materialization_batch_spec: str | Path = DEFAULT_MATERIALIZATION_BATCH_SPEC,
    materialization_preview_spec: str | Path = DEFAULT_MATERIALIZATION_PREVIEW_SPEC,
    bulk_scaleout_spec: str | Path = DEFAULT_BULK_SCALEOUT_SPEC,
    bulk_preview_spec: str | Path = DEFAULT_BULK_PREVIEW_SPEC,
    previous_merged_surface_spec: str | Path = DEFAULT_PREVIOUS_MERGED_SURFACE_SPEC,
    out_path: Path = DEFAULT_OUT_PATH,
    import_ready_path: Path = DEFAULT_IMPORT_READY_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    created_utc: str | None = None,
) -> dict[str, Any]:
    materialization_payload, materialization_source = _load_json_source(
        materialization_batch_spec
    )
    materialization_preview_payload, materialization_preview_source = _load_json_source(
        materialization_preview_spec
    )
    bulk_scaleout_payload, bulk_scaleout_source = _load_json_source(bulk_scaleout_spec)
    bulk_preview_payload, bulk_preview_source = _load_json_source(bulk_preview_spec)
    previous_merged_surface_payload, previous_merged_surface_source = _load_json_source(
        previous_merged_surface_spec
    )

    merged_surface = build_external_admission_merged_surface(
        materialization_payload=materialization_payload,
        materialization_preview_payload=materialization_preview_payload,
        bulk_scaleout_payload=bulk_scaleout_payload,
        bulk_preview_payload=bulk_preview_payload,
        previous_merged_surface_payload=previous_merged_surface_payload,
        source_artifacts={
            "external_materialization_admission_batch": materialization_source,
            "external_materialization_import_ready_preview": (
                materialization_preview_source
            ),
            "external_bulk_ingestion_scaleout": bulk_scaleout_source,
            "external_bulk_ingestion_scaleout_provisional_import_preview": (
                bulk_preview_source
            ),
            "previous_external_admission_qa_surface": previous_merged_surface_source,
        },
        created_utc=created_utc,
    )
    import_ready_preview = build_external_admission_import_ready_preview(merged_surface)
    repair_queue = build_external_admission_repair_queue(merged_surface)

    _write_json(out_path, merged_surface)
    import_ready_preview["source_artifacts"] = {
        "external_admission_merged_surface": {
            "path": str(out_path),
            "sha256": _sha256_text(out_path.read_text(encoding="utf-8")),
        }
    }
    repair_queue["source_artifacts"] = {
        "external_admission_merged_surface": {
            "path": str(out_path),
            "sha256": _sha256_text(out_path.read_text(encoding="utf-8")),
        }
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
