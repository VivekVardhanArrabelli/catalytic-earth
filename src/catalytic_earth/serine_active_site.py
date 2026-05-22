from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

from .structure import (
    atom_position,
    ligand_context_from_atoms,
    pairwise_distances,
    pocket_context_from_atoms,
    residue_centroid,
)


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
SERINE_NUCLEOPHILE_ATOMS = {"OG"}
HISTIDINE_BASE_ATOMS = {"ND1", "NE2"}
ACID_ORIENTER_ATOMS = {"ASP": {"OD1", "OD2"}, "GLU": {"OE1", "OE2"}}
SER_HIS_CUTOFF_ANGSTROM = 4.0
HIS_ACID_CUTOFF_ANGSTROM = 4.2


def extract_source_free_ser_his_acid_triad(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract a Ser-His-Asp/Glu hydrolase triad from coordinates only."""
    protein_sites = _protein_sites(atoms)
    candidates = _triad_candidates(protein_sites)
    candidates.sort(key=_candidate_sort_key)
    selected = candidates[0] if candidates else None
    residues = list(selected.get("residues", [])) if selected else []
    ligand_context = ligand_context_from_atoms(atoms, residues) if residues else {}
    pocket_context = pocket_context_from_atoms(atoms, residues) if residues else {}
    status = _status_for(selected)
    return {
        "accession": accession,
        "entry_id": row_id or (f"uniprot:{accession}" if accession else None),
        "status": status,
        "status_reason": _status_reason(status),
        "structure_id": structure_id,
        "source_free_coordinate_evidence": True,
        "text_or_label_fields_used_for_predictive_score": False,
        "predictive_input_policy": (
            "Only mmCIF atom coordinates, residue comp ids, atom names, and "
            "Ser-His-acid interatomic distances are used; EC, names, UniProt "
            "prose, and curated labels are excluded."
        ),
        "resolved_residue_count": len(residues),
        "residue_count": len(residues),
        "selected_triad": _public_triad(selected),
        "residues": residues,
        "pairwise_distances_angstrom": pairwise_distances(residues),
        "ligand_context": ligand_context,
        "pocket_context": pocket_context,
        "triad_candidate_count": len(candidates),
        "triad_candidates": [_public_triad(candidate) for candidate in candidates[:8]],
    }


def _triad_candidates(
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    ser_sites = [
        (key, atoms)
        for key, atoms in protein_sites.items()
        if key[0] == "SER" and _atoms_named(atoms, SERINE_NUCLEOPHILE_ATOMS)
    ]
    his_sites = [
        (key, atoms)
        for key, atoms in protein_sites.items()
        if key[0] == "HIS" and _atoms_named(atoms, HISTIDINE_BASE_ATOMS)
    ]
    acid_sites = [
        (key, atoms)
        for key, atoms in protein_sites.items()
        if key[0] in ACID_ORIENTER_ATOMS
        and _atoms_named(atoms, ACID_ORIENTER_ATOMS[key[0]])
    ]
    candidates = []
    for ser_key, ser_atoms in ser_sites:
        for his_key, his_atoms in his_sites:
            ser_his = _nearest_named_atom_pair(
                ser_atoms,
                SERINE_NUCLEOPHILE_ATOMS,
                his_atoms,
                HISTIDINE_BASE_ATOMS,
            )
            if ser_his is None or ser_his[0] > SER_HIS_CUTOFF_ANGSTROM:
                continue
            for acid_key, acid_atoms in acid_sites:
                his_acid = _nearest_named_atom_pair(
                    his_atoms,
                    HISTIDINE_BASE_ATOMS,
                    acid_atoms,
                    ACID_ORIENTER_ATOMS[acid_key[0]],
                )
                if his_acid is None or his_acid[0] > HIS_ACID_CUTOFF_ANGSTROM:
                    continue
                candidates.append(
                    _triad_candidate(
                        ser_key=ser_key,
                        ser_atoms=ser_atoms,
                        his_key=his_key,
                        his_atoms=his_atoms,
                        acid_key=acid_key,
                        acid_atoms=acid_atoms,
                        ser_his=ser_his,
                        his_acid=his_acid,
                    )
                )
    return candidates


def _triad_candidate(
    *,
    ser_key: tuple[str, str, str],
    ser_atoms: list[dict[str, Any]],
    his_key: tuple[str, str, str],
    his_atoms: list[dict[str, Any]],
    acid_key: tuple[str, str, str],
    acid_atoms: list[dict[str, Any]],
    ser_his: tuple[float, dict[str, Any], dict[str, Any]],
    his_acid: tuple[float, dict[str, Any], dict[str, Any]],
) -> dict[str, Any]:
    ser_distance, ser_atom, his_atom = ser_his
    acid_distance, his_acid_atom, acid_atom = his_acid
    residues = [
        _residue(
            ser_key,
            ser_atoms,
            roles=["nucleophile", "covalent catalysis"],
            evidence={
                "evidence_type": "serine_to_histidine_distance",
                "distance_angstrom": round(ser_distance, 3),
                "serine_atom": _atom_name(ser_atom),
                "histidine_atom": _atom_name(his_atom),
            },
        ),
        _residue(
            his_key,
            his_atoms,
            roles=["general_base", "proton acceptor", "proton donor"],
            evidence={
                "evidence_type": "histidine_bridge_distance",
                "serine_distance_angstrom": round(ser_distance, 3),
                "acid_distance_angstrom": round(acid_distance, 3),
                "serine_atom": _atom_name(ser_atom),
                "histidine_serine_atom": _atom_name(his_atom),
                "histidine_acid_atom": _atom_name(his_acid_atom),
                "acid_atom": _atom_name(acid_atom),
            },
        ),
        _residue(
            acid_key,
            acid_atoms,
            roles=["acid_or_orienter", "electrostatic stabiliser"],
            evidence={
                "evidence_type": "acid_to_histidine_distance",
                "distance_angstrom": round(acid_distance, 3),
                "histidine_atom": _atom_name(his_acid_atom),
                "acid_atom": _atom_name(acid_atom),
            },
        ),
    ]
    return {
        "ser_his_distance_angstrom": round(ser_distance, 3),
        "his_acid_distance_angstrom": round(acid_distance, 3),
        "distance_sum_angstrom": round(ser_distance + acid_distance, 3),
        "residues": residues,
    }


def _residue(
    key: tuple[str, str, str],
    atoms: list[dict[str, Any]],
    *,
    roles: list[str],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    code, chain_id, residue_id = key
    return {
        "residue_node_id": f"{chain_id}:{residue_id}:source_free_ser_his_acid_triad",
        "code": code,
        "chain_name": chain_id or None,
        "resid": residue_id or None,
        "atom_count": len(atoms),
        "centroid": residue_centroid(atoms),
        "ca": atom_position(atoms, "CA"),
        "roles": roles,
        "source_free_evidence": evidence,
    }


def _protein_sites(
    atoms: list[dict[str, Any]],
) -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        code = _comp_id(atom)
        if code not in STANDARD_AMINO_ACIDS:
            continue
        by_site[(code, _chain_id(atom), _residue_id(atom))].append(atom)
    return by_site


def _nearest_named_atom_pair(
    left_atoms: list[dict[str, Any]],
    left_names: set[str],
    right_atoms: list[dict[str, Any]],
    right_names: set[str],
) -> tuple[float, dict[str, Any], dict[str, Any]] | None:
    left = _atoms_named(left_atoms, left_names)
    right = _atoms_named(right_atoms, right_names)
    best: tuple[float, dict[str, Any], dict[str, Any]] | None = None
    for left_atom in left:
        left_pos = _atom_coordinate_tuple(left_atom)
        if left_pos is None:
            continue
        for right_atom in right:
            right_pos = _atom_coordinate_tuple(right_atom)
            if right_pos is None:
                continue
            distance = math.dist(left_pos, right_pos)
            if best is None or distance < best[0]:
                best = (distance, left_atom, right_atom)
    return best


def _atoms_named(atoms: list[dict[str, Any]], names: set[str]) -> list[dict[str, Any]]:
    return [atom for atom in atoms if _atom_name(atom) in names]


def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[float, str, str, str]:
    residues = candidate.get("residues", [])
    return (
        float(candidate.get("distance_sum_angstrom", 999.0)),
        str(residues[0].get("chain_name") if residues else ""),
        str(residues[0].get("resid") if residues else ""),
        str(residues[1].get("resid") if len(residues) > 1 else ""),
    )


def _status_for(selected: dict[str, Any] | None) -> str:
    if not selected:
        return "no_source_free_ser_his_acid_triad"
    return "ser_his_acid_triad_resolved"


def _status_reason(status: str) -> str:
    if status == "ser_his_acid_triad_resolved":
        return "Ser-His-Asp/Glu triad distances are resolved from coordinates only"
    return "No coordinate Ser-His-Asp/Glu triad met the distance cutoffs"


def _public_triad(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    if candidate is None:
        return None
    return {
        "ser_his_distance_angstrom": candidate.get("ser_his_distance_angstrom"),
        "his_acid_distance_angstrom": candidate.get("his_acid_distance_angstrom"),
        "distance_sum_angstrom": candidate.get("distance_sum_angstrom"),
        "residue_ids": [
            {
                "code": residue.get("code"),
                "chain_name": residue.get("chain_name"),
                "resid": residue.get("resid"),
            }
            for residue in candidate.get("residues", [])
        ],
    }


def _comp_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def _chain_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def _residue_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def _atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper()


def _atom_coordinate_tuple(atom: dict[str, Any]) -> tuple[float, float, float] | None:
    try:
        return (
            float(atom["Cartn_x"]),
            float(atom["Cartn_y"]),
            float(atom["Cartn_z"]),
        )
    except (KeyError, TypeError, ValueError):
        return None
