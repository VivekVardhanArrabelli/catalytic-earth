#!/usr/bin/env python3
"""Stress the v4 oligomeric ATP-terminal guard on no-Mg/component surfaces.

This lane helper keeps the query bounded, fetches mmCIF text in memory only,
and writes compact evidence for the current review-only ePK materializer plus
the proposed v4 source-free guard. It does not write coordinates.
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

import requests

import atpase_substrate_mode_stress as base
import auth_namespace_edge_case_stress as ns
import orc_mcm_guard_variant_sweep as variants
import orc_mcm_multisite_guard_stress as orc


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
MAX_UNIQUE_IDS = 360

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
KNOWN_ORC_COUNTEREXAMPLE_IDS = {
    "5UJ7",
    "5UJM",
    "6RQC",
    "7JGR",
    "7JGS",
    "7JK2",
    "7JK3",
    "7JK4",
    "7JPO",
    "7TJF",
    "7TJH",
    "9BCX",
    "9GJW",
}
PRESSURE_IDS = {"7CAG", "8BMS", "9L3M", "9L3U", "7ZE5"}
MANUAL_ADJUDICATION_IDS = {"9I3I"}

COMPONENT_QUERY_SURFACE = [
    {"name": "atp_component_start_0", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "atp_component_start_300", "ligand": "ATP", "start": 300, "rows": 45},
    {"name": "atp_component_start_600", "ligand": "ATP", "start": 600, "rows": 45},
    {"name": "atp_component_start_900", "ligand": "ATP", "start": 900, "rows": 45},
    {"name": "atp_component_start_1200", "ligand": "ATP", "start": 1200, "rows": 45},
    {"name": "adp_component_start_0", "ligand": "ADP", "start": 0, "rows": 45},
    {"name": "adp_component_start_300", "ligand": "ADP", "start": 300, "rows": 45},
    {"name": "adp_component_start_600", "ligand": "ADP", "start": 600, "rows": 45},
    {"name": "adp_component_start_900", "ligand": "ADP", "start": 900, "rows": 45},
    {"name": "anp_component_start_0", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "anp_component_start_150", "ligand": "ANP", "start": 150, "rows": 40},
    {"name": "anp_component_start_300", "ligand": "ANP", "start": 300, "rows": 40},
    {"name": "dtp_component_start_0", "ligand": "DTP", "start": 0, "rows": 35},
]

KINASE_DIMER_QUERIES = [
    {"name": "protein_kinase_dimer_atp", "phrase": "protein kinase dimer ATP", "rows": 35},
    {"name": "kinase_dimer_amppnp", "phrase": "kinase dimer AMPPNP", "rows": 35},
    {"name": "map_kinase_dimer_atp", "phrase": "MAP kinase dimer ATP", "rows": 35},
    {
        "name": "eukaryotic_protein_kinase_dimer_atp",
        "phrase": "eukaryotic protein kinase dimer ATP",
        "rows": 35,
    },
    {"name": "mek_erk_atp_complex", "phrase": "MEK ERK ATP complex", "rows": 35},
]

SEED_IDS = sorted(
    KNOWN_EPK_POSITIVE_IDS
    | KNOWN_ORC_COUNTEREXAMPLE_IDS
    | PRESSURE_IDS
    | MANUAL_ADJUDICATION_IDS
)


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def component_query(ligand: str, start: int, rows: int) -> list[str]:
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                "operator": "exact_match",
                "value": ligand,
            },
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


def collect_ids() -> tuple[list[str], dict[str, list[str]], dict[str, Any], dict[str, int]]:
    ordered_ids: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, Any] = {}
    query_counts: dict[str, int] = {}

    for pdb_id in reversed(SEED_IDS):
        id_to_queries[pdb_id].append("fixed_positive_counterexample_pressure_or_9i3i_seed")
        ordered_ids.insert(0, pdb_id)

    for query in KINASE_DIMER_QUERIES:
        name = str(query["name"])
        try:
            ids = base.rcsb_full_text_query(str(query["phrase"]), int(query["rows"]))
            query_counts[name] = len(ids)
        except Exception as exc:  # pragma: no cover - network evidence
            ids = []
            query_counts[name] = 0
            query_errors[name] = repr(exc)
        for pdb_id in ids:
            id_to_queries[pdb_id].append(f"{name}:{query['phrase']}")
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.15)

    for query in COMPONENT_QUERY_SURFACE:
        name = str(query["name"])
        try:
            ids = component_query(
                str(query["ligand"]),
                int(query["start"]),
                int(query["rows"]),
            )
            query_counts[name] = len(ids)
        except Exception as exc:  # pragma: no cover - network evidence
            ids = []
            query_counts[name] = 0
            query_errors[name] = repr(exc)
        for pdb_id in ids:
            id_to_queries[pdb_id].append(name)
            if pdb_id not in ordered_ids:
                ordered_ids.append(pdb_id)
        time.sleep(0.15)

    return ordered_ids[:MAX_UNIQUE_IDS], id_to_queries, query_errors, query_counts


def atom_comp(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def residue_key(atom: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        atom_comp(atom),
        str(atom.get("auth_asym_id") or atom.get("label_asym_id") or ""),
        str(atom.get("auth_seq_id") or atom.get("label_seq_id") or ""),
        str(atom.get("label_entity_id") or ""),
    )


def compact_nonpolymer_counts(atoms: list[dict[str, Any]]) -> dict[str, Any]:
    residues: Counter[str] = Counter()
    residue_keys: set[tuple[str, str, str, str]] = set()
    gamma_terminal_residues: set[tuple[str, str, str, str]] = set()
    magnesium_count = 0
    for atom in atoms:
        if atom.get("group_PDB") != "HETATM":
            continue
        comp = atom_comp(atom)
        if comp == "MG" or str(atom.get("type_symbol") or "").upper() == "MG":
            magnesium_count += 1
        key = residue_key(atom)
        if key not in residue_keys:
            residue_keys.add(key)
            residues[comp] += 1
        if (
            str(atom.get("type_symbol") or "").upper() == "P"
            and comp in orc.GAMMA_CAPABLE_CODES
            and atom_name(atom) == "PG"
        ):
            gamma_terminal_residues.add(key)
    return {
        "nonpolymer_residue_counts_selected": {
            code: residues.get(code, 0)
            for code in ["ATP", "ADP", "ANP", "ACP", "AGS", "A3P", "DTP", "MG"]
            if residues.get(code, 0)
        },
        "magnesium_atom_count": magnesium_count,
        "gamma_capable_terminal_residue_count": len(gamma_terminal_residues),
        "has_no_magnesium_atoms": magnesium_count == 0,
        "has_adp_component": residues.get("ADP", 0) > 0,
        "has_atp_component": residues.get("ATP", 0) > 0,
    }


def context_text(entry_payload: dict[str, Any], entity_descriptions: list[str]) -> str:
    keywords = entry_payload.get("struct_keywords", {}) or {}
    return " ".join(
        str(part or "")
        for part in [
            entry_payload.get("struct", {}).get("title", ""),
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
            " ".join(entity_descriptions),
        ]
    )


def manual_9i3i_adjudication(pdb_id: str, text: str, entity_descriptions: list[str]) -> dict[str, Any]:
    if pdb_id.upper() != "9I3I":
        return {}
    lower_descriptions = " ".join(entity_descriptions).lower()
    lower_text = text.lower()
    has_orc_mcm_entities = any(
        token in lower_descriptions
        for token in [
            "origin recognition complex",
            "mcm",
            "minichromosome maintenance",
            "dna replication licensing",
        ]
    )
    has_kinase_entity = any(
        token in lower_descriptions
        for token in ["protein kinase", "cyclin-dependent kinase", "cdk"]
    )
    return {
        "manual_adjudication_id": "9I3I_orc_mcm_cdk_keyword_case",
        "manual_adjudicated_non_epk": bool(has_orc_mcm_entities and not has_kinase_entity),
        "standard_context_probable_epk": orc.probable_epk(pdb_id, text),
        "adjudication_reason": (
            "Deposited title/keywords mention CDK, but polymer entity descriptions "
            "are ORC/MCM/DNA replication components and no kinase polymer entity "
            "is present."
            if has_orc_mcm_entities and not has_kinase_entity
            else "No ORC/MCM-without-kinase override applied."
        ),
        "cdk_keyword_in_deposited_text": "cdk" in lower_text,
        "entity_descriptions_support_orc_mcm": has_orc_mcm_entities,
        "entity_descriptions_support_kinase": has_kinase_entity,
    }


def substrate_mode_hit(hit: dict[str, Any]) -> bool:
    residue = str(hit.get("candidate_residue_code") or "").upper()
    seq_id = ns.optional_int(hit.get("candidate_auth_seq_id"))
    return residue == "TYR" or (
        residue in orc.ACCEPTOR_CODES
        and seq_id is not None
        and seq_id <= orc.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    )


def summarize_materializer_rows(
    materializer: dict[str, Any],
    rows_by_pdb: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    v4 = next(
        variant
        for variant in variants.VARIANTS
        if variant["guard_id"] == "v4_oligomeric_atp_terminals_no_mg_required"
    )
    for row in materializer.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        entry = rows_by_pdb.get(pdb_id, {})
        hits = [hit for hit in row.get("heteromeric_candidate_hits", []) or [] if isinstance(hit, dict)]
        substrate_hits = [hit for hit in hits if substrate_mode_hit(hit)]
        flags = orc.topology_flags(substrate_hits)
        topology_clear = bool(substrate_hits) and not flags["topology_ambiguity_counteraxis_hit"]
        known_positive = pdb_id in KNOWN_EPK_POSITIVE_IDS
        known_counterexample = pdb_id in KNOWN_ORC_COUNTEREXAMPLE_IDS
        manual_non_epk = bool(entry.get("manual_adjudicated_non_epk"))
        standard_probable_epk = bool(entry.get("probable_epk_from_context"))
        adjusted_probable_epk = standard_probable_epk and not manual_non_epk
        non_epk_for_counterexample_review = not adjusted_probable_epk
        v4_hit = variants.variant_hit(
            {
                "source_free_multisite_metrics": entry.get("source_free_multisite_metrics", {}),
            },
            v4,
        )
        if known_positive and topology_clear and v4_hit:
            decision = "known_epk_positive_lost_to_v4_review_only"
        elif known_positive and topology_clear:
            decision = "known_epk_positive_retained_by_v4_review_only"
        elif topology_clear and non_epk_for_counterexample_review and v4_hit:
            decision = "current_rule_counterexample_blocked_by_v4_review_only"
        elif topology_clear and non_epk_for_counterexample_review:
            decision = "current_rule_counterexample_residual_after_v4_review_only"
        elif substrate_hits and flags["topology_ambiguity_counteraxis_hit"]:
            decision = "substrate_mode_hit_blocked_by_existing_topology_review_only"
        elif substrate_hits:
            decision = "substrate_mode_hit_unclassified_review_only"
        else:
            decision = "no_substrate_mode_materializer_hit_review_only"
        out.append(
            {
                "pdb_id": pdb_id,
                "query_names": entry.get("query_names", []),
                "known_epk_positive_input": known_positive,
                "known_counterexample_input": known_counterexample,
                "known_pressure_id_input": pdb_id in PRESSURE_IDS,
                "manual_adjudication": entry.get("manual_adjudication", {}),
                "manual_adjudicated_non_epk": manual_non_epk,
                "standard_probable_epk_from_context": standard_probable_epk,
                "probable_epk_from_context": adjusted_probable_epk,
                "deposited_orc_mcm_role_tokens": entry.get("deposited_orc_mcm_role_tokens", []),
                "component_state": entry.get("component_state", {}),
                "candidate_status": row.get("candidate_status"),
                "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
                "substrate_mode_materializer_hit_count": len(substrate_hits),
                "topology_clear_substrate_mode_hit": topology_clear,
                **flags,
                "v4_oligomeric_atp_terminals_no_mg_required_hit": v4_hit,
                "v4_stress_decision": decision,
                "substrate_mode_materializer_hits": substrate_hits[:10],
                "source_free_multisite_metrics": entry.get("source_free_multisite_metrics", {}),
            }
        )
    return sorted(
        out,
        key=lambda item: (
            str(item.get("v4_stress_decision") or ""),
            str(item.get("pdb_id") or ""),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids()
    rows: list[dict[str, Any]] = []
    rows_by_pdb: dict[str, dict[str, Any]] = {}
    cif_text_by_pdb: dict[str, str] = {}
    fetch_errors: dict[str, str] = {}

    def fetch_review_row(pdb_id: str, index: int, *, retry: bool = False) -> dict[str, Any]:
        cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
        entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
        atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
        entity_descriptions = orc.entity_descriptions_from_cif(cif_text)
        text = context_text(entry_payload, entity_descriptions)
        manual = manual_9i3i_adjudication(pdb_id, text, entity_descriptions)
        row = {
            "pdb_id": pdb_id,
            "surface_order": index,
            "query_names": id_to_queries.get(pdb_id, []),
            "title": entry_payload.get("struct", {}).get("title", ""),
            "keywords": entry_payload.get("struct_keywords", {}),
            "entity_descriptions_compact": entity_descriptions[:14],
            "known_epk_positive_input": pdb_id in KNOWN_EPK_POSITIVE_IDS,
            "known_counterexample_input": pdb_id in KNOWN_ORC_COUNTEREXAMPLE_IDS,
            "known_pressure_id_input": pdb_id in PRESSURE_IDS,
            "manual_adjudication": manual,
            "manual_adjudicated_non_epk": bool(manual.get("manual_adjudicated_non_epk")),
            "probable_epk_from_context": orc.probable_epk(pdb_id, text),
            "deposited_orc_mcm_role_tokens": orc.deposited_role_tokens(text),
            "reviewed": True,
            "retry_fetch_after_initial_error": retry,
            **parse_meta,
            "component_state": compact_nonpolymer_counts(atoms),
            "source_free_multisite_metrics": orc.source_free_multisite_metrics(atoms),
        }
        rows.append(row)
        rows_by_pdb[pdb_id] = row
        cif_text_by_pdb[pdb_id] = cif_text
        return row

    surface_order_by_pdb = {pdb_id: index for index, pdb_id in enumerate(ordered_ids, start=1)}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            fetch_review_row(pdb_id, index)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.06)

    initial_fetch_errors = dict(fetch_errors)
    if initial_fetch_errors:
        time.sleep(1.0)
    for pdb_id in sorted(initial_fetch_errors):
        if pdb_id in rows_by_pdb:
            fetch_errors.pop(pdb_id, None)
            continue
        try:
            fetch_review_row(
                pdb_id,
                surface_order_by_pdb.get(pdb_id, len(rows) + 1),
                retry=True,
            )
            fetch_errors.pop(pdb_id, None)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.06)

    materializer = ns.materializer_probe(
        repo_root=Path(args.repo_root).resolve(),
        started_at=args.started_at,
        pressure_ids=[row["pdb_id"] for row in rows],
        cif_text_by_pdb=cif_text_by_pdb,
    )
    materializer_rows = summarize_materializer_rows(materializer, rows_by_pdb)
    decision_counts = Counter(str(row.get("v4_stress_decision") or "") for row in materializer_rows)
    current_counterexamples = [
        row
        for row in materializer_rows
        if row.get("v4_stress_decision")
        in {
            "current_rule_counterexample_blocked_by_v4_review_only",
            "current_rule_counterexample_residual_after_v4_review_only",
        }
        and not row.get("known_counterexample_input")
    ]
    residual_after_v4 = [
        row
        for row in materializer_rows
        if row.get("v4_stress_decision")
        == "current_rule_counterexample_residual_after_v4_review_only"
    ]
    blocked_by_v4 = [
        row
        for row in materializer_rows
        if row.get("v4_stress_decision")
        == "current_rule_counterexample_blocked_by_v4_review_only"
    ]
    known_positive_lost = [
        row
        for row in materializer_rows
        if row.get("v4_stress_decision") == "known_epk_positive_lost_to_v4_review_only"
    ]
    no_mg_reviewed = [
        row
        for row in rows
        if row.get("component_state", {}).get("has_no_magnesium_atoms")
    ]
    adp_reviewed = [
        row for row in rows if row.get("component_state", {}).get("has_adp_component")
    ]
    manual_adjudications = [
        row for row in materializer_rows if row.get("manual_adjudication")
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_component_no_mg_kinase_dimer_stress",
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0 "
                "and build_epk_heteromeric_positive_coverage_candidate_scout"
            ),
            "guard_under_test": "v4_oligomeric_atp_terminals_no_mg_required",
            "query_surface": {
                "component_queries": COMPONENT_QUERY_SURFACE,
                "kinase_dimer_queries": KINASE_DIMER_QUERIES,
                "seed_ids": SEED_IDS,
                "max_unique_ids": MAX_UNIQUE_IDS,
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "rows_reviewed": len(rows),
            "initial_fetch_error_count": len(initial_fetch_errors),
            "retry_fetch_success_count": len(initial_fetch_errors) - len(fetch_errors),
            "fetch_error_count": len(fetch_errors),
            "no_mg_structure_count": len(no_mg_reviewed),
            "adp_component_structure_count": len(adp_reviewed),
            "actual_materializer_input_count": len(rows),
            "actual_materializer_candidate_status_counts": materializer.get("metadata", {}).get(
                "candidate_status_counts", {}
            ),
            "v4_decision_counts": dict(sorted(decision_counts.items())),
            "current_rule_counterexample_count": len(current_counterexamples),
            "current_rule_counterexample_pdb_ids": sorted(
                {str(row["pdb_id"]) for row in current_counterexamples}
            ),
            "current_rule_counterexample_residual_after_v4_count": len(residual_after_v4),
            "current_rule_counterexample_residual_after_v4_pdb_ids": sorted(
                {str(row["pdb_id"]) for row in residual_after_v4}
            ),
            "current_rule_counterexample_blocked_by_v4_count": len(blocked_by_v4),
            "current_rule_counterexample_blocked_by_v4_pdb_ids": sorted(
                {str(row["pdb_id"]) for row in blocked_by_v4}
            ),
            "known_epk_positive_lost_to_v4_count": len(known_positive_lost),
            "known_epk_positive_lost_to_v4_pdb_ids": sorted(
                {str(row["pdb_id"]) for row in known_positive_lost}
            ),
            "manual_adjudication_ids": [row["pdb_id"] for row in manual_adjudications],
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
        "current_rule_counterexamples_review_only": current_counterexamples,
        "current_rule_counterexamples_residual_after_v4_review_only": residual_after_v4,
        "known_epk_positives_lost_to_v4_review_only": known_positive_lost,
        "manual_adjudications": manual_adjudications,
        "warnings": [
            "Review-only bounded stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Component surfaces are ligand-component samples and are not exhaustive PDB evidence.",
            "9I3I adjudication uses deposited title/entity context only to classify the adversarial review row; it is not a source-free production feature.",
            "No raw coordinate files are written; mmCIF text is reduced in memory to compact metrics and materializer hits.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
