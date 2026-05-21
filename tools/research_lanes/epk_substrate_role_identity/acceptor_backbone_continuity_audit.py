#!/usr/bin/env python3
"""Audit source-free acceptor backbone continuity for ePK candidates.

This lane-local helper tests one bounded coordinate modality: whether the
candidate acceptor residue is materially embedded in a continuous protein
backbone, at a resolved chain boundary, or in a chain-break/missing-backbone
context. It fetches structures in memory, writes compact reduced evidence only,
and does not promote backbone continuity into substrate-role identity calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
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
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
    residue_sort_key,
)


ARTIFACT_ID = "epk_acceptor_backbone_continuity_audit_v1_20260521"
SOURCE_CANDIDATE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
SOURCE_CONFLICT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_conflict_decision_v1_20260521.json"
)
SOURCE_PHOSPHOPRODUCT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_phosphoproduct_materialization_audit_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_acceptor_backbone_continuity_audit_v1_20260521.json"
)

HARD_CASE_PDBS = {
    "1L0O",
    "1QHA",
    "3QHR",
    "3QHW",
    "3TM0",
    "4HPU",
    "7B56",
    "9UUR",
    "9UUX",
    "9UW4",
}

STANDARD_AMINO_ACIDS = {
    "ALA",
    "ARG",
    "ASN",
    "ASP",
    "CYS",
    "GLN",
    "GLU",
    "GLY",
    "HIS",
    "ILE",
    "LEU",
    "LYS",
    "MET",
    "PHE",
    "PRO",
    "SER",
    "THR",
    "TRP",
    "TYR",
    "VAL",
}
PHOSPHO_ACCEPTOR_RESIDUES = {"SEP", "TPO", "PTR"}
POLYMER_LIKE_RESIDUES = STANDARD_AMINO_ACIDS | PHOSPHO_ACCEPTOR_RESIDUES
BACKBONE_ATOMS = {"N", "CA", "C", "O", "OXT"}
PEPTIDE_BOND_MAX_ANGSTROM = 1.7


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row["source_free_evidence"]


def review_label(row: dict[str, Any]) -> str:
    return row["review_context_for_evaluation_only"]["evaluation_label"]


def is_positive_label(label: str) -> bool:
    return label == "positive_true_substrate_acceptor"


def compact_key(compact_atom: dict[str, Any] | None) -> tuple[str, str, str, str, str] | None:
    if not compact_atom:
        return None
    return (
        compact_atom["atom_name"],
        compact_atom["residue_code"],
        compact_atom["chain_id"],
        str(compact_atom["auth_seq_id"]),
        compact_atom.get("icode") or "",
    )


def atom_key(atom: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        atom["atom_name"],
        atom["resname"],
        atom["chain"],
        str(atom["resseq"]),
        atom["icode"] or "",
    )


def residue_key_from_compact(compact_atom: dict[str, Any] | None) -> tuple[str, str, str, str] | None:
    if not compact_atom:
        return None
    return (
        compact_atom["chain_id"],
        str(compact_atom["auth_seq_id"]),
        compact_atom.get("icode") or "",
        compact_atom["residue_code"],
    )


def topology_class(e: dict[str, Any]) -> str:
    if e.get("same_chain_topology") is True:
        return "same_chain_topology"
    if e.get("cross_chain_topology") is True:
        return "cross_chain_topology"
    return "topology_unavailable"


def terminal_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
        return "internal_fragment_like_n_terminal"
    if e.get("acceptor_resolved_n_terminal_auth_terminal_like"):
        return "auth_terminal_like_n_terminal"
    if e.get("acceptor_is_n_terminal_sty"):
        return "resolved_n_terminal_sty_without_auth_support"
    return "not_resolved_n_terminal_sty"


def chain_size_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_chain_is_short_peptide_like"):
        return "short_peptide_like_acceptor_chain"
    if e.get("acceptor_chain_is_folded_like"):
        return "folded_like_acceptor_chain"
    return "acceptor_chain_size_unclassified"


def residue_class(e: dict[str, Any]) -> str:
    residue = e.get("acceptor_residue_code")
    if residue in {"TYR", "PTR"}:
        return "tyr_acceptor"
    if residue in {"SER", "THR", "SEP", "TPO"}:
        return "ser_thr_acceptor"
    if residue is None:
        return "no_acceptor_residue"
    return "other_acceptor_residue"


def count_class(value: int | None) -> str:
    if value is None:
        return "count_unavailable"
    if value == 0:
        return "zero"
    if value == 1:
        return "one"
    if value <= 3:
        return "two_or_three"
    return "four_or_more"


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def atom_maps(
    atoms: list[dict[str, Any]],
) -> tuple[
    dict[tuple[str, str, str, str], dict[str, dict[str, Any]]],
    dict[str, list[tuple[str, str, str, str]]],
]:
    residue_atoms: dict[tuple[str, str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    residues_by_chain: dict[str, set[tuple[str, str, str, str]]] = defaultdict(set)
    for atom in atoms:
        if atom["resname"] not in POLYMER_LIKE_RESIDUES:
            continue
        key = atom["residue_key"]
        residues_by_chain[atom["chain"]].add(key)
        if atom["atom_name"] not in residue_atoms[key]:
            residue_atoms[key][atom["atom_name"]] = atom
    sorted_residues = {
        chain: sorted(residues, key=residue_sort_key)
        for chain, residues in residues_by_chain.items()
    }
    return residue_atoms, sorted_residues


def peptide_side_state(
    left_atoms: dict[str, dict[str, Any]] | None,
    right_atoms: dict[str, dict[str, Any]] | None,
    left_name: str,
    right_name: str,
) -> tuple[str, float | None]:
    if left_atoms is None or right_atoms is None:
        return "resolved_chain_boundary_no_neighbor", None
    left_atom = left_atoms.get(left_name)
    right_atom = right_atoms.get(right_name)
    if left_atom is None or right_atom is None:
        return "neighbor_present_backbone_atom_missing", None
    distance = round(dist(left_atom, right_atom), 3)
    if distance <= PEPTIDE_BOND_MAX_ANGSTROM:
        return "peptide_bond_continuous", distance
    return "neighbor_present_peptide_bond_not_materialized", distance


def backbone_continuity_class(n_state: str, c_state: str) -> str:
    n_cont = n_state == "peptide_bond_continuous"
    c_cont = c_state == "peptide_bond_continuous"
    n_boundary = n_state == "resolved_chain_boundary_no_neighbor"
    c_boundary = c_state == "resolved_chain_boundary_no_neighbor"
    if n_cont and c_cont:
        return "internal_backbone_continuous"
    if n_boundary and c_cont:
        return "resolved_n_terminal_backbone_boundary"
    if n_cont and c_boundary:
        return "resolved_c_terminal_backbone_boundary"
    if n_boundary and c_boundary:
        return "isolated_residue_or_singleton_chain"
    return "backbone_break_or_missing_atom_context"


def resolved_position_class(n_state: str, c_state: str) -> str:
    n_boundary = n_state == "resolved_chain_boundary_no_neighbor"
    c_boundary = c_state == "resolved_chain_boundary_no_neighbor"
    if n_boundary and c_boundary:
        return "single_residue_or_isolated_resolved_position"
    if n_boundary:
        return "resolved_n_terminal_position"
    if c_boundary:
        return "resolved_c_terminal_position"
    return "internal_resolved_position"


def atom_completeness_class(current_atoms: dict[str, dict[str, Any]] | None) -> str:
    if current_atoms is None:
        return "acceptor_residue_unavailable"
    present = set(current_atoms)
    required = {"N", "CA", "C"}
    if required <= present and ("O" in present or "OXT" in present):
        return "complete_n_ca_c_o_backbone"
    if required <= present:
        return "n_ca_c_backbone_present_o_missing"
    if {"N", "CA"} <= present or {"CA", "C"} <= present:
        return "partial_backbone_two_core_atoms"
    return "sparse_or_missing_backbone_atoms"


def backbone_features_for_candidate(
    row: dict[str, Any],
    atoms: list[dict[str, Any]] | None,
    fetch_status: str,
    fetch_error: str | None,
) -> dict[str, Any]:
    e = evidence(row)
    acceptor_atom = e.get("acceptor_atom")
    if acceptor_atom is None:
        return {
            "backbone_continuity_status": "not_applicable_no_acceptor_atom",
            "backbone_fetch_status": fetch_status,
            "backbone_fetch_error": fetch_error,
            "acceptor_backbone_atom_completeness_class": "acceptor_residue_unavailable",
            "acceptor_backbone_atoms_present": [],
            "acceptor_position_class": "acceptor_position_unavailable",
            "n_side_state": "not_applicable_no_acceptor_atom",
            "c_side_state": "not_applicable_no_acceptor_atom",
            "n_side_peptide_bond_distance_angstrom": None,
            "c_side_peptide_bond_distance_angstrom": None,
            "backbone_continuity_class": "state_or_candidate_without_acceptor_atom",
            "resolved_chain_length": e.get("acceptor_chain_length"),
            "resolved_ordinal_in_chain": e.get("acceptor_residue_ordinal_in_chain"),
            "resolved_n_neighbor_residue": None,
            "resolved_c_neighbor_residue": None,
            "nearby_same_chain_backbone_atom_count_within_6a_of_acceptor": None,
        }
    if atoms is None:
        return {
            "backbone_continuity_status": "fetch_error",
            "backbone_fetch_status": fetch_status,
            "backbone_fetch_error": fetch_error,
            "acceptor_backbone_atom_completeness_class": "acceptor_residue_unavailable",
            "acceptor_backbone_atoms_present": [],
            "acceptor_position_class": "acceptor_position_unavailable",
            "n_side_state": "fetch_error",
            "c_side_state": "fetch_error",
            "n_side_peptide_bond_distance_angstrom": None,
            "c_side_peptide_bond_distance_angstrom": None,
            "backbone_continuity_class": "backbone_fetch_error",
            "resolved_chain_length": e.get("acceptor_chain_length"),
            "resolved_ordinal_in_chain": e.get("acceptor_residue_ordinal_in_chain"),
            "resolved_n_neighbor_residue": None,
            "resolved_c_neighbor_residue": None,
            "nearby_same_chain_backbone_atom_count_within_6a_of_acceptor": None,
        }

    residue_atoms, residues_by_chain = atom_maps(atoms)
    acceptor_key = residue_key_from_compact(acceptor_atom)
    chain = acceptor_atom["chain_id"]
    residues = residues_by_chain.get(chain, [])
    if acceptor_key not in residue_atoms or acceptor_key not in residues:
        return {
            "backbone_continuity_status": "acceptor_residue_not_found_in_polymer_model",
            "backbone_fetch_status": fetch_status,
            "backbone_fetch_error": fetch_error,
            "acceptor_backbone_atom_completeness_class": "acceptor_residue_unavailable",
            "acceptor_backbone_atoms_present": [],
            "acceptor_position_class": "acceptor_position_unavailable",
            "n_side_state": "acceptor_residue_not_found_in_polymer_model",
            "c_side_state": "acceptor_residue_not_found_in_polymer_model",
            "n_side_peptide_bond_distance_angstrom": None,
            "c_side_peptide_bond_distance_angstrom": None,
            "backbone_continuity_class": "acceptor_residue_not_found_in_polymer_model",
            "resolved_chain_length": len(residues),
            "resolved_ordinal_in_chain": None,
            "resolved_n_neighbor_residue": None,
            "resolved_c_neighbor_residue": None,
            "nearby_same_chain_backbone_atom_count_within_6a_of_acceptor": None,
        }

    index = residues.index(acceptor_key)
    previous_key = residues[index - 1] if index > 0 else None
    next_key = residues[index + 1] if index + 1 < len(residues) else None
    current_atoms = residue_atoms[acceptor_key]
    previous_atoms = residue_atoms.get(previous_key) if previous_key else None
    next_atoms = residue_atoms.get(next_key) if next_key else None

    n_state, n_distance = peptide_side_state(previous_atoms, current_atoms, "C", "N")
    c_state, c_distance = peptide_side_state(current_atoms, next_atoms, "C", "N")
    continuity_class = backbone_continuity_class(n_state, c_state)
    position_class = resolved_position_class(n_state, c_state)

    acceptor_match_key = compact_key(acceptor_atom)
    selected_acceptor_atom = None
    for atom in atoms:
        if atom_key(atom) == acceptor_match_key:
            selected_acceptor_atom = atom
            break
    nearby_count = None
    if selected_acceptor_atom is not None:
        nearby_count = sum(
            1
            for key, atoms_by_name in residue_atoms.items()
            if key[0] == chain
            for atom_name, atom in atoms_by_name.items()
            if atom_name in BACKBONE_ATOMS and dist(atom, selected_acceptor_atom) <= 6.0
        )

    def compact_residue(key: tuple[str, str, str, str] | None) -> dict[str, Any] | None:
        if key is None:
            return None
        return {
            "chain_id": key[0],
            "auth_seq_id": key[1],
            "icode": key[2] or None,
            "residue_code": key[3],
        }

    return {
        "backbone_continuity_status": "ok",
        "backbone_fetch_status": fetch_status,
        "backbone_fetch_error": fetch_error,
        "acceptor_backbone_atom_completeness_class": atom_completeness_class(current_atoms),
        "acceptor_backbone_atoms_present": sorted(set(current_atoms) & BACKBONE_ATOMS),
        "acceptor_position_class": position_class,
        "n_side_state": n_state,
        "c_side_state": c_state,
        "n_side_peptide_bond_distance_angstrom": n_distance,
        "c_side_peptide_bond_distance_angstrom": c_distance,
        "backbone_continuity_class": continuity_class,
        "resolved_chain_length": len(residues),
        "resolved_ordinal_in_chain": index + 1,
        "resolved_n_neighbor_residue": compact_residue(previous_key),
        "resolved_c_neighbor_residue": compact_residue(next_key),
        "nearby_same_chain_backbone_atom_count_within_6a_of_acceptor": nearby_count,
    }


def backbone_materiality_class(e: dict[str, Any], features: dict[str, Any]) -> str:
    state = e.get("coordinate_state")
    if state in {"product_state", "adp_state", "split_state", "substrate_acceptor_analog_state"}:
        return f"{state}_backbone_context_review_only"
    if state != "active_gamma":
        return f"{state or 'unknown_state'}_no_active_gamma_backbone_context"
    continuity = features["backbone_continuity_class"]
    if continuity == "internal_backbone_continuous":
        if e.get("same_chain_topology"):
            return "same_chain_internal_continuous_backbone"
        if (e.get("reciprocal_context_class") or "").startswith("reciprocal_"):
            return "reciprocal_folded_internal_continuous_backbone"
        if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
            return "cross_chain_internal_fragment_continuous_backbone"
        return "cross_chain_folded_internal_continuous_backbone"
    if continuity == "resolved_n_terminal_backbone_boundary":
        if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
            return "internal_fragment_n_boundary_backbone"
        if e.get("acceptor_resolved_n_terminal_auth_terminal_like"):
            return "auth_terminal_n_boundary_backbone"
        return "resolved_n_boundary_without_auth_terminal_support"
    if continuity == "resolved_c_terminal_backbone_boundary":
        return "resolved_c_boundary_backbone"
    if continuity == "isolated_residue_or_singleton_chain":
        return "isolated_or_singleton_backbone"
    if continuity == "backbone_break_or_missing_atom_context":
        return "chain_break_or_missing_backbone_context"
    return continuity


def backbone_blocker_class(e: dict[str, Any], materiality_class: str) -> str:
    state = e.get("coordinate_state")
    if state in {"product_state", "adp_state"}:
        return "product_state_evidence"
    if state == "substrate_acceptor_analog_state":
        return "substrate_analog_evidence"
    if state == "split_state":
        return "split_state_evidence"
    if state in {"ligand_absent", "unavailable_coordinate_state", "ambiguous_coordinate_state"}:
        return "ligand_materialization"
    if "internal_fragment" in materiality_class and not e.get("acceptor_chain_is_short_peptide_like"):
        return "internal_fragment_mimicry"
    if e.get("same_chain_topology") or (e.get("reciprocal_context_class") or "").startswith("reciprocal_"):
        return "topology_ambiguity"
    if e.get("blocker_class") == "none":
        return "none"
    return e.get("blocker_class") or "active_gamma_geometry"


def backbone_signature(
    row: dict[str, Any],
    features: dict[str, Any],
    materiality_class: str,
) -> dict[str, Any]:
    e = evidence(row)
    return {
        "coordinate_state": e.get("coordinate_state"),
        "topology_class": topology_class(e),
        "candidate_role_class": e.get("candidate_role_class") or "state_only",
        "reciprocal_context_class": e.get("reciprocal_context_class") or "none",
        "acceptor_residue_class": residue_class(e),
        "acceptor_terminal_class": terminal_class(e),
        "acceptor_chain_size_class": chain_size_class(e),
        "backbone_materiality_class": materiality_class,
        "backbone_continuity_class": features["backbone_continuity_class"],
        "acceptor_position_class": features["acceptor_position_class"],
        "acceptor_backbone_atom_completeness_class": features[
            "acceptor_backbone_atom_completeness_class"
        ],
        "nearby_same_chain_backbone_atom_count_6a_class": count_class(
            features["nearby_same_chain_backbone_atom_count_within_6a_of_acceptor"]
        ),
    }


def build_backbone_row(
    row: dict[str, Any],
    atoms_by_pdb: dict[str, list[dict[str, Any]] | None],
    fetch_status_by_pdb: dict[str, tuple[str, str | None]],
) -> dict[str, Any]:
    pdb_id = row["pdb_id"]
    fetch_status, fetch_error = fetch_status_by_pdb[pdb_id]
    e = evidence(row)
    features = backbone_features_for_candidate(
        row, atoms_by_pdb[pdb_id], fetch_status, fetch_error
    )
    materiality_class = backbone_materiality_class(e, features)
    signature = backbone_signature(row, features, materiality_class)
    blocker_class = backbone_blocker_class(e, materiality_class)
    return {
        "candidate_id": row["candidate_id"],
        "diagnostic_row_index": row.get("diagnostic_row_index"),
        "pdb_id": pdb_id,
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
        "row_schema": "epk_acceptor_backbone_continuity_audit_v1",
        "source_free_evidence": {
            "coordinate_state": e.get("coordinate_state"),
            "source_blocker_class": e.get("blocker_class"),
            "blocker_class": blocker_class,
            "candidate_role_class": e.get("candidate_role_class") or "state_only",
            "topology_class": topology_class(e),
            "same_chain_topology": e.get("same_chain_topology"),
            "cross_chain_topology": e.get("cross_chain_topology"),
            "reciprocal_context_class": e.get("reciprocal_context_class"),
            "distance_angstrom": e.get("distance_angstrom"),
            "acceptor_atom": e.get("acceptor_atom"),
            "acceptor_residue_code": e.get("acceptor_residue_code"),
            "acceptor_chain_length": e.get("acceptor_chain_length"),
            "acceptor_chain_is_short_peptide_like": e.get("acceptor_chain_is_short_peptide_like"),
            "acceptor_chain_is_folded_like": e.get("acceptor_chain_is_folded_like"),
            "acceptor_resolved_n_terminal_auth_terminal_like": e.get(
                "acceptor_resolved_n_terminal_auth_terminal_like"
            ),
            "acceptor_resolved_n_terminal_internal_fragment_like": e.get(
                "acceptor_resolved_n_terminal_internal_fragment_like"
            ),
            "backbone_continuity": features,
            "backbone_materiality_class": materiality_class,
            "backbone_continuity_signature": signature,
            "backbone_continuity_signature_id": stable_signature_id(signature),
        },
    }


def merged_input_rows(
    candidate_payload: dict[str, Any],
    phosphoproduct_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = candidate_payload["candidate_evidence_rows"] + candidate_payload.get(
        "state_only_rows", []
    )
    seen_candidate_ids = {row["candidate_id"] for row in rows}
    for row in phosphoproduct_payload["phosphoproduct_materialization_rows"]:
        if row["candidate_row_kind"] == "terminal_gamma_context":
            continue
        if row["candidate_id"] in seen_candidate_ids:
            continue
        rows.append(row)
        seen_candidate_ids.add(row["candidate_id"])
    return rows


def label_collision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[evidence(row)["backbone_continuity_signature_id"]].append(row)

    collisions = []
    for signature_id, group in sorted(grouped.items()):
        labels = Counter(review_label(row) for row in group)
        positives = labels.get("positive_true_substrate_acceptor", 0)
        negatives = labels.get("counterexample_not_true_substrate_acceptor", 0)
        if positives and negatives:
            collision_class = "mixed_positive_counterexample_backbone_signature"
        elif positives:
            collision_class = "positive_only_backbone_signature"
        else:
            collision_class = "counterexample_only_backbone_signature"
        collisions.append(
            {
                "backbone_continuity_signature_id": signature_id,
                "backbone_continuity_signature": evidence(group[0])[
                    "backbone_continuity_signature"
                ],
                "collision_class": collision_class,
                "label_counts_for_evaluation_only": dict(sorted(labels.items())),
                "candidate_count": len(group),
                "pdb_ids": sorted({row["pdb_id"] for row in group}),
                "hard_case_candidate_ids": sorted(
                    row["candidate_id"]
                    for row in group
                    if row["pdb_id"] in HARD_CASE_PDBS
                ),
            }
        )
    return collisions


def project_no_promotion_confusion(
    conflict_payload: dict[str, Any],
) -> tuple[dict[str, int], dict[str, list[str]]]:
    confusion = Counter()
    pdb_ids_by_outcome: dict[str, list[str]] = defaultdict(list)
    for row in conflict_payload["candidate_conflict_rows"]:
        label = row["review_context_for_evaluation_only"]["evaluation_label"]
        decision = row["source_free_decision_class"]
        if decision == "source_free_structural_support_review_only":
            outcome = "true_positive" if is_positive_label(label) else "false_positive"
        elif decision == "source_free_blocked_counterevidence_review_only":
            outcome = "false_negative" if is_positive_label(label) else "true_negative"
        elif is_positive_label(label):
            outcome = "abstained_positive"
        else:
            outcome = "abstained_negative"
        confusion[outcome] += 1
        pdb_ids_by_outcome[outcome].append(row["pdb_id"])
    ordered = {
        "true_positive": confusion["true_positive"],
        "false_positive": confusion["false_positive"],
        "true_negative": confusion["true_negative"],
        "false_negative": confusion["false_negative"],
        "abstained_positive": confusion["abstained_positive"],
        "abstained_negative": confusion["abstained_negative"],
    }
    return ordered, {key: sorted(value) for key, value in pdb_ids_by_outcome.items()}


def pdb_backbone_digest(rows: list[dict[str, Any]], pdb_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
    digest: dict[str, list[dict[str, Any]]] = {}
    for pdb_id in sorted(pdb_ids):
        pdb_rows = [row for row in rows if row["pdb_id"] == pdb_id]
        if not pdb_rows:
            continue
        digest[pdb_id] = [
            {
                "candidate_id": row["candidate_id"],
                "coordinate_state": evidence(row)["coordinate_state"],
                "blocker_class": evidence(row)["blocker_class"],
                "source_blocker_class": evidence(row)["source_blocker_class"],
                "candidate_role_class": evidence(row)["candidate_role_class"],
                "topology_class": evidence(row)["topology_class"],
                "backbone_materiality_class": evidence(row)["backbone_materiality_class"],
                "backbone_continuity_signature_id": evidence(row)[
                    "backbone_continuity_signature_id"
                ],
                "backbone_continuity": evidence(row)["backbone_continuity"],
            }
            for row in pdb_rows
        ]
    return digest


def build_payload(workflow_started_at: str, append_ledger: bool) -> dict[str, Any]:
    started_at = workflow_started_at
    script_started_at = utc_now()
    candidate_payload = load_json(SOURCE_CANDIDATE_ARTIFACT)
    conflict_payload = load_json(SOURCE_CONFLICT_ARTIFACT)
    phosphoproduct_payload = load_json(SOURCE_PHOSPHOPRODUCT_ARTIFACT)
    input_rows = merged_input_rows(candidate_payload, phosphoproduct_payload)

    atoms_by_pdb: dict[str, list[dict[str, Any]] | None] = {}
    fetch_status_by_pdb: dict[str, tuple[str, str | None]] = {}
    for pdb_id in sorted({row["pdb_id"] for row in input_rows}):
        text, fetch_error = fetch_pdb_text(pdb_id)
        if text is None:
            atoms_by_pdb[pdb_id] = None
            fetch_status_by_pdb[pdb_id] = ("error", fetch_error)
        else:
            atoms_by_pdb[pdb_id] = parse_pdb_atoms(text)
            fetch_status_by_pdb[pdb_id] = ("ok", None)

    backbone_rows = [
        build_backbone_row(row, atoms_by_pdb, fetch_status_by_pdb)
        for row in input_rows
    ]
    state_only_rows = [
        row for row in backbone_rows if evidence(row)["candidate_role_class"] == "state_only"
    ]
    candidate_pair_rows = [
        row for row in backbone_rows if evidence(row)["candidate_role_class"] != "state_only"
    ]
    collision_rows = label_collision_rows(backbone_rows)
    mixed_collision_rows = [
        row
        for row in collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_backbone_signature"
    ]
    hard_digest = pdb_backbone_digest(backbone_rows, HARD_CASE_PDBS)
    confusion_matrix, pdb_ids_by_outcome = project_no_promotion_confusion(conflict_payload)

    coordinate_state_counts = Counter(
        evidence(row)["coordinate_state"] for row in backbone_rows
    )
    blocker_class_counts = Counter(evidence(row)["blocker_class"] for row in backbone_rows)
    materiality_counts = Counter(
        evidence(row)["backbone_materiality_class"] for row in backbone_rows
    )
    continuity_counts = Counter(
        evidence(row)["backbone_continuity"]["backbone_continuity_class"]
        for row in backbone_rows
    )
    signature_collision_counts = Counter(row["collision_class"] for row in collision_rows)
    fetch_counts = Counter(status for status, _ in fetch_status_by_pdb.values())

    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60, 2)
    primary_outcome = "candidate_evidence_rows_emitted"
    run_record = {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "artifact_path": str(DEFAULT_OUTPUT_PATH),
        "hypothesis": (
            "A source-free acceptor backbone-continuity audit can separate resolved "
            "terminal/boundary acceptor contexts from internal continuous folded-chain "
            "or chain-break contexts, while testing whether those signatures still "
            "collide between review positives and counterexamples."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(
                candidate_payload["candidate_evidence_rows"]
                + candidate_payload.get("state_only_rows", [])
            ),
            "reused_from_phosphoproduct_materialization_artifact": len(
                phosphoproduct_payload["phosphoproduct_materialization_rows"]
            ),
            "reused_from_conflict_decision_artifact": len(
                conflict_payload["candidate_conflict_rows"]
            ),
            "coordinate_pdbs_scanned": len(atoms_by_pdb),
        },
        "candidate_evidence_rows_emitted": {
            "acceptor_backbone_continuity_rows": len(backbone_rows),
            "candidate_pair_rows": len(candidate_pair_rows),
            "state_only_rows": len(state_only_rows),
            "nonterminal_phosphoproduct_state_rows_reemitted": len(input_rows)
            - len(candidate_payload["candidate_evidence_rows"])
            - len(candidate_payload.get("state_only_rows", [])),
            "backbone_signature_rows": len(collision_rows),
            "mixed_backbone_signature_rows": len(mixed_collision_rows),
        },
        "coordinate_states_observed": dict(sorted(coordinate_state_counts.items())),
        "source_free_features_tested": [
            "resolved acceptor backbone atom completeness for N/CA/C/O atoms",
            "fixed 1.7A C-N peptide-bond continuity on both acceptor residue sides",
            "resolved terminal, internal, singleton, and chain-break acceptor contexts",
            "phosphoproduct product/split acceptor backbone context re-emitted as review-only state evidence",
            "backbone-continuity signature collision audit with review labels used only after grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "acceptor_backbone_continuity_no_promotion_v1": {
                "rule_id": "acceptor_backbone_continuity_no_promotion_v1",
                "rule_description": (
                    "Emit acceptor backbone-continuity rows and keep the existing "
                    "source-free conflict abstention policy; backbone signatures are "
                    "not promoted to substrate-role identity calls."
                ),
                "new_threshold_or_rescue_rule_added": False,
                "clears_diagnostic_tranche": False,
                "confusion_matrix": confusion_matrix,
                "pdb_ids_by_outcome": pdb_ids_by_outcome,
                "production_claim_allowed": False,
            },
            "backbone_continuity_signature_collision_audit_v1": {
                "rule_id": "backbone_continuity_signature_collision_audit_v1",
                "rule_description": (
                    "Group source-free backbone-continuity signatures before evaluating "
                    "review labels; mixed positive/counterexample signatures block "
                    "source-free promotion."
                ),
                "backbone_signature_count": len(collision_rows),
                "mixed_backbone_signature_count": len(mixed_collision_rows),
                "collision_class_counts": dict(sorted(signature_collision_counts.items())),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "same_chain_internal_backbone_overlap": (
                "Internal continuous same-chain backbone contexts appear in both "
                "review-positive topology rows and counterexample pressure rows, so "
                "backbone continuity is not substrate-role identity."
            ),
            "9UUR_9UUX_9UW4_reciprocal_backbone_overlap": (
                "The reciprocal folded-chain Tyr candidates in 9UUR, 9UUX, and 9UW4 "
                "all remain internal continuous backbone contexts."
            ),
            "product_and_split_state_backbone_context": (
                "3QHR/3QHW product rows and 4HPU split rows can materialize acceptor "
                "backbone, but state chemistry remains review-only blocker evidence."
            ),
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": pdb_ids_by_outcome.get("false_positive", []),
            "interpretation": (
                "No new non-abstaining positive calls were introduced. Backbone "
                "continuity collides across positives and counterexamples, so it is "
                "compact review-routing evidence only."
            ),
        },
        "false_negative_analysis": {
            "abstained_positive_pdb_ids": pdb_ids_by_outcome.get("abstained_positive", []),
            "non_abstaining_false_negative_pdb_ids": pdb_ids_by_outcome.get("false_negative", []),
            "interpretation": (
                "Product/ADP, reciprocal folded-chain, and same-chain analog/topology "
                "positives remain abstained rather than converted to active-gamma false negatives."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
            "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
            "backbone_materiality_class_counts": dict(sorted(materiality_counts.items())),
            "backbone_continuity_class_counts": dict(sorted(continuity_counts.items())),
            "backbone_signature_collision_class_counts": dict(
                sorted(signature_collision_counts.items())
            ),
            "interpretation": (
                "Acceptor backbone continuity can distinguish resolved boundary, chain "
                "break, and internal folded-chain contexts, but the internal contexts "
                "still mix source-reviewed positives with counterexamples."
            ),
        },
        "next_query": (
            "Stop backbone-continuity probing as a promotion route. Only resume this "
            "lane for a genuinely new source-free modality that can adjudicate ADP/"
            "product, substrate-analog, reciprocal folded-chain, or same-chain biology "
            "without review-context leakage."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep acceptor backbone-continuity rows as compact review-only blocker "
            "evidence. Do not claim ePK production readiness or promote backbone "
            "materialization into substrate-role calls."
        ),
    }
    payload = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": script_started_at,
            "source_artifacts": [
                str(SOURCE_CANDIDATE_ARTIFACT),
                str(SOURCE_CONFLICT_ARTIFACT),
                str(SOURCE_PHOSPHOPRODUCT_ARTIFACT),
            ],
            "candidate_evidence_row_count": len(backbone_rows),
            "candidate_pair_row_count": len(candidate_pair_rows),
            "state_only_row_count": len(state_only_rows),
            "diagnostic_pdb_count": len(atoms_by_pdb),
            "raw_coordinate_files_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "review_only": True,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "acceptor_backbone_atom_completeness_class": (
                "Whether the candidate acceptor residue has compact resolved N/CA/C/O "
                "backbone materialization in model 1."
            ),
            "n_side_state": (
                "Whether the previous resolved residue C atom forms a fixed 1.7A "
                "peptide-bond contact with the candidate residue N atom."
            ),
            "c_side_state": (
                "Whether the candidate residue C atom forms a fixed 1.7A peptide-bond "
                "contact with the next resolved residue N atom."
            ),
            "backbone_materiality_class": (
                "Categorical backbone-continuity route used only for blocker triage and "
                "signature collision checks."
            ),
        },
        "backbone_fetch_status_counts": dict(sorted(fetch_counts.items())),
        "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
        "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
        "backbone_materiality_class_counts": dict(sorted(materiality_counts.items())),
        "backbone_continuity_class_counts": dict(sorted(continuity_counts.items())),
        "backbone_signature_collision_class_counts": dict(sorted(signature_collision_counts.items())),
        "acceptor_backbone_continuity_rows": backbone_rows,
        "backbone_signature_collision_rows": collision_rows,
        "hard_case_backbone_digest": hard_digest,
        "run_record": run_record,
        "rules": run_record["rule_results"],
    }
    if append_ledger:
        append_jsonl(LEDGER_PATH, run_record)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--no-append-ledger", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args.started_at, append_ledger=not args.no_append_ledger)
    write_json(args.output, payload)
    print(json.dumps(payload["run_record"], sort_keys=True))


if __name__ == "__main__":
    main()
