"""Project operator-qualified biological-assembly coordinate context.

The projector expands only assembly copies explicitly declared by the mmCIF
assembly tables. A data specification selects deposited residue instances,
operator paths, atoms, and distance pairs. Every selected atom retains its
deposited identity, model, alternate identifier, occupancy, and both deposited
and transformed coordinates. Distances are geometric candidates; they do not
establish bonds, protonation, or joint alternate-state populations.
"""

from __future__ import annotations

import copy
from itertools import product
import json
import math
import re
from typing import Any

from .atlas_primary_source_check import parse_mmcif_categories


SCHEMA_VERSION = "catalytic-earth.atlas-assembly-context.v1"

_MISSING = {".", "?"}
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.]+$")
_RANGE_RE = re.compile(r"^([0-9]+)-([0-9]+)$")
_MAX_OPERATOR_PATHS = 10_000
_SPEC_FIELDS = {"pdb_id", "assembly_id", "selections", "distance_pairs"}
_SELECTION_FIELDS = {
    "selection_id",
    "operator_ids",
    "model_id",
    "label_asym_id",
    "auth_seq_id",
    "label_comp_id",
    "atom_names",
}
_PAIR_FIELDS = {"pair_id", "left_selection_id", "right_selection_id"}
_CATEGORIES = frozenset(
    {
        "_atom_site",
        "_entry",
        "_pdbx_struct_assembly",
        "_pdbx_struct_assembly_auth_evidence",
        "_pdbx_struct_assembly_gen",
        "_pdbx_struct_oper_list",
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
_OPERATOR_FIELDS = {
    "id",
    "matrix[1][1]",
    "matrix[1][2]",
    "matrix[1][3]",
    "matrix[2][1]",
    "matrix[2][2]",
    "matrix[2][3]",
    "matrix[3][1]",
    "matrix[3][2]",
    "matrix[3][3]",
    "vector[1]",
    "vector[2]",
    "vector[3]",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
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
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{label} must be nonempty text",
    )
    return value


def _optional_token(value: Any) -> str | None:
    return None if value in _MISSING or value is None else str(value)


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


def _expand_operator_group(group: str, label: str) -> list[str]:
    _require(group, f"{label} has an empty operator group")
    output: list[str] = []
    for item in group.split(","):
        _require(item, f"{label} has an empty operator ID")
        match = _RANGE_RE.fullmatch(item)
        if match is not None:
            start, end = (int(value) for value in match.groups())
            _require(start <= end, f"{label} has a descending operator range")
            _require(
                len(output) + end - start + 1 <= _MAX_OPERATOR_PATHS,
                f"{label} expands beyond {_MAX_OPERATOR_PATHS} operators",
            )
            output.extend(str(value) for value in range(start, end + 1))
        else:
            _require(
                _TOKEN_RE.fullmatch(item) is not None,
                f"{label} has unsupported operator grammar",
            )
            output.append(item)
        _require(
            len(output) <= _MAX_OPERATOR_PATHS,
            f"{label} expands beyond {_MAX_OPERATOR_PATHS} operators",
        )
    _require(len(output) == len(set(output)), f"{label} repeats an operator ID")
    return output


def _expand_oper_expression(expression: Any, label: str) -> list[tuple[str, ...]]:
    text = "".join(_text(expression, label).split())
    if "(" in text or ")" in text:
        matches = list(re.finditer(r"\(([^()]*)\)", text))
        _require(
            matches and "".join(match.group(0) for match in matches) == text,
            f"{label} has unsupported product grammar",
        )
        groups = [
            _expand_operator_group(match.group(1), label) for match in matches
        ]
    else:
        groups = [_expand_operator_group(text, label)]
    count = 1
    for group in groups:
        count *= len(group)
        _require(
            count <= _MAX_OPERATOR_PATHS,
            f"{label} expands beyond {_MAX_OPERATOR_PATHS} operator paths",
        )
    paths = [tuple(path) for path in product(*groups)]
    _require(len(paths) == len(set(paths)), f"{label} repeats an operator path")
    return paths


def _asym_ids(value: Any, label: str) -> list[str]:
    text = _text(value, label)
    result = [item.strip() for item in text.split(",")]
    _require(
        all(result) and len(result) == len(set(result)),
        f"{label} must contain unique nonempty asym IDs",
    )
    return result


def _operator_transform(row: dict[str, str]) -> dict[str, Any]:
    _required_fields(row, _OPERATOR_FIELDS, "_pdbx_struct_oper_list row")
    operator_id = _text(row["id"], "operator ID")
    _require(
        _TOKEN_RE.fullmatch(operator_id) is not None,
        "operator ID has unsupported syntax",
    )
    matrix = [
        [
            _number(
                row[f"matrix[{axis}][{column}]"], "operator matrix value"
            )
            for column in (1, 2, 3)
        ]
        for axis in (1, 2, 3)
    ]
    vector = [
        _number(row[f"vector[{axis}]"], "operator vector value")
        for axis in (1, 2, 3)
    ]
    return {"operator_id": operator_id, "matrix": matrix, "vector": vector}


def _apply_operator(point: list[float], transform: dict[str, Any]) -> list[float]:
    matrix = transform["matrix"]
    vector = transform["vector"]
    output = [
        sum(matrix[axis][column] * point[column] for column in range(3))
        + vector[axis]
        for axis in range(3)
    ]
    _require(
        all(math.isfinite(value) for value in output),
        "transformed coordinate is not finite",
    )
    return [0.0 if value == 0.0 else value for value in output]


def _transform_point(
    point: list[float],
    operator_ids: tuple[str, ...],
    transforms: dict[str, dict[str, Any]],
) -> list[float]:
    output = point
    # wwPDB products are written in composition order: the rightmost operator
    # acts first, e.g. (1)(2) means operator 2 followed by operator 1.
    for operator_id in reversed(operator_ids):
        output = _apply_operator(output, transforms[operator_id])
    return output


def _residue_identity(row: dict[str, str]) -> tuple[str | None, ...]:
    return (
        row["label_asym_id"],
        row["label_entity_id"],
        row["label_comp_id"],
        _optional_token(row["label_seq_id"]),
        row["auth_asym_id"],
        row["auth_comp_id"],
        row["auth_seq_id"],
        _optional_token(row["pdbx_pdb_ins_code"]),
        row["pdbx_pdb_model_num"],
    )


def _residue_output(identity: tuple[str | None, ...]) -> dict[str, Any]:
    return {
        "label_asym_id": identity[0],
        "label_entity_id": identity[1],
        "label_component_id": identity[2],
        "label_seq_id": identity[3],
        "author_chain_id": identity[4],
        "author_component_id": identity[5],
        "author_residue_number": identity[6],
        "insertion_code": identity[7],
        "model_id": identity[8],
    }


def _atom_output(
    row: dict[str, str],
    *,
    pdb_id: str,
    assembly_id: str,
    selection_id: str,
    operator_ids: tuple[str, ...],
    transforms: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    _required_fields(row, _ATOM_FIELDS, "_atom_site row")
    deposited_xyz = [
        _number(row["cartn_x"], "atom x coordinate"),
        _number(row["cartn_y"], "atom y coordinate"),
        _number(row["cartn_z"], "atom z coordinate"),
    ]
    occupancy = _number(row["occupancy"], "atom occupancy")
    _require(
        0.0 <= occupancy <= 1.0,
        "atom occupancy must be between zero and one",
    )
    atom_site_id = _text(row["id"], "atom-site ID")
    path = "+".join(operator_ids)
    return {
        "atom_instance_id": (
            f"{pdb_id}:assembly-{assembly_id}:operators-{path}:"
            f"model-{row['pdbx_pdb_model_num']}:atom-site-{atom_site_id}"
        ),
        "selection_id": selection_id,
        "assembly_id": assembly_id,
        "operator_ids": list(operator_ids),
        "atom_site_id": atom_site_id,
        "record_type": row["group_pdb"],
        "element": row["type_symbol"],
        "label_atom_id": row["label_atom_id"],
        "label_alt_id": _optional_token(row["label_alt_id"]),
        "label_component_id": row["label_comp_id"],
        "label_asym_id": row["label_asym_id"],
        "label_entity_id": row["label_entity_id"],
        "label_seq_id": _optional_token(row["label_seq_id"]),
        "author_atom_id": row["auth_atom_id"],
        "author_component_id": row["auth_comp_id"],
        "author_chain_id": row["auth_asym_id"],
        "author_residue_number": row["auth_seq_id"],
        "insertion_code": _optional_token(row["pdbx_pdb_ins_code"]),
        "model_id": row["pdbx_pdb_model_num"],
        "occupancy": occupancy,
        "b_iso_or_equiv": _number(row["b_iso_or_equiv"], "atom B factor"),
        "formal_charge": _optional_token(row.get("pdbx_formal_charge")),
        "deposited_xyz": deposited_xyz,
        "transformed_xyz": _transform_point(
            deposited_xyz, operator_ids, transforms
        ),
    }


def _project_selection(
    value: Any,
    *,
    index: int,
    pdb_id: str,
    assembly_id: str,
    generated_instances: dict[tuple[str, tuple[str, ...]], int],
    atom_rows: list[dict[str, str]],
    transforms: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    label = f"selections[{index}]"
    row = _exact(value, _SELECTION_FIELDS, label)
    selection_id = _text(row["selection_id"], f"{label}.selection_id")
    operator_values = _array(row["operator_ids"], f"{label}.operator_ids")
    _require(operator_values, f"{label}.operator_ids must be nonempty")
    _require(
        all(
            isinstance(item, str) and _TOKEN_RE.fullmatch(item)
            for item in operator_values
        ),
        f"{label}.operator_ids contain an invalid ID",
    )
    operator_ids = tuple(operator_values)
    label_asym_id = _text(row["label_asym_id"], f"{label}.label_asym_id")
    count = generated_instances.get((label_asym_id, operator_ids), 0)
    _require(count > 0, f"{label} is not generated in the declared assembly")
    _require(count == 1, f"{label} has ambiguous assembly generation")
    for operator_id in operator_ids:
        _require(
            operator_id in transforms,
            f"{label} references an absent operator ID",
        )

    model_id = _text(row["model_id"], f"{label}.model_id")
    auth_seq_id = _text(row["auth_seq_id"], f"{label}.auth_seq_id")
    label_comp_id = _text(row["label_comp_id"], f"{label}.label_comp_id")
    atom_names = _array(row["atom_names"], f"{label}.atom_names")
    _require(
        atom_names
        and all(
            isinstance(item, str) and bool(item.strip()) for item in atom_names
        )
        and len(atom_names) == len(set(atom_names)),
        f"{label}.atom_names must be unique nonempty strings",
    )
    candidates = []
    for atom in atom_rows:
        _required_fields(atom, _ATOM_FIELDS, "_atom_site row")
        if (
            atom["label_asym_id"] == label_asym_id
            and atom["label_comp_id"] == label_comp_id
            and atom["auth_seq_id"] == auth_seq_id
            and atom["pdbx_pdb_model_num"] == model_id
        ):
            candidates.append(atom)
    _require(candidates, f"{label} has no deposited residue rows")
    identities = {_residue_identity(atom) for atom in candidates}
    _require(
        len(identities) == 1,
        f"{label} resolves to ambiguous deposited residue identities",
    )
    identity = next(iter(identities))
    selected_atoms = [
        atom for atom in candidates if atom["label_atom_id"] in atom_names
    ]
    observed_names = {atom["label_atom_id"] for atom in selected_atoms}
    _require(
        observed_names == set(atom_names),
        f"{label} lacks selected atoms "
        f"{sorted(set(atom_names) - observed_names)}",
    )
    atom_site_ids = [atom["id"] for atom in selected_atoms]
    _require(
        len(atom_site_ids) == len(set(atom_site_ids)),
        f"{label} repeats atom-site IDs",
    )
    atom_identities = [
        (atom["label_atom_id"], _optional_token(atom["label_alt_id"]))
        for atom in selected_atoms
    ]
    _require(
        len(atom_identities) == len(set(atom_identities)),
        f"{label} repeats deposited atom identities",
    )
    name_order = {name: position for position, name in enumerate(atom_names)}
    selected_atoms.sort(
        key=lambda atom: (
            name_order[atom["label_atom_id"]],
            _optional_token(atom["label_alt_id"]) or "",
            atom["id"],
        )
    )
    atoms = [
        _atom_output(
            atom,
            pdb_id=pdb_id,
            assembly_id=assembly_id,
            selection_id=selection_id,
            operator_ids=operator_ids,
            transforms=transforms,
        )
        for atom in selected_atoms
    ]
    residue = _residue_output(identity)
    residue_path = "+".join(operator_ids)
    return {
        "selection_id": selection_id,
        "operator_ids": list(operator_ids),
        "operation_application_order": list(reversed(operator_ids)),
        "requested_atom_names": copy.deepcopy(atom_names),
        "operator_qualified_residue_id": (
            f"{pdb_id}:assembly-{assembly_id}:operators-{residue_path}:"
            f"model-{model_id}:label-{residue['label_asym_id']}:"
            f"{residue['label_component_id']}-{residue['label_seq_id']}:"
            f"author-{residue['author_chain_id']}:"
            f"{residue['author_component_id']}-"
            f"{residue['author_residue_number']}:"
            f"ins-{residue['insertion_code']}"
        ),
        "residue_identity": residue,
        "atoms": atoms,
        "scope": (
            "operator-qualified generated coordinate copy; "
            "no new deposited atom"
        ),
    }


def _distance_pairs(
    declarations: list[Any], selections: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_id = {selection["selection_id"]: selection for selection in selections}
    output = []
    seen: set[str] = set()
    for index, value in enumerate(declarations):
        label = f"distance_pairs[{index}]"
        row = _exact(value, _PAIR_FIELDS, label)
        pair_id = _text(row["pair_id"], f"{label}.pair_id")
        _require(pair_id not in seen, "distance pair IDs repeat")
        seen.add(pair_id)
        left_id = _text(
            row["left_selection_id"], f"{label}.left_selection_id"
        )
        right_id = _text(
            row["right_selection_id"], f"{label}.right_selection_id"
        )
        _require(left_id in by_id, f"{label} left selection is absent")
        _require(right_id in by_id, f"{label} right selection is absent")
        left = by_id[left_id]
        right = by_id[right_id]
        _require(
            left["residue_identity"]["model_id"]
            == right["residue_identity"]["model_id"],
            f"{label} crosses deposited models",
        )
        same_residue = (
            left["operator_qualified_residue_id"]
            == right["operator_qualified_residue_id"]
        )
        measurements = []
        for left_atom in left["atoms"]:
            for right_atom in right["atoms"]:
                left_alt = left_atom["label_alt_id"]
                right_alt = right_atom["label_alt_id"]
                if same_residue and left_alt and right_alt and left_alt != right_alt:
                    continue
                if same_residue:
                    coexistence = "compatible_within_same_generated_residue"
                elif left_alt is None and right_alt is None:
                    coexistence = "no_explicit_alternate_labels"
                else:
                    coexistence = (
                        "cross_residue_or_copy_alternate_coexistence_unresolved"
                    )
                distance = math.dist(
                    left_atom["transformed_xyz"],
                    right_atom["transformed_xyz"],
                )
                _require(
                    math.isfinite(distance),
                    "derived assembly distance is not finite",
                )
                measurements.append(
                    {
                        "measurement_id": f"{pair_id}:{len(measurements) + 1}",
                        "model_id": left_atom["model_id"],
                        "left_atom_instance_id": left_atom["atom_instance_id"],
                        "right_atom_instance_id": right_atom["atom_instance_id"],
                        "left_atom_site_id": left_atom["atom_site_id"],
                        "right_atom_site_id": right_atom["atom_site_id"],
                        "left_label_atom_id": left_atom["label_atom_id"],
                        "right_label_atom_id": right_atom["label_atom_id"],
                        "left_label_alt_id": left_alt,
                        "right_label_alt_id": right_alt,
                        "left_occupancy": left_atom["occupancy"],
                        "right_occupancy": right_atom["occupancy"],
                        "alternate_coexistence": coexistence,
                        "distance_angstrom": round(distance, 6),
                    }
                )
        _require(
            measurements,
            f"{label} has no alternate-compatible atom pairs",
        )
        output.append(
            {
                "pair_id": pair_id,
                "left_selection_id": left_id,
                "right_selection_id": right_id,
                "measurement_semantics": (
                    "all model-matched, alternate-compatible selected atom "
                    "combinations; cross-residue or copy joint state unresolved"
                ),
                "measurements": measurements,
            }
        )
    return output


def project_assembly(cif_text: str, spec: dict[str, Any]) -> dict[str, Any]:
    """Project selected atoms and distances into one biological assembly."""

    _require(isinstance(cif_text, str), "mmCIF source must be text")
    top = _exact(spec, _SPEC_FIELDS, "assembly projection spec")
    pdb_id = _text(top["pdb_id"], "pdb_id")
    _require(pdb_id == pdb_id.upper(), "pdb_id must be uppercase")
    assembly_id = _text(top["assembly_id"], "assembly_id")
    tables = parse_mmcif_categories(cif_text, categories=_CATEGORIES)
    entries = [row for row in tables["_entry"] if row.get("id") == pdb_id]
    _require(
        len(entries) == 1 and len(tables["_entry"]) == 1,
        "PDB entry ID differs",
    )
    deposited_atom_site_ids = [
        _text(row.get("id"), "deposited atom-site ID")
        for row in tables["_atom_site"]
    ]
    _require(
        len(deposited_atom_site_ids) == len(set(deposited_atom_site_ids)),
        "deposited atom-site IDs are ambiguous",
    )

    assembly_rows = [
        row
        for row in tables["_pdbx_struct_assembly"]
        if row.get("id") == assembly_id
    ]
    _require(len(assembly_rows) == 1, "assembly ID is absent or ambiguous")
    generation_rows = [
        row
        for row in tables["_pdbx_struct_assembly_gen"]
        if row.get("assembly_id") == assembly_id
    ]
    _require(generation_rows, "assembly has no generation rows")

    operator_rows: dict[str, dict[str, str]] = {}
    operator_transforms: dict[str, dict[str, Any]] = {}
    for raw in tables["_pdbx_struct_oper_list"]:
        transform = _operator_transform(raw)
        operator_id = transform["operator_id"]
        _require(operator_id not in operator_rows, "operator IDs are ambiguous")
        operator_rows[operator_id] = raw
        operator_transforms[operator_id] = transform

    parsed_generation = []
    generated_instances: dict[tuple[str, tuple[str, ...]], int] = {}
    referenced_operator_ids: set[str] = set()
    for index, raw in enumerate(generation_rows):
        _required_fields(
            raw,
            {"assembly_id", "oper_expression", "asym_id_list"},
            "_pdbx_struct_assembly_gen row",
        )
        paths = _expand_oper_expression(
            raw["oper_expression"],
            f"assembly generation row {index} operator expression",
        )
        asym_ids = _asym_ids(
            raw["asym_id_list"],
            f"assembly generation row {index} asym IDs",
        )
        for path in paths:
            for operator_id in path:
                _require(
                    operator_id in operator_transforms,
                    "assembly generation references an absent operator ID",
                )
                referenced_operator_ids.add(operator_id)
            for asym_id in asym_ids:
                key = (asym_id, path)
                generated_instances[key] = generated_instances.get(key, 0) + 1
        parsed_generation.append(
            {
                "source_row": copy.deepcopy(raw),
                "asym_ids": asym_ids,
                "operator_paths": [list(path) for path in paths],
            }
        )

    selections = [
        _project_selection(
            value,
            index=index,
            pdb_id=pdb_id,
            assembly_id=assembly_id,
            generated_instances=generated_instances,
            atom_rows=tables["_atom_site"],
            transforms=operator_transforms,
        )
        for index, value in enumerate(_array(top["selections"], "selections"))
    ]
    selection_ids = [selection["selection_id"] for selection in selections]
    _require(
        len(selection_ids) == len(set(selection_ids)),
        "selection IDs repeat",
    )
    result = {
        "schema_version": SCHEMA_VERSION,
        "pdb_id": pdb_id,
        "assembly_id": assembly_id,
        "deposited_metadata": {
            "assembly_record": copy.deepcopy(assembly_rows[0]),
            "assembly_generation_records": copy.deepcopy(generation_rows),
            "assembly_author_evidence_records": copy.deepcopy(
                [
                    row
                    for row in tables[
                        "_pdbx_struct_assembly_auth_evidence"
                    ]
                    if row.get("assembly_id") == assembly_id
                ]
            ),
            "operator_records": [
                copy.deepcopy(operator_rows[operator_id])
                for operator_id in operator_rows
                if operator_id in referenced_operator_ids
            ],
        },
        "generation_rules": parsed_generation,
        "operator_transforms": [
            copy.deepcopy(operator_transforms[operator_id])
            for operator_id in operator_rows
            if operator_id in referenced_operator_ids
        ],
        "selections": selections,
        "distance_pairs": _distance_pairs(
            _array(top["distance_pairs"], "distance_pairs"),
            selections,
        ),
        "scope": "geometric candidates; no bond or joint-state inference",
    }
    try:
        json.dumps(result, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("assembly projection is not finite plain JSON") from exc
    return result
