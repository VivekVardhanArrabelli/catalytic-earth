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
]


def summarize_geometry_slices(artifact_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for slice_label, suffix in GEOMETRY_SLICES:
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
        if not evaluation:
            continue
        eval_meta = evaluation.get("metadata", {})
        hard_meta = hard_negatives.get("metadata", {}) if hard_negatives else {}
        margin_meta = margins.get("metadata", {}) if margins else {}
        in_scope_meta = in_scope_failures.get("metadata", {}) if in_scope_failures else {}
        mapping_meta = mapping_issues.get("metadata", {}) if mapping_issues else {}
        label_candidate_meta = label_candidates.get("metadata", {}) if label_candidates else {}
        rows.append(
            {
                "slice": slice_label,
                "evaluated_count": eval_meta.get("evaluated_count"),
                "evaluable_count": eval_meta.get("evaluable_count"),
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
                "score_separation_gap": margin_meta.get("score_separation_gap"),
                "correct_positive_score_separation_gap": margin_meta.get(
                    "correct_positive_score_separation_gap"
                ),
                "strict_threshold_exists": margin_meta.get(
                    "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
                ),
                "in_scope_failure_count": in_scope_meta.get("failure_count"),
                "mapping_issue_count": mapping_meta.get("issue_count"),
                "labeled_mapping_issue_count": mapping_meta.get("labeled_issue_count"),
                "label_candidate_count": label_candidate_meta.get("candidate_count"),
                "ready_label_candidate_count": label_candidate_meta.get(
                    "ready_for_label_review_count"
                ),
            }
        )

    failure_counts = [
        int(row["in_scope_failure_count"])
        for row in rows
        if row.get("in_scope_failure_count") is not None
    ]
    slices_with_in_scope_failures = [
        row["slice"]
        for row in rows
        if int(row.get("in_scope_failure_count") or 0) > 0
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
            "slices_with_in_scope_failures": slices_with_in_scope_failures,
            "total_in_scope_failure_count": sum(failure_counts),
            "all_zero_ready_label_candidates": all(
                int(row.get("ready_label_candidate_count") or 0) == 0 for row in rows
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
