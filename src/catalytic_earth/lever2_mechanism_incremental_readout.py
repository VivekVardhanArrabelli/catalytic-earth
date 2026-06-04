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
        "| row | current score | current abstains | mechanism residual | mechanism abstains | union abstains | caught retained OOS |",
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
