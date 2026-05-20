#!/usr/bin/env python3
"""Review-only ePK source-free substrate-role diagnostic.

The script fetches PDB-format coordinate files in memory, reduces each
structure to compact source-free structural features, applies two fixed rules,
and writes JSON/JSONL lane artifacts. It deliberately does not read titles,
papers, UniProt prose, EC/Rhea, curated mechanism labels, or production
registries as predictive inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PDB_URL = "https://files.rcsb.org/download/{pdb_id}.pdb"

HYDROXYL_ATOMS = {
    ("SER", "OG"),
    ("THR", "OG1"),
    ("TYR", "OH"),
}

WATER_CODES = {"HOH", "WAT", "DOD"}
METAL_CODES = {
    "MG",
    "MN",
    "ZN",
    "CA",
    "K",
    "NA",
    "CD",
    "CO",
    "FE",
    "NI",
}
NUCLEOTIDE_LIKE_CODES = {
    "ATP",
    "ANP",
    "AGS",
    "ACP",
    "ADP",
    "AMP",
    "GTP",
    "GNP",
    "GDP",
    "GSP",
    "TNP",
    "A3P",
    "APC",
}
GAMMA_ATOM_NAMES = {"PG", "P3"}
ACTIVE_GAMMA_CODES = {"ATP", "ANP", "AGS", "ACP", "GTP", "GNP", "GSP", "TNP", "A3P", "APC"}


FORBIDDEN_PREDICTIVE_FEATURES = [
    "PDB title",
    "UniProt prose",
    "EC/Rhea",
    "paper/source text",
    "mechanism labels",
    "curated substrate names",
    "post-hoc source repair",
    "candidate-specific threshold tuning",
]


DIAGNOSTIC_ROWS = [
    {
        "pdb_id": "5HVK",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive",
        "evaluation_label_source": "prior review-only ePK synthesis: LIMK1/cofilin kinase-substrate co-complex, P23528 Ser3 near ANP PG",
        "requested_set": "positive",
    },
    {
        "pdb_id": "6Z3R",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive",
        "evaluation_label_source": "prior review-only ePK synthesis: SMG1/UPF1 short-peptide positive",
        "requested_set": "positive",
    },
    {
        "pdb_id": "9UUR",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive",
        "evaluation_label_source": "prior review-only ePK synthesis: source-reviewed MEK/ERK Tyr phosphosite positive",
        "requested_set": "positive",
    },
    {
        "pdb_id": "9UUX",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive",
        "evaluation_label_source": "prior review-only ePK synthesis: source-reviewed MEK/ERK Tyr phosphosite positive",
        "requested_set": "positive",
    },
    {
        "pdb_id": "1QMZ",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "3QHR",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "3QHW",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "3X2U",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "3X2V",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "3X2W",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "4IAC",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "review_only_positive_pressure",
        "evaluation_label_source": "user-requested review-only positive candidate; label used only after feature extraction",
        "requested_set": "positive",
    },
    {
        "pdb_id": "2JJ2",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample",
        "evaluation_label_source": "prior review-only ePK synthesis: F1-ATPase ANP false positive / large-chain context",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "7ZE5",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample",
        "evaluation_label_source": "prior review-only ePK synthesis: ABC transporter ATP/ANP/Mg false positive",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "7B56",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample",
        "evaluation_label_source": "prior review-only ePK synthesis: decisive folded/polymer false hit for relaxed protein-role rules",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "9UW4",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "counterexample",
        "evaluation_label_source": "prior review-only ePK synthesis: fresh same-chain topology-confounded nonpositive control",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "3R5F",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "atp_grasp_sibling_control",
        "evaluation_label_source": "prior review-only sibling-control synthesis: ATP-grasp nearest-hydroxyl mimic",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "5C1O",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "atp_grasp_sibling_control",
        "evaluation_label_source": "prior review-only sibling-control synthesis: ATP-grasp nearest-hydroxyl mimic",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "6U1D",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "atp_grasp_pressure",
        "evaluation_label_source": "user-requested ATP-grasp pressure row; label used only after feature extraction",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "6U1E",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "atp_grasp_pressure",
        "evaluation_label_source": "user-requested ATP-grasp pressure row; label used only after feature extraction",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "5TT6",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "same_chain_atpase_ligase_pressure",
        "evaluation_label_source": "user-requested same-chain ATPase/ligase pressure row; label used only after feature extraction",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "6NOO",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "same_chain_atpase_ligase_pressure",
        "evaluation_label_source": "user-requested same-chain ATPase/ligase pressure row; label used only after feature extraction",
        "requested_set": "counterexample",
    },
    {
        "pdb_id": "9NBW",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "same_chain_atpase_ligase_pressure",
        "evaluation_label_source": "user-requested same-chain ATPase/ligase pressure row; label used only after feature extraction",
        "requested_set": "counterexample",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def dist(a: dict[str, Any], b: dict[str, Any]) -> float:
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2 + (a["z"] - b["z"]) ** 2)


def parse_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def fetch_pdb_text(pdb_id: str, timeout: int = 30) -> tuple[str | None, str | None]:
    url = PDB_URL.format(pdb_id=pdb_id.upper())
    request = urllib.request.Request(url, headers={"User-Agent": "catalytic-earth-review-only/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace"), None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, repr(exc)


def parse_pdb_atoms(text: str) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    in_first_model = False
    saw_model = False
    for line in text.splitlines():
        rec = line[0:6].strip()
        if rec == "MODEL":
            saw_model = True
            if not in_first_model:
                in_first_model = True
                continue
        if rec == "ENDMDL" and saw_model:
            break
        if saw_model and not in_first_model:
            continue
        if rec not in {"ATOM", "HETATM"}:
            continue
        altloc = line[16:17].strip()
        if altloc not in {"", "A", "1"}:
            continue
        x = parse_float(line[30:38].strip())
        y = parse_float(line[38:46].strip())
        z = parse_float(line[46:54].strip())
        if x is None or y is None or z is None:
            continue
        element = line[76:78].strip().upper()
        atom_name = line[12:16].strip().upper()
        if not element:
            element = "".join(ch for ch in atom_name if ch.isalpha())[:1].upper()
        atoms.append(
            {
                "record": rec,
                "atom_name": atom_name,
                "resname": line[17:20].strip().upper(),
                "chain": line[21:22].strip() or "_",
                "resseq": line[22:26].strip(),
                "icode": line[26:27].strip(),
                "x": x,
                "y": y,
                "z": z,
                "element": element,
                "residue_key": (
                    line[21:22].strip() or "_",
                    line[22:26].strip(),
                    line[26:27].strip(),
                    line[17:20].strip().upper(),
                ),
            }
        )
    return atoms


def residue_sort_key(key: tuple[str, str, str, str]) -> tuple[int, float | str, str]:
    _, resseq, icode, _ = key
    try:
        return (0, float(resseq), icode)
    except ValueError:
        return (1, resseq, icode)


def chain_residue_maps(atoms: list[dict[str, Any]]) -> tuple[dict[str, list[tuple[str, str, str, str]]], dict[str, int]]:
    residues_by_chain: dict[str, set[tuple[str, str, str, str]]] = defaultdict(set)
    for atom in atoms:
        if atom["record"] == "ATOM":
            residues_by_chain[atom["chain"]].add(atom["residue_key"])
    sorted_by_chain = {
        chain: sorted(residues, key=residue_sort_key)
        for chain, residues in residues_by_chain.items()
    }
    residue_ordinals = {
        "|".join(key): index + 1
        for chain, residues in sorted_by_chain.items()
        for index, key in enumerate(residues)
    }
    return sorted_by_chain, residue_ordinals


def polymer_entity_count_by_sequence(residues_by_chain: dict[str, list[tuple[str, str, str, str]]]) -> int:
    sequences = set()
    for residues in residues_by_chain.values():
        sequences.add(tuple(residue[-1] for residue in residues))
    return len(sequences)


def compact_atom(atom: dict[str, Any] | None) -> dict[str, Any] | None:
    if not atom:
        return None
    return {
        "atom_name": atom["atom_name"],
        "residue_code": atom["resname"],
        "chain_id": atom["chain"],
        "auth_seq_id": atom["resseq"],
        "icode": atom["icode"] or None,
    }


def nearest_pair(gamma_atoms: list[dict[str, Any]], acceptor_atoms: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, dict[str, Any] | None, float | None]:
    best_gamma = None
    best_acceptor = None
    best_distance = None
    for gamma in gamma_atoms:
        for acceptor in acceptor_atoms:
            current = dist(gamma, acceptor)
            if best_distance is None or current < best_distance:
                best_distance = current
                best_gamma = gamma
                best_acceptor = acceptor
    if best_distance is None:
        return None, None, None
    return best_gamma, best_acceptor, round(best_distance, 3)


def local_atom_count(center: dict[str, Any], atoms: list[dict[str, Any]], radius: float) -> int:
    return sum(1 for atom in atoms if atom is not center and dist(center, atom) <= radius)


def nearest_nonpolymer_oxygen(
    gamma_atom: dict[str, Any] | None,
    hetero_atoms: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, float | None]:
    if not gamma_atom:
        return None, None
    best_atom = None
    best_distance = None
    selected_key = gamma_atom["residue_key"]
    for atom in hetero_atoms:
        if atom["element"] != "O":
            continue
        if atom["resname"] in WATER_CODES:
            continue
        if atom["residue_key"] == selected_key:
            continue
        current = dist(gamma_atom, atom)
        if best_distance is None or current < best_distance:
            best_distance = current
            best_atom = atom
    if best_distance is None:
        return None, None
    return best_atom, round(best_distance, 3)


def nearest_nucleotide_or_metal_to_atom(
    center: dict[str, Any] | None,
    hetero_atoms: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, float | None]:
    if not center:
        return None, None
    best_atom = None
    best_distance = None
    for atom in hetero_atoms:
        if atom["resname"] not in NUCLEOTIDE_LIKE_CODES and atom["resname"] not in METAL_CODES:
            continue
        current = dist(center, atom)
        if best_distance is None or current < best_distance:
            best_distance = current
            best_atom = atom
    if best_distance is None:
        return None, None
    return best_atom, round(best_distance, 3)


def chain_has_own_nucleotide_or_metal(
    chain_id: str | None,
    hetero_atoms: list[dict[str, Any]],
    selected_gamma_atom: dict[str, Any] | None,
) -> bool | None:
    if not chain_id:
        return None
    selected_residue = selected_gamma_atom["residue_key"] if selected_gamma_atom else None
    for atom in hetero_atoms:
        if atom["chain"] != chain_id:
            continue
        if selected_residue is not None and atom["residue_key"] == selected_residue:
            continue
        if atom["resname"] in NUCLEOTIDE_LIKE_CODES or atom["resname"] in METAL_CODES:
            return True
    return False


def residue_chain_position(
    atom: dict[str, Any] | None,
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
    residue_ordinals: dict[str, int],
) -> tuple[int | None, int | None]:
    if not atom:
        return None, None
    key = atom["residue_key"]
    chain_len = len(residues_by_chain.get(atom["chain"], []))
    ordinal = residue_ordinals.get("|".join(key))
    return chain_len or None, ordinal


def ligand_state(nucleotide_atoms: list[dict[str, Any]], gamma_atoms: list[dict[str, Any]]) -> str:
    if gamma_atoms:
        codes = sorted({atom["resname"] for atom in gamma_atoms})
        return "active_gamma_capable:" + ",".join(codes)
    if nucleotide_atoms:
        codes = sorted({atom["resname"] for atom in nucleotide_atoms})
        return "nucleotide_like_without_terminal_gamma:" + ",".join(codes)
    return "no_nucleotide_like_ligand_detected"


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
    candidate_is_tyr = acceptor_atom["resname"] == "TYR"
    candidate_is_short_peptide_like = bool(candidate_chain_len is not None and candidate_chain_len <= 40)
    candidate_is_midlength = bool(candidate_chain_len is not None and 41 <= candidate_chain_len <= 119)
    candidate_is_folded_like = bool(candidate_chain_len is not None and candidate_chain_len >= 120)
    cross_chain = gamma_atom["chain"] != acceptor_atom["chain"]
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
        "same_chain_topology": not cross_chain,
        "cross_chain_topology": cross_chain,
        "candidate_acceptor_is_n_terminal_sty": candidate_is_n_terminal_sty,
        "candidate_acceptor_is_tyr": candidate_is_tyr,
        "candidate_acceptor_chain_is_short_peptide_like": candidate_is_short_peptide_like,
        "candidate_acceptor_chain_is_midlength": candidate_is_midlength,
        "candidate_acceptor_chain_is_folded_like": candidate_is_folded_like,
        "candidate_chain_has_own_nucleotide_or_metal": chain_has_own_nucleotide_or_metal(
            acceptor_atom["chain"], hetero_atoms, gamma_atom
        ),
    }


def hydroxyl_pair_candidates(
    gamma_atoms: list[dict[str, Any]],
    hydroxyl_atoms: list[dict[str, Any]],
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
    residue_ordinals: dict[str, int],
    hetero_atoms: list[dict[str, Any]],
    max_distance: float = 8.0,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
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


def nearest_strict_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    for candidate in candidates:
        if candidate["distance_angstrom"] > 6.0:
            continue
        if not candidate["cross_chain_topology"]:
            continue
        if candidate["candidate_chain_has_own_nucleotide_or_metal"]:
            continue
        if (
            candidate["candidate_acceptor_chain_is_short_peptide_like"]
            or candidate["candidate_acceptor_is_n_terminal_sty"]
            or candidate["candidate_acceptor_is_tyr"]
        ):
            return candidate
    return None


def reduced_features(pdb_id: str, row_template: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text(pdb_id)
    base = {
        "pdb_id": pdb_id,
        "requested_set": row_template["requested_set"],
        "evaluation_label": row_template["evaluation_label"],
        "evaluation_group": row_template["evaluation_group"],
        "evaluation_label_source": row_template["evaluation_label_source"],
        "evaluation_label_used_only_for_eval": True,
        "feature_extraction_started_after": workflow_started_at,
        "source_free_feature_only": True,
        "forbidden_predictive_features_excluded": FORBIDDEN_PREDICTIVE_FEATURES,
    }
    if text is None:
        base.update(
            {
                "fetch_status": "error",
                "fetch_error": fetch_error,
                "pdb_sha256_12": None,
                "atom_count_model1": 0,
                "structure_features": empty_feature_payload(),
            }
        )
        return base

    atoms = parse_pdb_atoms(text)
    atom_atoms = [atom for atom in atoms if atom["record"] == "ATOM"]
    hetero_atoms = [atom for atom in atoms if atom["record"] == "HETATM"]
    residues_by_chain, residue_ordinals = chain_residue_maps(atoms)
    nucleotide_atoms = [atom for atom in hetero_atoms if atom["resname"] in NUCLEOTIDE_LIKE_CODES]
    gamma_atoms = [
        atom
        for atom in nucleotide_atoms
        if atom["resname"] in ACTIVE_GAMMA_CODES and atom["atom_name"] in GAMMA_ATOM_NAMES
    ]
    hydroxyl_atoms = [
        atom for atom in atom_atoms if (atom["resname"], atom["atom_name"]) in HYDROXYL_ATOMS
    ]
    gamma_atom, acceptor_atom, nearest_hydroxyl_distance = nearest_pair(gamma_atoms, hydroxyl_atoms)
    nonpolymer_o_atom, nonpolymer_o_distance = nearest_nonpolymer_oxygen(gamma_atom, hetero_atoms)
    local_context_atom, local_context_distance = nearest_nucleotide_or_metal_to_atom(acceptor_atom, hetero_atoms)
    pair_candidates = hydroxyl_pair_candidates(
        gamma_atoms, hydroxyl_atoms, residues_by_chain, residue_ordinals, hetero_atoms
    )
    strict_candidate = nearest_strict_candidate(pair_candidates)

    candidate_chain_len, candidate_ordinal = residue_chain_position(
        acceptor_atom, residues_by_chain, residue_ordinals
    )
    ligand_chain_len, _ = residue_chain_position(gamma_atom, residues_by_chain, residue_ordinals)
    same_chain = bool(gamma_atom and acceptor_atom and gamma_atom["chain"] == acceptor_atom["chain"])
    cross_chain = bool(gamma_atom and acceptor_atom and gamma_atom["chain"] != acceptor_atom["chain"])
    candidate_is_sty = bool(acceptor_atom and acceptor_atom["resname"] in {"SER", "THR", "TYR"})
    candidate_is_n_terminal_sty = bool(
        candidate_is_sty and candidate_ordinal is not None and candidate_ordinal <= 5
    )
    candidate_is_tyr = bool(acceptor_atom and acceptor_atom["resname"] == "TYR")
    candidate_is_short_peptide_like = bool(candidate_chain_len is not None and candidate_chain_len <= 40)
    candidate_is_midlength = bool(candidate_chain_len is not None and 41 <= candidate_chain_len <= 119)
    candidate_is_folded_like = bool(candidate_chain_len is not None and candidate_chain_len >= 120)
    acceptor_has_local_nucleotide_or_metal = bool(
        local_context_distance is not None and local_context_distance <= 8.0
    )
    reciprocal_cross_chain_topology = bool(cross_chain and gamma_atom and acceptor_atom)

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
        "ligand_chain_length": ligand_chain_len,
        "same_chain_topology": same_chain,
        "cross_chain_topology": cross_chain,
        "reciprocal_cross_chain_topology": reciprocal_cross_chain_topology,
        "polymer_chain_count": len(residues_by_chain),
        "polymer_entity_count_sequence_proxy": polymer_entity_count_by_sequence(residues_by_chain),
        "candidate_acceptor_is_n_terminal_sty": candidate_is_n_terminal_sty,
        "candidate_acceptor_is_tyr": candidate_is_tyr,
        "candidate_acceptor_chain_is_short_peptide_like": candidate_is_short_peptide_like,
        "candidate_acceptor_chain_is_midlength": candidate_is_midlength,
        "candidate_acceptor_chain_is_folded_like": candidate_is_folded_like,
        "candidate_local_atom_count_within_8a": local_atom_count(acceptor_atom, atom_atoms, 8.0)
        if acceptor_atom
        else None,
        "candidate_local_context_nearest_nucleotide_or_metal_distance_angstrom": local_context_distance,
        "candidate_local_context_nearest_nucleotide_or_metal_atom": compact_atom(local_context_atom),
        "candidate_acceptor_chain_has_local_nucleotide_or_metal": acceptor_has_local_nucleotide_or_metal,
        "candidate_chain_has_own_nucleotide_or_metal": chain_has_own_nucleotide_or_metal(
            acceptor_atom["chain"] if acceptor_atom else None, hetero_atoms, gamma_atom
        ),
        "nearest_hydroxyl_pair_candidates_within_8a": pair_candidates[:8],
        "nearest_strict_cross_chain_candidate": strict_candidate,
        "co_materialized_gamma_and_hydroxyl_in_one_structure": bool(gamma_atom and acceptor_atom),
    }
    base.update(
        {
            "fetch_status": "ok",
            "pdb_sha256_12": hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
            "atom_count_model1": len(atoms),
            "structure_features": features,
        }
    )
    return base


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
        "ligand_chain_length": None,
        "same_chain_topology": None,
        "cross_chain_topology": None,
        "reciprocal_cross_chain_topology": None,
        "polymer_chain_count": None,
        "polymer_entity_count_sequence_proxy": None,
        "candidate_acceptor_is_n_terminal_sty": False,
        "candidate_acceptor_is_tyr": False,
        "candidate_acceptor_chain_is_short_peptide_like": False,
        "candidate_acceptor_chain_is_midlength": False,
        "candidate_acceptor_chain_is_folded_like": False,
        "candidate_local_atom_count_within_8a": None,
        "candidate_local_context_nearest_nucleotide_or_metal_distance_angstrom": None,
        "candidate_local_context_nearest_nucleotide_or_metal_atom": None,
        "candidate_acceptor_chain_has_local_nucleotide_or_metal": None,
        "candidate_chain_has_own_nucleotide_or_metal": None,
        "nearest_hydroxyl_pair_candidates_within_8a": [],
        "nearest_strict_cross_chain_candidate": None,
        "co_materialized_gamma_and_hydroxyl_in_one_structure": False,
    }


def rule_strict_structural(features: dict[str, Any]) -> bool:
    return bool(features["nearest_strict_cross_chain_candidate"])


def rule_permissive_nearest_hydroxyl(features: dict[str, Any]) -> bool:
    distance = features["nearest_protein_hydroxyl_distance_angstrom"]
    return bool(features["terminal_gamma_equivalent_atom_available"] and distance is not None and distance <= 6.0)


RULES = {
    "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1": {
        "description": (
            "PG/P3 gamma-equivalent present; nearest eligible protein hydroxyl <=6.0 A; "
            "acceptor chain differs from ligand chain; acceptor chain lacks its own "
            "nucleotide/metal hetero context; and acceptor is short-peptide-like, "
            "N-terminal STY (first five resolved residues), or Tyr. This scans compact "
            "candidate pairs rather than requiring the global nearest hydroxyl to be the substrate."
        ),
        "function": rule_strict_structural,
    },
    "permissive_nearest_hydroxyl_6a_v1": {
        "description": "PG/P3 gamma-equivalent present and nearest protein Ser/Thr/Tyr hydroxyl <=6.0 A.",
        "function": rule_permissive_nearest_hydroxyl,
    },
}


def is_positive_label(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def classify_failure_mode(row: dict[str, Any], predicted_positive: bool) -> str | None:
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
        strict_candidate = features.get("nearest_strict_cross_chain_candidate")
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
        if features["nearest_nonpolymer_oxygen_distance_angstrom"] is not None:
            return "acceptor_identity_ambiguity"
        return "biological_role_ambiguity"
    if actual_positive and not predicted_positive:
        if features["same_chain_topology"]:
            return "topology_ambiguity"
        if features["candidate_acceptor_chain_is_folded_like"] and not (
            features["candidate_acceptor_is_tyr"] or features["candidate_acceptor_is_n_terminal_sty"]
        ):
            return "peptide_vs_folded_substrate_ambiguity"
        distance = features["nearest_protein_hydroxyl_distance_angstrom"]
        if distance is None or distance > 6.0:
            return "structure_not_containing_biological_substrate_state"
        if features["candidate_acceptor_chain_has_local_nucleotide_or_metal"]:
            return "acceptor_identity_ambiguity"
        return "method_weakness"
    return "method_weakness"


def confusion_for_rule(rows: list[dict[str, Any]], rule_id: str, rule_spec: dict[str, Any]) -> dict[str, Any]:
    tp: list[str] = []
    fp: list[str] = []
    tn: list[str] = []
    fn: list[str] = []
    decisions = []
    failure_counts: Counter[str] = Counter()
    for row in rows:
        predicted_positive = bool(rule_spec["function"](row["structure_features"]))
        actual_positive = is_positive_label(row)
        if predicted_positive and actual_positive:
            tp.append(row["pdb_id"])
        elif predicted_positive and not actual_positive:
            fp.append(row["pdb_id"])
        elif (not predicted_positive) and actual_positive:
            fn.append(row["pdb_id"])
        else:
            tn.append(row["pdb_id"])
        failure_mode = classify_failure_mode(row, predicted_positive)
        if failure_mode:
            failure_counts[failure_mode] += 1
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": (
                    "true_positive"
                    if predicted_positive and actual_positive
                    else "false_positive"
                    if predicted_positive and not actual_positive
                    else "false_negative"
                    if (not predicted_positive) and actual_positive
                    else "true_negative"
                ),
                "failure_mode": failure_mode,
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": rule_spec["description"],
        "confusion_matrix": {
            "true_positive": len(tp),
            "false_positive": len(fp),
            "true_negative": len(tn),
            "false_negative": len(fn),
        },
        "pdb_ids_by_outcome": {
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn,
        },
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "decisions": decisions,
        "clears_diagnostic_tranche": not fp and not fn,
    }


def derive_primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    aggregate_failures: Counter[str] = Counter()
    for result in rule_results:
        aggregate_failures.update(result["failure_mode_counts"])
    if aggregate_failures.get("sibling_family_mimicry", 0) or aggregate_failures.get("topology_ambiguity", 0):
        return "blocker_not_cleared_biology_ambiguity"
    if aggregate_failures.get("structure_not_containing_biological_substrate_state", 0) >= 3:
        return "blocker_not_cleared_data_scarcity"
    return "blocker_not_cleared_method_weakness"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--artifact-dir", default="artifacts/research_lanes/epk_substrate_role_identity")
    args = parser.parse_args(argv)

    run_started_at = utc_now()
    artifact_dir = Path(args.artifact_dir)
    tranche_path = artifact_dir / "epk_substrate_role_identity_tranche_20260520.json"
    eval_path = artifact_dir / "epk_substrate_role_identity_rule_eval_20260520.json"
    ledger_path = artifact_dir / "epk_substrate_role_identity_runs.jsonl"

    rows: list[dict[str, Any]] = []
    for row_template in DIAGNOSTIC_ROWS:
        rows.append(reduced_features(row_template["pdb_id"], row_template, args.workflow_started_at))
        time.sleep(0.1)

    rule_results = [
        confusion_for_rule(rows, rule_id, rule_spec)
        for rule_id, rule_spec in RULES.items()
    ]
    primary_outcome = derive_primary_outcome(rule_results)
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    materialized_rows = [row for row in rows if row["fetch_status"] == "ok"]

    tranche_payload = {
        "metadata": {
            "artifact_id": "epk_substrate_role_identity_tranche_20260520",
            "created_at": utc_now(),
            "workflow_started_at": args.workflow_started_at,
            "script_run_started_at": run_started_at,
            "method": "source_free_structure_reduction_from_pdb_model1",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "row_count": len(rows),
            "materialized_row_count": len(materialized_rows),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "raw_coordinate_files_written": False,
        },
        "feature_definitions": {
            "terminal_gamma_equivalent_atom_available": "A nucleotide-like nonpolymer residue has atom PG or P3 in model 1.",
            "nearest_protein_hydroxyl_distance_angstrom": "Minimum distance from any terminal gamma-equivalent atom to any resolved Ser OG, Thr OG1, or Tyr OH atom.",
            "nearest_nonpolymer_oxygen_distance_angstrom": "Minimum distance from selected gamma-equivalent atom to any non-water HETATM oxygen outside the selected nucleotide residue.",
            "reciprocal_cross_chain_topology": "Selected nearest gamma/hydroxyl pair spans two chains; no source role assignment is implied.",
            "polymer_entity_count_sequence_proxy": "Count of distinct resolved ATOM residue-name sequences across chains.",
            "candidate_acceptor_is_n_terminal_sty": "Nearest hydroxyl residue is Ser/Thr/Tyr within the first five resolved residues of its chain.",
            "candidate_chain_has_own_nucleotide_or_metal": "A nucleotide-like ligand or metal is assigned to the candidate chain ID, excluding the selected nucleotide residue.",
            "nearest_strict_cross_chain_candidate": "Nearest compact hydroxyl pair satisfying the strict rule preconditions; null means no such source-free candidate.",
        },
        "rows": rows,
    }

    eval_payload = {
        "metadata": {
            "artifact_id": "epk_substrate_role_identity_rule_eval_20260520",
            "created_at": utc_now(),
            "workflow_started_at": args.workflow_started_at,
            "script_run_started_at": run_started_at,
            "method": "fixed_source_free_rule_eval_against_review_only_labels",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "primary_outcome": primary_outcome,
            "rule_count": len(rule_results),
            "row_count": len(rows),
            "positive_label_count": sum(1 for row in rows if is_positive_label(row)),
            "counterexample_label_count": sum(1 for row in rows if not is_positive_label(row)),
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
        },
        "rules": rule_results,
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "data_scarcity_signal": "Positive pressure rows include repeat/review-only positives; current synthesis still reports 0 fresh clean folded-protein positives.",
            "method_weakness_signal": "Nearest-hydroxyl and simple cross-chain/locality rules do not encode kinase/substrate role identity.",
            "biology_ambiguity_signal": "ATP-dependent sibling families, ATPases/transporters, kinase-kinase, and folded-substrate contexts can co-materialize gamma-proximal Ser/Thr/Tyr hydroxyls without making them true ePK substrate phosphoacceptors.",
            "historical_comparator_assessment": "Comparable blockers in this project have not been cleared by structure-only nearest-atom rules; prior accepted progress required source-reviewed hybrid evidence kept outside predictive features.",
        },
    }

    write_json(tranche_path, tranche_payload)
    write_json(eval_path, eval_payload)

    append_jsonl(
        ledger_path,
        {
            "run_started_at": run_started_at,
            "workflow_started_at": args.workflow_started_at,
            "completed_at": utc_now(),
            "primary_outcome": primary_outcome,
            "tranche_path": str(tranche_path),
            "rule_eval_path": str(eval_path),
            "row_count": len(rows),
            "materialized_row_count": len(materialized_rows),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
    )

    print(json.dumps({"primary_outcome": primary_outcome, "row_count": len(rows), "fetch_status_counts": dict(fetch_counts)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
