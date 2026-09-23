#!/usr/bin/env python3
"""Build the exact RA95.5-8F parent control and one observed-state comparison."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np


SEQUENCE_SHA = "b842c993f9e9e3e80cffb546e6c8b5142541953e89b0bf4ddcfdfcb6aae0297b"
SOURCE_SHA = "6a7867da4e141c79ecb0c5542b3c5ab8b9aca20d638554c504612fde3930398d"
STATE_SHA = "90d9c76913dc67714e04b34bd8a126f4d35e5e01ba3bd80929ba623ef974d93c"
CIF_SHA = {
    "5AOU": "f97adeb9ea6b49b76f3cdb83366aa17bdfb56a42c8c168eb9e4d3f6ef121130e",
    "5AN7": "2ec74e2ac07a32c763a9f7ba75b2a0f33d92e5249ed0b2bcc89aa38a17dc9d5f",
}
DESIGN_CHECKS_SHA = "75ff8a12ebfd8b54d7c4e8a950893e119c3fe7f2ad97ac47b83aaca37a624393"
MOTIF = [
    (51, "TYR", "OH"), (51, "TYR", "CZ"),
    (83, "LYS", "NZ"), (83, "LYS", "CE"),
    (110, "ASN", "OD1"), (110, "ASN", "CG"), (110, "ASN", "ND2"),
    (180, "TYR", "OH"), (180, "TYR", "CZ"),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ranges(values: list[int]) -> list[str]:
    result: list[str] = []
    for _, group in itertools.groupby(enumerate(values), lambda item: item[1] - item[0]):
        run = [item[1] for item in group]
        result.append(str(run[0]) if len(run) == 1 else f"{run[0]}-{run[-1]}")
    return result


def compact_numbering(rows: list[dict[str, str]]) -> list[dict[str, int]]:
    rows = sorted(rows, key=lambda row: int(row["seq_id"]))
    assert [int(row["seq_id"]) for row in rows] == list(range(1, 259))
    segments: list[dict[str, int]] = []
    start = 1
    offset = int(rows[0]["pdb_seq_num"]) - 1
    for pos, row in enumerate(rows[1:], 2):
        new_offset = int(row["pdb_seq_num"]) - pos
        if new_offset != offset:
            segments.append({"label_start": start, "label_end": pos - 1, "author_offset": offset})
            start, offset = pos, new_offset
    segments.append({"label_start": start, "label_end": 258, "author_offset": offset})
    return segments


def choose_rows(atom_rows: list[dict[str, str]], atom_name: str) -> tuple[dict[int, dict], list[dict]]:
    grouped: dict[int, list[dict]] = {}
    for row in atom_rows:
        if row["label_asym_id"] != "A" or row["label_atom_id"] != atom_name:
            continue
        if row["label_seq_id"] in (".", "?"):
            continue
        grouped.setdefault(int(row["label_seq_id"]), []).append(row)
    selected: dict[int, dict] = {}
    alternates: list[dict] = []
    for pos, candidates in sorted(grouped.items()):
        candidates = sorted(
            candidates,
            key=lambda row: (
                0 if row["label_alt_id"] in (".", "?") else 1 if row["label_alt_id"] == "A" else 2,
                -float(row["occupancy"]), row["label_alt_id"], int(row["id"]),
            ),
        )
        chosen = candidates[0]
        selected[pos] = chosen
        if len(candidates) > 1:
            alternates.append({
                "label_seq_id": pos,
                "selected": {"atom_site_id": chosen["id"], "alt_id": chosen["label_alt_id"],
                             "occupancy": float(chosen["occupancy"])},
                "available": [{"atom_site_id": row["id"], "alt_id": row["label_alt_id"],
                               "occupancy": float(row["occupancy"])} for row in candidates],
            })
    return selected, alternates


def xyz(row: dict[str, str]) -> np.ndarray:
    return np.array([float(row[key]) for key in ("cartn_x", "cartn_y", "cartn_z")])


def align(mobile: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    x, y = mobile - mobile.mean(0), target - target.mean(0)
    u, _, vt = np.linalg.svd(x.T @ y)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(u @ vt)
    rotation = u @ correction @ vt
    translation = target.mean(0) - mobile.mean(0) @ rotation
    fitted = mobile @ rotation + translation
    rmsd = float(np.sqrt(np.mean(np.sum((fitted - target) ** 2, axis=1))))
    return rotation, translation, rmsd


def atom_record(row: dict[str, str]) -> dict:
    return {
        "label_seq_id": int(row["label_seq_id"]),
        "label_comp_id": row["label_comp_id"],
        "author_seq_id": row["auth_seq_id"],
        "atom_name": row["label_atom_id"],
        "atom_site_id": row["id"],
        "alt_id": None if row["label_alt_id"] in (".", "?") else row["label_alt_id"],
        "occupancy": float(row["occupancy"]),
        "xyz_angstrom": xyz(row).tolist(),
    }


def selected_motif(atom_rows: list[dict[str, str]], pdb_id: str) -> tuple[list[dict], np.ndarray]:
    records: list[dict] = []
    coordinates: list[np.ndarray] = []
    for pos, resname, atom_name in MOTIF:
        candidates = [row for row in atom_rows if row["label_asym_id"] == "A"
                      and row["label_seq_id"] == str(pos)
                      and row["label_comp_id"] == resname
                      and row["label_atom_id"] == atom_name]
        blanks = [row for row in candidates if row["label_alt_id"] in (".", "?")]
        alts_a = [row for row in candidates if row["label_alt_id"] == "A"]
        chosen = blanks[0] if len(blanks) == 1 else alts_a[0] if len(alts_a) == 1 else None
        if chosen is None:
            raise ValueError(f"{pdb_id} has no unique blank/alt-A row for {pos}:{atom_name}")
        records.append(atom_record(chosen))
        coordinates.append(xyz(chosen))
    return records, np.array(coordinates)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    repo, out_dir = args.repo.resolve(), args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(repo / "src"))
    from catalytic_earth.atlas_deposit_context import check_deposit_context
    from catalytic_earth.atlas_primary_source_check import parse_mmcif_categories

    source_path = repo / "data/atlas/study_context/ra95_2017/source_qualification.json"
    state_path = repo / "data/atlas/study_context/ra95_2017/chemical_state.json"
    design_checks = repo / "tools/research_lanes/ra95_design_reference/results/20260923-sequence-fold/checks.json"
    cif_paths = {pdb: repo / f"data/atlas/deposit_context/ra95_{pdb.lower()}/{pdb}.cif"
                 for pdb in ("5AOU", "5AN7")}
    expected = {source_path: SOURCE_SHA, state_path: STATE_SHA, design_checks: DESIGN_CHECKS_SHA,
                **{path: CIF_SHA[pdb] for pdb, path in cif_paths.items()}}
    for path, expected_sha in expected.items():
        if sha(path) != expected_sha:
            raise ValueError(f"source hash mismatch: {path}")

    tables = {}
    for pdb in ("5AOU", "5AN7"):
        packet = Path(f"data/atlas/deposit_context/ra95_{pdb.lower()}")
        check_deposit_context(packet, repo)
        tables[pdb] = parse_mmcif_categories(
            cif_paths[pdb].read_text(), categories={"_atom_site", "_pdbx_poly_seq_scheme"}
        )

    source = json.loads(source_path.read_text())
    state = json.loads(state_path.read_text())
    parent = next(row for row in source["constructs"] if row["construct_id"] == "RA95.5-8F")
    sequence = parent["sequence"]
    if len(sequence) != 258 or hashlib.sha256(sequence.encode()).hexdigest() != SEQUENCE_SHA:
        raise ValueError("source-printed parent sequence identity changed")
    activity = next(row for row in source["kinetic_observations"]
                    if row["construct_id"] == "RA95.5-8F")
    correspondence = state["sequence_correspondence"]
    states = {row["pdb_id"]: row for row in state["states"]}

    schemes, ca_rows, ca_alternates, atom_rows = {}, {}, {}, {}
    for pdb in ("5AOU", "5AN7"):
        schemes[pdb] = [row for row in tables[pdb]["_pdbx_poly_seq_scheme"]
                        if row["asym_id"] == "A" and row["entity_id"] == "1"]
        atom_rows[pdb] = tables[pdb]["_atom_site"]
        ca_rows[pdb], ca_alternates[pdb] = choose_rows(atom_rows[pdb], "CA")

    shared = sorted(set(ca_rows["5AOU"]) & set(ca_rows["5AN7"]))
    if shared != list(range(2, 58)) + list(range(64, 249)):
        raise ValueError(f"unexpected shared CA positions: {ranges(shared)}")
    core_shared = [pos for pos in shared if pos <= 245]
    apo_ca = np.array([xyz(ca_rows["5AOU"][pos]) for pos in shared])
    complex_ca = np.array([xyz(ca_rows["5AN7"][pos]) for pos in shared])
    rotation, translation, ca_rmsd = align(apo_ca, complex_ca)
    _, _, core_ca_rmsd = align(
        np.array([xyz(ca_rows["5AOU"][pos]) for pos in core_shared]),
        np.array([xyz(ca_rows["5AN7"][pos]) for pos in core_shared]),
    )

    motif_records, motif_xyz = {}, {}
    for pdb in ("5AOU", "5AN7"):
        motif_records[pdb], motif_xyz[pdb] = selected_motif(atom_rows[pdb], pdb)
    fitted_apo_motif = motif_xyz["5AOU"] @ rotation + translation
    motif_rmsd = float(np.sqrt(np.mean(np.sum((fitted_apo_motif - motif_xyz["5AN7"]) ** 2, axis=1))))
    pair_rows = []
    for i, j in itertools.combinations(range(len(MOTIF)), 2):
        apo_distance = float(np.linalg.norm(motif_xyz["5AOU"][i] - motif_xyz["5AOU"][j]))
        complex_distance = float(np.linalg.norm(motif_xyz["5AN7"][i] - motif_xyz["5AN7"][j]))
        pair_rows.append({
            "atoms": [f"{MOTIF[i][1]}{MOTIF[i][0]}:{MOTIF[i][2]}",
                      f"{MOTIF[j][1]}{MOTIF[j][0]}:{MOTIF[j][2]}"],
            "apo_5AOU_angstrom": apo_distance,
            "complex_5AN7_angstrom": complex_distance,
            "complex_minus_apo_angstrom": complex_distance - apo_distance,
        })
    absolute_deltas = [abs(row["complex_minus_apo_angstrom"]) for row in pair_rows]
    tyr_pair = next(row for row in pair_rows if row["atoms"] == ["TYR51:OH", "TYR180:OH"])

    fasta_path = out_dir / "ra95_5_8f_parent.fasta"
    fasta_path.write_text(">protein|ra95_5_8f_parent\n" + sequence + "\n")
    selected_numbering = {}
    for pdb in ("5AOU", "5AN7"):
        scheme_by_label = {int(row["seq_id"]): row for row in schemes[pdb]}
        selected_numbering[pdb] = {
            name: {"label_seq_id": pos, "author_seq_id": scheme_by_label[pos]["pdb_seq_num"]}
            for name, pos in (("Tyr51", 51), ("Ser81", 81), ("Lys83", 83),
                              ("Asn110", 110), ("Tyr180", 180), ("MHO237", 237))
        }

    manifest = {
        "schema_version": "catalytic-earth.ra95-parent-chai-control.v1",
        "repository_base_commit": "99142e880a10d87cee9dab5f5609eb6eae931f5c",
        "scope": {
            "purpose": "Known-active RA95.5-8F protein-only Chai sanity control.",
            "execution_status": "materialized_only; no model invocation",
            "claim_boundary": "Not an independent assay, activity prediction, Atlas-benefit test, fresh-generalization test or calibrated precision estimate. Predictor training-set independence for this known parent is not established.",
        },
        "construct": {
            "id": "RA95.5-8F",
            "source_packet": {"path": str(source_path.relative_to(repo)), "sha256": SOURCE_SHA,
                              "json_pointer": "/constructs/0"},
            "sequence_source": parent["source"],
            "sequence_status": parent["sequence_status"],
            "sequence_length": 258,
            "sequence_sha256": SEQUENCE_SHA,
            "fasta": {"path": fasta_path.name, "sha256": sha(fasta_path),
                      "header": "protein|ra95_5_8f_parent"},
            "sequence_handling": {
                "trimmed": False,
                "starting_methionine_retained": True,
                "terminal_suffix": correspondence["source_reported_suffix"],
                "terminal_suffix_positions": correspondence["source_reported_suffix_positions"],
                "mature_n_terminus_limit": correspondence["initiator_methionine_limit"],
            },
            "source_reported_activity": activity,
            "physical_specimen_identity": correspondence["physical_preparation_identity_status"],
        },
        "reference_5AOU": {
            "state_id": states["5AOU"]["state_id"],
            "source_assignment": states["5AOU"]["source_assignment"],
            "cif": {"path": str(cif_paths["5AOU"].relative_to(repo)), "sha256": CIF_SHA["5AOU"]},
            "projection_sha256": sha(repo / "data/atlas/deposit_context/ra95_5aou/projection.json"),
            "numbering": {"source_category": "_pdbx_poly_seq_scheme",
                          "segments": compact_numbering(schemes["5AOU"]),
                          "selected": selected_numbering["5AOU"], "global_offset_valid": False},
            "coordinate_scope": {
                "fully_unmodeled_label_positions": correspondence["source_deposit_model_conflict"]["deposits"]["5AOU_unmodeled_label_positions"],
                "partially_modeled_without_CA": {"label_seq_id": 249, "component": "GLY",
                                                 "present_atoms": ["N"], "atom_site_id": "2079"},
                "selected_CA_position_ranges": ranges(sorted(ca_rows["5AOU"])),
                "selected_CA_count": len(ca_rows["5AOU"]),
                "expression_tag_positions": correspondence["deposit_tag_scope"]["5AOU_expression_tag_positions"],
                "MHO237": {"canonical_parent": "MET", "deposited": "MHO",
                           "OD1_occupancy": correspondence["mho_oxygen_occupancy"]["5AOU"],
                           "use": "CA backbone comparison only; no side-chain identity score or functional inference"},
                "alternate_policy": "Blank alt, otherwise alt A when present, otherwise highest occupancy/lexical id; bookkeeping only, not a joint conformer assertion.",
            },
            "motif_rows": motif_records["5AOU"],
            "role": "Apo coordinate context, not productive or transition-state geometry.",
        },
        "future_chai_run": {
            "input": {"fasta": fasta_path.name, "entity_type": "protein", "ligand": None,
                      "template": None, "motif_restraints": None},
            "matched_settings": {"seed": 43, "num_trunk_recycles": 3,
                                 "num_diffn_timesteps": 200, "structure_output": ["pdb", "cif"],
                                 "export_arrays": True, "export_seed": True,
                                 "expected_native_model_indices": [0, 1, 2, 3, 4],
                                 "samples_are_correlated": True},
            "evaluation": {
                "mapping": "Prediction residue i maps to 5AOU label_seq_id i; never use one global author offset.",
                "integrity": ["exact 258-residue sequence", "chain inventory", "complete prediction backbone",
                              "finite/duplicate atom checks", "all nine motif atoms"],
                "primary_alignment": "Kabsch alignment on all 241 5AOU positions with a selected CA (ranges 2-57,64-248); motif RMSD uses this same transform.",
                "secondary_core_alignment": "Separately report CA RMSD for 238 shared positions <=245, excluding the deposited expression-tag scope.",
                "matched_design_metrics": ["global_ca_rmsd_angstrom", "motif_rmsd_after_global_alignment_angstrom",
                                           "36 motif_pair_distance_differences", "motif_pair_absolute_delta_mean_angstrom",
                                           "motif_pair_absolute_delta_max_angstrom", "ptm", "complex_plddt",
                                           "aggregate_score", "has_inter_chain_clashes"],
                "threshold": None,
            },
            "design_comparator": {"path": str(design_checks.relative_to(repo)),
                                  "sha256": DESIGN_CHECKS_SHA,
                                  "state_rule": "Compare deviations within each arm's own reference: parent to apo 5AOU, design to its generated 5AN7-derived reference. Do not equate absolute apo/inhibitor geometry.",
                                  "length_limit": "258-versus-150 length and context differ; report descriptive metrics without an uncalibrated threshold."},
        },
        "interpretation": {
            "parent_recovers_design_does_not": "The same protein-only setup recovers this known parent's apo fold/local geometry better than the design recovers its own conditioned reference. This does not prove inactivity or Atlas causation and may reflect predictor familiarity with the known fold.",
            "parent_does_not_recover": "Design local-geometry loss is not separable from failure of this protein-only setup on the parent control; do not use it as a catalytic discriminator.",
            "both_recover": "Sequence-to-structure compatibility only; no biochemical validation.",
        },
    }

    comparison = {
        "schema_version": "catalytic-earth.ra95-observed-state-comparison.v1",
        "scope": "Observed apo-versus-inhibitor structural spread; not Chai calibration, activity evidence, productive geometry or a pass threshold.",
        "sources": {pdb: {"path": str(cif_paths[pdb].relative_to(repo)), "sha256": CIF_SHA[pdb],
                           "state_id": states[pdb]["state_id"],
                           "numbering_segments": compact_numbering(schemes[pdb])}
                    for pdb in ("5AOU", "5AN7")},
        "row_selection": {
            "shared_CA_label_position_ranges": ranges(shared),
            "shared_CA_count": len(shared),
            "core_CA_label_position_ranges": ranges(core_shared),
            "core_CA_count": len(core_shared),
            "residue_249": {"component": "GLY", "status": "N-only in both deposits; excluded from CA alignment",
                            "5AOU_atom_site_id": "2079", "5AN7_atom_site_id": "4474"},
            "CA_policy": "Blank alt, otherwise alt A when present; if A is absent, highest occupancy then lexical id. No joint-state inference.",
            "5AOU_CA_alternates": ca_alternates["5AOU"],
            "5AN7_CA_alternates": ca_alternates["5AN7"],
            "MHO237": "Included by CA only in both structures; canonical source residue is MET.",
            "motif_policy": "Blank row when unique; otherwise author-control alt A. All selected rows and occupancies are retained below.",
            "motif_rows": motif_records,
        },
        "metrics": {
            "global_CA_RMSD_angstrom": ca_rmsd,
            "global_CA_atom_count": len(shared),
            "secondary_core_CA_RMSD_angstrom": core_ca_rmsd,
            "secondary_core_CA_atom_count": len(core_shared),
            "motif_RMSD_after_same_global_CA_alignment_angstrom": motif_rmsd,
            "motif_atom_count": len(MOTIF),
            "motif_pair_count": len(pair_rows),
            "motif_pair_absolute_delta_mean_angstrom": float(np.mean(absolute_deltas)),
            "motif_pair_absolute_delta_max_angstrom": float(np.max(absolute_deltas)),
            "Tyr51OH_Tyr180OH": tyr_pair,
            "motif_pair_distance_differences": pair_rows,
        },
        "state_limit": "5AOU is source-named apo at pH4.6; 5AN7 is inhibitor-derived with unresolved deposited/source pH and alternate occupancies. The spread is observed crystal-state context, not conformational dynamics or productive-state evidence.",
    }
    manifest_path = out_dir / "manifest.json"
    comparison_path = out_dir / "apo_complex_comparison.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    comparison_path.write_text(json.dumps(comparison, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"fasta_sha256": sha(fasta_path), "manifest_sha256": sha(manifest_path),
                      "comparison_sha256": sha(comparison_path), "sequence_sha256": SEQUENCE_SHA,
                      "shared_CA_count": len(shared), "motif_atom_count": len(MOTIF)}, indent=2))


if __name__ == "__main__":
    main()
