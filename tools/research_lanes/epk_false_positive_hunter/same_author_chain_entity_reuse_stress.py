#!/usr/bin/env python3
"""Same-author-chain entity-reuse stress for ePK false-positive hunting.

This lane helper attacks the case where an mmCIF author chain ID is reused by
distinct polymer entities. The current review-only materializer can then report
different acceptor/gamma entities while the source-free topology counteraxis
sees the same chain name. The script writes compact evidence only; fetched
coordinates stay in memory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shlex
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import auth_namespace_edge_case_stress as ns
import atpase_substrate_mode_stress as base


LANE_ID = "epk_false_positive_hunter"
GAMMA_CAPABLE_CODES = {"ACP", "ANP", "ATP", "DTP"}
CURRENT_ATP_LIKE_LIGANDS = {"A3P", "ACP", "AGS", "ANP", "ATP"}
SCAN_LIGANDS = sorted(CURRENT_ATP_LIKE_LIGANDS | GAMMA_CAPABLE_CODES)
ACCEPTOR_CODES = {"SER": "OG", "THR": "OG1", "TYR": "OH"}
TERMINAL_P_NAMES = {"PG", "P3G", "P03", "P3", "P03G", "PG1", "PG2", "PN", "PB"}
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MAX_UNIQUE_IDS = 820

KNOWN_EPK_POSITIVE_IDS = {
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
EXTRA_EPK_CONTEXT_TOKENS = [
    "insulin receptor tyrosine kinase",
    "receptor tyrosine kinase",
    "tyrosine kinase",
    "serine/threonine-protein kinase",
    "serine/threonine protein kinase",
    "eukaryotic protein kinase",
]

COMPONENT_QUERY_SURFACE = [
    {"name": "atp_mg_start_0", "ligand": "ATP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "atp_mg_start_120", "ligand": "ATP", "metal": "MG", "start": 120, "rows": 55},
    {"name": "atp_mg_start_240", "ligand": "ATP", "metal": "MG", "start": 240, "rows": 55},
    {"name": "atp_mg_start_360", "ligand": "ATP", "metal": "MG", "start": 360, "rows": 55},
    {"name": "atp_mg_start_540", "ligand": "ATP", "metal": "MG", "start": 540, "rows": 55},
    {"name": "atp_mg_start_720", "ligand": "ATP", "metal": "MG", "start": 720, "rows": 55},
    {"name": "atp_mg_start_900", "ligand": "ATP", "metal": "MG", "start": 900, "rows": 55},
    {"name": "atp_mg_start_1080", "ligand": "ATP", "metal": "MG", "start": 1080, "rows": 55},
    {"name": "atp_mg_start_1260", "ligand": "ATP", "metal": "MG", "start": 1260, "rows": 55},
    {"name": "anp_mg_start_0", "ligand": "ANP", "metal": "MG", "start": 0, "rows": 50},
    {"name": "anp_mg_start_120", "ligand": "ANP", "metal": "MG", "start": 120, "rows": 50},
    {"name": "anp_mg_start_240", "ligand": "ANP", "metal": "MG", "start": 240, "rows": 50},
    {"name": "anp_mg_start_360", "ligand": "ANP", "metal": "MG", "start": 360, "rows": 50},
    {"name": "anp_mg_start_480", "ligand": "ANP", "metal": "MG", "start": 480, "rows": 50},
    {"name": "acp_mg_start_0", "ligand": "ACP", "metal": "MG", "start": 0, "rows": 50},
    {"name": "acp_mg_start_120", "ligand": "ACP", "metal": "MG", "start": 120, "rows": 50},
    {"name": "acp_mg_start_240", "ligand": "ACP", "metal": "MG", "start": 240, "rows": 50},
    {"name": "ags_mg_start_0", "ligand": "AGS", "metal": "MG", "start": 0, "rows": 50},
    {"name": "ags_mg_start_120", "ligand": "AGS", "metal": "MG", "start": 120, "rows": 50},
    {"name": "ags_mg_start_240", "ligand": "AGS", "metal": "MG", "start": 240, "rows": 50},
    {"name": "a3p_mg_start_0", "ligand": "A3P", "metal": "MG", "start": 0, "rows": 45},
    {"name": "a3p_mg_start_120", "ligand": "A3P", "metal": "MG", "start": 120, "rows": 45},
    {"name": "dtp_mg_start_0", "ligand": "DTP", "metal": "MG", "start": 0, "rows": 45},
    {"name": "dtp_mg_start_120", "ligand": "DTP", "metal": "MG", "start": 120, "rows": 45},
]

SEED_IDS = [
    "7CAG",
    "8BMS",
    "9L3M",
    "9L3U",
    "7ZE5",
    "5TT6",
    "6NOO",
    "9NBW",
    "4KFT",
    "1A82",
    "3C9S",
    "1N56",
    "2ZH6",
    "4RWT",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_loop_rows(cif_text: str, prefix: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [line.rstrip("\n") for line in cif_text.splitlines()]
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        index += 1
        tags: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("_"):
            tag = lines[index].strip()
            if tag.startswith(prefix):
                tags.append(tag)
            elif tags:
                tags = []
                break
            index += 1
        if not tags:
            continue
        while index < len(lines):
            line = lines[index].strip()
            if not line or line == "#":
                break
            if line == "loop_" or line.startswith("_") or line.startswith("data_"):
                break
            try:
                values = shlex.split(line)
            except ValueError:
                values = line.split()
            if len(values) >= len(tags):
                rows.append(
                    {
                        tag.removeprefix(prefix): value
                        for tag, value in zip(tags, values, strict=False)
                    }
                )
            index += 1
    return rows


def normalize(value: Any) -> str | None:
    text = str(value or "")
    if text in {"", ".", "?"}:
        return None
    return text


def chain_label_entity_map(cif_text: str) -> dict[str, str]:
    return {
        str(row.get("id") or ""): str(row.get("entity_id") or "")
        for row in parse_loop_rows(cif_text, "_struct_asym.")
        if normalize(row.get("id")) and normalize(row.get("entity_id"))
    }


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def preferred_seq_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def atom_entity(atom: dict[str, Any], label_chain_to_entity: dict[str, str]) -> str | None:
    entity_id = normalize(atom.get("label_entity_id"))
    if entity_id:
        return entity_id
    label_chain = str(atom.get("label_asym_id") or "")
    return label_chain_to_entity.get(label_chain)


def polymer_entities_by_auth_chain(atoms: list[dict[str, Any]]) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        auth_chain = normalize(atom.get("auth_asym_id"))
        entity_id = normalize(atom.get("label_entity_id"))
        if auth_chain and entity_id:
            mapping[auth_chain].add(entity_id)
    return mapping


def first_polymer_entity_by_auth_chain(atoms: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        entity_id = normalize(atom.get("label_entity_id"))
        if not entity_id:
            continue
        for chain_key in ("auth_asym_id", "label_asym_id"):
            chain_id = normalize(atom.get(chain_key))
            if chain_id and chain_id not in mapping:
                mapping[chain_id] = entity_id
    return mapping


def terminal_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferred = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom.get("type_symbol") == "P"
        and atom_code(atom) in set(SCAN_LIGANDS)
        and atom_name(atom) == "PG"
    ]
    fallback = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom.get("type_symbol") == "P"
        and atom_code(atom) in set(SCAN_LIGANDS)
        and atom_name(atom) in TERMINAL_P_NAMES
    ]
    return preferred or fallback


def is_probable_epk(pdb_id: str, context_text: str) -> bool:
    lower = context_text.lower()
    return (
        pdb_id.upper() in KNOWN_EPK_POSITIVE_IDS
        or base.looks_probable_epk(context_text)
        or any(token in lower for token in EXTRA_EPK_CONTEXT_TOKENS)
    )


def topology_blocked(hits: list[dict[str, Any]]) -> tuple[bool, bool, bool]:
    pairs = [
        (
            str(hit.get("candidate_chain_name") or ""),
            str(hit.get("gamma_associated_polymer_chain_name") or ""),
        )
        for hit in hits
        if hit.get("candidate_chain_name") and hit.get("gamma_associated_polymer_chain_name")
    ]
    same_chain = any(candidate == gamma for candidate, gamma in pairs)
    reciprocal = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for left_index, (left_candidate, left_gamma) in enumerate(pairs)
        for right_candidate, right_gamma in pairs[left_index + 1 :]
    )
    return same_chain or reciprocal, same_chain, reciprocal


def compact_local_hit(
    terminal: dict[str, Any],
    acceptor: dict[str, Any],
    *,
    distance: float,
    nearest_mg: float | None,
    acceptor_entity_id: str | None,
    gamma_entity_id: str | None,
    auth_chain_entity_count: int,
) -> dict[str, Any]:
    residue = atom_code(acceptor)
    seq_id = ns.optional_int(preferred_seq_id(acceptor))
    substrate_mode = residue == "TYR" or (
        residue in ACCEPTOR_CODES
        and seq_id is not None
        and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    )
    candidate_chain = preferred_chain(acceptor)
    gamma_chain = preferred_chain(terminal)
    return {
        "ligand": atom_code(terminal),
        "terminal_p_atom": atom_name(terminal),
        "gamma_chain_name": gamma_chain,
        "gamma_associated_polymer_chain_name": gamma_chain,
        "gamma_auth_chain": terminal.get("auth_asym_id"),
        "gamma_label_chain": terminal.get("label_asym_id"),
        "gamma_auth_seq_id": terminal.get("auth_seq_id"),
        "gamma_label_entity_id": terminal.get("label_entity_id"),
        "gamma_associated_polymer_entity_id": gamma_entity_id,
        "candidate_chain_name": candidate_chain,
        "candidate_auth_chain": acceptor.get("auth_asym_id"),
        "candidate_label_chain": acceptor.get("label_asym_id"),
        "candidate_auth_seq_id": preferred_seq_id(acceptor),
        "candidate_label_entity_id": acceptor.get("label_entity_id"),
        "acceptor_entity_id": acceptor_entity_id,
        "candidate_residue_code": residue,
        "candidate_atom_name": atom_name(acceptor),
        "distance_angstrom": round(distance, 3),
        "nearest_mg_distance_angstrom": round(nearest_mg, 3) if nearest_mg is not None else None,
        "substrate_mode_rule_hit": substrate_mode,
        "candidate_same_chain_as_gamma": bool(candidate_chain and candidate_chain == gamma_chain),
        "distinct_acceptor_gamma_entities": bool(
            acceptor_entity_id and gamma_entity_id and acceptor_entity_id != gamma_entity_id
        ),
        "same_author_chain_distinct_entity_reuse": bool(
            candidate_chain
            and candidate_chain == gamma_chain
            and acceptor_entity_id
            and gamma_entity_id
            and acceptor_entity_id != gamma_entity_id
        ),
        "author_chain_entity_count": auth_chain_entity_count,
    }


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


def summarize_entry(
    pdb_id: str,
    query_names: list[str],
    cif_text: str,
    entry_payload: dict[str, Any],
) -> dict[str, Any]:
    atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
    title = entry_payload.get("struct", {}).get("title", "")
    keywords = entry_payload.get("struct_keywords", {}) or {}
    if not atoms:
        return {
            "pdb_id": pdb_id,
            "query_names": query_names,
            "title": title,
            "keywords": keywords,
            "reviewed": False,
            **parse_meta,
        }

    label_chain_to_entity = chain_label_entity_map(cif_text)
    auth_chain_entities = polymer_entities_by_auth_chain(atoms)
    first_entity_by_auth_chain = first_polymer_entity_by_auth_chain(atoms)
    reused_auth_chains = {
        chain: sorted(entities)
        for chain, entities in sorted(auth_chain_entities.items())
        if len(entities) > 1
    }
    terminals = terminal_atoms(atoms)
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and (atom_code(atom) == "MG" or atom.get("type_symbol") == "MG")
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "ATOM"
        and ACCEPTOR_CODES.get(atom_code(atom)) == atom_name(atom)
    ]

    local_hits: list[dict[str, Any]] = []
    for terminal in terminals:
        mg_distances = [ns.distance(terminal, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        gamma_chain = preferred_chain(terminal)
        gamma_entity_id = first_entity_by_auth_chain.get(gamma_chain) or atom_entity(
            terminal, label_chain_to_entity
        )
        auth_chain_entity_count = len(auth_chain_entities.get(gamma_chain, set()))
        for acceptor in acceptor_atoms:
            distance = ns.distance(terminal, acceptor)
            if distance > DISTANCE_CUTOFF_ANGSTROM:
                continue
            acceptor_entity_id = atom_entity(acceptor, label_chain_to_entity)
            hit = compact_local_hit(
                terminal,
                acceptor,
                distance=distance,
                nearest_mg=nearest_mg,
                acceptor_entity_id=acceptor_entity_id,
                gamma_entity_id=gamma_entity_id,
                auth_chain_entity_count=auth_chain_entity_count,
            )
            local_hits.append(hit)

    substrate_hits = [hit for hit in local_hits if hit["substrate_mode_rule_hit"]]
    reuse_hits = [
        hit for hit in substrate_hits if hit["same_author_chain_distinct_entity_reuse"]
    ]
    distinct_entity_hits = [
        hit for hit in substrate_hits if hit["distinct_acceptor_gamma_entities"]
    ]
    topology_is_blocked, same_chain, reciprocal = topology_blocked(distinct_entity_hits)
    topology_clear_distinct_entity_hits = [] if topology_is_blocked else distinct_entity_hits
    probable_epk = is_probable_epk(pdb_id, context_text(entry_payload))
    non_epk_topology_clear = [
        hit for hit in topology_clear_distinct_entity_hits if not probable_epk
    ]
    local_hits.sort(
        key=lambda hit: (
            0 if hit["same_author_chain_distinct_entity_reuse"] else 1,
            0 if hit["distinct_acceptor_gamma_entities"] else 1,
            0 if hit["substrate_mode_rule_hit"] else 1,
            hit["distance_angstrom"],
        )
    )
    return {
        "pdb_id": pdb_id,
        "query_names": query_names,
        "title": title,
        "keywords": {
            "pdbx_keywords": keywords.get("pdbx_keywords"),
            "text": keywords.get("text"),
        },
        "reviewed": True,
        **parse_meta,
        "known_epk_positive_id": pdb_id.upper() in KNOWN_EPK_POSITIVE_IDS,
        "probable_epk_from_context": probable_epk,
        "reused_auth_chain_count": len(reused_auth_chains),
        "reused_auth_chains": dict(list(reused_auth_chains.items())[:12]),
        "terminal_p_atom_count": len(terminals),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "local_mg_acceptor_hit_count": len(local_hits),
        "substrate_mode_rule_hit_count": len(substrate_hits),
        "distinct_entity_substrate_mode_hit_count": len(distinct_entity_hits),
        "same_author_chain_distinct_entity_reuse_hit_count": len(reuse_hits),
        "same_chain_topology_detected": same_chain,
        "reciprocal_cross_chain_topology_detected": reciprocal,
        "topology_ambiguity_counteraxis_hit": topology_is_blocked,
        "topology_clear_distinct_entity_substrate_mode_hit_count": len(
            topology_clear_distinct_entity_hits
        ),
        "non_epk_topology_clear_distinct_entity_hit_count": len(non_epk_topology_clear),
        "same_author_chain_entity_reuse_pressure": bool(reuse_hits),
        "current_rule_counterexample_candidate_review_only": bool(
            non_epk_topology_clear
        ),
        "best_hits": local_hits[:10],
    }


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, Any], dict[str, list[str]]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, Any] = {}
    query_results: dict[str, list[str]] = {}

    for query in COMPONENT_QUERY_SURFACE:
        name = str(query["name"])
        try:
            ids = ns.component_query(
                str(query["ligand"]),
                str(query["metal"]),
                int(query["start"]),
                int(query["rows"]),
            )
            query_results[name] = ids
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[name] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries[pdb_id].append(name)
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.15)

    for pdb_id in reversed(SEED_IDS):
        id_to_queries[pdb_id].append("seed_attack_or_prior_reuse_pressure_id")
        if pdb_id in ordered_ids:
            ordered_ids.remove(pdb_id)
        ordered_ids.insert(0, pdb_id)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_results


def materializer_substrate_mode_rows(
    materializer: dict[str, Any],
    probable_epk_by_pdb: dict[str, bool],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    pressure_rows: list[dict[str, Any]] = []
    topology_clear_counterexamples: list[dict[str, Any]] = []
    non_epk_pressure_rows: list[dict[str, Any]] = []
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        hits = [
            hit
            for hit in row.get("heteromeric_candidate_hits", []) or []
            if isinstance(hit, dict)
        ]
        substrate_hits = []
        reuse_hits = []
        for hit in hits:
            residue = str(hit.get("candidate_residue_code") or "").upper()
            seq_id = ns.optional_int(hit.get("candidate_auth_seq_id"))
            substrate_mode = residue == "TYR" or (
                residue in ACCEPTOR_CODES
                and seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
            )
            if not substrate_mode:
                continue
            substrate_hits.append(hit)
            if str(hit.get("candidate_chain_name") or "") == str(
                hit.get("gamma_associated_polymer_chain_name") or ""
            ):
                reuse_hits.append(hit)
        if reuse_hits:
            pressure_rows.append({**row, "same_author_chain_reuse_hits": reuse_hits})
        if reuse_hits and not probable_epk_by_pdb.get(pdb_id):
            non_epk_pressure_rows.append({**row, "same_author_chain_reuse_hits": reuse_hits})
        blocked, same_chain, reciprocal = topology_blocked(substrate_hits)
        if substrate_hits and not blocked and not probable_epk_by_pdb.get(pdb_id):
            topology_clear_counterexamples.append(
                {
                    **row,
                    "substrate_mode_materializer_hits": substrate_hits,
                    "same_chain_topology_detected": same_chain,
                    "reciprocal_cross_chain_topology_detected": reciprocal,
                }
            )
    return pressure_rows, non_epk_pressure_rows, topology_clear_counterexamples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    ordered_ids, id_to_queries, query_errors, query_results = collect_ids()
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    cif_text_by_pdb: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            row = summarize_entry(pdb_id, id_to_queries.get(pdb_id, []), cif_text, entry_payload)
            row["surface_order"] = index
            rows.append(row)
            if row.get("same_author_chain_entity_reuse_pressure"):
                cif_text_by_pdb[pdb_id] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.08)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    reuse_rows = [
        row for row in reviewed_rows if row.get("same_author_chain_entity_reuse_pressure")
    ]
    pressure_ids = sorted({row["pdb_id"] for row in reuse_rows})
    materializer = ns.materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=pressure_ids,
        cif_text_by_pdb=cif_text_by_pdb,
    )
    probable_epk_by_pdb = {
        str(row.get("pdb_id") or "").upper(): bool(row.get("probable_epk_from_context"))
        for row in reviewed_rows
    }
    (
        materializer_reuse_rows,
        materializer_non_epk_reuse_rows,
        materializer_counterexamples,
    ) = materializer_substrate_mode_rows(materializer, probable_epk_by_pdb)
    materializer_status_counts = Counter(
        str(row.get("candidate_status") or "") for row in materializer.get("rows", []) or []
    )
    local_counterexamples = [
        row
        for row in reviewed_rows
        if row.get("current_rule_counterexample_candidate_review_only")
    ]
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "same_author_chain_entity_reuse_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0"
            ),
            "search_surface": {
                "component_query_surface": COMPONENT_QUERY_SURFACE,
                "seed_ids": SEED_IDS,
                "scan_ligands": SCAN_LIGANDS,
                "current_atp_like_ligands": sorted(CURRENT_ATP_LIKE_LIGANDS),
                "actual_materializer_gamma_capable_codes": sorted(GAMMA_CAPABLE_CODES),
                "candidate_threshold_angstrom": DISTANCE_CUTOFF_ANGSTROM,
                "mg_distance_cutoff_angstrom": MG_DISTANCE_CUTOFF_ANGSTROM,
                "max_n_terminal_acceptor_auth_seq_id": MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
                "max_unique_ids": MAX_UNIQUE_IDS,
                "raw_coordinate_files_written": False,
                "known_epk_positive_ids_excluded_from_counterexamples": sorted(
                    KNOWN_EPK_POSITIVE_IDS
                ),
                "extra_epk_context_tokens": EXTRA_EPK_CONTEXT_TOKENS,
            },
            "query_result_counts": {name: len(ids) for name, ids in query_results.items()},
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(reviewed_rows),
            "fetch_error_count": len(fetch_errors),
            "same_author_chain_entity_reuse_pressure_entry_count": len(reuse_rows),
            "same_author_chain_entity_reuse_pressure_pdb_ids": pressure_ids,
            "local_current_rule_counterexample_count": len(local_counterexamples),
            "local_current_rule_counterexample_pdb_ids": [
                row["pdb_id"] for row in local_counterexamples
            ],
            "actual_materializer_input_count": len(pressure_ids),
            "actual_materializer_candidate_status_counts": dict(materializer_status_counts),
            "actual_materializer_same_author_chain_reuse_entry_count": len(
                materializer_reuse_rows
            ),
            "actual_materializer_same_author_chain_reuse_pdb_ids": [
                row["pdb_id"] for row in materializer_reuse_rows
            ],
            "actual_materializer_non_epk_same_author_chain_reuse_entry_count": len(
                materializer_non_epk_reuse_rows
            ),
            "actual_materializer_non_epk_same_author_chain_reuse_pdb_ids": [
                row["pdb_id"] for row in materializer_non_epk_reuse_rows
            ],
            "actual_materializer_topology_clear_non_epk_counterexample_count": len(
                materializer_counterexamples
            ),
            "actual_materializer_topology_clear_non_epk_counterexample_pdb_ids": [
                row["pdb_id"] for row in materializer_counterexamples
            ],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "fetch_errors": fetch_errors,
        "same_author_chain_entity_reuse_pressure_rows": reuse_rows,
        "local_current_rule_counterexamples_review_only": local_counterexamples,
        "actual_materializer_probe": materializer,
        "actual_materializer_same_author_chain_reuse_rows": materializer_reuse_rows,
        "actual_materializer_non_epk_same_author_chain_reuse_rows": (
            materializer_non_epk_reuse_rows
        ),
        "actual_materializer_topology_clear_non_epk_counterexamples_review_only": (
            materializer_counterexamples
        ),
        "rows": rows,
        "warnings": [
            "Review-only false-positive stress evidence; no production scoring, threshold calibration, label import, or fingerprint edit.",
            "DTP is scanned only because the actual review-only materializer currently lists it as gamma-capable; this is not a ligand-set expansion recommendation.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
