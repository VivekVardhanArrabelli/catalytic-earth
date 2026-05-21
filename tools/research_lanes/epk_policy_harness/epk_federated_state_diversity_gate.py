#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from epk_candidate_policy_bridge_scoreboard_gate import (
    build_artifact,
    rel,
    summarize_result,
    write_json,
)
from epk_federated_candidate_adapter_smoke import ADAPTERS, load_git_json
from epk_federated_real_overlap_gate import (
    DEFAULT_POLICY,
    REAL_OVERLAP_INPUT_SPECS,
    entry_id_for_raw_row,
    payload_rows_by_entry,
)
from epk_policy_harness import (
    CLAIM_STATUS_VALUES,
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    evaluate_tranche,
    load_json,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4"
REQUIRED_REAL_OVERLAP_COORDINATE_STATES = (
    "active_gamma",
    "adp_state",
    "substrate_acceptor_analog_state",
    "unavailable_coordinate_state",
    "ambiguous_coordinate_state",
)
TARGET_REAL_OVERLAP_CLAIM_STATUSES = (
    "review_only_abstain_product_state",
    "review_only_abstain_analog_state",
    "review_only_abstain_sibling_control",
    "review_only_abstain_topology_ambiguity",
    "review_only_abstain_missing_role_policy",
)
STATE_PRIORITY = {
    "substrate_acceptor_analog_state": 0,
    "adp_state": 1,
    "product_state": 2,
    "split_state": 3,
    "ambiguous_coordinate_state": 4,
    "unavailable_coordinate_state": 5,
    "ligand_absent": 6,
    "metal_absent": 7,
    "active_gamma": 8,
}


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def source_false_fields() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_ROW_FLAGS}


def count_values(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        value = str(row.get(field) or "")
        if value:
            counts[value] += 1
    return dict(sorted(counts.items()))


def adapt_entry_rows(
    spec: dict[str, Any],
    rows_by_entry: dict[str, list[tuple[str, dict[str, Any], int]]],
) -> dict[str, list[dict[str, Any]]]:
    lane_id = str(spec["lane_id"])
    adapted_by_entry: dict[str, list[dict[str, Any]]] = {}
    for entry_id, row_items in rows_by_entry.items():
        for row_key, raw_row, raw_index in row_items:
            adapted = ADAPTERS[lane_id](
                raw_row,
                source_artifact=str(spec["path"]),
                source_row_key=row_key,
                index=raw_index,
            )
            adapted["entry_id"] = entry_id
            adapted["pdb_id"] = adapted.get("pdb_id") or entry_id
            adapted.update(
                {key: adapted.get(key, value) for key, value in source_false_fields().items()}
            )
            adapted_by_entry.setdefault(entry_id, []).append(adapted)
    return adapted_by_entry


def state_diverse_row_key(row: dict[str, Any]) -> tuple[Any, ...]:
    state = str(row.get("coordinate_state") or "")
    claim_status = str(row.get("expected_claim_status") or "")
    return (
        STATE_PRIORITY.get(state, 50),
        claim_status not in TARGET_REAL_OVERLAP_CLAIM_STATUSES,
        str(row.get("row_id") or row.get("candidate_id") or ""),
    )


def representative_rows_for_entry(
    entry_candidates: dict[str, dict[str, list[dict[str, Any]]]],
    entry_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane_id in sorted(entry_candidates[entry_id]):
        candidates = entry_candidates[entry_id][lane_id]
        rows.append(copy.deepcopy(sorted(candidates, key=state_diverse_row_key)[0]))
    return rows


def entry_score(
    rows: list[dict[str, Any]],
    uncovered_states: set[str],
    uncovered_statuses: set[str],
) -> tuple[int, int, int, int, str]:
    states = {str(row.get("coordinate_state") or "") for row in rows}
    statuses = {str(row.get("expected_claim_status") or "") for row in rows}
    non_active_count = sum(
        1 for row in rows if row.get("coordinate_state") != "active_gamma"
    )
    return (
        len(states & uncovered_states) * 100,
        len(statuses & uncovered_statuses) * 20,
        non_active_count * 5,
        len(rows),
        ",".join(sorted(states)),
    )


def select_state_diverse_entries(
    entry_candidates: dict[str, dict[str, list[dict[str, Any]]]],
    *,
    max_entries: int,
    min_entries: int,
) -> list[str]:
    eligible = [
        entry_id
        for entry_id, by_lane in entry_candidates.items()
        if len(by_lane) >= 2
    ]
    if not eligible:
        raise ValueError("state-diversity gate found no real overlapping entries")

    representative_by_entry = {
        entry_id: representative_rows_for_entry(entry_candidates, entry_id)
        for entry_id in eligible
    }
    chosen: list[str] = []
    uncovered_states = set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES)
    uncovered_statuses = set(TARGET_REAL_OVERLAP_CLAIM_STATUSES)

    while uncovered_states or uncovered_statuses:
        remaining = [entry for entry in eligible if entry not in chosen]
        if not remaining:
            break
        best_entry = max(
            remaining,
            key=lambda entry: (
                entry_score(
                    representative_by_entry[entry],
                    uncovered_states,
                    uncovered_statuses,
                ),
                entry,
            ),
        )
        best_score = entry_score(
            representative_by_entry[best_entry],
            uncovered_states,
            uncovered_statuses,
        )
        if best_score[:4] == (0, 0, 0, 0):
            break
        chosen.append(best_entry)
        for row in representative_by_entry[best_entry]:
            uncovered_states.discard(str(row.get("coordinate_state") or ""))
            uncovered_statuses.discard(str(row.get("expected_claim_status") or ""))
        if len(chosen) >= max_entries:
            break

    for entry_id in sorted(
        eligible,
        key=lambda entry: (
            -sum(
                1
                for row in representative_by_entry[entry]
                if row.get("coordinate_state") != "active_gamma"
            ),
            entry,
        ),
    ):
        if len(chosen) >= max_entries or len(chosen) >= min_entries:
            break
        if entry_id not in chosen:
            chosen.append(entry_id)

    return chosen[:max_entries]


def refresh_state_metadata(tranche: dict[str, Any]) -> None:
    rows = tranche["rows"]
    source_lanes = sorted({str(row["source_lane_id"]) for row in rows})
    entry_ids: list[str] = []
    for row in rows:
        entry_id = str(row.get("entry_id") or "")
        if entry_id and entry_id not in entry_ids:
            entry_ids.append(entry_id)
    coordinate_state_counts = count_values(rows, "coordinate_state")
    claim_status_counts = count_values(rows, "expected_claim_status")
    covered_required = sorted(
        set(coordinate_state_counts) & set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES)
    )
    uncovered_required = sorted(
        set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES) - set(coordinate_state_counts)
    )
    tranche["metadata"].update(
        {
            "row_count": len(rows),
            "source_lanes": source_lanes,
            "source_lane_count": len(source_lanes),
            "selected_overlap_entry_ids": entry_ids,
            "selected_overlap_entry_count": len(entry_ids),
            "selected_entry_source_lanes": {
                entry_id: sorted(
                    {
                        str(row["source_lane_id"])
                        for row in rows
                        if row.get("entry_id") == entry_id
                    }
                )
                for entry_id in entry_ids
            },
            "selected_coordinate_state_counts": coordinate_state_counts,
            "selected_expected_claim_status_counts": claim_status_counts,
            "covered_required_real_overlap_coordinate_state_values": covered_required,
            "uncovered_required_real_overlap_coordinate_state_values": uncovered_required,
            "covered_requested_coordinate_state_values": sorted(
                set(coordinate_state_counts) & COORDINATE_STATE_VALUES
            ),
            "uncovered_requested_coordinate_state_values": sorted(
                COORDINATE_STATE_VALUES - set(coordinate_state_counts)
            ),
        }
    )


def build_tranche_from_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    *,
    max_entries: int,
    min_entries: int,
) -> dict[str, Any]:
    raw_rows_by_lane: dict[str, dict[str, list[tuple[str, dict[str, Any], int]]]] = {}
    adapted_by_entry: dict[str, dict[str, list[dict[str, Any]]]] = {}
    all_input_summaries: list[dict[str, Any]] = []
    entry_source_lanes: dict[str, set[str]] = {}

    for spec, payload in payloads:
        lane_id = str(spec["lane_id"])
        rows_by_entry = payload_rows_by_entry(spec, payload)
        raw_rows_by_lane[lane_id] = rows_by_entry
        adapted = adapt_entry_rows(spec, rows_by_entry)
        for entry_id, rows in adapted.items():
            adapted_by_entry.setdefault(entry_id, {})[lane_id] = rows
            entry_source_lanes.setdefault(entry_id, set()).add(lane_id)

    overlap_entry_ids = [
        entry_id for entry_id, lanes in entry_source_lanes.items() if len(lanes) >= 2
    ]
    available_representative_rows: list[dict[str, Any]] = []
    for entry_id in overlap_entry_ids:
        available_representative_rows.extend(
            representative_rows_for_entry(adapted_by_entry, entry_id)
        )

    selected_entry_ids = select_state_diverse_entries(
        adapted_by_entry,
        max_entries=max_entries,
        min_entries=min_entries,
    )
    selected_rows: list[dict[str, Any]] = []
    for entry_id in selected_entry_ids:
        selected_rows.extend(representative_rows_for_entry(adapted_by_entry, entry_id))

    selected_counts_by_lane = Counter(str(row["source_lane_id"]) for row in selected_rows)
    selected_lanes = sorted(selected_counts_by_lane)
    for spec, payload in payloads:
        lane_id = str(spec["lane_id"])
        row_count = sum(len(rows) for rows in raw_rows_by_lane[lane_id].values())
        all_input_summaries.append(
            {
                "lane_id": lane_id,
                "ref": spec.get("ref"),
                "artifact": spec["path"],
                "row_keys": list(spec["row_keys"]),
                "available_row_count": row_count,
                "available_entry_count": len(raw_rows_by_lane[lane_id]),
                "available_overlap_entry_count": sum(
                    1
                    for entry_id in raw_rows_by_lane[lane_id]
                    if len(entry_source_lanes.get(entry_id, set())) >= 2
                ),
                "selected_row_count": selected_counts_by_lane.get(lane_id, 0),
                "selected_entry_count": sum(
                    1
                    for entry_id in selected_entry_ids
                    if lane_id in adapted_by_entry.get(entry_id, {})
                ),
                "review_only_input": True,
            }
        )

    tranche = {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "available_overlap_entry_count": len(overlap_entry_ids),
            "available_overlap_coordinate_state_counts": count_values(
                available_representative_rows, "coordinate_state"
            ),
            "available_overlap_expected_claim_status_counts": count_values(
                available_representative_rows, "expected_claim_status"
            ),
            "input_summaries": [
                summary for summary in all_input_summaries if summary["lane_id"] in selected_lanes
            ],
            "all_scanned_input_summaries": all_input_summaries,
            "require_candidate_identity_fields": True,
            "requested_coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
            "required_real_overlap_coordinate_state_values": list(
                REQUIRED_REAL_OVERLAP_COORDINATE_STATES
            ),
            "target_real_overlap_claim_status_values": list(
                TARGET_REAL_OVERLAP_CLAIM_STATUSES
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
            "state_diversity_gate_contract": {
                "entry_ids_from_real_cross_lane_artifact_intersections": True,
                "every_selected_entry_has_at_least_two_source_lanes": True,
                "selected_rows_are_candidate_level": True,
                "coordinate_state_first_class_in_policy_decisions": True,
                "claim_admissibility_separate_from_discovery_signal": True,
                "product_adp_analog_split_states_review_only": True,
                "source_text_and_protein_names_not_copied": True,
                "progress_claim_allowed": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            },
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "rows": selected_rows,
    }
    refresh_state_metadata(tranche)
    return tranche


def validate_state_diversity_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("state-diversity gate requires review_only=true")
    contract = metadata.get("state_diversity_gate_contract")
    if not isinstance(contract, dict):
        raise ValueError("state-diversity gate requires metadata.state_diversity_gate_contract")
    for flag in (
        "entry_ids_from_real_cross_lane_artifact_intersections",
        "every_selected_entry_has_at_least_two_source_lanes",
        "selected_rows_are_candidate_level",
        "coordinate_state_first_class_in_policy_decisions",
        "claim_admissibility_separate_from_discovery_signal",
        "product_adp_analog_split_states_review_only",
        "source_text_and_protein_names_not_copied",
    ):
        if contract.get(flag) is not True:
            raise ValueError(f"state-diversity gate requires {flag}=true")
    for flag in (
        "progress_claim_allowed",
        "production_claim_allowed",
        "labels_or_fingerprints_changed",
    ):
        if contract.get(flag) is not False:
            raise ValueError(f"state-diversity gate requires {flag}=false")

    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("state-diversity gate requires non-empty rows")

    entry_lanes: dict[str, set[str]] = {}
    for row in rows:
        row_id = str(row.get("row_id") or row.get("pdb_id") or "unknown_row")
        entry_id = str(row.get("entry_id") or "").strip()
        if not entry_id:
            raise ValueError(f"state-diversity gate requires entry_id on every row: {row_id}")
        source_lane_id = str(row.get("source_lane_id") or "").strip()
        if not source_lane_id:
            raise ValueError(
                f"state-diversity gate requires source_lane_id on every row: {row_id}"
            )
        entry_lanes.setdefault(entry_id, set()).add(source_lane_id)
    single_lane_entries = {
        entry_id: sorted(lanes)
        for entry_id, lanes in entry_lanes.items()
        if len(lanes) < 2
    }
    if single_lane_entries:
        raise ValueError(
            "state-diversity gate requires every selected entry to contain "
            f"candidate rows from at least two source lanes: {single_lane_entries}"
        )

    selected_states = {str(row.get("coordinate_state") or "") for row in rows}
    missing_required = sorted(
        set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES) - selected_states
    )
    if missing_required:
        raise ValueError(
            "state-diversity gate requires coordinate-state coverage for current "
            f"real-overlap states: {missing_required}"
        )
    non_active_count = sum(1 for state in selected_states if state != "active_gamma")
    if non_active_count < 3:
        raise ValueError("state-diversity gate requires at least three non-active states")

    selected_entries = [str(entry) for entry in metadata.get("selected_overlap_entry_ids", [])]
    if sorted(selected_entries) != sorted(entry_lanes):
        raise ValueError("state-diversity gate selected_overlap_entry_ids drifted from rows")
    if metadata.get("selected_coordinate_state_counts") != count_values(
        rows, "coordinate_state"
    ):
        raise ValueError("state-diversity gate coordinate-state counts drifted from rows")


def validate_state_diversity_scoreboard(gate: dict[str, Any]) -> None:
    if gate.get("gate", {}).get("gate_pass") is not True:
        raise ValueError("state-diversity scoreboard gate must pass")
    summary = gate.get("scoreboard_summary", {})
    covered_states = set(summary.get("covered_coordinate_state_values") or [])
    missing_required = sorted(
        set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES) - covered_states
    )
    if missing_required:
        raise ValueError(
            "state-diversity scoreboard missed required coordinate states: "
            f"{missing_required}"
        )
    for scoreboard_row in gate.get("scoreboard_rows", []):
        for rollup in scoreboard_row.get("entry_rollups", []):
            if len(rollup.get("source_lane_ids") or []) < 2:
                raise ValueError(
                    "state-diversity scoreboard contains single-lane entry rollup: "
                    f"{rollup.get('entry_id')}"
                )
            if rollup.get("progress_claim_allowed") is not False:
                raise ValueError("state-diversity scoreboard must not allow progress claims")
            if rollup.get("production_claim_allowed") is not False:
                raise ValueError(
                    "state-diversity scoreboard must not allow production claims"
                )


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


def recompute_result_metadata_counts(result: dict[str, Any]) -> None:
    rows = result.get("rows", [])
    result["metadata"]["row_count"] = len(rows)
    result["metadata"]["claim_status_counts"] = count_values(rows, "claim_status")
    result["metadata"]["coordinate_state_counts"] = count_values(rows, "coordinate_state")


def write_unsafe_control_fault(
    root: Path,
    path: Path,
    result: dict[str, Any],
) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    row = mutated["rows"][0]
    row["row_id"] = "fault:state_diversity_unsafe_control_nonabstention"
    row["row_role"] = "sibling_control"
    row["claim_status"] = "review_only_nonabstaining_candidate"
    row["claim_admissibility"] = "review_only"
    row["abstention_reasons"] = []
    row["sibling_control_match_status"] = "unsafe_nonabstaining_control_fixture"
    mutated["metadata"]["fault_injection_expected_failure"] = (
        "unsafe_control_nonabstention"
    )
    recompute_result_metadata_counts(mutated)
    write_json(path, mutated, pretty=True)
    summary = summarize_result(root, path, mutated)
    if summary["gate_pass"] is not False:
        raise ValueError("unsafe control nonabstention fault must fail scoreboard gate")
    return {
        "artifact": rel(path, root),
        "sha256": sha256_file(path),
        "expected_failure": "unsafe_control_nonabstention",
        "rejected": True,
        "unsafe_control_nonabstention_count": summary[
            "unsafe_control_nonabstention_count"
        ],
        "unsafe_control_nonabstention_rows": summary[
            "unsafe_control_nonabstention_rows"
        ],
    }


def mutate_required_state_to_active(tranche: dict[str, Any], state: str) -> dict[str, Any]:
    mutated = copy.deepcopy(tranche)
    for row in mutated["rows"]:
        if row.get("coordinate_state") == state:
            row["coordinate_state"] = "active_gamma"
            row["ligand_code_from_structure"] = "ATP"
            row["terminal_gamma_equivalent_geometry"] = True
            row["terminal_gamma_atom_name"] = "PG"
            row["product_state_context"] = False
            row["substrate_acceptor_analog_context"] = False
            row["split_state_context"] = False
            row["ligand_context"] = None
            row["expected_claim_status"] = "review_only_abstain_missing_role_policy"
            break
    refresh_state_metadata(mutated)
    return mutated


def build_outputs(
    root: Path,
    output_dir: Path,
    run_stamp: str,
    policy_path: Path,
    *,
    max_entries: int,
    min_entries: int,
) -> dict[str, Path]:
    payloads = [
        (dict(spec), load_git_json(str(spec["ref"]), str(spec["path"])))
        for spec in REAL_OVERLAP_INPUT_SPECS
    ]
    policy = load_json(policy_path)
    tranche = build_tranche_from_payloads(
        payloads,
        max_entries=max_entries,
        min_entries=min_entries,
    )
    validate_state_diversity_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("state-diversity gate produced claim-status mismatches")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    report_path = output_dir / f"{stem}.json"
    negative_single_lane_path = (
        output_dir / f"{stem}_negative_single_lane_entry_result.json"
    )
    negative_missing_state_path = (
        output_dir / f"{stem}_negative_missing_state_diversity_result.json"
    )
    negative_source_copy_path = (
        output_dir / f"{stem}_negative_source_context_copy_result.json"
    )
    negative_unsafe_control_path = (
        output_dir / f"{stem}_negative_unsafe_control_nonabstention_result.json"
    )

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)
    gate = build_artifact(root, [result_path])
    validate_state_diversity_scoreboard(gate)
    write_json(gate_path, gate, pretty=True)

    single_lane_fault = copy.deepcopy(tranche)
    first_entry = single_lane_fault["metadata"]["selected_overlap_entry_ids"][0]
    first_lane = next(
        row["source_lane_id"]
        for row in single_lane_fault["rows"]
        if row.get("entry_id") == first_entry
    )
    single_lane_fault["rows"] = [
        row
        for row in single_lane_fault["rows"]
        if row.get("entry_id") != first_entry or row.get("source_lane_id") == first_lane
    ]
    refresh_state_metadata(single_lane_fault)
    single_lane_rejection = write_rejection(
        root,
        negative_single_lane_path,
        expected_failure="single_lane_entry",
        expected_error_fragment="at least two source lanes",
        action=lambda: validate_state_diversity_tranche(single_lane_fault),
    )

    missing_state_fault = mutate_required_state_to_active(tranche, "adp_state")
    missing_state_rejection = write_rejection(
        root,
        negative_missing_state_path,
        expected_failure="missing_state_diversity",
        expected_error_fragment="coordinate-state coverage",
        action=lambda: validate_state_diversity_tranche(missing_state_fault),
    )

    source_copy_fault = copy.deepcopy(tranche)
    source_copy_fault["rows"][0]["protein_names"] = ["copied source-side protein name"]
    source_copy_rejection = write_rejection(
        root,
        negative_source_copy_path,
        expected_failure="source_context_copy",
        expected_error_fragment="must not be copied",
        action=lambda: evaluate_tranche(policy, source_copy_fault),
    )
    unsafe_control_rejection = write_unsafe_control_fault(
        root,
        negative_unsafe_control_path,
        result,
    )

    selected_state_counts = tranche["metadata"]["selected_coordinate_state_counts"]
    requested_uncovered = tranche["metadata"]["uncovered_requested_coordinate_state_values"]
    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "primary_outcome": "scoreboard_gate_created",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": (
            "Real cross-lane overlapping ePK candidate rows can exercise "
            "coordinate-state diversity only when coordinate_state remains a "
            "first-class policy-decision field and state blockers stay review-only."
        ),
        "state_diversity_summary": {
            "available_overlap_entry_count": tranche["metadata"][
                "available_overlap_entry_count"
            ],
            "selected_overlap_entry_count": tranche["metadata"][
                "selected_overlap_entry_count"
            ],
            "selected_overlap_entry_ids": tranche["metadata"][
                "selected_overlap_entry_ids"
            ],
            "selected_entry_source_lanes": tranche["metadata"][
                "selected_entry_source_lanes"
            ],
            "available_overlap_coordinate_state_counts": tranche["metadata"][
                "available_overlap_coordinate_state_counts"
            ],
            "selected_coordinate_state_counts": selected_state_counts,
            "covered_required_real_overlap_coordinate_state_values": tranche[
                "metadata"
            ]["covered_required_real_overlap_coordinate_state_values"],
            "uncovered_required_real_overlap_coordinate_state_values": tranche[
                "metadata"
            ]["uncovered_required_real_overlap_coordinate_state_values"],
            "uncovered_requested_coordinate_state_values": requested_uncovered,
            "literal_product_or_split_real_overlap_rows_available": any(
                state in selected_state_counts for state in ("product_state", "split_state")
            ),
            "source_text_and_protein_names_copied": False,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
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
            "artifact": rel(gate_path, root),
            "sha256": sha256_file(gate_path),
            "gate_pass": gate["gate"]["gate_pass"],
            "summary": gate["scoreboard_summary"],
        },
        "negative_fault_injections": [
            single_lane_rejection,
            missing_state_rejection,
            source_copy_rejection,
            unsafe_control_rejection,
        ],
        "artifacts": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(gate_path, root),
            "scoreboard_gate_sha256": sha256_file(gate_path),
            "negative_single_lane_entry": rel(negative_single_lane_path, root),
            "negative_single_lane_entry_sha256": sha256_file(negative_single_lane_path),
            "negative_missing_state_diversity": rel(negative_missing_state_path, root),
            "negative_missing_state_diversity_sha256": sha256_file(
                negative_missing_state_path
            ),
            "negative_source_context_copy": rel(negative_source_copy_path, root),
            "negative_source_context_copy_sha256": sha256_file(negative_source_copy_path),
            "negative_unsafe_control_nonabstention": rel(negative_unsafe_control_path, root),
            "negative_unsafe_control_nonabstention_sha256": sha256_file(
                negative_unsafe_control_path
            ),
        },
        "gate": {
            "gate_pass": gate["gate"]["gate_pass"],
            "state_diversity_gate_pass": True,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
        },
    }
    write_json(report_path, report, pretty=True)
    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": gate_path,
        "negative_single_lane_entry": negative_single_lane_path,
        "negative_missing_state_diversity": negative_missing_state_path,
        "negative_source_context_copy": negative_source_copy_path,
        "negative_unsafe_control_nonabstention": negative_unsafe_control_path,
        "report": report_path,
    }


def self_test() -> None:
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
    payloads = [
        (
            {
                "lane_id": "epk_positive_evidence",
                "path": "positive_fixture.json",
                "row_keys": ("adjudicated_candidate_rows",),
            },
            {
                "adjudicated_candidate_rows": [
                    {
                        "candidate_id": "3QHW:analog",
                        "pdb_id": "3QHW",
                        "coordinate_state": "transition_analog",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ANP",
                            "terminal_atom_name": "PN",
                            "nearest_terminal_distance_angstrom": 3.2,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "SER",
                        },
                    },
                    {
                        "candidate_id": "4HPU:active",
                        "pdb_id": "4HPU",
                        "coordinate_state": "active_gamma",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ANP",
                            "terminal_atom_name": "PG",
                            "nearest_terminal_distance_angstrom": 4.0,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "TYR",
                        },
                    },
                ]
            },
        ),
        (
            {
                "lane_id": "epk_substrate_role_identity",
                "path": "substrate_fixture.json",
                "row_keys": ("candidate_evidence_rows", "state_only_rows"),
            },
            {
                "candidate_evidence_rows": [
                    {
                        "candidate_id": "9NBW:active",
                        "pdb_id": "9NBW",
                        "source_free_evidence": {
                            "coordinate_state": "active_gamma",
                            "terminal_gamma_atom": {
                                "residue_code": "ATP",
                                "atom_name": "PG",
                            },
                            "acceptor_atom": {"residue_code": "SER"},
                            "distance_angstrom": 3.5,
                            "terminal_gamma_equivalent_atom_available": True,
                            "blocker_class": "none",
                        },
                    }
                ],
                "state_only_rows": [
                    {
                        "candidate_id": "3QHW:adp",
                        "pdb_id": "3QHW",
                        "source_free_evidence": {
                            "coordinate_state": "adp_state",
                            "terminal_gamma_atom": {
                                "residue_code": "ADP",
                                "atom_name": "PB",
                            },
                            "blocker_class": "product_state_evidence",
                        },
                    },
                    {
                        "candidate_id": "4HPU:ambiguous",
                        "pdb_id": "4HPU",
                        "source_free_evidence": {
                            "coordinate_state": "ambiguous_coordinate_state",
                            "terminal_gamma_atom": {
                                "residue_code": "ANP",
                                "atom_name": "PG",
                            },
                            "blocker_class": "topology_ambiguity",
                        },
                    },
                ],
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
                        "fixture_id": "9NBW:unavailable",
                        "pdb_id": "9NBW",
                        "control_class": "atpase_non_epk_control",
                        "non_epk_control": True,
                        "candidate": {},
                    }
                ]
            },
        ),
    ]
    tranche = build_tranche_from_payloads(payloads, max_entries=5, min_entries=3)
    validate_state_diversity_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    assert result["metadata"]["expected_claim_status_mismatch_count"] == 0
    result_path = Path("/private/tmp/epk_state_diversity_gate_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(Path.cwd(), [result_path])
    validate_state_diversity_scoreboard(gate)
    assert set(REQUIRED_REAL_OVERLAP_COORDINATE_STATES).issubset(
        set(gate["scoreboard_summary"]["covered_coordinate_state_values"])
    )
    bad = mutate_required_state_to_active(tranche, "adp_state")
    try:
        validate_state_diversity_tranche(bad)
    except ValueError as error:
        assert "coordinate-state coverage" in str(error)
    else:
        raise AssertionError("missing state-diversity fixture must fail")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a compact review-only real-overlap state-diversity gate from "
            "independent ePK candidate-evidence lanes."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_policy_harness"),
    )
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-entries", type=int, default=5)
    parser.add_argument("--min-entries", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0
    if args.max_entries <= 0:
        parser.error("--max-entries must be positive")
    if args.min_entries <= 0:
        parser.error("--min-entries must be positive")
    if args.min_entries > args.max_entries:
        parser.error("--min-entries must be <= --max-entries")

    run_stamp = args.timestamp or timestamp()
    outputs = build_outputs(
        Path.cwd(),
        args.output_dir,
        run_stamp,
        args.policy,
        max_entries=args.max_entries,
        min_entries=args.min_entries,
    )
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
