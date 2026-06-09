from __future__ import annotations

import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_query
from .external_scaleout_redox_cofactor_confounded import (
    DEFAULT_PRIOR_ARTIFACT_GLOBS,
    DEFAULT_PRIOR_GIT_ARTIFACTS,
    _load_prior_payloads,
    _prior_duplicate_status,
    fetch_uniprot_entry_with_timeout,
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
    "v3_external_scaleout_shard_near_orphan_diversity_current702_20260609"
)
IMPORT_READY_PREVIEW_ARTIFACT_ID = (
    "v3_external_scaleout_shard_near_orphan_diversity_"
    "import_ready_preview_current702_20260609"
)
SCHEMA_VERSION = "v3.external_scaleout_shard_near_orphan_diversity"
IMPORT_READY_PREVIEW_SCHEMA_VERSION = (
    "v3.external_scaleout_shard_near_orphan_diversity_import_ready_preview"
)

DEFAULT_OUT_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_near_orphan_diversity_current702_20260609.json"
)
DEFAULT_IMPORT_READY_PREVIEW_PATH = Path(
    "artifacts/"
    "v3_external_scaleout_shard_near_orphan_diversity_"
    "import_ready_preview_current702_20260609.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/external_scaleout_shard_near_orphan_diversity_current702_20260609.md"
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

OOS_BOUNDARY_ROLES = {
    "oos_hard_negative",
    "fold_confounded_hard_negative",
    "cofactor_confounded_non_target_enzyme",
}

REPAIR_TERMINAL_STATES = {
    "locator_ready_candidate",
    "coordinate_ready_pending_locator",
    "locator_repair_candidate",
    "coordinate_repair_candidate",
}

DEFAULT_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "near_orphan_uncharacterized_reviewed",
        "target_family_lane": "near-orphan/no-reliable-structure",
        "diversity_bin": "near_orphan_uncharacterized",
        "boundary_class": "near_orphan_no_reliable_structure",
        "boundary_role": "near_orphan_source_candidate",
        "import_route": "provisional",
        "query": (
            "(reviewed:true) AND ((protein_name:uncharacterized) OR "
            "(protein_name:hypothetical) OR (protein_name:DUF))"
        ),
    },
    {
        "lane_id": "near_orphan_low_annotation_reviewed",
        "target_family_lane": "near-orphan/no-reliable-structure",
        "diversity_bin": "near_orphan_low_annotation",
        "boundary_class": "near_orphan_no_reliable_structure",
        "boundary_role": "near_orphan_source_candidate",
        "import_route": "provisional",
        "query": "(reviewed:true) AND ((annotation_score:1) OR (annotation_score:2))",
    },
    {
        "lane_id": "terpene_synthase_lyase",
        "target_family_lane": "terpene synthase/lyase",
        "diversity_bin": "terpene_lyase",
        "boundary_class": "terpene_lyase_isomerase_transferase",
        "boundary_role": "sparse_family_source_candidate",
        "import_route": "import_ready_preview",
        "query": (
            "(reviewed:true) AND ((protein_name:terpene) OR "
            "(protein_name:sesquiterpene) OR (protein_name:monoterpene) OR "
            "(ec:4.2.3.*))"
        ),
    },
    {
        "lane_id": "isomerase_racemase_epimerase_mutase",
        "target_family_lane": "isomerase/racemase/epimerase",
        "diversity_bin": "isomerase_transferase_tail",
        "boundary_class": "terpene_lyase_isomerase_transferase",
        "boundary_role": "sparse_family_source_candidate",
        "import_route": "import_ready_preview",
        "query": (
            "(reviewed:true) AND ((ec:5.*) OR (protein_name:isomerase) OR "
            "(protein_name:racemase) OR (protein_name:epimerase) OR "
            "(protein_name:mutase))"
        ),
    },
    {
        "lane_id": "glycosyl_methyl_transferase_tail",
        "target_family_lane": "transferase tail outside current fingerprints",
        "diversity_bin": "isomerase_transferase_tail",
        "boundary_class": "terpene_lyase_isomerase_transferase",
        "boundary_role": "sparse_family_source_candidate",
        "import_route": "import_ready_preview",
        "query": (
            "(reviewed:true) AND ((ec:2.1.*) OR (ec:2.4.*) OR "
            "(protein_name:methyltransferase) OR "
            "(protein_name:glycosyltransferase))"
        ),
    },
    {
        "lane_id": "carbon_carbon_lyase_decarboxylase",
        "target_family_lane": "carbon-carbon lyase/decarboxylase",
        "diversity_bin": "carbon_carbon_lyase_decarboxylase",
        "boundary_class": "diverse_lyase_nonhydrolase",
        "boundary_role": "sparse_family_source_candidate",
        "import_route": "import_ready_preview",
        "query": (
            "(reviewed:true) AND ((ec:4.1.*) OR "
            "(protein_name:decarboxylase) OR (protein_name:aldolase))"
        ),
    },
    {
        "lane_id": "dehydratase_hydratase_lyase",
        "target_family_lane": "dehydratase/hydratase lyase",
        "diversity_bin": "diverse_lyase_hydratase",
        "boundary_class": "diverse_lyase_nonhydrolase",
        "boundary_role": "sparse_family_source_candidate",
        "import_route": "import_ready_preview",
        "query": (
            "(reviewed:true) AND ((ec:4.2.*) OR "
            "(protein_name:dehydratase) OR (protein_name:hydratase))"
        ),
    },
    {
        "lane_id": "ligase_synthetase_oos_abstention",
        "target_family_lane": "ligase/synthetase abstention probe",
        "diversity_bin": "ligase_synthetase_oos",
        "boundary_class": "oos_hard_negative_abstention_probe",
        "boundary_role": "oos_hard_negative",
        "import_route": "reject",
        "query": (
            "(reviewed:true) AND ((ec:6.*) OR "
            "(protein_name:ligase) OR (protein_name:synthetase))"
        ),
    },
    {
        "lane_id": "transport_atpase_oos_hard_negative",
        "target_family_lane": "ATPase/transporter OOS hard negative",
        "diversity_bin": "transport_atpase_oos",
        "boundary_class": "oos_hard_negative_abstention_probe",
        "boundary_role": "oos_hard_negative",
        "import_route": "reject",
        "query": (
            "(reviewed:true) AND ((protein_name:ATPase) OR "
            "(protein_name:transporter) OR (ec:7.*))"
        ),
    },
    {
        "lane_id": "hydrolase_fold_confounded_negative",
        "target_family_lane": "hydrolase-like fold-confounded negative",
        "diversity_bin": "fold_confounded_hydrolase_like",
        "boundary_class": "fold_confounded_negative",
        "boundary_role": "fold_confounded_hard_negative",
        "import_route": "reject",
        "query": (
            "(reviewed:true) AND ((ec:3.1.*) OR "
            "(protein_name:esterase) OR (protein_name:lipase) OR "
            "(protein_name:peptidase))"
        ),
    },
    {
        "lane_id": "metalloprotein_nonhydrolase_fold_confounded",
        "target_family_lane": "metal-cofactor non-target enzyme",
        "diversity_bin": "fold_confounded_metal_nonhydrolase",
        "boundary_class": "fold_confounded_negative",
        "boundary_role": "fold_confounded_hard_negative",
        "import_route": "reject",
        "query": (
            "(reviewed:true) AND (((cc_cofactor:zinc) OR (protein_name:zinc)) "
            "AND ((protein_name:dehydrogenase) OR "
            "(protein_name:transcription) OR (protein_name:alcohol)))"
        ),
    },
    {
        "lane_id": "plp_non_target_cofactor_confounded",
        "target_family_lane": "PLP cofactor-confounded non-target",
        "diversity_bin": "cofactor_confounded_non_target",
        "boundary_class": "cofactor_confounded_non_target",
        "boundary_role": "cofactor_confounded_non_target_enzyme",
        "import_route": "reject",
        "query": (
            '(reviewed:true) AND (((keyword:"Pyridoxal phosphate") OR '
            '(cc_cofactor:"pyridoxal phosphate")) AND '
            "((protein_name:decarboxylase) OR (protein_name:racemase) OR "
            "(protein_name:synthase)))"
        ),
    },
    {
        "lane_id": "sam_methyltransferase_nonradical_confounded",
        "target_family_lane": "SAM methyltransferase non-radical control",
        "diversity_bin": "cofactor_confounded_non_target",
        "boundary_class": "cofactor_confounded_non_target",
        "boundary_role": "cofactor_confounded_non_target_enzyme",
        "import_route": "reject",
        "query": (
            '(reviewed:true) AND ((protein_name:methyltransferase) OR '
            '(keyword:"S-adenosyl-L-methionine"))'
        ),
    },
    {
        "lane_id": "cysteine_aspartic_metallo_protease_boundary",
        "target_family_lane": "non-serine protease OOS boundary",
        "diversity_bin": "fold_confounded_protease_boundary",
        "boundary_class": "fold_confounded_negative",
        "boundary_role": "fold_confounded_hard_negative",
        "import_route": "reject",
        "query": (
            '(reviewed:true) AND ((protein_name:"cysteine protease") OR '
            '(protein_name:"aspartic protease") OR '
            "(protein_name:metalloprotease))"
        ),
    },
    {
        "lane_id": "no_reliable_structure_reviewed_enzyme_tail",
        "target_family_lane": "no-reliable-structure enzyme tail",
        "diversity_bin": "no_reliable_structure_tail",
        "boundary_class": "near_orphan_no_reliable_structure",
        "boundary_role": "no_reliable_structure_source_candidate",
        "import_route": "provisional",
        "query": (
            "(reviewed:true) AND ((protein_name:enzyme) OR (ec:*)) "
            "AND ((annotation_score:1) OR (annotation_score:2))"
        ),
    },
)


def _mechanism_feature_groups(row: dict[str, Any]) -> list[str]:
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
    text_parts.extend(
        str(row.get(key) or "") for key in ("protein_name", "target_family_lane")
    )
    for ec in row.get("rhea_ec_provenance", {}).get("ec_numbers", []) or []:
        text_parts.append(str(ec))
    text = " ".join(text_parts).lower()
    groups: set[str] = set()
    if any(token in text for token in ("pyridoxal", "plp")):
        groups.add("plp")
    if any(token in text for token in ("sam", "s-adenosyl", "methyltransferase")):
        groups.add("sam_or_methyltransferase")
    if any(token in text for token in ("cobalamin", "b12")):
        groups.add("cobalamin")
    if any(token in text for token in ("fad", "fmn", "flavin")):
        groups.add("flavin")
    if any(token in text for token in ("heme", "haem")):
        groups.add("heme")
    if any(token in text for token in ("zinc", "metal", "metallo", "mg", "mn")):
        groups.add("metal")
    if any(token in text for token in ("terpene", "isoprene", "sesquiterpene")):
        groups.add("terpene")
    if any(token in text for token in ("isomerase", "racemase", "epimerase", "mutase")):
        groups.add("isomerase")
    if any(token in text for token in ("glycosyl", "transferase", "ec 2.")):
        groups.add("transferase")
    if any(token in text for token in ("lyase", "decarboxylase", "aldolase", "hydratase")):
        groups.add("lyase")
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
    if state == "blocked_duplicate_or_current_registry_conflict":
        return "duplicate_or_current_conflict"
    if state == "reject/OOS_preserve_signal":
        return "reject_oos_or_confounded_signal"
    return "hard_materialization_or_source_blocker"


def _no_structure_route(row: dict[str, Any], lane: dict[str, str]) -> dict[str, Any]:
    missing = row.get("coordinate_source_status") == "coordinate_provenance_missing"
    explicit_lane = lane["boundary_role"] in {
        "near_orphan_source_candidate",
        "no_reliable_structure_source_candidate",
    }
    return {
        "explicit_no_structure_or_provenance_route": bool(missing or explicit_lane),
        "coordinate_source_status": row.get("coordinate_source_status"),
        "afdb_or_pdb_identifier": row.get("afdb_or_pdb_identifier"),
        "route_basis": (
            "coordinate_provenance_missing_or_lane_targets_no_reliable_structure"
            if missing or explicit_lane
            else "coordinate_provenance_present"
        ),
        "next_action": (
            "Preserve no-structure/near-orphan evidence; source AFDB/PDB or "
            "document no-reliable-structure policy before import review."
            if missing
            else "Use existing AFDB/PDB provenance for locator and duplicate review."
        ),
    }


def _apply_near_orphan_diversity_policy(
    row: dict[str, Any],
    *,
    lane: dict[str, str],
    prior_duplicate: dict[str, Any],
) -> dict[str, Any]:
    candidate = json.loads(json.dumps(row))
    candidate["stable_candidate_key"] = (
        "external_scaleout_near_orphan_diversity:"
        f"uniprot:{candidate['accession']}"
    )
    candidate["diversity_bin"] = lane["diversity_bin"]
    candidate["boundary_class"] = lane["boundary_class"]
    candidate["boundary_role"] = lane["boundary_role"]
    candidate["import_route"] = lane["import_route"]
    candidate["terminal_state_original_from_source_route"] = candidate["terminal_state"]
    candidate["prior_external_duplicate_conflict"] = prior_duplicate
    duplicate_record = candidate.setdefault("duplicate_current_registry_conflict", {})
    duplicate_record["prior_external_conflict"] = prior_duplicate

    current_conflict = bool(duplicate_record.get("duplicate_or_current_registry_conflict"))
    prior_conflict = prior_duplicate["duplicate_or_prior_external_conflict"]
    oos_role = lane["boundary_role"] in OOS_BOUNDARY_ROLES

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
    elif oos_role:
        candidate["terminal_state"] = "reject/OOS_preserve_signal"
        candidate["terminal_route_basis"] = (
            f"{lane['boundary_role']}_preserved_as_abstention_generalization_signal"
        )
        candidate["confidence_tier"] = "oos_hard_negative_signal"
        candidate["exact_next_action"] = (
            "Preserve as OOS/fold/cofactor-confounded hard-negative signal; do "
            "not route to import without an explicit human family decision."
        )
        candidate.setdefault("blocker_basis", {})["applicable"] = True
    elif candidate["terminal_state"] == "external_countable_preflight_candidate":
        if lane["import_route"] == "provisional":
            candidate["terminal_state"] = (
                "provisional_external_countable_preflight_candidate"
            )
            candidate["terminal_route_basis"] = (
                "reviewed_exact_locator_coordinate_reaction_ready_but_near_orphan_or_"
                "diversity_family_requires_policy_review"
            )
            candidate["confidence_tier"] = "provisional"
            candidate["exact_next_action"] = (
                "Keep as provisional near-orphan/diversity candidate; run family "
                "policy review and structural duplicate screening before any "
                "import-ready promotion."
            )
        else:
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

    feature_groups = _mechanism_feature_groups(candidate)
    no_structure = candidate.get("coordinate_source_status") == "coordinate_provenance_missing"
    near_orphan = lane["boundary_role"] in {
        "near_orphan_source_candidate",
        "no_reliable_structure_source_candidate",
    }
    candidate["near_orphan_signal"] = near_orphan
    candidate["no_structure_or_no_reliable_structure_signal"] = bool(
        no_structure or near_orphan
    )
    candidate["oos_hard_negative_signal"] = lane["boundary_role"] == "oos_hard_negative"
    candidate["fold_confounded_negative_signal"] = (
        lane["boundary_role"] == "fold_confounded_hard_negative"
    )
    candidate["cofactor_confounded_non_target_signal"] = (
        lane["boundary_role"] == "cofactor_confounded_non_target_enzyme"
        or lane["diversity_bin"] == "cofactor_confounded_non_target"
    )
    candidate["mechanism_or_cofactor_feature_groups"] = feature_groups
    candidate["no_structure_route"] = _no_structure_route(candidate, lane)
    candidate["materialization_bucket"] = _materialization_bucket(candidate)
    candidate["duplicate_status_summary"] = {
        "current702_status": candidate.get("duplicate_current_registry_conflict_status"),
        "prior_external_status": prior_duplicate["prior_external_conflict_status"],
        "blocked_by_current_or_prior_duplicate": bool(current_conflict or prior_conflict),
    }
    candidate.setdefault("guardrails", {}).update(
        {
            "external_near_orphan_diversity_shard_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
            "production_import_edited": False,
            "ontology_edited": False,
            "heldout_split_or_threshold_edited": False,
            "model_weights_edited": False,
            "ec_rhea_names_and_source_ids_provenance_only": True,
            "no_structure_rows_routed_explicitly": True,
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
    coordinate_missing = not (
        search_record.get("pdb_ids") or search_record.get("alphafold_ids")
    )
    return {
        "stable_candidate_key": (
            "external_scaleout_near_orphan_diversity:"
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
        "diversity_bin": lane["diversity_bin"],
        "boundary_class": lane["boundary_class"],
        "boundary_role": lane["boundary_role"],
        "import_route": lane["import_route"],
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
        "near_orphan_signal": lane["boundary_role"]
        in {"near_orphan_source_candidate", "no_reliable_structure_source_candidate"},
        "no_structure_or_no_reliable_structure_signal": coordinate_missing,
        "oos_hard_negative_signal": lane["boundary_role"] == "oos_hard_negative",
        "fold_confounded_negative_signal": lane["boundary_role"]
        == "fold_confounded_hard_negative",
        "cofactor_confounded_non_target_signal": lane["boundary_role"]
        == "cofactor_confounded_non_target_enzyme",
        "mechanism_or_cofactor_feature_groups": [],
        "no_structure_route": {
            "explicit_no_structure_or_provenance_route": True,
            "coordinate_source_status": "entry_retrieval_failed_before_coordinate_check",
            "afdb_or_pdb_identifier": None,
            "route_basis": "source_retrieval_failed_before_coordinate_provenance_check",
            "next_action": "Retry source retrieval before structural routing.",
        },
        "materialization_bucket": "hard_materialization_or_source_blocker",
        "guardrails": {
            "external_near_orphan_diversity_shard_only": True,
            "label_import_performed": False,
            "production_registry_edited": False,
        },
    }


def build_external_scaleout_near_orphan_diversity_shard(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    prior_payloads: list[dict[str, Any]] | None = None,
    prior_source_records: list[dict[str, Any]] | None = None,
    prior_load_failures: list[dict[str, Any]] | None = None,
    created_utc: str | None = None,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    max_records_per_lane: int = 500,
    max_candidates: int = 4500,
    target_unique_candidates: int = 2000,
    stretch_unique_candidates: int = 3500,
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
    prior_index = _load_prior_index(prior_payloads or [])
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
                    "diversity_bin": lane["diversity_bin"],
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
                    "diversity_bin": lane["diversity_bin"],
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
                "diversity_bin": lane["diversity_bin"],
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
            _apply_near_orphan_diversity_policy(
                candidate,
                lane=lane,
                prior_duplicate=prior_duplicate,
            )
        )
        fetch_failures.extend(rhea_failures)

    terminal_counts = Counter(row["terminal_state"] for row in rows)
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    diversity_counts: dict[str, Counter[str]] = defaultdict(Counter)
    boundary_counts: dict[str, Counter[str]] = defaultdict(Counter)
    materialization_counts = Counter(row["materialization_bucket"] for row in rows)
    for row in rows:
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
        diversity_counts[row["diversity_bin"]][row["terminal_state"]] += 1
        boundary_counts[row["boundary_class"]][row["terminal_state"]] += 1

    duplicate_count = terminal_counts.get("blocked_duplicate_or_current_registry_conflict", 0)
    import_ready_count = terminal_counts.get("import_ready_preview", 0)
    provisional_count = terminal_counts.get(
        "provisional_external_countable_preflight_candidate", 0
    )
    repair_count = sum(terminal_counts.get(state, 0) for state in REPAIR_TERMINAL_STATES)
    reject_count = terminal_counts.get("reject/OOS_preserve_signal", 0)
    near_orphan_count = sum(1 for row in rows if row.get("near_orphan_signal"))
    no_structure_count = sum(
        1
        for row in rows
        if row.get("no_structure_or_no_reliable_structure_signal")
    )
    oos_hard_negative_count = sum(
        1
        for row in rows
        if row.get("oos_hard_negative_signal")
        or row.get("fold_confounded_negative_signal")
        or row.get("cofactor_confounded_non_target_signal")
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
        "all_rows_have_diversity_bin": all(row.get("diversity_bin") for row in rows),
        "all_rows_have_materialization_bucket": all(
            row.get("materialization_bucket") for row in rows
        ),
        "coordinate_missing_rows_have_explicit_no_structure_route": all(
            row.get("no_structure_route", {}).get(
                "explicit_no_structure_or_provenance_route"
            )
            for row in rows
            if row.get("coordinate_source_status") == "coordinate_provenance_missing"
        ),
        "candidate_count_matches_terminal_counts": len(rows)
        == sum(terminal_counts.values()),
        "target_2000_unique_non_duplicate_candidates_met": unique_non_duplicate_count
        >= target_unique_candidates,
        "production_registry_edit_count": 0,
    }
    validation_checks["stretch_unique_non_duplicate_candidates_met"] = (
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
            "mission": "targeted_external_scaleout_for_near_orphan_diversity",
            "rationale": (
                "Dense structural neighborhoods cannot prove the atlas north star. "
                "This shard therefore targets reviewed sparse-family, near-orphan, "
                "no-reliable-structure, OOS hard-negative, fold-confounded, "
                "cofactor-confounded non-target, terpene, lyase, isomerase, "
                "transferase, and ligase/synthetase rows that force abstention "
                "or explicit family review rather than nearest-neighbor transfer."
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
                "not an explicit OOS/fold/cofactor-confounded hard-negative lane",
                "not a near-orphan/no-reliable-structure provisional lane",
            ],
            "no_structure_route": (
                "Rows lacking AFDB/PDB provenance are preserved with explicit "
                "no-structure routing and are not silently discarded."
            ),
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
            "provisional_external_countable_preflight_candidate_rows": provisional_count,
            "repair_or_materialization_candidate_rows": repair_count,
            "reject_oos_preserve_signal_rows": reject_count,
            "near_orphan_signal_rows": near_orphan_count,
            "no_structure_or_no_reliable_structure_rows": no_structure_count,
            "oos_hard_negative_or_confounded_rows": oos_hard_negative_count,
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
        "diversity_bin_terminal_state_counts": {
            diversity_bin: dict(sorted(counts.items()))
            for diversity_bin, counts in sorted(diversity_counts.items())
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
            "no_structure_rows_routed_explicitly": True,
            "oos_and_hard_negative_signal_preserved": True,
        },
    }


def _load_prior_index(prior_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    from .external_scaleout_redox_cofactor_confounded import _prior_index_from_payloads

    return _prior_index_from_payloads(prior_payloads)


def build_external_scaleout_near_orphan_diversity_import_ready_preview(
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
            "diversity_bin": row["diversity_bin"],
            "boundary_class": row["boundary_class"],
            "boundary_role": row["boundary_role"],
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
            "mechanism_or_cofactor_feature_groups": row[
                "mechanism_or_cofactor_feature_groups"
            ],
            "near_orphan_signal": row["near_orphan_signal"],
            "no_structure_route": row["no_structure_route"],
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


def render_external_scaleout_near_orphan_diversity_report(
    artifact: dict[str, Any],
) -> str:
    counts = artifact["counts"]
    lines = [
        "# External Scaleout Shard - Near-Orphan Diversity current702",
        "",
        "Read-only targeted external scaleout over reviewed Swiss-Prot rows. "
        "The shard targets sparse, no-reliable-structure, OOS, fold-confounded, "
        "and diverse mechanism rows instead of nearest-neighbor expansion.",
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
        f"- Stretch met: `{artifact['validation_checks']['stretch_unique_non_duplicate_candidates_met']}`",
        f"- Import-ready preview rows: `{counts['import_ready_preview_rows']}`",
        f"- Provisional rows: `{counts['provisional_external_countable_preflight_candidate_rows']}`",
        f"- Repair/materialization candidate rows: `{counts['repair_or_materialization_candidate_rows']}`",
        f"- Reject/OOS preserve-signal rows: `{counts['reject_oos_preserve_signal_rows']}`",
        f"- Near-orphan signal rows: `{counts['near_orphan_signal_rows']}`",
        f"- No-structure/no-reliable-structure rows: `{counts['no_structure_or_no_reliable_structure_rows']}`",
        f"- OOS/fold/cofactor hard-negative rows: `{counts['oos_hard_negative_or_confounded_rows']}`",
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
            "## Diversity Bins",
            "",
            "| diversity bin | terminal counts |",
            "| --- | --- |",
        ]
    )
    for diversity_bin, terminal_counts in artifact[
        "diversity_bin_terminal_state_counts"
    ].items():
        lines.append(f"| `{diversity_bin}` | `{terminal_counts}` |")

    lines.extend(
        [
            "",
            "## Materialization And Provenance Blockers",
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
            "| lane | diversity bin | boundary role | fetched | unique queued | status |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for lane in artifact["lane_summaries"]:
        lines.append(
            f"| `{lane['lane_id']}` | `{lane['diversity_bin']}` | "
            f"`{lane['boundary_role']}` | {lane['fetched_record_count']} | "
            f"{lane['unique_candidate_count']} | {lane['status']} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Matrix Sample",
            "",
            "| candidate | bin | terminal state | locators | coordinate | groups | next action |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in artifact["rows"][:120]:
        groups = ",".join(row.get("mechanism_or_cofactor_feature_groups", [])) or "none"
        action = str(row["exact_next_action"]).replace("|", "\\|")
        lines.append(
            f"| `{row['candidate_id']}` | `{row['diversity_bin']}` | "
            f"`{row['terminal_state']}` | {row['exact_residue_locator_count']} | "
            f"{row['coordinate_source_status']} | {groups} | {action} |"
        )

    lines.extend(
        [
            "",
            "## Blockers",
            "",
            "- `source_preflight_provisional`: family-policy and structural duplicate "
            "review required before import-ready promotion.",
            "- `repairable_locator_blocker`: exact residue locator or reaction/locator "
            "repair required before review.",
            "- `repairable_coordinate_blocker`: AFDB/PDB coordinate provenance missing "
            "for otherwise useful locator evidence.",
            "- `hard_materialization_or_source_blocker`: source entry retrieval, "
            "coordinate provenance, or no-reliable-structure policy is unresolved.",
            "- `reject_oos_or_confounded_signal`: preserved hard-negative signal only.",
            "",
            "## Next Mechanical Continuation",
            "",
            "- Run current-countable structural duplicate screens and label-factory "
            "review only on `import_ready_preview` rows.",
            "- For provisional near-orphan/no-reliable-structure rows, decide the "
            "family policy before any import-ready promotion.",
            "- Retry UniProt entry materialization for hard-blocked rows before "
            "treating them as terminal no-structure evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_external_scaleout_near_orphan_diversity_shard(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    import_ready_preview_path: Path | None = DEFAULT_IMPORT_READY_PREVIEW_PATH,
    created_utc: str | None = None,
    max_records_per_lane: int = 500,
    max_candidates: int = 4500,
    target_unique_candidates: int = 2000,
    stretch_unique_candidates: int = 3500,
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
    artifact = build_external_scaleout_near_orphan_diversity_shard(
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
            render_external_scaleout_near_orphan_diversity_report(artifact),
            encoding="utf-8",
        )
    if (
        import_ready_preview_path is not None
        and artifact["counts"]["import_ready_preview_rows"] > 0
    ):
        preview = build_external_scaleout_near_orphan_diversity_import_ready_preview(
            artifact
        )
        preview["source_artifacts"] = {
            "external_scaleout_shard_near_orphan_diversity": _source_record(out_path)
        }
        import_ready_preview_path.parent.mkdir(parents=True, exist_ok=True)
        import_ready_preview_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    return artifact
