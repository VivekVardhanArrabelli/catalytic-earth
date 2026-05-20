#!/usr/bin/env python3
"""ATP-like component-level cross-chain false-positive stress search."""

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
import cross_chain_substrate_mode_stress as cross_chain


LANE_ID = "epk_false_positive_hunter"
MAX_UNIQUE_IDS = 220
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"

COMPONENT_QUERY_SURFACE = [
    {"name": "atp_mg_start_0", "ligand": "ATP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "atp_mg_start_350", "ligand": "ATP", "metal": "MG", "start": 350, "rows": 55},
    {"name": "atp_mg_start_700", "ligand": "ATP", "metal": "MG", "start": 700, "rows": 55},
    {"name": "atp_mg_start_1050", "ligand": "ATP", "metal": "MG", "start": 1050, "rows": 55},
    {"name": "atp_mg_start_1400", "ligand": "ATP", "metal": "MG", "start": 1400, "rows": 55},
    {"name": "anp_mg_start_0", "ligand": "ANP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "anp_mg_start_150", "ligand": "ANP", "metal": "MG", "start": 150, "rows": 55},
    {"name": "anp_mg_start_300", "ligand": "ANP", "metal": "MG", "start": 300, "rows": 55},
    {"name": "ags_mg_start_0", "ligand": "AGS", "metal": "MG", "start": 0, "rows": 55},
    {"name": "ags_mg_start_150", "ligand": "AGS", "metal": "MG", "start": 150, "rows": 55},
    {"name": "acp_mg_start_0", "ligand": "ACP", "metal": "MG", "start": 0, "rows": 55},
    {"name": "acp_mg_start_100", "ligand": "ACP", "metal": "MG", "start": 100, "rows": 55},
]

SEED_ATTACK_IDS = [
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
            "paginate": {
                "start": start,
                "rows": rows,
            },
            "results_content_type": ["experimental"],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=query, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return [row["identifier"].upper() for row in payload.get("result_set", [])]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    query_results: dict[str, list[str]] = {}
    query_errors: dict[str, str] = {}
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)

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

    for pdb_id in SEED_ATTACK_IDS:
        id_to_queries[pdb_id].append("seed_attack_surface")
        if pdb_id not in ordered_ids:
            ordered_ids.insert(0, pdb_id)

    ordered_ids = ordered_ids[:MAX_UNIQUE_IDS]
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            row = cross_chain.summarize_cross_chain_entry(
                pdb_id,
                id_to_queries.get(pdb_id, []),
                cif_text,
                entry_payload,
            )
            row["surface_order"] = index
            rows.append(row)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.12)

    reviewed_rows = [row for row in rows if row.get("reviewed")]
    cross_chain_rows = [
        row for row in reviewed_rows if row.get("cross_chain_substrate_mode_hit_count", 0) > 0
    ]
    topology_clear_rows = [
        row
        for row in reviewed_rows
        if row.get("topology_clear_cross_chain_substrate_mode_hit_count", 0) > 0
    ]
    candidate_rows = [row for row in reviewed_rows if row.get("counterexample_candidate_review_only")]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "component_atp_like_mg_cross_chain_substrate_mode_stress",
            "rule_under_attack": "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0",
            "candidate_threshold_angstrom": base.DISTANCE_CUTOFF_ANGSTROM,
            "mg_distance_cutoff_angstrom": base.MG_DISTANCE_CUTOFF_ANGSTROM,
            "max_n_terminal_acceptor_auth_seq_id": base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
            "query_surface": COMPONENT_QUERY_SURFACE,
            "seed_attack_ids": SEED_ATTACK_IDS,
            "query_result_counts": {name: len(ids) for name, ids in query_results.items()},
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(reviewed_rows),
            "fetch_error_count": len(fetch_errors),
            "fetch_errors": fetch_errors,
            "cross_chain_substrate_mode_hit_count": len(cross_chain_rows),
            "topology_clear_cross_chain_substrate_mode_hit_count": len(topology_clear_rows),
            "counterexample_candidate_count": len(candidate_rows),
            "counterexample_candidate_pdb_ids": [row["pdb_id"] for row in candidate_rows],
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
        },
        "counterexample_candidates_review_only": candidate_rows,
        "topology_clear_cross_chain_substrate_mode_hits_review_only": topology_clear_rows,
        "cross_chain_substrate_mode_hits_review_only": cross_chain_rows[:75],
        "rows": rows,
        "warnings": [
            "Review-only component-level stress evidence; no production ePK scoring or label import.",
            "RCSB component queries sample ATP/ANP/AGS/ACP plus MG entries at fixed offsets, capped before coordinate reduction.",
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
