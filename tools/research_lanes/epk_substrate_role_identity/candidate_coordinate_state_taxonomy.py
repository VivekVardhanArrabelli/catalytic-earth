#!/usr/bin/env python3
"""Audit source-free coordinate-state taxonomy for ePK candidate rows.

This lane-local helper projects the existing candidate evidence table and the
metal materialization overlay into first-class coordinate-state rows. It keeps
review/source context out of source-free evidence and makes source-leakage risk
explicit for product/analog review groups that are not independently
materialized by source-free coordinate state.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)
from substrate_role_identity_eval import (
    ACTIVE_GAMMA_CODES,
    GAMMA_ATOM_NAMES,
    NUCLEOTIDE_LIKE_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_candidate_coordinate_state_taxonomy_v1_20260521"
SOURCE_EVIDENCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
SOURCE_METAL_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_gamma_metal_transfer_geometry_probe_v1_20260521.json"
)
SOURCE_CONFLICT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_conflict_decision_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_coordinate_state_taxonomy_v1_20260521.json"
)

PRIMARY_OUTCOMES = {
    "candidate_evidence_rows_emitted",
    "blocker_cleared_source_free",
    "blocker_not_cleared_data_scarcity",
    "blocker_not_cleared_method_weakness",
    "blocker_not_cleared_biology_ambiguity",
    "counterexample_found",
    "next_query_defined",
}

COORDINATE_STATES = {
    "active_gamma",
    "product_state",
    "adp_state",
    "substrate_acceptor_analog_state",
    "split_state",
    "ligand_absent",
    "metal_absent",
    "unavailable_coordinate_state",
    "ambiguous_coordinate_state",
}

BLOCKER_CLASSES = {
    "active_gamma_geometry",
    "product_state_evidence",
    "substrate_analog_evidence",
    "split_state_evidence",
    "topology_ambiguity",
    "substrate_role_identity",
    "internal_fragment_mimicry",
    "ligand_materialization",
    "source_leakage",
    "wetlab_only_biology",
    "none",
}

STATE_REVIEW_CONTEXTS = {
    "review_product_state_context",
    "review_substrate_acceptor_analog_context",
    "no_review_state_context",
}

PHOSPHO_ACCEPTOR_CODES = {"SEP", "TPO", "PTR"}
PRODUCT_NUCLEOTIDE_CODES = {"ADP"}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    evidence_payload = json.loads(SOURCE_EVIDENCE_ARTIFACT.read_text(encoding="utf-8"))
    metal_payload = json.loads(SOURCE_METAL_ARTIFACT.read_text(encoding="utf-8"))
    conflict_payload = json.loads(SOURCE_CONFLICT_ARTIFACT.read_text(encoding="utf-8"))
    return evidence_payload, metal_payload, conflict_payload


def all_candidate_rows(evidence_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return evidence_payload["candidate_evidence_rows"] + evidence_payload["state_only_rows"]


def metal_rows_by_candidate(metal_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = metal_payload["candidate_transfer_geometry_rows"] + metal_payload["state_only_rows"]
    return {row["candidate_id"]: row for row in rows}


def conflict_rows_by_pdb(conflict_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["pdb_id"]: row for row in conflict_payload["candidate_conflict_rows"]}


def residue_label(key: tuple[str, str, str, str]) -> str:
    chain, resseq, icode, resname = key
    suffix = icode or ""
    return f"{chain}:{resname}{resseq}{suffix}"


def distance_class(value: float | None) -> str:
    if value is None:
        return "none"
    if value <= 4.0:
        return "direct_contact_le_4a"
    if value <= 8.0:
        return "near_active_site_4_to_8a"
    return "distant_gt_8a"


def coordinate_chemistry_scan(pdb_id: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text(pdb_id)
    if text is None:
        return {
            "coordinate_chemistry_status": "fetch_error",
            "coordinate_chemistry_fetch_error": fetch_error,
            "coordinate_chemistry_state_class": "unavailable_coordinate_chemistry",
            "nucleotide_codes_observed": [],
            "active_gamma_codes_observed": [],
            "terminal_gamma_atom_count": 0,
            "product_nucleotide_codes_observed": [],
            "phosphorylated_sty_residue_count": 0,
            "phosphorylated_sty_near_nucleotide_count_le_8a": 0,
            "nearest_phosphorylated_sty_to_nucleotide_distance_angstrom": None,
            "nearest_phosphorylated_sty_to_nucleotide_distance_class": "none",
            "nearest_phosphorylated_sty_residue": None,
            "nearest_nucleotide_atom_to_phosphorylated_sty": None,
        }
    atoms = parse_pdb_atoms(text)
    nucleotide_atoms = [
        atom for atom in atoms if atom["record"] == "HETATM" and atom["resname"] in NUCLEOTIDE_LIKE_CODES
    ]
    terminal_gamma_atoms = [
        atom
        for atom in nucleotide_atoms
        if atom["resname"] in ACTIVE_GAMMA_CODES and atom["atom_name"] in GAMMA_ATOM_NAMES
    ]
    phospho_residues: dict[tuple[str, str, str, str], list[dict[str, Any]]] = {}
    for atom in atoms:
        if atom["resname"] in PHOSPHO_ACCEPTOR_CODES:
            phospho_residues.setdefault(atom["residue_key"], []).append(atom)

    nearest_distance: float | None = None
    nearest_residue: tuple[str, str, str, str] | None = None
    nearest_nucleotide_atom: dict[str, Any] | None = None
    near_nucleotide_residues: set[tuple[str, str, str, str]] = set()
    if nucleotide_atoms:
        for residue_key, residue_atoms in phospho_residues.items():
            residue_nearest: float | None = None
            for residue_atom in residue_atoms:
                for nucleotide_atom in nucleotide_atoms:
                    current = dist(residue_atom, nucleotide_atom)
                    if residue_nearest is None or current < residue_nearest:
                        residue_nearest = current
                    if nearest_distance is None or current < nearest_distance:
                        nearest_distance = current
                        nearest_residue = residue_key
                        nearest_nucleotide_atom = nucleotide_atom
            if residue_nearest is not None and residue_nearest <= 8.0:
                near_nucleotide_residues.add(residue_key)

    nucleotide_codes = sorted({atom["resname"] for atom in nucleotide_atoms})
    product_codes = sorted(set(nucleotide_codes) & PRODUCT_NUCLEOTIDE_CODES)
    if terminal_gamma_atoms:
        state_class = "active_gamma_materialized_by_terminal_gamma_atom"
    elif product_codes and near_nucleotide_residues:
        state_class = "product_state_materialized_by_adp_and_near_phosphorylated_sty"
    elif product_codes and phospho_residues:
        state_class = "adp_with_distant_phosphorylated_sty_product_not_materialized"
    elif product_codes:
        state_class = "adp_without_phosphorylated_sty_product_not_materialized"
    elif nucleotide_atoms:
        state_class = "ambiguous_nucleotide_without_terminal_gamma_product_not_materialized"
    else:
        state_class = "ligand_absent_product_not_materialized"

    if nearest_nucleotide_atom is None:
        compact_nearest_nucleotide = None
    else:
        compact_nearest_nucleotide = {
            "atom_name": nearest_nucleotide_atom["atom_name"],
            "residue_code": nearest_nucleotide_atom["resname"],
            "chain_id": nearest_nucleotide_atom["chain"],
            "auth_seq_id": nearest_nucleotide_atom["resseq"],
            "icode": nearest_nucleotide_atom["icode"] or None,
        }

    return {
        "coordinate_chemistry_status": "ok",
        "coordinate_chemistry_fetch_error": None,
        "coordinate_chemistry_state_class": state_class,
        "nucleotide_codes_observed": nucleotide_codes,
        "active_gamma_codes_observed": sorted({atom["resname"] for atom in terminal_gamma_atoms}),
        "terminal_gamma_atom_count": len(terminal_gamma_atoms),
        "product_nucleotide_codes_observed": product_codes,
        "phosphorylated_sty_residue_count": len(phospho_residues),
        "phosphorylated_sty_near_nucleotide_count_le_8a": len(near_nucleotide_residues),
        "nearest_phosphorylated_sty_to_nucleotide_distance_angstrom": (
            round(nearest_distance, 3) if nearest_distance is not None else None
        ),
        "nearest_phosphorylated_sty_to_nucleotide_distance_class": distance_class(nearest_distance),
        "nearest_phosphorylated_sty_residue": (
            residue_label(nearest_residue) if nearest_residue is not None else None
        ),
        "nearest_nucleotide_atom_to_phosphorylated_sty": compact_nearest_nucleotide,
    }


def coordinate_chemistry_by_pdb(pdb_ids: set[str]) -> dict[str, dict[str, Any]]:
    return {pdb_id: coordinate_chemistry_scan(pdb_id) for pdb_id in sorted(pdb_ids)}


def review_state_context(row: dict[str, Any]) -> str:
    group = row["review_context_for_evaluation_only"].get("evaluation_group", "")
    if "product_state" in group or group.endswith("_product_state_positive"):
        return "review_product_state_context"
    if "ligand_analog" in group or "substrate_analog" in group:
        return "review_substrate_acceptor_analog_context"
    return "no_review_state_context"


def source_state_overlay(
    row: dict[str, Any],
    metal_row: dict[str, Any] | None,
) -> tuple[str, str, bool, bool, str | None]:
    source_state = row["source_free_evidence"]["coordinate_state"]
    if metal_row is None:
        return source_state, source_state, False, False, None
    metal_evidence = metal_row["source_free_evidence"]
    overlay_state = metal_evidence.get("coordinate_state", source_state)
    source_before_overlay = metal_evidence.get("source_coordinate_state", source_state)
    return overlay_state, source_before_overlay, overlay_state != source_before_overlay, False, (
        metal_evidence.get("gamma_metal_geometry", {}).get("gamma_metal_shell_class")
    )


def chemistry_state_overlay(
    source_state: str,
    chemistry: dict[str, Any],
) -> tuple[str, bool]:
    if (
        source_state == "adp_state"
        and chemistry.get("coordinate_chemistry_state_class")
        == "product_state_materialized_by_adp_and_near_phosphorylated_sty"
    ):
        return "product_state", True
    return source_state, False


def state_materialization_class(
    source_state: str,
    source_state_before_overlay: str,
    overlay_applied: bool,
    chemistry_overlay_applied: bool,
) -> str:
    if chemistry_overlay_applied and source_state == "product_state":
        return "source_free_product_state_materialized_by_coordinate_chemistry"
    if source_state == "active_gamma":
        return "source_free_active_gamma_materialized"
    if source_state == "metal_absent":
        return "source_free_active_gamma_materialized_but_metal_absent_overlay"
    if source_state == "adp_state":
        return "source_free_terminal_gamma_unavailable_adp_state"
    if source_state == "ligand_absent":
        return "source_free_ligand_absent"
    if source_state == "ambiguous_coordinate_state":
        return "source_free_ambiguous_nucleotide_without_terminal_gamma"
    if source_state == "product_state":
        return "source_free_product_state_materialized"
    if source_state == "substrate_acceptor_analog_state":
        return "source_free_substrate_acceptor_analog_materialized"
    if source_state == "split_state":
        return "source_free_split_state_materialized"
    if source_state == "unavailable_coordinate_state":
        return "source_free_unavailable_coordinate_state"
    if overlay_applied and source_state_before_overlay == "active_gamma":
        return "source_free_active_gamma_overlay_other"
    return "source_free_other_coordinate_state"


def leakage_guard(
    source_state: str,
    context: str,
) -> tuple[str, bool, str]:
    if context == "review_product_state_context":
        if source_state == "product_state":
            return (
                "review_product_context_has_source_free_product_state",
                False,
                "Product-state review context matches a source-free product-state coordinate row.",
            )
        return (
            "review_product_context_not_source_free_product_state",
            True,
            "Do not promote product-state identity from review context; source-free state remains non-product.",
        )
    if context == "review_substrate_acceptor_analog_context":
        if source_state == "substrate_acceptor_analog_state":
            return (
                "review_analog_context_has_source_free_analog_state",
                False,
                "Analog review context matches a source-free substrate-analog coordinate row.",
            )
        return (
            "review_analog_context_not_source_free_analog_state",
            True,
            "Do not promote substrate-analog identity from review context; source-free state remains non-analog.",
        )
    return (
        "no_review_state_claim_to_promote",
        False,
        "No product or analog review-state context is present.",
    )


def compact_source_free_evidence(
    row: dict[str, Any],
    metal_row: dict[str, Any] | None,
    chemistry: dict[str, Any],
) -> dict[str, Any]:
    evidence = row["source_free_evidence"]
    coordinate_state, source_state, overlay_applied, _, metal_shell = source_state_overlay(
        row,
        metal_row,
    )
    coordinate_state, chemistry_overlay_applied = chemistry_state_overlay(coordinate_state, chemistry)
    if coordinate_state not in COORDINATE_STATES:
        raise ValueError(f"unexpected coordinate_state: {coordinate_state}")
    blocker = evidence.get("blocker_class")
    if blocker not in BLOCKER_CLASSES:
        raise ValueError(f"unexpected blocker_class: {blocker}")
    certainty = evidence.get("coordinate_certainty")
    if isinstance(certainty, dict):
        certainty_class = certainty.get("coordinate_certainty_class")
    else:
        certainty_class = None
    orientation = evidence.get("orientation")
    if isinstance(orientation, dict):
        orientation_class = orientation.get("orientation_support_class")
    else:
        orientation_class = None
    exposure = evidence.get("exposure")
    if isinstance(exposure, dict):
        exposure_class = exposure.get("local_exposure_profile_class")
    else:
        exposure_class = None
    return {
        "coordinate_state": coordinate_state,
        "source_coordinate_state_before_metal_overlay": source_state,
        "metal_overlay_applied": overlay_applied,
        "gamma_metal_shell_class": metal_shell,
        "coordinate_state_materialization_class": state_materialization_class(
            coordinate_state,
            source_state,
            overlay_applied,
            chemistry_overlay_applied,
        ),
        "coordinate_chemistry_overlay_applied": chemistry_overlay_applied,
        "coordinate_chemistry": chemistry,
        "blocker_class": blocker,
        "candidate_role_class": evidence.get("candidate_role_class"),
        "ligand_state": evidence.get("ligand_state"),
        "availability_class": evidence.get("availability_class"),
        "terminal_gamma_atom": evidence.get("terminal_gamma_atom"),
        "acceptor_atom": evidence.get("acceptor_atom"),
        "distance_angstrom": evidence.get("distance_angstrom"),
        "reciprocal_context_class": evidence.get("reciprocal_context_class"),
        "same_chain_topology": evidence.get("same_chain_topology"),
        "cross_chain_topology": evidence.get("cross_chain_topology"),
        "ligand_acceptor_same_sequence_entity": evidence.get(
            "ligand_acceptor_same_sequence_entity"
        ),
        "acceptor_residue_code": evidence.get("acceptor_residue_code"),
        "acceptor_chain_is_short_peptide_like": evidence.get(
            "acceptor_chain_is_short_peptide_like"
        ),
        "acceptor_chain_is_folded_like": evidence.get("acceptor_chain_is_folded_like"),
        "coordinate_certainty_class": certainty_class,
        "orientation_support_class": orientation_class,
        "local_exposure_profile_class": exposure_class,
    }


def taxonomy_row(
    row: dict[str, Any],
    metal_row: dict[str, Any] | None,
    conflict_row: dict[str, Any] | None,
    chemistry: dict[str, Any],
) -> dict[str, Any]:
    context = review_state_context(row)
    source_free = compact_source_free_evidence(row, metal_row, chemistry)
    guard_class, prohibited, reason = leakage_guard(source_free["coordinate_state"], context)
    if context not in STATE_REVIEW_CONTEXTS:
        raise ValueError(f"unexpected review state context: {context}")
    return {
        "row_schema": "epk_candidate_coordinate_state_taxonomy_v1",
        "candidate_id": row["candidate_id"],
        "pdb_id": row["pdb_id"],
        "diagnostic_row_index": row["diagnostic_row_index"],
        "candidate_rank_within_8a": row.get("candidate_rank_within_8a"),
        "candidate_row_kind": (
            "state_only" if row["row_schema"].endswith("_state_only") else "gamma_acceptor_candidate"
        ),
        "source_free_evidence": source_free,
        "source_free_pdb_context": {
            "source_free_decision_class": (
                conflict_row or {}
            ).get("source_free_decision_class"),
            "conflict_class": (conflict_row or {}).get("conflict_class"),
            "non_abstaining_decision": (conflict_row or {}).get("non_abstaining_decision"),
            "source_free_conflict_signature": (
                conflict_row or {}
            ).get("source_free_conflict_signature"),
        },
        "review_context_for_evaluation_only": {
            "evaluation_label": row["review_context_for_evaluation_only"]["evaluation_label"],
            "evaluation_group": row["review_context_for_evaluation_only"]["evaluation_group"],
            "evaluation_label_used_only_for_eval": True,
            "source_artifact_id": row["review_context_for_evaluation_only"].get(
                "source_artifact_id"
            ),
            "review_state_context": context,
        },
        "source_leakage_guard_for_review_only": {
            "guard_class": guard_class,
            "promotion_from_review_context_prohibited": prohibited,
            "reason": reason,
        },
    }


def count_nested(rows: list[dict[str, Any]], path: tuple[str, ...]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value: Any = row
        for key in path:
            if not isinstance(value, dict):
                value = None
                break
            value = value.get(key)
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def source_free_state_gaps(rows: list[dict[str, Any]]) -> dict[str, Any]:
    observed = set()
    for row in rows:
        observed.add(row["source_free_evidence"]["coordinate_state"])
    missing = sorted(COORDINATE_STATES - observed)
    return {
        "observed_coordinate_states": sorted(observed),
        "missing_coordinate_states": missing,
        "source_free_product_state_observed": "product_state" in observed,
        "source_free_substrate_acceptor_analog_state_observed": (
            "substrate_acceptor_analog_state" in observed
        ),
        "source_free_split_state_observed": "split_state" in observed,
    }


def leakage_guard_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prohibited_rows = [
        row
        for row in rows
        if row["source_leakage_guard_for_review_only"]["promotion_from_review_context_prohibited"]
    ]
    return {
        "promotion_from_review_context_prohibited_count": len(prohibited_rows),
        "promotion_from_review_context_prohibited_pdb_ids": sorted(
            {row["pdb_id"] for row in prohibited_rows}
        ),
        "promotion_from_review_context_prohibited_candidate_ids": sorted(
            row["candidate_id"] for row in prohibited_rows
        ),
        "guard_class_counts": count_nested(
            rows,
            ("source_leakage_guard_for_review_only", "guard_class"),
        ),
    }


def confusion_from_conflict_rows(conflict_payload: dict[str, Any]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
        "abstained_positive": [],
        "abstained_negative": [],
    }
    decisions = []
    for row in conflict_payload["candidate_conflict_rows"]:
        label = row["review_context_for_evaluation_only"]["evaluation_label"]
        actual_positive = label == "positive_true_substrate_acceptor"
        decision = row["source_free_decision_class"]
        predicted_positive = decision == "source_free_structural_support_review_only"
        predicted_negative = decision == "source_free_blocked_counterevidence_review_only"
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif predicted_negative and not actual_positive:
            outcome = "true_negative"
        elif predicted_negative and actual_positive:
            outcome = "false_negative"
        elif actual_positive:
            outcome = "abstained_positive"
        else:
            outcome = "abstained_negative"
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "source_free_decision_class": decision,
                "outcome": outcome,
                "conflict_class": row["conflict_class"],
            }
        )
    return {
        "rule_id": "coordinate_state_source_separation_no_promotion_v1",
        "rule_description": (
            "Review-only projection of existing source-free conflict decisions after "
            "coordinate-state source separation. Product/analog review context is never "
            "promoted into a source-free coordinate-state claim."
        ),
        "row_level": "pdb",
        "production_claim_allowed": False,
        "clears_diagnostic_tranche": False,
        "confusion_matrix": {key: len(value) for key, value in buckets.items()},
        "pdb_ids_by_outcome": {key: sorted(value) for key, value in buckets.items()},
        "decisions": decisions,
    }


def hard_case_digest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    hard = {"1L0O", "3QHR", "3QHW", "3TM0", "7B56", "9UUR", "9UUX", "9UW4"}
    by_pdb: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["pdb_id"] not in hard:
            continue
        by_pdb.setdefault(row["pdb_id"], []).append(
            {
                "candidate_id": row["candidate_id"],
                "coordinate_state": row["source_free_evidence"]["coordinate_state"],
                "source_coordinate_state_before_metal_overlay": row["source_free_evidence"][
                    "source_coordinate_state_before_metal_overlay"
                ],
                "blocker_class": row["source_free_evidence"]["blocker_class"],
                "candidate_role_class": row["source_free_evidence"].get("candidate_role_class"),
                "review_state_context": row["review_context_for_evaluation_only"][
                    "review_state_context"
                ],
                "guard_class": row["source_leakage_guard_for_review_only"]["guard_class"],
            }
        )
    return dict(sorted(by_pdb.items()))


def build_payload(started_at: str, ended_at: str) -> dict[str, Any]:
    evidence_payload, metal_payload, conflict_payload = load_sources()
    metal_by_candidate = metal_rows_by_candidate(metal_payload)
    conflict_by_pdb = conflict_rows_by_pdb(conflict_payload)
    source_rows = all_candidate_rows(evidence_payload)
    chemistry_by_pdb = coordinate_chemistry_by_pdb({row["pdb_id"] for row in source_rows})
    taxonomy_rows = [
        taxonomy_row(
            row,
            metal_by_candidate.get(row["candidate_id"]),
            conflict_by_pdb.get(row["pdb_id"]),
            chemistry_by_pdb[row["pdb_id"]],
        )
        for row in source_rows
    ]

    coordinate_state_counts = count_nested(taxonomy_rows, ("source_free_evidence", "coordinate_state"))
    blocker_counts = count_nested(taxonomy_rows, ("source_free_evidence", "blocker_class"))
    review_state_context_counts = count_nested(
        taxonomy_rows,
        ("review_context_for_evaluation_only", "review_state_context"),
    )
    materialization_counts = count_nested(
        taxonomy_rows,
        ("source_free_evidence", "coordinate_state_materialization_class"),
    )
    chemistry_state_counts = count_nested(
        taxonomy_rows,
        ("source_free_evidence", "coordinate_chemistry", "coordinate_chemistry_state_class"),
    )
    rule = confusion_from_conflict_rows(conflict_payload)
    confusion_matrix = rule["confusion_matrix"]
    state_gaps = source_free_state_gaps(taxonomy_rows)
    leakage_summary = leakage_guard_summary(taxonomy_rows)
    measured = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60.0, 2)

    run_record = {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured,
        "hypothesis": (
            "A first-class coordinate-state source-separation overlay can reduce "
            "substrate-role uncertainty by marking which product/analog state claims "
            "are coordinate-materialized source-free and which would require review "
            "context leakage."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(source_rows),
            "reused_from_metal_transfer_geometry_artifact": len(metal_by_candidate),
            "reused_from_conflict_decision_artifact": len(
                conflict_payload["candidate_conflict_rows"]
            ),
            "coordinate_chemistry_scanned_pdbs": len(chemistry_by_pdb),
        },
        "candidate_evidence_rows_emitted": {
            "coordinate_state_taxonomy_rows": len(taxonomy_rows),
            "candidate_pair_rows_reused": len(evidence_payload["candidate_evidence_rows"]),
            "state_only_rows_reused": len(evidence_payload["state_only_rows"]),
        },
        "coordinate_states_observed": coordinate_state_counts,
        "source_free_features_tested": [
            "candidate-level coordinate-state source separation",
            "direct coordinate chemistry scan for terminal-gamma atoms, ADP, and phosphorylated STY residue materialization",
            "metal materialization overlay reused only as coordinate-state blocker evidence",
            "review-context product/analog leakage guard kept outside source-free evidence",
            "source-free coordinate-state gap audit for product_state, substrate_acceptor_analog_state, and split_state",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            rule["rule_id"]: {
                key: value for key, value in rule.items() if key != "decisions"
            },
            "coordinate_state_gap_audit_v1": {
                "production_claim_allowed": False,
                "clears_diagnostic_tranche": False,
                "rule_description": (
                    "Audit whether target coordinate states are source-free materialized "
                    "in candidate rows without promoting review product/analog context."
                ),
                **state_gaps,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "source_free_state_gaps": state_gaps,
            "source_leakage_guard_summary": leakage_summary,
            "hard_case_state_digest": hard_case_digest(taxonomy_rows),
            "hard_reciprocal_trio": ["9UUR", "9UUX", "9UW4"],
            "same_chain_topology_pair": ["3TM0", "6NOO"],
            "coordinate_chemistry_state_counts": chemistry_state_counts,
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": rule["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "interpretation": (
                "The taxonomy overlay introduces no new non-abstaining positive calls. "
                "Review-only product/analog context is blocked from becoming source-free "
                "state evidence."
            ),
        },
        "false_negative_analysis": {
            "non_abstaining_false_negative_pdb_ids": rule["pdb_ids_by_outcome"][
                "false_negative"
            ],
            "abstained_positive_pdb_ids": rule["pdb_ids_by_outcome"]["abstained_positive"],
            "interpretation": (
                "Known product/ADP and topology positives remain abstained rather than "
                "converted to active-gamma false negatives; source-free coordinate state "
                "does not independently materialize product_state or analog_state for "
                "review-labeled groups."
            ),
        },
        "blocker_classification": {
            "classification": "blocker_not_cleared_method_weakness",
            "primary_outcome": "candidate_evidence_rows_emitted",
            "coordinate_state_counts": coordinate_state_counts,
            "blocker_class_counts": blocker_counts,
            "review_state_context_counts_for_evaluation_only": review_state_context_counts,
            "coordinate_state_materialization_class_counts": materialization_counts,
            "coordinate_chemistry_state_class_counts": chemistry_state_counts,
            "source_leakage_guard_summary": leakage_summary,
            "interpretation": (
                "The coordinate-state taxonomy is useful review-routing evidence, but "
                "product/analog state identity cannot be promoted from review context. "
                "Topology and source-free product-state materialization remain blockers."
            ),
        },
        "next_query": (
            "Do not add scalar rescues. If this lane resumes, require a new source-free "
            "coordinate modality that directly materializes product/analog chemistry "
            "without review-context leakage; otherwise preserve source-reviewed adjudication."
        ),
        "primary_outcome": "candidate_evidence_rows_emitted",
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep the coordinate-state taxonomy as compact review-only evidence. Do not "
            "claim ePK production readiness, import labels, calibrate thresholds, or "
            "promote product/analog review groups into source-free substrate-role calls."
        ),
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "lane_id": LANE_ID,
            "created_at": ended_at,
            "source_artifacts": [
                str(SOURCE_EVIDENCE_ARTIFACT),
                str(SOURCE_METAL_ARTIFACT),
                str(SOURCE_CONFLICT_ARTIFACT),
            ],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "hypothesis": run_record["hypothesis"],
        "candidate_coordinate_state_taxonomy_rows": taxonomy_rows,
        "coordinate_state_counts": coordinate_state_counts,
        "blocker_class_counts": blocker_counts,
        "review_state_context_counts_for_evaluation_only": review_state_context_counts,
        "coordinate_state_materialization_class_counts": materialization_counts,
        "coordinate_chemistry_state_class_counts": chemistry_state_counts,
        "source_free_state_gaps": state_gaps,
        "source_leakage_guard_summary": leakage_summary,
        "rules": [rule],
        "feature_definitions": {
            "coordinate_state": (
                "Source-free coordinate state after the existing metal overlay. Review "
                "product/analog labels are not used to assign this field."
            ),
            "coordinate_state_materialization_class": (
                "Source-free materialization bucket for terminal gamma, ADP, missing "
                "ligand, ambiguous nucleotide, metal-absent overlay, or unavailable state."
            ),
            "coordinate_chemistry": (
                "Compact source-free coordinate scan for terminal gamma, ADP, and "
                "phosphorylated SER/THR/TYR residue materialization. It uses coordinates "
                "only and writes no raw coordinate dump."
            ),
            "source_leakage_guard_for_review_only": (
                "Evaluation-only comparison showing where review product/analog context "
                "would be forbidden as a predictive source-free input."
            ),
        },
        "run_record": run_record,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    args = parser.parse_args()

    ended_at = utc_now()
    payload = build_payload(args.started_at, ended_at)
    primary_outcome = payload["run_record"]["primary_outcome"]
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")
    write_json(args.output, payload)
    record = {
        "artifact_path": str(args.output),
        **payload["run_record"],
    }
    append_jsonl(args.ledger, record)
    print(json.dumps(payload["run_record"], sort_keys=True))


if __name__ == "__main__":
    main()
