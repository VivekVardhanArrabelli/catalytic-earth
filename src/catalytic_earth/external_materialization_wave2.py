from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_DATE = "20260609"
ARTIFACT_ID = f"v3_external_materialization_wave2_current702_{RUN_DATE}"
IMPORT_READY_ARTIFACT_ID = (
    f"v3_external_materialization_wave2_import_ready_preview_current702_{RUN_DATE}"
)
REPAIR_QUEUE_ARTIFACT_ID = (
    f"v3_external_materialization_wave2_repair_queue_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_materialization_wave2"
IMPORT_READY_SCHEMA_VERSION = "v3.external_materialization_wave2_import_ready_preview"
REPAIR_QUEUE_SCHEMA_VERSION = "v3.external_materialization_wave2_repair_queue"
LOCATOR_SIDECAR_SCHEMA_VERSION = (
    "v3.external_materialization_wave2_source_free_locator_sidecar"
)

DEFAULT_MERGED_SURFACE_PATH = Path(
    "artifacts/v3_external_admission_merged_surface_current702_20260609.json"
)
DEFAULT_IMPORT_READY_SOURCE_PATH = Path(
    "artifacts/v3_external_admission_import_ready_preview_current702_20260609.json"
)
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_external_materialization_wave2_current702_{RUN_DATE}.json"
)
DEFAULT_IMPORT_READY_PREVIEW_PATH = Path(
    f"artifacts/v3_external_materialization_wave2_import_ready_preview_current702_{RUN_DATE}.json"
)
DEFAULT_REPAIR_QUEUE_PATH = Path(
    f"artifacts/v3_external_materialization_wave2_repair_queue_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/external_materialization_wave2_current702_{RUN_DATE}.md"
)
DEFAULT_LOCATOR_DIR = Path(
    f"artifacts/external_materialization_wave2_source_free_locators_current702_{RUN_DATE}"
)

LOW_DISK_COORDINATE_POLICY = (
    "coordinate_downloads_disabled_because_run_started_below_10_gib_floor"
)
SIDECAR_ADVANCE_STATES = {
    "locator_ready_candidate",
    "provisional_external_countable_preflight_candidate",
}
IMPORT_READY_STATE = "import_ready_preview"
DUPLICATE_STATE = "blocked_duplicate_or_current_registry_conflict"
COORDINATE_READY_STATE = "coordinate_ready_pending_locator"
REPAIR_STATES = {
    "coordinate_repair_candidate",
    "hard_blocked_with_next_action",
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


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": _sha256_path(path),
        "bytes": path.stat().st_size,
    }


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return sorted(value)
    return [value]


def _sidecar_token(candidate_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", candidate_id.replace(":", "_"))


def _exact_locators(row: dict[str, Any]) -> list[dict[str, Any]]:
    locators = [
        locator
        for locator in _as_list(row.get("residue_locators"))
        if isinstance(locator, dict)
    ]
    return [locator for locator in locators if locator.get("exact") is True]


def _position(locator: dict[str, Any]) -> int | None:
    try:
        return int(str(locator.get("position")))
    except (TypeError, ValueError):
        return None


def _role_hint(locator: dict[str, Any]) -> str:
    feature_code = str(locator.get("feature_code") or "")
    ligand_name = str(locator.get("ligand_name") or "").lower()
    if feature_code == "ACT_SITE":
        return "reviewed_active_site_feature"
    if feature_code == "METAL":
        return "reviewed_metal_binding_feature"
    if feature_code == "BINDING":
        if "heme" in ligand_name:
            return "reviewed_heme_binding_feature"
        if "phosphate" in ligand_name or "atp" in ligand_name:
            return "reviewed_phosphoryl_binding_feature"
        if "pyridoxal" in ligand_name or "plp" in ligand_name:
            return "reviewed_plp_binding_feature"
        if "s-adenosyl" in ligand_name or ligand_name == "sam":
            return "reviewed_sam_binding_feature"
        if "cobalamin" in ligand_name:
            return "reviewed_cobalamin_binding_feature"
        if "iron-sulfur" in ligand_name:
            return "reviewed_iron_sulfur_binding_feature"
        return "reviewed_binding_feature"
    if feature_code == "SITE":
        return "reviewed_site_feature"
    if feature_code == "MOD_RES":
        return "reviewed_modified_residue_feature"
    return "reviewed_structured_feature"


def _duplicate_status(row: dict[str, Any]) -> dict[str, Any]:
    duplicate_summary = row.get("duplicate_status_summary")
    duplicate_current = row.get("duplicate_current_registry_conflict")
    if isinstance(duplicate_summary, dict):
        return {
            "blocked_by_duplicate_or_current_registry_conflict": bool(
                duplicate_summary.get("blocked_by_duplicate_or_current_registry_conflict")
            ),
            "current702_status": duplicate_summary.get("current702_status"),
            "external_pilot_status": duplicate_summary.get("external_pilot_status"),
        }
    if isinstance(duplicate_current, dict):
        return {
            "blocked_by_duplicate_or_current_registry_conflict": bool(
                duplicate_current.get("duplicate_or_current_registry_conflict")
            ),
            "current702_status": duplicate_current.get(
                "current_registry_conflict_status"
            ),
            "external_pilot_status": (
                duplicate_current.get("external_pilot_conflict", {}) or {}
            ).get("external_pilot_conflict_status"),
        }
    return {
        "blocked_by_duplicate_or_current_registry_conflict": (
            row.get("terminal_state") == DUPLICATE_STATE
        ),
        "current702_status": row.get("duplicate_current_registry_conflict_status"),
        "external_pilot_status": row.get("duplicate_external_pilot_conflict_status"),
    }


def _sidecar_payload(
    row: dict[str, Any],
    *,
    created_utc: str,
    sidecar_path: Path,
) -> dict[str, Any]:
    candidate_id = str(row.get("candidate_id") or "")
    residue_locators: list[dict[str, Any]] = []
    for locator in _exact_locators(row):
        position = _position(locator)
        if position is None:
            continue
        residue_locators.append(
            {
                "sequence_position": position,
                "end": locator.get("end"),
                "reviewed_feature_code": locator.get("feature_code"),
                "reviewed_feature_type": locator.get("feature_type"),
                "evidence_codes": sorted(str(code) for code in _as_list(locator.get("evidence_codes"))),
                "ligand_id": locator.get("ligand_id"),
                "ligand_name": locator.get("ligand_name"),
                "role_hint": _role_hint(locator),
                "locator_confidence": 0.5,
                "locator_evidence_class": (
                    "reviewed_exact_position_without_source_text_pending_"
                    "coordinate_local_residue_identity"
                ),
                "coordinate_independent_provenance": {
                    "heldout_rows_used": False,
                    "method": (
                        "reviewed_exact_position_source_free_locator_sidecar_"
                        "without_coordinate_download"
                    ),
                    "sequence_position_uniprot_declared": True,
                    "coordinate_local_residue_identity_validated": False,
                    "source_text_used": False,
                    "reviewed_feature_code": locator.get("feature_code"),
                    "reviewed_feature_type": locator.get("feature_type"),
                },
            }
        )
    return {
        "artifact_id": (
            "v3_external_materialization_wave2_source_free_locator_"
            f"{_sidecar_token(candidate_id)}_current702_{RUN_DATE}"
        ),
        "schema_version": LOCATOR_SIDECAR_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_id": candidate_id,
        "source_accession": row.get("accession"),
        "source_family_lane": row.get("target_family_lane") or row.get("lane_id"),
        "source_terminal_state": row.get("terminal_state"),
        "source_hashes": row.get("source_hashes", {}),
        "coordinate_provenance": {
            "afdb_or_pdb_identifier": row.get("afdb_or_pdb_identifier"),
            "alphafold_ids": row.get("alphafold_ids", []),
            "pdb_ids": row.get("pdb_ids", []),
            "coordinate_source_status": row.get("coordinate_source_status")
            or row.get("coordinate_status")
            or (row.get("evidence_basis", {}) or {}).get("coordinate_status"),
            "coordinate_mapping_basis": row.get("coordinate_mapping_basis"),
            "coordinate_path": None,
            "coordinate_sha256": None,
            "coordinate_download_performed": False,
            "coordinate_download_policy": LOW_DISK_COORDINATE_POLICY,
            "coordinate_local_residue_identity_validated": False,
        },
        "forbidden_feature_audit": {
            "benchmark_role": False,
            "ec_identifiers": False,
            "entry_name": False,
            "fingerprint_id": False,
            "label_type": False,
            "mechanism_text": False,
            "panel_id_as_feature": False,
            "rhea_identifiers": False,
            "source_prose": False,
            "source_review_rationale": False,
        },
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "review_only": True,
            "source_text_or_label_fields_used_as_predictive_features": False,
        },
        "locator_policy": (
            "review_only_exact_position_locator_pending_coordinate_identity"
        ),
        "ready_for_controlled_import_review": False,
        "ready_for_predicted_geometry_scoring": False,
        "residue_locators": residue_locators,
        "sidecar_path": str(sidecar_path),
        "source_free_active_site_locator_status": (
            "materialized_pending_coordinate_local_residue_identity"
        ),
        "split_protection": {
            "allowed_for_threshold_selection": False,
            "allowed_for_training": False,
            "ready_for_label_import": False,
            "review_only": True,
        },
    }


def _repair_bucket(row: dict[str, Any], wave2_terminal_state: str) -> str:
    source_state = str(row.get("terminal_state") or "")
    if wave2_terminal_state == "locator_sidecar_materialized_coordinate_pending":
        return "coordinate_materialization_continuation_due_disk_floor"
    if source_state == DUPLICATE_STATE:
        return "duplicate_conflict_no_import"
    if source_state == COORDINATE_READY_STATE:
        return "source_free_locator_materialization_needed"
    if source_state == "locator_repair_candidate":
        return "locator_repair"
    if source_state == "coordinate_repair_candidate":
        return "coordinate_repair"
    if source_state == "repairable_locator_blocker":
        return "locator_repair"
    if source_state == "hard_blocked_with_next_action":
        return "hard_blocker"
    return "admission_or_materialization_continuation"


def _next_action(row: dict[str, Any], wave2_terminal_state: str) -> str:
    if wave2_terminal_state == "locator_sidecar_materialized_coordinate_pending":
        return (
            "When disk free space is above 10 GiB, materialize or reuse the "
            "coordinate file, validate coordinate-local residue identity for "
            "the sidecar, then rerun import-ready preview admission."
        )
    if wave2_terminal_state == "import_ready_preview_carried_forward":
        return (
            "Keep in preview-only controlled import-review queue; structural "
            "duplicate screening and explicit production authorization remain."
        )
    return str(
        row.get("exact_next_action")
        or row.get("next_action")
        or "Resolve the recorded blocker before import-ready preview admission."
    )


def _compact_wave2_row(
    row: dict[str, Any],
    *,
    wave2_terminal_state: str,
    locator_sidecar_path: str | None,
    import_ready_row: dict[str, Any] | None,
) -> dict[str, Any]:
    exact_locators = _exact_locators(row)
    coordinate_path = None
    locator_path = locator_sidecar_path
    if import_ready_row:
        coordinate_path = import_ready_row.get("coordinate_path")
        locator_path = import_ready_row.get("locator_sidecar_path")
    return {
        "candidate_id": row.get("candidate_id"),
        "accession": row.get("accession"),
        "target_family_lane": row.get("target_family_lane") or row.get("lane_id"),
        "source_terminal_state": row.get("terminal_state"),
        "wave2_terminal_state": wave2_terminal_state,
        "repair_bucket": _repair_bucket(row, wave2_terminal_state),
        "coordinate_path": coordinate_path,
        "locator_sidecar_path": locator_path,
        "coordinate_materialization_status": (
            "carried_from_consumed_materialization_preview"
            if import_ready_row
            else LOW_DISK_COORDINATE_POLICY
        ),
        "locator_sidecar_status": (
            "carried_from_consumed_materialization_preview"
            if import_ready_row
            else (
                "materialized_pending_coordinate_identity"
                if locator_sidecar_path
                else "not_materialized"
            )
        ),
        "exact_residue_locator_count": len(exact_locators),
        "duplicate_status": _duplicate_status(row),
        "ready_for_controlled_import_review": bool(
            import_ready_row and import_ready_row.get("ready_for_controlled_import_review")
        ),
        "ready_for_production_label_import": False,
        "source_hashes": row.get("source_hashes", {}),
        "stable_candidate_key": row.get("stable_candidate_key"),
        "next_action": _next_action(row, wave2_terminal_state),
    }


def build_external_materialization_wave2(
    *,
    merged_surface_path: Path = DEFAULT_MERGED_SURFACE_PATH,
    import_ready_source_path: Path = DEFAULT_IMPORT_READY_SOURCE_PATH,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    created_utc: str | None = None,
    disk_free_gib_at_start: float | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[tuple[Path, dict[str, Any]]]]:
    created_utc = created_utc or _utc_now_iso()
    merged_surface = _read_json(merged_surface_path)
    import_ready_source = _read_json(import_ready_source_path)
    rows = list(merged_surface.get("rows", []))
    import_rows = list(import_ready_source.get("rows", []))
    import_by_candidate = {
        str(row.get("candidate_id")): row
        for row in import_rows
        if row.get("candidate_id")
    }

    wave2_rows: list[dict[str, Any]] = []
    repair_rows: list[dict[str, Any]] = []
    sidecars: list[tuple[Path, dict[str, Any]]] = []
    duplicate_conflicts = 0
    source_terminal_counts: Counter[str] = Counter()
    wave2_terminal_counts: Counter[str] = Counter()
    lane_terminal_counts: dict[str, Counter[str]] = defaultdict(Counter)

    for row in rows:
        candidate_id = str(row.get("candidate_id") or "")
        source_state = str(row.get("terminal_state") or "")
        source_terminal_counts[source_state] += 1
        import_ready_row = import_by_candidate.get(candidate_id)
        locator_sidecar_path: str | None = None
        if import_ready_row:
            wave2_state = "import_ready_preview_carried_forward"
        elif source_state in SIDECAR_ADVANCE_STATES and _exact_locators(row):
            sidecar_path = locator_dir / f"{_sidecar_token(candidate_id)}.json"
            sidecar = _sidecar_payload(
                row, created_utc=created_utc, sidecar_path=sidecar_path
            )
            sidecars.append((sidecar_path, sidecar))
            locator_sidecar_path = str(sidecar_path)
            wave2_state = "locator_sidecar_materialized_coordinate_pending"
        elif source_state == DUPLICATE_STATE:
            duplicate_conflicts += 1
            wave2_state = "blocked_duplicate_or_current_registry_conflict"
        else:
            wave2_state = f"repair_queue_{source_state or 'unknown'}"

        wave2_row = _compact_wave2_row(
            row,
            wave2_terminal_state=wave2_state,
            locator_sidecar_path=locator_sidecar_path,
            import_ready_row=import_ready_row,
        )
        wave2_rows.append(wave2_row)
        wave2_terminal_counts[wave2_state] += 1
        lane = str(row.get("target_family_lane") or row.get("lane_id") or "unknown")
        lane_terminal_counts[lane][wave2_state] += 1
        if wave2_state != "import_ready_preview_carried_forward":
            repair_rows.append(wave2_row)

    consumed_source_artifacts = dict(merged_surface.get("source_artifacts", {}))
    consumed_source_artifacts["wave2_merged_surface_input"] = _source_record(
        merged_surface_path
    )
    consumed_source_artifacts["wave2_import_ready_source_input"] = _source_record(
        import_ready_source_path
    )

    counts = {
        "input_rows": len(rows),
        "coordinate_downloads_performed": 0,
        "coordinate_materialized_new": 0,
        "coordinate_reused_from_consumed_preview": len(import_rows),
        "locator_sidecars_materialized_new": len(sidecars),
        "locator_sidecars_reused_from_consumed_preview": len(import_rows),
        "import_ready_preview_count": len(import_rows),
        "repair_queue_count": len(repair_rows),
        "duplicate_conflict_count": duplicate_conflicts,
        "disk_free_gib_at_start": disk_free_gib_at_start,
    }
    validation_checks = {
        "passed": (
            counts["input_rows"]
            == counts["import_ready_preview_count"] + counts["repair_queue_count"]
        )
        and counts["locator_sidecars_materialized_new"]
        == wave2_terminal_counts["locator_sidecar_materialized_coordinate_pending"],
        "input_rows_reconcile": (
            counts["input_rows"]
            == counts["import_ready_preview_count"] + counts["repair_queue_count"]
        ),
        "sidecar_count_reconciles": (
            counts["locator_sidecars_materialized_new"]
            == wave2_terminal_counts["locator_sidecar_materialized_coordinate_pending"]
        ),
        "coordinate_download_guardrail_enforced": True,
        "production_edit_guardrails": {
            "final_import_files_edited": False,
            "heldout_splits_edited": False,
            "label_import_performed": False,
            "model_weights_edited": False,
            "ontology_edited": False,
            "production_registry_edited": False,
            "production_thresholds_edited": False,
        },
    }
    artifact = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc,
        "scope": {
            "benchmark_surface": "current702",
            "mission": "external_materialization_admission_wave2",
            "coordinate_policy": LOW_DISK_COORDINATE_POLICY,
            "source_pattern": (
                "continues origin/ce-external-materialization-admission-batch-"
                "20260608 without coordinate downloads"
            ),
        },
        "source_artifacts": consumed_source_artifacts,
        "counts": counts,
        "source_terminal_state_counts": dict(sorted(source_terminal_counts.items())),
        "wave2_terminal_state_counts": dict(sorted(wave2_terminal_counts.items())),
        "lane_wave2_terminal_state_counts": {
            lane: dict(sorted(counter.items()))
            for lane, counter in sorted(lane_terminal_counts.items())
        },
        "rows": wave2_rows,
        "validation_checks": validation_checks,
        "guardrails": validation_checks["production_edit_guardrails"],
        "exact_next_continuation": (
            "Restore disk free space above 10 GiB, then rerun coordinate "
            "materialization for the locator-sidecar continuation rows and "
            "the coordinate-ready pending-locator queue before expanding the "
            "controlled import-ready preview."
        ),
    }

    import_preview = {
        "artifact_id": IMPORT_READY_ARTIFACT_ID,
        "schema_version": IMPORT_READY_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_count": len(import_rows),
        "source_artifacts": consumed_source_artifacts,
        "guardrails": {
            "label_import_performed": False,
            "preview_only": True,
            "production_registry_edited": False,
            "coordinate_files_recopied_in_this_run": False,
        },
        "rows": import_rows,
    }
    repair_queue = {
        "artifact_id": REPAIR_QUEUE_ARTIFACT_ID,
        "schema_version": REPAIR_QUEUE_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_count": len(repair_rows),
        "repair_bucket_counts": dict(
            sorted(Counter(row["repair_bucket"] for row in repair_rows).items())
        ),
        "source_artifacts": consumed_source_artifacts,
        "rows": repair_rows,
        "exact_next_continuation": artifact["exact_next_continuation"],
    }
    return artifact, import_preview, repair_queue, sidecars


def render_external_materialization_wave2_report(
    artifact: dict[str, Any],
    import_preview: dict[str, Any],
    repair_queue: dict[str, Any],
) -> str:
    counts = artifact["counts"]
    lines = [
        "# External Materialization Wave 2 - current702",
        "",
        f"Run: {artifact['created_utc']}",
        "",
        "Wave 2 consumed the 2026-06-09 admission QA merged surface and import-ready preview, carrying forward already materialized rows while avoiding coordinate downloads because the run started below the 10 GiB disk floor.",
        "",
        "## Summary",
        "",
        f"- Input rows: `{counts['input_rows']}`",
        f"- Coordinate materialized new: `{counts['coordinate_materialized_new']}`",
        f"- Coordinate reused from consumed preview: `{counts['coordinate_reused_from_consumed_preview']}`",
        f"- Locator sidecars materialized new: `{counts['locator_sidecars_materialized_new']}`",
        f"- Locator sidecars reused from consumed preview: `{counts['locator_sidecars_reused_from_consumed_preview']}`",
        f"- Import-ready preview count: `{counts['import_ready_preview_count']}`",
        f"- Repair/continuation queue count: `{counts['repair_queue_count']}`",
        f"- Duplicate conflicts: `{counts['duplicate_conflict_count']}`",
        f"- Disk free at start GiB: `{counts['disk_free_gib_at_start']}`",
        "",
        "## Consumed Source Artifacts",
        "",
    ]
    for name, record in sorted(artifact["source_artifacts"].items()):
        spec = record.get("spec") or record.get("path") or record.get("artifact_path")
        sha = record.get("sha256")
        lines.append(f"- `{name}`: `{spec}` (sha256 `{sha}`)")
    lines.extend(
        [
            "",
            "## Wave 2 Terminal Counts",
            "",
            "| terminal state | count |",
            "| --- | ---: |",
        ]
    )
    for state, count in artifact["wave2_terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")
    lines.extend(
        [
            "",
            "## Repair Buckets",
            "",
            "| repair bucket | count |",
            "| --- | ---: |",
        ]
    )
    for bucket, count in repair_queue["repair_bucket_counts"].items():
        lines.append(f"| `{bucket}` | {count} |")
    lines.extend(
        [
            "",
            "## Import-Ready Preview",
            "",
            f"- Rows: `{import_preview['candidate_count']}`",
            "- Preview-only; no production import, registry, ontology, split, threshold, or model-weight edit was performed.",
            "",
            "## Exact Next Continuation",
            "",
            f"- {artifact['exact_next_continuation']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_external_materialization_wave2(
    *,
    merged_surface_path: Path = DEFAULT_MERGED_SURFACE_PATH,
    import_ready_source_path: Path = DEFAULT_IMPORT_READY_SOURCE_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    import_ready_preview_path: Path = DEFAULT_IMPORT_READY_PREVIEW_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    created_utc: str | None = None,
    disk_free_gib_at_start: float | None = None,
) -> dict[str, Any]:
    artifact, import_preview, repair_queue, sidecars = build_external_materialization_wave2(
        merged_surface_path=merged_surface_path,
        import_ready_source_path=import_ready_source_path,
        locator_dir=locator_dir,
        created_utc=created_utc,
        disk_free_gib_at_start=disk_free_gib_at_start,
    )
    for sidecar_path, sidecar in sidecars:
        _write_json(sidecar_path, sidecar)
    _write_json(out_path, artifact)
    _write_json(import_ready_preview_path, import_preview)
    _write_json(repair_queue_path, repair_queue)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_materialization_wave2_report(
                artifact, import_preview, repair_queue
            ),
            encoding="utf-8",
        )
    return artifact
