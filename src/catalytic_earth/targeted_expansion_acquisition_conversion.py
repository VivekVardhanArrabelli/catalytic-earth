from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ID = "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608"
SCHEMA_VERSION = "v3.targeted_expansion_acquisition_conversion_screens"

DEFAULT_BATCH_PATH = Path(
    "artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md"
)
DEFAULT_OUT_PATH = Path(
    "artifacts/"
    "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json"
)

TERMINAL_STATES = (
    "review_only_evidence",
    "reject/OOS_preserve_signal",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "countable_candidate_preflight_only",
)

REQUIRED_SCREEN_AXES = (
    "current_reference_sequence_duplicate_screen",
    "current_countable_structural_screen",
    "external_all_vs_all_structural_cluster_assignment",
    "broad_sequence_neighborhood_duplicate_screen",
    "locator_coordinate_readiness",
    "label_factory_pre_promotion_readiness",
)

DEFAULT_SCREEN_PATHS = {
    "external_source_sequence_reference_screen_audit": (
        Path("artifacts/v3_external_source_sequence_reference_screen_audit_1025.json")
    ),
    "external_source_sequence_alignment_verification": (
        Path("artifacts/v3_external_source_sequence_alignment_verification_1025.json")
    ),
    "external_source_backend_sequence_search": (
        Path("artifacts/v3_external_source_backend_sequence_search_1025.json")
    ),
    "external_source_all_vs_all_sequence_search": (
        Path("artifacts/v3_external_source_all_vs_all_sequence_search_1025.json")
    ),
    "external_structural_cluster_index_all30": (
        Path("artifacts/v3_external_structural_cluster_index_1025_all30.json")
    ),
    "external_structural_tm_holdout_path_all30": (
        Path("artifacts/v3_external_structural_tm_holdout_path_1025_all30.json")
    ),
    "external_source_import_readiness_audit": (
        Path("artifacts/v3_external_source_import_readiness_audit_1025.json")
    ),
    "external_source_transfer_blocker_matrix": (
        Path("artifacts/v3_external_source_transfer_blocker_matrix_1025.json")
    ),
    "external_source_pilot_decisions_review_resolved": (
        Path("artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json")
    ),
    "external_source_pilot_terminal_decisions": (
        Path("artifacts/v3_external_source_pilot_terminal_decisions_1025.json")
    ),
    "external_source_pilot_representation_adjudication": (
        Path("artifacts/v3_external_source_pilot_representation_adjudication_1025.json")
    ),
    "external_source_representation_backend_sample": (
        Path("artifacts/v3_external_source_representation_backend_sample_1025.json")
    ),
    "external_hard_negative_new_backend_sequence_search": (
        Path("artifacts/v3_external_hard_negative_new_candidate_backend_sequence_search_1025.json")
    ),
    "external_hard_negative_new_current_countable_structural_screen": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_new_candidate_current_countable_structural_screen_1025.json"
        )
    ),
    "external_hard_negative_new_structural_cluster_index": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_new_candidate_structural_cluster_index_1025.json"
        )
    ),
    "external_hard_negative_new_structural_tm_holdout_path": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_new_candidate_structural_tm_holdout_path_1025.json"
        )
    ),
    "external_hard_negative_new_terminal_decisions": (
        Path("artifacts/v3_external_hard_negative_new_candidate_terminal_decisions_1025.json")
    ),
    "external_hard_negative_next_backend_sequence_search": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_backend_sequence_search_1025.json"
        )
    ),
    "external_hard_negative_next_all_vs_all_sequence_search": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_1025.json"
        )
    ),
    "external_hard_negative_next_current_countable_structural_screen": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_current_countable_structural_screen_1025.json"
        )
    ),
    "external_hard_negative_next_structural_cluster_index": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_structural_cluster_index_1025.json"
        )
    ),
    "external_hard_negative_next_structural_tm_holdout_path": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_structural_tm_holdout_path_1025.json"
        )
    ),
    "external_hard_negative_next_uniref_current_reference_screen": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_uniref_current_reference_screen_1025.json"
        )
    ),
    "external_hard_negative_next_targeted_uniref_check": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_targeted_uniref_check_1025.json"
        )
    ),
    "external_hard_negative_next_terminal_decisions": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_terminal_decisions_1025.json"
        )
    ),
    "external_hard_negative_next_duplicate_evidence_review": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_duplicate_evidence_review_1025.json"
        )
    ),
    "external_hard_negative_next_factory_import_gate": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_next_candidate_factory_import_gate_1025.json"
        )
    ),
    "external_hard_negative_second_tranche_current_countable_structural_screen": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_second_tranche_current_countable_structural_screen_1025.json"
        )
    ),
    "external_hard_negative_second_tranche_terminal_decisions": (
        Path(
            "artifacts/"
            "v3_external_hard_negative_second_tranche_terminal_decisions_1025.json"
        )
    ),
    "sequence_cluster_proxy_1025": Path("artifacts/v3_sequence_cluster_proxy_1025.json"),
    "sequence_distance_holdout_eval_1025": (
        Path("artifacts/v3_sequence_distance_holdout_eval_1025.json")
    ),
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
    return json.loads(path.read_text(encoding="utf-8"))


def _rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in (
        "rows",
        "review_items",
        "results",
        "entries",
        "candidate_rows",
        "queue_rows",
        "audit_rows",
        "decisions",
        "expert_import_decisions",
    ):
        rows = payload.get(key)
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
        if isinstance(rows, dict):
            return [row for row in rows.values() if isinstance(row, dict)]
    return []


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _strip_uniprot(value: Any) -> str:
    text = str(value)
    if text.startswith("uniprot:"):
        return text.split(":", 1)[1]
    return text


def _row_accessions(row: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key, value in row.items():
        lowered = key.lower()
        if key in {
            "accession",
            "accession_or_source_id",
            "candidate_id",
            "entry_id",
            "uniprot",
            "uniprot_id",
            "structure_id",
        } or "accession" in lowered or "uniprot" in lowered:
            values.extend(_strip_uniprot(item) for item in _as_list(value))
    return sorted({value for value in values if value and value != "None"})


def _accession_from_batch_row(row: dict[str, Any]) -> str:
    accession = row.get("accession_or_source_id")
    if accession:
        return _strip_uniprot(accession)
    candidate_id = row.get("candidate_id")
    if candidate_id:
        return _strip_uniprot(candidate_id)
    raise ValueError("acquisition row missing accession_or_source_id/candidate_id")


def _index_screen_rows(
    screen_payloads: dict[str, Any],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    by_accession: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for screen_name, payload in screen_payloads.items():
        for row in _rows_from_payload(payload):
            for accession in _row_accessions(row):
                by_accession[accession][screen_name].append(row)
    return {
        accession: {name: list(rows) for name, rows in by_screen.items()}
        for accession, by_screen in by_accession.items()
    }


def _rows_for(
    rows_by_screen: dict[str, list[dict[str, Any]]],
    *screen_names: str,
) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for screen_name in screen_names:
        for row in rows_by_screen.get(screen_name, []):
            rows.append((screen_name, row))
    return rows


def _contributing_source_hashes(
    screen_rows: list[tuple[str, dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for screen_name, _ in screen_rows:
        record = source_records.get(screen_name)
        if record is not None:
            hashes[screen_name] = str(record["sha256"])
    return hashes


def _has_status(statuses: list[str], *needles: str) -> bool:
    return any(any(needle in status for needle in needles) for status in statuses)


def _status_values(rows: list[tuple[str, dict[str, Any]]], *keys: str) -> list[str]:
    values: list[str] = []
    for _, row in rows:
        for key in keys:
            for value in _as_list(row.get(key)):
                if value not in (None, ""):
                    values.append(str(value))
    return sorted(set(values))


def _nearest_current_hit(rows: list[tuple[str, dict[str, Any]]]) -> dict[str, Any] | None:
    for _, row in rows:
        hit = row.get("nearest_current_countable_hit")
        if isinstance(hit, dict):
            keep = {
                key: hit.get(key)
                for key in (
                    "example_current_entry_id",
                    "current_entry_ids",
                    "current_label_types",
                    "current_target_fingerprint_ids",
                    "current_selected_structure_key",
                    "max_pair_tm_score",
                    "ttmscore",
                    "qtmscore",
                    "alntmscore",
                )
                if key in hit
            }
            return keep
    return None


def _current_reference_sequence_screen(
    accession: str,
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = _rows_for(
        rows_by_screen,
        "external_source_sequence_reference_screen_audit",
        "external_source_backend_sequence_search",
        "external_hard_negative_new_backend_sequence_search",
        "external_hard_negative_next_backend_sequence_search",
        "external_hard_negative_next_uniref_current_reference_screen",
        "external_hard_negative_next_targeted_uniref_check",
        "sequence_cluster_proxy_1025",
        "sequence_distance_holdout_eval_1025",
    )
    statuses = _status_values(
        rows,
        "search_status",
        "current_reference_screen_status",
        "targeted_uniref_check_status",
        "uniref_current_reference_screen_status",
        "holdout_status",
        "status",
    )
    exact_proxy_rows = [
        row
        for screen_name, row in rows
        if screen_name == "sequence_cluster_proxy_1025"
        and accession in {_strip_uniprot(value) for value in _as_list(row.get("reference_uniprot_ids"))}
    ]
    exact_proxy_available = "sequence_cluster_proxy_1025" in source_records
    exact_overlap = any(
        row.get("exact_reference_overlap") is True for _, row in rows
    ) or bool(exact_proxy_rows)
    exact_status = _has_status(
        statuses,
        "exact_reference_holdout",
        "preexisting_sequence_holdout_retained",
        "exact_reference_overlap_holdout",
    )
    near_status = any(
        status
        for status in statuses
        if "near_duplicate" in status
        and "no_near_duplicate" not in status
        and "no_current_reference_overlap" not in status
    )
    if exact_overlap or exact_status:
        screen_status = "exact_reference_or_sequence_holdout"
    elif near_status:
        screen_status = "near_duplicate_or_sequence_holdout"
    elif _has_status(
        statuses,
        "no_near_duplicate_signal",
        "current_reference_top_hits_aligned_no_alert",
        "uniref_current_reference_screen_no_current_reference_overlap",
        "targeted_uniref_nearest_reference_no_shared_cluster",
        "ok",
    ):
        screen_status = "no_near_duplicate_signal"
    elif exact_proxy_available:
        screen_status = "no_exact_current_reference_accession_proxy"
    elif rows:
        screen_status = "screen_present_status_unclassified"
    else:
        screen_status = "not_available"
    matched_entries: list[str] = []
    sequence_cluster_ids: list[str] = []
    for screen_name, row in rows:
        matched_entries.extend(str(value) for value in _as_list(row.get("matched_m_csa_entry_ids")))
        entry_id = row.get("entry_id")
        if (
            screen_name == "sequence_cluster_proxy_1025"
            and row in exact_proxy_rows
            and entry_id
            and not str(entry_id).startswith("uniprot:")
        ):
            matched_entries.append(str(entry_id))
        cluster_id = row.get("sequence_cluster_id")
        if cluster_id:
            sequence_cluster_ids.append(str(cluster_id))
    contributing_artifacts = {name for name, _ in rows}
    source_hashes = _contributing_source_hashes(rows, source_records)
    if exact_proxy_available:
        contributing_artifacts.add("sequence_cluster_proxy_1025")
        source_hashes["sequence_cluster_proxy_1025"] = str(
            source_records["sequence_cluster_proxy_1025"]["sha256"]
        )
    return {
        "axis": "current_reference_sequence_duplicate_screen",
        "status": screen_status,
        "screen_complete": screen_status != "not_available",
        "observed_statuses": statuses,
        "matched_current_entry_ids": sorted(set(matched_entries)),
        "sequence_cluster_ids": sorted(set(sequence_cluster_ids)),
        "contributing_artifacts": sorted(contributing_artifacts),
        "source_hashes": source_hashes,
    }


def _current_countable_structural_screen(
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = _rows_for(
        rows_by_screen,
        "external_hard_negative_new_current_countable_structural_screen",
        "external_hard_negative_next_current_countable_structural_screen",
        "external_hard_negative_second_tranche_current_countable_structural_screen",
    )
    statuses = _status_values(rows, "current_countable_structural_screen_status")
    duplicate_signal = any(
        status == "current_countable_structural_duplicate_signal"
        for status in statuses
    )
    no_signal = any(
        status == "no_current_countable_structural_duplicate_signal"
        for status in statuses
    )
    if duplicate_signal:
        screen_status = "current_countable_structural_duplicate_signal"
    elif no_signal:
        screen_status = "no_current_countable_structural_duplicate_signal"
    elif rows:
        screen_status = "screen_present_status_unclassified"
    else:
        screen_status = "not_available"
    high_hit_counts = [
        int(row.get("current_countable_high_tm_hit_count") or 0)
        for _, row in rows
        if row.get("current_countable_high_tm_hit_count") is not None
    ]
    return {
        "axis": "current_countable_structural_screen",
        "status": screen_status,
        "screen_complete": screen_status != "not_available",
        "observed_statuses": statuses,
        "max_current_countable_high_tm_hit_count": max(high_hit_counts)
        if high_hit_counts
        else 0,
        "nearest_current_countable_hit": _nearest_current_hit(rows),
        "contributing_artifacts": sorted({name for name, _ in rows}),
        "source_hashes": _contributing_source_hashes(rows, source_records),
    }


def _external_structural_cluster_assignment(
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = _rows_for(
        rows_by_screen,
        "external_structural_cluster_index_all30",
        "external_structural_tm_holdout_path_all30",
        "external_hard_negative_new_structural_cluster_index",
        "external_hard_negative_new_structural_tm_holdout_path",
        "external_hard_negative_next_structural_cluster_index",
        "external_hard_negative_next_structural_tm_holdout_path",
    )
    statuses = _status_values(
        rows,
        "structural_neighbor_cache_status",
        "structural_holdout_status",
        "structure_reference_status",
        "coordinate_status",
    )
    if _has_status(statuses, "external_structural_cluster_neighbor_at_or_above_threshold"):
        screen_status = "external_structural_cluster_neighbor_at_or_above_threshold"
    elif _has_status(statuses, "no_external_structural_neighbor_above_threshold"):
        screen_status = "external_structural_cluster_assigned_no_neighbor_above_threshold"
    elif _has_status(statuses, "ready_for_external_structure_indexing"):
        screen_status = "structure_reference_ready_cluster_assignment_pending"
    elif rows:
        screen_status = "screen_present_status_unclassified"
    else:
        screen_status = "not_available"
    nearest_neighbors: list[dict[str, Any]] = []
    cluster_ids: list[str] = []
    coordinate_paths: list[str] = []
    coordinate_hashes: list[str] = []
    for _, row in rows:
        neighbor = row.get("nearest_neighbor")
        if isinstance(neighbor, dict):
            nearest_neighbors.append(
                {
                    key: neighbor.get(key)
                    for key in ("accession", "tm_score")
                    if key in neighbor
                }
            )
        cluster_id = row.get("tm_cluster_id")
        if cluster_id:
            cluster_ids.append(str(cluster_id))
        coordinate_path = row.get("coordinate_path")
        if coordinate_path:
            coordinate_paths.append(str(coordinate_path))
        coordinate_digest = row.get("coordinate_digest_sha256")
        if coordinate_digest:
            coordinate_hashes.append(str(coordinate_digest))
    return {
        "axis": "external_all_vs_all_structural_cluster_assignment",
        "status": screen_status,
        "screen_complete": screen_status != "not_available",
        "observed_statuses": statuses,
        "tm_cluster_ids": sorted(set(cluster_ids)),
        "nearest_external_neighbors": nearest_neighbors[:3],
        "coordinate_paths": sorted(set(coordinate_paths)),
        "coordinate_sha256": sorted(set(coordinate_hashes)),
        "contributing_artifacts": sorted({name for name, _ in rows}),
        "source_hashes": _contributing_source_hashes(rows, source_records),
    }


def _broad_sequence_neighborhood_screen(
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = _rows_for(
        rows_by_screen,
        "external_source_sequence_alignment_verification",
        "external_source_all_vs_all_sequence_search",
        "external_hard_negative_next_all_vs_all_sequence_search",
        "external_hard_negative_next_duplicate_evidence_review",
        "external_hard_negative_next_uniref_current_reference_screen",
        "external_hard_negative_next_targeted_uniref_check",
    )
    statuses = _status_values(
        rows,
        "verification_status",
        "search_status",
        "external_all_vs_all_sequence_status",
        "duplicate_evidence_status",
        "targeted_uniref_check_status",
        "uniref_current_reference_screen_status",
    )
    near_duplicate = any(
        status
        for status in statuses
        if ("near_duplicate" in status or "shared_cluster" in status)
        and "no_near_duplicate" not in status
        and "no_shared_cluster" not in status
        and "no_current_reference_overlap" not in status
    )
    targeted_uniref_clear = _has_status(
        statuses,
        "targeted_uniref_nearest_reference_no_shared_cluster",
        "uniref_current_reference_screen_no_current_reference_overlap",
    )
    all_vs_all_clear = _has_status(
        statuses,
        "external_all_vs_all_no_near_duplicate_signal",
        "alignment_no_near_duplicate_signal",
    )
    duplicate_review_clear = _has_status(
        statuses,
        "bounded_duplicate_controls_clear_uniref_pending",
    )
    if near_duplicate:
        screen_status = "broad_sequence_near_duplicate_or_holdout"
    elif targeted_uniref_clear:
        screen_status = "targeted_uniref_current_reference_no_overlap"
    elif duplicate_review_clear:
        screen_status = "bounded_duplicate_controls_clear_uniref_wide_pending"
    elif all_vs_all_clear:
        screen_status = "external_all_vs_all_no_near_duplicate_signal"
    elif rows:
        screen_status = "screen_present_status_unclassified"
    else:
        screen_status = "not_available"
    blockers: list[str] = []
    for _, row in rows:
        blockers.extend(str(value) for value in _as_list(row.get("blockers")))
        blockers.extend(
            str(value) for value in _as_list(row.get("remaining_import_blockers"))
        )
    return {
        "axis": "broad_sequence_neighborhood_duplicate_screen",
        "status": screen_status,
        "screen_complete": screen_status != "not_available",
        "observed_statuses": statuses,
        "blockers": sorted(set(blockers)),
        "contributing_artifacts": sorted({name for name, _ in rows}),
        "source_hashes": _contributing_source_hashes(rows, source_records),
    }


def _locator_coordinate_readiness(
    batch_row: dict[str, Any],
    structural_screen: dict[str, Any],
    structural_cluster: dict[str, Any],
) -> dict[str, Any]:
    active_site = batch_row.get("active_site_or_locator_evidence", {}) or {}
    coordinate = (
        batch_row.get("predicted_coordinate_or_provenance_availability", {}) or {}
    )
    active_site_status = str(active_site.get("active_site_evidence_status") or "")
    active_site_features = active_site.get("active_site_feature_count")
    binding_features = active_site.get("binding_site_feature_count")
    if (
        "explicit_active_site" in active_site_status
        or (isinstance(active_site_features, int) and active_site_features > 0)
    ):
        locator_status = "source_free_locator_ready_explicit_active_site_source"
    elif active_site_status in {"not_sampled_metadata_blocked", "not_sampled_cap_reached", ""}:
        locator_status = "blocked_locator_active_site_not_sampled"
    else:
        locator_status = f"locator_status_{active_site_status}"

    coordinate_paths = list(structural_cluster.get("coordinate_paths", []))
    nearest_hit = structural_screen.get("nearest_current_countable_hit")
    if coordinate_paths:
        coordinate_status = "coordinate_materialized_for_external_screen"
    elif nearest_hit:
        coordinate_status = "coordinate_materialized_for_current_countable_screen"
    elif coordinate.get("coordinate_provenance_available") is True:
        coordinate_status = "coordinate_provenance_ready_materialization_pending"
    else:
        coordinate_status = "blocked_coordinate_no_source_free_provenance"
    return {
        "axis": "locator_coordinate_readiness",
        "status": f"{locator_status}|{coordinate_status}",
        "locator_status": locator_status,
        "coordinate_status": coordinate_status,
        "active_site_feature_count": active_site_features,
        "binding_site_feature_count": binding_features,
        "pdb_ids": sorted({str(value) for value in _as_list(coordinate.get("pdb_ids"))}),
        "alphafold_ids": sorted(
            {str(value) for value in _as_list(coordinate.get("alphafold_ids"))}
        ),
        "coordinate_paths": coordinate_paths,
        "screen_complete": True,
        "contributing_artifacts": ["targeted_expansion_factory_batch"],
        "source_hashes": {},
    }


def _label_factory_readiness(
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = _rows_for(
        rows_by_screen,
        "external_hard_negative_next_factory_import_gate",
        "external_hard_negative_new_terminal_decisions",
        "external_hard_negative_next_terminal_decisions",
        "external_hard_negative_second_tranche_terminal_decisions",
        "external_source_pilot_decisions_review_resolved",
        "external_source_pilot_terminal_decisions",
        "external_source_pilot_representation_adjudication",
        "external_source_import_readiness_audit",
        "external_source_transfer_blocker_matrix",
    )
    statuses = _status_values(
        rows,
        "factory_gate_status",
        "terminal_import_attempt_status",
        "terminal_review_decision_status",
        "normalized_decision_status",
        "readiness_status",
        "representation_control_adjudication_status",
        "review_status",
    )
    countable_preflight = any(
        row.get("countable_label_candidate") is True
        and (
            row.get("ready_for_label_import") is True
            or row.get("import_ready_candidate") is True
        )
        for _, row in rows
    )
    rejected_statuses = [
        status
        for status in statuses
        if status.startswith("rejected_")
        and status != "rejected_active_site_evidence_missing"
    ]
    active_site_rejections = [
        status for status in statuses if status == "rejected_active_site_evidence_missing"
    ]
    blockers: list[str] = []
    for _, row in rows:
        blockers.extend(str(value) for value in _as_list(row.get("blockers")))
        blockers.extend(
            str(value) for value in _as_list(row.get("remaining_import_blockers"))
        )
        blockers.extend(
            str(value) for value in _as_list(row.get("import_readiness_blockers"))
        )
    if countable_preflight:
        status = "countable_candidate_preflight_passed_import_not_performed"
    elif rejected_statuses:
        status = "terminal_review_reject_or_oos_preserve_signal"
    elif active_site_rejections:
        status = "terminal_review_blocked_locator_active_site_missing"
    elif _has_status(statuses, "blocked_by_active_site_sourcing", "blocked_by_active_site_gap"):
        status = "blocked_by_active_site_sourcing"
    elif rows:
        status = "pre_promotion_review_only_or_gate_incomplete"
    else:
        status = "not_available"
    return {
        "axis": "label_factory_pre_promotion_readiness",
        "status": status,
        "screen_complete": status != "not_available",
        "observed_statuses": statuses,
        "blockers": sorted(set(blockers)),
        "countable_preflight_source_signal": countable_preflight,
        "contributing_artifacts": sorted({name for name, _ in rows}),
        "source_hashes": _contributing_source_hashes(rows, source_records),
    }


def _build_screens(
    batch_row: dict[str, Any],
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    accession = _accession_from_batch_row(batch_row)
    current_reference = _current_reference_sequence_screen(
        accession, rows_by_screen, source_records
    )
    structural = _current_countable_structural_screen(rows_by_screen, source_records)
    structural_cluster = _external_structural_cluster_assignment(
        rows_by_screen, source_records
    )
    broad_sequence = _broad_sequence_neighborhood_screen(
        rows_by_screen, source_records
    )
    locator_coordinate = _locator_coordinate_readiness(
        batch_row, structural, structural_cluster
    )
    label_factory = _label_factory_readiness(rows_by_screen, source_records)
    return {
        "current_reference_sequence_duplicate_screen": current_reference,
        "current_countable_structural_screen": structural,
        "external_all_vs_all_structural_cluster_assignment": structural_cluster,
        "broad_sequence_neighborhood_duplicate_screen": broad_sequence,
        "locator_coordinate_readiness": locator_coordinate,
        "label_factory_pre_promotion_readiness": label_factory,
    }


def _mechanical_requirements(row: dict[str, Any]) -> dict[str, Any]:
    requirements = row.get("mechanical_unblock_requirements", {})
    return requirements if isinstance(requirements, dict) else {}


def _source_evidence_blockers(row: dict[str, Any]) -> set[str]:
    return {
        str(value)
        for value in _as_list(_mechanical_requirements(row).get("source_evidence_blockers"))
    }


def _terminal_state_and_rationale(
    batch_row: dict[str, Any],
    screens: dict[str, Any],
) -> tuple[str, str, list[str], str]:
    current_reference = screens["current_reference_sequence_duplicate_screen"]
    structural = screens["current_countable_structural_screen"]
    broad_sequence = screens["broad_sequence_neighborhood_duplicate_screen"]
    locator_coordinate = screens["locator_coordinate_readiness"]
    label_factory = screens["label_factory_pre_promotion_readiness"]
    source_blockers = _source_evidence_blockers(batch_row)

    if current_reference["status"] in {
        "exact_reference_or_sequence_holdout",
        "near_duplicate_or_sequence_holdout",
    }:
        return (
            "reject/OOS_preserve_signal",
            "current_reference_sequence_duplicate_or_holdout",
            ["current_reference_duplicate_or_holdout"],
            "current-reference sequence/cluster evidence indicates an exact or near duplicate holdout",
        )
    if structural["status"] == "current_countable_structural_duplicate_signal":
        return (
            "reject/OOS_preserve_signal",
            "current_countable_structural_duplicate",
            ["current_countable_structural_duplicate_signal"],
            "Foldseek/current-countable structural screen reports a duplicate-level current atlas neighbor",
        )
    if broad_sequence["status"] == "broad_sequence_near_duplicate_or_holdout":
        return (
            "reject/OOS_preserve_signal",
            "broad_sequence_neighborhood_duplicate",
            ["broad_sequence_near_duplicate_or_holdout"],
            "broad/all-vs-all sequence-neighborhood evidence indicates a duplicate holdout",
        )
    if label_factory["status"] == "terminal_review_reject_or_oos_preserve_signal":
        return (
            "reject/OOS_preserve_signal",
            "terminal_review_reject_or_oos",
            label_factory.get("observed_statuses", []),
            "pre-existing terminal review artifact rejected the row or preserved it as non-counting OOS evidence",
        )
    if label_factory["status"] == "countable_candidate_preflight_passed_import_not_performed":
        return (
            "countable_candidate_preflight_only",
            "factory_preflight_passed_import_not_performed",
            ["preflight_only_no_registry_change"],
            "existing label-factory/import-gate evidence marks the row import-ready, but this run performs no import or promotion",
        )
    if any(
        blocker in source_blockers
        for blocker in {
            "mechanism_lane_not_covered_by_existing_counterevidence_rules",
            "specific_ec_context_missing",
        }
    ):
        return (
            "blocked_family_decision",
            "source_context_or_family_lane_decision_required",
            sorted(source_blockers),
            "source context requires a lane/family decision before source-free screens can be interpreted",
        )
    if locator_coordinate["locator_status"].startswith("blocked_locator") or (
        label_factory["status"]
        in {
            "blocked_by_active_site_sourcing",
            "terminal_review_blocked_locator_active_site_missing",
        }
    ):
        return (
            "blocked_locator",
            "source_free_active_site_locator_not_ready",
            sorted(
                set(label_factory.get("blockers", []))
                | {"active_site_or_locator_evidence_missing"}
            ),
            "active-site residue/source locator evidence is missing or still sourcing-blocked",
        )
    if locator_coordinate["coordinate_status"].startswith("blocked_coordinate"):
        return (
            "blocked_coordinate",
            "coordinate_or_structure_provenance_not_ready",
            ["coordinate_or_structure_provenance_missing"],
            "no local coordinate path, PDB reference, or AlphaFold provenance is available for source-free structural screens",
        )
    if "terminal_duplicate_rejection_previous_tranche" in source_blockers:
        return (
            "reject/OOS_preserve_signal",
            "prior_terminal_duplicate_rejection_preserved",
            sorted(source_blockers),
            "source lineage records a prior terminal duplicate rejection; preserve the signal rather than retrying acquisition",
        )
    return (
        "review_only_evidence",
        "screened_review_only_no_promotion_authority",
        sorted(set(label_factory.get("blockers", []))),
        "source-free evidence is present but no import/promotion authority is granted in this conversion run",
    )


def _conversion_row(
    batch_row: dict[str, Any],
    rows_by_screen: dict[str, list[dict[str, Any]]],
    source_records: dict[str, dict[str, Any]],
    batch_source_record: dict[str, Any],
) -> dict[str, Any]:
    accession = _accession_from_batch_row(batch_row)
    screens = _build_screens(batch_row, rows_by_screen, source_records)
    terminal_state, route_basis, blockers, rationale = _terminal_state_and_rationale(
        batch_row, screens
    )
    screen_hashes: dict[str, str] = {}
    for screen in screens.values():
        screen_hashes.update(screen.get("source_hashes", {}))
    explicit_required = _mechanical_requirements(batch_row).get("next_required_screens")
    priority_screen_ready = bool(explicit_required)
    payload = {
        "candidate_id": batch_row.get("candidate_id"),
        "accession": accession,
        "display_name": batch_row.get("display_name"),
        "family_axis": batch_row.get("family_axis"),
        "input_admission_state": batch_row.get("admission_state"),
        "terminal_state": terminal_state,
        "terminal_route_basis": route_basis,
        "terminal_rationale": rationale,
        "terminal_blockers": blockers,
        "priority_screen_ready": priority_screen_ready,
        "input_required_screens": sorted(str(value) for value in _as_list(explicit_required)),
        "screens": screens,
        "source_row_context_sha256": batch_row.get("row_context_sha256"),
        "input_batch_sha256": batch_source_record["sha256"],
        "input_source_hashes": batch_row.get("source_hashes", {}),
        "screen_source_hashes": screen_hashes,
        "guardrails": {
            "countable_label_candidate": terminal_state
            == "countable_candidate_preflight_only",
            "ready_for_label_import": False,
            "import_or_promotion_performed": False,
        },
        "allowed_next_action": _next_action_for_state(terminal_state),
    }
    payload["conversion_context_sha256"] = _canonical_sha256(
        {
            "candidate_id": payload["candidate_id"],
            "source_row_context_sha256": payload["source_row_context_sha256"],
            "terminal_state": terminal_state,
            "terminal_route_basis": route_basis,
            "screens": {
                axis: {
                    "status": screen["status"],
                    "contributing_artifacts": screen["contributing_artifacts"],
                }
                for axis, screen in screens.items()
            },
        }
    )
    return payload


def _next_action_for_state(state: str) -> str:
    return {
        "review_only_evidence": (
            "preserve as review-only evidence until a separate controlled-promotion review"
        ),
        "reject/OOS_preserve_signal": (
            "preserve duplicate/OOS signal and do not retry the accession without new evidence"
        ),
        "blocked_locator": (
            "source explicit active-site residues or build a source-free locator packet"
        ),
        "blocked_coordinate": (
            "materialize coordinate/provenance before structural duplicate screening"
        ),
        "blocked_family_decision": (
            "resolve the family/lane decision before promotion or import discussion"
        ),
        "countable_candidate_preflight_only": (
            "hold for Vivek/main-thread controlled-promotion decision; do not import automatically"
        ),
    }[state]


def _screen_axis_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {
        axis: Counter() for axis in REQUIRED_SCREEN_AXES
    }
    for row in rows:
        for axis in REQUIRED_SCREEN_AXES:
            counts[axis][str(row["screens"][axis]["status"])] += 1
    return {axis: dict(counter) for axis, counter in counts.items()}


def _family_state_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        counts[str(row["family_axis"])][str(row["terminal_state"])] += 1
    return {axis: dict(counter) for axis, counter in sorted(counts.items())}


def _validation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    for row in rows:
        missing_axes = [
            axis for axis in REQUIRED_SCREEN_AXES if axis not in row.get("screens", {})
        ]
        if row["input_admission_state"] != "acquisition_needed":
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "input_row_not_acquisition_needed",
                }
            )
        if row["terminal_state"] not in TERMINAL_STATES:
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "terminal_state_not_allowed",
                }
            )
        if row["terminal_state"] == "acquisition_needed":
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "acquisition_needed_not_converted",
                }
            )
        if row["guardrails"]["import_or_promotion_performed"]:
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "import_or_promotion_performed",
                }
            )
        if not row["input_source_hashes"] or not row["input_batch_sha256"]:
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "missing_input_source_hashes",
                }
            )
        if missing_axes:
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "missing_required_screen_axes",
                    "missing_axes": missing_axes,
                }
            )
        if not row.get("conversion_context_sha256"):
            violations.append(
                {
                    "candidate_id": row["candidate_id"],
                    "reason": "missing_conversion_context_sha256",
                }
            )
    return {
        "passed": not violations,
        "rows_checked": len(rows),
        "violation_count": len(violations),
        "violations": violations,
        "required_screen_axes": list(REQUIRED_SCREEN_AXES),
        "all_rows_terminal_state_allowed": all(
            row["terminal_state"] in TERMINAL_STATES for row in rows
        ),
        "all_rows_converted_from_acquisition_needed": all(
            row["input_admission_state"] == "acquisition_needed"
            and row["terminal_state"] != "acquisition_needed"
            for row in rows
        ),
        "no_imports_or_promotions": all(
            not row["guardrails"]["import_or_promotion_performed"] for row in rows
        ),
        "all_rows_have_required_screen_axes": all(
            all(axis in row.get("screens", {}) for axis in REQUIRED_SCREEN_AXES)
            for row in rows
        ),
        "all_rows_have_conversion_context_hashes": all(
            bool(row.get("conversion_context_sha256")) for row in rows
        ),
        "all_rows_have_input_source_hashes": all(
            bool(row.get("input_source_hashes")) and bool(row.get("input_batch_sha256"))
            for row in rows
        ),
    }


def _markdown_table_text(value: Any) -> str:
    return str(value).replace("|", "\\|")


def _markdown_code_cell(value: Any) -> str:
    return f"`{_markdown_table_text(value)}`"


def build_targeted_expansion_acquisition_conversion_screens(
    *,
    batch_payload: dict[str, Any],
    batch_source_record: dict[str, Any],
    screen_payloads: dict[str, Any],
    screen_source_records: dict[str, dict[str, Any]],
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    candidate_rows = [
        row
        for row in batch_payload.get("candidate_rows", [])
        if isinstance(row, dict) and row.get("admission_state") == "acquisition_needed"
    ]
    screen_index = _index_screen_rows(screen_payloads)
    rows = [
        _conversion_row(
            row,
            screen_index.get(_accession_from_batch_row(row), {}),
            screen_source_records,
            batch_source_record,
        )
        for row in candidate_rows
    ]
    rows.sort(key=lambda row: (not row["priority_screen_ready"], row["family_axis"], row["candidate_id"]))
    state_counts = Counter(str(row["terminal_state"]) for row in rows)
    priority_rows = [row for row in rows if row["priority_screen_ready"]]
    non_priority_rows = [row for row in rows if not row["priority_screen_ready"]]
    artifact = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "source_batch_artifact": batch_source_record,
        "screen_source_artifacts": screen_source_records,
        "scope": (
            "source-free conversion screens for acquisition_needed rows from the "
            "first targeted expansion factory batch; non-importing states only"
        ),
        "candidate_count": len(rows),
        "priority_screen_ready_count": len(priority_rows),
        "non_priority_acquisition_count": len(non_priority_rows),
        "terminal_state_counts": {state: state_counts.get(state, 0) for state in TERMINAL_STATES},
        "priority_terminal_state_counts": dict(
            Counter(str(row["terminal_state"]) for row in priority_rows)
        ),
        "non_priority_terminal_state_counts": dict(
            Counter(str(row["terminal_state"]) for row in non_priority_rows)
        ),
        "family_terminal_state_counts": _family_state_counts(rows),
        "screen_axis_status_counts": _screen_axis_counts(rows),
        "guardrails": {
            "label_registry_edited": False,
            "ontology_edited": False,
            "imports_or_promotions_performed": False,
            "train_test_splits_changed": False,
            "model_weights_fit_or_refit": False,
            "production_thresholds_changed": False,
            "heldout_mcsa_rows_used_for_training_or_tuning": False,
            "mechanism_text_or_ids_used_as_scoring_features": False,
            "source_ids_or_target_names_used_as_scoring_features": False,
        },
        "routing_policy": {
            "terminal_states": list(TERMINAL_STATES),
            "required_screen_axes": list(REQUIRED_SCREEN_AXES),
            "countable_candidate_preflight_only_is_not_import": True,
            "terminal_routing_priority": [
                "current-reference exact or near duplicate holdout",
                "current-countable structural duplicate",
                "broad sequence-neighborhood duplicate holdout",
                "existing terminal reject/OOS review decision",
                "existing factory preflight pass with no import performed",
                "family/lane decision blockers",
                "locator and coordinate blockers",
                "review-only evidence carryover",
            ],
        },
        "rows": rows,
    }
    artifact["validation_checks"] = _validation(rows)
    return artifact


def render_acquisition_conversion_report(artifact: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Targeted Expansion Acquisition Conversion Screens",
        "",
        f"Run: `{artifact['created_utc']}`",
        "",
        (
            "Non-importing conversion/screening artifact for the first targeted "
            "expansion factory batch. No labels, registries, ontologies, splits, "
            "model weights, thresholds, or imports were changed."
        ),
        "",
        "## Summary",
        "",
        f"- Acquisition rows screened: `{artifact['candidate_count']}`",
        f"- Priority screen-ready rows: `{artifact['priority_screen_ready_count']}`",
        f"- Expanded non-priority rows: `{artifact['non_priority_acquisition_count']}`",
        f"- Validation passed: `{artifact['validation_checks']['passed']}`",
        "",
        "## Terminal States",
        "",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Priority Rows", ""])
    for state, count in sorted(artifact["priority_terminal_state_counts"].items()):
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Priority Row Outcome Matrix", ""])
    lines.append(
        "| Candidate | Terminal state | Current-reference sequence | "
        "Current-countable structure | Broad sequence | Route basis |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in [row for row in artifact["rows"] if row["priority_screen_ready"]]:
        screens = row["screens"]
        lines.append(
            f"| {_markdown_code_cell(row['candidate_id'])} | "
            f"{_markdown_code_cell(row['terminal_state'])} | "
            f"{_markdown_code_cell(screens['current_reference_sequence_duplicate_screen']['status'])} | "
            f"{_markdown_code_cell(screens['current_countable_structural_screen']['status'])} | "
            f"{_markdown_code_cell(screens['broad_sequence_neighborhood_duplicate_screen']['status'])} | "
            f"{_markdown_code_cell(row['terminal_route_basis'])} |"
        )
    lines.extend(["", "## Family Routing", ""])
    lines.append("| Family axis | Terminal mix |")
    lines.append("| --- | --- |")
    for family_axis, counts in artifact["family_terminal_state_counts"].items():
        mix = ", ".join(
            f"{_markdown_table_text(state)}={count}"
            for state, count in sorted(counts.items())
        )
        lines.append(f"| {_markdown_code_cell(family_axis)} | {mix} |")
    lines.extend(["", "## Screen Axis Coverage", ""])
    lines.append("| Axis | Status mix |")
    lines.append("| --- | --- |")
    for axis, counts in artifact["screen_axis_status_counts"].items():
        mix = ", ".join(
            f"{_markdown_table_text(status)}={count}"
            for status, count in sorted(counts.items())
        )
        lines.append(f"| {_markdown_code_cell(axis)} | {mix} |")
    lines.extend(["", "## Countable Preflight Only", ""])
    preflight_rows = [
        row
        for row in artifact["rows"]
        if row["terminal_state"] == "countable_candidate_preflight_only"
    ]
    if preflight_rows:
        for row in preflight_rows:
            lines.append(
                f"- `{row['candidate_id']}` via `{row['family_axis']}`: "
                "factory preflight/import-ready evidence exists, but no import was performed."
            )
    else:
        lines.append("- None.")
    lines.extend(["", "## Remaining Blockers", ""])
    for state in ("blocked_locator", "blocked_coordinate", "blocked_family_decision"):
        blocked = [row for row in artifact["rows"] if row["terminal_state"] == state]
        lines.append(f"- `{state}`: {len(blocked)}")
        for row in blocked[:12]:
            lines.append(f"  - `{row['candidate_id']}`: {row['allowed_next_action']}")
        if len(blocked) > 12:
            lines.append(f"  - ... {len(blocked) - 12} more")
    locator_blockers = [
        row for row in artifact["rows"] if row["terminal_state"] == "blocked_locator"
    ]
    if locator_blockers:
        lines.extend(["", "## Locator Blocker Queue", ""])
        lines.append(
            "| Family axis | Candidate | Current-reference sequence | "
            "Structure | Locator/coordinate |"
        )
        lines.append("| --- | --- | --- | --- | --- |")
        for row in locator_blockers:
            screens = row["screens"]
            lines.append(
                f"| {_markdown_code_cell(row['family_axis'])} | "
                f"{_markdown_code_cell(row['candidate_id'])} | "
                f"{_markdown_code_cell(screens['current_reference_sequence_duplicate_screen']['status'])} | "
                f"{_markdown_code_cell(screens['current_countable_structural_screen']['status'])} | "
                f"{_markdown_code_cell(screens['locator_coordinate_readiness']['status'])} |"
            )
    family_blockers = [
        row
        for row in artifact["rows"]
        if row["terminal_state"] == "blocked_family_decision"
    ]
    if family_blockers:
        grouped_family_blockers: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in family_blockers:
            grouped_family_blockers[str(row["family_axis"])].append(row)
        lines.extend(["", "## Family Decision Blocker Queue", ""])
        lines.append(
            "| Family axis | Candidate | Current-reference sequence | "
            "Structure | Locator/coordinate |"
        )
        lines.append("| --- | --- | --- | --- | --- |")
        for family_axis, rows in sorted(grouped_family_blockers.items()):
            for row in rows:
                screens = row["screens"]
                lines.append(
                    f"| {_markdown_code_cell(family_axis)} | "
                    f"{_markdown_code_cell(row['candidate_id'])} | "
                    f"{_markdown_code_cell(screens['current_reference_sequence_duplicate_screen']['status'])} | "
                    f"{_markdown_code_cell(screens['current_countable_structural_screen']['status'])} | "
                    f"{_markdown_code_cell(screens['locator_coordinate_readiness']['status'])} |"
                )
    lines.extend(["", "## Representative Converted Rows", ""])
    lines.append("| Candidate | Family axis | Terminal state | Route basis |")
    lines.append("| --- | --- | --- | --- |")
    for row in artifact["rows"][:40]:
        lines.append(
            f"| {_markdown_code_cell(row['candidate_id'])} | "
            f"{_markdown_code_cell(row['family_axis'])} | "
            f"{_markdown_code_cell(row['terminal_state'])} | "
            f"{_markdown_code_cell(row['terminal_route_basis'])} |"
        )
    lines.extend(
        [
            "",
            "## Controlled Promotion Recommendation",
            "",
            (
                "Do not import or promote labels from this artifact automatically. "
                "The next controlled action is human review of the preflight-only "
                "and review-only rows, with duplicate/OOS rows preserved as "
                "non-counting evidence and blocker rows repaired mechanically first."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def write_targeted_expansion_acquisition_conversion_screens(
    *,
    batch_path: Path = DEFAULT_BATCH_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    screen_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    selected_screen_paths = dict(DEFAULT_SCREEN_PATHS if screen_paths is None else screen_paths)
    batch_payload = _read_json(batch_path)
    batch_source_record = _source_record(batch_path)
    screen_payloads: dict[str, Any] = {}
    screen_source_records: dict[str, dict[str, Any]] = {}
    for name, path in selected_screen_paths.items():
        if not path.exists():
            continue
        screen_payloads[name] = _read_json(path)
        screen_source_records[name] = _source_record(path)
    artifact = build_targeted_expansion_acquisition_conversion_screens(
        batch_payload=batch_payload,
        batch_source_record=batch_source_record,
        screen_payloads=screen_payloads,
        screen_source_records=screen_source_records,
        created_utc=created_utc,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_acquisition_conversion_report(artifact), encoding="utf-8")
    return artifact
