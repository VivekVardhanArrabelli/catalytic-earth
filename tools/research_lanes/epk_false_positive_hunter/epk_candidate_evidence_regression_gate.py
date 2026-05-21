#!/usr/bin/env python3
"""Emit lane-only ePK false-positive regression evidence rows.

This converter turns recent false-positive hunter artifacts into compact
`epk_candidate_evidence_v1`-style rows. It intentionally reads only lane
artifacts, writes no raw coordinates, and does not edit production registries,
fingerprints, thresholds, labels, or migrations.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


LANE_ID = "epk_false_positive_hunter"
SCHEMA_VERSION = "epk_candidate_evidence_v1"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"


SOURCE_SPECS = [
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "v4_entry_level_assembly_guard_stress_deep_20260521_015936Z.json",
        "row_key": "entry_level_guard_materializer_rows",
        "source_profile": "biological_assembly_split",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "v4_entry_level_epk_overblock_later_offset_stress_targeted_20260521_025652Z.json",
        "row_key": "custom_materializer_rows",
        "source_profile": "source_valid_epk_and_orc_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "v4_entry_level_epk_overblock_later_offset_contaminant_stress_20260521_030753Z.json",
        "row_key": "custom_materializer_rows",
        "source_profile": "epk_query_non_epk_contaminants",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "atpase_transporter_substrate_mode_stress_20260520.json",
        "row_key": "substrate_mode_hits_review_only",
        "source_profile": "atpase_transporter_topology_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "walker_a_substrate_mode_confirmation_20260520.json",
        "row_key": "substrate_mode_hits_review_only",
        "source_profile": "walker_a_topology_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "non_epk_atp_mg_enzyme_substrate_mode_stress_20260520.json",
        "row_key": "substrate_mode_hits_review_only",
        "source_profile": "non_epk_atp_mg_enzyme_topology_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "same_author_chain_entity_reuse_stress_20260520.json",
        "row_key": "actual_materializer_non_epk_same_author_chain_reuse_rows",
        "source_profile": "same_author_chain_entity_reuse_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "gamma_chain_assignment_stress_20260520.json",
        "row_key": "current_atp_like_namespace_artifact_rows_review_only",
        "source_profile": "gamma_chain_assignment_namespace_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "actual_materializer_probe_namespace_pressure_20260520.json",
        "row_key": "rows",
        "source_profile": "ligand_namespace_materialization_nohit_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "auth_label_gamma_collision_counterexample_summary_20260520_202229Z.json",
        "row_key": "counterexamples",
        "source_profile": "auth_label_gamma_collision_counterexamples",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json",
        "row_key": "custom_materializer_rows",
        "source_profile": "source_valid_epk_seed_geometry_prefilter_controls",
    },
    {
        "path": "artifacts/research_lanes/epk_false_positive_hunter/"
        "source_valid_later_offset_gap_audit_20260521_053401Z.json",
        "row_key": "custom_materializer_rows",
        "source_profile": "source_valid_epk_seed_geometry_prefilter_controls",
    },
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def boolish(value: Any) -> bool:
    return bool(value)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def intish(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def first_hit(row: dict[str, Any]) -> dict[str, Any]:
    for key in (
        "substrate_mode_materializer_hits",
        "heteromeric_candidate_hits",
        "actual_materializer_hits",
    ):
        hits = row.get(key)
        if isinstance(hits, list) and hits:
            first = hits[0]
            if isinstance(first, dict):
                return first
    for best in row.get("best_hits", []) or []:
        if not isinstance(best, dict):
            continue
        primary = best.get("primary_mode_hit")
        if isinstance(primary, dict):
            return {
                "candidate_atom_name": primary.get("atom"),
                "candidate_auth_seq_id": primary.get("auth_seq_id"),
                "candidate_chain_name": primary.get("chain"),
                "candidate_residue_code": primary.get("residue"),
                "gamma_associated_polymer_chain_name": best.get("ligand_chain"),
                "gamma_atom_name": best.get("terminal_p_atom"),
                "gamma_ligand_code": best.get("ligand"),
                "nearest_gamma_distance_angstrom": primary.get("distance_angstrom"),
                "nearest_mg_distance_angstrom": best.get(
                    "nearest_mg_distance_angstrom"
                ),
            }
    for hit in row.get("local_best_hits", []) or []:
        if isinstance(hit, dict):
            return {
                "candidate_atom_name": hit.get("candidate_atom_name"),
                "candidate_auth_seq_id": hit.get("candidate_auth_seq_id"),
                "candidate_chain_name": hit.get("candidate_chain_name")
                or hit.get("candidate_auth_chain"),
                "candidate_residue_code": hit.get("candidate_residue_code"),
                "gamma_associated_polymer_chain_name": hit.get(
                    "actual_gamma_associated_polymer_chain_name"
                )
                or hit.get("gamma_chain_name"),
                "gamma_atom_name": hit.get("terminal_p_atom"),
                "gamma_ligand_code": hit.get("ligand"),
                "nearest_gamma_distance_angstrom": hit.get("distance_angstrom"),
                "nearest_mg_distance_angstrom": hit.get(
                    "nearest_mg_distance_angstrom"
                ),
            }
    return {}


def materializer_hit_count(row: dict[str, Any]) -> int:
    for key in (
        "substrate_mode_materializer_hit_count",
        "heteromeric_candidate_hit_count",
        "substrate_mode_rule_hit_count",
        "local_atp_mg_acceptor_hit_count",
    ):
        if key in row:
            return intish(row.get(key))
    for key in (
        "substrate_mode_materializer_hits",
        "heteromeric_candidate_hits",
        "actual_materializer_hits",
    ):
        hits = row.get(key)
        if isinstance(hits, list):
            return len(hits)
    return 0


def topology_ambiguity(row: dict[str, Any]) -> bool:
    if "topology_ambiguity_counteraxis_hit" in row:
        return boolish(row.get("topology_ambiguity_counteraxis_hit"))
    if "auth_topology_ambiguity_counteraxis_hit" in row:
        return boolish(row.get("auth_topology_ambiguity_counteraxis_hit"))
    if "same_chain_topology_detected" in row:
        return boolish(row.get("same_chain_topology_detected")) or boolish(
            row.get("reciprocal_cross_chain_topology_detected")
        )
    if "auth_same_chain_topology_detected" in row:
        return boolish(row.get("auth_same_chain_topology_detected")) or boolish(
            row.get("auth_reciprocal_cross_chain_topology_detected")
        )
    topology = row.get("actual_materializer_topology")
    if isinstance(topology, dict):
        return boolish(topology.get("same_chain")) or boolish(
            topology.get("reciprocal_cross_chain")
        )
    return False


def topology_clear(row: dict[str, Any]) -> bool:
    if "topology_clear_substrate_mode_hit" in row:
        return boolish(row.get("topology_clear_substrate_mode_hit"))
    if "topology_clear_substrate_mode_hit_count" in row:
        return intish(row.get("topology_clear_substrate_mode_hit_count")) > 0
    if row.get("actual_materializer_hits"):
        return not topology_ambiguity(row)
    return materializer_hit_count(row) > 0 and not topology_ambiguity(row)


def coordinate_state(row: dict[str, Any]) -> str:
    context = str(row.get("coordinate_context") or "deposited_atom_site")
    if context.startswith("biological_assembly"):
        return "biological_assembly"
    return "deposited_atom_site"


def is_non_epk(row: dict[str, Any], profile: str) -> bool:
    if row.get("known_epk_positive_input"):
        return False
    if row.get("probable_epk_from_context") and not row.get(
        "non_epk_for_counterexample_review"
    ):
        return False
    if profile in {
        "source_valid_epk_and_orc_controls",
    } and row.get("source_context_epk_review_candidate"):
        return False
    if (
        profile == "source_valid_epk_seed_geometry_prefilter_controls"
        and row.get("source_valid_epk_seed_review_candidate")
    ):
        return False
    return True


def control_class(row: dict[str, Any], profile: str) -> str:
    context = str(row.get("coordinate_context") or "deposited_atom_site")
    role_tokens = row.get("deposited_orc_mcm_role_tokens") or []
    groups = row.get("query_surface_groups") or []
    if profile == "biological_assembly_split":
        if row.get("known_epk_positive_input"):
            return "source_valid_epk_positive_overblock_control"
        if row.get("known_orc_counterexample_input") or role_tokens:
            if context.startswith("biological_assembly"):
                return "orc_mcm_biological_assembly_split_control"
            return "orc_mcm_deposited_coordinate_control"
        if "non_orc_aaa_atpase_component_text" in groups:
            return "atpase_biological_assembly_split_control"
        return "biological_assembly_split_control"
    if profile == "source_valid_epk_and_orc_controls":
        if row.get("source_context_epk_review_candidate"):
            return "source_valid_epk_entry_guard_overblock_control"
        if row.get("known_orc_counterexample_input") or role_tokens:
            return "orc_mcm_fixed_counterexample_control"
        if row.get("non_orc_atpase_later_offset_review_candidate"):
            return "later_offset_atpase_split_control"
        return "entry_level_guard_control"
    if profile == "epk_query_non_epk_contaminants":
        return "ligand_materialization_non_epk_contaminant_control"
    if profile == "source_valid_epk_seed_geometry_prefilter_controls":
        if row.get("source_valid_epk_seed_review_candidate"):
            return "source_valid_epk_entity_seed_overblock_control"
        if row.get("non_epk_v4_contaminant_prefilter_candidate"):
            return "geometry_prefiltered_non_epk_v4_contaminant_control"
        if row.get("known_orc_counterexample_input") or role_tokens:
            return "orc_mcm_fixed_counterexample_control"
        return "source_valid_geometry_prefilter_stress_control"
    if profile == "atpase_transporter_topology_controls":
        return "atpase_transporter_topology_control"
    if profile == "walker_a_topology_controls":
        return "walker_a_internal_fragment_topology_control"
    if profile == "non_epk_atp_mg_enzyme_topology_controls":
        return "non_epk_atp_mg_enzyme_topology_control"
    if profile == "same_author_chain_entity_reuse_controls":
        return "same_chain_entity_reuse_topology_control"
    if profile == "gamma_chain_assignment_namespace_controls":
        return "gamma_chain_assignment_namespace_control"
    if profile == "ligand_namespace_materialization_nohit_controls":
        return "ligand_namespace_materialization_nohit_control"
    if profile == "auth_label_gamma_collision_counterexamples":
        return "auth_label_gamma_collision_counterexample_control"
    return profile


def blocker_class(row: dict[str, Any], profile: str) -> str:
    if (
        row.get("known_epk_positive_input")
        or row.get("source_context_epk_review_candidate")
        or row.get("source_valid_epk_seed_review_candidate")
    ):
        return "positive_control_retention_expected"
    if row.get("context_v4_oligomeric_atp_terminals_no_mg_required_hit"):
        return "context_v4_oligomeric_atp_terminals_no_mg_required"
    if row.get("entry_level_any_context_v4_guard_hit_review_only"):
        return "entry_level_any_context_v4_review_only"
    if topology_ambiguity(row):
        return "same_chain_or_reciprocal_topology_ambiguity"
    if profile == "same_author_chain_entity_reuse_controls":
        return "same_author_chain_entity_reuse"
    if profile == "gamma_chain_assignment_namespace_controls":
        return "auth_label_gamma_namespace_assignment"
    if profile == "auth_label_gamma_collision_counterexamples":
        return "auth_label_gamma_collision_counteraxis_needed"
    if materializer_hit_count(row) == 0:
        return "no_substrate_mode_materializer_hit"
    return "missing_policy_blocker_review_only"


def expected_policy_decision(row: dict[str, Any], profile: str) -> str:
    if (
        row.get("known_epk_positive_input")
        or row.get("source_context_epk_review_candidate")
        or row.get("source_valid_epk_seed_review_candidate")
    ):
        return "retain_or_source_validate_epk_positive_review_only"
    if blocker_class(row, profile) == "no_substrate_mode_materializer_hit":
        return "abstain_no_materializer_hit"
    return "block_or_abstain_non_epk_control"


def observed_materializer_decision(row: dict[str, Any]) -> str:
    if topology_clear(row):
        return "topology_clear_substrate_mode_nonabstention"
    if materializer_hit_count(row) > 0 and topology_ambiguity(row):
        return "topology_ambiguous_substrate_mode_hit"
    if materializer_hit_count(row) > 0:
        return "materializer_candidate_nonabstention"
    return "no_substrate_mode_materializer_hit"


def compact_candidate_fields(hit: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_acceptor_chain_name": hit.get("candidate_chain_name"),
        "candidate_acceptor_auth_seq_id": hit.get("candidate_auth_seq_id"),
        "candidate_acceptor_residue_code": hit.get("candidate_residue_code"),
        "candidate_acceptor_atom_name": hit.get("candidate_atom_name"),
        "gamma_associated_polymer_chain_name": hit.get(
            "gamma_associated_polymer_chain_name"
        ),
        "gamma_associated_polymer_entity_id": hit.get(
            "gamma_associated_polymer_entity_id"
        ),
        "gamma_ligand_code": hit.get("gamma_ligand_code"),
        "gamma_atom_name": hit.get("gamma_atom_name"),
        "nearest_gamma_distance_angstrom": (
            round(numeric(hit.get("nearest_gamma_distance_angstrom")), 3)
            if hit.get("nearest_gamma_distance_angstrom") is not None
            else None
        ),
        "nearest_mg_distance_angstrom": (
            round(numeric(hit.get("nearest_mg_distance_angstrom")), 3)
            if hit.get("nearest_mg_distance_angstrom") is not None
            else None
        ),
    }


def row_fixture_id(row: dict[str, Any], profile: str) -> str:
    pdb_id = str(row.get("pdb_id") or "unknown").upper()
    context = str(row.get("coordinate_context") or "deposited_atom_site")
    cls = control_class(row, profile)
    return f"{SCHEMA_VERSION}:{pdb_id}:{context}:{cls}"


def convert_row(
    row: dict[str, Any],
    *,
    source_path: str,
    source_profile: str,
    source_method: str | None,
) -> dict[str, Any]:
    hit = first_hit(row)
    cls = control_class(row, source_profile)
    block = blocker_class(row, source_profile)
    expected = expected_policy_decision(row, source_profile)
    observed = observed_materializer_decision(row)
    non_epk = is_non_epk(row, source_profile)
    raw_nonabstention = observed != "no_substrate_mode_materializer_hit"
    topo_clear = topology_clear(row)
    context_v4_hit = boolish(
        row.get("context_v4_oligomeric_atp_terminals_no_mg_required_hit")
    )
    context_v4_only_unsafe = bool(
        non_epk
        and topo_clear
        and not context_v4_hit
        and block == "entry_level_any_context_v4_review_only"
    )
    unsafe_after_expected_policy = bool(
        non_epk
        and topo_clear
        and expected == "block_or_abstain_non_epk_control"
        and block == "missing_policy_blocker_review_only"
    )
    context_metrics = row.get("context_source_free_multisite_metrics") or {}
    compact_metrics = {
        key: context_metrics.get(key)
        for key in (
            "gamma_capable_terminal_p_count",
            "gamma_capable_terminal_p_near_mg_count",
            "gamma_capable_terminal_p_near_mg_chain_count",
            "polymer_chain_count",
            "polymer_entity_count",
        )
        if isinstance(context_metrics, dict) and key in context_metrics
    }
    converted = {
        "schema_version": SCHEMA_VERSION,
        "row_type": "epk_false_positive_regression_control_row",
        "fixture_id": row_fixture_id(row, source_profile),
        "lane_id": LANE_ID,
        "target_family_id": TARGET_FAMILY_ID,
        "target_fingerprint_id": TARGET_FINGERPRINT_ID,
        "review_only": True,
        "production_scoring_admissible": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "ready_for_orphan_discovery_claims": False,
        "countable_label_candidate": False,
        "epk_score_computed": False,
        "external_hard_negative_reaudit_scored": False,
        "pdb_id": str(row.get("pdb_id") or "").upper(),
        "coordinate_state": coordinate_state(row),
        "coordinate_context": str(row.get("coordinate_context") or "deposited_atom_site"),
        "control_class": cls,
        "source_profile": source_profile,
        "source_artifact": source_path,
        "source_method": source_method,
        "known_epk_positive_input": boolish(row.get("known_epk_positive_input")),
        "probable_epk_from_context": boolish(row.get("probable_epk_from_context")),
        "non_epk_control": non_epk,
        "guard_blocker_class": block,
        "expected_policy_decision": expected,
        "observed_materializer_decision": observed,
        "observed_materializer_nonabstention": raw_nonabstention,
        "observed_topology_clear_substrate_mode_hit": topo_clear,
        "raw_materializer_hit_count": materializer_hit_count(row),
        "context_v4_oligomeric_atp_terminals_no_mg_required_hit": context_v4_hit,
        "entry_level_any_context_v4_guard_hit_review_only": boolish(
            row.get("entry_level_any_context_v4_guard_hit_review_only")
        ),
        "deposited_v4_context_below_chain_floor": boolish(
            row.get("deposited_v4_context_below_chain_floor")
        ),
        "same_chain_topology_detected": boolish(
            row.get("same_chain_topology_detected")
            or row.get("auth_same_chain_topology_detected")
        ),
        "reciprocal_cross_chain_topology_detected": boolish(
            row.get("reciprocal_cross_chain_topology_detected")
            or row.get("auth_reciprocal_cross_chain_topology_detected")
        ),
        "topology_ambiguity_counteraxis_hit": topology_ambiguity(row),
        "current_context_v4_only_unsafe_nonabstention": context_v4_only_unsafe,
        "unsafe_nonabstention_after_expected_policy": unsafe_after_expected_policy,
        "observed_source_decision": row.get("entry_level_guard_stress_decision")
        or row.get("custom_stress_decision")
        or row.get("source_valid_geometry_prefilter_stress_decision")
        or row.get("source_validation_status")
        or row.get("counterexample_rationale"),
        "source_query_surface_groups": row.get("query_surface_groups", []),
        "source_context_terms": row.get("source_context_terms", []),
        "role_tokens": row.get("deposited_orc_mcm_role_tokens", []),
        "context_guard_metrics": compact_metrics,
        "candidate": compact_candidate_fields(hit),
        "remaining_blockers": sorted(
            {
                "review_only_lane_fixture_not_production_scoring",
                "threshold_not_calibrated",
                "external_hard_negative_reaudit_not_real_scorer",
                "registry_and_label_factory_extension_not_implemented",
                block,
            }
        ),
    }
    return converted


def convert_source(repo_root: Path, spec: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rel_path = str(spec["path"])
    path = repo_root / rel_path
    if not path.exists():
        return [], {"path": rel_path, "status": "missing", "row_count": 0}
    payload = load_json(path)
    source_method = None
    if isinstance(payload.get("metadata"), dict):
        source_method = payload["metadata"].get("method")
    rows = payload.get(str(spec["row_key"]), [])
    if not isinstance(rows, list):
        rows = []
    source_profile = str(spec["source_profile"])
    if source_profile == "source_valid_epk_seed_geometry_prefilter_controls":
        rows = [
            row
            for row in rows
            if isinstance(row, dict)
            and (
                row.get("source_valid_epk_seed_review_candidate")
                or row.get("non_epk_v4_contaminant_prefilter_candidate")
            )
        ]
    converted = [
        convert_row(
            row,
            source_path=rel_path,
            source_profile=source_profile,
            source_method=source_method,
        )
        for row in rows
        if isinstance(row, dict)
    ]
    return converted, {
        "path": rel_path,
        "status": "ok",
        "source_method": source_method,
        "row_key": spec["row_key"],
        "source_profile": spec["source_profile"],
        "row_count": len(rows),
        "converted_row_count": len(converted),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--ended-at", default=None)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ended_at = args.ended_at or now_utc()
    rows: list[dict[str, Any]] = []
    source_summaries: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        converted, summary = convert_source(repo_root, spec)
        rows.extend(converted)
        source_summaries.append(summary)

    rows = sorted(
        rows,
        key=lambda row: (
            str(row.get("control_class") or ""),
            str(row.get("pdb_id") or ""),
            str(row.get("coordinate_context") or ""),
            str(row.get("source_artifact") or ""),
        ),
    )
    class_counts = Counter(str(row["control_class"]) for row in rows)
    blocker_counts = Counter(str(row["guard_blocker_class"]) for row in rows)
    observed_counts = Counter(str(row["observed_materializer_decision"]) for row in rows)
    current_context_v4_failures = [
        row for row in rows if row["current_context_v4_only_unsafe_nonabstention"]
    ]
    unsafe_after_expected = [
        row for row in rows if row["unsafe_nonabstention_after_expected_policy"]
    ]
    biological_split_materializer_rows = [
        row
        for row in rows
        if row["control_class"] == "orc_mcm_biological_assembly_split_control"
        and row["observed_topology_clear_substrate_mode_hit"]
    ]
    output = {
        "metadata": {
            "method": "epk_candidate_evidence_regression_gate_from_lane_artifacts",
            "schema_version": SCHEMA_VERSION,
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id": TARGET_FINGERPRINT_ID,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "source_artifact_count": len(source_summaries),
            "source_artifacts": source_summaries,
            "source_rows_reviewed": sum(
                intish(summary.get("row_count"))
                for summary in source_summaries
                if summary.get("status") == "ok"
            ),
            "regression_rows_emitted": len(rows),
            "control_class_counts": dict(sorted(class_counts.items())),
            "guard_blocker_class_counts": dict(sorted(blocker_counts.items())),
            "observed_materializer_decision_counts": dict(
                sorted(observed_counts.items())
            ),
            "observed_materializer_nonabstention_count": sum(
                1 for row in rows if row["observed_materializer_nonabstention"]
            ),
            "observed_topology_clear_non_epk_nonabstention_count": sum(
                1
                for row in rows
                if row["non_epk_control"]
                and row["observed_topology_clear_substrate_mode_hit"]
            ),
            "unsafe_nonabstention_after_expected_policy_count": len(
                unsafe_after_expected
            ),
            "unsafe_nonabstention_after_expected_policy_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in unsafe_after_expected
            ),
            "current_context_v4_only_unsafe_nonabstention_count": len(
                current_context_v4_failures
            ),
            "current_context_v4_only_unsafe_nonabstention_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in current_context_v4_failures
            ),
            "biological_assembly_split_materializer_counterexample_count": len(
                biological_split_materializer_rows
            ),
            "biological_assembly_split_materializer_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}"
                for row in biological_split_materializer_rows
            ),
            "regression_gate_status": (
                "passes_expected_policy_gate_review_only"
                if not unsafe_after_expected
                else "fails_expected_policy_gate_review_only"
            ),
            "context_v4_only_gate_status": (
                "falsified_by_known_assembly_split_counterexample_review_only"
                if current_context_v4_failures
                else "no_context_v4_only_failure_in_emitted_rows_review_only"
            ),
            "rule_under_attack": (
                "current materializer non-abstention on ATPase/transporter/"
                "ORC-MCM/motor/same-chain/internal-fragment/namespace controls "
                "and assembly-context v4 sufficiency"
            ),
            "gate_rule": (
                "Every non-ePK control row with a topology-clear materializer "
                "non-abstention must carry an explicit review-only blocker; "
                "5UJ7 biological assembly 1 remains the pinned context-v4-only "
                "assembly split failure."
            ),
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "epk_score_computed": False,
            "external_hard_negative_reaudit_scored": False,
            "selected_threshold_angstrom": None,
            "threshold_calibrated": False,
        },
        "rows": rows,
        "warnings": [
            (
                "This is a lane-only regression evidence artifact. It does not "
                "authorize production scoring, label import, threshold "
                "selection, registry edits, or fingerprint changes."
            )
        ],
    }
    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
