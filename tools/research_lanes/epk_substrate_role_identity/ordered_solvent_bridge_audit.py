#!/usr/bin/env python3
"""Audit ordered solvent bridges between ePK gamma and acceptor candidates.

This lane-local helper tests one bounded source-free coordinate modality:
whether ordered model-1 water oxygens bridge, solvate, or avoid the candidate
gamma/acceptor pair. It writes compact reduced evidence only and does not
promote solvent features into substrate-role identity calls.
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
    WATER_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_ordered_solvent_bridge_audit_v1_20260521"
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
    "epk_ordered_solvent_bridge_audit_v1_20260521.json"
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

WATER_CONTACT_MAX_ANGSTROM = 3.5


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
        str(compact_atom["atom_name"]),
        str(compact_atom["residue_code"]),
        str(compact_atom["chain_id"]),
        str(compact_atom["auth_seq_id"]),
        compact_atom.get("icode") or "",
    )


def atom_key(atom: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        str(atom["atom_name"]),
        str(atom["resname"]),
        str(atom["chain"]),
        str(atom["resseq"]),
        atom.get("icode") or "",
    )


def find_atom(atoms: list[dict[str, Any]], compact_atom: dict[str, Any] | None) -> dict[str, Any] | None:
    key = compact_key(compact_atom)
    if key is None:
        return None
    for atom in atoms:
        if atom_key(atom) == key:
            return atom
    return None


def compact_atom(atom: dict[str, Any] | None) -> dict[str, Any] | None:
    if atom is None:
        return None
    return {
        "atom_name": atom["atom_name"],
        "residue_code": atom["resname"],
        "chain_id": atom["chain"],
        "auth_seq_id": atom["resseq"],
        "icode": atom["icode"] or None,
        "element": atom["element"],
    }


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def water_oxygen_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        atom
        for atom in atoms
        if atom["record"] == "HETATM"
        and atom["resname"] in WATER_CODES
        and atom["element"] == "O"
    ]


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


def distance_class(value: float | None) -> str:
    if value is None:
        return "distance_unavailable"
    if value <= 4.0:
        return "direct_contact_le_4a"
    if value <= 6.0:
        return "preexisting_transfer_shell_4_to_6a"
    if value <= 8.0:
        return "near_shell_6_to_8a"
    return "distant_gt_8a"


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


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def ordered_solvent_features(
    row: dict[str, Any],
    atoms: list[dict[str, Any]] | None,
    fetch_status: str,
    fetch_error: str | None,
) -> dict[str, Any]:
    e = evidence(row)
    state = e.get("coordinate_state")
    if state != "active_gamma":
        return {
            "ordered_solvent_status": f"not_applicable_{state or 'unknown_state'}",
            "ordered_solvent_fetch_status": fetch_status,
            "ordered_solvent_fetch_error": fetch_error,
            "water_contact_max_angstrom": WATER_CONTACT_MAX_ANGSTROM,
            "water_oxygen_count_model1": None,
            "nearest_water_to_gamma_atom": None,
            "nearest_water_to_gamma_distance_angstrom": None,
            "nearest_water_to_acceptor_atom": None,
            "nearest_water_to_acceptor_distance_angstrom": None,
            "gamma_water_count_within_3p5a": None,
            "acceptor_water_count_within_3p5a": None,
            "gamma_acceptor_bridging_water_count_within_3p5a": None,
            "nearest_bridging_water_atom": None,
            "nearest_bridging_water_gamma_distance_angstrom": None,
            "nearest_bridging_water_acceptor_distance_angstrom": None,
            "nearest_bridging_water_distance_sum_angstrom": None,
            "ordered_solvent_bridge_class": f"not_applicable_{state or 'unknown_state'}",
        }
    if atoms is None:
        return {
            "ordered_solvent_status": "fetch_error",
            "ordered_solvent_fetch_status": fetch_status,
            "ordered_solvent_fetch_error": fetch_error,
            "water_contact_max_angstrom": WATER_CONTACT_MAX_ANGSTROM,
            "water_oxygen_count_model1": None,
            "nearest_water_to_gamma_atom": None,
            "nearest_water_to_gamma_distance_angstrom": None,
            "nearest_water_to_acceptor_atom": None,
            "nearest_water_to_acceptor_distance_angstrom": None,
            "gamma_water_count_within_3p5a": None,
            "acceptor_water_count_within_3p5a": None,
            "gamma_acceptor_bridging_water_count_within_3p5a": None,
            "nearest_bridging_water_atom": None,
            "nearest_bridging_water_gamma_distance_angstrom": None,
            "nearest_bridging_water_acceptor_distance_angstrom": None,
            "nearest_bridging_water_distance_sum_angstrom": None,
            "ordered_solvent_bridge_class": "ordered_solvent_fetch_error",
        }

    gamma_atom = find_atom(atoms, e.get("terminal_gamma_atom"))
    acceptor_atom = find_atom(atoms, e.get("acceptor_atom"))
    waters = water_oxygen_atoms(atoms)
    if gamma_atom is None or acceptor_atom is None:
        return {
            "ordered_solvent_status": "gamma_or_acceptor_atom_not_resolved",
            "ordered_solvent_fetch_status": fetch_status,
            "ordered_solvent_fetch_error": fetch_error,
            "water_contact_max_angstrom": WATER_CONTACT_MAX_ANGSTROM,
            "water_oxygen_count_model1": len(waters),
            "nearest_water_to_gamma_atom": None,
            "nearest_water_to_gamma_distance_angstrom": None,
            "nearest_water_to_acceptor_atom": None,
            "nearest_water_to_acceptor_distance_angstrom": None,
            "gamma_water_count_within_3p5a": None,
            "acceptor_water_count_within_3p5a": None,
            "gamma_acceptor_bridging_water_count_within_3p5a": None,
            "nearest_bridging_water_atom": None,
            "nearest_bridging_water_gamma_distance_angstrom": None,
            "nearest_bridging_water_acceptor_distance_angstrom": None,
            "nearest_bridging_water_distance_sum_angstrom": None,
            "ordered_solvent_bridge_class": "gamma_or_acceptor_atom_not_resolved",
        }

    gamma_distances = [(water, dist(gamma_atom, water)) for water in waters]
    acceptor_distances = [(water, dist(acceptor_atom, water)) for water in waters]
    nearest_gamma = min(gamma_distances, key=lambda item: item[1]) if gamma_distances else (None, None)
    nearest_acceptor = (
        min(acceptor_distances, key=lambda item: item[1]) if acceptor_distances else (None, None)
    )
    bridges = []
    for water in waters:
        gamma_distance = dist(gamma_atom, water)
        acceptor_distance = dist(acceptor_atom, water)
        if gamma_distance <= WATER_CONTACT_MAX_ANGSTROM and acceptor_distance <= WATER_CONTACT_MAX_ANGSTROM:
            bridges.append((water, gamma_distance, acceptor_distance))
    nearest_bridge = min(bridges, key=lambda item: item[1] + item[2]) if bridges else (None, None, None)
    gamma_water_count = sum(1 for _, current in gamma_distances if current <= WATER_CONTACT_MAX_ANGSTROM)
    acceptor_water_count = sum(
        1 for _, current in acceptor_distances if current <= WATER_CONTACT_MAX_ANGSTROM
    )

    if bridges:
        bridge_class = "ordered_water_bridge_between_gamma_and_acceptor"
    elif gamma_water_count and acceptor_water_count:
        bridge_class = "separate_ordered_waters_near_gamma_and_acceptor"
    elif acceptor_water_count:
        bridge_class = "acceptor_solvated_only"
    elif gamma_water_count:
        bridge_class = "gamma_solvated_only"
    else:
        bridge_class = "no_ordered_water_within_3p5a"

    return {
        "ordered_solvent_status": "ok",
        "ordered_solvent_fetch_status": fetch_status,
        "ordered_solvent_fetch_error": fetch_error,
        "water_contact_max_angstrom": WATER_CONTACT_MAX_ANGSTROM,
        "water_oxygen_count_model1": len(waters),
        "nearest_water_to_gamma_atom": compact_atom(nearest_gamma[0]),
        "nearest_water_to_gamma_distance_angstrom": round_or_none(nearest_gamma[1]),
        "nearest_water_to_acceptor_atom": compact_atom(nearest_acceptor[0]),
        "nearest_water_to_acceptor_distance_angstrom": round_or_none(nearest_acceptor[1]),
        "gamma_water_count_within_3p5a": gamma_water_count,
        "acceptor_water_count_within_3p5a": acceptor_water_count,
        "gamma_acceptor_bridging_water_count_within_3p5a": len(bridges),
        "nearest_bridging_water_atom": compact_atom(nearest_bridge[0]),
        "nearest_bridging_water_gamma_distance_angstrom": round_or_none(nearest_bridge[1]),
        "nearest_bridging_water_acceptor_distance_angstrom": round_or_none(nearest_bridge[2]),
        "nearest_bridging_water_distance_sum_angstrom": round_or_none(
            nearest_bridge[1] + nearest_bridge[2]
            if nearest_bridge[1] is not None and nearest_bridge[2] is not None
            else None
        ),
        "ordered_solvent_bridge_class": bridge_class,
    }


def solvent_materiality_class(e: dict[str, Any], features: dict[str, Any]) -> str:
    state = e.get("coordinate_state")
    if state in {"product_state", "adp_state", "split_state", "substrate_acceptor_analog_state"}:
        return f"{state}_ordered_solvent_review_only"
    if state != "active_gamma":
        return f"{state or 'unknown_state'}_no_active_gamma_ordered_solvent_context"
    bridge_class = features["ordered_solvent_bridge_class"]
    if bridge_class == "ordered_water_bridge_between_gamma_and_acceptor":
        return "active_gamma_acceptor_ordered_water_bridge"
    if bridge_class == "separate_ordered_waters_near_gamma_and_acceptor":
        return "active_gamma_acceptor_separately_solvated"
    if bridge_class == "acceptor_solvated_only":
        return "active_gamma_acceptor_solvated_only"
    if bridge_class == "gamma_solvated_only":
        return "active_gamma_gamma_solvated_only"
    if bridge_class == "no_ordered_water_within_3p5a":
        return "active_gamma_no_ordered_water_contact"
    return bridge_class


def solvent_blocker_class(e: dict[str, Any], materiality_class: str) -> str:
    state = e.get("coordinate_state")
    if state in {"product_state", "adp_state"}:
        return "product_state_evidence"
    if state == "substrate_acceptor_analog_state":
        return "substrate_analog_evidence"
    if state == "split_state":
        return "split_state_evidence"
    if state in {"ligand_absent", "unavailable_coordinate_state", "ambiguous_coordinate_state"}:
        return "ligand_materialization"
    if materiality_class in {"ordered_solvent_fetch_error", "gamma_or_acceptor_atom_not_resolved"}:
        return "ligand_materialization"
    return e.get("blocker_class") or "active_gamma_geometry"


def solvent_signature(
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
        "ordered_solvent_bridge_class": features["ordered_solvent_bridge_class"],
        "solvent_materiality_class": materiality_class,
        "gamma_water_count_3p5a_class": count_class(features["gamma_water_count_within_3p5a"]),
        "acceptor_water_count_3p5a_class": count_class(
            features["acceptor_water_count_within_3p5a"]
        ),
        "bridging_water_count_3p5a_class": count_class(
            features["gamma_acceptor_bridging_water_count_within_3p5a"]
        ),
    }


def build_solvent_row(
    row: dict[str, Any],
    atoms_by_pdb: dict[str, list[dict[str, Any]] | None],
    fetch_status_by_pdb: dict[str, tuple[str, str | None]],
) -> dict[str, Any]:
    pdb_id = row["pdb_id"]
    fetch_status, fetch_error = fetch_status_by_pdb[pdb_id]
    e = evidence(row)
    features = ordered_solvent_features(row, atoms_by_pdb[pdb_id], fetch_status, fetch_error)
    materiality_class = solvent_materiality_class(e, features)
    signature = solvent_signature(row, features, materiality_class)
    blocker_class = solvent_blocker_class(e, materiality_class)
    return {
        "candidate_id": row["candidate_id"],
        "diagnostic_row_index": row.get("diagnostic_row_index"),
        "pdb_id": pdb_id,
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
        "row_schema": "epk_ordered_solvent_bridge_audit_v1",
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
            "ordered_solvent_bridge": features,
            "solvent_materiality_class": materiality_class,
            "ordered_solvent_signature": signature,
            "ordered_solvent_signature_id": stable_signature_id(signature),
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
        grouped[evidence(row)["ordered_solvent_signature_id"]].append(row)

    collisions = []
    for signature_id, group in sorted(grouped.items()):
        labels = Counter(review_label(row) for row in group)
        positives = labels.get("positive_true_substrate_acceptor", 0)
        negatives = labels.get("counterexample_not_true_substrate_acceptor", 0)
        if positives and negatives:
            collision_class = "mixed_positive_counterexample_ordered_solvent_signature"
        elif positives:
            collision_class = "positive_only_ordered_solvent_signature"
        else:
            collision_class = "counterexample_only_ordered_solvent_signature"
        collisions.append(
            {
                "ordered_solvent_signature_id": signature_id,
                "ordered_solvent_signature": evidence(group[0])["ordered_solvent_signature"],
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


def pdb_solvent_digest(rows: list[dict[str, Any]], pdb_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
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
                "solvent_materiality_class": evidence(row)["solvent_materiality_class"],
                "ordered_solvent_signature_id": evidence(row)[
                    "ordered_solvent_signature_id"
                ],
                "ordered_solvent_bridge": evidence(row)["ordered_solvent_bridge"],
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

    solvent_rows = [
        build_solvent_row(row, atoms_by_pdb, fetch_status_by_pdb)
        for row in input_rows
    ]
    state_only_rows = [
        row for row in solvent_rows if evidence(row)["candidate_role_class"] == "state_only"
    ]
    candidate_pair_rows = [
        row for row in solvent_rows if evidence(row)["candidate_role_class"] != "state_only"
    ]
    collision_rows = label_collision_rows(solvent_rows)
    mixed_collision_rows = [
        row
        for row in collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_ordered_solvent_signature"
    ]
    hard_digest = pdb_solvent_digest(solvent_rows, HARD_CASE_PDBS)
    confusion_matrix, pdb_ids_by_outcome = project_no_promotion_confusion(conflict_payload)

    coordinate_state_counts = Counter(
        evidence(row)["coordinate_state"] for row in solvent_rows
    )
    blocker_class_counts = Counter(evidence(row)["blocker_class"] for row in solvent_rows)
    materiality_counts = Counter(
        evidence(row)["solvent_materiality_class"] for row in solvent_rows
    )
    bridge_counts = Counter(
        evidence(row)["ordered_solvent_bridge"]["ordered_solvent_bridge_class"]
        for row in solvent_rows
    )
    signature_collision_counts = Counter(row["collision_class"] for row in collision_rows)
    fetch_counts = Counter(status for status, _ in fetch_status_by_pdb.values())
    bridging_rows = [
        row
        for row in solvent_rows
        if evidence(row)["ordered_solvent_bridge"]["ordered_solvent_bridge_class"]
        == "ordered_water_bridge_between_gamma_and_acceptor"
    ]

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
            "A source-free ordered-solvent bridge audit can show whether model-1 water "
            "oxygens bridge or separately solvate active-gamma acceptor pairs, while "
            "testing whether those solvent signatures still collide between review "
            "positives and counterexamples."
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
            "ordered_solvent_bridge_rows": len(solvent_rows),
            "candidate_pair_rows": len(candidate_pair_rows),
            "state_only_rows": len(state_only_rows),
            "nonterminal_phosphoproduct_state_rows_reemitted": len(input_rows)
            - len(candidate_payload["candidate_evidence_rows"])
            - len(candidate_payload.get("state_only_rows", [])),
            "ordered_solvent_signature_rows": len(collision_rows),
            "mixed_ordered_solvent_signature_rows": len(mixed_collision_rows),
            "ordered_water_bridge_candidate_rows": len(bridging_rows),
        },
        "coordinate_states_observed": dict(sorted(coordinate_state_counts.items())),
        "source_free_features_tested": [
            "model-1 ordered water oxygen count near terminal gamma within fixed 3.5A shell",
            "model-1 ordered water oxygen count near acceptor hydroxyl within fixed 3.5A shell",
            "ordered water bridge count simultaneously within fixed 3.5A shells of gamma and acceptor",
            "nearest ordered water distances to gamma, acceptor, and bridged gamma/acceptor pairs",
            "ordered-solvent signature collision audit with review labels used only after grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "ordered_solvent_bridge_no_promotion_v1": {
                "rule_id": "ordered_solvent_bridge_no_promotion_v1",
                "rule_description": (
                    "Emit ordered-solvent bridge rows and keep the existing source-free "
                    "conflict abstention policy; solvent signatures are not promoted to "
                    "substrate-role identity calls."
                ),
                "new_threshold_or_rescue_rule_added": False,
                "clears_diagnostic_tranche": False,
                "confusion_matrix": confusion_matrix,
                "pdb_ids_by_outcome": pdb_ids_by_outcome,
                "production_claim_allowed": False,
            },
            "ordered_solvent_signature_collision_audit_v1": {
                "rule_id": "ordered_solvent_signature_collision_audit_v1",
                "rule_description": (
                    "Group source-free ordered-solvent signatures before evaluating "
                    "review labels; mixed positive/counterexample signatures block "
                    "source-free promotion."
                ),
                "ordered_solvent_signature_count": len(collision_rows),
                "mixed_ordered_solvent_signature_count": len(mixed_collision_rows),
                "ordered_water_bridge_candidate_rows": len(bridging_rows),
                "collision_class_counts": dict(sorted(signature_collision_counts.items())),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "ordered_solvent_collisions": (
                "Ordered-solvent signatures are mixed across review positives and "
                "counterexamples, so water materialization cannot be promoted as "
                "substrate-role identity."
            ),
            "state_specific_no_active_gamma_context": (
                "ADP, product, ligand-absent, ambiguous, and split-state rows remain "
                "state-specific review evidence rather than active-gamma solvent "
                "geometry calls."
            ),
            "topology_cases_remain_biological": (
                "Reciprocal folded-chain and same-chain topology rows can have ordered "
                "solvent context, but topology biology remains source-reviewed."
            ),
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": pdb_ids_by_outcome.get("false_positive", []),
            "interpretation": (
                "No new non-abstaining positive calls were introduced. Ordered solvent "
                "context is emitted as review-only blocker evidence because the "
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
            "solvent_materiality_class_counts": dict(sorted(materiality_counts.items())),
            "ordered_solvent_bridge_class_counts": dict(sorted(bridge_counts.items())),
            "ordered_solvent_signature_collision_class_counts": dict(
                sorted(signature_collision_counts.items())
            ),
            "interpretation": (
                "Ordered solvent bridge evidence reduces review uncertainty around "
                "whether water is materialized between a gamma/acceptor pair, but it "
                "does not adjudicate biological substrate-role identity source-free."
            ),
        },
        "next_query": (
            "Stop ordered-solvent bridge probing as a promotion route. Only resume this "
            "lane for a genuinely different source-free modality that can adjudicate "
            "ADP/product, substrate-analog, reciprocal folded-chain, or same-chain "
            "biology without review-context leakage."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep ordered-solvent bridge rows as compact review-only blocker evidence. "
            "Do not claim ePK production readiness or promote solvent materialization "
            "into substrate-role calls."
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
            "candidate_evidence_row_count": len(solvent_rows),
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
            "ordered_solvent_bridge_class": (
                "Whether model-1 ordered water oxygens are within fixed 3.5A shells of "
                "the terminal gamma atom, acceptor atom, both atoms, or neither."
            ),
            "solvent_materiality_class": (
                "Categorical ordered-solvent route used only for blocker triage and "
                "signature collision checks."
            ),
            "ordered_solvent_signature": (
                "Source-free categorical solvent/context signature grouped before "
                "review labels are inspected for collision analysis."
            ),
        },
        "ordered_solvent_fetch_status_counts": dict(sorted(fetch_counts.items())),
        "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
        "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
        "solvent_materiality_class_counts": dict(sorted(materiality_counts.items())),
        "ordered_solvent_bridge_class_counts": dict(sorted(bridge_counts.items())),
        "ordered_solvent_signature_collision_class_counts": dict(
            sorted(signature_collision_counts.items())
        ),
        "ordered_solvent_bridge_rows": solvent_rows,
        "ordered_solvent_signature_collision_rows": collision_rows,
        "hard_case_ordered_solvent_digest": hard_digest,
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
