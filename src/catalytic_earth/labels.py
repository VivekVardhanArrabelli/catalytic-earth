from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .sources import PROJECT_ROOT


LABEL_REGISTRY = PROJECT_ROOT / "data" / "registries" / "curated_mechanism_labels.json"


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

        if label.fingerprint_id:
            in_scope_total += 1
            is_top1 = top1_id == label.fingerprint_id
            is_top3 = label.fingerprint_id in top3_ids
            top1_correct += int(is_top1)
            top3_correct += int(is_top3)
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
                "top1_correct": is_top1,
                "top3_correct": is_top3,
                "abstained": abstained,
                "rationale": label.rationale,
            }
        )

    return {
        "metadata": {
            "method": "geometry_retrieval_against_curated_seed_labels",
            "evaluated_count": len(rows),
            "in_scope_count": in_scope_total,
            "out_of_scope_count": out_scope_total,
            "abstain_threshold": abstain_threshold,
            "top1_accuracy_in_scope": _ratio(top1_correct, in_scope_total),
            "top3_accuracy_in_scope": _ratio(top3_correct, in_scope_total),
            "out_of_scope_abstention_rate": _ratio(out_scope_abstained, out_scope_total),
            "label_summary": label_summary(labels),
        },
        "rows": sorted(rows, key=lambda row: row["entry_id"]),
    }


def sweep_abstention_thresholds(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    thresholds: list[float] | None = None,
) -> dict[str, Any]:
    if thresholds is None:
        thresholds = [round(index / 20, 2) for index in range(0, 21)]
    rows = [
        evaluate_geometry_retrieval(retrieval, labels, abstain_threshold=threshold)["metadata"]
        for threshold in thresholds
    ]
    selected = select_threshold(rows)
    return {
        "metadata": {
            "method": "abstention_threshold_sweep",
            "threshold_count": len(rows),
            "selected_threshold": selected.get("abstain_threshold") if selected else None,
            "selection_rule": "maximize top3 in-scope accuracy, then out-of-scope abstention, then coverage",
        },
        "thresholds": rows,
        "selected": selected,
    }


def select_threshold(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None

    def score(row: dict[str, Any]) -> tuple[float, float, float, float]:
        top3 = row.get("top3_accuracy_in_scope") or 0.0
        abstention = row.get("out_of_scope_abstention_rate") or 0.0
        threshold = float(row.get("abstain_threshold") or 0.0)
        coverage = 1.0 - threshold
        return (top3, abstention, coverage, -threshold)

    return max(rows, key=score)


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)
