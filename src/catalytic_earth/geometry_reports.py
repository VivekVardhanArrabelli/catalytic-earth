from __future__ import annotations

import json
from pathlib import Path
from typing import Any


GEOMETRY_SLICES = [
    ("20", ""),
    ("30", "_30"),
    ("40", "_40"),
    ("50", "_50"),
    ("60", "_60"),
    ("75", "_75"),
    ("100", "_100"),
    ("125", "_125"),
    ("150", "_150"),
    ("175", "_175"),
    ("200", "_200"),
    ("225", "_225"),
    ("250", "_250"),
    ("275", "_275"),
    ("300", "_300"),
    ("325", "_325"),
    ("350", "_350"),
    ("375", "_375"),
    ("400", "_400"),
    ("425", "_425"),
    ("450", "_450"),
    ("475", "_475"),
    ("500", "_500"),
    ("525", "_525"),
    ("550", "_550"),
    ("575", "_575"),
    ("600", "_600"),
]


def summarize_geometry_slices(artifact_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for slice_label, suffix in GEOMETRY_SLICES:
        geometry = _read_optional_json(artifact_dir / f"v3_geometry_features{suffix}.json")
        evaluation = _read_optional_json(artifact_dir / f"v3_geometry_label_eval{suffix}.json")
        hard_negatives = _read_optional_json(
            artifact_dir / f"v3_hard_negative_controls{suffix}.json"
        )
        margins = _read_optional_json(artifact_dir / f"v3_geometry_score_margins{suffix}.json")
        in_scope_failures = _read_optional_json(
            artifact_dir / f"v3_in_scope_failure_analysis{suffix}.json"
        )
        mapping_issues = _read_optional_json(
            artifact_dir / f"v3_structure_mapping_issues{suffix}.json"
        )
        label_candidates = _read_optional_json(
            artifact_dir / f"v3_label_expansion_candidates{suffix}.json"
        )
        cofactor_coverage = _read_optional_json(
            artifact_dir / f"v3_cofactor_coverage{suffix}.json"
        )
        cofactor_policy = _read_optional_json(
            artifact_dir / f"v3_cofactor_policy{suffix}.json"
        )
        seed_family_performance = _read_optional_json(
            artifact_dir / f"v3_seed_family_performance{suffix}.json"
        )
        if not evaluation:
            continue
        geometry_meta = geometry.get("metadata", {}) if geometry else {}
        eval_meta = evaluation.get("metadata", {})
        hard_meta = hard_negatives.get("metadata", {}) if hard_negatives else {}
        margin_meta = margins.get("metadata", {}) if margins else {}
        in_scope_meta = in_scope_failures.get("metadata", {}) if in_scope_failures else {}
        mapping_meta = mapping_issues.get("metadata", {}) if mapping_issues else {}
        label_candidate_meta = label_candidates.get("metadata", {}) if label_candidates else {}
        cofactor_meta = cofactor_coverage.get("metadata", {}) if cofactor_coverage else {}
        cofactor_policy_meta = cofactor_policy.get("metadata", {}) if cofactor_policy else {}
        family_meta = (
            seed_family_performance.get("metadata", {})
            if seed_family_performance
            else {}
        )
        closest_near_miss = _closest_near_miss(hard_negatives)
        rows.append(
            {
                "slice": slice_label,
                "evaluated_count": eval_meta.get("evaluated_count"),
                "evaluable_count": eval_meta.get("evaluable_count"),
                "entries_with_proximal_ligands": geometry_meta.get(
                    "entries_with_proximal_ligands"
                ),
                "entries_with_inferred_cofactors": geometry_meta.get(
                    "entries_with_inferred_cofactors"
                ),
                "entries_with_structure_ligands": geometry_meta.get(
                    "entries_with_structure_ligands"
                ),
                "entries_with_structure_inferred_cofactors": geometry_meta.get(
                    "entries_with_structure_inferred_cofactors"
                ),
                "in_scope_count": eval_meta.get("in_scope_count"),
                "out_of_scope_count": eval_meta.get("out_of_scope_count"),
                "abstain_threshold": eval_meta.get("abstain_threshold"),
                "top1_accuracy_in_scope_evaluable": eval_meta.get(
                    "top1_accuracy_in_scope_evaluable"
                ),
                "top3_accuracy_in_scope_evaluable": eval_meta.get(
                    "top3_accuracy_in_scope_evaluable"
                ),
                "in_scope_retention_rate_evaluable": eval_meta.get(
                    "in_scope_retention_rate_evaluable"
                ),
                "out_of_scope_false_non_abstentions_evaluable": eval_meta.get(
                    "out_of_scope_false_non_abstentions_evaluable"
                ),
                "hard_negative_count": hard_meta.get("hard_negative_count"),
                "near_miss_count": hard_meta.get("near_miss_count"),
                "near_miss_top1_fingerprint_counts": hard_meta.get(
                    "near_miss_top1_fingerprint_counts"
                ),
                "near_miss_cofactor_evidence_counts": hard_meta.get(
                    "near_miss_cofactor_evidence_counts"
                ),
                "closest_near_miss_entry_id": closest_near_miss.get("entry_id"),
                "closest_near_miss_top1_fingerprint_id": closest_near_miss.get(
                    "top1_fingerprint_id"
                ),
                "closest_near_miss_score": closest_near_miss.get("top1_score"),
                "closest_near_miss_score_gap_to_floor": closest_near_miss.get(
                    "score_gap_to_floor"
                ),
                "closest_below_floor_entry_id": hard_meta.get(
                    "closest_below_floor_entry_id"
                ),
                "closest_below_floor_top1_fingerprint_id": hard_meta.get(
                    "closest_below_floor_top1_fingerprint_id"
                ),
                "minimum_below_floor_score_gap": hard_meta.get(
                    "minimum_below_floor_score_gap"
                ),
                "score_separation_gap": margin_meta.get("score_separation_gap"),
                "correct_positive_score_separation_gap": margin_meta.get(
                    "correct_positive_score_separation_gap"
                ),
                "strict_threshold_exists": margin_meta.get(
                    "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
                ),
                "in_scope_failure_count": in_scope_meta.get("failure_count"),
                "actionable_in_scope_failure_count": in_scope_meta.get(
                    "actionable_failure_count"
                ),
                "evidence_limited_abstention_count": in_scope_meta.get(
                    "evidence_limited_abstention_count"
                ),
                "mapping_issue_count": mapping_meta.get("issue_count"),
                "labeled_mapping_issue_count": mapping_meta.get("labeled_issue_count"),
                "label_candidate_count": label_candidate_meta.get("candidate_count"),
                "ready_label_candidate_count": label_candidate_meta.get(
                    "ready_for_label_review_count"
                ),
                "cofactor_expected_absent_count": cofactor_meta.get(
                    "expected_absent_count"
                ),
                "cofactor_expected_absent_retained_count": cofactor_meta.get(
                    "expected_absent_retained_count"
                ),
                "cofactor_expected_absent_abstained_count": cofactor_meta.get(
                    "expected_absent_abstained_count"
                ),
                "cofactor_structure_only_count": cofactor_meta.get("structure_only_count"),
                "cofactor_structure_only_retained_count": cofactor_meta.get(
                    "structure_only_retained_count"
                ),
                "cofactor_evidence_limited_retained_count": cofactor_meta.get(
                    "evidence_limited_retained_count"
                ),
                "cofactor_evidence_limited_abstained_count": cofactor_meta.get(
                    "evidence_limited_abstained_count"
                ),
                "cofactor_local_supported_count": cofactor_meta.get(
                    "local_supported_count"
                ),
                "cofactor_policy_recommendation": cofactor_policy_meta.get(
                    "recommendation"
                ),
                "cofactor_policy_guardrail_passing_policy_count": cofactor_policy_meta.get(
                    "guardrail_passing_policy_count"
                ),
                "cofactor_policy_lossless_decision_changing_policy_count": (
                    cofactor_policy_meta.get("lossless_decision_changing_policy_count")
                ),
                "cofactor_policy_audit_evidence_limited_retained_positive_count": (
                    cofactor_policy_meta.get(
                        "audit_evidence_limited_retained_positive_count"
                    )
                ),
                "cofactor_policy_minimum_evidence_limited_retained_margin": (
                    cofactor_policy_meta.get("minimum_evidence_limited_retained_margin")
                ),
                "seed_family_count": family_meta.get("in_scope_family_count"),
                "largest_seed_family": family_meta.get("largest_in_scope_family"),
                "largest_seed_family_count": family_meta.get(
                    "largest_in_scope_family_count"
                ),
                "weakest_retained_seed_family": family_meta.get(
                    "weakest_retained_in_scope_family"
                ),
                "weakest_retained_seed_family_accuracy": family_meta.get(
                    "weakest_retained_in_scope_family_accuracy"
                ),
                "out_of_scope_retained_seed_family_count": family_meta.get(
                    "out_of_scope_retained_family_count"
                ),
            }
        )

    failure_counts = [
        int(row["in_scope_failure_count"])
        for row in rows
        if row.get("in_scope_failure_count") is not None
    ]
    actionable_failure_counts = [
        int(row["actionable_in_scope_failure_count"])
        for row in rows
        if row.get("actionable_in_scope_failure_count") is not None
    ]
    slices_with_in_scope_failures = [
        row["slice"]
        for row in rows
        if int(row.get("in_scope_failure_count") or 0) > 0
    ]
    cofactor_absent_counts = [
        int(row["cofactor_expected_absent_count"])
        for row in rows
        if row.get("cofactor_expected_absent_count") is not None
    ]
    cofactor_limited_retained_counts = [
        int(row["cofactor_evidence_limited_retained_count"])
        for row in rows
        if row.get("cofactor_evidence_limited_retained_count") is not None
    ]
    slices_with_absent_expected_cofactors = [
        row["slice"]
        for row in rows
        if int(row.get("cofactor_expected_absent_count") or 0) > 0
    ]
    slices_with_limited_retained_cofactor_evidence = [
        row["slice"]
        for row in rows
        if int(row.get("cofactor_evidence_limited_retained_count") or 0) > 0
    ]
    slices_with_lossless_cofactor_penalty = [
        row["slice"]
        for row in rows
        if int(row.get("cofactor_policy_lossless_decision_changing_policy_count") or 0) > 0
    ]
    slices_recommending_audit_only_cofactor_policy = [
        row["slice"]
        for row in rows
        if row.get("cofactor_policy_recommendation") == "audit_only_or_separate_stratum"
    ]
    limited_retained_margins = [
        float(row["cofactor_policy_minimum_evidence_limited_retained_margin"])
        for row in rows
        if row.get("cofactor_policy_minimum_evidence_limited_retained_margin") is not None
    ]
    out_scope_retained_family_counts = [
        int(row["out_of_scope_retained_seed_family_count"])
        for row in rows
        if row.get("out_of_scope_retained_seed_family_count") is not None
    ]
    near_miss_gaps = [
        float(row["closest_near_miss_score_gap_to_floor"])
        for row in rows
        if row.get("closest_near_miss_score_gap_to_floor") is not None
    ]
    below_floor_boundary_rows = [
        row for row in rows if row.get("minimum_below_floor_score_gap") is not None
    ]
    closest_below_floor = min(
        below_floor_boundary_rows,
        key=lambda row: (
            float(row.get("minimum_below_floor_score_gap", float("inf"))),
            str(row.get("slice", "")),
        ),
        default={},
    )
    slices_with_near_misses = [
        row["slice"]
        for row in rows
        if int(row.get("near_miss_count") or 0) > 0
    ]

    return {
        "metadata": {
            "method": "geometry_slice_metric_summary",
            "slice_count": len(rows),
            "largest_slice": rows[-1]["slice"] if rows else None,
            "all_zero_hard_negatives": all(row.get("hard_negative_count") == 0 for row in rows),
            "all_zero_false_non_abstentions": all(
                row.get("out_of_scope_false_non_abstentions_evaluable") == 0
                for row in rows
            ),
            "all_zero_in_scope_failures": all(
                int(row.get("in_scope_failure_count") or 0) == 0 for row in rows
            ),
            "max_in_scope_failure_count": max(failure_counts, default=0),
            "max_actionable_in_scope_failure_count": max(
                actionable_failure_counts, default=0
            ),
            "all_zero_actionable_in_scope_failures": all(
                int(row.get("actionable_in_scope_failure_count") or 0) == 0
                for row in rows
            ),
            "slices_with_in_scope_failures": slices_with_in_scope_failures,
            "total_in_scope_failure_count": sum(failure_counts),
            "total_actionable_in_scope_failure_count": sum(actionable_failure_counts),
            "all_zero_ready_label_candidates": all(
                int(row.get("ready_label_candidate_count") or 0) == 0 for row in rows
            ),
            "max_cofactor_expected_absent_count": max(cofactor_absent_counts, default=0),
            "slices_with_absent_expected_cofactors": slices_with_absent_expected_cofactors,
            "max_cofactor_evidence_limited_retained_count": max(
                cofactor_limited_retained_counts,
                default=0,
            ),
            "slices_with_limited_retained_cofactor_evidence": (
                slices_with_limited_retained_cofactor_evidence
            ),
            "slices_with_lossless_cofactor_penalty": slices_with_lossless_cofactor_penalty,
            "slices_recommending_audit_only_cofactor_policy": (
                slices_recommending_audit_only_cofactor_policy
            ),
            "minimum_evidence_limited_retained_margin": min(
                limited_retained_margins,
                default=None,
            ),
            "max_out_of_scope_retained_seed_family_count": max(
                out_scope_retained_family_counts,
                default=0,
            ),
            "slices_with_near_misses": slices_with_near_misses,
            "minimum_near_miss_score_gap_to_floor": min(
                near_miss_gaps,
                default=None,
            ),
            "minimum_below_floor_score_gap": closest_below_floor.get(
                "minimum_below_floor_score_gap"
            ),
            "closest_below_floor_slice": closest_below_floor.get("slice"),
            "closest_below_floor_entry_id": closest_below_floor.get(
                "closest_below_floor_entry_id"
            ),
            "closest_below_floor_top1_fingerprint_id": closest_below_floor.get(
                "closest_below_floor_top1_fingerprint_id"
            ),
            "validation_boundary": "artifact summary only; depends on curated labels and generated JSON inputs",
        },
        "rows": rows,
    }


def write_geometry_slice_summary(artifact_dir: Path, out_path: Path) -> dict[str, Any]:
    summary = summarize_geometry_slices(artifact_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def _closest_near_miss(hard_negatives: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(hard_negatives, dict):
        return {}
    rows = hard_negatives.get("near_miss_rows", [])
    if not isinstance(rows, list):
        return {}
    candidates = [row for row in rows if isinstance(row, dict)]
    return min(
        candidates,
        key=lambda row: (
            float(row.get("score_gap_to_floor", float("inf"))),
            str(row.get("entry_id", "")),
        ),
        default={},
    )
