#!/usr/bin/env python3
"""Audit the review-only sibling counteraxis scorer fixture.

This helper intentionally stays lane-local. It validates that the consolidated
source-free sibling control matrix is suitable as future scorer-design input
without importing labels, touching production registries, or claiming production
scoring.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE = Path("artifacts/research_lanes/epk_sibling_controls")
DEFAULT_MATRIX = LANE / "review_only_counteraxis_scorer_test_matrix_20260520.json"
DEFAULT_UNIFIED_PROTOTYPE = Path(
    "artifacts/v3_epk_unified_review_only_scoring_prototype_1025.json"
)
DEFAULT_COUNTERAXIS_DECISION = Path(
    "artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json"
)
DEFAULT_PRECOUNT_GATE = Path("artifacts/v3_epk_precount_gate_status_1025.json")
DEFAULT_SUBSTRATE_IDENTITY_PROBE = Path(
    "artifacts/v3_epk_unified_substrate_identity_rule_probe_1025.json"
)
DEFAULT_FAMILY_EXPANSION = Path(
    "artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json"
)

REQUIRED_GAMMA_FAMILIES = {
    "askha",
    "atp_grasp",
    "dnk",
    "ghkl",
    "ghmp",
    "ndk",
    "pfka",
    "pfkb",
}
EXPECTED_PRODUCT_FAMILIES = {"atp_grasp", "dnk", "pfka", "pfkb"}

ALLOWED_GAMMA_BLOCKERS = {
    "nonpolymer_acceptor_local_to_gamma",
    "nonpolymer_or_same_chain_local_oxygen_not_ePK_protein_substrate",
}
ALLOWED_PRODUCT_BLOCKERS = {
    "free_phosphate_product",
    "phosphorylated_hetatm_nonpolymer_product",
}

FORBIDDEN_TRUE_RESULT_FLAGS = {
    "production_scoring_admissible",
    "epk_score_computed",
    "production_claim_allowed",
    "labels_or_fingerprints_changed",
}
FORBIDDEN_TRUE_METADATA_FLAGS = {
    "production_claim_allowed",
    "production_scoring_admissible",
    "curated_label_registry_edited",
    "fingerprint_registry_edited",
    "labels_or_fingerprints_changed",
    "raw_coordinate_files_written",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def counter_dict(rows: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(rows).items()))


def case_axis(case: dict[str, Any]) -> str:
    axis = case.get("axis")
    if axis == "gamma_proximity_counteraxis":
        return "gamma"
    if axis == "product_phosphoryl_identity_counteraxis":
        return "product"
    return str(axis or "unknown")


def weak_rule_hit(case: dict[str, Any]) -> bool:
    features = case.get("input_features", {})
    if case_axis(case) == "gamma":
        return bool(features.get("weak_nearest_any_oxygen_rule_hit_6a"))
    if case_axis(case) == "product":
        return bool(features.get("weak_product_any_oxygen_rule_hit_6a"))
    return False


def expected_block(case: dict[str, Any]) -> bool:
    result = case.get("expected_review_only_result", {})
    if case_axis(case) == "gamma":
        return bool(result.get("should_block_weak_rule_hit"))
    if case_axis(case) == "product":
        return bool(result.get("should_block_weak_product_rule_hit"))
    return False


def expected_blocker(case: dict[str, Any]) -> str | None:
    blocker = case.get("expected_review_only_result", {}).get("expected_blocker")
    return blocker if isinstance(blocker, str) else None


def blocker_allowed(case: dict[str, Any]) -> bool:
    blocker = expected_blocker(case)
    if not expected_block(case):
        return blocker is None
    if case_axis(case) == "gamma":
        return blocker in ALLOWED_GAMMA_BLOCKERS
    if case_axis(case) == "product":
        return blocker in ALLOWED_PRODUCT_BLOCKERS
    return False


def production_flags_closed(case: dict[str, Any]) -> bool:
    result = case.get("expected_review_only_result", {})
    return all(result.get(flag) is False for flag in FORBIDDEN_TRUE_RESULT_FLAGS)


def source_artifacts_lane_local(case: dict[str, Any]) -> bool:
    sources = case.get("source_artifacts", [])
    if not isinstance(sources, list) or not sources:
        return False
    for source in sources:
        if not isinstance(source, str):
            return False
        path = Path(source)
        if path.is_absolute() or LANE not in path.parents:
            return False
        if not path.exists():
            return False
    return True


def assertion(name: str, passed: bool, details: Any) -> dict[str, Any]:
    return {"assertion": name, "passed": passed, "details": details}


def compact_adjacent_gate_alignment(paths: dict[str, Path]) -> dict[str, Any]:
    alignment: dict[str, Any] = {}
    for name, path in paths.items():
        data = load_json(path)
        metadata = data.get("metadata", {})
        alignment[name] = {
            "path": str(path),
            "curated_label_registry_edited": metadata.get("curated_label_registry_edited"),
            "fingerprint_registry_edited": metadata.get("fingerprint_registry_edited"),
            "epk_score_computed": metadata.get("epk_score_computed"),
            "ready_for_label_import": metadata.get("ready_for_label_import"),
            "ready_for_production_scoring": metadata.get("ready_for_production_scoring"),
            "ready_to_run_epk_scorer": metadata.get("ready_to_run_epk_scorer"),
            "precount_gate_status": metadata.get("precount_gate_status"),
            "prototype_gate_status": metadata.get("prototype_gate_status"),
            "unified_substrate_identity_ready_review_only": metadata.get(
                "unified_substrate_identity_ready_review_only"
            ),
            "unified_source_free_substrate_identity_ready_review_only": metadata.get(
                "unified_source_free_substrate_identity_ready_review_only"
            ),
            "unified_source_free_substrate_identity_production_admissible": metadata.get(
                "unified_source_free_substrate_identity_production_admissible"
            ),
            "counteraxis_sufficient_to_block_distance_only_threshold": metadata.get(
                "counteraxis_sufficient_to_block_distance_only_threshold"
            ),
        }
    return alignment


def compact_family_boundary_alignment(path: Path) -> dict[str, Any]:
    data = load_json(path)
    metadata = data.get("metadata", {})
    epk_family = next(
        (
            family
            for family in data.get("target_families", [])
            if family.get("id") == "epk"
        ),
        {},
    )
    return {
        "path": str(path),
        "parent_family_id": metadata.get("parent_family_id"),
        "boundary_guardrail_ready": metadata.get("boundary_guardrail_ready"),
        "countable_label_candidate_count": metadata.get("countable_label_candidate_count"),
        "unmapped_required_family_ids": metadata.get("unmapped_required_family_ids"),
        "unsupported_mapping_count": metadata.get("unsupported_mapping_count"),
        "epk_sibling_ids": sorted(epk_family.get("sibling_ids", [])),
        "epk_scope_note": epk_family.get("scope_note"),
    }


def adjacent_gate_alignment_passes(alignment: dict[str, Any]) -> bool:
    unified = alignment.get("unified_review_only_scoring_prototype", {})
    decision = alignment.get("counteraxis_sufficiency_decision", {})
    precount = alignment.get("precount_gate_status", {})
    substrate = alignment.get("unified_substrate_identity_rule_probe", {})
    return (
        unified.get("ready_for_label_import") is False
        and unified.get("ready_for_production_scoring") is False
        and unified.get("ready_to_run_epk_scorer") is False
        and unified.get("epk_score_computed") is False
        and unified.get("prototype_gate_status") == "fail_closed_review_only"
        and decision.get("counteraxis_sufficient_to_block_distance_only_threshold") is True
        and decision.get("unified_substrate_identity_ready_review_only") is True
        and decision.get("precount_gate_status") == "blocked_review_only"
        and precount.get("precount_gate_status") == "blocked_review_only"
        and precount.get("ready_for_label_import") is False
        and precount.get("ready_to_run_epk_scorer") is False
        and substrate.get("unified_source_free_substrate_identity_ready_review_only") is True
        and substrate.get("unified_source_free_substrate_identity_production_admissible")
        is False
        and substrate.get("ready_for_production_scoring") is False
    )


def family_boundary_alignment_passes(alignment: dict[str, Any]) -> bool:
    return (
        set(alignment.get("epk_sibling_ids", [])) == REQUIRED_GAMMA_FAMILIES
        and alignment.get("parent_family_id") == "atp_phosphoryl_transfer"
        and alignment.get("boundary_guardrail_ready") is True
        and alignment.get("countable_label_candidate_count") == 0
        and alignment.get("unmapped_required_family_ids") == []
        and alignment.get("unsupported_mapping_count") == 0
    )


def build_audit(
    matrix_path: Path,
    adjacent_paths: dict[str, Path],
    family_expansion_path: Path,
) -> dict[str, Any]:
    matrix = load_json(matrix_path)
    metadata = matrix.get("metadata", {})
    contract = matrix.get("review_only_contract", {})
    adjacent_alignment = compact_adjacent_gate_alignment(adjacent_paths)
    family_boundary_alignment = compact_family_boundary_alignment(family_expansion_path)
    gamma_cases = matrix.get("gamma_proximity_counteraxis_cases", [])
    product_cases = matrix.get("product_phosphoryl_identity_counteraxis_cases", [])
    cases = [*gamma_cases, *product_cases]
    case_ids = [case.get("case_id") for case in cases]
    source_artifact_paths = sorted(
        {
            source
            for case in cases
            for source in case.get("source_artifacts", [])
            if isinstance(source, str)
        }
    )
    digest_paths = [
        matrix_path,
        family_expansion_path,
        *adjacent_paths.values(),
        *(Path(source) for source in source_artifact_paths),
    ]
    source_file_sha256 = {str(path): file_sha256(path) for path in digest_paths}
    duplicate_case_ids = sorted(
        case_id for case_id, count in Counter(case_ids).items() if count > 1
    )

    weak_cases = [case for case in cases if weak_rule_hit(case)]
    weak_unblocked = [
        case["case_id"]
        for case in weak_cases
        if not expected_block(case) or not blocker_allowed(case)
    ]
    existing_minimal_design_panel_case_ids = sorted(
        case["case_id"]
        for case in cases
        if case.get("included_in_existing_minimal_design_panel") is True
    )
    forbidden_flag_cases = [
        case["case_id"] for case in cases if not production_flags_closed(case)
    ]
    nonlocal_source_cases = [
        case["case_id"] for case in cases if not source_artifacts_lane_local(case)
    ]
    blocker_mismatches = [
        case["case_id"] for case in cases if not blocker_allowed(case)
    ]

    family_axis_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for case in cases:
        family_axis_counts[case["family_id"]][case_axis(case)] += 1

    missing_gamma_families = sorted(
        REQUIRED_GAMMA_FAMILIES
        - {case["family_id"] for case in gamma_cases}
    )
    unexpected_product_families = sorted(
        {case["family_id"] for case in product_cases} - EXPECTED_PRODUCT_FAMILIES
    )

    metadata_forbidden_flags = {
        flag: metadata.get(flag) for flag in sorted(FORBIDDEN_TRUE_METADATA_FLAGS)
    }
    metadata_flags_closed = all(
        metadata.get(flag) is False for flag in FORBIDDEN_TRUE_METADATA_FLAGS
    )

    expected_unblocked_from_metadata = metadata.get("expected_unblocked_weak_case_count")
    stored_unique_count = metadata.get("unique_case_count")
    computed_unique_count = len(set(case_ids))

    assertions = [
        assertion(
            "matrix_has_expected_case_count",
            len(cases) == 91 and len(gamma_cases) == 72 and len(product_cases) == 19,
            {
                "total_cases": len(cases),
                "gamma_cases": len(gamma_cases),
                "product_cases": len(product_cases),
            },
        ),
        assertion(
            "case_ids_are_unique",
            not duplicate_case_ids,
            {"duplicate_case_ids": duplicate_case_ids},
        ),
        assertion(
            "metadata_unique_count_matches_cases",
            stored_unique_count == computed_unique_count,
            {
                "metadata_unique_case_count": stored_unique_count,
                "computed_unique_case_count": computed_unique_count,
            },
        ),
        assertion(
            "all_weak_cases_have_expected_review_only_blockers",
            not weak_unblocked,
            {"weak_case_count": len(weak_cases), "weak_unblocked_case_ids": weak_unblocked},
        ),
        assertion(
            "expected_blockers_are_allowed_by_axis",
            not blocker_mismatches,
            {"blocker_mismatch_case_ids": blocker_mismatches},
        ),
        assertion(
            "per_case_production_flags_closed",
            not forbidden_flag_cases,
            {"cases_with_forbidden_true_flags": forbidden_flag_cases},
        ),
        assertion(
            "metadata_production_flags_closed",
            metadata_flags_closed,
            metadata_forbidden_flags,
        ),
        assertion(
            "review_only_contract_forbids_label_threshold_registry_use",
            contract.get("do_not_import_as_labels") is True
            and contract.get("do_not_calibrate_thresholds") is True
            and contract.get("do_not_edit_production_registries") is True
            and contract.get("do_not_claim_production_scoring") is True,
            contract,
        ),
        assertion(
            "source_artifacts_are_existing_lane_local_json",
            not nonlocal_source_cases,
            {"cases_with_missing_or_nonlocal_sources": nonlocal_source_cases},
        ),
        assertion(
            "gamma_family_surface_is_complete_for_defined_fixture",
            not missing_gamma_families,
            {
                "required_gamma_families": sorted(REQUIRED_GAMMA_FAMILIES),
                "missing_gamma_families": missing_gamma_families,
            },
        ),
        assertion(
            "product_family_surface_is_expected_subset",
            not unexpected_product_families,
            {
                "expected_product_families": sorted(EXPECTED_PRODUCT_FAMILIES),
                "unexpected_product_families": unexpected_product_families,
            },
        ),
        assertion(
            "metadata_unblocked_weak_count_matches_audit",
            expected_unblocked_from_metadata == len(weak_unblocked),
            {
                "metadata_expected_unblocked_weak_case_count": expected_unblocked_from_metadata,
                "computed_unblocked_weak_case_count": len(weak_unblocked),
            },
        ),
        assertion(
            "existing_minimal_design_panel_is_represented",
            len(existing_minimal_design_panel_case_ids) == metadata.get(
                "existing_minimal_design_panel_case_count"
            )
            == 16,
            {
                "metadata_existing_minimal_design_panel_case_count": metadata.get(
                    "existing_minimal_design_panel_case_count"
                ),
                "computed_existing_minimal_design_panel_case_count": len(
                    existing_minimal_design_panel_case_ids
                ),
                "existing_minimal_design_panel_case_ids": existing_minimal_design_panel_case_ids,
            },
        ),
        assertion(
            "adjacent_review_only_gate_artifacts_remain_fail_closed",
            adjacent_gate_alignment_passes(adjacent_alignment),
            adjacent_alignment,
        ),
        assertion(
            "ontology_family_boundary_matches_fixture_surface",
            family_boundary_alignment_passes(family_boundary_alignment),
            family_boundary_alignment,
        ),
    ]
    passed = all(item["passed"] for item in assertions)

    weak_case_ids_by_axis = {
        "gamma": sorted(case["case_id"] for case in gamma_cases if weak_rule_hit(case)),
        "product": sorted(case["case_id"] for case in product_cases if weak_rule_hit(case)),
    }

    return {
        "metadata": {
            "method": "epk_sibling_controls_review_only_fixture_readiness_audit",
            "created_at": utc_now(),
            "source_matrix": str(matrix_path),
            "source_file_digest_count": len(source_file_sha256),
            "review_only": True,
            "production_claim_allowed": False,
            "production_scoring_admissible": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "controls_adjudicated": len(cases),
            "controls_added": 0,
            "rows_reviewed": len(cases),
            "gamma_case_count": len(gamma_cases),
            "product_case_count": len(product_cases),
            "weak_gamma_case_count": len(weak_case_ids_by_axis["gamma"]),
            "weak_product_case_count": len(weak_case_ids_by_axis["product"]),
            "expected_unblocked_weak_case_count": len(weak_unblocked),
            "existing_minimal_design_panel_case_count": len(
                existing_minimal_design_panel_case_ids
            ),
            "assertion_count": len(assertions),
            "assertions_passed": sum(1 for item in assertions if item["passed"]),
            "fixture_readiness_status": "ready_review_only" if passed else "blocked",
            "primary_outcome": "evidence_for" if passed else "evidence_against",
            "search_surface": (
                "Bounded 91-case review-only sibling counteraxis matrix: 72 gamma "
                "controls and 19 strict product controls from existing lane artifacts."
            ),
            "next_query": (
                "Use the matrix and readiness audit as future source-free scorer-design "
                "fixtures; only reopen sibling sourcing if a specific curated seed set appears."
            ),
        },
        "summary": {
            "case_counts_by_axis": {
                "gamma": len(gamma_cases),
                "product": len(product_cases),
            },
            "case_counts_by_family_and_axis": {
                family: dict(sorted(axis_counts.items()))
                for family, axis_counts in sorted(family_axis_counts.items())
            },
            "weak_case_counts_by_axis": {
                axis: len(ids) for axis, ids in weak_case_ids_by_axis.items()
            },
            "expected_blocker_counts": counter_dict(
                [
                    f"{case_axis(case)}::{expected_blocker(case) or 'none_required'}"
                    for case in cases
                ]
            ),
            "weak_case_ids_by_axis": weak_case_ids_by_axis,
            "expected_unblocked_weak_case_ids": weak_unblocked,
            "existing_minimal_design_panel_case_ids": existing_minimal_design_panel_case_ids,
        },
        "source_file_sha256": source_file_sha256,
        "assertions": assertions,
        "review_only_contract": {
            "do_not_import_as_labels": True,
            "do_not_calibrate_thresholds": True,
            "do_not_edit_production_registries": True,
            "do_not_claim_production_scoring": True,
            "do_not_claim_production_ePK_separation": True,
            "expected_runtime_scope": "future scorer tests only",
        },
        "adjacent_review_only_gate_alignment": adjacent_alignment,
        "ontology_family_boundary_alignment": family_boundary_alignment,
        "recommendation": (
            "Use this readiness artifact only to guide future source-free "
            "substrate-identity and family-boundary scorer tests. Keep production "
            "labels, registries, fingerprints, thresholds, and scoring claims closed."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    parser.add_argument("--out", required=True)
    parser.add_argument("--unified-prototype", default=str(DEFAULT_UNIFIED_PROTOTYPE))
    parser.add_argument(
        "--counteraxis-decision",
        default=str(DEFAULT_COUNTERAXIS_DECISION),
    )
    parser.add_argument("--precount-gate", default=str(DEFAULT_PRECOUNT_GATE))
    parser.add_argument(
        "--substrate-identity-probe",
        default=str(DEFAULT_SUBSTRATE_IDENTITY_PROBE),
    )
    parser.add_argument("--family-expansion", default=str(DEFAULT_FAMILY_EXPANSION))
    args = parser.parse_args()

    audit = build_audit(
        Path(args.matrix),
        {
            "unified_review_only_scoring_prototype": Path(args.unified_prototype),
            "counteraxis_sufficiency_decision": Path(args.counteraxis_decision),
            "precount_gate_status": Path(args.precount_gate),
            "unified_substrate_identity_rule_probe": Path(args.substrate_identity_probe),
        },
        Path(args.family_expansion),
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit["metadata"], indent=2, sort_keys=True))
    return 0 if audit["metadata"]["fixture_readiness_status"] == "ready_review_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
