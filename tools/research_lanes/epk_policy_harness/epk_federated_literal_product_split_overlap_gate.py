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
    entry_id_for_raw_row,
    payload_rows_by_entry,
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
ARTIFACT_ID = "epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5"
TARGET_COORDINATE_STATES = ("product_state", "split_state")
TARGET_STATE_TO_STATUS = {
    "product_state": "review_only_abstain_product_state",
    "split_state": "review_only_abstain_split_state",
}
REAL_OVERLAP_INPUT_SPECS_V5 = (
    {
        "lane_id": "epk_positive_evidence",
        "ref": "origin/research/epk-positive-evidence",
        "path": "artifacts/research_lanes/epk_positive_evidence/candidate_source_adjudication_all_20260521.json",
        "row_keys": ("adjudicated_candidate_rows",),
    },
    {
        "lane_id": "epk_substrate_role_identity",
        "ref": "origin/research/epk-substrate-role-identity",
        "path": "artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json",
        "row_keys": ("phosphoproduct_materialization_rows",),
    },
    {
        "lane_id": "epk_false_positive_hunter",
        "ref": "origin/research/epk-false-positive-hunter",
        "path": "artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json",
        "row_keys": ("rows",),
    },
    {
        "lane_id": "epk_sibling_controls",
        "ref": "origin/research/epk-sibling-controls",
        "path": "artifacts/research_lanes/epk_sibling_controls/review_only_counteraxis_scorer_test_matrix_20260520.json",
        "row_keys": (
            "gamma_proximity_counteraxis_cases",
            "product_phosphoryl_identity_counteraxis_cases",
        ),
    },
)


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


def raw_row_count(payload: dict[str, Any], row_keys: tuple[str, ...]) -> int:
    total = 0
    for key in row_keys:
        value = payload.get(key, [])
        if isinstance(value, list):
            total += sum(1 for row in value if isinstance(row, dict))
    return total


def adapt_payload_rows(
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


def compact_row_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "entry_id": row.get("entry_id"),
        "candidate_id": row.get("candidate_id"),
        "source_lane_id": row.get("source_lane_id"),
        "source_row_key": row.get("source_row_key"),
        "coordinate_state": row.get("coordinate_state"),
        "expected_claim_status": row.get("expected_claim_status"),
        "ligand_code_from_structure": row.get("ligand_code_from_structure"),
        "nearest_gamma_acceptor_distance_angstrom": row.get(
            "nearest_gamma_acceptor_distance_angstrom"
        ),
    }


def representative_row_key(row: dict[str, Any]) -> tuple[Any, ...]:
    state = str(row.get("coordinate_state") or "")
    return (
        state not in TARGET_COORDINATE_STATES,
        state != "substrate_acceptor_analog_state",
        str(row.get("row_id") or row.get("candidate_id") or ""),
    )


def select_literal_entries(
    adapted_by_entry: dict[str, dict[str, list[dict[str, Any]]]],
    *,
    max_entries: int,
) -> list[str]:
    literal_entries = [
        entry_id
        for entry_id, lanes in adapted_by_entry.items()
        if len(lanes) >= 2
        and any(
            row.get("coordinate_state") in TARGET_COORDINATE_STATES
            for lane_rows in lanes.values()
            for row in lane_rows
        )
    ]
    if not literal_entries:
        raise ValueError(
            "literal product/split real-overlap gate found no overlapping entries"
        )

    def score(entry_id: str) -> tuple[int, int, int, str]:
        rows = [
            row
            for lane_rows in adapted_by_entry[entry_id].values()
            for row in lane_rows
        ]
        states = {str(row.get("coordinate_state") or "") for row in rows}
        target_count = sum(
            1 for row in rows if row.get("coordinate_state") in TARGET_COORDINATE_STATES
        )
        return (
            len(states & set(TARGET_COORDINATE_STATES)),
            target_count,
            len(adapted_by_entry[entry_id]),
            entry_id,
        )

    selected: list[str] = []
    uncovered = set(TARGET_COORDINATE_STATES)
    while uncovered:
        remaining = [entry for entry in literal_entries if entry not in selected]
        if not remaining:
            break
        best = max(remaining, key=score)
        selected.append(best)
        for lane_rows in adapted_by_entry[best].values():
            for row in lane_rows:
                uncovered.discard(str(row.get("coordinate_state") or ""))
        if len(selected) >= max_entries:
            break

    for entry_id in sorted(literal_entries, key=lambda entry: (-score(entry)[1], entry)):
        if len(selected) >= max_entries:
            break
        if entry_id not in selected:
            selected.append(entry_id)
    return selected[:max_entries]


def selected_rows_for_entry(
    entry_id: str,
    lane_rows: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for lane_id in sorted(lane_rows):
        rows = lane_rows[lane_id]
        target_rows = [
            copy.deepcopy(row)
            for row in rows
            if row.get("coordinate_state") in TARGET_COORDINATE_STATES
        ]
        if target_rows:
            selected.extend(sorted(target_rows, key=representative_row_key))
            continue
        selected.append(copy.deepcopy(sorted(rows, key=representative_row_key)[0]))
    return selected


def refresh_literal_metadata(tranche: dict[str, Any]) -> None:
    rows = tranche["rows"]
    entry_ids: list[str] = []
    for row in rows:
        entry_id = str(row.get("entry_id") or "")
        if entry_id and entry_id not in entry_ids:
            entry_ids.append(entry_id)
    target_rows = [
        row for row in rows if row.get("coordinate_state") in TARGET_COORDINATE_STATES
    ]
    tranche["metadata"].update(
        {
            "row_count": len(rows),
            "source_lanes": sorted({str(row["source_lane_id"]) for row in rows}),
            "source_lane_count": len({str(row["source_lane_id"]) for row in rows}),
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
            "selected_coordinate_state_counts": count_values(rows, "coordinate_state"),
            "selected_expected_claim_status_counts": count_values(
                rows, "expected_claim_status"
            ),
            "literal_target_row_count": len(target_rows),
            "literal_target_coordinate_state_counts": count_values(
                target_rows, "coordinate_state"
            ),
            "covered_literal_target_coordinate_state_values": sorted(
                set(count_values(target_rows, "coordinate_state"))
                & set(TARGET_COORDINATE_STATES)
            ),
            "uncovered_literal_target_coordinate_state_values": sorted(
                set(TARGET_COORDINATE_STATES)
                - set(count_values(target_rows, "coordinate_state"))
            ),
            "uncovered_requested_coordinate_state_values": sorted(
                COORDINATE_STATE_VALUES - set(count_values(rows, "coordinate_state"))
            ),
        }
    )


def build_tranche_from_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    *,
    max_entries: int,
) -> dict[str, Any]:
    raw_rows_by_lane: dict[str, dict[str, list[tuple[str, dict[str, Any], int]]]] = {}
    adapted_by_entry: dict[str, dict[str, list[dict[str, Any]]]] = {}
    entry_source_lanes: dict[str, set[str]] = {}
    input_summaries: list[dict[str, Any]] = []

    for spec, payload in payloads:
        lane_id = str(spec["lane_id"])
        rows_by_entry = payload_rows_by_entry(spec, payload)
        raw_rows_by_lane[lane_id] = rows_by_entry
        adapted = adapt_payload_rows(spec, rows_by_entry)
        for entry_id, rows in adapted.items():
            adapted_by_entry.setdefault(entry_id, {})[lane_id] = rows
            entry_source_lanes.setdefault(entry_id, set()).add(lane_id)

    overlap_entry_ids = [
        entry_id for entry_id, lanes in entry_source_lanes.items() if len(lanes) >= 2
    ]
    overlap_rows = [
        row
        for entry_id in overlap_entry_ids
        for lane_rows in adapted_by_entry[entry_id].values()
        for row in lane_rows
    ]
    literal_overlap_rows = [
        row for row in overlap_rows if row.get("coordinate_state") in TARGET_COORDINATE_STATES
    ]
    selected_entry_ids = select_literal_entries(
        adapted_by_entry,
        max_entries=max_entries,
    )
    selected_rows: list[dict[str, Any]] = []
    for entry_id in selected_entry_ids:
        selected_rows.extend(selected_rows_for_entry(entry_id, adapted_by_entry[entry_id]))

    selected_counts_by_lane = Counter(str(row["source_lane_id"]) for row in selected_rows)
    for spec, payload in payloads:
        lane_id = str(spec["lane_id"])
        input_summaries.append(
            {
                "lane_id": lane_id,
                "ref": spec.get("ref"),
                "artifact": spec["path"],
                "row_keys": list(spec["row_keys"]),
                "available_row_count": raw_row_count(payload, tuple(spec["row_keys"])),
                "available_entry_count": len(raw_rows_by_lane[lane_id]),
                "available_overlap_entry_count": sum(
                    1
                    for entry_id in raw_rows_by_lane[lane_id]
                    if len(entry_source_lanes.get(entry_id, set())) >= 2
                ),
                "available_literal_overlap_row_count": sum(
                    1
                    for row in literal_overlap_rows
                    if row.get("source_lane_id") == lane_id
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
                overlap_rows, "coordinate_state"
            ),
            "available_literal_overlap_row_count": len(literal_overlap_rows),
            "available_literal_overlap_coordinate_state_counts": count_values(
                literal_overlap_rows, "coordinate_state"
            ),
            "available_literal_overlap_rows_compact": [
                compact_row_summary(row)
                for row in sorted(
                    literal_overlap_rows,
                    key=lambda row: (
                        str(row.get("coordinate_state") or ""),
                        str(row.get("entry_id") or ""),
                        str(row.get("candidate_id") or ""),
                    ),
                )
            ],
            "all_scanned_input_summaries": input_summaries,
            "input_summaries": [
                summary for summary in input_summaries if summary["selected_row_count"] > 0
            ],
            "requested_coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
            "literal_target_coordinate_state_values": list(TARGET_COORDINATE_STATES),
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
            "literal_product_split_gate_contract": {
                "entry_ids_from_real_cross_lane_artifact_intersections": True,
                "every_selected_entry_has_at_least_two_source_lanes": True,
                "literal_product_state_rows_required": True,
                "literal_split_state_rows_required": True,
                "target_state_rows_are_review_only_abstentions": True,
                "entry_status_derived_from_candidate_decisions": True,
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
    refresh_literal_metadata(tranche)
    return tranche


def validate_literal_product_split_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("literal product/split gate requires review_only=true")
    contract = metadata.get("literal_product_split_gate_contract")
    if not isinstance(contract, dict):
        raise ValueError(
            "literal product/split gate requires metadata.literal_product_split_gate_contract"
        )
    for flag in (
        "entry_ids_from_real_cross_lane_artifact_intersections",
        "every_selected_entry_has_at_least_two_source_lanes",
        "literal_product_state_rows_required",
        "literal_split_state_rows_required",
        "target_state_rows_are_review_only_abstentions",
        "entry_status_derived_from_candidate_decisions",
        "source_text_and_protein_names_not_copied",
    ):
        if contract.get(flag) is not True:
            raise ValueError(f"literal product/split gate requires {flag}=true")
    for flag in (
        "progress_claim_allowed",
        "production_claim_allowed",
        "labels_or_fingerprints_changed",
    ):
        if contract.get(flag) is not False:
            raise ValueError(f"literal product/split gate requires {flag}=false")

    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("literal product/split gate requires non-empty rows")
    entry_lanes: dict[str, set[str]] = {}
    for row in rows:
        row_id = str(row.get("row_id") or row.get("candidate_id") or "unknown_row")
        entry_id = str(row.get("entry_id") or "").strip()
        if not entry_id:
            raise ValueError(
                f"literal product/split gate requires entry_id on every row: {row_id}"
            )
        source_lane_id = str(row.get("source_lane_id") or "").strip()
        if not source_lane_id:
            raise ValueError(
                f"literal product/split gate requires source_lane_id on every row: {row_id}"
            )
        entry_lanes.setdefault(entry_id, set()).add(source_lane_id)
        state = str(row.get("coordinate_state") or "")
        if state in TARGET_STATE_TO_STATUS:
            expected_status = TARGET_STATE_TO_STATUS[state]
            if row.get("expected_claim_status") != expected_status:
                raise ValueError(
                    "literal product/split target rows must expect review-only "
                    f"state abstention: {row_id}"
                )
            if row.get("expected_frozen_policy_decision") != "review_only_abstain":
                raise ValueError(
                    "literal product/split target rows must expect review_only_abstain: "
                    f"{row_id}"
                )

    single_lane_entries = {
        entry_id: sorted(lanes)
        for entry_id, lanes in entry_lanes.items()
        if len(lanes) < 2
    }
    if single_lane_entries:
        raise ValueError(
            "literal product/split gate requires every selected entry to contain "
            f"candidate rows from at least two source lanes: {single_lane_entries}"
        )
    selected_states = {str(row.get("coordinate_state") or "") for row in rows}
    missing_targets = sorted(set(TARGET_COORDINATE_STATES) - selected_states)
    if missing_targets:
        raise ValueError(
            "literal product/split gate requires literal coordinate-state coverage: "
            f"{missing_targets}"
        )
    declared_entries = [str(entry) for entry in metadata.get("selected_overlap_entry_ids", [])]
    if sorted(declared_entries) != sorted(entry_lanes):
        raise ValueError(
            "literal product/split gate selected_overlap_entry_ids drifted from rows"
        )
    if metadata.get("selected_coordinate_state_counts") != count_values(
        rows, "coordinate_state"
    ):
        raise ValueError(
            "literal product/split gate coordinate-state counts drifted from rows"
        )


def validate_literal_product_split_scoreboard(gate: dict[str, Any]) -> None:
    if gate.get("gate", {}).get("gate_pass") is not True:
        raise ValueError("literal product/split scoreboard gate must pass")
    summary = gate.get("scoreboard_summary", {})
    covered_states = set(summary.get("covered_coordinate_state_values") or [])
    missing_targets = sorted(set(TARGET_COORDINATE_STATES) - covered_states)
    if missing_targets:
        raise ValueError(
            "literal product/split scoreboard missed required coordinate states: "
            f"{missing_targets}"
        )
    for scoreboard_row in gate.get("scoreboard_rows", []):
        for rollup in scoreboard_row.get("entry_rollups", []):
            if len(rollup.get("source_lane_ids") or []) < 2:
                raise ValueError(
                    "literal product/split scoreboard contains single-lane entry rollup: "
                    f"{rollup.get('entry_id')}"
                )
            if rollup.get("progress_claim_allowed") is not False:
                raise ValueError(
                    "literal product/split scoreboard must not allow progress claims"
                )
            if rollup.get("production_claim_allowed") is not False:
                raise ValueError(
                    "literal product/split scoreboard must not allow production claims"
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


def mutate_target_state_to_active(tranche: dict[str, Any], state: str) -> dict[str, Any]:
    mutated = copy.deepcopy(tranche)
    for row in mutated["rows"]:
        if row.get("coordinate_state") == state:
            row["coordinate_state"] = "active_gamma"
            row["ligand_code_from_structure"] = "ATP"
            row["terminal_gamma_equivalent_geometry"] = True
            row["terminal_gamma_atom_name"] = "PG"
            row["product_state_context"] = False
            row["split_state_context"] = False
            row["expected_claim_status"] = "review_only_abstain_missing_role_policy"
            break
    refresh_literal_metadata(mutated)
    return mutated


def mutate_target_expected_to_nonabstaining(tranche: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(tranche)
    for row in mutated["rows"]:
        if row.get("coordinate_state") in TARGET_COORDINATE_STATES:
            row["expected_claim_status"] = "review_only_nonabstaining_candidate"
            row["expected_frozen_policy_decision"] = "nonabstaining_candidate"
            break
    refresh_literal_metadata(mutated)
    return mutated


def build_outputs(
    root: Path,
    output_dir: Path,
    run_stamp: str,
    policy_path: Path,
    *,
    max_entries: int,
) -> dict[str, Path]:
    payloads = [
        (dict(spec), load_git_json(str(spec["ref"]), str(spec["path"])))
        for spec in REAL_OVERLAP_INPUT_SPECS_V5
    ]
    policy = load_json(policy_path)
    tranche = build_tranche_from_payloads(payloads, max_entries=max_entries)
    validate_literal_product_split_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError(
            "literal product/split gate produced claim-status mismatches"
        )

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    report_path = output_dir / f"{stem}.json"
    negative_single_lane_path = output_dir / f"{stem}_negative_single_lane_entry_result.json"
    negative_missing_state_path = (
        output_dir / f"{stem}_negative_missing_literal_state_result.json"
    )
    negative_nonabstention_path = (
        output_dir / f"{stem}_negative_literal_state_nonabstention_result.json"
    )
    negative_source_copy_path = (
        output_dir / f"{stem}_negative_source_context_copy_result.json"
    )

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)
    gate = build_artifact(root, [result_path])
    validate_literal_product_split_scoreboard(gate)
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
    refresh_literal_metadata(single_lane_fault)
    single_lane_rejection = write_rejection(
        root,
        negative_single_lane_path,
        expected_failure="single_lane_entry",
        expected_error_fragment="at least two source lanes",
        action=lambda: validate_literal_product_split_tranche(single_lane_fault),
    )

    missing_state_fault = mutate_target_state_to_active(tranche, "split_state")
    missing_state_rejection = write_rejection(
        root,
        negative_missing_state_path,
        expected_failure="missing_literal_state",
        expected_error_fragment="literal coordinate-state coverage",
        action=lambda: validate_literal_product_split_tranche(missing_state_fault),
    )

    nonabstention_fault = mutate_target_expected_to_nonabstaining(tranche)
    nonabstention_rejection = write_rejection(
        root,
        negative_nonabstention_path,
        expected_failure="literal_state_nonabstention",
        expected_error_fragment="must expect review-only state abstention",
        action=lambda: validate_literal_product_split_tranche(nonabstention_fault),
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
            "Literal product_state and split_state coordinate rows from an "
            "independent source-free lane can be admitted only as review-only "
            "candidate evidence when the selected entries also have independent "
            "cross-lane support."
        ),
        "literal_product_split_summary": {
            "available_overlap_entry_count": tranche["metadata"][
                "available_overlap_entry_count"
            ],
            "available_literal_overlap_row_count": tranche["metadata"][
                "available_literal_overlap_row_count"
            ],
            "available_literal_overlap_coordinate_state_counts": tranche[
                "metadata"
            ]["available_literal_overlap_coordinate_state_counts"],
            "selected_overlap_entry_ids": tranche["metadata"][
                "selected_overlap_entry_ids"
            ],
            "selected_entry_source_lanes": tranche["metadata"][
                "selected_entry_source_lanes"
            ],
            "selected_coordinate_state_counts": tranche["metadata"][
                "selected_coordinate_state_counts"
            ],
            "literal_target_coordinate_state_counts": tranche["metadata"][
                "literal_target_coordinate_state_counts"
            ],
            "covered_literal_target_coordinate_state_values": tranche["metadata"][
                "covered_literal_target_coordinate_state_values"
            ],
            "uncovered_literal_target_coordinate_state_values": tranche["metadata"][
                "uncovered_literal_target_coordinate_state_values"
            ],
            "literal_product_or_split_rows_nonabstaining": False,
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
            nonabstention_rejection,
            source_copy_rejection,
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
            "negative_missing_literal_state": rel(negative_missing_state_path, root),
            "negative_missing_literal_state_sha256": sha256_file(
                negative_missing_state_path
            ),
            "negative_literal_state_nonabstention": rel(
                negative_nonabstention_path, root
            ),
            "negative_literal_state_nonabstention_sha256": sha256_file(
                negative_nonabstention_path
            ),
            "negative_source_context_copy": rel(negative_source_copy_path, root),
            "negative_source_context_copy_sha256": sha256_file(negative_source_copy_path),
        },
        "gate": {
            "gate_pass": gate["gate"]["gate_pass"],
            "literal_product_split_gate_pass": True,
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
        "negative_missing_literal_state": negative_missing_state_path,
        "negative_literal_state_nonabstention": negative_nonabstention_path,
        "negative_source_context_copy": negative_source_copy_path,
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
                        "candidate_id": "1AAA:active",
                        "pdb_id": "1AAA",
                        "coordinate_state": "active_gamma",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ANP",
                            "terminal_atom_name": "PG",
                            "nearest_terminal_distance_angstrom": 4.0,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "SER",
                        },
                    },
                    {
                        "candidate_id": "2BBB:active",
                        "pdb_id": "2BBB",
                        "coordinate_state": "active_gamma",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ANP",
                            "terminal_atom_name": "PG",
                            "nearest_terminal_distance_angstrom": 4.2,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "SER",
                        },
                    },
                ]
            },
        ),
        (
            {
                "lane_id": "epk_substrate_role_identity",
                "path": "phosphoproduct_fixture.json",
                "row_keys": ("phosphoproduct_materialization_rows",),
            },
            {
                "phosphoproduct_materialization_rows": [
                    {
                        "candidate_id": "1AAA|gamma=none|acceptor=A:TPO1|nucleotide=A:ADP1",
                        "pdb_id": "1AAA",
                        "source_free_evidence": {
                            "coordinate_state": "product_state",
                            "blocker_class": "product_state_evidence",
                            "nucleotide_anchor_atom": {
                                "residue_code": "ADP",
                                "atom_name": "PB",
                            },
                            "acceptor_atom": {"residue_code": "TPO"},
                            "nearest_distance_angstrom": 12.5,
                        },
                    },
                    {
                        "candidate_id": "2BBB|gamma=none|acceptor=A:SEP2|nucleotide=A:ANP2",
                        "pdb_id": "2BBB",
                        "source_free_evidence": {
                            "coordinate_state": "split_state",
                            "blocker_class": "split_state_evidence",
                            "nucleotide_anchor_atom": {
                                "residue_code": "ANP",
                                "atom_name": "PB",
                            },
                            "acceptor_atom": {"residue_code": "SEP"},
                            "nearest_distance_angstrom": 3.5,
                        },
                    },
                ]
            },
        ),
    ]
    tranche = build_tranche_from_payloads(payloads, max_entries=3)
    validate_literal_product_split_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    assert result["metadata"]["expected_claim_status_mismatch_count"] == 0
    result_path = Path("/private/tmp/epk_literal_product_split_gate_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(Path.cwd(), [result_path])
    validate_literal_product_split_scoreboard(gate)
    assert set(TARGET_COORDINATE_STATES).issubset(
        set(gate["scoreboard_summary"]["covered_coordinate_state_values"])
    )
    bad = mutate_target_state_to_active(tranche, "split_state")
    try:
        validate_literal_product_split_tranche(bad)
    except ValueError as error:
        assert "literal coordinate-state coverage" in str(error)
    else:
        raise AssertionError("missing literal split-state fixture must fail")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a compact review-only real-overlap gate for literal "
            "product_state and split_state candidate rows."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_policy_harness"),
    )
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-entries", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0
    if args.max_entries <= 0:
        parser.error("--max-entries must be positive")

    run_stamp = args.timestamp or timestamp()
    outputs = build_outputs(
        Path.cwd(),
        args.output_dir,
        run_stamp,
        args.policy,
        max_entries=args.max_entries,
    )
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
