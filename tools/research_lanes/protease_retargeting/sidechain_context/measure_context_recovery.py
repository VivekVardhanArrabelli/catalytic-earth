#!/usr/bin/env python3
"""Measure frozen joint reference-geometry recovery; never run models."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import statistics
import sys
import numpy as np
sys.dont_write_bytecode = True

GROUPS = {
    "zinc": [["ligand", 1, "ZN"]],
    "water": [["ligand", 1, "O"]],
    "histidine_36": [["enzyme", 36, "NE2"]],
    "histidine_40": [["enzyme", 40, "NE2"]],
    "metal_glutamate_152": [["enzyme", 152, a] for a in ("CD", "OE1", "OE2")],
    "general_base_37": [["enzyme", 37, a] for a in ("CD", "OE1", "OE2")],
    "tyrosine_115": [["enzyme", 115, a] for a in ("CZ", "OH")],
    "reactive_backbone": [["peptide", p, a] for p in (7, 8) for a in ("N", "CA", "C", "O")],
}
SWAPPABLE = {"metal_glutamate_152", "general_base_37"}
PEPTIDE = "ALQSSWGMMGML"
SHA = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def helpers(path):
    sys.path.insert(0, str(Path(path).resolve()))
    return importlib.import_module("measure_water_recovery")

def arrays(atoms, sequence, h):
    enzyme, peptide, ligand = h.identify(atoms, sequence)
    if len(enzyme) != 187:
        raise ValueError("Expected exact enzyme length187")
    ca = np.asarray([r["atoms"]["CA"] for r in enzyme], float)
    def get(spec):
        role, pos, name = spec
        return ligand[name] if role == "ligand" else (enzyme if role == "enzyme" else peptide)[pos-1]["atoms"][name]
    groups = {g: np.asarray([get(spec) for spec in specs], float) for g, specs in GROUPS.items()}
    return ca, groups

def reference(path, h):
    atoms = h.cif_atoms(Path(path), "retained_RFD3_scaffold")
    ca = sorted([a for a in atoms if a["chain"] == "A" and a["atom_name"] == "CA"], key=lambda a:a["residue_number"])
    if [a["residue_number"] for a in ca] != list(range(1,188)):
        raise ValueError("Reference enzyme numbering changed")
    sequence = "".join(h.AA[a["residue_name"]] for a in ca)
    return arrays(atoms, sequence, h)

def score_arrays(pred_ca, pred_groups, ref_ca, ref_groups, h):
    rotation, cx, cy, residual = h.fit_transform(pred_ca, ref_ca)
    values, permutations = {}, {}
    for name in GROUPS:
        moved = (np.asarray(pred_groups[name])-cx) @ rotation + cy
        wanted = np.asarray(ref_groups[name])
        orders = [list(range(len(wanted)))]
        if name in SWAPPABLE:
            orders.append([0,2,1])
        scores = [float(np.sqrt(np.mean(np.sum((moved-wanted[order])**2, axis=1)))) for order in orders]
        index = int(np.argmin(scores))
        values[name], permutations[name] = scores[index], orders[index]
    return {"group_rmsd_A": values, "reference_atom_permutations": permutations,
            "worst_group_rmsd_A": max(values.values()), "enzyme_CA_rmsd_to_scaffold_A": residual}

def decision(candidates, assignments, tolerance):
    pairs = []
    for seed in sorted({a["pair_seed"] for a in assignments}):
        pair = {c["arm"]: c for c in candidates if c["pair_seed"] == seed}
        hidden, revealed = pair.get("context_hidden"), pair.get("context_revealed")
        complete = bool(hidden and revealed and hidden["complete_ES"] and revealed["complete_ES"])
        row = {"pair_seed": seed, "complete": complete}
        if complete:
            row["revealed_minus_hidden_median_worst_group_A"] = revealed["median_worst_group_rmsd_A"]-hidden["median_worst_group_rmsd_A"]
            row["revealed_minus_hidden_group_median_A"] = {g: revealed["group_median_rmsd_A"][g]-hidden["group_median_rmsd_A"][g] for g in GROUPS}
        pairs.append(row)
    outcome = "incomplete_comparison"
    if len(pairs) == 4 and all(p["complete"] for p in pairs):
        positive = all(p["revealed_minus_hidden_median_worst_group_A"] < -tolerance and max(p["revealed_minus_hidden_group_median_A"].values()) <= tolerance for p in pairs)
        reverse = all(p["revealed_minus_hidden_median_worst_group_A"] > tolerance and min(p["revealed_minus_hidden_group_median_A"].values()) >= -tolerance for p in pairs)
        outcome = "consistent_revealed_context_reference_recovery_benefit" if positive else "consistent_hidden_context_reference_recovery_benefit" if reverse else "no_consistent_joint_reference_recovery_advantage"
    return outcome, pairs

def evaluate(manifest, plan, reference_path, helper_dir):
    h = helpers(helper_dir)
    if SHA(reference_path) != plan["reference_scaffold"]["sha256"]:
        raise ValueError("Frozen reference scaffold changed")
    if plan["primary"]["groups"] != GROUPS:
        raise ValueError("Frozen atom groups differ from implementation")
    ref_ca, ref_groups = reference(reference_path, h)
    candidates = manifest["candidates"]
    identifiers = [c["id"] for c in candidates]
    allowed = {a["id"] for a in plan["assignments"]}
    if len(identifiers) != len(set(identifiers)) or not set(identifiers) <= allowed:
        raise ValueError("Duplicate or unassigned candidate")
    results = []
    for assignment in plan["assignments"]:
        c = next((c for c in candidates if c["id"] == assignment["id"]), {})
        row = {k: assignment[k] for k in ("id", "arm", "pair_seed")}
        sequence = c.get("enzyme_sequence") or ""
        input_path = c.get("rf3_input_paths", {}).get("ES")
        name, input_error = None, None
        if sequence and input_path and Path(input_path).exists():
            try:
                spec = json.loads(Path(input_path).read_text())
                assert hashlib.sha256(sequence.encode()).hexdigest() == c["enzyme_sha256"]
                assert spec["components"] == [{"seq": sequence, "chain_id": "A"}, {"seq": PEPTIDE, "chain_id": "B"}, {"smiles": "[Zn+2].O", "chain_id": "C"}]
                assert spec["name"] == assignment["id"]+"_ES"
                name = spec["name"]
            except Exception as exc:
                input_error = f"{type(exc).__name__}: {exc}"
        outputs = []
        for slot in h.assigned_samples(c.get("rf3_output_dirs", {}).get("ES"), name):
            paths = slot.pop("matches")
            slot["observed_files"] = [str(p) for p in paths]
            try:
                if input_error:
                    raise ValueError(input_error)
                if len(paths) != 1 or not sequence:
                    raise ValueError("Assigned output missing or ambiguous")
                atoms = h.cif_atoms(paths[0], "RF3_ES")
                ca, groups = arrays(atoms, sequence, h)
                slot.update(score_arrays(ca, groups, ref_ca, ref_groups, h))
                slot.update(status="measured", sha256=SHA(paths[0]))
                slot["scaffold_site_context"] = h.observe(paths[0], sequence,
                    [ref_groups[g][0] for g in ("zinc", "histidine_36", "histidine_40")], ref_groups["water"][0])
            except Exception as exc:
                slot.update(status="missing_or_unresolved", error=f"{type(exc).__name__}: {exc}")
            outputs.append(slot)
        complete = len(outputs) == 5 and all(r["status"] == "measured" for r in outputs)
        row.update(outputs=outputs, assigned_ES=5, observed_ES=sum(r["status"] == "measured" for r in outputs), complete_ES=complete,
                   median_worst_group_rmsd_A=statistics.median(r["worst_group_rmsd_A"] for r in outputs) if complete else None,
                   group_median_rmsd_A={g: statistics.median(r["group_rmsd_A"][g] for r in outputs) for g in GROUPS} if complete else None)
        row["structural_context"] = {state: h.structural_context(c, state, sequence) for state in ("monomer", "ES")}
        results.append(row)
    outcome, pairs = decision(results, plan["assignments"], plan["primary"]["numerical_tolerance_A"])
    return {"assigned_candidates": 8, "assigned_ES": 40, "assigned_monomer": 40,
            "observed_ES": sum(c["observed_ES"] for c in results),
            "observed_monomer_context": sum(r["status"] == "measured" for c in results for r in c["structural_context"]["monomer"]),
            "reference_scaffold_sha256": SHA(reference_path), "candidates": results, "paired_seed_results": pairs,
            "decision": outcome, "claim_boundary": plan["claim_boundary"]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "decision", "reference-scaffold", "output"):
        ap.add_argument("--"+name, required=True, type=Path)
    ap.add_argument("--helper-dir", type=Path, default=Path(__file__).resolve().parents[1]/"water_conditioning")
    args = ap.parse_args()
    report = evaluate(json.loads(args.manifest.read_text()), json.loads(args.decision.read_text()), args.reference_scaffold, args.helper_dir)
    report.update(measurement_script_sha256=SHA(__file__), decision_sha256=SHA(args.decision), manifest_sha256=SHA(args.manifest))
    with args.output.open("x") as handle:
        handle.write(json.dumps(report, indent=2, allow_nan=False)+"\n")

if __name__ == "__main__":
    main()
