#!/usr/bin/env python3
"""Inspect one five-output protein-only Chai run of the RA95.5-8F parent."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


EXPECTED_MANIFEST_SHA = "462e4a1888c23d729034c11031c74aabc819f1145ef76ab967a092028c062fba"
EXPECTED_MATERIALIZER_SHA = "b7aa4ae18dc7e2cf421c465610c050ae755aa7bb8e4fad5042b309551b3d7cd1"
EXPECTED_INDICES = list(range(5))
AA3 = {a: b for a, b in zip(
    "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
    "ARNDCQEGHILKMFPSTWYV",
)}
CONFIDENCE_FIELDS = [
    "aggregate_score", "ptm", "iptm", "per_chain_ptm", "per_chain_pair_iptm",
    "has_inter_chain_clashes", "chain_intra_clashes", "chain_chain_inter_clashes",
    "pae", "per_chain_plddt", "complex_plddt", "seed",
]
ARRAY_FIELDS = ["pae_array", "plddt_array"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path, repo: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("ra95_parent_materializer", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load materializer {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_fasta(path: Path) -> tuple[str, str]:
    header = None
    sequence: list[str] = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                raise ValueError("parent FASTA must contain exactly one record")
            header = line[1:]
        elif header is None:
            raise ValueError("FASTA sequence precedes header")
        else:
            sequence.append(line)
    if header is None:
        raise ValueError("parent FASTA is empty")
    return header, "".join(sequence)


def expand_ranges(items: list[str]) -> list[int]:
    positions: list[int] = []
    for item in items:
        if "-" in item:
            start, end = (int(value) for value in item.split("-", 1))
            positions.extend(range(start, end + 1))
        else:
            positions.append(int(item))
    return positions


def read_pdb(path: Path) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    residues: dict[int, dict[str, Any]] = {}
    duplicates: list[str] = []
    parse_errors: list[dict[str, Any]] = []
    ignored_alternates = 0
    for line_number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if line[:6] != "ATOM  ":
            continue
        if len(line) < 54:
            parse_errors.append({"line": line_number, "error": "short ATOM row"})
            continue
        alt = line[16:17]
        if alt not in ("", " ", "A"):
            ignored_alternates += 1
            continue
        try:
            chain = line[21:22].strip() or "_"
            position = int(line[22:26])
            insertion = line[26:27].strip()
            atom_name = line[12:16].strip()
            residue_name = line[17:20].strip()
            coordinate = np.array([float(line[a:b]) for a, b in ((30, 38), (38, 46), (46, 54))])
        except Exception as exc:
            parse_errors.append({"line": line_number, "error": str(exc)})
            continue
        residue = residues.setdefault(position, {
            "chain": chain, "position": position, "insertion_code": insertion,
            "residue_name": residue_name, "atoms": {},
        })
        if (residue["chain"], residue["insertion_code"], residue["residue_name"]) != (
            chain, insertion, residue_name
        ):
            parse_errors.append({"line": line_number, "error": f"conflicting residue identity at {position}"})
            continue
        if atom_name in residue["atoms"]:
            duplicates.append(f"{chain}{position}{insertion}:{atom_name}")
        else:
            residue["atoms"][atom_name] = coordinate
    positions = sorted(residues)
    chains = sorted({row["chain"] for row in residues.values()})
    insertions = sorted({row["insertion_code"] for row in residues.values() if row["insertion_code"]})
    sequence = "".join(AA3.get(residues[pos]["residue_name"], "X") for pos in positions)
    missing_backbone = [
        f"{residues[pos]['chain']}{pos}:{atom}"
        for pos in positions for atom in ("N", "CA", "C", "O")
        if atom not in residues[pos]["atoms"]
    ]
    nonfinite = [
        f"{residues[pos]['chain']}{pos}:{atom}"
        for pos in positions for atom, coordinate in residues[pos]["atoms"].items()
        if not np.isfinite(coordinate).all()
    ]
    return residues, {
        "path": str(path),
        "sha256": sha(path),
        "bytes": path.stat().st_size,
        "residue_count": len(residues),
        "position_ranges": positions,
        "chains": chains,
        "insertion_codes": insertions,
        "sequence": sequence,
        "sequence_sha256": hashlib.sha256(sequence.encode()).hexdigest(),
        "missing_backbone_atoms": missing_backbone,
        "nonfinite_atoms": nonfinite,
        "duplicate_atoms": duplicates,
        "parse_errors": parse_errors,
        "ignored_non_A_alternate_atom_rows": ignored_alternates,
    }


def array_shape(value: Any) -> list[int] | None:
    shape: list[int] = []
    cursor = value
    while isinstance(cursor, list):
        shape.append(len(cursor))
        if not cursor:
            return shape
        first_shape = array_shape(cursor[0])
        if any(array_shape(item) != first_shape for item in cursor[1:]):
            return None
        cursor = cursor[0]
    return shape


def score_summary(path: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(), parse_constant=lambda token: token)
    except Exception as exc:
        return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size,
                "parse_error": str(exc)}, ["score JSON did not parse"]
    if not isinstance(payload, dict):
        return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size,
                "parse_error": "top level is not an object"}, ["score JSON top level is not an object"]
    native = {key: payload.get(key) for key in CONFIDENCE_FIELDS if key in payload}
    arrays = {
        key: {"shape": array_shape(payload[key]), "retained_in_raw_score_file": True}
        for key in ARRAY_FIELDS if key in payload
    }
    seed = payload.get("seed")
    required = {"aggregate_score", "ptm", "complex_plddt", "has_inter_chain_clashes", "seed",
                "pae_array", "plddt_array"}
    missing = sorted(required - set(payload))
    if missing:
        errors.append(f"native score fields missing: {missing}")
    if seed != 43:
        errors.append(f"native score seed differs: {seed!r}")
    return {
        "path": str(path), "sha256": sha(path), "bytes": path.stat().st_size,
        "native_confidence": native, "large_arrays": arrays,
        "other_native_fields": sorted(set(payload) - set(CONFIDENCE_FIELDS) - set(ARRAY_FIELDS)),
        "parse_error": None,
    }, errors


def pair_differences(model: np.ndarray, reference: np.ndarray, labels: list[str]) -> list[dict]:
    rows = []
    for i, j in itertools.combinations(range(len(labels)), 2):
        ref_distance = float(np.linalg.norm(reference[i] - reference[j]))
        model_distance = float(np.linalg.norm(model[i] - model[j]))
        rows.append({
            "atoms": [labels[i], labels[j]],
            "reference_angstrom": ref_distance,
            "model_angstrom": model_distance,
            "model_minus_reference_angstrom": model_distance - ref_distance,
        })
    return rows


def compare_geometry(
    model_atoms: dict[int, dict[str, np.ndarray]],
    reference_ca: dict[int, np.ndarray],
    reference_motif: np.ndarray,
    motif_spec: list[tuple[int, str]],
    align_fn,
) -> dict:
    positions = sorted(reference_ca)
    missing_ca = [pos for pos in positions if pos not in model_atoms or "CA" not in model_atoms[pos]]
    if missing_ca:
        raise ValueError(f"prediction lacks mapped CA positions {missing_ca}")
    model_ca = np.array([model_atoms[pos]["CA"] for pos in positions])
    target_ca = np.array([reference_ca[pos] for pos in positions])
    rotation, translation, global_rmsd = align_fn(model_ca, target_ca)
    core = [pos for pos in positions if pos <= 245]
    _, _, core_rmsd = align_fn(
        np.array([model_atoms[pos]["CA"] for pos in core]),
        np.array([reference_ca[pos] for pos in core]),
    )
    missing_motif = [
        f"A{pos}:{atom}" for pos, atom in motif_spec
        if pos not in model_atoms or atom not in model_atoms[pos]
    ]
    if missing_motif:
        raise ValueError(f"prediction lacks motif atoms {missing_motif}")
    model_motif = np.array([model_atoms[pos][atom] for pos, atom in motif_spec])
    fitted = model_motif @ rotation + translation
    motif_rmsd = float(np.sqrt(np.mean(np.sum((fitted - reference_motif) ** 2, axis=1))))
    labels = [f"A{pos}:{atom}" for pos, atom in motif_spec]
    pairs = pair_differences(model_motif, reference_motif, labels)
    deltas = [abs(row["model_minus_reference_angstrom"]) for row in pairs]
    tyr_pair = next(row for row in pairs if row["atoms"] == ["A51:OH", "A180:OH"])
    return {
        "global_ca_rmsd_angstrom": global_rmsd,
        "global_ca_atom_count": len(positions),
        "secondary_core_ca_rmsd_angstrom": core_rmsd,
        "secondary_core_ca_atom_count": len(core),
        "motif_rmsd_after_global_alignment_angstrom": motif_rmsd,
        "missing_motif_atoms": [],
        "motif_pair_distance_differences": pairs,
        "motif_pair_absolute_delta_mean_angstrom": float(np.mean(deltas)),
        "motif_pair_absolute_delta_max_angstrom": float(np.max(deltas)),
        "tyr51_oh_to_tyr180_oh": tyr_pair,
    }


def load_reference(repo: Path, manifest_path: Path, materializer_path: Path) -> dict[str, Any]:
    if sha(manifest_path) != EXPECTED_MANIFEST_SHA:
        raise ValueError("canonical parent manifest hash differs")
    if sha(materializer_path) != EXPECTED_MATERIALIZER_SHA:
        raise ValueError("canonical parent materializer hash differs")
    manifest = json.loads(manifest_path.read_text())
    fasta_path = manifest_path.parent / manifest["construct"]["fasta"]["path"]
    if sha(fasta_path) != manifest["construct"]["fasta"]["sha256"]:
        raise ValueError("parent FASTA hash differs from manifest")
    fasta_header, sequence = read_fasta(fasta_path)
    if len(sequence) != manifest["construct"]["sequence_length"]:
        raise ValueError("parent FASTA length differs from manifest")
    if hashlib.sha256(sequence.encode()).hexdigest() != manifest["construct"]["sequence_sha256"]:
        raise ValueError("parent sequence hash differs from manifest")
    cif_path = repo / manifest["reference_5AOU"]["cif"]["path"]
    if sha(cif_path) != manifest["reference_5AOU"]["cif"]["sha256"]:
        raise ValueError("5AOU CIF hash differs from manifest")

    sys.path.insert(0, str(repo / "src"))
    from catalytic_earth.atlas_deposit_context import check_deposit_context
    from catalytic_earth.atlas_primary_source_check import parse_mmcif_categories
    check_deposit_context(Path("data/atlas/deposit_context/ra95_5aou"), repo)
    materializer = load_module(materializer_path)
    tables = parse_mmcif_categories(cif_path.read_text(), categories={"_atom_site"})
    atom_rows = tables["_atom_site"]
    selected_ca, _ = materializer.choose_rows(atom_rows, "CA")
    expected_positions = expand_ranges(
        manifest["reference_5AOU"]["coordinate_scope"]["selected_CA_position_ranges"]
    )
    if sorted(selected_ca) != expected_positions:
        raise ValueError("rebuilt 5AOU CA selection differs from manifest")
    reference_ca = {pos: materializer.xyz(selected_ca[pos]) for pos in expected_positions}
    rebuilt_motif, rebuilt_xyz = materializer.selected_motif(atom_rows, "5AOU")
    if rebuilt_motif != manifest["reference_5AOU"]["motif_rows"]:
        raise ValueError("rebuilt 5AOU motif selection differs from manifest")
    motif_spec = [(row["label_seq_id"], row["atom_name"]) for row in rebuilt_motif]
    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "materializer_path": materializer_path,
        "materializer": materializer,
        "sequence": sequence,
        "fasta_header": fasta_header,
        "fasta_path": fasta_path,
        "cif_path": cif_path,
        "reference_ca": reference_ca,
        "reference_motif": rebuilt_xyz,
        "motif_spec": motif_spec,
    }


def run_self_test(reference: dict[str, Any]) -> dict:
    model_atoms: dict[int, dict[str, np.ndarray]] = {
        pos: {"CA": coordinate.copy()} for pos, coordinate in reference["reference_ca"].items()
    }
    for (pos, atom), coordinate in zip(reference["motif_spec"], reference["reference_motif"]):
        model_atoms.setdefault(pos, {})[atom] = coordinate.copy()
    exact = compare_geometry(
        model_atoms, reference["reference_ca"], reference["reference_motif"],
        reference["motif_spec"], reference["materializer"].align,
    )
    exact_values = [
        exact["global_ca_rmsd_angstrom"],
        exact["secondary_core_ca_rmsd_angstrom"],
        exact["motif_rmsd_after_global_alignment_angstrom"],
        exact["motif_pair_absolute_delta_max_angstrom"],
    ]
    if max(exact_values) > 1e-10:
        raise ValueError(f"5AOU exact self-control was not zero: {exact_values}")

    shifted = {pos + 1: atoms for pos, atoms in model_atoms.items() if pos < 258}
    detected = False
    error = None
    try:
        compare_geometry(
            shifted, reference["reference_ca"], reference["reference_motif"],
            reference["motif_spec"], reference["materializer"].align,
        )
    except ValueError as exc:
        detected, error = True, str(exc)
    if not detected:
        raise ValueError("shifted-residue fixture was not rejected")
    return {
        "schema_version": "catalytic-earth.ra95-parent-inspector-self-test.v1",
        "pins": {
            "manifest_sha256": EXPECTED_MANIFEST_SHA,
            "materializer_sha256": EXPECTED_MATERIALIZER_SHA,
            "reference_cif_sha256": sha(reference["cif_path"]),
        },
        "exact_5AOU_self_control": {
            "source": str(reference["cif_path"]),
            "global_ca_atom_count": exact["global_ca_atom_count"],
            "motif_atom_count": len(reference["motif_spec"]),
            "metrics": {
                "global_ca_rmsd_angstrom": exact["global_ca_rmsd_angstrom"],
                "secondary_core_ca_rmsd_angstrom": exact["secondary_core_ca_rmsd_angstrom"],
                "motif_rmsd_after_global_alignment_angstrom": exact["motif_rmsd_after_global_alignment_angstrom"],
                "motif_pair_count": len(exact["motif_pair_distance_differences"]),
                "motif_pair_absolute_delta_max_angstrom": exact["motif_pair_absolute_delta_max_angstrom"],
            },
            "zero_tolerance_angstrom": 1e-10,
            "passed": True,
        },
        "perturbed_residue_mapping_fixture": {
            "perturbation": "Shift every selected model residue key by +1; coordinates unchanged.",
            "detected": detected,
            "error": error,
        },
        "passed": True,
    }


def inspect_model(
    index: int,
    pdb_candidates: list[Path],
    cif_candidates: list[Path],
    score_candidates: list[Path],
    reference: dict[str, Any],
    repo: Path,
) -> tuple[dict[str, Any], list[str]]:
    record: dict[str, Any] = {
        "model_index": index,
        "pdb_candidates": [display_path(path, repo) for path in pdb_candidates],
        "cif_candidates": [display_path(path, repo) for path in cif_candidates],
        "score_candidates": [display_path(path, repo) for path in score_candidates],
    }
    errors: list[str] = []
    if len(pdb_candidates) != 1:
        errors.append(f"expected one PDB, found {len(pdb_candidates)}")
    if len(cif_candidates) != 1:
        errors.append(f"expected one CIF, found {len(cif_candidates)}")
    if len(score_candidates) != 1:
        errors.append(f"expected one score JSON, found {len(score_candidates)}")
    if len(cif_candidates) == 1:
        path = cif_candidates[0]
        record["cif"] = {"path": display_path(path, repo), "sha256": sha(path),
                         "bytes": path.stat().st_size}
    else:
        record["cif"] = None
    if len(score_candidates) == 1:
        record["score_as_supplied"], score_errors = score_summary(score_candidates[0])
        record["score_as_supplied"]["path"] = display_path(score_candidates[0], repo)
        errors.extend(score_errors)
    else:
        record["score_as_supplied"] = None
    if len(pdb_candidates) != 1:
        record["structure"] = None
        record["geometry"] = None
        record["errors"] = errors
        return record, errors

    pdb_path = pdb_candidates[0]
    residues, summary = read_pdb(pdb_path)
    summary["path"] = display_path(pdb_path, repo)
    expected_positions = list(range(1, 259))
    actual_positions = sorted(residues)
    mapping_errors = []
    if actual_positions != expected_positions:
        mapping_errors.append(f"residue positions differ: expected 1..258, observed {actual_positions}")
    if summary["chains"] != ["A"]:
        mapping_errors.append(f"chain inventory differs: {summary['chains']}")
    if summary["insertion_codes"]:
        mapping_errors.append(f"insertion codes present: {summary['insertion_codes']}")
    if summary["sequence"] != reference["sequence"]:
        mapping_errors.append("prediction sequence differs from exact 258-residue parent")
    if summary["missing_backbone_atoms"]:
        mapping_errors.append("prediction has missing backbone atoms")
    if summary["nonfinite_atoms"]:
        mapping_errors.append("prediction has non-finite atoms")
    if summary["duplicate_atoms"]:
        mapping_errors.append("prediction has duplicate atoms")
    if summary["parse_errors"]:
        mapping_errors.append("prediction PDB has parse errors")
    summary["exact_parent_sequence"] = summary["sequence"] == reference["sequence"]
    summary["position_mapping_valid"] = not mapping_errors
    summary["mapping_errors"] = mapping_errors
    record["structure"] = summary
    errors.extend(mapping_errors)
    if mapping_errors:
        record["geometry"] = None
    else:
        atoms = {pos: row["atoms"] for pos, row in residues.items()}
        try:
            record["geometry"] = compare_geometry(
                atoms, reference["reference_ca"], reference["reference_motif"],
                reference["motif_spec"], reference["materializer"].align,
            )
        except ValueError as exc:
            errors.append(str(exc))
            record["geometry"] = None
    record["errors"] = errors
    return record, errors


def run_inspection(repo: Path, prediction_dir: Path, reference: dict[str, Any]) -> tuple[dict, bool]:
    if not prediction_dir.is_dir():
        raise ValueError(f"prediction directory is missing: {prediction_dir}")
    inventory = [
        {"path": str(path.relative_to(prediction_dir)), "sha256": sha(path), "bytes": path.stat().st_size}
        for path in sorted(prediction_dir.rglob("*")) if path.is_file()
    ]
    models = []
    all_errors = []
    for index in EXPECTED_INDICES:
        pdb = sorted(prediction_dir.glob(f"pred.*_model_idx_{index}.pdb"))
        cif = sorted(prediction_dir.glob(f"pred.*_model_idx_{index}.cif"))
        score = sorted(prediction_dir.glob(f"scores.*_model_idx_{index}.json"))
        model, errors = inspect_model(index, pdb, cif, score, reference, repo)
        models.append(model)
        all_errors.extend(f"model {index}: {error}" for error in errors)
    result = {
        "schema_version": "catalytic-earth.ra95-parent-chai-inspection.v1",
        "scope": "Descriptive known-parent protein-only Chai sanity control; no calibrated cutoff, activity claim, fresh-generalization claim or Atlas-benefit claim.",
        "pins": {
            "manifest": {"path": display_path(reference["manifest_path"], repo),
                         "sha256": EXPECTED_MANIFEST_SHA},
            "materializer": {"path": display_path(reference["materializer_path"], repo),
                             "sha256": EXPECTED_MATERIALIZER_SHA},
            "parent_fasta": {"path": display_path(reference["fasta_path"], repo),
                             "sha256": sha(reference["fasta_path"]),
                             "sequence_sha256": reference["manifest"]["construct"]["sequence_sha256"]},
            "reference_5AOU": {"path": display_path(reference["cif_path"], repo),
                               "sha256": sha(reference["cif_path"])},
        },
        "prediction_directory": display_path(prediction_dir, repo),
        "output_inventory": inventory,
        "expected_model_indices": EXPECTED_INDICES,
        "models": models,
        "all_five_models_present_and_valid": not all_errors,
        "errors": all_errors,
        "interpretation_boundary": {
            "parent_recovery": "Pipeline sanity only; may reflect predictor familiarity with the known fold and does not validate activity.",
            "parent_nonrecovery": "Weakens use of the protein-only Chai local geometry as a catalytic discriminator for the designed sequence.",
            "selection": "Retain and report all five correlated native outputs; no winner or post-hoc threshold.",
        },
    }
    return result, not all_errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect five RA95.5-8F parent Chai outputs against apo 5AOU."
    )
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--materializer", type=Path)
    parser.add_argument("--prediction-dir", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    manifest_path = (args.manifest or repo / "tools/research_lanes/ra95_design_reference/parent_control/manifest.json").resolve()
    materializer_path = (args.materializer or repo / "tools/research_lanes/ra95_design_reference/parent_control/materialize_parent.py").resolve()
    reference = load_reference(repo, manifest_path, materializer_path)
    if args.self_test:
        result, valid = run_self_test(reference), True
    else:
        if args.prediction_dir is None:
            parser.error("--prediction-dir is required unless --self-test is used")
        result, valid = run_inspection(repo, args.prediction_dir.resolve(), reference)
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
