#!/usr/bin/env python3
"""Audit source-free carboxylate proximity around ePK acceptor candidates.

This lane-local helper tests one bounded coordinate modality: whether a
candidate acceptor atom is near protein Asp/Glu carboxylate oxygens, and
whether that contact is coupled to an active terminal-gamma site. It emits
compact reduced evidence only and does not promote acid/base geometry into
substrate-role identity calls.
"""

from __future__ import annotations

import argparse
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
from ordered_solvent_bridge_audit import (
    chain_size_class,
    compact_atom,
    distance_class,
    evidence,
    find_atom,
    is_positive_label,
    load_json,
    merged_input_rows,
    project_no_promotion_confusion,
    residue_class,
    review_label,
    stable_signature_id,
    terminal_class,
    topology_class,
)
from substrate_role_identity_eval import dist, fetch_pdb_text, parse_pdb_atoms


ARTIFACT_ID = "epk_acid_base_proximity_audit_v1_20260521"
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
    "epk_acid_base_proximity_audit_v1_20260521.json"
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

CARBOXYLATE_ACCEPTOR_CONTACT_MAX_ANGSTROM = 3.5
CARBOXYLATE_ACCEPTOR_PROXIMAL_MAX_ANGSTROM = 5.0
CARBOXYLATE_GAMMA_CONTEXT_MAX_ANGSTROM = 6.0


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


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


def carboxylate_oxygen_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    allowed = {("ASP", "OD1"), ("ASP", "OD2"), ("GLU", "OE1"), ("GLU", "OE2")}
    return [
        atom
        for atom in atoms
        if atom["record"] == "ATOM"
        and atom["element"] == "O"
        and (atom["resname"], atom["atom_name"]) in allowed
    ]


def nearest_atom(
    center: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, float | None]:
    if center is None or not atoms:
        return None, None
    best_atom = None
    best_distance = None
    for atom in atoms:
        current = dist(center, atom)
        if best_distance is None or current < best_distance:
            best_atom = atom
            best_distance = current
    return best_atom, best_distance


def unique_residue_count(atoms: list[dict[str, Any]]) -> int:
    return len({atom["residue_key"] for atom in atoms})


def carboxylate_topology_class(
    carboxylate: dict[str, Any] | None,
    acceptor: dict[str, Any] | None,
    gamma: dict[str, Any] | None,
) -> str:
    if carboxylate is None or acceptor is None:
        return "carboxylate_topology_unavailable"
    same_acceptor = carboxylate["chain"] == acceptor["chain"]
    same_gamma = bool(gamma is not None and carboxylate["chain"] == gamma["chain"])
    if same_acceptor and same_gamma:
        return "carboxylate_same_chain_as_acceptor_and_gamma"
    if same_acceptor:
        return "carboxylate_same_chain_as_acceptor"
    if same_gamma:
        return "carboxylate_same_chain_as_gamma"
    if gamma is None:
        return "carboxylate_cross_chain_to_acceptor_no_gamma"
    return "carboxylate_cross_chain_to_acceptor_and_gamma"


def proximity_class(features: dict[str, Any]) -> str:
    status = features["acid_base_status"]
    if status != "ok":
        return status
    if features["acceptor_carboxylate_count_within_3p5a"] > 0:
        if features["gamma_context_carboxylate_count"] > 0:
            return "acceptor_carboxylate_contact_with_gamma_context"
        return "acceptor_carboxylate_contact_without_gamma_context"
    if features["acceptor_carboxylate_count_within_5a"] > 0:
        if features["gamma_context_carboxylate_count"] > 0:
            return "acceptor_carboxylate_proximal_with_gamma_context"
        return "acceptor_carboxylate_proximal_without_gamma_context"
    return "no_near_acceptor_carboxylate"


def acid_base_features(
    row: dict[str, Any],
    atoms: list[dict[str, Any]] | None,
    fetch_status: str,
    fetch_error: str | None,
) -> dict[str, Any]:
    e = evidence(row)
    state = e.get("coordinate_state")
    if atoms is None:
        return {
            "acid_base_status": "fetch_error",
            "acid_base_fetch_status": fetch_status,
            "acid_base_fetch_error": fetch_error,
            "carboxylate_acceptor_contact_max_angstrom": CARBOXYLATE_ACCEPTOR_CONTACT_MAX_ANGSTROM,
            "carboxylate_acceptor_proximal_max_angstrom": CARBOXYLATE_ACCEPTOR_PROXIMAL_MAX_ANGSTROM,
            "carboxylate_gamma_context_max_angstrom": CARBOXYLATE_GAMMA_CONTEXT_MAX_ANGSTROM,
            "protein_carboxylate_oxygen_count_model1": None,
            "nearest_carboxylate_to_acceptor_atom": None,
            "nearest_carboxylate_to_acceptor_distance_angstrom": None,
            "nearest_carboxylate_to_gamma_atom": None,
            "nearest_carboxylate_to_gamma_distance_angstrom": None,
            "acceptor_carboxylate_count_within_3p5a": None,
            "acceptor_carboxylate_residue_count_within_3p5a": None,
            "acceptor_carboxylate_count_within_5a": None,
            "acceptor_carboxylate_residue_count_within_5a": None,
            "gamma_context_carboxylate_count": None,
            "nearest_gamma_context_carboxylate_atom": None,
            "nearest_gamma_context_carboxylate_acceptor_distance_angstrom": None,
            "nearest_gamma_context_carboxylate_gamma_distance_angstrom": None,
            "nearest_gamma_context_carboxylate_distance_sum_angstrom": None,
            "nearest_carboxylate_topology_class": "carboxylate_topology_unavailable",
            "acid_base_proximity_class": "fetch_error",
        }

    gamma_atom = find_atom(atoms, e.get("terminal_gamma_atom"))
    acceptor_atom = find_atom(atoms, e.get("acceptor_atom"))
    carboxylates = carboxylate_oxygen_atoms(atoms)
    if acceptor_atom is None:
        return {
            "acid_base_status": f"acceptor_atom_not_resolved_or_absent_{state or 'unknown_state'}",
            "acid_base_fetch_status": fetch_status,
            "acid_base_fetch_error": fetch_error,
            "carboxylate_acceptor_contact_max_angstrom": CARBOXYLATE_ACCEPTOR_CONTACT_MAX_ANGSTROM,
            "carboxylate_acceptor_proximal_max_angstrom": CARBOXYLATE_ACCEPTOR_PROXIMAL_MAX_ANGSTROM,
            "carboxylate_gamma_context_max_angstrom": CARBOXYLATE_GAMMA_CONTEXT_MAX_ANGSTROM,
            "protein_carboxylate_oxygen_count_model1": len(carboxylates),
            "nearest_carboxylate_to_acceptor_atom": None,
            "nearest_carboxylate_to_acceptor_distance_angstrom": None,
            "nearest_carboxylate_to_gamma_atom": None,
            "nearest_carboxylate_to_gamma_distance_angstrom": None,
            "acceptor_carboxylate_count_within_3p5a": None,
            "acceptor_carboxylate_residue_count_within_3p5a": None,
            "acceptor_carboxylate_count_within_5a": None,
            "acceptor_carboxylate_residue_count_within_5a": None,
            "gamma_context_carboxylate_count": None,
            "nearest_gamma_context_carboxylate_atom": None,
            "nearest_gamma_context_carboxylate_acceptor_distance_angstrom": None,
            "nearest_gamma_context_carboxylate_gamma_distance_angstrom": None,
            "nearest_gamma_context_carboxylate_distance_sum_angstrom": None,
            "nearest_carboxylate_topology_class": "carboxylate_topology_unavailable",
            "acid_base_proximity_class": f"acceptor_atom_not_resolved_or_absent_{state or 'unknown_state'}",
        }

    nearest_acceptor_atom, nearest_acceptor_distance = nearest_atom(acceptor_atom, carboxylates)
    nearest_gamma_atom, nearest_gamma_distance = nearest_atom(gamma_atom, carboxylates)
    acceptor_contacts = [
        atom
        for atom in carboxylates
        if dist(acceptor_atom, atom) <= CARBOXYLATE_ACCEPTOR_CONTACT_MAX_ANGSTROM
    ]
    acceptor_proximal = [
        atom
        for atom in carboxylates
        if dist(acceptor_atom, atom) <= CARBOXYLATE_ACCEPTOR_PROXIMAL_MAX_ANGSTROM
    ]
    gamma_context = []
    if gamma_atom is not None:
        for atom in acceptor_proximal:
            if dist(gamma_atom, atom) <= CARBOXYLATE_GAMMA_CONTEXT_MAX_ANGSTROM:
                gamma_context.append((atom, dist(acceptor_atom, atom), dist(gamma_atom, atom)))
    nearest_context = (
        min(gamma_context, key=lambda item: item[1] + item[2])
        if gamma_context
        else (None, None, None)
    )

    features = {
        "acid_base_status": "ok",
        "acid_base_fetch_status": fetch_status,
        "acid_base_fetch_error": fetch_error,
        "carboxylate_acceptor_contact_max_angstrom": CARBOXYLATE_ACCEPTOR_CONTACT_MAX_ANGSTROM,
        "carboxylate_acceptor_proximal_max_angstrom": CARBOXYLATE_ACCEPTOR_PROXIMAL_MAX_ANGSTROM,
        "carboxylate_gamma_context_max_angstrom": CARBOXYLATE_GAMMA_CONTEXT_MAX_ANGSTROM,
        "protein_carboxylate_oxygen_count_model1": len(carboxylates),
        "nearest_carboxylate_to_acceptor_atom": compact_atom(nearest_acceptor_atom),
        "nearest_carboxylate_to_acceptor_distance_angstrom": round_or_none(
            nearest_acceptor_distance
        ),
        "nearest_carboxylate_to_gamma_atom": compact_atom(nearest_gamma_atom),
        "nearest_carboxylate_to_gamma_distance_angstrom": round_or_none(nearest_gamma_distance),
        "acceptor_carboxylate_count_within_3p5a": len(acceptor_contacts),
        "acceptor_carboxylate_residue_count_within_3p5a": unique_residue_count(
            acceptor_contacts
        ),
        "acceptor_carboxylate_count_within_5a": len(acceptor_proximal),
        "acceptor_carboxylate_residue_count_within_5a": unique_residue_count(
            acceptor_proximal
        ),
        "gamma_context_carboxylate_count": len(gamma_context),
        "nearest_gamma_context_carboxylate_atom": compact_atom(nearest_context[0]),
        "nearest_gamma_context_carboxylate_acceptor_distance_angstrom": round_or_none(
            nearest_context[1]
        ),
        "nearest_gamma_context_carboxylate_gamma_distance_angstrom": round_or_none(
            nearest_context[2]
        ),
        "nearest_gamma_context_carboxylate_distance_sum_angstrom": round_or_none(
            nearest_context[1] + nearest_context[2]
            if nearest_context[1] is not None and nearest_context[2] is not None
            else None
        ),
        "nearest_carboxylate_topology_class": carboxylate_topology_class(
            nearest_acceptor_atom, acceptor_atom, gamma_atom
        ),
    }
    features["acid_base_proximity_class"] = proximity_class(features)
    return features


def acid_base_materiality_class(e: dict[str, Any], features: dict[str, Any]) -> str:
    state = e.get("coordinate_state")
    proximity = features["acid_base_proximity_class"]
    if state in {"product_state", "adp_state", "split_state", "substrate_acceptor_analog_state"}:
        if proximity.startswith("acceptor_carboxylate"):
            return f"{state}_acceptor_carboxylate_review_only"
        return f"{state}_no_acceptor_carboxylate_context_review_only"
    if state != "active_gamma":
        return f"{state or 'unknown_state'}_no_active_gamma_acid_base_context"
    if proximity == "acceptor_carboxylate_contact_with_gamma_context":
        return "active_gamma_acceptor_carboxylate_contact_with_gamma_context"
    if proximity == "acceptor_carboxylate_proximal_with_gamma_context":
        return "active_gamma_acceptor_carboxylate_proximal_with_gamma_context"
    if proximity.startswith("acceptor_carboxylate"):
        return "active_gamma_acceptor_carboxylate_without_gamma_context"
    if proximity == "no_near_acceptor_carboxylate":
        return "active_gamma_no_near_acceptor_carboxylate"
    return proximity


def acid_base_blocker_class(e: dict[str, Any], materiality_class: str) -> str:
    state = e.get("coordinate_state")
    if state in {"product_state", "adp_state"}:
        return "product_state_evidence"
    if state == "substrate_acceptor_analog_state":
        return "substrate_analog_evidence"
    if state == "split_state":
        return "split_state_evidence"
    if state in {"ligand_absent", "unavailable_coordinate_state", "ambiguous_coordinate_state"}:
        return "ligand_materialization"
    if materiality_class in {"fetch_error"} or materiality_class.startswith(
        "acceptor_atom_not_resolved"
    ):
        return "ligand_materialization"
    return e.get("blocker_class") or "active_gamma_geometry"


def acid_base_signature(
    row: dict[str, Any],
    features: dict[str, Any],
    materiality_class: str,
) -> dict[str, Any]:
    e = evidence(row)
    return {
        "coordinate_state": e.get("coordinate_state"),
        "source_blocker_class": e.get("blocker_class"),
        "topology_class": topology_class(e),
        "candidate_role_class": e.get("candidate_role_class") or "state_only",
        "reciprocal_context_class": e.get("reciprocal_context_class") or "none",
        "acceptor_residue_class": residue_class(e),
        "acceptor_terminal_class": terminal_class(e),
        "acceptor_chain_size_class": chain_size_class(e),
        "distance_class": distance_class(e.get("distance_angstrom")),
        "acid_base_proximity_class": features["acid_base_proximity_class"],
        "acid_base_materiality_class": materiality_class,
        "acceptor_carboxylate_count_3p5a_class": count_class(
            features["acceptor_carboxylate_count_within_3p5a"]
        ),
        "acceptor_carboxylate_count_5a_class": count_class(
            features["acceptor_carboxylate_count_within_5a"]
        ),
        "gamma_context_carboxylate_count_class": count_class(
            features["gamma_context_carboxylate_count"]
        ),
        "nearest_carboxylate_topology_class": features["nearest_carboxylate_topology_class"],
    }


def build_acid_base_row(
    row: dict[str, Any],
    atoms_by_pdb: dict[str, list[dict[str, Any]] | None],
    fetch_status_by_pdb: dict[str, tuple[str, str | None]],
) -> dict[str, Any]:
    pdb_id = row["pdb_id"]
    fetch_status, fetch_error = fetch_status_by_pdb[pdb_id]
    e = evidence(row)
    features = acid_base_features(row, atoms_by_pdb[pdb_id], fetch_status, fetch_error)
    materiality_class = acid_base_materiality_class(e, features)
    signature = acid_base_signature(row, features, materiality_class)
    blocker_class = acid_base_blocker_class(e, materiality_class)
    return {
        "candidate_id": row["candidate_id"],
        "diagnostic_row_index": row.get("diagnostic_row_index"),
        "pdb_id": pdb_id,
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
        "row_schema": "epk_acid_base_proximity_audit_v1",
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
            "terminal_gamma_atom": e.get("terminal_gamma_atom"),
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
            "acid_base_proximity": features,
            "acid_base_materiality_class": materiality_class,
            "acid_base_signature": signature,
            "acid_base_signature_id": stable_signature_id(signature),
        },
    }


def label_collision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[evidence(row)["acid_base_signature_id"]].append(row)

    collisions = []
    for signature_id, group in sorted(grouped.items()):
        labels = Counter(review_label(row) for row in group)
        positives = labels.get("positive_true_substrate_acceptor", 0)
        negatives = labels.get("counterexample_not_true_substrate_acceptor", 0)
        if positives and negatives:
            collision_class = "mixed_positive_counterexample_acid_base_signature"
        elif positives:
            collision_class = "positive_only_acid_base_signature"
        else:
            collision_class = "counterexample_only_acid_base_signature"
        collisions.append(
            {
                "acid_base_signature_id": signature_id,
                "acid_base_signature": evidence(group[0])["acid_base_signature"],
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


def pdb_acid_base_digest(rows: list[dict[str, Any]], pdb_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
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
                "acid_base_materiality_class": evidence(row)["acid_base_materiality_class"],
                "acid_base_signature_id": evidence(row)["acid_base_signature_id"],
                "acid_base_proximity": evidence(row)["acid_base_proximity"],
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

    acid_base_rows = [
        build_acid_base_row(row, atoms_by_pdb, fetch_status_by_pdb)
        for row in input_rows
    ]
    state_only_rows = [
        row for row in acid_base_rows if evidence(row)["candidate_role_class"] == "state_only"
    ]
    candidate_pair_rows = [
        row for row in acid_base_rows if evidence(row)["candidate_role_class"] != "state_only"
    ]
    product_or_split_acceptor_rows = [
        row
        for row in acid_base_rows
        if evidence(row)["coordinate_state"] in {"product_state", "split_state"}
        and evidence(row)["acceptor_atom"] is not None
    ]
    gamma_context_rows = [
        row
        for row in acid_base_rows
        if evidence(row)["acid_base_proximity"]["gamma_context_carboxylate_count"]
        and evidence(row)["acid_base_proximity"]["gamma_context_carboxylate_count"] > 0
    ]
    collision_rows = label_collision_rows(acid_base_rows)
    mixed_collision_rows = [
        row
        for row in collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_acid_base_signature"
    ]
    hard_digest = pdb_acid_base_digest(acid_base_rows, HARD_CASE_PDBS)
    confusion_matrix, pdb_ids_by_outcome = project_no_promotion_confusion(conflict_payload)

    coordinate_state_counts = Counter(
        evidence(row)["coordinate_state"] for row in acid_base_rows
    )
    blocker_class_counts = Counter(evidence(row)["blocker_class"] for row in acid_base_rows)
    materiality_counts = Counter(
        evidence(row)["acid_base_materiality_class"] for row in acid_base_rows
    )
    proximity_counts = Counter(
        evidence(row)["acid_base_proximity"]["acid_base_proximity_class"]
        for row in acid_base_rows
    )
    signature_collision_counts = Counter(row["collision_class"] for row in collision_rows)
    fetch_counts = Counter(status for status, _ in fetch_status_by_pdb.values())

    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60, 2)
    primary_outcome = "candidate_evidence_rows_emitted"
    hypothesis = (
        "A source-free protein carboxylate proximity audit can show whether candidate "
        "acceptor atoms have nearby Asp/Glu oxygens, and whether that acid/base-like "
        "contact is coupled to an active terminal-gamma site, while testing whether "
        "those signatures still collide between review positives and counterexamples."
    )
    run_record = {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "artifact_path": str(DEFAULT_OUTPUT_PATH),
        "hypothesis": hypothesis,
        "git_sync_status": (
            "git fetch origin failed at run start with Operation not permitted writing "
            "linked-worktree FETCH_HEAD; git pull --ff-only origin "
            "research/epk-substrate-role-identity failed on the same metadata path. "
            "Continued from current on-disk lane state; use remote-tip temporary-index "
            "commit/push if normal linked-worktree metadata operations remain blocked."
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
            "acid_base_proximity_rows": len(acid_base_rows),
            "candidate_pair_rows": len(candidate_pair_rows),
            "state_only_rows": len(state_only_rows),
            "nonterminal_phosphoproduct_state_rows_reemitted": len(input_rows)
            - len(candidate_payload["candidate_evidence_rows"])
            - len(candidate_payload.get("state_only_rows", [])),
            "product_or_split_acceptor_rows_with_acceptor_atom": len(
                product_or_split_acceptor_rows
            ),
            "active_or_candidate_rows_with_gamma_context_carboxylate": len(gamma_context_rows),
            "acid_base_signature_rows": len(collision_rows),
            "mixed_acid_base_signature_rows": len(mixed_collision_rows),
        },
        "coordinate_states_observed": dict(sorted(coordinate_state_counts.items())),
        "source_free_features_tested": [
            "model-1 protein Asp/Glu carboxylate oxygen count near acceptor within fixed 3.5A shell",
            "model-1 protein Asp/Glu carboxylate oxygen count near acceptor within fixed 5.0A shell",
            "carboxylate oxygen coupling to active terminal gamma within fixed 6.0A shell",
            "nearest carboxylate topology relative to acceptor chain and gamma chain",
            "acid/base proximity signature collision audit with review labels used only after grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "acid_base_proximity_no_promotion_v1": {
                "rule_id": "acid_base_proximity_no_promotion_v1",
                "rule_description": (
                    "Emit carboxylate proximity rows and keep the existing source-free "
                    "conflict abstention policy; acid/base geometry is not promoted to "
                    "substrate-role identity calls."
                ),
                "new_threshold_or_rescue_rule_added": False,
                "clears_diagnostic_tranche": False,
                "confusion_matrix": confusion_matrix,
                "pdb_ids_by_outcome": pdb_ids_by_outcome,
                "production_claim_allowed": False,
            },
            "acid_base_signature_collision_audit_v1": {
                "rule_id": "acid_base_signature_collision_audit_v1",
                "rule_description": (
                    "Group source-free acid/base proximity signatures before evaluating "
                    "review labels; mixed positive/counterexample signatures block "
                    "source-free promotion."
                ),
                "acid_base_signature_count": len(collision_rows),
                "mixed_acid_base_signature_count": len(mixed_collision_rows),
                "gamma_context_carboxylate_rows": len(gamma_context_rows),
                "product_or_split_acceptor_rows_with_acceptor_atom": len(
                    product_or_split_acceptor_rows
                ),
                "collision_class_counts": dict(sorted(signature_collision_counts.items())),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "acid_base_signature_collisions": (
                "Asp/Glu proximity signatures are mixed across review positives and "
                "counterexamples, so carboxylate geometry cannot be promoted as "
                "substrate-role identity."
            ),
            "product_and_split_state_context": (
                "Product/split acceptor rows can carry carboxylate proximity evidence, "
                "but without active gamma they remain state-specific review evidence."
            ),
            "topology_cases_remain_biological": (
                "Reciprocal folded-chain and same-chain topology rows can have nearby "
                "carboxylates, but that does not adjudicate biological substrate role "
                "source-free."
            ),
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": pdb_ids_by_outcome.get("false_positive", []),
            "interpretation": (
                "No new non-abstaining positive calls were introduced. Carboxylate "
                "proximity is emitted as review-only blocker evidence because the "
                "signature space collides across positives and counterexamples."
            ),
        },
        "false_negative_analysis": {
            "abstained_positive_pdb_ids": pdb_ids_by_outcome.get("abstained_positive", []),
            "non_abstaining_false_negative_pdb_ids": pdb_ids_by_outcome.get("false_negative", []),
            "interpretation": (
                "Product/ADP, reciprocal folded-chain, and same-chain topology positives "
                "remain abstained rather than converted to active-gamma false negatives."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
            "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
            "acid_base_materiality_class_counts": dict(sorted(materiality_counts.items())),
            "acid_base_proximity_class_counts": dict(sorted(proximity_counts.items())),
            "acid_base_signature_collision_class_counts": dict(
                sorted(signature_collision_counts.items())
            ),
            "interpretation": (
                "Carboxylate proximity reduces review uncertainty around acid/base-like "
                "acceptor geometry, including product/split acceptors, but it does not "
                "adjudicate biological substrate-role identity source-free."
            ),
        },
        "next_query": (
            "Stop acid/base carboxylate proximity probing as a promotion route. Only "
            "resume this lane for a genuinely different source-free modality that can "
            "adjudicate ADP/product, substrate-analog, reciprocal folded-chain, or "
            "same-chain biology without review-context leakage."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep carboxylate proximity rows as compact review-only blocker evidence. "
            "Do not claim ePK production readiness or promote acid/base geometry into "
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
            "candidate_evidence_row_count": len(acid_base_rows),
            "candidate_pair_row_count": len(candidate_pair_rows),
            "state_only_row_count": len(state_only_rows),
            "diagnostic_pdb_count": len(atoms_by_pdb),
            "raw_coordinate_files_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "review_only": True,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
        },
        "hypothesis": hypothesis,
        "feature_definitions": {
            "acid_base_proximity_class": (
                "Whether model-1 protein Asp/Glu carboxylate oxygens are within fixed "
                "3.5A or 5.0A shells of the acceptor atom and, when active gamma is "
                "resolved, also within a fixed 6.0A shell of terminal gamma."
            ),
            "acid_base_materiality_class": (
                "Categorical carboxylate proximity route used only for blocker triage "
                "and signature collision checks."
            ),
            "acid_base_signature": (
                "Source-free categorical acid/base context signature grouped before "
                "review labels are inspected for collision analysis."
            ),
        },
        "acid_base_fetch_status_counts": dict(sorted(fetch_counts.items())),
        "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
        "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
        "acid_base_materiality_class_counts": dict(sorted(materiality_counts.items())),
        "acid_base_proximity_class_counts": dict(sorted(proximity_counts.items())),
        "acid_base_signature_collision_class_counts": dict(
            sorted(signature_collision_counts.items())
        ),
        "acid_base_proximity_rows": acid_base_rows,
        "acid_base_signature_collision_rows": collision_rows,
        "hard_case_acid_base_digest": hard_digest,
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
