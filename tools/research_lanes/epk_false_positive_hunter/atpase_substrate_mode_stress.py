#!/usr/bin/env python3
"""Bounded source-free ePK false-positive stress search.

The script queries RCSB for ATP/Mg ATPase/transporter/translocase-like
entries, fetches candidate mmCIF files in memory, and records only compact
distance/topology evidence. It intentionally does not write raw coordinates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import shlex
import sys
import time
from pathlib import Path
from typing import Any

import requests


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"
RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
TERMINAL_LIGANDS = {"ATP", "ANP", "AGS", "ACP", "A3P", "AMPPNP", "ATP-GAMMA-S"}
TERMINAL_PHOSPHATE_NAMES = {"PG", "P3G", "P03", "P3", "P03G", "PG1", "PG2", "PN"}
ACCEPTOR_ATOMS = {
    ("SER", "OG"),
    ("THR", "OG1"),
    ("TYR", "OH"),
}
MAGNESIUM_CODES = {"MG"}
QUERY_ROWS = 35
MAX_UNIQUE_IDS = 110
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25


QUERY_SURFACE_PROFILES = {
    "atpase_transport": [
        {
            "name": "atpase_atp_magnesium",
            "phrase": "ATPase ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "abc_transporter_atp_magnesium",
            "phrase": "ABC transporter ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "translocase_atp_magnesium",
            "phrase": "translocase ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "motor_atpase_atp_magnesium",
            "phrase": "motor ATPase ATP magnesium",
            "rows": QUERY_ROWS,
        },
    ],
    "walker_a_confirmation": [
        {
            "name": "walker_a_atp_magnesium",
            "phrase": "Walker A ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "p_loop_ntpase_atp_magnesium",
            "phrase": "P-loop NTPase ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "arsa_mgatp_arsenite",
            "phrase": "ArsA MgATP arsenite",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atpase_like_mgatp_walker_a",
            "phrase": "ATPase-like protein MgATP Walker A",
            "rows": QUERY_ROWS,
        },
    ],
    "non_epk_atp_mg_enzymes": [
        {
            "name": "atp_grasp_atp_magnesium",
            "phrase": "ATP-grasp ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_dependent_ligase_magnesium",
            "phrase": "ATP-dependent ligase magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "pfkb_atp_magnesium",
            "phrase": "PfkB ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "ribokinase_atp_magnesium",
            "phrase": "ribokinase ATP magnesium",
            "rows": QUERY_ROWS,
        },
    ],
}

SEED_ATTACK_IDS = ["7CAG", "8BMS", "9L3M", "9L3U", "7ZE5"]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rcsb_full_text_query(phrase: str, rows: int) -> list[str]:
    query = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {
                "value": phrase,
            },
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {
                "start": 0,
                "rows": rows,
            },
            "results_content_type": ["experimental"],
            "sort": [
                {
                    "sort_by": "score",
                    "direction": "desc",
                }
            ],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=query, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return [row["identifier"].upper() for row in payload.get("result_set", [])]


def fetch_text(url: str) -> str:
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    return response.text


def fetch_json(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_loop(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int]:
    tags: list[str] = []
    rows: list[list[str]] = []
    index = start + 1
    while index < len(lines) and lines[index].startswith("_"):
        tags.append(lines[index].strip())
        index += 1
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line == "#" or line == "loop_" or line.startswith("_"):
            break
        try:
            tokens = shlex.split(line)
        except ValueError:
            tokens = line.split()
        if len(tokens) >= len(tags):
            rows.append(tokens[: len(tags)])
        index += 1
    return tags, rows, index


def parse_atom_site(cif_text: str) -> list[dict[str, Any]]:
    lines = [line.rstrip("\n") for line in cif_text.splitlines()]
    atoms: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        tags, rows, next_index = parse_loop(lines, index)
        if not tags or not tags[0].startswith("_atom_site."):
            index = max(next_index, index + 1)
            continue
        tag_index = {tag: pos for pos, tag in enumerate(tags)}
        required = [
            "_atom_site.group_PDB",
            "_atom_site.type_symbol",
            "_atom_site.label_atom_id",
            "_atom_site.label_comp_id",
            "_atom_site.label_asym_id",
            "_atom_site.Cartn_x",
            "_atom_site.Cartn_y",
            "_atom_site.Cartn_z",
        ]
        if any(tag not in tag_index for tag in required):
            return atoms
        for row in rows:
            def value(tag: str, default: str = "") -> str:
                pos = tag_index.get(tag)
                if pos is None or pos >= len(row):
                    return default
                return row[pos]

            try:
                x = float(value("_atom_site.Cartn_x"))
                y = float(value("_atom_site.Cartn_y"))
                z = float(value("_atom_site.Cartn_z"))
            except ValueError:
                continue
            model = value("_atom_site.pdbx_PDB_model_num", "1")
            alt_id = value("_atom_site.label_alt_id", ".")
            if model not in {"1", ".", "?"}:
                continue
            if alt_id not in {".", "?", "A"}:
                continue
            atom = {
                "group": value("_atom_site.group_PDB"),
                "type_symbol": value("_atom_site.type_symbol").upper(),
                "label_atom_id": value("_atom_site.label_atom_id"),
                "auth_atom_id": value("_atom_site.auth_atom_id", value("_atom_site.label_atom_id")),
                "label_comp_id": value("_atom_site.label_comp_id").upper(),
                "auth_comp_id": value("_atom_site.auth_comp_id", value("_atom_site.label_comp_id")).upper(),
                "label_asym_id": value("_atom_site.label_asym_id"),
                "auth_asym_id": value("_atom_site.auth_asym_id", value("_atom_site.label_asym_id")),
                "label_seq_id": value("_atom_site.label_seq_id", "?"),
                "auth_seq_id": value("_atom_site.auth_seq_id", "?"),
                "x": x,
                "y": y,
                "z": z,
            }
            atoms.append(atom)
        return atoms
    return atoms


def norm_atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def atom_comp(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper().replace('"', "")


def distance(a: dict[str, Any], b: dict[str, Any]) -> float:
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2 + (a["z"] - b["z"]) ** 2)


def parse_intish(value: str) -> int | None:
    match = re.match(r"^-?\d+", str(value))
    if not match:
        return None
    return int(match.group(0))


def residue_key(atom: dict[str, Any]) -> tuple[str, str, str]:
    return (str(atom["auth_asym_id"]), str(atom["auth_seq_id"]), atom_comp(atom))


def ligand_key(atom: dict[str, Any]) -> tuple[str, str, str]:
    return (str(atom["auth_asym_id"]), str(atom["auth_seq_id"]), atom_comp(atom))


def looks_probable_epk(context_text: str) -> bool:
    lower = context_text.lower()
    epk_tokens = [
        "protein kinase",
        "serine/threonine kinase",
        "serine-threonine kinase",
        "tyrosine-protein kinase",
        "map kinase",
        "mapk",
        "cyclin-dependent kinase",
        "cdk",
        "erk",
        "mek",
    ]
    return any(token in lower for token in epk_tokens)


def context_family_hint(context_text: str) -> str:
    lower = context_text.lower()
    if "abc transporter" in lower:
        return "abc_transporter"
    if "transporter" in lower:
        return "transporter"
    if "translocase" in lower:
        return "translocase"
    if "atpase" in lower:
        return "atpase"
    if "motor" in lower or "myosin" in lower or "kinesin" in lower:
        return "motor_atpase"
    if "kinase" in lower:
        return "kinase_named_non_epk_or_uncertain"
    return "unclassified_from_context"


def entry_keywords(entry_payload: dict[str, Any]) -> dict[str, str | None]:
    keywords = entry_payload.get("struct_keywords", {}) or {}
    return {
        "pdbx_keywords": keywords.get("pdbx_keywords"),
        "text": keywords.get("text"),
    }


def fetch_polymer_summaries(pdb_id: str, entry_payload: dict[str, Any]) -> list[dict[str, Any]]:
    entity_ids = entry_payload.get("rcsb_entry_container_identifiers", {}).get("polymer_entity_ids") or []
    summaries: list[dict[str, Any]] = []
    for entity_id in entity_ids:
        response = requests.get(f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}", timeout=30)
        response.raise_for_status()
        payload = response.json()
        summaries.append(
            {
                "entity_id": entity_id,
                "description": payload.get("rcsb_polymer_entity", {}).get("pdbx_description"),
                "polymer_type": payload.get("entity_poly", {}).get("rcsb_entity_polymer_type"),
                "uniprot_ids": payload.get("rcsb_polymer_entity_container_identifiers", {}).get("uniprot_ids") or [],
            }
        )
    return summaries


def summarize_entry(pdb_id: str, query_names: list[str], cif_text: str, entry_payload: dict[str, Any]) -> dict[str, Any]:
    title = entry_payload.get("struct", {}).get("title", "")
    keywords = entry_keywords(entry_payload)
    polymer_summaries = fetch_polymer_summaries(pdb_id, entry_payload)
    context_text = " ".join(
        str(part or "")
        for part in [
            title,
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
            " ".join(str(summary.get("description") or "") for summary in polymer_summaries),
        ]
    )
    atoms = parse_atom_site(cif_text)
    if not atoms:
        return {
            "pdb_id": pdb_id,
            "query_names": query_names,
            "title": title,
            "keywords": keywords,
            "polymer_entities": polymer_summaries,
            "parse_status": "no_atom_site_rows",
            "reviewed": False,
        }

    terminal_p_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and atom_comp(atom) in TERMINAL_LIGANDS
        and norm_atom_name(atom) in TERMINAL_PHOSPHATE_NAMES
    ]
    all_triphosphate_p_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and atom_comp(atom) in TERMINAL_LIGANDS
    ]
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and (atom_comp(atom) in MAGNESIUM_CODES or atom["type_symbol"] == "MG")
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "ATOM"
        and (atom_comp(atom), norm_atom_name(atom)) in ACCEPTOR_ATOMS
    ]

    local_hits: list[dict[str, Any]] = []
    terminal_atoms_for_distance = terminal_p_atoms or all_triphosphate_p_atoms
    for p_atom in terminal_atoms_for_distance:
        mg_distances = [distance(p_atom, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        nearby_acceptors = []
        for acceptor in acceptor_atoms:
            d = distance(p_atom, acceptor)
            if d <= DISTANCE_CUTOFF_ANGSTROM:
                seq_id = parse_intish(acceptor["auth_seq_id"])
                is_n_terminal = seq_id is not None and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
                is_tyr = atom_comp(acceptor) == "TYR"
                substrate_mode_hit = is_tyr or is_n_terminal
                nearby_acceptors.append(
                    {
                        "chain": acceptor["auth_asym_id"],
                        "auth_seq_id": acceptor["auth_seq_id"],
                        "residue": atom_comp(acceptor),
                        "atom": norm_atom_name(acceptor),
                        "distance_angstrom": round(d, 3),
                        "n_terminal_acceptor": is_n_terminal,
                        "tyrosine_acceptor": is_tyr,
                        "substrate_mode_rule_hit": substrate_mode_hit,
                    }
                )
        nearby_acceptors.sort(key=lambda row: row["distance_angstrom"])
        if not nearby_acceptors:
            continue
        mode_hits = [row for row in nearby_acceptors if row["substrate_mode_rule_hit"]]
        same_chain_companion_count = 0
        if mode_hits:
            primary_chain = mode_hits[0]["chain"]
            same_chain_companion_count = sum(
                1
                for row in nearby_acceptors
                if row["chain"] == primary_chain and row != mode_hits[0]
            )
        local_hits.append(
            {
                "ligand_chain": p_atom["auth_asym_id"],
                "ligand_auth_seq_id": p_atom["auth_seq_id"],
                "ligand": atom_comp(p_atom),
                "terminal_p_atom": norm_atom_name(p_atom),
                "nearest_mg_distance_angstrom": round(nearest_mg, 3),
                "nearby_acceptor_count": len(nearby_acceptors),
                "substrate_mode_hit_count": len(mode_hits),
                "same_chain_companion_count_for_primary_mode_hit": same_chain_companion_count,
                "same_chain_topology_hit": any(
                    row["chain"] == p_atom["auth_asym_id"] for row in nearby_acceptors
                ),
                "reciprocal_cross_chain_like": False,
                "primary_mode_hit": mode_hits[0] if mode_hits else None,
                "nearest_acceptors": nearby_acceptors[:8],
            }
        )

    mode_hits = [hit for hit in local_hits if hit["substrate_mode_hit_count"] > 0]
    topology_pairs: list[tuple[str, str]] = []
    for hit in local_hits:
        gamma_chain = str(hit["ligand_chain"])
        for acceptor in hit.get("nearest_acceptors", []) or []:
            candidate_chain = str(acceptor.get("chain") or "")
            if candidate_chain and gamma_chain:
                topology_pairs.append((candidate_chain, gamma_chain))
    same_chain_topology_detected = any(
        candidate_chain == gamma_chain for candidate_chain, gamma_chain in topology_pairs
    )
    reciprocal_cross_chain_detected = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for left_index, (left_candidate, left_gamma) in enumerate(topology_pairs)
        for right_candidate, right_gamma in topology_pairs[left_index + 1 :]
    )
    topology_ambiguity_counteraxis_hit = (
        same_chain_topology_detected or reciprocal_cross_chain_detected
    )
    for hit in local_hits:
        hit["reciprocal_cross_chain_like"] = reciprocal_cross_chain_detected
    topology_clear_hits = [
        hit
        for hit in mode_hits
        if not topology_ambiguity_counteraxis_hit
    ]
    singleton_topology_clear = len(topology_clear_hits) == 1 and len(mode_hits) == 1
    non_epk_context = not looks_probable_epk(context_text)
    counterexample_candidate = bool(non_epk_context and singleton_topology_clear)
    return {
        "pdb_id": pdb_id,
        "query_names": query_names,
        "title": title,
        "keywords": keywords,
        "polymer_entities": polymer_summaries,
        "family_hint_from_context": context_family_hint(context_text),
        "parse_status": "ok",
        "reviewed": True,
        "probable_epk_from_context": looks_probable_epk(context_text),
        "terminal_p_atom_count": len(terminal_p_atoms),
        "triphosphate_p_atom_count": len(all_triphosphate_p_atoms),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "local_atp_mg_acceptor_hit_count": len(local_hits),
        "substrate_mode_rule_hit_count": len(mode_hits),
        "same_chain_topology_detected": same_chain_topology_detected,
        "reciprocal_cross_chain_topology_detected": reciprocal_cross_chain_detected,
        "topology_ambiguity_counteraxis_hit": topology_ambiguity_counteraxis_hit,
        "topology_clear_substrate_mode_hit_count": len(topology_clear_hits),
        "singleton_topology_clear_substrate_mode_hit": singleton_topology_clear,
        "counterexample_candidate_review_only": counterexample_candidate,
        "counterexample_rationale": (
            "non_ePK_context_plus_singleton_terminal_phosphate_Mg_to_Tyr_or_N_terminal_STY_hit"
            if counterexample_candidate
            else None
        ),
        "best_hits": sorted(
            local_hits,
            key=lambda row: (
                0 if row["substrate_mode_hit_count"] > 0 else 1,
                row["nearest_acceptors"][0]["distance_angstrom"] if row["nearest_acceptors"] else 99,
            ),
        )[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--profile", choices=sorted(QUERY_SURFACE_PROFILES), default="atpase_transport")
    args = parser.parse_args()
    query_surface = QUERY_SURFACE_PROFILES[args.profile]

    query_results: dict[str, list[str]] = {}
    query_errors: dict[str, str] = {}
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = {}

    for query in query_surface:
        try:
            ids = rcsb_full_text_query(query["phrase"], query["rows"])
            query_results[query["name"]] = ids
        except Exception as exc:  # pragma: no cover - recorded as run evidence
            query_errors[query["name"]] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries.setdefault(pdb_id, []).append(query["name"])
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.25)

    for pdb_id in SEED_ATTACK_IDS:
        id_to_queries.setdefault(pdb_id, []).append("seed_attack_surface")
        if pdb_id not in ordered_ids:
            ordered_ids.insert(0, pdb_id)

    ordered_ids = ordered_ids[:MAX_UNIQUE_IDS]
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = fetch_text(RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = fetch_json(RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            row = summarize_entry(pdb_id, id_to_queries.get(pdb_id, []), cif_text, entry_payload)
            row["surface_order"] = index
            rows.append(row)
        except Exception as exc:  # pragma: no cover - recorded as run evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.15)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    candidate_rows = [row for row in reviewed_rows if row.get("counterexample_candidate_review_only")]
    substrate_mode_rows = [row for row in reviewed_rows if row.get("substrate_mode_rule_hit_count", 0) > 0]
    topology_clear_rows = [row for row in reviewed_rows if row.get("topology_clear_substrate_mode_hit_count", 0) > 0]
    now = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now,
            "method": "atpase_transporter_translocase_substrate_mode_stress",
            "surface_profile": args.profile,
            "rule_under_attack": "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 plus bounded topology-ambiguity counteraxis",
            "candidate_threshold_angstrom": DISTANCE_CUTOFF_ANGSTROM,
            "mg_distance_cutoff_angstrom": MG_DISTANCE_CUTOFF_ANGSTROM,
            "max_n_terminal_acceptor_auth_seq_id": MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
            "query_surface": query_surface,
            "seed_attack_ids": SEED_ATTACK_IDS,
            "query_result_counts": {name: len(ids) for name, ids in query_results.items()},
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(reviewed_rows),
            "fetch_error_count": len(fetch_errors),
            "fetch_errors": fetch_errors,
            "substrate_mode_rule_hit_count": len(substrate_mode_rows),
            "topology_clear_substrate_mode_hit_count": len(topology_clear_rows),
            "counterexample_candidate_count": len(candidate_rows),
            "counterexample_candidate_pdb_ids": [row["pdb_id"] for row in candidate_rows],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "counterexample_candidates_review_only": candidate_rows,
        "topology_clear_substrate_mode_hits_review_only": topology_clear_rows,
        "substrate_mode_hits_review_only": substrate_mode_rows[:50],
        "rows": rows,
        "warnings": [
            "Review-only geometry/topology stress evidence; no production ePK scoring or label import.",
            "Topology ambiguity is approximated as singleton source-free local hit absence of same-chain companion or cross-chain-like acceptor hits.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
