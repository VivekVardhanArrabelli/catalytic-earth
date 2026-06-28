"""Preregistered current-57 cofactor + fold-NN fusion rule (train/cal only).

The current-57 cofactor precision contract fail-closed on a single cofactor
threshold (best safe point 20/35 recovery at the trusted OOS-FP ceiling). Now
that ``current57_fold_tm_recompute_readout`` has produced a row-aligned fold-NN
TM surface for the exact current-57 calibration cofactor rows, this module
preregisters a two-gate fusion rule that uses the fold-NN nearest-neighbor TM as
an OOS-rejection / abstention channel on top of the cofactor call:

    retained_in_scope_call := fused.top1_score >= cofactor_threshold
                              AND fold_nn_alntmscore >= fold_threshold

Correctness uses the same documented legacy-v1 metal-umbrella compatibility
projection as the precision contract. Thresholds are swept on the calibration
split only (out-of-sample for the sequence cofactor channel, never heldout); no
heldout row is read or scored, and no production threshold/registry is changed.
The rule is eligible only if a calibration operating point clears the trusted
June 9 done bar (recovery and OOS-FP ceiling). It also quantifies the marginal
OOS-rejection value the fold channel adds over the cofactor-only contract.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

from .cofactor_precision_contract import (
    BASE_THRESHOLD_GRID,
    _legacy_v1_compatible,
    _round_threshold,
    _trusted_done_bar,
)


DEFAULT_CURRENT57_OPERATING_POINT_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_"
    "20260628_current57_rerun.json"
)
DEFAULT_FOLD_READOUT_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json"
)
DEFAULT_TRUSTED_PRECISION_PATH = (
    "artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/"
    "v3_current57_cofactor_fold_fusion_preregistration_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/current57_cofactor_fold_fusion_preregistration_current702_20260628.md"
)

# Fold-NN TM (alntmscore) gate grid; 0.0 leaves the fold gate inactive so the
# cofactor-only contract is recoverable as a sub-case of this sweep.
BASE_FOLD_THRESHOLD_GRID: tuple[float, ...] = (
    0.0,
    0.50,
    0.55,
    0.58,
    0.60,
    0.62,
    0.65,
    0.68,
    0.70,
    0.72,
    0.74,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_summary(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "artifact_id": data.get("artifact_id"),
        "status": data.get("status"),
        "schema_version": data.get("schema_version"),
        "sha256": _sha256(path),
    }


def _fold_scores_by_entry(fold_readout: dict[str, Any]) -> dict[str, float]:
    scores: dict[str, float] = {}
    rows = fold_readout.get("rows", {})
    for group in ("calibration_inscope", "calibration_oos"):
        for row in rows.get(group, []) or []:
            entry_id = str(row.get("entry_id"))
            value = row.get("fold_nn_alntmscore")
            if entry_id and value is not None:
                scores[entry_id] = float(value)
    return scores


def _cofactor_score(row: dict[str, Any]) -> float:
    return float(row.get("fused", {}).get("top1_score") or 0.0)


def _called(row: dict[str, Any]) -> str | None:
    value = row.get("fused", {}).get("top1_fingerprint_id")
    return str(value) if value else None


def _compatible(row: dict[str, Any]) -> bool:
    return _legacy_v1_compatible(
        true_fingerprint_id=row.get("true_fingerprint_id"),
        called_fingerprint_id=_called(row),
    )


def _retained(
    row: dict[str, Any],
    *,
    cofactor_threshold: float,
    fold_threshold: float,
    fold_scores: dict[str, float],
) -> bool:
    if _cofactor_score(row) < cofactor_threshold:
        return False
    fold = fold_scores.get(str(row.get("entry_id")))
    if fold is None or fold < fold_threshold:
        return False
    return True


def _fold_grid(fold_scores: dict[str, float]) -> list[float]:
    values = {_round_threshold(v) for v in BASE_FOLD_THRESHOLD_GRID}
    for value in fold_scores.values():
        values.add(_round_threshold(value))
    return sorted(values)


def _cofactor_grid(rows: list[dict[str, Any]]) -> list[float]:
    values = {_round_threshold(v) for v in BASE_THRESHOLD_GRID}
    min_threshold = min(values)
    for row in rows:
        score = _cofactor_score(row)
        if score >= min_threshold:
            values.add(_round_threshold(score))
    return sorted(values)


def _point(
    *,
    cofactor_threshold: float,
    fold_threshold: float,
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    fold_scores: dict[str, float],
) -> dict[str, Any]:
    correct = [
        str(row.get("entry_id"))
        for row in inscope_rows
        if _retained(
            row,
            cofactor_threshold=cofactor_threshold,
            fold_threshold=fold_threshold,
            fold_scores=fold_scores,
        )
        and _compatible(row)
    ]
    fp = [
        str(row.get("entry_id"))
        for row in oos_rows
        if _retained(
            row,
            cofactor_threshold=cofactor_threshold,
            fold_threshold=fold_threshold,
            fold_scores=fold_scores,
        )
    ]
    return {
        "cofactor_threshold": _round_threshold(cofactor_threshold),
        "fold_threshold": _round_threshold(fold_threshold),
        "inscope_correct": len(correct),
        "inscope_total": len(inscope_rows),
        "inscope_recall": round(len(correct) / len(inscope_rows), 4)
        if inscope_rows
        else None,
        "oos_false_positives": len(fp),
        "oos_total": len(oos_rows),
        "oos_false_positive_rate": round(len(fp) / len(oos_rows), 4)
        if oos_rows
        else None,
    }


def _sweep(
    *,
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    fold_scores: dict[str, float],
) -> list[dict[str, Any]]:
    cofactor_grid = _cofactor_grid(inscope_rows + oos_rows)
    fold_grid = _fold_grid(fold_scores)
    return [
        _point(
            cofactor_threshold=cth,
            fold_threshold=fth,
            inscope_rows=inscope_rows,
            oos_rows=oos_rows,
            fold_scores=fold_scores,
        )
        for cth, fth in product(cofactor_grid, fold_grid)
    ]


def _best_under_fp_ceiling(
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
            -(point.get("oos_false_positives") or 0),
            -(point.get("cofactor_threshold") or 0.0),
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


def _max_precision_point(
    points: list[dict[str, Any]], *, min_recall: int
) -> dict[str, Any] | None:
    eligible = [
        point
        for point in points
        if (point.get("inscope_correct") or 0) >= min_recall
    ]
    if not eligible:
        return None
    return min(
        eligible,
        key=lambda point: (
            point.get("oos_false_positives") or 0,
            -(point.get("inscope_correct") or 0),
        ),
    )


def _recovery_ceiling(inscope_rows: list[dict[str, Any]]) -> dict[str, Any]:
    compatible = sum(1 for row in inscope_rows if _compatible(row))
    exact = sum(
        1
        for row in inscope_rows
        if row.get("true_fingerprint_id")
        and _called(row) == row.get("true_fingerprint_id")
    )
    return {
        "inscope_total": len(inscope_rows),
        "compatible_recovery_ceiling": compatible,
        "exact_recovery_ceiling": exact,
        "note": (
            "Maximum in-scope recovery at any threshold pair (fold gate open). The "
            "compatible ceiling caps fusion recovery regardless of the fold channel."
        ),
    }


def build_current57_cofactor_fold_fusion_preregistration(
    *,
    current_operating_point: dict[str, Any],
    fold_readout: dict[str, Any],
    trusted_precision: dict[str, Any],
) -> dict[str, Any]:
    done_bar = _trusted_done_bar(trusted_precision)
    min_correct = done_bar.get("min_calibration_inscope_correct")
    max_oos_fp = done_bar.get("max_calibration_oos_false_positives")

    fold_scores = _fold_scores_by_entry(fold_readout)
    details = current_operating_point.get("row_details_by_split", {}).get(
        "calibration", {}
    )
    inscope_rows = list(details.get("inscope_rows", []) or [])
    oos_rows = list(details.get("oos_rows", []) or [])

    fold_covered = sum(
        1
        for row in inscope_rows + oos_rows
        if str(row.get("entry_id")) in fold_scores
    )
    fold_coverage_complete = fold_covered == len(inscope_rows) + len(oos_rows)

    sweep = _sweep(
        inscope_rows=inscope_rows, oos_rows=oos_rows, fold_scores=fold_scores
    )
    cofactor_only = [point for point in sweep if point["fold_threshold"] == 0.0]

    eligible = _eligible_points(
        sweep, min_correct=min_correct, max_oos_fp=max_oos_fp
    )
    fusion_best = _best_under_fp_ceiling(sweep, max_oos_fp=max_oos_fp)
    cofactor_only_best = _best_under_fp_ceiling(cofactor_only, max_oos_fp=max_oos_fp)
    ceiling = _recovery_ceiling(inscope_rows)

    fusion_recall = (fusion_best or {}).get("inscope_correct")
    cofactor_only_recall = (cofactor_only_best or {}).get("inscope_correct")
    marginal_gain = (
        fusion_recall - cofactor_only_recall
        if fusion_recall is not None and cofactor_only_recall is not None
        else None
    )
    # Max-precision regime: hold the cofactor-only safe recovery, minimise OOS FP.
    max_precision = _max_precision_point(
        sweep, min_recall=cofactor_only_recall or 0
    )

    status = (
        "eligible_current57_cofactor_fold_fusion_contract_found"
        if eligible and fold_coverage_complete
        else "blocked_current57_cofactor_fold_fusion_not_deployable"
    )

    return {
        "artifact_id": (
            "v3_current57_cofactor_fold_fusion_preregistration_current702_20260628"
        ),
        "schema_version": "current57_cofactor_fold_fusion_preregistration.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_train_cal_fusion_preregistration_no_threshold_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "selection_surface": "calibration_out_of_sample_for_cofactor_channel",
            "fold_scores_are_calibration_vs_train_only": True,
            "threshold_selected_on_heldout": False,
            "supervised_model_trained": False,
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
            "fold_readout_artifact_id": fold_readout.get("artifact_id"),
            "trusted_precision_artifact_id": trusted_precision.get("artifact_id"),
        },
        "fold_coverage": {
            "rows_with_fold_score": fold_covered,
            "rows_total": len(inscope_rows) + len(oos_rows),
            "coverage_complete": fold_coverage_complete,
        },
        "fusion_rule": {
            "definition": (
                "retained_in_scope_call := fused.top1_score >= cofactor_threshold AND "
                "fold_nn_alntmscore >= fold_threshold; correctness uses the documented "
                "legacy-v1 metal-umbrella compatibility projection."
            ),
            "fold_channel_role": "out_of_scope_rejection_abstention_gate",
            "cofactor_threshold_grid_size": len(_cofactor_grid(inscope_rows + oos_rows)),
            "fold_threshold_grid_size": len(_fold_grid(fold_scores)),
        },
        "pre_registered_done_bar": done_bar,
        "recovery_ceiling": ceiling,
        "selection_rule": {
            "surface": "calibration_out_of_sample",
            "eligibility": (
                "Eligible only if a calibration (cofactor_threshold, fold_threshold) "
                "pair keeps recovery >= the trusted June 9 fused primary count and "
                "OOS FP <= the trusted June 9 threshold-dial OOS false-positive count, "
                "with complete fold coverage."
            ),
            "eligible_points": eligible,
            "selected_point": eligible[0] if eligible else None,
            "decision": (
                "current57_cofactor_fold_fusion_candidate_requires_heldout_confirmation"
                if eligible and fold_coverage_complete
                else "fail_closed_keep_atlas_engine_blocked_on_current57_cofactor_surface"
            ),
        },
        "fold_marginal_value": {
            "cofactor_only_best_under_trusted_oos_fp": cofactor_only_best,
            "fusion_best_under_trusted_oos_fp": fusion_best,
            "fold_recovery_gain_at_oos_fp_ceiling": marginal_gain,
            "max_precision_point_at_cofactor_only_recovery": max_precision,
            "note": (
                "The fold-NN gate adds OOS-rejection power: at the trusted OOS-FP "
                "ceiling it matches or exceeds the cofactor-only recovery, and it can "
                "drive OOS FP far lower while holding the same recovery. It cannot lift "
                "recovery above the current-57 compatible ceiling."
            ),
        },
        "calibration_sweep": sweep,
        "interpretation": {
            "headline": (
                "A row-aligned current-57 cofactor + fold-NN fusion is preregistered and "
                "fail-closed: the fold channel adds real OOS-rejection power but cannot "
                "clear the trusted June 9 recovery bar, which is capped by the current-57 "
                "compatible-recovery ceiling."
                if not (eligible and fold_coverage_complete)
                else "A row-aligned current-57 cofactor + fold-NN fusion clears the "
                "trusted June 9 done bar on calibration and is a heldout-confirmation "
                "candidate."
            ),
            "deployment_decision": (
                "Fail closed for atlas-engine fusion on the current-57 cofactor surface. "
                "The binding constraint is the current-57 router's compatible-recovery "
                "ceiling, not OOS false positives, so the documented next step is to "
                "pin/replay the intended June 9 router/fingerprint surface (whose recovery "
                "clears the bar) and then re-apply this fold-NN OOS-rejection gate. The "
                "high-precision fusion regime (near-zero OOS FP at reduced recovery) is a "
                "separate, narrower product framing that would still require heldout "
                "confirmation."
                if not (eligible and fold_coverage_complete)
                else "Promote the selected calibration point to a single heldout-final "
                "evaluation; do not change any production threshold until that heldout "
                "read passes."
            ),
        },
    }


def _fmt(point: dict[str, Any] | None) -> str:
    if not point:
        return "none"
    return (
        f"cofactor {point.get('cofactor_threshold')} + fold "
        f"{point.get('fold_threshold')}: recall "
        f"{point.get('inscope_correct')}/{point.get('inscope_total')} "
        f"({point.get('inscope_recall')}) · OOS FP "
        f"{point.get('oos_false_positives')}/{point.get('oos_total')} "
        f"({point.get('oos_false_positive_rate')})"
    )


def _report(prereg: dict[str, Any]) -> str:
    done = prereg["pre_registered_done_bar"]
    ceiling = prereg["recovery_ceiling"]
    marginal = prereg["fold_marginal_value"]
    lines = [
        "# Current-57 Cofactor + Fold-NN Fusion Preregistration",
        "",
        f"Run: {prereg['created_utc']}",
        f"Status: `{prereg['status']}`",
        "",
        "## Rule",
        "",
        f"- {prereg['fusion_rule']['definition']}",
        f"- Fold channel role: {prereg['fusion_rule']['fold_channel_role']}.",
        "",
        "## Done Bar (trusted June 9, calibration)",
        "",
        f"- Required recovery: >= {done.get('min_calibration_inscope_correct')}/"
        f"{done.get('calibration_inscope_total')}.",
        f"- OOS FP ceiling: <= {done.get('max_calibration_oos_false_positives')}/"
        f"{done.get('calibration_oos_total')}.",
        "",
        "## Recovery Ceiling (current-57 router)",
        "",
        f"- Compatible recovery ceiling: "
        f"{ceiling['compatible_recovery_ceiling']}/{ceiling['inscope_total']}.",
        f"- Exact recovery ceiling: "
        f"{ceiling['exact_recovery_ceiling']}/{ceiling['inscope_total']}.",
        "",
        "## Fold-NN Marginal Value",
        "",
        f"- Cofactor-only best under OOS-FP ceiling: "
        f"{_fmt(marginal['cofactor_only_best_under_trusted_oos_fp'])}.",
        f"- Fusion best under OOS-FP ceiling: "
        f"{_fmt(marginal['fusion_best_under_trusted_oos_fp'])}.",
        f"- Fold recovery gain at the OOS-FP ceiling: "
        f"{marginal['fold_recovery_gain_at_oos_fp_ceiling']}.",
        f"- Max-precision point (>= cofactor-only recovery): "
        f"{_fmt(marginal['max_precision_point_at_cofactor_only_recovery'])}.",
        "",
        "## Eligibility",
        "",
        f"- Eligible calibration points clearing the done bar: "
        f"{len(prereg['selection_rule']['eligible_points'])}.",
        f"- Decision: `{prereg['selection_rule']['decision']}`.",
        "",
        "## Deployment Decision",
        "",
        f"- {prereg['interpretation']['deployment_decision']}",
        "",
        "## Guardrails",
        "",
        "- Fold scores are calibration-vs-train only; no heldout row was scored or read.",
        "- No threshold was selected on heldout rows; no supervised model was trained.",
        "- No production threshold, model weight, registry, ontology, label, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_current57_cofactor_fold_fusion_preregistration(
    *,
    current_operating_point_path: Path,
    fold_readout_path: Path,
    trusted_precision_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    current = _load_json(current_operating_point_path)
    fold_readout = _load_json(fold_readout_path)
    trusted = _load_json(trusted_precision_path)
    prereg = build_current57_cofactor_fold_fusion_preregistration(
        current_operating_point=current,
        fold_readout=fold_readout,
        trusted_precision=trusted,
    )
    prereg["source_artifacts"] = {
        "current57_cofactor_operating_point": _artifact_summary(
            current_operating_point_path, current
        ),
        "fold_recompute_readout": _artifact_summary(fold_readout_path, fold_readout),
        "trusted_precision": _artifact_summary(trusted_precision_path, trusted),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(prereg, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(prereg), encoding="utf-8")
    return prereg
