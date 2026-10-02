#!/usr/bin/env python3
"""Finite, source-pinned 8-backbone/8-sequence/80-prediction experiment.

No provisioning, downloads, replacement designs, or retries. Default mode only
writes the frozen assignments. --execute requires a separately approved runtime.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

COMMIT = "0932f1cb165ae7d413c11b1a7acc04ee31758817"
TARGET = "ALQSSWGMMGML"
AA = dict(zip("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(), "ARNDCQEGHILKMFPSTWYV"))
ROLES = {36: "H", 37: "E", 40: "H", 115: "Y", 152: "E"}
INPUT_PINS = {
    "water_fixed.json": "5d3cac4d1588bb5662b2f3b8a61e896d012601526e85ce553262775892d1c390",
    "water_unfixed.json": "43399d8c7b3e89f663306789d9abc2bc07f4b07b7c5fb9fbfaebe4ab8875a943",
    "ALQSSWGMMGML78_Zn2plus.pdb": "85830251fcf93fb26c00a6c79cfb6c2815b444e3db941e7470cf341cb8ebb8e0",
}
WEIGHTS = {"rfd3": ("rfd3_foundry_2025_12_01_remapped.ckpt", 2690316669),
           "mpnn": ("ligandmpnn_v_32_010_25.pt", 10541943),
           "rf3": ("rf3_foundry_01_24_latest_remapped.ckpt", 3038876446)}
RF3_SHA = "364ef592fd8042a9cf4176d045015190f8322f961ccca38d891b20ca578d3bb0"
RF3_MIN_REMAINING_SECONDS = 900


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


def native_array(path):
    from atomworks.io import parse
    from atomworks.io.parser import STANDARD_PARSER_ARGS
    kwargs = dict(STANDARD_PARSER_ARGS)
    kwargs.update(remove_ccds=[], remove_waters=False)
    data = parse(filename=str(path), **kwargs)
    # A generated design is one deposited model, not a biological assembly.
    require("asym_unit" in data, "Native parser returned no asymmetric unit")
    return data["asym_unit"][0]


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


def mpnn_gate(config):
    from mpnn.utils.inference import MPNNInferenceInput
    cfg = json.loads(Path(config).read_text())
    spec = MPNNInferenceInput.from_atom_array_and_dict(input_dict=cfg["inputs"][0])
    report = identities(spec.atom_array)
    aa = spec.atom_array
    require("mpnn_designed_residue_mask" in aa.get_annotation_categories(), "No native sequence-design mask")
    for i in range(len(aa)):
        c, r = str(aa.chain_id[i]), int(aa.res_id[i])
        if c in ("A", "B"):
            expected = c == "A" and r not in ROLES
            require(bool(aa.mpnn_designed_residue_mask[i]) == expected, f"Incorrect native sequence mask {c}{r}")
    report["fixed_A_positions"] = list(ROLES)
    report["fixed_B_positions"] = list(range(1, 13))
    report["status"] = "passed_native_mpnn_input_gate"
    save(Path(config).with_name("mpnn_native_gate.json"), report)


def rf3_worker(config):
    from rf3.utils.inference import InferenceInput
    cfg = json.loads(Path(config).read_text())
    specs, gate = [], []
    require(not os.environ.get("LOCAL_MSA_DIRS"), "Unexpected local MSA configuration")
    for row in cfg["inputs"]:
        data = json.loads(Path(row["path"]).read_text())
        require(set(data) == {"name", "components"}, "Unexpected RF3 conditioning fields")
        expected = [{"seq": row["enzyme_sequence"], "chain_id": "A"}]
        if row["state"] == "ES":
            expected += [{"seq": TARGET, "chain_id": "B"}, {"smiles": "[Zn+2].O", "chain_id": "C"}]
        require(data["components"] == expected, "RF3 input components changed")
        spec = InferenceInput.from_json_dict(data)
        report = identities(spec.atom_array, row["enzyme_sequence"], row["state"] == "ES", check_bonds=True)
        require(spec.template_selection is None and spec.ground_truth_conformer_selection is None, "Unexpected RF3 structural conditioning")
        require(not spec.cyclic_chains and not any(v.get("msa_path") for v in spec.chain_info.values() if isinstance(v, dict)), "Unexpected cyclic/MSA conditioning")
        gate.append({"id": data["name"], "input_sha256": digest(row["path"]), **report})
        specs.append(spec)
    save(Path(cfg["out_dir"]).parent / "rf3_native_gate.json", {"status": "passed_native_input_gate_before_weight_loading", "inputs": gate})
    from rf3.inference_engines.rf3 import RF3InferenceEngine
    engine = RF3InferenceEngine(ckpt_path=cfg["checkpoint"], seed=0, n_recycles=10,
        diffusion_batch_size=5, num_steps=200, early_stopping_plddt_threshold=0.0, compress_outputs=False)
    engine.run(inputs=specs, out_dir=Path(cfg["out_dir"]), dump_predictions=True,
        dump_trajectories=False, one_model_per_file=True, annotate_b_factor_with_plddt=True, skip_existing=False)


def assigned_manifest():
    candidates = []
    for seed in range(4):
        for arm in ("water_fixed", "water_coordinate_free"):
            cid = f"{arm}_seed{seed}"
            candidates.append({"id": cid, "arm": arm, "rfd3_seed": seed, "mpnn_seed": 100+seed,
                "status": "assigned_not_started", "enzyme_sequence": None, "enzyme_sha256": None,
                "scaffold_path": None, "mpnn_output_path": None,
                "rf3_input_paths": {"monomer": None, "ES": None},
                "rf3_output_dirs": {"monomer": None, "ES": None},
                "rf3_assignments": [{"state": state, "seed": 0, "sample": sample, "status": "assigned_not_started", "path": None}
                                    for state in ("monomer", "ES") for sample in range(5)]})
    return {"source_commit": COMMIT, "target_sequence": TARGET, "intended_bond": "B:G7:C--B:M8:N",
        "role_map": {"metal_histidine_1": {"chain": "A", "position": 36, "identity": "H", "atom": "NE2"},
                     "general_base": {"chain": "A", "position": 37, "identity": "E"},
                     "metal_histidine_2": {"chain": "A", "position": 40, "identity": "H", "atom": "NE2"},
                     "oxyanion_donor": {"chain": "A", "position": 115, "identity": "Y", "atom": "OH"},
                     "metal_glutamate": {"chain": "A", "position": 152, "identity": "E"}},
        "assigned_candidates": 8, "assigned_RF3_outputs": 80, "primary_assigned_ES_outputs": 40,
        "missingness_rule": "No replacement, rescue, score selection or imputation. Produced does not mean chemically valid or active.",
        "candidates": candidates}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worker", choices=("mpnn-gate", "rf3"))
    p.add_argument("--worker-config", type=Path)
    p.add_argument("--input-dir", type=Path)
    p.add_argument("--foundry-root", type=Path)
    p.add_argument("--out-dir", type=Path)
    p.add_argument("--checkpoint-dir", type=Path)
    p.add_argument("--checkpoint-receipt", type=Path)
    p.add_argument("--native-pair-receipt", type=Path)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--max-seconds", type=int, default=5400, help="Run-only wall limit; root separately enforces full rental cap and retrieval reserve")
    args = p.parse_args()
    if args.worker:
        return (mpnn_gate if args.worker == "mpnn-gate" else rf3_worker)(args.worker_config)
    require(args.out_dir and args.input_dir and args.foundry_root, "input-dir, foundry-root and out-dir required")
    out, inputs, foundry = args.out_dir.resolve(), args.input_dir.resolve(), args.foundry_root.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest = assigned_manifest()
    manifest_path = out / "candidate_manifest.json"
    save(manifest_path, manifest)
    for name, pin in INPUT_PINS.items():
        require(digest(inputs / name) == pin, f"Corrected input changed: {name}")
    pins = json.loads(Path(__file__).with_name("consumer_source_pins.json").read_text())
    for relative, pin in pins["files"].items():
        require(digest(foundry / relative) == pin, f"Consumer source changed: {relative}")
    manifest["input_pins"] = INPUT_PINS
    manifest["source_pin_manifest_sha256"] = digest(Path(__file__).with_name("consumer_source_pins.json"))
    manifest["runner_sha256"] = digest(__file__)
    save(manifest_path, manifest)
    if not args.execute:
        print(f"Prepared all frozen assignments without model execution: {manifest_path}")
        return
    require(1 <= args.max_seconds <= 6600, "Invalid run duration; retain at least ten minutes within external two-hour cap")
    require(args.checkpoint_dir and args.checkpoint_receipt and args.native_pair_receipt, "Execution requires native-pair and checkpoint receipts")
    native_receipt = json.loads(args.native_pair_receipt.read_text())
    require(native_receipt.get("status") == "passed_actual_native_pair_checks" and native_receipt.get("model_execution") is False, "Native pair did not pass the actual weight-free checks")
    manifest["native_pair_receipt"] = {"path": str(args.native_pair_receipt.resolve()), "sha256": digest(args.native_pair_receipt)}
    receipts = {r["file"]: r for r in json.loads(args.checkpoint_receipt.read_text())["checkpoints"]}
    checkpoints = {}
    for model, (name, size) in WEIGHTS.items():
        path = args.checkpoint_dir.resolve() / name
        require(path.stat().st_size == size and digest(path) == receipts[name]["sha256"], f"Checkpoint changed: {name}")
        if model == "rf3":
            require(receipts[name]["sha256"] == RF3_SHA, "RF3 differs from prior successful run")
        checkpoints[model] = str(path)
    manifest["checkpoint_receipts"] = list(receipts.values())
    env = os.environ.copy()
    require(not env.get("LOCAL_MSA_DIRS"), "Unset LOCAL_MSA_DIRS")
    env["PYTHONPATH"] = os.pathsep.join(str(foundry / s) for s in ("src", "models/rfd3/src", "models/mpnn/src", "models/rf3/src"))
    script = str(Path(__file__).resolve())
    deadline = time.monotonic() + args.max_seconds
    commands = []

    def command(tokens, label):
        remaining = deadline - time.monotonic()
        require(remaining > 0, "Assigned runtime exhausted")
        log = out / "logs" / f"{label}.log"
        log.parent.mkdir(exist_ok=True)
        row = {"label": label, "argv": [str(t) for t in tokens], "started_unix": time.time(), "status": "running"}
        commands.append(row)
        save(out / "commands.json", commands)
        with log.open("w") as handle:
            proc = subprocess.Popen(row["argv"], stdout=handle, stderr=subprocess.STDOUT, env=env, start_new_session=True)
            try:
                code = proc.wait(timeout=remaining)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                row.update(status="stopped_at_runtime_limit_or_interrupt", returncode=proc.returncode, finished_unix=time.time())
                save(out / "commands.json", commands)
                raise
        row.update(status="completed" if code == 0 else "failed", returncode=code, finished_unix=time.time())
        save(out / "commands.json", commands)
        require(code == 0, f"Native stage {label} failed; see {log}")

    try:
        for c in manifest["candidates"]:
            directory = out / "candidates" / c["id"]
            directory.mkdir(parents=True)
            try:
                source = inputs / ("water_fixed.json" if c["arm"] == "water_fixed" else "water_unfixed.json")
                data = json.loads(source.read_text())
                data["des"]["input"] = str(inputs / "ALQSSWGMMGML78_Zn2plus.pdb")
                resolved = directory / "rfd3_input.json"
                save(resolved, data)
                rfd_out = directory / "rfd3"
                c["status"] = "rfd3_started"; save(manifest_path, manifest)
                command([sys.executable, "-m", "rfd3.cli", "design", f"inputs={resolved}", f"out_dir={rfd_out}", f"ckpt_path={checkpoints['rfd3']}", f"seed={c['rfd3_seed']}", "n_batches=1", "diffusion_batch_size=1", "inference_sampler.num_timesteps=200", "inference_sampler.step_scale=1.5", "skip_existing=False", "dump_prediction_metadata_json=True", "dump_trajectories=False"], c["id"] + "_rfd3")
                structures = list(rfd_out.rglob("*.cif.gz")) + list(rfd_out.rglob("*.cif"))
                require(len(structures) == 1, f"Expected one RFD3 backbone, observed {len(structures)}")
                scaffold = structures[0]
                c["scaffold_path"] = str(scaffold)
                c["scaffold_sha256"] = digest(scaffold)
                cfg = {"model_type": "ligand_mpnn", "checkpoint_path": checkpoints["mpnn"], "is_legacy_weights": True,
                    "out_directory": str(directory / "mpnn"), "write_fasta": True, "write_structures": True,
                    "inputs": [{"structure_path": str(scaffold), "name": c["id"], "seed": c["mpnn_seed"],
                        "batch_size": 1, "number_of_batches": 1, "temperature": 0.1, "structure_noise": 0.0,
                        "atomize_side_chains": False, "remove_ccds": [], "remove_waters": False,
                        "fixed_residues": [f"A{r}" for r in ROLES] + [f"B{r}" for r in range(1, 13)]}]}
                mpnn_cfg = directory / "mpnn_config.json"
                save(mpnn_cfg, cfg)
                command([sys.executable, script, "--worker", "mpnn-gate", "--worker-config", str(mpnn_cfg)], c["id"] + "_mpnn_gate")
                c["status"] = "mpnn_started"; save(manifest_path, manifest)
                command([sys.executable, "-m", "mpnn.inference", "--config_json", str(mpnn_cfg)], c["id"] + "_mpnn")
                structure = directory / "mpnn" / f"{c['id']}_b0_d0.cif"
                require(structure.exists() and len(list(structure.parent.glob("*.cif"))) == 1, "Expected exactly one MPNN structure")
                # Parent loads only the native parser; model processes have exited.
                for entry in reversed(env["PYTHONPATH"].split(os.pathsep)):
                    if entry not in sys.path: sys.path.insert(0, entry)
                report = identities(native_array(structure))
                save(directory / "mpnn_output_identity.json", report)
                enzyme = report["sequences"]["A"]
                c.update(status="sequence_ready", enzyme_sequence=enzyme, enzyme_sha256=hashlib.sha256(enzyme.encode()).hexdigest(), mpnn_output_path=str(structure), mpnn_output_sha256=digest(structure))
                for state in ("monomer", "ES"):
                    name = f"{c['id']}_{state}"
                    components = [{"seq": enzyme, "chain_id": "A"}]
                    if state == "ES": components += [{"seq": TARGET, "chain_id": "B"}, {"smiles": "[Zn+2].O", "chain_id": "C"}]
                    path = directory / f"rf3_{state}.json"
                    save(path, {"name": name, "components": components})
                    c["rf3_input_paths"][state] = str(path)
                    c["rf3_output_dirs"][state] = str(out / "rf3" / "predictions" / name)
            except Exception:
                c["status"] = "failed_no_replacement"
                c["error"] = traceback.format_exc()
            finally:
                save(manifest_path, manifest)
            if time.monotonic() >= deadline: break
        ready = [c for c in manifest["candidates"] if c["status"] == "sequence_ready"]
        remaining = deadline - time.monotonic()
        manifest["RF3_start_budget_check"] = {"remaining_seconds": remaining, "minimum_seconds": RF3_MIN_REMAINING_SECONDS,
            "status": "eligible" if ready and remaining >= RF3_MIN_REMAINING_SECONDS else "not_started_preserve_missingness"}
        if ready and remaining >= RF3_MIN_REMAINING_SECONDS:
            rf3_cfg = out / "rf3" / "config.json"
            save(rf3_cfg, {"checkpoint": checkpoints["rf3"], "out_dir": str(out / "rf3" / "predictions"),
                "inputs": [{"path": c["rf3_input_paths"][s], "state": s, "enzyme_sequence": c["enzyme_sequence"]}
                           for c in ready for s in ("monomer", "ES")]})
            for c in ready: c["status"] = "rf3_started"
            save(manifest_path, manifest)
            command([sys.executable, script, "--worker", "rf3", "--worker-config", str(rf3_cfg)], "all_assigned_available_RF3")
    except BaseException:
        manifest["run_error"] = traceback.format_exc()
        raise
    finally:
        for c in manifest["candidates"]:
            for a in c["rf3_assignments"]:
                folder = c["rf3_output_dirs"][a["state"]]
                name = f"{c['id']}_{a['state']}_seed-0_sample-{a['sample']}_model.cif"
                matches = list(Path(folder).rglob(name)) if folder and Path(folder).exists() else []
                a["status"] = "produced_pending_measurement" if len(matches) == 1 else ("missing" if not matches else "ambiguous")
                a["path"] = str(matches[0]) if len(matches) == 1 else None
                if len(matches) == 1: a["sha256"] = digest(matches[0])
            if all(a["status"] == "produced_pending_measurement" for a in c["rf3_assignments"]): c["status"] = "all_10_predictions_produced_pending_measurement"
            elif c["status"] in ("assigned_not_started", "sequence_ready", "rf3_started"): c["status"] = "incomplete_no_replacement"
        manifest["observed_RF3_outputs"] = sum(a["status"] == "produced_pending_measurement" for c in manifest["candidates"] for a in c["rf3_assignments"])
        manifest["completed_unix"] = time.time()
        save(manifest_path, manifest)


if __name__ == "__main__":
    main()
