#!/usr/bin/env python3
"""Evaluate source-free ORC/MCM guard variants on a compact stress artifact."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LANE_ID = "epk_false_positive_hunter"

VARIANTS = [
    {
        "guard_id": "v0_strict_multisite_entities",
        "source_free": True,
        "min_gamma_mg_sites": 3,
        "min_gamma_mg_chains": 3,
        "min_polymer_chains": 0,
        "min_polymer_entities": 4,
        "rationale": "First-pass guard from the bounded ORC/MCM stress.",
    },
    {
        "guard_id": "v1_relaxed_oligomeric_atpase_chains",
        "source_free": True,
        "min_gamma_mg_sites": 2,
        "min_gamma_mg_chains": 2,
        "min_polymer_chains": 5,
        "min_polymer_entities": 0,
        "rationale": (
            "Blocks ORC motor modules with two or more ATP/Mg sites across "
            "multiple chains while excluding compact two-kinase positive controls."
        ),
    },
    {
        "guard_id": "v2_relaxed_oligomeric_atpase_chains_or_entities",
        "source_free": True,
        "min_gamma_mg_sites": 2,
        "min_gamma_mg_chains": 2,
        "min_polymer_chains": 5,
        "min_polymer_entities": 3,
        "chain_or_entity_floor": True,
        "rationale": (
            "Same as v1, but also allows at least three polymer entities to "
            "cover author-chain/entity edge cases."
        ),
    },
    {
        "guard_id": "v3_too_broad_multisite_only",
        "source_free": True,
        "min_gamma_mg_sites": 2,
        "min_gamma_mg_chains": 2,
        "min_polymer_chains": 0,
        "min_polymer_entities": 0,
        "rationale": "Negative-control variant expected to overblock kinase dimers.",
    },
    {
        "guard_id": "v4_oligomeric_atp_terminals_no_mg_required",
        "source_free": True,
        "min_gamma_mg_sites": 0,
        "min_gamma_mg_chains": 0,
        "min_gamma_terminal_p": 3,
        "min_polymer_chains": 5,
        "min_polymer_entities": 0,
        "rationale": (
            "Covers ORC/OCCM materializer hits where ATP terminal phosphates "
            "are present but Mg is absent or outside the local cutoff."
        ),
    },
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def metric(row: dict[str, Any], key: str) -> int:
    metrics = row.get("source_free_multisite_metrics") or {}
    value = metrics.get(key)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def variant_hit(row: dict[str, Any], variant: dict[str, Any]) -> bool:
    sites = metric(row, "gamma_capable_terminal_p_near_mg_count")
    chains = metric(row, "gamma_capable_terminal_p_near_mg_chain_count")
    terminal_p = metric(row, "gamma_capable_terminal_p_count")
    polymer_chains = metric(row, "polymer_chain_count")
    polymer_entities = metric(row, "polymer_entity_count")
    min_terminal_p = int(variant.get("min_gamma_terminal_p") or 0)
    if min_terminal_p and terminal_p < min_terminal_p:
        return False
    if sites < int(variant["min_gamma_mg_sites"]):
        return False
    if chains < int(variant["min_gamma_mg_chains"]):
        return False
    chain_floor = int(variant.get("min_polymer_chains") or 0)
    entity_floor = int(variant.get("min_polymer_entities") or 0)
    if variant.get("chain_or_entity_floor"):
        return (not chain_floor or polymer_chains >= chain_floor) or (
            not entity_floor or polymer_entities >= entity_floor
        )
    if chain_floor and polymer_chains < chain_floor:
        return False
    if entity_floor and polymer_entities < entity_floor:
        return False
    return True


def decision_for_row(row: dict[str, Any], guard_hit: bool) -> str:
    if not row.get("topology_clear_substrate_mode_hit"):
        return "not_topology_clear_substrate_hit_review_only"
    if row.get("known_epk_positive_input") and guard_hit:
        return "known_epk_positive_lost_to_guard_review_only"
    if row.get("known_epk_positive_input"):
        return "known_epk_positive_retained_review_only"
    if row.get("known_counterexample_input") and guard_hit:
        return "known_counterexample_blocked_by_guard_review_only"
    if row.get("known_counterexample_input"):
        return "known_counterexample_residual_after_guard_review_only"
    if row.get("probable_epk_from_context") is False and guard_hit:
        return "non_epk_topology_clear_hit_blocked_by_guard_review_only"
    if row.get("probable_epk_from_context") is False:
        return "non_epk_topology_clear_residual_after_guard_review_only"
    return "topology_clear_hit_unclassified_review_only"


def summarize_variant(rows: list[dict[str, Any]], variant: dict[str, Any]) -> dict[str, Any]:
    decisions: Counter[str] = Counter()
    row_summaries: list[dict[str, Any]] = []
    for row in rows:
        guard_hit = variant_hit(row, variant)
        decision = decision_for_row(row, guard_hit)
        decisions[decision] += 1
        if row.get("topology_clear_substrate_mode_hit"):
            row_summaries.append(
                {
                    "pdb_id": row.get("pdb_id"),
                    "known_counterexample_input": row.get("known_counterexample_input"),
                    "known_epk_positive_input": row.get("known_epk_positive_input"),
                    "probable_epk_from_context": row.get("probable_epk_from_context"),
                    "deposited_text_role_diagnostic_hit": row.get(
                        "deposited_text_role_diagnostic_hit"
                    ),
                    "guard_hit": guard_hit,
                    "variant_decision": decision,
                    "metrics": row.get("source_free_multisite_metrics"),
                }
            )
    lost_positive_ids = sorted(
        str(row.get("pdb_id"))
        for row in row_summaries
        if row.get("variant_decision") == "known_epk_positive_lost_to_guard_review_only"
    )
    known_residual_ids = sorted(
        str(row.get("pdb_id"))
        for row in row_summaries
        if row.get("variant_decision") == "known_counterexample_residual_after_guard_review_only"
    )
    non_epk_residual_ids = sorted(
        str(row.get("pdb_id"))
        for row in row_summaries
        if row.get("variant_decision")
        == "non_epk_topology_clear_residual_after_guard_review_only"
    )
    status = (
        "passes_current_bounded_guard_variant_review_only"
        if not lost_positive_ids and not known_residual_ids and not non_epk_residual_ids
        else "fails_closed_current_bounded_guard_variant_review_only"
    )
    return {
        **variant,
        "variant_status": status,
        "decision_counts": dict(sorted(decisions.items())),
        "known_epk_positive_lost_pdb_ids": lost_positive_ids,
        "known_counterexample_residual_pdb_ids": known_residual_ids,
        "non_epk_topology_clear_residual_pdb_ids": non_epk_residual_ids,
        "topology_clear_row_summaries": sorted(
            row_summaries, key=lambda row: str(row.get("pdb_id") or "")
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = [
        row
        for row in source.get("guard_stress_rows", []) or []
        if isinstance(row, dict)
    ]
    variant_summaries = [summarize_variant(rows, variant) for variant in VARIANTS]
    passing_variants = [
        summary["guard_id"]
        for summary in variant_summaries
        if summary.get("variant_status") == "passes_current_bounded_guard_variant_review_only"
    ]
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "orc_mcm_guard_variant_sweep",
            "source_artifact": args.input,
            "source_method": source.get("metadata", {}).get("method"),
            "variant_count": len(VARIANTS),
            "passing_guard_variant_ids": passing_variants,
            "reviewed_materializer_row_count": len(rows),
            "topology_clear_substrate_mode_row_count": sum(
                1 for row in rows if row.get("topology_clear_substrate_mode_hit")
            ),
            "source_free_predictive_feature_materialized": True,
            "threshold_calibrated": False,
            "selected_threshold_angstrom": None,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "epk_score_computed": False,
            "external_hard_negative_reaudit_scored": False,
            "raw_coordinate_files_written": False,
        },
        "variant_summaries": variant_summaries,
        "warnings": [
            "Variant sweep reuses compact stress evidence only; it is review-only.",
            "Passing variants are bounded to the source artifact and need broader non-ORC ATPase stress before any production discussion.",
        ],
    }
    Path(args.output).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
