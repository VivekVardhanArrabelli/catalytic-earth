#!/usr/bin/env python3
"""Emit candidate-level materiality rows for ePK substrate-role blockers.

This lane-local helper projects the existing source-free gamma/acceptor
candidate table onto the existing PDB-level abstention decisions. It does not
introduce a new scalar rescue rule; it makes explicit which candidate rows
drive support, counterevidence, topology abstention, or state-specific
abstention.
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
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_candidate_materiality_manifest_v1_20260521"
SOURCE_EVIDENCE_ARTIFACT = Path(
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
    "epk_candidate_materiality_manifest_v1_20260521.json"
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

STATE_ABSTENTION_STATES = {"product_state", "adp_state"}
MATERIALIZATION_STATES = {
    "ligand_absent",
    "ambiguous_coordinate_state",
    "unavailable_coordinate_state",
    "metal_absent",
    "split_state",
    "substrate_acceptor_analog_state",
}
NON_ABSTAINING_DECISIONS = {
    "source_free_structural_support_review_only",
    "source_free_blocked_counterevidence_review_only",
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


def load_sources() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    evidence_payload = json.loads(SOURCE_EVIDENCE_ARTIFACT.read_text(encoding="utf-8"))
    conflict_payload = json.loads(SOURCE_CONFLICT_ARTIFACT.read_text(encoding="utf-8"))
    rows = evidence_payload["candidate_evidence_rows"] + evidence_payload["state_only_rows"]
    return evidence_payload, conflict_payload, rows


def evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row["source_free_evidence"]


def count_values(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(evidence(row).get(key)) for row in rows).items()))


def counter(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows).items()))


def conflict_map(conflict_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["pdb_id"]: row
        for row in conflict_payload["candidate_conflict_rows"]
    }


def coord_certainty_class(source_free_evidence: dict[str, Any]) -> str | None:
    certainty = source_free_evidence.get("coordinate_certainty")
    if not isinstance(certainty, dict):
        return None
    return certainty.get("coordinate_certainty_class")


def local_exposure_class(source_free_evidence: dict[str, Any]) -> str | None:
    exposure = source_free_evidence.get("exposure")
    if not isinstance(exposure, dict):
        return None
    return exposure.get("local_exposure_profile_class")


def orientation_class(source_free_evidence: dict[str, Any]) -> str | None:
    orientation = source_free_evidence.get("orientation")
    if not isinstance(orientation, dict):
        return None
    return orientation.get("orientation_support_class")


def materiality_class(
    row: dict[str, Any],
    conflict_row: dict[str, Any],
) -> tuple[str, str]:
    row_evidence = evidence(row)
    blocker = row_evidence.get("blocker_class")
    state = row_evidence.get("coordinate_state")
    decision = conflict_row["source_free_decision_class"]

    if state in STATE_ABSTENTION_STATES:
        return (
            "material_state_abstention_driver",
            "Product/ADP state lacks terminal-gamma transfer geometry.",
        )
    if state in MATERIALIZATION_STATES:
        return (
            "material_coordinate_materialization_driver",
            "Ligand or coordinate materialization blocks active-gamma adjudication.",
        )
    if decision == "source_free_structural_support_review_only":
        if blocker == "none":
            return (
                "material_unblocked_structural_support",
                "Active-gamma candidate has no source-free blocker.",
            )
        if blocker in {"topology_ambiguity", "substrate_role_identity"}:
            return (
                "competing_ambiguous_candidate_nonfatal",
                "An unblocked candidate exists in the same PDB, so this ambiguity is nonfatal for review routing.",
            )
        return (
            "competing_blocked_candidate_nonfatal",
            "An unblocked candidate exists in the same PDB, so this blocked row is nonfatal for review routing.",
        )
    if decision == "source_free_blocked_counterevidence_review_only":
        if blocker == "internal_fragment_mimicry":
            return (
                "material_internal_fragment_counterevidence",
                "Auth-terminal-looking acceptor is an internal-fragment mimic.",
            )
        if blocker == "active_gamma_geometry":
            return (
                "material_active_gamma_geometry_counterevidence",
                "Active gamma is present but no transfer-compatible candidate is materialized.",
            )
        return (
            "material_blocked_counterevidence",
            "Source-free blocker supports review-only negative counterevidence.",
        )
    if decision == "abstain_state_specific_review_required":
        return (
            "material_state_specific_abstention",
            "State-specific evidence requires review-only abstention.",
        )
    if decision == "abstain_biology_topology_review_required":
        if blocker == "topology_ambiguity":
            return (
                "material_topology_abstention_driver",
                "Same-chain or reciprocal folded-chain topology leaves substrate role ambiguous.",
            )
        if blocker == "substrate_role_identity":
            return (
                "material_substrate_role_abstention_driver",
                "Folded cross-chain context leaves biological substrate role ambiguous.",
            )
        if blocker == "active_gamma_geometry":
            return (
                "secondary_geometry_within_topology_abstention",
                "Geometry is blocked, but topology ambiguity is the PDB-level abstention driver.",
            )
        return (
            "secondary_candidate_within_topology_abstention",
            "PDB-level source-free decision abstains for topology or substrate-role biology.",
        )
    return (
        "material_mixed_review_abstention",
        "Mixed source-free evidence requires review-only abstention.",
    )


def compact_source_free_evidence(row: dict[str, Any]) -> dict[str, Any]:
    row_evidence = evidence(row)
    return {
        "availability_class": row_evidence.get("availability_class"),
        "coordinate_state": row_evidence.get("coordinate_state"),
        "blocker_class": row_evidence.get("blocker_class"),
        "ligand_state": row_evidence.get("ligand_state"),
        "terminal_gamma_atom": row_evidence.get("terminal_gamma_atom"),
        "acceptor_atom": row_evidence.get("acceptor_atom"),
        "distance_angstrom": row_evidence.get("distance_angstrom"),
        "candidate_role_class": row_evidence.get("candidate_role_class"),
        "reciprocal_context_class": row_evidence.get("reciprocal_context_class"),
        "same_chain_topology": row_evidence.get("same_chain_topology"),
        "cross_chain_topology": row_evidence.get("cross_chain_topology"),
        "ligand_acceptor_same_sequence_entity": row_evidence.get(
            "ligand_acceptor_same_sequence_entity"
        ),
        "acceptor_residue_code": row_evidence.get("acceptor_residue_code"),
        "acceptor_auth_seq_id_int": row_evidence.get("acceptor_auth_seq_id_int"),
        "acceptor_residue_ordinal_in_chain": row_evidence.get(
            "acceptor_residue_ordinal_in_chain"
        ),
        "acceptor_auth_seq_minus_resolved_ordinal": row_evidence.get(
            "acceptor_auth_seq_minus_resolved_ordinal"
        ),
        "acceptor_chain_length": row_evidence.get("acceptor_chain_length"),
        "acceptor_chain_is_folded_like": row_evidence.get("acceptor_chain_is_folded_like"),
        "acceptor_chain_is_short_peptide_like": row_evidence.get(
            "acceptor_chain_is_short_peptide_like"
        ),
        "acceptor_is_n_terminal_sty": row_evidence.get("acceptor_is_n_terminal_sty"),
        "acceptor_is_tyr": row_evidence.get("acceptor_is_tyr"),
        "acceptor_resolved_n_terminal_auth_terminal_like": row_evidence.get(
            "acceptor_resolved_n_terminal_auth_terminal_like"
        ),
        "acceptor_resolved_n_terminal_internal_fragment_like": row_evidence.get(
            "acceptor_resolved_n_terminal_internal_fragment_like"
        ),
        "candidate_chain_has_own_nucleotide_or_metal": row_evidence.get(
            "candidate_chain_has_own_nucleotide_or_metal"
        ),
        "candidate_chain_active_gamma_count": row_evidence.get(
            "candidate_chain_active_gamma_count"
        ),
        "ligand_chain_active_gamma_count": row_evidence.get(
            "ligand_chain_active_gamma_count"
        ),
        "candidate_count_within_8a": row_evidence.get("candidate_count_within_8a"),
        "nearest_protein_hydroxyl_distance_angstrom": row_evidence.get(
            "nearest_protein_hydroxyl_distance_angstrom"
        ),
        "terminal_gamma_equivalent_atom_available": row_evidence.get(
            "terminal_gamma_equivalent_atom_available"
        ),
        "coordinate_certainty_class": coord_certainty_class(row_evidence),
        "local_exposure_profile_class": local_exposure_class(row_evidence),
        "orientation_support_class": orientation_class(row_evidence),
    }


def build_materiality_rows(
    rows: list[dict[str, Any]],
    conflicts_by_pdb: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    materiality_rows: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: (item["pdb_id"], item["candidate_id"])):
        pdb_id = row["pdb_id"]
        conflict_row = conflicts_by_pdb[pdb_id]
        materiality, reason = materiality_class(row, conflict_row)
        source_free_context = {
            "source_free_conflict_signature": conflict_row[
                "source_free_conflict_signature"
            ],
            "conflict_class": conflict_row["conflict_class"],
            "source_free_decision_class": conflict_row["source_free_decision_class"],
            "non_abstaining_decision": conflict_row["non_abstaining_decision"],
            "pdb_candidate_pair_row_count": conflict_row["candidate_pair_row_count"],
            "pdb_state_only_row_count": conflict_row["state_only_row_count"],
            "pdb_unblocked_candidate_count": len(conflict_row["unblocked_candidate_ids"]),
            "pdb_topology_ambiguity_candidate_count": len(
                conflict_row["topology_ambiguity_candidate_ids"]
            ),
            "pdb_internal_fragment_mimicry_candidate_count": len(
                conflict_row["internal_fragment_mimicry_candidate_ids"]
            ),
        }
        materiality_rows.append(
            {
                "row_schema": "epk_candidate_materiality_manifest_v1",
                "candidate_id": row["candidate_id"],
                "pdb_id": pdb_id,
                "candidate_rank_within_8a": row.get("candidate_rank_within_8a"),
                "diagnostic_row_index": row.get("diagnostic_row_index"),
                "candidate_row_kind": (
                    "state_only"
                    if row["row_schema"].endswith("_state_only")
                    else "gamma_acceptor_candidate"
                ),
                "candidate_materiality_class": materiality,
                "candidate_materiality_reason": reason,
                "hard_case": pdb_id in HARD_CASE_PDBS,
                "source_free_evidence": compact_source_free_evidence(row),
                "source_free_pdb_context": source_free_context,
                "review_context_for_evaluation_only": {
                    "evaluation_label": row["review_context_for_evaluation_only"][
                        "evaluation_label"
                    ],
                    "evaluation_group": row["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "source_artifact_id": row["review_context_for_evaluation_only"].get(
                        "source_artifact_id"
                    ),
                    "evaluation_label_used_only_for_eval": True,
                },
            }
        )
    return materiality_rows


def materiality_rule(
    conflict_payload: dict[str, Any],
    materiality_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    prior_rule = conflict_payload["rules"][0]
    materiality_counts = counter(materiality_rows, "candidate_materiality_class")
    return {
        "rule_id": "candidate_materiality_projection_v1",
        "rule_description": (
            "Project each source-free candidate row onto the existing conflict "
            "abstention decision to identify support, counterevidence, topology "
            "abstention, and state-specific abstention drivers. This is review "
            "routing only and makes no production substrate-role call."
        ),
        "confusion_matrix": prior_rule["confusion_matrix"],
        "pdb_ids_by_outcome": prior_rule["pdb_ids_by_outcome"],
        "candidate_materiality_class_counts": materiality_counts,
        "clears_diagnostic_tranche": False,
        "production_claim_allowed": False,
        "new_threshold_or_rescue_rule_added": False,
    }


def hard_case_digest(materiality_rows: list[dict[str, Any]]) -> dict[str, Any]:
    digest: dict[str, Any] = {}
    for row in materiality_rows:
        if not row["hard_case"]:
            continue
        pdb_digest = digest.setdefault(
            row["pdb_id"],
            {
                "candidate_materiality_classes": Counter(),
                "coordinate_states": Counter(),
                "blocker_classes": Counter(),
                "candidate_ids_by_materiality": {},
            },
        )
        pdb_digest["candidate_materiality_classes"][row["candidate_materiality_class"]] += 1
        pdb_digest["coordinate_states"][row["source_free_evidence"]["coordinate_state"]] += 1
        pdb_digest["blocker_classes"][row["source_free_evidence"]["blocker_class"]] += 1
        pdb_digest["candidate_ids_by_materiality"].setdefault(
            row["candidate_materiality_class"],
            [],
        ).append(row["candidate_id"])

    compact_digest = {}
    for pdb_id, row in sorted(digest.items()):
        compact_digest[pdb_id] = {
            "candidate_materiality_classes": dict(
                sorted(row["candidate_materiality_classes"].items())
            ),
            "coordinate_states": dict(sorted(row["coordinate_states"].items())),
            "blocker_classes": dict(sorted(row["blocker_classes"].items())),
            "candidate_ids_by_materiality": {
                key: sorted(value)
                for key, value in sorted(row["candidate_ids_by_materiality"].items())
            },
        }
    return compact_digest


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    evidence_payload, conflict_payload, source_rows = load_sources()
    conflicts_by_pdb = conflict_map(conflict_payload)
    materiality_rows = build_materiality_rows(source_rows, conflicts_by_pdb)
    rule = materiality_rule(conflict_payload, materiality_rows)
    primary_outcome = "candidate_evidence_rows_emitted"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )
    coordinate_state_counts = count_values(source_rows, "coordinate_state")
    blocker_class_counts = count_values(source_rows, "blocker_class")
    materiality_class_counts = counter(materiality_rows, "candidate_materiality_class")
    decision_class_counts = conflict_payload["decision_class_counts"]
    conflict_class_counts = conflict_payload["conflict_class_counts"]
    rule_matrix = rule["confusion_matrix"]
    abstention_driver_count = sum(
        count
        for key, count in materiality_class_counts.items()
        if "abstention" in key
    )

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "Projecting candidate rows onto the existing source-free conflict "
            "abstention decision can make row-level support and blocker materiality "
            "first-class without adding unsafe non-abstention or a post-hoc scalar rule."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": conflict_payload["metadata"][
                "candidate_conflict_row_count"
            ],
            "total": conflict_payload["metadata"]["candidate_conflict_row_count"],
        },
        "candidate_evidence_rows_emitted": {
            "candidate_pair_rows_reused": evidence_payload["metadata"][
                "candidate_pair_row_count"
            ],
            "state_only_rows_reused": evidence_payload["metadata"]["state_only_row_count"],
            "candidate_materiality_rows_emitted": len(materiality_rows),
            "new_gamma_acceptor_candidate_rows_emitted": 0,
        },
        "coordinate_states_observed": coordinate_state_counts,
        "source_free_features_tested": [
            "candidate-level materiality projection from existing source-free blockers",
            "candidate-level inheritance of PDB conflict abstention class",
            "hard-case row grouping for topology/state/internal-fragment blockers",
            "no new scalar split, rescue threshold, or candidate-specific tuning",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            rule["rule_id"]: {
                "rule_description": rule["rule_description"],
                "confusion_matrix": rule["confusion_matrix"],
                "pdb_ids_by_outcome": rule["pdb_ids_by_outcome"],
                "candidate_materiality_class_counts": rule[
                    "candidate_materiality_class_counts"
                ],
                "clears_diagnostic_tranche": rule["clears_diagnostic_tranche"],
                "production_claim_allowed": rule["production_claim_allowed"],
                "new_threshold_or_rescue_rule_added": rule[
                    "new_threshold_or_rescue_rule_added"
                ],
            }
        },
        "confusion_matrix": rule_matrix,
        "decisive_counterexamples": {
            "hard_case_digest": hard_case_digest(materiality_rows),
            "materiality_class_counts": materiality_class_counts,
            "conflict_class_counts": conflict_class_counts,
            "decision_class_counts": decision_class_counts,
            "abstained_positive_pdb_ids": rule["pdb_ids_by_outcome"][
                "abstained_positive"
            ],
            "abstained_negative_count": rule_matrix["abstained_negative"],
        },
        "false_positive_analysis": {
            "candidate_materiality_projection_false_positive_pdb_ids": rule[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "interpretation": (
                "No false positives are introduced because the manifest inherits "
                "the prior abstention routing and does not promote topology/state "
                "rows to source-free substrate-role calls."
            ),
        },
        "false_negative_analysis": {
            "candidate_materiality_projection_false_negative_pdb_ids": rule[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "abstained_positive_pdb_ids": rule["pdb_ids_by_outcome"][
                "abstained_positive"
            ],
            "interpretation": (
                "Resolved false negatives remain zero under the review-only "
                "projection, but product/ADP positives and topology positives stay "
                "abstained because candidate materiality still cannot assign "
                "biological substrate role source-free."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "coordinate_state_counts": coordinate_state_counts,
            "blocker_class_counts": blocker_class_counts,
            "materiality_class_counts": materiality_class_counts,
            "abstention_driver_row_count": abstention_driver_count,
            "classification": (
                "Candidate evidence rows were emitted with first-class materiality, "
                "but the blocker is not cleared. Source-free rows still require "
                "state-specific or topology abstention for the known product/ADP, "
                "reciprocal folded-chain, and same-chain hard cases."
            ),
        },
        "next_query": (
            "Use the candidate materiality manifest for review routing; stop "
            "source-free substrate-role identity probing unless a new evidence "
            "modality can reduce state/topology abstentions without admitting "
            "9UW4-like counterexamples."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Treat the materiality manifest "
            "as source-free review evidence only; source-reviewed adjudication "
            "remains required for product/ADP and topology substrate biology."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "candidate_materiality_manifest",
            "review_only": True,
            "source_free_evidence_separated_from_review_context": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_evidence_artifact": str(SOURCE_EVIDENCE_ARTIFACT),
            "source_conflict_artifact": str(SOURCE_CONFLICT_ARTIFACT),
            "output_path": str(output_path),
            "candidate_materiality_row_count": len(materiality_rows),
            "source_candidate_pair_row_count": evidence_payload["metadata"][
                "candidate_pair_row_count"
            ],
            "source_state_only_row_count": evidence_payload["metadata"][
                "state_only_row_count"
            ],
            "diagnostic_pdb_count": conflict_payload["metadata"][
                "candidate_conflict_row_count"
            ],
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "candidate_materiality_class": (
                "Source-free review-routing materiality assigned from the candidate "
                "blocker and the PDB-level abstention decision. It is not a "
                "production substrate-role label."
            ),
            "source_free_pdb_context": (
                "PDB-level source-free conflict and decision context inherited from "
                "epk_candidate_conflict_decision_v1."
            ),
            "candidate_materiality_projection_v1": rule["rule_description"],
        },
        "coordinate_state_counts": coordinate_state_counts,
        "blocker_class_counts": blocker_class_counts,
        "materiality_class_counts": materiality_class_counts,
        "conflict_class_counts": conflict_class_counts,
        "decision_class_counts": decision_class_counts,
        "candidate_materiality_rows": materiality_rows,
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
