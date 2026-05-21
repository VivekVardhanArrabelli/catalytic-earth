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
    write_json,
)
from epk_federated_candidate_adapter_smoke import (
    ADAPTERS,
    load_git_json,
    rows_for_keys,
)
from epk_policy_harness import (
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    evaluate_tranche,
    load_json,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_candidate_entry_rollup_real_entry_overlap_v3"
DEFAULT_POLICY = Path("artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json")
REAL_OVERLAP_INPUT_SPECS = (
    {
        "lane_id": "epk_positive_evidence",
        "ref": "origin/research/epk-positive-evidence",
        "path": "artifacts/research_lanes/epk_positive_evidence/candidate_source_adjudication_all_20260521.json",
        "row_keys": ("adjudicated_candidate_rows",),
    },
    {
        "lane_id": "epk_substrate_role_identity",
        "ref": "origin/research/epk-substrate-role-identity",
        "path": "artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json",
        "row_keys": ("candidate_evidence_rows", "state_only_rows"),
    },
    {
        "lane_id": "epk_false_positive_hunter",
        "ref": "origin/research/epk-false-positive-hunter",
        "path": "artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json",
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
ENTRY_PRIORITY = (
    "6U1D",
    "6U1E",
    "9NBW",
    "4EKK",
    "7ZDU",
    "9UUR",
    "9UUX",
    "9UW4",
    "2JJ2",
    "5C1O",
    "8W2J",
    "1QHA",
)


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def entry_id_for_raw_row(row: dict[str, Any]) -> str | None:
    value = row.get("entry_id") or row.get("pdb_id") or row.get("pdb")
    if not value and isinstance(row.get("candidate"), dict):
        value = row["candidate"].get("entry_id") or row["candidate"].get("pdb_id")
    entry_id = str(value or "").strip().upper()
    return entry_id or None


def source_false_fields() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_ROW_FLAGS}


def row_preference(lane_id: str, row_key: str, row: dict[str, Any], index: int) -> tuple[Any, ...]:
    if lane_id == "epk_positive_evidence":
        geometry = row.get("source_free_geometry") or {}
        coordinate_state = str(row.get("coordinate_state") or "")
        blockers = " ".join(str(value) for value in row.get("original_blockers") or [])
        return (
            coordinate_state != "active_gamma",
            not bool(geometry.get("has_local_mg_or_mn")),
            "no_local_metal" not in blockers,
            index,
        )
    if lane_id == "epk_substrate_role_identity":
        evidence = row.get("source_free_evidence") or {}
        blocker = str(evidence.get("blocker_class") or "")
        blocker_order = {
            "none": 0,
            "topology_ambiguity": 1,
            "product_state_evidence": 2,
            "substrate_role_identity": 3,
            "active_gamma_geometry": 4,
            "internal_fragment_mimicry": 5,
            "ligand_materialization": 6,
        }
        return (blocker_order.get(blocker, 20), row_key != "candidate_evidence_rows", index)
    if lane_id == "epk_false_positive_hunter":
        control_class = str(row.get("control_class") or "")
        guard_blocker = str(row.get("guard_blocker_class") or "")
        return (
            row.get("current_context_v4_only_unsafe_nonabstention") is not True,
            row.get("non_epk_control") is not True,
            "split" not in guard_blocker,
            not any(token in control_class for token in ("atpase", "orc", "mcm", "transporter")),
            index,
        )
    if lane_id == "epk_sibling_controls":
        expected = row.get("expected_review_only_result") or {}
        return (
            expected.get("should_block_weak_rule_hit") is not True
            and expected.get("should_block_weak_product_rule_hit") is not True,
            row_key != "gamma_proximity_counteraxis_cases",
            index,
        )
    return (index,)


def payload_rows_by_entry(
    spec: dict[str, Any], payload: dict[str, Any]
) -> dict[str, list[tuple[str, dict[str, Any], int]]]:
    rows_by_entry: dict[str, list[tuple[str, dict[str, Any], int]]] = {}
    for index, (row_key, row) in enumerate(rows_for_keys(payload, tuple(spec["row_keys"]))):
        entry_id = entry_id_for_raw_row(row)
        if not entry_id:
            continue
        rows_by_entry.setdefault(entry_id, []).append((row_key, row, index))
    return rows_by_entry


def selected_entries(
    entry_source_lanes: dict[str, set[str]], max_entries: int
) -> list[str]:
    overlapping = {
        entry_id: lanes
        for entry_id, lanes in entry_source_lanes.items()
        if len(lanes) >= 2
    }
    if not overlapping:
        raise ValueError("real-overlap gate found no entries shared by at least two lanes")
    chosen: list[str] = []
    for entry_id in ENTRY_PRIORITY:
        if entry_id in overlapping and entry_id not in chosen:
            chosen.append(entry_id)
    for entry_id in sorted(
        overlapping,
        key=lambda item: (-len(overlapping[item]), item),
    ):
        if entry_id not in chosen:
            chosen.append(entry_id)
    return chosen[:max_entries]


def choose_row(
    lane_id: str, rows: list[tuple[str, dict[str, Any], int]]
) -> tuple[str, dict[str, Any], int]:
    return sorted(
        rows,
        key=lambda item: row_preference(lane_id, item[0], item[1], item[2]),
    )[0]


def build_tranche_from_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    *,
    max_entries: int,
) -> dict[str, Any]:
    rows_by_lane: dict[str, dict[str, list[tuple[str, dict[str, Any], int]]]] = {}
    input_summaries: list[dict[str, Any]] = []
    for spec, payload in payloads:
        lane_id = spec["lane_id"]
        by_entry = payload_rows_by_entry(spec, payload)
        rows_by_lane[lane_id] = by_entry

    entry_source_lanes: dict[str, set[str]] = {}
    for lane_id, by_entry in rows_by_lane.items():
        for entry_id in by_entry:
            entry_source_lanes.setdefault(entry_id, set()).add(lane_id)
    overlap_entry_ids = selected_entries(entry_source_lanes, max_entries)
    selected_overlap_set = set(overlap_entry_ids)

    adapted_rows: list[dict[str, Any]] = []
    selected_counts_by_lane: Counter[str] = Counter()
    available_overlap_counts_by_lane: Counter[str] = Counter()
    for spec, _payload in payloads:
        lane_id = spec["lane_id"]
        by_entry = rows_by_lane[lane_id]
        available_overlap_counts_by_lane[lane_id] = sum(
            1 for entry_id in by_entry if len(entry_source_lanes.get(entry_id, set())) >= 2
        )
        for entry_id in overlap_entry_ids:
            if entry_id not in by_entry:
                continue
            row_key, raw_row, raw_index = choose_row(lane_id, by_entry[entry_id])
            adapted = ADAPTERS[lane_id](
                raw_row,
                source_artifact=spec["path"],
                source_row_key=row_key,
                index=raw_index,
            )
            adapted["entry_id"] = entry_id
            adapted["pdb_id"] = adapted.get("pdb_id") or entry_id
            adapted.update({key: adapted.get(key, value) for key, value in source_false_fields().items()})
            adapted_rows.append(adapted)
            selected_counts_by_lane[lane_id] += 1

    selected_source_lanes = sorted({row["source_lane_id"] for row in adapted_rows})
    selected_entry_source_lanes: dict[str, list[str]] = {}
    for entry_id in overlap_entry_ids:
        selected_entry_source_lanes[entry_id] = sorted(
            {
                row["source_lane_id"]
                for row in adapted_rows
                if row.get("entry_id") == entry_id
            }
        )
    for spec, payload in payloads:
        row_count = len(rows_for_keys(payload, tuple(spec["row_keys"])))
        lane_id = spec["lane_id"]
        input_summaries.append(
            {
                "lane_id": lane_id,
                "ref": spec.get("ref"),
                "artifact": spec["path"],
                "row_keys": list(spec["row_keys"]),
                "available_row_count": row_count,
                "available_entry_count": len(rows_by_lane[lane_id]),
                "available_overlap_entry_count": available_overlap_counts_by_lane[lane_id],
                "selected_entry_count": sum(
                    1 for entry_id in selected_overlap_set if entry_id in rows_by_lane[lane_id]
                ),
                "selected_row_count": selected_counts_by_lane[lane_id],
                "review_only_input": True,
            }
        )

    return {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": len(adapted_rows),
            "source_lane_count": len(selected_source_lanes),
            "source_lanes": selected_source_lanes,
            "input_summaries": input_summaries,
            "available_overlap_entry_count": sum(
                1 for lanes in entry_source_lanes.values() if len(lanes) >= 2
            ),
            "selected_overlap_entry_count": len(overlap_entry_ids),
            "selected_overlap_entry_ids": overlap_entry_ids,
            "selected_entry_source_lanes": selected_entry_source_lanes,
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
            "real_overlap_gate_contract": {
                "entry_ids_from_real_cross_lane_artifact_intersections": True,
                "every_selected_entry_has_at_least_two_source_lanes": True,
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
        "rows": adapted_rows,
    }


def validate_real_overlap_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("real-overlap gate requires review_only=true")
    contract = metadata.get("real_overlap_gate_contract")
    if not isinstance(contract, dict):
        raise ValueError("real-overlap gate requires metadata.real_overlap_gate_contract")
    for flag in (
        "entry_ids_from_real_cross_lane_artifact_intersections",
        "every_selected_entry_has_at_least_two_source_lanes",
        "entry_status_derived_from_candidate_decisions",
        "source_text_and_protein_names_not_copied",
    ):
        if contract.get(flag) is not True:
            raise ValueError(f"real-overlap gate requires {flag}=true")
    for flag in (
        "progress_claim_allowed",
        "production_claim_allowed",
        "labels_or_fingerprints_changed",
    ):
        if contract.get(flag) is not False:
            raise ValueError(f"real-overlap gate requires {flag}=false")
    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("real-overlap gate requires non-empty rows")
    entry_lanes: dict[str, set[str]] = {}
    for row in rows:
        row_id = str(row.get("row_id") or row.get("pdb_id") or "unknown_row")
        entry_id = str(row.get("entry_id") or "").strip()
        if not entry_id:
            raise ValueError(f"real-overlap gate requires entry_id on every row: {row_id}")
        source_lane_id = str(row.get("source_lane_id") or "").strip()
        if not source_lane_id:
            raise ValueError(
                f"real-overlap gate requires source_lane_id on every row: {row_id}"
            )
        entry_lanes.setdefault(entry_id, set()).add(source_lane_id)
    single_lane_entries = {
        entry_id: sorted(lanes)
        for entry_id, lanes in entry_lanes.items()
        if len(lanes) < 2
    }
    if single_lane_entries:
        raise ValueError(
            "real-overlap gate requires every selected entry to contain candidate "
            f"rows from at least two source lanes: {single_lane_entries}"
        )
    declared_entries = [str(entry) for entry in metadata.get("selected_overlap_entry_ids", [])]
    if sorted(declared_entries) != sorted(entry_lanes):
        raise ValueError("real-overlap gate selected_overlap_entry_ids drifted from rows")
    if int(metadata.get("selected_overlap_entry_count") or -1) != len(entry_lanes):
        raise ValueError("real-overlap gate selected_overlap_entry_count drifted from rows")


def validate_real_overlap_scoreboard(gate: dict[str, Any]) -> None:
    if gate.get("gate", {}).get("gate_pass") is not True:
        raise ValueError("real-overlap scoreboard gate must pass")
    for scoreboard_row in gate.get("scoreboard_rows", []):
        for rollup in scoreboard_row.get("entry_rollups", []):
            if len(rollup.get("source_lane_ids") or []) < 2:
                raise ValueError(
                    "real-overlap scoreboard contains single-lane entry rollup: "
                    f"{rollup.get('entry_id')}"
                )
            if rollup.get("progress_claim_allowed") is not False:
                raise ValueError("real-overlap scoreboard must not allow progress claims")
            if rollup.get("production_claim_allowed") is not False:
                raise ValueError("real-overlap scoreboard must not allow production claims")


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


def refresh_tranche_metadata(tranche: dict[str, Any]) -> None:
    rows = tranche["rows"]
    source_lanes = sorted({row["source_lane_id"] for row in rows})
    entry_ids = []
    for row in rows:
        entry_id = row.get("entry_id")
        if entry_id and entry_id not in entry_ids:
            entry_ids.append(entry_id)
    tranche["metadata"]["row_count"] = len(rows)
    tranche["metadata"]["source_lanes"] = source_lanes
    tranche["metadata"]["source_lane_count"] = len(source_lanes)
    tranche["metadata"]["selected_overlap_entry_ids"] = entry_ids
    tranche["metadata"]["selected_overlap_entry_count"] = len(entry_ids)
    tranche["metadata"]["selected_entry_source_lanes"] = {
        entry_id: sorted(
            {
                row["source_lane_id"]
                for row in rows
                if row.get("entry_id") == entry_id
            }
        )
        for entry_id in entry_ids
    }


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
        for spec in REAL_OVERLAP_INPUT_SPECS
    ]
    policy = load_json(policy_path)
    tranche = build_tranche_from_payloads(payloads, max_entries=max_entries)
    validate_real_overlap_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("real-overlap gate produced unexpected claim-status mismatch")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    report_path = output_dir / f"{stem}.json"
    negative_single_lane_path = (
        output_dir / f"{stem}_negative_single_lane_entry_result.json"
    )
    negative_missing_entry_path = (
        output_dir / f"{stem}_negative_missing_entry_id_result.json"
    )
    negative_source_copy_path = (
        output_dir / f"{stem}_negative_source_context_copy_result.json"
    )

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)
    gate = build_artifact(root, [result_path])
    validate_real_overlap_scoreboard(gate)
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
    refresh_tranche_metadata(single_lane_fault)
    single_lane_rejection = write_rejection(
        root,
        negative_single_lane_path,
        expected_failure="single_lane_entry",
        expected_error_fragment="at least two source lanes",
        action=lambda: validate_real_overlap_tranche(single_lane_fault),
    )

    missing_entry_fault = copy.deepcopy(tranche)
    missing_entry_fault["rows"][0].pop("entry_id", None)
    refresh_tranche_metadata(missing_entry_fault)
    missing_entry_rejection = write_rejection(
        root,
        negative_missing_entry_path,
        expected_failure="missing_entry_id",
        expected_error_fragment="entry_id on every row",
        action=lambda: validate_real_overlap_tranche(missing_entry_fault),
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

    source_lane_counts = Counter(row["source_lane_id"] for row in tranche["rows"])
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
            "Real entries emitted by at least two independent ePK lanes can be "
            "rolled up only when candidate-level decisions remain visible and "
            "each selected entry keeps multi-lane support."
        ),
        "real_overlap_summary": {
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
            "source_lane_counts": dict(sorted(source_lane_counts.items())),
            "all_selected_entries_have_multi_lane_support": True,
            "source_text_and_protein_names_copied": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "federated_inputs": tranche["metadata"]["input_summaries"],
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
            missing_entry_rejection,
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
            "negative_missing_entry_id": rel(negative_missing_entry_path, root),
            "negative_missing_entry_id_sha256": sha256_file(negative_missing_entry_path),
            "negative_source_context_copy": rel(negative_source_copy_path, root),
            "negative_source_context_copy_sha256": sha256_file(negative_source_copy_path),
        },
        "gate": {
            "gate_pass": gate["gate"]["gate_pass"],
            "real_overlap_gate_pass": True,
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
        "negative_missing_entry_id": negative_missing_entry_path,
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
                        "candidate_id": "1AAA:positive",
                        "pdb_id": "1AAA",
                        "coordinate_state": "active_gamma",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ATP",
                            "terminal_atom_name": "PG",
                            "nearest_terminal_distance_angstrom": 3.2,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "SER",
                        },
                    },
                ],
            },
        ),
        (
            {
                "lane_id": "epk_sibling_controls",
                "path": "sibling_fixture.json",
                "row_keys": ("gamma_proximity_counteraxis_cases",),
            },
            {
                "gamma_proximity_counteraxis_cases": [
                    {
                        "case_id": "1AAA:sibling",
                        "pdb_id": "1AAA",
                        "input_features": {
                            "gamma_capable_nucleotide_codes": ["ANP"],
                            "nearest_gamma_to_protein_hydroxyl_distance_angstrom": 4.1,
                            "metal_ligand_codes": ["MG"],
                        },
                        "expected_review_only_result": {
                            "should_block_weak_rule_hit": True,
                        },
                    },
                ],
            },
        ),
    ]
    tranche = build_tranche_from_payloads(payloads, max_entries=1)
    validate_real_overlap_tranche(tranche)
    result = evaluate_tranche(policy, tranche)
    result_path = Path("/private/tmp/epk_real_overlap_gate_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(Path.cwd(), [result_path])
    validate_real_overlap_scoreboard(gate)
    assert result["metadata"]["claim_status_counts"] == {
        "review_only_abstain_missing_role_policy": 1,
        "review_only_abstain_sibling_control": 1,
    }
    bad = copy.deepcopy(tranche)
    bad["rows"] = [bad["rows"][0]]
    refresh_tranche_metadata(bad)
    try:
        validate_real_overlap_tranche(bad)
    except ValueError as error:
        assert "at least two source lanes" in str(error)
    else:
        raise AssertionError("single-lane overlap fixture must fail")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a compact review-only gate from real entries shared by "
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
    parser.add_argument("--max-entries", type=int, default=12)
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
