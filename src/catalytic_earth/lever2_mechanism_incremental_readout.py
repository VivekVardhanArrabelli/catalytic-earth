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


def _m_csa_ids_from_candidate_dir(candidate_dir: Path | None) -> set[str]:
    if candidate_dir is None or not Path(candidate_dir).exists():
        return set()
    entry_ids: set[str] = set()
    for path in Path(candidate_dir).glob("*.json"):
        parts = path.stem.split("_")
        if len(parts) >= 3 and parts[0] == "m" and parts[1] == "csa":
            entry_ids.add(f"m_csa:{parts[2]}")
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
