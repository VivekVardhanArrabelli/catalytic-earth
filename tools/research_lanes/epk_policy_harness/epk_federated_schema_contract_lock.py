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
    build_entry_rollups,
    rel,
    schema_drafts,
    write_json,
)
from epk_policy_harness import (
    CLAIM_STATUS_VALUES,
    COORDINATE_STATE_VALUES,
    FEDERATED_ADAPTER_FORBIDDEN_COPIED_FIELDS,
    FORBIDDEN_ROW_FLAGS,
    SCHEMA_VERSION,
    SOURCE_DERIVED_ALLOWED_FEATURE_DENYLIST,
    SOURCE_LEAKAGE_ROW_FLAGS,
    load_json,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_candidate_entry_rollup_schema_contract_lock_v7"
DEFAULT_ARTIFACT_DIR = Path("artifacts/research_lanes/epk_policy_harness")

CANDIDATE_IDENTITY_REQUIRED_FIELDS = (
    "candidate_id",
    "source_lane_id",
    "source_artifact",
    "source_row_key",
    "source_row_id",
)
ENTRY_IDENTITY_REQUIRED_FIELDS = ("entry_id", "pdb_id")
POLICY_DECISION_REQUIRED_FIELDS = (
    "schema_version",
    "row_id",
    "candidate_id",
    "source_lane_id",
    "source_artifact",
    "source_row_key",
    "source_row_id",
    "entry_id",
    "pdb_id",
    "coordinate_state",
    "claim_status",
    "claim_admissibility",
    "abstention_reasons",
    "forbidden_predictive_context_flags",
    "production_claim_allowed",
    "labels_or_fingerprints_changed",
)
CANDIDATE_EVIDENCE_REQUIRED_FIELDS = (
    "schema_version",
    "row_id",
    "candidate_id",
    "source_lane_id",
    "source_artifact",
    "source_row_key",
    "source_row_id",
    "entry_id",
    "pdb_id",
    "row_role",
    "ligand_code_from_structure",
    "coordinate_state",
    "terminal_gamma_equivalent_geometry",
    "local_metal_context",
    "catalytic_site_locality",
    "source_free_acceptor_role_features",
    "same_structure_co_materialization",
)
ENTRY_ROLLUP_REQUIRED_FIELDS = (
    "entry_id",
    "candidate_count",
    "candidate_row_ids",
    "source_lane_ids",
    "claim_status_counts",
    "coordinate_state_counts",
    "entry_claim_status",
    "entry_claim_admissibility",
    "discovery_signal_candidate_count",
    "nonabstaining_candidate_count",
    "progress_claim_allowed",
    "production_claim_allowed",
    "labels_or_fingerprints_changed",
)
FAULTS = (
    "missing_candidate_provenance",
    "copied_source_context",
    "source_derived_predictive_feature",
    "invalid_coordinate_state",
    "invalid_claim_admissibility",
    "metadata_count_drift",
    "entry_rollup_precedence_drift",
)


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def latest_path(output_dir: Path, pattern: str) -> Path:
    matches = sorted(
        path for path in output_dir.glob(pattern) if "_negative_" not in path.name
    )
    if not matches:
        raise FileNotFoundError(f"no artifacts match {output_dir / pattern}")
    return matches[-1]


def nonempty(value: Any) -> bool:
    return value not in (None, "", [], {})


def required_nonempty(row: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if not nonempty(row.get(field))]


def forbidden_copied_fields(row: dict[str, Any]) -> list[str]:
    return [
        field
        for field in FEDERATED_ADAPTER_FORBIDDEN_COPIED_FIELDS
        if nonempty(row.get(field))
    ]


def forbidden_true_flags(row: dict[str, Any]) -> list[str]:
    return [flag for flag in FORBIDDEN_ROW_FLAGS if row.get(flag) is True]


def source_leakage_true_flags(row: dict[str, Any]) -> list[str]:
    return [flag for flag in SOURCE_LEAKAGE_ROW_FLAGS if row.get(flag) is True]


def count_rows(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field) or "") for row in rows).items()))


def validate_allowed_predictive_features(payload: dict[str, Any]) -> None:
    allowed = payload.get("allowed_predictive_features", [])
    if allowed is None:
        return
    if not isinstance(allowed, list):
        raise ValueError("allowed_predictive_features must be a list")
    allowed_set = {str(feature) for feature in allowed}
    denied = sorted(allowed_set & set(SOURCE_DERIVED_ALLOWED_FEATURE_DENYLIST))
    denied.extend(sorted(allowed_set & set(FORBIDDEN_ROW_FLAGS)))
    if denied:
        raise ValueError(
            "allowed_predictive_features include source-derived or forbidden fields: "
            f"{sorted(set(denied))}"
        )


def validate_schema_drafts_contract(drafts: dict[str, Any]) -> dict[str, Any]:
    schemas = drafts.get("schemas")
    if not isinstance(schemas, dict):
        raise ValueError("schema drafts require schemas object")
    required_schema_names = {
        "epk_candidate_evidence_v1",
        "epk_scoreboard_row_v1",
        "epk_policy_decision_v1",
    }
    missing_schemas = sorted(required_schema_names - set(schemas))
    if missing_schemas:
        raise ValueError(f"schema drafts missing schemas: {missing_schemas}")

    candidate = schemas["epk_candidate_evidence_v1"]
    decision = schemas["epk_policy_decision_v1"]
    scoreboard = schemas["epk_scoreboard_row_v1"]
    candidate_required = set(candidate.get("required_fields") or [])
    missing_candidate_fields = sorted(
        set(CANDIDATE_EVIDENCE_REQUIRED_FIELDS) - candidate_required
    )
    if missing_candidate_fields:
        raise ValueError(
            "epk_candidate_evidence_v1 missing required federated fields: "
            f"{missing_candidate_fields}"
        )
    decision_required = set(decision.get("required_fields") or [])
    missing_decision_fields = sorted(
        {
            "schema_version",
            "row_id",
            "coordinate_state",
            "claim_status",
            "claim_admissibility",
            "abstention_reasons",
            "forbidden_predictive_context_flags",
            "production_claim_allowed",
            "labels_or_fingerprints_changed",
        }
        - decision_required
    )
    if missing_decision_fields:
        raise ValueError(
            "epk_policy_decision_v1 missing required fields: "
            f"{missing_decision_fields}"
        )
    if set(candidate.get("coordinate_state_enum") or []) != COORDINATE_STATE_VALUES:
        raise ValueError("candidate coordinate_state_enum drifted")
    state_rules = candidate.get("coordinate_state_field_rules") or {}
    for state in ("ligand_absent", "unavailable_coordinate_state"):
        rule = state_rules.get(state) or {}
        if rule.get("ligand_code_from_structure") != "field_present_may_be_null":
            raise ValueError(
                "candidate coordinate_state_field_rules must allow explicit "
                f"{state} rows to carry a present-but-null ligand_code_from_structure"
            )
        if rule.get("coordinate_ligand_materialized_from_structure") is not False:
            raise ValueError(
                "candidate coordinate_state_field_rules must mark "
                f"{state} as not coordinate-ligand materialized"
            )
    metal_rule = state_rules.get("metal_absent") or {}
    if metal_rule.get("local_metal_context") is not False:
        raise ValueError(
            "candidate coordinate_state_field_rules must mark metal_absent "
            "with local_metal_context=false"
        )
    adp_rule = state_rules.get("adp_state") or {}
    if adp_rule.get("claim_status") != "review_only_abstain_product_state":
        raise ValueError(
            "candidate coordinate_state_field_rules must keep adp_state "
            "under review_only_abstain_product_state"
        )
    if set(decision.get("coordinate_state_enum") or []) != COORDINATE_STATE_VALUES:
        raise ValueError("decision coordinate_state_enum drifted")
    if set(decision.get("claim_status_enum") or []) != CLAIM_STATUS_VALUES:
        raise ValueError("decision claim_status_enum drifted")
    if tuple(scoreboard.get("entry_claim_status_precedence") or []) != (
        ENTRY_CLAIM_STATUS_PRECEDENCE
    ):
        raise ValueError("scoreboard entry precedence drifted")
    allowed_boundary = set(candidate.get("allowed_predictive_feature_boundary") or [])
    denied_boundary = sorted(
        (allowed_boundary & set(SOURCE_DERIVED_ALLOWED_FEATURE_DENYLIST))
        | (allowed_boundary & set(FORBIDDEN_ROW_FLAGS))
    )
    if denied_boundary:
        raise ValueError(
            "candidate allowed predictive boundary includes forbidden/source fields: "
            f"{denied_boundary}"
        )
    return {
        "schema_names": sorted(required_schema_names),
        "candidate_required_field_count": len(candidate_required),
        "coordinate_state_values": sorted(COORDINATE_STATE_VALUES),
        "claim_status_values": sorted(CLAIM_STATUS_VALUES),
        "entry_claim_status_precedence": list(ENTRY_CLAIM_STATUS_PRECEDENCE),
    }


def validate_candidate_evidence_tranche(tranche: dict[str, Any]) -> dict[str, Any]:
    metadata = tranche.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("candidate evidence tranche must be review_only=true")
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("candidate evidence tranche schema_version drifted")
    if metadata.get("production_claim_allowed") is not False:
        raise ValueError("candidate evidence tranche must not allow production claims")
    if metadata.get("labels_or_fingerprints_changed") is not False:
        raise ValueError("candidate evidence tranche must not change labels")
    rows = tranche.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("candidate evidence tranche requires non-empty rows")
    if metadata.get("row_count") not in (None, len(rows)):
        raise ValueError("candidate evidence tranche row_count drifted")

    row_ids: set[str] = set()
    candidate_keys: set[tuple[str, str]] = set()
    source_lanes: set[str] = set()
    for row in rows:
        row_id = str(row.get("row_id") or "unknown_row")
        missing_existing = [
            field for field in CANDIDATE_EVIDENCE_REQUIRED_FIELDS if field not in row
        ]
        missing_identity = required_nonempty(
            row,
            CANDIDATE_IDENTITY_REQUIRED_FIELDS
            + ENTRY_IDENTITY_REQUIRED_FIELDS
            + ("row_id",),
        )
        if missing_existing or missing_identity:
            raise ValueError(
                f"candidate evidence row {row_id} missing fields: "
                f"{sorted(set(missing_existing + missing_identity))}"
            )
        if row_id in row_ids:
            raise ValueError(f"candidate evidence row_id is duplicated: {row_id}")
        row_ids.add(row_id)
        source_lane_id = str(row["source_lane_id"])
        if source_lane_id == LANE_ID:
            raise ValueError(
                f"candidate evidence row {row_id} uses harness lane as source lane"
            )
        source_lanes.add(source_lane_id)
        candidate_key = (source_lane_id, str(row["candidate_id"]))
        if candidate_key in candidate_keys:
            raise ValueError(
                "candidate evidence candidate_id is duplicated within source lane: "
                f"{candidate_key}"
            )
        candidate_keys.add(candidate_key)
        coordinate_state = row.get("coordinate_state")
        if coordinate_state not in COORDINATE_STATE_VALUES:
            raise ValueError(
                f"candidate evidence row {row_id} has invalid coordinate_state: "
                f"{coordinate_state}"
            )
        expected_claim_status = row.get("expected_claim_status")
        if expected_claim_status is not None and expected_claim_status not in CLAIM_STATUS_VALUES:
            raise ValueError(
                f"candidate evidence row {row_id} has invalid expected_claim_status: "
                f"{expected_claim_status}"
            )
        copied_fields = forbidden_copied_fields(row)
        if copied_fields:
            raise ValueError(
                f"candidate evidence row {row_id} copies forbidden source context: "
                f"{copied_fields}"
            )
        leakage_flags = source_leakage_true_flags(row)
        if leakage_flags:
            raise ValueError(
                f"candidate evidence row {row_id} sets source leakage flags: "
                f"{leakage_flags}"
            )
        true_flags = forbidden_true_flags(row)
        if true_flags:
            raise ValueError(
                f"candidate evidence row {row_id} sets forbidden predictive flags: "
                f"{true_flags}"
            )
    if len(source_lanes) < 2:
        raise ValueError("candidate evidence tranche requires at least two source lanes")
    return {
        "rows_reviewed": len(rows),
        "source_lane_count": len(source_lanes),
        "source_lanes": sorted(source_lanes),
        "coordinate_state_counts": count_rows(rows, "coordinate_state"),
    }


def validate_policy_result(result: dict[str, Any]) -> dict[str, Any]:
    validate_allowed_predictive_features(result)
    metadata = result.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("policy result must be review_only=true")
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("policy result schema_version drifted")
    for flag in ("production_claim_allowed", "labels_or_fingerprints_changed"):
        if metadata.get(flag) is not False:
            raise ValueError(f"policy result metadata.{flag} must be false")
    rows = result.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("policy result requires non-empty rows")
    if metadata.get("row_count") not in (None, len(rows)):
        raise ValueError("policy result row_count drifted")

    row_ids: set[str] = set()
    candidate_keys: set[tuple[str, str]] = set()
    source_lanes: set[str] = set()
    for row in rows:
        row_id = str(row.get("row_id") or "unknown_row")
        missing_existing = [
            field for field in POLICY_DECISION_REQUIRED_FIELDS if field not in row
        ]
        missing_identity = required_nonempty(
            row,
            CANDIDATE_IDENTITY_REQUIRED_FIELDS
            + ENTRY_IDENTITY_REQUIRED_FIELDS
            + ("row_id",),
        )
        missing = sorted(set(missing_existing + missing_identity))
        if missing:
            raise ValueError(f"policy result row {row_id} missing fields: {missing}")
        if row_id in row_ids:
            raise ValueError(f"policy result row_id is duplicated: {row_id}")
        row_ids.add(row_id)
        source_lane_id = str(row["source_lane_id"])
        if source_lane_id == LANE_ID:
            raise ValueError(f"policy result row {row_id} uses harness as source lane")
        source_lanes.add(source_lane_id)
        candidate_key = (source_lane_id, str(row["candidate_id"]))
        if candidate_key in candidate_keys:
            raise ValueError(
                "policy result candidate_id is duplicated within source lane: "
                f"{candidate_key}"
            )
        candidate_keys.add(candidate_key)

        coordinate_state = row.get("coordinate_state")
        claim_status = row.get("claim_status")
        if coordinate_state not in COORDINATE_STATE_VALUES:
            raise ValueError(
                f"policy result row {row_id} has invalid coordinate_state: "
                f"{coordinate_state}"
            )
        if claim_status not in CLAIM_STATUS_VALUES:
            raise ValueError(
                f"policy result row {row_id} has invalid claim_status: {claim_status}"
            )
        expected_admissibility = (
            "forbidden" if claim_status == "forbidden_source_leakage" else "review_only"
        )
        if row.get("claim_admissibility") != expected_admissibility:
            raise ValueError(
                f"policy result row {row_id} claim_admissibility drifted: "
                f"{row.get('claim_admissibility')} != {expected_admissibility}"
            )
        if row.get("production_claim_allowed") is not False:
            raise ValueError(f"policy result row {row_id} allows production claims")
        if row.get("labels_or_fingerprints_changed") is not False:
            raise ValueError(f"policy result row {row_id} changes labels/fingerprints")
        if not isinstance(row.get("abstention_reasons"), list):
            raise ValueError(f"policy result row {row_id} abstention_reasons not list")
        if not isinstance(row.get("forbidden_predictive_context_flags"), list):
            raise ValueError(
                f"policy result row {row_id} forbidden_predictive_context_flags not list"
            )
        copied_fields = forbidden_copied_fields(row)
        if copied_fields:
            raise ValueError(
                f"policy result row {row_id} copies forbidden source context: "
                f"{copied_fields}"
            )
        leakage_flags = source_leakage_true_flags(row)
        if leakage_flags:
            raise ValueError(
                f"policy result row {row_id} sets source leakage flags: "
                f"{leakage_flags}"
            )
        true_flags = forbidden_true_flags(row)
        if true_flags:
            raise ValueError(
                f"policy result row {row_id} sets forbidden predictive flags: "
                f"{true_flags}"
            )

    if metadata.get("claim_status_counts") != count_rows(rows, "claim_status"):
        raise ValueError("policy result claim_status_counts drifted from rows")
    if metadata.get("coordinate_state_counts") != count_rows(rows, "coordinate_state"):
        raise ValueError("policy result coordinate_state_counts drifted from rows")
    if len(source_lanes) < 2:
        raise ValueError("policy result requires at least two source lanes")
    return {
        "rows_reviewed": len(rows),
        "source_lane_count": len(source_lanes),
        "source_lanes": sorted(source_lanes),
        "claim_status_counts": count_rows(rows, "claim_status"),
        "coordinate_state_counts": count_rows(rows, "coordinate_state"),
    }


def rollups_by_entry(rollups: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(rollup.get("entry_id")): rollup for rollup in rollups}


def validate_scoreboard_gate(result: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    metadata = gate.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("scoreboard gate must be review_only=true")
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("scoreboard gate schema_version drifted")
    if gate.get("gate", {}).get("gate_pass") is not True:
        raise ValueError("positive scoreboard gate must pass")
    if gate.get("gate", {}).get("production_claim_allowed") is not False:
        raise ValueError("scoreboard gate must not allow production claims")
    scoreboard_rows = gate.get("scoreboard_rows")
    if not isinstance(scoreboard_rows, list) or len(scoreboard_rows) != 1:
        raise ValueError("schema contract expects exactly one scoreboard row")
    scoreboard_row = scoreboard_rows[0]
    if scoreboard_row.get("gate_pass") is not True:
        raise ValueError("positive scoreboard row must pass")
    for field in (
        "rows_reviewed",
        "entry_count",
        "discovery_signal_row_count",
        "claim_status_counts",
        "entry_claim_status_counts",
        "coordinate_state_counts",
        "entry_rollups",
    ):
        if field not in scoreboard_row:
            raise ValueError(f"scoreboard row missing {field}")
    expected_rollups = rollups_by_entry(build_entry_rollups(result["rows"]))
    actual_rollups = rollups_by_entry(scoreboard_row.get("entry_rollups") or [])
    if set(actual_rollups) != set(expected_rollups):
        raise ValueError("scoreboard entry rollup entry set drifted")
    for entry_id, expected in expected_rollups.items():
        actual = actual_rollups[entry_id]
        missing = required_nonempty(actual, ENTRY_ROLLUP_REQUIRED_FIELDS)
        if missing:
            raise ValueError(f"entry rollup {entry_id} missing fields: {missing}")
        for field in (
            "candidate_count",
            "candidate_row_ids",
            "source_lane_ids",
            "claim_status_counts",
            "coordinate_state_counts",
            "entry_claim_status",
            "entry_claim_admissibility",
            "discovery_signal_candidate_count",
            "nonabstaining_candidate_count",
        ):
            if actual.get(field) != expected.get(field):
                raise ValueError(
                    f"entry rollup {entry_id} {field} drifted: "
                    f"{actual.get(field)} != {expected.get(field)}"
                )
        if actual.get("progress_claim_allowed") is not False:
            raise ValueError(f"entry rollup {entry_id} allows progress claims")
        if actual.get("production_claim_allowed") is not False:
            raise ValueError(f"entry rollup {entry_id} allows production claims")
    summary = gate.get("scoreboard_summary") or {}
    if summary.get("claim_status_counts") != count_rows(result["rows"], "claim_status"):
        raise ValueError("scoreboard claim_status_counts drifted from result rows")
    if summary.get("coordinate_state_counts") != count_rows(result["rows"], "coordinate_state"):
        raise ValueError("scoreboard coordinate_state_counts drifted from result rows")
    return {
        "entry_count": len(expected_rollups),
        "entry_claim_status_counts": summary.get("entry_claim_status_counts"),
        "scoreboard_gate_pass": True,
    }


def validate_contract_bundle(
    *,
    tranche: dict[str, Any],
    result: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    schema_summary = validate_schema_drafts_contract(schema_drafts())
    tranche_summary = validate_candidate_evidence_tranche(tranche)
    result_summary = validate_policy_result(result)
    gate_summary = validate_scoreboard_gate(result, gate)
    return {
        "schema": schema_summary,
        "candidate_evidence": tranche_summary,
        "policy_result": result_summary,
        "scoreboard_gate": gate_summary,
    }


def mutate_fault(
    fault: str,
    *,
    tranche: dict[str, Any],
    result: dict[str, Any],
    gate: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    fault_tranche = copy.deepcopy(tranche)
    fault_result = copy.deepcopy(result)
    fault_gate = copy.deepcopy(gate)
    if fault == "missing_candidate_provenance":
        fault_result["rows"][0].pop("source_row_id", None)
    elif fault == "copied_source_context":
        fault_result["rows"][0]["protein_names"] = ["copied source protein name"]
    elif fault == "source_derived_predictive_feature":
        fault_result.setdefault("allowed_predictive_features", []).append(
            "pdb_title_as_predictive_feature"
        )
    elif fault == "invalid_coordinate_state":
        fault_result["rows"][0]["coordinate_state"] = "state_from_source_title"
    elif fault == "invalid_claim_admissibility":
        fault_result["rows"][0]["claim_admissibility"] = "forbidden"
    elif fault == "metadata_count_drift":
        fault_result["metadata"]["claim_status_counts"] = {
            "review_only_nonabstaining_candidate": 999
        }
    elif fault == "entry_rollup_precedence_drift":
        rollups = fault_gate["scoreboard_rows"][0]["entry_rollups"]
        for rollup in rollups:
            claim_counts = rollup.get("claim_status_counts") or {}
            state_counts = rollup.get("coordinate_state_counts") or {}
            if state_counts.get("product_state") and claim_counts.get(
                "review_only_abstain_analog_state"
            ):
                rollup["entry_claim_status"] = "review_only_abstain_product_state"
                break
        else:
            raise ValueError("entry rollup precedence fault requires product/analog row")
    else:
        raise ValueError(f"unknown fault injection: {fault}")
    return fault_tranche, fault_result, fault_gate


def run_fault_injections(
    *,
    tranche: dict[str, Any],
    result: dict[str, Any],
    gate: dict[str, Any],
) -> list[dict[str, Any]]:
    fault_results: list[dict[str, Any]] = []
    for fault in FAULTS:
        fault_tranche, fault_result, fault_gate = mutate_fault(
            fault,
            tranche=tranche,
            result=result,
            gate=gate,
        )
        try:
            validate_contract_bundle(
                tranche=fault_tranche,
                result=fault_result,
                gate=fault_gate,
            )
        except ValueError as error:
            fault_results.append(
                {
                    "fault": fault,
                    "rejected": True,
                    "error": str(error),
                }
            )
        else:
            fault_results.append(
                {
                    "fault": fault,
                    "rejected": False,
                    "error": None,
                }
            )
    return fault_results


def build_schema_artifact() -> dict[str, Any]:
    drafts = schema_drafts()
    return {
        "metadata": {
            "artifact_id": f"{ARTIFACT_ID}_schema",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "contract_version": ARTIFACT_ID,
            "primary_outcome": "schema_frozen_review_only",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        **drafts,
        "schema_contract_lock_v7": {
            "candidate_evidence_required_fields": list(CANDIDATE_EVIDENCE_REQUIRED_FIELDS),
            "policy_decision_required_fields": list(POLICY_DECISION_REQUIRED_FIELDS),
            "entry_rollup_required_fields": list(ENTRY_ROLLUP_REQUIRED_FIELDS),
            "candidate_identity_unique_per_source_lane": True,
            "source_text_protein_titles_ec_rhea_paper_metadata_forbidden": True,
            "source_derived_predictive_features_forbidden": True,
            "entry_status_derived_from_candidate_decisions": True,
            "claim_admissibility_separate_from_discovery_signal": True,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
        },
    }


def build_outputs(
    root: Path,
    output_dir: Path,
    run_stamp: str,
    *,
    tranche_path: Path,
    result_path: Path,
    scoreboard_gate_path: Path,
) -> dict[str, Path]:
    tranche = load_json(tranche_path)
    result = load_json(result_path)
    gate = load_json(scoreboard_gate_path)
    positive_summary = validate_contract_bundle(
        tranche=tranche,
        result=result,
        gate=gate,
    )
    fault_results = run_fault_injections(
        tranche=tranche,
        result=result,
        gate=gate,
    )
    unexpected_passes = [
        item["fault"] for item in fault_results if item["rejected"] is not True
    ]
    if unexpected_passes:
        raise ValueError(f"schema contract fault injections passed: {unexpected_passes}")

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    schema_path = output_dir / f"{stem}_schema.json"
    gate_path = output_dir / f"{stem}_gate.json"
    report_path = output_dir / f"{stem}.json"

    schema_artifact = build_schema_artifact()
    write_json(schema_path, schema_artifact, pretty=True)

    gate_artifact = {
        "metadata": {
            "artifact_id": f"{ARTIFACT_ID}_gate",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "contract_version": ARTIFACT_ID,
            "primary_outcome": "schema_frozen_review_only",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "positive_inputs": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(scoreboard_gate_path, root),
            "scoreboard_gate_sha256": sha256_file(scoreboard_gate_path),
        },
        "positive_contract_summary": positive_summary,
        "fault_injection_results": fault_results,
        "gate": {
            "gate_pass": True,
            "positive_contract_pass": True,
            "fault_rejection_count": len(fault_results),
            "unexpected_fault_pass_count": 0,
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    write_json(gate_path, gate_artifact, pretty=True)

    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "contract_version": ARTIFACT_ID,
            "primary_outcome": "schema_frozen_review_only",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": (
            "The federated candidate-evidence schema can be locked as review-only "
            "when candidate identity, coordinate state, claim admissibility, and "
            "entry rollups are validated from candidate rows and source-derived "
            "context remains non-predictive."
        ),
        "schema_contract": schema_artifact["schema_contract_lock_v7"],
        "positive_contract_summary": positive_summary,
        "fault_injection_summary": {
            "fault_count": len(fault_results),
            "rejected_fault_count": len(
                [item for item in fault_results if item["rejected"] is True]
            ),
            "faults": fault_results,
        },
        "artifacts": {
            "schema": rel(schema_path, root),
            "schema_sha256": sha256_file(schema_path),
            "gate": rel(gate_path, root),
            "gate_sha256": sha256_file(gate_path),
        },
        "gate": {
            "gate_pass": True,
            "primary_outcome": "schema_frozen_review_only",
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    write_json(report_path, report, pretty=True)
    return {
        "schema": schema_path,
        "gate": gate_path,
        "report": report_path,
    }


def fixture_row(
    *,
    source_lane_id: str,
    candidate_id: str,
    coordinate_state: str,
    expected_claim_status: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "source_lane_id": source_lane_id,
        "source_artifact": f"artifacts/research_lanes/{source_lane_id}/fixture.json",
        "source_row_key": "rows",
        "source_row_id": candidate_id,
        "row_id": f"{source_lane_id}:rows:{candidate_id}",
        "candidate_id": candidate_id,
        "entry_id": "SELF",
        "pdb_id": "SELF",
        "row_role": "schema_contract_fixture",
        "ligand_code_from_structure": "ANP",
        "coordinate_state": coordinate_state,
        "terminal_gamma_equivalent_geometry": coordinate_state == "active_gamma",
        "terminal_gamma_atom_name": "PG",
        "nearest_gamma_acceptor_distance_angstrom": 4.2,
        "local_metal_context": True,
        "catalytic_site_locality": True,
        "source_free_acceptor_role_features": True,
        "source_free_acceptor_role_policy_id": None,
        "same_structure_co_materialization": True,
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": True,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "expected_claim_status": expected_claim_status,
        **{flag: False for flag in FORBIDDEN_ROW_FLAGS},
    }


def policy_result_row(row: dict[str, Any], claim_status: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "row_id": row["row_id"],
        "candidate_id": row["candidate_id"],
        "source_lane_id": row["source_lane_id"],
        "source_artifact": row["source_artifact"],
        "source_row_key": row["source_row_key"],
        "source_row_id": row["source_row_id"],
        "entry_id": row["entry_id"],
        "pdb_id": row["pdb_id"],
        "row_role": row["row_role"],
        "coordinate_state": row["coordinate_state"],
        "claim_status": claim_status,
        "claim_admissibility": "review_only",
        "abstention_reasons": ["self_test_review_only"],
        "forbidden_predictive_context_flags": [],
        "nearest_gamma_acceptor_distance_angstrom": row[
            "nearest_gamma_acceptor_distance_angstrom"
        ],
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }


def self_test() -> None:
    root = Path.cwd()
    row_a = fixture_row(
        source_lane_id="epk_positive_evidence",
        candidate_id="SELF:analog",
        coordinate_state="substrate_acceptor_analog_state",
        expected_claim_status="review_only_abstain_analog_state",
    )
    row_b = fixture_row(
        source_lane_id="epk_substrate_role_identity",
        candidate_id="SELF:product",
        coordinate_state="product_state",
        expected_claim_status="review_only_abstain_product_state",
    )
    tranche = {
        "metadata": {
            "tranche_id": "schema_contract_self_test",
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": 2,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": [row_a, row_b],
    }
    result_rows = [
        policy_result_row(row_a, "review_only_abstain_analog_state"),
        policy_result_row(row_b, "review_only_abstain_product_state"),
    ]
    result = {
        "metadata": {
            "tranche_id": "schema_contract_self_test",
            "policy_version": "self_test",
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": 2,
            "claim_status_counts": count_rows(result_rows, "claim_status"),
            "coordinate_state_counts": count_rows(result_rows, "coordinate_state"),
            "expected_decision_mismatch_count": 0,
            "expected_claim_status_mismatch_count": 0,
            "require_candidate_identity_fields": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
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
        "rows": result_rows,
    }
    result_path = Path("/private/tmp/epk_schema_contract_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(root, [result_path])
    summary = validate_contract_bundle(tranche=tranche, result=result, gate=gate)
    assert summary["scoreboard_gate"]["entry_count"] == 1
    fault_results = run_fault_injections(tranche=tranche, result=result, gate=gate)
    assert all(item["rejected"] is True for item in fault_results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lock the review-only federated ePK candidate schema contract over "
            "candidate identity, claim admissibility, and entry rollups."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_ARTIFACT_DIR,
    )
    parser.add_argument("--tranche", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--scoreboard-gate", type=Path)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    output_dir = args.output_dir
    tranche_path = args.tranche or latest_path(
        output_dir,
        "epk_federated_literal_product_split_entry_precedence_controls_v6_*_tranche.json",
    )
    result_path = args.result or latest_path(
        output_dir,
        "epk_federated_literal_product_split_entry_precedence_controls_v6_*_result.json",
    )
    scoreboard_gate_path = args.scoreboard_gate or latest_path(
        output_dir,
        "epk_federated_literal_product_split_entry_precedence_controls_v6_*_scoreboard_gate.json",
    )
    outputs = build_outputs(
        Path.cwd(),
        output_dir,
        args.timestamp or timestamp(),
        tranche_path=tranche_path,
        result_path=result_path,
        scoreboard_gate_path=scoreboard_gate_path,
    )
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
