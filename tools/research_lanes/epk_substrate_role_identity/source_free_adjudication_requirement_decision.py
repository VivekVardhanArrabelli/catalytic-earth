#!/usr/bin/env python3
"""Review-only ePK source-free adjudication requirement decision.

This lane-local helper converts the frozen source-free diagnostic evidence into
a compact claim/review/no-claim matrix. It does not fetch structures and does
not use source text as predictive input.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_source_free_adjudication_requirement_decision_v1_20260520"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_false_negative_state_topology_decision_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_source_free_adjudication_requirement_decision_v1_20260520.json"
)


REVIEW_REQUIRED_CLASSES = {
    "phosphotransfer_gamma_unavailable_product_or_adp_state",
    "phosphotransfer_gamma_unavailable_unknown_state",
    "ambiguous_reciprocal_folded_tyr_context",
    "ambiguous_same_chain_autophosphorylation_like_context",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_source_payload() -> dict[str, Any]:
    return json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))


def load_prior_run_records() -> list[dict[str, Any]]:
    if not LEDGER_PATH.exists():
        return []
    records = []
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def evidence_action(row: dict[str, Any]) -> str:
    availability = row["availability_class"]
    if availability == "claimable_by_auth_guard_strict_context":
        return "source_free_claim_allowed_strict_context"
    if availability == "blocked_internal_fragment_n_terminal_mimic":
        return "no_claim_internal_fragment_counterevidence"
    if availability in REVIEW_REQUIRED_CLASSES:
        return "review_required_source_free_ambiguous_or_unavailable"
    return "no_claim_source_free_insufficient_identity_context"


def review_reason(row: dict[str, Any]) -> str:
    availability = row["availability_class"]
    if availability == "phosphotransfer_gamma_unavailable_product_or_adp_state":
        return "product_or_adp_state_lacks_terminal_gamma_transfer_geometry"
    if availability == "phosphotransfer_gamma_unavailable_unknown_state":
        return "terminal_gamma_transfer_geometry_unavailable"
    if availability == "ambiguous_reciprocal_folded_tyr_context":
        return "reciprocal_folded_tyr_context_shared_by_true_positives_and_9UW4"
    if availability == "ambiguous_same_chain_autophosphorylation_like_context":
        return "same_chain_near_hydroxyl_context_admits_many_counterexamples"
    if availability == "blocked_internal_fragment_n_terminal_mimic":
        return "author_terminal_counterevidence_blocks_internal_fragment_mimic"
    if availability == "claimable_by_auth_guard_strict_context":
        return "accepted_by_zero_false_positive_auth_guard_strict_context"
    return "near_hydroxyl_geometry_has_no_claimable_substrate_identity_context"


def confusion_for_claim_gate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    for row in rows:
        predicted_positive = evidence_action(row) == "source_free_claim_allowed_strict_context"
        actual_positive = is_positive(row)
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "availability_class": row["availability_class"],
                "evidence_action": evidence_action(row),
                "review_reason": review_reason(row),
            }
        )
    return {
        "rule_id": "source_free_claim_gate_or_review_required_v1",
        "rule_description": (
            "Permit a source-free positive claim only for the frozen auth-terminal "
            "guarded strict context. Route product/ADP, reciprocal folded-chain, "
            "and same-chain/autophosphorylation-like contexts to review instead of "
            "calling them positive."
        ),
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": buckets,
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
    }


def action_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label: dict[str, Counter[str]] = {"positive": Counter(), "counterexample": Counter()}
    by_availability: dict[str, Counter[str]] = {}
    for row in rows:
        label_key = "positive" if is_positive(row) else "counterexample"
        action = evidence_action(row)
        by_label[label_key][action] += 1
        by_availability.setdefault(row["availability_class"], Counter())[action] += 1
    return {
        "by_evaluation_label": {key: dict(sorted(counter.items())) for key, counter in by_label.items()},
        "by_availability_class": {
            key: dict(sorted(counter.items())) for key, counter in sorted(by_availability.items())
        },
    }


def compact_decision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact = []
    for row in rows:
        selected = row.get("selected_claim_or_ambiguity_candidate") or {}
        same_chain = row.get("nearest_same_chain_candidate") or {}
        compact.append(
            {
                "pdb_id": row["pdb_id"],
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "availability_class": row["availability_class"],
                "evidence_action": evidence_action(row),
                "review_reason": review_reason(row),
                "ligand_state": row.get("ligand_state"),
                "terminal_gamma_equivalent_atom_available": row.get(
                    "terminal_gamma_equivalent_atom_available"
                ),
                "candidate_count_within_8a": row.get("candidate_count_within_8a"),
                "nearest_protein_hydroxyl_distance_angstrom": row.get(
                    "nearest_protein_hydroxyl_distance_angstrom"
                ),
                "selected_candidate_distance_angstrom": selected.get("distance_angstrom"),
                "selected_candidate_residue_code": selected.get("candidate_acceptor_residue_code"),
                "selected_candidate_same_chain_topology": selected.get("same_chain_topology"),
                "selected_candidate_cross_chain_topology": selected.get("cross_chain_topology"),
                "selected_candidate_reciprocal_context_class": selected.get(
                    "reciprocal_context_class"
                ),
                "selected_candidate_orientation_support_class": selected.get(
                    "orientation_support_class"
                ),
                "nearest_same_chain_distance_angstrom": same_chain.get("distance_angstrom"),
            }
        )
    return compact


def prior_feature_family_matrix(records: list[dict[str, Any]]) -> dict[str, Any]:
    lane_records = [record for record in records if record.get("lane_id") == LANE_ID]
    outcomes = Counter(record.get("primary_outcome", "unknown") for record in lane_records)
    families = Counter()
    for record in lane_records:
        for feature in record.get("source_free_features_tested", []):
            families[feature] += 1
    cleared = [
        record
        for record in lane_records
        if record.get("primary_outcome") == "blocker_cleared_source_free"
    ]
    record_summaries = [
        {
            "artifact_path": record.get("artifact_path"),
            "primary_outcome": record.get("primary_outcome"),
            "confusion_matrix": record.get("confusion_matrix"),
            "decisive_counterexamples": record.get("decisive_counterexamples"),
            "next_query": record.get("next_query"),
            "recommendation": record.get("recommendation"),
        }
        for record in lane_records
    ]
    return {
        "records_checked": len(lane_records),
        "outcome_counts": dict(sorted(outcomes.items())),
        "any_prior_source_free_clearance": bool(cleared),
        "prior_run_outcome_matrix": record_summaries,
        "source_free_feature_families_seen": dict(sorted(families.items())),
        "assessment": (
            "No prior run in this lane cleared comparable ePK substrate-role "
            "identity blockers with source-free structure-only features. The "
            "historical lane pattern supports a source-reviewed adjudication "
            "requirement, with source evidence excluded from predictive features."
        ),
    }


def review_required_positive_ids(rows: list[dict[str, Any]]) -> list[str]:
    return [
        row["pdb_id"]
        for row in rows
        if is_positive(row)
        and evidence_action(row) == "review_required_source_free_ambiguous_or_unavailable"
    ]


def review_required_counterexample_ids(rows: list[dict[str, Any]]) -> list[str]:
    return [
        row["pdb_id"]
        for row in rows
        if not is_positive(row)
        and evidence_action(row) == "review_required_source_free_ambiguous_or_unavailable"
    ]


def probe_row(rows: list[dict[str, Any]], pdb_id: str) -> dict[str, Any] | None:
    for row in rows:
        if row["pdb_id"] == pdb_id:
            selected = (
                row.get("selected_claim_or_ambiguity_candidate")
                or row.get("nearest_same_chain_candidate")
                or {}
            )
            return {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "availability_class": row["availability_class"],
                "evidence_action": evidence_action(row),
                "review_reason": review_reason(row),
                "ligand_state": row.get("ligand_state"),
                "candidate_count_within_8a": row.get("candidate_count_within_8a"),
                "nearest_protein_hydroxyl_distance_angstrom": row.get(
                    "nearest_protein_hydroxyl_distance_angstrom"
                ),
                "selected_candidate_distance_angstrom": selected.get("distance_angstrom"),
                "selected_candidate_residue_code": selected.get("candidate_acceptor_residue_code"),
                "selected_candidate_auth_seq_id_int": selected.get(
                    "candidate_acceptor_auth_seq_id_int"
                ),
                "selected_candidate_residue_ordinal_in_chain": selected.get(
                    "candidate_acceptor_residue_ordinal_in_chain"
                ),
                "selected_candidate_internal_fragment_like": selected.get(
                    "candidate_resolved_n_terminal_internal_fragment_like"
                ),
                "selected_candidate_same_chain_topology": selected.get("same_chain_topology"),
                "selected_candidate_cross_chain_topology": selected.get("cross_chain_topology"),
                "selected_candidate_reciprocal_context_class": selected.get(
                    "reciprocal_context_class"
                ),
                "selected_candidate_orientation_support_class": selected.get(
                    "orientation_support_class"
                ),
            }
    return None


def build_payload(started_at: str) -> dict[str, Any]:
    source_payload = load_source_payload()
    rows = source_payload["diagnostic_rows"]
    prior_records = load_prior_run_records()
    claim_gate = confusion_for_claim_gate(rows)
    actions = action_summary(rows)
    history = prior_feature_family_matrix(prior_records)
    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60.0, 2)

    positive_review_ids = review_required_positive_ids(rows)
    counterexample_review_ids = review_required_counterexample_ids(rows)
    false_negative_ids = claim_gate["pdb_ids_by_outcome"]["false_negative"]
    blocker_probe_rows = {
        pdb_id: probe_row(rows, pdb_id) for pdb_id in ["7B56", "9UUR", "9UUX", "9UW4", "3TM0"]
    }
    primary_outcome = "blocker_not_cleared_biology_ambiguity"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    source_free_features = [
        "frozen availability_class taxonomy from ligand gamma availability and topology",
        "source-free claim gate versus review-required abstention action",
        "auth-terminal guarded strict context as only source-free claimable class",
        "product/ADP terminal-gamma unavailability class",
        "reciprocal folded-chain Tyr ambiguity class",
        "same-chain/autophosphorylation-like ambiguity class",
        "historical lane feature-family clearance matrix from JSONL run records",
    ]

    rule_results = {
        claim_gate["rule_id"]: {
            "confusion_matrix": claim_gate["confusion_matrix"],
            "pdb_ids_by_outcome": claim_gate["pdb_ids_by_outcome"],
            "clears_diagnostic_tranche": claim_gate["clears_diagnostic_tranche"],
        },
        "review_required_abstention_matrix_v1": {
            "action_summary": actions,
            "review_required_positive_ids": positive_review_ids,
            "review_required_counterexample_ids": counterexample_review_ids,
            "production_identity_rule": False,
        },
    }

    run_record = {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "If current structure-derived source-free features are sufficient for ePK "
            "substrate-role identity, the frozen claim gate should allow all true "
            "substrate phosphoacceptors without false positives; otherwise the "
            "remaining rows must be routed to source-reviewed adjudication."
        ),
        "diagnostic_rows_added_or_reused": {
            "reused_from_false_negative_state_topology_decision_probe": len(rows),
            "added_this_run": [],
            "total": len(rows),
        },
        "source_free_features_tested": source_free_features,
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": rule_results,
        "confusion_matrix": claim_gate["confusion_matrix"],
        "decisive_counterexamples": {
            "7B56": (
                "Blocked by source-free internal-fragment/auth-terminal counterevidence; "
                "this separates the decisive strict false positive locally but does not "
                "identify reciprocal folded-chain or same-chain true positives."
            ),
            "review_required_positive_ids": positive_review_ids,
            "review_required_counterexample_ids": counterexample_review_ids,
            "hard_reciprocal_trio": ["9UUR", "9UUX", "9UW4"],
            "blocker_probe_rows": blocker_probe_rows,
            "same_chain_review_pressure_count": actions["by_availability_class"]
            .get("ambiguous_same_chain_autophosphorylation_like_context", {})
            .get("review_required_source_free_ambiguous_or_unavailable", 0),
            "prior_lane_source_free_clearance_found": history["any_prior_source_free_clearance"],
        },
        "false_positive_analysis": {
            "claim_gate_false_positives": claim_gate["pdb_ids_by_outcome"]["false_positive"],
            "review_required_counterexamples": counterexample_review_ids,
            "interpretation": (
                "The conservative claim gate has zero false positives, but that is "
                "achieved by abstaining on reciprocal folded-chain and same-chain "
                "contexts rather than identifying substrate role source-free."
            ),
        },
        "false_negative_analysis": {
            "claim_gate_false_negatives": false_negative_ids,
            "review_required_positive_ids": positive_review_ids,
            "review_required_positive_reasons": {
                row["pdb_id"]: review_reason(row)
                for row in rows
                if row["pdb_id"] in positive_review_ids
            },
            "interpretation": (
                "The false negatives are not repairable with current frozen structure "
                "features without admitting known counterexamples or product-state "
                "geometry that lacks terminal-gamma transfer evidence."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": (
                "Source-free structure evidence supports a review requirement, not a "
                "production substrate-role identity rule."
            ),
            "historical_comparator_assessment": history["assessment"],
        },
        "primary_outcome": primary_outcome,
        "next_query": (
            "Stop source-free scalar probing unless a new evidence modality is introduced; "
            "promote this lane finding into a source-reviewed adjudication requirement for "
            "product/ADP, reciprocal folded-chain, and same-chain/autophosphorylation-like rows."
        ),
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep structure-derived features as "
            "compact review evidence and require hybrid source-reviewed adjudication for "
            "substrate-role identity decisions."
        ),
        "git_sync_status": (
            "git fetch and fast-forward merge were blocked by linked-worktree metadata "
            "permission errors; live remote was checked with git ls-remote before this run."
        ),
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_adjudication_requirement_decision",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifact": str(SOURCE_ARTIFACT),
            "frozen_row_count": len(rows),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "source_free_claim_allowed_strict_context": (
                "Only the frozen auth-terminal guarded strict context is allowed to make "
                "a source-free positive claim in this review-only decision probe."
            ),
            "review_required_source_free_ambiguous_or_unavailable": (
                "The structure-only state either lacks transfer geometry or shares a "
                "topology class with true positives and counterexamples."
            ),
            "no_claim_source_free_insufficient_identity_context": (
                "Resolved near-hydroxyl geometry exists, but no accepted source-free "
                "identity context supports a substrate-role claim."
            ),
        },
        "decision_rows": compact_decision_rows(rows),
        "action_summary": actions,
        "claim_gate_rule": claim_gate,
        "blocker_probe_rows": blocker_probe_rows,
        "historical_lane_feature_family_matrix": history,
        "blocker_classification": run_record["blocker_classification"],
        "run_record": run_record,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    payload = build_payload(args.started_at)
    output_path = Path(args.output)
    write_json(output_path, payload)
    if args.append_ledger:
        append_jsonl(LEDGER_PATH, payload["run_record"])
    print(
        json.dumps(
            {
                "artifact": str(output_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "claim_gate_confusion": payload["claim_gate_rule"]["confusion_matrix"],
                "review_required_positives": payload["run_record"]["decisive_counterexamples"][
                    "review_required_positive_ids"
                ],
                "prior_source_free_clearance": payload["historical_lane_feature_family_matrix"][
                    "any_prior_source_free_clearance"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
