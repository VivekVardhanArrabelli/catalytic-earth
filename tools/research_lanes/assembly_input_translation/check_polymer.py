#!/usr/bin/env python3
"""Narrow RFdiffusion2 input-consumer checks; no model import or execution.

The polymer checks execute the exact pinned parse_pdb_lines_target function and
ContigMap class bodies with explicitly supplied dependencies.  This is not a full native RFdiffusion2 environment check.
"""

from __future__ import annotations

import argparse
import ast
import collections
import contextlib
import hashlib
import json
import random
import sys
import types
from pathlib import Path

import numpy as np


PIN = "d365cbf4db3958814a9f8e4f6f94fa309dfebc2b"
SOURCE = None
RESULT = None
SOURCE_SHA256 = {
    "parsers.py": "8602cba9671b2c7a8abf0f5064ab56a037d1fcb19f14eb35cc602d393d253b34",
    "contigs.py": "68989d8b0fd5c67ab6dde91179080767ac42d451eb2e787f54fdab913902a36f",
    "rf2aa-chemical.py": "8eee997451e5a50a35841c02f49777f5d2fd0f024943c084b368e5d53364d2f8",
}


def source_path(name):
    return SOURCE / name


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_ast_node(path: Path, kind: type[ast.AST], name: str) -> ast.AST:
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, kind) and getattr(node, "name", None) == name:
            return node
    raise RuntimeError(f"{name} not found in {path}")


def pinned_chemical_constants(path: Path) -> tuple[int, list[str], list[tuple]]:
    """Literal-extract default num2aa/aa2long tables from pinned rf2aa source."""
    tree = ast.parse(path.read_text(), filename=str(path))
    load_base = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "load_base_data":
            load_base = node
            break
    if load_base is None:
        raise RuntimeError("load_base_data not found")

    num2aa = None
    nheavy = None
    aa2long_candidates = []
    for node in ast.walk(load_base):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value = node.value
        for target in targets:
            if not isinstance(target, ast.Attribute) or not isinstance(target.value, ast.Name):
                continue
            if target.value.id != "self":
                continue
            if target.attr == "num2aa":
                num2aa = ast.literal_eval(value)
            elif target.attr == "NHEAVY":
                nheavy = ast.literal_eval(value)
            elif target.attr == "aa2long":
                aa2long_candidates.append(ast.literal_eval(value))
    if nheavy is None or num2aa is None or len(aa2long_candidates) != 2:
        raise RuntimeError("unexpected pinned chemical table layout")
    # Default RFdiffusion2 initialization uses phosphate frames: the second table.
    return nheavy, num2aa, aa2long_candidates[1]


def exact_polymer_and_contig_checks(lines: list[str]) -> dict:
    nheavy, num2aa, aa2long = pinned_chemical_constants(SOURCE / "rf2aa-chemical.py")

    class SuppliedChemData:
        NHEAVY = nheavy

    SuppliedChemData.aa2num = {name: i for i, name in enumerate(num2aa)}
    SuppliedChemData.aa2num["MEN"] = 20
    SuppliedChemData.aa2long = aa2long

    # parse_pdb_lines_target only uses this context manager on successful rows.
    supplied_rf_diffusion = types.SimpleNamespace(
        error=types.SimpleNamespace(context=lambda _line: contextlib.nullcontext())
    )
    parser_node = find_ast_node(
        source_path("parsers.py"), ast.FunctionDef, "parse_pdb_lines_target"
    )
    parser_ns = {
        "np": np,
        "ChemData": SuppliedChemData,
        "rf_diffusion": supplied_rf_diffusion,
    }
    exec(compile(ast.Module(body=[parser_node], type_ignores=[]), str(source_path("parsers.py")), "exec"), parser_ns)
    parsed = parser_ns["parse_pdb_lines_target"](lines, parse_hetatom=True)

    contig_node = find_ast_node(SOURCE / "contigs.py", ast.ClassDef, "ContigMap")
    contig_ns = {
        "np": np,
        "random": random,
        "sys": sys,
        "defaultdict": collections.defaultdict,
        "ChemData": SuppliedChemData,
        # Unused for this deterministic, unshuffled test fixture.
        "shuffle_contig_string": lambda *_a, **_k: (_ for _ in ()).throw(
            RuntimeError("shuffle_contig_string unexpectedly called")
        ),
        # Exact pinned mapping for the two real protein tokens used here.
        "inds_to_mol_class": {
            SuppliedChemData.aa2num["GLN"]: "protein",
            SuppliedChemData.aa2num["GLU"]: "protein",
        },
    }
    exec(compile(ast.Module(body=[contig_node], type_ignores=[]), str(SOURCE / "contigs.py"), "exec"), contig_ns)
    ContigMap = contig_ns["ContigMap"]

    # The string literal in interface.json is parsed separately with literal_eval;
    # ipd.dev.safe_eval is intentionally not substituted or claimed as executed.
    interface = json.loads((RESULT / "interface.json").read_text())
    contig_atoms = ast.literal_eval(interface["contigmap"]["contig_atoms"])
    cm = ContigMap(
        parsed,
        contigs=["A160-160_B366-366"],
        contig_atoms=contig_atoms,
        has_termini=[True, True],
    )

    pdb_idx = [[str(ch), int(i)] for ch, i in parsed["pdb_idx"]]
    expected_pdb_idx = [["A", 160], ["A", 366], ["B", 366]]
    expected_ref = [["A", 160], ["B", 366]]
    expected_atoms = {"A160": ["NE2"], "B366": ["OE1", "OE2"]}
    actual_atoms = {f"{ch}{i}": list(v) for (ch, i), v in cm.atomize_resnum2atomnames.items()}

    receipt = json.loads((RESULT / "receipt.json").read_text())
    guide_checks = []
    for atom in receipt["atoms"]:
        if not atom["guidepost"]:
            continue
        residue_i = parsed["pdb_idx"].index((atom["consumer_chain"], atom["consumer_residue"]))
        atom_names = [n.strip() if n is not None else None for n in aa2long[parsed["seq"][residue_i]][:23]]
        atom_i = atom_names.index(atom["author_atom_id"])
        xyz = parsed["xyz"][residue_i, atom_i]
        guide_checks.append(bool(parsed["mask"][residue_i, atom_i]) and
                            bool(np.allclose(xyz, atom["transformed_xyz"], rtol=0, atol=0.000002)))

    assertions = {
        "pdb_idx_preserves_operator_chains": pdb_idx == expected_pdb_idx,
        "identity_control_A366_parsed": ["A", 366] in pdb_idx,
        "identity_control_A366_not_selected": ("A", 366) not in cm.ref,
        "selected_ref_is_A160_B366": [[str(ch), int(i)] for ch, i in cm.ref] == expected_ref,
        "selected_ref_indices_are_0_2": list(cm.ref_idx0) == [0, 2],
        "contig_atoms_exact": actual_atoms == expected_atoms,
        "selected_atom_masks_and_coordinates_match": len(guide_checks) == 3 and all(guide_checks),
        "atomized_indices_are_distinct": cm.atomize_indices2atomname == {0: ["NE2"], 1: ["OE1", "OE2"]},
        "two_output_chains": list(cm.hal) == [("A", 1), ("B", 34)],
        "protein_mol_classes": cm.mol_classes == ["protein", "protein"],
        "hetero_count": len(parsed["info_het"]) == 42,
        "hetero_parser_drops_chain_identity": all("chain" not in row for row in parsed["info_het"]),
    }
    return {
        "scope": "exact pinned function/class bodies with supplied successful-row context, literal chemical tables, NumPy, and explicit protein token class map; not native module imports",
        "test_contigs": ["A160-160_B366-366"],
        "test_contigs_are_design_recipe": False,
        "pdb_idx": pdb_idx,
        "ref": [[str(ch), int(i)] for ch, i in cm.ref],
        "hal": [[str(ch), int(i)] for ch, i in cm.hal],
        "ref_idx0": [int(i) for i in cm.ref_idx0],
        "atomize_resnum2atomnames": actual_atoms,
        "atomize_indices2atomname": {str(k): list(v) for k, v in cm.atomize_indices2atomname.items()},
        "assertions": assertions,
        "passed": all(assertions.values()),
    }



def main():
    global SOURCE, RESULT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True,
                        help="Three pinned source files named in SOURCE_SHA256; see consumer-execution.json URLs")
    parser.add_argument("--result-dir", type=Path, default=Path(__file__).with_name("6ha3"))
    args = parser.parse_args()
    SOURCE, RESULT = args.source_dir, args.result_dir
    for name, expected in SOURCE_SHA256.items():
        if sha256(SOURCE / name) != expected:
            raise ValueError(f"source pin differs: {name}")
    result = exact_polymer_and_contig_checks((RESULT / "assembly.pdb").read_text().splitlines(True))
    if not result["passed"]:
        raise ValueError(json.dumps(result))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
