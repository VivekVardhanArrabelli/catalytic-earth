#!/usr/bin/env python3
"""Exercise the OpenBabel calls delegated by pinned RFdiffusion2 ligand loading.

Requires the separately installed openbabel-wheel. This does not import the
RFdiffusion2 pipeline, create feature tensors, or infer a bound microstate.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from openbabel import openbabel as ob


def inspect(result_dir):
    receipt = json.loads((result_dir / "receipt.json").read_text())
    interface = json.loads((result_dir / "interface.json").read_text())
    raw = (result_dir / "assembly.pdb").read_bytes()
    ligand = interface["inference"]["ligand"]
    # Same filtering as rf_diffusion.parsers.load_ligand_from_pdb at the pin.
    stream = [l for l in raw.decode().splitlines(True)
              if (("HETATM" in l) and l[17:20].strip() == ligand) or "CONECT" in l]
    # Same no-conformer, string=True, remove_H=True OpenBabel operations as
    # rf2aa.data.parsers.parse_mol. No chemistry repair is performed.
    conversion = ob.OBConversion()
    conversion.SetInFormat("pdb")
    mol = ob.OBMol()
    ok = conversion.ReadString(mol, "".join(stream))
    mol.DeleteHydrogens()
    i = 1
    while i < mol.NumAtoms() + 1:
        if mol.GetAtom(i).GetAtomicNum() == 1:
            mol.DeleteAtom(mol.GetAtom(i))
        else:
            i += 1
    source = [a for a in receipt["atoms"] if a["selection_role"] == "ligand"]
    if not ok or len(source) != mol.NumAtoms():
        raise ValueError("ligand parse or atom count differs")
    names = [a["author_atom_id"] for a in source]
    correspondence = []
    for i, atom in enumerate(source, 1):
        parsed = mol.GetAtom(i)
        name = parsed.GetResidue().GetAtomID(parsed).strip()
        xyz = [parsed.x(), parsed.y(), parsed.z()]
        if name != atom["author_atom_id"] or ob.GetSymbol(parsed.GetAtomicNum()) != atom["element"]:
            raise ValueError("ligand atom name/element correspondence lost")
        if any(abs(x - y) > 0.0005001 for x, y in zip(xyz, atom["transformed_xyz"])):
            raise ValueError("ligand coordinates changed")
        correspondence.append({"source_atom": atom["author_atom_id"], "ob_name": name,
                               "element_number": parsed.GetAtomicNum(),
                               "formal_charge": parsed.GetFormalCharge(), "xyz": xyz})
    bonds = []
    for bond in ob.OBMolBondIter(mol):
        i, j = bond.GetBeginAtomIdx() - 1, bond.GetEndAtomIdx() - 1
        bonds.append({"names": sorted([names[i], names[j]]),
                      "order": bond.GetBondOrder(), "aromatic": bond.IsAromatic()})
    expected = {tuple(sorted((b["atom_id_1"], b["atom_id_2"]))):
                ({"sing": 1, "doub": 2, "trip": 3}[b["value_order"]], b["pdbx_aromatic_flag"] == "Y")
                for b in receipt["ligand_dictionary_heavy_bonds"]}
    actual = {tuple(b["names"]): (b["order"], b["aromatic"]) for b in bonds}
    # get_bond_feats at the pin uses GetBondOrder() unless IsAromatic(), then 4.
    # Comparing both values catches a model-feature change hidden by equal counts.
    differences = [{"edge": list(k), "expected": list(expected.get(k, ())),
                    "actual": list(actual.get(k, ()))}
                   for k in sorted(set(actual) | set(expected)) if actual.get(k) != expected.get(k)]
    return {"openbabel_release": ob.OBReleaseVersion(), "pdb_sha256": hashlib.sha256(raw).hexdigest(),
            "read_ok": ok, "atoms": mol.NumAtoms(), "bonds": mol.NumBonds(),
            "orders": dict(Counter(b["order"] for b in bonds)),
            "aromatic_edges": sum(b["aromatic"] for b in bonds), "differences": differences,
            "atom_correspondence": correspondence, "bonds_actual": bonds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-dir", type=Path, default=Path(__file__).with_name("6ha3"))
    parser.add_argument("--expected", type=Path,
                        help="Check reproduction of a retained result, which may be a chemical incompatibility")
    args = parser.parse_args()
    result = inspect(args.result_dir)
    if args.expected:
        # Normalize integer histogram keys through JSON before comparison.
        if json.loads(json.dumps(result)) != json.loads(args.expected.read_text()):
            raise ValueError("consumer result differs from retained observation")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
