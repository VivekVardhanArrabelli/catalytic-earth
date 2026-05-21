#!/usr/bin/env python3
"""Audit source-free active-site contact-interface materialization.

This lane-local helper tests one bounded coordinate modality: whether the
candidate acceptor chain materially occupies the nucleotide/gamma active-site
interface. It fetches structures in memory, writes compact reduced evidence
only, and does not promote contact materialization into substrate-role calls.
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
    NUCLEOTIDE_LIKE_CODES,
    WATER_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_active_site_contact_interface_audit_v1_20260521"
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
    "epk_active_site_contact_interface_audit_v1_20260521.json"
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

HARD_CASE_PDBS = {
    "1L0O",
    "3QHR",
    "3QHW",
    "3TM0",
    "4HPU",
    "7B56",
    "9UUR",
    "9UUX",
    "9UW4",
}


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


def heavy(atom: dict[str, Any]) -> bool:
    return atom["element"] != "H"


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


def find_atom(atoms: list[dict[str, Any]], compact_atom: dict[str, Any] | None) -> dict[str, Any] | None:
    key = compact_key(compact_atom)
    if key is None:
        return None
    for atom in atoms:
        if atom_key(atom) == key:
            return atom
    return None


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
    if residue == "TYR":
        return "tyr_acceptor"
    if residue in {"SER", "THR"}:
        return "ser_thr_acceptor"
    if residue is None:
        return "no_acceptor_residue"
    return "other_acceptor_residue"


def contact_materiality_class(e: dict[str, Any], features: dict[str, Any]) -> str:
    state = e.get("coordinate_state")
    if state != "active_gamma":
        return f"{state or 'unknown_state'}_no_active_gamma_interface"
    if features["contact_interface_status"] != "ok":
        return features["contact_interface_status"]
    if e.get("same_chain_topology"):
        if features["acceptor_chain_residue_count_within_6a_of_gamma"] >= 6:
            return "same_chain_broad_intramolecular_active_site_contact"
        return "same_chain_local_intramolecular_active_site_contact"
    if e.get("candidate_chain_active_gamma_count") or e.get("candidate_chain_has_own_nucleotide_or_metal"):
        return "cross_chain_reciprocal_nucleotide_bearing_interface"
    if e.get("acceptor_chain_is_short_peptide_like") or e.get(
        "acceptor_resolved_n_terminal_auth_terminal_like"
    ):
        return "cross_chain_terminal_or_short_peptide_interface"
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
        return "cross_chain_internal_fragment_contact"
    if features["ligand_chain_acceptor_chain_contact_pair_count_le_4a"] >= 4:
        return "cross_chain_extended_folded_interface"
    return "cross_chain_sparse_hydroxyl_contact"


def contact_blocker_class(e: dict[str, Any], materiality_class: str) -> str:
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


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def contact_features_for_candidate(
    row: dict[str, Any],
    atoms: list[dict[str, Any]] | None,
    fetch_status: str,
    fetch_error: str | None,
) -> dict[str, Any]:
    e = evidence(row)
    state = e.get("coordinate_state")
    if state != "active_gamma":
        return {
            "contact_interface_status": f"not_applicable_{state or 'unknown_state'}",
            "contact_interface_fetch_status": fetch_status,
            "contact_interface_fetch_error": fetch_error,
            "acceptor_chain_residue_count_within_6a_of_gamma": None,
            "acceptor_chain_residue_count_within_8a_of_gamma": None,
            "acceptor_chain_nonself_residue_count_within_8a_of_gamma": None,
            "ligand_chain_residue_count_within_8a_of_gamma": None,
            "ligand_chain_acceptor_chain_contact_pair_count_le_4a": None,
            "nucleotide_heavy_atom_count_within_4a_of_acceptor_atom": None,
            "nucleotide_heavy_atom_count_within_6a_of_acceptor_atom": None,
            "nonwater_hetero_heavy_atom_count_within_6a_of_acceptor_atom": None,
        }
    if atoms is None:
        return {
            "contact_interface_status": "fetch_error",
            "contact_interface_fetch_status": fetch_status,
            "contact_interface_fetch_error": fetch_error,
            "acceptor_chain_residue_count_within_6a_of_gamma": None,
            "acceptor_chain_residue_count_within_8a_of_gamma": None,
            "acceptor_chain_nonself_residue_count_within_8a_of_gamma": None,
            "ligand_chain_residue_count_within_8a_of_gamma": None,
            "ligand_chain_acceptor_chain_contact_pair_count_le_4a": None,
            "nucleotide_heavy_atom_count_within_4a_of_acceptor_atom": None,
            "nucleotide_heavy_atom_count_within_6a_of_acceptor_atom": None,
            "nonwater_hetero_heavy_atom_count_within_6a_of_acceptor_atom": None,
        }

    if e.get("terminal_gamma_atom") is None or e.get("acceptor_atom") is None:
        return {
            "contact_interface_status": "active_gamma_no_acceptor_candidate",
            "contact_interface_fetch_status": fetch_status,
            "contact_interface_fetch_error": fetch_error,
            "acceptor_chain_residue_count_within_6a_of_gamma": None,
            "acceptor_chain_residue_count_within_8a_of_gamma": None,
            "acceptor_chain_nonself_residue_count_within_8a_of_gamma": None,
            "ligand_chain_residue_count_within_8a_of_gamma": None,
            "ligand_chain_acceptor_chain_contact_pair_count_le_4a": None,
            "nucleotide_heavy_atom_count_within_4a_of_acceptor_atom": None,
            "nucleotide_heavy_atom_count_within_6a_of_acceptor_atom": None,
            "nonwater_hetero_heavy_atom_count_within_6a_of_acceptor_atom": None,
        }

    gamma_atom = find_atom(atoms, e.get("terminal_gamma_atom"))
    acceptor_atom = find_atom(atoms, e.get("acceptor_atom"))
    if gamma_atom is None or acceptor_atom is None:
        return {
            "contact_interface_status": "candidate_atom_not_resolved",
            "contact_interface_fetch_status": fetch_status,
            "contact_interface_fetch_error": fetch_error,
            "acceptor_chain_residue_count_within_6a_of_gamma": None,
            "acceptor_chain_residue_count_within_8a_of_gamma": None,
            "acceptor_chain_nonself_residue_count_within_8a_of_gamma": None,
            "ligand_chain_residue_count_within_8a_of_gamma": None,
            "ligand_chain_acceptor_chain_contact_pair_count_le_4a": None,
            "nucleotide_heavy_atom_count_within_4a_of_acceptor_atom": None,
            "nucleotide_heavy_atom_count_within_6a_of_acceptor_atom": None,
            "nonwater_hetero_heavy_atom_count_within_6a_of_acceptor_atom": None,
        }

    heavy_atoms = [atom for atom in atoms if heavy(atom)]
    protein_atoms = [atom for atom in heavy_atoms if atom["record"] == "ATOM"]
    hetero_atoms = [atom for atom in heavy_atoms if atom["record"] == "HETATM"]
    acceptor_chain = acceptor_atom["chain"]
    ligand_chain = gamma_atom["chain"]
    acceptor_residue_key = acceptor_atom["residue_key"]
    gamma_residue_key = gamma_atom["residue_key"]

    acceptor_chain_atoms = [
        atom for atom in protein_atoms if atom["chain"] == acceptor_chain
    ]
    ligand_chain_protein_atoms = [
        atom for atom in protein_atoms if atom["chain"] == ligand_chain
    ]
    acceptor_residues_6 = {
        atom["residue_key"] for atom in acceptor_chain_atoms if dist(atom, gamma_atom) <= 6.0
    }
    acceptor_residues_8 = {
        atom["residue_key"] for atom in acceptor_chain_atoms if dist(atom, gamma_atom) <= 8.0
    }
    ligand_residues_8 = {
        atom["residue_key"] for atom in ligand_chain_protein_atoms if dist(atom, gamma_atom) <= 8.0
    }
    contact_pairs: set[tuple[tuple[str, str, str, str], tuple[str, str, str, str]]] = set()
    if acceptor_chain != ligand_chain:
        acceptor_interface_atoms = [
            atom for atom in acceptor_chain_atoms if dist(atom, gamma_atom) <= 10.0
        ]
        ligand_interface_atoms = [
            atom for atom in ligand_chain_protein_atoms if dist(atom, gamma_atom) <= 10.0
        ]
        for acceptor_candidate in acceptor_interface_atoms:
            for ligand_candidate in ligand_interface_atoms:
                if dist(acceptor_candidate, ligand_candidate) <= 4.0:
                    contact_pairs.add(
                        (acceptor_candidate["residue_key"], ligand_candidate["residue_key"])
                    )

    nucleotide_atoms = [
        atom
        for atom in hetero_atoms
        if atom["residue_key"] == gamma_residue_key or atom["resname"] in NUCLEOTIDE_LIKE_CODES
    ]
    nonwater_hetero_atoms = [
        atom
        for atom in hetero_atoms
        if atom["resname"] not in WATER_CODES and atom["residue_key"] != gamma_residue_key
    ]
    nonself_residues_8 = {
        residue for residue in acceptor_residues_8 if residue != acceptor_residue_key
    }
    return {
        "contact_interface_status": "ok",
        "contact_interface_fetch_status": fetch_status,
        "contact_interface_fetch_error": fetch_error,
        "acceptor_chain_residue_count_within_6a_of_gamma": len(acceptor_residues_6),
        "acceptor_chain_residue_count_within_8a_of_gamma": len(acceptor_residues_8),
        "acceptor_chain_nonself_residue_count_within_8a_of_gamma": len(nonself_residues_8),
        "ligand_chain_residue_count_within_8a_of_gamma": len(ligand_residues_8),
        "ligand_chain_acceptor_chain_contact_pair_count_le_4a": len(contact_pairs),
        "nucleotide_heavy_atom_count_within_4a_of_acceptor_atom": sum(
            1 for atom in nucleotide_atoms if dist(atom, acceptor_atom) <= 4.0
        ),
        "nucleotide_heavy_atom_count_within_6a_of_acceptor_atom": sum(
            1 for atom in nucleotide_atoms if dist(atom, acceptor_atom) <= 6.0
        ),
        "nonwater_hetero_heavy_atom_count_within_6a_of_acceptor_atom": sum(
            1 for atom in nonwater_hetero_atoms if dist(atom, acceptor_atom) <= 6.0
        ),
    }


def interface_signature(row: dict[str, Any], contact_features: dict[str, Any], materiality_class: str) -> dict[str, Any]:
    e = evidence(row)
    return {
        "coordinate_state": e.get("coordinate_state"),
        "topology_class": topology_class(e),
        "candidate_role_class": e.get("candidate_role_class") or "state_only",
        "reciprocal_context_class": e.get("reciprocal_context_class") or "none",
        "acceptor_residue_class": residue_class(e),
        "acceptor_terminal_class": terminal_class(e),
        "acceptor_chain_size_class": chain_size_class(e),
        "candidate_chain_nucleotide_context": (
            "candidate_chain_nucleotide_or_metal_present"
            if e.get("candidate_chain_has_own_nucleotide_or_metal")
            or e.get("candidate_chain_active_gamma_count")
            else "candidate_chain_no_nucleotide_or_metal"
        ),
        "contact_materiality_class": materiality_class,
        "acceptor_chain_residue_count_within_6a_class": count_class(
            contact_features["acceptor_chain_residue_count_within_6a_of_gamma"]
        ),
        "cross_chain_contact_pair_count_le_4a_class": count_class(
            contact_features["ligand_chain_acceptor_chain_contact_pair_count_le_4a"]
        ),
    }


def build_contact_row(
    row: dict[str, Any],
    atoms_by_pdb: dict[str, list[dict[str, Any]] | None],
    fetch_status_by_pdb: dict[str, tuple[str, str | None]],
) -> dict[str, Any]:
    pdb_id = row["pdb_id"]
    fetch_status, fetch_error = fetch_status_by_pdb[pdb_id]
    contact_features = contact_features_for_candidate(
        row, atoms_by_pdb[pdb_id], fetch_status, fetch_error
    )
    e = evidence(row)
    materiality_class = contact_materiality_class(e, contact_features)
    signature = interface_signature(row, contact_features, materiality_class)
    blocker_class = contact_blocker_class(e, materiality_class)
    return {
        "candidate_id": row["candidate_id"],
        "diagnostic_row_index": row.get("diagnostic_row_index"),
        "pdb_id": pdb_id,
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
        "row_schema": "epk_active_site_contact_interface_audit_v1",
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
            "candidate_chain_active_gamma_count": e.get("candidate_chain_active_gamma_count"),
            "candidate_chain_has_own_nucleotide_or_metal": e.get(
                "candidate_chain_has_own_nucleotide_or_metal"
            ),
            "terminal_gamma_atom": e.get("terminal_gamma_atom"),
            "acceptor_atom": e.get("acceptor_atom"),
            "contact_interface": contact_features,
            "contact_materiality_class": materiality_class,
            "contact_interface_signature": signature,
            "contact_interface_signature_id": stable_signature_id(signature),
        },
    }


def label_collision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[evidence(row)["contact_interface_signature_id"]].append(row)

    collisions = []
    for signature_id, group in sorted(grouped.items()):
        labels = Counter(review_label(row) for row in group)
        positives = labels.get("positive_true_substrate_acceptor", 0)
        negatives = labels.get("counterexample_not_true_substrate_acceptor", 0)
        if positives and negatives:
            collision_class = "mixed_positive_counterexample_contact_signature"
        elif positives:
            collision_class = "positive_only_contact_signature"
        else:
            collision_class = "counterexample_only_contact_signature"
        collisions.append(
            {
                "contact_interface_signature_id": signature_id,
                "contact_interface_signature": evidence(group[0])["contact_interface_signature"],
                "collision_class": collision_class,
                "label_counts_for_evaluation_only": dict(sorted(labels.items())),
                "candidate_count": len(group),
                "pdb_ids": sorted({row["pdb_id"] for row in group}),
                "hard_case_candidate_ids": sorted(
                    row["candidate_id"] for row in group if row["pdb_id"] in HARD_CASE_PDBS
                ),
            }
        )
    return collisions


def conflict_rows_by_pdb(conflict_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["pdb_id"]: row for row in conflict_payload["candidate_conflict_rows"]}


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


def project_no_promotion_confusion(conflict_payload: dict[str, Any]) -> tuple[dict[str, int], dict[str, list[str]]]:
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


def pdb_contact_digest(rows: list[dict[str, Any]], pdb_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
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
                "contact_materiality_class": evidence(row)["contact_materiality_class"],
                "contact_interface_signature_id": evidence(row)["contact_interface_signature_id"],
                "contact_interface": evidence(row)["contact_interface"],
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

    contact_rows = [
        build_contact_row(row, atoms_by_pdb, fetch_status_by_pdb) for row in input_rows
    ]
    state_only_rows = [
        row
        for row in contact_rows
        if row["row_schema"] == "epk_active_site_contact_interface_audit_v1"
        and evidence(row)["candidate_role_class"] == "state_only"
    ]
    candidate_pair_rows = [
        row for row in contact_rows if evidence(row)["candidate_role_class"] != "state_only"
    ]
    collision_rows = label_collision_rows(contact_rows)
    mixed_collision_rows = [
        row
        for row in collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_contact_signature"
    ]
    hard_digest = pdb_contact_digest(contact_rows, HARD_CASE_PDBS)
    confusion_matrix, pdb_ids_by_outcome = project_no_promotion_confusion(conflict_payload)
    conflict_by_pdb = conflict_rows_by_pdb(conflict_payload)

    coordinate_state_counts = Counter(
        evidence(row)["coordinate_state"] for row in contact_rows
    )
    blocker_class_counts = Counter(evidence(row)["blocker_class"] for row in contact_rows)
    materiality_counts = Counter(
        evidence(row)["contact_materiality_class"] for row in contact_rows
    )
    signature_collision_counts = Counter(row["collision_class"] for row in collision_rows)
    contact_fetch_counts = Counter(status for status, _ in fetch_status_by_pdb.values())

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
            "A source-free active-site contact-interface audit can reveal whether the "
            "candidate acceptor chain materially occupies the nucleotide/gamma site, "
            "while testing whether those interface signatures still collide between "
            "review positives and counterexamples."
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
            "reused_from_conflict_decision_artifact": len(conflict_payload["candidate_conflict_rows"]),
            "coordinate_pdbs_scanned": len(atoms_by_pdb),
        },
        "candidate_evidence_rows_emitted": {
            "contact_interface_rows": len(contact_rows),
            "candidate_pair_rows": len(candidate_pair_rows),
            "state_only_rows": len(state_only_rows),
            "nonterminal_phosphoproduct_state_rows_reemitted": len(input_rows)
            - len(candidate_payload["candidate_evidence_rows"])
            - len(candidate_payload.get("state_only_rows", [])),
            "contact_signature_rows": len(collision_rows),
            "mixed_contact_signature_rows": len(mixed_collision_rows),
        },
        "coordinate_states_observed": dict(sorted(coordinate_state_counts.items())),
        "source_free_features_tested": [
            "acceptor-chain residue materialization within fixed 6A/8A gamma shells",
            "cross-chain ligand-chain/acceptor-chain residue contact pairs within a fixed 4A shell",
            "candidate-chain nucleotide or metal reciprocity context reused as structural evidence",
            "non-terminal phosphoproduct product/ADP/split state rows re-emitted as state-only contact blockers",
            "contact-interface signature collision audit with review labels used only after grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "active_site_contact_interface_no_promotion_v1": {
                "rule_id": "active_site_contact_interface_no_promotion_v1",
                "rule_description": (
                    "Emit contact-interface materialization rows and keep the existing "
                    "source-free conflict abstention policy; contact signatures are not "
                    "promoted to substrate-role identity calls."
                ),
                "new_threshold_or_rescue_rule_added": False,
                "clears_diagnostic_tranche": False,
                "confusion_matrix": confusion_matrix,
                "pdb_ids_by_outcome": pdb_ids_by_outcome,
                "production_claim_allowed": False,
            },
            "contact_signature_collision_audit_v1": {
                "rule_id": "contact_signature_collision_audit_v1",
                "rule_description": (
                    "Group source-free contact-interface signatures before evaluating "
                    "review labels; mixed positive/counterexample signatures block "
                    "source-free promotion."
                ),
                "contact_signature_count": len(collision_rows),
                "mixed_contact_signature_count": len(mixed_collision_rows),
                "collision_class_counts": dict(sorted(signature_collision_counts.items())),
                "hard_case_signature_collision_digest": {
                    pdb_id: conflict_by_pdb[pdb_id]["source_free_decision_class"]
                    for pdb_id in sorted(HARD_CASE_PDBS & set(conflict_by_pdb))
                },
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "9UUR_9UUX_9UW4_contact_collision": (
                "The reciprocal folded Tyr contact-interface class remains shared by "
                "review positives 9UUR/9UUX and counterexample 9UW4."
            ),
            "7B56_internal_fragment_contact": (
                "7B56 still materializes a cross-chain active-site contact but remains "
                "blocked by internal-fragment mimicry, so contact materiality is not "
                "substrate-role identity."
            ),
            "6NOO_3TM0_same_chain_overlap": (
                "Same-chain active-site contact materialization is present in both "
                "review-positive analog/topology context and counterexample pressure rows."
            ),
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": pdb_ids_by_outcome.get("false_positive", []),
            "positive_only_terminal_interface_note": (
                "cross_chain_terminal_or_short_peptide_interface is positive-only in this "
                "tranche because it mirrors the preexisting strict terminal/short-peptide "
                "support class; it is not counted as a new rescue rule and does not address "
                "the hard state/topology abstentions."
            ),
            "interpretation": (
                "No new non-abstaining positive calls were introduced. Contact materiality "
                "collides across positives and counterexamples, so it is review-only blocker evidence."
            ),
        },
        "false_negative_analysis": {
            "abstained_positive_pdb_ids": pdb_ids_by_outcome.get("abstained_positive", []),
            "non_abstaining_false_negative_pdb_ids": pdb_ids_by_outcome.get("false_negative", []),
            "interpretation": (
                "Product/ADP, reciprocal folded-chain, and same-chain analog/topology positives "
                "remain abstained rather than converted to active-gamma false negatives."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
            "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
            "contact_materiality_class_counts": dict(sorted(materiality_counts.items())),
            "contact_signature_collision_class_counts": dict(sorted(signature_collision_counts.items())),
            "interpretation": (
                "Active-site contact materiality is structurally useful but not biological "
                "substrate-role identity; hard topology signatures still collide."
            ),
        },
        "next_query": (
            "Stop contact/interface scalar probing. Only resume this lane for a new "
            "source-free modality that can distinguish reciprocal folded-chain biology "
            "or ADP/analog state without review-context leakage."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep active-site contact-interface rows as compact review-only blocker evidence. "
            "Do not claim ePK production readiness or promote contact materiality into "
            "substrate-role calls."
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
            "candidate_evidence_row_count": len(contact_rows),
            "candidate_pair_row_count": len(candidate_pair_rows),
            "state_only_row_count": len(state_only_rows),
            "diagnostic_pdb_count": len(atoms_by_pdb),
            "raw_coordinate_files_written": False,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "acceptor_chain_residue_count_within_6a_of_gamma": (
                "Unique protein residues on the candidate acceptor chain with any heavy atom "
                "within 6A of the terminal gamma atom."
            ),
            "acceptor_chain_nonself_residue_count_within_8a_of_gamma": (
                "Unique acceptor-chain residues within 8A of gamma, excluding the candidate "
                "acceptor residue itself."
            ),
            "ligand_chain_acceptor_chain_contact_pair_count_le_4a": (
                "Unique cross-chain protein residue pairs, one on the nucleotide/gamma chain "
                "and one on the candidate acceptor chain, with any heavy atoms within 4A."
            ),
            "contact_materiality_class": (
                "Categorical contact-interface route used only for blocker triage and "
                "signature collision checks."
            ),
        },
        "contact_fetch_status_counts": dict(sorted(contact_fetch_counts.items())),
        "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
        "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
        "contact_materiality_class_counts": dict(sorted(materiality_counts.items())),
        "contact_signature_collision_class_counts": dict(sorted(signature_collision_counts.items())),
        "active_site_contact_interface_rows": contact_rows,
        "contact_signature_collision_rows": collision_rows,
        "hard_case_contact_digest": hard_digest,
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
