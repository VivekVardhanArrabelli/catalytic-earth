#!/usr/bin/env python3
"""Reproduce the retained M0173 Step 1 -> Step 2 source-panel audit.

This checker uses only Python's standard library.  It reads the immutable
M-CSA snapshot already retained by the repository, derives the two complete
depiction-node graphs, checks six reviewed source-flow-bound edits, and verifies that
the edits replay the second panel exactly.  It does not resolve the source R
groups or assign a canonical chemical participant.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = REPO / "data/atlas/atlas10/sources/mcsa/M0173.json"
OUTPUT = HERE / "retained_graph_audit.json"

EXPECTED_SOURCE_SHA256 = "d3db64e9a1db6e22e8baae48a738bff261a2296f375a884c19f2f4abc7d8f22e"
EXPECTED_SCHEME_SHA256 = {
    1: "61e6e50dce4e376699ebbf430c3190a0805efc0586d33f683e31b0f3c7263eab",
    2: "7cc3b37af574d0bb078bd46059d6559729ee4bb633ec7190b273182af0497f88",
}
EXPECTED_FLOWS = {
    "o24": [
        {"kind": "MAtomSetPoint", "atom_refs": ["a44", "a50"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a44", "a3"]},
    ],
    "o25": [
        {"kind": "MAtomSetPoint", "atom_refs": ["a3", "a10"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a10"]},
    ],
    "o26": [
        {"kind": "MEFlowBasePoint", "atom_refs": ["a21"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a21", "a50"]},
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _natural(atom_id: str) -> tuple[str, int]:
    prefix = atom_id.rstrip("0123456789")
    suffix = atom_id[len(prefix) :]
    return prefix, int(suffix) if suffix else -1


def _canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _parse_step(row: dict[str, object]) -> dict[str, object]:
    source_text = str(row["content_utf8"])
    source_bytes = source_text.encode("utf-8")
    if hashlib.sha256(source_bytes).hexdigest() != row["content_sha256"]:
        raise ValueError(f"Step {row['step_id']} content hash differs")
    root = ET.fromstring(source_text)
    molecules = [node for node in root.iter() if _local(node.tag) == "molecule"]
    if len(molecules) != 1 or molecules[0].get("molID") != "m1":
        raise ValueError(f"Step {row['step_id']} molecule layout differs")

    atoms: dict[str, dict[str, str]] = {}
    atom_order: list[str] = []
    for node in root.iter():
        if _local(node.tag) != "atom":
            continue
        atom_id = node.get("id")
        if not atom_id or atom_id in atoms:
            raise ValueError(f"Step {row['step_id']} atom identifier differs")
        atoms[atom_id] = dict(node.attrib)
        atom_order.append(atom_id)

    bonds: dict[tuple[str, str], int] = {}
    bond_rows: list[dict[str, object]] = []
    for node in root.iter():
        if _local(node.tag) != "bond":
            continue
        refs = node.get("atomRefs2", "").split()
        if len(refs) != 2 or any(ref not in atoms for ref in refs):
            raise ValueError(f"Step {row['step_id']} bond endpoint differs")
        stereo_nodes = [child for child in node if _local(child.tag) == "bondStereo"]
        if len(stereo_nodes) > 1:
            raise ValueError(f"Step {row['step_id']} has an unsupported stereo row")
        bond_row = {
            "bond_id": node.get("id"),
            "atom_ids": refs,
            "order": node.get("order"),
            "convention": node.get("convention"),
            "bond_stereo": None
            if not stereo_nodes
            else {"text": stereo_nodes[0].text, "attributes": dict(stereo_nodes[0].attrib)},
        }
        bond_rows.append(bond_row)
        if node.get("convention") == "cxn:coord":
            continue
        if node.get("order") not in {"1", "2", "3"}:
            raise ValueError(f"Step {row['step_id']} covalent bond order differs")
        key = tuple(sorted(refs))
        if key in bonds:
            raise ValueError(f"Step {row['step_id']} repeats a covalent edge")
        bonds[key] = int(node.get("order", "0"))

    flows: list[dict[str, object]] = []
    for node in root.iter():
        if _local(node.tag) != "MEFlow":
            continue
        points: list[dict[str, object]] = []
        for child in node:
            raw_refs = child.get("atomRefs") or child.get("atomRef") or ""
            refs = raw_refs.replace("m1.", "").split()
            if not refs or any(ref not in atoms for ref in refs):
                raise ValueError(f"Step {row['step_id']} flow endpoint differs")
            points.append({"kind": _local(child.tag), "atom_refs": refs})
        flows.append({"flow_id": node.get("id"), "points": points})

    graph = {
        "graph_id": f"M0173:mechanism-1:step-{row['step_id']}:full-source-panel",
        "atom_id_scope": "source_panel_local_locator",
        "atoms": [
            {
                "atom_id": atom_id,
                "element": atoms[atom_id]["elementType"],
                "formal_charge": int(atoms[atom_id].get("formalCharge", "0")),
                "stereochemistry": None,
            }
            for atom_id in atom_order
        ],
        "bonds": [
            {"atom_ids": list(edge), "order": bonds[edge]}
            for edge in sorted(bonds, key=lambda pair: (_natural(pair[0]), _natural(pair[1])))
        ],
    }

    adjacency = {atom_id: set() for atom_id in atoms}
    for left, right in bonds:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components: list[list[str]] = []
    seen: set[str] = set()
    for seed in atom_order:
        if seed in seen:
            continue
        todo = [seed]
        seen.add(seed)
        component: list[str] = []
        while todo:
            current = todo.pop()
            component.append(current)
            for neighbor in sorted(adjacency[current], key=_natural, reverse=True):
                if neighbor not in seen:
                    seen.add(neighbor)
                    todo.append(neighbor)
        components.append(sorted(component, key=_natural))

    annotations = [
        {
            "atom_id": atom_id,
            "mrv_extra_label": atom.get("mrvExtraLabel"),
            "mrv_alias": atom.get("mrvAlias"),
            "rgroup_ref": atom.get("rgroupRef"),
        }
        for atom_id, atom in ((atom_id, atoms[atom_id]) for atom_id in atom_order)
        if any(atom.get(key) is not None for key in ("mrvExtraLabel", "mrvAlias", "rgroupRef"))
    ]
    return {
        "step_id": row["step_id"],
        "scheme_sha256": row["content_sha256"],
        "atom_attributes": atoms,
        "atom_order": atom_order,
        "bond_rows": bond_rows,
        "graph": graph,
        "flows": flows,
        "components": components,
        "source_atom_annotations": annotations,
    }


def _apply_edits(graph: dict[str, object], edits: list[dict[str, object]]) -> dict[str, object]:
    atoms = {row["atom_id"]: dict(row) for row in graph["atoms"]}
    bonds = {tuple(sorted(row["atom_ids"])): row["order"] for row in graph["bonds"]}
    for edit in edits:
        refs = edit["atom_ids"]
        if edit["operation"] in {"remove_bond", "add_bond", "set_bond_order"}:
            key = tuple(sorted(refs))
            if bonds.get(key, 0) != edit["before"]:
                raise ValueError(f"{edit['edit_id']} bond precondition differs")
            if edit["after"] == 0:
                bonds.pop(key, None)
            else:
                bonds[key] = edit["after"]
        elif edit["operation"] == "set_formal_charge":
            atom = atoms[refs[0]]
            if atom["formal_charge"] != edit["before"]:
                raise ValueError(f"{edit['edit_id']} charge precondition differs")
            atom["formal_charge"] = edit["after"]
        else:
            raise ValueError(f"{edit['edit_id']} operation is unsupported")
    return {
        "atoms": [atoms[row["atom_id"]] for row in graph["atoms"]],
        "bonds": [
            {"atom_ids": list(edge), "order": bonds[edge]}
            for edge in sorted(bonds, key=lambda pair: (_natural(pair[0]), _natural(pair[1])))
        ],
    }


def _graph_content(graph: dict[str, object]) -> dict[str, object]:
    return {"atoms": graph["atoms"], "bonds": graph["bonds"]}


def _build() -> dict[str, object]:
    if _sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise ValueError("M0173 source snapshot hash differs")
    wrapped = json.loads(SOURCE.read_text(encoding="utf-8"))
    if wrapped.get("record_id") != "M0173":
        raise ValueError("M0173 source record identity differs")
    selected = {
        int(row["step_id"]): row
        for row in wrapped.get("step_schemes", [])
        if row.get("mechanism_id") == 1 and row.get("step_id") in {1, 2}
    }
    if set(selected) != {1, 2}:
        raise ValueError("M0173 state-pair source coverage differs")
    for step_id, expected in EXPECTED_SCHEME_SHA256.items():
        if selected[step_id].get("content_sha256") != expected:
            raise ValueError(f"M0173 Step {step_id} source hash differs")

    before = _parse_step(selected[1])
    after = _parse_step(selected[2])
    if before["atom_order"] != after["atom_order"] or before["atom_order"] != [f"a{i}" for i in range(1, 51)]:
        raise ValueError("M0173 source atom locator alignment differs")

    identity_keys = ("elementType", "mrvExtraLabel", "mrvAlias", "rgroupRef", "isotope")
    identity_differences: list[dict[str, object]] = []
    coordinate_differences: list[dict[str, object]] = []
    chemical_attribute_differences: list[dict[str, object]] = []
    for atom_id in before["atom_order"]:
        left = before["atom_attributes"][atom_id]
        right = after["atom_attributes"][atom_id]
        identity_changes = {key: [left.get(key), right.get(key)] for key in identity_keys if left.get(key) != right.get(key)}
        if identity_changes:
            identity_differences.append({"atom_id": atom_id, "changes": identity_changes})
        coordinate_changes = {key: [left.get(key), right.get(key)] for key in ("x2", "y2") if left.get(key) != right.get(key)}
        if coordinate_changes:
            coordinate_differences.append({"atom_id": atom_id, "changes": coordinate_changes})
        chemical_changes = {
            key: [left.get(key), right.get(key)]
            for key in ("formalCharge", "lonePair")
            if left.get(key) != right.get(key)
        }
        if chemical_changes:
            chemical_attribute_differences.append({"atom_id": atom_id, "changes": chemical_changes})
    if identity_differences or coordinate_differences:
        raise ValueError("M0173 source locator or identity attributes differ across the state pair")
    if before["source_atom_annotations"] != after["source_atom_annotations"]:
        raise ValueError("M0173 source annotations differ across the state pair")

    before_bonds = {tuple(row["atom_ids"]): row["order"] for row in before["graph"]["bonds"]}
    after_bonds = {tuple(row["atom_ids"]): row["order"] for row in after["graph"]["bonds"]}
    raw_bond_differences = [
        {"atom_ids": list(edge), "before": before_bonds.get(edge, 0), "after": after_bonds.get(edge, 0)}
        for edge in sorted(set(before_bonds) | set(after_bonds), key=lambda pair: (_natural(pair[0]), _natural(pair[1])))
        if before_bonds.get(edge) != after_bonds.get(edge)
    ]

    before_flow_rows = {row["flow_id"]: row["points"] for row in before["flows"]}
    if before_flow_rows != EXPECTED_FLOWS:
        raise ValueError("M0173 Step 1 electron-flow endpoints differ")
    edits = [
        {"edit_id": "e1", "operation": "remove_bond", "atom_ids": ["a44", "a50"], "before": 1, "after": 0, "source_flow_id": "o24"},
        {"edit_id": "e2", "operation": "add_bond", "atom_ids": ["a3", "a44"], "before": 0, "after": 1, "source_flow_id": "o24"},
        {"edit_id": "e3", "operation": "set_bond_order", "atom_ids": ["a3", "a10"], "before": 2, "after": 1, "source_flow_id": "o25"},
        {"edit_id": "e4", "operation": "set_formal_charge", "atom_ids": ["a10"], "before": 0, "after": -1, "source_flow_id": "o25"},
        {"edit_id": "e5", "operation": "add_bond", "atom_ids": ["a21", "a50"], "before": 0, "after": 1, "source_flow_id": "o26"},
        {"edit_id": "e6", "operation": "set_formal_charge", "atom_ids": ["a21"], "before": 0, "after": 1, "source_flow_id": "o26"},
    ]
    replayed = _apply_edits(before["graph"], edits)
    if replayed != _graph_content(after["graph"]):
        raise ValueError("M0173 six-edit replay does not reproduce Step 2")

    all_bond_stereo = [
        {"source_step_id": parsed["step_id"], **row}
        for parsed in (before, after)
        for row in parsed["bond_rows"]
        if row["bond_stereo"] is not None or row["convention"] is not None
    ]
    if all_bond_stereo:
        raise ValueError("M0173 retained state pair unexpectedly carries bond stereo or bond conventions")

    element_r = [
        atom_id for atom_id in before["atom_order"]
        if before["atom_attributes"][atom_id].get("elementType") == "R"
    ]
    alias_r = [
        atom_id for atom_id in before["atom_order"]
        if before["atom_attributes"][atom_id].get("mrvAlias") == "R"
    ]
    all_aliases = [
        {"atom_id": atom_id, "mrv_alias": before["atom_attributes"][atom_id]["mrvAlias"]}
        for atom_id in before["atom_order"]
        if before["atom_attributes"][atom_id].get("mrvAlias") is not None
    ]
    explicit_h = [
        {
            "atom_id": atom_id,
            "raw_label": before["atom_attributes"][atom_id].get("mrvExtraLabel"),
            "step_1_neighbors": sorted(
                [other for edge in before_bonds for other in edge if atom_id in edge and other != atom_id], key=_natural
            ),
            "step_2_neighbors": sorted(
                [other for edge in after_bonds for other in edge if atom_id in edge and other != atom_id], key=_natural
            ),
        }
        for atom_id in before["atom_order"]
        if before["atom_attributes"][atom_id].get("elementType") == "H"
    ]
    reused_bond_ids = []
    before_by_id = {row["bond_id"]: row for row in before["bond_rows"]}
    after_by_id = {row["bond_id"]: row for row in after["bond_rows"]}
    for bond_id in sorted(set(before_by_id) & set(after_by_id)):
        left, right = before_by_id[bond_id], after_by_id[bond_id]
        if left["atom_ids"] != right["atom_ids"] or left["order"] != right["order"]:
            reused_bond_ids.append({"bond_id": bond_id, "step_1": left, "step_2": right})

    return {
        "audit_schema_version": "catalytic-earth.m0173-source-panel-audit.v1",
        "audit_method": {
            "implementation": "python_stdlib_xml_elementtree",
            "script_path": "data/atlas/transformations/m0173/audit_m0173.py",
            "script_sha256": _sha256(Path(__file__)),
            "network_requests": 0,
        },
        "source_snapshot": {
            "path": SOURCE.relative_to(REPO).as_posix(),
            "sha256": _sha256(SOURCE),
            "record_id": "M0173",
        },
        "state_pair": {
            "same_50_depiction_node_ids": True,
            "same_coordinates": True,
            "same_source_identity_annotations": True,
            "atom_id_alignment_scope": "project_reviewed_same_token_alignment_not_upstream_atom_map",
            "step_1": {
                "scheme_sha256": before["scheme_sha256"],
                "node_count": len(before["atom_order"]),
                "element_counts": dict(sorted(Counter(row["element"] for row in before["graph"]["atoms"]).items())),
                "covalent_bond_count": len(before["graph"]["bonds"]),
                "component_count": len(before["components"]),
                "formal_charge_sum": sum(row["formal_charge"] for row in before["graph"]["atoms"]),
            },
            "step_2": {
                "scheme_sha256": after["scheme_sha256"],
                "node_count": len(after["atom_order"]),
                "element_counts": dict(sorted(Counter(row["element"] for row in after["graph"]["atoms"]).items())),
                "covalent_bond_count": len(after["graph"]["bonds"]),
                "component_count": len(after["components"]),
                "formal_charge_sum": sum(row["formal_charge"] for row in after["graph"]["atoms"]),
            },
        },
        "before_graph": before["graph"],
        "after_graph": after["graph"],
        "graph_edits": edits,
        "source_flow_bindings": [
            {"source_step_id": 1, "flow_id": "o24", "edit_ids": ["e1", "e2"]},
            {"source_step_id": 1, "flow_id": "o25", "edit_ids": ["e3", "e4"]},
            {"source_step_id": 1, "flow_id": "o26", "edit_ids": ["e5", "e6"]},
        ],
        "replay": {
            "status": "exact",
            "scope": "complete_50_source_depiction_node_graph",
            "atom_map": [
                {"before_atom_id": atom_id, "after_atom_id": atom_id}
                for atom_id in before["atom_order"]
            ],
        },
        "raw_checks": {
            "raw_bond_differences": raw_bond_differences,
            "chemical_atom_attribute_differences": chemical_attribute_differences,
            "source_identity_attribute_differences": identity_differences,
            "coordinate_differences": coordinate_differences,
            "bond_stereo_or_convention_rows": all_bond_stereo,
            "step_1_flow_points": before["flows"],
            "step_2_flow_points": after["flows"],
            "bond_identifier_reuse": reused_bond_ids,
        },
        "source_context": {
            "source_atom_annotations": before["source_atom_annotations"],
            "element_r_atom_ids": element_r,
            "alias_r_atom_ids": alias_r,
            "all_alias_rows": all_aliases,
            "explicit_hydrogen_rows": explicit_h,
            "step_1_components": before["components"],
            "step_2_components": after["components"],
        },
        "limits": [
            "The 50 graph vertices are source depiction nodes, not 50 asserted physical atoms.",
            "The elementType=R and mrvAlias=R source tokens are preserved without resolving generic peptide substituents.",
            "No bondStereo token occurs in either panel; the tetrahedral carbon created in Step 2 has no asserted stereochemical assignment.",
            "Shared atom identifiers and unchanged coordinates support a reviewed panel-locator alignment only; M-CSA does not supply an upstream atom map.",
            "Raw bond identifier b42 changes endpoints across the panels and is not used as a bond-continuity identifier.",
            "The audit makes no canonical participant, exact peptide, product, experimental-intermediate, or complete-path claim.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the committed audit is reproducible")
    args = parser.parse_args()
    result = _build()
    encoded = _canonical_bytes(result)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != encoded:
            print(f"{OUTPUT}: generated bytes differ", file=sys.stderr)
            return 1
        print(f"M0173 source-panel audit is reproducible: {hashlib.sha256(encoded).hexdigest()}")
        return 0
    OUTPUT.write_bytes(encoded)
    print(f"wrote {OUTPUT}")
    print(f"sha256 {hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
