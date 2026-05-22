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
HEME_LIGAND_CODES = {"HEM", "HEA", "HEB", "HEC", "HEO"}
FLAVIN_LIGAND_CODES = {"FAD", "FMN", "RBF"}
IGNORED_LIGAND_CODES = {"HOH", "WAT", "DOD", "SOL", "MSE"}

HEME_LIGAND_RESIDUES = {"HIS", "CYS", "TYR", "MET"}
HEME_ACID_BASE_RESIDUES = {"HIS", "ARG", "ASP"}
HEME_ELECTRON_PATH_RESIDUES = {"PHE", "TYR", "TRP", "HIS", "CYS"}

FLAVIN_BINDER_RESIDUES = {
    "ARG",
    "LYS",
    "HIS",
    "ASN",
    "GLN",
    "SER",
    "THR",
    "TYR",
    "CYS",
    "GLY",
}
FLAVIN_REDOX_RESIDUES = {"HIS", "GLU", "CYS", "TYR", "ARG"}
FLAVIN_ELECTRON_PATH_RESIDUES = {"PHE", "TYR", "TRP", "HIS", "CYS"}

HEME_IRON_COORDINATION_CUTOFF_ANGSTROM = 3.2
HEME_CONTACT_CUTOFF_ANGSTROM = 4.8
FLAVIN_CONTACT_CUTOFF_ANGSTROM = 4.2
FLAVIN_REDOX_CONTACT_CUTOFF_ANGSTROM = 5.0


def extract_source_free_heme_site(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract a heme redox active-site proxy from coordinates only."""
    return _extract_redox_site(
        atoms,
        ligand_codes=HEME_LIGAND_CODES,
        role_specs=[
            _RoleSpec(
                role="heme_ligand",
                allowed_residues=HEME_LIGAND_RESIDUES,
                cutoff=HEME_IRON_COORDINATION_CUTOFF_ANGSTROM,
                prefer_ligand_atoms={"FE"},
                fallback_cutoff=HEME_CONTACT_CUTOFF_ANGSTROM,
            ),
            _RoleSpec(
                role="acid_base",
                allowed_residues=HEME_ACID_BASE_RESIDUES,
                cutoff=HEME_CONTACT_CUTOFF_ANGSTROM,
            ),
            _RoleSpec(
                role="electron_transfer_path",
                allowed_residues=HEME_ELECTRON_PATH_RESIDUES,
                cutoff=HEME_CONTACT_CUTOFF_ANGSTROM,
            ),
        ],
        resolved_status="source_free_heme_active_site_resolved",
        unresolved_status="no_source_free_heme_active_site",
        status_reason_resolved=(
            "Heme ligand, acid/base, and electron-transfer residues are resolved "
            "from coordinate contacts only"
        ),
        status_reason_unresolved=(
            "No coordinate heme site met the ligand, acid/base, and electron-transfer "
            "contact requirements"
        ),
        row_id=row_id,
        accession=accession,
        structure_id=structure_id,
        residue_node_suffix="source_free_heme_site",
    )


def extract_source_free_flavin_site(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract a flavin redox active-site proxy from coordinates only."""
    return _extract_redox_site(
        atoms,
        ligand_codes=FLAVIN_LIGAND_CODES,
        role_specs=[
            _RoleSpec(
                role="flavin_binder",
                allowed_residues=FLAVIN_BINDER_RESIDUES,
                cutoff=FLAVIN_CONTACT_CUTOFF_ANGSTROM,
            ),
            _RoleSpec(
                role="redox_acid_base",
                allowed_residues=FLAVIN_REDOX_RESIDUES,
                cutoff=FLAVIN_REDOX_CONTACT_CUTOFF_ANGSTROM,
            ),
            _RoleSpec(
                role="electron_transfer_path",
                allowed_residues=FLAVIN_ELECTRON_PATH_RESIDUES,
                cutoff=FLAVIN_REDOX_CONTACT_CUTOFF_ANGSTROM,
            ),
        ],
        resolved_status="source_free_flavin_redox_site_resolved",
        unresolved_status="no_source_free_flavin_redox_site",
        status_reason_resolved=(
            "Flavin binder, redox acid/base, and electron-transfer residues are "
            "resolved from coordinate contacts only"
        ),
        status_reason_unresolved=(
            "No coordinate flavin site met the binder, redox acid/base, and "
            "electron-transfer contact requirements"
        ),
        row_id=row_id,
        accession=accession,
        structure_id=structure_id,
        residue_node_suffix="source_free_flavin_site",
    )


class _RoleSpec:
    def __init__(
        self,
        *,
        role: str,
        allowed_residues: set[str],
        cutoff: float,
        prefer_ligand_atoms: set[str] | None = None,
        fallback_cutoff: float | None = None,
    ) -> None:
        self.role = role
        self.allowed_residues = allowed_residues
        self.cutoff = cutoff
        self.prefer_ligand_atoms = prefer_ligand_atoms or set()
        self.fallback_cutoff = fallback_cutoff


def _extract_redox_site(
    atoms: list[dict[str, Any]],
    *,
    ligand_codes: set[str],
    role_specs: list[_RoleSpec],
    resolved_status: str,
    unresolved_status: str,
    status_reason_resolved: str,
    status_reason_unresolved: str,
    row_id: str | None,
    accession: str | None,
    structure_id: str | None,
    residue_node_suffix: str,
) -> dict[str, Any]:
    protein_sites = _protein_sites(atoms)
    ligand_sites = [
        site for site in _ligand_sites(atoms) if site["code"] in ligand_codes
    ]
    candidates = [
        _site_candidate(
            site,
            protein_sites,
            role_specs=role_specs,
            residue_node_suffix=residue_node_suffix,
        )
        for site in ligand_sites
    ]
    candidates.sort(key=_candidate_sort_key)
    selected = candidates[0] if candidates else None
    residues = list(selected.get("residues", [])) if selected else []
    ligand_context = ligand_context_from_atoms(atoms, residues) if residues else {}
    pocket_context = pocket_context_from_atoms(atoms, residues) if residues else {}
    role_counts = {
        spec.role: sum(1 for residue in residues if spec.role in residue["roles"])
        for spec in role_specs
    }
    resolved = bool(selected) and all(count > 0 for count in role_counts.values())
    status = resolved_status if resolved else unresolved_status
    return {
        "accession": accession,
        "entry_id": row_id or (f"uniprot:{accession}" if accession else None),
        "status": status,
        "status_reason": status_reason_resolved if resolved else status_reason_unresolved,
        "structure_id": structure_id,
        "selected_ligand": _public_ligand_site(selected),
        "target_ligand_site_count": len(ligand_sites),
        "source_free_coordinate_evidence": True,
        "text_or_label_fields_used_for_predictive_score": False,
        "predictive_input_policy": (
            "Only mmCIF atom coordinates, residue/ligand comp ids, atom names, "
            "and interatomic distances are used; EC, names, UniProt prose, and "
            "curated labels are excluded."
        ),
        "resolved_residue_count": len(residues),
        "residue_count": len(residues),
        "role_contact_counts": role_counts,
        "residues": residues,
        "pairwise_distances_angstrom": pairwise_distances(residues),
        "ligand_context": ligand_context,
        "pocket_context": pocket_context,
        "site_candidates": [_public_site_candidate(candidate) for candidate in candidates[:8]],
    }


def _site_candidate(
    ligand_site: dict[str, Any],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
    *,
    role_specs: list[_RoleSpec],
    residue_node_suffix: str,
) -> dict[str, Any]:
    residues_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    role_contacts: dict[str, list[dict[str, Any]]] = {}
    ligand_atoms = list(ligand_site["atoms"])
    for spec in role_specs:
        contacts = _role_contacts(ligand_atoms, protein_sites, spec)
        role_contacts[spec.role] = contacts
        for contact in contacts:
            key = (
                str(contact["residue_code"]),
                str(contact["residue_chain_id"] or ""),
                str(contact["residue_id"] or ""),
            )
            residue = residues_by_key.get(key)
            if residue is None:
                residue = _residue_from_contact(
                    contact,
                    role=spec.role,
                    residue_node_suffix=residue_node_suffix,
                )
                residues_by_key[key] = residue
            elif spec.role not in residue["roles"]:
                residue["roles"].append(spec.role)
                residue["source_free_evidence"][spec.role] = _public_contact(contact)
    residues = sorted(
        residues_by_key.values(),
        key=lambda residue: (
            str(residue.get("chain_name") or ""),
            _natural_residue_number(residue.get("resid")),
            str(residue.get("code") or ""),
        ),
    )
    complete_role_count = sum(1 for contacts in role_contacts.values() if contacts)
    best_contact_distance_sum = sum(
        float(contacts[0]["distance_angstrom"])
        for contacts in role_contacts.values()
        if contacts
    )
    return {
        "ligand_site": {
            "code": ligand_site["code"],
            "chain_id": ligand_site["chain_id"] or None,
            "residue_id": ligand_site["residue_id"] or None,
            "atom_count": len(ligand_atoms),
        },
        "complete_role_count": complete_role_count,
        "best_contact_distance_sum": round(best_contact_distance_sum, 3),
        "role_contact_counts": {
            role: len(contacts) for role, contacts in role_contacts.items()
        },
        "role_contacts": {
            role: [_public_contact(contact) for contact in contacts[:8]]
            for role, contacts in role_contacts.items()
        },
        "residues": residues,
    }


def _role_contacts(
    ligand_atoms: list[dict[str, Any]],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
    spec: _RoleSpec,
) -> list[dict[str, Any]]:
    contacts = _contacts_for_cutoff(
        ligand_atoms=_preferred_ligand_atoms(ligand_atoms, spec.prefer_ligand_atoms),
        protein_sites=protein_sites,
        allowed_residues=spec.allowed_residues,
        cutoff=spec.cutoff,
    )
    if contacts or spec.fallback_cutoff is None:
        return contacts
    return _contacts_for_cutoff(
        ligand_atoms=ligand_atoms,
        protein_sites=protein_sites,
        allowed_residues=spec.allowed_residues,
        cutoff=spec.fallback_cutoff,
    )


def _contacts_for_cutoff(
    *,
    ligand_atoms: list[dict[str, Any]],
    protein_sites: dict[tuple[str, str, str], list[dict[str, Any]]],
    allowed_residues: set[str],
    cutoff: float,
) -> list[dict[str, Any]]:
    contacts: list[dict[str, Any]] = []
    for (code, chain_id, residue_id), residue_atoms in protein_sites.items():
        if code not in allowed_residues:
            continue
        nearest = _nearest_atom_pair(ligand_atoms, residue_atoms)
        if nearest is None:
            continue
        distance, ligand_atom, residue_atom = nearest
        if distance > cutoff:
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


def _ligand_sites(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") != "HETATM":
            continue
        code = _comp_id(atom)
        if not code or code in IGNORED_LIGAND_CODES:
            continue
        by_site[(code, _chain_id(atom), _residue_id(atom))].append(atom)
    return [
        {"code": code, "chain_id": chain_id, "residue_id": residue_id, "atoms": site_atoms}
        for (code, chain_id, residue_id), site_atoms in sorted(by_site.items())
    ]


def _preferred_ligand_atoms(
    ligand_atoms: list[dict[str, Any]],
    preferred_names: set[str],
) -> list[dict[str, Any]]:
    if not preferred_names:
        return ligand_atoms
    preferred = [
        atom
        for atom in ligand_atoms
        if _atom_name(atom) in preferred_names
        or str(atom.get("type_symbol") or "").upper() in preferred_names
    ]
    return preferred or ligand_atoms


def _nearest_atom_pair(
    left_atoms: list[dict[str, Any]],
    right_atoms: list[dict[str, Any]],
) -> tuple[float, dict[str, Any], dict[str, Any]] | None:
    best: tuple[float, dict[str, Any], dict[str, Any]] | None = None
    for left_atom in left_atoms:
        left_pos = _atom_coordinate_tuple(left_atom)
        if left_pos is None:
            continue
        for right_atom in right_atoms:
            right_pos = _atom_coordinate_tuple(right_atom)
            if right_pos is None:
                continue
            distance = math.dist(left_pos, right_pos)
            if best is None or distance < best[0]:
                best = (distance, left_atom, right_atom)
    return best


def _residue_from_contact(
    contact: dict[str, Any],
    *,
    role: str,
    residue_node_suffix: str,
) -> dict[str, Any]:
    residue_atoms = list(contact.get("_residue_atoms", []))
    chain_id = contact.get("residue_chain_id")
    residue_id = contact.get("residue_id")
    code = str(contact.get("residue_code") or "")
    return {
        "residue_node_id": f"{chain_id}:{residue_id}:{residue_node_suffix}",
        "code": code,
        "chain_name": chain_id,
        "resid": residue_id,
        "atom_count": len(residue_atoms),
        "centroid": residue_centroid(residue_atoms),
        "ca": atom_position(residue_atoms, "CA"),
        "roles": [role],
        "source_free_evidence": {role: _public_contact(contact)},
    }


def _public_contact(contact: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_type": "ligand_residue_coordinate_contact",
        "ligand_comp_id": contact.get("ligand_comp_id"),
        "ligand_chain_id": contact.get("ligand_chain_id"),
        "ligand_residue_id": contact.get("ligand_residue_id"),
        "ligand_atom": contact.get("ligand_atom"),
        "distance_angstrom": contact.get("distance_angstrom"),
        "residue_atom": contact.get("residue_atom"),
    }


def _public_ligand_site(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    if candidate is None:
        return None
    return dict(candidate.get("ligand_site") or {})


def _public_site_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "ligand_site": candidate.get("ligand_site"),
        "complete_role_count": candidate.get("complete_role_count"),
        "best_contact_distance_sum": candidate.get("best_contact_distance_sum"),
        "role_contact_counts": candidate.get("role_contact_counts"),
        "role_contacts": candidate.get("role_contacts"),
    }


def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[int, float, str, str]:
    return (
        -int(candidate.get("complete_role_count") or 0),
        float(candidate.get("best_contact_distance_sum") or 999.0),
        str((candidate.get("ligand_site") or {}).get("chain_id") or ""),
        str((candidate.get("ligand_site") or {}).get("residue_id") or ""),
    )


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


def _natural_residue_number(value: Any) -> tuple[int, str]:
    text = str(value or "")
    digits = "".join(char for char in text if char.isdigit() or char == "-")
    try:
        return (int(digits), text)
    except ValueError:
        return (10**9, text)
