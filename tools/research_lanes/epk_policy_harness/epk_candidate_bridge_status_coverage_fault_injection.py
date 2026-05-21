#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epk_candidate_policy_bridge_scoreboard_gate import (
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
ARTIFACT_ID = "epk_candidate_bridge_status_coverage_fault_injection_v2"
COVERAGE_POLICY_VERSION = (
    "epk_candidate_bridge_status_coverage_fixture_review_only_not_production_20260521"
)
ACCEPTED_ROLE_POLICY_ID = "role_policy_v0_review_only_coverage_fixture"
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


def coverage_policy() -> dict[str, Any]:
    return {
        "metadata": {
            "policy_version": COVERAGE_POLICY_VERSION,
            "policy_id": "epk_candidate_bridge_status_coverage_fixture",
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
            "Synthetic review-only bridge rows can exercise claim-status and "
            "coordinate-state emission without changing the frozen production policy."
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
                "synthetic coverage fixture only; not a production role policy"
            ),
        },
        "allowed_predictive_features": ALLOWED_PREDICTIVE_FEATURES,
        "review_only_features": sorted(REVIEW_ONLY_BLOCKER_FEATURES),
        "forbidden_features": sorted(FORBIDDEN_ROW_FLAGS),
        "review_only_ligand_contexts": sorted(REVIEW_ONLY_LIGAND_CONTEXTS),
    }


def active_gamma_row(row_id: str, claim_status: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "pdb_id": f"COV{len(row_id):02d}",
        "row_role": "synthetic_bridge_status_coverage_fixture",
        "ligand_code_from_structure": "ATP",
        "coordinate_state": "active_gamma",
        "terminal_gamma_equivalent_geometry": True,
        "terminal_gamma_atom_name": "PG",
        "nearest_gamma_acceptor_distance_angstrom": 3.2,
        "local_metal_context": True,
        "catalytic_site_locality": True,
        "source_free_acceptor_role_features": True,
        "source_free_acceptor_role_policy_id": ACCEPTED_ROLE_POLICY_ID,
        "same_structure_co_materialization": True,
        "coordinate_ligand_materialized_from_structure": True,
        "coordinate_ligand_code_source": "mmcif_atom_site_auth_or_label_comp_id",
        "query_ligand_synonym_used_as_coordinate_ligand": False,
        "expected_frozen_policy_decision": (
            "review_only_nonabstaining_candidate"
            if claim_status == "review_only_nonabstaining_candidate"
            else "review_only_abstain_bridge_status_coverage"
        ),
        "expected_claim_status": claim_status,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }


def coverage_rows() -> list[dict[str, Any]]:
    rows = [
        active_gamma_row(
            "coverage_nonabstaining_active_gamma",
            "review_only_nonabstaining_candidate",
        ),
        dict(
            active_gamma_row(
                "coverage_missing_role_policy_active_gamma",
                "review_only_abstain_missing_role_policy",
            ),
            source_free_acceptor_role_features=False,
            source_free_acceptor_role_policy_id=None,
            same_structure_co_materialization=False,
        ),
        dict(
            active_gamma_row(
                "coverage_sibling_control_active_gamma",
                "review_only_abstain_sibling_control",
            ),
            row_role="synthetic_sibling_control_review_only",
            sibling_counterfamily_context=True,
            sibling_pair_id="coverage_pair_1",
            sibling_pair_role="sibling_control",
            sibling_control_match_status="matched_source_free_control_fixture",
        ),
        dict(
            active_gamma_row(
                "coverage_product_state",
                "review_only_abstain_product_state",
            ),
            coordinate_state="product_state",
            product_state_context=True,
            ligand_context="PRODUCT_STATE",
        ),
        dict(
            active_gamma_row("coverage_adp_state", "review_only_abstain_product_state"),
            coordinate_state="adp_state",
            ligand_code_from_structure="ADP",
            ligand_context="ADP",
        ),
        dict(
            active_gamma_row(
                "coverage_substrate_acceptor_analog_state",
                "review_only_abstain_analog_state",
            ),
            coordinate_state="substrate_acceptor_analog_state",
            substrate_acceptor_analog_context=True,
            ligand_context="SUBSTRATE_ACCEPTOR_ANALOG",
        ),
        dict(
            active_gamma_row(
                "coverage_split_state",
                "review_only_abstain_split_state",
            ),
            coordinate_state="split_state",
            split_state_context=True,
            ligand_context="SPLIT_STATE",
        ),
        dict(
            active_gamma_row(
                "coverage_ambiguous_coordinate_state",
                "review_only_abstain_topology_ambiguity",
            ),
            coordinate_state="ambiguous_coordinate_state",
            topology_ambiguity_status="ambiguous_same_structure_topology_fixture",
        ),
        dict(
            active_gamma_row(
                "coverage_unavailable_coordinate_state",
                "review_only_abstain_topology_ambiguity",
            ),
            coordinate_state="unavailable_coordinate_state",
            coordinate_ligand_materialized_from_structure=False,
        ),
        dict(
            active_gamma_row(
                "coverage_ligand_absent_forbidden_context",
                "review_only_abstain_forbidden_context",
            ),
            coordinate_state="ligand_absent",
            ligand_code_from_structure=None,
        ),
        dict(
            active_gamma_row(
                "coverage_metal_absent_missing_role_policy",
                "review_only_abstain_missing_role_policy",
            ),
            coordinate_state="metal_absent",
            local_metal_context=False,
        ),
    ]
    return rows


def coverage_tranche() -> dict[str, Any]:
    rows = coverage_rows()
    return {
        "metadata": {
            "tranche_id": f"{ARTIFACT_ID}_positive_tranche",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "row_count": len(rows),
            "synthetic_fixture": True,
            "coverage_fixture_not_production_policy": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "schema_version": SCHEMA_VERSION,
            "target_claim_status_values": sorted(CLAIM_STATUS_VALUES - {"forbidden_source_leakage"}),
            "target_coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
            "negative_fixtures_cover_forbidden_source_leakage": True,
        },
        "rows": rows,
    }


def result_counts(result: dict[str, Any], field: str) -> set[str]:
    values = result.get("metadata", {}).get(field, {})
    if not isinstance(values, dict):
        raise ValueError(f"result metadata.{field} must be an object")
    return set(values)


def mutated_result(result: dict[str, Any], mutation: str) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    mutated["metadata"]["fault_injection_expected_failure"] = mutation
    mutated["metadata"]["primary_outcome"] = "policy_falsified"
    if mutation == "unsafe_control_nonabstention":
        mutated["rows"] = [copy.deepcopy(result["rows"][0])]
        row = mutated["rows"][0]
        row["row_id"] = "fault_unsafe_sibling_control_nonabstention"
        row["row_role"] = "sibling_control"
        row["claim_status"] = "review_only_nonabstaining_candidate"
        row["coordinate_state"] = "active_gamma"
        mutated["metadata"]["row_count"] = 1
        mutated["metadata"]["claim_status_counts"] = {
            "review_only_nonabstaining_candidate": 1,
        }
        mutated["metadata"]["coordinate_state_counts"] = {"active_gamma": 1}
    elif mutation == "missing_schema_fields":
        mutated["rows"] = [copy.deepcopy(result["rows"][0])]
        row = mutated["rows"][0]
        row["row_id"] = "fault_missing_schema_version"
        row.pop("schema_version", None)
        row.pop("claim_admissibility", None)
        mutated["metadata"]["row_count"] = 1
        mutated["metadata"]["claim_status_counts"] = {
            row["claim_status"]: 1,
        }
        mutated["metadata"]["coordinate_state_counts"] = {
            row["coordinate_state"]: 1,
        }
    elif mutation == "metadata_count_drift":
        mutated["rows"] = [copy.deepcopy(result["rows"][0])]
        mutated["rows"][0]["row_id"] = "fault_metadata_count_drift"
        mutated["metadata"]["row_count"] = 1
        mutated["metadata"]["claim_status_counts"] = {
            "review_only_abstain_product_state": 1,
        }
        mutated["metadata"]["coordinate_state_counts"] = {"active_gamma": 1}
    else:
        raise ValueError(f"unknown mutation {mutation}")
    return mutated


def source_leak_result(policy: dict[str, Any]) -> dict[str, Any]:
    row = active_gamma_row(
        "fault_forbidden_source_leakage",
        "forbidden_source_leakage",
    )
    row["source_query_used_for_predictive_feature"] = True
    row["expected_frozen_policy_decision"] = "review_only_abstain_forbidden_context"
    tranche = {
        "metadata": {
            "tranche_id": f"{ARTIFACT_ID}_forbidden_source_leakage_negative",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "row_count": 1,
            "fault_injection_expected_failure": "forbidden_source_leakage",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": [row],
    }
    return evaluate_tranche(policy, tranche)


def source_leakage_flag_audit(policy: dict[str, Any]) -> list[dict[str, Any]]:
    audit: list[dict[str, Any]] = []
    for flag in sorted(SOURCE_LEAKAGE_ROW_FLAGS):
        row = active_gamma_row(
            f"fault_{flag}",
            "forbidden_source_leakage",
        )
        row[flag] = True
        row["expected_frozen_policy_decision"] = "review_only_abstain_forbidden_context"
        result = evaluate_tranche(
            policy,
            {
                "metadata": {
                    "tranche_id": f"{ARTIFACT_ID}_{flag}_source_leakage_audit",
                    "created_at": utc_now(),
                    "lane_id": LANE_ID,
                    "review_only": True,
                    "row_count": 1,
                    "source_leakage_flag_audit": True,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                },
                "rows": [row],
            },
        )
        result_row = result["rows"][0]
        if result_row["claim_status"] != "forbidden_source_leakage":
            raise ValueError(f"{flag} did not emit forbidden_source_leakage")
        if result_row["claim_admissibility"] != "forbidden":
            raise ValueError(f"{flag} did not emit forbidden claim_admissibility")
        audit.append(
            {
                "forbidden_source_leakage_flag": flag,
                "claim_status": result_row["claim_status"],
                "claim_admissibility": result_row["claim_admissibility"],
                "gate_expected_failure": True,
            }
        )
    return audit


def summarize_fault(
    root: Path,
    path: Path,
    result: dict[str, Any],
    expected_reason: str,
) -> dict[str, Any]:
    try:
        summary = summarize_result(root, path, result)
    except ValueError as error:
        return {
            "artifact": rel(path, root),
            "expected_failure": expected_reason,
            "rejected": True,
            "rejection_type": "validator_error",
            "error": str(error),
        }
    return {
        "artifact": rel(path, root),
        "expected_failure": expected_reason,
        "rejected": summary["gate_pass"] is False,
        "rejection_type": "gate_failure",
        "forbidden_source_leakage_count": summary["forbidden_source_leakage_count"],
        "unsafe_control_nonabstention_count": summary[
            "unsafe_control_nonabstention_count"
        ],
        "missing_schema_row_count": summary["missing_schema_row_count"],
        "gate_pass": summary["gate_pass"],
    }


def build_outputs(root: Path, output_dir: Path, run_stamp: str) -> dict[str, Path]:
    policy = coverage_policy()
    tranche = coverage_tranche()
    result = evaluate_tranche(policy, tranche)
    covered_statuses = result_counts(result, "claim_status_counts")
    covered_states = result_counts(result, "coordinate_state_counts")
    expected_positive_statuses = CLAIM_STATUS_VALUES - {"forbidden_source_leakage"}
    if covered_statuses != expected_positive_statuses:
        raise ValueError(
            "positive bridge coverage did not cover every non-forbidden claim status: "
            f"{sorted(covered_statuses)}"
        )
    if covered_states != COORDINATE_STATE_VALUES:
        raise ValueError(
            "positive bridge coverage did not cover every coordinate state: "
            f"{sorted(covered_states)}"
        )
    if result["metadata"]["primary_outcome"] != "policy_frozen_review_only":
        raise ValueError("positive bridge coverage must remain policy_frozen_review_only")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    report_path = output_dir / f"{stem}.json"
    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)

    gate = build_artifact(root, [result_path])
    if gate["gate"]["gate_pass"] is not True:
        raise ValueError("positive bridge coverage scoreboard gate must pass")
    write_json(gate_path, gate, pretty=True)

    source_leak = source_leak_result(policy)
    source_leakage_audit = source_leakage_flag_audit(policy)
    source_leak_path = output_dir / f"{stem}_negative_forbidden_source_leakage_result.json"
    write_json(source_leak_path, source_leak, pretty=True)

    negative_results = {
        "unsafe_control_nonabstention": mutated_result(
            result, "unsafe_control_nonabstention"
        ),
        "missing_schema_fields": mutated_result(result, "missing_schema_fields"),
        "metadata_count_drift": mutated_result(result, "metadata_count_drift"),
    }
    negative_paths = {
        name: output_dir / f"{stem}_negative_{name}_result.json"
        for name in negative_results
    }
    for name, payload in negative_results.items():
        write_json(negative_paths[name], payload, pretty=True)

    fault_summaries = [
        summarize_fault(
            root,
            source_leak_path,
            source_leak,
            "forbidden_source_leakage",
        )
    ]
    for name, payload in negative_results.items():
        fault_summaries.append(summarize_fault(root, negative_paths[name], payload, name))
    failed_to_reject = [
        fault for fault in fault_summaries if fault.get("rejected") is not True
    ]
    if failed_to_reject:
        raise ValueError(f"fault injections were not rejected: {failed_to_reject}")

    all_covered_statuses = sorted(covered_statuses | {"forbidden_source_leakage"})
    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "policy_version": COVERAGE_POLICY_VERSION,
            "primary_outcome": "scoreboard_gate_created",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "coverage_fixture_not_production_policy": True,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": (
            "The candidate-level bridge is regression-testable only if positive "
            "coverage exercises every review-only status and coordinate state while "
            "negative fixtures prove that source leakage, unsafe controls, missing "
            "schema fields, and metadata drift cannot pass the scoreboard gate."
        ),
        "positive_coverage": {
            "tranche_artifact": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result_artifact": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate_artifact": rel(gate_path, root),
            "scoreboard_gate_sha256": sha256_file(gate_path),
            "rows_reviewed": result["metadata"]["row_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "covered_non_forbidden_claim_status_values": sorted(covered_statuses),
            "covered_coordinate_state_values": sorted(covered_states),
            "gate_pass": gate["gate"]["gate_pass"],
        },
        "negative_fault_injections": fault_summaries,
        "source_leakage_flag_audit": source_leakage_audit,
        "coverage_summary": {
            "claim_status_allowed_values": sorted(CLAIM_STATUS_VALUES),
            "claim_status_values_covered_by_positive_or_expected_negative_fixture": (
                all_covered_statuses
            ),
            "claim_status_values_uncovered": sorted(
                CLAIM_STATUS_VALUES - set(all_covered_statuses)
            ),
            "coordinate_state_allowed_values": sorted(COORDINATE_STATE_VALUES),
            "coordinate_state_values_covered": sorted(covered_states),
            "coordinate_state_values_uncovered": sorted(
                COORDINATE_STATE_VALUES - covered_states
            ),
            "forbidden_source_leakage_is_expected_gate_failure": True,
            "unsafe_control_nonabstention_is_expected_gate_failure": True,
            "missing_schema_fields_are_expected_gate_failure": True,
            "metadata_count_drift_is_expected_validator_error": True,
            "source_leakage_flag_count_audited": len(source_leakage_audit),
            "discovery_signal_separate_from_claim_admissibility": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    if report["coverage_summary"]["claim_status_values_uncovered"]:
        raise ValueError("claim status coverage remains incomplete")
    if report["coverage_summary"]["coordinate_state_values_uncovered"]:
        raise ValueError("coordinate state coverage remains incomplete")
    write_json(report_path, report, pretty=True)
    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": gate_path,
        "report": report_path,
        "negative_forbidden_source_leakage": source_leak_path,
        **{f"negative_{name}": path for name, path in negative_paths.items()},
    }


def self_test() -> None:
    root = Path.cwd()
    output_dir = Path("/private/tmp/epk_candidate_bridge_status_coverage_self_test")
    outputs = build_outputs(root, output_dir, "selftest")
    report = json.loads(outputs["report"].read_text(encoding="utf-8"))
    assert report["coverage_summary"]["claim_status_values_uncovered"] == []
    assert report["coverage_summary"]["coordinate_state_values_uncovered"] == []
    assert all(
        fault["rejected"] is True for fault in report["negative_fault_injections"]
    )
    assert report["positive_coverage"]["gate_pass"] is True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate compact review-only candidate bridge status/coordinate "
            "coverage and expected-failure scoreboard fixtures."
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
