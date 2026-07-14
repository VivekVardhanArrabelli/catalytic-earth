"""Deterministic readers for the bounded Atlas-10 source package."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"source snapshot must be an object: {path}")
    return value


def _chebi_from_uri(value: str | None) -> str | None:
    if not value:
        return None
    marker = "CHEBI_"
    if marker not in value:
        raise ValueError(f"unsupported Rhea ChEBI URI: {value}")
    return "CHEBI:" + value.rsplit(marker, 1)[1]


def read_atlas10_rhea_snapshot(
    path: Path,
    expected_record_id: str,
    *,
    selected_participant_ids: set[str],
) -> dict[str, Any]:
    """Read either a direct Rhea record or a content-bound zero-row EC query."""
    value = load_json(path)
    if value.get("source") != "Rhea" or value.get("record_id") != expected_record_id:
        raise ValueError(f"Rhea snapshot identity differs for {expected_record_id}")
    kind = value.get("query_result_kind")
    if expected_record_id.startswith("EC:"):
        if kind != "documented_zero_row_query" or value.get("rows") != []:
            raise ValueError(f"Rhea source gap differs for {expected_record_id}")
        if value.get("participant_rows") != []:
            raise ValueError(f"Rhea source gap cannot contain RDF participants")
        return {
            "source_status": "documented_query_gap",
            "source_id": "Rhea",
            "source_record_id": None,
            "source_query": value["query"],
            "directionality": "unknown_no_direct_record",
            "equation": None,
            "ec_number": expected_record_id.removeprefix("EC:"),
            "participants": [],
            "gap_context": {
                "query_result_count": 0,
                "query_snapshot_kind": "official_zero_row_tsv",
                "interpretation": (
                    "No direct Rhea record was returned by this frozen EC query; this is "
                    "not evidence that no reaction description exists in another source."
                ),
            },
        }
    if kind != "direct_record":
        raise ValueError(f"Rhea direct record differs for {expected_record_id}")
    rows = value.get("rows")
    if not isinstance(rows, list) or len(rows) != 1:
        raise ValueError(f"Rhea direct TSV row differs for {expected_record_id}")
    row = rows[0]
    if row.get("Reaction identifier") != expected_record_id:
        raise ValueError(f"Rhea direct row identity differs for {expected_record_id}")
    equation = row.get("Equation")
    ec_number = str(row.get("EC number", "")).removeprefix("EC:")
    if not isinstance(equation, str) or " = " not in equation or not ec_number:
        raise ValueError(f"Rhea direct reaction fields differ for {expected_record_id}")

    participants: list[dict[str, Any]] = []
    observed_ids: set[str] = set()
    observed_reactive_ids: set[str] = set()
    for source_row in value.get("participant_rows", []):
        accession = source_row.get("accession")
        if not isinstance(accession, str):
            raise ValueError(f"Rhea RDF participant lacks accession for {expected_record_id}")
        if accession.startswith("CHEBI:"):
            participant_id = accession
            participant_type = "small_molecule"
            reactive_part_id = None
        elif accession.startswith("GENERIC:"):
            participant_id = "RHEA-COMP:" + accession.split(":", 1)[1]
            participant_type = "macromolecule"
            reactive_part_id = _chebi_from_uri(source_row.get("reactive_chebi_uri"))
        else:
            raise ValueError(f"unsupported Rhea participant accession: {accession}")
        side_uri = source_row.get("side_uri")
        if not isinstance(side_uri, str) or not side_uri.endswith(("_L", "_R")):
            raise ValueError(f"Rhea participant side differs for {expected_record_id}")
        observed_ids.add(participant_id)
        if reactive_part_id is not None:
            observed_reactive_ids.add(reactive_part_id)
        participants.append(
            {
                "participant_id": participant_id,
                "name": source_row.get("name"),
                "participant_type": participant_type,
                "side": "left" if side_uri.endswith("_L") else "right",
                "stoichiometry": 1,
                "source_scope": "Rhea RDF participant",
                "source_accession": accession,
                "reactive_part_id": reactive_part_id,
                "source_row_count": 1,
                "source_count_values": [1],
            }
        )
    if observed_ids | observed_reactive_ids != selected_participant_ids:
        raise ValueError(
            f"Rhea participant/reactive-part set differs for {expected_record_id}: "
            f"{sorted(observed_ids | observed_reactive_ids)}"
        )
    return {
        "source_status": "direct_record",
        "source_id": "Rhea",
        "source_record_id": expected_record_id,
        "source_query": value["query"],
        "directionality": "undirected",
        "equation": equation,
        "ec_number": ec_number,
        "participants": sorted(
            participants, key=lambda item: (item["side"], item["participant_id"])
        ),
        "gap_context": None,
    }


def read_atlas10_mcsa_snapshot(path: Path, expected_record_id: str) -> dict[str, Any]:
    value = load_json(path)
    if value.get("source") != "M-CSA" or value.get("record_id") != expected_record_id:
        raise ValueError(f"M-CSA snapshot identity differs for {expected_record_id}")
    entry = value.get("entry")
    if not isinstance(entry, dict) or entry.get("mcsa_id") != int(expected_record_id[1:]):
        raise ValueError(f"M-CSA entry identity differs for {expected_record_id}")
    mechanisms = entry.get("reaction", {}).get("mechanisms")
    residues = entry.get("residues")
    schemes = value.get("step_schemes")
    if not isinstance(mechanisms, list) or not isinstance(residues, list):
        raise ValueError(f"M-CSA mechanism/residue fields are missing for {expected_record_id}")
    if not isinstance(schemes, list):
        raise ValueError(f"M-CSA schemes are missing for {expected_record_id}")
    scheme_index = {
        (item["mechanism_id"], item["step_id"]): item
        for item in schemes
        if isinstance(item, dict)
    }
    expected_keys = {
        (mechanism["mechanism_id"], step["step_id"])
        for mechanism in mechanisms
        for step in mechanism.get("steps", [])
    }
    if set(scheme_index) != expected_keys:
        raise ValueError(f"M-CSA scheme set differs for {expected_record_id}")
    proteins = [
        item.get("uniprot_id")
        for item in entry.get("protein", {}).get("sequences", [])
        if isinstance(item, dict) and isinstance(item.get("uniprot_id"), str)
    ]
    return {
        "record_id": expected_record_id,
        "mcsa_id": int(expected_record_id[1:]),
        "enzyme_name": entry.get("enzyme_name"),
        "description": entry.get("description"),
        "ec_numbers": entry.get("all_ecs", []),
        "reference_uniprot_id": entry.get("reference_uniprot_id"),
        "proteins": proteins,
        "compounds": entry.get("reaction", {}).get("compounds", []),
        "mechanisms": mechanisms,
        "residues": residues,
        "scheme_index": scheme_index,
    }


def mcsa_gap_participants(
    entry: dict[str, Any], *, selected_participant_ids: set[str]
) -> list[dict[str, Any]]:
    """Preserve M-CSA participant rows without relabeling them as a Rhea reaction."""
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for source_row in entry["compounds"]:
        participant_id = "CHEBI:" + str(source_row.get("chebi_id"))
        side = {"reactant": "left", "product": "right"}.get(source_row.get("type"))
        name = source_row.get("name")
        count = source_row.get("count")
        if side is None or not isinstance(name, str) or not isinstance(count, int):
            raise ValueError(f"M-CSA compound row is incomplete: {source_row}")
        key = participant_id, side, name
        group = grouped.setdefault(
            key,
            {
                "participant_id": participant_id,
                "name": name,
                "participant_type": "small_molecule_or_class",
                "side": side,
                "stoichiometry": 0,
                "source_scope": "M-CSA participant context; not a Rhea canonical reaction",
                "source_accession": participant_id,
                "reactive_part_id": None,
                "source_row_count": 0,
                "source_count_values": [],
            },
        )
        group["stoichiometry"] += count
        group["source_row_count"] += 1
        group["source_count_values"].append(count)
    if {item[0] for item in grouped} != selected_participant_ids:
        raise ValueError(f"M-CSA gap participant set differs: {sorted(item[0] for item in grouped)}")
    return [grouped[key] for key in sorted(grouped)]


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _atom_descriptor(raw_ref: str, atoms: dict[str, dict[str, Any]]) -> dict[str, Any]:
    descriptor = atoms.get(raw_ref)
    if descriptor is None:
        raise ValueError(f"M-CSA electron-flow point references an unknown atom: {raw_ref}")
    return {"source_atom_ref": raw_ref, **descriptor}


def parse_mcsa_scheme_flows(scheme: dict[str, Any]) -> dict[str, Any]:
    """Extract source-ordered curved-arrow endpoints without inferring atom maps."""
    content = scheme.get("content_utf8")
    if content is None:
        if scheme.get("retrieval_status") != "source_link_missing_http_404":
            raise ValueError("missing M-CSA scheme lacks an explicit retrieval failure")
        return {
            "scheme_status": "source_link_missing_http_404",
            "scheme_sha256": None,
            "electron_flows": [],
        }
    root = ET.fromstring(content)
    atoms: dict[str, dict[str, Any]] = {}
    for molecule in (item for item in root.iter() if _local_name(item) == "molecule"):
        molecule_id = molecule.get("molID")
        if not molecule_id:
            continue
        for atom in (item for item in molecule.iter() if _local_name(item) == "atom"):
            atom_id = atom.get("id")
            element = atom.get("elementType")
            if not atom_id or not element:
                raise ValueError("M-CSA scheme atom is incomplete")
            full_ref = f"{molecule_id}.{atom_id}"
            labels = [
                value
                for value in (atom.get("mrvExtraLabel"), atom.get("mrvAlias"))
                if value
            ]
            formal_charge = atom.get("formalCharge")
            atoms[full_ref] = {
                "element": element,
                "formal_charge": int(formal_charge) if formal_charge is not None else None,
                "semantic_labels": labels,
            }
    flows: list[dict[str, Any]] = []
    for flow in (item for item in root.iter() if _local_name(item) == "MEFlow"):
        points: list[dict[str, Any]] = []
        for point in list(flow):
            tag = _local_name(point)
            if tag not in {"MEFlowBasePoint", "MAtomSetPoint"}:
                raise ValueError(f"unsupported M-CSA electron-flow point: {tag}")
            raw_refs = point.get("atomRefs") or point.get("atomRef")
            if not raw_refs:
                raise ValueError("M-CSA electron-flow point lacks atom references")
            references = raw_refs.split()
            points.append(
                {
                    "point_kind": (
                        "electron_base_atom" if tag == "MEFlowBasePoint" else "atom_set"
                    ),
                    "atoms": [_atom_descriptor(reference, atoms) for reference in references],
                }
            )
        if len(points) != 2:
            raise ValueError("M-CSA curved arrow must contain exactly two ordered points")
        flows.append(
            {
                "flow_id": flow.get("id") or f"flow-{len(flows) + 1}",
                "source_point": points[0],
                "target_point": points[1],
                "ordering_semantics": "source_file_order_not_independently_inferred",
            }
        )
    return {
        "scheme_status": "source_curved_arrows_preserved",
        "scheme_sha256": scheme["content_sha256"],
        "electron_flows": flows,
    }


def mcsa_reference_residue_rows(entry: dict[str, Any]) -> list[dict[str, Any]]:
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
                chain_id = (
                    chain.get("auth_chain_name")
                    or chain.get("assembly_chain_name")
                    or chain.get("chain_name")
                )
                rows.append(
                    {
                        "uniprot_id": sequence.get("uniprot_id"),
                        "residue_name": sequence.get("code"),
                        "sequence_position": sequence.get("resid"),
                        "pdb_id": str(chain.get("pdb_id", "")).upper(),
                        "chain_id": chain_id,
                        "author_position": chain.get("auth_resid"),
                        "label_position": chain.get("resid"),
                        "roles": roles,
                    }
                )
    return rows


def read_cath_snapshot(path: Path, expected_record_id: str) -> dict[str, Any]:
    value = load_json(path)
    if value.get("source") != "CATH" or value.get("record_id") != expected_record_id:
        raise ValueError(f"CATH snapshot identity differs for {expected_record_id}")
    classification = expected_record_id.removeprefix("CATH:")
    rows = value.get("domain_rows")
    if not isinstance(rows, list) or any(
        row.get("classification_id") != classification for row in rows
    ):
        raise ValueError(f"CATH domain rows differ for {expected_record_id}")
    return {
        "record_id": expected_record_id,
        "classification_id": classification,
        "description": value["name_row"]["description"],
        "selected_pdb_ids": value["selected_pdb_ids"],
        "domain_rows": rows,
    }
