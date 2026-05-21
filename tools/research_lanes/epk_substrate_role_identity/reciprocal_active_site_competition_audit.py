#!/usr/bin/env python3
"""Audit reciprocal active-site competition for ePK substrate-role blockers.

This lane-local helper tests one bounded source-free modality: whether
reciprocal folded-chain candidates are isolated at their gamma site or compete
with same-chain hydroxyl candidates, and whether the acceptor residue has a
simple ligand-chain ordinal/auth counterpart. It writes compact reduced
evidence only and does not promote reciprocal signatures into substrate-role
identity calls.
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
    chain_residue_maps,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_reciprocal_active_site_competition_audit_v1_20260521"
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
    "epk_reciprocal_active_site_competition_audit_v1_20260521.json"
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

STATE_BLOCKERS = {
    "adp_state": "product_state_evidence",
    "product_state": "product_state_evidence",
    "split_state": "split_state_evidence",
    "substrate_acceptor_analog_state": "substrate_analog_evidence",
    "ligand_absent": "ligand_materialization",
    "unavailable_coordinate_state": "ligand_materialization",
    "ambiguous_coordinate_state": "ligand_materialization",
    "metal_absent": "active_gamma_geometry",
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


def atom_id(atom: dict[str, Any] | None) -> str:
    if not atom:
        return "none"
    suffix = atom.get("icode") or ""
    return (
        f"{atom.get('chain_id')}:{atom.get('residue_code')}"
        f"{atom.get('auth_seq_id')}{suffix}:{atom.get('atom_name')}"
    )


def gamma_site_id(row: dict[str, Any]) -> str:
    return f"{row['pdb_id']}|gamma={atom_id(evidence(row).get('terminal_gamma_atom'))}"


def topology_class(e: dict[str, Any]) -> str:
    if e.get("same_chain_topology"):
        return "same_chain_topology"
    if e.get("cross_chain_topology"):
        return "cross_chain_topology"
    return "topology_unavailable"


def acceptor_residue_class(e: dict[str, Any]) -> str:
    residue = e.get("acceptor_residue_code")
    if residue in {"TYR", "PTR"}:
        return "tyr_acceptor"
    if residue in {"SER", "THR", "SEP", "TPO"}:
        return "ser_thr_acceptor"
    if residue is None:
        return "no_acceptor_residue"
    return "other_acceptor_residue"


def chain_size_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_chain_is_short_peptide_like"):
        return "short_peptide_like_acceptor_chain"
    if e.get("acceptor_chain_is_folded_like"):
        return "folded_like_acceptor_chain"
    return "acceptor_chain_size_unclassified"


def terminal_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
        return "internal_fragment_like_n_terminal"
    if e.get("acceptor_resolved_n_terminal_auth_terminal_like"):
        return "auth_terminal_like_n_terminal"
    if e.get("acceptor_is_n_terminal_sty"):
        return "resolved_n_terminal_sty_without_auth_support"
    return "not_resolved_n_terminal_sty"


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


def distance_order_class(
    candidate_distance: float | None,
    nearest_same_chain_distance: float | None,
) -> str:
    if candidate_distance is None:
        return "candidate_distance_unavailable"
    if nearest_same_chain_distance is None:
        return "no_same_chain_competitor_within_preexisting_6a_shell"
    rounded_candidate = round(candidate_distance, 3)
    rounded_same = round(nearest_same_chain_distance, 3)
    if rounded_candidate == rounded_same:
        return "reciprocal_same_chain_distance_tie_at_0_001a"
    if rounded_candidate < rounded_same:
        return "reciprocal_closer_than_same_chain_competitor"
    return "same_chain_competitor_closer_than_reciprocal"


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


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


def residue_key_from_compact(atom: dict[str, Any] | None) -> tuple[str, str, str, str] | None:
    if not atom:
        return None
    return (
        atom["chain_id"],
        str(atom["auth_seq_id"]),
        atom.get("icode") or "",
        atom["residue_code"],
    )


def compact_residue(residue: tuple[str, str, str, str] | None, ordinal: int | None) -> dict[str, Any] | None:
    if residue is None:
        return None
    chain_id, auth_seq_id, icode, residue_code = residue
    return {
        "chain_id": chain_id,
        "auth_seq_id": auth_seq_id,
        "icode": icode or None,
        "residue_code": residue_code,
        "resolved_ordinal_in_chain": ordinal,
    }


def hydroxyl_residue_class(residue: tuple[str, str, str, str] | None) -> str:
    if residue is None:
        return "counterpart_unavailable"
    residue_code = residue[3]
    if residue_code == "TYR":
        return "counterpart_tyr_hydroxyl"
    if residue_code in {"SER", "THR"}:
        return "counterpart_ser_thr_hydroxyl"
    return "counterpart_not_sty_hydroxyl"


def fetch_residue_maps(pdb_ids: set[str]) -> tuple[
    dict[str, dict[str, list[tuple[str, str, str, str]]]],
    dict[str, tuple[str, str | None]],
]:
    maps_by_pdb: dict[str, dict[str, list[tuple[str, str, str, str]]]] = {}
    status_by_pdb: dict[str, tuple[str, str | None]] = {}
    for pdb_id in sorted(pdb_ids):
        text, fetch_error = fetch_pdb_text(pdb_id)
        if text is None:
            maps_by_pdb[pdb_id] = {}
            status_by_pdb[pdb_id] = ("error", fetch_error)
            continue
        atoms = parse_pdb_atoms(text)
        residues_by_chain, _ = chain_residue_maps(atoms)
        maps_by_pdb[pdb_id] = residues_by_chain
        status_by_pdb[pdb_id] = ("ok", None)
    return maps_by_pdb, status_by_pdb


def counterpart_context(
    row: dict[str, Any],
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
    fetch_status: str,
    fetch_error: str | None,
) -> dict[str, Any]:
    e = evidence(row)
    gamma_atom = e.get("terminal_gamma_atom")
    acceptor_atom = e.get("acceptor_atom")
    if e.get("coordinate_state") != "active_gamma" or not gamma_atom or not acceptor_atom:
        return {
            "counterpart_status": f"not_applicable_{e.get('coordinate_state') or 'unknown_state'}",
            "counterpart_fetch_status": fetch_status,
            "counterpart_fetch_error": fetch_error,
            "ligand_chain_ordinal_counterpart": None,
            "ligand_chain_auth_counterpart": None,
            "ordinal_counterpart_class": "counterpart_not_applicable",
            "auth_counterpart_class": "counterpart_not_applicable",
            "acceptor_residue_found_in_model": False,
            "acceptor_resolved_ordinal_in_model": None,
        }
    if fetch_status != "ok":
        return {
            "counterpart_status": "fetch_error",
            "counterpart_fetch_status": fetch_status,
            "counterpart_fetch_error": fetch_error,
            "ligand_chain_ordinal_counterpart": None,
            "ligand_chain_auth_counterpart": None,
            "ordinal_counterpart_class": "counterpart_unavailable",
            "auth_counterpart_class": "counterpart_unavailable",
            "acceptor_residue_found_in_model": False,
            "acceptor_resolved_ordinal_in_model": None,
        }

    ligand_chain = gamma_atom["chain_id"]
    acceptor_chain = acceptor_atom["chain_id"]
    ligand_residues = residues_by_chain.get(ligand_chain, [])
    acceptor_residues = residues_by_chain.get(acceptor_chain, [])
    acceptor_key = residue_key_from_compact(acceptor_atom)
    acceptor_ordinal: int | None = None
    if acceptor_key in acceptor_residues:
        acceptor_ordinal = acceptor_residues.index(acceptor_key) + 1
    elif e.get("acceptor_residue_ordinal_in_chain") is not None:
        acceptor_ordinal = int(e["acceptor_residue_ordinal_in_chain"])

    ordinal_residue = None
    if acceptor_ordinal is not None and 1 <= acceptor_ordinal <= len(ligand_residues):
        ordinal_residue = ligand_residues[acceptor_ordinal - 1]

    auth_residue = None
    auth_ordinal = None
    for index, residue in enumerate(ligand_residues, start=1):
        if residue[1] == str(acceptor_atom["auth_seq_id"]) and residue[2] == (
            acceptor_atom.get("icode") or ""
        ):
            auth_residue = residue
            auth_ordinal = index
            break

    return {
        "counterpart_status": "ok",
        "counterpart_fetch_status": fetch_status,
        "counterpart_fetch_error": fetch_error,
        "ligand_chain_ordinal_counterpart": compact_residue(ordinal_residue, acceptor_ordinal),
        "ligand_chain_auth_counterpart": compact_residue(auth_residue, auth_ordinal),
        "ordinal_counterpart_class": hydroxyl_residue_class(ordinal_residue),
        "auth_counterpart_class": hydroxyl_residue_class(auth_residue),
        "acceptor_residue_found_in_model": acceptor_key in acceptor_residues,
        "acceptor_resolved_ordinal_in_model": acceptor_ordinal,
    }


def gamma_site_competition(row: dict[str, Any], gamma_rows: list[dict[str, Any]]) -> dict[str, Any]:
    e = evidence(row)
    active_rows = [
        candidate
        for candidate in gamma_rows
        if evidence(candidate).get("coordinate_state") == "active_gamma"
        and evidence(candidate).get("distance_angstrom") is not None
    ]
    sorted_rows = sorted(
        active_rows,
        key=lambda candidate: (
            evidence(candidate).get("distance_angstrom") is None,
            evidence(candidate).get("distance_angstrom") or 999.0,
            candidate["candidate_id"],
        ),
    )
    rank = None
    for index, candidate in enumerate(sorted_rows, start=1):
        if candidate["candidate_id"] == row["candidate_id"]:
            rank = index
            break

    same_chain = [
        candidate
        for candidate in active_rows
        if evidence(candidate).get("same_chain_topology")
        and evidence(candidate).get("distance_angstrom") is not None
        and evidence(candidate)["distance_angstrom"] <= 6.0
    ]
    cross_chain_folded = [
        candidate
        for candidate in active_rows
        if evidence(candidate).get("cross_chain_topology")
        and evidence(candidate).get("acceptor_chain_is_folded_like")
        and not evidence(candidate).get("acceptor_chain_is_short_peptide_like")
        and evidence(candidate).get("distance_angstrom") is not None
        and evidence(candidate)["distance_angstrom"] <= 6.0
    ]
    nearest_same = min(
        (evidence(candidate)["distance_angstrom"] for candidate in same_chain),
        default=None,
    )
    nearest_cross = min(
        (evidence(candidate)["distance_angstrom"] for candidate in cross_chain_folded),
        default=None,
    )
    candidate_distance = e.get("distance_angstrom")
    candidate_is_reciprocal = (
        e.get("candidate_role_class") == "reciprocal_folded_tyr_candidate"
        or (e.get("reciprocal_context_class") or "").startswith("reciprocal_")
    )
    if e.get("coordinate_state") != "active_gamma":
        competition_class = f"not_applicable_{e.get('coordinate_state') or 'unknown_state'}"
    elif not candidate_is_reciprocal:
        competition_class = "not_reciprocal_folded_candidate"
    else:
        competition_class = distance_order_class(candidate_distance, nearest_same)

    delta = None
    if candidate_distance is not None and nearest_same is not None:
        delta = round(candidate_distance - nearest_same, 3)

    return {
        "gamma_site_id": gamma_site_id(row),
        "gamma_site_active_candidate_count": len(active_rows),
        "candidate_rank_by_gamma_distance": rank,
        "same_chain_competitor_count_le_6a": len(same_chain),
        "cross_chain_folded_competitor_count_le_6a": len(cross_chain_folded),
        "nearest_same_chain_competitor_distance_angstrom": nearest_same,
        "nearest_cross_chain_folded_competitor_distance_angstrom": nearest_cross,
        "candidate_minus_nearest_same_chain_distance_angstrom": delta,
        "reciprocal_competition_class": competition_class,
        "same_chain_competitor_candidate_ids_le_6a": sorted(
            candidate["candidate_id"] for candidate in same_chain
        ),
        "cross_chain_folded_candidate_ids_le_6a": sorted(
            candidate["candidate_id"] for candidate in cross_chain_folded
        ),
    }


def competition_signature(
    row: dict[str, Any],
    competition: dict[str, Any],
    counterpart: dict[str, Any],
) -> dict[str, Any]:
    e = evidence(row)
    return {
        "coordinate_state": e.get("coordinate_state"),
        "blocker_class": e.get("blocker_class"),
        "candidate_role_class": e.get("candidate_role_class") or "state_only",
        "topology_class": topology_class(e),
        "reciprocal_context_class": e.get("reciprocal_context_class") or "none",
        "acceptor_residue_class": acceptor_residue_class(e),
        "acceptor_terminal_class": terminal_class(e),
        "acceptor_chain_size_class": chain_size_class(e),
        "gamma_site_active_candidate_count_class": count_class(
            competition["gamma_site_active_candidate_count"]
        ),
        "same_chain_competitor_count_le_6a_class": count_class(
            competition["same_chain_competitor_count_le_6a"]
        ),
        "cross_chain_folded_competitor_count_le_6a_class": count_class(
            competition["cross_chain_folded_competitor_count_le_6a"]
        ),
        "reciprocal_competition_class": competition["reciprocal_competition_class"],
        "ordinal_counterpart_class": counterpart["ordinal_counterpart_class"],
        "auth_counterpart_class": counterpart["auth_counterpart_class"],
    }


def competition_blocker_class(e: dict[str, Any]) -> str:
    state = e.get("coordinate_state")
    if state in STATE_BLOCKERS:
        return STATE_BLOCKERS[state]
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like") and not e.get(
        "acceptor_chain_is_short_peptide_like"
    ):
        return "internal_fragment_mimicry"
    if e.get("same_chain_topology") or (e.get("reciprocal_context_class") or "").startswith(
        "reciprocal_"
    ):
        return "topology_ambiguity"
    return e.get("blocker_class") or "active_gamma_geometry"


def build_competition_row(
    row: dict[str, Any],
    rows_by_gamma: dict[str, list[dict[str, Any]]],
    residue_maps_by_pdb: dict[str, dict[str, list[tuple[str, str, str, str]]]],
    fetch_status_by_pdb: dict[str, tuple[str, str | None]],
) -> dict[str, Any]:
    pdb_id = row["pdb_id"]
    fetch_status, fetch_error = fetch_status_by_pdb[pdb_id]
    competition = gamma_site_competition(row, rows_by_gamma[gamma_site_id(row)])
    counterpart = counterpart_context(
        row, residue_maps_by_pdb[pdb_id], fetch_status, fetch_error
    )
    e = evidence(row)
    signature = competition_signature(row, competition, counterpart)
    return {
        "candidate_id": row["candidate_id"],
        "diagnostic_row_index": row.get("diagnostic_row_index"),
        "pdb_id": pdb_id,
        "review_context_for_evaluation_only": row["review_context_for_evaluation_only"],
        "row_schema": "epk_reciprocal_active_site_competition_audit_v1",
        "source_free_evidence": {
            "coordinate_state": e.get("coordinate_state"),
            "source_blocker_class": e.get("blocker_class"),
            "blocker_class": competition_blocker_class(e),
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
            "candidate_chain_active_gamma_count": e.get("candidate_chain_active_gamma_count"),
            "candidate_chain_has_own_nucleotide_or_metal": e.get(
                "candidate_chain_has_own_nucleotide_or_metal"
            ),
            "gamma_site_competition": competition,
            "ligand_chain_counterpart_context": counterpart,
            "reciprocal_competition_signature": signature,
            "reciprocal_competition_signature_id": stable_signature_id(signature),
        },
    }


def label_collision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[evidence(row)["reciprocal_competition_signature_id"]].append(row)

    collisions = []
    for signature_id, group in sorted(grouped.items()):
        labels = Counter(review_label(row) for row in group)
        positives = labels.get("positive_true_substrate_acceptor", 0)
        negatives = labels.get("counterexample_not_true_substrate_acceptor", 0)
        if positives and negatives:
            collision_class = "mixed_positive_counterexample_competition_signature"
        elif positives:
            collision_class = "positive_only_competition_signature"
        else:
            collision_class = "counterexample_only_competition_signature"
        collisions.append(
            {
                "reciprocal_competition_signature_id": signature_id,
                "reciprocal_competition_signature": evidence(group[0])[
                    "reciprocal_competition_signature"
                ],
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


def hard_case_digest(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    digest: dict[str, list[dict[str, Any]]] = {}
    for pdb_id in sorted(HARD_CASE_PDBS):
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
                "distance_angstrom": evidence(row)["distance_angstrom"],
                "reciprocal_competition_class": evidence(row)["gamma_site_competition"][
                    "reciprocal_competition_class"
                ],
                "candidate_minus_nearest_same_chain_distance_angstrom": evidence(row)[
                    "gamma_site_competition"
                ]["candidate_minus_nearest_same_chain_distance_angstrom"],
                "same_chain_competitor_candidate_ids_le_6a": evidence(row)[
                    "gamma_site_competition"
                ]["same_chain_competitor_candidate_ids_le_6a"],
                "ordinal_counterpart_class": evidence(row)["ligand_chain_counterpart_context"][
                    "ordinal_counterpart_class"
                ],
                "auth_counterpart_class": evidence(row)["ligand_chain_counterpart_context"][
                    "auth_counterpart_class"
                ],
                "reciprocal_competition_signature_id": evidence(row)[
                    "reciprocal_competition_signature_id"
                ],
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

    residue_maps_by_pdb, fetch_status_by_pdb = fetch_residue_maps(
        {row["pdb_id"] for row in input_rows}
    )
    rows_by_gamma: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in input_rows:
        rows_by_gamma[gamma_site_id(row)].append(row)

    competition_rows = [
        build_competition_row(row, rows_by_gamma, residue_maps_by_pdb, fetch_status_by_pdb)
        for row in input_rows
    ]
    state_only_rows = [
        row for row in competition_rows if evidence(row)["candidate_role_class"] == "state_only"
    ]
    candidate_pair_rows = [
        row for row in competition_rows if evidence(row)["candidate_role_class"] != "state_only"
    ]
    reciprocal_rows = [
        row
        for row in competition_rows
        if evidence(row)["gamma_site_competition"]["reciprocal_competition_class"]
        not in {
            "not_reciprocal_folded_candidate",
            "not_applicable_adp_state",
            "not_applicable_product_state",
            "not_applicable_split_state",
            "not_applicable_ligand_absent",
            "not_applicable_ambiguous_coordinate_state",
        }
    ]
    collision_rows = label_collision_rows(competition_rows)
    mixed_collision_rows = [
        row
        for row in collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_competition_signature"
    ]
    reciprocal_collision_rows = label_collision_rows(reciprocal_rows)
    mixed_reciprocal_collision_rows = [
        row
        for row in reciprocal_collision_rows
        if row["collision_class"] == "mixed_positive_counterexample_competition_signature"
    ]

    confusion_matrix, pdb_ids_by_outcome = project_no_promotion_confusion(conflict_payload)
    coordinate_state_counts = Counter(evidence(row)["coordinate_state"] for row in competition_rows)
    blocker_class_counts = Counter(evidence(row)["blocker_class"] for row in competition_rows)
    competition_class_counts = Counter(
        evidence(row)["gamma_site_competition"]["reciprocal_competition_class"]
        for row in competition_rows
    )
    counterpart_class_counts = Counter(
        evidence(row)["ligand_chain_counterpart_context"]["ordinal_counterpart_class"]
        for row in competition_rows
    )
    signature_collision_counts = Counter(row["collision_class"] for row in collision_rows)
    reciprocal_signature_collision_counts = Counter(
        row["collision_class"] for row in reciprocal_collision_rows
    )
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
            "A source-free reciprocal active-site competition audit can test whether "
            "folded reciprocal acceptors are structurally isolated from same-chain "
            "hydroxyl competitors, and whether simple ligand-chain ordinal/auth "
            "counterparts separate 9UUR/9UUX-like positives from 9UW4-like pressure."
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
            "coordinate_pdbs_scanned": len(residue_maps_by_pdb),
        },
        "candidate_evidence_rows_emitted": {
            "reciprocal_competition_rows": len(competition_rows),
            "candidate_pair_rows": len(candidate_pair_rows),
            "state_only_rows": len(state_only_rows),
            "reciprocal_folded_candidate_rows": len(reciprocal_rows),
            "competition_signature_rows": len(collision_rows),
            "mixed_competition_signature_rows": len(mixed_collision_rows),
            "reciprocal_signature_rows": len(reciprocal_collision_rows),
            "mixed_reciprocal_signature_rows": len(mixed_reciprocal_collision_rows),
        },
        "coordinate_states_observed": dict(sorted(coordinate_state_counts.items())),
        "source_free_features_tested": [
            "per-gamma-site same-chain hydroxyl competitor count within the preexisting 6A shell",
            "reciprocal folded candidate distance order relative to same-chain competitors",
            "candidate gamma-site rank by source-free gamma/acceptor distance",
            "ligand-chain residue counterpart at the candidate acceptor resolved ordinal",
            "ligand-chain residue counterpart at the candidate acceptor auth residue number",
            "reciprocal competition signature collision audit with review labels used only after grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "reciprocal_active_site_competition_no_promotion_v1": {
                "rule_id": "reciprocal_active_site_competition_no_promotion_v1",
                "rule_description": (
                    "Emit reciprocal active-site competition and ligand-chain counterpart "
                    "rows while preserving the existing source-free conflict abstention "
                    "policy; no reciprocal signature is promoted to substrate-role identity."
                ),
                "new_threshold_or_rescue_rule_added": False,
                "clears_diagnostic_tranche": False,
                "confusion_matrix": confusion_matrix,
                "pdb_ids_by_outcome": pdb_ids_by_outcome,
                "production_claim_allowed": False,
            },
            "reciprocal_competition_signature_collision_audit_v1": {
                "rule_id": "reciprocal_competition_signature_collision_audit_v1",
                "rule_description": (
                    "Group source-free reciprocal competition signatures before evaluating "
                    "labels; collisions and residual positive abstentions block promotion."
                ),
                "competition_signature_count": len(collision_rows),
                "mixed_competition_signature_count": len(mixed_collision_rows),
                "reciprocal_signature_count": len(reciprocal_collision_rows),
                "mixed_reciprocal_signature_count": len(mixed_reciprocal_collision_rows),
                "collision_class_counts": dict(sorted(signature_collision_counts.items())),
                "reciprocal_collision_class_counts": dict(
                    sorted(reciprocal_signature_collision_counts.items())
                ),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": confusion_matrix,
        "decisive_counterexamples": {
            "positive_only_reciprocal_signature_not_a_rule": (
                "The isolated reciprocal Tyr competition signature is positive-only for "
                "9UUR/9UUX in this tranche, but promoting that narrow distance/order split "
                "would be a post-hoc rescue rule and would not address product/ADP or "
                "same-chain substrate biology."
            ),
            "9UW4_same_reciprocal_family_pressure": (
                "9UW4 is separated by a same-gamma same-chain competitor tie, which is useful "
                "counterpressure evidence but still a review-routing feature rather than "
                "source-free substrate-role proof."
            ),
            "mixed_same_chain_competition_signatures": (
                "Nine broader competition signatures mix positives and counterexamples, "
                "especially same-chain rows, so competition context is not a general "
                "substrate-role identity rule."
            ),
            "state_specific_positive_abstentions": (
                "1L0O, 3QHR, and 3QHW remain product/ADP review-state positives rather "
                "than active-gamma substrate-role calls."
            ),
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": pdb_ids_by_outcome.get("false_positive", []),
            "interpretation": (
                "No new non-abstaining positive calls were introduced. Reciprocal-specific "
                "competition separates 9UUR/9UUX from 9UW4 in this tranche, but the positive-only "
                "split is kept as review evidence instead of a post-hoc rescue rule."
            ),
        },
        "false_negative_analysis": {
            "abstained_positive_pdb_ids": pdb_ids_by_outcome.get("abstained_positive", []),
            "non_abstaining_false_negative_pdb_ids": pdb_ids_by_outcome.get("false_negative", []),
            "interpretation": (
                "The existing no-promotion projection keeps product/ADP, same-chain, and "
                "reciprocal folded-chain positives abstained rather than treating them as "
                "active-gamma false negatives."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
            "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
            "reciprocal_competition_class_counts": dict(sorted(competition_class_counts.items())),
            "ordinal_counterpart_class_counts": dict(sorted(counterpart_class_counts.items())),
            "competition_signature_collision_class_counts": dict(
                sorted(signature_collision_counts.items())
            ),
            "reciprocal_signature_collision_class_counts": dict(
                sorted(reciprocal_signature_collision_counts.items())
            ),
            "interpretation": (
                "Reciprocal active-site competition is compact structural review evidence. "
                "It reduces the 9UUR/9UUX/9UW4 uncertainty, but same-chain signature collisions "
                "and product-state biology still require source-reviewed adjudication."
            ),
        },
        "next_query": (
            "Do not add reciprocal distance/order rescue rules. Only resume this lane for "
            "a genuinely different source-free modality that can adjudicate state-specific "
            "or reciprocal folded-chain biology without review-context leakage."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep reciprocal competition rows as review-only blocker evidence. Do not claim "
            "ePK production readiness or promote reciprocal competition signatures into "
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
            "candidate_evidence_row_count": len(competition_rows),
            "candidate_pair_row_count": len(candidate_pair_rows),
            "state_only_row_count": len(state_only_rows),
            "diagnostic_pdb_count": len(residue_maps_by_pdb),
            "raw_coordinate_files_written": False,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "same_chain_competitor_count_le_6a": (
                "Number of same-gamma candidate hydroxyl rows on the nucleotide/gamma chain "
                "within the preexisting 6A candidate shell."
            ),
            "reciprocal_competition_class": (
                "Categorical distance-order relation between a reciprocal folded candidate "
                "and the nearest same-chain gamma-site competitor; used only for review routing."
            ),
            "ligand_chain_ordinal_counterpart": (
                "Residue on the nucleotide/gamma chain at the same resolved ordinal as the "
                "candidate acceptor residue, if available from model-1 coordinates."
            ),
            "ligand_chain_auth_counterpart": (
                "Residue on the nucleotide/gamma chain with the same auth residue number and "
                "insertion code as the candidate acceptor residue, if present."
            ),
        },
        "counterpart_fetch_status_counts": dict(sorted(fetch_counts.items())),
        "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
        "blocker_class_counts": dict(sorted(blocker_class_counts.items())),
        "reciprocal_competition_class_counts": dict(sorted(competition_class_counts.items())),
        "ordinal_counterpart_class_counts": dict(sorted(counterpart_class_counts.items())),
        "competition_signature_collision_class_counts": dict(sorted(signature_collision_counts.items())),
        "reciprocal_signature_collision_class_counts": dict(
            sorted(reciprocal_signature_collision_counts.items())
        ),
        "reciprocal_active_site_competition_rows": competition_rows,
        "competition_signature_collision_rows": collision_rows,
        "reciprocal_signature_collision_rows": reciprocal_collision_rows,
        "hard_case_competition_digest": hard_case_digest(competition_rows),
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
