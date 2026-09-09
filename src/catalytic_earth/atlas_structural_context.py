"""Derive source-bound catalytic-site coordinate context from retained mmCIF.

The extractor is deliberately data driven.  A specification selects Atlas-10
records, structures, sites, atoms, and distance pairs; this module checks those
selections against the frozen kernel and derives deposited coordinate facts.
It preserves alternate conformers and connections without choosing a preferred
geometry or interpreting a short distance as a chemical bond.

Version 1 intentionally accepts one context per PDB and requires each selected
canonical site to resolve through exactly one Atlas-10 PDB mapping and one
unambiguous label-chain/insertion-code residue instance.  It therefore does not
yet represent biological-assembly copies, deliberately selected symmetry mates,
or alternative mappings of one canonical site.  Those cases fail explicitly
rather than being collapsed into this bounded two-structure comparison.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Any, Mapping

from .atlas_primary_source_check import parse_mmcif_categories
from .canonical_hash import canonical_file_sha256


SPEC_SCHEMA_VERSION = "catalytic-earth.atlas-structural-context-spec.v1"
BUNDLE_SCHEMA_VERSION = "catalytic-earth.atlas-structural-context.v1"
QUERY_SCHEMA_VERSION = "catalytic-earth.atlas-structural-context-query.v1"

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_PDB_RE = re.compile(r"^[0-9][A-Z0-9]{3}$")
_MISSING = {".", "?"}
_SPEC_FIELDS = {"schema_version", "bundle_id", "atlas10_binding", "structures"}
_BINDING_FIELDS = {"path", "sha256"}
_STRUCTURE_FIELDS = {
    "context_id",
    "case_id",
    "record_id",
    "pdb_id",
    "coordinate_binding",
    "selected_sites",
    "declared_distance_pairs",
    "interpretation",
}
_SITE_SELECTION_FIELDS = {"site_id", "atom_names"}
_PAIR_FIELDS = {"pair_id", "left", "right"}
_PAIR_ENDPOINT_FIELDS = {"site_id", "atom_name"}
_PARSED_CATEGORIES = frozenset(
    {
        "_atom_site",
        "_chem_comp",
        "_entry",
        "_entity",
        "_exptl_crystal_grow",
        "_pdbx_modification_feature",
        "_pdbx_nonpoly_scheme",
        "_struct",
        "_struct_conn",
    }
)
_ATOM_FIELDS = {
    "group_pdb",
    "id",
    "type_symbol",
    "label_atom_id",
    "label_alt_id",
    "label_comp_id",
    "label_asym_id",
    "label_entity_id",
    "label_seq_id",
    "pdbx_pdb_ins_code",
    "cartn_x",
    "cartn_y",
    "cartn_z",
    "occupancy",
    "b_iso_or_equiv",
    "auth_atom_id",
    "auth_comp_id",
    "auth_asym_id",
    "auth_seq_id",
    "pdbx_pdb_model_num",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    _require(
        isinstance(value, list) and (not nonempty or bool(value)),
        f"{label} must be a{' nonempty' if nonempty else 'n'} array",
    )
    return value


def _exact(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    row = _object(value, label)
    actual = set(row)
    _require(
        actual == fields,
        f"{label} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return row


def _text(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")
    return value


def _sha(value: Any, label: str) -> str:
    _require(isinstance(value, str) and _SHA_RE.fullmatch(value) is not None, f"{label} must be a lowercase SHA-256")
    return value


def _canonical_bytes(value: Any) -> bytes:
    try:
        return (
            json.dumps(
                value,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("structural context must be finite canonical JSON data") from exc


def _optional_token(value: Any) -> str | None:
    return None if value in _MISSING or value is None else str(value)


def _integer(value: Any, label: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an integer") from exc
    _require(str(result) == str(value).lstrip("+"), f"{label} must be an integer")
    return result


def _optional_integer(value: Any, label: str) -> int | None:
    return None if value in _MISSING or value is None else _integer(value, label)


def _number(value: Any, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _require(math.isfinite(result), f"{label} must be finite")
    return result


def _required_fields(row: dict[str, str], fields: set[str], label: str) -> None:
    missing = fields - set(row)
    _require(not missing, f"{label} lacks fields {sorted(missing)}")


def _validate_binding(value: Any, label: str) -> dict[str, str]:
    row = _exact(value, _BINDING_FIELDS, label)
    path = _text(row["path"], f"{label}.path")
    posix = PurePosixPath(path)
    windows = PureWindowsPath(path)
    _require(
        "\\" not in path
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and path == posix.as_posix()
        and "." not in posix.parts
        and ".." not in posix.parts,
        f"{label}.path must be a safe repository-relative POSIX path",
    )
    _sha(row["sha256"], f"{label}.sha256")
    return row


def _read_cif(path: Path) -> str:
    _require(path.is_file(), f"coordinate source is missing: {path}")
    try:
        if path.suffix.lower() == ".gz":
            with gzip.open(path, "rt", encoding="utf-8", errors="strict") as handle:
                return handle.read()
        return path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"coordinate source is not readable mmCIF: {path}") from exc


def _atlas_records(kernel: dict[str, Any]) -> list[dict[str, Any]]:
    records = kernel.get("follow_on_records")
    _require(isinstance(records, list), "Atlas-10 kernel lacks follow_on_records")
    _require(all(isinstance(row, dict) for row in records), "Atlas-10 records are invalid")
    return records


def _bound_record(
    kernel: dict[str, Any], *, case_id: str, record_id: str
) -> dict[str, Any]:
    matches = [
        row
        for row in _atlas_records(kernel)
        if row.get("case_id") == case_id and row.get("record_id") == record_id
    ]
    _require(len(matches) == 1, "Atlas-10 case/record binding is absent or ambiguous")
    record = matches[0]
    _require(
        record.get("object_type") == "mechanism_hypothesis"
        and record.get("evidence_tier") == 2,
        "structural context must bind an Atlas-10 Tier-2 mechanism hypothesis",
    )
    return record


def _bound_structure(record: dict[str, Any], pdb_id: str) -> dict[str, Any]:
    matches = [row for row in record.get("structures", []) if row.get("pdb_id") == pdb_id]
    _require(len(matches) == 1, "Atlas-10 structure binding is absent or ambiguous")
    return matches[0]


def _bound_site(
    record: dict[str, Any], *, site_id: str, pdb_id: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    sites = [row for row in record.get("sites", []) if row.get("site_id") == site_id]
    _require(len(sites) == 1, "Atlas-10 site mapping is absent or ambiguous")
    site = sites[0]
    mappings = [row for row in site.get("pdb_mappings", []) if row.get("pdb_id") == pdb_id]
    _require(len(mappings) == 1, "Atlas-10 site mapping is absent or ambiguous")
    return site, mappings[0]


def _atom_output(row: dict[str, str], *, requested: bool) -> dict[str, Any]:
    _required_fields(row, _ATOM_FIELDS, "_atom_site row")
    return {
        "atom_site_id": row["id"],
        "record_type": row["group_pdb"],
        "element": row["type_symbol"],
        "label_atom_id": row["label_atom_id"],
        "label_alt_id": _optional_token(row["label_alt_id"]),
        "label_component_id": row["label_comp_id"],
        "label_asym_id": row["label_asym_id"],
        "label_entity_id": row["label_entity_id"],
        "label_seq_id": _optional_integer(row["label_seq_id"], "atom label sequence ID"),
        "author_atom_id": row["auth_atom_id"],
        "author_component_id": row["auth_comp_id"],
        "author_chain_id": row["auth_asym_id"],
        "author_residue_number": _integer(row["auth_seq_id"], "atom author residue number"),
        "insertion_code": _optional_token(row["pdbx_pdb_ins_code"]),
        "model_id": _integer(row["pdbx_pdb_model_num"], "atom model ID"),
        "x": _number(row["cartn_x"], "atom x coordinate"),
        "y": _number(row["cartn_y"], "atom y coordinate"),
        "z": _number(row["cartn_z"], "atom z coordinate"),
        "occupancy": _number(row["occupancy"], "atom occupancy"),
        "b_iso_or_equiv": _number(row["b_iso_or_equiv"], "atom B factor"),
        "requested_for_distance": requested,
    }


def _residue_rows(
    atom_rows: list[dict[str, str]], site: dict[str, Any], mapping: dict[str, Any]
) -> list[dict[str, str]]:
    residue = _text(site.get("residue_name"), "Atlas-10 site residue name").upper()
    chain = _text(mapping.get("chain_id"), "Atlas-10 PDB chain")
    author_position = mapping.get("author_position")
    label_position = mapping.get("label_position")
    _require(type(author_position) is int and author_position > 0, "Atlas-10 author position is invalid")
    _require(type(label_position) is int and label_position > 0, "Atlas-10 label position is invalid")
    matches = []
    for row in atom_rows:
        _required_fields(
            row,
            {
                "label_comp_id",
                "label_seq_id",
                "auth_comp_id",
                "auth_asym_id",
                "auth_seq_id",
            },
            "_atom_site row",
        )
        if (
            row["auth_asym_id"] == chain
            and row["auth_comp_id"] == residue
            and _optional_integer(row["auth_seq_id"], "atom author position") == author_position
            and row["label_comp_id"] == residue
            and _optional_integer(row["label_seq_id"], "atom label position") == label_position
        ):
            matches.append(row)
    _require(matches, "Atlas-10 site mapping has no deposited atom rows")
    residue_instances = {
        (
            row.get("label_asym_id"),
            _optional_token(row.get("pdbx_pdb_ins_code")),
        )
        for row in matches
    }
    _require(
        len(residue_instances) == 1,
        "Atlas-10 site mapping resolves to ambiguous label-chain or insertion-code instances",
    )
    return matches


def _site_identity(mapping: dict[str, Any], site: dict[str, Any]) -> tuple[Any, ...]:
    return (
        mapping["pdb_id"],
        mapping["chain_id"],
        mapping["author_position"],
        mapping["label_position"],
        site["residue_name"].upper(),
    )


def _endpoint_matches_site(
    row: dict[str, str], side: int, site: dict[str, Any], mapping: dict[str, Any]
) -> bool:
    prefix = f"ptnr{side}_"
    label_seq = _optional_integer(row.get(prefix + "label_seq_id"), "connection label position")
    author_seq = _optional_integer(row.get(prefix + "auth_seq_id"), "connection author position")
    return (
        row.get(prefix + "label_comp_id") == site["residue_name"].upper()
        and row.get(prefix + "auth_comp_id") == site["residue_name"].upper()
        and row.get(prefix + "auth_asym_id") == mapping["chain_id"]
        and label_seq == mapping["label_position"]
        and author_seq == mapping["author_position"]
    )


def _connection_sides(row: dict[str, str]) -> list[int]:
    sides = []
    for side in (1, 2, 3):
        atom = row.get(f"ptnr{side}_label_atom_id")
        if atom is not None and atom not in _MISSING:
            sides.append(side)
    _require(len(sides) >= 2, "incident connection has fewer than two deposited endpoints")
    return sides


def _connection_endpoint(row: dict[str, str], side: int) -> dict[str, Any]:
    prefix = f"ptnr{side}_"
    required = {
        prefix + "label_asym_id",
        prefix + "label_atom_id",
        prefix + "label_comp_id",
        prefix + "label_seq_id",
        prefix + "auth_asym_id",
        prefix + "auth_comp_id",
        prefix + "auth_seq_id",
    }
    _required_fields(row, required, "_struct_conn row")
    return {
        "side": side,
        "label_asym_id": row[prefix + "label_asym_id"],
        "label_atom_id": row[prefix + "label_atom_id"],
        "label_component_id": row[prefix + "label_comp_id"],
        "label_seq_id": _optional_integer(row[prefix + "label_seq_id"], "connection label position"),
        "label_alt_id": _optional_token(row.get(f"pdbx_ptnr{side}_label_alt_id")),
        "author_chain_id": row[prefix + "auth_asym_id"],
        "author_component_id": row[prefix + "auth_comp_id"],
        "author_residue_number": _integer(row[prefix + "auth_seq_id"], "connection author position"),
        "insertion_code": _optional_token(row.get(f"pdbx_ptnr{side}_pdb_ins_code")),
        "symmetry": _optional_token(row.get(prefix + "symmetry")),
    }


def _endpoint_atom_rows(
    endpoint: dict[str, Any], atom_rows: list[dict[str, str]]
) -> list[dict[str, Any]]:
    matches = []
    for row in atom_rows:
        if (
            row.get("label_asym_id") == endpoint["label_asym_id"]
            and row.get("label_atom_id") == endpoint["label_atom_id"]
            and row.get("label_comp_id") == endpoint["label_component_id"]
            and _optional_integer(row.get("label_seq_id"), "endpoint atom label position")
            == endpoint["label_seq_id"]
            and row.get("auth_asym_id") == endpoint["author_chain_id"]
            and row.get("auth_comp_id") == endpoint["author_component_id"]
            and _optional_integer(row.get("auth_seq_id"), "endpoint atom author position")
            == endpoint["author_residue_number"]
            and _optional_token(row.get("pdbx_pdb_ins_code"))
            == endpoint["insertion_code"]
            and (
                endpoint["label_alt_id"] is None
                or _optional_token(row.get("label_alt_id")) == endpoint["label_alt_id"]
            )
        ):
            matches.append(_atom_output(row, requested=False))
    _require(matches, "connection endpoint does not resolve to deposited atom rows")
    return sorted(matches, key=_atom_sort_key)


def _atom_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["model_id"],
        row["label_asym_id"],
        row["label_seq_id"] if row["label_seq_id"] is not None else -1,
        row["label_atom_id"],
        row["label_alt_id"] or "",
        row["atom_site_id"],
    )


def _incident_connections(
    tables: dict[str, list[dict[str, str]]],
    selected: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output = []
    seen_ids: set[str] = set()
    for raw in tables["_struct_conn"]:
        connection_id = _text(raw.get("id"), "connection ID")
        _require(connection_id not in seen_ids, "deposited connection IDs repeat")
        seen_ids.add(connection_id)
        sides = _connection_sides(raw)
        incident = {
            item["site_id"]
            for item in selected
            for side in sides
            if _endpoint_matches_site(raw, side, item["atlas10_site"], item["pdb_mapping"])
        }
        if not incident:
            continue
        endpoints = []
        for side in sides:
            endpoint = _connection_endpoint(raw, side)
            endpoint_sites = sorted(
                item["site_id"]
                for item in selected
                if _endpoint_matches_site(raw, side, item["atlas10_site"], item["pdb_mapping"])
            )
            endpoints.append(
                {
                    **endpoint,
                    "selected_site_ids": endpoint_sites,
                    "atom_rows": _endpoint_atom_rows(endpoint, tables["_atom_site"]),
                }
            )
        distance = raw.get("pdbx_dist_value")
        output.append(
            {
                "connection_id": connection_id,
                "connection_type": _text(raw.get("conn_type_id"), "connection type"),
                "deposited_distance_angstrom": (
                    None if distance in _MISSING or distance is None else _number(distance, "connection distance")
                ),
                "source_bond_order_token": _optional_token(raw.get("pdbx_value_order")),
                "leaving_atom_flag": _optional_token(raw.get("pdbx_leaving_atom_flag")),
                "details": _optional_token(raw.get("details")),
                "incident_site_ids": sorted(incident),
                "endpoints": endpoints,
                "source_row": copy.deepcopy(raw),
                "interpretation_boundary": "deposited_connection_record_not_distance_inference",
            }
        )
    return sorted(output, key=lambda row: row["connection_id"])


def _modification_features(
    rows: list[dict[str, str]], selected: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        site_ids = []
        for item in selected:
            site = item["atlas10_site"]
            mapping = item["pdb_mapping"]
            if (
                row.get("modified_residue_label_comp_id") == site["residue_name"].upper()
                and row.get("modified_residue_auth_comp_id") == site["residue_name"].upper()
                and row.get("modified_residue_auth_asym_id") == mapping["chain_id"]
                and _optional_integer(
                    row.get("modified_residue_label_seq_id"),
                    "modification label position",
                )
                == mapping["label_position"]
                and _optional_integer(
                    row.get("modified_residue_auth_seq_id"),
                    "modification author position",
                )
                == mapping["author_position"]
            ):
                site_ids.append(item["site_id"])
        if site_ids:
            output.append(
                {
                    "feature_id": _text(row.get("ordinal"), "modification feature ordinal"),
                    "category": _optional_token(row.get("category")),
                    "component_id": _optional_token(row.get("label_comp_id")),
                    "selected_site_ids": sorted(site_ids),
                    "source_row": copy.deepcopy(row),
                }
            )
    return sorted(output, key=lambda row: row["feature_id"])


def _is_water_component(component_id: str, name: str) -> bool:
    return component_id.upper() in {"HOH", "DOD"} or name.strip().casefold() in {
        "water",
        "deuterated water",
    }


def _nonwater_nonpolymer_components(
    tables: dict[str, list[dict[str, str]]],
) -> list[dict[str, Any]]:
    entity_rows = {
        row.get("id"): row
        for row in tables["_entity"]
        if row.get("type") == "non-polymer" and row.get("id") not in _MISSING
    }
    component_rows = {row.get("id"): row for row in tables["_chem_comp"]}
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for atom in tables["_atom_site"]:
        entity_id = atom.get("label_entity_id")
        component_id = atom.get("label_comp_id")
        if entity_id in entity_rows and isinstance(component_id, str):
            grouped.setdefault((entity_id, component_id), []).append(atom)

    output = []
    for (entity_id, component_id), atoms in sorted(grouped.items()):
        entity = entity_rows[entity_id]
        component = component_rows.get(component_id)
        _require(component is not None, "nonpolymer component lacks _chem_comp identity")
        name = _text(component.get("name"), "nonpolymer component name")
        if _is_water_component(component_id, name):
            continue
        scheme_rows = [
            copy.deepcopy(row)
            for row in tables["_pdbx_nonpoly_scheme"]
            if row.get("entity_id") == entity_id and row.get("mon_id") == component_id
        ]
        _require(scheme_rows, "nonwater nonpolymer component lacks scheme rows")
        instance_groups: dict[tuple[Any, ...], list[dict[str, str]]] = {}
        for atom in atoms:
            key = (
                atom.get("label_asym_id"),
                atom.get("label_entity_id"),
                atom.get("label_comp_id"),
                _optional_integer(atom.get("label_seq_id"), "nonpolymer label position"),
                atom.get("auth_asym_id"),
                atom.get("auth_comp_id"),
                _integer(atom.get("auth_seq_id"), "nonpolymer author position"),
            )
            instance_groups.setdefault(key, []).append(atom)
        instances = []
        for key, instance_atoms in sorted(
            instance_groups.items(), key=lambda item: (item[0][0], item[0][4], item[0][6])
        ):
            instances.append(
                {
                    "label_asym_id": key[0],
                    "label_entity_id": key[1],
                    "label_component_id": key[2],
                    "label_seq_id": key[3],
                    "author_chain_id": key[4],
                    "author_component_id": key[5],
                    "author_residue_number": key[6],
                    "atom_rows": sorted(
                        [_atom_output(row, requested=False) for row in instance_atoms],
                        key=_atom_sort_key,
                    ),
                }
            )
        output.append(
            {
                "component_id": component_id,
                "component_name": name,
                "entity_id": entity_id,
                "entity_record": copy.deepcopy(entity),
                "component_record": copy.deepcopy(component),
                "nonpoly_scheme_rows": scheme_rows,
                "instances": instances,
                "interpretation_boundary": "deposited_nonpolymer_identity_not_biological_role",
            }
        )
    return output


def _distance_pairs(
    declarations: list[Any], selected: list[dict[str, Any]], context: str
) -> list[dict[str, Any]]:
    by_id = {row["site_id"]: row for row in selected}
    output = []
    pair_ids: set[str] = set()
    for index, raw in enumerate(declarations):
        label = f"{context}.declared_distance_pairs[{index}]"
        pair = _exact(raw, _PAIR_FIELDS, label)
        pair_id = _text(pair["pair_id"], f"{label}.pair_id")
        _require(pair_id not in pair_ids, f"{context} distance pair IDs repeat")
        pair_ids.add(pair_id)
        endpoints = {}
        for side in ("left", "right"):
            endpoint = _exact(pair[side], _PAIR_ENDPOINT_FIELDS, f"{label}.{side}")
            site_id = _text(endpoint["site_id"], f"{label}.{side}.site_id")
            atom_name = _text(endpoint["atom_name"], f"{label}.{side}.atom_name")
            site_row = by_id.get(site_id)
            _require(site_row is not None, f"distance endpoint site {site_id} is absent")
            _require(
                atom_name in site_row["requested_atom_names"],
                f"distance endpoint atom {site_id}:{atom_name} is absent from the selection",
            )
            atoms = [row for row in site_row["atom_rows"] if row["label_atom_id"] == atom_name]
            _require(atoms, f"distance endpoint atom {site_id}:{atom_name} is absent")
            endpoints[side] = (endpoint, site_row, atoms)

        left_endpoint, left_site, left_atoms = endpoints["left"]
        right_endpoint, right_site, right_atoms = endpoints["right"]
        same_residue = _site_identity(
            left_site["pdb_mapping"], left_site["atlas10_site"]
        ) == _site_identity(right_site["pdb_mapping"], right_site["atlas10_site"])
        measurements = []
        for left in left_atoms:
            for right in right_atoms:
                if left["model_id"] != right["model_id"]:
                    continue
                left_alt = left["label_alt_id"]
                right_alt = right["label_alt_id"]
                if same_residue and left_alt and right_alt and left_alt != right_alt:
                    continue
                if same_residue:
                    coexistence = "compatible_within_same_residue"
                elif left_alt is None and right_alt is None:
                    coexistence = "no_explicit_alternate_labels"
                else:
                    coexistence = "cross_residue_alternate_coexistence_unresolved"
                distance = math.dist(
                    (left["x"], left["y"], left["z"]),
                    (right["x"], right["y"], right["z"]),
                )
                _require(math.isfinite(distance), "derived atom distance must be finite")
                measurements.append(
                    {
                        "measurement_id": (
                            f"{pair_id}:model-{left['model_id']}:"
                            f"{left['atom_site_id']}--{right['atom_site_id']}"
                        ),
                        "model_id": left["model_id"],
                        "left_atom_site_id": left["atom_site_id"],
                        "right_atom_site_id": right["atom_site_id"],
                        "left_label_alt_id": left_alt,
                        "right_label_alt_id": right_alt,
                        "left_occupancy": left["occupancy"],
                        "right_occupancy": right["occupancy"],
                        "alternate_coexistence": coexistence,
                        "distance_angstrom": round(distance, 6),
                    }
                )
        _require(measurements, f"distance pair {pair_id} has no model-compatible atom rows")
        output.append(
            {
                "pair_id": pair_id,
                "left": copy.deepcopy(left_endpoint),
                "right": copy.deepcopy(right_endpoint),
                "measurement_semantics": "all_deposited_model_and_compatible_alternate_combinations_no_preferred_or_averaged_distance",
                "measurements": sorted(
                    measurements,
                    key=lambda row: (
                        row["model_id"],
                        row["left_atom_site_id"],
                        row["right_atom_site_id"],
                    ),
                ),
            }
        )
    return output


def _build_context(
    declaration: Any,
    *,
    index: int,
    atlas10_kernel: dict[str, Any],
    coordinate_path: Path,
    atlas10_binding: dict[str, str],
) -> dict[str, Any]:
    label = f"structures[{index}]"
    row = _exact(declaration, _STRUCTURE_FIELDS, label)
    context_id = _text(row["context_id"], f"{label}.context_id")
    case_id = _text(row["case_id"], f"{label}.case_id")
    record_id = _text(row["record_id"], f"{label}.record_id")
    pdb_id = _text(row["pdb_id"], f"{label}.pdb_id").upper()
    _require(_PDB_RE.fullmatch(pdb_id) is not None and row["pdb_id"] == pdb_id, f"{label}.pdb_id is invalid")
    coordinate_binding = _validate_binding(row["coordinate_binding"], f"{label}.coordinate_binding")
    _require(
        canonical_file_sha256(coordinate_path) == coordinate_binding["sha256"],
        "coordinate binding hash differs",
    )
    record = _bound_record(atlas10_kernel, case_id=case_id, record_id=record_id)
    structure = _bound_structure(record, pdb_id)
    tables = parse_mmcif_categories(_read_cif(coordinate_path), categories=_PARSED_CATEGORIES)
    entry_ids = {entry.get("id") for entry in tables["_entry"]}
    _require(entry_ids == {pdb_id}, "coordinate entry ID differs from selected PDB ID")

    selected = []
    seen_sites: set[str] = set()
    selected_atom_site_ids: set[str] = set()
    selected_atom_identities: set[tuple[Any, ...]] = set()
    deposited_models = {
        _integer(atom.get("pdbx_pdb_model_num"), "deposited model ID")
        for atom in tables["_atom_site"]
    }
    for site_index, raw_site in enumerate(_array(row["selected_sites"], f"{label}.selected_sites", nonempty=True)):
        site_label = f"{label}.selected_sites[{site_index}]"
        selection = _exact(raw_site, _SITE_SELECTION_FIELDS, site_label)
        site_id = _text(selection["site_id"], f"{site_label}.site_id")
        _require(site_id not in seen_sites, f"{label} selected site IDs repeat")
        seen_sites.add(site_id)
        atom_names = _array(selection["atom_names"], f"{site_label}.atom_names", nonempty=True)
        _require(
            all(isinstance(name, str) and bool(name.strip()) for name in atom_names)
            and len(atom_names) == len(set(atom_names)),
            f"{site_label}.atom_names must be unique nonempty strings",
        )
        site, mapping = _bound_site(record, site_id=site_id, pdb_id=pdb_id)
        residue_rows = _residue_rows(tables["_atom_site"], site, mapping)
        observed_names = {atom["label_atom_id"] for atom in residue_rows}
        missing = set(atom_names) - observed_names
        _require(not missing, f"selected atom {site_id}:{sorted(missing)} is absent")
        models = {
            _integer(atom["pdbx_pdb_model_num"], "selected-site model ID")
            for atom in residue_rows
        }
        _require(
            models == deposited_models,
            f"selected site {site_id} does not cover every deposited model",
        )
        for model_id in models:
            model_names = {
                atom["label_atom_id"]
                for atom in residue_rows
                if _integer(atom["pdbx_pdb_model_num"], "selected-site model ID") == model_id
            }
            _require(
                set(atom_names) <= model_names,
                f"selected atom {site_id} is incomplete in model {model_id}",
            )
        for atom in residue_rows:
            atom_site_id = _text(atom.get("id"), "selected atom-site ID")
            _require(
                atom_site_id not in selected_atom_site_ids,
                "selected residue atom-site IDs repeat",
            )
            selected_atom_site_ids.add(atom_site_id)
            identity = (
                _integer(atom.get("pdbx_pdb_model_num"), "selected atom model ID"),
                atom.get("label_asym_id"),
                _optional_integer(atom.get("label_seq_id"), "selected atom label position"),
                atom.get("label_atom_id"),
                _optional_token(atom.get("label_alt_id")),
                _optional_token(atom.get("pdbx_pdb_ins_code")),
            )
            _require(
                identity not in selected_atom_identities,
                "selected residue atom identity repeats",
            )
            selected_atom_identities.add(identity)
        selected.append(
            {
                "site_id": site_id,
                "requested_atom_names": copy.deepcopy(atom_names),
                "atlas10_site": copy.deepcopy(site),
                "pdb_mapping": copy.deepcopy(mapping),
                "atom_rows": sorted(
                    [
                        _atom_output(atom, requested=atom["label_atom_id"] in atom_names)
                        for atom in residue_rows
                    ],
                    key=_atom_sort_key,
                ),
            }
        )

    interpretation = _object(row["interpretation"], f"{label}.interpretation")
    return {
        "context_id": context_id,
        "case_id": case_id,
        "record_id": record_id,
        "pdb_id": pdb_id,
        "source_bindings": {
            "atlas10": copy.deepcopy(atlas10_binding),
            "coordinate": copy.deepcopy(coordinate_binding),
        },
        "atlas10_structure": copy.deepcopy(structure),
        "sites": selected,
        "distance_pairs": _distance_pairs(row["declared_distance_pairs"], selected, label),
        "incident_connections": _incident_connections(tables, selected),
        "modification_features": _modification_features(
            tables["_pdbx_modification_feature"], selected
        ),
        "nonwater_nonpolymer_components": _nonwater_nonpolymer_components(tables),
        "deposited_metadata": {
            "entry_records": copy.deepcopy(tables["_entry"]),
            "structure_records": copy.deepcopy(tables["_struct"]),
            "crystal_growth_records": copy.deepcopy(tables["_exptl_crystal_grow"]),
        },
        "interpretation": copy.deepcopy(interpretation),
        "claim_boundary": {
            "source_facts": "deposited rows and direct Euclidean distances bound to retained coordinate bytes",
            "reviewed_interpretation": "separate declared interpretation; not inferred by the extractor",
            "does_not_support": [
                "preferred or conformer-averaged geometry",
                "cross-residue alternate-state populations",
                "covalency inferred from distance",
                "productive protonation, transition-state geometry, activity, or design competence",
            ],
        },
    }


def build_structural_context(
    spec: dict[str, Any],
    *,
    atlas10_kernel: dict[str, Any],
    coordinate_paths: Mapping[str, Path],
) -> dict[str, Any]:
    """Build a deterministic structural-context bundle from declared selections."""

    top = _exact(spec, _SPEC_FIELDS, "structural-context spec")
    _require(top["schema_version"] == SPEC_SCHEMA_VERSION, "unsupported structural-context spec")
    bundle_id = _text(top["bundle_id"], "bundle_id")
    atlas_binding = _validate_binding(top["atlas10_binding"], "atlas10_binding")
    _require(
        hashlib.sha256(_canonical_bytes(atlas10_kernel)).hexdigest() == atlas_binding["sha256"],
        "Atlas-10 binding hash differs",
    )
    _canonical_bytes(spec)
    declarations = _array(top["structures"], "structures", nonempty=True)
    _require(isinstance(coordinate_paths, Mapping), "coordinate_paths must be a mapping")
    contexts = []
    context_ids: set[str] = set()
    pdb_ids: set[str] = set()
    for index, declaration in enumerate(declarations):
        raw = _object(declaration, f"structures[{index}]")
        pdb_id = _text(raw.get("pdb_id"), f"structures[{index}].pdb_id").upper()
        coordinate_path = coordinate_paths.get(pdb_id)
        _require(isinstance(coordinate_path, Path), f"coordinate path for {pdb_id} is missing")
        context = _build_context(
            declaration,
            index=index,
            atlas10_kernel=atlas10_kernel,
            coordinate_path=coordinate_path,
            atlas10_binding=atlas_binding,
        )
        _require(context["context_id"] not in context_ids, "structural context IDs repeat")
        context_ids.add(context["context_id"])
        _require(context["pdb_id"] not in pdb_ids, "structural context PDB IDs repeat")
        pdb_ids.add(context["pdb_id"])
        contexts.append(context)
    bundle = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "bundle_id": bundle_id,
        "spec_payload_sha256": hashlib.sha256(_canonical_bytes(spec)).hexdigest(),
        "atlas10_binding": copy.deepcopy(atlas_binding),
        "context_count": len(contexts),
        "site_count": sum(len(context["sites"]) for context in contexts),
        "distance_pair_count": sum(len(context["distance_pairs"]) for context in contexts),
        "distance_measurement_count": sum(
            len(pair["measurements"])
            for context in contexts
            for pair in context["distance_pairs"]
        ),
        "structures": contexts,
        "bundle_semantics": {
            "distance_selection": "none_all_compatible_deposited_combinations_retained",
            "alternate_policy": "same_residue_distinct_nonmissing_alt_ids_excluded_cross_residue_coexistence_unresolved",
            "connection_policy": "all_deposited_connections_incident_on_any_atom_of_each_selected_residue",
            "empty_connection_policy": "no_matching_deposited_row_not_evidence_of_physical_noncovalency",
            "nonpolymer_policy": "all_deposited_nonwater_nonpolymer_components_retained_without_role_inference",
        },
    }
    _canonical_bytes(bundle)
    return bundle


def _safe_bound_path(repo_root: Path, relative: str, label: str) -> Path:
    posix = PurePosixPath(relative)
    windows = PureWindowsPath(relative)
    _require(
        "\\" not in relative
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and relative == posix.as_posix()
        and "." not in posix.parts
        and ".." not in posix.parts,
        f"{label} must be a safe repository-relative POSIX path",
    )
    path = (repo_root / Path(posix)).resolve()
    _require(repo_root == path or repo_root in path.parents, f"{label} escapes repository root")
    _require(path.is_file(), f"{label} is missing")
    return path


def load_and_build_structural_context(
    spec_path: Path, kernel_path: Path, repo_root: Path
) -> dict[str, Any]:
    """Load a repository-bound spec and build its structural-context bundle."""

    repo_root = repo_root.resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    atlas_binding = _validate_binding(spec.get("atlas10_binding"), "atlas10_binding")
    expected_kernel = _safe_bound_path(repo_root, atlas_binding["path"], "Atlas-10 binding path")
    _require(kernel_path.resolve() == expected_kernel, "kernel path differs from Atlas-10 binding")
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    coordinate_paths: dict[str, Path] = {}
    for index, declaration in enumerate(_array(spec.get("structures"), "structures", nonempty=True)):
        row = _object(declaration, f"structures[{index}]")
        pdb_id = _text(row.get("pdb_id"), f"structures[{index}].pdb_id").upper()
        binding = _validate_binding(row.get("coordinate_binding"), f"structures[{index}].coordinate_binding")
        _require(pdb_id not in coordinate_paths, "structural context PDB IDs repeat")
        coordinate_paths[pdb_id] = _safe_bound_path(
            repo_root, binding["path"], f"coordinate binding path for {pdb_id}"
        )
    return build_structural_context(
        spec,
        atlas10_kernel=kernel,
        coordinate_paths=coordinate_paths,
    )


def query_structural_context(
    bundle: dict[str, Any],
    *,
    case_id: str | None = None,
    pdb_id: str | None = None,
    site_id: str | None = None,
) -> dict[str, Any]:
    """Filter contexts while retaining each matching context as a complete unit."""

    _require(bundle.get("schema_version") == BUNDLE_SCHEMA_VERSION, "unsupported structural-context bundle")
    for value, label in ((case_id, "case_id"), (pdb_id, "pdb_id"), (site_id, "site_id")):
        _require(value is None or (isinstance(value, str) and bool(value.strip())), f"{label} filter must be nonempty text")
    normalized_pdb = pdb_id.upper() if pdb_id is not None else None
    contexts = []
    for context in _array(bundle.get("structures"), "bundle structures"):
        if case_id is not None and context.get("case_id") != case_id:
            continue
        if normalized_pdb is not None and context.get("pdb_id") != normalized_pdb:
            continue
        if site_id is not None and site_id not in {row.get("site_id") for row in context.get("sites", [])}:
            continue
        contexts.append(copy.deepcopy(context))
    return {
        "schema_version": QUERY_SCHEMA_VERSION,
        "bundle_id": bundle.get("bundle_id"),
        "filters": {"case_id": case_id, "pdb_id": normalized_pdb, "site_id": site_id},
        "context_count": len(contexts),
        "structures": contexts,
        "query_semantics": {
            "matching_context_retained_complete": True,
            "site_filter_does_not_prune_sibling_sites_or_interpretation": True,
            "empty_result": "no_matching_packaged_context_not_absence_of_structure_or_catalysis",
        },
    }
