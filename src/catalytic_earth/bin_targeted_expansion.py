from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGET_BINS = [
    "no_reliable_structure",
    "low_structure_neighborhood_near_orphan",
]


def build_bin_targeted_expansion_plan(
    *,
    wave1_audit: dict[str, Any],
    slice_contract: dict[str, Any],
    readiness_matrix: dict[str, Any],
    target_primary_n: int = 30,
    target_oos_n: int = 10,
) -> dict[str, Any]:
    """Build a review-only queue to lift sparse Wave 1.2 bins."""
    current_bins = _current_bin_support(wave1_audit)
    readiness_rows = [
        row for row in readiness_matrix.get("rows", []) if isinstance(row, dict)
    ]
    slice_rows = [row for row in slice_contract.get("rows", []) if isinstance(row, dict)]
    expansion_bins = []
    for bin_name in TARGET_BINS:
        support = current_bins.get(bin_name, _empty_support(bin_name))
        primary_gap = max(0, target_primary_n - support["primary_support_count"])
        oos_gap = max(0, target_oos_n - support["oos_or_secondary_support_count"])
        expansion_bins.append(
            {
                "bin": bin_name,
                "current_support": support,
                "target_primary_n": target_primary_n,
                "target_oos_or_secondary_n": target_oos_n,
                "primary_gap_to_target": primary_gap,
                "oos_or_secondary_gap_to_target": oos_gap,
                "priority": _bin_priority(primary_gap, oos_gap),
            }
        )

    candidate_rows = _candidate_rows(
        slice_rows=slice_rows,
        readiness_rows=readiness_rows,
        current_bins=current_bins,
    )
    status_counts = Counter(row["queue_status"] for row in candidate_rows)
    bin_counts = Counter(row["target_bin"] for row in candidate_rows)
    action_counts = Counter(row["next_action"] for row in candidate_rows)
    return {
        "artifact_id": "v3_bin_targeted_expansion_plan_702_20260529",
        "schema_version": "bin_targeted_expansion_plan.v1",
        "created_utc": _utc_now_iso(),
        "status": "review_only_plan",
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "label_import_performed": False,
            "heldout_tuning_performed": False,
            "large_downloads_performed": False,
        },
        "objective": (
            "Lift no_reliable_structure and near_orphan Wave 1.2 bins to "
            "evaluable support without changing current labels or tuning on "
            "heldout rows."
        ),
        "target_policy": {
            "primary_target_per_bin": target_primary_n,
            "oos_or_secondary_target_per_bin": target_oos_n,
            "countable_import_required_before_metric_use": True,
            "current_rows_remain_final_only": True,
        },
        "current_bins": expansion_bins,
        "queue_summary": {
            "candidate_count": len(candidate_rows),
            "queue_status_counts": dict(sorted(status_counts.items())),
            "target_bin_counts": dict(sorted(bin_counts.items())),
            "next_action_counts": dict(sorted(action_counts.items())),
        },
        "candidate_rows": candidate_rows,
        "recommendation": _recommendation(expansion_bins, candidate_rows),
        "source_artifacts": {
            "wave1_audit": (
                "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json"
            ),
            "slice_contract": (
                "artifacts/v3_wave1_2_fold_conflict_near_orphan_slice_contract_702_20260528.json"
            ),
            "readiness_matrix": "artifacts/v3_active_site_encoder_readiness_matrix_20260528.json",
        },
    }


def write_bin_targeted_expansion_plan(
    *,
    wave1_audit_path: Path,
    slice_contract_path: Path,
    readiness_matrix_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    target_primary_n: int = 30,
    target_oos_n: int = 10,
) -> dict[str, Any]:
    with wave1_audit_path.open("r", encoding="utf-8") as handle:
        wave1_audit = json.load(handle)
    with slice_contract_path.open("r", encoding="utf-8") as handle:
        slice_contract = json.load(handle)
    with readiness_matrix_path.open("r", encoding="utf-8") as handle:
        readiness_matrix = json.load(handle)
    plan = build_bin_targeted_expansion_plan(
        wave1_audit=wave1_audit,
        slice_contract=slice_contract,
        readiness_matrix=readiness_matrix,
        target_primary_n=target_primary_n,
        target_oos_n=target_oos_n,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(plan), encoding="utf-8")
    return plan


def _current_bin_support(wave1_audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    per_bin = wave1_audit.get("per_bin_results", {})
    support: dict[str, dict[str, Any]] = {}
    if isinstance(per_bin, dict):
        for bin_name, payload in per_bin.items():
            if not isinstance(payload, dict):
                continue
            track_results = payload.get("track_results", {})
            geometry = (
                track_results.get("geometry_baseline_reexport", {})
                if isinstance(track_results, dict)
                else {}
            )
            support[str(bin_name)] = {
                "row_count": geometry.get("row_count", 0),
                "primary_support_count": geometry.get("primary_support_count", 0),
                "primary_abstention_count": geometry.get("primary_abstention_count", 0),
                "primary_accuracy_available": geometry.get(
                    "primary_accuracy_available"
                ),
                "oos_or_secondary_support_count": geometry.get(
                    "oos_or_secondary_support_count", 0
                ),
                "oos_or_secondary_false_positive_rate_available": geometry.get(
                    "oos_or_secondary_false_positive_rate_available"
                ),
                "row_ids": payload.get("row_ids", []),
            }
    return support


def _candidate_rows(
    *,
    slice_rows: list[dict[str, Any]],
    readiness_rows: list[dict[str, Any]],
    current_bins: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    current_near_orphan_ids = set(
        current_bins.get("low_structure_neighborhood_near_orphan", {}).get(
            "row_ids", []
        )
    )
    current_no_reliable_ids = set(
        current_bins.get("no_reliable_structure", {}).get("row_ids", [])
    )
    for row in slice_rows:
        bin_name = str(row.get("structural_neighborhood_bin") or "")
        if bin_name not in TARGET_BINS:
            continue
        candidates.append(
            {
                "candidate_id": row.get("entry_id"),
                "target_bin": bin_name,
                "current_fingerprint_id": row.get("current_fingerprint_id"),
                "split_assignment": row.get("split_assignment"),
                "source": "wave1_2_slice_contract",
                "queue_status": (
                    "already_in_current_heldout_bin"
                    if row.get("entry_id") in current_near_orphan_ids
                    or row.get("entry_id") in current_no_reliable_ids
                    else "slice_candidate_needs_review"
                ),
                "next_action": (
                    "use_as_current_final_only_diagnostic_context"
                    if row.get("entry_id") in current_near_orphan_ids
                    or row.get("entry_id") in current_no_reliable_ids
                    else "review_before_future_split_assignment"
                ),
                "ready_for_label_import": False,
                "countable_label_candidate": False,
                "notes": row.get("use_reason"),
            }
        )
    for row in readiness_rows:
        source_group = str(row.get("source_group") or "")
        allowed_use = str(row.get("allowed_use") or "")
        candidate_id = str(row.get("candidate_id") or "")
        if source_group == "clean_near_orphan_anchor":
            target_bin = "low_structure_neighborhood_near_orphan"
            next_action = (
                "reserve_as_calibration_or_architecture_probe_context"
                if row.get("split_assignment") == "heldout"
                else "consider_for_future_near_orphan_train_cal_expansion"
            )
        elif (
            source_group == "external_router_priority"
            and allowed_use == "external_materialization_needed_before_feature_extraction"
        ):
            target_bin = "low_structure_neighborhood_near_orphan"
            next_action = "materialize_structure_then_score_as_review_only_oos_control"
        elif source_group == "oos_router_control":
            target_bin = "no_reliable_structure"
            next_action = "hold_as_oos_router_control_context"
        else:
            continue
        candidates.append(
            {
                "candidate_id": candidate_id,
                "target_bin": target_bin,
                "current_fingerprint_id": row.get("current_fingerprint_id"),
                "split_assignment": row.get("split_assignment"),
                "source": "active_site_encoder_readiness_matrix",
                "source_group": source_group,
                "queue_status": allowed_use,
                "coordinate_status": row.get("coordinate_status"),
                "next_action": next_action,
                "ready_for_label_import": False,
                "countable_label_candidate": False,
                "notes": "review-only expansion queue; not a label import",
            }
        )
    deduped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in candidates:
        key = (
            str(row.get("candidate_id")),
            str(row.get("target_bin")),
            str(row.get("source")),
        )
        deduped[key] = row
    return sorted(
        deduped.values(),
        key=lambda row: (
            str(row.get("target_bin")),
            str(row.get("next_action")),
            str(row.get("candidate_id")),
        ),
    )


def _recommendation(
    expansion_bins: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    materialization = [
        row
        for row in candidate_rows
        if row.get("next_action")
        == "materialize_structure_then_score_as_review_only_oos_control"
    ]
    no_reliable = next(
        row for row in expansion_bins if row["bin"] == "no_reliable_structure"
    )
    near = next(
        row
        for row in expansion_bins
        if row["bin"] == "low_structure_neighborhood_near_orphan"
    )
    return {
        "first_batch": "near_orphan_oos_control_materialization",
        "rationale": (
            "near_orphan already has primary support at the target but lacks "
            "OOS/secondary controls; no_reliable_structure remains underpowered "
            "on both primary and OOS support."
        ),
        "near_orphan_oos_materialization_candidate_count": len(materialization),
        "no_reliable_structure_primary_gap": no_reliable["primary_gap_to_target"],
        "no_reliable_structure_oos_gap": no_reliable[
            "oos_or_secondary_gap_to_target"
        ],
        "near_orphan_primary_gap": near["primary_gap_to_target"],
        "near_orphan_oos_gap": near["oos_or_secondary_gap_to_target"],
        "required_before_metric_use": [
            "review-only materialization/scoring",
            "expert decision artifact",
            "label-factory gates",
            "batch acceptance",
            "new frozen split or pre-registered eval slice",
        ],
    }


def _empty_support(bin_name: str) -> dict[str, Any]:
    return {
        "row_count": 0,
        "primary_support_count": 0,
        "primary_abstention_count": 0,
        "primary_accuracy_available": None,
        "oos_or_secondary_support_count": 0,
        "oos_or_secondary_false_positive_rate_available": None,
        "row_ids": [],
        "bin": bin_name,
    }


def _bin_priority(primary_gap: int, oos_gap: int) -> str:
    if primary_gap and oos_gap:
        return "high_primary_and_oos_gap"
    if oos_gap:
        return "high_oos_control_gap"
    if primary_gap:
        return "primary_support_gap"
    return "target_met_for_current_policy"


def _markdown_report(plan: dict[str, Any]) -> str:
    lines = [
        "# Bin-targeted Expansion Plan",
        "",
        f"Run: {plan['created_utc']}",
        "",
        "Review-only plan. No labels, registries, imports, production scoring, or thresholds were changed.",
        "",
        "## Current Gaps",
        "",
        "| Bin | Primary | Primary gap | OOS/sec | OOS/sec gap | Priority |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in plan["current_bins"]:
        support = row["current_support"]
        lines.append(
            "| "
            + " | ".join(
                [
                    row["bin"],
                    str(support["primary_support_count"]),
                    str(row["primary_gap_to_target"]),
                    str(support["oos_or_secondary_support_count"]),
                    str(row["oos_or_secondary_gap_to_target"]),
                    row["priority"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"First batch: `{plan['recommendation']['first_batch']}`.",
            plan["recommendation"]["rationale"],
            "",
            "Required before metric use: "
            + ", ".join(plan["recommendation"]["required_before_metric_use"])
            + ".",
            "",
        ]
    )
    return "\n".join(lines)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
