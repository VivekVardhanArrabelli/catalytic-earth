#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from epk_candidate_policy_bridge_scoreboard_gate import build_artifact, rel, write_json
from epk_federated_candidate_adapter_smoke import (
    ADAPTERS,
    load_git_json,
    rows_for_keys,
)
from epk_federated_schema_contract_lock import (
    run_fault_injections,
    validate_contract_bundle,
)
from epk_policy_harness import (
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    evaluate_tranche,
    load_json,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_real_lane_missing_coordinate_state_adapter_v9"
DEFAULT_ARTIFACT_DIR = Path("artifacts/research_lanes/epk_policy_harness")
DEFAULT_POLICY = Path(
    "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json"
)
TARGET_COORDINATE_STATES = (
    "adp_state",
    "ligand_absent",
    "metal_absent",
    "unavailable_coordinate_state",
)
REQUIRED_REAL_TARGET_STATES = (
    "adp_state",
    "ligand_absent",
    "unavailable_coordinate_state",
)
REAL_INPUT_SPECS = (
    {
        "lane_id": "epk_positive_evidence",
        "ref": "origin/research/epk-positive-evidence",
        "path": (
            "artifacts/research_lanes/epk_positive_evidence/"
            "candidate_source_adjudication_all_20260521.json"
        ),
        "row_keys": ("adjudicated_candidate_rows",),
    },
    {
        "lane_id": "epk_substrate_role_identity",
        "ref": "origin/research/epk-substrate-role-identity",
        "path": (
            "artifacts/research_lanes/epk_substrate_role_identity/"
            "epk_candidate_evidence_v1_20260521.json"
        ),
        "row_keys": ("candidate_evidence_rows", "state_only_rows"),
    },
    {
        "lane_id": "epk_false_positive_hunter",
        "ref": "origin/research/epk-false-positive-hunter",
        "path": (
            "artifacts/research_lanes/epk_false_positive_hunter/"
            "epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json"
        ),
        "row_keys": ("rows",),
    },
    {
        "lane_id": "epk_sibling_controls",
        "ref": "origin/research/epk-sibling-controls",
        "path": (
            "artifacts/research_lanes/epk_sibling_controls/"
            "review_only_counteraxis_scorer_test_matrix_20260520.json"
        ),
        "row_keys": (
            "gamma_proximity_counteraxis_cases",
            "product_phosphoryl_identity_counteraxis_cases",
        ),
    },
)
STATE_PRIORITY = {
    "adp_state": 0,
    "ligand_absent": 1,
    "unavailable_coordinate_state": 2,
    "metal_absent": 3,
    "ambiguous_coordinate_state": 4,
    "product_state": 5,
    "split_state": 6,
    "substrate_acceptor_analog_state": 7,
    "active_gamma": 8,
}


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def false_flag_fields() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_ROW_FLAGS}


def count_values(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        value = str(row.get(field) or "")
        if value:
            counts[value] += 1
    return dict(sorted(counts.items()))


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_id": row.get("row_id"),
        "candidate_id": row.get("candidate_id"),
        "entry_id": row.get("entry_id"),
        "source_lane_id": row.get("source_lane_id"),
        "source_artifact": row.get("source_artifact"),
        "source_row_key": row.get("source_row_key"),
        "coordinate_state": row.get("coordinate_state"),
        "ligand_code_from_structure": row.get("ligand_code_from_structure"),
        "coordinate_ligand_materialized_from_structure": row.get(
            "coordinate_ligand_materialized_from_structure"
        ),
        "local_metal_context": row.get("local_metal_context"),
        "expected_claim_status": row.get("expected_claim_status"),
    }


def row_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        STATE_PRIORITY.get(str(row.get("coordinate_state") or ""), 50),
        row.get("ligand_code_from_structure") is not None
        if row.get("coordinate_state")
        in {"ligand_absent", "unavailable_coordinate_state"}
        else False,
        str(row.get("entry_id") or row.get("pdb_id") or ""),
        str(row.get("row_id") or ""),
    )


def adapt_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    all_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for spec, payload in payloads:
        lane_id = str(spec["lane_id"])
        adapted_rows: list[dict[str, Any]] = []
        for index, (row_key, raw_row) in enumerate(
            rows_for_keys(payload, tuple(spec["row_keys"]))
        ):
            adapted = ADAPTERS[lane_id](
                raw_row,
                source_artifact=str(spec["path"]),
                source_row_key=row_key,
                index=index,
            )
            entry_id = str(
                adapted.get("entry_id") or adapted.get("pdb_id") or ""
            ).strip()
            adapted["entry_id"] = entry_id or None
            adapted["pdb_id"] = adapted.get("pdb_id") or adapted["entry_id"]
            adapted.update(
                {
                    key: adapted.get(key, value)
                    for key, value in false_flag_fields().items()
                }
            )
            adapted_rows.append(adapted)
            all_rows.append(adapted)
        target_rows = [
            row
            for row in adapted_rows
            if row.get("coordinate_state") in TARGET_COORDINATE_STATES
        ]
        summaries.append(
            {
                "lane_id": lane_id,
                "ref": spec.get("ref"),
                "artifact": spec["path"],
                "row_keys": list(spec["row_keys"]),
                "available_row_count": len(adapted_rows),
                "available_entry_count": len(
                    {str(row.get("entry_id") or "") for row in adapted_rows}
                    - {""}
                ),
                "available_coordinate_state_counts": count_values(
                    adapted_rows, "coordinate_state"
                ),
                "available_target_coordinate_state_counts": count_values(
                    target_rows, "coordinate_state"
                ),
                "available_target_row_count": len(target_rows),
                "selected_row_count": 0,
                "review_only_input": True,
            }
        )
    return all_rows, summaries


def selected_real_target_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows_by_state: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        state = str(row.get("coordinate_state") or "")
        if state in TARGET_COORDINATE_STATES:
            rows_by_state[state].append(row)

    selected: list[dict[str, Any]] = []
    for state in TARGET_COORDINATE_STATES:
        candidates = sorted(rows_by_state.get(state, []), key=row_sort_key)
        if candidates:
            selected.append(copy.deepcopy(candidates[0]))
    return selected


def update_selected_counts(
    summaries: list[dict[str, Any]], selected_rows: list[dict[str, Any]]
) -> None:
    selected_counts = Counter(str(row["source_lane_id"]) for row in selected_rows)
    selected_entries: dict[str, set[str]] = defaultdict(set)
    for row in selected_rows:
        selected_entries[str(row["source_lane_id"])].add(str(row.get("entry_id") or ""))
    for summary in summaries:
        lane_id = str(summary["lane_id"])
        summary["selected_row_count"] = selected_counts.get(lane_id, 0)
        summary["selected_entry_count"] = len(selected_entries.get(lane_id, set()))


def build_tranche_from_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]]
) -> dict[str, Any]:
    all_rows, summaries = adapt_payloads(payloads)
    selected_rows = selected_real_target_rows(all_rows)
    update_selected_counts(summaries, selected_rows)

    selected_states = set(count_values(selected_rows, "coordinate_state"))
    available_target_rows = [
        row for row in all_rows if row.get("coordinate_state") in TARGET_COORDINATE_STATES
    ]
    available_target_counts = count_values(available_target_rows, "coordinate_state")
    missing_targets = sorted(set(TARGET_COORDINATE_STATES) - selected_states)
    selected_lanes = sorted({str(row["source_lane_id"]) for row in selected_rows})

    return {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": len(selected_rows),
            "source_lanes": selected_lanes,
            "source_lane_count": len(selected_lanes),
            "input_summaries": [
                summary
                for summary in summaries
                if int(summary.get("selected_row_count") or 0) > 0
            ],
            "all_scanned_input_summaries": summaries,
            "require_candidate_identity_fields": True,
            "target_coordinate_state_values": list(TARGET_COORDINATE_STATES),
            "required_real_target_coordinate_state_values": list(
                REQUIRED_REAL_TARGET_STATES
            ),
            "available_target_coordinate_state_counts": available_target_counts,
            "selected_coordinate_state_counts": count_values(
                selected_rows, "coordinate_state"
            ),
            "selected_expected_claim_status_counts": count_values(
                selected_rows, "expected_claim_status"
            ),
            "selected_entry_ids": [
                str(row.get("entry_id") or "") for row in selected_rows
            ],
            "selected_rows_compact": [compact_row(row) for row in selected_rows],
            "available_target_rows_compact": [
                compact_row(row)
                for row in sorted(available_target_rows, key=row_sort_key)[:12]
            ],
            "covered_real_target_coordinate_state_values": sorted(selected_states),
            "missing_real_target_coordinate_state_values": missing_targets,
            "metal_absent_real_row_observed": "metal_absent" in selected_states,
            "ligand_absent_present_null_ligand_code": any(
                row.get("coordinate_state") == "ligand_absent"
                and "ligand_code_from_structure" in row
                and row.get("ligand_code_from_structure") is None
                and row.get("coordinate_ligand_materialized_from_structure") is False
                for row in selected_rows
            ),
            "unavailable_present_null_ligand_code": any(
                row.get("coordinate_state") == "unavailable_coordinate_state"
                and "ligand_code_from_structure" in row
                and row.get("ligand_code_from_structure") is None
                and row.get("coordinate_ligand_materialized_from_structure") is False
                for row in selected_rows
            ),
            "federated_adapter_smoke_contract": {
                "candidate_rows_from_independent_lanes": True,
                "source_artifacts_review_only": True,
                "source_text_and_protein_names_not_copied": True,
                "source_review_context_not_predictive": True,
                "raw_coordinate_dump_written": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            },
            "real_missing_coordinate_state_adapter_contract": {
                "source_rows_loaded_from_git_refs": True,
                "selected_rows_are_candidate_level": True,
                "synthetic_fixture_rows_excluded": True,
                "present_null_ligand_code_for_ligand_absent": True,
                "present_null_ligand_code_for_unavailable_coordinate_state": True,
                "metal_absent_absence_recorded_as_next_query": (
                    "metal_absent" not in selected_states
                ),
                "source_text_and_protein_names_not_copied": True,
                "progress_claim_allowed": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            },
            "next_query": "epk_real_lane_metal_absent_candidate_evidence_v10_review_only",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "rows": selected_rows,
    }


def validate_v9_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("v9 adapter requires review_only=true")
    contract = metadata.get("real_missing_coordinate_state_adapter_contract")
    if not isinstance(contract, dict):
        raise ValueError("v9 adapter requires real_missing_coordinate_state_adapter_contract")
    for flag in (
        "source_rows_loaded_from_git_refs",
        "selected_rows_are_candidate_level",
        "synthetic_fixture_rows_excluded",
        "present_null_ligand_code_for_ligand_absent",
        "present_null_ligand_code_for_unavailable_coordinate_state",
        "source_text_and_protein_names_not_copied",
    ):
        if contract.get(flag) is not True:
            raise ValueError(f"v9 adapter requires {flag}=true")
    for flag in (
        "progress_claim_allowed",
        "production_claim_allowed",
        "labels_or_fingerprints_changed",
    ):
        if contract.get(flag) is not False:
            raise ValueError(f"v9 adapter requires {flag}=false")

    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("v9 adapter requires non-empty selected rows")
    selected_states = {str(row.get("coordinate_state") or "") for row in rows}
    missing_required = sorted(set(REQUIRED_REAL_TARGET_STATES) - selected_states)
    if missing_required:
        raise ValueError(
            "v9 adapter missed required real coordinate states: "
            f"{missing_required}"
        )
    if not set(selected_states).issubset(COORDINATE_STATE_VALUES):
        raise ValueError(f"v9 adapter emitted invalid coordinate states: {selected_states}")
    for row in rows:
        row_id = str(row.get("row_id") or "")
        source_key = str(row.get("source_row_key") or "")
        source_artifact = str(row.get("source_artifact") or "")
        if not row_id or not row.get("candidate_id") or not row.get("source_lane_id"):
            raise ValueError(f"v9 adapter row missing candidate identity: {row_id}")
        if "synthetic" in source_key or "compact_candidate_fixture" in source_artifact:
            raise ValueError(f"v9 adapter selected non-real fixture row: {row_id}")
        state = str(row.get("coordinate_state") or "")
        if state in {"ligand_absent", "unavailable_coordinate_state"}:
            if "ligand_code_from_structure" not in row:
                raise ValueError(
                    f"v9 adapter row missing present ligand field: {row_id}"
                )
            if row.get("ligand_code_from_structure") is not None:
                raise ValueError(
                    "v9 adapter requires present-but-null ligand_code_from_structure "
                    f"for {state}: {row_id}"
                )
            if row.get("coordinate_ligand_materialized_from_structure") is not False:
                raise ValueError(
                    f"v9 adapter requires {state} materialization=false: {row_id}"
                )
        if state == "metal_absent" and row.get("local_metal_context") is not False:
            raise ValueError(
                f"v9 adapter requires metal_absent local_metal_context=false: {row_id}"
            )
    selected_counts = count_values(rows, "coordinate_state")
    if metadata.get("selected_coordinate_state_counts") != selected_counts:
        raise ValueError("v9 selected coordinate-state counts drifted from rows")
    missing_targets = sorted(set(TARGET_COORDINATE_STATES) - set(selected_counts))
    if metadata.get("missing_real_target_coordinate_state_values") != missing_targets:
        raise ValueError("v9 missing target list drifted from rows")


def write_rejection(
    root: Path,
    path: Path,
    *,
    expected_failure: str,
    expected_error_fragment: str,
    action: Callable[[], Any],
) -> dict[str, Any]:
    try:
        action()
    except ValueError as error:
        observed_error = str(error)
    else:
        raise AssertionError(f"{expected_failure} fault must fail validation")
    rejected = expected_error_fragment in observed_error
    payload = {
        "metadata": {
            "artifact_id": f"{ARTIFACT_ID}_{expected_failure}",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "fault_injection_expected_failure": expected_failure,
            "rejected": rejected,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "expected_error_fragment": expected_error_fragment,
        "observed_error": observed_error,
    }
    write_json(path, payload, pretty=True)
    if not rejected:
        raise ValueError(
            f"{expected_failure} rejected with unexpected error: {observed_error}"
        )
    return {
        "artifact": rel(path, root),
        "sha256": sha256_file(path),
        "expected_failure": expected_failure,
        "rejected": rejected,
        "observed_error": observed_error,
    }


def build_outputs(
    root: Path,
    output_dir: Path,
    run_stamp: str,
    policy_path: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    payloads = [
        (dict(spec), load_git_json(str(spec["ref"]), str(spec["path"])))
        for spec in REAL_INPUT_SPECS
    ]
    policy = load_json(policy_path)
    tranche = build_tranche_from_payloads(payloads)
    validate_v9_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("v9 adapter produced claim-status mismatches")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    scoreboard_path = output_dir / f"{stem}_scoreboard_gate.json"
    contract_path = output_dir / f"{stem}_contract_gate.json"
    report_path = output_dir / f"{stem}.json"
    negative_source_copy_path = (
        output_dir / f"{stem}_negative_source_context_copy_result.json"
    )
    negative_present_null_path = (
        output_dir / f"{stem}_negative_missing_present_null_ligand_result.json"
    )
    negative_identity_path = (
        output_dir / f"{stem}_negative_missing_candidate_identity_result.json"
    )

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)

    scoreboard = build_artifact(root, [result_path])
    if scoreboard["gate"]["gate_pass"] is not True:
        raise ValueError("v9 real missing-coordinate scoreboard gate must pass")
    write_json(scoreboard_path, scoreboard, pretty=True)

    contract_summary = validate_contract_bundle(
        tranche=tranche,
        result=result,
        gate=scoreboard,
    )
    schema_faults: list[dict[str, Any]] = []
    schema_faults_skipped_reason: str | None = None
    try:
        schema_faults = run_fault_injections(
            tranche=tranche,
            result=result,
            gate=scoreboard,
        )
    except ValueError as error:
        if "product/analog row" not in str(error):
            raise
        schema_faults_skipped_reason = (
            "generic v7 entry-precedence fault injection requires a product/analog "
            "pair; v9 intentionally selects only real rows for missing-coordinate "
            "states and uses v9-specific faults instead"
        )
    unexpected_schema_faults = [
        fault["fault"] for fault in schema_faults if fault["rejected"] is not True
    ]
    if unexpected_schema_faults:
        raise ValueError(
            "v9 schema fault injections passed unexpectedly: "
            f"{unexpected_schema_faults}"
        )

    source_copy_fault = copy.deepcopy(tranche)
    source_copy_fault["rows"][0]["protein_names"] = [
        "copied source-side protein name"
    ]
    source_copy_rejection = write_rejection(
        root,
        negative_source_copy_path,
        expected_failure="source_context_copy",
        expected_error_fragment="must not be copied",
        action=lambda: evaluate_tranche(policy, source_copy_fault),
    )
    present_null_fault = copy.deepcopy(tranche)
    for row in present_null_fault["rows"]:
        if row.get("coordinate_state") == "ligand_absent":
            row["ligand_code_from_structure"] = "ATP"
            break
    present_null_rejection = write_rejection(
        root,
        negative_present_null_path,
        expected_failure="missing_present_null_ligand",
        expected_error_fragment="present-but-null ligand_code_from_structure",
        action=lambda: validate_v9_tranche(present_null_fault),
    )
    identity_fault = copy.deepcopy(tranche)
    identity_fault["rows"][0]["source_row_id"] = None
    identity_rejection = write_rejection(
        root,
        negative_identity_path,
        expected_failure="missing_candidate_identity",
        expected_error_fragment="missing candidate identity fields",
        action=lambda: evaluate_tranche(policy, identity_fault),
    )

    observed_targets = sorted(
        tranche["metadata"]["selected_coordinate_state_counts"]
    )
    missing_targets = tranche["metadata"][
        "missing_real_target_coordinate_state_values"
    ]
    primary_outcome = "next_query_defined" if missing_targets else "scoreboard_gate_created"
    next_query = (
        "epk_real_lane_metal_absent_candidate_evidence_v10_review_only"
        if "metal_absent" in missing_targets
        else "epk_real_lane_missing_coordinate_state_full_coverage_v10_review_only"
    )
    contract_gate = {
        "metadata": {
            "artifact_id": f"{ARTIFACT_ID}_contract_gate",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "adapter_version": ARTIFACT_ID,
            "primary_outcome": primary_outcome,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "positive_inputs": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(scoreboard_path, root),
            "scoreboard_gate_sha256": sha256_file(scoreboard_path),
        },
        "positive_contract_summary": contract_summary,
        "schema_fault_injection_results": schema_faults,
        "schema_fault_injection_skipped_reason": schema_faults_skipped_reason,
        "v9_fault_injection_results": [
            source_copy_rejection,
            present_null_rejection,
            identity_rejection,
        ],
        "real_missing_coordinate_state_gate": {
            "gate_pass": True,
            "scoreboard_gate_pass": True,
            "target_coordinate_state_values": list(TARGET_COORDINATE_STATES),
            "observed_real_target_coordinate_state_values": observed_targets,
            "missing_real_target_coordinate_state_values": missing_targets,
            "required_real_target_coordinate_state_values": list(
                REQUIRED_REAL_TARGET_STATES
            ),
            "required_real_target_states_covered": sorted(
                set(observed_targets) & set(REQUIRED_REAL_TARGET_STATES)
            ),
            "all_target_states_covered_by_real_rows": not missing_targets,
            "next_query": next_query,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    write_json(contract_path, contract_gate, pretty=True)

    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "primary_outcome": primary_outcome,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": (
            "Real federated lane rows can replace synthetic missing-coordinate "
            "fixtures only for states that source lanes actually emit as "
            "candidate-level rows; absent target states must become explicit "
            "next-query gaps, not synthetic progress."
        ),
        "real_lane_adapter_summary": {
            "target_coordinate_state_values": list(TARGET_COORDINATE_STATES),
            "observed_real_target_coordinate_state_values": observed_targets,
            "missing_real_target_coordinate_state_values": missing_targets,
            "available_target_coordinate_state_counts": tranche["metadata"][
                "available_target_coordinate_state_counts"
            ],
            "selected_coordinate_state_counts": tranche["metadata"][
                "selected_coordinate_state_counts"
            ],
            "selected_expected_claim_status_counts": tranche["metadata"][
                "selected_expected_claim_status_counts"
            ],
            "selected_rows_compact": tranche["metadata"]["selected_rows_compact"],
            "source_text_and_protein_names_copied": False,
            "ligand_absent_present_null_ligand_code": tranche["metadata"][
                "ligand_absent_present_null_ligand_code"
            ],
            "unavailable_present_null_ligand_code": tranche["metadata"][
                "unavailable_present_null_ligand_code"
            ],
            "metal_absent_real_row_observed": tranche["metadata"][
                "metal_absent_real_row_observed"
            ],
            "next_query": next_query,
        },
        "federated_inputs": tranche["metadata"]["all_scanned_input_summaries"],
        "policy_result": {
            "artifact": rel(result_path, root),
            "sha256": sha256_file(result_path),
            "primary_outcome": result["metadata"]["primary_outcome"],
            "rows_reviewed": result["metadata"]["row_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "expected_claim_status_mismatch_count": result["metadata"][
                "expected_claim_status_mismatch_count"
            ],
            "counterexamples_found": result["metadata"]["counterexamples_found"],
        },
        "scoreboard_gate": {
            "artifact": rel(scoreboard_path, root),
            "sha256": sha256_file(scoreboard_path),
            "gate_pass": scoreboard["gate"]["gate_pass"],
            "summary": scoreboard["scoreboard_summary"],
        },
        "contract_gate": {
            "artifact": rel(contract_path, root),
            "sha256": sha256_file(contract_path),
            "gate_pass": contract_gate["real_missing_coordinate_state_gate"][
                "gate_pass"
            ],
        },
        "negative_fault_injections": [
            source_copy_rejection,
            present_null_rejection,
            identity_rejection,
        ],
        "artifacts": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(scoreboard_path, root),
            "scoreboard_gate_sha256": sha256_file(scoreboard_path),
            "contract_gate": rel(contract_path, root),
            "contract_gate_sha256": sha256_file(contract_path),
            "negative_source_context_copy": rel(negative_source_copy_path, root),
            "negative_source_context_copy_sha256": sha256_file(
                negative_source_copy_path
            ),
            "negative_missing_present_null_ligand": rel(negative_present_null_path, root),
            "negative_missing_present_null_ligand_sha256": sha256_file(
                negative_present_null_path
            ),
            "negative_missing_candidate_identity": rel(negative_identity_path, root),
            "negative_missing_candidate_identity_sha256": sha256_file(
                negative_identity_path
            ),
        },
        "gate": {
            "gate_pass": True,
            "primary_outcome": primary_outcome,
            "scoreboard_gate_pass": scoreboard["gate"]["gate_pass"],
            "all_target_states_covered_by_real_rows": not missing_targets,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    write_json(report_path, report, pretty=True)

    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": scoreboard_path,
        "contract_gate": contract_path,
        "negative_source_context_copy": negative_source_copy_path,
        "negative_missing_present_null_ligand": negative_present_null_path,
        "negative_missing_candidate_identity": negative_identity_path,
        "report": report_path,
    }


def self_test() -> None:
    root = Path.cwd()
    policy_path = Path("/private/tmp/epk_real_missing_coordinate_state_policy.json")
    policy = {
        "metadata": {
            "policy_version": "self_test_policy",
            "policy_id": "self_test_policy",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "threshold_calibrated": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
        },
        "frozen_inputs": {
            "ligand_code_alias_map": {"ATP": ["ATP"], "ANP": ["ANP"]},
            "candidate_distance_cutoff_angstrom": 6.0,
            "required_same_structure_features": [
                "terminal_gamma_equivalent_geometry",
                "local_metal_context",
                "catalytic_site_locality",
                "source_free_acceptor_role_features",
                "same_structure_co_materialization",
            ],
            "accepted_source_free_acceptor_role_policy_ids": [],
        },
        "allowed_predictive_features": [
            "ligand_code_from_structure",
            "terminal_gamma_equivalent_geometry",
            "terminal_gamma_atom_name",
            "nearest_gamma_acceptor_distance_angstrom",
            "local_metal_context",
            "catalytic_site_locality",
            "source_free_acceptor_role_features",
            "source_free_acceptor_role_policy_id",
            "same_structure_co_materialization",
        ],
        "review_only_features": [
            "product_state_context",
            "substrate_acceptor_analog_context",
            "split_state_context",
            "candidate_specific_source_repair",
            "sibling_counterfamily_context",
        ],
        "forbidden_features": list(FORBIDDEN_ROW_FLAGS),
    }
    write_json(policy_path, policy, pretty=True)
    payloads = [
        (
            {
                "lane_id": "epk_substrate_role_identity",
                "path": "substrate_role_identity_fixture.json",
                "row_keys": ("state_only_rows",),
            },
            {
                "state_only_rows": [
                    {
                        "candidate_id": "STADP|gamma=none|acceptor=none",
                        "pdb_id": "STADP",
                        "source_free_evidence": {
                            "coordinate_state": "adp_state",
                            "nucleotide_anchor_atom": {"residue_code": "ADP"},
                            "blocker_class": "product_state_evidence",
                        },
                    },
                    {
                        "candidate_id": "STABS|gamma=none|acceptor=none",
                        "pdb_id": "STABS",
                        "source_free_evidence": {
                            "coordinate_state": "ligand_absent",
                            "blocker_class": "ligand_materialization",
                        },
                    },
                ]
            },
        ),
        (
            {
                "lane_id": "epk_false_positive_hunter",
                "path": "false_positive_fixture.json",
                "row_keys": ("rows",),
            },
            {
                "rows": [
                    {
                        "fixture_id": "FPUNV:unavailable",
                        "pdb_id": "FPUNV",
                        "control_class": "atpase_control",
                        "non_epk_control": True,
                        "candidate": {},
                    }
                ]
            },
        ),
    ]
    tranche = build_tranche_from_payloads(payloads)
    validate_v9_tranche(tranche)
    assert tranche["metadata"]["missing_real_target_coordinate_state_values"] == [
        "metal_absent"
    ]
    result = evaluate_tranche(policy, tranche)
    assert result["metadata"]["expected_claim_status_mismatch_count"] == 0
    output_dir = Path("/private/tmp/epk_real_missing_coordinate_state_self_test")
    write_json(output_dir / "result.json", result, pretty=True)
    gate = build_artifact(root, [output_dir / "result.json"])
    assert gate["gate"]["gate_pass"] is True
    assert set(gate["scoreboard_summary"]["covered_coordinate_state_values"]) == {
        "adp_state",
        "ligand_absent",
        "unavailable_coordinate_state",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a compact review-only v9 adapter gate for real lane rows "
            "covering missing coordinate-state rules."
        )
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    outputs = build_outputs(
        Path.cwd(),
        args.output_dir,
        args.timestamp or timestamp(),
        args.policy,
    )
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
