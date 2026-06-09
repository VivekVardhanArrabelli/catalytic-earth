from __future__ import annotations

import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query
from .external_scaleout_redox_cofactor_confounded import (
    DEFAULT_PRIOR_ARTIFACT_GLOBS,
    DEFAULT_PRIOR_GIT_ARTIFACTS,
    _load_prior_payloads,
    _prior_duplicate_status,
    _prior_index_from_payloads,
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


ARTIFACT_ID = "v3_external_bulk_ingestion_scaleout_wave2_current702_20260609"
PROVISIONAL_IMPORT_PREVIEW_ARTIFACT_ID = (
    "v3_external_bulk_ingestion_scaleout_wave2_provisional_import_preview_"
    "current702_20260609"
)
SCHEMA_VERSION = "v3.external_bulk_ingestion_scaleout_wave2"
PROVISIONAL_IMPORT_PREVIEW_SCHEMA_VERSION = (
    "v3.external_bulk_ingestion_scaleout_wave2_provisional_import_preview"
)

DEFAULT_OUT_PATH = Path(
    "artifacts/v3_external_bulk_ingestion_scaleout_wave2_current702_20260609.json"
)
DEFAULT_PREVIEW_PATH = Path(
    "artifacts/"
    "v3_external_bulk_ingestion_scaleout_wave2_provisional_import_preview_"
    "current702_20260609.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/external_bulk_ingestion_scaleout_wave2_current702_20260609.md"
)
DEFAULT_CURRENT_MANIFEST_PATH = Path(
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_LABEL_REGISTRY_PATH = Path("data/registries/curated_mechanism_labels.json")

TERMINAL_STATES = (
    "provisional_external_countable_preflight_candidate",
    "locator_ready_candidate",
    "coordinate_ready_pending_locator",
    "locator_repair_candidate",
    "coordinate_repair_candidate",
    "review_only_evidence",
    "reject/OOS_preserve_signal",
    "blocked_duplicate_or_current_registry_conflict",
    "hard_blocked_with_next_action",
)

CONTROL_BOUNDARY_ROLES = {
    "cofactor_confounded_oos_negative",
    "fold_confounded_control",
    "adjacent_mechanism_control",
    "lyase_isomerase_amidase_deaminase_control",
}

DEFAULT_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "metal_hydrolase_zinc_metallo_ec3",
        "target_family_lane": "metal hydrolase",
        "wave2_lane_group": "metal_hydrolase",
        "review_story_lane": "metal hydrolase",
        "boundary_role": "source_candidate",
        "mechanism_axis_focus": "metal_activated_water_hydrolysis",
        "query": (
            "(reviewed:true) AND (ec:3.*) AND "
            "((protein_name:metallo) OR (protein_name:zinc) OR "
            "(protein_name:metal) OR (cc_cofactor:zinc))"
        ),
    },
    {
        "lane_id": "metal_hydrolase_amidase_peptidase_boundary",
        "target_family_lane": "metal hydrolase amidase/peptidase boundary",
        "wave2_lane_group": "metal_hydrolase",
        "review_story_lane": "metal hydrolase",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "metal_hydrolase_vs_serine_cysteine_hydrolase",
        "query": (
            "(reviewed:true) AND ((protein_name:amidase) OR "
            "(protein_name:peptidase) OR (protein_name:protease)) AND "
            "((protein_name:metallo) OR (cc_cofactor:zinc) OR (ec:3.4.*))"
        ),
    },
    {
        "lane_id": "metal_hydrolase_manganese_magnesium_controls",
        "target_family_lane": "metal hydrolase Mg/Mn controls",
        "wave2_lane_group": "metal_hydrolase",
        "review_story_lane": "metal hydrolase",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "divalent_metal_hydrolase_specificity",
        "query": (
            "(reviewed:true) AND (ec:3.*) AND "
            "((cc_cofactor:magnesium) OR (cc_cofactor:manganese) OR "
            "(protein_name:magnesium) OR (protein_name:manganese))"
        ),
    },
    {
        "lane_id": "phosphoryl_transfer_kinase_ec27",
        "target_family_lane": "phosphoryl transfer kinase-like",
        "wave2_lane_group": "phosphoryl_transfer",
        "review_story_lane": "phosphoryl transfer",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "atp_phosphoryl_transfer",
        "query": (
            "(reviewed:true) AND ((ec:2.7.*) OR "
            "(protein_name:kinase) OR (protein_name:phosphotransferase))"
        ),
    },
    {
        "lane_id": "phosphoryl_transfer_phosphatase_ec313",
        "target_family_lane": "phosphatase/phosphoryl hydrolase",
        "wave2_lane_group": "phosphoryl_transfer",
        "review_story_lane": "phosphoryl transfer",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "phosphoryl_hydrolysis_vs_transfer",
        "query": (
            "(reviewed:true) AND ((ec:3.1.3.*) OR "
            "(protein_name:phosphatase) OR (protein_name:phosphodiesterase))"
        ),
    },
    {
        "lane_id": "phosphoryl_transfer_nucleotide_enzyme_boundary",
        "target_family_lane": "nucleotide phosphoryl-transfer boundary",
        "wave2_lane_group": "phosphoryl_transfer",
        "review_story_lane": "phosphoryl transfer",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "nucleotide_substrate_role_confounding",
        "query": (
            "(reviewed:true) AND ((protein_name:nucleotide) OR "
            "(protein_name:ATP) OR (protein_name:GTP)) AND "
            "((protein_name:kinase) OR (protein_name:phosphatase) OR (ec:2.7.*))"
        ),
    },
    {
        "lane_id": "glycoside_hydrolase_ec32",
        "target_family_lane": "glycoside hydrolase",
        "wave2_lane_group": "glycoside_nucleoside",
        "review_story_lane": "glycoside/nucleoside",
        "boundary_role": "source_candidate",
        "mechanism_axis_focus": "glycosidic_bond_hydrolysis",
        "query": (
            "(reviewed:true) AND ((ec:3.2.*) OR "
            "(protein_name:glycosidase) OR (protein_name:glucosidase) OR "
            "(protein_name:xylanase))"
        ),
    },
    {
        "lane_id": "glycosyltransferase_ec24_boundary",
        "target_family_lane": "glycosyltransferase boundary",
        "wave2_lane_group": "glycoside_nucleoside",
        "review_story_lane": "glycoside/nucleoside",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "glycosidic_transfer_vs_hydrolysis",
        "query": (
            "(reviewed:true) AND ((ec:2.4.*) OR "
            "(protein_name:glycosyltransferase) OR (protein_name:transferase))"
        ),
    },
    {
        "lane_id": "nucleoside_nucleotide_hydrolase_boundary",
        "target_family_lane": "nucleoside/nucleotide hydrolase boundary",
        "wave2_lane_group": "glycoside_nucleoside",
        "review_story_lane": "glycoside/nucleoside",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "nucleosidic_bond_and_base_hydrolysis",
        "query": (
            "(reviewed:true) AND ((protein_name:nucleosidase) OR "
            "(protein_name:nucleotidase) OR (protein_name:purine) OR "
            "(protein_name:pyrimidine) OR (ec:3.2.2.*))"
        ),
    },
    {
        "lane_id": "redox_oxygenase_ec114_ec113",
        "target_family_lane": "oxygenase redox",
        "wave2_lane_group": "redox_cofactor_confounded",
        "review_story_lane": "redox/cofactor-confounded",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "oxygen_transfer_vs_redox",
        "query": (
            "(reviewed:true) AND ((ec:1.14.*) OR (ec:1.13.*) OR "
            "(protein_name:monooxygenase) OR (protein_name:dioxygenase))"
        ),
    },
    {
        "lane_id": "redox_sulfur_oxidoreductase_ec18",
        "target_family_lane": "sulfur oxidoreductase",
        "wave2_lane_group": "redox_cofactor_confounded",
        "review_story_lane": "redox/cofactor-confounded",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "sulfur_redox_and_metal_cofactor_boundary",
        "query": (
            "(reviewed:true) AND ((ec:1.8.*) OR (protein_name:sulfite) OR "
            "(protein_name:sulfur) OR (protein_name:thiosulfate))"
        ),
    },
    {
        "lane_id": "redox_dehydrogenase_reductase_oos",
        "target_family_lane": "dehydrogenase/reductase OOS controls",
        "wave2_lane_group": "redox_cofactor_confounded",
        "review_story_lane": "redox/cofactor-confounded",
        "boundary_role": "cofactor_confounded_oos_negative",
        "mechanism_axis_focus": "nad_flavin_redox_not_oxygen_transfer",
        "query": (
            "(reviewed:true) AND ((protein_name:dehydrogenase) OR "
            "(protein_name:reductase) OR (ec:1.3.*) OR (ec:1.5.*) OR (ec:1.6.*))"
        ),
    },
    {
        "lane_id": "plp_broad_pyridoxal",
        "target_family_lane": "PLP broad cofactor context",
        "wave2_lane_group": "plp_radical_cobalamin",
        "review_story_lane": "PLP/radical/cobalamin",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "plp_schiff_base_proton_transfer",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate") OR (protein_name:aminotransferase) OR '
            "(protein_name:decarboxylase))"
        ),
    },
    {
        "lane_id": "plp_lyase_racemase_boundary",
        "target_family_lane": "PLP lyase/racemase boundary",
        "wave2_lane_group": "plp_radical_cobalamin",
        "review_story_lane": "PLP/radical/cobalamin",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "plp_beta_elimination_and_stereochemistry",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR '
            '(keyword:"Pyridoxal phosphate")) AND '
            "((protein_name:lyase) OR (protein_name:racemase) OR "
            "(protein_name:epimerase) OR (ec:4.3.*) OR (ec:5.1.1.*))"
        ),
    },
    {
        "lane_id": "radical_sam_iron_sulfur",
        "target_family_lane": "radical SAM iron-sulfur",
        "wave2_lane_group": "plp_radical_cobalamin",
        "review_story_lane": "PLP/radical/cobalamin",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "radical_sam_sf4_electron_transfer",
        "query": (
            '(reviewed:true) AND ((protein_name:"radical SAM") OR '
            '(keyword:"S-adenosyl-L-methionine")) AND '
            '((keyword:"Iron-sulfur") OR (protein_name:radical))'
        ),
    },
    {
        "lane_id": "cobalamin_b12_radical",
        "target_family_lane": "cobalamin/B12 radical enzymes",
        "wave2_lane_group": "plp_radical_cobalamin",
        "review_story_lane": "PLP/radical/cobalamin",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "adenosylcobalamin_radical_rearrangement",
        "query": (
            '(reviewed:true) AND ((cc_cofactor:cobalamin) OR '
            "(keyword:Cobalamin) OR (protein_name:cobalamin) OR "
            '(protein_name:"vitamin B12") OR (protein_name:adenosylcobalamin))'
        ),
    },
    {
        "lane_id": "near_orphan_uncharacterized_reviewed",
        "target_family_lane": "near-orphan reviewed proteins",
        "wave2_lane_group": "near_orphan_no_structure_fold_confounded",
        "review_story_lane": "near-orphan/no-structure/OOS/fold-confounded",
        "boundary_role": "near_orphan_review",
        "mechanism_axis_focus": "low_annotation_reviewed_candidate_triage",
        "query": (
            "(reviewed:true) AND ((protein_name:uncharacterized) OR "
            "(protein_name:hypothetical) OR (annotation_score:1))"
        ),
    },
    {
        "lane_id": "no_reliable_structure_coordinate_missing",
        "target_family_lane": "no reliable structure pressure",
        "wave2_lane_group": "near_orphan_no_structure_fold_confounded",
        "review_story_lane": "near-orphan/no-structure/OOS/fold-confounded",
        "boundary_role": "near_orphan_review",
        "mechanism_axis_focus": "coordinate_absence_and_locator_gap_pressure",
        "query": (
            "(reviewed:true) AND ((protein_name:enzyme) OR (ec:*)) "
            "NOT (database:pdb) NOT (database:alphafolddb)"
        ),
    },
    {
        "lane_id": "fold_confounded_rossmann_nad_controls",
        "target_family_lane": "Rossmann/NAD fold-confounded controls",
        "wave2_lane_group": "near_orphan_no_structure_fold_confounded",
        "review_story_lane": "near-orphan/no-structure/OOS/fold-confounded",
        "boundary_role": "fold_confounded_control",
        "mechanism_axis_focus": "fold_similarity_not_mechanism_identity",
        "query": (
            "(reviewed:true) AND ((keyword:NAD) OR (cc_cofactor:NAD) OR "
            "(protein_name:dehydrogenase)) AND (protein_name:domain)"
        ),
    },
    {
        "lane_id": "fmo_flavin_monooxygenase_boundary",
        "target_family_lane": "FMO/flavin monooxygenase boundary",
        "wave2_lane_group": "fmo_heme_fe_s_flavin_boundary",
        "review_story_lane": "FMO/heme/Fe-S/flavin boundary",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "flavin_oxygen_transfer_vs_redox",
        "query": (
            "(reviewed:true) AND ((protein_name:monooxygenase) OR "
            "(protein_name:FMO)) AND ((cc_cofactor:FAD) OR (cc_cofactor:FMN) OR "
            "(keyword:Flavoprotein))"
        ),
    },
    {
        "lane_id": "heme_peroxidase_oxidase_boundary",
        "target_family_lane": "heme peroxidase/oxidase boundary",
        "wave2_lane_group": "fmo_heme_fe_s_flavin_boundary",
        "review_story_lane": "FMO/heme/Fe-S/flavin boundary",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "heme_oxygen_chemistry_boundary",
        "query": (
            "(reviewed:true) AND ((ec:1.11.1.*) OR "
            "(protein_name:peroxidase) OR (protein_name:oxidase) OR "
            "(cc_cofactor:heme) OR (keyword:Heme))"
        ),
    },
    {
        "lane_id": "fe_s_flavin_combined_boundary",
        "target_family_lane": "Fe-S/flavin combined boundary",
        "wave2_lane_group": "fmo_heme_fe_s_flavin_boundary",
        "review_story_lane": "FMO/heme/Fe-S/flavin boundary",
        "boundary_role": "boundary_review",
        "mechanism_axis_focus": "multi_cofactor_electron_transfer_boundary",
        "query": (
            '(reviewed:true) AND (((keyword:"Iron-sulfur") OR '
            "(protein_name:ferredoxin)) AND ((cc_cofactor:FAD) OR "
            "(cc_cofactor:FMN) OR (protein_name:flavoprotein)))"
        ),
    },
    {
        "lane_id": "flavin_dehydrogenase_boundary",
        "target_family_lane": "flavin dehydrogenase boundary",
        "wave2_lane_group": "fmo_heme_fe_s_flavin_boundary",
        "review_story_lane": "FMO/heme/Fe-S/flavin boundary",
        "boundary_role": "cofactor_confounded_oos_negative",
        "mechanism_axis_focus": "flavin_redox_not_fmo_primary",
        "query": (
            "(reviewed:true) AND ((protein_name:dehydrogenase) OR "
            "(protein_name:reductase)) AND ((cc_cofactor:FAD) OR "
            "(cc_cofactor:FMN) OR (keyword:Flavoprotein))"
        ),
    },
    {
        "lane_id": "lyase_ec4_controls",
        "target_family_lane": "lyase controls",
        "wave2_lane_group": "lyase_isomerase_amidase_deaminase_controls",
        "review_story_lane": "lyase/isomerase/amidase/deaminase controls",
        "boundary_role": "lyase_isomerase_amidase_deaminase_control",
        "mechanism_axis_focus": "non_hydrolytic_elimination_control",
        "query": (
            "(reviewed:true) AND ((ec:4.*) OR (protein_name:lyase) OR "
            "(protein_name:dehydratase) OR (protein_name:synthase))"
        ),
    },
    {
        "lane_id": "isomerase_ec5_controls",
        "target_family_lane": "isomerase controls",
        "wave2_lane_group": "lyase_isomerase_amidase_deaminase_controls",
        "review_story_lane": "lyase/isomerase/amidase/deaminase controls",
        "boundary_role": "lyase_isomerase_amidase_deaminase_control",
        "mechanism_axis_focus": "isomerization_without_net_transfer_control",
        "query": (
            "(reviewed:true) AND ((ec:5.*) OR (protein_name:isomerase) OR "
            "(protein_name:mutase) OR (protein_name:racemase) OR "
            "(protein_name:epimerase))"
        ),
    },
    {
        "lane_id": "amidase_deaminase_controls",
        "target_family_lane": "amidase/deaminase controls",
        "wave2_lane_group": "lyase_isomerase_amidase_deaminase_controls",
        "review_story_lane": "lyase/isomerase/amidase/deaminase controls",
        "boundary_role": "lyase_isomerase_amidase_deaminase_control",
        "mechanism_axis_focus": "amide_or_amine_hydrolysis_boundary_control",
        "query": (
            "(reviewed:true) AND ((protein_name:amidase) OR "
            "(protein_name:deaminase) OR (ec:3.5.1.*) OR (ec:3.5.4.*))"
        ),
    },
)


def _current_duplicate_status(
    *,
    accession: str,
    sequence_sha: str | None,
    current_index: dict[str, Any],
) -> dict[str, Any]:
    accession_entries = current_index["accession_to_entries"].get(accession, [])
    sequence_entries = (
        current_index["sequence_sha_to_entries"].get(sequence_sha, [])
        if sequence_sha
        else []
    )
    if accession_entries:
        status = "exact_current702_accession_overlap"
    elif sequence_entries:
        status = "exact_current702_sequence_sha_overlap"
    else:
        status = "no_exact_current702_accession_or_sequence_sha_overlap"
    return {
        "duplicate_or_current_registry_conflict": bool(
            accession_entries or sequence_entries
        ),
        "current_registry_conflict_status": status,
        "exact_accession_matched_current_entry_ids": accession_entries,
        "exact_sequence_sha256": sequence_sha,
        "exact_sequence_matched_current_entry_ids": sequence_entries,
        "structural_duplicate_screen_status": (
            "not_run_in_external_bulk_scaleout_wave2; required before production import"
        ),
    }


def _coordinate_summary(search_record: dict[str, Any]) -> dict[str, Any]:
    pdb_ids = sorted(str(item) for item in search_record.get("pdb_ids", []) or [] if item)
    alphafold_ids = sorted(
        str(item) for item in search_record.get("alphafold_ids", []) or [] if item
    )
    if pdb_ids:
        return {
            "coordinate_source_status": "experimental_pdb_coordinate_provenance_available",
            "coordinate_status": "experimental_pdb_coordinate_provenance_available",
            "coordinate_source": "PDB",
            "afdb_or_pdb_identifier": pdb_ids[0],
            "pdb_ids": pdb_ids,
            "alphafold_ids": alphafold_ids,
            "coordinate_mapping_status": "duplicate_row_not_materialized",
        }
    if alphafold_ids:
        return {
            "coordinate_source_status": "afdb_predicted_coordinate_provenance_available",
            "coordinate_status": "afdb_predicted_coordinate_provenance_available",
            "coordinate_source": "AlphaFoldDB",
            "afdb_or_pdb_identifier": f"AF-{alphafold_ids[0]}-F1",
            "pdb_ids": pdb_ids,
            "alphafold_ids": alphafold_ids,
            "coordinate_mapping_status": "duplicate_row_not_materialized",
        }
    return {
        "coordinate_source_status": "coordinate_provenance_missing",
        "coordinate_status": "coordinate_provenance_missing",
        "coordinate_source": None,
        "afdb_or_pdb_identifier": None,
        "pdb_ids": pdb_ids,
        "alphafold_ids": alphafold_ids,
        "coordinate_mapping_status": "coordinate_mapping_not_available",
    }


def _current_status_text(status: dict[str, Any]) -> str:
    return str(status.get("current_registry_conflict_status") or "")


def _prior_status_text(status: dict[str, Any]) -> str:
    return str(status.get("prior_external_conflict_status") or "")


def _duplicate_summary(
    current_status: dict[str, Any],
    prior_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "current702_status": _current_status_text(current_status),
        "prior_external_status": _prior_status_text(prior_status),
        "blocked_by_current_or_prior_duplicate": bool(
            current_status.get("duplicate_or_current_registry_conflict")
            or prior_status.get("duplicate_or_prior_external_conflict")
        ),
    }


def _source_retrieval_summary(fetch_failures: list[dict[str, Any]]) -> dict[str, Any]:
    by_source = Counter(str(item.get("source") or "unknown") for item in fetch_failures)
    by_lane = Counter(str(item.get("lane_id") or "unknown") for item in fetch_failures)
    return {
        "failure_count": len(fetch_failures),
        "failure_counts_by_source": dict(sorted(by_source.items())),
        "failure_counts_by_lane": dict(sorted(by_lane.items())),
        "api_failures_reported": bool(fetch_failures),
    }


def _source_blocker_row(
    *,
    lane: dict[str, str],
    search_record: dict[str, Any],
    search_metadata: dict[str, Any],
    created: str,
    error: Exception,
    current_status: dict[str, Any],
    prior_status: dict[str, Any],
) -> dict[str, Any]:
    accession = _clean_accession(search_record.get("accession"))
    coordinate = _coordinate_summary(search_record)
    return {
        "stable_candidate_key": f"external_bulk_scaleout_wave2:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "reviewed_status": search_record.get("reviewed"),
        "protein_name": search_record.get("protein_name"),
        "organism": search_record.get("organism"),
        "sequence_length": search_record.get("length"),
        "target_family_lane": lane["target_family_lane"],
        "lane_id": lane["lane_id"],
        "wave2_lane_group": lane["wave2_lane_group"],
        "review_story_lane": lane["review_story_lane"],
        "boundary_role": lane["boundary_role"],
        "mechanism_axis_focus": lane["mechanism_axis_focus"],
        "source_query": lane["query"],
        "source_evidence_features": [],
        "source_evidence_feature_count": 0,
        "source_evidence_codes": [],
        "residue_locators": [],
        "residue_locator_count": 0,
        "exact_residue_locator_count": 0,
        **coordinate,
        "rhea_ec_provenance": {
            "ec_numbers": search_record.get("ec_numbers", []) or [],
            "specific_ec_count": 0,
            "catalytic_activity_comment_count": 0,
            "rhea_records": [],
            "rhea_record_count": 0,
            "rhea_status": "entry_retrieval_failed",
        },
        "cofactor_provenance": [],
        "duplicate_current_registry_conflict_status": _current_status_text(
            current_status
        ),
        "duplicate_current_registry_conflict": current_status,
        "prior_external_duplicate_conflict": prior_status,
        "duplicate_status_summary": _duplicate_summary(current_status, prior_status),
        "source_hashes": {
            "source_query_sha256": _canonical_sha256(lane["query"]),
            "uniprot_search_row_sha256": _canonical_sha256(search_record),
        },
        "source_provenance": {
            "query_timestamp_utc": created,
            "source_query": lane["query"],
            "source_query_sha256": _canonical_sha256(lane["query"]),
            "uniprot_search_url": search_metadata.get("url"),
            "uniprot_entry_url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
        },
        "evidence_basis": {
            "reviewed_swiss_prot": False,
            "structured_feature_count": 0,
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
        "materialization_bucket": "source_retrieval_blocker",
        "review_story_tags": _review_story_tags(lane=lane, row=None),
        "exact_next_action": (
            "Retry UniProt entry materialization for this accession before locator, "
            "coordinate, family, or import-preview review."
        ),
        "guardrails": _guardrails(),
    }


def _duplicate_blocker_row(
    *,
    lane: dict[str, str],
    search_record: dict[str, Any],
    search_metadata: dict[str, Any],
    created: str,
    current_status: dict[str, Any],
    prior_status: dict[str, Any],
) -> dict[str, Any]:
    accession = _clean_accession(search_record.get("accession"))
    coordinate = _coordinate_summary(search_record)
    basis = (
        "exact_current702_accession_or_sequence_overlap"
        if current_status.get("duplicate_or_current_registry_conflict")
        else "exact_prior_external_artifact_or_branch_accession_or_sequence_overlap"
    )
    return {
        "stable_candidate_key": f"external_bulk_scaleout_wave2:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "reviewed_status": search_record.get("reviewed"),
        "protein_name": search_record.get("protein_name"),
        "organism": search_record.get("organism"),
        "sequence_length": search_record.get("length"),
        "target_family_lane": lane["target_family_lane"],
        "lane_id": lane["lane_id"],
        "wave2_lane_group": lane["wave2_lane_group"],
        "review_story_lane": lane["review_story_lane"],
        "boundary_role": lane["boundary_role"],
        "mechanism_axis_focus": lane["mechanism_axis_focus"],
        "source_query": lane["query"],
        "source_evidence_features": [],
        "source_evidence_feature_count": 0,
        "source_evidence_codes": [],
        "residue_locators": [],
        "residue_locator_count": 0,
        "exact_residue_locator_count": 0,
        **coordinate,
        "rhea_ec_provenance": {
            "ec_numbers": search_record.get("ec_numbers", []) or [],
            "specific_ec_count": 0,
            "catalytic_activity_comment_count": 0,
            "rhea_records": [],
            "rhea_record_count": 0,
            "rhea_status": "not_materialized_for_duplicate_conflict",
        },
        "cofactor_provenance": [],
        "duplicate_current_registry_conflict_status": _current_status_text(
            current_status
        ),
        "duplicate_current_registry_conflict": current_status,
        "prior_external_duplicate_conflict": prior_status,
        "duplicate_status_summary": _duplicate_summary(current_status, prior_status),
        "source_hashes": {
            "source_query_sha256": _canonical_sha256(lane["query"]),
            "uniprot_search_row_sha256": _canonical_sha256(search_record),
        },
        "source_provenance": {
            "query_timestamp_utc": created,
            "source_query": lane["query"],
            "source_query_sha256": _canonical_sha256(lane["query"]),
            "uniprot_search_url": search_metadata.get("url"),
            "uniprot_entry_url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
        },
        "evidence_basis": {
            "reviewed_swiss_prot": search_record.get("reviewed") == "reviewed",
            "structured_feature_count": 0,
            "duplicate_pre_materialization_short_circuit": True,
        },
        "blocker_basis": {
            "applicable": True,
            "terminal_route_basis": basis,
            "missing_preflight_requirements": [
                "no_current702_or_prior_external_accession_or_sequence_conflict"
            ],
            "duplicate_or_current_registry_conflict": current_status.get(
                "duplicate_or_current_registry_conflict"
            ),
            "duplicate_or_prior_external_conflict": prior_status.get(
                "duplicate_or_prior_external_conflict"
            ),
            "source_retrieval_blocker": False,
        },
        "terminal_state": "blocked_duplicate_or_current_registry_conflict",
        "terminal_route_basis": basis,
        "confidence_tier": "blocked",
        "materialization_bucket": "duplicate_or_current_conflict",
        "review_story_tags": _review_story_tags(lane=lane, row=None),
        "exact_next_action": (
            "Do not import; preserve only as duplicate/current/prior external "
            "conflict evidence for the Wave 2 review ledger."
        ),
        "guardrails": _guardrails(),
    }


def _text_blob(row: dict[str, Any] | None) -> str:
    if not row:
        return ""
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


def _review_story_tags(
    *,
    lane: dict[str, str],
    row: dict[str, Any] | None,
) -> list[str]:
    text = _text_blob(row)
    tags = {lane["wave2_lane_group"], lane["review_story_lane"], lane["boundary_role"]}
    token_tags = {
        "flavin": ("fad", "fmn", "flavin"),
        "heme": ("heme", "haem", "porphyrin"),
        "iron_sulfur": ("iron-sulfur", "fe-s", "sf4", "4fe-4s"),
        "plp": ("pyridoxal", "plp", "pyridoxamine"),
        "cobalamin": ("cobalamin", "vitamin b12", "adenosylcobalamin"),
        "sam": ("s-adenosyl", "adomet", "sam"),
        "metal": ("zinc", "magnesium", "manganese", "metal", "iron"),
        "phosphoryl": ("phosphate", "phosphoryl", "kinase", "phosphatase"),
        "glycoside": ("glycos", "nucleosid", "nucleotid"),
        "coordinate_missing": ("coordinate_provenance_missing",),
    }
    for tag, tokens in token_tags.items():
        if any(token in text for token in tokens):
            tags.add(tag)
    if row and row.get("coordinate_source_status") == "coordinate_provenance_missing":
        tags.add("coordinate_missing")
    return sorted(tags)


def _materialization_bucket(row: dict[str, Any]) -> str:
    state = row["terminal_state"]
    if state == "provisional_external_countable_preflight_candidate":
        return "provisional_import_preview_preflight"
    if state == "locator_ready_candidate":
        return "reaction_or_family_review_pending"
    if state in {"coordinate_ready_pending_locator", "locator_repair_candidate"}:
        return "locator_repair_or_sourcing"
    if state == "coordinate_repair_candidate":
        return "coordinate_repair"
    if state == "blocked_duplicate_or_current_registry_conflict":
        return "duplicate_or_current_conflict"
    if state == "reject/OOS_preserve_signal":
        return "oos_or_control_preserve_signal"
    if state == "hard_blocked_with_next_action":
        return "hard_source_or_materialization_blocker"
    return "review_only_evidence"


def _guardrails() -> dict[str, bool]:
    return {
        "external_bulk_scaleout_wave2_discovery_preflight_only": True,
        "label_import_performed": False,
        "production_registry_edited": False,
        "production_import_edited": False,
        "ontology_edited": False,
        "heldout_split_or_threshold_edited": False,
        "model_weights_edited": False,
        "coordinate_downloads_performed": False,
        "ec_rhea_names_and_source_ids_provenance_only": True,
    }


def _apply_wave2_policy(
    *,
    row: dict[str, Any],
    lane: dict[str, str],
    prior_status: dict[str, Any],
) -> dict[str, Any]:
    candidate = json.loads(json.dumps(row))
    accession = candidate["accession"]
    current_status = candidate["duplicate_current_registry_conflict"]
    current_conflict = bool(current_status.get("duplicate_or_current_registry_conflict"))
    prior_conflict = bool(prior_status.get("duplicate_or_prior_external_conflict"))

    candidate.update(
        {
            "stable_candidate_key": f"external_bulk_scaleout_wave2:uniprot:{accession}",
            "wave2_lane_group": lane["wave2_lane_group"],
            "review_story_lane": lane["review_story_lane"],
            "boundary_role": lane["boundary_role"],
            "mechanism_axis_focus": lane["mechanism_axis_focus"],
            "prior_external_duplicate_conflict": prior_status,
            "duplicate_status_summary": _duplicate_summary(current_status, prior_status),
            "terminal_state_original_from_source_route": candidate["terminal_state"],
        }
    )

    blocker = candidate.setdefault("blocker_basis", {})
    blocker["prior_external_conflict"] = prior_status
    if current_conflict or prior_conflict:
        candidate["terminal_state"] = "blocked_duplicate_or_current_registry_conflict"
        candidate["terminal_route_basis"] = (
            "exact_current702_or_prior_external_accession_or_sequence_overlap"
        )
        candidate["confidence_tier"] = "blocked"
        candidate["exact_next_action"] = (
            "Do not import; preserve only as current/prior duplicate-conflict evidence."
        )
        blocker["applicable"] = True
        blocker["terminal_route_basis"] = candidate["terminal_route_basis"]
        blocker.setdefault("missing_preflight_requirements", [])
        if (
            "no_current702_or_prior_external_accession_or_sequence_conflict"
            not in blocker["missing_preflight_requirements"]
        ):
            blocker["missing_preflight_requirements"].append(
                "no_current702_or_prior_external_accession_or_sequence_conflict"
            )
    elif lane["boundary_role"] in CONTROL_BOUNDARY_ROLES:
        candidate["terminal_state"] = "reject/OOS_preserve_signal"
        candidate["terminal_route_basis"] = (
            f"wave2_{lane['boundary_role']}_preserved_as_review_control"
        )
        candidate["confidence_tier"] = "oos_or_control_signal"
        candidate["exact_next_action"] = (
            "Preserve as Wave 2 OOS/control signal; do not promote without explicit "
            "human family decision and a separate authorized import path."
        )
        blocker["applicable"] = True
        blocker["terminal_route_basis"] = candidate["terminal_route_basis"]
    elif candidate["terminal_state"] == "external_countable_preflight_candidate":
        candidate["terminal_state"] = "provisional_external_countable_preflight_candidate"
        candidate["terminal_route_basis"] = (
            "wave2_reviewed_exact_locator_coordinate_and_rhea_or_specific_ec_preflight_clear"
        )
        candidate["exact_next_action"] = (
            "Stage only in the Wave 2 provisional import preview; still requires "
            "source-free structural duplicate screening, label-factory review, "
            "explicit expert decision, and production registry-change authorization."
        )
        blocker["applicable"] = True
        blocker["terminal_route_basis"] = candidate["terminal_route_basis"]
        blocker["missing_preflight_requirements"] = [
            "source_free_structural_duplicate_screen",
            "label_factory_gate_and_explicit_review_decision",
            "production_registry_change_authorization",
        ]
    elif candidate["terminal_state"] == "review_only_evidence":
        candidate["exact_next_action"] = (
            "Preserve as review-only Wave 2 evidence; fill the smallest missing "
            "locator, coordinate, reaction, or family-decision gate before preview."
        )

    candidate["review_story_tags"] = _review_story_tags(lane=lane, row=candidate)
    candidate["materialization_bucket"] = _materialization_bucket(candidate)
    candidate["guardrails"] = {**candidate.get("guardrails", {}), **_guardrails()}
    return candidate


def build_external_bulk_scaleout_wave2(
    *,
    current_manifest_payload: dict[str, Any],
    label_registry_payload: list[dict[str, Any]],
    prior_payloads: list[dict[str, Any]] | None = None,
    prior_source_records: list[dict[str, Any]] | None = None,
    prior_load_failures: list[dict[str, Any]] | None = None,
    created_utc: str | None = None,
    lane_queries: tuple[dict[str, str], ...] = DEFAULT_LANE_QUERIES,
    max_records_per_query: int = 250,
    max_pages_per_query: int = 2,
    max_candidates: int = 9000,
    max_candidates_per_lane: int | None = 360,
    target_unique_non_duplicate_candidates: int = 2500,
    entry_fetch_workers: int = 16,
    query_fetcher: Callable[[str, int, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
    fetch_rhea_fallback: bool = False,
    max_reactions_per_ec: int = 1,
) -> dict[str, Any]:
    if max_records_per_query < 1 or max_records_per_query > 500:
        raise ValueError("max_records_per_query must be between 1 and 500")
    if max_pages_per_query < 1 or max_pages_per_query > 20:
        raise ValueError("max_pages_per_query must be between 1 and 20")
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    if max_candidates_per_lane is not None and max_candidates_per_lane < 1:
        raise ValueError("max_candidates_per_lane must be positive when set")
    if target_unique_non_duplicate_candidates < 1:
        raise ValueError("target_unique_non_duplicate_candidates must be positive")
    if entry_fetch_workers < 1 or entry_fetch_workers > 32:
        raise ValueError("entry_fetch_workers must be between 1 and 32")

    created = created_utc or _utc_now_iso()
    current_index = _current_reference_index(
        current_manifest_payload, label_registry_payload
    )
    prior_index = _prior_index_from_payloads(prior_payloads or [])
    lane_cap = max_candidates_per_lane or max(1, max_candidates // len(lane_queries))

    rows: list[dict[str, Any]] = []
    queued: list[
        tuple[dict[str, str], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]
    ] = []
    lane_summaries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = list(prior_load_failures or [])
    seen_accessions: set[str] = set()
    seen_sequence_shas: set[str] = set()
    total_search_rows_fetched = 0
    within_run_duplicate_rows_skipped = 0
    stopped_by_max_candidates = False

    for lane in lane_queries:
        if len(rows) + len(queued) >= max_candidates:
            stopped_by_max_candidates = True
            lane_summaries.append(_skipped_lane_summary(lane, "max_candidates_reached"))
            continue
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
            lane_summaries.append(_skipped_lane_summary(lane, "query_fetch_failed"))
            continue

        search_metadata = search_payload.get("metadata", {}) or {}
        fetched_records = [
            item
            for item in search_payload.get("records", []) or []
            if isinstance(item, dict)
        ]
        total_search_rows_fetched += len(fetched_records)
        unique_for_lane = 0
        duplicate_short_circuit_count = 0
        queued_for_lane = 0
        for search_record in fetched_records:
            accession = _clean_accession(search_record.get("accession"))
            sequence_sha = _sequence_sha256(search_record.get("sequence"))
            if not accession:
                continue
            if accession in seen_accessions or (
                sequence_sha and sequence_sha in seen_sequence_shas
            ):
                within_run_duplicate_rows_skipped += 1
                continue
            if unique_for_lane >= lane_cap:
                break
            if len(rows) + len(queued) >= max_candidates:
                stopped_by_max_candidates = True
                break
            seen_accessions.add(accession)
            if sequence_sha:
                seen_sequence_shas.add(sequence_sha)
            unique_for_lane += 1

            current_status = _current_duplicate_status(
                accession=accession,
                sequence_sha=sequence_sha,
                current_index=current_index,
            )
            prior_status = _prior_duplicate_status(
                accession=accession,
                sequence_sha=sequence_sha,
                prior_index=prior_index,
            )
            if current_status["duplicate_or_current_registry_conflict"] or prior_status[
                "duplicate_or_prior_external_conflict"
            ]:
                rows.append(
                    _duplicate_blocker_row(
                        lane=lane,
                        search_record=search_record,
                        search_metadata=search_metadata,
                        created=created,
                        current_status=current_status,
                        prior_status=prior_status,
                    )
                )
                duplicate_short_circuit_count += 1
                continue
            queued.append((lane, search_record, search_metadata, current_status, prior_status))
            queued_for_lane += 1

        lane_summaries.append(
            {
                "lane_id": lane["lane_id"],
                "target_family_lane": lane["target_family_lane"],
                "wave2_lane_group": lane["wave2_lane_group"],
                "review_story_lane": lane["review_story_lane"],
                "boundary_role": lane["boundary_role"],
                "mechanism_axis_focus": lane["mechanism_axis_focus"],
                "query": lane["query"],
                "fetched_record_count": len(fetched_records),
                "unique_candidate_count": unique_for_lane,
                "duplicate_short_circuit_count": duplicate_short_circuit_count,
                "queued_for_entry_materialization_count": queued_for_lane,
                "pages_fetched": search_metadata.get("pages_fetched", 1),
                "source_url": search_metadata.get("url"),
                "status": "query_fetched",
            }
        )

    def fetch_entry(
        item: tuple[
            dict[str, str],
            dict[str, Any],
            dict[str, Any],
            dict[str, Any],
            dict[str, Any],
        ]
    ) -> tuple[
        dict[str, str],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any] | None,
        Exception | None,
    ]:
        lane, search_record, search_metadata, current_status, prior_status = item
        accession = _clean_accession(search_record.get("accession"))
        try:
            return (
                lane,
                search_record,
                search_metadata,
                current_status,
                prior_status,
                entry_fetcher(accession),
                None,
            )
        except Exception as exc:  # pragma: no cover - live source failure path
            return lane, search_record, search_metadata, current_status, prior_status, None, exc

    with ThreadPoolExecutor(max_workers=entry_fetch_workers) as executor:
        entry_payloads = list(executor.map(fetch_entry, queued))

    for (
        lane,
        search_record,
        search_metadata,
        current_status,
        prior_status,
        entry_payload,
        entry_error,
    ) in entry_payloads:
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
            rows.append(
                _source_blocker_row(
                    lane=lane,
                    search_record=search_record,
                    search_metadata=search_metadata,
                    created=created,
                    error=entry_error,
                    current_status=current_status,
                    prior_status=prior_status,
                )
            )
            continue
        entry_record = (
            entry_payload.get("record", entry_payload)
            if isinstance(entry_payload, dict)
            else None
        )
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
                _source_blocker_row(
                    lane=lane,
                    search_record=search_record,
                    search_metadata=search_metadata,
                    created=created,
                    error=error,
                    current_status=current_status,
                    prior_status=prior_status,
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
        rows.append(
            _apply_wave2_policy(
                row=candidate,
                lane=lane,
                prior_status=prior_status,
            )
        )
        fetch_failures.extend(rhea_failures)

    rows.sort(key=lambda row: (row["wave2_lane_group"], row["lane_id"], row["accession"]))
    terminal_counts = Counter(row["terminal_state"] for row in rows)
    lane_group_counts: dict[str, Counter[str]] = defaultdict(Counter)
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    materialization_counts: Counter[str] = Counter()
    review_story_tag_counts: Counter[str] = Counter()
    current_duplicate_count = 0
    prior_duplicate_count = 0
    for row in rows:
        lane_group_counts[row["wave2_lane_group"]][row["terminal_state"]] += 1
        family_counts[row["target_family_lane"]][row["terminal_state"]] += 1
        materialization_counts[row["materialization_bucket"]] += 1
        review_story_tag_counts.update(row.get("review_story_tags", []))
        if row["duplicate_current_registry_conflict"].get(
            "duplicate_or_current_registry_conflict"
        ):
            current_duplicate_count += 1
        if row["prior_external_duplicate_conflict"].get(
            "duplicate_or_prior_external_conflict"
        ):
            prior_duplicate_count += 1

    duplicate_count = terminal_counts.get("blocked_duplicate_or_current_registry_conflict", 0)
    non_duplicate_count = len(rows) - duplicate_count
    preview_count = terminal_counts.get(
        "provisional_external_countable_preflight_candidate", 0
    )
    required_lane_groups = sorted({lane["wave2_lane_group"] for lane in lane_queries})
    lane_groups_with_rows = sorted({row["wave2_lane_group"] for row in rows})
    validation_checks = {
        "candidate_ids_unique_after_within_run_dedupe": len(
            {row["candidate_id"] for row in rows}
        )
        == len(rows),
        "candidate_count_matches_terminal_counts": len(rows)
        == sum(terminal_counts.values()),
        "all_terminal_states_known": all(
            row["terminal_state"] in TERMINAL_STATES for row in rows
        ),
        "all_rows_have_source_provenance": all(
            row.get("source_hashes") and row.get("source_provenance") for row in rows
        ),
        "all_rows_have_duplicate_status_summary": all(
            row.get("duplicate_status_summary") for row in rows
        ),
        "all_rows_have_review_story_tags": all(row.get("review_story_tags") for row in rows),
        "all_required_lane_groups_have_rows": set(required_lane_groups).issubset(
            set(lane_groups_with_rows)
        ),
        "target_unique_non_duplicate_candidates_met": non_duplicate_count
        >= target_unique_non_duplicate_candidates,
        "stretch_4000_unique_non_duplicate_candidates_met": non_duplicate_count
        >= 4000,
        "production_registry_edit_count": 0,
    }
    validation_checks["passed"] = all(
        value is True
        for key, value in validation_checks.items()
        if isinstance(value, bool)
        and key != "passed"
        and not key.startswith("stretch_")
    )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "source_scope": {
            "current_reference_scope": "current702",
            "primary_sources": [
                "UniProtKB/Swiss-Prot reviewed entries",
                "UniProt structured feature, cofactor, and catalytic activity records",
                "UniProt AFDB/PDB cross-reference coordinate provenance",
                "Rhea/EC provenance when present or explicitly fetched",
            ],
            "dedupe_scope": [
                "current702 accessions and sequence SHA256 values",
                "prior local external artifacts",
                "prior local scaleout artifacts",
                "completed external admission/scaleout branch artifacts",
                "within-run accession and sequence SHA256 dedupe",
            ],
            "mission": "broad_external_bulk_scaleout_wave2_discovery_admission_preflight_only",
            "rationale": (
                "Wave 2 broad scaleout prioritizes reviewed, mechanism-informative "
                "Swiss-Prot rows across hydrolase, phosphoryl-transfer, carbohydrate, "
                "redox/cofactor, PLP/radical/cobalamin, near-orphan/no-structure, "
                "FMO/heme/Fe-S/flavin boundary, and adjacent control lanes. Rows are "
                "review/admission-preflight candidates, not production labels."
            ),
            "production_surfaces_not_edited": [
                "curated mechanism registries",
                "imports",
                "ontologies",
                "heldout splits",
                "thresholds",
                "model weights",
            ],
        },
        "routing_policy": {
            "terminal_states": list(TERMINAL_STATES),
            "provisional_import_preview_gate": [
                "reviewed Swiss-Prot status",
                "no exact current702 accession or sequence SHA overlap",
                "no exact prior external/scaleout artifact accession or sequence SHA overlap",
                "at least one exact curated residue locator",
                "AFDB/PDB coordinate provenance available",
                "specific EC and Rhea-style reaction provenance available",
                "not an explicit OOS/control boundary lane",
            ],
            "production_import_rule": (
                "No production import is authorized. Preview rows require structural "
                "duplicate screening, label-factory gates, explicit expert decision, "
                "and a separate production registry-change authorization."
            ),
        },
        "counts": {
            "fetched_uniprot_search_records": total_search_rows_fetched,
            "candidate_rows": len(rows),
            "unique_candidates_after_within_run_dedupe": len(rows),
            "unique_non_duplicate_candidate_rows": non_duplicate_count,
            "target_unique_non_duplicate_candidates": target_unique_non_duplicate_candidates,
            "stretch_unique_non_duplicate_candidates": 4000,
            "provisional_import_preview_rows": preview_count,
            "duplicate_current_or_prior_conflict_rows": duplicate_count,
            "current702_duplicate_conflict_rows": current_duplicate_count,
            "prior_external_duplicate_conflict_rows": prior_duplicate_count,
            "oos_or_control_preserve_signal_rows": terminal_counts.get(
                "reject/OOS_preserve_signal", 0
            ),
            "api_failure_rows": len(fetch_failures),
            "within_run_duplicate_rows_skipped": within_run_duplicate_rows_skipped,
            "max_candidate_cap": max_candidates,
            "stopped_by_max_candidates": stopped_by_max_candidates,
        },
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "wave2_lane_group_terminal_state_counts": {
            group: dict(sorted(counts.items()))
            for group, counts in sorted(lane_group_counts.items())
        },
        "family_lane_terminal_state_counts": {
            family: dict(sorted(counts.items()))
            for family, counts in sorted(family_counts.items())
        },
        "materialization_bucket_counts": dict(sorted(materialization_counts.items())),
        "review_story_tag_counts": dict(sorted(review_story_tag_counts.items())),
        "required_lane_groups": required_lane_groups,
        "lane_groups_with_rows": lane_groups_with_rows,
        "lane_summaries": lane_summaries,
        "deduplication_summary": {
            **prior_index,
            "current_reference_accession_count": current_index[
                "current_reference_accession_count"
            ],
            "current_sequence_sha_count": current_index["current_sequence_sha_count"],
            "prior_source_records": prior_source_records or [],
            "prior_load_failure_count": len(prior_load_failures or []),
            "within_run_duplicate_rows_skipped": within_run_duplicate_rows_skipped,
        },
        "api_query_limits": {
            "max_records_per_query": max_records_per_query,
            "max_pages_per_query": max_pages_per_query,
            "max_candidates": max_candidates,
            "max_candidates_per_lane": lane_cap,
            "entry_fetch_workers": entry_fetch_workers,
            "fetch_rhea_fallback": fetch_rhea_fallback,
            "coordinate_downloads_performed": False,
        },
        "source_retrieval_summary": _source_retrieval_summary(fetch_failures),
        "fetch_failures": fetch_failures,
        "rows": rows,
        "validation_checks": validation_checks,
        "guardrails": _guardrails(),
    }


def _skipped_lane_summary(lane: dict[str, str], status: str) -> dict[str, Any]:
    return {
        "lane_id": lane["lane_id"],
        "target_family_lane": lane["target_family_lane"],
        "wave2_lane_group": lane["wave2_lane_group"],
        "review_story_lane": lane["review_story_lane"],
        "boundary_role": lane["boundary_role"],
        "mechanism_axis_focus": lane["mechanism_axis_focus"],
        "query": lane["query"],
        "fetched_record_count": 0,
        "unique_candidate_count": 0,
        "duplicate_short_circuit_count": 0,
        "queued_for_entry_materialization_count": 0,
        "pages_fetched": 0,
        "source_url": None,
        "status": status,
    }


def build_external_bulk_scaleout_wave2_provisional_import_preview(
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
            "wave2_lane_group": row["wave2_lane_group"],
            "review_story_lane": row["review_story_lane"],
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
            "review_story_tags": row["review_story_tags"],
            "duplicate_status_summary": row["duplicate_status_summary"],
            "source_hashes": row["source_hashes"],
            "source_provenance": row["source_provenance"],
            "evidence_basis": row["evidence_basis"],
            "blocker_basis": row["blocker_basis"],
            "provisional_import_preview": True,
            "ready_for_production_label_import": False,
            "remaining_required_before_import": [
                "source_free_structural_duplicate_screen",
                "label_factory_gate_and_explicit_review_decision",
                "expert_family_or_mechanism_accept_decision",
                "production_registry_change_authorization",
            ],
            "exact_next_action": row["exact_next_action"],
        }
        for row in artifact.get("rows", [])
        if row.get("terminal_state")
        == "provisional_external_countable_preflight_candidate"
    ]
    return {
        "artifact_id": PROVISIONAL_IMPORT_PREVIEW_ARTIFACT_ID,
        "schema_version": PROVISIONAL_IMPORT_PREVIEW_SCHEMA_VERSION,
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


def render_external_bulk_scaleout_wave2_report(artifact: dict[str, Any]) -> str:
    counts = artifact["counts"]
    lines = [
        "# External Bulk Scaleout Wave 2 - current702",
        "",
        "Read-only broad external discovery/admission-preflight artifact over "
        "reviewed Swiss-Prot/UniProt candidates. No production registry, import, "
        "ontology, heldout split, threshold, or model artifact was changed.",
        "",
        "## Summary",
        "",
        f"- Fetched UniProt search records: `{counts['fetched_uniprot_search_records']}`",
        f"- Candidate rows: `{counts['candidate_rows']}`",
        f"- Unique non-duplicate candidates: `{counts['unique_non_duplicate_candidate_rows']}`",
        f"- Target unique non-duplicate candidates: `{counts['target_unique_non_duplicate_candidates']}`",
        f"- Provisional import-preview rows: `{counts['provisional_import_preview_rows']}`",
        f"- OOS/control preserve-signal rows: `{counts['oos_or_control_preserve_signal_rows']}`",
        f"- Current/prior duplicate conflicts: `{counts['duplicate_current_or_prior_conflict_rows']}`",
        f"- API/source failure rows: `{counts['api_failure_rows']}`",
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
            "## Wave 2 Lane Group Counts",
            "",
            "| lane group | terminal counts |",
            "| --- | --- |",
        ]
    )
    for lane_group, terminal_counts in artifact[
        "wave2_lane_group_terminal_state_counts"
    ].items():
        lines.append(f"| `{lane_group}` | `{terminal_counts}` |")

    lines.extend(
        [
            "",
            "## API Failures And Dedupe",
            "",
            f"- Failure counts by source: `{artifact['source_retrieval_summary']['failure_counts_by_source']}`",
            f"- Prior artifact count indexed: `{artifact['deduplication_summary']['prior_artifact_count']}`",
            f"- Prior candidate rows indexed: `{artifact['deduplication_summary']['prior_candidate_row_count']}`",
            f"- Within-run duplicates skipped: `{counts['within_run_duplicate_rows_skipped']}`",
            "",
            "## Source Query Coverage",
            "",
            "| lane | group | fetched | unique | duplicate short-circuit | entry queued | status |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for lane in artifact["lane_summaries"]:
        lines.append(
            f"| `{lane['lane_id']}` | `{lane['wave2_lane_group']}` | "
            f"{lane['fetched_record_count']} | {lane['unique_candidate_count']} | "
            f"{lane['duplicate_short_circuit_count']} | "
            f"{lane['queued_for_entry_materialization_count']} | {lane['status']} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Matrix Sample",
            "",
            "| candidate | group | lane | terminal state | locators | coordinate | next action |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in artifact["rows"][:160]:
        action = str(row["exact_next_action"]).replace("|", "\\|")
        lines.append(
            f"| `{row['candidate_id']}` | `{row['wave2_lane_group']}` | "
            f"{row['target_family_lane']} | `{row['terminal_state']}` | "
            f"{row['exact_residue_locator_count']} | "
            f"{row['coordinate_source_status']} | {action} |"
        )

    lines.extend(
        [
            "",
            "## Next Mechanical Continuation",
            "",
            "- Run source-free structural duplicate screens and label-factory review "
            "on only the provisional import-preview rows.",
            "- Retry UniProt entry materialization for hard-blocked source rows before "
            "treating them as locator or coordinate candidates.",
            "- Continue Wave 2 by splitting the lowest-yield lane groups into "
            "subqueries after preserving current702/prior-external dedupe.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_external_bulk_scaleout_wave2(
    *,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    label_registry_path: Path = DEFAULT_LABEL_REGISTRY_PATH,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path | None = DEFAULT_REPORT_PATH,
    provisional_import_preview_path: Path | None = DEFAULT_PREVIEW_PATH,
    created_utc: str | None = None,
    max_records_per_query: int = 250,
    max_pages_per_query: int = 2,
    max_candidates: int = 9000,
    max_candidates_per_lane: int | None = 360,
    target_unique_non_duplicate_candidates: int = 2500,
    entry_fetch_workers: int = 16,
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
        DEFAULT_PREVIEW_PATH.resolve(),
    }
    if provisional_import_preview_path is not None:
        exclude_paths.add(provisional_import_preview_path.resolve())
    prior_payloads, prior_source_records, prior_load_failures = _load_prior_payloads(
        prior_artifact_paths=prior_artifact_paths or [],
        prior_artifact_globs=prior_artifact_globs,
        prior_git_artifacts=prior_git_artifacts,
        exclude_paths=exclude_paths,
    )
    artifact = build_external_bulk_scaleout_wave2(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=label_registry_payload,
        prior_payloads=prior_payloads,
        prior_source_records=prior_source_records,
        prior_load_failures=prior_load_failures,
        created_utc=created_utc,
        max_records_per_query=max_records_per_query,
        max_pages_per_query=max_pages_per_query,
        max_candidates=max_candidates,
        max_candidates_per_lane=max_candidates_per_lane,
        target_unique_non_duplicate_candidates=target_unique_non_duplicate_candidates,
        entry_fetch_workers=entry_fetch_workers,
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
            render_external_bulk_scaleout_wave2_report(artifact), encoding="utf-8"
        )
    if (
        provisional_import_preview_path is not None
        and artifact["counts"]["provisional_import_preview_rows"] > 0
    ):
        preview = build_external_bulk_scaleout_wave2_provisional_import_preview(
            artifact
        )
        preview["source_artifacts"] = {
            "external_bulk_scaleout_wave2": _source_record(out_path)
        }
        provisional_import_preview_path.parent.mkdir(parents=True, exist_ok=True)
        provisional_import_preview_path.write_text(
            json.dumps(preview, indent=2, sort_keys=True), encoding="utf-8"
        )
    return artifact
