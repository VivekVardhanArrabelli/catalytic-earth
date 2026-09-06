"""Unreviewed panel candidates with narrow opaque source context preservation.

This module projects supported source drawing annotations out of the covalent
graph, delegates graph/edit extraction to :mod:`atlas_candidate_extraction`,
and then proves that those uninterpreted annotations are unchanged, fully
mapped, and disjoint from every proposed edit.  It does not interpret stereo,
coordinate chemistry, or physical atom identity.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any
import xml.etree.ElementTree as ET

from .atlas_candidate_extraction import (
    _base_candidate,
    _decode_snapshot,
    _select_steps,
    extract_panel_candidate,
)


SCHEMA_VERSION = "catalytic-earth.context-panel-candidate.v1"

_COUNT_KEYS = ("bond_stereo", "atom_parity", "bond_conventions")

_CONTEXT_SCOPE = {
    "opaque_annotations_preserved": True,
    "stereochemistry_interpreted": False,
    "coordination_chemistry_interpreted": False,
    "covalent_graph_excludes_convention_bonds": True,
    "full_source_electronic_state_replayed": False,
}

_STEREO_MARKERS = ("stereo", "parity", "chiral")


class _ContextReview(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"unsupported JSON numeric constant: {value}")


def _strict_snapshot(snapshot_bytes: bytes) -> dict[str, Any]:
    if not isinstance(snapshot_bytes, bytes):
        raise ValueError("snapshot_bytes must be bytes")
    try:
        value = json.loads(
            snapshot_bytes.decode("utf-8"),
            object_pairs_hook=_unique_keys,
            parse_constant=_invalid_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("snapshot_bytes is not valid strict UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise ValueError("M-CSA snapshot must be an object")
    entry = value.get("entry")
    if (
        not isinstance(entry, dict)
        or type(entry.get("mcsa_id")) is not int
        or entry["mcsa_id"] <= 0
    ):
        raise ValueError("M-CSA entry ID must be a positive integer")
    reaction = entry.get("reaction")
    mechanisms = reaction.get("mechanisms") if isinstance(reaction, dict) else None
    schemes = value.get("step_schemes")
    if not isinstance(mechanisms, list) or not isinstance(schemes, list):
        raise ValueError("M-CSA mechanism or scheme rows are missing")
    for mechanism in mechanisms:
        if (
            not isinstance(mechanism, dict)
            or type(mechanism.get("mechanism_id")) is not int
            or mechanism["mechanism_id"] <= 0
            or not isinstance(mechanism.get("steps"), list)
        ):
            raise ValueError("M-CSA mechanism IDs must be positive integers")
        for step in mechanism["steps"]:
            if (
                not isinstance(step, dict)
                or type(step.get("step_id")) is not int
                or step["step_id"] <= 0
            ):
                raise ValueError("M-CSA entry step IDs must be positive integers")
    for scheme in schemes:
        if (
            not isinstance(scheme, dict)
            or type(scheme.get("mechanism_id")) is not int
            or scheme["mechanism_id"] <= 0
            or type(scheme.get("step_id")) is not int
            or scheme["step_id"] <= 0
        ):
            raise ValueError("M-CSA scheme IDs must be positive integers")
    return value


def _empty_preservation(reason: str) -> dict[str, Any]:
    return {
        "status": "needs_review",
        "before_counts": None,
        "after_counts": None,
        "matched_counts": None,
        "special_before_atom_ids": [],
        "special_after_atom_ids": [],
        "all_references_mapped": None,
        "ordered_metadata_preserved": None,
        "before_special_boundary_bonds": [],
        "after_special_boundary_bonds": [],
        "no_special_boundary_bonds": None,
        "proposed_edit_endpoints_disjoint": None,
        "reason": reason,
    }


def _context_candidate_base(
    record_id: str,
    snapshot_sha256: str,
    mechanism_id: int,
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    result = _base_candidate(
        record_id, snapshot_sha256, mechanism_id, before, after
    )
    result["schema_version"] = SCHEMA_VERSION
    result["candidate_id"] = (
        f"panel-context-candidate:{record_id}:mechanism-{mechanism_id}:"
        f"steps-{before['step_id']}-{after['step_id']}"
    )
    result["opaque_source_context"] = None
    result["context_preservation"] = _empty_preservation(
        "opaque source context has not been evaluated"
    )
    result["scope_effect"].update(copy.deepcopy(_CONTEXT_SCOPE))
    return result


def _needs_review(
    candidate: dict[str, Any],
    code: str,
    detail: str,
    *,
    capture_complete: bool,
) -> dict[str, Any]:
    candidate["extraction_status"] = "needs_review"
    candidate["proposed_graph_edits"] = []
    candidate["source_flow_bindings"] = []
    candidate["coverage"] = None
    candidate["diagnostics"] = [{"code": code, "detail": detail}]
    candidate["scope_effect"]["opaque_annotations_preserved"] = capture_complete
    if not capture_complete:
        candidate["opaque_source_context"] = None
        candidate["context_preservation"] = _empty_preservation(detail)
    return candidate


def _parse_panel(
    content: str,
    scheme_sha256: str,
    label: str,
) -> tuple[dict[str, Any], str]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError(f"{label} MRV is malformed") from error

    if any(
        marker in name.casefold()
        for item in root.iter()
        for name in item.attrib
        for marker in _STEREO_MARKERS
    ):
        raise _ContextReview(
            "unsupported_opaque_source_context",
            f"{label} uses an unsupported stereo-related XML attribute",
        )

    atoms: list[str] = []
    atom_ids: set[str] = set()
    for atom in (item for item in root.iter() if _local_name(item) == "atom"):
        atom_id = atom.get("id")
        if not atom_id or atom_id in atom_ids:
            raise ValueError(f"{label} atom identifiers are missing or repeated")
        atom_ids.add(atom_id)
        atoms.append(atom_id)
        if any(_local_name(child) == "atomParity" for child in atom):
            raise _ContextReview(
                "unsupported_opaque_source_context",
                f"{label} contains atomParity, which this bounded context schema does not interpret",
            )
    if not atoms:
        raise ValueError(f"{label} MRV contains no atoms")
    if any(_local_name(item) == "atomParity" for item in root.iter()):
        raise _ContextReview(
            "unsupported_opaque_source_context",
            f"{label} contains atomParity outside the supported empty context",
        )

    bond_stereo: list[dict[str, Any]] = []
    bond_conventions: list[dict[str, Any]] = []
    bond_ids: set[str] = set()
    bond_pairs: set[tuple[str, str]] = set()
    captured_stereo_children: set[ET.Element] = set()
    parent_by_child = {
        child: parent for parent in root.iter() for child in list(parent)
    }
    convention_bonds: list[ET.Element] = []
    for bond in (item for item in root.iter() if _local_name(item) == "bond"):
        bond_id = bond.get("id")
        refs = (bond.get("atomRefs2") or "").split()
        if (
            not bond_id
            or bond_id in bond_ids
            or len(refs) != 2
            or len(set(refs)) != 2
            or any(atom_id not in atom_ids for atom_id in refs)
        ):
            raise ValueError(f"{label} bond identifiers or endpoints are invalid")
        bond_ids.add(bond_id)
        pair = tuple(sorted(refs))
        if pair in bond_pairs:
            raise _ContextReview(
                "unsupported_opaque_source_context",
                f"{label} repeats one undirected bond pair across source rows",
            )
        bond_pairs.add(pair)
        children = list(bond)
        stereo_children = [
            item for item in children if _local_name(item) == "bondStereo"
        ]
        convention = bond.get("convention")
        if convention is not None:
            if (
                convention != "cxn:coord"
                or set(bond.attrib) != {"id", "atomRefs2", "convention"}
                or children
            ):
                raise _ContextReview(
                    "unsupported_opaque_source_context",
                    f"{label} contains an unsupported or decorated bond convention",
                )
            bond_conventions.append(
                {
                    "bond_id": bond_id,
                    "ordered_atom_refs2": refs,
                    "order_token": None,
                    "raw_convention": convention,
                }
            )
            convention_bonds.append(bond)
            continue
        if children:
            if (
                len(children) != 1
                or len(stereo_children) != 1
                or set(bond.attrib) != {"id", "atomRefs2", "order"}
            ):
                raise _ContextReview(
                    "unsupported_opaque_source_context",
                    f"{label} contains an unsupported bond child or special-bond attributes",
                )
            stereo = stereo_children[0]
            raw_text = stereo.text
            if (
                raw_text not in {"W", "H"}
                or stereo.attrib
                or list(stereo)
                or bond.get("order") not in {"1", "2", "3"}
            ):
                raise _ContextReview(
                    "unsupported_opaque_source_context",
                    f"{label} contains an unsupported bondStereo form",
                )
            bond_stereo.append(
                {
                    "bond_id": bond_id,
                    "ordered_atom_refs2": refs,
                    "order_token": bond.get("order"),
                    "raw_text": raw_text,
                    "raw_attributes": {},
                }
            )
            captured_stereo_children.add(stereo)
            bond.remove(stereo)
        elif set(bond.attrib) != {"id", "atomRefs2", "order"}:
            raise _ContextReview(
                "unsupported_opaque_source_context",
                f"{label} contains unsupported ordinary-bond attributes",
            )

    if any(
        _local_name(item) == "bondStereo" and item not in captured_stereo_children
        for item in root.iter()
    ):
        raise _ContextReview(
            "unsupported_opaque_source_context",
            f"{label} contains bondStereo outside one supported bond child",
        )

    for bond in convention_bonds:
        parent = parent_by_child.get(bond)
        if parent is None:
            raise ValueError(f"{label} convention bond lacks a parent")
        parent.remove(bond)

    context = {
        "scheme_sha256": scheme_sha256,
        "bond_stereo": bond_stereo,
        "atom_parity": [],
        "bond_conventions": bond_conventions,
    }
    projected = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return context, projected


def _private_snapshot(
    snapshot: dict[str, Any],
    mechanism_id: int,
    projections: dict[int, str],
) -> bytes:
    private = copy.deepcopy(snapshot)
    selected: set[int] = set()
    for scheme in private["step_schemes"]:
        if (
            isinstance(scheme, dict)
            and scheme.get("mechanism_id") == mechanism_id
            and scheme.get("step_id") in projections
        ):
            step_id = scheme["step_id"]
            scheme["content_utf8"] = projections[step_id]
            scheme["content_sha256"] = hashlib.sha256(
                projections[step_id].encode("utf-8")
            ).hexdigest()
            selected.add(step_id)
    if selected != set(projections):
        raise ValueError("private covalent projection does not cover both source panels")
    return json.dumps(
        private, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _count(context: dict[str, Any]) -> dict[str, int]:
    return {key: len(context[key]) for key in _COUNT_KEYS}


def _special_atoms(context: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for row in context["bond_stereo"]:
        result.update(row["ordered_atom_refs2"])
    for row in context["atom_parity"]:
        result.add(row["atom_id"])
        result.update(row["ordered_atom_refs4"])
    for row in context["bond_conventions"]:
        result.update(row["ordered_atom_refs2"])
    return result


def _signature(
    kind: str,
    row: dict[str, Any],
    mapping: dict[str, str] | None,
) -> tuple[Any, ...]:
    def mapped(atom_id: str) -> str:
        return mapping[atom_id] if mapping is not None else atom_id

    if kind == "bond_stereo":
        return (
            tuple(mapped(item) for item in row["ordered_atom_refs2"]),
            row["order_token"],
            row["raw_text"],
            tuple(sorted(row["raw_attributes"].items())),
        )
    if kind == "atom_parity":
        return (
            mapped(row["atom_id"]),
            tuple(mapped(item) for item in row["ordered_atom_refs4"]),
            row["raw_text"],
            tuple(sorted(row["raw_attributes"].items())),
        )
    return (
        tuple(mapped(item) for item in row["ordered_atom_refs2"]),
        row["order_token"],
        row["raw_convention"],
    )


def _ordered_subset(atom_order: list[str], selected: set[str]) -> list[str]:
    return [atom_id for atom_id in atom_order if atom_id in selected]


def _validate_context_preservation(
    candidate: dict[str, Any],
    before_context: dict[str, Any],
    after_context: dict[str, Any],
    *,
    assess_edit_disjointness: bool,
) -> dict[str, Any]:
    correspondence = candidate.get("correspondence")
    if not isinstance(correspondence, dict):
        return _empty_preservation(
            "base candidate did not establish a locator correspondence"
        )
    rows = correspondence.get("atom_map")
    if not isinstance(rows, list):
        return _empty_preservation(
            "base candidate did not expose a locator correspondence"
        )
    mapping = {
        row["before_atom_id"]: row["after_atom_id"]
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("before_atom_id"), str)
        and isinstance(row.get("after_atom_id"), str)
    }
    inverse = {right: left for left, right in mapping.items()}
    before_special = _special_atoms(before_context)
    after_special = _special_atoms(after_context)
    panels = candidate.get("source_panels")
    before_order = (
        [item["atom_id"] for item in panels["before_graph"]["atoms"]]
        if isinstance(panels, dict)
        else []
    )
    after_order = (
        [item["atom_id"] for item in panels["after_graph"]["atoms"]]
        if isinstance(panels, dict)
        else []
    )
    before_counts = _count(before_context)
    after_counts = _count(after_context)
    result = {
        "status": "needs_review",
        "before_counts": before_counts,
        "after_counts": after_counts,
        "matched_counts": None,
        "special_before_atom_ids": _ordered_subset(before_order, before_special),
        "special_after_atom_ids": _ordered_subset(after_order, after_special),
        "all_references_mapped": False,
        "ordered_metadata_preserved": False,
        "before_special_boundary_bonds": [],
        "after_special_boundary_bonds": [],
        "no_special_boundary_bonds": None,
        "proposed_edit_endpoints_disjoint": None,
        "reason": "opaque source context has not passed all preservation gates",
    }
    if not before_special <= set(mapping) or not after_special <= set(inverse):
        result["reason"] = "one or more opaque source-context references are unmatched"
        return result
    result["all_references_mapped"] = True

    matched_counts: dict[str, int] = {}
    for kind in _COUNT_KEYS:
        before_signatures = [
            _signature(kind, row, mapping) for row in before_context[kind]
        ]
        after_signatures = [
            _signature(kind, row, None) for row in after_context[kind]
        ]
        if (
            len(set(before_signatures)) != len(before_signatures)
            or len(set(after_signatures)) != len(after_signatures)
            or before_signatures != after_signatures
        ):
            result["matched_counts"] = matched_counts
            result["reason"] = (
                f"{kind} rows change, reverse, repeat, or reorder across the locator map"
            )
            return result
        matched_counts[kind] = len(before_signatures)
    result["matched_counts"] = matched_counts
    result["ordered_metadata_preserved"] = True

    mapped_before = set(mapping)
    mapped_after = set(inverse)
    before_boundary = [
        copy.deepcopy(bond)
        for bond in panels["before_graph"]["bonds"]
        if len(set(bond["atom_ids"]) & mapped_before) == 1
        and bool(set(bond["atom_ids"]) & before_special)
    ]
    after_boundary = [
        copy.deepcopy(bond)
        for bond in panels["after_graph"]["bonds"]
        if len(set(bond["atom_ids"]) & mapped_after) == 1
        and bool(set(bond["atom_ids"]) & after_special)
    ]
    result["before_special_boundary_bonds"] = before_boundary
    result["after_special_boundary_bonds"] = after_boundary
    result["no_special_boundary_bonds"] = not before_boundary and not after_boundary

    if assess_edit_disjointness:
        edit_atoms = {
            atom_id
            for edit in candidate.get("proposed_graph_edits", [])
            if isinstance(edit, dict)
            for atom_id in edit.get("atom_ids", [])
            if isinstance(atom_id, str)
        }
        result["proposed_edit_endpoints_disjoint"] = not (
            edit_atoms & before_special
        )
    if not result["no_special_boundary_bonds"]:
        result["reason"] = (
            "an opaque source-context reference has an unmatched covalent neighbor"
        )
        return result
    if not assess_edit_disjointness:
        result["reason"] = (
            "Proposed-edit disjointness was not assessed because delegated "
            "covalent extraction needs review."
        )
        return result

    if not result["proposed_edit_endpoints_disjoint"]:
        result["reason"] = (
            "one or more proposed edits overlap an opaque source-context reference"
        )
        return result
    result["status"] = "preserved_opaque_context_disjoint_from_proposed_edits"
    result["reason"] = (
        "Supported raw annotations are unchanged under the locator map and are "
        "retained without stereochemical or coordination interpretation."
    )
    return result


def _rename_coverage(candidate: dict[str, Any]) -> None:
    coverage = candidate.get("coverage")
    if isinstance(coverage, dict) and "full_panel_replay_asserted" in coverage:
        coverage["full_covalent_graph_replay_asserted"] = coverage.pop(
            "full_panel_replay_asserted"
        )


def extract_context_panel_candidate(
    snapshot_bytes: bytes,
    *,
    mechanism_id: int,
    before_step_id: int,
) -> dict[str, Any]:
    """Extract a covalent candidate while preserving supported context opaquely."""

    snapshot = _strict_snapshot(snapshot_bytes)
    decoded, record_id = _decode_snapshot(snapshot_bytes)
    if decoded != snapshot:
        raise ValueError("strict and source snapshot decoders differ")
    before, after = _select_steps(snapshot, mechanism_id, before_step_id)
    candidate = _context_candidate_base(
        record_id,
        hashlib.sha256(snapshot_bytes).hexdigest(),
        mechanism_id,
        before,
        after,
    )
    try:
        before_context, before_projection = _parse_panel(
            before["content_utf8"], before["content_sha256"], "before"
        )
        after_context, after_projection = _parse_panel(
            after["content_utf8"], after["content_sha256"], "after"
        )
    except _ContextReview as review:
        return _needs_review(
            candidate,
            review.code,
            review.detail,
            capture_complete=False,
        )

    candidate["opaque_source_context"] = {
        "before": before_context,
        "after": after_context,
    }
    private_bytes = _private_snapshot(
        snapshot,
        mechanism_id,
        {before["step_id"]: before_projection, after["step_id"]: after_projection},
    )
    delegated = extract_panel_candidate(
        private_bytes,
        mechanism_id=mechanism_id,
        before_step_id=before_step_id,
    )
    for key in (
        "extraction_status",
        "source_panels",
        "correspondence",
        "proposed_graph_edits",
        "source_flow_bindings",
        "coverage",
        "diagnostics",
    ):
        candidate[key] = copy.deepcopy(delegated[key])
    panels = candidate.get("source_panels")
    if isinstance(panels, dict):
        for name in ("before_graph", "after_graph"):
            graph = panels.get(name)
            if isinstance(graph, dict) and isinstance(graph.get("graph_id"), str):
                graph["graph_id"] = graph["graph_id"].replace(
                    ":full-source-panel", ":full-covalent-source-panel"
                )
    candidate["source_binding"] = copy.deepcopy(
        _base_candidate(
            record_id,
            hashlib.sha256(snapshot_bytes).hexdigest(),
            mechanism_id,
            before,
            after,
        )["source_binding"]
    )
    _rename_coverage(candidate)
    preservation = _validate_context_preservation(
        candidate,
        before_context,
        after_context,
        assess_edit_disjointness=candidate["extraction_status"] == "candidate",
    )
    candidate["context_preservation"] = preservation
    if candidate["extraction_status"] != "candidate":
        return candidate
    if preservation["status"] != "preserved_opaque_context_disjoint_from_proposed_edits":
        reason = preservation["reason"]
        if not preservation["all_references_mapped"]:
            code = "opaque_context_unmapped"
        elif not preservation["ordered_metadata_preserved"]:
            code = "opaque_context_changed"
        elif not preservation["no_special_boundary_bonds"]:
            code = "opaque_context_unmapped_boundary"
        else:
            code = "opaque_context_overlaps_proposed_edit"
        return _needs_review(
            candidate, code, reason, capture_complete=True
        )
    return candidate


__all__ = ["SCHEMA_VERSION", "extract_context_panel_candidate"]
