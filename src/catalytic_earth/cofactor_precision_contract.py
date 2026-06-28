"""Current-router cofactor precision contract for predicted-geometry recovery.

The June 9 train/cal precision artifact was produced before the registry grew to
57 fingerprint families. A direct rerun on the current router is not comparable:
some frozen current702 rows still carry coarse v1 labels, while the current
router can call documented v2 subclasses. This module turns that mismatch into a
fail-closed contract instead of letting a downstream atlas-engine readout choose
an ambiguous surface.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CURRENT57_OPERATING_POINT_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_"
    "20260628_current57_rerun.json"
)
DEFAULT_TRUSTED_PRECISION_PATH = (
    "artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json"
)
DEFAULT_ONTOLOGY_PATH = "data/registries/mechanism_ontology.json"
DEFAULT_OUT_PATH = (
    "artifacts/"
    "v3_current57_cofactor_precision_contract_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/current57_cofactor_precision_contract_current702_20260628.md"
)

BASE_THRESHOLD_GRID: tuple[float, ...] = (
    0.4115,
    0.42,
    0.44,
    0.45,
    0.47,
    0.50,
    0.53,
    0.56,
    0.60,
    0.65,
    0.70,
    0.75,
    0.80,
    0.84,
    0.86,
    0.88,
)

# Explicitly documented frozen-v1 compatibility projection. This is not a new
# label family and not a production collapse: it only asks whether the current
# router is calling v2 subclasses of a frozen v1 umbrella.
LEGACY_V1_COMPATIBILITY: dict[str, tuple[str, ...]] = {
    "metal_dependent_hydrolase": (
        "metal_dependent_hydrolase",
        "metallopeptidase",
        "metallophosphoesterase_nuclease",
        "metallophosphomonoesterase",
        "metallo_amidohydrolase_deaminase",
    )
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _score(row: dict[str, Any], surface: str) -> float:
    value = row.get(surface, {}).get("top1_score")
    return float(value or 0.0)


def _called(row: dict[str, Any], surface: str) -> str | None:
    value = row.get(surface, {}).get("top1_fingerprint_id")
    return str(value) if value else None


def _legacy_v1_compatible(
    *, true_fingerprint_id: str | None, called_fingerprint_id: str | None
) -> bool:
    if not true_fingerprint_id or not called_fingerprint_id:
        return False
    if true_fingerprint_id == called_fingerprint_id:
        return True
    return called_fingerprint_id in LEGACY_V1_COMPATIBILITY.get(
        true_fingerprint_id, ()
    )


def _correct_at_threshold(
    row: dict[str, Any], *, surface: str, threshold: float, compatibility: bool
) -> bool:
    if _score(row, surface) < threshold:
        return False
    true_fingerprint = row.get("true_fingerprint_id")
    called_fingerprint = _called(row, surface)
    if compatibility:
        return _legacy_v1_compatible(
            true_fingerprint_id=true_fingerprint,
            called_fingerprint_id=called_fingerprint,
        )
    return bool(true_fingerprint and called_fingerprint == true_fingerprint)


def _fp_at_threshold(row: dict[str, Any], *, surface: str, threshold: float) -> bool:
    return _score(row, surface) >= threshold


def _round_threshold(value: float) -> float:
    return round(float(value), 4)


def _threshold_grid(rows: list[dict[str, Any]], *, surface: str) -> list[float]:
    values = {_round_threshold(v) for v in BASE_THRESHOLD_GRID}
    min_threshold = min(values)
    for row in rows:
        value = row.get(surface, {}).get("top1_score")
        if value is not None and float(value) >= min_threshold:
            values.add(_round_threshold(float(value)))
    return sorted(values)


def _point(
    *,
    threshold: float,
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    surface: str,
    compatibility: bool,
) -> dict[str, Any]:
    correct_rows = [
        str(row.get("entry_id"))
        for row in inscope_rows
        if _correct_at_threshold(
            row, surface=surface, threshold=threshold, compatibility=compatibility
        )
    ]
    fp_rows = [
        str(row.get("entry_id"))
        for row in oos_rows
        if _fp_at_threshold(row, surface=surface, threshold=threshold)
    ]
    return {
        "threshold": _round_threshold(threshold),
        "inscope_correct": len(correct_rows),
        "inscope_total": len(inscope_rows),
        "inscope_recall": round(len(correct_rows) / len(inscope_rows), 4)
        if inscope_rows
        else None,
        "oos_false_positives": len(fp_rows),
        "oos_total": len(oos_rows),
        "oos_false_positive_rate": round(len(fp_rows) / len(oos_rows), 4)
        if oos_rows
        else None,
        "correct_entry_ids": correct_rows,
        "oos_false_positive_entry_ids": fp_rows,
    }


def _sweep(
    *,
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    surface: str,
    compatibility: bool,
) -> list[dict[str, Any]]:
    return [
        _point(
            threshold=threshold,
            inscope_rows=inscope_rows,
            oos_rows=oos_rows,
            surface=surface,
            compatibility=compatibility,
        )
        for threshold in _threshold_grid(inscope_rows + oos_rows, surface=surface)
    ]


def _split_rows(
    current_operating_point: dict[str, Any], split: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    details = current_operating_point.get("row_details_by_split", {}).get(split, {})
    return list(details.get("inscope_rows", []) or []), list(
        details.get("oos_rows", []) or []
    )


def _trusted_done_bar(trusted_precision: dict[str, Any]) -> dict[str, Any]:
    cal = trusted_precision.get("operating_points_by_split", {}).get("calibration", {})
    fused = cal.get("fused_frozen_threshold", {})
    dial = trusted_precision.get("dial_comparison", {}).get(
        "threshold_dial_matching_suppression_precision"
    ) or fused
    return {
        "source_artifact_id": trusted_precision.get("artifact_id"),
        "min_calibration_inscope_correct": fused.get("inscope_correct"),
        "calibration_inscope_total": fused.get("inscope_total"),
        "max_calibration_oos_false_positives": dial.get("oos_false_positives"),
        "calibration_oos_total": dial.get("oos_total"),
        "reference_threshold": dial.get("threshold"),
        "reference_note": (
            "June 9 trusted cofactor precision bar: keep the fused calibration "
            "primary recovery while not exceeding the recalibrated 0.44 "
            "threshold-dial OOS false positives."
        ),
    }


def _best_point(
    points: list[dict[str, Any]], *, max_oos_fp: int | None
) -> dict[str, Any] | None:
    eligible = [
        point
        for point in points
        if max_oos_fp is not None
        and point.get("oos_false_positives") is not None
        and point["oos_false_positives"] <= max_oos_fp
    ]
    if not eligible:
        return None
    return max(
        eligible,
        key=lambda point: (
            point.get("inscope_correct") or 0,
            -(point.get("threshold") or 0.0),
        ),
    )


def _eligible_points(
    points: list[dict[str, Any]], *, min_correct: int | None, max_oos_fp: int | None
) -> list[dict[str, Any]]:
    if min_correct is None or max_oos_fp is None:
        return []
    return [
        point
        for point in points
        if point.get("inscope_correct") is not None
        and point.get("oos_false_positives") is not None
        and point["inscope_correct"] >= min_correct
        and point["oos_false_positives"] <= max_oos_fp
    ]


def _taxonomy_recovery_rows(
    inscope_rows: list[dict[str, Any]], *, surface: str, threshold: float
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inscope_rows:
        exact = _correct_at_threshold(
            row, surface=surface, threshold=threshold, compatibility=False
        )
        compatible = _correct_at_threshold(
            row, surface=surface, threshold=threshold, compatibility=True
        )
        if not exact and compatible:
            rows.append(
                {
                    "entry_id": row.get("entry_id"),
                    "true_fingerprint_id": row.get("true_fingerprint_id"),
                    "called_fingerprint_id": _called(row, surface),
                    "top1_score": row.get(surface, {}).get("top1_score"),
                }
            )
    return rows


def _compatibility_sources(ontology: dict[str, Any]) -> dict[str, Any]:
    families = ontology.get("families", []) if isinstance(ontology, dict) else []
    matching_notes = []
    for family in families:
        note = str(family.get("v2_split_note") or "")
        if "metal_dependent_hydrolase" in note and "v2 sub-families" in note:
            matching_notes.append(
                {
                    "family_id": family.get("id"),
                    "fingerprint_ids": family.get("fingerprint_ids", []),
                    "v2_split_note": note,
                }
            )
    return {
        "legacy_v1_compatibility": {
            key: list(values) for key, values in LEGACY_V1_COMPATIBILITY.items()
        },
        "source": (
            "data/registries/mechanism_ontology.json v2_split_note plus "
            "mechanism_fingerprints metal_dependent_hydrolase v2_split_note"
        ),
        "ontology_notes": matching_notes,
        "not_a_production_label_collapse": True,
    }


def build_current57_cofactor_precision_contract(
    *,
    current_operating_point: dict[str, Any],
    trusted_precision: dict[str, Any],
    ontology: dict[str, Any],
) -> dict[str, Any]:
    done_bar = _trusted_done_bar(trusted_precision)
    min_correct = done_bar.get("min_calibration_inscope_correct")
    max_oos_fp = done_bar.get("max_calibration_oos_false_positives")

    splits: dict[str, Any] = {}
    for split in ("calibration", "train"):
        inscope_rows, oos_rows = _split_rows(current_operating_point, split)
        exact = _sweep(
            inscope_rows=inscope_rows,
            oos_rows=oos_rows,
            surface="fused",
            compatibility=False,
        )
        compatible = _sweep(
            inscope_rows=inscope_rows,
            oos_rows=oos_rows,
            surface="fused",
            compatibility=True,
        )
        frozen_threshold = _round_threshold(
            current_operating_point.get("inputs", {}).get(
                "frozen_router_threshold", 0.4115
            )
        )
        exact_at_frozen = next(
            point for point in exact if point["threshold"] == frozen_threshold
        )
        compatible_at_frozen = next(
            point for point in compatible if point["threshold"] == frozen_threshold
        )
        splits[split] = {
            "is_out_of_sample_for_channel": split == "calibration",
            "exact_fused_sweep": exact,
            "legacy_v1_compatible_fused_sweep": compatible,
            "exact_fused_at_frozen_threshold": exact_at_frozen,
            "legacy_v1_compatible_fused_at_frozen_threshold": compatible_at_frozen,
            "taxonomy_version_recovery_rows_at_frozen_threshold": _taxonomy_recovery_rows(
                inscope_rows, surface="fused", threshold=frozen_threshold
            ),
            "best_legacy_v1_compatible_point_under_trusted_oos_fp": _best_point(
                compatible, max_oos_fp=max_oos_fp
            ),
        }

    cal_compatible = splits["calibration"]["legacy_v1_compatible_fused_sweep"]
    eligible = _eligible_points(
        cal_compatible, min_correct=min_correct, max_oos_fp=max_oos_fp
    )
    status = (
        "eligible_current57_threshold_contract_found"
        if eligible
        else "blocked_current57_cofactor_precision_contract_not_deployable"
    )

    cal_exact_frozen = splits["calibration"]["exact_fused_at_frozen_threshold"]
    cal_compat_frozen = splits["calibration"][
        "legacy_v1_compatible_fused_at_frozen_threshold"
    ]
    best_safe = splits["calibration"][
        "best_legacy_v1_compatible_point_under_trusted_oos_fp"
    ]

    return {
        "artifact_id": "v3_current57_cofactor_precision_contract_current702_20260628",
        "schema_version": "current57_cofactor_precision_contract.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_train_cal_precision_contract_no_threshold_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "input_surface": "train_cal_only_current57_cofactor_operating_point",
            "production_threshold_changed": False,
            "model_weights_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
            "compatibility_projection_is_diagnostic_only": True,
        },
        "inputs": {
            "current_operating_point_artifact_id": current_operating_point.get(
                "artifact_id"
            ),
            "trusted_precision_artifact_id": trusted_precision.get("artifact_id"),
            "current_router_threshold": current_operating_point.get("inputs", {}).get(
                "frozen_router_threshold"
            ),
            "observed_score_thresholds_included": True,
        },
        "compatibility_projection": _compatibility_sources(ontology),
        "pre_registered_done_bar": done_bar,
        "selection_rule": {
            "surface": "calibration_out_of_sample",
            "candidate_rule": (
                "A current-57 threshold-only cofactor precision contract is eligible "
                "only if a calibration threshold keeps at least the trusted June 9 "
                "fused primary count under the documented v1 metal-umbrella "
                "compatibility projection and does not exceed the trusted June 9 "
                "threshold-dial OOS false-positive count."
            ),
            "eligible_thresholds": eligible,
            "selected_threshold": eligible[0]["threshold"] if eligible else None,
            "decision": (
                "fail_closed_keep_atlas_engine_blocked_on_current57_cofactor_surface"
                if not eligible
                else "current57_threshold_contract_candidate_requires_review"
            ),
        },
        "calibration_summary": {
            "exact_fused_current57_at_frozen_threshold": cal_exact_frozen,
            "legacy_v1_compatible_fused_current57_at_frozen_threshold": (
                cal_compat_frozen
            ),
            "taxonomy_version_recovered_count": len(
                splits["calibration"][
                    "taxonomy_version_recovery_rows_at_frozen_threshold"
                ]
            ),
            "remaining_recovery_gap_vs_trusted": (
                (min_correct or 0)
                - (
                    cal_compat_frozen.get("inscope_correct")
                    if cal_compat_frozen
                    else 0
                )
            ),
            "best_point_under_trusted_oos_fp": best_safe,
        },
        "splits": splits,
        "interpretation": {
            "headline": (
                "The documented v1 metal-umbrella projection explains a large part "
                "of the current-57 exact-match drift, but no current-57 threshold "
                "meets the trusted June 9 cofactor precision bar on calibration."
            ),
            "deployment_decision": (
                "Fail closed for atlas-engine fusion on the current-57 cofactor "
                "surface. Either pin/replay the intended June 9 router/fingerprint "
                "surface, or build a new precision channel/fusion rule with a new "
                "preregistered train/cal done bar before any heldout-facing read."
            ),
        },
    }


def _report(contract: dict[str, Any]) -> str:
    done = contract["pre_registered_done_bar"]
    cal = contract["calibration_summary"]
    exact = cal["exact_fused_current57_at_frozen_threshold"]
    compat = cal["legacy_v1_compatible_fused_current57_at_frozen_threshold"]
    best = cal.get("best_point_under_trusted_oos_fp") or {}

    def fmt(point: dict[str, Any]) -> str:
        return (
            f"threshold {point.get('threshold')}: recall "
            f"{point.get('inscope_correct')}/{point.get('inscope_total')} "
            f"({point.get('inscope_recall')}) · OOS FP "
            f"{point.get('oos_false_positives')}/{point.get('oos_total')} "
            f"({point.get('oos_false_positive_rate')})"
        )

    lines = [
        "# Current-57 Cofactor Precision Contract",
        "",
        f"Run: {contract['created_utc']}",
        f"Status: `{contract['status']}`",
        "",
        "## Done Bar",
        "",
        "- Surface: calibration, out-of-sample for the sequence cofactor channel.",
        f"- Required primary recovery: >= {done.get('min_calibration_inscope_correct')}/"
        f"{done.get('calibration_inscope_total')}.",
        f"- Required OOS FP ceiling: <= {done.get('max_calibration_oos_false_positives')}/"
        f"{done.get('calibration_oos_total')} at the trusted June 9 threshold dial.",
        "",
        "## Current-57 Readout",
        "",
        f"- Exact current-57 fused at frozen threshold: {fmt(exact)}.",
        f"- Legacy-v1 metal-compatible fused at frozen threshold: {fmt(compat)}.",
        f"- Taxonomy-version recovered rows at frozen threshold: "
        f"{cal.get('taxonomy_version_recovered_count')}.",
        f"- Remaining recovery gap vs trusted bar: "
        f"{cal.get('remaining_recovery_gap_vs_trusted')}.",
        f"- Best compatible point under the trusted OOS FP ceiling: {fmt(best)}.",
        "",
        "## Decision",
        "",
        f"- {contract['interpretation']['deployment_decision']}",
        "",
        "## Guardrails",
        "",
        "- No heldout rows were scored or read.",
        "- No production threshold, model weight, split, label, ontology, registry, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_current57_cofactor_precision_contract(
    *,
    current_operating_point_path: Path,
    trusted_precision_path: Path,
    ontology_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    contract = build_current57_cofactor_precision_contract(
        current_operating_point=_load_json(current_operating_point_path),
        trusted_precision=_load_json(trusted_precision_path),
        ontology=_load_json(ontology_path),
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(contract), encoding="utf-8")
    return contract
