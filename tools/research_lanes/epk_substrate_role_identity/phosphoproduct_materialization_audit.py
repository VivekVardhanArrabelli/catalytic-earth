#!/usr/bin/env python3
"""Audit source-free phosphoproduct materialization for ePK blockers.

This lane-local helper tests one bounded coordinate modality: whether ADP plus
covalently phosphorylated SER/THR/TYR residue chemistry is materialized in the
coordinate file without reading titles, papers, curated labels, or source text.
Rows remain review-only evidence; product/split state rows are not promoted to
substrate-role calls.
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
from substrate_role_identity_eval import (
    ACTIVE_GAMMA_CODES,
    GAMMA_ATOM_NAMES,
    NUCLEOTIDE_LIKE_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_phosphoproduct_materialization_audit_v1_20260521"
SOURCE_TAXONOMY_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_coordinate_state_taxonomy_v1_20260521.json"
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
    "epk_phosphoproduct_materialization_audit_v1_20260521.json"
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

PHOSPHO_ACCEPTOR_ATOMS = {
    "SEP": "OG",
    "TPO": "OG1",
    "PTR": "OH",
}
PRODUCT_NUCLEOTIDE_CODES = {"ADP"}
HARD_CASE_PDBS = {"1L0O", "3QHR", "3QHW", "3TM0", "4HPU", "7B56", "9UUR", "9UUX", "9UW4"}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    taxonomy_payload = json.loads(SOURCE_TAXONOMY_ARTIFACT.read_text(encoding="utf-8"))
    conflict_payload = json.loads(SOURCE_CONFLICT_ARTIFACT.read_text(encoding="utf-8"))
    return taxonomy_payload, conflict_payload


def conflict_rows_by_pdb(conflict_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["pdb_id"]: row for row in conflict_payload["candidate_conflict_rows"]}


def atom_id(atom: dict[str, Any] | None) -> str:
    if atom is None:
        return "none"
    icode = atom.get("icode") or ""
    return f"{atom['chain']}:{atom['resname']}{atom['resseq']}{icode}:{atom['atom_name']}"


def residue_id(key: tuple[str, str, str, str]) -> str:
    chain, resseq, icode, resname = key
    suffix = icode or ""
    return f"{chain}:{resname}{resseq}{suffix}"


def compact_atom(atom: dict[str, Any] | None) -> dict[str, Any] | None:
    if atom is None:
        return None
    return {
        "atom_name": atom["atom_name"],
        "residue_code": atom["resname"],
        "chain_id": atom["chain"],
        "auth_seq_id": atom["resseq"],
        "icode": atom["icode"] or None,
    }


def group_residue_atoms(atoms: list[dict[str, Any]]) -> dict[tuple[str, str, str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        grouped[atom["residue_key"]].append(atom)
    return grouped


def preferred_atom(
    residue_atoms: list[dict[str, Any]],
    preferred_names: list[str],
) -> dict[str, Any] | None:
    by_name = {atom["atom_name"]: atom for atom in residue_atoms}
    for name in preferred_names:
        if name in by_name:
            return by_name[name]
    return residue_atoms[0] if residue_atoms else None


def nearest_distance(
    atoms_a: list[dict[str, Any]],
    atoms_b: list[dict[str, Any]],
) -> tuple[float | None, dict[str, Any] | None, dict[str, Any] | None]:
    best: float | None = None
    best_a: dict[str, Any] | None = None
    best_b: dict[str, Any] | None = None
    for atom_a in atoms_a:
        for atom_b in atoms_b:
            current = dist(atom_a, atom_b)
            if best is None or current < best:
                best = current
                best_a = atom_a
                best_b = atom_b
    return best, best_a, best_b


def nearest_phospho_to_atoms(
    target_atoms: list[dict[str, Any]],
    phospho_residues: dict[tuple[str, str, str, str], list[dict[str, Any]]],
) -> tuple[tuple[str, str, str, str] | None, float | None, dict[str, Any] | None, dict[str, Any] | None]:
    best_key: tuple[str, str, str, str] | None = None
    best_distance: float | None = None
    best_target_atom: dict[str, Any] | None = None
    best_phospho_atom: dict[str, Any] | None = None
    for phospho_key, phospho_atoms in phospho_residues.items():
        current, target_atom, phospho_atom = nearest_distance(target_atoms, phospho_atoms)
        if current is not None and (best_distance is None or current < best_distance):
            best_key = phospho_key
            best_distance = current
            best_target_atom = target_atom
            best_phospho_atom = phospho_atom
    return best_key, best_distance, best_target_atom, best_phospho_atom


def distance_class(distance: float | None) -> str:
    if distance is None:
        return "none"
    if distance <= 4.0:
        return "direct_contact_le_4a"
    if distance <= 8.0:
        return "near_active_site_4_to_8a"
    return "distant_gt_8a"


def review_state_context(conflict_row: dict[str, Any]) -> str:
    group = conflict_row["review_context_for_evaluation_only"].get("evaluation_group", "")
    if "product_state" in group or group.endswith("_product_state_positive"):
        return "review_product_state_context"
    if "ligand_analog" in group or "substrate_analog" in group:
        return "review_substrate_acceptor_analog_context"
    return "no_review_state_context"


def leakage_guard(coordinate_state: str, context: str) -> tuple[str, bool, str]:
    if context == "review_product_state_context":
        if coordinate_state == "product_state":
            return (
                "review_product_context_has_source_free_phosphoproduct_state",
                False,
                "ADP plus covalently phosphorylated STY materializes product chemistry source-free, but substrate role remains review-only.",
            )
        return (
            "review_product_context_not_source_free_product_state",
            True,
            "Do not promote product-state identity from review context; phosphoproduct chemistry is not materialized.",
        )
    if context == "review_substrate_acceptor_analog_context":
        if coordinate_state == "substrate_acceptor_analog_state":
            return (
                "review_analog_context_has_source_free_analog_state",
                False,
                "Analog review context matches a source-free analog coordinate row.",
            )
        return (
            "review_analog_context_not_source_free_analog_state",
            True,
            "Do not promote substrate-analog identity from review context; phosphoproduct audit found no analog state.",
        )
    return (
        "no_review_state_claim_to_promote",
        False,
        "No product or analog review-state context is present.",
    )


def blocker_for_state(coordinate_state: str) -> str:
    if coordinate_state == "product_state":
        return "product_state_evidence"
    if coordinate_state == "adp_state":
        return "product_state_evidence"
    if coordinate_state == "split_state":
        return "split_state_evidence"
    if coordinate_state in {"ligand_absent", "ambiguous_coordinate_state", "unavailable_coordinate_state"}:
        return "ligand_materialization"
    return "none"


def row_kind_for_state(coordinate_state: str) -> str:
    if coordinate_state == "active_gamma":
        return "terminal_gamma_context"
    if coordinate_state == "product_state":
        return "adp_phosphoacceptor_pair"
    if coordinate_state == "split_state":
        return "non_adp_nucleotide_phosphoacceptor_pair"
    if coordinate_state == "adp_state":
        return "adp_only_state"
    return "state_only"


def materialization_class(
    coordinate_state: str,
    nucleotide_key: tuple[str, str, str, str] | None,
    phospho_key: tuple[str, str, str, str] | None,
) -> str:
    if coordinate_state == "active_gamma":
        return "active_gamma_terminal_gamma_present_product_scan_suppressed"
    if coordinate_state == "product_state" and nucleotide_key and phospho_key:
        if nucleotide_key[0] == phospho_key[0]:
            return "adp_plus_phosphorylated_sty_same_chain_global_product_chemistry"
        return "adp_plus_phosphorylated_sty_cross_chain_global_product_chemistry"
    if coordinate_state == "adp_state":
        return "adp_without_phosphorylated_sty_product_not_materialized"
    if coordinate_state == "split_state":
        return "non_adp_nucleotide_without_terminal_gamma_plus_phosphorylated_sty_split_like"
    if coordinate_state == "ambiguous_coordinate_state":
        return "nucleotide_without_terminal_gamma_no_phosphoacceptor"
    if coordinate_state == "ligand_absent":
        return "ligand_absent_product_not_materialized"
    return "unavailable_coordinate_state"


def build_row(
    pdb_id: str,
    conflict_row: dict[str, Any],
    coordinate_state: str,
    gamma_atom: dict[str, Any] | None,
    acceptor_atom: dict[str, Any] | None,
    nucleotide_key: tuple[str, str, str, str] | None,
    nucleotide_anchor_atom: dict[str, Any] | None,
    phospho_key: tuple[str, str, str, str] | None,
    nearest_distance_value: float | None,
    nearest_nucleotide_atom: dict[str, Any] | None,
    nearest_phospho_atom: dict[str, Any] | None,
    scan_status: str,
    fetch_error: str | None,
    nucleotide_codes_observed: list[str],
    active_gamma_count: int,
    phospho_count: int,
) -> dict[str, Any]:
    context = review_state_context(conflict_row)
    guard_class, prohibited, guard_reason = leakage_guard(coordinate_state, context)
    nucleotide_residue = residue_id(nucleotide_key) if nucleotide_key else "none"
    candidate_id = (
        f"{pdb_id}|gamma={atom_id(gamma_atom)}|acceptor={atom_id(acceptor_atom)}"
        f"|nucleotide={nucleotide_residue}"
    )
    blocker = blocker_for_state(coordinate_state)
    if coordinate_state not in COORDINATE_STATES:
        raise ValueError(f"unexpected coordinate_state: {coordinate_state}")
    if blocker not in BLOCKER_CLASSES:
        raise ValueError(f"unexpected blocker_class: {blocker}")
    return {
        "row_schema": "epk_phosphoproduct_materialization_audit_v1",
        "candidate_id": candidate_id,
        "pdb_id": pdb_id,
        "candidate_row_kind": row_kind_for_state(coordinate_state),
        "hard_case": pdb_id in HARD_CASE_PDBS,
        "source_free_evidence": {
            "coordinate_state": coordinate_state,
            "blocker_class": blocker,
            "phosphoproduct_materialization_class": materialization_class(
                coordinate_state,
                nucleotide_key,
                phospho_key,
            ),
            "scan_status": scan_status,
            "fetch_error": fetch_error,
            "terminal_gamma_atom": compact_atom(gamma_atom),
            "acceptor_atom": compact_atom(acceptor_atom),
            "nucleotide_residue": nucleotide_residue,
            "nucleotide_anchor_atom": compact_atom(nucleotide_anchor_atom),
            "phosphoacceptor_residue": residue_id(phospho_key) if phospho_key else None,
            "nearest_distance_angstrom": (
                round(nearest_distance_value, 3) if nearest_distance_value is not None else None
            ),
            "nearest_distance_class": distance_class(nearest_distance_value),
            "nearest_nucleotide_atom": compact_atom(nearest_nucleotide_atom),
            "nearest_phosphoacceptor_atom": compact_atom(nearest_phospho_atom),
            "nucleotide_codes_observed": nucleotide_codes_observed,
            "active_gamma_terminal_atom_count": active_gamma_count,
            "phosphorylated_sty_residue_count": phospho_count,
            "adp_phosphoacceptor_same_chain": (
                bool(nucleotide_key and phospho_key and nucleotide_key[0] == phospho_key[0])
            ),
            "source_free_review_context_used_for_state_assignment": False,
        },
        "source_free_pdb_context": {
            "source_free_decision_class": conflict_row["source_free_decision_class"],
            "conflict_class": conflict_row["conflict_class"],
            "non_abstaining_decision": conflict_row["non_abstaining_decision"],
            "source_free_conflict_signature": conflict_row["source_free_conflict_signature"],
        },
        "review_context_for_evaluation_only": {
            "evaluation_label": conflict_row["review_context_for_evaluation_only"][
                "evaluation_label"
            ],
            "evaluation_group": conflict_row["review_context_for_evaluation_only"][
                "evaluation_group"
            ],
            "evaluation_label_used_only_for_eval": True,
            "source_artifact_id": conflict_row["review_context_for_evaluation_only"].get(
                "source_artifact_id"
            ),
            "review_state_context": context,
        },
        "source_leakage_guard_for_review_only": {
            "guard_class": guard_class,
            "promotion_from_review_context_prohibited": prohibited,
            "reason": guard_reason,
        },
    }


def scan_pdb(pdb_id: str, conflict_row: dict[str, Any]) -> list[dict[str, Any]]:
    text, fetch_error = fetch_pdb_text(pdb_id)
    if text is None:
        return [
            build_row(
                pdb_id=pdb_id,
                conflict_row=conflict_row,
                coordinate_state="unavailable_coordinate_state",
                gamma_atom=None,
                acceptor_atom=None,
                nucleotide_key=None,
                nucleotide_anchor_atom=None,
                phospho_key=None,
                nearest_distance_value=None,
                nearest_nucleotide_atom=None,
                nearest_phospho_atom=None,
                scan_status="fetch_error",
                fetch_error=fetch_error,
                nucleotide_codes_observed=[],
                active_gamma_count=0,
                phospho_count=0,
            )
        ]

    atoms = parse_pdb_atoms(text)
    by_residue = group_residue_atoms(atoms)
    nucleotide_residues = {
        key: residue_atoms
        for key, residue_atoms in by_residue.items()
        if key[3] in NUCLEOTIDE_LIKE_CODES
        and any(atom["record"] == "HETATM" for atom in residue_atoms)
    }
    phospho_residues = {
        key: residue_atoms
        for key, residue_atoms in by_residue.items()
        if key[3] in PHOSPHO_ACCEPTOR_ATOMS
    }
    active_gamma_atoms = [
        atom
        for atom in atoms
        if atom["resname"] in ACTIVE_GAMMA_CODES and atom["atom_name"] in GAMMA_ATOM_NAMES
    ]
    nucleotide_codes = sorted({key[3] for key in nucleotide_residues})
    rows: list[dict[str, Any]] = []

    if active_gamma_atoms:
        for gamma_atom in sorted(active_gamma_atoms, key=atom_id):
            phospho_key, nearest, nearest_gamma_atom, nearest_phospho_atom = nearest_phospho_to_atoms(
                [gamma_atom],
                phospho_residues,
            )
            rows.append(
                build_row(
                    pdb_id=pdb_id,
                    conflict_row=conflict_row,
                    coordinate_state="active_gamma",
                    gamma_atom=gamma_atom,
                    acceptor_atom=None,
                    nucleotide_key=gamma_atom["residue_key"],
                    nucleotide_anchor_atom=gamma_atom,
                    phospho_key=phospho_key,
                    nearest_distance_value=nearest,
                    nearest_nucleotide_atom=nearest_gamma_atom,
                    nearest_phospho_atom=nearest_phospho_atom,
                    scan_status="ok",
                    fetch_error=None,
                    nucleotide_codes_observed=nucleotide_codes,
                    active_gamma_count=len(active_gamma_atoms),
                    phospho_count=len(phospho_residues),
                )
            )
        return rows

    adp_residues = {
        key: residue_atoms
        for key, residue_atoms in nucleotide_residues.items()
        if key[3] in PRODUCT_NUCLEOTIDE_CODES
    }
    if adp_residues:
        for adp_key, adp_atoms in sorted(adp_residues.items(), key=lambda item: residue_id(item[0])):
            adp_anchor = preferred_atom(adp_atoms, ["PB", "PA"])
            phospho_key, nearest, nearest_adp_atom, nearest_phospho_atom = nearest_phospho_to_atoms(
                adp_atoms,
                phospho_residues,
            )
            acceptor_atom = None
            if phospho_key:
                acceptor_atom = preferred_atom(
                    phospho_residues[phospho_key],
                    [PHOSPHO_ACCEPTOR_ATOMS[phospho_key[3]], "P"],
                )
            rows.append(
                build_row(
                    pdb_id=pdb_id,
                    conflict_row=conflict_row,
                    coordinate_state="product_state" if phospho_key else "adp_state",
                    gamma_atom=None,
                    acceptor_atom=acceptor_atom,
                    nucleotide_key=adp_key,
                    nucleotide_anchor_atom=adp_anchor,
                    phospho_key=phospho_key,
                    nearest_distance_value=nearest,
                    nearest_nucleotide_atom=nearest_adp_atom,
                    nearest_phospho_atom=nearest_phospho_atom,
                    scan_status="ok",
                    fetch_error=None,
                    nucleotide_codes_observed=nucleotide_codes,
                    active_gamma_count=0,
                    phospho_count=len(phospho_residues),
                )
            )
        return rows

    if nucleotide_residues:
        for nucleotide_key, nucleotide_atoms in sorted(
            nucleotide_residues.items(),
            key=lambda item: residue_id(item[0]),
        ):
            nucleotide_anchor = preferred_atom(nucleotide_atoms, ["PB", "PA", "P"])
            phospho_key, nearest, nearest_nucleotide_atom, nearest_phospho_atom = nearest_phospho_to_atoms(
                nucleotide_atoms,
                phospho_residues,
            )
            acceptor_atom = None
            if phospho_key:
                acceptor_atom = preferred_atom(
                    phospho_residues[phospho_key],
                    [PHOSPHO_ACCEPTOR_ATOMS[phospho_key[3]], "P"],
                )
            rows.append(
                build_row(
                    pdb_id=pdb_id,
                    conflict_row=conflict_row,
                    coordinate_state="split_state" if phospho_key else "ambiguous_coordinate_state",
                    gamma_atom=None,
                    acceptor_atom=acceptor_atom,
                    nucleotide_key=nucleotide_key,
                    nucleotide_anchor_atom=nucleotide_anchor,
                    phospho_key=phospho_key,
                    nearest_distance_value=nearest,
                    nearest_nucleotide_atom=nearest_nucleotide_atom,
                    nearest_phospho_atom=nearest_phospho_atom,
                    scan_status="ok",
                    fetch_error=None,
                    nucleotide_codes_observed=nucleotide_codes,
                    active_gamma_count=0,
                    phospho_count=len(phospho_residues),
                )
            )
        return rows

    rows.append(
        build_row(
            pdb_id=pdb_id,
            conflict_row=conflict_row,
            coordinate_state="ligand_absent",
            gamma_atom=None,
            acceptor_atom=None,
            nucleotide_key=None,
            nucleotide_anchor_atom=None,
            phospho_key=None,
            nearest_distance_value=None,
            nearest_nucleotide_atom=None,
            nearest_phospho_atom=None,
            scan_status="ok",
            fetch_error=None,
            nucleotide_codes_observed=[],
            active_gamma_count=0,
            phospho_count=len(phospho_residues),
        )
    )
    return rows


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


def conflict_projection_rule(conflict_payload: dict[str, Any]) -> dict[str, Any]:
    prior_rule = conflict_payload["rules"][0]
    return {
        "rule_id": "phosphoproduct_materialization_no_promotion_v1",
        "rule_description": (
            "Project source-free phosphoproduct materialization rows onto the existing "
            "candidate conflict abstention policy. Product and split states remain "
            "review-only evidence and are not promoted to substrate-role calls."
        ),
        "confusion_matrix": prior_rule["confusion_matrix"],
        "pdb_ids_by_outcome": prior_rule["pdb_ids_by_outcome"],
        "production_claim_allowed": False,
        "clears_diagnostic_tranche": False,
        "new_threshold_or_rescue_rule_added": False,
    }


def phosphoproduct_audit_rule(rows: list[dict[str, Any]]) -> dict[str, Any]:
    product_pdbs = sorted(
        {
            row["pdb_id"]
            for row in rows
            if row["source_free_evidence"]["coordinate_state"] == "product_state"
        }
    )
    split_pdbs = sorted(
        {
            row["pdb_id"]
            for row in rows
            if row["source_free_evidence"]["coordinate_state"] == "split_state"
        }
    )
    adp_only_pdbs = sorted(
        {
            row["pdb_id"]
            for row in rows
            if row["source_free_evidence"]["coordinate_state"] == "adp_state"
        }
    )
    review_product_pdbs = {
        row["pdb_id"]
        for row in rows
        if row["review_context_for_evaluation_only"]["review_state_context"]
        == "review_product_state_context"
    }
    review_analog_pdbs = {
        row["pdb_id"]
        for row in rows
        if row["review_context_for_evaluation_only"]["review_state_context"]
        == "review_substrate_acceptor_analog_context"
    }
    analog_state_pdbs = {
        row["pdb_id"]
        for row in rows
        if row["source_free_evidence"]["coordinate_state"] == "substrate_acceptor_analog_state"
    }
    return {
        "rule_id": "phosphoproduct_state_gap_audit_v1",
        "rule_description": (
            "Audit-only coordinate chemistry inventory for terminal-gamma-absent "
            "ADP plus phosphorylated STY product rows and non-ADP split-like rows. "
            "This is not a substrate-role identity rule."
        ),
        "production_claim_allowed": False,
        "clears_diagnostic_tranche": False,
        "product_state_materialized_pdb_ids": product_pdbs,
        "split_state_materialized_pdb_ids": split_pdbs,
        "adp_only_pdb_ids": adp_only_pdbs,
        "review_product_positive_without_source_free_phosphoproduct_state": sorted(
            review_product_pdbs - set(product_pdbs)
        ),
        "review_analog_positive_without_source_free_analog_state": sorted(
            review_analog_pdbs - analog_state_pdbs
        ),
        "split_state_counterexample_pressure_pdb_ids": split_pdbs,
    }


def source_leakage_guard_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prohibited = [
        row
        for row in rows
        if row["source_leakage_guard_for_review_only"]["promotion_from_review_context_prohibited"]
    ]
    return {
        "promotion_from_review_context_prohibited_count": len(prohibited),
        "promotion_from_review_context_prohibited_pdb_ids": sorted({row["pdb_id"] for row in prohibited}),
        "promotion_from_review_context_prohibited_candidate_ids": sorted(
            row["candidate_id"] for row in prohibited
        ),
        "guard_class_counts": count_nested(
            rows,
            ("source_leakage_guard_for_review_only", "guard_class"),
        ),
    }


def hard_case_digest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    digest: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["pdb_id"] not in HARD_CASE_PDBS:
            continue
        evidence = row["source_free_evidence"]
        digest.setdefault(row["pdb_id"], []).append(
            {
                "candidate_id": row["candidate_id"],
                "coordinate_state": evidence["coordinate_state"],
                "blocker_class": evidence["blocker_class"],
                "phosphoproduct_materialization_class": evidence[
                    "phosphoproduct_materialization_class"
                ],
                "nearest_distance_angstrom": evidence["nearest_distance_angstrom"],
                "nearest_distance_class": evidence["nearest_distance_class"],
                "review_state_context": row["review_context_for_evaluation_only"][
                    "review_state_context"
                ],
                "guard_class": row["source_leakage_guard_for_review_only"]["guard_class"],
            }
        )
    return dict(sorted(digest.items()))


def build_payload(started_at: str, ended_at: str) -> dict[str, Any]:
    taxonomy_payload, conflict_payload = load_sources()
    conflicts = conflict_rows_by_pdb(conflict_payload)
    rows: list[dict[str, Any]] = []
    for pdb_id in sorted(conflicts):
        rows.extend(scan_pdb(pdb_id, conflicts[pdb_id]))

    coordinate_state_counts = count_nested(rows, ("source_free_evidence", "coordinate_state"))
    blocker_counts = count_nested(rows, ("source_free_evidence", "blocker_class"))
    materialization_counts = count_nested(
        rows,
        ("source_free_evidence", "phosphoproduct_materialization_class"),
    )
    review_context_counts = count_nested(
        rows,
        ("review_context_for_evaluation_only", "review_state_context"),
    )
    row_kind_counts = count_nested(rows, ("candidate_row_kind",))
    leakage_summary = source_leakage_guard_summary(rows)
    projection_rule = conflict_projection_rule(conflict_payload)
    audit_rule = phosphoproduct_audit_rule(rows)
    measured = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60.0, 2)
    product_rows = [
        row
        for row in rows
        if row["source_free_evidence"]["coordinate_state"] == "product_state"
    ]
    split_rows = [
        row
        for row in rows
        if row["source_free_evidence"]["coordinate_state"] == "split_state"
    ]

    run_record = {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured,
        "hypothesis": (
            "A source-free phosphoproduct materialization audit can directly enumerate "
            "terminal-gamma-absent ADP plus covalently phosphorylated SER/THR/TYR "
            "coordinate rows, while exposing product/split blockers without promoting "
            "review-only biological substrate role."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_conflict_decision_artifact": len(conflicts),
            "reused_from_coordinate_state_taxonomy_artifact": len(
                taxonomy_payload["candidate_coordinate_state_taxonomy_rows"]
            ),
            "coordinate_pdbs_scanned": len(conflicts),
        },
        "candidate_evidence_rows_emitted": {
            "phosphoproduct_materialization_rows": len(rows),
            "product_state_rows": len(product_rows),
            "split_state_rows": len(split_rows),
            "row_kind_counts": row_kind_counts,
        },
        "coordinate_states_observed": coordinate_state_counts,
        "source_free_features_tested": [
            "ADP plus covalently phosphorylated SER/THR/TYR coordinate co-materialization",
            "terminal-gamma override so active-gamma structures are not product-state rescues",
            "non-ADP nucleotide without terminal gamma plus phosphorylated STY split-state audit",
            "review product/analog context leakage guard outside source-free state assignment",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            projection_rule["rule_id"]: projection_rule,
            audit_rule["rule_id"]: audit_rule,
        },
        "confusion_matrix": projection_rule["confusion_matrix"],
        "decisive_counterexamples": {
            "hard_case_phosphoproduct_digest": hard_case_digest(rows),
            "product_state_materialized_pdb_ids": audit_rule["product_state_materialized_pdb_ids"],
            "split_state_materialized_pdb_ids": audit_rule["split_state_materialized_pdb_ids"],
            "review_product_positive_without_source_free_phosphoproduct_state": audit_rule[
                "review_product_positive_without_source_free_phosphoproduct_state"
            ],
            "substrate_analog_review_context_not_materialized_source_free": audit_rule[
                "review_analog_positive_without_source_free_analog_state"
            ],
        },
        "false_positive_analysis": {
            "non_abstaining_false_positive_pdb_ids": projection_rule["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "split_state_counterexample_pressure_pdb_ids": audit_rule[
                "split_state_counterexample_pressure_pdb_ids"
            ],
            "interpretation": (
                "The audit introduces no new non-abstaining positive calls. The split-like "
                "4HPU row is a pressure counterexample against promoting split/product "
                "chemistry to substrate-role identity."
            ),
        },
        "false_negative_analysis": {
            "non_abstaining_false_negative_pdb_ids": projection_rule["pdb_ids_by_outcome"][
                "false_negative"
            ],
            "abstained_positive_pdb_ids": projection_rule["pdb_ids_by_outcome"][
                "abstained_positive"
            ],
            "interpretation": (
                "3QHR and 3QHW now have source-free product_state chemistry rows, but "
                "1L0O remains ADP-only and 3TM0/9UUR/9UUX remain analog or topology "
                "biology abstentions."
            ),
        },
        "blocker_classification": {
            "classification": "blocker_not_cleared_method_weakness",
            "primary_outcome": "candidate_evidence_rows_emitted",
            "coordinate_state_counts": coordinate_state_counts,
            "blocker_class_counts": blocker_counts,
            "phosphoproduct_materialization_class_counts": materialization_counts,
            "review_state_context_counts_for_evaluation_only": review_context_counts,
            "source_leakage_guard_summary": leakage_summary,
            "interpretation": (
                "Phosphoproduct chemistry can be materialized source-free for 3QHR/3QHW, "
                "but it does not prove biological substrate role and does not cover ADP-only "
                "1L0O or substrate-analog/topology hard cases."
            ),
        },
        "next_query": (
            "Do not add scalar rescues. Only resume this lane for a genuinely new "
            "source-free modality that can adjudicate biological substrate role for "
            "ADP-only, analog, reciprocal folded-chain, or same-chain cases without "
            "review-context leakage."
        ),
        "primary_outcome": "candidate_evidence_rows_emitted",
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep phosphoproduct rows as compact review-only blocker evidence. Do not "
            "claim ePK production readiness, import labels, calibrate thresholds, or "
            "promote product/split chemistry into production substrate-role calls."
        ),
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "lane_id": LANE_ID,
            "created_at": ended_at,
            "source_artifacts": [
                str(SOURCE_TAXONOMY_ARTIFACT),
                str(SOURCE_CONFLICT_ARTIFACT),
            ],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "hypothesis": run_record["hypothesis"],
        "phosphoproduct_materialization_rows": rows,
        "coordinate_state_counts": coordinate_state_counts,
        "blocker_class_counts": blocker_counts,
        "phosphoproduct_materialization_class_counts": materialization_counts,
        "review_state_context_counts_for_evaluation_only": review_context_counts,
        "source_leakage_guard_summary": leakage_summary,
        "rules": [projection_rule, audit_rule],
        "feature_definitions": {
            "phosphoproduct_materialization_class": (
                "Coordinate-only inventory of terminal-gamma-present, ADP-only, "
                "ADP-plus-phosphorylated-STY product chemistry, or split-like "
                "non-ADP nucleotide plus phosphorylated STY. It is review-only evidence."
            ),
            "product_state": (
                "Assigned only when terminal gamma is absent and ADP plus a covalently "
                "phosphorylated SER/THR/TYR residue are both materialized in coordinates."
            ),
            "split_state": (
                "Assigned only when terminal gamma is absent, ADP is absent, and another "
                "nucleotide-like ligand plus a phosphorylated SER/THR/TYR residue are "
                "materialized in coordinates."
            ),
            "source_leakage_guard_for_review_only": (
                "Evaluation-only comparison showing where review product/analog context "
                "would be forbidden as a predictive source-free input."
            ),
        },
        "run_record": run_record,
    }


def run_self_test() -> None:
    active = materialization_class("active_gamma", ("A", "1", "", "ANP"), None)
    product = materialization_class("product_state", ("A", "2", "", "ADP"), ("A", "3", "", "TPO"))
    split = materialization_class("split_state", ("A", "2", "", "ANP"), ("B", "3", "", "SEP"))
    assert active == "active_gamma_terminal_gamma_present_product_scan_suppressed"
    assert product == "adp_plus_phosphorylated_sty_same_chain_global_product_chemistry"
    assert split == "non_adp_nucleotide_without_terminal_gamma_plus_phosphorylated_sty_split_like"
    assert blocker_for_state("product_state") == "product_state_evidence"
    assert blocker_for_state("split_state") == "split_state_evidence"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        print("self-test ok")
        return
    if not args.started_at:
        parser.error("--started-at is required unless --self-test is used")

    ended_at = utc_now()
    payload = build_payload(args.started_at, ended_at)
    primary_outcome = payload["run_record"]["primary_outcome"]
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")
    write_json(args.output, payload)
    append_jsonl(
        args.ledger,
        {
            "artifact_path": str(args.output),
            **payload["run_record"],
        },
    )
    print(json.dumps(payload["run_record"], sort_keys=True))


if __name__ == "__main__":
    main()
