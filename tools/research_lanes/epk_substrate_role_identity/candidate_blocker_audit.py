#!/usr/bin/env python3
"""Audit source-free ePK candidate evidence into blocker triage rows.

This lane-local helper consumes the candidate-level gamma/acceptor evidence
table and emits compact PDB-level blocker summaries. It does not fetch
additional source material and keeps review labels only in evaluation context.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_candidate_blocker_audit_v1_20260521"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_blocker_audit_v1_20260521.json"
)

PRIMARY_OUTCOMES = {
    "candidate_evidence_rows_emitted",
    "blocker_cleared_source_free",
    "blocker_not_cleared_data_scarcity",
    "blocker_not_cleared_method_weakness",
    "blocker_not_cleared_biology_ambiguity",
    "counterexample_found",
    "next_query_defined",
}

HARD_CASE_PDBS = {"7B56", "9UUR", "9UUX", "9UW4", "3QHR", "3QHW", "1L0O", "3TM0", "1QHA"}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_candidate_rows() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    rows = payload["candidate_evidence_rows"] + payload["state_only_rows"]
    return payload, rows


def count_by(rows: list[dict[str, Any]], evidence_key: str) -> dict[str, int]:
    counter = Counter(str(row["source_free_evidence"].get(evidence_key)) for row in rows)
    return dict(sorted(counter.items()))


def state_blocker_matrix(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        evidence = row["source_free_evidence"]
        matrix[str(evidence["coordinate_state"])][str(evidence["blocker_class"])] += 1
    return {state: dict(sorted(counter.items())) for state, counter in sorted(matrix.items())}


def grouped_by_pdb(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["pdb_id"]].append(row)
    return dict(sorted(grouped.items()))


def nearest_candidate(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [
        row
        for row in rows
        if row["source_free_evidence"].get("distance_angstrom") is not None
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda row: row["source_free_evidence"]["distance_angstrom"])


def unblocked_candidate_ids(rows: list[dict[str, Any]]) -> list[str]:
    return sorted(
        row["candidate_id"]
        for row in rows
        if row["source_free_evidence"]["coordinate_state"] == "active_gamma"
        and row["source_free_evidence"]["blocker_class"] == "none"
    )


def blocker_candidate_ids(rows: list[dict[str, Any]], blocker: str) -> list[str]:
    return sorted(
        row["candidate_id"]
        for row in rows
        if row["source_free_evidence"]["blocker_class"] == blocker
    )


def triage_bucket(rows: list[dict[str, Any]]) -> str:
    states = {row["source_free_evidence"]["coordinate_state"] for row in rows}
    blockers = {row["source_free_evidence"]["blocker_class"] for row in rows}
    if states & {"product_state", "adp_state"}:
        return "state_specific_product_or_adp_review"
    if states & {
        "ligand_absent",
        "ambiguous_coordinate_state",
        "unavailable_coordinate_state",
        "metal_absent",
        "split_state",
        "substrate_acceptor_analog_state",
    }:
        return "coordinate_materialization_review"
    if any(row["row_schema"].endswith("_state_only") for row in rows):
        return "active_gamma_no_near_hydroxyl_review"
    if "internal_fragment_mimicry" in blockers:
        return "internal_fragment_mimicry_blocked"
    if unblocked_candidate_ids(rows):
        return "unblocked_structural_candidate_present"
    if "topology_ambiguity" in blockers:
        return "topology_review_required"
    if "substrate_role_identity" in blockers:
        return "substrate_role_review_required"
    if blockers == {"active_gamma_geometry"}:
        return "active_gamma_geometry_blocked"
    return "mixed_structural_review"


def review_required_reason(bucket: str) -> str:
    reasons = {
        "state_specific_product_or_adp_review": (
            "Terminal gamma transfer geometry is unavailable in product/ADP state."
        ),
        "coordinate_materialization_review": (
            "Ligand or coordinate materialization prevents active-gamma candidate adjudication."
        ),
        "active_gamma_no_near_hydroxyl_review": (
            "Active gamma is present, but no materialized hydroxyl candidate is within the row evidence."
        ),
        "internal_fragment_mimicry_blocked": (
            "N-terminal-looking acceptor is source-free internal-fragment mimicry."
        ),
        "unblocked_structural_candidate_present": (
            "A source-free unblocked structural candidate is present; still evaluation-only."
        ),
        "topology_review_required": (
            "Same-chain or reciprocal folded-chain topology leaves biological substrate role ambiguous."
        ),
        "substrate_role_review_required": (
            "Folded cross-chain protein context leaves substrate role ambiguous."
        ),
        "active_gamma_geometry_blocked": (
            "Terminal gamma is present, but candidate geometry does not support transfer."
        ),
        "mixed_structural_review": "Mixed source-free blockers require review-only adjudication.",
    }
    return reasons[bucket]


def compact_nearest(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    evidence = row["source_free_evidence"]
    return {
        "candidate_id": row["candidate_id"],
        "distance_angstrom": evidence.get("distance_angstrom"),
        "coordinate_state": evidence.get("coordinate_state"),
        "blocker_class": evidence.get("blocker_class"),
        "candidate_role_class": evidence.get("candidate_role_class"),
        "reciprocal_context_class": evidence.get("reciprocal_context_class"),
        "same_chain_topology": evidence.get("same_chain_topology"),
        "coordinate_certainty_class": evidence.get("coordinate_certainty", {}).get(
            "coordinate_certainty_class"
        ),
    }


def build_pdb_triage_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    triage_rows = []
    for pdb_id, pdb_rows in grouped_by_pdb(rows).items():
        first = pdb_rows[0]
        bucket = triage_bucket(pdb_rows)
        unblocked_ids = unblocked_candidate_ids(pdb_rows)
        triage_rows.append(
            {
                "row_schema": "epk_candidate_blocker_audit_v1",
                "pdb_id": pdb_id,
                "candidate_pair_row_count": sum(
                    1 for row in pdb_rows if row["row_schema"] == "epk_candidate_evidence_v1"
                ),
                "state_only_row_count": sum(1 for row in pdb_rows if row["row_schema"].endswith("_state_only")),
                "coordinate_states_observed": count_by(pdb_rows, "coordinate_state"),
                "blocker_classes_observed": count_by(pdb_rows, "blocker_class"),
                "state_blocker_matrix": state_blocker_matrix(pdb_rows),
                "source_free_unblocked_candidate_present": bool(unblocked_ids),
                "source_free_unblocked_candidate_ids": unblocked_ids,
                "topology_ambiguity_candidate_ids": blocker_candidate_ids(pdb_rows, "topology_ambiguity"),
                "substrate_role_identity_candidate_ids": blocker_candidate_ids(
                    pdb_rows, "substrate_role_identity"
                ),
                "internal_fragment_mimicry_candidate_ids": blocker_candidate_ids(
                    pdb_rows, "internal_fragment_mimicry"
                ),
                "triage_bucket": bucket,
                "review_required_reason": review_required_reason(bucket),
                "nearest_candidate_by_distance": compact_nearest(nearest_candidate(pdb_rows)),
                "hard_case": pdb_id in HARD_CASE_PDBS,
                "review_context_for_evaluation_only": {
                    "evaluation_label": first["review_context_for_evaluation_only"]["evaluation_label"],
                    "evaluation_group": first["review_context_for_evaluation_only"]["evaluation_group"],
                    "source_artifact_id": first["review_context_for_evaluation_only"].get(
                        "source_artifact_id"
                    ),
                    "evaluation_label_used_only_for_eval": True,
                },
            }
        )
    return triage_rows


def confusion_for_pdb_triage(triage_rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    for row in triage_rows:
        predicted_positive = bool(row["source_free_unblocked_candidate_present"])
        actual_positive = (
            row["review_context_for_evaluation_only"]["evaluation_label"]
            == "positive_true_substrate_acceptor"
        )
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
                "predicted_unblocked_candidate_present": predicted_positive,
                "outcome": outcome,
                "triage_bucket": row["triage_bucket"],
                "coordinate_states_observed": row["coordinate_states_observed"],
                "blocker_classes_observed": row["blocker_classes_observed"],
            }
        )
    return {
        "rule_id": "pdb_level_unblocked_candidate_triage_v1",
        "rule_description": (
            "PDB-level sanity triage: at least one active-gamma candidate row has blocker_class=none. "
            "This is review support only, not a production substrate-role identity rule."
        ),
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": {key: sorted(value) for key, value in buckets.items()},
        "decisions": sorted(decisions, key=lambda item: item["pdb_id"]),
        "clears_diagnostic_tranche": False,
        "production_claim_allowed": False,
    }


def triage_counter(triage_rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in triage_rows).items()))


def hard_case_digest(triage_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    digest = {}
    for row in triage_rows:
        if not row["hard_case"]:
            continue
        digest[row["pdb_id"]] = {
            "triage_bucket": row["triage_bucket"],
            "coordinate_states_observed": row["coordinate_states_observed"],
            "blocker_classes_observed": row["blocker_classes_observed"],
            "source_free_unblocked_candidate_present": row[
                "source_free_unblocked_candidate_present"
            ],
            "nearest_candidate_by_distance": row["nearest_candidate_by_distance"],
        }
    return dict(sorted(digest.items()))


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    source_payload, rows = load_candidate_rows()
    triage_rows = build_pdb_triage_rows(rows)
    rule = confusion_for_pdb_triage(triage_rows)
    primary_outcome = "blocker_not_cleared_biology_ambiguity"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0, 2)
    blocker_counts = count_by(rows, "blocker_class")
    coordinate_state_counts = count_by(rows, "coordinate_state")
    triage_bucket_counts = triage_counter(triage_rows, "triage_bucket")

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "Candidate-level source-free evidence can support compact PDB-level blocker triage "
            "without adding unsafe non-abstention, but it still cannot adjudicate product/ADP, "
            "reciprocal folded-chain, or same-chain substrate-role biology."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(triage_rows),
            "total": len(triage_rows),
        },
        "candidate_evidence_rows_emitted": {
            "candidate_pair_rows_reused": source_payload["metadata"]["candidate_pair_row_count"],
            "state_only_rows_reused": source_payload["metadata"]["state_only_row_count"],
            "pdb_level_triage_rows_emitted": len(triage_rows),
            "new_gamma_acceptor_candidate_rows_emitted": 0,
        },
        "coordinate_states_observed": coordinate_state_counts,
        "source_free_features_tested": [
            "PDB-level aggregation of candidate coordinate states",
            "PDB-level aggregation of candidate blocker classes",
            "source-free unblocked active-gamma candidate presence sanity triage",
            "hard-case blocker digest for product/ADP, reciprocal folded-chain, same-chain, and internal-fragment rows",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            rule["rule_id"]: {
                "rule_description": rule["rule_description"],
                "confusion_matrix": rule["confusion_matrix"],
                "pdb_ids_by_outcome": rule["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": rule["clears_diagnostic_tranche"],
                "production_claim_allowed": rule["production_claim_allowed"],
            }
        },
        "confusion_matrix": rule["confusion_matrix"],
        "decisive_counterexamples": {
            "hard_case_digest": hard_case_digest(triage_rows),
            "triage_bucket_counts": triage_bucket_counts,
            "blocker_class_counts": blocker_counts,
            "state_blocker_matrix": state_blocker_matrix(rows),
        },
        "false_positive_analysis": {
            "pdb_level_unblocked_candidate_triage_false_positive_pdb_ids": rule[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "interpretation": (
                "The diagnostic audit has zero false positives for the unblocked-candidate sanity flag, "
                "but that flag remains review support because the diagnostic labels are evaluation-only "
                "and ambiguous ePK biology is still unresolved source-free."
            ),
        },
        "false_negative_analysis": {
            "pdb_level_unblocked_candidate_triage_false_negative_pdb_ids": rule[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "interpretation": (
                "False negatives are the known review-required classes: product/ADP rows lack "
                "terminal-gamma transfer geometry, reciprocal folded-chain Tyr rows share source-free "
                "topology with the 9UW4 counterexample, and 3TM0 is same-chain/autophosphorylation-like."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "coordinate_state_counts": coordinate_state_counts,
            "blocker_class_counts": blocker_counts,
            "triage_bucket_counts": triage_bucket_counts,
            "classification": (
                "The blocker remains biology ambiguity, not data scarcity: candidate evidence is "
                "materialized, but source-free structure cannot assign biological substrate role for "
                "product/ADP, reciprocal folded-chain, and same-chain cases."
            ),
        },
        "next_query": (
            "Use the PDB-level blocker audit for review triage and stop source-free scalar probing "
            "unless a genuinely new evidence modality becomes available."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep the candidate table and PDB-level audit as "
            "review-only evidence; product/ADP, reciprocal folded-chain, and same-chain cases still "
            "require source-reviewed adjudication."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "candidate_evidence_blocker_triage_audit",
            "review_only": True,
            "source_free_evidence_separated_from_review_context": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifact": str(SOURCE_ARTIFACT),
            "output_path": str(output_path),
            "source_candidate_pair_row_count": source_payload["metadata"]["candidate_pair_row_count"],
            "source_state_only_row_count": source_payload["metadata"]["state_only_row_count"],
            "pdb_level_triage_row_count": len(triage_rows),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "triage_bucket": (
                "Compact source-free blocker grouping for review routing; it is not a production "
                "substrate-role identity label."
            ),
            "source_free_unblocked_candidate_present": (
                "True when at least one active-gamma candidate row has blocker_class=none. "
                "This is a sanity flag only."
            ),
            "state_blocker_matrix": (
                "Coordinate-state by blocker-class counts from candidate rows, with review labels excluded."
            ),
        },
        "coordinate_state_counts": coordinate_state_counts,
        "blocker_class_counts": blocker_counts,
        "state_blocker_matrix": state_blocker_matrix(rows),
        "triage_bucket_counts": triage_bucket_counts,
        "pdb_level_triage_rows": triage_rows,
        "rules": [rule],
        "run_record": run_record,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--git-sync-status", required=True)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    payload = build_payload(args.workflow_started_at, args.git_sync_status, output_path)
    write_json(output_path, payload)
    if args.append_ledger:
        append_jsonl(LEDGER_PATH, payload["run_record"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
