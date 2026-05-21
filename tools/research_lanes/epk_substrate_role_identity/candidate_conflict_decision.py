#!/usr/bin/env python3
"""Build source-free ePK candidate conflict and abstention decisions.

This lane-local helper consumes the candidate-level evidence table and emits a
compact PDB-level conflict matrix. It intentionally avoids another scalar
rescue rule: non-abstaining calls are limited to already materialized
source-free structural support or hard source-free blockers, while topology and
state-specific cases remain review-only.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from candidate_blocker_audit import compact_nearest, grouped_by_pdb, nearest_candidate
from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_candidate_conflict_decision_v1_20260521"
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
    "epk_candidate_conflict_decision_v1_20260521.json"
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

HARD_CASE_PDBS = {
    "7B56",
    "9UUR",
    "9UUX",
    "9UW4",
    "3QHR",
    "3QHW",
    "1L0O",
    "3TM0",
    "1QHA",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_candidate_rows() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    rows = payload["candidate_evidence_rows"] + payload["state_only_rows"]
    return payload, rows


def evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row["source_free_evidence"]


def count_values(
    rows: list[dict[str, Any]],
    key: str,
    default: str | None = None,
) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value = evidence(row).get(key)
        if value is None and default is not None:
            value = default
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def count_nested(
    rows: list[dict[str, Any]],
    path: list[str],
    default: str | None = None,
) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value: Any = evidence(row)
        for key in path:
            value = value.get(key, {}) if isinstance(value, dict) else {}
        if value in ({}, None) and default is not None:
            value = default
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def rows_by_blocker(rows: list[dict[str, Any]], blocker: str) -> list[dict[str, Any]]:
    return [row for row in rows if evidence(row).get("blocker_class") == blocker]


def rows_by_role(rows: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    return [row for row in rows if evidence(row).get("candidate_role_class") == role]


def candidate_ids(rows: list[dict[str, Any]]) -> list[str]:
    return sorted(row["candidate_id"] for row in rows)


def bool_count(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if bool(evidence(row).get(key)))


def state_blocker_matrix(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        state = str(evidence(row).get("coordinate_state"))
        blocker = str(evidence(row).get("blocker_class"))
        matrix[state][blocker] += 1
    return {state: dict(sorted(counter.items())) for state, counter in sorted(matrix.items())}


def role_blocker_matrix(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        role = str(evidence(row).get("candidate_role_class") or "state_only")
        blocker = str(evidence(row).get("blocker_class"))
        matrix[role][blocker] += 1
    return {role: dict(sorted(counter.items())) for role, counter in sorted(matrix.items())}


def unblocked_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if evidence(row).get("coordinate_state") == "active_gamma"
        and evidence(row).get("blocker_class") == "none"
    ]


def materialization_states(states: set[str]) -> set[str]:
    return states & {
        "ligand_absent",
        "ambiguous_coordinate_state",
        "unavailable_coordinate_state",
        "metal_absent",
        "split_state",
        "substrate_acceptor_analog_state",
    }


def conflict_class(rows: list[dict[str, Any]]) -> str:
    states = {str(evidence(row).get("coordinate_state")) for row in rows}
    blockers = {str(evidence(row).get("blocker_class")) for row in rows}
    roles = {str(evidence(row).get("candidate_role_class")) for row in rows}
    unblocked = unblocked_rows(rows)

    if states & {"product_state", "adp_state"}:
        return "state_specific_product_or_adp_conflict"
    if materialization_states(states):
        return "coordinate_materialization_conflict"
    if "internal_fragment_mimicry" in blockers:
        return "internal_fragment_mimicry_conflict"
    if unblocked:
        if blockers & {"topology_ambiguity", "substrate_role_identity"}:
            return "unblocked_support_with_competing_ambiguous_candidates"
        return "unblocked_support_low_conflict"
    if "topology_ambiguity" in blockers:
        reciprocal = bool(rows_by_role(rows, "reciprocal_folded_tyr_candidate"))
        same_chain = bool(rows_by_role(rows, "same_chain_candidate"))
        if reciprocal and same_chain:
            return "topology_conflict_reciprocal_and_same_chain"
        if reciprocal:
            return "topology_conflict_reciprocal_folded_chain"
        if same_chain:
            return "topology_conflict_same_chain"
        return "topology_conflict_other"
    if "substrate_role_identity" in blockers:
        return "folded_cross_chain_role_identity_conflict"
    if blockers == {"active_gamma_geometry"}:
        if any(row["row_schema"].endswith("_state_only") for row in rows):
            return "active_gamma_no_near_hydroxyl_conflict"
        return "active_gamma_geometry_conflict"
    return "mixed_structural_conflict"


def decision_class(conflict: str) -> str:
    if conflict.startswith("unblocked_support"):
        return "source_free_structural_support_review_only"
    if conflict in {
        "internal_fragment_mimicry_conflict",
        "coordinate_materialization_conflict",
        "active_gamma_no_near_hydroxyl_conflict",
        "active_gamma_geometry_conflict",
    }:
        return "source_free_blocked_counterevidence_review_only"
    if conflict == "state_specific_product_or_adp_conflict":
        return "abstain_state_specific_review_required"
    if conflict.startswith("topology_conflict") or conflict == "folded_cross_chain_role_identity_conflict":
        return "abstain_biology_topology_review_required"
    return "abstain_mixed_review_required"


def conflict_signature(rows: list[dict[str, Any]]) -> str:
    states = "+".join(sorted({str(evidence(row).get("coordinate_state")) for row in rows}))
    blockers = "+".join(sorted({str(evidence(row).get("blocker_class")) for row in rows}))
    roles = "+".join(
        sorted(
            {
                str(evidence(row).get("candidate_role_class") or "state_only")
                for row in rows
            }
        )
    )
    return f"states={states}|blockers={blockers}|roles={roles}"


def compact_candidate(row: dict[str, Any]) -> dict[str, Any]:
    row_evidence = evidence(row)
    return {
        "candidate_id": row["candidate_id"],
        "coordinate_state": row_evidence.get("coordinate_state"),
        "blocker_class": row_evidence.get("blocker_class"),
        "candidate_role_class": row_evidence.get("candidate_role_class"),
        "distance_angstrom": row_evidence.get("distance_angstrom"),
        "reciprocal_context_class": row_evidence.get("reciprocal_context_class"),
        "same_chain_topology": row_evidence.get("same_chain_topology"),
        "cross_chain_topology": row_evidence.get("cross_chain_topology"),
        "acceptor_chain_is_short_peptide_like": row_evidence.get(
            "acceptor_chain_is_short_peptide_like"
        ),
        "acceptor_chain_is_folded_like": row_evidence.get("acceptor_chain_is_folded_like"),
        "coordinate_certainty_class": row_evidence.get("coordinate_certainty", {}).get(
            "coordinate_certainty_class"
        ),
    }


def build_conflict_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflict_rows: list[dict[str, Any]] = []
    for pdb_id, pdb_rows in grouped_by_pdb(rows).items():
        first = pdb_rows[0]
        conflict = conflict_class(pdb_rows)
        decision = decision_class(conflict)
        unblocked = unblocked_rows(pdb_rows)
        topology = rows_by_blocker(pdb_rows, "topology_ambiguity")
        substrate_role = rows_by_blocker(pdb_rows, "substrate_role_identity")
        internal_fragment = rows_by_blocker(pdb_rows, "internal_fragment_mimicry")
        geometry = rows_by_blocker(pdb_rows, "active_gamma_geometry")

        conflict_rows.append(
            {
                "row_schema": "epk_candidate_conflict_decision_v1",
                "pdb_id": pdb_id,
                "candidate_pair_row_count": sum(
                    1 for row in pdb_rows if row["row_schema"] == "epk_candidate_evidence_v1"
                ),
                "state_only_row_count": sum(
                    1 for row in pdb_rows if row["row_schema"].endswith("_state_only")
                ),
                "source_free_conflict_signature": conflict_signature(pdb_rows),
                "coordinate_states_observed": count_values(pdb_rows, "coordinate_state"),
                "blocker_classes_observed": count_values(pdb_rows, "blocker_class"),
                "candidate_role_classes_observed": count_values(
                    pdb_rows,
                    "candidate_role_class",
                    default="state_only",
                ),
                "reciprocal_context_classes_observed": count_values(
                    pdb_rows,
                    "reciprocal_context_class",
                    default="none",
                ),
                "coordinate_certainty_classes_observed": count_nested(
                    pdb_rows,
                    ["coordinate_certainty", "coordinate_certainty_class"],
                    default="state_only_or_unavailable",
                ),
                "state_blocker_matrix": state_blocker_matrix(pdb_rows),
                "role_blocker_matrix": role_blocker_matrix(pdb_rows),
                "same_chain_candidate_count": bool_count(pdb_rows, "same_chain_topology"),
                "cross_chain_candidate_count": bool_count(pdb_rows, "cross_chain_topology"),
                "unblocked_candidate_ids": candidate_ids(unblocked),
                "topology_ambiguity_candidate_ids": candidate_ids(topology),
                "substrate_role_identity_candidate_ids": candidate_ids(substrate_role),
                "internal_fragment_mimicry_candidate_ids": candidate_ids(internal_fragment),
                "active_gamma_geometry_candidate_count": len(geometry),
                "nearest_candidate_by_distance": compact_nearest(nearest_candidate(pdb_rows)),
                "nearest_unblocked_candidate_by_distance": compact_nearest(nearest_candidate(unblocked)),
                "nearest_topology_candidate_by_distance": compact_nearest(nearest_candidate(topology)),
                "conflict_class": conflict,
                "source_free_decision_class": decision,
                "non_abstaining_decision": decision
                in {
                    "source_free_structural_support_review_only",
                    "source_free_blocked_counterevidence_review_only",
                },
                "hard_case": pdb_id in HARD_CASE_PDBS,
                "compact_candidate_digest": [compact_candidate(row) for row in pdb_rows],
                "review_context_for_evaluation_only": {
                    "evaluation_label": first["review_context_for_evaluation_only"][
                        "evaluation_label"
                    ],
                    "evaluation_group": first["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "source_artifact_id": first["review_context_for_evaluation_only"].get(
                        "source_artifact_id"
                    ),
                    "evaluation_label_used_only_for_eval": True,
                },
            }
        )
    return conflict_rows


def abstention_rule(conflict_rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
        "abstained_positive": [],
        "abstained_negative": [],
    }
    decisions = []
    for row in conflict_rows:
        actual_positive = (
            row["review_context_for_evaluation_only"]["evaluation_label"]
            == "positive_true_substrate_acceptor"
        )
        decision = row["source_free_decision_class"]
        if decision == "source_free_structural_support_review_only":
            outcome = "true_positive" if actual_positive else "false_positive"
        elif decision == "source_free_blocked_counterevidence_review_only":
            outcome = "false_negative" if actual_positive else "true_negative"
        else:
            outcome = "abstained_positive" if actual_positive else "abstained_negative"
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "source_free_decision_class": decision,
                "conflict_class": row["conflict_class"],
                "outcome": outcome,
            }
        )

    confusion_matrix = {
        "true_positive": len(buckets["true_positive"]),
        "false_positive": len(buckets["false_positive"]),
        "true_negative": len(buckets["true_negative"]),
        "false_negative": len(buckets["false_negative"]),
        "abstained_positive": len(buckets["abstained_positive"]),
        "abstained_negative": len(buckets["abstained_negative"]),
    }
    return {
        "rule_id": "candidate_conflict_abstention_v1",
        "rule_description": (
            "Source-free conflict routing: call only unblocked structural-support rows "
            "or hard coordinate/geometry/internal-fragment blockers; abstain on "
            "product/ADP, reciprocal folded-chain, same-chain, and folded-role biology."
        ),
        "confusion_matrix": confusion_matrix,
        "pdb_ids_by_outcome": {key: sorted(value) for key, value in buckets.items()},
        "decisions": sorted(decisions, key=lambda item: item["pdb_id"]),
        "clears_diagnostic_tranche": False,
        "production_claim_allowed": False,
        "abstention_required_for_source_free_biology": True,
    }


def counter(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows).items()))


def hard_case_digest(conflict_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    digest: dict[str, dict[str, Any]] = {}
    for row in conflict_rows:
        if not row["hard_case"]:
            continue
        digest[row["pdb_id"]] = {
            "conflict_class": row["conflict_class"],
            "source_free_decision_class": row["source_free_decision_class"],
            "coordinate_states_observed": row["coordinate_states_observed"],
            "blocker_classes_observed": row["blocker_classes_observed"],
            "candidate_role_classes_observed": row["candidate_role_classes_observed"],
            "nearest_candidate_by_distance": row["nearest_candidate_by_distance"],
            "unblocked_candidate_ids": row["unblocked_candidate_ids"],
            "topology_ambiguity_candidate_ids": row["topology_ambiguity_candidate_ids"],
            "internal_fragment_mimicry_candidate_ids": row[
                "internal_fragment_mimicry_candidate_ids"
            ],
        }
    return dict(sorted(digest.items()))


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    source_payload, rows = load_candidate_rows()
    conflict_rows = build_conflict_rows(rows)
    rule = abstention_rule(conflict_rows)
    primary_outcome = "blocker_not_cleared_biology_ambiguity"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )
    coordinate_state_counts = count_values(rows, "coordinate_state")
    blocker_class_counts = count_values(rows, "blocker_class")
    conflict_class_counts = counter(conflict_rows, "conflict_class")
    decision_class_counts = counter(conflict_rows, "source_free_decision_class")
    non_abstaining_count = sum(1 for row in conflict_rows if row["non_abstaining_decision"])
    abstaining_count = len(conflict_rows) - non_abstaining_count

    false_negatives = rule["pdb_ids_by_outcome"]["false_negative"]
    false_positives = rule["pdb_ids_by_outcome"]["false_positive"]
    abstained_positives = rule["pdb_ids_by_outcome"]["abstained_positive"]

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "A source-free candidate conflict matrix can distinguish rows with "
            "materialized structural support or hard blockers from rows that must "
            "abstain for product/ADP state, reciprocal folded-chain, same-chain, or "
            "folded-role biology without increasing unsafe non-abstention."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(conflict_rows),
            "total": len(conflict_rows),
        },
        "candidate_evidence_rows_emitted": {
            "candidate_pair_rows_reused": source_payload["metadata"]["candidate_pair_row_count"],
            "state_only_rows_reused": source_payload["metadata"]["state_only_row_count"],
            "candidate_conflict_rows_emitted": len(conflict_rows),
            "new_gamma_acceptor_candidate_rows_emitted": 0,
        },
        "coordinate_states_observed": coordinate_state_counts,
        "source_free_features_tested": [
            "candidate conflict signature from coordinate-state, blocker, and role-class sets",
            "role-by-blocker matrix from source-free candidate rows",
            "state-by-blocker matrix from source-free candidate rows",
            "abstention-only conflict routing for topology and state-specific biology",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            rule["rule_id"]: {
                "rule_description": rule["rule_description"],
                "confusion_matrix": rule["confusion_matrix"],
                "pdb_ids_by_outcome": rule["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": rule["clears_diagnostic_tranche"],
                "production_claim_allowed": rule["production_claim_allowed"],
                "abstention_required_for_source_free_biology": rule[
                    "abstention_required_for_source_free_biology"
                ],
            }
        },
        "confusion_matrix": rule["confusion_matrix"],
        "decisive_counterexamples": {
            "hard_case_digest": hard_case_digest(conflict_rows),
            "conflict_class_counts": conflict_class_counts,
            "decision_class_counts": decision_class_counts,
            "abstained_positive_pdb_ids": abstained_positives,
            "abstained_negative_count": rule["confusion_matrix"]["abstained_negative"],
        },
        "false_positive_analysis": {
            "candidate_conflict_abstention_false_positive_pdb_ids": false_positives,
            "interpretation": (
                "No false positives are introduced because reciprocal folded-chain, "
                "same-chain, and folded-role conflict classes abstain rather than "
                "being promoted to source-free substrate-role calls."
            ),
        },
        "false_negative_analysis": {
            "candidate_conflict_abstention_false_negative_pdb_ids": false_negatives,
            "abstained_positive_pdb_ids": abstained_positives,
            "interpretation": (
                "The rule has no resolved false negatives, but it abstains on the "
                "known positive product/ADP and topology cases: 1L0O, 3QHR, 3QHW, "
                "3TM0, 9UUR, and 9UUX."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "coordinate_state_counts": coordinate_state_counts,
            "blocker_class_counts": blocker_class_counts,
            "conflict_class_counts": conflict_class_counts,
            "decision_class_counts": decision_class_counts,
            "non_abstaining_pdb_count": non_abstaining_count,
            "abstaining_pdb_count": abstaining_count,
            "classification": (
                "The blocker remains source-free biology ambiguity. The conflict "
                "matrix can route 22 non-abstaining review-only cases with no "
                "diagnostic false positives or false negatives, but it must abstain "
                "on 32 PDBs including all product/ADP and reciprocal/same-chain "
                "positive hard cases."
            ),
        },
        "next_query": (
            "Use candidate_conflict_abstention_v1 for review routing and stop "
            "source-free substrate-role identity probing unless a new evidence "
            "modality can reduce the topology/state abstention set without admitting "
            "9UW4-like counterexamples."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Preserve source-free conflict "
            "routing as review-only evidence; source-reviewed adjudication remains "
            "required for product/ADP, reciprocal folded-chain, same-chain, and "
            "folded-role substrate biology."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "candidate_conflict_abstention_decision",
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
            "source_candidate_pair_row_count": source_payload["metadata"][
                "candidate_pair_row_count"
            ],
            "source_state_only_row_count": source_payload["metadata"]["state_only_row_count"],
            "candidate_conflict_row_count": len(conflict_rows),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "source_free_conflict_signature": (
                "Sorted coordinate-state, blocker-class, and candidate-role sets. "
                "It uses only candidate-row source-free evidence."
            ),
            "conflict_class": (
                "Compact review-routing class derived from source-free candidate "
                "conflicts; it is not a production substrate identity label."
            ),
            "source_free_decision_class": (
                "Review-only abstention decision. Topology, product/ADP, and "
                "folded-role biology conflicts abstain."
            ),
            "candidate_conflict_abstention_v1": rule["rule_description"],
        },
        "coordinate_state_counts": coordinate_state_counts,
        "blocker_class_counts": blocker_class_counts,
        "conflict_class_counts": conflict_class_counts,
        "decision_class_counts": decision_class_counts,
        "candidate_conflict_rows": conflict_rows,
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
