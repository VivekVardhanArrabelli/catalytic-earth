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


PLP_LIKE_CODES = {"PLP", "LLP", "PMP", "P5P", "PLV", "PDD", "5PA"}
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

SIDECHAIN_ATOMS = {
    "ARG": {"NE", "NH1", "NH2"},
    "ASP": {"OD1", "OD2"},
    "GLU": {"OE1", "OE2"},
    "HIS": {"ND1", "NE2"},
    "LYS": {"NZ"},
    "SER": {"OG"},
    "THR": {"OG1"},
    "TYR": {"OH"},
}
PHOSPHATE_BINDER_CODES = {"GLY", "SER", "THR"}
ACID_BASE_CODES = {"ASP", "GLU", "HIS", "TYR"}
PLP_ALDIMINE_ATOMS = {"C4A", "N4A"}


def extract_source_free_plp_active_site(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract PLP active-site evidence from coordinate atoms only.

    This function deliberately ignores EC numbers, protein names, UniProt prose,
    and curated labels. It selects the best PLP-like coordinate site and reports
    whether that site carries a covalent/modified lysine anchor plus nearby
    acid/base and phosphate-binding residues.
    """
    ligand_sites = _plp_like_sites(atoms)
    protein_sites = _protein_sites(atoms)
    site_summaries = [
        _summarize_plp_site(site_atoms, protein_sites) for site_atoms in ligand_sites
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
        "plp_like_site_count": len(ligand_sites),
        "plp_like_comp_ids_observed": sorted(
            {
                str(summary["site"]["comp_id"])
                for summary in site_summaries
                if summary.get("site", {}).get("comp_id")
            }
        ),
        "selected_site": selected.get("site") if selected else None,
        "status": status,
        "status_reason": _status_reason(status),
        "source_free_coordinate_evidence": True,
        "text_or_label_fields_used_for_predictive_score": False,
        "structure_id": structure_id,
        "residue_count": len(residues),
        "residues": residues,
        "pairwise_distances_angstrom": pairwise_distances(residues),
        "ligand_context": ligand_context,
        "pocket_context": pocket_context,
        "site_candidates": site_summaries[:8],
    }


def _plp_like_sites(atoms: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        code = _comp_id(atom)
        if code not in PLP_LIKE_CODES:
            continue
        by_site[(code, _chain_id(atom), _residue_id(atom))].append(atom)
    return [by_site[key] for key in sorted(by_site)]


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


def _summarize_plp_site(
    ligand_atoms: list[dict[str, Any]],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
) -> dict[str, Any]:
    comp_id = _comp_id(ligand_atoms[0])
    chain_id = _chain_id(ligand_atoms[0])
    residue_id = _residue_id(ligand_atoms[0])
    contacts = _nearest_contacts(ligand_atoms, protein_sites)
    anchor = _plp_anchor_residue(comp_id, chain_id, residue_id, ligand_atoms, contacts)
    acid_base = _nearest_role_residue(
        contacts,
        allowed_codes=ACID_BASE_CODES,
        max_distance=3.4,
        role="acid_base",
        extra_roles=["proton acceptor", "hydrogen bond acceptor"],
    )
    phosphate_binder = _nearest_phosphate_binder(contacts, max_distance=3.5)
    residues = [item for item in [anchor, acid_base, phosphate_binder] if item]
    return {
        "site": {
            "comp_id": comp_id,
            "chain_id": chain_id or None,
            "residue_id": residue_id or None,
            "atom_count": len(ligand_atoms),
        },
        "anchor_detected": anchor is not None,
        "acid_base_residue_detected": acid_base is not None,
        "phosphate_binder_detected": phosphate_binder is not None,
        "resolved_role_count": len(residues),
        "residues": residues,
        "nearest_contacts": contacts[:12],
    }


def _nearest_contacts(
    ligand_atoms: list[dict[str, Any]],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    contacts: list[dict[str, Any]] = []
    phosphate_atoms = _phosphate_ligand_atoms(ligand_atoms)
    for (code, chain, resid), residue_atoms in protein_sites.items():
        candidate_atoms = [
            atom
            for atom in residue_atoms
            if _atom_name(atom) in SIDECHAIN_ATOMS.get(code, set())
        ] or residue_atoms
        distance, ligand_atom, residue_atom = _nearest_atom_pair(
            ligand_atoms,
            candidate_atoms,
        )
        if distance is None or ligand_atom is None or residue_atom is None:
            continue
        if distance > 4.0:
            continue
        contact = {
            "distance_angstrom": round(distance, 3),
            "ligand_atom": _atom_name(ligand_atom),
            "residue_atom": _atom_name(residue_atom),
            "residue_code": code,
            "residue_chain_id": chain or None,
            "residue_id": resid or None,
            "_residue_atoms": residue_atoms,
        }
        phosphate_distance, phosphate_atom, phosphate_residue_atom = _nearest_atom_pair(
            phosphate_atoms,
            candidate_atoms,
        )
        if (
            phosphate_distance is not None
            and phosphate_atom is not None
            and phosphate_residue_atom is not None
        ):
            contact.update(
                {
                    "nearest_phosphate_distance_angstrom": round(phosphate_distance, 3),
                    "nearest_phosphate_ligand_atom": _atom_name(phosphate_atom),
                    "nearest_phosphate_residue_atom": _atom_name(phosphate_residue_atom),
                }
            )
        contacts.append(contact)
    contacts.sort(
        key=lambda item: (
            float(item["distance_angstrom"]),
            str(item["residue_code"]),
            str(item["residue_chain_id"]),
            str(item["residue_id"]),
        )
    )
    return contacts


def _plp_anchor_residue(
    comp_id: str,
    chain_id: str,
    residue_id: str,
    ligand_atoms: list[dict[str, Any]],
    contacts: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if comp_id == "LLP":
        return {
            "residue_node_id": f"{chain_id}:{residue_id}:llp_modified_lysine_anchor",
            "code": "LYS",
            "chain_name": chain_id or None,
            "resid": residue_id or None,
            "atom_count": len(ligand_atoms),
            "centroid": residue_centroid(ligand_atoms),
            "ca": None,
            "roles": [
                "plp_anchor",
                "covalently attached",
                "internal aldimine proxy from LLP comp_id",
            ],
            "source_free_evidence": {
                "evidence_type": "modified_residue_comp_id",
                "comp_id": "LLP",
            },
        }
    for contact in contacts:
        if contact["residue_code"] != "LYS":
            continue
        if contact["residue_atom"] != "NZ":
            continue
        if contact["ligand_atom"] not in PLP_ALDIMINE_ATOMS:
            continue
        if float(contact["distance_angstrom"]) > 2.2:
            continue
        residue_atoms = contact["_residue_atoms"]
        return {
            "residue_node_id": (
                f"{contact['residue_chain_id']}:{contact['residue_id']}:plp_lysine_anchor"
            ),
            "code": "LYS",
            "chain_name": contact["residue_chain_id"],
            "resid": contact["residue_id"],
            "atom_count": len(residue_atoms),
            "centroid": residue_centroid(residue_atoms),
            "ca": atom_position(residue_atoms, "CA"),
            "roles": ["plp_anchor", "covalently attached", "internal aldimine distance"],
            "source_free_evidence": {
                "evidence_type": "plp_aldimine_atom_distance",
                "ligand_atom": contact["ligand_atom"],
                "residue_atom": contact["residue_atom"],
                "distance_angstrom": contact["distance_angstrom"],
            },
        }
    return None


def _nearest_role_residue(
    contacts: list[dict[str, Any]],
    *,
    allowed_codes: set[str],
    max_distance: float,
    role: str,
    extra_roles: list[str],
) -> dict[str, Any] | None:
    for contact in contacts:
        if contact["residue_code"] not in allowed_codes:
            continue
        if float(contact["distance_angstrom"]) > max_distance:
            continue
        residue_atoms = contact["_residue_atoms"]
        return {
            "residue_node_id": (
                f"{contact['residue_chain_id']}:{contact['residue_id']}:{role}"
            ),
            "code": contact["residue_code"],
            "chain_name": contact["residue_chain_id"],
            "resid": contact["residue_id"],
            "atom_count": len(residue_atoms),
            "centroid": residue_centroid(residue_atoms),
            "ca": atom_position(residue_atoms, "CA"),
            "roles": [role, *extra_roles],
            "source_free_evidence": {
                "evidence_type": "nearest_plp_contact",
                "ligand_atom": contact["ligand_atom"],
                "residue_atom": contact["residue_atom"],
                "distance_angstrom": contact["distance_angstrom"],
            },
        }
    return None


def _nearest_phosphate_binder(
    contacts: list[dict[str, Any]],
    *,
    max_distance: float,
) -> dict[str, Any] | None:
    for contact in contacts:
        if contact["residue_code"] not in PHOSPHATE_BINDER_CODES:
            continue
        phosphate_distance = contact.get("nearest_phosphate_distance_angstrom")
        if phosphate_distance is None or float(phosphate_distance) > max_distance:
            continue
        residue_atoms = contact["_residue_atoms"]
        return {
            "residue_node_id": (
                f"{contact['residue_chain_id']}:{contact['residue_id']}:phosphate_binder"
            ),
            "code": contact["residue_code"],
            "chain_name": contact["residue_chain_id"],
            "resid": contact["residue_id"],
            "atom_count": len(residue_atoms),
            "centroid": residue_centroid(residue_atoms),
            "ca": atom_position(residue_atoms, "CA"),
            "roles": ["phosphate_binder", "hydrogen bond donor"],
            "source_free_evidence": {
                "evidence_type": "nearest_plp_phosphate_contact",
                "ligand_atom": contact["nearest_phosphate_ligand_atom"],
                "residue_atom": contact["nearest_phosphate_residue_atom"],
                "distance_angstrom": phosphate_distance,
            },
        }
    return None


def _status_for(selected_site: dict[str, Any] | None) -> str:
    if selected_site is None:
        return "plp_like_cofactor_absent"
    if selected_site.get("anchor_detected") and selected_site.get("resolved_role_count") == 3:
        return "source_free_plp_active_site_ready"
    if selected_site.get("anchor_detected"):
        return "source_free_plp_anchor_partial"
    return "plp_anchor_not_resolved"


def _status_reason(status: str) -> str:
    return {
        "plp_like_cofactor_absent": "no PLP/LLP/PMP/P5P-like coordinate site was observed",
        "source_free_plp_active_site_ready": (
            "coordinate-only PLP-like cofactor, lysine anchor, acid/base residue, "
            "and phosphate-binding residue were resolved"
        ),
        "source_free_plp_anchor_partial": (
            "coordinate-only PLP-like cofactor and lysine anchor were resolved, "
            "but the active-site role triplet is incomplete"
        ),
        "plp_anchor_not_resolved": (
            "PLP-like coordinate site was observed but no covalent/modified lysine "
            "anchor was resolved"
        ),
    }[status]


def _site_sort_key(site: dict[str, Any]) -> tuple[int, int, int, int]:
    return (
        1 if site.get("anchor_detected") else 0,
        int(site.get("resolved_role_count") or 0),
        1 if site.get("site", {}).get("comp_id") == "LLP" else 0,
        int(site.get("site", {}).get("atom_count") or 0),
    )


def _nearest_atom_pair(
    left_atoms: list[dict[str, Any]],
    right_atoms: list[dict[str, Any]],
) -> tuple[float | None, dict[str, Any] | None, dict[str, Any] | None]:
    best_distance: float | None = None
    best_left: dict[str, Any] | None = None
    best_right: dict[str, Any] | None = None
    for left in left_atoms:
        for right in right_atoms:
            distance = _distance(left, right)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_left = left
                best_right = right
    return best_distance, best_left, best_right


def _phosphate_ligand_atoms(ligand_atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [atom for atom in ligand_atoms if "P" in _atom_name(atom).upper()]


def _distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    return math.sqrt(
        (float(left["Cartn_x"]) - float(right["Cartn_x"])) ** 2
        + (float(left["Cartn_y"]) - float(right["Cartn_y"])) ** 2
        + (float(left["Cartn_z"]) - float(right["Cartn_z"])) ** 2
    )


def _comp_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def _chain_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def _residue_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def _atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "")


def strip_internal_contact_fields(value: Any) -> Any:
    """Remove non-serializable atom lists from extractor diagnostics."""
    if isinstance(value, list):
        return [strip_internal_contact_fields(item) for item in value]
    if isinstance(value, dict):
        return {
            key: strip_internal_contact_fields(item)
            for key, item in value.items()
            if key != "_residue_atoms"
        }
    return value
