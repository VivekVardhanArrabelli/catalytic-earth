"""Reviewed comparisons between source panels with incomplete node continuity.

This contract keeps complete source-panel depictions while replaying edits only
on the induced subgraphs whose locator correspondence is visible in both
panels.  Unmatched nodes are missing next-panel evidence, not deleted atoms.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

from .atlas10_source_adapters import parse_mcsa_scheme_flows
from .atlas_transformations import (
    _array,
    _edge_key,
    _exact,
    _integer,
    _object,
    _require,
    _sha,
    _string,
    _validate_binding_path,
    _validate_edits,
    _validate_graph,
    _validate_record_binding,
    _validate_review,
    _validate_state_pair,
    apply_graph_edits,
    replay_graph_edits,
)


SCHEMA_VERSION = "catalytic-earth.partial-panel-comparisons.v1"

_COVERAGE_KEYS = {
    "before_node_count",
    "after_node_count",
    "mapped_node_count",
    "unmatched_before_atom_ids",
    "unmatched_after_atom_ids",
    "before_boundary_bonds",
    "after_boundary_bonds",
    "replayed_edit_ids",
    "after_graph_unverified_edit_ids",
    "source_flow_ids",
    "source_flow_covered_edit_ids",
    "flow_coverage",
    "full_before_formal_charge",
    "full_after_formal_charge",
    "projected_before_formal_charge",
    "projected_after_formal_charge",
    "projection_replays_exactly",
    "full_panel_replay_asserted",
}

_SCOPE_KEYS = {
    "retained_projection_replay",
    "complete_panel_replay",
    "canonical_participant_correspondence",
    "physical_atom_map",
    "omitted_nodes_are_deleted",
    "unverified_edits_are_after_graph_confirmed",
    "complete_mechanism_path",
    "experimentally_observed_intermediate",
    "stereochemistry_assignment",
}

_NODE_KEYS = {
    "atom_id",
    "x2",
    "y2",
    "isotope",
    "mrv_extra_label",
    "mrv_alias",
    "rgroup_ref",
}


def comparison_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every comparison declaration except its manual review block."""

    data = _object(value, "partial panel comparisons")
    return _sha({key: item for key, item in data.items() if key != "review"})


def _validate_nodes(value: Any, graph: dict[str, Any], label: str) -> list[dict[str, Any]]:
    rows = _array(value, label)
    graph_ids = [item["atom_id"] for item in graph["atoms"]]
    _require(len(rows) == len(graph_ids), f"{label} does not cover every graph node")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(rows):
        row = _object(raw, f"{label}[{index}]")
        _exact(row, _NODE_KEYS, f"{label}[{index}]")
        atom_id = _string(row["atom_id"], f"{label}[{index}].atom_id")
        _require(atom_id not in seen, f"{label} repeats {atom_id}")
        seen.add(atom_id)
        for key in ("x2", "y2"):
            _string(row[key], f"{label}[{index}].{key}")
        for key in ("isotope", "mrv_extra_label", "mrv_alias", "rgroup_ref"):
            _require(row[key] is None or isinstance(row[key], str), f"{label}[{index}].{key} must be a string or null")
        result.append(row)
    _require([item["atom_id"] for item in result] == graph_ids, f"{label} order differs from its graph")
    return result


def _match_key(node: dict[str, Any], atoms: dict[str, dict[str, Any]]) -> tuple[Any, ...]:
    return (
        atoms[node["atom_id"]]["element"],
        node["x2"],
        node["y2"],
        node["isotope"],
        node["mrv_extra_label"],
        node["mrv_alias"],
        node["rgroup_ref"],
    )


def _unique_locator_map(
    before_graph: dict[str, Any],
    after_graph: dict[str, Any],
    before_nodes: list[dict[str, Any]],
    after_nodes: list[dict[str, Any]],
) -> list[dict[str, str]]:
    before_atoms = {item["atom_id"]: item for item in before_graph["atoms"]}
    after_atoms = {item["atom_id"]: item for item in after_graph["atoms"]}
    before_by_key: dict[tuple[Any, ...], list[str]] = {}
    after_by_key: dict[tuple[Any, ...], list[str]] = {}
    for row in before_nodes:
        before_by_key.setdefault(_match_key(row, before_atoms), []).append(row["atom_id"])
    for row in after_nodes:
        after_by_key.setdefault(_match_key(row, after_atoms), []).append(row["atom_id"])
    result = []
    for row in before_nodes:
        key = _match_key(row, before_atoms)
        if len(before_by_key[key]) == 1 and len(after_by_key.get(key, [])) == 1:
            result.append({"before_atom_id": row["atom_id"], "after_atom_id": after_by_key[key][0]})
    return result


def _validate_map(
    value: Any,
    before_ids: set[str],
    after_ids: set[str],
    label: str,
) -> list[dict[str, str]]:
    rows = _array(value, label)
    _require(bool(rows), f"{label} is empty")
    left: set[str] = set()
    right: set[str] = set()
    result: list[dict[str, str]] = []
    for index, raw in enumerate(rows):
        row = _object(raw, f"{label}[{index}]")
        _exact(row, {"before_atom_id", "after_atom_id"}, f"{label}[{index}]")
        before_id = _string(row["before_atom_id"], f"{label}[{index}].before_atom_id")
        after_id = _string(row["after_atom_id"], f"{label}[{index}].after_atom_id")
        _require(
            before_id in before_ids and after_id in after_ids
            and before_id not in left and after_id not in right,
            f"{label} is not a valid partial bijection",
        )
        left.add(before_id)
        right.add(after_id)
        result.append(row)
    return result


def _project_graph(graph: dict[str, Any], selected: set[str], suffix: str) -> dict[str, Any]:
    return {
        "graph_id": f"{graph['graph_id']}:{suffix}",
        "atom_id_scope": graph["atom_id_scope"],
        "atoms": [copy.deepcopy(item) for item in graph["atoms"] if item["atom_id"] in selected],
        "bonds": [
            copy.deepcopy(item)
            for item in graph["bonds"]
            if set(item["atom_ids"]) <= selected
        ],
    }


def _crossing_bonds(graph: dict[str, Any], selected: set[str]) -> list[dict[str, Any]]:
    return [
        copy.deepcopy(item)
        for item in graph["bonds"]
        if len(set(item["atom_ids"]) & selected) == 1
    ]


def _validate_flow_rows(
    value: Any,
    edits: list[dict[str, Any]],
    *,
    source_step_id: int | None = None,
    source_flows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    rows = _array(value, "source_flow_bindings")
    _require(bool(rows), "source_flow_bindings is empty")
    edits_by_id = {item["edit_id"]: item for item in edits}
    seen_flows: set[str] = set()
    covered: list[str] = []
    flow_index = {item.get("flow_id"): item for item in source_flows or []}
    if source_flows is not None:
        _require(len(flow_index) == len(source_flows), "source electron-flow IDs repeat")
    for index, raw in enumerate(rows):
        row = _object(raw, f"source_flow_bindings[{index}]")
        _exact(row, {"source_step_id", "flow_id", "edit_ids"}, f"source_flow_bindings[{index}]")
        step_id = _integer(row["source_step_id"], f"source_flow_bindings[{index}].source_step_id")
        flow_id = _string(row["flow_id"], f"source_flow_bindings[{index}].flow_id")
        _require(flow_id not in seen_flows, "source_flow_bindings repeats a flow")
        seen_flows.add(flow_id)
        if source_step_id is not None:
            _require(step_id == source_step_id, "source flow belongs to another step")
        edit_ids = _array(row["edit_ids"], f"source_flow_bindings[{index}].edit_ids")
        _require(bool(edit_ids), "source flow binding has no edits")
        for edit_id in edit_ids:
            _require(
                isinstance(edit_id, str) and edit_id in edits_by_id
                and edit_id not in covered
                and edits_by_id[edit_id]["source_flow_id"] == flow_id,
                "source flow edit coverage differs",
            )
            covered.append(edit_id)
        if source_flows is not None:
            _require(flow_id in flow_index, "source flow binding is absent from Atlas10")
            point_sets = [
                {
                    atom["source_atom_ref"].rsplit(".", 1)[-1]
                    for atom in point.get("atoms", [])
                }
                for point in (flow_index[flow_id]["source_point"], flow_index[flow_id]["target_point"])
            ]
            _require(all(set(edits_by_id[item]["atom_ids"]) in point_sets for item in edit_ids), "graph edit does not match one ordered source-flow point")
            endpoint_atoms = set().union(*point_sets)
            edit_atoms = {
                atom_id
                for edit_id in edit_ids
                for atom_id in edits_by_id[edit_id]["atom_ids"]
            }
            _require(edit_atoms == endpoint_atoms, "graph edits do not cover every source-flow endpoint atom")
    edit_order = [item["edit_id"] for item in edits]
    _require(covered == edit_order, "source flow bindings must cover edits once in declared order")
    if source_flows is not None:
        _require([item["flow_id"] for item in rows] == [item["flow_id"] for item in source_flows], "source flow order or coverage differs from Atlas10")
    return rows


def derive_partial_panel_coverage(
    before_graph: dict[str, Any],
    after_graph: dict[str, Any],
    atom_map: list[dict[str, str]],
    proposed_graph_edits: list[dict[str, Any]],
    source_flow_bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Derive the exact visible and unverified portions of a partial comparison."""

    before = _validate_graph(copy.deepcopy(before_graph), "before_graph")
    after = _validate_graph(copy.deepcopy(after_graph), "after_graph")
    before_ids = {item["atom_id"] for item in before["atoms"]}
    after_ids = {item["atom_id"] for item in after["atoms"]}
    mapping_rows = _validate_map(copy.deepcopy(atom_map), before_ids, after_ids, "atom_map")
    mapped_before = {item["before_atom_id"] for item in mapping_rows}
    mapped_after = {item["after_atom_id"] for item in mapping_rows}
    _require(mapped_before != before_ids or mapped_after != after_ids, "partial comparison must leave at least one panel node unmatched")
    edits = _validate_edits(copy.deepcopy(proposed_graph_edits), before_ids, "proposed_graph_edits")
    flows = _validate_flow_rows(copy.deepcopy(source_flow_bindings), edits)

    # This result is intentionally discarded.  Applying all edits verifies only
    # their before-panel preconditions; it does not synthesize a claimed panel.
    apply_graph_edits(before, edits)
    replayed = [item for item in edits if set(item["atom_ids"]) <= mapped_before]
    unverified = [item for item in edits if not set(item["atom_ids"]) <= mapped_before]
    before_projection = _project_graph(before, mapped_before, "mapped-projection")
    after_projection = _project_graph(after, mapped_after, "mapped-projection")
    projection_exact = replay_graph_edits(before_projection, replayed, after_projection, mapping_rows)
    replayed_ids = [item["edit_id"] for item in replayed]
    unverified_ids = [item["edit_id"] for item in unverified]
    flow_coverage = []
    for flow in flows:
        flow_replayed = [item for item in flow["edit_ids"] if item in replayed_ids]
        flow_unverified = [item for item in flow["edit_ids"] if item in unverified_ids]
        status = (
            "fully_replayed" if flow_replayed and not flow_unverified
            else "partially_replayed" if flow_replayed and flow_unverified
            else "after_graph_unverified"
        )
        flow_coverage.append(
            {
                "flow_id": flow["flow_id"],
                "replayed_edit_ids": flow_replayed,
                "after_graph_unverified_edit_ids": flow_unverified,
                "status": status,
            }
        )
    return {
        "before_node_count": len(before["atoms"]),
        "after_node_count": len(after["atoms"]),
        "mapped_node_count": len(mapping_rows),
        "unmatched_before_atom_ids": [item["atom_id"] for item in before["atoms"] if item["atom_id"] not in mapped_before],
        "unmatched_after_atom_ids": [item["atom_id"] for item in after["atoms"] if item["atom_id"] not in mapped_after],
        "before_boundary_bonds": _crossing_bonds(before, mapped_before),
        "after_boundary_bonds": _crossing_bonds(after, mapped_after),
        "replayed_edit_ids": replayed_ids,
        "after_graph_unverified_edit_ids": unverified_ids,
        "source_flow_ids": [item["flow_id"] for item in flows],
        "source_flow_covered_edit_ids": [edit_id for item in flows for edit_id in item["edit_ids"]],
        "flow_coverage": flow_coverage,
        "full_before_formal_charge": sum(item["formal_charge"] for item in before["atoms"]),
        "full_after_formal_charge": sum(item["formal_charge"] for item in after["atoms"]),
        "projected_before_formal_charge": sum(item["formal_charge"] for item in before_projection["atoms"]),
        "projected_after_formal_charge": sum(item["formal_charge"] for item in after_projection["atoms"]),
        "projection_replays_exactly": projection_exact,
        "full_panel_replay_asserted": False,
    }


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _raw_panel(content: str, label: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError(f"{label} raw MRV is malformed") from error
    atoms = []
    nodes = []
    seen: set[str] = set()
    for raw in (item for item in root.iter() if _local_name(item) == "atom"):
        atom_id = raw.get("id")
        element = raw.get("elementType")
        x2, y2 = raw.get("x2"), raw.get("y2")
        _require(atom_id is not None and atom_id not in seen and element is not None and x2 is not None and y2 is not None, f"{label} raw atom is incomplete or repeated")
        seen.add(atom_id)
        try:
            charge = int(raw.get("formalCharge", "0"))
        except ValueError as error:
            raise ValueError(f"{label} raw formal charge is unsupported") from error
        atoms.append({"atom_id": atom_id, "element": element, "formal_charge": charge, "stereochemistry": None})
        nodes.append(
            {
                "atom_id": atom_id,
                "x2": x2,
                "y2": y2,
                "isotope": raw.get("isotope"),
                "mrv_extra_label": raw.get("mrvExtraLabel"),
                "mrv_alias": raw.get("mrvAlias"),
                "rgroup_ref": raw.get("rgroupRef"),
            }
        )
    _require(bool(atoms), f"{label} raw MRV has no atoms")
    bonds = []
    seen_edges: set[tuple[str, str]] = set()
    for raw in (item for item in root.iter() if _local_name(item) == "bond"):
        refs = (raw.get("atomRefs2") or "").split()
        _require(len(refs) == 2 and all(item in seen for item in refs), f"{label} raw bond endpoints differ")
        _require(raw.get("convention") is None and not any(_local_name(item) == "bondStereo" for item in raw), f"{label} raw source contains unsupported stereochemistry")
        try:
            order = int(raw.get("order", ""))
        except ValueError as error:
            raise ValueError(f"{label} raw bond order is unsupported") from error
        _require(order in {1, 2, 3}, f"{label} raw bond order is unsupported")
        edge = _edge_key(refs)
        _require(edge not in seen_edges, f"{label} raw bond repeats")
        seen_edges.add(edge)
        bonds.append({"atom_ids": refs, "order": order})
    return {
        "graph_id": label,
        "atom_id_scope": "source_panel_local_locator",
        "atoms": atoms,
        "bonds": bonds,
    }, nodes


def _validate_raw_sources(
    row: dict[str, Any],
    panels: dict[str, Any],
    steps: dict[int, dict[str, Any]],
    binding: dict[str, Any],
    root: Path,
) -> None:
    source = json.loads((root / binding["path"]).read_text(encoding="utf-8"))
    mcsa_id = row["record_binding"]["mcsa_id"]
    _require(
        source.get("source") == "M-CSA" and source.get("record_id") == mcsa_id
        and source.get("entry", {}).get("mcsa_id") == int(mcsa_id[1:]),
        "raw M-CSA source identity differs",
    )
    mechanism_id = row["proposal_binding"]["source_mechanism_id"]
    schemes = [item for item in source.get("step_schemes", []) if item.get("mechanism_id") == mechanism_id]
    raw_steps = {item.get("step_id"): item for item in schemes}
    _require(len(raw_steps) == len(schemes), "raw source mechanism repeats a step")
    for state_name in ("before", "after"):
        state = row["state_pair"][state_name]
        raw = raw_steps.get(state["source_step_id"])
        _require(isinstance(raw, dict) and raw.get("content_sha256") == state["scheme_sha256"], f"raw {state_name} scheme binding differs")
        content = raw.get("content_utf8")
        _require(isinstance(content, str) and hashlib.sha256(content.encode("utf-8")).hexdigest() == state["scheme_sha256"], f"raw {state_name} scheme content differs")
        graph, nodes = _raw_panel(content, f"raw-{state_name}")
        declared_graph = panels[f"{state_name}_graph"]
        raw_bonds = {_edge_key(item["atom_ids"]): item["order"] for item in graph["bonds"]}
        declared_bonds = {_edge_key(item["atom_ids"]): item["order"] for item in declared_graph["bonds"]}
        _require(graph["atoms"] == declared_graph["atoms"] and raw_bonds == declared_bonds, f"{state_name} graph differs from raw MRV")
        _require(nodes == panels[f"{state_name}_nodes"], f"{state_name} node metadata differs from raw MRV")
    before_id = row["state_pair"]["before"]["source_step_id"]
    raw_flows = parse_mcsa_scheme_flows(raw_steps[before_id])["electron_flows"]
    compiled_flows = steps[before_id].get("electron_flows", [])
    _require(raw_flows == compiled_flows, "source flow witnesses differ from raw MRV")
    _validate_flow_rows(
        row["source_flow_bindings"],
        row["proposed_graph_edits"],
        source_step_id=before_id,
        source_flows=raw_flows,
    )


def validate_panel_comparisons(
    value: Any,
    *,
    atlas10_bundle: dict[str, Any],
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate partial source panels and optionally rederive their raw facts."""

    data = _object(value, "partial panel comparisons")
    _exact(data, {"schema_version", "comparison_set_id", "status", "source_bindings", "comparisons", "review"}, "partial panel comparisons")
    _require(data["schema_version"] == SCHEMA_VERSION and data["status"] == "reviewed", "comparison set schema/status differs")
    set_id = _string(data["comparison_set_id"], "comparison_set_id")
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

    rows = _array(data["comparisons"], "comparisons")
    _require(bool(rows), "comparisons is empty")
    comparison_ids: set[str] = set()
    record_ids: set[str] = set()
    bundle = _object(atlas10_bundle, "atlas10_bundle")
    for index, raw in enumerate(rows):
        row = _object(raw, f"comparisons[{index}]")
        _exact(
            row,
            {"comparison_id", "record_binding", "proposal_binding", "state_pair", "source_panels", "correspondence", "proposed_graph_edits", "source_flow_bindings", "coverage", "scope_effect", "mandatory_abstentions"},
            f"comparisons[{index}]",
        )
        comparison_id = _string(row["comparison_id"], f"comparisons[{index}].comparison_id")
        _require(comparison_id not in comparison_ids, f"comparison_id repeats {comparison_id}")
        comparison_ids.add(comparison_id)
        record, proposal, steps = _validate_record_binding(row, bundle)
        del record, proposal
        record_ids.add(row["record_binding"]["record_id"])
        _validate_state_pair(row["state_pair"], steps)
        mcsa_id = row["record_binding"]["mcsa_id"]
        source_binding = bindings.get(f"source:M-CSA:{mcsa_id}")
        _require(source_binding is not None and source_binding["sha256"] == row["record_binding"]["source_snapshot_sha256"], "M-CSA source binding differs")

        panels = _object(row["source_panels"], "source_panels")
        _exact(panels, {"before_graph", "after_graph", "before_nodes", "after_nodes"}, "source_panels")
        before = _validate_graph(panels["before_graph"], "before_graph")
        after = _validate_graph(panels["after_graph"], "after_graph")
        _require(all(item["stereochemistry"] is None for graph in (before, after) for item in graph["atoms"]), "partial source panels cannot assert stereochemistry")
        before_nodes = _validate_nodes(panels["before_nodes"], before, "before_nodes")
        after_nodes = _validate_nodes(panels["after_nodes"], after, "after_nodes")

        correspondence = _object(row["correspondence"], "correspondence")
        _exact(correspondence, {"method", "interpretation", "atom_map"}, "correspondence")
        _require(correspondence["method"] == "unique_exact_source_position_and_identity", "correspondence method differs")
        _require(correspondence["interpretation"] == "project_reviewed_panel_alignment_not_physical_atom_map", "correspondence interpretation differs")
        atom_map = _validate_map(
            correspondence["atom_map"],
            {item["atom_id"] for item in before["atoms"]},
            {item["atom_id"] for item in after["atoms"]},
            "correspondence.atom_map",
        )
        expected_map = _unique_locator_map(before, after, before_nodes, after_nodes)
        _require(atom_map == expected_map, "correspondence is not the exhaustive unique source-locator match")

        edits = _validate_edits(row["proposed_graph_edits"], {item["atom_id"] for item in before["atoms"]}, "proposed_graph_edits")
        _require(all(item["operation"] != "set_stereochemistry" for item in edits), "partial source comparison cannot assert a stereochemistry edit")
        source_flows = [
            item for item in steps[row["state_pair"]["before"]["source_step_id"]].get("electron_flows", [])
        ]
        _validate_flow_rows(
            row["source_flow_bindings"], edits,
            source_step_id=row["state_pair"]["before"]["source_step_id"],
            source_flows=source_flows,
        )
        coverage = _object(row["coverage"], "coverage")
        _exact(coverage, _COVERAGE_KEYS, "coverage")
        derived = derive_partial_panel_coverage(before, after, atom_map, edits, row["source_flow_bindings"])
        # Canonical JSON comparison keeps booleans distinct from integers; bare
        # Python equality would accept True == 1 and False == 0.
        _require(_sha(coverage) == _sha(derived), "declared partial-panel coverage differs from derived coverage")
        _require(coverage["projection_replays_exactly"] is True and coverage["full_panel_replay_asserted"] is False, "partial-panel replay scope differs")

        scope = _object(row["scope_effect"], "scope_effect")
        _exact(scope, _SCOPE_KEYS, "scope_effect")
        _require(all(isinstance(item, bool) for item in scope.values()), "scope_effect values must be boolean")
        _require(scope["retained_projection_replay"] and not any(scope[key] for key in _SCOPE_KEYS - {"retained_projection_replay"}), "scope_effect promotes an unsupported partial-panel claim")
        abstentions = _array(row["mandatory_abstentions"], "mandatory_abstentions")
        abstention_ids: set[str] = set()
        for abstention_index, raw_abstention in enumerate(abstentions):
            abstention = _object(raw_abstention, f"mandatory_abstentions[{abstention_index}]")
            _exact(abstention, {"abstention_id", "reason"}, f"mandatory_abstentions[{abstention_index}]")
            abstention_id = _string(abstention["abstention_id"], f"mandatory_abstentions[{abstention_index}].abstention_id")
            _require(abstention_id not in abstention_ids, "mandatory abstention repeats")
            abstention_ids.add(abstention_id)
            _string(abstention["reason"], f"mandatory_abstentions[{abstention_index}].reason")
        required = (_SCOPE_KEYS - {"retained_projection_replay"}) | {"water_hydrogen_correspondence", "released_peptide_after_graph"}
        _require(required <= abstention_ids, "mandatory abstentions omit an unsupported scope")
        if root is not None:
            _validate_raw_sources(row, panels, steps, source_binding, root)

    payload_hash = comparison_payload_sha256(data)
    _validate_review(data["review"], payload_hash)
    return {
        "comparison_set_id": set_id,
        "comparison_payload_sha256": payload_hash,
        "comparison_count": len(rows),
        "record_count": len(record_ids),
    }


__all__ = [
    "SCHEMA_VERSION",
    "comparison_payload_sha256",
    "derive_partial_panel_coverage",
    "validate_panel_comparisons",
]
