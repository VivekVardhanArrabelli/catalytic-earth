#!/usr/bin/env python3
"""Stress a source-free multi-ATP-site guard for ORC/Cdc6/MCM false hits.

The guard tested here uses only local coordinate-derived counts: ATP-like
terminal phosphates with nearby Mg across multiple polymer chains/entities. It
is compared with a deposited-text ORC/MCM token diagnostic, but the diagnostic
is recorded separately and is not treated as source-free.
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

import auth_namespace_edge_case_stress as ns
import atpase_substrate_mode_stress as base
import same_author_chain_entity_reuse_stress as reuse


LANE_ID = "epk_false_positive_hunter"
GAMMA_CAPABLE_CODES = {"ACP", "ANP", "ATP", "DTP"}
ACCEPTOR_CODES = {"SER", "THR", "TYR"}
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MULTISITE_MIN_GAMMA_MG_SITES = 3
MULTISITE_MIN_GAMMA_MG_CHAINS = 3
MULTISITE_MIN_POLYMER_ENTITIES = 4
MAX_UNIQUE_IDS = 180

COUNTEREXAMPLE_IDS = ["7JGR", "7JGS", "7JK2", "7JK3", "7JK4", "9BCX"]
KNOWN_EPK_POSITIVE_IDS = [
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
]
PRESSURE_IDS = ["7CAG", "8BMS", "9L3M", "9L3U", "7ZE5"]
FULL_TEXT_QUERIES = [
    {"name": "orc_cdc6_atp", "phrase": "origin recognition complex Cdc6 ATP", "rows": 35},
    {"name": "orc_cdc6_mg", "phrase": "ORC Cdc6 ATP magnesium", "rows": 35},
    {"name": "orc_mcm_atp", "phrase": "ORC Cdc6 Mcm2-7 ATP", "rows": 35},
    {"name": "mcm_orc_cdc6", "phrase": "Mcm2-7 ORC Cdc6 ATP", "rows": 35},
    {
        "name": "aaa_replication_initiator",
        "phrase": "AAA+ replication initiator ATP magnesium",
        "rows": 35,
    },
    {
        "name": "replication_initiation_atpase",
        "phrase": "replication initiation ATPase magnesium",
        "rows": 35,
    },
]
BROAD_ATPASE_QUERIES = [
    {"name": "aaa_atpase_mg", "phrase": "AAA+ ATPase ATP magnesium", "rows": 30},
    {"name": "helicase_atp_mg", "phrase": "helicase ATP magnesium", "rows": 30},
    {"name": "clamp_loader_atp_mg", "phrase": "clamp loader ATP magnesium", "rows": 30},
    {"name": "proteasome_atpase_mg", "phrase": "proteasome ATPase magnesium", "rows": 30},
    {"name": "walker_a_oligomer", "phrase": "Walker A oligomer ATP magnesium", "rows": 30},
    {"name": "p_loop_oligomer", "phrase": "P-loop NTPase oligomer ATP magnesium", "rows": 30},
]
ORC_MOTOR_QUERIES = [
    {
        "name": "origin_recognition_complex_motor",
        "phrase": "Origin Recognition Complex ATPase motor module",
        "rows": 40,
    },
    {"name": "orc_atpase_motor", "phrase": "ORC ATPase motor module", "rows": 40},
    {"name": "orc1_orc4_orc5_atp", "phrase": "ORC1 ORC4 ORC5 ATP", "rows": 40},
    {"name": "orc_o1aaa", "phrase": "ORC-O1AAA ATP", "rows": 40},
    {
        "name": "human_orc_atpase_motor",
        "phrase": "human Origin Recognition Complex ATPase motor",
        "rows": 40,
    },
]
ORC_CDK_KEYWORD_QUERIES = [
    {"name": "mcm_orc_cdk_atp", "phrase": "MCM ORC CDK ATP", "rows": 30},
    {
        "name": "orc2_regulatory_cdk",
        "phrase": "ORC2 regulatory domain CDK ATP",
        "rows": 30,
    },
    {
        "name": "mcm_double_hexamer_orc_cdk",
        "phrase": "MCM double hexamer ORC CDK ATP",
        "rows": 30,
    },
    {
        "name": "cell_cycle_orc_mcm_atp",
        "phrase": "cell cycle ORC MCM ATP",
        "rows": 30,
    },
]
TRANSPORT_MOTOR_QUERIES = [
    {
        "name": "abc_transporter_tyr_atp_mg",
        "phrase": "ABC transporter tyrosine ATP magnesium",
        "rows": 30,
    },
    {
        "name": "ftsk_hera_atpase_mg",
        "phrase": "FtsK HerA ATPase ATP magnesium",
        "rows": 30,
    },
    {
        "name": "dna_translocase_tyr_atp_mg",
        "phrase": "DNA translocase tyrosine ATP magnesium",
        "rows": 30,
    },
    {"name": "dynein_atp_mg", "phrase": "dynein ATP magnesium", "rows": 30},
    {
        "name": "aaa_unfoldase_atp_mg",
        "phrase": "AAA+ unfoldase ATP magnesium",
        "rows": 30,
    },
    {"name": "vcp_p97_atp_mg", "phrase": "VCP p97 ATP magnesium", "rows": 30},
]
QUERY_PROFILES = {
    "orc_mcm": FULL_TEXT_QUERIES,
    "orc_motor": ORC_MOTOR_QUERIES,
    "orc_cdk_keyword": ORC_CDK_KEYWORD_QUERIES,
    "transport_motor": TRANSPORT_MOTOR_QUERIES,
    "broad_atpase": BROAD_ATPASE_QUERIES,
}

ORC_MCM_ROLE_TOKENS = [
    "origin recognition complex",
    "orc",
    "cdc6",
    "mcm",
    "mcm2-7",
    "replication licensing",
    "replication initiation",
    "occ m",
    "occm",
]
EUKARYOTIC_KINASE_TOKENS = [
    "protein kinase",
    "tyrosine kinase",
    "serine/threonine-protein kinase",
    "serine/threonine protein kinase",
    "eukaryotic protein kinase",
    "mitogen-activated protein kinase",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def normalize(value: Any) -> str | None:
    text = str(value or "")
    if text in {"", ".", "?"}:
        return None
    return text


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def atom_entity(atom: dict[str, Any]) -> str | None:
    return normalize(atom.get("label_entity_id"))


def optional_int(value: Any) -> int | None:
    return ns.optional_int(value)


def substrate_mode_hit(hit: dict[str, Any]) -> bool:
    residue = str(hit.get("candidate_residue_code") or "").upper()
    seq_id = optional_int(hit.get("candidate_auth_seq_id"))
    return residue == "TYR" or (
        residue in ACCEPTOR_CODES
        and seq_id is not None
        and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    )


def collect_ids(
    full_text_queries: list[dict[str, Any]],
    retry_fetch_errors_from: str | None = None,
) -> tuple[list[str], dict[str, list[str]], dict[str, Any], dict[str, int]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, Any] = {}
    query_counts: dict[str, int] = {}

    for pdb_id in reversed(PRESSURE_IDS + KNOWN_EPK_POSITIVE_IDS + COUNTEREXAMPLE_IDS):
        id_to_queries[pdb_id].append("fixed_counterexample_positive_or_pressure_seed")
        if pdb_id in ordered_ids:
            ordered_ids.remove(pdb_id)
        ordered_ids.insert(0, pdb_id)

    if retry_fetch_errors_from:
        retry_source = json.loads(Path(retry_fetch_errors_from).read_text(encoding="utf-8"))
        retry_ids = sorted(str(pdb_id).upper() for pdb_id in retry_source.get("fetch_errors", {}))
        query_counts["retry_fetch_errors"] = len(retry_ids)
        for pdb_id in retry_ids:
            id_to_queries[pdb_id].append(f"retry_fetch_error_from:{retry_fetch_errors_from}")
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_counts

    for query in full_text_queries:
        name = str(query["name"])
        phrase = str(query["phrase"])
        try:
            ids = base.rcsb_full_text_query(phrase, int(query["rows"]))
            query_counts[name] = len(ids)
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[name] = repr(exc)
            ids = []
            query_counts[name] = 0
        for pdb_id in ids:
            id_to_queries[pdb_id].append(f"{name}:{phrase}")
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.15)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_counts


def context_text(entry_payload: dict[str, Any]) -> str:
    keywords = entry_payload.get("struct_keywords", {}) or {}
    return " ".join(
        str(part or "")
        for part in [
            entry_payload.get("struct", {}).get("title", ""),
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
        ]
    )


def entity_descriptions_from_cif(cif_text: str) -> list[str]:
    descriptions = []
    for row in reuse.parse_loop_rows(cif_text, "_entity."):
        value = normalize(row.get("pdbx_description"))
        if value:
            descriptions.append(value)
    return sorted(set(descriptions))


def deposited_role_tokens(text: str) -> list[str]:
    lower = text.lower()
    return sorted(token for token in ORC_MCM_ROLE_TOKENS if token in lower)


def probable_epk(pdb_id: str, text: str) -> bool:
    lower = text.lower()
    return (
        pdb_id.upper() in KNOWN_EPK_POSITIVE_IDS
        or base.looks_probable_epk(text)
        or any(token in lower for token in EUKARYOTIC_KINASE_TOKENS)
    )


def source_free_multisite_metrics(atoms: list[dict[str, Any]]) -> dict[str, Any]:
    polymer_chains = {
        preferred_chain(atom)
        for atom in atoms
        if atom.get("group_PDB") == "ATOM" and preferred_chain(atom)
    }
    polymer_entities = {
        atom_entity(atom)
        for atom in atoms
        if atom.get("group_PDB") == "ATOM" and atom_entity(atom)
    }
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and (atom_code(atom) == "MG" or str(atom.get("type_symbol") or "").upper() == "MG")
    ]
    terminal_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and str(atom.get("type_symbol") or "").upper() == "P"
        and atom_code(atom) in GAMMA_CAPABLE_CODES
        and atom_name(atom) == "PG"
    ]

    site_rows: list[dict[str, Any]] = []
    near_mg_chains: set[str] = set()
    near_mg_entities: set[str] = set()
    near_mg_ligands: Counter[str] = Counter()
    for terminal in terminal_atoms:
        distances = [ns.distance(terminal, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(distances) if distances else None
        if nearest_mg is None or nearest_mg > MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        chain = preferred_chain(terminal)
        entity_id = atom_entity(terminal)
        near_mg_chains.add(chain)
        if entity_id:
            near_mg_entities.add(entity_id)
        near_mg_ligands[atom_code(terminal)] += 1
        site_rows.append(
            {
                "ligand": atom_code(terminal),
                "terminal_p_atom": atom_name(terminal),
                "auth_chain": terminal.get("auth_asym_id"),
                "label_chain": terminal.get("label_asym_id"),
                "chain_name": chain,
                "entity_id": entity_id,
                "nearest_mg_distance_angstrom": round(nearest_mg, 3),
            }
        )

    guard_hit = (
        len(site_rows) >= MULTISITE_MIN_GAMMA_MG_SITES
        and len(near_mg_chains) >= MULTISITE_MIN_GAMMA_MG_CHAINS
        and len(polymer_entities) >= MULTISITE_MIN_POLYMER_ENTITIES
    )
    return {
        "gamma_capable_terminal_p_count": len(terminal_atoms),
        "gamma_capable_terminal_p_near_mg_count": len(site_rows),
        "gamma_capable_terminal_p_near_mg_chain_count": len(near_mg_chains),
        "gamma_capable_terminal_p_near_mg_entity_count": len(near_mg_entities),
        "gamma_capable_terminal_p_near_mg_ligand_counts": dict(sorted(near_mg_ligands.items())),
        "polymer_chain_count": len(polymer_chains),
        "polymer_entity_count": len(polymer_entities),
        "source_free_multisite_atpase_guard_hit": guard_hit,
        "source_free_multisite_atpase_guard_reasons": [
            reason
            for reason, ok in [
                (f"gamma_mg_sites_ge_{MULTISITE_MIN_GAMMA_MG_SITES}", len(site_rows) >= MULTISITE_MIN_GAMMA_MG_SITES),
                (f"gamma_mg_chains_ge_{MULTISITE_MIN_GAMMA_MG_CHAINS}", len(near_mg_chains) >= MULTISITE_MIN_GAMMA_MG_CHAINS),
                (f"polymer_entities_ge_{MULTISITE_MIN_POLYMER_ENTITIES}", len(polymer_entities) >= MULTISITE_MIN_POLYMER_ENTITIES),
            ]
            if ok
        ],
        "compact_gamma_mg_sites": sorted(
            site_rows,
            key=lambda row: (
                str(row.get("chain_name") or ""),
                str(row.get("ligand") or ""),
                float(row.get("nearest_mg_distance_angstrom") or 9999.0),
            ),
        )[:20],
    }


def topology_flags(hits: list[dict[str, Any]]) -> dict[str, bool]:
    blocked, same_chain, reciprocal = reuse.topology_blocked(hits)
    return {
        "same_chain_topology_detected": same_chain,
        "reciprocal_cross_chain_topology_detected": reciprocal,
        "topology_ambiguity_counteraxis_hit": blocked,
    }


def summarize_materializer_rows(
    materializer: dict[str, Any],
    rows_by_pdb: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        entry = rows_by_pdb.get(pdb_id, {})
        hits = [
            hit
            for hit in row.get("heteromeric_candidate_hits", []) or []
            if isinstance(hit, dict)
        ]
        substrate_hits = [hit for hit in hits if substrate_mode_hit(hit)]
        flags = topology_flags(substrate_hits)
        topology_clear_substrate_hit = bool(substrate_hits) and not flags[
            "topology_ambiguity_counteraxis_hit"
        ]
        known_counterexample = pdb_id in COUNTEREXAMPLE_IDS
        known_positive = pdb_id in KNOWN_EPK_POSITIVE_IDS
        non_epk = bool(entry) and not bool(entry.get("probable_epk_from_context"))
        guard_hit = bool(entry.get("source_free_multisite_atpase_guard_hit"))
        role_token_hit = bool(entry.get("deposited_orc_mcm_role_tokens"))
        if known_positive and topology_clear_substrate_hit and guard_hit:
            decision = "known_epk_positive_lost_to_multisite_guard_review_only"
        elif known_positive and topology_clear_substrate_hit:
            decision = "known_epk_positive_retained_review_only"
        elif known_counterexample and topology_clear_substrate_hit and guard_hit:
            decision = "known_counterexample_blocked_by_multisite_guard_review_only"
        elif known_counterexample and topology_clear_substrate_hit:
            decision = "known_counterexample_residual_after_multisite_guard_review_only"
        elif non_epk and topology_clear_substrate_hit and guard_hit:
            decision = "non_epk_topology_clear_hit_blocked_by_multisite_guard_review_only"
        elif non_epk and topology_clear_substrate_hit:
            decision = "non_epk_topology_clear_residual_after_multisite_guard_review_only"
        elif substrate_hits and flags["topology_ambiguity_counteraxis_hit"]:
            decision = "substrate_mode_hit_blocked_by_existing_topology_review_only"
        elif substrate_hits:
            decision = "substrate_mode_hit_unclassified_review_only"
        else:
            decision = "no_substrate_mode_materializer_hit_review_only"
        output_rows.append(
            {
                "pdb_id": pdb_id,
                "query_names": entry.get("query_names", []),
                "known_counterexample_input": known_counterexample,
                "known_epk_positive_input": known_positive,
                "probable_epk_from_context": entry.get("probable_epk_from_context"),
                "deposited_orc_mcm_role_tokens": entry.get("deposited_orc_mcm_role_tokens", []),
                "deposited_text_role_diagnostic_hit": role_token_hit,
                "source_free_multisite_atpase_guard_hit": guard_hit,
                "source_free_multisite_atpase_guard_reasons": entry.get(
                    "source_free_multisite_atpase_guard_reasons", []
                ),
                "candidate_status": row.get("candidate_status"),
                "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
                "substrate_mode_materializer_hit_count": len(substrate_hits),
                "topology_clear_substrate_mode_hit": topology_clear_substrate_hit,
                **flags,
                "guard_stress_decision": decision,
                "substrate_mode_materializer_hits": substrate_hits[:10],
                "source_free_multisite_metrics": {
                    key: entry.get(key)
                    for key in [
                        "gamma_capable_terminal_p_count",
                        "gamma_capable_terminal_p_near_mg_count",
                        "gamma_capable_terminal_p_near_mg_chain_count",
                        "gamma_capable_terminal_p_near_mg_entity_count",
                        "gamma_capable_terminal_p_near_mg_ligand_counts",
                        "polymer_chain_count",
                        "polymer_entity_count",
                    ]
                },
            }
        )
    return sorted(
        output_rows,
        key=lambda row: (
            str(row.get("guard_stress_decision") or ""),
            str(row.get("pdb_id") or ""),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--query-profile",
        choices=sorted(QUERY_PROFILES),
        default="orc_mcm",
    )
    parser.add_argument("--retry-fetch-errors-from")
    args = parser.parse_args()

    full_text_queries = QUERY_PROFILES[args.query_profile]
    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids(
        full_text_queries,
        args.retry_fetch_errors_from,
    )
    rows: list[dict[str, Any]] = []
    rows_by_pdb: dict[str, dict[str, Any]] = {}
    fetch_errors: dict[str, str] = {}
    cif_text_by_pdb: dict[str, str] = {}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
            descriptions = entity_descriptions_from_cif(cif_text)
            text = " ".join([context_text(entry_payload), " ".join(descriptions)])
            metrics = source_free_multisite_metrics(atoms)
            row = {
                "pdb_id": pdb_id,
                "surface_order": index,
                "query_names": id_to_queries.get(pdb_id, []),
                "title": entry_payload.get("struct", {}).get("title", ""),
                "keywords": entry_payload.get("struct_keywords", {}),
                "entity_descriptions_compact": descriptions[:14],
                "known_counterexample_input": pdb_id in COUNTEREXAMPLE_IDS,
                "known_epk_positive_input": pdb_id in KNOWN_EPK_POSITIVE_IDS,
                "probable_epk_from_context": probable_epk(pdb_id, text),
                "deposited_orc_mcm_role_tokens": deposited_role_tokens(text),
                "reviewed": True,
                **parse_meta,
                **metrics,
            }
            rows.append(row)
            rows_by_pdb[pdb_id] = row
            cif_text_by_pdb[pdb_id] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.08)

    materializer = ns.materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=[row["pdb_id"] for row in rows],
        cif_text_by_pdb=cif_text_by_pdb,
    )
    materializer_rows = summarize_materializer_rows(materializer, rows_by_pdb)
    decision_counts = Counter(
        str(row.get("guard_stress_decision") or "") for row in materializer_rows
    )
    known_counterexample_rows = [
        row for row in materializer_rows if row.get("known_counterexample_input")
    ]
    known_positive_rows = [
        row for row in materializer_rows if row.get("known_epk_positive_input")
    ]
    blocked_counterexample_ids = sorted(
        row["pdb_id"]
        for row in known_counterexample_rows
        if row.get("guard_stress_decision")
        == "known_counterexample_blocked_by_multisite_guard_review_only"
    )
    residual_counterexample_ids = sorted(
        row["pdb_id"]
        for row in known_counterexample_rows
        if row.get("guard_stress_decision")
        == "known_counterexample_residual_after_multisite_guard_review_only"
    )
    lost_positive_ids = sorted(
        row["pdb_id"]
        for row in known_positive_rows
        if row.get("guard_stress_decision")
        == "known_epk_positive_lost_to_multisite_guard_review_only"
    )
    retained_positive_ids = sorted(
        row["pdb_id"]
        for row in known_positive_rows
        if row.get("guard_stress_decision")
        == "known_epk_positive_retained_review_only"
    )
    role_token_topology_clear_non_epk_ids = sorted(
        row["pdb_id"]
        for row in materializer_rows
        if row.get("deposited_text_role_diagnostic_hit")
        and row.get("topology_clear_substrate_mode_hit")
        and not row.get("probable_epk_from_context")
    )
    role_token_residual_after_guard_ids = sorted(
        row["pdb_id"]
        for row in materializer_rows
        if row["pdb_id"] in role_token_topology_clear_non_epk_ids
        and not row.get("source_free_multisite_atpase_guard_hit")
    )
    non_epk_residual_after_guard_ids = sorted(
        row["pdb_id"]
        for row in materializer_rows
        if row.get("guard_stress_decision")
        == "non_epk_topology_clear_residual_after_multisite_guard_review_only"
    )

    guard_status = (
        "passes_bounded_orc_cdc6_mcm_counterexample_controls_review_only"
        if len(blocked_counterexample_ids) == len(COUNTEREXAMPLE_IDS)
        and not residual_counterexample_ids
        and not lost_positive_ids
        and not role_token_residual_after_guard_ids
        else "fails_closed_orc_cdc6_mcm_guard_stress_review_only"
    )
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "orc_mcm_multisite_guard_stress",
            "query_profile": args.query_profile,
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0 "
                "and build_epk_heteromeric_positive_coverage_candidate_scout"
            ),
            "guard_under_test": "source_free_multisite_atpase_complex_counteraxis_v0_review_only",
            "guard_status": guard_status,
            "search_surface": {
                "fixed_counterexample_ids": COUNTEREXAMPLE_IDS,
                "known_epk_positive_ids": KNOWN_EPK_POSITIVE_IDS,
                "pressure_ids": PRESSURE_IDS,
                "full_text_queries": full_text_queries,
                "retry_fetch_errors_from": args.retry_fetch_errors_from,
                "max_unique_ids": MAX_UNIQUE_IDS,
                "gamma_capable_codes": sorted(GAMMA_CAPABLE_CODES),
                "mg_distance_cutoff_angstrom": MG_DISTANCE_CUTOFF_ANGSTROM,
                "multisite_min_gamma_mg_sites": MULTISITE_MIN_GAMMA_MG_SITES,
                "multisite_min_gamma_mg_chains": MULTISITE_MIN_GAMMA_MG_CHAINS,
                "multisite_min_polymer_entities": MULTISITE_MIN_POLYMER_ENTITIES,
                "max_n_terminal_acceptor_auth_seq_id": MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
                "raw_coordinate_files_written": False,
                "deposited_text_role_diagnostic_not_source_free": True,
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(rows),
            "fetch_error_count": len(fetch_errors),
            "actual_materializer_input_count": len(rows),
            "materializer_decision_counts": dict(sorted(decision_counts.items())),
            "known_counterexample_input_count": len(COUNTEREXAMPLE_IDS),
            "known_counterexample_blocked_by_multisite_guard_count": len(blocked_counterexample_ids),
            "known_counterexample_blocked_by_multisite_guard_pdb_ids": blocked_counterexample_ids,
            "known_counterexample_residual_after_multisite_guard_count": len(residual_counterexample_ids),
            "known_counterexample_residual_after_multisite_guard_pdb_ids": residual_counterexample_ids,
            "known_epk_positive_retained_count": len(retained_positive_ids),
            "known_epk_positive_retained_pdb_ids": retained_positive_ids,
            "known_epk_positive_lost_to_multisite_guard_count": len(lost_positive_ids),
            "known_epk_positive_lost_to_multisite_guard_pdb_ids": lost_positive_ids,
            "role_token_topology_clear_non_epk_count": len(role_token_topology_clear_non_epk_ids),
            "role_token_topology_clear_non_epk_pdb_ids": role_token_topology_clear_non_epk_ids,
            "role_token_residual_after_multisite_guard_count": len(role_token_residual_after_guard_ids),
            "role_token_residual_after_multisite_guard_pdb_ids": role_token_residual_after_guard_ids,
            "non_epk_topology_clear_residual_after_multisite_guard_count": len(non_epk_residual_after_guard_ids),
            "non_epk_topology_clear_residual_after_multisite_guard_pdb_ids": non_epk_residual_after_guard_ids,
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
        "warnings": [
            "Review-only source-free guard stress; no production scoring, threshold calibration, label import, or fingerprint edit.",
            "The ORC/MCM deposited-text token diagnostic is not source-free and is recorded only as review context.",
            "The multi-site guard is bounded to replication-initiation and fixed ePK controls in this artifact.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
