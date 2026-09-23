#!/usr/bin/env python3
"""Recompute the packing diagnosis from the unchanged, tracked RA95 archive."""
import hashlib
import json
import math
from pathlib import Path
import tarfile

BUNDLE = Path(__file__).resolve().parents[1] / "20260923-sequence-fold/continuation-bundle.tgz"
BUNDLE_SHA = "3ccf8b5f7ea3673fffc8058bf49f119c0f059588682fe5e49499e4138482f097"
MOTIF = {24: ["OD1", "CG", "ND2"], 78: ["NZ", "CE"],
         112: ["OH", "CZ"], 118: ["OH", "CZ"]}
CHI_PATHS = {24: ["N", "CA", "CB", "CG", "OD1"],
             78: ["N", "CA", "CB", "CG", "CD", "CE", "NZ"],
             112: ["N", "CA", "CB", "CG", "CD1"],
             118: ["N", "CA", "CB", "CG", "CD1"]}


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def angle(a, b, c):
    u, v = sub(a, b), sub(c, b)
    return math.degrees(math.acos(max(-1, min(1, dot(u, v) / (norm(u)*norm(v))))))


def dihedral(p0, p1, p2, p3):
    b0, b1, b2 = sub(p0, p1), sub(p2, p1), sub(p3, p2)
    axis = tuple(x / norm(b1) for x in b1)
    v = tuple(x - dot(b0, axis)*y for x, y in zip(b0, axis))
    w = tuple(x - dot(b2, axis)*y for x, y in zip(b2, axis))
    return math.degrees(math.atan2(dot(cross(axis, v), w), dot(v, w)))


def parse(data):
    atoms, serials, bonds, conect_count = {}, {}, [], 0
    for line in data.decode("ascii").splitlines():
        if line[:6].strip() in {"ATOM", "HETATM"}:
            key = (line[21], int(line[22:26]), line[12:16].strip())
            if key in atoms or line[16] != " " or line[26] != " ":
                raise ValueError(f"unexpected duplicate, alternate or insertion: {key}")
            xyz = tuple(float(line[i:i+8]) for i in (30, 38, 46))
            if not all(math.isfinite(x) for x in xyz):
                raise ValueError(f"nonfinite coordinate: {key}")
            atoms[key] = xyz
            serials[int(line[6:11])] = line[:6].strip()
        elif line.startswith("CONECT"):
            conect_count += 1
            ids = [int(line[i:i+5]) for i in range(6, len(line), 5) if line[i:i+5].strip()]
            bonds.extend((ids[0], other) for other in ids[1:])
    cross_count = sum({serials[a], serials[b]} == {"ATOM", "HETATM"} for a, b in bonds)
    return atoms, {"records": conect_count, "protein_ligand_directed_pairs": cross_count}


def main():
    if hashlib.sha256(BUNDLE.read_bytes()).hexdigest() != BUNDLE_SHA:
        raise ValueError("preserved continuation archive hash differs")
    members = {"reference": "output/reference.pdb",
               "packed": "output/ligmpnn/packed/reference_packed_1_1.pdb"}
    with tarfile.open(BUNDLE) as archive:
        raw = {name: archive.extractfile(path).read() for name, path in members.items()}
    before, before_bonds = parse(raw["reference"])
    after, after_bonds = parse(raw["packed"])
    shifts = {f"A{pos}:{atom}": norm(sub(before[("A", pos, atom)], after[("A", pos, atom)]))
              for pos, names in MOTIF.items() for atom in names}
    chi_delta, angles = {}, {}
    for pos, names in CHI_PATHS.items():
        for i in range(len(names) - 3):
            chis = [dihedral(*(state[("A", pos, atom)] for atom in names[i:i+4]))
                    for state in (before, after)]
            chi_delta[f"A{pos}:chi{i+1}"] = (chis[1] - chis[0] + 180) % 360 - 180
    for pos in (112, 118):
        for names in (("N", "CA", "CB"), ("CA", "CB", "CG")):
            angles[f"A{pos}:{'-'.join(names)}"] = {
                label: angle(*(state[("A", pos, atom)] for atom in names))
                for label, state in (("reference", before), ("packed", after))}
    ca_keys = [("A", i, "CA") for i in range(1, 151)]
    ligand_keys = [key for key in before if key[0] == "B"]
    assert len(ligand_keys) == 17
    output = {
        "scope": "Post hoc coordinates from preserved outputs; no new or corrected model run",
        "bundle_sha256": BUNDLE_SHA,
        "members": {k: {"path": members[k], "sha256": hashlib.sha256(v).hexdigest()}
                    for k, v in raw.items()},
        "ca_count": len(ca_keys),
        "ca_coordinates_exactly_unchanged": all(before[k] == after[k] for k in ca_keys),
        "ligand_heavy_atom_count": len(ligand_keys),
        "ligand_coordinates_exactly_unchanged": all(before[k] == after[k] for k in ligand_keys),
        "motif_rms_displacement_angstrom": math.sqrt(sum(x*x for x in shifts.values()) / len(shifts)),
        "motif_atom_displacement_angstrom": shifts,
        "chi_packed_minus_reference_degrees": chi_delta,
        "tyrosine_angles_degrees": angles,
        "lys78_NZ_to_LLK_C13_angstrom": {
            label: norm(sub(state[("A", 78, "NZ")], state[("B", 376, "C13")]))
            for label, state in (("reference", before), ("packed", after))},
        "conect": {"reference": before_bonds, "packed": after_bonds},
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
