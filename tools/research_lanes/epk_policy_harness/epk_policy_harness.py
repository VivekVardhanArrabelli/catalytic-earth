#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
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
    "source_validation_used_for_predictive_feature",
    "candidate_specific_source_repair_used_for_predictive_feature",
    "mechanism_text_as_predictive_feature",
    "pdb_title_as_predictive_feature",
    "structure_title_used_for_predictive_feature",
    "uniprot_prose_as_predictive_feature",
    "ec_or_rhea_as_predictive_feature",
    "source_id_as_predictive_feature",
    "source_query_used_for_predictive_feature",
    "source_text_used_for_predictive_feature",
    "post_hoc_ligand_alias_expansion",
    "query_ligand_synonym_used_as_coordinate_ligand",
    "post_hoc_threshold_selection",
    "cross_pdb_split_state_fusion",
    "homomeric_chain_choice_as_substrate_mapping",
)

SOURCE_VALIDATION_PHASE_CONTRACT_TRUE_FLAGS = (
    "candidate_ids_frozen_before_local_feature_review",
    "source_free_local_features_computed_before_source_validation",
    "source_validation_applied_after_local_features",
    "source_validation_review_only",
)

SOURCE_VALIDATION_PHASE_CONTRACT_ROW_FALSE_FLAGS = (
    "source_validation_used_for_predictive_feature",
    "source_text_used_for_predictive_feature",
    "structure_title_used_for_predictive_feature",
    "source_id_as_predictive_feature",
    "source_query_used_for_predictive_feature",
)

TOPOLOGY_REVIEW_CONTRACT_TRUE_FLAGS = (
    "topology_status_required",
    "cross_chain_geometry_review_only_without_preaccepted_role_policy",
)

SIBLING_CONTROL_CONTRACT_TRUE_FLAGS = (
    "lead_control_pairing_frozen_before_evaluation",
    "pairing_uses_source_free_local_features_only",
    "sibling_control_context_review_only",
    "lead_and_control_expected_abstention",
)

SIBLING_PAIR_ROLES = {"geometry_lead", "sibling_control"}

SOURCE_DERIVED_FEATURE_TOKENS = (
    "source",
    "query",
    "title",
    "text",
    "label",
    "mechanism",
    "uniprot",
    "ec",
    "rhea",
)

PRIMARY_OUTCOMES = {
    "policy_frozen_review_only",
    "policy_falsified",
    "counterexample_found",
    "search_surface_exhausted",
    "next_query_defined",
}

QUERY_CONTEXT_CONTRACT_TRUE_FLAGS = (
    "source_queries_review_only",
    "query_text_not_matching_feature",
    "coordinate_ligand_code_required",
)

COORDINATE_LIGAND_MATERIALIZATION_GUARD_TRUE_FLAGS = (
    "coordinate_ligand_codes_inventoried_before_local_feature_review",
    "query_synonyms_review_only",
    "post_hoc_ligand_alias_expansion_forbidden",
    "terminal_gamma_rows_limited_to_pre_frozen_coordinate_codes",
    "non_prefrozen_materializations_recorded_as_review_only_blockers",
)

COORDINATE_LIGAND_CODE_SOURCES = {
    "mmcif_atom_site_auth_or_label_comp_id",
    "mmcif_atom_site_label_comp_id",
    "mmcif_atom_site_auth_comp_id",
}

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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def upper_string_set(values: Any, *, field_name: str) -> set[str]:
    if not isinstance(values, list):
        raise ValueError(f"{field_name} must be a list")
    normalized = {str(value).strip().upper() for value in values if str(value).strip()}
    if len(normalized) != len(values):
        raise ValueError(f"{field_name} must contain only non-empty strings")
    return normalized


def accepted_role_policy(policy: dict[str, Any], row: dict[str, Any]) -> bool:
    accepted = set(
        policy["frozen_inputs"].get("accepted_source_free_acceptor_role_policy_ids", [])
    )
    policy_id = row.get("source_free_acceptor_role_policy_id")
    return bool(policy_id and policy_id in accepted)


def frozen_distance_cutoff_reason(policy: dict[str, Any], row: dict[str, Any]) -> str | None:
    cutoff = policy["frozen_inputs"].get("candidate_distance_cutoff_angstrom")
    if cutoff is None or not bool_feature(row, "terminal_gamma_equivalent_geometry"):
        return None

    distance = row.get("nearest_gamma_acceptor_distance_angstrom")
    if distance is None:
        return "nearest_gamma_acceptor_distance_missing"

    try:
        distance_value = float(distance)
        cutoff_value = float(cutoff)
    except (TypeError, ValueError):
        return "nearest_gamma_acceptor_distance_not_numeric"

    if distance_value > cutoff_value:
        return "nearest_gamma_acceptor_distance_above_frozen_cutoff"
    return None


def expected_decision_match(row: dict[str, Any], decision: str) -> bool | None:
    expected = row.get("expected_frozen_policy_decision")
    if expected is None:
        return None
    return str(expected).startswith(decision)


def validate_policy(policy: dict[str, Any]) -> None:
    metadata = policy.get("metadata", {})
    if metadata.get("review_only") is not True:
        raise ValueError("policy metadata.review_only must be true")
    for flag in REQUIRED_POLICY_FALSE_FLAGS:
        if metadata.get(flag) is not False:
            raise ValueError(f"policy metadata.{flag} must be false")

    frozen_inputs = policy.get("frozen_inputs", {})
    cutoff = frozen_inputs.get("candidate_distance_cutoff_angstrom")
    if cutoff is None:
        raise ValueError("policy frozen_inputs.candidate_distance_cutoff_angstrom is required")
    try:
        cutoff_value = float(cutoff)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "policy frozen_inputs.candidate_distance_cutoff_angstrom must be numeric"
        ) from error
    if cutoff_value <= 0:
        raise ValueError(
            "policy frozen_inputs.candidate_distance_cutoff_angstrom must be positive"
        )

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


def validate_tranche(tranche: dict[str, Any], policy: dict[str, Any] | None = None) -> None:
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
    if metadata.get("terminal_gamma_required_for_tranche") is True:
        terminal_gamma_count = metadata.get("terminal_gamma_candidate_count_reviewed")
        try:
            terminal_gamma_count_value = int(terminal_gamma_count)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "terminal-gamma tranches require numeric "
                "metadata.terminal_gamma_candidate_count_reviewed"
            ) from error
        if terminal_gamma_count_value <= 0:
            raise ValueError(
                "terminal-gamma tranches require positive "
                "metadata.terminal_gamma_candidate_count_reviewed"
            )
        required_atom_name = str(metadata.get("terminal_gamma_atom_name_required", "PG")).upper()
        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            if row.get("terminal_gamma_equivalent_geometry") is not True:
                raise ValueError(
                    f"row {row_id} violates terminal-gamma tranche contract: "
                    "terminal_gamma_equivalent_geometry must be true"
                )
            if str(row.get("terminal_gamma_atom_name") or "").upper() != required_atom_name:
                raise ValueError(
                    f"row {row_id} violates terminal-gamma tranche contract: "
                    f"terminal_gamma_atom_name must be {required_atom_name}"
                )
    topology_contract = metadata.get("topology_review_contract")
    if topology_contract:
        if not isinstance(topology_contract, dict):
            raise ValueError("tranche metadata.topology_review_contract must be an object")
        for flag in TOPOLOGY_REVIEW_CONTRACT_TRUE_FLAGS:
            if topology_contract.get(flag) is not True:
                raise ValueError(f"topology review contract requires {flag}=true")
        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            topology_status = str(row.get("topology_ambiguity_status") or "").strip()
            if not topology_status:
                raise ValueError(
                    f"row {row_id} violates topology review contract: "
                    "topology_ambiguity_status is required"
                )
            cross_chain_candidate = (
                "nonconfounded" in str(row.get("row_role") or "")
                or topology_status.startswith("cross_auth_chain_candidate")
            )
            if cross_chain_candidate and not bool_feature(
                row, "source_free_acceptor_role_features"
            ):
                if bool_feature(row, "same_structure_co_materialization"):
                    raise ValueError(
                        f"row {row_id} violates topology review contract: "
                        "same_structure_co_materialization must remain false without "
                        "source-free role features"
                    )
                expected = str(row.get("expected_frozen_policy_decision") or "")
                if not expected.startswith("review_only_abstain"):
                    raise ValueError(
                        f"row {row_id} violates topology review contract: "
                        "cross-chain geometry without a source-free role policy must "
                        "expect review-only abstention"
                    )
    sibling_contract = metadata.get("sibling_control_contract")
    if sibling_contract:
        if not isinstance(sibling_contract, dict):
            raise ValueError("tranche metadata.sibling_control_contract must be an object")
        for flag in SIBLING_CONTROL_CONTRACT_TRUE_FLAGS:
            if sibling_contract.get(flag) is not True:
                raise ValueError(f"sibling control contract requires {flag}=true")
        matching_features = sibling_contract.get("source_free_matching_features")
        if not isinstance(matching_features, list) or not matching_features:
            raise ValueError(
                "sibling control contract requires non-empty source_free_matching_features"
            )
        forbidden_matching_features = [
            str(feature)
            for feature in matching_features
            if set(re.split(r"[^a-z0-9]+", str(feature).lower()))
            & set(SOURCE_DERIVED_FEATURE_TOKENS)
        ]
        if forbidden_matching_features:
            raise ValueError(
                "sibling control matching features must be source-free local features: "
                f"{forbidden_matching_features}"
            )

        allowed_matching_features = {str(feature) for feature in matching_features}
        pair_roles: dict[str, set[str]] = {}
        pair_role_counts: dict[str, dict[str, int]] = {}
        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            pair_id = str(row.get("sibling_pair_id") or "").strip()
            pair_role = str(row.get("sibling_pair_role") or "").strip()
            if not pair_id:
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "sibling_pair_id is required"
                )
            if pair_role not in SIBLING_PAIR_ROLES:
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    f"sibling_pair_role must be one of {sorted(SIBLING_PAIR_ROLES)}"
                )
            pair_roles.setdefault(pair_id, set()).add(pair_role)
            pair_role_counts.setdefault(pair_id, {})
            pair_role_counts[pair_id][pair_role] = (
                pair_role_counts[pair_id].get(pair_role, 0) + 1
            )
            row_matching_features = row.get("sibling_matching_features")
            if not isinstance(row_matching_features, list) or not row_matching_features:
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "sibling_matching_features must be a non-empty list"
                )
            row_forbidden_features = [
                str(feature)
                for feature in row_matching_features
                if set(re.split(r"[^a-z0-9]+", str(feature).lower()))
                & set(SOURCE_DERIVED_FEATURE_TOKENS)
            ]
            if row_forbidden_features:
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "row sibling_matching_features must be source-free local features"
                )
            unexpected_row_features = sorted(
                {str(feature) for feature in row_matching_features}
                - allowed_matching_features
            )
            if unexpected_row_features:
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "row sibling_matching_features must be declared in metadata "
                    f"{unexpected_row_features}"
                )
            expected = str(row.get("expected_frozen_policy_decision") or "")
            if not expected.startswith("review_only_abstain"):
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "lead/control rows must expect review-only abstention"
                )
            if bool_feature(row, "same_structure_co_materialization"):
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "same_structure_co_materialization must remain false"
                )
            if pair_role == "sibling_control" and not bool_feature(
                row, "sibling_counterfamily_context"
            ):
                raise ValueError(
                    f"row {row_id} violates sibling control contract: "
                    "sibling controls must set sibling_counterfamily_context=true"
                )
        if not pair_roles:
            raise ValueError("sibling control contract requires at least one pair")
        missing_roles = {
            pair_id: sorted(SIBLING_PAIR_ROLES - roles)
            for pair_id, roles in pair_roles.items()
            if roles != SIBLING_PAIR_ROLES
        }
        if missing_roles:
            raise ValueError(
                "sibling control contract requires one geometry_lead and one "
                f"sibling_control per pair: {missing_roles}"
            )
        duplicate_roles = {
            pair_id: role_counts
            for pair_id, role_counts in pair_role_counts.items()
            if any(role_counts.get(role, 0) != 1 for role in SIBLING_PAIR_ROLES)
        }
        if duplicate_roles:
            raise ValueError(
                "sibling control contract requires exactly one row per pair role: "
                f"{duplicate_roles}"
            )
        expected_pair_count = sibling_contract.get("matched_pair_count")
        if expected_pair_count is not None:
            try:
                expected_pair_count_value = int(expected_pair_count)
            except (TypeError, ValueError) as error:
                raise ValueError(
                    "sibling control contract matched_pair_count must be numeric"
                ) from error
            if expected_pair_count_value != len(pair_roles):
                raise ValueError(
                    "sibling control contract matched_pair_count does not match "
                    f"row pairs: {expected_pair_count_value} != {len(pair_roles)}"
                )
    if metadata.get("search_surface_exhausted") is True:
        reviewed = metadata.get("search_surface_candidate_count_reviewed")
        try:
            reviewed_count = int(reviewed)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "search_surface_exhausted tranches require numeric "
                "metadata.search_surface_candidate_count_reviewed"
            ) from error
        if reviewed_count <= 0:
            raise ValueError(
                "search_surface_exhausted tranches require positive "
                "metadata.search_surface_candidate_count_reviewed"
            )
        nonconfounded = metadata.get("nonconfounded_candidate_count_within_cutoff")
        try:
            nonconfounded_count = int(nonconfounded)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "search_surface_exhausted tranches require numeric "
                "metadata.nonconfounded_candidate_count_within_cutoff"
            ) from error
        if nonconfounded_count != 0:
            raise ValueError(
                "search_surface_exhausted tranches require "
                "metadata.nonconfounded_candidate_count_within_cutoff=0"
            )
        source_artifacts = metadata.get("source_artifacts", [])
        if not any("search_surface" in str(path) for path in source_artifacts):
            raise ValueError(
                "search_surface_exhausted tranches must cite a search_surface artifact"
                    )
    query_context_contract = metadata.get("query_context_review_only_contract")
    if query_context_contract:
        if not isinstance(query_context_contract, dict):
            raise ValueError(
                "tranche metadata.query_context_review_only_contract must be an object"
            )
        for flag in QUERY_CONTEXT_CONTRACT_TRUE_FLAGS:
            if query_context_contract.get(flag) is not True:
                raise ValueError(f"query context review-only contract requires {flag}=true")
        contexts = metadata.get("source_surface_query_contexts_review_only")
        if not isinstance(contexts, list) or not contexts:
            raise ValueError(
                "query context review-only contract requires "
                "metadata.source_surface_query_contexts_review_only"
            )
        for index, context in enumerate(contexts):
            if not isinstance(context, dict):
                raise ValueError(
                    "query context review-only contract requires object contexts"
                )
            if context.get("review_only") is not True:
                raise ValueError(
                    "query context review-only contract requires "
                    f"context {index} review_only=true"
                )
            if not str(context.get("query") or "").strip():
                raise ValueError(
                    "query context review-only contract requires non-empty query text"
                )
        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            if not str(row.get("ligand_code_from_structure") or "").strip():
                raise ValueError(
                    f"row {row_id} violates query context review-only contract: "
                    "ligand_code_from_structure is required"
                )
            if bool_feature(row, "source_query_used_for_predictive_feature"):
                raise ValueError(
                    f"row {row_id} violates query context review-only contract: "
                    "source_query_used_for_predictive_feature"
                )
    materialization_guard = metadata.get("coordinate_ligand_materialization_guard")
    if materialization_guard:
        if not isinstance(materialization_guard, dict):
            raise ValueError(
                "tranche metadata.coordinate_ligand_materialization_guard must be an object"
            )
        for flag in COORDINATE_LIGAND_MATERIALIZATION_GUARD_TRUE_FLAGS:
            if materialization_guard.get(flag) is not True:
                raise ValueError(
                    "coordinate ligand materialization guard requires "
                    f"{flag}=true"
                )

        pre_frozen_codes = upper_string_set(
            materialization_guard.get("pre_frozen_coordinate_ligand_codes"),
            field_name=(
                "metadata.coordinate_ligand_materialization_guard."
                "pre_frozen_coordinate_ligand_codes"
            ),
        )
        if not pre_frozen_codes:
            raise ValueError(
                "coordinate ligand materialization guard requires at least one "
                "pre-frozen coordinate ligand code"
            )
        if policy is not None:
            frozen_policy_codes = {
                str(code).upper()
                for code in policy["frozen_inputs"]["ligand_code_alias_map"]
            }
            undeclared_policy_codes = sorted(pre_frozen_codes - frozen_policy_codes)
            if undeclared_policy_codes:
                raise ValueError(
                    "coordinate ligand materialization guard requires pre-frozen "
                    "coordinate codes to be declared in the frozen policy ligand map: "
                    f"{undeclared_policy_codes}"
                )

        query_synonyms = upper_string_set(
            materialization_guard.get("query_ligand_synonyms_review_only"),
            field_name=(
                "metadata.coordinate_ligand_materialization_guard."
                "query_ligand_synonyms_review_only"
            ),
        )
        if not query_synonyms:
            raise ValueError(
                "coordinate ligand materialization guard requires review-only "
                "query ligand synonyms"
            )
        overlapping_query_codes = sorted(pre_frozen_codes & query_synonyms)
        if overlapping_query_codes:
            raise ValueError(
                "coordinate ligand materialization guard requires query synonyms "
                "to stay outside the pre-frozen coordinate code set: "
                f"{overlapping_query_codes}"
            )

        observed_codes = upper_string_set(
            metadata.get("coordinate_ligand_codes_observed"),
            field_name="metadata.coordinate_ligand_codes_observed",
        )
        if not observed_codes:
            raise ValueError(
                "coordinate ligand materialization guard requires observed "
                "coordinate ligand codes"
            )
        blockers = upper_string_set(
            metadata.get("alias_map_blockers_review_only", []),
            field_name="metadata.alias_map_blockers_review_only",
        )
        blocker_overlap = sorted(blockers & pre_frozen_codes)
        if blocker_overlap:
            raise ValueError(
                "coordinate ligand materialization guard requires review-only "
                "blockers to stay outside the pre-frozen coordinate code set: "
                f"{blocker_overlap}"
            )
        unblocked_non_prefrozen = sorted(observed_codes - pre_frozen_codes - blockers)
        if unblocked_non_prefrozen:
            raise ValueError(
                "coordinate ligand materialization guard requires non-prefrozen "
                "coordinate materializations to be recorded as review-only blockers: "
                f"{unblocked_non_prefrozen}"
            )

        contexts = metadata.get("source_surface_query_contexts_review_only")
        if not isinstance(contexts, list) or not contexts:
            raise ValueError(
                "coordinate ligand materialization guard requires "
                "metadata.source_surface_query_contexts_review_only"
            )
        for index, context in enumerate(contexts):
            if not isinstance(context, dict):
                raise ValueError(
                    "coordinate ligand materialization guard requires object contexts"
                )
            if context.get("review_only") is not True:
                raise ValueError(
                    "coordinate ligand materialization guard requires "
                    f"context {index} review_only=true"
                )
            context_observed = context.get("coordinate_ligand_codes_observed")
            if context_observed is not None:
                context_codes = upper_string_set(
                    context_observed,
                    field_name=(
                        "metadata.source_surface_query_contexts_review_only"
                        f"[{index}].coordinate_ligand_codes_observed"
                    ),
                )
                undeclared_context_codes = sorted(context_codes - observed_codes)
                if undeclared_context_codes:
                    raise ValueError(
                        "coordinate ligand materialization guard requires context "
                        "observed codes to be declared in metadata: "
                        f"{undeclared_context_codes}"
                    )

        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            ligand_code = str(row.get("ligand_code_from_structure") or "").strip().upper()
            if ligand_code not in pre_frozen_codes:
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "ligand_code_from_structure must be a pre-frozen coordinate code"
                )
            if ligand_code not in observed_codes:
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "ligand_code_from_structure must be present in the coordinate "
                    "ligand inventory"
                )
            if row.get("coordinate_ligand_materialized_from_structure") is not True:
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "coordinate_ligand_materialized_from_structure must be true"
                )
            source = str(row.get("coordinate_ligand_code_source") or "").strip()
            if source not in COORDINATE_LIGAND_CODE_SOURCES:
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "coordinate_ligand_code_source must be an mmCIF atom_site source"
                )
            if bool_feature(row, "query_ligand_synonym_used_as_coordinate_ligand"):
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "query_ligand_synonym_used_as_coordinate_ligand"
                )
            if bool_feature(row, "post_hoc_ligand_alias_expansion"):
                raise ValueError(
                    f"row {row_id} violates coordinate ligand materialization guard: "
                    "post_hoc_ligand_alias_expansion"
                )
    phase_contract = metadata.get("source_validation_phase_contract")
    if phase_contract:
        if not isinstance(phase_contract, dict):
            raise ValueError("tranche metadata.source_validation_phase_contract must be an object")
        for flag in SOURCE_VALIDATION_PHASE_CONTRACT_TRUE_FLAGS:
            if phase_contract.get(flag) is not True:
                raise ValueError(
                    f"source validation phase contract requires {flag}=true"
                )
        for row in rows:
            row_id = row.get("row_id") or row.get("pdb_id")
            for flag in SOURCE_VALIDATION_PHASE_CONTRACT_ROW_FALSE_FLAGS:
                if bool_feature(row, flag):
                    raise ValueError(
                        f"row {row_id} violates source validation phase contract: {flag}"
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

    distance_reason = frozen_distance_cutoff_reason(policy, row)
    if distance_reason:
        reasons.append(distance_reason)

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
        "nearest_gamma_acceptor_distance_angstrom": row.get(
            "nearest_gamma_acceptor_distance_angstrom"
        ),
        "decision": decision,
        "abstention_reasons": sorted(set(reasons)),
        "missing_required_same_structure_features": missing_features,
        "forbidden_predictive_context_flags": flags,
        "post_score_review_status": row.get("post_score_review_status"),
        "source_validation_status": row.get("source_validation_status"),
        "source_validation_phase": row.get("source_validation_phase"),
        "topology_ambiguity_status": row.get("topology_ambiguity_status"),
        "sibling_pair_id": row.get("sibling_pair_id"),
        "sibling_pair_role": row.get("sibling_pair_role"),
        "sibling_counterfamily_context": bool_feature(row, "sibling_counterfamily_context"),
        "sibling_control_match_status": row.get("sibling_control_match_status"),
        "freshness_status": row.get("freshness_status"),
        "coordinate_ligand_materialized_from_structure": bool_feature(
            row, "coordinate_ligand_materialized_from_structure"
        ),
        "coordinate_ligand_code_source": row.get("coordinate_ligand_code_source"),
        "query_ligand_synonym_used_as_coordinate_ligand": bool_feature(
            row, "query_ligand_synonym_used_as_coordinate_ligand"
        ),
        "expected_frozen_policy_decision": row.get("expected_frozen_policy_decision"),
        "expected_frozen_policy_match": expected_decision_match(row, decision),
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }


def choose_primary_outcome(
    row_results: list[dict[str, Any]], tranche_metadata: dict[str, Any] | None = None
) -> str:
    tranche_metadata = tranche_metadata or {}
    if not row_results:
        if tranche_metadata.get("search_surface_exhausted") is True:
            return "search_surface_exhausted"
        return "next_query_defined"
    if any(result.get("expected_frozen_policy_match") is False for result in row_results):
        return "policy_falsified"
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
    if tranche_metadata.get("search_surface_exhausted") is True:
        return "search_surface_exhausted"
    return "policy_frozen_review_only"


def evaluate_tranche(policy: dict[str, Any], tranche: dict[str, Any]) -> dict[str, Any]:
    validate_policy(policy)
    validate_tranche(tranche, policy=policy)
    rows = tranche.get("rows", [])
    tranche_metadata = tranche.get("metadata", {})
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
    expected_decision_mismatches = [
        result["row_id"]
        for result in row_results
        if result.get("expected_frozen_policy_match") is False
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
            "expected_decision_mismatch_count": len(expected_decision_mismatches),
            "expected_decision_mismatches": expected_decision_mismatches,
            "terminal_gamma_required_for_tranche": bool(
                tranche_metadata.get("terminal_gamma_required_for_tranche", False)
            ),
            "topology_review_contract_enforced": bool(
                tranche_metadata.get("topology_review_contract")
            ),
            "sibling_control_contract_enforced": bool(
                tranche_metadata.get("sibling_control_contract")
            ),
            "query_context_review_only_contract_enforced": bool(
                tranche_metadata.get("query_context_review_only_contract")
            ),
            "coordinate_ligand_materialization_guard_enforced": bool(
                tranche_metadata.get("coordinate_ligand_materialization_guard")
            ),
            "search_surface_exhausted": bool(
                tranche_metadata.get("search_surface_exhausted", False)
            ),
            "harness_forbidden_row_flags": sorted(FORBIDDEN_ROW_FLAGS),
            "primary_outcome_allowed_values": sorted(PRIMARY_OUTCOMES),
            "primary_outcome": choose_primary_outcome(row_results, tranche_metadata),
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
            "candidate_distance_cutoff_angstrom": 6.0,
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
        "terminal_gamma_atom_name": "PG",
        "local_metal_context": True,
        "catalytic_site_locality": True,
        "source_free_acceptor_role_features": True,
        "source_free_acceptor_role_policy_id": "role_policy_v0",
        "same_structure_co_materialization": True,
        "nearest_gamma_acceptor_distance_angstrom": 3.0,
        "expected_frozen_policy_decision": "review_only_nonabstaining_candidate",
    }
    blocked_adp = dict(
        passing_row,
        row_id="adp",
        ligand_code_from_structure="ADP",
        expected_frozen_policy_decision="review_only_abstain_adp_context",
    )
    far_distance = dict(
        passing_row,
        row_id="far",
        nearest_gamma_acceptor_distance_angstrom=6.001,
        expected_frozen_policy_decision="review_only_abstain_distance_cutoff",
    )
    forbidden = dict(
        passing_row,
        row_id="forbidden",
        source_review_used_for_predictive_feature=True,
        expected_frozen_policy_decision="review_only_abstain_forbidden_context",
    )
    source_validation_leak = dict(
        passing_row,
        row_id="source_validation_leak",
        source_validation_used_for_predictive_feature=True,
        expected_frozen_policy_decision="review_only_abstain_forbidden_context",
    )
    passing_result = evaluate_row(policy, passing_row)
    assert passing_result["decision"] == "review_only_nonabstaining_candidate"
    assert passing_result["expected_frozen_policy_match"] is True
    assert evaluate_row(policy, blocked_adp)["decision"] == "review_only_abstain"
    far_result = evaluate_row(policy, far_distance)
    assert far_result["decision"] == "review_only_abstain"
    assert "nearest_gamma_acceptor_distance_above_frozen_cutoff" in far_result[
        "abstention_reasons"
    ]
    assert far_result["expected_frozen_policy_match"] is True
    forbidden_result = evaluate_row(policy, forbidden)
    assert forbidden_result["decision"] == "review_only_abstain"
    assert "source_review_used_for_predictive_feature" in forbidden_result[
        "forbidden_predictive_context_flags"
    ]
    source_validation_leak_result = evaluate_row(policy, source_validation_leak)
    assert source_validation_leak_result["decision"] == "review_only_abstain"
    assert "source_validation_used_for_predictive_feature" in source_validation_leak_result[
        "forbidden_predictive_context_flags"
    ]
    result = evaluate_tranche(
        policy,
        {
            "metadata": {"review_only": True, "row_count": 4},
            "rows": [
                passing_row,
                blocked_adp,
                far_distance,
                forbidden,
            ],
        },
    )
    assert result["metadata"]["expected_decision_mismatch_count"] == 0
    mismatch = dict(
        passing_row,
        row_id="mismatch",
        expected_frozen_policy_decision="review_only_abstain_expected_mismatch",
    )
    mismatch_result = evaluate_tranche(
        policy,
        {
            "metadata": {"review_only": True, "row_count": 1},
            "rows": [mismatch],
        },
    )
    assert mismatch_result["metadata"]["expected_decision_mismatch_count"] == 1
    assert mismatch_result["metadata"]["primary_outcome"] == "policy_falsified"
    phase_result = evaluate_tranche(
        policy,
        {
            "metadata": {
                "review_only": True,
                "row_count": 1,
                "search_surface_exhausted": True,
                "search_surface_candidate_count_reviewed": 1,
                "nonconfounded_candidate_count_within_cutoff": 0,
                "source_artifacts": ["artifacts/search_surface_self_test.json"],
                "source_validation_phase_contract": {
                    "candidate_ids_frozen_before_local_feature_review": True,
                    "source_free_local_features_computed_before_source_validation": True,
                    "source_validation_applied_after_local_features": True,
                    "source_validation_review_only": True,
                },
            },
            "rows": [blocked_adp],
        },
    )
    assert phase_result["metadata"]["primary_outcome"] == "search_surface_exhausted"
    assert phase_result["metadata"]["search_surface_exhausted"] is True
    assert phase_result["metadata"]["primary_outcome"] in PRIMARY_OUTCOMES
    terminal_gamma_result = evaluate_tranche(
        policy,
        {
            "metadata": {
                "review_only": True,
                "row_count": 1,
                "terminal_gamma_required_for_tranche": True,
                "terminal_gamma_atom_name_required": "PG",
                "terminal_gamma_candidate_count_reviewed": 1,
            },
            "rows": [passing_row],
        },
    )
    assert terminal_gamma_result["metadata"]["terminal_gamma_required_for_tranche"] is True
    topology_row = dict(
        passing_row,
        row_id="topology_cross_chain_without_role",
        row_role="fresh_atp_nonconfounded_folded_role_identity_lead_review_only",
        source_free_acceptor_role_features=False,
        source_free_acceptor_role_policy_id=None,
        same_structure_co_materialization=False,
        topology_ambiguity_status="cross_auth_chain_candidate_distance_5.0A",
        expected_frozen_policy_decision="review_only_abstain_missing_source_free_acceptor_role",
    )
    topology_result = evaluate_tranche(
        policy,
        {
            "metadata": {
                "review_only": True,
                "row_count": 1,
                "topology_review_contract": {
                    "topology_status_required": True,
                    "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                },
            },
            "rows": [topology_row],
        },
    )
    assert topology_result["metadata"]["topology_review_contract_enforced"] is True
    sibling_lead = dict(
        topology_row,
        row_id="sibling_lead",
        sibling_pair_id="pair_self_test",
        sibling_pair_role="geometry_lead",
        sibling_matching_features=[
            "ligand_code_from_structure",
            "terminal_gamma_atom_name",
            "local_metal_context",
            "nearest_gamma_acceptor_distance_angstrom",
        ],
        sibling_counterfamily_context=False,
    )
    sibling_control = dict(
        topology_row,
        row_id="sibling_control",
        row_role="fresh_atp_sibling_topology_control_review_only",
        sibling_pair_id="pair_self_test",
        sibling_pair_role="sibling_control",
        sibling_matching_features=[
            "ligand_code_from_structure",
            "terminal_gamma_atom_name",
            "local_metal_context",
            "nearest_gamma_acceptor_distance_angstrom",
        ],
        sibling_counterfamily_context=True,
        sibling_control_match_status="matched_source_free_topology_control",
        topology_ambiguity_status="same_auth_chain_best_acceptor_cross_chain_distance_7.0A",
        expected_frozen_policy_decision="review_only_abstain_sibling_control_context",
    )
    sibling_result = evaluate_tranche(
        policy,
        {
            "metadata": {
                "review_only": True,
                "row_count": 2,
                "sibling_control_contract": {
                    "lead_control_pairing_frozen_before_evaluation": True,
                    "pairing_uses_source_free_local_features_only": True,
                    "sibling_control_context_review_only": True,
                    "lead_and_control_expected_abstention": True,
                    "matched_pair_count": 1,
                    "source_free_matching_features": [
                        "ligand_code_from_structure",
                        "terminal_gamma_atom_name",
                        "local_metal_context",
                        "nearest_gamma_acceptor_distance_angstrom",
                    ],
                },
                "source_surface_query_contexts_review_only": [
                    {
                        "artifact": "artifacts/search_surface_self_test.json",
                        "query": "full_text AMP-PNP self test",
                        "query_mode": "full_text",
                        "ligand_code": "ANP",
                        "chem_comp_id": "ANP",
                        "review_only": True,
                    }
                ],
                "query_context_review_only_contract": {
                    "source_queries_review_only": True,
                    "query_text_not_matching_feature": True,
                    "coordinate_ligand_code_required": True,
                },
            },
            "rows": [sibling_lead, sibling_control],
        },
    )
    assert sibling_result["metadata"]["sibling_control_contract_enforced"] is True
    assert (
        sibling_result["metadata"]["query_context_review_only_contract_enforced"] is True
    )
    materialized_row = dict(
        passing_row,
        row_id="materialized_anp",
        ligand_code_from_structure="ANP",
        coordinate_ligand_materialized_from_structure=True,
        coordinate_ligand_code_source="mmcif_atom_site_auth_or_label_comp_id",
        query_ligand_synonym_used_as_coordinate_ligand=False,
        post_hoc_ligand_alias_expansion=False,
    )
    materialization_tranche = {
        "metadata": {
            "review_only": True,
            "row_count": 1,
            "source_surface_query_contexts_review_only": [
                {
                    "artifact": "artifacts/materialization_guard_self_test.json",
                    "query": "full_text AMP-PNP self test",
                    "query_mode": "full_text",
                    "query_ligand_synonyms_review_only": ["AMP-PNP", "AMPPNP"],
                    "coordinate_ligand_codes_observed": ["ANP", "XYZ"],
                    "review_only": True,
                }
            ],
            "coordinate_ligand_codes_observed": ["ANP", "XYZ"],
            "alias_map_blockers_review_only": ["XYZ"],
            "coordinate_ligand_materialization_guard": {
                "coordinate_ligand_codes_inventoried_before_local_feature_review": True,
                "query_synonyms_review_only": True,
                "post_hoc_ligand_alias_expansion_forbidden": True,
                "terminal_gamma_rows_limited_to_pre_frozen_coordinate_codes": True,
                "non_prefrozen_materializations_recorded_as_review_only_blockers": True,
                "pre_frozen_coordinate_ligand_codes": ["ANP", "ATP"],
                "query_ligand_synonyms_review_only": ["AMP-PNP", "AMPPNP"],
            },
        },
        "rows": [materialized_row],
    }
    materialization_result = evaluate_tranche(policy, materialization_tranche)
    assert (
        materialization_result["metadata"][
            "coordinate_ligand_materialization_guard_enforced"
        ]
        is True
    )
    bad_materialization_overlap = json.loads(json.dumps(materialization_tranche))
    bad_materialization_overlap["metadata"]["coordinate_ligand_materialization_guard"][
        "query_ligand_synonyms_review_only"
    ] = ["AMP-PNP", "ANP"]
    try:
        evaluate_tranche(policy, bad_materialization_overlap)
    except ValueError as error:
        assert "outside the pre-frozen coordinate code set" in str(error)
    else:
        raise AssertionError("query synonyms cannot overlap coordinate codes")
    bad_materialization_blocker = json.loads(json.dumps(materialization_tranche))
    bad_materialization_blocker["metadata"]["alias_map_blockers_review_only"] = [
        "ANP",
        "XYZ",
    ]
    try:
        evaluate_tranche(policy, bad_materialization_blocker)
    except ValueError as error:
        assert "blockers to stay outside" in str(error)
    else:
        raise AssertionError("materialization blockers cannot overlap coordinate codes")
    bad_materialization_prefrozen = json.loads(json.dumps(materialization_tranche))
    bad_materialization_prefrozen["metadata"]["coordinate_ligand_materialization_guard"][
        "pre_frozen_coordinate_ligand_codes"
    ] = ["ANP", "GTP"]
    try:
        evaluate_tranche(policy, bad_materialization_prefrozen)
    except ValueError as error:
        assert "frozen policy ligand map" in str(error)
    else:
        raise AssertionError("pre-frozen coordinate codes must be policy-declared")
    bad_sibling_control = dict(
        sibling_control,
        row_id="bad_sibling_control",
        sibling_pair_id="pair_without_lead",
    )
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "sibling_control_contract": {
                        "lead_control_pairing_frozen_before_evaluation": True,
                        "pairing_uses_source_free_local_features_only": True,
                        "sibling_control_context_review_only": True,
                        "lead_and_control_expected_abstention": True,
                        "matched_pair_count": 1,
                        "source_free_matching_features": ["structure_title"],
                    },
                },
                "rows": [bad_sibling_control],
            },
        )
    except ValueError as error:
        assert "sibling control" in str(error)
    else:
        raise AssertionError("sibling-control source-derived matching must fail validation")
    bad_query_context = {
        "metadata": {
            "review_only": True,
            "row_count": 1,
            "source_surface_query_contexts_review_only": [
                {
                    "artifact": "artifacts/search_surface_self_test.json",
                    "query": "full_text AMP-PNP self test",
                    "query_mode": "full_text",
                    "ligand_code": "ANP",
                    "chem_comp_id": "ANP",
                    "review_only": False,
                }
            ],
            "query_context_review_only_contract": {
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
            },
        },
        "rows": [passing_row],
    }
    try:
        evaluate_tranche(policy, bad_query_context)
    except ValueError as error:
        assert "query context review-only contract" in str(error)
    else:
        raise AssertionError("query contexts must stay review-only")
    bad_materialization_row = dict(
        materialized_row,
        row_id="bad_query_synonym_materialization",
        ligand_code_from_structure="AMP-PNP",
        query_ligand_synonym_used_as_coordinate_ligand=True,
    )
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "source_surface_query_contexts_review_only": [
                        {
                            "artifact": "artifacts/materialization_guard_self_test.json",
                            "query": "full_text AMP-PNP self test",
                            "query_mode": "full_text",
                            "query_ligand_synonyms_review_only": ["AMP-PNP"],
                            "coordinate_ligand_codes_observed": ["ANP"],
                            "review_only": True,
                        }
                    ],
                    "coordinate_ligand_codes_observed": ["ANP"],
                    "alias_map_blockers_review_only": [],
                    "coordinate_ligand_materialization_guard": {
                        "coordinate_ligand_codes_inventoried_before_local_feature_review": True,
                        "query_synonyms_review_only": True,
                        "post_hoc_ligand_alias_expansion_forbidden": True,
                        "terminal_gamma_rows_limited_to_pre_frozen_coordinate_codes": True,
                        "non_prefrozen_materializations_recorded_as_review_only_blockers": True,
                        "pre_frozen_coordinate_ligand_codes": ["ANP", "ATP"],
                        "query_ligand_synonyms_review_only": ["AMP-PNP"],
                    },
                },
                "rows": [bad_materialization_row],
            },
        )
    except ValueError as error:
        assert "coordinate ligand materialization guard" in str(error)
    else:
        raise AssertionError("query synonym coordinate materialization must fail validation")
    bad_topology_row = dict(
        topology_row,
        row_id="bad_topology",
        same_structure_co_materialization=True,
    )
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "topology_review_contract": {
                        "topology_status_required": True,
                        "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                    },
                },
                "rows": [bad_topology_row],
            },
        )
    except ValueError as error:
        assert "topology review contract" in str(error)
    else:
        raise AssertionError("cross-chain geometry cannot co-materialize without role features")
    missing_terminal_gamma = dict(
        passing_row,
        row_id="missing_terminal_gamma",
        terminal_gamma_equivalent_geometry=False,
        terminal_gamma_atom_name=None,
    )
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "terminal_gamma_required_for_tranche": True,
                    "terminal_gamma_atom_name_required": "PG",
                    "terminal_gamma_candidate_count_reviewed": 1,
                },
                "rows": [missing_terminal_gamma],
            },
        )
    except ValueError as error:
        assert "terminal-gamma tranche contract" in str(error)
    else:
        raise AssertionError("missing terminal gamma must fail validation")
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "search_surface_exhausted": True,
                    "source_artifacts": ["artifacts/search_surface_self_test.json"],
                },
                "rows": [blocked_adp],
            },
        )
    except ValueError as error:
        assert "search_surface_candidate_count_reviewed" in str(error)
    else:
        raise AssertionError("missing search-surface counts must fail validation")
    leaking_row = dict(blocked_adp, source_validation_used_for_predictive_feature=True)
    try:
        evaluate_tranche(
            policy,
            {
                "metadata": {
                    "review_only": True,
                    "row_count": 1,
                    "source_validation_phase_contract": {
                        "candidate_ids_frozen_before_local_feature_review": True,
                        "source_free_local_features_computed_before_source_validation": True,
                        "source_validation_applied_after_local_features": True,
                        "source_validation_review_only": True,
                    },
                },
                "rows": [leaking_row],
            },
        )
    except ValueError as error:
        assert "violates source validation phase contract" in str(error)
    else:
        raise AssertionError("source-validation leakage must fail validation")


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
    result["metadata"]["policy_sha256"] = sha256_file(args.policy)
    result["metadata"]["tranche_sha256"] = sha256_file(args.tranche)
    write_json(args.output, result, pretty=args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
