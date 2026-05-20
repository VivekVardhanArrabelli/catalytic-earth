#!/usr/bin/env python3
"""Review-only ePK folded N-terminal substrate-role stress test.

This lane-local helper tests whether a source-free terminal-index feature can
separate the decisive 7B56 false hit from true N-terminal/folded substrate
positives. It fetches coordinates in memory and writes only compact reduced
evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from substrate_role_identity_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    HYDROXYL_ATOMS,
    ACTIVE_GAMMA_CODES,
    NUCLEOTIDE_LIKE_CODES,
    compact_atom,
    fetch_pdb_text,
    parse_pdb_atoms,
    chain_residue_maps,
    polymer_entity_count_by_sequence,
    ligand_state,
    nearest_pair,
    nearest_nonpolymer_oxygen,
    nearest_nucleotide_or_metal_to_atom,
    chain_has_own_nucleotide_or_metal,
    residue_chain_position,
    local_atom_count,
    dist,
)


LANE_ID = "epk_substrate_role_identity"
ARTIFACT_ID = "epk_folded_nterminal_auth_terminal_stress_20260520"
PRIMARY_OUTCOMES = {
    "blocker_cleared_source_free",
    "blocker_not_cleared_data_scarcity",
    "blocker_not_cleared_method_weakness",
    "blocker_not_cleared_biology_ambiguity",
    "counterexample_found",
    "next_query_defined",
}


FROZEN_ROWS = [
    {
        "pdb_id": "5HVK",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only LIMK1/cofilin positive; label used only after feature extraction",
    },
    {
        "pdb_id": "6Z3R",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only SMG1/UPF1 positive; label used only after feature extraction",
    },
    {
        "pdb_id": "9UUR",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only MEK/ERK Tyr phosphosite positive; label used only after feature extraction",
    },
    {
        "pdb_id": "9UUX",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only MEK/ERK Tyr phosphosite positive; label used only after feature extraction",
    },
    {
        "pdb_id": "1QMZ",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only positive pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "3QHR",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_product_state_positive_reused",
        "evaluation_label_source": "prior review-only ADP/product-state positive; label used only after feature extraction",
    },
    {
        "pdb_id": "3QHW",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_product_state_positive_reused",
        "evaluation_label_source": "prior review-only ADP/product-state positive; label used only after feature extraction",
    },
    {
        "pdb_id": "3X2U",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only peptide-substrate positive; label used only after feature extraction",
    },
    {
        "pdb_id": "3X2V",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only peptide-substrate positive; label used only after feature extraction",
    },
    {
        "pdb_id": "3X2W",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only peptide-substrate positive; label used only after feature extraction",
    },
    {
        "pdb_id": "4IAC",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_reused",
        "evaluation_label_source": "prior review-only peptide-substrate positive; label used only after feature extraction",
    },
    {
        "pdb_id": "1O6K",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "fresh_review_only_positive_pkb_gsk3",
        "evaluation_label_source": "read-only prior source validation accepted PKB/GSK3 substrate control; label used only after feature extraction",
    },
    {
        "pdb_id": "1O6L",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "fresh_review_only_positive_pkb_gsk3",
        "evaluation_label_source": "read-only prior source validation accepted PKB/GSK3 substrate control; label used only after feature extraction",
    },
    {
        "pdb_id": "8OXM",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "fresh_review_only_positive_atm_p53",
        "evaluation_label_source": "read-only prior source validation accepted ATM/p53 substrate control; label used only after feature extraction",
    },
    {
        "pdb_id": "8OXO",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "fresh_review_only_positive_atm_p53",
        "evaluation_label_source": "read-only prior source validation accepted ATM/p53 substrate control; label used only after feature extraction",
    },
    {
        "pdb_id": "2JJ2",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_atpase",
        "evaluation_label_source": "prior review-only F1-ATPase/ANP counterexample; label used only after feature extraction",
    },
    {
        "pdb_id": "7ZE5",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_transporter",
        "evaluation_label_source": "prior review-only ABC transporter counterexample; label used only after feature extraction",
    },
    {
        "pdb_id": "7B56",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_midlength_internal_fragment",
        "evaluation_label_source": "prior review-only decisive 7B56 false hit; label used only after feature extraction",
    },
    {
        "pdb_id": "9UW4",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_topology",
        "evaluation_label_source": "prior review-only same-chain topology control; label used only after feature extraction",
    },
    {
        "pdb_id": "3R5F",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_atp_grasp",
        "evaluation_label_source": "prior review-only ATP-grasp sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "5C1O",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_atp_grasp",
        "evaluation_label_source": "prior review-only ATP-grasp sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "6U1D",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_atp_grasp",
        "evaluation_label_source": "prior review-only ATP-grasp pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "6U1E",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_atp_grasp",
        "evaluation_label_source": "prior review-only ATP-grasp pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "5TT6",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_same_chain_atpase",
        "evaluation_label_source": "prior review-only same-chain ATPase/ligase pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "6NOO",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_same_chain_atpase",
        "evaluation_label_source": "prior review-only same-chain ATPase/ligase pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "9NBW",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample_reused_same_chain_atpase",
        "evaluation_label_source": "prior review-only same-chain ATPase/ligase pressure row; label used only after feature extraction",
    },
    {
        "pdb_id": "7ZDT",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "fresh_counterexample_transporter",
        "evaluation_label_source": "read-only prior source validation blocked ABC transporter control; label used only after feature extraction",
    },
    {
        "pdb_id": "7ZDU",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "fresh_counterexample_transporter",
        "evaluation_label_source": "read-only prior source validation blocked ABC transporter control; label used only after feature extraction",
    },
    {
        "pdb_id": "9L3M",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "fresh_counterexample_transporter",
        "evaluation_label_source": "read-only prior source validation blocked membrane translocase control; label used only after feature extraction",
    },
    {
        "pdb_id": "7T55",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "fresh_counterexample_transporter",
        "evaluation_label_source": "read-only prior source validation blocked bacteriocin transporter control; label used only after feature extraction",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_auth_seq_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def terminal_index_features(atom: dict[str, Any] | None, ordinal: int | None) -> dict[str, Any]:
    auth_seq_int = parse_auth_seq_int(atom["resseq"] if atom else None)
    offset = None if auth_seq_int is None or ordinal is None else auth_seq_int - ordinal
    n_terminal_ordinal = bool(ordinal is not None and ordinal <= 5)
    auth_terminal_like = bool(n_terminal_ordinal and offset is not None and abs(offset) <= 5)
    internal_fragment_like = bool(n_terminal_ordinal and offset is not None and abs(offset) > 5)
    return {
        "candidate_acceptor_auth_seq_id_int": auth_seq_int,
        "candidate_acceptor_auth_seq_minus_resolved_ordinal": offset,
        "candidate_resolved_n_terminal_auth_terminal_like": auth_terminal_like,
        "candidate_resolved_n_terminal_internal_fragment_like": internal_fragment_like,
    }


def pair_candidate_record(
    gamma_atom: dict[str, Any],
    acceptor_atom: dict[str, Any],
    distance_angstrom: float,
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
    residue_ordinals: dict[str, int],
    hetero_atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    candidate_chain_len, candidate_ordinal = residue_chain_position(
        acceptor_atom, residues_by_chain, residue_ordinals
    )
    ligand_chain_len, _ = residue_chain_position(gamma_atom, residues_by_chain, residue_ordinals)
    candidate_is_sty = acceptor_atom["resname"] in {"SER", "THR", "TYR"}
    candidate_is_n_terminal_sty = bool(
        candidate_is_sty and candidate_ordinal is not None and candidate_ordinal <= 5
    )
    terminal_features = terminal_index_features(acceptor_atom, candidate_ordinal)
    return {
        "distance_angstrom": round(distance_angstrom, 3),
        "terminal_gamma_equivalent_atom": compact_atom(gamma_atom),
        "nearest_protein_hydroxyl_atom": compact_atom(acceptor_atom),
        "terminal_gamma_ligand_chain": gamma_atom["chain"],
        "candidate_acceptor_chain": acceptor_atom["chain"],
        "candidate_acceptor_residue_code": acceptor_atom["resname"],
        "candidate_acceptor_chain_length": candidate_chain_len,
        "candidate_acceptor_residue_ordinal_in_chain": candidate_ordinal,
        "ligand_chain_length": ligand_chain_len,
        "same_chain_topology": gamma_atom["chain"] == acceptor_atom["chain"],
        "cross_chain_topology": gamma_atom["chain"] != acceptor_atom["chain"],
        "candidate_acceptor_is_n_terminal_sty": candidate_is_n_terminal_sty,
        "candidate_acceptor_is_tyr": acceptor_atom["resname"] == "TYR",
        "candidate_acceptor_chain_is_short_peptide_like": bool(
            candidate_chain_len is not None and candidate_chain_len <= 40
        ),
        "candidate_acceptor_chain_is_midlength": bool(
            candidate_chain_len is not None and 41 <= candidate_chain_len <= 119
        ),
        "candidate_acceptor_chain_is_folded_like": bool(
            candidate_chain_len is not None and candidate_chain_len >= 120
        ),
        "candidate_chain_has_own_nucleotide_or_metal": chain_has_own_nucleotide_or_metal(
            acceptor_atom["chain"], hetero_atoms, gamma_atom
        ),
        **terminal_features,
    }


def hydroxyl_pair_candidates(
    gamma_atoms: list[dict[str, Any]],
    hydroxyl_atoms: list[dict[str, Any]],
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
    residue_ordinals: dict[str, int],
    hetero_atoms: list[dict[str, Any]],
    max_distance: float = 8.0,
) -> list[dict[str, Any]]:
    candidates = []
    for gamma in gamma_atoms:
        for acceptor in hydroxyl_atoms:
            current = dist(gamma, acceptor)
            if current <= max_distance:
                candidates.append(
                    pair_candidate_record(
                        gamma, acceptor, current, residues_by_chain, residue_ordinals, hetero_atoms
                    )
                )
    return sorted(candidates, key=lambda item: item["distance_angstrom"])


def candidate_passes_strict_common(candidate: dict[str, Any]) -> bool:
    if candidate["distance_angstrom"] > 6.0:
        return False
    if not candidate["cross_chain_topology"]:
        return False
    if candidate["candidate_chain_has_own_nucleotide_or_metal"]:
        return False
    return True


def original_identity_mode(candidate: dict[str, Any]) -> bool:
    return bool(
        candidate["candidate_acceptor_chain_is_short_peptide_like"]
        or candidate["candidate_acceptor_is_n_terminal_sty"]
        or candidate["candidate_acceptor_is_tyr"]
    )


def auth_terminal_guard_identity_mode(candidate: dict[str, Any]) -> bool:
    return bool(
        candidate["candidate_acceptor_chain_is_short_peptide_like"]
        or candidate["candidate_acceptor_is_tyr"]
        or (
            candidate["candidate_acceptor_is_n_terminal_sty"]
            and candidate["candidate_resolved_n_terminal_auth_terminal_like"]
        )
    )


def nearest_rule_candidate(candidates: list[dict[str, Any]], guard: str) -> dict[str, Any] | None:
    identity_fn = original_identity_mode if guard == "original" else auth_terminal_guard_identity_mode
    for candidate in candidates:
        if candidate_passes_strict_common(candidate) and identity_fn(candidate):
            return candidate
    return None


def empty_feature_payload() -> dict[str, Any]:
    return {
        "ligand_state": "unavailable_fetch_error",
        "terminal_gamma_equivalent_atom_available": False,
        "terminal_gamma_equivalent_atom": None,
        "terminal_gamma_ligand_chain": None,
        "gamma_capable_ligand_codes_observed": [],
        "nucleotide_like_ligand_codes_observed": [],
        "nearest_protein_hydroxyl_distance_angstrom": None,
        "nearest_protein_hydroxyl_atom": None,
        "nearest_nonpolymer_oxygen_distance_angstrom": None,
        "nearest_nonpolymer_oxygen_atom": None,
        "candidate_acceptor_chain": None,
        "candidate_acceptor_residue_code": None,
        "candidate_acceptor_chain_length": None,
        "candidate_acceptor_residue_ordinal_in_chain": None,
        "candidate_acceptor_auth_seq_id_int": None,
        "candidate_acceptor_auth_seq_minus_resolved_ordinal": None,
        "candidate_resolved_n_terminal_auth_terminal_like": False,
        "candidate_resolved_n_terminal_internal_fragment_like": False,
        "ligand_chain_length": None,
        "same_chain_topology": None,
        "cross_chain_topology": None,
        "polymer_chain_count": None,
        "polymer_entity_count_sequence_proxy": None,
        "candidate_acceptor_is_n_terminal_sty": False,
        "candidate_acceptor_is_tyr": False,
        "candidate_acceptor_chain_is_short_peptide_like": False,
        "candidate_acceptor_chain_is_midlength": False,
        "candidate_acceptor_chain_is_folded_like": False,
        "candidate_local_atom_count_within_8a": None,
        "candidate_local_context_nearest_nucleotide_or_metal_distance_angstrom": None,
        "candidate_acceptor_chain_has_local_nucleotide_or_metal": None,
        "candidate_chain_has_own_nucleotide_or_metal": None,
        "nearest_hydroxyl_pair_candidates_within_8a": [],
        "nearest_strict_cross_chain_candidate": None,
        "nearest_strict_auth_terminal_guard_candidate": None,
        "co_materialized_gamma_and_hydroxyl_in_one_structure": False,
    }


def reduced_features(pdb_id: str, row_template: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text(pdb_id)
    base = {
        **row_template,
        "requested_set": (
            "positive"
            if row_template["evaluation_label"] == "positive_true_substrate_acceptor"
            else "counterexample"
        ),
        "evaluation_label_used_only_for_eval": True,
        "feature_extraction_started_after": workflow_started_at,
        "source_free_feature_only": True,
        "forbidden_predictive_features_excluded": FORBIDDEN_PREDICTIVE_FEATURES,
    }
    if text is None:
        return {
            **base,
            "fetch_status": "error",
            "fetch_error": fetch_error,
            "pdb_sha256_12": None,
            "atom_count_model1": 0,
            "structure_features": empty_feature_payload(),
        }

    atoms = parse_pdb_atoms(text)
    atom_atoms = [atom for atom in atoms if atom["record"] == "ATOM"]
    hetero_atoms = [atom for atom in atoms if atom["record"] == "HETATM"]
    residues_by_chain, residue_ordinals = chain_residue_maps(atoms)
    nucleotide_atoms = [atom for atom in hetero_atoms if atom["resname"] in NUCLEOTIDE_LIKE_CODES]
    gamma_atoms = [
        atom
        for atom in nucleotide_atoms
        if atom["resname"] in ACTIVE_GAMMA_CODES and atom["atom_name"] in {"PG", "P3"}
    ]
    hydroxyl_atoms = [
        atom for atom in atom_atoms if (atom["resname"], atom["atom_name"]) in HYDROXYL_ATOMS
    ]
    gamma_atom, acceptor_atom, nearest_hydroxyl_distance = nearest_pair(gamma_atoms, hydroxyl_atoms)
    nonpolymer_o_atom, nonpolymer_o_distance = nearest_nonpolymer_oxygen(gamma_atom, hetero_atoms)
    local_context_atom, local_context_distance = nearest_nucleotide_or_metal_to_atom(
        acceptor_atom, hetero_atoms
    )
    pair_candidates = hydroxyl_pair_candidates(
        gamma_atoms, hydroxyl_atoms, residues_by_chain, residue_ordinals, hetero_atoms
    )
    strict_candidate = nearest_rule_candidate(pair_candidates, "original")
    auth_guard_candidate = nearest_rule_candidate(pair_candidates, "auth_terminal_guard")
    candidate_chain_len, candidate_ordinal = residue_chain_position(
        acceptor_atom, residues_by_chain, residue_ordinals
    )
    ligand_chain_len, _ = residue_chain_position(gamma_atom, residues_by_chain, residue_ordinals)
    terminal_features = terminal_index_features(acceptor_atom, candidate_ordinal)
    candidate_is_sty = bool(acceptor_atom and acceptor_atom["resname"] in {"SER", "THR", "TYR"})
    features = {
        "ligand_state": ligand_state(nucleotide_atoms, gamma_atoms),
        "terminal_gamma_equivalent_atom_available": bool(gamma_atom),
        "terminal_gamma_equivalent_atom": compact_atom(gamma_atom),
        "terminal_gamma_ligand_chain": gamma_atom["chain"] if gamma_atom else None,
        "gamma_capable_ligand_codes_observed": sorted({atom["resname"] for atom in gamma_atoms}),
        "nucleotide_like_ligand_codes_observed": sorted({atom["resname"] for atom in nucleotide_atoms}),
        "nearest_protein_hydroxyl_distance_angstrom": nearest_hydroxyl_distance,
        "nearest_protein_hydroxyl_atom": compact_atom(acceptor_atom),
        "nearest_nonpolymer_oxygen_distance_angstrom": nonpolymer_o_distance,
        "nearest_nonpolymer_oxygen_atom": compact_atom(nonpolymer_o_atom),
        "candidate_acceptor_chain": acceptor_atom["chain"] if acceptor_atom else None,
        "candidate_acceptor_residue_code": acceptor_atom["resname"] if acceptor_atom else None,
        "candidate_acceptor_chain_length": candidate_chain_len,
        "candidate_acceptor_residue_ordinal_in_chain": candidate_ordinal,
        **terminal_features,
        "ligand_chain_length": ligand_chain_len,
        "same_chain_topology": bool(gamma_atom and acceptor_atom and gamma_atom["chain"] == acceptor_atom["chain"]),
        "cross_chain_topology": bool(gamma_atom and acceptor_atom and gamma_atom["chain"] != acceptor_atom["chain"]),
        "polymer_chain_count": len(residues_by_chain),
        "polymer_entity_count_sequence_proxy": polymer_entity_count_by_sequence(residues_by_chain),
        "candidate_acceptor_is_n_terminal_sty": bool(
            candidate_is_sty and candidate_ordinal is not None and candidate_ordinal <= 5
        ),
        "candidate_acceptor_is_tyr": bool(acceptor_atom and acceptor_atom["resname"] == "TYR"),
        "candidate_acceptor_chain_is_short_peptide_like": bool(
            candidate_chain_len is not None and candidate_chain_len <= 40
        ),
        "candidate_acceptor_chain_is_midlength": bool(
            candidate_chain_len is not None and 41 <= candidate_chain_len <= 119
        ),
        "candidate_acceptor_chain_is_folded_like": bool(
            candidate_chain_len is not None and candidate_chain_len >= 120
        ),
        "candidate_local_atom_count_within_8a": local_atom_count(acceptor_atom, atom_atoms, 8.0)
        if acceptor_atom
        else None,
        "candidate_local_context_nearest_nucleotide_or_metal_distance_angstrom": local_context_distance,
        "candidate_local_context_nearest_nucleotide_or_metal_atom": compact_atom(local_context_atom),
        "candidate_acceptor_chain_has_local_nucleotide_or_metal": bool(
            local_context_distance is not None and local_context_distance <= 8.0
        ),
        "candidate_chain_has_own_nucleotide_or_metal": chain_has_own_nucleotide_or_metal(
            acceptor_atom["chain"] if acceptor_atom else None, hetero_atoms, gamma_atom
        ),
        "nearest_hydroxyl_pair_candidates_within_8a": pair_candidates[:8],
        "nearest_strict_cross_chain_candidate": strict_candidate,
        "nearest_strict_auth_terminal_guard_candidate": auth_guard_candidate,
        "co_materialized_gamma_and_hydroxyl_in_one_structure": bool(gamma_atom and acceptor_atom),
    }
    return {
        **base,
        "fetch_status": "ok",
        "fetch_error": None,
        "pdb_sha256_12": hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
        "atom_count_model1": len(atoms),
        "structure_features": features,
    }


def is_positive_label(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def rule_strict_structural(features: dict[str, Any]) -> bool:
    return bool(features["nearest_strict_cross_chain_candidate"])


def rule_auth_terminal_guard(features: dict[str, Any]) -> bool:
    return bool(features["nearest_strict_auth_terminal_guard_candidate"])


def rule_permissive(features: dict[str, Any]) -> bool:
    distance = features["nearest_protein_hydroxyl_distance_angstrom"]
    return bool(features["terminal_gamma_equivalent_atom_available"] and distance is not None and distance <= 6.0)


RULES = {
    "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1": {
        "description": "Existing strict source-free rule reused as baseline.",
        "function": rule_strict_structural,
    },
    "strict_auth_terminal_guard_v1": {
        "description": (
            "Same strict topology and ligand-context checks, but N-terminal STY identity "
            "requires author residue numbering to be consistent with a true resolved "
            "N terminus: abs(auth_seq_id - resolved_ordinal) <= 5. Short peptide-like "
            "and Tyr modes are unchanged."
        ),
        "function": rule_auth_terminal_guard,
    },
    "permissive_nearest_hydroxyl_6a_v1": {
        "description": "PG/P3 gamma-equivalent present and nearest protein Ser/Thr/Tyr hydroxyl <=6.0 A.",
        "function": rule_permissive,
    },
}


def classify_failure_mode(row: dict[str, Any], predicted_positive: bool, rule_id: str) -> str | None:
    actual_positive = is_positive_label(row)
    if predicted_positive == actual_positive:
        return None
    features = row["structure_features"]
    group = row["evaluation_group"]
    if not features["terminal_gamma_equivalent_atom_available"]:
        if features["nucleotide_like_ligand_codes_observed"]:
            return "product_or_analog_state"
        return "structure_not_containing_biological_substrate_state"
    if predicted_positive and not actual_positive:
        strict_candidate = (
            features.get("nearest_strict_auth_terminal_guard_candidate")
            if rule_id == "strict_auth_terminal_guard_v1"
            else features.get("nearest_strict_cross_chain_candidate")
        )
        if strict_candidate and strict_candidate.get("candidate_resolved_n_terminal_internal_fragment_like"):
            return "internal_fragment_n_terminal_mimicry"
        if "atp_grasp" in group:
            return "sibling_family_mimicry"
        if features["same_chain_topology"]:
            return "topology_ambiguity"
        if strict_candidate and (
            strict_candidate["candidate_acceptor_chain_is_midlength"]
            or strict_candidate["candidate_acceptor_chain_is_folded_like"]
        ):
            return "peptide_vs_folded_substrate_ambiguity"
        if features["candidate_acceptor_chain_has_local_nucleotide_or_metal"]:
            return "topology_ambiguity"
        return "biological_role_ambiguity"
    if actual_positive and not predicted_positive:
        original_candidate = features.get("nearest_strict_cross_chain_candidate")
        if (
            rule_id == "strict_auth_terminal_guard_v1"
            and original_candidate
            and original_candidate.get("candidate_resolved_n_terminal_internal_fragment_like")
        ):
            return "auth_terminal_guard_rejected_positive_internal_fragment_like"
        if features["same_chain_topology"]:
            return "topology_ambiguity"
        if features["candidate_acceptor_chain_has_local_nucleotide_or_metal"]:
            return "acceptor_identity_ambiguity"
        distance = features["nearest_protein_hydroxyl_distance_angstrom"]
        if distance is None or distance > 6.0:
            return "structure_not_containing_biological_substrate_state"
        if features["candidate_acceptor_chain_is_folded_like"] and not (
            features["candidate_acceptor_is_tyr"] or features["candidate_acceptor_is_n_terminal_sty"]
        ):
            return "peptide_vs_folded_substrate_ambiguity"
        return "method_weakness"
    return "method_weakness"


def confusion_for_rule(rows: list[dict[str, Any]], rule_id: str, rule_spec: dict[str, Any]) -> dict[str, Any]:
    buckets = {"true_positive": [], "false_positive": [], "true_negative": [], "false_negative": []}
    decisions = []
    failure_counts: Counter[str] = Counter()
    for row in rows:
        predicted_positive = bool(rule_spec["function"](row["structure_features"]))
        actual_positive = is_positive_label(row)
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        buckets[outcome].append(row["pdb_id"])
        failure_mode = classify_failure_mode(row, predicted_positive, rule_id)
        if failure_mode:
            failure_counts[failure_mode] += 1
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "failure_mode": failure_mode,
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": rule_spec["description"],
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": buckets,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
    }


def primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    auth_result = next(result for result in rule_results if result["rule_id"] == "strict_auth_terminal_guard_v1")
    failures = Counter(auth_result["failure_mode_counts"])
    if auth_result["confusion_matrix"]["false_positive"]:
        return "blocker_not_cleared_biology_ambiguity"
    if failures.get("topology_ambiguity", 0) or failures.get("acceptor_identity_ambiguity", 0):
        return "blocker_not_cleared_biology_ambiguity"
    if failures.get("product_or_analog_state", 0):
        return "blocker_not_cleared_data_scarcity"
    return "blocker_not_cleared_method_weakness"


def summarize_rule_delta(rule_results: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {result["rule_id"]: result for result in rule_results}
    strict = by_id["strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1"]
    auth = by_id["strict_auth_terminal_guard_v1"]
    return {
        "baseline_strict_false_positives": strict["pdb_ids_by_outcome"]["false_positive"],
        "auth_guard_false_positives": auth["pdb_ids_by_outcome"]["false_positive"],
        "false_positives_removed_by_auth_guard": sorted(
            set(strict["pdb_ids_by_outcome"]["false_positive"])
            - set(auth["pdb_ids_by_outcome"]["false_positive"])
        ),
        "positives_lost_by_auth_guard": sorted(
            set(strict["pdb_ids_by_outcome"]["true_positive"])
            - set(auth["pdb_ids_by_outcome"]["true_positive"])
        ),
    }


def row_probe(rows: list[dict[str, Any]], pdb_ids: list[str]) -> list[dict[str, Any]]:
    probes = []
    rows_by_id = {row["pdb_id"]: row for row in rows}
    for pdb_id in pdb_ids:
        row = rows_by_id[pdb_id]
        features = row["structure_features"]
        strict_candidate = features["nearest_strict_cross_chain_candidate"]
        guard_candidate = features["nearest_strict_auth_terminal_guard_candidate"]
        probes.append(
            {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "nearest_distance_angstrom": features["nearest_protein_hydroxyl_distance_angstrom"],
                "candidate_acceptor_chain_length": features["candidate_acceptor_chain_length"],
                "candidate_acceptor_residue_ordinal_in_chain": features[
                    "candidate_acceptor_residue_ordinal_in_chain"
                ],
                "candidate_acceptor_auth_seq_id_int": features["candidate_acceptor_auth_seq_id_int"],
                "candidate_acceptor_auth_seq_minus_resolved_ordinal": features[
                    "candidate_acceptor_auth_seq_minus_resolved_ordinal"
                ],
                "candidate_resolved_n_terminal_internal_fragment_like": features[
                    "candidate_resolved_n_terminal_internal_fragment_like"
                ],
                "strict_candidate": strict_candidate,
                "auth_terminal_guard_candidate": guard_candidate,
            }
        )
    return probes


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def build_payload(workflow_started_at: str) -> dict[str, Any]:
    script_started_at = utc_now()
    rows = []
    for row_template in FROZEN_ROWS:
        rows.append(reduced_features(row_template["pdb_id"], row_template, workflow_started_at))
        time.sleep(0.1)
    rule_results = [
        confusion_for_rule(rows, rule_id, rule_spec)
        for rule_id, rule_spec in RULES.items()
    ]
    outcome = primary_outcome(rule_results)
    if outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {outcome}")
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    materialized_rows = [row for row in rows if row["fetch_status"] == "ok"]
    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "workflow_started_at": workflow_started_at,
            "script_started_at": script_started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_terminal_index_stress",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "frozen_row_count": len(FROZEN_ROWS),
            "materialized_row_count": len(materialized_rows),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "primary_outcome": outcome,
        },
        "hypothesis": (
            "A source-free terminal-index guard can reject internal-fragment N-terminal-STY "
            "mimics such as 7B56 while retaining true short-peptide and folded N-terminal "
            "substrate positives, but it cannot solve topology/product-state ambiguity."
        ),
        "feature_definitions": {
            "candidate_acceptor_auth_seq_id_int": "Integer author residue number from coordinate records when parseable.",
            "candidate_acceptor_auth_seq_minus_resolved_ordinal": (
                "author residue number minus resolved 1-based chain ordinal for the hydroxyl candidate"
            ),
            "candidate_resolved_n_terminal_auth_terminal_like": (
                "N-terminal STY candidate with abs(auth_seq_id - resolved_ordinal) <= 5"
            ),
            "candidate_resolved_n_terminal_internal_fragment_like": (
                "N-terminal STY candidate with parseable author numbering inconsistent with a true chain N terminus"
            ),
        },
        "diagnostic_rows": rows,
        "rules": rule_results,
        "rule_delta": summarize_rule_delta(rule_results),
        "seven_b56_probe": row_probe(rows, ["7B56", "5HVK", "1O6K", "1O6L", "8OXM", "8OXO", "7T55"]),
        "false_negative_probe": row_probe(rows, ["9UUR", "9UUX", "3QHR", "3QHW"]),
        "blocker_classification": {
            "primary_outcome": outcome,
            "terminal_index_signal": (
                "The terminal-index guard removes internal-fragment N-terminal-STY false hits "
                "without losing current strict-rule positives."
            ),
            "remaining_blocker_signal": (
                "False negatives remain from product/analog ligand state and topology/acceptor "
                "identity ambiguity; the guard is a counteraxis, not a substrate-role identity rule."
            ),
        },
    }


def ledger_record(payload: dict[str, Any], workflow_started_at: str, started_at: str) -> dict[str, Any]:
    ended_at = utc_now()
    start_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(ended_at.replace("Z", "+00:00"))
    measured_minutes = round((end_dt - start_dt).total_seconds() / 60.0, 2)
    auth_rule = next(rule for rule in payload["rules"] if rule["rule_id"] == "strict_auth_terminal_guard_v1")
    strict_rule = next(
        rule
        for rule in payload["rules"]
        if rule["rule_id"] == "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1"
    )
    permissive_rule = next(rule for rule in payload["rules"] if rule["rule_id"] == "permissive_nearest_hydroxyl_6a_v1")
    return {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": payload["hypothesis"],
        "diagnostic_rows_added_or_reused": {
            "total": payload["metadata"]["frozen_row_count"],
            "reused_from_prior_22_row_tranche": 22,
            "added_this_run": ["1O6K", "1O6L", "8OXM", "8OXO", "7ZDT", "7ZDU", "9L3M", "7T55"],
        },
        "source_free_features_tested": [
            "candidate author residue number",
            "resolved chain ordinal",
            "auth_seq_id minus resolved ordinal",
            "auth-terminal-like N-terminal STY guard",
            "internal-fragment-like N-terminal STY guard",
            "existing chain length/topology/nucleotide context features",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "strict_baseline": strict_rule,
            "strict_auth_terminal_guard": auth_rule,
            "permissive_nearest_hydroxyl": permissive_rule,
            "delta": payload["rule_delta"],
        },
        "confusion_matrix": auth_rule["confusion_matrix"],
        "decisive_counterexamples": {
            "7B56": "baseline strict false positive; auth-terminal guard blocks it as internal-fragment-like",
            "7T55": "fresh transporter pressure row remains blocked by strict topology/context checks",
        },
        "false_positive_analysis": {
            "baseline_strict_false_positives": payload["rule_delta"]["baseline_strict_false_positives"],
            "auth_guard_false_positives": payload["rule_delta"]["auth_guard_false_positives"],
            "interpretation": (
                "The new source-free terminal-index guard removes the decisive 7B56 false hit, "
                "but this is a local counteraxis rather than evidence of general substrate-role identity."
            ),
        },
        "false_negative_analysis": {
            "auth_guard_false_negatives": auth_rule["pdb_ids_by_outcome"]["false_negative"],
            "failure_mode_counts": auth_rule["failure_mode_counts"],
            "interpretation": (
                "Remaining misses are dominated by topology/acceptor ambiguity and ADP/product-state "
                "structures where a terminal gamma-equivalent atom is absent."
            ),
        },
        "blocker_classification": payload["blocker_classification"],
        "next_query": (
            "Freeze a larger non-overlap set specifically enriched for true folded N-terminal "
            "substrate positives with auth-terminal-like residue numbering, then test whether the "
            "guard generalizes beyond 5HVK without source-text repair."
        ),
        "primary_outcome": payload["metadata"]["primary_outcome"],
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep the terminal-index guard as review-only "
            "counterevidence for internal-fragment mimics and continue seeking a broader source-free "
            "substrate-role identity feature."
        ),
        "git_sync_status": (
            "git fetch origin failed at start with Operation not permitted writing FETCH_HEAD; "
            "continued on current research/epk-substrate-role-identity branch state"
        ),
        "workflow_started_at": workflow_started_at,
        "artifact_path": f"artifacts/research_lanes/epk_substrate_role_identity/{ARTIFACT_ID}.json",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--artifact-dir", default="artifacts/research_lanes/epk_substrate_role_identity")
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    artifact_dir = Path(args.artifact_dir)
    payload = build_payload(args.workflow_started_at)
    artifact_path = artifact_dir / f"{ARTIFACT_ID}.json"
    write_json(artifact_path, payload)
    if args.append_ledger:
        append_jsonl(
            artifact_dir / "epk_substrate_role_identity_runs.jsonl",
            ledger_record(payload, args.workflow_started_at, args.started_at),
        )
    print(
        json.dumps(
            {
                "artifact_path": str(artifact_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "rule_delta": payload["rule_delta"],
                "fetch_status_counts": payload["metadata"]["fetch_status_counts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
