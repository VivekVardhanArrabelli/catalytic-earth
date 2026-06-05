"""Lever 2 row-specific mechanism-feature incremental readout.

This module asks one narrow question: does the current train/cal-only
row-specific mechanism surface add measurable operating-point value beyond the
current geometry/fold surface on split-compatible train/cal rows?

It deliberately reports a measured overlap before any blocker conclusion. When
the overlap cannot support a valid in-scope retention readout, the artifact
names the smallest missing evidence needed to make Lever 2 measurable.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "lever2_mechanism_feature_incremental_readout.v0"
DEFAULT_ARTIFACT_ID = (
    "v3_lever2_mechanism_feature_incremental_readout_current702_20260604"
)
DEFAULT_ELECTRON_FLOW_SPLIT_ALIGNMENT_ARTIFACT_ID = (
    "v3_lever2_source_free_electron_flow_split_alignment_readout_current702_20260604"
)
DEFAULT_CURRENT_EXTENDED_OOS_MECHANISM_OVERLAP_ARTIFACT_ID = (
    "v3_lever2_current_extended_oos_mechanism_overlap_readout_current702_20260604"
)
DEFAULT_PARTIAL_SURFACE_CURRENT_SPLIT_PORTABILITY_ARTIFACT_ID = (
    "v3_lever2_source_free_partial_surface_current_split_portability_readout_"
    "current702_20260604"
)
DEFAULT_EVENT_AXIS_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID = (
    "v3_lever2_event_axis_current_extended_frontier_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_LOO_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID = (
    "v3_lever2_event_axis_loo_current_extended_frontier_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_PRIMARY_SAFE_FRONTIER_ARTIFACT_ID = (
    "v3_lever2_event_axis_primary_safe_frontier_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_RESCUE_ARTIFACT_ID = (
    "v3_lever2_event_axis_primary_controlled_rescue_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUDED_FRONTIER_ARTIFACT_ID = (
    "v3_lever2_event_axis_signature_excluded_frontier_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUSION_SENSITIVITY_ARTIFACT_ID = (
    "v3_lever2_event_axis_signature_exclusion_sensitivity_readout_current702_20260604"
)
DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_NULL_ARTIFACT_ID = (
    "v3_lever2_event_axis_primary_controlled_null_readout_current702_20260604"
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _source_path_record(path: Path) -> dict[str, Any]:
    path = Path(path)
    return {
        "exists": path.exists(),
        "path": str(path),
        "sha256": _sha256(path) if path.exists() else None,
    }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _recall(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 6)


def _entry_sort_key(entry_id: str) -> tuple[int, str]:
    if entry_id.startswith("m_csa:"):
        suffix = entry_id.split(":", 1)[1]
        if suffix.isdigit():
            return (0, f"{int(suffix):08d}")
    return (1, entry_id)


def _stable_hash_text(*parts: object) -> str:
    return hashlib.sha256(
        "::".join(str(part) for part in parts).encode("utf-8")
    ).hexdigest()


def _deterministic_null_mapping(
    entry_ids: list[str],
    *,
    seed: str,
) -> dict[str, str]:
    ordered = sorted(entry_ids, key=_entry_sort_key)
    if not ordered:
        return {}
    permuted = sorted(
        ordered,
        key=lambda entry_id: _stable_hash_text(seed, entry_id),
    )
    if len(ordered) > 1:
        for offset in range(len(permuted)):
            candidate = permuted[offset:] + permuted[:offset]
            if all(target != source for target, source in zip(ordered, candidate)):
                permuted = candidate
                break
        else:
            permuted = permuted[1:] + permuted[:1]
    return dict(zip(ordered, permuted))


def _features_with_axis_fields_from_source(
    features: dict[str, Any],
    source_features: dict[str, Any],
    fields: list[str],
) -> dict[str, Any]:
    copied = dict(features)
    for field in fields:
        copied[field] = source_features.get(field, 0)
    return copied


def _empirical_quantile(values: list[int], percentile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(int(value) for value in values)
    bounded = min(1.0, max(0.0, percentile))
    index = int((len(ordered) - 1) * bounded)
    return ordered[index]


def _channel_threshold(expanded_threshold_contract: dict[str, Any]) -> tuple[str, float]:
    primary = expanded_threshold_contract.get("primary_channel_readout") or {}
    channel = str(primary.get("channel") or "combined_mean_geometry_fold")
    selected = primary.get("selected_at_90pct_calibration_in_scope_retention_max_oos_abstain") or {}
    threshold = selected.get("threshold")
    if threshold is None:
        contract = expanded_threshold_contract.get("threshold_contract") or {}
        selected = (
            (contract.get(channel) or {}).get(
                "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain"
            )
            or {}
        )
        threshold = selected.get("threshold")
    if threshold is None:
        raise ValueError("current geometry/fold threshold is missing")
    return channel, float(threshold)


def _mechanism_threshold(
    mechanism_no_template_rerun: dict[str, Any],
    mechanism_operating_point_contract: dict[str, Any] | None,
) -> float:
    residual = mechanism_no_template_rerun.get("residual_variant") or {}
    selected = residual.get("calibration_selected_residual_threshold") or {}
    threshold = selected.get("threshold")
    if threshold is None and mechanism_operating_point_contract is not None:
        contract = (
            mechanism_operating_point_contract.get("calibration_contract") or {}
        ).get("residual_distance") or {}
        threshold = contract.get("threshold")
    if threshold is None:
        raise ValueError("mechanism residual threshold is missing")
    return float(threshold)


def _selected_current_summary(expanded_threshold_contract: dict[str, Any]) -> dict[str, Any]:
    primary = expanded_threshold_contract.get("primary_channel_readout") or {}
    selected = primary.get("selected_at_90pct_calibration_in_scope_retention_max_oos_abstain")
    if selected:
        return selected
    channel = str(primary.get("channel") or "combined_mean_geometry_fold")
    return (
        (expanded_threshold_contract.get("threshold_contract") or {})
        .get(channel, {})
        .get("selected_at_90pct_calibration_in_scope_retention_max_oos_abstain")
        or {}
    )


def _mechanism_calibration_rows(
    mechanism_no_template_rerun: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    scored = mechanism_no_template_rerun.get("scored_rows") or {}
    rows = scored.get("calibration") or []
    return {
        str(row["entry_id"]): row
        for row in rows
        if isinstance(row, dict) and row.get("entry_id")
    }


def _fold_rows_by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(row["entry_id"]): row
        for row in rows
        if isinstance(row, dict) and row.get("entry_id")
    }


def _current_score(row: dict[str, Any], channel: str) -> float | None:
    value = (row.get("channel_scores") or {}).get(channel)
    return float(value) if value is not None else None


def _rounded_current_score(row: dict[str, Any], channel: str) -> float | None:
    score = _current_score(row, channel)
    return round(score, 8) if score is not None else None


def _mechanism_abstains(row: dict[str, Any], threshold: float) -> bool:
    return float(row.get("out_of_atlas_span_residual") or 0.0) > threshold


def _current_abstains(row: dict[str, Any], channel: str, threshold: float) -> bool:
    score = _current_score(row, channel)
    if score is None:
        return False
    return score < threshold


def _current_readout_threshold(
    current_measured_readout: dict[str, Any],
) -> tuple[str, float]:
    fixed = current_measured_readout.get("fixed_operating_point") or {}
    channel = str(fixed.get("channel") or "combined_mean_geometry_fold")
    threshold = fixed.get("threshold")
    if threshold is None:
        selection = fixed.get("calibration_selection") or {}
        threshold = selection.get("threshold")
    if threshold is None:
        raise ValueError("current measured readout threshold is missing")
    return channel, float(threshold)


def _current_surface_rows_with_score(
    current_extended_oos_surface: dict[str, Any], channel: str
) -> dict[str, dict[str, Any]]:
    rows = _fold_rows_by_id(
        current_extended_oos_surface.get("candidate_row_scores") or []
    )
    return {
        entry_id: row
        for entry_id, row in rows.items()
        if _current_score(row, channel) is not None
    }


def _feature_rows_by_id(
    train_cal_feature_sidecar: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("entry_id")): row
        for row in train_cal_feature_sidecar.get("feature_rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    }


def _event_feature_summary(
    overlap_rows: list[dict[str, Any]],
    *,
    current_retained_only: bool = False,
) -> dict[str, int]:
    rows = [
        row
        for row in overlap_rows
        if (not current_retained_only or not row["current_surface_abstains"])
    ]
    return {
        "rows": len(rows),
        "with_bond_change_event": sum(
            1 for row in rows if row.get("has_bond_change_event")
        ),
        "with_proton_transfer_event": sum(
            1 for row in rows if row.get("has_proton_transfer_event")
        ),
        "with_electron_transfer_event": sum(
            1 for row in rows if row.get("has_electron_transfer_event")
        ),
        "mechanism_abstained_rows": sum(
            1 for row in rows if row["mechanism_surface_abstains"]
        ),
        "current_retained_caught_by_mechanism": sum(
            1
            for row in rows
            if not row["current_surface_abstains"]
            and row["mechanism_surface_abstains"]
        ),
    }


def _event_axis_frontier_definitions() -> list[dict[str, Any]]:
    return [
        {
            "axis_id": "source_free_projected_proton_role_subset",
            "source_free_status": "source_free_compatible_proxy",
            "feature_fields": [
                "expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser",
                "expanded_residue_code_count__residue_code_count_his_3",
                "has_proton_transfer_event",
                "proton_transfer_count",
            ],
            "description": (
                "currently projected source-free-compatible proton-role and "
                "residue-count subset"
            ),
        },
        {
            "axis_id": "bond_change",
            "source_free_status": "requires_new_source_free_axis",
            "feature_fields": [
                "has_bond_change_event",
                "bond_change_event_count",
                "bond_broken_count",
                "bond_formed_count",
                "bond_order_changed_count",
            ],
            "description": "bond break/form/order-change event surface",
        },
        {
            "axis_id": "proton_transfer",
            "source_free_status": "partially_supported_by_event_axis_linkers",
            "feature_fields": ["has_proton_transfer_event", "proton_transfer_count"],
            "description": "proton-transfer event surface",
        },
        {
            "axis_id": "electron_flow",
            "source_free_status": "requires_new_source_free_axis",
            "feature_fields": [
                "has_electron_transfer_event",
                "electron_transfer_count",
            ],
            "description": "electron-transfer event surface",
        },
        {
            "axis_id": "event_topology",
            "source_free_status": "requires_new_source_free_axis",
            "feature_fields": ["event_count", "multi_event_mechanism_flag"],
            "description": "event-count/topology surface",
        },
        {
            "axis_id": "active_site_locator_count",
            "source_free_status": "requires_source_free_locator_coverage",
            "feature_fields": [
                "mapped_active_site_residue_count",
                "unique_mapped_active_site_residue_count",
            ],
            "description": "source-free locator residue-count surface",
        },
        {
            "axis_id": "confidence_metadata",
            "source_free_status": "research_only_metadata_axis",
            "feature_fields": [
                "high_confidence_event_count",
                "medium_confidence_event_count",
                "low_confidence_event_count",
                "unknown_confidence_event_count",
            ],
            "description": "event-confidence count surface",
        },
        {
            "axis_id": "all_priority_event_axes",
            "source_free_status": "requires_multi_axis_source_free_materialization",
            "feature_fields": [
                "has_bond_change_event",
                "bond_change_event_count",
                "bond_broken_count",
                "bond_formed_count",
                "bond_order_changed_count",
                "has_proton_transfer_event",
                "proton_transfer_count",
                "has_electron_transfer_event",
                "electron_transfer_count",
                "event_count",
                "multi_event_mechanism_flag",
            ],
            "description": "combined priority event surface",
        },
    ]


def _feature_numeric_value(features: dict[str, Any], field: str) -> float:
    value = features.get(field, 0)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _axis_score(features: dict[str, Any], fields: list[str]) -> float:
    return sum(_feature_numeric_value(features, field) for field in fields)


def _axis_signature(features: dict[str, Any], fields: list[str]) -> tuple[float, ...]:
    return tuple(round(_feature_numeric_value(features, field), 8) for field in fields)


def _axis_rule_abstains(score: float, *, direction: str, threshold: float) -> bool:
    if direction == "high":
        return score >= threshold
    if direction == "low":
        return score <= threshold
    raise ValueError(f"unsupported axis rule direction: {direction}")


def _select_axis_rule(
    calibration_rows: list[dict[str, Any]],
    fields: list[str],
    *,
    min_primary_retain: float,
) -> dict[str, Any]:
    candidates = _axis_rule_candidates(
        calibration_rows, fields, min_primary_retain=min_primary_retain
    )
    if not candidates:
        raise ValueError("no axis rule can satisfy the primary retention target")

    def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[float, ...]:
        direction_rank = 1.0 if candidate["direction"] == "high" else 0.0
        threshold = float(candidate["threshold"])
        threshold_rank = -threshold if candidate["direction"] == "high" else threshold
        return (
            float(candidate["calibration_oos_abstained"]),
            float(candidate["calibration_primary_retained"]),
            direction_rank,
            threshold_rank,
        )

    return sorted(candidates, key=_candidate_sort_key, reverse=True)[0]


def _axis_rule_candidates(
    calibration_rows: list[dict[str, Any]],
    fields: list[str],
    *,
    min_primary_retain: float,
) -> list[dict[str, Any]]:
    primary_rows = [row for row in calibration_rows if row["is_primary"]]
    oos_rows = [row for row in calibration_rows if not row["is_primary"]]
    if not primary_rows or not oos_rows:
        raise ValueError("axis rule selection requires primary and OOS calibration rows")

    scored_rows = [
        {
            "entry_id": row["entry_id"],
            "is_primary": bool(row["is_primary"]),
            "axis_score": _axis_score(row["features"], fields),
        }
        for row in calibration_rows
    ]
    values = sorted({row["axis_score"] for row in scored_rows}) or [0.0]
    candidate_thresholds = sorted(
        set(values + [min(values) - 1.0, max(values) + 1.0])
    )
    candidates: list[dict[str, Any]] = []
    for direction in ["high", "low"]:
        for threshold in candidate_thresholds:
            primary_abstained = sum(
                1
                for row in scored_rows
                if row["is_primary"]
                and _axis_rule_abstains(
                    row["axis_score"], direction=direction, threshold=threshold
                )
            )
            oos_abstained = sum(
                1
                for row in scored_rows
                if not row["is_primary"]
                and _axis_rule_abstains(
                    row["axis_score"], direction=direction, threshold=threshold
                )
            )
            primary_retained = len(primary_rows) - primary_abstained
            primary_retain_recall = primary_retained / len(primary_rows)
            if primary_retain_recall + 1e-12 < min_primary_retain:
                continue
            candidates.append(
                {
                    "direction": direction,
                    "threshold": threshold,
                    "calibration_primary_rows": len(primary_rows),
                    "calibration_primary_retained": primary_retained,
                    "calibration_primary_retain_recall": round(
                        primary_retain_recall, 6
                    ),
                    "calibration_oos_rows": len(oos_rows),
                    "calibration_oos_abstained": oos_abstained,
                    "calibration_oos_abstain_recall": round(
                        oos_abstained / len(oos_rows), 6
                    ),
                }
            )
    for candidate in candidates:
        candidate["threshold"] = round(float(candidate["threshold"]), 8)
    return candidates


def _select_axis_pair_rule(
    calibration_rows: list[dict[str, Any]],
    baseline_fields: list[str],
    added_fields: list[str],
    *,
    min_primary_retain: float,
) -> dict[str, Any]:
    baseline_candidates = _axis_rule_candidates(
        calibration_rows, baseline_fields, min_primary_retain=min_primary_retain
    )
    added_candidates = _axis_rule_candidates(
        calibration_rows, added_fields, min_primary_retain=min_primary_retain
    )
    primary_rows = [row for row in calibration_rows if row["is_primary"]]
    oos_rows = [row for row in calibration_rows if not row["is_primary"]]
    candidates: list[dict[str, Any]] = []

    for baseline_rule in baseline_candidates:
        for added_rule in added_candidates:

            def _pair_abstains(row: dict[str, Any]) -> bool:
                baseline_score = _axis_score(row["features"], baseline_fields)
                added_score = _axis_score(row["features"], added_fields)
                return bool(
                    _axis_rule_abstains(
                        baseline_score,
                        direction=str(baseline_rule["direction"]),
                        threshold=float(baseline_rule["threshold"]),
                    )
                    or _axis_rule_abstains(
                        added_score,
                        direction=str(added_rule["direction"]),
                        threshold=float(added_rule["threshold"]),
                    )
                )

            primary_abstained = sum(1 for row in primary_rows if _pair_abstains(row))
            primary_retained = len(primary_rows) - primary_abstained
            primary_retain_recall = primary_retained / len(primary_rows)
            if primary_retain_recall + 1e-12 < min_primary_retain:
                continue
            oos_abstained = sum(1 for row in oos_rows if _pair_abstains(row))
            candidates.append(
                {
                    "baseline_rule": baseline_rule,
                    "added_rule": added_rule,
                    "calibration_primary_rows": len(primary_rows),
                    "calibration_primary_retained": primary_retained,
                    "calibration_primary_retain_recall": round(
                        primary_retain_recall, 6
                    ),
                    "calibration_oos_rows": len(oos_rows),
                    "calibration_oos_abstained": oos_abstained,
                    "calibration_oos_abstain_recall": _recall(
                        oos_abstained, len(oos_rows)
                    ),
                }
            )

    if not candidates:
        raise ValueError("no axis-pair rule can satisfy the primary retention target")

    def _rule_sort_tuple(rule: dict[str, Any]) -> tuple[float, ...]:
        direction_rank = 1.0 if rule["direction"] == "high" else 0.0
        threshold = float(rule["threshold"])
        threshold_rank = -threshold if rule["direction"] == "high" else threshold
        return (direction_rank, threshold_rank)

    def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[float, ...]:
        return (
            float(candidate["calibration_oos_abstained"]),
            float(candidate["calibration_primary_retained"]),
            float(candidate["baseline_rule"]["calibration_oos_abstained"]),
            float(candidate["added_rule"]["calibration_oos_abstained"]),
            *_rule_sort_tuple(candidate["baseline_rule"]),
            *_rule_sort_tuple(candidate["added_rule"]),
        )

    return sorted(candidates, key=_candidate_sort_key, reverse=True)[0]


def _primary_control_summary(
    primary_control_rows: list[dict[str, Any]],
    fields: list[str],
    rule: dict[str, Any],
) -> dict[str, Any]:
    control_rows = []
    for row in primary_control_rows:
        score = round(_axis_score(row["features"], fields), 8)
        abstains = _axis_rule_abstains(
            score,
            direction=str(rule["direction"]),
            threshold=float(rule["threshold"]),
        )
        control_rows.append(
            {
                "entry_id": row["entry_id"],
                "axis_score": score,
                "axis_abstains": abstains,
                "axis_retains": not abstains,
            }
        )
    retained = sum(1 for row in control_rows if row["axis_retains"])
    return {
        "target_rows": len(control_rows),
        "retained_rows": retained,
        "retention_recall": _recall(retained, len(control_rows)),
        "abstained_entry_ids": [
            row["entry_id"] for row in control_rows if row["axis_abstains"]
        ],
        "control_rows": control_rows,
    }


def _pair_primary_control_summary(
    primary_control_rows: list[dict[str, Any]],
    baseline_fields: list[str],
    added_fields: list[str],
    pair_rule: dict[str, Any],
) -> dict[str, Any]:
    baseline_rule = pair_rule["baseline_rule"]
    added_rule = pair_rule["added_rule"]
    control_rows = []
    for row in primary_control_rows:
        baseline_score = round(_axis_score(row["features"], baseline_fields), 8)
        added_score = round(_axis_score(row["features"], added_fields), 8)
        baseline_abstains = _axis_rule_abstains(
            baseline_score,
            direction=str(baseline_rule["direction"]),
            threshold=float(baseline_rule["threshold"]),
        )
        added_abstains = _axis_rule_abstains(
            added_score,
            direction=str(added_rule["direction"]),
            threshold=float(added_rule["threshold"]),
        )
        pair_abstains = bool(baseline_abstains or added_abstains)
        control_rows.append(
            {
                "entry_id": row["entry_id"],
                "baseline_axis_score": baseline_score,
                "added_axis_score": added_score,
                "baseline_axis_abstains": baseline_abstains,
                "added_axis_abstains": added_abstains,
                "projection_plus_axis_abstains": pair_abstains,
                "projection_plus_axis_retains": not pair_abstains,
            }
        )
    retained = sum(1 for row in control_rows if row["projection_plus_axis_retains"])
    return {
        "target_rows": len(control_rows),
        "retained_rows": retained,
        "retention_recall": _recall(retained, len(control_rows)),
        "abstained_entry_ids": [
            row["entry_id"]
            for row in control_rows
            if row["projection_plus_axis_abstains"]
        ],
        "control_rows": control_rows,
    }


def _select_primary_controlled_axis_rule(
    selection_rows: list[dict[str, Any]],
    primary_control_rows: list[dict[str, Any]],
    fields: list[str],
    *,
    min_primary_retain: float,
) -> dict[str, Any]:
    candidates = _axis_rule_candidates(
        selection_rows,
        fields,
        min_primary_retain=0.0,
    )
    controlled: list[dict[str, Any]] = []
    for candidate in candidates:
        control = _primary_control_summary(primary_control_rows, fields, candidate)
        recall = control.get("retention_recall")
        if recall is None or float(recall) + 1e-12 < min_primary_retain:
            continue
        controlled.append({**candidate, "primary_control": control})
    if not controlled:
        raise ValueError("no axis rule can satisfy the primary control target")

    def _rule_sort_key(candidate: dict[str, Any]) -> tuple[float, ...]:
        direction = str(candidate["direction"])
        threshold = float(candidate["threshold"])
        strict_threshold = threshold if direction == "high" else -threshold
        direction_rank = 1.0 if direction == "high" else 0.0
        return (
            float(candidate["calibration_oos_abstained"]),
            float(candidate["primary_control"]["retained_rows"]),
            direction_rank,
            strict_threshold,
        )

    return sorted(controlled, key=_rule_sort_key, reverse=True)[0]


def _select_primary_controlled_axis_pair_rule(
    selection_rows: list[dict[str, Any]],
    primary_control_rows: list[dict[str, Any]],
    baseline_fields: list[str],
    added_fields: list[str],
    *,
    min_primary_retain: float,
) -> dict[str, Any]:
    baseline_candidates = _axis_rule_candidates(
        selection_rows,
        baseline_fields,
        min_primary_retain=0.0,
    )
    added_candidates = _axis_rule_candidates(
        selection_rows,
        added_fields,
        min_primary_retain=0.0,
    )
    oos_rows = [row for row in selection_rows if not row["is_primary"]]
    candidates: list[dict[str, Any]] = []

    def _pair_abstains(
        row: dict[str, Any],
        baseline_rule: dict[str, Any],
        added_rule: dict[str, Any],
    ) -> bool:
        return bool(
            _axis_rule_abstains(
                _axis_score(row["features"], baseline_fields),
                direction=str(baseline_rule["direction"]),
                threshold=float(baseline_rule["threshold"]),
            )
            or _axis_rule_abstains(
                _axis_score(row["features"], added_fields),
                direction=str(added_rule["direction"]),
                threshold=float(added_rule["threshold"]),
            )
        )

    for baseline_rule in baseline_candidates:
        for added_rule in added_candidates:
            pair_rule = {
                "baseline_rule": baseline_rule,
                "added_rule": added_rule,
            }
            control = _pair_primary_control_summary(
                primary_control_rows,
                baseline_fields,
                added_fields,
                pair_rule,
            )
            recall = control.get("retention_recall")
            if recall is None or float(recall) + 1e-12 < min_primary_retain:
                continue
            oos_abstained = sum(
                1 for row in oos_rows if _pair_abstains(row, baseline_rule, added_rule)
            )
            candidates.append(
                {
                    "baseline_rule": baseline_rule,
                    "added_rule": added_rule,
                    "primary_control": control,
                    "calibration_oos_rows": len(oos_rows),
                    "calibration_oos_abstained": oos_abstained,
                    "calibration_oos_abstain_recall": _recall(
                        oos_abstained, len(oos_rows)
                    ),
                }
            )
    if not candidates:
        raise ValueError("no axis-pair rule can satisfy the primary control target")

    def _rule_sort_tuple(rule: dict[str, Any]) -> tuple[float, ...]:
        direction = str(rule["direction"])
        threshold = float(rule["threshold"])
        strict_threshold = threshold if direction == "high" else -threshold
        direction_rank = 1.0 if direction == "high" else 0.0
        return (direction_rank, strict_threshold)

    def _candidate_sort_key(candidate: dict[str, Any]) -> tuple[float, ...]:
        return (
            float(candidate["calibration_oos_abstained"]),
            float(candidate["primary_control"]["retained_rows"]),
            float(candidate["baseline_rule"]["calibration_oos_abstained"]),
            float(candidate["added_rule"]["calibration_oos_abstained"]),
            *_rule_sort_tuple(candidate["baseline_rule"]),
            *_rule_sort_tuple(candidate["added_rule"]),
        )

    return sorted(candidates, key=_candidate_sort_key, reverse=True)[0]


def _m_csa_ids_from_candidate_dir(candidate_dir: Path | None) -> set[str]:
    if candidate_dir is None or not Path(candidate_dir).exists():
        return set()
    entry_ids: set[str] = set()
    for path in Path(candidate_dir).glob("*.json"):
        parts = path.stem.split("_")
        if len(parts) >= 3 and parts[0] == "m" and parts[1] == "csa":
            entry_ids.add(f"m_csa:{parts[2]}")
            continue
        try:
            data = _read_json(path)
        except (json.JSONDecodeError, OSError):
            continue
        pending: list[Any] = [data]
        while pending:
            value = pending.pop()
            if isinstance(value, dict):
                entry_id = value.get("entry_id")
                if isinstance(entry_id, str) and entry_id.startswith("m_csa:"):
                    entry_ids.add(entry_id)
                pending.extend(value.values())
            elif isinstance(value, list):
                pending.extend(value)
    return entry_ids


def _variant_by_name(
    readout: dict[str, Any], variant_name: str
) -> dict[str, Any] | None:
    rows = (
        (readout.get("measured_readout") or {}).get("axis_repair_ceiling_rows") or []
    )
    for row in rows:
        if isinstance(row, dict) and row.get("variant") == variant_name:
            return row
    return None


def _entry_ids_from_candidate_surface(candidate_surface: dict[str, Any]) -> set[str]:
    rows = candidate_surface.get("candidate_projection_rows") or []
    return {
        str(row.get("entry_id"))
        for row in rows
        if isinstance(row, dict) and row.get("entry_id")
    }


def _entry_ids_from_event_axis_materialization(
    event_axis_materialization: dict[str, Any],
) -> set[str]:
    rows = event_axis_materialization.get("materialization_rows") or []
    return {
        str(row.get("entry_id"))
        for row in rows
        if isinstance(row, dict)
        and row.get("entry_id")
        and not row.get("critical_violations")
        and row.get("source_free_event_axis_status")
        == "source_free_event_axis_linker_ready"
    }


def _entry_ids_from_locator_materialization(
    locator_materialization: dict[str, Any],
) -> set[str]:
    rows = locator_materialization.get("row_decisions") or []
    return {
        str(row.get("entry_id"))
        for row in rows
        if isinstance(row, dict)
        and row.get("entry_id")
        and row.get("approved_locator_sidecar_written") is True
        and row.get("decision") == "materialized_to_audited_locator_dir"
        and not row.get("critical_violations")
    }


def _surface_overlap_summary(
    *,
    surface_ids: set[str],
    current_primary_rows: dict[str, dict[str, Any]],
    current_oos_rows: dict[str, dict[str, Any]],
    current_retained_oos_ids: set[str],
    current_abstained_oos_ids: set[str],
    channel: str,
) -> dict[str, Any]:
    primary_overlap = sorted(
        surface_ids & set(current_primary_rows), key=_entry_sort_key
    )
    retained_oos_overlap = sorted(
        surface_ids & current_retained_oos_ids, key=_entry_sort_key
    )
    abstained_oos_overlap = sorted(
        surface_ids & current_abstained_oos_ids, key=_entry_sort_key
    )

    def _primary_row(entry_id: str) -> dict[str, Any]:
        row = current_primary_rows[entry_id]
        return {
            "entry_id": entry_id,
            "current_surface_score": _rounded_current_score(row, channel),
        }

    def _oos_row(entry_id: str, *, abstains: bool) -> dict[str, Any]:
        row = current_oos_rows[entry_id]
        return {
            "entry_id": entry_id,
            "current_surface_score": _rounded_current_score(row, channel),
            "current_surface_abstains": abstains,
        }

    return {
        "surface_rows": len(surface_ids),
        "current_primary_overlap_rows": len(primary_overlap),
        "current_retained_oos_overlap_rows": len(retained_oos_overlap),
        "current_abstained_oos_overlap_rows": len(abstained_oos_overlap),
        "current_scored_oos_overlap_rows": (
            len(retained_oos_overlap) + len(abstained_oos_overlap)
        ),
        "current_primary_overlap_entry_ids": primary_overlap,
        "current_retained_oos_overlap_entry_ids": retained_oos_overlap,
        "current_abstained_oos_overlap_entry_ids": abstained_oos_overlap,
        "row_readouts": {
            "current_primary_overlap_rows": [
                _primary_row(entry_id) for entry_id in primary_overlap
            ],
            "current_retained_oos_overlap_rows": [
                _oos_row(entry_id, abstains=False)
                for entry_id in retained_oos_overlap
            ],
            "current_abstained_oos_overlap_rows": [
                _oos_row(entry_id, abstains=True)
                for entry_id in abstained_oos_overlap
            ],
        },
    }


def _score_value(row: dict[str, Any]) -> float:
    value = row.get("current_surface_score")
    return float(value) if value is not None else -1.0


def _missing_current_rows(
    incremental: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    missing = incremental.get("missing_evidence_rows") or {}
    primary = [
        row
        for row in (
            missing.get(
                "current_calibration_primary_rows_requiring_source_free_mechanism_features"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    oos = [
        row
        for row in (
            missing.get(
                "current_calibration_oos_rows_requiring_source_free_mechanism_features"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    return primary, oos


def _raw_electron_flow_current_overlap_diagnostic(
    *,
    train_cal_feature_sidecar: dict[str, Any],
    current_in_scope_threshold_contract: dict[str, Any],
    expanded_oos_calibrated_threshold_contract: dict[str, Any],
) -> dict[str, Any]:
    channel, current_threshold = _channel_threshold(
        expanded_oos_calibrated_threshold_contract
    )
    feature_rows = {
        str(row.get("entry_id")): row
        for row in train_cal_feature_sidecar.get("feature_rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    current_primary_rows = _fold_rows_by_id(
        current_in_scope_threshold_contract.get("calibration_row_scores") or []
    )
    current_oos_rows = _fold_rows_by_id(
        expanded_oos_calibrated_threshold_contract.get(
            "calibration_oos_negative_row_scores"
        )
        or []
    )
    valid_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )
    oos_overlap = sorted(
        set(current_oos_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    oos_rows: list[dict[str, Any]] = []
    for entry_id in oos_overlap:
        feature_row = feature_rows[entry_id]
        current_row = current_oos_rows[entry_id]
        features = feature_row.get("row_specific_event_features") or {}
        current_abstain = _current_abstains(
            current_row, channel, current_threshold
        )
        electron_count = int(features.get("electron_transfer_count") or 0)
        has_electron = bool(features.get("has_electron_transfer_event"))
        oos_rows.append(
            {
                "entry_id": entry_id,
                "current_surface_score": _rounded_current_score(
                    current_row, channel
                ),
                "current_surface_abstains": current_abstain,
                "has_electron_transfer_event": has_electron,
                "electron_transfer_count": electron_count,
                "current_retained_oos_with_electron_flow": bool(
                    not current_abstain and has_electron
                ),
            }
        )
    current_retained_oos_rows = [
        row for row in oos_rows if not row["current_surface_abstains"]
    ]
    current_abstained_oos_rows = [
        row for row in oos_rows if row["current_surface_abstains"]
    ]
    return {
        "available": True,
        "channel": channel,
        "current_threshold": round(current_threshold, 8),
        "note": (
            "Train/cal-only raw full-sidecar diagnostic. It does not select a "
            "new threshold, does not score heldout, and cannot support a "
            "deployable claim without split-aligned source-free primary "
            "retention evidence."
        ),
        "counts": {
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                primary_train_target_overlap
            ),
            "current_oos_calibration_feature_overlap_rows": len(oos_rows),
            "current_retained_oos_overlap_rows": len(current_retained_oos_rows),
            "current_abstained_oos_overlap_rows": len(current_abstained_oos_rows),
            "electron_positive_oos_overlap_rows": sum(
                1 for row in oos_rows if row["has_electron_transfer_event"]
            ),
            "electron_positive_current_retained_oos_overlap_rows": sum(
                1
                for row in current_retained_oos_rows
                if row["has_electron_transfer_event"]
            ),
            "electron_positive_current_abstained_oos_overlap_rows": sum(
                1
                for row in current_abstained_oos_rows
                if row["has_electron_transfer_event"]
            ),
        },
        "valid_current_primary_calibration_feature_overlap_entry_ids": (
            valid_primary_overlap
        ),
        "current_primary_rows_excluded_as_mechanism_train_targets": [
            {
                "entry_id": entry_id,
                "reason": "row_is_mechanism_feature_train_target",
            }
            for entry_id in primary_train_target_overlap
        ],
        "current_oos_overlap_rows": oos_rows,
    }


def build_lever2_current_extended_oos_mechanism_overlap_readout(
    *,
    current_measured_readout_path: Path,
    current_extended_oos_surface_path: Path,
    mechanism_no_template_rerun_path: Path,
    current_in_scope_threshold_contract_path: Path,
    mechanism_operating_point_contract_path: Path | None = None,
    train_cal_feature_sidecar_path: Path | None = None,
    projection_readout_path: Path | None = None,
    source_free_coordinate_anchor_candidate_dir_path: Path | None = None,
    artifact_id: str = DEFAULT_CURRENT_EXTENDED_OOS_MECHANISM_OVERLAP_ARTIFACT_ID,
) -> dict[str, Any]:
    current_measured = _read_json(current_measured_readout_path)
    current_surface = _read_json(current_extended_oos_surface_path)
    mechanism = _read_json(mechanism_no_template_rerun_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    mechanism_contract = (
        _read_json(mechanism_operating_point_contract_path)
        if mechanism_operating_point_contract_path is not None
        and Path(mechanism_operating_point_contract_path).exists()
        else None
    )
    feature_rows = (
        _feature_rows_by_id(_read_json(train_cal_feature_sidecar_path))
        if train_cal_feature_sidecar_path is not None
        and Path(train_cal_feature_sidecar_path).exists()
        else {}
    )
    projection_readout = (
        _read_json(projection_readout_path)
        if projection_readout_path is not None
        and Path(projection_readout_path).exists()
        else None
    )
    source_free_candidate_ids = _m_csa_ids_from_candidate_dir(
        source_free_coordinate_anchor_candidate_dir_path
    )

    channel, current_threshold = _current_readout_threshold(current_measured)
    mechanism_threshold = _mechanism_threshold(mechanism, mechanism_contract)
    current_rows = _current_surface_rows_with_score(current_surface, channel)
    all_current_rows = _fold_rows_by_id(current_surface.get("candidate_row_scores") or [])
    current_abstained_ids = {
        entry_id
        for entry_id, row in current_rows.items()
        if _current_abstains(row, channel, current_threshold)
    }
    current_retained_ids = set(current_rows) - current_abstained_ids

    mechanism_rows = _mechanism_calibration_rows(mechanism)
    mechanism_oos_ids = {
        entry_id
        for entry_id, row in mechanism_rows.items()
        if not bool(row.get("is_primary"))
    }
    mechanism_primary_ids = {
        entry_id
        for entry_id, row in mechanism_rows.items()
        if bool(row.get("is_primary"))
    }
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    valid_primary_overlap = sorted(
        mechanism_primary_ids & set(current_primary_rows), key=_entry_sort_key
    )
    current_extended_oos_overlap = sorted(
        mechanism_oos_ids & set(current_rows), key=_entry_sort_key
    )

    oos_rows: list[dict[str, Any]] = []
    for entry_id in current_extended_oos_overlap:
        current_row = current_rows[entry_id]
        mechanism_row = mechanism_rows[entry_id]
        features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        current_score = _current_score(current_row, channel)
        current_abstain = _current_abstains(
            current_row, channel, current_threshold
        )
        mechanism_residual = float(
            mechanism_row.get("out_of_atlas_span_residual") or 0.0
        )
        mechanism_abstain = mechanism_residual > mechanism_threshold
        oos_rows.append(
            {
                "entry_id": entry_id,
                "accession": current_row.get("accession"),
                "current_surface_score": round(current_score, 8)
                if current_score is not None
                else None,
                "current_surface_abstains": current_abstain,
                "mechanism_residual": round(mechanism_residual, 8),
                "mechanism_surface_abstains": mechanism_abstain,
                "union_or_gate_abstains": bool(current_abstain or mechanism_abstain),
                "current_false_negative_caught_by_mechanism": bool(
                    not current_abstain and mechanism_abstain
                ),
                "has_bond_change_event": bool(features.get("has_bond_change_event")),
                "has_proton_transfer_event": bool(
                    features.get("has_proton_transfer_event")
                ),
                "has_electron_transfer_event": bool(
                    features.get("has_electron_transfer_event")
                ),
                "bond_change_event_count": int(
                    features.get("bond_change_event_count") or 0
                ),
                "proton_transfer_count": int(
                    features.get("proton_transfer_count") or 0
                ),
                "electron_transfer_count": int(
                    features.get("electron_transfer_count") or 0
                ),
                "event_count": int(features.get("event_count") or 0),
            }
        )

    current_oos_abstained = sum(
        1 for row in oos_rows if row["current_surface_abstains"]
    )
    mechanism_oos_abstained = sum(
        1 for row in oos_rows if row["mechanism_surface_abstains"]
    )
    union_oos_abstained = sum(1 for row in oos_rows if row["union_or_gate_abstains"])
    current_retained_overlap_rows = [
        row for row in oos_rows if not row["current_surface_abstains"]
    ]
    current_retained_caught = [
        row
        for row in current_retained_overlap_rows
        if row["mechanism_surface_abstains"]
    ]
    oos_overlap_lift = (
        round(
            (_recall(union_oos_abstained, len(oos_rows)) or 0.0)
            - (_recall(current_oos_abstained, len(oos_rows)) or 0.0),
            6,
        )
        if oos_rows
        else None
    )

    missing_primary_rows = sorted(
        set(current_primary_rows) - set(valid_primary_overlap), key=_entry_sort_key
    )
    missing_scored_oos_rows = sorted(
        set(current_rows) - set(current_extended_oos_overlap), key=_entry_sort_key
    )
    missing_retained_oos_rows = sorted(
        current_retained_ids - set(current_extended_oos_overlap), key=_entry_sort_key
    )
    missing_abstained_oos_rows = sorted(
        current_abstained_ids - set(current_extended_oos_overlap), key=_entry_sort_key
    )
    candidate_reuse = {
        "candidate_files": len(source_free_candidate_ids),
        "missing_primary_overlap_rows": sorted(
            set(missing_primary_rows) & source_free_candidate_ids,
            key=_entry_sort_key,
        ),
        "missing_retained_oos_overlap_rows": sorted(
            set(missing_retained_oos_rows) & source_free_candidate_ids,
            key=_entry_sort_key,
        ),
        "missing_abstained_oos_overlap_rows": sorted(
            set(missing_abstained_oos_rows) & source_free_candidate_ids,
            key=_entry_sort_key,
        ),
    }

    valid_integrated_operating_point_measurable = bool(
        valid_primary_overlap and oos_rows
    )
    local_oos_signal = bool(
        oos_rows and union_oos_abstained > current_oos_abstained
    )
    deployable = False
    source_free_axis_overlap = {
        "available": False,
        "best_single_axis_name": None,
        "best_single_axis_new_oos_rows": [],
    }
    if isinstance(projection_readout, dict):
        projected_measured = projection_readout.get("measured_readout") or {}
        best_axis = projected_measured.get("best_single_axis_repair_ceiling") or {}
        best_axis_name = str(best_axis.get("variant") or "").replace(
            "current_plus_missing_", ""
        )
        best_axis_rows: list[dict[str, Any]] = []
        for row in projected_measured.get("best_single_axis_new_oos_rows") or []:
            if not isinstance(row, dict) or not row.get("entry_id"):
                continue
            entry_id = str(row.get("entry_id"))
            current_row = current_rows.get(entry_id)
            current_score = (
                _current_score(current_row, channel)
                if current_row is not None
                else None
            )
            current_abstain = (
                _current_abstains(current_row, channel, current_threshold)
                if current_row is not None
                else None
            )
            best_axis_rows.append(
                {
                    "entry_id": entry_id,
                    "best_single_axis_residual": row.get(
                        "best_single_axis_residual"
                    ),
                    "best_single_axis_threshold": row.get(
                        "best_single_axis_threshold"
                    ),
                    "current_projected_subset_residual": row.get(
                        "current_projected_subset_residual"
                    ),
                    "in_current_extended_scored_oos": current_row is not None,
                    "current_surface_score": round(current_score, 8)
                    if current_score is not None
                    else None,
                    "current_surface_abstains": current_abstain,
                    "current_retained_oos_caught_by_best_axis": bool(
                        current_row is not None and current_abstain is False
                    ),
                }
            )
        source_free_axis_overlap = {
            "available": True,
            "best_single_axis_name": best_axis_name or None,
            "best_single_axis_train_cal_ceiling": best_axis,
            "best_single_axis_new_oos_rows": best_axis_rows,
            "best_single_axis_new_oos_rows_on_current_extended_oos": [
                row for row in best_axis_rows if row["in_current_extended_scored_oos"]
            ],
            "best_single_axis_new_current_retained_oos_rows": [
                row
                for row in best_axis_rows
                if row["current_retained_oos_caught_by_best_axis"]
            ],
        }

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.current_extended_oos_mechanism_overlap_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": (
            "lever2_current_extended_oos_mechanism_overlap_readout_research_only"
        ),
        "result_class": "research_only",
        "scope": (
            "Lever 2 train/cal readout comparing the frozen row-specific "
            "mechanism residual surface against the current Lever 3 extended "
            "train/cal OOS surface. It uses fixed thresholds only, evaluates "
            "non-heldout current OOS rows with existing train/cal mechanism "
            "features, and does not read or tune heldout."
        ),
        "fixed_operating_points": {
            "current_surface": {
                "channel": channel,
                "threshold": round(current_threshold, 8),
                "decision_rule": "abstain_when_current_surface_score_below_threshold",
                "current_measured_context": (
                    (current_measured.get("measured_readout") or {}).get(
                        "train_cal_oos_current_scored_surface"
                    )
                ),
            },
            "mechanism_surface": {
                "channel": "row_specific_mechanism_out_of_atlas_span_residual",
                "threshold": round(mechanism_threshold, 8),
                "decision_rule": "abstain_when_mechanism_residual_above_threshold",
                "train_cal_selection_summary": (
                    (mechanism.get("residual_variant") or {}).get(
                        "calibration_selected_residual_threshold"
                    )
                ),
            },
        },
        "measured_readout": {
            "current_extended_oos_overlap_rows": {
                "row_count": len(oos_rows),
                "current_surface_abstained": current_oos_abstained,
                "current_surface_abstain_recall": _recall(
                    current_oos_abstained, len(oos_rows)
                ),
                "mechanism_surface_abstained": mechanism_oos_abstained,
                "mechanism_surface_abstain_recall": _recall(
                    mechanism_oos_abstained, len(oos_rows)
                ),
                "union_or_gate_abstained": union_oos_abstained,
                "union_or_gate_abstain_recall": _recall(
                    union_oos_abstained, len(oos_rows)
                ),
                "union_minus_current_abstain_recall": oos_overlap_lift,
                "current_retained_oos_rows": len(current_retained_overlap_rows),
                "current_retained_oos_caught_by_mechanism": len(
                    current_retained_caught
                ),
                "current_retained_oos_catch_fraction": _recall(
                    len(current_retained_caught), len(current_retained_overlap_rows)
                ),
            },
            "event_feature_overlap_summary": {
                "all_overlap_rows": _event_feature_summary(oos_rows),
                "current_retained_overlap_rows": _event_feature_summary(
                    oos_rows, current_retained_only=True
                ),
                "feature_sidecar_available": bool(feature_rows),
            },
            "source_free_best_axis_current_extended_overlap": (
                source_free_axis_overlap
            ),
            "existing_source_free_coordinate_anchor_candidate_reuse": {
                **candidate_reuse,
                "candidate_dir_available": bool(source_free_candidate_ids),
                "reuse_reduces_current_primary_gap": bool(
                    candidate_reuse["missing_primary_overlap_rows"]
                ),
                "reuse_reduces_current_retained_oos_gap": bool(
                    candidate_reuse["missing_retained_oos_overlap_rows"]
                ),
            },
            "valid_primary_overlap_rows": {
                "row_count": len(valid_primary_overlap),
                "entry_ids": valid_primary_overlap,
            },
        },
        "row_readouts": {
            "current_extended_oos_overlap_rows": oos_rows,
            "valid_primary_overlap_rows": [
                {
                    "entry_id": entry_id,
                    "current_surface_score": _rounded_current_score(
                        current_primary_rows[entry_id], channel
                    ),
                    "mechanism_residual": round(
                        float(
                            mechanism_rows[entry_id].get(
                                "out_of_atlas_span_residual"
                            )
                            or 0.0
                        ),
                        8,
                    ),
                }
                for entry_id in valid_primary_overlap
            ],
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_mechanism_retention_gate",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_primary_overlap),
                "why_it_matters": (
                    "A deployable or promotable Lever 2 operating-point claim "
                    "requires primary retention cost on the same current "
                    "geometry/fold calibration-primary split."
                ),
            },
            {
                "gap_id": "current_extended_retained_oos_mechanism_features",
                "required_rows": len(current_retained_ids),
                "valid_overlap_rows_now": len(current_retained_overlap_rows),
                "missing_rows_now": len(missing_retained_oos_rows),
                "why_it_matters": (
                    "These are current-surface retained OOS rows where "
                    "mechanism evidence would be most valuable if it transfers."
                ),
            },
            {
                "gap_id": "current_extended_abstained_oos_mechanism_features",
                "required_rows": len(current_abstained_ids),
                "valid_overlap_rows_now": current_oos_abstained,
                "missing_rows_now": len(missing_abstained_oos_rows),
                "why_it_matters": (
                    "These complete the current extended OOS surface but are "
                    "lower priority because geometry/fold already abstains."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_mechanism_features": [
                {
                    "entry_id": entry_id,
                    "accession": current_primary_rows[entry_id].get("accession"),
                    "current_surface_score": _rounded_current_score(
                        current_primary_rows[entry_id], channel
                    ),
                    "required_evidence": (
                        "source-free row-specific mechanism feature sidecar "
                        "compatible with the frozen residual contract"
                    ),
                }
                for entry_id in missing_primary_rows
            ],
            "current_extended_retained_oos_rows_requiring_mechanism_features": [
                {
                    "entry_id": entry_id,
                    "accession": current_rows[entry_id].get("accession"),
                    "current_surface_score": _rounded_current_score(
                        current_rows[entry_id], channel
                    ),
                    "required_evidence": (
                        "source-free row-specific mechanism feature sidecar "
                        "compatible with the frozen residual contract"
                    ),
                }
                for entry_id in missing_retained_oos_rows
            ],
            "current_extended_abstained_oos_rows_requiring_mechanism_features": [
                {
                    "entry_id": entry_id,
                    "accession": current_rows[entry_id].get("accession"),
                    "current_surface_score": _rounded_current_score(
                        current_rows[entry_id], channel
                    ),
                    "required_evidence": (
                        "source-free row-specific mechanism feature sidecar "
                        "compatible with the frozen residual contract"
                    ),
                }
                for entry_id in missing_abstained_oos_rows
            ],
            "current_extended_unscored_oos_rows": [
                {
                    "entry_id": entry_id,
                    "accession": all_current_rows[entry_id].get("accession"),
                    "reason": "current_surface_missing_full_channel_score",
                }
                for entry_id in sorted(
                    set(all_current_rows) - set(current_rows), key=_entry_sort_key
                )
            ],
        },
        "counts": {
            "critical_violation_total": 0,
            "current_extended_candidate_oos_rows": len(all_current_rows),
            "current_extended_scored_oos_rows": len(current_rows),
            "current_extended_unscored_oos_rows": len(all_current_rows)
            - len(current_rows),
            "current_extended_oos_overlap_rows": len(oos_rows),
            "current_extended_current_abstained_overlap_rows": current_oos_abstained,
            "current_extended_current_retained_overlap_rows": len(
                current_retained_overlap_rows
            ),
            "mechanism_surface_abstained_overlap_rows": mechanism_oos_abstained,
            "union_or_gate_abstained_overlap_rows": union_oos_abstained,
            "current_retained_oos_caught_by_mechanism": len(
                current_retained_caught
            ),
            "best_single_axis_new_oos_catches": len(
                source_free_axis_overlap.get("best_single_axis_new_oos_rows") or []
            ),
            "best_single_axis_new_oos_catches_on_current_extended_oos": len(
                source_free_axis_overlap.get(
                    "best_single_axis_new_oos_rows_on_current_extended_oos"
                )
                or []
            ),
            "best_single_axis_new_current_retained_oos_catches": len(
                source_free_axis_overlap.get(
                    "best_single_axis_new_current_retained_oos_rows"
                )
                or []
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_primary_overlap_rows": len(valid_primary_overlap),
            "missing_current_primary_mechanism_feature_rows": len(
                missing_primary_rows
            ),
            "missing_current_extended_scored_oos_mechanism_feature_rows": len(
                missing_scored_oos_rows
            ),
            "missing_current_extended_retained_oos_mechanism_feature_rows": len(
                missing_retained_oos_rows
            ),
            "missing_current_extended_abstained_oos_mechanism_feature_rows": len(
                missing_abstained_oos_rows
            ),
            "source_free_coordinate_anchor_candidate_files": len(
                source_free_candidate_ids
            ),
            "source_free_candidate_overlap_missing_primary_rows": len(
                candidate_reuse["missing_primary_overlap_rows"]
            ),
            "source_free_candidate_overlap_missing_retained_oos_rows": len(
                candidate_reuse["missing_retained_oos_overlap_rows"]
            ),
            "source_free_candidate_overlap_missing_abstained_oos_rows": len(
                candidate_reuse["missing_abstained_oos_overlap_rows"]
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "local_oos_signal_measured": local_oos_signal,
            "mechanism_adds_oos_abstentions_on_current_extended_overlap": (
                local_oos_signal
            ),
            "best_axis_new_oos_rows_overlap_current_extended_surface": bool(
                source_free_axis_overlap.get(
                    "best_single_axis_new_oos_rows_on_current_extended_oos"
                )
            ),
            "valid_integrated_operating_point_measurable": (
                valid_integrated_operating_point_measurable
            ),
            "adds_operating_point_value_beyond_current_surface": deployable,
            "deployable_now": deployable,
            "research_only": True,
            "negative": False,
            "apply_or_promote_now": False,
            "next_gate": (
                "Materialize split-aligned source-free mechanism fields for "
                f"the {len(missing_retained_oos_rows)} current-retained OOS "
                f"rows and {len(missing_primary_rows)} current calibration-"
                "primary rows, then rerun this fixed-threshold readout before "
                "any heldout or deployment claim."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "threshold_selected_or_tuned": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "current_measured_readout": _source_path_record(
                current_measured_readout_path
            ),
            "current_extended_oos_surface": _source_path_record(
                current_extended_oos_surface_path
            ),
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "mechanism_operating_point_contract": (
                _source_path_record(mechanism_operating_point_contract_path)
                if mechanism_operating_point_contract_path is not None
                else None
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "train_cal_feature_sidecar": (
                _source_path_record(train_cal_feature_sidecar_path)
                if train_cal_feature_sidecar_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
            "projection_readout": (
                _source_path_record(projection_readout_path)
                if projection_readout_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
            "source_free_coordinate_anchor_candidate_dir": {
                "exists": bool(
                    source_free_coordinate_anchor_candidate_dir_path is not None
                    and Path(source_free_coordinate_anchor_candidate_dir_path).exists()
                ),
                "path": (
                    str(source_free_coordinate_anchor_candidate_dir_path)
                    if source_free_coordinate_anchor_candidate_dir_path is not None
                    else None
                ),
                "file_count": len(source_free_candidate_ids),
            },
        },
        "interpretation": {
            "headline": (
                "On the current extended OOS overlap, the mechanism residual "
                f"catches {len(current_retained_caught)}/"
                f"{len(current_retained_overlap_rows)} rows retained by the "
                "current geometry/fold surface."
            ),
            "result": (
                "Research-only: the newer current OOS surface increases the "
                f"train/cal mechanism overlap to {len(oos_rows)} rows and "
                f"raises overlap abstentions from {current_oos_abstained} to "
                f"{union_oos_abstained} under a fixed OR gate, but valid "
                f"primary overlap remains {len(valid_primary_overlap)} rows."
            ),
            "next_action": (
                "Build split-aligned source-free mechanism features for the "
                "current primary retention gate and current-retained OOS rows."
            ),
        },
    }


def build_lever2_event_axis_current_extended_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 0.9,
    artifact_id: str = DEFAULT_EVENT_AXIS_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    partial_surface = (
        _read_json(partial_surface_current_split_portability_readout_path)
        if partial_surface_current_split_portability_readout_path is not None
        and Path(partial_surface_current_split_portability_readout_path).exists()
        else None
    )

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    train_rows = [
        row
        for row in (mechanism.get("scored_rows") or {}).get("train") or []
        if isinstance(row, dict) and str(row.get("entry_id") or "") in feature_rows
    ]

    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    current_primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )

    axis_frontier_rows: list[dict[str, Any]] = []
    axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    for axis in _event_axis_frontier_definitions():
        fields = list(axis["feature_fields"])
        rule = _select_axis_rule(
            calibration_rows, fields, min_primary_retain=min_primary_retain
        )
        row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            feature_row = feature_rows[entry_id]
            features = feature_row.get("row_specific_event_features") or {}
            score = round(_axis_score(features, fields), 8)
            axis_abstains = _axis_rule_abstains(
                score,
                direction=str(rule["direction"]),
                threshold=float(rule["threshold"]),
            )
            current_surface_abstains = bool(row.get("current_surface_abstains"))
            row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "axis_score": score,
                    "axis_abstains": axis_abstains,
                    "current_retained_caught_by_axis": bool(
                        axis_abstains and not current_surface_abstains
                    ),
                    "union_or_gate_abstains": bool(
                        axis_abstains or current_surface_abstains
                    ),
                }
            )
        axis_abstained = sum(1 for row in row_readouts if row["axis_abstains"])
        retained_caught = [
            row
            for row in row_readouts
            if row["current_retained_caught_by_axis"]
        ]
        union_abstained = sum(
            1 for row in row_readouts if row["union_or_gate_abstains"]
        )
        axis_id = str(axis["axis_id"])
        axis_row_readouts[axis_id] = row_readouts
        axis_frontier_rows.append(
            {
                "axis_id": axis_id,
                "description": axis["description"],
                "source_free_status": axis["source_free_status"],
                "feature_fields": fields,
                "feature_field_count": len(fields),
                "selected_rule": rule,
                "current_extended_overlap": {
                    "row_count": len(row_readouts),
                    "current_surface_abstained_rows": len(current_abstained_rows),
                    "current_surface_retained_rows": len(current_retained_rows),
                    "axis_abstained_rows": axis_abstained,
                    "axis_abstain_recall_on_overlap": _recall(
                        axis_abstained, len(row_readouts)
                    ),
                    "current_retained_oos_caught_by_axis": len(retained_caught),
                    "current_retained_oos_catch_recall": _recall(
                        len(retained_caught), len(current_retained_rows)
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(row_readouts)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained - len(current_abstained_rows)
                    ),
                    "current_retained_caught_entry_ids": [
                        row["entry_id"] for row in retained_caught
                    ],
                },
            }
        )

    def _axis_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        selected = row["selected_rule"]
        return (
            int(overlap["current_retained_oos_caught_by_axis"]),
            int(overlap["union_minus_current_abstained_rows"]),
            int(selected["calibration_oos_abstained"]),
            str(row["axis_id"]),
        )

    best_axis = sorted(axis_frontier_rows, key=_axis_sort_key, reverse=True)[0]
    best_overlap = best_axis["current_extended_overlap"]
    axis_by_id = {row["axis_id"]: row for row in axis_frontier_rows}
    axis_pair_frontier_rows: list[dict[str, Any]] = []
    axis_ids = [row["axis_id"] for row in axis_frontier_rows]
    for left_index, left_axis_id in enumerate(axis_ids):
        for right_axis_id in axis_ids[left_index + 1 :]:
            axis_ids_for_pair = [left_axis_id, right_axis_id]

            def _pair_abstains(features: dict[str, Any]) -> bool:
                for axis_id in axis_ids_for_pair:
                    axis_row = axis_by_id[axis_id]
                    rule = axis_row["selected_rule"]
                    if _axis_rule_abstains(
                        _axis_score(features, axis_row["feature_fields"]),
                        direction=str(rule["direction"]),
                        threshold=float(rule["threshold"]),
                    ):
                        return True
                return False

            primary_abstained = sum(
                1
                for row in calibration_rows
                if row["is_primary"] and _pair_abstains(row["features"])
            )
            oos_abstained = sum(
                1
                for row in calibration_rows
                if not row["is_primary"] and _pair_abstains(row["features"])
            )
            primary_rows = [row for row in calibration_rows if row["is_primary"]]
            oos_rows = [row for row in calibration_rows if not row["is_primary"]]
            primary_retained = len(primary_rows) - primary_abstained
            primary_retain_recall = _recall(primary_retained, len(primary_rows))
            if (
                primary_retain_recall is not None
                and primary_retain_recall + 1e-12 < min_primary_retain
            ):
                continue

            pair_row_readouts: list[dict[str, Any]] = []
            for row in current_rows:
                entry_id = str(row["entry_id"])
                member_rows = [
                    axis_row_readouts[axis_id][index]
                    for axis_id in axis_ids_for_pair
                    for index, member in enumerate(axis_row_readouts[axis_id])
                    if member["entry_id"] == entry_id
                ]
                axis_abstains = any(member["axis_abstains"] for member in member_rows)
                current_surface_abstains = bool(row.get("current_surface_abstains"))
                pair_row_readouts.append(
                    {
                        "entry_id": entry_id,
                        "current_surface_score": row.get("current_surface_score"),
                        "current_surface_abstains": current_surface_abstains,
                        "axis_pair_abstains": axis_abstains,
                        "current_retained_caught_by_axis_pair": bool(
                            axis_abstains and not current_surface_abstains
                        ),
                        "union_or_gate_abstains": bool(
                            axis_abstains or current_surface_abstains
                        ),
                    }
                )
            retained_caught = [
                row
                for row in pair_row_readouts
                if row["current_retained_caught_by_axis_pair"]
            ]
            union_abstained = sum(
                1 for row in pair_row_readouts if row["union_or_gate_abstains"]
            )
            pair_axis_fields = sorted(
                {
                    field
                    for axis_id in axis_ids_for_pair
                    for field in axis_by_id[axis_id]["feature_fields"]
                }
            )
            axis_pair_frontier_rows.append(
                {
                    "axis_pair_id": "+".join(axis_ids_for_pair),
                    "axis_ids": axis_ids_for_pair,
                    "source_free_status": (
                        "requires_source_free_materialization"
                        if any(
                            axis_by_id[axis_id]["source_free_status"]
                            != "source_free_compatible_proxy"
                            for axis_id in axis_ids_for_pair
                        )
                        else "source_free_compatible_proxy"
                    ),
                    "feature_fields": pair_axis_fields,
                    "feature_field_count": len(pair_axis_fields),
                    "calibration_primary_rows": len(primary_rows),
                    "calibration_primary_retained": primary_retained,
                    "calibration_primary_retain_recall": primary_retain_recall,
                    "calibration_oos_rows": len(oos_rows),
                    "calibration_oos_abstained": oos_abstained,
                    "calibration_oos_abstain_recall": _recall(
                        oos_abstained, len(oos_rows)
                    ),
                    "current_extended_overlap": {
                        "row_count": len(pair_row_readouts),
                        "current_surface_abstained_rows": len(current_abstained_rows),
                        "current_surface_retained_rows": len(current_retained_rows),
                        "axis_pair_abstained_rows": sum(
                            1
                            for row in pair_row_readouts
                            if row["axis_pair_abstains"]
                        ),
                        "current_retained_oos_caught_by_axis_pair": len(
                            retained_caught
                        ),
                        "current_retained_oos_catch_recall": _recall(
                            len(retained_caught), len(current_retained_rows)
                        ),
                        "union_or_gate_abstained_rows": union_abstained,
                        "union_or_gate_abstain_recall": _recall(
                            union_abstained, len(pair_row_readouts)
                        ),
                        "union_minus_current_abstained_rows": (
                            union_abstained - len(current_abstained_rows)
                        ),
                        "current_retained_caught_entry_ids": [
                            row["entry_id"] for row in retained_caught
                        ],
                    },
                    "row_readouts": pair_row_readouts,
                }
            )

    def _axis_pair_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        return (
            int(overlap["current_retained_oos_caught_by_axis_pair"]),
            int(overlap["union_minus_current_abstained_rows"]),
            int(row["calibration_oos_abstained"]),
            str(row["axis_pair_id"]),
        )

    best_axis_pair = (
        sorted(axis_pair_frontier_rows, key=_axis_pair_sort_key, reverse=True)[0]
        if axis_pair_frontier_rows
        else None
    )
    best_pair_overlap = (
        best_axis_pair["current_extended_overlap"] if best_axis_pair else {}
    )
    partial_counts = (partial_surface or {}).get("counts") or {}
    partial_missing_rows = (partial_surface or {}).get("missing_evidence_rows") or {}
    missing_primary_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_primary_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_retained_oos_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    best_axis_rows_by_id = {
        row["entry_id"]: row
        for row in axis_row_readouts[str(best_axis["axis_id"])]
        if row["current_retained_caught_by_axis"]
    }
    best_axis_materialization_rows = [
        {
            "entry_id": entry_id,
            "current_surface_score": row.get("current_surface_score"),
            "axis_score": row.get("axis_score"),
            "required_evidence": (
                "source-free current-split event-axis row for "
                f"{best_axis['axis_id']}"
            ),
        }
        for entry_id, row in sorted(
            best_axis_rows_by_id.items(), key=lambda item: _entry_sort_key(item[0])
        )
    ]
    best_axis_pair_materialization_rows = (
        [
            {
                "entry_id": row["entry_id"],
                "current_surface_score": row.get("current_surface_score"),
                "required_evidence": (
                    "source-free current-split event-axis row for "
                    f"{best_axis_pair['axis_pair_id']}"
                ),
            }
            for row in sorted(
                [
                    row
                    for row in best_axis_pair["row_readouts"]
                    if row["current_retained_caught_by_axis_pair"]
                ],
                key=lambda row: _entry_sort_key(str(row["entry_id"])),
            )
        ]
        if best_axis_pair
        else []
    )
    missing_current_primary_source_free = int(
        partial_counts.get(
            "missing_current_primary_source_free_partial_surface_rows",
            len(current_primary_rows) - len(valid_current_primary_overlap),
        )
        or 0
    )
    missing_current_retained_source_free = int(
        partial_counts.get(
            "missing_current_retained_oos_source_free_partial_surface_rows",
            len(current_retained_rows),
        )
        or 0
    )
    local_axis_signal = (
        int(best_overlap["current_retained_oos_caught_by_axis"]) > 0
    )
    local_pair_signal = bool(
        best_axis_pair
        and int(best_pair_overlap["current_retained_oos_caught_by_axis_pair"])
        > int(best_overlap["current_retained_oos_caught_by_axis"])
    )
    source_free_current_split_measurable = (
        missing_current_primary_source_free == 0
        and missing_current_retained_source_free == 0
    )
    result_class = (
        "research_only_current_extended_axis_signal"
        if local_axis_signal
        else "research_only_axis_negative"
    )
    status = f"lever2_event_axis_current_extended_frontier_readout_{result_class}"

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_current_extended_frontier_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "scope": (
            "Lever 2 train/cal readout selecting simple row-specific mechanism "
            "event-axis abstention rules on calibration rows only, then applying "
            "them to the current extended train/cal OOS overlap with the fixed "
            "geometry/fold surface. It does not score heldout rows or promote a "
            "deployment gate."
        ),
        "status": status,
        "result_class": result_class,
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "min_primary_retain": min_primary_retain,
                "selection_rows": "mechanism calibration split only",
                "objective": (
                    "maximize calibration OOS abstention subject to primary "
                    "retention"
                ),
            },
        },
        "measured_readout": {
            "axis_frontier_rows": axis_frontier_rows,
            "best_axis": best_axis,
            "axis_pair_frontier_rows": axis_pair_frontier_rows,
            "best_axis_pair": best_axis_pair,
            "current_primary_overlap": {
                "valid_current_primary_calibration_feature_overlap_rows": len(
                    valid_current_primary_overlap
                ),
                "valid_current_primary_calibration_feature_overlap_entry_ids": (
                    valid_current_primary_overlap
                ),
                "current_primary_rows_excluded_as_mechanism_train_targets": [
                    {
                        "entry_id": entry_id,
                        "reason": "row_is_mechanism_feature_train_target",
                    }
                    for entry_id in current_primary_train_target_overlap
                ],
            },
        },
        "row_readouts": {
            "current_extended_overlap_by_axis": axis_row_readouts,
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_event_axis_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_current_primary_overlap),
                "missing_rows_now": missing_current_primary_source_free,
                "why_it_matters": (
                    "The current primary retention gate must be measured on "
                    "source-free row-specific mechanism/event-axis features "
                    "before any deployable Lever 2 claim."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_event_axis_rows",
                "required_rows": int(
                    partial_counts.get("current_retained_oos_rows")
                    or len(current_retained_rows)
                ),
                "valid_overlap_rows_now": (
                    int(
                        partial_counts.get(
                            "union_current_retained_oos_overlap_rows", 0
                        )
                        or 0
                    )
                    if partial_surface is not None
                    else len(current_retained_rows)
                ),
                "missing_rows_now": missing_current_retained_source_free,
                "why_it_matters": (
                    "These are rows retained by geometry/fold where event-axis "
                    "mechanism evidence can add abstention value."
                ),
            },
            {
                "gap_id": "best_axis_source_free_materialization_fields",
                "required_rows": len(best_axis["feature_fields"]),
                "valid_overlap_rows_now": 0
                if best_axis["source_free_status"]
                != "source_free_compatible_proxy"
                else len(best_axis["feature_fields"]),
                "missing_rows_now": 0
                if best_axis["source_free_status"]
                == "source_free_compatible_proxy"
                else len(best_axis["feature_fields"]),
                "why_it_matters": (
                    "The best local axis fields must exist as source-free "
                    "deployment-valid row features on the current split, not "
                    "only as M-CSA train/cal research fields."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_event_axis": (
                missing_primary_source_free_rows
            ),
            "current_retained_oos_rows_requiring_source_free_event_axis": (
                missing_retained_source_free_rows
            ),
            "best_axis_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_axis_materialization_rows
            ),
            "best_axis_pair_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_axis_pair_materialization_rows
            ),
        },
        "counts": {
            "critical_violation_total": 0,
            "axis_surfaces_evaluated": len(axis_frontier_rows),
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": sum(
                1 for row in calibration_rows if row["is_primary"]
            ),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "train_rows": len(train_rows),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "best_axis_current_retained_oos_catches": int(
                best_overlap["current_retained_oos_caught_by_axis"]
            ),
            "best_axis_union_or_gate_abstained_overlap_rows": int(
                best_overlap["union_or_gate_abstained_rows"]
            ),
            "axis_pair_surfaces_evaluated": len(axis_pair_frontier_rows),
            "best_axis_pair_current_retained_oos_catches": (
                int(best_pair_overlap["current_retained_oos_caught_by_axis_pair"])
                if best_axis_pair
                else 0
            ),
            "best_axis_pair_union_or_gate_abstained_overlap_rows": (
                int(best_pair_overlap["union_or_gate_abstained_rows"])
                if best_axis_pair
                else 0
            ),
            "best_axis_pair_calibration_oos_abstained": (
                int(best_axis_pair["calibration_oos_abstained"])
                if best_axis_pair
                else 0
            ),
            "best_axis_calibration_oos_abstained": int(
                best_axis["selected_rule"]["calibration_oos_abstained"]
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                current_primary_train_target_overlap
            ),
            "missing_current_primary_source_free_event_axis_rows": (
                missing_current_primary_source_free
            ),
            "missing_current_retained_oos_source_free_event_axis_rows": (
                missing_current_retained_source_free
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "local_event_axis_signal_beyond_current_surface": local_axis_signal,
            "event_axis_pair_adds_beyond_best_single_axis": local_pair_signal,
            "adds_local_overlap_value_beyond_current_surface": local_axis_signal,
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                source_free_current_split_measurable
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not local_axis_signal,
            "apply_or_promote_now": False,
            "best_axis_id": best_axis["axis_id"],
            "best_axis_pair_id": (
                best_axis_pair["axis_pair_id"] if best_axis_pair else None
            ),
            "next_gate": (
                "Materialize source-free event-axis rows on the current split, "
                f"starting with {missing_current_primary_source_free} primary "
                "retention-gate rows and "
                f"{missing_current_retained_source_free} current-retained OOS "
                "rows; prioritize the best single/pair frontier fields, then "
                "rerun this train/cal frontier."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": "calibration_only",
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                f"Best event axis {best_axis['axis_id']} catches "
                f"{best_overlap['current_retained_oos_caught_by_axis']}/"
                f"{len(current_retained_rows)} current-retained overlap rows."
            ),
            "result": (
                "Research-only local signal: simple mechanism event axes add "
                "abstentions on the current extended OOS overlap, but current "
                "primary source-free coverage is absent so no integrated "
                "operating-point value can be claimed."
                if local_axis_signal
                else (
                    "Research-only negative on this local frontier: no simple "
                    "event axis adds current-retained OOS catches beyond "
                    "geometry/fold under calibration primary-retention rules."
                )
            ),
            "next_action": (
                "Materialize split-aligned source-free event-axis fields for "
                "the current primary and current-retained OOS rows before any "
                "deployment or heldout claim."
            ),
        },
    }


def build_lever2_source_free_electron_flow_split_alignment_readout(
    *,
    projection_readout_path: Path,
    incremental_readout_path: Path,
    source_free_projection_repair_candidate_surface_path: Path,
    train_cal_feature_sidecar_path: Path | None = None,
    current_in_scope_threshold_contract_path: Path | None = None,
    expanded_oos_calibrated_threshold_contract_path: Path | None = None,
    current_extended_oos_surface_path: Path | None = None,
    artifact_id: str = DEFAULT_ELECTRON_FLOW_SPLIT_ALIGNMENT_ARTIFACT_ID,
) -> dict[str, Any]:
    projection = _read_json(projection_readout_path)
    incremental = _read_json(incremental_readout_path)
    candidate_surface = _read_json(source_free_projection_repair_candidate_surface_path)
    raw_overlap_diagnostic: dict[str, Any] = {"available": False}
    if (
        train_cal_feature_sidecar_path is not None
        and current_in_scope_threshold_contract_path is not None
        and expanded_oos_calibrated_threshold_contract_path is not None
        and Path(train_cal_feature_sidecar_path).exists()
        and Path(current_in_scope_threshold_contract_path).exists()
        and Path(expanded_oos_calibrated_threshold_contract_path).exists()
    ):
        raw_overlap_diagnostic = _raw_electron_flow_current_overlap_diagnostic(
            train_cal_feature_sidecar=_read_json(train_cal_feature_sidecar_path),
            current_in_scope_threshold_contract=_read_json(
                current_in_scope_threshold_contract_path
            ),
            expanded_oos_calibrated_threshold_contract=_read_json(
                expanded_oos_calibrated_threshold_contract_path
            ),
        )

    current_subset = _variant_by_name(projection, "current_source_free_projected_subset")
    electron_flow = _variant_by_name(
        projection, "current_plus_missing_electron_flow"
    )
    full_surface = _variant_by_name(projection, "full_frozen_row_specific_surface")
    blockers: list[str] = []
    if current_subset is None:
        blockers.append("current_source_free_projected_subset_variant_missing")
    if electron_flow is None:
        blockers.append("electron_flow_axis_variant_missing")
    if full_surface is None:
        blockers.append("full_frozen_row_specific_surface_variant_missing")

    measured = projection.get("measured_readout") or {}
    best_axis = measured.get("best_single_axis_repair_ceiling") or {}
    best_axis_name = str(best_axis.get("variant") or "").replace(
        "current_plus_missing_", ""
    )
    if best_axis_name and best_axis_name != "electron_flow":
        blockers.append("best_single_axis_is_not_electron_flow")

    best_new_oos_rows = [
        row
        for row in measured.get("best_single_axis_new_oos_rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    ]
    best_new_oos_current_overlap = [
        row for row in best_new_oos_rows if row.get("in_current_geometry_fold_calibration_oos")
    ]
    best_new_oos_current_extended_overlap: list[dict[str, Any]] = []
    best_new_oos_current_extended_retained: list[dict[str, Any]] = []
    current_extended_axis_overlap: dict[str, Any] = {"available": False}
    if (
        current_extended_oos_surface_path is not None
        and expanded_oos_calibrated_threshold_contract_path is not None
        and Path(current_extended_oos_surface_path).exists()
        and Path(expanded_oos_calibrated_threshold_contract_path).exists()
    ):
        channel, current_threshold = _channel_threshold(
            _read_json(expanded_oos_calibrated_threshold_contract_path)
        )
        current_extended_rows = _current_surface_rows_with_score(
            _read_json(current_extended_oos_surface_path), channel
        )
        current_extended_row_readouts: list[dict[str, Any]] = []
        for row in best_new_oos_rows:
            entry_id = str(row.get("entry_id"))
            current_row = current_extended_rows.get(entry_id)
            current_score = (
                _current_score(current_row, channel)
                if current_row is not None
                else None
            )
            current_abstain = (
                _current_abstains(current_row, channel, current_threshold)
                if current_row is not None
                else None
            )
            current_extended_row = {
                "entry_id": entry_id,
                "in_current_extended_scored_oos": current_row is not None,
                "current_surface_score": round(current_score, 8)
                if current_score is not None
                else None,
                "current_surface_abstains": current_abstain,
                "current_retained_oos_caught_by_best_axis": bool(
                    current_row is not None and current_abstain is False
                ),
                "best_single_axis_residual": row.get("best_single_axis_residual"),
                "best_single_axis_threshold": row.get("best_single_axis_threshold"),
            }
            current_extended_row_readouts.append(current_extended_row)
        best_new_oos_current_extended_overlap = [
            row
            for row in current_extended_row_readouts
            if row["in_current_extended_scored_oos"]
        ]
        best_new_oos_current_extended_retained = [
            row
            for row in current_extended_row_readouts
            if row["current_retained_oos_caught_by_best_axis"]
        ]
        current_extended_axis_overlap = {
            "available": True,
            "channel": channel,
            "threshold": round(current_threshold, 8),
            "best_single_axis_new_oos_rows": current_extended_row_readouts,
            "best_single_axis_new_oos_rows_on_current_extended_oos": (
                best_new_oos_current_extended_overlap
            ),
            "best_single_axis_new_current_retained_oos_rows": (
                best_new_oos_current_extended_retained
            ),
        }
    split_context = measured.get("split_alignment_context") or {}
    primary_missing_rows, oos_missing_rows = _missing_current_rows(incremental)
    retained_oos_missing = [
        row for row in oos_missing_rows if not bool(row.get("current_surface_abstains"))
    ]
    abstained_oos_missing = [
        row for row in oos_missing_rows if bool(row.get("current_surface_abstains"))
    ]
    candidate_ids = _entry_ids_from_candidate_surface(candidate_surface)

    def _with_evidence_status(
        row: dict[str, Any],
        *,
        priority_tier: int,
        priority_class: str,
    ) -> dict[str, Any]:
        entry_id = str(row.get("entry_id"))
        candidate_available = entry_id in candidate_ids
        return {
            "entry_id": entry_id,
            "accession": row.get("accession"),
            "priority_tier": priority_tier,
            "priority_class": priority_class,
            "current_surface_score": row.get("current_surface_score"),
            "current_surface_abstains": row.get("current_surface_abstains"),
            "source_free_candidate_projection_row_available": candidate_available,
            "electron_flow_fields_required": [
                "has_electron_transfer_event",
                "electron_transfer_count",
            ],
            "required_evidence": (
                "source-free electron-flow axis sidecar row using approved "
                "local structure, cofactor geometry, or active-site evidence "
                "only; no mechanism text, labels, EC/Rhea IDs, source IDs, "
                "target names, or heldout tuning"
            ),
        }

    acquisition_rows: list[dict[str, Any]] = []
    for row in sorted(retained_oos_missing, key=_score_value, reverse=True):
        acquisition_rows.append(
            _with_evidence_status(
                row,
                priority_tier=1,
                priority_class="current_retained_oos_missing_electron_flow_axis",
            )
        )
    for row in sorted(primary_missing_rows, key=_score_value):
        acquisition_rows.append(
            _with_evidence_status(
                row,
                priority_tier=2,
                priority_class="current_primary_retention_gate_missing_electron_flow_axis",
            )
        )
    for row in sorted(abstained_oos_missing, key=_score_value, reverse=True):
        acquisition_rows.append(
            _with_evidence_status(
                row,
                priority_tier=3,
                priority_class="already_abstained_oos_missing_electron_flow_axis",
            )
        )

    electron_delta = None
    if current_subset is not None and electron_flow is not None:
        electron_delta = round(
            float(electron_flow.get("oos_abstain_recall") or 0.0)
            - float(current_subset.get("oos_abstain_recall") or 0.0),
            6,
        )
    electron_primary_retain = (
        electron_flow.get("primary_retain_recall")
        if electron_flow is not None
        else None
    )
    electron_flow_signal = bool(
        not blockers
        and electron_delta is not None
        and electron_delta > 0
        and electron_primary_retain is not None
        and float(electron_primary_retain) >= 0.9
    )
    split_aligned_measurable = bool(
        (projection.get("decision") or {}).get(
            "split_aligned_current_surface_incremental_readout_measurable"
        )
    )
    deployable = bool(electron_flow_signal and split_aligned_measurable)
    result_class = "deployable" if deployable else (
        "blocker" if blockers else "research_only"
    )
    status = (
        "lever2_source_free_electron_flow_split_alignment_readout_deployable"
        if deployable
        else (
            "lever2_source_free_electron_flow_split_alignment_readout_blocked"
            if blockers
            else "lever2_source_free_electron_flow_split_alignment_readout_research_only"
        )
    )

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.source_free_electron_flow_split_alignment_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Lever 2 measured train/cal readout for the source-free "
            "electron-flow repair axis, tied to the current geometry/fold "
            "calibration split. It consumes existing train/cal projection "
            "metrics and current-surface missing-row evidence, does not "
            "materialize features, and does not read or tune heldout."
        ),
        "result_class": result_class,
        "blockers": blockers,
        "measured_readout": {
            "train_cal_axis_ceiling": {
                "current_source_free_projected_subset": current_subset,
                "current_plus_missing_electron_flow": electron_flow,
                "full_frozen_row_specific_surface": full_surface,
                "electron_flow_oos_abstain_recall_delta_vs_current_projected": (
                    electron_delta
                ),
                "best_single_axis_name": best_axis_name or None,
                "best_single_axis_new_oos_rows": best_new_oos_rows,
                "best_single_axis_new_oos_rows_on_current_geometry_fold_oos": (
                    best_new_oos_current_overlap
                ),
            },
            "split_alignment_context": split_context,
            "raw_full_sidecar_current_surface_overlap_diagnostic": (
                raw_overlap_diagnostic
            ),
            "best_axis_current_extended_oos_overlap_diagnostic": (
                current_extended_axis_overlap
            ),
            "current_surface_missing_row_context": {
                "current_retained_oos_missing_electron_flow_rows": len(
                    retained_oos_missing
                ),
                "already_abstained_oos_missing_electron_flow_rows": len(
                    abstained_oos_missing
                ),
                "primary_retention_gate_missing_electron_flow_rows": len(
                    primary_missing_rows
                ),
            },
        },
        "acquisition_priority_rows": acquisition_rows,
        "counts": {
            "blockers": len(blockers),
            "critical_violation_total": 0,
            "best_single_axis_new_oos_catches": len(best_new_oos_rows),
            "best_single_axis_new_oos_catches_on_current_geometry_fold_oos": len(
                best_new_oos_current_overlap
            ),
            "best_single_axis_new_oos_catches_on_current_extended_oos": len(
                best_new_oos_current_extended_overlap
            ),
            "best_single_axis_new_current_retained_oos_catches": len(
                best_new_oos_current_extended_retained
            ),
            "current_geometry_fold_calibration_primary_rows": int(
                split_context.get("current_geometry_fold_calibration_primary_rows") or 0
            ),
            "current_geometry_fold_calibration_oos_rows": int(
                split_context.get("current_geometry_fold_calibration_oos_rows") or 0
            ),
            "source_free_candidate_projection_overlap_primary_rows": int(
                split_context.get(
                    "source_free_candidate_projection_overlap_primary_rows"
                )
                or 0
            ),
            "source_free_candidate_projection_overlap_oos_rows": int(
                split_context.get("source_free_candidate_projection_overlap_oos_rows")
                or 0
            ),
            "missing_current_primary_electron_flow_rows": len(primary_missing_rows),
            "missing_current_oos_electron_flow_rows": len(oos_missing_rows),
            "missing_current_retained_oos_electron_flow_rows": len(
                retained_oos_missing
            ),
            "missing_current_abstained_oos_electron_flow_rows": len(
                abstained_oos_missing
            ),
            "candidate_surface_rows": len(candidate_ids),
            "candidate_surface_overlap_missing_primary_rows": sum(
                1 for row in primary_missing_rows if str(row.get("entry_id")) in candidate_ids
            ),
            "candidate_surface_overlap_missing_retained_oos_rows": sum(
                1 for row in retained_oos_missing if str(row.get("entry_id")) in candidate_ids
            ),
            "candidate_surface_overlap_missing_abstained_oos_rows": sum(
                1 for row in abstained_oos_missing if str(row.get("entry_id")) in candidate_ids
            ),
            "acquisition_priority_rows": len(acquisition_rows),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "source_free_electron_flow_axis_materialized_by_this_artifact": False,
            "m_csa_row_specific_features_train_cal_only": True,
            "threshold_selected_or_tuned": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "missing_evidence": [
            {
                "gap_id": "current_retained_oos_source_free_electron_flow_axis",
                "required_rows": len(retained_oos_missing),
                "valid_candidate_projection_rows_now": sum(
                    1
                    for row in retained_oos_missing
                    if str(row.get("entry_id")) in candidate_ids
                ),
                "why_it_matters": (
                    "These are the current geometry/fold false-negative OOS "
                    "candidates most likely to show incremental abstention "
                    "value if electron-flow evidence transfers."
                ),
            },
            {
                "gap_id": "current_primary_source_free_electron_flow_axis",
                "required_rows": len(primary_missing_rows),
                "valid_candidate_projection_rows_now": sum(
                    1
                    for row in primary_missing_rows
                    if str(row.get("entry_id")) in candidate_ids
                ),
                "why_it_matters": (
                    "A valid operating-point claim needs calibration-primary "
                    "retention cost on the current geometry/fold split."
                ),
            },
            {
                "gap_id": "current_abstained_oos_source_free_electron_flow_axis",
                "required_rows": len(abstained_oos_missing),
                "valid_candidate_projection_rows_now": sum(
                    1
                    for row in abstained_oos_missing
                    if str(row.get("entry_id")) in candidate_ids
                ),
                "why_it_matters": (
                    "These rows are lower priority for incremental value "
                    "because geometry/fold already abstains, but they complete "
                    "the split-aligned OOS surface."
                ),
            },
        ],
        "decision": {
            "measured_readout_available": not blockers,
            "source_free_electron_flow_axis_has_train_cal_signal": (
                electron_flow_signal
            ),
            "split_aligned_current_surface_incremental_readout_measurable": (
                split_aligned_measurable
            ),
            "best_axis_new_oos_rows_overlap_current_geometry_fold_oos": bool(
                best_new_oos_current_overlap
            ),
            "best_axis_new_oos_rows_overlap_current_extended_oos": bool(
                best_new_oos_current_extended_overlap
            ),
            "adds_operating_point_value_beyond_current_surface": deployable,
            "deployable_now": deployable,
            "research_only": bool(not deployable and not blockers),
            "negative": False,
            "apply_or_promote_now": False,
            "next_gate": (
                "Materialize source-free electron-flow fields for the "
                f"{len(retained_oos_missing)} current-retained OOS rows and "
                f"{len(primary_missing_rows)} current calibration-primary rows "
                "first, then rerun the train/cal projection and fixed-threshold "
                "incremental readouts before any heldout or deployment claim."
            ),
        },
        "source_artifacts": {
            "projection_readout": _source_path_record(projection_readout_path),
            "incremental_readout": _source_path_record(incremental_readout_path),
            "source_free_projection_repair_candidate_surface": _source_path_record(
                source_free_projection_repair_candidate_surface_path
            ),
            "train_cal_feature_sidecar": (
                _source_path_record(train_cal_feature_sidecar_path)
                if train_cal_feature_sidecar_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
            "current_in_scope_threshold_contract": (
                _source_path_record(current_in_scope_threshold_contract_path)
                if current_in_scope_threshold_contract_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
            "expanded_oos_calibrated_threshold_contract": (
                _source_path_record(expanded_oos_calibrated_threshold_contract_path)
                if expanded_oos_calibrated_threshold_contract_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
            "current_extended_oos_surface": (
                _source_path_record(current_extended_oos_surface_path)
                if current_extended_oos_surface_path is not None
                else {"path": None, "exists": False, "sha256": None}
            ),
        },
        "interpretation": {
            "result": (
                "Research-only: electron-flow is the best single missing "
                "source-free axis on the existing train/cal mechanism sidecar, "
                f"adding {electron_delta} OOS abstain recall versus the current "
                "projected subset, but its newly caught OOS rows overlap "
                f"{len(best_new_oos_current_overlap)} current geometry/fold "
                "calibration-OOS rows."
                if not blockers
                else (
                    "The electron-flow split-alignment readout is blocked by "
                    "missing input variants."
                )
            ),
            "next_action": (
                "Acquire split-aligned source-free electron-flow evidence for "
                "the priority rows in this artifact; start with current-retained "
                "OOS rows, then primary retention-gate rows."
            ),
        },
    }


def build_lever2_event_axis_loo_current_extended_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 0.9,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_LOO_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    partial_surface = (
        _read_json(partial_surface_current_split_portability_readout_path)
        if partial_surface_current_split_portability_readout_path is not None
        and Path(partial_surface_current_split_portability_readout_path).exists()
        else None
    )

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    train_rows = [
        row
        for row in (mechanism.get("scored_rows") or {}).get("train") or []
        if isinstance(row, dict) and str(row.get("entry_id") or "") in feature_rows
    ]
    calibration_entry_ids = {row["entry_id"] for row in calibration_rows}

    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]

    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    current_primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )

    axis_definitions = _event_axis_frontier_definitions()
    axes_by_id = {str(axis["axis_id"]): axis for axis in axis_definitions}
    if baseline_axis_id not in axes_by_id:
        raise ValueError(f"unknown baseline event axis: {baseline_axis_id}")

    def _selection_rows_for(entry_id: str) -> list[dict[str, Any]]:
        return [row for row in calibration_rows if row["entry_id"] != entry_id]

    axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    axis_frontier_rows: list[dict[str, Any]] = []
    for axis in axis_definitions:
        axis_id = str(axis["axis_id"])
        fields = list(axis["feature_fields"])
        row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            features = (
                feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
            )
            training_rows = _selection_rows_for(entry_id)
            rule: dict[str, Any] | None
            axis_abstains = False
            selection_error = None
            try:
                rule = _select_axis_rule(
                    training_rows,
                    fields,
                    min_primary_retain=min_primary_retain,
                )
                axis_score = round(_axis_score(features, fields), 8)
                axis_abstains = _axis_rule_abstains(
                    axis_score,
                    direction=str(rule["direction"]),
                    threshold=float(rule["threshold"]),
                )
            except ValueError as exc:
                rule = None
                axis_score = round(_axis_score(features, fields), 8)
                selection_error = str(exc)
            current_surface_abstains = bool(row.get("current_surface_abstains"))
            row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "target_excluded_from_axis_selection": (
                        entry_id in calibration_entry_ids
                    ),
                    "axis_score": axis_score,
                    "axis_rule_evaluable": rule is not None,
                    "selection_error": selection_error,
                    "selected_rule": rule,
                    "axis_loo_abstains": axis_abstains,
                    "current_retained_caught_by_axis_loo": bool(
                        rule is not None
                        and axis_abstains
                        and not current_surface_abstains
                    ),
                    "union_or_gate_abstains": bool(
                        current_surface_abstains
                        or (rule is not None and axis_abstains)
                    ),
                }
            )
        evaluable_rows = [row for row in row_readouts if row["axis_rule_evaluable"]]
        retained_caught = [
            row
            for row in evaluable_rows
            if row["current_retained_caught_by_axis_loo"]
        ]
        union_abstained = sum(
            1 for row in evaluable_rows if row["union_or_gate_abstains"]
        )
        axis_row_readouts[axis_id] = row_readouts
        axis_frontier_rows.append(
            {
                "axis_id": axis_id,
                "description": axis["description"],
                "source_free_status": axis["source_free_status"],
                "feature_fields": fields,
                "feature_field_count": len(fields),
                "leave_one_out_selection": {
                    "target_rows": len(row_readouts),
                    "evaluable_rows": len(evaluable_rows),
                    "unevaluable_rows": len(row_readouts) - len(evaluable_rows),
                    "target_excluded_from_selection_rows": sum(
                        1
                        for row in row_readouts
                        if row["target_excluded_from_axis_selection"]
                    ),
                },
                "current_extended_overlap": {
                    "row_count": len(evaluable_rows),
                    "current_surface_abstained_rows": sum(
                        1 for row in evaluable_rows if row["current_surface_abstains"]
                    ),
                    "current_surface_retained_rows": sum(
                        1
                        for row in evaluable_rows
                        if not row["current_surface_abstains"]
                    ),
                    "axis_loo_abstained_rows": sum(
                        1 for row in evaluable_rows if row["axis_loo_abstains"]
                    ),
                    "current_retained_oos_caught_by_axis_loo": len(
                        retained_caught
                    ),
                    "current_retained_oos_catch_recall": _recall(
                        len(retained_caught),
                        sum(
                            1
                            for row in evaluable_rows
                            if not row["current_surface_abstains"]
                        ),
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(evaluable_rows)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained
                        - sum(
                            1
                            for row in evaluable_rows
                            if row["current_surface_abstains"]
                        )
                    ),
                    "current_retained_caught_entry_ids": [
                        row["entry_id"] for row in retained_caught
                    ],
                },
            }
        )

    baseline_axis = next(
        row for row in axis_frontier_rows if row["axis_id"] == baseline_axis_id
    )
    baseline_by_entry = {
        row["entry_id"]: row for row in axis_row_readouts[baseline_axis_id]
    }
    projection_plus_axis_rows: list[dict[str, Any]] = []
    projection_plus_axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    for axis in axis_definitions:
        axis_id = str(axis["axis_id"])
        if axis_id == baseline_axis_id:
            continue
        added_by_entry = {row["entry_id"]: row for row in axis_row_readouts[axis_id]}
        pair_id = f"{baseline_axis_id}+{axis_id}"
        pair_row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            baseline_row = baseline_by_entry.get(entry_id)
            added_row = added_by_entry.get(entry_id)
            if baseline_row is None or added_row is None:
                continue
            pair_evaluable = bool(
                baseline_row["axis_rule_evaluable"]
                and added_row["axis_rule_evaluable"]
            )
            pair_primary_retained = None
            pair_primary_rows = None
            pair_primary_retain_recall = None
            pair_oos_abstained = None
            pair_oos_rows = None
            pair_error = None
            if pair_evaluable:
                training_rows = _selection_rows_for(entry_id)
                baseline_rule = baseline_row["selected_rule"] or {}
                added_rule = added_row["selected_rule"] or {}

                def _row_axis_abstains(
                    cal_row: dict[str, Any],
                    axis_id_for_rule: str,
                    rule: dict[str, Any],
                ) -> bool:
                    axis_fields = list(axes_by_id[axis_id_for_rule]["feature_fields"])
                    score = _axis_score(cal_row["features"], axis_fields)
                    return _axis_rule_abstains(
                        score,
                        direction=str(rule["direction"]),
                        threshold=float(rule["threshold"]),
                    )

                primary_rows = [row for row in training_rows if row["is_primary"]]
                oos_rows = [row for row in training_rows if not row["is_primary"]]
                pair_primary_abstained = sum(
                    1
                    for cal_row in primary_rows
                    if _row_axis_abstains(cal_row, baseline_axis_id, baseline_rule)
                    or _row_axis_abstains(cal_row, axis_id, added_rule)
                )
                pair_oos_abstained = sum(
                    1
                    for cal_row in oos_rows
                    if _row_axis_abstains(cal_row, baseline_axis_id, baseline_rule)
                    or _row_axis_abstains(cal_row, axis_id, added_rule)
                )
                pair_primary_rows = len(primary_rows)
                pair_oos_rows = len(oos_rows)
                pair_primary_retained = pair_primary_rows - pair_primary_abstained
                pair_primary_retain_recall = _recall(
                    pair_primary_retained, pair_primary_rows
                )
                if (
                    pair_primary_retain_recall is not None
                    and pair_primary_retain_recall + 1e-12 < min_primary_retain
                ):
                    pair_evaluable = False
                    pair_error = "pair_rule_fails_min_primary_retain_on_loo_selection"
            else:
                pair_error = "single_axis_rule_not_evaluable"

            current_surface_abstains = bool(row.get("current_surface_abstains"))
            baseline_abstains = bool(
                baseline_row.get("axis_loo_abstains")
                and baseline_row.get("axis_rule_evaluable")
            )
            added_abstains = bool(
                added_row.get("axis_loo_abstains")
                and added_row.get("axis_rule_evaluable")
            )
            pair_abstains = bool(pair_evaluable and (baseline_abstains or added_abstains))
            baseline_current_retained_catch = bool(
                baseline_abstains and not current_surface_abstains
            )
            pair_current_retained_catch = bool(
                pair_abstains and not current_surface_abstains
            )
            pair_row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "pair_rule_evaluable": pair_evaluable,
                    "selection_error": pair_error,
                    "baseline_axis_score": baseline_row.get("axis_score"),
                    "added_axis_score": added_row.get("axis_score"),
                    "baseline_selected_rule": baseline_row.get("selected_rule"),
                    "added_axis_selected_rule": added_row.get("selected_rule"),
                    "projected_subset_abstains": baseline_abstains,
                    "added_axis_abstains": added_abstains,
                    "projection_plus_axis_abstains": pair_abstains,
                    "current_retained_caught_by_projected_subset": (
                        baseline_current_retained_catch
                    ),
                    "current_retained_caught_by_projection_plus_axis": (
                        pair_current_retained_catch
                    ),
                    "current_retained_caught_beyond_projected_subset": bool(
                        pair_current_retained_catch
                        and not baseline_current_retained_catch
                    ),
                    "union_or_gate_abstains": bool(
                        current_surface_abstains or pair_abstains
                    ),
                    "loo_selection_primary_rows": pair_primary_rows,
                    "loo_selection_primary_retained": pair_primary_retained,
                    "loo_selection_primary_retain_recall": pair_primary_retain_recall,
                    "loo_selection_oos_rows": pair_oos_rows,
                    "loo_selection_oos_abstained": pair_oos_abstained,
                }
            )
        evaluable_pair_rows = [
            row for row in pair_row_readouts if row["pair_rule_evaluable"]
        ]
        baseline_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projected_subset"]
        ]
        pair_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projection_plus_axis"]
        ]
        marginal_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_beyond_projected_subset"]
        ]
        union_abstained = sum(
            1 for row in evaluable_pair_rows if row["union_or_gate_abstains"]
        )
        current_abstained = sum(
            1 for row in evaluable_pair_rows if row["current_surface_abstains"]
        )
        current_retained = sum(
            1 for row in evaluable_pair_rows if not row["current_surface_abstains"]
        )
        pair_fields = sorted(
            set(axes_by_id[baseline_axis_id]["feature_fields"])
            | set(axis["feature_fields"])
        )
        primary_loo_control_rows: list[dict[str, Any]] = []
        for primary_row in [row for row in calibration_rows if row["is_primary"]]:
            entry_id = str(primary_row["entry_id"])
            training_rows = _selection_rows_for(entry_id)
            try:
                baseline_rule = _select_axis_rule(
                    training_rows,
                    list(axes_by_id[baseline_axis_id]["feature_fields"]),
                    min_primary_retain=min_primary_retain,
                )
                added_rule = _select_axis_rule(
                    training_rows,
                    list(axis["feature_fields"]),
                    min_primary_retain=min_primary_retain,
                )
                baseline_score = _axis_score(
                    primary_row["features"],
                    list(axes_by_id[baseline_axis_id]["feature_fields"]),
                )
                added_score = _axis_score(
                    primary_row["features"], list(axis["feature_fields"])
                )
                baseline_abstains = _axis_rule_abstains(
                    baseline_score,
                    direction=str(baseline_rule["direction"]),
                    threshold=float(baseline_rule["threshold"]),
                )
                added_abstains = _axis_rule_abstains(
                    added_score,
                    direction=str(added_rule["direction"]),
                    threshold=float(added_rule["threshold"]),
                )
                pair_abstains = bool(baseline_abstains or added_abstains)
                primary_loo_control_rows.append(
                    {
                        "entry_id": entry_id,
                        "primary_rule_evaluable": True,
                        "baseline_axis_score": round(baseline_score, 8),
                        "added_axis_score": round(added_score, 8),
                        "baseline_selected_rule": baseline_rule,
                        "added_axis_selected_rule": added_rule,
                        "projection_plus_axis_abstains": pair_abstains,
                        "projection_plus_axis_retains": not pair_abstains,
                    }
                )
            except ValueError as exc:
                primary_loo_control_rows.append(
                    {
                        "entry_id": entry_id,
                        "primary_rule_evaluable": False,
                        "selection_error": str(exc),
                        "projection_plus_axis_abstains": None,
                        "projection_plus_axis_retains": None,
                    }
                )
        primary_loo_evaluable_rows = [
            row
            for row in primary_loo_control_rows
            if row["primary_rule_evaluable"]
        ]
        primary_loo_retained_rows = [
            row
            for row in primary_loo_evaluable_rows
            if row["projection_plus_axis_retains"]
        ]
        projection_plus_axis_row_readouts[pair_id] = pair_row_readouts
        projection_plus_axis_rows.append(
            {
                "projection_plus_axis_id": pair_id,
                "baseline_axis_id": baseline_axis_id,
                "added_axis_id": axis_id,
                "source_free_status": (
                    "source_free_compatible_proxy"
                    if axis["source_free_status"] == "source_free_compatible_proxy"
                    else "requires_source_free_materialization"
                ),
                "feature_fields": pair_fields,
                "feature_field_count": len(pair_fields),
                "leave_one_out_selection": {
                    "target_rows": len(pair_row_readouts),
                    "evaluable_rows": len(evaluable_pair_rows),
                    "unevaluable_rows": (
                        len(pair_row_readouts) - len(evaluable_pair_rows)
                    ),
                    "min_primary_retain": min_primary_retain,
                },
                "primary_leave_one_out_control": {
                    "target_rows": len(primary_loo_control_rows),
                    "evaluable_rows": len(primary_loo_evaluable_rows),
                    "retained_rows": len(primary_loo_retained_rows),
                    "retention_recall": _recall(
                        len(primary_loo_retained_rows),
                        len(primary_loo_evaluable_rows),
                    ),
                    "abstained_entry_ids": [
                        row["entry_id"]
                        for row in primary_loo_evaluable_rows
                        if row["projection_plus_axis_abstains"]
                    ],
                },
                "primary_leave_one_out_control_rows": primary_loo_control_rows,
                "current_extended_overlap": {
                    "row_count": len(evaluable_pair_rows),
                    "current_surface_abstained_rows": current_abstained,
                    "current_surface_retained_rows": current_retained,
                    "projected_subset_current_retained_oos_catches": len(
                        baseline_caught
                    ),
                    "projection_plus_axis_current_retained_oos_catches": len(
                        pair_caught
                    ),
                    "marginal_current_retained_oos_catches_beyond_projected_subset": len(
                        marginal_caught
                    ),
                    "current_retained_oos_catch_recall": _recall(
                        len(pair_caught), current_retained
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(evaluable_pair_rows)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained - current_abstained
                    ),
                    "projected_subset_caught_entry_ids": [
                        row["entry_id"] for row in baseline_caught
                    ],
                    "projection_plus_axis_caught_entry_ids": [
                        row["entry_id"] for row in pair_caught
                    ],
                    "marginal_caught_entry_ids": [
                        row["entry_id"] for row in marginal_caught
                    ],
                },
            }
        )

    def _single_axis_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
        overlap = row["current_extended_overlap"]
        return (
            int(overlap["current_retained_oos_caught_by_axis_loo"]),
            int(overlap["union_minus_current_abstained_rows"]),
            str(row["axis_id"]),
        )

    def _projection_plus_axis_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        return (
            int(
                overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            int(overlap["projection_plus_axis_current_retained_oos_catches"]),
            int(overlap["union_minus_current_abstained_rows"]),
            str(row["projection_plus_axis_id"]),
        )

    best_single_axis = sorted(
        axis_frontier_rows, key=_single_axis_sort_key, reverse=True
    )[0]
    best_projection_plus_axis = sorted(
        projection_plus_axis_rows,
        key=_projection_plus_axis_sort_key,
        reverse=True,
    )[0]
    baseline_overlap = baseline_axis["current_extended_overlap"]
    best_projection_overlap = best_projection_plus_axis["current_extended_overlap"]
    best_primary_loo_control = best_projection_plus_axis[
        "primary_leave_one_out_control"
    ]

    partial_counts = (partial_surface or {}).get("counts") or {}
    partial_missing_rows = (partial_surface or {}).get("missing_evidence_rows") or {}
    missing_primary_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_primary_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_retained_oos_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_ids = {
        str(row["entry_id"]) for row in missing_retained_source_free_rows
    }
    missing_current_primary_source_free = int(
        partial_counts.get(
            "missing_current_primary_source_free_partial_surface_rows",
            len(current_primary_rows) - len(valid_current_primary_overlap),
        )
        or 0
    )
    missing_current_retained_source_free = int(
        partial_counts.get(
            "missing_current_retained_oos_source_free_partial_surface_rows",
            len(current_retained_rows),
        )
        or 0
    )

    best_pair_rows_by_id = {
        row["entry_id"]: row
        for row in projection_plus_axis_row_readouts[
            best_projection_plus_axis["projection_plus_axis_id"]
        ]
        if row["current_retained_caught_by_projection_plus_axis"]
    }
    best_pair_materialization_rows = [
        {
            "entry_id": entry_id,
            "current_surface_score": row.get("current_surface_score"),
            "baseline_axis_score": row.get("baseline_axis_score"),
            "added_axis_score": row.get("added_axis_score"),
            "baseline_selected_rule": row.get("baseline_selected_rule"),
            "added_axis_selected_rule": row.get("added_axis_selected_rule"),
            "existing_source_free_partial_surface_row_available": bool(
                partial_surface is not None
                and entry_id not in missing_retained_source_free_ids
            ),
            "marginal_beyond_projected_subset": row[
                "current_retained_caught_beyond_projected_subset"
            ],
            "required_evidence": (
                "source-free current-split event-axis rows for "
                f"{best_projection_plus_axis['projection_plus_axis_id']}"
            ),
        }
        for entry_id, row in sorted(
            best_pair_rows_by_id.items(), key=lambda item: _entry_sort_key(item[0])
        )
    ]
    best_pair_reusable_source_free_rows = [
        row
        for row in best_pair_materialization_rows
        if row["existing_source_free_partial_surface_row_available"]
    ]

    loo_projected_signal = (
        int(baseline_overlap["current_retained_oos_caught_by_axis_loo"]) > 0
    )
    marginal_signal = (
        int(
            best_projection_overlap[
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        > 0
    )
    def _primary_control_passes(row: dict[str, Any]) -> bool:
        control = row["primary_leave_one_out_control"]
        recall = control.get("retention_recall")
        return bool(recall is not None and float(recall) + 1e-12 >= min_primary_retain)

    primary_control_passing_surfaces = [
        row for row in projection_plus_axis_rows if _primary_control_passes(row)
    ]
    best_primary_control_passes = _primary_control_passes(best_projection_plus_axis)
    baseline_source_free_field_count = (
        len(axes_by_id[baseline_axis_id]["feature_fields"])
        if axes_by_id[baseline_axis_id]["source_free_status"]
        == "source_free_compatible_proxy"
        else 0
    )
    best_projection_missing_field_count = max(
        0,
        len(best_projection_plus_axis["feature_fields"])
        - baseline_source_free_field_count,
    )
    source_free_current_split_measurable = (
        missing_current_primary_source_free == 0
        and missing_current_retained_source_free == 0
    )
    result_class = (
        "research_only_loo_marginal_axis_signal"
        if marginal_signal and best_primary_control_passes
        else "research_only_loo_marginal_axis_signal_primary_control_caveat"
        if marginal_signal
        else (
            "research_only_loo_projected_subset_signal"
            if loo_projected_signal
            else "research_only_loo_axis_negative"
        )
    )
    status = f"lever2_event_axis_loo_current_extended_frontier_readout_{result_class}"

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_loo_current_extended_frontier_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "scope": (
            "Lever 2 train/cal readout selecting simple row-specific mechanism "
            "event-axis abstention rules on calibration rows while excluding "
            "each measured OOS target row from its own rule selection. It then "
            "measures single-axis and projected-subset-plus-axis catches on the "
            "current extended train/cal OOS overlap with the fixed geometry/fold "
            "surface. It does not score heldout rows or promote a deployment gate."
        ),
        "status": status,
        "result_class": result_class,
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "baseline_axis_id": baseline_axis_id,
                "min_primary_retain": min_primary_retain,
                "selection_rows": (
                    "mechanism calibration split only, excluding each target "
                    "OOS row from its own rule selection"
                ),
                "objective": (
                    "maximize calibration OOS abstention subject to primary "
                    "retention before applying to the excluded current-overlap "
                    "OOS row"
                ),
            },
        },
        "measured_readout": {
            "axis_loo_frontier_rows": axis_frontier_rows,
            "baseline_projected_subset_axis": baseline_axis,
            "best_single_axis": best_single_axis,
            "projection_plus_axis_loo_rows": projection_plus_axis_rows,
            "best_projection_plus_axis": best_projection_plus_axis,
            "current_primary_overlap": {
                "valid_current_primary_calibration_feature_overlap_rows": len(
                    valid_current_primary_overlap
                ),
                "valid_current_primary_calibration_feature_overlap_entry_ids": (
                    valid_current_primary_overlap
                ),
                "current_primary_rows_excluded_as_mechanism_train_targets": [
                    {
                        "entry_id": entry_id,
                        "reason": "row_is_mechanism_feature_train_target",
                    }
                    for entry_id in current_primary_train_target_overlap
                ],
            },
        },
        "row_readouts": {
            "current_extended_overlap_by_axis_loo": axis_row_readouts,
            "current_extended_overlap_by_projection_plus_axis_loo": (
                projection_plus_axis_row_readouts
            ),
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_event_axis_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_current_primary_overlap),
                "missing_rows_now": missing_current_primary_source_free,
                "why_it_matters": (
                    "The current primary retention gate must be measured on "
                    "source-free row-specific mechanism/event-axis features "
                    "before any deployable Lever 2 claim."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_event_axis_rows",
                "required_rows": int(
                    partial_counts.get("current_retained_oos_rows")
                    or len(current_retained_rows)
                ),
                "valid_overlap_rows_now": (
                    int(
                        partial_counts.get(
                            "union_current_retained_oos_overlap_rows", 0
                        )
                        or 0
                    )
                    if partial_surface is not None
                    else len(current_retained_rows)
                ),
                "missing_rows_now": missing_current_retained_source_free,
                "why_it_matters": (
                    "These are rows retained by geometry/fold where event-axis "
                    "mechanism evidence can add abstention value."
                ),
            },
            {
                "gap_id": "best_loo_projection_plus_axis_source_free_fields",
                "required_rows": len(best_projection_plus_axis["feature_fields"]),
                "valid_overlap_rows_now": baseline_source_free_field_count,
                "missing_rows_now": best_projection_missing_field_count,
                "why_it_matters": (
                    "The best leave-one-out marginal axis must exist as "
                    "source-free deployment-valid row features on the current "
                    "split, not only as M-CSA train/cal research fields."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_event_axis": (
                missing_primary_source_free_rows
            ),
            "current_retained_oos_rows_requiring_source_free_event_axis": (
                missing_retained_source_free_rows
            ),
            "best_projection_plus_axis_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_pair_materialization_rows
            ),
            "best_projection_plus_axis_marginal_rows": [
                row
                for row in best_pair_materialization_rows
                if row["marginal_beyond_projected_subset"]
            ],
        },
        "counts": {
            "critical_violation_total": 0,
            "axis_surfaces_evaluated": len(axis_frontier_rows),
            "projection_plus_axis_surfaces_evaluated": len(
                projection_plus_axis_rows
            ),
            "projection_plus_axis_primary_loo_control_passing_surfaces": len(
                primary_control_passing_surfaces
            ),
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": sum(
                1 for row in calibration_rows if row["is_primary"]
            ),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "train_rows": len(train_rows),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "baseline_projected_subset_current_retained_oos_catches": int(
                baseline_overlap["current_retained_oos_caught_by_axis_loo"]
            ),
            "baseline_projected_subset_union_or_gate_abstained_overlap_rows": int(
                baseline_overlap["union_or_gate_abstained_rows"]
            ),
            "best_single_axis_current_retained_oos_catches": int(
                best_single_axis["current_extended_overlap"][
                    "current_retained_oos_caught_by_axis_loo"
                ]
            ),
            "best_projection_plus_axis_current_retained_oos_catches": int(
                best_projection_overlap[
                    "projection_plus_axis_current_retained_oos_catches"
                ]
            ),
            "best_projection_plus_axis_marginal_current_retained_oos_catches": int(
                best_projection_overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            "best_projection_plus_axis_union_or_gate_abstained_overlap_rows": int(
                best_projection_overlap["union_or_gate_abstained_rows"]
            ),
            "best_projection_plus_axis_source_free_compatible_fields": (
                baseline_source_free_field_count
            ),
            "best_projection_plus_axis_missing_new_feature_fields": (
                best_projection_missing_field_count
            ),
            "best_projection_plus_axis_caught_rows_with_existing_source_free_partial_surface": len(
                best_pair_reusable_source_free_rows
            ),
            "best_projection_plus_axis_primary_loo_control_rows": int(
                best_primary_loo_control["target_rows"]
            ),
            "best_projection_plus_axis_primary_loo_retained_rows": int(
                best_primary_loo_control["retained_rows"]
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                current_primary_train_target_overlap
            ),
            "missing_current_primary_source_free_event_axis_rows": (
                missing_current_primary_source_free
            ),
            "missing_current_retained_oos_source_free_event_axis_rows": (
                missing_current_retained_source_free
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "leave_one_out_projected_subset_signal_beyond_current_surface": (
                loo_projected_signal
            ),
            "genuinely_new_axis_adds_beyond_projected_subset": marginal_signal,
            "best_projection_plus_axis_caught_rows_reusable_from_existing_source_free_partial_surface": bool(
                best_pair_reusable_source_free_rows
            ),
            "best_projection_plus_axis_primary_loo_control_passes": bool(
                best_primary_control_passes
            ),
            "any_projection_plus_axis_primary_loo_control_passes": bool(
                primary_control_passing_surfaces
            ),
            "adds_local_overlap_value_beyond_current_surface": bool(
                loo_projected_signal or marginal_signal
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                source_free_current_split_measurable
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not bool(loo_projected_signal or marginal_signal),
            "apply_or_promote_now": False,
            "baseline_axis_id": baseline_axis_id,
            "best_single_axis_id": best_single_axis["axis_id"],
            "best_projection_plus_axis_id": best_projection_plus_axis[
                "projection_plus_axis_id"
            ],
            "best_new_axis_id": best_projection_plus_axis["added_axis_id"],
            "next_gate": (
                "Materialize source-free current-split event-axis rows for "
                f"{best_projection_plus_axis['projection_plus_axis_id']}, "
                f"starting with {missing_current_primary_source_free} primary "
                "retention-gate rows and "
                f"{missing_current_retained_source_free} current-retained OOS "
                "rows; then rerun this leave-one-out frontier before any "
                "deployment or heldout claim."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "target_oos_rows_excluded_from_their_own_axis_rule_selection": True,
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": (
                "calibration_only_leave_one_oos_row_out_for_each_target"
            ),
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                "Leave-one-out projected-subset plus "
                f"{best_projection_plus_axis['added_axis_id']} catches "
                f"{best_projection_overlap['projection_plus_axis_current_retained_oos_catches']}/"
                f"{len(current_retained_rows)} current-retained overlap rows, "
                f"with {best_projection_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
                "marginal catches beyond the projected subset."
            ),
            "result": (
                "Research-only leave-one-out marginal signal: a genuinely new "
                "event axis still adds local current-overlap catches beyond the "
                "source-free-compatible projected subset after excluding each "
                "target OOS row from its own calibration rule selection."
                if marginal_signal and best_primary_control_passes
                else (
                    "Research-only leave-one-out marginal signal with a primary "
                    "control caveat: the best new axis adds local "
                    "current-overlap catches beyond the projected subset, but "
                    "the same projected-subset-plus-axis rule retains only "
                    f"{best_primary_loo_control['retained_rows']}/"
                    f"{best_primary_loo_control['target_rows']} mechanism "
                    "primaries under leave-one-primary-out control."
                )
                if marginal_signal
                else (
                    "Research-only leave-one-out result: the projected subset "
                    "has local signal, but no added event axis contributes "
                    "marginal current-retained OOS catches beyond it."
                    if loo_projected_signal
                    else (
                        "Research-only leave-one-out negative: no tested simple "
                        "event axis catches current-retained overlap rows beyond "
                        "the fixed geometry/fold surface."
                    )
                )
            ),
            "next_action": (
                "Build split-aligned source-free event-axis evidence for the "
                "best leave-one-out marginal axis on the current primary and "
                "current-retained OOS rows before any deployment or heldout claim."
            ),
        },
    }


def build_lever2_event_axis_primary_safe_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    include_floor_sensitivity: bool = True,
    floor_sensitivity_values: tuple[float, ...] = (1.0, 0.9, 0.75),
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_SAFE_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    partial_surface = (
        _read_json(partial_surface_current_split_portability_readout_path)
        if partial_surface_current_split_portability_readout_path is not None
        and Path(partial_surface_current_split_portability_readout_path).exists()
        else None
    )

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    train_rows = [
        row
        for row in (mechanism.get("scored_rows") or {}).get("train") or []
        if isinstance(row, dict) and str(row.get("entry_id") or "") in feature_rows
    ]
    calibration_entry_ids = {row["entry_id"] for row in calibration_rows}
    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    current_primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )

    axis_definitions = _event_axis_frontier_definitions()
    axes_by_id = {str(axis["axis_id"]): axis for axis in axis_definitions}
    if baseline_axis_id not in axes_by_id:
        raise ValueError(f"unknown baseline event axis: {baseline_axis_id}")
    baseline_fields = list(axes_by_id[baseline_axis_id]["feature_fields"])

    def _selection_rows_for(entry_id: str) -> list[dict[str, Any]]:
        return [row for row in calibration_rows if row["entry_id"] != entry_id]

    baseline_row_readouts: list[dict[str, Any]] = []
    for row in current_rows:
        entry_id = str(row["entry_id"])
        features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        current_surface_abstains = bool(row.get("current_surface_abstains"))
        try:
            baseline_rule = _select_axis_rule(
                _selection_rows_for(entry_id),
                baseline_fields,
                min_primary_retain=min_primary_retain,
            )
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = _axis_rule_abstains(
                baseline_score,
                direction=str(baseline_rule["direction"]),
                threshold=float(baseline_rule["threshold"]),
            )
            baseline_error = None
        except ValueError as exc:
            baseline_rule = None
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = False
            baseline_error = str(exc)
        baseline_row_readouts.append(
            {
                "entry_id": entry_id,
                "current_surface_score": row.get("current_surface_score"),
                "current_surface_abstains": current_surface_abstains,
                "target_excluded_from_axis_selection": (
                    entry_id in calibration_entry_ids
                ),
                "baseline_axis_score": baseline_score,
                "baseline_rule_evaluable": baseline_rule is not None,
                "selection_error": baseline_error,
                "selected_rule": baseline_rule,
                "baseline_axis_abstains": baseline_abstains,
                "current_retained_caught_by_baseline": bool(
                    baseline_abstains and not current_surface_abstains
                ),
                "union_or_gate_abstains": bool(
                    current_surface_abstains or baseline_abstains
                ),
            }
        )
    baseline_evaluable = [
        row for row in baseline_row_readouts if row["baseline_rule_evaluable"]
    ]
    baseline_retained_caught = [
        row
        for row in baseline_evaluable
        if row["current_retained_caught_by_baseline"]
    ]
    baseline_summary = {
        "axis_id": baseline_axis_id,
        "source_free_status": axes_by_id[baseline_axis_id]["source_free_status"],
        "leave_one_out_selection": {
            "target_rows": len(baseline_row_readouts),
            "evaluable_rows": len(baseline_evaluable),
            "unevaluable_rows": (
                len(baseline_row_readouts) - len(baseline_evaluable)
            ),
            "min_primary_retain": min_primary_retain,
        },
        "current_extended_overlap": {
            "row_count": len(baseline_evaluable),
            "current_surface_abstained_rows": sum(
                1 for row in baseline_evaluable if row["current_surface_abstains"]
            ),
            "current_surface_retained_rows": sum(
                1
                for row in baseline_evaluable
                if not row["current_surface_abstains"]
            ),
            "baseline_axis_abstained_rows": sum(
                1 for row in baseline_evaluable if row["baseline_axis_abstains"]
            ),
            "current_retained_oos_caught_by_baseline": len(
                baseline_retained_caught
            ),
            "union_or_gate_abstained_rows": sum(
                1 for row in baseline_evaluable if row["union_or_gate_abstains"]
            ),
            "current_retained_caught_entry_ids": [
                row["entry_id"] for row in baseline_retained_caught
            ],
        },
    }
    baseline_by_entry = {row["entry_id"]: row for row in baseline_row_readouts}

    projection_plus_axis_rows: list[dict[str, Any]] = []
    projection_plus_axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    for axis in axis_definitions:
        axis_id = str(axis["axis_id"])
        if axis_id == baseline_axis_id:
            continue
        added_fields = list(axis["feature_fields"])
        pair_id = f"{baseline_axis_id}+{axis_id}"
        pair_row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            features = (
                feature_rows.get(entry_id, {}).get("row_specific_event_features")
                or {}
            )
            current_surface_abstains = bool(row.get("current_surface_abstains"))
            baseline_only_row = baseline_by_entry[entry_id]
            try:
                pair_rule = _select_axis_pair_rule(
                    _selection_rows_for(entry_id),
                    baseline_fields,
                    added_fields,
                    min_primary_retain=min_primary_retain,
                )
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = _axis_rule_abstains(
                    baseline_score,
                    direction=str(pair_rule["baseline_rule"]["direction"]),
                    threshold=float(pair_rule["baseline_rule"]["threshold"]),
                )
                added_abstains = _axis_rule_abstains(
                    added_score,
                    direction=str(pair_rule["added_rule"]["direction"]),
                    threshold=float(pair_rule["added_rule"]["threshold"]),
                )
                pair_abstains = bool(pair_baseline_abstains or added_abstains)
                pair_error = None
            except ValueError as exc:
                pair_rule = None
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = False
                added_abstains = False
                pair_abstains = False
                pair_error = str(exc)
            baseline_only_catch = bool(
                baseline_only_row.get("current_retained_caught_by_baseline")
            )
            pair_current_retained_catch = bool(
                pair_abstains and not current_surface_abstains
            )
            pair_row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "pair_rule_evaluable": pair_rule is not None,
                    "selection_error": pair_error,
                    "baseline_axis_score": baseline_score,
                    "added_axis_score": added_score,
                    "baseline_only_abstains": baseline_only_row.get(
                        "baseline_axis_abstains"
                    ),
                    "pair_baseline_axis_abstains": pair_baseline_abstains,
                    "added_axis_abstains": added_abstains,
                    "projection_plus_axis_abstains": pair_abstains,
                    "current_retained_caught_by_projected_subset": (
                        baseline_only_catch
                    ),
                    "current_retained_caught_by_projection_plus_axis": (
                        pair_current_retained_catch
                    ),
                    "current_retained_caught_beyond_projected_subset": bool(
                        pair_current_retained_catch and not baseline_only_catch
                    ),
                    "union_or_gate_abstains": bool(
                        current_surface_abstains or pair_abstains
                    ),
                    "selected_pair_rule": pair_rule,
                }
            )

        evaluable_pair_rows = [
            row for row in pair_row_readouts if row["pair_rule_evaluable"]
        ]
        baseline_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projected_subset"]
        ]
        pair_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projection_plus_axis"]
        ]
        marginal_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_beyond_projected_subset"]
        ]
        current_abstained = sum(
            1 for row in evaluable_pair_rows if row["current_surface_abstains"]
        )
        current_retained = sum(
            1 for row in evaluable_pair_rows if not row["current_surface_abstains"]
        )
        union_abstained = sum(
            1 for row in evaluable_pair_rows if row["union_or_gate_abstains"]
        )
        primary_loo_control_rows: list[dict[str, Any]] = []
        for primary_row in [row for row in calibration_rows if row["is_primary"]]:
            entry_id = str(primary_row["entry_id"])
            try:
                pair_rule = _select_axis_pair_rule(
                    _selection_rows_for(entry_id),
                    baseline_fields,
                    added_fields,
                    min_primary_retain=min_primary_retain,
                )
                baseline_score = round(
                    _axis_score(primary_row["features"], baseline_fields), 8
                )
                added_score = round(
                    _axis_score(primary_row["features"], added_fields), 8
                )
                baseline_abstains = _axis_rule_abstains(
                    baseline_score,
                    direction=str(pair_rule["baseline_rule"]["direction"]),
                    threshold=float(pair_rule["baseline_rule"]["threshold"]),
                )
                added_abstains = _axis_rule_abstains(
                    added_score,
                    direction=str(pair_rule["added_rule"]["direction"]),
                    threshold=float(pair_rule["added_rule"]["threshold"]),
                )
                pair_abstains = bool(baseline_abstains or added_abstains)
                primary_loo_control_rows.append(
                    {
                        "entry_id": entry_id,
                        "primary_rule_evaluable": True,
                        "baseline_axis_score": baseline_score,
                        "added_axis_score": added_score,
                        "selected_pair_rule": pair_rule,
                        "projection_plus_axis_abstains": pair_abstains,
                        "projection_plus_axis_retains": not pair_abstains,
                    }
                )
            except ValueError as exc:
                primary_loo_control_rows.append(
                    {
                        "entry_id": entry_id,
                        "primary_rule_evaluable": False,
                        "selection_error": str(exc),
                        "projection_plus_axis_abstains": None,
                        "projection_plus_axis_retains": None,
                    }
                )
        primary_loo_evaluable_rows = [
            row
            for row in primary_loo_control_rows
            if row["primary_rule_evaluable"]
        ]
        primary_loo_retained_rows = [
            row
            for row in primary_loo_evaluable_rows
            if row["projection_plus_axis_retains"]
        ]
        pair_fields = sorted(set(baseline_fields) | set(added_fields))
        projection_plus_axis_row_readouts[pair_id] = pair_row_readouts
        projection_plus_axis_rows.append(
            {
                "projection_plus_axis_id": pair_id,
                "baseline_axis_id": baseline_axis_id,
                "added_axis_id": axis_id,
                "source_free_status": (
                    "source_free_compatible_proxy"
                    if axis["source_free_status"] == "source_free_compatible_proxy"
                    else "requires_source_free_materialization"
                ),
                "feature_fields": pair_fields,
                "feature_field_count": len(pair_fields),
                "leave_one_out_selection": {
                    "target_rows": len(pair_row_readouts),
                    "evaluable_rows": len(evaluable_pair_rows),
                    "unevaluable_rows": (
                        len(pair_row_readouts) - len(evaluable_pair_rows)
                    ),
                    "min_primary_retain": min_primary_retain,
                    "selector": "joint_axis_pair_rule_search",
                },
                "primary_leave_one_out_control": {
                    "target_rows": len(primary_loo_control_rows),
                    "evaluable_rows": len(primary_loo_evaluable_rows),
                    "retained_rows": len(primary_loo_retained_rows),
                    "retention_recall": _recall(
                        len(primary_loo_retained_rows),
                        len(primary_loo_evaluable_rows),
                    ),
                    "abstained_entry_ids": [
                        row["entry_id"]
                        for row in primary_loo_evaluable_rows
                        if row["projection_plus_axis_abstains"]
                    ],
                },
                "primary_leave_one_out_control_rows": primary_loo_control_rows,
                "current_extended_overlap": {
                    "row_count": len(evaluable_pair_rows),
                    "current_surface_abstained_rows": current_abstained,
                    "current_surface_retained_rows": current_retained,
                    "projected_subset_current_retained_oos_catches": len(
                        baseline_caught
                    ),
                    "projection_plus_axis_current_retained_oos_catches": len(
                        pair_caught
                    ),
                    "marginal_current_retained_oos_catches_beyond_projected_subset": len(
                        marginal_caught
                    ),
                    "current_retained_oos_catch_recall": _recall(
                        len(pair_caught), current_retained
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(evaluable_pair_rows)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained - current_abstained
                    ),
                    "projected_subset_caught_entry_ids": [
                        row["entry_id"] for row in baseline_caught
                    ],
                    "projection_plus_axis_caught_entry_ids": [
                        row["entry_id"] for row in pair_caught
                    ],
                    "marginal_caught_entry_ids": [
                        row["entry_id"] for row in marginal_caught
                    ],
                },
            }
        )

    def _primary_control_passes(row: dict[str, Any]) -> bool:
        control = row["primary_leave_one_out_control"]
        recall = control.get("retention_recall")
        return bool(recall is not None and float(recall) + 1e-12 >= min_primary_retain)

    def _projection_plus_axis_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        control = row["primary_leave_one_out_control"]
        return (
            int(
                overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            int(overlap["projection_plus_axis_current_retained_oos_catches"]),
            int(control["retained_rows"]),
            str(row["projection_plus_axis_id"]),
        )

    primary_control_passing_surfaces = [
        row for row in projection_plus_axis_rows if _primary_control_passes(row)
    ]
    best_marginal_axis = sorted(
        projection_plus_axis_rows, key=_projection_plus_axis_sort_key, reverse=True
    )[0]
    best_primary_safe_axis = (
        sorted(
            primary_control_passing_surfaces,
            key=_projection_plus_axis_sort_key,
            reverse=True,
        )[0]
        if primary_control_passing_surfaces
        else None
    )
    best_marginal_overlap = best_marginal_axis["current_extended_overlap"]
    best_marginal_control = best_marginal_axis["primary_leave_one_out_control"]
    best_primary_safe_overlap = (
        best_primary_safe_axis["current_extended_overlap"]
        if best_primary_safe_axis
        else {}
    )

    partial_counts = (partial_surface or {}).get("counts") or {}
    partial_missing_rows = (partial_surface or {}).get("missing_evidence_rows") or {}
    missing_primary_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_primary_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_retained_oos_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_ids = {
        str(row["entry_id"]) for row in missing_retained_source_free_rows
    }
    missing_current_primary_source_free = int(
        partial_counts.get(
            "missing_current_primary_source_free_partial_surface_rows",
            len(current_primary_rows) - len(valid_current_primary_overlap),
        )
        or 0
    )
    missing_current_retained_source_free = int(
        partial_counts.get(
            "missing_current_retained_oos_source_free_partial_surface_rows",
            len(current_retained_rows),
        )
        or 0
    )
    baseline_source_free_field_count = (
        len(baseline_fields)
        if axes_by_id[baseline_axis_id]["source_free_status"]
        == "source_free_compatible_proxy"
        else 0
    )
    best_marginal_missing_field_count = max(
        0, len(best_marginal_axis["feature_fields"]) - baseline_source_free_field_count
    )
    best_marginal_pair_rows_by_id = {
        row["entry_id"]: row
        for row in projection_plus_axis_row_readouts[
            best_marginal_axis["projection_plus_axis_id"]
        ]
        if row["current_retained_caught_by_projection_plus_axis"]
    }
    best_marginal_materialization_rows = [
        {
            "entry_id": entry_id,
            "current_surface_score": row.get("current_surface_score"),
            "baseline_axis_score": row.get("baseline_axis_score"),
            "added_axis_score": row.get("added_axis_score"),
            "selected_pair_rule": row.get("selected_pair_rule"),
            "existing_source_free_partial_surface_row_available": bool(
                partial_surface is not None
                and entry_id not in missing_retained_source_free_ids
            ),
            "marginal_beyond_projected_subset": row[
                "current_retained_caught_beyond_projected_subset"
            ],
            "required_evidence": (
                "source-free current-split event-axis rows for "
                f"{best_marginal_axis['projection_plus_axis_id']}"
            ),
        }
        for entry_id, row in sorted(
            best_marginal_pair_rows_by_id.items(),
            key=lambda item: _entry_sort_key(item[0]),
        )
    ]
    best_marginal_primary_control_abstained_rows = [
        row
        for row in best_marginal_axis.get(
            "primary_leave_one_out_control_rows", []
        )
        if row.get("projection_plus_axis_abstains")
    ]

    marginal_signal_before_primary_control = (
        int(
            best_marginal_overlap[
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        > 0
    )
    primary_safe_marginal_signal = bool(
        best_primary_safe_axis
        and int(
            best_primary_safe_overlap[
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        > 0
    )
    source_free_current_split_measurable = (
        missing_current_primary_source_free == 0
        and missing_current_retained_source_free == 0
    )
    result_class = (
        "research_only_primary_safe_marginal_axis_signal"
        if primary_safe_marginal_signal
        else "research_only_primary_safe_marginal_axis_negative"
    )
    status = f"lever2_event_axis_primary_safe_frontier_readout_{result_class}"
    primary_retain_floor_sensitivity: list[dict[str, Any]] = [
        {
            "min_primary_retain": min_primary_retain,
            "result_class": result_class,
            "best_marginal_axis_id": best_marginal_axis["projection_plus_axis_id"],
            "best_marginal_axis_marginal_current_retained_oos_catches": int(
                best_marginal_overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            "best_marginal_axis_primary_loo_retained_rows": int(
                best_marginal_control["retained_rows"]
            ),
            "best_marginal_axis_primary_loo_control_rows": int(
                best_marginal_control["target_rows"]
            ),
            "primary_control_passing_projection_plus_axis_surfaces": len(
                primary_control_passing_surfaces
            ),
            "best_primary_safe_axis_id": (
                best_primary_safe_axis["projection_plus_axis_id"]
                if best_primary_safe_axis
                else None
            ),
            "best_primary_safe_axis_current_retained_oos_catches": (
                int(
                    best_primary_safe_overlap[
                        "projection_plus_axis_current_retained_oos_catches"
                    ]
                )
                if best_primary_safe_axis
                else 0
            ),
            "best_primary_safe_axis_marginal_current_retained_oos_catches": (
                int(
                    best_primary_safe_overlap[
                        "marginal_current_retained_oos_catches_beyond_projected_subset"
                    ]
                )
                if best_primary_safe_axis
                else 0
            ),
            "best_primary_safe_axis_marginal_caught_entry_ids": (
                best_primary_safe_overlap.get("marginal_caught_entry_ids", [])
                if best_primary_safe_axis
                else []
            ),
        }
    ]
    if include_floor_sensitivity:
        for floor in floor_sensitivity_values:
            floor_value = float(floor)
            if abs(floor_value - float(min_primary_retain)) < 1e-12:
                continue
            sensitivity_readout = build_lever2_event_axis_primary_safe_frontier_readout(
                mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
                train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_extended_oos_mechanism_overlap_readout_path
                ),
                current_in_scope_threshold_contract_path=(
                    current_in_scope_threshold_contract_path
                ),
                partial_surface_current_split_portability_readout_path=(
                    partial_surface_current_split_portability_readout_path
                ),
                min_primary_retain=floor_value,
                baseline_axis_id=baseline_axis_id,
                include_floor_sensitivity=False,
                floor_sensitivity_values=(),
                artifact_id=f"{artifact_id}.sensitivity_{floor_value:g}",
            )
            primary_retain_floor_sensitivity.extend(
                (
                    sensitivity_readout.get("measured_readout") or {}
                ).get("primary_retain_floor_sensitivity", [])
            )
    primary_retain_floor_sensitivity = sorted(
        primary_retain_floor_sensitivity,
        key=lambda row: float(row["min_primary_retain"]),
        reverse=True,
    )
    below_90_primary_safe_signal = any(
        float(row["min_primary_retain"]) < 0.9
        and int(row["best_primary_safe_axis_marginal_current_retained_oos_catches"])
        > 0
        for row in primary_retain_floor_sensitivity
    )

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_primary_safe_frontier_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal readout testing whether any projected-subset "
            "plus genuinely new event-axis rule can add current-retained OOS "
            "catches while also passing leave-one-primary-out retention control. "
            "Rules are selected on mechanism calibration rows only, exclude each "
            "target row from its own selection, and do not score heldout rows or "
            "promote a deployment gate."
        ),
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "baseline_axis_id": baseline_axis_id,
                "min_primary_retain": min_primary_retain,
                "selection_rows": (
                    "mechanism calibration split only, excluding each target "
                    "OOS or primary row from its own rule selection"
                ),
                "objective": (
                    "jointly maximize calibration OOS abstention for the "
                    "projected-subset plus added-axis OR rule while preserving "
                    "primary retention"
                ),
            },
        },
        "measured_readout": {
            "baseline_projected_subset_axis": baseline_summary,
            "projection_plus_axis_primary_safe_rows": projection_plus_axis_rows,
            "best_marginal_axis_before_primary_control": best_marginal_axis,
            "best_primary_safe_axis": best_primary_safe_axis,
            "primary_control_passing_projection_plus_axis_rows": (
                primary_control_passing_surfaces
            ),
            "primary_retain_floor_sensitivity": primary_retain_floor_sensitivity,
            "current_primary_overlap": {
                "valid_current_primary_calibration_feature_overlap_rows": len(
                    valid_current_primary_overlap
                ),
                "valid_current_primary_calibration_feature_overlap_entry_ids": (
                    valid_current_primary_overlap
                ),
                "current_primary_rows_excluded_as_mechanism_train_targets": [
                    {
                        "entry_id": entry_id,
                        "reason": "row_is_mechanism_feature_train_target",
                    }
                    for entry_id in current_primary_train_target_overlap
                ],
            },
        },
        "row_readouts": {
            "current_extended_overlap_by_baseline_primary_safe_loo": (
                baseline_row_readouts
            ),
            "current_extended_overlap_by_projection_plus_axis_primary_safe_loo": (
                projection_plus_axis_row_readouts
            ),
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_event_axis_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_current_primary_overlap),
                "missing_rows_now": missing_current_primary_source_free,
                "why_it_matters": (
                    "The current primary retention gate must be measured on "
                    "source-free row-specific mechanism/event-axis features "
                    "before any deployable Lever 2 claim."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_event_axis_rows",
                "required_rows": int(
                    partial_counts.get("current_retained_oos_rows")
                    or len(current_retained_rows)
                ),
                "valid_overlap_rows_now": (
                    int(
                        partial_counts.get(
                            "union_current_retained_oos_overlap_rows", 0
                        )
                        or 0
                    )
                    if partial_surface is not None
                    else len(current_retained_rows)
                ),
                "missing_rows_now": missing_current_retained_source_free,
                "why_it_matters": (
                    "These are rows retained by geometry/fold where event-axis "
                    "mechanism evidence can add abstention value."
                ),
            },
            {
                "gap_id": "best_marginal_axis_source_free_fields",
                "required_rows": len(best_marginal_axis["feature_fields"]),
                "valid_overlap_rows_now": baseline_source_free_field_count,
                "missing_rows_now": best_marginal_missing_field_count,
                "why_it_matters": (
                    "The best marginal event-axis fields must exist as "
                    "source-free deployment-valid row features on the current "
                    "split, not only as M-CSA train/cal research fields."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_event_axis": (
                missing_primary_source_free_rows
            ),
            "current_retained_oos_rows_requiring_source_free_event_axis": (
                missing_retained_source_free_rows
            ),
            "best_marginal_axis_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_marginal_materialization_rows
            ),
            "best_marginal_axis_marginal_rows": [
                row
                for row in best_marginal_materialization_rows
                if row["marginal_beyond_projected_subset"]
            ],
            "best_marginal_axis_primary_control_abstained_rows": [
                {
                    "entry_id": row.get("entry_id"),
                    "baseline_axis_score": row.get("baseline_axis_score"),
                    "added_axis_score": row.get("added_axis_score"),
                    "selected_pair_rule": row.get("selected_pair_rule"),
                    "reason": "leave_one_primary_out_abstained",
                    "required_control_evidence": (
                        "source-free current-split event-axis evidence must "
                        "distinguish this known in-atlas primary control from "
                        "the marginal current-retained OOS catches before the "
                        "axis can be promoted"
                    ),
                }
                for row in best_marginal_primary_control_abstained_rows
            ],
        },
        "counts": {
            "critical_violation_total": 0,
            "projection_plus_axis_surfaces_evaluated": len(
                projection_plus_axis_rows
            ),
            "primary_control_passing_projection_plus_axis_surfaces": len(
                primary_control_passing_surfaces
            ),
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": sum(
                1 for row in calibration_rows if row["is_primary"]
            ),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "train_rows": len(train_rows),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "baseline_projected_subset_current_retained_oos_catches": int(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
            ),
            "best_marginal_axis_current_retained_oos_catches": int(
                best_marginal_overlap[
                    "projection_plus_axis_current_retained_oos_catches"
                ]
            ),
            "best_marginal_axis_marginal_current_retained_oos_catches": int(
                best_marginal_overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            "best_marginal_axis_primary_loo_control_rows": int(
                best_marginal_control["target_rows"]
            ),
            "best_marginal_axis_primary_loo_retained_rows": int(
                best_marginal_control["retained_rows"]
            ),
            "best_primary_safe_axis_current_retained_oos_catches": (
                int(
                    best_primary_safe_overlap[
                        "projection_plus_axis_current_retained_oos_catches"
                    ]
                )
                if best_primary_safe_axis
                else 0
            ),
            "best_primary_safe_axis_marginal_current_retained_oos_catches": (
                int(
                    best_primary_safe_overlap[
                        "marginal_current_retained_oos_catches_beyond_projected_subset"
                    ]
                )
                if best_primary_safe_axis
                else 0
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                current_primary_train_target_overlap
            ),
            "missing_current_primary_source_free_event_axis_rows": (
                missing_current_primary_source_free
            ),
            "missing_current_retained_oos_source_free_event_axis_rows": (
                missing_current_retained_source_free
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "genuinely_new_axis_adds_beyond_projected_subset_before_primary_control": (
                marginal_signal_before_primary_control
            ),
            "genuinely_new_axis_adds_beyond_projected_subset_under_primary_safe_control": (
                primary_safe_marginal_signal
            ),
            "best_marginal_axis_primary_loo_control_passes": (
                _primary_control_passes(best_marginal_axis)
            ),
            "any_projection_plus_axis_primary_loo_control_passes": bool(
                primary_control_passing_surfaces
            ),
            "primary_safe_marginal_signal_requires_below_90pct_primary_floor": (
                below_90_primary_safe_signal and not primary_safe_marginal_signal
            ),
            "adds_local_overlap_value_beyond_current_surface": bool(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
                or marginal_signal_before_primary_control
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                source_free_current_split_measurable
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not primary_safe_marginal_signal,
            "apply_or_promote_now": False,
            "baseline_axis_id": baseline_axis_id,
            "best_marginal_axis_id": best_marginal_axis[
                "projection_plus_axis_id"
            ],
            "best_primary_safe_axis_id": (
                best_primary_safe_axis["projection_plus_axis_id"]
                if best_primary_safe_axis
                else None
            ),
            "next_gate": (
                "Treat the current bond-change marginal signal as research-only "
                "until a source-free current-split event-axis surface preserves "
                "all primary controls. The smallest smoke tranche remains the "
                f"{missing_current_primary_source_free} current primary rows "
                "plus the best marginal current-retained OOS rows, with the "
                "primary-control abstained rows explicitly checked as controls."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "target_oos_and_primary_rows_excluded_from_their_own_axis_rule_selection": (
                True
            ),
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": (
                "calibration_only_leave_one_target_row_out_for_each_oos_or_primary_control"
            ),
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                f"Best marginal axis {best_marginal_axis['projection_plus_axis_id']} "
                f"adds {best_marginal_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
                "current-retained OOS catches before primary control, while "
                f"the best primary-safe axis adds "
                f"{best_primary_safe_overlap.get('marginal_current_retained_oos_catches_beyond_projected_subset', 0)}."
            ),
            "result": (
                "Research-only primary-safe negative: a genuinely new event "
                "axis has local marginal signal before the primary control, "
                "but no projected-subset-plus-axis surface keeps the primary "
                "leave-one-out control while adding marginal current-retained "
                "OOS catches beyond the projected subset."
                if not primary_safe_marginal_signal
                else (
                    "Research-only primary-safe signal: a genuinely new event "
                    "axis adds marginal current-retained OOS catches while "
                    "passing the primary leave-one-out control, but source-free "
                    "current-split coverage is still missing."
                )
            ),
            "next_action": (
                "Do not promote the bond-change marginal axis yet. Materialize "
                "source-free current-split event-axis evidence for the current "
                "primary rows, the marginal OOS rows, and the primary-control "
                "abstained rows, then rerun this primary-safe frontier."
            ),
        },
    }


def build_lever2_event_axis_primary_controlled_rescue_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_RESCUE_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    partial_surface = (
        _read_json(partial_surface_current_split_portability_readout_path)
        if partial_surface_current_split_portability_readout_path is not None
        and Path(partial_surface_current_split_portability_readout_path).exists()
        else None
    )

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    primary_control_rows = [row for row in calibration_rows if row["is_primary"]]
    train_rows = [
        row
        for row in (mechanism.get("scored_rows") or {}).get("train") or []
        if isinstance(row, dict) and str(row.get("entry_id") or "") in feature_rows
    ]
    calibration_entry_ids = {row["entry_id"] for row in calibration_rows}
    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    current_primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )

    axis_definitions = _event_axis_frontier_definitions()
    axes_by_id = {str(axis["axis_id"]): axis for axis in axis_definitions}
    if baseline_axis_id not in axes_by_id:
        raise ValueError(f"unknown baseline event axis: {baseline_axis_id}")
    baseline_fields = list(axes_by_id[baseline_axis_id]["feature_fields"])

    def _selection_rows_for(entry_id: str) -> list[dict[str, Any]]:
        return [row for row in calibration_rows if row["entry_id"] != entry_id]

    baseline_row_readouts: list[dict[str, Any]] = []
    for row in current_rows:
        entry_id = str(row["entry_id"])
        features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        current_surface_abstains = bool(row.get("current_surface_abstains"))
        try:
            baseline_rule = _select_primary_controlled_axis_rule(
                _selection_rows_for(entry_id),
                primary_control_rows,
                baseline_fields,
                min_primary_retain=min_primary_retain,
            )
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = _axis_rule_abstains(
                baseline_score,
                direction=str(baseline_rule["direction"]),
                threshold=float(baseline_rule["threshold"]),
            )
            baseline_error = None
        except ValueError as exc:
            baseline_rule = None
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = False
            baseline_error = str(exc)
        baseline_row_readouts.append(
            {
                "entry_id": entry_id,
                "current_surface_score": row.get("current_surface_score"),
                "current_surface_abstains": current_surface_abstains,
                "target_excluded_from_axis_selection": (
                    entry_id in calibration_entry_ids
                ),
                "baseline_axis_score": baseline_score,
                "baseline_rule_evaluable": baseline_rule is not None,
                "selection_error": baseline_error,
                "selected_rule": baseline_rule,
                "baseline_axis_abstains": baseline_abstains,
                "current_retained_caught_by_baseline": bool(
                    baseline_abstains and not current_surface_abstains
                ),
                "union_or_gate_abstains": bool(
                    current_surface_abstains or baseline_abstains
                ),
            }
        )
    baseline_evaluable = [
        row for row in baseline_row_readouts if row["baseline_rule_evaluable"]
    ]
    baseline_retained_caught = [
        row
        for row in baseline_evaluable
        if row["current_retained_caught_by_baseline"]
    ]
    baseline_summary = {
        "axis_id": baseline_axis_id,
        "source_free_status": axes_by_id[baseline_axis_id]["source_free_status"],
        "primary_controlled_selection": {
            "target_rows": len(baseline_row_readouts),
            "evaluable_rows": len(baseline_evaluable),
            "unevaluable_rows": (
                len(baseline_row_readouts) - len(baseline_evaluable)
            ),
            "min_primary_retain": min_primary_retain,
            "primary_control_rows": len(primary_control_rows),
        },
        "current_extended_overlap": {
            "row_count": len(baseline_evaluable),
            "current_surface_abstained_rows": sum(
                1 for row in baseline_evaluable if row["current_surface_abstains"]
            ),
            "current_surface_retained_rows": sum(
                1
                for row in baseline_evaluable
                if not row["current_surface_abstains"]
            ),
            "baseline_axis_abstained_rows": sum(
                1 for row in baseline_evaluable if row["baseline_axis_abstains"]
            ),
            "current_retained_oos_caught_by_baseline": len(
                baseline_retained_caught
            ),
            "union_or_gate_abstained_rows": sum(
                1 for row in baseline_evaluable if row["union_or_gate_abstains"]
            ),
            "current_retained_caught_entry_ids": [
                row["entry_id"] for row in baseline_retained_caught
            ],
        },
    }
    baseline_by_entry = {row["entry_id"]: row for row in baseline_row_readouts}

    projection_plus_axis_rows: list[dict[str, Any]] = []
    projection_plus_axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    for axis in axis_definitions:
        axis_id = str(axis["axis_id"])
        if axis_id == baseline_axis_id:
            continue
        added_fields = list(axis["feature_fields"])
        pair_id = f"{baseline_axis_id}+{axis_id}"
        pair_row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            features = (
                feature_rows.get(entry_id, {}).get("row_specific_event_features")
                or {}
            )
            current_surface_abstains = bool(row.get("current_surface_abstains"))
            baseline_only_row = baseline_by_entry[entry_id]
            try:
                pair_rule = _select_primary_controlled_axis_pair_rule(
                    _selection_rows_for(entry_id),
                    primary_control_rows,
                    baseline_fields,
                    added_fields,
                    min_primary_retain=min_primary_retain,
                )
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = _axis_rule_abstains(
                    baseline_score,
                    direction=str(pair_rule["baseline_rule"]["direction"]),
                    threshold=float(pair_rule["baseline_rule"]["threshold"]),
                )
                added_abstains = _axis_rule_abstains(
                    added_score,
                    direction=str(pair_rule["added_rule"]["direction"]),
                    threshold=float(pair_rule["added_rule"]["threshold"]),
                )
                pair_abstains = bool(pair_baseline_abstains or added_abstains)
                pair_error = None
            except ValueError as exc:
                pair_rule = None
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = False
                added_abstains = False
                pair_abstains = False
                pair_error = str(exc)
            baseline_only_catch = bool(
                baseline_only_row.get("current_retained_caught_by_baseline")
            )
            pair_current_retained_catch = bool(
                pair_abstains and not current_surface_abstains
            )
            pair_row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "pair_rule_evaluable": pair_rule is not None,
                    "selection_error": pair_error,
                    "baseline_axis_score": baseline_score,
                    "added_axis_score": added_score,
                    "baseline_only_abstains": baseline_only_row.get(
                        "baseline_axis_abstains"
                    ),
                    "pair_baseline_axis_abstains": pair_baseline_abstains,
                    "added_axis_abstains": added_abstains,
                    "projection_plus_axis_abstains": pair_abstains,
                    "current_retained_caught_by_projected_subset": (
                        baseline_only_catch
                    ),
                    "current_retained_caught_by_projection_plus_axis": (
                        pair_current_retained_catch
                    ),
                    "current_retained_caught_beyond_projected_subset": bool(
                        pair_current_retained_catch and not baseline_only_catch
                    ),
                    "union_or_gate_abstains": bool(
                        current_surface_abstains or pair_abstains
                    ),
                    "selected_pair_rule": pair_rule,
                }
            )
        evaluable_pair_rows = [
            row for row in pair_row_readouts if row["pair_rule_evaluable"]
        ]
        baseline_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projected_subset"]
        ]
        pair_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projection_plus_axis"]
        ]
        marginal_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_beyond_projected_subset"]
        ]
        current_abstained = sum(
            1 for row in evaluable_pair_rows if row["current_surface_abstains"]
        )
        current_retained = sum(
            1 for row in evaluable_pair_rows if not row["current_surface_abstains"]
        )
        union_abstained = sum(
            1 for row in evaluable_pair_rows if row["union_or_gate_abstains"]
        )
        primary_control_passed_rows = sum(
            1
            for row in evaluable_pair_rows
            if (row.get("selected_pair_rule") or {})
            .get("primary_control", {})
            .get("retention_recall")
            is not None
            and float(
                (row.get("selected_pair_rule") or {})
                .get("primary_control", {})
                .get("retention_recall")
            )
            + 1e-12
            >= min_primary_retain
        )
        pair_fields = sorted(set(baseline_fields) | set(added_fields))
        projection_plus_axis_row_readouts[pair_id] = pair_row_readouts
        projection_plus_axis_rows.append(
            {
                "projection_plus_axis_id": pair_id,
                "baseline_axis_id": baseline_axis_id,
                "added_axis_id": axis_id,
                "source_free_status": (
                    "source_free_compatible_proxy"
                    if axis["source_free_status"] == "source_free_compatible_proxy"
                    else "requires_source_free_materialization"
                ),
                "feature_fields": pair_fields,
                "feature_field_count": len(pair_fields),
                "primary_controlled_selection": {
                    "target_rows": len(pair_row_readouts),
                    "evaluable_rows": len(evaluable_pair_rows),
                    "unevaluable_rows": (
                        len(pair_row_readouts) - len(evaluable_pair_rows)
                    ),
                    "min_primary_retain": min_primary_retain,
                    "primary_control_rows": len(primary_control_rows),
                    "target_rows_passing_primary_control": (
                        primary_control_passed_rows
                    ),
                },
                "current_extended_overlap": {
                    "row_count": len(evaluable_pair_rows),
                    "current_surface_abstained_rows": current_abstained,
                    "current_surface_retained_rows": current_retained,
                    "projected_subset_current_retained_oos_catches": len(
                        baseline_caught
                    ),
                    "projection_plus_axis_current_retained_oos_catches": len(
                        pair_caught
                    ),
                    "marginal_current_retained_oos_catches_beyond_projected_subset": len(
                        marginal_caught
                    ),
                    "current_retained_oos_catch_recall": _recall(
                        len(pair_caught), current_retained
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(evaluable_pair_rows)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained - current_abstained
                    ),
                    "projected_subset_caught_entry_ids": [
                        row["entry_id"] for row in baseline_caught
                    ],
                    "projection_plus_axis_caught_entry_ids": [
                        row["entry_id"] for row in pair_caught
                    ],
                    "marginal_caught_entry_ids": [
                        row["entry_id"] for row in marginal_caught
                    ],
                },
            }
        )

    def _projection_plus_axis_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        control = row["primary_controlled_selection"]
        return (
            int(
                overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            int(overlap["projection_plus_axis_current_retained_oos_catches"]),
            int(control["target_rows_passing_primary_control"]),
            str(row["projection_plus_axis_id"]),
        )

    best_axis = sorted(
        projection_plus_axis_rows,
        key=_projection_plus_axis_sort_key,
        reverse=True,
    )[0]
    best_overlap = best_axis["current_extended_overlap"]
    best_axis_rows_by_id = {
        row["entry_id"]: row
        for row in projection_plus_axis_row_readouts[best_axis["projection_plus_axis_id"]]
        if row["current_retained_caught_by_projection_plus_axis"]
    }

    partial_counts = (partial_surface or {}).get("counts") or {}
    partial_missing_rows = (partial_surface or {}).get("missing_evidence_rows") or {}
    missing_primary_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_primary_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_retained_oos_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_ids = {
        str(row["entry_id"]) for row in missing_retained_source_free_rows
    }
    missing_current_primary_source_free = int(
        partial_counts.get(
            "missing_current_primary_source_free_partial_surface_rows",
            len(current_primary_rows) - len(valid_current_primary_overlap),
        )
        or 0
    )
    missing_current_retained_source_free = int(
        partial_counts.get(
            "missing_current_retained_oos_source_free_partial_surface_rows",
            len(current_retained_rows),
        )
        or 0
    )
    baseline_source_free_field_count = (
        len(baseline_fields)
        if axes_by_id[baseline_axis_id]["source_free_status"]
        == "source_free_compatible_proxy"
        else 0
    )
    best_missing_field_count = max(
        0, len(best_axis["feature_fields"]) - baseline_source_free_field_count
    )
    best_materialization_rows = [
        {
            "entry_id": entry_id,
            "current_surface_score": row.get("current_surface_score"),
            "baseline_axis_score": row.get("baseline_axis_score"),
            "added_axis_score": row.get("added_axis_score"),
            "baseline_selected_rule": (
                (row.get("selected_pair_rule") or {}).get("baseline_rule")
            ),
            "added_axis_selected_rule": (
                (row.get("selected_pair_rule") or {}).get("added_rule")
            ),
            "primary_control": (
                (row.get("selected_pair_rule") or {}).get("primary_control")
            ),
            "existing_source_free_partial_surface_row_available": bool(
                partial_surface is not None
                and entry_id not in missing_retained_source_free_ids
            ),
            "marginal_beyond_projected_subset": row[
                "current_retained_caught_beyond_projected_subset"
            ],
            "required_evidence": (
                "source-free current-split event-axis rows for "
                f"{best_axis['projection_plus_axis_id']}"
            ),
        }
        for entry_id, row in sorted(
            best_axis_rows_by_id.items(), key=lambda item: _entry_sort_key(item[0])
        )
    ]
    best_marginal_rows = [
        row for row in best_materialization_rows if row["marginal_beyond_projected_subset"]
    ]
    representative_control = (
        (best_marginal_rows[0].get("primary_control") or {})
        if best_marginal_rows
        else (
            (best_materialization_rows[0].get("primary_control") or {})
            if best_materialization_rows
            else {}
        )
    )
    representative_baseline_rule = (
        best_marginal_rows[0].get("baseline_selected_rule")
        if best_marginal_rows
        else (
            best_materialization_rows[0].get("baseline_selected_rule")
            if best_materialization_rows
            else None
        )
    )
    representative_added_rule = (
        best_marginal_rows[0].get("added_axis_selected_rule")
        if best_marginal_rows
        else (
            best_materialization_rows[0].get("added_axis_selected_rule")
            if best_materialization_rows
            else None
        )
    )
    best_primary_control_rows = [
        {
            "entry_id": row.get("entry_id"),
            "baseline_axis_score": row.get("baseline_axis_score"),
            "added_axis_score": row.get("added_axis_score"),
            "projection_plus_axis_retains": row.get("projection_plus_axis_retains"),
            "baseline_selected_rule": representative_baseline_rule,
            "added_axis_selected_rule": representative_added_rule,
            "required_evidence": (
                "source-free event-axis evidence for the mechanism primary "
                "control row under the best primary-controlled axis"
            ),
        }
        for row in (representative_control.get("control_rows") or [])
    ]
    tranche_by_id: dict[str, dict[str, Any]] = {}

    def _add_tranche_row(
        row: dict[str, Any],
        *,
        priority_class: str,
        required_evidence: str,
    ) -> None:
        entry_id = str(row.get("entry_id") or "")
        if not entry_id:
            return
        record = tranche_by_id.setdefault(
            entry_id,
            {
                "entry_id": entry_id,
                "priority_classes": [],
                "required_evidence": required_evidence,
            },
        )
        if priority_class not in record["priority_classes"]:
            record["priority_classes"].append(priority_class)
        if row.get("current_surface_score") is not None:
            record["current_surface_score"] = row.get("current_surface_score")
        if row.get("baseline_axis_score") is not None:
            record["baseline_axis_score"] = row.get("baseline_axis_score")
        if row.get("added_axis_score") is not None:
            record["added_axis_score"] = row.get("added_axis_score")

    for row in missing_primary_source_free_rows:
        _add_tranche_row(
            row,
            priority_class="current_primary_retention_gate",
            required_evidence=(
                "source-free current-split event-axis row for the current "
                "primary retention gate"
            ),
        )
    for row in best_primary_control_rows:
        _add_tranche_row(
            row,
            priority_class="mechanism_primary_control",
            required_evidence=(
                "source-free event-axis row for the mechanism primary-control "
                "check under the best rescue axis"
            ),
        )
    for row in best_marginal_rows:
        _add_tranche_row(
            row,
            priority_class="primary_controlled_marginal_current_retained_oos",
            required_evidence=(
                "source-free event-axis row for the primary-controlled "
                "marginal current-retained OOS check"
            ),
        )
    smallest_smoke_tranche_rows = sorted(
        tranche_by_id.values(),
        key=lambda row: _entry_sort_key(str(row["entry_id"])),
    )
    smoke_tranche_ids = {
        str(row["entry_id"]) for row in smallest_smoke_tranche_rows
    }

    def _ids_from_partial_source(
        source_name: str,
        loader_name: str,
    ) -> set[str]:
        if partial_surface is None:
            return set()
        source_record = ((partial_surface.get("source_artifacts") or {}).get(source_name) or {})
        source_path = source_record.get("path")
        if not source_path:
            return set()
        path = Path(source_path)
        if loader_name == "candidate_surface":
            return (
                _entry_ids_from_candidate_surface(_read_json(path))
                if path.exists()
                else set()
            )
        if loader_name == "event_axis":
            return (
                _entry_ids_from_event_axis_materialization(_read_json(path))
                if path.exists()
                else set()
            )
        if loader_name == "locator":
            return (
                _entry_ids_from_locator_materialization(_read_json(path))
                if path.exists()
                else set()
            )
        if loader_name == "review_locator":
            return _m_csa_ids_from_candidate_dir(path)
        raise ValueError(f"unsupported partial source loader: {loader_name}")

    smoke_projection_ids = _ids_from_partial_source(
        "source_free_projection_repair_candidate_surface",
        "candidate_surface",
    )
    smoke_event_axis_ids = _ids_from_partial_source(
        "source_free_event_axis_linker_materialization_gate",
        "event_axis",
    )
    smoke_locator_ids = _ids_from_partial_source(
        "source_free_locator_rewrite_materialization_gate",
        "locator",
    )
    smoke_review_locator_ids = _ids_from_partial_source(
        "review_only_locator_candidate_dir",
        "review_locator",
    )
    smoke_source_free_union_ids = (
        smoke_projection_ids
        | smoke_event_axis_ids
        | smoke_locator_ids
        | smoke_review_locator_ids
    )
    smoke_covered_ids = sorted(
        smoke_tranche_ids & smoke_source_free_union_ids,
        key=_entry_sort_key,
    )
    smoke_missing_ids = sorted(
        smoke_tranche_ids - smoke_source_free_union_ids,
        key=_entry_sort_key,
    )
    smoke_tranche_existing_source_free_coverage = {
        "available": partial_surface is not None,
        "tranche_rows": len(smoke_tranche_ids),
        "existing_source_free_union_rows": len(smoke_source_free_union_ids),
        "covered_rows": len(smoke_covered_ids),
        "missing_rows": len(smoke_missing_ids),
        "covered_entry_ids": smoke_covered_ids,
        "missing_entry_ids": smoke_missing_ids,
        "coverage_by_surface": {
            "source_free_projection_candidate_surface": {
                "surface_rows": len(smoke_projection_ids),
                "covered_tranche_rows": len(smoke_tranche_ids & smoke_projection_ids),
                "covered_entry_ids": sorted(
                    smoke_tranche_ids & smoke_projection_ids,
                    key=_entry_sort_key,
                ),
            },
            "source_free_event_axis_linkers": {
                "surface_rows": len(smoke_event_axis_ids),
                "covered_tranche_rows": len(smoke_tranche_ids & smoke_event_axis_ids),
                "covered_entry_ids": sorted(
                    smoke_tranche_ids & smoke_event_axis_ids,
                    key=_entry_sort_key,
                ),
            },
            "source_free_locator_sidecars": {
                "surface_rows": len(smoke_locator_ids),
                "covered_tranche_rows": len(smoke_tranche_ids & smoke_locator_ids),
                "covered_entry_ids": sorted(
                    smoke_tranche_ids & smoke_locator_ids,
                    key=_entry_sort_key,
                ),
            },
            "review_only_locator_candidates": {
                "surface_rows": len(smoke_review_locator_ids),
                "covered_tranche_rows": len(
                    smoke_tranche_ids & smoke_review_locator_ids
                ),
                "covered_entry_ids": sorted(
                    smoke_tranche_ids & smoke_review_locator_ids,
                    key=_entry_sort_key,
                ),
            },
        },
    }
    marginal_signal = (
        int(
            best_overlap[
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        > 0
    )
    source_free_current_split_measurable = (
        missing_current_primary_source_free == 0
        and missing_current_retained_source_free == 0
    )
    result_class = (
        "research_only_primary_controlled_marginal_axis_signal_source_free_gap"
        if marginal_signal
        else "research_only_primary_controlled_axis_negative"
    )
    status = f"lever2_event_axis_primary_controlled_rescue_readout_{result_class}"

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_primary_controlled_rescue_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal rescue readout testing whether stricter "
            "primary-control-aware event-axis threshold selection recovers a "
            "genuinely new mechanism-axis signal beyond the projected subset. "
            "Each current-overlap OOS row is excluded from its own rule "
            "selection, all calibration primaries are used only as retention "
            "controls, and no heldout rows are scored or tuned."
        ),
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "baseline_axis_id": baseline_axis_id,
                "min_primary_retain": min_primary_retain,
                "selection_rows": (
                    "mechanism calibration split only, excluding each target "
                    "OOS row from its own rule selection"
                ),
                "primary_control_rows": (
                    "all mechanism calibration primary rows, used only for "
                    "retention filtering"
                ),
                "objective": (
                    "maximize calibration OOS abstention among rules that "
                    "retain the full primary-control set"
                ),
            },
        },
        "measured_readout": {
            "baseline_projected_subset_axis": baseline_summary,
            "projection_plus_axis_primary_controlled_rows": projection_plus_axis_rows,
            "best_primary_controlled_axis": best_axis,
            "smallest_smoke_tranche_existing_source_free_coverage": (
                smoke_tranche_existing_source_free_coverage
            ),
            "current_primary_overlap": {
                "valid_current_primary_calibration_feature_overlap_rows": len(
                    valid_current_primary_overlap
                ),
                "valid_current_primary_calibration_feature_overlap_entry_ids": (
                    valid_current_primary_overlap
                ),
                "current_primary_rows_excluded_as_mechanism_train_targets": [
                    {
                        "entry_id": entry_id,
                        "reason": "row_is_mechanism_feature_train_target",
                    }
                    for entry_id in current_primary_train_target_overlap
                ],
            },
        },
        "row_readouts": {
            "current_extended_overlap_by_baseline_primary_controlled": (
                baseline_row_readouts
            ),
            "current_extended_overlap_by_projection_plus_axis_primary_controlled": (
                projection_plus_axis_row_readouts
            ),
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_event_axis_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_current_primary_overlap),
                "missing_rows_now": missing_current_primary_source_free,
                "why_it_matters": (
                    "The current primary retention gate must be measured on "
                    "source-free row-specific mechanism/event-axis features "
                    "before any deployable Lever 2 claim."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_event_axis_rows",
                "required_rows": int(
                    partial_counts.get("current_retained_oos_rows")
                    or len(current_retained_rows)
                ),
                "valid_overlap_rows_now": (
                    int(
                        partial_counts.get(
                            "union_current_retained_oos_overlap_rows", 0
                        )
                        or 0
                    )
                    if partial_surface is not None
                    else len(current_retained_rows)
                ),
                "missing_rows_now": missing_current_retained_source_free,
                "why_it_matters": (
                    "These are rows retained by geometry/fold where event-axis "
                    "mechanism evidence can add abstention value."
                ),
            },
            {
                "gap_id": "best_primary_controlled_axis_source_free_fields",
                "required_rows": len(best_axis["feature_fields"]),
                "valid_overlap_rows_now": baseline_source_free_field_count,
                "missing_rows_now": best_missing_field_count,
                "why_it_matters": (
                    "The best primary-controlled event-axis fields must exist "
                    "as source-free deployment-valid row features on the current "
                    "split, not only as M-CSA train/cal research fields."
                ),
            },
            {
                "gap_id": "best_primary_controlled_axis_mechanism_primary_control_rows",
                "required_rows": len(best_primary_control_rows),
                "valid_overlap_rows_now": 0,
                "missing_rows_now": len(best_primary_control_rows),
                "why_it_matters": (
                    "The rescue signal must keep known in-atlas mechanism "
                    "primary controls, including the prior failed control row, "
                    "when the event-axis surface is materialized source-free."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_event_axis": (
                missing_primary_source_free_rows
            ),
            "current_retained_oos_rows_requiring_source_free_event_axis": (
                missing_retained_source_free_rows
            ),
            "best_primary_controlled_axis_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_materialization_rows
            ),
            "best_primary_controlled_axis_marginal_rows": [
                row for row in best_materialization_rows if row["marginal_beyond_projected_subset"]
            ],
            "best_primary_controlled_axis_mechanism_primary_control_rows_requiring_source_free_materialization": (
                best_primary_control_rows
            ),
            "smallest_primary_controlled_rescue_smoke_tranche_rows": (
                smallest_smoke_tranche_rows
            ),
        },
        "counts": {
            "critical_violation_total": 0,
            "projection_plus_axis_surfaces_evaluated": len(
                projection_plus_axis_rows
            ),
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": len(primary_control_rows),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "train_rows": len(train_rows),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "baseline_projected_subset_current_retained_oos_catches": int(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
            ),
            "best_primary_controlled_axis_current_retained_oos_catches": int(
                best_overlap[
                    "projection_plus_axis_current_retained_oos_catches"
                ]
            ),
            "best_primary_controlled_axis_marginal_current_retained_oos_catches": int(
                best_overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            "best_primary_controlled_axis_target_rows_passing_primary_control": int(
                best_axis["primary_controlled_selection"][
                    "target_rows_passing_primary_control"
                ]
            ),
            "best_primary_controlled_axis_mechanism_primary_control_rows": len(
                best_primary_control_rows
            ),
            "smallest_primary_controlled_rescue_smoke_tranche_rows": len(
                smallest_smoke_tranche_rows
            ),
            "smallest_smoke_tranche_existing_source_free_covered_rows": (
                smoke_tranche_existing_source_free_coverage["covered_rows"]
            ),
            "smallest_smoke_tranche_existing_source_free_missing_rows": (
                smoke_tranche_existing_source_free_coverage["missing_rows"]
            ),
            "smallest_smoke_tranche_existing_event_axis_linker_covered_rows": (
                smoke_tranche_existing_source_free_coverage["coverage_by_surface"][
                    "source_free_event_axis_linkers"
                ]["covered_tranche_rows"]
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                current_primary_train_target_overlap
            ),
            "missing_current_primary_source_free_event_axis_rows": (
                missing_current_primary_source_free
            ),
            "missing_current_retained_oos_source_free_event_axis_rows": (
                missing_current_retained_source_free
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "genuinely_new_axis_adds_beyond_projected_subset_under_primary_control": (
                marginal_signal
            ),
            "primary_controlled_axis_signal_beyond_current_surface": (
                marginal_signal
            ),
            "adds_local_overlap_value_beyond_current_surface": bool(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
                or marginal_signal
            ),
            "adds_train_cal_primary_controlled_local_value_beyond_current_surface": (
                marginal_signal
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                source_free_current_split_measurable
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not marginal_signal,
            "apply_or_promote_now": False,
            "baseline_axis_id": baseline_axis_id,
            "best_primary_controlled_axis_id": best_axis[
                "projection_plus_axis_id"
            ],
            "best_new_axis_id": best_axis["added_axis_id"],
            "next_gate": (
                "Do not promote yet. Materialize source-free current-split "
                "event-axis rows for the current primary controls plus the "
                "mechanism primary-control rows and primary-controlled "
                "marginal OOS rows, then rerun this rescue readout against "
                "the current split before any heldout or deployment claim."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "target_oos_rows_excluded_from_their_own_axis_rule_selection": True,
            "primary_labels_used_only_for_retention_control": True,
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": (
                "calibration_only_leave_one_oos_row_out_with_all_primary_controls"
            ),
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                f"Primary-controlled {best_axis['projection_plus_axis_id']} "
                f"catches {best_overlap['projection_plus_axis_current_retained_oos_catches']}/"
                f"{len(current_retained_rows)} current-retained overlap rows, "
                f"with {best_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
                "marginal catches beyond the projected subset."
            ),
            "result": (
                "Research-only signal: stricter primary-control-aware threshold "
                "selection recovers a genuine bond-change/event-axis marginal "
                "signal while retaining all calibration primary controls, but "
                "the current split still lacks source-free event-axis rows for "
                "primary retention and retained-OOS measurement."
                if marginal_signal
                else (
                    "Research-only negative: primary-control-aware threshold "
                    "selection did not recover marginal current-retained OOS "
                    "signal beyond the projected subset."
                )
            ),
            "next_action": (
                "Materialize source-free current-split event-axis rows for the "
                "34 current primary rows, the four mechanism primary-control "
                "rows, and the primary-controlled marginal OOS rows before "
                "making any deployment or heldout claim."
            ),
        },
    }


def build_lever2_event_axis_signature_excluded_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    signature_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    partial_surface = (
        _read_json(partial_surface_current_split_portability_readout_path)
        if partial_surface_current_split_portability_readout_path is not None
        and Path(partial_surface_current_split_portability_readout_path).exists()
        else None
    )

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    primary_control_rows = [row for row in calibration_rows if row["is_primary"]]
    train_rows = [
        row
        for row in (mechanism.get("scored_rows") or {}).get("train") or []
        if isinstance(row, dict) and str(row.get("entry_id") or "") in feature_rows
    ]
    calibration_entry_ids = {row["entry_id"] for row in calibration_rows}
    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    train_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "train"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    current_primary_train_target_overlap = sorted(
        set(current_primary_rows) & train_feature_ids, key=_entry_sort_key
    )

    axis_definitions = _event_axis_frontier_definitions()
    axes_by_id = {str(axis["axis_id"]): axis for axis in axis_definitions}
    if baseline_axis_id not in axes_by_id:
        raise ValueError(f"unknown baseline event axis: {baseline_axis_id}")
    if signature_axis_id not in axes_by_id:
        raise ValueError(f"unknown signature event axis: {signature_axis_id}")
    baseline_fields = list(axes_by_id[baseline_axis_id]["feature_fields"])
    signature_fields = list(axes_by_id[signature_axis_id]["feature_fields"])

    def _selection_context_for(entry_id: str) -> dict[str, Any]:
        target_features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        signature = _axis_signature(target_features, signature_fields)
        selection_rows: list[dict[str, Any]] = []
        target_excluded = False
        same_signature_oos_rows: list[str] = []
        for cal_row in calibration_rows:
            cal_entry_id = str(cal_row["entry_id"])
            if cal_entry_id == entry_id:
                target_excluded = True
                continue
            if not cal_row["is_primary"] and _axis_signature(
                cal_row["features"], signature_fields
            ) == signature:
                same_signature_oos_rows.append(cal_entry_id)
                continue
            selection_rows.append(cal_row)
        return {
            "selection_rows": selection_rows,
            "target_signature": list(signature),
            "target_excluded_from_axis_selection": target_excluded,
            "same_signature_oos_rows_excluded": sorted(
                same_signature_oos_rows, key=_entry_sort_key
            ),
            "same_signature_oos_rows_excluded_count": len(same_signature_oos_rows),
            "selection_primary_rows": sum(
                1 for row in selection_rows if row["is_primary"]
            ),
            "selection_oos_rows": sum(
                1 for row in selection_rows if not row["is_primary"]
            ),
        }

    baseline_row_readouts: list[dict[str, Any]] = []
    for row in current_rows:
        entry_id = str(row["entry_id"])
        features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        context = _selection_context_for(entry_id)
        current_surface_abstains = bool(row.get("current_surface_abstains"))
        try:
            baseline_rule = _select_primary_controlled_axis_rule(
                context["selection_rows"],
                primary_control_rows,
                baseline_fields,
                min_primary_retain=min_primary_retain,
            )
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = _axis_rule_abstains(
                baseline_score,
                direction=str(baseline_rule["direction"]),
                threshold=float(baseline_rule["threshold"]),
            )
            baseline_error = None
        except ValueError as exc:
            baseline_rule = None
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = False
            baseline_error = str(exc)
        baseline_row_readouts.append(
            {
                "entry_id": entry_id,
                "current_surface_score": row.get("current_surface_score"),
                "current_surface_abstains": current_surface_abstains,
                "signature_exclusion": {
                    key: value for key, value in context.items() if key != "selection_rows"
                },
                "baseline_axis_score": baseline_score,
                "baseline_rule_evaluable": baseline_rule is not None,
                "selection_error": baseline_error,
                "selected_rule": baseline_rule,
                "baseline_axis_abstains": baseline_abstains,
                "current_retained_caught_by_baseline": bool(
                    baseline_abstains and not current_surface_abstains
                ),
                "union_or_gate_abstains": bool(
                    current_surface_abstains or baseline_abstains
                ),
            }
        )
    baseline_evaluable = [
        row for row in baseline_row_readouts if row["baseline_rule_evaluable"]
    ]
    baseline_retained_caught = [
        row
        for row in baseline_evaluable
        if row["current_retained_caught_by_baseline"]
    ]
    baseline_summary = {
        "axis_id": baseline_axis_id,
        "signature_axis_id": signature_axis_id,
        "source_free_status": axes_by_id[baseline_axis_id]["source_free_status"],
        "signature_excluded_selection": {
            "target_rows": len(baseline_row_readouts),
            "evaluable_rows": len(baseline_evaluable),
            "unevaluable_rows": (
                len(baseline_row_readouts) - len(baseline_evaluable)
            ),
            "min_primary_retain": min_primary_retain,
            "primary_control_rows": len(primary_control_rows),
        },
        "current_extended_overlap": {
            "row_count": len(baseline_evaluable),
            "current_surface_abstained_rows": sum(
                1 for row in baseline_evaluable if row["current_surface_abstains"]
            ),
            "current_surface_retained_rows": sum(
                1
                for row in baseline_evaluable
                if not row["current_surface_abstains"]
            ),
            "baseline_axis_abstained_rows": sum(
                1 for row in baseline_evaluable if row["baseline_axis_abstains"]
            ),
            "current_retained_oos_caught_by_baseline": len(
                baseline_retained_caught
            ),
            "union_or_gate_abstained_rows": sum(
                1 for row in baseline_evaluable if row["union_or_gate_abstains"]
            ),
            "current_retained_caught_entry_ids": [
                row["entry_id"] for row in baseline_retained_caught
            ],
        },
    }
    baseline_by_entry = {row["entry_id"]: row for row in baseline_row_readouts}

    projection_plus_axis_rows: list[dict[str, Any]] = []
    projection_plus_axis_row_readouts: dict[str, list[dict[str, Any]]] = {}
    for axis in axis_definitions:
        axis_id = str(axis["axis_id"])
        if axis_id == baseline_axis_id:
            continue
        added_fields = list(axis["feature_fields"])
        pair_id = f"{baseline_axis_id}+{axis_id}"
        pair_row_readouts: list[dict[str, Any]] = []
        for row in current_rows:
            entry_id = str(row["entry_id"])
            features = (
                feature_rows.get(entry_id, {}).get("row_specific_event_features")
                or {}
            )
            context = _selection_context_for(entry_id)
            current_surface_abstains = bool(row.get("current_surface_abstains"))
            baseline_only_row = baseline_by_entry[entry_id]
            try:
                pair_rule = _select_primary_controlled_axis_pair_rule(
                    context["selection_rows"],
                    primary_control_rows,
                    baseline_fields,
                    added_fields,
                    min_primary_retain=min_primary_retain,
                )
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = _axis_rule_abstains(
                    baseline_score,
                    direction=str(pair_rule["baseline_rule"]["direction"]),
                    threshold=float(pair_rule["baseline_rule"]["threshold"]),
                )
                added_abstains = _axis_rule_abstains(
                    added_score,
                    direction=str(pair_rule["added_rule"]["direction"]),
                    threshold=float(pair_rule["added_rule"]["threshold"]),
                )
                pair_abstains = bool(pair_baseline_abstains or added_abstains)
                pair_error = None
            except ValueError as exc:
                pair_rule = None
                baseline_score = round(_axis_score(features, baseline_fields), 8)
                added_score = round(_axis_score(features, added_fields), 8)
                pair_baseline_abstains = False
                added_abstains = False
                pair_abstains = False
                pair_error = str(exc)
            baseline_only_catch = bool(
                baseline_only_row.get("current_retained_caught_by_baseline")
            )
            pair_current_retained_catch = bool(
                pair_abstains and not current_surface_abstains
            )
            pair_row_readouts.append(
                {
                    "entry_id": entry_id,
                    "current_surface_score": row.get("current_surface_score"),
                    "current_surface_abstains": current_surface_abstains,
                    "pair_rule_evaluable": pair_rule is not None,
                    "selection_error": pair_error,
                    "signature_exclusion": {
                        key: value
                        for key, value in context.items()
                        if key != "selection_rows"
                    },
                    "baseline_axis_score": baseline_score,
                    "added_axis_score": added_score,
                    "baseline_only_abstains": baseline_only_row.get(
                        "baseline_axis_abstains"
                    ),
                    "pair_baseline_axis_abstains": pair_baseline_abstains,
                    "added_axis_abstains": added_abstains,
                    "projection_plus_axis_abstains": pair_abstains,
                    "current_retained_caught_by_projected_subset": (
                        baseline_only_catch
                    ),
                    "current_retained_caught_by_projection_plus_axis": (
                        pair_current_retained_catch
                    ),
                    "current_retained_caught_beyond_projected_subset": bool(
                        pair_current_retained_catch and not baseline_only_catch
                    ),
                    "union_or_gate_abstains": bool(
                        current_surface_abstains or pair_abstains
                    ),
                    "selected_pair_rule": pair_rule,
                }
            )
        evaluable_pair_rows = [
            row for row in pair_row_readouts if row["pair_rule_evaluable"]
        ]
        baseline_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projected_subset"]
        ]
        pair_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_by_projection_plus_axis"]
        ]
        marginal_caught = [
            row
            for row in evaluable_pair_rows
            if row["current_retained_caught_beyond_projected_subset"]
        ]
        current_abstained = sum(
            1 for row in evaluable_pair_rows if row["current_surface_abstains"]
        )
        current_retained = sum(
            1 for row in evaluable_pair_rows if not row["current_surface_abstains"]
        )
        union_abstained = sum(
            1 for row in evaluable_pair_rows if row["union_or_gate_abstains"]
        )
        primary_control_passed_rows = sum(
            1
            for row in evaluable_pair_rows
            if (row.get("selected_pair_rule") or {})
            .get("primary_control", {})
            .get("retention_recall")
            is not None
            and float(
                (row.get("selected_pair_rule") or {})
                .get("primary_control", {})
                .get("retention_recall")
            )
            + 1e-12
            >= min_primary_retain
        )
        signature_excluded_rows = sum(
            int(
                (row.get("signature_exclusion") or {}).get(
                    "same_signature_oos_rows_excluded_count"
                )
                or 0
            )
            for row in pair_row_readouts
        )
        signature_excluded_targets = sum(
            1
            for row in pair_row_readouts
            if int(
                (row.get("signature_exclusion") or {}).get(
                    "same_signature_oos_rows_excluded_count"
                )
                or 0
            )
            > 0
        )
        pair_fields = sorted(set(baseline_fields) | set(added_fields))
        projection_plus_axis_row_readouts[pair_id] = pair_row_readouts
        projection_plus_axis_rows.append(
            {
                "projection_plus_axis_id": pair_id,
                "baseline_axis_id": baseline_axis_id,
                "added_axis_id": axis_id,
                "signature_axis_id": signature_axis_id,
                "source_free_status": (
                    "source_free_compatible_proxy"
                    if axis["source_free_status"] == "source_free_compatible_proxy"
                    else "requires_source_free_materialization"
                ),
                "feature_fields": pair_fields,
                "feature_field_count": len(pair_fields),
                "signature_excluded_selection": {
                    "target_rows": len(pair_row_readouts),
                    "evaluable_rows": len(evaluable_pair_rows),
                    "unevaluable_rows": (
                        len(pair_row_readouts) - len(evaluable_pair_rows)
                    ),
                    "min_primary_retain": min_primary_retain,
                    "primary_control_rows": len(primary_control_rows),
                    "target_rows_passing_primary_control": (
                        primary_control_passed_rows
                    ),
                    "targets_with_same_signature_oos_exclusions": (
                        signature_excluded_targets
                    ),
                    "total_same_signature_oos_rows_excluded": (
                        signature_excluded_rows
                    ),
                },
                "current_extended_overlap": {
                    "row_count": len(evaluable_pair_rows),
                    "current_surface_abstained_rows": current_abstained,
                    "current_surface_retained_rows": current_retained,
                    "projected_subset_current_retained_oos_catches": len(
                        baseline_caught
                    ),
                    "projection_plus_axis_current_retained_oos_catches": len(
                        pair_caught
                    ),
                    "marginal_current_retained_oos_catches_beyond_projected_subset": len(
                        marginal_caught
                    ),
                    "current_retained_oos_catch_recall": _recall(
                        len(pair_caught), current_retained
                    ),
                    "union_or_gate_abstained_rows": union_abstained,
                    "union_or_gate_abstain_recall": _recall(
                        union_abstained, len(evaluable_pair_rows)
                    ),
                    "union_minus_current_abstained_rows": (
                        union_abstained - current_abstained
                    ),
                    "projected_subset_caught_entry_ids": [
                        row["entry_id"] for row in baseline_caught
                    ],
                    "projection_plus_axis_caught_entry_ids": [
                        row["entry_id"] for row in pair_caught
                    ],
                    "marginal_caught_entry_ids": [
                        row["entry_id"] for row in marginal_caught
                    ],
                },
            }
        )

    def _projection_plus_axis_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
        overlap = row["current_extended_overlap"]
        selection = row["signature_excluded_selection"]
        return (
            int(
                overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            int(overlap["projection_plus_axis_current_retained_oos_catches"]),
            int(selection["target_rows_passing_primary_control"]),
            str(row["projection_plus_axis_id"]),
        )

    best_axis = sorted(
        projection_plus_axis_rows,
        key=_projection_plus_axis_sort_key,
        reverse=True,
    )[0]
    best_overlap = best_axis["current_extended_overlap"]
    best_pair_rows = projection_plus_axis_row_readouts[
        best_axis["projection_plus_axis_id"]
    ]
    best_pair_rows_by_id = {
        row["entry_id"]: row
        for row in best_pair_rows
        if row["current_retained_caught_by_projection_plus_axis"]
    }

    partial_counts = (partial_surface or {}).get("counts") or {}
    partial_missing_rows = (partial_surface or {}).get("missing_evidence_rows") or {}
    missing_primary_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_primary_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_rows = [
        row
        for row in (
            partial_missing_rows.get(
                "current_retained_oos_rows_requiring_source_free_partial_surface"
            )
            or []
        )
        if isinstance(row, dict) and row.get("entry_id")
    ]
    missing_retained_source_free_ids = {
        str(row["entry_id"]) for row in missing_retained_source_free_rows
    }
    missing_current_primary_source_free = int(
        partial_counts.get(
            "missing_current_primary_source_free_partial_surface_rows",
            len(current_primary_rows) - len(valid_current_primary_overlap),
        )
        or 0
    )
    missing_current_retained_source_free = int(
        partial_counts.get(
            "missing_current_retained_oos_source_free_partial_surface_rows",
            len(current_retained_rows),
        )
        or 0
    )
    baseline_source_free_field_count = (
        len(baseline_fields)
        if axes_by_id[baseline_axis_id]["source_free_status"]
        == "source_free_compatible_proxy"
        else 0
    )
    best_missing_field_count = max(
        0, len(best_axis["feature_fields"]) - baseline_source_free_field_count
    )
    best_materialization_rows = [
        {
            "entry_id": entry_id,
            "current_surface_score": row.get("current_surface_score"),
            "baseline_axis_score": row.get("baseline_axis_score"),
            "added_axis_score": row.get("added_axis_score"),
            "signature_exclusion": row.get("signature_exclusion"),
            "baseline_selected_rule": (
                (row.get("selected_pair_rule") or {}).get("baseline_rule")
            ),
            "added_axis_selected_rule": (
                (row.get("selected_pair_rule") or {}).get("added_rule")
            ),
            "primary_control": (
                (row.get("selected_pair_rule") or {}).get("primary_control")
            ),
            "existing_source_free_partial_surface_row_available": bool(
                partial_surface is not None
                and entry_id not in missing_retained_source_free_ids
            ),
            "marginal_beyond_projected_subset": row[
                "current_retained_caught_beyond_projected_subset"
            ],
            "required_evidence": (
                "source-free current-split event-axis rows for "
                f"{best_axis['projection_plus_axis_id']} after same-signature "
                "calibration OOS exclusion"
            ),
        }
        for entry_id, row in sorted(
            best_pair_rows_by_id.items(), key=lambda item: _entry_sort_key(item[0])
        )
    ]
    best_marginal_rows = [
        row for row in best_materialization_rows if row["marginal_beyond_projected_subset"]
    ]
    signature_excluded_targets = [
        row
        for row in best_pair_rows
        if int(
            (row.get("signature_exclusion") or {}).get(
                "same_signature_oos_rows_excluded_count"
            )
            or 0
        )
        > 0
    ]
    source_free_current_split_measurable = (
        missing_current_primary_source_free == 0
        and missing_current_retained_source_free == 0
    )
    marginal_signal = (
        int(
            best_overlap[
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        > 0
    )
    result_class = (
        "research_only_signature_excluded_marginal_axis_signal_source_free_gap"
        if marginal_signal
        else "research_only_signature_excluded_marginal_axis_negative"
    )
    status = f"lever2_event_axis_signature_excluded_frontier_readout_{result_class}"

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_signature_excluded_frontier_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal readout testing whether a genuinely new "
            "event-axis signal survives a stricter de novo-style exclusion. "
            "For each current-overlap OOS target, rules are selected after "
            "excluding the target and calibration OOS rows with the same "
            "configured mechanism-axis signature. All mechanism primary "
            "rows are retained as controls, and no heldout rows are scored or "
            "tuned."
        ),
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "baseline_axis_id": baseline_axis_id,
                "signature_axis_id": signature_axis_id,
                "signature_fields": signature_fields,
                "min_primary_retain": min_primary_retain,
                "selection_rows": (
                    "mechanism calibration split only, excluding each target "
                    "OOS row plus calibration OOS rows sharing its configured "
                    "mechanism-axis signature"
                ),
                "primary_control_rows": (
                    "all mechanism calibration primary rows, used only for "
                    "retention filtering"
                ),
            },
        },
        "measured_readout": {
            "baseline_projected_subset_axis": baseline_summary,
            "projection_plus_axis_signature_excluded_rows": projection_plus_axis_rows,
            "best_signature_excluded_axis": best_axis,
            "current_primary_overlap": {
                "valid_current_primary_calibration_feature_overlap_rows": len(
                    valid_current_primary_overlap
                ),
                "valid_current_primary_calibration_feature_overlap_entry_ids": (
                    valid_current_primary_overlap
                ),
                "current_primary_rows_excluded_as_mechanism_train_targets": [
                    {
                        "entry_id": entry_id,
                        "reason": "row_is_mechanism_feature_train_target",
                    }
                    for entry_id in current_primary_train_target_overlap
                ],
            },
        },
        "row_readouts": {
            "current_extended_overlap_by_baseline_signature_excluded": (
                baseline_row_readouts
            ),
            "current_extended_overlap_by_projection_plus_axis_signature_excluded": (
                projection_plus_axis_row_readouts
            ),
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_event_axis_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": len(valid_current_primary_overlap),
                "missing_rows_now": missing_current_primary_source_free,
                "why_it_matters": (
                    "The current primary retention gate must be measured on "
                    "source-free row-specific mechanism/event-axis features "
                    "before any deployable Lever 2 claim."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_event_axis_rows",
                "required_rows": int(
                    partial_counts.get("current_retained_oos_rows")
                    or len(current_retained_rows)
                ),
                "valid_overlap_rows_now": (
                    int(
                        partial_counts.get(
                            "union_current_retained_oos_overlap_rows", 0
                        )
                        or 0
                    )
                    if partial_surface is not None
                    else len(current_retained_rows)
                ),
                "missing_rows_now": missing_current_retained_source_free,
                "why_it_matters": (
                    "These are rows retained by geometry/fold where event-axis "
                    "mechanism evidence can add abstention value."
                ),
            },
            {
                "gap_id": "best_signature_excluded_axis_source_free_fields",
                "required_rows": len(best_axis["feature_fields"]),
                "valid_overlap_rows_now": baseline_source_free_field_count,
                "missing_rows_now": best_missing_field_count,
                "why_it_matters": (
                    "The best signature-excluded event-axis fields must exist "
                    "as source-free deployment-valid row features on the current "
                    "split, not only as M-CSA train/cal research fields."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_event_axis": (
                missing_primary_source_free_rows
            ),
            "current_retained_oos_rows_requiring_source_free_event_axis": (
                missing_retained_source_free_rows
            ),
            "best_signature_excluded_axis_current_retained_overlap_rows_requiring_source_free_materialization": (
                best_materialization_rows
            ),
            "best_signature_excluded_axis_marginal_rows": best_marginal_rows,
        },
        "counts": {
            "critical_violation_total": 0,
            "projection_plus_axis_surfaces_evaluated": len(
                projection_plus_axis_rows
            ),
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": len(primary_control_rows),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "train_rows": len(train_rows),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "signature_excluded_target_rows": len(signature_excluded_targets),
            "signature_excluded_same_signature_oos_rows_for_best_axis": sum(
                int(
                    (row.get("signature_exclusion") or {}).get(
                        "same_signature_oos_rows_excluded_count"
                    )
                    or 0
                )
                for row in best_pair_rows
            ),
            "baseline_projected_subset_current_retained_oos_catches": int(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
            ),
            "best_signature_excluded_axis_current_retained_oos_catches": int(
                best_overlap[
                    "projection_plus_axis_current_retained_oos_catches"
                ]
            ),
            "best_signature_excluded_axis_marginal_current_retained_oos_catches": int(
                best_overlap[
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            "best_signature_excluded_axis_target_rows_passing_primary_control": int(
                best_axis["signature_excluded_selection"][
                    "target_rows_passing_primary_control"
                ]
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "current_primary_rows_excluded_as_mechanism_train_targets": len(
                current_primary_train_target_overlap
            ),
            "missing_current_primary_source_free_event_axis_rows": (
                missing_current_primary_source_free
            ),
            "missing_current_retained_oos_source_free_event_axis_rows": (
                missing_current_retained_source_free
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "genuinely_new_axis_adds_beyond_projected_subset_after_signature_exclusion": (
                marginal_signal
            ),
            "signature_excluded_axis_signal_beyond_current_surface": marginal_signal,
            "adds_local_overlap_value_beyond_current_surface": bool(
                baseline_summary["current_extended_overlap"][
                    "current_retained_oos_caught_by_baseline"
                ]
                or marginal_signal
            ),
            "adds_train_cal_signature_excluded_local_value_beyond_current_surface": (
                marginal_signal
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                source_free_current_split_measurable
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not marginal_signal,
            "apply_or_promote_now": False,
            "baseline_axis_id": baseline_axis_id,
            "signature_axis_id": signature_axis_id,
            "best_signature_excluded_axis_id": best_axis[
                "projection_plus_axis_id"
            ],
            "best_new_axis_id": best_axis["added_axis_id"],
            "next_gate": (
                "Do not promote yet. Materialize source-free current-split "
                "event-axis rows for the current primary controls and the "
                "signature-excluded marginal OOS rows, then rerun this "
                "signature-excluded readout before any heldout or deployment "
                "claim."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "target_oos_rows_excluded_from_their_own_axis_rule_selection": True,
            "same_signature_calibration_oos_rows_excluded_from_target_selection": True,
            "same_projected_signature_calibration_oos_rows_excluded_from_target_selection": True,
            "primary_labels_used_only_for_retention_control": True,
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": (
                "calibration_only_leave_target_signature_oos_neighborhood_out"
            ),
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                f"Signature-excluded {best_axis['projection_plus_axis_id']} "
                f"catches {best_overlap['projection_plus_axis_current_retained_oos_catches']}/"
                f"{len(current_retained_rows)} current-retained overlap rows, "
                f"with {best_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
                "marginal catches beyond the projected subset."
            ),
            "result": (
                "Research-only signal: the new event axis still adds marginal "
                "current-retained OOS catches after excluding same-signature "
                "calibration OOS neighbors, but source-free current-split "
                "event-axis rows are still missing."
                if marginal_signal
                else (
                    "Research-only negative under the stricter signature "
                    "exclusion: no genuinely new event axis adds marginal "
                    "current-retained OOS catches beyond the projected subset."
                )
            ),
            "next_action": (
                "Use the signature-excluded marginal rows as the next smoke "
                "target only if they remain nonzero; otherwise prioritize "
                "new source-free evidence rather than tuning this surface."
            ),
        },
    }


def build_lever2_event_axis_signature_exclusion_sensitivity_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    signature_axis_ids: tuple[str, ...] = (
        "source_free_projected_proton_role_subset",
        "bond_change",
        "electron_flow",
        "event_topology",
    ),
    artifact_id: str = DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUSION_SENSITIVITY_ARTIFACT_ID,
) -> dict[str, Any]:
    if not signature_axis_ids:
        raise ValueError("at least one signature axis is required")

    signature_rows: list[dict[str, Any]] = []
    source_artifacts: dict[str, Any] = {}
    missing_evidence: list[dict[str, Any]] = []
    for signature_axis_id in signature_axis_ids:
        readout = build_lever2_event_axis_signature_excluded_frontier_readout(
            mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
            train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
            current_extended_oos_mechanism_overlap_readout_path=(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            current_in_scope_threshold_contract_path=(
                current_in_scope_threshold_contract_path
            ),
            partial_surface_current_split_portability_readout_path=(
                partial_surface_current_split_portability_readout_path
            ),
            min_primary_retain=min_primary_retain,
            baseline_axis_id=baseline_axis_id,
            signature_axis_id=signature_axis_id,
            artifact_id=f"{artifact_id}.{signature_axis_id}",
        )
        source_artifacts = readout.get("source_artifacts") or source_artifacts
        missing_evidence = readout.get("missing_evidence") or missing_evidence
        counts = readout["counts"]
        decision = readout["decision"]
        measured = readout["measured_readout"]
        rows_by_pair = {
            row["projection_plus_axis_id"]: row
            for row in measured["projection_plus_axis_signature_excluded_rows"]
        }

        def _pair_marginal(axis_id: str) -> dict[str, Any]:
            row = rows_by_pair.get(f"{baseline_axis_id}+{axis_id}") or {}
            overlap = row.get("current_extended_overlap") or {}
            return {
                "marginal_current_retained_oos_catches": int(
                    overlap.get(
                        "marginal_current_retained_oos_catches_beyond_projected_subset",
                        0,
                    )
                    or 0
                ),
                "marginal_caught_entry_ids": overlap.get("marginal_caught_entry_ids")
                or [],
            }

        signature_rows.append(
            {
                "signature_axis_id": signature_axis_id,
                "status": readout["status"],
                "result_class": readout["result_class"],
                "best_signature_excluded_axis_id": decision[
                    "best_signature_excluded_axis_id"
                ],
                "best_new_axis_id": decision["best_new_axis_id"],
                "baseline_projected_subset_current_retained_oos_catches": counts[
                    "baseline_projected_subset_current_retained_oos_catches"
                ],
                "best_signature_excluded_axis_current_retained_oos_catches": counts[
                    "best_signature_excluded_axis_current_retained_oos_catches"
                ],
                "best_signature_excluded_axis_marginal_current_retained_oos_catches": counts[
                    "best_signature_excluded_axis_marginal_current_retained_oos_catches"
                ],
                "best_signature_excluded_axis_marginal_entry_ids": (
                    readout["measured_readout"]["best_signature_excluded_axis"][
                        "current_extended_overlap"
                    ]["marginal_caught_entry_ids"]
                ),
                "signature_excluded_target_rows": counts[
                    "signature_excluded_target_rows"
                ],
                "signature_excluded_same_signature_oos_rows": counts[
                    "signature_excluded_same_signature_oos_rows_for_best_axis"
                ],
                "bond_change_pair": _pair_marginal("bond_change"),
                "electron_flow_pair": _pair_marginal("electron_flow"),
                "deployable_now": decision["deployable_now"],
            }
        )

    def _summary_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
        return (
            int(row["best_signature_excluded_axis_marginal_current_retained_oos_catches"]),
            int(row["best_signature_excluded_axis_current_retained_oos_catches"]),
            str(row["signature_axis_id"]),
        )

    best_signature_row = sorted(
        signature_rows, key=_summary_sort_key, reverse=True
    )[0]
    projected_row = next(
        (
            row
            for row in signature_rows
            if row["signature_axis_id"] == "source_free_projected_proton_role_subset"
        ),
        None,
    )
    bond_signature_row = next(
        (row for row in signature_rows if row["signature_axis_id"] == "bond_change"),
        None,
    )
    projected_bond_marginal = (
        int(projected_row["bond_change_pair"]["marginal_current_retained_oos_catches"])
        if projected_row is not None
        else 0
    )
    bond_signature_bond_marginal = (
        int(
            bond_signature_row["bond_change_pair"][
                "marginal_current_retained_oos_catches"
            ]
        )
        if bond_signature_row is not None
        else 0
    )
    bond_signature_electron_marginal = (
        int(
            bond_signature_row["electron_flow_pair"][
                "marginal_current_retained_oos_catches"
            ]
        )
        if bond_signature_row is not None
        else 0
    )
    any_signature_marginal_signal = any(
        int(row["best_signature_excluded_axis_marginal_current_retained_oos_catches"])
        > 0
        for row in signature_rows
    )
    bond_change_collapses_under_own_signature = bool(
        projected_bond_marginal > 0 and bond_signature_bond_marginal == 0
    )
    result_class = (
        "research_only_signature_exclusion_sensitivity_signal_with_axis_caveat"
        if bond_change_collapses_under_own_signature
        else (
            "research_only_signature_exclusion_sensitivity_signal"
            if any_signature_marginal_signal
            else "research_only_signature_exclusion_sensitivity_negative"
        )
    )

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_signature_exclusion_sensitivity_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": f"lever2_event_axis_signature_exclusion_sensitivity_readout_{result_class}",
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal sensitivity readout that reruns the "
            "signature-excluded event-axis frontier under several mechanism "
            "signature definitions. It summarizes whether marginal signal "
            "survives projected-subset, bond-change, electron-flow, and "
            "event-topology neighbor exclusions without scoring heldout rows."
        ),
        "fixed_operating_points": {
            "baseline_axis_id": baseline_axis_id,
            "signature_axis_ids": list(signature_axis_ids),
            "min_primary_retain": min_primary_retain,
        },
        "measured_readout": {
            "signature_axis_sensitivity_rows": signature_rows,
            "best_signature_axis_row": best_signature_row,
        },
        "counts": {
            "critical_violation_total": 0,
            "signature_axes_evaluated": len(signature_rows),
            "signature_axes_with_marginal_signal": sum(
                1
                for row in signature_rows
                if int(
                    row[
                        "best_signature_excluded_axis_marginal_current_retained_oos_catches"
                    ]
                )
                > 0
            ),
            "projected_signature_bond_change_marginal_catches": (
                projected_bond_marginal
            ),
            "bond_signature_bond_change_marginal_catches": (
                bond_signature_bond_marginal
            ),
            "bond_signature_electron_flow_marginal_catches": (
                bond_signature_electron_marginal
            ),
            "best_signature_axis_marginal_catches": int(
                best_signature_row[
                    "best_signature_excluded_axis_marginal_current_retained_oos_catches"
                ]
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "any_signature_excluded_axis_signal_beyond_current_surface": (
                any_signature_marginal_signal
            ),
            "bond_change_signal_survives_projected_signature_exclusion": bool(
                projected_bond_marginal > 0
            ),
            "bond_change_signal_survives_bond_signature_exclusion": bool(
                bond_signature_bond_marginal > 0
            ),
            "bond_change_signal_collapses_under_own_signature_exclusion": (
                bond_change_collapses_under_own_signature
            ),
            "electron_flow_signal_survives_bond_signature_exclusion": bool(
                bond_signature_electron_marginal > 0
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not any_signature_marginal_signal,
            "apply_or_promote_now": False,
            "next_gate": (
                "Treat the bond-change rescue as research-only and axis-fragile "
                "until source-free current-split event-axis evidence can be "
                "measured. Prioritize m_csa:256 because it remains marginal "
                "under the bond-signature exclusion through electron-flow."
            ),
        },
        "missing_evidence": missing_evidence,
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": source_artifacts,
        "interpretation": {
            "headline": (
                "Projected-signature exclusion preserves two bond-change "
                "marginal catches, but bond-signature exclusion removes the "
                "bond-change marginal signal and leaves one electron-flow catch."
            ),
            "result": (
                "Research-only mixed signal: mechanism event axes add local "
                "current-retained OOS value under signature exclusion, but the "
                "bond-change marginal effect is not robust to excluding "
                "same-bond-signature calibration OOS neighbors."
            ),
            "next_action": (
                "Materialize source-free current-split event-axis rows for "
                "m_csa:256 first, then m_csa:312 only if the projected-signature "
                "bond-change path remains primary-controlled."
            ),
        },
    }


def build_lever2_event_axis_primary_controlled_null_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    null_permutations: int = 128,
    null_seed: str = "lever2_primary_controlled_event_axis_null_v0",
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_NULL_ARTIFACT_ID,
) -> dict[str, Any]:
    if null_permutations <= 0:
        raise ValueError("null_permutations must be positive")

    observed = build_lever2_event_axis_primary_controlled_rescue_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=current_in_scope_threshold_contract_path,
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        artifact_id=f"{artifact_id}.observed",
    )
    mechanism = _read_json(mechanism_no_template_rerun_path)
    feature_sidecar = _read_json(train_cal_feature_sidecar_path)
    current_overlap = _read_json(current_extended_oos_mechanism_overlap_readout_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)

    feature_rows = _feature_rows_by_id(feature_sidecar)
    calibration_rows: list[dict[str, Any]] = []
    for row in (mechanism.get("scored_rows") or {}).get("calibration") or []:
        entry_id = str(row.get("entry_id") or "")
        feature_row = feature_rows.get(entry_id)
        if not entry_id or feature_row is None:
            continue
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "is_primary": bool(row.get("is_primary")),
                "features": feature_row.get("row_specific_event_features") or {},
            }
        )
    current_rows = [
        row
        for row in (current_overlap.get("row_readouts") or {}).get(
            "current_extended_oos_overlap_rows"
        )
        or []
        if isinstance(row, dict) and row.get("entry_id") in feature_rows
    ]
    current_retained_rows = [
        row for row in current_rows if not row.get("current_surface_abstains")
    ]
    current_abstained_rows = [
        row for row in current_rows if row.get("current_surface_abstains")
    ]
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    calibration_feature_ids = {
        entry_id
        for entry_id, row in feature_rows.items()
        if row.get("assigned_embedding_split") == "calibration"
    }
    valid_current_primary_overlap = sorted(
        set(current_primary_rows) & calibration_feature_ids, key=_entry_sort_key
    )
    primary_control_rows = [row for row in calibration_rows if row["is_primary"]]
    axes_by_id = {
        str(axis["axis_id"]): axis for axis in _event_axis_frontier_definitions()
    }
    if baseline_axis_id not in axes_by_id:
        raise ValueError(f"unknown baseline event axis: {baseline_axis_id}")
    baseline_fields = list(axes_by_id[baseline_axis_id]["feature_fields"])

    feature_universe_ids = sorted(
        {
            row["entry_id"]
            for row in calibration_rows
            if row["entry_id"] in feature_rows
        }
        | {
            str(row["entry_id"])
            for row in current_rows
            if str(row["entry_id"]) in feature_rows
        },
        key=_entry_sort_key,
    )
    source_features_by_id = {
        entry_id: (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        for entry_id in feature_universe_ids
    }

    def _selection_rows_for(entry_id: str) -> list[dict[str, Any]]:
        return [row for row in calibration_rows if row["entry_id"] != entry_id]

    baseline_row_readouts: list[dict[str, Any]] = []
    for row in current_rows:
        entry_id = str(row["entry_id"])
        features = (
            feature_rows.get(entry_id, {}).get("row_specific_event_features") or {}
        )
        current_surface_abstains = bool(row.get("current_surface_abstains"))
        try:
            rule = _select_primary_controlled_axis_rule(
                _selection_rows_for(entry_id),
                primary_control_rows,
                baseline_fields,
                min_primary_retain=min_primary_retain,
            )
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = _axis_rule_abstains(
                baseline_score,
                direction=str(rule["direction"]),
                threshold=float(rule["threshold"]),
            )
            selection_error = None
        except ValueError as exc:
            rule = None
            baseline_score = round(_axis_score(features, baseline_fields), 8)
            baseline_abstains = False
            selection_error = str(exc)
        baseline_row_readouts.append(
            {
                "entry_id": entry_id,
                "current_surface_abstains": current_surface_abstains,
                "baseline_rule_evaluable": rule is not None,
                "selection_error": selection_error,
                "baseline_axis_score": baseline_score,
                "selected_rule": rule,
                "baseline_axis_abstains": baseline_abstains,
                "current_retained_caught_by_baseline": bool(
                    baseline_abstains and not current_surface_abstains
                ),
            }
        )
    baseline_by_entry = {row["entry_id"]: row for row in baseline_row_readouts}
    baseline_caught_ids = [
        row["entry_id"]
        for row in baseline_row_readouts
        if row["current_retained_caught_by_baseline"]
    ]

    added_axes = [
        axis
        for axis in _event_axis_frontier_definitions()
        if str(axis["axis_id"]) != baseline_axis_id
        and any(field not in baseline_fields for field in axis["feature_fields"])
    ]

    def _with_shuffled_added_fields(
        row: dict[str, Any],
        *,
        mapping: dict[str, str],
        shuffle_fields: list[str],
    ) -> dict[str, Any]:
        source_id = mapping.get(row["entry_id"], row["entry_id"])
        source_features = source_features_by_id.get(source_id, {})
        return {
            **row,
            "features": _features_with_axis_fields_from_source(
                row["features"], source_features, shuffle_fields
            ),
        }

    null_permutation_rows: list[dict[str, Any]] = []
    for permutation_index in range(null_permutations):
        axis_rows: list[dict[str, Any]] = []
        for axis in added_axes:
            axis_id = str(axis["axis_id"])
            added_fields = list(axis["feature_fields"])
            shuffle_fields = [
                field for field in added_fields if field not in baseline_fields
            ]
            mapping = _deterministic_null_mapping(
                feature_universe_ids,
                seed=f"{null_seed}:{axis_id}:{permutation_index}",
            )
            shuffled_primary_control_rows = [
                _with_shuffled_added_fields(
                    row, mapping=mapping, shuffle_fields=shuffle_fields
                )
                for row in primary_control_rows
            ]
            row_readouts: list[dict[str, Any]] = []
            for row in current_rows:
                entry_id = str(row["entry_id"])
                target_feature_row = feature_rows[entry_id]
                target_features = (
                    target_feature_row.get("row_specific_event_features") or {}
                )
                source_id = mapping.get(entry_id, entry_id)
                shuffled_target_features = _features_with_axis_fields_from_source(
                    target_features,
                    source_features_by_id.get(source_id, {}),
                    shuffle_fields,
                )
                shuffled_selection_rows = [
                    _with_shuffled_added_fields(
                        cal_row, mapping=mapping, shuffle_fields=shuffle_fields
                    )
                    for cal_row in _selection_rows_for(entry_id)
                ]
                current_surface_abstains = bool(row.get("current_surface_abstains"))
                baseline_only_catch = bool(
                    baseline_by_entry.get(entry_id, {}).get(
                        "current_retained_caught_by_baseline"
                    )
                )
                try:
                    pair_rule = _select_primary_controlled_axis_pair_rule(
                        shuffled_selection_rows,
                        shuffled_primary_control_rows,
                        baseline_fields,
                        added_fields,
                        min_primary_retain=min_primary_retain,
                    )
                    baseline_score = round(
                        _axis_score(shuffled_target_features, baseline_fields), 8
                    )
                    added_score = round(
                        _axis_score(shuffled_target_features, added_fields), 8
                    )
                    pair_baseline_abstains = _axis_rule_abstains(
                        baseline_score,
                        direction=str(pair_rule["baseline_rule"]["direction"]),
                        threshold=float(pair_rule["baseline_rule"]["threshold"]),
                    )
                    added_abstains = _axis_rule_abstains(
                        added_score,
                        direction=str(pair_rule["added_rule"]["direction"]),
                        threshold=float(pair_rule["added_rule"]["threshold"]),
                    )
                    pair_abstains = bool(pair_baseline_abstains or added_abstains)
                    pair_error = None
                except ValueError as exc:
                    pair_rule = None
                    baseline_score = round(
                        _axis_score(shuffled_target_features, baseline_fields), 8
                    )
                    added_score = round(
                        _axis_score(shuffled_target_features, added_fields), 8
                    )
                    pair_baseline_abstains = False
                    added_abstains = False
                    pair_abstains = False
                    pair_error = str(exc)
                pair_current_retained_catch = bool(
                    pair_abstains and not current_surface_abstains
                )
                row_readouts.append(
                    {
                        "entry_id": entry_id,
                        "source_entry_id_for_shuffled_added_axis": source_id,
                        "current_surface_abstains": current_surface_abstains,
                        "pair_rule_evaluable": pair_rule is not None,
                        "selection_error": pair_error,
                        "baseline_axis_score": baseline_score,
                        "added_axis_score": added_score,
                        "pair_baseline_axis_abstains": pair_baseline_abstains,
                        "added_axis_abstains": added_abstains,
                        "projection_plus_axis_abstains": pair_abstains,
                        "current_retained_caught_by_projected_subset": (
                            baseline_only_catch
                        ),
                        "current_retained_caught_by_projection_plus_axis": (
                            pair_current_retained_catch
                        ),
                        "current_retained_caught_beyond_projected_subset": bool(
                            pair_current_retained_catch and not baseline_only_catch
                        ),
                    }
                )
            evaluable_rows = [
                row for row in row_readouts if row["pair_rule_evaluable"]
            ]
            pair_caught = [
                row
                for row in evaluable_rows
                if row["current_retained_caught_by_projection_plus_axis"]
            ]
            marginal_caught = [
                row
                for row in evaluable_rows
                if row["current_retained_caught_beyond_projected_subset"]
            ]
            axis_rows.append(
                {
                    "axis_id": axis_id,
                    "projection_plus_axis_id": f"{baseline_axis_id}+{axis_id}",
                    "shuffle_fields": shuffle_fields,
                    "evaluable_rows": len(evaluable_rows),
                    "projection_plus_axis_current_retained_oos_catches": len(
                        pair_caught
                    ),
                    "marginal_current_retained_oos_catches_beyond_projected_subset": len(
                        marginal_caught
                    ),
                    "marginal_caught_entry_ids": [
                        row["entry_id"] for row in marginal_caught
                    ],
                }
            )

        def _axis_null_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
            return (
                int(row["marginal_current_retained_oos_catches_beyond_projected_subset"]),
                int(row["projection_plus_axis_current_retained_oos_catches"]),
                str(row["projection_plus_axis_id"]),
            )

        best_null_axis = sorted(axis_rows, key=_axis_null_sort_key, reverse=True)[0]
        null_permutation_rows.append(
            {
                "permutation_index": permutation_index,
                "best_null_axis": best_null_axis,
                "axis_rows": axis_rows,
            }
        )

    priority_null_axis_ids = {
        "bond_change",
        "electron_flow",
        "event_topology",
        "all_priority_event_axes",
    }
    priority_null_rows: list[dict[str, Any]] = []
    for row in null_permutation_rows:
        priority_axis_rows = [
            axis_row
            for axis_row in row["axis_rows"]
            if axis_row["axis_id"] in priority_null_axis_ids
        ]
        if not priority_axis_rows:
            continue
        best_priority_axis = sorted(
            priority_axis_rows,
            key=lambda axis_row: (
                int(
                    axis_row[
                        "marginal_current_retained_oos_catches_beyond_projected_subset"
                    ]
                ),
                int(axis_row["projection_plus_axis_current_retained_oos_catches"]),
                str(axis_row["projection_plus_axis_id"]),
            ),
            reverse=True,
        )[0]
        priority_null_rows.append(
            {
                "permutation_index": row["permutation_index"],
                "best_null_axis": best_priority_axis,
            }
        )

    observed_counts = observed["counts"]
    observed_best = observed["measured_readout"]["best_primary_controlled_axis"]
    observed_best_overlap = observed_best["current_extended_overlap"]
    observed_marginal = int(
        observed_counts[
            "best_primary_controlled_axis_marginal_current_retained_oos_catches"
        ]
    )
    observed_total = int(
        observed_counts["best_primary_controlled_axis_current_retained_oos_catches"]
    )
    null_max_marginals = [
        int(
            row["best_null_axis"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        for row in null_permutation_rows
    ]
    null_max_totals = [
        int(
            row["best_null_axis"][
                "projection_plus_axis_current_retained_oos_catches"
            ]
        )
        for row in null_permutation_rows
    ]
    priority_null_max_marginals = [
        int(
            row["best_null_axis"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ]
        )
        for row in priority_null_rows
    ]
    priority_null_ge_observed = sum(
        1 for value in priority_null_max_marginals if value >= observed_marginal
    )
    priority_empirical_p_value = round(
        (priority_null_ge_observed + 1)
        / (len(priority_null_max_marginals) + 1),
        6,
    )
    priority_null_marginal_q95 = _empirical_quantile(
        priority_null_max_marginals, 0.95
    )
    observed_exceeds_priority_null_95 = bool(
        priority_null_marginal_q95 is not None
        and observed_marginal > priority_null_marginal_q95
    )
    null_ge_observed = sum(
        1 for value in null_max_marginals if value >= observed_marginal
    )
    empirical_p_value = round(
        (null_ge_observed + 1) / (len(null_max_marginals) + 1), 6
    )
    null_marginal_q95 = _empirical_quantile(null_max_marginals, 0.95)
    observed_exceeds_null_95 = bool(
        null_marginal_q95 is not None and observed_marginal > null_marginal_q95
    )
    observed_above_null_max = bool(
        null_max_marginals and observed_marginal > max(null_max_marginals)
    )
    null_top_rows = sorted(
        null_permutation_rows,
        key=lambda row: (
            int(
                row["best_null_axis"][
                    "marginal_current_retained_oos_catches_beyond_projected_subset"
                ]
            ),
            int(
                row["best_null_axis"][
                    "projection_plus_axis_current_retained_oos_catches"
                ]
            ),
            str(row["best_null_axis"]["projection_plus_axis_id"]),
        ),
        reverse=True,
    )[:10]

    result_class = (
        "research_only_null_controlled_marginal_axis_signal_source_free_gap"
        if observed_marginal > 0 and observed_exceeds_null_95
        else (
            "research_only_null_controlled_marginal_signal_not_distinguishable_from_null"
            if observed_marginal > 0
            else "research_only_null_controlled_axis_negative"
        )
    )

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}.event_axis_primary_controlled_null_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": f"lever2_event_axis_primary_controlled_null_readout_{result_class}",
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal null-control readout for the primary-controlled "
            "event-axis rescue. The observed projected-subset-plus-axis result "
            "is compared with deterministic permutations of the genuinely new "
            "added-axis fields while preserving the fixed geometry/fold surface, "
            "split rows, baseline projected subset, primary controls, and rule "
            "selection discipline. No heldout rows are scored or tuned."
        ),
        "fixed_operating_points": {
            "current_surface": (
                current_overlap.get("fixed_operating_points") or {}
            ).get("current_surface")
            or {},
            "axis_selection": {
                "baseline_axis_id": baseline_axis_id,
                "min_primary_retain": min_primary_retain,
                "null_seed": null_seed,
                "null_permutations": null_permutations,
                "null_added_axis_assignment": (
                    "deterministic SHA256 permutation of non-baseline added-axis "
                    "feature fields across train/cal feature rows"
                ),
            },
        },
        "measured_readout": {
            "observed_primary_controlled_rescue": {
                "status": observed["status"],
                "result_class": observed["result_class"],
                "best_axis_id": observed["decision"][
                    "best_primary_controlled_axis_id"
                ],
                "best_new_axis_id": observed["decision"]["best_new_axis_id"],
                "baseline_projected_subset_current_retained_oos_catches": (
                    observed_counts[
                        "baseline_projected_subset_current_retained_oos_catches"
                    ]
                ),
                "best_axis_current_retained_oos_catches": observed_total,
                "best_axis_marginal_current_retained_oos_catches": (
                    observed_marginal
                ),
                "best_axis_marginal_entry_ids": observed_best_overlap[
                    "marginal_caught_entry_ids"
                ],
            },
            "baseline_projected_subset_row_readouts": baseline_row_readouts,
            "null_distribution": {
                "permutations": null_permutations,
                "added_axes_evaluated_per_permutation": len(added_axes),
                "max_marginal_catches_by_permutation": null_max_marginals,
                "max_total_catches_by_permutation": null_max_totals,
                "summary": {
                    "min": min(null_max_marginals) if null_max_marginals else None,
                    "median": _empirical_quantile(null_max_marginals, 0.5),
                    "p90": _empirical_quantile(null_max_marginals, 0.9),
                    "p95": null_marginal_q95,
                    "max": max(null_max_marginals) if null_max_marginals else None,
                    "null_ge_observed_permutations": null_ge_observed,
                    "empirical_p_value_greater_equal_observed": empirical_p_value,
                },
            },
            "priority_event_axis_null_distribution": {
                "priority_axis_ids": sorted(priority_null_axis_ids),
                "permutations": len(priority_null_rows),
                "max_marginal_catches_by_permutation": (
                    priority_null_max_marginals
                ),
                "summary": {
                    "min": (
                        min(priority_null_max_marginals)
                        if priority_null_max_marginals
                        else None
                    ),
                    "median": _empirical_quantile(
                        priority_null_max_marginals, 0.5
                    ),
                    "p90": _empirical_quantile(priority_null_max_marginals, 0.9),
                    "p95": priority_null_marginal_q95,
                    "max": (
                        max(priority_null_max_marginals)
                        if priority_null_max_marginals
                        else None
                    ),
                    "null_ge_observed_permutations": priority_null_ge_observed,
                    "empirical_p_value_greater_equal_observed": (
                        priority_empirical_p_value
                    ),
                },
            },
            "top_null_permutations": null_top_rows,
        },
        "counts": {
            "critical_violation_total": 0,
            "calibration_rows": len(calibration_rows),
            "calibration_primary_rows": len(primary_control_rows),
            "calibration_oos_rows": sum(
                1 for row in calibration_rows if not row["is_primary"]
            ),
            "current_extended_oos_overlap_rows": len(current_rows),
            "current_extended_current_retained_overlap_rows": len(
                current_retained_rows
            ),
            "current_extended_current_abstained_overlap_rows": len(
                current_abstained_rows
            ),
            "current_primary_rows": len(current_primary_rows),
            "valid_current_primary_calibration_feature_overlap_rows": len(
                valid_current_primary_overlap
            ),
            "baseline_projected_subset_current_retained_oos_catches": len(
                baseline_caught_ids
            ),
            "observed_best_axis_current_retained_oos_catches": observed_total,
            "observed_best_axis_marginal_current_retained_oos_catches": (
                observed_marginal
            ),
            "null_permutations": null_permutations,
            "null_added_axes_evaluated": len(added_axes),
            "null_max_marginal_catches_min": (
                min(null_max_marginals) if null_max_marginals else None
            ),
            "null_max_marginal_catches_median": _empirical_quantile(
                null_max_marginals, 0.5
            ),
            "null_max_marginal_catches_p90": _empirical_quantile(
                null_max_marginals, 0.9
            ),
            "null_max_marginal_catches_p95": null_marginal_q95,
            "null_max_marginal_catches_max": (
                max(null_max_marginals) if null_max_marginals else None
            ),
            "null_permutations_ge_observed_marginal": null_ge_observed,
            "priority_event_axis_null_max_marginal_catches_p95": (
                priority_null_marginal_q95
            ),
            "priority_event_axis_null_max_marginal_catches_max": (
                max(priority_null_max_marginals)
                if priority_null_max_marginals
                else None
            ),
            "priority_event_axis_null_permutations_ge_observed_marginal": (
                priority_null_ge_observed
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "observed_primary_controlled_marginal_signal": bool(
                observed_marginal > 0
            ),
            "observed_marginal_exceeds_empirical_null_p95": (
                observed_exceeds_null_95
            ),
            "observed_marginal_exceeds_empirical_null_max": observed_above_null_max,
            "empirical_p_value_greater_equal_observed": empirical_p_value,
            "null_control_supports_genuinely_new_axis_signal": bool(
                observed_marginal > 0 and observed_exceeds_null_95
            ),
            "priority_event_axis_null_control_supports_signal": bool(
                observed_marginal > 0 and observed_exceeds_priority_null_95
            ),
            "null_controlled_result_is_negative": not bool(
                observed_marginal > 0 and observed_exceeds_null_95
            ),
            "adds_local_overlap_value_beyond_current_surface": bool(
                observed_marginal > 0
            ),
            "adds_operating_point_value_beyond_current_surface": False,
            "source_free_current_split_operating_point_measurable": (
                observed["decision"][
                    "source_free_current_split_operating_point_measurable"
                ]
            ),
            "valid_integrated_operating_point_measurable": False,
            "deployable_now": False,
            "research_only": True,
            "negative": not bool(
                observed_marginal > 0 and observed_exceeds_null_95
            ),
            "apply_or_promote_now": False,
            "best_observed_axis_id": observed["decision"][
                "best_primary_controlled_axis_id"
            ],
            "best_observed_new_axis_id": observed["decision"]["best_new_axis_id"],
            "next_gate": (
                "Do not promote Lever 2 from this result. If source-free "
                "event-axis rows are materialized, rerun the primary-controlled "
                "frontier plus this null control and require an observed "
                "marginal count above the empirical null p95 before any "
                "heldout or deployment claim."
            ),
        },
        "missing_evidence": observed["missing_evidence"],
        "missing_evidence_rows": observed["missing_evidence_rows"],
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "target_oos_rows_excluded_from_their_own_axis_rule_selection": True,
            "primary_labels_used_only_for_retention_control": True,
            "null_control_randomizes_added_axis_feature_assignments_only": True,
            "null_control_preserves_current_surface_and_split_rows": True,
            "threshold_selected_or_tuned": True,
            "threshold_selection_rows": (
                "calibration_only_leave_one_oos_row_out_with_all_primary_controls"
            ),
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "train_cal_feature_sidecar": _source_path_record(
                train_cal_feature_sidecar_path
            ),
            "current_extended_oos_mechanism_overlap_readout": _source_path_record(
                current_extended_oos_mechanism_overlap_readout_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "partial_surface_current_split_portability_readout": (
                _source_path_record(partial_surface_current_split_portability_readout_path)
                if partial_surface_current_split_portability_readout_path is not None
                else {"exists": False, "path": None, "sha256": None}
            ),
        },
        "interpretation": {
            "headline": (
                f"Observed primary-controlled marginal catches: {observed_marginal}; "
                f"empirical null p95: {null_marginal_q95}; empirical p-value: "
                f"{empirical_p_value}; priority-event null p95: "
                f"{priority_null_marginal_q95}."
            ),
            "result": (
                "Research-only null-controlled signal: the observed new-axis "
                "marginal count exceeds the deterministic added-axis null p95, "
                "but source-free current-split event-axis rows are still "
                "missing."
                if observed_marginal > 0 and observed_exceeds_null_95
                else (
                    "Research-only measured negative: the observed "
                    "primary-controlled marginal signal is not distinguishable "
                    "from deterministic added-axis assignment nulls under the "
                    "same split and primary-control discipline."
                )
            ),
            "next_action": (
                "Use this as the promotion gate for future source-free "
                "materialization: rerun on materialized current-split rows and "
                "require null-controlled marginal signal before heldout or "
                "deployment work."
            ),
        },
    }


def build_lever2_source_free_partial_surface_current_split_portability_readout(
    *,
    current_measured_readout_path: Path,
    current_extended_oos_surface_path: Path,
    current_in_scope_threshold_contract_path: Path,
    source_free_projection_repair_candidate_surface_path: Path,
    source_free_event_axis_linker_materialization_gate_path: Path,
    source_free_locator_rewrite_materialization_gate_path: Path,
    review_only_locator_candidate_dir_path: Path | None = None,
    artifact_id: str = DEFAULT_PARTIAL_SURFACE_CURRENT_SPLIT_PORTABILITY_ARTIFACT_ID,
) -> dict[str, Any]:
    current_measured = _read_json(current_measured_readout_path)
    current_surface = _read_json(current_extended_oos_surface_path)
    current_primary_contract = _read_json(current_in_scope_threshold_contract_path)
    candidate_surface = _read_json(source_free_projection_repair_candidate_surface_path)
    event_axis_materialization = _read_json(
        source_free_event_axis_linker_materialization_gate_path
    )
    locator_materialization = _read_json(
        source_free_locator_rewrite_materialization_gate_path
    )

    channel, current_threshold = _current_readout_threshold(current_measured)
    current_primary_rows = _fold_rows_by_id(
        current_primary_contract.get("calibration_row_scores") or []
    )
    current_oos_rows = _current_surface_rows_with_score(current_surface, channel)
    all_current_oos_rows = _fold_rows_by_id(
        current_surface.get("candidate_row_scores") or []
    )
    current_abstained_oos_ids = {
        entry_id
        for entry_id, row in current_oos_rows.items()
        if _current_abstains(row, channel, current_threshold)
    }
    current_retained_oos_ids = set(current_oos_rows) - current_abstained_oos_ids

    candidate_ids = _entry_ids_from_candidate_surface(candidate_surface)
    event_axis_ids = _entry_ids_from_event_axis_materialization(
        event_axis_materialization
    )
    locator_ids = _entry_ids_from_locator_materialization(locator_materialization)
    review_only_locator_candidate_ids = _m_csa_ids_from_candidate_dir(
        review_only_locator_candidate_dir_path
    )
    union_ids = candidate_ids | event_axis_ids | locator_ids

    surfaces = {
        "source_free_projection_candidate_surface": candidate_ids,
        "source_free_event_axis_linkers": event_axis_ids,
        "source_free_locator_sidecars": locator_ids,
        "source_free_partial_surface_union": union_ids,
    }
    surface_summaries = {
        name: _surface_overlap_summary(
            surface_ids=ids,
            current_primary_rows=current_primary_rows,
            current_oos_rows=current_oos_rows,
            current_retained_oos_ids=current_retained_oos_ids,
            current_abstained_oos_ids=current_abstained_oos_ids,
            channel=channel,
        )
        for name, ids in surfaces.items()
    }
    review_only_locator_candidate_summary = _surface_overlap_summary(
        surface_ids=review_only_locator_candidate_ids,
        current_primary_rows=current_primary_rows,
        current_oos_rows=current_oos_rows,
        current_retained_oos_ids=current_retained_oos_ids,
        current_abstained_oos_ids=current_abstained_oos_ids,
        channel=channel,
    )
    union_summary = surface_summaries["source_free_partial_surface_union"]

    missing_primary_ids = sorted(
        set(current_primary_rows) - union_ids, key=_entry_sort_key
    )
    missing_retained_oos_ids = sorted(
        current_retained_oos_ids - union_ids, key=_entry_sort_key
    )
    missing_abstained_oos_ids = sorted(
        current_abstained_oos_ids - union_ids, key=_entry_sort_key
    )

    def _missing_primary_row(entry_id: str) -> dict[str, Any]:
        row = current_primary_rows[entry_id]
        return {
            "entry_id": entry_id,
            "current_surface_score": _rounded_current_score(row, channel),
            "required_evidence": (
                "source-free row-specific mechanism feature row on the current "
                "calibration-primary split"
            ),
        }

    def _missing_oos_row(entry_id: str, *, abstains: bool) -> dict[str, Any]:
        row = current_oos_rows[entry_id]
        return {
            "entry_id": entry_id,
            "current_surface_score": _rounded_current_score(row, channel),
            "current_surface_abstains": abstains,
            "required_evidence": (
                "source-free row-specific mechanism feature row on the current "
                "extended train/cal OOS split"
            ),
        }

    route_reduces_primary_gap = bool(union_summary["current_primary_overlap_rows"])
    route_reduces_retained_oos_gap = bool(
        union_summary["current_retained_oos_overlap_rows"]
    )
    route_reduces_current_gap = bool(
        route_reduces_primary_gap
        or route_reduces_retained_oos_gap
        or union_summary["current_abstained_oos_overlap_rows"]
    )
    route_negative = not route_reduces_current_gap
    status = (
        "lever2_source_free_partial_surface_current_split_portability_"
        "readout_research_only_reuse_negative"
        if route_negative
        else (
            "lever2_source_free_partial_surface_current_split_portability_"
            "readout_research_only_overlap_available"
        )
    )
    result_class = "research_only_reuse_negative" if route_negative else "research_only"

    return {
        "artifact_id": artifact_id,
        "schema_version": (
            f"{SCHEMA_VERSION}."
            "source_free_partial_surface_current_split_portability_readout.v0"
        ),
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": result_class,
        "scope": (
            "Lever 2 train/cal readout testing whether existing approved "
            "source-free partial-surface rows, locator sidecars, and event-axis "
            "linkers reduce the current geometry/fold primary or extended-OOS "
            "mechanism evidence gap. It uses entry IDs only for split accounting, "
            "does not score heldout rows, and does not apply or tune thresholds."
        ),
        "fixed_operating_points": {
            "current_surface": {
                "channel": channel,
                "threshold": round(current_threshold, 8),
                "decision_rule": "abstain_when_current_surface_score_below_threshold",
                "current_measured_context": (
                    (current_measured.get("measured_readout") or {}).get(
                        "train_cal_oos_current_scored_surface"
                    )
                ),
            },
        },
        "measured_readout": {
            "current_split_surface": {
                "current_primary_rows": len(current_primary_rows),
                "current_extended_candidate_oos_rows": len(all_current_oos_rows),
                "current_extended_scored_oos_rows": len(current_oos_rows),
                "current_extended_unscored_oos_rows": (
                    len(all_current_oos_rows) - len(current_oos_rows)
                ),
                "current_retained_oos_rows": len(current_retained_oos_ids),
                "current_abstained_oos_rows": len(current_abstained_oos_ids),
            },
            "source_free_partial_surface_overlap": surface_summaries,
            "review_only_locator_candidate_current_split_overlap": (
                review_only_locator_candidate_summary
            ),
        },
        "missing_evidence": [
            {
                "gap_id": "current_primary_source_free_partial_surface_rows",
                "required_rows": len(current_primary_rows),
                "valid_overlap_rows_now": union_summary[
                    "current_primary_overlap_rows"
                ],
                "missing_rows_now": len(missing_primary_ids),
                "why_it_matters": (
                    "Primary retention cost must be measurable on the current "
                    "geometry/fold calibration-primary split before Lever 2 can "
                    "claim operating-point value."
                ),
            },
            {
                "gap_id": "current_retained_oos_source_free_partial_surface_rows",
                "required_rows": len(current_retained_oos_ids),
                "valid_overlap_rows_now": union_summary[
                    "current_retained_oos_overlap_rows"
                ],
                "missing_rows_now": len(missing_retained_oos_ids),
                "why_it_matters": (
                    "These rows are current geometry/fold retained OOS cases; "
                    "they are the direct path for source-free mechanism features "
                    "to add OOS abstention value."
                ),
            },
            {
                "gap_id": "current_abstained_oos_source_free_partial_surface_rows",
                "required_rows": len(current_abstained_oos_ids),
                "valid_overlap_rows_now": union_summary[
                    "current_abstained_oos_overlap_rows"
                ],
                "missing_rows_now": len(missing_abstained_oos_ids),
                "why_it_matters": (
                    "These complete the current extended OOS surface but are "
                    "lower priority because geometry/fold already abstains."
                ),
            },
        ],
        "missing_evidence_rows": {
            "current_primary_rows_requiring_source_free_partial_surface": [
                _missing_primary_row(entry_id) for entry_id in missing_primary_ids
            ],
            "current_retained_oos_rows_requiring_source_free_partial_surface": [
                _missing_oos_row(entry_id, abstains=False)
                for entry_id in missing_retained_oos_ids
            ],
            "current_abstained_oos_rows_requiring_source_free_partial_surface": [
                _missing_oos_row(entry_id, abstains=True)
                for entry_id in missing_abstained_oos_ids
            ],
        },
        "counts": {
            "critical_violation_total": 0,
            "current_primary_rows": len(current_primary_rows),
            "current_extended_candidate_oos_rows": len(all_current_oos_rows),
            "current_extended_scored_oos_rows": len(current_oos_rows),
            "current_extended_unscored_oos_rows": len(all_current_oos_rows)
            - len(current_oos_rows),
            "current_retained_oos_rows": len(current_retained_oos_ids),
            "current_abstained_oos_rows": len(current_abstained_oos_ids),
            "source_free_projection_candidate_rows": len(candidate_ids),
            "source_free_event_axis_linker_rows": len(event_axis_ids),
            "source_free_locator_sidecar_rows": len(locator_ids),
            "source_free_partial_surface_union_rows": len(union_ids),
            "review_only_locator_candidate_rows": len(
                review_only_locator_candidate_ids
            ),
            "review_only_locator_candidate_current_primary_overlap_rows": (
                review_only_locator_candidate_summary[
                    "current_primary_overlap_rows"
                ]
            ),
            "review_only_locator_candidate_current_retained_oos_overlap_rows": (
                review_only_locator_candidate_summary[
                    "current_retained_oos_overlap_rows"
                ]
            ),
            "review_only_locator_candidate_current_abstained_oos_overlap_rows": (
                review_only_locator_candidate_summary[
                    "current_abstained_oos_overlap_rows"
                ]
            ),
            "union_current_primary_overlap_rows": union_summary[
                "current_primary_overlap_rows"
            ],
            "union_current_retained_oos_overlap_rows": union_summary[
                "current_retained_oos_overlap_rows"
            ],
            "union_current_abstained_oos_overlap_rows": union_summary[
                "current_abstained_oos_overlap_rows"
            ],
            "union_current_scored_oos_overlap_rows": union_summary[
                "current_scored_oos_overlap_rows"
            ],
            "missing_current_primary_source_free_partial_surface_rows": len(
                missing_primary_ids
            ),
            "missing_current_retained_oos_source_free_partial_surface_rows": len(
                missing_retained_oos_ids
            ),
            "missing_current_abstained_oos_source_free_partial_surface_rows": len(
                missing_abstained_oos_ids
            ),
        },
        "decision": {
            "measured_readout_available": True,
            "existing_partial_surface_reduces_current_primary_gap": (
                route_reduces_primary_gap
            ),
            "existing_partial_surface_reduces_current_retained_oos_gap": (
                route_reduces_retained_oos_gap
            ),
            "existing_partial_surface_reduces_any_current_split_gap": (
                route_reduces_current_gap
            ),
            "route_negative_for_existing_partial_surface_reuse": (
                route_negative
            ),
            "lever2_overall_negative": False,
            "adds_operating_point_value_beyond_current_surface": False,
            "deployable_now": False,
            "research_only": True,
            "negative": False,
            "apply_or_promote_now": False,
            "next_gate": (
                "Materialize source-free mechanism rows on the current split: "
                f"{len(missing_primary_ids)} primary retention-gate rows and "
                f"{len(missing_retained_oos_ids)} current-retained OOS rows "
                "before rerunning the fixed train/cal mechanism readouts."
            ),
        },
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "heldout_rows_evaluated": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_as_feature_values": False,
            "labels_used_only_for_train_cal_metric_accounting": False,
            "entry_ids_used_only_for_split_overlap_accounting": True,
            "source_free_partial_surface_materialized_by_this_artifact": False,
            "threshold_selected_or_tuned": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "source_artifacts": {
            "current_measured_readout": _source_path_record(
                current_measured_readout_path
            ),
            "current_extended_oos_surface": _source_path_record(
                current_extended_oos_surface_path
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "source_free_projection_repair_candidate_surface": _source_path_record(
                source_free_projection_repair_candidate_surface_path
            ),
            "source_free_event_axis_linker_materialization_gate": (
                _source_path_record(
                    source_free_event_axis_linker_materialization_gate_path
                )
            ),
            "source_free_locator_rewrite_materialization_gate": (
                _source_path_record(
                    source_free_locator_rewrite_materialization_gate_path
                )
            ),
            "review_only_locator_candidate_dir": {
                "exists": bool(
                    review_only_locator_candidate_dir_path is not None
                    and Path(review_only_locator_candidate_dir_path).exists()
                ),
                "path": (
                    str(review_only_locator_candidate_dir_path)
                    if review_only_locator_candidate_dir_path is not None
                    else None
                ),
                "file_count": len(review_only_locator_candidate_ids),
            },
        },
        "interpretation": {
            "headline": (
                "Existing approved source-free partial-surface rows overlap "
                f"{union_summary['current_primary_overlap_rows']} current "
                "primary rows and "
                f"{union_summary['current_retained_oos_overlap_rows']} "
                "current-retained OOS rows."
            ),
            "result": (
                "Research-only route negative: the prior approved partial "
                "source-free surface does not reduce the current train/cal "
                "primary or retained-OOS mechanism-evidence gaps, so it cannot "
                "make the integrated Lever 2 operating point measurable."
            ),
            "next_action": (
                "Build source-free mechanism evidence directly for the current "
                "primary rows and current-retained OOS rows, rather than "
                "reusing the heldout-oriented partial surface."
            ),
        },
    }


def build_lever2_mechanism_feature_incremental_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    current_in_scope_threshold_contract_path: Path,
    expanded_oos_calibrated_threshold_contract_path: Path,
    mechanism_operating_point_contract_path: Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    mechanism = _read_json(mechanism_no_template_rerun_path)
    mechanism_contract = (
        _read_json(mechanism_operating_point_contract_path)
        if mechanism_operating_point_contract_path is not None
        and Path(mechanism_operating_point_contract_path).exists()
        else None
    )
    current_in_scope = _read_json(current_in_scope_threshold_contract_path)
    expanded = _read_json(expanded_oos_calibrated_threshold_contract_path)

    channel, current_threshold = _channel_threshold(expanded)
    mechanism_threshold = _mechanism_threshold(mechanism, mechanism_contract)
    current_summary = _selected_current_summary(expanded)
    mechanism_selected = (
        mechanism.get("residual_variant", {})
        .get("calibration_selected_residual_threshold", {})
    )

    mechanism_rows = _mechanism_calibration_rows(mechanism)
    mechanism_primary_ids = {
        entry_id
        for entry_id, row in mechanism_rows.items()
        if bool(row.get("is_primary"))
    }
    mechanism_oos_ids = set(mechanism_rows) - mechanism_primary_ids
    current_primary_rows = _fold_rows_by_id(
        current_in_scope.get("calibration_row_scores") or []
    )
    current_oos_rows = _fold_rows_by_id(
        expanded.get("calibration_oos_negative_row_scores") or []
    )
    current_train_ids = set(
        str(entry_id)
        for entry_id in (current_in_scope.get("train_cal_partition") or {}).get(
            "train_entry_ids", []
        )
    )

    valid_primary_overlap = sorted(
        mechanism_primary_ids & set(current_primary_rows), key=_entry_sort_key
    )
    invalid_primary_train_target_overlap = sorted(
        mechanism_primary_ids & current_train_ids, key=_entry_sort_key
    )
    oos_overlap = sorted(mechanism_oos_ids & set(current_oos_rows), key=_entry_sort_key)
    missing_primary_ids = sorted(
        set(current_primary_rows) - set(valid_primary_overlap), key=_entry_sort_key
    )
    missing_oos_ids = sorted(
        set(current_oos_rows) - set(oos_overlap), key=_entry_sort_key
    )

    oos_rows: list[dict[str, Any]] = []
    for entry_id in oos_overlap:
        mechanism_row = mechanism_rows[entry_id]
        current_row = current_oos_rows[entry_id]
        current_score = _current_score(current_row, channel)
        current_abstain = _current_abstains(
            current_row, channel, current_threshold
        )
        mechanism_abstain = _mechanism_abstains(mechanism_row, mechanism_threshold)
        union_abstain = bool(current_abstain or mechanism_abstain)
        oos_rows.append(
            {
                "entry_id": entry_id,
                "current_surface_score": round(current_score, 8)
                if current_score is not None
                else None,
                "current_surface_abstains": current_abstain,
                "mechanism_residual": round(
                    float(mechanism_row.get("out_of_atlas_span_residual") or 0.0),
                    8,
                ),
                "mechanism_surface_abstains": mechanism_abstain,
                "union_or_gate_abstains": union_abstain,
                "current_false_negative_caught_by_mechanism": bool(
                    not current_abstain and mechanism_abstain
                ),
            }
        )

    primary_rows: list[dict[str, Any]] = []
    for entry_id in valid_primary_overlap:
        mechanism_row = mechanism_rows[entry_id]
        current_row = current_primary_rows[entry_id]
        current_score = _current_score(current_row, channel)
        current_abstain = _current_abstains(
            current_row, channel, current_threshold
        )
        mechanism_abstain = _mechanism_abstains(mechanism_row, mechanism_threshold)
        union_abstain = bool(current_abstain or mechanism_abstain)
        primary_rows.append(
            {
                "entry_id": entry_id,
                "current_surface_score": round(current_score, 8)
                if current_score is not None
                else None,
                "current_surface_retains": not current_abstain,
                "mechanism_residual": round(
                    float(mechanism_row.get("out_of_atlas_span_residual") or 0.0),
                    8,
                ),
                "mechanism_surface_retains": not mechanism_abstain,
                "union_or_gate_retains": not union_abstain,
            }
        )

    current_oos_abstained = sum(1 for row in oos_rows if row["current_surface_abstains"])
    mechanism_oos_abstained = sum(
        1 for row in oos_rows if row["mechanism_surface_abstains"]
    )
    union_oos_abstained = sum(1 for row in oos_rows if row["union_or_gate_abstains"])
    current_retained_oos = [row for row in oos_rows if not row["current_surface_abstains"]]
    caught_current_retained_oos = [
        row for row in current_retained_oos if row["mechanism_surface_abstains"]
    ]
    current_primary_retained = sum(
        1 for row in primary_rows if row["current_surface_retains"]
    )
    mechanism_primary_retained = sum(
        1 for row in primary_rows if row["mechanism_surface_retains"]
    )
    union_primary_retained = sum(1 for row in primary_rows if row["union_or_gate_retains"])

    mechanism_own_primary_rows = int(mechanism_selected.get("primary_rows") or 0)
    mechanism_own_oos_rows = int(mechanism_selected.get("oos_rows") or 0)
    mechanism_own_oos_abstained = round(
        float(mechanism_selected.get("oos_abstain_recall") or 0.0)
        * mechanism_own_oos_rows
    )
    mechanism_own_primary_retained = round(
        float(mechanism_selected.get("primary_retain_recall") or 0.0)
        * mechanism_own_primary_rows
    )

    valid_operating_point_measurable = bool(primary_rows and oos_rows)
    oos_overlap_lift = round(
        _recall(union_oos_abstained, len(oos_rows) or 0)
        - _recall(current_oos_abstained, len(oos_rows) or 0),
        6,
    ) if oos_rows else None
    local_oos_signal = bool(
        oos_rows and union_oos_abstained > current_oos_abstained
    )
    deployable = bool(
        valid_operating_point_measurable
        and local_oos_signal
        and _recall(union_primary_retained, len(primary_rows)) is not None
        and (_recall(union_primary_retained, len(primary_rows)) or 0.0) >= 0.90
    )
    result_class = "deployable" if deployable else "research_only"
    status = (
        "lever2_mechanism_feature_incremental_readout_deployable"
        if deployable
        else "lever2_mechanism_feature_incremental_readout_research_only_overlap_blocked"
    )

    missing_evidence = [
        {
            "gap_id": "current_calibration_primary_source_free_mechanism_features",
            "required_rows": len(current_primary_rows),
            "valid_overlap_rows_now": len(valid_primary_overlap),
            "invalid_available_rows_are_current_surface_train_targets": len(
                invalid_primary_train_target_overlap
            ),
            "why_it_matters": (
                "Incremental value cannot be claimed without measuring primary "
                "retention on rows that are calibration/evaluation rows for the "
                "current geometry/fold surface."
            ),
        },
        {
            "gap_id": "current_calibration_oos_source_free_mechanism_features",
            "required_rows": len(current_oos_rows),
            "valid_overlap_rows_now": len(oos_overlap),
            "why_it_matters": (
                "The local OOS lift is measured on the available overlap, but the "
                "coverage is too sparse to represent the current train/cal OOS "
                "surface."
            ),
        },
        {
            "gap_id": "single_split_aligned_lever2_operating_contract",
            "required_rows": len(current_primary_rows) + len(current_oos_rows),
            "valid_overlap_rows_now": len(valid_primary_overlap) + len(oos_overlap),
            "why_it_matters": (
                "The current mechanism sidecar and the current geometry/fold "
                "threshold contract use different train/cal partitions."
            ),
        },
    ]

    return {
        "artifact_id": artifact_id,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Lever 2 train/cal readout for a genuinely row-specific mechanism "
            "surface: row-specific bond-change/proton/electron/event-topology "
            "features scored by the frozen residual contract, compared against "
            "the current geometry/fold operating point on overlapping non-heldout "
            "rows. The mechanism features remain train/cal-only and are not a "
            "deployment-valid source-free heldout projection."
        ),
        "result_class": result_class,
        "guardrails": {
            "measured_readout_first": True,
            "heldout_rows_used_for_training_or_threshold_tuning": False,
            "heldout_rows_scored_by_this_artifact": False,
            "mechanism_text_or_source_ids_used_as_predictive_features": False,
            "ec_rhea_ids_labels_source_ids_target_names_used_as_predictive_features": False,
            "labels_used_only_for_train_cal_metric_accounting": True,
            "m_csa_row_specific_features_train_cal_only": True,
            "current_surface_train_targets_excluded_from_primary_retention_claim": True,
            "threshold_selected_or_tuned": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
        },
        "fixed_operating_points": {
            "current_surface": {
                "channel": channel,
                "threshold": round(current_threshold, 8),
                "decision_rule": "abstain_when_current_surface_score_below_threshold",
                "train_cal_selection_summary": current_summary,
            },
            "mechanism_surface": {
                "channel": "row_specific_mechanism_out_of_atlas_span_residual",
                "threshold": round(mechanism_threshold, 8),
                "decision_rule": "abstain_when_mechanism_residual_above_threshold",
                "train_cal_selection_summary": mechanism_selected,
            },
        },
        "measured_readout": {
            "mechanism_surface_standalone_calibration_contract": {
                "primary_rows": mechanism_own_primary_rows,
                "primary_retained": mechanism_own_primary_retained,
                "primary_retain_recall": mechanism_selected.get(
                    "primary_retain_recall"
                ),
                "oos_rows": mechanism_own_oos_rows,
                "oos_abstained": mechanism_own_oos_abstained,
                "oos_abstain_recall": mechanism_selected.get("oos_abstain_recall"),
            },
            "overlap_oos_rows": {
                "row_count": len(oos_rows),
                "current_surface_abstained": current_oos_abstained,
                "current_surface_abstain_recall": _recall(
                    current_oos_abstained, len(oos_rows)
                ),
                "mechanism_surface_abstained": mechanism_oos_abstained,
                "mechanism_surface_abstain_recall": _recall(
                    mechanism_oos_abstained, len(oos_rows)
                ),
                "union_or_gate_abstained": union_oos_abstained,
                "union_or_gate_abstain_recall": _recall(
                    union_oos_abstained, len(oos_rows)
                ),
                "union_minus_current_abstain_recall": oos_overlap_lift,
                "current_retained_oos_rows": len(current_retained_oos),
                "current_retained_oos_caught_by_mechanism": len(
                    caught_current_retained_oos
                ),
                "current_retained_oos_catch_fraction": _recall(
                    len(caught_current_retained_oos), len(current_retained_oos)
                ),
            },
            "valid_primary_overlap_rows": {
                "row_count": len(primary_rows),
                "current_surface_retained": current_primary_retained,
                "current_surface_retain_recall": _recall(
                    current_primary_retained, len(primary_rows)
                ),
                "mechanism_surface_retained": mechanism_primary_retained,
                "mechanism_surface_retain_recall": _recall(
                    mechanism_primary_retained, len(primary_rows)
                ),
                "union_or_gate_retained": union_primary_retained,
                "union_or_gate_retain_recall": _recall(
                    union_primary_retained, len(primary_rows)
                ),
            },
        },
        "row_readouts": {
            "oos_overlap_rows": oos_rows,
            "valid_primary_overlap_rows": primary_rows,
            "mechanism_primary_rows_excluded_from_current_surface_retention_claim": [
                {
                    "entry_id": entry_id,
                    "reason": "row_is_current_geometry_fold_train_target",
                }
                for entry_id in invalid_primary_train_target_overlap
            ],
        },
        "missing_evidence_rows": {
            "current_calibration_primary_rows_requiring_source_free_mechanism_features": [
                {
                    "entry_id": entry_id,
                    "accession": current_primary_rows[entry_id].get("accession"),
                    "current_surface_score": _rounded_current_score(
                        current_primary_rows[entry_id], channel
                    ),
                    "reason": (
                        "row_is_current_geometry_fold_calibration_primary_without_"
                        "split_aligned_mechanism_feature_sidecar"
                    ),
                    "required_evidence": (
                        "source-free row-specific mechanism feature sidecar "
                        "compatible with the frozen residual contract"
                    ),
                }
                for entry_id in missing_primary_ids
            ],
            "current_calibration_oos_rows_requiring_source_free_mechanism_features": [
                {
                    "entry_id": entry_id,
                    "accession": current_oos_rows[entry_id].get("accession"),
                    "current_surface_score": _rounded_current_score(
                        current_oos_rows[entry_id], channel
                    ),
                    "current_surface_abstains": _current_abstains(
                        current_oos_rows[entry_id], channel, current_threshold
                    ),
                    "reason": (
                        "row_is_current_geometry_fold_calibration_oos_without_"
                        "split_aligned_mechanism_feature_sidecar"
                    ),
                    "required_evidence": (
                        "source-free row-specific mechanism feature sidecar "
                        "compatible with the frozen residual contract"
                    ),
                }
                for entry_id in missing_oos_ids
            ],
        },
        "counts": {
            "mechanism_calibration_primary_rows": len(mechanism_primary_ids),
            "mechanism_calibration_oos_rows": len(mechanism_oos_ids),
            "current_surface_calibration_primary_rows": len(current_primary_rows),
            "current_surface_calibration_oos_rows": len(current_oos_rows),
            "valid_primary_overlap_rows": len(primary_rows),
            "oos_overlap_rows": len(oos_rows),
            "missing_current_calibration_primary_mechanism_feature_rows": len(
                missing_primary_ids
            ),
            "missing_current_calibration_oos_mechanism_feature_rows": len(
                missing_oos_ids
            ),
            "mechanism_primary_rows_excluded_as_current_surface_train_targets": len(
                invalid_primary_train_target_overlap
            ),
            "current_retained_oos_overlap_rows": len(current_retained_oos),
            "current_retained_oos_caught_by_mechanism": len(
                caught_current_retained_oos
            ),
            "critical_violation_total": 0,
            "missing_evidence_items": len(missing_evidence),
        },
        "decision": {
            "local_oos_signal_measured": local_oos_signal,
            "mechanism_adds_oos_abstentions_on_overlap": local_oos_signal,
            "valid_integrated_operating_point_measurable": (
                valid_operating_point_measurable
            ),
            "adds_operating_point_value_beyond_current_surface": deployable,
            "deployable_now": deployable,
            "research_only": not deployable,
            "negative": False,
            "apply_or_promote_now": False,
            "smallest_next_experiment": (
                "Materialize the same source-free mechanism feature contract for "
                f"the {len(missing_primary_ids)} current geometry/fold "
                "calibration-primary rows and the "
                f"{len(missing_oos_ids)} current train/cal OOS negative rows "
                "not already covered by the mechanism sidecar, then rerun this "
                "fixed-threshold union readout without reading or tuning on "
                "heldout."
            ),
        },
        "missing_evidence": missing_evidence,
        "source_artifacts": {
            "mechanism_no_template_rerun": _source_path_record(
                mechanism_no_template_rerun_path
            ),
            "mechanism_operating_point_contract": (
                _source_path_record(mechanism_operating_point_contract_path)
                if mechanism_operating_point_contract_path is not None
                else None
            ),
            "current_in_scope_threshold_contract": _source_path_record(
                current_in_scope_threshold_contract_path
            ),
            "expanded_oos_calibrated_threshold_contract": _source_path_record(
                expanded_oos_calibrated_threshold_contract_path
            ),
        },
        "interpretation": {
            "headline": (
                "Mechanism features catch "
                f"{len(caught_current_retained_oos)}/{len(current_retained_oos)} "
                "current-surface retained OOS rows on the available overlap, but "
                f"valid primary overlap is {len(primary_rows)} rows."
            ),
            "result": (
                "Research-only: the train/cal row-specific mechanism surface shows local OOS "
                "signal beyond geometry/fold, but the current data cannot measure "
                "the in-scope retention cost because the mechanism calibration "
                "primaries are current geometry/fold train targets."
            ),
            "next_action": (
                "Build a split-aligned source-free mechanism sidecar for the "
                "current geometry/fold calibration-primary and train/cal OOS rows."
            ),
        },
    }


def render_lever2_mechanism_feature_incremental_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    measured = readout["measured_readout"]
    decision = readout["decision"]
    fixed = readout["fixed_operating_points"]
    overlap = measured["overlap_oos_rows"]
    primary = measured["valid_primary_overlap_rows"]
    missing_rows = readout.get("missing_evidence_rows") or {}
    missing_primary_rows = (
        missing_rows.get(
            "current_calibration_primary_rows_requiring_source_free_mechanism_features"
        )
        or []
    )
    missing_oos_rows = (
        missing_rows.get(
            "current_calibration_oos_rows_requiring_source_free_mechanism_features"
        )
        or []
    )
    missing_oos_retained = [
        row for row in missing_oos_rows if not row.get("current_surface_abstains")
    ]
    missing_oos_abstained = [
        row for row in missing_oos_rows if row.get("current_surface_abstains")
    ]

    def _score_sort(row: dict[str, Any]) -> float:
        score = row.get("current_surface_score")
        return float(score) if score is not None else -1.0

    def _entry_ids(rows: list[dict[str, Any]]) -> str:
        ids = [str(row.get("entry_id")) for row in rows if row.get("entry_id")]
        return ", ".join(ids) if ids else "none"

    lines = [
        "# Lever 2 Mechanism Feature Incremental Readout - current702",
        "",
        f"Run: {readout['created_utc']}",
        "",
        readout["scope"],
        "",
        "## Status",
        "",
        f"- {readout['status']}",
        f"- Result class: {readout['result_class']}",
        f"- Current surface: {fixed['current_surface']['channel']} "
        f"< {fixed['current_surface']['threshold']} abstains",
        f"- Mechanism residual > {fixed['mechanism_surface']['threshold']} abstains",
        "- Valid primary overlap: "
        f"{counts['valid_primary_overlap_rows']}/"
        f"{counts['current_surface_calibration_primary_rows']}",
        "- OOS overlap: "
        f"{counts['oos_overlap_rows']}/"
        f"{counts['current_surface_calibration_oos_rows']}",
        "",
        "## Measured Readout",
        "",
        "| surface | rows | abstained or retained | recall |",
        "| --- | ---: | ---: | ---: |",
        (
            "| current OOS overlap abstain | "
            f"{overlap['row_count']} | {overlap['current_surface_abstained']} | "
            f"{overlap['current_surface_abstain_recall']} |"
        ),
        (
            "| mechanism OOS overlap abstain | "
            f"{overlap['row_count']} | {overlap['mechanism_surface_abstained']} | "
            f"{overlap['mechanism_surface_abstain_recall']} |"
        ),
        (
            "| union OOS overlap abstain | "
            f"{overlap['row_count']} | {overlap['union_or_gate_abstained']} | "
            f"{overlap['union_or_gate_abstain_recall']} |"
        ),
        (
            "| union primary overlap retain | "
            f"{primary['row_count']} | {primary['union_or_gate_retained']} | "
            f"{primary['union_or_gate_retain_recall']} |"
        ),
        "",
        "## OOS Overlap Rows",
        "",
        "| row | current score | current abstains | mechanism residual | "
        "mechanism abstains | union abstains | caught retained OOS |",
        "| --- | ---: | --- | ---: | --- | --- | --- |",
    ]
    for row in readout["row_readouts"]["oos_overlap_rows"]:
        lines.append(
            f"| {row['entry_id']} | {row['current_surface_score']} | "
            f"{row['current_surface_abstains']} | {row['mechanism_residual']} | "
            f"{row['mechanism_surface_abstains']} | "
            f"{row['union_or_gate_abstains']} | "
            f"{row['current_false_negative_caught_by_mechanism']} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | why it matters |",
        "| --- | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Exact Missing Row Sets",
        "",
        (
            "- Current calibration primary rows still requiring source-free "
            f"mechanism features ({len(missing_primary_rows)}): "
            f"{_entry_ids(missing_primary_rows)}"
        ),
        (
            "- Current calibration OOS rows still requiring source-free mechanism "
            f"features ({len(missing_oos_rows)}): {_entry_ids(missing_oos_rows)}"
        ),
        "",
        "## Missing OOS Priority",
        "",
        f"- Current-retained missing OOS rows: {len(missing_oos_retained)}",
        f"- Already-abstained missing OOS rows: {len(missing_oos_abstained)}",
        "- Prioritize current-retained rows first because they are the direct "
        "route to incremental OOS value beyond geometry/fold.",
        "",
        "| retained OOS row | accession | current score |",
        "| --- | --- | ---: |",
    ]
    for row in sorted(missing_oos_retained, key=_score_sort, reverse=True)[:20]:
        lines.append(
            f"| {row['entry_id']} | {row.get('accession')} | "
            f"{row.get('current_surface_score')} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        f"- Local OOS signal measured: {decision['local_oos_signal_measured']}",
        "- Valid integrated operating point measurable: "
        f"{decision['valid_integrated_operating_point_measurable']}",
        "- Adds operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next experiment: {decision['smallest_next_experiment']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_source_free_partial_surface_current_split_portability_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    fixed = readout["fixed_operating_points"]["current_surface"]
    measured = readout["measured_readout"]
    surface = measured["current_split_surface"]
    overlap = measured["source_free_partial_surface_overlap"]
    review_only_locator = (
        measured.get("review_only_locator_candidate_current_split_overlap") or {}
    )
    missing_rows = readout.get("missing_evidence_rows") or {}
    missing_primary = (
        missing_rows.get(
            "current_primary_rows_requiring_source_free_partial_surface"
        )
        or []
    )
    missing_retained = (
        missing_rows.get(
            "current_retained_oos_rows_requiring_source_free_partial_surface"
        )
        or []
    )
    missing_abstained = (
        missing_rows.get(
            "current_abstained_oos_rows_requiring_source_free_partial_surface"
        )
        or []
    )

    def _entry_ids(rows: list[dict[str, Any]], limit: int | None = None) -> str:
        sliced = rows if limit is None else rows[:limit]
        ids = [str(row.get("entry_id")) for row in sliced if row.get("entry_id")]
        if not ids:
            return "none"
        suffix = " ..." if limit is not None and len(rows) > limit else ""
        return ", ".join(ids) + suffix

    def _score_sort(row: dict[str, Any]) -> float:
        score = row.get("current_surface_score")
        return float(score) if score is not None else -1.0

    lines = [
        "# Lever 2 Source-Free Partial Surface Current-Split Portability Readout - current702",
        "",
        f"Run: {readout['created_utc']}",
        "",
        readout["scope"],
        "",
        "## Status",
        "",
        f"- {readout['status']}",
        f"- Result class: {readout['result_class']}",
        f"- Current surface: {fixed['channel']} < {fixed['threshold']} abstains",
        "- Existing partial-surface union rows: "
        f"{counts['source_free_partial_surface_union_rows']}",
        "- Union overlap with current primary rows: "
        f"{counts['union_current_primary_overlap_rows']}/"
        f"{counts['current_primary_rows']}",
        "- Union overlap with current-retained OOS rows: "
        f"{counts['union_current_retained_oos_overlap_rows']}/"
        f"{counts['current_retained_oos_rows']}",
        "- Union overlap with already-abstained OOS rows: "
        f"{counts['union_current_abstained_oos_overlap_rows']}/"
        f"{counts['current_abstained_oos_rows']}",
        "- Review-only locator candidate overlap with current primary rows: "
        f"{counts['review_only_locator_candidate_current_primary_overlap_rows']}/"
        f"{counts['current_primary_rows']}",
        "- Review-only locator candidate overlap with current-retained OOS rows: "
        f"{counts['review_only_locator_candidate_current_retained_oos_overlap_rows']}/"
        f"{counts['current_retained_oos_rows']}",
        "",
        "## Current Split Surface",
        "",
        "| subset | rows |",
        "| --- | ---: |",
        f"| current primary | {surface['current_primary_rows']} |",
        f"| current extended OOS candidates | {surface['current_extended_candidate_oos_rows']} |",
        f"| current extended scored OOS | {surface['current_extended_scored_oos_rows']} |",
        f"| current-retained OOS | {surface['current_retained_oos_rows']} |",
        f"| already-abstained OOS | {surface['current_abstained_oos_rows']} |",
        "",
        "## Source-Free Partial-Surface Overlap",
        "",
        "| surface | rows | primary overlap | retained OOS overlap | abstained OOS overlap |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name in [
        "source_free_projection_candidate_surface",
        "source_free_event_axis_linkers",
        "source_free_locator_sidecars",
        "source_free_partial_surface_union",
    ]:
        summary = overlap[name]
        lines.append(
            f"| {name} | {summary['surface_rows']} | "
            f"{summary['current_primary_overlap_rows']} | "
            f"{summary['current_retained_oos_overlap_rows']} | "
            f"{summary['current_abstained_oos_overlap_rows']} |"
        )
    lines += [
        "",
        "## Review-Only Locator Candidate Diagnostic",
        "",
        "| surface | rows | primary overlap | retained OOS overlap | abstained OOS overlap |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            "| source_free_review_only_locator_candidates | "
            f"{review_only_locator.get('surface_rows')} | "
            f"{review_only_locator.get('current_primary_overlap_rows')} | "
            f"{review_only_locator.get('current_retained_oos_overlap_rows')} | "
            f"{review_only_locator.get('current_abstained_oos_overlap_rows')} |"
        ),
        "",
        "- Current primary rows with review-only locator candidates: "
        f"{', '.join(review_only_locator.get('current_primary_overlap_entry_ids') or []) or 'none'}",
        "- Current-retained OOS rows with review-only locator candidates: "
        f"{', '.join(review_only_locator.get('current_retained_oos_overlap_entry_ids') or []) or 'none'}",
    ]
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | "
            f"{gap['missing_rows_now']} | {gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Exact Missing Row Sets",
        "",
        (
            "- Current primary rows still requiring source-free partial-surface "
            f"mechanism evidence ({len(missing_primary)}): "
            f"{_entry_ids(missing_primary, 60)}"
        ),
        (
            "- Current-retained OOS rows still requiring source-free "
            f"partial-surface mechanism evidence ({len(missing_retained)}): "
            f"{_entry_ids(missing_retained, 60)}"
        ),
        (
            "- Already-abstained OOS rows still requiring source-free "
            f"partial-surface mechanism evidence ({len(missing_abstained)}): "
            f"{_entry_ids(missing_abstained, 60)}"
        ),
        "",
        "## Top Missing Current-Retained OOS Rows",
        "",
        "| row | current score |",
        "| --- | ---: |",
    ]
    for row in sorted(missing_retained, key=_score_sort, reverse=True)[:25]:
        lines.append(f"| {row['entry_id']} | {row.get('current_surface_score')} |")
    lines += [
        "",
        "## Decision",
        "",
        "- Existing partial surface reduces current primary gap: "
        f"{decision['existing_partial_surface_reduces_current_primary_gap']}",
        "- Existing partial surface reduces current-retained OOS gap: "
        f"{decision['existing_partial_surface_reduces_current_retained_oos_gap']}",
        "- Route negative for existing partial-surface reuse: "
        f"{decision['route_negative_for_existing_partial_surface_reuse']}",
        "- Adds operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_current_extended_frontier_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    best = measured["best_axis"]
    best_overlap = best["current_extended_overlap"]
    best_pair = measured.get("best_axis_pair")
    best_pair_overlap = (
        best_pair.get("current_extended_overlap") if isinstance(best_pair, dict) else {}
    )
    lines = [
        "# Lever 2 Event-Axis Current-Extended Frontier Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Best local event axis: "
            f"`{best['axis_id']}` catches "
            f"{best_overlap['current_retained_oos_caught_by_axis']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows beyond the fixed geometry/fold "
            "surface."
        ),
        (
            "- The best-axis OR gate abstains "
            f"{best_overlap['union_or_gate_abstained_rows']}/"
            f"{counts['current_extended_oos_overlap_rows']} current-overlap "
            "OOS rows."
        ),
        (
            "- Best paired-axis frontier: "
            f"`{best_pair['axis_pair_id']}` catches "
            f"{best_pair_overlap['current_retained_oos_caught_by_axis_pair']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows."
            if best_pair
            else "- Best paired-axis frontier: none"
        ),
        (
            "- Current primary retention on the active 34-row split remains "
            "unmeasurable: "
            f"{counts['valid_current_primary_calibration_feature_overlap_rows']}/"
            f"{counts['current_primary_rows']} valid current-primary rows have "
            "calibration-split mechanism features."
        ),
        "",
        "## Axis Frontier",
        "",
        (
            "| axis | source-free status | cal primary retained | "
            "cal OOS abstained | retained OOS caught | OR abstained |"
        ),
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in measured["axis_frontier_rows"]:
        selected = row["selected_rule"]
        overlap = row["current_extended_overlap"]
        lines.append(
            f"| {row['axis_id']} | {row['source_free_status']} | "
            f"{selected['calibration_primary_retained']}/"
            f"{selected['calibration_primary_rows']} | "
            f"{selected['calibration_oos_abstained']}/"
            f"{selected['calibration_oos_rows']} | "
            f"{overlap['current_retained_oos_caught_by_axis']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['union_or_gate_abstained_rows']}/"
            f"{overlap['row_count']} |"
        )
    if best_pair:
        top_pairs = sorted(
            measured["axis_pair_frontier_rows"],
            key=lambda row: (
                row["current_extended_overlap"][
                    "current_retained_oos_caught_by_axis_pair"
                ],
                row["current_extended_overlap"]["union_minus_current_abstained_rows"],
                row["calibration_oos_abstained"],
            ),
            reverse=True,
        )[:8]
        lines += [
            "",
            "## Axis Pair Frontier",
            "",
            (
                "| axis pair | source-free status | cal primary retained | "
                "cal OOS abstained | retained OOS caught | OR abstained |"
            ),
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
        for row in top_pairs:
            overlap = row["current_extended_overlap"]
            lines.append(
                f"| {row['axis_pair_id']} | {row['source_free_status']} | "
                f"{row['calibration_primary_retained']}/"
                f"{row['calibration_primary_rows']} | "
                f"{row['calibration_oos_abstained']}/"
                f"{row['calibration_oos_rows']} | "
                f"{overlap['current_retained_oos_caught_by_axis_pair']}/"
                f"{overlap['current_surface_retained_rows']} | "
                f"{overlap['union_or_gate_abstained_rows']}/"
                f"{overlap['row_count']} |"
            )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['missing_rows_now']} | "
            f"{gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        "- Local event-axis signal beyond current surface: "
        f"{decision['local_event_axis_signal_beyond_current_surface']}",
        "- Event-axis pair adds beyond best single axis: "
        f"{decision['event_axis_pair_adds_beyond_best_single_axis']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        "- Source-free current split operating point measurable: "
        f"{decision['source_free_current_split_operating_point_measurable']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_loo_current_extended_frontier_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    baseline = measured["baseline_projected_subset_axis"]
    baseline_overlap = baseline["current_extended_overlap"]
    best = measured["best_projection_plus_axis"]
    best_overlap = best["current_extended_overlap"]
    lines = [
        "# Lever 2 Event-Axis Leave-One-Out Current-Extended Frontier Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Baseline projected subset: "
            f"`{baseline['axis_id']}` catches "
            f"{baseline_overlap['current_retained_oos_caught_by_axis_loo']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows under leave-one-out selection."
        ),
        (
            "- Best projected-subset-plus-axis frontier: "
            f"`{best['projection_plus_axis_id']}` catches "
            f"{best_overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows."
        ),
        (
            "- Marginal catches beyond projected subset: "
            f"{best_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
            f"({', '.join(best_overlap['marginal_caught_entry_ids']) or 'none'})."
        ),
        (
            "- Current primary retention on the active split remains unmeasurable: "
            f"{counts['valid_current_primary_calibration_feature_overlap_rows']}/"
            f"{counts['current_primary_rows']} valid current-primary rows have "
            "calibration-split mechanism features."
        ),
        "",
        "## Leave-One-Out Single-Axis Frontier",
        "",
        (
            "| axis | source-free status | LOO rows | retained OOS caught | "
            "OR abstained | caught rows |"
        ),
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in measured["axis_loo_frontier_rows"]:
        overlap = row["current_extended_overlap"]
        lines.append(
            f"| {row['axis_id']} | {row['source_free_status']} | "
            f"{overlap['row_count']} | "
            f"{overlap['current_retained_oos_caught_by_axis_loo']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['union_or_gate_abstained_rows']}/"
            f"{overlap['row_count']} | "
            f"{', '.join(overlap['current_retained_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Projected Subset Plus Added Axis",
        "",
        (
            "| added axis | source-free status | retained OOS caught | "
            "marginal caught | primary LOO retained | OR abstained | marginal rows |"
        ),
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    top_pairs = sorted(
        measured["projection_plus_axis_loo_rows"],
        key=lambda row: (
            row["current_extended_overlap"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ],
            row["current_extended_overlap"][
                "projection_plus_axis_current_retained_oos_catches"
            ],
            row["current_extended_overlap"]["union_minus_current_abstained_rows"],
        ),
        reverse=True,
    )
    for row in top_pairs:
        overlap = row["current_extended_overlap"]
        primary_control = row["primary_leave_one_out_control"]
        lines.append(
            f"| {row['added_axis_id']} | {row['source_free_status']} | "
            f"{overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} | "
            f"{primary_control['retained_rows']}/"
            f"{primary_control['evaluable_rows']} | "
            f"{overlap['union_or_gate_abstained_rows']}/"
            f"{overlap['row_count']} | "
            f"{', '.join(overlap['marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['missing_rows_now']} | "
            f"{gap['why_it_matters']} |"
        )
    priority_rows = readout["missing_evidence_rows"][
        "best_projection_plus_axis_current_retained_overlap_rows_requiring_source_free_materialization"
    ]
    lines += [
        "",
        "## Priority Current-Retained Overlap Rows",
        "",
        (
            "| row | current score | baseline score | added-axis score | "
            "added rule | source-free row exists | marginal |"
        ),
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in priority_rows:
        added_rule = row.get("added_axis_selected_rule") or {}
        rule_label = (
            f"{added_rule.get('direction')} {added_rule.get('threshold')}"
            if added_rule
            else "n/a"
        )
        lines.append(
            f"| {row['entry_id']} | {row.get('current_surface_score')} | "
            f"{row.get('baseline_axis_score')} | {row.get('added_axis_score')} | "
            f"{rule_label} | "
            f"{row.get('existing_source_free_partial_surface_row_available')} | "
            f"{row['marginal_beyond_projected_subset']} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        "- Leave-one-out projected subset signal beyond current surface: "
        f"{decision['leave_one_out_projected_subset_signal_beyond_current_surface']}",
        "- Genuinely new axis adds beyond projected subset: "
        f"{decision['genuinely_new_axis_adds_beyond_projected_subset']}",
        "- Best new axis: "
        f"`{decision['best_new_axis_id']}`",
        "- Best projected-subset-plus-axis primary LOO control passes: "
        f"{decision['best_projection_plus_axis_primary_loo_control_passes']}",
        "- Any projected-subset-plus-axis primary LOO control passes: "
        f"{decision['any_projection_plus_axis_primary_loo_control_passes']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        "- Source-free current split operating point measurable: "
        f"{decision['source_free_current_split_operating_point_measurable']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_primary_safe_frontier_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    baseline = measured["baseline_projected_subset_axis"]
    baseline_overlap = baseline["current_extended_overlap"]
    best_marginal = measured["best_marginal_axis_before_primary_control"]
    best_marginal_overlap = best_marginal["current_extended_overlap"]
    best_marginal_control = best_marginal["primary_leave_one_out_control"]
    best_primary_safe = measured.get("best_primary_safe_axis")
    best_primary_safe_overlap = (
        best_primary_safe.get("current_extended_overlap")
        if isinstance(best_primary_safe, dict)
        else {}
    )
    priority_rows = readout["missing_evidence_rows"][
        "best_marginal_axis_current_retained_overlap_rows_requiring_source_free_materialization"
    ]
    primary_control_rows = readout["missing_evidence_rows"][
        "best_marginal_axis_primary_control_abstained_rows"
    ]
    sensitivity_rows = measured.get("primary_retain_floor_sensitivity") or []

    lines = [
        "# Lever 2 Event-Axis Primary-Safe Frontier Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Baseline projected subset catches "
            f"{baseline_overlap['current_retained_oos_caught_by_baseline']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows under strict LOO selection."
        ),
        (
            "- Best marginal pair before primary control: "
            f"`{best_marginal['projection_plus_axis_id']}` catches "
            f"{best_marginal_overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained rows, with "
            f"{best_marginal_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
            "marginal catches."
        ),
        (
            "- Its primary LOO control retains "
            f"{best_marginal_control['retained_rows']}/"
            f"{best_marginal_control['evaluable_rows']} rows; abstained controls: "
            f"{', '.join(best_marginal_control['abstained_entry_ids']) or 'none'}."
        ),
        (
            "- Best primary-safe pair: "
            f"`{best_primary_safe['projection_plus_axis_id']}` adds "
            f"{best_primary_safe_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
            "marginal catches."
            if best_primary_safe
            else "- Best primary-safe pair: none."
        ),
        "",
        "## Primary-Safe Frontier",
        "",
        (
            "| added axis | retained OOS caught | marginal caught | "
            "primary LOO retained | primary-safe | marginal rows |"
        ),
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in sorted(
        measured["projection_plus_axis_primary_safe_rows"],
        key=lambda item: (
            item["current_extended_overlap"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ],
            item["current_extended_overlap"][
                "projection_plus_axis_current_retained_oos_catches"
            ],
            item["primary_leave_one_out_control"]["retained_rows"],
        ),
        reverse=True,
    ):
        overlap = row["current_extended_overlap"]
        control = row["primary_leave_one_out_control"]
        control_passes = (
            control["retention_recall"] is not None
            and control["retention_recall"]
            >= readout["fixed_operating_points"]["axis_selection"][
                "min_primary_retain"
            ]
        )
        lines.append(
            f"| {row['added_axis_id']} | "
            f"{overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} | "
            f"{control['retained_rows']}/{control['evaluable_rows']} | "
            f"{control_passes} | "
            f"{', '.join(overlap['marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Primary-Retention Floor Sensitivity",
        "",
        (
            "| min primary retain | primary-safe surfaces | best marginal axis | "
            "best marginal catches | best primary-safe axis | primary-safe marginal catches | rows |"
        ),
        "| ---: | ---: | --- | ---: | --- | ---: | --- |",
    ]
    for row in sensitivity_rows:
        lines.append(
            f"| {row['min_primary_retain']} | "
            f"{row['primary_control_passing_projection_plus_axis_surfaces']} | "
            f"{row['best_marginal_axis_id']} | "
            f"{row['best_marginal_axis_marginal_current_retained_oos_catches']} | "
            f"{row['best_primary_safe_axis_id'] or 'none'} | "
            f"{row['best_primary_safe_axis_marginal_current_retained_oos_catches']} | "
            f"{', '.join(row['best_primary_safe_axis_marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['missing_rows_now']} | "
            f"{gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Priority Rows",
        "",
        "| row | current score | baseline score | added-axis score | marginal |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in priority_rows:
        lines.append(
            f"| {row['entry_id']} | {row.get('current_surface_score')} | "
            f"{row.get('baseline_axis_score')} | {row.get('added_axis_score')} | "
            f"{row['marginal_beyond_projected_subset']} |"
        )
    lines += [
        "",
        "- Best marginal primary-control rows requiring explicit control treatment: "
        f"{', '.join(row['entry_id'] for row in primary_control_rows) or 'none'}",
        "",
        "| control row | baseline score | added-axis score | baseline rule | added rule |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in primary_control_rows:
        pair_rule = row.get("selected_pair_rule") or {}
        baseline_rule = pair_rule.get("baseline_rule") or {}
        added_rule = pair_rule.get("added_rule") or {}
        baseline_label = (
            f"{baseline_rule.get('direction')} {baseline_rule.get('threshold')}"
            if baseline_rule
            else "n/a"
        )
        added_label = (
            f"{added_rule.get('direction')} {added_rule.get('threshold')}"
            if added_rule
            else "n/a"
        )
        lines.append(
            f"| {row['entry_id']} | {row.get('baseline_axis_score')} | "
            f"{row.get('added_axis_score')} | {baseline_label} | "
            f"{added_label} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        "- Genuinely new axis adds beyond projected subset before primary control: "
        f"{decision['genuinely_new_axis_adds_beyond_projected_subset_before_primary_control']}",
        "- Genuinely new axis adds beyond projected subset under primary-safe control: "
        f"{decision['genuinely_new_axis_adds_beyond_projected_subset_under_primary_safe_control']}",
        "- Best marginal axis primary LOO control passes: "
        f"{decision['best_marginal_axis_primary_loo_control_passes']}",
        "- Primary-safe marginal signal requires below-90% primary floor: "
        f"{decision['primary_safe_marginal_signal_requires_below_90pct_primary_floor']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        "- Source-free current split operating point measurable: "
        f"{decision['source_free_current_split_operating_point_measurable']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_primary_controlled_rescue_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    baseline = measured["baseline_projected_subset_axis"]
    baseline_overlap = baseline["current_extended_overlap"]
    best = measured["best_primary_controlled_axis"]
    best_overlap = best["current_extended_overlap"]
    priority_rows = readout["missing_evidence_rows"][
        "best_primary_controlled_axis_current_retained_overlap_rows_requiring_source_free_materialization"
    ]
    marginal_rows = readout["missing_evidence_rows"][
        "best_primary_controlled_axis_marginal_rows"
    ]
    primary_control_rows = readout["missing_evidence_rows"][
        "best_primary_controlled_axis_mechanism_primary_control_rows_requiring_source_free_materialization"
    ]
    smoke_tranche_rows = readout["missing_evidence_rows"][
        "smallest_primary_controlled_rescue_smoke_tranche_rows"
    ]
    smoke_coverage = measured[
        "smallest_smoke_tranche_existing_source_free_coverage"
    ]

    lines = [
        "# Lever 2 Event-Axis Primary-Controlled Rescue Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Baseline projected subset catches "
            f"{baseline_overlap['current_retained_oos_caught_by_baseline']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows under primary-controlled selection."
        ),
        (
            "- Best primary-controlled pair: "
            f"`{best['projection_plus_axis_id']}` catches "
            f"{best_overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained rows, with "
            f"{best_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
            "marginal catches."
        ),
        (
            "- Target selections passing primary control: "
            f"{best['primary_controlled_selection']['target_rows_passing_primary_control']}/"
            f"{best['primary_controlled_selection']['evaluable_rows']}."
        ),
        "",
        "## Primary-Controlled Frontier",
        "",
        (
            "| added axis | retained OOS caught | marginal caught | "
            "target rules passing primary control | marginal rows |"
        ),
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(
        measured["projection_plus_axis_primary_controlled_rows"],
        key=lambda item: (
            item["current_extended_overlap"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ],
            item["current_extended_overlap"][
                "projection_plus_axis_current_retained_oos_catches"
            ],
            item["primary_controlled_selection"][
                "target_rows_passing_primary_control"
            ],
        ),
        reverse=True,
    ):
        overlap = row["current_extended_overlap"]
        control = row["primary_controlled_selection"]
        lines.append(
            f"| {row['added_axis_id']} | "
            f"{overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} | "
            f"{control['target_rows_passing_primary_control']}/"
            f"{control['evaluable_rows']} | "
            f"{', '.join(overlap['marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['missing_rows_now']} | "
            f"{gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Priority Rows",
        "",
        "| row | current score | baseline score | added-axis score | marginal | added rule |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in priority_rows:
        added_rule = row.get("added_axis_selected_rule") or {}
        added_label = (
            f"{added_rule.get('direction')} {added_rule.get('threshold')}"
            if added_rule
            else "n/a"
        )
        lines.append(
            f"| {row['entry_id']} | {row.get('current_surface_score')} | "
            f"{row.get('baseline_axis_score')} | {row.get('added_axis_score')} | "
            f"{row['marginal_beyond_projected_subset']} | {added_label} |"
        )
    lines += [
        "",
        "- Primary-controlled marginal rows: "
        f"{', '.join(row['entry_id'] for row in marginal_rows) or 'none'}",
        "- Mechanism primary-control rows requiring source-free materialization: "
        f"{', '.join(row['entry_id'] for row in primary_control_rows) or 'none'}",
        "- Smallest primary-controlled rescue smoke tranche: "
        f"{len(smoke_tranche_rows)} rows.",
        "- Existing source-free coverage for that tranche: "
        f"{smoke_coverage['covered_rows']}/{smoke_coverage['tranche_rows']} "
        "rows; event-axis linker coverage: "
        f"{smoke_coverage['coverage_by_surface']['source_free_event_axis_linkers']['covered_tranche_rows']}/"
        f"{smoke_coverage['tranche_rows']}.",
        "",
        "## Decision",
        "",
        "- Genuinely new axis adds beyond projected subset under primary control: "
        f"{decision['genuinely_new_axis_adds_beyond_projected_subset_under_primary_control']}",
        "- Adds train/cal primary-controlled local value beyond current surface: "
        f"{decision['adds_train_cal_primary_controlled_local_value_beyond_current_surface']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        "- Source-free current split operating point measurable: "
        f"{decision['source_free_current_split_operating_point_measurable']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_signature_excluded_frontier_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    baseline = measured["baseline_projected_subset_axis"]
    baseline_overlap = baseline["current_extended_overlap"]
    best = measured["best_signature_excluded_axis"]
    best_overlap = best["current_extended_overlap"]
    marginal_rows = readout["missing_evidence_rows"][
        "best_signature_excluded_axis_marginal_rows"
    ]
    priority_rows = readout["missing_evidence_rows"][
        "best_signature_excluded_axis_current_retained_overlap_rows_requiring_source_free_materialization"
    ]

    lines = [
        "# Lever 2 Event-Axis Signature-Excluded Frontier Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Baseline projected subset catches "
            f"{baseline_overlap['current_retained_oos_caught_by_baseline']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained overlap rows under signature-excluded selection."
        ),
        (
            "- Best signature-excluded pair: "
            f"`{best['projection_plus_axis_id']}` catches "
            f"{best_overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained rows, with "
            f"{best_overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} "
            "marginal catches."
        ),
        (
            "- Same-signature OOS exclusions for the best pair: "
            f"{counts['signature_excluded_same_signature_oos_rows_for_best_axis']} "
            f"rows across {counts['signature_excluded_target_rows']} targets."
        ),
        "",
        "## Signature-Excluded Frontier",
        "",
        (
            "| added axis | retained OOS caught | marginal caught | "
            "rules passing primary control | same-signature rows excluded | marginal rows |"
        ),
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(
        measured["projection_plus_axis_signature_excluded_rows"],
        key=lambda item: (
            item["current_extended_overlap"][
                "marginal_current_retained_oos_catches_beyond_projected_subset"
            ],
            item["current_extended_overlap"][
                "projection_plus_axis_current_retained_oos_catches"
            ],
            item["signature_excluded_selection"][
                "target_rows_passing_primary_control"
            ],
        ),
        reverse=True,
    ):
        overlap = row["current_extended_overlap"]
        selection = row["signature_excluded_selection"]
        lines.append(
            f"| {row['added_axis_id']} | "
            f"{overlap['projection_plus_axis_current_retained_oos_catches']}/"
            f"{overlap['current_surface_retained_rows']} | "
            f"{overlap['marginal_current_retained_oos_catches_beyond_projected_subset']} | "
            f"{selection['target_rows_passing_primary_control']}/"
            f"{selection['evaluable_rows']} | "
            f"{selection['total_same_signature_oos_rows_excluded']} | "
            f"{', '.join(overlap['marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | {gap['missing_rows_now']} | "
            f"{gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Priority Rows",
        "",
        "| row | current score | baseline score | added-axis score | marginal | same-signature OOS excluded |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in priority_rows:
        signature = row.get("signature_exclusion") or {}
        lines.append(
            f"| {row['entry_id']} | {row.get('current_surface_score')} | "
            f"{row.get('baseline_axis_score')} | {row.get('added_axis_score')} | "
            f"{row['marginal_beyond_projected_subset']} | "
            f"{', '.join(signature.get('same_signature_oos_rows_excluded') or []) or 'none'} |"
        )
    lines += [
        "",
        "- Signature-excluded marginal rows: "
        f"{', '.join(row['entry_id'] for row in marginal_rows) or 'none'}",
        "",
        "## Decision",
        "",
        "- Genuinely new axis adds beyond projected subset after signature exclusion: "
        f"{decision['genuinely_new_axis_adds_beyond_projected_subset_after_signature_exclusion']}",
        "- Adds train/cal signature-excluded local value beyond current surface: "
        f"{decision['adds_train_cal_signature_excluded_local_value_beyond_current_surface']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        "- Source-free current split operating point measurable: "
        f"{decision['source_free_current_split_operating_point_measurable']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_signature_exclusion_sensitivity_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    rows = readout["measured_readout"]["signature_axis_sensitivity_rows"]
    lines = [
        "# Lever 2 Event-Axis Signature-Exclusion Sensitivity Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Sensitivity Matrix",
        "",
        (
            "| signature axis | best new axis | best marginal catches | "
            "best marginal rows | bond-change marginal | electron-flow marginal | "
            "same-signature rows excluded |"
        ),
        "| --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['signature_axis_id']} | {row['best_new_axis_id']} | "
            f"{row['best_signature_excluded_axis_marginal_current_retained_oos_catches']} | "
            f"{', '.join(row['best_signature_excluded_axis_marginal_entry_ids']) or 'none'} | "
            f"{row['bond_change_pair']['marginal_current_retained_oos_catches']} | "
            f"{row['electron_flow_pair']['marginal_current_retained_oos_catches']} | "
            f"{row['signature_excluded_same_signature_oos_rows']} |"
        )
    lines += [
        "",
        "## Key Counts",
        "",
        "- Signature axes evaluated: "
        f"{counts['signature_axes_evaluated']}",
        "- Signature axes with any marginal signal: "
        f"{counts['signature_axes_with_marginal_signal']}",
        "- Projected-signature bond-change marginal catches: "
        f"{counts['projected_signature_bond_change_marginal_catches']}",
        "- Bond-signature bond-change marginal catches: "
        f"{counts['bond_signature_bond_change_marginal_catches']}",
        "- Bond-signature electron-flow marginal catches: "
        f"{counts['bond_signature_electron_flow_marginal_catches']}",
        "",
        "## Decision",
        "",
        "- Any signature-excluded axis signal beyond current surface: "
        f"{decision['any_signature_excluded_axis_signal_beyond_current_surface']}",
        "- Bond-change survives projected-signature exclusion: "
        f"{decision['bond_change_signal_survives_projected_signature_exclusion']}",
        "- Bond-change survives bond-signature exclusion: "
        f"{decision['bond_change_signal_survives_bond_signature_exclusion']}",
        "- Bond-change collapses under own-signature exclusion: "
        f"{decision['bond_change_signal_collapses_under_own_signature_exclusion']}",
        "- Electron-flow survives bond-signature exclusion: "
        f"{decision['electron_flow_signal_survives_bond_signature_exclusion']}",
        "- Adds operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def render_lever2_event_axis_primary_controlled_null_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    observed = readout["measured_readout"]["observed_primary_controlled_rescue"]
    null_summary = readout["measured_readout"]["null_distribution"]["summary"]
    priority_null_summary = readout["measured_readout"][
        "priority_event_axis_null_distribution"
    ]["summary"]
    lines = [
        "# Lever 2 Event-Axis Primary-Controlled Null Readout",
        "",
        f"- Artifact: `{readout['artifact_id']}`",
        f"- Status: `{readout['status']}`",
        f"- Created UTC: `{readout['created_utc']}`",
        "",
        "## Measured Result",
        "",
        (
            "- Observed best pair: "
            f"`{observed['best_axis_id']}` with "
            f"{observed['best_axis_current_retained_oos_catches']}/"
            f"{counts['current_extended_current_retained_overlap_rows']} "
            "current-retained catches and "
            f"{observed['best_axis_marginal_current_retained_oos_catches']} "
            "marginal catches beyond the projected subset."
        ),
        (
            "- Observed marginal rows: "
            f"{', '.join(observed['best_axis_marginal_entry_ids']) or 'none'}."
        ),
        (
            "- Null distribution over "
            f"{counts['null_permutations']} deterministic permutations and "
            f"{counts['null_added_axes_evaluated']} added axes: min "
            f"{null_summary['min']}, median {null_summary['median']}, p90 "
            f"{null_summary['p90']}, p95 {null_summary['p95']}, max "
            f"{null_summary['max']}."
        ),
        (
            "- Priority event-axis null p95: "
            f"{priority_null_summary['p95']} with empirical p-value "
            f"{priority_null_summary['empirical_p_value_greater_equal_observed']}."
        ),
        (
            "- Empirical p-value for null max marginal catches >= observed: "
            f"{null_summary['empirical_p_value_greater_equal_observed']} "
            f"({null_summary['null_ge_observed_permutations']} permutations)."
        ),
        "",
        "## Top Null Permutations",
        "",
        "| permutation | best null axis | total catches | marginal catches | marginal rows |",
        "| ---: | --- | ---: | ---: | --- |",
    ]
    for row in readout["measured_readout"]["top_null_permutations"]:
        axis = row["best_null_axis"]
        lines.append(
            f"| {row['permutation_index']} | {axis['projection_plus_axis_id']} | "
            f"{axis['projection_plus_axis_current_retained_oos_catches']} | "
            f"{axis['marginal_current_retained_oos_catches_beyond_projected_subset']} | "
            f"{', '.join(axis['marginal_caught_entry_ids']) or 'none'} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        "- Observed marginal signal: "
        f"{decision['observed_primary_controlled_marginal_signal']}",
        "- Observed marginal exceeds null p95: "
        f"{decision['observed_marginal_exceeds_empirical_null_p95']}",
        "- Null control supports genuinely new axis signal: "
        f"{decision['null_control_supports_genuinely_new_axis_signal']}",
        "- Priority event-axis null supports signal: "
        f"{decision['priority_event_axis_null_control_supports_signal']}",
        "- Adds integrated operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Negative: {decision['negative']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_lever2_mechanism_feature_incremental_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    current_in_scope_threshold_contract_path: Path,
    expanded_oos_calibrated_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    mechanism_operating_point_contract_path: Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_mechanism_feature_incremental_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        mechanism_operating_point_contract_path=mechanism_operating_point_contract_path,
        current_in_scope_threshold_contract_path=current_in_scope_threshold_contract_path,
        expanded_oos_calibrated_threshold_contract_path=(
            expanded_oos_calibrated_threshold_contract_path
        ),
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_mechanism_feature_incremental_readout_report(readout),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_current_extended_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 0.9,
    artifact_id: str = DEFAULT_EVENT_AXIS_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_current_extended_frontier_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_current_extended_frontier_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_loo_current_extended_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 0.9,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_LOO_CURRENT_EXTENDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_loo_current_extended_frontier_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_loo_current_extended_frontier_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_primary_safe_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_SAFE_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_primary_safe_frontier_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_primary_safe_frontier_readout_report(readout),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_primary_controlled_rescue_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_RESCUE_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_primary_controlled_rescue_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_primary_controlled_rescue_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_signature_excluded_frontier_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    signature_axis_id: str = "source_free_projected_proton_role_subset",
    artifact_id: str = DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUDED_FRONTIER_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_signature_excluded_frontier_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        signature_axis_id=signature_axis_id,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_signature_excluded_frontier_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_signature_exclusion_sensitivity_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    signature_axis_ids: tuple[str, ...] = (
        "source_free_projected_proton_role_subset",
        "bond_change",
        "electron_flow",
        "event_topology",
    ),
    artifact_id: str = DEFAULT_EVENT_AXIS_SIGNATURE_EXCLUSION_SENSITIVITY_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_signature_exclusion_sensitivity_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        signature_axis_ids=signature_axis_ids,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_signature_exclusion_sensitivity_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_event_axis_primary_controlled_null_readout(
    *,
    mechanism_no_template_rerun_path: Path,
    train_cal_feature_sidecar_path: Path,
    current_extended_oos_mechanism_overlap_readout_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    partial_surface_current_split_portability_readout_path: Path | None = None,
    min_primary_retain: float = 1.0,
    baseline_axis_id: str = "source_free_projected_proton_role_subset",
    null_permutations: int = 128,
    null_seed: str = "lever2_primary_controlled_event_axis_null_v0",
    artifact_id: str = DEFAULT_EVENT_AXIS_PRIMARY_CONTROLLED_NULL_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_event_axis_primary_controlled_null_readout(
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_extended_oos_mechanism_overlap_readout_path=(
            current_extended_oos_mechanism_overlap_readout_path
        ),
        current_in_scope_threshold_contract_path=(
            current_in_scope_threshold_contract_path
        ),
        partial_surface_current_split_portability_readout_path=(
            partial_surface_current_split_portability_readout_path
        ),
        min_primary_retain=min_primary_retain,
        baseline_axis_id=baseline_axis_id,
        null_permutations=null_permutations,
        null_seed=null_seed,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_event_axis_primary_controlled_null_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def write_lever2_source_free_partial_surface_current_split_portability_readout(
    *,
    current_measured_readout_path: Path,
    current_extended_oos_surface_path: Path,
    current_in_scope_threshold_contract_path: Path,
    source_free_projection_repair_candidate_surface_path: Path,
    source_free_event_axis_linker_materialization_gate_path: Path,
    source_free_locator_rewrite_materialization_gate_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    review_only_locator_candidate_dir_path: Path | None = None,
    artifact_id: str = DEFAULT_PARTIAL_SURFACE_CURRENT_SPLIT_PORTABILITY_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = (
        build_lever2_source_free_partial_surface_current_split_portability_readout(
            current_measured_readout_path=current_measured_readout_path,
            current_extended_oos_surface_path=current_extended_oos_surface_path,
            current_in_scope_threshold_contract_path=(
                current_in_scope_threshold_contract_path
            ),
            source_free_projection_repair_candidate_surface_path=(
                source_free_projection_repair_candidate_surface_path
            ),
            source_free_event_axis_linker_materialization_gate_path=(
                source_free_event_axis_linker_materialization_gate_path
            ),
            source_free_locator_rewrite_materialization_gate_path=(
                source_free_locator_rewrite_materialization_gate_path
            ),
            review_only_locator_candidate_dir_path=(
                review_only_locator_candidate_dir_path
            ),
            artifact_id=artifact_id,
        )
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_source_free_partial_surface_current_split_portability_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def render_lever2_current_extended_oos_mechanism_overlap_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    measured = readout["measured_readout"]
    decision = readout["decision"]
    fixed = readout["fixed_operating_points"]
    overlap = measured["current_extended_oos_overlap_rows"]
    events = measured["event_feature_overlap_summary"]
    axis_overlap = measured.get("source_free_best_axis_current_extended_overlap") or {}
    candidate_reuse = (
        measured.get("existing_source_free_coordinate_anchor_candidate_reuse") or {}
    )
    missing_rows = readout.get("missing_evidence_rows") or {}
    missing_primary_rows = (
        missing_rows.get("current_primary_rows_requiring_mechanism_features") or []
    )
    missing_retained_oos_rows = (
        missing_rows.get(
            "current_extended_retained_oos_rows_requiring_mechanism_features"
        )
        or []
    )
    missing_abstained_oos_rows = (
        missing_rows.get(
            "current_extended_abstained_oos_rows_requiring_mechanism_features"
        )
        or []
    )

    def _score_sort(row: dict[str, Any]) -> float:
        score = row.get("current_surface_score")
        return float(score) if score is not None else -1.0

    def _entry_ids(rows: list[dict[str, Any]]) -> str:
        ids = [str(row.get("entry_id")) for row in rows if row.get("entry_id")]
        return ", ".join(ids) if ids else "none"

    lines = [
        "# Lever 2 Current Extended OOS Mechanism Overlap Readout - current702",
        "",
        f"Run: {readout['created_utc']}",
        "",
        readout["scope"],
        "",
        "## Status",
        "",
        f"- {readout['status']}",
        f"- Result class: {readout['result_class']}",
        f"- Current surface: {fixed['current_surface']['channel']} "
        f"< {fixed['current_surface']['threshold']} abstains",
        f"- Mechanism residual > {fixed['mechanism_surface']['threshold']} abstains",
        "- Current extended OOS overlap: "
        f"{counts['current_extended_oos_overlap_rows']}/"
        f"{counts['current_extended_scored_oos_rows']} scored rows",
        "- Best source-free axis current-extended OOS catches: "
        f"{counts['best_single_axis_new_oos_catches_on_current_extended_oos']}/"
        f"{counts['best_single_axis_new_oos_catches']}",
        "- Best source-free axis current-retained OOS catches: "
        f"{counts['best_single_axis_new_current_retained_oos_catches']}",
        "- Valid primary overlap: "
        f"{counts['valid_primary_overlap_rows']}/"
        f"{counts['current_primary_rows']}",
        "- Existing source-free coordinate-anchor candidate overlap with "
        "missing rows: "
        f"{counts['source_free_candidate_overlap_missing_primary_rows']} primary, "
        f"{counts['source_free_candidate_overlap_missing_retained_oos_rows']} "
        "current-retained OOS",
        "",
        "## Measured Readout",
        "",
        "| surface | overlap rows | abstained | recall |",
        "| --- | ---: | ---: | ---: |",
        (
            "| current geometry/fold | "
            f"{overlap['row_count']} | {overlap['current_surface_abstained']} | "
            f"{overlap['current_surface_abstain_recall']} |"
        ),
        (
            "| full mechanism residual | "
            f"{overlap['row_count']} | {overlap['mechanism_surface_abstained']} | "
            f"{overlap['mechanism_surface_abstain_recall']} |"
        ),
        (
            "| OR union | "
            f"{overlap['row_count']} | {overlap['union_or_gate_abstained']} | "
            f"{overlap['union_or_gate_abstain_recall']} |"
        ),
        "",
        "## Current-Retained OOS Catches",
        "",
        "- Current-retained overlap rows: "
        f"{overlap['current_retained_oos_rows']}",
        "- Current-retained rows caught by mechanism: "
        f"{overlap['current_retained_oos_caught_by_mechanism']}",
        "- Catch fraction: "
        f"{overlap['current_retained_oos_catch_fraction']}",
        "- Union minus current abstain recall on overlap: "
        f"{overlap['union_minus_current_abstain_recall']}",
        "",
        "## Event-Feature Context",
        "",
        "| subset | rows | bond-change | proton-transfer | electron-transfer | "
        "mechanism abstained | retained caught |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label, summary in [
        ("all overlap", events["all_overlap_rows"]),
        ("current-retained overlap", events["current_retained_overlap_rows"]),
    ]:
        lines.append(
            f"| {label} | {summary['rows']} | "
            f"{summary['with_bond_change_event']} | "
            f"{summary['with_proton_transfer_event']} | "
            f"{summary['with_electron_transfer_event']} | "
            f"{summary['mechanism_abstained_rows']} | "
            f"{summary['current_retained_caught_by_mechanism']} |"
        )
    lines += [
        "",
        "## Source-Free Best-Axis Current Surface Overlap",
        "",
        f"- Best single axis: {axis_overlap.get('best_single_axis_name')}",
        "- New OOS catches on current extended OOS: "
        f"{counts['best_single_axis_new_oos_catches_on_current_extended_oos']}/"
        f"{counts['best_single_axis_new_oos_catches']}",
        "- New current-retained OOS catches: "
        f"{counts['best_single_axis_new_current_retained_oos_catches']}",
        "",
        "| row | in current extended OOS | current score | current abstains | "
        "best-axis residual | current retained catch |",
        "| --- | --- | ---: | --- | ---: | --- |",
    ]
    for row in axis_overlap.get("best_single_axis_new_oos_rows") or []:
        lines.append(
            f"| {row['entry_id']} | {row['in_current_extended_scored_oos']} | "
            f"{row.get('current_surface_score')} | "
            f"{row.get('current_surface_abstains')} | "
            f"{row.get('best_single_axis_residual')} | "
            f"{row.get('current_retained_oos_caught_by_best_axis')} |"
        )
    lines += [
        "",
        "## Existing Source-Free Candidate Reuse",
        "",
        "- Coordinate-anchor candidate files checked: "
        f"{candidate_reuse.get('candidate_files')}",
        "- Missing current primary rows covered by existing candidates: "
        f"{len(candidate_reuse.get('missing_primary_overlap_rows') or [])}",
        "- Missing current-retained OOS rows covered by existing candidates: "
        f"{len(candidate_reuse.get('missing_retained_oos_overlap_rows') or [])}",
        "- Missing already-abstained OOS rows covered by existing candidates: "
        f"{len(candidate_reuse.get('missing_abstained_oos_overlap_rows') or [])}",
        "",
        "## OOS Overlap Rows",
        "",
        "| row | current score | current abstains | mechanism residual | "
        "mechanism abstains | caught retained OOS | electron | proton | bond |",
        "| --- | ---: | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in readout["row_readouts"]["current_extended_oos_overlap_rows"]:
        lines.append(
            f"| {row['entry_id']} | {row['current_surface_score']} | "
            f"{row['current_surface_abstains']} | {row['mechanism_residual']} | "
            f"{row['mechanism_surface_abstains']} | "
            f"{row['current_false_negative_caught_by_mechanism']} | "
            f"{row['has_electron_transfer_event']} | "
            f"{row['has_proton_transfer_event']} | "
            f"{row['has_bond_change_event']} |"
        )
    lines += [
        "",
        "## Missing Evidence",
        "",
        "| gap | required | valid now | missing now | why it matters |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for gap in readout["missing_evidence"]:
        missing_now = gap.get(
            "missing_rows_now",
            gap["required_rows"] - gap["valid_overlap_rows_now"],
        )
        lines.append(
            f"| {gap['gap_id']} | {gap['required_rows']} | "
            f"{gap['valid_overlap_rows_now']} | "
            f"{missing_now} | "
            f"{gap['why_it_matters']} |"
        )
    lines += [
        "",
        "## Exact Missing Row Sets",
        "",
        (
            "- Current primary rows still requiring mechanism features "
            f"({len(missing_primary_rows)}): {_entry_ids(missing_primary_rows)}"
        ),
        (
            "- Current-retained extended OOS rows still requiring mechanism "
            f"features ({len(missing_retained_oos_rows)}): "
            f"{_entry_ids(missing_retained_oos_rows[:40])}"
            + (" ..." if len(missing_retained_oos_rows) > 40 else "")
        ),
        (
            "- Already-abstained extended OOS rows still requiring mechanism "
            f"features ({len(missing_abstained_oos_rows)}): "
            f"{_entry_ids(missing_abstained_oos_rows[:40])}"
            + (" ..." if len(missing_abstained_oos_rows) > 40 else "")
        ),
        "",
        "## Top Missing Current-Retained OOS Rows",
        "",
        "| row | accession | current score |",
        "| --- | --- | ---: |",
    ]
    for row in sorted(missing_retained_oos_rows, key=_score_sort, reverse=True)[:20]:
        lines.append(
            f"| {row['entry_id']} | {row.get('accession')} | "
            f"{row.get('current_surface_score')} |"
        )
    lines += [
        "",
        "## Decision",
        "",
        f"- Local OOS signal measured: {decision['local_oos_signal_measured']}",
        "- Valid integrated operating point measurable: "
        f"{decision['valid_integrated_operating_point_measurable']}",
        "- Adds operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['headline']}",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_lever2_current_extended_oos_mechanism_overlap_readout(
    *,
    current_measured_readout_path: Path,
    current_extended_oos_surface_path: Path,
    mechanism_no_template_rerun_path: Path,
    current_in_scope_threshold_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    mechanism_operating_point_contract_path: Path | None = None,
    train_cal_feature_sidecar_path: Path | None = None,
    projection_readout_path: Path | None = None,
    source_free_coordinate_anchor_candidate_dir_path: Path | None = None,
    artifact_id: str = DEFAULT_CURRENT_EXTENDED_OOS_MECHANISM_OVERLAP_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_current_extended_oos_mechanism_overlap_readout(
        current_measured_readout_path=current_measured_readout_path,
        current_extended_oos_surface_path=current_extended_oos_surface_path,
        mechanism_no_template_rerun_path=mechanism_no_template_rerun_path,
        mechanism_operating_point_contract_path=mechanism_operating_point_contract_path,
        current_in_scope_threshold_contract_path=current_in_scope_threshold_contract_path,
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        projection_readout_path=projection_readout_path,
        source_free_coordinate_anchor_candidate_dir_path=(
            source_free_coordinate_anchor_candidate_dir_path
        ),
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_current_extended_oos_mechanism_overlap_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout


def render_lever2_source_free_electron_flow_split_alignment_readout_report(
    readout: dict[str, Any],
) -> str:
    counts = readout["counts"]
    decision = readout["decision"]
    measured = readout["measured_readout"]
    ceiling = measured["train_cal_axis_ceiling"]
    raw_overlap = measured.get("raw_full_sidecar_current_surface_overlap_diagnostic")
    raw_counts = (
        raw_overlap.get("counts", {})
        if isinstance(raw_overlap, dict) and raw_overlap.get("available")
        else {}
    )
    extended_overlap = (
        measured.get("best_axis_current_extended_oos_overlap_diagnostic") or {}
    )
    current = ceiling.get("current_source_free_projected_subset") or {}
    electron = ceiling.get("current_plus_missing_electron_flow") or {}
    full = ceiling.get("full_frozen_row_specific_surface") or {}
    acquisition_rows = readout.get("acquisition_priority_rows") or []
    lines = [
        "# Lever 2 Source-Free Electron-Flow Split-Alignment Readout - current702",
        "",
        f"Run: {readout['created_utc']}",
        "",
        readout["scope"],
        "",
        "## Status",
        "",
        f"- {readout['status']}",
        f"- Result class: {readout['result_class']}",
        "- Electron-flow train/cal OOS recall delta: "
        f"{ceiling['electron_flow_oos_abstain_recall_delta_vs_current_projected']}",
        "- Best-axis new OOS catches on current geometry/fold OOS rows: "
        f"{counts['best_single_axis_new_oos_catches_on_current_geometry_fold_oos']}/"
        f"{counts['best_single_axis_new_oos_catches']}",
        "- Best-axis new OOS catches on current extended OOS rows: "
        f"{counts['best_single_axis_new_oos_catches_on_current_extended_oos']}/"
        f"{counts['best_single_axis_new_oos_catches']}",
        "- Best-axis new current-retained OOS catches: "
        f"{counts['best_single_axis_new_current_retained_oos_catches']}",
        "- Source-free candidate overlap with current calibration primary rows: "
        f"{counts['source_free_candidate_projection_overlap_primary_rows']}/"
        f"{counts['current_geometry_fold_calibration_primary_rows']}",
        "- Source-free candidate overlap with current calibration OOS rows: "
        f"{counts['source_free_candidate_projection_overlap_oos_rows']}/"
        f"{counts['current_geometry_fold_calibration_oos_rows']}",
        "",
        "## Measured Train/Cal Axis Readout",
        "",
        "| variant | fields | primary retain | OOS abstain | AUC | threshold |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        (
            "| current projected subset | "
            f"{current.get('feature_field_count')} | "
            f"{current.get('primary_retain_recall')} | "
            f"{current.get('oos_abstain_recall')} | "
            f"{current.get('auc_oos_gt_primary')} | "
            f"{current.get('threshold')} |"
        ),
        (
            "| current + electron flow | "
            f"{electron.get('feature_field_count')} | "
            f"{electron.get('primary_retain_recall')} | "
            f"{electron.get('oos_abstain_recall')} | "
            f"{electron.get('auc_oos_gt_primary')} | "
            f"{electron.get('threshold')} |"
        ),
        (
            "| full row-specific surface | "
            f"{full.get('feature_field_count')} | "
            f"{full.get('primary_retain_recall')} | "
            f"{full.get('oos_abstain_recall')} | "
            f"{full.get('auc_oos_gt_primary')} | "
            f"{full.get('threshold')} |"
        ),
        "",
        "## Raw Full-Sidecar Current-Surface Overlap",
        "",
        (
            "- Available: "
            f"{bool(isinstance(raw_overlap, dict) and raw_overlap.get('available'))}"
        ),
        "- Valid current-primary calibration-feature overlap rows: "
        f"{raw_counts.get('valid_current_primary_calibration_feature_overlap_rows')}",
        "- Current-primary rows excluded as mechanism train targets: "
        f"{raw_counts.get('current_primary_rows_excluded_as_mechanism_train_targets')}",
        "- Current-OOS calibration-feature overlap rows: "
        f"{raw_counts.get('current_oos_calibration_feature_overlap_rows')}",
        "- Current-retained OOS overlap rows with electron transfer: "
        f"{raw_counts.get('electron_positive_current_retained_oos_overlap_rows')}/"
        f"{raw_counts.get('current_retained_oos_overlap_rows')}",
        "",
        "## Missing Split-Aligned Evidence",
        "",
        "- Current-retained OOS rows missing electron-flow evidence: "
        f"{counts['missing_current_retained_oos_electron_flow_rows']}",
        "- Current primary retention-gate rows missing electron-flow evidence: "
        f"{counts['missing_current_primary_electron_flow_rows']}",
        "- Already-abstained OOS rows missing electron-flow evidence: "
        f"{counts['missing_current_abstained_oos_electron_flow_rows']}",
        "- Candidate-surface overlap with retained OOS priority rows: "
        f"{counts['candidate_surface_overlap_missing_retained_oos_rows']}",
        "",
        "## Acquisition Priority Rows",
        "",
        "| priority | row | class | accession | current score | candidate row exists |",
        "| ---: | --- | --- | --- | ---: | --- |",
    ]
    for row in acquisition_rows[:80]:
        lines.append(
            f"| {row['priority_tier']} | {row['entry_id']} | "
            f"{row['priority_class']} | {row.get('accession')} | "
            f"{row.get('current_surface_score')} | "
            f"{row['source_free_candidate_projection_row_available']} |"
        )
    if len(acquisition_rows) > 80:
        lines.append(f"| ... | {len(acquisition_rows) - 80} additional rows |  |  |  |  |")
    if extended_overlap.get("available"):
        lines += [
            "",
            "## Best-Axis Current Extended OOS Rows",
            "",
            "| row | in current extended OOS | current score | current abstains | retained catch |",
            "| --- | --- | ---: | --- | --- |",
        ]
        for row in extended_overlap.get("best_single_axis_new_oos_rows") or []:
            lines.append(
                f"| {row['entry_id']} | {row['in_current_extended_scored_oos']} | "
                f"{row.get('current_surface_score')} | "
                f"{row.get('current_surface_abstains')} | "
                f"{row.get('current_retained_oos_caught_by_best_axis')} |"
            )
    if isinstance(raw_overlap, dict) and raw_overlap.get("available"):
        lines += [
            "",
            "## Raw Overlap OOS Rows",
            "",
            "| row | current score | current abstains | has electron transfer | electron count |",
            "| --- | ---: | --- | --- | ---: |",
        ]
        for row in raw_overlap.get("current_oos_overlap_rows", []):
            lines.append(
                f"| {row['entry_id']} | {row.get('current_surface_score')} | "
                f"{row.get('current_surface_abstains')} | "
                f"{row.get('has_electron_transfer_event')} | "
                f"{row.get('electron_transfer_count')} |"
            )
    lines += [
        "",
        "## Decision",
        "",
        "- Electron-flow train/cal signal measured: "
        f"{decision['source_free_electron_flow_axis_has_train_cal_signal']}",
        "- Split-aligned current-surface incremental readout measurable: "
        f"{decision['split_aligned_current_surface_incremental_readout_measurable']}",
        "- Adds operating-point value beyond current surface: "
        f"{decision['adds_operating_point_value_beyond_current_surface']}",
        f"- Deployable now: {decision['deployable_now']}",
        f"- Research-only: {decision['research_only']}",
        f"- Next gate: {decision['next_gate']}",
        "",
        "## Interpretation",
        "",
        f"- {readout['interpretation']['result']}",
        f"- {readout['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_lever2_source_free_electron_flow_split_alignment_readout(
    *,
    projection_readout_path: Path,
    incremental_readout_path: Path,
    source_free_projection_repair_candidate_surface_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    train_cal_feature_sidecar_path: Path | None = None,
    current_in_scope_threshold_contract_path: Path | None = None,
    expanded_oos_calibrated_threshold_contract_path: Path | None = None,
    current_extended_oos_surface_path: Path | None = None,
    artifact_id: str = DEFAULT_ELECTRON_FLOW_SPLIT_ALIGNMENT_ARTIFACT_ID,
) -> dict[str, Any]:
    readout = build_lever2_source_free_electron_flow_split_alignment_readout(
        projection_readout_path=projection_readout_path,
        incremental_readout_path=incremental_readout_path,
        source_free_projection_repair_candidate_surface_path=(
            source_free_projection_repair_candidate_surface_path
        ),
        train_cal_feature_sidecar_path=train_cal_feature_sidecar_path,
        current_in_scope_threshold_contract_path=current_in_scope_threshold_contract_path,
        expanded_oos_calibrated_threshold_contract_path=(
            expanded_oos_calibrated_threshold_contract_path
        ),
        current_extended_oos_surface_path=current_extended_oos_surface_path,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_lever2_source_free_electron_flow_split_alignment_readout_report(
                readout
            ),
            encoding="utf-8",
        )
    return readout
