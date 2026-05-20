#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REVIEW_ONLY_LIGAND_CONTEXTS = {
    "ADP",
    "PRODUCT_STATE",
    "SUBSTRATE_ACCEPTOR_ANALOG",
    "SPLIT_STATE",
    "POST_HOC_REPAIR",
}

FORBIDDEN_ROW_FLAGS = (
    "source_review_used_for_predictive_feature",
    "candidate_specific_source_repair_used_for_predictive_feature",
    "mechanism_text_as_predictive_feature",
    "pdb_title_as_predictive_feature",
    "uniprot_prose_as_predictive_feature",
    "ec_or_rhea_as_predictive_feature",
    "source_id_as_predictive_feature",
    "post_hoc_ligand_alias_expansion",
    "post_hoc_threshold_selection",
    "cross_pdb_split_state_fusion",
    "homomeric_chain_choice_as_substrate_mapping",
)

POST_SCORE_BLOCKED_STATUSES = {
    "blocked_source_context_insufficient_review_only",
    "source_context_insufficient_or_review_only_conflict",
    "rejected_nonpositive_review_only",
}

REQUIRED_POLICY_FALSE_FLAGS = (
    "production_claim_allowed",
    "labels_or_fingerprints_changed",
    "epk_score_computed",
    "threshold_calibrated",
    "ready_for_production_scoring",
    "ready_for_label_import",
)

REVIEW_ONLY_BLOCKER_FEATURES = {
    "product_state_context",
    "substrate_acceptor_analog_context",
    "split_state_context",
    "candidate_specific_source_repair",
    "sibling_counterfamily_context",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, payload: dict[str, Any], *, pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if pretty:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        else:
            json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
            handle.write("\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def alias_lookup(policy: dict[str, Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    alias_map = policy["frozen_inputs"]["ligand_code_alias_map"]
    for canonical, aliases in alias_map.items():
        lookup[canonical.upper()] = canonical
    for canonical in alias_map:
        aliases = alias_map[canonical]
        for alias in aliases:
            lookup.setdefault(str(alias).upper(), canonical)
    return lookup


def normalize_ligand(policy: dict[str, Any], row: dict[str, Any]) -> str | None:
    raw_code = row.get("ligand_code_from_structure")
    if raw_code is None:
        return None
    return alias_lookup(policy).get(str(raw_code).upper())


def bool_feature(row: dict[str, Any], key: str) -> bool:
    return bool(row.get(key, False))


def accepted_role_policy(policy: dict[str, Any], row: dict[str, Any]) -> bool:
    accepted = set(
        policy["frozen_inputs"].get("accepted_source_free_acceptor_role_policy_ids", [])
    )
    policy_id = row.get("source_free_acceptor_role_policy_id")
    return bool(policy_id and policy_id in accepted)


def validate_policy(policy: dict[str, Any]) -> None:
    metadata = policy.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("policy metadata.review_only must be true")
    for flag in REQUIRED_POLICY_FALSE_FLAGS:
        if metadata.get(flag) is not False:
            raise ValueError(f"policy metadata.{flag} must be false")

    allowed = set(policy.get("allowed_predictive_features", []))
    forbidden = set(policy.get("forbidden_features", []))
    review_only = set(policy.get("review_only_features", []))
    if allowed & forbidden:
        overlap = sorted(allowed & forbidden)
        raise ValueError(f"predictive features overlap forbidden features: {overlap}")
    if allowed & REVIEW_ONLY_BLOCKER_FEATURES:
        overlap = sorted(allowed & REVIEW_ONLY_BLOCKER_FEATURES)
        raise ValueError(f"predictive features include review-only blockers: {overlap}")
    if not REVIEW_ONLY_BLOCKER_FEATURES.issubset(review_only):
        missing = sorted(REVIEW_ONLY_BLOCKER_FEATURES - review_only)
        raise ValueError(f"review-only blocker features missing from policy: {missing}")


def validate_tranche(tranche: dict[str, Any]) -> None:
    metadata = tranche.get("metadata", {})
    rows = tranche.get("rows")
    if metadata.get("review_only") is not True:
        raise ValueError("tranche metadata.review_only must be true")
    if rows is None or not isinstance(rows, list):
        raise ValueError("tranche rows must be a list")
    expected_count = metadata.get("row_count")
    if expected_count is not None and expected_count != len(rows):
        raise ValueError(
            f"tranche metadata.row_count={expected_count} does not match {len(rows)} rows"
        )


def evaluate_row(policy: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    required_features = list(policy["frozen_inputs"]["required_same_structure_features"])
    normalized_ligand = normalize_ligand(policy, row)
    active_ligands = set(policy["frozen_inputs"]["ligand_code_alias_map"])
    reasons: list[str] = []
    flags: list[str] = []

    for flag in FORBIDDEN_ROW_FLAGS:
        if bool_feature(row, flag):
            flags.append(flag)
    if flags:
        reasons.append("forbidden_predictive_context_present")

    if bool_feature(row, "product_state_context"):
        reasons.append("product_state_context_review_only")
    if bool_feature(row, "substrate_acceptor_analog_context"):
        reasons.append("substrate_acceptor_analog_review_only")
    if bool_feature(row, "split_state_context"):
        reasons.append("split_state_context_review_only")
    if bool_feature(row, "candidate_specific_source_repair"):
        reasons.append("candidate_specific_source_repair_review_only")
    if bool_feature(row, "sibling_counterfamily_context"):
        reasons.append("sibling_counterfamily_control_review_only")

    raw_context = str(row.get("ligand_context", "")).upper()
    if raw_context in REVIEW_ONLY_LIGAND_CONTEXTS:
        reasons.append(f"{raw_context.lower()}_review_only")

    if normalized_ligand not in active_ligands:
        reasons.append("ligand_not_in_frozen_active_gamma_alias_map")

    missing_features = [
        feature for feature in required_features if not bool_feature(row, feature)
    ]
    if missing_features:
        reasons.append("missing_required_same_structure_features")

    if bool_feature(row, "source_free_acceptor_role_features") and not accepted_role_policy(
        policy, row
    ):
        reasons.append("source_free_acceptor_role_policy_not_preaccepted")

    if row.get("clean_held_out_performance_evidence") is False:
        reasons.append("not_clean_held_out_performance_evidence")
    if bool_feature(row, "development_or_regression_context"):
        reasons.append("development_or_regression_context")

    if reasons:
        decision = "review_only_abstain"
    else:
        decision = "review_only_nonabstaining_candidate"

    return {
        "row_id": row.get("row_id") or row.get("pdb_id"),
        "pdb_id": row.get("pdb_id"),
        "row_role": row.get("row_role"),
        "normalized_ligand_state": normalized_ligand,
        "decision": decision,
        "abstention_reasons": sorted(set(reasons)),
        "missing_required_same_structure_features": missing_features,
        "forbidden_predictive_context_flags": flags,
        "post_score_review_status": row.get("post_score_review_status"),
        "expected_frozen_policy_decision": row.get("expected_frozen_policy_decision"),
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }


def choose_primary_outcome(row_results: list[dict[str, Any]]) -> str:
    if not row_results:
        return "next_query_defined"
    if any(result["forbidden_predictive_context_flags"] for result in row_results):
        return "policy_falsified"
    nonabstaining = [
        result
        for result in row_results
        if result["decision"] == "review_only_nonabstaining_candidate"
    ]
    if any(
        result.get("post_score_review_status") in POST_SCORE_BLOCKED_STATUSES
        for result in nonabstaining
    ):
        return "counterexample_found"
    return "policy_frozen_review_only"


def evaluate_tranche(policy: dict[str, Any], tranche: dict[str, Any]) -> dict[str, Any]:
    validate_policy(policy)
    validate_tranche(tranche)
    rows = tranche.get("rows", [])
    row_results = [evaluate_row(policy, row) for row in rows]
    decision_counts: dict[str, int] = {}
    abstention_reason_counts: dict[str, int] = {}
    for result in row_results:
        decision_counts[result["decision"]] = decision_counts.get(result["decision"], 0) + 1
        for reason in result["abstention_reasons"]:
            abstention_reason_counts[reason] = abstention_reason_counts.get(reason, 0) + 1

    nonabstaining = [
        result
        for result in row_results
        if result["decision"] == "review_only_nonabstaining_candidate"
    ]
    counterexamples = [
        result["pdb_id"]
        for result in nonabstaining
        if result.get("post_score_review_status") in POST_SCORE_BLOCKED_STATUSES
    ]

    return {
        "metadata": {
            "policy_version": policy["metadata"]["policy_version"],
            "policy_id": policy["metadata"]["policy_id"],
            "tranche_id": tranche.get("metadata", {}).get("tranche_id"),
            "created_at": utc_now(),
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "threshold_calibrated": False,
            "row_count": len(rows),
            "decision_counts": decision_counts,
            "abstention_reason_counts": abstention_reason_counts,
            "counterexamples_found": counterexamples,
            "primary_outcome": choose_primary_outcome(row_results),
        },
        "frozen_inputs": policy["frozen_inputs"],
        "allowed_predictive_features": policy["allowed_predictive_features"],
        "review_only_features": policy["review_only_features"],
        "forbidden_features": policy["forbidden_features"],
        "rows": row_results,
    }


def self_test() -> None:
    policy = {
        "metadata": {
            "policy_version": "self_test_policy",
            "policy_id": "self_test_policy_id",
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
            "required_same_structure_features": [
                "terminal_gamma_equivalent_geometry",
                "local_metal_context",
                "catalytic_site_locality",
                "source_free_acceptor_role_features",
                "same_structure_co_materialization",
            ],
            "accepted_source_free_acceptor_role_policy_ids": ["role_policy_v0"],
        },
        "allowed_predictive_features": [],
        "review_only_features": sorted(REVIEW_ONLY_BLOCKER_FEATURES),
        "forbidden_features": [],
    }
    passing_row = {
        "row_id": "pass",
        "pdb_id": "PASS",
        "ligand_code_from_structure": "ATP",
        "terminal_gamma_equivalent_geometry": True,
        "local_metal_context": True,
        "catalytic_site_locality": True,
        "source_free_acceptor_role_features": True,
        "source_free_acceptor_role_policy_id": "role_policy_v0",
        "same_structure_co_materialization": True,
    }
    blocked_adp = dict(passing_row, row_id="adp", ligand_code_from_structure="ADP")
    forbidden = dict(
        passing_row,
        row_id="forbidden",
        source_review_used_for_predictive_feature=True,
    )
    assert evaluate_row(policy, passing_row)["decision"] == "review_only_nonabstaining_candidate"
    assert evaluate_row(policy, blocked_adp)["decision"] == "review_only_abstain"
    forbidden_result = evaluate_row(policy, forbidden)
    assert forbidden_result["decision"] == "review_only_abstain"
    assert "source_review_used_for_predictive_feature" in forbidden_result[
        "forbidden_predictive_context_flags"
    ]
    evaluate_tranche(policy, {"metadata": {"review_only": True, "row_count": 3}, "rows": [
        passing_row,
        blocked_adp,
        forbidden,
    ]})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the frozen review-only ePK policy harness on a compact tranche."
    )
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--tranche", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    if not args.policy or not args.tranche or not args.output:
        parser.error("--policy, --tranche, and --output are required unless --self-test is set")

    policy = load_json(args.policy)
    tranche = load_json(args.tranche)
    result = evaluate_tranche(policy, tranche)
    write_json(args.output, result, pretty=args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
