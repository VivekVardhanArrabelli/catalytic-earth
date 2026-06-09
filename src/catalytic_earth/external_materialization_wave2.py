from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .structure import STANDARD_AMINO_ACIDS, parse_atom_site_loop
from .transfer_scope import fetch_external_structure_cif


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
DEFAULT_ADDITIONAL_SURFACE_PATHS = (
    Path(
        "artifacts/"
        "v3_external_bulk_ingestion_scaleout_wave2_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_metal_phosphoryl_glycoside_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_near_orphan_diversity_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609.json"
    ),
)
DEFAULT_ADDITIONAL_IMPORT_READY_SOURCE_PATHS = (
    Path(
        "artifacts/"
        "v3_external_bulk_ingestion_scaleout_wave2_provisional_import_preview_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_metal_phosphoryl_glycoside_import_ready_preview_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_near_orphan_diversity_import_ready_preview_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_current702_20260609.json"
    ),
    Path(
        "artifacts/"
        "v3_external_scaleout_shard_redox_cofactor_confounded_import_ready_preview_current702_20260609.json"
    ),
)
DEFAULT_SUPPLEMENTAL_REVIEW_SHARD_PATHS = (
    Path("artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_near_orphan_tail_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_plp_children_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json"),
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
DEFAULT_COORDINATE_DIR = Path(
    f"artifacts/external_materialization_wave2_coordinates_current702_{RUN_DATE}"
)

LOW_DISK_COORDINATE_POLICY = (
    "coordinate_downloads_disabled_because_run_started_below_10_gib_floor"
)
COORDINATE_DOWNLOAD_FLOOR_GIB = 10.0
COORDINATE_DOWNLOAD_STOP_BUFFER_GIB = 0.5
COORDINATE_LOCAL_IDENTITY_CLASS = (
    "reviewed_exact_position_coordinate_local_residue_identity_without_source_text"
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
    "repairable_coordinate_blocker",
    "repairable_locator_blocker",
}
SOURCE_TERMINAL_PRECEDENCE = {
    IMPORT_READY_STATE: 100,
    "provisional_external_countable_preflight_candidate": 90,
    "locator_ready_candidate": 80,
    COORDINATE_READY_STATE: 70,
    "repairable_locator_blocker": 50,
    "locator_repair_candidate": 45,
    "repairable_coordinate_blocker": 40,
    "coordinate_repair_candidate": 35,
    DUPLICATE_STATE: 25,
    "reject/OOS_preserve_signal": 10,
    "hard_blocked_with_next_action": 5,
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


def _artifact_key(path: Path, artifact: dict[str, Any]) -> str:
    artifact_id = str(artifact.get("artifact_id") or path.stem)
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", artifact_id)


def _path_list(paths: list[Path] | tuple[Path, ...] | None) -> list[Path]:
    return [Path(path) for path in paths or []]


def _existing_optional_paths(
    paths: list[Path] | tuple[Path, ...] | None,
) -> tuple[list[Path], list[str]]:
    existing: list[Path] = []
    missing: list[str] = []
    for path in _path_list(paths):
        if path.exists():
            existing.append(path)
        else:
            missing.append(str(path))
    return existing, missing


def _candidate_key(row: dict[str, Any]) -> str:
    return str(
        row.get("candidate_id")
        or row.get("stable_candidate_key")
        or row.get("accession")
        or ""
    )


def _row_with_source(
    row: dict[str, Any],
    *,
    source_key: str,
    source_path: Path,
) -> dict[str, Any]:
    copy = dict(row)
    copy["_wave2_source_key"] = source_key
    copy["_wave2_source_path"] = str(source_path)
    return copy


def _source_rank(row: dict[str, Any]) -> tuple[int, int, int]:
    exact_count = len(_exact_locators(row))
    field_count = len(row)
    terminal_rank = SOURCE_TERMINAL_PRECEDENCE.get(
        str(row.get("terminal_state") or ""), 0
    )
    return terminal_rank, exact_count, field_count


def _import_rank(row: dict[str, Any]) -> tuple[int, int, int, int]:
    ready = 1 if row.get("ready_for_controlled_import_review") is True else 0
    coordinate = 1 if row.get("coordinate_path") else 0
    locator = 1 if row.get("locator_sidecar_path") else 0
    exact_count = len(_exact_locators(row))
    return ready, coordinate, locator, exact_count


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


def _clean_accession(value: Any) -> str:
    text = str(value or "").strip()
    return text.split(":", 1)[1] if text.startswith("uniprot:") else text


def _coordinate_file_name(row: dict[str, Any]) -> str | None:
    identifier = str(row.get("afdb_or_pdb_identifier") or "").strip()
    if not identifier:
        return None
    if identifier.upper().startswith("AF-") and "-F1" in identifier.upper():
        return f"{identifier}-model_v6.cif"
    cleaned = identifier.upper().removeprefix("PDB:")
    return f"pdb_{cleaned}.cif"


def _best_structure_source(row: dict[str, Any]) -> tuple[str | None, str | None]:
    alphafold_ids = [
        str(value).strip()
        for value in row.get("alphafold_ids", []) or []
        if str(value).strip()
    ]
    if alphafold_ids:
        return "alphafold", alphafold_ids[0]
    pdb_ids = [
        str(value).strip().upper()
        for value in row.get("pdb_ids", []) or []
        if str(value).strip()
    ]
    if pdb_ids:
        return "pdb", pdb_ids[0]
    identifier = str(row.get("afdb_or_pdb_identifier") or "").strip()
    if identifier.upper().startswith("AF-") and "-F1" in identifier.upper():
        parts = identifier.split("-")
        if len(parts) >= 3:
            return "alphafold", parts[1]
    if identifier:
        return "pdb", identifier.upper().removeprefix("PDB:")
    return None, None


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
        normalized = str(value or "").strip().lower()
        if normalized:
            keys.add(normalized)
            keys.add(normalized.replace(":", "_"))
    identifier = str(row.get("afdb_or_pdb_identifier") or "").strip().lower()
    if identifier:
        keys.add(identifier.removeprefix("pdb:"))
        keys.add(f"pdb_{identifier.removeprefix('pdb:')}")
        if identifier.startswith("af-"):
            parts = identifier.split("-")
            if len(parts) >= 3:
                keys.add(parts[1])
                keys.add(f"uniprot:{parts[1]}")
    for value in row.get("pdb_ids", []) or []:
        normalized = str(value or "").strip().lower()
        if normalized:
            keys.add(normalized.removeprefix("pdb:"))
            keys.add(f"pdb_{normalized.removeprefix('pdb:')}")
    for value in row.get("alphafold_ids", []) or []:
        normalized = str(value or "").strip().lower()
        if normalized:
            accession = normalized.removeprefix("uniprot:")
            keys.add(accession)
            keys.add(f"uniprot:{accession}")
            keys.add(f"af-{accession}-f1")
    return keys


def _add_coordinate_index_key(
    index: dict[str, list[dict[str, Any]]],
    key: Any,
    record: dict[str, Any],
) -> None:
    normalized = str(key or "").strip().lower()
    if not normalized:
        return
    index.setdefault(normalized, []).append(record)
    index.setdefault(normalized.replace(":", "_"), []).append(record)
    if normalized.startswith("uniprot:"):
        index.setdefault(normalized.split(":", 1)[1], []).append(record)


def _index_coordinate_files(
    artifacts_dir: Path = Path("artifacts"),
) -> dict[str, list[dict[str, Any]]]:
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


def _coordinate_matches(
    row: dict[str, Any],
    coordinate_index: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in _coordinate_lookup_keys(row):
        for record in coordinate_index.get(key, []):
            path = str(record["path"])
            if path in seen:
                continue
            seen.add(path)
            matches.append(
                {
                    "path": path,
                    "bytes": record["bytes"],
                    "sha256": _sha256_path(Path(path)),
                }
            )
    return sorted(matches, key=lambda record: record["path"])


def _free_gib(path: Path) -> float:
    usage_path = path if path.exists() else path.parent
    while not usage_path.exists() and usage_path.parent != usage_path:
        usage_path = usage_path.parent
    usage = shutil.disk_usage(usage_path)
    return usage.free / (1024 ** 3)


def _fetch_coordinate(
    row: dict[str, Any],
    *,
    coordinate_dir: Path,
    fetcher: Callable[[str, str], str],
) -> dict[str, Any]:
    file_name = _coordinate_file_name(row)
    if not file_name:
        return {
            "status": "coordinate_identifier_missing",
            "coordinate_path": None,
            "fetched_now": False,
            "fetch_error": "coordinate_identifier_missing",
        }
    coordinate_path = coordinate_dir / file_name
    if coordinate_path.exists():
        return {
            "status": "coordinate_reused_existing_wave2_file",
            "coordinate_path": str(coordinate_path),
            "fetched_now": False,
            "fetch_error": None,
        }
    source, structure_id = _best_structure_source(row)
    if not source or not structure_id:
        return {
            "status": "coordinate_fetch_not_possible_no_supported_source",
            "coordinate_path": None,
            "fetched_now": False,
            "fetch_error": "no_supported_structure_source",
        }
    try:
        cif_text = fetcher(source, structure_id)
    except Exception as exc:  # pragma: no cover - live-source fallback
        return {
            "status": "coordinate_fetch_failed",
            "coordinate_path": None,
            "fetched_now": False,
            "fetch_error": f"{type(exc).__name__}: {exc}",
            "structure_source": source,
            "structure_id": structure_id,
        }
    coordinate_dir.mkdir(parents=True, exist_ok=True)
    coordinate_path.write_text(cif_text, encoding="utf-8")
    return {
        "status": "coordinate_fetched_now",
        "coordinate_path": str(coordinate_path),
        "fetched_now": True,
        "fetch_error": None,
        "structure_source": source,
        "structure_id": structure_id,
    }


def _position_to_residue_codes(cif_path: Path) -> dict[int, set[str]]:
    atoms = parse_atom_site_loop(cif_path.read_text(encoding="utf-8"))
    position_to_codes: dict[int, set[str]] = defaultdict(set)
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        code = str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if code not in STANDARD_AMINO_ACIDS:
            continue
        for raw_position in (atom.get("auth_seq_id"), atom.get("label_seq_id")):
            try:
                position = int(str(raw_position))
            except (TypeError, ValueError):
                continue
            position_to_codes[position].add(code)
    return position_to_codes


def _coordinate_ready_sidecar_payload(
    row: dict[str, Any],
    *,
    created_utc: str,
    sidecar_path: Path,
    coordinate_path: Path,
    coordinate_download_performed: bool,
) -> tuple[dict[str, Any] | None, list[str]]:
    exact_locators = _exact_locators(row)
    if len(exact_locators) < 2:
        return None, ["fewer_than_two_exact_reviewed_residue_locators"]
    position_codes = _position_to_residue_codes(coordinate_path)
    residue_locators: list[dict[str, Any]] = []
    blockers: list[str] = []
    for locator in exact_locators:
        position = _position(locator)
        if position is None:
            blockers.append("non_integer_exact_locator_position")
            continue
        codes = sorted(position_codes.get(position, set()))
        if len(codes) != 1:
            blockers.append(f"coordinate_residue_code_unresolved_at_position:{position}")
            continue
        residue_locators.append(
            {
                "sequence_position": position,
                "end": locator.get("end"),
                "residue_code": codes[0],
                "reviewed_feature_code": locator.get("feature_code"),
                "reviewed_feature_type": locator.get("feature_type"),
                "evidence_codes": sorted(
                    str(code) for code in _as_list(locator.get("evidence_codes"))
                ),
                "ligand_id": locator.get("ligand_id"),
                "ligand_name": locator.get("ligand_name"),
                "role_hint": _role_hint(locator),
                "locator_confidence": 1.0,
                "locator_evidence_class": COORDINATE_LOCAL_IDENTITY_CLASS,
                "coordinate_independent_provenance": {
                    "heldout_rows_used": False,
                    "method": (
                        "reviewed_exact_position_plus_coordinate_local_residue_identity"
                    ),
                    "sequence_position_uniprot_declared": True,
                    "coordinate_local_residue_identity_validated": True,
                    "source_text_used": False,
                    "reviewed_feature_code": locator.get("feature_code"),
                    "reviewed_feature_type": locator.get("feature_type"),
                },
            }
        )
    if len(residue_locators) < 2:
        return None, sorted(set(blockers or ["insufficient_resolved_coordinate_locators"]))
    payload = _sidecar_payload(row, created_utc=created_utc, sidecar_path=sidecar_path)
    payload["coordinate_provenance"].update(
        {
            "coordinate_path": str(coordinate_path),
            "coordinate_sha256": _sha256_path(coordinate_path),
            "coordinate_download_performed": coordinate_download_performed,
            "coordinate_download_policy": "bounded_wave2_materialization_above_10_gib_floor",
            "coordinate_local_residue_identity_validated": True,
        }
    )
    payload["locator_policy"] = (
        "review_only_exact_position_coordinate_local_residue_identity"
    )
    payload["ready_for_controlled_import_review"] = True
    payload["source_free_active_site_locator_status"] = (
        "ready_coordinate_local_residue_identity"
    )
    payload["residue_locators"] = residue_locators
    return payload, []


def _duplicate_status(row: dict[str, Any]) -> dict[str, Any]:
    duplicate_summary = row.get("duplicate_status_summary")
    duplicate_current = row.get("duplicate_current_registry_conflict")
    if isinstance(duplicate_summary, dict):
        return {
            "blocked_by_duplicate_or_current_registry_conflict": bool(
                duplicate_summary.get("blocked_by_duplicate_or_current_registry_conflict")
                or duplicate_summary.get("blocked_by_current_or_prior_duplicate")
            ),
            "current702_status": duplicate_summary.get("current702_status"),
            "external_pilot_status": duplicate_summary.get("external_pilot_status"),
            "prior_external_status": duplicate_summary.get("prior_external_status"),
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
            "prior_external_status": None,
        }
    return {
        "blocked_by_duplicate_or_current_registry_conflict": (
            row.get("terminal_state") == DUPLICATE_STATE
        ),
        "current702_status": row.get("duplicate_current_registry_conflict_status"),
        "external_pilot_status": row.get("duplicate_external_pilot_conflict_status"),
        "prior_external_status": row.get("duplicate_prior_external_conflict_status"),
    }


def _is_exact_current_or_external_pilot_duplicate(row: dict[str, Any]) -> bool:
    status = _duplicate_status(row)
    current702_status = str(status.get("current702_status") or "")
    external_pilot_status = str(status.get("external_pilot_status") or "")
    return current702_status.startswith("exact_current702") or (
        external_pilot_status.startswith("exact_external_pilot")
    )


def _is_prior_external_duplicate_only(row: dict[str, Any]) -> bool:
    status = _duplicate_status(row)
    prior_external_status = str(status.get("prior_external_status") or "")
    return (
        prior_external_status.startswith("exact_prior_external")
        and not _is_exact_current_or_external_pilot_duplicate(row)
    )


def _ready_import_preview_row(row: dict[str, Any]) -> bool:
    return row.get("ready_for_controlled_import_review") is True and not (
        _is_exact_current_or_external_pilot_duplicate(row)
    )


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
    if wave2_terminal_state in {
        "locator_sidecar_materialized_coordinate_pending",
        "locator_sidecar_reused_coordinate_pending",
        "shard_import_ready_preview_locator_sidecar_materialized_coordinate_pending",
        "shard_import_ready_preview_locator_sidecar_reused_coordinate_pending",
    }:
        return "coordinate_materialization_continuation_due_disk_floor"
    if wave2_terminal_state == "blocked_duplicate_or_current_registry_conflict":
        return "duplicate_conflict_no_import"
    if wave2_terminal_state == "import_ready_preview_materialized_coordinate_locator":
        return "controlled_import_review_preview"
    if source_state == COORDINATE_READY_STATE:
        return "source_free_locator_materialization_needed"
    if source_state == "locator_repair_candidate":
        return "locator_repair"
    if source_state in {"coordinate_repair_candidate", "repairable_coordinate_blocker"}:
        return "coordinate_repair"
    if source_state == "repairable_locator_blocker":
        return "locator_repair"
    if source_state == "hard_blocked_with_next_action":
        return "hard_blocker"
    if source_state == "reject/OOS_preserve_signal":
        return "reject_or_oos_preserve_signal_no_import"
    return "admission_or_materialization_continuation"


def _next_action(row: dict[str, Any], wave2_terminal_state: str) -> str:
    if wave2_terminal_state in {
        "locator_sidecar_materialized_coordinate_pending",
        "locator_sidecar_reused_coordinate_pending",
        "shard_import_ready_preview_locator_sidecar_materialized_coordinate_pending",
        "shard_import_ready_preview_locator_sidecar_reused_coordinate_pending",
    }:
        return (
            "When disk free space is above 10 GiB, materialize or reuse the "
            "coordinate file, validate coordinate-local residue identity for "
            "the sidecar, then rerun import-ready preview admission."
        )
    if wave2_terminal_state == "blocked_duplicate_or_current_registry_conflict":
        return (
            "Do not import from this row; preserve the duplicate/current-registry "
            "conflict and use the non-conflicting merged candidate if one exists."
        )
    if wave2_terminal_state == "import_ready_preview_carried_forward":
        return (
            "Keep in preview-only controlled import-review queue; structural "
            "duplicate screening and explicit production authorization remain."
        )
    if wave2_terminal_state == "import_ready_preview_materialized_coordinate_locator":
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
    source_occurrences: list[dict[str, Any]],
    cross_source_duplicate_collapsed: bool,
    coordinate_path_override: str | None = None,
    coordinate_materialization_status_override: str | None = None,
    locator_sidecar_status_override: str | None = None,
) -> dict[str, Any]:
    exact_locators = _exact_locators(row)
    coordinate_path = coordinate_path_override
    locator_path = locator_sidecar_path
    if (
        coordinate_path is None
        and wave2_terminal_state == "import_ready_preview_carried_forward"
        and import_ready_row
    ):
        coordinate_path = import_ready_row.get("coordinate_path")
        locator_path = locator_sidecar_path or import_ready_row.get("locator_sidecar_path")
    if locator_path is None:
        locator_path = locator_sidecar_path
    return {
        "candidate_id": row.get("candidate_id"),
        "accession": row.get("accession"),
        "target_family_lane": row.get("target_family_lane") or row.get("lane_id"),
        "source_terminal_state": row.get("terminal_state"),
        "wave2_terminal_state": wave2_terminal_state,
        "repair_bucket": _repair_bucket(row, wave2_terminal_state),
        "coordinate_path": coordinate_path,
        "locator_sidecar_path": locator_path,
        "coordinate_materialization_status": coordinate_materialization_status_override
        or (
            "carried_from_consumed_materialization_preview"
            if wave2_terminal_state == "import_ready_preview_carried_forward"
            else LOW_DISK_COORDINATE_POLICY
        ),
        "locator_sidecar_status": locator_sidecar_status_override
        or (
            "carried_from_consumed_materialization_preview"
            if (
                wave2_terminal_state == "import_ready_preview_carried_forward"
                and locator_sidecar_path is None
            )
            else (
                "materialized_or_reused_pending_coordinate_identity"
                if locator_sidecar_path
                else "not_materialized"
            )
        ),
        "exact_residue_locator_count": len(exact_locators),
        "duplicate_status": _duplicate_status(row),
        "ready_for_controlled_import_review": bool(
            (
                wave2_terminal_state == "import_ready_preview_carried_forward"
                and import_ready_row
                and import_ready_row.get("ready_for_controlled_import_review")
            )
            or wave2_terminal_state
            == "import_ready_preview_materialized_coordinate_locator"
        ),
        "ready_for_production_label_import": False,
        "source_artifacts_consumed": sorted(
            {str(source["source_key"]) for source in source_occurrences}
        ),
        "source_occurrence_count": len(source_occurrences),
        "source_occurrences": source_occurrences,
        "source_import_ready_preview_consumed": bool(import_ready_row),
        "cross_source_duplicate_collapsed": cross_source_duplicate_collapsed,
        "source_hashes": row.get("source_hashes", {}),
        "stable_candidate_key": row.get("stable_candidate_key"),
        "next_action": _next_action(row, wave2_terminal_state),
    }


def _source_occurrences(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for row in rows:
        occurrences.append(
            {
                "source_key": row.get("_wave2_source_key"),
                "source_path": row.get("_wave2_source_path"),
                "terminal_state": row.get("terminal_state"),
                "duplicate_status": _duplicate_status(row),
                "prior_external_duplicate_only": _is_prior_external_duplicate_only(row),
            }
        )
    return occurrences


def _select_source_row(
    rows: list[dict[str, Any]],
    import_ready_row: dict[str, Any] | None,
) -> dict[str, Any]:
    if import_ready_row is not None:
        import_ready_surface_rows = [
            row for row in rows if row.get("terminal_state") == IMPORT_READY_STATE
        ]
        if import_ready_surface_rows:
            return max(import_ready_surface_rows, key=_source_rank)
    return max(rows, key=_source_rank)


def _locator_sidecar_for_row(
    row: dict[str, Any],
    *,
    locator_dir: Path,
    created_utc: str,
    sidecars_to_write: list[tuple[Path, dict[str, Any]]],
) -> tuple[str | None, bool]:
    if not _exact_locators(row):
        return None, False
    candidate_id = str(row.get("candidate_id") or "")
    sidecar_path = locator_dir / f"{_sidecar_token(candidate_id)}.json"
    if sidecar_path.exists():
        return str(sidecar_path), True
    sidecars_to_write.append(
        (
            sidecar_path,
            _sidecar_payload(row, created_utc=created_utc, sidecar_path=sidecar_path),
        )
    )
    return str(sidecar_path), False


def _record_coordinate_file(
    coordinate_index: dict[str, list[dict[str, Any]]],
    *,
    row: dict[str, Any],
    coordinate_path: Path,
) -> None:
    if not coordinate_path.exists():
        return
    record = {"path": str(coordinate_path), "bytes": coordinate_path.stat().st_size}
    for key in {
        coordinate_path.name,
        coordinate_path.stem,
        *_coordinate_lookup_keys(row),
    }:
        _add_coordinate_index_key(coordinate_index, key, record)
    name = coordinate_path.name.lower()
    if name.startswith("pdb_"):
        _add_coordinate_index_key(
            coordinate_index, name[4:].rsplit(".", 1)[0], record
        )
    if name.startswith("af-") and "-f1" in name:
        parts = name.split("-")
        if len(parts) >= 3:
            accession = parts[1]
            _add_coordinate_index_key(coordinate_index, accession, record)
            _add_coordinate_index_key(coordinate_index, f"uniprot:{accession}", record)
            _add_coordinate_index_key(coordinate_index, f"af-{accession}-f1", record)


def _is_ready_coordinate_sidecar(path: Path, coordinate_path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = _read_json(path)
    except json.JSONDecodeError:
        return False
    provenance = payload.get("coordinate_provenance", {}) or {}
    return (
        payload.get("source_free_active_site_locator_status")
        == "ready_coordinate_local_residue_identity"
        and provenance.get("coordinate_path") == str(coordinate_path)
        and provenance.get("coordinate_local_residue_identity_validated") is True
    )


def _coordinate_ready_materialization_for_row(
    row: dict[str, Any],
    *,
    coordinate_index: dict[str, list[dict[str, Any]]],
    coordinate_dir: Path,
    locator_dir: Path,
    created_utc: str,
    sidecars_to_write: list[tuple[Path, dict[str, Any]]],
    fetcher: Callable[[str, str], str],
    coordinate_budget: dict[str, int],
    coordinate_downloads_enabled: bool,
    disk_free_gib_provider: Callable[[Path], float],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ready": False,
        "coordinate_path": None,
        "locator_sidecar_path": None,
        "coordinate_status": "not_attempted",
        "locator_status": "not_attempted",
        "blockers": [],
        "coordinate_download_performed": False,
        "coordinate_reused_local": False,
        "locator_sidecar_reused": False,
    }
    if len(_exact_locators(row)) < 2:
        result["coordinate_status"] = "skipped_fewer_than_two_exact_locators"
        result["blockers"] = ["fewer_than_two_exact_reviewed_residue_locators"]
        return result

    coordinate_matches = _coordinate_matches(row, coordinate_index)
    coordinate_attempt: dict[str, Any] | None = None
    if not coordinate_matches:
        if not coordinate_downloads_enabled:
            result["coordinate_status"] = (
                "coordinate_downloads_disabled_or_disk_below_floor"
            )
            result["blockers"] = [LOW_DISK_COORDINATE_POLICY]
            return result
        if coordinate_budget["remaining"] <= 0:
            coordinate_budget["budget_exhausted"] = 1
            result["coordinate_status"] = "coordinate_download_budget_exhausted"
            result["blockers"] = ["bounded_coordinate_download_budget_exhausted"]
            return result
        current_free_gib = disk_free_gib_provider(coordinate_dir)
        if current_free_gib <= COORDINATE_DOWNLOAD_FLOOR_GIB + COORDINATE_DOWNLOAD_STOP_BUFFER_GIB:
            coordinate_budget["skipped_due_floor"] += 1
            result["coordinate_status"] = "coordinate_download_skipped_due_disk_floor"
            result["blockers"] = [
                f"disk_free_gib_at_or_below_floor_buffer:{current_free_gib:.3f}"
            ]
            return result

        coordinate_budget["remaining"] -= 1
        coordinate_budget["attempted"] += 1
        coordinate_attempt = _fetch_coordinate(
            row,
            coordinate_dir=coordinate_dir,
            fetcher=fetcher,
        )
        result["coordinate_status"] = str(coordinate_attempt.get("status"))
        result["coordinate_download_performed"] = bool(
            coordinate_attempt.get("fetched_now")
        )
        if coordinate_attempt.get("fetched_now"):
            coordinate_budget["performed"] += 1
        if coordinate_attempt.get("coordinate_path"):
            _record_coordinate_file(
                coordinate_index,
                row=row,
                coordinate_path=Path(str(coordinate_attempt["coordinate_path"])),
            )
            coordinate_matches = _coordinate_matches(row, coordinate_index)
        else:
            if coordinate_attempt.get("fetch_error"):
                result["blockers"] = [str(coordinate_attempt["fetch_error"])]
            return result

    if not coordinate_matches:
        result["coordinate_status"] = result["coordinate_status"] or (
            "coordinate_not_materialized_locally"
        )
        result["blockers"] = ["coordinate_not_materialized_locally"]
        return result

    coordinate_path = Path(str(coordinate_matches[0]["path"]))
    result["coordinate_path"] = str(coordinate_path)
    result["coordinate_reused_local"] = coordinate_attempt is None
    if result["coordinate_status"] == "not_attempted":
        result["coordinate_status"] = "coordinate_reused_local_artifact"

    candidate_id = str(row.get("candidate_id") or "")
    sidecar_path = locator_dir / f"{_sidecar_token(candidate_id)}.json"
    result["locator_sidecar_path"] = str(sidecar_path)
    if _is_ready_coordinate_sidecar(sidecar_path, coordinate_path):
        result["ready"] = True
        result["locator_status"] = "coordinate_identity_sidecar_reused"
        result["locator_sidecar_reused"] = True
        return result

    payload, blockers = _coordinate_ready_sidecar_payload(
        row,
        created_utc=created_utc,
        sidecar_path=sidecar_path,
        coordinate_path=coordinate_path,
        coordinate_download_performed=bool(result["coordinate_download_performed"]),
    )
    if payload is None:
        result["locator_status"] = "coordinate_identity_sidecar_blocked"
        result["blockers"] = blockers
        return result

    sidecars_to_write.append((sidecar_path, payload))
    result["ready"] = True
    result["locator_status"] = (
        "coordinate_identity_sidecar_refreshed"
        if sidecar_path.exists()
        else "coordinate_identity_sidecar_materialized"
    )
    return result


def _preview_row(
    import_ready_row: dict[str, Any],
    *,
    locator_sidecar_path: str | None,
) -> dict[str, Any]:
    row = dict(import_ready_row)
    if locator_sidecar_path:
        row["locator_sidecar_path"] = locator_sidecar_path
    row["ready_for_controlled_import_review"] = True
    row["ready_for_production_label_import"] = False
    row.setdefault(
        "next_action",
        (
            "Keep in preview-only controlled import-review queue; structural "
            "duplicate screening and explicit production authorization remain."
        ),
    )
    row.setdefault(
        "remaining_required_before_import",
        [
            "current_countable_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ],
    )
    return row


def _materialized_preview_row(
    source_row: dict[str, Any],
    *,
    coordinate_path: str,
    locator_sidecar_path: str,
) -> dict[str, Any]:
    row = dict(source_row)
    row["terminal_state"] = IMPORT_READY_STATE
    row["wave2_materialization_state"] = (
        "coordinate_and_locator_identity_materialized"
    )
    row["coordinate_path"] = coordinate_path
    row["locator_sidecar_path"] = locator_sidecar_path
    row["ready_for_controlled_import_review"] = True
    row["ready_for_production_label_import"] = False
    row["next_action"] = (
        "Keep in preview-only controlled import-review queue; structural "
        "duplicate screening and explicit production authorization remain."
    )
    row["remaining_required_before_import"] = [
        "current_countable_structural_duplicate_screen",
        "label_factory_gate_and_explicit_review_decision",
        "production_registry_change_authorization",
    ]
    return row


def build_external_materialization_wave2(
    *,
    merged_surface_path: Path = DEFAULT_MERGED_SURFACE_PATH,
    import_ready_source_path: Path = DEFAULT_IMPORT_READY_SOURCE_PATH,
    additional_surface_paths: list[Path] | tuple[Path, ...] | None = None,
    additional_import_ready_source_paths: list[Path] | tuple[Path, ...] | None = None,
    supplemental_review_shard_paths: list[Path] | tuple[Path, ...] | None = None,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    created_utc: str | None = None,
    disk_free_gib_at_start: float | None = None,
    max_coordinate_downloads: int = 0,
    coordinate_fetcher: Callable[[str, str], str] = fetch_external_structure_cif,
    disk_free_gib_provider: Callable[[Path], float] = _free_gib,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[tuple[Path, dict[str, Any]]]]:
    created_utc = created_utc or _utc_now_iso()
    surface_paths = [Path(merged_surface_path)]
    optional_surface_paths, missing_surface_paths = _existing_optional_paths(
        additional_surface_paths
    )
    surface_paths.extend(optional_surface_paths)
    import_ready_paths = [Path(import_ready_source_path)]
    optional_import_paths, missing_import_paths = _existing_optional_paths(
        additional_import_ready_source_paths
    )
    import_ready_paths.extend(optional_import_paths)
    supplemental_paths, missing_supplemental_paths = _existing_optional_paths(
        supplemental_review_shard_paths
    )

    wave2_rows: list[dict[str, Any]] = []
    repair_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    sidecars: list[tuple[Path, dict[str, Any]]] = []
    sidecar_reused = 0
    source_terminal_counts: Counter[str] = Counter()
    selected_source_terminal_counts: Counter[str] = Counter()
    wave2_terminal_counts: Counter[str] = Counter()
    lane_terminal_counts: dict[str, Counter[str]] = defaultdict(Counter)
    coordinate_index = _index_coordinate_files(Path("artifacts"))
    disk_reference_gib = (
        float(disk_free_gib_at_start)
        if disk_free_gib_at_start is not None
        else disk_free_gib_provider(Path("."))
    )
    coordinate_downloads_enabled = (
        max(0, int(max_coordinate_downloads or 0)) > 0
        and disk_reference_gib > COORDINATE_DOWNLOAD_FLOOR_GIB
    )
    coordinate_budget = {
        "remaining": max(0, int(max_coordinate_downloads or 0)),
        "attempted": 0,
        "performed": 0,
        "skipped_due_floor": 0,
        "budget_exhausted": 0,
    }
    coordinate_reused_local_for_wave2 = 0
    coordinate_ready_sidecars_reused = 0
    coordinate_ready_promoted_rows = 0
    coordinate_materialization_blockers: Counter[str] = Counter()

    rows_by_candidate: dict[str, list[dict[str, Any]]] = {}
    source_artifacts: dict[str, dict[str, Any]] = {}
    source_surface_row_count = 0
    for path in surface_paths:
        surface = _read_json(path)
        source_key = _artifact_key(path, surface)
        source_rows = [
            row for row in _as_list(surface.get("rows")) if isinstance(row, dict)
        ]
        source_surface_row_count += len(source_rows)
        record = _source_record(path)
        record["artifact_id"] = surface.get("artifact_id")
        record["rows_consumed"] = len(source_rows)
        record["consumption_role"] = "materialization_surface"
        source_artifacts[source_key] = record
        for source_row in source_rows:
            candidate_id = _candidate_key(source_row)
            if not candidate_id:
                continue
            source_state = str(source_row.get("terminal_state") or "")
            source_terminal_counts[source_state] += 1
            rows_by_candidate.setdefault(candidate_id, []).append(
                _row_with_source(source_row, source_key=source_key, source_path=path)
            )

    import_by_candidate: dict[str, dict[str, Any]] = {}
    import_source_row_count = 0
    for path in import_ready_paths:
        source = _read_json(path)
        source_key = _artifact_key(path, source)
        import_rows = [
            row for row in _as_list(source.get("rows")) if isinstance(row, dict)
        ]
        import_source_row_count += len(import_rows)
        record = _source_record(path)
        record["artifact_id"] = source.get("artifact_id")
        record["rows_consumed"] = len(import_rows)
        record["consumption_role"] = "import_ready_preview_source"
        source_artifacts[source_key] = record
        for import_row in import_rows:
            candidate_id = _candidate_key(import_row)
            if not candidate_id:
                continue
            row = _row_with_source(import_row, source_key=source_key, source_path=path)
            current = import_by_candidate.get(candidate_id)
            if current is None or _import_rank(row) > _import_rank(current):
                import_by_candidate[candidate_id] = row

    supplemental_review_shards: dict[str, dict[str, Any]] = {}
    for path in supplemental_paths:
        shard = _read_json(path)
        source_key = _artifact_key(path, shard)
        shard_rows = [
            row for row in _as_list(shard.get("rows")) if isinstance(row, dict)
        ]
        record = _source_record(path)
        record["artifact_id"] = shard.get("artifact_id")
        record["rows_consumed"] = len(shard_rows)
        record["consumption_role"] = "supplemental_review_shard_reference"
        record["terminal_state_counts"] = dict(
            sorted(
                Counter(str(row.get("terminal_state") or "unknown") for row in shard_rows).items()
            )
        )
        record["uniprot_candidate_rows"] = sum(
            1 for row in shard_rows if _candidate_key(row).startswith("uniprot:")
        )
        supplemental_review_shards[source_key] = record
        source_artifacts[source_key] = record

    for candidate_id, source_rows in rows_by_candidate.items():
        import_ready_row = import_by_candidate.get(candidate_id)
        row = _select_source_row(source_rows, import_ready_row)
        source_state = str(row.get("terminal_state") or "")
        selected_source_terminal_counts[source_state] += 1
        occurrences = _source_occurrences(source_rows)
        cross_source_duplicate_collapsed = len(source_rows) > 1 or any(
            occurrence["prior_external_duplicate_only"] for occurrence in occurrences
        )
        exact_current_or_external_duplicate = any(
            _is_exact_current_or_external_pilot_duplicate(candidate_row)
            for candidate_row in source_rows + ([import_ready_row] if import_ready_row else [])
        )
        prior_external_duplicate_only = (
            not exact_current_or_external_duplicate
            and any(_is_prior_external_duplicate_only(candidate_row) for candidate_row in source_rows)
        )
        locator_sidecar_path: str | None = None
        coordinate_path_override: str | None = None
        coordinate_status_override: str | None = None
        locator_status_override: str | None = None
        materialization_row: dict[str, Any] | None = None
        if import_ready_row and _exact_locators(import_ready_row):
            materialization_row = import_ready_row
        elif (
            source_state in (SIDECAR_ADVANCE_STATES | {COORDINATE_READY_STATE})
            and _exact_locators(row)
        ):
            materialization_row = row
        materialization_result: dict[str, Any] | None = None
        if materialization_row is not None and not exact_current_or_external_duplicate:
            materialization_result = _coordinate_ready_materialization_for_row(
                materialization_row,
                coordinate_index=coordinate_index,
                coordinate_dir=coordinate_dir,
                locator_dir=locator_dir,
                created_utc=created_utc,
                sidecars_to_write=sidecars,
                fetcher=coordinate_fetcher,
                coordinate_budget=coordinate_budget,
                coordinate_downloads_enabled=coordinate_downloads_enabled,
                disk_free_gib_provider=disk_free_gib_provider,
            )
            if materialization_result.get("coordinate_reused_local"):
                coordinate_reused_local_for_wave2 += 1
            if materialization_result.get("locator_sidecar_reused"):
                coordinate_ready_sidecars_reused += 1
                sidecar_reused += 1
            if not materialization_result.get("ready"):
                for blocker in materialization_result.get("blockers") or [
                    materialization_result.get("coordinate_status") or "unknown"
                ]:
                    coordinate_materialization_blockers[str(blocker)] += 1

        if exact_current_or_external_duplicate:
            wave2_state = "blocked_duplicate_or_current_registry_conflict"
        elif import_ready_row and _ready_import_preview_row(import_ready_row):
            wave2_state = "import_ready_preview_carried_forward"
            preview_rows.append(_preview_row(import_ready_row, locator_sidecar_path=None))
        elif materialization_result and materialization_result.get("ready"):
            wave2_state = "import_ready_preview_materialized_coordinate_locator"
            row = materialization_row or row
            locator_sidecar_path = str(materialization_result["locator_sidecar_path"])
            coordinate_path_override = str(materialization_result["coordinate_path"])
            coordinate_status_override = str(materialization_result["coordinate_status"])
            locator_status_override = str(materialization_result["locator_status"])
            coordinate_ready_promoted_rows += 1
            preview_rows.append(
                _materialized_preview_row(
                    row,
                    coordinate_path=coordinate_path_override,
                    locator_sidecar_path=locator_sidecar_path,
                )
            )
        elif import_ready_row and _exact_locators(import_ready_row):
            locator_sidecar_path, reused = _locator_sidecar_for_row(
                import_ready_row,
                locator_dir=locator_dir,
                created_utc=created_utc,
                sidecars_to_write=sidecars,
            )
            sidecar_reused += int(reused)
            wave2_state = (
                "shard_import_ready_preview_locator_sidecar_reused_coordinate_pending"
                if reused
                else "shard_import_ready_preview_locator_sidecar_materialized_coordinate_pending"
            )
            row = import_ready_row
        elif source_state in SIDECAR_ADVANCE_STATES and _exact_locators(row):
            locator_sidecar_path, reused = _locator_sidecar_for_row(
                row,
                locator_dir=locator_dir,
                created_utc=created_utc,
                sidecars_to_write=sidecars,
            )
            sidecar_reused += int(reused)
            wave2_state = (
                "locator_sidecar_reused_coordinate_pending"
                if reused
                else "locator_sidecar_materialized_coordinate_pending"
            )
        elif source_state == DUPLICATE_STATE:
            if prior_external_duplicate_only and cross_source_duplicate_collapsed:
                wave2_state = "blocked_duplicate_or_current_registry_conflict"
            else:
                wave2_state = "blocked_duplicate_or_current_registry_conflict"
        else:
            wave2_state = f"repair_queue_{source_state or 'unknown'}"

        wave2_row = _compact_wave2_row(
            row,
            wave2_terminal_state=wave2_state,
            locator_sidecar_path=locator_sidecar_path,
            import_ready_row=import_ready_row,
            source_occurrences=occurrences,
            cross_source_duplicate_collapsed=cross_source_duplicate_collapsed,
            coordinate_path_override=coordinate_path_override,
            coordinate_materialization_status_override=coordinate_status_override,
            locator_sidecar_status_override=locator_status_override,
        )
        wave2_rows.append(wave2_row)
        wave2_terminal_counts[wave2_state] += 1
        lane = str(row.get("target_family_lane") or row.get("lane_id") or "unknown")
        lane_terminal_counts[lane][wave2_state] += 1
        if wave2_state not in {
            "import_ready_preview_carried_forward",
            "import_ready_preview_materialized_coordinate_locator",
        }:
            repair_rows.append(wave2_row)

    sidecar_row_count = sum(
        1
        for row in wave2_rows
        if row.get("locator_sidecar_path")
        and row.get("locator_sidecar_status") in {
            "materialized_or_reused_pending_coordinate_identity",
            "coordinate_identity_sidecar_materialized",
            "coordinate_identity_sidecar_refreshed",
            "coordinate_identity_sidecar_reused",
        }
    )
    materialized_preview_rows = [
        row for row in preview_rows if row.get("wave2_materialization_state")
    ]
    coordinate_reused_preview_rows = [
        row
        for row in preview_rows
        if row.get("coordinate_path") and not row.get("wave2_materialization_state")
    ]
    local_coordinate_paths_present = sum(
        1
        for row in coordinate_reused_preview_rows
        if Path(str(row.get("coordinate_path"))).exists()
    )
    local_locator_sidecar_paths_present = sum(
        1
        for row in preview_rows
        if row.get("locator_sidecar_path")
        and not row.get("wave2_materialization_state")
        and Path(str(row.get("locator_sidecar_path"))).exists()
    )
    wave2_coordinate_files = (
        [path for path in coordinate_dir.glob("*") if path.is_file()]
        if coordinate_dir.exists()
        else []
    )
    wave2_coordinate_dir_bytes = sum(path.stat().st_size for path in wave2_coordinate_files)

    counts = {
        "source_surface_rows_consumed": source_surface_row_count,
        "input_rows": len(wave2_rows),
        "unique_candidate_rows": len(wave2_rows),
        "import_ready_source_rows_consumed": import_source_row_count,
        "supplemental_review_shards_consumed": len(supplemental_review_shards),
        "supplemental_review_shard_rows_consumed": sum(
            record["rows_consumed"] for record in supplemental_review_shards.values()
        ),
        "coordinate_downloads_performed": coordinate_budget["performed"],
        "coordinate_downloads_performed_this_invocation": coordinate_budget["performed"],
        "coordinate_downloads_attempted": coordinate_budget["attempted"],
        "coordinate_download_budget": max(0, int(max_coordinate_downloads or 0)),
        "coordinate_download_budget_exhausted": bool(
            coordinate_budget["budget_exhausted"]
        ),
        "coordinate_downloads_skipped_due_disk_floor": coordinate_budget[
            "skipped_due_floor"
        ],
        "coordinate_downloads_enabled": coordinate_downloads_enabled,
        "coordinate_materialized_new": len(wave2_coordinate_files),
        "coordinate_materialized_new_this_invocation": coordinate_budget["performed"],
        "wave2_coordinate_files_present": len(wave2_coordinate_files),
        "wave2_coordinate_dir_bytes": wave2_coordinate_dir_bytes,
        "coordinate_reused_from_local_artifacts_for_wave2": (
            coordinate_reused_local_for_wave2
        ),
        "coordinate_reused_from_consumed_preview": len(coordinate_reused_preview_rows),
        "coordinate_paths_present_from_consumed_preview": local_coordinate_paths_present,
        "locator_sidecars_materialized_new": len(sidecars),
        "locator_sidecars_reused_existing_wave2": sidecar_reused,
        "locator_sidecars_coordinate_identity_reused": coordinate_ready_sidecars_reused,
        "locator_sidecars_reused_from_consumed_preview": local_locator_sidecar_paths_present,
        "coordinate_ready_promoted_preview_count": coordinate_ready_promoted_rows,
        "coordinate_ready_materialized_preview_rows": len(materialized_preview_rows),
        "source_import_ready_preview_rows_consumed": len(import_by_candidate),
        "source_import_ready_preview_coordinate_pending_count": (
            wave2_terminal_counts[
                "shard_import_ready_preview_locator_sidecar_materialized_coordinate_pending"
            ]
            + wave2_terminal_counts[
                "shard_import_ready_preview_locator_sidecar_reused_coordinate_pending"
            ]
        ),
        "import_ready_preview_count": len(preview_rows),
        "repair_queue_count": len(repair_rows),
        "duplicate_conflict_count": wave2_terminal_counts[
            "blocked_duplicate_or_current_registry_conflict"
        ],
        "cross_source_duplicate_collapsed_count": sum(
            1 for row in wave2_rows if row.get("cross_source_duplicate_collapsed")
        ),
        "disk_free_gib_at_start": disk_free_gib_at_start,
        "disk_free_gib_at_end": round(_free_gib(Path(".")), 3),
    }
    validation_checks = {
        "passed": (
            counts["input_rows"]
            == counts["import_ready_preview_count"] + counts["repair_queue_count"]
        )
        and (
            counts["locator_sidecars_materialized_new"]
            + counts["locator_sidecars_reused_existing_wave2"]
            == sidecar_row_count
        ),
        "input_rows_reconcile": (
            counts["input_rows"]
            == counts["import_ready_preview_count"] + counts["repair_queue_count"]
        ),
        "sidecar_count_reconciles": (
            counts["locator_sidecars_materialized_new"]
            + counts["locator_sidecars_reused_existing_wave2"]
            == sidecar_row_count
        ),
        "coordinate_download_guardrail_enforced": True,
        "coordinate_materialization_blocker_counts": dict(
            sorted(coordinate_materialization_blockers.items())
        ),
        "missing_optional_source_surface_paths": missing_surface_paths,
        "missing_optional_import_ready_source_paths": missing_import_paths,
        "missing_optional_supplemental_review_shard_paths": missing_supplemental_paths,
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
            "coordinate_policy": (
                "bounded_coordinate_downloads_enabled_above_10_gib_floor"
                if coordinate_downloads_enabled
                else LOW_DISK_COORDINATE_POLICY
            ),
            "source_pattern": (
                "merges current Wave 2 admission plus landed broad bulk, "
                "metal/phosphoryl/glycoside, near-orphan/diversity, "
                "PLP/radical/cobalamin, and redox/cofactor shard previews "
                "without coordinate downloads"
            ),
        },
        "source_artifacts": source_artifacts,
        "counts": counts,
        "source_terminal_state_counts": dict(sorted(source_terminal_counts.items())),
        "selected_source_terminal_state_counts": dict(
            sorted(selected_source_terminal_counts.items())
        ),
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
            "materialization for the shard-preview and locator-sidecar "
            "continuation rows, then rerun the controlled import-review "
            "preflight before any production registry/import action."
        ),
    }

    import_preview = {
        "artifact_id": IMPORT_READY_ARTIFACT_ID,
        "schema_version": IMPORT_READY_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_count": len(preview_rows),
        "source_artifacts": source_artifacts,
        "guardrails": {
            "label_import_performed": False,
            "preview_only": True,
            "production_registry_edited": False,
            "coordinate_files_recopied_in_this_run": False,
        },
        "rows": preview_rows,
    }
    repair_queue = {
        "artifact_id": REPAIR_QUEUE_ARTIFACT_ID,
        "schema_version": REPAIR_QUEUE_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_count": len(repair_rows),
        "repair_bucket_counts": dict(
            sorted(Counter(row["repair_bucket"] for row in repair_rows).items())
        ),
        "source_artifacts": source_artifacts,
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
        "Wave 2 consumed the 2026-06-09 admission QA surface plus landed broad bulk, metal/phosphoryl/glycoside, near-orphan/diversity, PLP/radical/cobalamin, and redox/cofactor shard previews. It deduped the surfaces into one review surface, carried only controlled-review-ready rows into the import-ready preview, and avoided coordinate downloads while producing source-free locator sidecars for coordinate-continuation rows.",
        "",
        "## Summary",
        "",
        f"- Source surface rows consumed: `{counts['source_surface_rows_consumed']}`",
        f"- Unique input candidates: `{counts['input_rows']}`",
        f"- Import-ready source preview rows consumed: `{counts['import_ready_source_rows_consumed']}`",
        f"- Supplemental review shard rows referenced: `{counts['supplemental_review_shard_rows_consumed']}`",
        f"- Coordinate download budget: `{counts['coordinate_download_budget']}`",
        f"- Coordinate downloads attempted: `{counts['coordinate_downloads_attempted']}`",
        f"- Coordinate downloads performed: `{counts['coordinate_downloads_performed']}`",
        f"- Coordinate downloads performed this invocation: `{counts['coordinate_downloads_performed_this_invocation']}`",
        f"- Coordinate materialized new: `{counts['coordinate_materialized_new']}`",
        f"- Coordinate materialized new this invocation: `{counts['coordinate_materialized_new_this_invocation']}`",
        f"- Wave 2 coordinate files present: `{counts['wave2_coordinate_files_present']}`",
        f"- Coordinate reused from local artifacts for Wave 2: `{counts['coordinate_reused_from_local_artifacts_for_wave2']}`",
        f"- Coordinate reused from consumed preview metadata: `{counts['coordinate_reused_from_consumed_preview']}`",
        f"- Local coordinate paths present from consumed preview: `{counts['coordinate_paths_present_from_consumed_preview']}`",
        f"- Locator sidecars materialized new: `{counts['locator_sidecars_materialized_new']}`",
        f"- Locator sidecars reused from this Wave 2 directory: `{counts['locator_sidecars_reused_existing_wave2']}`",
        f"- Coordinate-identity locator sidecars reused: `{counts['locator_sidecars_coordinate_identity_reused']}`",
        f"- Local locator paths present from consumed preview: `{counts['locator_sidecars_reused_from_consumed_preview']}`",
        f"- Coordinate-ready rows promoted into preview: `{counts['coordinate_ready_promoted_preview_count']}`",
        f"- Coordinate-ready materialized preview rows: `{counts['coordinate_ready_materialized_preview_rows']}`",
        f"- Source import-ready previews kept in coordinate continuation: `{counts['source_import_ready_preview_coordinate_pending_count']}`",
        f"- Import-ready preview count: `{counts['import_ready_preview_count']}`",
        f"- Repair/continuation queue count: `{counts['repair_queue_count']}`",
        f"- Duplicate conflicts: `{counts['duplicate_conflict_count']}`",
        f"- Cross-source duplicates collapsed: `{counts['cross_source_duplicate_collapsed_count']}`",
        f"- Disk free at start GiB: `{counts['disk_free_gib_at_start']}`",
        f"- Disk free at end GiB: `{counts['disk_free_gib_at_end']}`",
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
    additional_surface_paths: list[Path] | tuple[Path, ...] | None = None,
    additional_import_ready_source_paths: list[Path] | tuple[Path, ...] | None = None,
    supplemental_review_shard_paths: list[Path] | tuple[Path, ...] | None = None,
    out_path: Path = DEFAULT_OUT_PATH,
    import_ready_preview_path: Path = DEFAULT_IMPORT_READY_PREVIEW_PATH,
    repair_queue_path: Path = DEFAULT_REPAIR_QUEUE_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    created_utc: str | None = None,
    disk_free_gib_at_start: float | None = None,
    max_coordinate_downloads: int = 0,
    coordinate_fetcher: Callable[[str, str], str] = fetch_external_structure_cif,
) -> dict[str, Any]:
    artifact, import_preview, repair_queue, sidecars = build_external_materialization_wave2(
        merged_surface_path=merged_surface_path,
        import_ready_source_path=import_ready_source_path,
        additional_surface_paths=additional_surface_paths,
        additional_import_ready_source_paths=additional_import_ready_source_paths,
        supplemental_review_shard_paths=supplemental_review_shard_paths,
        locator_dir=locator_dir,
        coordinate_dir=coordinate_dir,
        created_utc=created_utc,
        disk_free_gib_at_start=disk_free_gib_at_start,
        max_coordinate_downloads=max_coordinate_downloads,
        coordinate_fetcher=coordinate_fetcher,
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
