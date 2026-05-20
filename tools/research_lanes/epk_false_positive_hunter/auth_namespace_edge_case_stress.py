#!/usr/bin/env python3
"""Bounded author-chain namespace edge stress for ePK false-positive hunting.

This helper scans ATP-like/Mg entries for atom_site auth_asym_id/auth_seq_id
edge cases around terminal phosphates and nearby Ser/Thr/Tyr acceptors. It
keeps only compact evidence and invokes the current review-only materializer on
the pressure IDs found by that scan.
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
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import requests

import atpase_substrate_mode_stress as base


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
ACTUAL_MATERIALIZER_GAMMA_CODES = {"ACP", "ANP", "ATP", "DTP"}
CURRENT_ATP_LIKE_LIGANDS = {"A3P", "ACP", "AGS", "ANP", "ATP"}
SCAN_LIGANDS = sorted(CURRENT_ATP_LIKE_LIGANDS | ACTUAL_MATERIALIZER_GAMMA_CODES)
ACCEPTOR_CODES = {"SER": "OG", "THR": "OG1", "TYR": "OH"}
TERMINAL_P_NAMES = {"PG", "P3G", "P03", "P3", "P03G", "PG1", "PG2", "PN", "PB"}
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MAX_UNIQUE_IDS = 520
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
    {"name": "atp_mg_start_180", "ligand": "ATP", "metal": "MG", "start": 180, "rows": 60},
    {"name": "atp_mg_start_360", "ligand": "ATP", "metal": "MG", "start": 360, "rows": 60},
    {"name": "atp_mg_start_720", "ligand": "ATP", "metal": "MG", "start": 720, "rows": 60},
    {"name": "atp_mg_start_1080", "ligand": "ATP", "metal": "MG", "start": 1080, "rows": 60},
    {"name": "anp_mg_start_0", "ligand": "ANP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "anp_mg_start_160", "ligand": "ANP", "metal": "MG", "start": 160, "rows": 55},
    {"name": "anp_mg_start_320", "ligand": "ANP", "metal": "MG", "start": 320, "rows": 55},
    {"name": "acp_mg_start_0", "ligand": "ACP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "acp_mg_start_160", "ligand": "ACP", "metal": "MG", "start": 160, "rows": 55},
    {"name": "ags_mg_start_0", "ligand": "AGS", "metal": "MG", "start": 0, "rows": 55},
    {"name": "ags_mg_start_160", "ligand": "AGS", "metal": "MG", "start": 160, "rows": 55},
    {"name": "a3p_mg_start_0", "ligand": "A3P", "metal": "MG", "start": 0, "rows": 55},
    {"name": "a3p_mg_start_160", "ligand": "A3P", "metal": "MG", "start": 160, "rows": 55},
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
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def component_query(ligand: str, metal: str, start: int, rows: int) -> list[str]:
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                        "operator": "exact_match",
                        "value": ligand,
                    },
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                        "operator": "exact_match",
                        "value": metal,
                    },
                },
            ],
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": start, "rows": rows},
            "results_content_type": ["experimental"],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=query, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return [row["identifier"].upper() for row in payload.get("result_set", [])]


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, Any], dict[str, list[str]]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, Any] = {}
    query_results: dict[str, list[str]] = {}

    for query in COMPONENT_QUERY_SURFACE:
        name = str(query["name"])
        try:
            ids = component_query(
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
        id_to_queries[pdb_id].append("seed_attack_or_namespace_pressure_id")
        if pdb_id in ordered_ids:
            ordered_ids.remove(pdb_id)
        ordered_ids.insert(0, pdb_id)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_results


def normalize(value: str | None) -> str | None:
    if value in {None, "", ".", "?"}:
        return None
    return value


def raw_is_missing(value: str | None, present: bool) -> bool:
    return (not present) or normalize(value) is None


def parse_atom_site_raw(cif_text: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lines = [line.rstrip("\n") for line in cif_text.splitlines()]
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        index += 1
        tags: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("_"):
            tags.append(lines[index].strip())
            index += 1
        if not tags or not all(tag.startswith("_atom_site.") for tag in tags):
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
            return [], {"parse_status": "atom_site_missing_required_tags", "tags": tags}

        atoms: list[dict[str, Any]] = []
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
            if len(values) < len(tags):
                index += 1
                continue

            def raw(tag: str) -> str | None:
                pos = tag_index.get(tag)
                if pos is None or pos >= len(values):
                    return None
                return values[pos]

            model = normalize(raw("_atom_site.pdbx_PDB_model_num")) or "1"
            alt_id = normalize(raw("_atom_site.label_alt_id"))
            if model != "1" or alt_id not in {None, "A"}:
                index += 1
                continue
            try:
                x = float(raw("_atom_site.Cartn_x") or "")
                y = float(raw("_atom_site.Cartn_y") or "")
                z = float(raw("_atom_site.Cartn_z") or "")
            except ValueError:
                index += 1
                continue
            atom = {
                "group_PDB": normalize(raw("_atom_site.group_PDB")) or "",
                "type_symbol": (normalize(raw("_atom_site.type_symbol")) or "").upper(),
                "label_atom_id": normalize(raw("_atom_site.label_atom_id")),
                "auth_atom_id": normalize(raw("_atom_site.auth_atom_id")),
                "label_comp_id": normalize(raw("_atom_site.label_comp_id")),
                "auth_comp_id": normalize(raw("_atom_site.auth_comp_id")),
                "label_asym_id": normalize(raw("_atom_site.label_asym_id")),
                "auth_asym_id": normalize(raw("_atom_site.auth_asym_id")),
                "label_seq_id": normalize(raw("_atom_site.label_seq_id")),
                "auth_seq_id": normalize(raw("_atom_site.auth_seq_id")),
                "label_entity_id": normalize(raw("_atom_site.label_entity_id")),
                "Cartn_x": x,
                "Cartn_y": y,
                "Cartn_z": z,
                "_raw": {
                    "auth_asym_id": raw("_atom_site.auth_asym_id"),
                    "auth_seq_id": raw("_atom_site.auth_seq_id"),
                    "label_asym_id": raw("_atom_site.label_asym_id"),
                    "label_seq_id": raw("_atom_site.label_seq_id"),
                },
                "_present": {
                    "auth_asym_id": "_atom_site.auth_asym_id" in tag_index,
                    "auth_seq_id": "_atom_site.auth_seq_id" in tag_index,
                    "label_asym_id": "_atom_site.label_asym_id" in tag_index,
                    "label_seq_id": "_atom_site.label_seq_id" in tag_index,
                },
            }
            atoms.append(atom)
            index += 1
        return atoms, {
            "parse_status": "ok",
            "auth_asym_id_tag_present": "_atom_site.auth_asym_id" in tag_index,
            "auth_seq_id_tag_present": "_atom_site.auth_seq_id" in tag_index,
            "label_asym_id_tag_present": "_atom_site.label_asym_id" in tag_index,
            "label_seq_id_tag_present": "_atom_site.label_seq_id" in tag_index,
        }
    return [], {"parse_status": "no_atom_site_loop"}


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def preferred_seq_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def optional_int(value: Any) -> int | None:
    try:
        if value in {None, "", ".", "?"}:
            return None
        return int(float(str(value)))
    except (TypeError, ValueError):
        return None


def intish(value: Any) -> int | None:
    match = re.match(r"^-?\d+", str(value or ""))
    return int(match.group(0)) if match else None


def distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    return math.sqrt(
        (float(left["Cartn_x"]) - float(right["Cartn_x"])) ** 2
        + (float(left["Cartn_y"]) - float(right["Cartn_y"])) ** 2
        + (float(left["Cartn_z"]) - float(right["Cartn_z"])) ** 2
    )


def atom_edge_flags(atom: dict[str, Any], *, include_seq: bool) -> dict[str, bool]:
    raw = atom.get("_raw", {})
    present = atom.get("_present", {})
    auth_asym_missing = raw_is_missing(raw.get("auth_asym_id"), bool(present.get("auth_asym_id")))
    auth_seq_missing = raw_is_missing(raw.get("auth_seq_id"), bool(present.get("auth_seq_id")))
    label_asym = normalize(raw.get("label_asym_id"))
    label_seq = normalize(raw.get("label_seq_id"))
    auth_asym = normalize(raw.get("auth_asym_id"))
    auth_seq = normalize(raw.get("auth_seq_id"))
    auth_seq_nonstandard = bool(auth_seq and optional_int(auth_seq) is None)
    flags = {
        "auth_asym_id_missing": auth_asym_missing,
        "auth_asym_id_label_fallback": bool(auth_asym_missing and label_asym),
        "auth_asym_id_differs_from_label": bool(auth_asym and label_asym and auth_asym != label_asym),
    }
    if include_seq:
        flags.update(
            {
                "auth_seq_id_missing": auth_seq_missing,
                "auth_seq_id_label_fallback": bool(auth_seq_missing and label_seq),
                "auth_seq_id_nonstandard": auth_seq_nonstandard,
                "auth_seq_id_nonstandard_label_parseable": bool(
                    auth_seq_nonstandard and optional_int(label_seq) is not None
                ),
            }
        )
    return flags


def edge_reasons_for_pair(terminal: dict[str, Any], acceptor: dict[str, Any]) -> list[str]:
    reasons = []
    terminal_flags = atom_edge_flags(terminal, include_seq=True)
    acceptor_flags = atom_edge_flags(acceptor, include_seq=True)
    for prefix, flags in (("terminal", terminal_flags), ("acceptor", acceptor_flags)):
        for name, value in flags.items():
            if value:
                reasons.append(f"{prefix}_{name}")
    return sorted(reasons)


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


def summarize_entry(
    pdb_id: str,
    query_names: list[str],
    cif_text: str,
    entry_payload: dict[str, Any],
) -> dict[str, Any]:
    atoms, parse_meta = parse_atom_site_raw(cif_text)
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
    topology_pairs: list[tuple[str, str]] = []
    edge_pressure_ids = False
    for terminal in terminals:
        mg_distances = [distance(terminal, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        nearby_acceptors = []
        for acceptor in acceptor_atoms:
            d = distance(terminal, acceptor)
            if d > DISTANCE_CUTOFF_ANGSTROM:
                continue
            seq_id = optional_int(preferred_seq_id(acceptor))
            lenient_seq_id = intish(acceptor.get("auth_seq_id")) or intish(
                acceptor.get("label_seq_id")
            )
            residue = atom_code(acceptor)
            tyrosine = residue == "TYR"
            n_terminal = bool(
                seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
                and residue in ACCEPTOR_CODES
            )
            lenient_n_terminal = bool(
                lenient_seq_id is not None
                and lenient_seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
                and residue in ACCEPTOR_CODES
            )
            edge_reasons = edge_reasons_for_pair(terminal, acceptor)
            substrate_mode = bool(tyrosine or n_terminal)
            edge_pressure = bool(substrate_mode and edge_reasons)
            edge_pressure_ids = edge_pressure_ids or edge_pressure
            acceptor_chain = preferred_chain(acceptor)
            gamma_chain = preferred_chain(terminal)
            if acceptor_chain and gamma_chain:
                topology_pairs.append((acceptor_chain, gamma_chain))
            nearby_acceptors.append(
                {
                    "acceptor_chain": acceptor_chain,
                    "acceptor_auth_chain": acceptor.get("auth_asym_id"),
                    "acceptor_label_chain": acceptor.get("label_asym_id"),
                    "acceptor_auth_seq_id": acceptor.get("auth_seq_id"),
                    "acceptor_label_seq_id": acceptor.get("label_seq_id"),
                    "residue": residue,
                    "atom": atom_name(acceptor),
                    "distance_angstrom": round(d, 3),
                    "tyrosine_acceptor": tyrosine,
                    "n_terminal_acceptor_exact": n_terminal,
                    "n_terminal_acceptor_lenient_intish": lenient_n_terminal,
                    "substrate_mode_rule_hit_exact": substrate_mode,
                    "edge_pressure_hit": edge_pressure,
                    "edge_reasons": edge_reasons[:10],
                }
            )
        nearby_acceptors.sort(
            key=lambda row: (
                0 if row["substrate_mode_rule_hit_exact"] else 1,
                0 if row["edge_pressure_hit"] else 1,
                row["distance_angstrom"],
            )
        )
        if not nearby_acceptors:
            continue
        local_hits.append(
            {
                "ligand": atom_code(terminal),
                "gamma_chain": preferred_chain(terminal),
                "gamma_auth_chain": terminal.get("auth_asym_id"),
                "gamma_label_chain": terminal.get("label_asym_id"),
                "gamma_auth_seq_id": terminal.get("auth_seq_id"),
                "gamma_label_seq_id": terminal.get("label_seq_id"),
                "gamma_atom_name": atom_name(terminal),
                "actual_materializer_gamma_capable": atom_code(terminal)
                in ACTUAL_MATERIALIZER_GAMMA_CODES
                and atom_name(terminal) == "PG",
                "nearest_mg_distance_angstrom": round(nearest_mg, 3),
                "terminal_edge_flags": atom_edge_flags(terminal, include_seq=True),
                "nearby_acceptor_count": len(nearby_acceptors),
                "substrate_mode_hit_count_exact": sum(
                    1 for row in nearby_acceptors if row["substrate_mode_rule_hit_exact"]
                ),
                "edge_pressure_hit_count": sum(
                    1 for row in nearby_acceptors if row["edge_pressure_hit"]
                ),
                "nearest_acceptors": nearby_acceptors[:8],
            }
        )

    same_chain_topology = any(candidate == gamma for candidate, gamma in topology_pairs)
    reciprocal_topology = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for left_index, (left_candidate, left_gamma) in enumerate(topology_pairs)
        for right_candidate, right_gamma in topology_pairs[left_index + 1 :]
    )
    topology_ambiguity = same_chain_topology or reciprocal_topology
    edge_mode_hits = [
        acceptor
        for hit in local_hits
        for acceptor in hit["nearest_acceptors"]
        if acceptor["edge_pressure_hit"]
    ]
    topology_clear_edge_mode_hits = [] if topology_ambiguity else edge_mode_hits
    probable_epk = is_probable_epk(pdb_id, context_text(entry_payload))
    local_hits.sort(
        key=lambda hit: (
            0 if hit["edge_pressure_hit_count"] else 1,
            0 if hit["substrate_mode_hit_count_exact"] else 1,
            hit["nearest_mg_distance_angstrom"],
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
        "probable_epk_from_context": probable_epk,
        "known_epk_positive_id": pdb_id.upper() in KNOWN_EPK_POSITIVE_IDS,
        "terminal_p_atom_count": len(terminals),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "local_gamma_acceptor_hit_count": len(local_hits),
        "edge_pressure_hit_count": len(edge_mode_hits),
        "same_chain_topology_detected": same_chain_topology,
        "reciprocal_cross_chain_topology_detected": reciprocal_topology,
        "topology_ambiguity_counteraxis_hit": topology_ambiguity,
        "topology_clear_edge_pressure_hit_count": len(topology_clear_edge_mode_hits),
        "auth_namespace_edge_pressure": edge_pressure_ids,
        "local_hits": local_hits[:8],
    }


def fetch_summarized(
    pdb_id: str,
    query_names: list[str],
) -> tuple[dict[str, Any], str | None]:
    cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
    entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    return summarize_entry(pdb_id, query_names, cif_text, entry_payload), cif_text


def load_materializer(repo_root: Path):
    src_path = str(repo_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from catalytic_earth.labels import (  # pylint: disable=import-outside-toplevel
        build_epk_heteromeric_positive_coverage_candidate_scout,
    )

    return build_epk_heteromeric_positive_coverage_candidate_scout


def materializer_probe(
    *,
    repo_root: Path,
    started_at: str,
    pressure_ids: list[str],
    cif_text_by_pdb: dict[str, str],
) -> dict[str, Any]:
    if not pressure_ids:
        return {
            "metadata": {
                "lane_id": LANE_ID,
                "started_at": started_at,
                "ended_at": now_utc(),
                "method": "epk_heteromeric_positive_coverage_candidate_scout",
                "run_context": "actual_materializer_probe_for_auth_namespace_edge_pressure_ids",
                "input_candidate_count": 0,
                "candidate_status_counts": {},
                "fetch_failure_count": 0,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "raw_coordinate_files_written": False,
            },
            "rows": [],
        }
    materializer = load_materializer(repo_root)
    stub_audit = {
        "metadata": {
            "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            "method": "lane_stub_auth_namespace_edge_case_stress",
            "full_probe_heteromeric_candidate_pdb_ids": [],
        }
    }
    return materializer(
        epk_heteromeric_chain_topology_signal_audit=stub_audit,
        candidate_pdb_ids=pressure_ids,
        source_query="epk_false_positive_hunter_auth_namespace_edge_pressure_ids",
        candidate_threshold_angstrom=DISTANCE_CUTOFF_ANGSTROM,
        cif_text_by_pdb=cif_text_by_pdb,
    )


def materializer_counterexample_rows(
    materializer: dict[str, Any],
    probable_epk_by_pdb: dict[str, bool],
) -> list[dict[str, Any]]:
    rows = []
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        if probable_epk_by_pdb.get(pdb_id):
            continue
        hits = row.get("heteromeric_candidate_hits", []) or []
        if not hits:
            continue
        kept_hits = []
        for hit in hits:
            residue = str(hit.get("candidate_residue_code") or "").upper()
            seq_id = optional_int(hit.get("candidate_auth_seq_id"))
            substrate_mode = residue == "TYR" or (
                residue in ACCEPTOR_CODES
                and seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
            )
            same_chain = str(hit.get("candidate_chain_name") or "") == str(
                hit.get("gamma_associated_polymer_chain_name") or ""
            )
            if substrate_mode and not same_chain:
                kept_hits.append(hit)
        if kept_hits:
            rows.append({**row, "substrate_mode_materializer_hits": kept_hits})
    return rows


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
            row, cif_text = fetch_summarized(pdb_id, id_to_queries.get(pdb_id, []))
            row["surface_order"] = index
            rows.append(row)
            if row.get("auth_namespace_edge_pressure"):
                cif_text_by_pdb[pdb_id] = cif_text or ""
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.08)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    edge_rows = [row for row in reviewed_rows if row.get("auth_namespace_edge_pressure")]
    pressure_ids = sorted({row["pdb_id"] for row in edge_rows})
    materializer = materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=pressure_ids,
        cif_text_by_pdb=cif_text_by_pdb,
    )
    probable_epk_by_pdb = {
        str(row.get("pdb_id") or "").upper(): bool(row.get("probable_epk_from_context"))
        for row in reviewed_rows
    }
    materializer_counterexamples = materializer_counterexample_rows(
        materializer,
        probable_epk_by_pdb,
    )
    materializer_status_counts = Counter(
        str(row.get("candidate_status") or "") for row in materializer.get("rows", []) or []
    )
    current_rule_counterexamples = [
        row
        for row in edge_rows
        if not row.get("probable_epk_from_context")
        and int(row.get("topology_clear_edge_pressure_hit_count") or 0) > 0
    ]
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "auth_namespace_edge_case_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0"
            ),
            "search_surface": {
                "component_query_surface": COMPONENT_QUERY_SURFACE,
                "seed_ids": SEED_IDS,
                "scan_ligands": SCAN_LIGANDS,
                "current_atp_like_ligands": sorted(CURRENT_ATP_LIKE_LIGANDS),
                "actual_materializer_gamma_capable_codes": sorted(
                    ACTUAL_MATERIALIZER_GAMMA_CODES
                ),
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
            "auth_namespace_edge_pressure_entry_count": len(edge_rows),
            "auth_namespace_edge_pressure_pdb_ids": pressure_ids,
            "current_rule_counterexample_count": len(current_rule_counterexamples),
            "current_rule_counterexample_pdb_ids": [
                row["pdb_id"] for row in current_rule_counterexamples
            ],
            "actual_materializer_input_count": len(pressure_ids),
            "actual_materializer_candidate_status_counts": dict(materializer_status_counts),
            "actual_materializer_substrate_mode_counterexample_count": len(
                materializer_counterexamples
            ),
            "actual_materializer_substrate_mode_counterexample_pdb_ids": [
                row["pdb_id"] for row in materializer_counterexamples
            ],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "fetch_errors": fetch_errors,
        "auth_namespace_edge_pressure_rows": edge_rows,
        "current_rule_counterexample_candidates_review_only": current_rule_counterexamples,
        "actual_materializer_probe": materializer,
        "actual_materializer_substrate_mode_counterexamples_review_only": materializer_counterexamples,
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
    raise SystemExit(main())
