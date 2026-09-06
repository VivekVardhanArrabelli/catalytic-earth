"""Deterministic, unreviewed candidates from adjacent retained M-CSA panels.

The extractor reports only source-depiction locator continuity, graph deltas,
and ordered curved-arrow coverage.  Its output is deliberately not a reviewed
atlas record and contains no review pin or evidence-tier effect.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any
import xml.etree.ElementTree as ET

from .atlas10_source_adapters import parse_mcsa_scheme_flows
from .atlas_partial_panels import (
    _crossing_bonds,
    _project_graph,
    _raw_panel,
    derive_partial_panel_coverage,
)
from .atlas_transformations import (
    _edge_key,
    _graph_rows,
    apply_graph_edits,
    replay_graph_edits,
)


SCHEMA_VERSION = "catalytic-earth.panel-candidate.v1"

_SCOPE_EFFECT = {
    "unreviewed_candidate": True,
    "reviewed_evidence": False,
    "physical_atom_map": False,
    "canonical_participant_correspondence": False,
    "source_omission_is_atom_deletion": False,
    "synthesized_product_graph": False,
    "stereochemistry_assignment": False,
    "lone_pair_annotations_replayed": False,
    "complete_mechanism_path": False,
    "experimentally_validated": False,
}

_MATCH_FIELDS = (
    "element",
    "x2",
    "y2",
    "isotope",
    "mrv_extra_label",
    "mrv_alias",
    "rgroup_ref",
)


class _NeedsReview(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _source_atom_id(reference: str) -> str:
    return reference.rsplit(".", 1)[-1]


def _decode_snapshot(snapshot_bytes: bytes) -> tuple[dict[str, Any], str]:
    _require(isinstance(snapshot_bytes, bytes), "snapshot_bytes must be bytes")
    try:
        value = json.loads(snapshot_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("snapshot_bytes is not valid UTF-8 JSON") from error
    _require(isinstance(value, dict), "M-CSA snapshot must be an object")
    record_id = value.get("record_id")
    _require(
        value.get("source") == "M-CSA"
        and isinstance(record_id, str)
        and re.fullmatch(r"M[0-9]{4}", record_id) is not None,
        "M-CSA snapshot identity differs",
    )
    entry = value.get("entry")
    _require(
        isinstance(entry, dict) and entry.get("mcsa_id") == int(record_id[1:]),
        "M-CSA entry identity differs",
    )
    return value, record_id


def _select_steps(
    snapshot: dict[str, Any], mechanism_id: int, before_step_id: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    _require(isinstance(mechanism_id, int) and not isinstance(mechanism_id, bool) and mechanism_id > 0, "mechanism_id must be a positive integer")
    _require(isinstance(before_step_id, int) and not isinstance(before_step_id, bool) and before_step_id > 0, "before_step_id must be a positive integer")
    mechanisms = snapshot.get("entry", {}).get("reaction", {}).get("mechanisms")
    _require(isinstance(mechanisms, list), "M-CSA mechanism rows are missing")
    selected_mechanisms = [item for item in mechanisms if isinstance(item, dict) and item.get("mechanism_id") == mechanism_id]
    _require(len(selected_mechanisms) == 1, "mechanism_id does not select exactly one mechanism")
    source_step_ids = [item.get("step_id") for item in selected_mechanisms[0].get("steps", []) if isinstance(item, dict)]
    after_step_id = before_step_id + 1
    _require(source_step_ids.count(before_step_id) == 1 and source_step_ids.count(after_step_id) == 1, "requested adjacent source steps are missing or repeated")
    schemes = snapshot.get("step_schemes")
    _require(isinstance(schemes, list), "M-CSA step schemes are missing")
    selected = {
        step_id: [
            item for item in schemes
            if isinstance(item, dict)
            and item.get("mechanism_id") == mechanism_id
            and item.get("step_id") == step_id
        ]
        for step_id in (before_step_id, after_step_id)
    }
    _require(all(len(rows) == 1 for rows in selected.values()), "requested scheme does not occur exactly once")
    before, after = selected[before_step_id][0], selected[after_step_id][0]
    for label, scheme in (("before", before), ("after", after)):
        content = scheme.get("content_utf8")
        digest = scheme.get("content_sha256")
        _require(isinstance(content, str) and isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{label} scheme content/hash is missing")
        _require(hashlib.sha256(content.encode("utf-8")).hexdigest() == digest, f"{label} embedded scheme hash differs")
    return before, after


def _base_candidate(
    record_id: str,
    snapshot_sha256: str,
    mechanism_id: int,
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    before_id, after_id = before["step_id"], after["step_id"]
    return {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": f"panel-candidate:{record_id}:mechanism-{mechanism_id}:steps-{before_id}-{after_id}",
        "status": "unreviewed",
        "extraction_status": "candidate",
        "source_binding": {
            "provider": "M-CSA",
            "record_id": record_id,
            "snapshot_sha256": snapshot_sha256,
            "mechanism_id": mechanism_id,
            "before_step_id": before_id,
            "after_step_id": after_id,
            "before_scheme_sha256": before["content_sha256"],
            "after_scheme_sha256": after["content_sha256"],
        },
        "source_panels": None,
        "correspondence": None,
        "proposed_graph_edits": [],
        "source_flow_bindings": [],
        "coverage": None,
        "diagnostics": [],
        "scope_effect": copy.deepcopy(_SCOPE_EFFECT),
    }


def _needs_review(
    candidate: dict[str, Any], code: str, detail: str
) -> dict[str, Any]:
    result = copy.deepcopy(candidate)
    result["extraction_status"] = "needs_review"
    result["proposed_graph_edits"] = []
    result["source_flow_bindings"] = []
    result["coverage"] = None
    result["diagnostics"] = [{"code": code, "detail": detail}]
    return result


def _preflight_panel(content: str, label: str, *, check_flows: bool) -> None:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError(f"{label} MRV is malformed") from error
    atoms = [item for item in root.iter() if _local_name(item) == "atom"]
    if any(
        raw.get("atomParity") is not None
        or raw.get("chirality") is not None
        or any(_local_name(item) == "atomParity" for item in raw)
        for raw in atoms
    ):
        raise _NeedsReview(
            "stereochemistry_requires_review",
            f"{label} panel contains source atom stereochemistry data",
        )
    if any(raw.get("elementType") == "*" for raw in atoms):
        raise _NeedsReview(
            "unsupported_source_format",
            f"{label} panel contains an unsupported wildcard atom",
        )
    bonds = [item for item in root.iter() if _local_name(item) == "bond"]
    if any(
        raw.get("convention") is not None
        or any(_local_name(item) == "bondStereo" for item in raw)
        for raw in bonds
    ):
        raise _NeedsReview(
            "stereochemistry_requires_review",
            f"{label} panel contains source stereochemistry or bond-convention data",
        )
    for raw in bonds:
        try:
            order = int(raw.get("order", ""))
        except ValueError:
            order = 0
        if order not in {1, 2, 3}:
            raise _NeedsReview(
                "unsupported_source_format",
                f"{label} panel contains a bond order outside the supported integer covalent orders",
            )
    if not check_flows:
        return
    seen_flow_ids: set[str] = set()
    for raw in (item for item in root.iter() if _local_name(item) == "MEFlow"):
        children = list(raw)
        tags = [_local_name(item) for item in children]
        base_point = bool(tags) and tags[0] == "MEFlowBasePoint"
        expected_attributes = {"id", "arcAngle"}
        if base_point:
            expected_attributes |= {
                "baseElectronContainerIndex",
                "baseElectronIndexInContainer",
            }
        if (
            set(raw.attrib) != expected_attributes
            or not raw.get("id")
            or raw.get("id") in seen_flow_ids
            or raw.get("arcAngle") not in {"90", "270"}
            or (base_point and raw.get("baseElectronContainerIndex") != "0")
            or (base_point and raw.get("baseElectronIndexInContainer") != "-1")
            or len(children) != 2
            or tags[0] not in {"MEFlowBasePoint", "MAtomSetPoint"}
            or tags[1] != "MAtomSetPoint"
        ):
            raise _NeedsReview(
                "unsupported_source_format",
                f"{label} panel contains unsupported electron-flow attributes or point shape",
            )
        seen_flow_ids.add(raw.get("id", ""))
        for point, tag in zip(children, tags, strict=True):
            expected_point_attributes = (
                {"atomRef"} if tag == "MEFlowBasePoint" else {"atomRefs"}
            )
            if (
                set(point.attrib) != expected_point_attributes
                or list(point)
                or not next(iter(point.attrib.values()), "").strip()
            ):
                raise _NeedsReview(
                    "unsupported_source_format",
                    f"{label} panel contains an unsupported electron-flow point",
                )


def _match_key(
    node: dict[str, Any], atoms: dict[str, dict[str, Any]]
) -> tuple[Any, ...]:
    return (
        atoms[node["atom_id"]]["element"],
        node["x2"],
        node["y2"],
        node["isotope"],
        node["mrv_extra_label"],
        node["mrv_alias"],
        node["rgroup_ref"],
    )


def _key_object(key: tuple[Any, ...]) -> dict[str, Any]:
    return dict(zip(_MATCH_FIELDS, key, strict=True))


def _derive_correspondence(
    before_graph: dict[str, Any],
    after_graph: dict[str, Any],
    before_nodes: list[dict[str, Any]],
    after_nodes: list[dict[str, Any]],
) -> dict[str, Any]:
    before_atoms = {item["atom_id"]: item for item in before_graph["atoms"]}
    after_atoms = {item["atom_id"]: item for item in after_graph["atoms"]}
    before_by_key: dict[tuple[Any, ...], list[str]] = {}
    after_by_key: dict[tuple[Any, ...], list[str]] = {}
    for row in before_nodes:
        before_by_key.setdefault(_match_key(row, before_atoms), []).append(row["atom_id"])
    for row in after_nodes:
        after_by_key.setdefault(_match_key(row, after_atoms), []).append(row["atom_id"])
    keys = set(before_by_key) | set(after_by_key)
    ambiguous_keys = [
        key for key in keys
        if len(before_by_key.get(key, [])) > 1 or len(after_by_key.get(key, [])) > 1
    ]
    ambiguous = [
        {
            "match_key": _key_object(key),
            "before_atom_ids": before_by_key.get(key, []),
            "after_atom_ids": after_by_key.get(key, []),
        }
        for key in sorted(
            ambiguous_keys,
            key=lambda item: json.dumps(_key_object(item), sort_keys=True, separators=(",", ":")),
        )
    ]
    mapping = []
    for row in before_nodes:
        key = _match_key(row, before_atoms)
        if len(before_by_key[key]) == 1 and len(after_by_key.get(key, [])) == 1:
            mapping.append(
                {"before_atom_id": row["atom_id"], "after_atom_id": after_by_key[key][0]}
            )
    return {
        "method": "unique_exact_source_position_and_identity",
        "interpretation": "project_unreviewed_panel_alignment_not_physical_atom_map",
        "atom_map": mapping,
        "ambiguous_matches": ambiguous,
    }


def _projected_deltas(
    before: dict[str, Any], after: dict[str, Any], atom_map: list[dict[str, str]]
) -> list[dict[str, Any]]:
    mapping = {item["before_atom_id"]: item["after_atom_id"] for item in atom_map}
    inverse = {right: left for left, right in mapping.items()}
    before_ids, after_ids = set(mapping), set(inverse)
    before_projection = _project_graph(before, before_ids, "candidate-projection")
    after_projection = _project_graph(after, after_ids, "candidate-projection")
    before_atoms, before_bonds = _graph_rows(before_projection)
    after_atoms, after_bonds_raw = _graph_rows(after_projection)
    after_bonds = {
        _edge_key([inverse[left], inverse[right]]): order
        for (left, right), order in after_bonds_raw.items()
    }
    order_index = {item["atom_id"]: index for index, item in enumerate(before["atoms"])}

    def ordered_atoms(atom_ids: tuple[str, str]) -> list[str]:
        return sorted(atom_ids, key=order_index.__getitem__)

    deltas: list[dict[str, Any]] = []
    for key in sorted(set(before_bonds) | set(after_bonds), key=lambda ids: tuple(order_index[item] for item in ids)):
        old, new = before_bonds.get(key, 0), after_bonds.get(key, 0)
        if old == new:
            continue
        operation = "remove_bond" if new == 0 else "add_bond" if old == 0 else "set_bond_order"
        deltas.append({"operation": operation, "atom_ids": ordered_atoms(key), "before": old, "after": new})
    for before_id in [item["atom_id"] for item in before["atoms"] if item["atom_id"] in mapping]:
        after_id = mapping[before_id]
        old, new = before_atoms[before_id]["formal_charge"], after_atoms[after_id]["formal_charge"]
        if old != new:
            deltas.append({"operation": "set_formal_charge", "atom_ids": [before_id], "before": old, "after": new})
    return deltas


def _flow_view(flows: list[dict[str, Any]], before_ids: set[str]) -> list[dict[str, Any]]:
    result = []
    seen: set[str] = set()
    for index, flow in enumerate(flows):
        flow_id = flow.get("flow_id")
        if not isinstance(flow_id, str) or not flow_id or flow_id in seen:
            raise _NeedsReview("unsupported_source_format", "source arrows lack unique explicit identifiers")
        seen.add(flow_id)
        sides = []
        for name in ("source_point", "target_point"):
            point = flow.get(name)
            if not isinstance(point, dict) or point.get("point_kind") not in {"electron_base_atom", "atom_set"}:
                raise _NeedsReview("unsupported_source_format", f"{flow_id} has an unsupported arrow point")
            atom_ids = [_source_atom_id(item.get("source_atom_ref", "")) for item in point.get("atoms", []) if isinstance(item, dict)]
            if len(atom_ids) not in {1, 2} or len(set(atom_ids)) != len(atom_ids) or any(item not in before_ids for item in atom_ids):
                raise _NeedsReview("unsupported_source_format", f"{flow_id} has unsupported or unknown arrow endpoints")
            sides.append(atom_ids)
        if set(sides[0]) == set(sides[1]):
            raise _NeedsReview("contradictory_source_arrow", f"{flow_id} has indistinguishable source and target point sets")
        result.append({"index": index, "flow_id": flow_id, "source": sides[0], "target": sides[1]})
    if not result:
        raise _NeedsReview("unsupported_source_format", "before panel has no supported source arrows")
    return result


def _assign_delta(delta: dict[str, Any], flows: list[dict[str, Any]]) -> tuple[int, int]:
    refs = set(delta["atom_ids"])
    operation = delta["operation"]
    if operation == "set_formal_charge":
        increase = delta["after"] > delta["before"]
        side = 0 if increase else 1
        matches = [
            flow["index"] for flow in flows
            if len(flow[("source", "target")[side]]) == 1
            and set(flow[("source", "target")[side]]) == refs
        ]
        if len(matches) == 1:
            return matches[0], side
    else:
        decrease = delta["after"] < delta["before"]
        side = 0 if decrease else 1
        matches = [
            flow["index"] for flow in flows
            if len(flow[("source", "target")[side]]) == 2
            and set(flow[("source", "target")[side]]) == refs
        ]
        if len(matches) == 1:
            return matches[0], side
    raise _NeedsReview(
        "contradictory_source_arrow",
        f"mapped graph delta {operation} on {','.join(delta['atom_ids'])} lacks one uniquely oriented source arrow",
    )


def _derive_edits(
    before: dict[str, Any],
    before_step_id: int,
    atom_map: list[dict[str, str]],
    deltas: list[dict[str, Any]],
    flows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mapped = {item["before_atom_id"] for item in atom_map}
    _, before_bonds = _graph_rows(before)
    order_index = {item["atom_id"]: index for index, item in enumerate(before["atoms"])}
    assigned: list[dict[str, Any]] = []
    represented: set[tuple[int, int]] = set()
    for delta in deltas:
        flow_index, side = _assign_delta(delta, flows)
        assigned.append({**delta, "flow_index": flow_index, "side": side, "support": "after_graph_confirmed"})
        represented.add((flow_index, side))

    for flow in flows:
        for side, side_name in enumerate(("source", "target")):
            refs = flow[side_name]
            if len(refs) != 2 or (flow["index"], side) in represented:
                continue
            if set(refs) <= mapped:
                raise _NeedsReview(
                    "contradictory_source_arrow",
                    f"{flow['flow_id']} {side_name} pair is fully mapped but has no oriented after-graph delta",
                )
            key = _edge_key(refs)
            current = before_bonds.get(key, 0)
            if side == 0 and current == 1:
                operation, old, new = "remove_bond", 1, 0
            elif side == 1 and current == 0:
                operation, old, new = "add_bond", 0, 1
            else:
                raise _NeedsReview(
                    "unsupported_source_format",
                    f"{flow['flow_id']} {side_name} pair cannot yield the bounded single-bond arrow-only proposal",
                )
            assigned.append(
                {
                    "operation": operation,
                    "atom_ids": sorted(refs, key=order_index.__getitem__),
                    "before": old,
                    "after": new,
                    "flow_index": flow["index"],
                    "side": side,
                    "support": "source_arrow_only",
                }
            )
            represented.add((flow["index"], side))

    def sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
        return (
            item["flow_index"],
            1 if item["operation"] == "set_formal_charge" else 0,
            item["side"],
            tuple(order_index[atom_id] for atom_id in item["atom_ids"]),
            item["operation"],
        )

    assigned.sort(key=sort_key)
    edits = []
    for index, item in enumerate(assigned, 1):
        flow = flows[item["flow_index"]]
        edits.append(
            {
                "edit_id": f"e{index}",
                "operation": item["operation"],
                "atom_ids": item["atom_ids"],
                "before": item["before"],
                "after": item["after"],
                "source_flow_id": flow["flow_id"],
                "support": item["support"],
            }
        )
    flow_bindings = []
    for flow in flows:
        edit_ids = [item["edit_id"] for item in edits if item["source_flow_id"] == flow["flow_id"]]
        endpoint_union = set(flow["source"]) | set(flow["target"])
        edit_union = {
            atom_id for item in edits if item["source_flow_id"] == flow["flow_id"] for atom_id in item["atom_ids"]
        }
        if not edit_ids or edit_union != endpoint_union:
            raise _NeedsReview(
                "contradictory_source_arrow",
                f"{flow['flow_id']} source endpoints are not completely covered by bounded proposals",
            )
        flow_bindings.append(
            {"source_step_id": before_step_id, "flow_id": flow["flow_id"], "edit_ids": edit_ids}
        )
    return edits, flow_bindings


def _standard_edits(edits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in item.items() if key != "support"}
        for item in edits
    ]


def _full_coverage(
    before: dict[str, Any],
    after: dict[str, Any],
    atom_map: list[dict[str, str]],
    edits: list[dict[str, Any]],
    flows: list[dict[str, Any]],
) -> dict[str, Any]:
    standard = _standard_edits(edits)
    exact = replay_graph_edits(before, standard, after, atom_map)
    return {
        "before_node_count": len(before["atoms"]),
        "after_node_count": len(after["atoms"]),
        "mapped_node_count": len(atom_map),
        "unmatched_before_atom_ids": [],
        "unmatched_after_atom_ids": [],
        "before_boundary_bonds": [],
        "after_boundary_bonds": [],
        "replayed_edit_ids": [item["edit_id"] for item in edits],
        "after_graph_unverified_edit_ids": [],
        "source_flow_ids": [item["flow_id"] for item in flows],
        "source_flow_covered_edit_ids": [edit_id for flow in flows for edit_id in flow["edit_ids"]],
        "flow_coverage": [
            {
                "flow_id": flow["flow_id"],
                "replayed_edit_ids": list(flow["edit_ids"]),
                "after_graph_unverified_edit_ids": [],
                "status": "fully_replayed",
            }
            for flow in flows
        ],
        "full_before_formal_charge": sum(item["formal_charge"] for item in before["atoms"]),
        "full_after_formal_charge": sum(item["formal_charge"] for item in after["atoms"]),
        "projected_before_formal_charge": sum(item["formal_charge"] for item in before["atoms"]),
        "projected_after_formal_charge": sum(item["formal_charge"] for item in after["atoms"]),
        "projection_replays_exactly": exact,
        "full_panel_replay_asserted": exact,
    }


def extract_panel_candidate(
    snapshot_bytes: bytes,
    *,
    mechanism_id: int,
    before_step_id: int,
) -> dict[str, Any]:
    """Extract an unreviewed adjacent-panel graph candidate from retained bytes."""

    snapshot, record_id = _decode_snapshot(snapshot_bytes)
    before_scheme, after_scheme = _select_steps(snapshot, mechanism_id, before_step_id)
    candidate = _base_candidate(
        record_id,
        hashlib.sha256(snapshot_bytes).hexdigest(),
        mechanism_id,
        before_scheme,
        after_scheme,
    )
    try:
        _preflight_panel(before_scheme["content_utf8"], "before", check_flows=True)
        _preflight_panel(after_scheme["content_utf8"], "after", check_flows=False)
        before_graph, before_nodes = _raw_panel(
            before_scheme["content_utf8"],
            f"{record_id}:mechanism-{mechanism_id}:step-{before_step_id}:full-source-panel",
        )
        after_graph, after_nodes = _raw_panel(
            after_scheme["content_utf8"],
            f"{record_id}:mechanism-{mechanism_id}:step-{before_step_id + 1}:full-source-panel",
        )
        candidate["source_panels"] = {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_nodes": before_nodes,
            "after_nodes": after_nodes,
        }
        correspondence = _derive_correspondence(
            before_graph, after_graph, before_nodes, after_nodes
        )
        candidate["correspondence"] = correspondence
        if correspondence["ambiguous_matches"]:
            raise _NeedsReview(
                "ambiguous_locator_key",
                "one or more exact source position-and-identity keys are non-unique",
            )
        if not correspondence["atom_map"]:
            raise _NeedsReview(
                "ambiguous_locator_key", "adjacent panels have no unique exact locator matches"
            )
        try:
            raw_flows = parse_mcsa_scheme_flows(before_scheme)["electron_flows"]
        except ValueError as error:
            raise _NeedsReview("unsupported_source_format", str(error)) from error
        flow_views = _flow_view(
            raw_flows, {item["atom_id"] for item in before_graph["atoms"]}
        )
        deltas = _projected_deltas(
            before_graph, after_graph, correspondence["atom_map"]
        )
        edits, flow_bindings = _derive_edits(
            before_graph,
            before_step_id,
            correspondence["atom_map"],
            deltas,
            flow_views,
        )
        standard = _standard_edits(edits)
        try:
            apply_graph_edits(before_graph, standard)
            full_map = (
                len(correspondence["atom_map"]) == len(before_graph["atoms"])
                == len(after_graph["atoms"])
            )
            if full_map:
                if any(item["support"] != "after_graph_confirmed" for item in edits):
                    raise _NeedsReview(
                        "contradictory_source_arrow",
                        "a complete locator map produced an after-graph-unverified edit",
                    )
                coverage = _full_coverage(
                    before_graph, after_graph, correspondence["atom_map"], edits, flow_bindings
                )
            else:
                coverage = derive_partial_panel_coverage(
                    before_graph,
                    after_graph,
                    correspondence["atom_map"],
                    standard,
                    flow_bindings,
                )
        except _NeedsReview:
            raise
        except ValueError as error:
            raise _NeedsReview("failed_mapped_replay", str(error)) from error
        if not coverage["projection_replays_exactly"]:
            raise _NeedsReview(
                "failed_mapped_replay",
                "derived edits do not exactly reproduce the mapped after-panel projection",
            )
        confirmed = [item["edit_id"] for item in edits if item["support"] == "after_graph_confirmed"]
        arrow_only = [item["edit_id"] for item in edits if item["support"] == "source_arrow_only"]
        if confirmed != coverage["replayed_edit_ids"] or arrow_only != coverage["after_graph_unverified_edit_ids"]:
            raise _NeedsReview(
                "failed_mapped_replay", "edit evidence classes differ from mapped-node coverage"
            )
        candidate["proposed_graph_edits"] = edits
        candidate["source_flow_bindings"] = flow_bindings
        candidate["coverage"] = coverage
        return candidate
    except _NeedsReview as review:
        return _needs_review(candidate, review.code, review.detail)


__all__ = ["SCHEMA_VERSION", "extract_panel_candidate"]
