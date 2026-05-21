#!/usr/bin/env python3
"""Check whether biological assemblies split fixed v4 controls.

The stress is intentionally small: prior known ePK positives plus prior
ORC/OCCM/MCM counterexamples, deposited coordinates, and the first few
biological assemblies declared by RCSB. It writes compact decisions only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import atpase_substrate_mode_stress as base
import auth_namespace_edge_case_stress as ns
import orc_mcm_multisite_guard_stress as orc
import v4_component_no_mg_kinase_dimer_stress as prior
import v4_high_order_epk_atpase_overblock_stress as high_order


LANE_ID = "epk_false_positive_hunter"
RCSB_ASSEMBLY_CIF_URL = "https://files.rcsb.org/download/{pdb_id}-assembly{assembly_id}.cif"
MAX_ASSEMBLIES_PER_ENTRY = 6


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "gamma_capable_terminal_p_count": metrics.get("gamma_capable_terminal_p_count"),
        "gamma_capable_terminal_p_near_mg_count": metrics.get(
            "gamma_capable_terminal_p_near_mg_count"
        ),
        "gamma_capable_terminal_p_near_mg_chain_count": metrics.get(
            "gamma_capable_terminal_p_near_mg_chain_count"
        ),
        "gamma_capable_terminal_p_near_mg_entity_count": metrics.get(
            "gamma_capable_terminal_p_near_mg_entity_count"
        ),
        "gamma_capable_terminal_p_near_mg_ligand_counts": metrics.get(
            "gamma_capable_terminal_p_near_mg_ligand_counts", {}
        ),
        "polymer_chain_count": metrics.get("polymer_chain_count"),
        "polymer_entity_count": metrics.get("polymer_entity_count"),
        "compact_gamma_mg_sites": metrics.get("compact_gamma_mg_sites", [])[:12],
    }


def limited_assembly_ids(entry_payload: dict[str, Any]) -> list[str]:
    ids = (
        entry_payload.get("rcsb_entry_container_identifiers", {}).get("assembly_ids")
        or ["1"]
    )
    normalized = [str(value) for value in ids if str(value)]
    return normalized[:MAX_ASSEMBLIES_PER_ENTRY] or ["1"]


def materializer_decision(
    repo_root: Path,
    started_at: str,
    pdb_id: str,
    cif_text: str,
    guard_hit: bool,
    known_positive: bool,
    known_counterexample: bool,
) -> dict[str, Any]:
    materializer = ns.materializer_probe(
        repo_root=repo_root,
        started_at=started_at,
        pressure_ids=[pdb_id],
        cif_text_by_pdb={pdb_id: cif_text},
    )
    row = (materializer.get("rows") or [{}])[0]
    hits = [
        hit
        for hit in row.get("heteromeric_candidate_hits", []) or []
        if isinstance(hit, dict)
    ]
    substrate_hits = [hit for hit in hits if prior.substrate_mode_hit(hit)]
    flags = orc.topology_flags(substrate_hits)
    topology_clear = bool(substrate_hits) and not flags["topology_ambiguity_counteraxis_hit"]

    if known_positive and topology_clear and guard_hit:
        decision = "known_epk_positive_lost_to_v4_review_only"
    elif known_positive and topology_clear:
        decision = "known_epk_positive_retained_review_only"
    elif known_counterexample and topology_clear and guard_hit:
        decision = "known_orc_counterexample_blocked_by_v4_review_only"
    elif known_counterexample and topology_clear:
        decision = "known_orc_counterexample_residual_after_v4_review_only"
    elif topology_clear and guard_hit:
        decision = "topology_clear_hit_blocked_by_v4_review_only"
    elif topology_clear:
        decision = "topology_clear_hit_residual_after_v4_review_only"
    elif substrate_hits and flags["topology_ambiguity_counteraxis_hit"]:
        decision = "substrate_mode_hit_blocked_by_existing_topology_review_only"
    elif substrate_hits:
        decision = "substrate_mode_hit_unclassified_review_only"
    else:
        decision = "no_substrate_mode_materializer_hit_review_only"

    return {
        "actual_materializer_candidate_status": row.get("candidate_status"),
        "heteromeric_candidate_hit_count": row.get("heteromeric_candidate_hit_count"),
        "substrate_mode_materializer_hit_count": len(substrate_hits),
        "topology_clear_substrate_mode_hit": topology_clear,
        **flags,
        "v4_control_split_decision": decision,
        "substrate_mode_materializer_hits": substrate_hits[:8],
    }


def review_coordinate_context(
    repo_root: Path,
    started_at: str,
    pdb_id: str,
    coord_context: str,
    cif_text: str,
    known_positive: bool,
    known_counterexample: bool,
) -> dict[str, Any]:
    atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
    metrics = orc.source_free_multisite_metrics(atoms)
    guard_hit = high_order.v4_hit(metrics)
    decision = materializer_decision(
        repo_root,
        started_at,
        pdb_id,
        cif_text,
        guard_hit,
        known_positive,
        known_counterexample,
    )
    return {
        "pdb_id": pdb_id,
        "coordinate_context": coord_context,
        "known_epk_positive_input": known_positive,
        "known_orc_counterexample_input": known_counterexample,
        "parse_meta": parse_meta,
        "source_free_multisite_metrics": compact_metrics(metrics),
        "v4_oligomeric_atp_terminals_no_mg_required_hit": guard_hit,
        **decision,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--pdb-ids",
        nargs="*",
        default=None,
        help="Optional fixed-control subset to retry.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    fixed_control_ids = (
        high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
        | high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
    )
    if args.pdb_ids:
        pdb_ids = sorted({str(pdb_id).upper() for pdb_id in args.pdb_ids})
    else:
        pdb_ids = sorted(fixed_control_ids)
    rows: list[dict[str, Any]] = []
    fetch_errors: dict[str, str] = {}
    entry_contexts: dict[str, list[str]] = {}

    for pdb_id in pdb_ids:
        known_positive = pdb_id in high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
        known_counterexample = pdb_id in high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
        try:
            entry_payload = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            deposited_cif = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
            rows.append(
                review_coordinate_context(
                    repo_root,
                    args.started_at,
                    pdb_id,
                    "deposited_atom_site",
                    deposited_cif,
                    known_positive,
                    known_counterexample,
                )
            )
            entry_contexts[pdb_id] = ["deposited_atom_site"]
            for assembly_id in limited_assembly_ids(entry_payload):
                context = f"biological_assembly_{assembly_id}"
                try:
                    assembly_cif = base.fetch_text(
                        RCSB_ASSEMBLY_CIF_URL.format(
                            pdb_id=pdb_id,
                            assembly_id=assembly_id,
                        )
                    )
                    rows.append(
                        review_coordinate_context(
                            repo_root,
                            args.started_at,
                            pdb_id,
                            context,
                            assembly_cif,
                            known_positive,
                            known_counterexample,
                        )
                    )
                    entry_contexts[pdb_id].append(context)
                except Exception as exc:  # pragma: no cover - network evidence
                    fetch_errors[f"{pdb_id}:{context}"] = repr(exc)
                time.sleep(0.05)
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[f"{pdb_id}:entry_or_deposited"] = repr(exc)
        print(
            json.dumps(
                {
                    "progress_pdb_id": pdb_id,
                    "progress_rows": len(rows),
                    "progress_fetch_errors": len(fetch_errors),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        time.sleep(0.08)

    decision_counts = Counter(row["v4_control_split_decision"] for row in rows)
    residual_rows = [
        row
        for row in rows
        if row["v4_control_split_decision"]
        in {
            "known_orc_counterexample_residual_after_v4_review_only",
            "topology_clear_hit_residual_after_v4_review_only",
        }
    ]
    assembly_residual_rows = [
        row
        for row in residual_rows
        if str(row.get("coordinate_context") or "").startswith("biological_assembly_")
    ]
    known_positive_lost_rows = [
        row
        for row in rows
        if row["v4_control_split_decision"] == "known_epk_positive_lost_to_v4_review_only"
    ]

    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "method": "v4_assembly_control_split_stress",
            "rule_under_attack": (
                "v4_oligomeric_atp_terminals_no_mg_required review guard candidate "
                "under deposited atom_site versus biological assembly coordinate contexts"
            ),
            "guard_under_test": "v4_oligomeric_atp_terminals_no_mg_required",
            "fixed_known_epk_positive_count": len(high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS),
            "fixed_orc_counterexample_count": len(high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS),
            "fixed_control_pdb_ids": pdb_ids,
            "max_assemblies_per_entry": MAX_ASSEMBLIES_PER_ENTRY,
            "rows_reviewed": len(rows),
            "entry_contexts": entry_contexts,
            "fetch_error_count": len(fetch_errors),
            "v4_control_split_decision_counts": dict(sorted(decision_counts.items())),
            "residual_context_count": len(residual_rows),
            "residual_context_pdb_ids": sorted({row["pdb_id"] for row in residual_rows}),
            "assembly_residual_context_count": len(assembly_residual_rows),
            "assembly_residual_context_pdb_ids": sorted(
                {row["pdb_id"] for row in assembly_residual_rows}
            ),
            "known_epk_positive_lost_context_count": len(known_positive_lost_rows),
            "known_epk_positive_lost_context_pdb_ids": sorted(
                {row["pdb_id"] for row in known_positive_lost_rows}
            ),
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
        "rows": rows,
        "residual_context_rows": residual_rows,
        "assembly_residual_context_rows": assembly_residual_rows,
        "known_epk_positive_lost_rows": known_positive_lost_rows,
        "warnings": [
            "Review-only fixed-control stress; no production scoring, labels, thresholds, registries, fingerprints, or migrations.",
            "Assembly CIFs were fetched in memory and reduced to compact metrics and materializer-hit summaries.",
            "Coordinate-context decisions are research evidence only and are not production scoring.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
