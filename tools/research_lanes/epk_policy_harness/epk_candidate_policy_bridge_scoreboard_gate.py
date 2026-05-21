#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from epk_policy_harness import (
    CLAIM_STATUS_VALUES,
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    SOURCE_LEAKAGE_ROW_FLAGS,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
GATE_VERSION = "epk_candidate_policy_bridge_scoreboard_gate_v1_20260521"
CONTROL_ROLE_TOKENS = (
    "sibling",
    "control",
    "atpase",
    "transporter",
    "orc",
    "mcm",
    "internal_fragment",
    "internal-fragment",
)
POLICY_DECISION_REQUIRED_FIELDS = (
    "schema_version",
    "row_id",
    "coordinate_state",
    "claim_status",
    "claim_admissibility",
    "abstention_reasons",
    "forbidden_predictive_context_flags",
    "production_claim_allowed",
    "labels_or_fingerprints_changed",
)
CANDIDATE_IDENTITY_REQUIRED_FIELDS = (
    "candidate_id",
    "source_lane_id",
    "source_artifact",
)
ENTRY_CLAIM_STATUS_PRECEDENCE = (
    "forbidden_source_leakage",
    "review_only_abstain_forbidden_context",
    "review_only_abstain_sibling_control",
    "review_only_abstain_topology_ambiguity",
    "review_only_abstain_split_state",
    "review_only_abstain_analog_state",
    "review_only_abstain_product_state",
    "review_only_abstain_missing_role_policy",
    "review_only_nonabstaining_candidate",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, payload: dict[str, Any], *, pretty: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if pretty:
            json.dump(payload, handle, indent=2, sort_keys=True)
        else:
            json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
        handle.write("\n")


def rel(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root.resolve()))
    except ValueError:
        return str(resolved)


def schema_drafts() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "review_only": True,
        "production_claim_allowed": False,
        "schemas": {
            "epk_candidate_evidence_v1": {
                "scope": "candidate_level_gamma_acceptor_pair_not_pdb_level",
                "candidate_identity_fields": [
                    "lane_id",
                    "source_lane_id",
                    "source_artifact",
                    "source_row_key",
                    "source_row_id",
                    "row_id",
                    "candidate_id",
                    "entry_id",
                    "pdb_id",
                    "model_id",
                    "chain_or_auth_asym_id",
                    "ligand_instance_id",
                    "terminal_gamma_atom_id",
                    "acceptor_atom_id",
                ],
                "candidate_identity_rule": (
                    "row_id or candidate_id identifies one gamma/acceptor candidate; "
                    "entry-level status is derived from candidate decisions"
                ),
                "required_fields": [
                    "schema_version",
                    "row_id",
                    "candidate_id",
                    "pdb_id",
                    "row_role",
                    "ligand_code_from_structure",
                    "coordinate_state",
                    "terminal_gamma_equivalent_geometry",
                    "local_metal_context",
                    "catalytic_site_locality",
                    "source_free_acceptor_role_features",
                    "same_structure_co_materialization",
                ],
                "coordinate_state_enum": sorted(COORDINATE_STATE_VALUES),
                "allowed_predictive_feature_boundary": [
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
                "review_only_context_fields": [
                    "source_query",
                    "source_validation_status",
                    "source_review_status",
                    "structure_title",
                    "entity_descriptions",
                    "chain_accessions",
                    "source_lane_id",
                    "source_artifact",
                    "source_row_key",
                    "source_row_id",
                    "expert_notes",
                    "product_state_context",
                    "substrate_acceptor_analog_context",
                    "split_state_context",
                    "sibling_counterfamily_context",
                ],
                "federated_source_provenance_rule": (
                    "source_lane_id/source_artifact/source_row_key/source_row_id "
                    "identify review-only emitting-lane provenance and must not "
                    "carry source text, protein names, titles, EC/Rhea, or paper "
                    "metadata as predictive features"
                ),
                "forbidden_predictive_flags": sorted(FORBIDDEN_ROW_FLAGS),
                "source_leakage_predictive_flags": sorted(SOURCE_LEAKAGE_ROW_FLAGS),
                "compact_artifact_rule": "do_not_write_large_raw_coordinate_dumps",
            },
            "epk_policy_decision_v1": {
                "required_fields": [
                    "schema_version",
                    "row_id",
                    "coordinate_state",
                    "claim_status",
                    "claim_admissibility",
                    "abstention_reasons",
                    "forbidden_predictive_context_flags",
                    "production_claim_allowed",
                    "labels_or_fingerprints_changed",
                ],
                "candidate_provenance_fields": [
                    "candidate_id",
                    "pdb_id",
                    "entry_id",
                    "source_lane_id",
                    "source_artifact",
                    "source_row_key",
                    "source_row_id",
                ],
                "federated_candidate_identity_rule": (
                    "candidate/source provenance is required for federated gate "
                    "tranches and remains review-only provenance, not a predictive "
                    "feature"
                ),
                "claim_status_enum": sorted(CLAIM_STATUS_VALUES),
                "claim_admissibility_enum": ["review_only", "forbidden"],
                "nonabstaining_is_review_only": True,
                "coordinate_state_enum": sorted(COORDINATE_STATE_VALUES),
                "production_scoring_rule": "not_production_scoring_or_label_import",
            },
            "epk_scoreboard_row_v1": {
                "required_fields": [
                    "source_result_artifact",
                    "tranche_id",
                    "rows_reviewed",
                    "entry_count",
                    "discovery_signal_row_count",
                    "claim_status_counts",
                    "entry_claim_status_counts",
                    "coordinate_state_counts",
                    "forbidden_source_leakage_count",
                    "unsafe_control_nonabstention_count",
                    "production_claim_allowed",
                    "labels_or_fingerprints_changed",
                ],
                "scoreboard_artifact_required_fields": [
                    "scoreboard_summary.covered_claim_status_values",
                    "scoreboard_summary.uncovered_claim_status_values",
                    "scoreboard_summary.covered_coordinate_state_values",
                    "scoreboard_summary.uncovered_coordinate_state_values",
                    "gate.gate_pass",
                ],
                "separates_discovery_signal_from_claim_admissibility": True,
                "entry_rollup_rule": (
                    "derive entry-level status from candidate-level decisions only; "
                    "keep candidate status counts visible and use fail-closed "
                    "precedence for forbidden/source leakage and review-only blockers"
                ),
                "entry_claim_status_precedence": list(ENTRY_CLAIM_STATUS_PRECEDENCE),
                "progress_gate": "fails on forbidden source leakage or unsafe control nonabstention",
            },
        },
    }


def is_control_like(row: dict[str, Any]) -> bool:
    haystack = " ".join(
        str(row.get(field) or "").lower()
        for field in (
            "row_id",
            "row_role",
            "post_score_review_status",
            "topology_ambiguity_status",
            "sibling_control_match_status",
        )
    )
    return any(token in haystack for token in CONTROL_ROLE_TOKENS)


def entry_key_for_row(row: dict[str, Any]) -> str:
    entry_id = str(row.get("entry_id") or "").strip()
    if entry_id:
        return entry_id
    pdb_id = str(row.get("pdb_id") or "").strip()
    if pdb_id:
        return pdb_id
    return str(row.get("row_id") or "unknown_entry").strip() or "unknown_entry"


def entry_claim_status_for_counts(claim_status_counts: dict[str, int]) -> str:
    for status in ENTRY_CLAIM_STATUS_PRECEDENCE:
        if claim_status_counts.get(status, 0):
            return status
    return "review_only_abstain_topology_ambiguity"


def build_entry_rollups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        entry_id = entry_key_for_row(row)
        rollup = grouped.setdefault(
            entry_id,
            {
                "entry_id": entry_id,
                "candidate_count": 0,
                "candidate_row_ids": [],
                "source_lane_ids": set(),
                "claim_status_counts": {},
                "coordinate_state_counts": {},
                "discovery_signal_candidate_count": 0,
                "nonabstaining_candidate_count": 0,
                "forbidden_source_leakage_rows": [],
                "unsafe_control_nonabstention_rows": [],
            },
        )
        rollup["candidate_count"] += 1
        rollup["candidate_row_ids"].append(row.get("row_id"))
        source_lane_id = str(row.get("source_lane_id") or "").strip()
        if source_lane_id:
            rollup["source_lane_ids"].add(source_lane_id)

        claim_status = str(row.get("claim_status") or "")
        coordinate_state = str(row.get("coordinate_state") or "")
        rollup["claim_status_counts"][claim_status] = (
            rollup["claim_status_counts"].get(claim_status, 0) + 1
        )
        rollup["coordinate_state_counts"][coordinate_state] = (
            rollup["coordinate_state_counts"].get(coordinate_state, 0) + 1
        )
        if (
            coordinate_state == "active_gamma"
            or row.get("nearest_gamma_acceptor_distance_angstrom") is not None
        ):
            rollup["discovery_signal_candidate_count"] += 1
        if claim_status == "review_only_nonabstaining_candidate":
            rollup["nonabstaining_candidate_count"] += 1
        if claim_status == "forbidden_source_leakage":
            rollup["forbidden_source_leakage_rows"].append(row.get("row_id"))
        if claim_status == "review_only_nonabstaining_candidate" and is_control_like(row):
            rollup["unsafe_control_nonabstention_rows"].append(row.get("row_id"))

    entry_rollups: list[dict[str, Any]] = []
    for entry_id in sorted(grouped):
        rollup = grouped[entry_id]
        entry_claim_status = entry_claim_status_for_counts(rollup["claim_status_counts"])
        entry_rollups.append(
            {
                "entry_id": entry_id,
                "candidate_count": rollup["candidate_count"],
                "candidate_row_ids": rollup["candidate_row_ids"],
                "source_lane_ids": sorted(rollup["source_lane_ids"]),
                "claim_status_counts": dict(sorted(rollup["claim_status_counts"].items())),
                "coordinate_state_counts": dict(
                    sorted(rollup["coordinate_state_counts"].items())
                ),
                "entry_claim_status": entry_claim_status,
                "entry_claim_admissibility": (
                    "forbidden"
                    if entry_claim_status == "forbidden_source_leakage"
                    else "review_only"
                ),
                "discovery_signal_candidate_count": rollup[
                    "discovery_signal_candidate_count"
                ],
                "nonabstaining_candidate_count": rollup[
                    "nonabstaining_candidate_count"
                ],
                "forbidden_source_leakage_rows": rollup[
                    "forbidden_source_leakage_rows"
                ],
                "unsafe_control_nonabstention_rows": rollup[
                    "unsafe_control_nonabstention_rows"
                ],
                "progress_claim_allowed": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
            }
        )
    return entry_rollups


def summarize_result(root: Path, result_path: Path, result: dict[str, Any]) -> dict[str, Any]:
    metadata = result.get("metadata", {})
    rows = result.get("rows")
    if metadata.get("review_only") is not True:
        raise ValueError(f"{result_path} metadata.review_only must be true")
    if metadata.get("production_claim_allowed") is not False:
        raise ValueError(f"{result_path} must not allow production claims")
    if metadata.get("labels_or_fingerprints_changed") is not False:
        raise ValueError(f"{result_path} must not change labels/fingerprints")
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"{result_path} metadata.schema_version must be {SCHEMA_VERSION}")
    if not isinstance(rows, list):
        raise ValueError(f"{result_path} rows must be a list")

    claim_status_counts: dict[str, int] = {}
    coordinate_state_counts: dict[str, int] = {}
    missing_schema_rows: list[str] = []
    missing_schema_details: list[dict[str, Any]] = []
    forbidden_source_leakage_rows: list[str] = []
    unsafe_control_nonabstention_rows: list[str] = []
    discovery_signal_row_count = 0
    valid_rows_for_rollup: list[dict[str, Any]] = []
    required_fields = list(POLICY_DECISION_REQUIRED_FIELDS)
    if metadata.get("require_candidate_identity_fields") is True:
        required_fields.extend(CANDIDATE_IDENTITY_REQUIRED_FIELDS)

    for row in rows:
        row_id = str(row.get("row_id") or row.get("pdb_id") or "unknown_row")
        missing_fields = [
            field
            for field in required_fields
            if field not in row or row.get(field) in (None, "")
        ]
        if missing_fields:
            missing_schema_rows.append(row_id)
            missing_schema_details.append(
                {"row_id": row_id, "missing_fields": missing_fields}
            )
        claim_status = row.get("claim_status")
        coordinate_state = row.get("coordinate_state")
        claim_admissibility = row.get("claim_admissibility")
        if row.get("schema_version") != SCHEMA_VERSION:
            missing_schema_rows.append(row_id)
            missing_schema_details.append(
                {"row_id": row_id, "invalid_field": "schema_version"}
            )
        if claim_status not in CLAIM_STATUS_VALUES:
            missing_schema_rows.append(row_id)
            missing_schema_details.append(
                {"row_id": row_id, "invalid_field": "claim_status"}
            )
            continue
        if coordinate_state not in COORDINATE_STATE_VALUES:
            missing_schema_rows.append(row_id)
            missing_schema_details.append(
                {"row_id": row_id, "invalid_field": "coordinate_state"}
            )
            continue
        expected_admissibility = (
            "forbidden" if claim_status == "forbidden_source_leakage" else "review_only"
        )
        if claim_admissibility != expected_admissibility:
            missing_schema_rows.append(row_id)
            missing_schema_details.append(
                {
                    "row_id": row_id,
                    "invalid_field": "claim_admissibility",
                    "expected": expected_admissibility,
                    "actual": claim_admissibility,
                }
            )
        valid_rows_for_rollup.append(row)
        claim_status_counts[claim_status] = claim_status_counts.get(claim_status, 0) + 1
        coordinate_state_counts[coordinate_state] = (
            coordinate_state_counts.get(coordinate_state, 0) + 1
        )
        if (
            coordinate_state == "active_gamma"
            or row.get("nearest_gamma_acceptor_distance_angstrom") is not None
        ):
            discovery_signal_row_count += 1
        if claim_status == "forbidden_source_leakage":
            forbidden_source_leakage_rows.append(row_id)
        if (
            claim_status == "review_only_nonabstaining_candidate"
            and is_control_like(row)
        ):
            unsafe_control_nonabstention_rows.append(row_id)

    if metadata.get("claim_status_counts") not in (None, claim_status_counts):
        raise ValueError(f"{result_path} metadata.claim_status_counts drifted from rows")
    if metadata.get("coordinate_state_counts") not in (None, coordinate_state_counts):
        raise ValueError(
            f"{result_path} metadata.coordinate_state_counts drifted from rows"
        )

    expected_mismatch_count = int(metadata.get("expected_decision_mismatch_count") or 0)
    expected_claim_mismatch_count = int(
        metadata.get("expected_claim_status_mismatch_count") or 0
    )
    entry_rollups = build_entry_rollups(valid_rows_for_rollup)
    entry_claim_status_counts: dict[str, int] = {}
    for entry_rollup in entry_rollups:
        entry_claim_status = entry_rollup["entry_claim_status"]
        entry_claim_status_counts[entry_claim_status] = (
            entry_claim_status_counts.get(entry_claim_status, 0) + 1
        )
    gate_pass = not (
        missing_schema_rows
        or forbidden_source_leakage_rows
        or unsafe_control_nonabstention_rows
        or expected_mismatch_count
        or expected_claim_mismatch_count
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "scoreboard_schema": "epk_scoreboard_row_v1",
        "source_result_artifact": rel(result_path, root),
        "source_result_sha256": sha256_file(result_path),
        "tranche_id": metadata.get("tranche_id"),
        "policy_version": metadata.get("policy_version"),
        "rows_reviewed": len(rows),
        "entry_count": len(entry_rollups),
        "discovery_signal_row_count": discovery_signal_row_count,
        "claim_status_counts": claim_status_counts,
        "entry_claim_status_counts": entry_claim_status_counts,
        "coordinate_state_counts": coordinate_state_counts,
        "entry_rollup_contract": {
            "candidate_rows_are_source_of_truth": True,
            "entry_status_derived_from_candidate_decisions": True,
            "claim_admissibility_separate_from_discovery_signal": True,
            "fail_closed_claim_status_precedence": list(
                ENTRY_CLAIM_STATUS_PRECEDENCE
            ),
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
        },
        "entry_rollups": entry_rollups,
        "forbidden_source_leakage_count": len(forbidden_source_leakage_rows),
        "forbidden_source_leakage_rows": forbidden_source_leakage_rows,
        "unsafe_control_nonabstention_count": len(unsafe_control_nonabstention_rows),
        "unsafe_control_nonabstention_rows": unsafe_control_nonabstention_rows,
        "expected_decision_mismatch_count": expected_mismatch_count,
        "expected_claim_status_mismatch_count": expected_claim_mismatch_count,
        "missing_schema_row_count": len(set(missing_schema_rows)),
        "missing_schema_rows": sorted(set(missing_schema_rows)),
        "missing_schema_details": missing_schema_details,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "gate_pass": gate_pass,
    }


def merge_counts(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    merged: dict[str, int] = {}
    for row in rows:
        for key, value in row[field].items():
            merged[key] = merged.get(key, 0) + int(value)
    return merged


def build_artifact(root: Path, result_paths: list[Path]) -> dict[str, Any]:
    scoreboard_rows = [
        summarize_result(root, result_path, load_json(result_path))
        for result_path in result_paths
    ]
    gate_failures = [
        row
        for row in scoreboard_rows
        if row["gate_pass"] is not True
    ]
    aggregate_claim_status_counts = merge_counts(scoreboard_rows, "claim_status_counts")
    aggregate_entry_claim_status_counts = merge_counts(
        scoreboard_rows, "entry_claim_status_counts"
    )
    aggregate_coordinate_state_counts = merge_counts(
        scoreboard_rows, "coordinate_state_counts"
    )
    total_rows_reviewed = sum(row["rows_reviewed"] for row in scoreboard_rows)
    total_entry_count = sum(row["entry_count"] for row in scoreboard_rows)
    total_discovery_signal_rows = sum(
        row["discovery_signal_row_count"] for row in scoreboard_rows
    )
    return {
        "metadata": {
            "artifact_id": GATE_VERSION,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "gate_version": GATE_VERSION,
            "result_artifact_count": len(result_paths),
            "scoreboard_row_count": len(scoreboard_rows),
            "gate_pass": not gate_failures,
            "primary_outcome": "scoreboard_gate_created",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "schema_drafts": schema_drafts(),
        "scoreboard_summary": {
            "rows_reviewed": total_rows_reviewed,
            "entry_count": total_entry_count,
            "discovery_signal_row_count": total_discovery_signal_rows,
            "claim_status_counts": aggregate_claim_status_counts,
            "entry_claim_status_counts": aggregate_entry_claim_status_counts,
            "coordinate_state_counts": aggregate_coordinate_state_counts,
            "forbidden_source_leakage_count": sum(
                row["forbidden_source_leakage_count"] for row in scoreboard_rows
            ),
            "unsafe_control_nonabstention_count": sum(
                row["unsafe_control_nonabstention_count"] for row in scoreboard_rows
            ),
            "covered_claim_status_values": sorted(aggregate_claim_status_counts),
            "uncovered_claim_status_values": sorted(
                CLAIM_STATUS_VALUES - set(aggregate_claim_status_counts)
            ),
            "covered_entry_claim_status_values": sorted(
                aggregate_entry_claim_status_counts
            ),
            "uncovered_entry_claim_status_values": sorted(
                CLAIM_STATUS_VALUES - set(aggregate_entry_claim_status_counts)
            ),
            "covered_coordinate_state_values": sorted(aggregate_coordinate_state_counts),
            "uncovered_coordinate_state_values": sorted(
                COORDINATE_STATE_VALUES - set(aggregate_coordinate_state_counts)
            ),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "scoreboard_rows": scoreboard_rows,
        "gate": {
            "gate_pass": not gate_failures,
            "failure_count": len(gate_failures),
            "failed_result_artifacts": [
                row["source_result_artifact"] for row in gate_failures
            ],
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }


def self_test() -> None:
    root = Path.cwd()
    result_path = Path("/private/tmp/epk_policy_bridge_scoreboard_gate_self_test.json")
    good_result = {
        "metadata": {
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "require_candidate_identity_fields": False,
            "tranche_id": "self_test",
            "policy_version": "self_test",
            "claim_status_counts": {
                "review_only_abstain_missing_role_policy": 1,
            },
            "coordinate_state_counts": {
                "active_gamma": 1,
            },
        },
        "rows": [
            {
                "schema_version": SCHEMA_VERSION,
                "row_id": "candidate:active",
                "row_role": "geometry_lead",
                "coordinate_state": "active_gamma",
                "claim_status": "review_only_abstain_missing_role_policy",
                "claim_admissibility": "review_only",
                "abstention_reasons": ["missing_required_same_structure_features"],
                "forbidden_predictive_context_flags": [],
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "nearest_gamma_acceptor_distance_angstrom": 3.2,
            }
        ],
    }
    write_json(result_path, good_result, pretty=False)
    good_summary = summarize_result(root, result_path, good_result)
    assert good_summary["gate_pass"] is True
    assert good_summary["entry_count"] == 1
    assert good_summary["entry_claim_status_counts"] == {
        "review_only_abstain_missing_role_policy": 1,
    }
    assert good_summary["entry_rollups"][0]["entry_claim_status"] == (
        "review_only_abstain_missing_role_policy"
    )
    assert good_summary["entry_rollups"][0]["progress_claim_allowed"] is False
    bad_result = json.loads(json.dumps(good_result))
    bad_result["rows"][0]["row_id"] = "candidate:sibling_control"
    bad_result["rows"][0]["row_role"] = "sibling_control"
    bad_result["rows"][0]["claim_status"] = "review_only_nonabstaining_candidate"
    bad_result["metadata"]["claim_status_counts"] = {
        "review_only_nonabstaining_candidate": 1,
    }
    bad_summary = summarize_result(root, result_path, bad_result)
    assert bad_summary["gate_pass"] is False
    assert bad_summary["unsafe_control_nonabstention_count"] == 1
    assert bad_summary["entry_rollups"][0]["unsafe_control_nonabstention_rows"] == [
        "candidate:sibling_control",
    ]
    source_leak = json.loads(json.dumps(good_result))
    source_leak["rows"][0]["claim_status"] = "forbidden_source_leakage"
    source_leak["metadata"]["claim_status_counts"] = {
        "forbidden_source_leakage": 1,
    }
    leak_summary = summarize_result(root, result_path, source_leak)
    assert leak_summary["gate_pass"] is False
    assert leak_summary["forbidden_source_leakage_count"] == 1
    assert leak_summary["entry_claim_status_counts"] == {"forbidden_source_leakage": 1}
    assert leak_summary["entry_rollups"][0]["entry_claim_admissibility"] == "forbidden"
    mixed_entry = json.loads(json.dumps(good_result))
    mixed_entry["metadata"]["claim_status_counts"] = {
        "review_only_abstain_product_state": 1,
        "review_only_nonabstaining_candidate": 1,
    }
    mixed_entry["metadata"]["coordinate_state_counts"] = {
        "active_gamma": 1,
        "product_state": 1,
    }
    mixed_entry["rows"][0]["pdb_id"] = "MIXED"
    mixed_entry["rows"][0]["claim_status"] = "review_only_nonabstaining_candidate"
    mixed_entry["rows"][0]["claim_admissibility"] = "review_only"
    product_row = json.loads(json.dumps(good_result["rows"][0]))
    product_row["row_id"] = "candidate:product_state"
    product_row["pdb_id"] = "MIXED"
    product_row["coordinate_state"] = "product_state"
    product_row["claim_status"] = "review_only_abstain_product_state"
    mixed_entry["rows"].append(product_row)
    mixed_summary = summarize_result(root, result_path, mixed_entry)
    assert mixed_summary["gate_pass"] is True
    assert mixed_summary["entry_count"] == 1
    assert mixed_summary["entry_rollups"][0]["candidate_count"] == 2
    assert mixed_summary["entry_rollups"][0]["nonabstaining_candidate_count"] == 1
    assert mixed_summary["entry_rollups"][0]["entry_claim_status"] == (
        "review_only_abstain_product_state"
    )
    split_topology = json.loads(json.dumps(good_result))
    split_topology["metadata"]["claim_status_counts"] = {
        "review_only_abstain_split_state": 1,
        "review_only_abstain_topology_ambiguity": 1,
    }
    split_topology["metadata"]["coordinate_state_counts"] = {
        "ambiguous_coordinate_state": 1,
        "split_state": 1,
    }
    split_topology["rows"][0]["pdb_id"] = "SPLIT_TOPOLOGY"
    split_topology["rows"][0]["coordinate_state"] = "split_state"
    split_topology["rows"][0]["claim_status"] = "review_only_abstain_split_state"
    split_topology["rows"][0]["claim_admissibility"] = "review_only"
    topology_row = json.loads(json.dumps(good_result["rows"][0]))
    topology_row["row_id"] = "candidate:topology_ambiguity"
    topology_row["pdb_id"] = "SPLIT_TOPOLOGY"
    topology_row["coordinate_state"] = "ambiguous_coordinate_state"
    topology_row["claim_status"] = "review_only_abstain_topology_ambiguity"
    topology_row["claim_admissibility"] = "review_only"
    split_topology["rows"].append(topology_row)
    split_topology_summary = summarize_result(root, result_path, split_topology)
    assert split_topology_summary["gate_pass"] is True
    assert split_topology_summary["entry_rollups"][0]["entry_claim_status"] == (
        "review_only_abstain_topology_ambiguity"
    )
    forbidden_mixed = json.loads(json.dumps(good_result))
    forbidden_mixed["metadata"]["claim_status_counts"] = {
        "forbidden_source_leakage": 1,
        "review_only_abstain_sibling_control": 1,
    }
    forbidden_mixed["metadata"]["coordinate_state_counts"] = {
        "active_gamma": 2,
    }
    forbidden_mixed["rows"][0]["pdb_id"] = "FORBIDDEN_MIXED"
    forbidden_mixed["rows"][0]["claim_status"] = "forbidden_source_leakage"
    forbidden_mixed["rows"][0]["claim_admissibility"] = "forbidden"
    sibling_row = json.loads(json.dumps(good_result["rows"][0]))
    sibling_row["row_id"] = "candidate:sibling_abstaining_control"
    sibling_row["pdb_id"] = "FORBIDDEN_MIXED"
    sibling_row["row_role"] = "sibling_control"
    sibling_row["claim_status"] = "review_only_abstain_sibling_control"
    sibling_row["claim_admissibility"] = "review_only"
    forbidden_mixed["rows"].append(sibling_row)
    forbidden_mixed_summary = summarize_result(root, result_path, forbidden_mixed)
    assert forbidden_mixed_summary["gate_pass"] is False
    assert forbidden_mixed_summary["forbidden_source_leakage_count"] == 1
    assert forbidden_mixed_summary["entry_rollups"][0]["entry_claim_status"] == (
        "forbidden_source_leakage"
    )
    missing_schema = json.loads(json.dumps(good_result))
    del missing_schema["rows"][0]["schema_version"]
    del missing_schema["rows"][0]["claim_admissibility"]
    missing_schema_summary = summarize_result(root, result_path, missing_schema)
    assert missing_schema_summary["gate_pass"] is False
    assert missing_schema_summary["missing_schema_row_count"] == 1
    assert missing_schema_summary["missing_schema_details"][0]["missing_fields"] == [
        "schema_version",
        "claim_admissibility",
    ]
    missing_identity = json.loads(json.dumps(good_result))
    missing_identity["metadata"]["require_candidate_identity_fields"] = True
    missing_identity_summary = summarize_result(root, result_path, missing_identity)
    assert missing_identity_summary["gate_pass"] is False
    assert missing_identity_summary["missing_schema_row_count"] == 1
    assert missing_identity_summary["missing_schema_details"][0]["missing_fields"] == [
        "candidate_id",
        "source_lane_id",
        "source_artifact",
    ]
    bad_admissibility = json.loads(json.dumps(good_result))
    bad_admissibility["rows"][0]["claim_admissibility"] = "forbidden"
    bad_admissibility_summary = summarize_result(
        root, result_path, bad_admissibility
    )
    assert bad_admissibility_summary["gate_pass"] is False
    assert any(
        detail.get("invalid_field") == "claim_admissibility"
        for detail in bad_admissibility_summary["missing_schema_details"]
    )
    drift = json.loads(json.dumps(good_result))
    drift["metadata"]["claim_status_counts"] = {
        "review_only_abstain_product_state": 1,
    }
    try:
        summarize_result(root, result_path, drift)
    except ValueError as error:
        assert "claim_status_counts drifted" in str(error)
    else:
        raise AssertionError("scoreboard gate must reject metadata count drift")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build compact review-only ePK candidate policy bridge schema and "
            "scoreboard gate artifacts."
        )
    )
    parser.add_argument("--result", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--schema-output", type=Path)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    if not args.result or not args.output:
        parser.error("--result and --output are required unless --self-test is set")

    root = Path.cwd()
    artifact = build_artifact(root, args.result)
    write_json(args.output, artifact, pretty=not args.compact)
    if args.schema_output:
        schema_artifact = {
            "metadata": {
                "artifact_id": f"{SCHEMA_VERSION}_drafts",
                "created_at": utc_now(),
                "lane_id": LANE_ID,
                "review_only": True,
                "schema_version": SCHEMA_VERSION,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "primary_outcome": "schema_frozen_review_only",
            },
            **schema_drafts(),
        }
        write_json(args.schema_output, schema_artifact, pretty=not args.compact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
