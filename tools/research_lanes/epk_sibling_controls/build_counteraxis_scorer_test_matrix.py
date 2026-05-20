#!/usr/bin/env python3
"""Build review-only scorer-design test cases from sibling controls.

This lane helper consolidates compact gamma/product counteraxis artifacts into
future scorer-design fixtures. It deliberately produces review-only data under
the research lane; it does not import labels, tune thresholds, or edit any
production registry.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE = Path("artifacts/research_lanes/epk_sibling_controls")

DEFAULT_GAMMA_ARTIFACTS = [
    LANE / "undercovered_expanded_gamma_counteraxis_20260520.json",
    LANE / "thin_expanded_gamma_counteraxis_20260520.json",
    LANE / "atp_grasp_expanded_gamma_counteraxis_20260520.json",
    LANE / "atp_grasp_expanded_product_state_gamma_counteraxis_20260520.json",
]

DEFAULT_PRODUCT_ARTIFACTS = [
    LANE / "strict_product_substrate_identity_counteraxis_20260520.json",
    LANE / "atp_grasp_expanded_product_counteraxis_20260520.json",
    LANE / "atp_grasp_expanded_product_state_product_counteraxis_20260520.json",
]

DEFAULT_DESIGN_PANEL = LANE / "counteraxis_scorer_design_cases_20260520.json"

ALLOWED_GAMMA_BLOCKERS = {
    "nonpolymer_acceptor_local_to_gamma",
    "nonpolymer_or_same_chain_local_oxygen_not_ePK_protein_substrate",
}

ALLOWED_PRODUCT_BLOCKERS = {
    "free_phosphate_product",
    "phosphorylated_hetatm_nonpolymer_product",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sorted_unique(values: list[Any]) -> list[Any]:
    return sorted({value for value in values if value is not None})


def min_distance(values: list[Any]) -> float | None:
    numbers = [value for value in values if isinstance(value, int | float)]
    if not numbers:
        return None
    return round(min(numbers), 3)


def merge_bool(values: list[Any]) -> bool:
    return any(bool(value) for value in values)


def collect_design_panel_case_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    panel = load_json(path)
    case_ids = set()
    for key in ("gamma_design_cases", "product_design_cases"):
        for row in panel.get(key, []):
            case_id = row.get("case_id")
            if case_id:
                case_ids.add(case_id)
    return case_ids


def blocker_class(blocker_id: str | None) -> str:
    if blocker_id in {
        "nonpolymer_acceptor_local_to_gamma",
        "free_phosphate_product",
        "phosphorylated_hetatm_nonpolymer_product",
    }:
        return "substrate_identity"
    if blocker_id == "nonpolymer_or_same_chain_local_oxygen_not_ePK_protein_substrate":
        return "substrate_identity_or_family_boundary"
    return "none_required"


def source_instances(rows: list[dict[str, Any]], axis: str) -> list[dict[str, Any]]:
    instances = []
    for row in rows:
        if axis == "gamma":
            instances.append(
                {
                    "source_artifact": row.get("_source_artifact") or row.get("source_artifact"),
                    "review_status": row.get("review_status"),
                    "nearest_gamma_to_metal_distance_angstrom": row.get(
                        "nearest_gamma_to_metal_distance_angstrom"
                    ),
                    "nearest_gamma_to_protein_hydroxyl_distance_angstrom": row.get(
                        "nearest_gamma_to_protein_hydroxyl_distance_angstrom"
                    ),
                    "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom": row.get(
                        "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom"
                    ),
                    "weak_nearest_any_oxygen_rule_hit_6a": row.get(
                        "weak_nearest_any_oxygen_rule_hit_6a"
                    ),
                    "source_free_counteraxis_blocker": row.get(
                        "source_free_counteraxis_blocker"
                    ),
                }
            )
        else:
            instances.append(
                {
                    "source_artifact": row.get("_source_artifact") or row.get("source_artifact"),
                    "product_state_branch_status": row.get("product_state_branch_status"),
                    "nearest_product_phosphoryl_to_metal_distance_angstrom": row.get(
                        "nearest_product_phosphoryl_to_metal_distance_angstrom"
                    ),
                    "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom": row.get(
                        "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom"
                    ),
                    "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom": row.get(
                        "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom"
                    ),
                    "weak_product_any_oxygen_rule_hit_6a": row.get(
                        "weak_product_any_oxygen_rule_hit_6a"
                    ),
                    "substrate_identity_counteraxis_blocker": row.get(
                        "substrate_identity_counteraxis_blocker"
                    ),
                }
            )
    return sorted(instances, key=lambda item: json.dumps(item, sort_keys=True))


def pick_blocker(rows: list[dict[str, Any]], key: str, allowed: set[str]) -> str | None:
    counts = Counter(row.get(key) for row in rows if row.get(key) in allowed)
    if not counts:
        return None
    return counts.most_common(1)[0][0]


def build_gamma_cases(
    paths: list[Path],
    design_panel_case_ids: set[str],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for path in paths:
        artifact = load_json(path)
        for row in artifact.get("controls", []):
            item = dict(row)
            item["_source_artifact"] = str(path)
            grouped[(item["family_id"], item["pdb_id"])].append(item)

    cases = []
    for (family_id, pdb_id), rows in sorted(grouped.items()):
        case_id = f"gamma::{family_id}::{pdb_id}"
        expected_block = merge_bool(
            [row.get("source_free_counteraxis_expected_block_review_only") for row in rows]
        )
        weak_any = merge_bool([row.get("weak_nearest_any_oxygen_rule_hit_6a") for row in rows])
        weak_protein = merge_bool(
            [row.get("weak_nearest_protein_hydroxyl_rule_hit_6a") for row in rows]
        )
        weak_nonpolymer = merge_bool(
            [row.get("weak_nearest_nonpolymer_oxygen_rule_hit_6a") for row in rows]
        )
        blocker_id = pick_blocker(
            rows,
            "source_free_counteraxis_blocker",
            ALLOWED_GAMMA_BLOCKERS,
        )
        expected_blocker_id = blocker_id if expected_block else None
        case_type = (
            "gamma_metal_weak_rule_expected_block"
            if weak_any
            else "gamma_metal_control_no_weak_rule_hit"
        )
        local_nonpolymer_acceptor = merge_bool(
            [
                row.get("source_free_counteraxis_features", {}).get(
                    "local_nonpolymer_acceptor_oxygen_6a"
                )
                for row in rows
            ]
        )
        cases.append(
            {
                "case_id": case_id,
                "axis": "gamma_proximity_counteraxis",
                "case_type": case_type,
                "family_id": family_id,
                "pdb_id": pdb_id,
                "structure_titles": sorted_unique(
                    [row.get("structure_title") for row in rows]
                ),
                "input_features": {
                    "gamma_capable_nucleotide_codes": sorted_unique(
                        code
                        for row in rows
                        for code in row.get("gamma_capable_nucleotide_codes", [])
                    ),
                    "metal_ligand_codes": sorted_unique(
                        code for row in rows for code in row.get("metal_ligand_codes", [])
                    ),
                    "nearest_gamma_to_metal_distance_angstrom": min_distance(
                        [row.get("nearest_gamma_to_metal_distance_angstrom") for row in rows]
                    ),
                    "nearest_gamma_to_protein_hydroxyl_distance_angstrom": min_distance(
                        [
                            row.get("nearest_gamma_to_protein_hydroxyl_distance_angstrom")
                            for row in rows
                        ]
                    ),
                    "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom": min_distance(
                        [
                            row.get("nearest_gamma_to_nonpolymer_oxygen_distance_angstrom")
                            for row in rows
                        ]
                    ),
                    "weak_nearest_protein_hydroxyl_rule_hit_6a": weak_protein,
                    "weak_nearest_nonpolymer_oxygen_rule_hit_6a": weak_nonpolymer,
                    "weak_nearest_any_oxygen_rule_hit_6a": weak_any,
                    "local_nonpolymer_acceptor_oxygen_6a": local_nonpolymer_acceptor,
                    "family_title_boundary_non_epk": True,
                },
                "expected_review_only_result": {
                    "should_block_weak_rule_hit": expected_block,
                    "expected_blocker": expected_blocker_id,
                    "expected_blocker_class": blocker_class(expected_blocker_id),
                    "production_scoring_admissible": False,
                    "epk_score_computed": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                },
                "assertions": [
                    "production_scoring_admissible == false",
                    "epk_score_computed == false",
                    "production_claim_allowed == false",
                    "labels_or_fingerprints_changed == false",
                    (
                        "if weak_nearest_any_oxygen_rule_hit_6a then "
                        "should_block_weak_rule_hit == true"
                    ),
                ],
                "source_artifacts": sorted_unique(
                    [row.get("_source_artifact") for row in rows]
                ),
                "source_instances": source_instances(rows, "gamma"),
                "included_in_existing_minimal_design_panel": case_id
                in design_panel_case_ids,
                "review_only": True,
            }
        )
    return cases


def build_product_cases(
    paths: list[Path],
    design_panel_case_ids: set[str],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for path in paths:
        artifact = load_json(path)
        for row in artifact.get("controls", []):
            item = dict(row)
            item["_source_artifact"] = str(path)
            grouped[(item["family_id"], item["pdb_id"])].append(item)

    cases = []
    for (family_id, pdb_id), rows in sorted(grouped.items()):
        case_id = f"product::{family_id}::{pdb_id}"
        expected_block = merge_bool(
            [
                row.get("substrate_identity_counteraxis_expected_block_review_only")
                for row in rows
            ]
        )
        weak_any = merge_bool([row.get("weak_product_any_oxygen_rule_hit_6a") for row in rows])
        weak_protein = merge_bool(
            [row.get("weak_product_protein_hydroxyl_rule_hit_6a") for row in rows]
        )
        weak_nonpolymer = merge_bool(
            [row.get("weak_product_nonpolymer_oxygen_rule_hit_6a") for row in rows]
        )
        blocker_id = pick_blocker(
            rows,
            "substrate_identity_counteraxis_blocker",
            ALLOWED_PRODUCT_BLOCKERS,
        )
        expected_blocker_id = blocker_id if expected_block else None
        cases.append(
            {
                "case_id": case_id,
                "axis": "product_phosphoryl_identity_counteraxis",
                "case_type": "strict_product_state_expected_block",
                "family_id": family_id,
                "pdb_id": pdb_id,
                "structure_titles": sorted_unique(
                    [row.get("structure_title") for row in rows]
                ),
                "input_features": {
                    "product_or_partial_nucleotide_codes": sorted_unique(
                        code
                        for row in rows
                        for code in row.get("product_or_partial_nucleotide_codes", [])
                    ),
                    "phosphate_or_phosphoryl_mimic_codes": sorted_unique(
                        code
                        for row in rows
                        for code in row.get("phosphate_or_phosphoryl_mimic_codes", [])
                    ),
                    "phosphorylated_nonpolymer_ligand_codes": sorted_unique(
                        code
                        for row in rows
                        for code in row.get("phosphorylated_nonpolymer_ligand_codes", [])
                    ),
                    "metal_ligand_codes": sorted_unique(
                        code for row in rows for code in row.get("metal_ligand_codes", [])
                    ),
                    "nearest_product_phosphoryl_to_metal_distance_angstrom": min_distance(
                        [
                            row.get("nearest_product_phosphoryl_to_metal_distance_angstrom")
                            for row in rows
                        ]
                    ),
                    "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom": min_distance(
                        [
                            row.get(
                                "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom"
                            )
                            for row in rows
                        ]
                    ),
                    "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom": min_distance(
                        [
                            row.get(
                                "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom"
                            )
                            for row in rows
                        ]
                    ),
                    "weak_product_protein_hydroxyl_rule_hit_6a": weak_protein,
                    "weak_product_nonpolymer_oxygen_rule_hit_6a": weak_nonpolymer,
                    "weak_product_any_oxygen_rule_hit_6a": weak_any,
                    "phosphoryl_source_is_hetatm_product": blocker_id
                    in ALLOWED_PRODUCT_BLOCKERS,
                },
                "expected_review_only_result": {
                    "should_block_weak_product_rule_hit": expected_block,
                    "expected_blocker": expected_blocker_id,
                    "expected_blocker_class": blocker_class(expected_blocker_id),
                    "production_scoring_admissible": False,
                    "epk_score_computed": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                },
                "assertions": [
                    "production_scoring_admissible == false",
                    "epk_score_computed == false",
                    "production_claim_allowed == false",
                    "labels_or_fingerprints_changed == false",
                    (
                        "if weak_product_any_oxygen_rule_hit_6a then "
                        "should_block_weak_product_rule_hit == true"
                    ),
                ],
                "source_artifacts": sorted_unique(
                    [row.get("_source_artifact") for row in rows]
                ),
                "source_instances": source_instances(rows, "product"),
                "included_in_existing_minimal_design_panel": case_id
                in design_panel_case_ids,
                "review_only": True,
            }
        )
    return cases


def summarize_counts(cases: list[dict[str, Any]], expected_key: str) -> dict[str, Any]:
    family_counts = Counter(row["family_id"] for row in cases)
    blocker_counts = Counter(
        row["expected_review_only_result"]["expected_blocker"] or "none_required"
        for row in cases
    )
    expected_block_cases = [
        row for row in cases if row["expected_review_only_result"][expected_key]
    ]
    return {
        "case_count": len(cases),
        "expected_block_count": len(expected_block_cases),
        "expected_block_case_ids": [row["case_id"] for row in expected_block_cases],
        "family_case_counts": dict(sorted(family_counts.items())),
        "expected_blocker_counts": dict(sorted(blocker_counts.items())),
    }


def validate_cases(gamma_cases: list[dict[str, Any]], product_cases: list[dict[str, Any]]) -> list[str]:
    warnings = []
    gamma_unblocked = [
        row["case_id"]
        for row in gamma_cases
        if row["input_features"]["weak_nearest_any_oxygen_rule_hit_6a"]
        and not row["expected_review_only_result"]["should_block_weak_rule_hit"]
    ]
    product_unblocked = [
        row["case_id"]
        for row in product_cases
        if row["input_features"]["weak_product_any_oxygen_rule_hit_6a"]
        and not row["expected_review_only_result"]["should_block_weak_product_rule_hit"]
    ]
    if gamma_unblocked:
        warnings.append(f"unblocked_gamma_weak_cases={gamma_unblocked}")
    if product_unblocked:
        warnings.append(f"unblocked_product_weak_cases={product_unblocked}")
    return warnings


def build_artifact(args: argparse.Namespace) -> dict[str, Any]:
    gamma_paths = [Path(path) for path in args.gamma_artifact] or DEFAULT_GAMMA_ARTIFACTS
    product_paths = [Path(path) for path in args.product_artifact] or DEFAULT_PRODUCT_ARTIFACTS
    design_panel_case_ids = collect_design_panel_case_ids(Path(args.design_panel))

    gamma_cases = build_gamma_cases(gamma_paths, design_panel_case_ids)
    product_cases = build_product_cases(product_paths, design_panel_case_ids)
    warnings = validate_cases(gamma_cases, product_cases)
    gamma_summary = summarize_counts(gamma_cases, "should_block_weak_rule_hit")
    product_summary = summarize_counts(product_cases, "should_block_weak_product_rule_hit")
    existing_panel_case_ids = sorted(
        {
            row["case_id"]
            for row in [*gamma_cases, *product_cases]
            if row["included_in_existing_minimal_design_panel"]
        }
    )

    expected_unblocked = [
        row["case_id"]
        for row in gamma_cases
        if row["input_features"]["weak_nearest_any_oxygen_rule_hit_6a"]
        and not row["expected_review_only_result"]["should_block_weak_rule_hit"]
    ] + [
        row["case_id"]
        for row in product_cases
        if row["input_features"]["weak_product_any_oxygen_rule_hit_6a"]
        and not row["expected_review_only_result"]["should_block_weak_product_rule_hit"]
    ]

    return {
        "metadata": {
            "method": "epk_sibling_controls_review_only_counteraxis_scorer_test_matrix",
            "created_at": utc_now(),
            "review_only": True,
            "production_claim_allowed": False,
            "production_scoring_admissible": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "target_family_id": "epk",
            "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            "source_gamma_artifacts": [str(path) for path in gamma_paths],
            "source_product_artifacts": [str(path) for path in product_paths],
            "source_design_panel": str(args.design_panel),
            "unique_case_count": len(gamma_cases) + len(product_cases),
            "gamma_summary": gamma_summary,
            "product_summary": product_summary,
            "existing_minimal_design_panel_case_count": len(existing_panel_case_ids),
            "existing_minimal_design_panel_case_ids": existing_panel_case_ids,
            "expected_unblocked_weak_case_count": len(expected_unblocked),
            "expected_unblocked_weak_case_ids": expected_unblocked,
            "primary_outcome": "evidence_for" if not expected_unblocked else "evidence_against",
            "search_surface": (
                "De-duplicated review-only scorer-design matrix from expanded bounded "
                "ASKHA, dNK, GHKL, GHMP, NDK, PfkA, PfkB, and ATP-grasp sibling "
                "gamma/product counteraxis artifacts; no new structure fetches."
            ),
            "next_query": (
                "Keep these as future source-free scorer-design fixtures; only reopen "
                "sibling sourcing if a specific curated seed set appears."
            ),
        },
        "review_only_contract": {
            "do_not_import_as_labels": True,
            "do_not_calibrate_thresholds": True,
            "do_not_edit_production_registries": True,
            "do_not_claim_production_scoring": True,
            "expected_runtime_scope": "future scorer tests only",
        },
        "gamma_proximity_counteraxis_cases": gamma_cases,
        "product_phosphoryl_identity_counteraxis_cases": product_cases,
        "warnings": [
            "Review-only scorer-design matrix, not labels or production scoring.",
            "Weak gamma/product proximity rules remain unsafe unless paired with source-free substrate-identity and family-boundary blockers.",
            *warnings,
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--gamma-artifact", action="append", default=[])
    parser.add_argument("--product-artifact", action="append", default=[])
    parser.add_argument("--design-panel", default=str(DEFAULT_DESIGN_PANEL))
    args = parser.parse_args()

    artifact = build_artifact(args)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
