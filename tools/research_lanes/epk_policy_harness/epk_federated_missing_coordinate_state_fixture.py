#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epk_candidate_policy_bridge_scoreboard_gate import build_artifact, rel, write_json
from epk_federated_schema_contract_lock import (
    run_fault_injections,
    validate_contract_bundle,
)
from epk_policy_harness import (
    COORDINATE_STATE_VALUES,
    FORBIDDEN_ROW_FLAGS,
    REVIEW_ONLY_BLOCKER_FEATURES,
    REVIEW_ONLY_LIGAND_CONTEXTS,
    SCHEMA_VERSION,
    evaluate_tranche,
    sha256_file,
    utc_now,
)


LANE_ID = "epk_policy_harness"
ARTIFACT_ID = "epk_federated_schema_contract_missing_coordinate_state_fixture_v8"
DEFAULT_ARTIFACT_DIR = Path("artifacts/research_lanes/epk_policy_harness")
FIXTURE_POLICY_VERSION = (
    "epk_missing_coordinate_state_fixture_v8_review_only_not_production_20260521"
)
ACCEPTED_ROLE_POLICY_ID = "role_policy_v0_review_only_missing_state_fixture"
MISSING_FROM_V7_SOURCE_BUNDLE = (
    "adp_state",
    "ligand_absent",
    "metal_absent",
    "unavailable_coordinate_state",
)
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


def count_values(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field) or "") for row in rows).items()))


def fixture_policy() -> dict[str, Any]:
    return {
        "metadata": {
            "policy_version": FIXTURE_POLICY_VERSION,
            "policy_id": "epk_missing_coordinate_state_fixture_v8",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "threshold_calibrated": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "coordinate_state_fixture_not_production_policy": True,
        },
        "hypothesis": (
            "Coordinate states absent from the v7 positive source bundle can be "
            "accepted as review-only candidate evidence only when source provenance, "
            "claim admissibility, and entry rollups remain under the same fail-closed "
            "schema contract."
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
                "synthetic v8 coordinate-state fixture only; not a production role policy"
            ),
        },
        "allowed_predictive_features": ALLOWED_PREDICTIVE_FEATURES,
        "review_only_features": sorted(REVIEW_ONLY_BLOCKER_FEATURES),
        "forbidden_features": sorted(FORBIDDEN_ROW_FLAGS),
        "review_only_ligand_contexts": sorted(REVIEW_ONLY_LIGAND_CONTEXTS),
    }


def fixture_row(
    *,
    source_lane_id: str,
    entry_id: str,
    candidate_suffix: str,
    coordinate_state: str,
    expected_claim_status: str,
    ligand_code_from_structure: str | None,
    ligand_context: str | None = None,
    terminal_gamma_equivalent_geometry: bool = False,
    terminal_gamma_atom_name: str | None = None,
    nearest_gamma_acceptor_distance_angstrom: float | None = None,
    local_metal_context: bool = True,
    catalytic_site_locality: bool = True,
    source_free_acceptor_role_features: bool = True,
    same_structure_co_materialization: bool = True,
    coordinate_ligand_materialized_from_structure: bool = True,
    product_state_context: bool = False,
    substrate_acceptor_analog_context: bool = False,
    topology_ambiguity_status: str | None = None,
) -> dict[str, Any]:
    candidate_id = f"{entry_id}:{candidate_suffix}"
    return {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "source_lane_id": source_lane_id,
        "source_artifact": (
            f"artifacts/research_lanes/{source_lane_id}/"
            "compact_candidate_fixture.json"
        ),
        "source_row_key": "rows",
        "source_row_id": candidate_id,
        "row_id": f"{source_lane_id}:v8:{candidate_id}",
        "candidate_id": candidate_id,
        "entry_id": entry_id,
        "pdb_id": entry_id,
        "row_role": "v8_missing_coordinate_state_review_only_fixture",
        "ligand_code_from_structure": ligand_code_from_structure,
        "ligand_context": ligand_context,
        "coordinate_state": coordinate_state,
        "terminal_gamma_equivalent_geometry": terminal_gamma_equivalent_geometry,
        "terminal_gamma_atom_name": terminal_gamma_atom_name,
        "nearest_gamma_acceptor_distance_angstrom": (
            nearest_gamma_acceptor_distance_angstrom
        ),
        "local_metal_context": local_metal_context,
        "catalytic_site_locality": catalytic_site_locality,
        "source_free_acceptor_role_features": source_free_acceptor_role_features,
        "source_free_acceptor_role_policy_id": (
            ACCEPTED_ROLE_POLICY_ID if source_free_acceptor_role_features else None
        ),
        "same_structure_co_materialization": same_structure_co_materialization,
        "coordinate_ligand_materialized_from_structure": (
            coordinate_ligand_materialized_from_structure
        ),
        "coordinate_ligand_code_source": (
            "mmcif_atom_site_auth_or_label_comp_id"
            if coordinate_ligand_materialized_from_structure
            else None
        ),
        "query_ligand_synonym_used_as_coordinate_ligand": False,
        "product_state_context": product_state_context,
        "substrate_acceptor_analog_context": substrate_acceptor_analog_context,
        "topology_ambiguity_status": topology_ambiguity_status,
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": True,
        "expected_frozen_policy_decision": "review_only_abstain",
        "expected_claim_status": expected_claim_status,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        **{flag: False for flag in FORBIDDEN_ROW_FLAGS},
    }


def fixture_rows() -> list[dict[str, Any]]:
    rows = [
        fixture_row(
            source_lane_id="epk_positive_evidence",
            entry_id="V8ADP",
            candidate_suffix="adp_product_state",
            coordinate_state="adp_state",
            ligand_code_from_structure="ADP",
            ligand_context="ADP",
            terminal_gamma_atom_name=None,
            nearest_gamma_acceptor_distance_angstrom=4.0,
            expected_claim_status="review_only_abstain_product_state",
        ),
        fixture_row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="V8ABS",
            candidate_suffix="ligand_absent",
            coordinate_state="ligand_absent",
            ligand_code_from_structure=None,
            ligand_context=None,
            coordinate_ligand_materialized_from_structure=False,
            same_structure_co_materialization=False,
            expected_claim_status="review_only_abstain_missing_role_policy",
        ),
        fixture_row(
            source_lane_id="epk_false_positive_hunter",
            entry_id="V8MET",
            candidate_suffix="metal_absent",
            coordinate_state="metal_absent",
            ligand_code_from_structure="ATP",
            terminal_gamma_equivalent_geometry=True,
            terminal_gamma_atom_name="PG",
            nearest_gamma_acceptor_distance_angstrom=3.4,
            local_metal_context=False,
            expected_claim_status="review_only_abstain_missing_role_policy",
        ),
        fixture_row(
            source_lane_id="epk_state_diversity",
            entry_id="V8UNV",
            candidate_suffix="unavailable_coordinate_state",
            coordinate_state="unavailable_coordinate_state",
            ligand_code_from_structure=None,
            coordinate_ligand_materialized_from_structure=False,
            same_structure_co_materialization=False,
            topology_ambiguity_status="coordinate_state_unavailable_fixture",
            expected_claim_status="review_only_abstain_topology_ambiguity",
        ),
        fixture_row(
            source_lane_id="epk_positive_evidence",
            entry_id="V8PRE",
            candidate_suffix="product_anchor",
            coordinate_state="product_state",
            ligand_code_from_structure="ADP",
            ligand_context="PRODUCT_STATE",
            nearest_gamma_acceptor_distance_angstrom=4.3,
            product_state_context=True,
            expected_claim_status="review_only_abstain_product_state",
        ),
        fixture_row(
            source_lane_id="epk_substrate_role_identity",
            entry_id="V8PRE",
            candidate_suffix="analog_anchor",
            coordinate_state="substrate_acceptor_analog_state",
            ligand_code_from_structure="ANP",
            ligand_context="SUBSTRATE_ACCEPTOR_ANALOG",
            terminal_gamma_equivalent_geometry=True,
            terminal_gamma_atom_name="PG",
            nearest_gamma_acceptor_distance_angstrom=3.9,
            substrate_acceptor_analog_context=True,
            expected_claim_status="review_only_abstain_analog_state",
        ),
    ]
    return rows


def fixture_tranche() -> dict[str, Any]:
    rows = fixture_rows()
    return {
        "metadata": {
            "tranche_id": f"{ARTIFACT_ID}_positive_tranche",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": len(rows),
            "require_candidate_identity_fields": True,
            "synthetic_fixture": True,
            "coordinate_state_fixture_not_production_policy": True,
            "states_missing_from_v7_source_bundle": list(
                MISSING_FROM_V7_SOURCE_BUNDLE
            ),
            "positive_coordinate_state_counts": count_values(rows, "coordinate_state"),
            "source_text_protein_titles_ec_rhea_paper_metadata_copied": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "rows": rows,
    }


def assert_positive_result(result: dict[str, Any]) -> None:
    metadata = result["metadata"]
    if metadata["primary_outcome"] != "policy_frozen_review_only":
        raise ValueError("v8 missing-coordinate fixture must remain policy_frozen_review_only")
    if metadata["expected_claim_status_mismatch_count"] != 0:
        raise ValueError("v8 missing-coordinate fixture has claim-status mismatches")
    if metadata["expected_decision_mismatch_count"] != 0:
        raise ValueError("v8 missing-coordinate fixture has decision mismatches")
    state_counts = metadata["coordinate_state_counts"]
    missing = sorted(set(MISSING_FROM_V7_SOURCE_BUNDLE) - set(state_counts))
    if missing:
        raise ValueError(f"v8 fixture failed to cover missing coordinate states: {missing}")
    if not set(state_counts).issubset(COORDINATE_STATE_VALUES):
        raise ValueError(f"v8 fixture emitted invalid coordinate states: {state_counts}")


def build_outputs(root: Path, output_dir: Path, run_stamp: str) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    policy = fixture_policy()
    tranche = fixture_tranche()
    result = evaluate_tranche(policy, tranche)
    assert_positive_result(result)

    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    scoreboard_gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    contract_gate_path = output_dir / f"{stem}_contract_gate.json"
    report_path = output_dir / f"{stem}.json"

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)

    scoreboard_gate = build_artifact(root, [result_path])
    if scoreboard_gate["gate"]["gate_pass"] is not True:
        raise ValueError("v8 missing-coordinate scoreboard gate must pass")
    write_json(scoreboard_gate_path, scoreboard_gate, pretty=True)

    contract_summary = validate_contract_bundle(
        tranche=tranche,
        result=result,
        gate=scoreboard_gate,
    )
    fault_results = run_fault_injections(
        tranche=tranche,
        result=result,
        gate=scoreboard_gate,
    )
    unexpected_fault_passes = [
        fault["fault"] for fault in fault_results if fault["rejected"] is not True
    ]
    if unexpected_fault_passes:
        raise ValueError(
            f"v8 contract fault injections passed unexpectedly: {unexpected_fault_passes}"
        )

    contract_gate = {
        "metadata": {
            "artifact_id": f"{ARTIFACT_ID}_contract_gate",
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "fixture_version": ARTIFACT_ID,
            "primary_outcome": "scoreboard_gate_created",
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
        "positive_contract_summary": contract_summary,
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
    write_json(contract_gate_path, contract_gate, pretty=True)

    report = {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "policy_version": FIXTURE_POLICY_VERSION,
            "primary_outcome": "scoreboard_gate_created",
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_dump_written": False,
        },
        "hypothesis": policy["hypothesis"],
        "positive_fixture": {
            "tranche_artifact": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result_artifact": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate_artifact": rel(scoreboard_gate_path, root),
            "scoreboard_gate_sha256": sha256_file(scoreboard_gate_path),
            "contract_gate_artifact": rel(contract_gate_path, root),
            "contract_gate_sha256": sha256_file(contract_gate_path),
            "rows_reviewed": result["metadata"]["row_count"],
            "entry_count": scoreboard_gate["scoreboard_summary"]["entry_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "entry_claim_status_counts": scoreboard_gate["scoreboard_summary"][
                "entry_claim_status_counts"
            ],
            "discovery_signal_row_count": scoreboard_gate["scoreboard_summary"][
                "discovery_signal_row_count"
            ],
            "covered_missing_v7_coordinate_states": sorted(
                set(MISSING_FROM_V7_SOURCE_BUNDLE)
                & set(result["metadata"]["coordinate_state_counts"])
            ),
            "source_lane_count": contract_summary["policy_result"][
                "source_lane_count"
            ],
        },
        "schema_refinement": {
            "coordinate_state_field_rules_locked": True,
            "ligand_absent_ligand_code_from_structure": "field_present_may_be_null",
            "unavailable_coordinate_state_ligand_code_from_structure": (
                "field_present_may_be_null"
            ),
            "metal_absent_local_metal_context": False,
            "adp_state_claim_status": "review_only_abstain_product_state",
        },
        "contract_summary": contract_summary,
        "fault_injection_summary": {
            "schema_contract_faults_rejected": fault_results,
        },
        "gate": {
            "gate_pass": True,
            "primary_outcome": "scoreboard_gate_created",
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
    }
    write_json(report_path, report, pretty=True)

    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": scoreboard_gate_path,
        "contract_gate": contract_gate_path,
        "report": report_path,
    }


def self_test() -> None:
    root = Path.cwd()
    output_dir = Path("/private/tmp/epk_missing_coordinate_state_fixture_self_test")
    outputs = build_outputs(root, output_dir, "selftest")
    report = json.loads(outputs["report"].read_text(encoding="utf-8"))
    covered = set(report["positive_fixture"]["covered_missing_v7_coordinate_states"])
    assert covered == set(MISSING_FROM_V7_SOURCE_BUNDLE)
    assert report["gate"]["gate_pass"] is True
    assert report["schema_refinement"]["coordinate_state_field_rules_locked"] is True
    assert all(
        fault["rejected"] is True
        for fault in report["fault_injection_summary"][
            "schema_contract_faults_rejected"
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a compact review-only v8 fixture for coordinate states "
            "missing from the v7 positive source bundle."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_ARTIFACT_DIR,
    )
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
    )
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
