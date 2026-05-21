#!/usr/bin/env python3
"""Stress entry-level v4 overblock risk on expanded ePK assemblies.

This helper follows the 5UJ7 entry-level guard thread, but aims at the next
failure mode: source-context ePK biological assembly candidates beyond the
fixed positive panel. It also probes later-offset non-ORC ATPase entries for
deposited-v4 / assembly-chain-floor split risk. CIFs are fetched in memory only
and reduced to compact context/materializer evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import v4_entry_level_assembly_guard_stress as entry_guard
import v4_high_order_epk_atpase_overblock_stress as high_order


LANE_ID = "epk_false_positive_hunter"

SOURCE_CONTEXT_TERMS = [
    "cdpk",
    "cyclin-dependent kinase",
    "erk",
    "jnk",
    "map kinase",
    "mapk",
    "mtor",
    "p38",
    "peptide",
    "protein kinase",
    "rsk",
    "serine/threonine",
    "substrate",
    "tyrosine kinase",
]

EPK_SOURCE_CONTEXT_QUERIES = [
    {"name": "protein_kinase_peptide_atp_0", "phrase": "protein kinase peptide", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "protein_kinase_peptide_atp_75", "phrase": "protein kinase peptide", "ligand": "ATP", "start": 75, "rows": 45},
    {"name": "protein_kinase_peptide_atp_150", "phrase": "protein kinase peptide", "ligand": "ATP", "start": 150, "rows": 45},
    {"name": "protein_kinase_peptide_anp_0", "phrase": "protein kinase peptide", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "protein_kinase_peptide_anp_75", "phrase": "protein kinase peptide", "ligand": "ANP", "start": 75, "rows": 45},
    {"name": "substrate_peptide_kinase_atp_0", "phrase": "substrate peptide kinase", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "substrate_peptide_kinase_atp_80", "phrase": "substrate peptide kinase", "ligand": "ATP", "start": 80, "rows": 40},
    {"name": "substrate_peptide_kinase_anp_0", "phrase": "substrate peptide kinase", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "map_kinase_substrate_peptide_atp", "phrase": "MAP kinase substrate peptide", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "map_kinase_substrate_peptide_anp", "phrase": "MAP kinase substrate peptide", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "jnk_substrate_peptide_atp", "phrase": "JNK substrate peptide", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "jnk_substrate_peptide_anp", "phrase": "JNK substrate peptide", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "erk_substrate_peptide_atp", "phrase": "ERK substrate peptide", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "erk_substrate_peptide_anp", "phrase": "ERK substrate peptide", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "p38_map_kinase_peptide_atp", "phrase": "p38 MAP kinase peptide", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "rsk_kinase_atp_0", "phrase": "RSK kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "rsk_kinase_anp_0", "phrase": "RSK kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "cdpk_kinase_atp_0", "phrase": "CDPK kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "cdpk_kinase_anp_0", "phrase": "CDPK kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mtor_kinase_atp_0", "phrase": "mTOR kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtor_kinase_atp_50", "phrase": "mTOR kinase", "ligand": "ATP", "start": 50, "rows": 35},
    {"name": "mtor_kinase_anp_0", "phrase": "mTOR kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "protein_kinase_atp_180", "phrase": "protein kinase", "ligand": "ATP", "start": 180, "rows": 45},
    {"name": "protein_kinase_atp_270", "phrase": "protein kinase", "ligand": "ATP", "start": 270, "rows": 45},
    {"name": "protein_kinase_anp_180", "phrase": "protein kinase", "ligand": "ANP", "start": 180, "rows": 45},
    {"name": "eukaryotic_protein_kinase_atp_90", "phrase": "eukaryotic protein kinase", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "eukaryotic_protein_kinase_anp_90", "phrase": "eukaryotic protein kinase", "ligand": "ANP", "start": 90, "rows": 45},
    {"name": "protein_kinase_complex_atp_0", "phrase": "protein kinase complex", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "protein_kinase_complex_atp_90", "phrase": "protein kinase complex", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "protein_kinase_complex_anp_0", "phrase": "protein kinase complex", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "eukaryotic_protein_kinase_complex_atp", "phrase": "eukaryotic protein kinase complex", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "mek_erk_atp", "phrase": "MEK ERK", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "mek_erk_anp", "phrase": "MEK ERK", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "raf_mek_atp", "phrase": "RAF MEK", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "raf_mek_anp", "phrase": "RAF MEK", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "braf_mek_atp", "phrase": "BRAF MEK", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "braf_mek_anp", "phrase": "BRAF MEK", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "craf_mek_atp", "phrase": "CRAF MEK", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "craf_mek_anp", "phrase": "CRAF MEK", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "mapk_cascade_atp", "phrase": "MAPK cascade", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtor_complex_atp", "phrase": "mTOR complex", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtorc1_atp", "phrase": "mTORC1", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtorc2_atp", "phrase": "mTORC2", "ligand": "ATP", "start": 0, "rows": 35},
]

NON_ORC_ATPASE_LATER_OFFSET_QUERIES = [
    {"name": "aaa_atpase_atp_240", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 240, "rows": 45},
    {"name": "aaa_atpase_atp_360", "phrase": "AAA+ ATPase", "ligand": "ATP", "start": 360, "rows": 45},
    {"name": "aaa_atpase_anp_180", "phrase": "AAA+ ATPase", "ligand": "ANP", "start": 180, "rows": 45},
    {"name": "aaa_atpase_anp_300", "phrase": "AAA+ ATPase", "ligand": "ANP", "start": 300, "rows": 45},
    {"name": "abc_transporter_atp_120", "phrase": "ABC transporter ATP", "ligand": "ATP", "start": 120, "rows": 45},
    {"name": "abc_transporter_atp_240", "phrase": "ABC transporter ATP", "ligand": "ATP", "start": 240, "rows": 45},
    {"name": "abc_transporter_anp_120", "phrase": "ABC transporter ATP", "ligand": "ANP", "start": 120, "rows": 45},
    {"name": "proteasome_atpase_atp_120", "phrase": "proteasome ATPase", "ligand": "ATP", "start": 120, "rows": 45},
    {"name": "proteasome_atpase_anp_120", "phrase": "proteasome ATPase", "ligand": "ANP", "start": 120, "rows": 45},
    {"name": "helicase_atp_180", "phrase": "helicase ATP", "ligand": "ATP", "start": 180, "rows": 45},
    {"name": "helicase_atp_300", "phrase": "helicase ATP", "ligand": "ATP", "start": 300, "rows": 45},
    {"name": "helicase_anp_180", "phrase": "helicase ATP", "ligand": "ANP", "start": 180, "rows": 45},
    {"name": "clamp_loader_atp_80", "phrase": "clamp loader ATP", "ligand": "ATP", "start": 80, "rows": 35},
    {"name": "clamp_loader_anp_80", "phrase": "clamp loader ATP", "ligand": "ANP", "start": 80, "rows": 35},
    {"name": "replication_factor_c_atp_80", "phrase": "replication factor C ATP", "ligand": "ATP", "start": 80, "rows": 35},
    {"name": "replication_factor_c_anp_80", "phrase": "replication factor C ATP", "ligand": "ANP", "start": 80, "rows": 35},
    {"name": "dynein_atp_120", "phrase": "dynein ATP", "ligand": "ATP", "start": 120, "rows": 40},
    {"name": "dynein_anp_120", "phrase": "dynein ATP", "ligand": "ANP", "start": 120, "rows": 40},
    {"name": "vcp_p97_atp_60", "phrase": "VCP p97 ATP", "ligand": "ATP", "start": 60, "rows": 35},
    {"name": "vcp_p97_anp_60", "phrase": "VCP p97 ATP", "ligand": "ANP", "start": 60, "rows": 35},
    {"name": "translocase_atp_120", "phrase": "translocase ATP", "ligand": "ATP", "start": 120, "rows": 40},
]

CONTROL_IDS = sorted(
    high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
    | high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
    | high_order.PRESSURE_IDS
)


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


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


def surface_groups(query_names: list[str]) -> list[str]:
    groups = set()
    for name in query_names:
        if name.startswith("epk_source_context_text:"):
            groups.add("epk_source_context_text")
        elif name.startswith("non_orc_atpase_later_offset_text:"):
            groups.add("non_orc_atpase_later_offset_text")
        elif name == "fixed_control_positive_counterexample_or_pressure":
            groups.add("fixed_control")
    return sorted(groups)


def collect_ids(
    max_unique_ids: int,
    epk_quota: int,
    atpase_quota: int,
) -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    ordered: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}
    surface_ids: dict[str, list[str]] = {
        "epk_source_context_text": [],
        "non_orc_atpase_later_offset_text": [],
    }

    for pdb_id in CONTROL_IDS:
        add_id(ordered, id_to_queries, pdb_id, "fixed_control_positive_counterexample_or_pressure")

    for surface, queries in [
        ("epk_source_context_text", EPK_SOURCE_CONTEXT_QUERIES),
        ("non_orc_atpase_later_offset_text", NON_ORC_ATPASE_LATER_OFFSET_QUERIES),
    ]:
        for query in queries:
            name = str(query["name"])
            try:
                ids = entry_guard.component_full_text_query(query)
                query_counts[f"{surface}:{name}"] = len(ids)
            except Exception as exc:  # pragma: no cover - network evidence
                ids = []
                query_counts[f"{surface}:{name}"] = 0
                query_errors[f"{surface}:{name}"] = repr(exc)
            for pdb_id in ids:
                id_to_queries[pdb_id].append(
                    f"{surface}:{name}:{query['phrase']}:{query['ligand']}:start_{query['start']}"
                )
                if pdb_id not in surface_ids[surface]:
                    surface_ids[surface].append(pdb_id)
            time.sleep(0.12)

    for pdb_id in surface_ids["epk_source_context_text"][:epk_quota]:
        if pdb_id not in ordered:
            ordered.append(pdb_id)
    for pdb_id in surface_ids["non_orc_atpase_later_offset_text"][:atpase_quota]:
        if pdb_id not in ordered:
            ordered.append(pdb_id)

    query_counts["fixed_control_ids"] = len(CONTROL_IDS)
    query_counts["epk_source_context_unique_ids_available"] = len(
        surface_ids["epk_source_context_text"]
    )
    query_counts["epk_source_context_selected_quota"] = epk_quota
    query_counts["non_orc_atpase_later_unique_ids_available"] = len(
        surface_ids["non_orc_atpase_later_offset_text"]
    )
    query_counts["non_orc_atpase_later_selected_quota"] = atpase_quota
    return ordered[:max_unique_ids], id_to_queries, query_errors, query_counts


def entry_context_text(entry: dict[str, Any]) -> str:
    keywords = entry.get("keywords", {}) or {}
    return " ".join(
        str(part or "")
        for part in [
            entry.get("title", ""),
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
            " ".join(entry.get("entity_descriptions_compact", []) or []),
            " ".join(entry.get("query_names", []) or []),
        ]
    )


def source_context_terms(text: str) -> list[str]:
    lower = text.lower()
    return sorted(term for term in SOURCE_CONTEXT_TERMS if term in lower)


def annotate_entry(entry: dict[str, Any], context_rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups = surface_groups(entry.get("query_names", []))
    text = entry_context_text(entry)
    terms = source_context_terms(text)
    assembly_v4_contexts = [
        row["coordinate_context"]
        for row in context_rows
        if row["coordinate_context"] != "deposited_atom_site"
        and row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
    ]
    source_epk = bool(
        "epk_source_context_text" in groups
        and entry.get("probable_epk_from_context")
        and entry.get("entity_kinase_tokens")
        and terms
    )
    non_orc_later = bool(
        "non_orc_atpase_later_offset_text" in groups
        and not entry.get("probable_epk_from_context")
        and not entry.get("deposited_orc_mcm_role_tokens")
    )
    entry_guard_hit = bool(entry.get("entry_level_any_context_v4_guard_hit_review_only"))
    annotated = dict(entry)
    annotated.update(
        {
            "query_surface_groups": groups,
            "source_context_terms": terms,
            "assembly_v4_context_count": len(assembly_v4_contexts),
            "assembly_v4_contexts": assembly_v4_contexts,
            "source_context_epk_review_candidate": source_epk,
            "source_context_epk_entry_guard_candidate_review_only": bool(
                source_epk
                and entry_guard_hit
                and not entry.get("known_epk_positive_input")
            ),
            "source_context_epk_assembly_v4_candidate_review_only": bool(
                source_epk
                and assembly_v4_contexts
                and not entry.get("known_epk_positive_input")
            ),
            "non_orc_atpase_later_offset_review_candidate": non_orc_later,
            "non_orc_atpase_later_split_risk_review_only": bool(
                non_orc_later and entry.get("entry_split_risk_review_only")
            ),
            "epk_query_non_epk_v4_contaminant_review_only": bool(
                "epk_source_context_text" in groups
                and not entry.get("probable_epk_from_context")
                and not entry.get("deposited_orc_mcm_role_tokens")
                and entry_guard_hit
            ),
            "epk_query_non_epk_assembly_v4_contaminant_review_only": bool(
                "epk_source_context_text" in groups
                and not entry.get("probable_epk_from_context")
                and not entry.get("deposited_orc_mcm_role_tokens")
                and assembly_v4_contexts
            ),
        }
    )
    return annotated


def context_selection_priority(selected: dict[str, Any]) -> tuple[int, str, str]:
    entry = selected["entry_row"]
    context_row = selected["context_row"]
    context_v4 = bool(context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))
    source_epk = bool(entry.get("source_context_epk_entry_guard_candidate_review_only"))
    assembly_ctx = context_row["coordinate_context"] != "deposited_atom_site"
    split = bool(context_row.get("deposited_v4_context_below_chain_floor"))
    if source_epk and assembly_ctx and context_v4:
        priority = 0
    elif source_epk and context_v4:
        priority = 1
    elif source_epk and assembly_ctx:
        priority = 2
    elif source_epk:
        priority = 3
    elif entry.get("epk_query_non_epk_v4_contaminant_review_only") and context_v4:
        priority = 4
    elif entry.get("epk_query_non_epk_v4_contaminant_review_only") and assembly_ctx:
        priority = 5
    elif entry.get("non_orc_atpase_later_split_risk_review_only") and split:
        priority = 6
    elif entry.get("non_orc_atpase_later_split_risk_review_only"):
        priority = 7
    elif entry.get("known_epk_positive_input") and context_v4:
        priority = 8
    elif entry.get("known_orc_counterexample_input") and context_v4:
        priority = 9
    else:
        priority = 10
    return priority, str(entry["pdb_id"]), str(context_row["coordinate_context"])


def select_materializer_contexts(
    entry_rows: list[dict[str, Any]],
    context_rows_by_pdb: dict[str, list[dict[str, Any]]],
    max_materializer_contexts: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for entry in entry_rows:
        contexts = context_rows_by_pdb.get(entry["pdb_id"], [])
        source_epk = bool(entry.get("source_context_epk_entry_guard_candidate_review_only"))
        non_orc_split = bool(entry.get("non_orc_atpase_later_split_risk_review_only"))
        contaminant = bool(entry.get("epk_query_non_epk_v4_contaminant_review_only"))
        control = bool(entry.get("known_epk_positive_input") or entry.get("known_orc_counterexample_input"))
        if source_epk:
            for context_row in contexts:
                include = bool(
                    context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
                    or context_row["coordinate_context"] != "deposited_atom_site"
                    or context_row.get("deposited_v4_context_below_chain_floor")
                )
                if include:
                    selected.append({"entry_row": entry, "context_row": context_row})
        elif contaminant:
            for context_row in contexts:
                include = bool(
                    context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
                    or (
                        context_row["coordinate_context"] != "deposited_atom_site"
                        and entry.get("epk_query_non_epk_assembly_v4_contaminant_review_only")
                    )
                )
                if include:
                    selected.append({"entry_row": entry, "context_row": context_row})
        elif non_orc_split:
            for context_row in contexts:
                include = bool(
                    context_row.get("deposited_v4_context_below_chain_floor")
                    or context_row["coordinate_context"] == "deposited_atom_site"
                )
                if include:
                    selected.append({"entry_row": entry, "context_row": context_row})
        elif control:
            for context_row in contexts:
                if context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit"):
                    selected.append({"entry_row": entry, "context_row": context_row})

    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for row in selected:
        key = (row["entry_row"]["pdb_id"], row["context_row"]["coordinate_context"])
        unique.setdefault(key, row)
    return sorted(unique.values(), key=context_selection_priority)[:max_materializer_contexts]


def materializer_context_summary(
    repo_root: Path,
    started_at: str,
    entry: dict[str, Any],
    context_row: dict[str, Any],
    cif_text: str,
) -> dict[str, Any]:
    base_summary = entry_guard.materializer_context_summary(
        repo_root=repo_root,
        started_at=started_at,
        entry=entry,
        context_row=context_row,
        cif_text=cif_text,
    )
    topology_clear = bool(base_summary.get("topology_clear_substrate_mode_hit"))
    substrate_hit_count = int(base_summary.get("substrate_mode_materializer_hit_count") or 0)
    entry_guard_hit = bool(entry.get("entry_level_any_context_v4_guard_hit_review_only"))
    context_v4 = bool(context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))
    source_epk = bool(entry.get("source_context_epk_entry_guard_candidate_review_only"))
    non_orc_split = bool(entry.get("non_orc_atpase_later_split_risk_review_only"))
    contaminant = bool(entry.get("epk_query_non_epk_v4_contaminant_review_only"))
    non_epk = bool(entry.get("non_epk_for_counterexample_review"))
    existing_topology = bool(base_summary.get("topology_ambiguity_counteraxis_hit"))

    if source_epk and topology_clear and entry_guard_hit:
        decision = "source_context_epk_overblock_risk_by_entry_level_guard_review_only"
    elif source_epk and topology_clear and not entry_guard_hit:
        decision = "source_context_epk_hit_retained_by_entry_level_guard_review_only"
    elif source_epk and substrate_hit_count and existing_topology:
        decision = "source_context_epk_substrate_mode_hit_existing_topology_blocked_review_only"
    elif source_epk:
        decision = "source_context_epk_no_substrate_mode_materializer_hit_review_only"
    elif non_orc_split and non_epk and topology_clear and entry_guard_hit:
        decision = "non_orc_later_split_counterexample_closed_by_entry_level_guard_review_only"
    elif non_orc_split and non_epk and topology_clear:
        decision = "non_orc_later_split_counterexample_residual_after_entry_level_guard_review_only"
    elif non_orc_split and substrate_hit_count and existing_topology:
        decision = "non_orc_later_split_substrate_mode_hit_existing_topology_blocked_review_only"
    elif non_orc_split:
        decision = "non_orc_later_split_no_substrate_mode_materializer_hit_review_only"
    elif contaminant and non_epk and topology_clear and context_v4:
        decision = "epk_query_non_epk_v4_contaminant_counterexample_blocked_by_context_v4_review_only"
    elif contaminant and non_epk and topology_clear and entry_guard_hit:
        decision = "epk_query_non_epk_v4_contaminant_counterexample_closed_by_entry_level_guard_review_only"
    elif contaminant and non_epk and topology_clear:
        decision = "epk_query_non_epk_v4_contaminant_counterexample_residual_after_entry_level_guard_review_only"
    elif contaminant and substrate_hit_count and existing_topology:
        decision = "epk_query_non_epk_v4_contaminant_substrate_mode_hit_existing_topology_blocked_review_only"
    elif contaminant:
        decision = "epk_query_non_epk_v4_contaminant_no_substrate_mode_materializer_hit_review_only"
    else:
        decision = str(base_summary.get("entry_level_guard_stress_decision") or "unclassified")

    base_summary.update(
        {
            "source_context_terms": entry.get("source_context_terms", []),
            "source_context_epk_review_candidate": entry.get(
                "source_context_epk_review_candidate"
            ),
            "source_context_epk_entry_guard_candidate_review_only": source_epk,
            "source_context_epk_assembly_v4_candidate_review_only": entry.get(
                "source_context_epk_assembly_v4_candidate_review_only"
            ),
            "non_orc_atpase_later_offset_review_candidate": entry.get(
                "non_orc_atpase_later_offset_review_candidate"
            ),
            "non_orc_atpase_later_split_risk_review_only": non_orc_split,
            "epk_query_non_epk_v4_contaminant_review_only": contaminant,
            "epk_query_non_epk_assembly_v4_contaminant_review_only": entry.get(
                "epk_query_non_epk_assembly_v4_contaminant_review_only"
            ),
            "custom_stress_decision": decision,
        }
    )
    return base_summary


def compact_ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(row["pdb_id"]) for row in rows if row.get(key))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-unique-ids", type=int, default=340)
    parser.add_argument("--epk-quota", type=int, default=220)
    parser.add_argument("--atpase-quota", type=int, default=120)
    parser.add_argument("--max-materializer-contexts", type=int, default=220)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids(
        max_unique_ids=args.max_unique_ids,
        epk_quota=args.epk_quota,
        atpase_quota=args.atpase_quota,
    )

    entry_rows: list[dict[str, Any]] = []
    context_rows_by_pdb: dict[str, list[dict[str, Any]]] = {}
    cif_text_by_pdb_context: dict[tuple[str, str], str] = {}
    fetch_errors: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            entry_row, context_rows, cif_by_context = entry_guard.fetch_entry_contexts(
                pdb_id,
                index,
                id_to_queries.get(pdb_id, []),
            )
            annotated = annotate_entry(entry_row, context_rows)
            entry_rows.append(annotated)
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
                    repo_root=repo_root,
                    started_at=args.started_at,
                    entry=entry,
                    context_row=context_row,
                    cif_text=cif_text_by_pdb_context[key],
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

    decision_counts = Counter(
        str(row.get("custom_stress_decision") or "") for row in materializer_rows
    )
    context_count = sum(len(rows) for rows in context_rows_by_pdb.values())
    source_epk_rows = [
        row for row in entry_rows if row.get("source_context_epk_entry_guard_candidate_review_only")
    ]
    source_epk_assembly_v4_rows = [
        row for row in entry_rows if row.get("source_context_epk_assembly_v4_candidate_review_only")
    ]
    non_orc_split_rows = [
        row for row in entry_rows if row.get("non_orc_atpase_later_split_risk_review_only")
    ]
    contaminant_rows = [
        row for row in entry_rows if row.get("epk_query_non_epk_v4_contaminant_review_only")
    ]
    contaminant_assembly_v4_rows = [
        row
        for row in entry_rows
        if row.get("epk_query_non_epk_assembly_v4_contaminant_review_only")
    ]
    overblock_rows = [
        row
        for row in materializer_rows
        if row.get("custom_stress_decision")
        == "source_context_epk_overblock_risk_by_entry_level_guard_review_only"
    ]
    residual_counterexample_rows = [
        row
        for row in materializer_rows
        if row.get("custom_stress_decision")
        == "non_orc_later_split_counterexample_residual_after_entry_level_guard_review_only"
    ]
    closed_counterexample_rows = [
        row
        for row in materializer_rows
        if row.get("custom_stress_decision")
        == "non_orc_later_split_counterexample_closed_by_entry_level_guard_review_only"
    ]
    contaminant_blocked_rows = [
        row
        for row in materializer_rows
        if row.get("custom_stress_decision")
        == "epk_query_non_epk_v4_contaminant_counterexample_blocked_by_context_v4_review_only"
    ]
    contaminant_residual_rows = [
        row
        for row in materializer_rows
        if row.get("custom_stress_decision")
        == "epk_query_non_epk_v4_contaminant_counterexample_residual_after_entry_level_guard_review_only"
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_entry_level_epk_overblock_later_offset_stress",
            "rule_under_attack": (
                "entry-level any-context v4_oligomeric_atp_terminals_no_mg_required "
                "review-only guard risk on source-context ePK assemblies and later-offset "
                "non-ORC ATPase split contexts"
            ),
            "guard_variant_under_test": (
                "entry_level_any_context_v4_review_only: deposited atom_site OR any "
                "reviewed biological assembly satisfies v4"
            ),
            "query_surface": {
                "fixed_control_ids": CONTROL_IDS,
                "epk_source_context_queries": EPK_SOURCE_CONTEXT_QUERIES,
                "non_orc_atpase_later_offset_queries": NON_ORC_ATPASE_LATER_OFFSET_QUERIES,
                "max_unique_ids": args.max_unique_ids,
                "epk_quota": args.epk_quota,
                "atpase_quota": args.atpase_quota,
                "max_assemblies_per_entry": entry_guard.MAX_ASSEMBLIES_PER_ENTRY,
                "max_materializer_contexts": args.max_materializer_contexts,
                "high_order_filter": {
                    "min_gamma_capable_terminal_p_count": entry_guard.HIGH_ORDER_MIN_GAMMA_TERMINAL_P,
                    "min_polymer_chain_count": entry_guard.HIGH_ORDER_MIN_POLYMER_CHAINS,
                },
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "entry_rows_reviewed": len(entry_rows),
            "coordinate_context_rows_reviewed": context_count,
            "fetch_error_count": len(fetch_errors),
            "assembly_context_cap_applied_entry_count": sum(
                1 for row in entry_rows if row.get("biological_assembly_cap_applied")
            ),
            "entry_level_any_context_v4_guard_hit_entry_count": sum(
                1 for row in entry_rows if row.get("entry_level_any_context_v4_guard_hit_review_only")
            ),
            "source_context_epk_entry_guard_candidate_count": len(source_epk_rows),
            "source_context_epk_entry_guard_candidate_pdb_ids": compact_ids(
                source_epk_rows,
                "source_context_epk_entry_guard_candidate_review_only",
            ),
            "source_context_epk_assembly_v4_candidate_count": len(
                source_epk_assembly_v4_rows
            ),
            "source_context_epk_assembly_v4_candidate_pdb_ids": compact_ids(
                source_epk_assembly_v4_rows,
                "source_context_epk_assembly_v4_candidate_review_only",
            ),
            "non_orc_atpase_later_split_risk_count": len(non_orc_split_rows),
            "non_orc_atpase_later_split_risk_pdb_ids": compact_ids(
                non_orc_split_rows,
                "non_orc_atpase_later_split_risk_review_only",
            ),
            "epk_query_non_epk_v4_contaminant_count": len(contaminant_rows),
            "epk_query_non_epk_v4_contaminant_pdb_ids": compact_ids(
                contaminant_rows,
                "epk_query_non_epk_v4_contaminant_review_only",
            ),
            "epk_query_non_epk_assembly_v4_contaminant_count": len(
                contaminant_assembly_v4_rows
            ),
            "epk_query_non_epk_assembly_v4_contaminant_pdb_ids": compact_ids(
                contaminant_assembly_v4_rows,
                "epk_query_non_epk_assembly_v4_contaminant_review_only",
            ),
            "materializer_context_input_count": len(selected_contexts),
            "materializer_context_error_count": len(materializer_context_errors),
            "custom_stress_decision_counts": dict(sorted(decision_counts.items())),
            "source_context_epk_entry_level_overblock_risk_count": len(overblock_rows),
            "source_context_epk_entry_level_overblock_risk_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}" for row in overblock_rows
            ),
            "non_orc_later_split_residual_counterexample_count": len(
                residual_counterexample_rows
            ),
            "non_orc_later_split_residual_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in residual_counterexample_rows
            ),
            "non_orc_later_split_closed_counterexample_count": len(
                closed_counterexample_rows
            ),
            "non_orc_later_split_closed_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in closed_counterexample_rows
            ),
            "epk_query_non_epk_v4_contaminant_blocked_counterexample_count": len(
                contaminant_blocked_rows
            ),
            "epk_query_non_epk_v4_contaminant_blocked_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in contaminant_blocked_rows
            ),
            "epk_query_non_epk_v4_contaminant_residual_counterexample_count": len(
                contaminant_residual_rows
            ),
            "epk_query_non_epk_v4_contaminant_residual_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in contaminant_residual_rows
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
        "selected_materializer_context_rows": [
            {
                "pdb_id": selected["entry_row"]["pdb_id"],
                "coordinate_context": selected["context_row"]["coordinate_context"],
                "context_priority": context_selection_priority(selected)[0],
            }
            for selected in selected_contexts
        ],
        "custom_materializer_rows": materializer_rows,
        "source_context_epk_entry_level_overblock_risk_rows": overblock_rows,
        "non_orc_later_split_residual_counterexample_rows": residual_counterexample_rows,
        "non_orc_later_split_closed_counterexample_rows": closed_counterexample_rows,
        "epk_query_non_epk_v4_contaminant_blocked_counterexample_rows": contaminant_blocked_rows,
        "epk_query_non_epk_v4_contaminant_residual_counterexample_rows": contaminant_residual_rows,
        "warnings": [
            "Review-only guard stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Source-context ePK candidates are query/context review candidates, not imported labels.",
            "Deposited and assembly CIFs were fetched in memory only and reduced to compact metrics/materializer evidence.",
            "The entry-level guard variant is research evidence only and is not a production rule.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
