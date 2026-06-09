from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .external_source_admission_validation import (
    _clean_accession,
    _coordinate_matches,
    _coordinate_lookup_keys,
    _current_reference_index,
    _index_coordinate_files,
    _locator_matches,
    _normalize_key,
    _reaction_evidence,
    _recomputed_duplicate_status,
    _source_provenance_issues,
    sha256_path,
)
from .structure import STANDARD_AMINO_ACIDS, parse_atom_site_loop
from .transfer_scope import fetch_external_structure_cif


RUN_DATE = "20260608"
ARTIFACT_ID = f"v3_external_materialization_admission_batch_current702_{RUN_DATE}"
IMPORT_READY_ARTIFACT_ID = (
    f"v3_external_materialization_import_ready_preview_current702_{RUN_DATE}"
)
SCHEMA_VERSION = "v3.external_materialization_admission_batch"
IMPORT_READY_SCHEMA_VERSION = "v3.external_materialization_import_ready_preview"
LOCATOR_SIDECAR_SCHEMA_VERSION = (
    "v3.external_source_free_active_site_locator_review_only"
)
LOCATOR_EVIDENCE_CLASS = (
    "reviewed_exact_position_coordinate_local_residue_identity_without_source_text"
)
LOCATOR_POLICY = "review_only_exact_position_coordinate_local_residue_identity"

DEFAULT_READY_PREVIEW_PATH = Path(
    "artifacts/v3_external_source_admission_ready_preview_current702_20260608.json"
)
DEFAULT_PROVISIONAL_PREVIEW_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json"
)
DEFAULT_PILOT_PATH = Path(
    "artifacts/v3_external_source_ingestion_pilot_current702_20260608.json"
)
DEFAULT_BULK_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json"
)
DEFAULT_CURRENT_MANIFEST_PATH = Path(
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_LABEL_REGISTRY_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_OUT_PATH = Path(
    f"artifacts/v3_external_materialization_admission_batch_current702_{RUN_DATE}.json"
)
DEFAULT_IMPORT_READY_PREVIEW_PATH = Path(
    f"artifacts/v3_external_materialization_import_ready_preview_current702_{RUN_DATE}.json"
)
DEFAULT_REPORT_PATH = Path(
    f"work/external_materialization_admission_batch_current702_{RUN_DATE}.md"
)
DEFAULT_COORDINATE_DIR = Path(
    f"artifacts/external_materialized_coordinates_current702_{RUN_DATE}"
)
DEFAULT_LOCATOR_DIR = Path(
    f"artifacts/external_source_free_active_site_locators_current702_{RUN_DATE}"
)

INPUT_QUEUE_PRIORITY = {
    "validated_ready_preview": 0,
    "provisional_bulk_preview": 1,
}
LANE_PRIORITY = {
    "PLP children": 0,
    "phosphoryl transfer": 1,
    "redox oxygen/sulfur": 2,
    "radical-SAM/cobalamin": 3,
    "glycoside/nucleoside": 4,
    "metal hydrolase": 5,
    "near-orphan/no-reliable-structure": 6,
}
IMPORT_READY_TERMINAL_STATE = "import_ready_preview"
REPAIRABLE_COORDINATE_BLOCKER = "repairable_coordinate_blocker"
REPAIRABLE_LOCATOR_BLOCKER = "repairable_locator_blocker"
DUPLICATE_CONFLICT = "duplicate/current-registry conflict"
FAMILY_DECISION_BLOCKER = "family-decision blocker"
REJECT_OOS = "reject/OOS-preserve-signal"
HARD_BLOCKER = "hard blocker"


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


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": sha256_path(path),
        "bytes": path.stat().st_size,
    }


def _sidecar_token(candidate_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", candidate_id.replace(":", "_"))


def _coordinate_file_name(row: dict[str, Any]) -> str | None:
    identifier = str(row.get("afdb_or_pdb_identifier") or "").strip()
    if not identifier:
        return None
    if identifier.upper().startswith("AF-") and "-F1" in identifier.upper():
        return f"{identifier}-model_v6.cif"
    cleaned = identifier.upper().removeprefix("PDB:")
    return f"pdb_{cleaned}.cif"


def _best_structure_source(row: dict[str, Any]) -> tuple[str | None, str | None]:
    alphafold_ids = [str(value).strip() for value in row.get("alphafold_ids", []) or [] if str(value).strip()]
    if alphafold_ids:
        return "alphafold", alphafold_ids[0]
    pdb_ids = [str(value).strip().upper() for value in row.get("pdb_ids", []) or [] if str(value).strip()]
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


def _fetch_coordinate(
    row: dict[str, Any],
    *,
    coordinate_dir: Path,
    fetcher: Callable[[str, str], str] = fetch_external_structure_cif,
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
            "status": "coordinate_reused_existing_batch_file",
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


def _exact_locators(row: dict[str, Any]) -> list[dict[str, Any]]:
    locators = [locator for locator in row.get("residue_locators", []) or [] if isinstance(locator, dict)]
    return [locator for locator in locators if locator.get("exact") is True]


def _role_hint(locator: dict[str, Any]) -> str:
    feature_code = str(locator.get("feature_code") or "")
    if feature_code == "ACT_SITE":
        return "reviewed_active_site_feature"
    if feature_code == "METAL":
        return "reviewed_metal_binding_feature"
    if feature_code == "BINDING":
        ligand_name = str(locator.get("ligand_name") or "").lower()
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
    if feature_code == "CROSSLNK":
        return "reviewed_crosslink_feature"
    return "reviewed_exact_residue_feature"


def _locator_sidecar_payload(
    *,
    row: dict[str, Any],
    coordinate_path: Path,
    created_utc: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    exact_locators = _exact_locators(row)
    if len(exact_locators) < 2:
        return None, ["fewer_than_two_exact_reviewed_residue_locators"]
    position_codes = _position_to_residue_codes(coordinate_path)
    sidecar_locators: list[dict[str, Any]] = []
    blockers: list[str] = []
    for locator in exact_locators:
        try:
            position = int(locator.get("position"))
        except (TypeError, ValueError):
            blockers.append("non_integer_exact_locator_position")
            continue
        codes = sorted(position_codes.get(position, set()))
        if len(codes) != 1:
            blockers.append(
                f"coordinate_residue_code_unresolved_at_position:{position}"
            )
            continue
        sidecar_locators.append(
            {
                "sequence_position": position,
                "residue_code": codes[0],
                "role_hint": _role_hint(locator),
                "locator_confidence": 1.0,
                "locator_evidence_class": LOCATOR_EVIDENCE_CLASS,
                "coordinate_independent_provenance": {
                    "heldout_rows_used": False,
                    "method": "reviewed_exact_position_plus_coordinate_local_residue_identity",
                    "source_text_used": False,
                    "sequence_position_uniprot_validated": True,
                    "reviewed_feature_code": locator.get("feature_code"),
                    "reviewed_feature_type": locator.get("feature_type"),
                },
            }
        )
    if len(sidecar_locators) < 2:
        return None, sorted(set(blockers or ["insufficient_resolved_coordinate_locators"]))
    candidate_id = str(row.get("candidate_id") or "")
    accession = str(row.get("accession") or candidate_id)
    payload = {
        "artifact_id": (
            f"v3_external_source_free_active_site_locator_{_sidecar_token(candidate_id)}"
            f"_current702_{RUN_DATE}"
        ),
        "schema_version": LOCATOR_SIDECAR_SCHEMA_VERSION,
        "created_utc": created_utc,
        "candidate_id": candidate_id,
        "source_accession": accession,
        "locator_policy": LOCATOR_POLICY,
        "locator_evidence_class": LOCATOR_EVIDENCE_CLASS,
        "source_free_active_site_locator_status": "ready",
        "residue_locators": sidecar_locators,
        "forbidden_feature_audit": {
            "entry_name": False,
            "ec_identifiers": False,
            "rhea_identifiers": False,
            "source_prose": False,
            "mechanism_text": False,
            "source_review_rationale": False,
            "label_type": False,
            "fingerprint_id": False,
            "benchmark_role": False,
            "panel_id_as_feature": False,
        },
        "split_protection": {
            "review_only": True,
            "allowed_for_training": False,
            "allowed_for_threshold_selection": False,
            "ready_for_label_import": False,
        },
        "ready_for_predicted_geometry_scoring": False,
        "coordinate_provenance": {
            "coordinate_path": str(coordinate_path),
            "coordinate_sha256": sha256_path(coordinate_path),
            "afdb_or_pdb_identifier": row.get("afdb_or_pdb_identifier"),
            "coordinate_mapping_basis": row.get("coordinate_mapping_basis"),
        },
        "guardrails": {
            "review_only": True,
            "source_text_or_label_fields_used_as_predictive_features": False,
            "label_import_performed": False,
            "production_registry_edited": False,
        },
    }
    violations = _validate_locator_sidecar(payload)
    if violations:
        return None, violations
    return payload, []


def _validate_locator_sidecar(sidecar: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for field in (
        "artifact_id",
        "schema_version",
        "created_utc",
        "candidate_id",
        "source_accession",
        "locator_policy",
        "locator_evidence_class",
        "source_free_active_site_locator_status",
        "residue_locators",
        "forbidden_feature_audit",
        "split_protection",
    ):
        if field not in sidecar:
            violations.append(f"missing_top_level_field:{field}")
    if sidecar.get("source_free_active_site_locator_status") != "ready":
        violations.append("source_free_active_site_locator_status_not_ready")
    locators = [
        locator for locator in sidecar.get("residue_locators", []) if isinstance(locator, dict)
    ]
    if len(locators) < 2:
        violations.append("insufficient_residue_locators")
    for index, locator in enumerate(locators):
        for field in (
            "sequence_position",
            "residue_code",
            "role_hint",
            "locator_confidence",
            "locator_evidence_class",
            "coordinate_independent_provenance",
        ):
            if field not in locator:
                violations.append(f"residue_locator_{index}_missing_field:{field}")
        if locator.get("locator_evidence_class") != LOCATOR_EVIDENCE_CLASS:
            violations.append(f"residue_locator_{index}_unexpected_locator_evidence_class")
        if not isinstance(locator.get("sequence_position"), int):
            violations.append(f"residue_locator_{index}_sequence_position_not_int")
        provenance = locator.get("coordinate_independent_provenance") or {}
        if provenance.get("source_text_used") is not False:
            violations.append(f"residue_locator_{index}_source_text_used")
        if provenance.get("heldout_rows_used") is not False:
            violations.append(f"residue_locator_{index}_heldout_rows_used")
        if provenance.get("sequence_position_uniprot_validated") is not True:
            violations.append(
                f"residue_locator_{index}_sequence_position_not_uniprot_validated"
            )
    for value in (sidecar.get("forbidden_feature_audit") or {}).values():
        if value is not False:
            violations.append("forbidden_feature_audit_has_nonfalse_flags")
            break
    split = sidecar.get("split_protection") or {}
    if split.get("review_only") is not True:
        violations.append("split_protection_review_only_not_true")
    for field in ("allowed_for_training", "allowed_for_threshold_selection", "ready_for_label_import"):
        if split.get(field) is not False:
            violations.append(f"split_protection_{field}_not_false")
    if sidecar.get("ready_for_predicted_geometry_scoring") is not False:
        violations.append("ready_for_predicted_geometry_scoring_not_false")
    return sorted(set(violations))


def _queue_rows(
    ready_preview: dict[str, Any],
    provisional_preview: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for queue_name, payload in (
        ("validated_ready_preview", ready_preview),
        ("provisional_bulk_preview", provisional_preview),
    ):
        for row in payload.get("rows", []) or []:
            if not isinstance(row, dict):
                continue
            candidate_id = str(row.get("candidate_id") or "")
            if not candidate_id or candidate_id in seen:
                continue
            seen.add(candidate_id)
            rows.append(
                {
                    "queue_name": queue_name,
                    "candidate_id": candidate_id,
                    "queue_row": row,
                }
            )
    return sorted(
        rows,
        key=lambda row: (
            INPUT_QUEUE_PRIORITY.get(row["queue_name"], 99),
            LANE_PRIORITY.get(
                str(row["queue_row"].get("target_family_lane") or ""), 99
            ),
            row["candidate_id"],
        ),
    )


def _known_lanes(*payloads: dict[str, Any]) -> set[str]:
    lanes: set[str] = set()
    for payload in payloads:
        for row in payload.get("rows", []) or []:
            lane = row.get("target_family_lane")
            if lane:
                lanes.add(str(lane))
    return lanes


def _full_row_lookup(*payloads: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        for row in payload.get("rows", []) or []:
            if (
                isinstance(row, dict)
                and row.get("candidate_id")
                and str(row["candidate_id"]) not in lookup
            ):
                lookup[str(row["candidate_id"])] = row
    return lookup


def _lane_or_family_issues(row: dict[str, Any], known_lanes: set[str]) -> list[str]:
    issues: list[str] = []
    lane = row.get("target_family_lane")
    if lane not in known_lanes:
        issues.append("target_family_lane_not_in_known_external_lanes")
    reaction = _reaction_evidence(row)
    if reaction["specific_ec_count"] < 1:
        issues.append("specific_ec_provenance_missing")
    if reaction["rhea_record_count"] < 1:
        issues.append("rhea_reaction_provenance_missing")
    return sorted(set(issues))


def _input_row_payload(
    *,
    queue_name: str,
    queue_row: dict[str, Any],
    full_row: dict[str, Any],
    known_lanes: set[str],
    current_index: dict[str, Any],
    coordinate_index: dict[str, list[dict[str, Any]]],
    locator_index: dict[str, list[dict[str, Any]]],
    coordinate_dir: Path,
    locator_dir: Path,
    created_utc: str,
    fetcher: Callable[[str, str], str],
) -> dict[str, Any]:
    candidate_id = str(full_row.get("candidate_id") or queue_row.get("candidate_id") or "")
    duplicate = _recomputed_duplicate_status(full_row, current_index)
    source_issues = _source_provenance_issues(full_row)
    family_issues = _lane_or_family_issues(full_row, known_lanes)
    exact_locators = _exact_locators(full_row)
    existing_coordinate_matches = _coordinate_matches(full_row, coordinate_index)
    coordinate_attempt = None
    coordinate_matches = existing_coordinate_matches
    if not coordinate_matches and len(exact_locators) >= 2:
        coordinate_attempt = _fetch_coordinate(
            full_row, coordinate_dir=coordinate_dir, fetcher=fetcher
        )
        if coordinate_attempt.get("coordinate_path"):
            coordinate_index = _index_coordinate_files(Path("artifacts"))
            coordinate_matches = _coordinate_matches(full_row, coordinate_index)
    locator_matches = _locator_matches(full_row, locator_index)
    locator_sidecar_path = None
    locator_violations: list[str] = []
    locator_materialized_now = False
    coordinate_path = None
    if coordinate_matches:
        coordinate_path = Path(coordinate_matches[0]["path"])
    elif coordinate_attempt and coordinate_attempt.get("coordinate_path"):
        coordinate_path = Path(str(coordinate_attempt["coordinate_path"]))
    if not locator_matches and coordinate_path is not None and len(exact_locators) >= 2:
        payload, locator_violations = _locator_sidecar_payload(
            row=full_row,
            coordinate_path=coordinate_path,
            created_utc=created_utc,
        )
        if payload is not None:
            locator_sidecar_path = locator_dir / f"{_sidecar_token(candidate_id)}.json"
            locator_dir.mkdir(parents=True, exist_ok=True)
            locator_sidecar_path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            locator_materialized_now = True
            locator_index = _index_external_locator_sidecars(locator_dir)
            locator_matches = _locator_matches(full_row, locator_index)
    elif locator_matches:
        locator_sidecar_path = Path(str(locator_matches[0].get("approved_locator_path") or locator_matches[0].get("artifact")))

    if duplicate["duplicate_or_current_registry_conflict"]:
        terminal_state = DUPLICATE_CONFLICT
        next_action = "Preserve as duplicate/current702 conflict evidence; do not admit or import."
        blocker_basis = [
            duplicate["current_registry_conflict_status"],
            "exact_current702_accession_or_sequence_conflict_blocks_materialization",
        ]
    elif source_issues:
        terminal_state = HARD_BLOCKER
        next_action = "Repair source provenance or reviewed-status lineage before rerunning this batch."
        blocker_basis = source_issues
    elif family_issues:
        terminal_state = FAMILY_DECISION_BLOCKER
        next_action = "Resolve family/lane or Rhea/specific-EC provenance gaps before admission."
        blocker_basis = family_issues
    elif len(exact_locators) == 0:
        terminal_state = REJECT_OOS
        next_action = "Preserve signal only; this row lacks any exact reviewed residue locators for safe source-free admission."
        blocker_basis = ["no_exact_reviewed_residue_locators"]
    elif len(exact_locators) < 2:
        terminal_state = REPAIRABLE_LOCATOR_BLOCKER
        next_action = "Expand to at least two source-free locators via coordinate-local review before any import-ready preview."
        blocker_basis = ["fewer_than_two_exact_reviewed_residue_locators"]
    elif not coordinate_matches:
        terminal_state = REPAIRABLE_COORDINATE_BLOCKER
        next_action = "Materialize a supported AFDB/PDB coordinate locally, then rerun locator sidecar materialization."
        blocker_basis = [
            (coordinate_attempt or {}).get("status")
            or "coordinate_not_materialized_locally"
        ]
        if coordinate_attempt and coordinate_attempt.get("fetch_error"):
            blocker_basis.append(str(coordinate_attempt["fetch_error"]))
    elif not locator_matches:
        terminal_state = REPAIRABLE_LOCATOR_BLOCKER
        next_action = "Resolve coordinate-to-sequence residue code mapping or choose an alternate coordinate, then rerun sidecar materialization."
        blocker_basis = locator_violations or [
            "source_free_locator_sidecar_not_materialized"
        ]
    else:
        terminal_state = IMPORT_READY_TERMINAL_STATE
        next_action = (
            "Stage in preview-only external import queue; structural duplicate screening "
            "and explicit production authorization still remain outside this lane."
        )
        blocker_basis = []

    row_payload = {
        "candidate_id": candidate_id,
        "accession": full_row.get("accession"),
        "stable_candidate_key": full_row.get("stable_candidate_key"),
        "target_family_lane": full_row.get("target_family_lane"),
        "queue_name": queue_name,
        "input_preview_terminal_state": queue_row.get("terminal_state"),
        "terminal_state": terminal_state,
        "coordinate_materialized": bool(coordinate_matches),
        "locator_sidecar_materialized": bool(locator_matches),
        "coordinate_materialized_now": bool(
            coordinate_attempt and coordinate_attempt.get("fetched_now")
        ),
        "locator_sidecar_materialized_now": locator_materialized_now,
        "coordinate_path": str(coordinate_path) if coordinate_path is not None else None,
        "locator_sidecar_path": str(locator_sidecar_path) if locator_sidecar_path else None,
        "exact_residue_locator_count": len(exact_locators),
        "reviewed_status": full_row.get("reviewed_status"),
        "afdb_or_pdb_identifier": full_row.get("afdb_or_pdb_identifier"),
        "duplicate_status": duplicate,
        "blocker_basis": blocker_basis,
        "next_action": next_action,
        "source_hashes": {
            **(full_row.get("source_hashes", {}) or {}),
            "full_row_sha256": _canonical_sha256(full_row),
            "queue_row_sha256": _canonical_sha256(queue_row),
        },
        "source_provenance": full_row.get("source_provenance", {}),
        "evidence_basis": {
            "coordinate_source_status": full_row.get("coordinate_source_status"),
            "coordinate_mapping_basis": full_row.get("coordinate_mapping_basis"),
            "rhea_ec_provenance": full_row.get("rhea_ec_provenance", {}),
            "residue_locators": full_row.get("residue_locators", []),
            "queue_preview_row": queue_row,
            "coordinate_attempt": coordinate_attempt,
        },
        "guardrails": {
            "review_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
            "source_ids_or_names_used_as_predictive_features": False,
        },
    }
    row_payload["row_sha256"] = _canonical_sha256(row_payload)
    return row_payload


def _index_external_locator_sidecars(locator_dir: Path) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    if not locator_dir.exists():
        return index
    for path in locator_dir.glob("*.json"):
        payload = _read_json(path)
        keys = {
            str(payload.get("candidate_id") or ""),
            str(payload.get("source_accession") or ""),
            str(payload.get("candidate_id") or "").replace(":", "_"),
            _clean_accession(payload.get("source_accession")),
        }
        record = {
            "artifact": str(path),
            "approved_locator_path": str(path),
            "status": "review_only_external_locator_sidecar_present",
        }
        for key in sorted(
            {
                normalized
                for normalized in (_normalize_key(value) for value in keys)
                if normalized
            }
        ):
            index.setdefault(key, []).append(record)
    return index


def build_external_materialization_admission_batch(
    *,
    ready_preview_path: Path = DEFAULT_READY_PREVIEW_PATH,
    provisional_preview_path: Path = DEFAULT_PROVISIONAL_PREVIEW_PATH,
    pilot_path: Path = DEFAULT_PILOT_PATH,
    bulk_path: Path = DEFAULT_BULK_PATH,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    created_utc: str | None = None,
    fetcher: Callable[[str, str], str] = fetch_external_structure_cif,
) -> tuple[dict[str, Any], dict[str, Any]]:
    created_utc = created_utc or _utc_now_iso()
    ready_preview = _read_json(ready_preview_path)
    provisional_preview = _read_json(provisional_preview_path)
    pilot = _read_json(pilot_path)
    bulk = _read_json(bulk_path)
    current_index = _current_reference_index(
        _read_json(current_manifest_path), _read_json(label_registry_path)
    )
    known_lanes = _known_lanes(pilot, bulk)
    full_lookup = _full_row_lookup(pilot, bulk)
    coordinate_index = _index_coordinate_files(Path("artifacts"))
    locator_index = _index_external_locator_sidecars(locator_dir)
    row_payloads: list[dict[str, Any]] = []
    queue_rows = _queue_rows(ready_preview, provisional_preview)
    for queue in queue_rows:
        candidate_id = queue["candidate_id"]
        full_row = full_lookup.get(candidate_id)
        if full_row is None:
            row_payloads.append(
                {
                    "candidate_id": candidate_id,
                    "queue_name": queue["queue_name"],
                    "input_preview_terminal_state": queue["queue_row"].get("terminal_state"),
                    "terminal_state": HARD_BLOCKER,
                    "coordinate_materialized": False,
                    "locator_sidecar_materialized": False,
                    "coordinate_materialized_now": False,
                    "locator_sidecar_materialized_now": False,
                    "blocker_basis": ["candidate_missing_from_full_source_artifacts"],
                    "next_action": "Repair preview/source-artifact lineage and rerun the batch.",
                    "guardrails": {
                        "review_only": True,
                        "label_import_performed": False,
                        "production_registry_edited": False,
                    },
                    "row_sha256": None,
                }
            )
            continue
        row_payload = _input_row_payload(
            queue_name=queue["queue_name"],
            queue_row=queue["queue_row"],
            full_row=full_row,
            known_lanes=known_lanes,
            current_index=current_index,
            coordinate_index=coordinate_index,
            locator_index=locator_index,
            coordinate_dir=coordinate_dir,
            locator_dir=locator_dir,
            created_utc=created_utc,
            fetcher=fetcher,
        )
        row_payloads.append(row_payload)
        coordinate_index = _index_coordinate_files(Path("artifacts"))
        locator_index = _index_external_locator_sidecars(locator_dir)

    terminal_counts = dict(
        sorted(Counter(str(row["terminal_state"]) for row in row_payloads).items())
    )
    lane_terminal_counts: dict[str, dict[str, int]] = {}
    for lane in sorted(
        {
            str(row.get("target_family_lane") or "unknown")
            for row in row_payloads
        }
    ):
        lane_rows = [row for row in row_payloads if str(row.get("target_family_lane") or "unknown") == lane]
        lane_terminal_counts[lane] = dict(
            sorted(Counter(str(row["terminal_state"]) for row in lane_rows).items())
        )
    import_ready_rows = [
        {
            "candidate_id": row["candidate_id"],
            "accession": row.get("accession"),
            "stable_candidate_key": row.get("stable_candidate_key"),
            "target_family_lane": row.get("target_family_lane"),
            "afdb_or_pdb_identifier": row.get("afdb_or_pdb_identifier"),
            "coordinate_path": row.get("coordinate_path"),
            "locator_sidecar_path": row.get("locator_sidecar_path"),
            "source_hashes": row.get("source_hashes"),
            "duplicate_status": row.get("duplicate_status"),
            "ready_for_external_label_admission": True,
            "ready_for_production_label_import": False,
            "terminal_state": row["terminal_state"],
            "next_action": row["next_action"],
        }
        for row in row_payloads
        if row["terminal_state"] == IMPORT_READY_TERMINAL_STATE
    ]
    artifact = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc,
        "scope": (
            "Large-scale external materialization/admission batch across the "
            "validated 16-row queue and the 354-row provisional bulk queue. "
            "It preserves source provenance, checks duplicate/current702 conflicts, "
            "materializes supported AFDB/PDB coordinates into a review-only external "
            "bundle, writes review-only source-free locator sidecars, and emits only "
            "preview artifacts without touching production registries or audited "
            "locator directories."
        ),
        "source_artifacts": {
            "ready_preview": _source_record(ready_preview_path),
            "provisional_preview": _source_record(provisional_preview_path),
            "pilot": _source_record(pilot_path),
            "bulk": _source_record(bulk_path),
            "current_manifest": _source_record(current_manifest_path),
            "label_registry": _source_record(label_registry_path),
        },
        "materialization_dirs": {
            "coordinate_dir": str(coordinate_dir),
            "locator_dir": str(locator_dir),
        },
        "counts": {
            "input_rows": len(row_payloads),
            "coordinate_materialized": sum(
                1 for row in row_payloads if row.get("coordinate_materialized")
            ),
            "locator_sidecar_materialized": sum(
                1 for row in row_payloads if row.get("locator_sidecar_materialized")
            ),
            "import_ready_preview": terminal_counts.get(IMPORT_READY_TERMINAL_STATE, 0),
            "repairable_coordinate_blockers": terminal_counts.get(
                REPAIRABLE_COORDINATE_BLOCKER, 0
            ),
            "repairable_locator_blockers": terminal_counts.get(
                REPAIRABLE_LOCATOR_BLOCKER, 0
            ),
            "duplicate_current_registry_conflicts": terminal_counts.get(
                DUPLICATE_CONFLICT, 0
            ),
            "family_decision_blockers": terminal_counts.get(
                FAMILY_DECISION_BLOCKER, 0
            ),
            "reject_oos_preserve_signal": terminal_counts.get(REJECT_OOS, 0),
            "hard_blockers": terminal_counts.get(HARD_BLOCKER, 0),
            "coordinate_fetched_now": sum(
                1 for row in row_payloads if row.get("coordinate_materialized_now")
            ),
            "locator_sidecars_written_now": sum(
                1 for row in row_payloads if row.get("locator_sidecar_materialized_now")
            ),
        },
        "terminal_state_counts": terminal_counts,
        "lane_terminal_state_counts": lane_terminal_counts,
        "guardrails": {
            "review_only": True,
            "production_registry_edited": False,
            "label_import_performed": False,
            "audited_locator_directory_edited": False,
            "m_csa_used_for_external_admission": False,
        },
        "rows": row_payloads,
    }
    import_ready_preview = {
        "artifact_id": IMPORT_READY_ARTIFACT_ID,
        "schema_version": IMPORT_READY_SCHEMA_VERSION,
        "created_utc": created_utc,
        "source_artifact_id": ARTIFACT_ID,
        "source_artifact_sha256": _canonical_sha256(artifact),
        "candidate_count": len(import_ready_rows),
        "terminal_state_counts": {IMPORT_READY_TERMINAL_STATE: len(import_ready_rows)},
        "guardrails": {
            "review_only": True,
            "ready_for_production_label_import": False,
            "production_registry_edited": False,
            "label_import_performed": False,
        },
        "rows": import_ready_rows,
    }
    return artifact, import_ready_preview


def render_external_materialization_admission_batch_report(
    artifact: dict[str, Any], import_ready_preview: dict[str, Any]
) -> str:
    counts = artifact["counts"]
    lines = [
        "# External Materialization Admission Batch - current702",
        "",
        f"Run: {artifact['created_utc']}",
        "",
        artifact["scope"],
        "",
        "## Terminal Counts",
        "",
        f"- Input rows: `{counts['input_rows']}`",
        f"- Coordinate materialized: `{counts['coordinate_materialized']}`",
        f"- Locator sidecar materialized: `{counts['locator_sidecar_materialized']}`",
        f"- Import-ready preview: `{counts['import_ready_preview']}`",
        f"- Repairable coordinate blockers: `{counts['repairable_coordinate_blockers']}`",
        f"- Repairable locator blockers: `{counts['repairable_locator_blockers']}`",
        f"- Duplicate/current-registry conflicts: `{counts['duplicate_current_registry_conflicts']}`",
        f"- Family-decision blockers: `{counts['family_decision_blockers']}`",
        f"- Reject/OOS preserve-signal: `{counts['reject_oos_preserve_signal']}`",
        f"- Hard blockers: `{counts['hard_blockers']}`",
        "",
        "## Lane Counts",
        "",
    ]
    for lane, lane_counts in artifact["lane_terminal_state_counts"].items():
        lines.append(f"- {lane}: `{json.dumps(lane_counts, sort_keys=True)}`")
    lines += [
        "",
        "## Import-Ready Preview",
        "",
        f"- Rows: `{import_ready_preview['candidate_count']}`",
        f"- Preview artifact: `{DEFAULT_IMPORT_READY_PREVIEW_PATH}`",
        "",
        "## Next Actions",
        "",
        "- Non-ready rows keep their exact next action inline in the batch artifact.",
        "- Import-ready preview rows remain preview-only; structural duplicate screening and explicit production authorization are still required outside this lane.",
    ]
    return "\n".join(lines) + "\n"


def _validation_summary(
    artifact: dict[str, Any], import_ready_preview: dict[str, Any]
) -> dict[str, Any]:
    rows = artifact.get("rows", []) or []
    counts = artifact["counts"]
    violations: list[str] = []
    if counts["input_rows"] != len(rows):
        violations.append("input_rows_count_mismatch")
    if counts["import_ready_preview"] != len(import_ready_preview.get("rows", []) or []):
        violations.append("import_ready_preview_count_mismatch")
    if counts["coordinate_materialized"] != sum(
        1 for row in rows if row.get("coordinate_materialized")
    ):
        violations.append("coordinate_materialized_count_mismatch")
    if counts["locator_sidecar_materialized"] != sum(
        1 for row in rows if row.get("locator_sidecar_materialized")
    ):
        violations.append("locator_sidecar_materialized_count_mismatch")
    return {
        "passed": not violations,
        "violations": violations,
        "json_parseable": True,
        "counts_reconciled": not violations,
    }


def write_external_materialization_admission_batch(
    *,
    ready_preview_path: Path = DEFAULT_READY_PREVIEW_PATH,
    provisional_preview_path: Path = DEFAULT_PROVISIONAL_PREVIEW_PATH,
    pilot_path: Path = DEFAULT_PILOT_PATH,
    bulk_path: Path = DEFAULT_BULK_PATH,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    import_ready_preview_path: Path = DEFAULT_IMPORT_READY_PREVIEW_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    locator_dir: Path = DEFAULT_LOCATOR_DIR,
    created_utc: str | None = None,
    fetcher: Callable[[str, str], str] = fetch_external_structure_cif,
) -> dict[str, Any]:
    artifact, import_ready_preview = build_external_materialization_admission_batch(
        ready_preview_path=ready_preview_path,
        provisional_preview_path=provisional_preview_path,
        pilot_path=pilot_path,
        bulk_path=bulk_path,
        current_manifest_path=current_manifest_path,
        label_registry_path=label_registry_path,
        coordinate_dir=coordinate_dir,
        locator_dir=locator_dir,
        created_utc=created_utc,
        fetcher=fetcher,
    )
    artifact["validation"] = _validation_summary(artifact, import_ready_preview)
    _write_json(out_path, artifact)
    _write_json(import_ready_preview_path, import_ready_preview)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_materialization_admission_batch_report(
                artifact, import_ready_preview
            ),
            encoding="utf-8",
        )
    return artifact
