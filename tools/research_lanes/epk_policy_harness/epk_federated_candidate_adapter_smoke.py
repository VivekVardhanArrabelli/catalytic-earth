#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from epk_candidate_policy_bridge_scoreboard_gate import (
    build_artifact,
    rel,
    summarize_result,
    write_json,
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
ARTIFACT_ID = "epk_federated_lane_candidate_evidence_adapter_smoke_v1"
DEFAULT_POLICY = Path("artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json")

FEDERATED_INPUT_SPECS = (
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
        "path": "artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json",
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


def load_git_json(ref: str, artifact_path: str) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{ref}:{artifact_path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise ValueError(f"{ref}:{artifact_path} must contain a JSON object")
    return value


def rows_for_keys(payload: dict[str, Any], row_keys: tuple[str, ...]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for row_key in row_keys:
        value = payload.get(row_key, [])
        if not isinstance(value, list):
            raise ValueError(f"row key {row_key} must contain a list")
        rows.extend((row_key, row) for row in value if isinstance(row, dict))
    return rows


def first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def numeric(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 3)
    except (TypeError, ValueError):
        return None


def bool_value(value: Any) -> bool:
    return bool(value is True)


def ligand_from_state(value: Any) -> str | None:
    text = str(value or "")
    if ":" in text:
        ligand = text.rsplit(":", 1)[-1].strip()
        if ligand:
            return ligand
    return None


def normalize_coordinate_state(value: Any) -> str:
    text = str(value or "").strip()
    if text in COORDINATE_STATE_VALUES:
        return text
    lowered = text.lower()
    if lowered in {"transition_analog", "transition_state_analog", "pseudosubstrate"}:
        return "substrate_acceptor_analog_state"
    if lowered in {"product", "product_state"}:
        return "product_state"
    if lowered in {"deposited_atom_site", "biological_assembly", "coordinate_context"}:
        return "active_gamma"
    if not text:
        return "unavailable_coordinate_state"
    return "ambiguous_coordinate_state"


def flag_false_fields() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_ROW_FLAGS}


def with_policy_expectation(row: dict[str, Any]) -> dict[str, Any]:
    coordinate_state = row["coordinate_state"]
    if row.get("sibling_counterfamily_context") is True:
        claim_status = "review_only_abstain_sibling_control"
    elif row.get("split_state_context") is True or coordinate_state == "split_state":
        claim_status = "review_only_abstain_split_state"
    elif (
        row.get("substrate_acceptor_analog_context") is True
        or coordinate_state == "substrate_acceptor_analog_state"
    ):
        claim_status = "review_only_abstain_analog_state"
    elif coordinate_state in {"product_state", "adp_state"}:
        claim_status = "review_only_abstain_product_state"
    elif coordinate_state in {"unavailable_coordinate_state", "ambiguous_coordinate_state"}:
        claim_status = "review_only_abstain_topology_ambiguity"
    elif row.get("candidate_specific_source_repair") is True:
        claim_status = "review_only_abstain_forbidden_context"
    else:
        claim_status = "review_only_abstain_missing_role_policy"
    row["expected_frozen_policy_decision"] = "review_only_abstain"
    row["expected_claim_status"] = claim_status
    return row


def base_row(
    *,
    source_lane_id: str,
    source_artifact: str,
    source_row_key: str,
    source_row_id: str,
    candidate_id: str,
    pdb_id: str | None,
    row_role: str,
    coordinate_state: str,
    ligand_code: str | None,
    terminal_gamma_atom_name: str | None,
    nearest_distance: float | None,
    local_metal_context: bool,
    terminal_gamma_equivalent_geometry: bool,
    catalytic_site_locality: bool,
    source_free_acceptor_role_features: bool,
    same_structure_co_materialization: bool,
) -> dict[str, Any]:
    row = {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "source_lane_id": source_lane_id,
        "source_artifact": source_artifact,
        "source_row_key": source_row_key,
        "source_row_id": source_row_id,
        "row_id": f"{source_lane_id}:{source_row_key}:{source_row_id}",
        "candidate_id": candidate_id,
        "pdb_id": pdb_id,
        "row_role": row_role,
        "ligand_code_from_structure": ligand_code,
        "coordinate_state": coordinate_state,
        "terminal_gamma_equivalent_geometry": terminal_gamma_equivalent_geometry,
        "terminal_gamma_atom_name": terminal_gamma_atom_name,
        "nearest_gamma_acceptor_distance_angstrom": nearest_distance,
        "local_metal_context": local_metal_context,
        "catalytic_site_locality": catalytic_site_locality,
        "source_free_acceptor_role_features": source_free_acceptor_role_features,
        "source_free_acceptor_role_policy_id": None,
        "same_structure_co_materialization": same_structure_co_materialization,
        "coordinate_ligand_materialized_from_structure": ligand_code is not None,
        "coordinate_ligand_code_source": "lane_adapter_compact_source_free_fields",
        "query_ligand_synonym_used_as_coordinate_ligand": False,
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": True,
        "source_review_status": "review_only_context_not_predictive",
        "source_validation_status": "review_only_context_not_predictive",
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }
    row.update(flag_false_fields())
    return with_policy_expectation(row)


def adapt_positive_evidence(
    row: dict[str, Any], *, source_artifact: str, source_row_key: str, index: int
) -> dict[str, Any]:
    geometry = row.get("source_free_geometry") or {}
    coordinate_state = normalize_coordinate_state(
        first_present(row.get("coordinate_state"), geometry.get("coordinate_state"))
    )
    ligand_code = first_present(
        geometry.get("terminal_ligand_code"),
        ligand_from_state(geometry.get("ligand_state")),
    )
    distance = numeric(geometry.get("nearest_terminal_distance_angstrom"))
    terminal_atom = geometry.get("terminal_atom_name")
    candidate_id = str(row.get("candidate_id") or f"{row.get('pdb_id', 'unknown')}:{index}")
    terminal_geometry = terminal_atom == "PG" and coordinate_state == "active_gamma"
    same_structure = bool(distance is not None and geometry.get("candidate_atom_name"))
    adapted = base_row(
        source_lane_id="epk_positive_evidence",
        source_artifact=source_artifact,
        source_row_key=source_row_key,
        source_row_id=candidate_id,
        candidate_id=candidate_id,
        pdb_id=row.get("pdb_id"),
        row_role="federated_adapter_positive_source_adjudication",
        coordinate_state=coordinate_state,
        ligand_code=ligand_code,
        terminal_gamma_atom_name=terminal_atom,
        nearest_distance=distance,
        local_metal_context=bool_value(geometry.get("has_local_mg_or_mn")),
        terminal_gamma_equivalent_geometry=terminal_geometry,
        catalytic_site_locality=bool(distance is not None and distance <= 6.0),
        source_free_acceptor_role_features=bool(geometry.get("candidate_residue_code")),
        same_structure_co_materialization=same_structure,
    )
    if coordinate_state == "substrate_acceptor_analog_state":
        adapted["substrate_acceptor_analog_context"] = True
    return with_policy_expectation(adapted)


def adapt_substrate_role_identity(
    row: dict[str, Any], *, source_artifact: str, source_row_key: str, index: int
) -> dict[str, Any]:
    evidence = row.get("source_free_evidence") or {}
    terminal = evidence.get("terminal_gamma_atom") or {}
    acceptor = evidence.get("acceptor_atom") or {}
    coordinate_state = normalize_coordinate_state(evidence.get("coordinate_state"))
    ligand_code = first_present(
        terminal.get("residue_code"),
        ligand_from_state(evidence.get("ligand_state")),
    )
    distance = numeric(
        first_present(
            evidence.get("distance_angstrom"),
            evidence.get("nearest_protein_hydroxyl_distance_angstrom"),
        )
    )
    blocker = str(evidence.get("blocker_class") or "")
    candidate_role = str(evidence.get("candidate_role_class") or "")
    source_row_id = str(row.get("candidate_id") or f"{row.get('pdb_id', 'unknown')}:{index}")
    adapted = base_row(
        source_lane_id="epk_substrate_role_identity",
        source_artifact=source_artifact,
        source_row_key=source_row_key,
        source_row_id=source_row_id,
        candidate_id=source_row_id,
        pdb_id=row.get("pdb_id"),
        row_role="federated_adapter_substrate_role_identity",
        coordinate_state=coordinate_state,
        ligand_code=ligand_code,
        terminal_gamma_atom_name=terminal.get("atom_name"),
        nearest_distance=distance,
        local_metal_context=False,
        terminal_gamma_equivalent_geometry=bool_value(
            evidence.get("terminal_gamma_equivalent_atom_available")
        ),
        catalytic_site_locality=bool(distance is not None and distance <= 6.0),
        source_free_acceptor_role_features=bool(
            acceptor.get("residue_code") or candidate_role
        ),
        same_structure_co_materialization=bool(distance is not None),
    )
    if coordinate_state == "adp_state" or blocker == "product_state_evidence":
        adapted["product_state_context"] = True
    if "topology" in blocker or evidence.get("same_chain_topology") is True:
        adapted["topology_ambiguity_status"] = "source_free_topology_blocker_review_only"
    if blocker == "internal_fragment_mimicry":
        adapted["sibling_counterfamily_context"] = True
        adapted["sibling_control_match_status"] = "internal_fragment_control_review_only"
    return with_policy_expectation(adapted)


def adapt_false_positive_hunter(
    row: dict[str, Any], *, source_artifact: str, source_row_key: str, index: int
) -> dict[str, Any]:
    candidate = row.get("candidate") or {}
    ligand_code = candidate.get("gamma_ligand_code")
    distance = numeric(candidate.get("nearest_gamma_distance_angstrom"))
    control_class = str(row.get("control_class") or "")
    guard_blocker = str(row.get("guard_blocker_class") or "")
    source_row_id = str(
        row.get("fixture_id")
        or f"{row.get('pdb_id', 'unknown')}:{row.get('coordinate_context', 'context')}:{index}"
    )
    local_metal_distance = numeric(candidate.get("nearest_mg_distance_angstrom"))
    adapted = base_row(
        source_lane_id="epk_false_positive_hunter",
        source_artifact=source_artifact,
        source_row_key=source_row_key,
        source_row_id=source_row_id,
        candidate_id=source_row_id,
        pdb_id=row.get("pdb_id"),
        row_role=f"federated_adapter_false_positive_control:{control_class}",
        coordinate_state="active_gamma" if ligand_code else "unavailable_coordinate_state",
        ligand_code=ligand_code,
        terminal_gamma_atom_name=candidate.get("gamma_atom_name"),
        nearest_distance=distance,
        local_metal_context=bool(local_metal_distance is not None and local_metal_distance <= 4.0),
        terminal_gamma_equivalent_geometry=bool(candidate.get("gamma_atom_name") == "PG"),
        catalytic_site_locality=bool(distance is not None and distance <= 6.0),
        source_free_acceptor_role_features=bool_value(
            row.get("observed_materializer_nonabstention")
        ),
        same_structure_co_materialization=bool_value(
            row.get("observed_materializer_nonabstention")
        ),
    )
    if row.get("non_epk_control") is True or any(
        token in control_class
        for token in ("atpase", "transporter", "orc", "mcm", "internal_fragment")
    ):
        adapted["sibling_counterfamily_context"] = True
        adapted["sibling_control_match_status"] = "false_positive_control_review_only"
    if "topology" in guard_blocker or row.get("same_chain_topology_detected") is True:
        adapted["topology_ambiguity_status"] = guard_blocker or "topology_control"
    return with_policy_expectation(adapted)


def adapt_sibling_controls(
    row: dict[str, Any], *, source_artifact: str, source_row_key: str, index: int
) -> dict[str, Any]:
    features = row.get("input_features") or {}
    expected = row.get("expected_review_only_result") or {}
    source_row_id = str(row.get("case_id") or f"{row.get('pdb_id', 'unknown')}:{index}")
    if source_row_key.startswith("product_"):
        ligand_code = first_present(
            (features.get("product_or_partial_nucleotide_codes") or [None])[0],
            "ADP",
        )
        distance = numeric(
            first_present(
                features.get("nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom"),
                features.get("nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom"),
            )
        )
        coordinate_state = "product_state"
        terminal_atom = None
        terminal_geometry = False
        row_role = "federated_adapter_sibling_product_control"
    else:
        ligand_code = (features.get("gamma_capable_nucleotide_codes") or [None])[0]
        distance = numeric(features.get("nearest_gamma_to_protein_hydroxyl_distance_angstrom"))
        coordinate_state = "active_gamma"
        terminal_atom = "PG" if ligand_code else None
        terminal_geometry = ligand_code is not None
        row_role = "federated_adapter_sibling_gamma_control"

    adapted = base_row(
        source_lane_id="epk_sibling_controls",
        source_artifact=source_artifact,
        source_row_key=source_row_key,
        source_row_id=source_row_id,
        candidate_id=source_row_id,
        pdb_id=row.get("pdb_id"),
        row_role=row_role,
        coordinate_state=coordinate_state,
        ligand_code=ligand_code,
        terminal_gamma_atom_name=terminal_atom,
        nearest_distance=distance,
        local_metal_context=bool(features.get("metal_ligand_codes")),
        terminal_gamma_equivalent_geometry=terminal_geometry,
        catalytic_site_locality=bool(distance is not None and distance <= 6.0),
        source_free_acceptor_role_features=bool(
            expected.get("should_block_weak_rule_hit")
            or expected.get("should_block_weak_product_rule_hit")
        ),
        same_structure_co_materialization=bool(distance is not None),
    )
    adapted["sibling_counterfamily_context"] = True
    adapted["sibling_control_match_status"] = "sibling_counteraxis_control_review_only"
    if coordinate_state == "product_state":
        adapted["product_state_context"] = True
    return with_policy_expectation(adapted)


ADAPTERS: dict[str, Callable[..., dict[str, Any]]] = {
    "epk_positive_evidence": adapt_positive_evidence,
    "epk_substrate_role_identity": adapt_substrate_role_identity,
    "epk_false_positive_hunter": adapt_false_positive_hunter,
    "epk_sibling_controls": adapt_sibling_controls,
}


def select_rows(
    lane_id: str, row_items: list[tuple[str, dict[str, Any]]]
) -> list[tuple[str, dict[str, Any]]]:
    selected: list[tuple[str, dict[str, Any]]] = []
    seen: set[int] = set()

    def take(predicate: Callable[[str, dict[str, Any]], bool]) -> None:
        for index, (row_key, row) in enumerate(row_items):
            if index in seen:
                continue
            if predicate(row_key, row):
                seen.add(index)
                selected.append((row_key, row))
                return

    if lane_id == "epk_positive_evidence":
        take(
            lambda _key, row: row.get("coordinate_state") == "active_gamma"
            and bool((row.get("source_free_geometry") or {}).get("has_local_mg_or_mn"))
        )
        take(lambda _key, row: str(row.get("coordinate_state")) == "transition_analog")
        take(
            lambda _key, row: "no_local_metal"
            in " ".join(row.get("original_blockers") or [])
        )
    elif lane_id == "epk_substrate_role_identity":
        take(
            lambda key, row: key == "candidate_evidence_rows"
            and (row.get("source_free_evidence") or {}).get("blocker_class") == "none"
        )
        take(
            lambda key, row: key == "candidate_evidence_rows"
            and "topology" in str((row.get("source_free_evidence") or {}).get("blocker_class"))
        )
        take(lambda key, row: key == "state_only_rows")
    elif lane_id == "epk_false_positive_hunter":
        take(lambda _key, row: "atpase" in str(row.get("control_class") or ""))
        take(lambda _key, row: "orc_mcm" in str(row.get("control_class") or ""))
        take(lambda _key, row: "internal_fragment" in str(row.get("control_class") or ""))
    elif lane_id == "epk_sibling_controls":
        take(
            lambda key, row: key == "gamma_proximity_counteraxis_cases"
            and (row.get("expected_review_only_result") or {}).get(
                "should_block_weak_rule_hit"
            )
            is True
        )
        take(lambda key, _row: key == "product_phosphoryl_identity_counteraxis_cases")
    if not selected and row_items:
        selected.append(row_items[0])
    return selected


def build_tranche_from_payloads(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]]
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    input_summaries: list[dict[str, Any]] = []
    for spec, payload in payloads:
        lane_id = spec["lane_id"]
        adapter = ADAPTERS[lane_id]
        row_items = rows_for_keys(payload, tuple(spec["row_keys"]))
        selected = select_rows(lane_id, row_items)
        input_summaries.append(
            {
                "lane_id": lane_id,
                "ref": spec.get("ref"),
                "artifact": spec["path"],
                "row_keys": list(spec["row_keys"]),
                "available_row_count": len(row_items),
                "selected_row_count": len(selected),
                "review_only_input": True,
            }
        )
        for index, (row_key, row) in enumerate(selected):
            rows.append(
                adapter(
                    row,
                    source_artifact=spec["path"],
                    source_row_key=row_key,
                    index=index,
                )
            )

    selected_lanes = sorted({row["source_lane_id"] for row in rows})
    if len(selected_lanes) < 2:
        raise ValueError("federated adapter smoke requires at least two source lanes")
    return {
        "metadata": {
            "tranche_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "lane_id": LANE_ID,
            "review_only": True,
            "schema_version": SCHEMA_VERSION,
            "row_count": len(rows),
            "source_lane_count": len(selected_lanes),
            "source_lanes": selected_lanes,
            "input_summaries": input_summaries,
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
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": rows,
    }


def write_validation_rejection(
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
        error_message = str(error)
    else:
        raise AssertionError(f"{expected_failure} fault must fail validation")

    rejected = expected_error_fragment in error_message
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
        "observed_error": error_message,
    }
    write_json(path, payload, pretty=True)
    if not rejected:
        raise ValueError(
            f"{expected_failure} rejected with unexpected error: {error_message}"
        )
    return {
        "artifact": rel(path, root),
        "sha256": sha256_file(path),
        "expected_failure": expected_failure,
        "rejected": rejected,
        "observed_error": error_message,
    }


def build_outputs(root: Path, output_dir: Path, run_stamp: str, policy_path: Path) -> dict[str, Path]:
    payloads = [
        (dict(spec), load_git_json(str(spec["ref"]), str(spec["path"])))
        for spec in FEDERATED_INPUT_SPECS
    ]
    policy = load_json(policy_path)
    tranche = build_tranche_from_payloads(payloads)
    result = evaluate_tranche(policy, tranche)
    if result["metadata"]["expected_claim_status_mismatch_count"]:
        raise ValueError("adapter smoke produced unexpected claim-status mismatch")
    stem = f"{ARTIFACT_ID}_{run_stamp}"
    tranche_path = output_dir / f"{stem}_tranche.json"
    result_path = output_dir / f"{stem}_result.json"
    gate_path = output_dir / f"{stem}_scoreboard_gate.json"
    negative_identity_path = (
        output_dir / f"{stem}_negative_missing_candidate_identity_result.json"
    )
    negative_duplicate_path = (
        output_dir / f"{stem}_negative_duplicate_candidate_identity_result.json"
    )
    negative_source_copy_path = (
        output_dir / f"{stem}_negative_source_context_copy_result.json"
    )
    report_path = output_dir / f"{stem}.json"

    write_json(tranche_path, tranche, pretty=True)
    write_json(result_path, result, pretty=True)
    gate = build_artifact(root, [result_path])
    if gate["gate"]["gate_pass"] is not True:
        raise ValueError("federated adapter smoke scoreboard gate must pass")
    write_json(gate_path, gate, pretty=True)

    negative_identity = json.loads(json.dumps(result))
    negative_identity["metadata"]["fault_injection_expected_failure"] = (
        "missing_candidate_identity"
    )
    negative_identity["metadata"]["row_count"] = 1
    negative_identity["rows"] = [negative_identity["rows"][0]]
    negative_row = negative_identity["rows"][0]
    negative_identity["metadata"]["decision_counts"] = {
        negative_row["decision"]: 1,
    }
    negative_identity["metadata"]["claim_status_counts"] = {
        negative_row["claim_status"]: 1,
    }
    negative_identity["metadata"]["coordinate_state_counts"] = {
        negative_row["coordinate_state"]: 1,
    }
    negative_identity["rows"][0].pop("candidate_id", None)
    negative_identity["rows"][0].pop("source_lane_id", None)
    negative_identity["rows"][0].pop("source_artifact", None)
    write_json(negative_identity_path, negative_identity, pretty=True)
    negative_identity_summary = summarize_result(root, negative_identity_path, negative_identity)
    if negative_identity_summary["gate_pass"] is not False:
        raise ValueError("missing candidate identity fault must fail the scoreboard gate")

    negative_duplicate_tranche = json.loads(json.dumps(tranche))
    negative_duplicate_tranche["rows"][1]["candidate_id"] = negative_duplicate_tranche[
        "rows"
    ][0]["candidate_id"]
    negative_duplicate_tranche["rows"][1]["source_row_id"] = negative_duplicate_tranche[
        "rows"
    ][0]["source_row_id"]
    negative_duplicate_rejection = write_validation_rejection(
        root,
        negative_duplicate_path,
        expected_failure="duplicate_candidate_identity",
        expected_error_fragment="candidate_id must be unique within each source lane",
        action=lambda: evaluate_tranche(policy, negative_duplicate_tranche),
    )

    negative_source_copy_tranche = json.loads(json.dumps(tranche))
    negative_source_copy_tranche["rows"][0]["protein_names"] = [
        "copied source-side protein name"
    ]
    negative_source_copy_rejection = write_validation_rejection(
        root,
        negative_source_copy_path,
        expected_failure="source_context_copy",
        expected_error_fragment="must not be copied",
        action=lambda: evaluate_tranche(policy, negative_source_copy_tranche),
    )

    source_lane_counts: dict[str, int] = {}
    for row in tranche["rows"]:
        source_lane = row["source_lane_id"]
        source_lane_counts[source_lane] = source_lane_counts.get(source_lane, 0) + 1
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
            "Independent ePK lanes can emit compact candidate rows that map into "
            "the shared candidate-evidence schema, while source review remains "
            "review-only and claim admissibility remains governed by the policy bridge."
        ),
        "federated_inputs": tranche["metadata"]["input_summaries"],
        "adapter_summary": {
            "adapted_row_count": len(tranche["rows"]),
            "source_lane_count": len(source_lane_counts),
            "source_lane_counts": source_lane_counts,
            "candidate_identity_required": True,
            "candidate_identity_unique_per_source_lane": True,
            "row_id_unique": True,
            "federated_contract_validated_by_policy_harness": True,
            "entry_status_derived_from_candidate_decisions": True,
            "source_text_and_protein_names_copied": False,
            "discovery_signal_separate_from_claim_admissibility": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "summary": {
            "rows_reviewed": result["metadata"]["row_count"],
            "source_lane_count": len(source_lane_counts),
            "source_lane_counts": source_lane_counts,
            "entry_count": gate["scoreboard_summary"]["entry_count"],
            "claim_status_counts": result["metadata"]["claim_status_counts"],
            "entry_claim_status_counts": gate["scoreboard_summary"][
                "entry_claim_status_counts"
            ],
            "coordinate_state_counts": result["metadata"]["coordinate_state_counts"],
            "scoreboard_gate_pass": gate["gate"]["gate_pass"],
            "negative_fault_injection_count": 3,
        },
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
            "entry_rollup_contract": (
                gate["scoreboard_rows"][0]["entry_rollup_contract"]
                if gate["scoreboard_rows"]
                else {}
            ),
            "summary": gate["scoreboard_summary"],
        },
        "negative_fault_injections": [
            {
                "artifact": rel(negative_identity_path, root),
                "sha256": sha256_file(negative_identity_path),
                "expected_failure": "missing_candidate_identity",
                "rejected": negative_identity_summary["gate_pass"] is False,
                "missing_schema_row_count": negative_identity_summary[
                    "missing_schema_row_count"
                ],
                "missing_schema_details": negative_identity_summary[
                    "missing_schema_details"
                ],
            },
            negative_duplicate_rejection,
            negative_source_copy_rejection,
        ],
        "gate": {
            "gate_pass": gate["gate"]["gate_pass"],
            "progress_claim_allowed": False,
            "production_claim_allowed": False,
        },
        "artifacts": {
            "tranche": rel(tranche_path, root),
            "tranche_sha256": sha256_file(tranche_path),
            "result": rel(result_path, root),
            "result_sha256": sha256_file(result_path),
            "scoreboard_gate": rel(gate_path, root),
            "scoreboard_gate_sha256": sha256_file(gate_path),
            "negative_missing_candidate_identity": rel(negative_identity_path, root),
            "negative_missing_candidate_identity_sha256": sha256_file(
                negative_identity_path
            ),
            "negative_duplicate_candidate_identity": rel(negative_duplicate_path, root),
            "negative_duplicate_candidate_identity_sha256": sha256_file(
                negative_duplicate_path
            ),
            "negative_source_context_copy": rel(negative_source_copy_path, root),
            "negative_source_context_copy_sha256": sha256_file(
                negative_source_copy_path
            ),
        },
    }
    write_json(report_path, report, pretty=True)
    return {
        "tranche": tranche_path,
        "result": result_path,
        "scoreboard_gate": gate_path,
        "negative_missing_candidate_identity": negative_identity_path,
        "negative_duplicate_candidate_identity": negative_duplicate_path,
        "negative_source_context_copy": negative_source_copy_path,
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
                        "candidate_id": "P:1",
                        "pdb_id": "P001",
                        "coordinate_state": "active_gamma",
                        "source_free_geometry": {
                            "terminal_ligand_code": "ATP",
                            "terminal_atom_name": "PG",
                            "nearest_terminal_distance_angstrom": 3.2,
                            "has_local_mg_or_mn": True,
                            "candidate_residue_code": "SER",
                        },
                    }
                ]
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
                        "case_id": "gamma::control::1",
                        "pdb_id": "C001",
                        "input_features": {
                            "gamma_capable_nucleotide_codes": ["ANP"],
                            "nearest_gamma_to_protein_hydroxyl_distance_angstrom": 4.1,
                            "metal_ligand_codes": ["MG"],
                        },
                        "expected_review_only_result": {
                            "should_block_weak_rule_hit": True
                        },
                    }
                ]
            },
        ),
    ]
    tranche = build_tranche_from_payloads(payloads)
    result = evaluate_tranche(policy, tranche)
    result_path = Path("/private/tmp/epk_federated_adapter_smoke_self_test_result.json")
    write_json(result_path, result, pretty=False)
    gate = build_artifact(root, [result_path])
    assert gate["gate"]["gate_pass"] is True
    assert result["metadata"]["require_candidate_identity_fields"] is True
    assert result["metadata"]["claim_status_counts"] == {
        "review_only_abstain_missing_role_policy": 1,
        "review_only_abstain_sibling_control": 1,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Adapt compact review-only rows from independent ePK lanes into the "
            "candidate-level policy bridge schema and build a scoreboard gate."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_policy_harness"),
    )
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    run_stamp = args.timestamp or timestamp()
    outputs = build_outputs(Path.cwd(), args.output_dir, run_stamp, args.policy)
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
