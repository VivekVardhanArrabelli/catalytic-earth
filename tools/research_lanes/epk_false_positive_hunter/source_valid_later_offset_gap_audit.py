#!/usr/bin/env python3
"""Audit local-geometry/materializer gaps and later-offset ePK seeds.

This helper keeps the false-positive hunter lane in review-only mode. It
materializes compact rows for the 8OOZ/9OFD/9OFE/9W1G local-geometry gap and
then expands later-offset source-valid ePK entity seed searches. It writes no
raw coordinates and does not edit production labels, registries, fingerprints,
thresholds, migrations, or scoring.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import auth_namespace_edge_case_stress as ns
import source_valid_epk_seed_geometry_prefilter_stress as prior_seed
import v4_entry_level_assembly_guard_stress as entry_guard


LANE_ID = "epk_false_positive_hunter"
GAP_AUDIT_IDS = ["8OOZ", "9OFD", "9OFE", "9W1G"]
PRIOR_SOURCE_VALID_ARTIFACT = Path(
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json"
)
REGRESSION_GATE_PATH = Path(
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "epk_candidate_evidence_v1_regression_gate_20260521_051511Z.json"
)

LATER_OFFSET_EPK_SEED_QUERIES = [
    {"name": "cdk_cyclin_atp_start_45", "phrase": "CDK cyclin", "ligand": "ATP", "start": 45, "rows": 45},
    {"name": "cdk_cyclin_atp_start_90", "phrase": "CDK cyclin", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "cdk_cyclin_anp_start_45", "phrase": "CDK cyclin", "ligand": "ANP", "start": 45, "rows": 45},
    {"name": "cyclin_dependent_kinase_cyclin_atp_start_45", "phrase": "cyclin-dependent kinase cyclin", "ligand": "ATP", "start": 45, "rows": 45},
    {"name": "cyclin_dependent_kinase_cyclin_atp_start_90", "phrase": "cyclin-dependent kinase cyclin", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "cyclin_dependent_kinase_cyclin_anp_start_45", "phrase": "cyclin-dependent kinase cyclin", "ligand": "ANP", "start": 45, "rows": 45},
    {"name": "jnk_kinase_atp_start_40", "phrase": "JNK kinase", "ligand": "ATP", "start": 40, "rows": 40},
    {"name": "jnk_kinase_atp_start_80", "phrase": "JNK kinase", "ligand": "ATP", "start": 80, "rows": 40},
    {"name": "jnk_kinase_anp_start_40", "phrase": "JNK kinase", "ligand": "ANP", "start": 40, "rows": 40},
    {"name": "c_jun_n_terminal_kinase_atp_start_35", "phrase": "c-Jun N-terminal kinase", "ligand": "ATP", "start": 35, "rows": 35},
    {"name": "c_jun_n_terminal_kinase_anp_start_0", "phrase": "c-Jun N-terminal kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "receptor_tyrosine_kinase_dimer_atp_start_45", "phrase": "receptor tyrosine kinase dimer", "ligand": "ATP", "start": 45, "rows": 45},
    {"name": "receptor_tyrosine_kinase_dimer_atp_start_90", "phrase": "receptor tyrosine kinase dimer", "ligand": "ATP", "start": 90, "rows": 45},
    {"name": "receptor_tyrosine_kinase_dimer_anp_start_45", "phrase": "receptor tyrosine kinase dimer", "ligand": "ANP", "start": 45, "rows": 45},
    {"name": "egfr_kinase_dimer_atp_start_0", "phrase": "EGFR kinase dimer", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "egfr_kinase_dimer_anp_start_0", "phrase": "EGFR kinase dimer", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "insulin_receptor_kinase_atp_start_35", "phrase": "insulin receptor kinase", "ligand": "ATP", "start": 35, "rows": 35},
    {"name": "insulin_receptor_kinase_atp_start_70", "phrase": "insulin receptor kinase", "ligand": "ATP", "start": 70, "rows": 35},
    {"name": "insulin_receptor_kinase_anp_start_35", "phrase": "insulin receptor kinase", "ligand": "ANP", "start": 35, "rows": 35},
    {"name": "mtor_kinase_atp_start_35", "phrase": "mTOR kinase", "ligand": "ATP", "start": 35, "rows": 35},
    {"name": "mtor_kinase_anp_start_35", "phrase": "mTOR kinase", "ligand": "ANP", "start": 35, "rows": 35},
    {"name": "mtorc1_atp_start_35", "phrase": "mTORC1", "ligand": "ATP", "start": 35, "rows": 35},
    {"name": "mtorc1_anp_start_0", "phrase": "mTORC1", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mtorc2_atp_start_35", "phrase": "mTORC2", "ligand": "ATP", "start": 35, "rows": 35},
    {"name": "mtorc2_anp_start_0", "phrase": "mTORC2", "ligand": "ANP", "start": 0, "rows": 35},
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


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


def prior_gap_contexts(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / PRIOR_SOURCE_VALID_ARTIFACT
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    wanted = set(GAP_AUDIT_IDS)
    for row in payload.get("custom_materializer_rows", []) or []:
        if str(row.get("pdb_id") or "").upper() in wanted:
            rows.append(
                {
                    "pdb_id": str(row.get("pdb_id") or "").upper(),
                    "coordinate_context": str(
                        row.get("coordinate_context") or "deposited_atom_site"
                    ),
                    "prior_candidate_status": row.get("candidate_status"),
                    "prior_decision": row.get(
                        "source_valid_geometry_prefilter_stress_decision"
                    ),
                }
            )
    return rows


def collect_later_offset_ids(
    *,
    max_unique_ids: int,
) -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    ordered: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}
    for query in LATER_OFFSET_EPK_SEED_QUERIES:
        name = str(query["name"])
        try:
            ids = entry_guard.component_full_text_query(query)
            query_counts[name] = len(ids)
        except Exception as exc:  # pragma: no cover - network evidence
            ids = []
            query_counts[name] = 0
            query_errors[name] = repr(exc)
        for pdb_id in ids:
            add_id(
                ordered,
                id_to_queries,
                pdb_id,
                (
                    "epk_entity_seed_text:"
                    f"{name}:{query['phrase']}:{query['ligand']}:"
                    f"start_{query['start']}"
                ),
            )
        time.sleep(0.12)
    return ordered[:max_unique_ids], id_to_queries, query_errors, query_counts


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


def entity_gap_evaluations(
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
        same_entity = bool(acceptor_entity and gamma_entity and acceptor_entity == gamma_entity)
        reject_reasons = []
        if same_chain:
            reject_reasons.append("same_author_chain_topology")
        if same_entity:
            reject_reasons.append("acceptor_entity_equals_gamma_associated_polymer_entity")
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


def annotate_later_offset_entry(
    entry: dict[str, Any],
    context_rows: list[dict[str, Any]],
    deposited_cif: str,
) -> dict[str, Any]:
    annotated = prior_seed.annotate_entry(entry, context_rows, deposited_cif)
    family_buckets = annotated.get("source_valid_epk_seed_family_buckets", [])
    any_context_v4 = bool(
        annotated.get("entry_level_any_context_v4_guard_hit_review_only")
        or any(
            row.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
            for row in context_rows
        )
    )
    later_offset_seed = bool(family_buckets and any_context_v4)
    annotated["source_valid_later_offset_entity_seed_review_candidate"] = (
        later_offset_seed
    )
    annotated["source_valid_later_offset_entity_seed_basis"] = (
        "polymer_entity_family_bucket_and_deposited_or_assembly_v4"
        if later_offset_seed
        else "not_source_valid_v4_seed_on_this_surface"
    )
    if later_offset_seed:
        annotated["source_valid_epk_seed_review_candidate"] = True
    return annotated


def context_selection_priority(selected: dict[str, Any]) -> tuple[int, str, str]:
    entry = selected["entry_row"]
    context = selected["context_row"]
    if entry.get("gap_audit_control"):
        priority = 0 if context["coordinate_context"] == "deposited_atom_site" else 1
    elif entry.get("source_valid_later_offset_entity_seed_review_candidate"):
        priority = 2 if context.get("v4_oligomeric_atp_terminals_no_mg_required_hit") else 3
    else:
        priority = 4
    return priority, str(entry["pdb_id"]), str(context["coordinate_context"])


def select_materializer_contexts(
    entry_rows: list[dict[str, Any]],
    context_rows_by_pdb: dict[str, list[dict[str, Any]]],
    *,
    max_materializer_contexts: int,
) -> list[dict[str, Any]]:
    selected = []
    for entry in entry_rows:
        contexts = context_rows_by_pdb.get(entry["pdb_id"], [])
        if entry.get("gap_audit_control"):
            for context in contexts:
                if context["coordinate_context"] in {
                    "deposited_atom_site",
                    "biological_assembly_1",
                }:
                    selected.append({"entry_row": entry, "context_row": context})
            continue
        if entry.get("source_valid_later_offset_entity_seed_review_candidate"):
            for context in contexts:
                selected.append({"entry_row": entry, "context_row": context})

    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for row in selected:
        key = (row["entry_row"]["pdb_id"], row["context_row"]["coordinate_context"])
        unique.setdefault(key, row)
    return sorted(unique.values(), key=context_selection_priority)[:max_materializer_contexts]


def materializer_row(
    repo_root: Path,
    started_at: str,
    entry: dict[str, Any],
    context_row: dict[str, Any],
    cif_text: str,
    gate_lookup: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    row = prior_seed.materializer_decision(
        repo_root,
        started_at,
        entry,
        context_row,
        cif_text,
        gate_lookup,
    )
    row["source_valid_later_offset_entity_seed_review_candidate"] = bool(
        entry.get("source_valid_later_offset_entity_seed_review_candidate")
    )
    row["source_valid_later_offset_entity_seed_basis"] = entry.get(
        "source_valid_later_offset_entity_seed_basis"
    )
    row["gap_audit_control"] = bool(entry.get("gap_audit_control"))
    if entry.get("gap_audit_control"):
        local_geometry = context_row.get("local_substrate_geometry", {})
        evaluations = entity_gap_evaluations(cif_text, local_geometry)
        same_chain = bool(
            local_geometry.get("local_same_chain_topology_detected")
            or any(item.get("same_author_chain_topology") for item in evaluations)
        )
        reciprocal = bool(
            local_geometry.get("local_reciprocal_cross_chain_topology_detected")
        )
        heteromeric_eligible = any(
            item.get("materializer_heteromeric_entity_eligible")
            for item in evaluations
        )
        row.update(
            {
                "non_epk_v4_contaminant_prefilter_candidate": True,
                "same_chain_topology_detected": same_chain,
                "reciprocal_cross_chain_topology_detected": reciprocal,
                "topology_ambiguity_counteraxis_hit": bool(same_chain or reciprocal),
                "materializer_equivalence_gap_audit": True,
                "local_geometry_entity_mapping_evaluations": evaluations,
                "local_geometry_materializer_equivalent_hit_count": sum(
                    1
                    for item in evaluations
                    if item.get("materializer_heteromeric_entity_eligible")
                ),
                "gap_audit_decision": (
                    "local_geometry_same_chain_same_entity_explains_materializer_abstention"
                    if evaluations and not heteromeric_eligible
                    else "local_geometry_has_heteromeric_entity_candidate_needs_review"
                ),
            }
        )
    return row


def compact_ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(row["pdb_id"]) for row in rows if row.get(key))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-unique-ids", type=int, default=320)
    parser.add_argument("--max-materializer-contexts", type=int, default=220)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    later_ids, id_to_queries, query_errors, query_counts = collect_later_offset_ids(
        max_unique_ids=args.max_unique_ids,
    )
    ordered_ids: list[str] = []
    for pdb_id in GAP_AUDIT_IDS:
        add_id(ordered_ids, id_to_queries, pdb_id, "fixed_gap_audit_control")
    for pdb_id in later_ids:
        add_id(ordered_ids, id_to_queries, pdb_id, "selected_later_offset_epk_seed_surface")

    gate_lookup = prior_seed.load_regression_gate(repo_root)
    entry_rows: list[dict[str, Any]] = []
    context_rows_by_pdb: dict[str, list[dict[str, Any]]] = {}
    cif_text_by_pdb_context: dict[tuple[str, str], str] = {}
    fetch_errors: dict[str, str] = {}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            entry, contexts, cif_by_context = entry_guard.fetch_entry_contexts(
                pdb_id,
                index,
                id_to_queries.get(pdb_id, []),
            )
            for context in contexts:
                cif_text = cif_by_context[context["coordinate_context"]]
                context["local_substrate_geometry"] = prior_seed.local_substrate_geometry(
                    cif_text
                )
                context["regression_gate_fixture_joined"] = bool(
                    gate_lookup.get((pdb_id, context["coordinate_context"]))
                )
            annotated = annotate_later_offset_entry(
                entry,
                contexts,
                cif_by_context["deposited_atom_site"],
            )
            if pdb_id in GAP_AUDIT_IDS:
                annotated.update(
                    {
                        "gap_audit_control": True,
                        "source_valid_epk_seed_review_candidate": False,
                        "source_valid_later_offset_entity_seed_review_candidate": False,
                        "non_epk_v4_contaminant_prefilter_candidate": True,
                    }
                )
            entry_rows.append(annotated)
            context_rows_by_pdb[pdb_id] = contexts
            for context_name, cif_text in cif_by_context.items():
                cif_text_by_pdb_context[(pdb_id, context_name)] = cif_text
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
        max_materializer_contexts=args.max_materializer_contexts,
    )
    materializer_rows: list[dict[str, Any]] = []
    materializer_context_errors: dict[str, str] = {}
    for index, selected in enumerate(selected_contexts, start=1):
        entry = selected["entry_row"]
        context = selected["context_row"]
        key = (entry["pdb_id"], context["coordinate_context"])
        try:
            materializer_rows.append(
                materializer_row(
                    repo_root,
                    args.started_at,
                    entry,
                    context,
                    cif_text_by_pdb_context[key],
                    gate_lookup,
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

    context_rows = [row for rows in context_rows_by_pdb.values() for row in rows]
    later_seed_rows = [
        row
        for row in entry_rows
        if row.get("source_valid_later_offset_entity_seed_review_candidate")
    ]
    later_seed_v4_rows = [
        row
        for row in later_seed_rows
        if row.get("entry_level_any_context_v4_guard_hit_review_only")
    ]
    gap_rows = [row for row in materializer_rows if row.get("gap_audit_control")]
    gap_unexplained = [
        row
        for row in gap_rows
        if row.get("gap_audit_decision")
        == "local_geometry_has_heteromeric_entity_candidate_needs_review"
    ]
    overblock_rows = [
        row
        for row in materializer_rows
        if row.get("source_valid_geometry_prefilter_stress_decision")
        == "source_valid_epk_seed_overblock_risk_by_entry_level_guard_review_only"
    ]
    residual_rows = [
        row
        for row in materializer_rows
        if row.get("unsafe_nonabstention_after_expected_policy")
    ]
    decision_counts = Counter(
        str(
            row.get("gap_audit_decision")
            or row.get("source_valid_geometry_prefilter_stress_decision")
            or row.get("entry_level_guard_stress_decision")
            or ""
        )
        for row in materializer_rows
    )
    source_family_counts = Counter(
        bucket
        for row in later_seed_rows
        for bucket in row.get("source_valid_epk_seed_family_buckets", []) or []
    )
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "source_valid_later_offset_gap_audit",
            "rule_under_attack": (
                "materializer equivalence on local geometry prefilters plus "
                "later-offset source-valid ePK entity v4 seed coverage"
            ),
            "query_surface": {
                "gap_audit_ids": GAP_AUDIT_IDS,
                "later_offset_epk_seed_queries": LATER_OFFSET_EPK_SEED_QUERIES,
                "max_unique_ids": args.max_unique_ids,
                "max_materializer_contexts": args.max_materializer_contexts,
                "prior_source_valid_artifact": str(PRIOR_SOURCE_VALID_ARTIFACT),
                "regression_gate_artifact": str(REGRESSION_GATE_PATH),
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "entry_rows_reviewed": len(entry_rows),
            "coordinate_context_rows_reviewed": len(context_rows),
            "fetch_error_count": len(fetch_errors),
            "gap_audit_context_count": len(gap_rows),
            "gap_audit_unexplained_context_count": len(gap_unexplained),
            "gap_audit_unexplained_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in gap_unexplained
            ),
            "source_valid_later_offset_seed_entry_count": len(later_seed_rows),
            "source_valid_later_offset_seed_pdb_ids": compact_ids(
                later_seed_rows,
                "source_valid_later_offset_entity_seed_review_candidate",
            ),
            "source_valid_later_offset_v4_seed_entry_count": len(later_seed_v4_rows),
            "source_valid_later_offset_v4_seed_pdb_ids": compact_ids(
                later_seed_v4_rows,
                "entry_level_any_context_v4_guard_hit_review_only",
            ),
            "source_valid_later_offset_v4_seed_beyond_9lgo_count": len(
                [row for row in later_seed_v4_rows if row["pdb_id"] != "9LGO"]
            ),
            "source_valid_later_offset_family_bucket_counts": dict(
                sorted(source_family_counts.items())
            ),
            "materializer_context_input_count": len(selected_contexts),
            "materializer_context_error_count": len(materializer_context_errors),
            "source_valid_epk_entry_level_overblock_risk_count": len(overblock_rows),
            "source_valid_epk_entry_level_overblock_risk_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in overblock_rows
            ),
            "unsafe_nonabstention_count": len(residual_rows),
            "unsafe_nonabstention_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in residual_rows
            ),
            "custom_stress_decision_counts": dict(sorted(decision_counts.items())),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "epk_score_computed": False,
            "external_hard_negative_reaudit_scored": False,
        },
        "fetch_errors": fetch_errors,
        "materializer_context_errors": materializer_context_errors,
        "prior_gap_contexts": prior_gap_contexts(repo_root),
        "entry_review_rows": entry_rows,
        "coordinate_context_review_rows": context_rows,
        "selected_materializer_context_rows": [
            {
                "pdb_id": selected["entry_row"]["pdb_id"],
                "coordinate_context": selected["context_row"]["coordinate_context"],
                "context_priority": context_selection_priority(selected)[0],
            }
            for selected in selected_contexts
        ],
        "custom_materializer_rows": materializer_rows,
        "gap_audit_rows": gap_rows,
        "source_valid_later_offset_seed_rows": later_seed_rows,
        "source_valid_later_offset_v4_seed_rows": later_seed_v4_rows,
        "source_valid_epk_entry_level_overblock_risk_rows": overblock_rows,
        "unsafe_nonabstention_rows": residual_rows,
        "warnings": [
            "Review-only lane artifact; no production labels, thresholds, registries, fingerprints, migrations, or scoring.",
            "Source-valid seed status is based on compact polymer/entity family buckets plus deposited-or-assembly v4 context.",
            "Gap audit compares local gamma-to-acceptor geometry with the materializer's heteromeric entity mapping.",
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
