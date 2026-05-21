#!/usr/bin/env python3
"""Stress v4 against biological assembly coordinates.

This helper keeps the search bounded, fetches deposited and biological
assembly mmCIF text in memory only, and writes compact metrics/materializer
evidence. It intentionally does not write raw coordinate dumps.
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
import orc_mcm_multisite_guard_stress as orc
import v4_component_no_mg_kinase_dimer_stress as prior
import v4_high_order_epk_atpase_overblock_stress as high_order


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_ASSEMBLY_CIF_URL = "https://files.rcsb.org/download/{pdb_id}-assembly{assembly_id}.cif"
MAX_UNIQUE_IDS = 260
MAX_ASSEMBLIES_PER_ENTRY = 3
MAX_MATERIALIZER_IDS = 120
HIGH_ORDER_MIN_GAMMA_TERMINAL_P = 3
HIGH_ORDER_MIN_POLYMER_CHAINS = 5

FIXED_CONTROL_IDS = sorted(
    high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
    | high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
    | high_order.PRESSURE_IDS
)

EPK_ASSEMBLY_QUERIES = [
    {"name": "protein_kinase_atp_assembly", "phrase": "protein kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "protein_kinase_anp_assembly", "phrase": "protein kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "kinase_peptide_atp", "phrase": "kinase peptide", "ligand": "ATP", "start": 0, "rows": 30},
    {"name": "kinase_peptide_anp", "phrase": "kinase peptide", "ligand": "ANP", "start": 0, "rows": 30},
    {"name": "substrate_peptide_kinase_atp", "phrase": "substrate peptide kinase", "ligand": "ATP", "start": 0, "rows": 30},
    {"name": "substrate_peptide_kinase_anp", "phrase": "substrate peptide kinase", "ligand": "ANP", "start": 0, "rows": 30},
    {"name": "jnk_substrate_peptide_atp", "phrase": "JNK substrate peptide", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "jnk_substrate_peptide_anp", "phrase": "JNK substrate peptide", "ligand": "ANP", "start": 0, "rows": 25},
    {"name": "rsk_kinase_atp", "phrase": "RSK kinase", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "rsk_kinase_anp", "phrase": "RSK kinase", "ligand": "ANP", "start": 0, "rows": 25},
    {"name": "cdpk_kinase_atp", "phrase": "CDPK kinase", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "cdpk_kinase_anp", "phrase": "CDPK kinase", "ligand": "ANP", "start": 0, "rows": 25},
    {"name": "mtor_kinase_atp_assembly", "phrase": "mTOR kinase", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "mtor_kinase_anp_assembly", "phrase": "mTOR kinase", "ligand": "ANP", "start": 0, "rows": 25},
]

NON_ORC_ATPASE_ASSEMBLY_QUERIES = [
    {"name": "aaa_atpase_atp_assembly", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "aaa_atpase_anp_assembly", "phrase": "AAA+ ATPase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "proteasome_atpase_atp_assembly", "phrase": "proteasome ATPase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "proteasome_atpase_anp_assembly", "phrase": "proteasome ATPase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "helicase_atp_assembly", "phrase": "helicase ATP", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "helicase_anp_assembly", "phrase": "helicase ATP", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "clamp_loader_atp_assembly", "phrase": "clamp loader ATP", "ligand": "ATP", "start": 0, "rows": 30},
    {"name": "clamp_loader_anp_assembly", "phrase": "clamp loader ATP", "ligand": "ANP", "start": 0, "rows": 30},
    {"name": "dynein_atp_assembly", "phrase": "dynein ATP", "ligand": "ATP", "start": 0, "rows": 30},
    {"name": "dynein_anp_assembly", "phrase": "dynein ATP", "ligand": "ANP", "start": 0, "rows": 30},
    {"name": "abc_transporter_atp_assembly", "phrase": "ABC transporter ATP", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "abc_transporter_anp_assembly", "phrase": "ABC transporter ATP", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "vcp_p97_atp_assembly", "phrase": "VCP p97 ATP", "ligand": "ATP", "start": 0, "rows": 30},
    {"name": "vcp_p97_anp_assembly", "phrase": "VCP p97 ATP", "ligand": "ANP", "start": 0, "rows": 30},
]

SOURCE_PRIORITY_TERMS = [
    "cdpk",
    "jnk",
    "map kinase",
    "mtor",
    "peptide",
    "protein kinase",
    "rsk",
    "substrate",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def component_full_text_query(query: dict[str, Any]) -> list[str]:
    payload = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "full_text",
                    "parameters": {"value": str(query["phrase"])},
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                        "operator": "exact_match",
                        "value": str(query["ligand"]),
                    },
                },
            ],
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": int(query["start"]), "rows": int(query["rows"])},
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "score", "direction": "desc"}],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=payload, timeout=30)
    if response.status_code == 204 or not response.text.strip():
        return []
    response.raise_for_status()
    result = response.json()
    return [str(row["identifier"]).upper() for row in result.get("result_set", [])]


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    surface_ids: dict[str, list[str]] = {
        "epk_assembly_text": [],
        "non_orc_atpase_assembly_text": [],
    }
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}

    ordered = list(FIXED_CONTROL_IDS)
    for pdb_id in ordered:
        id_to_queries[pdb_id].append("fixed_prior_positive_counterexample_or_pressure_control")

    for surface, queries in [
        ("epk_assembly_text", EPK_ASSEMBLY_QUERIES),
        ("non_orc_atpase_assembly_text", NON_ORC_ATPASE_ASSEMBLY_QUERIES),
    ]:
        for query in queries:
            name = str(query["name"])
            try:
                ids = component_full_text_query(query)
                query_counts[name] = len(ids)
            except Exception as exc:  # pragma: no cover - network evidence
                ids = []
                query_counts[name] = 0
                query_errors[name] = repr(exc)
            for pdb_id in ids:
                id_to_queries[pdb_id].append(
                    f"{surface}:{name}:{query['phrase']}:{query['ligand']}"
                )
                if pdb_id not in surface_ids[surface]:
                    surface_ids[surface].append(pdb_id)
            time.sleep(0.12)

    remaining = max(MAX_UNIQUE_IDS - len(ordered), 0)
    epk_quota = remaining // 2
    atpase_quota = remaining - epk_quota
    for pdb_id in surface_ids["epk_assembly_text"][:epk_quota]:
        if pdb_id not in ordered:
            ordered.append(pdb_id)
    for pdb_id in surface_ids["non_orc_atpase_assembly_text"][:atpase_quota]:
        if pdb_id not in ordered:
            ordered.append(pdb_id)

    query_counts["fixed_control_ids"] = len(FIXED_CONTROL_IDS)
    query_counts["epk_assembly_text_unique_ids_available"] = len(surface_ids["epk_assembly_text"])
    query_counts["epk_assembly_text_selected_quota"] = epk_quota
    query_counts["non_orc_atpase_assembly_text_unique_ids_available"] = len(
        surface_ids["non_orc_atpase_assembly_text"]
    )
    query_counts["non_orc_atpase_assembly_text_selected_quota"] = atpase_quota
    return ordered[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_counts


def query_surface_groups(query_names: list[str]) -> list[str]:
    groups = set()
    for name in query_names:
        if name.startswith("epk_assembly_text:"):
            groups.add("epk_assembly_text")
        if name.startswith("non_orc_atpase_assembly_text:"):
            groups.add("non_orc_atpase_assembly_text")
        if name == "fixed_prior_positive_counterexample_or_pressure_control":
            groups.add("fixed_control")
    return sorted(groups)


def limited_assembly_ids(entry_payload: dict[str, Any]) -> list[str]:
    ids = (
        entry_payload.get("rcsb_entry_container_identifiers", {}).get("assembly_ids")
        or ["1"]
    )
    normalized = [str(value) for value in ids if str(value)]
    return normalized[:MAX_ASSEMBLIES_PER_ENTRY] or ["1"]


def high_order_feature(metrics: dict[str, Any]) -> bool:
    try:
        terminal_p = int(metrics.get("gamma_capable_terminal_p_count") or 0)
        polymer_chains = int(metrics.get("polymer_chain_count") or 0)
    except (TypeError, ValueError):
        return False
    return (
        terminal_p >= HIGH_ORDER_MIN_GAMMA_TERMINAL_P
        and polymer_chains >= HIGH_ORDER_MIN_POLYMER_CHAINS
    )


def compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "gamma_capable_terminal_p_count",
        "gamma_capable_terminal_p_near_mg_count",
        "gamma_capable_terminal_p_near_mg_chain_count",
        "gamma_capable_terminal_p_near_mg_entity_count",
        "gamma_capable_terminal_p_near_mg_ligand_counts",
        "polymer_chain_count",
        "polymer_entity_count",
        "compact_gamma_mg_sites",
    ]
    return {key: metrics.get(key) for key in keys if key in metrics}


def metric_sort_key(row: dict[str, Any]) -> tuple[int, int, int, int]:
    metrics = row["assembly_metrics"]
    return (
        int(row.get("assembly_v4_oligomeric_atp_terminals_no_mg_required_hit") or False),
        int(metrics.get("gamma_capable_terminal_p_count") or 0),
        int(metrics.get("polymer_chain_count") or 0),
        int(metrics.get("gamma_capable_terminal_p_near_mg_count") or 0),
    )


def source_priority_terms(text: str) -> list[str]:
    lower = text.lower()
    return sorted(term for term in SOURCE_PRIORITY_TERMS if term in lower)


def fetch_best_assembly_row(
    pdb_id: str,
    index: int,
    id_to_queries: dict[str, list[str]],
) -> tuple[dict[str, Any], str]:
    deposited_cif = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
    entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    deposited_atoms, deposited_parse_meta = ns.parse_atom_site_raw(deposited_cif)
    deposited_entity_descriptions = orc.entity_descriptions_from_cif(deposited_cif)
    text = prior.context_text(entry_payload, deposited_entity_descriptions)
    role_tokens = orc.deposited_role_tokens(text)
    probable_epk = orc.probable_epk(pdb_id, text)
    kinase_tokens = high_order.entity_kinase_tokens(deposited_entity_descriptions)
    query_names = id_to_queries.get(pdb_id, [])
    groups = query_surface_groups(query_names)
    deposited_metrics = orc.source_free_multisite_metrics(deposited_atoms)
    deposited_v4 = high_order.v4_hit(deposited_metrics)

    assembly_rows = []
    assembly_fetch_errors: dict[str, str] = {}
    best_assembly_text = deposited_cif
    for assembly_id in limited_assembly_ids(entry_payload):
        try:
            assembly_cif = base.fetch_text(
                RCSB_ASSEMBLY_CIF_URL.format(pdb_id=pdb_id, assembly_id=assembly_id)
            )
            assembly_atoms, assembly_parse_meta = ns.parse_atom_site_raw(assembly_cif)
            assembly_metrics = orc.source_free_multisite_metrics(assembly_atoms)
            assembly_v4 = high_order.v4_hit(assembly_metrics)
            assembly_rows.append(
                {
                    "assembly_id": assembly_id,
                    "assembly_parse_meta": assembly_parse_meta,
                    "assembly_metrics": assembly_metrics,
                    "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit": assembly_v4,
                    "assembly_high_order_v4_feature": high_order_feature(assembly_metrics),
                    "assembly_cif_text": assembly_cif,
                }
            )
        except Exception as exc:  # pragma: no cover - network evidence
            assembly_fetch_errors[assembly_id] = repr(exc)
        time.sleep(0.04)

    if not assembly_rows:
        assembly_rows.append(
            {
                "assembly_id": "deposited_fallback",
                "assembly_parse_meta": deposited_parse_meta,
                "assembly_metrics": deposited_metrics,
                "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit": deposited_v4,
                "assembly_high_order_v4_feature": high_order_feature(deposited_metrics),
                "assembly_cif_text": deposited_cif,
            }
        )

    best = sorted(assembly_rows, key=metric_sort_key, reverse=True)[0]
    best_assembly_text = str(best.pop("assembly_cif_text"))
    compact_assembly_rows = [
        {
            "assembly_id": str(row["assembly_id"]),
            "assembly_parse_meta": row["assembly_parse_meta"],
            "assembly_metrics": compact_metrics(row["assembly_metrics"]),
            "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit": row[
                "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit"
            ],
            "assembly_high_order_v4_feature": row["assembly_high_order_v4_feature"],
        }
        for row in assembly_rows
    ]
    best_metrics = best["assembly_metrics"]
    assembly_v4 = bool(best["assembly_v4_oligomeric_atp_terminals_no_mg_required_hit"])
    assembly_promoted = assembly_v4 and not deposited_v4
    deposited_single_entity_or_chain_limited = (
        int(deposited_metrics.get("gamma_capable_terminal_p_count") or 0)
        >= HIGH_ORDER_MIN_GAMMA_TERMINAL_P
        and int(deposited_metrics.get("polymer_chain_count") or 0)
        < HIGH_ORDER_MIN_POLYMER_CHAINS
        and int(deposited_metrics.get("polymer_entity_count") or 0) <= 1
    )
    epk_assembly_candidate = (
        "epk_assembly_text" in groups
        and assembly_v4
        and probable_epk
        and pdb_id not in high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
    )
    prioritized_source_context = bool(
        epk_assembly_candidate
        and kinase_tokens
        and source_priority_terms(text)
    )
    non_orc_atpase_assembly_candidate = (
        "non_orc_atpase_assembly_text" in groups
        and assembly_v4
        and not probable_epk
        and not role_tokens
    )
    row = {
        "pdb_id": pdb_id,
        "surface_order": index,
        "query_names": query_names,
        "query_surface_groups": groups,
        "title": entry_payload.get("struct", {}).get("title", ""),
        "keywords": entry_payload.get("struct_keywords", {}),
        "entity_descriptions_compact": deposited_entity_descriptions[:14],
        "entity_kinase_tokens": kinase_tokens,
        "source_priority_terms": source_priority_terms(text),
        "known_epk_positive_input": pdb_id in high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS,
        "known_orc_counterexample_input": pdb_id in high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS,
        "known_pressure_id_input": pdb_id in high_order.PRESSURE_IDS,
        "probable_epk_from_context": probable_epk,
        "deposited_orc_mcm_role_tokens": role_tokens,
        "reviewed": True,
        "deposited_parse_meta": deposited_parse_meta,
        "deposited_component_state": prior.compact_nonpolymer_counts(deposited_atoms),
        "deposited_source_free_multisite_metrics": compact_metrics(deposited_metrics),
        "deposited_v4_oligomeric_atp_terminals_no_mg_required_hit": deposited_v4,
        "deposited_high_order_v4_feature": high_order_feature(deposited_metrics),
        "assembly_ids_reviewed": [row["assembly_id"] for row in compact_assembly_rows],
        "best_assembly_id": str(best["assembly_id"]),
        "assembly_fetch_errors": assembly_fetch_errors,
        "assembly_metric_summaries": compact_assembly_rows,
        "best_assembly_source_free_multisite_metrics": compact_metrics(best_metrics),
        "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit": assembly_v4,
        "assembly_high_order_v4_feature": high_order_feature(best_metrics),
        "assembly_promoted_v4_from_deposited_negative": assembly_promoted,
        "assembly_promoted_from_single_entity_or_chain_limited_deposited": (
            assembly_promoted and deposited_single_entity_or_chain_limited
        ),
        "epk_assembly_v4_overblock_candidate_not_prior_seed": epk_assembly_candidate,
        "epk_assembly_prioritized_source_context_candidate": prioritized_source_context,
        "non_orc_atpase_assembly_v4_candidate": non_orc_atpase_assembly_candidate,
    }
    return row, best_assembly_text


def selected_materializer_ids(rows: list[dict[str, Any]]) -> list[str]:
    selected: list[str] = []
    priority_flags = [
        "known_epk_positive_input",
        "known_orc_counterexample_input",
        "epk_assembly_prioritized_source_context_candidate",
        "epk_assembly_v4_overblock_candidate_not_prior_seed",
        "non_orc_atpase_assembly_v4_candidate",
        "assembly_promoted_v4_from_deposited_negative",
    ]
    for flag in priority_flags:
        for row in rows:
            pdb_id = str(row["pdb_id"])
            if row.get(flag) and pdb_id not in selected:
                selected.append(pdb_id)
                if len(selected) >= MAX_MATERIALIZER_IDS:
                    return selected
    for row in rows:
        pdb_id = str(row["pdb_id"])
        if row.get("assembly_v4_oligomeric_atp_terminals_no_mg_required_hit") and pdb_id not in selected:
            selected.append(pdb_id)
            if len(selected) >= MAX_MATERIALIZER_IDS:
                return selected
    return selected


def summarize_materializer_rows(
    materializer: dict[str, Any],
    rows_by_pdb: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    summaries = []
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
        fixed_positive = bool(entry.get("known_epk_positive_input"))
        fixed_orc_counterexample = bool(entry.get("known_orc_counterexample_input"))
        epk_assembly_candidate = bool(entry.get("epk_assembly_v4_overblock_candidate_not_prior_seed"))
        non_orc_atpase_candidate = bool(entry.get("non_orc_atpase_assembly_v4_candidate"))
        guard_hit = bool(entry.get("assembly_v4_oligomeric_atp_terminals_no_mg_required_hit"))

        if epk_assembly_candidate and topology_clear and guard_hit:
            decision = "assembly_epk_overblock_risk_by_v4_review_only"
        elif epk_assembly_candidate and topology_clear:
            decision = "assembly_epk_current_hit_retained_by_v4_review_only"
        elif fixed_positive and topology_clear and guard_hit:
            decision = "fixed_known_epk_positive_lost_to_assembly_v4_review_only"
        elif fixed_positive and topology_clear:
            decision = "fixed_known_epk_positive_retained_by_assembly_v4_review_only"
        elif non_orc_atpase_candidate and topology_clear and guard_hit:
            decision = "non_orc_assembly_counterexample_blocked_by_v4_review_only"
        elif non_orc_atpase_candidate and topology_clear:
            decision = "non_orc_assembly_counterexample_residual_after_v4_review_only"
        elif fixed_orc_counterexample and topology_clear and guard_hit:
            decision = "fixed_orc_counterexample_blocked_by_assembly_v4_review_only"
        elif fixed_orc_counterexample and topology_clear:
            decision = "fixed_orc_counterexample_residual_after_assembly_v4_review_only"
        elif topology_clear and not probable_epk and guard_hit:
            decision = "non_epk_topology_clear_hit_blocked_by_assembly_v4_review_only"
        elif topology_clear and not probable_epk:
            decision = "non_epk_topology_clear_hit_residual_after_assembly_v4_review_only"
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
                "best_assembly_id": entry.get("best_assembly_id"),
                "known_epk_positive_input": fixed_positive,
                "known_orc_counterexample_input": fixed_orc_counterexample,
                "probable_epk_from_context": entry.get("probable_epk_from_context"),
                "entity_kinase_tokens": entry.get("entity_kinase_tokens", []),
                "source_priority_terms": entry.get("source_priority_terms", []),
                "deposited_orc_mcm_role_tokens": entry.get("deposited_orc_mcm_role_tokens", []),
                "assembly_v4_oligomeric_atp_terminals_no_mg_required_hit": guard_hit,
                "assembly_promoted_v4_from_deposited_negative": entry.get(
                    "assembly_promoted_v4_from_deposited_negative"
                ),
                "epk_assembly_v4_overblock_candidate_not_prior_seed": epk_assembly_candidate,
                "epk_assembly_prioritized_source_context_candidate": entry.get(
                    "epk_assembly_prioritized_source_context_candidate"
                ),
                "non_orc_atpase_assembly_v4_candidate": non_orc_atpase_candidate,
                "candidate_status": row.get("candidate_status"),
                "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
                "substrate_mode_materializer_hit_count": len(substrate_hits),
                "topology_clear_substrate_mode_hit": topology_clear,
                **flags,
                "assembly_v4_stress_decision": decision,
                "substrate_mode_materializer_hits": substrate_hits[:10],
                "best_assembly_source_free_multisite_metrics": entry.get(
                    "best_assembly_source_free_multisite_metrics", {}
                ),
            }
        )
    return sorted(
        summaries,
        key=lambda item: (
            str(item.get("assembly_v4_stress_decision") or ""),
            str(item.get("pdb_id") or ""),
        ),
    )


def compact_ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(row["pdb_id"]) for row in rows if row.get(key))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids()
    rows: list[dict[str, Any]] = []
    rows_by_pdb: dict[str, dict[str, Any]] = {}
    assembly_text_by_pdb: dict[str, str] = {}
    fetch_errors: dict[str, str] = {}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            row, assembly_text = fetch_best_assembly_row(pdb_id, index, id_to_queries)
            rows.append(row)
            rows_by_pdb[pdb_id] = row
            assembly_text_by_pdb[pdb_id] = assembly_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        if index % 25 == 0:
            print(
                json.dumps(
                    {
                        "progress_reviewed": len(rows),
                        "progress_fetch_errors": len(fetch_errors),
                        "last_index": index,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        time.sleep(0.05)

    materializer_ids = selected_materializer_ids(rows)
    materializer = ns.materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=materializer_ids,
        cif_text_by_pdb={pdb_id: assembly_text_by_pdb[pdb_id] for pdb_id in materializer_ids},
    )
    materializer_rows = summarize_materializer_rows(materializer, rows_by_pdb)
    decision_counts = Counter(
        str(row.get("assembly_v4_stress_decision") or "") for row in materializer_rows
    )

    overblock_rows = [
        row
        for row in materializer_rows
        if row.get("assembly_v4_stress_decision")
        == "assembly_epk_overblock_risk_by_v4_review_only"
    ]
    non_epk_counterexample_rows = [
        row
        for row in materializer_rows
        if row.get("assembly_v4_stress_decision")
        in {
            "non_orc_assembly_counterexample_blocked_by_v4_review_only",
            "non_orc_assembly_counterexample_residual_after_v4_review_only",
            "non_epk_topology_clear_hit_blocked_by_assembly_v4_review_only",
            "non_epk_topology_clear_hit_residual_after_assembly_v4_review_only",
        }
    ]
    residual_rows = [
        row
        for row in materializer_rows
        if row.get("assembly_v4_stress_decision")
        in {
            "non_orc_assembly_counterexample_residual_after_v4_review_only",
            "non_epk_topology_clear_hit_residual_after_assembly_v4_review_only",
            "fixed_orc_counterexample_residual_after_assembly_v4_review_only",
        }
    ]
    fixed_positive_lost_rows = [
        row
        for row in materializer_rows
        if row.get("assembly_v4_stress_decision")
        == "fixed_known_epk_positive_lost_to_assembly_v4_review_only"
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_assembly_overblock_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0, "
                "build_epk_heteromeric_positive_coverage_candidate_scout, and "
                "v4_oligomeric_atp_terminals_no_mg_required review guard candidate"
            ),
            "guard_under_test": "v4_oligomeric_atp_terminals_no_mg_required",
            "query_surface": {
                "epk_assembly_text_queries": EPK_ASSEMBLY_QUERIES,
                "non_orc_atpase_assembly_text_queries": NON_ORC_ATPASE_ASSEMBLY_QUERIES,
                "fixed_control_ids": FIXED_CONTROL_IDS,
                "max_unique_ids": MAX_UNIQUE_IDS,
                "max_assemblies_per_entry": MAX_ASSEMBLIES_PER_ENTRY,
                "high_order_filter": {
                    "min_gamma_capable_terminal_p_count": HIGH_ORDER_MIN_GAMMA_TERMINAL_P,
                    "min_polymer_chain_count": HIGH_ORDER_MIN_POLYMER_CHAINS,
                },
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(rows),
            "fetch_error_count": len(fetch_errors),
            "assembly_v4_feature_row_count": sum(
                1 for row in rows if row.get("assembly_v4_oligomeric_atp_terminals_no_mg_required_hit")
            ),
            "deposited_v4_feature_row_count": sum(
                1 for row in rows if row.get("deposited_v4_oligomeric_atp_terminals_no_mg_required_hit")
            ),
            "assembly_promoted_v4_from_deposited_negative_count": sum(
                1 for row in rows if row.get("assembly_promoted_v4_from_deposited_negative")
            ),
            "assembly_promoted_v4_from_deposited_negative_pdb_ids": compact_ids(
                rows, "assembly_promoted_v4_from_deposited_negative"
            ),
            "assembly_promoted_from_single_entity_or_chain_limited_count": sum(
                1
                for row in rows
                if row.get("assembly_promoted_from_single_entity_or_chain_limited_deposited")
            ),
            "epk_assembly_v4_overblock_candidate_not_prior_seed_count": sum(
                1 for row in rows if row.get("epk_assembly_v4_overblock_candidate_not_prior_seed")
            ),
            "epk_assembly_v4_overblock_candidate_not_prior_seed_pdb_ids": compact_ids(
                rows, "epk_assembly_v4_overblock_candidate_not_prior_seed"
            ),
            "epk_assembly_prioritized_source_context_candidate_count": sum(
                1 for row in rows if row.get("epk_assembly_prioritized_source_context_candidate")
            ),
            "epk_assembly_prioritized_source_context_candidate_pdb_ids": compact_ids(
                rows, "epk_assembly_prioritized_source_context_candidate"
            ),
            "non_orc_atpase_assembly_v4_candidate_count": sum(
                1 for row in rows if row.get("non_orc_atpase_assembly_v4_candidate")
            ),
            "non_orc_atpase_assembly_v4_candidate_pdb_ids": compact_ids(
                rows, "non_orc_atpase_assembly_v4_candidate"
            ),
            "actual_materializer_input_count": len(materializer_ids),
            "actual_materializer_input_pdb_ids": materializer_ids,
            "actual_materializer_candidate_status_counts": materializer.get("metadata", {}).get(
                "candidate_status_counts", {}
            ),
            "assembly_v4_stress_decision_counts": dict(sorted(decision_counts.items())),
            "assembly_epk_overblock_risk_count": len(overblock_rows),
            "assembly_epk_overblock_risk_pdb_ids": sorted(row["pdb_id"] for row in overblock_rows),
            "fixed_known_epk_positive_lost_to_assembly_v4_count": len(fixed_positive_lost_rows),
            "fixed_known_epk_positive_lost_to_assembly_v4_pdb_ids": sorted(
                row["pdb_id"] for row in fixed_positive_lost_rows
            ),
            "non_epk_topology_clear_counterexample_count": len(non_epk_counterexample_rows),
            "non_epk_topology_clear_counterexample_pdb_ids": sorted(
                row["pdb_id"] for row in non_epk_counterexample_rows
            ),
            "non_epk_or_fixed_orc_residual_after_assembly_v4_count": len(residual_rows),
            "non_epk_or_fixed_orc_residual_after_assembly_v4_pdb_ids": sorted(
                row["pdb_id"] for row in residual_rows
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
        "assembly_v4_materializer_rows": materializer_rows,
        "assembly_epk_overblock_risk_rows": overblock_rows,
        "non_epk_topology_clear_counterexamples_review_only": non_epk_counterexample_rows,
        "non_epk_or_fixed_orc_residual_after_assembly_v4_review_only": residual_rows,
        "warnings": [
            "Review-only bounded stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Biological assembly CIFs were fetched in memory and reduced to compact metrics and materializer hits.",
            "Assembly ePK rows are query/context candidates, not imported positives or production labels.",
            "The materializer was run only on a bounded prioritized subset of assembly-v4 candidates and controls.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
