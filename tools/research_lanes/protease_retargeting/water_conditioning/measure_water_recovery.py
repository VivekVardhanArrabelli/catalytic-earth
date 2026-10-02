#!/usr/bin/env python3
"""Measure the prospectively assigned water-conditioning experiment; no inference."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics

import numpy as np
from window_metrics import cif_atoms, AA, angle, distance

ROLES = {"His1": (36, "HIS", "NE2"), "base": (37, "GLU", "OE1"),
         "His2": (40, "HIS", "NE2"), "donor": (115, "TYR", "OH"),
         "Glu_ligand": (152, "GLU", "OE1")}
PEPTIDE = "ALQSSWGMMGML"


def require(value, message):
    if not value:
        raise ValueError(message)


def fit_transform(predicted, reference):
    x, y = np.asarray(predicted, float), np.asarray(reference, float)
    require(x.shape == y.shape and x.ndim == 2 and x.shape[1] == 3,
            "Alignment inputs have incompatible shapes")
    cx, cy = x.mean(axis=0), y.mean(axis=0)
    u, s, vt = np.linalg.svd((x - cx).T @ (y - cy))
    require(s[1] > 1e-6, "Undefined collinear or coincident anchor frame")
    correction = np.eye(3)
    correction[2, 2] = np.linalg.det(u @ vt)
    rotation = u @ correction @ vt
    residual = float(np.sqrt(np.mean(np.sum(((x-cx) @ rotation + cy-y)**2, axis=1))))
    return rotation, cx, cy, residual


def water_recovery(anchors, water, reference_anchors, reference_water):
    rotation, cx, cy, residual = fit_transform(anchors, reference_anchors)
    moved_water = (np.asarray(water)-cx) @ rotation + cy
    return {"source_water_recovery_error_A": float(np.linalg.norm(moved_water-reference_water)),
            "three_anchor_fit_rmsd_A": residual}


def reference(path):
    rows = {}
    for line in path.read_text().splitlines():
        if line[:6] in ("ATOM  ", "HETATM"):
            key = (line[21], int(line[22:26]), line[12:16].strip())
            rows[key] = [float(line[i:i+8]) for i in (30, 38, 46)]
    return [rows[k] for k in (("C", 1, "ZN1"), ("A", 293, "NE2"), ("A", 297, "NE2"))], rows[("C", 1, "O1")]


def identify(atoms, sequence):
    chains = {}
    for atom in atoms:
        residue = chains.setdefault(atom["chain"], {}).setdefault(
            (atom["residue_number"], atom["insertion_code"]), {"name": atom["residue_name"], "atoms": {}})
        require(residue["name"] == atom["residue_name"], "Mixed residue identity")
        require(atom["atom_name"] not in residue["atoms"], "Duplicate atom")
        residue["atoms"][atom["atom_name"]] = atom["coordinates_angstrom"]
    def match(wanted):
        choices = [(chain, [rows[k] for k in sorted(rows)]) for chain, rows in chains.items()
                   if "".join(AA.get(rows[k]["name"], "?") for k in sorted(rows)) == wanted]
        require(len(choices) == 1, "Exact unique sequence-chain identity missing")
        return choices[0]
    enzyme_chain, enzyme = match(sequence)
    peptide_chain, peptide = match(PEPTIDE)
    ligand = [a for a in atoms if a["chain"] not in (enzyme_chain, peptide_chain)
              and a["element"] not in ("H", "D")]
    require(sorted(a["element"] for a in ligand) == ["O", "ZN"], "Expected exactly Zn and water oxygen")
    for position, name, _ in ROLES.values():
        require(enzyme[position-1]["name"] == name, "Catalytic residue identity changed")
    return enzyme, peptide, {a["element"]: a["coordinates_angstrom"] for a in ligand}


def observe(path, sequence, anchors, source_water):
    record = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    try:
        enzyme, peptide, ligand = identify(cif_atoms(path, str(path)), sequence)
        e = lambda p, name: enzyme[p-1]["atoms"][name]
        p = lambda pos, name: peptide[pos-1]["atoms"][name]
        zinc, water = ligand["ZN"], ligand["O"]
        record.update(water_recovery([zinc, e(36, "NE2"), e(40, "NE2")], water, anchors, source_water))
        record["geometry"] = {
            "Zn_H36_NE2_A": distance(zinc, e(36, "NE2")),
            "Zn_H40_NE2_A": distance(zinc, e(40, "NE2")),
            "Zn_E152_min_A": min(distance(zinc, e(152, o)) for o in ("OE1", "OE2")),
            "E37_water_min_A": min(distance(e(37, o), water) for o in ("OE1", "OE2")),
            "Zn_water_A": distance(zinc, water), "Zn_G7_O_A": distance(zinc, p(7, "O")),
            "water_G7_C_A": distance(water, p(7, "C")),
            "water_G7_C_G7_O_degrees": angle(water, p(7, "C"), p(7, "O")),
            "Y115_OH_G7_O_A": distance(e(115, "OH"), p(7, "O")),
            "Y115_CZ_OH_G7_O_degrees": angle(e(115, "CZ"), e(115, "OH"), p(7, "O")),
            "G7_C_M8_N_A": distance(p(7, "C"), p(8, "N")),
        }
        record["amide_register_distances_A"] = {f"{PEPTIDE[i-1]}{i}-{PEPTIDE[i]}{i+1}": distance(zinc, p(i, "O")) for i in range(1, 12)}
        record["status"] = "measured"
    except Exception as exc:
        record.update(status="missing_or_unresolved", error=f"{type(exc).__name__}: {exc}")
    return record


def assigned_samples(directory, example_id):
    """Never count native top-ranked/aggregate copies as additional samples."""
    rows = []
    for sample in range(5):
        basename = f"{example_id}_seed-0_sample-{sample}_model.cif"
        matches = sorted(set(Path(directory).rglob(basename)) |
                         set(Path(directory).rglob(basename + ".gz"))) if directory and example_id else []
        rows.append({"seed": 0, "sample": sample, "matches": matches})
    return rows


def scaffold_agreement(path, scaffold, sequence):
    """All enzyme C-alpha positions; no best subset or catalytic-only alignment."""
    predicted = cif_atoms(path, str(path))
    designed = cif_atoms(Path(scaffold), str(scaffold))
    chains = {}
    for atom in predicted:
        if atom["atom_name"] == "CA" and atom["residue_name"] in AA:
            key = (atom["residue_number"], atom["insertion_code"])
            require(key not in chains.setdefault(atom["chain"], {}), "Duplicate C-alpha")
            chains[atom["chain"]][key] = atom
    choices = [[rows[k] for k in sorted(rows)] for rows in chains.values()
               if "".join(AA[rows[k]["residue_name"]] for k in sorted(rows)) == sequence]
    require(len(choices) == 1, "Unique exact predicted enzyme sequence required for scaffold comparison")
    fixed = sorted([a for a in designed if a["chain"] == "A" and a["atom_name"] == "CA"],
                   key=lambda a: (a["residue_number"], a["insertion_code"]))
    require([a["residue_number"] for a in fixed] == list(range(1,188)), "Scaffold A187 numbering changed")
    _, _, _, rmsd = fit_transform([a["coordinates_angstrom"] for a in choices[0]],
                                  [a["coordinates_angstrom"] for a in fixed])
    return {"enzyme_CA_rmsd_to_scaffold_A": rmsd, "aligned_residues": 187}


def structural_context(candidate, state, sequence):
    input_path = candidate.get("rf3_input_paths", {}).get(state)
    output_dir = candidate.get("rf3_output_dirs", {}).get(state)
    name = json.loads(Path(input_path).read_text())["name"] if input_path and Path(input_path).exists() else None
    rows = []
    for slot in assigned_samples(output_dir, name):
        paths = slot.pop("matches")
        slot["observed_files"] = [str(p) for p in paths]
        try:
            require(len(paths) == 1, "Assigned sample missing or ambiguous")
            slot.update(scaffold_agreement(paths[0], candidate["scaffold_path"], sequence))
            base = str(paths[0]).removesuffix(".gz").removesuffix("_model.cif")
            slot["confidence_files"] = [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for suffix in ("summary_confidences", "confidences")
                for p in [Path(f"{base}_{suffix}.json")] if p.exists()]
            slot["status"] = "measured"
        except Exception as exc:
            slot.update(status="missing_or_unresolved", error=f"{type(exc).__name__}: {exc}")
        rows.append(slot)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--decision", required=True, type=Path)
    ap.add_argument("--source-pdb", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text())
    candidates = manifest if isinstance(manifest, list) else manifest["candidates"]
    plan = json.loads(args.decision.read_text())
    require(len(plan["assignments"]) == 8, "Expected eight prospectively assigned candidates")
    candidate_ids = [c["id"] for c in candidates]
    require(len(candidate_ids) == len(set(candidate_ids)), "Duplicate candidate entries")
    require(set(candidate_ids) <= {a["id"] for a in plan["assignments"]}, "Unassigned candidates")
    anchors, source_water = reference(args.source_pdb)
    results = []
    for assignment in plan["assignments"]:
        candidate = next((c for c in candidates if c["id"] == assignment["id"]), {})
        row = {k: assignment[k] for k in ("id", "arm", "rfd3_seed")}
        row.update({k: candidate.get(k) for k in ("status", "enzyme_sha256")})
        output = candidate.get("rf3_output_dirs", {}).get("ES")
        sequence = candidate.get("enzyme_sequence", "")
        input_path = candidate.get("rf3_input_paths", {}).get("ES")
        example_id = None
        if sequence and input_path and Path(input_path).exists():
            spec = json.loads(Path(input_path).read_text())
            require(hashlib.sha256(sequence.encode()).hexdigest() == candidate["enzyme_sha256"], "Sequence hash mismatch")
            require(spec["components"] == [{"seq": sequence, "chain_id": "A"},
                    {"seq": PEPTIDE, "chain_id": "B"}, {"smiles": "[Zn+2].O", "chain_id": "C"}],
                    "Unconditioned ES input changed")
            example_id = spec["name"]
        rows = []
        for slot in assigned_samples(output, example_id):
            paths = slot.pop("matches")
            slot["observed_files"] = [str(path) for path in paths]
            if len(paths) == 1 and sequence:
                slot.update(observe(paths[0], sequence, anchors, source_water))
            else:
                slot["status"] = "missing_output" if not paths else "ambiguous_multiple_outputs"
            rows.append(slot)
        errors = [r["source_water_recovery_error_A"] for r in rows if r["status"] == "measured"]
        row.update(assigned_ES=5, outputs=rows, observed_ES=len(errors),
                   complete=(len(errors) == 5),
                   observed_median_error_A=statistics.median(errors) if errors else None)
        row["structural_context"] = {state: structural_context(candidate, state, sequence) for state in ("monomer", "ES")}
        results.append(row)
    pairs = []
    for seed in range(4):
        fixed = [r for r in results if r["rfd3_seed"] == seed and r["arm"] == "water_fixed"]
        free = [r for r in results if r["rfd3_seed"] == seed and r["arm"] == "water_coordinate_free"]
        complete = len(fixed) == len(free) == 1 and fixed[0]["complete"] and free[0]["complete"]
        pairs.append({"seed": seed, "complete": complete, "fixed_minus_free_A":
                      fixed[0]["observed_median_error_A"]-free[0]["observed_median_error_A"] if complete else None})
    complete = len(results) == 8 and all(p["complete"] for p in pairs)
    decision = "incomplete_comparison"
    if complete:
        signs = [p["fixed_minus_free_A"] for p in pairs]
        decision = ("consistent_fixed_water_recovery_benefit" if max(signs) < 0 else
                    "consistent_free_water_recovery_benefit" if min(signs) > 0 else "no_consistent_advantage")
    report = {"assigned_candidates": 8, "assigned_ES_outputs": 40, "assigned_monomer_outputs": 40, "candidates": results,
              "paired_seed_results": pairs, "decision": decision,
              "claim_boundary": "Water-position recovery only; no catalysis, rate or Atlas efficacy claim."}
    with args.output.open("x") as handle:
        handle.write(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
