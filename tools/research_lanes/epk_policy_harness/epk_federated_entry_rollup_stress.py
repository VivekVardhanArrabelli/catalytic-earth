#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epk_candidate_policy_bridge_scoreboard_gate import (
    ENTRY_CLAIM_STATUS_PRECEDENCE,
    build_artifact,
    rel,
    summarize_result,
    write_json,
)
from epk_policy_harness import (
    CLAIM_STATUS_VALUES,
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    REVIEW_ONLY_BLOCKER_FEATURES,
    REVIEW_ONLY_LIGAND_CONTEXTS,
    SCHEMA_VERSION,
    SOURCE_LEAKAGE_ROW_FLAGS,
    evaluate_tranche,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_candidate_entry_rollup_cross_lane_expansion_v2"
STRESS_POLICY_VERSION = (
    "epk_federated_entry_rollup_stress_fixture_review_only_not_production_20260521"
)
ACCEPTED_ROLE_POLICY_ID = "role_policy_v0_review_only_entry_rollup_fixture"
SOURCE_LANE_ARTIFACTS = {
    "epk_positive_evidence": (
        "artifacts/research_lanes/epk_positive_evidence/"
        "candidate_source_adjudication_all_20260521.json"
    ),
    "epk_substrate_role_identity": (
        "artifacts/research_lanes/epk_substrate_role_identity/"
        "epk_candidate_evidence_v1_20260521.json"
    ),
    "epk_false_positive_hunter": (
        "artifacts/research_lanes/epk_false_positive_hunter/"
        "epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json"
    ),
    "epk_sibling_controls": (
        "artifacts/research_lanes/epk_sibling_controls/"
        "review_only_counteraxis_scorer_test_matrix_20260520.json"
    ),
}
ALLOWED_PREDICTIVE_FEATURES = [
    "ligand_code_from_structure",
    "terminal_gamma_equivalent_geometry",
    "terminal_gamma_atom_name",
    "nearest_gamma_acceptor_distance_angstrom",
    "local_metal_context",
    "catalytic_site_locality",
    "source_free_acceptor_role_features",
    "source_free_acceptor_role_policy_id",
    "same_structure_co_materialization",
]


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def stress_policy() -> dict[str, Any]:
    return {
        "metadata": {
            "policy_version": STRESS_POLICY_VERSION,
            "policy_id": "epk_federated_entry_rollup_stress_fixture",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "threshold_calibrated": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "coverage_fixture_not_production_policy": True,
        },
        "hypothesis": (
            "Synthetic review-only federated rows can stress candidate-to-entry "
            "rollup precedence without creating production labels or thresholds."
        ),
        "frozen_inputs": {
            "ligand_code_alias_map": {
                "ATP": ["ATP"],
                "ANP": ["ANP"],
                "AMP_PNP": ["AMP-PNP", "AMPPNP"],
            },
            "candidate_distance_cutoff_angstrom": 6.0,
            "required_same_structure_features": [
                "terminal_gamma_equivalent_geometry",
                "local_metal_context",
                "catalytic_site_locality",
                "source_free_acceptor_role_features",
                "same_structure_co_materialization",
            ],
            "accepted_source_free_acceptor_role_policy_ids": [
                ACCEPTED_ROLE_POLICY_ID
            ],
            "accepted_source_free_acceptor_role_policy_status": (
                "synthetic entry-rollup fixture only; not a production role policy"
            ),
        },
        "allowed_predictive_features": ALLOWED_PREDICTIVE_FEATURES,
        "review_only_features": sorted(REVIEW_ONLY_BLOCKER_FEATURES),
        "forbidden_features": sorted(FORBIDDEN_ROW_FLAGS),
        "review_only_ligand_contexts": sorted(REVIEW_ONLY_LIGAND_CONTEXTS),
    }


def flag_false_fields() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_ROW_FLAGS}


def row(
    *,
    source_lane_id: str,
    entry_id: str,
    candidate_suffix: str,
    claim_status: str,
    coordinate_state: str = "active_gamma",
    ligand_code: str | None = "ATP",
    row_role: str = "federated_entry_rollup_stress_candidate",
    source_row_key: str = "synthetic_candidate_rows",
    all_required_features: bool = True,
    source_free_role_policy_id: str | None = ACCEPTED_ROLE_POLICY_ID,
    terminal_gamma_equivalent_geometry: bool = True,
    local_metal_context: bool = True,
    catalytic_site_locality: bool = True,
    nearest_distance: float | None = 3.2,
    product_state_context: bool = False,
    substrate_acceptor_analog_context: bool = False,
    split_state_context: bool = False,
    candidate_specific_source_repair: bool = False,
    sibling_counterfamily_context: bool = False,
    topology_ambiguity_status: str | None = None,
    sibling_control_match_status: str | None = None,
    coordinate_ligand_materialized: bool = True,
    ligand_context: str | None = None,
    clean_held_out_performance_evidence: bool = True,
    development_or_regression_context: bool = False,
) -> dict[str, Any]:
    source_artifact = SOURCE_LANE_ARTIFACTS[source_lane_id]
    candidate_id = f"{entry_id}:{source_lane_id}:{candidate_suffix}"
    source_free_acceptor_role_features = all_required_features
    same_structure_co_materialization = all_required_features
    if not all_required_features:
        source_free_role_policy_id = None
        terminal_gamma_equivalent_geometry = False
        local_metal_context = False
        catalytic_site_locality = False
        source_free_acceptor_role_features = False
        same_structure_co_materialization = False
    payload = {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "source_lane_id": source_lane_id,
        "source_artifact": source_artifact,
        "source_row_key": source_row_key,
        "source_row_id": candidate_id,
        "row_id": f"{source_lane_id}:{source_row_key}:{candidate_id}",
        "candidate_id": candidate_id,
        "entry_id": entry_id,
        "pdb_id": None,
        "row_role": row_role,
        "ligand_code_from_structure": ligand_code,
        "coordinate_state": coordinate_state,
        "terminal_gamma_equivalent_geometry": terminal_gamma_equivalent_geometry,
        "terminal_gamma_atom_name": (
            "PG" if terminal_gamma_equivalent_geometry else None
        ),
        "nearest_gamma_acceptor_distance_angstrom": nearest_distance,
        "local_metal_context": local_metal_context,
        "catalytic_site_locality": catalytic_site_locality,
        "source_free_acceptor_role_features": source_free_acceptor_role_features,
        "source_free_acceptor_role_policy_id": source_free_role_policy_id,
        "same_structure_co_materialization": same_structure_co_materialization,
        "coordinate_ligand_materialized_from_structure": (
            coordinate_ligand_materialized
        ),
        "coordinate_ligand_code_source": "lane_adapter_compact_source_free_fields",
        "query_ligand_synonym_used_as_coordinate_ligand": False,
        "clean_held_out_performance_evidence": clean_held_out_performance_evidence,
        "development_or_regression_context": development_or_regression_context,
        "source_review_status": "review_only_context_not_predictive",
        "source_validation_status": "review_only_context_not_predictive",
        "product_state_context": product_state_context,
        "substrate_acceptor_analog_context": substrate_acceptor_analog_context,
        "split_state_context": split_state_context,
        "candidate_specific_source_repair": candidate_specific_source_repair,
        "sibling_counterfamily_context": sibling_counterfamily_context,
        "topology_ambiguity_status": topology_ambiguity_status,
        "sibling_control_match_status": sibling_control_match_status,
        "ligand_context": ligand_context,
        "expected_frozen_policy_decision": (
            "review_only_nonabstaining_candidate"
            if claim_status == "review_only_nonabstaining_candidate"
            else "review_only_abstain_entry_rollup_stress"
        ),
        "expected_claim_status": claim_status,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }
    payload.update(flag_false_fields())
    return payload


def stress_rows() -> list[dict[str, Any]]:
    return [
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_nonabstaining_only",
            candidate_suffix="active",
            claim_status="review_only_nonabstaining_candidate",
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_product_over_active",
            candidate_suffix="active",
            claim_status="review_only_nonabstaining_candidate",
        ),
        row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="entry_rollup_product_over_active",
            candidate_suffix="adp",
            claim_status="review_only_abstain_product_state",
            coordinate_state="adp_state",
            ligand_code="ADP",
            product_state_context=True,
            ligand_context="ADP",
            nearest_distance=None,
        ),
        row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="entry_rollup_analog_over_product",
            candidate_suffix="product",
            claim_status="review_only_abstain_product_state",
            coordinate_state="product_state",
            ligand_code="ADP",
            product_state_context=True,
            ligand_context="PRODUCT_STATE",
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_analog_over_product",
            candidate_suffix="analog",
            claim_status="review_only_abstain_analog_state",
            coordinate_state="substrate_acceptor_analog_state",
            ligand_code="ANP",
            substrate_acceptor_analog_context=True,
            ligand_context="SUBSTRATE_ACCEPTOR_ANALOG",
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_split_over_analog",
            candidate_suffix="analog",
            claim_status="review_only_abstain_analog_state",
            coordinate_state="substrate_acceptor_analog_state",
            ligand_code="ANP",
            substrate_acceptor_analog_context=True,
            ligand_context="SUBSTRATE_ACCEPTOR_ANALOG",
        ),
        row(
            source_lane_id="epk_false_positive_hunter",
            entry_id="entry_rollup_split_over_analog",
            candidate_suffix="split",
            claim_status="review_only_abstain_split_state",
            coordinate_state="split_state",
            split_state_context=True,
            ligand_context="SPLIT_STATE",
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_counteraxis_over_active",
            candidate_suffix="active",
            claim_status="review_only_nonabstaining_candidate",
        ),
        row(
            source_lane_id="epk_sibling_controls",
            entry_id="entry_rollup_counteraxis_over_active",
            candidate_suffix="sibling",
            claim_status="review_only_abstain_sibling_control",
            row_role="federated_entry_rollup_sibling_control",
            sibling_counterfamily_context=True,
            sibling_control_match_status="source_free_sibling_control_review_only",
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_topology_over_active",
            candidate_suffix="active",
            claim_status="review_only_nonabstaining_candidate",
        ),
        row(
            source_lane_id="epk_false_positive_hunter",
            entry_id="entry_rollup_topology_over_active",
            candidate_suffix="ambiguous",
            claim_status="review_only_abstain_topology_ambiguity",
            coordinate_state="ambiguous_coordinate_state",
            ligand_code="ATP",
            topology_ambiguity_status="ambiguous_candidate_topology_review_only",
        ),
        row(
            source_lane_id="epk_false_positive_hunter",
            entry_id="entry_rollup_topology_over_active",
            candidate_suffix="unavailable",
            claim_status="review_only_abstain_topology_ambiguity",
            coordinate_state="unavailable_coordinate_state",
            ligand_code=None,
            coordinate_ligand_materialized=False,
            nearest_distance=None,
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_forbidden_context_over_missing",
            candidate_suffix="missing",
            claim_status="review_only_abstain_missing_role_policy",
            all_required_features=False,
        ),
        row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="entry_rollup_forbidden_context_over_missing",
            candidate_suffix="repair",
            claim_status="review_only_abstain_forbidden_context",
            candidate_specific_source_repair=True,
            ligand_context="POST_HOC_REPAIR",
        ),
        row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="entry_rollup_missing_role_only",
            candidate_suffix="ligand_absent",
            claim_status="review_only_abstain_missing_role_policy",
            coordinate_state="ligand_absent",
            ligand_code=None,
            all_required_features=False,
            coordinate_ligand_materialized=False,
            nearest_distance=None,
        ),
        row(
            source_lane_id="epk_positive_evidence",
            entry_id="entry_rollup_missing_role_only",
            candidate_suffix="metal_absent",
            claim_status="review_only_abstain_missing_role_policy",
            coordinate_state="metal_absent",
            ligand_code="ATP",
            all_required_features=False,
            nearest_distance=3.8,
        ),
    ]


def source_lane_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for candidate in rows:
        lane_id = candidate["source_lane_id"]
        counts[lane_id] = counts.get(lane_id, 0) + 1
    return counts


def stress_tranche() -> dict[str, Any]:
    rows = stress_rows()
    lane_counts = source_lane_counts(rows)
    return {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": len(rows),
            "source_lane_count": len(lane_counts),
            "source_lanes": sorted(lane_counts),
            "input_summaries": [
                {
                    "lane_id": lane_id,
                    "artifact": SOURCE_LANE_ARTIFACTS[lane_id],
                    "selected_row_count": count,
                    "review_only_input": True,
                    "synthetic_entry_rollup_stress_fixture": True,
                }
                for lane_id, count in sorted(lane_counts.items())
            ],
            "require_candidate_identity_fields": True,
            "federated_adapter_smoke_contract": {
                "candidate_rows_from_independent_lanes": True,
                "source_artifacts_review_only": True,
                "source_text_and_protein_names_not_copied": True,
                "source_review_context_not_predictive": True,
                "raw_coordinate_dump_written": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            },
            "entry_rollup_stress_contract": {
                "entry_id_first_class": True,
                "candidate_rows_are_source_of_truth": True,
                "shared_entries_cross_source_lanes": True,
                "fail_closed_entry_claim_status_precedence": list(
                    ENTRY_CLAIM_STATUS_PRECEDENCE
                ),
                "discovery_signal_separate_from_claim_admissibility": True,
                "coverage_fixture_not_production_policy": True,
            },
            "target_entry_claim_status_values": sorted(
                CLAIM_STATUS_VALUES - {"forbidden_source_leakage"}
            ),
            "target_coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": rows,
    }


def sorted_count_keys(result: dict[str, Any], field: str) -> list[str]:
    values = result.get("metadata", {}).get(field, {})
    if not isinstance(values, dict):
        raise ValueError(f"result metadata.{field} must be an object")
    return sorted(values)


def summarize_fault(
    root: Path,
    path: Path,
    result: dict[str, Any],
    expected_failure: str,
) -> dict[str, Any]:
    try:
        summary = summarize_result(root, path, result)
    except ValueError as error:
        return {
            "artifact": rel(path, root),
            "expected_failure": expected_failure,
            "rejected": True,
            "rejection_type": "validator_error",
            "error": str(error),
        }
    return {
        "artifact": rel(path, root),
        "expected_failure": expected_failure,
        "rejected": summary["gate_pass"] is False,
        "rejection_type": "gate_failure",
        "entry_claim_status_counts": summary["entry_claim_status_counts"],
        "forbidden_source_leakage_count": summary["forbidden_source_leakage_count"],
        "unsafe_control_nonabstention_count": summary[
            "unsafe_control_nonabstention_count"
        ],
        "missing_schema_row_count": summary["missing_schema_row_count"],
        "entry_rollups": summary["entry_rollups"],
        "gate_pass": summary["gate_pass"],
    }


def forbidden_source_leakage_result(result: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    mutated["metadata"]["fault_injection_expected_failure"] = (
        "mixed_entry_forbidden_source_leakage"
    )
    mutated["metadata"]["primary_outcome"] = "policy_falsified"
    row = mutated["rows"][0]
    row["row_id"] = "fault:mixed_entry_forbidden_source_leakage"
    row["entry_id"] = "entry_rollup_source_leakage_blocks_all"
    row["claim_status"] = "forbidden_source_leakage"
    row["claim_admissibility"] = "forbidden"
    row["forbidden_predictive_context_flags"] = [
        "source_query_used_for_predictive_feature"
    ]
    mutated["metadata"]["claim_status_counts"] = dict(
        mutated["metadata"]["claim_status_counts"]
    )
    mutated["metadata"]["claim_status_counts"]["forbidden_source_leakage"] = 1
    original_status = "review_only_nonabstaining_candidate"
    mutated["metadata"]["claim_status_counts"][original_status] -= 1
    if mutated["metadata"]["claim_status_counts"][original_status] == 0:
        del mutated["metadata"]["claim_status_counts"][original_status]
    return mutated


def unsafe_control_nonabstention_result(result: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    mutated["metadata"]["fault_injection_expected_failure"] = (
        "mixed_entry_unsafe_control_nonabstention"
    )
    row = mutated["rows"][0]
    row["row_id"] = "fault:mixed_entry_unsafe_control_nonabstention"
    row["entry_id"] = "entry_rollup_unsafe_control_nonabstention"
    row["row_role"] = "sibling_control"
    row["sibling_control_match_status"] = "unsafe_nonabstaining_control_fixture"
    return mutated


def missing_entry_identity_result(result: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    mutated["metadata"]["fault_injection_expected_failure"] = (
        "missing_candidate_identity"
    )
    mutated["rows"] = [copy.deepcopy(result["rows"][0])]
    row = mutated["rows"][0]
    row["row_id"] = "fault:missing_candidate_identity"
    row.pop("candidate_id", None)
    row.pop("source_lane_id", None)
    row.pop("source_artifact", None)
    mutated["metadata"]["row_count"] = 1
    mutated["metadata"]["claim_status_counts"] = {row["claim_status"]: 1}
    mutated["metadata"]["coordinate_state_counts"] = {row["coordinate_state"]: 1}
    return mutated


def build_outputs(root: Path, output_dir: Path, run_stamp: str) -> dict[str, Path]:
    policy = stress_policy()
    tranche = stress_tranche()
    result = evaluate_tranche(policy, tranche)
    expected_statuses = CLAIM_STATUS_VALUES - {"forbidden_source_leakage"}
    if set(sorted_count_keys(result, "claim_status_counts")) != expected_statuses:
        raise ValueError("entry-rollup stress did not cover all non-forbidden statuses")
    if set(sorted_count_keys(result, "coordinate_state_counts")) != COORDINATE_STATE_VALUES:
        raise ValueError("entry-rollup stress did not cover all coordinate states")
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("entry-rollup stress produced claim-status mismatches")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    report_path = output_dir / f"{stem}.json"
    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)

    gate = build_artifact(root, [result_path])
    if gate["gate"]["gate_pass"] is not True:
        raise ValueError("entry-rollup stress scoreboard gate must pass")

    covered_entry_statuses = set(
        gate["scoreboard_summary"]["covered_entry_claim_status_values"]
    )
    if covered_entry_statuses != expected_statuses:
        raise ValueError("entry-rollup stress did not cover all non-forbidden entries")
    write_json(gate_path, gate, pretty=True)

    negative_results = {
        "mixed_entry_forbidden_source_leakage": forbidden_source_leakage_result(
            result
        ),
        "mixed_entry_unsafe_control_nonabstention": (
            unsafe_control_nonabstention_result(result)
        ),
        "missing_candidate_identity": missing_entry_identity_result(result),
    }
    negative_paths = {
        name: output_dir / f"{stem}_negative_{name}_result.json"
        for name in negative_results
    }
    fault_summaries: list[dict[str, Any]] = []
    for name, payload in negative_results.items():
        path = negative_paths[name]
        write_json(path, payload, pretty=True)
        fault_summaries.append(summarize_fault(root, path, payload, name))

    failed_to_reject = [
        summary for summary in fault_summaries if summary.get("rejected") is not True
    ]
    if failed_to_reject:
        raise ValueError(f"fault injections were not rejected: {failed_to_reject}")

    source_leakage_fault = next(
        summary
        for summary in fault_summaries
        if summary["expected_failure"] == "mixed_entry_forbidden_source_leakage"
    )
    source_leakage_rollups = [
        rollup
        for rollup in source_leakage_fault["entry_rollups"]
        if rollup["entry_id"] == "entry_rollup_source_leakage_blocks_all"
    ]
    if not source_leakage_rollups or source_leakage_rollups[0][
        "entry_claim_status"
    ] != "forbidden_source_leakage":
        raise ValueError("source leakage must dominate mixed-entry rollup status")

    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "policy_version": STRESS_POLICY_VERSION,
            "primary_outcome": "scoreboard_gate_created",
            "coverage_fixture_not_production_policy": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": (
            "Candidate rows from independent ePK lanes can be summarized to entry "
            "status only if entry_id is first-class, candidate decisions remain "
            "visible, and fail-closed precedence dominates discovery signal."
        ),
        "positive_stress": {
            "tranche_artifact": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result_artifact": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate_artifact": rel(gate_path, root),
            "scoreboard_gate_sha256": sha256_file(gate_path),
            "rows_reviewed": result["metadata"]["row_count"],
            "entry_count": gate["scoreboard_summary"]["entry_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "entry_claim_status_counts": gate["scoreboard_summary"][
                "entry_claim_status_counts"
            ],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "source_lane_counts": source_lane_counts(tranche["rows"]),
            "gate_pass": gate["gate"]["gate_pass"],
        },
        "entry_rollup_contract": {
            "entry_id_is_first_class": True,
            "candidate_rows_are_source_of_truth": True,
            "entry_status_derived_from_candidate_decisions": True,
            "claim_admissibility_separate_from_discovery_signal": True,
            "entry_claim_status_precedence": list(ENTRY_CLAIM_STATUS_PRECEDENCE),
            "nonabstaining_candidate_rows_remain_review_only": True,
            "product_adp_analog_split_rows_are_review_only_state_classes": True,
            "production_claim_allowed": False,
        },
        "negative_fault_injections": fault_summaries,
        "coverage_summary": {
            "claim_status_allowed_values": sorted(CLAIM_STATUS_VALUES),
            "claim_status_values_covered_by_positive_or_expected_negative_fixture": (
                sorted(CLAIM_STATUS_VALUES)
            ),
            "entry_claim_status_values_covered_by_positive_fixture": sorted(
                covered_entry_statuses
            ),
            "entry_claim_status_values_uncovered_by_positive_fixture": sorted(
                expected_statuses - covered_entry_statuses
            ),
            "coordinate_state_allowed_values": sorted(COORDINATE_STATE_VALUES),
            "coordinate_state_values_covered": sorted(
                result["metadata"]["coordinate_state_counts"]
            ),
            "coordinate_state_values_uncovered": sorted(
                COORDINATE_STATE_VALUES
                - set(result["metadata"]["coordinate_state_counts"])
            ),
            "forbidden_source_leakage_is_expected_gate_failure": True,
            "unsafe_control_nonabstention_is_expected_gate_failure": True,
            "missing_candidate_identity_is_expected_gate_failure": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "artifacts": {
            "tranche": rel(tranche_path, root),
            "result": rel(result_path, root),
            "scoreboard_gate": rel(gate_path, root),
            **{
                f"negative_{name}": rel(path, root)
                for name, path in negative_paths.items()
            },
        },
    }
    write_json(report_path, report, pretty=True)
    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": gate_path,
        "report": report_path,
        **{f"negative_{name}": path for name, path in negative_paths.items()},
    }


def self_test() -> None:
    root = Path.cwd()
    output_dir = Path("/private/tmp/epk_federated_entry_rollup_stress_self_test")
    outputs = build_outputs(root, output_dir, "selftest")
    report = json.loads(outputs["report"].read_text(encoding="utf-8"))
    assert report["positive_stress"]["gate_pass"] is True
    assert report["coverage_summary"][
        "entry_claim_status_values_uncovered_by_positive_fixture"
    ] == []
    assert report["coverage_summary"]["coordinate_state_values_uncovered"] == []
    assert all(
        fault["rejected"] is True for fault in report["negative_fault_injections"]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a compact review-only federated entry-rollup stress fixture "
            "with cross-lane candidate rows and expected-failure gate cases."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_policy_harness"),
    )
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    run_stamp = args.timestamp or timestamp()
    outputs = build_outputs(Path.cwd(), args.output_dir, run_stamp)
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
