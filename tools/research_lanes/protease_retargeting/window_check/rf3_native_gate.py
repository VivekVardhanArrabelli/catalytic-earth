#!/usr/bin/env python3
"""Remote-only native RF3 chemistry gate; inference requires --infer-seed.

No downloads, installations, substituted parser bodies, or model construction in
the default gate mode. This file has not been executed against RF3 locally.
"""
import argparse
import hashlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import subprocess
import traceback

COMMIT = "0932f1cb165ae7d413c11b1a7acc04ee31758817"
UTILS_SHA = "71f306e5dd7369c7736ffd6a3390791465cb1641e67d0d03c0b4399923d1027b"
ENGINE_SHA = "292bba9feae83d6001dae83190da170c5e1d303adbdb4f1b5257e55f98b0bd55"
ENZYME_SHA = "b5a77431300a76ff417cab0e36e3d1839cb8c191917d81256220b5cca2061165"
CONDITIONS = [
    ("tdpn3_rf3_window_10mer.json", "ALQSSWGMMG", "626d3f2600929c55004260ba235d26f3a94c693a2ef1502f96c2eeddb11e65c7"),
    ("tdpn3_rf3_window_12mer.json", "ALQSSWGMMGML", "5afdbf256678f327b756a51fab8b709c1fa08d2b1b71f7759c5c5d768fe7cdd9"),
]
AA = dict(zip(
    "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
    "ARNDCQEGHILKMFPSTWYV",
))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    with Path(path).open("x") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def check_native_input(spec, expected_a, expected_b, single_bond_type):
    aa = spec.atom_array
    categories = set(aa.get_annotation_categories())
    charge_fields = [name for name in ("charge", "formal_charge") if name in categories]
    require(bool(charge_fields), "Native parser did not retain an inspectable formal-charge annotation")
    charges = [float(x) for x in aa.get_annotation(charge_fields[0])]
    for field in charge_fields[1:]:
        require(charges == [float(x) for x in aa.get_annotation(field)], "Charge annotations disagree")
    require(aa.bonds is not None, "Native parser did not retain bonds")
    bonds = [[int(x) for x in row] for row in aa.bonds.as_array()]
    edges = {}
    for i, j, kind in bonds:
        pair = tuple(sorted((i, j)))
        require(pair not in edges or edges[pair] == kind, "Conflicting bond types")
        edges[pair] = kind
    atoms = []
    keyed = {}
    for i in range(len(aa)):
        key = (str(aa.chain_id[i]), int(aa.res_id[i]), str(aa.atom_name[i]))
        require(key not in keyed, f"Ambiguous native atom identifier: {key}")
        keyed[key] = i
        atoms.append({"index": i, "chain_id": key[0], "res_id": key[1],
                      "res_name": str(aa.res_name[i]), "atom_name": key[2],
                      "element": str(aa.element[i]).upper(), "formal_charge": charges[i]})

    peptide_edges = []
    for chain, expected in (("A", expected_a), ("B", expected_b)):
        residues = {}
        for atom in atoms:
            if atom["chain_id"] == chain:
                rid = atom["res_id"]
                require(rid not in residues or residues[rid] == atom["res_name"], "Mixed residue identity")
                residues[rid] = atom["res_name"]
        require(sorted(residues) == list(range(1, len(expected) + 1)), f"Chain {chain} numbering/length changed")
        sequence = "".join(AA.get(residues[i], "?") for i in sorted(residues))
        require(sequence == expected, f"Chain {chain} sequence changed")
        for rid in range(1, len(expected)):
            carbon = keyed[(chain, rid, "C")]
            nitrogen = keyed[(chain, rid + 1, "N")]
            pair = tuple(sorted((carbon, nitrogen)))
            require(edges.get(pair) == single_bond_type, f"Missing/non-single ordinary peptide edge {chain}{rid}-{rid + 1}")
            peptide_edges.append({"chain_id": chain, "left_res_id": rid,
                                  "C_index": carbon, "next_N_index": nitrogen,
                                  "bond_type": edges[pair]})

    ligand_heavy = [a for a in atoms if a["chain_id"] not in ("A", "B") and a["element"] not in ("H", "D")]
    require(sorted(a["element"] for a in ligand_heavy) == ["O", "ZN"], "Ligand loss, duplication, or extra heavy atoms")
    zinc = next(a for a in ligand_heavy if a["element"] == "ZN")
    water = next(a for a in ligand_heavy if a["element"] == "O")
    require(zinc["formal_charge"] == 2.0 and water["formal_charge"] == 0.0, "Zn/water charge identity changed")
    zn_edges = [b for b in bonds if zinc["index"] in b[:2]]
    require(not zn_edges, "Native parser added a bond to dot-disconnected Zn")
    water_neighbors = [j if i == water["index"] else i for i, j, _ in bonds if water["index"] in (i, j)]
    require(all(atoms[i]["element"] in ("H", "D") for i in water_neighbors), "Water acquired a heavy-atom bond")
    require(len(set(water_neighbors)) in (0, 2), "Neutral-water explicit hydrogen count is neither zero nor two")
    require(spec.template_selection is None and spec.ground_truth_conformer_selection is None, "Unexpected template/conformer conditioning")
    require(not spec.cyclic_chains, "Unexpected cyclic peptide conditioning")
    require(not any(v.get("msa_path") for v in spec.chain_info.values() if isinstance(v, dict)), "Unexpected MSA path")

    evaluation_keys = [("B", 7, "C"), ("B", 7, "O"), ("B", 8, "N"),
                       ("A", 146, "NE2"), ("A", 150, "NE2"),
                       ("A", 45, "OE1"), ("A", 45, "OE2"),
                       ("A", 147, "OE1"), ("A", 147, "OE2"),
                       ("A", 78, "OH"), ("A", 78, "CZ")]
    evaluation_map = {f"{c}:{r}:{n}": atoms[keyed[(c, r, n)]] for c, r, n in evaluation_keys}
    return {"example_id": spec.example_id, "A_length": len(expected_a), "B_sequence": expected_b,
            "atom_count": len(atoms), "charge_annotation": charge_fields,
            "zinc": zinc, "water_oxygen": water, "water_explicit_H_neighbors": water_neighbors,
            "Zn_O_bond_present": False, "ordinary_peptide_edges": peptide_edges,
            "evaluation_atom_map": evaluation_map, "atoms": atoms, "bonds": bonds,
            "map_scope": "Native input parsing only. Reidentify output atoms by sequence/residue/chemistry; do not reuse input array indices blindly."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--foundry-root", type=Path, help="Optional checkout: also verify its exact commit and tracked cleanliness")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--infer-seed", type=int, choices=[0, 1])
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-sha256")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    write_json(args.out_dir / "all_20_prespecified_assignments.json", {
        "assigned_denominator": 20,
        "interpretation": "A failed gate or interrupted seed does not change the denominator and supplies no structural result.",
        "assignments": [{"condition_input": filename, "seed": seed, "sample": sample,
                         "status": "assigned_not_yet_observed"}
                        for filename, _, _ in CONDITIONS for seed in (0, 1) for sample in range(5)]})
    head = None
    if args.foundry_root is not None:
        root = args.foundry_root.resolve()
        head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        require(head == COMMIT, "Foundry checkout is not the pinned commit")
        subprocess.run(["git", "-C", str(root), "diff", "--quiet", "HEAD", "--"], check=True)
    require(not os.environ.get("LOCAL_MSA_DIRS"), "Unset LOCAL_MSA_DIRS for the prespecified no-MSA comparison")
    # Import the installed, real RF3 parser. No engine import or weight loading here.
    from rf3.utils.inference import InferenceInput
    from biotite.structure import BondType
    native_utils = Path(inspect.getfile(InferenceInput)).resolve()
    require(digest(native_utils) == UTILS_SHA, "RF3 native parser source hash changed")
    engine_source = native_utils.parents[1] / "inference_engines/rf3.py"
    require(digest(engine_source) == ENGINE_SHA, "RF3 engine source hash changed")
    specifications = []
    gate = {"status": "running", "source_contract_commit": COMMIT, "verified_checkout_commit": head,
            "native_parser_path": str(native_utils), "native_parser_sha256": UTILS_SHA,
            "engine_sha256": ENGINE_SHA, "weight_loading_in_gate": False,
            "conditions": [], "versions": {},
            "version_scope": "The two imported RF3 source files are hash-pinned. With no checkout argument, the full package commit is not established by these two hashes alone."}
    for name in ("rc-foundry", "atomworks", "biotite", "torch", "rdkit"):
        try:
            gate["versions"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            gate["versions"][name] = None
    try:
        for filename, peptide, expected_sha in CONDITIONS:
            path = args.input_dir / filename
            require(digest(path) == expected_sha, f"Input bytes changed: {filename}")
            data = json.loads(path.read_text())
            require(set(data) == {"name", "components"}, "Unexpected conditioning or explicit bonds in input")
            require(len(data["components"]) == 3, "Input component count changed")
            enzyme = data["components"][0]["seq"]
            require(hashlib.sha256(enzyme.encode()).hexdigest() == ENZYME_SHA and len(enzyme) == 187, "Enzyme identity changed")
            require(data["components"] == [{"seq": enzyme, "chain_id": "A"},
                                            {"seq": peptide, "chain_id": "B"},
                                            {"smiles": "[Zn+2].O", "chain_id": "C"}], "Chemical input changed")
            spec = InferenceInput.from_json_dict(data)
            atom_map = check_native_input(spec, enzyme, peptide, int(BondType.SINGLE))
            map_path = args.out_dir / f"{data['name']}_native_atom_map.json"
            write_json(map_path, atom_map)
            gate["conditions"].append({"input": filename, "input_sha256": expected_sha,
                                       "example_id": spec.example_id, "atom_map": map_path.name,
                                       "atom_map_sha256": digest(map_path)})
            specifications.append(spec)
        gate["status"] = "passed_native_input_chemistry_gate"
    except BaseException:
        gate["status"] = "failed_native_input_chemistry_gate"
        gate["error"] = traceback.format_exc()
        raise
    finally:
        write_json(args.out_dir / "native_gate.json", gate)
    if args.infer_seed is None:
        return

    require(args.checkpoint is not None and args.checkpoint_sha256, "Inference requires a previously pinned checkpoint hash")
    require(digest(args.checkpoint) == args.checkpoint_sha256.lower(), "Checkpoint hash does not match the pin")
    assignments = [{"example_id": s.example_id, "seed": args.infer_seed, "sample": i,
                    "status": "assigned_not_yet_observed"} for s in specifications for i in range(5)]
    write_json(args.out_dir / "assignments_before_inference.json", assignments)
    write_json(args.out_dir / "checkpoint_pin.json", {"path": str(args.checkpoint.resolve()), "sha256": args.checkpoint_sha256.lower()})
    # This branch is for separately authorized remote inference only.
    from rf3.inference_engines.rf3 import RF3InferenceEngine
    require(Path(inspect.getfile(RF3InferenceEngine)).resolve() == engine_source, "Engine import changed")
    prediction_dir = args.out_dir / "predictions"
    error = None
    try:
        engine = RF3InferenceEngine(ckpt_path=str(args.checkpoint), seed=args.infer_seed,
                                    n_recycles=10, diffusion_batch_size=5, num_steps=200,
                                    early_stopping_plddt_threshold=0.0, compress_outputs=False)
        engine.run(inputs=specifications, out_dir=prediction_dir, dump_predictions=True,
                   dump_trajectories=False, one_model_per_file=True,
                   annotate_b_factor_with_plddt=True, skip_existing=False)
    except BaseException:
        error = traceback.format_exc()
        raise
    finally:
        for assignment in assignments:
            filename = f"{assignment['example_id']}_seed-{assignment['seed']}_sample-{assignment['sample']}_model.cif"
            matches = list(prediction_dir.rglob(filename)) if prediction_dir.exists() else []
            assignment["observed_files"] = [str(p.relative_to(args.out_dir)) for p in matches]
            assignment["status"] = "produced" if len(matches) == 1 else ("missing" if not matches else "ambiguous_multiple_outputs")
        write_json(args.out_dir / "assignments_after_inference.json", {"assignments": assignments, "error": error})


if __name__ == "__main__":
    main()
