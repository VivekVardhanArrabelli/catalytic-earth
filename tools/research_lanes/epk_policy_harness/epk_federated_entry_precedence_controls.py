#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epk_candidate_policy_bridge_scoreboard_gate import (
    ENTRY_CLAIM_STATUS_PRECEDENCE,
    build_artifact,
    is_control_like,
    rel,
    write_json,
)
from epk_federated_candidate_adapter_smoke import (
    ADAPTERS,
    load_git_json,
    rows_for_keys,
    select_rows,
)
from epk_federated_literal_product_split_overlap_gate import (
    REAL_OVERLAP_INPUT_SPECS_V5,
    build_tranche_from_payloads as build_literal_tranche_from_payloads,
    count_values,
    source_false_fields,
    validate_literal_product_split_tranche,
)
from epk_federated_real_overlap_gate import DEFAULT_POLICY, entry_id_for_raw_row
from epk_policy_harness import (
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    SOURCE_LEAKAGE_ROW_FLAGS,
    evaluate_tranche,
    load_json,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_literal_product_split_entry_precedence_controls_v6"

CONTACT_INTERFACE_SPEC_V6 = {
    "lane_id": "epk_substrate_role_identity",
    "ref": "origin/research/epk-substrate-role-identity",
    "path": (
        "artifacts/research_lanes/epk_substrate_role_identity/"
        "epk_active_site_contact_interface_audit_v1_20260521.json"
    ),
    "row_keys": ("active_site_contact_interface_rows",),
}
FALSE_POSITIVE_CONTROLS_SPEC_V6 = {
    "lane_id": "epk_false_positive_hunter",
    "ref": "origin/research/epk-false-positive-hunter",
    "path": (
        "artifacts/research_lanes/epk_false_positive_hunter/"
        "epk_candidate_evidence_v1_regression_gate_20260521_172900Z.json"
    ),
    "row_keys": ("rows",),
}
SIBLING_CONTROLS_SPEC_V6 = {
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
}
SUPPLEMENTAL_SPECS_V6 = (
    CONTACT_INTERFACE_SPEC_V6,
    SIBLING_CONTROLS_SPEC_V6,
    FALSE_POSITIVE_CONTROLS_SPEC_V6,
)
TOPOLOGY_COORDINATE_STATES = {
    "ambiguous_coordinate_state",
    "unavailable_coordinate_state",
    "ligand_absent",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def raw_row_count(payload: dict[str, Any], row_keys: tuple[str, ...]) -> int:
    total = 0
    for row_key in row_keys:
        rows = payload.get(row_key, [])
        if isinstance(rows, list):
            total += sum(1 for row in rows if isinstance(row, dict))
    return total


def entry_source_lanes(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    lanes_by_entry: dict[str, set[str]] = {}
    for row in rows:
        entry_id = str(row.get("entry_id") or row.get("pdb_id") or "unknown_entry")
        source_lane_id = str(row.get("source_lane_id") or "").strip()
        if source_lane_id:
            lanes_by_entry.setdefault(entry_id, set()).add(source_lane_id)
    return {entry: sorted(lanes) for entry, lanes in sorted(lanes_by_entry.items())}


def add_source_false_defaults(row: dict[str, Any]) -> dict[str, Any]:
    for key, value in source_false_fields().items():
        row.setdefault(key, value)
    return row


def is_topology_contact_row(raw_row: dict[str, Any]) -> bool:
    evidence = raw_row.get("source_free_evidence") or {}
    state = str(evidence.get("coordinate_state") or "")
    blocker = str(evidence.get("blocker_class") or "")
    return state in TOPOLOGY_COORDINATE_STATES or blocker == "topology_ambiguity"


def adapt_contact_topology_rows(
    spec: dict[str, Any],
    payload: dict[str, Any],
    selected_entry_ids: list[str],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_entries: set[str] = set()
    selected_entry_set = set(selected_entry_ids)
    for index, (row_key, raw_row) in enumerate(rows_for_keys(payload, tuple(spec["row_keys"]))):
        entry_id = entry_id_for_raw_row(raw_row)
        if entry_id not in selected_entry_set or entry_id in seen_entries:
            continue
        if not is_topology_contact_row(raw_row):
            continue
        adapted = ADAPTERS[str(spec["lane_id"])](
            raw_row,
            source_artifact=str(spec["path"]),
            source_row_key=row_key,
            index=index,
        )
        adapted["entry_id"] = entry_id
        adapted["pdb_id"] = adapted.get("pdb_id") or entry_id
        adapted.setdefault(
            "topology_ambiguity_status",
            "v6_entry_precedence_topology_review_only",
        )
        adapted["expected_claim_status"] = "review_only_abstain_topology_ambiguity"
        adapted["expected_frozen_policy_decision"] = (
            "review_only_abstain_topology_ambiguity"
        )
        add_source_false_defaults(adapted)
        selected.append(adapted)
        seen_entries.add(entry_id)
    return selected


def adapt_selected_control_rows(
    spec: dict[str, Any], payload: dict[str, Any]
) -> list[dict[str, Any]]:
    lane_id = str(spec["lane_id"])
    selected_rows = select_rows(lane_id, rows_for_keys(payload, tuple(spec["row_keys"])))
    adapted_rows: list[dict[str, Any]] = []
    for index, (row_key, raw_row) in enumerate(selected_rows):
        adapted = ADAPTERS[lane_id](
            raw_row,
            source_artifact=str(spec["path"]),
            source_row_key=row_key,
            index=index,
        )
        entry_id = entry_id_for_raw_row(raw_row) or str(adapted.get("pdb_id") or "")
        if entry_id:
            adapted["entry_id"] = entry_id
            adapted["pdb_id"] = adapted.get("pdb_id") or entry_id
        add_source_false_defaults(adapted)
        adapted_rows.append(adapted)
    return adapted_rows


def refresh_precedence_metadata(
    tranche: dict[str, Any],
    *,
    input_summaries: list[dict[str, Any]],
    literal_selected_entries: list[str],
) -> None:
    rows = tranche["rows"]
    source_lanes = sorted({str(row["source_lane_id"]) for row in rows})
    entry_ids = []
    for row in rows:
        entry_id = str(row.get("entry_id") or row.get("pdb_id") or "")
        if entry_id and entry_id not in entry_ids:
            entry_ids.append(entry_id)
    product_analog_entries = [
        entry_id
        for entry_id in entry_ids
        if {
            str(row.get("coordinate_state") or "")
            for row in rows
            if str(row.get("entry_id") or row.get("pdb_id") or "") == entry_id
        }
        >= {"product_state", "substrate_acceptor_analog_state"}
    ]
    split_topology_entries = [
        entry_id
        for entry_id in entry_ids
        if any(
            row.get("coordinate_state") == "split_state"
            for row in rows
            if str(row.get("entry_id") or row.get("pdb_id") or "") == entry_id
        )
        and any(
            row.get("expected_claim_status")
            == "review_only_abstain_topology_ambiguity"
            for row in rows
            if str(row.get("entry_id") or row.get("pdb_id") or "") == entry_id
        )
    ]
    sibling_control_entries = [
        entry_id
        for entry_id in entry_ids
        if any(
            row.get("sibling_counterfamily_context") is True
            for row in rows
            if str(row.get("entry_id") or row.get("pdb_id") or "") == entry_id
        )
    ]
    metadata = tranche["metadata"]
    metadata.update(
        {
            "row_count": len(rows),
            "source_lanes": source_lanes,
            "source_lane_count": len(source_lanes),
            "input_summaries": input_summaries,
            "selected_literal_overlap_entry_ids": literal_selected_entries,
            "selected_entry_ids": entry_ids,
            "selected_entry_source_lanes": entry_source_lanes(rows),
            "coordinate_state_counts": count_values(rows, "coordinate_state"),
            "expected_claim_status_counts": count_values(
                rows, "expected_claim_status"
            ),
            "product_analog_precedence_entries": product_analog_entries,
            "split_topology_precedence_entries": split_topology_entries,
            "sibling_control_precedence_entries": sibling_control_entries,
            "entry_claim_status_precedence": list(ENTRY_CLAIM_STATUS_PRECEDENCE),
            "requested_coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        }
    )


def supplemental_input_summary(
    spec: dict[str, Any], payload: dict[str, Any], selected_count: int
) -> dict[str, Any]:
    return {
        "lane_id": spec["lane_id"],
        "ref": spec.get("ref"),
        "artifact": spec["path"],
        "row_keys": list(spec["row_keys"]),
        "available_row_count": raw_row_count(payload, tuple(spec["row_keys"])),
        "selected_row_count": selected_count,
        "review_only_input": True,
    }


def build_precedence_tranche_from_payloads(
    literal_payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    *,
    contact_payload: dict[str, Any],
    sibling_payload: dict[str, Any],
    false_positive_payload: dict[str, Any],
    max_entries: int,
) -> dict[str, Any]:
    literal_tranche = build_literal_tranche_from_payloads(
        literal_payloads,
        max_entries=max_entries,
    )
    validate_literal_product_split_tranche(literal_tranche)
    rows = copy.deepcopy(literal_tranche["rows"])
    literal_selected_entries = [
        str(entry)
        for entry in literal_tranche["metadata"]["selected_overlap_entry_ids"]
    ]

    contact_rows = adapt_contact_topology_rows(
        CONTACT_INTERFACE_SPEC_V6,
        contact_payload,
        literal_selected_entries,
    )
    sibling_rows = adapt_selected_control_rows(SIBLING_CONTROLS_SPEC_V6, sibling_payload)
    false_positive_rows = adapt_selected_control_rows(
        FALSE_POSITIVE_CONTROLS_SPEC_V6,
        false_positive_payload,
    )
    rows.extend(contact_rows)
    rows.extend(sibling_rows)
    rows.extend(false_positive_rows)

    input_summaries = list(literal_tranche["metadata"].get("input_summaries", []))
    input_summaries.extend(
        [
            supplemental_input_summary(
                CONTACT_INTERFACE_SPEC_V6,
                contact_payload,
                len(contact_rows),
            ),
            supplemental_input_summary(
                SIBLING_CONTROLS_SPEC_V6,
                sibling_payload,
                len(sibling_rows),
            ),
            supplemental_input_summary(
                FALSE_POSITIVE_CONTROLS_SPEC_V6,
                false_positive_payload,
                len(false_positive_rows),
            ),
        ]
    )

    tranche = {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
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
            "entry_precedence_controls_contract": {
                "candidate_rows_are_source_of_truth": True,
                "entry_status_derived_from_candidate_decisions": True,
                "literal_product_split_rows_remain_visible": True,
                "product_rows_do_not_override_analog_state": True,
                "split_rows_do_not_override_topology_ambiguity": True,
                "sibling_controls_do_not_nonabstain": True,
                "forbidden_source_leakage_is_expected_gate_failure": True,
                "unsafe_control_nonabstention_is_expected_gate_failure": True,
                "progress_claim_allowed": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            },
        },
        "rows": rows,
    }
    refresh_precedence_metadata(
        tranche,
        input_summaries=input_summaries,
        literal_selected_entries=literal_selected_entries,
    )
    validate_precedence_tranche(tranche)
    return tranche


def validate_precedence_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("entry precedence controls require review_only=true")
    contract = metadata.get("entry_precedence_controls_contract")
    if not isinstance(contract, dict):
        raise ValueError(
            "entry precedence controls require metadata.entry_precedence_controls_contract"
        )
    for flag in (
        "candidate_rows_are_source_of_truth",
        "entry_status_derived_from_candidate_decisions",
        "literal_product_split_rows_remain_visible",
        "product_rows_do_not_override_analog_state",
        "split_rows_do_not_override_topology_ambiguity",
        "sibling_controls_do_not_nonabstain",
        "forbidden_source_leakage_is_expected_gate_failure",
        "unsafe_control_nonabstention_is_expected_gate_failure",
    ):
        if contract.get(flag) is not True:
            raise ValueError(f"entry precedence controls require {flag}=true")
    for flag in (
        "progress_claim_allowed",
        "production_claim_allowed",
        "labels_or_fingerprints_changed",
    ):
        if contract.get(flag) is not False:
            raise ValueError(f"entry precedence controls require {flag}=false")

    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("entry precedence controls require non-empty rows")
    if not metadata.get("product_analog_precedence_entries"):
        raise ValueError(
            "entry precedence controls require product/analog mixed entries"
        )
    if not metadata.get("split_topology_precedence_entries"):
        raise ValueError(
            "entry precedence controls require split/topology mixed entries"
        )
    if not metadata.get("sibling_control_precedence_entries"):
        raise ValueError("entry precedence controls require sibling control entries")
    for row in rows:
        row_id = str(row.get("row_id") or row.get("candidate_id") or "unknown_row")
        leakage_flags = [
            flag for flag in SOURCE_LEAKAGE_ROW_FLAGS if row.get(flag) is True
        ]
        if leakage_flags:
            raise ValueError(
                f"positive entry precedence tranche has forbidden leakage flags: "
                f"{row_id} {leakage_flags}"
            )
        if row.get("sibling_counterfamily_context") is True and row.get(
            "expected_claim_status"
        ) == "review_only_nonabstaining_candidate":
            raise ValueError(
                "positive entry precedence sibling controls must not expect "
                f"nonabstention: {row_id}"
            )
    if metadata.get("coordinate_state_counts") != count_values(rows, "coordinate_state"):
        raise ValueError("entry precedence coordinate-state counts drifted from rows")
    if metadata.get("expected_claim_status_counts") != count_values(
        rows, "expected_claim_status"
    ):
        raise ValueError("entry precedence expected-status counts drifted from rows")


def rollups_by_entry(gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rollups: dict[str, dict[str, Any]] = {}
    for scoreboard_row in gate.get("scoreboard_rows", []):
        for rollup in scoreboard_row.get("entry_rollups", []):
            rollups[str(rollup.get("entry_id"))] = rollup
    return rollups


def validate_precedence_scoreboard(gate: dict[str, Any]) -> dict[str, Any]:
    if gate.get("gate", {}).get("gate_pass") is not True:
        raise ValueError("entry precedence positive scoreboard gate must pass")
    rollups = rollups_by_entry(gate)
    product_analog_entries: list[str] = []
    split_topology_entries: list[str] = []
    sibling_entries: list[str] = []
    for entry_id, rollup in sorted(rollups.items()):
        claim_counts = rollup.get("claim_status_counts") or {}
        state_counts = rollup.get("coordinate_state_counts") or {}
        if state_counts.get("product_state") and state_counts.get(
            "substrate_acceptor_analog_state"
        ):
            if rollup.get("entry_claim_status") != "review_only_abstain_analog_state":
                raise ValueError(
                    "product/analog mixed entry did not roll up to analog abstention: "
                    f"{entry_id}"
                )
            product_analog_entries.append(entry_id)
        if state_counts.get("split_state") and claim_counts.get(
            "review_only_abstain_topology_ambiguity"
        ):
            if rollup.get("entry_claim_status") != (
                "review_only_abstain_topology_ambiguity"
            ):
                raise ValueError(
                    "split/topology mixed entry did not roll up to topology "
                    f"abstention: {entry_id}"
                )
            split_topology_entries.append(entry_id)
        if claim_counts.get("review_only_abstain_sibling_control"):
            if rollup.get("entry_claim_status") != "review_only_abstain_sibling_control":
                raise ValueError(
                    "sibling control entry did not roll up to sibling abstention: "
                    f"{entry_id}"
                )
            sibling_entries.append(entry_id)
        if rollup.get("progress_claim_allowed") is not False:
            raise ValueError("entry precedence rollups must not allow progress claims")
        if rollup.get("production_claim_allowed") is not False:
            raise ValueError("entry precedence rollups must not allow production claims")
    if not product_analog_entries:
        raise ValueError("scoreboard missed product/analog precedence entries")
    if not split_topology_entries:
        raise ValueError("scoreboard missed split/topology precedence entries")
    if not sibling_entries:
        raise ValueError("scoreboard missed sibling-control precedence entries")
    return {
        "product_analog_entries": product_analog_entries,
        "split_topology_entries": split_topology_entries,
        "sibling_control_entries": sibling_entries,
    }


def source_leakage_negative_tranche(tranche: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(tranche)
    metadata = mutated["metadata"]
    metadata.pop("federated_adapter_smoke_contract", None)
    metadata["federated_adapter_contract_removed_for_expected_source_leakage"] = True
    metadata["fault_injection_expected_failure"] = "forbidden_source_leakage"
    for row in mutated["rows"]:
        if row.get("coordinate_state") in {"product_state", "split_state"}:
            for flag in SOURCE_LEAKAGE_ROW_FLAGS:
                row[flag] = False
            row["source_text_used_for_predictive_feature"] = True
            row["expected_claim_status"] = "forbidden_source_leakage"
            row["expected_frozen_policy_decision"] = (
                "review_only_abstain_forbidden_source_leakage"
            )
            return mutated
    raise ValueError("source leakage fault requires a product or split row")


def recompute_result_metadata(result: dict[str, Any]) -> None:
    rows = result.get("rows", [])
    decision_counts: Counter[str] = Counter()
    claim_status_counts: Counter[str] = Counter()
    coordinate_state_counts: Counter[str] = Counter()
    abstention_reason_counts: Counter[str] = Counter()
    expected_decision_mismatches: list[str] = []
    expected_claim_status_mismatches: list[str] = []
    for row in rows:
        decision_counts[str(row.get("decision") or "")] += 1
        claim_status_counts[str(row.get("claim_status") or "")] += 1
        coordinate_state_counts[str(row.get("coordinate_state") or "")] += 1
        for reason in row.get("abstention_reasons") or []:
            abstention_reason_counts[str(reason)] += 1
        if row.get("expected_frozen_policy_match") is False:
            expected_decision_mismatches.append(str(row.get("row_id")))
        if row.get("expected_claim_status_match") is False:
            expected_claim_status_mismatches.append(str(row.get("row_id")))
    result["metadata"].update(
        {
            "row_count": len(rows),
            "decision_counts": dict(sorted(decision_counts.items())),
            "claim_status_counts": dict(sorted(claim_status_counts.items())),
            "coordinate_state_counts": dict(sorted(coordinate_state_counts.items())),
            "abstention_reason_counts": dict(sorted(abstention_reason_counts.items())),
            "expected_decision_mismatch_count": len(expected_decision_mismatches),
            "expected_decision_mismatches": expected_decision_mismatches,
            "expected_claim_status_mismatch_count": len(
                expected_claim_status_mismatches
            ),
            "expected_claim_status_mismatches": expected_claim_status_mismatches,
        }
    )


def unsafe_control_nonabstention_negative_result(
    result: dict[str, Any]
) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    mutated["metadata"]["fault_injection_expected_failure"] = (
        "unsafe_control_nonabstention"
    )
    mutated_count = 0
    for row in mutated["rows"]:
        if not is_control_like(row):
            continue
        row["decision"] = "review_only_nonabstaining_candidate"
        row["claim_status"] = "review_only_nonabstaining_candidate"
        row["claim_admissibility"] = "review_only"
        row["abstention_reasons"] = []
        row["expected_frozen_policy_decision"] = (
            "review_only_nonabstaining_candidate"
        )
        row["expected_frozen_policy_match"] = True
        row["expected_claim_status"] = "review_only_nonabstaining_candidate"
        row["expected_claim_status_match"] = True
        mutated_count += 1
    if not mutated_count:
        raise ValueError("unsafe nonabstention fault requires control-like rows")
    mutated["metadata"]["unsafe_control_nonabstention_fault_row_count"] = mutated_count
    recompute_result_metadata(mutated)
    return mutated


def validate_negative_gate(
    gate: dict[str, Any],
    *,
    expected_failure: str,
    required_count_field: str,
) -> None:
    if gate.get("gate", {}).get("gate_pass") is not False:
        raise ValueError(f"{expected_failure} negative scoreboard gate must fail")
    summary = gate.get("scoreboard_summary") or {}
    if int(summary.get(required_count_field) or 0) <= 0:
        raise ValueError(
            f"{expected_failure} negative gate did not populate {required_count_field}"
        )
    if gate.get("gate", {}).get("progress_claim_allowed") is not False:
        raise ValueError(f"{expected_failure} gate must not allow progress claims")


def build_outputs(
    root: Path,
    output_dir: Path,
    run_stamp: str,
    policy_path: Path,
    *,
    max_entries: int,
) -> dict[str, Path]:
    literal_payloads = [
        (dict(spec), load_git_json(str(spec["ref"]), str(spec["path"])))
        for spec in REAL_OVERLAP_INPUT_SPECS_V5
    ]
    supplemental_payloads = {
        str(spec["lane_id"]): load_git_json(str(spec["ref"]), str(spec["path"]))
        for spec in SUPPLEMENTAL_SPECS_V6
    }
    policy = load_json(policy_path)
    tranche = build_precedence_tranche_from_payloads(
        literal_payloads,
        contact_payload=supplemental_payloads["epk_substrate_role_identity"],
        sibling_payload=supplemental_payloads["epk_sibling_controls"],
        false_positive_payload=supplemental_payloads["epk_false_positive_hunter"],
        max_entries=max_entries,
    )
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("entry precedence controls produced claim-status mismatches")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    source_leak_result_path = (
        output_dir / f"{stem}_negative_forbidden_source_leakage_result.json"
    )
    source_leak_gate_path = (
        output_dir / f"{stem}_negative_forbidden_source_leakage_scoreboard_gate.json"
    )
    unsafe_result_path = (
        output_dir / f"{stem}_negative_unsafe_control_nonabstention_result.json"
    )
    unsafe_gate_path = (
        output_dir / f"{stem}_negative_unsafe_control_nonabstention_scoreboard_gate.json"
    )
    report_path = output_dir / f"{stem}.json"

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)
    gate = build_artifact(root, [result_path])
    precedence_assertions = validate_precedence_scoreboard(gate)
    write_json(gate_path, gate, pretty=True)

    source_leak_tranche = source_leakage_negative_tranche(tranche)
    source_leak_result = evaluate_tranche(policy, source_leak_tranche)
    if source_leak_result["metadata"]["claim_status_counts"].get(
        "forbidden_source_leakage", 0
    ) <= 0:
        raise ValueError("source leakage fault did not emit forbidden_source_leakage")
    write_json(source_leak_result_path, source_leak_result, pretty=True)
    source_leak_gate = build_artifact(root, [source_leak_result_path])
    validate_negative_gate(
        source_leak_gate,
        expected_failure="forbidden_source_leakage",
        required_count_field="forbidden_source_leakage_count",
    )
    write_json(source_leak_gate_path, source_leak_gate, pretty=True)

    unsafe_result = unsafe_control_nonabstention_negative_result(result)
    write_json(unsafe_result_path, unsafe_result, pretty=True)
    unsafe_gate = build_artifact(root, [unsafe_result_path])
    validate_negative_gate(
        unsafe_gate,
        expected_failure="unsafe_control_nonabstention",
        required_count_field="unsafe_control_nonabstention_count",
    )
    write_json(unsafe_gate_path, unsafe_gate, pretty=True)

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
            "Candidate-level product/split rows can remain visible while "
            "entry-level claim status follows fail-closed precedence over analog, "
            "topology, sibling-control, unsafe nonabstention, and source-leakage "
            "contexts."
        ),
        "precedence_summary": {
            "rows_reviewed": result["metadata"]["row_count"],
            "entry_count": gate["scoreboard_summary"]["entry_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "entry_claim_status_counts": gate["scoreboard_summary"][
                "entry_claim_status_counts"
            ],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "entry_claim_status_precedence": list(ENTRY_CLAIM_STATUS_PRECEDENCE),
            "precedence_assertions": precedence_assertions,
            "positive_gate_pass": gate["gate"]["gate_pass"],
            "forbidden_source_leakage_gate_pass": source_leak_gate["gate"][
                "gate_pass"
            ],
            "unsafe_control_nonabstention_gate_pass": unsafe_gate["gate"][
                "gate_pass"
            ],
            "progress_claim_allowed": False,
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
            {
                "artifact": rel(source_leak_result_path, root),
                "scoreboard_gate_artifact": rel(source_leak_gate_path, root),
                "sha256": sha256_file(source_leak_result_path),
                "scoreboard_gate_sha256": sha256_file(source_leak_gate_path),
                "expected_failure": "forbidden_source_leakage",
                "gate_pass": source_leak_gate["gate"]["gate_pass"],
                "forbidden_source_leakage_count": source_leak_gate[
                    "scoreboard_summary"
                ]["forbidden_source_leakage_count"],
            },
            {
                "artifact": rel(unsafe_result_path, root),
                "scoreboard_gate_artifact": rel(unsafe_gate_path, root),
                "sha256": sha256_file(unsafe_result_path),
                "scoreboard_gate_sha256": sha256_file(unsafe_gate_path),
                "expected_failure": "unsafe_control_nonabstention",
                "gate_pass": unsafe_gate["gate"]["gate_pass"],
                "unsafe_control_nonabstention_count": unsafe_gate[
                    "scoreboard_summary"
                ]["unsafe_control_nonabstention_count"],
            },
        ],
        "artifacts": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(gate_path, root),
            "scoreboard_gate_sha256": sha256_file(gate_path),
            "negative_forbidden_source_leakage_result": rel(
                source_leak_result_path, root
            ),
            "negative_forbidden_source_leakage_scoreboard_gate": rel(
                source_leak_gate_path, root
            ),
            "negative_unsafe_control_nonabstention_result": rel(
                unsafe_result_path, root
            ),
            "negative_unsafe_control_nonabstention_scoreboard_gate": rel(
                unsafe_gate_path, root
            ),
        },
        "gate": {
            "gate_pass": gate["gate"]["gate_pass"],
            "negative_forbidden_source_leakage_gate_failed": source_leak_gate[
                "gate"
            ]["gate_pass"]
            is False,
            "negative_unsafe_control_nonabstention_gate_failed": unsafe_gate[
                "gate"
            ]["gate_pass"]
            is False,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
        },
    }
    write_json(report_path, report, pretty=True)
    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": gate_path,
        "negative_forbidden_source_leakage_result": source_leak_result_path,
        "negative_forbidden_source_leakage_scoreboard_gate": source_leak_gate_path,
        "negative_unsafe_control_nonabstention_result": unsafe_result_path,
        "negative_unsafe_control_nonabstention_scoreboard_gate": unsafe_gate_path,
        "report": report_path,
    }


def self_test() -> None:
    root = Path.cwd()
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
    literal_payloads = [
        (
            {
                "lane_id": "epk_positive_evidence",
                "path": "positive_fixture.json",
                "row_keys": ("adjudicated_candidate_rows",),
            },
            {
                "adjudicated_candidate_rows": [
                    {
                        "candidate_id": "1AAA:transition_analog",
                        "pdb_id": "1AAA",
                        "coordinate_state": "transition_analog",
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
    contact_payload = {
        "active_site_contact_interface_rows": [
            {
                "candidate_id": "2BBB|gamma=none|acceptor=none",
                "pdb_id": "2BBB",
                "source_free_evidence": {
                    "coordinate_state": "ambiguous_coordinate_state",
                    "blocker_class": "ligand_materialization",
                    "topology_class": "topology_unavailable",
                    "nucleotide_anchor_atom": {
                        "residue_code": "ANP",
                        "atom_name": "PB",
                    },
                },
            }
        ]
    }
    sibling_payload = {
        "gamma_proximity_counteraxis_cases": [
            {
                "case_id": "sibling_gamma_control",
                "pdb_id": "SIB1",
                "input_features": {
                    "gamma_capable_nucleotide_codes": ["ANP"],
                    "nearest_gamma_to_protein_hydroxyl_distance_angstrom": 4.1,
                    "metal_ligand_codes": ["MG"],
                },
                "expected_review_only_result": {"should_block_weak_rule_hit": True},
            }
        ],
        "product_phosphoryl_identity_counteraxis_cases": [
            {
                "case_id": "sibling_product_control",
                "pdb_id": "SIB2",
                "input_features": {
                    "product_or_partial_nucleotide_codes": ["ADP"],
                    "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom": 3.8,
                    "metal_ligand_codes": ["MG"],
                },
                "expected_review_only_result": {
                    "should_block_weak_product_rule_hit": True
                },
            }
        ],
    }
    false_positive_payload = {
        "rows": [
            {
                "fixture_id": "atpase_transporter_control",
                "pdb_id": "ATP1",
                "control_class": "atpase_transporter_topology_control",
                "non_epk_control": True,
                "observed_materializer_nonabstention": True,
                "candidate": {
                    "gamma_ligand_code": "ANP",
                    "gamma_atom_name": "PG",
                    "nearest_gamma_distance_angstrom": 4.0,
                    "nearest_mg_distance_angstrom": 2.2,
                },
            },
            {
                "fixture_id": "orc_mcm_control",
                "pdb_id": "ORC1",
                "control_class": "orc_mcm_biological_assembly_split_control",
                "non_epk_control": True,
                "observed_materializer_nonabstention": True,
                "candidate": {
                    "gamma_ligand_code": "ANP",
                    "gamma_atom_name": "PG",
                    "nearest_gamma_distance_angstrom": 4.5,
                    "nearest_mg_distance_angstrom": 2.4,
                },
            },
            {
                "fixture_id": "internal_fragment_control",
                "pdb_id": "INT1",
                "control_class": "walker_a_internal_fragment_topology_control",
                "non_epk_control": True,
                "observed_materializer_nonabstention": True,
                "candidate": {
                    "gamma_ligand_code": "ANP",
                    "gamma_atom_name": "PG",
                    "nearest_gamma_distance_angstrom": 4.7,
                    "nearest_mg_distance_angstrom": 2.5,
                },
            },
        ]
    }
    tranche = build_precedence_tranche_from_payloads(
        literal_payloads,
        contact_payload=contact_payload,
        sibling_payload=sibling_payload,
        false_positive_payload=false_positive_payload,
        max_entries=2,
    )
    result = evaluate_tranche(policy, tranche)
    assert result["metadata"]["expected_claim_status_mismatch_count"] == 0
    result_path = Path("/private/tmp/epk_entry_precedence_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(root, [result_path])
    assertions = validate_precedence_scoreboard(gate)
    assert assertions["product_analog_entries"] == ["1AAA"]
    assert assertions["split_topology_entries"] == ["2BBB"]

    leak_result = evaluate_tranche(policy, source_leakage_negative_tranche(tranche))
    leak_path = Path("/private/tmp/epk_entry_precedence_self_test_source_leak.json")
    write_json(leak_path, leak_result, pretty=False)
    leak_gate = build_artifact(root, [leak_path])
    validate_negative_gate(
        leak_gate,
        expected_failure="forbidden_source_leakage",
        required_count_field="forbidden_source_leakage_count",
    )

    unsafe_result = unsafe_control_nonabstention_negative_result(result)
    unsafe_path = Path("/private/tmp/epk_entry_precedence_self_test_unsafe.json")
    write_json(unsafe_path, unsafe_result, pretty=False)
    unsafe_gate = build_artifact(root, [unsafe_path])
    validate_negative_gate(
        unsafe_gate,
        expected_failure="unsafe_control_nonabstention",
        required_count_field="unsafe_control_nonabstention_count",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build compact review-only entry-precedence controls for federated "
            "candidate evidence rows."
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
