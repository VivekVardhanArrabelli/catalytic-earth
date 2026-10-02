#!/usr/bin/env python3
"""Native RF3 worker: one loaded engine, reset seed0 before each input.

Prepared prospectively; does not provision/download. Running it loads the
approved RF3 checkpoint and produces only the supplied assigned five-draw inputs.
Native identity gate is copied verbatim from the frozen predecessor runner.
"""
import argparse
import hashlib
import inspect
import json
import os
from pathlib import Path
import time
import traceback

COMMIT = "0932f1cb165ae7d413c11b1a7acc04ee31758817"
RF3_SHA = "364ef592fd8042a9cf4176d045015190f8322f961ccca38d891b20ca578d3bb0"
NATIVE_SOURCE_PINS = {
    "parser": "71f306e5dd7369c7736ffd6a3390791465cb1641e67d0d03c0b4399923d1027b",
    "engine": "292bba9feae83d6001dae83190da170c5e1d303adbdb4f1b5257e55f98b0bd55",
    "base": "fcb76d4a8f5fbf4d3f0e33974e04a0379ee3717127f316ab21cf22bbf3c1437f",
}

TARGET = "ALQSSWGMMGML"

AA = dict(zip("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(), "ARNDCQEGHILKMFPSTWYV"))

ROLES = {36: "H", 37: "E", 40: "H", 115: "Y", 152: "E"}

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n")
    tmp.replace(path)

def identities(aa, expected_a=None, es=True, check_bonds=False):
    """Inspect native atoms, not the concatenated MPNN FASTA sequence."""
    atoms, residues, keyed = [], {}, {}
    for i in range(len(aa)):
        c, r, n = str(aa.chain_id[i]), int(aa.res_id[i]), str(aa.atom_name[i])
        key = (c, r, n)
        require(key not in keyed, f"Duplicate native atom identity {key}")
        keyed[key] = i
        residues.setdefault(c, {})
        old = residues[c].setdefault(r, str(aa.res_name[i]))
        require(old == str(aa.res_name[i]), f"Mixed residue identity {c}{r}")
        atoms.append({"chain": c, "residue": r, "name": n, "element": str(aa.element[i]).upper()})
    sequences = {}
    for chain, length in (("A", 187), *(([("B", 12)] if es else []))):
        require(sorted(residues.get(chain, {})) == list(range(1, length + 1)), f"Changed {chain} length/numbering")
        sequences[chain] = "".join(AA.get(residues[chain][r], "?") for r in range(1, length + 1))
        require("?" not in sequences[chain], f"Noncanonical {chain} sequence")
        for r in range(1, length + 1):
            require(all((chain, r, a) in keyed for a in ("N", "CA", "C", "O")), f"Missing backbone {chain}{r}")
    require(expected_a is None or sequences["A"] == expected_a, "Enzyme sequence changed")
    require(all(sequences["A"][r-1] == name for r, name in ROLES.items()), "Catalytic identities changed")
    if es:
        require(sequences["B"] == TARGET, "Substrate sequence changed")
    else:
        require(set(residues) == {"A"}, "Unexpected monomer component")
    report = {"sequences": sequences, "residue_counts": {k: len(v) for k, v in residues.items()}, "atom_count": len(aa)}
    if es:
        other = [(i, a) for i, a in enumerate(atoms) if a["chain"] not in ("A", "B") and a["element"] not in ("H", "D")]
        require(sorted(a["element"] for i, a in other) == ["O", "ZN"], "Zn/water chemical identity or count changed")
        fields = [f for f in ("charge", "formal_charge") if f in aa.get_annotation_categories()]
        require(fields, "No native formal-charge annotation")
        charges = [float(x) for x in aa.get_annotation(fields[0])]
        require(all(charges == [float(x) for x in aa.get_annotation(f)] for f in fields), "Charge fields disagree")
        zinc = next(i for i, a in other if a["element"] == "ZN")
        water = next(i for i, a in other if a["element"] == "O")
        require(charges[zinc] == 2.0 and charges[water] == 0.0, "Zn2+/neutral-water formal charge lost")
        bonds = [] if aa.bonds is None else aa.bonds.as_array().tolist()
        require(not any(zinc in row[:2] for row in bonds), "Unexpected covalent bond to Zn")
        water_neighbors = [j if i == water else i for i, j, _ in bonds if water in (i, j)]
        require(all(atoms[i]["element"] in ("H", "D") for i in water_neighbors), "Water has a heavy-atom bond")
        require(len(set(water_neighbors)) in (0, 2), "Unexpected water explicit-H count")
        report["ligand"] = {"Zn_index": zinc, "water_O_index": water, "Zn_charge": charges[zinc], "O_charge": charges[water], "water_H_neighbors": water_neighbors}
    if check_bonds:
        from biotite.structure import BondType
        require(aa.bonds is not None, "No native peptide bond graph")
        edges = {tuple(sorted((int(i), int(j)))): int(t) for i, j, t in aa.bonds.as_array()}
        for chain, sequence in sequences.items():
            for r in range(1, len(sequence)):
                require(edges.get(tuple(sorted((keyed[(chain, r, "C")], keyed[(chain, r+1, "N")])))) == int(BondType.SINGLE), f"Changed peptide bond {chain}{r}-{r+1}")
    return report

def run(config_path):
    from lightning.fabric import seed_everything
    from rf3.utils.inference import InferenceInput
    from rf3.inference_engines.rf3 import RF3InferenceEngine
    from foundry.inference_engines.base import BaseInferenceEngine
    for name, native in (("parser", InferenceInput), ("engine", RF3InferenceEngine), ("base", BaseInferenceEngine)):
        require(digest(inspect.getfile(native)) == NATIVE_SOURCE_PINS[name], f"Pinned native {name} source changed")
    cfg = json.loads(Path(config_path).read_text())
    require(0 < len(cfg["inputs"]) <= 16, "At most sixteen assigned five-draw inputs are allowed")
    require(not os.environ.get("LOCAL_MSA_DIRS"), "Unexpected local MSA configuration")
    require(digest(cfg["checkpoint"]) == RF3_SHA, "RF3 checkpoint differs from pinned prior execution")
    out = Path(cfg["out_dir"])
    require(not out.exists(), "Prediction directory exists; no retry or overwrite")
    specs, gate, names = [], [], set()
    for row in cfg["inputs"]:
        require(row["state"] in ("monomer", "ES"), "Unassigned prediction state")
        data = json.loads(Path(row["path"]).read_text())
        require(set(data) == {"name", "components"}, "Unexpected RF3 conditioning fields")
        require(data["name"] not in names, "Duplicate input name")
        names.add(data["name"])
        expected = [{"seq": row["enzyme_sequence"], "chain_id": "A"}]
        if row["state"] == "ES":
            expected += [{"seq": TARGET, "chain_id": "B"}, {"smiles": "[Zn+2].O", "chain_id": "C"}]
        require(data["components"] == expected, "RF3 input components changed")
        # Reset input materialization too; reference construction is not pose conditioning.
        seed_everything(0, workers=True, verbose=True)
        spec = InferenceInput.from_json_dict(data)
        report = identities(spec.atom_array, row["enzyme_sequence"], row["state"] == "ES", check_bonds=True)
        require(spec.template_selection is None and spec.ground_truth_conformer_selection is None, "Unexpected RF3 structural conditioning")
        require(not spec.cyclic_chains and not any(v.get("msa_path") for v in spec.chain_info.values() if isinstance(v, dict)), "Unexpected cyclic/MSA conditioning")
        gate.append({"id": data["name"], "input_sha256": digest(row["path"]), **report})
        specs.append(spec)
    save(out.parent / "rf3_native_gate.json", {"status": "passed_native_input_gate_before_weight_loading", "inputs": gate})
    reset = {"method": "lightning.fabric.seed_everything(0, workers=True, verbose=True)",
        "native_base_source_sha256": NATIVE_SOURCE_PINS["base"],
        "reset_before_materialization": True, "reset_before_each_single_input_run": True,
        "engine_reused": True, "additional_outputs": 0,
        "scope": "Controls dependence on earlier input RNG consumption; does not guarantee bitwise GPU determinism or atom-matched noise across different sequences/shapes.",
        "inputs": []}
    save(out.parent / "rf3_rng_reset_receipt.json", reset)
    engine = RF3InferenceEngine(ckpt_path=cfg["checkpoint"], seed=0, n_recycles=10,
        diffusion_batch_size=5, num_steps=200, early_stopping_plddt_threshold=0.0, compress_outputs=False)
    for spec in specs:
        row = {"example_id": spec.example_id, "seed": 0, "assigned_samples": list(range(5)),
               "status": "started", "started_unix": time.time()}
        reset["inputs"].append(row)
        save(out.parent / "rf3_rng_reset_receipt.json", reset)
        try:
            # Same public helper used by native BaseInferenceEngine.__init__.
            # run() supports an already-loaded engine and a single InferenceInput.
            seed_everything(0, workers=True, verbose=True)
            engine.run(inputs=[spec], out_dir=out, dump_predictions=True,
                dump_trajectories=False, one_model_per_file=True,
                annotate_b_factor_with_plddt=True, skip_existing=False)
            row["status"] = "native_run_returned"
        except BaseException:
            row.update(status="failed_no_retry", error=traceback.format_exc())
            raise
        finally:
            row["finished_unix"] = time.time()
            save(out.parent / "rf3_rng_reset_receipt.json", reset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", "--worker-config", dest="config", type=Path, required=True)
    run(parser.parse_args().config)
