#!/usr/bin/env python3
"""Metric-seeded ligand-only assembly/deposited split stress.

This helper avoids broad full-text buckets. It queries only by ATP-like ligand
component IDs, then locally filters compact coordinate metrics for deposited-v4
non-ORC/non-ePK entries with multiple polymer entities and checks whether any
declared biological assembly falls below the current v4 chain floor.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import requests

import v4_entry_level_assembly_guard_stress as split


LANE_ID = "epk_false_positive_hunter"
RCSB_SEARCH_URL = split.RCSB_SEARCH_URL

LIGAND_COMPONENT_QUERIES = [
    {"name": "atp_recent_0", "ligand": "ATP", "start": 0, "rows": 80},
    {"name": "atp_recent_80", "ligand": "ATP", "start": 80, "rows": 80},
    {"name": "atp_recent_160", "ligand": "ATP", "start": 160, "rows": 80},
    {"name": "atp_recent_240", "ligand": "ATP", "start": 240, "rows": 80},
    {"name": "atp_recent_400", "ligand": "ATP", "start": 400, "rows": 80},
    {"name": "atp_recent_640", "ligand": "ATP", "start": 640, "rows": 80},
    {"name": "anp_recent_0", "ligand": "ANP", "start": 0, "rows": 80},
    {"name": "anp_recent_80", "ligand": "ANP", "start": 80, "rows": 80},
    {"name": "anp_recent_160", "ligand": "ANP", "start": 160, "rows": 80},
    {"name": "acp_recent_0", "ligand": "ACP", "start": 0, "rows": 60},
    {"name": "acp_recent_60", "ligand": "ACP", "start": 60, "rows": 60},
    {"name": "dtp_recent_0", "ligand": "DTP", "start": 0, "rows": 60},
    {"name": "dtp_recent_60", "ligand": "DTP", "start": 60, "rows": 60},
]
DEFAULT_MAX_LOCAL_GEOMETRY_ATOM_SITE_ROWS = 120_000
DEFAULT_MAX_CONTEXT_ATOM_SITE_ROWS_BEFORE_PARSE = 160_000

DEFAULT_EXCLUDE_ARTIFACTS = [
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json",
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "v4_entry_level_assembly_guard_fetch_error_recovery_20260521_160625Z.json",
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def ligand_component_query(query: dict[str, Any]) -> list[str]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": (
                    "rcsb_nonpolymer_entity_container_identifiers."
                    "nonpolymer_comp_id"
                ),
                "operator": "exact_match",
                "value": str(query["ligand"]),
            },
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {
                "start": int(query["start"]),
                "rows": int(query["rows"]),
            },
            "results_content_type": ["experimental"],
            "sort": [
                {
                    "sort_by": "rcsb_accession_info.initial_release_date",
                    "direction": "desc",
                }
            ],
        },
    }
    response = requests.post(RCSB_SEARCH_URL, json=payload, timeout=30)
    if response.status_code == 204 or not response.text.strip():
        return []
    response.raise_for_status()
    return [
        str(row["identifier"]).upper()
        for row in response.json().get("result_set", [])
    ]


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


def reviewed_ids_from_artifact(repo_root: Path, rel_path: str) -> set[str]:
    path = repo_root / rel_path
    if not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(row.get("pdb_id") or "").upper()
        for row in payload.get("entry_review_rows", [])
        if isinstance(row, dict)
        and row.get("pdb_id")
        and row.get("reviewed") is not False
    }


def fetch_error_ids_from_artifact(repo_root: Path, rel_path: str) -> list[str]:
    path = repo_root / rel_path
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    fetch_errors = payload.get("fetch_errors") or {}
    if not isinstance(fetch_errors, dict):
        return []
    return [str(pdb_id).upper() for pdb_id in fetch_errors if pdb_id]


def collect_ids(
    repo_root: Path,
    max_unique_ids: int,
    exclude_artifacts: list[str],
    priority_pdb_ids: list[str] | None = None,
) -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int], dict[str, int]]:
    excluded: set[str] = set()
    exclude_counts: dict[str, int] = {}
    for rel_path in exclude_artifacts:
        ids = reviewed_ids_from_artifact(repo_root, rel_path)
        excluded.update(ids)
        exclude_counts[rel_path] = len(ids)

    ordered: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    for pdb_id in priority_pdb_ids or []:
        add_id(ordered, id_to_queries, pdb_id, "priority_fetch_error_retry")
        if len(ordered) >= max_unique_ids:
            return ordered, id_to_queries, {}, {}, exclude_counts

    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}
    for query in LIGAND_COMPONENT_QUERIES:
        name = str(query["name"])
        ligand = str(query["ligand"])
        try:
            ids = ligand_component_query(query)
            query_counts[name] = len(ids)
        except Exception as exc:  # pragma: no cover - network evidence
            ids = []
            query_counts[name] = 0
            query_errors[name] = repr(exc)
        for pdb_id in ids:
            if pdb_id in excluded:
                continue
            add_id(
                ordered,
                id_to_queries,
                pdb_id,
                f"metric_seeded_ligand_component:{name}:{ligand}",
            )
            if len(ordered) >= max_unique_ids:
                break
        if len(ordered) >= max_unique_ids:
            break
        time.sleep(0.12)
    return ordered[:max_unique_ids], id_to_queries, query_errors, query_counts, exclude_counts


def add_metric_surface_fields(entry_row: dict[str, Any], query_names: list[str]) -> None:
    groups = set(entry_row.get("query_surface_groups", []))
    if any(name.startswith("metric_seeded_ligand_component:") for name in query_names):
        groups.add("metric_seeded_ligand_component")
    entry_row["query_surface_groups"] = sorted(groups)
    metrics = entry_row.get("deposited_source_free_multisite_metrics") or {}
    polymer_entity_count = int(metrics.get("polymer_entity_count") or 0)
    entry_row["metric_seeded_ligand_component_surface"] = (
        "metric_seeded_ligand_component" in groups
    )
    entry_row["metric_seeded_non_orc_deposited_v4_prefilter_candidate"] = bool(
        entry_row.get("metric_seeded_ligand_component_surface")
        and entry_row.get("deposited_v4_oligomeric_atp_terminals_no_mg_required_hit")
        and polymer_entity_count > 1
        and entry_row.get("non_epk_for_counterexample_review")
        and not entry_row.get("known_orc_counterexample_input")
        and not entry_row.get("deposited_orc_mcm_role_tokens")
        and not entry_row.get("probable_epk_from_context")
    )


def estimated_atom_site_rows(cif_text: str) -> int:
    return (
        cif_text.count("\nATOM ")
        + cif_text.count("\nHETATM ")
        + int(cif_text.startswith("ATOM "))
        + int(cif_text.startswith("HETATM "))
    )


def add_local_geometry(
    context_rows: list[dict[str, Any]],
    cif_by_context: dict[str, str],
    max_atom_site_rows: int,
) -> None:
    for context_row in context_rows:
        context_name = context_row["coordinate_context"]
        if context_name not in cif_by_context:
            context_row["local_substrate_geometry"] = {
                "parse_meta": context_row.get("parse_meta", {}),
                "local_gamma_acceptor_substrate_geometry_hit_count": 0,
                "local_gamma_acceptor_substrate_geometry_topology_clear": False,
                "local_geometry_hits": [],
                "local_geometry_scan_status": context_row.get("fetch_status")
                or "skipped_no_cif_text",
            }
            context_row["local_geometry_entity_mapping_evaluations"] = []
            context_row["local_geometry_materializer_equivalent_hit_count"] = 0
            continue
        cif_text = cif_by_context[context_name]
        atom_site_rows = estimated_atom_site_rows(cif_text)
        context_row["estimated_atom_site_row_count"] = atom_site_rows
        if atom_site_rows > max_atom_site_rows:
            context_row["local_substrate_geometry"] = {
                "parse_meta": context_row.get("parse_meta", {}),
                "local_gamma_acceptor_substrate_geometry_hit_count": 0,
                "local_gamma_acceptor_substrate_geometry_topology_clear": False,
                "local_geometry_hits": [],
                "local_geometry_scan_status": "skipped_atom_site_row_cap",
                "local_geometry_atom_site_row_cap": max_atom_site_rows,
                "estimated_atom_site_row_count": atom_site_rows,
            }
            context_row["local_geometry_entity_mapping_evaluations"] = []
            context_row["local_geometry_materializer_equivalent_hit_count"] = 0
            continue
        local_geometry = split.local_substrate_geometry(cif_text)
        local_evaluations = split.local_geometry_entity_evaluations(
            cif_text,
            local_geometry,
        )
        context_row["local_substrate_geometry"] = local_geometry
        context_row["local_geometry_entity_mapping_evaluations"] = local_evaluations
        context_row["local_geometry_materializer_equivalent_hit_count"] = sum(
            1
            for evaluation in local_evaluations
            if evaluation.get("materializer_heteromeric_entity_eligible")
        )


def metric_split_context(entry: dict[str, Any], context_row: dict[str, Any]) -> bool:
    return bool(
        entry.get("metric_seeded_non_orc_deposited_v4_prefilter_candidate")
        and context_row.get("deposited_v4_context_below_chain_floor")
    )


def select_materializer_contexts(
    entry_rows: list[dict[str, Any]],
    context_rows_by_pdb: dict[str, list[dict[str, Any]]],
    max_materializer_contexts: int,
) -> list[dict[str, Any]]:
    contexts: list[dict[str, Any]] = []
    for entry in entry_rows:
        for context_row in context_rows_by_pdb.get(entry["pdb_id"], []):
            if context_row.get("deposited_v4_context_below_chain_floor"):
                contexts.append({"entry_row": entry, "context_row": context_row})
    contexts.sort(
        key=lambda selected: (
            0
            if metric_split_context(selected["entry_row"], selected["context_row"])
            and int(
                selected["context_row"].get(
                    "local_geometry_materializer_equivalent_hit_count"
                )
                or 0
            )
            > 0
            else 1,
            str(selected["entry_row"]["pdb_id"]),
            str(selected["context_row"]["coordinate_context"]),
        )
    )
    return contexts[:max_materializer_contexts]


def annotate_materializer_row(
    row: dict[str, Any],
    entry: dict[str, Any],
    context_row: dict[str, Any],
) -> None:
    local_heteromeric_count = int(
        context_row.get("local_geometry_materializer_equivalent_hit_count") or 0
    )
    metric_split = metric_split_context(entry, context_row)
    row["metric_seeded_ligand_component_surface"] = entry.get(
        "metric_seeded_ligand_component_surface"
    )
    row["metric_seeded_non_orc_deposited_v4_prefilter_candidate"] = entry.get(
        "metric_seeded_non_orc_deposited_v4_prefilter_candidate"
    )
    row[
        "metric_seeded_non_orc_deposited_v4_assembly_below_floor_candidate"
    ] = metric_split
    row[
        "metric_seeded_non_orc_deposited_v4_assembly_below_floor_heteromeric_candidate"
    ] = bool(metric_split and local_heteromeric_count > 0)
    if metric_split and local_heteromeric_count > 0:
        row["non_orc_deposited_v4_assembly_below_floor_heteromeric_candidate"] = True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-unique-ids", type=int, default=320)
    parser.add_argument("--max-materializer-contexts", type=int, default=180)
    parser.add_argument(
        "--max-local-geometry-atom-site-rows",
        type=int,
        default=DEFAULT_MAX_LOCAL_GEOMETRY_ATOM_SITE_ROWS,
    )
    parser.add_argument(
        "--max-context-atom-site-rows-before-parse",
        type=int,
        default=DEFAULT_MAX_CONTEXT_ATOM_SITE_ROWS_BEFORE_PARSE,
    )
    parser.add_argument(
        "--exclude-artifact",
        action="append",
        default=[],
        help="Artifact whose entry_review_rows should be skipped.",
    )
    parser.add_argument(
        "--priority-fetch-error-artifact",
        action="append",
        default=[],
        help="Artifact whose fetch_errors IDs should be retried before new IDs.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    exclude_artifacts = DEFAULT_EXCLUDE_ARTIFACTS + list(args.exclude_artifact)
    priority_pdb_ids: list[str] = []
    priority_fetch_error_counts: dict[str, int] = {}
    for rel_path in args.priority_fetch_error_artifact:
        ids = fetch_error_ids_from_artifact(repo_root, rel_path)
        priority_fetch_error_counts[rel_path] = len(ids)
        for pdb_id in ids:
            if pdb_id not in priority_pdb_ids:
                priority_pdb_ids.append(pdb_id)
    ordered_ids, id_to_queries, query_errors, query_counts, exclude_counts = collect_ids(
        repo_root,
        args.max_unique_ids,
        exclude_artifacts,
        priority_pdb_ids,
    )

    entry_rows: list[dict[str, Any]] = []
    context_rows_by_pdb: dict[str, list[dict[str, Any]]] = {}
    cif_text_by_pdb_context: dict[tuple[str, str], str] = {}
    fetch_errors: dict[str, str] = {}
    for index, pdb_id in enumerate(ordered_ids, start=1):
        query_names = id_to_queries.get(pdb_id, [])
        try:
            entry_row, context_rows, cif_by_context = split.fetch_entry_contexts(
                pdb_id,
                index,
                query_names,
                max_context_atom_site_rows_before_parse=(
                    args.max_context_atom_site_rows_before_parse
                ),
            )
            add_metric_surface_fields(entry_row, query_names)
            add_local_geometry(
                context_rows,
                cif_by_context,
                args.max_local_geometry_atom_site_rows,
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
            row = split.materializer_context_summary(
                repo_root,
                args.started_at,
                entry,
                context_row,
                cif_text_by_pdb_context[key],
            )
            annotate_materializer_row(row, entry, context_row)
            materializer_rows.append(row)
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

    context_rows = [row for rows in context_rows_by_pdb.values() for row in rows]
    split_context_rows = [
        row for row in context_rows if row.get("deposited_v4_context_below_chain_floor")
    ]
    metric_prefilter_rows = [
        row
        for row in entry_rows
        if row.get("metric_seeded_non_orc_deposited_v4_prefilter_candidate")
    ]
    metric_split_context_rows = [
        context_row
        for entry in entry_rows
        for context_row in context_rows_by_pdb.get(entry["pdb_id"], [])
        if metric_split_context(entry, context_row)
    ]
    metric_heteromeric_split_context_rows = [
        row
        for row in metric_split_context_rows
        if int(row.get("local_geometry_materializer_equivalent_hit_count") or 0) > 0
    ]
    preparse_skipped_entry_rows = [
        row
        for row in entry_rows
        if row.get("review_skip_status") == "skipped_atom_site_row_cap_before_parse"
    ]
    preparse_skipped_context_rows = [
        row
        for row in context_rows
        if row.get("fetch_status") == "skipped_atom_site_row_cap_before_parse"
    ]
    decision_counts = Counter(
        str(row.get("entry_level_guard_stress_decision") or "")
        for row in materializer_rows
    )
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_metric_seeded_ligand_assembly_split_stress",
            "rule_under_attack": (
                "metric-seeded deposited-v4 / biological-assembly-below-floor "
                "split traps without broad full-text bucket dependence"
            ),
            "query_surface": {
                "ligand_component_queries": LIGAND_COMPONENT_QUERIES,
                "sort": "rcsb_accession_info.initial_release_date desc",
                "exclude_artifacts": exclude_artifacts,
                "exclude_reviewed_id_counts": exclude_counts,
                "priority_fetch_error_artifacts": list(
                    args.priority_fetch_error_artifact
                ),
                "priority_fetch_error_id_counts": priority_fetch_error_counts,
                "priority_fetch_error_unique_id_count": len(priority_pdb_ids),
                "max_unique_ids": args.max_unique_ids,
                "max_assemblies_per_entry": split.MAX_ASSEMBLIES_PER_ENTRY,
                "max_materializer_contexts": args.max_materializer_contexts,
                "max_local_geometry_atom_site_rows": (
                    args.max_local_geometry_atom_site_rows
                ),
                "max_context_atom_site_rows_before_parse": (
                    args.max_context_atom_site_rows_before_parse
                ),
                "deposited_prefilter": {
                    "deposited_v4_required": True,
                    "polymer_entity_count_gt": 1,
                    "probable_epk_from_context_required": False,
                    "orc_mcm_role_tokens_required": False,
                },
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "entry_rows_reviewed": len(entry_rows),
            "entry_rows_fully_reviewed": sum(
                1 for row in entry_rows if row.get("reviewed") is not False
            ),
            "entry_rows_skipped_atom_site_row_cap_before_parse": len(
                preparse_skipped_entry_rows
            ),
            "entry_rows_skipped_atom_site_row_cap_before_parse_pdb_ids": sorted(
                row["pdb_id"] for row in preparse_skipped_entry_rows
            ),
            "coordinate_context_rows_reviewed": len(context_rows),
            "coordinate_context_rows_skipped_atom_site_row_cap_before_parse": len(
                preparse_skipped_context_rows
            ),
            "coordinate_contexts_skipped_atom_site_row_cap_before_parse": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in preparse_skipped_context_rows
            ),
            "fetch_error_count": len(fetch_errors),
            "deposited_v4_entry_count": sum(
                1
                for row in entry_rows
                if row.get("deposited_v4_oligomeric_atp_terminals_no_mg_required_hit")
            ),
            "metric_seeded_non_orc_deposited_v4_prefilter_entry_count": len(
                metric_prefilter_rows
            ),
            "metric_seeded_non_orc_deposited_v4_prefilter_pdb_ids": sorted(
                row["pdb_id"] for row in metric_prefilter_rows
            ),
            "split_context_count": len(split_context_rows),
            "split_context_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in split_context_rows
            ),
            "metric_seeded_non_orc_split_context_count": len(
                metric_split_context_rows
            ),
            "metric_seeded_non_orc_split_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in metric_split_context_rows
            ),
            "metric_seeded_non_orc_split_with_pre_materializer_heteromeric_entity_count": len(
                metric_heteromeric_split_context_rows
            ),
            "metric_seeded_non_orc_split_with_pre_materializer_heteromeric_entity_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in metric_heteromeric_split_context_rows
            ),
            "materializer_context_input_count": len(selected_contexts),
            "materializer_context_error_count": len(materializer_context_errors),
            "materializer_decision_counts": dict(sorted(decision_counts.items())),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "threshold_calibrated": False,
            "selected_threshold_angstrom": None,
            "epk_score_computed": False,
            "external_hard_negative_reaudit_scored": False,
            "raw_coordinate_files_written": False,
        },
        "fetch_errors": fetch_errors,
        "materializer_context_errors": materializer_context_errors,
        "entry_review_rows": entry_rows,
        "coordinate_context_review_rows": context_rows,
        "metric_seeded_non_orc_deposited_v4_prefilter_entry_rows": (
            metric_prefilter_rows
        ),
        "metric_seeded_non_orc_deposited_v4_assembly_below_floor_context_rows": (
            metric_split_context_rows
        ),
        "selected_materializer_context_rows": [
            {
                "pdb_id": selected["entry_row"]["pdb_id"],
                "coordinate_context": selected["context_row"]["coordinate_context"],
            }
            for selected in selected_contexts
        ],
        "entry_level_guard_materializer_rows": materializer_rows,
        "warnings": [
            "Review-only metric-seeded stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Deposited and assembly CIFs were fetched in memory only and reduced to compact metrics/materializer evidence.",
            "Ligand component queries intentionally avoid broad full-text buckets.",
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
    raise SystemExit(main())
