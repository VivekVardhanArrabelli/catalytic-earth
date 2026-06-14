from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import load_json


RUN_DATE = "20260608"
ARTIFACT_ID = f"v3_countable_label_unblocker_matrix_current702_{RUN_DATE}"
IMPORT_PREVIEW_ARTIFACT_ID = (
    f"v3_countable_label_unblocker_import_preview_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.countable_label_unblocker_matrix"

DEFAULT_MERGED_SURFACE_PATH = Path(
    "artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json"
)
DEFAULT_REPAIR_OVERLAY_PATH = Path(
    "artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json"
)
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_countable_label_unblocker_matrix_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/countable_label_unblocker_matrix_current702_{RUN_DATE}.md"
)
DEFAULT_IMPORT_PREVIEW_PATH = Path(
    f"artifacts/v3_countable_label_unblocker_import_preview_current702_{RUN_DATE}.json"
)

TARGET_CANONICAL_STATES = {
    "review_only_evidence",
    "blocked_family_decision",
    "blocked_locator",
    "blocked_coordinate",
}

UNBLOCK_CLASSIFICATIONS = {
    "auto_promotable_import_preview_candidate",
    "locator_repair_candidate",
    "coordinate_repair_candidate",
    "family_default_resolved",
    "true_expert_only",
    "reject/OOS_preserve_signal",
    "hard_blocked_with_next_action",
}

POSITIVE_DUPLICATE_STATUSES = {
    "accession_exact_current_reference_duplicate",
    "current702_entry_id_present_duplicate_for_import",
    "current_countable_structural_duplicate_signal",
    "current_plp_structural_duplicate_signal",
    "exact_reference_or_sequence_holdout",
    "external_accession_exact_current_reference_match",
    "sequence_cluster_proxy_duplicate_cluster",
}

EXPERT_ONLY_MARKERS = (
    "expert",
    "human",
    "needs_review",
    "mechanism_match_review_ready",
    "terminal review",
    "explicit approval",
    "reviewer",
    "manual",
)

FAMILY_DEFAULT_MARKERS = (
    "policy_not_active",
    "registry_and_label_factory_extension_not_implemented",
    "threshold_not_calibrated",
    "candidate_evidence_lane_only_no_import",
    "not_in_current_epk_readiness_packet",
    "resolve epk_atp_gamma_transfer",
    "resolve pfkb_ribokinase_like",
    "resolve pfka_phosphofructokinase",
    "resolve ndk_phosphohistidine",
    "resolve atp_grasp_phosphointermediate",
    "resolve phosphatase_phosphoesterase",
)

COORDINATE_MISSING_MARKERS = {
    "missing_selected_structure",
    "missing_or_unsupported_structure",
    "predicted_geometry_missing",
    "unsupported_or_missing_geometry",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


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


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _read_json(path: Path) -> Any:
    return load_json(path)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _walk_values(payload: Any) -> list[Any]:
    values: list[Any] = []
    if isinstance(payload, dict):
        for value in payload.values():
            values.append(value)
            values.extend(_walk_values(value))
    elif isinstance(payload, list):
        for value in payload:
            values.append(value)
            values.extend(_walk_values(value))
    return values


def _find_key_values(payload: Any, key: str) -> list[Any]:
    values: list[Any] = []
    if isinstance(payload, dict):
        for current_key, value in payload.items():
            if current_key == key:
                values.append(value)
            values.extend(_find_key_values(value, key))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(_find_key_values(value, key))
    return values


def _string_values_for_keys(payload: Any, keys: set[str]) -> list[str]:
    values: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in keys:
                for item in _as_list(value):
                    if item not in (None, "", [], {}):
                        values.append(str(item))
            values.extend(_string_values_for_keys(value, keys))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(_string_values_for_keys(value, keys))
    return values


def _counter_dict(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def _lower_blob(values: list[Any]) -> str:
    return " ".join(str(value).lower() for value in values if value not in (None, ""))


def _normalize_lookup_key(value: Any) -> str | None:
    if value in (None, "", [], {}):
        return None
    text = str(value).strip().lower()
    if not text:
        return None
    return text.replace(" ", "_")


def _candidate_lookup_keys(canonical: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for value in [canonical.get("canonical_key")]:
        norm = _normalize_lookup_key(value)
        if norm:
            keys.add(norm)
            keys.add(norm.replace(":", "_"))
    axes = canonical.get("dedupe_axes", {})
    for axis_key in (
        "accession_candidate_keys",
        "accessions_observed",
        "candidate_ids_observed",
    ):
        for value in _as_list(axes.get(axis_key)):
            norm = _normalize_lookup_key(value)
            if not norm:
                continue
            keys.add(norm)
            keys.add(norm.replace(":", "_"))
            if norm.startswith("uniprot:"):
                keys.add(norm.split(":", 1)[1])
    for member in canonical.get("source_members", []):
        for value in (member.get("accession"), member.get("candidate_id")):
            norm = _normalize_lookup_key(value)
            if not norm:
                continue
            keys.add(norm)
            keys.add(norm.replace(":", "_"))
            if norm.startswith("uniprot:"):
                keys.add(norm.split(":", 1)[1])
    return keys


def _index_coordinate_files(artifacts_dir: Path = Path("artifacts")) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    if not artifacts_dir.exists():
        return index
    for directory in artifacts_dir.iterdir():
        if not directory.is_dir() or "coordinate" not in directory.name.lower():
            continue
        for path in directory.rglob("*.cif"):
            name = path.name.lower()
            keys = {name, path.stem.lower()}
            if name.startswith("pdb_") and name.endswith(".cif"):
                keys.add(name[4:-4])
            if name.startswith("af-") and "-f1-model" in name:
                keys.add(name.split("-")[1].lower())
                keys.add(f"uniprot:{name.split('-')[1].lower()}")
            record = {"path": str(path), "bytes": path.stat().st_size}
            for key in keys:
                index.setdefault(key, []).append(record)
    return index


def _coordinate_matches(
    coordinate_index: dict[str, list[dict[str, Any]]],
    selected_structures: list[str],
    pdb_ids: list[str],
    alphafold_ids: list[str],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    seen: set[str] = set()
    keys: set[str] = set()
    for value in selected_structures + pdb_ids:
        norm = _normalize_lookup_key(value)
        if not norm or norm in COORDINATE_MISSING_MARKERS:
            continue
        keys.add(norm.removeprefix("pdb:"))
        keys.add(f"pdb_{norm.removeprefix('pdb:')}.cif")
    for value in alphafold_ids:
        norm = _normalize_lookup_key(value)
        if not norm:
            continue
        keys.add(norm.removeprefix("uniprot:"))
        keys.add(f"uniprot:{norm.removeprefix('uniprot:')}")
    for key in keys:
        for record in coordinate_index.get(key, []):
            path = record["path"]
            if path in seen:
                continue
            seen.add(path)
            matches.append(record)
    return sorted(matches, key=lambda record: record["path"])


def _index_locator_evidence() -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}

    def add(keys: list[Any], record: dict[str, Any]) -> None:
        normalized = sorted({key for key in (_normalize_lookup_key(v) for v in keys) if key})
        for key in normalized:
            index.setdefault(key, []).append(record)
            index.setdefault(key.replace(":", "_"), []).append(record)
            if key.startswith("uniprot:"):
                index.setdefault(key.split(":", 1)[1], []).append(record)

    materialization_path = Path(
        "artifacts/"
        "v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_"
        "source_free_locator_rewrite_materialization_gate_current702_20260603.json"
    )
    if materialization_path.exists():
        payload = _read_json(materialization_path)
        for row in payload.get("row_decisions", []):
            if row.get("approved_locator_sidecar_written") is True:
                add(
                    [row.get("entry_id"), row.get("source_accession")],
                    {
                        "artifact": str(materialization_path),
                        "entry_id": row.get("entry_id"),
                        "source_accession": row.get("source_accession"),
                        "approved_locator_path": row.get(
                            "planned_audited_locator_sidecar_path"
                        ),
                        "status": "approved_locator_sidecar_written",
                    },
                )

    resolution_path = Path(
        "artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json"
    )
    if resolution_path.exists():
        payload = _read_json(resolution_path)
        for row in payload.get("resolved_rows", []):
            if row.get("ready_for_predicted_geometry_scoring") is True:
                add(
                    [row.get("entry_id"), row.get("source_accession")],
                    {
                        "artifact": str(resolution_path),
                        "entry_id": row.get("entry_id"),
                        "source_accession": row.get("source_accession"),
                        "approved_locator_path": row.get("approved_locator_path"),
                        "status": row.get("resolution_status"),
                    },
                )

    sidecar_dir = Path("artifacts/family_panel_source_free_active_site_locators_current702_20260601")
    if sidecar_dir.exists():
        for path in sidecar_dir.glob("*.json"):
            keys = [path.stem, path.name]
            try:
                payload = _read_json(path)
            except json.JSONDecodeError:
                payload = {}
            for key in ("entry_id", "candidate_id", "source_accession", "accession"):
                keys.extend(_find_key_values(payload, key))
            add(
                keys,
                {
                    "artifact": str(path),
                    "approved_locator_path": str(path),
                    "status": "audited_locator_sidecar_present",
                },
            )
    return index


def _load_source_rows(merged: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    source_rows: dict[str, list[dict[str, Any]]] = {}
    source_records: dict[str, dict[str, Any]] = {}
    for shard in merged.get("source_shard_readiness", []):
        path = Path(shard["artifact_path"])
        payload = _read_json(path)
        rows = payload.get(shard.get("row_key", "rows"), [])
        source_rows[str(path)] = rows
        source_records[str(path)] = _source_record(path)
    return source_rows, source_records


def _source_row_for_member(
    member: dict[str, Any], source_rows: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    rows = source_rows[str(member["source_artifact"])]
    return rows[int(member["row_index"])]


def _repair_overlay_matches(
    canonical: dict[str, Any], repair_overlay: dict[str, Any] | None
) -> list[dict[str, Any]]:
    if not repair_overlay:
        return []
    keys = _candidate_lookup_keys(canonical)
    matches: list[dict[str, Any]] = []
    for row in repair_overlay.get("rows", []):
        row_keys = {
            _normalize_lookup_key(row.get("candidate_id")),
            _normalize_lookup_key(row.get("accession")),
        }
        row_keys = {key for key in row_keys if key}
        row_keys |= {key.split(":", 1)[1] for key in row_keys if key.startswith("uniprot:")}
        if keys & row_keys:
            matches.append(row)
    return matches


def _source_summary(
    canonical: dict[str, Any],
    source_rows: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
    coordinate_index: dict[str, list[dict[str, Any]]],
    locator_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    statuses: list[str] = list(
        canonical.get("dedupe_axes", {})
        .get("sequence_neighborhood", {})
        .get("statuses", [])
    )
    blockers: list[str] = []
    selected_structures: list[str] = []
    pdb_ids: list[str] = []
    alphafold_ids: list[str] = []
    coordinate_paths: list[str] = []
    source_hashes: dict[str, Any] = {
        "canonical_record_sha256": canonical.get("canonical_record_sha256"),
        "source_artifacts": {},
        "source_members": [],
    }
    next_steps: list[str] = []
    gate_ready_values: list[Any] = []
    gate_countable_values: list[Any] = []
    source_rows_compact: list[dict[str, Any]] = []
    locator_feature_counts: Counter[str] = Counter()

    for member in canonical.get("source_members", []):
        source_artifact = str(member["source_artifact"])
        row = _source_row_for_member(member, source_rows)
        source_hashes["source_artifacts"][source_artifact] = source_records[source_artifact]
        row_source_hashes = row.get("source_hashes", {})
        source_hashes["source_members"].append(
            {
                "source_artifact": source_artifact,
                "source_shard": member.get("source_shard"),
                "row_index": member.get("row_index"),
                "row_key": member.get("row_key"),
                "row_hash": member.get("row_hash"),
                "source_hash_count": member.get("source_hash_count"),
                "row_source_hashes": row_source_hashes,
            }
        )
        statuses.extend(
            _string_values_for_keys(
                row,
                {
                    "status",
                    "geometry_status",
                    "locator_status",
                    "coordinate_status",
                    "resolution_status",
                    "candidate_status",
                },
            )
        )
        blockers.extend(
            _string_values_for_keys(
                row,
                {
                    "terminal_blockers",
                    "readiness_blockers",
                    "blockers",
                    "candidate_blockers",
                    "remaining_import_blockers",
                    "manifest_blockers",
                    "input_terminal_blockers",
                },
            )
        )
        selected_structures.extend(
            _string_values_for_keys(
                row, {"selected_structure", "selected_structure_id", "selected_structures"}
            )
        )
        pdb_ids.extend(_string_values_for_keys(row, {"pdb_id", "pdb_ids"}))
        alphafold_ids.extend(_string_values_for_keys(row, {"alphafold_ids"}))
        coordinate_paths.extend(_string_values_for_keys(row, {"coordinate_path", "coordinate_paths"}))
        gate_ready_values.extend(_find_key_values(row, "ready_for_label_import"))
        gate_countable_values.extend(_find_key_values(row, "countable_label_candidate"))
        next_steps.extend(
            str(step)
            for step in _as_list(row.get("machine_actionable_next_step"))
            + _as_list(row.get("machine_actionable_next_steps"))
            if step
        )
        for key in ("active_site_feature_count", "binding_site_feature_count"):
            for value in _find_key_values(row, key):
                if isinstance(value, int) and value > 0:
                    locator_feature_counts[key] += value
        source_rows_compact.append(
            {
                "source_shard": member.get("source_shard"),
                "source_artifact": source_artifact,
                "row_index": member.get("row_index"),
                "candidate_id": row.get("candidate_id"),
                "accession": row.get("accession"),
                "terminal_state": member.get("terminal_state"),
                "confidence_tier": row.get("confidence_tier") or member.get("confidence_tier"),
                "proposed_family_lane": row.get("proposed_family_lane")
                or member.get("proposed_family_lane"),
                "proposed_subfamily_lane": row.get("proposed_subfamily_lane")
                or member.get("proposed_subfamily_lane"),
                "machine_actionable_next_step": row.get("machine_actionable_next_step")
                or member.get("machine_actionable_next_step"),
            }
        )

    selected_structures = sorted(set(selected_structures))
    pdb_ids = sorted(set(pdb_ids))
    alphafold_ids = sorted(set(alphafold_ids))
    coordinate_paths = sorted(set(path for path in coordinate_paths if path))
    local_coordinate_matches = _coordinate_matches(
        coordinate_index, selected_structures, pdb_ids, alphafold_ids
    )
    for path in coordinate_paths:
        coordinate_path = Path(path)
        if coordinate_path.exists():
            local_coordinate_matches.append(
                {"path": path, "bytes": coordinate_path.stat().st_size}
            )
    seen_paths: set[str] = set()
    deduped_coordinate_matches: list[dict[str, Any]] = []
    for match in local_coordinate_matches:
        if match["path"] in seen_paths:
            continue
        seen_paths.add(match["path"])
        payload = dict(match)
        payload["sha256"] = sha256_path(Path(match["path"]))
        deduped_coordinate_matches.append(payload)

    lookup_keys = _candidate_lookup_keys(canonical)
    approved_locator_matches: list[dict[str, Any]] = []
    seen_locator_paths: set[str] = set()
    for key in lookup_keys:
        for record in locator_index.get(key, []):
            marker = record.get("approved_locator_path") or record.get("artifact")
            if marker in seen_locator_paths:
                continue
            seen_locator_paths.add(str(marker))
            approved_locator_matches.append(record)

    return {
        "statuses": sorted(set(statuses)),
        "status_counts": _counter_dict(statuses),
        "blockers": sorted(set(blockers)),
        "selected_structures": selected_structures,
        "pdb_ids": pdb_ids,
        "alphafold_ids": alphafold_ids,
        "coordinate_paths_declared": coordinate_paths,
        "local_coordinate_matches": deduped_coordinate_matches,
        "approved_locator_matches": approved_locator_matches,
        "source_hashes": source_hashes,
        "source_rows": source_rows_compact,
        "gate_ready_for_label_import_true": any(value is True for value in gate_ready_values),
        "gate_countable_label_candidate_true": any(value is True for value in gate_countable_values),
        "gate_ready_for_label_import_values": _counter_dict(gate_ready_values),
        "gate_countable_label_candidate_values": _counter_dict(gate_countable_values),
        "next_steps": sorted(set(next_steps)),
        "locator_feature_counts": dict(locator_feature_counts),
    }


def _positive_duplicate_statuses(statuses: list[str]) -> list[str]:
    positive: list[str] = []
    for status in statuses:
        lowered = status.lower()
        if status in POSITIVE_DUPLICATE_STATUSES:
            positive.append(status)
            continue
        if (
            "duplicate_signal" in lowered
            and "no_" not in lowered
            and "not_" not in lowered
        ):
            positive.append(status)
    return sorted(set(positive))


def _family_default_resolvable(summary: dict[str, Any]) -> bool:
    blob = _lower_blob(summary["statuses"] + summary["blockers"] + summary["next_steps"])
    if any(marker in blob for marker in EXPERT_ONLY_MARKERS):
        return False
    return any(marker in blob for marker in FAMILY_DEFAULT_MARKERS)


def _expert_only(summary: dict[str, Any]) -> bool:
    blob = _lower_blob(summary["statuses"] + summary["blockers"] + summary["next_steps"])
    return any(marker in blob for marker in EXPERT_ONLY_MARKERS)


def _has_coordinate_handle(summary: dict[str, Any]) -> bool:
    return bool(
        summary["local_coordinate_matches"]
        or summary["coordinate_paths_declared"]
        or summary["selected_structures"]
        or summary["pdb_ids"]
        or summary["alphafold_ids"]
    )


def _classify_row(
    canonical: dict[str, Any],
    summary: dict[str, Any],
    repair_matches: list[dict[str, Any]],
) -> tuple[str, list[str], str]:
    state = canonical["canonical_terminal_state"]
    overlap = canonical["dedupe_axes"]["current_registry_overlap"]["overlap"]
    duplicate_statuses = _positive_duplicate_statuses(summary["statuses"])
    source_counts = canonical.get("source_terminal_state_counts", {})

    blockers: list[str] = []
    if overlap:
        blockers.append("current_registry_overlap_blocks_import_preview")
    blockers.extend(summary["blockers"])
    if duplicate_statuses:
        blockers.extend(f"positive_duplicate_screen:{status}" for status in duplicate_statuses)
    if not summary["gate_ready_for_label_import_true"]:
        blockers.append("no_source_gate_sets_ready_for_label_import_true")
    if not summary["gate_countable_label_candidate_true"]:
        blockers.append("no_source_gate_sets_countable_label_candidate_true")

    for repair in repair_matches:
        recommended = repair.get("recommended_terminal_state_for_future_surface")
        if recommended == "reject/OOS_preserve_signal":
            return (
                "reject/OOS_preserve_signal",
                sorted(set(blockers + ["repair_overlay_recommends_reject_oos"])),
                "preserve the mechanical duplicate/OOS repair recommendation; do not import",
            )

    if (
        state == "review_only_evidence"
        and not overlap
        and not duplicate_statuses
        and summary["gate_ready_for_label_import_true"]
        and summary["gate_countable_label_candidate_true"]
        and not summary["blockers"]
        and not source_counts.get("blocked_locator")
        and not source_counts.get("blocked_coordinate")
        and not source_counts.get("blocked_family_decision")
    ):
        return (
            "auto_promotable_import_preview_candidate",
            [],
            "write to import-preview candidate artifact; no production import is performed",
        )

    if overlap:
        return (
            "hard_blocked_with_next_action",
            sorted(set(blockers)),
            "do not import; exact/current registry overlap must be resolved or preserved as an existing current702 label",
        )

    if duplicate_statuses:
        return (
            "reject/OOS_preserve_signal",
            sorted(set(blockers)),
            "preserve the current duplicate-screen signal as non-counting evidence; do not import",
        )

    if state == "blocked_locator":
        if summary["approved_locator_matches"]:
            blockers.append("approved_locator_exists_but_import_gate_not_run_for_this_surface")
        else:
            blockers.append("approved_source_free_locator_missing_for_this_surface")
        return (
            "locator_repair_candidate",
            sorted(set(blockers)),
            "repair or approve a source-free active-site locator, then rerun duplicate and label-factory gates",
        )

    if state == "blocked_coordinate":
        if summary["local_coordinate_matches"]:
            blockers.append("coordinate_file_found_but_residue_locator_or_geometry_support_incomplete")
            return (
                "locator_repair_candidate",
                sorted(set(blockers)),
                "local coordinate provenance is present; repair active-site residue locator/support and rerun gates",
            )
        if _has_coordinate_handle(summary):
            blockers.append("coordinate_handle_present_but_no_hash_matched_local_coordinate_file")
        else:
            blockers.append("coordinate_or_structure_provenance_missing")
        return (
            "coordinate_repair_candidate",
            sorted(set(blockers)),
            "materialize or hash-match coordinate provenance before locator and import-gate review",
        )

    if state == "blocked_family_decision":
        if _family_default_resolvable(summary):
            return (
                "family_default_resolved",
                sorted(set(blockers + ["existing_family_policy_resolves_to_no_import_now"])),
                "apply existing family policy: keep non-counting until source-free active-site/substrate-mode evidence and gates pass",
            )
        if _expert_only(summary):
            return (
                "true_expert_only",
                sorted(set(blockers + ["explicit_family_or_terminal_expert_decision_required"])),
                "route to expert family/terminal decision; automation lacks a safe policy default",
            )
        return (
            "hard_blocked_with_next_action",
            sorted(set(blockers + ["family_source_or_preflight_gate_incomplete"])),
            "complete the named source-free family evidence, duplicate screen, or label-factory gate, then rerun",
        )

    if state == "review_only_evidence":
        if _expert_only(summary):
            return (
                "true_expert_only",
                sorted(set(blockers + ["review_only_requires_explicit_expert_promotion"])),
                "keep review-only until explicit expert promotion request and full gates exist",
            )
        return (
            "hard_blocked_with_next_action",
            sorted(set(blockers + ["conservative_review_only_policy_no_import_authority"])),
            "keep review-only; run a controlled promotion/import-preview gate before any countable use",
        )

    return (
        "hard_blocked_with_next_action",
        sorted(set(blockers + ["unhandled_terminal_state"])),
        "rerun after adding an explicit unblocker policy for this terminal state",
    )


def _matrix_row(
    canonical: dict[str, Any],
    source_rows: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
    coordinate_index: dict[str, list[dict[str, Any]]],
    locator_index: dict[str, list[dict[str, Any]]],
    repair_overlay: dict[str, Any] | None,
) -> dict[str, Any]:
    summary = _source_summary(
        canonical,
        source_rows=source_rows,
        source_records=source_records,
        coordinate_index=coordinate_index,
        locator_index=locator_index,
    )
    repair_matches = _repair_overlay_matches(canonical, repair_overlay)
    classification, blocker_basis, next_action = _classify_row(
        canonical, summary, repair_matches
    )
    axes = canonical.get("dedupe_axes", {})
    family_axis = axes.get("ligand_cofactor_family_lane", {})
    row = {
        "canonical_key": canonical["canonical_key"],
        "terminal_state": canonical["canonical_terminal_state"],
        "canonical_terminal_state": canonical["canonical_terminal_state"],
        "unblock_classification": classification,
        "import_preview_eligible": classification
        == "auto_promotable_import_preview_candidate",
        "evidence_basis": {
            "source_terminal_state_counts": canonical.get("source_terminal_state_counts", {}),
            "source_shards": canonical.get("source_shards", []),
            "family_lanes": family_axis.get("family_lanes", []),
            "subfamily_lanes": family_axis.get("subfamily_lanes", []),
            "sequence_or_duplicate_statuses": summary["statuses"],
            "current_registry_overlap": axes.get("current_registry_overlap", {}),
            "selected_structures": summary["selected_structures"],
            "pdb_ids": summary["pdb_ids"],
            "alphafold_ids": summary["alphafold_ids"],
            "local_coordinate_matches": summary["local_coordinate_matches"],
            "approved_locator_matches": summary["approved_locator_matches"],
            "locator_feature_counts": summary["locator_feature_counts"],
            "repair_overlay_matches": [
                {
                    "candidate_id": row.get("candidate_id"),
                    "accession": row.get("accession"),
                    "repair_decision": row.get("repair_decision"),
                    "recommended_terminal_state_for_future_surface": row.get(
                        "recommended_terminal_state_for_future_surface"
                    ),
                    "remaining_blockers_after_repair_audit": row.get(
                        "remaining_blockers_after_repair_audit"
                    ),
                }
                for row in repair_matches
            ],
            "source_members": summary["source_rows"],
            "gate_evidence": {
                "ready_for_label_import_true": summary[
                    "gate_ready_for_label_import_true"
                ],
                "countable_label_candidate_true": summary[
                    "gate_countable_label_candidate_true"
                ],
                "ready_for_label_import_values": summary[
                    "gate_ready_for_label_import_values"
                ],
                "countable_label_candidate_values": summary[
                    "gate_countable_label_candidate_values"
                ],
            },
        },
        "blocker_basis": blocker_basis,
        "source_hashes": summary["source_hashes"],
        "next_action": next_action,
    }
    row["unblock_context_sha256"] = _canonical_sha256(
        {
            "canonical_key": row["canonical_key"],
            "terminal_state": row["terminal_state"],
            "unblock_classification": row["unblock_classification"],
            "blocker_basis": row["blocker_basis"],
            "source_hashes": row["source_hashes"],
        }
    )
    return row


def _validation(merged: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    canonical_counts = Counter(
        record["canonical_terminal_state"] for record in merged["canonical_records"]
    )
    target_counts = Counter(row["terminal_state"] for row in rows)
    merged_source_row_count = sum(merged.get("source_terminal_state_counts", {}).values())
    merged_canonical_source_member_count = sum(
        int(record.get("source_member_count", 0))
        for record in merged.get("canonical_records", [])
    )
    target_source_member_count = sum(
        len(row.get("evidence_basis", {}).get("source_members", [])) for row in rows
    )
    expected_target_counts = {
        state: canonical_counts.get(state, 0) for state in sorted(TARGET_CANONICAL_STATES)
    }
    violations: list[dict[str, Any]] = []
    for row in rows:
        if row["terminal_state"] not in TARGET_CANONICAL_STATES:
            violations.append(
                {"canonical_key": row["canonical_key"], "reason": "unexpected_terminal_state"}
            )
        if row["unblock_classification"] not in UNBLOCK_CLASSIFICATIONS:
            violations.append(
                {
                    "canonical_key": row["canonical_key"],
                    "reason": "unexpected_unblock_classification",
                }
            )
        for required in (
            "terminal_state",
            "evidence_basis",
            "blocker_basis",
            "source_hashes",
            "next_action",
        ):
            if required not in row or row[required] in (None, "", [], {}):
                violations.append(
                    {
                        "canonical_key": row["canonical_key"],
                        "reason": f"missing_required_{required}",
                    }
                )
    if dict(target_counts) != expected_target_counts:
        violations.append(
            {
                "reason": "target_terminal_counts_do_not_match_merged_surface",
                "expected": expected_target_counts,
                "observed": dict(target_counts),
            }
        )
    if sum(target_counts.values()) != 523:
        violations.append(
            {
                "reason": "target_row_count_not_current_expected_523",
                "observed": sum(target_counts.values()),
            }
        )
    if merged_source_row_count != merged_canonical_source_member_count:
        violations.append(
            {
                "reason": "merged_source_rows_do_not_reconcile_to_canonical_members",
                "merged_source_row_count": merged_source_row_count,
                "merged_canonical_source_member_count": (
                    merged_canonical_source_member_count
                ),
            }
        )
    return {
        "passed": not violations,
        "violation_count": len(violations),
        "violations": violations,
        "target_terminal_counts_match_merged_surface": dict(target_counts)
        == expected_target_counts,
        "source_canonical_counts": dict(sorted(canonical_counts.items())),
        "target_terminal_counts": dict(sorted(target_counts.items())),
        "all_rows_have_terminal_state_evidence_blockers_hashes_next_action": not any(
            violation["reason"].startswith("missing_required_") for violation in violations
        ),
        "merged_source_row_count": merged_source_row_count,
        "merged_canonical_source_member_count": merged_canonical_source_member_count,
        "merged_source_rows_reconcile_to_canonical_members": (
            merged_source_row_count == merged_canonical_source_member_count
        ),
        "target_source_member_count": target_source_member_count,
    }


def build_countable_label_unblocker_matrix(
    *,
    merged_surface_path: Path = DEFAULT_MERGED_SURFACE_PATH,
    repair_overlay_path: Path = DEFAULT_REPAIR_OVERLAY_PATH,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created_utc = created_utc or _utc_now_iso()
    merged = _read_json(merged_surface_path)
    repair_overlay = _read_json(repair_overlay_path) if repair_overlay_path.exists() else None
    source_rows, source_records = _load_source_rows(merged)
    coordinate_index = _index_coordinate_files()
    locator_index = _index_locator_evidence()
    target_records = [
        record
        for record in merged["canonical_records"]
        if record["canonical_terminal_state"] in TARGET_CANONICAL_STATES
    ]
    rows = [
        _matrix_row(
            record,
            source_rows=source_rows,
            source_records=source_records,
            coordinate_index=coordinate_index,
            locator_index=locator_index,
            repair_overlay=repair_overlay,
        )
        for record in target_records
    ]
    classification_counts = Counter(row["unblock_classification"] for row in rows)
    terminal_by_classification: dict[str, dict[str, int]] = {}
    for row in rows:
        terminal_by_classification.setdefault(row["unblock_classification"], {})
        terminal_by_classification[row["unblock_classification"]].setdefault(
            row["terminal_state"], 0
        )
        terminal_by_classification[row["unblock_classification"]][row["terminal_state"]] += 1

    import_preview_rows = [row for row in rows if row["import_preview_eligible"]]
    target_source_member_counts = Counter()
    for row in rows:
        target_source_member_counts[row["terminal_state"]] += len(
            row["evidence_basis"]["source_members"]
        )
    source_records_payload = {
        "merged_acceptance_surface": _source_record(merged_surface_path),
        "repair_overlay": _source_record(repair_overlay_path)
        if repair_overlay_path.exists()
        else None,
        "source_shards": source_records,
    }
    artifact = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc,
        "scope": (
            "Promotion/unblock matrix over non-reject canonical candidates from the "
            "current702 merged scale-out acceptance surface."
        ),
        "source_artifacts": source_records_payload,
        "guardrails": {
            "label_registry_edited": False,
            "imports_or_promotions_performed": False,
            "import_preview_artifact_built": bool(import_preview_rows),
            "locator_sidecars_copied_or_materialized_now": False,
            "coordinates_fetched_or_materialized_now": False,
            "ontology_edited": False,
            "train_test_splits_changed": False,
            "model_weights_fit_or_refit": False,
            "production_thresholds_changed": False,
            "heldout_training_or_tuning_performed": False,
            "mechanism_text_ec_rhea_ids_labels_target_names_or_source_ids_used_as_predictive_scoring_features": False,
            "provenance_and_rationale_fields_allowed": True,
            "reject_oos_and_review_only_signal_preserved": True,
        },
        "classification_policy": {
            "target_input_terminal_states": sorted(TARGET_CANONICAL_STATES),
            "terminal_classifications": sorted(UNBLOCK_CLASSIFICATIONS),
            "auto_promote_rule": (
                "Requires no current-registry overlap, no positive duplicate signal, "
                "ready_for_label_import=True, countable_label_candidate=True, and no "
                "locator/coordinate/family blockers in source rows."
            ),
            "coordinate_rule": (
                "Local coordinate files are hash-proven from existing artifacts only; "
                "coordinate files are not fetched or copied."
            ),
            "locator_rule": (
                "Existing approved locators are evidence only unless this surface has "
                "an explicit import gate; candidate sidecars are never copied."
            ),
        },
        "counts": {
            "merged_canonical_records": len(merged["canonical_records"]),
            "merged_source_row_count": sum(
                merged.get("source_terminal_state_counts", {}).values()
            ),
            "merged_canonical_source_member_count": sum(
                int(record.get("source_member_count", 0))
                for record in merged.get("canonical_records", [])
            ),
            "merged_source_terminal_state_counts": merged.get(
                "source_terminal_state_counts", {}
            ),
            "target_canonical_records": len(rows),
            "target_source_member_count": sum(target_source_member_counts.values()),
            "target_source_member_count_by_input_terminal_state": dict(
                sorted(target_source_member_counts.items())
            ),
            "input_terminal_state_counts": dict(
                sorted(Counter(row["terminal_state"] for row in rows).items())
            ),
            "unblock_classification_counts": dict(sorted(classification_counts.items())),
            "terminal_state_by_unblock_classification": {
                key: dict(sorted(value.items()))
                for key, value in sorted(terminal_by_classification.items())
            },
            "current_registry_overlap_blocked_rows": sum(
                1
                for row in rows
                if row["evidence_basis"]["current_registry_overlap"].get("overlap")
            ),
            "positive_duplicate_signal_rows": sum(
                1
                for row in rows
                if any(
                    blocker.startswith("positive_duplicate_screen:")
                    for blocker in row["blocker_basis"]
                )
            ),
            "rows_with_local_coordinate_file_matches": sum(
                1 for row in rows if row["evidence_basis"]["local_coordinate_matches"]
            ),
            "rows_with_approved_locator_matches": sum(
                1 for row in rows if row["evidence_basis"]["approved_locator_matches"]
            ),
            "rows_with_ready_for_label_import_true": sum(
                1
                for row in rows
                if row["evidence_basis"]["gate_evidence"]["ready_for_label_import_true"]
            ),
            "rows_with_countable_label_candidate_true": sum(
                1
                for row in rows
                if row["evidence_basis"]["gate_evidence"][
                    "countable_label_candidate_true"
                ]
            ),
            "import_preview_candidate_rows": len(import_preview_rows),
        },
        "rows": rows,
        "import_preview_candidates": [
            _import_preview_row(row) for row in import_preview_rows
        ],
    }
    artifact["validation_checks"] = _validation(merged, rows)
    return artifact


def _import_preview_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "canonical_key": row["canonical_key"],
        "source_terminal_state": row["terminal_state"],
        "unblock_context_sha256": row["unblock_context_sha256"],
        "source_hashes": row["source_hashes"],
        "next_action": "candidate only; no production import performed",
    }


def build_import_preview_artifact(
    matrix: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created_utc = created_utc or matrix["created_utc"]
    rows = matrix["import_preview_candidates"]
    return {
        "artifact_id": IMPORT_PREVIEW_ARTIFACT_ID,
        "schema_version": "v3.countable_label_unblocker_import_preview",
        "created_utc": created_utc,
        "source_matrix_artifact_id": matrix["artifact_id"],
        "source_matrix_sha256_context": _canonical_sha256(
            {
                "artifact_id": matrix["artifact_id"],
                "rows": [
                    row["unblock_context_sha256"]
                    for row in matrix["rows"]
                    if row["import_preview_eligible"]
                ],
            }
        ),
        "guardrails": {
            "production_registry_import_performed": False,
            "label_registry_edited": False,
            "locator_sidecars_copied_or_materialized_now": False,
            "coordinates_fetched_or_materialized_now": False,
        },
        "candidate_count": len(rows),
        "rows": rows,
    }


def render_countable_label_unblocker_report(matrix: dict[str, Any]) -> str:
    counts = matrix["counts"]
    lines: list[str] = [
        "# Countable Label Unblocker Matrix - current702 - 20260608",
        "",
        f"- Created UTC: `{matrix['created_utc']}`",
        f"- JSON artifact: `artifacts/v3_countable_label_unblocker_matrix_current702_{RUN_DATE}.json`",
        "- Source surface: `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`",
        "",
        "## Result",
        "",
        (
            "The unblocker consumed the non-reject canonical candidates from the "
            "merged scale-out surface and classified each row into a terminal "
            "machine action. No registry, import, sidecar, coordinate, ontology, "
            "threshold, model, split, training, or tuning surface was changed."
        ),
        "",
        f"- Target canonical rows: `{counts['target_canonical_records']}`",
        f"- Target source-member rows: `{counts['target_source_member_count']}`",
        f"- Merged source rows reconciled: `{counts['merged_source_row_count']}`",
        f"- Import-preview candidates: `{counts['import_preview_candidate_rows']}`",
        f"- Rows with `ready_for_label_import=True`: `{counts['rows_with_ready_for_label_import_true']}`",
        f"- Rows with `countable_label_candidate=True`: `{counts['rows_with_countable_label_candidate_true']}`",
        f"- Current-registry overlap blockers: `{counts['current_registry_overlap_blocked_rows']}`",
        f"- Positive duplicate-screen blockers: `{counts['positive_duplicate_signal_rows']}`",
        f"- Rows with local coordinate files found: `{counts['rows_with_local_coordinate_file_matches']}`",
        f"- Rows with approved locator matches: `{counts['rows_with_approved_locator_matches']}`",
        "",
        "## Input Terminal Counts",
        "",
    ]
    for state, count in counts["input_terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Target Source-Member Counts", ""])
    for state, count in counts[
        "target_source_member_count_by_input_terminal_state"
    ].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Unblock Classification Counts", ""])
    for state, count in counts["unblock_classification_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Classification By Input State", ""])
    lines.append("| Unblock classification | Input terminal mix |")
    lines.append("| --- | --- |")
    for classification, mix in counts["terminal_state_by_unblock_classification"].items():
        mix_text = ", ".join(f"`{state}`={count}" for state, count in mix.items())
        lines.append(f"| `{classification}` | {mix_text} |")
    lines.extend(["", "## Import Preview", ""])
    if counts["import_preview_candidate_rows"]:
        for row in matrix["import_preview_candidates"]:
            lines.append(f"- `{row['canonical_key']}`")
    else:
        lines.append(
            "- None. No target row had both `ready_for_label_import=True` and "
            "`countable_label_candidate=True`, and duplicate/current-registry "
            "screens still block several otherwise informative rows."
        )
    lines.extend(["", "## Mechanical Findings", ""])
    lines.append(
        "- Review-only rows are not countable by default: they carry evidence but no "
        "source gate grants import-preview authority in this surface."
    )
    lines.append(
        "- Family-decision rows are split between existing policy/default no-import "
        "resolutions, exact expert-only decisions, and hard missing source-free "
        "family evidence."
    )
    lines.append(
        "- Locator rows remain repair candidates unless a current duplicate signal "
        "or exact current-registry overlap blocks them earlier."
    )
    lines.append(
        "- Coordinate rows with local coordinate files were moved to locator repair; "
        "rows without local coordinates remain coordinate repair candidates."
    )
    lines.extend(["", "## Representative Next Actions", ""])
    for classification in sorted(matrix["counts"]["unblock_classification_counts"]):
        sample = next(
            row for row in matrix["rows"] if row["unblock_classification"] == classification
        )
        lines.append(
            f"- `{classification}` sample `{sample['canonical_key']}`: "
            f"{sample['next_action']}"
        )
    lines.extend(["", "## Validation", ""])
    validation = matrix["validation_checks"]
    lines.append(f"- Validation passed: `{validation['passed']}`")
    lines.append(
        "- Target counts match merged surface: "
        f"`{validation['target_terminal_counts_match_merged_surface']}`"
    )
    lines.append(
        "- Merged source rows reconcile to canonical members: "
        f"`{validation['merged_source_rows_reconcile_to_canonical_members']}`"
    )
    lines.append(
        "- Required row fields present: "
        f"`{validation['all_rows_have_terminal_state_evidence_blockers_hashes_next_action']}`"
    )
    return "\n".join(lines) + "\n"


def write_countable_label_unblocker_matrix(
    *,
    merged_surface_path: Path = DEFAULT_MERGED_SURFACE_PATH,
    repair_overlay_path: Path = DEFAULT_REPAIR_OVERLAY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    import_preview_path: Path | None = DEFAULT_IMPORT_PREVIEW_PATH,
    created_utc: str | None = None,
) -> dict[str, Any]:
    matrix = build_countable_label_unblocker_matrix(
        merged_surface_path=merged_surface_path,
        repair_overlay_path=repair_overlay_path,
        created_utc=created_utc,
    )
    _write_json(out_path, matrix)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_countable_label_unblocker_report(matrix), encoding="utf-8")
    if import_preview_path is not None and matrix["import_preview_candidates"]:
        _write_json(
            import_preview_path,
            build_import_preview_artifact(matrix, created_utc=matrix["created_utc"]),
        )
    return matrix
