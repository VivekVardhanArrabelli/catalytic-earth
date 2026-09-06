#!/usr/bin/env python3
"""Reproduce the retained M0173 Step 2 -> Step 3 partial-panel audit.

The audit imports the separately pinned M0173 XML extractor, derives the
complete source graphs and every unique position-and-identity locator pair,
then checks six reviewed Step 2 arrow edits and the three-edit retained-core
replay.  A node absent from the next panel is reported as missing evidence and
is never interpreted as physical atom deletion.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = REPO / "data/atlas/atlas10/sources/mcsa/M0173.json"
EXTRACTOR = REPO / "data/atlas/transformations/m0173/audit_m0173.py"
OUTPUT = HERE / "retained_graph_audit.json"

EXPECTED_SOURCE_SHA256 = "d3db64e9a1db6e22e8baae48a738bff261a2296f375a884c19f2f4abc7d8f22e"
EXPECTED_EXTRACTOR_SHA256 = "1683827222e2bf8ea03b236d494493612c0ebc5cfc69dcbfe3eb0a9b5fe3114f"
EXPECTED_SCHEME_SHA256 = {
    2: "7cc3b37af574d0bb078bd46059d6559729ee4bb633ec7190b273182af0497f88",
    3: "69c950d577fe89bebaac371b18c8ef9be8690d0573e982d7ed599e38bdf474e2",
}
EXPECTED_FLOWS = {
    "o24": [
        {"kind": "MAtomSetPoint", "atom_refs": ["a3", "a4"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a4", "a50"]},
    ],
    "o25": [
        {"kind": "MAtomSetPoint", "atom_refs": ["a21", "a50"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a21"]},
    ],
    "o26": [
        {"kind": "MEFlowBasePoint", "atom_refs": ["a10"]},
        {"kind": "MAtomSetPoint", "atom_refs": ["a3", "a10"]},
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load_extractor():
    if _sha256(EXTRACTOR) != EXPECTED_EXTRACTOR_SHA256:
        raise ValueError("Pinned M0173 XML extractor hash differs")
    spec = importlib.util.spec_from_file_location("m0173_source_panel_extractor", EXTRACTOR)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load the pinned M0173 XML extractor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _source_nodes(parsed: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for atom_id in parsed["atom_order"]:
        atom = parsed["atom_attributes"][atom_id]
        rows.append(
            {
                "atom_id": atom_id,
                "x2": atom["x2"],
                "y2": atom["y2"],
                "isotope": atom.get("isotope"),
                "mrv_extra_label": atom.get("mrvExtraLabel"),
                "mrv_alias": atom.get("mrvAlias"),
                "rgroup_ref": atom.get("rgroupRef"),
            }
        )
    return rows


def _match_key(
    graph_atom: dict[str, object], source_node: dict[str, object]
) -> tuple[object, ...]:
    return (
        graph_atom["element"],
        source_node["x2"],
        source_node["y2"],
        source_node["isotope"],
        source_node["mrv_extra_label"],
        source_node["mrv_alias"],
        source_node["rgroup_ref"],
    )


def _graph_rows(graph: dict[str, object]):
    atoms = {row["atom_id"]: dict(row) for row in graph["atoms"]}
    bonds = {tuple(sorted(row["atom_ids"])): row["order"] for row in graph["bonds"]}
    return atoms, bonds


def _apply_projected_edits(
    before_graph: dict[str, object], edits: list[dict[str, object]]
):
    atoms, bonds = _graph_rows(before_graph)
    for edit in edits:
        refs = edit["atom_ids"]
        if edit["operation"] == "set_bond_order":
            edge = tuple(sorted(refs))
            if bonds.get(edge) != edit["before"]:
                raise ValueError(f"{edit['edit_id']} projected bond precondition differs")
            bonds[edge] = edit["after"]
        elif edit["operation"] == "set_formal_charge":
            atom = atoms[refs[0]]
            if atom["formal_charge"] != edit["before"]:
                raise ValueError(f"{edit['edit_id']} projected charge precondition differs")
            atom["formal_charge"] = edit["after"]
        else:
            raise ValueError(f"{edit['edit_id']} is not retained-core replayable")
    return atoms, bonds


def _build() -> dict[str, object]:
    if _sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise ValueError("M0173 source snapshot hash differs")
    extractor = _load_extractor()
    wrapped = json.loads(SOURCE.read_text(encoding="utf-8"))
    raw_steps = {
        int(row["step_id"]): row
        for row in wrapped.get("step_schemes", [])
        if row.get("mechanism_id") == 1 and row.get("step_id") in {2, 3}
    }
    if set(raw_steps) != {2, 3}:
        raise ValueError("M0173 partial state-pair coverage differs")
    for step_id, expected in EXPECTED_SCHEME_SHA256.items():
        if raw_steps[step_id].get("content_sha256") != expected:
            raise ValueError(f"M0173 Step {step_id} scheme hash differs")
    before = extractor._parse_step(raw_steps[2])
    after = extractor._parse_step(raw_steps[3])
    before_graph = before["graph"]
    after_graph = after["graph"]
    before_nodes = _source_nodes(before)
    after_nodes = _source_nodes(after)
    before_graph_atoms = {row["atom_id"]: row for row in before_graph["atoms"]}
    after_graph_atoms = {row["atom_id"]: row for row in after_graph["atoms"]}

    after_index: dict[tuple[object, ...], list[str]] = {}
    for node in after_nodes:
        key = _match_key(after_graph_atoms[node["atom_id"]], node)
        after_index.setdefault(key, []).append(node["atom_id"])
    before_index: dict[tuple[object, ...], list[str]] = {}
    for node in before_nodes:
        key = _match_key(before_graph_atoms[node["atom_id"]], node)
        before_index.setdefault(key, []).append(node["atom_id"])

    atom_map = []
    for node in before_nodes:
        key = _match_key(before_graph_atoms[node["atom_id"]], node)
        before_hits = before_index[key]
        after_hits = after_index.get(key, [])
        if len(before_hits) == len(after_hits) == 1:
            atom_map.append(
                {"before_atom_id": node["atom_id"], "after_atom_id": after_hits[0]}
            )
    if len(atom_map) != 40:
        raise ValueError("M0173 unique locator correspondence count differs")
    mapped_before = {row["before_atom_id"] for row in atom_map}
    mapped_after = {row["after_atom_id"] for row in atom_map}
    unmatched_before = [row["atom_id"] for row in before_nodes if row["atom_id"] not in mapped_before]
    unmatched_after = [row["atom_id"] for row in after_nodes if row["atom_id"] not in mapped_after]
    if unmatched_before != ["a4", "a5", "a6", "a7", "a8", "a9", "a12", "a13", "a14", "a50"]:
        raise ValueError("M0173 unmatched Step 2 nodes differ")
    if unmatched_after != ["a6", "a7"]:
        raise ValueError("M0173 unmatched Step 3 nodes differ")

    expected_flow_rows = {row["flow_id"]: row["points"] for row in before["flows"]}
    if expected_flow_rows != EXPECTED_FLOWS:
        raise ValueError("M0173 Step 2 source-flow endpoints differ")
    edits = [
        {"edit_id": "e1", "operation": "remove_bond", "atom_ids": ["a3", "a4"], "before": 1, "after": 0, "source_flow_id": "o24"},
        {"edit_id": "e2", "operation": "add_bond", "atom_ids": ["a4", "a50"], "before": 0, "after": 1, "source_flow_id": "o24"},
        {"edit_id": "e3", "operation": "remove_bond", "atom_ids": ["a21", "a50"], "before": 1, "after": 0, "source_flow_id": "o25"},
        {"edit_id": "e4", "operation": "set_formal_charge", "atom_ids": ["a21"], "before": 1, "after": 0, "source_flow_id": "o25"},
        {"edit_id": "e5", "operation": "set_bond_order", "atom_ids": ["a3", "a10"], "before": 1, "after": 2, "source_flow_id": "o26"},
        {"edit_id": "e6", "operation": "set_formal_charge", "atom_ids": ["a10"], "before": -1, "after": 0, "source_flow_id": "o26"},
    ]
    before_atoms, before_bonds = _graph_rows(before_graph)
    for edit in edits:
        refs = edit["atom_ids"]
        if edit["operation"] in {"remove_bond", "add_bond", "set_bond_order"}:
            actual = before_bonds.get(tuple(sorted(refs)), 0)
        else:
            actual = before_atoms[refs[0]]["formal_charge"]
        if actual != edit["before"]:
            raise ValueError(f"{edit['edit_id']} full-before precondition differs")

    projected_before = {
        "atoms": [row for row in before_graph["atoms"] if row["atom_id"] in mapped_before],
        "bonds": [row for row in before_graph["bonds"] if set(row["atom_ids"]) <= mapped_before],
    }
    projected_after = {
        "atoms": [row for row in after_graph["atoms"] if row["atom_id"] in mapped_after],
        "bonds": [row for row in after_graph["bonds"] if set(row["atom_ids"]) <= mapped_after],
    }
    replayed_edits = [row for row in edits if set(row["atom_ids"]) <= mapped_before]
    if [row["edit_id"] for row in replayed_edits] != ["e4", "e5", "e6"]:
        raise ValueError("M0173 retained-core edit classification differs")
    predicted_atoms, predicted_bonds = _apply_projected_edits(projected_before, replayed_edits)
    after_atoms, after_bonds = _graph_rows(projected_after)
    locator_map = {row["before_atom_id"]: row["after_atom_id"] for row in atom_map}
    for before_id, after_id in locator_map.items():
        predicted = predicted_atoms[before_id]
        observed = after_atoms[after_id]
        if (
            predicted["element"],
            predicted["formal_charge"],
            predicted["stereochemistry"],
        ) != (
            observed["element"],
            observed["formal_charge"],
            observed["stereochemistry"],
        ):
            raise ValueError("M0173 retained-core atom replay differs")
    mapped_predicted_bonds = {
        tuple(sorted((locator_map[left], locator_map[right]))): order
        for (left, right), order in predicted_bonds.items()
    }
    if mapped_predicted_bonds != after_bonds:
        raise ValueError("M0173 retained-core bond replay differs")

    before_boundary_bonds = [
        row
        for row in before_graph["bonds"]
        if len(set(row["atom_ids"]) & mapped_before) == 1
    ]
    after_boundary_bonds = [
        row
        for row in after_graph["bonds"]
        if len(set(row["atom_ids"]) & mapped_after) == 1
    ]
    if before_boundary_bonds != [
        {"atom_ids": ["a3", "a4"], "order": 1},
        {"atom_ids": ["a21", "a50"], "order": 1},
    ] or after_boundary_bonds:
        raise ValueError("M0173 mapped/unmatched boundary edges differ")

    stereo_or_convention = [
        {"source_step_id": parsed["step_id"], **row}
        for parsed in (before, after)
        for row in parsed["bond_rows"]
        if row["bond_stereo"] is not None or row["convention"] is not None
    ]
    if stereo_or_convention:
        raise ValueError("M0173 partial state pair unexpectedly contains bond stereo or conventions")
    full_before_charge = sum(row["formal_charge"] for row in before_graph["atoms"])
    full_after_charge = sum(row["formal_charge"] for row in after_graph["atoms"])
    projected_before_charge = sum(row["formal_charge"] for row in projected_before["atoms"])
    projected_after_charge = sum(row["formal_charge"] for row in projected_after["atoms"])
    if (full_before_charge, full_after_charge, projected_before_charge, projected_after_charge) != (-1, 0, 0, 0):
        raise ValueError("M0173 full/projected charge accounting differs")

    flow_coverage = [
        {"flow_id": "o24", "replayed_edit_ids": [], "after_graph_unverified_edit_ids": ["e1", "e2"], "status": "after_graph_unverified"},
        {"flow_id": "o25", "replayed_edit_ids": ["e4"], "after_graph_unverified_edit_ids": ["e3"], "status": "partially_replayed"},
        {"flow_id": "o26", "replayed_edit_ids": ["e5", "e6"], "after_graph_unverified_edit_ids": [], "status": "fully_replayed"},
    ]
    coverage = {
        "before_node_count": len(before_graph["atoms"]),
        "after_node_count": len(after_graph["atoms"]),
        "mapped_node_count": len(atom_map),
        "unmatched_before_atom_ids": unmatched_before,
        "unmatched_after_atom_ids": unmatched_after,
        "before_boundary_bonds": before_boundary_bonds,
        "after_boundary_bonds": after_boundary_bonds,
        "replayed_edit_ids": ["e4", "e5", "e6"],
        "after_graph_unverified_edit_ids": ["e1", "e2", "e3"],
        "source_flow_ids": ["o24", "o25", "o26"],
        "source_flow_covered_edit_ids": ["e1", "e2", "e3", "e4", "e5", "e6"],
        "flow_coverage": flow_coverage,
        "full_before_formal_charge": full_before_charge,
        "full_after_formal_charge": full_after_charge,
        "projected_before_formal_charge": projected_before_charge,
        "projected_after_formal_charge": projected_after_charge,
        "projection_replays_exactly": True,
        "full_panel_replay_asserted": False,
    }
    source_annotation_differences = []
    after_nodes_by_id = {row["atom_id"]: row for row in after_nodes}
    for pair in atom_map:
        left = next(row for row in before_nodes if row["atom_id"] == pair["before_atom_id"])
        right = after_nodes_by_id[pair["after_atom_id"]]
        for key in ("x2", "y2", "isotope", "mrv_extra_label", "mrv_alias", "rgroup_ref"):
            if left[key] != right[key]:
                source_annotation_differences.append(
                    {"before_atom_id": pair["before_atom_id"], "after_atom_id": pair["after_atom_id"], "field": key, "before": left[key], "after": right[key]}
                )
    if source_annotation_differences:
        raise ValueError("M0173 mapped source annotations differ")

    return {
        "audit_schema_version": "catalytic-earth.m0173-partial-panel-audit.v1",
        "audit_method": {
            "implementation": "python_stdlib_importlib_and_exact_source_projection",
            "script_path": "data/atlas/panel_comparisons/m0173/audit_m0173_partial.py",
            "script_sha256": _sha256(Path(__file__)),
            "extractor_path": "data/atlas/transformations/m0173/audit_m0173.py",
            "extractor_sha256": _sha256(EXTRACTOR),
            "network_requests": 0,
        },
        "source_snapshot": {
            "path": SOURCE.relative_to(REPO).as_posix(),
            "sha256": _sha256(SOURCE),
            "record_id": "M0173",
        },
        "state_pair": {
            "before_source_step_id": 2,
            "before_scheme_sha256": before["scheme_sha256"],
            "after_source_step_id": 3,
            "after_scheme_sha256": after["scheme_sha256"],
        },
        "source_panels": {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_nodes": before_nodes,
            "after_nodes": after_nodes,
        },
        "correspondence": {
            "method": "unique_exact_source_position_and_identity",
            "match_fields": ["element", "x2", "y2", "isotope", "mrv_extra_label", "mrv_alias", "rgroup_ref"],
            "interpretation": "project_reviewed_panel_alignment_not_physical_atom_map",
            "atom_map": atom_map,
            "mapped_source_annotation_differences": source_annotation_differences,
        },
        "proposed_graph_edits": edits,
        "source_flow_bindings": [
            {"source_step_id": 2, "flow_id": "o24", "edit_ids": ["e1", "e2"]},
            {"source_step_id": 2, "flow_id": "o25", "edit_ids": ["e3", "e4"]},
            {"source_step_id": 2, "flow_id": "o26", "edit_ids": ["e5", "e6"]},
        ],
        "source_flow_points": before["flows"],
        "coverage": coverage,
        "unmatched_node_classification": {
            "before": [
                {"classification": "released_peptide_fragment_not_drawn_in_next_panel", "atom_ids": ["a4", "a5", "a6", "a7", "a8", "a9"]},
                {"classification": "three_node_water_depiction_not_uniquely_mapped_to_redrawn_water", "atom_ids": ["a12", "a13", "a14"]},
                {"classification": "transferred_proton_not_drawn_in_next_panel", "atom_ids": ["a50"]},
            ],
            "after": [
                {"classification": "redrawn_two_node_water_with_physical_identity_unresolved", "atom_ids": ["a6", "a7"]}
            ],
            "interpretation": "unmatched_source_nodes_are_missing_evidence_not_physical_creation_or_deletion",
        },
        "raw_representation_checks": {
            "bond_stereo_or_convention_rows": stereo_or_convention,
            "step_2_explicit_h_atom_ids": ["a12", "a14", "a50"],
            "step_3_explicit_h_atom_ids": ["a6"],
            "water_identity_asserted": False,
            "complete_panel_replay_asserted": False,
        },
        "limits": [
            "The 40 exact pairs are project-selected source locators, not a source-supplied or physical atom map.",
            "The ten unmatched Step 2 nodes and two unmatched Step 3 nodes are missing or redrawn evidence, not asserted atom deletion or creation.",
            "The Step 2 H-O-H and Step 3 H-O water depictions do not establish a unique physical water or hydrogen correspondence.",
            "Three of six Step 2 arrow edits cross into nodes absent from Step 3 and therefore lack after-graph verification.",
            "The generic CHEBI:90799 labels and R tokens do not establish an exact peptide or canonical participant correspondence.",
            "No bondStereo token occurs in either panel, so no stereochemical assignment or preservation is asserted.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify committed audit bytes")
    args = parser.parse_args()
    result = _build()
    encoded = _json_bytes(result)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != encoded:
            print(f"{OUTPUT}: generated bytes differ", file=sys.stderr)
            return 1
        print(f"M0173 partial-panel audit is reproducible: {hashlib.sha256(encoded).hexdigest()}")
        return 0
    OUTPUT.write_bytes(encoded)
    print(f"wrote {OUTPUT}")
    print(f"sha256 {hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
