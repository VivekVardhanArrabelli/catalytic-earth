from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from catalytic_earth.scaleout_metal_hydrolase_shard import (
    TERMINAL_STATES,
    _append_unique,
    _as_list,
    _canonical_sha256,
    _candidate_id,
    _merge_list,
    _read_json,
    _sort_key,
    _source_record,
)


ARTIFACT_ID = "v3_scaleout_radical_sam_cobalamin_shard_current702_20260608"
SCHEMA_VERSION = "v3.scaleout_radical_sam_cobalamin_shard"

DEFAULT_OUT_PATH = Path(
    "artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/scaleout_radical_sam_cobalamin_shard_current702_20260608.md"
)
DEFAULT_HANDOFF_PATH = Path(
    "work/handoff_radical_sam_cobalamin_shard_20260608.md"
)

DEFAULT_SOURCE_PATHS = {
    "targeted_expansion_factory_batch": Path(
        "artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json"
    ),
    "targeted_expansion_acquisition_conversion_screens": Path(
        "artifacts/"
        "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json"
    ),
    "radical_sam_locus_sidecar": Path(
        "artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json"
    ),
    "iron_sulfur_locus_sidecar": Path(
        "artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json"
    ),
    "cobalamin_locus_sidecar": Path(
        "artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json"
    ),
    "radical_sam_locus_schema_audit": Path(
        "artifacts/"
        "v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json"
    ),
    "iron_sulfur_locus_schema_audit": Path(
        "artifacts/"
        "v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json"
    ),
    "cobalamin_locus_schema_audit": Path(
        "artifacts/"
        "v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json"
    ),
    "radical_sam_minicampaign_freeze": Path(
        "artifacts/v3_prospective_external_radical_sam_minicampaign_freeze_20260521.json"
    ),
    "radical_sam_minicampaign_decision_packet": Path(
        "artifacts/v3_prospective_external_radical_sam_minicampaign_decision_packet_20260521.json"
    ),
    "radical_sam_minicampaign_baseline_comparison": Path(
        "artifacts/v3_radical_sam_minicampaign_baseline_comparison_20260521.json"
    ),
    "radical_sam_minicampaign_sequence_baseline": Path(
        "artifacts/v3_radical_sam_minicampaign_sequence_baseline_diagnostic_20260521.json"
    ),
    "cobalamin_radical_minicampaign_blocker_review": Path(
        "artifacts/v3_prospective_external_cobalamin_radical_minicampaign_blocker_review_20260521.json"
    ),
    "cobalamin_and_radical_rearrangement_panel": Path(
        "artifacts/"
        "v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json"
    ),
    "glycyl_radical_or_thiamine_radical_panel": Path(
        "artifacts/"
        "v3_family_panel_evidence_packet_glycyl_radical_or_thiamine_radical_lyase_current702_20260601.json"
    ),
    "glycyl_radical_readiness_packet": Path(
        "artifacts/"
        "v3_family_panel_high_value_glycyl_radical_readiness_packet_current702_20260601.json"
    ),
    "glycyl_radical_no_template_guardrail": Path(
        "artifacts/"
        "v3_family_panel_high_value_glycyl_radical_no_template_feature_guardrail_current702_20260601.json"
    ),
    "radical_sam_source_check_secondary_probe": Path(
        "artifacts/"
        "v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json"
    ),
    "coupled_plp_cobalamin_schema_decision": Path(
        "artifacts/"
        "v3_mcsa_positive_schema_decision_m_csa737_coupled_plp_cobalamin_proposal_20260524.json"
    ),
    "coupled_plp_cobalamin_expert_guidance": Path(
        "artifacts/"
        "v3_expert_guidance_amp_nontransfer_and_coupled_plp_cobalamin_20260524.json"
    ),
    "iron_sulfur_electron_flow_qualified_union": Path(
        "artifacts/"
        "v3_lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_current702_20260605.json"
    ),
    "iron_sulfur_electron_flow_support_subset": Path(
        "artifacts/"
        "v3_lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_current702_20260605.json"
    ),
    "iron_sulfur_electron_flow_tiny_tranche": Path(
        "artifacts/"
        "v3_lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_current702_20260605.json"
    ),
}

DEFAULT_FASTA_PATHS = {
    "radical_sam_minicampaign_sequence_fasta": Path(
        "artifacts/v3_radical_sam_minicampaign_sequence_baseline_external_20260521.fasta"
    )
}

STATE_PRIORITY = {
    "reject/OOS_preserve_signal": 0,
    "countable_candidate_preflight_only": 1,
    "blocked_family_decision": 2,
    "blocked_locator": 3,
    "blocked_coordinate": 4,
    "review_only_evidence": 5,
}

SUBFAMILY_PRIORITY = {
    "coupled_plp_adenosylcobalamin_aminomutase": 0,
    "cobalamin_radical_rearrangement": 1,
    "radical_sam_sf4_cx3cx2c_probe": 2,
    "radical_sam_sf4_copresence_probe": 3,
    "external_radical_sam_minicampaign": 4,
    "fe_s_radical_or_electron_flow_boundary": 5,
    "plp_sam_fe_s_coupled_boundary": 6,
    "cobalamin_context_boundary": 7,
    "methylcobalamin_not_radical_oos_control": 8,
    "sam_methyltransferase_near_oos_control": 9,
    "glycyl_radical_or_thiamine_radical_boundary": 10,
    "hard_near_ood_radical_cobalamin_sam_control": 20,
    "radical_sam_cobalamin_general_review_queue": 50,
}

TARGET_FINGERPRINTS = {
    "radical_sam_enzyme",
    "cobalamin_radical_rearrangement",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _new_candidate(candidate_id: str) -> dict[str, Any]:
    accession = candidate_id.split(":", 1)[1] if candidate_id.startswith("uniprot:") else None
    return {
        "candidate_id": candidate_id,
        "accession": accession,
        "display_names": [],
        "aliases": [],
        "candidate_roles": [],
        "state_votes": [],
        "subfamily_votes": [],
        "active_site_sources": [],
        "coordinate_sources": [],
        "cofactor_sources": [],
        "duplicate_screen_sources": [],
        "source_free_preflight_sources": [],
        "next_steps": [],
        "terminal_blockers": [],
        "source_hashes": {},
        "source_contributions": [],
    }


def _candidate(
    records: dict[str, dict[str, Any]], candidate_id: str
) -> dict[str, Any]:
    return records.setdefault(candidate_id, _new_candidate(candidate_id))


def _contribute(
    record: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
    source_row: dict[str, Any],
    contribution_role: str,
) -> None:
    record["source_hashes"][source_key] = source_record["sha256"]
    record["source_contributions"].append(
        {
            "source_key": source_key,
            "path": source_record["path"],
            "source_artifact_sha256": source_record["sha256"],
            "source_row_sha256": _canonical_sha256(source_row),
            "contribution_role": contribution_role,
            "terminal_hint": (
                source_row.get("terminal_state")
                or source_row.get("admission_state")
                or source_row.get("terminal_decision")
                or source_row.get("score_status")
                or source_row.get("sidecar_status")
                or source_row.get("evidence_role")
            ),
        }
    )


def _first_text(row: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return None


def _contains(text: str, *needles: str) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def _factory_terminal_state(row: dict[str, Any]) -> str:
    state = str(row.get("admission_state") or "")
    if state == "countable_candidate":
        return "countable_candidate_preflight_only"
    if state in TERMINAL_STATES:
        return state
    if state == "acquisition_needed":
        return "blocked_family_decision"
    return "review_only_evidence"


def _sidecar_terminal_state(row: dict[str, Any], kind: str) -> str:
    status = str(row.get("sidecar_status") or "")
    fingerprint = str(row.get("fingerprint_id") or "")
    if status == "unsupported_or_missing_geometry":
        return "blocked_coordinate"
    if "structure_wide" in status:
        return "blocked_locator"
    if fingerprint in TARGET_FINGERPRINTS:
        return "review_only_evidence"
    if status.startswith("no_"):
        return "reject/OOS_preserve_signal"
    if kind in {"radical_sam", "iron_sulfur", "cobalamin"}:
        return "review_only_evidence"
    return "review_only_evidence"


def _external_radical_sam_terminal_state(row: dict[str, Any]) -> str:
    decision = str(row.get("terminal_decision") or "")
    score_status = str(row.get("production_score_status") or row.get("score_status") or "")
    if "duplicate" in decision or "reject" in decision:
        return "reject/OOS_preserve_signal"
    if "geometry_missing" in score_status or "not_scored" in score_status:
        return "blocked_coordinate"
    if decision == "needs_review":
        return "blocked_family_decision"
    return "review_only_evidence"


def _panel_terminal_state(row: dict[str, Any]) -> str:
    status = str(row.get("predicted_geometry_status") or "")
    role = str(row.get("evidence_role") or "")
    entry_id = str(row.get("entry_id") or "")
    if status == "missing":
        return "blocked_coordinate"
    if "oos control" in role.lower() and not entry_id.startswith("secondary_probe::"):
        return "reject/OOS_preserve_signal"
    return "review_only_evidence"


def _infer_factory_subfamily(row: dict[str, Any]) -> str:
    text = " ".join(
        str(row.get(key, ""))
        for key in ("display_name", "rationale", "admission_route_basis")
    )
    cofactor_text = json.dumps(row.get("cofactor_or_metal_evidence") or {}).lower()
    fold_text = json.dumps(row.get("fold_tm_or_near_neighbor_signal") or {}).lower()
    if _contains(text, "cobalamin", "b12", "adenosylcobalamin") or "cobalamin" in cofactor_text:
        return "cobalamin_context_boundary"
    if _contains(text, "plp", "aminomutase") and _contains(
        text, "sam", "iron-sulfur", "fe-s"
    ):
        return "plp_sam_fe_s_coupled_boundary"
    if "sam" in cofactor_text and _contains(text, "methyltransferase", "methylase"):
        return "sam_methyltransferase_near_oos_control"
    if "radical_sam" in fold_text or "sam" in cofactor_text:
        return "radical_sam_sf4_cx3cx2c_probe"
    if _contains(cofactor_text, "fe-s", "iron", "sulfur", "sf4"):
        return "fe_s_radical_or_electron_flow_boundary"
    return "hard_near_ood_radical_cobalamin_sam_control"


def _infer_sidecar_subfamily(row: dict[str, Any], kind: str) -> str:
    fingerprint = str(row.get("fingerprint_id") or "")
    status = str(row.get("sidecar_status") or "")
    codes = {str(code) for code in _as_list(row.get("supporting_ligand_codes"))}
    if status.startswith("no_"):
        return "hard_near_ood_radical_cobalamin_sam_control"
    if fingerprint == "cobalamin_radical_rearrangement":
        return "cobalamin_radical_rearrangement"
    if fingerprint == "radical_sam_enzyme":
        return "radical_sam_sf4_cx3cx2c_probe"
    if fingerprint == "plp_dependent_enzyme" and kind in {"radical_sam", "iron_sulfur"}:
        return "plp_sam_fe_s_coupled_boundary"
    if kind == "cobalamin":
        if not row.get("radical_rearrangement_source_flag") and codes:
            return "methylcobalamin_not_radical_oos_control"
        return "cobalamin_context_boundary"
    if kind == "radical_sam":
        if row.get("sam_fe_s_copresence_status") == "proximal_sam_and_fe_s_context":
            return "radical_sam_sf4_copresence_probe"
        return "radical_sam_sf4_cx3cx2c_probe"
    if kind == "iron_sulfur":
        return "fe_s_radical_or_electron_flow_boundary"
    return "radical_sam_cobalamin_general_review_queue"


def _cofactor_signal_tokens(sources: list[dict[str, Any]]) -> list[str]:
    tokens: list[str] = []

    def add_value(value: Any) -> None:
        if value in (None, "", [], {}):
            return
        if isinstance(value, dict):
            for key in (
                "code",
                "ligand_code",
                "resn",
                "cofactor_locus",
                "motif_family",
                "motif_pattern",
            ):
                add_value(value.get(key))
            return
        if isinstance(value, list):
            for item in value:
                add_value(item)
            return
        tokens.append(str(value).lower())

    for source in sources:
        for key in (
            "supporting_ligand_codes",
            "supporting_structure_ligand_codes",
            "ligand_codes",
            "hetatms_in_structure",
            "cofactors_required",
            "cofactor_families",
            "cofactor_or_ligand_states",
            "proximal_ligands",
            "structure_ligands",
            "positive_contact_examples",
            "family_distance_examples",
            "b12_ligands",
            "motifs",
        ):
            add_value(source.get(key))
        copresence = str(source.get("sam_fe_s_copresence_status") or "")
        if copresence and copresence != "no_context_detected":
            add_value(copresence)
        if source.get("radical_sam_source_context_present"):
            add_value("radical_sam")
        if source.get("fe_s_or_sam_source_context_present"):
            add_value("sam fe-s")
        if source.get("adenosyl_or_methyl_context_flag"):
            add_value("adenosylcobalamin_or_methylcobalamin_context")
        if source.get("radical_rearrangement_source_flag"):
            add_value("cobalamin_radical_rearrangement_context")
        if source.get("cx3cx2c_motif_evidence_present") or source.get("motif_count", 0):
            add_value("cx3cx2c")
    return tokens


def _cofactor_flags_from_sources(sources: list[dict[str, Any]]) -> dict[str, bool]:
    tokens = _cofactor_signal_tokens(sources)
    text = " ".join(tokens)
    return {
        "sf4_or_fe_s_evidence_present": any(
            needle in text
            for needle in ("sf4", "fes", "f3s", "fs4", "fe-s", "iron_sulfur")
        ),
        "sam_or_adomet_evidence_present": any(
            needle in text for needle in ("sam", "adomet", "s-adenosyl", "ado-met")
        ),
        "cobalamin_or_adocbl_evidence_present": any(
            needle in text
            for needle in ("cobalamin", "adenosylcobalamin", "b12", "cob", "adocbl")
        ),
        "plp_evidence_present": any(
            needle in text for needle in ("plp", "pyridoxal", "llp")
        ),
        "cx3cx2c_motif_evidence_present": "cx3cx2c" in text
        or "cxxxcxxc" in text,
    }


def _merge_factory_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    if row.get("family_axis") != "radical_cobalamin_sam_like_probes":
        return
    candidate_id = str(row["candidate_id"])
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "factory_radical_cobalamin_sam_axis_row")
    _append_unique(record["display_names"], row.get("display_name"))
    _append_unique(record["candidate_roles"], row.get("proposed_label_tier"))
    record["state_votes"].append(_factory_terminal_state(row))
    record["subfamily_votes"].append(_infer_factory_subfamily(row))
    _append_unique(record["next_steps"], row.get("allowed_next_action"))
    mechanical = row.get("mechanical_unblock_requirements") or {}
    _append_unique(record["next_steps"], mechanical.get("allowed_next_action"))
    for blocker in _as_list(mechanical.get("readiness_blockers")):
        _append_unique(record["terminal_blockers"], blocker)
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "factory_active_site_or_locator_evidence",
            **(row.get("active_site_or_locator_evidence") or {}),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            **(row.get("predicted_coordinate_or_provenance_availability") or {}),
            "geometry_or_reconstruction_status": row.get(
                "geometry_or_reconstruction_status"
            ),
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "factory_cofactor_or_metal_evidence",
            **(row.get("cofactor_or_metal_evidence") or {}),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "factory_fold_tm_or_near_neighbor_signal",
            "status": "near_neighbor_signal_present"
            if row.get("fold_tm_or_near_neighbor_signal")
            else "not_available_in_factory_axis",
            "fold_tm_or_near_neighbor_signal": row.get("fold_tm_or_near_neighbor_signal"),
            "source_separation_role": (
                "factory routing/provenance only; no mechanism text, source IDs, "
                "labels, target names, EC, or Rhea IDs used as predictive features"
            ),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "admission_route_basis": row.get("admission_route_basis"),
            "proposed_label_tier": row.get("proposed_label_tier"),
            "rationale": row.get("rationale"),
            "row_context_sha256": row.get("row_context_sha256"),
            "guardrails": {
                "import_or_promotion_performed": False,
                "ready_for_label_import": False,
                "candidate_evidence_lane_only": True,
            },
        }
    )


def _merge_acquisition_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    if row.get("family_axis") != "radical_cobalamin_sam_like_probes":
        return
    candidate_id = str(row["candidate_id"])
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "acquisition_conversion_radical_axis_row")
    _append_unique(record["display_names"], row.get("display_name"))
    record["state_votes"].append(str(row.get("terminal_state") or "review_only_evidence"))
    record["subfamily_votes"].append("radical_sam_cobalamin_general_review_queue")
    for blocker in _as_list(row.get("terminal_blockers")):
        _append_unique(record["terminal_blockers"], blocker)
    _append_unique(record["next_steps"], row.get("allowed_next_action"))
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "acquisition_conversion_required_screen_pack",
            "screens": row.get("screens"),
            "terminal_route_basis": row.get("terminal_route_basis"),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "conversion_context_sha256": row.get("conversion_context_sha256"),
            "priority_screen_ready": row.get("priority_screen_ready"),
        }
    )


def _merge_sidecar_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
    kind: str,
) -> None:
    candidate_id = str(row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, f"{kind}_locus_sidecar_row")
    _append_unique(record["candidate_roles"], row.get("benchmark_role"))
    _append_unique(record["candidate_roles"], row.get("label_type"))
    _append_unique(record["candidate_roles"], row.get("fingerprint_id"))
    record["state_votes"].append(_sidecar_terminal_state(row, kind))
    record["subfamily_votes"].append(_infer_sidecar_subfamily(row, kind))
    status = str(row.get("sidecar_status") or "")
    if status == "unsupported_or_missing_geometry":
        _append_unique(
            record["next_steps"],
            "materialize or approve coordinate geometry before treating this "
            "locus as source-free radical/cobalamin evidence",
        )
        _append_unique(record["terminal_blockers"], "unsupported_or_missing_geometry")
    elif "structure_wide" in status:
        _append_unique(
            record["next_steps"],
            "repair local active-site locator; structure-wide cofactor context "
            "must not count as catalytic evidence",
        )
        _append_unique(record["terminal_blockers"], "structure_wide_only_context")
    elif status.startswith("no_"):
        _append_unique(
            record["next_steps"],
            "preserve as a hard near-OOD control for the radical/SAM/cobalamin lane",
        )
    else:
        _append_unique(
            record["next_steps"],
            "keep as review-only locus evidence until source-free duplicate, "
            "locator, and label-factory gates pass",
        )
    proximal_key = {
        "radical_sam": "proximal_radical_sam_ligands",
        "iron_sulfur": "proximal_iron_sulfur_ligands",
        "cobalamin": "proximal_cobalamin_ligands",
    }[kind]
    structure_key = {
        "radical_sam": "structure_radical_sam_ligands",
        "iron_sulfur": "structure_iron_sulfur_ligands",
        "cobalamin": "structure_cobalamin_ligands",
    }[kind]
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": f"{kind}_locus_sidecar",
            "sidecar_status": row.get("sidecar_status"),
            "nearest_active_site_distance_angstrom": row.get(
                "nearest_active_site_distance_angstrom"
            ),
            "proximal_ligands": row.get(proximal_key) or [],
            "structure_ligands": row.get(structure_key) or [],
            "structure_wide_only": row.get("structure_wide_only")
            or row.get("structure_wide_only_flag"),
            "sam_fe_s_copresence_status": row.get("sam_fe_s_copresence_status"),
            "guardrail_note": row.get("guardrail_note"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "evidence_scope": row.get("evidence_scope"),
            "source_feature_status": row.get("source_feature_status"),
            "sidecar_status": row.get("sidecar_status"),
            "split_assignment": row.get("split_assignment"),
            "structure_wide_context_available": row.get("structure_wide_context_available"),
            "coordinate_or_provenance_available": row.get("source_feature_status") == "ok"
            and row.get("sidecar_status") != "unsupported_or_missing_geometry",
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": f"{kind}_locus_sidecar",
            "supporting_ligand_codes": row.get("supporting_ligand_codes") or [],
            "supporting_structure_ligand_codes": row.get(
                "supporting_structure_ligand_codes"
            )
            or [],
            "proximal_ligands": row.get(proximal_key) or [],
            "structure_ligands": row.get(structure_key) or [],
            "adenosyl_or_methyl_context_flag": row.get("adenosyl_or_methyl_context_flag"),
            "radical_rearrangement_source_flag": row.get(
                "radical_rearrangement_source_flag"
            ),
            "sam_fe_s_copresence_status": row.get("sam_fe_s_copresence_status"),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "current702_locus_sidecar_boundary_context",
            "status": row.get("sidecar_status"),
            "label_type": row.get("label_type"),
            "fingerprint_id": row.get("fingerprint_id"),
            "benchmark_role": row.get("benchmark_role"),
            "predictive_use_allowed": row.get("predictive_use_allowed"),
            "ready_for_label_import": row.get("ready_for_label_import"),
            "source_separation_role": (
                "current label and benchmark context are provenance/rationale "
                "only, never predictive scoring features"
            ),
        }
    )


def _merge_radical_sam_freeze_or_decision_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = _candidate_id(row)
    if candidate_id is None:
        return
    record = _candidate(records, candidate_id)
    if row.get("accession"):
        record["accession"] = str(row["accession"])
    _contribute(record, source_key, source_record, row, "external_radical_sam_minicampaign_row")
    _append_unique(record["display_names"], _first_text(row, "protein_name", "entry_name"))
    _append_unique(record["candidate_roles"], row.get("selection_reason"))
    _append_unique(record["candidate_roles"], row.get("target_current_fingerprint_lane"))
    record["state_votes"].append(_external_radical_sam_terminal_state(row))
    record["subfamily_votes"].append("external_radical_sam_minicampaign")
    _append_unique(
        record["next_steps"],
        "materialize source-free external geometry, structural duplicate screens, "
        "and radical-SAM locus review before any promotion",
    )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "external_radical_sam_annotation_context",
            "active_site_annotation_present": row.get("active_site_annotation_present"),
            "binding_site_annotation_present": row.get("binding_site_annotation_present"),
            "catalytic_activity_annotation_present": row.get(
                "catalytic_activity_annotation_present"
            ),
            "review_context": row.get("review_context"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "pdb_count": row.get("pdb_count"),
            "pdb_ids": row.get("pdb_ids_sample") or [],
            "coordinate_or_provenance_available": bool(row.get("pdb_ids_sample")),
            "score_status": row.get("score_status") or row.get("production_score_status"),
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "external_radical_sam_source_context",
            "radical_sam_source_context_present": row.get(
                "radical_sam_source_context_present"
            )
            or (row.get("review_context") or {}).get("source_radical_sam_context_present"),
            "fe_s_or_sam_source_context_present": row.get(
                "fe_s_or_sam_source_context_present"
            )
            or (row.get("review_context") or {}).get("fe_s_or_sam_source_context_present"),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "external_radical_sam_current_reference_sequence_screen",
            "review_context": row.get("review_context"),
            "primary_ec": row.get("primary_ec"),
            "ec_numbers": row.get("ec_numbers"),
            "source_separation_role": (
                "EC/source context retained only as provenance/rationale, not "
                "as predictive scoring input"
            ),
        }
    )


def _merge_sequence_or_baseline_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = _candidate_id(row)
    if candidate_id is None:
        return
    record = _candidate(records, candidate_id)
    if row.get("accession"):
        record["accession"] = str(row["accession"])
    _contribute(record, source_key, source_record, row, "radical_sam_duplicate_or_baseline_screen")
    record["state_votes"].append(_external_radical_sam_terminal_state(row))
    record["subfamily_votes"].append("external_radical_sam_minicampaign")
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "deterministic_sequence_or_baseline_duplicate_screen",
            "sequence_baseline_signal": row.get("sequence_baseline_signal"),
            "nearest_current_reference_id": row.get("exact_current_reference_id")
            or row.get("deterministic_5mer_nearest_current_reference_id"),
            "deterministic_5mer_jaccard_to_nearest_current_reference": row.get(
                "deterministic_5mer_jaccard_to_nearest_current_reference"
            ),
            "geometry_retrieval_status": row.get("geometry_retrieval_status"),
            "terminal_decision": row.get("terminal_decision")
            or row.get("terminal_decision_input_status"),
        }
    )


def _merge_panel_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
    subfamily: str,
) -> None:
    candidate_id = str(row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "family_panel_radical_boundary_row")
    _append_unique(record["candidate_roles"], row.get("benchmark_role"))
    _append_unique(record["candidate_roles"], row.get("evidence_role"))
    record["state_votes"].append(_panel_terminal_state(row))
    record["subfamily_votes"].append(subfamily)
    if _panel_terminal_state(row) == "blocked_coordinate":
        _append_unique(
            record["next_steps"],
            "repair missing predicted geometry before family-promotion discussion",
        )
        _append_unique(record["terminal_blockers"], "predicted_geometry_missing")
    else:
        _append_unique(
            record["next_steps"],
            "keep as review-only radical/cofactor boundary evidence; do not import",
        )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "family_panel_predicted_geometry_context",
            "predicted_geometry_status": row.get("predicted_geometry_status"),
            "predicted_geometry_top1": row.get("predicted_geometry_top1"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "predicted_geometry_status": row.get("predicted_geometry_status"),
            "predicted_geometry_accession_repair": row.get(
                "predicted_geometry_accession_repair"
            ),
            "predicted_structure_fold_channel": row.get("predicted_structure_fold_channel"),
            "coordinate_or_provenance_available": row.get("predicted_geometry_status") == "ok",
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "selected_organic_cofactor_scores",
            "selected_organic_cofactor_scores": row.get("selected_organic_cofactor_scores")
            or {},
            "selected_organic_cofactor_max": row.get("selected_organic_cofactor_max"),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "family_panel_predicted_structure_fold_channel",
            "predicted_structure_fold_channel": row.get("predicted_structure_fold_channel"),
            "selected_pdb_fold_proxy": row.get("selected_pdb_fold_proxy"),
        }
    )


def _merge_glycyl_guardrail_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = str(row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "glycyl_radical_guardrail_row")
    _append_unique(record["candidate_roles"], row.get("benchmark_role"))
    _append_unique(record["candidate_roles"], row.get("promotion_readiness"))
    _append_unique(record["candidate_roles"], row.get("guardrail_decision"))
    record["state_votes"].append("reject/OOS_preserve_signal")
    record["subfamily_votes"].append("glycyl_radical_or_thiamine_radical_boundary")
    for blocker in _as_list(row.get("remaining_blockers")):
        _append_unique(record["terminal_blockers"], blocker)
    _append_unique(
        record["next_steps"],
        row.get("next_source_action")
        or "preserve as heldout/review-only radical boundary control; do not import",
    )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "glycyl_radical_review_guardrail",
            "predicted_geometry_top1_fingerprint_id": row.get(
                "predicted_geometry_top1_fingerprint_id"
            ),
            "predicted_geometry_top1_score": row.get(
                "predicted_geometry_top1_score"
            ),
            "row_specific_bond_change_schema_status": row.get(
                "row_specific_bond_change_schema_status"
            ),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "split_assignment": row.get("split_assignment"),
            "research_gate_status": row.get("research_gate_status"),
            "coordinate_or_provenance_available": True,
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "allowed_for_model_training_now": row.get("allowed_for_model_training_now"),
            "allowed_for_threshold_selection_now": row.get(
                "allowed_for_threshold_selection_now"
            ),
            "guardrail_decision": row.get("guardrail_decision"),
            "promotion_readiness": row.get("promotion_readiness"),
        }
    )


def _merge_radical_sam_source_check(
    records: dict[str, dict[str, Any]],
    payload: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    row = payload.get("row") or {}
    candidate_id = str(row.get("source_accession") or row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    if candidate_id.startswith("uniprot:"):
        record["accession"] = candidate_id.split(":", 1)[1]
    _contribute(record, source_key, source_record, row, "secondary_radical_sam_source_check")
    _append_unique(record["aliases"], row.get("entry_id"))
    _append_unique(record["display_names"], row.get("display_name"))
    _append_unique(record["candidate_roles"], row.get("candidate_role"))
    record["state_votes"].append("blocked_family_decision")
    record["subfamily_votes"].append("radical_sam_sf4_cx3cx2c_probe")
    _append_unique(
        record["next_steps"],
        (payload.get("source_check_decision") or {}).get("next_action"),
    )
    _append_unique(record["terminal_blockers"], "geometry_fold_fingerprint_disagreement")
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "secondary_probe_source_check",
            "source_check_focus": (payload.get("fold_augmented_readout") or {}).get(
                "source_check_focus"
            ),
            "local_source_evidence": payload.get("local_source_evidence"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "fold_augmented_readout": payload.get("fold_augmented_readout"),
            "coordinate_or_provenance_available": True,
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "secondary_probe_current702_duplicate_and_leakage_screen",
            **(payload.get("duplicate_and_leakage_screen") or {}),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "source_check_decision": payload.get("source_check_decision"),
            "ready_for_label_import": row.get("ready_for_label_import"),
        }
    )


def _merge_coupled_plp_cobalamin_decision(
    records: dict[str, dict[str, Any]],
    payload: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    row = payload.get("row") or {}
    if not row:
        return
    candidate_id = str(row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "coupled_plp_cobalamin_schema_decision")
    _append_unique(record["display_names"], row.get("entry_name"))
    _append_unique(record["candidate_roles"], row.get("current_target_fingerprint"))
    _append_unique(record["candidate_roles"], row.get("schema_issue"))
    record["state_votes"].append("blocked_family_decision")
    record["subfamily_votes"].append("coupled_plp_adenosylcobalamin_aminomutase")
    _append_unique(record["terminal_blockers"], row.get("exact_blocker"))
    _append_unique(record["next_steps"], row.get("future_reopen_condition"))
    context = row.get("observed_cofactor_context") or {}
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "coupled_plp_cobalamin_schema_blocker",
            "selected_pdb": row.get("selected_pdb"),
            "current_status": row.get("current_status"),
            "observed_cofactor_context": context,
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "selected_pdb": row.get("selected_pdb"),
            "coordinate_or_provenance_available": bool(row.get("selected_pdb")),
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "coupled_plp_adenosylcobalamin",
            "hetatms_in_structure": context.get("hetatms_in_structure"),
            "b12_ligands": context.get("b12_ligands"),
            "cofactors_required": context.get("cofactors_required"),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "import_gate_eligible": row.get("import_gate_eligible"),
            "not_counted_as": row.get("not_counted_as"),
            "terminal_current_production_universe_no_go": row.get(
                "terminal_current_production_universe_no_go"
            ),
        }
    )


def _merge_coupled_plp_cobalamin_guidance(
    records: dict[str, dict[str, Any]],
    payload: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    guidance = payload.get("coupled_plp_cobalamin_guidance") or {}
    members = guidance.get("canonical_members") or []
    target = next(
        (member for member in members if member.get("m_csa_id") == "m_csa:737"),
        None,
    )
    if not target:
        return
    record = _candidate(records, "m_csa:737")
    _contribute(record, source_key, source_record, guidance, "coupled_plp_cobalamin_expert_guidance")
    _append_unique(record["display_names"], target.get("name"))
    record["state_votes"].append("blocked_family_decision")
    record["subfamily_votes"].append("coupled_plp_adenosylcobalamin_aminomutase")
    for requirement in _as_list(guidance.get("minimal_evidence_required")):
        _append_unique(record["terminal_blockers"], requirement)
    _append_unique(
        record["next_steps"],
        "draft ontology/fingerprint and dedicated gates for coupled PLP-AdoCbl "
        "aminomutase before any countable decision",
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "expert_guidance_coupled_plp_adenosylcobalamin",
            "recommended_schema": guidance.get("recommended_schema"),
            "production_schema_status": guidance.get("production_schema_status"),
            "scientific_name_candidates": guidance.get("scientific_name_candidates"),
            "minimal_evidence_required": guidance.get("minimal_evidence_required"),
        }
    )


def _iron_sulfur_feature_evidence(row: dict[str, Any]) -> dict[str, Any]:
    evidence = row.get("approval_readiness_evidence") or {}
    source_free = evidence.get("source_free_feature_evidence") or {}
    if not source_free:
        source_free = row.get("relaxed_non_pqq_donor_acceptor_evidence") or {}
    if not source_free:
        source_free = (
            (row.get("approval_qualified_evidence") or {})
            .get("projection_backed_pqq_nad_evidence", {})
            .get("pqq_donor_acceptor_evidence", {})
        )
    return source_free


def _merge_iron_sulfur_feature_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = str(row.get("entry_id") or "")
    if not candidate_id:
        return
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "source_free_iron_sulfur_sF4_feature_row")
    evidence = _iron_sulfur_feature_evidence(row)
    readiness = row.get("approval_readiness_evidence") or {}
    state = (
        "blocked_family_decision"
        if readiness.get("missing_import_requirements")
        else "review_only_evidence"
    )
    record["state_votes"].append(state)
    record["subfamily_votes"].append("fe_s_radical_or_electron_flow_boundary")
    for requirement in _as_list(readiness.get("missing_import_requirements")):
        _append_unique(record["terminal_blockers"], requirement)
    _append_unique(
        record["next_steps"],
        "preserve source-free SF4/Fe-S contact evidence as review-only support; "
        "resolve predictive-use, train/cal sidecar, and import-gate blockers before promotion",
    )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "locator_class": "source_free_sf4_fe_s_donor_acceptor_contacts",
            "row_specific_event_features": row.get("row_specific_event_features"),
            "positive_contact_examples": evidence.get("positive_contact_examples") or [],
            "family_distance_examples": evidence.get("family_distance_examples") or [],
            "min_relaxed_non_pqq_donor_acceptor_distance_to_active_site_atom": evidence.get(
                "min_relaxed_non_pqq_donor_acceptor_distance_to_active_site_atom"
            ),
            "contact_count": evidence.get("contact_count"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "coordinate_path": evidence.get("coordinate_path"),
            "geometry_status": evidence.get("geometry_status"),
            "field_status": evidence.get("field_status"),
            "coordinate_or_provenance_available": bool(evidence.get("coordinate_path")),
        }
    )
    record["cofactor_sources"].append(
        {
            "source_key": source_key,
            "cofactor_axis": "source_free_sf4_fe_s_donor_acceptor_contacts",
            "included_redox_families": evidence.get("included_redox_families"),
            "excluded_redox_families": evidence.get("excluded_redox_families"),
            "ligand_codes": sorted(
                {
                    str(example.get("ligand_code"))
                    for example in _as_list(evidence.get("family_distance_examples"))
                    if isinstance(example, dict) and example.get("ligand_code")
                }
            ),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "source_free_electron_flow_field_complete": row.get(
                "source_free_electron_flow_field_complete"
            ),
            "assigned_embedding_split": row.get("assigned_embedding_split"),
            "predictive_use_allowed_now": readiness.get("predictive_use_allowed_now"),
            "present_in_current_train_cal_feature_sidecar": readiness.get(
                "present_in_current_train_cal_feature_sidecar"
            ),
            "missing_import_requirements": readiness.get("missing_import_requirements"),
        }
    )


def _parse_fasta(path: Path) -> dict[str, str]:
    sequences: dict[str, list[str]] = {}
    current_id: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            current_id = line[1:].split("|", 1)[0]
            sequences[current_id] = []
        elif current_id:
            sequences[current_id].append(line.strip())
    return {key: "".join(parts) for key, parts in sequences.items()}


def _cx3cx2c_motifs(sequence: str) -> list[dict[str, Any]]:
    motifs: list[dict[str, Any]] = []
    for match in re.finditer(r"(?=(C...C..C))", sequence):
        motifs.append(
            {
                "motif_family": "CX3CX2C",
                "motif_pattern": "CxxxCxxC",
                "start_1_based": match.start(1) + 1,
                "end_1_based": match.start(1) + len(match.group(1)),
                "motif_sequence": match.group(1),
            }
        )
    return motifs


def _merge_fasta_motifs(
    records: dict[str, dict[str, Any]],
    fasta_paths: dict[str, Path],
    fasta_records: dict[str, dict[str, Any]],
) -> None:
    for source_key, path in fasta_paths.items():
        if source_key not in fasta_records:
            continue
        for candidate_id, sequence in _parse_fasta(path).items():
            record = _candidate(records, candidate_id)
            if candidate_id.startswith("uniprot:"):
                record["accession"] = candidate_id.split(":", 1)[1]
            source_row = {
                "candidate_id": candidate_id,
                "sequence_sha256": hashlib.sha256(sequence.encode("utf-8")).hexdigest(),
                "sequence_length": len(sequence),
                "cx3cx2c_motif_count": len(_cx3cx2c_motifs(sequence)),
            }
            _contribute(
                record,
                source_key,
                fasta_records[source_key],
                source_row,
                "radical_sam_sequence_cx3cx2c_motif_scan",
            )
            motifs = _cx3cx2c_motifs(sequence)
            if motifs:
                record["state_votes"].append("review_only_evidence")
                record["subfamily_votes"].append("radical_sam_sf4_cx3cx2c_probe")
                _append_unique(
                    record["next_steps"],
                    "map CX3CX2C motif cysteines to source-free coordinates and "
                    "confirm SF4/SAM geometry before promotion",
                )
            else:
                record["state_votes"].append("blocked_locator")
                _append_unique(record["terminal_blockers"], "cx3cx2c_motif_not_detected")
            record["active_site_sources"].append(
                {
                    "source_key": source_key,
                    "locator_class": "sequence_cx3cx2c_radical_sam_motif_scan",
                    "sequence_length": len(sequence),
                    "motif_count": len(motifs),
                    "motifs": motifs[:12],
                    "motif_scan_status": "cx3cx2c_detected"
                    if motifs
                    else "cx3cx2c_not_detected",
                }
            )
            record["cofactor_sources"].append(
                {
                    "source_key": source_key,
                    "cofactor_axis": "radical_sam_sequence_motif",
                    "cx3cx2c_motif_count": len(motifs),
                    "cx3cx2c_motif_evidence_present": bool(motifs),
                    "requires_coordinate_followup": True,
                }
            )


def _rows_for_source(source_key: str, payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    if source_key in {
        "targeted_expansion_factory_batch",
        "targeted_expansion_acquisition_conversion_screens",
        "radical_sam_minicampaign_freeze",
        "radical_sam_minicampaign_decision_packet",
        "radical_sam_minicampaign_baseline_comparison",
        "radical_sam_minicampaign_sequence_baseline",
        "radical_sam_locus_sidecar",
        "iron_sulfur_locus_sidecar",
        "cobalamin_locus_sidecar",
    }:
        key = "candidate_rows" if source_key == "targeted_expansion_factory_batch" else "rows"
        rows = payload.get(key) or []
        return [row for row in rows if isinstance(row, dict)]
    if source_key in {
        "cobalamin_and_radical_rearrangement_panel",
        "glycyl_radical_or_thiamine_radical_panel",
    }:
        return [row for row in payload.get("row_evidence", []) if isinstance(row, dict)]
    if source_key == "glycyl_radical_readiness_packet":
        return [row for row in payload.get("row_readiness", []) if isinstance(row, dict)]
    if source_key == "glycyl_radical_no_template_guardrail":
        return [row for row in payload.get("row_guardrails", []) if isinstance(row, dict)]
    if source_key == "iron_sulfur_electron_flow_qualified_union":
        return [row for row in payload.get("feature_rows", []) if isinstance(row, dict)]
    if source_key == "iron_sulfur_electron_flow_support_subset":
        return [
            row
            for row in payload.get("selected_support_feature_rows", [])
            if isinstance(row, dict)
        ]
    if source_key == "iron_sulfur_electron_flow_tiny_tranche":
        return [
            row
            for row in payload.get("candidate_feature_sidecar_rows", [])
            if isinstance(row, dict)
        ]
    if source_key == "coupled_plp_cobalamin_schema_decision":
        row = payload.get("row")
        return [row] if isinstance(row, dict) else []
    return []


def _load_sources(
    source_paths: dict[str, Path], fasta_paths: dict[str, Path]
) -> tuple[
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, str],
]:
    payloads: dict[str, Any] = {}
    source_records: dict[str, dict[str, Any]] = {}
    fasta_records: dict[str, dict[str, Any]] = {}
    missing: dict[str, str] = {}
    for source_key, path in source_paths.items():
        if not path.exists():
            missing[source_key] = str(path)
            continue
        payloads[source_key] = _read_json(path)
        source_records[source_key] = _source_record(path)
    for source_key, path in fasta_paths.items():
        if not path.exists():
            missing[source_key] = str(path)
            continue
        fasta_records[source_key] = _source_record(path)
    return payloads, source_records, fasta_records, missing


def _merge_sources(
    payloads: dict[str, Any],
    source_records: dict[str, dict[str, Any]],
    fasta_paths: dict[str, Path],
    fasta_records: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for source_key, payload in payloads.items():
        if source_key == "targeted_expansion_factory_batch":
            for row in _rows_for_source(source_key, payload):
                _merge_factory_row(records, row, source_key, source_records[source_key])
        elif source_key == "targeted_expansion_acquisition_conversion_screens":
            for row in _rows_for_source(source_key, payload):
                _merge_acquisition_row(records, row, source_key, source_records[source_key])
        elif source_key in {
            "radical_sam_locus_sidecar",
            "iron_sulfur_locus_sidecar",
            "cobalamin_locus_sidecar",
        }:
            kind = source_key.replace("_locus_sidecar", "")
            for row in _rows_for_source(source_key, payload):
                _merge_sidecar_row(records, row, source_key, source_records[source_key], kind)
        elif source_key in {
            "radical_sam_minicampaign_freeze",
            "radical_sam_minicampaign_decision_packet",
        }:
            for row in _rows_for_source(source_key, payload):
                _merge_radical_sam_freeze_or_decision_row(
                    records, row, source_key, source_records[source_key]
                )
        elif source_key in {
            "radical_sam_minicampaign_baseline_comparison",
            "radical_sam_minicampaign_sequence_baseline",
        }:
            for row in _rows_for_source(source_key, payload):
                _merge_sequence_or_baseline_row(
                    records, row, source_key, source_records[source_key]
                )
        elif source_key == "cobalamin_and_radical_rearrangement_panel":
            for row in _rows_for_source(source_key, payload):
                _merge_panel_row(
                    records,
                    row,
                    source_key,
                    source_records[source_key],
                    "cobalamin_context_boundary",
                )
        elif source_key == "glycyl_radical_or_thiamine_radical_panel":
            for row in _rows_for_source(source_key, payload):
                _merge_panel_row(
                    records,
                    row,
                    source_key,
                    source_records[source_key],
                    "glycyl_radical_or_thiamine_radical_boundary",
                )
        elif source_key in {
            "glycyl_radical_readiness_packet",
            "glycyl_radical_no_template_guardrail",
        }:
            for row in _rows_for_source(source_key, payload):
                _merge_glycyl_guardrail_row(
                    records, row, source_key, source_records[source_key]
                )
        elif source_key == "radical_sam_source_check_secondary_probe":
            _merge_radical_sam_source_check(
                records, payload, source_key, source_records[source_key]
            )
        elif source_key == "coupled_plp_cobalamin_schema_decision":
            _merge_coupled_plp_cobalamin_decision(
                records, payload, source_key, source_records[source_key]
            )
        elif source_key == "coupled_plp_cobalamin_expert_guidance":
            _merge_coupled_plp_cobalamin_guidance(
                records, payload, source_key, source_records[source_key]
            )
        elif source_key in {
            "iron_sulfur_electron_flow_qualified_union",
            "iron_sulfur_electron_flow_support_subset",
            "iron_sulfur_electron_flow_tiny_tranche",
        }:
            for row in _rows_for_source(source_key, payload):
                _merge_iron_sulfur_feature_row(
                    records, row, source_key, source_records[source_key]
                )
    _merge_fasta_motifs(records, fasta_paths, fasta_records)
    return records


def _choose_terminal_state(record: dict[str, Any]) -> str:
    states = [state for state in record["state_votes"] if state in TERMINAL_STATES]
    if not states:
        return "review_only_evidence"
    return sorted(states, key=lambda state: STATE_PRIORITY[state])[0]


def _choose_subfamily(record: dict[str, Any]) -> str:
    lanes = _merge_list(record["subfamily_votes"])
    if not lanes:
        return "radical_sam_cobalamin_general_review_queue"
    return sorted(
        lanes, key=lambda lane: (SUBFAMILY_PRIORITY.get(str(lane), 99), str(lane))
    )[0]


def _confidence_from_state(record: dict[str, Any], terminal_state: str) -> str:
    flags = _cofactor_flags_from_sources(record["cofactor_sources"] + record["active_site_sources"])
    if terminal_state == "countable_candidate_preflight_only":
        return "tier_A_source_free_preflight_import_not_performed"
    if flags["cx3cx2c_motif_evidence_present"] and flags["sf4_or_fe_s_evidence_present"]:
        return "tier_A_radical_sam_motif_and_fe_s_context"
    if flags["cobalamin_or_adocbl_evidence_present"] and flags["plp_evidence_present"]:
        return "tier_A_coupled_plp_adocbl_schema_blocked"
    if flags["cobalamin_or_adocbl_evidence_present"]:
        return "tier_A_cobalamin_locus_context"
    if flags["sf4_or_fe_s_evidence_present"] or flags["sam_or_adomet_evidence_present"]:
        return "tier_B_radical_sam_or_fe_s_context"
    if terminal_state in {"blocked_locator", "blocked_coordinate", "blocked_family_decision"}:
        return "tier_C_repair_or_decision_queue"
    if terminal_state == "reject/OOS_preserve_signal":
        return "tier_B_hard_near_ood_control"
    return "tier_B_review_only_candidate"


def _status_counts(sources: list[dict[str, Any]], *keys: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for source in sources:
        for key in keys:
            for value in _as_list(source.get(key)):
                if value not in (None, "", [], {}):
                    counts[str(value)] += 1
    return dict(sorted(counts.items()))


def _active_site_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    motifs = []
    proximal_ligands = []
    positive_contacts = []
    for source in sources:
        for motif in _as_list(source.get("motifs")):
            if isinstance(motif, dict):
                motifs.append(motif)
        for ligand in _as_list(source.get("proximal_ligands")):
            if isinstance(ligand, dict):
                proximal_ligands.append(ligand)
        for contact in _as_list(source.get("positive_contact_examples")):
            if isinstance(contact, dict):
                positive_contacts.append(contact)
    return {
        "locator_status_counts": _status_counts(
            sources,
            "locator_class",
            "sidecar_status",
            "motif_scan_status",
            "predicted_geometry_status",
            "field_status",
        ),
        "cx3cx2c_motif_count": len(motifs),
        "cx3cx2c_motif_examples": motifs[:8],
        "proximal_ligand_examples": proximal_ligands[:8],
        "sf4_fe_s_contact_examples": positive_contacts[:8],
        "source_specific": sources,
    }


def _coordinate_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    paths = []
    pdb_ids = []
    selected = []
    statuses = []
    for source in sources:
        for value in _as_list(source.get("coordinate_path")):
            if value:
                paths.append(str(value))
        for key in ("pdb_ids", "pdb_ids_sample"):
            for value in _as_list(source.get(key)):
                if value:
                    pdb_ids.append(str(value))
        for key in ("selected_pdb", "selected_structure", "selected_structure_id"):
            value = source.get(key)
            if value not in (None, "", [], {}):
                selected.append(str(value))
        for key in (
            "score_status",
            "geometry_status",
            "source_feature_status",
            "sidecar_status",
            "field_status",
        ):
            value = source.get(key)
            if value not in (None, "", [], {}):
                statuses.append(str(value))
    return {
        "coordinate_paths": sorted(set(paths)),
        "pdb_ids": sorted(set(pdb_ids)),
        "selected_structures": sorted(set(selected)),
        "status_counts": dict(sorted(Counter(statuses).items())),
        "coordinate_or_provenance_available": bool(paths or pdb_ids or selected)
        or any(source.get("coordinate_or_provenance_available") for source in sources),
        "source_specific": sources,
    }


def _cofactor_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    ligand_codes = []
    axes = []
    for source in sources:
        _append_unique(axes, source.get("cofactor_axis"))
        for key in (
            "supporting_ligand_codes",
            "supporting_structure_ligand_codes",
            "ligand_codes",
            "hetatms_in_structure",
        ):
            for value in _as_list(source.get(key)):
                if value:
                    ligand_codes.append(str(value))
    return {
        "evidence_flags": _cofactor_flags_from_sources(sources),
        "cofactor_axes": sorted(str(axis) for axis in axes),
        "supporting_ligand_codes": sorted(set(ligand_codes)),
        "source_specific": sources,
    }


def _duplicate_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    nearest_hits = []
    for source in sources:
        for key in ("nearest_current_reference_id", "nearest_atlas_entry_id"):
            value = source.get(key)
            if value not in (None, "", [], {}):
                nearest_hits.append(str(value))
        screen = source.get("predicted_structure_fold_channel")
        if isinstance(screen, dict) and screen.get("nearest_atlas_entry_id"):
            nearest_hits.append(str(screen["nearest_atlas_entry_id"]))
    return {
        "status_counts": _status_counts(
            sources,
            "status",
            "screen",
            "sequence_baseline_signal",
            "terminal_decision",
            "sidecar_status",
        ),
        "nearest_current_or_atlas_hits_sample": nearest_hits[:8],
        "source_specific": sources,
    }


def _default_next_step(terminal_state: str) -> str:
    return {
        "countable_candidate_preflight_only": (
            "hold for main-thread controlled-promotion decision; do not import automatically"
        ),
        "review_only_evidence": (
            "preserve as review-only radical/SAM/cobalamin evidence until explicit gates pass"
        ),
        "reject/OOS_preserve_signal": (
            "preserve the non-counting OOS, hard-negative, or duplicate boundary signal"
        ),
        "blocked_locator": (
            "repair local active-site locator evidence before source-free scoring"
        ),
        "blocked_coordinate": (
            "materialize or approve valid coordinate/provenance before source-free scoring"
        ),
        "blocked_family_decision": (
            "resolve family/schema decision and rerun pre-promotion gates"
        ),
    }[terminal_state]


def _machine_steps_for_terminal(
    terminal_state: str, next_steps: list[Any]
) -> list[str]:
    cleaned = [str(step) for step in _merge_list(next_steps) if str(step)]
    if not cleaned:
        cleaned = [_default_next_step(terminal_state)]
    needles = {
        "countable_candidate_preflight_only": ("hold", "do not import"),
        "review_only_evidence": ("review-only", "preserve", "gates"),
        "reject/OOS_preserve_signal": ("preserve", "oos", "hard", "do not import"),
        "blocked_locator": ("locator", "motif", "active-site"),
        "blocked_coordinate": ("coordinate", "geometry", "materialize"),
        "blocked_family_decision": ("family", "schema", "gate", "promotion"),
    }[terminal_state]
    preferred = [
        (index, step)
        for index, step in enumerate(cleaned)
        if any(needle in step.lower() for needle in needles)
    ]
    def rank(step: str) -> int:
        lowered = step.lower()
        if terminal_state == "review_only_evidence":
            if "review-only" in lowered and "hard near-ood" not in lowered:
                return 0
            if "gate" in lowered:
                return 1
            return 2
        if terminal_state == "blocked_family_decision":
            if any(
                needle in lowered
                for needle in ("schema", "fingerprint", "ontology")
            ):
                return 0
            if "family" in lowered:
                return 1
            if any(needle in lowered for needle in ("gate", "promotion")):
                return 2
            return 2
        if terminal_state == "blocked_locator":
            if any(needle in lowered for needle in ("locator", "motif")):
                return 0
            return 1
        if terminal_state == "blocked_coordinate":
            if any(needle in lowered for needle in ("coordinate", "geometry")):
                return 0
            return 1
        return 0

    sorted_preferred = [
        step for index, step in sorted(preferred, key=lambda item: (rank(item[1]), item[0]))
    ]
    ordered = sorted_preferred + cleaned + [_default_next_step(terminal_state)]
    deduped = []
    seen = set()
    for step in ordered:
        if step not in seen:
            seen.add(step)
            deduped.append(step)
    return deduped


def _finalize_record(record: dict[str, Any]) -> dict[str, Any]:
    terminal_state = _choose_terminal_state(record)
    subfamily = _choose_subfamily(record)
    cofactor_evidence = _cofactor_summary(record["cofactor_sources"])
    confidence_tier = _confidence_from_state(record, terminal_state)
    next_steps = _machine_steps_for_terminal(terminal_state, record["next_steps"])
    row = {
        "candidate_id": record["candidate_id"],
        "accession": record["accession"],
        "display_name": record["display_names"][0] if record["display_names"] else None,
        "aliases": _merge_list(record["aliases"]),
        "proposed_family_lane": "radical_cobalamin_sam_like_probes",
        "proposed_subfamily_lane": subfamily,
        "terminal_state": terminal_state,
        "candidate_roles": _merge_list(record["candidate_roles"]),
        "confidence_tier": confidence_tier,
        "active_site_or_locator_evidence": _active_site_summary(
            record["active_site_sources"]
        ),
        "coordinate_or_provenance_status": _coordinate_summary(
            record["coordinate_sources"]
        ),
        "sf4_fe_s_sam_cobalamin_plp_evidence": cofactor_evidence,
        "duplicate_screens": _duplicate_summary(record["duplicate_screen_sources"]),
        "source_free_preflight": {
            "status": "source_free_preflight_or_review_context_available"
            if record["source_free_preflight_sources"]
            else "source_free_preflight_not_available",
            "guardrail": (
                "candidate/evidence lane only; no imports, promotions, registry "
                "edits, threshold changes, heldout training, or tuning"
            ),
            "source_specific": record["source_free_preflight_sources"],
        },
        "source_hashes": dict(sorted(record["source_hashes"].items())),
        "source_contributions": record["source_contributions"],
        "terminal_blockers": sorted(
            set(str(value) for value in record["terminal_blockers"] if value)
        ),
        "machine_actionable_next_step": next_steps[0],
        "machine_actionable_next_steps": next_steps,
    }
    row["row_context_sha256"] = _canonical_sha256(
        {
            "candidate_id": row["candidate_id"],
            "terminal_state": row["terminal_state"],
            "proposed_subfamily_lane": row["proposed_subfamily_lane"],
            "source_contributions": row["source_contributions"],
        }
    )
    return row


def _validate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [row["candidate_id"] for row in rows]
    duplicate_ids = sorted(
        candidate_id for candidate_id, count in Counter(ids).items() if count > 1
    )
    invalid_states = sorted(
        {
            row.get("terminal_state")
            for row in rows
            if row.get("terminal_state") not in TERMINAL_STATES
        }
    )
    required_keys = {
        "candidate_id",
        "accession",
        "proposed_family_lane",
        "proposed_subfamily_lane",
        "terminal_state",
        "active_site_or_locator_evidence",
        "coordinate_or_provenance_status",
        "sf4_fe_s_sam_cobalamin_plp_evidence",
        "duplicate_screens",
        "source_hashes",
        "confidence_tier",
        "machine_actionable_next_step",
    }
    missing_required = []
    for row in rows:
        missing = sorted(required_keys - set(row))
        if missing:
            missing_required.append(
                {"candidate_id": row.get("candidate_id"), "missing_keys": missing}
            )
    return {
        "candidate_ids_unique": not duplicate_ids,
        "duplicate_candidate_ids": duplicate_ids,
        "terminal_states_allowed": not invalid_states,
        "invalid_terminal_states": invalid_states,
        "required_row_fields_present": not missing_required,
        "rows_missing_required_fields": missing_required[:20],
        "source_hashes_present_for_all_rows": all(row.get("source_hashes") for row in rows),
        "machine_actionable_next_steps_present": all(
            row.get("machine_actionable_next_step") for row in rows
        ),
    }


def _evidence_coverage(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        flags = (
            row["sf4_fe_s_sam_cobalamin_plp_evidence"].get("evidence_flags") or {}
        )
        for key, value in flags.items():
            if value:
                counts[key] += 1
        if row["coordinate_or_provenance_status"].get(
            "coordinate_or_provenance_available"
        ):
            counts["coordinate_or_provenance_available"] += 1
        if row["active_site_or_locator_evidence"].get("cx3cx2c_motif_count", 0) > 0:
            counts["cx3cx2c_motif_locator_rows"] += 1
        if row["active_site_or_locator_evidence"].get("sf4_fe_s_contact_examples"):
            counts["sf4_fe_s_contact_locator_rows"] += 1
    return dict(sorted(counts.items()))


def build_scaleout_radical_sam_cobalamin_shard(
    *,
    source_paths: dict[str, Path] | None = None,
    fasta_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
    started_at_utc: str | None = None,
    started_at_local: str | None = None,
) -> dict[str, Any]:
    paths = source_paths or DEFAULT_SOURCE_PATHS
    fasta = fasta_paths or DEFAULT_FASTA_PATHS
    payloads, source_records, fasta_records, missing_sources = _load_sources(paths, fasta)
    records = _merge_sources(payloads, source_records, fasta, fasta_records)
    rows = [
        _finalize_record(records[candidate_id])
        for candidate_id in sorted(records, key=_sort_key)
    ]
    terminal_counts = Counter(row["terminal_state"] for row in rows)
    subfamily_counts = Counter(row["proposed_subfamily_lane"] for row in rows)
    confidence_counts = Counter(row["confidence_tier"] for row in rows)
    validation = _validate_rows(rows)
    source_artifacts = {**source_records, **fasta_records}
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc or _utc_now_iso(),
        "automation_id": "ce-expansion-shard-radical-sam-cobalamin",
        "started_at_utc": started_at_utc,
        "started_at_local": started_at_local,
        "status": "candidate_evidence_lane_ready",
        "scope": {
            "current_countable_label_count": 702,
            "family_lane": "radical_cobalamin_sam_like_probes",
            "included_motifs": [
                "radical SAM CX3CX2C/CxxxCxxC sequence motif",
                "SF4/Fe-S source-free contact probes",
                "SAM/AdoMet ligand locus",
                "cobalamin/AdoCbl ligand locus",
                "coupled PLP-adenosylcobalamin review-only schema blocker",
            ],
            "source_policy": (
                "source-free candidate/evidence lane; source IDs, EC/Rhea-like "
                "terms, target names, and mechanism text may appear only as "
                "provenance/rationale"
            ),
            "output_policy": (
                "no registry, ontology, import, split, threshold, model, heldout-training, "
                "or tuning edits"
            ),
        },
        "candidate_count": len(rows),
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "subfamily_lane_counts": dict(sorted(subfamily_counts.items())),
        "confidence_tier_counts": dict(sorted(confidence_counts.items())),
        "evidence_coverage": _evidence_coverage(rows),
        "source_artifacts": source_artifacts,
        "missing_optional_source_artifacts": missing_sources,
        "source_row_counts": {
            key: len(_rows_for_source(key, payload)) for key, payload in payloads.items()
        }
        | {
            key: len(_parse_fasta(path))
            for key, path in fasta.items()
            if key in fasta_records
        },
        "guardrails": {
            "candidate_evidence_lane_only": True,
            "registry_edits_performed": False,
            "ontology_edits_performed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "train_test_splits_changed": False,
            "model_weights_changed": False,
            "heldout_training_or_tuning_performed": False,
            "mechanism_text_or_source_ids_used_as_predictive_scoring_features": False,
            "oos_reject_signal_preserved": terminal_counts["reject/OOS_preserve_signal"]
            > 0,
        },
        "validation_checks": validation,
        "rows": rows,
    }


def render_scaleout_radical_sam_cobalamin_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# Radical SAM Cobalamin Scale-Out Shard",
        "",
        f"- Artifact: `{artifact['artifact_id']}`",
        f"- Created UTC: `{artifact['created_utc']}`",
        f"- Candidate rows: `{artifact['candidate_count']}`",
        f"- Status: `{artifact['status']}`",
        f"- Family lane: `{artifact['scope']['family_lane']}`",
        "",
        "## Terminal States",
        "",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Subfamily Lanes", ""])
    for lane, count in artifact["subfamily_lane_counts"].items():
        lines.append(f"- `{lane}`: {count}")
    lines.extend(["", "## Evidence Coverage", ""])
    for key, count in artifact["evidence_coverage"].items():
        lines.append(f"- `{key}`: {count}")
    lines.extend(["", "## Source Artifacts", ""])
    for key, record in artifact["source_artifacts"].items():
        lines.append(
            f"- `{key}`: `{record['path']}` sha256 `{record['sha256']}`"
        )
    lines.extend(["", "## Review Queues", ""])
    for state in TERMINAL_STATES:
        examples = [
            row for row in artifact["rows"] if row["terminal_state"] == state
        ][:14]
        if not examples:
            continue
        lines.append(f"### `{state}`")
        lines.append("")
        for row in examples:
            lines.append(
                "- "
                f"`{row['candidate_id']}` "
                f"`{row['proposed_subfamily_lane']}` "
                f"`{row['confidence_tier']}` - "
                f"{row['machine_actionable_next_step']}"
            )
        lines.append("")
    lines.extend(
        [
            "## Guardrails",
            "",
            "- No registry, ontology, import, train/test split, threshold, model, or heldout-training/tuning edits were performed.",
            "- Mechanism text, source IDs, EC/Rhea-like context, target names, and source labels are preserved only as provenance/rationale, not predictive scoring features.",
            "- OOS, hard-negative, duplicate, locator, coordinate, and family-decision blockers remain non-counting signals.",
            "",
            "## Validation",
            "",
        ]
    )
    for key, value in artifact["validation_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def render_handoff(
    artifact: dict[str, Any],
    *,
    started_at_utc: str | None,
    started_at_local: str | None,
    elapsed_minutes: float | None = None,
) -> str:
    lines = [
        "# Radical SAM Cobalamin Shard Handoff",
        "",
        "- Automation ID: `ce-expansion-shard-radical-sam-cobalamin`",
        f"- STARTED_AT_UTC: `{started_at_utc or artifact.get('started_at_utc')}`",
        f"- STARTED_AT_LOCAL: `{started_at_local or artifact.get('started_at_local')}`",
        f"- ENDED_AT_UTC: `{_utc_now_iso()}`",
    ]
    if elapsed_minutes is not None:
        lines.append(f"- ELAPSED_MINUTES: `{elapsed_minutes:.3f}`")
    lines.extend(
        [
            "- Lock: `/tmp/ce_scaleout_radical_sam_cobalamin_current702.lock`",
            "- Status: durable lane artifact/report generated; candidate/evidence lane only.",
            "",
            "## Outputs",
            "",
            f"- JSON: `{DEFAULT_OUT_PATH}`",
            f"- Report: `{DEFAULT_REPORT_PATH}`",
            f"- Handoff: `{DEFAULT_HANDOFF_PATH}`",
            "",
            "## Counts",
            "",
            f"- Candidate rows: `{artifact['candidate_count']}`",
        ]
    )
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Next Action", ""])
    lines.append(
        "Merger lane should review the radical/SAM/cobalamin shard by subfamily "
        "and terminal state, with special attention to CX3CX2C+SF4 external "
        "radical-SAM rows, cobalamin/AdoCbl locus rows, m_csa:737 coupled "
        "PLP-AdoCbl schema blocking, and near-OOD Fe-S controls. Do not import "
        "from this shard directly."
    )
    return "\n".join(lines) + "\n"


def write_scaleout_radical_sam_cobalamin_shard(
    *,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
    handoff_path: Path = DEFAULT_HANDOFF_PATH,
    source_paths: dict[str, Path] | None = None,
    fasta_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
    started_at_utc: str | None = None,
    started_at_local: str | None = None,
    elapsed_minutes: float | None = None,
) -> dict[str, Any]:
    artifact = build_scaleout_radical_sam_cobalamin_shard(
        source_paths=source_paths,
        fasta_paths=fasta_paths,
        created_utc=created_utc,
        started_at_utc=started_at_utc,
        started_at_local=started_at_local,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    handoff_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    report_path.write_text(render_scaleout_radical_sam_cobalamin_report(artifact))
    handoff_path.write_text(
        render_handoff(
            artifact,
            started_at_utc=started_at_utc,
            started_at_local=started_at_local,
            elapsed_minutes=elapsed_minutes,
        )
    )
    return artifact


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="build the current702 radical SAM/cobalamin scale-out shard"
    )
    parser.add_argument("--out", default=str(DEFAULT_OUT_PATH))
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--handoff", default=str(DEFAULT_HANDOFF_PATH))
    parser.add_argument("--created-utc")
    parser.add_argument("--started-at-utc")
    parser.add_argument("--started-at-local")
    parser.add_argument("--elapsed-minutes", type=float)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    artifact = write_scaleout_radical_sam_cobalamin_shard(
        out_path=Path(args.out),
        report_path=Path(args.report),
        handoff_path=Path(args.handoff),
        created_utc=args.created_utc,
        started_at_utc=args.started_at_utc,
        started_at_local=args.started_at_local,
        elapsed_minutes=args.elapsed_minutes,
    )
    print(f"wrote {args.out} ({artifact['candidate_count']} candidates)")
    print(f"wrote {args.report}")
    print(f"wrote {args.handoff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
