#!/usr/bin/env python3
"""Adjudicate strict product controls against a source-free identity blocker.

This review-only lane helper reads existing compact sibling-control artifacts
and summarizes whether strict product-state controls would be blocked by a
substrate-identity counteraxis based on the phosphoryl source being free
phosphate or a phosphorylated HETATM nonpolymer, not an ePK protein residue.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


CONTROL_ARTIFACTS = [
    Path("artifacts/research_lanes/epk_sibling_controls/atp_grasp_product_state_acceptor_adjudication_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/dnk_product_state_acceptor_adjudication_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/pfka_product_state_acceptor_adjudication_20260520.json"),
    Path("artifacts/research_lanes/epk_sibling_controls/pfkb_product_state_acceptor_adjudication_20260520.json"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_controls(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    family_id = data["metadata"]["reviewed_sibling_family_id"]
    controls = [
        row
        for row in data["rows"]
        if row.get("product_state_control_candidate_review_only")
    ]
    for row in controls:
        row["_source_artifact"] = str(path)
        row["_family_id"] = family_id
    return controls


def blocker_for(row: dict) -> tuple[str, str]:
    phosphorylated_nonpolymer_codes = row.get("phosphorylated_nonpolymer_ligand_codes", [])
    phosphoryl_codes = row.get("phosphate_or_phosphoryl_mimic_codes", [])
    if phosphorylated_nonpolymer_codes:
        return (
            "phosphorylated_hetatm_nonpolymer_product",
            "product phosphoryl source is a phosphorylated HETATM nonpolymer ligand, not an ATOM Ser/Thr/Tyr substrate residue",
        )
    if "PO4" in phosphoryl_codes:
        return (
            "free_phosphate_product",
            "product phosphoryl source is free HETATM phosphate, not an ATOM Ser/Thr/Tyr substrate residue",
        )
    return (
        "unclassified_product_phosphoryl_source",
        "strict control lacks a recognized free-phosphate or phosphorylated-nonpolymer identity blocker",
    )


def compact_control(row: dict) -> dict:
    blocker_id, blocker_reason = blocker_for(row)
    protein_distance = row.get("nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom")
    nonpolymer_distance = row.get("nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom")
    metal_distance = row.get("nearest_product_phosphoryl_to_metal_distance_angstrom")
    return {
        "pdb_id": row["pdb_id"],
        "family_id": row["_family_id"],
        "source_artifact": row["_source_artifact"],
        "structure_title": row.get("structure_title"),
        "product_state_branch_status": row.get("product_state_branch_status"),
        "product_or_partial_nucleotide_codes": row.get("product_or_partial_nucleotide_codes", []),
        "phosphate_or_phosphoryl_mimic_codes": row.get("phosphate_or_phosphoryl_mimic_codes", []),
        "phosphorylated_nonpolymer_ligand_codes": row.get("phosphorylated_nonpolymer_ligand_codes", []),
        "metal_ligand_codes": row.get("metal_ligand_codes", []),
        "nearest_product_phosphoryl_to_metal_distance_angstrom": metal_distance,
        "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom": protein_distance,
        "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom": nonpolymer_distance,
        "weak_product_protein_hydroxyl_rule_hit_6a": (
            protein_distance is not None and protein_distance <= 6.0
        ),
        "weak_product_nonpolymer_oxygen_rule_hit_6a": (
            nonpolymer_distance is not None and nonpolymer_distance <= 6.0
        ),
        "weak_product_any_oxygen_rule_hit_6a": (
            min(
                [
                    distance
                    for distance in (protein_distance, nonpolymer_distance)
                    if distance is not None
                ]
                or [999.0]
            )
            <= 6.0
        ),
        "substrate_identity_counteraxis_blocker": blocker_id,
        "substrate_identity_counteraxis_reason": blocker_reason,
        "substrate_identity_counteraxis_expected_block_review_only": blocker_id
        != "unclassified_product_phosphoryl_source",
        "source_free_counteraxis_features": {
            "product_or_partial_nucleotide_present": bool(
                row.get("product_or_partial_nucleotide_codes")
            ),
            "metal_local_to_product_phosphoryl_7a": (
                metal_distance is not None and metal_distance <= 7.0
            ),
            "phosphoryl_source_is_hetatm_product": blocker_id
            != "unclassified_product_phosphoryl_source",
            "production_scoring_admissible": row.get("production_scoring_admissible", False),
            "epk_score_computed": row.get("epk_score_computed", False),
            "labels_or_fingerprints_changed": row.get(
                "labels_or_fingerprints_changed", False
            ),
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
        help="Optional control artifact path; defaults to the 20260520 strict product controls.",
    )
    args = parser.parse_args()

    paths = [Path(path) for path in args.artifact] if args.artifact else CONTROL_ARTIFACTS
    started_at = utc_now()
    controls = []
    for path in paths:
        controls.extend(load_controls(path))

    compact_controls = [compact_control(row) for row in controls]
    blocked = [
        row
        for row in compact_controls
        if row["substrate_identity_counteraxis_expected_block_review_only"]
    ]
    weak_product_any_hits = [
        row for row in compact_controls if row["weak_product_any_oxygen_rule_hit_6a"]
    ]
    weak_product_protein_hits = [
        row for row in compact_controls if row["weak_product_protein_hydroxyl_rule_hit_6a"]
    ]
    weak_product_nonpolymer_hits = [
        row for row in compact_controls if row["weak_product_nonpolymer_oxygen_rule_hit_6a"]
    ]
    blocker_counts = Counter(
        row["substrate_identity_counteraxis_blocker"] for row in compact_controls
    )
    family_counts = Counter(row["family_id"] for row in compact_controls)
    family_blocked_counts = Counter(row["family_id"] for row in blocked)
    unblocked = [
        row
        for row in compact_controls
        if not row["substrate_identity_counteraxis_expected_block_review_only"]
    ]

    artifact = {
        "metadata": {
            "method": "epk_sibling_controls_strict_product_substrate_identity_counteraxis_adjudication",
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
            "strict_product_controls_reviewed": len(compact_controls),
            "strict_product_control_pdb_ids": [row["pdb_id"] for row in compact_controls],
            "family_control_counts": dict(sorted(family_counts.items())),
            "substrate_identity_counteraxis_blocked_count": len(blocked),
            "substrate_identity_counteraxis_blocked_pdb_ids": [
                row["pdb_id"] for row in blocked
            ],
            "family_blocked_counts": dict(sorted(family_blocked_counts.items())),
            "substrate_identity_counteraxis_unblocked_count": len(unblocked),
            "substrate_identity_counteraxis_unblocked_pdb_ids": [
                row["pdb_id"] for row in unblocked
            ],
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "weak_product_any_oxygen_counterexample_count": len(weak_product_any_hits),
            "weak_product_any_oxygen_counterexample_pdb_ids": [
                row["pdb_id"] for row in weak_product_any_hits
            ],
            "weak_product_protein_hydroxyl_counterexample_count": len(
                weak_product_protein_hits
            ),
            "weak_product_protein_hydroxyl_counterexample_pdb_ids": [
                row["pdb_id"] for row in weak_product_protein_hits
            ],
            "weak_product_nonpolymer_oxygen_counterexample_count": len(
                weak_product_nonpolymer_hits
            ),
            "weak_product_nonpolymer_oxygen_counterexample_pdb_ids": [
                row["pdb_id"] for row in weak_product_nonpolymer_hits
            ],
            "primary_outcome": "evidence_for" if not unblocked else "evidence_against",
            "search_surface": (
                "Existing strict product-state controls from ATP-grasp, dNK, PfkA, "
                "and PfkB lane artifacts; source-free blocker uses only ligand "
                "identity, HETATM/ATOM class inherited from the source scan, and "
                "local product-phosphoryl distances already recorded in compact JSON."
            ),
            "next_query": (
                "Use this review-only blocker definition when a future scorer adds "
                "substrate-identity counteraxes; do not calibrate production thresholds "
                "from these rows."
            ),
        },
        "controls": compact_controls,
        "warnings": [
            "Review-only counteraxis adjudication; not production scoring, threshold calibration, registry work, or label import.",
            "A blocked sibling control can still be a weak-rule counterexample because local product-phosphoryl geometry alone is not substrate identity.",
        ],
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
