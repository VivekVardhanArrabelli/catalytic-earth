#!/usr/bin/env python3
"""Adjudicate gamma/metal sibling controls against source-free blockers.

This review-only lane helper reads compact sibling-control screen artifacts and
summarizes whether weak ePK gamma-proximity hits remain separable by source-free
non-ePK substrate identity or sibling-family boundary evidence.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ARTIFACTS = [
    Path("artifacts/research_lanes/epk_sibling_controls/atp_grasp_product_state_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/askha_product_state_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/dnk_product_state_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/ghkl_product_state_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/ghmp_product_state_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/pfka_bounded_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/pfkb_bounded_control_screen_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/ndk_bounded_control_screen_20260520.json"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_gamma_controls(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for row in data["rows"]:
        family_id = row.get("family_id")
        if row.get("review_status") != f"{family_id}_gamma_metal_control_candidate_review_only":
            continue
        item = dict(row)
        item["_source_artifact"] = str(path)
        rows.append(item)
    return rows


def weak_hit(row: dict) -> bool:
    return bool(
        row.get("weak_nearest_any_oxygen_rule_hit_6a")
        or row.get("weak_nearest_protein_hydroxyl_rule_hit_6a")
        or row.get("weak_nearest_nonpolymer_oxygen_rule_hit_6a")
    )


def first_local_nonpolymer(row: dict) -> dict | None:
    for oxygen in row.get("nearest_nonpolymer_oxygen_rows", []):
        distance = oxygen.get("distance_angstrom")
        if distance is not None and distance <= 6.0:
            return oxygen
    return None


def blocker_for(row: dict) -> tuple[str, str]:
    local_nonpolymer = first_local_nonpolymer(row)
    if local_nonpolymer:
        comp = local_nonpolymer.get("comp")
        atom = local_nonpolymer.get("atom")
        distance = local_nonpolymer.get("distance_angstrom")
        return (
            "nonpolymer_acceptor_local_to_gamma",
            f"nearest gamma-proximal oxygen is HETATM {comp}:{atom} at {distance} A, not an ATOM Ser/Thr/Tyr substrate residue",
        )
    expected = row.get("unified_rule_expected_blocker_source_free")
    if expected:
        return (
            expected,
            "existing compact screen marks the local oxygen context as non-ePK substrate identity evidence",
        )
    if weak_hit(row):
        return (
            "sibling_family_title_boundary_no_epk_substrate_role",
            "structure title and query boundary place the hit in a non-ePK ATP/Mg sibling family without ePK substrate-role context",
        )
    return (
        "control_without_weak_rule_hit",
        "gamma/metal sibling control does not hit the weak 6 A oxygen proximity rule",
    )


def compact_control(row: dict) -> dict:
    blocker_id, blocker_reason = blocker_for(row)
    local_nonpolymer = first_local_nonpolymer(row)
    local_nonpolymer_summary = None
    if local_nonpolymer:
        local_nonpolymer_summary = {
            "comp": local_nonpolymer.get("comp"),
            "atom": local_nonpolymer.get("atom"),
            "auth_asym_id": local_nonpolymer.get("auth_asym_id"),
            "auth_seq_id": local_nonpolymer.get("auth_seq_id"),
            "label_asym_id": local_nonpolymer.get("label_asym_id"),
            "label_seq_id": local_nonpolymer.get("label_seq_id"),
            "distance_angstrom": local_nonpolymer.get("distance_angstrom"),
            "gamma_ligand_code": local_nonpolymer.get("gamma_ligand_code"),
            "gamma_atom_name": local_nonpolymer.get("gamma_atom_name"),
        }
    weak_rule = weak_hit(row)
    expected_block = weak_rule and blocker_id != "control_without_weak_rule_hit"
    return {
        "pdb_id": row["pdb_id"],
        "family_id": row["family_id"],
        "family_name": row.get("family_name"),
        "source_artifact": row["_source_artifact"],
        "structure_title": row.get("structure_title"),
        "query_origins": row.get("query_origins", []),
        "review_status": row.get("review_status"),
        "gamma_capable_nucleotide_codes": row.get("gamma_capable_nucleotide_codes", []),
        "metal_ligand_codes": row.get("metal_ligand_codes", []),
        "observed_ligand_codes": row.get("observed_ligand_codes", []),
        "nearest_gamma_to_metal_distance_angstrom": row.get("nearest_gamma_to_metal_distance_angstrom"),
        "nearest_gamma_to_protein_hydroxyl_distance_angstrom": row.get("nearest_gamma_to_protein_hydroxyl_distance_angstrom"),
        "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom": row.get("nearest_gamma_to_nonpolymer_oxygen_distance_angstrom"),
        "weak_nearest_protein_hydroxyl_rule_hit_6a": bool(row.get("weak_nearest_protein_hydroxyl_rule_hit_6a")),
        "weak_nearest_nonpolymer_oxygen_rule_hit_6a": bool(row.get("weak_nearest_nonpolymer_oxygen_rule_hit_6a")),
        "weak_nearest_any_oxygen_rule_hit_6a": weak_rule,
        "nearest_local_nonpolymer_oxygen": local_nonpolymer_summary,
        "source_free_counteraxis_blocker": blocker_id,
        "source_free_counteraxis_reason": blocker_reason,
        "source_free_counteraxis_expected_block_review_only": expected_block,
        "source_free_counteraxis_features": {
            "gamma_capable_nucleotide_present": bool(row.get("gamma_capable_nucleotide_codes")),
            "metal_local_to_gamma_6a": (
                row.get("nearest_gamma_to_metal_distance_angstrom") is not None
                and row["nearest_gamma_to_metal_distance_angstrom"] <= 6.0
            ),
            "local_nonpolymer_acceptor_oxygen_6a": local_nonpolymer is not None,
            "family_title_boundary_non_epk": True,
            "production_scoring_admissible": row.get("production_scoring_admissible", False),
            "epk_score_computed": row.get("epk_score_computed", False),
            "labels_or_fingerprints_changed": row.get("labels_or_fingerprints_changed", False),
        },
        "review_only": True,
        "production_claim_allowed": False,
        "production_scoring_admissible": False,
        "epk_score_computed": False,
        "labels_or_fingerprints_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Optional bounded control artifact path; defaults to all current sibling family screens.",
    )
    args = parser.parse_args()

    paths = [Path(path) for path in args.artifact] if args.artifact else DEFAULT_ARTIFACTS
    started_at = utc_now()
    controls = []
    for path in paths:
        controls.extend(load_gamma_controls(path))

    compact_controls = [compact_control(row) for row in controls]
    weak_controls = [row for row in compact_controls if row["weak_nearest_any_oxygen_rule_hit_6a"]]
    blocked_weak = [
        row
        for row in weak_controls
        if row["source_free_counteraxis_expected_block_review_only"]
    ]
    unblocked_weak = [
        row
        for row in weak_controls
        if not row["source_free_counteraxis_expected_block_review_only"]
    ]
    nonpolymer_blocked = [
        row
        for row in blocked_weak
        if row["source_free_counteraxis_blocker"] == "nonpolymer_acceptor_local_to_gamma"
    ]
    family_counts = Counter(row["family_id"] for row in compact_controls)
    family_weak_counts = Counter(row["family_id"] for row in weak_controls)
    family_blocked_counts = Counter(row["family_id"] for row in blocked_weak)
    blocker_counts = Counter(row["source_free_counteraxis_blocker"] for row in compact_controls)
    weak_blocker_counts = Counter(row["source_free_counteraxis_blocker"] for row in blocked_weak)

    artifact = {
        "metadata": {
            "method": "epk_sibling_controls_gamma_control_source_free_counteraxis_adjudication",
            "created_at": utc_now(),
            "screen_started_at": started_at,
            "review_only": True,
            "production_claim_allowed": False,
            "production_scoring_admissible": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "target_family_id": "epk",
            "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            "source_artifacts": [str(path) for path in paths],
            "gamma_metal_controls_reviewed": len(compact_controls),
            "gamma_metal_control_pdb_ids": [row["pdb_id"] for row in compact_controls],
            "family_control_counts": dict(sorted(family_counts.items())),
            "weak_rule_counterexample_count": len(weak_controls),
            "weak_rule_counterexample_pdb_ids": [row["pdb_id"] for row in weak_controls],
            "family_weak_rule_counts": dict(sorted(family_weak_counts.items())),
            "source_free_counteraxis_blocked_weak_count": len(blocked_weak),
            "source_free_counteraxis_blocked_weak_pdb_ids": [row["pdb_id"] for row in blocked_weak],
            "family_blocked_weak_counts": dict(sorted(family_blocked_counts.items())),
            "source_free_counteraxis_unblocked_weak_count": len(unblocked_weak),
            "source_free_counteraxis_unblocked_weak_pdb_ids": [row["pdb_id"] for row in unblocked_weak],
            "nonpolymer_acceptor_blocked_weak_count": len(nonpolymer_blocked),
            "nonpolymer_acceptor_blocked_weak_pdb_ids": [row["pdb_id"] for row in nonpolymer_blocked],
            "blocker_counts_all_gamma_controls": dict(sorted(blocker_counts.items())),
            "blocker_counts_blocked_weak_controls": dict(sorted(weak_blocker_counts.items())),
            "primary_outcome": "evidence_for" if not unblocked_weak else "evidence_against",
            "search_surface": (
                "Existing bounded gamma/metal sibling controls from ASKHA, dNK, GHKL, GHMP, ATP-grasp, PfkA, PfkB, and NDK artifacts; "
                "adjudication uses only compact source-free fields already recorded in lane JSON."
            ),
            "next_query": (
                "Add a fresh under-covered ASKHA/dNK/GHKL/GHMP seed set only if new curated ligand/title seeds appear; otherwise keep using these blockers as review-only scorer design inputs."
            ),
        },
        "controls": compact_controls,
        "warnings": [
            "Review-only counteraxis adjudication; not production scoring, threshold calibration, registry work, or label import.",
            "Weak gamma-to-oxygen proximity remains falsified on sibling families unless paired with source-free substrate-identity and family-boundary blockers.",
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
