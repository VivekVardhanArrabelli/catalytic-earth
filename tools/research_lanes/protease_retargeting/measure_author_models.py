"""Reproduce coordinate-derived TDPn3 measurements from immutable author files.

This is an offline scientific recipe, not a model execution or a validator of
catalysis. Distances are Euclidean; angles use the middle heavy atom as vertex.
Contact cutoffs enumerate candidates and are not energetic acceptance rules.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
MODEL_DIR = HERE / "models"
SEQUENCE = (
    "MSLSEIFDRLVEPTLRVPRLARTVDELVAAGYDRRDAARLVAAIEALAFAGVALVAPEAYREIAEAIRELDPTAYE"
    "VYVEGAEALLAAARAGDPVAQELLERARRLGEEALTNERGKELRERIEEIVDELETRASREAVIEAATIHEYLHAAL"
    "FDGEILALRVEGPWIVSEVAVPRERLDELLEKVK"
)
FILES = {
    "apo_monomer": ("TDPn3-author-monomer-seed-1-sample-0-filtered.pdb", "f7347af939dbca54c399c0e52a0e968e9516246428863187e508a5192a1cd16b"),
    "enzyme_substrate_Zn_water": ("TDPn3-author-complex-seed-1-sample-3-filtered.pdb", "a25ad433f43762e4fec54eb4cdb3043ea338131b3f1b9ea2a01748b13683341f"),
    "author_phosphoTS_analogue": ("TDPn3-author-phosphoTS-seed-1-sample-0-filtered.pdb", "168d84af0111f1ae1dffa1a29286ac6f32571c5c677bbe1ed4a218d63e994c6f"),
    "rejected_unfiltered_ES_sample0": ("TDPn3-author-complex-seed-1-sample-0-unfiltered.pdb", "4ad4fde6bfb4cb66cbf57b699d18107486beed0da470af04a6e9296c5c5ebac2"),
}
AA = dict(zip("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(), "ARNDCQEGHILKMFPSTWYV"))
ROLE_ATOMS = {
    "zn_ligand_histidine_1": [("A", 146, "NE2")],
    "zn_ligand_histidine_2": [("A", 150, "NE2")],
    "zn_ligand_glutamate": [("A", 45, "OE1"), ("A", 45, "OE2")],
    "general_base_glutamate": [("A", 147, "OE1"), ("A", 147, "OE2")],
    "oxyanion_stabilizing_tyrosine": [("A", 78, "CZ"), ("A", 78, "OH")],
    "zinc": [("C", 1, "ZN1")],
    "catalytic_water": [("C", 1, "O1")],
}


def read_pdb(path: Path, expected_sha256: str) -> dict:
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256:
        raise ValueError(f"Wrong immutable model bytes: {path.name}: {actual}")
    atoms = {}
    for line in payload.decode().splitlines():
        if line[:6] not in ("ATOM  ", "HETATM"):
            continue
        chain, resid, name = line[21], int(line[22:26]), line[12:16].strip()
        key = (chain, resid, name)
        if key in atoms or line[16].strip() or line[26].strip():
            raise ValueError(f"Ambiguous atom/residue naming: {path.name}: {line}")
        atoms[key] = {
            "atom_id": f"{chain}:{line[17:20].strip()}{resid}:{name}",
            "chain": chain,
            "residue_number": resid,
            "residue_name": line[17:20].strip(),
            "atom_name": name,
            "element": line[76:78].strip(),
            "coordinates_angstrom": [float(line[i:i+8]) for i in (30, 38, 46)],
            "occupancy": float(line[54:60]),
            "stored_b_factor_field": float(line[60:66]),
        }
    sequence = "".join(AA[a["residue_name"]] for key, a in atoms.items() if key[0] == "A" and key[2] == "CA")
    if sequence != SEQUENCE:
        raise ValueError(f"Table S4 designed-core sequence mismatch: {path.name}")
    return atoms


def distance(atoms, a, b):
    return math.dist(atoms[a]["coordinates_angstrom"], atoms[b]["coordinates_angstrom"])


def angle(atoms, a, b, c):
    points = [atoms[x]["coordinates_angstrom"] for x in (a, b, c)]
    u, v = ([points[j][i] - points[1][i] for i in range(3)] for j in (0, 2))
    cosine = sum(x*y for x, y in zip(u, v)) / (math.sqrt(sum(x*x for x in u)) * math.sqrt(sum(x*x for x in v)))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def atom_reference(atom, state=None):
    out = {key:atom[key] for key in ("chain","residue_number","residue_name","atom_name")}
    if state is not None:
        out["model_state"] = state
    return out


def metric(atoms, metric_id, atom_keys, unit, meaning):
    value = distance(atoms, *atom_keys) if len(atom_keys) == 2 else angle(atoms, *atom_keys)
    return {"id": metric_id, "ordered_atoms": [atom_reference(atoms[x]) for x in atom_keys], "value": value, "unit": unit, "meaning": meaning}


def catalytic_metrics(atoms, tsa=False):
    z, w = ("C", 1, "ZN1"), ("C", 1, "O1")
    c, o, n = (("B", 7, "P1"), ("B", 7, "O1"), ("B", 7, "N2")) if tsa else (("B", 7, "C"), ("B", 7, "O"), ("B", 8, "N"))
    rows = []
    for atom, name in [(("A",146,"NE2"),"His146_NE2"), (("A",150,"NE2"),"His150_NE2"), (("A",45,"OE1"),"Glu45_OE1"), (("A",45,"OE2"),"Glu45_OE2")]:
        rows.append(metric(atoms, f"zinc_{name}", [z,atom], "angstrom", "metal-to-protein-ligand distance"))
    rows += [
        metric(atoms, "zinc_target_oxygen", [z,o], "angstrom", "Zn to oxyanion-like TSA O1" if tsa else "Zn to P1 Gly7 carbonyl oxygen"),
        metric(atoms, "tyr_target_oxygen", [("A",78,"OH"),o], "angstrom", "candidate oxyanion-donor contact"),
        metric(atoms, "tyr_CZ_OH_target_oxygen", [("A",78,"CZ"),("A",78,"OH"),o], "degree", "heavy-atom donor angle, vertex Tyr OH; no hydrogen position is supplied"),
    ]
    for name in ("OE1","OE2"):
        rows.append(metric(atoms, f"base_{name}_leaving_nitrogen", [("A",147,name),n], "angstrom", "proposed acid-to-leaving-group contact; ES/TSA is not product-release state"))
        rows.append(metric(atoms, f"base_{name}_nucleophile_oxygen", [("A",147,name),("B",7,"O2") if tsa else w], "angstrom", "base-to-TSA O2" if tsa else "base-to-modeled-water oxygen"))
    if not tsa:
        rows += [
            metric(atoms, "scissile_C_N", [c,n], "angstrom", "intended substrate amide bond"),
            metric(atoms, "zinc_water", [z,w], "angstrom", "Zn to modeled catalytic water oxygen"),
            metric(atoms, "water_carbonyl_carbon", [w,c], "angstrom", "modeled nucleophile-to-electrophile separation"),
            metric(atoms, "water_C_O_attack_angle", [w,c,o], "degree", "water O-P1 carbonyl C-P1 carbonyl O, vertex C; a snapshot angle, not a transition state"),
        ]
    return rows


def contacts(atoms):
    """Residue-pair minima at 4 A, preserving backbone/sidechain and truncation."""
    substrate = [a for a in atoms.values() if a["chain"] == "B" and a["element"] != "H"]
    protein = [a for a in atoms.values() if a["chain"] == "A" and a["element"] != "H"]
    candidates, backbone = {}, []
    for s, p in itertools.product(substrate, protein):
        d = math.dist(s["coordinates_angstrom"], p["coordinates_angstrom"])
        category = "artificial_truncated_C_terminal_OXT" if s["atom_name"] == "OXT" else ("substrate_backbone" if s["atom_name"] in ("N","CA","C","O") else "substrate_sidechain")
        if d <= 4.0:
            key = (s["residue_number"], p["residue_number"], category)
            if key not in candidates or candidates[key]["distance_angstrom"] > d:
                candidates[key] = {"assay_peptide_position":s["residue_number"], "substrate_residue":s["residue_name"], "protein_residue":f"A:{p['residue_name']}{p['residue_number']}", "ordered_atoms":[atom_reference(s,"enzyme_substrate_Zn_water"),atom_reference(p,"enzyme_substrate_Zn_water")], "substrate_atom_class":category, "distance_angstrom":d, "excluded_from_full_12mer_by_terminal_atom_mismatch":category == "artificial_truncated_C_terminal_OXT"}
        if d <= 3.5 and (s["atom_name"],p["atom_name"]) in (("N","O"),("O","N")):
            backbone.append({"ordered_atoms":[atom_reference(s,"enzyme_substrate_Zn_water"),atom_reference(p,"enzyme_substrate_Zn_water")], "distance_angstrom":d, "interpretation":"candidate backbone hydrogen-bond pair; hydrogens absent, so no H-bond energy/occupancy claim"})
    return {"enumeration_cutoffs_angstrom":{"residue_pair_minimum_by_substrate_atom_class":4.0,"backbone_N_O_candidate":3.5}, "scope":"Selected ES sample3 only. Cutoffs are analyst enumeration choices, not causal or energetic thresholds. No assembly/symmetry expansion.", "residue_pair_contacts":sorted(candidates.values(), key=lambda x:(x["assay_peptide_position"],x["protein_residue"],x["substrate_atom_class"])), "backbone_register_contacts":backbone}


def compare_states(reference, mobile, mobile_state):
    """Fit all 187 protein C-alpha atoms, then report catalytic-atom displacement."""
    ca_keys = [("A",i,"CA") for i in range(1,188)]
    x = np.array([mobile[k]["coordinates_angstrom"] for k in ca_keys])
    y = np.array([reference[k]["coordinates_angstrom"] for k in ca_keys])
    xc,yc = x.mean(axis=0),y.mean(axis=0)
    u,_,vt = np.linalg.svd((x-xc).T @ (y-yc))
    correction = np.diag([1.,1.,np.linalg.det(u @ vt)])
    rot = u @ correction @ vt
    transformed = (x-xc) @ rot + yc
    atom_keys = [k for role,keys in ROLE_ATOMS.items() if role not in ("zinc","catalytic_water") for k in keys]
    displacement = []
    for k in atom_keys:
        xyz=(np.array(mobile[k]["coordinates_angstrom"])-xc) @ rot + yc
        displacement.append({"ordered_atoms":[atom_reference(reference[k],"enzyme_substrate_Zn_water"),atom_reference(mobile[k],mobile_state)],"displacement_angstrom":float(np.linalg.norm(xyz-np.array(reference[k]["coordinates_angstrom"])))})
    symmetric=[]
    for role,keys in ROLE_ATOMS.items():
        if role in ("zinc","catalytic_water"):
            continue
        assignments=[keys, keys[::-1]] if role in ("zn_ligand_glutamate","general_base_glutamate") else [keys]
        options=[]
        for assigned in assignments:
            rows=[]
            for ref_key,mobile_key in zip(keys,assigned):
                xyz=(np.array(mobile[mobile_key]["coordinates_angstrom"])-xc) @ rot + yc
                rows.append({"ordered_atoms":[atom_reference(reference[ref_key],"enzyme_substrate_Zn_water"),atom_reference(mobile[mobile_key],mobile_state)],"displacement_angstrom":float(np.linalg.norm(xyz-np.array(reference[ref_key]["coordinates_angstrom"])))})
            options.append(rows)
        symmetric.extend(min(options,key=lambda rows:sum(r["displacement_angstrom"]**2 for r in rows)))
    return {"alignment":"least-squares proper rotation of all 187 corresponding protein CA atoms; no local active-site refit", "fitted_atom_selection":{"reference_state":"enzyme_substrate_Zn_water","mobile_state":mobile_state,"chain":"A","residue_numbers":list(range(1,188)),"atom_name":"CA"}, "CA_RMSD_angstrom":float(np.sqrt(np.mean(np.sum((transformed-y)**2,axis=1)))), "same_atom_name_displacements_after_CA_fit":displacement, "same_atom_name_catalytic_RMSD_angstrom":math.sqrt(sum(d["displacement_angstrom"]**2 for d in displacement)/len(displacement)), "carboxylate_symmetry_aware_displacements_after_CA_fit":symmetric, "carboxylate_symmetry_aware_catalytic_RMSD_angstrom":math.sqrt(sum(d["displacement_angstrom"]**2 for d in symmetric)/len(symmetric)), "symmetry_rule":"After the unchanged CA fit, independently choose same or exchanged OE1/OE2 correspondence for each glutamate by minimum squared displacement. This compares carboxylate geometry without imposing equivalence on a specified protonated oxygen; protonation is absent from these models.", "scope":"coordinate consistency among author predictions, not a measured conformational distribution, binding cost, or evidence that the active geometry is occupied"}


def main():
    states = {state:read_pdb(MODEL_DIR/name,sha) for state,(name,sha) in FILES.items()}
    es = states["enzyme_substrate_Zn_water"]
    es_sequence = "".join(AA[a["residue_name"]] for (c,_,n),a in es.items() if c == "B" and n == "CA")
    assert es_sequence == "ALQSSWGMMG"
    out = {"evidence_level":"coordinate-derived measurements of author computational models", "precision":"PDB coordinates are stored to 0.001 angstrom; additional arithmetic digits are retained only for reproducibility and are not accuracy or an uncertainty estimate", "model_files":{s:{"file":f"models/{f}","path_basis":"relative_to_measurement_record","sha256":h} for s,(f,h) in FILES.items()}, "identity":{"designed_core_sequence":SEQUENCE,"core_residues":len(SEQUENCE),"ES_substrate_sequence":es_sequence,"ES_missing_assay_positions":[11,12],"assay_construct_scope":"Exact Table S4 designed core match, not identity to a full tagged experimental construct."}, "role_atoms":{role:{state:[atoms[k] for k in keys if k in atoms] for state,atoms in states.items()} for role,keys in ROLE_ATOMS.items()}, "metrics":{s:catalytic_metrics(atoms, s == "author_phosphoTS_analogue") for s,atoms in states.items() if s != "apo_monomer"}, "selected_ES_contacts":contacts(es), "state_comparisons":{s:compare_states(es,states[s],s) for s in ("apo_monomer","author_phosphoTS_analogue","rejected_unfiltered_ES_sample0")}}
    for state,rows in out["metrics"].items():
        for row in rows:
            for atom in row["ordered_atoms"]:
                atom["model_state"] = state
    destination=HERE/"model_measurements.json"
    destination.write_text(json.dumps(out,indent=2)+"\n")
    print(destination)
    print(f"{len(out['selected_ES_contacts']['residue_pair_contacts'])} residue-pair/contact-class minima; {len(out['selected_ES_contacts']['backbone_register_contacts'])} candidate backbone N/O pairs")


if __name__ == "__main__":
    main()
