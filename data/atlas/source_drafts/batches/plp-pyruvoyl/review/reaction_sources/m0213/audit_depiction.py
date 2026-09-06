"""Reproduce a source-depiction diagnostic using RDKit 2025.03.3.

Optional analysis environment: python -m pip install rdkit==2025.3.3
This script never downloads data and is not an Atlas runtime dependency.
It parses each retained panel independently; atom IDs are panel-local locators,
not reaction atom maps. Computed stereochemistry does not establish the identity
or physiological relevance of a depicted species or a mechanism trajectory.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


SOURCE_PATH = "data/atlas/source_drafts/batches/plp-pyruvoyl/sources/M0213.json"
SOURCE_SHA256 = "375d66615ee7a38cb3adc817b39ae28308d554590c26c3b4bbb7d08f2a74728d"

REFERENCE_PINS = {'57972': {'sha256': '5ba0e73a3fc10496994273277032a8349759046bc7e50d3da10304bbf11e5a78', 'cip': 'S', 'formal_charge': 0}, '57416': {'sha256': '2d65c26df7cf47ddb07e3145ddd88601f43ce44889836e1ee3d50a02ab14f483', 'cip': 'R', 'formal_charge': 0}}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(repo_root: Path, references_root: Path) -> dict:
    from rdkit import Chem, rdBase

    if rdBase.rdkitVersion != "2025.03.3":
        raise ValueError("This diagnostic is pinned to RDKit 2025.03.3")
    source = repo_root / SOURCE_PATH
    if sha256(source) != SOURCE_SHA256:
        raise ValueError("The retained M0213 snapshot changed; repeat source review")
    snapshot = json.loads(source.read_text(encoding="utf-8"))
    panels = snapshot["step_schemes"]
    if [panel["step_id"] for panel in panels] != list(range(1, 8)):
        raise ValueError("Unexpected retained panel set")

    references = []
    for chebi_id in ("57972", "57416"):
        path = references_root / f"CHEBI_{chebi_id}.mol"
        pin = REFERENCE_PINS[chebi_id]
        if sha256(path) != pin["sha256"]:
            raise ValueError("Reference bytes changed; repeat source review")
        mol = Chem.MolFromMolFile(
            str(path), sanitize=True, removeHs=False, strictParsing=True,
        )
        if mol is None:
            raise ValueError(f"Cannot parse reference {path.name}")
        centers = Chem.FindMolChiralCenters(
            mol, includeUnassigned=True, useLegacyImplementation=False,
        )
        if len(centers) != 1:
            raise ValueError("Reference does not have exactly one assigned stereocenter")
        if centers[0][1] != pin["cip"] or Chem.GetFormalCharge(mol) != pin["formal_charge"]:
            raise ValueError("Reference stereochemistry or charge differs from reviewed expectation")
        references.append({
            "source_file": path.name,
            "source_sha256": sha256(path),
            "source_chebi_id": f"CHEBI:{chebi_id}",
            "computed_cip": centers[0][1],
            "computed_formal_charge": Chem.GetFormalCharge(mol),
            "computed_smiles": Chem.MolToSmiles(mol),
        })

    rows = []
    for panel in panels:
        block = panel["content_utf8"]
        if hashlib.sha256(block.encode("utf-8")).hexdigest() != panel["content_sha256"]:
            raise ValueError("Source panel content hash differs")
        mol = Chem.MolFromMrvBlock(block, sanitize=True, removeHs=False)
        if mol is None:
            raise ValueError(f"Cannot parse panel {panel['step_id']}")
        xml = ET.fromstring(block)
        atoms = [item for item in xml.iter() if item.tag.rsplit("}", 1)[-1] == "atom"]
        if len(atoms) != mol.GetNumAtoms():
            raise ValueError("Parser/source atom counts differ")
        # Verify the local parser index against the original atom's element and
        # coordinates. No index is used to connect atoms across panels.
        source_atom = next(item for item in atoms if item.get("id") == "a17")
        index = atoms.index(source_atom)
        atom = mol.GetAtomWithIdx(index)
        position = mol.GetConformer().GetAtomPosition(index)
        if (atom.GetSymbol() != source_atom.get("elementType")
                or abs(position.x - float(source_atom.get("x2"))) > 1e-6
                or abs(position.y - float(source_atom.get("y2"))) > 1e-6):
            raise ValueError("Local source atom locator does not match parsed atom")
        centers = dict(Chem.FindMolChiralCenters(
            mol, includeUnassigned=True, useLegacyImplementation=False,
        ))
        row = {
            "step_id": panel["step_id"],
            "is_product": panel["is_product"],
            "scheme_sha256": panel["content_sha256"],
            "source_atom_id": "a17",
            "parser_atom_index": index,
            "computed_cip": centers.get(index),
            "computed_atom_formal_charge": atom.GetFormalCharge(),
        }
        if panel["step_id"] in (1, 7):
            fragments = [fragment for fragment in Chem.GetMolFrags(
                mol, asMols=True, sanitizeFrags=True,
            ) if Counter(a.GetSymbol() for a in fragment.GetAtoms()
                         if a.GetAtomicNum() != 1) == {"C": 3, "N": 1, "O": 2}]
            if len(fragments) != 1:
                raise ValueError("Endpoint free-fragment selection is ambiguous")
            fragment = fragments[0]
            fragment_centers = Chem.FindMolChiralCenters(
                fragment, includeUnassigned=True, useLegacyImplementation=False,
            )
            if len(fragment_centers) != 1 or fragment_centers[0][1] != centers[index]:
                raise ValueError("Endpoint fragment and source-located stereocenter differ")
            row.update({
                "computed_endpoint_smiles": Chem.MolToSmiles(Chem.RemoveHs(fragment)),
                "computed_endpoint_formal_charge": Chem.GetFormalCharge(fragment),
            })
        rows.append(row)
    return {
        "schema_version": "catalytic-earth.m0213-depiction-diagnostic.v1",
        "method": "independent_panel_MolFromMrvBlock_and_FindMolChiralCenters",
        "method_parameters": {"sanitize": True, "removeHs": False,
                              "includeUnassigned": True, "useLegacyImplementation": False},
        "rdkit_version": rdBase.rdkitVersion,
        "script_sha256": sha256(Path(__file__)),
        "source_snapshot_sha256": SOURCE_SHA256,
        "references": references,
        "panels": rows,
        "interpretation_scope": "computed_source_depiction_consistency_only",
        "exact_chebi_species_assigned": False,
        "reaction_atom_mapping_established": False,
        "intermediate_trajectory_status": "not_asserted",
        "limits": [
            "The source endpoint fragments and curated zwitterions have different charges.",
            "Panel 3 has an explicit alpha hydrogen and a different readout from panels 1 and 2.",
            "The panel readouts do not establish a coherent reverse mechanism or physical trajectory.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--references-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(audit(args.repo_root, args.references_root), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
