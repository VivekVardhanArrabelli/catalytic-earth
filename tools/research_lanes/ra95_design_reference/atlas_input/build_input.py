#!/usr/bin/env python3
"""Rebuild RA95 coordinate fields from Atlas, retaining the author PDB template.

This case-specific translation does not infer an atom selection, joint alternate
state, ligand graph, protonation or catalytic geometry. No model is invoked.
"""

import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas_deposit_context import check_deposit_context

LANE = ROOT / "tools/research_lanes/ra95_design_reference"
PACKET = ROOT / "data/atlas/deposit_context/ra95_5an7"
BUNDLE = LANE / "results/20260923/run-bundle.tgz"
BUNDLE_SHA = "1bab79f7a2122ae6a1d44b164b60f65b5833920951b80006a2a3aaf0d68cfaf8"
TEMPLATE_MEMBER = "output/input/ra_5an7_no_cov_ORI_cm1.pdb"
# Explicit author-control choices, never highest occupancy or nearest distance.
GROUPS = {"tyr51-atoms": "A", "lys83-atoms": "A",
          "asn110-atoms": ".", "tyr180-atoms": "."}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def atom_key(row):
    return (row["group_pdb"], row["auth_asym_id"], row["auth_seq_id"],
            row["auth_comp_id"], row["auth_atom_id"],
            " " if row["label_alt_id"] == "." else row["label_alt_id"])


def rebuild(template, source_rows):
    """Replace selected XYZ/occupancy fields; never fall back to template values."""
    wanted = {}
    for row in source_rows:
        key = atom_key(row)
        if key in wanted:
            raise ValueError(f"ambiguous source atom: {key}")
        if row["pdbx_pdb_model_num"] != "1" or row["pdbx_pdb_ins_code"] != "?":
            raise ValueError("this case expects model 1 without insertion codes")
        wanted[key] = row
    seen = set()
    output = []
    provenance = []
    for line in template.decode("ascii").splitlines(keepends=True):
        if line[:6].strip() in {"ATOM", "HETATM"}:
            key = (line[:6].strip(), line[21], line[22:26].strip(),
                   line[17:20], line[12:16].strip(), line[16])
            if key in wanted:
                if key in seen:
                    raise ValueError(f"duplicate template atom: {key}")
                seen.add(key)
                row = wanted[key]
                if line[76:78].strip() != row["type_symbol"]:
                    raise ValueError(f"element mismatch: {key}")
                xyz = [float(row[f"cartn_{axis}"]) for axis in "xyz"]
                occupancy = float(row["occupancy"])
                if not all(math.isfinite(x) for x in xyz + [occupancy]):
                    raise ValueError(f"nonfinite source value: {key}")
                fields = "".join(f"{x:8.3f}" for x in xyz) + f"{occupancy:6.2f}"
                if len(fields) != 30:
                    raise ValueError(f"PDB field overflow: {key}")
                line = line[:30] + fields + line[60:]
                provenance.append({"atom_site_id": row["id"],
                                   "label_seq_id": row["label_seq_id"],
                                   "label_asym_id": row["label_asym_id"],
                                   "author_key": list(key),
                                   "template_serial": int(line[6:11]),
                                   "xyz_angstrom": xyz, "occupancy": occupancy})
        output.append(line)
    if seen != set(wanted):
        raise ValueError(f"source atoms absent from template: {sorted(set(wanted) - seen)}")
    return "".join(output).encode("ascii"), provenance


def select_rows(projection, interface):
    selections = {item["selection_id"]: item["rows"] for item in projection["row_selections"]}
    rows = []
    for group, alt in GROUPS.items():
        for row in selections[group]:
            selector = row["auth_asym_id"] + row["auth_seq_id"]
            if (row["auth_atom_id"] in interface["contig_atoms"].get(selector, [])
                    and row["label_alt_id"] == alt):
                rows.append(row)
    if len(rows) != 9:
        raise ValueError("expected exactly nine source-bound guidepost atoms")
    ligand = [row for row in selections["ligand-atoms"] if row["type_symbol"] != "H"]
    if len(ligand) != 17 or any(row["label_comp_id"] != "LLK" for row in ligand):
        raise ValueError("expected the seventeen LLK heavy atoms")
    if any(row["label_alt_id"] != "." or row["auth_seq_id"] != "5001" for row in ligand):
        raise ValueError("LLK instance differs from the author-control choice")
    return rows + ligand



def verify_interface(interface, config):
    actual_atoms = {key: value.split(",") for key, value in
                    ast.literal_eval(config["contigmap"]["contig_atoms"]).items()}
    checks = [config["contigmap"]["contigs"] == [",".join(interface["contigs"])],
              actual_atoms == interface["contig_atoms"],
              config["contigmap"]["length"] == interface["length"],
              config["inference"]["ligand"] == interface["ligand"],
              config["inference"]["contig_as_guidepost"] == interface["contig_as_guidepost"]]
    if not all(checks):
        raise ValueError("interface differs from the executed reference configuration")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Fresh directory for the generated PDB, interface and receipt")
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("output directory must be fresh")
    projection = check_deposit_context(PACKET, ROOT)
    audit = json.loads((LANE / "input_state.json").read_text())
    # This reads native interface choices, not the sidecar's native_atom_map.
    interface = audit["native_control"]["interface"]
    if sha(BUNDLE.read_bytes()) != BUNDLE_SHA:
        raise ValueError("frozen reference bundle changed")
    with tarfile.open(BUNDLE) as archive:
        template = archive.extractfile(TEMPLATE_MEMBER).read()
        config = json.load(archive.extractfile("logs/resolved-inference-config.json"))
    verify_interface(interface, config)
    if sha(template) != audit["native_control"]["input_pdb"]["sha256"]:
        raise ValueError("author template hash differs")
    rows = select_rows(projection, interface)
    output, provenance = rebuild(template, rows)
    receipt = {
        "scope": "Executed coordinate/occupancy translation on an exposed development case; author-template dependent",
        "atlas_source": projection["source_binding"],
        "deposit_projection_sha256": sha((PACKET / "projection.json").read_bytes()),
        "author_template": {"bundle_sha256": BUNDLE_SHA, "member": TEMPLATE_MEMBER,
                            "sha256": sha(template)},
        "author_interface_sidecar_sha256": sha((LANE / "input_state.json").read_bytes()),
        "output_sha256": sha(output),
        "output_bytes": len(output),
        "byte_equal_to_author_input": output == template,
        "atlas_rebuilt_fields": "XYZ and occupancy for nine guidepost atoms and seventeen LLK heavy atoms",
        "author_retained_pdb_content": "All PDB content except XYZ and occupancy for the 26 selected atom records, including all CONECT records",
        "author_supplied_choices": "Guidepost atom selection, alternate selection and consumer settings",
        "interface_matches_executed_reference_config": True,
        "alternate_choices": GROUPS,
        "joint_alternate_state_established": False,
        "complete_adduct_graph_established": False,
        "new_model_run": False,
        "atlas_efficacy_test": False,
        "atoms": provenance,
    }
    args.output_dir.mkdir(parents=True)
    (args.output_dir / "ra95_atlas_coordinates_author_template.pdb").write_bytes(output)
    (args.output_dir / "interface.json").write_text(json.dumps(interface, indent=2) + "\n")
    (args.output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "atoms"}, indent=2))


if __name__ == "__main__":
    main()
