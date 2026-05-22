from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

from .structure import (
    METAL_ION_CODES,
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
METAL_COORDINATING_SIDECHAIN_ATOMS = {
    "ASP": {"OD1", "OD2"},
    "GLU": {"OE1", "OE2"},
    "HIS": {"ND1", "NE2"},
    "CYS": {"SG"},
    "SER": {"OG"},
    "THR": {"OG1"},
    "TYR": {"OH"},
    "ASN": {"OD1", "ND2"},
    "GLN": {"OE1", "NE2"},
}
PHOSPHATE_BINDING_SIDECHAIN_ATOMS = {
    "ARG": {"NE", "NH1", "NH2"},
    "ASN": {"ND2", "OD1"},
    "ASP": {"OD1", "OD2"},
    "GLN": {"NE2", "OE1"},
    "GLU": {"OE1", "OE2"},
    "HIS": {"ND1", "NE2"},
    "LYS": {"NZ"},
    "SER": {"OG"},
    "THR": {"OG1"},
    "TYR": {"OH"},
}
IGNORED_SOURCE_FREE_LIGAND_CODES = {"HOH", "WAT", "DOD", "SOL", "MSE"}
PHOSPHATE_LIKE_LIGAND_CODES = {
    "2GP",
    "3PG",
    "6PG",
    "BGP",
    "F6P",
    "G1P",
    "G6P",
    "PGA",
    "PO4",
    "PTR",
    "SEP",
    "TPO",
}
METAL_COORDINATION_CUTOFF_ANGSTROM = 3.0
METAL_TO_PHOSPHATE_CUTOFF_ANGSTROM = 5.0
PHOSPHATE_BINDER_CUTOFF_ANGSTROM = 3.8


def extract_source_free_metal_hydrolase_site(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract a metal-hydrolase active-site proxy from coordinate atoms only."""
    protein_sites = _protein_sites(atoms)
    metal_sites = _metal_sites(atoms)
    phosphate_sites = _phosphate_like_sites(atoms)
    site_summaries = [
        _summarize_metal_site(metal, protein_sites, phosphate_sites)
        for metal in metal_sites
    ]
    site_summaries.sort(key=_site_sort_key)
    site_summaries.reverse()
    selected = site_summaries[0] if site_summaries else None
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
        "metal_site_count": len(metal_sites),
        "phosphate_like_site_count": len(phosphate_sites),
        "selected_site": selected.get("site") if selected else None,
        "source_free_coordinate_evidence": True,
        "text_or_label_fields_used_for_predictive_score": False,
        "predictive_input_policy": (
            "Only mmCIF atom coordinates, residue/ligand comp ids, atom names, "
            "and interatomic distances are used; EC, names, UniProt prose, and "
            "curated labels are excluded."
        ),
        "resolved_residue_count": len(residues),
        "residue_count": len(residues),
        "residues": residues,
        "pairwise_distances_angstrom": pairwise_distances(residues),
        "ligand_context": ligand_context,
        "pocket_context": pocket_context,
        "site_candidates": site_summaries[:8],
    }


def _summarize_metal_site(
    metal_atom: dict[str, Any],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
    phosphate_sites: list[list[dict[str, Any]]],
) -> dict[str, Any]:
    metal = {
        "comp_id": _comp_id(metal_atom),
        "chain_id": _chain_id(metal_atom) or None,
        "residue_id": _residue_id(metal_atom) or None,
        "atom_name": _atom_name(metal_atom) or None,
        "coordinate": _atom_coordinate(metal_atom),
    }
    metal_contacts = _metal_coordination_contacts(metal_atom, protein_sites)
    phosphate_context = _nearest_phosphate_context(metal_atom, phosphate_sites)
    phosphate_contacts = _phosphate_binding_contacts(
        phosphate_context.get("_site_atoms") if phosphate_context else [],
        protein_sites,
    )

    residues_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for contact in metal_contacts:
        residue = _residue_from_contact(contact, role="metal_ligand")
        if residue["code"] in {"ASP", "GLU", "HIS"}:
            residue["roles"].append("water_activator")
        residue["source_free_evidence"] = {
            "evidence_type": "metal_coordination_distance",
            "metal_comp_id": metal["comp_id"],
            "metal_chain_id": metal["chain_id"],
            "metal_residue_id": metal["residue_id"],
            "distance_angstrom": contact["distance_angstrom"],
            "residue_atom": contact["residue_atom"],
        }
        residues_by_key[_residue_key(residue)] = residue

    for contact in phosphate_contacts:
        key = (
            str(contact["residue_code"]),
            str(contact["residue_chain_id"] or ""),
            str(contact["residue_id"] or ""),
        )
        residue = residues_by_key.get(key)
        if residue is None:
            residue = _residue_from_contact(contact, role="leaving_group_stabilizer")
            residue["source_free_evidence"] = {
                "evidence_type": "phosphate_like_ligand_contact",
                "ligand_comp_id": contact["ligand_comp_id"],
                "ligand_chain_id": contact["ligand_chain_id"],
                "ligand_residue_id": contact["ligand_residue_id"],
                "distance_angstrom": contact["distance_angstrom"],
                "residue_atom": contact["residue_atom"],
            }
            residues_by_key[key] = residue
        elif "leaving_group_stabilizer" not in residue["roles"]:
            residue["roles"].append("leaving_group_stabilizer")
            residue["source_free_evidence"]["phosphate_like_contact"] = {
                "ligand_comp_id": contact["ligand_comp_id"],
                "ligand_chain_id": contact["ligand_chain_id"],
                "ligand_residue_id": contact["ligand_residue_id"],
                "distance_angstrom": contact["distance_angstrom"],
                "residue_atom": contact["residue_atom"],
            }

    residues = sorted(
        residues_by_key.values(),
        key=lambda residue: (
            str(residue.get("chain_name") or ""),
            _natural_residue_number(residue.get("resid")),
            str(residue.get("code") or ""),
        ),
    )
    return {
        "site": {
            **metal,
            "coordinating_residue_count": len(metal_contacts),
            "phosphate_like_ligand_detected": phosphate_context is not None,
            "phosphate_like_context": _public_phosphate_context(phosphate_context),
        },
        "metal_ligand_residue_count": len(metal_contacts),
        "acid_base_residue_count": sum(
            1
            for residue in residues
            if residue["code"] in {"ASP", "GLU", "HIS"}
            and "water_activator" in residue["roles"]
        ),
        "phosphate_binder_residue_count": sum(
            1 for residue in residues if "leaving_group_stabilizer" in residue["roles"]
        ),
        "residues": residues,
        "metal_contacts": metal_contacts[:12],
        "phosphate_binding_contacts": phosphate_contacts[:12],
    }


def _metal_coordination_contacts(
    metal_atom: dict[str, Any],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    contacts = []
    for (code, chain_id, residue_id), residue_atoms in protein_sites.items():
        candidate_atoms = [
            atom
            for atom in residue_atoms
            if _atom_name(atom) in METAL_COORDINATING_SIDECHAIN_ATOMS.get(code, set())
        ]
        if not candidate_atoms:
            continue
        nearest = _nearest_atom_pair([metal_atom], candidate_atoms)
        if nearest is None:
            continue
        distance, metal, residue_atom = nearest
        if distance > METAL_COORDINATION_CUTOFF_ANGSTROM:
            continue
        contacts.append(
            {
                "distance_angstrom": round(distance, 3),
                "metal_comp_id": _comp_id(metal),
                "metal_chain_id": _chain_id(metal) or None,
                "metal_residue_id": _residue_id(metal) or None,
                "metal_atom": _atom_name(metal) or None,
                "residue_code": code,
                "residue_chain_id": chain_id or None,
                "residue_id": residue_id or None,
                "residue_atom": _atom_name(residue_atom) or None,
                "_residue_atoms": residue_atoms,
            }
        )
    contacts.sort(
        key=lambda item: (
            float(item["distance_angstrom"]),
            str(item["residue_chain_id"] or ""),
            _natural_residue_number(item["residue_id"]),
            str(item["residue_code"]),
        )
    )
    return contacts


def _phosphate_binding_contacts(
    phosphate_atoms: list[dict[str, Any]],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    if not phosphate_atoms:
        return []
    contacts = []
    polar_phosphate_atoms = [
        atom
        for atom in phosphate_atoms
        if _atom_name(atom).startswith(("O", "P"))
        or str(atom.get("type_symbol", "")).upper() in {"O", "P"}
    ]
    for (code, chain_id, residue_id), residue_atoms in protein_sites.items():
        candidate_atoms = [
            atom
            for atom in residue_atoms
            if _atom_name(atom) in PHOSPHATE_BINDING_SIDECHAIN_ATOMS.get(code, set())
        ]
        if not candidate_atoms:
            continue
        nearest = _nearest_atom_pair(polar_phosphate_atoms, candidate_atoms)
        if nearest is None:
            continue
        distance, ligand_atom, residue_atom = nearest
        if distance > PHOSPHATE_BINDER_CUTOFF_ANGSTROM:
            continue
        contacts.append(
            {
                "distance_angstrom": round(distance, 3),
                "ligand_comp_id": _comp_id(ligand_atom),
                "ligand_chain_id": _chain_id(ligand_atom) or None,
                "ligand_residue_id": _residue_id(ligand_atom) or None,
                "ligand_atom": _atom_name(ligand_atom) or None,
                "residue_code": code,
                "residue_chain_id": chain_id or None,
                "residue_id": residue_id or None,
                "residue_atom": _atom_name(residue_atom) or None,
                "_residue_atoms": residue_atoms,
            }
        )
    contacts.sort(
        key=lambda item: (
            float(item["distance_angstrom"]),
            str(item["residue_chain_id"] or ""),
            _natural_residue_number(item["residue_id"]),
            str(item["residue_code"]),
        )
    )
    return contacts


def _nearest_phosphate_context(
    metal_atom: dict[str, Any],
    phosphate_sites: list[list[dict[str, Any]]],
) -> dict[str, Any] | None:
    contexts = []
    for site_atoms in phosphate_sites:
        nearest = _nearest_atom_pair([metal_atom], site_atoms)
        if nearest is None:
            continue
        distance, _, ligand_atom = nearest
        if distance > METAL_TO_PHOSPHATE_CUTOFF_ANGSTROM:
            continue
        contexts.append(
            {
                "ligand_comp_id": _comp_id(ligand_atom),
                "ligand_chain_id": _chain_id(ligand_atom) or None,
                "ligand_residue_id": _residue_id(ligand_atom) or None,
                "nearest_ligand_atom": _atom_name(ligand_atom) or None,
                "metal_to_ligand_distance_angstrom": round(distance, 3),
                "_site_atoms": site_atoms,
            }
        )
    contexts.sort(
        key=lambda item: (
            float(item["metal_to_ligand_distance_angstrom"]),
            str(item["ligand_comp_id"]),
            str(item["ligand_chain_id"] or ""),
            _natural_residue_number(item["ligand_residue_id"]),
        )
    )
    return contexts[0] if contexts else None


def _residue_from_contact(contact: dict[str, Any], *, role: str) -> dict[str, Any]:
    residue_atoms = list(contact.get("_residue_atoms", []))
    chain_id = contact.get("residue_chain_id")
    residue_id = contact.get("residue_id")
    code = str(contact.get("residue_code") or "")
    return {
        "residue_node_id": f"{chain_id}:{residue_id}:source_free_metal_site",
        "code": code,
        "chain_name": chain_id,
        "resid": residue_id,
        "atom_count": len(residue_atoms),
        "centroid": residue_centroid(residue_atoms),
        "ca": atom_position(residue_atoms, "CA"),
        "roles": [role],
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


def _metal_sites(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM" and _comp_id(atom) in METAL_ION_CODES
    ]


def _phosphate_like_sites(atoms: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") != "HETATM":
            continue
        code = _comp_id(atom)
        if code in IGNORED_SOURCE_FREE_LIGAND_CODES or code in METAL_ION_CODES:
            continue
        by_site[(code, _chain_id(atom), _residue_id(atom))].append(atom)
    return [
        site_atoms
        for site_atoms in by_site.values()
        if _is_phosphate_like_site(site_atoms)
    ]


def _is_phosphate_like_site(site_atoms: list[dict[str, Any]]) -> bool:
    if not site_atoms:
        return False
    comp_id = _comp_id(site_atoms[0])
    if comp_id in PHOSPHATE_LIKE_LIGAND_CODES:
        return True
    return any(
        _atom_name(atom).startswith("P")
        or str(atom.get("type_symbol", "")).upper() == "P"
        for atom in site_atoms
    )


def _nearest_atom_pair(
    left_atoms: list[dict[str, Any]],
    right_atoms: list[dict[str, Any]],
) -> tuple[float, dict[str, Any], dict[str, Any]] | None:
    best: tuple[float, dict[str, Any], dict[str, Any]] | None = None
    for left in left_atoms:
        left_pos = _atom_coordinate_tuple(left)
        if left_pos is None:
            continue
        for right in right_atoms:
            right_pos = _atom_coordinate_tuple(right)
            if right_pos is None:
                continue
            distance = math.dist(left_pos, right_pos)
            if best is None or distance < best[0]:
                best = (distance, left, right)
    return best


def _status_for(selected: dict[str, Any] | None) -> str:
    if not selected:
        return "no_source_free_metal_site"
    if selected["metal_ligand_residue_count"] < 2:
        return "metal_site_undercoordinated"
    if selected["phosphate_binder_residue_count"] > 0:
        return "metal_phosphate_site_resolved"
    return "metal_cluster_without_phosphate_or_substrate_ligand"


def _status_reason(status: str) -> str:
    reasons = {
        "no_source_free_metal_site": "no coordinate metal site was detected",
        "metal_site_undercoordinated": (
            "a coordinate metal is present but fewer than two protein ligands "
            "are resolved within the metal-coordination cutoff"
        ),
        "metal_phosphate_site_resolved": (
            "coordinate metal ligands and a nearby phosphate-like ligand contact "
            "are resolved without source annotations"
        ),
        "metal_cluster_without_phosphate_or_substrate_ligand": (
            "a coordinate metal-ligand cluster is resolved, but no nearby "
            "phosphate-like substrate/product ligand is present"
        ),
    }
    return reasons.get(status, "unclassified source-free metal-site status")


def _site_sort_key(summary: dict[str, Any]) -> tuple[Any, ...]:
    site = summary.get("site", {})
    return (
        int(summary.get("phosphate_binder_residue_count", 0) > 0),
        int(site.get("phosphate_like_ligand_detected", False)),
        int(summary.get("metal_ligand_residue_count", 0)),
        int(summary.get("acid_base_residue_count", 0)),
        str(site.get("comp_id") or ""),
        str(site.get("chain_id") or ""),
        _natural_residue_number(site.get("residue_id")),
    )


def _public_phosphate_context(context: dict[str, Any] | None) -> dict[str, Any] | None:
    if context is None:
        return None
    return {key: value for key, value in context.items() if not key.startswith("_")}


def _residue_key(residue: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(residue.get("code") or ""),
        str(residue.get("chain_name") or ""),
        str(residue.get("resid") or ""),
    )


def _comp_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def _chain_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def _residue_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def _atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper()


def _atom_coordinate(atom: dict[str, Any]) -> dict[str, float] | None:
    coordinate = _atom_coordinate_tuple(atom)
    if coordinate is None:
        return None
    return {
        "x": round(coordinate[0], 3),
        "y": round(coordinate[1], 3),
        "z": round(coordinate[2], 3),
    }


def _atom_coordinate_tuple(atom: dict[str, Any]) -> tuple[float, float, float] | None:
    try:
        return (
            float(atom["Cartn_x"]),
            float(atom["Cartn_y"]),
            float(atom["Cartn_z"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def _natural_residue_number(value: Any) -> tuple[int, str]:
    text = str(value or "")
    digits = ""
    suffix = ""
    for char in text:
        if char.isdigit() or (char == "-" and not digits):
            digits += char
        else:
            suffix += char
    try:
        number = int(digits) if digits not in {"", "-"} else 0
    except ValueError:
        number = 0
    return (number, suffix)
