#!/usr/bin/env python3
"""Measure the 20 assigned TDPn3 RF3 window outputs; never run predictions.

Requires the real Biotite installation used with RF3. The decision JSON and
its two immutable input JSONs are required inputs, not generated substitutes.
"""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import statistics

AA = dict(zip("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
              "ARNDCQEGHILKMFPSTWYV"))
ENZYME_SHA = "b5a77431300a76ff417cab0e36e3d1839cb8c191917d81256220b5cca2061165"
INPUT_SHA = {10: "626d3f2600929c55004260ba235d26f3a94c693a2ef1502f96c2eeddb11e65c7",
             12: "5afdbf256678f327b756a51fab8b709c1fa08d2b1b71f7759c5c5d768fe7cdd9"}
THRESHOLD = 3.2  # Strict source filter, not a new catalytic threshold.


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(), parse_constant=lambda x: {"nonfinite_source_constant": x})


def require(test, message):
    if not test:
        raise ValueError(message)


def distance(a, b):
    return math.dist(a, b)


def angle(a, b, c):
    x = [u - v for u, v in zip(a, b)]
    y = [u - v for u, v in zip(c, b)]
    denominator = math.sqrt(sum(v*v for v in x) * sum(v*v for v in y))
    require(denominator > 0, "Zero-length angle vector")
    cosine = sum(u*v for u, v in zip(x, y)) / denominator
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def cif_atoms(path, state):
    # Use the native library, not an extracted/stub parser. Label fields avoid
    # nonunique author chain labels; explicit output identifiers are preserved.
    from biotite.structure.io import pdbx
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt") as handle:
        cif = pdbx.CIFFile.read(handle)
    site = cif.block["atom_site"]
    if "pdbx_PDB_model_num" in site:
        require(len(set(site["pdbx_PDB_model_num"].as_array(str))) == 1,
                "Assigned output contains more than one structural model")
    array = pdbx.get_structure(cif, model=1, use_author_fields=False, altloc="all")
    atoms = []
    for i in range(len(array)):
        coord = [float(v) for v in array.coord[i]]
        require(all(math.isfinite(v) for v in coord), "Nonfinite output coordinates")
        atoms.append({"model_state": state, "chain": str(array.chain_id[i]),
                      "residue_number": int(array.res_id[i]),
                      "insertion_code": str(array.ins_code[i]),
                      "residue_name": str(array.res_name[i]),
                      "atom_name": str(array.atom_name[i]),
                      "element": str(array.element[i]).upper(), "coordinates_angstrom": coord})
    return atoms


def atom_ref(atom):
    return {k: v for k, v in atom.items() if k != "coordinates_angstrom"}


def identify(atoms, enzyme, peptide):
    chains = {}
    for atom in atoms:
        key = (atom["residue_number"], atom["insertion_code"])
        residues = chains.setdefault(atom["chain"], {})
        residue = residues.setdefault(key, {"name": atom["residue_name"], "atoms": {}})
        require(residue["name"] == atom["residue_name"], "Mixed residue identity in output")
        require(atom["atom_name"] not in residue["atoms"], "Duplicate or alternate output atom")
        residue["atoms"][atom["atom_name"]] = atom
    selected = {}
    chain_map = {}
    for role, sequence in (("enzyme", enzyme), ("peptide", peptide)):
        candidates = []
        for chain, residues in chains.items():
            keys = sorted(residues)
            observed = "".join(AA.get(residues[k]["name"], "?") for k in keys)
            if observed == sequence:
                candidates.append((chain, [residues[k] for k in keys]))
        require(len(candidates) == 1, f"Expected exactly one output chain with exact {role} sequence")
        chain, residues = candidates[0]
        selected[role] = residues
        chain_map[role] = {"chain": chain, "sequence": sequence,
                           "residue_numbers": [[a["residue_number"], a["insertion_code"]]
                             for residue in residues for a in [next(iter(residue["atoms"].values()))]]}
    protein_chains = {v["chain"] for v in chain_map.values()}
    heavy = [a for a in atoms if a["chain"] not in protein_chains and a["element"] not in ("H", "D")]
    require(sorted(a["element"] for a in heavy) == ["O", "ZN"],
            "Output ligand does not contain exactly one Zn and one nonprotein water O")
    roles = {"Zn": next(a for a in heavy if a["element"] == "ZN"),
             "water_O": next(a for a in heavy if a["element"] == "O")}
    for position, expected, names in ((146, "HIS", ("NE2",)), (150, "HIS", ("NE2",)),
            (45, "GLU", ("OE1", "OE2")), (147, "GLU", ("OE1", "OE2")),
            (78, "TYR", ("OH", "CZ"))):
        residue = selected["enzyme"][position - 1]
        require(residue["name"] == expected, "Source-role residue identity changed")
        for name in names:
            roles[f"enzyme_{position}_{name}"] = residue["atoms"].get(name)
    for position, residue in enumerate(selected["peptide"], 1):
        roles[f"peptide_{position}_O"] = residue["atoms"].get("O")
        if position == 7:
            roles["peptide_7_C"] = residue["atoms"].get("C")
        if position == 8:
            roles["peptide_8_N"] = residue["atoms"].get("N")
    return roles, chain_map


def measurements(roles, peptide):
    metrics = []

    def add(key, atom_roles, operation=distance):
        atoms = [roles.get(r) for r in atom_roles]
        row = {"id": key, "atom_roles": atom_roles,
               "ordered_atoms": [atom_ref(a) if a else None for a in atoms],
               "unit": "degree" if operation is angle else "angstrom", "value": None}
        if any(a is None for a in atoms):
            row["status"] = "missing_atom"
        else:
            try:
                row["value"] = operation(*(a["coordinates_angstrom"] for a in atoms))
                row["status"] = "measured"
            except ValueError as exc:
                row["status"] = "undefined_geometry"
                row["error"] = str(exc)
        metrics.append(row)
        return row

    def add_minimum(key, component_ids):
        candidates = [next(m for m in metrics if m["id"] == c) for c in component_ids]
        row = {"id": key, "component_metrics": component_ids, "unit": "angstrom",
               "value": None, "ordered_atoms": [], "status": "missing_atom"}
        if all(m["value"] is not None for m in candidates):
            best = min(candidates, key=lambda m: m["value"])
            row.update(value=best["value"], ordered_atoms=best["ordered_atoms"],
                       selected_component=best["id"], status="measured")
        metrics.append(row)

    add("Zn_G7_O", ["Zn", "peptide_7_O"])
    add("Zn_H146_NE2", ["Zn", "enzyme_146_NE2"])
    add("Zn_H150_NE2", ["Zn", "enzyme_150_NE2"])
    for oxygen in ("OE1", "OE2"):
        add(f"Zn_E45_{oxygen}", ["Zn", f"enzyme_45_{oxygen}"])
        add(f"E147_{oxygen}_water_O", [f"enzyme_147_{oxygen}", "water_O"])
    add_minimum("Zn_E45_min", ["Zn_E45_OE1", "Zn_E45_OE2"])
    add_minimum("E147_water_min", ["E147_OE1_water_O", "E147_OE2_water_O"])
    add("Zn_water_O", ["Zn", "water_O"])
    add("water_O_G7_C", ["water_O", "peptide_7_C"])
    add("water_O_G7_C_G7_O", ["water_O", "peptide_7_C", "peptide_7_O"], angle)
    add("Y78_OH_G7_O", ["enzyme_78_OH", "peptide_7_O"])
    add("Y78_CZ_OH_G7_O", ["enzyme_78_CZ", "enzyme_78_OH", "peptide_7_O"], angle)
    add("G7_C_M8_N", ["peptide_7_C", "peptide_8_N"])
    register = []
    for position in range(1, len(peptide)):
        if position == 7:
            row = next(m for m in metrics if m["id"] == "Zn_G7_O")
        else:
            row = add(f"Zn_peptide_{position}_O", ["Zn", f"peptide_{position}_O"])
        register.append({"amide": f"{peptide[position-1]}{position}-{peptide[position]}{position+1}",
                         "carbonyl_position": position, "metric_id": row["id"], "distance_angstrom": row["value"]})
    target = next(r["distance_angstrom"] for r in register if r["carbonyl_position"] == 7)
    complete = all(r["distance_angstrom"] is not None for r in register)
    rank = 1 + sum(r["distance_angstrom"] < target for r in register) if complete else None
    return metrics, {"amide_carbonyls": register, "G7_rank": rank,
        "ranking_rule": "One plus the number of strictly shorter distances; exact ties share a rank.",
        "assigned_amide_carbonyls": len(peptide)-1,
        "scope": "Final terminal carbonyl excluded. Proximity and rank do not assign cleavage."}


def observe(path, output_root, enzyme, peptide):
    state = path.relative_to(output_root).as_posix()
    row = {"file": state, "sha256": digest(path)}
    base = str(path).removesuffix(".gz").removesuffix("_model.cif")
    confidence = {}
    for suffix in ("summary_confidences", "confidences"):
        confidence_path = Path(f"{base}_{suffix}.json")
        if confidence_path.exists():
            item = {"file": confidence_path.relative_to(output_root).as_posix(), "sha256": digest(confidence_path)}
            if suffix == "summary_confidences":
                try:
                    item["native_values"] = read_json(confidence_path)
                except Exception as exc:
                    item["read_error"] = f"{type(exc).__name__}: {exc}"
            confidence[suffix] = item
        else:
            confidence[suffix] = {"status": "missing"}
    row["confidence"] = confidence
    try:
        atoms = cif_atoms(path, state)
        roles, chain_map = identify(atoms, enzyme, peptide)
        metric_rows, register = measurements(roles, peptide)
        row.update(status="measured", atom_count=len(atoms), chain_map=chain_map,
                   identified_atoms={key: value for key, value in roles.items() if value is not None},
                   metrics=metric_rows, peptide_register=register,
                   all_required_geometry_present=all(m["value"] is not None for m in metric_rows))
        row["primary_distance_angstrom"] = metric_rows[0]["value"]
    except Exception as exc:
        row.update(status="unreadable_or_identity_unresolved", error=f"{type(exc).__name__}: {exc}",
                   all_required_geometry_present=False, primary_distance_angstrom=None)
    return row


def summarize(slots):
    groups = []
    for length in (10, 12):
        for seed in (0, 1):
            members = [s for s in slots if s["peptide_length"] == length and s["seed"] == seed]
            distances = [s.get("primary_distance_angstrom") for s in members]
            observed = [x for x in distances if x is not None]
            groups.append({"peptide_length": length, "seed": seed, "assigned": 5,
                "samples": [{"sample": s["sample"], "status": s["status"], "Zn_G7_O_angstrom": x}
                            for s, x in zip(members, distances)],
                "contact_count": sum(x < THRESHOLD for x in observed),
                "noncontact_count": sum(x >= THRESHOLD for x in observed), "missing_count": 5-len(observed),
                "observed_primary": len(observed), "median_angstrom": statistics.median(observed) if observed else None,
                "range_angstrom": [min(observed), max(observed)] if observed else None})
    by = {(g["peptide_length"], g["seed"]): g for g in groups}
    differences = []
    for seed in (0, 1):
        short, long = (by[(length, seed)] for length in (10, 12))
        a, b = short["median_angstrom"], long["median_angstrom"]
        differences.append({"seed": seed, "12mer_minus_10mer_median_angstrom": b-a if a is not None and b is not None else None,
                            "complete_primary_sets": short["observed_primary"] == long["observed_primary"] == 5})
    complete = all(s.get("all_required_geometry_present", False) for s in slots)
    classification = "incomplete_comparison"
    if complete:
        short = [by[(10, seed)]["contact_count"] for seed in (0, 1)]
        long = [by[(12, seed)]["contact_count"] for seed in (0, 1)]
        if min(short) >= 4 and max(long) <= 1:
            classification = "reproducible_loss"
        elif min(long) >= 4 and max(short) <= 1:
            classification = "reproducible_gain"
        elif min(short + long) >= 4:
            classification = "contact_retained"
        else:
            classification = "mixed_inconclusive_or_noninformative_baseline"
    return {"assigned_total": 20, "readable_identity_verified_outputs": sum(s["status"] == "measured" for s in slots),
            "all_required_geometry_complete": complete, "condition_seed_groups": groups,
            "seed_median_differences": differences, "contact_count_pattern": classification,
            "chemical_interpretation_status": "Requires joint inspection of all prespecified metal/site-water metrics; no new site/water cutoff is applied."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, required=True, help="Contains both seed-0 and seed-1 output directories")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--decision", type=Path, required=True, help="Authoritative tracked window_check decision JSON")
    parser.add_argument("--out-json", type=Path, required=True, help="Must not already exist")
    args = parser.parse_args()
    require(args.output_root.is_dir(), "Output root does not exist")
    require(not args.out_json.exists(), "Refusing to overwrite a previous measurement result")
    decision = read_json(args.decision)
    require("completeness_gate" in decision["decision"], "Use current decision record with complete-20 gate")
    require(decision["fixed_sampling"]["seeds"] == [0, 1] and decision["fixed_sampling"]["diffusion_batch_size"] == 5,
            "Unexpected assignment plan")
    conditions = []
    for condition in decision["conditions"]:
        path = args.input_dir / condition["input"]
        spec = read_json(path)
        peptide = condition["peptide"]
        require(digest(path) == condition["sha256"] == INPUT_SHA[len(peptide)], "Input hash changed")
        enzyme = spec["components"][0]["seq"]
        require(hashlib.sha256(enzyme.encode()).hexdigest() == ENZYME_SHA, "Enzyme sequence changed")
        require(spec["components"] == [{"seq": enzyme, "chain_id": "A"}, {"seq": peptide, "chain_id": "B"},
                                       {"smiles": "[Zn+2].O", "chain_id": "C"}], "Chemical input changed")
        conditions.append((spec["name"], enzyme, peptide))
    require(sorted(len(c[2]) for c in conditions) == [10, 12], "Both fixed windows are required")
    try:
        version = importlib.metadata.version("biotite")
    except importlib.metadata.PackageNotFoundError:
        version = None
    slots = []
    for name, enzyme, peptide in conditions:
        for seed in (0, 1):
            for sample in range(5):
                basename = f"{name}_seed-{seed}_sample-{sample}_model.cif"
                matches = sorted(set(args.output_root.rglob(basename)) | set(args.output_root.rglob(basename + ".gz")))
                slot = {"example_id": name, "peptide_length": len(peptide), "seed": seed, "sample": sample,
                        "observed_files": [p.relative_to(args.output_root).as_posix() for p in matches]}
                if len(matches) == 1:
                    slot.update(observe(matches[0], args.output_root, enzyme, peptide))
                else:
                    slot.update(status="missing_output" if not matches else "ambiguous_multiple_outputs",
                                primary_distance_angstrom=None, all_required_geometry_present=False)
                slots.append(slot)
    receipt_names = {"native_gate.json", "checkpoint_pin.json", "assignments_before_inference.json",
                     "assignments_after_inference.json", "all_20_prespecified_assignments.json"}
    receipts = [{"file": p.relative_to(args.output_root).as_posix(), "sha256": digest(p)}
                for p in sorted(args.output_root.rglob("*"))
                if p.is_file() and (p.name in receipt_names or p.name.endswith("_ranking_scores.csv"))]
    payload = {"question": decision["question"], "adapter_sha256": digest(__file__), "biotite_version": version,
        "decision": {"file": args.decision.name, "sha256": digest(args.decision), "rules": decision["decision"]},
        "input_sources": [{"file": c["input"], "sha256": c["sha256"]} for c in decision["conditions"]],
        "metric_scope": "Same distance/ordered heavy-atom angle definitions as the source-scoped author-model lane. Only the strict 3.2-A primary contact filter is thresholded; this is not a catalytic success rule.",
        "output_identity_scope": "CIF protein sequence and Zn/O elemental identity reidentified independently of array indices. Native input charge/connectivity gate remains separate; these coordinate measurements do not certify an output chemical graph.",
        "confidence_scope": "Native summary fields retained without AF3 cutoffs or scale conversion; full confidence files retained by path/hash.",
        "interpretation_limit": decision["interpretation_limit"],
        "chemical_interpretation_gate": decision["primary"]["chemical_interpretation_gate"],
        "native_execution_receipts": receipts,
        "summary": summarize(slots), "assignments": slots}
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    with args.out_json.open("x") as handle:
        json.dump(payload, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.out_json), "sha256": digest(args.out_json), "summary": payload["summary"]}, indent=2))


if __name__ == "__main__":
    main()
