#!/usr/bin/env python3
"""Stress v4 overblock risk on high-order kinase and non-ORC ATPase surfaces.

The helper keeps the search bounded, fetches mmCIF text in memory only, and
stores compact review evidence. It does not write raw coordinates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import requests

import atpase_substrate_mode_stress as base
import auth_namespace_edge_case_stress as ns
import orc_mcm_guard_variant_sweep as variants
import orc_mcm_multisite_guard_stress as orc
import v4_component_no_mg_kinase_dimer_stress as prior


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
MAX_UNIQUE_IDS = 460
HIGH_ORDER_MIN_GAMMA_TERMINAL_P = 3
HIGH_ORDER_MIN_POLYMER_CHAINS = 5

PRIOR_KNOWN_EPK_POSITIVE_IDS = {
    "1IR3",
    "1O6K",
    "1O6L",
    "2PHK",
    "3TM0",
    "5HVK",
    "6Z3R",
    "8OXM",
    "8OXO",
    "9UUR",
    "9UUX",
}
PRIOR_ORC_COUNTEREXAMPLE_IDS = {
    "5UJ7",
    "5UJM",
    "6RQC",
    "7JGR",
    "7JGS",
    "7JK2",
    "7JK3",
    "7JK4",
    "7JPO",
    "7TJF",
    "7TJH",
    "9BCX",
    "9GJW",
    "9I3I",
}
PRESSURE_IDS = {"7CAG", "8BMS", "9L3M", "9L3U", "7ZE5"}

EPK_COMPONENT_TEXT_QUERIES = [
    {"name": "protein_kinase_atp_0", "phrase": "protein kinase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "protein_kinase_atp_90", "phrase": "protein kinase", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "protein_kinase_anp_0", "phrase": "protein kinase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "protein_kinase_anp_90", "phrase": "protein kinase", "ligand": "ANP", "start": 90, "rows": 45},
    {"name": "eukaryotic_kinase_atp", "phrase": "eukaryotic protein kinase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "eukaryotic_kinase_anp", "phrase": "eukaryotic protein kinase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "map_kinase_atp", "phrase": "MAP kinase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "map_kinase_anp", "phrase": "MAP kinase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "cyclin_dependent_kinase_atp", "phrase": "cyclin-dependent kinase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "cyclin_dependent_kinase_anp", "phrase": "cyclin-dependent kinase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "receptor_tyrosine_kinase_atp", "phrase": "receptor tyrosine kinase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "receptor_tyrosine_kinase_anp", "phrase": "receptor tyrosine kinase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "mtor_kinase_atp", "phrase": "mTOR kinase", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "mtor_kinase_anp", "phrase": "mTOR kinase", "ligand": "ANP", "start": 0, "rows": 25},
]

NON_ORC_ATPASE_COMPONENT_TEXT_QUERIES = [
    {"name": "aaa_atpase_atp", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "aaa_atpase_anp", "phrase": "AAA+ ATPase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "proteasome_atpase_atp", "phrase": "proteasome ATPase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "proteasome_atpase_anp", "phrase": "proteasome ATPase", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "clamp_loader_atp", "phrase": "clamp loader ATP", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "clamp_loader_anp", "phrase": "clamp loader ATP", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "helicase_atp", "phrase": "helicase ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "helicase_anp", "phrase": "helicase ATP", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "dynein_atp", "phrase": "dynein ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "dynein_anp", "phrase": "dynein ATP", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "abc_transporter_atp", "phrase": "ABC transporter ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "abc_transporter_anp", "phrase": "ABC transporter ATP", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "vcp_p97_atp", "phrase": "VCP p97 ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "vcp_p97_anp", "phrase": "VCP p97 ATP", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "replication_factor_c_atp", "phrase": "replication factor C ATP", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "replication_factor_c_anp", "phrase": "replication factor C ATP", "ligand": "ANP", "start": 0, "rows": 35},
]

KINASE_ENTITY_TOKENS = [
    "protein kinase",
    "tyrosine kinase",
    "serine/threonine kinase",
    "serine/threonine-protein kinase",
    "cyclin-dependent kinase",
    "mitogen-activated protein kinase",
    "casein kinase",
    "cAMP-dependent protein kinase",
    "raf kinase",
    "aurora kinase",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def component_full_text_query(phrase: str, ligand: str, start: int, rows: int) -> list[str]:
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "full_text",
                    "parameters": {"value": phrase},
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                        "operator": "exact_match",
                        "value": ligand,
                    },
                },
            ],
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": start, "rows": rows},
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "score", "direction": "desc"}],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=query, timeout=30)
    if response.status_code == 204 or not response.text.strip():
        return []
    response.raise_for_status()
    payload = response.json()
    return [row["identifier"].upper() for row in payload.get("result_set", [])]


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    fixed_ordered_ids: list[str] = []
    surface_ordered_ids: dict[str, list[str]] = {
        "epk_component_text": [],
        "non_orc_atpase_component_text": [],
    }
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}

    fixed_controls = sorted(
        PRIOR_KNOWN_EPK_POSITIVE_IDS | PRIOR_ORC_COUNTEREXAMPLE_IDS | PRESSURE_IDS
    )
    for pdb_id in reversed(fixed_controls):
        id_to_queries[pdb_id].append("fixed_prior_positive_counterexample_or_pressure_control")
        fixed_ordered_ids.insert(0, pdb_id)

    for surface, queries in [
        ("epk_component_text", EPK_COMPONENT_TEXT_QUERIES),
        ("non_orc_atpase_component_text", NON_ORC_ATPASE_COMPONENT_TEXT_QUERIES),
    ]:
        for query in queries:
            name = str(query["name"])
            try:
                ids = component_full_text_query(
                    str(query["phrase"]),
                    str(query["ligand"]),
                    int(query["start"]),
                    int(query["rows"]),
                )
                query_counts[name] = len(ids)
            except Exception as exc:  # pragma: no cover - network evidence
                ids = []
                query_counts[name] = 0
                query_errors[name] = repr(exc)
            for pdb_id in ids:
                id_to_queries[pdb_id].append(f"{surface}:{name}:{query['phrase']}:{query['ligand']}")
                if pdb_id not in surface_ordered_ids[surface]:
                    surface_ordered_ids[surface].append(pdb_id)
            time.sleep(0.12)

    remaining = max(MAX_UNIQUE_IDS - len(fixed_ordered_ids), 0)
    epk_quota = remaining // 2
    atpase_quota = remaining - epk_quota
    ordered_ids = list(fixed_ordered_ids)
    for pdb_id in surface_ordered_ids["epk_component_text"][:epk_quota]:
        if pdb_id not in ordered_ids:
            ordered_ids.append(pdb_id)
    for pdb_id in surface_ordered_ids["non_orc_atpase_component_text"][:atpase_quota]:
        if pdb_id not in ordered_ids:
            ordered_ids.append(pdb_id)

    query_counts["balanced_fixed_control_ids"] = len(fixed_ordered_ids)
    query_counts["balanced_epk_component_text_unique_ids_available"] = len(
        surface_ordered_ids["epk_component_text"]
    )
    query_counts["balanced_epk_component_text_unique_ids_selected_quota"] = epk_quota
    query_counts["balanced_non_orc_atpase_component_text_unique_ids_available"] = len(
        surface_ordered_ids["non_orc_atpase_component_text"]
    )
    query_counts["balanced_non_orc_atpase_component_text_unique_ids_selected_quota"] = atpase_quota
    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_counts


def entity_kinase_tokens(entity_descriptions: list[str]) -> list[str]:
    lower = " ".join(entity_descriptions).lower()
    return sorted(token for token in KINASE_ENTITY_TOKENS if token.lower() in lower)


def query_surface_groups(query_names: list[str]) -> list[str]:
    groups = set()
    for name in query_names:
        if name.startswith("epk_component_text:"):
            groups.add("epk_component_text")
        if name.startswith("non_orc_atpase_component_text:"):
            groups.add("non_orc_atpase_component_text")
        if name == "fixed_prior_positive_counterexample_or_pressure_control":
            groups.add("fixed_control")
    return sorted(groups)


def high_order_v4_feature(metrics: dict[str, Any]) -> bool:
    try:
        terminal_p = int(metrics.get("gamma_capable_terminal_p_count") or 0)
        polymer_chains = int(metrics.get("polymer_chain_count") or 0)
    except (TypeError, ValueError):
        return False
    return (
        terminal_p >= HIGH_ORDER_MIN_GAMMA_TERMINAL_P
        and polymer_chains >= HIGH_ORDER_MIN_POLYMER_CHAINS
    )


def v4_hit(metrics: dict[str, Any]) -> bool:
    variant = next(
        variant
        for variant in variants.VARIANTS
        if variant["guard_id"] == "v4_oligomeric_atp_terminals_no_mg_required"
    )
    return variants.variant_hit({"source_free_multisite_metrics": metrics}, variant)


def fetch_review_row(
    pdb_id: str,
    index: int,
    id_to_queries: dict[str, list[str]],
    *,
    retry: bool = False,
) -> tuple[dict[str, Any], str]:
    cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
    entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
    entity_descriptions = orc.entity_descriptions_from_cif(cif_text)
    text = prior.context_text(entry_payload, entity_descriptions)
    metrics = orc.source_free_multisite_metrics(atoms)
    groups = query_surface_groups(id_to_queries.get(pdb_id, []))
    role_tokens = orc.deposited_role_tokens(text)
    probable_epk = orc.probable_epk(pdb_id, text)
    kinase_tokens = entity_kinase_tokens(entity_descriptions)
    high_order = high_order_v4_feature(metrics)
    fixed_positive = pdb_id in PRIOR_KNOWN_EPK_POSITIVE_IDS
    fixed_counterexample = pdb_id in PRIOR_ORC_COUNTEREXAMPLE_IDS
    epk_query_candidate = (
        "epk_component_text" in groups
        and high_order
        and probable_epk
        and not fixed_positive
    )
    non_orc_atpase_candidate = (
        "non_orc_atpase_component_text" in groups
        and high_order
        and not probable_epk
        and not role_tokens
    )
    row = {
        "pdb_id": pdb_id,
        "surface_order": index,
        "query_names": id_to_queries.get(pdb_id, []),
        "query_surface_groups": groups,
        "title": entry_payload.get("struct", {}).get("title", ""),
        "keywords": entry_payload.get("struct_keywords", {}),
        "entity_descriptions_compact": entity_descriptions[:14],
        "entity_kinase_tokens": kinase_tokens,
        "known_epk_positive_input": fixed_positive,
        "known_orc_counterexample_input": fixed_counterexample,
        "known_pressure_id_input": pdb_id in PRESSURE_IDS,
        "probable_epk_from_context": probable_epk,
        "deposited_orc_mcm_role_tokens": role_tokens,
        "reviewed": True,
        "retry_fetch_after_initial_error": retry,
        **parse_meta,
        "component_state": prior.compact_nonpolymer_counts(atoms),
        "source_free_multisite_metrics": metrics,
        "high_order_v4_feature": high_order,
        "v4_oligomeric_atp_terminals_no_mg_required_hit": v4_hit(metrics),
        "high_order_epk_query_candidate_not_prior_seed": epk_query_candidate,
        "non_orc_high_order_atpase_query_candidate": non_orc_atpase_candidate,
    }
    return row, cif_text


def summarize_materializer_rows(
    materializer: dict[str, Any],
    rows_by_pdb: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        entry = rows_by_pdb.get(pdb_id, {})
        hits = [
            hit
            for hit in row.get("heteromeric_candidate_hits", []) or []
            if isinstance(hit, dict)
        ]
        substrate_hits = [hit for hit in hits if prior.substrate_mode_hit(hit)]
        flags = orc.topology_flags(substrate_hits)
        topology_clear = bool(substrate_hits) and not flags["topology_ambiguity_counteraxis_hit"]
        probable_epk = bool(entry.get("probable_epk_from_context"))
        high_order_epk = bool(entry.get("high_order_epk_query_candidate_not_prior_seed"))
        non_orc_atpase = bool(entry.get("non_orc_high_order_atpase_query_candidate"))
        fixed_positive = bool(entry.get("known_epk_positive_input"))
        fixed_orc_counterexample = bool(entry.get("known_orc_counterexample_input"))
        guard_hit = bool(entry.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))

        if high_order_epk and topology_clear and guard_hit:
            decision = "high_order_epk_overblock_risk_by_v4_review_only"
        elif high_order_epk and topology_clear:
            decision = "high_order_epk_current_hit_retained_by_v4_review_only"
        elif fixed_positive and topology_clear and guard_hit:
            decision = "fixed_known_epk_positive_lost_to_v4_review_only"
        elif fixed_positive and topology_clear:
            decision = "fixed_known_epk_positive_retained_by_v4_review_only"
        elif non_orc_atpase and topology_clear and guard_hit:
            decision = "non_orc_current_rule_counterexample_blocked_by_v4_review_only"
        elif non_orc_atpase and topology_clear:
            decision = "non_orc_current_rule_counterexample_residual_after_v4_review_only"
        elif fixed_orc_counterexample and topology_clear and guard_hit:
            decision = "fixed_orc_counterexample_blocked_by_v4_review_only"
        elif fixed_orc_counterexample and topology_clear:
            decision = "fixed_orc_counterexample_residual_after_v4_review_only"
        elif topology_clear and not probable_epk and guard_hit:
            decision = "non_epk_topology_clear_hit_blocked_by_v4_review_only"
        elif topology_clear and not probable_epk:
            decision = "non_epk_topology_clear_hit_residual_after_v4_review_only"
        elif substrate_hits and flags["topology_ambiguity_counteraxis_hit"]:
            decision = "substrate_mode_hit_blocked_by_existing_topology_review_only"
        elif substrate_hits:
            decision = "substrate_mode_hit_unclassified_review_only"
        else:
            decision = "no_substrate_mode_materializer_hit_review_only"

        summaries.append(
            {
                "pdb_id": pdb_id,
                "query_names": entry.get("query_names", []),
                "query_surface_groups": entry.get("query_surface_groups", []),
                "known_epk_positive_input": fixed_positive,
                "known_orc_counterexample_input": fixed_orc_counterexample,
                "known_pressure_id_input": entry.get("known_pressure_id_input"),
                "probable_epk_from_context": entry.get("probable_epk_from_context"),
                "entity_kinase_tokens": entry.get("entity_kinase_tokens", []),
                "deposited_orc_mcm_role_tokens": entry.get("deposited_orc_mcm_role_tokens", []),
                "high_order_v4_feature": entry.get("high_order_v4_feature"),
                "high_order_epk_query_candidate_not_prior_seed": high_order_epk,
                "non_orc_high_order_atpase_query_candidate": non_orc_atpase,
                "component_state": entry.get("component_state", {}),
                "candidate_status": row.get("candidate_status"),
                "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
                "substrate_mode_materializer_hit_count": len(substrate_hits),
                "topology_clear_substrate_mode_hit": topology_clear,
                **flags,
                "v4_oligomeric_atp_terminals_no_mg_required_hit": guard_hit,
                "v4_high_order_stress_decision": decision,
                "substrate_mode_materializer_hits": substrate_hits[:10],
                "source_free_multisite_metrics": entry.get("source_free_multisite_metrics", {}),
            }
        )
    return sorted(
        summaries,
        key=lambda item: (
            str(item.get("v4_high_order_stress_decision") or ""),
            str(item.get("pdb_id") or ""),
        ),
    )


def compact_ids(rows: list[dict[str, Any]], decision: str) -> list[str]:
    return sorted(
        {
            str(row.get("pdb_id") or "")
            for row in rows
            if row.get("v4_high_order_stress_decision") == decision
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids()
    rows: list[dict[str, Any]] = []
    rows_by_pdb: dict[str, dict[str, Any]] = {}
    cif_text_by_pdb: dict[str, str] = {}
    fetch_errors: dict[str, str] = {}
    surface_order_by_pdb = {pdb_id: index for index, pdb_id in enumerate(ordered_ids, start=1)}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            row, cif_text = fetch_review_row(pdb_id, index, id_to_queries)
            rows.append(row)
            rows_by_pdb[pdb_id] = row
            cif_text_by_pdb[pdb_id] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.06)

    initial_fetch_errors = dict(fetch_errors)
    if initial_fetch_errors:
        time.sleep(1.0)
    for pdb_id in sorted(initial_fetch_errors):
        if pdb_id in rows_by_pdb:
            fetch_errors.pop(pdb_id, None)
            continue
        try:
            row, cif_text = fetch_review_row(
                pdb_id,
                surface_order_by_pdb.get(pdb_id, len(rows) + 1),
                id_to_queries,
                retry=True,
            )
            rows.append(row)
            rows_by_pdb[pdb_id] = row
            cif_text_by_pdb[pdb_id] = cif_text
            fetch_errors.pop(pdb_id, None)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.06)

    materializer = ns.materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=[row["pdb_id"] for row in rows],
        cif_text_by_pdb=cif_text_by_pdb,
    )
    materializer_rows = summarize_materializer_rows(materializer, rows_by_pdb)
    decision_counts = Counter(
        str(row.get("v4_high_order_stress_decision") or "") for row in materializer_rows
    )
    high_order_epk_rows = [
        row for row in rows if row.get("high_order_epk_query_candidate_not_prior_seed")
    ]
    non_orc_high_order_atpase_rows = [
        row for row in rows if row.get("non_orc_high_order_atpase_query_candidate")
    ]
    v4_feature_rows = [row for row in rows if row.get("high_order_v4_feature")]
    overblock_rows = [
        row
        for row in materializer_rows
        if row.get("v4_high_order_stress_decision")
        == "high_order_epk_overblock_risk_by_v4_review_only"
    ]
    retained_high_order_epk_rows = [
        row
        for row in materializer_rows
        if row.get("v4_high_order_stress_decision")
        == "high_order_epk_current_hit_retained_by_v4_review_only"
    ]
    non_orc_counterexample_rows = [
        row
        for row in materializer_rows
        if row.get("v4_high_order_stress_decision")
        in {
            "non_orc_current_rule_counterexample_blocked_by_v4_review_only",
            "non_orc_current_rule_counterexample_residual_after_v4_review_only",
        }
    ]
    non_epk_residual_rows = [
        row
        for row in materializer_rows
        if row.get("v4_high_order_stress_decision")
        in {
            "non_orc_current_rule_counterexample_residual_after_v4_review_only",
            "non_epk_topology_clear_hit_residual_after_v4_review_only",
        }
    ]
    fixed_positive_lost_rows = [
        row
        for row in materializer_rows
        if row.get("v4_high_order_stress_decision")
        == "fixed_known_epk_positive_lost_to_v4_review_only"
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_high_order_epk_atpase_overblock_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0 "
                "and build_epk_heteromeric_positive_coverage_candidate_scout"
            ),
            "guard_under_test": "v4_oligomeric_atp_terminals_no_mg_required",
            "query_surface": {
                "epk_component_text_queries": EPK_COMPONENT_TEXT_QUERIES,
                "non_orc_atpase_component_text_queries": NON_ORC_ATPASE_COMPONENT_TEXT_QUERIES,
                "fixed_control_ids": sorted(
                    PRIOR_KNOWN_EPK_POSITIVE_IDS | PRIOR_ORC_COUNTEREXAMPLE_IDS | PRESSURE_IDS
                ),
                "max_unique_ids": MAX_UNIQUE_IDS,
                "high_order_filter": {
                    "min_gamma_capable_terminal_p_count": HIGH_ORDER_MIN_GAMMA_TERMINAL_P,
                    "min_polymer_chain_count": HIGH_ORDER_MIN_POLYMER_CHAINS,
                },
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(rows),
            "initial_fetch_error_count": len(initial_fetch_errors),
            "retry_fetch_success_count": len(initial_fetch_errors) - len(fetch_errors),
            "fetch_error_count": len(fetch_errors),
            "high_order_v4_feature_row_count": len(v4_feature_rows),
            "high_order_epk_query_candidate_not_prior_seed_count": len(high_order_epk_rows),
            "high_order_epk_query_candidate_not_prior_seed_pdb_ids": sorted(
                row["pdb_id"] for row in high_order_epk_rows
            ),
            "non_orc_high_order_atpase_query_candidate_count": len(non_orc_high_order_atpase_rows),
            "non_orc_high_order_atpase_query_candidate_pdb_ids": sorted(
                row["pdb_id"] for row in non_orc_high_order_atpase_rows
            ),
            "actual_materializer_input_count": len(rows),
            "actual_materializer_candidate_status_counts": materializer.get("metadata", {}).get(
                "candidate_status_counts", {}
            ),
            "v4_high_order_decision_counts": dict(sorted(decision_counts.items())),
            "high_order_epk_overblock_risk_count": len(overblock_rows),
            "high_order_epk_overblock_risk_pdb_ids": sorted(row["pdb_id"] for row in overblock_rows),
            "high_order_epk_current_hit_retained_count": len(retained_high_order_epk_rows),
            "high_order_epk_current_hit_retained_pdb_ids": sorted(
                row["pdb_id"] for row in retained_high_order_epk_rows
            ),
            "fixed_known_epk_positive_lost_to_v4_count": len(fixed_positive_lost_rows),
            "fixed_known_epk_positive_lost_to_v4_pdb_ids": sorted(
                row["pdb_id"] for row in fixed_positive_lost_rows
            ),
            "non_orc_current_rule_counterexample_count": len(non_orc_counterexample_rows),
            "non_orc_current_rule_counterexample_pdb_ids": sorted(
                row["pdb_id"] for row in non_orc_counterexample_rows
            ),
            "non_epk_topology_clear_residual_after_v4_count": len(non_epk_residual_rows),
            "non_epk_topology_clear_residual_after_v4_pdb_ids": sorted(
                row["pdb_id"] for row in non_epk_residual_rows
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
        "fetch_errors": fetch_errors,
        "review_rows": rows,
        "actual_materializer_probe": materializer,
        "guard_stress_rows": materializer_rows,
        "high_order_epk_overblock_risk_rows": overblock_rows,
        "high_order_epk_current_hit_retained_rows": retained_high_order_epk_rows,
        "non_orc_current_rule_counterexamples_review_only": non_orc_counterexample_rows,
        "non_epk_topology_clear_residual_after_v4_review_only": non_epk_residual_rows,
        "warnings": [
            "Review-only bounded stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "High-order ePK rows are query/context candidates, not imported positives or production labels.",
            "Non-ORC ATPase classification excludes deposited ORC/MCM role tokens and probable ePK context for this adversarial review only.",
            "No raw coordinate files are written; mmCIF text is reduced in memory to compact metrics and materializer hits.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
