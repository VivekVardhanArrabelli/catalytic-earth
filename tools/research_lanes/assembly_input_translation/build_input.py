#!/usr/bin/env python3
"""Translate reviewed assembly selections to PDB identities and RFdiffusion2 keys.

This research adapter preserves a reversible atom map. It does not select a
productive motif, invent atoms, assign protonation, or construct a design recipe.
"""
import argparse
from collections import defaultdict
import copy
import hashlib
import json
from pathlib import Path
import string
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from build_atlas_assembly_context import check as check_assembly
from catalytic_earth.atlas_assembly_context import project_assembly
from catalytic_earth.atlas_primary_source_check import parse_mmcif_categories


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def chain_key(atom):
    return (atom["record_type"] != "ATOM", atom["model_id"],
            tuple(atom["operator_ids"]), atom["label_asym_id"])


def pdb_line(atom, serial, chain):
    name = atom["author_atom_id"]
    number = int(atom["author_residue_number"])
    comp = atom["author_component_id"]
    require(0 < serial <= 99999 and -999 <= number <= 9999, "PDB numeric field overflow")
    require(0 < len(name) <= 4 and len(comp) == 3, "PDB name field overflow")
    require(atom["label_alt_id"] is None and atom["insertion_code"] is None,
            "alternate/insertion choice is unsupported; do not silently collapse it")
    require(atom["formal_charge"] is None, "explicit charge needs a reviewed serializer")
    xyz = "".join(f"{x:8.3f}" for x in atom["transformed_xyz"])
    require(len(xyz) == 24, "PDB coordinate field overflow")
    name_field = f" {name:<3}" if len(atom["element"]) == 1 and len(name) < 4 and not name[0].isdigit() else f"{name:<4}"
    line = (f"{atom['record_type']:<6}{serial:5d} {name_field} {comp:3} {chain}{number:4d}    "
            f"{xyz}{atom['occupancy']:6.2f}{atom['b_iso_or_equiv']:6.2f}          "
            f"{atom['element']:>2}  ")
    require(len(line) == 80, "PDB record field overflow")
    return line


def build(case, root=ROOT):
    packet = root / case["assembly_packet"]
    reviewed = check_assembly(packet, root)
    spec = json.loads((packet / "spec.json").read_text())
    source = root / reviewed["coordinate_source"]["path"]
    cif = source.read_text()
    tables = parse_mmcif_categories(cif, categories={"_atom_site", "_chem_comp", "_chem_comp_atom", "_chem_comp_bond"})
    roles = case["selection_roles"]
    original = {s["selection_id"]: s for s in reviewed["geometry"]["selections"]}
    require(set(roles) == set(original), "all reviewed selections need an explicit role")
    require(set(roles.values()) <= {"guidepost", "ligand", "identity_control"}, "unknown selection role")
    require(list(roles.values()).count("ligand") == 1, "consumer ligand-name filter requires one ligand instance")

    # Extra atoms are deposited residue context, never additional guideposts.
    expanded_spec = copy.deepcopy(spec["assembly_spec"])
    expanded_spec["distance_pairs"] = []
    for selection in expanded_spec["selections"]:
        rows = [a for a in tables["_atom_site"] if
                a["label_asym_id"] == selection["label_asym_id"] and
                a["label_comp_id"] == selection["label_comp_id"] and
                a["auth_seq_id"] == selection["auth_seq_id"] and
                a["pdbx_pdb_model_num"] == selection["model_id"] and
                a["type_symbol"] not in {"H", "D"}]
        selection["atom_names"] = list(dict.fromkeys(a["label_atom_id"] for a in rows))
    expanded = project_assembly(cif, expanded_spec)
    atoms = [a for s in expanded["selections"] for a in s["atoms"]]
    require(len({a["model_id"] for a in atoms}) == 1, "consumer cannot preserve multiple models")
    require(len({a["atom_instance_id"] for a in atoms}) == len(atoms), "overlapping residue selections")
    keys = sorted({chain_key(a) for a in atoms})
    require(len(keys) <= 26, "consumer chain namespace exhausted")
    chains = dict(zip(keys, string.ascii_uppercase))
    atoms.sort(key=lambda a: (chains[chain_key(a)], int(a["author_residue_number"]), int(a["atom_site_id"])))
    selected = {a["atom_instance_id"] for s in original.values() for a in s["atoms"]}
    guide_ids = {a["atom_instance_id"] for sid, s in original.items() if roles[sid] == "guidepost" for a in s["atoms"]}
    require(selected <= {a["atom_instance_id"] for a in atoms}, "reviewed atom lost during heavy-atom expansion")
    lines, mapping, selectors = [], [], defaultdict(list)
    consumer_keys = set()
    for serial, atom in enumerate(atoms, 1):
        chain = chains[chain_key(atom)]
        selector = chain + str(int(atom["author_residue_number"]))
        key = (chain, int(atom["author_residue_number"]), atom["author_atom_id"])
        require(key not in consumer_keys, "consumer atom identity collision")
        consumer_keys.add(key)
        role = roles[atom["selection_id"]]
        require((role == "ligand") == (atom["record_type"] == "HETATM"), "role/record type mismatch")
        guide = atom["atom_instance_id"] in guide_ids
        if guide:
            require(int(atom["author_residue_number"]) > 0, "consumer guidepost numbering must be positive")
            require("," not in atom["author_atom_id"], "contig_atoms cannot delimit an atom name containing a comma")
            selectors[selector].append(atom["author_atom_id"])
        lines.append(pdb_line(atom, serial, chain))
        mapping.append({**atom, "consumer_serial": serial, "consumer_chain": chain,
                        "consumer_residue": int(atom["author_residue_number"]),
                        "consumer_selector": selector, "selection_role": role,
                        "reviewed_selected_atom": atom["atom_instance_id"] in selected,
                        "guidepost": guide})

    ligand_atoms = [a for a in mapping if a["selection_role"] == "ligand"]
    ligand = {a["label_component_id"] for a in ligand_atoms}
    require(len(ligand) == 1, "ligand component is ambiguous")
    ligand = next(iter(ligand))
    components = [c for c in tables["_chem_comp"] if c["id"] == ligand]
    require(len(components) == 1, "ligand component metadata is absent or ambiguous")
    require(all(a["author_component_id"] == ligand for a in ligand_atoms), "ligand name namespace differs")
    dictionary_atoms = [a for a in tables["_chem_comp_atom"] if a["comp_id"] == ligand]
    heavy_dictionary = {a["atom_id"]: a["type_symbol"] for a in dictionary_atoms if a["type_symbol"] not in {"H", "D"}}
    by_name = {a["label_atom_id"]: a for a in ligand_atoms}
    require(len(by_name) == len(ligand_atoms), "ligand atom names repeat")
    require({n: a["element"] for n, a in by_name.items()} == heavy_dictionary,
            "observed ligand does not contain exactly the dictionary heavy atoms")
    require(all(a["label_atom_id"] == a["author_atom_id"] for a in ligand_atoms), "ligand atom namespace differs")
    bonds = [b for b in tables["_chem_comp_bond"] if b["comp_id"] == ligand and
             b["atom_id_1"] in by_name and b["atom_id_2"] in by_name]
    adjacency = defaultdict(list)
    orders = {"sing": 1, "doub": 2, "trip": 3}
    edges = set()
    for bond in bonds:
        edge = tuple(sorted((bond["atom_id_1"], bond["atom_id_2"])))
        require(edge not in edges and edge[0] != edge[1], "ligand dictionary bond repeats")
        edges.add(edge)
        require(bond["value_order"] in orders, "unsupported dictionary bond order")
        i, j = (by_name[bond[f"atom_id_{k}"]]["consumer_serial"] for k in (1, 2))
        adjacency[i].extend([j] * orders[bond["value_order"]])
        adjacency[j].extend([i] * orders[bond["value_order"]])
    for i, neighbors in sorted(adjacency.items()):
        neighbors.sort()
        for start in range(0, len(neighbors), 4):
            lines.append(f"CONECT{i:5d}" + "".join(f"{j:5d}" for j in neighbors[start:start + 4]))
    output = ("\n".join(lines + ["END"]) + "\n").encode("ascii")
    interface = {"scope": "Partial consumer interface; no design contigs, gaps, length or model run specified",
                 "inference": {"ligand": ligand},
                 "contigmap": {"contig_atoms": repr({k: ",".join(v) for k, v in selectors.items()})}}
    receipt = {
        "scope": case["scope"], "source_binding": reviewed["coordinate_source"],
        "assembly_packet": case["assembly_packet"], "packet_id": reviewed["packet_id"],
        "output_sha256": sha(output), "atom_count": len(mapping),
        "guidepost_count": len(guide_ids), "ligand_heavy_atom_count": len(ligand_atoms),
        "ligand_heavy_bond_count": len(bonds), "atoms": mapping,
        "ligand_component": components[0],
        "ligand_dictionary_atoms": dictionary_atoms, "ligand_dictionary_heavy_bonds": bonds,
        "serialization_context": "Heavy-atom copies use only deposited atom rows and declared assembly transforms; no invented chemical atoms or hydrogens",
        "unknown_charge_policy": "Missing atom_site formal charge stays blank; no H or charge is assigned by the translation. Consumer residue/ligand template perception is not evidence of the bound microstate",
        "connectivity_scope": "Only retained component heavy bonds; repeated CONECT neighbors encode dictionary integer orders. CIF aromatic and stereo descriptors remain in this receipt, not explicit PDB fields; native perception of order/stereo/charge must be checked separately",
        "omitted_context": case["omitted_context"],
        "occupancy_limit": "Individual deposited occupancies are retained; neither joint occupancy nor a chemical-state population is established",
        "design_recipe": False, "productive_motif": False, "new_model_run": False,
    }
    return output, interface, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=Path(__file__).with_name("6ha3.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output_dir.exists(), "output directory must be fresh")
    output, interface, receipt = build(json.loads(args.case.read_text()))
    args.output_dir.mkdir(parents=True)
    (args.output_dir / "assembly.pdb").write_bytes(output)
    for name, data in (("interface.json", interface), ("receipt.json", receipt)):
        (args.output_dir / name).write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ("output_sha256", "atom_count", "guidepost_count", "ligand_heavy_atom_count", "ligand_heavy_bond_count")}, indent=2))


if __name__ == "__main__":
    main()
