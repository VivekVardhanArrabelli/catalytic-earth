#!/usr/bin/env python3
"""Audit source-free ePK candidate signature collisions.

This lane-local helper consumes the existing candidate evidence and conflict
decision artifacts. It does not fetch source text or coordinates. The audit
groups candidate rows by categorical source-free structural signatures, then
uses review labels only after grouping to detect positive/counterexample
collisions that force abstention for substrate-role identity.
"""

from __future__ import annotations

import argparse
import hashlib
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


ARTIFACT_ID = "epk_candidate_signature_collision_audit_v1_20260521"
SOURCE_CANDIDATE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
SOURCE_CONFLICT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_conflict_decision_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_signature_collision_audit_v1_20260521.json"
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
    "1L0O",
    "1QHA",
    "3QHR",
    "3QHW",
    "3TM0",
    "7B56",
    "9UUR",
    "9UUX",
    "9UW4",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_candidate_rows() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(SOURCE_CANDIDATE_ARTIFACT.read_text(encoding="utf-8"))
    rows = payload["candidate_evidence_rows"] + payload["state_only_rows"]
    return payload, rows


def load_conflict_rows() -> dict[str, Any]:
    return json.loads(SOURCE_CONFLICT_ARTIFACT.read_text(encoding="utf-8"))


def evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row["source_free_evidence"]


def evaluation_label(row: dict[str, Any]) -> str:
    return row["review_context_for_evaluation_only"]["evaluation_label"]


def is_positive(label: str) -> bool:
    return label == "positive_true_substrate_acceptor"


def count_labels(labels: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(labels).items()))


def distance_transfer_class(value: float | None) -> str:
    if value is None:
        return "no_gamma_acceptor_distance"
    if value <= 6.0:
        return "within_preexisting_transfer_geometry_6a"
    return "outside_preexisting_transfer_geometry_6a"


def chain_size_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_chain_is_short_peptide_like"):
        return "short_peptide_like_acceptor_chain"
    if e.get("acceptor_chain_is_folded_like"):
        return "folded_like_acceptor_chain"
    return "acceptor_chain_size_unclassified"


def acceptor_terminal_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
        return "n_terminal_internal_fragment_like"
    if e.get("acceptor_resolved_n_terminal_auth_terminal_like"):
        return "n_terminal_auth_terminal_like"
    if e.get("acceptor_is_n_terminal_sty"):
        return "resolved_n_terminal_sty_without_auth_terminal_support"
    return "not_resolved_n_terminal_sty"


def acceptor_residue_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_is_tyr"):
        return "tyr_acceptor"
    residue = e.get("acceptor_residue_code")
    if residue in {"SER", "THR"}:
        return "ser_thr_acceptor"
    if residue is None:
        return "no_acceptor_residue"
    return "other_acceptor_residue"


def topology_class(e: dict[str, Any]) -> str:
    if e.get("same_chain_topology"):
        return "same_chain_topology"
    if e.get("cross_chain_topology"):
        return "cross_chain_topology"
    return "no_candidate_topology"


def count_class(value: Any) -> str:
    if value is None:
        return "count_unavailable"
    if value == 0:
        return "zero"
    if value == 1:
        return "one"
    return "multiple"


def nested_value(mapping: dict[str, Any], path: list[str], default: str) -> Any:
    value: Any = mapping
    for key in path:
        if not isinstance(value, dict):
            return default
        value = value.get(key)
    if value is None:
        return default
    return value


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def candidate_signature_fields(row: dict[str, Any]) -> dict[str, Any]:
    e = evidence(row)
    return {
        "coordinate_state": e.get("coordinate_state"),
        "blocker_class": e.get("blocker_class"),
        "candidate_role_class": e.get("candidate_role_class") or "state_only",
        "availability_class": e.get("availability_class"),
        "distance_transfer_class": distance_transfer_class(e.get("distance_angstrom")),
        "topology_class": topology_class(e),
        "reciprocal_context_class": e.get("reciprocal_context_class") or "no_reciprocal_context",
        "acceptor_residue_class": acceptor_residue_class(e),
        "acceptor_terminal_class": acceptor_terminal_class(e),
        "acceptor_chain_size_class": chain_size_class(e),
        "ligand_acceptor_same_sequence_entity": e.get("ligand_acceptor_same_sequence_entity"),
        "candidate_chain_has_own_nucleotide_or_metal": e.get(
            "candidate_chain_has_own_nucleotide_or_metal"
        ),
        "candidate_chain_active_gamma_count_class": count_class(
            e.get("candidate_chain_active_gamma_count")
        ),
        "ligand_chain_active_gamma_count_class": count_class(
            e.get("ligand_chain_active_gamma_count")
        ),
        "orientation_support_class": nested_value(
            e,
            ["orientation", "orientation_support_class"],
            "orientation_unavailable",
        ),
        "local_exposure_profile_class": nested_value(
            e,
            ["exposure", "local_exposure_profile_class"],
            "exposure_unavailable",
        ),
        "coordinate_certainty_class": nested_value(
            e,
            ["coordinate_certainty", "coordinate_certainty_class"],
            "coordinate_certainty_unavailable",
        ),
    }


def candidate_signature_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signature_rows = []
    for row in rows:
        fields = candidate_signature_fields(row)
        signature_rows.append(
            {
                "row_schema": "epk_source_free_candidate_signature_collision_v1",
                "candidate_id": row["candidate_id"],
                "pdb_id": row["pdb_id"],
                "source_free_candidate_signature_id": stable_signature_id(fields),
                "source_free_candidate_signature_fields": fields,
                "source_free_evidence_digest": {
                    "coordinate_state": fields["coordinate_state"],
                    "blocker_class": fields["blocker_class"],
                    "candidate_role_class": fields["candidate_role_class"],
                    "distance_transfer_class": fields["distance_transfer_class"],
                    "topology_class": fields["topology_class"],
                    "reciprocal_context_class": fields["reciprocal_context_class"],
                    "orientation_support_class": fields["orientation_support_class"],
                    "local_exposure_profile_class": fields["local_exposure_profile_class"],
                    "coordinate_certainty_class": fields["coordinate_certainty_class"],
                },
                "review_context_for_evaluation_only": {
                    "evaluation_label": evaluation_label(row),
                    "evaluation_group": row["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "evaluation_label_used_only_after_signature_grouping": True,
                },
            }
        )
    return signature_rows


def group_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return dict(sorted(grouped.items()))


def collision_class(labels: list[str]) -> str:
    positives = sum(1 for label in labels if is_positive(label))
    negatives = len(labels) - positives
    if positives and negatives:
        return "mixed_positive_counterexample_signature"
    if positives:
        return "positive_only_signature"
    return "counterexample_only_signature"


def collision_group_rows(signature_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    for signature_id, rows in group_by_key(
        signature_rows,
        "source_free_candidate_signature_id",
    ).items():
        labels = [
            row["review_context_for_evaluation_only"]["evaluation_label"]
            for row in rows
        ]
        pdb_ids = sorted({row["pdb_id"] for row in rows})
        groups.append(
            {
                "row_schema": "epk_source_free_candidate_signature_group_v1",
                "source_free_candidate_signature_id": signature_id,
                "source_free_candidate_signature_fields": rows[0][
                    "source_free_candidate_signature_fields"
                ],
                "candidate_row_count": len(rows),
                "pdb_count": len(pdb_ids),
                "pdb_ids": pdb_ids,
                "candidate_ids": sorted(row["candidate_id"] for row in rows),
                "hard_case_pdb_ids": sorted(set(pdb_ids) & HARD_CASE_PDBS),
                "collision_class_for_evaluation_only": collision_class(labels),
                "review_label_counts_for_evaluation_only": count_labels(labels),
            }
        )
    return sorted(
        groups,
        key=lambda row: (
            row["collision_class_for_evaluation_only"] != "mixed_positive_counterexample_signature",
            -row["candidate_row_count"],
            row["source_free_candidate_signature_id"],
        ),
    )


def rows_by_pdb(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["pdb_id"]].append(row)
    return dict(sorted(grouped.items()))


def pdb_signature_fields(
    row: dict[str, Any],
    source_rows_by_pdb: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    source_rows = source_rows_by_pdb.get(row["pdb_id"], [])
    return {
        "coordinate_state_set": sorted(row["coordinate_states_observed"]),
        "blocker_class_set": sorted(row["blocker_classes_observed"]),
        "candidate_role_class_set": sorted(row["candidate_role_classes_observed"]),
        "reciprocal_context_class_set": sorted(row["reciprocal_context_classes_observed"]),
        "coordinate_certainty_class_set": sorted(row["coordinate_certainty_classes_observed"]),
        "orientation_support_class_set": sorted(
            {
                nested_value(
                    evidence(candidate),
                    ["orientation", "orientation_support_class"],
                    "orientation_unavailable",
                )
                for candidate in source_rows
            }
        ),
        "local_exposure_profile_class_set": sorted(
            {
                nested_value(
                    evidence(candidate),
                    ["exposure", "local_exposure_profile_class"],
                    "exposure_unavailable",
                )
                for candidate in source_rows
            }
        ),
        "conflict_class": row["conflict_class"],
        "source_free_decision_class": row["source_free_decision_class"],
    }


def pdb_signature_rows(
    conflict_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_rows_by_pdb = rows_by_pdb(source_rows)
    rows = []
    for row in conflict_rows:
        fields = pdb_signature_fields(row, source_rows_by_pdb)
        rows.append(
            {
                "row_schema": "epk_source_free_pdb_signature_collision_v1",
                "pdb_id": row["pdb_id"],
                "source_free_pdb_signature_id": stable_signature_id(fields),
                "source_free_pdb_signature_fields": fields,
                "conflict_class": row["conflict_class"],
                "source_free_decision_class": row["source_free_decision_class"],
                "hard_case": row["hard_case"],
                "review_context_for_evaluation_only": {
                    "evaluation_label": row["review_context_for_evaluation_only"][
                        "evaluation_label"
                    ],
                    "evaluation_group": row["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "evaluation_label_used_only_after_signature_grouping": True,
                },
            }
        )
    return rows


def pdb_collision_group_rows(signature_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    for signature_id, rows in group_by_key(rows=signature_rows, key="source_free_pdb_signature_id").items():
        labels = [
            row["review_context_for_evaluation_only"]["evaluation_label"]
            for row in rows
        ]
        pdb_ids = sorted(row["pdb_id"] for row in rows)
        groups.append(
            {
                "row_schema": "epk_source_free_pdb_signature_group_v1",
                "source_free_pdb_signature_id": signature_id,
                "source_free_pdb_signature_fields": rows[0][
                    "source_free_pdb_signature_fields"
                ],
                "pdb_count": len(rows),
                "pdb_ids": pdb_ids,
                "hard_case_pdb_ids": sorted(set(pdb_ids) & HARD_CASE_PDBS),
                "collision_class_for_evaluation_only": collision_class(labels),
                "review_label_counts_for_evaluation_only": count_labels(labels),
            }
        )
    return sorted(
        groups,
        key=lambda row: (
            row["collision_class_for_evaluation_only"] != "mixed_positive_counterexample_signature",
            -row["pdb_count"],
            row["source_free_pdb_signature_id"],
        ),
    )


def label_counts_for_rows(rows: list[dict[str, Any]]) -> dict[str, int]:
    return count_labels(
        [row["review_context_for_evaluation_only"]["evaluation_label"] for row in rows]
    )


def confusion_from_conflict_decisions(conflict_rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
        "abstained_positive": [],
        "abstained_negative": [],
    }
    for row in conflict_rows:
        actual_positive = is_positive(
            row["review_context_for_evaluation_only"]["evaluation_label"]
        )
        decision = row["source_free_decision_class"]
        if decision == "source_free_structural_support_review_only":
            outcome = "true_positive" if actual_positive else "false_positive"
        elif decision == "source_free_blocked_counterevidence_review_only":
            outcome = "false_negative" if actual_positive else "true_negative"
        else:
            outcome = "abstained_positive" if actual_positive else "abstained_negative"
        buckets[outcome].append(row["pdb_id"])
    return {
        "confusion_matrix": {key: len(value) for key, value in buckets.items()},
        "pdb_ids_by_outcome": {key: sorted(value) for key, value in buckets.items()},
    }


def mixed_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        group
        for group in groups
        if group["collision_class_for_evaluation_only"]
        == "mixed_positive_counterexample_signature"
    ]


def mixed_candidate_groups_by_blocker(
    groups: list[dict[str, Any]],
) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for group in mixed_groups(groups):
        blocker = group["source_free_candidate_signature_fields"]["blocker_class"]
        counter[str(blocker)] += 1
    return dict(sorted(counter.items()))


def mixed_group_count_for_blocker(groups: list[dict[str, Any]], blocker: str) -> int:
    return sum(
        1
        for group in mixed_groups(groups)
        if group["source_free_candidate_signature_fields"]["blocker_class"] == blocker
    )


def hard_case_collision_digest(
    candidate_groups: list[dict[str, Any]],
    pdb_groups: list[dict[str, Any]],
) -> dict[str, Any]:
    hard_candidate_groups = [
        group
        for group in mixed_groups(candidate_groups)
        if set(group["hard_case_pdb_ids"]) & HARD_CASE_PDBS
    ]
    hard_pdb_groups = [
        group
        for group in mixed_groups(pdb_groups)
        if set(group["hard_case_pdb_ids"]) & HARD_CASE_PDBS
    ]
    return {
        "mixed_candidate_signature_hard_case_groups": hard_candidate_groups[:12],
        "mixed_pdb_signature_hard_case_groups": hard_pdb_groups[:12],
        "interpretation": (
            "Hard-case positive and counterexample rows share source-free "
            "structural signatures, including reciprocal folded-chain and "
            "same-chain topology contexts. Promoting those signatures would "
            "admit 9UW4-like counterexamples."
        ),
    }


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    source_payload, rows = load_candidate_rows()
    conflict_payload = load_conflict_rows()
    conflict_rows = conflict_payload["candidate_conflict_rows"]
    candidate_rows = candidate_signature_rows(rows)
    candidate_groups = collision_group_rows(candidate_rows)
    pdb_rows = pdb_signature_rows(conflict_rows, rows)
    pdb_groups = pdb_collision_group_rows(pdb_rows)
    rule_eval = confusion_from_conflict_decisions(conflict_rows)

    primary_outcome = "blocker_not_cleared_biology_ambiguity"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    mixed_candidate_groups = mixed_groups(candidate_groups)
    mixed_pdb_groups = mixed_groups(pdb_groups)
    mixed_candidate_row_count = sum(
        group["candidate_row_count"] for group in mixed_candidate_groups
    )
    mixed_unblocked_group_count = mixed_group_count_for_blocker(candidate_groups, "none")
    mixed_topology_group_count = mixed_group_count_for_blocker(
        candidate_groups,
        "topology_ambiguity",
    )
    mixed_candidate_pdbs = sorted(
        {
            pdb_id
            for group in mixed_candidate_groups
            for pdb_id in group["pdb_ids"]
        }
    )
    mixed_pdb_signature_pdbs = sorted(
        {pdb_id for group in mixed_pdb_groups for pdb_id in group["pdb_ids"]}
    )

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "If categorical source-free candidate signatures collide between "
            "known positives and counterexamples, then coordinate certainty, "
            "orientation, exposure, reciprocal context, topology, and coordinate "
            "state cannot safely reduce the topology/state abstention set without "
            "source-reviewed biology."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": len(rows),
            "reused_from_conflict_decision_artifact": len(conflict_rows),
            "total_pdbs_reused": len(conflict_rows),
        },
        "candidate_evidence_rows_emitted": {
            "source_free_candidate_signature_rows_emitted": len(candidate_rows),
            "source_free_candidate_signature_group_rows_emitted": len(candidate_groups),
            "source_free_pdb_signature_rows_emitted": len(pdb_rows),
            "source_free_pdb_signature_group_rows_emitted": len(pdb_groups),
            "candidate_pair_rows_reused": source_payload["metadata"][
                "candidate_pair_row_count"
            ],
            "state_only_rows_reused": source_payload["metadata"]["state_only_row_count"],
        },
        "coordinate_states_observed": conflict_payload["coordinate_state_counts"],
        "source_free_features_tested": [
            "categorical candidate signature collision audit",
            "coordinate state plus blocker class grouping",
            "topology and reciprocal context grouping",
            "orientation support class grouping",
            "local exposure profile grouping",
            "coordinate certainty class grouping",
            "preexisting 6A transfer-geometry distance class grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "source_free_signature_collision_audit_v1": {
                "rule_id": "source_free_signature_collision_audit_v1",
                "rule_description": (
                    "Audit-only grouping by source-free categorical structural "
                    "signatures; review labels are used only after grouping to "
                    "detect collisions, not as predictive inputs."
                ),
                "candidate_signature_group_count": len(candidate_groups),
                "mixed_candidate_signature_group_count": len(mixed_candidate_groups),
                "mixed_candidate_signature_row_count": mixed_candidate_row_count,
                "mixed_candidate_signature_pdb_count": len(mixed_candidate_pdbs),
                "mixed_unblocked_none_blocker_signature_group_count": (
                    mixed_unblocked_group_count
                ),
                "mixed_topology_ambiguity_signature_group_count": (
                    mixed_topology_group_count
                ),
                "pdb_signature_group_count": len(pdb_groups),
                "mixed_pdb_signature_group_count": len(mixed_pdb_groups),
                "mixed_pdb_signature_pdb_count": len(mixed_pdb_signature_pdbs),
                "mixed_candidate_groups_by_blocker_class": mixed_candidate_groups_by_blocker(
                    candidate_groups
                ),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
                "abstention_required_for_source_free_biology": True,
            },
            "candidate_conflict_abstention_v1_reused_for_comparison": {
                "rule_id": "candidate_conflict_abstention_v1_reused_for_comparison",
                "rule_description": (
                    "Previously emitted review-only conflict routing reused as "
                    "comparison; topology and state-specific biology abstain."
                ),
                "confusion_matrix": rule_eval["confusion_matrix"],
                "pdb_ids_by_outcome": rule_eval["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": rule_eval["confusion_matrix"],
        "decisive_counterexamples": {
            "mixed_candidate_signature_pdb_ids": mixed_candidate_pdbs,
            "mixed_pdb_signature_pdb_ids": mixed_pdb_signature_pdbs,
            "hard_case_collision_digest": hard_case_collision_digest(
                candidate_groups,
                pdb_groups,
            ),
            "9UW4_collision_role": (
                "9UW4 remains a decisive topology counterexample because its "
                "reciprocal folded-chain Tyr candidate and same-chain topology "
                "candidates collide with positive 9UUR/9UUX source-free "
                "signatures."
            ),
        },
        "false_positive_analysis": {
            "candidate_conflict_abstention_false_positive_pdb_ids": rule_eval[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "interpretation": (
                "No additional false positives are introduced because mixed "
                "topology signatures are audit blockers and remain abstained."
            ),
        },
        "false_negative_analysis": {
            "candidate_conflict_abstention_false_negative_pdb_ids": rule_eval[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "abstained_positive_pdb_ids": rule_eval["pdb_ids_by_outcome"][
                "abstained_positive"
            ],
            "interpretation": (
                "Remaining positives are abstained rather than false negatives: "
                "product/ADP rows lack active gamma transfer geometry, and "
                "reciprocal or same-chain topology positives collide with "
                "counterexample signatures."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "mixed_candidate_signature_group_count": len(mixed_candidate_groups),
            "mixed_candidate_signature_row_count": mixed_candidate_row_count,
            "mixed_candidate_signature_pdb_count": len(mixed_candidate_pdbs),
            "mixed_unblocked_none_blocker_signature_group_count": (
                mixed_unblocked_group_count
            ),
            "mixed_topology_ambiguity_signature_group_count": mixed_topology_group_count,
            "mixed_candidate_groups_by_blocker_class": mixed_candidate_groups_by_blocker(
                candidate_groups
            ),
            "mixed_pdb_signature_group_count": len(mixed_pdb_groups),
            "mixed_pdb_signature_pdb_count": len(mixed_pdb_signature_pdbs),
            "interpretation": (
                "Candidate-level source-free structural signatures are not unique "
                "to true substrate-role positives. The mixed topology signatures "
                "make source-free de-abstention unsafe without source-reviewed "
                "biology."
            ),
        },
        "next_query": (
            "Do not run another scalar source-free rescue on this tranche. Only "
            "resume if a genuinely new evidence modality can separate mixed "
            "topology signatures, especially 9UUR/9UUX versus 9UW4, without "
            "using source text or candidate-specific thresholds."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep candidate evidence and signature collision rows as review-only "
            "blocker evidence. Do not claim ePK production readiness, import "
            "labels, calibrate thresholds, or promote topology/state conflicts "
            "into production substrate-role calls."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "source_free_candidate_signature_collision_audit",
            "review_only": True,
            "source_free_evidence_separated_from_review_context": True,
            "source_labels_used_only_after_signature_grouping": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_candidate_artifact": str(SOURCE_CANDIDATE_ARTIFACT),
            "source_conflict_artifact": str(SOURCE_CONFLICT_ARTIFACT),
            "output_path": str(output_path),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "source_free_candidate_signature_fields": (
                "Categorical coordinate-state, blocker, topology, reciprocal, "
                "orientation, exposure, and coordinate-certainty features. The "
                "only distance bucket is the preexisting 6A transfer-geometry "
                "class already used by earlier lane evidence."
            ),
            "mixed_positive_counterexample_signature": (
                "A source-free signature group containing at least one review-only "
                "positive and at least one review-only counterexample after "
                "signature grouping."
            ),
            "collision_audit_scope": (
                "Review-only blocker evidence. It is not a production rule and "
                "does not use labels as predictive inputs."
            ),
        },
        "source_free_candidate_signature_rows": candidate_rows,
        "source_free_candidate_signature_groups": candidate_groups,
        "source_free_pdb_signature_rows": pdb_rows,
        "source_free_pdb_signature_groups": pdb_groups,
        "summary": {
            "candidate_signature_group_count": len(candidate_groups),
            "mixed_candidate_signature_group_count": len(mixed_candidate_groups),
            "mixed_candidate_signature_row_count": mixed_candidate_row_count,
            "mixed_candidate_signature_pdb_count": len(mixed_candidate_pdbs),
            "mixed_unblocked_none_blocker_signature_group_count": (
                mixed_unblocked_group_count
            ),
            "mixed_topology_ambiguity_signature_group_count": mixed_topology_group_count,
            "pdb_signature_group_count": len(pdb_groups),
            "mixed_pdb_signature_group_count": len(mixed_pdb_groups),
            "mixed_pdb_signature_pdb_count": len(mixed_pdb_signature_pdbs),
            "mixed_candidate_groups_by_blocker_class": mixed_candidate_groups_by_blocker(
                candidate_groups
            ),
            "candidate_signature_label_counts": label_counts_for_rows(candidate_rows),
            "pdb_signature_label_counts": label_counts_for_rows(pdb_rows),
        },
        "rules": list(run_record["rule_results"].values()),
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
