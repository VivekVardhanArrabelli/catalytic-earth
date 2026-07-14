"""Small, deterministic readers for the bounded Atlas-3 source snapshots."""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path
from typing import Any


THREE_TO_ONE = {
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


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"source snapshot must be an object: {path}")
    return value


def read_rhea_snapshot(path: Path, expected_record_id: str) -> dict[str, Any]:
    """Return the exact bounded reaction fields from a normalized Rhea snapshot."""
    value = load_json(path)
    if value.get("source") != "Rhea" or value.get("record_id") != expected_record_id:
        raise ValueError(f"Rhea snapshot identity differs for {expected_record_id}")
    row = value.get("row")
    if not isinstance(row, dict) or row.get("Reaction identifier") != expected_record_id:
        raise ValueError(f"Rhea row identity differs for {expected_record_id}")
    identifiers = str(row.get("ChEBI identifier", "")).split(";")
    names = str(row.get("ChEBI name", "")).split(";")
    if not identifiers or len(identifiers) != len(names):
        raise ValueError(f"Rhea participant columns differ for {expected_record_id}")
    participants = [
        {"chebi_id": identifier, "name": name}
        for identifier, name in zip(identifiers, names, strict=True)
    ]
    ec_number = str(row.get("EC number", ""))
    if not ec_number.startswith("EC:"):
        raise ValueError(f"Rhea EC field is missing for {expected_record_id}")
    equation = row.get("Equation")
    if not isinstance(equation, str) or " = " not in equation:
        raise ValueError(f"Rhea equation is missing for {expected_record_id}")
    return {
        "source_id": "Rhea",
        "source_record_id": expected_record_id,
        "directionality": "undirected",
        "equation": equation,
        "ec_number": ec_number.removeprefix("EC:"),
        "participants": participants,
    }


def read_uniprot_snapshot(path: Path, expected_accession: str) -> dict[str, Any]:
    """Return identity, sequence, feature, and PDB cross-reference fields."""
    value = load_json(path)
    if value.get("primaryAccession") != expected_accession:
        raise ValueError(f"UniProt snapshot identity differs for {expected_accession}")
    sequence = value.get("sequence", {}).get("value")
    if not isinstance(sequence, str) or not sequence:
        raise ValueError(f"UniProt sequence is missing for {expected_accession}")
    features: list[dict[str, Any]] = []
    for feature in value.get("features", []):
        location = feature.get("location", {})
        start = location.get("start", {}).get("value")
        end = location.get("end", {}).get("value")
        if isinstance(start, int) and isinstance(end, int):
            features.append(
                {
                    "type": feature.get("type"),
                    "start": start,
                    "end": end,
                    "description": feature.get("description", ""),
                    "ligand": feature.get("ligand", {}).get("name"),
                }
            )
    pdb_cross_references: dict[str, dict[str, str]] = {}
    for cross_reference in value.get("uniProtKBCrossReferences", []):
        if cross_reference.get("database") != "PDB":
            continue
        properties = {
            item["key"]: item["value"]
            for item in cross_reference.get("properties", [])
            if isinstance(item, dict)
            and isinstance(item.get("key"), str)
            and isinstance(item.get("value"), str)
        }
        pdb_cross_references[str(cross_reference.get("id"))] = properties
    protein_name = (
        value.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value")
    )
    organism = value.get("organism", {}).get("scientificName")
    return {
        "accession": expected_accession,
        "protein_name": protein_name,
        "organism": organism,
        "sequence": sequence,
        "features": features,
        "pdb_cross_references": pdb_cross_references,
    }


def read_mcsa_snapshot(path: Path, expected_record_id: str) -> dict[str, Any]:
    """Return a checked M-CSA entry without changing its scientific wording."""
    value = load_json(path)
    numeric_id = int(expected_record_id.removeprefix("M"))
    if value.get("mcsa_id") != numeric_id:
        raise ValueError(f"M-CSA snapshot identity differs for {expected_record_id}")
    reaction = value.get("reaction")
    if not isinstance(reaction, dict):
        raise ValueError(f"M-CSA reaction is missing for {expected_record_id}")
    mechanisms = reaction.get("mechanisms")
    residues = value.get("residues")
    if not isinstance(mechanisms, list) or not isinstance(residues, list):
        raise ValueError(f"M-CSA mechanism/residue fields are missing for {expected_record_id}")
    proteins = [
        item.get("uniprot_id")
        for item in value.get("protein", {}).get("sequences", [])
        if isinstance(item, dict) and isinstance(item.get("uniprot_id"), str)
    ]
    return {
        "record_id": expected_record_id,
        "mcsa_id": numeric_id,
        "enzyme_name": value.get("enzyme_name"),
        "ec_numbers": value.get("all_ecs", []),
        "proteins": proteins,
        "mechanisms": mechanisms,
        "residues": residues,
    }


def select_mcsa_mechanism(entry: dict[str, Any], mechanism_id: int) -> dict[str, Any]:
    matches = [
        item
        for item in entry["mechanisms"]
        if isinstance(item, dict) and item.get("mechanism_id") == mechanism_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"M-CSA {entry['record_id']} does not contain exactly one mechanism {mechanism_id}"
        )
    mechanism = matches[0]
    if not isinstance(mechanism.get("rating"), int):
        raise ValueError("M-CSA mechanism rating is missing")
    return mechanism


def mcsa_residue_rows(entry: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten reference residue mappings while preserving numbering systems."""
    rows: list[dict[str, Any]] = []
    for residue in entry["residues"]:
        roles = sorted(
            {
                role.get("function")
                for role in residue.get("roles", [])
                if isinstance(role, dict) and isinstance(role.get("function"), str)
            }
        )
        for sequence in residue.get("residue_sequences", []):
            if not sequence.get("is_reference"):
                continue
            for chain in residue.get("residue_chains", []):
                if not chain.get("is_reference"):
                    continue
                rows.append(
                    {
                        "uniprot_id": sequence.get("uniprot_id"),
                        "residue_name": sequence.get("code"),
                        "sequence_position": sequence.get("resid"),
                        "pdb_id": str(chain.get("pdb_id", "")).upper(),
                        "chain_id": chain.get("auth_chain_name")
                        or chain.get("assembly_chain_name")
                        or chain.get("chain_name"),
                        "author_position": chain.get("auth_resid"),
                        "label_position": chain.get("resid"),
                        "roles": roles,
                    }
                )
    return rows


def read_pdb_snapshot(path: Path, expected_pdb_id: str) -> dict[str, Any]:
    """Read only the mmCIF metadata and polymer coordinate identities we need."""
    with gzip.open(path, "rt", encoding="utf-8", errors="strict") as handle:
        lines = handle.read().splitlines()
    entry_lines = [line for line in lines if line.startswith("_entry.id ")]
    if len(entry_lines) != 1 or expected_pdb_id not in entry_lines[0].upper():
        raise ValueError(f"PDB snapshot identity differs for {expected_pdb_id}")

    def scalar(prefix: str) -> str | None:
        matches = [line[len(prefix) :].strip() for line in lines if line.startswith(prefix)]
        if len(matches) != 1:
            return None
        return matches[0].strip("'")

    residues: dict[tuple[str, int], dict[str, Any]] = {}
    for line in lines:
        if not line.startswith("ATOM "):
            continue
        columns = line.split()
        if len(columns) < 21 or columns[3] != "CA":
            continue
        chain = columns[18]
        author_position = int(columns[16])
        residue_name = columns[17]
        residues[(chain, author_position)] = {
            "chain_id": chain,
            "author_position": author_position,
            "label_position": int(columns[8]),
            "residue_name": residue_name,
        }
    resolution = scalar("_refine.ls_d_res_high ")
    return {
        "pdb_id": expected_pdb_id,
        "title": scalar("_struct.title "),
        "method": scalar("_exptl.method "),
        "resolution_angstrom": float(resolution) if resolution else None,
        "residues": residues,
    }


def uniprot_chain_ranges(properties: dict[str, str]) -> list[dict[str, Any]]:
    """Parse a UniProt PDB Chains property such as ``A/B=2-206``."""
    raw = properties.get("Chains")
    if not raw:
        return []
    ranges: list[dict[str, Any]] = []
    for group in raw.split(","):
        match = re.fullmatch(r"\s*([^=]+)=(\d+)-(\d+)\s*", group)
        if not match:
            raise ValueError(f"unsupported UniProt PDB chain range: {group!r}")
        chains, start, end = match.groups()
        for chain in chains.split("/"):
            ranges.append(
                {
                    "chain_id": chain,
                    "uniprot_start": int(start),
                    "uniprot_end": int(end),
                }
            )
    return ranges


def residue_one_letter(residue_name: str) -> str:
    try:
        return THREE_TO_ONE[residue_name.upper()]
    except KeyError as exc:
        raise ValueError(f"unsupported standard residue name: {residue_name}") from exc
