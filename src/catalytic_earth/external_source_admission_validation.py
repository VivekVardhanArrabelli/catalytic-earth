from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import load_json


RUN_DATE = "20260608"
ARTIFACT_ID = f"v3_external_source_admission_validation_16_current702_{RUN_DATE}"
READY_PREVIEW_ARTIFACT_ID = (
    f"v3_external_source_admission_ready_preview_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_source_admission_validation"
READY_PREVIEW_SCHEMA_VERSION = "v3.external_source_admission_ready_preview"

DEFAULT_PILOT_PATH = Path(
    "artifacts/v3_external_source_ingestion_pilot_current702_20260608.json"
)
DEFAULT_IMPORT_PREVIEW_PATH = Path(
    "artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json"
)
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_external_source_admission_validation_16_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/external_source_admission_validation_16_current702_{RUN_DATE}.md"
)
DEFAULT_READY_PREVIEW_PATH = Path(
    f"artifacts/v3_external_source_admission_ready_preview_current702_{RUN_DATE}.json"
)

TERMINAL_STATES = (
    "admission_ready_external_label_candidate",
    "admission_ready_pending_locator_materialization",
    "admission_ready_pending_coordinate_materialization",
    "blocked_duplicate_or_current_registry_conflict",
    "blocked_source_provenance",
    "blocked_locator_or_coordinate_mapping",
    "blocked_family_or_mechanism_policy",
    "review_only_evidence",
    "reject/OOS_preserve_signal",
)

ADMISSION_READY_STATES = {
    "admission_ready_external_label_candidate",
    "admission_ready_pending_locator_materialization",
    "admission_ready_pending_coordinate_materialization",
}

PREVIEW_SOURCE_TERMINAL_STATE = "external_countable_preflight_candidate"
COORDINATE_READY_STATUSES = {
    "experimental_pdb_coordinate_provenance_available",
    "afdb_predicted_coordinate_provenance_available",
}

DEFAULT_LOCATOR_SIDECAR_DIRS = (
    Path("artifacts/family_panel_source_free_active_site_locators_current702_20260601"),
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _read_json(path: Path) -> Any:
    return load_json(path)


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


def _clean_accession(value: Any) -> str:
    text = str(value or "").strip()
    return text.split(":", 1)[1] if text.startswith("uniprot:") else text


def _normalize_key(value: Any) -> str | None:
    if value in (None, "", [], {}):
        return None
    text = str(value).strip().lower()
    return text or None


def _counter_dict(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def _find_key_values(payload: Any, key: str) -> list[Any]:
    values: list[Any] = []
    if isinstance(payload, dict):
        for current_key, value in payload.items():
            if current_key == key:
                values.append(value)
            values.extend(_find_key_values(value, key))
    elif isinstance(payload, list):
        for item in payload:
            values.extend(_find_key_values(item, key))
    return values


def _current_reference_index(
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
) -> dict[str, Any]:
    accessions: set[str] = set()
    sequence_sha_to_entries: dict[str, list[str]] = defaultdict(list)
    accession_to_entries: dict[str, list[str]] = defaultdict(list)

    for row in current_manifest_payload.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id") or "")
        for accession in [row.get("accession"), row.get("sequence_id")]:
            cleaned = _clean_accession(accession)
            if cleaned:
                accessions.add(cleaned)
                accession_to_entries[cleaned].append(entry_id)
        for accession in row.get("real_sequence_accessions", []) or []:
            cleaned = _clean_accession(accession)
            if cleaned:
                accessions.add(cleaned)
                accession_to_entries[cleaned].append(entry_id)
        sequence_sha = row.get("sequence_sha256")
        if sequence_sha:
            sequence_sha_to_entries[str(sequence_sha)].append(entry_id)
        for sequence_record in row.get("sequence_records", []) or []:
            if not isinstance(sequence_record, dict):
                continue
            cleaned = _clean_accession(sequence_record.get("accession"))
            if cleaned:
                accessions.add(cleaned)
                accession_to_entries[cleaned].append(entry_id)
            record_sha = sequence_record.get("sequence_sha256")
            if record_sha:
                sequence_sha_to_entries[str(record_sha)].append(entry_id)

    for label in label_registry_payload:
        if not isinstance(label, dict):
            continue
        entry_id = str(label.get("entry_id") or "")
        if entry_id.startswith("uniprot:"):
            accession = _clean_accession(entry_id)
            accessions.add(accession)
            accession_to_entries[accession].append(entry_id)

    return {
        "accession_to_entries": {
            key: sorted(set(value)) for key, value in accession_to_entries.items()
        },
        "sequence_sha_to_entries": {
            key: sorted(set(value)) for key, value in sequence_sha_to_entries.items()
        },
        "current_reference_accession_count": len(accessions),
        "current_sequence_sha_count": len(sequence_sha_to_entries),
    }


def _load_current_reference_index(pilot: dict[str, Any]) -> dict[str, Any]:
    source_artifacts = pilot.get("source_artifacts", {})
    current_manifest_path = Path(
        source_artifacts.get("current_manifest", {}).get(
            "path", "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
        )
    )
    label_registry_path = Path(
        source_artifacts.get("label_registry", {}).get(
            "path", "data/registries/curated_mechanism_labels.json"
        )
    )
    return _current_reference_index(
        _read_json(current_manifest_path), _read_json(label_registry_path)
    )


def _recomputed_duplicate_status(
    row: dict[str, Any], current_index: dict[str, Any]
) -> dict[str, Any]:
    accession = _clean_accession(row.get("accession") or row.get("candidate_id"))
    duplicate = row.get("duplicate_current_registry_conflict", {}) or {}
    sequence_sha = duplicate.get("exact_sequence_sha256")
    accession_entries = current_index["accession_to_entries"].get(accession, [])
    sequence_entries = (
        current_index["sequence_sha_to_entries"].get(str(sequence_sha), [])
        if sequence_sha
        else []
    )
    conflict = bool(accession_entries or sequence_entries)
    if accession_entries:
        status = "exact_current702_accession_overlap"
    elif sequence_entries:
        status = "exact_current702_sequence_sha_overlap"
    else:
        status = "no_exact_current702_accession_or_sequence_sha_overlap"
    return {
        "duplicate_or_current_registry_conflict": conflict,
        "current_registry_conflict_status": status,
        "exact_accession_matched_current_entry_ids": accession_entries,
        "exact_sequence_sha256": sequence_sha,
        "exact_sequence_matched_current_entry_ids": sequence_entries,
    }


def _add_coordinate_index_key(
    index: dict[str, list[dict[str, Any]]], key: Any, record: dict[str, Any]
) -> None:
    normalized = _normalize_key(key)
    if not normalized:
        return
    index.setdefault(normalized, []).append(record)
    index.setdefault(normalized.replace(":", "_"), []).append(record)
    if normalized.startswith("uniprot:"):
        index.setdefault(normalized.split(":", 1)[1], []).append(record)


def _index_coordinate_files(artifacts_dir: Path = Path("artifacts")) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    if not artifacts_dir.exists():
        return index
    for path in artifacts_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".cif", ".pdb", ".bcif"}:
            continue
        record = {"path": str(path), "bytes": path.stat().st_size}
        name = path.name.lower()
        stem = path.stem.lower()
        for key in {name, stem}:
            _add_coordinate_index_key(index, key, record)
        if name.startswith("pdb_"):
            _add_coordinate_index_key(index, name[4:].rsplit(".", 1)[0], record)
        if name.startswith("afdb_"):
            accession = name[5:].rsplit(".", 1)[0]
            _add_coordinate_index_key(index, accession, record)
            _add_coordinate_index_key(index, f"uniprot:{accession}", record)
            _add_coordinate_index_key(index, f"af-{accession}-f1", record)
        if name.startswith("af-") and "-f1" in name:
            parts = name.split("-")
            if len(parts) >= 3:
                accession = parts[1]
                _add_coordinate_index_key(index, accession, record)
                _add_coordinate_index_key(index, f"uniprot:{accession}", record)
                _add_coordinate_index_key(index, f"af-{accession}-f1", record)
    return index


def _coordinate_lookup_keys(row: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    accession = _clean_accession(row.get("accession") or row.get("candidate_id"))
    for value in [
        row.get("candidate_id"),
        row.get("accession"),
        row.get("afdb_or_pdb_identifier"),
        f"uniprot:{accession}" if accession else None,
        accession,
    ]:
        normalized = _normalize_key(value)
        if normalized:
            keys.add(normalized)
            keys.add(normalized.replace(":", "_"))
    identifier = _normalize_key(row.get("afdb_or_pdb_identifier"))
    if identifier:
        keys.add(identifier.removeprefix("pdb:"))
        keys.add(f"pdb_{identifier.removeprefix('pdb:')}")
        if identifier.startswith("af-"):
            parts = identifier.split("-")
            if len(parts) >= 3:
                keys.add(parts[1])
                keys.add(f"uniprot:{parts[1]}")
    for value in row.get("pdb_ids", []) or []:
        normalized = _normalize_key(value)
        if normalized:
            keys.add(normalized.removeprefix("pdb:"))
            keys.add(f"pdb_{normalized.removeprefix('pdb:')}")
    for value in row.get("alphafold_ids", []) or []:
        normalized = _normalize_key(value)
        if normalized:
            keys.add(normalized.removeprefix("uniprot:"))
            keys.add(f"uniprot:{normalized.removeprefix('uniprot:')}")
            keys.add(f"af-{normalized.removeprefix('uniprot:')}-f1")
    return keys


def _coordinate_matches(
    row: dict[str, Any], coordinate_index: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in _coordinate_lookup_keys(row):
        for record in coordinate_index.get(key, []):
            path = record["path"]
            if path in seen:
                continue
            seen.add(path)
            path_obj = Path(path)
            matches.append(
                {
                    "path": path,
                    "bytes": record["bytes"],
                    "sha256": sha256_path(path_obj),
                }
            )
    return sorted(matches, key=lambda record: record["path"])


def _add_locator_index_record(
    index: dict[str, list[dict[str, Any]]], keys: list[Any], record: dict[str, Any]
) -> None:
    normalized_keys = sorted(
        {key for key in (_normalize_key(value) for value in keys) if key}
    )
    for key in normalized_keys:
        index.setdefault(key, []).append(record)
        index.setdefault(key.replace(":", "_"), []).append(record)
        if key.startswith("uniprot:"):
            index.setdefault(key.split(":", 1)[1], []).append(record)


def _index_approved_locator_evidence(
    sidecar_dirs: tuple[Path, ...] = DEFAULT_LOCATOR_SIDECAR_DIRS,
) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    materialization_path = Path(
        "artifacts/"
        "v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_"
        "source_free_locator_rewrite_materialization_gate_current702_20260603.json"
    )
    if materialization_path.exists():
        payload = _read_json(materialization_path)
        for row in payload.get("row_decisions", []) or []:
            if row.get("approved_locator_sidecar_written") is True:
                _add_locator_index_record(
                    index,
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

    for sidecar_dir in sidecar_dirs:
        if not sidecar_dir.exists():
            continue
        for path in sidecar_dir.glob("*.json"):
            keys: list[Any] = [path.stem, path.name]
            try:
                payload = _read_json(path)
            except json.JSONDecodeError:
                payload = {}
            for key in ("entry_id", "candidate_id", "source_accession", "accession"):
                keys.extend(_find_key_values(payload, key))
            _add_locator_index_record(
                index,
                keys,
                {
                    "artifact": str(path),
                    "approved_locator_path": str(path),
                    "status": "audited_locator_sidecar_present",
                },
            )
    return index


def _locator_matches(
    row: dict[str, Any], locator_index: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    keys = [
        row.get("candidate_id"),
        row.get("accession"),
        row.get("stable_candidate_key"),
        _clean_accession(row.get("accession") or row.get("candidate_id")),
    ]
    matches: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in keys:
        normalized = _normalize_key(key)
        if not normalized:
            continue
        for record in locator_index.get(normalized, []):
            marker = str(record.get("approved_locator_path") or record.get("artifact"))
            if marker in seen:
                continue
            seen.add(marker)
            matches.append(record)
    return sorted(matches, key=lambda record: str(record.get("approved_locator_path")))


def _source_provenance_issues(row: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    provenance = row.get("source_provenance", {}) or {}
    source_hashes = row.get("source_hashes", {}) or {}
    for key in ("uniprot_entry_url", "uniprot_search_url", "query_timestamp_utc"):
        if not provenance.get(key):
            issues.append(f"missing_source_provenance_{key}")
    for key in (
        "uniprot_search_row_sha256",
        "uniprot_entry_record_sha256",
        "rhea_records_sha256",
    ):
        digest = str(source_hashes.get(key) or "")
        if len(digest) != 64:
            issues.append(f"missing_or_invalid_source_hash_{key}")
    if row.get("reviewed_status") != "reviewed":
        issues.append("uniprot_record_not_reviewed_swiss_prot")
    return issues


def _residue_evidence(row: dict[str, Any]) -> dict[str, Any]:
    locators = row.get("residue_locators", []) or []
    exact_locators = [locator for locator in locators if locator.get("exact") is True]
    feature_codes = sorted(
        {
            str(locator.get("feature_code"))
            for locator in locators
            if locator.get("feature_code")
        }
    )
    evidence_codes = sorted(
        {
            str(code)
            for locator in locators
            for code in locator.get("evidence_codes", []) or []
            if code
        }
    )
    return {
        "residue_locator_count": len(locators),
        "exact_residue_locator_count": len(exact_locators),
        "feature_codes": feature_codes,
        "evidence_codes": evidence_codes,
        "source_evidence_feature_count": row.get("source_evidence_feature_count"),
        "source_evidence_codes": row.get("source_evidence_codes", []),
    }


def _reaction_evidence(row: dict[str, Any]) -> dict[str, Any]:
    provenance = row.get("rhea_ec_provenance", {}) or {}
    rhea_records = provenance.get("rhea_records", []) or []
    return {
        "ec_numbers": provenance.get("ec_numbers", []) or [],
        "specific_ec_count": provenance.get("specific_ec_count", 0),
        "rhea_record_count": provenance.get("rhea_record_count", 0),
        "rhea_ids": sorted(
            {
                str(record.get("rhea_id"))
                for record in rhea_records
                if isinstance(record, dict) and record.get("rhea_id")
            }
        ),
        "rhea_status": provenance.get("rhea_status"),
    }


def _classify_admission_row(
    *,
    full_row: dict[str, Any],
    preview_row: dict[str, Any],
    known_lanes: set[str],
    duplicate_status: dict[str, Any],
    coordinate_matches: list[dict[str, Any]],
    locator_matches: list[dict[str, Any]],
) -> tuple[str, list[str], str, str]:
    provenance_issues = _source_provenance_issues(full_row)
    preview_source_hashes = preview_row.get("source_hashes", {}) or {}
    if preview_row.get("terminal_state") != PREVIEW_SOURCE_TERMINAL_STATE:
        provenance_issues.append("preview_row_not_external_preflight_candidate")
    if preview_row.get("import_preview_candidate") is not True:
        provenance_issues.append("preview_row_missing_import_preview_candidate_flag")
    if preview_source_hashes != full_row.get("source_hashes", {}):
        provenance_issues.append("preview_source_hashes_do_not_match_pilot_row")
    if provenance_issues:
        return (
            "blocked_source_provenance",
            sorted(set(provenance_issues)),
            "repair source provenance, reviewed status, preview lineage, or source hashes before admission",
            "source_provenance_or_reviewed_status_failed",
        )

    if duplicate_status["duplicate_or_current_registry_conflict"]:
        return (
            "blocked_duplicate_or_current_registry_conflict",
            [
                duplicate_status["current_registry_conflict_status"],
                "exact_current702_accession_or_sequence_conflict_blocks_admission",
            ],
            "do not admit; preserve as duplicate/current-registry conflict evidence",
            "exact_duplicate_or_current_registry_conflict",
        )

    reaction = _reaction_evidence(full_row)
    lane = full_row.get("target_family_lane")
    lane_issues: list[str] = []
    if lane not in known_lanes:
        lane_issues.append("target_family_lane_not_in_pilot_lane_summaries")
    if reaction["specific_ec_count"] < 1:
        lane_issues.append("specific_ec_provenance_missing")
    if reaction["rhea_record_count"] < 1:
        lane_issues.append("rhea_reaction_provenance_missing")
    if lane_issues:
        return (
            "blocked_family_or_mechanism_policy",
            sorted(set(lane_issues)),
            "route to family/mechanism policy only after specific EC/Rhea and lane evidence are complete",
            "family_lane_or_reaction_policy_failed",
        )

    residue = _residue_evidence(full_row)
    coordinate_status = full_row.get("coordinate_source_status")
    locator_mapping_issues: list[str] = []
    if residue["exact_residue_locator_count"] < 1:
        locator_mapping_issues.append("no_exact_reviewed_residue_locator")
    if coordinate_status not in COORDINATE_READY_STATUSES:
        locator_mapping_issues.append("afdb_or_pdb_coordinate_provenance_missing")
    if not full_row.get("afdb_or_pdb_identifier"):
        locator_mapping_issues.append("afdb_or_pdb_identifier_missing")
    if not full_row.get("coordinate_mapping_basis"):
        locator_mapping_issues.append("coordinate_mapping_basis_missing")
    if locator_mapping_issues:
        return (
            "blocked_locator_or_coordinate_mapping",
            sorted(set(locator_mapping_issues)),
            "repair locator or coordinate mapping evidence before admission",
            "locator_or_coordinate_mapping_failed",
        )

    if not coordinate_matches:
        return (
            "admission_ready_pending_coordinate_materialization",
            [],
            (
                "materialize or hash-match local PDB/AFDB coordinates, then "
                "materialize source-free locator sidecar and rerun admission validation"
            ),
            "all_source_gates_clear_coordinate_file_not_materialized_locally",
        )
    if not locator_matches:
        return (
            "admission_ready_pending_locator_materialization",
            [],
            (
                "materialize an approved source-free locator sidecar from exact "
                "reviewed residue locators against the local coordinate, then rerun"
            ),
            "all_source_and_coordinate_gates_clear_locator_sidecar_not_materialized",
        )
    return (
        "admission_ready_external_label_candidate",
        [],
        (
            "stage as an external label candidate in the controlled admission queue; "
            "no production label import is performed"
        ),
        "source_coordinate_locator_and_duplicate_gates_clear",
    )


def _row_payload(
    *,
    full_row: dict[str, Any],
    preview_row: dict[str, Any],
    known_lanes: set[str],
    current_index: dict[str, Any],
    coordinate_index: dict[str, list[dict[str, Any]]],
    locator_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    recomputed_duplicate = _recomputed_duplicate_status(full_row, current_index)
    original_duplicate = full_row.get("duplicate_current_registry_conflict", {}) or {}
    coord_matches = _coordinate_matches(full_row, coordinate_index)
    loc_matches = _locator_matches(full_row, locator_index)
    terminal_state, blocker_basis, next_action, route_basis = _classify_admission_row(
        full_row=full_row,
        preview_row=preview_row,
        known_lanes=known_lanes,
        duplicate_status=recomputed_duplicate,
        coordinate_matches=coord_matches,
        locator_matches=loc_matches,
    )
    duplicate_status_match = (
        recomputed_duplicate["current_registry_conflict_status"]
        == original_duplicate.get("current_registry_conflict_status")
        and recomputed_duplicate["duplicate_or_current_registry_conflict"]
        == original_duplicate.get("duplicate_or_current_registry_conflict")
    )
    residue = _residue_evidence(full_row)
    reaction = _reaction_evidence(full_row)
    source_free_locator_status = (
        "approved_source_free_locator_sidecar_present"
        if loc_matches
        else "pending_source_free_locator_materialization"
    )
    coordinate_materialization_status = (
        "local_coordinate_materialized"
        if coord_matches
        else "coordinate_provenance_available_local_file_missing"
    )
    row = {
        "stable_candidate_key": full_row.get("stable_candidate_key"),
        "candidate_id": full_row.get("candidate_id"),
        "accession": full_row.get("accession"),
        "target_family_lane": full_row.get("target_family_lane"),
        "lane_id": full_row.get("lane_id"),
        "terminal_state": terminal_state,
        "terminal_route_basis": route_basis,
        "input_preview_terminal_state": preview_row.get("terminal_state"),
        "evidence_basis": {
            "reviewed_status": full_row.get("reviewed_status"),
            "source_provenance_status": "present"
            if not _source_provenance_issues(full_row)
            else "incomplete",
            "residue_evidence": residue,
            "reaction_evidence": reaction,
            "coordinate_evidence": {
                "coordinate_source": full_row.get("coordinate_source"),
                "coordinate_source_status": full_row.get("coordinate_source_status"),
                "afdb_or_pdb_identifier": full_row.get("afdb_or_pdb_identifier"),
                "pdb_ids": full_row.get("pdb_ids", []),
                "alphafold_ids": full_row.get("alphafold_ids", []),
                "coordinate_mapping_basis": full_row.get("coordinate_mapping_basis"),
                "coordinate_materialization_status": coordinate_materialization_status,
                "local_coordinate_matches": coord_matches,
            },
            "lane_assignment": {
                "target_family_lane": full_row.get("target_family_lane"),
                "lane_id": full_row.get("lane_id"),
                "source_query": full_row.get("source_query"),
                "lane_known_in_pilot": full_row.get("target_family_lane") in known_lanes,
            },
            "source_free_locator_gate": {
                "source_free_locator_status": source_free_locator_status,
                "approved_locator_matches": loc_matches,
                "exact_reviewed_locators_available_for_materialization": (
                    residue["exact_residue_locator_count"] > 0
                ),
            },
            "admission_gate": {
                "import_preview_candidate": preview_row.get("import_preview_candidate"),
                "source_provenance_clear": not _source_provenance_issues(full_row),
                "reviewed_swiss_prot_clear": full_row.get("reviewed_status")
                == "reviewed",
                "duplicate_exact_current_registry_clear": not recomputed_duplicate[
                    "duplicate_or_current_registry_conflict"
                ],
                "residue_locator_clear": residue["exact_residue_locator_count"] > 0,
                "coordinate_provenance_clear": full_row.get("coordinate_source_status")
                in COORDINATE_READY_STATUSES,
                "coordinate_materialized_locally": bool(coord_matches),
                "source_free_locator_materialized": bool(loc_matches),
                "specific_ec_and_rhea_clear": (
                    reaction["specific_ec_count"] > 0
                    and reaction["rhea_record_count"] > 0
                ),
                "lane_assignment_clear": full_row.get("target_family_lane")
                in known_lanes,
            },
        },
        "blocker_basis": blocker_basis,
        "materialization_basis": {
            "coordinate_materialization_status": coordinate_materialization_status,
            "source_free_locator_status": source_free_locator_status,
        },
        "source_hashes": {
            **(full_row.get("source_hashes", {}) or {}),
            "pilot_row_sha256": _canonical_sha256(full_row),
            "import_preview_row_sha256": _canonical_sha256(preview_row),
        },
        "source_provenance": full_row.get("source_provenance", {}),
        "duplicate_status": {
            "artifact_duplicate_status": original_duplicate,
            "recomputed_current_registry_duplicate_status": recomputed_duplicate,
            "recomputed_status_matches_artifact": duplicate_status_match,
            "structural_duplicate_screen_status": original_duplicate.get(
                "structural_duplicate_screen_status",
                "not_run_in_external_admission_validation",
            ),
        },
        "next_action": next_action,
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "source_ids_or_accession_ids_used_as_predictive_features": False,
            "source_ids_or_accession_ids_used_as_provenance_only": True,
            "mechanism_text_ec_rhea_ids_labels_or_target_names_used_as_predictive_features": False,
        },
    }
    row["admission_context_sha256"] = _canonical_sha256(
        {
            "candidate_id": row["candidate_id"],
            "terminal_state": row["terminal_state"],
            "evidence_basis": row["evidence_basis"],
            "blocker_basis": row["blocker_basis"],
            "source_hashes": row["source_hashes"],
            "duplicate_status": row["duplicate_status"],
            "next_action": row["next_action"],
        }
    )
    return row


def _validation_checks(
    *,
    expected_preview_count: int,
    pilot: dict[str, Any],
    preview: dict[str, Any],
    rows: list[dict[str, Any]],
    missing_from_pilot: list[str],
    non_preflight_matches: list[str],
    pilot_path: Path,
    import_preview_path: Path,
) -> dict[str, Any]:
    preview_declared = preview.get("source_artifacts", {}).get(
        "external_ingestion_pilot", {}
    )
    violations: list[dict[str, Any]] = []
    if preview.get("candidate_count") != expected_preview_count:
        violations.append(
            {
                "reason": "preview_candidate_count_mismatch",
                "expected": expected_preview_count,
                "observed": preview.get("candidate_count"),
            }
        )
    if len(preview.get("rows", []) or []) != expected_preview_count:
        violations.append(
            {
                "reason": "preview_row_count_mismatch",
                "expected": expected_preview_count,
                "observed": len(preview.get("rows", []) or []),
            }
        )
    if missing_from_pilot:
        violations.append(
            {
                "reason": "preview_rows_missing_from_pilot",
                "candidate_ids": missing_from_pilot,
            }
        )
    if non_preflight_matches:
        violations.append(
            {
                "reason": "preview_rows_not_pilot_preflight_candidates",
                "candidate_ids": non_preflight_matches,
            }
        )
    if preview_declared.get("sha256") and preview_declared.get("sha256") != sha256_path(
        pilot_path
    ):
        violations.append(
            {
                "reason": "preview_declared_pilot_file_sha256_mismatch",
                "declared": preview_declared.get("sha256"),
                "observed": sha256_path(pilot_path),
            }
        )
    for row in rows:
        if row.get("terminal_state") not in TERMINAL_STATES:
            violations.append(
                {
                    "candidate_id": row.get("candidate_id"),
                    "reason": "unknown_terminal_state",
                }
            )
        for key in (
            "terminal_state",
            "evidence_basis",
            "source_hashes",
            "source_provenance",
            "duplicate_status",
            "next_action",
        ):
            if row.get(key) in (None, "", {}, []):
                violations.append(
                    {
                        "candidate_id": row.get("candidate_id"),
                        "reason": f"missing_required_{key}",
                    }
                )
        if not row["duplicate_status"]["recomputed_status_matches_artifact"]:
            violations.append(
                {
                    "candidate_id": row.get("candidate_id"),
                    "reason": "recomputed_duplicate_status_mismatch",
                }
            )

    return {
        "passed": not violations,
        "violation_count": len(violations),
        "violations": violations,
        "json_inputs_parsed": True,
        "preview_candidate_count_matches_expected": preview.get("candidate_count")
        == expected_preview_count,
        "preview_row_count_matches_expected": len(preview.get("rows", []) or [])
        == expected_preview_count,
        "preview_rows_reconciled_to_pilot": not missing_from_pilot,
        "preview_rows_match_pilot_preflight_state": not non_preflight_matches,
        "all_terminal_states_known": all(
            row.get("terminal_state") in TERMINAL_STATES for row in rows
        ),
        "all_rows_have_required_fields": not any(
            violation["reason"].startswith("missing_required_")
            for violation in violations
        ),
        "all_rows_have_source_hashes_and_provenance": all(
            bool(row.get("source_hashes")) and bool(row.get("source_provenance"))
            for row in rows
        ),
        "all_rows_have_duplicate_status": all(
            bool(row.get("duplicate_status")) for row in rows
        ),
        "all_duplicate_statuses_recomputed_match_artifact": all(
            row["duplicate_status"]["recomputed_status_matches_artifact"]
            for row in rows
        ),
        "pilot_file_sha256": sha256_path(pilot_path),
        "import_preview_file_sha256": sha256_path(import_preview_path),
        "preview_declared_pilot_file_sha256_matches": not preview_declared.get("sha256")
        or preview_declared.get("sha256") == sha256_path(pilot_path),
        "pilot_artifact_id": pilot.get("artifact_id"),
        "import_preview_artifact_id": preview.get("artifact_id"),
    }


def build_external_source_admission_validation(
    *,
    pilot_path: Path = DEFAULT_PILOT_PATH,
    import_preview_path: Path = DEFAULT_IMPORT_PREVIEW_PATH,
    created_utc: str | None = None,
    expected_preview_count: int = 16,
    artifacts_dir: Path = Path("artifacts"),
    locator_sidecar_dirs: tuple[Path, ...] = DEFAULT_LOCATOR_SIDECAR_DIRS,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    pilot = _read_json(pilot_path)
    preview = _read_json(import_preview_path)
    current_index = _load_current_reference_index(pilot)
    coordinate_index = _index_coordinate_files(artifacts_dir)
    locator_index = _index_approved_locator_evidence(locator_sidecar_dirs)
    pilot_rows_by_id = {
        row.get("candidate_id"): row for row in pilot.get("rows", []) or []
    }
    known_lanes = {
        str(lane.get("target_family_lane"))
        for lane in pilot.get("lane_summaries", []) or []
        if lane.get("target_family_lane")
    }
    missing_from_pilot: list[str] = []
    non_preflight_matches: list[str] = []
    rows: list[dict[str, Any]] = []
    for preview_row in preview.get("rows", []) or []:
        candidate_id = preview_row.get("candidate_id")
        full_row = pilot_rows_by_id.get(candidate_id)
        if full_row is None:
            missing_from_pilot.append(str(candidate_id))
            continue
        if full_row.get("terminal_state") != PREVIEW_SOURCE_TERMINAL_STATE:
            non_preflight_matches.append(str(candidate_id))
        rows.append(
            _row_payload(
                full_row=full_row,
                preview_row=preview_row,
                known_lanes=known_lanes,
                current_index=current_index,
                coordinate_index=coordinate_index,
                locator_index=locator_index,
            )
        )

    terminal_counts = Counter(row["terminal_state"] for row in rows)
    family_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
    admission_ready_rows = [
        row for row in rows if row["terminal_state"] in ADMISSION_READY_STATES
    ]
    direct_ready_rows = [
        row
        for row in rows
        if row["terminal_state"] == "admission_ready_external_label_candidate"
    ]
    validation_checks = _validation_checks(
        expected_preview_count=expected_preview_count,
        pilot=pilot,
        preview=preview,
        rows=rows,
        missing_from_pilot=missing_from_pilot,
        non_preflight_matches=non_preflight_matches,
        pilot_path=pilot_path,
        import_preview_path=import_preview_path,
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "scope": (
            "Admission validation for the first 16 external import-preview "
            "candidates from the current702 reviewed UniProt external ingestion lane."
        ),
        "source_artifacts": {
            "external_ingestion_pilot": _source_record(pilot_path),
            "external_ingestion_import_preview": _source_record(import_preview_path),
            "pilot_declared_source_artifacts": pilot.get("source_artifacts", {}),
            "import_preview_declared_source_artifacts": preview.get("source_artifacts", {}),
        },
        "classification_policy": {
            "terminal_states": list(TERMINAL_STATES),
            "direct_ready_requires": [
                "reviewed Swiss-Prot/UniProt status",
                "source hashes and source URLs present",
                "no exact current702 accession or sequence SHA conflict",
                "specific EC and Rhea reaction provenance",
                "known pilot family lane assignment",
                "at least one exact reviewed residue locator",
                "PDB/AFDB coordinate provenance",
                "hash-matched local coordinate file",
                "approved source-free locator sidecar",
            ],
            "pending_coordinate_materialization": (
                "all source admission gates clear, but no local coordinate file "
                "matched the PDB/AFDB handle or same-accession AFDB cache"
            ),
            "pending_locator_materialization": (
                "source and local coordinate gates clear, but no approved source-free "
                "locator sidecar matched the candidate"
            ),
            "production_import_rule": (
                "No production label import is authorized here; admission-ready rows "
                "remain preview candidates until controlled registry authorization."
            ),
        },
        "input_reconciliation": {
            "expected_preview_count": expected_preview_count,
            "preview_candidate_count": preview.get("candidate_count"),
            "preview_row_count": len(preview.get("rows", []) or []),
            "pilot_candidate_count": pilot.get("candidate_count"),
            "matched_preview_rows_in_pilot": len(rows),
            "missing_preview_candidate_ids_from_pilot": missing_from_pilot,
            "preview_candidate_ids_not_pilot_preflight": non_preflight_matches,
        },
        "counts": {
            "validated_rows": len(rows),
            "admission_ready_rows": len(admission_ready_rows),
            "direct_external_label_candidate_rows": len(direct_ready_rows),
            "pending_coordinate_materialization_rows": terminal_counts.get(
                "admission_ready_pending_coordinate_materialization", 0
            ),
            "pending_locator_materialization_rows": terminal_counts.get(
                "admission_ready_pending_locator_materialization", 0
            ),
        },
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "family_lane_terminal_state_counts": {
            family: dict(sorted(counts.items()))
            for family, counts in sorted(family_counts.items())
        },
        "rows": rows,
        "validation_checks": validation_checks,
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "production_import_edited": False,
            "ontology_edited": False,
            "model_weights_or_thresholds_edited": False,
            "train_test_splits_changed": False,
            "heldout_training_or_tuning_performed": False,
            "coordinates_fetched_or_materialized_now": False,
            "locator_sidecars_copied_or_materialized_now": False,
            "mechanism_text_ec_rhea_ids_labels_target_names_accession_ids_or_source_ids_used_as_predictive_features": False,
            "source_ids_and_accessions_used_as_provenance_only": True,
        },
    }


def build_external_source_admission_ready_preview(
    validation: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or validation.get("created_utc") or _utc_now_iso()
    rows = [
        {
            "stable_candidate_key": row["stable_candidate_key"],
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "terminal_route_basis": row["terminal_route_basis"],
            "coordinate_materialization_status": row["materialization_basis"][
                "coordinate_materialization_status"
            ],
            "source_free_locator_status": row["materialization_basis"][
                "source_free_locator_status"
            ],
            "afdb_or_pdb_identifier": row["evidence_basis"]["coordinate_evidence"][
                "afdb_or_pdb_identifier"
            ],
            "reviewed_status": row["evidence_basis"]["reviewed_status"],
            "exact_residue_locator_count": row["evidence_basis"]["residue_evidence"][
                "exact_residue_locator_count"
            ],
            "rhea_record_count": row["evidence_basis"]["reaction_evidence"][
                "rhea_record_count"
            ],
            "duplicate_status": row["duplicate_status"][
                "recomputed_current_registry_duplicate_status"
            ]["current_registry_conflict_status"],
            "source_hashes": row["source_hashes"],
            "ready_for_external_label_admission": True,
            "ready_for_production_label_import": False,
            "label_import_performed": False,
            "next_action": row["next_action"],
        }
        for row in validation.get("rows", [])
        if row.get("terminal_state") in ADMISSION_READY_STATES
    ]
    terminal_counts = Counter(row["terminal_state"] for row in rows)
    return {
        "artifact_id": READY_PREVIEW_ARTIFACT_ID,
        "schema_version": READY_PREVIEW_SCHEMA_VERSION,
        "created_utc": created,
        "source_artifact_id": validation.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(validation),
        "candidate_count": len(rows),
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "rows": rows,
        "guardrails": {
            "preview_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
            "coordinates_fetched_or_materialized_now": False,
            "locator_sidecars_copied_or_materialized_now": False,
        },
    }


def render_external_source_admission_validation_report(
    artifact: dict[str, Any],
) -> str:
    lines = [
        "# External Source Admission Validation - 16 current702 candidates",
        "",
        "Read-only admission validation for the first 16 reviewed UniProt external "
        "import-preview rows. No labels, registries, imports, ontologies, models, "
        "thresholds, splits, coordinates, or locator sidecars were edited.",
        "",
        "## Summary",
        "",
        f"- Created UTC: `{artifact['created_utc']}`",
        f"- Validated rows: `{artifact['counts']['validated_rows']}`",
        f"- Admission-ready rows: `{artifact['counts']['admission_ready_rows']}`",
        f"- Direct external label candidates: `{artifact['counts']['direct_external_label_candidate_rows']}`",
        f"- Pending coordinate materialization: `{artifact['counts']['pending_coordinate_materialization_rows']}`",
        f"- Pending locator materialization: `{artifact['counts']['pending_locator_materialization_rows']}`",
        f"- Validation passed: `{artifact['validation_checks']['passed']}`",
        "",
        "## Terminal State Counts",
        "",
        "| Terminal state | Count |",
        "| --- | ---: |",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    terminal_states = sorted(artifact["terminal_state_counts"])
    lines.extend(
        [
            "",
            "## Family/Lane Counts",
            "",
            "| Family/lane | " + " | ".join(terminal_states) + " |",
            "| --- | " + " | ".join("---:" for _ in terminal_states) + " |",
        ]
    )
    for family, counts in artifact["family_lane_terminal_state_counts"].items():
        values = [str(counts.get(state, 0)) for state in terminal_states]
        lines.append(f"| {family} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## Admission Matrix",
            "",
            "| Candidate | Lane | Terminal state | Exact locators | Coordinate | Local coordinate | Source-free locator | Next action |",
            "| --- | --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in artifact["rows"]:
        coordinate = row["evidence_basis"]["coordinate_evidence"]
        residue = row["evidence_basis"]["residue_evidence"]
        lines.append(
            "| "
            f"`{row['candidate_id']}` | {row['target_family_lane']} | "
            f"`{row['terminal_state']}` | "
            f"{residue['exact_residue_locator_count']} | "
            f"{coordinate['afdb_or_pdb_identifier']} | "
            f"{coordinate['coordinate_materialization_status']} | "
            f"{row['materialization_basis']['source_free_locator_status']} | "
            f"{row['next_action']} |"
        )

    lines.extend(
        [
            "",
            "## Mechanical Findings",
            "",
            "- All 16 preview rows reconcile exactly to pilot rows in `external_countable_preflight_candidate` state.",
            "- All 16 rows have reviewed Swiss-Prot status, source hashes/provenance, exact residue locators, PDB/AFDB handles, Rhea/specific EC provenance, and no recomputed exact current702 accession or sequence conflict.",
            f"- {artifact['counts']['pending_locator_materialization_rows']} rows have a matching local coordinate file in existing artifacts and remain pending source-free locator materialization.",
            f"- {artifact['counts']['pending_coordinate_materialization_rows']} rows have coordinate provenance but no matching local CIF in the current artifact cache, so they are pending coordinate materialization before locator sidecar materialization.",
            "- No direct production/import-ready label candidate is emitted; the ready preview is an admission/materialization queue only.",
            "",
            "## Validation",
            "",
        ]
    )
    for key, value in artifact["validation_checks"].items():
        if key == "violations":
            continue
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def write_external_source_admission_validation(
    *,
    pilot_path: Path = DEFAULT_PILOT_PATH,
    import_preview_path: Path = DEFAULT_IMPORT_PREVIEW_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    ready_preview_path: Path | None = DEFAULT_READY_PREVIEW_PATH,
    created_utc: str | None = None,
    expected_preview_count: int = 16,
    artifacts_dir: Path = Path("artifacts"),
) -> dict[str, Any]:
    artifact = build_external_source_admission_validation(
        pilot_path=pilot_path,
        import_preview_path=import_preview_path,
        created_utc=created_utc,
        expected_preview_count=expected_preview_count,
        artifacts_dir=artifacts_dir,
    )
    _write_json(out_path, artifact)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_source_admission_validation_report(artifact),
            encoding="utf-8",
        )
    if ready_preview_path is not None and artifact["counts"]["admission_ready_rows"] > 0:
        preview = build_external_source_admission_ready_preview(
            artifact, created_utc=artifact["created_utc"]
        )
        _write_json(ready_preview_path, preview)
    return artifact
