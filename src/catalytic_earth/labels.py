from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .ontology import fingerprint_family, load_mechanism_ontology
from .sources import PROJECT_ROOT
from .structure import COFACTOR_LIGAND_MAP, METAL_ION_CODES


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
COFACTOR_EVIDENCE_LIMITED_STATUSES = {
    "expected_absent_from_structure",
    "expected_structure_only",
}
LABEL_TIERS = {"bronze", "silver", "gold"}
REVIEW_STATUSES = {
    "unreviewed",
    "automation_curated",
    "needs_expert_review",
    "expert_reviewed",
    "rejected",
}
COUNTABLE_REVIEW_STATUSES = {"automation_curated", "expert_reviewed"}
CONFIDENCE_EVIDENCE_SCORES = {
    "high": 0.85,
    "medium": 0.65,
    "low": 0.4,
}


@dataclass(frozen=True)
class MechanismLabel:
    entry_id: str
    fingerprint_id: str | None
    label_type: str
    confidence: str
    rationale: str
    tier: str = "bronze"
    review_status: str = "automation_curated"
    evidence_score: float = 0.65
    evidence: dict[str, Any] = field(
        default_factory=lambda: {
            "sources": ["curator_rationale"],
            "retrieval_score": None,
            "cofactor_evidence_level": None,
            "conflicts": [],
            "notes": [],
            "migration": "label_factory_v1_default",
        }
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MechanismLabel":
        data = migrate_label_record(data)
        entry_id = data.get("entry_id")
        fingerprint_id = data.get("fingerprint_id")
        label_type = data.get("label_type")
        tier = data.get("tier")
        review_status = data.get("review_status")
        confidence = data.get("confidence")
        evidence_score = data.get("evidence_score")
        evidence = data.get("evidence")
        rationale = data.get("rationale")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValueError("entry_id must be a non-empty string")
        if fingerprint_id is not None and not isinstance(fingerprint_id, str):
            raise ValueError(f"{entry_id}: fingerprint_id must be null or string")
        if label_type not in {"seed_fingerprint", "out_of_scope"}:
            raise ValueError(f"{entry_id}: invalid label_type")
        if tier not in LABEL_TIERS:
            raise ValueError(f"{entry_id}: invalid tier")
        if review_status not in REVIEW_STATUSES:
            raise ValueError(f"{entry_id}: invalid review_status")
        if confidence not in {"high", "medium", "low"}:
            raise ValueError(f"{entry_id}: invalid confidence")
        if not isinstance(evidence_score, (int, float)) or not 0 <= float(evidence_score) <= 1:
            raise ValueError(f"{entry_id}: evidence_score must be between 0 and 1")
        if not isinstance(evidence, dict):
            raise ValueError(f"{entry_id}: evidence must be an object")
        sources = evidence.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError(f"{entry_id}: evidence.sources must be a non-empty list")
        if not all(isinstance(source, str) and source for source in sources):
            raise ValueError(f"{entry_id}: evidence.sources must contain non-empty strings")
        if not isinstance(rationale, str) or len(rationale) < 20:
            raise ValueError(f"{entry_id}: rationale is too short")
        if label_type == "seed_fingerprint" and not fingerprint_id:
            raise ValueError(f"{entry_id}: seed_fingerprint requires fingerprint_id")
        if label_type == "out_of_scope" and fingerprint_id is not None:
            raise ValueError(f"{entry_id}: out_of_scope requires null fingerprint_id")
        if tier == "gold" and review_status != "expert_reviewed":
            raise ValueError(f"{entry_id}: gold labels require expert_reviewed status")
        return cls(
            entry_id=entry_id,
            fingerprint_id=fingerprint_id,
            label_type=label_type,
            tier=tier,
            review_status=review_status,
            confidence=confidence,
            evidence_score=round(float(evidence_score), 4),
            evidence=dict(evidence),
            rationale=rationale,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "fingerprint_id": self.fingerprint_id,
            "label_type": self.label_type,
            "tier": self.tier,
            "review_status": self.review_status,
            "confidence": self.confidence,
            "evidence_score": self.evidence_score,
            "evidence": self.evidence,
            "rationale": self.rationale,
        }


def migrate_label_record(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("label record must be an object")
    confidence = data.get("confidence")
    default_score = CONFIDENCE_EVIDENCE_SCORES.get(str(confidence), 0.4)
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        evidence = {}
    sources = evidence.get("sources")
    if not isinstance(sources, list) or not sources:
        sources = ["curator_rationale"]
    migrated_evidence = {
        **evidence,
        "sources": [str(source) for source in sources if str(source)],
        "retrieval_score": evidence.get("retrieval_score"),
        "cofactor_evidence_level": evidence.get("cofactor_evidence_level"),
        "conflicts": evidence.get("conflicts", []),
        "notes": evidence.get("notes", []),
        "migration": evidence.get("migration", "label_factory_v1_default"),
    }
    return {
        **data,
        "tier": data.get("tier", "bronze"),
        "review_status": data.get("review_status", "automation_curated"),
        "evidence_score": data.get("evidence_score", default_score),
        "evidence": migrated_evidence,
    }


def migrate_label_registry_records(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [MechanismLabel.from_dict(item).to_dict() for item in data]


def load_labels(path: Path = LABEL_REGISTRY) -> list[MechanismLabel]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("label registry must be a list")
    labels = [MechanismLabel.from_dict(item) for item in data]
    duplicates = [entry_id for entry_id, count in Counter(label.entry_id for label in labels).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate labels: {', '.join(sorted(duplicates))}")
    _validate_label_fingerprints(labels)
    return labels


def label_summary(labels: list[MechanismLabel]) -> dict[str, Any]:
    evidence_scores = [label.evidence_score for label in labels]
    return {
        "label_count": len(labels),
        "by_type": dict(sorted(Counter(label.label_type for label in labels).items())),
        "by_tier": dict(sorted(Counter(label.tier for label in labels).items())),
        "by_review_status": dict(
            sorted(Counter(label.review_status for label in labels).items())
        ),
        "by_confidence": dict(sorted(Counter(label.confidence for label in labels).items())),
        "by_fingerprint": dict(
            sorted(Counter(label.fingerprint_id for label in labels if label.fingerprint_id).items())
        ),
        "mean_evidence_score": (
            round(sum(evidence_scores) / len(evidence_scores), 4) if evidence_scores else None
        ),
    }


def countable_benchmark_labels(labels: list[MechanismLabel]) -> list[MechanismLabel]:
    return [
        label
        for label in labels
        if label.review_status in COUNTABLE_REVIEW_STATUSES
    ]


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
                "context": _retrieval_result_context(result),
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


def analyze_in_scope_failures(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    rows: list[dict[str, Any]] = []
    evaluated_in_scope = 0
    retained_in_scope = 0
    top1_correct = 0

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label or label.label_type != "seed_fingerprint" or not label.fingerprint_id:
            continue
        evaluated_in_scope += 1
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_score = float(top1.get("score", 0.0) or 0.0)
        abstained = top1_score < abstain_threshold
        retained_in_scope += int(not abstained)
        is_top1 = top1.get("fingerprint_id") == label.fingerprint_id
        top1_correct += int(is_top1)
        target_cofactor_coverage = _cofactor_coverage_row_parts(
            result,
            fingerprints_by_id.get(label.fingerprint_id, {}),
        )

        target_rank = None
        target_score = None
        target_fingerprint = None
        for index, fingerprint in enumerate(top, start=1):
            if fingerprint.get("fingerprint_id") == label.fingerprint_id:
                target_rank = index
                target_score = float(fingerprint.get("score", 0.0) or 0.0)
                target_fingerprint = fingerprint
                break

        if is_top1 and not abstained:
            continue

        failure_modes = []
        if not is_top1:
            failure_modes.append("top1_mismatch")
        if target_rank is None:
            failure_modes.append("target_absent_from_top_k")
        if abstained:
            failure_modes.append("abstained_positive")

        row = {
            "entry_id": entry_id,
            "target_fingerprint_id": label.fingerprint_id,
            "top1_fingerprint_id": top1.get("fingerprint_id"),
            "top1_score": round(top1_score, 4),
            "top1_cofactor_evidence_level": top1.get("cofactor_evidence_level"),
            "target_rank": target_rank,
            "target_score": round(target_score, 4) if target_score is not None else None,
            "target_cofactor_evidence_level": (target_fingerprint or {}).get(
                "cofactor_evidence_level"
            ),
            "score_gap_top1_minus_target": (
                round(top1_score - target_score, 4) if target_score is not None else None
            ),
            "abstain_threshold": abstain_threshold,
            "abstained": abstained,
            "failure_modes": failure_modes,
            "status": result.get("status"),
            "resolved_residue_count": result.get("resolved_residue_count", 0),
            "evaluable": _is_geometry_evaluable(result),
            "top1_component_scores": _fingerprint_component_scores(top1),
            "target_component_scores": _fingerprint_component_scores(target_fingerprint or {}),
            "target_expected_cofactor_families": target_cofactor_coverage[
                "expected_cofactor_families"
            ],
            "target_cofactor_coverage_status": target_cofactor_coverage[
                "coverage_status"
            ],
            "target_missing_expected_cofactor_families": target_cofactor_coverage[
                "missing_expected_families"
            ],
            "context": _retrieval_result_context(result),
            "label_rationale": label.rationale,
        }
        row["failure_cause"] = _classify_in_scope_failure(row)
        rows.append(row)

    failure_mode_counts = Counter(mode for row in rows for mode in row["failure_modes"])
    target_fingerprint_counts = Counter(row["target_fingerprint_id"] for row in rows)
    top1_fingerprint_counts = Counter(row["top1_fingerprint_id"] for row in rows)
    target_evidence_counts = Counter(
        row.get("target_cofactor_evidence_level") or "not_ranked" for row in rows
    )
    failure_cause_counts = Counter(row["failure_cause"] for row in rows)
    evidence_limited_abstentions = [
        row
        for row in rows
        if row["abstained"]
        and row["failure_cause"]
        in {"target_cofactor_absent_from_structure", "target_cofactor_not_proximal"}
    ]
    return {
        "metadata": {
            "method": "in_scope_geometry_failure_analysis",
            "evaluated_in_scope_count": evaluated_in_scope,
            "failure_count": len(rows),
            "actionable_failure_count": len(rows) - len(evidence_limited_abstentions),
            "evidence_limited_abstention_count": len(evidence_limited_abstentions),
            "top1_mismatch_count": int(failure_mode_counts.get("top1_mismatch", 0)),
            "abstained_positive_count": int(failure_mode_counts.get("abstained_positive", 0)),
            "target_absent_from_top_k_count": int(
                failure_mode_counts.get("target_absent_from_top_k", 0)
            ),
            "retained_in_scope_count": retained_in_scope,
            "top1_correct_count": top1_correct,
            "abstain_threshold": abstain_threshold,
            "failure_mode_counts": dict(sorted(failure_mode_counts.items())),
            "failure_cause_counts": dict(sorted(failure_cause_counts.items())),
            "target_cofactor_evidence_counts": dict(sorted(target_evidence_counts.items())),
            "target_fingerprint_counts": dict(sorted(target_fingerprint_counts.items())),
            "top1_fingerprint_counts": dict(sorted(top1_fingerprint_counts.items())),
        },
        "rows": sorted(rows, key=lambda row: row["entry_id"]),
    }


def analyze_cofactor_coverage(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    rows: list[dict[str, Any]] = []

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label or label.label_type != "seed_fingerprint" or not label.fingerprint_id:
            continue

        fingerprint = fingerprints_by_id.get(label.fingerprint_id, {})
        coverage = _cofactor_coverage_row_parts(result, fingerprint)
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_score = float(top1.get("score", 0.0) or 0.0)
        rows.append(
            {
                "entry_id": entry_id,
                "target_fingerprint_id": label.fingerprint_id,
                **coverage,
                "top1_fingerprint_id": top1.get("fingerprint_id"),
                "top1_score": round(top1_score, 4),
                "abstained": top1_score < abstain_threshold,
                "status": result.get("status"),
                "resolved_residue_count": result.get("resolved_residue_count", 0),
                "evaluable": _is_geometry_evaluable(result),
                "context": _retrieval_result_context(result),
            }
        )

    status_counts = Counter(row["coverage_status"] for row in rows)
    target_counts = Counter(row["target_fingerprint_id"] for row in rows)
    missing_counts = Counter(
        family for row in rows for family in row["missing_expected_families"]
    )
    expected_absent_rows = [
        row for row in rows if row["coverage_status"] == "expected_absent_from_structure"
    ]
    structure_only_rows = [
        row for row in rows if row["coverage_status"] == "expected_structure_only"
    ]
    evidence_limited_rows = expected_absent_rows + structure_only_rows
    expected_absent_retained_rows = [
        row for row in expected_absent_rows if not row["abstained"]
    ]
    expected_absent_abstained_rows = [
        row for row in expected_absent_rows if row["abstained"]
    ]
    structure_only_retained_rows = [
        row for row in structure_only_rows if not row["abstained"]
    ]
    structure_only_abstained_rows = [
        row for row in structure_only_rows if row["abstained"]
    ]
    evidence_limited_retained_rows = [
        row for row in evidence_limited_rows if not row["abstained"]
    ]
    evidence_limited_abstained_rows = [
        row for row in evidence_limited_rows if row["abstained"]
    ]
    return {
        "metadata": {
            "method": "in_scope_cofactor_coverage_analysis",
            "evaluated_in_scope_count": len(rows),
            "abstain_threshold": abstain_threshold,
            "coverage_status_counts": dict(sorted(status_counts.items())),
            "target_fingerprint_counts": dict(sorted(target_counts.items())),
            "missing_expected_family_counts": dict(sorted(missing_counts.items())),
            "structure_only_count": int(status_counts.get("expected_structure_only", 0)),
            "expected_absent_count": int(
                status_counts.get("expected_absent_from_structure", 0)
            ),
            "expected_absent_entry_ids": sorted(
                (row["entry_id"] for row in expected_absent_rows),
                key=_entry_id_sort_key,
            ),
            "expected_absent_abstained_count": len(expected_absent_abstained_rows),
            "expected_absent_abstained_entry_ids": sorted(
                (row["entry_id"] for row in expected_absent_abstained_rows),
                key=_entry_id_sort_key,
            ),
            "expected_absent_retained_count": len(expected_absent_retained_rows),
            "expected_absent_retained_entry_ids": sorted(
                (row["entry_id"] for row in expected_absent_retained_rows),
                key=_entry_id_sort_key,
            ),
            "structure_only_retained_count": len(structure_only_retained_rows),
            "structure_only_retained_entry_ids": sorted(
                (row["entry_id"] for row in structure_only_retained_rows),
                key=_entry_id_sort_key,
            ),
            "structure_only_abstained_count": len(structure_only_abstained_rows),
            "structure_only_abstained_entry_ids": sorted(
                (row["entry_id"] for row in structure_only_abstained_rows),
                key=_entry_id_sort_key,
            ),
            "structure_only_entry_ids": sorted(
                (row["entry_id"] for row in structure_only_rows),
                key=_entry_id_sort_key,
            ),
            "evidence_limited_retained_count": len(evidence_limited_retained_rows),
            "evidence_limited_retained_entry_ids": sorted(
                (row["entry_id"] for row in evidence_limited_retained_rows),
                key=_entry_id_sort_key,
            ),
            "evidence_limited_abstained_count": len(evidence_limited_abstained_rows),
            "evidence_limited_abstained_entry_ids": sorted(
                (row["entry_id"] for row in evidence_limited_abstained_rows),
                key=_entry_id_sort_key,
            ),
            "local_supported_count": int(
                status_counts.get("all_expected_local", 0)
                + status_counts.get("partial_expected_local", 0)
            ),
        },
        "rows": sorted(rows, key=lambda row: _entry_id_sort_key(str(row["entry_id"]))),
    }


def analyze_cofactor_abstention_policy(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
    absent_penalties: list[float] | None = None,
    structure_only_penalties: list[float] | None = None,
) -> dict[str, Any]:
    absent_penalties = _normalize_penalty_grid(absent_penalties or [0.0, 0.01, 0.02, 0.05, 0.08, 0.10])
    structure_only_penalties = _normalize_penalty_grid(
        structure_only_penalties or [0.0, 0.005, 0.01, 0.02, 0.05]
    )
    base_adjusted = apply_cofactor_score_policy(
        retrieval,
        absent_penalty=0.0,
        structure_only_penalty=0.0,
    )
    base_rows = _cofactor_policy_detail_rows(base_adjusted, labels, abstain_threshold)
    sensitivity_rows = _cofactor_policy_sensitivity_rows(base_rows, abstain_threshold)
    base_retained_positive_ids = _retained_positive_ids(base_rows)
    base_evidence_limited_retained_ids = _evidence_limited_retained_positive_ids(base_rows)
    base_rows_by_entry = {row["entry_id"]: row for row in base_rows}

    policies: list[dict[str, Any]] = []
    policy_detail_rows: dict[tuple[float, float], list[dict[str, Any]]] = {}
    for absent_penalty in absent_penalties:
        for structure_only_penalty in structure_only_penalties:
            adjusted = apply_cofactor_score_policy(
                retrieval,
                absent_penalty=absent_penalty,
                structure_only_penalty=structure_only_penalty,
            )
            rows = _cofactor_policy_detail_rows(adjusted, labels, abstain_threshold)
            policy_detail_rows[(absent_penalty, structure_only_penalty)] = rows
            evaluation = evaluate_geometry_retrieval(
                adjusted,
                labels,
                abstain_threshold=abstain_threshold,
            )
            margins = analyze_geometry_score_margins(adjusted, labels)
            hard_negatives = build_hard_negative_controls(adjusted, labels)
            retained_positive_ids = _retained_positive_ids(rows)
            evidence_limited_retained_ids = _evidence_limited_retained_positive_ids(rows)
            evidence_limited_abstained_ids = _evidence_limited_abstained_positive_ids(rows)
            lost_retained_positive_ids = sorted(
                base_retained_positive_ids - retained_positive_ids,
                key=_entry_id_sort_key,
            )
            newly_retained_positive_ids = sorted(
                retained_positive_ids - base_retained_positive_ids,
                key=_entry_id_sort_key,
            )
            changed_top1_ids = []
            changed_abstention_ids = []
            for row in rows:
                base_row = base_rows_by_entry.get(row["entry_id"])
                if not base_row:
                    continue
                if row["top1_fingerprint_id"] != base_row["top1_fingerprint_id"]:
                    changed_top1_ids.append(row["entry_id"])
                if row["abstained"] != base_row["abstained"]:
                    changed_abstention_ids.append(row["entry_id"])

            eval_meta = evaluation["metadata"]
            margin_meta = margins["metadata"]
            hard_meta = hard_negatives["metadata"]
            policies.append(
                {
                    "absent_penalty": absent_penalty,
                    "structure_only_penalty": structure_only_penalty,
                    "top3_retained_accuracy_in_scope_evaluable": eval_meta.get(
                        "top3_retained_accuracy_in_scope_evaluable"
                    ),
                    "in_scope_retention_rate_evaluable": eval_meta.get(
                        "in_scope_retention_rate_evaluable"
                    ),
                    "out_of_scope_false_non_abstentions_evaluable": eval_meta.get(
                        "out_of_scope_false_non_abstentions_evaluable"
                    ),
                    "hard_negative_count": hard_meta.get("hard_negative_count"),
                    "near_miss_count": hard_meta.get("near_miss_count"),
                    "correct_positive_score_separation_gap": margin_meta.get(
                        "correct_positive_score_separation_gap"
                    ),
                    "strict_threshold_exists_for_correct_positives": margin_meta.get(
                        "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope"
                    ),
                    "retained_positive_count": len(retained_positive_ids),
                    "lost_retained_positive_count": len(lost_retained_positive_ids),
                    "lost_retained_positive_entry_ids": lost_retained_positive_ids,
                    "newly_retained_positive_count": len(newly_retained_positive_ids),
                    "newly_retained_positive_entry_ids": newly_retained_positive_ids,
                    "evidence_limited_retained_positive_count": len(
                        evidence_limited_retained_ids
                    ),
                    "evidence_limited_retained_positive_entry_ids": sorted(
                        evidence_limited_retained_ids,
                        key=_entry_id_sort_key,
                    ),
                    "evidence_limited_abstained_positive_count": len(
                        evidence_limited_abstained_ids
                    ),
                    "evidence_limited_abstained_positive_entry_ids": sorted(
                        evidence_limited_abstained_ids,
                        key=_entry_id_sort_key,
                    ),
                    "changed_top1_count": len(changed_top1_ids),
                    "changed_top1_entry_ids": sorted(changed_top1_ids, key=_entry_id_sort_key),
                    "changed_abstention_count": len(changed_abstention_ids),
                    "changed_abstention_entry_ids": sorted(
                        changed_abstention_ids,
                        key=_entry_id_sort_key,
                    ),
                }
            )

    audit_policy = _find_policy(policies, absent_penalty=0.0, structure_only_penalty=0.0)
    guardrail_passing_policies = [
        row
        for row in policies
        if row["out_of_scope_false_non_abstentions_evaluable"] == 0
        and row["hard_negative_count"] == 0
        and row["lost_retained_positive_count"] == 0
    ]
    lossless_decision_changing_policies = [
        row
        for row in guardrail_passing_policies
        if row["evidence_limited_retained_positive_count"]
        < len(base_evidence_limited_retained_ids)
    ]
    if (
        audit_policy
        and (
            audit_policy["hard_negative_count"] > 0
            or audit_policy["out_of_scope_false_non_abstentions_evaluable"] > 0
        )
    ):
        recommendation = "cofactor_penalty_not_primary_blocker"
    elif lossless_decision_changing_policies:
        recommendation = "candidate_penalty_available"
    else:
        recommendation = "audit_only_or_separate_stratum"
    recommended_policy = (
        min(
            lossless_decision_changing_policies,
            key=lambda row: (
                row["evidence_limited_retained_positive_count"],
                row["absent_penalty"] + row["structure_only_penalty"],
            ),
        )
        if lossless_decision_changing_policies
        else audit_policy
    )
    return {
        "metadata": {
            "method": "cofactor_abstention_policy_sweep",
            "abstain_threshold": abstain_threshold,
            "policy_count": len(policies),
            "absent_penalties": absent_penalties,
            "structure_only_penalties": structure_only_penalties,
            "penalty_scope": (
                "post-hoc score subtraction for top-k fingerprint hits whose expected "
                "cofactor families are absent from the selected structure or only "
                "outside the local active-site neighborhood"
            ),
            "top_k_boundary": (
                "policy analysis reranks only the fingerprint hits already present in the retrieval artifact"
            ),
            "audit_evidence_limited_retained_positive_count": len(
                base_evidence_limited_retained_ids
            ),
            "audit_evidence_limited_retained_positive_entry_ids": sorted(
                base_evidence_limited_retained_ids,
                key=_entry_id_sort_key,
            ),
            "minimum_evidence_limited_retained_margin": min(
                (
                    row["score_margin_to_abstain_threshold"]
                    for row in sensitivity_rows
                    if row["retained_positive"]
                    and row["score_margin_to_abstain_threshold"] is not None
                ),
                default=None,
            ),
            "guardrail_passing_policy_count": len(guardrail_passing_policies),
            "lossless_decision_changing_policy_count": len(
                lossless_decision_changing_policies
            ),
            "recommendation": recommendation,
            "recommended_policy": recommended_policy,
        },
        "policies": sorted(
            policies,
            key=lambda row: (row["absent_penalty"], row["structure_only_penalty"]),
        ),
        "limiting_rows": _cofactor_policy_limiting_rows(
            policy_detail_rows,
            base_rows_by_entry,
        ),
        "sensitivity_rows": sensitivity_rows,
        "rows": sorted(base_rows, key=lambda row: _entry_id_sort_key(row["entry_id"])),
    }


def apply_cofactor_score_policy(
    retrieval: dict[str, Any],
    absent_penalty: float = 0.0,
    structure_only_penalty: float = 0.0,
) -> dict[str, Any]:
    if absent_penalty < 0 or structure_only_penalty < 0:
        raise ValueError("cofactor policy penalties must be non-negative")
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    adjusted_results: list[dict[str, Any]] = []
    for result in retrieval.get("results", []):
        top_fingerprints = result.get("top_fingerprints", [])
        adjusted_top: list[dict[str, Any]] = []
        for fingerprint_hit in top_fingerprints:
            if not isinstance(fingerprint_hit, dict):
                continue
            fingerprint_id = fingerprint_hit.get("fingerprint_id")
            fingerprint = fingerprints_by_id.get(str(fingerprint_id), {})
            coverage = _cofactor_coverage_row_parts(result, fingerprint)
            penalty = _cofactor_policy_penalty(
                coverage["coverage_status"],
                absent_penalty=absent_penalty,
                structure_only_penalty=structure_only_penalty,
            )
            base_score = float(
                fingerprint_hit.get("base_score", fingerprint_hit.get("score", 0.0)) or 0.0
            )
            adjusted_hit = dict(fingerprint_hit)
            adjusted_hit["base_score"] = round(base_score, 4)
            adjusted_hit["score"] = round(max(0.0, base_score - penalty), 4)
            adjusted_hit["cofactor_policy_penalty"] = round(penalty, 4)
            adjusted_hit["cofactor_policy_coverage_status"] = coverage["coverage_status"]
            adjusted_hit["cofactor_policy_expected_families"] = coverage[
                "expected_cofactor_families"
            ]
            adjusted_hit["cofactor_policy_missing_expected_families"] = coverage[
                "missing_expected_families"
            ]
            adjusted_hit["cofactor_policy_nearest_expected_ligand_distance_angstrom"] = (
                coverage["nearest_expected_ligand_distance_angstrom"]
            )
            adjusted_top.append(adjusted_hit)
        adjusted_result = dict(result)
        adjusted_result["top_fingerprints"] = sorted(
            adjusted_top,
            key=lambda item: (-float(item.get("score", 0.0) or 0.0), str(item.get("fingerprint_id"))),
        )
        adjusted_results.append(adjusted_result)

    metadata = dict(retrieval.get("metadata", {}))
    metadata["cofactor_policy"] = {
        "absent_penalty": round(absent_penalty, 4),
        "structure_only_penalty": round(structure_only_penalty, 4),
        "score_field": "score",
        "base_score_field": "base_score",
    }
    return {**retrieval, "metadata": metadata, "results": adjusted_results}


def analyze_seed_family_performance(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    in_scope_groups: dict[str, list[dict[str, Any]]] = {}
    out_scope_groups: dict[str, list[dict[str, Any]]] = {}

    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label:
            continue
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_id = str(top1.get("fingerprint_id") or "none")
        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        top3_ids = [item.get("fingerprint_id") for item in top[:3]]
        abstained = top1_score < abstain_threshold
        evaluable = _is_geometry_evaluable(result)
        if label.label_type == "seed_fingerprint" and label.fingerprint_id:
            target_coverage = _cofactor_coverage_row_parts(
                result,
                fingerprints_by_id.get(label.fingerprint_id, {}),
            )
            in_scope_groups.setdefault(label.fingerprint_id, []).append(
                {
                    "entry_id": label.entry_id,
                    "evaluable": evaluable,
                    "top1_fingerprint_id": top1_id,
                    "top1_score": top1_score,
                    "top1_correct": top1_id == label.fingerprint_id,
                    "top3_correct": label.fingerprint_id in top3_ids,
                    "abstained": abstained,
                    "cofactor_coverage_status": target_coverage["coverage_status"],
                }
            )
        elif label.label_type == "out_of_scope":
            out_scope_groups.setdefault(top1_id, []).append(
                {
                    "entry_id": label.entry_id,
                    "evaluable": evaluable,
                    "top1_fingerprint_id": top1_id,
                    "top1_score": top1_score,
                    "abstained": abstained,
                    "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                }
            )

    in_scope_rows = [
        _seed_family_in_scope_row(fingerprint_id, rows)
        for fingerprint_id, rows in in_scope_groups.items()
    ]
    out_scope_rows = [
        _seed_family_out_scope_row(fingerprint_id, rows)
        for fingerprint_id, rows in out_scope_groups.items()
    ]
    weakest_retained_rows = [
        row for row in in_scope_rows if row["evaluable_count"] > 0
    ]
    weakest_retained = min(
        weakest_retained_rows,
        key=lambda row: (
            row["top3_retained_accuracy_evaluable"] or 0.0,
            row["evaluable_count"],
            row["fingerprint_id"],
        ),
        default=None,
    )
    largest_family = max(
        in_scope_rows,
        key=lambda row: (row["labeled_count"], row["fingerprint_id"]),
        default=None,
    )
    return {
        "metadata": {
            "method": "seed_family_performance_audit",
            "abstain_threshold": abstain_threshold,
            "in_scope_family_count": len(in_scope_rows),
            "out_of_scope_top1_family_count": len(out_scope_rows),
            "largest_in_scope_family": (
                largest_family["fingerprint_id"] if largest_family else None
            ),
            "largest_in_scope_family_count": (
                largest_family["labeled_count"] if largest_family else 0
            ),
            "weakest_retained_in_scope_family": (
                weakest_retained["fingerprint_id"] if weakest_retained else None
            ),
            "weakest_retained_in_scope_family_accuracy": (
                weakest_retained["top3_retained_accuracy_evaluable"]
                if weakest_retained
                else None
            ),
            "out_of_scope_retained_family_count": sum(
                1 for row in out_scope_rows if row["false_non_abstention_count"] > 0
            ),
            "validation_boundary": (
                "small curated seed-family audit; not a learned family split benchmark"
            ),
        },
        "in_scope_families": sorted(
            in_scope_rows,
            key=lambda row: (-row["labeled_count"], row["fingerprint_id"]),
        ),
        "out_of_scope_top1_families": sorted(
            out_scope_rows,
            key=lambda row: (-row["count"], row["fingerprint_id"]),
        ),
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
                "context": _retrieval_result_context(result),
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
    strict_correct_positive_threshold_exists = (
        min_correct_in_scope_score is not None
        and max_out_scope_score is not None
        and max_out_scope_score < min_correct_in_scope_score
    )
    conflicting_out_scope = [
        row
        for row in out_scope_score_rows
        if min_in_scope_score is not None and row["top1_score"] >= min_in_scope_score
    ]
    conflicting_out_scope_against_correct_floor = [
        row
        for row in out_scope_score_rows
        if min_correct_in_scope_score is not None
        and row["top1_score"] >= min_correct_in_scope_score
    ]
    limiting_in_scope = [
        row
        for row in in_scope_score_rows
        if min_in_scope_score is not None and _same_float(row["top1_score"], min_in_scope_score)
    ]
    limiting_correct_in_scope = [
        row
        for row in correct_in_scope_score_rows
        if min_correct_in_scope_score is not None
        and _same_float(row["top1_score"], min_correct_in_scope_score)
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
            "correct_positive_score_separation_gap": (
                round(min_correct_in_scope_score - max_out_scope_score, 4)
                if min_correct_in_scope_score is not None and max_out_scope_score is not None
                else None
            ),
            "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope": (
                strict_threshold_exists
            ),
            "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope": (
                strict_correct_positive_threshold_exists
            ),
            "near_margin": near_margin,
            "score_margin_boundary_count": len(boundary_rows),
            "out_of_scope_entries_at_or_above_min_in_scope": len(conflicting_out_scope),
            "out_of_scope_entries_at_or_above_min_correct_in_scope": len(
                conflicting_out_scope_against_correct_floor
            ),
            "in_scope_entries_at_or_below_max_out_of_scope": len(in_scope_below_max_out_scope),
            "cofactor_evidence_counts": dict(sorted(cofactor_evidence_counts.items())),
        },
        "conflicting_out_of_scope_rows": sorted(
            conflicting_out_scope,
            key=lambda row: (-row["top1_score"], row["entry_id"]),
        ),
        "conflicting_out_of_scope_against_correct_floor_rows": sorted(
            conflicting_out_scope_against_correct_floor,
            key=lambda row: (-row["top1_score"], row["entry_id"]),
        ),
        "limiting_in_scope_rows": sorted(limiting_in_scope, key=lambda row: row["entry_id"]),
        "limiting_correct_in_scope_rows": sorted(
            limiting_correct_in_scope,
            key=lambda row: row["entry_id"],
        ),
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
                "near_miss_top1_fingerprint_counts": {},
                "near_miss_cofactor_evidence_counts": {},
                "closest_near_miss_entry_id": None,
                "closest_near_miss_top1_fingerprint_id": None,
                "minimum_near_miss_score_gap_to_floor": None,
                "closest_below_floor_entry_id": None,
                "closest_below_floor_top1_fingerprint_id": None,
                "minimum_below_floor_score_gap": None,
            },
            "rows": [],
            "near_miss_rows": [],
            "closest_below_floor_rows": [],
            "groups": [],
            "near_miss_groups": [],
        }
    floor = float(score_floor if score_floor is not None else inferred_floor)
    labels_by_entry = {label.entry_id: label for label in labels}
    rows: list[dict[str, Any]] = []
    near_miss_rows: list[dict[str, Any]] = []
    below_floor_rows: list[dict[str, Any]] = []

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
            below_floor_row = {
                **_hard_negative_row(
                    label=label,
                    result=result,
                    top1=top1,
                    top1_score=top1_score,
                    score_floor=floor,
                    negative_control_type="below_in_scope_floor",
                ),
                "score_gap_to_floor": round(floor - top1_score, 4),
            }
            below_floor_rows.append(below_floor_row)
            if below_floor_row["score_gap_to_floor"] <= near_margin:
                near_miss_rows.append(
                    {
                        **below_floor_row,
                        "negative_control_type": "near_miss_below_in_scope_floor",
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
    near_miss_fingerprint_counts = Counter(
        row["top1_fingerprint_id"] for row in near_miss_rows
    )
    near_miss_cofactor_evidence_counts = Counter(
        row.get("cofactor_evidence_level") or "unknown" for row in near_miss_rows
    )
    groups = group_hard_negative_controls(rows)
    near_miss_groups = group_hard_negative_controls(near_miss_rows)
    closest_near_miss = min(
        near_miss_rows,
        key=lambda row: (
            float(row.get("score_gap_to_floor", float("inf"))),
            str(row.get("entry_id", "")),
        ),
        default={},
    )
    closest_below_floor_rows = sorted(
        below_floor_rows,
        key=lambda row: (float(row["score_gap_to_floor"]), row["entry_id"]),
    )[:10]
    closest_below_floor = closest_below_floor_rows[0] if closest_below_floor_rows else {}
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
            "near_miss_top1_fingerprint_counts": dict(
                sorted(near_miss_fingerprint_counts.items())
            ),
            "near_miss_cofactor_evidence_counts": dict(
                sorted(near_miss_cofactor_evidence_counts.items())
            ),
            "closest_near_miss_entry_id": closest_near_miss.get("entry_id"),
            "closest_near_miss_top1_fingerprint_id": closest_near_miss.get(
                "top1_fingerprint_id"
            ),
            "minimum_near_miss_score_gap_to_floor": closest_near_miss.get(
                "score_gap_to_floor"
            ),
            "closest_below_floor_entry_id": closest_below_floor.get("entry_id"),
            "closest_below_floor_top1_fingerprint_id": closest_below_floor.get(
                "top1_fingerprint_id"
            ),
            "minimum_below_floor_score_gap": closest_below_floor.get(
                "score_gap_to_floor"
            ),
        },
        "rows": sorted(rows, key=lambda row: (-row["top1_score"], row["entry_id"])),
        "near_miss_rows": sorted(
            near_miss_rows,
            key=lambda row: (row["score_gap_to_floor"], row["entry_id"]),
        ),
        "closest_below_floor_rows": closest_below_floor_rows,
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
        gap_values = [
            float(row["score_gap_to_floor"])
            for row in group_rows
            if row.get("score_gap_to_floor") is not None
        ]
        reasons = Counter(str(row.get("hard_negative_reason") or "unknown") for row in group_rows)
        counterevidence_reasons = Counter(
            str(reason)
            for row in group_rows
            for reason in _counterevidence_reasons_from_row(row)
            if reason
        )
        result.append(
            {
                "top1_fingerprint_id": fingerprint_id,
                "cofactor_evidence_level": evidence_level,
                "count": len(group_rows),
                "min_top1_score": round(min(scores), 4),
                "mean_top1_score": round(sum(scores) / len(scores), 4),
                "max_top1_score": round(max(scores), 4),
                "min_score_gap_to_floor": (
                    round(min(gap_values), 4) if gap_values else None
                ),
                "mean_score_gap_to_floor": (
                    round(sum(gap_values) / len(gap_values), 4) if gap_values else None
                ),
                "max_score_gap_to_floor": (
                    round(max(gap_values), 4) if gap_values else None
                ),
                "hard_negative_reason_counts": dict(sorted(reasons.items())),
                "counterevidence_reason_counts": dict(
                    sorted(counterevidence_reasons.items())
                ),
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


def _counterevidence_reasons_from_row(row: dict[str, Any]) -> list[str]:
    component_scores = row.get("component_scores", {})
    if not isinstance(component_scores, dict):
        return []
    reasons = component_scores.get("counterevidence_reasons", [])
    if not isinstance(reasons, list):
        return []
    return [str(reason) for reason in reasons if reason]


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
            **_fingerprint_component_scores(top1),
        },
        "label_rationale": label.rationale,
    }


def _fingerprint_component_scores(fingerprint: dict[str, Any]) -> dict[str, Any]:
    counterevidence_reasons = fingerprint.get("counterevidence_reasons", [])
    if not isinstance(counterevidence_reasons, list):
        counterevidence_reasons = []
    penalty_details = fingerprint.get("counterevidence_penalty_details", [])
    if not isinstance(penalty_details, list):
        penalty_details = []
    return {
        "residue_match_fraction": float(fingerprint.get("residue_match_fraction", 0.0) or 0.0),
        "role_match_fraction": float(fingerprint.get("role_match_fraction", 0.0) or 0.0),
        "cofactor_context_score": float(fingerprint.get("cofactor_context_score", 0.0) or 0.0),
        "substrate_pocket_score": float(fingerprint.get("substrate_pocket_score", 0.0) or 0.0),
        "compactness_score": float(fingerprint.get("compactness_score", 0.0) or 0.0),
        "mechanistic_coherence_score": float(
            fingerprint.get("mechanistic_coherence_score", 0.0) or 0.0
        ),
        "counterevidence_penalty": float(
            fingerprint.get("counterevidence_penalty", 1.0) or 0.0
        ),
        "counterevidence_reasons": list(counterevidence_reasons),
        "counterevidence_penalty_details": [
            detail for detail in penalty_details if isinstance(detail, dict)
        ],
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
    mechanism_text_snippets = result.get("mechanism_text_snippets", [])
    if not isinstance(mechanism_text_snippets, list):
        mechanism_text_snippets = []
    return {
        "entry_name": result.get("entry_name"),
        "pdb_id": result.get("pdb_id"),
        "mechanism_text_count": int(result.get("mechanism_text_count", 0) or 0),
        "mechanism_text_snippets": mechanism_text_snippets,
        "residue_codes": result.get("residue_codes", []),
        "ligand_codes": ligand_context.get("ligand_codes", []),
        "cofactor_families": ligand_context.get("cofactor_families", []),
        "structure_ligand_codes": ligand_context.get("structure_ligand_codes", []),
        "structure_cofactor_families": ligand_context.get(
            "structure_cofactor_families", []
        ),
        "nearby_residue_count": pocket_context.get("nearby_residue_count", 0),
        "pocket_descriptors": descriptors,
    }


def _classify_in_scope_failure(row: dict[str, Any]) -> str:
    if "target_absent_from_top_k" in row.get("failure_modes", []):
        return "target_absent_from_top_k"
    if (row.get("target_cofactor_evidence_level") or "not_ranked") == "absent":
        if row.get("target_cofactor_coverage_status") == "expected_absent_from_structure":
            return "target_cofactor_absent_from_structure"
        if row.get("target_cofactor_coverage_status") == "expected_structure_only":
            return "target_cofactor_not_proximal"
        return "target_cofactor_context_absent"
    if row.get("abstained") and row.get("top1_fingerprint_id") == row.get("target_fingerprint_id"):
        return "low_confidence_correct_top1"
    if row.get("abstained"):
        return "low_confidence_top1_mismatch"
    return "top1_mismatch"


def _cofactor_coverage_row_parts(
    result: dict[str, Any],
    fingerprint: dict[str, Any],
) -> dict[str, Any]:
    expected = _expected_cofactor_families(fingerprint)
    ligand_context = result.get("ligand_context", {})
    if not isinstance(ligand_context, dict):
        ligand_context = {}
    local = {
        str(value)
        for value in ligand_context.get("cofactor_families", [])
        if isinstance(value, str)
    }
    structure = {
        str(value)
        for value in ligand_context.get("structure_cofactor_families", [])
        if isinstance(value, str)
    }
    structure |= local
    local_matches = expected & local
    structure_matches = expected & structure
    matching_structure_ligands = _matching_structure_ligands(ligand_context, expected)
    matching_distances = [
        float(item["min_distance_to_active_site"])
        for item in matching_structure_ligands
        if item.get("min_distance_to_active_site") is not None
    ]
    return {
        "expected_cofactor_families": sorted(expected),
        "local_cofactor_families": sorted(local),
        "structure_cofactor_families": sorted(structure),
        "local_matches": sorted(local_matches),
        "structure_matches": sorted(structure_matches),
        "missing_expected_families": sorted(expected - structure),
        "matching_structure_ligands": matching_structure_ligands,
        "nearest_expected_ligand_distance_angstrom": (
            round(min(matching_distances), 3) if matching_distances else None
        ),
        "coverage_status": _cofactor_coverage_status(
            expected=expected,
            local_matches=local_matches,
            structure_matches=structure_matches,
        ),
        "structure_ligand_codes": ligand_context.get("structure_ligand_codes", []),
        "proximal_ligand_codes": ligand_context.get("ligand_codes", []),
    }


def _matching_structure_ligands(
    ligand_context: dict[str, Any],
    expected_families: set[str],
) -> list[dict[str, Any]]:
    if not expected_families:
        return []
    ligands = ligand_context.get("structure_ligands", [])
    if not isinstance(ligands, list):
        return []
    matches: list[dict[str, Any]] = []
    for ligand in ligands:
        if not isinstance(ligand, dict):
            continue
        family = _ligand_code_family(str(ligand.get("code", "")))
        if family not in expected_families:
            continue
        matches.append(
            {
                "code": ligand.get("code"),
                "family": family,
                "min_distance_to_active_site": ligand.get("min_distance_to_active_site"),
                "instance_count": ligand.get("instance_count"),
            }
        )
    return sorted(
        matches,
        key=lambda item: (
            float(item.get("min_distance_to_active_site") or 0.0),
            str(item.get("code")),
        ),
    )


def _expected_cofactor_families(fingerprint: dict[str, Any]) -> set[str]:
    families: set[str] = set()
    for cofactor in fingerprint.get("cofactors", []):
        if not isinstance(cofactor, str):
            continue
        family = _cofactor_family(cofactor)
        if family:
            families.add(family)
    return families


def _ligand_code_family(code: str) -> str:
    normalized = code.strip().upper()
    if normalized in METAL_ION_CODES:
        return "metal_ion"
    return COFACTOR_LIGAND_MAP.get(normalized, "")


def _cofactor_family(cofactor: str) -> str:
    normalized = cofactor.lower().replace("_", " ").replace("-", " ").strip()
    if "h2o2" in normalized or " or o2 " in f" {normalized} " or normalized == "o2":
        return ""
    if any(
        metal in normalized for metal in ["zn2+", "mg2+", "mn2+", "fe2+", "fe3+", "metal"]
    ):
        return "metal_ion"
    if "heme" in normalized:
        return "heme"
    if "pyridoxal phosphate" in normalized:
        return "plp"
    if "cobalamin" in normalized or "vitamin b12" in normalized:
        return "cobalamin"
    if normalized in {"fad", "fmn"}:
        return "flavin"
    if normalized in {"nadph", "nadp", "nad", "nadh"}:
        return "nad"
    if "sam" in normalized or "adenosylmethionine" in normalized:
        return "sam"
    if "4fe 4s" in normalized:
        return "fe_s_cluster"
    return ""


def _cofactor_coverage_status(
    expected: set[str],
    local_matches: set[str],
    structure_matches: set[str],
) -> str:
    if not expected:
        return "not_required"
    if expected <= local_matches:
        return "all_expected_local"
    if local_matches:
        return "partial_expected_local"
    if structure_matches:
        return "expected_structure_only"
    return "expected_absent_from_structure"


def _normalize_penalty_grid(values: list[float]) -> list[float]:
    penalties = []
    for value in values:
        penalty = round(float(value), 4)
        if penalty < 0:
            raise ValueError("cofactor policy penalties must be non-negative")
        penalties.append(penalty)
    return sorted(set(penalties))


def _cofactor_policy_penalty(
    coverage_status: str,
    absent_penalty: float,
    structure_only_penalty: float,
) -> float:
    if coverage_status == "expected_absent_from_structure":
        return absent_penalty
    if coverage_status == "expected_structure_only":
        return structure_only_penalty
    return 0.0


def _cofactor_policy_detail_rows(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float,
) -> list[dict[str, Any]]:
    labels_by_entry = {label.entry_id: label for label in labels}
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    rows: list[dict[str, Any]] = []
    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label:
            continue
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_id = top1.get("fingerprint_id")
        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        top1_base_score = round(
            float(top1.get("base_score", top1.get("score", 0.0)) or 0.0),
            4,
        )
        top3_ids = [item.get("fingerprint_id") for item in top[:3]]
        abstained = top1_score < abstain_threshold
        target_hit = None
        target_rank = None
        if label.fingerprint_id:
            for index, fingerprint_hit in enumerate(top, start=1):
                if fingerprint_hit.get("fingerprint_id") == label.fingerprint_id:
                    target_hit = fingerprint_hit
                    target_rank = index
                    break
        target_fingerprint = fingerprints_by_id.get(str(label.fingerprint_id), {})
        target_coverage = (
            _cofactor_coverage_row_parts(result, target_fingerprint)
            if label.fingerprint_id
            else {}
        )
        top1_coverage_status = top1.get("cofactor_policy_coverage_status")
        if top1_id and not top1_coverage_status:
            top1_coverage_status = _cofactor_coverage_row_parts(
                result,
                fingerprints_by_id.get(str(top1_id), {}),
            )["coverage_status"]
        target_coverage_status = target_coverage.get("coverage_status")
        top1_correct = bool(label.fingerprint_id and top1_id == label.fingerprint_id)
        top3_correct = bool(label.fingerprint_id and label.fingerprint_id in top3_ids)
        target_score = (
            round(float(target_hit.get("score", 0.0) or 0.0), 4)
            if target_hit is not None
            else None
        )
        target_base_score = (
            round(
                float(target_hit.get("base_score", target_hit.get("score", 0.0)) or 0.0),
                4,
            )
            if target_hit is not None
            else None
        )
        target_policy_penalty = (
            round(float(target_hit.get("cofactor_policy_penalty", 0.0) or 0.0), 4)
            if target_hit is not None
            else None
        )
        rows.append(
            {
                "entry_id": str(entry_id),
                "label_type": label.label_type,
                "target_fingerprint_id": label.fingerprint_id,
                "confidence": label.confidence,
                "top1_fingerprint_id": top1_id,
                "top1_base_score": top1_base_score,
                "top1_adjusted_score": top1_score,
                "top1_policy_penalty": round(
                    float(top1.get("cofactor_policy_penalty", 0.0) or 0.0),
                    4,
                ),
                "top1_cofactor_coverage_status": top1_coverage_status,
                "target_rank": target_rank,
                "target_base_score": target_base_score,
                "target_adjusted_score": target_score,
                "target_policy_penalty": target_policy_penalty,
                "target_cofactor_coverage_status": target_coverage_status,
                "target_expected_cofactor_families": target_coverage.get(
                    "expected_cofactor_families",
                    [],
                ),
                "target_missing_expected_families": target_coverage.get(
                    "missing_expected_families",
                    [],
                ),
                "target_nearest_expected_ligand_distance_angstrom": target_coverage.get(
                    "nearest_expected_ligand_distance_angstrom"
                ),
                "target_evidence_limited": (
                    target_coverage_status in COFACTOR_EVIDENCE_LIMITED_STATUSES
                ),
                "abstain_threshold": abstain_threshold,
                "abstained": abstained,
                "top1_correct": top1_correct,
                "top3_correct": top3_correct,
                "retained_positive": top1_correct and not abstained,
                "status": result.get("status"),
                "resolved_residue_count": result.get("resolved_residue_count", 0),
                "evaluable": _is_geometry_evaluable(result),
                "label_rationale": label.rationale,
            }
        )
    return sorted(rows, key=lambda row: _entry_id_sort_key(row["entry_id"]))


def _retained_positive_ids(rows: list[dict[str, Any]]) -> set[str]:
    return {
        row["entry_id"]
        for row in rows
        if row["label_type"] == "seed_fingerprint" and row["retained_positive"]
    }


def _evidence_limited_retained_positive_ids(rows: list[dict[str, Any]]) -> set[str]:
    return {
        row["entry_id"]
        for row in rows
        if row["label_type"] == "seed_fingerprint"
        and row["target_evidence_limited"]
        and row["retained_positive"]
    }


def _evidence_limited_abstained_positive_ids(rows: list[dict[str, Any]]) -> set[str]:
    return {
        row["entry_id"]
        for row in rows
        if row["label_type"] == "seed_fingerprint"
        and row["target_evidence_limited"]
        and row["abstained"]
    }


def _find_policy(
    policies: list[dict[str, Any]],
    absent_penalty: float,
    structure_only_penalty: float,
) -> dict[str, Any] | None:
    for policy in policies:
        if _same_float(policy["absent_penalty"], absent_penalty) and _same_float(
            policy["structure_only_penalty"],
            structure_only_penalty,
        ):
            return policy
    return None


def _cofactor_policy_limiting_rows(
    policy_detail_rows: dict[tuple[float, float], list[dict[str, Any]]],
    base_rows_by_entry: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (absent_penalty, structure_only_penalty), detail_rows in policy_detail_rows.items():
        for row in detail_rows:
            base_row = base_rows_by_entry.get(row["entry_id"], {})
            changed_top1 = row["top1_fingerprint_id"] != base_row.get("top1_fingerprint_id")
            changed_abstention = row["abstained"] != base_row.get("abstained")
            lost_retained_positive = bool(base_row.get("retained_positive")) and not bool(
                row["retained_positive"]
            )
            if not (
                row["target_evidence_limited"]
                or changed_top1
                or changed_abstention
                or lost_retained_positive
            ):
                continue
            rows.append(
                {
                    "absent_penalty": absent_penalty,
                    "structure_only_penalty": structure_only_penalty,
                    "entry_id": row["entry_id"],
                    "label_type": row["label_type"],
                    "target_fingerprint_id": row["target_fingerprint_id"],
                    "target_cofactor_coverage_status": row[
                        "target_cofactor_coverage_status"
                    ],
                    "target_expected_cofactor_families": row[
                        "target_expected_cofactor_families"
                    ],
                    "top1_fingerprint_id": row["top1_fingerprint_id"],
                    "top1_base_score": row["top1_base_score"],
                    "top1_adjusted_score": row["top1_adjusted_score"],
                    "target_base_score": row["target_base_score"],
                    "target_adjusted_score": row["target_adjusted_score"],
                    "target_policy_penalty": row["target_policy_penalty"],
                    "abstained": row["abstained"],
                    "retained_positive": row["retained_positive"],
                    "changed_top1": changed_top1,
                    "changed_abstention": changed_abstention,
                    "lost_retained_positive": lost_retained_positive,
                }
            )
    return sorted(
        rows,
        key=lambda row: (
            _entry_id_sort_key(row["entry_id"]),
            row["absent_penalty"],
            row["structure_only_penalty"],
        ),
    )


def _cofactor_policy_sensitivity_rows(
    base_rows: list[dict[str, Any]],
    abstain_threshold: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in base_rows:
        if not row["target_evidence_limited"]:
            continue
        target_score = row["target_base_score"]
        margin = (
            round(float(target_score) - abstain_threshold, 4)
            if target_score is not None
            else None
        )
        if row["target_cofactor_coverage_status"] == "expected_absent_from_structure":
            affected_penalty = "absent_penalty"
        elif row["target_cofactor_coverage_status"] == "expected_structure_only":
            affected_penalty = "structure_only_penalty"
        else:
            affected_penalty = None
        rows.append(
            {
                "entry_id": row["entry_id"],
                "target_fingerprint_id": row["target_fingerprint_id"],
                "target_cofactor_coverage_status": row["target_cofactor_coverage_status"],
                "target_expected_cofactor_families": row[
                    "target_expected_cofactor_families"
                ],
                "target_base_score": target_score,
                "top1_fingerprint_id": row["top1_fingerprint_id"],
                "top1_correct": row["top1_correct"],
                "retained_positive": row["retained_positive"],
                "abstained": row["abstained"],
                "affected_penalty": affected_penalty,
                "score_margin_to_abstain_threshold": margin,
                "penalty_must_exceed_margin_to_abstain": (
                    margin if margin is not None and margin > 0 else None
                ),
                "already_below_threshold": bool(margin is not None and margin < 0),
                "nearest_expected_ligand_distance_angstrom": row[
                    "target_nearest_expected_ligand_distance_angstrom"
                ],
            }
        )
    return sorted(rows, key=lambda row: _entry_id_sort_key(row["entry_id"]))


def _seed_family_in_scope_row(
    fingerprint_id: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    evaluable_rows = [row for row in rows if row["evaluable"]]
    retained_rows = [row for row in evaluable_rows if not row["abstained"]]
    top1_correct_rows = [row for row in evaluable_rows if row["top1_correct"]]
    top3_correct_rows = [row for row in evaluable_rows if row["top3_correct"]]
    retained_top3_correct_rows = [
        row for row in evaluable_rows if row["top3_correct"] and not row["abstained"]
    ]
    evidence_limited_rows = [
        row
        for row in rows
        if row["cofactor_coverage_status"] in COFACTOR_EVIDENCE_LIMITED_STATUSES
    ]
    scores = [row["top1_score"] for row in evaluable_rows]
    return {
        "fingerprint_id": fingerprint_id,
        "labeled_count": len(rows),
        "evaluable_count": len(evaluable_rows),
        "top1_correct_count": len(top1_correct_rows),
        "top3_correct_count": len(top3_correct_rows),
        "retained_count": len(retained_rows),
        "retained_top3_correct_count": len(retained_top3_correct_rows),
        "abstained_count": len(evaluable_rows) - len(retained_rows),
        "top1_accuracy_evaluable": _ratio(len(top1_correct_rows), len(evaluable_rows)),
        "top3_accuracy_evaluable": _ratio(len(top3_correct_rows), len(evaluable_rows)),
        "top3_retained_accuracy_evaluable": _ratio(
            len(retained_top3_correct_rows),
            len(evaluable_rows),
        ),
        "retention_rate_evaluable": _ratio(len(retained_rows), len(evaluable_rows)),
        "min_top1_score": min(scores) if scores else None,
        "mean_top1_score": round(sum(scores) / len(scores), 4) if scores else None,
        "max_top1_score": max(scores) if scores else None,
        "cofactor_coverage_status_counts": dict(
            sorted(Counter(row["cofactor_coverage_status"] for row in rows).items())
        ),
        "evidence_limited_count": len(evidence_limited_rows),
        "evidence_limited_entry_ids": sorted(
            (row["entry_id"] for row in evidence_limited_rows),
            key=_entry_id_sort_key,
        ),
        "abstained_entry_ids": sorted(
            (row["entry_id"] for row in evaluable_rows if row["abstained"]),
            key=_entry_id_sort_key,
        ),
        "entry_ids": sorted((row["entry_id"] for row in rows), key=_entry_id_sort_key),
    }


def _seed_family_out_scope_row(
    fingerprint_id: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    evaluable_rows = [row for row in rows if row["evaluable"]]
    false_non_abstention_rows = [
        row for row in evaluable_rows if not row["abstained"]
    ]
    scores = [row["top1_score"] for row in evaluable_rows]
    return {
        "fingerprint_id": fingerprint_id,
        "count": len(rows),
        "evaluable_count": len(evaluable_rows),
        "abstained_count": len(evaluable_rows) - len(false_non_abstention_rows),
        "false_non_abstention_count": len(false_non_abstention_rows),
        "abstention_rate_evaluable": _ratio(
            len(evaluable_rows) - len(false_non_abstention_rows),
            len(evaluable_rows),
        ),
        "min_top1_score": min(scores) if scores else None,
        "mean_top1_score": round(sum(scores) / len(scores), 4) if scores else None,
        "max_top1_score": max(scores) if scores else None,
        "cofactor_evidence_counts": dict(
            sorted(
                Counter(
                    str(row.get("cofactor_evidence_level") or "unknown")
                    for row in rows
                ).items()
            )
        ),
        "false_non_abstention_entry_ids": sorted(
            (row["entry_id"] for row in false_non_abstention_rows),
            key=_entry_id_sort_key,
        ),
        "entry_ids": sorted((row["entry_id"] for row in rows), key=_entry_id_sort_key),
    }


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = entry_id.partition(":")
    try:
        numeric = int(suffix)
    except ValueError:
        numeric = 0
    return (prefix, numeric, entry_id)


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
                "entry_name": entry.get("entry_name"),
                "mechanism_text_count": int(entry.get("mechanism_text_count", 0) or 0),
                "mechanism_text_snippets": entry.get("mechanism_text_snippets", [])
                if isinstance(entry.get("mechanism_text_snippets"), list)
                else [],
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
            "candidate_group_count": len(group_label_expansion_candidates(rows)),
        },
        "rows": sorted(rows, key=lambda row: (-row["readiness_score"], row["entry_id"])),
        "groups": group_label_expansion_candidates(rows),
    }


def group_label_expansion_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
        ready_rows = [row for row in group_rows if int(row.get("readiness_score", 0) or 0) >= 4]
        blockers = Counter(
            blocker
            for row in group_rows
            for blocker in row.get("readiness_blockers", [])
            if isinstance(blocker, str)
        )
        result.append(
            {
                "top1_fingerprint_id": fingerprint_id,
                "cofactor_evidence_level": evidence_level,
                "count": len(group_rows),
                "ready_for_label_review_count": len(ready_rows),
                "min_top1_score": round(min(scores), 4) if scores else None,
                "mean_top1_score": round(sum(scores) / len(scores), 4) if scores else None,
                "max_top1_score": round(max(scores), 4) if scores else None,
                "readiness_blocker_counts": dict(sorted(blockers.items())),
                "entry_ids": sorted(str(row.get("entry_id")) for row in group_rows),
                "ready_entry_ids": sorted(str(row.get("entry_id")) for row in ready_rows),
                "ready_entries": [
                    {
                        "entry_id": str(row.get("entry_id")),
                        "entry_name": row.get("entry_name"),
                        "top1_score": row.get("top1_score"),
                        "mechanism_text_snippets": row.get("mechanism_text_snippets", []),
                    }
                    for row in sorted(
                        ready_rows,
                        key=lambda item: (
                            str(item.get("entry_id")),
                            str(item.get("entry_name") or ""),
                        ),
                    )
                ],
            }
        )
    return sorted(
        result,
        key=lambda row: (
            -int(row["ready_for_label_review_count"]),
            -int(row["count"]),
            str(row["top1_fingerprint_id"]),
            str(row["cofactor_evidence_level"]),
        ),
    )


def build_label_factory_audit(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
    hard_negative_controls: dict[str, Any] | None = None,
    adversarial_negatives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    ontology = load_mechanism_ontology()
    negative_control_index = _negative_control_index(
        hard_negative_controls=hard_negative_controls,
        adversarial_negatives=adversarial_negatives,
    )
    rows = [
        _label_factory_row(
            label=label,
            result=result,
            fingerprints_by_id=fingerprints_by_id,
            ontology=ontology,
            abstain_threshold=abstain_threshold,
            negative_control_evidence=negative_control_index.get(label.entry_id, []),
        )
        for result in retrieval.get("results", [])
        for label in [labels_by_entry.get(result.get("entry_id"))]
        if label
    ]
    action_counts = Counter(row["recommended_action"] for row in rows)
    target_tier_counts = Counter(row["proposed_tier"] for row in rows)
    tier_transition_counts = Counter(
        f"{row['current_tier']}->{row['proposed_tier']}" for row in rows
    )
    return {
        "metadata": {
            "method": "label_factory_promotion_demotion_audit",
            "label_count": len(labels),
            "evaluated_label_count": len(rows),
            "abstain_threshold": abstain_threshold,
            "promotion_rule": (
                "bronze labels promote to silver when retrieval agrees with the "
                "label, the score clears the abstention threshold, and no "
                "evidence-limiting cofactor or counterevidence conflict is present"
            ),
            "demotion_rule": (
                "silver/gold labels demote to bronze, or bronze labels stay "
                "review-only, when retrieval counterevidence, abstention, "
                "top-family mismatch, or out-of-scope false non-abstention is present"
            ),
            "action_counts": dict(sorted(action_counts.items())),
            "hard_negative_evidence_entry_count": sum(
                1 for row in rows if row["hard_negative_evidence"]
            ),
            "target_tier_counts": dict(sorted(target_tier_counts.items())),
            "tier_transition_counts": dict(sorted(tier_transition_counts.items())),
            "promote_to_silver_count": int(action_counts.get("promote_to_silver", 0)),
            "demote_to_bronze_count": int(action_counts.get("demote_to_bronze", 0)),
            "abstention_or_review_count": sum(
                int(action_counts.get(action, 0))
                for action in {
                    "abstain_pending_evidence",
                    "review_conflicting_out_of_scope",
                    "hold_bronze_boundary_review",
                    "hold_bronze_need_review",
                }
            ),
        },
        "rows": sorted(
            rows,
            key=lambda row: (
                row["review_priority_rank"],
                _entry_id_sort_key(row["entry_id"]),
            ),
        ),
    }


def _label_factory_row(
    label: MechanismLabel,
    result: dict[str, Any],
    fingerprints_by_id: dict[str, dict[str, Any]],
    ontology: dict[str, Any],
    abstain_threshold: float,
    negative_control_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    top = result.get("top_fingerprints", [])
    top1 = top[0] if top else {}
    top2 = top[1] if len(top) > 1 else {}
    top1_id = top1.get("fingerprint_id")
    top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
    top2_score = round(float(top2.get("score", 0.0) or 0.0), 4) if top2 else None
    top2_gap = round(top1_score - top2_score, 4) if top2_score is not None else None
    target_hit = _target_fingerprint_hit(top, label.fingerprint_id)
    target_rank = target_hit[0]
    target = target_hit[1]
    target_score = (
        round(float(target.get("score", 0.0) or 0.0), 4) if target is not None else None
    )
    abstained = top1_score < abstain_threshold
    target_coverage = (
        _cofactor_coverage_row_parts(
            result,
            fingerprints_by_id.get(label.fingerprint_id, {}),
        )
        if label.fingerprint_id
        else {}
    )
    target_coverage_status = target_coverage.get("coverage_status")
    conflicts = _label_evidence_conflicts(
        label=label,
        top1=top1,
        top1_score=top1_score,
        target=target,
        target_rank=target_rank,
        target_coverage_status=target_coverage_status,
        abstained=abstained,
        abstain_threshold=abstain_threshold,
    )
    if negative_control_evidence and label.label_type == "out_of_scope":
        conflicts.append("adversarial_negative_evidence")
        conflicts = sorted(set(conflicts))
    evidence_score = _label_factory_evidence_score(
        label=label,
        top1_score=top1_score,
        target_score=target_score,
        top1_matches_label=bool(label.fingerprint_id and top1_id == label.fingerprint_id),
        abstained=abstained,
        conflicts=conflicts,
    )
    recommended_action, proposed_tier = _label_factory_action(
        label=label,
        evidence_score=evidence_score,
        conflicts=conflicts,
        top1_score=top1_score,
        abstain_threshold=abstain_threshold,
    )
    return {
        "entry_id": label.entry_id,
        "entry_name": result.get("entry_name"),
        "label_type": label.label_type,
        "target_fingerprint_id": label.fingerprint_id,
        "target_ontology_family": fingerprint_family(label.fingerprint_id, ontology),
        "top1_fingerprint_id": top1_id,
        "top1_ontology_family": fingerprint_family(str(top1_id), ontology),
        "top2_fingerprint_id": top2.get("fingerprint_id") if top2 else None,
        "top2_ontology_family": fingerprint_family(str(top2.get("fingerprint_id")), ontology)
        if top2
        else None,
        "top1_score": top1_score,
        "top2_score": top2_score,
        "top2_gap": top2_gap,
        "target_rank": target_rank,
        "target_score": target_score,
        "abstain_threshold": abstain_threshold,
        "abstained": abstained,
        "current_tier": label.tier,
        "proposed_tier": proposed_tier,
        "review_status": label.review_status,
        "confidence": label.confidence,
        "registry_evidence_score": label.evidence_score,
        "factory_evidence_score": evidence_score,
        "recommended_action": recommended_action,
        "evidence_conflicts": conflicts,
        "cofactor_coverage_status": target_coverage_status,
        "expected_cofactor_families": target_coverage.get("expected_cofactor_families", []),
        "counterevidence_reasons": _counterevidence_reasons_from_row(
            {"component_scores": _fingerprint_component_scores(top1)}
        ),
        "hard_negative_evidence": negative_control_evidence,
        "evaluable": _is_geometry_evaluable(result),
        "review_priority_rank": _label_factory_priority(
            recommended_action=recommended_action,
            conflicts=conflicts,
            top1_score=top1_score,
            abstain_threshold=abstain_threshold,
        ),
        "context": _retrieval_result_context(result),
        "label_rationale": label.rationale,
    }


def build_active_learning_review_queue(
    geometry: dict[str, Any],
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    label_factory_audit: dict[str, Any] | None = None,
    abstain_threshold: float = 0.7,
    max_rows: int = 100,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    label_counts = Counter(label.fingerprint_id for label in labels if label.fingerprint_id)
    retrieval_by_entry = {result.get("entry_id"): result for result in retrieval.get("results", [])}
    geometry_by_entry = {entry.get("entry_id"): entry for entry in geometry.get("entries", [])}
    audit_rows_by_entry = {
        row.get("entry_id"): row for row in (label_factory_audit or {}).get("rows", [])
    }
    ontology = load_mechanism_ontology()

    queue_rows: list[dict[str, Any]] = []
    for entry_id in sorted(
        set(retrieval_by_entry) | set(geometry_by_entry),
        key=lambda value: _entry_id_sort_key(str(value)),
    ):
        if not isinstance(entry_id, str):
            continue
        result = retrieval_by_entry.get(entry_id, {})
        entry = geometry_by_entry.get(entry_id, {})
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top2 = top[1] if len(top) > 1 else {}
        label = labels_by_entry.get(entry_id)
        audit_row = audit_rows_by_entry.get(entry_id, {})
        if label and audit_row.get("recommended_action") in {
            "promote_to_silver",
            "hold_current_tier",
        }:
            continue
        if label and not audit_row:
            continue

        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        top2_score = round(float(top2.get("score", 0.0) or 0.0), 4) if top2 else 0.0
        top1_id = top1.get("fingerprint_id")
        family = fingerprint_family(str(top1_id), ontology)
        scores = _active_learning_scores(
            entry=entry,
            result=result,
            label=label,
            audit_row=audit_row,
            label_counts=label_counts,
            top1_score=top1_score,
            top2_score=top2_score,
            abstain_threshold=abstain_threshold,
            ontology=ontology,
        )
        queue_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": result.get("entry_name") or entry.get("entry_name"),
                "label_state": "labeled" if label else "unlabeled",
                "current_label_type": label.label_type if label else None,
                "current_tier": label.tier if label else None,
                "recommended_action": audit_row.get("recommended_action")
                if audit_row
                else "expert_label_decision_needed",
                "top1_fingerprint_id": top1_id,
                "top1_ontology_family": family,
                "top1_score": top1_score,
                "top2_fingerprint_id": top2.get("fingerprint_id") if top2 else None,
                "top2_score": top2_score if top2 else None,
                "abstain_threshold": abstain_threshold,
                "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                "counterevidence_reasons": _counterevidence_reasons_from_row(
                    {"component_scores": _fingerprint_component_scores(top1)}
                ),
                "review_scores": scores,
                "review_score": round(sum(scores.values()), 4),
                "mechanism_text_snippets": result.get("mechanism_text_snippets")
                or entry.get("mechanism_text_snippets", []),
                "readiness_blockers": _review_readiness_blockers(entry, top1_score),
            }
        )

    ranked_rows = sorted(
        queue_rows,
        key=lambda row: (-row["review_score"], _entry_id_sort_key(row["entry_id"])),
    )[:max_rows]
    for index, row in enumerate(ranked_rows, start=1):
        row["rank"] = index
    score_totals = Counter()
    for row in ranked_rows:
        for key, value in row["review_scores"].items():
            score_totals[key] += round(float(value), 4)
    return {
        "metadata": {
            "method": "active_learning_label_review_queue",
            "candidate_count": len(queue_rows),
            "queued_count": len(ranked_rows),
            "max_rows": max_rows,
            "abstain_threshold": abstain_threshold,
            "ranking_terms": [
                "uncertainty",
                "impact",
                "novelty",
                "hard_negative_value",
                "evidence_conflict",
                "family_boundary_value",
            ],
            "score_totals": dict(sorted((key, round(value, 4)) for key, value in score_totals.items())),
            "unlabeled_count": sum(1 for row in ranked_rows if row["label_state"] == "unlabeled"),
            "labeled_review_count": sum(1 for row in ranked_rows if row["label_state"] == "labeled"),
        },
        "rows": ranked_rows,
    }


def build_adversarial_negative_controls(
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    abstain_threshold: float = 0.7,
    max_rows: int = 100,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    ontology = load_mechanism_ontology()
    rows: list[dict[str, Any]] = []
    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        label = labels_by_entry.get(entry_id)
        if not label or label.label_type != "out_of_scope":
            continue
        top = result.get("top_fingerprints", [])
        if not top:
            continue
        top1 = top[0]
        top2 = top[1] if len(top) > 1 else {}
        top1_score = round(float(top1.get("score", 0.0) or 0.0), 4)
        top2_score = round(float(top2.get("score", 0.0) or 0.0), 4) if top2 else 0.0
        top1_family = fingerprint_family(str(top1.get("fingerprint_id")), ontology)
        top2_family = fingerprint_family(str(top2.get("fingerprint_id")), ontology) if top2 else None
        counterevidence = _counterevidence_reasons_from_row(
            {"component_scores": _fingerprint_component_scores(top1)}
        )
        control_axes = _adversarial_negative_axes(
            top1=top1,
            top1_score=top1_score,
            top2_score=top2_score,
            top1_family=top1_family,
            top2_family=top2_family,
            counterevidence=counterevidence,
            abstain_threshold=abstain_threshold,
        )
        if not control_axes:
            continue
        adversarial_score = _adversarial_negative_score(
            top1_score=top1_score,
            top2_score=top2_score,
            control_axes=control_axes,
            abstain_threshold=abstain_threshold,
        )
        rows.append(
            {
                "entry_id": label.entry_id,
                "entry_name": result.get("entry_name"),
                "top1_fingerprint_id": top1.get("fingerprint_id"),
                "top1_ontology_family": top1_family,
                "top1_score": top1_score,
                "top2_fingerprint_id": top2.get("fingerprint_id") if top2 else None,
                "top2_ontology_family": top2_family,
                "top2_score": top2_score if top2 else None,
                "abstain_threshold": abstain_threshold,
                "score_gap_to_abstain_threshold": round(abstain_threshold - top1_score, 4),
                "cofactor_evidence_level": top1.get("cofactor_evidence_level"),
                "control_axes": control_axes,
                "adversarial_score": adversarial_score,
                "counterevidence_reasons": counterevidence,
                "component_scores": _fingerprint_component_scores(top1),
                "context": _retrieval_result_context(result),
                "label_rationale": label.rationale,
            }
        )
    ranked_rows = sorted(
        rows,
        key=lambda row: (-row["adversarial_score"], _entry_id_sort_key(row["entry_id"])),
    )[:max_rows]
    for index, row in enumerate(ranked_rows, start=1):
        row["rank"] = index
    axis_counts = Counter(axis for row in ranked_rows for axis in row["control_axes"])
    return {
        "metadata": {
            "method": "adversarial_negative_control_mining",
            "candidate_count": len(rows),
            "control_count": len(ranked_rows),
            "max_rows": max_rows,
            "abstain_threshold": abstain_threshold,
            "axis_counts": dict(sorted(axis_counts.items())),
            "selection_rule": (
                "rank out-of-scope entries that stress ontology boundaries, "
                "cofactor mimics, counterevidence, close top1/top2 families, "
                "and abstention-threshold proximity"
            ),
        },
        "rows": ranked_rows,
    }


def build_expert_review_export(
    review_queue: dict[str, Any],
    labels: list[MechanismLabel],
    max_rows: int = 25,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    queue_rows = review_queue.get("rows", [])
    rows = list(queue_rows[:max_rows])
    selected_entry_ids = {row.get("entry_id") for row in rows if isinstance(row, dict)}
    rows.extend(
        row
        for row in queue_rows
        if isinstance(row, dict)
        and row.get("entry_id") not in selected_entry_ids
        and row.get("entry_id") not in labels_by_entry
    )
    return {
        "metadata": {
            "method": "expert_review_export",
            "exported_count": len(rows),
            "max_ranked_rows": max_rows,
            "unlabeled_inclusion_rule": "append all unlabeled queue rows even when ranked below the export cutoff",
            "decision_schema": {
                "action": [
                    "accept_label",
                    "mark_needs_more_evidence",
                    "reject_label",
                    "no_decision",
                ],
                "tier": ["bronze", "silver", "gold"],
                "label_type": ["seed_fingerprint", "out_of_scope"],
                "review_status": [
                    "automation_curated",
                    "needs_expert_review",
                    "expert_reviewed",
                ],
            },
            "provenance_rule": (
                "imports append review provenance and preserve existing evidence.sources"
            ),
        },
        "review_items": [
            {
                "rank": row.get("rank"),
                "entry_id": row.get("entry_id"),
                "entry_name": row.get("entry_name"),
                "current_label": labels_by_entry[row.get("entry_id")].to_dict()
                if row.get("entry_id") in labels_by_entry
                else None,
                "queue_context": row,
                "decision": {
                    "action": "no_decision",
                    "label_type": row.get("current_label_type"),
                    "fingerprint_id": row.get("top1_fingerprint_id"),
                    "tier": "silver",
                    "confidence": "medium",
                    "reviewer": None,
                    "rationale": None,
                    "evidence_score": None,
                    "review_status": "expert_reviewed",
                },
            }
            for row in rows
        ],
    }


def build_provisional_review_decision_batch(
    review_artifact: dict[str, Any],
    *,
    batch_id: str = "provisional_batch",
    reviewer: str = "automation_label_factory",
    max_boundary_controls: int = 5,
) -> dict[str, Any]:
    batch = deepcopy(review_artifact)
    decision_counts: Counter = Counter()
    selected_boundary_controls = 0
    for item in batch.get("review_items", []):
        if not isinstance(item, dict):
            continue
        queue_context = item.get("queue_context", {})
        if not isinstance(queue_context, dict):
            queue_context = {}
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            decision = {}
            item["decision"] = decision
        if item.get("current_label") is None:
            item["decision"] = _provisional_unlabeled_decision(
                item,
                queue_context,
                reviewer=reviewer,
            )
        elif selected_boundary_controls < max_boundary_controls:
            item["decision"] = _provisional_boundary_control_decision(
                item,
                queue_context,
                reviewer=reviewer,
            )
            selected_boundary_controls += 1
        decision_counts[str(item["decision"].get("action", "no_decision"))] += 1
    metadata = dict(batch.get("metadata", {}))
    metadata.update(
        {
            "method": "provisional_label_review_decision_batch",
            "source_method": review_artifact.get("metadata", {}).get("method"),
            "batch_id": batch_id,
            "reviewer": reviewer,
            "decision_counts": dict(sorted(decision_counts.items())),
            "boundary_control_decisions": selected_boundary_controls,
            "policy": (
                "Automation-curated batch decisions stay bronze and are imported "
                "as automation_curated or needs_expert_review records, not gold "
                "or expert-reviewed labels."
            ),
        }
    )
    batch["metadata"] = metadata
    return batch


def apply_label_factory_actions(
    labels: list[MechanismLabel],
    label_factory_audit: dict[str, Any],
) -> dict[str, Any]:
    audit_by_entry = {
        row.get("entry_id"): row
        for row in label_factory_audit.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    updated: list[MechanismLabel] = []
    action_counts: Counter = Counter()
    for label in labels:
        row = audit_by_entry.get(label.entry_id)
        if not row:
            updated.append(label)
            continue
        action = row.get("recommended_action")
        action_counts[str(action)] += 1
        record = label.to_dict()
        if action == "promote_to_silver":
            record["tier"] = "silver"
            record["evidence_score"] = max(
                float(record.get("evidence_score", 0.0) or 0.0),
                float(row.get("factory_evidence_score", 0.0) or 0.0),
            )
        elif action == "demote_to_bronze":
            record["tier"] = "bronze"
            record["review_status"] = "needs_expert_review"
        elif action in {
            "abstain_pending_evidence",
            "review_conflicting_out_of_scope",
            "hold_bronze_boundary_review",
            "hold_bronze_need_review",
        }:
            record["review_status"] = "needs_expert_review"
        else:
            updated.append(label)
            continue
        record["evidence"] = _factory_action_evidence(record.get("evidence", {}), row)
        updated.append(MechanismLabel.from_dict(record))
    summary = label_summary(updated)
    return {
        "metadata": {
            "method": "apply_label_factory_actions",
            "input_label_count": len(labels),
            "output_label_count": len(updated),
            "action_counts": dict(sorted(action_counts.items())),
            "output_summary": summary,
        },
        "labels": [label.to_dict() for label in updated],
    }


def check_label_factory_gates(
    labels: list[MechanismLabel],
    label_factory_audit: dict[str, Any],
    applied_label_factory: dict[str, Any] | None,
    active_learning_queue: dict[str, Any],
    adversarial_negatives: dict[str, Any],
    expert_review_export: dict[str, Any],
    family_propagation_guardrails: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ontology = load_mechanism_ontology()
    required_terms = {
        "uncertainty",
        "impact",
        "novelty",
        "hard_negative_value",
        "evidence_conflict",
        "family_boundary_value",
    }
    ranking_terms = set(active_learning_queue.get("metadata", {}).get("ranking_terms", []))
    adversarial_axes = set(adversarial_negatives.get("metadata", {}).get("axis_counts", {}))
    gates = {
        "label_schema_explicit": all(
            label.tier in LABEL_TIERS
            and label.review_status in REVIEW_STATUSES
            and isinstance(label.evidence, dict)
            and bool(label.evidence.get("sources"))
            for label in labels
        ),
        "promotion_demonstrated": int(
            label_factory_audit.get("metadata", {}).get("promote_to_silver_count", 0)
        )
        > 0,
        "demotion_or_abstention_demonstrated": int(
            label_factory_audit.get("metadata", {}).get("abstention_or_review_count", 0)
        )
        > 0
        or int(label_factory_audit.get("metadata", {}).get("demote_to_bronze_count", 0))
        > 0,
        "applied_label_actions_ready": (
            isinstance(applied_label_factory, dict)
            and int(applied_label_factory.get("metadata", {}).get("output_label_count", 0))
            == len(labels)
            and int(
                applied_label_factory.get("metadata", {})
                .get("output_summary", {})
                .get("by_tier", {})
                .get("silver", 0)
            )
            > 0
        ),
        "ontology_loaded": len(ontology.get("families", [])) > 0,
        "active_queue_ranked": int(
            active_learning_queue.get("metadata", {}).get("queued_count", 0)
        )
        > 0
        and required_terms <= ranking_terms,
        "adversarial_negatives_mined": int(
            adversarial_negatives.get("metadata", {}).get("control_count", 0)
        )
        > 0
        and bool(adversarial_axes - {"threshold_boundary", "false_non_abstention"}),
        "expert_review_export_ready": int(
            expert_review_export.get("metadata", {}).get("exported_count", 0)
        )
        > 0,
        "family_propagation_guardrails_ready": (
            isinstance(family_propagation_guardrails, dict)
            and int(family_propagation_guardrails.get("metadata", {}).get("reported_count", 0))
            > 0
            and bool(family_propagation_guardrails.get("metadata", {}).get("source_guardrails"))
        ),
    }
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "label_factory_gate_check",
            "label_count": len(labels),
            "passed_gate_count": sum(1 for passed in gates.values() if passed),
            "gate_count": len(gates),
            "automation_ready_for_next_label_batch": not blockers,
            "bulk_scaling_rule": (
                "new labels may be added in batches only after this gate check "
                "passes and the generated batch artifacts are regenerated"
            ),
        },
        "gates": gates,
        "blockers": blockers,
    }


def check_label_batch_acceptance(
    baseline_labels: list[MechanismLabel],
    review_state_labels: list[MechanismLabel],
    countable_labels: list[MechanismLabel],
    evaluation: dict[str, Any],
    hard_negatives: dict[str, Any],
    in_scope_failures: dict[str, Any],
    label_factory_gate: dict[str, Any],
    baseline_label_count: int | None = None,
) -> dict[str, Any]:
    baseline_count = baseline_label_count if baseline_label_count is not None else len(baseline_labels)
    countable_count = len(countable_labels)
    review_summary = label_summary(review_state_labels)
    countable_summary = label_summary(countable_labels)
    evaluation_meta = evaluation.get("metadata", {})
    hard_meta = hard_negatives.get("metadata", {})
    in_scope_meta = in_scope_failures.get("metadata", {})
    gate_meta = label_factory_gate.get("metadata", {})
    pending_review_count = int(
        review_summary.get("by_review_status", {}).get("needs_expert_review", 0)
    )
    gates = {
        "countable_registry_preserves_baseline": countable_count >= baseline_count,
        "accepted_labels_added": countable_count > baseline_count,
        "no_pending_review_in_countable": not any(
            label.review_status == "needs_expert_review" for label in countable_labels
        ),
        "zero_out_of_scope_false_non_abstentions": int(
            evaluation_meta.get("out_of_scope_false_non_abstentions", 0)
        )
        == 0,
        "zero_hard_negatives": int(hard_meta.get("hard_negative_count", 0)) == 0,
        "zero_near_misses": int(hard_meta.get("near_miss_count", 0)) == 0,
        "zero_actionable_in_scope_failures": int(
            in_scope_meta.get("actionable_failure_count", 0)
        )
        == 0,
        "factory_gate_ready": bool(gate_meta.get("automation_ready_for_next_label_batch")),
    }
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "label_batch_acceptance_check",
            "baseline_label_count": baseline_count,
            "review_state_label_count": len(review_state_labels),
            "countable_label_count": countable_count,
            "accepted_new_label_count": max(0, countable_count - baseline_count),
            "pending_review_count": pending_review_count,
            "out_of_scope_false_non_abstentions": evaluation_meta.get(
                "out_of_scope_false_non_abstentions"
            ),
            "hard_negative_count": hard_meta.get("hard_negative_count"),
            "near_miss_count": hard_meta.get("near_miss_count"),
            "actionable_in_scope_failure_count": in_scope_meta.get(
                "actionable_failure_count"
            ),
            "evidence_limited_abstention_count": in_scope_meta.get(
                "evidence_limited_abstention_count"
            ),
            "factory_gate_ready": gate_meta.get("automation_ready_for_next_label_batch"),
            "accepted_for_counting": not blockers,
            "review_state_rule": (
                "pending-review labels remain in the review-state registry but "
                "are not copied into the countable benchmark registry"
            ),
        },
        "gates": gates,
        "blockers": blockers,
        "summaries": {
            "review_state": review_summary,
            "countable": countable_summary,
        },
    }


def build_family_propagation_guardrails(
    geometry: dict[str, Any],
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    max_rows: int = 200,
) -> dict[str, Any]:
    labels_by_entry = {label.entry_id: label for label in labels}
    ontology = load_mechanism_ontology()
    geometry_by_entry = {entry.get("entry_id"): entry for entry in geometry.get("entries", [])}
    rows: list[dict[str, Any]] = []
    for result in retrieval.get("results", []):
        entry_id = result.get("entry_id")
        if not isinstance(entry_id, str):
            continue
        label = labels_by_entry.get(entry_id)
        entry = geometry_by_entry.get(entry_id, {})
        top = result.get("top_fingerprints", [])
        if not top:
            continue
        top1 = top[0]
        top2 = top[1] if len(top) > 1 else {}
        top1_id = top1.get("fingerprint_id")
        top2_id = top2.get("fingerprint_id")
        target_family = fingerprint_family(label.fingerprint_id, ontology) if label else None
        top1_family = fingerprint_family(str(top1_id), ontology)
        top2_family = fingerprint_family(str(top2_id), ontology) if top2 else None
        blockers = _family_propagation_blockers(
            label=label,
            top1=top1,
            top2=top2,
            target_family=target_family,
            top1_family=top1_family,
            top2_family=top2_family,
        )
        decision = _family_propagation_decision(label, blockers)
        if label and decision == "direct_label_no_propagation_issue":
            continue
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": result.get("entry_name") or entry.get("entry_name"),
                "label_state": "labeled" if label else "unlabeled",
                "current_label_type": label.label_type if label else None,
                "current_tier": label.tier if label else None,
                "target_fingerprint_id": label.fingerprint_id if label else None,
                "target_ontology_family": target_family,
                "top1_fingerprint_id": top1_id,
                "top1_ontology_family": top1_family,
                "top2_fingerprint_id": top2_id,
                "top2_ontology_family": top2_family,
                "top1_score": round(float(top1.get("score", 0.0) or 0.0), 4),
                "top2_score": round(float(top2.get("score", 0.0) or 0.0), 4) if top2 else None,
                "propagation_decision": decision,
                "propagation_blockers": blockers,
                "local_proxy_evidence": {
                    "mechanism_text_count": int(
                        result.get("mechanism_text_count", entry.get("mechanism_text_count", 0)) or 0
                    ),
                    "proximal_cofactor_families": (result.get("ligand_context") or {}).get(
                        "cofactor_families", []
                    )
                    if isinstance(result.get("ligand_context"), dict)
                    else [],
                    "structure_cofactor_families": (result.get("ligand_context") or {}).get(
                        "structure_cofactor_families", []
                    )
                    if isinstance(result.get("ligand_context"), dict)
                    else [],
                    "nearby_residue_count": (result.get("pocket_context") or {}).get(
                        "nearby_residue_count", 0
                    )
                    if isinstance(result.get("pocket_context"), dict)
                    else 0,
                },
                "mechanism_text_snippets": result.get("mechanism_text_snippets")
                or entry.get("mechanism_text_snippets", []),
            }
        )
    ranked_rows = sorted(
        rows,
        key=lambda row: (
            _family_decision_priority(row["propagation_decision"]),
            _entry_id_sort_key(row["entry_id"]),
        ),
    )[:max_rows]
    decision_counts = Counter(row["propagation_decision"] for row in ranked_rows)
    blocker_counts = Counter(
        blocker for row in ranked_rows for blocker in row["propagation_blockers"]
    )
    return {
        "metadata": {
            "method": "family_propagation_guardrail_audit",
            "audited_count": len(rows),
            "reported_count": len(ranked_rows),
            "max_rows": max_rows,
            "ontology_version": ontology.get("version"),
            "decision_counts": dict(sorted(decision_counts.items())),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "source_guardrails": ontology.get("propagation_guardrails", []),
            "local_proxy_rule": (
                "when UniRef, CATH, or InterPro evidence is unavailable, mechanism text, "
                "ligand/cofactor context, and pocket geometry can prioritize review but "
                "cannot promote beyond bronze by themselves"
            ),
        },
        "rows": ranked_rows,
    }


def import_expert_review_decisions(
    labels: list[MechanismLabel],
    review_artifact: dict[str, Any],
) -> list[MechanismLabel]:
    records_by_entry = {label.entry_id: label.to_dict() for label in labels}
    for item in review_artifact.get("review_items", []):
        if not isinstance(item, dict):
            continue
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            continue
        action = decision.get("action")
        if action == "no_decision":
            continue
        entry_id = item.get("entry_id")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValueError("review item entry_id must be a non-empty string")
        existing = records_by_entry.get(entry_id)
        if action == "mark_needs_more_evidence":
            if existing:
                records_by_entry[entry_id] = _apply_review_status(
                    existing,
                    review_status="needs_expert_review",
                    decision=decision,
                )
            else:
                records_by_entry[entry_id] = _review_placeholder_record(
                    entry_id=entry_id,
                    item=item,
                    decision=decision,
                )
            continue
        if action == "reject_label":
            if not existing:
                continue
            records_by_entry[entry_id] = _apply_review_status(
                existing,
                review_status="rejected",
                decision=decision,
            )
            continue
        if action != "accept_label":
            raise ValueError(f"{entry_id}: invalid review action {action}")
        records_by_entry[entry_id] = _accepted_expert_label_record(
            entry_id=entry_id,
            existing=existing,
            item=item,
            decision=decision,
        )
    imported = [
        MechanismLabel.from_dict(record)
        for record in sorted(records_by_entry.values(), key=lambda row: _entry_id_sort_key(row["entry_id"]))
    ]
    _validate_label_fingerprints(imported)
    return imported


def import_countable_review_decisions(
    labels: list[MechanismLabel],
    review_artifact: dict[str, Any],
) -> list[MechanismLabel]:
    countable_review = deepcopy(review_artifact)
    for item in countable_review.get("review_items", []):
        if not isinstance(item, dict):
            continue
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            continue
        if (
            decision.get("action") != "accept_label"
            or decision.get("review_status", "expert_reviewed") not in COUNTABLE_REVIEW_STATUSES
        ):
            item["decision"] = {**decision, "action": "no_decision"}
    return import_expert_review_decisions(labels, countable_review)


def _validate_label_fingerprints(labels: list[MechanismLabel]) -> None:
    fingerprint_ids = {fingerprint.id for fingerprint in load_fingerprints()}
    unknown = sorted(
        label.fingerprint_id
        for label in labels
        if label.fingerprint_id and label.fingerprint_id not in fingerprint_ids
    )
    if unknown:
        raise ValueError(f"unknown fingerprint ids: {', '.join(unknown)}")


def _target_fingerprint_hit(
    top: list[dict[str, Any]],
    fingerprint_id: str | None,
) -> tuple[int | None, dict[str, Any] | None]:
    if not fingerprint_id:
        return None, None
    for index, fingerprint in enumerate(top, start=1):
        if fingerprint.get("fingerprint_id") == fingerprint_id:
            return index, fingerprint
    return None, None


def _negative_control_index(
    hard_negative_controls: dict[str, Any] | None,
    adversarial_negatives: dict[str, Any] | None,
) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for source_name, artifact in [
        ("hard_negative_controls", hard_negative_controls),
        ("adversarial_negatives", adversarial_negatives),
    ]:
        if not isinstance(artifact, dict):
            continue
        for section in ["rows", "near_miss_rows", "closest_below_floor_rows"]:
            rows = artifact.get(section, [])
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                entry_id = row.get("entry_id")
                if not isinstance(entry_id, str):
                    continue
                index.setdefault(entry_id, []).append(
                    {
                        "source": source_name,
                        "section": section,
                        "rank": row.get("rank"),
                        "control_axes": row.get("control_axes", []),
                        "negative_control_type": row.get("negative_control_type"),
                        "top1_fingerprint_id": row.get("top1_fingerprint_id"),
                        "top1_score": row.get("top1_score"),
                    }
                )
    return index


def _label_evidence_conflicts(
    label: MechanismLabel,
    top1: dict[str, Any],
    top1_score: float,
    target: dict[str, Any] | None,
    target_rank: int | None,
    target_coverage_status: str | None,
    abstained: bool,
    abstain_threshold: float,
) -> list[str]:
    conflicts: list[str] = []
    if label.label_type == "seed_fingerprint":
        if target_rank is None:
            conflicts.append("target_absent_from_top_k")
        elif target_rank != 1:
            conflicts.append("target_not_top1")
        if abstained:
            conflicts.append("top1_below_abstention_threshold")
        if target_coverage_status in COFACTOR_EVIDENCE_LIMITED_STATUSES:
            conflicts.append(target_coverage_status)
        target_reasons = _fingerprint_component_scores(target or {}).get(
            "counterevidence_reasons", []
        )
        for reason in target_reasons:
            conflicts.append(f"target_counterevidence:{reason}")
    else:
        if top1_score >= abstain_threshold:
            conflicts.append("out_of_scope_false_non_abstention")
        if top1_score >= max(0.0, abstain_threshold - 0.02):
            conflicts.append("out_of_scope_boundary_near_positive_floor")
        for reason in _fingerprint_component_scores(top1).get("counterevidence_reasons", []):
            conflicts.append(f"top1_counterevidence:{reason}")
    return sorted(set(conflicts))


def _label_factory_evidence_score(
    label: MechanismLabel,
    top1_score: float,
    target_score: float | None,
    top1_matches_label: bool,
    abstained: bool,
    conflicts: list[str],
) -> float:
    base = label.evidence_score
    if label.label_type == "seed_fingerprint":
        retrieval_support = target_score if target_score is not None else 0.0
        agreement_bonus = 0.15 if top1_matches_label else 0.0
        abstention_penalty = 0.2 if abstained else 0.0
    else:
        retrieval_support = max(0.0, 1.0 - top1_score)
        agreement_bonus = 0.1 if not abstained else 0.15
        abstention_penalty = 0.0 if abstained else 0.25
    conflict_penalty = min(0.45, 0.08 * len(conflicts))
    return round(
        max(0.0, min(1.0, 0.35 * base + 0.45 * retrieval_support + agreement_bonus - abstention_penalty - conflict_penalty)),
        4,
    )


def _label_factory_action(
    label: MechanismLabel,
    evidence_score: float,
    conflicts: list[str],
    top1_score: float,
    abstain_threshold: float,
) -> tuple[str, str]:
    has_serious_conflict = any(
        conflict
        in {
            "target_absent_from_top_k",
            "target_not_top1",
            "top1_below_abstention_threshold",
            "expected_absent_from_structure",
            "expected_structure_only",
            "out_of_scope_false_non_abstention",
        }
        for conflict in conflicts
    )
    if has_serious_conflict and label.tier in {"silver", "gold"}:
        return "demote_to_bronze", "bronze"
    if label.label_type == "seed_fingerprint" and has_serious_conflict:
        return "abstain_pending_evidence", "bronze"
    if label.label_type == "out_of_scope" and "out_of_scope_false_non_abstention" in conflicts:
        return "review_conflicting_out_of_scope", "bronze"
    if label.label_type == "out_of_scope" and top1_score >= max(0.0, abstain_threshold - 0.02):
        return "hold_bronze_boundary_review", "bronze"
    if evidence_score >= 0.68 and label.tier == "bronze":
        return "promote_to_silver", "silver"
    if evidence_score < 0.45:
        return "hold_bronze_need_review", "bronze"
    return "hold_current_tier", label.tier


def _label_factory_priority(
    recommended_action: str,
    conflicts: list[str],
    top1_score: float,
    abstain_threshold: float,
) -> int:
    base_priority = {
        "demote_to_bronze": 1,
        "review_conflicting_out_of_scope": 2,
        "abstain_pending_evidence": 3,
        "hold_bronze_boundary_review": 4,
        "hold_bronze_need_review": 5,
        "promote_to_silver": 8,
        "hold_current_tier": 9,
    }.get(recommended_action, 10)
    if abs(top1_score - abstain_threshold) <= 0.02:
        base_priority = max(1, base_priority - 1)
    if conflicts:
        base_priority = max(1, base_priority - 1)
    return base_priority


def _active_learning_scores(
    entry: dict[str, Any],
    result: dict[str, Any],
    label: MechanismLabel | None,
    audit_row: dict[str, Any],
    label_counts: Counter,
    top1_score: float,
    top2_score: float,
    abstain_threshold: float,
    ontology: dict[str, Any],
) -> dict[str, float]:
    top = result.get("top_fingerprints", [])
    top1 = top[0] if top else {}
    top2 = top[1] if len(top) > 1 else {}
    top1_id = top1.get("fingerprint_id")
    top2_id = top2.get("fingerprint_id")
    top_gap = abs(top1_score - top2_score)
    threshold_gap = abs(top1_score - abstain_threshold)
    uncertainty = max(0.0, 0.6 * (1.0 - min(threshold_gap / 0.2, 1.0)) + 0.4 * (1.0 - min(top_gap / 0.2, 1.0)))
    mechanism_text_count = int(
        result.get("mechanism_text_count", entry.get("mechanism_text_count", 0)) or 0
    )
    resolved = int(result.get("resolved_residue_count", entry.get("resolved_residue_count", 0)) or 0)
    impact = min(1.0, 0.35 * min(mechanism_text_count, 3) / 3 + 0.35 * min(resolved, 5) / 5 + 0.3 * top1_score)
    family_count = int(label_counts.get(top1_id, 0) or 0)
    novelty = 1.0 / (1.0 + family_count / 25.0)
    unlabeled_bonus = 0.8 if label is None else 0.0
    counterevidence = _counterevidence_reasons_from_row(
        {"component_scores": _fingerprint_component_scores(top1)}
    )
    hard_negative_value = 0.0
    if not label or (label and label.label_type == "out_of_scope"):
        hard_negative_value = max(0.0, 1.0 - min(abs(top1_score - abstain_threshold) / 0.15, 1.0))
    evidence_conflict = min(
        1.0,
        0.35 * len(audit_row.get("evidence_conflicts", []))
        + 0.2 * len(counterevidence)
        + (0.25 if top1.get("cofactor_evidence_level") == "absent" else 0.0),
    )
    top1_family = fingerprint_family(str(top1_id), ontology)
    top2_family = fingerprint_family(str(top2_id), ontology)
    family_boundary_value = 0.0
    if top1_family and top2_family and top1_family != top2_family:
        family_boundary_value = max(0.0, 1.0 - min(top_gap / 0.2, 1.0))
    if label and label.fingerprint_id and top1_family != fingerprint_family(label.fingerprint_id, ontology):
        family_boundary_value = max(family_boundary_value, 0.8)
    return {
        "uncertainty": round(1.4 * uncertainty, 4),
        "impact": round(1.1 * impact, 4),
        "novelty": round(0.7 * novelty + unlabeled_bonus, 4),
        "hard_negative_value": round(1.2 * hard_negative_value, 4),
        "evidence_conflict": round(1.5 * evidence_conflict, 4),
        "family_boundary_value": round(1.1 * family_boundary_value, 4),
    }


def _adversarial_negative_axes(
    top1: dict[str, Any],
    top1_score: float,
    top2_score: float,
    top1_family: str | None,
    top2_family: str | None,
    counterevidence: list[str],
    abstain_threshold: float,
) -> list[str]:
    axes: list[str] = []
    if abs(top1_score - abstain_threshold) <= 0.03:
        axes.append("threshold_boundary")
    if top1_score >= abstain_threshold:
        axes.append("false_non_abstention")
    if top1_family and top2_family and top1_family != top2_family and abs(top1_score - top2_score) <= 0.05:
        axes.append("ontology_family_boundary")
    if top1.get("cofactor_evidence_level") in {"ligand_supported", "role_inferred"}:
        axes.append("cofactor_mimic")
    if counterevidence:
        axes.append("counterevidence_stress")
    if float(top1.get("mechanistic_coherence_score", 0.0) or 0.0) >= 0.8:
        axes.append("mechanistic_coherence_mimic")
    return sorted(set(axes))


def _adversarial_negative_score(
    top1_score: float,
    top2_score: float,
    control_axes: list[str],
    abstain_threshold: float,
) -> float:
    threshold_pressure = max(0.0, 1.0 - min(abs(top1_score - abstain_threshold) / 0.15, 1.0))
    rank_ambiguity = max(0.0, 1.0 - min(abs(top1_score - top2_score) / 0.2, 1.0))
    axis_weight = min(1.0, len(control_axes) / 4)
    return round(1.2 * threshold_pressure + 0.8 * rank_ambiguity + 1.4 * axis_weight, 4)


def _review_readiness_blockers(entry: dict[str, Any], top1_score: float) -> list[str]:
    blockers: list[str] = []
    if entry.get("status") != "ok":
        blockers.append("geometry_status_not_ok")
    if int(entry.get("resolved_residue_count", 0) or 0) < 3:
        blockers.append("fewer_than_three_resolved_residues")
    if not entry.get("mechanism_text_snippets"):
        blockers.append("missing_mechanism_text")
    if top1_score <= 0:
        blockers.append("missing_retrieval_score")
    return blockers


def _provisional_unlabeled_decision(
    item: dict[str, Any],
    queue_context: dict[str, Any],
    *,
    reviewer: str,
) -> dict[str, Any]:
    entry_id = str(item.get("entry_id", ""))
    entry_name = str(item.get("entry_name", entry_id))
    snippets = queue_context.get("mechanism_text_snippets", [])
    text = " ".join(str(snippet) for snippet in snippets).lower()
    top1 = str(queue_context.get("top1_fingerprint_id") or "")
    top1_score = float(queue_context.get("top1_score", 0.0) or 0.0)
    threshold = float(queue_context.get("abstain_threshold", 0.0) or 0.0)
    cofactor_level = str(queue_context.get("cofactor_evidence_level") or "unknown")
    counterevidence = [
        str(reason)
        for reason in queue_context.get("counterevidence_reasons", [])
        if str(reason)
    ]
    blockers = [
        str(blocker)
        for blocker in queue_context.get("readiness_blockers", [])
        if str(blocker)
    ]

    cobalamin_hint = (
        "cobalamin" in text
        or "co-c5" in text
        or "adenosylcobalamin" in text
        or entry_id == "m_csa:494"
    )
    metal_hydrolysis_hint = (
        top1 == "metal_dependent_hydrolase"
        and ("phosphatase" in text or "phosphodiester" in text or "phosphate" in text)
        and ("hydrolys" in text or "water" in text)
    )
    supported_seed = (
        top1_score >= threshold
        and top1
        and cofactor_level != "absent"
        and not counterevidence
    )
    if cobalamin_hint and (
        top1 != "cobalamin_radical_rearrangement"
        or cofactor_level != "ligand_supported"
    ):
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "cobalamin_radical_rearrangement",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has cobalamin-radical mechanism text, but the "
                "selected structure lacks local cobalamin support; keep this "
                "candidate in expert review before counting it."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if metal_hydrolysis_hint and top1_score < threshold + 0.03:
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "metal_dependent_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has metal-dependent hydrolysis mechanism text, "
                f"but its retrieval score {top1_score:.4f} is too close to the "
                f"{threshold:.4f} abstention floor for automatic counting."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if supported_seed or metal_hydrolysis_hint:
        confidence = "high" if top1_score >= 0.5 and cofactor_level == "ligand_supported" else "medium"
        return {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": top1,
            "tier": "bronze",
            "confidence": confidence,
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} is provisionally assigned to {top1}: retrieval "
                f"score {top1_score:.4f} clears the {threshold:.4f} floor and "
                f"the review context reports {cofactor_level} cofactor evidence."
            ),
            "evidence_score": 0.72 if confidence == "high" else 0.65,
            "review_status": "automation_curated",
        }

    confidence = "low" if blockers else "medium"
    rationale_bits = [
        f"{entry_name} is provisionally outside the current seed fingerprints.",
        f"Top retrieval {top1 or 'none'} scored {top1_score:.4f}, below the {threshold:.4f} floor.",
    ]
    if counterevidence:
        rationale_bits.append(
            "Counterevidence: " + ", ".join(sorted(counterevidence)) + "."
        )
    if blockers:
        rationale_bits.append("Review blockers: " + ", ".join(sorted(blockers)) + ".")
    return {
        "action": "accept_label",
        "label_type": "out_of_scope",
        "fingerprint_id": None,
        "tier": "bronze",
        "confidence": confidence,
        "reviewer": reviewer,
        "rationale": " ".join(rationale_bits),
        "evidence_score": 0.4 if confidence == "low" else 0.65,
        "review_status": "automation_curated",
    }


def _provisional_boundary_control_decision(
    item: dict[str, Any],
    queue_context: dict[str, Any],
    *,
    reviewer: str,
) -> dict[str, Any]:
    entry_name = str(item.get("entry_name", item.get("entry_id", "entry")))
    top1 = str(queue_context.get("top1_fingerprint_id") or "unknown")
    top1_score = float(queue_context.get("top1_score", 0.0) or 0.0)
    threshold = float(queue_context.get("abstain_threshold", 0.0) or 0.0)
    counterevidence = [
        str(reason)
        for reason in queue_context.get("counterevidence_reasons", [])
        if str(reason)
    ]
    evidence_note = (
        " Counterevidence: " + ", ".join(sorted(counterevidence)) + "."
        if counterevidence
        else ""
    )
    return {
        "action": "mark_needs_more_evidence",
        "label_type": queue_context.get("current_label_type", "out_of_scope"),
        "fingerprint_id": top1,
        "tier": "bronze",
        "confidence": "medium",
        "reviewer": reviewer,
        "rationale": (
            f"{entry_name} is a high-ranked boundary control: top retrieval "
            f"{top1} scored {top1_score:.4f} near the {threshold:.4f} "
            f"abstention floor.{evidence_note}"
        ),
        "evidence_score": 0.55,
        "review_status": "needs_expert_review",
    }


def _apply_review_status(
    existing: dict[str, Any],
    review_status: str,
    decision: dict[str, Any],
) -> dict[str, Any]:
    evidence = _expert_review_evidence(existing.get("evidence", {}), decision)
    return {
        **existing,
        "review_status": review_status,
        "evidence": evidence,
    }


def _factory_action_evidence(existing_evidence: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(existing_evidence, dict):
        existing_evidence = {}
    sources = list(existing_evidence.get("sources", []))
    if "label_factory_audit" not in sources:
        sources.append("label_factory_audit")
    actions = list(existing_evidence.get("factory_actions", []))
    actions.append(
        {
            "recommended_action": row.get("recommended_action"),
            "factory_evidence_score": row.get("factory_evidence_score"),
            "top1_fingerprint_id": row.get("top1_fingerprint_id"),
            "top1_score": row.get("top1_score"),
            "target_fingerprint_id": row.get("target_fingerprint_id"),
            "target_score": row.get("target_score"),
            "evidence_conflicts": row.get("evidence_conflicts", []),
        }
    )
    return {
        **existing_evidence,
        "sources": [str(source) for source in sources if str(source)],
        "retrieval_score": row.get("target_score") or row.get("top1_score"),
        "cofactor_evidence_level": row.get("cofactor_coverage_status"),
        "conflicts": row.get("evidence_conflicts", []),
        "factory_actions": actions,
    }


def _accepted_expert_label_record(
    entry_id: str,
    existing: dict[str, Any] | None,
    item: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    label_type = decision.get("label_type")
    if label_type not in {"seed_fingerprint", "out_of_scope"}:
        raise ValueError(f"{entry_id}: accepted review requires valid label_type")
    fingerprint_id = decision.get("fingerprint_id")
    if label_type == "out_of_scope":
        fingerprint_id = None
    rationale = decision.get("rationale") or (existing or {}).get("rationale")
    if not isinstance(rationale, str) or len(rationale) < 20:
        raise ValueError(f"{entry_id}: accepted review requires rationale")
    tier = decision.get("tier", "silver")
    confidence = decision.get("confidence", "medium")
    review_status = decision.get("review_status", "expert_reviewed")
    if review_status not in {"automation_curated", "expert_reviewed"}:
        raise ValueError(
            f"{entry_id}: accepted review requires automation_curated or expert_reviewed status"
        )
    if tier == "gold" and review_status != "expert_reviewed":
        raise ValueError(f"{entry_id}: gold labels require expert_reviewed status")
    evidence_score = decision.get("evidence_score")
    if evidence_score is None:
        evidence_score = 1.0 if tier == "gold" else CONFIDENCE_EVIDENCE_SCORES.get(str(confidence), 0.65)
    return {
        "entry_id": entry_id,
        "fingerprint_id": fingerprint_id,
        "label_type": label_type,
        "tier": tier,
        "review_status": review_status,
        "confidence": confidence,
        "evidence_score": evidence_score,
        "evidence": _expert_review_evidence(
            (existing or {}).get("evidence", {}),
            decision,
            queue_context=item.get("queue_context", {}),
        ),
        "rationale": rationale,
    }


def _review_placeholder_record(
    entry_id: str,
    item: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    label_type = decision.get("label_type")
    if label_type not in {"seed_fingerprint", "out_of_scope"}:
        raise ValueError(f"{entry_id}: review placeholder requires valid label_type")
    fingerprint_id = decision.get("fingerprint_id")
    if label_type == "out_of_scope":
        fingerprint_id = None
    rationale = decision.get("rationale")
    if not isinstance(rationale, str) or len(rationale) < 20:
        raise ValueError(f"{entry_id}: review placeholder requires rationale")
    confidence = decision.get("confidence", "low")
    evidence_score = decision.get("evidence_score")
    if evidence_score is None:
        evidence_score = CONFIDENCE_EVIDENCE_SCORES.get(str(confidence), 0.4)
    return {
        "entry_id": entry_id,
        "fingerprint_id": fingerprint_id,
        "label_type": label_type,
        "tier": "bronze",
        "review_status": "needs_expert_review",
        "confidence": confidence,
        "evidence_score": evidence_score,
        "evidence": _expert_review_evidence(
            {},
            decision,
            queue_context=item.get("queue_context", {}),
        ),
        "rationale": rationale,
    }


def _family_propagation_blockers(
    label: MechanismLabel | None,
    top1: dict[str, Any],
    top2: dict[str, Any],
    target_family: str | None,
    top1_family: str | None,
    top2_family: str | None,
) -> list[str]:
    blockers: list[str] = []
    if label and target_family and top1_family and target_family != top1_family:
        blockers.append("target_family_top1_family_mismatch")
    if top1_family and top2_family and top1_family != top2_family:
        top1_score = float(top1.get("score", 0.0) or 0.0)
        top2_score = float(top2.get("score", 0.0) or 0.0)
        if abs(top1_score - top2_score) <= 0.05:
            blockers.append("close_cross_family_top1_top2")
    if top1.get("cofactor_evidence_level") == "absent":
        blockers.append("top1_cofactor_absent")
    if _fingerprint_component_scores(top1).get("counterevidence_reasons"):
        blockers.append("top1_counterevidence_present")
    if not label:
        blockers.append("unlabeled_candidate_requires_direct_review")
    return sorted(set(blockers))


def _family_propagation_decision(
    label: MechanismLabel | None,
    blockers: list[str],
) -> str:
    if not label:
        if blockers == ["unlabeled_candidate_requires_direct_review"]:
            return "bronze_review_only"
        return "block_propagation_pending_review"
    if blockers:
        return "block_family_propagation"
    return "direct_label_no_propagation_issue"


def _family_decision_priority(decision: str) -> int:
    return {
        "block_propagation_pending_review": 1,
        "bronze_review_only": 2,
        "block_family_propagation": 3,
        "direct_label_no_propagation_issue": 9,
    }.get(decision, 10)


def _expert_review_evidence(
    existing_evidence: dict[str, Any],
    decision: dict[str, Any],
    queue_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(existing_evidence, dict):
        existing_evidence = {}
    sources = list(existing_evidence.get("sources", []))
    source_name = (
        "label_factory_review_import"
        if decision.get("review_status") == "automation_curated"
        or str(decision.get("reviewer", "")).startswith("automation")
        else "expert_review_import"
    )
    if source_name not in sources:
        sources.append(source_name)
    expert_reviews = list(existing_evidence.get("expert_reviews", []))
    expert_reviews.append(
        {
            "reviewer": decision.get("reviewer"),
            "action": decision.get("action"),
            "rationale": decision.get("rationale"),
            "queue_rank": (queue_context or {}).get("rank"),
            "review_status": decision.get("review_status"),
            "source": source_name,
        }
    )
    return {
        **existing_evidence,
        "sources": [str(source) for source in sources if str(source)],
        "expert_reviews": expert_reviews,
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
                "entry_name": entry.get("entry_name"),
                "pdb_id": entry.get("pdb_id"),
                "status": status,
                "mechanism_text_count": int(entry.get("mechanism_text_count", 0) or 0),
                "mechanism_text_snippets": entry.get("mechanism_text_snippets", [])
                if isinstance(entry.get("mechanism_text_snippets"), list)
                else [],
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
