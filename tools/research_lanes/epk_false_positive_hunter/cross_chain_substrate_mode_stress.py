#!/usr/bin/env python3
"""Cross-chain source-free ePK false-positive stress search.

Queries bounded RCSB full-text surfaces for non-ePK ATP/Mg structures, fetches
mmCIF files in memory, and writes only compact chain/distance evidence. The
target adversarial shape is a terminal ATP-like phosphate with Mg and a Tyr or
N-terminal Ser/Thr/Tyr hydroxyl on a different polymer chain, without same-chain
or reciprocal cross-chain topology ambiguity.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import atpase_substrate_mode_stress as base


LANE_ID = "epk_false_positive_hunter"
QUERY_ROWS = 45
MAX_UNIQUE_IDS = 150

CROSS_CHAIN_QUERY_SURFACE_PROFILES = {
    "general_complex": [
        {
            "name": "atp_magnesium_heterodimer",
            "phrase": "ATP magnesium heterodimer",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_magnesium_protein_complex",
            "phrase": "ATP magnesium protein complex",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atpase_dimer_atp_magnesium",
            "phrase": "ATPase dimer ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "abc_transporter_dimer_atp_magnesium",
            "phrase": "ABC transporter dimer ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "translocase_complex_atp_magnesium",
            "phrase": "translocase complex ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_dependent_ligase_protein_complex",
            "phrase": "ATP-dependent ligase protein complex ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "aminoacyl_trna_synthetase_complex_atp_magnesium",
            "phrase": "aminoacyl-tRNA synthetase complex ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "ntpase_protein_complex_atp_magnesium",
            "phrase": "NTPase protein complex ATP magnesium",
            "rows": QUERY_ROWS,
        },
    ],
    "interface_oligomer": [
        {
            "name": "amppnp_magnesium_dimer",
            "phrase": "AMPPNP magnesium dimer",
            "rows": QUERY_ROWS,
        },
        {
            "name": "adpnp_magnesium_protein_complex",
            "phrase": "ADPNP magnesium protein complex",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_gamma_s_magnesium_dimer",
            "phrase": "ATP gamma S magnesium dimer",
            "rows": QUERY_ROWS,
        },
        {
            "name": "aaa_atpase_substrate_atp_magnesium",
            "phrase": "AAA ATPase substrate ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "proteasome_atpase_substrate_atp_magnesium",
            "phrase": "proteasome ATPase substrate ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "clp_atpase_substrate_atp_magnesium",
            "phrase": "Clp ATPase substrate ATP magnesium",
            "rows": QUERY_ROWS,
        },
        {
            "name": "hsp90_atp_magnesium_dimer",
            "phrase": "HSP90 ATP magnesium dimer",
            "rows": QUERY_ROWS,
        },
        {
            "name": "hsp70_atp_magnesium_peptide",
            "phrase": "HSP70 ATP magnesium peptide",
            "rows": QUERY_ROWS,
        },
        {
            "name": "reca_atp_magnesium_filament",
            "phrase": "RecA ATP magnesium filament",
            "rows": QUERY_ROWS,
        },
        {
            "name": "rad51_atp_magnesium_filament",
            "phrase": "Rad51 ATP magnesium filament",
            "rows": QUERY_ROWS,
        },
        {
            "name": "helicase_atp_magnesium_dna_complex",
            "phrase": "helicase ATP magnesium DNA complex",
            "rows": QUERY_ROWS,
        },
        {
            "name": "smc_atpase_atp_magnesium_dimer",
            "phrase": "SMC ATPase ATP magnesium dimer",
            "rows": QUERY_ROWS,
        },
    ],
    "acceptor_targeted": [
        {
            "name": "atp_magnesium_tyrosine_complex",
            "phrase": "ATP magnesium tyrosine complex",
            "rows": QUERY_ROWS,
        },
        {
            "name": "amppnp_magnesium_tyrosine",
            "phrase": "AMPPNP magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atpase_atp_magnesium_tyrosine",
            "phrase": "ATPase ATP magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_dependent_ligase_atp_magnesium_tyrosine",
            "phrase": "ATP-dependent ligase ATP magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "synthetase_atp_magnesium_tyrosine",
            "phrase": "synthetase ATP magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_magnesium_n_terminal_serine",
            "phrase": "ATP magnesium N-terminal serine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_magnesium_n_terminal_threonine",
            "phrase": "ATP magnesium N-terminal threonine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_magnesium_n_terminal_tyrosine",
            "phrase": "ATP magnesium N-terminal tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "atp_gamma_s_magnesium_tyrosine",
            "phrase": "ATP gamma S magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
        {
            "name": "adpnp_magnesium_tyrosine",
            "phrase": "ADPNP magnesium tyrosine",
            "rows": QUERY_ROWS,
        },
    ],
}

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


def mode_acceptor(acceptor: dict[str, Any]) -> dict[str, Any]:
    seq_id = base.parse_intish(acceptor["auth_seq_id"])
    is_n_terminal = seq_id is not None and seq_id <= base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    is_tyr = base.atom_comp(acceptor) == "TYR"
    return {
        "chain": acceptor["auth_asym_id"],
        "auth_seq_id": acceptor["auth_seq_id"],
        "residue": base.atom_comp(acceptor),
        "atom": base.norm_atom_name(acceptor),
        "n_terminal_acceptor": is_n_terminal,
        "tyrosine_acceptor": is_tyr,
        "substrate_mode_rule_hit": is_tyr or is_n_terminal,
    }


def summarize_cross_chain_entry(
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

    terminal_p_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in base.TERMINAL_LIGANDS
        and base.norm_atom_name(atom) in base.TERMINAL_PHOSPHATE_NAMES
    ]
    all_triphosphate_p_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in base.TERMINAL_LIGANDS
    ]
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
    topology_pairs: list[tuple[str, str]] = []
    terminal_atoms_for_distance = terminal_p_atoms or all_triphosphate_p_atoms
    for p_atom in terminal_atoms_for_distance:
        mg_distances = [base.distance(p_atom, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > base.MG_DISTANCE_CUTOFF_ANGSTROM:
            continue

        nearby_acceptors = []
        for acceptor in acceptor_atoms:
            d = base.distance(p_atom, acceptor)
            if d > base.DISTANCE_CUTOFF_ANGSTROM:
                continue
            row = mode_acceptor(acceptor)
            row["distance_angstrom"] = round(d, 3)
            nearby_acceptors.append(row)
            topology_pairs.append((str(row["chain"]), str(p_atom["auth_asym_id"])))

        nearby_acceptors.sort(key=lambda row: row["distance_angstrom"])
        if not nearby_acceptors:
            continue

        same_chain_acceptors = [
            row for row in nearby_acceptors if str(row["chain"]) == str(p_atom["auth_asym_id"])
        ]
        cross_chain_mode_hits = [
            row
            for row in nearby_acceptors
            if row["substrate_mode_rule_hit"] and str(row["chain"]) != str(p_atom["auth_asym_id"])
        ]
        mode_hits = [row for row in nearby_acceptors if row["substrate_mode_rule_hit"]]
        local_hits.append(
            {
                "ligand_chain": p_atom["auth_asym_id"],
                "ligand_auth_seq_id": p_atom["auth_seq_id"],
                "ligand": base.atom_comp(p_atom),
                "terminal_p_atom": base.norm_atom_name(p_atom),
                "nearest_mg_distance_angstrom": round(nearest_mg, 3),
                "nearby_acceptor_count": len(nearby_acceptors),
                "same_chain_acceptor_count": len(same_chain_acceptors),
                "substrate_mode_hit_count": len(mode_hits),
                "cross_chain_substrate_mode_hit_count": len(cross_chain_mode_hits),
                "primary_cross_chain_mode_hit": cross_chain_mode_hits[0] if cross_chain_mode_hits else None,
                "nearest_acceptors": nearby_acceptors[:10],
            }
        )

    same_chain_topology_detected = any(candidate == gamma for candidate, gamma in topology_pairs)
    reciprocal_cross_chain_detected = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for left_index, (left_candidate, left_gamma) in enumerate(topology_pairs)
        for right_candidate, right_gamma in topology_pairs[left_index + 1 :]
    )
    topology_ambiguity_counteraxis_hit = same_chain_topology_detected or reciprocal_cross_chain_detected
    cross_chain_hits = [
        hit
        for hit in local_hits
        if hit["cross_chain_substrate_mode_hit_count"] > 0
    ]
    topology_clear_cross_chain_hits = [
        hit
        for hit in cross_chain_hits
        if hit["same_chain_acceptor_count"] == 0 and not reciprocal_cross_chain_detected
    ]
    non_epk_context = not base.looks_probable_epk(context_text)
    counterexample_candidate = bool(non_epk_context and topology_clear_cross_chain_hits)

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
        "terminal_p_atom_count": len(terminal_p_atoms),
        "triphosphate_p_atom_count": len(all_triphosphate_p_atoms),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "local_atp_mg_acceptor_hit_count": len(local_hits),
        "cross_chain_substrate_mode_hit_count": len(cross_chain_hits),
        "topology_clear_cross_chain_substrate_mode_hit_count": len(topology_clear_cross_chain_hits),
        "same_chain_topology_detected": same_chain_topology_detected,
        "reciprocal_cross_chain_topology_detected": reciprocal_cross_chain_detected,
        "topology_ambiguity_counteraxis_hit": topology_ambiguity_counteraxis_hit,
        "counterexample_candidate_review_only": counterexample_candidate,
        "counterexample_rationale": (
            "non_ePK_context_plus_terminal_phosphate_Mg_to_cross_chain_Tyr_or_N_terminal_STY_without_topology_ambiguity"
            if counterexample_candidate
            else None
        ),
        "topology_clear_cross_chain_hits": topology_clear_cross_chain_hits[:5],
        "cross_chain_substrate_mode_hits": cross_chain_hits[:8],
        "best_hits": sorted(
            local_hits,
            key=lambda row: (
                0 if row["cross_chain_substrate_mode_hit_count"] > 0 else 1,
                row["nearest_acceptors"][0]["distance_angstrom"] if row["nearest_acceptors"] else 99,
            ),
        )[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--surface-profile",
        choices=sorted(CROSS_CHAIN_QUERY_SURFACE_PROFILES),
        default="general_complex",
    )
    args = parser.parse_args()
    query_surface = CROSS_CHAIN_QUERY_SURFACE_PROFILES[args.surface_profile]

    query_results: dict[str, list[str]] = {}
    query_errors: dict[str, str] = {}
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)

    for query in query_surface:
        try:
            ids = base.rcsb_full_text_query(query["phrase"], query["rows"])
            query_results[query["name"]] = ids
        except Exception as exc:  # pragma: no cover - network evidence
            query_errors[query["name"]] = repr(exc)
            ids = []
        for pdb_id in ids:
            id_to_queries[pdb_id].append(query["name"])
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.25)

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
            row = summarize_cross_chain_entry(pdb_id, id_to_queries.get(pdb_id, []), cif_text, entry_payload)
            row["surface_order"] = index
            rows.append(row)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.15)

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
            "method": "cross_chain_non_epk_atp_mg_substrate_mode_stress",
            "surface_profile": args.surface_profile,
            "rule_under_attack": "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0",
            "candidate_threshold_angstrom": base.DISTANCE_CUTOFF_ANGSTROM,
            "mg_distance_cutoff_angstrom": base.MG_DISTANCE_CUTOFF_ANGSTROM,
            "max_n_terminal_acceptor_auth_seq_id": base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
            "query_surface": query_surface,
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
        "cross_chain_substrate_mode_hits_review_only": cross_chain_rows[:50],
        "rows": rows,
        "warnings": [
            "Review-only geometry/topology stress evidence; no production ePK scoring or label import.",
            "Candidate status is based on source-free local topology; source text is used only to exclude obvious ePK contexts during adversarial review.",
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
