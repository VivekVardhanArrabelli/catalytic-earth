from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query


ARTIFACT_ID = "v3_external_source_ingestion_pilot_current702_20260608"
IMPORT_PREVIEW_ARTIFACT_ID = (
    "v3_external_source_ingestion_import_preview_current702_20260608"
)
BULK_ARTIFACT_ID = "v3_external_bulk_ingestion_scout_current702_20260608"
BULK_IMPORT_PREVIEW_ARTIFACT_ID = (
    "v3_external_bulk_ingestion_provisional_import_preview_current702_20260608"
)
SCHEMA_VERSION = "v3.external_source_ingestion_pilot"
IMPORT_PREVIEW_SCHEMA_VERSION = "v3.external_source_ingestion_import_preview"
BULK_SCHEMA_VERSION = "v3.external_bulk_ingestion_scout"
BULK_IMPORT_PREVIEW_SCHEMA_VERSION = (
    "v3.external_bulk_ingestion_provisional_import_preview"
)

DEFAULT_OUT_PATH = Path(
    "artifacts/v3_external_source_ingestion_pilot_current702_20260608.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/external_source_ingestion_pilot_current702_20260608.md"
)
DEFAULT_IMPORT_PREVIEW_PATH = Path(
    "artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json"
)
DEFAULT_BULK_OUT_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json"
)
DEFAULT_BULK_REPORT_PATH = Path(
    "work/external_bulk_ingestion_scout_current702_20260608.md"
)
DEFAULT_BULK_IMPORT_PREVIEW_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json"
)
DEFAULT_EXTERNAL_PILOT_PATH = Path(
    "artifacts/v3_external_source_ingestion_pilot_current702_20260608.json"
)
DEFAULT_CURRENT_MANIFEST_PATH = Path(
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_LABEL_REGISTRY_PATH = Path("data/registries/curated_mechanism_labels.json")

TERMINAL_STATES = (
    "external_countable_preflight_candidate",
    "locator_ready_candidate",
    "coordinate_ready_pending_locator",
    "locator_repair_candidate",
    "coordinate_repair_candidate",
    "review_only_evidence",
    "reject/OOS_preserve_signal",
    "blocked_duplicate_or_current_registry_conflict",
    "blocked_family_decision",
    "hard_blocked_with_next_action",
)
BULK_TERMINAL_STATES = (
    *(
        "provisional_external_countable_preflight_candidate"
        if state == "external_countable_preflight_candidate"
        else state
        for state in TERMINAL_STATES
    ),
    "blocked_source_retrieval",
)

FEATURE_KEYS = (
    "active_site_features",
    "metal_binding_features",
    "binding_site_features",
    "site_features",
    "modified_residue_features",
    "cross_link_features",
)

FEATURE_CODE_BY_TYPE = {
    "Active site": "ACT_SITE",
    "Metal binding": "METAL",
    "Binding site": "BINDING",
    "Site": "SITE",
    "Modified residue": "MOD_RES",
    "Cross-link": "CROSSLNK",
}

DEFAULT_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "metal_hydrolase",
        "target_family_lane": "metal hydrolase",
        "query": (
            "(reviewed:true) AND (ec:3.*) AND "
            "((protein_name:metallo) OR (protein_name:zinc) OR (protein_name:metal))"
        ),
    },
    {
        "lane_id": "redox_oxygen_sulfur",
        "target_family_lane": "redox oxygen/sulfur",
        "query": (
            "(reviewed:true) AND ((ec:1.14.*) OR (ec:1.8.*) OR "
            "(protein_name:oxygenase) OR (protein_name:sulfur))"
        ),
    },
    {
        "lane_id": "plp_children",
        "target_family_lane": "PLP children",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate") OR (protein_name:aminotransferase))'
        ),
    },
    {
        "lane_id": "glycoside_nucleoside",
        "target_family_lane": "glycoside/nucleoside",
        "query": "(reviewed:true) AND (ec:3.2.*)",
    },
    {
        "lane_id": "phosphoryl_transfer",
        "target_family_lane": "phosphoryl transfer",
        "query": (
            "(reviewed:true) AND ((ec:2.7.*) OR "
            "(protein_name:phosphotransferase))"
        ),
    },
    {
        "lane_id": "radical_sam_cobalamin",
        "target_family_lane": "radical-SAM/cobalamin",
        "query": (
            '(reviewed:true) AND ((protein_name:"radical SAM") OR '
            '(keyword:"S-adenosyl-L-methionine") OR (keyword:Cobalamin) OR '
            "(protein_name:cobalamin))"
        ),
    },
    {
        "lane_id": "near_orphan_no_reliable_structure",
        "target_family_lane": "near-orphan/no-reliable-structure",
        "query": "(reviewed:true) AND (protein_name:uncharacterized)",
    },
)

DEFAULT_BULK_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "metal_hydrolase",
        "target_family_lane": "metal hydrolase",
        "query": (
            "(reviewed:true) AND (ec:3.*) AND "
            "((protein_name:metallo) OR (protein_name:zinc) OR "
            "(protein_name:metal) OR (cc_cofactor:zinc))"
        ),
    },
    {
        "lane_id": "redox_oxygen_sulfur",
        "target_family_lane": "redox oxygen/sulfur",
        "query": (
            "(reviewed:true) AND ((ec:1.14.*) OR (ec:1.8.*) OR "
            "(protein_name:oxygenase) OR (protein_name:sulfur) OR "
            '(keyword:"Iron-sulfur") OR (cc_cofactor:heme))'
        ),
    },
    {
        "lane_id": "plp_children",
        "target_family_lane": "PLP children",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate") OR (protein_name:aminotransferase) '
            "OR (protein_name:decarboxylase))"
        ),
    },
    {
        "lane_id": "glycoside_nucleoside",
        "target_family_lane": "glycoside/nucleoside",
        "query": (
            "(reviewed:true) AND ((ec:3.2.*) OR (ec:2.4.*) OR "
            "(protein_name:glycosidase) OR (protein_name:nucleosidase))"
        ),
    },
    {
        "lane_id": "phosphoryl_transfer",
        "target_family_lane": "phosphoryl transfer",
        "query": (
            "(reviewed:true) AND ((ec:2.7.*) OR "
            "(protein_name:phosphotransferase) OR (protein_name:kinase))"
        ),
    },
    {
        "lane_id": "radical_sam_cobalamin",
        "target_family_lane": "radical-SAM/cobalamin",
        "query": (
            '(reviewed:true) AND ((protein_name:"radical SAM") OR '
            '(keyword:"S-adenosyl-L-methionine") OR (keyword:Cobalamin) OR '
            "(protein_name:cobalamin) OR (cc_cofactor:cobalamin))"
        ),
    },
    {
        "lane_id": "near_orphan_no_reliable_structure",
        "target_family_lane": "near-orphan/no-reliable-structure",
        "query": (
            "(reviewed:true) AND ((protein_name:uncharacterized) OR "
            "(protein_name:hypothetical) OR (annotation_score:1))"
        ),
    },
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


def _sequence_sha256(sequence: Any) -> str | None:
    if not isinstance(sequence, str) or not sequence:
        return None
    return hashlib.sha256(sequence.encode("utf-8")).hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": _path_sha256(path),
        "bytes": path.stat().st_size,
    }


def _path_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _clean_accession(value: Any) -> str:
    text = str(value or "").strip()
    return text.split(":", 1)[1] if text.startswith("uniprot:") else text


def _is_reviewed(search_record: dict[str, Any], entry_record: dict[str, Any]) -> bool:
    reviewed = str(search_record.get("reviewed") or "").lower()
    entry_type = str(entry_record.get("entry_type") or "").lower()
    return reviewed == "reviewed" or "reviewed" in entry_type or "swiss-prot" in entry_type


def _is_specific_ec(ec_number: Any) -> bool:
    text = str(ec_number or "")
    return bool(text) and "-" not in text and text.count(".") == 3


def _evidence_codes(items: list[dict[str, Any]]) -> list[str]:
    codes: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        for evidence in item.get("evidence", []) or []:
            if not isinstance(evidence, dict):
                continue
            code = evidence.get("evidence_code")
            if code:
                codes.add(str(code))
    return sorted(codes)


def _feature_rows(entry_record: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in FEATURE_KEYS:
        for feature in entry_record.get(key, []) or []:
            if not isinstance(feature, dict):
                continue
            feature_type = str(feature.get("feature_type") or "")
            normalized = {
                "feature_code": FEATURE_CODE_BY_TYPE.get(feature_type, feature_type),
                "feature_type": feature_type,
                "begin": feature.get("begin"),
                "end": feature.get("end"),
                "description": feature.get("description") or "",
                "ligand_name": feature.get("ligand_name"),
                "ligand_id": feature.get("ligand_id"),
                "ligand_note": feature.get("ligand_note"),
                "evidence": feature.get("evidence", []) or [],
                "cross_references": feature.get("cross_references", []) or [],
            }
            stable_key = _canonical_sha256(normalized)
            if stable_key in seen:
                continue
            seen.add(stable_key)
            rows.append(normalized)
    return rows


def _residue_locators(features: list[dict[str, Any]]) -> list[dict[str, Any]]:
    locators: list[dict[str, Any]] = []
    for feature in features:
        begin = feature.get("begin")
        end = feature.get("end")
        if begin is None:
            continue
        locators.append(
            {
                "position": begin,
                "end": end,
                "exact": begin == end,
                "feature_code": feature.get("feature_code"),
                "feature_type": feature.get("feature_type"),
                "ligand_name": feature.get("ligand_name"),
                "ligand_id": feature.get("ligand_id"),
                "evidence_codes": _evidence_codes([feature]),
            }
        )
    return locators


def _coordinate_status(search_record: dict[str, Any]) -> dict[str, Any]:
    pdb_ids = sorted({str(item) for item in _as_list(search_record.get("pdb_ids")) if item})
    alphafold_ids = sorted(
        {str(item) for item in _as_list(search_record.get("alphafold_ids")) if item}
    )
    accession = _clean_accession(search_record.get("accession"))
    if pdb_ids:
        source = "PDB"
        status = "experimental_pdb_coordinate_provenance_available"
        identifier = pdb_ids[0]
    elif alphafold_ids:
        source = "AlphaFoldDB"
        status = "afdb_predicted_coordinate_provenance_available"
        identifier = f"AF-{alphafold_ids[0]}-F1"
    else:
        source = None
        status = "coordinate_provenance_missing"
        identifier = None
    return {
        "coordinate_status": status,
        "coordinate_source": source,
        "coordinate_source_status": status,
        "afdb_or_pdb_identifier": identifier,
        "pdb_ids": pdb_ids,
        "alphafold_ids": alphafold_ids,
        "residue_position_mapping_basis": (
            "UniProt residue positions map directly to AlphaFoldDB/UniProt sequence "
            "coordinates or to UniProt-referenced PDB coordinate provenance"
            if source
            else "no AFDB/PDB coordinate provenance in the fetched UniProt record"
        ),
        "afdb_url": (
            f"https://alphafold.ebi.ac.uk/entry/{alphafold_ids[0]}"
            if alphafold_ids
            else (f"https://alphafold.ebi.ac.uk/entry/{accession}" if accession else None)
        ),
    }


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

    external_label_accessions: set[str] = set()
    for label in label_registry_payload:
        if not isinstance(label, dict):
            continue
        entry_id = str(label.get("entry_id") or "")
        if entry_id.startswith("uniprot:"):
            accession = _clean_accession(entry_id)
            external_label_accessions.add(accession)
            accessions.add(accession)
            accession_to_entries[accession].append(entry_id)

    return {
        "accessions": accessions,
        "sequence_sha_to_entries": {
            key: sorted(set(value)) for key, value in sequence_sha_to_entries.items()
        },
        "accession_to_entries": {
            key: sorted(set(value)) for key, value in accession_to_entries.items()
        },
        "external_label_accessions": sorted(external_label_accessions),
        "current_reference_accession_count": len(accessions),
        "current_sequence_sha_count": len(sequence_sha_to_entries),
    }


def _duplicate_status(
    *,
    accession: str,
    search_record: dict[str, Any],
    current_index: dict[str, Any],
) -> dict[str, Any]:
    sequence_sha = _sequence_sha256(search_record.get("sequence"))
    accession_entries = current_index["accession_to_entries"].get(accession, [])
    sequence_entries = (
        current_index["sequence_sha_to_entries"].get(sequence_sha, [])
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
        "structural_duplicate_screen_status": (
            "not_run_in_external_ingestion_pilot; required before production import"
        ),
    }


def _cofactor_provenance(entry_record: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for comment in entry_record.get("cofactor_comments", []) or []:
        if not isinstance(comment, dict):
            continue
        for cofactor in comment.get("cofactors", []) or []:
            if not isinstance(cofactor, dict):
                continue
            rows.append(
                {
                    "name": cofactor.get("name"),
                    "cross_reference": cofactor.get("cross_reference"),
                    "evidence_codes": _evidence_codes([cofactor]),
                }
            )
    return rows


def _rhea_provenance_from_uniprot(entry_record: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for comment in entry_record.get("catalytic_activity_comments", []) or []:
        if not isinstance(comment, dict):
            continue
        for reference in comment.get("cross_references", []) or []:
            if not isinstance(reference, dict):
                continue
            if str(reference.get("database") or "").lower() != "rhea":
                continue
            rows.append(
                {
                    "source": "uniprot_catalytic_activity_cross_reference",
                    "rhea_id": reference.get("id"),
                    "ec_number": comment.get("ec_number"),
                    "reaction": comment.get("reaction"),
                    "evidence_codes": _evidence_codes([comment]),
                }
            )
    return rows


def _rhea_fallback_rows(
    *,
    accession: str,
    ec_numbers: list[str],
    rhea_fetcher: Callable[[str, int], dict[str, Any]],
    max_reactions_per_ec: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for ec_number in ec_numbers:
        if not _is_specific_ec(ec_number):
            continue
        try:
            payload = rhea_fetcher(ec_number, max_reactions_per_ec)
        except Exception as exc:  # pragma: no cover - live source failure path
            failures.append(
                {
                    "accession": accession,
                    "ec_number": ec_number,
                    "source": "rhea",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        for record in payload.get("records", []) or []:
            if not isinstance(record, dict):
                continue
            rows.append(
                {
                    "source": "rhea_ec_lookup",
                    "rhea_id": record.get("rhea_id"),
                    "ec_number": record.get("ec_number") or ec_number,
                    "equation": record.get("equation"),
                    "mapped_enzyme_count": record.get("mapped_enzyme_count"),
                    "lookup_url": payload.get("metadata", {}).get("url"),
                    "lookup_sha256": _canonical_sha256(record),
                }
            )
        break
    return rows, failures


def _terminal_route(
    *,
    reviewed: bool,
    duplicate_conflict: bool,
    coordinate_available: bool,
    locator_count: int,
    exact_locator_count: int,
    feature_count: int,
    reaction_context_count: int,
    rhea_count: int,
    specific_ec_count: int,
) -> tuple[str, str, str, str]:
    if duplicate_conflict:
        return (
            "blocked_duplicate_or_current_registry_conflict",
            "exact_current702_accession_or_sequence_overlap",
            "blocked",
            "Do not import; preserve as duplicate/current-registry conflict evidence.",
        )
    if not reviewed:
        return (
            "reject/OOS_preserve_signal",
            "source_entry_not_reviewed_swiss_prot",
            "low",
            "Reject for this reviewed-source lane; rerun only after reviewed status changes.",
        )
    if coordinate_available and feature_count == 0 and reaction_context_count == 0:
        return (
            "coordinate_ready_pending_locator",
            "coordinate_provenance_available_but_no_curated_locator_or_reaction_context",
            "low",
            "Keep as near-orphan coordinate-ready row; find residue-level evidence before review.",
        )
    if not coordinate_available and exact_locator_count > 0:
        return (
            "coordinate_repair_candidate",
            "curated_residue_locator_present_but_coordinate_provenance_missing",
            "medium",
            "Find AFDB/PDB or alternate coordinate provenance for the exact locators.",
        )
    if not coordinate_available:
        return (
            "hard_blocked_with_next_action",
            "no_coordinate_provenance_for_reviewed_external_row",
            "low",
            "Hard block until AFDB/PDB coordinate provenance or a no-structure policy exists.",
        )
    if locator_count == 0 and reaction_context_count > 0:
        return (
            "coordinate_ready_pending_locator",
            "coordinate_and_reaction_context_present_but_no_residue_locator",
            "medium",
            "Run locator sourcing/repair from curated features or reviewed literature.",
        )
    if locator_count > 0 and exact_locator_count == 0:
        return (
            "locator_repair_candidate",
            "only_range_or_ambiguous_residue_features_available",
            "medium",
            "Repair range/ambiguous locators to exact residue positions before preflight.",
        )
    if (
        exact_locator_count > 0
        and coordinate_available
        and rhea_count > 0
        and specific_ec_count > 0
    ):
        return (
            "external_countable_preflight_candidate",
            "reviewed_exact_locator_coordinate_and_rhea_or_specific_ec_preflight_clear",
            "high",
            "Stage in external import-preview artifact; run structural duplicate screen before import.",
        )
    if exact_locator_count > 0 and coordinate_available:
        return (
            "locator_ready_candidate",
            "reviewed_exact_locator_and_coordinate_ready_rhea_or_specific_ec_incomplete",
            "medium",
            "Attach Rhea/specific reaction provenance or route to family review.",
        )
    return (
        "review_only_evidence",
        "reviewed_external_evidence_present_but_mechanical_preflight_incomplete",
        "low",
        "Preserve evidence for review; fill the smallest missing locator, coordinate, or reaction gap.",
    )


def _missing_preflight_requirements(
    *,
    reviewed: bool,
    duplicate_conflict: bool,
    coordinate_available: bool,
    exact_locator_count: int,
    rhea_count: int,
    specific_ec_count: int,
) -> list[str]:
    missing: list[str] = []
    if not reviewed:
        missing.append("reviewed_swiss_prot_status")
    if duplicate_conflict:
        missing.append("no_current702_accession_or_sequence_conflict")
    if exact_locator_count < 1:
        missing.append("exact_curated_residue_locator")
    if not coordinate_available:
        missing.append("AFDB_or_PDB_coordinate_provenance")
    if specific_ec_count < 1:
        missing.append("specific_EC_number")
    if rhea_count < 1:
        missing.append("Rhea_or_UniProt_reaction_provenance")
    return missing


def _candidate_row(
    *,
    lane: dict[str, str],
    search_record: dict[str, Any],
    entry_record: dict[str, Any],
    current_index: dict[str, Any],
    source_query_timestamp_utc: str,
    search_metadata: dict[str, Any],
    fetch_rhea_fallback: bool,
    rhea_fetcher: Callable[[str, int], dict[str, Any]],
    max_reactions_per_ec: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    accession = _clean_accession(search_record.get("accession"))
    reviewed = _is_reviewed(search_record, entry_record)
    features = _feature_rows(entry_record)
    locators = _residue_locators(features)
    coordinate = _coordinate_status(search_record)
    duplicate = _duplicate_status(
        accession=accession,
        search_record=search_record,
        current_index=current_index,
    )
    ec_numbers = sorted({str(item) for item in search_record.get("ec_numbers", []) or []})
    catalytic_comments = entry_record.get("catalytic_activity_comments", []) or []
    cofactor_rows = _cofactor_provenance(entry_record)
    rhea_rows = _rhea_provenance_from_uniprot(entry_record)
    rhea_failures: list[dict[str, Any]] = []
    if fetch_rhea_fallback and not rhea_rows:
        fallback_rows, rhea_failures = _rhea_fallback_rows(
            accession=accession,
            ec_numbers=ec_numbers,
            rhea_fetcher=rhea_fetcher,
            max_reactions_per_ec=max_reactions_per_ec,
        )
        rhea_rows.extend(fallback_rows)

    locator_count = len(locators)
    exact_locator_count = sum(1 for locator in locators if locator.get("exact") is True)
    coordinate_available = coordinate["coordinate_status"] != "coordinate_provenance_missing"
    specific_ec_count = sum(1 for ec in ec_numbers if _is_specific_ec(ec))
    terminal_state, route_basis, confidence_tier, next_action = _terminal_route(
        reviewed=reviewed,
        duplicate_conflict=duplicate["duplicate_or_current_registry_conflict"],
        coordinate_available=coordinate_available,
        locator_count=locator_count,
        exact_locator_count=exact_locator_count,
        feature_count=len(features),
        reaction_context_count=len(catalytic_comments),
        rhea_count=len(rhea_rows),
        specific_ec_count=specific_ec_count,
    )

    evidence_codes = sorted(
        set(_evidence_codes(features))
        | set(_evidence_codes([item for item in catalytic_comments if isinstance(item, dict)]))
        | {code for row in cofactor_rows for code in row.get("evidence_codes", [])}
    )
    missing_preflight = _missing_preflight_requirements(
        reviewed=reviewed,
        duplicate_conflict=duplicate["duplicate_or_current_registry_conflict"],
        coordinate_available=coordinate_available,
        exact_locator_count=exact_locator_count,
        rhea_count=len(rhea_rows),
        specific_ec_count=specific_ec_count,
    )
    search_sha = _canonical_sha256(search_record)
    entry_sha = _canonical_sha256(entry_record)
    query_sha = _canonical_sha256(lane["query"])
    return (
        {
            "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
            "candidate_id": f"uniprot:{accession}",
            "accession": accession,
            "reviewed_status": "reviewed" if reviewed else str(search_record.get("reviewed")),
            "protein_name": search_record.get("protein_name"),
            "organism": search_record.get("organism"),
            "sequence_length": search_record.get("length")
            or entry_record.get("sequence_length"),
            "target_family_lane": lane["target_family_lane"],
            "lane_id": lane["lane_id"],
            "source_query": lane["query"],
            "source_evidence_features": features,
            "source_evidence_feature_count": len(features),
            "source_evidence_codes": evidence_codes,
            "residue_locators": locators,
            "residue_locator_count": locator_count,
            "exact_residue_locator_count": exact_locator_count,
            "coordinate_source_status": coordinate["coordinate_source_status"],
            "coordinate_status": coordinate["coordinate_status"],
            "coordinate_source": coordinate["coordinate_source"],
            "afdb_or_pdb_identifier": coordinate["afdb_or_pdb_identifier"],
            "pdb_ids": coordinate["pdb_ids"],
            "alphafold_ids": coordinate["alphafold_ids"],
            "coordinate_mapping_basis": coordinate["residue_position_mapping_basis"],
            "coordinate_mapping_status": (
                "uniprot_residue_position_mapping_assumed_from_afdb_or_uniprot_pdb_cross_reference"
                if coordinate_available
                else "coordinate_mapping_not_available_without_afdb_or_pdb_provenance"
            ),
            "rhea_ec_provenance": {
                "ec_numbers": ec_numbers,
                "specific_ec_count": specific_ec_count,
                "catalytic_activity_comment_count": len(catalytic_comments),
                "rhea_records": rhea_rows,
                "rhea_record_count": len(rhea_rows),
                "rhea_status": "rhea_provenance_available"
                if rhea_rows
                else "rhea_not_found_or_not_queried",
            },
            "cofactor_provenance": cofactor_rows,
            "duplicate_current_registry_conflict_status": duplicate[
                "current_registry_conflict_status"
            ],
            "duplicate_current_registry_conflict": duplicate,
            "source_hashes": {
                "source_query_sha256": query_sha,
                "uniprot_search_row_sha256": search_sha,
                "uniprot_entry_record_sha256": entry_sha,
                "rhea_records_sha256": _canonical_sha256(rhea_rows),
            },
            "source_provenance": {
                "query_timestamp_utc": source_query_timestamp_utc,
                "source_query": lane["query"],
                "source_query_sha256": query_sha,
                "uniprot_search_url": search_metadata.get("url"),
                "uniprot_entry_url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
                "source_hash_basis": "canonical_normalized_source_records",
            },
            "evidence_basis": {
                "reviewed_swiss_prot": reviewed,
                "structured_feature_count": len(features),
                "structured_feature_code_counts": dict(
                    sorted(Counter(feature.get("feature_code") for feature in features).items())
                ),
                "source_evidence_codes": evidence_codes,
                "cofactor_record_count": len(cofactor_rows),
                "exact_residue_locator_count": exact_locator_count,
                "coordinate_status": coordinate["coordinate_status"],
                "specific_ec_count": specific_ec_count,
                "rhea_record_count": len(rhea_rows),
            },
            "blocker_basis": {
                "applicable": bool(missing_preflight)
                or terminal_state
                in {
                    "blocked_duplicate_or_current_registry_conflict",
                    "blocked_family_decision",
                    "review_only_evidence",
                    "reject/OOS_preserve_signal",
                    "hard_blocked_with_next_action",
                    "locator_repair_candidate",
                    "coordinate_repair_candidate",
                    "coordinate_ready_pending_locator",
                },
                "terminal_route_basis": route_basis,
                "missing_preflight_requirements": missing_preflight,
                "duplicate_or_current_registry_conflict": duplicate[
                    "duplicate_or_current_registry_conflict"
                ],
                "source_retrieval_blocker": False,
            },
            "terminal_state": terminal_state,
            "terminal_route_basis": route_basis,
            "confidence_tier": confidence_tier,
            "exact_next_action": next_action,
            "guardrails": {
                "label_import_performed": False,
                "production_registry_edited": False,
                "uses_ec_rhea_or_names_as_predictive_features": False,
                "ec_rhea_or_names_provenance_only": True,
            },
        },
        rhea_failures,
    )


def build_external_source_ingestion_pilot(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    max_records_per_lane: int = 4,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
    fetch_rhea_fallback: bool = True,
    max_reactions_per_ec: int = 2,
) -> dict[str, Any]:
    if max_records_per_lane < 1 or max_records_per_lane > 500:
        raise ValueError("max_records_per_lane must be between 1 and 500")
    created = created_utc or _utc_now_iso()
    current_index = _current_reference_index(
        current_manifest_payload, label_registry_payload
    )
    rows: list[dict[str, Any]] = []
    lane_summaries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = []
    seen_accessions: set[str] = set()

    for lane in lane_queries:
        lane_id = lane["lane_id"]
        query = lane["query"]
        lane_record_count = 0
        try:
            search_payload = query_fetcher(query, max_records_per_lane)
        except Exception as exc:  # pragma: no cover - live source failure path
            fetch_failures.append(
                {
                    "lane_id": lane_id,
                    "source": "uniprot_search",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            lane_summaries.append(
                {
                    "lane_id": lane_id,
                    "target_family_lane": lane["target_family_lane"],
                    "query": query,
                    "record_count": 0,
                    "status": "query_fetch_failed",
                }
            )
            continue

        search_metadata = search_payload.get("metadata", {}) or {}
        for search_record in search_payload.get("records", []) or []:
            if not isinstance(search_record, dict):
                continue
            accession = _clean_accession(search_record.get("accession"))
            if not accession or accession in seen_accessions:
                continue
            seen_accessions.add(accession)
            lane_record_count += 1
            try:
                entry_payload = entry_fetcher(accession)
            except Exception as exc:  # pragma: no cover - live source failure path
                fetch_failures.append(
                    {
                        "lane_id": lane_id,
                        "accession": accession,
                        "source": "uniprot_entry",
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )
                continue
            entry_record = entry_payload.get("record", entry_payload)
            if not isinstance(entry_record, dict):
                fetch_failures.append(
                    {
                        "lane_id": lane_id,
                        "accession": accession,
                        "source": "uniprot_entry",
                        "error_type": "InvalidPayload",
                        "error": "entry fetcher did not return a record dictionary",
                    }
                )
                continue
            candidate, rhea_failures = _candidate_row(
                lane=lane,
                search_record=search_record,
                entry_record=entry_record,
                current_index=current_index,
                source_query_timestamp_utc=created,
                search_metadata=search_metadata,
                fetch_rhea_fallback=fetch_rhea_fallback,
                rhea_fetcher=rhea_fetcher,
                max_reactions_per_ec=max_reactions_per_ec,
            )
            rows.append(candidate)
            fetch_failures.extend(rhea_failures)

        lane_summaries.append(
            {
                "lane_id": lane_id,
                "target_family_lane": lane["target_family_lane"],
                "query": query,
                "record_count": lane_record_count,
                "source_url": search_metadata.get("url"),
                "status": "query_fetched",
            }
        )

    terminal_counts = Counter(row["terminal_state"] for row in rows)
    family_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
    preflight_count = terminal_counts.get("external_countable_preflight_candidate", 0)
    validation_checks = {
        "all_rows_have_terminal_state": all(row.get("terminal_state") for row in rows),
        "all_terminal_states_known": all(
            row.get("terminal_state") in TERMINAL_STATES for row in rows
        ),
        "all_rows_have_source_provenance": all(
            row.get("source_hashes") and row.get("source_provenance") for row in rows
        ),
        "all_rows_have_next_action": all(row.get("exact_next_action") for row in rows),
        "all_rows_have_duplicate_status": all(
            row.get("duplicate_current_registry_conflict_status") for row in rows
        ),
        "candidate_count_matches_rows": len(rows) == sum(terminal_counts.values()),
        "production_registry_edit_count": 0,
    }
    validation_checks["passed"] = all(
        value is True for value in validation_checks.values() if isinstance(value, bool)
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "source_scope": {
            "external_sources": [
                "UniProtKB/Swiss-Prot reviewed entries",
                "AlphaFoldDB/PDB coordinate provenance",
                "Rhea/EC reaction provenance",
            ],
            "excluded_expansion_source": "M-CSA mining excluded; current702 used only as duplicate/conflict context",
            "current_reference_scope": "current702",
        },
        "routing_policy": {
            "terminal_states": list(TERMINAL_STATES),
            "automated_preflight_gate": [
                "reviewed Swiss-Prot status",
                "no exact current702 accession or sequence SHA overlap",
                "at least one exact curated residue locator",
                "AFDB/PDB coordinate provenance available",
                "specific EC and Rhea-style reaction provenance available",
            ],
            "production_import_rule": (
                "No production import is authorized here; preflight rows are "
                "import-preview inputs only and still require structural duplicate "
                "screening and label-factory review before any registry change."
            ),
        },
        "candidate_count": len(rows),
        "import_preview_candidate_count": preflight_count,
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "family_lane_terminal_state_counts": {
            family: dict(sorted(counts.items()))
            for family, counts in sorted(family_counts.items())
        },
        "current_reference_index": {
            "current_reference_accession_count": current_index[
                "current_reference_accession_count"
            ],
            "current_sequence_sha_count": current_index["current_sequence_sha_count"],
            "external_label_accessions": current_index["external_label_accessions"],
        },
        "lane_summaries": lane_summaries,
        "fetch_failures": fetch_failures,
        "fetch_failure_count": len(fetch_failures),
        "rows": rows,
        "validation_checks": validation_checks,
        "guardrails": {
            "production_registry_edited": False,
            "production_import_edited": False,
            "ontology_edited": False,
            "model_weights_or_thresholds_edited": False,
            "heldout_training_or_tuning_performed": False,
            "m_csa_used_as_expansion_source": False,
        },
    }


def build_external_source_ingestion_import_preview(
    artifact: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or artifact.get("created_utc") or _utc_now_iso()
    rows = [
        {
            "stable_candidate_key": row["stable_candidate_key"],
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "confidence_tier": row["confidence_tier"],
            "reviewed_status": row["reviewed_status"],
            "protein_name": row["protein_name"],
            "organism": row["organism"],
            "sequence_length": row["sequence_length"],
            "residue_locators": row["residue_locators"],
            "coordinate_source_status": row["coordinate_source_status"],
            "afdb_or_pdb_identifier": row["afdb_or_pdb_identifier"],
            "rhea_ec_provenance": row["rhea_ec_provenance"],
            "duplicate_current_registry_conflict_status": row[
                "duplicate_current_registry_conflict_status"
            ],
            "source_hashes": row["source_hashes"],
            "import_preview_candidate": True,
            "ready_for_production_label_import": False,
            "remaining_required_before_import": [
                "current_countable_structural_duplicate_screen",
                "label_factory_gate_and_explicit_review_decision",
                "production_registry_change_authorization",
            ],
            "exact_next_action": row["exact_next_action"],
        }
        for row in artifact.get("rows", [])
        if row.get("terminal_state") == "external_countable_preflight_candidate"
    ]
    return {
        "artifact_id": IMPORT_PREVIEW_ARTIFACT_ID,
        "schema_version": IMPORT_PREVIEW_SCHEMA_VERSION,
        "created_utc": created,
        "source_artifact_id": artifact.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(artifact),
        "candidate_count": len(rows),
        "rows": rows,
        "guardrails": {
            "production_registry_edited": False,
            "label_import_performed": False,
            "preview_only": True,
        },
    }


def render_external_source_ingestion_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# External Source Ingestion Pilot - current702",
        "",
        "Read-only external-source ingestion pilot for reviewed Swiss-Prot rows, "
        "AFDB/PDB coordinate provenance, and Rhea/EC reaction provenance. No "
        "production registry, ontology, import, model, split, or threshold was edited.",
        "",
        "## Summary",
        "",
        f"- Candidate rows: {artifact['candidate_count']}",
        f"- Import-preview preflight rows: {artifact['import_preview_candidate_count']}",
        f"- Fetch failures: {artifact['fetch_failure_count']}",
        f"- Validation passed: {artifact['validation_checks']['passed']}",
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    terminal_states = sorted(artifact["terminal_state_counts"])
    lines.extend(["", "## Family/Lane Counts", "", "| family/lane | " + " | ".join(terminal_states) + " |"])
    lines.append("| --- | " + " | ".join("---:" for _ in terminal_states) + " |")
    for family, counts in artifact["family_lane_terminal_state_counts"].items():
        values = [str(counts.get(state, 0)) for state in terminal_states]
        lines.append(f"| {family} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## Candidate Matrix",
            "",
            "| candidate | lane | terminal state | locators | coordinate | conflict | next action |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in artifact["rows"]:
        lines.append(
            "| "
            f"`{row['candidate_id']}` | {row['target_family_lane']} | "
            f"`{row['terminal_state']}` | {row['exact_residue_locator_count']} | "
            f"{row['coordinate_source_status']} | "
            f"{row['duplicate_current_registry_conflict_status']} | "
            f"{row['exact_next_action']} |"
        )

    lines.extend(["", "## Source Queries", "", "| lane | records | query |", "| --- | ---: | --- |"])
    for lane in artifact["lane_summaries"]:
        query = str(lane.get("query") or "").replace("|", "\\|")
        lines.append(
            f"| {lane['target_family_lane']} | {lane['record_count']} | `{query}` |"
        )
    return "\n".join(lines) + "\n"


def write_external_source_ingestion_pilot(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    import_preview_path: Path | None = DEFAULT_IMPORT_PREVIEW_PATH,
    created_utc: str | None = None,
    max_records_per_lane: int = 4,
    fetch_rhea_fallback: bool = True,
) -> dict[str, Any]:
    current_manifest_payload = _read_json(current_manifest_path)
    label_registry_payload = _read_json(label_registry_path)
    artifact = build_external_source_ingestion_pilot(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=label_registry_payload,
        created_utc=created_utc,
        max_records_per_lane=max_records_per_lane,
        fetch_rhea_fallback=fetch_rhea_fallback,
    )
    artifact["source_artifacts"] = {
        "current_manifest": _source_record(current_manifest_path),
        "label_registry": _source_record(label_registry_path),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_source_ingestion_report(artifact), encoding="utf-8"
        )
    if import_preview_path is not None and artifact["import_preview_candidate_count"] > 0:
        preview = build_external_source_ingestion_import_preview(artifact)
        preview["source_artifacts"] = {"external_ingestion_pilot": _source_record(out_path)}
        import_preview_path.parent.mkdir(parents=True, exist_ok=True)
        import_preview_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True), encoding="utf-8"
        )
    return artifact


def _external_pilot_conflict_index(
    external_pilot_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    accessions: dict[str, list[str]] = defaultdict(list)
    sequence_sha_to_candidates: dict[str, list[str]] = defaultdict(list)
    if not external_pilot_payload:
        return {
            "accessions": {},
            "sequence_sha_to_candidates": {},
            "source_artifact_id": None,
            "source_artifact_sha256": None,
        }
    for row in external_pilot_payload.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id") or "")
        accession = _clean_accession(row.get("accession"))
        if accession:
            accessions[accession].append(candidate_id)
        sequence_sha = (
            row.get("duplicate_current_registry_conflict", {}) or {}
        ).get("exact_sequence_sha256")
        if sequence_sha:
            sequence_sha_to_candidates[str(sequence_sha)].append(candidate_id)
    return {
        "accessions": {
            key: sorted(set(value)) for key, value in accessions.items()
        },
        "sequence_sha_to_candidates": {
            key: sorted(set(value))
            for key, value in sequence_sha_to_candidates.items()
        },
        "source_artifact_id": external_pilot_payload.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(external_pilot_payload),
    }


def _bulk_duplicate_status(
    row: dict[str, Any], external_pilot_index: dict[str, Any]
) -> dict[str, Any]:
    accession = _clean_accession(row.get("accession"))
    sequence_sha = (
        row.get("duplicate_current_registry_conflict", {}) or {}
    ).get("exact_sequence_sha256")
    pilot_accession_matches = external_pilot_index["accessions"].get(accession, [])
    pilot_sequence_matches = (
        external_pilot_index["sequence_sha_to_candidates"].get(str(sequence_sha), [])
        if sequence_sha
        else []
    )
    if pilot_accession_matches:
        status = "exact_external_pilot_accession_overlap"
    elif pilot_sequence_matches:
        status = "exact_external_pilot_sequence_sha_overlap"
    else:
        status = "no_exact_external_pilot_accession_or_sequence_sha_overlap"
    return {
        "external_pilot_conflict_status": status,
        "duplicate_or_external_pilot_conflict": bool(
            pilot_accession_matches or pilot_sequence_matches
        ),
        "exact_accession_matched_external_pilot_candidate_ids": pilot_accession_matches,
        "exact_sequence_matched_external_pilot_candidate_ids": pilot_sequence_matches,
        "external_pilot_artifact_id": external_pilot_index.get("source_artifact_id"),
    }


def _refresh_ingestion_counts(
    artifact: dict[str, Any], *, provisional_state: str
) -> None:
    terminal_counts = Counter(row["terminal_state"] for row in artifact.get("rows", []))
    family_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in artifact.get("rows", []):
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
    artifact["candidate_count"] = len(artifact.get("rows", []))
    artifact["import_preview_candidate_count"] = terminal_counts.get(
        provisional_state, 0
    )
    artifact["terminal_state_counts"] = dict(sorted(terminal_counts.items()))
    artifact["family_lane_terminal_state_counts"] = {
        family: dict(sorted(counts.items()))
        for family, counts in sorted(family_counts.items())
    }
    validation_checks = artifact.get("validation_checks", {})
    validation_checks.update(
        {
            "all_rows_have_terminal_state": all(
                row.get("terminal_state") for row in artifact.get("rows", [])
            ),
            "all_terminal_states_known": all(
                row.get("terminal_state") in BULK_TERMINAL_STATES
                for row in artifact.get("rows", [])
            ),
            "all_rows_have_source_provenance": all(
                row.get("source_hashes") and row.get("source_provenance")
                for row in artifact.get("rows", [])
            ),
            "all_rows_have_source_query_hash_timestamp": all(
                (row.get("source_hashes") or {}).get("source_query_sha256")
                and (row.get("source_provenance") or {}).get("query_timestamp_utc")
                for row in artifact.get("rows", [])
            ),
            "all_rows_have_evidence_basis": all(
                row.get("evidence_basis") for row in artifact.get("rows", [])
            ),
            "all_rows_have_blocker_basis": all(
                row.get("blocker_basis") for row in artifact.get("rows", [])
            ),
            "all_rows_have_next_action": all(
                row.get("exact_next_action") for row in artifact.get("rows", [])
            ),
            "all_rows_have_duplicate_status": all(
                row.get("duplicate_status_summary")
                for row in artifact.get("rows", [])
            ),
            "candidate_count_matches_rows": artifact["candidate_count"]
            == sum(terminal_counts.values()),
            "production_registry_edit_count": 0,
        }
    )
    validation_checks["passed"] = all(
        value is True for value in validation_checks.values() if isinstance(value, bool)
    )
    artifact["validation_checks"] = validation_checks


def _source_retrieval_summary(fetch_failures: list[dict[str, Any]]) -> dict[str, Any]:
    source_counts = Counter(str(item.get("source") or "unknown") for item in fetch_failures)
    return {
        "failure_count": len(fetch_failures),
        "failure_counts_by_source": dict(sorted(source_counts.items())),
        "source_retrieval_failures_reported": bool(fetch_failures),
    }


def _bulk_query_continuation_plan(
    *,
    lane_queries: tuple[dict[str, str], ...],
    max_records_per_lane: int,
    fetch_rhea_fallback: bool,
) -> list[dict[str, Any]]:
    next_size: int | None = min(500, max_records_per_lane * 2)
    if next_size == max_records_per_lane:
        next_size = None
    plan: list[dict[str, Any]] = []
    for lane in lane_queries:
        plan.append(
            {
                "lane_id": lane["lane_id"],
                "target_family_lane": lane["target_family_lane"],
                "current_query": lane["query"],
                "next_query": lane["query"],
                "next_action": (
                    f"Rerun this lane with --max-records-per-lane {next_size}; "
                    "keep Rhea fallback disabled unless reaction provenance is the limiter."
                    if next_size is not None
                    else "Add UniProt cursor pagination or split this lane by EC/keyword subquery before increasing beyond the single-query 500-row limit."
                ),
                "rhea_fallback_currently_enabled": fetch_rhea_fallback,
            }
        )
    return plan


def _apply_bulk_scout_policy(
    artifact: dict[str, Any],
    *,
    external_pilot_payload: dict[str, Any] | None,
    max_records_per_lane: int,
    lane_queries: tuple[dict[str, str], ...],
    fetch_rhea_fallback: bool,
) -> dict[str, Any]:
    bulk = json.loads(json.dumps(artifact))
    external_pilot_index = _external_pilot_conflict_index(external_pilot_payload)
    provisional_state = "provisional_external_countable_preflight_candidate"
    for row in bulk.get("rows", []):
        pilot_duplicate = _bulk_duplicate_status(row, external_pilot_index)
        duplicate_record = row.setdefault("duplicate_current_registry_conflict", {})
        duplicate_record["external_pilot_conflict"] = pilot_duplicate
        current_conflict = bool(
            duplicate_record.get("duplicate_or_current_registry_conflict")
        )
        pilot_conflict = pilot_duplicate["duplicate_or_external_pilot_conflict"]
        row["duplicate_external_pilot_conflict_status"] = pilot_duplicate[
            "external_pilot_conflict_status"
        ]
        row["duplicate_status_summary"] = {
            "current702_status": row.get("duplicate_current_registry_conflict_status"),
            "external_pilot_status": row[
                "duplicate_external_pilot_conflict_status"
            ],
            "blocked_by_duplicate_or_current_registry_conflict": bool(
                current_conflict or pilot_conflict
            ),
        }
        if pilot_conflict and not current_conflict:
            row["terminal_state"] = "blocked_duplicate_or_current_registry_conflict"
            row["terminal_route_basis"] = (
                "exact_external_pilot_accession_or_sequence_overlap"
            )
            row["confidence_tier"] = "blocked"
            row["exact_next_action"] = (
                "Do not import; preserve as duplicate of the external pilot row."
            )
            row["blocker_basis"]["applicable"] = True
            row["blocker_basis"]["terminal_route_basis"] = row[
                "terminal_route_basis"
            ]
            row["blocker_basis"][
                "duplicate_or_external_pilot_conflict"
            ] = True
            if (
                "no_external_pilot_accession_or_sequence_conflict"
                not in row["blocker_basis"]["missing_preflight_requirements"]
            ):
                row["blocker_basis"]["missing_preflight_requirements"].append(
                    "no_external_pilot_accession_or_sequence_conflict"
                )
        elif row.get("terminal_state") == "external_countable_preflight_candidate":
            row["terminal_state"] = provisional_state
            row["terminal_route_basis"] = (
                "provisional_reviewed_exact_locator_coordinate_and_rhea_or_specific_ec_preflight_clear"
            )
            row["exact_next_action"] = (
                "Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import."
            )
            row["blocker_basis"]["applicable"] = True
            row["blocker_basis"]["terminal_route_basis"] = row[
                "terminal_route_basis"
            ]
            row["blocker_basis"]["missing_preflight_requirements"] = [
                "ce_external_admission_16_validation_gate"
            ]
        row.setdefault("guardrails", {})[
            "provisional_until_ce_external_admission_16_validation"
        ] = True

    bulk.update(
        {
            "artifact_id": BULK_ARTIFACT_ID,
            "schema_version": BULK_SCHEMA_VERSION,
            "bulk_scout_scope": {
                "source_pattern": "scaled_from_28_row_external_source_ingestion_pilot",
                "pilot_artifact_id": external_pilot_index.get("source_artifact_id"),
                "pilot_artifact_sha256": external_pilot_index.get(
                    "source_artifact_sha256"
                ),
                "requested_max_records_per_lane": max_records_per_lane,
                "lane_count": len(lane_queries),
            },
            "admission_validation_status": {
                "status": "provisional_pending_ce_external_admission_16_validation",
                "required_lane": "ce-external-admission-16-validation",
                "countable_import_authorized": False,
            },
            "routing_policy": {
                "terminal_states": list(BULK_TERMINAL_STATES),
                "automated_preflight_gate": [
                    "reviewed Swiss-Prot status",
                    "no exact current702 accession or sequence SHA overlap",
                    "no exact external pilot accession or sequence SHA overlap",
                    "at least one exact curated residue locator",
                    "AFDB/PDB coordinate provenance available",
                    "specific EC and Rhea-style reaction provenance available",
                    "ce-external-admission-16-validation still pending",
                ],
                "production_import_rule": (
                    "No production import is authorized here; all countable-looking "
                    "bulk rows are provisional until ce-external-admission-16-validation "
                    "confirms the gates and a separate production registry change is authorized."
                ),
            },
            "api_query_limits": {
                "uniprot_search_single_query_size_limit": 500,
                "requested_max_records_per_lane": max_records_per_lane,
                "pagination_implemented": False,
                "rhea_fallback_enabled": fetch_rhea_fallback,
                "coordinate_downloads_performed": False,
            },
            "query_continuation_plan": _bulk_query_continuation_plan(
                lane_queries=lane_queries,
                max_records_per_lane=max_records_per_lane,
                fetch_rhea_fallback=fetch_rhea_fallback,
            ),
            "source_retrieval_summary": _source_retrieval_summary(
                bulk.get("fetch_failures", [])
            ),
        }
    )
    _refresh_ingestion_counts(bulk, provisional_state=provisional_state)
    return bulk


def build_external_bulk_ingestion_scout(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    external_pilot_payload: dict[str, Any] | None = None,
    created_utc: str | None = None,
    max_records_per_lane: int = 100,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_BULK_LANE_QUERIES,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
    fetch_rhea_fallback: bool = False,
    max_reactions_per_ec: int = 1,
) -> dict[str, Any]:
    pilot_artifact = build_external_source_ingestion_pilot(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=label_registry_payload,
        created_utc=created_utc,
        max_records_per_lane=max_records_per_lane,
        lane_queries=lane_queries,
        query_fetcher=query_fetcher,
        entry_fetcher=entry_fetcher,
        rhea_fetcher=rhea_fetcher,
        fetch_rhea_fallback=fetch_rhea_fallback,
        max_reactions_per_ec=max_reactions_per_ec,
    )
    return _apply_bulk_scout_policy(
        pilot_artifact,
        external_pilot_payload=external_pilot_payload,
        max_records_per_lane=max_records_per_lane,
        lane_queries=lane_queries,
        fetch_rhea_fallback=fetch_rhea_fallback,
    )


def build_external_bulk_ingestion_provisional_import_preview(
    artifact: dict[str, Any],
    *,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created = created_utc or artifact.get("created_utc") or _utc_now_iso()
    provisional_state = "provisional_external_countable_preflight_candidate"
    rows = [
        {
            "stable_candidate_key": row["stable_candidate_key"],
            "candidate_id": row["candidate_id"],
            "accession": row["accession"],
            "target_family_lane": row["target_family_lane"],
            "terminal_state": row["terminal_state"],
            "confidence_tier": row["confidence_tier"],
            "reviewed_status": row["reviewed_status"],
            "protein_name": row["protein_name"],
            "organism": row["organism"],
            "sequence_length": row["sequence_length"],
            "residue_locators": row["residue_locators"],
            "coordinate_source_status": row["coordinate_source_status"],
            "coordinate_mapping_status": row["coordinate_mapping_status"],
            "afdb_or_pdb_identifier": row["afdb_or_pdb_identifier"],
            "rhea_ec_provenance": row["rhea_ec_provenance"],
            "duplicate_status_summary": row["duplicate_status_summary"],
            "source_hashes": row["source_hashes"],
            "source_provenance": row["source_provenance"],
            "evidence_basis": row["evidence_basis"],
            "blocker_basis": row["blocker_basis"],
            "import_preview_candidate": True,
            "ready_for_production_label_import": False,
            "provisional_until_ce_external_admission_16_validation": True,
            "remaining_required_before_import": [
                "ce_external_admission_16_validation_gate",
                "current_countable_structural_duplicate_screen",
                "label_factory_gate_and_explicit_review_decision",
                "production_registry_change_authorization",
            ],
            "exact_next_action": row["exact_next_action"],
        }
        for row in artifact.get("rows", [])
        if row.get("terminal_state") == provisional_state
    ]
    return {
        "artifact_id": BULK_IMPORT_PREVIEW_ARTIFACT_ID,
        "schema_version": BULK_IMPORT_PREVIEW_SCHEMA_VERSION,
        "created_utc": created,
        "source_artifact_id": artifact.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(artifact),
        "candidate_count": len(rows),
        "rows": rows,
        "admission_validation_status": artifact.get("admission_validation_status"),
        "guardrails": {
            "production_registry_edited": False,
            "label_import_performed": False,
            "preview_only": True,
            "provisional_until_ce_external_admission_16_validation": True,
        },
    }


def render_external_bulk_ingestion_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# External Bulk Ingestion Scout - current702",
        "",
        "Read-only scale-out scout over reviewed Swiss-Prot/UniProt rows with "
        "structured residue/cofactor evidence, AFDB/PDB coordinate provenance, "
        "and Rhea/EC provenance. All countable-looking rows remain provisional "
        "until `ce-external-admission-16-validation` validates the gate.",
        "",
        "## Summary",
        "",
        f"- Candidate rows: {artifact['candidate_count']}",
        f"- Provisional import-preview rows: {artifact['import_preview_candidate_count']}",
        f"- Fetch failures: {artifact['fetch_failure_count']}",
        f"- Validation passed: {artifact['validation_checks']['passed']}",
        f"- Requested max records per lane: {artifact['api_query_limits']['requested_max_records_per_lane']}",
        f"- Rhea fallback enabled: {artifact['api_query_limits']['rhea_fallback_enabled']}",
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    terminal_states = sorted(artifact["terminal_state_counts"])
    lines.extend(["", "## Family/Lane Counts", "", "| family/lane | " + " | ".join(terminal_states) + " |"])
    lines.append("| --- | " + " | ".join("---:" for _ in terminal_states) + " |")
    for family, counts in artifact["family_lane_terminal_state_counts"].items():
        values = [str(counts.get(state, 0)) for state in terminal_states]
        lines.append(f"| {family} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## Source Retrieval And Limits",
            "",
            f"- UniProt single-query size limit used by this CLI: {artifact['api_query_limits']['uniprot_search_single_query_size_limit']}",
            f"- Pagination implemented: {artifact['api_query_limits']['pagination_implemented']}",
            f"- Coordinate downloads performed: {artifact['api_query_limits']['coordinate_downloads_performed']}",
            f"- Failure counts by source: `{artifact['source_retrieval_summary']['failure_counts_by_source']}`",
            "",
            "## Candidate Matrix",
            "",
            "| candidate | lane | terminal state | locators | coordinate | duplicate status | next action |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in artifact["rows"]:
        duplicate_summary = row.get("duplicate_status_summary", {})
        duplicate_status = (
            f"{duplicate_summary.get('current702_status')} / "
            f"{duplicate_summary.get('external_pilot_status')}"
        )
        lines.append(
            "| "
            f"`{row['candidate_id']}` | {row['target_family_lane']} | "
            f"`{row['terminal_state']}` | {row['exact_residue_locator_count']} | "
            f"{row['coordinate_source_status']} | "
            f"{duplicate_status} | "
            f"{row['exact_next_action']} |"
        )

    lines.extend(["", "## Source Queries", "", "| lane | records | query |", "| --- | ---: | --- |"])
    for lane in artifact["lane_summaries"]:
        query = str(lane.get("query") or "").replace("|", "\\|")
        lines.append(
            f"| {lane['target_family_lane']} | {lane['record_count']} | `{query}` |"
        )

    lines.extend(
        [
            "",
            "## Query Plan To Continue",
            "",
            "| lane | next action |",
            "| --- | --- |",
        ]
    )
    for item in artifact["query_continuation_plan"]:
        action = str(item["next_action"]).replace("|", "\\|")
        lines.append(f"| {item['target_family_lane']} | {action} |")
    return "\n".join(lines) + "\n"


def write_external_bulk_ingestion_scout(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    external_pilot_path: Path | None = DEFAULT_EXTERNAL_PILOT_PATH,
    out_path: Path = DEFAULT_BULK_OUT_PATH,
    report_path: Path | None = DEFAULT_BULK_REPORT_PATH,
    import_preview_path: Path | None = DEFAULT_BULK_IMPORT_PREVIEW_PATH,
    created_utc: str | None = None,
    max_records_per_lane: int = 100,
    fetch_rhea_fallback: bool = False,
) -> dict[str, Any]:
    current_manifest_payload = _read_json(current_manifest_path)
    label_registry_payload = _read_json(label_registry_path)
    external_pilot_payload = (
        _read_json(external_pilot_path)
        if external_pilot_path is not None and external_pilot_path.exists()
        else None
    )
    artifact = build_external_bulk_ingestion_scout(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=label_registry_payload,
        external_pilot_payload=external_pilot_payload,
        created_utc=created_utc,
        max_records_per_lane=max_records_per_lane,
        fetch_rhea_fallback=fetch_rhea_fallback,
    )
    source_artifacts = {
        "current_manifest": _source_record(current_manifest_path),
        "label_registry": _source_record(label_registry_path),
    }
    if external_pilot_path is not None and external_pilot_path.exists():
        source_artifacts["external_source_ingestion_pilot"] = _source_record(
            external_pilot_path
        )
    artifact["source_artifacts"] = source_artifacts
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_bulk_ingestion_report(artifact), encoding="utf-8"
        )
    if import_preview_path is not None and artifact["import_preview_candidate_count"] > 0:
        preview = build_external_bulk_ingestion_provisional_import_preview(artifact)
        preview["source_artifacts"] = {
            "external_bulk_ingestion_scout": _source_record(out_path)
        }
        import_preview_path.parent.mkdir(parents=True, exist_ok=True)
        import_preview_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True), encoding="utf-8"
        )
    return artifact
