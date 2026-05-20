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
    LANE_ID,
    build_tranche_row,
    compact_structure_summary,
    sort_representative_rows,
)


DEFAULT_SOURCE_GLOB = (
    "epk_amp_pnp_query_context_coordinate_ligand_materialization_guard_*.json"
)
DEFAULT_PREFIX = (
    "epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control"
)
DEFAULT_QUERY_ID = (
    "epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_v1_review_only"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def latest_source_guard_artifact(root: Path) -> Path:
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    candidates = [
        path
        for path in artifact_dir.glob(DEFAULT_SOURCE_GLOB)
        if not path.name.endswith("_tranche.json")
        and not path.name.endswith("_result.json")
    ]
    if not candidates:
        raise ValueError("no AMP-PNP materialization guard artifact found")
    return sorted(candidates)[-1]


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = str(value).strip().upper()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            ordered.append(cleaned)
    return ordered


def timestamp_slug(timestamp: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "", timestamp)


def blocker_observations(
    guard_artifact: dict[str, Any], blocker_codes: set[str]
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for row in guard_artifact.get("rows", []):
        pdb_id = str(row.get("pdb_id") or "").upper()
        if not pdb_id:
            continue
        source_queries = [
            str(query)
            for query in row.get("source_queries_review_only", [])
            if str(query).strip()
        ]
        for code in row.get("non_prefrozen_terminal_gamma_ligand_codes_review_only", []):
            ligand_code = str(code).upper()
            if ligand_code not in blocker_codes:
                continue
            observations.append(
                {
                    "pdb_id": pdb_id,
                    "ligand_code": ligand_code,
                    "source_queries_review_only": source_queries,
                    "source_inventory_status": "nonprefrozen_terminal_gamma_blocker",
                }
            )
    return observations


def select_observations(
    observations: list[dict[str, Any]],
    *,
    blocker_codes: list[str],
    tranche_rows: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    selected_keys: set[tuple[str, str]] = set()
    for blocker_code in blocker_codes:
        for observation in observations:
            key = (observation["pdb_id"], observation["ligand_code"])
            if observation["ligand_code"] == blocker_code and key not in selected_keys:
                selected.append(observation)
                selected_keys.add(key)
                break
    for observation in observations:
        if len(selected) >= tranche_rows:
            break
        key = (observation["pdb_id"], observation["ligand_code"])
        if key in selected_keys:
            continue
        selected.append(observation)
        selected_keys.add(key)
    return selected


def context_observed_codes(
    query: str, rows: list[dict[str, Any]], *, selected_only: bool
) -> list[str]:
    observed: set[str] = set()
    for row in rows:
        if query not in row.get("source_queries_review_only", []):
            continue
        if selected_only and row.get("selected_for_tranche") is not True:
            continue
        observed.add(str(row.get("ligand_code") or "").upper())
    return sorted(code for code in observed if code)


def build_blocker_tranche_row(summary: dict[str, Any]) -> dict[str, Any]:
    ligand_code = str(summary["ligand_code"]).upper()
    row = build_tranche_row(summary, ligand_code=ligand_code)
    row["row_id"] = f"pdb:{summary['pdb_id']}:{ligand_code}:nonprefrozen_alias_blocker"
    row["row_role"] = "nonprefrozen_alias_blocker_negative_control_review_only"
    row["freshness_status"] = "bounded_prior_materialization_guard_blocker"
    row["ligand_code_from_structure"] = ligand_code
    row["coordinate_ligand_materialized_from_structure"] = True
    row["coordinate_ligand_code_source"] = "mmcif_atom_site_auth_or_label_comp_id"
    row["query_ligand_synonym_used_as_coordinate_ligand"] = False
    row["post_hoc_ligand_alias_expansion"] = False
    row["source_query_used_for_predictive_feature"] = False
    row["materialization_guard_status"] = (
        "nonprefrozen_coordinate_ligand_code_blocked_review_only"
    )
    row["source_queries_review_only"] = summary.get("source_queries_review_only", [])
    row["source_free_acceptor_role_features"] = False
    row["source_free_acceptor_role_policy_id"] = None
    row["same_structure_co_materialization"] = False
    row["post_score_review_status"] = (
        "nonprefrozen_alias_blocker_review_only_not_admitted"
    )
    row["expected_frozen_policy_decision"] = (
        "review_only_abstain_nonprefrozen_alias_blocker"
    )
    return row


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    source_guard_path = (
        Path(args.source_guard_artifact).resolve()
        if args.source_guard_artifact
        else latest_source_guard_artifact(root)
    )
    guard_artifact = load_json(source_guard_path)
    guard_metadata = guard_artifact.get("metadata", {})

    blocker_codes = unique_preserving_order(
        args.blocker_code or guard_metadata.get("alias_map_blockers_review_only", [])
    )
    if not blocker_codes:
        raise ValueError("no review-only alias-map blocker codes available")
    pre_frozen_codes = unique_preserving_order(
        args.pre_frozen_coordinate_code
        or guard_metadata.get("pre_frozen_coordinate_ligand_codes", [])
    )
    query_synonyms = unique_preserving_order(
        args.query_ligand_synonym
        or guard_metadata.get("query_ligand_synonyms_review_only", [])
    )
    queries = [
        str(query)
        for query in guard_metadata.get("queries", [])
        if str(query).strip()
    ]
    if not pre_frozen_codes:
        raise ValueError("source guard metadata has no pre-frozen coordinate codes")
    if not query_synonyms:
        raise ValueError("source guard metadata has no query ligand synonyms")
    if not queries:
        raise ValueError("source guard metadata has no query contexts")

    observations = blocker_observations(guard_artifact, set(blocker_codes))
    if not observations:
        raise ValueError("source guard artifact has no nonprefrozen blocker observations")
    selected_observations = select_observations(
        observations,
        blocker_codes=blocker_codes,
        tranche_rows=args.tranche_rows,
    )
    selected_keys = {
        (row["pdb_id"], row["ligand_code"]) for row in selected_observations
    }

    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    prefix = f"{args.artifact_prefix}_{timestamp_slug(args.timestamp)}"
    negative_control_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"

    compact_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for observation in observations:
        selected = (observation["pdb_id"], observation["ligand_code"]) in selected_keys
        if not selected and args.scan_selected_only:
            compact_rows.append({**observation, "selected_for_tranche": False})
            continue
        print(
            f"scanning blocker {observation['pdb_id']} {observation['ligand_code']}",
            file=sys.stderr,
            flush=True,
        )
        try:
            summary = compact_structure_summary(
                observation["pdb_id"],
                ligand_code=observation["ligand_code"],
                cutoff=args.cutoff,
                local_metal_cutoff=args.local_metal_cutoff,
                max_atoms=args.max_atoms,
            )
            summary.update(observation)
            summary["selected_for_tranche"] = selected
            summary["raw_coordinate_dump_written"] = False
            compact_rows.append(summary)
        except Exception as exc:  # pragma: no cover - live network/data failure.
            fetch_failures.append(
                {
                    "pdb_id": observation["pdb_id"],
                    "ligand_code": observation["ligand_code"],
                    "fetch_status": "failed",
                    "error": str(exc)[:200],
                }
            )

    tranche_source_rows = [
        row
        for row in compact_rows
        if row.get("selected_for_tranche") is True
        and row.get("terminal_gamma_atom_detected") is True
    ]
    if not tranche_source_rows:
        raise ValueError("no selected blocker rows retained terminal-gamma PG geometry")
    selected_codes = sorted({str(row["ligand_code"]).upper() for row in tranche_source_rows})
    missing_codes = sorted(set(blocker_codes) - set(selected_codes))
    if missing_codes:
        raise ValueError(
            "selected negative-control rows must cover all blocker codes: "
            f"{missing_codes}"
        )
    tranche_source_rows = sorted(tranche_source_rows, key=sort_representative_rows)[
        : args.tranche_rows
    ]
    nonconfounded_count = sum(
        1
        for row in tranche_source_rows
        if row.get("nonconfounded_inter_auth_chain_within_cutoff") is True
    )

    source_contexts = [
        {
            "artifact": str(negative_control_path.relative_to(root)),
            "source_guard_artifact": str(source_guard_path.relative_to(root)),
            "query": query,
            "query_mode": "full_text",
            "query_ligand_synonyms_review_only": query_synonyms,
            "coordinate_ligand_codes_observed": context_observed_codes(
                query, compact_rows, selected_only=False
            ),
            "review_only": True,
        }
        for query in queries
    ]
    negative_control_artifact = {
        "metadata": {
            "artifact_id": prefix,
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "query_id": args.query_id,
            "source_guard_artifact": str(source_guard_path.relative_to(root)),
            "source_guard_query_id": guard_metadata.get("query_id"),
            "candidate_ids_frozen_before_negative_control_selection": True,
            "blocker_codes_observed_in_coordinate_inventory": True,
            "blocker_codes_review_only": True,
            "blocker_codes_not_in_frozen_policy_ligand_map": True,
            "query_text_not_coordinate_ligand_materialization": True,
            "terminal_gamma_rows_for_blocker_codes_excluded_from_policy_admission": True,
            "pre_frozen_coordinate_ligand_codes": pre_frozen_codes,
            "nonprefrozen_coordinate_ligand_codes_review_only": blocker_codes,
            "coordinate_ligand_codes_observed": selected_codes,
            "alias_map_blockers_review_only": blocker_codes,
            "query_ligand_synonyms_review_only": query_synonyms,
            "source_surface_query_contexts_review_only": source_contexts,
            "blocker_observation_count": len(observations),
            "selected_blocker_row_count": len(tranche_source_rows),
            "nonconfounded_candidate_count_within_cutoff": nonconfounded_count,
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": compact_rows,
        "fetch_failures": fetch_failures,
    }
    write_json(negative_control_path, negative_control_artifact)

    tranche_rows = [build_blocker_tranche_row(row) for row in tranche_source_rows]
    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(tranche_rows),
            "search_surface_exhausted": False,
            "search_surface_candidate_count_reviewed": len(observations),
            "nonconfounded_candidate_count_within_cutoff": nonconfounded_count,
            "terminal_gamma_required_for_tranche": True,
            "terminal_gamma_atom_name_required": "PG",
            "terminal_gamma_candidate_count_reviewed": len(tranche_rows),
            "description": (
                "Review-only GNP/GTP negative-control tranche from AMP-PNP query "
                "materialization blockers. Rows are terminal-gamma coordinate "
                "materializations but are non-prefrozen and cannot be admitted by "
                "query wording or alias expansion."
            ),
            "source_artifacts": [
                "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
                str(source_guard_path.relative_to(root)),
                str(negative_control_path.relative_to(root)),
            ],
            "source_surface_query_contexts_review_only": source_contexts,
            "coordinate_ligand_codes_observed": selected_codes,
            "alias_map_blockers_review_only": blocker_codes,
            "query_context_review_only_contract": {
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
            },
            "nonprefrozen_alias_blocker_negative_control_contract": {
                "candidate_ids_frozen_before_negative_control_selection": True,
                "blocker_codes_observed_in_coordinate_inventory": True,
                "blocker_codes_review_only": True,
                "blocker_codes_not_in_frozen_policy_ligand_map": True,
                "query_text_not_coordinate_ligand_materialization": True,
                "terminal_gamma_rows_for_blocker_codes_excluded_from_policy_admission": True,
                "pre_frozen_coordinate_ligand_codes": pre_frozen_codes,
                "nonprefrozen_coordinate_ligand_codes_review_only": blocker_codes,
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
    return negative_control_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a compact review-only GNP/GTP nonprefrozen alias-blocker "
            "negative-control tranche."
        )
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--source-guard-artifact")
    parser.add_argument("--blocker-code", action="append")
    parser.add_argument("--pre-frozen-coordinate-code", action="append")
    parser.add_argument("--query-ligand-synonym", action="append")
    parser.add_argument("--tranche-rows", type=int, default=8)
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--local-metal-cutoff", type=float, default=4.5)
    parser.add_argument("--max-atoms", type=int, default=120000)
    parser.add_argument("--scan-selected-only", action="store_true")
    parser.add_argument("--artifact-prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--query-id", default=DEFAULT_QUERY_ID)
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.tranche_rows <= 0:
        raise ValueError("--tranche-rows must be positive")
    if args.cutoff <= 0:
        raise ValueError("--cutoff must be positive")
    if args.local_metal_cutoff <= 0:
        raise ValueError("--local-metal-cutoff must be positive")
    if args.max_atoms <= 0:
        raise ValueError("--max-atoms must be positive")
    negative_control_path, tranche_path = build_artifacts(args)
    print(negative_control_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
