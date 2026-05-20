#!/usr/bin/env python3
"""Review-only ePK false-negative state/topology decision probe.

This lane-local helper classifies the remaining source-free ePK substrate-role
identity misses by phosphotransfer-state availability and topology ambiguity.
It reuses compact reduced evidence from the active-site orientation probe and
writes no raw coordinate data.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_false_negative_state_topology_decision_probe_v1_20260520"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_active_site_orientation_asymmetry_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_false_negative_state_topology_decision_probe_v1_20260520.json"
)


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    return payload["diagnostic_rows"]


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def feature_dict(row: dict[str, Any]) -> dict[str, Any]:
    return row["structure_features"]


def orientation_class(candidate: dict[str, Any] | None) -> str | None:
    if not candidate:
        return None
    return candidate.get("active_site_orientation_features", {}).get("orientation_support_class")


def auth_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return features.get("nearest_strict_auth_terminal_guard_candidate")


def strict_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return features.get("nearest_strict_cross_chain_candidate")


def reciprocal_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return features.get("nearest_reciprocal_folded_tyr_rescue_candidate")


def candidates(features: dict[str, Any]) -> list[dict[str, Any]]:
    return features.get("orientation_enriched_candidates_within_8a", [])


def same_chain_candidates_within(features: dict[str, Any], distance_cutoff: float) -> list[dict[str, Any]]:
    return [
        candidate
        for candidate in candidates(features)
        if candidate.get("same_chain_topology")
        and candidate.get("distance_angstrom") is not None
        and candidate["distance_angstrom"] <= distance_cutoff
    ]


def compact_atom(atom: dict[str, Any] | None) -> dict[str, Any] | None:
    if not atom:
        return None
    return {
        "atom_name": atom.get("atom_name"),
        "residue_code": atom.get("residue_code"),
        "chain_id": atom.get("chain_id"),
        "auth_seq_id": atom.get("auth_seq_id"),
        "icode": atom.get("icode"),
    }


def compact_candidate(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    if not candidate:
        return None
    orientation = candidate.get("active_site_orientation_features", {})
    exposure = candidate.get("local_exposure_features", {})
    return {
        "distance_angstrom": candidate.get("distance_angstrom"),
        "terminal_gamma_ligand_chain": candidate.get("terminal_gamma_ligand_chain"),
        "candidate_acceptor_chain": candidate.get("candidate_acceptor_chain"),
        "candidate_acceptor_residue_code": candidate.get("candidate_acceptor_residue_code"),
        "candidate_acceptor_auth_seq_id_int": candidate.get("candidate_acceptor_auth_seq_id_int"),
        "candidate_acceptor_residue_ordinal_in_chain": candidate.get(
            "candidate_acceptor_residue_ordinal_in_chain"
        ),
        "candidate_acceptor_chain_length": candidate.get("candidate_acceptor_chain_length"),
        "candidate_acceptor_chain_is_short_peptide_like": candidate.get(
            "candidate_acceptor_chain_is_short_peptide_like"
        ),
        "candidate_acceptor_chain_is_folded_like": candidate.get(
            "candidate_acceptor_chain_is_folded_like"
        ),
        "candidate_acceptor_is_tyr": candidate.get("candidate_acceptor_is_tyr"),
        "candidate_resolved_n_terminal_internal_fragment_like": candidate.get(
            "candidate_resolved_n_terminal_internal_fragment_like"
        ),
        "same_chain_topology": candidate.get("same_chain_topology"),
        "cross_chain_topology": candidate.get("cross_chain_topology"),
        "ligand_acceptor_same_sequence_entity": candidate.get("ligand_acceptor_same_sequence_entity"),
        "candidate_chain_active_gamma_count": candidate.get("candidate_chain_active_gamma_count"),
        "candidate_chain_nucleotide_or_metal_residue_count": candidate.get(
            "candidate_chain_nucleotide_or_metal_residue_count"
        ),
        "reciprocal_context_class": candidate.get("reciprocal_context_class"),
        "orientation_support_class": orientation.get("orientation_support_class"),
        "gamma_to_hydroxyl_distance_angstrom": orientation.get("gamma_to_hydroxyl_distance_angstrom"),
        "hydroxyl_anchor_to_gamma_angle_degrees": orientation.get(
            "hydroxyl_anchor_to_gamma_angle_degrees"
        ),
        "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a": orientation.get(
            "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a_excluding_same_residue"
        ),
        "gamma_site_ligand_chain_heavy_atom_count_within_6a": orientation.get(
            "gamma_site_ligand_chain_heavy_atom_count_within_6a"
        ),
        "local_exposure_profile_class": exposure.get("local_exposure_profile_class"),
        "nearest_protein_hydroxyl_atom": compact_atom(candidate.get("nearest_protein_hydroxyl_atom")),
        "terminal_gamma_equivalent_atom": compact_atom(candidate.get("terminal_gamma_equivalent_atom")),
    }


def selected_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return reciprocal_candidate(features) or auth_candidate(features) or strict_candidate(features)


def availability_class(row: dict[str, Any]) -> str:
    features = feature_dict(row)
    if not features.get("terminal_gamma_equivalent_atom_available"):
        if str(features.get("ligand_state", "")).startswith("nucleotide_like_without_terminal_gamma"):
            return "phosphotransfer_gamma_unavailable_product_or_adp_state"
        return "phosphotransfer_gamma_unavailable_unknown_state"
    if auth_candidate(features):
        return "claimable_by_auth_guard_strict_context"
    strict = strict_candidate(features)
    if strict and strict.get("candidate_resolved_n_terminal_internal_fragment_like"):
        return "blocked_internal_fragment_n_terminal_mimic"
    reciprocal = reciprocal_candidate(features)
    if reciprocal:
        return "ambiguous_reciprocal_folded_tyr_context"
    same_chain_near = same_chain_candidates_within(features, 6.0)
    if same_chain_near:
        return "ambiguous_same_chain_autophosphorylation_like_context"
    if candidates(features):
        return "hydroxyl_near_gamma_but_no_claimable_identity_context"
    return "terminal_gamma_available_but_no_near_hydroxyl_candidate"


def false_negative_failure_class(row: dict[str, Any]) -> str:
    features = feature_dict(row)
    cls = availability_class(row)
    if cls.startswith("phosphotransfer_gamma_unavailable"):
        return "missing_ligand_terminal_gamma_or_product_state"
    if cls == "ambiguous_same_chain_autophosphorylation_like_context":
        return "same_chain_or_autophosphorylation_like_topology"
    if cls == "ambiguous_reciprocal_folded_tyr_context":
        return "reciprocal_folded_chain_topology_ambiguity"
    if not candidates(features):
        return "no_resolved_candidate_geometry"
    return "source_free_method_weakness_or_unmodeled_context"


def row_summary(row: dict[str, Any]) -> dict[str, Any]:
    features = feature_dict(row)
    nearest_same_chain = same_chain_candidates_within(features, 8.0)
    nearest_same_chain = nearest_same_chain[0] if nearest_same_chain else None
    return {
        "pdb_id": row["pdb_id"],
        "evaluation_label": row["evaluation_label"],
        "evaluation_group": row["evaluation_group"],
        "availability_class": availability_class(row),
        "ligand_state": features.get("ligand_state"),
        "terminal_gamma_equivalent_atom_available": features.get(
            "terminal_gamma_equivalent_atom_available"
        ),
        "nearest_protein_hydroxyl_distance_angstrom": features.get(
            "nearest_protein_hydroxyl_distance_angstrom"
        ),
        "candidate_count_within_8a": len(candidates(features)),
        "polymer_chain_count": features.get("polymer_chain_count"),
        "polymer_entity_count_sequence_proxy": features.get("polymer_entity_count_sequence_proxy"),
        "selected_claim_or_ambiguity_candidate": compact_candidate(selected_candidate(features)),
        "nearest_same_chain_candidate": compact_candidate(nearest_same_chain),
    }


RuleFn = Callable[[dict[str, Any]], bool]


def rule_auth_guard(row: dict[str, Any]) -> bool:
    return bool(auth_candidate(feature_dict(row)))


def rule_reciprocal_folded_tyr(row: dict[str, Any]) -> bool:
    features = feature_dict(row)
    return bool(auth_candidate(features) or reciprocal_candidate(features))


def rule_orientation_supported_reciprocal_folded_tyr(row: dict[str, Any]) -> bool:
    features = feature_dict(row)
    reciprocal = reciprocal_candidate(features)
    return bool(
        auth_candidate(features)
        or (reciprocal and orientation_class(reciprocal) == "gamma_facing_active_site_like")
    )


def rule_auth_or_same_chain_5a(row: dict[str, Any]) -> bool:
    features = feature_dict(row)
    return bool(auth_candidate(features) or same_chain_candidates_within(features, 5.0))


def rule_auth_or_same_chain_6a(row: dict[str, Any]) -> bool:
    features = feature_dict(row)
    return bool(auth_candidate(features) or same_chain_candidates_within(features, 6.0))


RULES: dict[str, dict[str, Any]] = {
    "strict_auth_terminal_guard_v1_reused": {
        "description": (
            "Existing source-free auth-terminal guarded strict context; included as the "
            "zero-false-positive no-claim baseline."
        ),
        "function": rule_auth_guard,
    },
    "reciprocal_folded_tyr_admitted_v1_reused": {
        "description": (
            "Auth-guard strict positives plus folded cross-chain Tyr reciprocal context. "
            "This admits the same topology class as 9UW4."
        ),
        "function": rule_reciprocal_folded_tyr,
    },
    "orientation_supported_folded_tyr_v1_reused": {
        "description": (
            "Auth-guard strict positives plus folded Tyr reciprocal candidates with the "
            "frozen gamma-facing orientation class."
        ),
        "function": rule_orientation_supported_reciprocal_folded_tyr,
    },
    "auth_or_same_chain_candidate_5a_probe": {
        "description": (
            "Stress test: auth-guard strict positives plus any same-chain hydroxyl within "
            "5 A of terminal gamma. This probes whether same-chain/autophosphorylation-like "
            "misses can be admitted by source-free geometry."
        ),
        "function": rule_auth_or_same_chain_5a,
    },
    "auth_or_same_chain_candidate_6a_probe": {
        "description": (
            "Stress test: auth-guard strict positives plus any same-chain hydroxyl within "
            "6 A of terminal gamma. This mirrors the permissive distance radius for the "
            "same-chain topology family."
        ),
        "function": rule_auth_or_same_chain_6a,
    },
}


def failure_mode(row: dict[str, Any], predicted_positive: bool, rule_id: str) -> str | None:
    actual_positive = is_positive(row)
    if predicted_positive == actual_positive:
        return None
    if actual_positive:
        return false_negative_failure_class(row)

    features = feature_dict(row)
    if rule_id in {
        "reciprocal_folded_tyr_admitted_v1_reused",
        "orientation_supported_folded_tyr_v1_reused",
    } and reciprocal_candidate(features):
        return "folded_tyr_topology_counterexample"
    if rule_id.startswith("auth_or_same_chain") and same_chain_candidates_within(features, 6.0):
        return "same_chain_nearest_hydroxyl_role_ambiguity"
    strict = strict_candidate(features)
    if strict and strict.get("candidate_resolved_n_terminal_internal_fragment_like"):
        return "internal_fragment_n_terminal_mimicry"
    if features.get("nearest_protein_hydroxyl_distance_angstrom") is not None:
        return "nearest_hydroxyl_role_ambiguity"
    return "biological_role_ambiguity"


def confusion_for_rule(rows: list[dict[str, Any]], rule_id: str, rule_spec: dict[str, Any]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    failures: Counter[str] = Counter()
    decisions = []
    rule_fn: RuleFn = rule_spec["function"]
    for row in rows:
        predicted_positive = bool(rule_fn(row))
        actual_positive = is_positive(row)
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        mode = failure_mode(row, predicted_positive, rule_id)
        if mode:
            failures[mode] += 1
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "failure_mode": mode,
                "availability_class": availability_class(row),
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": rule_spec["description"],
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": buckets,
        "failure_mode_counts": dict(sorted(failures.items())),
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
    }


def compact_rule_results(rule_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        result["rule_id"]: {
            "confusion_matrix": result["confusion_matrix"],
            "pdb_ids_by_outcome": result["pdb_ids_by_outcome"],
            "failure_mode_counts": result["failure_mode_counts"],
            "clears_diagnostic_tranche": result["clears_diagnostic_tranche"],
        }
        for result in rule_results
    }


def false_negative_probe(rows: list[dict[str, Any]], false_negative_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {row["pdb_id"]: row for row in rows}
    return [
        {
            **row_summary(by_id[pdb_id]),
            "false_negative_failure_class": false_negative_failure_class(by_id[pdb_id]),
        }
        for pdb_id in false_negative_ids
    ]


def availability_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label: dict[str, Counter[str]] = {"positive": Counter(), "counterexample": Counter()}
    for row in rows:
        key = "positive" if is_positive(row) else "counterexample"
        by_label[key][availability_class(row)] += 1
    return {key: dict(sorted(counter.items())) for key, counter in by_label.items()}


def select_primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    same_chain_5 = next(
        result for result in rule_results if result["rule_id"] == "auth_or_same_chain_candidate_5a_probe"
    )
    reciprocal = next(
        result
        for result in rule_results
        if result["rule_id"] == "orientation_supported_folded_tyr_v1_reused"
    )
    if reciprocal["pdb_ids_by_outcome"]["false_positive"] or same_chain_5["pdb_ids_by_outcome"][
        "false_positive"
    ]:
        return "blocker_not_cleared_biology_ambiguity"
    return "blocker_not_cleared_method_weakness"


def build_payload(workflow_started_at: str, ledger_started_at: str | None = None) -> dict[str, Any]:
    rows = load_rows()
    rule_results = [confusion_for_rule(rows, rule_id, spec) for rule_id, spec in RULES.items()]
    primary_outcome = select_primary_outcome(rule_results)
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")
    auth = next(result for result in rule_results if result["rule_id"] == "strict_auth_terminal_guard_v1_reused")
    reciprocal = next(
        result
        for result in rule_results
        if result["rule_id"] == "orientation_supported_folded_tyr_v1_reused"
    )
    same_chain_5 = next(
        result for result in rule_results if result["rule_id"] == "auth_or_same_chain_candidate_5a_probe"
    )
    same_chain_6 = next(
        result for result in rule_results if result["rule_id"] == "auth_or_same_chain_candidate_6a_probe"
    )
    ended_at = utc_now()
    started_for_measure = ledger_started_at or workflow_started_at
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_for_measure)).total_seconds() / 60.0, 2)

    strict_auth_fn_ids = auth["pdb_ids_by_outcome"]["false_negative"]
    orientation_remaining_fn_ids = reciprocal["pdb_ids_by_outcome"]["false_negative"]
    availability_counts = availability_summary(rows)
    diagnostic_rows = [row_summary(row) for row in rows]
    source_free_features = [
        "terminal gamma-equivalent availability from ligand atom identity",
        "nucleotide-like ligand state class without title/source text",
        "candidate count within 8 A of terminal gamma",
        "same-chain versus cross-chain hydroxyl/gamma topology",
        "same-sequence entity proxy from resolved chain residue-name hashes",
        "candidate-chain nucleotide or active-gamma occupancy",
        "frozen availability_class taxonomy",
        "same-chain 5 A and 6 A rescue stress rules",
    ]
    false_positive_ids = sorted(
        {
            pdb_id
            for result in rule_results
            for pdb_id in result["pdb_ids_by_outcome"]["false_positive"]
        }
    )
    false_negative_ids = sorted(
        {
            pdb_id
            for result in rule_results
            for pdb_id in result["pdb_ids_by_outcome"]["false_negative"]
        }
    )

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_false_negative_state_topology_decision_probe",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifact": str(SOURCE_ARTIFACT),
            "frozen_row_count": len(rows),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": (
            "If the remaining ePK substrate-role blocker is clearable from structure alone, "
            "then source-free phosphotransfer-state availability and same-chain/topology "
            "classes should either recover the remaining positives without admitting "
            "counterexamples, or cleanly classify the unresolved cases as outside the "
            "reachable evidence state."
        ),
        "feature_definitions": {
            "availability_class": (
                "Frozen source-free taxonomy derived only from ligand terminal-gamma "
                "availability, candidate distance/topology, reciprocal chain context, "
                "and resolved-chain entity proxies."
            ),
            "phosphotransfer_gamma_unavailable_product_or_adp_state": (
                "The compact structure features report a nucleotide-like ligand without a "
                "terminal gamma-equivalent atom, so gamma-to-hydroxyl identity geometry is "
                "unavailable in the resolved state."
            ),
            "ambiguous_same_chain_autophosphorylation_like_context": (
                "A same-chain hydroxyl is close to a terminal gamma in a folded chain; "
                "geometry alone does not decide catalytic-chain self context versus a true "
                "substrate-role acceptor."
            ),
            "ambiguous_reciprocal_folded_tyr_context": (
                "A folded cross-chain Tyr candidate has reciprocal active-site context. "
                "Admitting this class recovers 9UUR/9UUX but also admits 9UW4."
            ),
        },
        "diagnostic_rows": diagnostic_rows,
        "availability_summary_by_label": availability_counts,
        "rules": rule_results,
        "strict_auth_false_negative_probe": false_negative_probe(rows, strict_auth_fn_ids),
        "orientation_supported_remaining_false_negative_probe": false_negative_probe(
            rows, orientation_remaining_fn_ids
        ),
        "same_chain_rescue_stress": {
            "auth_or_same_chain_candidate_5a_probe": {
                "confusion_matrix": same_chain_5["confusion_matrix"],
                "false_positives": same_chain_5["pdb_ids_by_outcome"]["false_positive"],
                "false_negatives": same_chain_5["pdb_ids_by_outcome"]["false_negative"],
                "interpretation": (
                    "A 5 A same-chain rescue recovers 3TM0 and row-level positives with "
                    "near same-chain alternatives, but it admits many counterexamples and "
                    "therefore is not a substrate-role identity rule."
                ),
            },
            "auth_or_same_chain_candidate_6a_probe": {
                "confusion_matrix": same_chain_6["confusion_matrix"],
                "false_positives": same_chain_6["pdb_ids_by_outcome"]["false_positive"],
                "false_negatives": same_chain_6["pdb_ids_by_outcome"]["false_negative"],
                "interpretation": (
                    "At the permissive 6 A radius the same-chain rule collapses toward "
                    "nearest-hydroxyl behavior and produces broad role ambiguity."
                ),
            },
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": (
                "The blocker is not cleared: the remaining misses split into unavailable "
                "product/ADP state, reciprocal folded-chain topology shared by 9UW4, and "
                "same-chain/autophosphorylation-like topology that floods with false "
                "positives when admitted source-free."
            ),
            "historical_comparator_assessment": (
                "Within this lane, comparable ePK substrate-role blockers have not been "
                "cleared by structure-only nearest-atom, terminal-index, reciprocal-context, "
                "local-exposure, active-site-orientation, or state/topology proxies. The "
                "source-free features are useful for review triage, but source-reviewed "
                "adjudication remains required for production identity claims."
            ),
            "stop_feature_probing_decision": (
                "Stop broad scalar feature probing unless new source-free evidence modality "
                "is introduced. The current compact structure features define review-only "
                "ambiguity classes rather than a production identity rule."
            ),
        },
        "run_record": {
            "lane_id": LANE_ID,
            "started_at": started_for_measure,
            "ended_at": ended_at,
            "measured_minutes": measured_minutes,
            "hypothesis": (
                "Source-free phosphotransfer-state availability and chain topology can "
                "classify the remaining misses and determine whether the blocker is "
                "clearable without source-reviewed adjudication."
            ),
            "diagnostic_rows_added_or_reused": {
                "reused_from_active_site_orientation_probe": len(rows),
                "added_this_run": [],
                "total": len(rows),
            },
            "source_free_features_tested": source_free_features,
            "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
            "rule_results": compact_rule_results(rule_results),
            "confusion_matrix": reciprocal["confusion_matrix"],
            "decisive_counterexamples": {
                "false_positive_ids_seen_across_rules": false_positive_ids,
                "false_negative_ids_seen_across_rules": false_negative_ids,
                "hard_reciprocal_trio": ["9UUR", "9UUX", "9UW4"],
                "same_chain_probe_counterexamples_at_5a": same_chain_5["pdb_ids_by_outcome"][
                    "false_positive"
                ],
            },
            "false_positive_analysis": {
                "strict_auth_terminal_guard_v1_reused": auth["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "orientation_supported_folded_tyr_v1_reused": reciprocal["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "auth_or_same_chain_candidate_5a_probe": same_chain_5["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "auth_or_same_chain_candidate_6a_probe": same_chain_6["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "interpretation": (
                    "Avoiding false positives requires rejecting ambiguous folded reciprocal "
                    "and same-chain contexts; admitting either source-free recovers positives "
                    "only by admitting counterexamples."
                ),
            },
            "false_negative_analysis": {
                "strict_auth_terminal_guard_v1_reused": strict_auth_fn_ids,
                "orientation_supported_folded_tyr_v1_reused": orientation_remaining_fn_ids,
                "strict_auth_false_negative_classes": {
                    item["pdb_id"]: item["false_negative_failure_class"]
                    for item in false_negative_probe(rows, strict_auth_fn_ids)
                },
                "orientation_supported_remaining_false_negative_classes": {
                    item["pdb_id"]: item["false_negative_failure_class"]
                    for item in false_negative_probe(rows, orientation_remaining_fn_ids)
                },
                "interpretation": (
                    "3QHR, 3QHW, and 1L0O lack resolved terminal gamma-equivalent geometry; "
                    "3TM0 is same-chain/autophosphorylation-like; 9UUR/9UUX can be recovered "
                    "only by accepting the reciprocal folded-Tyr class that also admits 9UW4."
                ),
            },
            "blocker_classification": {
                "primary_outcome": primary_outcome,
                "classification": (
                    "Current source-free structure features do not clear ePK substrate-role "
                    "identity; they define review-only ambiguity classes."
                ),
            },
            "primary_outcome": primary_outcome,
            "next_query": (
                "Convert the lane result into a source-reviewed adjudication requirement: "
                "treat product/ADP, reciprocal folded-chain, and same-chain/autophosphorylation-like "
                "cases as review-only blockers unless a new source-free modality is introduced."
            ),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "recommendation": (
                "Do not claim ePK production readiness or tune production thresholds. Preserve "
                "source-reviewed adjudication for substrate-role identity and use these "
                "state/topology classes only as compact review evidence."
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--ledger-started-at")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    payload = build_payload(args.workflow_started_at, args.ledger_started_at)
    output_path = Path(args.output)
    write_json(output_path, payload)
    if args.append_ledger:
        append_jsonl(LEDGER_PATH, payload["run_record"])
    print(
        json.dumps(
            {
                "artifact": str(output_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "orientation_supported_confusion": payload["run_record"]["confusion_matrix"],
                "same_chain_5a_confusion": payload["same_chain_rescue_stress"][
                    "auth_or_same_chain_candidate_5a_probe"
                ]["confusion_matrix"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
