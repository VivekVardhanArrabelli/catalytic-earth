"""Row-alignment audit for current-57 cofactor/fold cached fusion.

The current-57 cofactor precision rerun and the older cached Fold/TM contracts
were built on different row-level surfaces. This audit prevents an atlas-engine
fusion readout from silently joining mostly non-overlapping train/cal rows.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_precision_contract import LEGACY_V1_COMPATIBILITY


DEFAULT_CURRENT57_OPERATING_POINT_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_"
    "20260628_current57_rerun.json"
)
DEFAULT_FOLD_INSCOPE_CONTRACT_PATH = (
    "artifacts/"
    "v3_fold_augmented_abstention_threshold_contract_current702_20260601.json"
)
DEFAULT_FOLD_OOS_CONTRACT_PATH = (
    "artifacts/"
    "v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_"
    "current702_20260603.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/"
    "v3_current57_cofactor_fold_alignment_audit_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/current57_cofactor_fold_alignment_audit_current702_20260628.md"
)

DEFAULT_MIN_CALIBRATION_INSCOPE_OVERLAP_FRACTION = 0.9
DEFAULT_MIN_CALIBRATION_OOS_OVERLAP_FRACTION = 0.9


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


def _rows(
    current57_operating_point: dict[str, Any], *, split: str, row_class: str
) -> list[dict[str, Any]]:
    details = current57_operating_point.get("row_details_by_split", {}).get(split, {})
    key = "inscope_rows" if row_class == "inscope" else "oos_rows"
    return list(details.get(key, []) or [])


def _fold_inscope_scores(fold_inscope_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("entry_id")): row
        for row in fold_inscope_contract.get("calibration_row_scores", []) or []
        if row.get("entry_id")
    }


def _fold_oos_scores(fold_oos_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("entry_id")): row
        for row in fold_oos_contract.get("calibration_oos_negative_row_scores", []) or []
        if row.get("entry_id")
    }


def _overlap_summary(
    *,
    current_rows: list[dict[str, Any]],
    fold_scores: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    current_ids = [str(row.get("entry_id")) for row in current_rows if row.get("entry_id")]
    current_set = set(current_ids)
    fold_set = set(fold_scores)
    overlap = sorted(current_set & fold_set)
    missing = sorted(current_set - fold_set)
    extra = sorted(fold_set - current_set)
    total = len(current_set)
    return {
        "current57_rows": total,
        "cached_fold_rows": len(fold_set),
        "overlap_rows": len(overlap),
        "overlap_fraction": round(len(overlap) / total, 4) if total else None,
        "overlap_entry_ids": overlap,
        "missing_current57_entry_ids": missing,
        "cached_fold_rows_not_on_current57_surface_count": len(extra),
        "cached_fold_rows_not_on_current57_surface_entry_ids": extra,
    }


def _fold_threshold(fold_inscope_contract: dict[str, Any]) -> float | None:
    primary = fold_inscope_contract.get("primary_channel_readout", {})
    selected = primary.get("selected_at_90pct_calibration_in_scope_retention", {})
    value = selected.get("threshold")
    return float(value) if value is not None else None


def _cofactor_score(row: dict[str, Any]) -> float:
    return float(row.get("fused", {}).get("top1_score") or 0.0)


def _fold_score(row: dict[str, Any] | None, channel: str) -> float | None:
    if not row:
        return None
    value = (row.get("channel_scores") or {}).get(channel)
    return float(value) if value is not None else None


def _compatible(row: dict[str, Any]) -> bool:
    true = row.get("true_fingerprint_id")
    called = row.get("fused", {}).get("top1_fingerprint_id")
    if not true or not called:
        return False
    return called == true or called in LEGACY_V1_COMPATIBILITY.get(true, ())


def _overlap_only_fixed_gate_probe(
    *,
    current57_operating_point: dict[str, Any],
    fold_inscope_scores: dict[str, dict[str, Any]],
    fold_oos_scores: dict[str, dict[str, Any]],
    fold_threshold: float | None,
    channel: str = "combined_mean_geometry_fold",
) -> dict[str, Any]:
    cal_inscope = _rows(current57_operating_point, split="calibration", row_class="inscope")
    cal_oos = _rows(current57_operating_point, split="calibration", row_class="oos")
    if fold_threshold is None:
        return {
            "interpretable": False,
            "reason": "fold_threshold_missing",
        }

    retained_correct = []
    retained_oos = []
    overlap_inscope = []
    overlap_oos = []
    for row in cal_inscope:
        fold_row = fold_inscope_scores.get(str(row.get("entry_id")))
        score = _fold_score(fold_row, channel)
        if score is None:
            continue
        overlap_inscope.append(str(row.get("entry_id")))
        if _cofactor_score(row) >= 0.4115 and score >= fold_threshold and _compatible(row):
            retained_correct.append(str(row.get("entry_id")))
    for row in cal_oos:
        fold_row = fold_oos_scores.get(str(row.get("entry_id")))
        score = _fold_score(fold_row, channel)
        if score is None:
            continue
        overlap_oos.append(str(row.get("entry_id")))
        if _cofactor_score(row) >= 0.4115 and score >= fold_threshold:
            retained_oos.append(str(row.get("entry_id")))

    return {
        "interpretable": bool(overlap_inscope and overlap_oos),
        "interpretation_limit": (
            "Overlap-only counts are diagnostic, not a selection rule, unless both "
            "calibration in-scope and OOS overlap gates pass."
        ),
        "channel": channel,
        "cofactor_threshold": 0.4115,
        "fold_threshold": fold_threshold,
        "overlap_inscope_rows": len(overlap_inscope),
        "overlap_oos_rows": len(overlap_oos),
        "compatible_inscope_correct_retained_on_overlap": len(retained_correct),
        "oos_false_positives_retained_on_overlap": len(retained_oos),
        "compatible_inscope_correct_entry_ids": retained_correct,
        "oos_false_positive_entry_ids": retained_oos,
    }


def build_current57_cofactor_fold_alignment_audit(
    *,
    current57_operating_point: dict[str, Any],
    fold_inscope_contract: dict[str, Any],
    fold_oos_contract: dict[str, Any],
    min_calibration_inscope_overlap_fraction: float = DEFAULT_MIN_CALIBRATION_INSCOPE_OVERLAP_FRACTION,
    min_calibration_oos_overlap_fraction: float = DEFAULT_MIN_CALIBRATION_OOS_OVERLAP_FRACTION,
) -> dict[str, Any]:
    inscope_scores = _fold_inscope_scores(fold_inscope_contract)
    oos_scores = _fold_oos_scores(fold_oos_contract)

    calibration_inscope = _overlap_summary(
        current_rows=_rows(
            current57_operating_point, split="calibration", row_class="inscope"
        ),
        fold_scores=inscope_scores,
    )
    calibration_oos = _overlap_summary(
        current_rows=_rows(current57_operating_point, split="calibration", row_class="oos"),
        fold_scores=oos_scores,
    )
    train_inscope = _overlap_summary(
        current_rows=_rows(current57_operating_point, split="train", row_class="inscope"),
        fold_scores={},
    )
    train_oos = _overlap_summary(
        current_rows=_rows(current57_operating_point, split="train", row_class="oos"),
        fold_scores={},
    )

    inscope_fraction = calibration_inscope.get("overlap_fraction") or 0.0
    oos_fraction = calibration_oos.get("overlap_fraction") or 0.0
    alignment_ready = (
        inscope_fraction >= min_calibration_inscope_overlap_fraction
        and oos_fraction >= min_calibration_oos_overlap_fraction
    )
    status = (
        "current57_cofactor_fold_cached_surface_aligned_ready"
        if alignment_ready
        else "blocked_cached_fold_surface_not_row_aligned_with_current57_cofactor_surface"
    )

    return {
        "artifact_id": "v3_current57_cofactor_fold_alignment_audit_current702_20260628",
        "schema_version": "current57_cofactor_fold_alignment_audit.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_cached_surface_alignment_audit_no_new_scores_no_fusion"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "new_foldseek_or_tm_scores_computed": False,
            "production_threshold_changed": False,
            "model_weights_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
            "cached_surface_fusion_authorized": alignment_ready,
        },
        "alignment_gate": {
            "surface": "calibration_train_cal_only_current57_cofactor_vs_cached_fold_contracts",
            "min_calibration_inscope_overlap_fraction": min_calibration_inscope_overlap_fraction,
            "min_calibration_oos_overlap_fraction": min_calibration_oos_overlap_fraction,
            "passed": alignment_ready,
            "decision": (
                "cached_current57_cofactor_fold_fusion_can_be_preregistered"
                if alignment_ready
                else "fail_closed_cached_fold_rows_do_not_cover_current57_cofactor_surface"
            ),
        },
        "calibration_overlap": {
            "inscope": calibration_inscope,
            "oos": calibration_oos,
        },
        "train_overlap": {
            "status": (
                "row_level_train_fold_scores_not_present_in_cached_fold_contracts"
            ),
            "inscope": train_inscope,
            "oos": train_oos,
        },
        "overlap_only_fixed_gate_probe": _overlap_only_fixed_gate_probe(
            current57_operating_point=current57_operating_point,
            fold_inscope_scores=inscope_scores,
            fold_oos_scores=oos_scores,
            fold_threshold=_fold_threshold(fold_inscope_contract),
        ),
        "interpretation": {
            "headline": (
                "Cached fold/TM row scores are not row-aligned with the current-57 "
                "cofactor train/cal precision surface."
                if not alignment_ready
                else "Cached fold/TM row scores cover the current-57 calibration "
                "cofactor surface sufficiently for a preregistered fusion readout."
            ),
            "deployment_decision": (
                "Fail closed for cached atlas-engine fusion. Install/expose foldseek "
                "and recompute Fold/TM on the current-57 train/cal cofactor rows, or "
                "pin/replay the older router/fingerprint surface whose fold rows are "
                "already cached."
                if not alignment_ready
                else "Cached atlas-engine fusion may proceed only under the separate "
                "cofactor precision contract and preregistered selection rule."
            ),
        },
    }


def _report(audit: dict[str, Any]) -> str:
    cal = audit["calibration_overlap"]
    gate = audit["alignment_gate"]
    probe = audit["overlap_only_fixed_gate_probe"]

    def fmt(item: dict[str, Any]) -> str:
        return (
            f"{item.get('overlap_rows')}/{item.get('current57_rows')} "
            f"({item.get('overlap_fraction')})"
        )

    lines = [
        "# Current-57 Cofactor/Fold Alignment Audit",
        "",
        f"Run: {audit['created_utc']}",
        f"Status: `{audit['status']}`",
        "",
        "## Alignment Gate",
        "",
        f"- Calibration in-scope overlap required: >= "
        f"{gate['min_calibration_inscope_overlap_fraction']}.",
        f"- Calibration OOS overlap required: >= "
        f"{gate['min_calibration_oos_overlap_fraction']}.",
        f"- Calibration in-scope overlap observed: {fmt(cal['inscope'])}.",
        f"- Calibration OOS overlap observed: {fmt(cal['oos'])}.",
        f"- Decision: `{gate['decision']}`.",
        "",
        "## Overlap-Only Probe",
        "",
        f"- Interpretable: {probe.get('interpretable')}.",
        f"- Fold threshold: {probe.get('fold_threshold')}.",
        f"- Compatible positives retained on overlap: "
        f"{probe.get('compatible_inscope_correct_retained_on_overlap')}.",
        f"- OOS false positives retained on overlap: "
        f"{probe.get('oos_false_positives_retained_on_overlap')}.",
        "",
        "## Decision",
        "",
        f"- {audit['interpretation']['deployment_decision']}",
        "",
        "## Guardrails",
        "",
        "- No heldout rows were scored or read.",
        "- No new Foldseek/TM scores, model weights, thresholds, labels, registries, "
        "ontologies, or fingerprint families were changed.",
    ]
    return "\n".join(lines) + "\n"


def write_current57_cofactor_fold_alignment_audit(
    *,
    current57_operating_point_path: Path,
    fold_inscope_contract_path: Path,
    fold_oos_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    min_calibration_inscope_overlap_fraction: float = DEFAULT_MIN_CALIBRATION_INSCOPE_OVERLAP_FRACTION,
    min_calibration_oos_overlap_fraction: float = DEFAULT_MIN_CALIBRATION_OOS_OVERLAP_FRACTION,
) -> dict[str, Any]:
    current57 = _load_json(current57_operating_point_path)
    fold_inscope = _load_json(fold_inscope_contract_path)
    fold_oos = _load_json(fold_oos_contract_path)
    audit = build_current57_cofactor_fold_alignment_audit(
        current57_operating_point=current57,
        fold_inscope_contract=fold_inscope,
        fold_oos_contract=fold_oos,
        min_calibration_inscope_overlap_fraction=min_calibration_inscope_overlap_fraction,
        min_calibration_oos_overlap_fraction=min_calibration_oos_overlap_fraction,
    )
    audit["source_artifacts"] = {
        "current57_cofactor_operating_point": _artifact_summary(
            current57_operating_point_path, current57
        ),
        "fold_inscope_contract": _artifact_summary(
            fold_inscope_contract_path, fold_inscope
        ),
        "fold_oos_contract": _artifact_summary(fold_oos_contract_path, fold_oos),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
