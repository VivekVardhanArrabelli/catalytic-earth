#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from epk_fresh_surface_scan import (  # noqa: E402
    LANE_ID,
    METAL_CODES,
    build_tranche_row,
    compact_structure_summary,
    rcsb_full_text_query,
    sort_representative_rows,
)
from src.catalytic_earth.structure import fetch_pdb_cif, parse_atom_site_loop  # noqa: E402


IGNORED_COMPONENT_CODES = {"DOD", "HOH", "SOL", "WAT", *METAL_CODES}
DEFAULT_QUERIES = (
    "protein kinase AMP-PNP magnesium",
    "protein kinase AMPPNP magnesium",
    "kinase substrate AMP-PNP magnesium",
)
DEFAULT_QUERY_SYNONYMS = ("AMP-PNP", "AMPPNP")
DEFAULT_PRE_FROZEN_COORDINATE_CODES = ("ANP", "ATP")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper()


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = value.strip().upper()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            ordered.append(cleaned)
    return ordered


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def query_context(query: str) -> str:
    return f"full_text {query} sorted by rcsb_accession_info.initial_release_date desc"


def candidate_ids_by_query(queries: list[str], *, query_rows: int) -> dict[str, list[str]]:
    by_query: dict[str, list[str]] = {}
    for query in queries:
        by_query[query] = rcsb_full_text_query(query, rows=query_rows)
    return by_query


def freeze_candidate_ids(
    query_hits: dict[str, list[str]], *, candidate_limit_per_query: int
) -> tuple[list[str], dict[str, list[str]]]:
    ordered: list[str] = []
    candidate_queries: dict[str, list[str]] = {}
    for query, pdb_ids in query_hits.items():
        selected_for_query = 0
        for pdb_id in pdb_ids:
            cleaned = pdb_id.upper()
            candidate_queries.setdefault(cleaned, []).append(query)
            if cleaned not in ordered and selected_for_query < candidate_limit_per_query:
                ordered.append(cleaned)
                selected_for_query += 1
    return ordered, candidate_queries


def coordinate_ligand_inventory(
    pdb_id: str,
    *,
    source_queries: list[str],
    pre_frozen_coordinate_codes: set[str],
    max_atoms: int,
) -> dict[str, Any]:
    cif_text = fetch_pdb_cif(pdb_id)
    atoms = parse_atom_site_loop(cif_text)
    if len(atoms) > max_atoms:
        return {
            "pdb_id": pdb_id,
            "fetch_status": "skipped_structure_too_large_for_compact_scan",
            "atom_site_row_count": len(atoms),
            "source_queries_review_only": [query_context(query) for query in source_queries],
            "all_nonwater_hetatm_component_ids": [],
            "terminal_gamma_ligand_codes_observed": [],
            "prefrozen_terminal_gamma_ligand_codes_observed": [],
            "non_prefrozen_terminal_gamma_ligand_codes_review_only": [],
            "raw_coordinate_dump_written": False,
        }

    hetatm_codes = sorted(
        {
            atom_code(atom)
            for atom in atoms
            if atom.get("group_PDB") == "HETATM"
            and atom_code(atom)
            and atom_code(atom) not in IGNORED_COMPONENT_CODES
        }
    )
    terminal_gamma_codes = sorted(
        {
            atom_code(atom)
            for atom in atoms
            if atom.get("group_PDB") == "HETATM"
            and atom_name(atom) == "PG"
            and atom_code(atom)
            and atom_code(atom) not in IGNORED_COMPONENT_CODES
        }
    )
    prefrozen = sorted(set(terminal_gamma_codes) & pre_frozen_coordinate_codes)
    non_prefrozen = sorted(set(terminal_gamma_codes) - pre_frozen_coordinate_codes)
    return {
        "pdb_id": pdb_id,
        "fetch_status": "fetched",
        "atom_site_row_count": len(atoms),
        "source_queries_review_only": [query_context(query) for query in source_queries],
        "all_nonwater_hetatm_component_ids": hetatm_codes,
        "terminal_gamma_ligand_codes_observed": terminal_gamma_codes,
        "prefrozen_terminal_gamma_ligand_codes_observed": prefrozen,
        "non_prefrozen_terminal_gamma_ligand_codes_review_only": non_prefrozen,
        "raw_coordinate_dump_written": False,
    }


def build_guarded_terminal_rows(
    inventory_rows: list[dict[str, Any]],
    *,
    pre_frozen_coordinate_codes: set[str],
    cutoff: float,
    local_metal_cutoff: float,
    max_atoms: int,
) -> list[dict[str, Any]]:
    terminal_rows: list[dict[str, Any]] = []
    for inventory in inventory_rows:
        if inventory.get("fetch_status") != "fetched":
            continue
        pdb_id = str(inventory.get("pdb_id") or "").upper()
        for ligand_code in inventory.get("prefrozen_terminal_gamma_ligand_codes_observed", []):
            if ligand_code not in pre_frozen_coordinate_codes:
                continue
            row = compact_structure_summary(
                pdb_id,
                ligand_code=ligand_code,
                cutoff=cutoff,
                local_metal_cutoff=local_metal_cutoff,
                max_atoms=max_atoms,
            )
            row["materialization_guard_status"] = (
                "prefrozen_coordinate_ligand_code_admitted_after_inventory"
            )
            row["source_queries_review_only"] = inventory.get(
                "source_queries_review_only", []
            )
            terminal_rows.append(row)
    return terminal_rows


def build_guarded_tranche_row(row: dict[str, Any], *, ligand_code: str) -> dict[str, Any]:
    tranche_row = build_tranche_row(row, ligand_code=ligand_code)
    tranche_row["row_id"] = f"pdb:{row['pdb_id']}:{ligand_code}"
    tranche_row["coordinate_ligand_materialized_from_structure"] = True
    tranche_row["coordinate_ligand_code_source"] = "mmcif_atom_site_auth_or_label_comp_id"
    tranche_row["query_ligand_synonym_used_as_coordinate_ligand"] = False
    tranche_row["post_hoc_ligand_alias_expansion"] = False
    tranche_row["source_query_used_for_predictive_feature"] = False
    tranche_row["materialization_guard_status"] = row.get("materialization_guard_status")
    return tranche_row


def context_observed_codes(
    query: str, inventory_rows: list[dict[str, Any]]
) -> list[str]:
    query_description = query_context(query)
    observed: set[str] = set()
    for row in inventory_rows:
        if query_description not in row.get("source_queries_review_only", []):
            continue
        observed.update(row.get("terminal_gamma_ligand_codes_observed", []))
    return sorted(observed)


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    timestamp_slug = args.timestamp.replace("-", "").replace(":", "").replace("Z", "Z")
    prefix = f"{args.artifact_prefix}_{timestamp_slug}"
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    guard_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"

    queries = unique_preserving_order(args.query or list(DEFAULT_QUERIES))
    pre_frozen_codes = set(
        unique_preserving_order(
            args.pre_frozen_coordinate_code
            or list(DEFAULT_PRE_FROZEN_COORDINATE_CODES)
        )
    )
    query_synonyms = unique_preserving_order(
        args.query_ligand_synonym or list(DEFAULT_QUERY_SYNONYMS)
    )
    query_hits = candidate_ids_by_query(queries, query_rows=args.query_rows)
    candidate_ids, candidate_queries = freeze_candidate_ids(
        query_hits, candidate_limit_per_query=args.candidate_limit_per_query
    )
    if not candidate_ids:
        raise ValueError("AMP-PNP/AMPPNP materialization guard found no candidate ids")

    inventory_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for pdb_id in candidate_ids:
        print(f"inventorying {pdb_id}", file=sys.stderr, flush=True)
        try:
            inventory_rows.append(
                coordinate_ligand_inventory(
                    pdb_id,
                    source_queries=candidate_queries.get(pdb_id, []),
                    pre_frozen_coordinate_codes=pre_frozen_codes,
                    max_atoms=args.max_atoms,
                )
            )
        except Exception as exc:  # pragma: no cover - live network/data failure.
            fetch_failures.append(
                {"pdb_id": pdb_id, "fetch_status": "failed", "error": str(exc)[:200]}
            )

    terminal_rows = build_guarded_terminal_rows(
        inventory_rows,
        pre_frozen_coordinate_codes=pre_frozen_codes,
        cutoff=args.cutoff,
        local_metal_cutoff=args.local_metal_cutoff,
        max_atoms=args.max_atoms,
    )
    observed_codes = sorted(
        {
            code
            for row in inventory_rows
            for code in row.get("terminal_gamma_ligand_codes_observed", [])
        }
    )
    alias_map_blockers = sorted(set(observed_codes) - pre_frozen_codes)
    admitted_rows = [
        row
        for row in terminal_rows
        if row.get("terminal_gamma_atom_detected") is True
        and row.get("gamma_ligand_code") in pre_frozen_codes
    ]
    representative_rows = sorted(admitted_rows, key=sort_representative_rows)[
        : args.tranche_rows
    ]
    if not representative_rows:
        raise ValueError(
            "materialization guard found no pre-frozen coordinate terminal-gamma rows"
        )

    source_contexts = [
        {
            "artifact": str(guard_path.relative_to(root)),
            "query": query_context(query),
            "query_mode": "full_text",
            "query_ligand_synonyms_review_only": query_synonyms,
            "coordinate_ligand_codes_observed": context_observed_codes(
                query, inventory_rows
            ),
            "review_only": True,
        }
        for query in queries
    ]
    nonconfounded_count = sum(
        1
        for row in admitted_rows
        if row.get("nonconfounded_inter_auth_chain_within_cutoff") is True
    )

    guard_artifact = {
        "metadata": {
            "artifact_id": prefix,
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "query_id": args.query_id,
            "query_mode": "full_text",
            "queries": [query_context(query) for query in queries],
            "query_ligand_synonyms_review_only": query_synonyms,
            "candidate_ids_frozen_before_coordinate_ligand_inventory": True,
            "coordinate_ligand_codes_inventoried_before_local_feature_review": True,
            "pre_frozen_coordinate_ligand_codes": sorted(pre_frozen_codes),
            "coordinate_ligand_codes_observed": observed_codes,
            "alias_map_blockers_review_only": alias_map_blockers,
            "terminal_gamma_candidate_count_reviewed": len(admitted_rows),
            "nonconfounded_candidate_count_within_cutoff": nonconfounded_count,
            "candidate_ids_reviewed": candidate_ids,
            "candidate_id_query_hits_review_only": {
                pdb_id: [query_context(query) for query in candidate_queries.get(pdb_id, [])]
                for pdb_id in candidate_ids
            },
            "freshness_status": "bounded_live_query_page_materialization_guard",
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": inventory_rows,
        "fetch_failures": fetch_failures,
    }
    write_json(guard_path, guard_artifact)

    tranche_rows = [
        build_guarded_tranche_row(row, ligand_code=str(row["gamma_ligand_code"]))
        for row in representative_rows
    ]
    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(tranche_rows),
            "search_surface_exhausted": False,
            "search_surface_candidate_count_reviewed": len(inventory_rows),
            "nonconfounded_candidate_count_within_cutoff": nonconfounded_count,
            "terminal_gamma_required_for_tranche": True,
            "terminal_gamma_atom_name_required": "PG",
            "terminal_gamma_candidate_count_reviewed": len(admitted_rows),
            "description": (
                "Review-only AMP-PNP/AMPPNP query-context materialization guard. "
                "Candidate ids were frozen before coordinate ligand inventory; only "
                "pre-frozen coordinate component ids are admitted to terminal-gamma "
                "evaluation."
            ),
            "source_artifacts": [
                "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
                str(guard_path.relative_to(root)),
            ],
            "source_surface_query_contexts_review_only": source_contexts,
            "coordinate_ligand_codes_observed": observed_codes,
            "alias_map_blockers_review_only": alias_map_blockers,
            "query_context_review_only_contract": {
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
            },
            "coordinate_ligand_materialization_guard": {
                "coordinate_ligand_codes_inventoried_before_local_feature_review": True,
                "query_synonyms_review_only": True,
                "post_hoc_ligand_alias_expansion_forbidden": True,
                "terminal_gamma_rows_limited_to_pre_frozen_coordinate_codes": True,
                "non_prefrozen_materializations_recorded_as_review_only_blockers": True,
                "pre_frozen_coordinate_ligand_codes": sorted(pre_frozen_codes),
                "query_ligand_synonyms_review_only": query_synonyms,
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
                ],
            },
            "topology_review_contract": {
                "topology_status_required": True,
                "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                "role_policy_status": "none_accepted_in_policy_v0",
            },
        },
        "rows": tranche_rows,
    }
    write_json(tranche_path, tranche)
    return guard_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an AMP-PNP query-context coordinate ligand materialization guard."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--query", action="append")
    parser.add_argument("--query-rows", type=int, default=18)
    parser.add_argument("--candidate-limit-per-query", type=int, default=8)
    parser.add_argument("--tranche-rows", type=int, default=8)
    parser.add_argument(
        "--pre-frozen-coordinate-code",
        action="append",
    )
    parser.add_argument(
        "--query-ligand-synonym",
        action="append",
    )
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--local-metal-cutoff", type=float, default=4.5)
    parser.add_argument("--max-atoms", type=int, default=120000)
    parser.add_argument(
        "--artifact-prefix",
        default="epk_amp_pnp_query_context_coordinate_ligand_materialization_guard",
    )
    parser.add_argument(
        "--query-id",
        default="epk_amp_pnp_query_context_coordinate_ligand_materialization_guard_v1_review_only",
    )
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.query_rows <= 0:
        raise ValueError("--query-rows must be positive")
    if args.candidate_limit_per_query <= 0:
        raise ValueError("--candidate-limit-per-query must be positive")
    if args.tranche_rows <= 0:
        raise ValueError("--tranche-rows must be positive")
    if args.cutoff <= 0:
        raise ValueError("--cutoff must be positive")
    if args.local_metal_cutoff <= 0:
        raise ValueError("--local-metal-cutoff must be positive")
    if args.max_atoms <= 0:
        raise ValueError("--max-atoms must be positive")
    guard_path, tranche_path = build_artifacts(args)
    print(guard_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
