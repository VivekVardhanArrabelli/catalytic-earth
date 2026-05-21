#!/usr/bin/env python3
"""Stress an entry-level v4 assembly guard variant.

This helper generalizes the 5UJ7 biological-assembly split: it finds entries
where deposited atom_site coordinates satisfy v4, but declared biological
assemblies fall below the v4 polymer-chain floor. It then tests a review-only
entry-level variant that can inherit v4 from deposited atom_site or any
declared biological assembly context. CIFs are fetched in memory only and are
reduced to compact metrics/materializer summaries.
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
import v4_assembly_overblock_stress as assembly
import v4_component_no_mg_kinase_dimer_stress as prior
import v4_high_order_epk_atpase_overblock_stress as high_order


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_ASSEMBLY_CIF_URL = "https://files.rcsb.org/download/{pdb_id}-assembly{assembly_id}.cif"
MAX_UNIQUE_IDS = 360
MAX_ASSEMBLIES_PER_ENTRY = 12
MAX_MATERIALIZER_CONTEXTS = 180
HIGH_ORDER_MIN_GAMMA_TERMINAL_P = 3
HIGH_ORDER_MIN_POLYMER_CHAINS = 5

FIXED_CONTROL_IDS = sorted(
    high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
    | high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
    | high_order.PRESSURE_IDS
)

ORC_MCM_COMPONENT_QUERIES = [
    {"name": "origin_recognition_complex_atp", "phrase": "origin recognition complex", "ligand": "ATP", "start": 0, "rows": 60},
    {"name": "origin_recognition_complex_anp", "phrase": "origin recognition complex", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "orc_cdc6_atp", "phrase": "ORC Cdc6", "ligand": "ATP", "start": 0, "rows": 60},
    {"name": "orc_cdc6_anp", "phrase": "ORC Cdc6", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "occm_atp", "phrase": "OCCM", "ligand": "ATP", "start": 0, "rows": 50},
    {"name": "mcm2_7_atp", "phrase": "Mcm2-7", "ligand": "ATP", "start": 0, "rows": 60},
    {"name": "mcm2_7_anp", "phrase": "Mcm2-7", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mcm_loading_atp", "phrase": "MCM loading", "ligand": "ATP", "start": 0, "rows": 50},
    {"name": "cmg_helicase_atp", "phrase": "CMG helicase", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "replication_initiation_atp", "phrase": "replication initiation", "ligand": "ATP", "start": 0, "rows": 60},
]

NON_ORC_ATPASE_COMPONENT_QUERIES = [
    {"name": "aaa_atpase_atp_0", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 0, "rows": 55},
    {"name": "aaa_atpase_atp_120", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 120, "rows": 55},
    {"name": "aaa_atpase_anp_0", "phrase": "AAA+ ATPase", "ligand": "ANP", "start": 0, "rows": 55},
    {"name": "abc_transporter_atp", "phrase": "ABC transporter ATP", "ligand": "ATP", "start": 0, "rows": 55},
    {"name": "abc_transporter_anp", "phrase": "ABC transporter ATP", "ligand": "ANP", "start": 0, "rows": 55},
    {"name": "clamp_loader_atp", "phrase": "clamp loader ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "clamp_loader_anp", "phrase": "clamp loader ATP", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "replication_factor_c_atp", "phrase": "replication factor C ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "helicase_atp", "phrase": "helicase ATP", "ligand": "ATP", "start": 0, "rows": 55},
    {"name": "helicase_anp", "phrase": "helicase ATP", "ligand": "ANP", "start": 0, "rows": 55},
    {"name": "proteasome_atpase_atp", "phrase": "proteasome ATPase", "ligand": "ATP", "start": 0, "rows": 55},
    {"name": "dynein_atp", "phrase": "dynein ATP", "ligand": "ATP", "start": 0, "rows": 55},
    {"name": "vcp_p97_atp", "phrase": "VCP p97 ATP", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "translocase_atp", "phrase": "translocase ATP", "ligand": "ATP", "start": 0, "rows": 45},
]

EPK_SAFETY_COMPONENT_QUERIES = [
    {"name": "protein_kinase_peptide_atp", "phrase": "protein kinase peptide", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "protein_kinase_peptide_anp", "phrase": "protein kinase peptide", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "substrate_peptide_kinase_atp", "phrase": "substrate peptide kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "substrate_peptide_kinase_anp", "phrase": "substrate peptide kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "map_kinase_atp", "phrase": "MAP kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "map_kinase_anp", "phrase": "MAP kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mtor_kinase_atp", "phrase": "mTOR kinase", "ligand": "ATP", "start": 0, "rows": 25},
    {"name": "mtor_kinase_anp", "phrase": "mTOR kinase", "ligand": "ANP", "start": 0, "rows": 25},
]

PRIOR_ASSEMBLY_ARTIFACTS = [
    Path("artifacts/research_lanes/epk_false_positive_hunter/v4_assembly_overblock_stress_20260521_002758Z.json"),
    Path("artifacts/research_lanes/epk_false_positive_hunter/v4_assembly_control_split_stress_20260521_002758Z.json"),
    Path("artifacts/research_lanes/epk_false_positive_hunter/v4_assembly_control_split_retry_20260521_002758Z.json"),
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


def add_id(
    ordered: list[str],
    id_to_queries: dict[str, list[str]],
    pdb_id: str,
    query_name: str,
) -> None:
    normalized = str(pdb_id).upper()
    id_to_queries[normalized].append(query_name)
    if normalized not in ordered:
        ordered.append(normalized)


def load_prior_seed_ids(repo_root: Path) -> tuple[list[str], dict[str, int]]:
    ids: list[str] = []
    counts: dict[str, int] = {}
    for rel_path in PRIOR_ASSEMBLY_ARTIFACTS:
        path = repo_root / rel_path
        if not path.exists():
            counts[str(rel_path)] = 0
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        selected: set[str] = set()
        for row in payload.get("review_rows", []) or payload.get("rows", []) or []:
            pdb_id = str(row.get("pdb_id") or "").upper()
            if not pdb_id:
                continue
            deposited_v4 = bool(
                row.get("deposited_v4_oligomeric_atp_terminals_no_mg_required_hit")
                or row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
            )
            assembly_metrics = row.get("assembly_metric_summaries", []) or []
            split_metric = any(
                int((summary.get("assembly_metrics") or {}).get("gamma_capable_terminal_p_count") or 0)
                >= HIGH_ORDER_MIN_GAMMA_TERMINAL_P
                and int((summary.get("assembly_metrics") or {}).get("polymer_chain_count") or 0)
                < HIGH_ORDER_MIN_POLYMER_CHAINS
                for summary in assembly_metrics
                if isinstance(summary, dict)
            )
            residual = row.get("v4_control_split_decision") in {
                "known_orc_counterexample_residual_after_v4_review_only",
                "topology_clear_hit_residual_after_v4_review_only",
            }
            if deposited_v4 or split_metric or residual:
                selected.add(pdb_id)
        for row in payload.get("assembly_residual_context_rows", []) or []:
            pdb_id = str(row.get("pdb_id") or "").upper()
            if pdb_id:
                selected.add(pdb_id)
        for pdb_id in sorted(selected):
            if pdb_id not in ids:
                ids.append(pdb_id)
        counts[str(rel_path)] = len(selected)
    return ids, counts


def collect_ids(
    repo_root: Path,
    max_unique_ids: int,
) -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    ordered: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}

    for pdb_id in FIXED_CONTROL_IDS:
        add_id(ordered, id_to_queries, pdb_id, "fixed_control_positive_counterexample_or_pressure")

    prior_ids, prior_counts = load_prior_seed_ids(repo_root)
    query_counts.update({f"prior_seed:{key}": value for key, value in prior_counts.items()})
    for pdb_id in prior_ids:
        add_id(ordered, id_to_queries, pdb_id, "prior_assembly_split_or_v4_seed")

    for surface, queries in [
        ("orc_occm_mcm_component_text", ORC_MCM_COMPONENT_QUERIES),
        ("non_orc_aaa_atpase_component_text", NON_ORC_ATPASE_COMPONENT_QUERIES),
        ("epk_safety_component_text", EPK_SAFETY_COMPONENT_QUERIES),
    ]:
        for query in queries:
            name = str(query["name"])
            try:
                ids = component_full_text_query(query)
                query_counts[f"{surface}:{name}"] = len(ids)
            except Exception as exc:  # pragma: no cover - network evidence
                ids = []
                query_counts[f"{surface}:{name}"] = 0
                query_errors[f"{surface}:{name}"] = repr(exc)
            for pdb_id in ids:
                add_id(
                    ordered,
                    id_to_queries,
                    pdb_id,
                    f"{surface}:{name}:{query['phrase']}:{query['ligand']}",
                )
            time.sleep(0.12)

    return ordered[:max_unique_ids], id_to_queries, query_errors, query_counts


def compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return assembly.compact_metrics(metrics)


def chain_floor_split(metrics: dict[str, Any]) -> bool:
    return (
        int(metrics.get("gamma_capable_terminal_p_count") or 0)
        >= HIGH_ORDER_MIN_GAMMA_TERMINAL_P
        and int(metrics.get("polymer_chain_count") or 0) < HIGH_ORDER_MIN_POLYMER_CHAINS
    )


def limited_assembly_ids(entry_payload: dict[str, Any]) -> tuple[list[str], bool, int]:
    ids = (
        entry_payload.get("rcsb_entry_container_identifiers", {}).get("assembly_ids")
        or ["1"]
    )
    normalized = [str(value) for value in ids if str(value)]
    total = len(normalized)
    return (normalized[:MAX_ASSEMBLIES_PER_ENTRY] or ["1"], total > MAX_ASSEMBLIES_PER_ENTRY, total)


def query_surface_groups(query_names: list[str]) -> list[str]:
    groups = set()
    for name in query_names:
        if name.startswith("orc_occm_mcm_component_text:"):
            groups.add("orc_occm_mcm_component_text")
        elif name.startswith("non_orc_aaa_atpase_component_text:"):
            groups.add("non_orc_aaa_atpase_component_text")
        elif name.startswith("epk_safety_component_text:"):
            groups.add("epk_safety_component_text")
        elif name == "fixed_control_positive_counterexample_or_pressure":
            groups.add("fixed_control")
        elif name == "prior_assembly_split_or_v4_seed":
            groups.add("prior_assembly_split_or_v4_seed")
    return sorted(groups)


def is_non_epk_counterexample_context(row: dict[str, Any]) -> bool:
    if row.get("known_epk_positive_input"):
        return False
    if row.get("known_orc_counterexample_input"):
        return True
    if row.get("deposited_orc_mcm_role_tokens"):
        return True
    return not bool(row.get("probable_epk_from_context"))


def context_priority(context: dict[str, Any]) -> tuple[int, str, str]:
    entry = context["entry_row"]
    ctx = context["context_row"]
    split = bool(ctx.get("deposited_v4_context_below_chain_floor"))
    if entry.get("known_orc_counterexample_input") and split:
        priority = 0
    elif entry.get("deposited_orc_mcm_role_tokens") and split:
        priority = 1
    elif "orc_occm_mcm_component_text" in entry.get("query_surface_groups", []) and split:
        priority = 2
    elif "non_orc_aaa_atpase_component_text" in entry.get("query_surface_groups", []) and split:
        priority = 3
    elif entry.get("known_epk_positive_input"):
        priority = 4
    elif "epk_safety_component_text" in entry.get("query_surface_groups", []):
        priority = 5
    elif split:
        priority = 6
    else:
        priority = 7
    return priority, str(entry["pdb_id"]), str(ctx["coordinate_context"])


def fetch_entry_contexts(
    pdb_id: str,
    index: int,
    query_names: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str]]:
    deposited_cif = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
    entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    deposited_atoms, deposited_parse_meta = ns.parse_atom_site_raw(deposited_cif)
    deposited_entity_descriptions = orc.entity_descriptions_from_cif(deposited_cif)
    text = prior.context_text(entry_payload, deposited_entity_descriptions)
    role_tokens = orc.deposited_role_tokens(text)
    probable_epk = orc.probable_epk(pdb_id, text)
    kinase_tokens = high_order.entity_kinase_tokens(deposited_entity_descriptions)
    groups = query_surface_groups(query_names)
    deposited_metrics = orc.source_free_multisite_metrics(deposited_atoms)
    deposited_v4 = high_order.v4_hit(deposited_metrics)
    assembly_ids, assembly_capped, assembly_count = limited_assembly_ids(entry_payload)

    context_rows: list[dict[str, Any]] = [
        {
            "pdb_id": pdb_id,
            "coordinate_context": "deposited_atom_site",
            "assembly_id": None,
            "parse_meta": deposited_parse_meta,
            "source_free_multisite_metrics": compact_metrics(deposited_metrics),
            "v4_oligomeric_atp_terminals_no_mg_required_hit": deposited_v4,
            "deposited_v4_context_below_chain_floor": False,
            "fetch_status": "ok",
        }
    ]
    cif_by_context = {"deposited_atom_site": deposited_cif}
    assembly_fetch_errors: dict[str, str] = {}
    any_assembly_v4 = False
    any_assembly_chain_floor_split = False

    for assembly_id in assembly_ids:
        context = f"biological_assembly_{assembly_id}"
        try:
            assembly_cif = base.fetch_text(
                RCSB_ASSEMBLY_CIF_URL.format(pdb_id=pdb_id, assembly_id=assembly_id)
            )
            assembly_atoms, assembly_parse_meta = ns.parse_atom_site_raw(assembly_cif)
            assembly_metrics = orc.source_free_multisite_metrics(assembly_atoms)
            assembly_v4 = high_order.v4_hit(assembly_metrics)
            split = bool(deposited_v4 and not assembly_v4 and chain_floor_split(assembly_metrics))
            any_assembly_v4 = any_assembly_v4 or assembly_v4
            any_assembly_chain_floor_split = any_assembly_chain_floor_split or split
            context_rows.append(
                {
                    "pdb_id": pdb_id,
                    "coordinate_context": context,
                    "assembly_id": assembly_id,
                    "parse_meta": assembly_parse_meta,
                    "source_free_multisite_metrics": compact_metrics(assembly_metrics),
                    "v4_oligomeric_atp_terminals_no_mg_required_hit": assembly_v4,
                    "deposited_v4_context_below_chain_floor": split,
                    "fetch_status": "ok",
                }
            )
            cif_by_context[context] = assembly_cif
        except Exception as exc:  # pragma: no cover - network evidence
            assembly_fetch_errors[context] = repr(exc)
        time.sleep(0.04)

    entry_level_any_context_v4 = bool(deposited_v4 or any_assembly_v4)
    entry_row = {
        "pdb_id": pdb_id,
        "surface_order": index,
        "query_names": query_names,
        "query_surface_groups": groups,
        "title": entry_payload.get("struct", {}).get("title", ""),
        "keywords": entry_payload.get("struct_keywords", {}),
        "entity_descriptions_compact": deposited_entity_descriptions[:16],
        "entity_kinase_tokens": kinase_tokens,
        "known_epk_positive_input": pdb_id in high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS,
        "known_orc_counterexample_input": pdb_id in high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS,
        "known_pressure_id_input": pdb_id in high_order.PRESSURE_IDS,
        "probable_epk_from_context": probable_epk,
        "deposited_orc_mcm_role_tokens": role_tokens,
        "deposited_v4_oligomeric_atp_terminals_no_mg_required_hit": deposited_v4,
        "entry_level_any_context_v4_guard_hit_review_only": entry_level_any_context_v4,
        "biological_assembly_declared_count": assembly_count,
        "biological_assembly_ids_reviewed": assembly_ids,
        "biological_assembly_cap_applied": assembly_capped,
        "assembly_fetch_error_count": len(assembly_fetch_errors),
        "assembly_fetch_errors": assembly_fetch_errors,
        "assembly_v4_context_count": sum(
            1 for row in context_rows if row["coordinate_context"] != "deposited_atom_site"
            and row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
        ),
        "assembly_below_chain_floor_split_context_count": sum(
            1 for row in context_rows if row.get("deposited_v4_context_below_chain_floor")
        ),
        "assembly_below_chain_floor_split_contexts": [
            row["coordinate_context"]
            for row in context_rows
            if row.get("deposited_v4_context_below_chain_floor")
        ],
        "deposited_source_free_multisite_metrics": compact_metrics(deposited_metrics),
        "reviewed": True,
    }
    entry_row["non_epk_for_counterexample_review"] = is_non_epk_counterexample_context(entry_row)
    entry_row["entry_split_risk_review_only"] = bool(
        deposited_v4 and any_assembly_chain_floor_split
    )
    return entry_row, context_rows, cif_by_context


def select_materializer_contexts(
    entry_rows: list[dict[str, Any]],
    context_rows_by_pdb: dict[str, list[dict[str, Any]]],
    max_materializer_contexts: int,
) -> list[dict[str, Any]]:
    contexts: list[dict[str, Any]] = []
    entries_by_pdb = {row["pdb_id"]: row for row in entry_rows}
    for entry in entry_rows:
        pdb_id = entry["pdb_id"]
        for context_row in context_rows_by_pdb[pdb_id]:
            include = False
            if context_row.get("deposited_v4_context_below_chain_floor"):
                include = True
            if entry.get("known_epk_positive_input") and entry.get(
                "entry_level_any_context_v4_guard_hit_review_only"
            ):
                include = True
            if entry.get("known_orc_counterexample_input") and context_row["coordinate_context"] == "deposited_atom_site":
                include = True
            if include:
                contexts.append({"entry_row": entries_by_pdb[pdb_id], "context_row": context_row})
    contexts = sorted(contexts, key=context_priority)
    return contexts[:max_materializer_contexts]


def materializer_context_summary(
    repo_root: Path,
    started_at: str,
    entry: dict[str, Any],
    context_row: dict[str, Any],
    cif_text: str,
) -> dict[str, Any]:
    materializer = ns.materializer_probe(
        repo_root=repo_root,
        started_at=started_at,
        pressure_ids=[entry["pdb_id"]],
        cif_text_by_pdb={entry["pdb_id"]: cif_text},
    )
    row = (materializer.get("rows") or [{}])[0]
    hits = [
        hit
        for hit in row.get("heteromeric_candidate_hits", []) or []
        if isinstance(hit, dict)
    ]
    substrate_hits = [hit for hit in hits if prior.substrate_mode_hit(hit)]
    flags = orc.topology_flags(substrate_hits)
    topology_clear = bool(substrate_hits) and not flags["topology_ambiguity_counteraxis_hit"]
    known_positive = bool(entry.get("known_epk_positive_input"))
    non_epk = bool(entry.get("non_epk_for_counterexample_review"))
    context_v4 = bool(context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))
    entry_guard = bool(entry.get("entry_level_any_context_v4_guard_hit_review_only"))

    if known_positive and topology_clear and context_v4:
        decision = "known_epk_positive_lost_to_context_v4_review_only"
    elif known_positive and topology_clear and entry_guard:
        decision = "known_epk_positive_lost_to_entry_level_guard_review_only"
    elif known_positive and topology_clear:
        decision = "known_epk_positive_retained_review_only"
    elif non_epk and topology_clear and context_v4:
        decision = "non_epk_counterexample_blocked_by_context_v4_review_only"
    elif non_epk and topology_clear and entry_guard:
        decision = "non_epk_counterexample_closed_by_entry_level_guard_review_only"
    elif non_epk and topology_clear:
        decision = "non_epk_counterexample_residual_after_entry_level_guard_review_only"
    elif topology_clear and context_v4:
        decision = "topology_clear_hit_blocked_by_context_v4_review_only"
    elif topology_clear and entry_guard:
        decision = "topology_clear_hit_closed_by_entry_level_guard_review_only"
    elif topology_clear:
        decision = "topology_clear_hit_residual_after_entry_level_guard_review_only"
    elif substrate_hits and flags["topology_ambiguity_counteraxis_hit"]:
        decision = "substrate_mode_hit_blocked_by_existing_topology_review_only"
    elif substrate_hits:
        decision = "substrate_mode_hit_unclassified_review_only"
    else:
        decision = "no_substrate_mode_materializer_hit_review_only"

    return {
        "pdb_id": entry["pdb_id"],
        "coordinate_context": context_row["coordinate_context"],
        "query_surface_groups": entry.get("query_surface_groups", []),
        "known_epk_positive_input": known_positive,
        "known_orc_counterexample_input": entry.get("known_orc_counterexample_input"),
        "probable_epk_from_context": entry.get("probable_epk_from_context"),
        "deposited_orc_mcm_role_tokens": entry.get("deposited_orc_mcm_role_tokens", []),
        "non_epk_for_counterexample_review": non_epk,
        "context_v4_oligomeric_atp_terminals_no_mg_required_hit": context_v4,
        "entry_level_any_context_v4_guard_hit_review_only": entry_guard,
        "deposited_v4_context_below_chain_floor": context_row.get(
            "deposited_v4_context_below_chain_floor"
        ),
        "context_source_free_multisite_metrics": context_row.get(
            "source_free_multisite_metrics", {}
        ),
        "candidate_status": row.get("candidate_status"),
        "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
        "substrate_mode_materializer_hit_count": len(substrate_hits),
        "topology_clear_substrate_mode_hit": topology_clear,
        **flags,
        "entry_level_guard_stress_decision": decision,
        "substrate_mode_materializer_hits": substrate_hits[:8],
    }


def compact_ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(row["pdb_id"]) for row in rows if row.get(key))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-unique-ids", type=int, default=MAX_UNIQUE_IDS)
    parser.add_argument("--max-materializer-contexts", type=int, default=MAX_MATERIALIZER_CONTEXTS)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids(
        repo_root,
        args.max_unique_ids,
    )
    entry_rows: list[dict[str, Any]] = []
    context_rows_by_pdb: dict[str, list[dict[str, Any]]] = {}
    cif_text_by_pdb_context: dict[tuple[str, str], str] = {}
    fetch_errors: dict[str, str] = {}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            entry_row, context_rows, cif_by_context = fetch_entry_contexts(
                pdb_id,
                index,
                id_to_queries.get(pdb_id, []),
            )
            entry_rows.append(entry_row)
            context_rows_by_pdb[pdb_id] = context_rows
            for context, cif_text in cif_by_context.items():
                cif_text_by_pdb_context[(pdb_id, context)] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        if index % 20 == 0:
            print(
                json.dumps(
                    {
                        "progress_entries_reviewed": len(entry_rows),
                        "progress_fetch_errors": len(fetch_errors),
                        "last_index": index,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        time.sleep(0.05)

    selected_contexts = select_materializer_contexts(
        entry_rows,
        context_rows_by_pdb,
        args.max_materializer_contexts,
    )
    materializer_rows: list[dict[str, Any]] = []
    materializer_context_errors: dict[str, str] = {}
    for index, selected in enumerate(selected_contexts, start=1):
        entry = selected["entry_row"]
        context_row = selected["context_row"]
        key = (entry["pdb_id"], context_row["coordinate_context"])
        try:
            materializer_rows.append(
                materializer_context_summary(
                    repo_root,
                    args.started_at,
                    entry,
                    context_row,
                    cif_text_by_pdb_context[key],
                )
            )
        except Exception as exc:  # pragma: no cover - network evidence
            materializer_context_errors[f"{key[0]}:{key[1]}"] = repr(exc)
        if index % 25 == 0:
            print(
                json.dumps(
                    {
                        "progress_materializer_contexts": index,
                        "progress_materializer_errors": len(materializer_context_errors),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        time.sleep(0.03)

    split_risk_rows = [row for row in entry_rows if row.get("entry_split_risk_review_only")]
    decision_counts = Counter(
        str(row.get("entry_level_guard_stress_decision") or "")
        for row in materializer_rows
    )
    current_context_residual_rows = [
        row
        for row in materializer_rows
        if row.get("entry_level_guard_stress_decision")
        in {
            "non_epk_counterexample_closed_by_entry_level_guard_review_only",
            "topology_clear_hit_closed_by_entry_level_guard_review_only",
        }
        and row.get("deposited_v4_context_below_chain_floor")
    ]
    entry_level_residual_rows = [
        row
        for row in materializer_rows
        if row.get("entry_level_guard_stress_decision")
        in {
            "non_epk_counterexample_residual_after_entry_level_guard_review_only",
            "topology_clear_hit_residual_after_entry_level_guard_review_only",
        }
    ]
    entry_level_positive_lost_rows = [
        row
        for row in materializer_rows
        if row.get("entry_level_guard_stress_decision")
        == "known_epk_positive_lost_to_entry_level_guard_review_only"
    ]
    context_positive_lost_rows = [
        row
        for row in materializer_rows
        if row.get("entry_level_guard_stress_decision")
        == "known_epk_positive_lost_to_context_v4_review_only"
    ]
    entry_level_closed_non_epk_rows = [
        row
        for row in materializer_rows
        if row.get("entry_level_guard_stress_decision")
        == "non_epk_counterexample_closed_by_entry_level_guard_review_only"
    ]

    context_row_count = sum(len(rows) for rows in context_rows_by_pdb.values())
    split_context_rows = [
        context_row
        for rows in context_rows_by_pdb.values()
        for context_row in rows
        if context_row.get("deposited_v4_context_below_chain_floor")
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_entry_level_assembly_guard_stress",
            "rule_under_attack": (
                "assembly-context v4_oligomeric_atp_terminals_no_mg_required "
                "sufficiency for review-only ePK substrate-mode/source-free topology "
                "false-positive control"
            ),
            "guard_variant_under_test": (
                "entry_level_any_context_v4_review_only: deposited atom_site OR any "
                "reviewed biological assembly satisfies v4"
            ),
            "query_surface": {
                "fixed_control_ids": FIXED_CONTROL_IDS,
                "orc_occm_mcm_component_queries": ORC_MCM_COMPONENT_QUERIES,
                "non_orc_aaa_atpase_component_queries": NON_ORC_ATPASE_COMPONENT_QUERIES,
                "epk_safety_component_queries": EPK_SAFETY_COMPONENT_QUERIES,
                "prior_assembly_artifacts": [str(path) for path in PRIOR_ASSEMBLY_ARTIFACTS],
                "max_unique_ids": args.max_unique_ids,
                "max_assemblies_per_entry": MAX_ASSEMBLIES_PER_ENTRY,
                "max_materializer_contexts": args.max_materializer_contexts,
                "chain_floor_split_filter": {
                    "deposited_v4_required": True,
                    "assembly_terminal_p_min": HIGH_ORDER_MIN_GAMMA_TERMINAL_P,
                    "assembly_polymer_chain_lt": HIGH_ORDER_MIN_POLYMER_CHAINS,
                },
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "entry_rows_reviewed": len(entry_rows),
            "coordinate_context_rows_reviewed": context_row_count,
            "fetch_error_count": len(fetch_errors),
            "assembly_context_cap_applied_entry_count": sum(
                1 for row in entry_rows if row.get("biological_assembly_cap_applied")
            ),
            "deposited_v4_entry_count": sum(
                1 for row in entry_rows if row.get("deposited_v4_oligomeric_atp_terminals_no_mg_required_hit")
            ),
            "entry_level_any_context_v4_guard_hit_entry_count": sum(
                1 for row in entry_rows if row.get("entry_level_any_context_v4_guard_hit_review_only")
            ),
            "split_risk_entry_count": len(split_risk_rows),
            "split_risk_pdb_ids": compact_ids(split_risk_rows, "entry_split_risk_review_only"),
            "split_context_count": len(split_context_rows),
            "materializer_context_input_count": len(selected_contexts),
            "materializer_context_error_count": len(materializer_context_errors),
            "materializer_decision_counts": dict(sorted(decision_counts.items())),
            "current_context_v4_residual_closed_by_entry_level_count": len(
                current_context_residual_rows
            ),
            "current_context_v4_residual_closed_by_entry_level_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in current_context_residual_rows
            ),
            "entry_level_non_epk_counterexample_closed_count": len(entry_level_closed_non_epk_rows),
            "entry_level_non_epk_counterexample_closed_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in entry_level_closed_non_epk_rows
            ),
            "entry_level_residual_counterexample_count": len(entry_level_residual_rows),
            "entry_level_residual_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in entry_level_residual_rows
            ),
            "entry_level_known_epk_positive_lost_count": len(entry_level_positive_lost_rows),
            "entry_level_known_epk_positive_lost_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in entry_level_positive_lost_rows
            ),
            "context_v4_known_epk_positive_lost_count": len(context_positive_lost_rows),
            "context_v4_known_epk_positive_lost_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in context_positive_lost_rows
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
        "materializer_context_errors": materializer_context_errors,
        "entry_review_rows": entry_rows,
        "coordinate_context_review_rows": [
            row for rows in context_rows_by_pdb.values() for row in rows
        ],
        "split_risk_entry_rows": split_risk_rows,
        "selected_materializer_context_rows": [
            {
                "pdb_id": selected["entry_row"]["pdb_id"],
                "coordinate_context": selected["context_row"]["coordinate_context"],
                "context_priority": context_priority(selected)[0],
            }
            for selected in selected_contexts
        ],
        "entry_level_guard_materializer_rows": materializer_rows,
        "current_context_v4_residual_closed_by_entry_level_rows": current_context_residual_rows,
        "entry_level_residual_counterexample_rows": entry_level_residual_rows,
        "entry_level_known_epk_positive_lost_rows": entry_level_positive_lost_rows,
        "warnings": [
            "Review-only guard stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Deposited and assembly CIFs were fetched in memory only and reduced to compact metrics/materializer evidence.",
            "The entry-level guard variant is research evidence only and is not a production rule.",
            "Assembly enumeration is capped per entry; cap applications are counted in metadata.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
