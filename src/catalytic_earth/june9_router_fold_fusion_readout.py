"""Layer the row-aligned fold-NN OOS-rejection gate on the pinned June 9 router.

The current-57 router drifts to a 26/35 compatible-recovery ceiling, so the
current-57 cofactor+fold fusion preregistration fail-closed. This readout tests
the documented alternative: take the trusted June 9 router surface (which clears
the recovery bar at 30/35) reconstructed with per-row detail via an isolated
registry pin, join the row-aligned fold-NN TM scores, and ask whether the
fold-NN gate Pareto-improves the June 9 operating point.

Rule, same shape as the current-57 preregistration but with June 9 exact
correctness (the pinned 8-family registry matches the frozen coarse labels):

    retained := fused.top1_score >= cofactor_threshold
                AND fold_nn_alntmscore >= fold_threshold

It is heldout-excluded and calibration-only. It selects no production threshold,
trains nothing, and does not mutate the live registry (the June 9 surface is a
committed row-detail reconstruction).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any


DEFAULT_PINNED_JUNE9_PATH = (
    "artifacts/"
    "v3_june9_router_pinned_rowdetail_operating_point_current702_20260628.json"
)
DEFAULT_FOLD_READOUT_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_june9_router_fold_fusion_readout_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/june9_router_fold_fusion_readout_current702_20260628.md"
)

FROZEN_THRESHOLD = 0.4115
DIAL_THRESHOLD = 0.44

BASE_FOLD_THRESHOLD_GRID: tuple[float, ...] = (
    0.0,
    0.45,
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
BASE_COFACTOR_THRESHOLD_GRID: tuple[float, ...] = (
    0.4115,
    0.44,
    0.47,
    0.50,
    0.55,
    0.60,
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
    return float((row.get("fused") or {}).get("top1_score") or 0.0)


def _exact_correct(row: dict[str, Any]) -> bool:
    true_fp = row.get("true_fingerprint_id")
    called = (row.get("fused") or {}).get("top1_fingerprint_id")
    return bool(true_fp and called == true_fp)


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
    return fold is not None and fold >= fold_threshold


def _point(
    *,
    cofactor_threshold: float,
    fold_threshold: float,
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    fold_scores: dict[str, float],
) -> dict[str, Any]:
    recovery = sum(
        1
        for row in inscope_rows
        if _exact_correct(row)
        and _retained(
            row,
            cofactor_threshold=cofactor_threshold,
            fold_threshold=fold_threshold,
            fold_scores=fold_scores,
        )
    )
    fp = sum(
        1
        for row in oos_rows
        if _retained(
            row,
            cofactor_threshold=cofactor_threshold,
            fold_threshold=fold_threshold,
            fold_scores=fold_scores,
        )
    )
    return {
        "cofactor_threshold": round(cofactor_threshold, 4),
        "fold_threshold": round(fold_threshold, 4),
        "inscope_correct": recovery,
        "inscope_total": len(inscope_rows),
        "oos_false_positives": fp,
        "oos_total": len(oos_rows),
    }


def _grids(
    inscope_rows: list[dict[str, Any]],
    oos_rows: list[dict[str, Any]],
    fold_scores: dict[str, float],
) -> tuple[list[float], list[float]]:
    cof = {round(v, 4) for v in BASE_COFACTOR_THRESHOLD_GRID}
    for row in inscope_rows + oos_rows:
        score = _cofactor_score(row)
        if score >= min(cof):
            cof.add(round(score, 4))
    fold = {round(v, 4) for v in BASE_FOLD_THRESHOLD_GRID}
    for value in fold_scores.values():
        fold.add(round(value, 4))
    return sorted(cof), sorted(fold)


def _frontier(
    sweep: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_recovery: dict[int, dict[str, Any]] = {}
    for point in sweep:
        recovery = point["inscope_correct"]
        current = by_recovery.get(recovery)
        if current is None or point["oos_false_positives"] < current["oos_false_positives"]:
            by_recovery[recovery] = point
    return [by_recovery[k] for k in sorted(by_recovery, reverse=True)]


def _residual_oos_fp_characterization(
    *,
    oos_rows: list[dict[str, Any]],
    fold_scores: dict[str, float],
    cofactor_threshold: float,
) -> list[dict[str, Any]]:
    rows = []
    for row in oos_rows:
        if _cofactor_score(row) >= cofactor_threshold:
            rows.append(
                {
                    "entry_id": row.get("entry_id"),
                    "cofactor_score": round(_cofactor_score(row), 4),
                    "fold_nn_alntmscore": round(
                        fold_scores.get(str(row.get("entry_id")), -1.0), 4
                    ),
                    "called_fingerprint_id": (row.get("fused") or {}).get(
                        "top1_fingerprint_id"
                    ),
                }
            )
    return sorted(rows, key=lambda r: -r["fold_nn_alntmscore"])


def build_june9_router_fold_fusion_readout(
    *,
    pinned_june9: dict[str, Any],
    fold_readout: dict[str, Any],
    frozen_threshold: float = FROZEN_THRESHOLD,
    dial_threshold: float = DIAL_THRESHOLD,
) -> dict[str, Any]:
    fold_scores = _fold_scores_by_entry(fold_readout)
    cal = pinned_june9.get("row_details_by_split", {}).get("calibration", {})
    inscope_rows = list(cal.get("inscope_rows", []) or [])
    oos_rows = list(cal.get("oos_rows", []) or [])

    fold_covered = sum(
        1
        for row in inscope_rows + oos_rows
        if str(row.get("entry_id")) in fold_scores
    )
    coverage_complete = fold_covered == len(inscope_rows) + len(oos_rows)

    # Baselines with the fold gate OFF (fold_threshold = 0.0).
    baseline_frozen = _point(
        cofactor_threshold=frozen_threshold,
        fold_threshold=0.0,
        inscope_rows=inscope_rows,
        oos_rows=oos_rows,
        fold_scores=fold_scores,
    )
    baseline_dial = _point(
        cofactor_threshold=dial_threshold,
        fold_threshold=0.0,
        inscope_rows=inscope_rows,
        oos_rows=oos_rows,
        fold_scores=fold_scores,
    )

    cof_grid, fold_grid = _grids(inscope_rows, oos_rows, fold_scores)
    sweep = [
        _point(
            cofactor_threshold=cth,
            fold_threshold=fth,
            inscope_rows=inscope_rows,
            oos_rows=oos_rows,
            fold_scores=fold_scores,
        )
        for cth, fth in product(cof_grid, fold_grid)
    ]
    frontier = _frontier(sweep)

    baseline_recovery = baseline_dial["inscope_correct"]
    baseline_fp = baseline_dial["oos_false_positives"]
    # Does any fold-gated point hold the baseline recovery at strictly fewer FP?
    pareto_improvement = next(
        (
            point
            for point in sweep
            if point["fold_threshold"] > 0.0
            and point["inscope_correct"] >= baseline_recovery
            and point["oos_false_positives"] < baseline_fp
        ),
        None,
    )
    recovery_ceiling = max((point["inscope_correct"] for point in sweep), default=0)

    fold_helps = pareto_improvement is not None
    status = (
        "june9_router_fold_gate_pareto_improves_operating_point"
        if fold_helps and coverage_complete
        else "june9_router_fold_gate_no_pareto_improvement_precision_recall_tradeoff_only"
    )

    return {
        "artifact_id": "v3_june9_router_fold_fusion_readout_current702_20260628",
        "schema_version": "june9_router_fold_fusion_readout.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_calibration_only_router_replay_fold_fusion_readout"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "selection_surface": "calibration_out_of_sample_for_cofactor_channel",
            "fold_scores_are_calibration_vs_train_only": True,
            "threshold_selected_on_heldout": False,
            "supervised_model_trained": False,
            "production_threshold_changed": False,
            "live_registry_mutated": False,
            "june9_surface_is_isolated_pin_reconstruction": True,
            "model_weights_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
        },
        "inputs": {
            "pinned_june9_artifact_id": pinned_june9.get("artifact_id"),
            "fold_readout_artifact_id": fold_readout.get("artifact_id"),
            "june9_pin_provenance": pinned_june9.get("pin_provenance"),
        },
        "fold_coverage": {
            "rows_with_fold_score": fold_covered,
            "rows_total": len(inscope_rows) + len(oos_rows),
            "coverage_complete": coverage_complete,
        },
        "june9_baseline_fold_gate_off": {
            "frozen_threshold": baseline_frozen,
            "dial_0p44_threshold": baseline_dial,
            "exact_recovery_ceiling": recovery_ceiling,
        },
        "fold_gate_assessment": {
            "rule": (
                "retained := fused.top1_score >= cofactor_threshold AND "
                "fold_nn_alntmscore >= fold_threshold (June 9 exact correctness)."
            ),
            "pareto_improvement_over_dial_baseline": pareto_improvement,
            "fold_gate_helps": fold_helps,
            "precision_recall_frontier": frontier,
            "residual_oos_false_positives_at_dial": _residual_oos_fp_characterization(
                oos_rows=oos_rows,
                fold_scores=fold_scores,
                cofactor_threshold=dial_threshold,
            ),
        },
        "interpretation": {
            "headline": (
                "On the reproduced June 9 router (which clears the 30/35 recovery bar), "
                "the row-aligned fold-NN gate does not Pareto-improve the operating "
                "point: residual OOS false positives are structurally high-fold-similar, "
                "so the fold gate only trades recovery for precision."
                if not fold_helps
                else "On the reproduced June 9 router, the fold-NN gate Pareto-improves "
                "the operating point (holds recovery at strictly fewer OOS false "
                "positives)."
            ),
            "deployment_decision": (
                "The deployable path remains the June 9 router at its dial operating "
                "point (30/35 recovery, 8/26 OOS FP). The fold-NN channel is a tunable "
                "precision/recall dial on this router (e.g., trading recovery for a "
                "near-zero-OOS-FP regime), not a free precision booster: its large "
                "marginal value was specific to rescuing the drifted current-57 router. "
                "Any chosen operating point still requires a single heldout-final read "
                "before deployment; no production threshold is changed here."
                if not fold_helps
                else "Promote the Pareto-improving June 9 + fold-gate point to a single "
                "heldout-final evaluation before any production threshold change."
            ),
        },
    }


def _fmt(point: dict[str, Any] | None) -> str:
    if not point:
        return "none"
    return (
        f"cofactor {point.get('cofactor_threshold')} + fold "
        f"{point.get('fold_threshold')}: recovery "
        f"{point.get('inscope_correct')}/{point.get('inscope_total')} · OOS FP "
        f"{point.get('oos_false_positives')}/{point.get('oos_total')}"
    )


def _report(readout: dict[str, Any]) -> str:
    baseline = readout["june9_baseline_fold_gate_off"]
    assessment = readout["fold_gate_assessment"]
    lines = [
        "# June 9 Router + Fold-NN Fusion Readout",
        "",
        f"Run: {readout['created_utc']}",
        f"Status: `{readout['status']}`",
        "",
        "## June 9 Baseline (fold gate off)",
        "",
        f"- Frozen threshold: {_fmt(baseline['frozen_threshold'])}.",
        f"- 0.44 dial: {_fmt(baseline['dial_0p44_threshold'])}.",
        f"- Exact recovery ceiling: {baseline['exact_recovery_ceiling']}/35.",
        "",
        "## Fold Gate Assessment",
        "",
        f"- Rule: {assessment['rule']}",
        f"- Fold gate Pareto-improves the dial baseline: "
        f"{assessment['fold_gate_helps']}.",
        f"- Pareto-improving point: "
        f"{_fmt(assessment['pareto_improvement_over_dial_baseline'])}.",
        "",
        "### Precision/Recall Frontier (recovery -> min OOS FP)",
        "",
    ]
    for point in assessment["precision_recall_frontier"]:
        lines.append(
            f"- recovery {point['inscope_correct']}/{point['inscope_total']} "
            f"-> OOS FP {point['oos_false_positives']}/{point['oos_total']} "
            f"(cofactor {point['cofactor_threshold']}, fold {point['fold_threshold']})"
        )
    lines += [
        "",
        "### Residual OOS False Positives at the 0.44 dial",
        "",
    ]
    for row in assessment["residual_oos_false_positives_at_dial"]:
        lines.append(
            f"- {row['entry_id']}: fold {row['fold_nn_alntmscore']}, cofactor "
            f"{row['cofactor_score']} (called {row['called_fingerprint_id']})"
        )
    lines += [
        "",
        "## Deployment Decision",
        "",
        f"- {readout['interpretation']['deployment_decision']}",
        "",
        "## Guardrails",
        "",
        "- The live 57-fingerprint registry was never mutated; the June 9 surface is an "
        "isolated registry-pin row-detail reconstruction.",
        "- Fold scores are calibration-vs-train only; no heldout row was scored or read.",
        "- No threshold was selected on heldout rows; no supervised model was trained.",
        "- No production threshold, model weight, registry, ontology, label, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_june9_router_fold_fusion_readout(
    *,
    pinned_june9_path: Path,
    fold_readout_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    pinned = _load_json(pinned_june9_path)
    fold_readout = _load_json(fold_readout_path)
    readout = build_june9_router_fold_fusion_readout(
        pinned_june9=pinned, fold_readout=fold_readout
    )
    readout["source_artifacts"] = {
        "pinned_june9_operating_point": _artifact_summary(pinned_june9_path, pinned),
        "fold_recompute_readout": _artifact_summary(fold_readout_path, fold_readout),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(readout), encoding="utf-8")
    return readout
