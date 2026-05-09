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
    residue_nodes = [node for node in nodes if node.get("type") == "catalytic_residue"]
    residues_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in residue_nodes:
        entry_id = _entry_id_from_residue_node(node.get("id", ""))
        if entry_id:
            residues_by_entry[entry_id].append(node)

    cif_cache: dict[str, list[dict[str, Any]]] = {}
    entry_features: list[dict[str, Any]] = []

    for entry_id in sorted(residues_by_entry)[:max_entries]:
        residues = residues_by_entry[entry_id]
        positions_by_pdb = _positions_by_pdb(residues)
        if not positions_by_pdb:
            entry_features.append(
                {
                    "entry_id": entry_id,
                    "status": "no_structure_positions",
                    "residue_count": len(residues),
                    "pdb_id": None,
                    "residues": [],
                    "pairwise_distances_angstrom": [],
                    "missing_positions": len(residues),
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
                    "status": "structure_fetch_failed",
                    "pdb_id": pdb_id,
                    "error": str(exc),
                    "residue_count": len(residues),
                    "residues": [],
                    "pairwise_distances_angstrom": [],
                    "missing_positions": len(positions_by_pdb[pdb_id]),
                }
            )
            continue

        resolved: list[dict[str, Any]] = []
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
                "status": "ok" if len(resolved) >= 2 else "insufficient_resolved_residues",
                "pdb_id": pdb_id,
                "residue_count": len(residues),
                "resolved_residue_count": len(resolved),
                "missing_positions": missing,
                "residues": resolved,
                "pairwise_distances_angstrom": pairwise_distances(resolved),
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
        atom_chain = atom.get("auth_asym_id") or atom.get("label_asym_id")
        atom_resid = atom.get("auth_seq_id") or atom.get("label_seq_id")
        atom_code = (atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if chain and atom_chain != chain:
            continue
        if residue_id and atom_resid != residue_id:
            continue
        if residue_code and atom_code and atom_code != residue_code:
            continue
        if atom.get("group_PDB") != "ATOM":
            continue
        selected.append(atom)
    return selected


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


def _atom_row(headers: list[str], values: list[str]) -> dict[str, Any]:
    row: dict[str, Any] = {}
    for header, value in zip(headers, values):
        key = header.replace("_atom_site.", "")
        row[key] = None if value in {".", "?"} else value
    for axis in ["Cartn_x", "Cartn_y", "Cartn_z"]:
        if row.get(axis) is not None:
            row[axis] = float(row[axis])
    return row


def _coords(atom: dict[str, Any]) -> tuple[float, float, float]:
    return float(atom["Cartn_x"]), float(atom["Cartn_y"]), float(atom["Cartn_z"])


def _distance(left: dict[str, float], right: dict[str, float]) -> float:
    return math.sqrt(
        (left["x"] - right["x"]) ** 2
        + (left["y"] - right["y"]) ** 2
        + (left["z"] - right["z"]) ** 2
    )


def _entry_id_from_residue_node(node_id: str) -> str | None:
    if ":residue:" not in node_id:
        return None
    return node_id.split(":residue:", 1)[0]


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
