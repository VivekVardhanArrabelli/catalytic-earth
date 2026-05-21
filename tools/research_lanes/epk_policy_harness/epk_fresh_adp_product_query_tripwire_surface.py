#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from epk_fresh_surface_scan import (  # noqa: E402
    ACCEPTOR_ATOMS,
    METAL_CODES,
    atom_chain,
    atom_code,
    atom_distance,
    atom_name,
    fetch_pdb_cif,
    ids_seen_in_existing_artifacts,
    parse_atom_site_loop,
    rcsb_candidate_ids,
    round_distance,
)


LANE_ID = "epk_policy_harness"
DEFAULT_PREFIX = "epk_fresh_adp_product_query_context_tripwire_surface"
ADP_PRODUCT_ATOM_NAMES = {
    "PB",
    "O1B",
    "O2B",
    "O3B",
    "PA",
    "O1A",
    "O2A",
    "O3A",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def timestamp_slug(timestamp: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "", timestamp)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def local_geometry_status(row: dict[str, Any], *, cutoff: float) -> bool:
    beta_distance = row.get("nearest_adp_product_phosphate_acceptor_distance_angstrom")
    metal_distance = row.get("nearest_adp_product_phosphate_metal_distance_angstrom")
    return (
        (beta_distance is not None and float(beta_distance) <= cutoff)
        or row.get("local_metal_context_review_only") is True
        or (metal_distance is not None and float(metal_distance) <= cutoff)
    )


def compact_adp_product_summary(
    pdb_id: str,
    *,
    cutoff: float,
    local_metal_cutoff: float,
    max_atoms: int,
) -> dict[str, Any]:
    cif_text = fetch_pdb_cif(pdb_id)
    atoms = parse_atom_site_loop(cif_text)
    if len(atoms) > max_atoms:
        return {
            "pdb_id": pdb_id,
            "fetch_status": "skipped_structure_too_large_for_compact_scan",
            "atom_site_row_count": len(atoms),
            "adp_coordinate_materialized": None,
            "adp_product_phosphate_atom_detected": None,
            "adp_product_phosphate_atom_names_observed": [],
            "nearest_adp_product_phosphate_acceptor_distance_angstrom": None,
            "nearest_adp_product_phosphate_acceptor_relation": (
                "not_reviewed_structure_too_large"
            ),
            "nearest_adp_product_phosphate_metal_distance_angstrom": None,
            "nearest_adp_product_phosphate_metal_code": None,
            "local_metal_context_review_only": False,
            "raw_coordinate_dump_written": False,
        }

    adp_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM" and atom_code(atom) == "ADP"
    ]
    product_atoms = [
        atom for atom in adp_atoms if atom_name(atom) in ADP_PRODUCT_ATOM_NAMES
    ]
    beta_atoms = [atom for atom in product_atoms if atom_name(atom) == "PB"]
    if beta_atoms:
        product_atoms = beta_atoms
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "ATOM"
        and ACCEPTOR_ATOMS.get(atom_code(atom)) == atom_name(atom)
    ]
    metal_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM" and atom_code(atom) in METAL_CODES
    ]

    best_acceptor: dict[str, Any] | None = None
    for product_atom in product_atoms:
        for acceptor in acceptor_atoms:
            try:
                distance = atom_distance(product_atom, acceptor)
            except (KeyError, TypeError, ValueError):
                continue
            hit = {
                "distance": distance,
                "acceptor_residue_code": atom_code(acceptor),
                "acceptor_atom_name": atom_name(acceptor),
                "acceptor_auth_chain": atom_chain(acceptor),
                "acceptor_auth_seq_id": str(
                    acceptor.get("auth_seq_id") or acceptor.get("label_seq_id") or ""
                ),
                "adp_auth_chain": atom_chain(product_atom),
                "adp_product_atom_name": atom_name(product_atom),
            }
            if best_acceptor is None or distance < float(best_acceptor["distance"]):
                best_acceptor = hit

    nearest_metal: dict[str, Any] | None = None
    for product_atom in product_atoms:
        for metal in metal_atoms:
            try:
                distance = atom_distance(product_atom, metal)
            except (KeyError, TypeError, ValueError):
                continue
            hit = {
                "distance": distance,
                "metal_code": atom_code(metal),
                "metal_auth_chain": atom_chain(metal),
                "adp_auth_chain": atom_chain(product_atom),
                "adp_product_atom_name": atom_name(product_atom),
            }
            if nearest_metal is None or distance < float(nearest_metal["distance"]):
                nearest_metal = hit

    acceptor_relation = "none_found"
    if best_acceptor is not None:
        acceptor_relation = (
            "same_auth_chain"
            if best_acceptor.get("acceptor_auth_chain")
            == best_acceptor.get("adp_auth_chain")
            else "cross_auth_chain"
        )
    nearest_acceptor_distance = round_distance(
        float(best_acceptor["distance"]) if best_acceptor else None
    )
    nearest_metal_distance = round_distance(
        float(nearest_metal["distance"]) if nearest_metal else None
    )
    return {
        "pdb_id": pdb_id,
        "fetch_status": "fetched",
        "atom_site_row_count": len(atoms),
        "adp_coordinate_materialized": bool(adp_atoms),
        "adp_atom_count": len(adp_atoms),
        "adp_product_phosphate_atom_detected": bool(product_atoms),
        "adp_product_phosphate_atom_names_observed": sorted(
            {atom_name(atom) for atom in product_atoms}
        ),
        "nearest_adp_product_phosphate_acceptor_distance_angstrom": (
            nearest_acceptor_distance
        ),
        "nearest_adp_product_phosphate_acceptor_relation": acceptor_relation,
        "nearest_adp_product_phosphate_acceptor_residue_code": (
            best_acceptor.get("acceptor_residue_code") if best_acceptor else None
        ),
        "nearest_adp_product_phosphate_acceptor_atom_name": (
            best_acceptor.get("acceptor_atom_name") if best_acceptor else None
        ),
        "nearest_adp_product_phosphate_metal_distance_angstrom": (
            nearest_metal_distance
        ),
        "nearest_adp_product_phosphate_metal_code": (
            nearest_metal.get("metal_code") if nearest_metal else None
        ),
        "local_metal_context_review_only": (
            nearest_metal_distance is not None
            and nearest_metal_distance <= local_metal_cutoff
        ),
        "local_geometry_like_fields_present_review_only": local_geometry_status(
            {
                "nearest_adp_product_phosphate_acceptor_distance_angstrom": (
                    nearest_acceptor_distance
                ),
                "nearest_adp_product_phosphate_metal_distance_angstrom": (
                    nearest_metal_distance
                ),
                "local_metal_context_review_only": (
                    nearest_metal_distance is not None
                    and nearest_metal_distance <= local_metal_cutoff
                ),
            },
            cutoff=cutoff,
        ),
        "raw_coordinate_dump_written": False,
    }


def sort_representative_rows(row: dict[str, Any]) -> tuple[int, float, str]:
    distance = row.get("nearest_adp_product_phosphate_acceptor_distance_angstrom")
    if distance is None:
        distance = 9999.0
    return (
        0 if row.get("local_geometry_like_fields_present_review_only") else 1,
        float(distance),
        str(row.get("pdb_id")),
    )


def build_tranche_row(row: dict[str, Any], *, freshness_status: str) -> dict[str, Any]:
    local_geometry_like = bool(row.get("local_geometry_like_fields_present_review_only"))
    local_metal = bool(row.get("local_metal_context_review_only"))
    return {
        "row_id": f"pdb:{row['pdb_id']}:adp_product_query_context_tripwire",
        "pdb_id": row["pdb_id"],
        "row_role": "fresh_adp_product_query_context_tripwire_review_only",
        "freshness_status": freshness_status,
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": False,
        "ligand_code_from_structure": "ADP",
        "ligand_context": "ADP",
        "product_state_context": True,
        "substrate_acceptor_analog_context": False,
        "split_state_context": False,
        "candidate_specific_source_repair": False,
        "tripwire_review_only_contexts": ["ADP", "PRODUCT_STATE"],
        "tripwire_predictive_status": "review_only_blocked",
        "local_geometry_like_fields_present": local_geometry_like,
        "terminal_gamma_equivalent_geometry": False,
        "terminal_gamma_atom_name": None,
        "nearest_gamma_acceptor_distance_angstrom": None,
        "local_metal_context": local_metal,
        "catalytic_site_locality": local_geometry_like,
        "source_free_acceptor_role_features": False,
        "source_free_acceptor_role_policy_id": None,
        "same_structure_co_materialization": False,
        "coordinate_ligand_materialized_from_structure": True,
        "coordinate_ligand_code_source": "mmcif_atom_site_auth_or_label_comp_id",
        "query_ligand_synonym_used_as_coordinate_ligand": False,
        "source_review_used_for_predictive_feature": False,
        "source_validation_used_for_predictive_feature": False,
        "source_query_used_for_predictive_feature": False,
        "source_text_used_for_predictive_feature": False,
        "structure_title_used_for_predictive_feature": False,
        "source_id_as_predictive_feature": False,
        "candidate_specific_source_repair_used_for_predictive_feature": False,
        "post_hoc_ligand_alias_expansion": False,
        "post_hoc_threshold_selection": False,
        "cross_pdb_split_state_fusion": False,
        "homomeric_chain_choice_as_substrate_mapping": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "threshold_calibrated": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "source_validation_phase": "after_source_free_local_feature_review",
        "source_validation_status": "not_used_for_prediction_review_only_unresolved",
        "post_score_review_status": (
            "fresh_adp_product_query_context_review_only_product_state_blocker"
        ),
        "nearest_adp_product_phosphate_acceptor_distance_angstrom": row.get(
            "nearest_adp_product_phosphate_acceptor_distance_angstrom"
        ),
        "nearest_adp_product_phosphate_acceptor_relation": row.get(
            "nearest_adp_product_phosphate_acceptor_relation"
        ),
        "nearest_adp_product_phosphate_metal_distance_angstrom": row.get(
            "nearest_adp_product_phosphate_metal_distance_angstrom"
        ),
        "nearest_adp_product_phosphate_metal_code": row.get(
            "nearest_adp_product_phosphate_metal_code"
        ),
        "expected_frozen_policy_decision": (
            "review_only_abstain_adp_product_query_context_tripwire"
        ),
    }


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    prefix = f"{args.surface_prefix}_{timestamp_slug(args.timestamp)}"
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    search_surface_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"
    output_paths = {search_surface_path, tranche_path}

    query_ids, query_description, source_description = rcsb_candidate_ids(args)
    seen_ids = (
        set()
        if args.skip_existing_scan
        else ids_seen_in_existing_artifacts(
            root,
            query_ids,
            output_paths,
            max_existing_text_bytes=args.max_existing_text_bytes,
        )
    )
    selected_ids = [pdb_id for pdb_id in query_ids if pdb_id not in seen_ids][
        : args.fresh_limit
    ]
    if not selected_ids:
        raise ValueError("RCSB query returned no fresh candidate ids for this surface")

    scan_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for pdb_id in selected_ids:
        print(f"scanning {pdb_id}", file=sys.stderr, flush=True)
        try:
            scan_rows.append(
                compact_adp_product_summary(
                    pdb_id,
                    cutoff=args.cutoff,
                    local_metal_cutoff=args.local_metal_cutoff,
                    max_atoms=args.max_atoms,
                )
            )
        except Exception as exc:  # pragma: no cover - live network/data failure.
            fetch_failures.append(
                {"pdb_id": pdb_id, "fetch_status": "failed", "error": str(exc)[:200]}
            )

    materialized_rows = [
        row for row in scan_rows if row.get("adp_coordinate_materialized") is True
    ]
    if not materialized_rows:
        raise ValueError("fresh ADP query-context surface had no materialized ADP rows")
    representative_rows = sorted(materialized_rows, key=sort_representative_rows)[
        : args.tranche_rows
    ]
    freshness_status = (
        "existing_artifact_scan_skipped_unverified"
        if args.skip_existing_scan
        else "not_present_in_lane_artifacts_before_this_surface"
    )
    geometry_like_count = sum(
        1
        for row in representative_rows
        if row.get("local_geometry_like_fields_present_review_only")
    )
    observed_codes = ["ADP"] if materialized_rows else []
    source_contexts = [
        {
            "artifact": str(search_surface_path.relative_to(root)),
            "query": query_description,
            "query_mode": args.query_mode,
            "query_ligand_synonyms_review_only": ["ADP"],
            "coordinate_ligand_codes_observed": observed_codes,
            "candidate_id_count_reviewed": len(selected_ids),
            "materialized_adp_count": len(materialized_rows),
            "review_only": True,
        }
    ]

    search_surface = {
        "metadata": {
            "artifact_id": prefix,
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "source": source_description,
            "query": query_description,
            "query_mode": args.query_mode,
            "query_rows_requested": args.query_rows,
            "candidate_ids_frozen_before_local_feature_review": True,
            "source_free_local_features_computed_before_source_validation": True,
            "source_validation_applied_after_local_features": True,
            "source_validation_review_only": True,
            "source_surface_query_contexts_review_only": source_contexts,
            "candidate_id_selection": (
                "query_page_ids_existing_artifact_scan_skipped"
                if args.skip_existing_scan
                else "query_page_ids_not_seen_in_lane_artifacts_before_this_surface"
            ),
            "existing_artifact_scan_scope": "lane_artifacts_and_lane_work_only",
            "candidate_ids_reviewed": selected_ids,
            "candidate_ids_seen_in_existing_lane_artifacts": sorted(seen_ids),
            "candidate_ids_not_seen_in_lane_artifacts_before_this_surface": (
                [] if args.skip_existing_scan else selected_ids
            ),
            "fresh_candidate_count_reviewed": len(scan_rows),
            "fetch_failure_count": len(fetch_failures),
            "adp_materialized_candidate_count": len(materialized_rows),
            "adp_product_local_geometry_like_candidate_count": sum(
                1
                for row in materialized_rows
                if row.get("local_geometry_like_fields_present_review_only")
            ),
            "candidate_distance_cutoff_angstrom": args.cutoff,
            "local_metal_context_review_cutoff_angstrom": args.local_metal_cutoff,
            "search_surface_scope": (
                f"first {len(selected_ids)} selected ids from a bounded ADP "
                f"{args.query_mode} query-context surface; this does not exhaust "
                "all possible RCSB ADP product-state structures"
            ),
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": scan_rows,
        "fetch_failures": fetch_failures,
    }
    write_json(search_surface_path, search_surface)

    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(representative_rows),
            "search_surface_exhausted": False,
            "search_surface_candidate_count_reviewed": len(scan_rows),
            "nonconfounded_candidate_count_within_cutoff": 0,
            "source_query_mode": args.query_mode,
            "chem_comp_id": args.chem_comp_id.upper(),
            "description": (
                "Compact review-only stress tranche for fresh ADP/product-state "
                "query contexts. Candidate ids were frozen before source-free "
                "local feature review; source validation and query text remain "
                "downstream review-only features."
            ),
            "source_artifacts": [
                "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
                str(search_surface_path.relative_to(root)),
            ],
            "source_surface_query_contexts_review_only": source_contexts,
            "query_context_review_only_contract": {
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
            },
            "source_validation_phase_contract": {
                "candidate_ids_frozen_before_local_feature_review": True,
                "source_free_local_features_computed_before_source_validation": True,
                "source_validation_applied_after_local_features": True,
                "source_validation_review_only": True,
                "review_only_source_validation_fields": [
                    "source_validation_status",
                    "source_validation_phase",
                    "post_score_review_status",
                    "source_surface_query_contexts_review_only",
                ],
            },
            "adp_product_query_context_tripwire_contract": {
                "candidate_ids_frozen_before_local_feature_review": True,
                "source_free_local_features_computed_before_source_validation": True,
                "source_validation_review_only": True,
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
                "adp_query_contexts_review_only": True,
                "adp_product_state_rows_review_only": True,
                "local_geometry_like_fields_cannot_override_review_only_context": True,
                "candidate_specific_source_repairs_forbidden_as_predictive_features": True,
                "future_policy_activation_requires_fresh_preregistered_policy": True,
                "future_policy_activation_allowed": False,
                "geometry_like_tripwire_row_count": geometry_like_count,
                "review_only_contexts": ["ADP", "PRODUCT_STATE"],
            },
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": [
            build_tranche_row(row, freshness_status=freshness_status)
            for row in representative_rows
        ],
    }
    write_json(tranche_path, tranche)
    return search_surface_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build compact review-only fresh ADP/product query-context tripwire "
            "surface artifacts."
        )
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--query-mode", choices=("full_text", "chemcomp"), default="full_text")
    parser.add_argument("--query", default="protein kinase substrate ADP magnesium")
    parser.add_argument("--chem-comp-id", default="ADP")
    parser.add_argument("--query-rows", type=int, default=80)
    parser.add_argument("--fresh-limit", type=int, default=12)
    parser.add_argument("--tranche-rows", type=int, default=6)
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--local-metal-cutoff", type=float, default=4.5)
    parser.add_argument("--max-atoms", type=int, default=120000)
    parser.add_argument("--max-existing-text-bytes", type=int, default=2_000_000)
    parser.add_argument("--skip-existing-scan", action="store_true")
    parser.add_argument("--surface-prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.query_rows <= 0:
        raise ValueError("--query-rows must be positive")
    if args.fresh_limit <= 0:
        raise ValueError("--fresh-limit must be positive")
    if args.tranche_rows <= 0:
        raise ValueError("--tranche-rows must be positive")
    if args.max_atoms <= 0:
        raise ValueError("--max-atoms must be positive")
    if args.max_existing_text_bytes <= 0:
        raise ValueError("--max-existing-text-bytes must be positive")
    search_surface_path, tranche_path = build_artifacts(args)
    print(search_surface_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
