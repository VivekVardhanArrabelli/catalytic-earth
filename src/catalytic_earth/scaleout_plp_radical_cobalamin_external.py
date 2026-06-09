from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_uniprot_entry, fetch_uniprot_query
from .external_source_ingestion import (
    _candidate_row,
    _canonical_sha256,
    _clean_accession,
    _current_reference_index,
    _read_json,
    _source_record,
)


ARTIFACT_ID = "v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609"
IMPORT_READY_ARTIFACT_ID = (
    "v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_"
    "current702_20260609"
)
SCHEMA_VERSION = "v3.external_scaleout_shard_plp_radical_cobalamin"
IMPORT_READY_SCHEMA_VERSION = (
    "v3.external_scaleout_shard_plp_radical_cobalamin_import_ready_preview"
)

DEFAULT_OUT_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609.json"
)
DEFAULT_IMPORT_READY_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_"
    "current702_20260609.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/external_scaleout_shard_plp_radical_cobalamin_current702_20260609.md"
)
DEFAULT_CURRENT_MANIFEST_PATH = Path(
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_LABEL_REGISTRY_PATH = Path("data/registries/curated_mechanism_labels.json")

TERMINAL_STATES = (
    "import_ready_preview",
    "provisional_external_countable_preflight_candidate",
    "locator_ready_candidate",
    "coordinate_ready_pending_locator",
    "repairable_locator_blocker",
    "repairable_coordinate_blocker",
    "blocked_duplicate_or_current_registry_conflict",
    "reject/OOS_preserve_signal",
    "hard_blocked_with_next_action",
    "review_only_evidence",
    "blocked_source_retrieval",
)

DEFAULT_PRIOR_EXTERNAL_ARTIFACT_PATHS = (
    Path("artifacts/v3_external_source_ingestion_pilot_current702_20260608.json"),
    Path("artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json"),
    Path("artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json"),
    Path(
        "artifacts/"
        "v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json"
    ),
    Path("artifacts/v3_external_source_admission_validation_16_current702_20260608.json"),
    Path(
        "artifacts/"
        "v3_external_source_admission_ready_preview_current702_20260608.json"
    ),
    Path("artifacts/v3_external_admission_merged_surface_current702_20260609.json"),
    Path(
        "artifacts/"
        "v3_external_admission_import_ready_preview_current702_20260609.json"
    ),
    Path("artifacts/v3_external_admission_repair_queue_current702_20260609.json"),
    Path("artifacts/v3_scaleout_plp_children_shard_current702_20260608.json"),
    Path("artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json"),
)

DEFAULT_PRIOR_EXTERNAL_BRANCH_SPECS = (
    (
        "origin/ce-external-bulk-pagination-scaleout-20260609:"
        "artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json"
    ),
    (
        "origin/ce-external-bulk-pagination-scaleout-20260609:"
        "artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_"
        "current702_20260609.json"
    ),
    (
        "origin/ce-external-materialization-admission-batch-20260608:"
        "artifacts/v3_external_materialization_admission_batch_current702_20260608.json"
    ),
    (
        "origin/ce-external-materialization-admission-batch-20260608:"
        "artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json"
    ),
)

DEFAULT_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "plp_aminotransferase_specific",
        "target_family_lane": "PLP aminotransferase",
        "lane_group": "plp",
        "mechanism_axis_focus": "proton_transfer_schiff_base_transamination",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:aminotransferase) OR (ec:2.6.*))"
        ),
    },
    {
        "lane_id": "plp_decarboxylase_specific",
        "target_family_lane": "PLP decarboxylase",
        "lane_group": "plp",
        "mechanism_axis_focus": "carbanion_protonation_decarboxylation",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:decarboxylase) OR (ec:4.1.1.*))"
        ),
    },
    {
        "lane_id": "plp_lyase_eliminase",
        "target_family_lane": "PLP lyase/eliminase",
        "lane_group": "plp",
        "mechanism_axis_focus": "beta_gamma_elimination_proton_transfer",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:lyase) OR (protein_name:eliminase) OR "
            "(protein_name:dehydratase) OR (ec:4.4.*) OR (ec:4.3.*))"
        ),
    },
    {
        "lane_id": "plp_racemase_epimerase",
        "target_family_lane": "PLP racemase/epimerase",
        "lane_group": "plp",
        "mechanism_axis_focus": "stereochemical_proton_abstraction_return",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:racemase) OR (protein_name:epimerase) OR (ec:5.1.1.*))"
        ),
    },
    {
        "lane_id": "plp_cystathionine_sulfur_lyase_boundary",
        "target_family_lane": "PLP sulfur lyase boundary",
        "lane_group": "plp",
        "mechanism_axis_focus": "plp_proton_sulfur_beta_elimination",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:cystathionine) OR (protein_name:cysteine) OR "
            "(protein_name:tryptophanase))"
        ),
    },
    {
        "lane_id": "plp_broad_pyridoxal_feature",
        "target_family_lane": "PLP broad cofactor context",
        "lane_group": "plp",
        "mechanism_axis_focus": "plp_cofactor_context_broad",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate"))'
        ),
    },
    {
        "lane_id": "radical_sam_name_specific",
        "target_family_lane": "radical SAM",
        "lane_group": "radical_sam",
        "mechanism_axis_focus": "radical_electron_transfer_sam_cleavage",
        "query": '(reviewed:true) AND (protein_name:"radical SAM")',
    },
    {
        "lane_id": "radical_sam_keyword_fe_s",
        "target_family_lane": "radical SAM iron-sulfur",
        "lane_group": "radical_sam",
        "mechanism_axis_focus": "sf4_sam_electron_transfer_context",
        "query": (
            '(reviewed:true) AND (keyword:"S-adenosyl-L-methionine") AND '
            '(keyword:"Iron-sulfur")'
        ),
    },
    {
        "lane_id": "radical_sam_enzyme_family_names",
        "target_family_lane": "radical SAM named families",
        "lane_group": "radical_sam",
        "mechanism_axis_focus": "radical_rearrangement_or_insertion_context",
        "query": (
            "(reviewed:true) AND ((protein_name:anaerobic) OR "
            "(protein_name:activating) OR (protein_name:spore) OR "
            "(protein_name:biotin) OR (protein_name:lipoate)) AND "
            '(keyword:"S-adenosyl-L-methionine")'
        ),
    },
    {
        "lane_id": "sam_dependent_radical_adjacent",
        "target_family_lane": "SAM-dependent radical-like boundary",
        "lane_group": "radical_sam",
        "mechanism_axis_focus": "sam_radical_context_disambiguation",
        "query": (
            '(reviewed:true) AND ((protein_name:"SAM-dependent") OR '
            '(protein_name:"S-adenosylmethionine")) AND '
            "((protein_name:radical) OR (keyword:Radical))"
        ),
    },
    {
        "lane_id": "cobalamin_radical_rearrangement",
        "target_family_lane": "cobalamin radical rearrangement",
        "lane_group": "cobalamin",
        "mechanism_axis_focus": "adenosylcobalamin_radical_rearrangement",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) '
            'OR (protein_name:cobalamin) OR (protein_name:"vitamin B12")) AND '
            "((protein_name:mutase) OR (protein_name:rearrangement) OR "
            "(protein_name:aminomutase) OR (protein_name:dehydratase))"
        ),
    },
    {
        "lane_id": "b12_adenosylcobalamin_enzymes",
        "target_family_lane": "B12 adenosylcobalamin enzymes",
        "lane_group": "cobalamin",
        "mechanism_axis_focus": "cofactor_context_radical_b12",
        "query": (
            '(reviewed:true) AND ((protein_name:adenosylcobalamin) OR '
            '(protein_name:"coenzyme B12") OR (cc_cofactor:adenosylcobalamin))'
        ),
    },
    {
        "lane_id": "b12_general_cobalamin",
        "target_family_lane": "B12/cobalamin broad enzymes",
        "lane_group": "cobalamin",
        "mechanism_axis_focus": "cobalamin_cofactor_context_broad",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) '
            'OR (protein_name:cobalamin) OR (protein_name:"vitamin B12"))'
        ),
    },
    {
        "lane_id": "coupled_plp_cobalamin_aminomutase",
        "target_family_lane": "coupled PLP adenosylcobalamin aminomutase",
        "lane_group": "cobalamin_plp_coupled",
        "mechanism_axis_focus": "coupled_plp_b12_radical_context",
        "query": (
            '(reviewed:true) AND ((protein_name:aminomutase) OR '
            '(protein_name:"lysine 5,6-aminomutase")) AND '
            '((cc_cofactor:cobalamin) OR (cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:Cobalamin) OR (keyword:"Pyridoxal phosphate"))'
        ),
    },
    {
        "lane_id": "negative_sam_methyltransferase",
        "target_family_lane": "adjacent SAM methyltransferase negative",
        "lane_group": "adjacent_cofactor_confounded_negative",
        "mechanism_axis_focus": "sam_nonradical_methyl_transfer_control",
        "query": (
            '(reviewed:true) AND ((keyword:"S-adenosyl-L-methionine") OR '
            '(protein_name:methyltransferase)) AND '
            "(protein_name:methyltransferase) NOT (protein_name:radical)"
        ),
    },
    {
        "lane_id": "negative_non_plp_decarboxylase",
        "target_family_lane": "adjacent non-PLP decarboxylase negative",
        "lane_group": "adjacent_cofactor_confounded_negative",
        "mechanism_axis_focus": "name_matched_non_plp_control",
        "query": (
            "(reviewed:true) AND (protein_name:decarboxylase) NOT "
            '(keyword:"Pyridoxal phosphate") NOT (cc_cofactor:"pyridoxal phosphate")'
        ),
    },
    {
        "lane_id": "negative_cobalamin_methyltransferase",
        "target_family_lane": "adjacent methylcobalamin negative",
        "lane_group": "adjacent_cofactor_confounded_negative",
        "mechanism_axis_focus": "cobalamin_nonradical_methyl_transfer_control",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) '
            "OR (protein_name:cobalamin)) AND (protein_name:methyltransferase)"
        ),
    },
    {
        "lane_id": "negative_schiff_base_non_plp",
        "target_family_lane": "adjacent Schiff-base non-PLP negative",
        "lane_group": "adjacent_cofactor_confounded_negative",
        "mechanism_axis_focus": "schiff_base_without_plp_control",
        "query": (
            '(reviewed:true) AND (protein_name:"Schiff-base") NOT '
            '(keyword:"Pyridoxal phosphate")'
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


def _sequence_sha256(sequence: Any) -> str | None:
    if not isinstance(sequence, str) or not sequence:
        return None
    return hashlib.sha256(sequence.encode("utf-8")).hexdigest()


def _git_json_spec_payload(spec: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        raw = subprocess.check_output(["git", "show", spec], text=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - live git failure
        return None, {"spec": spec, "status": "git_show_failed", "error": str(exc)}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover - malformed branch artifact
        return None, {"spec": spec, "status": "json_parse_failed", "error": str(exc)}
    return payload, {
        "spec": spec,
        "status": "loaded",
        "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "bytes": len(raw.encode("utf-8")),
    }


def _extract_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("rows", "candidate_rows"):
        for row in payload.get(key, []) or []:
            if isinstance(row, dict):
                rows.append(row)
    for key in ("validated_rows", "admission_ready_rows"):
        for row in payload.get(key, []) or []:
            if isinstance(row, dict):
                rows.append(row)
    return rows


def _row_accessions(row: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for key in ("accession", "candidate_id", "entry_id", "stable_candidate_key"):
        cleaned = _clean_accession(row.get(key))
        if cleaned and re.fullmatch(r"[A-Z0-9]+(?:-[0-9]+)?", cleaned):
            values.add(cleaned)
    for key in ("reference_uniprot_ids", "uniprot_accessions", "accessions"):
        for value in row.get(key, []) or []:
            cleaned = _clean_accession(value)
            if cleaned:
                values.add(cleaned)
    return values


def _row_sequence_sha(row: dict[str, Any]) -> str | None:
    for key in ("sequence_sha256", "exact_sequence_sha256"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    duplicate = row.get("duplicate_current_registry_conflict")
    if isinstance(duplicate, dict):
        value = duplicate.get("exact_sequence_sha256")
        if isinstance(value, str) and value:
            return value
    return None


def _prior_external_index(
    payloads: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    accession_to_matches: dict[str, list[dict[str, str]]] = defaultdict(list)
    sequence_sha_to_matches: dict[str, list[dict[str, str]]] = defaultdict(list)
    row_count = 0
    for source_key, payload in payloads:
        artifact_id = str(payload.get("artifact_id") or source_key)
        for row in _extract_rows(payload):
            row_count += 1
            candidate_id = str(row.get("candidate_id") or row.get("entry_id") or "")
            match = {
                "source_key": source_key,
                "artifact_id": artifact_id,
                "candidate_id": candidate_id,
            }
            for accession in _row_accessions(row):
                accession_to_matches[accession].append(match)
            sequence_sha = _row_sequence_sha(row)
            if sequence_sha:
                sequence_sha_to_matches[sequence_sha].append(match)
    return {
        "accession_to_matches": dict(accession_to_matches),
        "sequence_sha_to_matches": dict(sequence_sha_to_matches),
        "source_artifact_count": len(payloads),
        "indexed_row_count": row_count,
    }


def _dedupe_status(
    *,
    accession: str,
    sequence_sha: str | None,
    prior_index: dict[str, Any],
) -> dict[str, Any]:
    accession_matches = prior_index["accession_to_matches"].get(accession, [])
    sequence_matches = (
        prior_index["sequence_sha_to_matches"].get(sequence_sha, [])
        if sequence_sha
        else []
    )
    conflict = bool(accession_matches or sequence_matches)
    if accession_matches:
        status = "exact_prior_external_accession_overlap"
    elif sequence_matches:
        status = "exact_prior_external_sequence_sha_overlap"
    else:
        status = "no_exact_prior_external_accession_or_sequence_sha_overlap"
    return {
        "prior_external_conflict": conflict,
        "prior_external_conflict_status": status,
        "exact_accession_matched_prior_artifacts": _dedupe_matches(accession_matches),
        "exact_sequence_matched_prior_artifacts": _dedupe_matches(sequence_matches),
    }


def _dedupe_matches(matches: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[dict[str, str]] = []
    for match in matches:
        key = (
            match.get("source_key", ""),
            match.get("artifact_id", ""),
            match.get("candidate_id", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(match)
    return deduped[:12]


def _text_blob(row: dict[str, Any]) -> str:
    parts = [
        row.get("protein_name"),
        row.get("target_family_lane"),
        row.get("lane_id"),
        row.get("source_query"),
    ]
    for cofactor in row.get("cofactor_provenance", []) or []:
        if isinstance(cofactor, dict):
            parts.extend([cofactor.get("name"), cofactor.get("cross_reference")])
    for feature in row.get("source_evidence_features", []) or []:
        if isinstance(feature, dict):
            parts.extend(
                [
                    feature.get("feature_type"),
                    feature.get("description"),
                    feature.get("ligand_name"),
                    feature.get("ligand_id"),
                    feature.get("ligand_note"),
                ]
            )
    return " ".join(str(part or "") for part in parts).lower()


def _cx3cx2c_positions(sequence: str | None) -> list[int]:
    if not sequence:
        return []
    return [match.start() + 1 for match in re.finditer(r"C.{3}C.{2}C", sequence)]


def _cofactor_flags(row: dict[str, Any], search_record: dict[str, Any]) -> dict[str, Any]:
    text = _text_blob(row)
    sequence = str(search_record.get("sequence") or "")
    cx3cx2c_positions = _cx3cx2c_positions(sequence)
    rhea_records = row.get("rhea_ec_provenance", {}).get("rhea_records", []) or []
    direct_rhea = any(
        isinstance(record, dict)
        and record.get("source") == "uniprot_catalytic_activity_cross_reference"
        for record in rhea_records
    )
    return {
        "plp_evidence_present": any(
            token in text
            for token in (
                "pyridoxal",
                "pyridoxamine",
                "plp",
                "llp",
                "pyridoxal phosphate",
            )
        ),
        "sam_or_adomet_evidence_present": any(
            token in text
            for token in (
                "s-adenosyl",
                "adomet",
                "sam",
                "adenosylmethionine",
            )
        ),
        "sf4_or_fe_s_evidence_present": any(
            token in text
            for token in ("iron-sulfur", "iron sulfur", "sf4", "4fe-4s", "fe-s")
        )
        or bool(cx3cx2c_positions),
        "cobalamin_or_b12_evidence_present": any(
            token in text
            for token in ("cobalamin", "vitamin b12", "adenosylcobalamin", "b12")
        ),
        "cx3cx2c_motif_evidence_present": bool(cx3cx2c_positions),
        "cx3cx2c_motif_positions": cx3cx2c_positions[:8],
        "direct_uniprot_rhea_provenance_present": direct_rhea,
    }


def _mechanism_axes(lane: dict[str, str], flags: dict[str, Any]) -> list[str]:
    axes: set[str] = set()
    lane_group = lane.get("lane_group")
    if lane_group == "plp" or flags["plp_evidence_present"]:
        axes.update(["proton_transfer_axis", "cofactor_context_axis"])
    if lane_group in {"radical_sam", "cobalamin_plp_coupled"}:
        axes.update(["electron_transfer_axis", "radical_axis", "cofactor_context_axis"])
    if lane_group in {"cobalamin", "cobalamin_plp_coupled"}:
        axes.update(["radical_axis", "cofactor_context_axis"])
    if flags["sf4_or_fe_s_evidence_present"]:
        axes.add("electron_transfer_axis")
    if lane_group == "adjacent_cofactor_confounded_negative":
        axes.add("cofactor_confounded_negative_axis")
    return sorted(axes)


def _route_terminal_state(
    *,
    row: dict[str, Any],
    lane: dict[str, str],
    prior_status: dict[str, Any],
    flags: dict[str, Any],
) -> tuple[str, str, str, str]:
    current_conflict = row["duplicate_current_registry_conflict"][
        "duplicate_or_current_registry_conflict"
    ]
    if current_conflict or prior_status["prior_external_conflict"]:
        return (
            "blocked_duplicate_or_current_registry_conflict",
            "exact_current702_or_prior_external_accession_or_sequence_overlap",
            "blocked",
            "Do not import; preserve as current/prior external duplicate-conflict evidence.",
        )
    if lane.get("lane_group") == "adjacent_cofactor_confounded_negative":
        return (
            "reject/OOS_preserve_signal",
            "adjacent_cofactor_confounded_negative_control",
            "medium",
            "Preserve as adjacent cofactor-confounded negative; do not promote from this shard.",
        )
    raw_state = row.get("terminal_state")
    if raw_state == "external_countable_preflight_candidate":
        if row.get("coordinate_source") == "PDB" and flags[
            "direct_uniprot_rhea_provenance_present"
        ]:
            return (
                "import_ready_preview",
                "reviewed_exact_locator_experimental_coordinate_direct_rhea_preflight_clear",
                "high",
                "Stage in import-ready preview only; run source-free structural duplicate and label-factory gates before any production import.",
            )
        return (
            "provisional_external_countable_preflight_candidate",
            "reviewed_exact_locator_coordinate_and_reaction_preflight_clear_but_materialization_not_final",
            "high",
            "Stage only as provisional preview; materialize/review source-free locators before any import-ready claim.",
        )
    if raw_state == "locator_repair_candidate":
        return (
            "repairable_locator_blocker",
            "only_range_or_ambiguous_residue_features_available",
            "medium",
            "Repair range or ambiguous locators to exact residue positions before preflight.",
        )
    if raw_state == "coordinate_repair_candidate":
        return (
            "repairable_coordinate_blocker",
            "curated_residue_locator_present_but_coordinate_provenance_missing",
            "medium",
            "Find AFDB/PDB or alternate coordinate provenance for the exact locators.",
        )
    if raw_state in TERMINAL_STATES:
        return (
            str(raw_state),
            str(row.get("terminal_route_basis") or raw_state),
            str(row.get("confidence_tier") or "low"),
            str(row.get("exact_next_action") or "Preserve for review."),
        )
    return (
        "review_only_evidence",
        str(row.get("terminal_route_basis") or "unmapped_external_source_state"),
        "low",
        "Preserve evidence for review; fill the smallest missing locator, coordinate, or reaction gap.",
    )


def _decorate_candidate(
    *,
    row: dict[str, Any],
    search_record: dict[str, Any],
    lane: dict[str, str],
    prior_status: dict[str, Any],
) -> dict[str, Any]:
    flags = _cofactor_flags(row, search_record)
    axes = _mechanism_axes(lane, flags)
    terminal_state, route_basis, confidence, next_action = _route_terminal_state(
        row=row,
        lane=lane,
        prior_status=prior_status,
        flags=flags,
    )
    row = dict(row)
    row.update(
        {
            "target_family_lane": lane["target_family_lane"],
            "lane_id": lane["lane_id"],
            "lane_group": lane["lane_group"],
            "mechanism_axis_focus": lane["mechanism_axis_focus"],
            "mechanism_axis_coverage": axes,
            "cofactor_family_flags": flags,
            "prior_external_conflict": prior_status,
            "terminal_state": terminal_state,
            "terminal_route_basis": route_basis,
            "confidence_tier": confidence,
            "exact_next_action": next_action,
            "duplicate_status_summary": {
                "current702_status": row[
                    "duplicate_current_registry_conflict_status"
                ],
                "prior_external_status": prior_status[
                    "prior_external_conflict_status"
                ],
                "blocked_by_duplicate_or_current_registry_conflict": (
                    terminal_state == "blocked_duplicate_or_current_registry_conflict"
                ),
            },
            "materialization_status": _materialization_status(terminal_state),
        }
    )
    row["source_hashes"] = {
        **row.get("source_hashes", {}),
        "lane_query_sha256": _canonical_sha256(lane["query"]),
        "external_prior_conflict_sha256": _canonical_sha256(prior_status),
    }
    return row


def _materialization_status(terminal_state: str) -> dict[str, Any]:
    if terminal_state == "import_ready_preview":
        return {
            "materialization_bucket": "import_ready_preview",
            "blockers": [
                "production_registry_change_authorization",
                "final_label_factory_acceptance_required",
            ],
        }
    if terminal_state == "provisional_external_countable_preflight_candidate":
        return {
            "materialization_bucket": "provisional_preflight",
            "blockers": ["source_free_locator_materialization_or_admission_gate_not_run"],
        }
    if terminal_state == "repairable_locator_blocker":
        return {
            "materialization_bucket": "locator_repair",
            "blockers": ["exact_locator_repair_required"],
        }
    if terminal_state == "repairable_coordinate_blocker":
        return {
            "materialization_bucket": "coordinate_repair",
            "blockers": ["coordinate_provenance_repair_required"],
        }
    if terminal_state == "blocked_duplicate_or_current_registry_conflict":
        return {
            "materialization_bucket": "duplicate_conflict",
            "blockers": ["exact_current702_or_prior_external_conflict"],
        }
    return {"materialization_bucket": terminal_state, "blockers": []}


def build_external_scaleout_shard_plp_radical_cobalamin(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    prior_external_payloads: list[tuple[str, dict[str, Any]]] | None = None,
    created_utc: str | None = None,
    max_records_per_query: int = 100,
    max_pages_per_query: int = 5,
    max_candidates: int = 1800,
    max_candidates_per_lane: int | None = None,
    target_candidate_floor: int = 1500,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    query_fetcher: Callable[[str, int, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    entry_fetch_workers: int = 16,
) -> dict[str, Any]:
    if max_records_per_query < 1 or max_records_per_query > 500:
        raise ValueError("max_records_per_query must be between 1 and 500")
    if max_pages_per_query < 1 or max_pages_per_query > 20:
        raise ValueError("max_pages_per_query must be between 1 and 20")
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    if max_candidates_per_lane is not None and max_candidates_per_lane < 1:
        raise ValueError("max_candidates_per_lane must be positive when set")
    if entry_fetch_workers < 1 or entry_fetch_workers > 32:
        raise ValueError("entry_fetch_workers must be between 1 and 32")

    created = created_utc or _utc_now_iso()
    current_index = _current_reference_index(
        current_manifest_payload, label_registry_payload
    )
    prior_index = _prior_external_index(prior_external_payloads or [])
    lane_candidate_cap = max_candidates_per_lane or max(
        1, max_candidates // max(1, len(lane_queries))
    )
    rows: list[dict[str, Any]] = []
    lane_summaries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = []
    seen_accessions: set[str] = set()
    seen_sequence_shas: set[str] = set()
    total_fetched_records = 0

    for lane in lane_queries:
        if len(rows) >= max_candidates:
            break
        try:
            search_payload = query_fetcher(
                lane["query"], max_records_per_query, max_pages_per_query
            )
        except Exception as exc:  # pragma: no cover - live source failure path
            fetch_failures.append(
                {
                    "lane_id": lane["lane_id"],
                    "source": "uniprot_search",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            lane_summaries.append(_failed_lane_summary(lane))
            continue

        metadata = search_payload.get("metadata", {}) or {}
        search_records: list[dict[str, Any]] = []
        for record in search_payload.get("records", []) or []:
            if not isinstance(record, dict):
                continue
            total_fetched_records += 1
            accession = _clean_accession(record.get("accession"))
            sequence_sha = _sequence_sha256(record.get("sequence"))
            if not accession or accession in seen_accessions:
                continue
            if sequence_sha and sequence_sha in seen_sequence_shas:
                continue
            seen_accessions.add(accession)
            if sequence_sha:
                seen_sequence_shas.add(sequence_sha)
            search_records.append(record)
            if len(search_records) >= lane_candidate_cap:
                break
            if len(rows) + len(search_records) >= max_candidates:
                break

        def fetch_entry(record: dict[str, Any]) -> tuple[dict[str, Any], Any, Exception | None]:
            accession = _clean_accession(record.get("accession"))
            try:
                return record, entry_fetcher(accession), None
            except Exception as exc:  # pragma: no cover - live source failure path
                return record, None, exc

        with ThreadPoolExecutor(max_workers=entry_fetch_workers) as executor:
            entry_payloads = list(executor.map(fetch_entry, search_records))

        lane_unique_count = 0
        for search_record, entry_payload, entry_error in entry_payloads:
            accession = _clean_accession(search_record.get("accession"))
            if entry_error is not None:
                fetch_failures.append(
                    {
                        "lane_id": lane["lane_id"],
                        "accession": accession,
                        "source": "uniprot_entry",
                        "error_type": type(entry_error).__name__,
                        "error": str(entry_error),
                    }
                )
                continue
            entry_record = (
                entry_payload.get("record", entry_payload)
                if isinstance(entry_payload, dict)
                else None
            )
            if not isinstance(entry_record, dict):
                fetch_failures.append(
                    {
                        "lane_id": lane["lane_id"],
                        "accession": accession,
                        "source": "uniprot_entry",
                        "error_type": "InvalidPayload",
                        "error": "entry fetcher did not return a record dictionary",
                    }
                )
                continue
            row, rhea_failures = _candidate_row(
                lane=lane,
                search_record=search_record,
                entry_record=entry_record,
                current_index=current_index,
                source_query_timestamp_utc=created,
                search_metadata=metadata,
                fetch_rhea_fallback=False,
                rhea_fetcher=lambda _ec, _limit: {"records": []},
                max_reactions_per_ec=1,
            )
            prior_status = _dedupe_status(
                accession=accession,
                sequence_sha=_sequence_sha256(search_record.get("sequence")),
                prior_index=prior_index,
            )
            rows.append(
                _decorate_candidate(
                    row=row,
                    search_record=search_record,
                    lane=lane,
                    prior_status=prior_status,
                )
            )
            fetch_failures.extend(rhea_failures)
            lane_unique_count += 1

        pages = metadata.get("pages", []) or []
        lane_summaries.append(
            {
                "lane_id": lane["lane_id"],
                "target_family_lane": lane["target_family_lane"],
                "lane_group": lane["lane_group"],
                "mechanism_axis_focus": lane["mechanism_axis_focus"],
                "query": lane["query"],
                "fetched_record_count": metadata.get("record_count", len(search_records)),
                "unique_candidate_count": lane_unique_count,
                "pages_fetched": metadata.get("pages_fetched", len(pages) or 1),
                "page_urls": [page.get("url") for page in pages if isinstance(page, dict)],
                "status": "query_fetched",
            }
        )

    rows.sort(key=lambda row: (row["lane_id"], row["accession"]))
    terminal_counts = Counter(row["terminal_state"] for row in rows)
    lane_counts: dict[str, Counter[str]] = defaultdict(Counter)
    axis_counts: Counter[str] = Counter()
    materialization_counts: Counter[str] = Counter()
    duplicate_conflict_count = 0
    current_conflict_count = 0
    prior_conflict_count = 0
    for row in rows:
        lane_counts[row["target_family_lane"]][row["terminal_state"]] += 1
        axis_counts.update(row.get("mechanism_axis_coverage", []))
        materialization_counts.update([row["materialization_status"]["materialization_bucket"]])
        if row["terminal_state"] == "blocked_duplicate_or_current_registry_conflict":
            duplicate_conflict_count += 1
        if row["duplicate_current_registry_conflict"]["duplicate_or_current_registry_conflict"]:
            current_conflict_count += 1
        if row["prior_external_conflict"]["prior_external_conflict"]:
            prior_conflict_count += 1

    validation_checks = {
        "candidate_ids_unique": len({row["candidate_id"] for row in rows}) == len(rows),
        "candidate_count_matches_rows": len(rows) == sum(terminal_counts.values()),
        "all_terminal_states_known": all(
            row["terminal_state"] in TERMINAL_STATES for row in rows
        ),
        "all_rows_have_source_hashes": all(row.get("source_hashes") for row in rows),
        "all_rows_have_next_action": all(row.get("exact_next_action") for row in rows),
        "target_candidate_floor_met": len(rows) >= target_candidate_floor,
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
            "primary_sources": [
                "UniProtKB/Swiss-Prot reviewed entries",
                "UniProt feature and catalytic activity records",
                "AlphaFoldDB/PDB coordinate provenance",
                "Rhea/EC provenance when present in UniProt catalytic activity",
            ],
            "dedupe_scope": [
                "current702 accession and sequence SHA",
                "prior local external artifacts",
                "completed external admission branch artifacts loaded by git show",
            ],
            "excluded_actions": [
                "production registry import",
                "ontology edit",
                "split or threshold change",
                "model weight change",
                "coordinate download",
            ],
        },
        "family_selection_rationale": (
            "PLP, radical-SAM, and cobalamin/B12 families stress proton-transfer, "
            "electron-transfer, radical, and cofactor-context axes that shallow "
            "geometry or representation-only approaches miss; adjacent SAM, "
            "non-PLP decarboxylase, methylcobalamin, and Schiff-base controls "
            "preserve cofactor-confounded negatives."
        ),
        "candidate_count": len(rows),
        "target_candidate_floor": target_candidate_floor,
        "target_candidate_floor_met": len(rows) >= target_candidate_floor,
        "stretch_target_candidate_count": 3000,
        "import_ready_count": terminal_counts.get("import_ready_preview", 0),
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "family_lane_terminal_state_counts": {
            lane: dict(sorted(counts.items())) for lane, counts in sorted(lane_counts.items())
        },
        "mechanism_axis_counts": dict(sorted(axis_counts.items())),
        "materialization_bucket_counts": dict(sorted(materialization_counts.items())),
        "duplicate_conflict_counts": {
            "blocked_duplicate_or_current_registry_conflict": duplicate_conflict_count,
            "current702_exact_conflicts": current_conflict_count,
            "prior_external_exact_conflicts": prior_conflict_count,
        },
        "prior_external_index": {
            "source_artifact_count": prior_index["source_artifact_count"],
            "indexed_row_count": prior_index["indexed_row_count"],
        },
        "current_reference_index": {
            "current_reference_accession_count": current_index[
                "current_reference_accession_count"
            ],
            "current_sequence_sha_count": current_index["current_sequence_sha_count"],
            "external_label_accessions": current_index["external_label_accessions"],
        },
        "api_query_limits": {
            "max_records_per_query": max_records_per_query,
            "max_pages_per_query": max_pages_per_query,
            "max_candidates": max_candidates,
            "max_candidates_per_lane": lane_candidate_cap,
            "entry_fetch_workers": entry_fetch_workers,
            "coordinate_downloads_performed": False,
            "rhea_fallback_performed": False,
        },
        "lane_summaries": lane_summaries,
        "total_fetched_records": total_fetched_records,
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
            "coordinate_downloads_performed": False,
        },
    }


def _failed_lane_summary(lane: dict[str, str]) -> dict[str, Any]:
    return {
        "lane_id": lane["lane_id"],
        "target_family_lane": lane["target_family_lane"],
        "lane_group": lane["lane_group"],
        "mechanism_axis_focus": lane["mechanism_axis_focus"],
        "query": lane["query"],
        "fetched_record_count": 0,
        "unique_candidate_count": 0,
        "pages_fetched": 0,
        "page_urls": [],
        "status": "query_fetch_failed",
    }


def build_external_scaleout_import_ready_preview(
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
            "lane_id": row["lane_id"],
            "terminal_state": row["terminal_state"],
            "confidence_tier": row["confidence_tier"],
            "protein_name": row["protein_name"],
            "organism": row["organism"],
            "sequence_length": row["sequence_length"],
            "residue_locators": row["residue_locators"],
            "coordinate_source_status": row["coordinate_source_status"],
            "afdb_or_pdb_identifier": row["afdb_or_pdb_identifier"],
            "rhea_ec_provenance": row["rhea_ec_provenance"],
            "cofactor_family_flags": row["cofactor_family_flags"],
            "mechanism_axis_coverage": row["mechanism_axis_coverage"],
            "duplicate_status_summary": row["duplicate_status_summary"],
            "source_hashes": row["source_hashes"],
            "ready_for_production_label_import": False,
            "remaining_required_before_import": [
                "source_free_structural_duplicate_screen",
                "label_factory_gate_and_explicit_review_decision",
                "production_registry_change_authorization",
            ],
            "exact_next_action": row["exact_next_action"],
        }
        for row in artifact.get("rows", [])
        if row.get("terminal_state") == "import_ready_preview"
    ]
    return {
        "artifact_id": IMPORT_READY_ARTIFACT_ID,
        "schema_version": IMPORT_READY_SCHEMA_VERSION,
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


def render_external_scaleout_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# External Scaleout Shard - PLP/Radical/Cobalamin current702",
        "",
        artifact["family_selection_rationale"],
        "",
        "## Summary",
        "",
        f"- Candidate rows: {artifact['candidate_count']}",
        f"- Target floor met: {artifact['target_candidate_floor_met']}",
        f"- Import-ready preview rows: {artifact['import_ready_count']}",
        f"- Duplicate/current conflicts: {artifact['duplicate_conflict_counts']['blocked_duplicate_or_current_registry_conflict']}",
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

    lines.extend(["", "## Mechanism-Axis Coverage", "", "| axis | count |", "| --- | ---: |"])
    for axis, count in artifact["mechanism_axis_counts"].items():
        lines.append(f"| `{axis}` | {count} |")

    states = sorted(artifact["terminal_state_counts"])
    lines.extend(
        [
            "",
            "## Family/Lane Counts",
            "",
            "| family/lane | " + " | ".join(states) + " |",
            "| --- | " + " | ".join("---:" for _ in states) + " |",
        ]
    )
    for family, counts in artifact["family_lane_terminal_state_counts"].items():
        values = [str(counts.get(state, 0)) for state in states]
        lines.append(f"| {family} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## Materialization Blockers",
            "",
            "| bucket | count |",
            "| --- | ---: |",
        ]
    )
    for bucket, count in artifact["materialization_bucket_counts"].items():
        lines.append(f"| `{bucket}` | {count} |")

    failure_counts = Counter(
        (failure.get("source"), failure.get("error_type"))
        for failure in artifact.get("fetch_failures", [])
        if isinstance(failure, dict)
    )
    lines.extend(
        [
            "",
            "## Source Retrieval",
            "",
            f"- Total fetched search records before row materialization: {artifact['total_fetched_records']}",
            f"- UniProt/Rhea fallback performed: {artifact['api_query_limits']['rhea_fallback_performed']}",
            f"- Coordinate downloads performed: {artifact['api_query_limits']['coordinate_downloads_performed']}",
            "",
            "| source | error type | count |",
            "| --- | --- | ---: |",
        ]
    )
    if failure_counts:
        for (source, error_type), count in sorted(failure_counts.items()):
            lines.append(f"| `{source}` | `{error_type}` | {count} |")
    else:
        lines.append("| none | none | 0 |")

    lines.extend(
        [
            "",
            "## Source Queries",
            "",
            "| lane | group | unique candidates | pages | query |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for lane in artifact["lane_summaries"]:
        query = str(lane.get("query") or "").replace("|", "\\|")
        lines.append(
            f"| {lane['target_family_lane']} | `{lane['lane_group']}` | "
            f"{lane['unique_candidate_count']} | {lane['pages_fetched']} | `{query}` |"
        )

    lines.extend(
        [
            "",
            "## Next Mechanical Continuation",
            "",
            "Continue this lane by increasing `--max-pages-per-query` before raising "
            "`--max-records-per-query`; prioritize non-duplicate import-ready and "
            "provisional rows for source-free structural duplicate screens, then "
            "repair locator/coordinate blockers. Do not import directly from this shard.",
        ]
    )
    return "\n".join(lines) + "\n"


def _load_prior_external_payloads(
    *,
    prior_external_paths: tuple[Path, ...],
    prior_external_branch_specs: tuple[str, ...],
) -> tuple[list[tuple[str, dict[str, Any]]], dict[str, Any]]:
    payloads: list[tuple[str, dict[str, Any]]] = []
    source_records: dict[str, Any] = {}
    for path in prior_external_paths:
        if not path.exists():
            continue
        payloads.append((str(path), _read_json(path)))
        source_records[str(path)] = _source_record(path)
    for spec in prior_external_branch_specs:
        payload, source_record = _git_json_spec_payload(spec)
        source_records[spec] = source_record
        if payload is not None:
            payloads.append((spec, payload))
    return payloads, source_records


def write_external_scaleout_shard_plp_radical_cobalamin(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    prior_external_paths: tuple[Path, ...] = DEFAULT_PRIOR_EXTERNAL_ARTIFACT_PATHS,
    prior_external_branch_specs: tuple[str, ...] = DEFAULT_PRIOR_EXTERNAL_BRANCH_SPECS,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    import_ready_path: Path | None = DEFAULT_IMPORT_READY_PATH,
    created_utc: str | None = None,
    max_records_per_query: int = 100,
    max_pages_per_query: int = 5,
    max_candidates: int = 1800,
    max_candidates_per_lane: int | None = None,
    target_candidate_floor: int = 1500,
    entry_fetch_workers: int = 16,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    query_fetcher: Callable[[str, int, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
) -> dict[str, Any]:
    prior_payloads, prior_source_records = _load_prior_external_payloads(
        prior_external_paths=prior_external_paths,
        prior_external_branch_specs=prior_external_branch_specs,
    )
    artifact = build_external_scaleout_shard_plp_radical_cobalamin(
        current_manifest_payload=_read_json(current_manifest_path),
        label_registry_payload=_read_json(label_registry_path),
        prior_external_payloads=prior_payloads,
        created_utc=created_utc,
        max_records_per_query=max_records_per_query,
        max_pages_per_query=max_pages_per_query,
        max_candidates=max_candidates,
        max_candidates_per_lane=max_candidates_per_lane,
        target_candidate_floor=target_candidate_floor,
        lane_queries=lane_queries,
        query_fetcher=query_fetcher,
        entry_fetcher=entry_fetcher,
        entry_fetch_workers=entry_fetch_workers,
    )
    artifact["source_artifacts"] = {
        "current_manifest": _source_record(current_manifest_path),
        "label_registry": _source_record(label_registry_path),
        "prior_external_artifacts": prior_source_records,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_external_scaleout_report(artifact), encoding="utf-8")
    if import_ready_path is not None and artifact["import_ready_count"] > 0:
        preview = build_external_scaleout_import_ready_preview(artifact)
        preview["source_artifacts"] = {
            "external_scaleout_shard": _source_record(out_path)
        }
        import_ready_path.parent.mkdir(parents=True, exist_ok=True)
        import_ready_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True), encoding="utf-8"
        )
    return artifact
