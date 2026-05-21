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
import math
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
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MATERIALIZER_GAMMA_CODES = {"ACP", "ANP", "ATP", "DTP"}
ACCEPTOR_ATOMS = {"SER": "OG", "THR": "OG1", "TYR": "OH"}

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


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return (
        str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "")
        .upper()
        .replace('"', "")
    )


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def preferred_seq_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    return math.sqrt(
        (float(left["Cartn_x"]) - float(right["Cartn_x"])) ** 2
        + (float(left["Cartn_y"]) - float(right["Cartn_y"])) ** 2
        + (float(left["Cartn_z"]) - float(right["Cartn_z"])) ** 2
    )


def polymer_entity_by_chain(cif_text: str) -> dict[str, str]:
    atoms, _parse_meta = ns.parse_atom_site_raw(cif_text)
    mapping: dict[str, str] = {}
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        entity_id = str(atom.get("label_entity_id") or "")
        if not entity_id:
            continue
        for key in ("auth_asym_id", "label_asym_id"):
            chain_id = str(atom.get(key) or "")
            if chain_id and chain_id not in mapping:
                mapping[chain_id] = entity_id
    return mapping


def local_substrate_geometry(cif_text: str) -> dict[str, Any]:
    atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and (
            atom_code(atom) == "MG"
            or str(atom.get("type_symbol") or "").upper() == "MG"
        )
    ]
    gamma_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom.get("type_symbol") == "P"
        and atom_code(atom) in MATERIALIZER_GAMMA_CODES
        and atom_name(atom) == "PG"
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "ATOM"
        and ACCEPTOR_ATOMS.get(atom_code(atom)) == atom_name(atom)
    ]
    hits: list[dict[str, Any]] = []
    chain_pairs: list[tuple[str, str]] = []
    for gamma_atom in gamma_atoms:
        mg_distances = [distance(gamma_atom, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        for acceptor in acceptor_atoms:
            d = distance(gamma_atom, acceptor)
            if d > DISTANCE_CUTOFF_ANGSTROM:
                continue
            residue = atom_code(acceptor)
            seq_id = ns.optional_int(preferred_seq_id(acceptor))
            tyrosine = residue == "TYR"
            n_terminal = bool(
                residue in ACCEPTOR_ATOMS
                and seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
            )
            if not (tyrosine or n_terminal):
                continue
            candidate_chain = preferred_chain(acceptor)
            gamma_chain = preferred_chain(gamma_atom)
            if candidate_chain and gamma_chain:
                chain_pairs.append((candidate_chain, gamma_chain))
            hits.append(
                {
                    "candidate_chain_name": candidate_chain,
                    "candidate_auth_seq_id": preferred_seq_id(acceptor),
                    "candidate_residue_code": residue,
                    "candidate_atom_name": atom_name(acceptor),
                    "candidate_label_entity_id": acceptor.get("label_entity_id"),
                    "gamma_associated_polymer_chain_name": gamma_chain,
                    "gamma_label_entity_id": gamma_atom.get("label_entity_id"),
                    "gamma_ligand_code": atom_code(gamma_atom),
                    "gamma_atom_name": atom_name(gamma_atom),
                    "nearest_gamma_distance_angstrom": round(d, 3),
                    "nearest_mg_distance_angstrom": (
                        round(nearest_mg, 3) if nearest_mg is not None else None
                    ),
                    "tyrosine_acceptor": tyrosine,
                    "n_terminal_acceptor": n_terminal,
                    "near_mg": bool(
                        nearest_mg is not None
                        and nearest_mg <= MG_DISTANCE_CUTOFF_ANGSTROM
                    ),
                }
            )
    same_chain = any(candidate == gamma for candidate, gamma in chain_pairs)
    reciprocal = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for index, (left_candidate, left_gamma) in enumerate(chain_pairs)
        for right_candidate, right_gamma in chain_pairs[index + 1 :]
    )
    hits.sort(
        key=lambda hit: (
            0 if hit["tyrosine_acceptor"] else 1,
            0 if hit["near_mg"] else 1,
            float(hit["nearest_gamma_distance_angstrom"]),
        )
    )
    return {
        "parse_meta": parse_meta,
        "local_gamma_acceptor_substrate_geometry_hit_count": len(hits),
        "local_gamma_acceptor_substrate_geometry_topology_clear": bool(
            hits and not (same_chain or reciprocal)
        ),
        "local_same_chain_topology_detected": same_chain,
        "local_reciprocal_cross_chain_topology_detected": reciprocal,
        "local_geometry_hits": hits[:8],
    }


def local_geometry_entity_evaluations(
    cif_text: str,
    local_geometry: dict[str, Any],
) -> list[dict[str, Any]]:
    chain_entities = polymer_entity_by_chain(cif_text)
    evaluations = []
    for hit in local_geometry.get("local_geometry_hits", []) or []:
        if not isinstance(hit, dict):
            continue
        acceptor_chain = str(hit.get("candidate_chain_name") or "")
        gamma_chain = str(hit.get("gamma_associated_polymer_chain_name") or "")
        acceptor_entity = str(
            hit.get("candidate_label_entity_id")
            or chain_entities.get(acceptor_chain)
            or ""
        )
        gamma_entity = str(chain_entities.get(gamma_chain) or "")
        same_chain = bool(acceptor_chain and acceptor_chain == gamma_chain)
        same_entity = bool(
            acceptor_entity and gamma_entity and acceptor_entity == gamma_entity
        )
        reject_reasons = []
        if same_chain:
            reject_reasons.append("same_author_chain_topology")
        if same_entity:
            reject_reasons.append(
                "acceptor_entity_equals_gamma_associated_polymer_entity"
            )
        if not gamma_entity:
            reject_reasons.append("gamma_associated_polymer_entity_unmapped")
        evaluations.append(
            {
                "candidate_chain_name": acceptor_chain,
                "candidate_auth_seq_id": hit.get("candidate_auth_seq_id"),
                "candidate_residue_code": hit.get("candidate_residue_code"),
                "candidate_atom_name": hit.get("candidate_atom_name"),
                "acceptor_entity_id": acceptor_entity or None,
                "gamma_associated_polymer_chain_name": gamma_chain,
                "gamma_associated_polymer_entity_id": gamma_entity or None,
                "gamma_ligand_code": hit.get("gamma_ligand_code"),
                "gamma_atom_name": hit.get("gamma_atom_name"),
                "nearest_gamma_distance_angstrom": hit.get(
                    "nearest_gamma_distance_angstrom"
                ),
                "nearest_mg_distance_angstrom": hit.get(
                    "nearest_mg_distance_angstrom"
                ),
                "same_author_chain_topology": same_chain,
                "same_entity_reuse_topology": same_entity,
                "materializer_heteromeric_entity_eligible": bool(
                    acceptor_entity and gamma_entity and not same_entity
                ),
                "materializer_reject_reasons": reject_reasons
                or ["none_for_this_local_hit"],
            }
        )
    return evaluations


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
    heteromeric_local = bool(ctx.get("local_geometry_materializer_equivalent_hit_count"))
    if entry.get("known_orc_counterexample_input") and split:
        priority = 0
    elif (
        "non_orc_aaa_atpase_component_text" in entry.get("query_surface_groups", [])
        and split
        and heteromeric_local
    ):
        priority = 1
    elif entry.get("deposited_orc_mcm_role_tokens") and split:
        priority = 2
    elif "orc_occm_mcm_component_text" in entry.get("query_surface_groups", []) and split:
        priority = 3
    elif "non_orc_aaa_atpase_component_text" in entry.get("query_surface_groups", []) and split:
        priority = 4
    elif entry.get("known_epk_positive_input"):
        priority = 5
    elif "epk_safety_component_text" in entry.get("query_surface_groups", []):
        priority = 6
    elif split:
        priority = 7
    else:
        priority = 8
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
    local_evaluations = context_row.get("local_geometry_entity_mapping_evaluations", [])
    local_heteromeric_count = int(
        context_row.get("local_geometry_materializer_equivalent_hit_count") or 0
    )
    non_orc_split_heteromeric = bool(
        non_epk
        and not entry.get("known_orc_counterexample_input")
        and not entry.get("deposited_orc_mcm_role_tokens")
        and context_row.get("deposited_v4_context_below_chain_floor")
        and "non_orc_aaa_atpase_component_text"
        in entry.get("query_surface_groups", [])
        and local_heteromeric_count > 0
    )

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
        "local_substrate_geometry": context_row.get("local_substrate_geometry", {}),
        "local_geometry_entity_mapping_evaluations": local_evaluations,
        "local_geometry_materializer_equivalent_hit_count": local_heteromeric_count,
        "pre_materializer_heteromeric_entity_eligible": local_heteromeric_count > 0,
        "non_orc_deposited_v4_assembly_below_floor_heteromeric_candidate": (
            non_orc_split_heteromeric
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
    parser.add_argument(
        "--extra-pdb-id",
        action="append",
        default=[],
        help="Explicit PDB ID to include, repeatable or comma-separated.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids(
        repo_root,
        args.max_unique_ids,
    )
    explicit_extra_ids: list[str] = []
    for value in args.extra_pdb_id:
        for pdb_id in str(value).split(","):
            normalized = pdb_id.strip().upper()
            if not normalized:
                continue
            explicit_extra_ids.append(normalized)
            add_id(ordered_ids, id_to_queries, normalized, "explicit_retry_or_seed_pdb_id")
    query_counts["explicit_retry_or_seed_pdb_ids"] = len(set(explicit_extra_ids))
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
            for context_row in context_rows:
                context_name = context_row["coordinate_context"]
                cif_text = cif_by_context[context_name]
                local_geometry = local_substrate_geometry(cif_text)
                local_evaluations = local_geometry_entity_evaluations(
                    cif_text,
                    local_geometry,
                )
                context_row["local_substrate_geometry"] = local_geometry
                context_row["local_geometry_entity_mapping_evaluations"] = (
                    local_evaluations
                )
                context_row["local_geometry_materializer_equivalent_hit_count"] = sum(
                    1
                    for evaluation in local_evaluations
                    if evaluation.get("materializer_heteromeric_entity_eligible")
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
    non_orc_split_context_rows = [
        context_row
        for entry in entry_rows
        for context_row in context_rows_by_pdb.get(entry["pdb_id"], [])
        if context_row.get("deposited_v4_context_below_chain_floor")
        and "non_orc_aaa_atpase_component_text" in entry.get("query_surface_groups", [])
        and not entry.get("known_orc_counterexample_input")
        and not entry.get("deposited_orc_mcm_role_tokens")
    ]
    heteromeric_split_context_rows = [
        row
        for row in split_context_rows
        if int(row.get("local_geometry_materializer_equivalent_hit_count") or 0) > 0
    ]
    non_orc_heteromeric_split_context_rows = [
        row
        for row in non_orc_split_context_rows
        if int(row.get("local_geometry_materializer_equivalent_hit_count") or 0) > 0
    ]
    non_orc_heteromeric_materializer_rows = [
        row
        for row in materializer_rows
        if row.get("non_orc_deposited_v4_assembly_below_floor_heteromeric_candidate")
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
                "explicit_retry_or_seed_pdb_ids": sorted(set(explicit_extra_ids)),
                "chain_floor_split_filter": {
                    "deposited_v4_required": True,
                    "assembly_terminal_p_min": HIGH_ORDER_MIN_GAMMA_TERMINAL_P,
                    "assembly_polymer_chain_lt": HIGH_ORDER_MIN_POLYMER_CHAINS,
                    "local_geometry_filter": {
                        "gamma_acceptor_distance_cutoff_angstrom": DISTANCE_CUTOFF_ANGSTROM,
                        "mg_distance_cutoff_angstrom": MG_DISTANCE_CUTOFF_ANGSTROM,
                        "n_terminal_acceptor_auth_seq_id_max": MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
                        "acceptor_atoms": ACCEPTOR_ATOMS,
                        "gamma_ligand_codes": sorted(MATERIALIZER_GAMMA_CODES),
                    },
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
            "split_context_with_pre_materializer_heteromeric_entity_count": len(
                heteromeric_split_context_rows
            ),
            "split_context_with_pre_materializer_heteromeric_entity_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in heteromeric_split_context_rows
            ),
            "non_orc_split_context_count": len(non_orc_split_context_rows),
            "non_orc_split_with_pre_materializer_heteromeric_entity_count": len(
                non_orc_heteromeric_split_context_rows
            ),
            "non_orc_split_with_pre_materializer_heteromeric_entity_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in non_orc_heteromeric_split_context_rows
            ),
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
            "non_orc_deposited_v4_assembly_below_floor_heteromeric_materialized_count": len(
                non_orc_heteromeric_materializer_rows
            ),
            "non_orc_deposited_v4_assembly_below_floor_heteromeric_materialized_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in non_orc_heteromeric_materializer_rows
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
        "non_orc_deposited_v4_assembly_below_floor_heteromeric_materializer_rows": (
            non_orc_heteromeric_materializer_rows
        ),
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
