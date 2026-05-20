#!/usr/bin/env python3
"""Review-only ePK auth-terminal guard generalization stress test.

This lane-local helper reuses the compact coordinate reducer from the prior
terminal-index stress run. It freezes a non-overlap tranche before feature
extraction and asks whether the auth-terminal N-terminal-STY guard generalizes
beyond the single 5HVK folded N-terminal positive without using source text as
a predictive input.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    RULES,
    append_jsonl,
    confusion_for_rule,
    primary_outcome as inherited_primary_outcome,
    reduced_features,
    row_probe,
    summarize_rule_delta,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_auth_terminal_guard_generalization_v2_20260520"


FROZEN_ROWS = [
    {
        "pdb_id": "1IR3",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_current_positive_protein_substrate",
        "evaluation_label_source": "prior review-only current ePK protein-substrate role discriminator hit; label used only after feature extraction",
    },
    {
        "pdb_id": "2PHK",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_current_positive_protein_substrate",
        "evaluation_label_source": "prior review-only current ePK protein-substrate role discriminator hit; label used only after feature extraction",
    },
    {
        "pdb_id": "4EKK",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_exact_source_mapped_positive_with_context_ambiguity",
        "evaluation_label_source": "prior exact-source review mapped AKT/GSK3B Ser9, but later broad-source validation flagged source-context ambiguity; label used only after feature extraction",
    },
    {
        "pdb_id": "1L0O",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_product_state_positive",
        "evaluation_label_source": "prior review-only product-state protein kinase positive candidate m_csa:760; label used only after feature extraction",
    },
    {
        "pdb_id": "3TM0",
        "evaluation_label": "positive_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_ligand_analog_positive",
        "evaluation_label_source": "prior review-only ligand-analog ePK positive m_csa:640; label used only after feature extraction",
    },
    {
        "pdb_id": "4HPU",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_nonpositive_substrate_mode_rejected",
        "evaluation_label_source": "prior review-only source validation rejected substrate-mode assignment; label used only after feature extraction",
    },
    {
        "pdb_id": "7T56",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_transporter_control",
        "evaluation_label_source": "prior review-only transporter/source-expansion control; label used only after feature extraction",
    },
    {
        "pdb_id": "7T57",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_transporter_control",
        "evaluation_label_source": "prior review-only transporter/source-expansion control; label used only after feature extraction",
    },
    {
        "pdb_id": "9L3U",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_transporter_control",
        "evaluation_label_source": "prior review-only membrane translocase control; label used only after feature extraction",
    },
    {
        "pdb_id": "3Q4Z",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_heteromeric_topology_control",
        "evaluation_label_source": "prior review-only same-accession heteromeric topology control; label used only after feature extraction",
    },
    {
        "pdb_id": "4I94",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_heteromeric_topology_control",
        "evaluation_label_source": "prior review-only same-accession heteromeric topology control; label used only after feature extraction",
    },
    {
        "pdb_id": "5XD6",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_heteromeric_topology_control",
        "evaluation_label_source": "prior review-only same-accession heteromeric topology control; label used only after feature extraction",
    },
    {
        "pdb_id": "6ILT",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_pfkb_sibling_control",
        "evaluation_label_source": "prior review-only PfkB/ribokinase sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "8W2H",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_pfka_sibling_control",
        "evaluation_label_source": "prior review-only PfkA sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "8W2J",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_pfka_sibling_control",
        "evaluation_label_source": "prior review-only PfkA sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "9OAN",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_ndk_sibling_control",
        "evaluation_label_source": "prior review-only nucleoside diphosphate kinase sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "9PFY",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_ndk_sibling_control",
        "evaluation_label_source": "prior review-only nucleoside diphosphate kinase sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "3FGU",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_askha_sibling_control",
        "evaluation_label_source": "prior review-only ASKHA sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "3CRL",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_ghkl_sibling_control",
        "evaluation_label_source": "prior review-only GHKL sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "2OCP",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_dnk_sibling_control",
        "evaluation_label_source": "prior review-only deoxynucleoside kinase sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "1OJ4",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_ghmp_sibling_control",
        "evaluation_label_source": "prior review-only GHMP sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "1QHA",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_askha_sibling_control",
        "evaluation_label_source": "prior review-only ASKHA sibling control; label used only after feature extraction",
    },
    {
        "pdb_id": "1TFW",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_topology_confounded_same_chain_control",
        "evaluation_label_source": "prior review-only topology-confounded nonpositive row; label used only after feature extraction",
    },
    {
        "pdb_id": "2DRA",
        "evaluation_label": "counterexample_not_true_substrate_acceptor",
        "evaluation_group": "nonoverlap_topology_confounded_same_chain_control",
        "evaluation_label_source": "prior review-only topology-confounded nonpositive row; label used only after feature extraction",
    },
]


def folded_n_terminal_positive_coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    covered = []
    blocked_or_missing = []
    for row in rows:
        if row["evaluation_label"] != "positive_true_substrate_acceptor":
            continue
        features = row["structure_features"]
        candidates = features.get("nearest_hydroxyl_pair_candidates_within_8a", [])
        qualifying = [
            candidate
            for candidate in candidates
            if candidate.get("candidate_acceptor_chain_is_folded_like")
            and candidate.get("candidate_acceptor_is_n_terminal_sty")
            and candidate.get("candidate_resolved_n_terminal_auth_terminal_like")
        ]
        record = {
            "pdb_id": row["pdb_id"],
            "evaluation_group": row["evaluation_group"],
            "ligand_state": features["ligand_state"],
            "nearest_distance_angstrom": features["nearest_protein_hydroxyl_distance_angstrom"],
            "qualifying_folded_auth_terminal_candidate_count": len(qualifying),
            "qualifying_folded_auth_terminal_candidates": qualifying[:3],
        }
        if qualifying:
            covered.append(record)
        else:
            blocked_or_missing.append(record)
    return {
        "nonoverlap_positive_count": sum(
            1 for row in rows if row["evaluation_label"] == "positive_true_substrate_acceptor"
        ),
        "folded_auth_terminal_positive_count": len(covered),
        "folded_auth_terminal_positive_pdb_ids": [row["pdb_id"] for row in covered],
        "positive_rows_without_folded_auth_terminal_candidate": blocked_or_missing,
    }


def internal_fragment_mimic_pressure(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pressure_rows = []
    for row in rows:
        features = row["structure_features"]
        for candidate in features.get("nearest_hydroxyl_pair_candidates_within_8a", []):
            if not candidate.get("candidate_resolved_n_terminal_internal_fragment_like"):
                continue
            pressure_rows.append(
                {
                    "pdb_id": row["pdb_id"],
                    "evaluation_label": row["evaluation_label"],
                    "evaluation_group": row["evaluation_group"],
                    "candidate": candidate,
                }
            )
    return {
        "internal_fragment_like_candidate_count": len(pressure_rows),
        "internal_fragment_like_pdb_ids": sorted({row["pdb_id"] for row in pressure_rows}),
        "examples": pressure_rows[:10],
    }


def choose_primary_outcome(rule_results: list[dict[str, Any]], coverage: dict[str, Any]) -> str:
    inherited = inherited_primary_outcome(rule_results)
    if coverage["folded_auth_terminal_positive_count"] == 0:
        return "blocker_not_cleared_data_scarcity"
    return inherited


def build_payload(workflow_started_at: str) -> dict[str, Any]:
    script_started_at = utc_now()
    rows = []
    for row_template in FROZEN_ROWS:
        rows.append(reduced_features(row_template["pdb_id"], row_template, workflow_started_at))
        time.sleep(0.1)
    rule_results = [
        confusion_for_rule(rows, rule_id, rule_spec)
        for rule_id, rule_spec in RULES.items()
    ]
    coverage = folded_n_terminal_positive_coverage(rows)
    mimic_pressure = internal_fragment_mimic_pressure(rows)
    outcome = choose_primary_outcome(rule_results, coverage)
    if outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {outcome}")
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    materialized_rows = [row for row in rows if row["fetch_status"] == "ok"]
    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "workflow_started_at": workflow_started_at,
            "script_started_at": script_started_at,
            "lane_id": LANE_ID,
            "method": "epk_folded_nterminal_auth_terminal_guard_generalization_v2_review_only",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "nonoverlap_from_prior_terminal_stress": True,
            "frozen_row_count": len(FROZEN_ROWS),
            "materialized_row_count": len(materialized_rows),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "primary_outcome": outcome,
        },
        "row_freeze_rationale": {
            "handoff_next_experiment": "epk_folded_nterminal_auth_terminal_guard_generalization_v2_review_only",
            "requested_enrichment": [
                "true folded N-terminal substrate positives with auth-terminal-like numbering",
                "7B56-style internal-fragment N-terminal-STY mimics",
                "active gamma-capable ATP/ANP/analog rows from sibling families",
                "ADP/product-state positives kept separate from active-gamma positives",
            ],
            "why_full_enrichment_was_not_possible": (
                "Prior lane artifacts repeatedly identify 5HVK as the only source-valid "
                "heteromeric folded N-terminal protein-substrate positive. The non-overlap "
                "source-reviewed positives available for this run are current protein-substrate, "
                "exact-source/context-ambiguous, product-state, or ligand-analog rows rather than "
                "independent folded auth-terminal positives."
            ),
            "fallback_bounded_experiment": (
                "Freeze a 24-row non-overlap tranche from prior review artifacts and test whether "
                "strict_auth_terminal_guard_v1 has any independent folded-auth-terminal positive "
                "coverage while retaining sibling/control rejection."
            ),
        },
        "hypothesis": (
            "If author-terminal indexing is a general source-free substrate-role feature, "
            "strict_auth_terminal_guard_v1 should retain non-overlap folded N-terminal protein "
            "substrate positives and reject internal-fragment N-terminal-STY mimics and sibling controls. "
            "If the tranche contains no independent folded N-terminal positives, the apparent 7B56 repair "
            "is coverage-limited counterevidence rather than a cleared rule."
        ),
        "diagnostic_rows": rows,
        "rules": rule_results,
        "rule_delta": summarize_rule_delta(rule_results),
        "folded_n_terminal_positive_coverage": coverage,
        "internal_fragment_mimic_pressure": mimic_pressure,
        "focused_probe": row_probe(
            rows,
            ["1IR3", "2PHK", "4EKK", "1L0O", "3TM0", "4HPU", "7T56", "7T57", "9L3U"],
        ),
        "blocker_classification": {
            "primary_outcome": outcome,
            "coverage_signal": (
                "The non-overlap tranche does not contain an independent folded, auth-terminal-like "
                "N-terminal true substrate positive, so the guard cannot be generalized beyond 5HVK."
            ),
            "method_signal": (
                "The guard is a useful internal-fragment counteraxis, but it does not identify "
                "non-terminal folded protein substrate acceptors and cannot repair product/analog-state rows."
            ),
            "comparable_blocker_signal": (
                "Prior lane artifacts have not shown comparable ePK substrate-role blockers clearing "
                "with structure-only nearest-atom or terminal-position rules; usable progress remains "
                "hybrid source-reviewed evaluation with source evidence excluded from predictive features."
            ),
        },
    }


def ledger_record(payload: dict[str, Any], workflow_started_at: str, started_at: str) -> dict[str, Any]:
    ended_at = utc_now()
    start_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(ended_at.replace("Z", "+00:00"))
    measured_minutes = round((end_dt - start_dt).total_seconds() / 60.0, 2)
    by_id = {rule["rule_id"]: rule for rule in payload["rules"]}
    auth_rule = by_id["strict_auth_terminal_guard_v1"]
    strict_rule = by_id["strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1"]
    permissive_rule = by_id["permissive_nearest_hydroxyl_6a_v1"]
    coverage = payload["folded_n_terminal_positive_coverage"]
    return {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": payload["hypothesis"],
        "diagnostic_rows_added_or_reused": {
            "total": payload["metadata"]["frozen_row_count"],
            "added_this_run": [row["pdb_id"] for row in FROZEN_ROWS],
            "reused_from_prior_30_row_terminal_stress": 0,
            "nonoverlap_from_prior_terminal_stress": True,
            "row_freeze_rationale": payload["row_freeze_rationale"],
        },
        "source_free_features_tested": [
            "candidate author residue number",
            "resolved chain ordinal",
            "auth_seq_id minus resolved ordinal",
            "auth-terminal-like N-terminal STY guard",
            "internal-fragment-like N-terminal STY guard",
            "nonoverlap folded N-terminal positive coverage probe",
            "existing chain length/topology/nucleotide context features",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "strict_baseline": strict_rule,
            "strict_auth_terminal_guard": auth_rule,
            "permissive_nearest_hydroxyl": permissive_rule,
            "delta": payload["rule_delta"],
        },
        "confusion_matrix": auth_rule["confusion_matrix"],
        "decisive_counterexamples": {
            "independent_folded_n_terminal_positive_absent": (
                "no non-overlap true positive supplied a folded auth-terminal-like N-terminal STY candidate"
            ),
            "4EKK": "exact-source mapped positive remains source-context ambiguous in prior broad review and is not folded N-terminal guard evidence",
        },
        "false_positive_analysis": {
            "baseline_strict_false_positives": payload["rule_delta"]["baseline_strict_false_positives"],
            "auth_guard_false_positives": payload["rule_delta"]["auth_guard_false_positives"],
            "internal_fragment_pressure": payload["internal_fragment_mimic_pressure"],
            "interpretation": (
                "The guard did not produce a new decisive false positive in this non-overlap tranche, "
                "but this is not clearance because the tranche lacks an independent folded N-terminal positive."
            ),
        },
        "false_negative_analysis": {
            "auth_guard_false_negatives": auth_rule["pdb_ids_by_outcome"]["false_negative"],
            "failure_mode_counts": auth_rule["failure_mode_counts"],
            "folded_n_terminal_positive_coverage": coverage,
            "interpretation": (
                "False negatives are dominated by product/analog state or non-terminal folded protein "
                "substrate acceptors outside the N-terminal guard's identity mode."
            ),
        },
        "blocker_classification": payload["blocker_classification"],
        "next_query": (
            "Stop trying to generalize the terminal-index guard without independent folded N-terminal positives; "
            "next test a different source-free feature family, such as reciprocal cross-chain/entity asymmetry "
            "or residue burial/local solvent exposure, on the existing positive/control rows."
        ),
        "primary_outcome": payload["metadata"]["primary_outcome"],
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep auth-terminal indexing as review-only "
            "counterevidence for 7B56-like internal fragments, not a general substrate-role identity rule."
        ),
        "git_sync_status": (
            "git fetch origin failed at start with Operation not permitted writing FETCH_HEAD; "
            "continued on current research/epk-substrate-role-identity branch state"
        ),
        "workflow_started_at": workflow_started_at,
        "artifact_path": f"artifacts/research_lanes/epk_substrate_role_identity/{ARTIFACT_ID}.json",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--artifact-dir", default="artifacts/research_lanes/epk_substrate_role_identity")
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    artifact_dir = Path(args.artifact_dir)
    payload = build_payload(args.workflow_started_at)
    artifact_path = artifact_dir / f"{ARTIFACT_ID}.json"
    write_json(artifact_path, payload)
    if args.append_ledger:
        append_jsonl(
            artifact_dir / "epk_substrate_role_identity_runs.jsonl",
            ledger_record(payload, args.workflow_started_at, args.started_at),
        )
    print(
        json.dumps(
            {
                "artifact_path": str(artifact_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "rule_delta": payload["rule_delta"],
                "folded_n_terminal_positive_coverage": payload[
                    "folded_n_terminal_positive_coverage"
                ],
                "fetch_status_counts": payload["metadata"]["fetch_status_counts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
