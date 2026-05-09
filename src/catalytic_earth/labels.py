from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .sources import PROJECT_ROOT


LABEL_REGISTRY = PROJECT_ROOT / "data" / "registries" / "curated_mechanism_labels.json"
ZERO_FALSE_SELECTION_RULE = (
    "choose the smallest threshold with zero current out-of-scope false "
    "non-abstentions while preserving best top3 in-scope accuracy; fall back "
    "to legacy ranking if no threshold satisfies that guard"
)
LEGACY_SELECTION_RULE = "maximize top3 in-scope accuracy, then out-of-scope abstention, then coverage"
RETAINED_TOP3_REFERENCE_RULE = (
    "maximize top3 retained in-scope accuracy, then minimize out-of-scope "
    "false non-abstentions, then coverage"
)


@dataclass(frozen=True)
class MechanismLabel:
    entry_id: str
    fingerprint_id: str | None
    label_type: str
    confidence: str
    rationale: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MechanismLabel":
        entry_id = data.get("entry_id")
        fingerprint_id = data.get("fingerprint_id")
        label_type = data.get("label_type")
        confidence = data.get("confidence")
        rationale = data.get("rationale")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValueError("entry_id must be a non-empty string")
        if fingerprint_id is not None and not isinstance(fingerprint_id, str):
            raise ValueError(f"{entry_id}: fingerprint_id must be null or string")
        if label_type not in {"seed_fingerprint", "out_of_scope"}:
            raise ValueError(f"{entry_id}: invalid label_type")
        if confidence not in {"high", "medium", "low"}:
            raise ValueError(f"{entry_id}: invalid confidence")
        if not isinstance(rationale, str) or len(rationale) < 20:
            raise ValueError(f"{entry_id}: rationale is too short")
        if label_type == "seed_fingerprint" and not fingerprint_id:
            raise ValueError(f"{entry_id}: seed_fingerprint requires fingerprint_id")
        if label_type == "out_of_scope" and fingerprint_id is not None:
            raise ValueError(f"{entry_id}: out_of_scope requires null fingerprint_id")
        return cls(entry_id, fingerprint_id, label_type, confidence, rationale)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "fingerprint_id": self.fingerprint_id,
            "label_type": self.label_type,
            "confidence": self.confidence,
            "rationale": self.rationale,
        }


def load_labels(path: Path = LABEL_REGISTRY) -> list[MechanismLabel]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("label registry must be a list")
    labels = [MechanismLabel.from_dict(item) for item in data]
    duplicates = [entry_id for entry_id, count in Counter(label.entry_id for label in labels).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate labels: {', '.join(sorted(duplicates))}")
    fingerprint_ids = {fingerprint.id for fingerprint in load_fingerprints()}
    unknown = sorted(
        label.fingerprint_id
        for label in labels
        if label.fingerprint_id and label.fingerprint_id not in fingerprint_ids
    )
    if unknown:
        raise ValueError(f"unknown fingerprint ids: {', '.join(unknown)}")
    return labels


def label_summary(labels: list[MechanismLabel]) -> dict[str, Any]:
    return {
        "label_count": len(labels),
        "by_type": dict(sorted(Counter(label.label_type for label in labels).items())),
        "by_confidence": dict(sorted(Counter(label.confidence for label in labels).items())),
        "by_fingerprint": dict(
            sorted(Counter(label.fingerprint_id for label in labels if label.fingerprint_id).items())
        ),
    }


def evaluate_geometry_retrieval(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    rows: list[dict[str, Any]] = []
    in_scope_total = 0
    top1_correct = 0
    top3_correct = 0
    out_scope_total = 0
    out_scope_abstained = 0
    in_scope_abstained = 0
    top1_correct_retained = 0
    top3_correct_retained = 0

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label:
            continue
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_id = top1.get("fingerprint_id")
        top1_score = float(top1.get("score", 0.0) or 0.0)
        top3_ids = [item.get("fingerprint_id") for item in top[:3]]
        abstained = top1_score < abstain_threshold
        evaluable = _is_geometry_evaluable(result)

        if label.fingerprint_id:
            in_scope_total += 1
            is_top1 = top1_id == label.fingerprint_id
            is_top3 = label.fingerprint_id in top3_ids
            top1_correct += int(is_top1)
            top3_correct += int(is_top3)
            in_scope_abstained += int(abstained)
            top1_correct_retained += int(is_top1 and not abstained)
            top3_correct_retained += int(is_top3 and not abstained)
        else:
            out_scope_total += 1
            is_top1 = False
            is_top3 = False
            out_scope_abstained += int(abstained)

        rows.append(
            {
                "entry_id": entry_id,
                "label_type": label.label_type,
                "target_fingerprint_id": label.fingerprint_id,
                "confidence": label.confidence,
                "top1_fingerprint_id": top1_id,
                "top1_score": top1_score,
                "status": result.get("status"),
                "resolved_residue_count": result.get("resolved_residue_count", 0),
                "evaluable": evaluable,
                "top1_correct": is_top1,
                "top3_correct": is_top3,
                "abstained": abstained,
                "rationale": label.rationale,
            }
        )

    return {
        "metadata": _evaluation_metadata(
            rows=rows,
            labels=labels,
            abstain_threshold=abstain_threshold,
            in_scope_total=in_scope_total,
            top1_correct=top1_correct,
            top3_correct=top3_correct,
            out_scope_total=out_scope_total,
            out_scope_abstained=out_scope_abstained,
            in_scope_abstained=in_scope_abstained,
            top1_correct_retained=top1_correct_retained,
            top3_correct_retained=top3_correct_retained,
        ),
        "rows": sorted(rows, key=lambda row: row["entry_id"]),
    }


def _evaluation_metadata(
    rows: list[dict[str, Any]],
    labels: list[MechanismLabel],
    abstain_threshold: float,
    in_scope_total: int,
    top1_correct: int,
    top3_correct: int,
    out_scope_total: int,
    out_scope_abstained: int,
    in_scope_abstained: int,
    top1_correct_retained: int,
    top3_correct_retained: int,
) -> dict[str, Any]:
    evaluable_rows = [row for row in rows if row.get("evaluable")]
    in_scope_evaluable_rows = [
        row for row in evaluable_rows if row.get("label_type") == "seed_fingerprint"
    ]
    out_scope_evaluable_rows = [
        row for row in evaluable_rows if row.get("label_type") == "out_of_scope"
    ]
    in_scope_evaluable_count = len(in_scope_evaluable_rows)
    out_scope_evaluable_count = len(out_scope_evaluable_rows)
    in_scope_evaluable_abstained = sum(1 for row in in_scope_evaluable_rows if row["abstained"])
    out_scope_evaluable_abstained = sum(1 for row in out_scope_evaluable_rows if row["abstained"])
    return {
        "method": "geometry_retrieval_against_curated_seed_labels",
        "evaluated_count": len(rows),
        "evaluable_count": len(evaluable_rows),
        "in_scope_count": in_scope_total,
        "in_scope_evaluable_count": in_scope_evaluable_count,
        "in_scope_not_evaluable_count": in_scope_total - in_scope_evaluable_count,
        "out_of_scope_count": out_scope_total,
        "out_of_scope_evaluable_count": out_scope_evaluable_count,
        "out_of_scope_not_evaluable_count": out_scope_total - out_scope_evaluable_count,
        "abstain_threshold": abstain_threshold,
        "top1_accuracy_in_scope": _ratio(top1_correct, in_scope_total),
        "top3_accuracy_in_scope": _ratio(top3_correct, in_scope_total),
        "top1_retained_accuracy_in_scope": _ratio(top1_correct_retained, in_scope_total),
        "top3_retained_accuracy_in_scope": _ratio(top3_correct_retained, in_scope_total),
        "in_scope_retention_rate": _ratio(in_scope_total - in_scope_abstained, in_scope_total),
        "in_scope_abstention_rate": _ratio(in_scope_abstained, in_scope_total),
        "out_of_scope_abstention_rate": _ratio(out_scope_abstained, out_scope_total),
        "out_of_scope_false_non_abstentions": out_scope_total - out_scope_abstained,
        "top1_accuracy_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable_rows if row["top1_correct"]),
            in_scope_evaluable_count,
        ),
        "top3_accuracy_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable_rows if row["top3_correct"]),
            in_scope_evaluable_count,
        ),
        "top1_retained_accuracy_in_scope_evaluable": _ratio(
            sum(
                1
                for row in in_scope_evaluable_rows
                if row["top1_correct"] and not row["abstained"]
            ),
            in_scope_evaluable_count,
        ),
        "top3_retained_accuracy_in_scope_evaluable": _ratio(
            sum(
                1
                for row in in_scope_evaluable_rows
                if row["top3_correct"] and not row["abstained"]
            ),
            in_scope_evaluable_count,
        ),
        "in_scope_retention_rate_evaluable": _ratio(
            in_scope_evaluable_count - in_scope_evaluable_abstained,
            in_scope_evaluable_count,
        ),
        "out_of_scope_abstention_rate_evaluable": _ratio(
            out_scope_evaluable_abstained,
            out_scope_evaluable_count,
        ),
        "out_of_scope_false_non_abstentions_evaluable": (
            out_scope_evaluable_count - out_scope_evaluable_abstained
        ),
        "label_summary": label_summary(labels),
    }


def sweep_abstention_thresholds(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    thresholds: list[float] | None = None,
) -> dict[str, Any]:
    if thresholds is None:
        thresholds = default_abstention_thresholds(retrieval, labels)
    rows = [
        evaluate_geometry_retrieval(retrieval, labels, abstain_threshold=threshold)["metadata"]
        for threshold in thresholds
    ]
    selected = select_threshold(rows)
    legacy_selected = select_legacy_threshold(rows)
    retained_top3_reference = select_retained_top3_reference(rows)
    return {
        "metadata": {
            "method": "abstention_threshold_sweep",
            "threshold_count": len(rows),
            "selected_threshold": selected.get("abstain_threshold") if selected else None,
            "selection_rule": ZERO_FALSE_SELECTION_RULE,
            "legacy_selected_threshold": (
                legacy_selected.get("abstain_threshold") if legacy_selected else None
            ),
            "legacy_selection_rule": LEGACY_SELECTION_RULE,
            "retained_top3_reference_threshold": (
                retained_top3_reference.get("abstain_threshold") if retained_top3_reference else None
            ),
            "retained_top3_reference_rule": RETAINED_TOP3_REFERENCE_RULE,
            "selection_comparison": compare_threshold_policies(
                selected,
                legacy_selected,
                retained_top3_reference,
            ),
        },
        "thresholds": rows,
        "selected": selected,
        "legacy_selected": legacy_selected,
        "retained_top3_reference": retained_top3_reference,
    }


def default_abstention_thresholds(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
) -> list[float]:
    labels_by_entry = {label.entry_id: label for label in labels}
    thresholds = {round(index / 20, 2) for index in range(0, 21)}
    for result in retrieval.get("results", []):
        if result.get("entry_id") not in labels_by_entry:
            continue
        top = result.get("top_fingerprints", [])
        if not top:
            continue
        score = float(top[0].get("score", 0.0) or 0.0)
        thresholds.add(round(score, 4))
        thresholds.add(round(min(1.0, score + 0.0001), 4))
    return sorted(thresholds)


def analyze_out_of_scope_failures(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    false_non_abstentions: list[dict[str, Any]] = []
    out_scope_total = 0
    out_scope_abstained = 0

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label or label.label_type != "out_of_scope":
            continue
        out_scope_total += 1
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_score = float(top1.get("score", 0.0) or 0.0)
        abstained = top1_score < abstain_threshold
        if abstained:
            out_scope_abstained += 1
            continue
        category = classify_out_of_scope_failure(top1, abstain_threshold=abstain_threshold)
        false_non_abstentions.append(
            {
                "entry_id": entry_id,
                "top1_fingerprint_id": top1.get("fingerprint_id"),
                "top1_score": round(top1_score, 4),
                "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                "abstain_threshold": abstain_threshold,
                "evidence_pattern": category,
                "component_scores": {
                    "residue_match_fraction": float(top1.get("residue_match_fraction", 0.0) or 0.0),
                    "role_match_fraction": float(top1.get("role_match_fraction", 0.0) or 0.0),
                    "cofactor_context_score": float(top1.get("cofactor_context_score", 0.0) or 0.0),
                    "substrate_pocket_score": float(top1.get("substrate_pocket_score", 0.0) or 0.0),
                    "compactness_score": float(top1.get("compactness_score", 0.0) or 0.0),
                    "mechanistic_coherence_score": float(
                        top1.get("mechanistic_coherence_score", 0.0) or 0.0
                    ),
                },
                "label_rationale": label.rationale,
            }
        )

    category_counts = Counter(row["evidence_pattern"] for row in false_non_abstentions)
    max_false_score = max((row["top1_score"] for row in false_non_abstentions), default=None)
    recommended_threshold = (
        round(min(1.0, float(max_false_score) + 0.01), 4)
        if max_false_score is not None
        else abstain_threshold
    )
    return {
        "metadata": {
            "method": "out_of_scope_failure_pattern_analysis",
            "evaluated_out_of_scope_entries": out_scope_total,
            "false_non_abstentions": len(false_non_abstentions),
            "out_of_scope_abstention_rate": _ratio(out_scope_abstained, out_scope_total),
            "abstain_threshold": abstain_threshold,
            "max_false_non_abstention_score": max_false_score,
            "recommended_threshold_for_zero_current_false_non_abstentions": recommended_threshold,
            "category_counts": dict(sorted(category_counts.items())),
        },
        "rows": sorted(false_non_abstentions, key=lambda row: row["entry_id"]),
    }


def analyze_geometry_score_margins(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    near_margin: float = 0.02,
) -> dict[str, Any]:
    if near_margin < 0:
        raise ValueError("near_margin must be non-negative")
    labels_by_entry = {label.entry_id: label for label in labels}
    rows: list[dict[str, Any]] = []

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label:
            continue
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        rows.append(
            {
                "entry_id": entry_id,
                "label_type": label.label_type,
                "target_fingerprint_id": label.fingerprint_id,
                "top1_fingerprint_id": top1.get("fingerprint_id"),
                "top1_score": round(float(top1.get("score", 0.0) or 0.0), 4),
                "status": result.get("status"),
                "resolved_residue_count": result.get("resolved_residue_count", 0),
                "evaluable": _is_geometry_evaluable(result),
                "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                "top1_correct": top1.get("fingerprint_id") == label.fingerprint_id
                if label.fingerprint_id
                else False,
            }
        )

    in_scope_rows = [row for row in rows if row["label_type"] == "seed_fingerprint"]
    out_scope_rows = [row for row in rows if row["label_type"] == "out_of_scope"]
    in_scope_score_rows = [row for row in in_scope_rows if row["evaluable"]]
    correct_in_scope_score_rows = [row for row in in_scope_score_rows if row["top1_correct"]]
    out_scope_score_rows = [row for row in out_scope_rows if row["evaluable"]]
    cofactor_evidence_counts = Counter(
        row.get("cofactor_evidence_level") or "unknown" for row in rows
    )
    min_in_scope_score = min((row["top1_score"] for row in in_scope_score_rows), default=None)
    min_correct_in_scope_score = min(
        (row["top1_score"] for row in correct_in_scope_score_rows),
        default=None,
    )
    max_out_scope_score = max((row["top1_score"] for row in out_scope_score_rows), default=None)
    strict_threshold_exists = (
        min_in_scope_score is not None
        and max_out_scope_score is not None
        and max_out_scope_score < min_in_scope_score
    )
    conflicting_out_scope = [
        row
        for row in out_scope_score_rows
        if min_in_scope_score is not None and row["top1_score"] >= min_in_scope_score
    ]
    limiting_in_scope = [
        row
        for row in in_scope_score_rows
        if min_in_scope_score is not None and _same_float(row["top1_score"], min_in_scope_score)
    ]
    limiting_out_scope = [
        row
        for row in out_scope_score_rows
        if max_out_scope_score is not None and _same_float(row["top1_score"], max_out_scope_score)
    ]
    in_scope_below_max_out_scope = [
        row
        for row in in_scope_score_rows
        if max_out_scope_score is not None and row["top1_score"] <= max_out_scope_score
    ]
    boundary_rows = _score_margin_boundary_rows(
        in_scope_score_rows=in_scope_score_rows,
        out_scope_score_rows=out_scope_score_rows,
        min_in_scope_score=min_in_scope_score,
        max_out_scope_score=max_out_scope_score,
        near_margin=near_margin,
    )
    return {
        "metadata": {
            "method": "geometry_score_margin_analysis",
            "evaluated_count": len(rows),
            "in_scope_count": len(in_scope_rows),
            "in_scope_evaluable_count": len(in_scope_score_rows),
            "correct_in_scope_evaluable_count": len(correct_in_scope_score_rows),
            "out_of_scope_count": len(out_scope_rows),
            "out_of_scope_evaluable_count": len(out_scope_score_rows),
            "min_in_scope_top1_score": min_in_scope_score,
            "min_correct_in_scope_top1_score": min_correct_in_scope_score,
            "max_out_of_scope_top1_score": max_out_scope_score,
            "score_separation_gap": (
                round(min_in_scope_score - max_out_scope_score, 4)
                if min_in_scope_score is not None and max_out_scope_score is not None
                else None
            ),
            "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope": (
                strict_threshold_exists
            ),
            "near_margin": near_margin,
            "score_margin_boundary_count": len(boundary_rows),
            "out_of_scope_entries_at_or_above_min_in_scope": len(conflicting_out_scope),
            "in_scope_entries_at_or_below_max_out_of_scope": len(in_scope_below_max_out_scope),
            "cofactor_evidence_counts": dict(sorted(cofactor_evidence_counts.items())),
        },
        "conflicting_out_of_scope_rows": sorted(
            conflicting_out_scope,
            key=lambda row: (-row["top1_score"], row["entry_id"]),
        ),
        "limiting_in_scope_rows": sorted(limiting_in_scope, key=lambda row: row["entry_id"]),
        "limiting_out_of_scope_rows": sorted(
            limiting_out_scope,
            key=lambda row: (-row["top1_score"], row["entry_id"]),
        ),
        "score_margin_boundary_rows": sorted(
            boundary_rows,
            key=lambda row: (row["boundary_side"], row["score_gap_to_boundary"], row["entry_id"]),
        ),
        "in_scope_rows": sorted(in_scope_rows, key=lambda row: row["entry_id"]),
        "rows": sorted(rows, key=lambda row: row["entry_id"]),
    }


def _score_margin_boundary_rows(
    in_scope_score_rows: list[dict[str, Any]],
    out_scope_score_rows: list[dict[str, Any]],
    min_in_scope_score: float | None,
    max_out_scope_score: float | None,
    near_margin: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if min_in_scope_score is not None:
        for row in in_scope_score_rows:
            score_gap = round(row["top1_score"] - min_in_scope_score, 4)
            if score_gap <= near_margin:
                rows.append(
                    {
                        **row,
                        "boundary_side": "in_scope_floor",
                        "score_gap_to_boundary": score_gap,
                    }
                )
        for row in out_scope_score_rows:
            score_gap = round(min_in_scope_score - row["top1_score"], 4)
            if score_gap <= near_margin:
                rows.append(
                    {
                        **row,
                        "boundary_side": "out_of_scope_near_positive_floor",
                        "score_gap_to_boundary": score_gap,
                    }
                )
    if max_out_scope_score is not None:
        for row in out_scope_score_rows:
            score_gap = round(max_out_scope_score - row["top1_score"], 4)
            if score_gap <= near_margin:
                rows.append(
                    {
                        **row,
                        "boundary_side": "out_of_scope_ceiling",
                        "score_gap_to_boundary": score_gap,
                    }
                )
    return rows


def build_hard_negative_controls(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    score_floor: float | None = None,
    near_margin: float = 0.01,
) -> dict[str, Any]:
    margins = analyze_geometry_score_margins(retrieval, labels)
    inferred_floor = margins["metadata"].get("min_correct_in_scope_top1_score")
    floor_source = "min_correct_in_scope_top1_score"
    if inferred_floor is None:
        inferred_floor = margins["metadata"]["min_in_scope_top1_score"]
        floor_source = "min_in_scope_top1_score"
    if score_floor is None and inferred_floor is None:
        return {
            "metadata": {
                "method": "geometry_hard_negative_control_selection",
                "score_floor": None,
                "score_floor_source": floor_source,
                "hard_negative_count": 0,
                "near_miss_margin": near_margin,
                "near_miss_count": 0,
                "evaluated_out_of_scope_count": margins["metadata"]["out_of_scope_count"],
                "evaluable_out_of_scope_count": margins["metadata"]["out_of_scope_evaluable_count"],
                "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope": (
                    margins["metadata"][
                        "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
                    ]
                ),
                "top1_fingerprint_counts": {},
                "cofactor_evidence_counts": {},
            },
            "rows": [],
            "near_miss_rows": [],
            "groups": [],
            "near_miss_groups": [],
        }
    floor = float(score_floor if score_floor is not None else inferred_floor)
    labels_by_entry = {label.entry_id: label for label in labels}
    rows: list[dict[str, Any]] = []
    near_miss_rows: list[dict[str, Any]] = []

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label or label.label_type != "out_of_scope":
            continue
        if not _is_geometry_evaluable(result):
            continue
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        if top1_score < floor:
            if floor - top1_score <= near_margin:
                near_miss_rows.append(
                    {
                        **_hard_negative_row(
                            label=label,
                            result=result,
                            top1=top1,
                            top1_score=top1_score,
                            score_floor=floor,
                            negative_control_type="near_miss_below_in_scope_floor",
                        ),
                        "score_gap_to_floor": round(floor - top1_score, 4),
                    }
                )
            continue
        rows.append(
            _hard_negative_row(
                label=label,
                result=result,
                top1=top1,
                top1_score=top1_score,
                score_floor=floor,
                negative_control_type="score_overlap_with_in_scope_positive",
            )
        )

    fingerprint_counts = Counter(row["top1_fingerprint_id"] for row in rows)
    cofactor_evidence_counts = Counter(
        row.get("cofactor_evidence_level") or "unknown" for row in rows
    )
    groups = group_hard_negative_controls(rows)
    near_miss_groups = group_hard_negative_controls(near_miss_rows)
    return {
        "metadata": {
            "method": "geometry_hard_negative_control_selection",
            "score_floor": round(floor, 4),
            "score_floor_source": floor_source if score_floor is None else "explicit",
            "hard_negative_count": len(rows),
            "near_miss_margin": near_margin,
            "near_miss_count": len(near_miss_rows),
            "evaluated_out_of_scope_count": margins["metadata"]["out_of_scope_count"],
            "evaluable_out_of_scope_count": margins["metadata"]["out_of_scope_evaluable_count"],
            "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope": (
                margins["metadata"][
                    "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
                ]
            ),
            "top1_fingerprint_counts": dict(sorted(fingerprint_counts.items())),
            "cofactor_evidence_counts": dict(sorted(cofactor_evidence_counts.items())),
        },
        "rows": sorted(rows, key=lambda row: (-row["top1_score"], row["entry_id"])),
        "near_miss_rows": sorted(
            near_miss_rows,
            key=lambda row: (row["score_gap_to_floor"], row["entry_id"]),
        ),
        "groups": groups,
        "near_miss_groups": near_miss_groups,
    }


def group_hard_negative_controls(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (
            str(row.get("top1_fingerprint_id") or "unknown"),
            str(row.get("cofactor_evidence_level") or "unknown"),
        )
        grouped.setdefault(key, []).append(row)

    result: list[dict[str, Any]] = []
    for (fingerprint_id, evidence_level), group_rows in grouped.items():
        scores = [float(row.get("top1_score", 0.0) or 0.0) for row in group_rows]
        reasons = Counter(str(row.get("hard_negative_reason") or "unknown") for row in group_rows)
        result.append(
            {
                "top1_fingerprint_id": fingerprint_id,
                "cofactor_evidence_level": evidence_level,
                "count": len(group_rows),
                "min_top1_score": round(min(scores), 4),
                "mean_top1_score": round(sum(scores) / len(scores), 4),
                "max_top1_score": round(max(scores), 4),
                "hard_negative_reason_counts": dict(sorted(reasons.items())),
                "entry_ids": sorted(str(row.get("entry_id")) for row in group_rows),
            }
        )
    return sorted(
        result,
        key=lambda row: (
            -int(row["count"]),
            str(row["top1_fingerprint_id"]),
            str(row["cofactor_evidence_level"]),
        ),
    )


def _hard_negative_row(
    label: MechanismLabel,
    result: dict[str, Any],
    top1: dict[str, Any],
    top1_score: float,
    score_floor: float,
    negative_control_type: str,
) -> dict[str, Any]:
    return {
        "entry_id": label.entry_id,
        "negative_control_type": negative_control_type,
        "hard_negative_reason": classify_hard_negative_control(top1),
        "score_floor": round(score_floor, 4),
        "top1_fingerprint_id": top1.get("fingerprint_id"),
        "top1_score": top1_score,
        "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
        "context": _retrieval_result_context(result),
        "component_scores": {
            "residue_match_fraction": float(top1.get("residue_match_fraction", 0.0) or 0.0),
            "role_match_fraction": float(top1.get("role_match_fraction", 0.0) or 0.0),
            "cofactor_context_score": float(top1.get("cofactor_context_score", 0.0) or 0.0),
            "substrate_pocket_score": float(top1.get("substrate_pocket_score", 0.0) or 0.0),
            "compactness_score": float(top1.get("compactness_score", 0.0) or 0.0),
            "mechanistic_coherence_score": float(
                top1.get("mechanistic_coherence_score", 0.0) or 0.0
            ),
        },
        "label_rationale": label.rationale,
    }


def _retrieval_result_context(result: dict[str, Any]) -> dict[str, Any]:
    ligand_context = result.get("ligand_context", {})
    if not isinstance(ligand_context, dict):
        ligand_context = {}
    pocket_context = result.get("pocket_context", {})
    if not isinstance(pocket_context, dict):
        pocket_context = {}
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        descriptors = {}
    return {
        "pdb_id": result.get("pdb_id"),
        "residue_codes": result.get("residue_codes", []),
        "ligand_codes": ligand_context.get("ligand_codes", []),
        "cofactor_families": ligand_context.get("cofactor_families", []),
        "nearby_residue_count": pocket_context.get("nearby_residue_count", 0),
        "pocket_descriptors": descriptors,
    }


def classify_hard_negative_control(top1: dict[str, Any]) -> str:
    fingerprint_id = top1.get("fingerprint_id")
    cofactor_evidence = top1.get("cofactor_evidence_level")
    coherence = float(top1.get("mechanistic_coherence_score", 0.0) or 0.0)
    if fingerprint_id == "metal_dependent_hydrolase" and cofactor_evidence == "role_inferred":
        return "metal_role_overlap_without_confirmed_hydrolysis"
    if fingerprint_id == "ser_his_acid_hydrolase" and coherence < 0.5:
        return "ser_his_signature_without_ser_nucleophile_coherence"
    return "high_score_out_of_scope_overlap"


def build_label_expansion_candidates(
    geometry: dict[str, Any],
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
) -> dict[str, Any]:
    labeled_entry_ids = {label.entry_id for label in labels}
    retrieval_by_entry = {result.get("entry_id"): result for result in retrieval.get("results", [])}
    rows: list[dict[str, Any]] = []

    for entry in geometry.get("entries", []):
        entry_id = entry.get("entry_id")
        if not isinstance(entry_id, str) or entry_id in labeled_entry_ids:
            continue
        result = retrieval_by_entry.get(entry_id, {})
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        pocket_context = entry.get("pocket_context") if isinstance(entry, dict) else {}
        ligand_context = entry.get("ligand_context") if isinstance(entry, dict) else {}
        resolved_count = int(entry.get("resolved_residue_count", 0) or 0)
        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        has_pocket = bool(
            isinstance(pocket_context, dict)
            and int(pocket_context.get("nearby_residue_count", 0) or 0) > 0
        )
        has_pairwise_geometry = len(entry.get("pairwise_distances_angstrom", []) or []) > 0
        readiness_checks = {
            "status_ok": entry.get("status") == "ok",
            "resolved_at_least_three_residues": resolved_count >= 3,
            "has_pairwise_geometry": has_pairwise_geometry,
            "has_pocket_context": has_pocket,
            "top1_score_at_least_0_4": top1_score >= 0.4,
        }
        readiness_score = sum(int(value) for value in readiness_checks.values())
        rows.append(
            {
                "entry_id": entry_id,
                "pdb_id": entry.get("pdb_id"),
                "status": entry.get("status"),
                "resolved_residue_count": resolved_count,
                "has_pairwise_geometry": has_pairwise_geometry,
                "has_pocket_context": has_pocket,
                "cofactor_families": (
                    ligand_context.get("cofactor_families", [])
                    if isinstance(ligand_context, dict)
                    else []
                ),
                "top1_fingerprint_id": top1.get("fingerprint_id"),
                "top1_score": top1_score,
                "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                "mechanistic_coherence_score": top1.get("mechanistic_coherence_score"),
                "readiness_score": readiness_score,
                "readiness_checks": readiness_checks,
                "readiness_blockers": [
                    check for check, passed in readiness_checks.items() if not passed
                ],
            }
        )

    ready_rows = [row for row in rows if row["readiness_score"] >= 4]
    return {
        "metadata": {
            "method": "geometry_label_expansion_candidate_selection",
            "candidate_count": len(rows),
            "ready_for_label_review_count": len(ready_rows),
            "labeled_entry_count": len(labeled_entry_ids),
            "geometry_entry_count": len(geometry.get("entries", [])),
        },
        "rows": sorted(rows, key=lambda row: (-row["readiness_score"], row["entry_id"])),
    }


def analyze_structure_mapping_issues(
    geometry: dict[str, Any],
    labels: list[MechanismLabel],
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    rows: list[dict[str, Any]] = []
    for entry in geometry.get("entries", []):
        status = entry.get("status")
        if status == "ok":
            continue
        entry_id = entry.get("entry_id")
        label = labels_by_entry.get(entry_id)
        rows.append(
            {
                "entry_id": entry_id,
                "pdb_id": entry.get("pdb_id"),
                "status": status,
                "label_type": label.label_type if label else None,
                "target_fingerprint_id": label.fingerprint_id if label else None,
                "resolved_residue_count": entry.get("resolved_residue_count", 0),
                "missing_positions": entry.get("missing_positions", 0),
                "missing_position_details": entry.get("missing_position_details", []),
            }
        )
    labeled_rows = [row for row in rows if row["label_type"] is not None]
    status_counts = Counter(str(row["status"]) for row in rows)
    label_type_counts = Counter(str(row["label_type"] or "unlabeled") for row in rows)
    expected_code_counts: Counter[str] = Counter()
    observed_code_counts: Counter[str] = Counter()
    for row in rows:
        for detail in row["missing_position_details"]:
            expected_code = detail.get("expected_code")
            if expected_code:
                expected_code_counts[str(expected_code)] += 1
            for observed_code in detail.get("observed_codes_at_position", []):
                observed_code_counts[str(observed_code)] += 1
    return {
        "metadata": {
            "method": "structure_mapping_issue_analysis",
            "issue_count": len(rows),
            "labeled_issue_count": len(labeled_rows),
            "geometry_entry_count": len(geometry.get("entries", [])),
            "status_counts": dict(sorted(status_counts.items())),
            "label_type_counts": dict(sorted(label_type_counts.items())),
            "missing_expected_code_counts": dict(sorted(expected_code_counts.items())),
            "observed_code_at_missing_position_counts": dict(sorted(observed_code_counts.items())),
        },
        "rows": sorted(rows, key=lambda row: str(row["entry_id"])),
    }


def select_threshold(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    best_top3 = max(_row_metric(row, "top3_accuracy_in_scope_evaluable", "top3_accuracy_in_scope") for row in rows)
    candidates = [
        row
        for row in rows
        if _same_float(
            _row_metric(row, "top3_accuracy_in_scope_evaluable", "top3_accuracy_in_scope"),
            best_top3,
        )
        and _has_zero_out_of_scope_false_non_abstentions(row)
    ]
    if candidates:
        return min(candidates, key=lambda row: float(row.get("abstain_threshold") or 0.0))
    return select_legacy_threshold(rows)


def select_legacy_threshold(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None

    def score(row: dict[str, Any]) -> tuple[float, float, float, float]:
        top3 = _row_metric(row, "top3_accuracy_in_scope_evaluable", "top3_accuracy_in_scope")
        abstention = _row_metric(
            row,
            "out_of_scope_abstention_rate_evaluable",
            "out_of_scope_abstention_rate",
        )
        threshold = float(row.get("abstain_threshold") or 0.0)
        coverage = 1.0 - threshold
        return (top3, abstention, coverage, -threshold)

    return max(rows, key=score)


def select_retained_top3_reference(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None

    def score(row: dict[str, Any]) -> tuple[float, int, float, float]:
        retained_top3 = _row_metric(
            row,
            "top3_retained_accuracy_in_scope_evaluable",
            "top3_retained_accuracy_in_scope",
        )
        false_non_abstentions = int(
            row.get(
                "out_of_scope_false_non_abstentions_evaluable",
                row.get("out_of_scope_false_non_abstentions") or 0,
            )
        )
        threshold = float(row.get("abstain_threshold") or 0.0)
        coverage = 1.0 - threshold
        return (retained_top3, -false_non_abstentions, coverage, -threshold)

    return max(rows, key=score)


def compare_threshold_policies(
    selected: dict[str, Any] | None,
    legacy_selected: dict[str, Any] | None,
    retained_top3_reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selected_threshold = _threshold_value(selected)
    legacy_threshold = _threshold_value(legacy_selected)
    retained_reference_threshold = _threshold_value(retained_top3_reference)
    return {
        "same_threshold": selected_threshold == legacy_threshold,
        "selected_threshold": selected_threshold,
        "legacy_selected_threshold": legacy_threshold,
        "retained_top3_reference_threshold": retained_reference_threshold,
        "zero_false_preserves_retained_top3": _same_float(
            _comparison_metric(
                selected,
                "top3_retained_accuracy_in_scope_evaluable",
                "top3_retained_accuracy_in_scope",
            ),
            _comparison_metric(
                retained_top3_reference,
                "top3_retained_accuracy_in_scope_evaluable",
                "top3_retained_accuracy_in_scope",
            ),
        ),
        "zero_false_preserves_in_scope_retention": _same_float(
            _comparison_metric(
                selected,
                "in_scope_retention_rate_evaluable",
                "in_scope_retention_rate",
            ),
            _comparison_metric(
                retained_top3_reference,
                "in_scope_retention_rate_evaluable",
                "in_scope_retention_rate",
            ),
        ),
        "selected_out_of_scope_false_non_abstentions": _metadata_value(
            selected,
            "out_of_scope_false_non_abstentions",
        ),
        "legacy_out_of_scope_false_non_abstentions": _metadata_value(
            legacy_selected,
            "out_of_scope_false_non_abstentions",
        ),
        "retained_top3_reference_out_of_scope_false_non_abstentions": _metadata_value(
            retained_top3_reference,
            "out_of_scope_false_non_abstentions",
        ),
        "selected_in_scope_retention_rate": _metadata_value(selected, "in_scope_retention_rate"),
        "legacy_in_scope_retention_rate": _metadata_value(legacy_selected, "in_scope_retention_rate"),
        "retained_top3_reference_in_scope_retention_rate": _metadata_value(
            retained_top3_reference,
            "in_scope_retention_rate",
        ),
        "selected_top3_retained_accuracy_in_scope": _metadata_value(
            selected,
            "top3_retained_accuracy_in_scope",
        ),
        "legacy_top3_retained_accuracy_in_scope": _metadata_value(
            legacy_selected,
            "top3_retained_accuracy_in_scope",
        ),
        "retained_top3_reference_top3_retained_accuracy_in_scope": _metadata_value(
            retained_top3_reference,
            "top3_retained_accuracy_in_scope",
        ),
        "selected_in_scope_retention_rate_evaluable": _metadata_value(
            selected,
            "in_scope_retention_rate_evaluable",
        ),
        "retained_top3_reference_in_scope_retention_rate_evaluable": _metadata_value(
            retained_top3_reference,
            "in_scope_retention_rate_evaluable",
        ),
        "selected_top3_retained_accuracy_in_scope_evaluable": _metadata_value(
            selected,
            "top3_retained_accuracy_in_scope_evaluable",
        ),
        "retained_top3_reference_top3_retained_accuracy_in_scope_evaluable": _metadata_value(
            retained_top3_reference,
            "top3_retained_accuracy_in_scope_evaluable",
        ),
        "selected_out_of_scope_false_non_abstentions_evaluable": _metadata_value(
            selected,
            "out_of_scope_false_non_abstentions_evaluable",
        ),
        "retained_top3_reference_out_of_scope_false_non_abstentions_evaluable": _metadata_value(
            retained_top3_reference,
            "out_of_scope_false_non_abstentions_evaluable",
        ),
    }


def _has_zero_out_of_scope_false_non_abstentions(row: dict[str, Any]) -> bool:
    false_non_abstentions = row.get(
        "out_of_scope_false_non_abstentions_evaluable",
        row.get("out_of_scope_false_non_abstentions"),
    )
    if isinstance(false_non_abstentions, int):
        return false_non_abstentions == 0
    rate = row.get("out_of_scope_abstention_rate_evaluable", row.get("out_of_scope_abstention_rate"))
    return _same_float(float(rate or 0.0), 1.0)


def _row_metric(row: dict[str, Any], preferred: str, fallback: str) -> float:
    value = row.get(preferred)
    if value is None:
        value = row.get(fallback)
    return float(value or 0.0)


def _threshold_value(row: dict[str, Any] | None) -> float | None:
    if not row:
        return None
    value = row.get("abstain_threshold")
    return float(value) if value is not None else None


def _metadata_value(row: dict[str, Any] | None, key: str) -> Any:
    if not row:
        return None
    return row.get(key)


def _comparison_metric(row: dict[str, Any] | None, preferred: str, fallback: str) -> float:
    if not row:
        return 0.0
    return _row_metric(row, preferred, fallback)


def _is_geometry_evaluable(result: dict[str, Any]) -> bool:
    status = result.get("status")
    if status is None:
        return True
    return status == "ok" and int(result.get("resolved_residue_count", 0) or 0) > 0


def _same_float(left: float, right: float) -> bool:
    return abs(left - right) <= 1e-9


def classify_out_of_scope_failure(
    top1: dict[str, Any],
    abstain_threshold: float = 0.7,
) -> str:
    score = float(top1.get("score", 0.0) or 0.0)
    residue = float(top1.get("residue_match_fraction", 0.0) or 0.0)
    role = float(top1.get("role_match_fraction", 0.0) or 0.0)
    cofactor = float(top1.get("cofactor_context_score", 0.0) or 0.0)
    pocket = float(top1.get("substrate_pocket_score", 0.0) or 0.0)
    compactness = float(top1.get("compactness_score", 0.0) or 0.0)

    margin = score - abstain_threshold
    if margin <= 0.05:
        return "near_threshold"

    high_signals = sum(1 for value in [residue, role, cofactor, pocket] if value >= 0.6)
    if high_signals >= 2:
        return "mixed_signal_overlap"

    if cofactor >= 0.65 and max(residue, role, pocket) < 0.45:
        return "cofactor_dominant"
    if pocket >= 0.65 and max(residue, role, cofactor) < 0.45:
        return "pocket_dominant"
    if compactness >= 0.85 and max(residue, role, cofactor, pocket) < 0.45:
        return "compactness_dominant"
    if residue >= 0.65 or role >= 0.65:
        return "signature_overlap_dominant"
    return "unclear_mixed"


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)
