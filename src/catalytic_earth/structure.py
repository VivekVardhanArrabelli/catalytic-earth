from __future__ import annotations

import math
import shlex
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from .graph import summarize_graph
from .v2 import load_graph


PDB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"
USER_AGENT = "CatalyticEarth/0.0.1 research prototype"
LIGAND_DISTANCE_CUTOFF_ANGSTROM = 6.0
POCKET_DISTANCE_CUTOFF_ANGSTROM = 8.0
IGNORED_LIGAND_CODES = {"HOH", "WAT", "DOD", "SOL"}
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
HYDROPHOBIC_RESIDUES = {"ALA", "VAL", "ILE", "LEU", "MET", "PRO"}
POLAR_RESIDUES = {"SER", "THR", "ASN", "GLN", "CYS", "HIS"}
POSITIVE_RESIDUES = {"LYS", "ARG", "HIS"}
NEGATIVE_RESIDUES = {"ASP", "GLU"}
AROMATIC_RESIDUES = {"PHE", "TYR", "TRP", "HIS"}
SULFUR_RESIDUES = {"CYS", "MET"}
COFACTOR_LIGAND_MAP = {
    "HEM": "heme",
    "HEA": "heme",
    "HEB": "heme",
    "HEC": "heme",
    "HEO": "heme",
    "FAD": "flavin",
    "FMN": "flavin",
    "RBF": "flavin",
    "NAD": "nad",
    "NADH": "nad",
    "NADP": "nad",
    "NAP": "nad",
    "NPH": "nad",
    "PLP": "plp",
    "PLV": "plp",
    "PDD": "plp",
    "5PA": "plp",
    "PMP": "plp",
    "LLP": "plp",
    "SAM": "sam",
    "SAH": "sam",
    "MTA": "sam",
    "B12": "cobalamin",
    "CNC": "cobalamin",
    "COB": "cobalamin",
    "FES": "fe_s_cluster",
    "SF4": "fe_s_cluster",
    "FS4": "fe_s_cluster",
}
METAL_ION_CODES = {
    "ZN",
    "MG",
    "MN",
    "FE",
    "CU",
    "CO",
    "NI",
    "CA",
    "CD",
}


def fetch_pdb_cif(pdb_id: str, timeout: int = 30) -> str:
    cleaned = pdb_id.strip().upper()
    if not cleaned:
        raise ValueError("pdb_id is required")
    request = Request(PDB_CIF_URL.format(pdb_id=cleaned), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_atom_site_loop(cif_text: str) -> list[dict[str, Any]]:
    lines = cif_text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue

        index += 1
        headers: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("_"):
            header = lines[index].strip()
            headers.append(header)
            index += 1

        if not headers or not all(header.startswith("_atom_site.") for header in headers):
            continue

        rows: list[dict[str, Any]] = []
        while index < len(lines):
            line = lines[index].strip()
            if not line or line == "#":
                break
            if line == "loop_" or line.startswith("_") or line.startswith("data_"):
                break
            values = shlex.split(line)
            if len(values) >= len(headers):
                rows.append(_atom_row(headers, values))
            index += 1
        return rows

    return []


def build_geometry_features(
    graph: dict[str, Any],
    max_entries: int = 20,
    cif_fetcher=fetch_pdb_cif,
) -> dict[str, Any]:
    if max_entries < 1:
        raise ValueError("max_entries must be positive")

    nodes = graph.get("nodes", [])
    entry_context_by_id = _entry_context_by_id(nodes)
    residue_nodes = [node for node in nodes if node.get("type") == "catalytic_residue"]
    residues_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in residue_nodes:
        entry_id = _entry_id_from_residue_node(node.get("id", ""))
        if entry_id:
            residues_by_entry[entry_id].append(node)

    cif_cache: dict[str, list[dict[str, Any]]] = {}
    entry_features: list[dict[str, Any]] = []

    for entry_id in sorted(residues_by_entry, key=_entry_sort_key)[:max_entries]:
        residues = residues_by_entry[entry_id]
        positions_by_pdb = _positions_by_pdb(residues)
        if not positions_by_pdb:
            entry_features.append(
                {
                    "entry_id": entry_id,
                    **entry_context_by_id.get(entry_id, {}),
                    "status": "no_structure_positions",
                    "residue_count": len(residues),
                    "pdb_id": None,
                    "residues": [],
                    "pairwise_distances_angstrom": [],
                    "missing_positions": len(residues),
                    "ligand_context": {
                        "distance_cutoff_angstrom": LIGAND_DISTANCE_CUTOFF_ANGSTROM,
                        "proximal_ligands": [],
                        "ligand_codes": [],
                        "cofactor_families": [],
                        "structure_ligands": [],
                        "structure_ligand_codes": [],
                        "structure_cofactor_families": [],
                    },
                    "pocket_context": _empty_pocket_context(),
                }
            )
            continue

        pdb_id = sorted(positions_by_pdb, key=lambda item: (-len(positions_by_pdb[item]), item))[0]
        try:
            if pdb_id not in cif_cache:
                cif_cache[pdb_id] = parse_atom_site_loop(cif_fetcher(pdb_id))
            atoms = cif_cache[pdb_id]
        except Exception as exc:  # network/source errors should become artifact evidence
            entry_features.append(
                {
                    "entry_id": entry_id,
                    **entry_context_by_id.get(entry_id, {}),
                    "status": "structure_fetch_failed",
                    "pdb_id": pdb_id,
                    "error": str(exc),
                    "residue_count": len(residues),
                    "residues": [],
                    "pairwise_distances_angstrom": [],
                    "missing_positions": len(positions_by_pdb[pdb_id]),
                    "ligand_context": {
                        "distance_cutoff_angstrom": LIGAND_DISTANCE_CUTOFF_ANGSTROM,
                        "proximal_ligands": [],
                        "ligand_codes": [],
                        "cofactor_families": [],
                        "structure_ligands": [],
                        "structure_ligand_codes": [],
                        "structure_cofactor_families": [],
                    },
                    "pocket_context": _empty_pocket_context(),
                }
            )
            continue

        resolved: list[dict[str, Any]] = []
        missing_details: list[dict[str, Any]] = []
        missing = 0
        for item in positions_by_pdb[pdb_id]:
            residue_atoms = select_residue_atoms(
                atoms,
                chain_name=item.get("chain_name"),
                resid=item.get("resid"),
                code=item.get("code"),
            )
            if not residue_atoms:
                missing += 1
                missing_details.append(missing_position_detail(atoms, item))
                continue
            centroid = residue_centroid(residue_atoms)
            ca = atom_position(residue_atoms, "CA")
            resolved.append(
                {
                    "residue_node_id": item.get("residue_node_id"),
                    "code": item.get("code"),
                    "chain_name": item.get("chain_name"),
                    "resid": item.get("resid"),
                    "atom_count": len(residue_atoms),
                    "centroid": centroid,
                    "ca": ca,
                    "roles": item.get("roles", []),
                }
            )

        entry_features.append(
            {
                "entry_id": entry_id,
                **entry_context_by_id.get(entry_id, {}),
                "status": "ok" if len(resolved) >= 2 else "insufficient_resolved_residues",
                "pdb_id": pdb_id,
                "residue_count": len(residues),
                "resolved_residue_count": len(resolved),
                "missing_positions": missing,
                "missing_position_details": missing_details,
                "residues": resolved,
                "pairwise_distances_angstrom": pairwise_distances(resolved),
                "ligand_context": ligand_context_from_atoms(atoms, resolved),
                "pocket_context": pocket_context_from_atoms(atoms, resolved),
            }
        )

    return {
        "metadata": {
            "artifact": "active_site_geometry_features",
            "input_graph": summarize_graph(graph),
            "max_entries": max_entries,
            "entry_count": len(entry_features),
            "entries_with_pairwise_geometry": sum(
                1 for entry in entry_features if entry.get("pairwise_distances_angstrom")
            ),
            "entries_with_proximal_ligands": sum(
                1
                for entry in entry_features
                if entry.get("ligand_context", {}).get("proximal_ligands")
            ),
            "entries_with_inferred_cofactors": sum(
                1
                for entry in entry_features
                if entry.get("ligand_context", {}).get("cofactor_families")
            ),
            "entries_with_structure_ligands": sum(
                1
                for entry in entry_features
                if entry.get("ligand_context", {}).get("structure_ligands")
            ),
            "entries_with_structure_inferred_cofactors": sum(
                1
                for entry in entry_features
                if entry.get("ligand_context", {}).get("structure_cofactor_families")
            ),
            "entries_with_pocket_context": sum(
                1
                for entry in entry_features
                if entry.get("pocket_context", {}).get("nearby_residue_count", 0) > 0
            ),
            "source": "RCSB PDB mmCIF files via catalytic residue positions from M-CSA",
        },
        "entries": entry_features,
    }


def write_geometry_features(
    graph_path: Path,
    out_path: Path,
    max_entries: int = 20,
) -> dict[str, Any]:
    features = build_geometry_features(load_graph(graph_path), max_entries=max_entries)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(_json_dumps(features), encoding="utf-8")
    return features


def select_residue_atoms(
    atoms: list[dict[str, Any]],
    chain_name: Any,
    resid: Any,
    code: Any = None,
) -> list[dict[str, Any]]:
    chain = str(chain_name) if chain_name is not None else None
    residue_id = str(resid) if resid is not None else None
    residue_code = str(code).upper() if code is not None else None
    selected: list[dict[str, Any]] = []
    for atom in atoms:
        atom_code = (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if not _atom_matches_position(atom, chain, residue_id):
            continue
        if residue_code and atom_code and atom_code != residue_code:
            continue
        if atom.get("group_PDB") != "ATOM":
            continue
        selected.append(atom)
    return selected


def missing_position_detail(atoms: list[dict[str, Any]], item: dict[str, Any]) -> dict[str, Any]:
    chain = str(item.get("chain_name")) if item.get("chain_name") is not None else None
    residue_id = str(item.get("resid")) if item.get("resid") is not None else None
    observed_codes = sorted(
        {
            (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
            for atom in atoms
            if atom.get("group_PDB") == "ATOM"
            and _atom_matches_position(atom, chain, residue_id)
        }
    )
    return {
        "residue_node_id": item.get("residue_node_id"),
        "chain_name": item.get("chain_name"),
        "resid": item.get("resid"),
        "expected_code": item.get("code"),
        "observed_codes_at_position": observed_codes,
    }


def residue_centroid(atoms: list[dict[str, Any]]) -> dict[str, float]:
    if not atoms:
        raise ValueError("atoms are required")
    coords = [_coords(atom) for atom in atoms]
    return {
        "x": round(sum(coord[0] for coord in coords) / len(coords), 3),
        "y": round(sum(coord[1] for coord in coords) / len(coords), 3),
        "z": round(sum(coord[2] for coord in coords) / len(coords), 3),
    }


def atom_position(atoms: list[dict[str, Any]], atom_name: str) -> dict[str, float] | None:
    for atom in atoms:
        if atom.get("label_atom_id") == atom_name or atom.get("auth_atom_id") == atom_name:
            x, y, z = _coords(atom)
            return {"x": round(x, 3), "y": round(y, 3), "z": round(z, 3)}
    return None


def pairwise_distances(residues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    distances: list[dict[str, Any]] = []
    for left_index, left in enumerate(residues):
        for right in residues[left_index + 1 :]:
            left_point = left.get("ca") or left.get("centroid")
            right_point = right.get("ca") or right.get("centroid")
            if not left_point or not right_point:
                continue
            distances.append(
                {
                    "left": left.get("residue_node_id"),
                    "right": right.get("residue_node_id"),
                    "distance": round(_distance(left_point, right_point), 3),
                    "coordinate_type": "ca_or_centroid",
                }
            )
    return distances


def ligand_context_from_atoms(
    atoms: list[dict[str, Any]],
    resolved_residues: list[dict[str, Any]],
    cutoff_angstrom: float = LIGAND_DISTANCE_CUTOFF_ANGSTROM,
) -> dict[str, Any]:
    active_points = [item.get("ca") or item.get("centroid") for item in resolved_residues]
    active_points = [point for point in active_points if point]
    if not active_points:
        return {
            "distance_cutoff_angstrom": cutoff_angstrom,
            "proximal_ligands": [],
            "ligand_codes": [],
            "cofactor_families": [],
            "structure_ligands": [],
            "structure_ligand_codes": [],
            "structure_cofactor_families": [],
        }

    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") != "HETATM":
            continue
        code = (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if not code or code in IGNORED_LIGAND_CODES:
            continue
        chain = str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")
        resid = str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")
        by_site[(code, chain, resid)].append(atom)

    structure_sites: list[dict[str, Any]] = []
    site_hits: list[dict[str, Any]] = []
    for (code, chain, resid), ligand_atoms in by_site.items():
        min_distance = _min_ligand_distance_to_active_site(ligand_atoms, active_points)
        if min_distance is None:
            continue
        site = {
            "code": code,
            "chain_name": chain or None,
            "resid": resid or None,
            "atom_count": len(ligand_atoms),
            "min_distance_to_active_site": round(min_distance, 3),
        }
        structure_sites.append(site)
        if min_distance > cutoff_angstrom:
            continue
        site_hits.append(site)

    structure_ligands = _summarize_ligand_sites(structure_sites)
    proximal_ligands = _summarize_ligand_sites(site_hits)
    ligand_codes = [str(item["code"]) for item in proximal_ligands]
    cofactor_families = sorted(_infer_cofactor_families(ligand_codes))
    structure_ligand_codes = [str(item["code"]) for item in structure_ligands]
    structure_cofactor_families = sorted(_infer_cofactor_families(structure_ligand_codes))
    return {
        "distance_cutoff_angstrom": cutoff_angstrom,
        "proximal_ligands": proximal_ligands,
        "ligand_codes": ligand_codes,
        "cofactor_families": cofactor_families,
        "structure_ligands": structure_ligands,
        "structure_ligand_codes": structure_ligand_codes,
        "structure_cofactor_families": structure_cofactor_families,
    }


def structure_ligand_inventory_from_atoms(atoms: list[dict[str, Any]]) -> dict[str, Any]:
    by_code: dict[str, dict[str, Any]] = {}
    for atom in atoms:
        if atom.get("group_PDB") != "HETATM":
            continue
        code = (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if not code or code in IGNORED_LIGAND_CODES:
            continue
        existing = by_code.setdefault(
            code,
            {
                "code": code,
                "instance_count": 0,
                "atom_count": 0,
            },
        )
        existing["atom_count"] += 1
        chain = str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")
        resid = str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")
        site_key = (chain, resid)
        sites = existing.setdefault("_sites", set())
        if site_key not in sites:
            sites.add(site_key)
            existing["instance_count"] += 1

    ligands: list[dict[str, Any]] = []
    for item in by_code.values():
        item.pop("_sites", None)
        ligands.append(item)
    ligand_codes = sorted(by_code)
    return {
        "ligands": sorted(ligands, key=lambda item: str(item["code"])),
        "ligand_codes": ligand_codes,
        "cofactor_families": sorted(_infer_cofactor_families(ligand_codes)),
    }


def _summarize_ligand_sites(site_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_code: dict[str, dict[str, Any]] = {}
    for site in site_hits:
        code = str(site["code"])
        existing = by_code.get(code)
        if existing is None:
            by_code[code] = {
                "code": code,
                "instance_count": 1,
                "atom_count": int(site["atom_count"]),
                "min_distance_to_active_site": float(site["min_distance_to_active_site"]),
            }
            continue
        existing["instance_count"] += 1
        existing["atom_count"] += int(site["atom_count"])
        existing["min_distance_to_active_site"] = min(
            float(existing["min_distance_to_active_site"]),
            float(site["min_distance_to_active_site"]),
        )

    return sorted(
        (
            {
                **item,
                "min_distance_to_active_site": round(
                    float(item["min_distance_to_active_site"]), 3
                ),
            }
            for item in by_code.values()
        ),
        key=lambda item: (float(item["min_distance_to_active_site"]), str(item["code"])),
    )


def pocket_context_from_atoms(
    atoms: list[dict[str, Any]],
    resolved_residues: list[dict[str, Any]],
    cutoff_angstrom: float = POCKET_DISTANCE_CUTOFF_ANGSTROM,
) -> dict[str, Any]:
    active_points = [item.get("ca") or item.get("centroid") for item in resolved_residues]
    active_points = [point for point in active_points if point]
    if not active_points:
        return _empty_pocket_context(cutoff_angstrom)

    active_site_keys = {
        (str(item.get("chain_name") or ""), str(item.get("resid") or ""))
        for item in resolved_residues
    }

    by_site: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        code = (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if code not in STANDARD_AMINO_ACIDS:
            continue
        chain = str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")
        resid = str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")
        if any(_atom_matches_position(atom, active_chain, active_resid) for active_chain, active_resid in active_site_keys):
            continue
        by_site[(code, chain, resid)].append(atom)

    nearby_sites: list[dict[str, Any]] = []
    nearby_codes: list[str] = []
    for (code, chain, resid), site_atoms in by_site.items():
        min_distance = _min_atom_group_distance_to_points(site_atoms, active_points)
        if min_distance is None or min_distance > cutoff_angstrom:
            continue
        nearby_sites.append(
            {
                "code": code,
                "chain_name": chain or None,
                "resid": resid or None,
                "atom_count": len(site_atoms),
                "min_distance_to_active_site": round(min_distance, 3),
            }
        )
        nearby_codes.append(code)

    if not nearby_sites:
        return _empty_pocket_context(cutoff_angstrom)

    nearby_sites.sort(key=lambda item: (float(item["min_distance_to_active_site"]), str(item["code"])))
    residue_code_counts = {
        code: nearby_codes.count(code)
        for code in sorted(set(nearby_codes))
    }
    descriptors = _pocket_descriptors(nearby_codes, nearby_sites)
    return {
        "distance_cutoff_angstrom": cutoff_angstrom,
        "nearby_residue_count": len(nearby_sites),
        "nearby_residue_sites": nearby_sites,
        "residue_code_counts": residue_code_counts,
        "descriptors": descriptors,
    }


def _atom_row(headers: list[str], values: list[str]) -> dict[str, Any]:
    row: dict[str, Any] = {}
    for header, value in zip(headers, values):
        key = header.replace("_atom_site.", "")
        row[key] = None if value in {".", "?"} else value
    for axis in ["Cartn_x", "Cartn_y", "Cartn_z"]:
        if row.get(axis) is not None:
            row[axis] = float(row[axis])
    return row


def _atom_matches_position(
    atom: dict[str, Any],
    chain_name: str | None,
    residue_id: str | None,
) -> bool:
    if chain_name is not None and chain_name not in _atom_chain_ids(atom):
        return False
    if residue_id is not None and residue_id not in _atom_residue_ids(atom):
        return False
    return True


def _atom_chain_ids(atom: dict[str, Any]) -> set[str]:
    return {
        str(value)
        for value in [atom.get("auth_asym_id"), atom.get("label_asym_id")]
        if value not in {None, "", ".", "?"}
    }


def _atom_residue_ids(atom: dict[str, Any]) -> set[str]:
    return {
        str(value)
        for value in [atom.get("auth_seq_id"), atom.get("label_seq_id")]
        if value not in {None, "", ".", "?"}
    }


def _coords(atom: dict[str, Any]) -> tuple[float, float, float]:
    return float(atom["Cartn_x"]), float(atom["Cartn_y"]), float(atom["Cartn_z"])


def _distance(left: dict[str, float], right: dict[str, float]) -> float:
    return math.sqrt(
        (left["x"] - right["x"]) ** 2
        + (left["y"] - right["y"]) ** 2
        + (left["z"] - right["z"]) ** 2
    )


def _min_ligand_distance_to_active_site(
    ligand_atoms: list[dict[str, Any]],
    active_points: list[dict[str, float]],
) -> float | None:
    return _min_atom_group_distance_to_points(ligand_atoms, active_points)


def _min_atom_group_distance_to_points(
    atoms: list[dict[str, Any]],
    points: list[dict[str, float]],
) -> float | None:
    min_distance: float | None = None
    for atom in atoms:
        atom_point = {"x": float(atom["Cartn_x"]), "y": float(atom["Cartn_y"]), "z": float(atom["Cartn_z"])}
        for point in points:
            distance = _distance(atom_point, point)
            if min_distance is None or distance < min_distance:
                min_distance = distance
    return min_distance


def _infer_cofactor_families(ligand_codes: list[str]) -> set[str]:
    families: set[str] = set()
    for code in ligand_codes:
        upper = code.upper()
        mapped = COFACTOR_LIGAND_MAP.get(upper)
        if mapped:
            families.add(mapped)
        if upper in METAL_ION_CODES:
            families.add("metal_ion")
    return families


def _pocket_descriptors(
    residue_codes: list[str],
    nearby_sites: list[dict[str, Any]],
) -> dict[str, float]:
    count = len(residue_codes)
    if count < 1:
        return {
            "hydrophobic_fraction": 0.0,
            "polar_fraction": 0.0,
            "positive_fraction": 0.0,
            "negative_fraction": 0.0,
            "aromatic_fraction": 0.0,
            "sulfur_fraction": 0.0,
            "charge_balance": 0.0,
            "mean_min_distance_to_active_site": 0.0,
        }
    hydrophobic_fraction = _fraction(residue_codes, HYDROPHOBIC_RESIDUES)
    polar_fraction = _fraction(residue_codes, POLAR_RESIDUES)
    positive_fraction = _fraction(residue_codes, POSITIVE_RESIDUES)
    negative_fraction = _fraction(residue_codes, NEGATIVE_RESIDUES)
    aromatic_fraction = _fraction(residue_codes, AROMATIC_RESIDUES)
    sulfur_fraction = _fraction(residue_codes, SULFUR_RESIDUES)
    mean_distance = sum(float(item["min_distance_to_active_site"]) for item in nearby_sites) / len(nearby_sites)
    return {
        "hydrophobic_fraction": hydrophobic_fraction,
        "polar_fraction": polar_fraction,
        "positive_fraction": positive_fraction,
        "negative_fraction": negative_fraction,
        "aromatic_fraction": aromatic_fraction,
        "sulfur_fraction": sulfur_fraction,
        "charge_balance": round(positive_fraction - negative_fraction, 4),
        "mean_min_distance_to_active_site": round(mean_distance, 4),
    }


def _fraction(items: list[str], reference: set[str]) -> float:
    if not items:
        return 0.0
    return round(sum(1 for item in items if item in reference) / len(items), 4)


def _empty_pocket_context(cutoff_angstrom: float = POCKET_DISTANCE_CUTOFF_ANGSTROM) -> dict[str, Any]:
    return {
        "distance_cutoff_angstrom": cutoff_angstrom,
        "nearby_residue_count": 0,
        "nearby_residue_sites": [],
        "residue_code_counts": {},
        "descriptors": _pocket_descriptors([], []),
    }


def _entry_id_from_residue_node(node_id: str) -> str | None:
    if ":residue:" not in node_id:
        return None
    return node_id.split(":residue:", 1)[0]


def _entry_context_by_id(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    contexts: dict[str, dict[str, Any]] = {}
    mechanism_texts_by_entry: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        node_id = str(node.get("id", ""))
        if node.get("type") == "m_csa_entry":
            name = node.get("name")
            if isinstance(name, str) and name:
                contexts.setdefault(node_id, {})["entry_name"] = name
        elif node.get("type") == "mechanism_text":
            entry_id = _entry_id_from_mechanism_node(node_id)
            text = node.get("text")
            if entry_id and isinstance(text, str) and text.strip():
                mechanism_texts_by_entry[entry_id].append(_mechanism_text_snippet(text))

    for entry_id, snippets in mechanism_texts_by_entry.items():
        context = contexts.setdefault(entry_id, {})
        context["mechanism_text_count"] = len(snippets)
        context["mechanism_text_snippets"] = snippets[:3]
    return contexts


def _entry_id_from_mechanism_node(node_id: str) -> str | None:
    if ":mechanism:" not in node_id:
        return None
    return node_id.split(":mechanism:", 1)[0]


def _mechanism_text_snippet(text: str, limit: int = 300) -> str:
    cleaned = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _entry_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = entry_id.partition(":")
    try:
        numeric_id = int(suffix)
    except ValueError:
        numeric_id = 0
    return (prefix, numeric_id, entry_id)


def _positions_by_pdb(residue_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_pdb: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for residue in residue_nodes:
        for position in residue.get("structure_positions", []):
            pdb_id = position.get("pdb_id")
            if not pdb_id:
                continue
            by_pdb[str(pdb_id).upper()].append(
                {
                    "residue_node_id": residue.get("id"),
                    "roles": residue.get("roles", []),
                    "pdb_id": str(pdb_id).upper(),
                    "chain_name": position.get("chain_name"),
                    "code": position.get("code"),
                    "resid": position.get("resid"),
                }
            )
    return by_pdb


def _json_dumps(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
