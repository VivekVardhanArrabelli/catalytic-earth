from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import Any

from .structure import pairwise_distances, residue_centroid


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
ONE_LETTER = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}
NAD_P_LIKE_CODES = {"NAD", "NADH", "NADP", "NAP", "NPH"}
CATALYTIC_TYR_LYS_DISTANCE_CUTOFF_ANGSTROM = 7.0
NAD_P_TO_AXIS_DISTANCE_CUTOFF_ANGSTROM = 8.0


def extract_source_free_sdr_catalytic_axis(
    atoms: list[dict[str, Any]],
    *,
    row_id: str | None = None,
    accession: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    """Extract a review-only SDR catalytic-axis probe from structure atoms.

    The probe intentionally uses a narrow, preregisterable source-free rule:
    scan the coordinate sequence for Tyr-X-X-X-Lys motifs, then require the
    Tyr OH and Lys NZ side-chain atoms to be locally resolved. NAD(P)-like
    ligand support is accepted only from coordinate ligand records.
    """

    chains = _protein_chains(atoms)
    candidates: list[dict[str, Any]] = []
    for chain_id, residues in chains.items():
        candidates.extend(_chain_yxxxk_candidates(chain_id, residues))
    candidates.sort(key=_candidate_sort_key)

    nad_sites = _nad_p_like_sites(atoms)
    selected = candidates[0] if candidates else None
    nearest_nad_context = (
        _nearest_nad_p_context(selected, nad_sites) if selected is not None else None
    )
    residues = list(selected.get("residues", [])) if selected else []
    status = _status_for(selected, nearest_nad_context)

    return {
        "accession": accession,
        "entry_id": row_id or (f"uniprot:{accession}" if accession else None),
        "structure_id": structure_id,
        "status": status,
        "status_reason": _status_reason(status),
        "source_free_coordinate_evidence": True,
        "text_or_label_fields_used_for_predictive_score": False,
        "source_active_site_annotations_used": False,
        "sequence_motif_rule": "Tyr-X-X-X-Lys candidate scan, frozen before scoring",
        "predictive_input_policy": (
            "Only mmCIF atom coordinates, residue/ligand comp ids, atom names, "
            "sequence order from coordinates, and distances are used; EC, names, "
            "UniProt prose, source active-site annotations, and curated labels are "
            "excluded."
        ),
        "catalytic_tyr_lys_distance_cutoff_angstrom": (
            CATALYTIC_TYR_LYS_DISTANCE_CUTOFF_ANGSTROM
        ),
        "nad_p_to_axis_distance_cutoff_angstrom": NAD_P_TO_AXIS_DISTANCE_CUTOFF_ANGSTROM,
        "yxxxk_candidate_count": len(candidates),
        "source_free_catalytic_axis_resolved": bool(
            selected and selected["source_free_catalytic_axis_resolved"]
        ),
        "nad_p_like_ligand_site_count": len(nad_sites),
        "source_free_full_sdr_axis_ready": status
        == "source_free_sdr_catalytic_and_nad_p_site_resolved",
        "selected_candidate": _public_candidate(selected, nearest_nad_context),
        "residue_count": len(residues),
        "residues": [_clean_residue(residue) for residue in residues],
        "pairwise_distances_angstrom": pairwise_distances(residues),
        "candidate_summaries": [
            _public_candidate(candidate, _nearest_nad_p_context(candidate, nad_sites))
            for candidate in candidates[:8]
        ],
        "nad_p_like_sites": [_public_ligand_site(site) for site in nad_sites[:8]],
    }


def _protein_chains(
    atoms: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    residues_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        code = _comp_id(atom)
        if code not in STANDARD_AMINO_ACIDS:
            continue
        chain = _chain_id(atom)
        resid = _residue_id(atom)
        key = (chain, resid)
        residue = residues_by_key.get(key)
        if residue is None:
            residue = {
                "code": code,
                "chain_name": chain or None,
                "resid": resid or None,
                "atoms": [],
            }
            residues_by_key[key] = residue
        residue["atoms"].append(atom)

    chains: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for residue in residues_by_key.values():
        chains[str(residue.get("chain_name") or "")].append(residue)
    for chain_id in list(chains):
        chains[chain_id].sort(key=lambda residue: _residue_sort_key(residue["resid"]))
    return dict(chains)


def _chain_yxxxk_candidates(
    chain_id: str,
    residues: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    sequence = "".join(ONE_LETTER.get(str(residue["code"]), "X") for residue in residues)
    for index in range(max(0, len(residues) - 4)):
        tyr = residues[index]
        lys = residues[index + 4]
        if tyr["code"] != "TYR" or lys["code"] != "LYS":
            continue
        tyr_atom = _first_atom(tyr["atoms"], {"OH"})
        lys_atom = _first_atom(lys["atoms"], {"NZ"})
        tyr_lys_distance = _atom_distance(tyr_atom, lys_atom)
        geometry_resolved = (
            tyr_lys_distance is not None
            and tyr_lys_distance <= CATALYTIC_TYR_LYS_DISTANCE_CUTOFF_ANGSTROM
        )
        residues_for_candidate = [
            _residue_record(
                tyr,
                roles=["sdr_catalytic_tyr"],
                evidence_atom="OH",
                distance=tyr_lys_distance,
            ),
            _residue_record(
                lys,
                roles=["sdr_catalytic_lys"],
                evidence_atom="NZ",
                distance=tyr_lys_distance,
            ),
        ]
        candidates.append(
            {
                "chain_id": chain_id or None,
                "motif": sequence[index : index + 5],
                "sequence_index_start": index + 1,
                "tyr_resid": tyr["resid"],
                "lys_resid": lys["resid"],
                "tyr_lys_distance_angstrom": (
                    round(tyr_lys_distance, 3)
                    if tyr_lys_distance is not None
                    else None
                ),
                "source_free_catalytic_axis_resolved": geometry_resolved,
                "residues": residues_for_candidate,
            }
        )
    return candidates


def _nad_p_like_sites(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") not in {"HETATM", "ATOM"}:
            continue
        code = _comp_id(atom)
        if code not in NAD_P_LIKE_CODES:
            continue
        by_site[(code, _chain_id(atom), _residue_id(atom))].append(atom)
    sites = [
        {
            "code": code,
            "chain_id": chain or None,
            "residue_id": resid or None,
            "atom_count": len(site_atoms),
            "atoms": site_atoms,
            "centroid": residue_centroid(site_atoms),
        }
        for (code, chain, resid), site_atoms in sorted(by_site.items())
    ]
    return sites


def _nearest_nad_p_context(
    candidate: dict[str, Any] | None,
    nad_sites: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if candidate is None or not nad_sites:
        return None
    residue_atoms = [
        atom
        for residue in candidate.get("residues", [])
        for atom in residue.get("_atoms", [])
    ]
    if not residue_atoms:
        return None
    best: tuple[float, dict[str, Any]] | None = None
    for site in nad_sites:
        distance = _nearest_distance(residue_atoms, site["atoms"])
        if distance is None:
            continue
        if best is None or distance < best[0]:
            best = (distance, site)
    if best is None:
        return None
    distance, site = best
    return {
        "code": site["code"],
        "chain_id": site["chain_id"],
        "residue_id": site["residue_id"],
        "atom_count": site["atom_count"],
        "nearest_axis_distance_angstrom": round(distance, 3),
        "within_cutoff": distance <= NAD_P_TO_AXIS_DISTANCE_CUTOFF_ANGSTROM,
    }


def _status_for(
    selected: dict[str, Any] | None,
    nearest_nad_context: dict[str, Any] | None,
) -> str:
    if selected is None:
        return "no_source_free_sdr_catalytic_axis"
    if not selected["source_free_catalytic_axis_resolved"]:
        return "source_free_sdr_catalytic_motif_unresolved_geometry"
    if nearest_nad_context is None:
        return "source_free_sdr_catalytic_axis_without_nad_p_ligand"
    if nearest_nad_context["within_cutoff"]:
        return "source_free_sdr_catalytic_and_nad_p_site_resolved"
    return "source_free_sdr_catalytic_axis_with_distant_nad_p_ligand"


def _status_reason(status: str) -> str:
    return {
        "no_source_free_sdr_catalytic_axis": (
            "No coordinate-sequence Tyr-X-X-X-Lys candidate was found."
        ),
        "source_free_sdr_catalytic_motif_unresolved_geometry": (
            "A Tyr-X-X-X-Lys sequence candidate exists, but the Tyr OH to Lys NZ "
            "coordinate geometry is missing or outside the frozen cutoff."
        ),
        "source_free_sdr_catalytic_axis_without_nad_p_ligand": (
            "The Tyr-X-X-X-Lys catalytic-axis geometry is coordinate-resolved, "
            "but no NAD(P)-like ligand site is present in the structure."
        ),
        "source_free_sdr_catalytic_axis_with_distant_nad_p_ligand": (
            "The catalytic-axis geometry and an NAD(P)-like ligand are present, "
            "but the ligand is outside the frozen local-axis cutoff."
        ),
        "source_free_sdr_catalytic_and_nad_p_site_resolved": (
            "The catalytic Tyr/Lys axis and a local NAD(P)-like ligand site are "
            "resolved from coordinates."
        ),
    }[status]


def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[int, float, str, str]:
    resolved_penalty = 0 if candidate["source_free_catalytic_axis_resolved"] else 1
    distance = candidate["tyr_lys_distance_angstrom"]
    return (
        resolved_penalty,
        float(distance) if distance is not None else 999.0,
        str(candidate.get("chain_id") or ""),
        str(candidate.get("tyr_resid") or ""),
    )


def _public_candidate(
    candidate: dict[str, Any] | None,
    nearest_nad_context: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if candidate is None:
        return None
    return {
        "chain_id": candidate["chain_id"],
        "motif": candidate["motif"],
        "sequence_index_start": candidate["sequence_index_start"],
        "tyr_resid": candidate["tyr_resid"],
        "lys_resid": candidate["lys_resid"],
        "tyr_lys_distance_angstrom": candidate["tyr_lys_distance_angstrom"],
        "source_free_catalytic_axis_resolved": candidate[
            "source_free_catalytic_axis_resolved"
        ],
        "nearest_nad_p_like_ligand": nearest_nad_context,
    }


def _public_ligand_site(site: dict[str, Any]) -> dict[str, Any]:
    return {
        "code": site["code"],
        "chain_id": site["chain_id"],
        "residue_id": site["residue_id"],
        "atom_count": site["atom_count"],
        "centroid": site["centroid"],
    }


def _clean_residue(residue: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in residue.items() if key != "_atoms"}


def _residue_record(
    residue: dict[str, Any],
    *,
    roles: list[str],
    evidence_atom: str,
    distance: float | None,
) -> dict[str, Any]:
    return {
        "residue_node_id": (
            f"{residue.get('chain_name') or ''}:{residue.get('resid') or ''}:"
            f"{residue['code']}:sdr_source_free_axis"
        ),
        "code": residue["code"],
        "chain_name": residue.get("chain_name"),
        "resid": residue.get("resid"),
        "atom_count": len(residue["atoms"]),
        "centroid": residue_centroid(residue["atoms"]),
        "ca": _atom_point(_first_atom(residue["atoms"], {"CA"})),
        "roles": roles,
        "source_free_evidence": {
            "evidence_type": "coordinate_sequence_yxxxk_geometry",
            "evidence_atom": evidence_atom,
            "tyr_lys_distance_angstrom": round(distance, 3)
            if distance is not None
            else None,
        },
        "_atoms": residue["atoms"],
    }


def _first_atom(
    atoms: list[dict[str, Any]],
    atom_names: set[str],
) -> dict[str, Any] | None:
    for atom in atoms:
        if _atom_name(atom) in atom_names:
            return atom
    return None


def _nearest_distance(
    left_atoms: list[dict[str, Any]],
    right_atoms: list[dict[str, Any]],
) -> float | None:
    best: float | None = None
    for left in left_atoms:
        for right in right_atoms:
            distance = _atom_distance(left, right)
            if distance is None:
                continue
            if best is None or distance < best:
                best = distance
    return best


def _atom_distance(
    left: dict[str, Any] | None,
    right: dict[str, Any] | None,
) -> float | None:
    left_coord = _atom_coordinate(left)
    right_coord = _atom_coordinate(right)
    if left_coord is None or right_coord is None:
        return None
    return math.dist(left_coord, right_coord)


def _atom_coordinate(atom: dict[str, Any] | None) -> list[float] | None:
    if atom is None:
        return None
    try:
        return [
            float(atom["Cartn_x"]),
            float(atom["Cartn_y"]),
            float(atom["Cartn_z"]),
        ]
    except (KeyError, TypeError, ValueError):
        return None


def _atom_point(atom: dict[str, Any] | None) -> dict[str, float] | None:
    coordinate = _atom_coordinate(atom)
    if coordinate is None:
        return None
    return {
        "x": round(coordinate[0], 3),
        "y": round(coordinate[1], 3),
        "z": round(coordinate[2], 3),
    }


def _comp_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def _chain_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def _residue_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def _atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper()


def _residue_sort_key(resid: Any) -> tuple[int, str]:
    text = str(resid or "")
    match = re.search(r"-?\d+", text)
    return (int(match.group()) if match else 10**9, text)
