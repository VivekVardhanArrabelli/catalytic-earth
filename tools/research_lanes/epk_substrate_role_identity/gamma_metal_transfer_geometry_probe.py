#!/usr/bin/env python3
"""Compact source-free gamma metal/transfer-geometry probe for ePK candidates.

This lane-local helper overlays candidate evidence rows with metal cofactor
materialization and reduced phosphate geometry. It fetches coordinates in
memory only and writes compact rows, not raw coordinate dumps.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)
from substrate_role_identity_eval import METAL_CODES, dist, fetch_pdb_text, parse_pdb_atoms


ARTIFACT_ID = "epk_gamma_metal_transfer_geometry_probe_v1_20260521"
PRIMARY_OUTCOMES = {
    "candidate_evidence_rows_emitted",
    "blocker_cleared_source_free",
    "blocker_not_cleared_data_scarcity",
    "blocker_not_cleared_method_weakness",
    "blocker_not_cleared_biology_ambiguity",
    "counterexample_found",
    "next_query_defined",
}
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_gamma_metal_transfer_geometry_probe_v1_20260521.json"
)

BRIDGE_ATOM_NAMES = ("N3B", "O3B")
GAMMA_NEIGHBOR_ELEMENTS = {"O", "N"}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def compact_key(compact_atom: dict[str, Any] | None) -> tuple[str, str, str, str, str] | None:
    if not compact_atom:
        return None
    return (
        str(compact_atom["atom_name"]).upper(),
        str(compact_atom["residue_code"]).upper(),
        str(compact_atom["chain_id"]),
        str(compact_atom["auth_seq_id"]),
        str(compact_atom.get("icode") or ""),
    )


def atom_key(atom: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        atom["atom_name"],
        atom["resname"],
        atom["chain"],
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
    if not atom:
        return None
    return {
        "atom_name": atom["atom_name"],
        "residue_code": atom["resname"],
        "chain_id": atom["chain"],
        "auth_seq_id": atom["resseq"],
        "icode": atom["icode"] or None,
        "element": atom["element"],
    }


def vector(a: dict[str, Any], b: dict[str, Any]) -> tuple[float, float, float]:
    return (b["x"] - a["x"], b["y"] - a["y"], b["z"] - a["z"])


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a: tuple[float, float, float]) -> float:
    return math.sqrt(dot(a, a))


def angle_degrees(a: dict[str, Any], b: dict[str, Any], c: dict[str, Any]) -> float | None:
    first = vector(b, a)
    second = vector(b, c)
    first_len = norm(first)
    second_len = norm(second)
    if first_len == 0 or second_len == 0:
        return None
    cosine = max(-1.0, min(1.0, dot(first, second) / (first_len * second_len)))
    return round(math.degrees(math.acos(cosine)), 3)


def source_payload() -> dict[str, Any]:
    return json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))


class PdbAtomCache:
    def __init__(self) -> None:
        self._cache: dict[str, tuple[list[dict[str, Any]] | None, str | None]] = {}

    def atoms_for_pdb(self, pdb_id: str) -> tuple[list[dict[str, Any]] | None, str | None]:
        if pdb_id in self._cache:
            return self._cache[pdb_id]
        last_error = None
        for attempt in range(1, 4):
            text, error = fetch_pdb_text(pdb_id)
            if text is not None:
                atoms = parse_pdb_atoms(text)
                self._cache[pdb_id] = (atoms, None)
                time.sleep(0.05)
                return atoms, None
            last_error = error
            if attempt < 3:
                time.sleep(float(attempt))
        self._cache[pdb_id] = (None, last_error)
        return None, last_error


def same_residue_atoms(atoms: list[dict[str, Any]], atom: dict[str, Any] | None) -> list[dict[str, Any]]:
    if atom is None:
        return []
    return [candidate for candidate in atoms if candidate["residue_key"] == atom["residue_key"]]


def gamma_neighbor_atoms(gamma_atom: dict[str, Any] | None, atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if gamma_atom is None:
        return []
    neighbors = []
    for atom in same_residue_atoms(atoms, gamma_atom):
        if atom is gamma_atom:
            continue
        if atom["element"] not in GAMMA_NEIGHBOR_ELEMENTS:
            continue
        if dist(gamma_atom, atom) <= 2.2:
            neighbors.append(atom)
    return sorted(neighbors, key=lambda atom: (atom["atom_name"], atom["resname"], atom["chain"], atom["resseq"]))


def bridge_atom(gamma_atom: dict[str, Any] | None, atoms: list[dict[str, Any]]) -> dict[str, Any] | None:
    if gamma_atom is None:
        return None
    same = same_residue_atoms(atoms, gamma_atom)
    by_name = {atom["atom_name"]: atom for atom in same}
    for name in BRIDGE_ATOM_NAMES:
        if name in by_name:
            return by_name[name]
    beta = by_name.get("PB")
    if beta is None:
        return None
    candidates = [
        atom
        for atom in same
        if atom["element"] in GAMMA_NEIGHBOR_ELEMENTS
        and atom["atom_name"] != gamma_atom["atom_name"]
        and dist(gamma_atom, atom) <= 2.2
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda atom: dist(atom, beta) + dist(atom, gamma_atom))


def angle_class(angle: float | None) -> str:
    if angle is None:
        return "unavailable"
    if angle >= 150.0:
        return "inline_like_ge_150"
    if angle >= 120.0:
        return "partial_inline_120_to_150"
    if angle >= 80.0:
        return "oblique_80_to_120"
    return "not_inline_lt_80"


def metal_shell_class(nearest_distance: float | None, metal_count: int) -> str:
    if metal_count == 0:
        return "no_metal_atoms_model1"
    if nearest_distance is None:
        return "no_metal_within_8a"
    if nearest_distance <= 4.0:
        return "direct_metal_shell_le_4a"
    if nearest_distance <= 8.0:
        return "loose_metal_shell_4_to_8a"
    return "no_metal_within_8a"


def metal_features(
    gamma_atom: dict[str, Any] | None,
    acceptor_atom: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    metals = [
        atom
        for atom in atoms
        if atom["record"] == "HETATM" and atom["resname"] in METAL_CODES
    ]
    metal_codes = sorted({atom["resname"] for atom in metals})
    gamma_distances = [(atom, dist(gamma_atom, atom)) for atom in metals] if gamma_atom else []
    acceptor_distances = [(atom, dist(acceptor_atom, atom)) for atom in metals] if acceptor_atom else []
    nearest_gamma = min(gamma_distances, key=lambda item: item[1]) if gamma_distances else (None, None)
    nearest_acceptor = (
        min(acceptor_distances, key=lambda item: item[1]) if acceptor_distances else (None, None)
    )
    shared = []
    if gamma_atom and acceptor_atom:
        for metal in metals:
            gamma_distance = dist(gamma_atom, metal)
            acceptor_distance = dist(acceptor_atom, metal)
            if gamma_distance <= 8.0 and acceptor_distance <= 8.0:
                shared.append((metal, gamma_distance, acceptor_distance))
    nearest_shared = (
        min(shared, key=lambda item: item[1] + item[2]) if shared else (None, None, None)
    )
    nearest_gamma_distance = round_or_none(nearest_gamma[1])
    return {
        "metal_atom_count_model1": len(metals),
        "metal_codes_observed": metal_codes,
        "nearest_metal_to_gamma_atom": compact_atom(nearest_gamma[0]),
        "nearest_metal_to_gamma_distance_angstrom": nearest_gamma_distance,
        "nearest_metal_to_acceptor_atom": compact_atom(nearest_acceptor[0]),
        "nearest_metal_to_acceptor_distance_angstrom": round_or_none(nearest_acceptor[1]),
        "metal_count_within_4a_of_gamma": sum(1 for _, current in gamma_distances if current <= 4.0),
        "metal_count_within_8a_of_gamma": sum(1 for _, current in gamma_distances if current <= 8.0),
        "shared_gamma_acceptor_metal_count_within_8a": len(shared),
        "nearest_shared_gamma_acceptor_metal_atom": compact_atom(nearest_shared[0]),
        "nearest_shared_metal_gamma_distance_angstrom": round_or_none(nearest_shared[1]),
        "nearest_shared_metal_acceptor_distance_angstrom": round_or_none(nearest_shared[2]),
        "gamma_metal_shell_class": metal_shell_class(nearest_gamma_distance, len(metals)),
    }


def phosphate_transfer_geometry(
    gamma_atom: dict[str, Any] | None,
    acceptor_atom: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    if gamma_atom is None or acceptor_atom is None:
        return {
            "transfer_geometry_status": "gamma_or_acceptor_atom_not_resolved",
            "acceptor_gamma_distance_angstrom": None,
            "bridge_atom": None,
            "acceptor_gamma_bridge_angle_degrees": None,
            "acceptor_gamma_bridge_angle_class": "unavailable",
            "max_acceptor_gamma_neighbor_angle_degrees": None,
            "max_acceptor_gamma_neighbor_angle_atom": None,
            "max_acceptor_gamma_neighbor_angle_class": "unavailable",
            "gamma_neighbor_angle_count": 0,
        }
    bridge = bridge_atom(gamma_atom, atoms)
    bridge_angle = angle_degrees(acceptor_atom, gamma_atom, bridge) if bridge else None
    neighbor_angles = []
    for neighbor in gamma_neighbor_atoms(gamma_atom, atoms):
        angle = angle_degrees(acceptor_atom, gamma_atom, neighbor)
        if angle is not None:
            neighbor_angles.append((neighbor, angle))
    max_neighbor = max(neighbor_angles, key=lambda item: item[1]) if neighbor_angles else (None, None)
    return {
        "transfer_geometry_status": "ok",
        "acceptor_gamma_distance_angstrom": round_or_none(dist(acceptor_atom, gamma_atom)),
        "bridge_atom": compact_atom(bridge),
        "acceptor_gamma_bridge_angle_degrees": bridge_angle,
        "acceptor_gamma_bridge_angle_class": angle_class(bridge_angle),
        "max_acceptor_gamma_neighbor_angle_degrees": max_neighbor[1],
        "max_acceptor_gamma_neighbor_angle_atom": compact_atom(max_neighbor[0]),
        "max_acceptor_gamma_neighbor_angle_class": angle_class(max_neighbor[1]),
        "gamma_neighbor_angle_count": len(neighbor_angles),
    }


def metal_adjusted_coordinate_state(
    source_state: str,
    fetch_status: str,
    gamma_atom_resolved: bool,
    gamma_metal_shell_class: str,
) -> str:
    if source_state != "active_gamma":
        return source_state
    if fetch_status != "ok" or not gamma_atom_resolved:
        return "unavailable_coordinate_state"
    if gamma_metal_shell_class in {"direct_metal_shell_le_4a", "loose_metal_shell_4_to_8a"}:
        return "active_gamma"
    return "metal_absent"


def adjusted_blocker_class(source_blocker: str, coordinate_state: str) -> str:
    if coordinate_state == "metal_absent":
        return "active_gamma_geometry"
    if coordinate_state in {"unavailable_coordinate_state", "ambiguous_coordinate_state", "ligand_absent"}:
        return "ligand_materialization"
    return source_blocker


def candidate_transfer_row(row: dict[str, Any], cache: PdbAtomCache) -> dict[str, Any]:
    evidence = row["source_free_evidence"]
    atoms, fetch_error = cache.atoms_for_pdb(row["pdb_id"])
    if atoms is None:
        metal = {
            "metal_atom_count_model1": None,
            "metal_codes_observed": [],
            "nearest_metal_to_gamma_atom": None,
            "nearest_metal_to_gamma_distance_angstrom": None,
            "nearest_metal_to_acceptor_atom": None,
            "nearest_metal_to_acceptor_distance_angstrom": None,
            "metal_count_within_4a_of_gamma": None,
            "metal_count_within_8a_of_gamma": None,
            "shared_gamma_acceptor_metal_count_within_8a": None,
            "nearest_shared_gamma_acceptor_metal_atom": None,
            "nearest_shared_metal_gamma_distance_angstrom": None,
            "nearest_shared_metal_acceptor_distance_angstrom": None,
            "gamma_metal_shell_class": "unavailable_fetch_error",
        }
        transfer = phosphate_transfer_geometry(None, None, [])
        adjusted_state = "unavailable_coordinate_state"
    else:
        gamma_atom = find_atom(atoms, evidence.get("terminal_gamma_atom"))
        acceptor_atom = find_atom(atoms, evidence.get("acceptor_atom"))
        metal = metal_features(gamma_atom, acceptor_atom, atoms)
        transfer = phosphate_transfer_geometry(gamma_atom, acceptor_atom, atoms)
        adjusted_state = metal_adjusted_coordinate_state(
            evidence["coordinate_state"],
            "ok",
            gamma_atom is not None,
            metal["gamma_metal_shell_class"],
        )
    blocker = adjusted_blocker_class(evidence["blocker_class"], adjusted_state)
    return {
        "row_schema": "epk_gamma_metal_transfer_geometry_candidate_v1",
        "candidate_id": row["candidate_id"],
        "pdb_id": row["pdb_id"],
        "diagnostic_row_index": row["diagnostic_row_index"],
        "candidate_rank_within_8a": row.get("candidate_rank_within_8a"),
        "source_free_evidence": {
            "source_coordinate_state": evidence["coordinate_state"],
            "coordinate_state": adjusted_state,
            "source_blocker_class": evidence["blocker_class"],
            "blocker_class": blocker,
            "candidate_role_class": evidence.get("candidate_role_class"),
            "distance_angstrom": evidence.get("distance_angstrom"),
            "same_chain_topology": evidence.get("same_chain_topology"),
            "cross_chain_topology": evidence.get("cross_chain_topology"),
            "ligand_acceptor_same_sequence_entity": evidence.get(
                "ligand_acceptor_same_sequence_entity"
            ),
            "reciprocal_context_class": evidence.get("reciprocal_context_class"),
            "acceptor_residue_code": evidence.get("acceptor_residue_code"),
            "terminal_gamma_atom": evidence.get("terminal_gamma_atom"),
            "acceptor_atom": evidence.get("acceptor_atom"),
            "gamma_metal_geometry": metal,
            "phosphate_transfer_geometry": transfer,
            "coordinate_state_overlay_note": (
                "The source coordinate state remains active_gamma when PG/P3 is present; "
                "the overlay marks metal_absent only for candidate-level cofactor "
                "materialization review."
            ),
        },
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
    }


def state_transfer_row(row: dict[str, Any]) -> dict[str, Any]:
    evidence = row["source_free_evidence"]
    return {
        "row_schema": "epk_gamma_metal_transfer_geometry_state_only_v1",
        "candidate_id": row["candidate_id"],
        "pdb_id": row["pdb_id"],
        "diagnostic_row_index": row["diagnostic_row_index"],
        "source_free_evidence": {
            "source_coordinate_state": evidence["coordinate_state"],
            "coordinate_state": evidence["coordinate_state"],
            "source_blocker_class": evidence["blocker_class"],
            "blocker_class": evidence["blocker_class"],
            "ligand_state": evidence.get("ligand_state"),
            "terminal_gamma_equivalent_atom_available": evidence.get(
                "terminal_gamma_equivalent_atom_available"
            ),
            "candidate_count_within_8a": evidence.get("candidate_count_within_8a"),
            "gamma_metal_geometry": {
                "gamma_metal_shell_class": "unavailable_no_gamma_acceptor_candidate"
            },
            "phosphate_transfer_geometry": {
                "transfer_geometry_status": "unavailable_no_gamma_acceptor_candidate"
            },
        },
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
    }


def is_positive(row: dict[str, Any]) -> bool:
    return row["review_context_for_evaluation_only"]["evaluation_label"] == (
        "positive_true_substrate_acceptor"
    )


def outcome(predicted_positive: bool, actual_positive: bool) -> str:
    if predicted_positive and actual_positive:
        return "true_positive"
    if predicted_positive and not actual_positive:
        return "false_positive"
    if not predicted_positive and actual_positive:
        return "false_negative"
    return "true_negative"


def row_unblocked_prediction(row: dict[str, Any]) -> bool:
    evidence = row["source_free_evidence"]
    return evidence["coordinate_state"] == "active_gamma" and evidence["blocker_class"] == "none"


def reciprocal_tyr_rescue_prediction(row: dict[str, Any]) -> bool:
    evidence = row["source_free_evidence"]
    transfer = evidence["phosphate_transfer_geometry"]
    return bool(
        row_unblocked_prediction(row)
        or (
            evidence.get("source_blocker_class") == "topology_ambiguity"
            and evidence.get("candidate_role_class") == "reciprocal_folded_tyr_candidate"
            and evidence["coordinate_state"] == "active_gamma"
            and transfer.get("acceptor_gamma_bridge_angle_class")
            in {"inline_like_ge_150", "partial_inline_120_to_150"}
        )
    )


def same_chain_transfer_rescue_prediction(row: dict[str, Any]) -> bool:
    evidence = row["source_free_evidence"]
    transfer = evidence["phosphate_transfer_geometry"]
    return bool(
        row_unblocked_prediction(row)
        or (
            evidence.get("source_blocker_class") == "topology_ambiguity"
            and evidence.get("same_chain_topology")
            and evidence["coordinate_state"] == "active_gamma"
            and (evidence.get("distance_angstrom") or 999.0) <= 6.0
            and transfer.get("acceptor_gamma_bridge_angle_class")
            in {"inline_like_ge_150", "partial_inline_120_to_150"}
        )
    )


RuleFn = Callable[[dict[str, Any]], bool]


def candidate_confusion(rows: list[dict[str, Any]], rule_id: str, rule_fn: RuleFn, description: str) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    for row in rows:
        predicted = bool(rule_fn(row))
        result = outcome(predicted, is_positive(row))
        buckets[result].append(row["candidate_id"])
        evidence = row["source_free_evidence"]
        decisions.append(
            {
                "candidate_id": row["candidate_id"],
                "pdb_id": row["pdb_id"],
                "predicted_positive": predicted,
                "outcome": result,
                "coordinate_state": evidence["coordinate_state"],
                "blocker_class": evidence["blocker_class"],
                "source_blocker_class": evidence.get("source_blocker_class"),
                "candidate_role_class": evidence.get("candidate_role_class"),
                "gamma_metal_shell_class": evidence["gamma_metal_geometry"].get(
                    "gamma_metal_shell_class"
                ),
                "acceptor_gamma_bridge_angle_class": evidence[
                    "phosphate_transfer_geometry"
                ].get("acceptor_gamma_bridge_angle_class"),
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": description,
        "row_level": "candidate",
        "confusion_matrix": {key: len(value) for key, value in buckets.items()},
        "pdb_ids_by_outcome": {
            key: sorted({candidate_id.split("|", 1)[0] for candidate_id in value})
            for key, value in buckets.items()
        },
        "candidate_ids_by_outcome": buckets,
        "decisions": decisions,
        "clears_diagnostic_tranche": False,
        "production_claim_allowed": False,
    }


def pdb_confusion(rows: list[dict[str, Any]], rule_id: str, rule_fn: RuleFn, description: str) -> dict[str, Any]:
    by_pdb: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_pdb[row["pdb_id"]].append(row)
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    for pdb_id, pdb_rows in sorted(by_pdb.items()):
        predicted = any(rule_fn(row) for row in pdb_rows)
        actual = any(is_positive(row) for row in pdb_rows)
        result = outcome(predicted, actual)
        buckets[result].append(pdb_id)
        supporting = [row["candidate_id"] for row in pdb_rows if rule_fn(row)]
        decisions.append(
            {
                "pdb_id": pdb_id,
                "predicted_positive": predicted,
                "outcome": result,
                "supporting_candidate_ids": supporting,
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": description,
        "row_level": "pdb",
        "confusion_matrix": {key: len(value) for key, value in buckets.items()},
        "pdb_ids_by_outcome": buckets,
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
        "production_claim_allowed": False,
    }


def counter(rows: list[dict[str, Any]], path: list[str]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        value: Any = row
        for key in path:
            value = value.get(key, {}) if isinstance(value, dict) else {}
        counts[str(value)] += 1
    return dict(sorted(counts.items()))


def hard_case_digest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    wanted = {"5HVK", "6Z3R", "7B56", "9UUR", "9UUX", "9UW4", "3TM0"}
    digest: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["pdb_id"] not in wanted:
            continue
        evidence = row["source_free_evidence"]
        metal = evidence["gamma_metal_geometry"]
        transfer = evidence["phosphate_transfer_geometry"]
        digest.setdefault(row["pdb_id"], []).append(
            {
                "candidate_id": row["candidate_id"],
                "source_coordinate_state": evidence.get("source_coordinate_state"),
                "coordinate_state": evidence["coordinate_state"],
                "source_blocker_class": evidence.get("source_blocker_class"),
                "blocker_class": evidence["blocker_class"],
                "candidate_role_class": evidence.get("candidate_role_class"),
                "distance_angstrom": evidence.get("distance_angstrom"),
                "gamma_metal_shell_class": metal.get("gamma_metal_shell_class"),
                "nearest_metal_to_gamma_distance_angstrom": metal.get(
                    "nearest_metal_to_gamma_distance_angstrom"
                ),
                "acceptor_gamma_bridge_angle_degrees": transfer.get(
                    "acceptor_gamma_bridge_angle_degrees"
                ),
                "acceptor_gamma_bridge_angle_class": transfer.get(
                    "acceptor_gamma_bridge_angle_class"
                ),
            }
        )
    return {key: value for key, value in sorted(digest.items())}


def mixed_reciprocal_digest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    trio_ids = {"9UUR", "9UUX", "9UW4"}
    reciprocal_rows = [
        row
        for row in rows
        if row["pdb_id"] in trio_ids
        and row["source_free_evidence"].get("candidate_role_class")
        == "reciprocal_folded_tyr_candidate"
    ]
    return {
        "rows": hard_case_digest(reciprocal_rows),
        "interpretation": (
            "The reciprocal Tyr candidates in the hard trio share metal_absent overlay "
            "state and do not provide a source-free rescue axis that separates positives "
            "from the 9UW4 counterexample."
        ),
    }


def build_payload(workflow_started_at: str, git_sync_status: str) -> dict[str, Any]:
    source = source_payload()
    cache = PdbAtomCache()
    candidate_rows = [
        candidate_transfer_row(row, cache) for row in source["candidate_evidence_rows"]
    ]
    state_only_rows = [state_transfer_row(row) for row in source["state_only_rows"]]
    all_rows = candidate_rows + state_only_rows

    candidate_sanity = candidate_confusion(
        candidate_rows,
        "metal_adjusted_candidate_no_blocker_sanity_flag_v1",
        row_unblocked_prediction,
        (
            "Candidate-row sanity flag requiring active_gamma after metal overlay and no "
            "structural blocker. This is review-only and not a production substrate-role rule."
        ),
    )
    pdb_sanity = pdb_confusion(
        all_rows,
        "metal_adjusted_pdb_no_blocker_sanity_flag_v1",
        row_unblocked_prediction,
        (
            "PDB-level version of the metal-adjusted unblocked candidate sanity flag. "
            "State and topology cases remain abstention/review evidence."
        ),
    )
    reciprocal_stress = pdb_confusion(
        all_rows,
        "reciprocal_tyr_metal_transfer_rescue_stress_v1",
        reciprocal_tyr_rescue_prediction,
        (
            "Stress-only rescue: baseline unblocked rows plus reciprocal folded-Tyr "
            "topology rows only when the gamma is metal-supported and the bridge angle "
            "is at least partial-inline. Not a production rule."
        ),
    )
    same_chain_stress = pdb_confusion(
        all_rows,
        "same_chain_metal_transfer_rescue_stress_v1",
        same_chain_transfer_rescue_prediction,
        (
            "Stress-only rescue: baseline unblocked rows plus same-chain topology rows "
            "with metal-supported active gamma, <=6 A distance, and at least partial-"
            "inline bridge geometry. This probes whether the new modality admits "
            "same-chain counterexamples."
        ),
    )

    coordinate_state_counts = counter(candidate_rows, ["source_free_evidence", "coordinate_state"])
    source_coordinate_state_counts = counter(
        candidate_rows, ["source_free_evidence", "source_coordinate_state"]
    )
    state_only_coordinate_state_counts = counter(
        state_only_rows, ["source_free_evidence", "coordinate_state"]
    )
    blocker_counts = counter(candidate_rows, ["source_free_evidence", "blocker_class"])
    source_blocker_counts = counter(candidate_rows, ["source_free_evidence", "source_blocker_class"])
    metal_shell_counts = counter(
        candidate_rows, ["source_free_evidence", "gamma_metal_geometry", "gamma_metal_shell_class"]
    )
    bridge_angle_class_counts = counter(
        candidate_rows,
        [
            "source_free_evidence",
            "phosphate_transfer_geometry",
            "acceptor_gamma_bridge_angle_class",
        ],
    )

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )
    primary_outcome = "candidate_evidence_rows_emitted"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    same_chain_false_positives = same_chain_stress["pdb_ids_by_outcome"]["false_positive"]
    reciprocal_false_positives = reciprocal_stress["pdb_ids_by_outcome"]["false_positive"]
    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "A source-free metal cofactor and gamma-phosphate transfer-geometry overlay "
            "can make candidate coordinate state more explicit and may separate hard "
            "topology candidates without using source text or candidate-specific tuning."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(
                {row["pdb_id"] for row in all_rows}
            ),
            "source_candidate_pair_rows": len(source["candidate_evidence_rows"]),
            "source_state_only_rows": len(source["state_only_rows"]),
        },
        "candidate_evidence_rows_emitted": {
            "candidate_pair_rows": len(candidate_rows),
            "state_only_rows": len(state_only_rows),
            "total_rows_in_artifact": len(all_rows),
            "artifact_path": str(DEFAULT_OUTPUT_PATH),
        },
        "coordinate_states_observed": {
            "candidate_pair_rows_after_metal_overlay": coordinate_state_counts,
            "candidate_pair_rows_source_state": source_coordinate_state_counts,
            "state_only_rows": state_only_coordinate_state_counts,
        },
        "source_free_features_tested": [
            "candidate-level gamma metal shell class from model-1 HETATM metal atoms",
            "nearest metal to terminal gamma and acceptor distances",
            "shared gamma/acceptor metal within a broad 8 A cofactor shell",
            "metal-adjusted coordinate state overlay using metal_absent as review evidence",
            "gamma phosphate bridge atom identity from nucleotide coordinate atom names",
            "acceptor-gamma-bridge angle and max acceptor-gamma-neighbor angle classes",
            "stress-only reciprocal Tyr and same-chain topology rescue checks",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            candidate_sanity["rule_id"]: {
                "rule_description": candidate_sanity["rule_description"],
                "row_level": candidate_sanity["row_level"],
                "confusion_matrix": candidate_sanity["confusion_matrix"],
                "pdb_ids_by_outcome": candidate_sanity["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": candidate_sanity["clears_diagnostic_tranche"],
                "production_claim_allowed": candidate_sanity["production_claim_allowed"],
            },
            pdb_sanity["rule_id"]: {
                "rule_description": pdb_sanity["rule_description"],
                "row_level": pdb_sanity["row_level"],
                "confusion_matrix": pdb_sanity["confusion_matrix"],
                "pdb_ids_by_outcome": pdb_sanity["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": pdb_sanity["clears_diagnostic_tranche"],
                "production_claim_allowed": pdb_sanity["production_claim_allowed"],
            },
            reciprocal_stress["rule_id"]: {
                "rule_description": reciprocal_stress["rule_description"],
                "row_level": reciprocal_stress["row_level"],
                "confusion_matrix": reciprocal_stress["confusion_matrix"],
                "pdb_ids_by_outcome": reciprocal_stress["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": reciprocal_stress["clears_diagnostic_tranche"],
                "production_claim_allowed": reciprocal_stress["production_claim_allowed"],
            },
            same_chain_stress["rule_id"]: {
                "rule_description": same_chain_stress["rule_description"],
                "row_level": same_chain_stress["row_level"],
                "confusion_matrix": same_chain_stress["confusion_matrix"],
                "pdb_ids_by_outcome": same_chain_stress["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": same_chain_stress["clears_diagnostic_tranche"],
                "production_claim_allowed": same_chain_stress["production_claim_allowed"],
            },
        },
        "confusion_matrix": pdb_sanity["confusion_matrix"],
        "decisive_counterexamples": {
            "hard_case_rows": hard_case_digest(all_rows),
            "hard_reciprocal_trio": mixed_reciprocal_digest(candidate_rows),
            "same_chain_transfer_stress_false_positive_pdb_ids": same_chain_false_positives,
            "reciprocal_transfer_stress_false_positive_pdb_ids": reciprocal_false_positives,
            "metal_shell_counts": metal_shell_counts,
            "bridge_angle_class_counts": bridge_angle_class_counts,
        },
        "false_positive_analysis": {
            "metal_adjusted_pdb_no_blocker_false_positive_pdb_ids": pdb_sanity[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "reciprocal_tyr_stress_false_positive_pdb_ids": reciprocal_false_positives,
            "same_chain_stress_false_positive_pdb_ids": same_chain_false_positives,
            "interpretation": (
                "The conservative metal overlay does not add false positives, but using "
                "metal-supported same-chain transfer geometry as a rescue admits "
                "counterexamples. Metal and transfer geometry therefore remain blocker "
                "evidence, not source-free substrate-role identity."
            ),
        },
        "false_negative_analysis": {
            "metal_adjusted_pdb_no_blocker_false_negative_pdb_ids": pdb_sanity[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "reciprocal_tyr_stress_false_negative_pdb_ids": reciprocal_stress[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "interpretation": (
                "The metal overlay preserves abstention for product/ADP and topology "
                "positives and can mark some otherwise unblocked positives as "
                "metal_absent when the catalytic cofactor is not materialized near the "
                "selected gamma."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": (
                "Metal/cofactor materialization reduces coordinate-state uncertainty, "
                "but does not clear source-free substrate-role identity. Reciprocal "
                "folded-Tyr candidates remain review-only topology biology, and "
                "same-chain metal-supported transfer geometry is shared by positives "
                "and counterexamples."
            ),
            "candidate_pair_blocker_counts_after_metal_overlay": blocker_counts,
            "candidate_pair_blocker_counts_source": source_blocker_counts,
            "coordinate_state_overlay": (
                "active_gamma source rows with no metal within the broad 8 A gamma shell "
                "are marked metal_absent for review routing only."
            ),
        },
        "next_query": (
            "Treat metal/cofactor geometry as coordinate-state review evidence. Do not "
            "attempt another rescue unless a non-scalar, source-free modality can "
            "separate same-chain metal-supported topology counterexamples and the "
            "9UUR/9UUX/9UW4 reciprocal Tyr trio."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep metal/transfer geometry as "
            "candidate-level blocker evidence and preserve source-reviewed adjudication "
            "for topology and product-state substrate biology."
        ),
        "git_sync_status": git_sync_status,
        "artifact_path": str(DEFAULT_OUTPUT_PATH),
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "source_free_gamma_metal_transfer_geometry_overlay",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "source_free_evidence_separated_from_review_context": True,
            "candidate_specific_threshold_tuning": False,
            "threshold_calibrated": False,
            "raw_coordinate_files_written": False,
            "source_artifact": str(SOURCE_ARTIFACT),
            "candidate_pair_row_count": len(candidate_rows),
            "state_only_row_count": len(state_only_rows),
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "gamma_metal_shell_class": (
                "Source-free model-1 metal proximity class around the selected terminal "
                "gamma atom. The 8 A shell is a broad coordinate-materialization audit "
                "window, not a calibrated substrate-role threshold."
            ),
            "coordinate_state": (
                "Metal-adjusted review overlay. Source active_gamma rows remain "
                "active_gamma only when a model-1 metal is present within the broad "
                "gamma cofactor shell; otherwise they are marked metal_absent."
            ),
            "acceptor_gamma_bridge_angle_class": (
                "Reduced phosphate transfer geometry around the gamma atom and nucleotide "
                "beta-gamma bridge atom. Used only in stress tests, not production rules."
            ),
        },
        "coordinate_state_counts": run_record["coordinate_states_observed"],
        "blocker_class_counts": blocker_counts,
        "source_blocker_class_counts": source_blocker_counts,
        "metal_shell_counts": metal_shell_counts,
        "bridge_angle_class_counts": bridge_angle_class_counts,
        "candidate_transfer_geometry_rows": candidate_rows,
        "state_only_rows": state_only_rows,
        "rules": [candidate_sanity, pdb_sanity, reciprocal_stress, same_chain_stress],
        "blocker_classification": run_record["blocker_classification"],
        "run_record": run_record,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--git-sync-status", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--skip-ledger", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args.workflow_started_at, args.git_sync_status)
    write_json(args.output, payload)
    if not args.skip_ledger:
        append_jsonl(args.ledger, payload["run_record"])


if __name__ == "__main__":
    main()
