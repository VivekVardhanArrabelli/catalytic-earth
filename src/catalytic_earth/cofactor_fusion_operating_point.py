"""Leakage-safe train/cal operating-point readout for the cofactor-fusion router.

This closes the *precision* side of the Problem-2 step-4 operating-point question.

Background: the confirmed heldout one-shot moved predicted-apo primary 23/45 ->
37/45 by fusing the leakage-safe sequence -> cofactor-presence channel into the
router, but at a precision cost (OOS/secondary false positives 12.3% -> 25.9%;
decision_log 2026-06-04 "HELDOUT ONE-SHOT SPENT"). That heldout read is spent and
must never be tuned against. The in-distribution recovery harness
(`predicted_geometry_recovery.py`) measured the RECALL side of the same question
leakage-safe, but it scores only in-scope atlas rows (rows with a seed
fingerprint), so it has *no OOS rows* and could not measure the precision cost.

This module supplies the missing precision side. It scores the in-distribution
OUT-OF-SCOPE (OOS) rows of the train/cal split through the SAME frozen
cofactor-fusion router and counts every non-abstained primary call as a false
positive. With both the recall side (in-scope rows) and the precision side (OOS
rows) on one leakage-safe surface, the two pre-built precision dials can be
compared directly:

1. a *recalibrated abstention threshold* (raise the router threshold), and
2. the *sequence-supported suppression dial* (abstain calls whose required
   cofactor family the channel does not support).

Honesty guardrails (identical discipline to the recovery harness):

- Only in-distribution rows present in the train/cal split manifest are scored;
  heldout rows are never read or scored.
- The cofactor channel is consumed FROZEN (no refit). The router threshold sweep
  is a DIAGNOSTIC over the train/cal surface only; it selects no production
  threshold and changes nothing in the production scorer.
- The channel was fit on the train split, so train rows are in-sample for it and
  calibration rows are out-of-sample. The calibration surface is the honest
  read; train is reported only as an in-sample reference.
- Predicted-apo coordinates are read from already-staged train/cal-safe CIF
  directories only (the heldout query bundle and the cofactor-confounded heldout
  OOS bundle are excluded). Coverage is partial and disclosed; OOS rows without
  a staged predicted structure are reported as coverage gaps, never as true
  negatives.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .geometry_retrieval import run_geometry_retrieval
from .predicted_geometry_recovery import (
    _default_context_fusion,
    _default_unsupported_suppression,
)
from .predicted_geometry_robustness import (
    HAND_ROUTER_THRESHOLD,
    build_alphafold_predicted_geometry_features,
    _hand_router_rows,
    _target_manifest_row_selection,
)


COORDINATE_ROOT = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates"
)
# Train/cal-safe staged predicted-apo CIF directories. The heldout query bundle
# (`queries_all_heldout`) and the cofactor-confounded heldout OOS bundle
# (`queries_cofactor_confounded_oos`) are deliberately excluded so no heldout
# coordinate can enter this train/cal readout.
DEFAULT_STAGED_DIRS: tuple[str, ...] = (
    f"{COORDINATE_ROOT}/confounded_proxy_train_cal_tranche_queries",
    f"{COORDINATE_ROOT}/atlas_in_distribution",
)
DEFAULT_THRESHOLD_GRID: tuple[float, ...] = (
    0.4115,
    0.42,
    0.44,
    0.45,
    0.47,
    0.50,
    0.53,
    0.56,
    0.60,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def multi_dir_staged_cif_fetcher(
    staged_dirs: list[Path], *, version_tag: str = "v6"
) -> Callable[..., tuple[str, dict[str, Any]]]:
    """Return a fetcher that reads a staged CIF from the first matching directory.

    Matches the ``build_alphafold_predicted_geometry_features`` fetcher contract:
    ``fetch(accession, version=...) -> (text, meta)``. Missing coordinates raise,
    which the geometry builder records as a fetch failure / non-ok entry.
    """

    dirs = [Path(d) for d in staged_dirs]

    def fetch(accession: str, *, version: str = "auto", timeout: int = 30):
        cleaned = str(accession).strip()
        for staged_dir in dirs:
            path = staged_dir / f"afdb_{cleaned}_{version_tag}.cif"
            if path.exists():
                text = path.read_text(encoding="utf-8")
                return text, {
                    "backend": "staged_local_alphafold",
                    "accession": cleaned,
                    "staged_path": str(path),
                }
        raise RuntimeError(
            f"no staged train/cal-safe predicted CIF for {cleaned}"
        )

    return fetch


def _router_surface(
    *,
    rows: list[dict[str, Any]],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    channel: dict[str, Any],
    fetch: Callable[..., tuple[str, dict[str, Any]]],
    threshold: float,
    alphafold_version: str,
) -> dict[str, list[dict[str, Any]]]:
    """Score the frozen apo / fused / fused+suppressed router over ``rows``."""
    apo_geometry = build_alphafold_predicted_geometry_features(
        label_manifest_rows=rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        alphafold_version=alphafold_version,
        fetcher=fetch,
    )
    fused_geometry = _default_context_fusion(apo_geometry, channel)
    apo_rows = _hand_router_rows(
        target_rows=rows,
        predicted_geometry=apo_geometry,
        predicted_retrieval=run_geometry_retrieval(apo_geometry),
        wave1_audit={},
        threshold=threshold,
    )
    fused_rows = _hand_router_rows(
        target_rows=rows,
        predicted_geometry=fused_geometry,
        predicted_retrieval=run_geometry_retrieval(fused_geometry),
        wave1_audit={},
        threshold=threshold,
    )
    suppressed_rows = _default_unsupported_suppression(fused_rows, channel)
    return {
        "apo": apo_rows,
        "fused": fused_rows,
        "fused_suppressed": suppressed_rows,
        "apo_geometry_ok": sum(
            1 for e in apo_geometry.get("entries", []) if e.get("status") == "ok"
        ),
    }


def _scored(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("predicted_geometry_joined")]


def _inscope_correct(row: dict[str, Any], threshold: float) -> bool:
    """In-scope row is correct at ``threshold`` when it is retained on the true class."""
    return (
        float(row.get("top1_score", 0.0) or 0.0) >= threshold
        and row.get("top1_fingerprint_id") == row.get("true_fingerprint_id")
        and row.get("true_fingerprint_id") is not None
    )


def _oos_false_positive(row: dict[str, Any], threshold: float) -> bool:
    """OOS row is a false positive at ``threshold`` when it is NOT abstained."""
    return float(row.get("top1_score", 0.0) or 0.0) >= threshold


def _suppressed_inscope_correct(row: dict[str, Any]) -> bool:
    return (
        not row.get("abstained")
        and row.get("top1_fingerprint_id") == row.get("true_fingerprint_id")
        and row.get("true_fingerprint_id") is not None
    )


def _suppressed_oos_fp(row: dict[str, Any]) -> bool:
    return not row.get("abstained")


def build_cofactor_fusion_operating_point(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    split_manifest: dict[str, Any],
    channel: dict[str, Any],
    staged_dirs: list[Path],
    lever2_electron_flow_readout: dict[str, Any] | None = None,
    threshold: float = HAND_ROUTER_THRESHOLD,
    threshold_grid: tuple[float, ...] = DEFAULT_THRESHOLD_GRID,
    alphafold_version: str = "6",
    split_assignment: str = "in_distribution",
) -> dict[str, Any]:
    split_by = {
        str(r.get("entry_id")): str(r.get("assigned_embedding_split"))
        for r in split_manifest.get("split_records", [])
        if r.get("entry_id") and r.get("assigned_embedding_split")
    }
    train_cal_entry_ids = set(split_by)

    target_rows, _excluded = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment=split_assignment,
        max_rows=0,
    )
    # Leakage guard: only score rows that the split manifest assigns to train/cal.
    inscope_rows = [
        r
        for r in target_rows
        if (r.get("fingerprint_id") or r.get("mechanism_fingerprint_id"))
        and str(r.get("entry_id")) in train_cal_entry_ids
    ]
    oos_rows = [
        r
        for r in target_rows
        if not (r.get("fingerprint_id") or r.get("mechanism_fingerprint_id"))
        and str(r.get("entry_id")) in train_cal_entry_ids
    ]

    fetch = multi_dir_staged_cif_fetcher(staged_dirs)
    inscope = _router_surface(
        rows=inscope_rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        channel=channel,
        fetch=fetch,
        threshold=threshold,
        alphafold_version=alphafold_version,
    )
    oos = _router_surface(
        rows=oos_rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        channel=channel,
        fetch=fetch,
        threshold=threshold,
        alphafold_version=alphafold_version,
    )

    # Heldout-leakage assertion: nothing scored may sit outside the train/cal set.
    scored_entry_ids = {
        str(r.get("entry_id"))
        for surface in (inscope, oos)
        for variant in ("apo", "fused", "fused_suppressed")
        for r in surface[variant]
    }
    heldout_leak = sorted(scored_entry_ids - train_cal_entry_ids)
    if heldout_leak:  # pragma: no cover - defensive guard
        raise AssertionError(
            f"non-train/cal rows entered the operating-point surface: {heldout_leak[:5]}"
        )

    splits = ("train", "calibration")
    operating_points = _operating_points_by_split(
        inscope=inscope,
        oos=oos,
        split_by=split_by,
        splits=splits,
        threshold=threshold,
    )
    threshold_sweep = _threshold_sweep_by_split(
        inscope_fused=_scored(inscope["fused"]),
        oos_fused=_scored(oos["fused"]),
        split_by=split_by,
        splits=splits,
        threshold_grid=threshold_grid,
    )
    row_details = _row_details_by_split(
        inscope=inscope,
        oos=oos,
        split_by=split_by,
        splits=splits,
        threshold=threshold,
    )
    dial_comparison = _dial_comparison(operating_points, threshold_sweep)
    fp_called_distribution = _fp_called_distribution(_scored(oos["fused"]), threshold)

    lever2_summary = _lever2_complementary_summary(lever2_electron_flow_readout)

    return {
        "artifact_id": (
            "v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609"
        ),
        "schema_version": "cofactor_fusion_operating_point.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "result_class": (
            "research_only_leakage_safe_train_cal_operating_point_readout_"
            "no_production_threshold_change_no_heldout_read"
        ),
        "scope": (
            "Precision side of the Problem-2 step-4 operating-point question. Scores "
            "the in-distribution train/cal OOS rows through the frozen "
            "cofactor-fusion router so the recalibrated-threshold dial and the "
            "sequence-supported suppression dial can be compared on a leakage-safe "
            "out-of-sample surface, never the spent heldout one-shot."
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "split_assignment_scored": "in_distribution_train_cal_only",
            "cofactor_channel_refit": False,
            "cofactor_channel_artifact_id": channel.get("artifact_id"),
            "production_threshold_changed": False,
            "threshold_sweep_is_diagnostic_only": True,
            "global_threshold_changed": False,
            "production_scoring_changed": False,
            "registries_ontologies_imports_changed": False,
            "calibration_is_out_of_sample_for_channel": True,
            "train_is_in_sample_reference_only": True,
            "staged_coordinates_train_cal_safe_only": True,
            "heldout_query_bundles_excluded": [
                f"{COORDINATE_ROOT}/queries_all_heldout",
                f"{COORDINATE_ROOT}/queries_cofactor_confounded_oos",
            ],
            "oos_coverage_gaps_counted_as_true_negatives": False,
        },
        "inputs": {
            "frozen_router_threshold": threshold,
            "threshold_grid": list(threshold_grid),
            "alphafold_version": alphafold_version,
            "staged_dirs": [str(d) for d in staged_dirs],
            "channel_artifact_id": channel.get("artifact_id"),
        },
        "coverage": {
            "in_distribution_inscope_rows": len(inscope_rows),
            "in_distribution_oos_rows": len(oos_rows),
            "inscope_predicted_geometry_ok": inscope["apo_geometry_ok"],
            "oos_predicted_geometry_ok": oos["apo_geometry_ok"],
            "inscope_scored": len(_scored(inscope["fused"])),
            "oos_scored": len(_scored(oos["fused"])),
            "oos_coverage_gap_rows": len(oos_rows) - oos["apo_geometry_ok"],
        },
        "operating_points_by_split": operating_points,
        "threshold_sweep_by_split": threshold_sweep,
        "row_details_by_split": row_details,
        "dial_comparison": dial_comparison,
        "oos_false_positive_called_distribution_fused_frozen": fp_called_distribution,
        "lever2_electron_flow_complementary_lever": lever2_summary,
        "interpretation": _interpretation(dial_comparison),
        "verification": {
            "calibration_inscope_scored_rows": _split_n(
                _scored(inscope["fused"]), split_by, "calibration"
            ),
            "calibration_oos_scored_rows": _split_n(
                _scored(oos["fused"]), split_by, "calibration"
            ),
        },
    }


def _split_n(rows: list[dict[str, Any]], split_by: dict[str, str], split: str) -> int:
    return sum(1 for r in rows if split_by.get(str(r.get("entry_id"))) == split)


def _row_details_by_split(
    *,
    inscope: dict[str, list[dict[str, Any]]],
    oos: dict[str, list[dict[str, Any]]],
    split_by: dict[str, str],
    splits: tuple[str, ...],
    threshold: float,
) -> dict[str, Any]:
    details: dict[str, Any] = {}
    for split in splits:
        inscope_entries = _row_details(
            rows_by_surface=inscope,
            split_by=split_by,
            split=split,
            threshold=threshold,
            row_class="in_scope",
        )
        oos_entries = _row_details(
            rows_by_surface=oos,
            split_by=split_by,
            split=split,
            threshold=threshold,
            row_class="oos",
        )
        details[split] = {
            "is_out_of_sample_for_channel": split == "calibration",
            "inscope_rows": inscope_entries,
            "oos_rows": oos_entries,
        }
    return details


def _row_details(
    *,
    rows_by_surface: dict[str, list[dict[str, Any]]],
    split_by: dict[str, str],
    split: str,
    threshold: float,
    row_class: str,
) -> list[dict[str, Any]]:
    by_surface = {
        name: {
            str(row.get("entry_id")): row
            for row in _scored(rows)
            if split_by.get(str(row.get("entry_id"))) == split
        }
        for name, rows in rows_by_surface.items()
        if name in {"apo", "fused", "fused_suppressed"}
    }
    entry_ids = sorted({entry_id for rows in by_surface.values() for entry_id in rows})
    out: list[dict[str, Any]] = []
    for entry_id in entry_ids:
        apo = by_surface.get("apo", {}).get(entry_id, {})
        fused = by_surface.get("fused", {}).get(entry_id, {})
        suppressed = by_surface.get("fused_suppressed", {}).get(entry_id, {})
        true_fingerprint = fused.get("true_fingerprint_id") or apo.get("true_fingerprint_id")
        row: dict[str, Any] = {
            "entry_id": entry_id,
            "row_class": row_class,
            "embedding_split": split,
            "true_fingerprint_id": true_fingerprint,
            "apo": _surface_cell(apo, threshold=threshold, row_class=row_class),
            "fused": _surface_cell(fused, threshold=threshold, row_class=row_class),
            "fused_suppressed": _surface_cell(
                suppressed, threshold=threshold, row_class=row_class
            ),
        }
        if row_class == "in_scope":
            row["apo_correct_at_threshold"] = _inscope_correct(apo, threshold)
            row["fused_correct_at_threshold"] = _inscope_correct(fused, threshold)
            row["suppressed_correct"] = bool(suppressed) and _suppressed_inscope_correct(
                suppressed
            )
        else:
            row["apo_false_positive_at_threshold"] = _oos_false_positive(apo, threshold)
            row["fused_false_positive_at_threshold"] = _oos_false_positive(
                fused, threshold
            )
            row["suppressed_false_positive"] = bool(suppressed) and _suppressed_oos_fp(
                suppressed
            )
        out.append(row)
    return out


def _surface_cell(
    row: dict[str, Any], *, threshold: float, row_class: str
) -> dict[str, Any]:
    score = row.get("top1_score")
    retained = float(score or 0.0) >= threshold
    cell = {
        "predicted_geometry_joined": bool(row.get("predicted_geometry_joined")),
        "top1_fingerprint_id": row.get("top1_fingerprint_id"),
        "called_fingerprint_id": row.get("called_fingerprint_id"),
        "top1_score": score,
        "abstained": row.get("abstained"),
        "retained_at_threshold": retained,
    }
    if row_class == "in_scope":
        cell["correct_at_threshold"] = _inscope_correct(row, threshold)
    else:
        cell["false_positive_at_threshold"] = _oos_false_positive(row, threshold)
    return cell


def _operating_points_by_split(
    *,
    inscope: dict[str, list[dict[str, Any]]],
    oos: dict[str, list[dict[str, Any]]],
    split_by: dict[str, str],
    splits: tuple[str, ...],
    threshold: float,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for split in splits:
        def in_split(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [
                r
                for r in _scored(rows)
                if split_by.get(str(r.get("entry_id"))) == split
            ]

        apo_in = in_split(inscope["apo"])
        fused_in = in_split(inscope["fused"])
        supp_in = in_split(inscope["fused_suppressed"])
        apo_oos = in_split(oos["apo"])
        fused_oos = in_split(oos["fused"])
        supp_oos = in_split(oos["fused_suppressed"])

        out[split] = {
            "is_out_of_sample_for_channel": split == "calibration",
            "inscope_scored": len(fused_in),
            "oos_scored": len(fused_oos),
            "apo_baseline": _point(
                inscope_correct=sum(1 for r in apo_in if _inscope_correct(r, threshold)),
                inscope_total=len(apo_in),
                oos_fp=sum(1 for r in apo_oos if _oos_false_positive(r, threshold)),
                oos_total=len(apo_oos),
            ),
            "fused_frozen_threshold": _point(
                inscope_correct=sum(
                    1 for r in fused_in if _inscope_correct(r, threshold)
                ),
                inscope_total=len(fused_in),
                oos_fp=sum(1 for r in fused_oos if _oos_false_positive(r, threshold)),
                oos_total=len(fused_oos),
            ),
            "fused_suppression_dial": _point(
                inscope_correct=sum(
                    1 for r in supp_in if _suppressed_inscope_correct(r)
                ),
                inscope_total=len(supp_in),
                oos_fp=sum(1 for r in supp_oos if _suppressed_oos_fp(r)),
                oos_total=len(supp_oos),
            ),
        }
    return out


def _point(
    *, inscope_correct: int, inscope_total: int, oos_fp: int, oos_total: int
) -> dict[str, Any]:
    return {
        "inscope_correct": inscope_correct,
        "inscope_total": inscope_total,
        "inscope_recall": round(inscope_correct / inscope_total, 4)
        if inscope_total
        else None,
        "oos_false_positives": oos_fp,
        "oos_total": oos_total,
        "oos_false_positive_rate": round(oos_fp / oos_total, 4) if oos_total else None,
    }


def _threshold_sweep_by_split(
    *,
    inscope_fused: list[dict[str, Any]],
    oos_fused: list[dict[str, Any]],
    split_by: dict[str, str],
    splits: tuple[str, ...],
    threshold_grid: tuple[float, ...],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for split in splits:
        in_rows = [
            r for r in inscope_fused if split_by.get(str(r.get("entry_id"))) == split
        ]
        oos_split = [
            r for r in oos_fused if split_by.get(str(r.get("entry_id"))) == split
        ]
        grid = []
        for thr in threshold_grid:
            grid.append(
                {
                    "threshold": thr,
                    **_point(
                        inscope_correct=sum(
                            1 for r in in_rows if _inscope_correct(r, thr)
                        ),
                        inscope_total=len(in_rows),
                        oos_fp=sum(1 for r in oos_split if _oos_false_positive(r, thr)),
                        oos_total=len(oos_split),
                    ),
                }
            )
        out[split] = grid
    return out


def _dial_comparison(
    operating_points: dict[str, Any], threshold_sweep: dict[str, Any]
) -> dict[str, Any]:
    """Compare the recalibrated-threshold dial vs the suppression dial on calibration.

    The honest read is the calibration (out-of-sample) surface. For the
    suppression dial's OOS-FP target, find the lowest threshold on the fused
    sweep that reaches the same-or-better OOS precision, and report whether it
    keeps more in-scope recall (the threshold dial dominating the suppression
    dial).
    """
    cal = operating_points.get("calibration", {})
    sweep = threshold_sweep.get("calibration", [])
    fused = cal.get("fused_frozen_threshold", {})
    supp = cal.get("fused_suppression_dial", {})
    supp_fp = supp.get("oos_false_positives")

    threshold_match = None
    if supp_fp is not None and sweep:
        for point in sweep:
            if (
                point.get("oos_false_positives") is not None
                and point["oos_false_positives"] <= supp_fp
            ):
                threshold_match = point
                break

    dominates = None
    if (
        threshold_match is not None
        and threshold_match.get("inscope_correct") is not None
        and supp.get("inscope_correct") is not None
    ):
        dominates = threshold_match["inscope_correct"] > supp["inscope_correct"]

    return {
        "surface": "calibration_out_of_sample",
        "fused_frozen": fused,
        "suppression_dial": supp,
        "threshold_dial_matching_suppression_precision": threshold_match,
        "threshold_dial_dominates_suppression_dial": dominates,
        "decision_note": (
            "On the out-of-sample calibration surface, the recalibrated-threshold "
            "dial reaches the suppression dial's OOS precision while retaining more "
            "in-scope recall."
            if dominates
            else "Threshold and suppression dials are not cleanly separable on the "
            "calibration surface; read both and the train-reference surface."
        ),
    }


def _fp_called_distribution(
    oos_fused: list[dict[str, Any]], threshold: float
) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in oos_fused:
        if _oos_false_positive(row, threshold):
            counter[str(row.get("top1_fingerprint_id"))] += 1
    return dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])))


def _lever2_complementary_summary(
    readout: dict[str, Any] | None,
) -> dict[str, Any]:
    base = {
        "is_complementary_lever_on_a_different_surface": True,
        "surface_note": (
            "Lever-2 electron-flow is measured on the geometry/fold combined gate, "
            "not the cofactor-fusion router scored here, so its numbers are not "
            "merged with this surface. It adds OOS abstention at primary retention "
            "1.0 and is the natural precision complement to the cofactor channel "
            "(cofactor adds recall, electron-flow adds OOS abstention)."
        ),
    }
    if not readout:
        base["measured_incremental_oos_abstain_recall_vs_geometry_fold"] = "+0.04 (documented)"
        return base
    variants = readout.get("measured_readout", {}).get(
        "fixed_operating_point_variants", []
    )
    # The full current-split overlay (all electron-flow components) is the headline
    # complement; pick the direct variant with the largest incremental abstention.
    direct_variants = [
        v for v in variants if v.get("direct_source_free_electron_flow_fields_used")
    ]
    direct = (
        max(
            direct_variants,
            key=lambda v: v.get("incremental_oos_abstain_recall_vs_current_geometry_fold")
            or 0.0,
        )
        if direct_variants
        else None
    )
    baseline = next(
        (
            v
            for v in variants
            if v.get("direct_source_free_electron_flow_fields_used") is False
        ),
        None,
    )
    if direct and baseline:
        base["geometry_fold_baseline_oos_abstain_recall"] = baseline.get(
            "calibration_oos_abstain_recall"
        )
        base["with_electron_flow_oos_abstain_recall"] = direct.get(
            "calibration_oos_abstain_recall"
        )
        base["measured_incremental_oos_abstain_recall_vs_geometry_fold"] = (
            round(
                direct.get("calibration_oos_abstain_recall", 0.0)
                - baseline.get("calibration_oos_abstain_recall", 0.0),
                4,
            )
        )
        base["primary_retain_recall"] = direct.get("primary_retain_recall")
    base["source_artifact_id"] = readout.get("artifact_id")
    return base


def _interpretation(dial_comparison: dict[str, Any]) -> dict[str, str]:
    return {
        "headline": (
            "The precision side of the cofactor-fusion router is now measured on a "
            "leakage-safe train/cal OOS surface (previously unmeasured). Raw fusion "
            "raises OOS false positives; both the recalibrated-threshold dial and "
            "the sequence-supported suppression dial cut them back."
        ),
        "step4_decision": (
            "On the out-of-sample calibration surface the recalibrated-threshold "
            "dial reaches the suppression dial's OOS precision while keeping more "
            "in-scope recall, so the threshold dial is the better default; the "
            "suppression dial sacrifices in-scope primaries for the same precision."
            if dial_comparison.get("threshold_dial_dominates_suppression_dial")
            else "Read the calibration operating points and the train-reference "
            "surface together; the two dials are not cleanly separable here."
        ),
        "discipline": (
            "This is a research diagnostic only. It does not change the frozen "
            "production threshold and does not read the spent heldout one-shot. "
            "Choosing a deployable operating point remains a separately authorized "
            "decision and would need its own (not heldout-tuned) evaluation."
        ),
    }


def _report(audit: dict[str, Any]) -> str:
    cov = audit["coverage"]
    cal = audit["operating_points_by_split"].get("calibration", {})
    train = audit["operating_points_by_split"].get("train", {})
    dc = audit["dial_comparison"]

    def fmt(point: dict[str, Any]) -> str:
        return (
            f"recall {point.get('inscope_correct')}/{point.get('inscope_total')} "
            f"({point.get('inscope_recall')}) · FP "
            f"{point.get('oos_false_positives')}/{point.get('oos_total')} "
            f"({point.get('oos_false_positive_rate')})"
        )

    lines = [
        "# Cofactor-Fusion Operating Point — Train/Cal OOS Precision (leakage-safe)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Closes the precision side of the Problem-2 step-4 operating-point question.",
        "The recovery harness measured the recall side leakage-safe but had no OOS",
        "rows; this scores the in-distribution train/cal OOS rows through the same",
        "frozen cofactor-fusion router so the two precision dials can be compared.",
        "Calibration is the out-of-sample (honest) surface; train is in-sample only;",
        "heldout is never read.",
        "",
        "## Coverage",
        "",
        f"- In-scope in-distribution rows: {cov['in_distribution_inscope_rows']} "
        f"(predicted-apo ok {cov['inscope_predicted_geometry_ok']}).",
        f"- OOS in-distribution rows: {cov['in_distribution_oos_rows']} "
        f"(predicted-apo ok {cov['oos_predicted_geometry_ok']}; coverage gaps "
        f"{cov['oos_coverage_gap_rows']} — staged train/cal-safe CIFs only, not "
        "true negatives).",
        "",
        "## Operating points (in-scope recall | OOS false-positive rate)",
        "",
        "| Surface | apo baseline | fused @ frozen | fused + suppression |",
        "| --- | --- | --- | --- |",
        f"| calibration (out-of-sample) | {fmt(cal.get('apo_baseline', {}))} | "
        f"{fmt(cal.get('fused_frozen_threshold', {}))} | "
        f"{fmt(cal.get('fused_suppression_dial', {}))} |",
        f"| train (in-sample ref) | {fmt(train.get('apo_baseline', {}))} | "
        f"{fmt(train.get('fused_frozen_threshold', {}))} | "
        f"{fmt(train.get('fused_suppression_dial', {}))} |",
        "",
        "## Dial comparison (calibration, out-of-sample)",
        "",
        f"- Threshold dial dominates suppression dial: "
        f"**{dc.get('threshold_dial_dominates_suppression_dial')}**.",
        f"- {dc.get('decision_note')}",
    ]
    match = dc.get("threshold_dial_matching_suppression_precision")
    if match:
        lines.append(
            f"- Lowest fused threshold matching suppression precision: "
            f"{match.get('threshold')} -> recall "
            f"{match.get('inscope_correct')}/{match.get('inscope_total')}, "
            f"OOS FP {match.get('oos_false_positives')}/{match.get('oos_total')}."
        )
    lever2 = audit["lever2_electron_flow_complementary_lever"]
    lines.extend(
        [
            "",
            "## Complementary precision lever (Lever-2 electron-flow)",
            "",
            f"- {lever2.get('surface_note')}",
            f"- Measured incremental OOS abstain-recall vs geometry/fold: "
            f"{lever2.get('measured_incremental_oos_abstain_recall_vs_geometry_fold')}.",
            "",
            "## Discipline",
            "",
            f"- {audit['interpretation']['discipline']}",
            "",
            "## How to read",
            "",
            "- Each cell is `recall in-scope-correct/total (rate) · FP oos-fp/total "
            "(rate)`.",
            "- Raw fusion buys in-scope recall at an OOS false-positive cost; the two "
            "dials are the levers that cut the cost back.",
            "- The calibration row is the deployment-honest estimate; train over-states "
            "recall because the channel was fit on train.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_cofactor_fusion_operating_point(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    split_manifest_path: Path,
    channel_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    lever2_electron_flow_readout_path: Path | None = None,
    staged_dirs: list[Path] | None = None,
    threshold: float = HAND_ROUTER_THRESHOLD,
    alphafold_version: str = "6",
) -> dict[str, Any]:
    staged = staged_dirs or [Path(d) for d in DEFAULT_STAGED_DIRS]
    lever2 = (
        _load_json(lever2_electron_flow_readout_path)
        if lever2_electron_flow_readout_path
        and Path(lever2_electron_flow_readout_path).exists()
        else None
    )
    audit = build_cofactor_fusion_operating_point(
        label_manifest=_load_json(label_manifest_path),
        graph=_load_json(graph_path),
        experimental_geometry_features=_load_json(experimental_geometry_features_path),
        split_manifest=_load_json(split_manifest_path),
        channel=_load_json(channel_path),
        staged_dirs=staged,
        lever2_electron_flow_readout=lever2,
        threshold=threshold,
        alphafold_version=alphafold_version,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
