#!/usr/bin/env python3
"""Validate a source-bound Atlas study-context packet.

The validator is intentionally data driven: the packet declares one deposited
nonpolymer instance, atom selections, geometry, typed connections, observations,
and evidence-qualified relations.  The code recomputes coordinate facts without
promoting a study association to a mechanism-step or causal claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_primary_source_check import parse_mmcif_categories  # noqa: E402


DEFAULT_PACKET = ROOT / "data/atlas/study_context/6ha3"
PROJECTION_SCHEMA = "catalytic-earth.atlas-study-context.v1"
INVENTORY_SCHEMA = "catalytic-earth.atlas-study-context-source-inventory.v1"
RECEIPT_SCHEMA = "catalytic-earth.primary-source-acquisition-receipts.v1"
REVIEW_SCHEMA = "catalytic-earth.atlas-study-context-review.v1"
PARSED_CATEGORIES = {
    "_atom_site",
    "_chem_comp",
    "_chem_comp_bond",
    "_entry",
    "_entity",
    "_exptl_crystal_grow",
    "_pdbx_nonpoly_scheme",
    "_struct",
    "_struct_conn",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_bound_path(binding: dict[str, Any], root: Path) -> Path:
    relative = binding.get("path")
    _require(isinstance(relative, str) and relative, "source path must be nonempty text")
    posix = PurePosixPath(relative)
    windows = PureWindowsPath(relative)
    _require(
        "\\" not in relative
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and "." not in posix.parts
        and ".." not in posix.parts,
        "source path must be repository-relative",
    )
    path = (root / posix).resolve()
    _require(root in path.parents and path.is_file(), "bound source is missing")
    _require(_sha256(path) == binding.get("sha256"), "bound source hash differs")
    if "bytes" in binding:
        _require(path.stat().st_size == binding["bytes"], "bound source byte count differs")
    return path


def _one(rows: list[dict[str, str]], predicate, message: str) -> dict[str, str]:
    matches = [row for row in rows if predicate(row)]
    _require(len(matches) == 1, message)
    return matches[0]


def _float(value: str, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _require(math.isfinite(result), f"{label} must be finite")
    return result


def _distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    return math.dist(
        (left["x"], left["y"], left["z"]),
        (right["x"], right["y"], right["z"]),
    )


def _subtract(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(a - b for a, b in zip(left, right))


def _dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _cross(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _norm(vector: tuple[float, ...]) -> float:
    return math.sqrt(_dot(vector, vector))


def _torsion(points: list[dict[str, Any]]) -> float:
    p0, p1, p2, p3 = [
        (point["x"], point["y"], point["z"]) for point in points
    ]
    b0 = _subtract(p0, p1)
    b1 = _subtract(p2, p1)
    b2 = _subtract(p3, p2)
    length = _norm(b1)
    _require(length > 0, "torsion central bond has zero length")
    axis = tuple(value / length for value in b1)
    v = tuple(value - _dot(b0, axis) * direction for value, direction in zip(b0, axis))
    w = tuple(value - _dot(b2, axis) * direction for value, direction in zip(b2, axis))
    _require(_norm(v) > 0 and _norm(w) > 0, "torsion is undefined")
    return math.degrees(math.atan2(_dot(_cross(axis, v), w), _dot(v, w)))


def _atom_projection(row: dict[str, str]) -> dict[str, Any]:
    return {
        "atom_site_id": row["id"],
        "b_iso_or_equiv": _float(row["b_iso_or_equiv"], "atom B factor"),
        "element": row["type_symbol"],
        "label_atom_id": row["label_atom_id"],
        "occupancy": _float(row["occupancy"], "atom occupancy"),
        "x": _float(row["cartn_x"], "atom x"),
        "y": _float(row["cartn_y"], "atom y"),
        "z": _float(row["cartn_z"], "atom z"),
    }


def _validate_receipts(
    receipts: dict[str, Any], inventory: dict[str, Any], coordinate_path: Path
) -> None:
    _require(receipts.get("schema_version") == RECEIPT_SCHEMA, "receipt schema differs")
    attempts = receipts.get("attempts")
    _require(isinstance(attempts, list) and attempts, "receipt attempts are absent")
    indices = [row.get("request_index") for row in attempts]
    _require(indices == list(range(1, len(attempts) + 1)), "receipt request indices differ")
    _require(all(row.get("http_status") == 200 for row in attempts), "capture HTTP status differs")
    aggregate = receipts.get("aggregate", {})
    _require(
        aggregate.get("direct_capture_request_count") == len(attempts),
        "receipt request aggregate differs",
    )
    _require(
        aggregate.get("direct_capture_response_bytes")
        == sum(row.get("bytes_read", 0) for row in attempts),
        "receipt byte aggregate differs",
    )
    limits = receipts.get("limits", {})
    _require(
        len(attempts) <= limits.get("max_requests", -1)
        and aggregate["direct_capture_response_bytes"] <= limits.get("max_response_bytes", -1)
        and aggregate.get("within_limits") is True,
        "capture budget is exceeded",
    )
    inventory_sources = {row["artifact_id"]: row for row in inventory.get("sources", [])}
    _require(set(inventory_sources) == {row["artifact_id"] for row in attempts}, "inventory/receipt artifacts differ")
    for attempt in attempts:
        source = inventory_sources[attempt["artifact_id"]]
        _require(
            source.get("bytes") == attempt.get("bytes_read")
            and source.get("sha256") == attempt.get("sha256"),
            "inventory/receipt source facts differ",
        )
    retained = [row for row in inventory_sources.values() if row.get("redistributed")]
    _require(len(retained) == 1, "exactly one source must be redistributed")
    _require(retained[0].get("path") is not None and _sha256(coordinate_path) == retained[0]["sha256"], "redistributed coordinate source differs")


def _validate_observations(projection: dict[str, Any]) -> None:
    observations = projection.get("observations")
    _require(isinstance(observations, list) and len(observations) == 3, "observation set differs")
    by_id = {row.get("observation_id"): row for row in observations}
    _require(len(by_id) == len(observations), "observation IDs repeat")
    required = {
        "e160q-f6p-stopped-flow",
        "e160q-f6p-nmr",
        "e160q-x5p-r5p-turnover",
    }
    _require(set(by_id) == required, "observation IDs differ")
    _require(all(row.get("reported_variant") == "E160Q" for row in observations), "observation variant differs")
    stopped = by_id["e160q-f6p-stopped-flow"]
    _require(
        stopped.get("method") == "pre-steady-state stopped-flow"
        and stopped.get("endpoint") == "reversible covalent F6P-ThDP adduct formation"
        and stopped["conditions"].get("substrate") == "F6P",
        "stopped-flow endpoint scope differs",
    )
    _require(stopped["reported_values"].get("k_forward_per_s") == {"mean": 5.91, "sd": 0.43}, "stopped-flow rate differs")
    nmr = by_id["e160q-f6p-nmr"]
    _require(
        nmr.get("method") == "1D proton NMR after acid quench"
        and nmr.get("endpoint") == "acid-isolated covalent-intermediate accumulation",
        "NMR endpoint scope differs",
    )
    turnover = by_id["e160q-x5p-r5p-turnover"]
    _require(
        turnover.get("method") == "NADH-coupled steady-state spectrophotometry"
        and turnover.get("endpoint") == "X5P/R5P steady-state turnover to S7P/G3P"
        and turnover["conditions"].get("donor") == "X5P"
        and turnover["conditions"].get("acceptor") == "2 mM R5P",
        "turnover endpoint scope differs",
    )
    relations = projection.get("relations")
    _require(isinstance(relations, list) and len(relations) == len(observations), "relation set differs")
    _require({row.get("observation_id") for row in relations} == required, "relation observation bindings differ")
    arrangement = projection["arrangement"]
    instance = arrangement["deposited_instance"]
    expected_arrangement_id = (
        f"{arrangement['pdb_id']}:{instance['component_id']}:"
        f"{instance['label_asym_id']}:{instance['author_chain_id']}"
        f"{instance['author_residue_number']}:model{instance['model_id']}"
    )
    _require(
        all(row.get("arrangement_id") == expected_arrangement_id for row in relations),
        "relation arrangement binding differs",
    )
    relation_by_observation = {row["observation_id"]: row for row in relations}
    expected_relations = {
        "e160q-f6p-stopped-flow": "study_scoped_structure_state_to_measured_adduct_formation",
        "e160q-f6p-nmr": "study_scoped_structure_state_to_measured_intermediate_accumulation",
        "e160q-x5p-r5p-turnover": "same_variant_turnover_context_not_same_substrate_state",
    }
    _require(
        all(
            relation_by_observation[key].get("relation") == value
            for key, value in expected_relations.items()
        ),
        "relation evidence scope differs",
    )
    _require(
        all(row.get("unresolved_equivalences") for row in relations),
        "relations must preserve unresolved equivalences",
    )
    binding = projection.get("atlas_record_binding", {})
    _require(binding.get("mechanism_id") == "M0219", "Atlas record binding differs")
    _require(binding.get("relation") == "record_scope_only", "Atlas relation scope differs")
    _require(binding.get("proposal_step_grounding") is False, "unsupported mechanism-step promotion")
    claim = projection.get("claim_boundary", {})
    _require(
        claim.get("status")
        == "source_reviewed_study_scoped_association_not_independent_expert_validation",
        "claim status differs",
    )
    required_limits = {
        "identical protein preparation or tag sequence across crystallography and assays",
        "crystal-to-solution conformer identity, occupancy, protonation, or population",
        "a complete symmetry-expanded active site",
        "causation from the deposited distortion to any measured rate",
        "productive full-cycle turnover with F6P as donor",
        "an exact M0219 proposal or elementary-step assignment",
    }
    _require(
        set(claim.get("not_established", [])) == required_limits,
        "claim-boundary abstentions differ",
    )


def _validate_coordinates(projection: dict[str, Any], coordinate_path: Path) -> dict[str, Any]:
    arrangement = projection["arrangement"]
    tables = parse_mmcif_categories(
        coordinate_path.read_text(encoding="utf-8"), categories=PARSED_CATEGORIES
    )
    _require({row.get("id") for row in tables["_entry"]} == {arrangement["pdb_id"]}, "PDB entry differs")
    structure = _one(tables["_struct"], lambda row: row.get("entry_id") == arrangement["pdb_id"], "structure row differs")
    _require(structure.get("title") == arrangement.get("structure_title"), "structure title differs")
    protein = arrangement["protein"]
    entity = _one(tables["_entity"], lambda row: row.get("id") == protein["entity_id"], "protein entity differs")
    _require(entity.get("pdbx_mutation") == protein["deposited_mutation"], "deposited variant differs")
    _require(
        arrangement.get("assembly_scope", {}).get("complete_active_site_represented") is False,
        "unsupported complete-active-site promotion",
    )
    instance = arrangement["deposited_instance"]
    scheme = _one(
        tables["_pdbx_nonpoly_scheme"],
        lambda row: row.get("asym_id") == instance["label_asym_id"]
        and row.get("entity_id") == instance["label_entity_id"]
        and row.get("mon_id") == instance["component_id"]
        and int(row.get("pdb_seq_num", -1)) == instance["author_residue_number"]
        and row.get("pdb_strand_id") == instance["author_chain_id"],
        "deposited nonpolymer instance differs",
    )
    _require(scheme.get("pdb_mon_id") == instance["author_component_id"], "author component differs")
    component = _one(tables["_chem_comp"], lambda row: row.get("id") == instance["component_id"], "component identity differs")
    _require(component.get("pdbx_synonyms") == instance["component_name"], "component name differs")
    atoms = [
        row
        for row in tables["_atom_site"]
        if row.get("label_asym_id") == instance["label_asym_id"]
        and row.get("label_entity_id") == instance["label_entity_id"]
        and row.get("label_comp_id") == instance["component_id"]
        and row.get("auth_asym_id") == instance["author_chain_id"]
        and int(row.get("auth_seq_id", -1)) == instance["author_residue_number"]
        and int(row.get("pdbx_pdb_model_num", -1)) == instance["model_id"]
    ]
    _require(len(atoms) == instance["component_atom_count"], "component atom count differs")
    occupancies = [_float(row["occupancy"], "component occupancy") for row in atoms]
    _require([min(occupancies), max(occupancies)] == instance["occupancy_range"], "component occupancy range differs")
    selected_names = [row["label_atom_id"] for row in arrangement["selected_atoms"]]
    _require(len(selected_names) == len(set(selected_names)), "selected atom names repeat")
    selected = {
        name: _atom_projection(_one(atoms, lambda row, name=name: row.get("label_atom_id") == name, f"selected atom {name} differs"))
        for name in selected_names
    }
    _require([selected[name] for name in selected_names] == arrangement["selected_atoms"], "selected atom facts differ")
    declared_bonds = {
        (frozenset(row["atom_ids"]), row["order"])
        for row in arrangement["component_dictionary_bonds"]
    }
    deposited_bonds = {
        (frozenset((row.get("atom_id_1"), row.get("atom_id_2"))), row.get("value_order"))
        for row in tables["_chem_comp_bond"]
        if row.get("comp_id") == instance["component_id"]
    }
    _require(declared_bonds <= deposited_bonds, "component dictionary bond differs")
    incident = []
    protein_covalent = 0
    for row in tables["_struct_conn"]:
        side = None
        if row.get("ptnr1_label_asym_id") == instance["label_asym_id"] and row.get("ptnr1_label_comp_id") == instance["component_id"]:
            side = 1
        elif row.get("ptnr2_label_asym_id") == instance["label_asym_id"] and row.get("ptnr2_label_comp_id") == instance["component_id"]:
            side = 2
        if side is None:
            continue
        other = 2 if side == 1 else 1
        if row.get("conn_type_id") == "covale":
            protein_covalent += 1
        incident.append(
            {
                "connection_id": row["id"],
                "connection_type": row["conn_type_id"],
                "ligand_atom_id": row[f"ptnr{side}_label_atom_id"],
                "partner_alt_id": None if row.get(f"pdbx_ptnr{other}_label_alt_id") in {".", "?"} else row[f"pdbx_ptnr{other}_label_alt_id"],
                "partner_atom_id": row[f"ptnr{other}_label_atom_id"],
                "partner_component_id": row[f"ptnr{other}_label_comp_id"],
            }
        )
    _require(sorted(incident, key=lambda row: row["connection_id"]) == arrangement["incident_connections"], "incident connection inventory differs")
    _require(protein_covalent == arrangement["protein_covalent_connection_count"], "protein covalent-connection count differs")
    geometry_rows = arrangement["deposited_geometry"]
    _require(
        len({row.get("metric_id") for row in geometry_rows}) == len(geometry_rows),
        "geometry metric IDs repeat",
    )
    for metric in geometry_rows:
        atom_ids = metric.get("atom_ids")
        _require(
            isinstance(atom_ids, list)
            and all(atom_id in selected for atom_id in atom_ids),
            "geometry atom selection differs",
        )
        if metric.get("metric_type") == "distance_angstrom":
            _require(len(atom_ids) == 2, "distance geometry needs two atoms")
            observed = round(_distance(selected[atom_ids[0]], selected[atom_ids[1]]), 6)
            _require(observed == metric.get("value"), "declared distance differs")
        elif metric.get("metric_type") == "deviation_from_180_degree_torsion":
            _require(len(atom_ids) == 4, "torsion geometry needs four atoms")
            torsion = _torsion([selected[atom_id] for atom_id in atom_ids])
            _require(
                round(torsion, 6) == metric.get("source_torsion_degrees"),
                "declared torsion differs",
            )
            _require(
                round(180.0 - abs(torsion), 6) == metric.get("value_degrees"),
                "declared planar deviation differs",
            )
        else:
            raise ValueError("unsupported geometry metric type")
    geometry = {row["metric_id"]: row for row in geometry_rows}
    _require(
        geometry.get("cofactor-substrate-covalent-bond", {}).get("atom_ids")
        == ["C2", "CF2"]
        and geometry.get("source-highlighted-scissile-bond", {}).get("atom_ids")
        == ["CF2", "CF3"]
        and geometry.get("source-highlighted-out-of-plane-deviation", {}).get("atom_ids")
        == ["C5", "S1", "C2", "CF2"],
        "required geometry definitions differ",
    )
    grow = _one(tables["_exptl_crystal_grow"], lambda row: True, "crystal-growth row differs")
    conditions = arrangement["coordinate_conditions"]
    _require(
        _float(grow["ph"], "crystal pH") == conditions["crystal_growth_ph"]
        and _float(grow["temp"], "crystal temperature") == conditions["growth_temperature_conflict"]["scalar_kelvin"]
        and "279.0K" in grow["pdbx_details"],
        "crystal-growth conditions differ",
    )
    cif_text = coordinate_path.read_text(encoding="utf-8")
    accession = re.escape(protein["uniprot_accession"])
    _require(
        re.search(rf"^_struct_ref\.pdbx_db_accession\s+{accession}\s*$", cif_text, re.MULTILINE)
        is not None,
        "deposited UniProt accession differs",
    )
    match = re.search(r"^_diffrn\.ambient_temp\s+([0-9.]+)\s*$", cif_text, re.MULTILINE)
    _require(match is not None and float(match.group(1)) == conditions["measurement_temperature_kelvin"], "diffraction temperature differs")
    return {
        "atom_count": len(atoms),
        "incident_connection_count": len(incident),
        "selected_atom_count": len(selected),
    }


def validate_packet(packet: Path = DEFAULT_PACKET, root: Path = ROOT) -> dict[str, Any]:
    packet = packet.resolve()
    _require(packet.is_dir(), "study-context packet directory is missing")
    projection_path = packet / "evidence_projection.json"
    inventory_path = packet / "source_inventory.json"
    receipts_path = packet / "acquisition_receipts.json"
    review_path = packet / "review.json"
    projection = _read_json(projection_path)
    inventory = _read_json(inventory_path)
    receipts = _read_json(receipts_path)
    review = _read_json(review_path)
    _require(projection.get("schema_version") == PROJECTION_SCHEMA, "projection schema differs")
    _require(inventory.get("schema_version") == INVENTORY_SCHEMA, "inventory schema differs")
    coordinate_path = _safe_bound_path(projection["arrangement"]["coordinate_source"], root)
    record_path = _safe_bound_path(projection["atlas_record_binding"]["source"], root)
    records = _read_json(record_path).get("records", [])
    _require(sum(row.get("mcsa_id") == "M0219" for row in records) == 1, "M0219 record binding differs")
    _validate_receipts(receipts, inventory, coordinate_path)
    _validate_observations(projection)
    coordinate_summary = _validate_coordinates(projection, coordinate_path)
    _require(review.get("schema_version") == REVIEW_SCHEMA, "review schema differs")
    pins = review.get("reviewed_sha256", {})
    expected_pins = {
        "acquisition_receipts.json": _sha256(receipts_path),
        "evidence_projection.json": _sha256(projection_path),
        "source_inventory.json": _sha256(inventory_path),
    }
    _require(pins == expected_pins, "manual review pin is stale")
    _require(review.get("decision") == "accept_study_scoped_association", "review decision differs")
    return {
        "packet_id": projection["packet_id"],
        "observation_count": len(projection["observations"]),
        "relation_count": len(projection["relations"]),
        "direct_capture_request_count": receipts["aggregate"]["direct_capture_request_count"],
        **coordinate_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args()
    print(json.dumps(validate_packet(args.packet), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
