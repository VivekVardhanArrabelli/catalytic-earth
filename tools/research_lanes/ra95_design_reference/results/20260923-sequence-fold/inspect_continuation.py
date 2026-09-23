#!/usr/bin/env python3
"""One-off, descriptive audit of the bounded RA95 sequence/fold continuation."""
import argparse, hashlib, itertools, json, re
from pathlib import Path
import numpy as np

AA3 = {a: b for a, b in zip(
    "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
    "ARNDCQEGHILKMFPSTWYV")}
EXPECTED_REF_SHA = "a08e12068a43923f0abd18de8f91c8a68f5b165cf63a36074675f6b597b0e84c"
EXPECTED = {24: "N", 78: "K", 112: "Y", 118: "Y"}
MOTIF = [(112, "OH"), (112, "CZ"), (78, "NZ"), (78, "CE"),
         (24, "OD1"), (24, "CG"), (24, "ND2"), (118, "OH"), (118, "CZ")]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path and path.is_file() else None

def read_fasta(path):
    records, header, seq = [], None, []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(seq)))
            header, seq = line[1:], []
        elif header is None:
            raise ValueError("sequence before FASTA header")
        else:
            seq.append(line.replace("/", ""))
    if header is not None:
        records.append((header, "".join(seq)))
    return records

def read_pdb(path):
    residues, by_key, duplicates, parse_errors = [], {}, [], []
    for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if line[:6] != "ATOM  " or len(line) < 54 or line[16:17] not in ("", " ", "A"):
            continue
        try:
            key = (line[21:22].strip() or "_", int(line[22:26]), line[26:27].strip())
            name, resname = line[12:16].strip(), line[17:20].strip()
            xyz = np.array([float(line[a:b]) for a, b in ((30, 38), (38, 46), (46, 54))])
        except Exception as exc:
            parse_errors.append({"line": number, "error": str(exc)})
            continue
        if key not in by_key:
            by_key[key] = {"key": key, "resname": resname, "atoms": {}}
            residues.append(by_key[key])
        if name in by_key[key]["atoms"]:
            duplicates.append(f"{key}:{name}")
        else:
            by_key[key]["atoms"][name] = xyz
    return residues, duplicates, parse_errors

def structure_summary(path):
    residues, duplicates, errors = read_pdb(path)
    seq = "".join(AA3.get(r["resname"], "X") for r in residues)
    missing_bb = [f"{i}:{atom}" for i, r in enumerate(residues, 1)
                  for atom in ("N", "CA", "C", "O") if atom not in r["atoms"]]
    bad = [f"{i}:{atom}" for i, r in enumerate(residues, 1)
           for atom, xyz in r["atoms"].items() if not np.isfinite(xyz).all()]
    return residues, {"path": str(path), "sha256": sha(path), "residue_count": len(residues),
        "chains": sorted({r["key"][0] for r in residues}), "sequence": seq,
        "sequence_sha256": hashlib.sha256(seq.encode()).hexdigest(),
        "length_150": len(residues) == 150, "complete_backbone": not missing_bb,
        "missing_backbone_atoms": missing_bb,
        "all_coordinates_finite": not bad, "nonfinite_atoms": bad,
        "duplicate_atoms": duplicates, "parse_errors": errors}

def fixed_check(seq):
    return {str(pos): {"expected": aa, "observed": seq[pos - 1] if len(seq) >= pos else None,
                       "matches": len(seq) >= pos and seq[pos - 1] == aa}
            for pos, aa in EXPECTED.items()}

def motif_xyz(residues):
    values, missing = [], []
    for pos, atom in MOTIF:
        xyz = residues[pos - 1]["atoms"].get(atom) if len(residues) >= pos else None
        if xyz is None or not np.isfinite(xyz).all():
            missing.append(f"A{pos}:{atom}")
            xyz = None
        values.append(xyz)
    return values, missing

def align(mobile, target):
    x, y = mobile - mobile.mean(0), target - target.mean(0)
    u, _, vt = np.linalg.svd(x.T @ y)
    d = np.eye(3); d[-1, -1] = np.linalg.det(u @ vt)
    rot = u @ d @ vt
    shift = target.mean(0) - mobile.mean(0) @ rot
    fitted = mobile @ rot + shift
    return rot, shift, float(np.sqrt(np.mean(np.sum((fitted - target) ** 2, axis=1))))

def pair_differences(motif, reference_motif):
    pairs = []
    for i, j in itertools.combinations(range(9), 2):
        rd = float(np.linalg.norm(reference_motif[i] - reference_motif[j]))
        md = None if motif[i] is None or motif[j] is None else float(np.linalg.norm(motif[i] - motif[j]))
        pairs.append({"atoms": [f"A{MOTIF[i][0]}:{MOTIF[i][1]}", f"A{MOTIF[j][0]}:{MOTIF[j][1]}"],
                      "reference_angstrom": rd, "model_angstrom": md,
                      "model_minus_reference_angstrom": None if md is None else md - rd})
    return pairs

def one_model(index, pdb, cif, score, reference_ca, reference_motif, sequence):
    out = {"model_index": index, "pdb_candidates": [str(x) for x in pdb],
           "cif_candidates": [str(x) for x in cif], "score_candidates": [str(x) for x in score]}
    out["cif"] = ({"path": str(cif[0]), "sha256": sha(cif[0]), "bytes": cif[0].stat().st_size}
                  if len(cif) == 1 else None)
    if len(score) == 1:
        try:
            payload, error = json.loads(score[0].read_text(), parse_constant=lambda x: x), None
        except Exception as exc:
            payload, error = None, str(exc)
        out["score_as_supplied"] = {"path": str(score[0]), "sha256": sha(score[0]),
                                     "payload": payload, "parse_error": error}
    else:
        out["score_as_supplied"] = None
    if len(pdb) != 1:
        out["structure"] = None
        out["missing_motif_atoms"] = [f"A{pos}:{atom}" for pos, atom in MOTIF]
        out["global_ca_rmsd_angstrom"] = None
        out["motif_rmsd_after_global_alignment_angstrom"] = None
        out["motif_pair_distance_differences"] = pair_differences([None] * 9, reference_motif)
        return out
    residues, summary = structure_summary(pdb[0]); out["structure"] = summary
    summary["sequence_matches_mpnn"] = summary["sequence"] == sequence
    summary["fixed_positions"] = fixed_check(summary["sequence"])
    model_ca = [r["atoms"].get("CA") for r in residues]
    motif, missing = motif_xyz(residues)
    out["missing_motif_atoms"] = missing
    out["global_ca_rmsd_angstrom"] = None
    out["motif_rmsd_after_global_alignment_angstrom"] = None
    if len(model_ca) == 150 and all(x is not None and np.isfinite(x).all() for x in model_ca):
        rot, shift, out["global_ca_rmsd_angstrom"] = align(np.array(model_ca), reference_ca)
        if not missing:
            fitted = np.array(motif) @ rot + shift
            out["motif_rmsd_after_global_alignment_angstrom"] = float(
                np.sqrt(np.mean(np.sum((fitted - reference_motif) ** 2, axis=1))))
    out["motif_pair_distance_differences"] = pair_differences(motif, reference_motif)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", required=True, type=Path); ap.add_argument("--mpnn-fasta", required=True, type=Path)
    ap.add_argument("--packed-pdb", required=True, type=Path); ap.add_argument("--chai-dir", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path); args = ap.parse_args()
    records = read_fasta(args.mpnn_fasta)
    generated = [(h, s) for h, s in records if re.search(r"(?:^|,\s*)id=1(?:,|$)", h)]
    sequence = generated[0][1] if len(generated) == 1 else ""
    ref_res, ref_summary = structure_summary(args.reference); ref_ca = np.array([r["atoms"]["CA"] for r in ref_res])
    ref_motif_list, ref_missing = motif_xyz(ref_res)
    if len(ref_res) != 150 or ref_missing or ref_ca.shape != (150, 3):
        raise ValueError(f"reference is not the expected complete 150-residue scaffold: {ref_missing}")
    packed_res, packed_summary = structure_summary(args.packed_pdb)
    packed_summary["sequence_matches_generated"] = packed_summary["sequence"] == sequence
    packed_summary["fixed_positions"] = fixed_check(packed_summary["sequence"])
    packed_motif, packed_missing = motif_xyz(packed_res)
    packed_summary["missing_motif_atoms"] = packed_missing
    packed_summary["global_ca_rmsd_angstrom"] = None
    packed_summary["motif_rmsd_after_global_alignment_angstrom"] = None
    if len(packed_res) == 150 and all("CA" in r["atoms"] for r in packed_res):
        rot, shift, rms = align(np.array([r["atoms"]["CA"] for r in packed_res]), ref_ca)
        packed_summary["global_ca_rmsd_angstrom"] = rms
        if not packed_missing:
            fitted = np.array(packed_motif) @ rot + shift
            packed_summary["motif_rmsd_after_global_alignment_angstrom"] = float(
                np.sqrt(np.mean(np.sum((fitted - np.array(ref_motif_list)) ** 2, axis=1))))
    packed_summary["motif_pair_distance_differences"] = pair_differences(packed_motif, np.array(ref_motif_list))
    result = {"scope": "Descriptive consumer-compatibility audit; no activity or Atlas-efficacy claim",
      "reference": ref_summary, "reference_sha256_expected": EXPECTED_REF_SHA,
      "reference_sha256_matches_expected": ref_summary["sha256"] == EXPECTED_REF_SHA,
      "mpnn_fasta": {"path": str(args.mpnn_fasta), "sha256": sha(args.mpnn_fasta), "record_count": len(records),
          "generated_id_1_count": len(generated), "generated_header": generated[0][0] if len(generated) == 1 else None,
          "sequence": sequence or None, "sequence_sha256": hashlib.sha256(sequence.encode()).hexdigest() if sequence else None,
          "length_150": len(sequence) == 150, "canonical_amino_acids": bool(sequence) and set(sequence) <= set(AA3.values()),
          "fixed_positions": fixed_check(sequence)},
      "packed_pdb": packed_summary, "expected_model_indices": list(range(5)), "models": []}
    for i in range(5):
        result["models"].append(one_model(i, list(args.chai_dir.glob(f"pred.*_model_idx_{i}.pdb")),
          list(args.chai_dir.glob(f"pred.*_model_idx_{i}.cif")), list(args.chai_dir.glob(f"scores.*_model_idx_{i}.json")),
          ref_ca, np.array(ref_motif_list), sequence))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
