#!/usr/bin/env python3
"""Chain-namespace and non-ATP gamma-like ePK false-positive stress search.

This lane helper fetches mmCIFs in memory and writes compact evidence only. It
attacks two bounded surfaces:

1. current ATP-like ligand hits whose topology classification changes between
   auth_asym_id and label_asym_id namespaces;
2. non-ATP guanosine/transition-state-like Mg structures with the same local
   Tyr-or-N-terminal-STY geometry.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import requests

import atpase_substrate_mode_stress as base


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
MAX_UNIQUE_IDS = 260

CURRENT_ATP_LIKE_LIGANDS = {"ATP", "ANP", "AGS", "ACP", "A3P"}
NON_ATP_GAMMA_LIKE_LIGANDS = {"GTP", "GNP", "GSP", "GDP", "ADP"}
SCAN_LIGANDS = CURRENT_ATP_LIKE_LIGANDS | NON_ATP_GAMMA_LIKE_LIGANDS

COMPONENT_QUERY_SURFACE = [
    {"name": "atp_mg_start_0", "ligand": "ATP", "metal": "MG", "start": 0, "rows": 45},
    {"name": "atp_mg_start_600", "ligand": "ATP", "metal": "MG", "start": 600, "rows": 45},
    {"name": "anp_mg_start_0", "ligand": "ANP", "metal": "MG", "start": 0, "rows": 45},
    {"name": "ags_mg_start_0", "ligand": "AGS", "metal": "MG", "start": 0, "rows": 45},
    {"name": "acp_mg_start_0", "ligand": "ACP", "metal": "MG", "start": 0, "rows": 45},
    {"name": "gtp_mg_start_0", "ligand": "GTP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "gtp_mg_start_200", "ligand": "GTP", "metal": "MG", "start": 200, "rows": 55},
    {"name": "gnp_mg_start_0", "ligand": "GNP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "gsp_mg_start_0", "ligand": "GSP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "gdp_mg_start_0", "ligand": "GDP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "adp_mg_start_0", "ligand": "ADP", "metal": "MG", "start": 0, "rows": 55},
]

FULL_TEXT_QUERY_SURFACE = [
    {"name": "gtp_magnesium_tyrosine", "phrase": "GTP magnesium tyrosine", "rows": 45},
    {"name": "gtp_magnesium_n_terminal_serine", "phrase": "GTP magnesium N-terminal serine", "rows": 45},
    {"name": "gtp_magnesium_n_terminal_threonine", "phrase": "GTP magnesium N-terminal threonine", "rows": 45},
    {"name": "gmp_pnp_magnesium_tyrosine", "phrase": "GMPPNP magnesium tyrosine", "rows": 45},
    {"name": "gtp_gamma_s_magnesium_tyrosine", "phrase": "GTP gamma S magnesium tyrosine", "rows": 45},
    {"name": "gtpase_transition_state_magnesium", "phrase": "GTPase transition state magnesium", "rows": 45},
    {"name": "gdp_aluminum_fluoride_magnesium_tyrosine", "phrase": "GDP aluminum fluoride magnesium tyrosine", "rows": 45},
    {"name": "adp_aluminum_fluoride_magnesium_tyrosine", "phrase": "ADP aluminum fluoride magnesium tyrosine", "rows": 45},
]

SEED_IDS = [
    "7CAG",
    "8BMS",
    "9L3M",
    "9L3U",
    "7ZE5",
    "4KFT",
    "5TT6",
    "6NOO",
    "9NBW",
]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def chain_value(atom: dict[str, Any], namespace: str) -> str:
    key = "label_asym_id" if namespace == "label" else "auth_asym_id"
    return str(atom.get(key) or "")


def mode_acceptor(acceptor: dict[str, Any], namespace: str) -> dict[str, Any]:
    seq_id = base.parse_intish(acceptor["auth_seq_id"])
    is_n_terminal = seq_id is not None and seq_id <= base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    is_tyr = base.atom_comp(acceptor) == "TYR"
    return {
        "chain_namespace": namespace,
        "chain": chain_value(acceptor, namespace),
        "auth_chain": chain_value(acceptor, "auth"),
        "label_chain": chain_value(acceptor, "label"),
        "auth_seq_id": acceptor["auth_seq_id"],
        "label_seq_id": acceptor["label_seq_id"],
        "residue": base.atom_comp(acceptor),
        "atom": base.norm_atom_name(acceptor),
        "n_terminal_acceptor": is_n_terminal,
        "tyrosine_acceptor": is_tyr,
        "substrate_mode_rule_hit": is_tyr or is_n_terminal,
    }


def hit_pairs_for_namespace(local_hits: list[dict[str, Any]], namespace: str) -> list[tuple[str, str]]:
    pairs = []
    for hit in local_hits:
        ligand_chain = hit[f"{namespace}_ligand_chain"]
        for acceptor in hit[f"{namespace}_nearby_acceptors"]:
            pairs.append((str(acceptor["chain"]), str(ligand_chain)))
    return pairs


def same_chain_detected(pairs: list[tuple[str, str]]) -> bool:
    return any(candidate == ligand for candidate, ligand in pairs)


def reciprocal_detected(pairs: list[tuple[str, str]]) -> bool:
    return any(
        left_candidate == right_ligand
        and left_ligand == right_candidate
        and left_candidate != left_ligand
        for left_index, (left_candidate, left_ligand) in enumerate(pairs)
        for right_candidate, right_ligand in pairs[left_index + 1 :]
    )


def ligand_family(comp_id: str) -> str:
    if comp_id in CURRENT_ATP_LIKE_LIGANDS:
        return "current_atp_like"
    if comp_id in {"GTP", "GNP", "GSP", "GDP"}:
        return "non_atp_guanosine_like"
    if comp_id == "ADP":
        return "transition_state_adp_like"
    return "other"


def terminal_p_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferred = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in SCAN_LIGANDS
        and base.norm_atom_name(atom) in base.TERMINAL_PHOSPHATE_NAMES
    ]
    fallback = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in SCAN_LIGANDS
    ]
    return preferred or fallback


def compact_hit(hit: dict[str, Any]) -> dict[str, Any]:
    return {
        "ligand": hit["ligand"],
        "ligand_family": hit["ligand_family"],
        "terminal_p_atom": hit["terminal_p_atom"],
        "auth_ligand_chain": hit["auth_ligand_chain"],
        "label_ligand_chain": hit["label_ligand_chain"],
        "ligand_auth_seq_id": hit["ligand_auth_seq_id"],
        "nearest_mg_distance_angstrom": hit["nearest_mg_distance_angstrom"],
        "auth_cross_chain_substrate_mode_hit_count": hit["auth_cross_chain_substrate_mode_hit_count"],
        "label_cross_chain_substrate_mode_hit_count": hit["label_cross_chain_substrate_mode_hit_count"],
        "auth_same_chain_substrate_mode_hit_count": hit["auth_same_chain_substrate_mode_hit_count"],
        "label_same_chain_substrate_mode_hit_count": hit["label_same_chain_substrate_mode_hit_count"],
        "namespace_flip_count": hit["namespace_flip_count"],
        "best_auth_acceptors": hit["auth_nearby_acceptors"][:4],
        "best_label_acceptors": hit["label_nearby_acceptors"][:4],
    }


def summarize_entry(
    pdb_id: str,
    query_names: list[str],
    cif_text: str,
    entry_payload: dict[str, Any],
) -> dict[str, Any]:
    title = entry_payload.get("struct", {}).get("title", "")
    keywords = base.entry_keywords(entry_payload)
    polymer_summaries = base.fetch_polymer_summaries(pdb_id, entry_payload)
    context_text = " ".join(
        str(part or "")
        for part in [
            title,
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
            " ".join(str(summary.get("description") or "") for summary in polymer_summaries),
        ]
    )
    atoms = base.parse_atom_site(cif_text)
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

    p_atoms = terminal_p_atoms(atoms)
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and (base.atom_comp(atom) in base.MAGNESIUM_CODES or atom["type_symbol"] == "MG")
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "ATOM"
        and (base.atom_comp(atom), base.norm_atom_name(atom)) in base.ACCEPTOR_ATOMS
    ]

    local_hits: list[dict[str, Any]] = []
    for p_atom in p_atoms:
        mg_distances = [base.distance(p_atom, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > base.MG_DISTANCE_CUTOFF_ANGSTROM:
            continue

        namespace_acceptors: dict[str, list[dict[str, Any]]] = {}
        namespace_cross_counts: dict[str, int] = {}
        namespace_same_counts: dict[str, int] = {}
        for namespace in ["auth", "label"]:
            nearby_acceptors = []
            ligand_chain = chain_value(p_atom, namespace)
            for acceptor in acceptor_atoms:
                d = base.distance(p_atom, acceptor)
                if d > base.DISTANCE_CUTOFF_ANGSTROM:
                    continue
                row = mode_acceptor(acceptor, namespace)
                row["distance_angstrom"] = round(d, 3)
                row["same_chain_to_ligand"] = row["chain"] == ligand_chain
                nearby_acceptors.append(row)
            nearby_acceptors.sort(key=lambda row: row["distance_angstrom"])
            namespace_acceptors[namespace] = nearby_acceptors
            namespace_cross_counts[namespace] = sum(
                1
                for row in nearby_acceptors
                if row["substrate_mode_rule_hit"] and row["chain"] != ligand_chain
            )
            namespace_same_counts[namespace] = sum(
                1
                for row in nearby_acceptors
                if row["substrate_mode_rule_hit"] and row["chain"] == ligand_chain
            )

        namespace_flip_count = 0
        for auth_row, label_row in zip(
            namespace_acceptors["auth"],
            namespace_acceptors["label"],
            strict=False,
        ):
            if not auth_row["substrate_mode_rule_hit"]:
                continue
            auth_same = auth_row["same_chain_to_ligand"]
            label_same = label_row["same_chain_to_ligand"]
            if auth_same != label_same:
                namespace_flip_count += 1

        if not namespace_acceptors["auth"] and not namespace_acceptors["label"]:
            continue

        local_hits.append(
            {
                "ligand": base.atom_comp(p_atom),
                "ligand_family": ligand_family(base.atom_comp(p_atom)),
                "terminal_p_atom": base.norm_atom_name(p_atom),
                "auth_ligand_chain": chain_value(p_atom, "auth"),
                "label_ligand_chain": chain_value(p_atom, "label"),
                "ligand_auth_seq_id": p_atom["auth_seq_id"],
                "ligand_label_seq_id": p_atom["label_seq_id"],
                "nearest_mg_distance_angstrom": round(nearest_mg, 3),
                "auth_nearby_acceptors": namespace_acceptors["auth"][:10],
                "label_nearby_acceptors": namespace_acceptors["label"][:10],
                "auth_cross_chain_substrate_mode_hit_count": namespace_cross_counts["auth"],
                "label_cross_chain_substrate_mode_hit_count": namespace_cross_counts["label"],
                "auth_same_chain_substrate_mode_hit_count": namespace_same_counts["auth"],
                "label_same_chain_substrate_mode_hit_count": namespace_same_counts["label"],
                "namespace_flip_count": namespace_flip_count,
            }
        )

    auth_pairs = hit_pairs_for_namespace(local_hits, "auth")
    label_pairs = hit_pairs_for_namespace(local_hits, "label")
    auth_same_chain = same_chain_detected(auth_pairs)
    label_same_chain = same_chain_detected(label_pairs)
    auth_reciprocal = reciprocal_detected(auth_pairs)
    label_reciprocal = reciprocal_detected(label_pairs)
    auth_topology_blocked = auth_same_chain or auth_reciprocal
    label_topology_blocked = label_same_chain or label_reciprocal

    current_auth_topology_clear = [
        hit
        for hit in local_hits
        if hit["ligand_family"] == "current_atp_like"
        and hit["auth_cross_chain_substrate_mode_hit_count"] > 0
        and not auth_topology_blocked
    ]
    current_label_topology_clear = [
        hit
        for hit in local_hits
        if hit["ligand_family"] == "current_atp_like"
        and hit["label_cross_chain_substrate_mode_hit_count"] > 0
        and not label_topology_blocked
    ]
    namespace_artifact_hits = [
        hit
        for hit in local_hits
        if hit["ligand_family"] == "current_atp_like" and hit["namespace_flip_count"] > 0
    ]
    label_clear_auth_blocked = [
        hit
        for hit in current_label_topology_clear
        if auth_topology_blocked or hit["auth_cross_chain_substrate_mode_hit_count"] == 0
    ]
    non_atp_pressure_hits = [
        hit
        for hit in local_hits
        if hit["ligand_family"] != "current_atp_like"
        and (
            hit["auth_cross_chain_substrate_mode_hit_count"]
            + hit["label_cross_chain_substrate_mode_hit_count"]
            + hit["auth_same_chain_substrate_mode_hit_count"]
            + hit["label_same_chain_substrate_mode_hit_count"]
        )
        > 0
    ]
    non_epk_context = not base.looks_probable_epk(context_text)
    strict_current_auth_counterexample = bool(non_epk_context and current_auth_topology_clear)
    namespace_counterexample_pressure = bool(non_epk_context and label_clear_auth_blocked)

    return {
        "pdb_id": pdb_id,
        "query_names": query_names,
        "title": title,
        "keywords": keywords,
        "polymer_entities": polymer_summaries,
        "family_hint_from_context": base.context_family_hint(context_text),
        "parse_status": "ok",
        "reviewed": True,
        "probable_epk_from_context": base.looks_probable_epk(context_text),
        "terminal_scan_ligand_p_atom_count": len(p_atoms),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "local_mg_hydroxyl_hit_count": len(local_hits),
        "auth_same_chain_topology_detected": auth_same_chain,
        "auth_reciprocal_cross_chain_topology_detected": auth_reciprocal,
        "label_same_chain_topology_detected": label_same_chain,
        "label_reciprocal_cross_chain_topology_detected": label_reciprocal,
        "auth_topology_ambiguity_counteraxis_hit": auth_topology_blocked,
        "label_topology_ambiguity_counteraxis_hit": label_topology_blocked,
        "current_atp_like_auth_topology_clear_hit_count": len(current_auth_topology_clear),
        "current_atp_like_label_topology_clear_hit_count": len(current_label_topology_clear),
        "current_atp_like_namespace_artifact_hit_count": len(namespace_artifact_hits),
        "current_atp_like_label_clear_auth_blocked_hit_count": len(label_clear_auth_blocked),
        "non_atp_gamma_like_pressure_hit_count": len(non_atp_pressure_hits),
        "counterexample_candidate_current_auth_review_only": strict_current_auth_counterexample,
        "namespace_assignment_counterexample_pressure_review_only": namespace_counterexample_pressure,
        "counterexample_rationale": (
            "non_ePK_current_ATP_like_auth_namespace_topology_clear_cross_chain_substrate_mode"
            if strict_current_auth_counterexample
            else None
        ),
        "namespace_pressure_rationale": (
            "non_ePK_current_ATP_like_label_namespace_clear_but_auth_namespace_blocked_or_same_chain"
            if namespace_counterexample_pressure
            else None
        ),
        "current_atp_like_auth_topology_clear_hits": [
            compact_hit(hit) for hit in current_auth_topology_clear[:5]
        ],
        "current_atp_like_label_topology_clear_hits": [
            compact_hit(hit) for hit in current_label_topology_clear[:5]
        ],
        "current_atp_like_namespace_artifact_hits": [
            compact_hit(hit) for hit in namespace_artifact_hits[:8]
        ],
        "current_atp_like_label_clear_auth_blocked_hits": [
            compact_hit(hit) for hit in label_clear_auth_blocked[:8]
        ],
        "non_atp_gamma_like_pressure_hits": [
            compact_hit(hit) for hit in non_atp_pressure_hits[:8]
        ],
        "best_hits": [
            compact_hit(hit)
            for hit in sorted(
                local_hits,
                key=lambda row: (
                    0 if row["namespace_flip_count"] else 1,
                    0 if row["ligand_family"] != "current_atp_like" else 1,
                    row["auth_nearby_acceptors"][0]["distance_angstrom"]
                    if row["auth_nearby_acceptors"]
                    else 99,
                ),
            )[:8]
        ],
    }


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, list[str]]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_results: dict[str, list[str]] = {}

    for query in COMPONENT_QUERY_SURFACE:
        try:
            ids = component_query(
                str(query["ligand"]),
                str(query["metal"]),
                int(query["start"]),
                int(query["rows"]),
            )
            query_results[str(query["name"])] = ids
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[str(query["name"])] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries[pdb_id].append(str(query["name"]))
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.2)

    for query in FULL_TEXT_QUERY_SURFACE:
        try:
            ids = base.rcsb_full_text_query(str(query["phrase"]), int(query["rows"]))
            query_results[str(query["name"])] = ids
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[str(query["name"])] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries[pdb_id].append(str(query["name"]))
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.25)

    for pdb_id in SEED_IDS:
        id_to_queries[pdb_id].append("seed_attack_surface")
        if pdb_id not in ordered_ids:
            ordered_ids.insert(0, pdb_id)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    ordered_ids, id_to_queries, query_errors, query_results = collect_ids()
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            row = summarize_entry(pdb_id, id_to_queries.get(pdb_id, []), cif_text, entry_payload)
            row["surface_order"] = index
            rows.append(row)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.12)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    strict_counterexamples = [
        row for row in reviewed_rows if row.get("counterexample_candidate_current_auth_review_only")
    ]
    namespace_pressure_rows = [
        row for row in reviewed_rows if row.get("namespace_assignment_counterexample_pressure_review_only")
    ]
    namespace_artifact_rows = [
        row
        for row in reviewed_rows
        if row.get("current_atp_like_namespace_artifact_hit_count", 0) > 0
    ]
    non_atp_pressure_rows = [
        row for row in reviewed_rows if row.get("non_atp_gamma_like_pressure_hit_count", 0) > 0
    ]
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "gamma_chain_assignment_namespace_and_non_atp_stress",
            "rule_under_attack": "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0",
            "candidate_threshold_angstrom": base.DISTANCE_CUTOFF_ANGSTROM,
            "mg_distance_cutoff_angstrom": base.MG_DISTANCE_CUTOFF_ANGSTROM,
            "max_n_terminal_acceptor_auth_seq_id": base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
            "current_atp_like_ligands": sorted(CURRENT_ATP_LIKE_LIGANDS),
            "non_atp_gamma_like_ligands": sorted(NON_ATP_GAMMA_LIKE_LIGANDS),
            "component_query_surface": COMPONENT_QUERY_SURFACE,
            "full_text_query_surface": FULL_TEXT_QUERY_SURFACE,
            "seed_ids": SEED_IDS,
            "query_result_counts": {name: len(ids) for name, ids in query_results.items()},
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(reviewed_rows),
            "fetch_error_count": len(fetch_errors),
            "fetch_errors": fetch_errors,
            "current_auth_counterexample_candidate_count": len(strict_counterexamples),
            "current_auth_counterexample_candidate_pdb_ids": [
                row["pdb_id"] for row in strict_counterexamples
            ],
            "namespace_assignment_pressure_count": len(namespace_pressure_rows),
            "namespace_assignment_pressure_pdb_ids": [
                row["pdb_id"] for row in namespace_pressure_rows
            ],
            "current_atp_like_namespace_artifact_row_count": len(namespace_artifact_rows),
            "non_atp_gamma_like_pressure_row_count": len(non_atp_pressure_rows),
            "non_atp_gamma_like_pressure_pdb_ids": [
                row["pdb_id"] for row in non_atp_pressure_rows[:50]
            ],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "counterexample_candidates_current_auth_review_only": strict_counterexamples,
        "namespace_assignment_counterexample_pressure_review_only": namespace_pressure_rows[:40],
        "current_atp_like_namespace_artifact_rows_review_only": namespace_artifact_rows[:60],
        "non_atp_gamma_like_pressure_rows_review_only": non_atp_pressure_rows[:80],
        "rows": rows,
        "warnings": [
            "Review-only adversarial evidence; no production ePK scoring or label import.",
            "Chain namespace pressure compares auth_asym_id and label_asym_id without claiming which namespace production should use.",
            "Non-ATP gamma-like rows are pressure evidence only unless their ligand is in the current ATP-like ligand set.",
            "No raw coordinate files are written; mmCIF input is reduced to compact chain, residue, and distance evidence.",
        ],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
