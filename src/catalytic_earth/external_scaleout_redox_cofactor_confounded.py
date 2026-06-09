from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

from .adapters import (
    USER_AGENT,
    build_uniprot_entry_url,
    fetch_rhea_by_ec,
    fetch_uniprot_query,
    normalize_uniprot_entry_json,
)
from .external_source_ingestion import (
    _candidate_row,
    _canonical_sha256,
    _clean_accession,
    _current_reference_index,
    _read_json,
    _sequence_sha256,
    _source_record,
    _utc_now_iso,
)


ARTIFACT_ID = (
    "v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609"
)
IMPORT_READY_PREVIEW_ARTIFACT_ID = (
    "v3_external_scaleout_shard_redox_cofactor_confounded_"
    "import_ready_preview_current702_20260609"
)
SCHEMA_VERSION = "v3.external_scaleout_shard_redox_cofactor_confounded"
IMPORT_READY_PREVIEW_SCHEMA_VERSION = (
    "v3.external_scaleout_shard_redox_cofactor_confounded_import_ready_preview"
)

DEFAULT_OUT_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609.json"
)
DEFAULT_IMPORT_READY_PREVIEW_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_redox_cofactor_confounded_"
    "import_ready_preview_current702_20260609.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/external_scaleout_shard_redox_cofactor_confounded_current702_20260609.md"
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
    "locator_repair_candidate",
    "coordinate_repair_candidate",
    "blocked_duplicate_or_current_registry_conflict",
    "reject/OOS_preserve_signal",
    "hard_blocked_with_next_action",
)

DEFAULT_PRIOR_ARTIFACT_GLOBS = (
    "artifacts/v3_external*.json",
    "artifacts/v3_scaleout*.json",
)

DEFAULT_PRIOR_GIT_ARTIFACTS = (
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
        "origin/ce-external-admission-qa-merger-20260609:"
        "artifacts/v3_external_admission_merged_surface_current702_20260609.json"
    ),
    (
        "origin/ce-external-admission-qa-merger-20260609:"
        "artifacts/v3_external_admission_import_ready_preview_current702_20260609.json"
    ),
    (
        "origin/ce-external-admission-qa-merger-20260609:"
        "artifacts/v3_external_admission_repair_queue_current702_20260609.json"
    ),
)

DEFAULT_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "oxygenase_ec114_monooxygenase",
        "target_family_lane": "redox oxygen/sulfur",
        "boundary_class": "oxygenase",
        "boundary_role": "source_candidate",
        "query": "(reviewed:true) AND ((ec:1.14.*) OR (protein_name:monooxygenase))",
    },
    {
        "lane_id": "oxygenase_ec113_dioxygenase",
        "target_family_lane": "redox oxygen/sulfur",
        "boundary_class": "oxygenase",
        "boundary_role": "source_candidate",
        "query": "(reviewed:true) AND ((ec:1.13.*) OR (protein_name:dioxygenase))",
    },
    {
        "lane_id": "sulfur_oxidoreductase_ec18",
        "target_family_lane": "sulfur oxidoreductase",
        "boundary_class": "redox_oxygen_sulfur",
        "boundary_role": "source_candidate",
        "query": (
            "(reviewed:true) AND ((ec:1.8.*) OR (protein_name:sulfite) OR "
            "(protein_name:sulfur) OR (protein_name:thiosulfate))"
        ),
    },
    {
        "lane_id": "heme_peroxidase_ec1111",
        "target_family_lane": "heme peroxidase/oxidase-like",
        "boundary_class": "heme_peroxidase_oxidase_like",
        "boundary_role": "source_candidate",
        "query": "(reviewed:true) AND ((ec:1.11.1.*) OR (protein_name:peroxidase))",
    },
    {
        "lane_id": "heme_cytochrome_oxidase_like",
        "target_family_lane": "heme peroxidase/oxidase-like",
        "boundary_class": "heme_peroxidase_oxidase_like",
        "boundary_role": "boundary_review",
        "query": (
            "(reviewed:true) AND ((protein_name:cytochrome) OR "
            "(cc_cofactor:heme) OR (keyword:Heme))"
        ),
    },
    {
        "lane_id": "flavin_broad_redox",
        "target_family_lane": "flavin redox boundary",
        "boundary_class": "flavin_monooxygenase_dehydrogenase_boundary",
        "boundary_role": "boundary_review",
        "query": (
            "(reviewed:true) AND ((protein_name:flavin) OR "
            "(keyword:Flavoprotein) OR (cc_cofactor:FAD) OR (cc_cofactor:FMN))"
        ),
    },
    {
        "lane_id": "flavin_monooxygenase_oxygen_transfer",
        "target_family_lane": "flavin monooxygenase",
        "boundary_class": "flavin_monooxygenase_dehydrogenase_boundary",
        "boundary_role": "source_candidate",
        "query": (
            "(reviewed:true) AND ((protein_name:monooxygenase) AND "
            "((cc_cofactor:FAD) OR (cc_cofactor:FMN) OR (keyword:Flavoprotein)))"
        ),
    },
    {
        "lane_id": "flavin_dehydrogenase_reductase_oos",
        "target_family_lane": "flavin dehydrogenase/reductase boundary",
        "boundary_class": "flavin_monooxygenase_dehydrogenase_boundary",
        "boundary_role": "cofactor_confounded_oos_negative",
        "query": (
            "(reviewed:true) AND (((protein_name:dehydrogenase) OR "
            "(protein_name:reductase)) AND ((cc_cofactor:FAD) OR "
            "(cc_cofactor:FMN) OR (keyword:Flavoprotein)))"
        ),
    },
    {
        "lane_id": "fe_s_flavin_combined_systems",
        "target_family_lane": "Fe-S/flavin combined systems",
        "boundary_class": "fe_s_flavin_combined_system",
        "boundary_role": "boundary_review",
        "query": (
            '(reviewed:true) AND (((keyword:"Iron-sulfur") OR '
            "(protein_name:ferredoxin)) AND ((cc_cofactor:FAD) OR "
            "(cc_cofactor:FMN) OR (protein_name:flavoprotein)))"
        ),
    },
    {
        "lane_id": "dehydrogenase_reductase_oos_broad",
        "target_family_lane": "dehydrogenase/reductase OOS boundary",
        "boundary_class": "dehydrogenase_reductase_boundary",
        "boundary_role": "cofactor_confounded_oos_negative",
        "query": (
            "(reviewed:true) AND ((ec:1.3.*) OR (ec:1.5.*) OR "
            "(ec:1.6.*) OR (protein_name:dehydrogenase) OR "
            "(protein_name:reductase))"
        ),
    },
    {
        "lane_id": "oxidase_like_boundary",
        "target_family_lane": "heme peroxidase/oxidase-like",
        "boundary_class": "heme_peroxidase_oxidase_like",
        "boundary_role": "boundary_review",
        "query": "(reviewed:true) AND ((protein_name:oxidase) OR (ec:1.1.3.*) OR (ec:1.2.3.*))",
    },
    {
        "lane_id": "nitrogen_redox_oxygen_sulfur_boundary",
        "target_family_lane": "redox oxygen/sulfur",
        "boundary_class": "redox_oxygen_sulfur",
        "boundary_role": "boundary_review",
        "query": "(reviewed:true) AND ((ec:1.7.*) OR (protein_name:nitrite) OR (protein_name:nitrate))",
    },
    {
        "lane_id": "misc_oxidoreductase_boundary",
        "target_family_lane": "redox oxygen/sulfur",
        "boundary_class": "redox_oxygen_sulfur",
        "boundary_role": "boundary_review",
        "query": "(reviewed:true) AND ((ec:1.10.*) OR (ec:1.15.*) OR (ec:1.17.*) OR (ec:1.18.*) OR (ec:1.19.*))",
    },
    {
        "lane_id": "iron_sulfur_broad_boundary",
        "target_family_lane": "Fe-S/flavin combined systems",
        "boundary_class": "fe_s_flavin_combined_system",
        "boundary_role": "boundary_review",
        "query": (
            '(reviewed:true) AND ((keyword:"Iron-sulfur") OR '
            "(protein_name:ferredoxin) OR (protein_name:hydrogenase))"
        ),
    },
)


def fetch_uniprot_entry_with_timeout(
    accession: str, *, timeout_seconds: int = 8
) -> dict[str, Any]:
    url = build_uniprot_entry_url(accession)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    return {
        "metadata": {
            "source": "uniprotkb_json",
            "url": url,
            "record_count": 1,
            "timeout_seconds": timeout_seconds,
        },
        "record": normalize_uniprot_entry_json(payload),
    }


def _iter_candidate_records(payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        return rows
    for key in ("rows", "candidate_rows", "canonical_records"):
        value = payload.get(key)
        if isinstance(value, list):
            rows.extend(item for item in value if isinstance(item, dict))
    partitions = payload.get("terminal_state_partitions")
    if isinstance(partitions, dict):
        for value in partitions.values():
            if isinstance(value, list):
                rows.extend(item for item in value if isinstance(item, dict))
    return rows


def _row_accession(row: dict[str, Any]) -> str | None:
    for key in ("accession", "primary_accession"):
        cleaned = _clean_accession(row.get(key))
        if cleaned:
            return cleaned
    for key in ("candidate_id", "entry_id", "row_id", "stable_candidate_key"):
        value = str(row.get(key) or "")
        if "uniprot:" in value:
            return _clean_accession(value.split("uniprot:", 1)[1].split(":", 1)[0])
    return None


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


def _row_candidate_id(row: dict[str, Any]) -> str:
    for key in ("candidate_id", "entry_id", "row_id", "stable_candidate_key"):
        value = row.get(key)
        if value:
            return str(value)
    accession = _row_accession(row)
    return f"uniprot:{accession}" if accession else "unknown_candidate"


def _prior_index_from_payloads(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    accessions: dict[str, list[str]] = defaultdict(list)
    sequence_shas: dict[str, list[str]] = defaultdict(list)
    artifact_ids: list[str] = []
    row_count = 0
    for payload in payloads:
        artifact_id = str(payload.get("artifact_id") or "unknown_artifact")
        artifact_ids.append(artifact_id)
        for row in _iter_candidate_records(payload):
            row_count += 1
            candidate_ref = f"{artifact_id}:{_row_candidate_id(row)}"
            accession = _row_accession(row)
            if accession:
                accessions[accession].append(candidate_ref)
            sequence_sha = _row_sequence_sha(row)
            if sequence_sha:
                sequence_shas[sequence_sha].append(candidate_ref)
    return {
        "accession_to_prior_candidates": {
            key: sorted(set(value)) for key, value in accessions.items()
        },
        "sequence_sha_to_prior_candidates": {
            key: sorted(set(value)) for key, value in sequence_shas.items()
        },
        "prior_artifact_ids": sorted(set(artifact_ids)),
        "prior_artifact_count": len(set(artifact_ids)),
        "prior_candidate_row_count": row_count,
    }


def _prior_duplicate_status(
    *,
    accession: str,
    sequence_sha: str | None,
    prior_index: dict[str, Any],
) -> dict[str, Any]:
    accession_matches = prior_index["accession_to_prior_candidates"].get(accession, [])
    sequence_matches = (
        prior_index["sequence_sha_to_prior_candidates"].get(sequence_sha, [])
        if sequence_sha
        else []
    )
    if accession_matches:
        status = "exact_prior_external_artifact_or_branch_accession_overlap"
    elif sequence_matches:
        status = "exact_prior_external_artifact_or_branch_sequence_sha_overlap"
    else:
        status = "no_exact_prior_external_artifact_or_branch_overlap"
    return {
        "prior_external_conflict_status": status,
        "duplicate_or_prior_external_conflict": bool(accession_matches or sequence_matches),
        "exact_accession_matched_prior_external_candidate_ids": accession_matches,
        "exact_sequence_matched_prior_external_candidate_ids": sequence_matches,
    }


def _cofactor_terms(row: dict[str, Any]) -> list[str]:
    text_parts: list[str] = []
    for cofactor in row.get("cofactor_provenance", []) or []:
        if isinstance(cofactor, dict):
            text_parts.extend(
                str(cofactor.get(key) or "")
                for key in ("name", "cross_reference")
            )
    for feature in row.get("source_evidence_features", []) or []:
        if isinstance(feature, dict):
            text_parts.extend(
                str(feature.get(key) or "")
                for key in ("description", "ligand_name", "ligand_id", "ligand_note")
            )
    text = " ".join(text_parts).lower()
    groups: set[str] = set()
    if any(token in text for token in ("fad", "fmn", "flavin")):
        groups.add("flavin")
    if any(token in text for token in ("heme", "haem", "porphyrin")):
        groups.add("heme")
    if any(token in text for token in ("iron-sulfur", "fe-s", "4fe", "2fe", "sf4", "fes")):
        groups.add("iron_sulfur")
    if any(token in text for token in ("nad", "nadp", "nicotinamide")):
        groups.add("nad_or_nadp")
    if any(token in text for token in ("sulfur", "sulfide", "sulfite", "thiosulfate")):
        groups.add("sulfur")
    if any(token in text for token in ("oxygen", "peroxide", "dioxygen")):
        groups.add("oxygen_peroxide")
    if "molybd" in text:
        groups.add("molybdopterin")
    return sorted(groups)


def _materialization_bucket(row: dict[str, Any]) -> str:
    state = row["terminal_state"]
    if state == "import_ready_preview":
        return "source_preflight_import_ready_preview"
    if state == "provisional_external_countable_preflight_candidate":
        return "source_preflight_provisional"
    if state == "locator_ready_candidate":
        return "reaction_or_family_review_pending"
    if state in {"coordinate_ready_pending_locator", "locator_repair_candidate"}:
        return "repairable_locator_blocker"
    if state == "coordinate_repair_candidate":
        return "repairable_coordinate_blocker"
    if state == "hard_blocked_with_next_action":
        return "hard_materialization_or_source_blocker"
    if state == "blocked_duplicate_or_current_registry_conflict":
        return "duplicate_or_current_conflict"
    return "reject_oos_or_confounded_signal"


def _apply_redox_shard_policy(
    row: dict[str, Any],
    *,
    lane: dict[str, str],
    prior_duplicate: dict[str, Any],
) -> dict[str, Any]:
    candidate = json.loads(json.dumps(row))
    candidate["stable_candidate_key"] = (
        "external_scaleout_redox_cofactor_confounded:"
        f"uniprot:{candidate['accession']}"
    )
    candidate["boundary_class"] = lane["boundary_class"]
    candidate["boundary_role"] = lane["boundary_role"]
    candidate["terminal_state_original_from_source_route"] = candidate["terminal_state"]
    candidate["prior_external_duplicate_conflict"] = prior_duplicate
    duplicate_record = candidate.setdefault("duplicate_current_registry_conflict", {})
    duplicate_record["prior_external_conflict"] = prior_duplicate

    prior_conflict = prior_duplicate["duplicate_or_prior_external_conflict"]
    current_conflict = bool(duplicate_record.get("duplicate_or_current_registry_conflict"))
    if prior_conflict and not current_conflict:
        candidate["terminal_state"] = "blocked_duplicate_or_current_registry_conflict"
        candidate["terminal_route_basis"] = (
            "exact_prior_external_artifact_or_branch_accession_or_sequence_overlap"
        )
        candidate["confidence_tier"] = "blocked"
        candidate["exact_next_action"] = (
            "Do not import; preserve as duplicate/current conflict against prior "
            "external admission or scaleout artifacts."
        )
        blocker = candidate.setdefault("blocker_basis", {})
        blocker["applicable"] = True
        blocker["terminal_route_basis"] = candidate["terminal_route_basis"]
        blocker["duplicate_or_prior_external_conflict"] = True
        blocker.setdefault("missing_preflight_requirements", [])
        if (
            "no_prior_external_artifact_or_branch_accession_or_sequence_conflict"
            not in blocker["missing_preflight_requirements"]
        ):
            blocker["missing_preflight_requirements"].append(
                "no_prior_external_artifact_or_branch_accession_or_sequence_conflict"
            )
    elif lane["boundary_role"] == "cofactor_confounded_oos_negative":
        candidate["terminal_state"] = "reject/OOS_preserve_signal"
        candidate["terminal_route_basis"] = (
            "cofactor_confounded_dehydrogenase_reductase_boundary_negative"
        )
        candidate["confidence_tier"] = "oos_confounded_signal"
        candidate["exact_next_action"] = (
            "Preserve as cofactor-confounded OOS/boundary negative; do not count "
            "as oxygen-transfer import evidence without explicit human reversal."
        )
        candidate.setdefault("blocker_basis", {})["applicable"] = True
    elif candidate["terminal_state"] == "external_countable_preflight_candidate":
        candidate["terminal_state"] = "import_ready_preview"
        candidate["terminal_route_basis"] = (
            "reviewed_exact_locator_coordinate_rhea_or_specific_ec_and_no_current_or_prior_duplicate"
        )
        candidate["exact_next_action"] = (
            "Stage in import-ready preview only; still requires current-countable "
            "structural duplicate screening, label-factory review, and explicit "
            "production authorization before any import."
        )
    elif candidate["terminal_state"] == "review_only_evidence":
        candidate["terminal_state"] = "hard_blocked_with_next_action"
        candidate["terminal_route_basis"] = (
            "reviewed_external_evidence_present_but_no_existing_terminal_gate_passed"
        )
        candidate["exact_next_action"] = (
            "Keep as hard-blocked review evidence until the missing locator, "
            "coordinate, reaction, or family-decision gate is repaired."
        )

    cofactor_groups = _cofactor_terms(candidate)
    candidate["cofactor_confounded_signal"] = bool(
        lane["boundary_role"] == "cofactor_confounded_oos_negative"
        or len(cofactor_groups) > 1
        or candidate["boundary_class"]
        in {
            "flavin_monooxygenase_dehydrogenase_boundary",
            "fe_s_flavin_combined_system",
            "heme_peroxidase_oxidase_like",
        }
    )
    candidate["cofactor_or_ligand_feature_groups"] = cofactor_groups
    candidate["materialization_bucket"] = _materialization_bucket(candidate)
    candidate["duplicate_status_summary"] = {
        "current702_status": candidate.get("duplicate_current_registry_conflict_status"),
        "prior_external_status": prior_duplicate["prior_external_conflict_status"],
        "blocked_by_current_or_prior_duplicate": bool(current_conflict or prior_conflict),
    }
    candidate.setdefault("guardrails", {}).update(
        {
            "external_redox_cofactor_shard_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
            "production_import_edited": False,
            "ontology_edited": False,
            "heldout_split_or_threshold_edited": False,
            "model_weights_edited": False,
            "ec_rhea_names_and_source_ids_provenance_only": True,
        }
    )
    return candidate


def _source_retrieval_blocker_row(
    *,
    lane: dict[str, str],
    search_record: dict[str, Any],
    error: Exception,
    created: str,
    search_metadata: dict[str, Any],
    prior_index: dict[str, Any],
) -> dict[str, Any]:
    accession = _clean_accession(search_record.get("accession"))
    sequence_sha = _sequence_sha256(search_record.get("sequence"))
    prior_duplicate = _prior_duplicate_status(
        accession=accession,
        sequence_sha=sequence_sha,
        prior_index=prior_index,
    )
    return {
        "stable_candidate_key": (
            "external_scaleout_redox_cofactor_confounded:"
            f"uniprot:{accession}"
        ),
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "reviewed_status": search_record.get("reviewed"),
        "protein_name": search_record.get("protein_name"),
        "organism": search_record.get("organism"),
        "sequence_length": search_record.get("length"),
        "target_family_lane": lane["target_family_lane"],
        "lane_id": lane["lane_id"],
        "boundary_class": lane["boundary_class"],
        "boundary_role": lane["boundary_role"],
        "source_query": lane["query"],
        "source_evidence_features": [],
        "source_evidence_feature_count": 0,
        "source_evidence_codes": [],
        "residue_locators": [],
        "residue_locator_count": 0,
        "exact_residue_locator_count": 0,
        "coordinate_source_status": "entry_retrieval_failed_before_coordinate_check",
        "coordinate_status": "entry_retrieval_failed_before_coordinate_check",
        "coordinate_source": None,
        "afdb_or_pdb_identifier": None,
        "pdb_ids": search_record.get("pdb_ids", []) or [],
        "alphafold_ids": search_record.get("alphafold_ids", []) or [],
        "coordinate_mapping_status": "entry_retrieval_failed",
        "rhea_ec_provenance": {
            "ec_numbers": search_record.get("ec_numbers", []) or [],
            "specific_ec_count": 0,
            "catalytic_activity_comment_count": 0,
            "rhea_records": [],
            "rhea_record_count": 0,
            "rhea_status": "entry_retrieval_failed",
        },
        "cofactor_provenance": [],
        "prior_external_duplicate_conflict": prior_duplicate,
        "duplicate_status_summary": {
            "current702_status": "not_checked_after_entry_retrieval_failure",
            "prior_external_status": prior_duplicate["prior_external_conflict_status"],
            "blocked_by_current_or_prior_duplicate": prior_duplicate[
                "duplicate_or_prior_external_conflict"
            ],
        },
        "evidence_basis": {
            "reviewed_swiss_prot": False,
            "source_retrieval_blocker": True,
            "error_type": type(error).__name__,
            "error": str(error),
        },
        "blocker_basis": {
            "applicable": True,
            "terminal_route_basis": "uniprot_entry_retrieval_failed",
            "missing_preflight_requirements": ["uniprot_entry_record"],
            "source_retrieval_blocker": True,
        },
        "terminal_state": "hard_blocked_with_next_action",
        "terminal_route_basis": "uniprot_entry_retrieval_failed",
        "confidence_tier": "blocked",
        "exact_next_action": (
            "Retry UniProt entry materialization for this accession before any "
            "locator, coordinate, or import review."
        ),
        "source_hashes": {
            "source_query_sha256": _canonical_sha256(lane["query"]),
            "uniprot_search_row_sha256": _canonical_sha256(search_record),
        },
        "source_provenance": {
            "query_timestamp_utc": created,
            "source_query": lane["query"],
            "uniprot_search_url": search_metadata.get("url"),
            "uniprot_entry_url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
        },
        "cofactor_confounded_signal": lane["boundary_role"]
        == "cofactor_confounded_oos_negative",
        "cofactor_or_ligand_feature_groups": [],
        "materialization_bucket": "hard_materialization_or_source_blocker",
        "guardrails": {
            "external_redox_cofactor_shard_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
        },
    }


def build_external_scaleout_redox_cofactor_confounded_shard(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    prior_payloads: list[dict[str, Any]] | None = None,
    prior_source_records: list[dict[str, Any]] | None = None,
    prior_load_failures: list[dict[str, Any]] | None = None,
    created_utc: str | None = None,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    max_records_per_lane: int = 500,
    max_candidates: int = 4200,
    target_unique_candidates: int = 2000,
    stretch_unique_candidates: int = 4000,
    entry_fetch_workers: int = 12,
    entry_fetch_timeout_seconds: int = 8,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] | None = None,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
    fetch_rhea_fallback: bool = False,
    max_reactions_per_ec: int = 1,
) -> dict[str, Any]:
    if max_records_per_lane < 1 or max_records_per_lane > 500:
        raise ValueError("max_records_per_lane must be between 1 and 500")
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    if target_unique_candidates < 1:
        raise ValueError("target_unique_candidates must be positive")
    if stretch_unique_candidates < target_unique_candidates:
        raise ValueError(
            "stretch_unique_candidates must be greater than or equal to target_unique_candidates"
        )
    if entry_fetch_workers < 1 or entry_fetch_workers > 32:
        raise ValueError("entry_fetch_workers must be between 1 and 32")
    if entry_fetch_timeout_seconds < 1 or entry_fetch_timeout_seconds > 30:
        raise ValueError("entry_fetch_timeout_seconds must be between 1 and 30")
    effective_entry_fetcher = entry_fetcher or (
        lambda accession: fetch_uniprot_entry_with_timeout(
            accession, timeout_seconds=entry_fetch_timeout_seconds
        )
    )

    created = created_utc or _utc_now_iso()
    current_index = _current_reference_index(
        current_manifest_payload, label_registry_payload
    )
    prior_index = _prior_index_from_payloads(prior_payloads or [])
    queued: list[tuple[dict[str, str], dict[str, Any], dict[str, Any]]] = []
    lane_summaries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = list(prior_load_failures or [])
    seen_accessions: set[str] = set()
    seen_sequence_shas: set[str] = set()
    total_fetched_records = 0
    stopped_by_max_candidates = False

    for lane in lane_queries:
        if len(queued) >= max_candidates:
            lane_summaries.append(
                {
                    "lane_id": lane["lane_id"],
                    "target_family_lane": lane["target_family_lane"],
                    "boundary_class": lane["boundary_class"],
                    "boundary_role": lane["boundary_role"],
                    "query": lane["query"],
                    "fetched_record_count": 0,
                    "unique_candidate_count": 0,
                    "status": "skipped_after_max_candidates_reached",
                }
            )
            stopped_by_max_candidates = True
            continue
        try:
            search_payload = query_fetcher(lane["query"], max_records_per_lane)
        except Exception as exc:  # pragma: no cover - live source failure path
            fetch_failures.append(
                {
                    "lane_id": lane["lane_id"],
                    "source": "uniprot_search",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            lane_summaries.append(
                {
                    "lane_id": lane["lane_id"],
                    "target_family_lane": lane["target_family_lane"],
                    "boundary_class": lane["boundary_class"],
                    "boundary_role": lane["boundary_role"],
                    "query": lane["query"],
                    "fetched_record_count": 0,
                    "unique_candidate_count": 0,
                    "status": "query_fetch_failed",
                }
            )
            continue

        search_metadata = search_payload.get("metadata", {}) or {}
        fetched_records = [
            item
            for item in search_payload.get("records", []) or []
            if isinstance(item, dict)
        ]
        total_fetched_records += len(fetched_records)
        unique_count = 0
        for search_record in fetched_records:
            accession = _clean_accession(search_record.get("accession"))
            sequence_sha = _sequence_sha256(search_record.get("sequence"))
            if (
                not accession
                or accession in seen_accessions
                or (sequence_sha is not None and sequence_sha in seen_sequence_shas)
            ):
                continue
            if len(queued) >= max_candidates:
                stopped_by_max_candidates = True
                break
            seen_accessions.add(accession)
            if sequence_sha is not None:
                seen_sequence_shas.add(sequence_sha)
            queued.append((lane, search_record, search_metadata))
            unique_count += 1

        lane_summaries.append(
            {
                "lane_id": lane["lane_id"],
                "target_family_lane": lane["target_family_lane"],
                "boundary_class": lane["boundary_class"],
                "boundary_role": lane["boundary_role"],
                "query": lane["query"],
                "fetched_record_count": len(fetched_records),
                "unique_candidate_count": unique_count,
                "source_url": search_metadata.get("url"),
                "status": "query_fetched",
            }
        )

    def fetch_entry(
        item: tuple[dict[str, str], dict[str, Any], dict[str, Any]]
    ) -> tuple[
        dict[str, str],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any] | None,
        Exception | None,
    ]:
        lane, search_record, search_metadata = item
        accession = _clean_accession(search_record.get("accession"))
        try:
            return (
                lane,
                search_record,
                search_metadata,
                effective_entry_fetcher(accession),
                None,
            )
        except Exception as exc:  # pragma: no cover - live source failure path
            return lane, search_record, search_metadata, None, exc

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=entry_fetch_workers) as executor:
        entry_payloads = list(executor.map(fetch_entry, queued))

    for lane, search_record, search_metadata, entry_payload, entry_error in entry_payloads:
        accession = _clean_accession(search_record.get("accession"))
        sequence_sha = _sequence_sha256(search_record.get("sequence"))
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
            rows.append(
                _source_retrieval_blocker_row(
                    lane=lane,
                    search_record=search_record,
                    error=entry_error,
                    created=created,
                    search_metadata=search_metadata,
                    prior_index=prior_index,
                )
            )
            continue
        entry_record = entry_payload.get("record", entry_payload)
        if not isinstance(entry_record, dict):
            error = ValueError("entry fetcher did not return a record dictionary")
            fetch_failures.append(
                {
                    "lane_id": lane["lane_id"],
                    "accession": accession,
                    "source": "uniprot_entry",
                    "error_type": type(error).__name__,
                    "error": str(error),
                }
            )
            rows.append(
                _source_retrieval_blocker_row(
                    lane=lane,
                    search_record=search_record,
                    error=error,
                    created=created,
                    search_metadata=search_metadata,
                    prior_index=prior_index,
                )
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
        prior_duplicate = _prior_duplicate_status(
            accession=accession,
            sequence_sha=sequence_sha,
            prior_index=prior_index,
        )
        rows.append(
            _apply_redox_shard_policy(
                candidate,
                lane=lane,
                prior_duplicate=prior_duplicate,
            )
        )
        fetch_failures.extend(rhea_failures)

    terminal_counts = Counter(row["terminal_state"] for row in rows)
    family_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    boundary_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    materialization_counts = Counter(row["materialization_bucket"] for row in rows)
    for row in rows:
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
        boundary_counts[row["boundary_class"]][row["terminal_state"]] += 1

    duplicate_count = terminal_counts.get("blocked_duplicate_or_current_registry_conflict", 0)
    import_ready_count = terminal_counts.get("import_ready_preview", 0)
    oos_count = terminal_counts.get("reject/OOS_preserve_signal", 0)
    confounded_signal_count = sum(
        1 for row in rows if row.get("cofactor_confounded_signal") is True
    )
    unique_non_duplicate_count = len(rows) - duplicate_count

    validation_checks = {
        "all_rows_have_terminal_state": all(row.get("terminal_state") for row in rows),
        "all_terminal_states_known": all(
            row.get("terminal_state") in TERMINAL_STATES for row in rows
        ),
        "all_rows_have_source_provenance": all(
            row.get("source_hashes") and row.get("source_provenance") for row in rows
        ),
        "all_rows_have_boundary_class": all(row.get("boundary_class") for row in rows),
        "all_rows_have_materialization_bucket": all(
            row.get("materialization_bucket") for row in rows
        ),
        "candidate_count_matches_terminal_counts": len(rows)
        == sum(terminal_counts.values()),
        "target_2000_unique_non_duplicate_candidates_met": unique_non_duplicate_count
        >= target_unique_candidates,
        "production_registry_edit_count": 0,
    }
    validation_checks["stretch_4000_unique_non_duplicate_candidates_met"] = (
        unique_non_duplicate_count >= stretch_unique_candidates
    )
    validation_checks["passed"] = all(
        value is True
        for key, value in validation_checks.items()
        if isinstance(value, bool) and not key.startswith("stretch_")
    )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "scope": {
            "current_reference_scope": "current702",
            "mission": "targeted_external_scaleout_for_redox_cofactor_confounded_families",
            "rationale": (
                "Earlier experiments showed cofactor/fold confounding and OOS false "
                "positives as central failure modes; this shard therefore targets "
                "redox oxygen/sulfur, heme, flavin, Fe-S, sulfur oxidoreductase, "
                "oxygenase, dehydrogenase, and cofactor-confounded boundary rows."
            ),
            "production_surfaces_not_edited": [
                "curated mechanism registries",
                "imports",
                "ontologies",
                "heldout splits",
                "production thresholds",
                "model weights",
            ],
        },
        "routing_policy": {
            "terminal_states": list(TERMINAL_STATES),
            "import_ready_preview_gate": [
                "reviewed Swiss-Prot status",
                "no exact current702 accession or sequence SHA overlap",
                "no exact prior external artifact or branch accession/sequence overlap",
                "at least one exact curated residue locator",
                "AFDB/PDB coordinate provenance available",
                "specific EC and Rhea-style reaction provenance available",
                "not an explicit cofactor-confounded OOS-negative boundary lane",
            ],
            "production_import_rule": (
                "Preview rows are not production imports. They still require "
                "current-countable structural duplicate screening, label-factory "
                "review, and explicit registry-change authorization."
            ),
        },
        "counts": {
            "candidate_rows": len(rows),
            "unique_non_duplicate_candidate_rows": unique_non_duplicate_count,
            "target_unique_candidates": target_unique_candidates,
            "stretch_unique_candidates": stretch_unique_candidates,
            "import_ready_preview_rows": import_ready_count,
            "oos_preserve_signal_rows": oos_count,
            "cofactor_confounded_signal_rows": confounded_signal_count,
            "duplicate_current_or_prior_conflict_rows": duplicate_count,
            "fetch_failure_rows": len(fetch_failures),
            "total_uniprot_search_rows_fetched": total_fetched_records,
            "max_candidate_cap": max_candidates,
            "entry_fetch_timeout_seconds": entry_fetch_timeout_seconds,
            "stopped_by_max_candidates": stopped_by_max_candidates,
        },
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "family_lane_terminal_state_counts": {
            family: dict(sorted(counts.items()))
            for family, counts in sorted(family_counts.items())
        },
        "boundary_class_terminal_state_counts": {
            boundary: dict(sorted(counts.items()))
            for boundary, counts in sorted(boundary_counts.items())
        },
        "materialization_bucket_counts": dict(sorted(materialization_counts.items())),
        "deduplication_summary": {
            **prior_index,
            "current_reference_accession_count": current_index[
                "current_reference_accession_count"
            ],
            "current_sequence_sha_count": current_index["current_sequence_sha_count"],
            "prior_source_records": prior_source_records or [],
            "prior_load_failure_count": len(prior_load_failures or []),
        },
        "lane_summaries": lane_summaries,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "validation_checks": validation_checks,
        "guardrails": {
            "production_registry_edited": False,
            "production_import_edited": False,
            "ontology_edited": False,
            "heldout_split_or_threshold_edited": False,
            "model_weights_edited": False,
            "coordinate_downloads_performed": False,
            "mechanism_text_ec_rhea_names_and_source_ids_provenance_only": True,
            "oos_and_cofactor_confounded_signal_preserved": True,
        },
    }


def build_external_scaleout_redox_cofactor_confounded_import_ready_preview(
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
            "boundary_class": row["boundary_class"],
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
            "cofactor_provenance": row["cofactor_provenance"],
            "cofactor_or_ligand_feature_groups": row[
                "cofactor_or_ligand_feature_groups"
            ],
            "duplicate_status_summary": row["duplicate_status_summary"],
            "source_hashes": row["source_hashes"],
            "source_provenance": row["source_provenance"],
            "evidence_basis": row["evidence_basis"],
            "blocker_basis": row["blocker_basis"],
            "import_ready_preview": True,
            "ready_for_production_label_import": False,
            "remaining_required_before_import": [
                "current_countable_structural_duplicate_screen",
                "label_factory_gate_and_explicit_review_decision",
                "production_registry_change_authorization",
            ],
            "exact_next_action": row["exact_next_action"],
        }
        for row in artifact.get("rows", [])
        if row.get("terminal_state") == "import_ready_preview"
    ]
    return {
        "artifact_id": IMPORT_READY_PREVIEW_ARTIFACT_ID,
        "schema_version": IMPORT_READY_PREVIEW_SCHEMA_VERSION,
        "created_utc": created,
        "source_artifact_id": artifact.get("artifact_id"),
        "source_artifact_sha256": _canonical_sha256(artifact),
        "candidate_count": len(rows),
        "rows": rows,
        "guardrails": {
            "preview_only": True,
            "production_registry_edited": False,
            "label_import_performed": False,
        },
    }


def render_external_scaleout_redox_cofactor_confounded_report(
    artifact: dict[str, Any],
) -> str:
    counts = artifact["counts"]
    lines = [
        "# External Scaleout Shard - Redox Cofactor Confounded current702",
        "",
        "Read-only targeted external scaleout over reviewed Swiss-Prot rows. "
        "The shard targets redox/cofactor-confounded failure modes rather than "
        "random candidate volume and performs no production import.",
        "",
        "## Family-Selection Rationale",
        "",
        artifact["scope"]["rationale"],
        "",
        "## Summary",
        "",
        f"- Candidate rows: `{counts['candidate_rows']}`",
        f"- Unique non-duplicate candidate rows: `{counts['unique_non_duplicate_candidate_rows']}`",
        f"- Target met (>=2,000): `{artifact['validation_checks']['target_2000_unique_non_duplicate_candidates_met']}`",
        f"- Stretch met (>=4,000): `{artifact['validation_checks']['stretch_4000_unique_non_duplicate_candidates_met']}`",
        f"- Import-ready preview rows: `{counts['import_ready_preview_rows']}`",
        f"- OOS preserve-signal rows: `{counts['oos_preserve_signal_rows']}`",
        f"- Cofactor-confounded signal rows: `{counts['cofactor_confounded_signal_rows']}`",
        f"- Duplicate/current/prior conflicts: `{counts['duplicate_current_or_prior_conflict_rows']}`",
        f"- Fetch/source failure rows: `{counts['fetch_failure_rows']}`",
        f"- Validation passed: `{artifact['validation_checks']['passed']}`",
        "",
        "## Terminal State Counts",
        "",
        "| terminal state | count |",
        "| --- | ---: |",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"| `{state}` | {count} |")

    lines.extend(
        [
            "",
            "## Boundary Classes Covered",
            "",
            "| boundary class | terminal counts |",
            "| --- | --- |",
        ]
    )
    for boundary, terminal_counts in artifact[
        "boundary_class_terminal_state_counts"
    ].items():
        lines.append(f"| `{boundary}` | `{terminal_counts}` |")

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

    lines.extend(
        [
            "",
            "## Source Query Coverage",
            "",
            "| lane | boundary role | fetched | unique queued | status |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for lane in artifact["lane_summaries"]:
        lines.append(
            f"| `{lane['lane_id']}` | `{lane['boundary_role']}` | "
            f"{lane['fetched_record_count']} | {lane['unique_candidate_count']} | "
            f"{lane['status']} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Matrix Sample",
            "",
            "| candidate | lane | terminal state | locators | coordinate | cofactors | next action |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in artifact["rows"][:120]:
        cofactors = ",".join(row.get("cofactor_or_ligand_feature_groups", [])) or "none"
        action = str(row["exact_next_action"]).replace("|", "\\|")
        lines.append(
            f"| `{row['candidate_id']}` | `{row['boundary_class']}` | "
            f"`{row['terminal_state']}` | {row['exact_residue_locator_count']} | "
            f"{row['coordinate_source_status']} | {cofactors} | {action} |"
        )

    lines.extend(
        [
            "",
            "## Next Mechanical Continuation",
            "",
            "- Run current-countable structural duplicate screens and label-factory "
            "review only on `import_ready_preview` rows; keep OOS/confounded "
            "negative rows as preserved signal unless a human family decision "
            "explicitly reverses them.",
            "- For repair buckets, prioritize exact locator repair before coordinate "
            "download work when AFDB/PDB provenance is already present.",
        ]
    )
    return "\n".join(lines) + "\n"


def _load_git_json(spec: str) -> tuple[dict[str, Any], dict[str, Any]]:
    if ":" not in spec:
        raise ValueError("git artifact spec must be '<ref>:<path>'")
    ref, path = spec.split(":", 1)
    text = subprocess.check_output(["git", "show", spec], text=True)
    commit = subprocess.check_output(["git", "rev-parse", ref], text=True).strip()
    payload = json.loads(text)
    return payload, {
        "git_ref": ref,
        "git_commit": commit,
        "path": path,
        "sha256": _canonical_sha256(payload),
        "artifact_id": payload.get("artifact_id"),
    }


def _load_prior_payloads(
    *,
    prior_artifact_paths: list[Path],
    prior_artifact_globs: tuple[str, ...],
    prior_git_artifacts: tuple[str, ...],
    exclude_paths: set[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    paths: list[Path] = []
    for path in prior_artifact_paths:
        paths.append(path)
    for pattern in prior_artifact_globs:
        paths.extend(sorted(Path(".").glob(pattern)))
    unique_paths = []
    seen_paths: set[Path] = set()
    for path in paths:
        normalized = path.resolve()
        if normalized in seen_paths or normalized in exclude_paths:
            continue
        if not path.is_file():
            continue
        seen_paths.add(normalized)
        unique_paths.append(path)

    payloads: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for path in unique_paths:
        try:
            payload = _read_json(path)
        except Exception as exc:
            failures.append(
                {
                    "source": "prior_local_artifact",
                    "path": str(path),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        payloads.append(payload)
        record = _source_record(path)
        record["artifact_id"] = payload.get("artifact_id")
        source_records.append(record)

    for spec in prior_git_artifacts:
        try:
            payload, record = _load_git_json(spec)
        except Exception as exc:
            failures.append(
                {
                    "source": "prior_git_artifact",
                    "spec": spec,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        payloads.append(payload)
        source_records.append(record)
    return payloads, source_records, failures


def write_external_scaleout_redox_cofactor_confounded_shard(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    import_ready_preview_path: Path | None = DEFAULT_IMPORT_READY_PREVIEW_PATH,
    created_utc: str | None = None,
    max_records_per_lane: int = 500,
    max_candidates: int = 4200,
    target_unique_candidates: int = 2000,
    stretch_unique_candidates: int = 4000,
    entry_fetch_workers: int = 12,
    entry_fetch_timeout_seconds: int = 8,
    fetch_rhea_fallback: bool = False,
    prior_artifact_paths: list[Path] | None = None,
    prior_artifact_globs: tuple[str, ...] = DEFAULT_PRIOR_ARTIFACT_GLOBS,
    prior_git_artifacts: tuple[str, ...] = DEFAULT_PRIOR_GIT_ARTIFACTS,
) -> dict[str, Any]:
    current_manifest_payload = _read_json(current_manifest_path)
    label_registry_payload = _read_json(label_registry_path)
    exclude_paths = {
        out_path.resolve(),
        DEFAULT_OUT_PATH.resolve(),
        DEFAULT_IMPORT_READY_PREVIEW_PATH.resolve(),
    }
    prior_payloads, prior_source_records, prior_load_failures = _load_prior_payloads(
        prior_artifact_paths=prior_artifact_paths or [],
        prior_artifact_globs=prior_artifact_globs,
        prior_git_artifacts=prior_git_artifacts,
        exclude_paths=exclude_paths,
    )
    artifact = build_external_scaleout_redox_cofactor_confounded_shard(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=label_registry_payload,
        prior_payloads=prior_payloads,
        prior_source_records=prior_source_records,
        prior_load_failures=prior_load_failures,
        created_utc=created_utc,
        max_records_per_lane=max_records_per_lane,
        max_candidates=max_candidates,
        target_unique_candidates=target_unique_candidates,
        stretch_unique_candidates=stretch_unique_candidates,
        entry_fetch_workers=entry_fetch_workers,
        entry_fetch_timeout_seconds=entry_fetch_timeout_seconds,
        fetch_rhea_fallback=fetch_rhea_fallback,
    )
    artifact["source_artifacts"] = {
        "current_manifest": _source_record(current_manifest_path),
        "label_registry": _source_record(label_registry_path),
        "prior_artifact_count": len(prior_source_records),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_external_scaleout_redox_cofactor_confounded_report(artifact),
            encoding="utf-8",
        )
    if (
        import_ready_preview_path is not None
        and artifact["counts"]["import_ready_preview_rows"] > 0
    ):
        preview = build_external_scaleout_redox_cofactor_confounded_import_ready_preview(
            artifact
        )
        preview["source_artifacts"] = {
            "external_scaleout_shard_redox_cofactor_confounded": _source_record(out_path)
        }
        import_ready_preview_path.parent.mkdir(parents=True, exist_ok=True)
        import_ready_preview_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    return artifact
