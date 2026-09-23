#!/usr/bin/env python3
"""Verify source-to-serialization identity; this is not a native consumer test."""
import argparse
import ast
from collections import Counter
import copy
import json
import math
from pathlib import Path

import build_input


def verify(pdb, interface, receipt):
    require = build_input.require
    rows = [l for l in pdb.decode("ascii").splitlines() if l.startswith(("ATOM  ", "HETATM"))]
    keys = [(l[21], int(l[22:26]), l[12:16].strip()) for l in rows]
    require(len(keys) == len(set(keys)), "consumer identity collision")
    require(len(rows) == len(receipt["atoms"]), "emitted atom count differs")
    by_key = dict(zip(keys, rows))
    expected_guide = {}
    inverse = {}
    for atom in receipt["atoms"]:
        key = (atom["consumer_chain"], atom["consumer_residue"], atom["author_atom_id"])
        require(key in by_key, "source atom absent from consumer namespace")
        line = by_key[key]
        require(int(line[6:11]) == atom["consumer_serial"], "atom serial differs")
        require(line[:6].strip() == atom["record_type"] and line[17:20] == atom["author_component_id"], "atom component differs")
        require(line[16] == " " and line[26] == " " and line[78:80] == "  ", "unbound alternate/insertion/charge")
        require(line[76:78].strip() == atom["element"], "element differs")
        xyz = [float(line[i:i + 8]) for i in (30, 38, 46)]
        require(all(abs(a - b) <= 0.0005001 for a, b in zip(xyz, atom["transformed_xyz"])), "coordinate differs")
        require(abs(float(line[54:60]) - atom["occupancy"]) <= 0.005001, "occupancy differs")
        require(abs(float(line[60:66]) - atom["b_iso_or_equiv"]) <= 0.005001, "B factor differs")
        require(atom["atom_instance_id"] not in inverse, "inverse source identity repeats")
        inverse[atom["atom_instance_id"]] = key
        if atom["guidepost"]:
            expected_guide.setdefault(atom["consumer_selector"], []).append(atom["author_atom_id"])
    actual = ast.literal_eval(interface["contigmap"]["contig_atoms"])
    require({k: v.split(",") for k, v in actual.items()} == expected_guide, "guidepost/source selection differs")
    ligand_atoms = [a for a in receipt["atoms"] if a["selection_role"] == "ligand"]
    require({a["author_component_id"] for a in ligand_atoms} == {interface["inference"]["ligand"]}, "ligand name differs")
    serials = {a["label_atom_id"]: a["consumer_serial"] for a in ligand_atoms}
    expected_edges = Counter()
    orders = {"sing": 1, "doub": 2, "trip": 3}
    for b in receipt["ligand_dictionary_heavy_bonds"]:
        i, j = (serials[b[f"atom_id_{k}"]] for k in (1, 2))
        expected_edges[(i, j)] = expected_edges[(j, i)] = orders[b["value_order"]]
    actual_edges = Counter()
    for line in pdb.decode().splitlines():
        if line.startswith("CONECT"):
            values = [int(line[i:i + 5]) for i in range(6, len(line), 5)]
            actual_edges.update((values[0], j) for j in values[1:])
    require(actual_edges == expected_edges, "dictionary connectivity serialization differs")
    return {"atom_inverse_map_count": len(inverse), "guideposts": expected_guide,
            "ligand_heavy_atoms": len(ligand_atoms), "ligand_heavy_bonds": len(expected_edges) // 2,
            "source_to_pdb_verified": True, "native_parser_executed_by_this_check": False}


def must_reject(label, pdb, interface, receipt):
    try:
        verify(pdb, interface, receipt)
    except ValueError as exc:
        return {"case": label, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"failed to reject {label}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-dir", type=Path, required=True)
    args = parser.parse_args()
    case = json.loads(Path(__file__).with_name("6ha3.json").read_text())
    pdb, interface, receipt = build_input.build(case)
    require = build_input.require
    require(pdb == (args.result_dir / "assembly.pdb").read_bytes(), "PDB does not reproduce")
    for name, value in (("interface.json", interface), ("receipt.json", receipt)):
        require(value == json.loads((args.result_dir / name).read_text()), f"{name} does not reproduce")
    result = verify(pdb, interface, receipt)
    lines = pdb.decode().splitlines()
    collapsed = "\n".join(l[:21] + "A" + l[22:] if l.startswith("ATOM  ") and l[21] == "B" else l for l in lines) + "\n"
    missing = "\n".join(l for l in lines if not (l.startswith("ATOM  ") and l[21] == "B")) + "\n"
    wrong_interface = copy.deepcopy(interface)
    wrong_interface["contigmap"]["contig_atoms"] = "{'A160': 'NE2', 'A366': 'OE1,OE2'}"
    changed_name = pdb.replace(b" N1, T6F", b" N1  T6F")
    require(changed_name != pdb, "punctuation control did not mutate the atom")
    result["negative_controls"] = [
        must_reject("collapsed operator-qualified consumer chain", collapsed.encode(), interface, receipt),
        must_reject("partner copy omitted", missing.encode(), interface, receipt),
        must_reject("guidepost redirected to unexpanded copy", pdb, wrong_interface, receipt),
        must_reject("ligand atom comma removed", changed_name, interface, receipt),
        must_reject("ligand bonds omitted", ("\n".join(l for l in lines if not l.startswith("CONECT")) + "\n").encode(), interface, receipt),
    ]
    atoms = {(a["selection_id"], a["author_atom_id"]): a for a in receipt["atoms"]}
    result["partner_to_q160_angstrom"] = math.dist(atoms[("partner-e366", "OE1")]["transformed_xyz"], atoms[("q160", "NE2")]["transformed_xyz"])
    result["control_to_q160_angstrom"] = math.dist(atoms[("unexpanded-e366", "OE1")]["transformed_xyz"], atoms[("q160", "NE2")]["transformed_xyz"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
