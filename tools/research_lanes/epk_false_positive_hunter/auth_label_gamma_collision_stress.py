#!/usr/bin/env python3
"""Auth/label gamma-chain collision stress for ePK false-positive hunting.

This lane helper attacks the materializer path where a ligand auth_asym_id can
collide with a polymer label_asym_id. It compares the current review-only
gamma-associated polymer mapping with an auth-only gamma mapping variant, then
records compact pressure/counterexample evidence. Fetched coordinates remain
in memory and are not written.
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
CURRENT_ATP_LIKE_LIGANDS = {"A3P", "ACP", "AGS", "ANP", "ATP"}
SCAN_LIGANDS = sorted(CURRENT_ATP_LIKE_LIGANDS | GAMMA_CAPABLE_CODES)
ACCEPTOR_CODES = {"SER": "OG", "THR": "OG1", "TYR": "OH"}
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MAX_UNIQUE_IDS = 960

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
    {"name": "atp_mg_start_0", "ligand": "ATP", "metal": "MG", "start": 0, "rows": 60},
    {"name": "atp_mg_start_120", "ligand": "ATP", "metal": "MG", "start": 120, "rows": 60},
    {"name": "atp_mg_start_240", "ligand": "ATP", "metal": "MG", "start": 240, "rows": 60},
    {"name": "atp_mg_start_360", "ligand": "ATP", "metal": "MG", "start": 360, "rows": 60},
    {"name": "atp_mg_start_480", "ligand": "ATP", "metal": "MG", "start": 480, "rows": 60},
    {"name": "atp_mg_start_600", "ligand": "ATP", "metal": "MG", "start": 600, "rows": 60},
    {"name": "atp_mg_start_720", "ligand": "ATP", "metal": "MG", "start": 720, "rows": 60},
    {"name": "atp_mg_start_840", "ligand": "ATP", "metal": "MG", "start": 840, "rows": 60},
    {"name": "atp_mg_start_960", "ligand": "ATP", "metal": "MG", "start": 960, "rows": 60},
    {"name": "atp_mg_start_1080", "ligand": "ATP", "metal": "MG", "start": 1080, "rows": 60},
    {"name": "atp_mg_start_1200", "ligand": "ATP", "metal": "MG", "start": 1200, "rows": 60},
    {"name": "atp_mg_start_1320", "ligand": "ATP", "metal": "MG", "start": 1320, "rows": 60},
    {"name": "anp_mg_start_0", "ligand": "ANP", "metal": "MG", "start": 0, "rows": 50},
    {"name": "anp_mg_start_160", "ligand": "ANP", "metal": "MG", "start": 160, "rows": 50},
    {"name": "anp_mg_start_320", "ligand": "ANP", "metal": "MG", "start": 320, "rows": 50},
    {"name": "anp_mg_start_480", "ligand": "ANP", "metal": "MG", "start": 480, "rows": 50},
    {"name": "acp_mg_start_0", "ligand": "ACP", "metal": "MG", "start": 0, "rows": 50},
    {"name": "acp_mg_start_160", "ligand": "ACP", "metal": "MG", "start": 160, "rows": 50},
    {"name": "acp_mg_start_320", "ligand": "ACP", "metal": "MG", "start": 320, "rows": 50},
    {"name": "dtp_mg_start_0", "ligand": "DTP", "metal": "MG", "start": 0, "rows": 45},
    {"name": "dtp_mg_start_120", "ligand": "DTP", "metal": "MG", "start": 120, "rows": 45},
    {"name": "ags_mg_start_0", "ligand": "AGS", "metal": "MG", "start": 0, "rows": 45},
    {"name": "ags_mg_start_160", "ligand": "AGS", "metal": "MG", "start": 160, "rows": 45},
    {"name": "a3p_mg_start_0", "ligand": "A3P", "metal": "MG", "start": 0, "rows": 45},
]

SEED_IDS = [
    "7CAG",
    "8BMS",
    "9L3M",
    "9L3U",
    "7ZE5",
    "1N56",
    "2DRA",
    "2Q66",
    "2ZH6",
    "4RWT",
    "7Z3N",
    "7Z3O",
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
        id_to_queries[pdb_id].append("seed_attack_or_prior_namespace_pressure_id")
        if pdb_id in ordered_ids:
            ordered_ids.remove(pdb_id)
        ordered_ids.insert(0, pdb_id)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_results


def collect_full_text_ids(
    phrases: list[str],
    rows: int,
) -> tuple[list[str], dict[str, list[str]], dict[str, Any], dict[str, list[str]]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, Any] = {}
    query_results: dict[str, list[str]] = {}

    for index, phrase in enumerate(phrases, start=1):
        name = f"full_text_{index}"
        try:
            ids = base.rcsb_full_text_query(phrase, rows)
            query_results[name] = ids
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[name] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries[pdb_id].append(f"{name}:{phrase}")
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.15)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_results


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def preferred_seq_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def polymer_entity_maps(atoms: list[dict[str, Any]]) -> dict[str, dict[str, set[str]]]:
    by_auth: dict[str, set[str]] = defaultdict(set)
    by_label: dict[str, set[str]] = defaultdict(set)
    by_mixed_first: dict[str, set[str]] = defaultdict(set)
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        entity_id = normalize(atom.get("label_entity_id"))
        if not entity_id:
            continue
        auth_chain = normalize(atom.get("auth_asym_id"))
        label_chain = normalize(atom.get("label_asym_id"))
        if auth_chain:
            by_auth[auth_chain].add(entity_id)
            by_mixed_first[auth_chain].add(entity_id)
        if label_chain:
            by_label[label_chain].add(entity_id)
            by_mixed_first[label_chain].add(entity_id)
    return {"auth": by_auth, "label": by_label, "mixed": by_mixed_first}


def first_entity(mapping: dict[str, set[str]], chain: str) -> str | None:
    values = sorted(mapping.get(chain, set()))
    return values[0] if values else None


def atom_entity(atom: dict[str, Any]) -> str | None:
    return normalize(atom.get("label_entity_id"))


def terminal_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom.get("type_symbol") == "P"
        and atom_code(atom) in set(SCAN_LIGANDS)
        and atom_name(atom) == "PG"
    ]


def substrate_mode_for_acceptor(acceptor: dict[str, Any]) -> bool:
    residue = atom_code(acceptor)
    seq_id = ns.optional_int(preferred_seq_id(acceptor))
    return residue == "TYR" or (
        residue in ACCEPTOR_CODES
        and seq_id is not None
        and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    )


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


def is_probable_epk(pdb_id: str, text: str) -> bool:
    lower = text.lower()
    return (
        pdb_id.upper() in KNOWN_EPK_POSITIVE_IDS
        or base.looks_probable_epk(text)
        or any(token in lower for token in EXTRA_EPK_CONTEXT_TOKENS)
    )


def topology_blocked(hits: list[dict[str, Any]], gamma_key: str) -> tuple[bool, bool, bool]:
    pairs = [
        (str(hit.get("candidate_chain_name") or ""), str(hit.get(gamma_key) or ""))
        for hit in hits
        if hit.get("candidate_chain_name") and hit.get(gamma_key)
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


def compact_hit(
    *,
    terminal: dict[str, Any],
    acceptor: dict[str, Any],
    distance: float,
    nearest_mg: float,
    maps: dict[str, dict[str, set[str]]],
) -> dict[str, Any]:
    gamma_chain = preferred_chain(terminal)
    candidate_chain = preferred_chain(acceptor)
    acceptor_entity_id = atom_entity(acceptor)
    actual_gamma_entity_id = first_entity(maps["mixed"], gamma_chain)
    auth_only_gamma_entity_id = first_entity(maps["auth"], gamma_chain)
    label_collision_entities = sorted(maps["label"].get(gamma_chain, set()))
    residue = atom_code(acceptor)
    return {
        "ligand": atom_code(terminal),
        "terminal_p_atom": atom_name(terminal),
        "gamma_auth_chain": terminal.get("auth_asym_id"),
        "gamma_label_chain": terminal.get("label_asym_id"),
        "gamma_chain_name": gamma_chain,
        "candidate_chain_name": candidate_chain,
        "candidate_auth_chain": acceptor.get("auth_asym_id"),
        "candidate_label_chain": acceptor.get("label_asym_id"),
        "candidate_auth_seq_id": preferred_seq_id(acceptor),
        "candidate_label_seq_id": acceptor.get("label_seq_id"),
        "candidate_residue_code": residue,
        "candidate_atom_name": atom_name(acceptor),
        "acceptor_entity_id": acceptor_entity_id,
        "actual_gamma_associated_polymer_chain_name": gamma_chain,
        "actual_gamma_associated_polymer_entity_id": actual_gamma_entity_id,
        "auth_only_gamma_associated_polymer_chain_name": gamma_chain,
        "auth_only_gamma_associated_polymer_entity_id": auth_only_gamma_entity_id,
        "label_collision_polymer_entity_ids": label_collision_entities,
        "auth_label_gamma_collision": bool(
            gamma_chain
            and label_collision_entities
            and (
                auth_only_gamma_entity_id is None
                or auth_only_gamma_entity_id not in label_collision_entities
            )
        ),
        "acceptor_entity_differs_from_label_collision_entity": bool(
            acceptor_entity_id
            and label_collision_entities
            and acceptor_entity_id not in label_collision_entities
        ),
        "actual_distinct_acceptor_gamma_entities": bool(
            acceptor_entity_id
            and actual_gamma_entity_id
            and acceptor_entity_id != actual_gamma_entity_id
        ),
        "auth_only_distinct_acceptor_gamma_entities": bool(
            acceptor_entity_id
            and auth_only_gamma_entity_id
            and acceptor_entity_id != auth_only_gamma_entity_id
        ),
        "actual_vs_auth_only_gamma_entity_changed": actual_gamma_entity_id
        != auth_only_gamma_entity_id,
        "candidate_same_chain_as_gamma": bool(
            candidate_chain and candidate_chain == gamma_chain
        ),
        "substrate_mode_rule_hit": substrate_mode_for_acceptor(acceptor),
        "distance_angstrom": round(distance, 3),
        "nearest_mg_distance_angstrom": round(nearest_mg, 3),
    }


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

    maps = polymer_entity_maps(atoms)
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
    terminals = terminal_atoms(atoms)

    local_hits: list[dict[str, Any]] = []
    for terminal in terminals:
        mg_distances = [ns.distance(terminal, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        for acceptor in acceptor_atoms:
            distance = ns.distance(terminal, acceptor)
            if distance > DISTANCE_CUTOFF_ANGSTROM:
                continue
            hit = compact_hit(
                terminal=terminal,
                acceptor=acceptor,
                distance=distance,
                nearest_mg=nearest_mg,
                maps=maps,
            )
            if hit["substrate_mode_rule_hit"]:
                local_hits.append(hit)

    collision_hits = [
        hit
        for hit in local_hits
        if hit["auth_label_gamma_collision"]
        and hit["actual_distinct_acceptor_gamma_entities"]
        and hit["actual_vs_auth_only_gamma_entity_changed"]
    ]
    auth_only_hits = [
        hit
        for hit in local_hits
        if hit["auth_only_distinct_acceptor_gamma_entities"]
    ]
    actual_blocked, actual_same_chain, actual_reciprocal = topology_blocked(
        [hit for hit in local_hits if hit["actual_distinct_acceptor_gamma_entities"]],
        "actual_gamma_associated_polymer_chain_name",
    )
    auth_only_blocked, auth_only_same_chain, auth_only_reciprocal = topology_blocked(
        auth_only_hits,
        "auth_only_gamma_associated_polymer_chain_name",
    )
    topology_clear_collision_hits = [] if actual_blocked else collision_hits
    probable_epk = is_probable_epk(pdb_id, context_text(entry_payload))
    non_epk_topology_clear = [
        hit for hit in topology_clear_collision_hits if not probable_epk
    ]
    local_hits.sort(
        key=lambda hit: (
            0 if hit["auth_label_gamma_collision"] else 1,
            0 if hit["actual_vs_auth_only_gamma_entity_changed"] else 1,
            0 if hit["actual_distinct_acceptor_gamma_entities"] else 1,
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
        "terminal_p_atom_count": len(terminals),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "substrate_mode_local_hit_count": len(local_hits),
        "auth_label_gamma_collision_hit_count": len(collision_hits),
        "auth_label_gamma_collision_pressure": bool(collision_hits),
        "actual_distinct_entity_hit_count": sum(
            1 for hit in local_hits if hit["actual_distinct_acceptor_gamma_entities"]
        ),
        "auth_only_distinct_entity_hit_count": len(auth_only_hits),
        "actual_same_chain_topology_detected": actual_same_chain,
        "actual_reciprocal_cross_chain_topology_detected": actual_reciprocal,
        "actual_topology_ambiguity_counteraxis_hit": actual_blocked,
        "auth_only_same_chain_topology_detected": auth_only_same_chain,
        "auth_only_reciprocal_cross_chain_topology_detected": auth_only_reciprocal,
        "auth_only_topology_ambiguity_counteraxis_hit": auth_only_blocked,
        "topology_clear_auth_label_collision_hit_count": len(topology_clear_collision_hits),
        "current_rule_counterexample_candidate_review_only": bool(non_epk_topology_clear),
        "best_hits": local_hits[:10],
    }


def materializer_substrate_mode_counterexamples(
    materializer: dict[str, Any],
    probable_epk_by_pdb: dict[str, bool],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    non_epk_pressure_rows: list[dict[str, Any]] = []
    topology_clear_counterexamples: list[dict[str, Any]] = []
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        hits = [
            hit
            for hit in row.get("heteromeric_candidate_hits", []) or []
            if isinstance(hit, dict)
        ]
        substrate_hits = []
        for hit in hits:
            residue = str(hit.get("candidate_residue_code") or "").upper()
            seq_id = ns.optional_int(hit.get("candidate_auth_seq_id"))
            substrate_mode = residue == "TYR" or (
                residue in ACCEPTOR_CODES
                and seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
            )
            if substrate_mode:
                substrate_hits.append(hit)
        if substrate_hits and not probable_epk_by_pdb.get(pdb_id):
            non_epk_pressure_rows.append(
                {**row, "substrate_mode_materializer_hits": substrate_hits}
            )
        blocked, same_chain, reciprocal = reuse.topology_blocked(substrate_hits)
        if substrate_hits and not blocked and not probable_epk_by_pdb.get(pdb_id):
            topology_clear_counterexamples.append(
                {
                    **row,
                    "substrate_mode_materializer_hits": substrate_hits,
                    "same_chain_topology_detected": same_chain,
                    "reciprocal_cross_chain_topology_detected": reciprocal,
                }
            )
    return non_epk_pressure_rows, topology_clear_counterexamples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--retry-fetch-errors-from",
        help="Retry only the fetch_error PDB IDs recorded in a prior artifact.",
    )
    parser.add_argument(
        "--full-text-query",
        action="append",
        default=[],
        help="Run one bounded RCSB full-text query; may be repeated.",
    )
    parser.add_argument("--full-text-rows", type=int, default=80)
    args = parser.parse_args()

    retry_source = None
    surface_mode = "component_query"
    if args.retry_fetch_errors_from:
        surface_mode = "retry_fetch_errors"
        retry_source = Path(args.retry_fetch_errors_from)
        previous = json.loads(retry_source.read_text(encoding="utf-8"))
        ordered_ids = sorted(str(pdb_id).upper() for pdb_id in previous.get("fetch_errors", {}))
        id_to_queries = defaultdict(
            list,
            {
                pdb_id: [
                    f"retry_fetch_error_from_{retry_source.name}",
                ]
                for pdb_id in ordered_ids
            },
        )
        query_errors = {}
        query_results = {"retry_fetch_errors": ordered_ids}
    elif args.full_text_query:
        surface_mode = "full_text_query"
        ordered_ids, id_to_queries, query_errors, query_results = collect_full_text_ids(
            args.full_text_query,
            args.full_text_rows,
        )
    else:
        ordered_ids, id_to_queries, query_errors, query_results = collect_ids()
    ordered_ids = ordered_ids[:MAX_UNIQUE_IDS]
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    cif_text_by_pdb: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            row = summarize_entry(
                pdb_id,
                id_to_queries.get(pdb_id, []),
                cif_text,
                entry_payload,
            )
            row["surface_order"] = index
            rows.append(row)
            if row.get("auth_label_gamma_collision_pressure"):
                cif_text_by_pdb[pdb_id] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.08)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    collision_rows = [
        row for row in reviewed_rows if row.get("auth_label_gamma_collision_pressure")
    ]
    pressure_ids = sorted({str(row["pdb_id"]).upper() for row in collision_rows})
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
    materializer_non_epk_pressure_rows, materializer_counterexamples = (
        materializer_substrate_mode_counterexamples(materializer, probable_epk_by_pdb)
    )
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
            "method": "auth_label_gamma_collision_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0"
            ),
            "search_surface": {
                "surface_mode": surface_mode,
                "component_query_surface": (
                    COMPONENT_QUERY_SURFACE if surface_mode == "component_query" else []
                ),
                "seed_ids": SEED_IDS if surface_mode == "component_query" else [],
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
                "variant_comparison": (
                    "current materializer-like mixed auth/label chain-to-entity "
                    "gamma mapping vs auth-only polymer-chain gamma mapping"
                ),
                "retry_fetch_errors_from": str(retry_source) if retry_source else None,
                "full_text_queries": args.full_text_query,
                "full_text_rows": args.full_text_rows if args.full_text_query else None,
            },
            "query_result_counts": {
                name: len(ids) for name, ids in query_results.items()
            },
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(reviewed_rows),
            "fetch_error_count": len(fetch_errors),
            "auth_label_gamma_collision_pressure_entry_count": len(collision_rows),
            "auth_label_gamma_collision_pressure_pdb_ids": pressure_ids,
            "local_current_rule_counterexample_count": len(local_counterexamples),
            "local_current_rule_counterexample_pdb_ids": [
                row["pdb_id"] for row in local_counterexamples
            ],
            "actual_materializer_input_count": len(pressure_ids),
            "actual_materializer_candidate_status_counts": dict(
                materializer_status_counts
            ),
            "actual_materializer_non_epk_pressure_count": len(
                materializer_non_epk_pressure_rows
            ),
            "actual_materializer_non_epk_pressure_pdb_ids": [
                row["pdb_id"] for row in materializer_non_epk_pressure_rows
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
        "auth_label_gamma_collision_pressure_rows": collision_rows,
        "local_current_rule_counterexamples_review_only": local_counterexamples,
        "actual_materializer_probe": materializer,
        "actual_materializer_non_epk_pressure_rows": materializer_non_epk_pressure_rows,
        "actual_materializer_topology_clear_non_epk_counterexamples_review_only": (
            materializer_counterexamples
        ),
        "rows": rows,
        "warnings": [
            "Review-only false-positive stress evidence; no production scoring, threshold calibration, label import, or fingerprint edit.",
            "DTP is scanned only because the actual review-only materializer currently lists it as gamma-capable; this is not a ligand-set expansion recommendation.",
            "The auth-only variant is an adversarial comparison, not a production recommendation.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
