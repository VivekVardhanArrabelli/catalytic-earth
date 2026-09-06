"""Reviewed, executable source-panel transformations for Atlas records.

The v1 contract represents a bounded depicted-input to depicted-input graph
change.  Its atom identifiers are reviewed panel-locator correspondences, not
upstream atom maps.  Chemical symmetry alternatives remain separate from the
single raw-Kekule locator alignment used for exact graph replay.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any
import xml.etree.ElementTree as ET

from .canonical_hash import canonical_file_sha256
from .atlas10_source_adapters import parse_mcsa_scheme_flows


SCHEMA_VERSION = "catalytic-earth.transformations.v1"
SCHEMA_VERSION_V2 = "catalytic-earth.transformations.v2"
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:+-]*\Z")
_ELEMENT = re.compile(r"[A-Z][a-z]?\Z")
_SCOPE_KEYS = {
    "computed_canonical_input_correspondence",
    "depicted_intermediate_transition",
    "upstream_atom_map",
    "canonical_product_correspondence",
    "net_reaction_atom_map",
    "complete_racemization_path",
    "inferred_return_step",
}
_SOURCE_SCOPE_KEYS = {
    "source_depiction_transition",
    "canonical_input_correspondence",
    "canonical_product_correspondence",
    "upstream_atom_map",
    "net_reaction_atom_map",
    "complete_mechanism_path",
    "exact_physical_peptide_identity",
    "source_r_group_resolution",
    "experimentally_observed_intermediate",
}


def _fail(message: str) -> None:
    raise ValueError(message)


def _require(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
    return value


def _exact(value: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(keys - set(value))
    extra = sorted(set(value) - keys)
    _require(not missing and not extra, f"{label} fields differ: missing={missing}, extra={extra}")


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be a non-empty string")
    return value


def _integer(value: Any, label: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool), f"{label} must be an integer")
    return value


def _sha(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def transformation_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every declaration except the manually reviewed review block."""
    return _sha({key: item for key, item in value.items() if key != "review"})


def _edge_key(atom_ids: list[str]) -> tuple[str, str]:
    _require(len(atom_ids) == 2 and atom_ids[0] != atom_ids[1], "bond atom_ids must name two distinct atoms")
    return tuple(sorted(atom_ids))


def _validate_graph(value: Any, label: str) -> dict[str, Any]:
    graph = _object(value, label)
    _exact(graph, {"graph_id", "atom_id_scope", "atoms", "bonds"}, label)
    _string(graph["graph_id"], f"{label}.graph_id")
    _require(graph["atom_id_scope"] == "source_panel_local_locator", f"{label}.atom_id_scope differs")
    atoms = _array(graph["atoms"], f"{label}.atoms")
    _require(bool(atoms), f"{label}.atoms is empty")
    atom_ids: set[str] = set()
    for index, raw in enumerate(atoms):
        atom = _object(raw, f"{label}.atoms[{index}]")
        _exact(atom, {"atom_id", "element", "formal_charge", "stereochemistry"}, f"{label}.atoms[{index}]")
        atom_id = _string(atom["atom_id"], f"{label}.atoms[{index}].atom_id")
        _require(bool(_TOKEN.fullmatch(atom_id)), f"{label} atom_id is invalid: {atom_id}")
        _require(atom_id not in atom_ids, f"{label} repeats atom {atom_id}")
        atom_ids.add(atom_id)
        element = _string(atom["element"], f"{label}.{atom_id}.element")
        _require(element == "R" or bool(_ELEMENT.fullmatch(element)), f"{label}.{atom_id}.element is invalid")
        _integer(atom["formal_charge"], f"{label}.{atom_id}.formal_charge")
        _require(atom["stereochemistry"] in {None, "R", "S"}, f"{label}.{atom_id}.stereochemistry is invalid")
    edges: set[tuple[str, str]] = set()
    for index, raw in enumerate(_array(graph["bonds"], f"{label}.bonds")):
        bond = _object(raw, f"{label}.bonds[{index}]")
        _exact(bond, {"atom_ids", "order"}, f"{label}.bonds[{index}]")
        refs = _array(bond["atom_ids"], f"{label}.bonds[{index}].atom_ids")
        _require(all(isinstance(item, str) and item in atom_ids for item in refs), f"{label} bond references an unknown atom")
        key = _edge_key(refs)
        _require(key not in edges, f"{label} repeats bond {key}")
        edges.add(key)
        _require(_integer(bond["order"], f"{label}.bonds[{index}].order") in {1, 2, 3}, f"{label} bond order is unsupported")
    return graph


def _validate_edits(value: Any, atom_ids: set[str], label: str) -> list[dict[str, Any]]:
    edits = _array(value, label)
    _require(bool(edits), f"{label} is empty")
    edit_ids: set[str] = set()
    for index, raw in enumerate(edits):
        edit = _object(raw, f"{label}[{index}]")
        _exact(edit, {"edit_id", "operation", "atom_ids", "before", "after", "source_flow_id"}, f"{label}[{index}]")
        edit_id = _string(edit["edit_id"], f"{label}[{index}].edit_id")
        _require(edit_id not in edit_ids, f"{label} repeats edit_id {edit_id}")
        edit_ids.add(edit_id)
        operation = edit["operation"]
        _require(operation in {"remove_bond", "add_bond", "set_bond_order", "set_formal_charge", "set_stereochemistry"}, f"{label}[{index}].operation is unsupported")
        refs = _array(edit["atom_ids"], f"{label}[{index}].atom_ids")
        expected_length = 1 if operation in {"set_formal_charge", "set_stereochemistry"} else 2
        _require(len(refs) == expected_length and all(isinstance(item, str) and item in atom_ids for item in refs), f"{label}[{index}] atom references differ")
        if operation == "set_stereochemistry":
            _require(edit["before"] in {None, "R", "S"} and edit["after"] in {None, "R", "S"}, f"{label}[{index}] stereo values are invalid")
        else:
            _integer(edit["before"], f"{label}[{index}].before")
            _integer(edit["after"], f"{label}[{index}].after")
        if operation == "remove_bond":
            _require(edit["before"] in {1, 2, 3} and edit["after"] == 0, f"{label}[{index}] removal values differ")
        elif operation == "add_bond":
            _require(edit["before"] == 0 and edit["after"] in {1, 2, 3}, f"{label}[{index}] addition values differ")
        elif operation == "set_bond_order":
            _require(edit["before"] in {1, 2, 3} and edit["after"] in {1, 2, 3} and edit["before"] != edit["after"], f"{label}[{index}] bond-order values differ")
        _string(edit["source_flow_id"], f"{label}[{index}].source_flow_id")
    return edits


def _graph_rows(graph: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], int]]:
    atoms = {row["atom_id"]: copy.deepcopy(row) for row in graph["atoms"]}
    bonds = {_edge_key(row["atom_ids"]): row["order"] for row in graph["bonds"]}
    return atoms, bonds


def apply_graph_edits(graph: dict[str, Any], edits: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply checked bond, charge, and stereo edits to a compact covalent graph."""
    source = _validate_graph(copy.deepcopy(graph), "graph")
    atoms, bonds = _graph_rows(source)
    checked = _validate_edits(copy.deepcopy(edits), set(atoms), "edits")
    for edit in checked:
        operation = edit["operation"]
        refs = edit["atom_ids"]
        if operation in {"remove_bond", "add_bond", "set_bond_order"}:
            key = _edge_key(refs)
            current = bonds.get(key, 0)
            _require(current == edit["before"], f"{edit['edit_id']} expected bond order {edit['before']}, found {current}")
            if edit["after"] == 0:
                bonds.pop(key, None)
            else:
                bonds[key] = edit["after"]
        elif operation == "set_formal_charge":
            atom = atoms[refs[0]]
            _require(atom["formal_charge"] == edit["before"], f"{edit['edit_id']} formal charge precondition differs")
            atom["formal_charge"] = edit["after"]
        else:
            atom = atoms[refs[0]]
            _require(atom["stereochemistry"] == edit["before"], f"{edit['edit_id']} stereochemistry precondition differs")
            atom["stereochemistry"] = edit["after"]
    return {
        "graph_id": source["graph_id"],
        "atom_id_scope": source["atom_id_scope"],
        "atoms": [atoms[row["atom_id"]] for row in source["atoms"]],
        "bonds": [
            {"atom_ids": list(key), "order": bonds[key]}
            for key in sorted(bonds)
        ],
    }


def _mapped_content(graph: dict[str, Any], mapping: dict[str, str]) -> tuple[list[tuple], list[tuple]]:
    atoms, bonds = _graph_rows(graph)
    mapped_atoms = sorted(
        (
            mapping[atom_id],
            row["element"],
            row["formal_charge"],
            row["stereochemistry"],
        )
        for atom_id, row in atoms.items()
    )
    mapped_bonds = sorted(
        (tuple(sorted((mapping[left], mapping[right]))), order)
        for (left, right), order in bonds.items()
    )
    return mapped_atoms, mapped_bonds


def replay_graph_edits(
    before_graph: dict[str, Any],
    edits: list[dict[str, Any]],
    after_graph: dict[str, Any],
    atom_map: list[dict[str, str]],
) -> bool:
    """Return whether edits reproduce the declared after graph under an explicit map."""
    before = _validate_graph(copy.deepcopy(before_graph), "before_graph")
    after = _validate_graph(copy.deepcopy(after_graph), "after_graph")
    rows = _array(atom_map, "atom_map")
    before_ids = {row["atom_id"] for row in before["atoms"]}
    after_ids = {row["atom_id"] for row in after["atoms"]}
    mapping: dict[str, str] = {}
    for index, raw in enumerate(rows):
        row = _object(raw, f"atom_map[{index}]")
        _exact(row, {"before_atom_id", "after_atom_id"}, f"atom_map[{index}]")
        left = _string(row["before_atom_id"], f"atom_map[{index}].before_atom_id")
        right = _string(row["after_atom_id"], f"atom_map[{index}].after_atom_id")
        _require(left in before_ids and right in after_ids and left not in mapping, "atom_map is not a valid before-to-after map")
        mapping[left] = right
    _require(set(mapping) == before_ids and set(mapping.values()) == after_ids and len(mapping) == len(set(mapping.values())), "atom_map must be a complete bijection")
    predicted = apply_graph_edits(before, edits)
    return _mapped_content(predicted, mapping) == _mapped_content(after, {item: item for item in after_ids})


def _validate_binding_path(path_value: Any, repo_root: Path | None, digest: Any, label: str) -> str:
    path = _string(path_value, f"{label}.path")
    _require("\\" not in path, f"{label}.path must use repository POSIX separators")
    pure = PurePosixPath(path)
    _require(not pure.is_absolute() and ".." not in pure.parts and "." not in pure.parts, f"{label}.path must be safe and repository-relative")
    _require(isinstance(digest, str) and bool(_HEX64.fullmatch(digest)), f"{label}.sha256 is invalid")
    if repo_root is not None:
        root = repo_root.resolve()
        full = (root / Path(*pure.parts)).resolve()
        _require(full == root or root in full.parents, f"{label}.path escapes repository root")
        _require(full.is_file(), f"{label}.path is missing: {path}")
        _require(canonical_file_sha256(full) == digest, f"{label}.sha256 differs for {path}")
    return path


def _records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for key in ("records", "follow_on_records"):
        value = bundle.get(key)
        if isinstance(value, list):
            records.extend(item for item in value if isinstance(item, dict))
    inherited = bundle.get("inherited_kernel")
    if isinstance(inherited, dict):
        records.extend(_records(inherited))
    return records


def _validate_record_binding(row: dict[str, Any], bundle: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[int, dict[str, Any]]]:
    binding = _object(row["record_binding"], "record_binding")
    _exact(binding, {"case_id", "record_id", "mcsa_id", "source_snapshot_sha256"}, "record_binding")
    for key in ("case_id", "record_id", "mcsa_id"):
        _string(binding[key], f"record_binding.{key}")
    _require(bool(_HEX64.fullmatch(str(binding["source_snapshot_sha256"]))), "record_binding.source_snapshot_sha256 is invalid")
    matches = [item for item in _records(bundle) if item.get("record_id") == binding["record_id"]]
    _require(len(matches) == 1, f"bound Atlas10 record count differs for {binding['record_id']}")
    record = matches[0]
    _require(record.get("case_id") == binding["case_id"], "record_binding.case_id differs")
    proposal_binding = _object(row["proposal_binding"], "proposal_binding")
    _exact(proposal_binding, {"proposal_id", "source_mechanism_id"}, "proposal_binding")
    proposals = [
        proposal for proposal in record.get("mechanism_proposals", [])
        if proposal.get("proposal_id") == proposal_binding["proposal_id"]
        and proposal.get("source_mechanism_id") == proposal_binding["source_mechanism_id"]
        and proposal.get("source_record_id") == binding["mcsa_id"]
    ]
    _require(len(proposals) == 1, "proposal_binding does not select one Atlas10 proposal")
    steps = {item.get("source_step_id"): item for item in proposals[0].get("mechanism_steps", [])}
    return record, proposals[0], steps


def _validate_state_pair(value: Any, steps: dict[int, dict[str, Any]]) -> None:
    pair = _object(value, "state_pair")
    _exact(pair, {"semantics", "before", "after"}, "state_pair")
    _require(pair["semantics"] == "depicted_input_to_depicted_input", "state_pair.semantics differs")
    seen = []
    for label in ("before", "after"):
        state = _object(pair[label], f"state_pair.{label}")
        _exact(state, {"source_step_id", "step_id", "scheme_sha256"}, f"state_pair.{label}")
        source_step_id = _integer(state["source_step_id"], f"state_pair.{label}.source_step_id")
        step = steps.get(source_step_id)
        _require(step is not None and step.get("step_id") == state["step_id"] and step.get("source_scheme_sha256") == state["scheme_sha256"], f"state_pair.{label} differs from Atlas10")
        seen.append(source_step_id)
    _require(seen[1] == seen[0] + 1, "state_pair must bind consecutive source inputs")


def _validate_map_rows(value: Any, left_key: str, right_key: str, label: str) -> tuple[set[str], set[str]]:
    rows = _array(value, label)
    _require(bool(rows), f"{label} is empty")
    left: set[str] = set()
    right: set[str] = set()
    for index, raw in enumerate(rows):
        row = _object(raw, f"{label}[{index}]")
        _exact(row, {left_key, right_key}, f"{label}[{index}]")
        a = _string(row[left_key], f"{label}[{index}].{left_key}")
        b = _string(row[right_key], f"{label}[{index}].{right_key}")
        _require(a not in left and b not in right, f"{label} is not bijective")
        left.add(a)
        right.add(b)
    return left, right


def _validate_canonical(value: Any, bindings: dict[str, dict[str, Any]], before: dict[str, Any]) -> None:
    item = _object(value, "canonical_input_correspondence")
    _exact(item, {"status", "participant_id", "participant_structure_binding_id", "raw_source_labels", "method", "map_alternatives", "invariant_reactive_core", "remote_symmetry", "rejected_participant_matches"}, "canonical_input_correspondence")
    _require(item["status"] == "computed_graph_and_stereo_match_with_raw_identifier_conflict", "canonical correspondence status differs")
    _require(re.fullmatch(r"CHEBI:[1-9][0-9]*", _string(item["participant_id"], "participant_id")) is not None, "participant_id is invalid")
    _require(item["participant_structure_binding_id"] in bindings, "participant structure binding is missing")
    labels = _array(item["raw_source_labels"], "raw_source_labels")
    _require(bool(labels) and all(isinstance(value, str) and value for value in labels), "raw_source_labels differ")
    method = _object(item["method"], "canonical method")
    _exact(method, {"kind", "tool", "tool_version", "upstream_atom_map", "audit_script_binding_id", "audit_result_binding_id"}, "canonical method")
    _require(method["kind"] == "computed_graph_and_stereo_match" and method["tool"] == "RDKit" and method["upstream_atom_map"] is False, "canonical method scope differs")
    for key in ("audit_script_binding_id", "audit_result_binding_id"):
        _require(method[key] in bindings, f"canonical method {key} is unbound")
    alternatives = _array(item["map_alternatives"], "canonical map_alternatives")
    domains = ranges = None
    maps: list[dict[str, str]] = []
    for index, raw in enumerate(alternatives):
        alt = _object(raw, f"canonical map_alternatives[{index}]")
        _exact(alt, {"map_id", "canonical_to_before"}, f"canonical map_alternatives[{index}]")
        _string(alt["map_id"], "canonical map_id")
        left, right = _validate_map_rows(alt["canonical_to_before"], "canonical_atom_id", "before_atom_id", f"canonical map {index}")
        domains = left if domains is None else domains
        ranges = right if ranges is None else ranges
        _require(left == domains and right == ranges, "canonical alternatives cover different atoms")
        maps.append({entry["canonical_atom_id"]: entry["before_atom_id"] for entry in alt["canonical_to_before"]})
    _require(len({_sha(mapping) for mapping in maps}) == len(maps), "canonical map alternatives are not distinct")
    before_atoms = {row["atom_id"]: row for row in before["atoms"]}
    _require(ranges is not None and ranges <= set(before_atoms), "canonical map references an unknown before atom")
    core = _array(item["invariant_reactive_core"], "invariant_reactive_core")
    for index, raw in enumerate(core):
        row = _object(raw, f"invariant_reactive_core[{index}]")
        _exact(row, {"role", "canonical_atom_id", "before_atom_id"}, f"invariant_reactive_core[{index}]")
        _string(row["role"], "reactive-core role")
        _require(all(mapping.get(row["canonical_atom_id"]) == row["before_atom_id"] for mapping in maps), "canonical alternatives disagree on the reactive core")
    symmetry = _object(item["remote_symmetry"], "remote_symmetry")
    _exact(symmetry, {"kind", "full_map_count", "canonical_equivalence_classes", "before_equivalence_classes"}, "remote_symmetry")
    _require(symmetry["kind"] == "phenyl_reflection_equivalence" and symmetry["full_map_count"] == len(alternatives) and len(alternatives) > 1, "remote symmetry declaration differs")
    for key in ("canonical_equivalence_classes", "before_equivalence_classes"):
        classes = _array(symmetry[key], f"remote_symmetry.{key}")
        _require(all(isinstance(group, list) and len(group) > 1 and all(isinstance(atom, str) for atom in group) for group in classes), f"remote_symmetry.{key} differs")
    rejected = _array(item["rejected_participant_matches"], "rejected_participant_matches")
    rejected_ids: set[str] = set()
    for index, raw in enumerate(rejected):
        row = _object(raw, f"rejected_participant_matches[{index}]")
        _exact(row, {"participant_id", "chirality_sensitive_match_count"}, f"rejected_participant_matches[{index}]")
        rejected_id = _string(row["participant_id"], f"rejected_participant_matches[{index}].participant_id")
        _require(re.fullmatch(r"CHEBI:[1-9][0-9]*", rejected_id) is not None and rejected_id != item["participant_id"] and row["chirality_sensitive_match_count"] == 0, "rejected participant matches differ")
        rejected_ids.add(rejected_id)
    raw_ids = {
        f"CHEBI:{match.group(1)}"
        for label in labels
        if (match := re.fullmatch(r"(?i:chebi):([1-9][0-9]*)", label))
    }
    _require(bool(raw_ids) and item["participant_id"] not in raw_ids and raw_ids <= rejected_ids, "raw identifier conflict semantics differ")


def _validate_source_context(
    value: Any, bindings: dict[str, dict[str, Any]], mcsa_id: str,
    before: dict[str, Any], after: dict[str, Any],
) -> dict[str, dict[str, str | None]]:
    context = _object(value, "source_context")
    _exact(context, {"status", "depiction_node_semantics", "source_atom_annotations", "source_r_groups", "canonical_participant_correspondence", "source_binding_ids"}, "source_context")
    _require(context["status"] == "source_panel_only_no_canonical_participant_bridge", "source_context.status differs")
    _require(context["depiction_node_semantics"] == "source_graph_nodes_not_exact_physical_atoms", "source_context depiction-node semantics differ")
    _require(context["canonical_participant_correspondence"] == "not_asserted", "source_context promotes a canonical participant")
    binding_ids = _array(context["source_binding_ids"], "source_context.source_binding_ids")
    _require(len(binding_ids) == len(set(binding_ids)) and all(item in bindings for item in binding_ids), "source_context has unknown or repeated bindings")
    _require(f"source:M-CSA:{mcsa_id}" in binding_ids, "source_context omits its M-CSA source")
    annotations = _object(context["source_atom_annotations"], "source_atom_annotations")
    _exact(annotations, {"scope", "rows"}, "source_atom_annotations")
    _require(annotations["scope"] == "identical_across_bound_state_pair", "source atom annotation scope differs")
    rows: dict[str, dict[str, str | None]] = {}
    graph_ids = {item["atom_id"] for item in before["atoms"]}
    _require(graph_ids == {item["atom_id"] for item in after["atoms"]}, "source-panel graphs use different depiction nodes")
    for index, raw in enumerate(_array(annotations["rows"], "source_atom_annotations.rows")):
        row = _object(raw, f"source_atom_annotations.rows[{index}]")
        _exact(row, {"atom_id", "mrv_extra_label", "mrv_alias", "rgroup_ref"}, f"source_atom_annotations.rows[{index}]")
        atom_id = _string(row["atom_id"], f"source_atom_annotations.rows[{index}].atom_id")
        _require(atom_id in graph_ids and atom_id not in rows, "source atom annotation references an unknown or repeated node")
        _require(any(row[key] is not None for key in ("mrv_extra_label", "mrv_alias", "rgroup_ref")), "source atom annotation is empty")
        _require(all(row[key] is None or isinstance(row[key], str) for key in ("mrv_extra_label", "mrv_alias", "rgroup_ref")), "source atom annotation value is invalid")
        rows[atom_id] = row
    groups = _object(context["source_r_groups"], "source_r_groups")
    _exact(groups, {"status", "element_r_atom_ids", "alias_r_atom_ids", "expansion_asserted"}, "source_r_groups")
    _require(groups["status"] == "source_tokens_preserved_unresolved" and groups["expansion_asserted"] is False, "source R-group scope differs")
    element_r = _array(groups["element_r_atom_ids"], "element_r_atom_ids")
    alias_r = _array(groups["alias_r_atom_ids"], "alias_r_atom_ids")
    _require(len(element_r) == len(set(element_r)) and set(element_r) == {item["atom_id"] for item in before["atoms"] if item["element"] == "R"}, "element-R node inventory differs")
    _require(len(alias_r) == len(set(alias_r)) and set(alias_r) == {atom_id for atom_id, row in rows.items() if row["mrv_alias"] == "R"}, "alias-R node inventory differs")
    return rows


def _raw_source_annotations(
    scheme: dict[str, Any], selected: set[str], label: str,
) -> tuple[dict[str, dict[str, str | None]], set[str]]:
    root = ET.fromstring(scheme["content_utf8"])
    atoms = {
        item.get("id"): item for item in root.iter()
        if item.tag.rsplit("}", 1)[-1] == "atom"
    }
    _require(set(atoms) == selected, f"{label} does not cover every raw depiction node")
    rows: dict[str, dict[str, str | None]] = {}
    for atom_id, atom in atoms.items():
        row = {
            "atom_id": atom_id,
            "mrv_extra_label": atom.get("mrvExtraLabel"),
            "mrv_alias": atom.get("mrvAlias"),
            "rgroup_ref": atom.get("rgroupRef"),
        }
        if any(row[key] is not None for key in ("mrv_extra_label", "mrv_alias", "rgroup_ref")):
            rows[atom_id] = row
    element_r = {atom_id for atom_id, atom in atoms.items() if atom.get("elementType") == "R"}
    return rows, element_r


def _validate_chemical_maps(value: Any, before: dict[str, Any], after: dict[str, Any], replay: dict[str, Any]) -> None:
    alternatives = _array(value, "chemical_map_alternatives")
    _require(len(alternatives) == replay["chemical_topology_map_count"] > replay["raw_kekule_map_count"] >= 1, "raw-Kekule and chemical map counts differ")
    before_atoms, before_bonds = _graph_rows(before)
    after_atoms, after_bonds = _graph_rows(after)
    domains = ranges = None
    signatures: set[str] = set()
    for index, raw in enumerate(alternatives):
        alt = _object(raw, f"chemical_map_alternatives[{index}]")
        _exact(alt, {"map_id", "before_to_after"}, f"chemical_map_alternatives[{index}]")
        _string(alt["map_id"], "chemical map_id")
        left, right = _validate_map_rows(alt["before_to_after"], "before_atom_id", "after_atom_id", f"chemical map {index}")
        domains = left if domains is None else domains
        ranges = right if ranges is None else ranges
        _require(left == domains and right == ranges, "chemical alternatives cover different atoms")
        mapping = {row["before_atom_id"]: row["after_atom_id"] for row in alt["before_to_after"]}
        signatures.add(_sha(mapping))
        _require(left <= set(before_atoms) and right <= set(after_atoms), "chemical map references an unknown atom")
        _require(all(before_atoms[a]["element"] == after_atoms[b]["element"] and before_atoms[a]["formal_charge"] == after_atoms[b]["formal_charge"] for a, b in mapping.items()), "chemical map changes element or charge")
        mapped_edges = {tuple(sorted((mapping[a], mapping[b]))) for a, b in before_bonds if a in mapping and b in mapping}
        after_edges = {edge for edge in after_bonds if set(edge) <= right}
        _require(mapped_edges == after_edges, "chemical map does not preserve topology")
    _require(len(signatures) == len(alternatives), "chemical map alternatives are not distinct")


def _validate_review(value: Any, payload_hash: str) -> None:
    review = _object(value, "review")
    _exact(review, {"status", "reviewer_kind", "review_mode", "human_review_performed", "errors_may_be_correlated", "agreement_is_not_statistical_independence", "reviewed_payload_sha256"}, "review")
    _require(review["status"] == "accepted" and review["reviewer_kind"] == "same_model_agent" and review["review_mode"] == "informed_nonblind", "review provenance differs")
    _require(review["human_review_performed"] is False and review["errors_may_be_correlated"] is True and review["agreement_is_not_statistical_independence"] is True, "review independence disclosure differs")
    _require(review["reviewed_payload_sha256"] == payload_hash, "reviewed transformation payload hash differs")


def _validate_raw_graph(graph: dict[str, Any], scheme: dict[str, Any], label: str) -> None:
    root = ET.fromstring(scheme["content_utf8"])
    atoms = {item.get("id"): item for item in root.iter() if item.tag.rsplit("}", 1)[-1] == "atom"}
    bonds: dict[tuple[str, str], int] = {}
    for item in root.iter():
        if item.tag.rsplit("}", 1)[-1] != "bond" or item.get("convention") == "cxn:coord":
            continue
        refs = item.get("atomRefs2", "").split()
        _require(len(refs) == 2 and item.get("order") in {"1", "2", "3"}, f"{label} raw bond is unsupported")
        bonds[tuple(sorted(refs))] = int(item.get("order"))
    selected = {row["atom_id"] for row in graph["atoms"]}
    for row in graph["atoms"]:
        raw = atoms.get(row["atom_id"])
        _require(raw is not None and raw.get("elementType") == row["element"] and int(raw.get("formalCharge", "0")) == row["formal_charge"], f"{label} atom differs from raw MRV: {row['atom_id']}")
    projected = {edge: order for edge, order in bonds.items() if set(edge) <= selected}
    declared = {_edge_key(row["atom_ids"]): row["order"] for row in graph["bonds"]}
    _require(projected == declared, f"{label} bonds differ from raw MRV")


def _binding_for_kind(
    bindings: dict[str, dict[str, Any]], binding_ids: list[str], kind: str
) -> dict[str, Any]:
    matches = [bindings[item] for item in binding_ids if bindings[item]["artifact_kind"] == kind]
    _require(len(matches) == 1, f"canonical reaction must bind one {kind}")
    return matches[0]


def _tsv_rows(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8")), delimiter="\t"))


def _validate_rhea_sources(
    reaction: dict[str, Any], row: dict[str, Any], record: dict[str, Any],
    proposal: dict[str, Any], bindings: dict[str, dict[str, Any]], repo_root: Path,
) -> None:
    binding_ids = reaction["source_binding_ids"]
    query = _binding_for_kind(bindings, binding_ids, "official_reaction_query")
    directions = _binding_for_kind(bindings, binding_ids, "official_reaction_direction_map")
    crossrefs = _binding_for_kind(bindings, binding_ids, "official_reaction_cross_reference_map")
    rhea = bindings.get(f"source:Rhea:{reaction['master_id']}")
    _require(rhea is not None and rhea["binding_id"] in binding_ids, "canonical reaction Rhea snapshot is unbound")
    wrapped = json.loads((repo_root / rhea["path"]).read_text(encoding="utf-8"))
    _require(wrapped.get("record_id") == reaction["master_id"], "Rhea snapshot record differs")
    query_rows = _tsv_rows(repo_root / query["path"])
    _require(len(query_rows) == 1 and query_rows[0].get("Reaction identifier") == reaction["master_id"], "Rhea query record differs")
    _require(query_rows[0].get("Equation") == record.get("reaction", {}).get("equation"), "Rhea query equation differs")
    master = reaction["master_id"].split(":", 1)[1]
    directed = reaction["directed_id"].split(":", 1)[1]
    direction_rows = [item for item in _tsv_rows(repo_root / directions["path"]) if item.get("RHEA_ID_MASTER") == master]
    column = {"LR": "RHEA_ID_LR", "RL": "RHEA_ID_RL"}[reaction["directed_direction_code"]]
    _require(len(direction_rows) == 1 and direction_rows[0].get(column) == directed, "Rhea directed child differs")
    xref_rows = [item for item in _tsv_rows(repo_root / crossrefs["path"]) if item.get("ID") == row["record_binding"]["mcsa_id"]]
    _require(len(xref_rows) == 1 and xref_rows[0] == {
        "RHEA_ID": directed, "DIRECTION": reaction["directed_direction_code"],
        "MASTER_ID": master, "ID": row["record_binding"]["mcsa_id"],
    }, "Rhea M-CSA cross-reference differs")
    sides = {
        item.get("side_uri", "").rsplit("_", 1)[-1]: item.get("accession")
        for item in wrapped.get("participant_rows", [])
    }
    participants = {item.get("side"): item.get("participant_id") for item in record.get("reaction", {}).get("participants", [])}
    _require(sides == {"L": participants.get("left"), "R": participants.get("right")}, "Rhea participant sides differ")
    mcsa = bindings[f"source:M-CSA:{row['record_binding']['mcsa_id']}"]
    raw = json.loads((repo_root / mcsa["path"]).read_text(encoding="utf-8"))["entry"]["reaction"]
    compounds = {item["type"]: f"CHEBI:{item['chebi_id']}" for item in raw["compounds"]}
    raw_proposal = [item for item in raw["mechanisms"] if item["mechanism_id"] == row["proposal_binding"]["source_mechanism_id"]]
    _require(len(raw_proposal) == 1 and raw_proposal[0]["mechanism_text"] == proposal.get("mechanism_text"), "raw proposal text differs")
    orientation = None
    if compounds == {"reactant": sides.get("L"), "product": sides.get("R")}:
        orientation = "LR"
    elif compounds == {"reactant": sides.get("R"), "product": sides.get("L")}:
        orientation = "RL"
    _require(orientation is not None, "M-CSA participants do not align to Rhea sides")
    relation = (
        "record_xref_direction_agrees_with_declared_proposal_direction"
        if orientation == reaction["directed_direction_code"]
        else "record_xref_direction_opposes_declared_proposal_direction"
    )
    _require(reaction["proposal_direction_relation"] == relation, "proposal direction relation differs from bound sources")


def _validate_audit(item: dict[str, Any], bindings: dict[str, dict[str, Any]], repo_root: Path, panel: dict[str, Any]) -> None:
    method = item["canonical_input_correspondence"]["method"]
    audit_binding = bindings[method["audit_result_binding_id"]]
    audit = json.loads((repo_root / audit_binding["path"]).read_text(encoding="utf-8"))
    _require(audit.get("audit_method", {}).get("rdkit_version") == method["tool_version"], "audit RDKit version differs")
    participant = item["canonical_input_correspondence"]["participant_id"]
    structures = [row for row in audit.get("canonical_structures", []) if row.get("id") == participant]
    structure_binding = bindings[item["canonical_input_correspondence"]["participant_structure_binding_id"]]
    _require(len(structures) == 1 and structures[0].get("sha256") == structure_binding["sha256"], "canonical participant structure binding differs from pinned audit")
    actual = audit.get("complete_panel_canonical_participant_matches", {}).get("1", {}).get(f"{participant}:chiral", {})
    maps = item["canonical_input_correspondence"]["map_alternatives"]
    expected_maps = []
    for alt in maps:
        keyed = {int(row["canonical_atom_id"]): row["before_atom_id"] for row in alt["canonical_to_before"]}
        _require(set(keyed) == set(range(1, len(keyed) + 1)), "canonical atom positions are not consecutive")
        expected_maps.append([keyed[index] for index in range(1, len(keyed) + 1)])
    _require(actual.get("count") == len(maps) and actual.get("source_atom_maps") == expected_maps, "canonical input maps differ from pinned audit")
    audited_steps = {step.get("step_id"): step for step in audit.get("steps", [])}
    for state_name, graph_name in (("before", "before_graph"), ("after", "after_graph")):
        source_step_id = item["state_pair"][state_name]["source_step_id"]
        audited_atoms = {atom["source_atom_ref"]: atom for atom in audited_steps.get(source_step_id, {}).get("ligand_atoms", [])}
        for atom in panel[graph_name]["atoms"]:
            if atom["stereochemistry"] is not None or atom["atom_id"] in audited_atoms:
                _require(atom["atom_id"] in audited_atoms and atom["stereochemistry"] == audited_atoms[atom["atom_id"]].get("cip"), f"{graph_name} stereochemistry differs from pinned audit")
    raw_labels = sorted({atom["raw_label"] for atom in audited_steps.get(item["state_pair"]["before"]["source_step_id"], {}).get("ligand_atoms", []) if atom.get("raw_label")})
    _require(sorted(item["canonical_input_correspondence"]["raw_source_labels"]) == raw_labels, "canonical raw source labels differ from pinned audit")
    for rejected in item["canonical_input_correspondence"]["rejected_participant_matches"]:
        count = audit.get("complete_panel_canonical_participant_matches", {}).get("1", {}).get(f"{rejected['participant_id']}:chiral", {}).get("count")
        _require(count == rejected["chirality_sensitive_match_count"], "rejected participant count differs from pinned audit")
    for row in panel["product_graph_check"]["canonical_participant_match_counts"]:
        key = f"{row['participant_id']}:{row['match_mode']}"
        count = audit.get("complete_panel_canonical_participant_matches", {}).get(str(row["source_step_id"]), {}).get(key, {}).get("count")
        _require(count == row["match_count"], "product graph count differs from pinned audit")


def validate_transformations(
    value: Any,
    *,
    atlas10_bundle: dict[str, Any],
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate declarations, replay graph edits, and optionally audit bound sources."""
    data = _object(value, "transformations")
    _exact(data, {"schema_version", "transformation_set_id", "status", "source_bindings", "transformations", "review"}, "transformations")
    schema_version = data["schema_version"]
    _require(schema_version in {SCHEMA_VERSION, SCHEMA_VERSION_V2} and data["status"] == "reviewed", "transformation set identity/status differs")
    source_only = schema_version == SCHEMA_VERSION_V2
    set_id = _string(data["transformation_set_id"], "transformation_set_id")
    root = Path(repo_root) if repo_root is not None else None
    bindings: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(_array(data["source_bindings"], "source_bindings")):
        binding = _object(raw, f"source_bindings[{index}]")
        _exact(binding, {"binding_id", "artifact_kind", "path", "sha256"}, f"source_bindings[{index}]")
        binding_id = _string(binding["binding_id"], f"source_bindings[{index}].binding_id")
        _require(binding_id not in bindings, f"source binding repeats {binding_id}")
        _string(binding["artifact_kind"], f"source_bindings[{index}].artifact_kind")
        _validate_binding_path(binding["path"], root, binding["sha256"], f"source_bindings[{index}]")
        bindings[binding_id] = binding
    rows = _array(data["transformations"], "transformations")
    _require(bool(rows), "transformations is empty")
    ids: set[str] = set()
    record_ids: set[str] = set()
    for index, raw in enumerate(rows):
        row = _object(raw, f"transformations[{index}]")
        row_keys = (
            {"transformation_id", "correspondence_kind", "record_binding", "proposal_binding", "state_pair", "source_context", "panel_correspondence", "mandatory_abstentions", "scope_effect"}
            if source_only else
            {"transformation_id", "record_binding", "proposal_binding", "canonical_reaction_binding", "state_pair", "canonical_input_correspondence", "panel_correspondence", "mandatory_abstentions", "scope_effect"}
        )
        _exact(row, row_keys, f"transformations[{index}]")
        if source_only:
            _require(row["correspondence_kind"] == "source_panel_only", "source-only correspondence kind differs")
        transformation_id = _string(row["transformation_id"], f"transformations[{index}].transformation_id")
        _require(transformation_id not in ids, f"transformation_id repeats {transformation_id}")
        ids.add(transformation_id)
        record, proposal, steps = _validate_record_binding(row, _object(atlas10_bundle, "atlas10_bundle"))
        record_ids.add(row["record_binding"]["record_id"])
        mcsa_bindings = [item for item in bindings.values() if item["binding_id"] == f"source:M-CSA:{row['record_binding']['mcsa_id']}"]
        _require(len(mcsa_bindings) == 1 and mcsa_bindings[0]["sha256"] == row["record_binding"]["source_snapshot_sha256"], "M-CSA source binding differs")
        _validate_state_pair(row["state_pair"], steps)
        reaction = None
        if not source_only:
            reaction = _object(row["canonical_reaction_binding"], "canonical_reaction_binding")
            _exact(reaction, {"provider", "master_id", "master_directionality", "directed_id", "directed_direction_code", "xref_scope", "proposal_direction_relation", "source_binding_ids"}, "canonical_reaction_binding")
            _require(reaction["provider"] == "Rhea" and reaction["master_directionality"] == "undirected_master" and reaction["directed_direction_code"] in {"LR", "RL"} and reaction["xref_scope"] == "record_cross_reference_not_atom_map" and reaction["proposal_direction_relation"] in {"record_xref_direction_opposes_declared_proposal_direction", "record_xref_direction_agrees_with_declared_proposal_direction"}, "canonical reaction scope differs")
            _require(re.fullmatch(r"RHEA:[1-9][0-9]*", reaction["master_id"]) is not None and re.fullmatch(r"RHEA:[1-9][0-9]*", reaction["directed_id"]) is not None, "Rhea identifier is invalid")
            _require(all(binding_id in bindings for binding_id in _array(reaction["source_binding_ids"], "canonical source_binding_ids")), "canonical reaction has an unknown source binding")
        panel = _object(row["panel_correspondence"], "panel_correspondence")
        panel_keys = (
            {"status", "mapping_scope", "before_graph", "after_graph", "graph_edits", "source_flow_bindings", "replay", "representation_boundaries"}
            if source_only else
            {"status", "mapping_scope", "before_graph", "after_graph", "graph_edits", "source_flow_bindings", "chemical_map_alternatives", "replay", "stereochemistry", "product_graph_check", "representation_boundaries"}
        )
        _exact(panel, panel_keys, "panel_correspondence")
        expected_status = "depicted_before_after_source_panel_correspondence" if source_only else "depicted_before_after_reaction_center_correspondence"
        _require(panel["status"] == expected_status, "panel correspondence status differs")
        if source_only:
            _require(panel["mapping_scope"] == "full_source_panel_depiction_node_correspondence", "panel mapping_scope differs")
        else:
            _string(panel["mapping_scope"], "panel mapping_scope")
        before = _validate_graph(panel["before_graph"], "before_graph")
        after = _validate_graph(panel["after_graph"], "after_graph")
        edits = _validate_edits(panel["graph_edits"], {item["atom_id"] for item in before["atoms"]}, "graph_edits")
        replay = _object(panel["replay"], "replay")
        replay_keys = {"status", "scope", "raw_locator_alignment", "atom_map"}
        if not source_only:
            replay_keys |= {"raw_kekule_map_count", "chemical_topology_map_count"}
        _exact(replay, replay_keys, "replay")
        _require(replay["status"] == "exact" and replay["raw_locator_alignment"] == "project_reviewed_same_token_alignment_not_upstream_atom_map", "replay scope differs")
        _string(replay["scope"], "replay.scope")
        if not source_only:
            _integer(replay["raw_kekule_map_count"], "raw_kekule_map_count")
            _integer(replay["chemical_topology_map_count"], "chemical_topology_map_count")
        _require(replay_graph_edits(before, edits, after, replay["atom_map"]), "graph edits do not replay the after graph")
        if source_only:
            _require(all(item["before_atom_id"] == item["after_atom_id"] for item in replay["atom_map"]), "source-panel locator alignment must preserve exact source tokens")
            _require(all(atom["stereochemistry"] is None for graph in (before, after) for atom in graph["atoms"]), "source-only panel cannot assert computed stereochemistry")
            _require(all(edit["operation"] != "set_stereochemistry" for edit in edits), "source-only panel cannot add a stereochemistry edit")
        else:
            _validate_chemical_maps(panel["chemical_map_alternatives"], before, after, replay)
        flow_rows = _array(panel["source_flow_bindings"], "source_flow_bindings")
        edit_ids = {item["edit_id"] for item in edits}
        bound_edits: list[str] = []
        source_flows = {
            flow.get("flow_id"): flow
            for flow in steps[row["state_pair"]["before"]["source_step_id"]].get("electron_flows", [])
        }
        edits_by_id = {item["edit_id"]: item for item in edits}
        for flow in flow_rows:
            _exact(_object(flow, "source_flow_binding"), {"source_step_id", "flow_id", "edit_ids"}, "source_flow_binding")
            _require(flow["source_step_id"] == row["state_pair"]["before"]["source_step_id"] and flow["flow_id"] in source_flows, "source flow binding differs from Atlas10")
            flow_edits = _array(flow["edit_ids"], "source flow edit_ids")
            raw_atoms = {
                atom["source_atom_ref"].rsplit(".", 1)[-1]
                for point in (source_flows[flow["flow_id"]]["source_point"], source_flows[flow["flow_id"]]["target_point"])
                for atom in point.get("atoms", [])
            }
            _require(all(
                edit_id in edits_by_id
                and edits_by_id[edit_id]["source_flow_id"] == flow["flow_id"]
                and set(edits_by_id[edit_id]["atom_ids"]) <= raw_atoms
                for edit_id in flow_edits
            ), "graph edit does not match its source flow endpoints")
            bound_edits.extend(flow_edits)
        _require(sorted(bound_edits) == sorted(edit_ids), "source flows do not cover every graph edit exactly once")
        if not source_only:
            stereo = _object(panel["stereochemistry"], "stereochemistry")
            _exact(stereo, {"before_atom_id", "before_assignment", "after_atom_id", "after_assignment", "after_geometry", "assignment_scope"}, "stereochemistry")
            _require(stereo["assignment_scope"] == "computed_rdkit_cip_not_source_literal" and stereo["after_geometry"] == "sp2", "stereochemistry scope differs")
            _require(any(edit["operation"] == "set_stereochemistry" and edit["atom_ids"] == [stereo["before_atom_id"]] and edit["before"] == stereo["before_assignment"] and edit["after"] == stereo["after_assignment"] for edit in edits), "stereochemistry transition is not replayed")
            product = _object(panel["product_graph_check"], "product_graph_check")
            _exact(product, {"audit_result_binding_id", "canonical_participant_match_counts"}, "product_graph_check")
            _require(product["audit_result_binding_id"] in bindings, "product graph audit binding is missing")
            product_rows = _array(product["canonical_participant_match_counts"], "product match counts")
            _require(bool(product_rows), "product match counts are empty")
            for item in product_rows:
                _exact(_object(item, "product match count"), {"source_step_id", "participant_id", "match_mode", "match_count"}, "product match count")
                _require(item["source_step_id"] > row["state_pair"]["before"]["source_step_id"] and item["match_mode"] in {"achiral", "chiral"} and item["match_count"] == 0, "product graph claim exceeds abstention scope")
        boundaries = _array(panel["representation_boundaries"], "representation_boundaries")
        _require(bool(boundaries), "representation boundaries are empty")
        for item in boundaries:
            _exact(_object(item, "representation boundary"), {"boundary_id", "reason"}, "representation boundary")
            _string(item["boundary_id"], "boundary_id"); _string(item["reason"], "boundary reason")
        boundary_ids = {item["boundary_id"] for item in boundaries}
        if source_only:
            required_boundaries = {"generic_peptide_r_groups_unresolved", "depiction_nodes_not_exact_atoms", "new_tetrahedral_stereochemistry_unasserted", "raw_bond_id_reuse", "canonical_participant_bridge_absent"}
            _require(required_boundaries <= boundary_ids, "source-only representation boundaries are incomplete")
            _validate_source_context(row["source_context"], bindings, row["record_binding"]["mcsa_id"], before, after)
        else:
            _require("lys166_h67_explicitness" in boundary_ids, "Step 2 explicit-H representation boundary is missing")
            _validate_canonical(row["canonical_input_correspondence"], bindings, before)
        abstentions = _array(row["mandatory_abstentions"], "mandatory_abstentions")
        abstention_ids: set[str] = set()
        for item in abstentions:
            _exact(_object(item, "mandatory abstention"), {"abstention_id", "reason"}, "mandatory abstention")
            abstention_ids.add(_string(item["abstention_id"], "abstention_id")); _string(item["reason"], "abstention reason")
        scope = _object(row["scope_effect"], "scope_effect")
        scope_keys = _SOURCE_SCOPE_KEYS if source_only else _SCOPE_KEYS
        _exact(scope, scope_keys, "scope_effect")
        _require(all(isinstance(value, bool) for value in scope.values()), "scope_effect values must be boolean")
        if source_only:
            _require(scope["source_depiction_transition"] and not any(scope[key] for key in _SOURCE_SCOPE_KEYS - {"source_depiction_transition"}), "scope_effect promotes an unsupported source-panel claim")
            required_abstentions = {"canonical_input_correspondence", "canonical_product_correspondence", "upstream_atom_map", "net_reaction_atom_map", "complete_mechanism_path", "exact_physical_peptide_identity", "source_r_group_resolution", "experimentally_observed_intermediate", "tetrahedral_stereochemistry"}
        else:
            _require(scope["computed_canonical_input_correspondence"] and scope["depicted_intermediate_transition"] and not any(scope[key] for key in _SCOPE_KEYS - {"computed_canonical_input_correspondence", "depicted_intermediate_transition"}), "scope_effect promotes an unsupported claim")
            required_abstentions = {"canonical_product_correspondence", "net_reaction_atom_map", "complete_racemization_path", "inferred_return_step", "step2_explicit_h67_lineage"}
        _require(required_abstentions <= abstention_ids, "mandatory abstentions omit an unsupported scope")
        if root is not None:
            mcsa = json.loads((root / mcsa_bindings[0]["path"]).read_text(encoding="utf-8"))
            mechanism_schemes = [item for item in mcsa.get("step_schemes", []) if item.get("mechanism_id") == row["proposal_binding"]["source_mechanism_id"]]
            raw_steps = {item["step_id"]: item for item in mechanism_schemes}
            _require(len(raw_steps) == len(mechanism_schemes), "raw source mechanism repeats a step")
            before_state, after_state = row["state_pair"]["before"], row["state_pair"]["after"]
            _require(raw_steps.get(before_state["source_step_id"], {}).get("content_sha256") == before_state["scheme_sha256"] and raw_steps.get(after_state["source_step_id"], {}).get("content_sha256") == after_state["scheme_sha256"], "raw scheme binding differs")
            for state in (before_state, after_state):
                source_text = raw_steps[state["source_step_id"]]["content_utf8"]
                _require(hashlib.sha256(source_text.encode("utf-8")).hexdigest() == state["scheme_sha256"], "raw scheme content hash differs")
            _validate_raw_graph(before, raw_steps[before_state["source_step_id"]], "before_graph")
            _validate_raw_graph(after, raw_steps[after_state["source_step_id"]], "after_graph")
            if source_only:
                raw_flows = parse_mcsa_scheme_flows(raw_steps[before_state["source_step_id"]])["electron_flows"]
                _require(raw_flows == steps[before_state["source_step_id"]].get("electron_flows", []), "source flow witnesses differ from raw MRV")
                selected = {item["atom_id"] for item in before["atoms"]}
                expected = {item["atom_id"]: item for item in row["source_context"]["source_atom_annotations"]["rows"]}
                before_annotations, before_r = _raw_source_annotations(raw_steps[before_state["source_step_id"]], selected, "before_graph")
                after_annotations, after_r = _raw_source_annotations(raw_steps[after_state["source_step_id"]], selected, "after_graph")
                _require(before_annotations == after_annotations == expected, "source atom annotations differ from raw MRV")
                claimed_r = set(row["source_context"]["source_r_groups"]["element_r_atom_ids"])
                _require(before_r == after_r == claimed_r, "source element-R inventory differs from raw MRV")
            else:
                mapped_atoms = {
                    mapping["before_atom_id"]
                    for alternative in row["canonical_input_correspondence"]["map_alternatives"]
                    for mapping in alternative["canonical_to_before"]
                }
                raw_root = ET.fromstring(raw_steps[before_state["source_step_id"]]["content_utf8"])
                raw_labels = sorted({
                    atom.get("mrvExtraLabel")
                    for atom in raw_root.iter()
                    if atom.tag.rsplit("}", 1)[-1] == "atom"
                    and atom.get("id") in mapped_atoms
                    and atom.get("mrvExtraLabel")
                })
                _require(raw_labels == sorted(row["canonical_input_correspondence"]["raw_source_labels"]), "canonical raw source labels differ from raw MRV")
                _validate_rhea_sources(reaction, row, record, proposal, bindings, root)
                _validate_audit(row, bindings, root, panel)
    payload_hash = transformation_payload_sha256(data)
    _validate_review(data["review"], payload_hash)
    return {
        "transformation_set_id": set_id,
        "transformation_payload_sha256": payload_hash,
        "transformation_count": len(rows),
        "record_count": len(record_ids),
    }


__all__ = [
    "SCHEMA_VERSION",
    "SCHEMA_VERSION_V2",
    "apply_graph_edits",
    "replay_graph_edits",
    "transformation_payload_sha256",
    "validate_transformations",
]
