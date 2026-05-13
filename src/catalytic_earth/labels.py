from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .ontology import fingerprint_family, load_mechanism_ontology
from .sources import PROJECT_ROOT
from .structure import (
    COFACTOR_LIGAND_MAP,
    METAL_ION_CODES,
    STANDARD_AMINO_ACIDS,
    atom_position,
    fetch_pdb_cif,
    ligand_context_from_atoms,
    parse_atom_site_loop,
    residue_centroid,
    select_residue_atoms,
    structure_ligand_inventory_from_atoms,
)


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
ATP_PHOSPHORYL_PARENT_FAMILY_ID = "atp_phosphoryl_transfer"
ATP_PHOSPHORYL_TRANSFER_FAMILY_IDS = (
    "epk",
    "askha",
    "atp_grasp",
    "ghkl",
    "dnk",
    "ndk",
    "pfka",
    "pfkb",
    "ghmp",
)
ATP_PHOSPHORYL_TRANSFER_FAMILY_NAMES = {
    "epk": "ePK-fold protein and ePK-like kinases",
    "askha": "ASKHA sugar and acetate kinases",
    "atp_grasp": "ATP-grasp ligases",
    "ghkl": "GHKL/Bergerat ATP-binding kinases",
    "dnk": "Deoxynucleoside kinases",
    "ndk": "Nucleoside diphosphate kinases",
    "pfka": "PfkA-fold phosphofructokinases",
    "pfkb": "PfkB/ribokinase-family kinases",
    "ghmp": "GHMP-superfamily kinases",
}
ATP_PHOSPHORYL_FAMILY_HINT_ALIASES = {
    "epk": "epk",
    "epk-fold": "epk",
    "rtk": "epk",
    "askha": "askha",
    "hexokinase": "askha",
    "atp-grasp": "atp_grasp",
    "atp grasp": "atp_grasp",
    "ghkl": "ghkl",
    "bergerat": "ghkl",
    "dnk": "dnk",
    "deoxynucleoside": "dnk",
    "ndk": "ndk",
    "nucleoside-diphosphate": "ndk",
    "pfka": "pfka",
    "pfkb": "pfkb",
    "ribokinase": "pfkb",
    "ghmp": "ghmp",
}
ATP_PHOSPHORYL_FAMILY_TEXT_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "ghkl",
        (
            "protein histidine kinase",
            "histidine kinase",
            "chea",
            "pyruvate dehydrogenase",
            "pyruvate dehydrogenase kinase",
            "bergerat",
            "ghkl",
        ),
    ),
    (
        "atp_grasp",
        (
            "atp-grasp",
            "atp grasp",
            "glutathione synthase",
            "d-alanine-(r)-lactate ligase",
            "d-alanine-d-lactate ligase",
        ),
    ),
    (
        "askha",
        ("glucokinase", "hexokinase", "acetate kinase", "acka", "askha"),
    ),
    (
        "dnk",
        (
            "thymidine kinase",
            "deoxyguanosine kinase",
            "deoxynucleoside kinase",
            "dnk",
        ),
    ),
    (
        "ndk",
        (
            "nucleoside-diphosphate kinase",
            "nucleoside diphosphate kinase",
            "(deoxy)nucleoside-phosphate kinase",
            "nucleoside-phosphate kinase",
            "ndk",
        ),
    ),
    ("pfka", ("phosphofructokinase i", "pfka", "pfk-a")),
    (
        "pfkb",
        (
            "ribokinase",
            "hydroxymethylpyrimidine kinase",
            "thid",
            "pfkb",
            "pfk-b",
        ),
    ),
    (
        "ghmp",
        (
            "4-(cytidine 5'-diphospho)-2-c-methyl-d-erythritol kinase",
            "cdp-me kinase",
            "ispE".lower(),
            "ghmp",
        ),
    ),
    (
        "epk",
        (
            "phosphorylase kinase",
            "protein-tyrosine kinase",
            "receptor protein-tyrosine kinase",
            "mitogen-activated protein kinase kinase",
            "map2k",
            "mapkk",
            "kanamycin kinase",
            "aminoglycoside",
            "phosphatidylinositol-5-phosphate 4-kinase",
            "phosphatidylinositol",
            "pip5k",
            "epk",
            "protein kinase",
        ),
    ),
)


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
        reaction_mismatch_reasons = _remap_local_reaction_substrate_mismatch_reasons(
            entry_name=str(result.get("entry_name") or entry.get("entry_name") or ""),
            mechanism_text_snippets=result.get("mechanism_text_snippets")
            or entry.get("mechanism_text_snippets", []),
            top1_fingerprint_id=top1_id,
        )
        atp_family_assignment = _atp_phosphoryl_transfer_family_assignment(
            entry_name=result.get("entry_name") or entry.get("entry_name") or "",
            mechanism_text_snippets=result.get("mechanism_text_snippets")
            or entry.get("mechanism_text_snippets", []),
            top1_fingerprint_id=top1_id,
        )
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
            reaction_substrate_mismatch_reasons=reaction_mismatch_reasons,
            atp_phosphoryl_transfer_family_assignment=atp_family_assignment,
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
                "reaction_substrate_mismatch_reasons": reaction_mismatch_reasons,
                "atp_phosphoryl_transfer_family": atp_family_assignment,
                "atp_phosphoryl_transfer_family_id": _atp_family_id_from_assignment(
                    atp_family_assignment
                ),
                "review_scores": scores,
                "review_score": round(sum(scores.values()), 4),
                "mechanism_text_snippets": result.get("mechanism_text_snippets")
                or entry.get("mechanism_text_snippets", []),
                "readiness_blockers": _review_readiness_blockers(entry, top1_score),
            }
        )

    all_ranked_rows = sorted(
        queue_rows,
        key=lambda row: (-row["review_score"], _entry_id_sort_key(row["entry_id"])),
    )
    ranked_rows = all_ranked_rows[:max_rows]
    omitted_rows = all_ranked_rows[max_rows:]
    for index, row in enumerate(ranked_rows, start=1):
        row["rank"] = index
    omitted_unlabeled_count = sum(
        1 for row in omitted_rows if row["label_state"] == "unlabeled"
    )
    reaction_mismatch_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in ranked_rows
        if row.get("reaction_substrate_mismatch_reasons")
    )
    atp_family_counts = Counter(
        str(row.get("atp_phosphoryl_transfer_family_id"))
        for row in ranked_rows
        if row.get("atp_phosphoryl_transfer_family_id")
    )
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
                "reaction_substrate_mismatch_value",
                "atp_phosphoryl_family_boundary_value",
            ],
            "score_totals": dict(sorted((key, round(value, 4)) for key, value in score_totals.items())),
            "unlabeled_count": sum(1 for row in ranked_rows if row["label_state"] == "unlabeled"),
            "total_unlabeled_candidate_count": sum(
                1 for row in all_ranked_rows if row["label_state"] == "unlabeled"
            ),
            "unlabeled_omitted_by_max_rows": omitted_unlabeled_count,
            "all_unlabeled_rows_retained": omitted_unlabeled_count == 0,
            "reaction_substrate_mismatch_count": len(reaction_mismatch_entry_ids),
            "reaction_substrate_mismatch_entry_ids": reaction_mismatch_entry_ids,
            "atp_phosphoryl_transfer_family_counts": dict(
                sorted(atp_family_counts.items())
            ),
            "atp_phosphoryl_transfer_family_boundary_count": sum(
                atp_family_counts.values()
            ),
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
        atp_family_assignment = _atp_phosphoryl_transfer_family_assignment(
            entry_name=result.get("entry_name") or "",
            mechanism_text_snippets=result.get("mechanism_text_snippets", []),
            top1_fingerprint_id=top1.get("fingerprint_id"),
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
        if atp_family_assignment is not None:
            control_axes = sorted(
                set([*control_axes, "atp_phosphoryl_transfer_family_boundary"])
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
                "atp_phosphoryl_transfer_family": atp_family_assignment,
                "atp_phosphoryl_transfer_family_id": _atp_family_id_from_assignment(
                    atp_family_assignment
                ),
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
    atp_family_counts = Counter(
        str(row.get("atp_phosphoryl_transfer_family_id"))
        for row in ranked_rows
        if row.get("atp_phosphoryl_transfer_family_id")
    )
    return {
        "metadata": {
            "method": "adversarial_negative_control_mining",
            "candidate_count": len(rows),
            "control_count": len(ranked_rows),
            "max_rows": max_rows,
            "abstain_threshold": abstain_threshold,
            "axis_counts": dict(sorted(axis_counts.items())),
            "atp_phosphoryl_transfer_family_counts": dict(
                sorted(atp_family_counts.items())
            ),
            "atp_phosphoryl_transfer_family_boundary_count": sum(
                atp_family_counts.values()
            ),
            "selection_rule": (
                "rank out-of-scope entries that stress ontology boundaries, "
                "cofactor mimics, counterevidence, close top1/top2 families, "
                "ATP/phosphoryl-transfer family boundaries, and abstention-threshold proximity"
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
    family_counts = Counter(
        str(row.get("top1_ontology_family"))
        for row in queue_rows
        if isinstance(row, dict) and row.get("top1_ontology_family")
    )
    dominant_family = family_counts.most_common(1)[0] if family_counts else None
    family_total = sum(family_counts.values())
    dominant_fraction = (
        dominant_family[1] / family_total if dominant_family and family_total else 0.0
    )
    diversity_rows: list[dict[str, Any]] = []
    if dominant_family and dominant_fraction >= 0.6:
        dominant_family_id = dominant_family[0]
        for row in queue_rows:
            if not isinstance(row, dict):
                continue
            entry_id = row.get("entry_id")
            if entry_id in selected_entry_ids:
                continue
            family_id = row.get("top1_ontology_family")
            if family_id and str(family_id) != dominant_family_id:
                diversity_rows.append(row)
                selected_entry_ids.add(entry_id)
    rows.extend(diversity_rows)
    rows.extend(
        row
        for row in queue_rows
        if isinstance(row, dict)
        and row.get("entry_id") not in selected_entry_ids
        and row.get("entry_id") not in labels_by_entry
    )
    export_family_counts = Counter(
        str(row.get("top1_ontology_family"))
        for row in rows
        if isinstance(row, dict) and row.get("top1_ontology_family")
    )
    return {
        "metadata": {
            "method": "expert_review_export",
            "exported_count": len(rows),
            "max_ranked_rows": max_rows,
            "unlabeled_inclusion_rule": "append all unlabeled queue rows even when ranked below the export cutoff",
            "diversity_inclusion_rule": (
                "when one top1 ontology family covers at least 60% of the active "
                "queue, append all rows from non-dominant families so expert "
                "review does not collapse to one chemistry"
            ),
            "dominant_top1_ontology_family": dominant_family[0] if dominant_family else None,
            "dominant_top1_ontology_family_fraction": round(dominant_fraction, 4),
            "diversity_added_count": len(diversity_rows),
            "queue_top1_ontology_family_counts": dict(sorted(family_counts.items())),
            "export_top1_ontology_family_counts": dict(sorted(export_family_counts.items())),
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


def build_expert_label_decision_review_export(
    *,
    active_learning_queue: dict[str, Any],
    labels: list[MechanismLabel],
    review_debt: dict[str, Any] | None = None,
    reaction_substrate_mismatch_review_export: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export active-queue expert-label decisions without creating countable labels."""
    labels_by_entry = {label.entry_id: label for label in labels}
    review_debt_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in (review_debt or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    review_debt_meta = (review_debt or {}).get("metadata", {})
    carried_debt_ids = {
        str(entry_id)
        for entry_id in review_debt_meta.get("carried_review_debt_entry_ids", [])
        if isinstance(entry_id, str)
    }
    new_debt_ids = {
        str(entry_id)
        for entry_id in review_debt_meta.get("new_review_debt_entry_ids", [])
        if isinstance(entry_id, str)
    }
    all_debt_ids = carried_debt_ids | new_debt_ids
    mismatch_export_meta = (
        reaction_substrate_mismatch_review_export or {}
    ).get("metadata", {})
    mismatch_export_entry_ids = set(
        _sorted_entry_ids(mismatch_export_meta.get("exported_entry_ids", []))
    )
    if reaction_substrate_mismatch_review_export and not mismatch_export_entry_ids:
        mismatch_export_entry_ids = set(
            _sorted_entry_ids(
                item.get("entry_id")
                for item in reaction_substrate_mismatch_review_export.get(
                    "review_items", []
                )
                if isinstance(item, dict)
            )
        )

    rows = [
        row
        for row in active_learning_queue.get("rows", [])
        if isinstance(row, dict)
        and isinstance(row.get("entry_id"), str)
        and row.get("recommended_action") == "expert_label_decision_needed"
    ]
    rows = sorted(
        rows,
        key=lambda row: (
            int(row.get("rank", 0) or 0),
            _entry_id_sort_key(str(row.get("entry_id"))),
        ),
    )

    review_items: list[dict[str, Any]] = []
    mismatch_entry_ids: list[str] = []
    for row in rows:
        entry_id = str(row["entry_id"])
        mismatch_reasons = _sorted_strings(
            row.get("reaction_substrate_mismatch_reasons", [])
        )
        if mismatch_reasons:
            mismatch_entry_ids.append(entry_id)
        debt_status = (
            "carried"
            if entry_id in carried_debt_ids
            else "new"
            if entry_id in new_debt_ids
            else None
        )
        resolution_lane = (
            "already_routed_reaction_substrate_mismatch_export"
            if mismatch_reasons and entry_id in mismatch_export_entry_ids
            else "needs_reaction_substrate_mismatch_export"
            if mismatch_reasons
            else "external_expert_label_decision"
        )
        quality_risk_flags = _expert_label_decision_review_flags(
            row,
            mismatch_reasons,
        )
        label = labels_by_entry.get(entry_id)
        review_items.append(
            {
                "rank": row.get("rank"),
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "current_label": label.to_dict() if label else None,
                "queue_context": row,
                "review_debt_context": review_debt_rows_by_entry.get(entry_id),
                "expert_label_decision_context": {
                    "source_recommended_action": row.get("recommended_action"),
                    "resolution_lane": resolution_lane,
                    "external_review_required": True,
                    "countable_label_candidate": False,
                    "review_debt_status": debt_status,
                    "review_debt_present": entry_id in all_debt_ids,
                    "reaction_substrate_mismatch_reasons": mismatch_reasons,
                    "covered_by_reaction_substrate_mismatch_export": (
                        entry_id in mismatch_export_entry_ids
                    ),
                    "quality_risk_flags": quality_risk_flags,
                    "automation_import_policy": (
                        "no_decision only; automation must not accept, reject, "
                        "or count this row without external expert resolution"
                    ),
                },
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
                    "expert_label_resolution": "needs_external_review",
                },
            }
        )

    exported_entry_ids = _sorted_entry_ids(
        item.get("entry_id") for item in review_items
    )
    missing_mismatch_export_entry_ids = _sorted_entry_ids(
        set(mismatch_entry_ids) - mismatch_export_entry_ids
    )
    family_counts = Counter(
        str(row.get("top1_ontology_family"))
        for row in rows
        if row.get("top1_ontology_family")
    )
    label_state_counts = Counter(
        str(row.get("label_state", "unknown")) for row in rows
    )
    debt_status_counts = Counter(
        item["expert_label_decision_context"]["review_debt_status"] or "none"
        for item in review_items
    )
    quality_risk_counts = Counter(
        flag
        for item in review_items
        for flag in item["expert_label_decision_context"]["quality_risk_flags"]
    )
    return {
        "metadata": {
            "method": "expert_label_decision_review_export",
            "source_method": active_learning_queue.get("metadata", {}).get("method"),
            "source_recommended_action": "expert_label_decision_needed",
            "active_queue_expert_label_decision_count": len(rows),
            "exported_count": len(review_items),
            "exported_entry_ids": exported_entry_ids,
            "countable_label_candidate_count": 0,
            "decision_counts": {"no_decision": len(review_items)}
            if review_items
            else {},
            "current_label_count": sum(
                1 for item in review_items if item.get("current_label") is not None
            ),
            "unlabeled_count": sum(
                1 for item in review_items if item.get("current_label") is None
            ),
            "top1_ontology_family_counts": dict(sorted(family_counts.items())),
            "label_state_counts": dict(sorted(label_state_counts.items())),
            "review_debt_status_counts": dict(sorted(debt_status_counts.items())),
            "quality_risk_flag_counts": dict(sorted(quality_risk_counts.items())),
            "review_debt_linked_count": sum(
                1
                for item in review_items
                if item["expert_label_decision_context"]["review_debt_present"]
            ),
            "reaction_substrate_mismatch_lane_count": len(set(mismatch_entry_ids)),
            "reaction_substrate_mismatch_already_exported_count": len(
                set(mismatch_entry_ids) & mismatch_export_entry_ids
            ),
            "missing_reaction_substrate_mismatch_export_entry_ids": (
                missing_mismatch_export_entry_ids
            ),
            "export_ready": len(review_items) == len(rows)
            and not missing_mismatch_export_entry_ids,
            "review_only_rule": (
                "active-queue expert-label decisions are context exports only; "
                "automation leaves them as no_decision and countable import must "
                "not add benchmark labels without external expert resolution"
            ),
        },
        "review_items": review_items,
    }


def _expert_label_decision_review_flags(
    row: dict[str, Any],
    mismatch_reasons: list[str],
) -> list[str]:
    flags = {"external_expert_decision_required"}
    top1 = str(row.get("top1_fingerprint_id") or "")
    top2 = str(row.get("top2_fingerprint_id") or "")
    top1_score = float(row.get("top1_score", 0.0) or 0.0)
    top2_score = float(row.get("top2_score", 0.0) or 0.0)
    threshold = float(row.get("abstain_threshold", 0.0) or 0.0)
    cofactor_level = str(row.get("cofactor_evidence_level") or "unknown")
    blockers = _sorted_strings(row.get("readiness_blockers", []))
    counterevidence = _sorted_strings(row.get("counterevidence_reasons", []))
    snippets = row.get("mechanism_text_snippets", [])
    text = " ".join(str(snippet) for snippet in snippets)
    entry_name = str(row.get("entry_name") or "")

    cofactor_sensitive_top1 = top1 in {
        "cobalamin_radical_rearrangement",
        "flavin_dehydrogenase_reductase",
        "flavin_monooxygenase",
        "heme_peroxidase_oxidase",
        "metal_dependent_hydrolase",
    }
    if mismatch_reasons:
        flags.add("reaction_substrate_mismatch")
    if any(
        blocker
        in {
            "geometry_status_not_ok",
            "fewer_than_three_resolved_residues",
            "missing_pairwise_geometry",
        }
        for blocker in blockers
    ):
        flags.add("active_site_mapping_or_structure_gap")
    if cofactor_sensitive_top1 and cofactor_level in {
        "absent",
        "structure_only",
        "role_inferred",
        "unknown",
    }:
        flags.add("cofactor_family_ambiguity")
    if counterevidence:
        flags.add("counterevidence_boundary")
    if (
        top1 == "metal_dependent_hydrolase"
        and top2 == "ser_his_acid_hydrolase"
        and _has_ser_his_hydrolase_text(text.lower(), entry_name)
    ):
        flags.add("ser_his_metal_boundary")
    if top1 and top2 and fingerprint_family(top1) == fingerprint_family(top2):
        if abs(top1_score - top2_score) <= 0.05:
            flags.add("sibling_mechanism_confusion")
    if (
        threshold
        and top1_score >= threshold
        and cofactor_sensitive_top1
        and cofactor_level != "ligand_supported"
    ):
        flags.add("text_leakage_or_nonlocal_evidence_risk")
    if any(
        reason
        in {
            "glycosidase_not_metal_hydrolase_seed",
            "nucleotide_transfer_ligand_context",
            "role_inferred_metal_missing_water_activation_role",
        }
        for reason in counterevidence
    ):
        flags.add("substrate_class_boundary")
    return sorted(flags)


def summarize_expert_label_decision_repair_candidates(
    expert_label_decision_review_export: dict[str, Any],
    *,
    review_debt_remediation: dict[str, Any] | None = None,
    structure_mapping: dict[str, Any] | None = None,
    alternate_structure_scan: dict[str, Any] | None = None,
    max_rows: int = 30,
) -> dict[str, Any]:
    """Prioritize review-only expert-label rows for non-countable repair work."""
    remediation_by_entry = {
        str(row.get("entry_id")): row
        for row in (review_debt_remediation or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    mapping_by_entry = {
        str(row.get("entry_id")): row
        for row in (structure_mapping or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    alternate_scan_by_entry = {
        str(row.get("entry_id")): row
        for row in (alternate_structure_scan or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    def _alternate_scan_context(row: dict[str, Any]) -> dict[str, Any] | None:
        if not row:
            return None
        structure_hits = row.get("structure_hits", [])
        if not isinstance(structure_hits, list):
            structure_hits = []
        scanned_structure_count = row.get("scanned_structure_count")
        if scanned_structure_count is None:
            scanned_structure_count = row.get("candidate_pdb_count")
        if scanned_structure_count is None and isinstance(
            row.get("scanned_pdb_ids"), list
        ):
            scanned_structure_count = len(row["scanned_pdb_ids"])
        local_expected_family_hit_count = row.get("local_expected_family_hit_count")
        if local_expected_family_hit_count is None:
            local_expected_family_hit_count = sum(
                1
                for hit in structure_hits
                if isinstance(hit, dict) and hit.get("local_expected_family_hits")
            )
        structure_wide_expected_family_hit_count = row.get(
            "structure_wide_expected_family_hit_count"
        )
        if structure_wide_expected_family_hit_count is None:
            structure_wide_expected_family_hit_count = sum(
                1
                for hit in structure_hits
                if isinstance(hit, dict) and hit.get("expected_family_hits")
            )
        return {
            "scan_outcome": row.get("scan_outcome"),
            "scanned_structure_count": scanned_structure_count,
            "local_expected_family_hit_count": local_expected_family_hit_count,
            "structure_wide_expected_family_hit_count": (
                structure_wide_expected_family_hit_count
            ),
            "local_active_site_expected_family_observed": row.get(
                "local_active_site_expected_family_observed"
            ),
            "selected_structure_expected_family_observed": row.get(
                "selected_structure_expected_family_observed"
            ),
            "alternate_structure_expected_family_observed": row.get(
                "alternate_structure_expected_family_observed"
            ),
        }

    candidate_rows: list[dict[str, Any]] = []
    for item in expert_label_decision_review_export.get("review_items", []):
        if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
            continue
        entry_id = str(item["entry_id"])
        context = item.get("expert_label_decision_context", {})
        if not isinstance(context, dict):
            context = {}
        queue_context = item.get("queue_context", {})
        if not isinstance(queue_context, dict):
            queue_context = {}
        flags = _sorted_strings(context.get("quality_risk_flags", []))
        repair_bucket = _expert_label_decision_repair_bucket(flags)
        remediation_row = remediation_by_entry.get(entry_id, {})
        mapping_row = mapping_by_entry.get(entry_id, {})
        alternate_scan_row = alternate_scan_by_entry.get(entry_id, {})
        candidate_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": item.get("entry_name"),
                "rank": item.get("rank"),
                "repair_bucket": repair_bucket,
                "quality_risk_flags": flags,
                "top1_fingerprint_id": queue_context.get("top1_fingerprint_id"),
                "top1_ontology_family": queue_context.get("top1_ontology_family"),
                "top1_score": queue_context.get("top1_score"),
                "top2_fingerprint_id": queue_context.get("top2_fingerprint_id"),
                "top2_score": queue_context.get("top2_score"),
                "cofactor_evidence_level": queue_context.get("cofactor_evidence_level"),
                "readiness_blockers": queue_context.get("readiness_blockers", []),
                "counterevidence_reasons": queue_context.get(
                    "counterevidence_reasons", []
                ),
                "reaction_substrate_mismatch_reasons": context.get(
                    "reaction_substrate_mismatch_reasons", []
                ),
                "review_debt_remediation_context": {
                    "remediation_bucket": remediation_row.get("remediation_bucket"),
                    "selected_pdb_id": remediation_row.get("selected_pdb_id"),
                    "candidate_pdb_structure_count": remediation_row.get(
                        "candidate_pdb_structure_count"
                    ),
                    "alternate_pdb_count": remediation_row.get("alternate_pdb_count"),
                    "selected_pdb_residue_position_count": remediation_row.get(
                        "selected_pdb_residue_position_count"
                    ),
                    "alternate_pdb_with_residue_positions_count": remediation_row.get(
                        "alternate_pdb_with_residue_positions_count"
                    ),
                }
                if remediation_row
                else None,
                "structure_mapping_status": mapping_row.get("status"),
                "alternate_structure_scan_context": _alternate_scan_context(
                    alternate_scan_row
                ),
                "countable_label_candidate": False,
                "recommended_next_action": _expert_label_decision_repair_action(
                    repair_bucket
                ),
            }
        )

    bucket_priority = {
        "active_site_mapping_or_structure_gap_repair": 0,
        "text_leakage_or_nonlocal_evidence_guardrail": 1,
        "cofactor_evidence_repair": 2,
        "ser_his_metal_boundary_review": 3,
        "sibling_mechanism_boundary_review": 4,
        "reaction_substrate_review_already_exported": 5,
        "external_expert_label_decision": 6,
    }
    ranked_rows = sorted(
        candidate_rows,
        key=lambda row: (
            bucket_priority.get(str(row["repair_bucket"]), 99),
            int(row.get("rank", 0) or 0),
            _entry_id_sort_key(str(row["entry_id"])),
        ),
    )
    bucket_counts = Counter(str(row["repair_bucket"]) for row in candidate_rows)
    flag_counts = Counter(
        flag for row in candidate_rows for flag in row.get("quality_risk_flags", [])
    )
    emitted_rows = ranked_rows if max_rows <= 0 else ranked_rows[:max_rows]
    candidate_entry_ids = _sorted_entry_ids(row.get("entry_id") for row in candidate_rows)
    return {
        "metadata": {
            "method": "expert_label_decision_repair_candidate_summary",
            "source_method": expert_label_decision_review_export.get(
                "metadata", {}
            ).get("method"),
            "candidate_count": len(candidate_rows),
            "emitted_row_count": len(emitted_rows),
            "omitted_by_max_rows": max(0, len(ranked_rows) - len(emitted_rows)),
            "all_candidates_retained": len(emitted_rows) == len(ranked_rows),
            "max_rows": max_rows,
            "countable_label_candidate_count": 0,
            "candidate_entry_ids": candidate_entry_ids,
            "repair_bucket_counts": dict(sorted(bucket_counts.items())),
            "quality_risk_flag_counts": dict(sorted(flag_counts.items())),
            "remediation_context_linked_count": sum(
                1
                for row in candidate_rows
                if row.get("review_debt_remediation_context") is not None
            ),
            "structure_mapping_context_linked_count": sum(
                1 for row in candidate_rows if row.get("structure_mapping_status")
            ),
            "alternate_structure_scan_context_linked_count": sum(
                1
                for row in candidate_rows
                if row.get("alternate_structure_scan_context") is not None
            ),
            "review_only_rule": (
                "repair candidates identify evidence work only; they do not "
                "accept, reject, or count expert-label decision rows"
            ),
        },
        "rows": emitted_rows,
    }


def _expert_label_decision_repair_bucket(flags: list[str]) -> str:
    flag_set = set(flags)
    if "active_site_mapping_or_structure_gap" in flag_set:
        return "active_site_mapping_or_structure_gap_repair"
    if "text_leakage_or_nonlocal_evidence_risk" in flag_set:
        return "text_leakage_or_nonlocal_evidence_guardrail"
    if "cofactor_family_ambiguity" in flag_set:
        return "cofactor_evidence_repair"
    if "ser_his_metal_boundary" in flag_set:
        return "ser_his_metal_boundary_review"
    if "sibling_mechanism_confusion" in flag_set:
        return "sibling_mechanism_boundary_review"
    if "reaction_substrate_mismatch" in flag_set:
        return "reaction_substrate_review_already_exported"
    return "external_expert_label_decision"


def _expert_label_decision_repair_action(repair_bucket: str) -> str:
    return {
        "active_site_mapping_or_structure_gap_repair": (
            "inspect selected structure mapping, residue resolution, and alternate "
            "PDB support before any label decision"
        ),
        "text_leakage_or_nonlocal_evidence_guardrail": (
            "require local mechanistic evidence; do not count text-only or "
            "nonlocal support"
        ),
        "cofactor_evidence_repair": (
            "inspect local cofactor evidence and counterevidence before review"
        ),
        "ser_his_metal_boundary_review": (
            "keep Ser-His versus metal-hydrolase boundary rows in review"
        ),
        "sibling_mechanism_boundary_review": (
            "compare sibling mechanism evidence before external review"
        ),
        "reaction_substrate_review_already_exported": (
            "use the dedicated reaction/substrate mismatch review export"
        ),
        "external_expert_label_decision": (
            "external expert label decision required"
        ),
    }.get(repair_bucket, "external expert label decision required")


def audit_expert_label_decision_repair_guardrails(
    expert_label_decision_repair_candidates: dict[str, Any],
    *,
    remap_local_lead_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit priority expert-label repair lanes before any countable import."""
    repair_meta = expert_label_decision_repair_candidates.get("metadata", {})
    remap_meta = (remap_local_lead_audit or {}).get("metadata", {})
    strict_remap_ids = set(
        _sorted_entry_ids(remap_meta.get("strict_remap_guardrail_entry_ids", []))
    )
    family_review_ids = set(
        _sorted_entry_ids(remap_meta.get("expert_family_boundary_review_entry_ids", []))
    )
    reaction_review_ids = set(
        _sorted_entry_ids(
            remap_meta.get("expert_reaction_substrate_review_entry_ids", [])
        )
    )

    priority_rows: list[dict[str, Any]] = []
    for row in expert_label_decision_repair_candidates.get("rows", []):
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        flags = set(_sorted_strings(row.get("quality_risk_flags", [])))
        if flags & {
            "active_site_mapping_or_structure_gap",
            "text_leakage_or_nonlocal_evidence_risk",
        }:
            priority_rows.append(row)

    audit_rows: list[dict[str, Any]] = []
    for row in priority_rows:
        entry_id = str(row["entry_id"])
        flags = set(_sorted_strings(row.get("quality_risk_flags", [])))
        readiness_blockers = _sorted_strings(row.get("readiness_blockers", []))
        counterevidence = _sorted_strings(row.get("counterevidence_reasons", []))
        mismatch_reasons = _sorted_strings(
            row.get("reaction_substrate_mismatch_reasons", [])
        )
        rem_context = row.get("review_debt_remediation_context")
        if not isinstance(rem_context, dict):
            rem_context = {}
        scan_context = row.get("alternate_structure_scan_context")
        if not isinstance(scan_context, dict):
            scan_context = {}

        local_hit_count = int(scan_context.get("local_expected_family_hit_count", 0) or 0)
        structure_wide_hit_count = int(
            scan_context.get("structure_wide_expected_family_hit_count", 0) or 0
        )
        local_observed = (
            bool(scan_context.get("local_active_site_expected_family_observed"))
            or local_hit_count > 0
        )
        selected_observed = bool(
            scan_context.get("selected_structure_expected_family_observed")
        )
        alternate_observed = bool(
            scan_context.get("alternate_structure_expected_family_observed")
        )
        selected_position_count = int(
            rem_context.get("selected_pdb_residue_position_count", 0) or 0
        )
        alternate_position_count = int(
            rem_context.get("alternate_pdb_with_residue_positions_count", 0) or 0
        )

        blockers = {"external_expert_decision_required"}
        if row.get("countable_label_candidate") is True:
            blockers.add("repair_candidate_marked_countable")
        if "active_site_mapping_or_structure_gap" in flags:
            blockers.add("active_site_mapping_or_structure_gap_unresolved")
        if "text_leakage_or_nonlocal_evidence_risk" in flags:
            blockers.add("text_leakage_or_nonlocal_evidence_risk_unresolved")
        if "cofactor_family_ambiguity" in flags and not local_observed:
            blockers.add("missing_local_active_site_expected_family_evidence")
        if counterevidence:
            blockers.add("counterevidence_boundary_unresolved")
        if mismatch_reasons or entry_id in reaction_review_ids:
            blockers.add("reaction_substrate_mismatch_review_required")
        if entry_id in family_review_ids:
            blockers.add("expert_family_boundary_review_required")
        if entry_id in strict_remap_ids or (local_observed and alternate_position_count == 0):
            blockers.add("strict_conservative_remap_guardrail")
        if readiness_blockers:
            blockers.add("readiness_blockers_unresolved")
        if selected_position_count and selected_position_count < 3:
            blockers.add("insufficient_selected_structure_residue_support")
        if structure_wide_hit_count > 0 and not local_observed:
            blockers.add("structure_wide_only_evidence_noncountable")

        if local_observed and (
            entry_id in strict_remap_ids or alternate_position_count == 0
        ):
            local_evidence_status = (
                "local_expected_family_evidence_from_conservative_remap_review_only"
            )
        elif local_observed:
            local_evidence_status = (
                "local_expected_family_evidence_observed_review_only"
            )
        elif structure_wide_hit_count > 0 or selected_observed or alternate_observed:
            local_evidence_status = (
                "nonlocal_or_structure_wide_expected_family_evidence_only"
            )
        elif scan_context:
            local_evidence_status = "no_local_expected_family_evidence"
        else:
            local_evidence_status = "not_scanned_or_no_alternate_context"

        audit_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "repair_bucket": row.get("repair_bucket"),
                "quality_risk_flags": _sorted_strings(flags),
                "readiness_blockers": readiness_blockers,
                "counterevidence_reasons": counterevidence,
                "reaction_substrate_mismatch_reasons": mismatch_reasons,
                "local_mechanistic_evidence_status": local_evidence_status,
                "local_expected_family_hit_count": local_hit_count,
                "structure_wide_expected_family_hit_count": structure_wide_hit_count,
                "selected_pdb_id": rem_context.get("selected_pdb_id"),
                "selected_pdb_residue_position_count": selected_position_count,
                "alternate_pdb_with_residue_positions_count": alternate_position_count,
                "strict_remap_guardrail": entry_id in strict_remap_ids,
                "countable_label_candidate": False,
                "non_countable_blockers": sorted(blockers),
                "recommended_next_action": (
                    "keep as review-only evidence repair; require local "
                    "mechanistic evidence plus external expert resolution before "
                    "any countable import"
                ),
            }
        )

    blocker_counts = Counter(
        blocker for row in audit_rows for blocker in row["non_countable_blockers"]
    )
    local_evidence_entry_ids = _sorted_entry_ids(
        row["entry_id"]
        for row in audit_rows
        if row["local_mechanistic_evidence_status"]
        in {
            "local_expected_family_evidence_from_conservative_remap_review_only",
            "local_expected_family_evidence_observed_review_only",
        }
    )
    structure_wide_only_entry_ids = _sorted_entry_ids(
        row["entry_id"]
        for row in audit_rows
        if row["local_mechanistic_evidence_status"]
        == "nonlocal_or_structure_wide_expected_family_evidence_only"
    )
    missing_local_entry_ids = _sorted_entry_ids(
        row["entry_id"]
        for row in audit_rows
        if row["local_mechanistic_evidence_status"]
        in {"no_local_expected_family_evidence", "not_scanned_or_no_alternate_context"}
    )
    priority_entry_ids = _sorted_entry_ids(row["entry_id"] for row in audit_rows)
    countable_candidate_count = sum(
        1 for row in audit_rows if row.get("countable_label_candidate") is True
    )
    candidate_count = int(repair_meta.get("candidate_count", 0) or 0)
    full_table_input = bool(repair_meta.get("all_candidates_retained")) or (
        candidate_count > 0
        and len(expert_label_decision_repair_candidates.get("rows", []))
        >= candidate_count
    )
    all_priority_lanes_non_countable = (
        countable_candidate_count == 0
        and all(row["non_countable_blockers"] for row in audit_rows)
    )
    guardrail_ready = full_table_input and all_priority_lanes_non_countable
    return {
        "metadata": {
            "method": "expert_label_decision_repair_guardrail_audit",
            "source_method": repair_meta.get("method"),
            "candidate_count": candidate_count,
            "full_table_input": full_table_input,
            "priority_repair_row_count": len(audit_rows),
            "priority_repair_entry_ids": priority_entry_ids,
            "active_site_mapping_or_structure_gap_row_count": sum(
                1
                for row in audit_rows
                if "active_site_mapping_or_structure_gap"
                in row.get("quality_risk_flags", [])
            ),
            "text_leakage_or_nonlocal_evidence_risk_row_count": sum(
                1
                for row in audit_rows
                if "text_leakage_or_nonlocal_evidence_risk"
                in row.get("quality_risk_flags", [])
            ),
            "local_expected_family_evidence_review_only_count": len(
                local_evidence_entry_ids
            ),
            "local_expected_family_evidence_review_only_entry_ids": (
                local_evidence_entry_ids
            ),
            "structure_wide_only_evidence_entry_ids": structure_wide_only_entry_ids,
            "missing_local_mechanistic_evidence_entry_ids": missing_local_entry_ids,
            "strict_remap_guardrail_entry_ids": _sorted_entry_ids(strict_remap_ids),
            "non_countable_blocker_counts": dict(sorted(blocker_counts.items())),
            "countable_label_candidate_count": countable_candidate_count,
            "all_priority_lanes_non_countable": all_priority_lanes_non_countable,
            "guardrail_ready": guardrail_ready,
            "audit_recommendation": (
                "continue_repair_before_count_growth"
                if audit_rows
                else "no_priority_repair_lanes_detected"
            ),
            "review_only_rule": (
                "priority expert-label repair lanes stay non-countable unless "
                "local mechanistic evidence is explicit and external expert "
                "resolution removes review blockers"
            ),
        },
        "rows": audit_rows,
    }


def audit_expert_label_decision_local_evidence_gaps(
    expert_label_decision_repair_guardrail_audit: dict[str, Any],
    *,
    expert_label_decision_repair_candidates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify local-evidence gaps in priority expert-label repair lanes."""
    guardrail_meta = expert_label_decision_repair_guardrail_audit.get("metadata", {})
    candidate_by_entry = {
        str(row.get("entry_id")): row
        for row in (expert_label_decision_repair_candidates or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for guardrail_row in expert_label_decision_repair_guardrail_audit.get("rows", []):
        if not isinstance(guardrail_row, dict) or not isinstance(
            guardrail_row.get("entry_id"), str
        ):
            continue
        entry_id = str(guardrail_row["entry_id"])
        candidate_row = candidate_by_entry.get(entry_id, {})
        rem_context = candidate_row.get("review_debt_remediation_context")
        if not isinstance(rem_context, dict):
            rem_context = {}
        remediation_context_present = bool(rem_context)
        scan_context = candidate_row.get("alternate_structure_scan_context")
        if not isinstance(scan_context, dict):
            scan_context = {}

        quality_flags = _sorted_strings(
            guardrail_row.get("quality_risk_flags")
            or candidate_row.get("quality_risk_flags", [])
        )
        blockers = _sorted_strings(guardrail_row.get("non_countable_blockers", []))
        local_status = str(
            guardrail_row.get("local_mechanistic_evidence_status") or "unknown"
        )
        selected_residue_count = int(
            guardrail_row.get("selected_pdb_residue_position_count")
            if guardrail_row.get("selected_pdb_residue_position_count") is not None
            else rem_context.get("selected_pdb_residue_position_count", 0)
            or 0
        )
        alternate_position_count = int(
            guardrail_row.get("alternate_pdb_with_residue_positions_count")
            if guardrail_row.get("alternate_pdb_with_residue_positions_count")
            is not None
            else rem_context.get("alternate_pdb_with_residue_positions_count", 0)
            or 0
        )
        candidate_pdb_count = int(
            rem_context.get("candidate_pdb_structure_count", 0) or 0
        )
        alternate_pdb_count = int(rem_context.get("alternate_pdb_count", 0) or 0)
        local_hit_count = int(
            guardrail_row.get("local_expected_family_hit_count")
            if guardrail_row.get("local_expected_family_hit_count") is not None
            else scan_context.get("local_expected_family_hit_count", 0)
            or 0
        )
        structure_wide_hit_count = int(
            guardrail_row.get("structure_wide_expected_family_hit_count")
            if guardrail_row.get("structure_wide_expected_family_hit_count")
            is not None
            else scan_context.get("structure_wide_expected_family_hit_count", 0)
            or 0
        )
        scanned_structure_count = int(
            scan_context.get("scanned_structure_count", 0) or 0
        )

        gap_classes: set[str] = set()
        if local_status in {
            "local_expected_family_evidence_from_conservative_remap_review_only",
            "local_expected_family_evidence_observed_review_only",
        }:
            gap_classes.add("local_evidence_review_only_not_countable")
        elif local_status == "nonlocal_or_structure_wide_expected_family_evidence_only":
            gap_classes.add("structure_wide_or_nonlocal_evidence_only")
        elif local_status == "not_scanned_or_no_alternate_context":
            gap_classes.add("not_scanned_or_no_alternate_context")
        elif local_status == "no_local_expected_family_evidence":
            gap_classes.add("scanned_without_local_expected_family_evidence")
        else:
            gap_classes.add("local_evidence_status_unknown")

        if selected_residue_count < 3:
            gap_classes.add("selected_structure_residue_support_shortfall")
        if not remediation_context_present and not candidate_row:
            gap_classes.add("repair_candidate_context_missing")
        if (
            remediation_context_present
            and candidate_pdb_count <= 1
            and alternate_pdb_count == 0
        ):
            gap_classes.add("single_structure_no_alternate_context")
        if alternate_pdb_count > 0 and alternate_position_count == 0:
            gap_classes.add("alternate_structures_lack_explicit_residue_positions")
        if structure_wide_hit_count > 0 and local_hit_count == 0:
            gap_classes.add("structure_wide_hit_without_local_support")
        if scanned_structure_count > 0 and local_hit_count == 0:
            gap_classes.add("scanned_structures_without_local_expected_family_hit")
        if guardrail_row.get("strict_remap_guardrail"):
            gap_classes.add("strict_conservative_remap_guardrail")
        if guardrail_row.get("counterevidence_reasons"):
            gap_classes.add("counterevidence_boundary_unresolved")
        if guardrail_row.get("reaction_substrate_mismatch_reasons"):
            gap_classes.add("reaction_substrate_mismatch_review_required")
        if "text_leakage_or_nonlocal_evidence_risk" in quality_flags:
            gap_classes.add("text_leakage_or_nonlocal_evidence_risk")

        if "reaction_substrate_mismatch_review_required" in gap_classes:
            recommended_action = "route_to_reaction_substrate_expert_review"
        elif "counterevidence_boundary_unresolved" in gap_classes:
            recommended_action = "route_to_family_boundary_expert_review"
        elif "structure_wide_hit_without_local_support" in gap_classes:
            recommended_action = "inspect_active_site_mapping_or_structure_selection"
        elif "alternate_structures_lack_explicit_residue_positions" in gap_classes:
            recommended_action = "source_explicit_alternate_structure_residue_positions"
        elif "single_structure_no_alternate_context" in gap_classes:
            recommended_action = "source_external_cofactor_or_structure_evidence"
        elif "selected_structure_residue_support_shortfall" in gap_classes:
            recommended_action = "repair_selected_structure_residue_mapping"
        elif "local_evidence_review_only_not_countable" in gap_classes:
            recommended_action = "keep_local_evidence_review_only_until_expert_resolution"
        else:
            recommended_action = "collect_local_mechanistic_evidence_before_count_growth"

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": guardrail_row.get("entry_name")
                or candidate_row.get("entry_name"),
                "repair_bucket": guardrail_row.get("repair_bucket")
                or candidate_row.get("repair_bucket"),
                "quality_risk_flags": quality_flags,
                "local_mechanistic_evidence_status": local_status,
                "local_evidence_gap_classes": sorted(gap_classes),
                "recommended_next_action": recommended_action,
                "countable_label_candidate": False,
                "non_countable_blockers": blockers,
                "selected_pdb_id": guardrail_row.get("selected_pdb_id")
                or rem_context.get("selected_pdb_id"),
                "selected_pdb_residue_position_count": selected_residue_count,
                "candidate_pdb_structure_count": candidate_pdb_count,
                "alternate_pdb_count": alternate_pdb_count,
                "alternate_pdb_with_residue_positions_count": alternate_position_count,
                "alternate_structure_scan_outcome": scan_context.get("scan_outcome"),
                "alternate_structure_scanned_structure_count": scanned_structure_count,
                "local_expected_family_hit_count": local_hit_count,
                "structure_wide_expected_family_hit_count": structure_wide_hit_count,
                "top1_fingerprint_id": candidate_row.get("top1_fingerprint_id"),
                "top1_ontology_family": candidate_row.get("top1_ontology_family"),
                "top1_score": candidate_row.get("top1_score"),
                "cofactor_evidence_level": candidate_row.get(
                    "cofactor_evidence_level"
                ),
                "counterevidence_reasons": _sorted_strings(
                    guardrail_row.get("counterevidence_reasons", [])
                ),
                "reaction_substrate_mismatch_reasons": _sorted_strings(
                    guardrail_row.get("reaction_substrate_mismatch_reasons", [])
                ),
                "review_policy": (
                    "local-evidence gap rows are evidence-repair work only; they "
                    "cannot become countable labels without explicit local "
                    "mechanistic evidence, external review resolution, and a "
                    "passing label-factory gate"
                ),
            }
        )

    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))
    audited_entry_ids = _sorted_entry_ids(row.get("entry_id") for row in rows)
    priority_entry_ids = _sorted_entry_ids(
        guardrail_meta.get("priority_repair_entry_ids", [])
    )
    if not priority_entry_ids:
        priority_entry_ids = audited_entry_ids
    missing_priority_ids = _sorted_entry_ids(
        set(priority_entry_ids) - set(audited_entry_ids)
    )
    gap_class_counts = Counter(
        gap_class
        for row in rows
        for gap_class in row.get("local_evidence_gap_classes", [])
    )
    action_counts = Counter(str(row.get("recommended_next_action")) for row in rows)
    selected_shortfall_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if "selected_structure_residue_support_shortfall"
        in row.get("local_evidence_gap_classes", [])
    )
    no_alternate_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if "single_structure_no_alternate_context"
        in row.get("local_evidence_gap_classes", [])
    )
    alternate_lacks_positions_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if "alternate_structures_lack_explicit_residue_positions"
        in row.get("local_evidence_gap_classes", [])
    )
    structure_wide_only_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if "structure_wide_hit_without_local_support"
        in row.get("local_evidence_gap_classes", [])
        or row.get("local_mechanistic_evidence_status")
        == "nonlocal_or_structure_wide_expected_family_evidence_only"
    )
    countable_candidate_count = sum(
        1 for row in rows if row.get("countable_label_candidate") is True
    )
    priority_rows_accounted_for = not missing_priority_ids and (
        len(audited_entry_ids) >= len(priority_entry_ids)
    )
    all_audited_rows_non_countable = countable_candidate_count == 0 and all(
        row.get("non_countable_blockers") for row in rows
    )
    audit_ready = priority_rows_accounted_for and all_audited_rows_non_countable
    return {
        "metadata": {
            "method": "expert_label_decision_local_evidence_gap_audit",
            "source_guardrail_method": guardrail_meta.get("method"),
            "source_repair_candidate_method": (
                (expert_label_decision_repair_candidates or {})
                .get("metadata", {})
                .get("method")
            ),
            "priority_repair_row_count": len(priority_entry_ids),
            "audited_entry_count": len(rows),
            "audited_entry_ids": audited_entry_ids,
            "missing_priority_entry_ids": missing_priority_ids,
            "priority_rows_accounted_for": priority_rows_accounted_for,
            "local_evidence_gap_class_counts": dict(sorted(gap_class_counts.items())),
            "recommended_action_counts": dict(sorted(action_counts.items())),
            "missing_local_mechanistic_evidence_entry_ids": _sorted_entry_ids(
                guardrail_meta.get("missing_local_mechanistic_evidence_entry_ids", [])
            ),
            "structure_wide_only_evidence_entry_ids": structure_wide_only_ids,
            "local_expected_family_evidence_review_only_entry_ids": _sorted_entry_ids(
                guardrail_meta.get(
                    "local_expected_family_evidence_review_only_entry_ids", []
                )
            ),
            "selected_structure_residue_support_shortfall_entry_ids": (
                selected_shortfall_ids
            ),
            "single_structure_no_alternate_context_entry_ids": no_alternate_ids,
            "alternate_structures_lack_explicit_residue_positions_entry_ids": (
                alternate_lacks_positions_ids
            ),
            "countable_label_candidate_count": countable_candidate_count,
            "all_audited_rows_non_countable": all_audited_rows_non_countable,
            "audit_ready": audit_ready,
            "repair_ready_for_count_growth": False,
            "review_only_rule": (
                "priority expert-label local-evidence gaps are non-countable "
                "repair lanes until explicit local mechanistic evidence and "
                "external review resolution clear the factory gates"
            ),
        },
        "rows": rows,
    }


def build_expert_label_decision_local_evidence_review_export(
    local_evidence_gap_audit: dict[str, Any],
    labels: list[MechanismLabel],
) -> dict[str, Any]:
    """Build a review-only export for priority local-evidence gap lanes."""
    labels_by_entry = {label.entry_id: label for label in labels}
    source_meta = local_evidence_gap_audit.get("metadata", {})
    rows = [
        row
        for row in local_evidence_gap_audit.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    ]
    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))

    review_items: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        entry_id = str(row["entry_id"])
        label = labels_by_entry.get(entry_id)
        recommended_action = str(row.get("recommended_next_action") or "")
        if recommended_action == "route_to_reaction_substrate_expert_review":
            review_question = (
                "Does reaction or substrate evidence support the current family, "
                "an existing alternate fingerprint, or a new ontology family?"
            )
        elif recommended_action == "route_to_family_boundary_expert_review":
            review_question = (
                "Does the counterevidence cross a mechanism-family boundary, or "
                "can the row stay as review-only support for the current family?"
            )
        elif recommended_action == "inspect_active_site_mapping_or_structure_selection":
            review_question = (
                "Does local active-site mapping or structure selection explain the "
                "structure-wide/nonlocal evidence gap?"
            )
        elif recommended_action == "source_explicit_alternate_structure_residue_positions":
            review_question = (
                "Can explicit alternate-structure catalytic residue positions be "
                "sourced before any local-evidence claim is made?"
            )
        elif recommended_action == "source_external_cofactor_or_structure_evidence":
            review_question = (
                "Is there external cofactor, structure, or active-site evidence "
                "that can resolve this single-structure gap?"
            )
        else:
            review_question = (
                "What local mechanistic evidence is required before this row can "
                "leave review-only repair debt?"
            )
        review_items.append(
            {
                "rank": index,
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "current_label": label.to_dict() if label else None,
                "local_evidence_gap_context": row,
                "review_question": review_question,
                "decision": {
                    "action": "no_decision",
                    "label_type": label.label_type if label else None,
                    "fingerprint_id": label.fingerprint_id if label else row.get(
                        "top1_fingerprint_id"
                    ),
                    "tier": label.tier if label else "bronze",
                    "confidence": "medium",
                    "reviewer": None,
                    "rationale": None,
                    "evidence_score": None,
                    "review_status": "expert_reviewed",
                    "local_evidence_resolution": "needs_more_evidence",
                },
            }
        )

    gap_class_counts = Counter(
        gap_class
        for row in rows
        for gap_class in row.get("local_evidence_gap_classes", [])
    )
    action_counts = Counter(str(row.get("recommended_next_action")) for row in rows)
    exported_entry_ids = _sorted_entry_ids(
        item.get("entry_id") for item in review_items
    )
    return {
        "metadata": {
            "method": "expert_label_decision_local_evidence_review_export",
            "source_method": source_meta.get("method"),
            "exported_count": len(review_items),
            "exported_entry_ids": exported_entry_ids,
            "source_audited_entry_count": source_meta.get("audited_entry_count"),
            "all_source_rows_exported": len(review_items)
            == int(source_meta.get("audited_entry_count", len(review_items)) or 0),
            "local_evidence_gap_class_counts": dict(
                sorted(gap_class_counts.items())
            ),
            "recommended_action_counts": dict(sorted(action_counts.items())),
            "countable_label_candidate_count": 0,
            "decision_counts": {"no_decision": len(review_items)}
            if review_items
            else {},
            "export_ready": bool(source_meta.get("audit_ready", True))
            and len(review_items)
            == int(source_meta.get("audited_entry_count", len(review_items)) or 0),
            "decision_schema": {
                "action": [
                    "accept_label",
                    "mark_needs_more_evidence",
                    "reject_label",
                    "no_decision",
                ],
                "local_evidence_resolution": [
                    "confirms_local_mechanistic_evidence",
                    "requires_alternate_structure_mapping",
                    "requires_family_boundary_review",
                    "requires_reaction_substrate_review",
                    "needs_more_evidence",
                ],
                "review_status": [
                    "expert_reviewed",
                    "needs_expert_review",
                ],
            },
            "review_only_rule": (
                "local-evidence gap exports are expert-review context only; "
                "automation keeps all rows as no_decision and cannot count them "
                "without explicit local evidence, review resolution, and factory "
                "gate acceptance"
            ),
        },
        "review_items": review_items,
    }


def summarize_expert_label_decision_local_evidence_repair_plan(
    local_evidence_gap_audit: dict[str, Any],
    *,
    local_evidence_review_export: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prioritize non-countable repair lanes from the local-evidence gap audit."""
    audit_meta = local_evidence_gap_audit.get("metadata", {})
    export_meta = (local_evidence_review_export or {}).get("metadata", {})
    export_present = (
        export_meta.get("method")
        == "expert_label_decision_local_evidence_review_export"
    )
    exported_entry_ids = set(_sorted_entry_ids(export_meta.get("exported_entry_ids", [])))

    rows: list[dict[str, Any]] = []
    for row in local_evidence_gap_audit.get("rows", []):
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        entry_id = str(row["entry_id"])
        gap_classes = set(_sorted_strings(row.get("local_evidence_gap_classes", [])))
        recommended_action = str(row.get("recommended_next_action") or "")
        if recommended_action == "route_to_reaction_substrate_expert_review":
            repair_lane = "expert_reaction_substrate_review"
            repair_priority = 0
        elif recommended_action == "source_explicit_alternate_structure_residue_positions":
            repair_lane = "source_explicit_alternate_structure_residue_positions"
            repair_priority = 1
        elif recommended_action == "inspect_active_site_mapping_or_structure_selection":
            repair_lane = "inspect_active_site_mapping_or_structure_selection"
            repair_priority = 2
        elif recommended_action == "source_external_cofactor_or_structure_evidence":
            repair_lane = "source_external_cofactor_or_structure_evidence"
            repair_priority = 3
        elif recommended_action == "route_to_family_boundary_expert_review":
            repair_lane = "expert_family_boundary_review"
            repair_priority = 4
        elif recommended_action == "keep_local_evidence_review_only_until_expert_resolution":
            repair_lane = "keep_local_evidence_review_only_until_expert_resolution"
            repair_priority = 5
        else:
            repair_lane = "collect_local_mechanistic_evidence_before_count_growth"
            repair_priority = 6

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "repair_lane": repair_lane,
                "repair_priority": repair_priority,
                "recommended_next_action": recommended_action,
                "local_evidence_gap_classes": sorted(gap_classes),
                "review_exported": entry_id in exported_entry_ids
                if export_present
                else None,
                "countable_label_candidate": False,
                "selected_pdb_id": row.get("selected_pdb_id"),
                "selected_pdb_residue_position_count": row.get(
                    "selected_pdb_residue_position_count"
                ),
                "candidate_pdb_structure_count": row.get(
                    "candidate_pdb_structure_count"
                ),
                "alternate_pdb_count": row.get("alternate_pdb_count"),
                "alternate_pdb_with_residue_positions_count": row.get(
                    "alternate_pdb_with_residue_positions_count"
                ),
                "local_expected_family_hit_count": row.get(
                    "local_expected_family_hit_count"
                ),
                "structure_wide_expected_family_hit_count": row.get(
                    "structure_wide_expected_family_hit_count"
                ),
                "non_countable_blockers": _sorted_strings(
                    row.get("non_countable_blockers", [])
                ),
                "repair_policy": (
                    "repair lanes are work planning only; no row becomes countable "
                    "without local mechanistic evidence, external review resolution, "
                    "and a passing label-factory gate"
                ),
            }
        )

    rows = sorted(
        rows,
        key=lambda row: (
            int(
                row.get("repair_priority")
                if row.get("repair_priority") is not None
                else 99
            ),
            _entry_id_sort_key(str(row.get("entry_id"))),
        ),
    )
    lane_counts = Counter(str(row.get("repair_lane")) for row in rows)
    entry_ids_by_lane = {
        lane: _sorted_entry_ids(
            row.get("entry_id") for row in rows if row.get("repair_lane") == lane
        )
        for lane in sorted(lane_counts)
    }
    review_export_missing_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if export_present and not row.get("review_exported")
    )
    return {
        "metadata": {
            "method": "expert_label_decision_local_evidence_repair_plan",
            "source_audit_method": audit_meta.get("method"),
            "source_review_export_method": export_meta.get("method"),
            "repair_lane_count": len(lane_counts),
            "repair_lane_counts": dict(sorted(lane_counts.items())),
            "entry_ids_by_repair_lane": entry_ids_by_lane,
            "planned_entry_count": len(rows),
            "review_export_present": export_present,
            "review_export_ready": export_meta.get("export_ready"),
            "review_export_missing_entry_ids": review_export_missing_ids,
            "all_planned_rows_review_exported": (
                not export_present or not review_export_missing_ids
            ),
            "single_structure_no_alternate_context_entry_ids": _sorted_entry_ids(
                audit_meta.get("single_structure_no_alternate_context_entry_ids", [])
            ),
            "alternate_structures_lack_explicit_residue_positions_entry_ids": (
                _sorted_entry_ids(
                    audit_meta.get(
                        "alternate_structures_lack_explicit_residue_positions_entry_ids",
                        [],
                    )
                )
            ),
            "countable_label_candidate_count": 0,
            "repair_plan_ready": bool(audit_meta.get("audit_ready", True))
            and (not export_present or not review_export_missing_ids),
            "review_only_rule": (
                "the plan prioritizes evidence repair and expert review; it does "
                "not authorize count growth"
            ),
        },
        "rows": rows,
    }


def resolve_expert_label_decision_local_evidence_repair_lanes(
    local_evidence_repair_plan: dict[str, Any],
    *,
    local_evidence_gap_audit: dict[str, Any] | None = None,
    local_evidence_review_export: dict[str, Any] | None = None,
    reaction_substrate_mismatch_review_export: dict[str, Any] | None = None,
    reaction_substrate_mismatch_decision_batch: dict[str, Any] | None = None,
    entry_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Resolve local-evidence repair lanes that have external review decisions."""
    plan_meta = local_evidence_repair_plan.get("metadata", {})
    gap_meta = (local_evidence_gap_audit or {}).get("metadata", {})
    local_export_meta = (local_evidence_review_export or {}).get("metadata", {})
    mismatch_export_meta = (
        reaction_substrate_mismatch_review_export or {}
    ).get("metadata", {})
    mismatch_batch_meta = (
        reaction_substrate_mismatch_decision_batch or {}
    ).get("metadata", {})

    plan_rows = [
        row
        for row in local_evidence_repair_plan.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    ]
    target_entry_ids = set(_sorted_entry_ids(entry_ids or []))
    if not target_entry_ids:
        target_entry_ids = {
            str(row["entry_id"])
            for row in plan_rows
            if isinstance(row.get("entry_id"), str)
        }

    gap_by_entry = {
        str(row.get("entry_id")): row
        for row in (local_evidence_gap_audit or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    local_export_by_entry = {
        str(item.get("entry_id")): item
        for item in (local_evidence_review_export or {}).get("review_items", [])
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    }
    mismatch_export_entry_ids = set(
        _sorted_entry_ids(mismatch_export_meta.get("exported_entry_ids", []))
    )
    if reaction_substrate_mismatch_review_export and not mismatch_export_entry_ids:
        mismatch_export_entry_ids = set(
            _sorted_entry_ids(
                item.get("entry_id")
                for item in reaction_substrate_mismatch_review_export.get(
                    "review_items", []
                )
                if isinstance(item, dict)
            )
        )
    mismatch_decision_by_entry = {
        str(item.get("entry_id")): item
        for item in (reaction_substrate_mismatch_decision_batch or {}).get(
            "review_items", []
        )
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    target_missing_ids = set(target_entry_ids)
    for row in sorted(plan_rows, key=lambda item: _entry_id_sort_key(str(item["entry_id"]))):
        entry_id = str(row["entry_id"])
        target_missing_ids.discard(entry_id)
        gap_row = gap_by_entry.get(entry_id, {})
        local_export_item = local_export_by_entry.get(entry_id, {})
        local_export_decision = (
            local_export_item.get("decision", {})
            if isinstance(local_export_item.get("decision"), dict)
            else {}
        )
        mismatch_decision_item = mismatch_decision_by_entry.get(entry_id, {})
        mismatch_decision = (
            mismatch_decision_item.get("decision", {})
            if isinstance(mismatch_decision_item.get("decision"), dict)
            else {}
        )
        gap_classes = set(
            _sorted_strings(
                row.get("local_evidence_gap_classes", [])
                or gap_row.get("local_evidence_gap_classes", [])
            )
        )
        repair_lane = str(row.get("repair_lane") or "")
        recommended_action = str(row.get("recommended_next_action") or "")
        is_reaction_lane = (
            repair_lane == "expert_reaction_substrate_review"
            or recommended_action == "route_to_reaction_substrate_expert_review"
            or "reaction_substrate_mismatch_review_required" in gap_classes
        )
        decision_action = str(mismatch_decision.get("action") or "no_decision")
        reaction_resolution = str(
            mismatch_decision.get("reaction_substrate_resolution") or "needs_more_evidence"
        )
        review_status = str(mismatch_decision.get("review_status") or "")
        reviewer = mismatch_decision.get("reviewer")
        expert_resolved = (
            decision_action in {"accept_label", "reject_label", "mark_needs_more_evidence"}
            and review_status == "expert_reviewed"
            and bool(reviewer)
            and reaction_resolution != "needs_more_evidence"
        )
        exported_to_reaction_review = entry_id in mismatch_export_entry_ids
        targeted = entry_id in target_entry_ids

        unresolved_reasons: set[str] = set()
        resolution_status = "not_targeted"
        lane_status = "not_targeted"
        if targeted and is_reaction_lane and exported_to_reaction_review and expert_resolved:
            label_type = mismatch_decision.get("label_type")
            if (
                decision_action == "accept_label"
                and label_type == "out_of_scope"
                and reaction_resolution == "confirm_current_label_or_out_of_scope"
            ):
                resolution_status = "resolved_to_reviewed_out_of_scope"
            elif decision_action == "reject_label":
                resolution_status = "resolved_to_reviewed_rejection"
            else:
                resolution_status = "resolved_to_reviewed_reaction_substrate_decision"
            lane_status = "closed_by_reaction_substrate_review"
        elif targeted:
            resolution_status = "unresolved"
            lane_status = "open"
            if not is_reaction_lane:
                unresolved_reasons.add("repair_lane_not_reaction_substrate_review")
            if is_reaction_lane and not exported_to_reaction_review:
                unresolved_reasons.add("missing_reaction_substrate_review_export")
            if is_reaction_lane and exported_to_reaction_review and not expert_resolved:
                unresolved_reasons.add("missing_external_reaction_substrate_resolution")
            if not unresolved_reasons:
                unresolved_reasons.add("local_evidence_repair_still_open")

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "targeted": targeted,
                "repair_lane": repair_lane,
                "repair_priority": row.get("repair_priority"),
                "recommended_next_action": recommended_action,
                "resolution_status": resolution_status,
                "local_evidence_repair_lane_status": lane_status,
                "countable_label_candidate": False,
                "local_evidence_gap_classes": sorted(gap_classes),
                "non_countable_blockers": _sorted_strings(
                    row.get("non_countable_blockers", [])
                    or gap_row.get("non_countable_blockers", [])
                ),
                "unresolved_reasons": sorted(unresolved_reasons),
                "selected_pdb_id": row.get("selected_pdb_id")
                or gap_row.get("selected_pdb_id"),
                "selected_pdb_residue_position_count": row.get(
                    "selected_pdb_residue_position_count"
                )
                if row.get("selected_pdb_residue_position_count") is not None
                else gap_row.get("selected_pdb_residue_position_count"),
                "candidate_pdb_structure_count": row.get(
                    "candidate_pdb_structure_count"
                )
                if row.get("candidate_pdb_structure_count") is not None
                else gap_row.get("candidate_pdb_structure_count"),
                "alternate_pdb_count": row.get("alternate_pdb_count")
                if row.get("alternate_pdb_count") is not None
                else gap_row.get("alternate_pdb_count"),
                "alternate_pdb_with_residue_positions_count": row.get(
                    "alternate_pdb_with_residue_positions_count"
                )
                if row.get("alternate_pdb_with_residue_positions_count") is not None
                else gap_row.get("alternate_pdb_with_residue_positions_count"),
                "local_expected_family_hit_count": row.get(
                    "local_expected_family_hit_count"
                )
                if row.get("local_expected_family_hit_count") is not None
                else gap_row.get("local_expected_family_hit_count"),
                "reaction_substrate_mismatch_exported": exported_to_reaction_review,
                "reaction_substrate_decision": {
                    "action": decision_action,
                    "label_type": mismatch_decision.get("label_type"),
                    "fingerprint_id": mismatch_decision.get("fingerprint_id"),
                    "review_status": review_status or None,
                    "reviewer": reviewer,
                    "reaction_substrate_resolution": reaction_resolution,
                    "future_fingerprint_family_hint": mismatch_decision.get(
                        "future_fingerprint_family_hint"
                    ),
                    "expert_review_timestamp_utc": mismatch_decision.get(
                        "expert_review_timestamp_utc"
                    ),
                    "rationale": mismatch_decision.get("rationale"),
                },
                "local_evidence_review_export_decision": {
                    "action": local_export_decision.get("action"),
                    "local_evidence_resolution": local_export_decision.get(
                        "local_evidence_resolution"
                    ),
                    "reviewer": local_export_decision.get("reviewer"),
                }
                if local_export_decision
                else None,
                "resolution_policy": (
                    "external reaction/substrate review can close the local-evidence "
                    "repair lane as review-only debt, but this artifact never "
                    "promotes labels or makes rows countable"
                ),
            }
        )

    resolved_rows = [
        row
        for row in rows
        if row.get("targeted")
        and str(row.get("resolution_status", "")).startswith("resolved_")
    ]
    unresolved_rows = [
        row
        for row in rows
        if row.get("targeted") and row.get("resolution_status") == "unresolved"
    ]
    remaining_open_rows = [
        row
        for row in rows
        if row.get("local_evidence_repair_lane_status") != "closed_by_reaction_substrate_review"
    ]
    resolution_counts = Counter(str(row.get("resolution_status")) for row in rows)
    resolved_lane_counts = Counter(str(row.get("repair_lane")) for row in resolved_rows)
    remaining_lane_counts = Counter(str(row.get("repair_lane")) for row in remaining_open_rows)
    decision_action_counts = Counter(
        str(row.get("reaction_substrate_decision", {}).get("action"))
        for row in resolved_rows
    )
    label_type_counts = Counter(
        str(row.get("reaction_substrate_decision", {}).get("label_type"))
        for row in resolved_rows
    )
    unresolved_reason_counts = Counter(
        reason for row in unresolved_rows for reason in row.get("unresolved_reasons", [])
    )
    resolved_entry_ids = _sorted_entry_ids(row.get("entry_id") for row in resolved_rows)
    unresolved_entry_ids = _sorted_entry_ids(
        row.get("entry_id") for row in unresolved_rows
    )
    remaining_open_entry_ids = _sorted_entry_ids(
        row.get("entry_id") for row in remaining_open_rows
    )
    target_entry_id_list = _sorted_entry_ids(target_entry_ids)
    return {
        "metadata": {
            "method": "expert_label_decision_local_evidence_repair_resolution",
            "source_plan_method": plan_meta.get("method"),
            "source_gap_audit_method": gap_meta.get("method"),
            "source_local_evidence_review_export_method": local_export_meta.get(
                "method"
            ),
            "source_reaction_substrate_mismatch_review_export_method": (
                mismatch_export_meta.get("method")
            ),
            "source_reaction_substrate_mismatch_decision_batch_method": (
                mismatch_batch_meta.get("method")
            ),
            "planned_entry_count": len(plan_rows),
            "target_entry_count": len(target_entry_id_list),
            "target_entry_ids": target_entry_id_list,
            "target_missing_entry_ids": _sorted_entry_ids(target_missing_ids),
            "resolved_entry_count": len(resolved_rows),
            "resolved_entry_ids": resolved_entry_ids,
            "unresolved_entry_count": len(unresolved_rows),
            "unresolved_entry_ids": unresolved_entry_ids,
            "remaining_open_entry_count": len(remaining_open_rows),
            "remaining_open_entry_ids": remaining_open_entry_ids,
            "resolution_status_counts": dict(sorted(resolution_counts.items())),
            "resolved_repair_lane_counts": dict(sorted(resolved_lane_counts.items())),
            "remaining_repair_lane_counts": dict(sorted(remaining_lane_counts.items())),
            "resolved_decision_action_counts": dict(sorted(decision_action_counts.items())),
            "resolved_label_type_counts": dict(sorted(label_type_counts.items())),
            "unresolved_reason_counts": dict(sorted(unresolved_reason_counts.items())),
            "reaction_substrate_review_resolved_entry_ids": resolved_entry_ids,
            "all_resolved_rows_non_countable": all(
                row.get("countable_label_candidate") is False for row in resolved_rows
            ),
            "countable_label_candidate_count": 0,
            "resolution_ready": (
                plan_meta.get("method")
                == "expert_label_decision_local_evidence_repair_plan"
                and not target_missing_ids
                and bool(resolved_rows)
                and all(
                    row.get("countable_label_candidate") is False
                    for row in resolved_rows
                )
            ),
            "review_only_rule": (
                "resolved repair lanes stay non-countable until a separate "
                "countable import, local-evidence check, and label-factory gate "
                "explicitly accept them"
            ),
        },
        "rows": rows,
    }


def build_explicit_alternate_residue_position_requests(
    local_evidence_repair_plan: dict[str, Any],
    *,
    review_debt_remediation: dict[str, Any] | None = None,
    graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build review-only sourcing requests for alternate-PDB residue positions."""
    plan_meta = local_evidence_repair_plan.get("metadata", {})
    remediation_meta = (review_debt_remediation or {}).get("metadata", {})
    remediation_by_entry = {
        str(row.get("entry_id")): row
        for row in (review_debt_remediation or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    graph_nodes = {
        str(node.get("id")): node
        for node in (graph or {}).get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    ec_ids_by_entry: dict[str, list[str]] = defaultdict(list)
    reference_uniprot_by_entry: dict[str, str] = {}
    for edge in (graph or {}).get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = edge.get("source")
        target = edge.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if target.startswith("ec:"):
            ec_ids_by_entry[source].append(target)
        elif target.startswith("uniprot:"):
            reference_uniprot_by_entry[source] = target.removeprefix("uniprot:")

    rows: list[dict[str, Any]] = []
    for plan_row in local_evidence_repair_plan.get("rows", []):
        if not isinstance(plan_row, dict) or not isinstance(
            plan_row.get("entry_id"), str
        ):
            continue
        if (
            plan_row.get("repair_lane")
            != "source_explicit_alternate_structure_residue_positions"
        ):
            continue
        entry_id = str(plan_row["entry_id"])
        remediation_row = remediation_by_entry.get(entry_id, {})
        graph_node = graph_nodes.get(entry_id, {})
        candidate_ids = _sorted_strings(
            remediation_row.get("candidate_pdb_structure_ids", [])
            or plan_row.get("candidate_pdb_structure_ids", [])
        )
        selected_pdb_id = (
            plan_row.get("selected_pdb_id")
            or remediation_row.get("selected_pdb_id")
            or remediation_row.get("selected_structure_id")
        )
        alternate_ids = _sorted_strings(
            remediation_row.get("alternate_pdb_ids", [])
            or [
                pdb_id
                for pdb_id in candidate_ids
                if selected_pdb_id is None or pdb_id != selected_pdb_id
            ]
        )
        selected_position_count = plan_row.get("selected_pdb_residue_position_count")
        if selected_position_count is None:
            selected_position_count = remediation_row.get(
                "selected_pdb_residue_position_count"
            )
        alternate_with_positions = plan_row.get(
            "alternate_pdb_with_residue_positions_count"
        )
        if alternate_with_positions is None:
            alternate_with_positions = remediation_row.get(
                "alternate_pdb_with_residue_positions_count"
            )
        request_reasons = {
            "alternate_structures_lack_explicit_residue_positions",
            "external_expert_decision_required",
        }
        if int(selected_position_count or 0) < 3:
            request_reasons.add("selected_structure_residue_support_shortfall")
        if remediation_row.get("gap_reasons"):
            request_reasons.update(_sorted_strings(remediation_row.get("gap_reasons", [])))

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": plan_row.get("entry_name")
                or remediation_row.get("entry_name")
                or graph_node.get("name"),
                "repair_lane": plan_row.get("repair_lane"),
                "recommended_next_action": plan_row.get("recommended_next_action"),
                "request_status": "awaiting_explicit_alternate_structure_residue_positions",
                "countable_label_candidate": False,
                "selected_pdb_id": selected_pdb_id,
                "selected_pdb_residue_position_count": selected_position_count,
                "candidate_pdb_structure_ids": candidate_ids,
                "candidate_pdb_structure_count": len(candidate_ids)
                if candidate_ids
                else plan_row.get("candidate_pdb_structure_count"),
                "alternate_pdb_ids": alternate_ids,
                "alternate_pdb_count": len(alternate_ids)
                if alternate_ids
                else plan_row.get("alternate_pdb_count"),
                "alternate_pdb_with_residue_positions_count": int(
                    alternate_with_positions or 0
                ),
                "reference_uniprot_id": reference_uniprot_by_entry.get(entry_id)
                or graph_node.get("reference_uniprot_id"),
                "ec_ids": sorted(set(ec_ids_by_entry.get(entry_id, []))),
                "expected_cofactor_families": _sorted_strings(
                    remediation_row.get("expected_cofactor_families", [])
                ),
                "local_cofactor_families": _sorted_strings(
                    remediation_row.get("local_cofactor_families", [])
                ),
                "structure_cofactor_families": _sorted_strings(
                    remediation_row.get("structure_cofactor_families", [])
                ),
                "request_reasons": sorted(request_reasons),
                "required_evidence_fields": [
                    "alternate_pdb_id",
                    "chain_id",
                    "residue_number_or_auth_seq_id",
                    "residue_code",
                    "mapping_basis",
                    "source_reference",
                ],
                "non_countable_blockers": _sorted_strings(
                    plan_row.get("non_countable_blockers", [])
                ),
                "sourcing_policy": (
                    "explicit alternate-structure residue positions are sourcing "
                    "requests only; they do not count as local mechanistic evidence "
                    "until reviewed and passed through the label factory"
                ),
            }
        )

    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))
    alternate_structure_count = sum(
        int(row.get("alternate_pdb_count", 0) or 0) for row in rows
    )
    request_reason_counts = Counter(
        reason for row in rows for reason in row.get("request_reasons", [])
    )
    return {
        "metadata": {
            "method": "explicit_alternate_residue_position_sourcing_requests",
            "source_plan_method": plan_meta.get("method"),
            "source_remediation_method": remediation_meta.get("method"),
            "request_count": len(rows),
            "request_entry_ids": _sorted_entry_ids(row.get("entry_id") for row in rows),
            "candidate_alternate_structure_count": alternate_structure_count,
            "alternate_pdb_with_residue_positions_count": sum(
                int(row.get("alternate_pdb_with_residue_positions_count", 0) or 0)
                for row in rows
            ),
            "request_reason_counts": dict(sorted(request_reason_counts.items())),
            "countable_label_candidate_count": 0,
            "sourcing_request_ready": bool(rows),
            "review_only_rule": (
                "alternate residue-position sourcing requests are non-countable "
                "until explicit evidence is supplied, reviewed, and accepted by "
                "the label factory"
            ),
        },
        "rows": rows,
    }


def audit_accepted_review_debt_deferrals(
    review_debt: dict[str, Any],
    acceptance: dict[str, Any],
    *,
    scaling_quality_audit: dict[str, Any] | None = None,
    local_evidence_gap_audit: dict[str, Any] | None = None,
    local_evidence_review_export: dict[str, Any] | None = None,
    local_evidence_repair_plan: dict[str, Any] | None = None,
    local_evidence_repair_resolution: dict[str, Any] | None = None,
    explicit_alternate_residue_position_requests: dict[str, Any] | None = None,
    remap_local_lead_audit: dict[str, Any] | None = None,
    review_only_import_safety_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Confirm accepted-batch review-debt rows are explicitly non-countable."""
    review_debt_meta = review_debt.get("metadata", {})
    acceptance_meta = acceptance.get("metadata", {})
    scaling_meta = (scaling_quality_audit or {}).get("metadata", {})
    local_gap_meta = (local_evidence_gap_audit or {}).get("metadata", {})
    local_export_meta = (local_evidence_review_export or {}).get("metadata", {})
    plan_meta = (local_evidence_repair_plan or {}).get("metadata", {})
    resolution_meta = (local_evidence_repair_resolution or {}).get("metadata", {})
    alternate_meta = (
        explicit_alternate_residue_position_requests or {}
    ).get("metadata", {})
    remap_meta = (remap_local_lead_audit or {}).get("metadata", {})
    import_safety_meta = (review_only_import_safety_audit or {}).get("metadata", {})

    accepted_entry_ids = _sorted_entry_ids(
        acceptance_meta.get("accepted_new_label_entry_ids", [])
    )
    review_debt_entry_ids = _sorted_entry_ids(
        review_debt_meta.get("review_debt_entry_ids", [])
    )
    if not review_debt_entry_ids:
        review_debt_entry_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in review_debt.get("rows", [])
            if isinstance(row, dict)
        )
    review_debt_id_set = set(review_debt_entry_ids)
    accepted_review_debt_overlap_ids = _sorted_entry_ids(
        set(accepted_entry_ids) & review_debt_id_set
    )

    local_gap_entry_ids = _sorted_entry_ids(
        local_gap_meta.get("audited_entry_ids", [])
    )
    if local_evidence_gap_audit and not local_gap_entry_ids:
        local_gap_entry_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in local_evidence_gap_audit.get("rows", [])
            if isinstance(row, dict)
        )
    local_export_entry_ids = _sorted_entry_ids(
        local_export_meta.get("exported_entry_ids", [])
    )
    if local_evidence_review_export and not local_export_entry_ids:
        local_export_entry_ids = _sorted_entry_ids(
            item.get("entry_id")
            for item in local_evidence_review_export.get("review_items", [])
            if isinstance(item, dict)
        )
    plan_entry_ids = _sorted_entry_ids(plan_meta.get("planned_entry_ids", []))
    if local_evidence_repair_plan and not plan_entry_ids:
        plan_entry_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in local_evidence_repair_plan.get("rows", [])
            if isinstance(row, dict)
        )
    resolved_entry_ids = _sorted_entry_ids(
        resolution_meta.get("resolved_entry_ids", [])
    )
    resolution_target_entry_ids = _sorted_entry_ids(
        resolution_meta.get("target_entry_ids", [])
    )
    alternate_request_entry_ids = _sorted_entry_ids(
        alternate_meta.get("request_entry_ids", [])
    )
    remap_strict_entry_ids = _sorted_entry_ids(
        remap_meta.get("strict_remap_guardrail_entry_ids", [])
    )
    remap_family_review_entry_ids = _sorted_entry_ids(
        remap_meta.get("expert_family_boundary_review_entry_ids", [])
    )
    remap_reaction_review_entry_ids = _sorted_entry_ids(
        remap_meta.get("expert_reaction_substrate_review_entry_ids", [])
    )
    structure_wide_without_local_ids = _sorted_entry_ids(
        scaling_meta.get(
            "alternate_structure_scan_structure_wide_hit_without_local_support_entry_ids",
            [],
        )
    )
    local_hit_from_remap_ids = _sorted_entry_ids(
        scaling_meta.get(
            "alternate_structure_scan_local_expected_family_hit_from_remap_entry_ids",
            [],
        )
    )
    unclassified_new_debt_ids = _sorted_entry_ids(
        scaling_meta.get("unclassified_new_review_debt_entry_ids", [])
    )

    local_gap_set = set(local_gap_entry_ids)
    local_export_set = set(local_export_entry_ids)
    plan_set = set(plan_entry_ids)
    resolved_set = set(resolved_entry_ids)
    resolution_target_set = set(resolution_target_entry_ids)
    alternate_request_set = set(alternate_request_entry_ids)
    remap_strict_set = set(remap_strict_entry_ids)
    structure_wide_without_local_set = set(structure_wide_without_local_ids)
    local_hit_from_remap_set = set(local_hit_from_remap_ids)

    plan_by_entry = {
        str(row.get("entry_id")): row
        for row in (local_evidence_repair_plan or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    review_debt_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in review_debt.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    for entry_id in review_debt_entry_ids:
        if entry_id not in review_debt_rows_by_entry:
            review_debt_rows_by_entry[entry_id] = {
                "entry_id": entry_id,
                "debt_status": (
                    "new"
                    if entry_id
                    in set(review_debt_meta.get("new_review_debt_entry_ids", []))
                    else "carried"
                ),
                "recommended_next_action": "review_debt_metadata_only_defer",
                "gap_reasons": ["review_debt_summary_row_table_capped"],
            }

    rows: list[dict[str, Any]] = []
    for debt_row in sorted(
        review_debt_rows_by_entry.values(),
        key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))),
    ):
        entry_id = str(debt_row["entry_id"])
        plan_row = plan_by_entry.get(entry_id, {})
        deferral_actions: set[str] = set()
        if entry_id in local_gap_set:
            deferral_actions.add("priority_local_evidence_gap_audited")
        if entry_id in local_export_set:
            deferral_actions.add("local_evidence_review_export_no_decision")
        if entry_id in plan_set:
            repair_lane = str(plan_row.get("repair_lane") or "unclassified")
            deferral_actions.add(f"repair_lane:{repair_lane}")
        if entry_id in resolved_set:
            deferral_actions.add("local_evidence_repair_lane_closed_review_only")
        elif entry_id in resolution_target_set:
            deferral_actions.add("local_evidence_repair_lane_still_deferred")
        if entry_id in alternate_request_set:
            deferral_actions.add("explicit_alternate_residue_position_request")
        if entry_id in remap_strict_set:
            deferral_actions.add("strict_remap_guardrail_deferred")
        if entry_id in structure_wide_without_local_set:
            deferral_actions.add("structure_wide_hit_without_local_support_deferred")
        if entry_id in local_hit_from_remap_set:
            deferral_actions.add("conservative_remap_local_hit_requires_review")
        if not deferral_actions:
            action = str(debt_row.get("recommended_next_action") or "review_debt")
            deferral_actions.add(f"review_debt_deferred:{action}")

        if entry_id in accepted_review_debt_overlap_ids:
            deferral_status = "invalid_accepted_label_overlap"
        elif entry_id in resolved_set:
            deferral_status = "closed_non_countable_review_resolution"
        elif entry_id in remap_strict_set:
            deferral_status = "deferred_strict_remap_family_boundary_review"
        elif entry_id in alternate_request_set:
            deferral_status = "deferred_explicit_alternate_residue_positions"
        elif entry_id in local_gap_set:
            deferral_status = "deferred_priority_local_evidence_review"
        elif entry_id in structure_wide_without_local_set:
            deferral_status = "deferred_structure_wide_only_evidence"
        else:
            deferral_status = "deferred_review_debt"

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": debt_row.get("entry_name"),
                "debt_status": debt_row.get("debt_status"),
                "recommended_next_action": debt_row.get("recommended_next_action"),
                "decision_action": debt_row.get("decision_action"),
                "target_fingerprint_id": debt_row.get("target_fingerprint_id"),
                "top1_fingerprint_id": debt_row.get("top1_fingerprint_id"),
                "coverage_status": debt_row.get("coverage_status"),
                "gap_reasons": _sorted_strings(debt_row.get("gap_reasons", [])),
                "countable_label_candidate": False,
                "accepted_clean_label_overlap": (
                    entry_id in accepted_review_debt_overlap_ids
                ),
                "deferral_status": deferral_status,
                "deferral_actions": sorted(deferral_actions),
                "repair_lane": plan_row.get("repair_lane"),
                "non_countable_blockers": _sorted_strings(
                    [
                        "review_state_needs_more_evidence",
                        "not_in_countable_label_registry",
                        *debt_row.get("gap_reasons", []),
                        *plan_row.get("non_countable_blockers", []),
                    ]
                ),
                "deferral_policy": (
                    "review-debt rows stay non-countable until evidence removes "
                    "their gap reasons and a separate countable import plus label "
                    "factory gate accepts them"
                ),
            }
        )

    missing_review_debt_row_ids = _sorted_entry_ids(
        review_debt_id_set
        - {
            str(row.get("entry_id"))
            for row in rows
            if isinstance(row.get("entry_id"), str)
        }
    )
    deferral_status_counts = Counter(str(row.get("deferral_status")) for row in rows)
    deferral_action_counts = Counter(
        action for row in rows for action in row.get("deferral_actions", [])
    )
    countable_candidate_count = sum(
        1 for row in rows if row.get("countable_label_candidate") is not False
    )
    import_safety_ready = (
        not review_only_import_safety_audit
        or (
            import_safety_meta.get("method") == "review_only_import_safety_audit"
            and bool(import_safety_meta.get("countable_import_safe"))
            and int(import_safety_meta.get("total_new_countable_label_count", 0) or 0)
            == 0
        )
    )
    deferral_ready = (
        review_debt_meta.get("method") == "review_debt_summary"
        and bool(review_debt_entry_ids)
        and not accepted_review_debt_overlap_ids
        and not missing_review_debt_row_ids
        and countable_candidate_count == 0
        and not unclassified_new_debt_ids
        and import_safety_ready
    )
    return {
        "metadata": {
            "method": "accepted_review_debt_deferral_audit",
            "source_review_debt_method": review_debt_meta.get("method"),
            "source_acceptance_method": acceptance_meta.get("method"),
            "source_scaling_quality_method": scaling_meta.get("method"),
            "review_debt_count": len(review_debt_entry_ids),
            "deferred_entry_count": len(rows),
            "deferred_entry_ids": _sorted_entry_ids(
                row.get("entry_id") for row in rows
            ),
            "new_review_debt_count": int(
                review_debt_meta.get("new_review_debt_count", 0) or 0
            ),
            "new_review_debt_entry_ids": _sorted_entry_ids(
                review_debt_meta.get("new_review_debt_entry_ids", [])
            ),
            "accepted_new_label_entry_ids": accepted_entry_ids,
            "accepted_review_debt_overlap_count": len(
                accepted_review_debt_overlap_ids
            ),
            "accepted_review_debt_overlap_entry_ids": (
                accepted_review_debt_overlap_ids
            ),
            "missing_review_debt_row_entry_ids": missing_review_debt_row_ids,
            "metadata_only_review_debt_entry_count": sum(
                1
                for row in rows
                if "review_debt_summary_row_table_capped"
                in row.get("gap_reasons", [])
            ),
            "metadata_only_review_debt_entry_ids": _sorted_entry_ids(
                row.get("entry_id")
                for row in rows
                if "review_debt_summary_row_table_capped"
                in row.get("gap_reasons", [])
            ),
            "unclassified_new_review_debt_entry_ids": unclassified_new_debt_ids,
            "local_evidence_gap_audited_entry_count": len(local_gap_entry_ids),
            "local_evidence_gap_audited_entry_ids": local_gap_entry_ids,
            "local_evidence_review_export_entry_count": len(local_export_entry_ids),
            "local_evidence_review_export_entry_ids": local_export_entry_ids,
            "local_evidence_repair_plan_entry_count": len(plan_entry_ids),
            "local_evidence_repair_plan_entry_ids": plan_entry_ids,
            "local_evidence_repair_resolution_resolved_entry_count": len(
                resolved_entry_ids
            ),
            "local_evidence_repair_resolution_resolved_entry_ids": (
                resolved_entry_ids
            ),
            "explicit_alternate_residue_position_request_count": len(
                alternate_request_entry_ids
            ),
            "explicit_alternate_residue_position_request_entry_ids": (
                alternate_request_entry_ids
            ),
            "strict_remap_guardrail_entry_ids": remap_strict_entry_ids,
            "remap_family_boundary_review_entry_ids": remap_family_review_entry_ids,
            "remap_reaction_substrate_review_entry_ids": (
                remap_reaction_review_entry_ids
            ),
            "structure_wide_hit_without_local_support_entry_ids": (
                structure_wide_without_local_ids
            ),
            "local_expected_family_hit_from_remap_entry_ids": local_hit_from_remap_ids,
            "review_only_import_safety_ready": import_safety_ready,
            "review_only_import_safety_total_new_countable_label_count": int(
                import_safety_meta.get("total_new_countable_label_count", 0) or 0
            ),
            "deferral_status_counts": dict(sorted(deferral_status_counts.items())),
            "deferral_action_counts": dict(sorted(deferral_action_counts.items())),
            "countable_label_candidate_count": countable_candidate_count,
            "deferral_ready": deferral_ready,
            "deferral_rule": (
                "accepted clean labels must not overlap review debt; all review "
                "debt remains non-countable until later evidence and factory "
                "gates explicitly clear it"
            ),
        },
        "rows": rows,
    }


ONTOLOGY_GAP_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "transferase_phosphoryl",
        ("kinase", "phosphoryl", "phosphotransferase", "atp "),
    ),
    ("transferase_methyl", ("methyltransferase", "methyl transfer")),
    ("lyase", (" lyase", "aldolase", "decarboxylase", "dehydratase")),
    ("isomerase", ("isomerase", "mutase", "epimerase", "racemase")),
    (
        "oxidoreductase_long_tail",
        ("dehydrogenase", "reductase", "oxidase", "oxygenase", "catalase"),
    ),
    ("glycan_chemistry", ("glycosylase", "glycosidase", "dextranase")),
)


def audit_mechanism_ontology_gaps(
    active_learning_queue: dict[str, Any],
    *,
    expert_label_decision_repair_candidates: dict[str, Any] | None = None,
    family_propagation_guardrails: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_gap_audit: dict[str, Any] | None = None,
    max_rows: int = 60,
) -> dict[str, Any]:
    """Summarize non-countable mechanism scope pressure beyond current ontology."""
    ontology = load_mechanism_ontology()
    existing_families = sorted(
        str(family.get("id"))
        for family in ontology.get("families", [])
        if isinstance(family, dict) and family.get("id")
    )
    repair_by_entry = {
        str(row.get("entry_id")): row
        for row in (expert_label_decision_repair_candidates or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    family_guardrail_by_entry = {
        str(row.get("entry_id")): row
        for row in (family_propagation_guardrails or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    local_gap_by_entry = {
        str(row.get("entry_id")): row
        for row in (expert_label_decision_local_evidence_gap_audit or {}).get(
            "rows", []
        )
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for queue_row in active_learning_queue.get("rows", []):
        if not isinstance(queue_row, dict) or not isinstance(
            queue_row.get("entry_id"), str
        ):
            continue
        entry_id = str(queue_row["entry_id"])
        repair_row = repair_by_entry.get(entry_id, {})
        family_guardrail_row = family_guardrail_by_entry.get(entry_id, {})
        local_gap_row = local_gap_by_entry.get(entry_id, {})
        text = _ontology_gap_text(queue_row, repair_row)
        scope_signals = _ontology_gap_scope_signals(text)
        if not scope_signals:
            continue
        mismatch_reasons = _sorted_strings(
            queue_row.get("reaction_substrate_mismatch_reasons", [])
        ) or _sorted_strings(
            family_guardrail_row.get("reaction_substrate_mismatch_reasons", [])
        )
        quality_flags = _sorted_strings(repair_row.get("quality_risk_flags", []))
        blockers = {"keyword_only_scope_signal", "external_expert_review_required"}
        if mismatch_reasons:
            blockers.add("reaction_substrate_mismatch_review_required")
        if queue_row.get("recommended_action") == "expert_label_decision_needed":
            blockers.add("expert_label_decision_required")
        if "cofactor_family_ambiguity" in quality_flags:
            blockers.add("cofactor_family_ambiguity")
        if "counterevidence_boundary" in quality_flags:
            blockers.add("counterevidence_boundary")
        if "active_site_mapping_or_structure_gap" in quality_flags:
            blockers.add("active_site_mapping_or_structure_gap")
        if "text_leakage_or_nonlocal_evidence_risk" in quality_flags:
            blockers.add("text_leakage_or_nonlocal_evidence_risk")
        local_gap_classes = _sorted_strings(
            local_gap_row.get("local_evidence_gap_classes", [])
        )
        if local_gap_classes:
            blockers.add("local_evidence_gap_unresolved")

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": queue_row.get("entry_name")
                or repair_row.get("entry_name"),
                "rank": queue_row.get("rank"),
                "scope_signals": scope_signals,
                "top1_fingerprint_id": queue_row.get("top1_fingerprint_id")
                or repair_row.get("top1_fingerprint_id"),
                "top1_ontology_family": queue_row.get("top1_ontology_family")
                or repair_row.get("top1_ontology_family"),
                "recommended_action": queue_row.get("recommended_action"),
                "reaction_substrate_mismatch_reasons": mismatch_reasons,
                "quality_risk_flags": quality_flags,
                "local_evidence_gap_classes": local_gap_classes,
                "local_evidence_gap_recommended_action": local_gap_row.get(
                    "recommended_next_action"
                ),
                "countable_label_candidate": False,
                "ontology_update_blockers": sorted(blockers),
                "recommended_next_action": (
                    "collect local mechanistic evidence and expert-reviewed "
                    "examples before adding or splitting ontology families"
                ),
            }
        )

    signal_counts = Counter(signal for row in rows for signal in row["scope_signals"])
    blocker_counts = Counter(
        blocker for row in rows for blocker in row["ontology_update_blockers"]
    )
    local_gap_class_counts = Counter(
        gap_class for row in rows for gap_class in row["local_evidence_gap_classes"]
    )
    rows = sorted(
        rows,
        key=lambda row: (
            0
            if "reaction_substrate_mismatch_review_required"
            in row["ontology_update_blockers"]
            else 1,
            int(row.get("rank", 0) or 0),
            _entry_id_sort_key(str(row["entry_id"])),
        ),
    )
    priority_local_gap_added_count = 0
    if max_rows <= 0:
        emitted_rows = rows
    else:
        emitted_rows = rows[:max_rows]
        emitted_entry_ids = {str(row.get("entry_id")) for row in emitted_rows}
        priority_local_gap_rows = [
            row
            for row in rows[max_rows:]
            if row.get("local_evidence_gap_classes")
            and str(row.get("entry_id")) not in emitted_entry_ids
        ]
        priority_local_gap_added_count = len(priority_local_gap_rows)
        emitted_rows = [*emitted_rows, *priority_local_gap_rows]
    return {
        "metadata": {
            "method": "mechanism_ontology_gap_audit",
            "existing_ontology_families": existing_families,
            "candidate_scope_signal_count": len(rows),
            "emitted_row_count": len(emitted_rows),
            "omitted_by_max_rows": max(0, len(rows) - len(emitted_rows)),
            "max_rows": max_rows,
            "priority_local_evidence_gap_added_count": (
                priority_local_gap_added_count
            ),
            "scope_signal_counts": dict(sorted(signal_counts.items())),
            "ontology_update_blocker_counts": dict(sorted(blocker_counts.items())),
            "local_evidence_gap_context_source_method": (
                (expert_label_decision_local_evidence_gap_audit or {})
                .get("metadata", {})
                .get("method")
            ),
            "local_evidence_gap_context_entry_count": sum(
                1 for row in rows if row.get("local_evidence_gap_classes")
            ),
            "local_evidence_gap_class_counts": dict(
                sorted(local_gap_class_counts.items())
            ),
            "countable_label_candidate_count": 0,
            "ontology_update_ready": False,
            "review_only_rule": (
                "scope signals from names, text, and review queues are ontology "
                "pressure only; they cannot create countable labels or new "
                "families without local mechanism evidence and expert review"
            ),
            "recommended_path": (
                "prioritize transferase, lyase, isomerase, and long-tail redox "
                "examples for expert-reviewed seed ontology expansion"
            ),
        },
        "rows": emitted_rows,
    }


def _ontology_gap_text(
    queue_row: dict[str, Any],
    repair_row: dict[str, Any],
) -> str:
    snippets = queue_row.get("mechanism_text_snippets", [])
    if not isinstance(snippets, list):
        snippets = []
    values = [
        queue_row.get("entry_name"),
        repair_row.get("entry_name"),
        *snippets,
    ]
    return " ".join(str(value).lower() for value in values if value)


def _ontology_gap_scope_signals(text: str) -> list[str]:
    signals: list[str] = []
    padded = f" {text} "
    for signal, patterns in ONTOLOGY_GAP_PATTERNS:
        if any(pattern in padded for pattern in patterns):
            signals.append(signal)
    return signals


def build_atp_phosphoryl_transfer_family_expansion(
    *,
    reaction_substrate_mismatch_decision_batch: dict[str, Any],
    reaction_substrate_mismatch_review_export: dict[str, Any] | None = None,
    family_propagation_guardrails: dict[str, Any] | None = None,
    active_learning_queue: dict[str, Any] | None = None,
    adversarial_negatives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materialize expert-reviewed ATP/phosphoryl-transfer family boundaries."""
    ontology = load_mechanism_ontology()
    family_records = {
        str(family.get("id")): family
        for family in ontology.get("families", [])
        if isinstance(family, dict) and isinstance(family.get("id"), str)
    }
    target_family_records = [
        _atp_target_family_record(family_id, family_records.get(family_id, {}))
        for family_id in ATP_PHOSPHORYL_TRANSFER_FAMILY_IDS
    ]
    all_required_families_present = all(
        row["present_in_ontology"] for row in target_family_records
    )
    all_required_families_have_scope_notes = all(
        row["has_scope_note"] for row in target_family_records
    )
    all_required_family_relationships_declared = all(
        row["has_parent_or_sibling_relationship"] for row in target_family_records
    )

    export_context_by_entry = _review_export_context_by_entry(
        reaction_substrate_mismatch_review_export
    )
    family_guardrail_by_entry = {
        str(row.get("entry_id")): row
        for row in (family_propagation_guardrails or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    queue_by_entry = {
        str(row.get("entry_id")): row
        for row in (active_learning_queue or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    adversarial_by_entry = {
        str(row.get("entry_id")): row
        for row in (adversarial_negatives or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    non_target_hint_rows: list[dict[str, Any]] = []
    for item in reaction_substrate_mismatch_decision_batch.get("review_items", []):
        if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
            continue
        entry_id = str(item["entry_id"])
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            decision = {}
        context = item.get("mismatch_context", {})
        if not isinstance(context, dict):
            context = {}
        export_context = export_context_by_entry.get(entry_id, {})
        family_guardrail = family_guardrail_by_entry.get(entry_id, {})
        queue_row = queue_by_entry.get(entry_id, {})
        future_hint = decision.get("future_fingerprint_family_hint")
        assignment = _atp_phosphoryl_transfer_family_assignment(
            entry_name=(
                item.get("entry_name")
                or context.get("entry_name")
                or export_context.get("entry_name")
                or queue_row.get("entry_name")
                or family_guardrail.get("entry_name")
                or ""
            ),
            mechanism_text_snippets=(
                context.get("mechanism_text_snippets")
                or export_context.get("mechanism_text_snippets")
                or queue_row.get("mechanism_text_snippets")
                or family_guardrail.get("mechanism_text_snippets")
                or []
            ),
            top1_fingerprint_id=(
                context.get("top1_fingerprint_id")
                or export_context.get("top1_fingerprint_id")
                or queue_row.get("top1_fingerprint_id")
                or family_guardrail.get("top1_fingerprint_id")
            ),
            future_family_hint=future_hint,
            require_mismatch_signal=False,
        )
        if assignment is None:
            if future_hint:
                non_target_hint_rows.append(
                    {
                        "entry_id": entry_id,
                        "entry_name": item.get("entry_name")
                        or context.get("entry_name"),
                        "future_fingerprint_family_hint": future_hint,
                        "decision_action": decision.get("action"),
                        "countable_label_candidate": False,
                        "non_target_rule": (
                            "expert hints outside the nine prioritized families "
                            "are retained as future ontology pressure, not mapped "
                            "or counted in this expansion"
                        ),
                    }
                )
            continue
        family_id = str(assignment["family_id"])
        decision_action = str(decision.get("action") or "no_decision")
        reaction_resolution = str(
            decision.get("reaction_substrate_resolution") or "needs_more_evidence"
        )
        expert_supported = (
            decision.get("review_status") == "expert_reviewed"
            and reaction_resolution != "needs_more_evidence"
            and bool(decision.get("reviewer"))
            and bool(future_hint)
        )
        countable_label_candidate = False
        non_countable_blockers = {
            "review_only_reaction_substrate_mismatch_lane",
            "not_seed_fingerprint_training_label",
        }
        if decision_action == "reject_label":
            non_countable_blockers.add("expert_rejected_current_label_candidate")
        if decision.get("label_type") == "out_of_scope":
            non_countable_blockers.add("expert_confirmed_out_of_scope_boundary")
        if not expert_supported:
            non_countable_blockers.add("family_mapping_not_expert_supported")
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": item.get("entry_name")
                or context.get("entry_name")
                or export_context.get("entry_name"),
                "family_id": family_id,
                "family_name": assignment["family_name"],
                "parent_family_id": assignment["parent_family_id"],
                "support_level": (
                    "expert_review_supported_family_boundary"
                    if expert_supported
                    else "review_only_family_hint_without_expert_resolution"
                    if future_hint
                    else assignment["support_level"]
                ),
                "evidence_sources": assignment["evidence_sources"],
                "future_fingerprint_family_hint": future_hint,
                "decision_action": decision_action,
                "decision_label_type": decision.get("label_type"),
                "decision_review_status": decision.get("review_status"),
                "reaction_substrate_resolution": reaction_resolution,
                "reviewer": decision.get("reviewer"),
                "top1_fingerprint_id": context.get("top1_fingerprint_id")
                or export_context.get("top1_fingerprint_id")
                or queue_row.get("top1_fingerprint_id")
                or family_guardrail.get("top1_fingerprint_id"),
                "top1_ontology_family": context.get("top1_ontology_family")
                or export_context.get("top1_ontology_family")
                or queue_row.get("top1_ontology_family")
                or family_guardrail.get("top1_ontology_family"),
                "propagation_blockers": _sorted_strings(
                    family_guardrail.get("propagation_blockers", [])
                ),
                "mismatch_reasons": _sorted_strings(
                    context.get("mismatch_reasons", [])
                    or export_context.get("mismatch_reasons", [])
                    or family_guardrail.get("reaction_substrate_mismatch_reasons", [])
                    or queue_row.get("reaction_substrate_mismatch_reasons", [])
                ),
                "active_learning_rank": queue_row.get("rank"),
                "adversarial_control_axes": _sorted_strings(
                    adversarial_by_entry.get(entry_id, {}).get("control_axes", [])
                ),
                "countable_label_candidate": countable_label_candidate,
                "non_countable_blockers": sorted(non_countable_blockers),
                "review_policy": (
                    "Family assignment is a first-class ontology boundary for "
                    "routing and adversarial controls, but does not create a "
                    "countable label from review-only mismatch artifacts."
                ),
            }
        )

    mapped_required_family_ids = sorted({row["family_id"] for row in rows})
    unmapped_required_family_ids = sorted(
        set(ATP_PHOSPHORYL_TRANSFER_FAMILY_IDS) - set(mapped_required_family_ids)
    )
    supported_rows = [
        row
        for row in rows
        if row["support_level"] == "expert_review_supported_family_boundary"
    ]
    unsupported_rows = [
        row
        for row in rows
        if row["support_level"] != "expert_review_supported_family_boundary"
    ]
    family_counts = Counter(row["family_id"] for row in rows)
    decision_counts = Counter(row["decision_action"] for row in rows)
    countable_label_candidate_count = sum(
        1 for row in rows if row["countable_label_candidate"]
    )
    boundary_guardrail_ready = (
        all_required_families_present
        and all_required_families_have_scope_notes
        and all_required_family_relationships_declared
        and not unmapped_required_family_ids
        and not countable_label_candidate_count
        and not unsupported_rows
    )
    return {
        "metadata": {
            "method": "atp_phosphoryl_transfer_family_expansion",
            "ontology_version": ontology.get("version"),
            "parent_family_id": ATP_PHOSPHORYL_PARENT_FAMILY_ID,
            "required_family_ids": list(ATP_PHOSPHORYL_TRANSFER_FAMILY_IDS),
            "required_family_count": len(ATP_PHOSPHORYL_TRANSFER_FAMILY_IDS),
            "ontology_target_family_count": len(target_family_records),
            "all_required_families_present": all_required_families_present,
            "all_required_families_have_scope_notes": (
                all_required_families_have_scope_notes
            ),
            "all_required_family_relationships_declared": (
                all_required_family_relationships_declared
            ),
            "mapped_required_family_ids": mapped_required_family_ids,
            "unmapped_required_family_ids": unmapped_required_family_ids,
            "all_required_families_have_supported_mappings": (
                not unmapped_required_family_ids and not unsupported_rows
            ),
            "supported_mapping_count": len(supported_rows),
            "unsupported_mapping_count": len(unsupported_rows),
            "non_target_expert_hint_count": len(non_target_hint_rows),
            "family_counts": dict(sorted(family_counts.items())),
            "decision_action_counts": dict(sorted(decision_counts.items())),
            "countable_label_candidate_count": countable_label_candidate_count,
            "boundary_guardrail_ready": boundary_guardrail_ready,
            "ready_for_label_count_growth_after_gate": boundary_guardrail_ready,
            "active_queue_family_boundary_count": int(
                (active_learning_queue or {})
                .get("metadata", {})
                .get("atp_phosphoryl_transfer_family_boundary_count", 0)
                or 0
            ),
            "family_guardrail_family_boundary_count": int(
                (family_propagation_guardrails or {})
                .get("metadata", {})
                .get("atp_phosphoryl_transfer_family_boundary_count", 0)
                or 0
            ),
            "adversarial_negative_family_boundary_count": int(
                (adversarial_negatives or {})
                .get("metadata", {})
                .get("atp_phosphoryl_transfer_family_boundary_count", 0)
                or 0
            ),
            "review_only_rule": (
                "Expert-reviewed future-family hints map reaction/substrate "
                "mismatch lanes to ontology families, but all mapped rows remain "
                "non-countable boundary evidence unless a separate countable "
                "label-review path clears the factory gates."
            ),
        },
        "target_families": target_family_records,
        "rows": sorted(
            rows,
            key=lambda row: (row["family_id"], _entry_id_sort_key(row["entry_id"])),
        ),
        "non_target_expert_hint_rows": sorted(
            non_target_hint_rows,
            key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))),
        ),
    }


def _atp_target_family_record(
    family_id: str,
    family: dict[str, Any],
) -> dict[str, Any]:
    sibling_ids = _sorted_strings(family.get("sibling_ids", []))
    parent_id = family.get("parent_id")
    scope_note = family.get("scope_note")
    return {
        "id": family_id,
        "name": family.get("name") or ATP_PHOSPHORYL_TRANSFER_FAMILY_NAMES[family_id],
        "present_in_ontology": bool(family),
        "parent_id": parent_id,
        "scope_note": scope_note,
        "has_scope_note": isinstance(scope_note, str) and len(scope_note) >= 40,
        "sibling_ids": sibling_ids,
        "has_parent_or_sibling_relationship": (
            parent_id == ATP_PHOSPHORYL_PARENT_FAMILY_ID or bool(sibling_ids)
        ),
        "family_boundary_guardrails": _sorted_strings(
            family.get("family_boundary_guardrails", [])
        ),
    }


def _review_export_context_by_entry(
    review_export: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    contexts: dict[str, dict[str, Any]] = {}
    for item in (review_export or {}).get("review_items", []):
        if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
            continue
        context = item.get("mismatch_context", {})
        contexts[str(item["entry_id"])] = context if isinstance(context, dict) else {}
    return contexts


def audit_sequence_similarity_failure_sets(
    sequence_clusters: dict[str, Any],
    labels: list[MechanismLabel],
    *,
    active_learning_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prepare exact-reference cluster failure sets for propagation audits."""
    labels_by_entry = {label.entry_id: label for label in labels}
    queue_by_entry = {
        str(row.get("entry_id")): row
        for row in (active_learning_queue or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    rows: list[dict[str, Any]] = []
    for cluster in sequence_clusters.get("clusters", []):
        if not isinstance(cluster, dict):
            continue
        entry_ids = _sorted_entry_ids(cluster.get("entry_ids", []))
        if len(entry_ids) <= 1:
            continue
        label_type_counts = Counter(
            labels_by_entry[entry_id].label_type
            for entry_id in entry_ids
            if entry_id in labels_by_entry
        )
        fingerprint_counts = Counter(
            labels_by_entry[entry_id].fingerprint_id or "out_of_scope"
            for entry_id in entry_ids
            if entry_id in labels_by_entry
        )
        top1_family_counts = Counter(
            str(queue_by_entry[entry_id].get("top1_ontology_family"))
            for entry_id in entry_ids
            if entry_id in queue_by_entry
            and queue_by_entry[entry_id].get("top1_ontology_family")
        )
        review_actions = Counter(
            str(queue_by_entry[entry_id].get("recommended_action"))
            for entry_id in entry_ids
            if entry_id in queue_by_entry
            and queue_by_entry[entry_id].get("recommended_action")
        )
        risk_flags = set()
        if len(label_type_counts) > 1:
            risk_flags.add("mixed_label_types_within_sequence_cluster")
        if len(fingerprint_counts) > 1:
            risk_flags.add("mixed_fingerprints_within_sequence_cluster")
        if len(top1_family_counts) > 1:
            risk_flags.add("mixed_top1_families_within_sequence_cluster")
        if review_actions:
            risk_flags.add("active_queue_cluster_member")
        if any(
            labels_by_entry[entry_id].review_status not in COUNTABLE_REVIEW_STATUSES
            for entry_id in entry_ids
            if entry_id in labels_by_entry
        ):
            risk_flags.add("review_state_cluster_member")
        rows.append(
            {
                "sequence_cluster_id": cluster.get("sequence_cluster_id")
                or cluster.get("id"),
                "cluster_source": cluster.get("cluster_source"),
                "entry_ids": entry_ids,
                "label_type_counts": dict(sorted(label_type_counts.items())),
                "fingerprint_counts": dict(sorted(fingerprint_counts.items())),
                "top1_ontology_family_counts": dict(sorted(top1_family_counts.items())),
                "active_queue_recommended_action_counts": dict(
                    sorted(review_actions.items())
                ),
                "risk_flags": sorted(risk_flags) or ["duplicate_cluster_control"],
                "countable_label_candidate": False,
                "recommended_next_action": (
                    "keep as sequence-similarity failure control before any "
                    "family propagation or learned retrieval split"
                ),
            }
        )

    risk_counts = Counter(flag for row in rows for flag in row["risk_flags"])
    return {
        "metadata": {
            "method": "sequence_similarity_failure_set_audit",
            "cluster_source": sequence_clusters.get("metadata", {}).get(
                "cluster_source"
            ),
            "input_cluster_count": sequence_clusters.get("metadata", {}).get(
                "cluster_count"
            ),
            "duplicate_cluster_count": len(rows),
            "risk_flag_counts": dict(sorted(risk_counts.items())),
            "countable_label_candidate_count": 0,
            "review_only_rule": (
                "exact-reference clusters are failure-set controls; they do not "
                "propagate labels without mechanism evidence"
            ),
        },
        "rows": rows,
    }


def build_provisional_review_decision_batch(
    review_artifact: dict[str, Any],
    *,
    batch_id: str = "provisional_batch",
    reviewer: str = "automation_label_factory",
    max_boundary_controls: int = 5,
    entry_ids: set[str] | None = None,
) -> dict[str, Any]:
    batch = deepcopy(review_artifact)
    requested_entry_ids = set(entry_ids or set())
    if requested_entry_ids:
        batch["review_items"] = [
            item
            for item in batch.get("review_items", [])
            if isinstance(item, dict) and item.get("entry_id") in requested_entry_ids
        ]
    review_source_method = review_artifact.get("metadata", {}).get("method")
    reaction_mismatch_review_only = (
        review_source_method == "reaction_substrate_mismatch_review_export"
    )
    expert_label_decision_review_only = (
        review_source_method == "expert_label_decision_review_export"
    )
    local_evidence_gap_review_only = (
        review_source_method == "expert_label_decision_local_evidence_review_export"
    )
    decision_counts: Counter = Counter()
    decision_entry_ids: dict[str, list[str]] = {}
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
        if reaction_mismatch_review_only or isinstance(item.get("mismatch_context"), dict):
            item["decision"] = {
                **decision,
                "action": "no_decision",
                "reviewer": None,
                "rationale": None,
                "evidence_score": None,
                "review_status": "expert_reviewed",
                "reaction_substrate_resolution": "needs_more_evidence",
            }
        elif expert_label_decision_review_only or isinstance(
            item.get("expert_label_decision_context"), dict
        ):
            item["decision"] = {
                **decision,
                "action": "no_decision",
                "reviewer": None,
                "rationale": None,
                "evidence_score": None,
                "review_status": "expert_reviewed",
                "expert_label_resolution": "needs_external_review",
            }
        elif local_evidence_gap_review_only or isinstance(
            item.get("local_evidence_gap_context"), dict
        ):
            item["decision"] = {
                **decision,
                "action": "no_decision",
                "reviewer": None,
                "rationale": None,
                "evidence_score": None,
                "review_status": "expert_reviewed",
                "local_evidence_resolution": "needs_more_evidence",
            }
        elif item.get("current_label") is None:
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
        action = str(item["decision"].get("action", "no_decision"))
        decision_counts[action] += 1
        if isinstance(item.get("entry_id"), str):
            decision_entry_ids.setdefault(action, []).append(str(item["entry_id"]))
    metadata = dict(batch.get("metadata", {}))
    metadata.update(
        {
            "method": "provisional_label_review_decision_batch",
            "source_method": review_source_method,
            "batch_id": batch_id,
            "reviewer": reviewer,
            "selected_entry_ids": sorted(requested_entry_ids),
            "missing_entry_ids": sorted(
                requested_entry_ids
                - {
                    str(item.get("entry_id"))
                    for item in batch.get("review_items", [])
                    if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
                }
            ),
            "decision_counts": dict(sorted(decision_counts.items())),
            "decision_entry_ids": {
                action: sorted(entry_ids)
                for action, entry_ids in sorted(decision_entry_ids.items())
            },
            "boundary_control_decisions": selected_boundary_controls,
            "reaction_substrate_mismatch_review_only": reaction_mismatch_review_only,
            "expert_label_decision_review_only": expert_label_decision_review_only,
            "local_evidence_gap_review_only": local_evidence_gap_review_only,
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
    reaction_substrate_mismatch_review_export: dict[str, Any] | None = None,
    expert_label_decision_review_export: dict[str, Any] | None = None,
    expert_label_decision_repair_candidates: dict[str, Any] | None = None,
    expert_label_decision_repair_guardrail_audit: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_gap_audit: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_review_export: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_repair_resolution: dict[str, Any] | None = None,
    explicit_alternate_residue_position_requests: dict[str, Any] | None = None,
    review_only_import_safety_audit: dict[str, Any] | None = None,
    atp_phosphoryl_transfer_family_expansion: dict[str, Any] | None = None,
    accepted_review_debt_deferral_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ontology = load_mechanism_ontology()
    required_terms = {
        "uncertainty",
        "impact",
        "novelty",
        "hard_negative_value",
        "evidence_conflict",
        "family_boundary_value",
        "reaction_substrate_mismatch_value",
    }
    active_queue_meta = active_learning_queue.get("metadata", {})
    ranking_terms = set(active_queue_meta.get("ranking_terms", []))
    adversarial_axes = set(adversarial_negatives.get("metadata", {}).get("axis_counts", {}))
    queue_family_counts = Counter(
        str(row.get("top1_ontology_family"))
        for row in active_learning_queue.get("rows", [])
        if isinstance(row, dict) and row.get("top1_ontology_family")
    )
    queue_family_total = sum(queue_family_counts.values())
    dominant_queue_family = queue_family_counts.most_common(1)[0] if queue_family_counts else None
    dominant_queue_fraction = (
        dominant_queue_family[1] / queue_family_total
        if dominant_queue_family and queue_family_total
        else 0.0
    )
    exported_review_entry_ids = {
        str(item.get("entry_id"))
        for item in expert_review_export.get("review_items", [])
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    }
    underrepresented_queue_entry_ids = sorted(
        (
            str(row.get("entry_id"))
            for row in active_learning_queue.get("rows", [])
            if isinstance(row, dict)
            and isinstance(row.get("entry_id"), str)
            and dominant_queue_family
            and row.get("top1_ontology_family")
            and str(row.get("top1_ontology_family")) != dominant_queue_family[0]
        ),
        key=_entry_id_sort_key,
    )
    omitted_underrepresented_entry_ids = sorted(
        set(underrepresented_queue_entry_ids) - exported_review_entry_ids,
        key=_entry_id_sort_key,
    )
    export_diversity_ready = (
        dominant_queue_fraction < 0.6 or not omitted_underrepresented_entry_ids
    )
    family_meta = (family_propagation_guardrails or {}).get("metadata", {})
    family_mismatch_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in (family_propagation_guardrails or {}).get("rows", [])
        if isinstance(row, dict) and row.get("reaction_substrate_mismatch_reasons")
    )
    family_mismatch_count = max(
        int(family_meta.get("reaction_substrate_mismatch_count", 0) or 0),
        len(family_mismatch_entry_ids),
    )
    mismatch_export_meta = (reaction_substrate_mismatch_review_export or {}).get(
        "metadata", {}
    )
    mismatch_export_present = (
        mismatch_export_meta.get("method")
        == "reaction_substrate_mismatch_review_export"
    )
    mismatch_export_labeled_seed_count = int(
        mismatch_export_meta.get("labeled_seed_mismatch_count", 0) or 0
    )
    mismatch_export_entry_ids = _sorted_entry_ids(
        mismatch_export_meta.get("exported_entry_ids", [])
    )
    if reaction_substrate_mismatch_review_export and not mismatch_export_entry_ids:
        mismatch_export_entry_ids = _sorted_entry_ids(
            item.get("entry_id")
            for item in reaction_substrate_mismatch_review_export.get(
                "review_items", []
            )
            if isinstance(item, dict)
        )
    missing_mismatch_export_entry_ids = _sorted_entry_ids(
        set(family_mismatch_entry_ids) - set(mismatch_export_entry_ids)
    )
    mismatch_export_ready = (
        family_mismatch_count == 0
        or (
            mismatch_export_present
            and int(mismatch_export_meta.get("exported_count", 0) or 0)
            >= family_mismatch_count
            and not missing_mismatch_export_entry_ids
            and mismatch_export_labeled_seed_count == 0
        )
    )
    expert_label_decision_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in active_learning_queue.get("rows", [])
        if isinstance(row, dict)
        and isinstance(row.get("entry_id"), str)
        and row.get("recommended_action") == "expert_label_decision_needed"
    )
    expert_label_export_meta = (expert_label_decision_review_export or {}).get(
        "metadata", {}
    )
    expert_label_export_present = (
        expert_label_export_meta.get("method")
        == "expert_label_decision_review_export"
    )
    expert_label_export_entry_ids = _sorted_entry_ids(
        expert_label_export_meta.get("exported_entry_ids", [])
    )
    if expert_label_decision_review_export and not expert_label_export_entry_ids:
        expert_label_export_entry_ids = _sorted_entry_ids(
            item.get("entry_id")
            for item in expert_label_decision_review_export.get("review_items", [])
            if isinstance(item, dict)
        )
    missing_expert_label_export_entry_ids = _sorted_entry_ids(
        set(expert_label_decision_entry_ids) - set(expert_label_export_entry_ids)
    )
    expert_label_export_decision_counts = expert_label_export_meta.get(
        "decision_counts", {}
    )
    expert_label_export_countable_count = int(
        expert_label_export_meta.get("countable_label_candidate_count", 0) or 0
    )
    expert_label_export_ready = (
        not expert_label_decision_entry_ids
        or (
            expert_label_export_present
            and int(expert_label_export_meta.get("exported_count", 0) or 0)
            >= len(expert_label_decision_entry_ids)
            and not missing_expert_label_export_entry_ids
            and expert_label_export_countable_count == 0
            and bool(expert_label_export_meta.get("export_ready", True))
            and int(expert_label_export_decision_counts.get("no_decision", 0) or 0)
            == int(expert_label_export_meta.get("exported_count", 0) or 0)
        )
    )
    expert_label_repair_meta = (
        expert_label_decision_repair_candidates or {}
    ).get("metadata", {})
    expert_label_repair_present = (
        expert_label_repair_meta.get("method")
        == "expert_label_decision_repair_candidate_summary"
    )
    expert_label_repair_entry_ids = _sorted_entry_ids(
        expert_label_repair_meta.get("candidate_entry_ids", [])
    )
    if expert_label_decision_repair_candidates and not expert_label_repair_entry_ids:
        expert_label_repair_entry_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in expert_label_decision_repair_candidates.get("rows", [])
            if isinstance(row, dict)
        )
    expert_label_repair_candidate_count = int(
        expert_label_repair_meta.get("candidate_count", 0) or 0
    )
    expert_label_repair_entry_id_count_matches = (
        expert_label_repair_candidate_count == len(expert_label_repair_entry_ids)
    )
    missing_expert_label_repair_entry_ids = _sorted_entry_ids(
        set(expert_label_decision_entry_ids) - set(expert_label_repair_entry_ids)
    )
    expert_label_repair_countable_count = int(
        expert_label_repair_meta.get("countable_label_candidate_count", 0) or 0
    )
    expert_label_repair_ready = (
        not expert_label_decision_entry_ids
        or (
            expert_label_repair_present
            and expert_label_repair_candidate_count
            >= len(expert_label_decision_entry_ids)
            and expert_label_repair_entry_id_count_matches
            and not missing_expert_label_repair_entry_ids
            and expert_label_repair_countable_count == 0
        )
    )
    expert_label_repair_guardrail_meta = (
        expert_label_decision_repair_guardrail_audit or {}
    ).get("metadata", {})
    expert_label_repair_guardrail_present = (
        expert_label_repair_guardrail_meta.get("method")
        == "expert_label_decision_repair_guardrail_audit"
    )
    expert_label_repair_guardrail_countable_count = int(
        expert_label_repair_guardrail_meta.get("countable_label_candidate_count", 0)
        or 0
    )
    expert_label_repair_guardrail_ready = (
        not expert_label_decision_entry_ids
        or (
            expert_label_repair_guardrail_present
            and bool(expert_label_repair_guardrail_meta.get("guardrail_ready"))
            and bool(
                expert_label_repair_guardrail_meta.get(
                    "all_priority_lanes_non_countable"
                )
            )
            and expert_label_repair_guardrail_countable_count == 0
        )
    )
    expert_label_local_gap_meta = (
        expert_label_decision_local_evidence_gap_audit or {}
    ).get("metadata", {})
    expert_label_local_gap_present = (
        expert_label_local_gap_meta.get("method")
        == "expert_label_decision_local_evidence_gap_audit"
    )
    expert_label_local_gap_countable_count = int(
        expert_label_local_gap_meta.get("countable_label_candidate_count", 0) or 0
    )
    expert_label_guardrail_priority_count = int(
        expert_label_repair_guardrail_meta.get("priority_repair_row_count", 0) or 0
    )
    expert_label_local_gap_missing_ids = _sorted_entry_ids(
        expert_label_local_gap_meta.get("missing_priority_entry_ids", [])
    )
    expert_label_local_gap_ready = (
        not expert_label_decision_entry_ids
        or expert_label_guardrail_priority_count == 0
        or (
            expert_label_local_gap_present
            and bool(expert_label_local_gap_meta.get("audit_ready"))
            and bool(
                expert_label_local_gap_meta.get("priority_rows_accounted_for")
            )
            and not expert_label_local_gap_missing_ids
            and expert_label_local_gap_countable_count == 0
            and int(
                expert_label_local_gap_meta.get("audited_entry_count", 0) or 0
            )
            >= expert_label_guardrail_priority_count
        )
    )
    expert_label_local_export_meta = (
        expert_label_decision_local_evidence_review_export or {}
    ).get("metadata", {})
    expert_label_local_export_present = (
        expert_label_local_export_meta.get("method")
        == "expert_label_decision_local_evidence_review_export"
    )
    expert_label_local_export_count = int(
        expert_label_local_export_meta.get("exported_count", 0) or 0
    )
    expert_label_local_export_countable_count = int(
        expert_label_local_export_meta.get("countable_label_candidate_count", 0) or 0
    )
    expert_label_local_export_decision_counts = (
        expert_label_local_export_meta.get("decision_counts", {})
    )
    if not isinstance(expert_label_local_export_decision_counts, dict):
        expert_label_local_export_decision_counts = {}
    expert_label_local_export_no_decision_count = int(
        expert_label_local_export_decision_counts.get("no_decision", 0) or 0
    )
    expert_label_local_gap_audited_count = int(
        expert_label_local_gap_meta.get("audited_entry_count", 0) or 0
    )
    expert_label_local_export_ready = (
        not expert_label_decision_entry_ids
        or expert_label_guardrail_priority_count == 0
        or (
            expert_label_local_export_present
            and bool(expert_label_local_export_meta.get("export_ready"))
            and bool(expert_label_local_export_meta.get("all_source_rows_exported"))
            and expert_label_local_export_count >= expert_label_local_gap_audited_count
            and expert_label_local_export_countable_count == 0
            and expert_label_local_export_no_decision_count
            == expert_label_local_export_count
        )
    )
    expert_label_local_resolution_meta = (
        expert_label_decision_local_evidence_repair_resolution or {}
    ).get("metadata", {})
    expert_label_local_resolution_present = (
        expert_label_local_resolution_meta.get("method")
        == "expert_label_decision_local_evidence_repair_resolution"
    )
    expert_label_local_resolution_countable_count = int(
        expert_label_local_resolution_meta.get("countable_label_candidate_count", 0)
        or 0
    )
    expert_label_local_resolution_resolved_count = int(
        expert_label_local_resolution_meta.get("resolved_entry_count", 0) or 0
    )
    expert_label_local_resolution_ready = (
        not expert_label_decision_local_evidence_repair_resolution
        or (
            expert_label_local_resolution_present
            and bool(expert_label_local_resolution_meta.get("resolution_ready"))
            and expert_label_local_resolution_resolved_count > 0
            and expert_label_local_resolution_countable_count == 0
            and bool(
                expert_label_local_resolution_meta.get(
                    "all_resolved_rows_non_countable"
                )
            )
        )
    )
    alternate_residue_request_meta = (
        explicit_alternate_residue_position_requests or {}
    ).get("metadata", {})
    alternate_residue_request_present = (
        alternate_residue_request_meta.get("method")
        == "explicit_alternate_residue_position_sourcing_requests"
    )
    alternate_residue_request_count = int(
        alternate_residue_request_meta.get("request_count", 0) or 0
    )
    alternate_residue_request_countable_count = int(
        alternate_residue_request_meta.get("countable_label_candidate_count", 0) or 0
    )
    local_gap_action_counts = expert_label_local_gap_meta.get(
        "recommended_action_counts", {}
    )
    if not isinstance(local_gap_action_counts, dict):
        local_gap_action_counts = {}
    expected_alternate_residue_request_count = int(
        local_gap_action_counts.get(
            "source_explicit_alternate_structure_residue_positions", 0
        )
        or 0
    )
    alternate_residue_request_ready = (
        not explicit_alternate_residue_position_requests
        or expected_alternate_residue_request_count == 0
        or (
            alternate_residue_request_present
            and bool(alternate_residue_request_meta.get("sourcing_request_ready"))
            and alternate_residue_request_count
            >= expected_alternate_residue_request_count
            and alternate_residue_request_countable_count == 0
        )
    )
    import_safety_meta = (review_only_import_safety_audit or {}).get("metadata", {})
    import_safety_present = (
        import_safety_meta.get("method") == "review_only_import_safety_audit"
    )
    import_safety_new_count = int(
        import_safety_meta.get("total_new_countable_label_count", 0) or 0
    )
    import_safety_ready = (
        not review_only_import_safety_audit
        or (
            import_safety_present
            and bool(import_safety_meta.get("countable_import_safe"))
            and import_safety_new_count == 0
        )
    )
    atp_family_expansion_meta = (
        atp_phosphoryl_transfer_family_expansion or {}
    ).get("metadata", {})
    atp_family_expansion_present = (
        atp_family_expansion_meta.get("method")
        == "atp_phosphoryl_transfer_family_expansion"
    )
    atp_family_expansion_countable_count = int(
        atp_family_expansion_meta.get("countable_label_candidate_count", 0) or 0
    )
    atp_family_expansion_ready = (
        not atp_phosphoryl_transfer_family_expansion
        or (
            atp_family_expansion_present
            and bool(atp_family_expansion_meta.get("boundary_guardrail_ready"))
            and bool(atp_family_expansion_meta.get("all_required_families_present"))
            and bool(
                atp_family_expansion_meta.get(
                    "all_required_families_have_scope_notes"
                )
            )
            and bool(
                atp_family_expansion_meta.get(
                    "all_required_family_relationships_declared"
                )
            )
            and not atp_family_expansion_meta.get("unmapped_required_family_ids", [])
            and atp_family_expansion_countable_count == 0
        )
    )
    deferral_meta = (accepted_review_debt_deferral_audit or {}).get("metadata", {})
    deferral_present = (
        deferral_meta.get("method") == "accepted_review_debt_deferral_audit"
    )
    deferral_countable_count = int(
        deferral_meta.get("countable_label_candidate_count", 0) or 0
    )
    deferral_overlap_count = int(
        deferral_meta.get("accepted_review_debt_overlap_count", 0) or 0
    )
    deferral_ready = (
        not accepted_review_debt_deferral_audit
        or (
            deferral_present
            and bool(deferral_meta.get("deferral_ready"))
            and deferral_countable_count == 0
            and deferral_overlap_count == 0
        )
    )
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
            active_queue_meta.get("queued_count", 0)
        )
        > 0
        and required_terms <= ranking_terms,
        "active_queue_retains_unlabeled_candidates": bool(
            active_queue_meta.get("all_unlabeled_rows_retained", True)
        ),
        "adversarial_negatives_mined": int(
            adversarial_negatives.get("metadata", {}).get("control_count", 0)
        )
        > 0
        and bool(adversarial_axes - {"threshold_boundary", "false_non_abstention"}),
        "expert_review_export_ready": int(
            expert_review_export.get("metadata", {}).get("exported_count", 0)
        )
        > 0,
        "expert_review_export_diversity_ready": export_diversity_ready,
        "family_propagation_guardrails_ready": (
            isinstance(family_propagation_guardrails, dict)
            and int(family_meta.get("reported_count", 0))
            > 0
            and bool(family_meta.get("source_guardrails"))
        ),
        "reaction_substrate_mismatch_review_export_ready": mismatch_export_ready,
        "expert_label_decision_review_export_ready": expert_label_export_ready,
        "expert_label_decision_repair_candidates_ready": (
            expert_label_repair_ready
        ),
        "expert_label_decision_repair_guardrails_ready": (
            expert_label_repair_guardrail_ready
        ),
        "expert_label_decision_local_evidence_gaps_audited": (
            expert_label_local_gap_ready
        ),
        "expert_label_decision_local_evidence_review_export_ready": (
            expert_label_local_export_ready
        ),
    }
    if expert_label_decision_local_evidence_repair_resolution is not None:
        gates["expert_label_decision_local_evidence_repair_resolution_ready"] = (
            expert_label_local_resolution_ready
        )
    if explicit_alternate_residue_position_requests is not None:
        gates["explicit_alternate_residue_position_requests_ready"] = (
            alternate_residue_request_ready
        )
    if review_only_import_safety_audit is not None:
        gates["review_only_import_safety_audit_ready"] = import_safety_ready
    if atp_phosphoryl_transfer_family_expansion is not None:
        gates["atp_phosphoryl_transfer_family_expansion_ready"] = (
            atp_family_expansion_ready
        )
    if accepted_review_debt_deferral_audit is not None:
        gates["accepted_review_debt_deferral_audit_ready"] = deferral_ready
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "label_factory_gate_check",
            "label_count": len(labels),
            "passed_gate_count": sum(1 for passed in gates.values() if passed),
            "gate_count": len(gates),
            "automation_ready_for_next_label_batch": not blockers,
            "dominant_active_queue_family": dominant_queue_family[0]
            if dominant_queue_family
            else None,
            "dominant_active_queue_family_fraction": round(dominant_queue_fraction, 4),
            "underrepresented_queue_entry_count": len(underrepresented_queue_entry_ids),
            "omitted_underrepresented_queue_entry_ids": omitted_underrepresented_entry_ids,
            "family_guardrail_reaction_substrate_mismatch_count": family_mismatch_count,
            "family_guardrail_reaction_substrate_mismatch_entry_ids": (
                family_mismatch_entry_ids
            ),
            "reaction_substrate_mismatch_review_export_present": (
                mismatch_export_present
            ),
            "reaction_substrate_mismatch_review_export_entry_ids": (
                mismatch_export_entry_ids
            ),
            "reaction_substrate_mismatch_review_export_missing_entry_ids": (
                missing_mismatch_export_entry_ids
            ),
            "reaction_substrate_mismatch_review_export_labeled_seed_mismatch_count": (
                mismatch_export_labeled_seed_count
            ),
            "active_queue_expert_label_decision_count": len(
                expert_label_decision_entry_ids
            ),
            "active_queue_expert_label_decision_entry_ids": (
                expert_label_decision_entry_ids
            ),
            "expert_label_decision_review_export_present": (
                expert_label_export_present
            ),
            "expert_label_decision_review_export_entry_ids": (
                expert_label_export_entry_ids
            ),
            "expert_label_decision_review_export_missing_entry_ids": (
                missing_expert_label_export_entry_ids
            ),
            "expert_label_decision_review_export_countable_label_candidate_count": (
                expert_label_export_countable_count
            ),
            "expert_label_decision_repair_candidates_present": (
                expert_label_repair_present
            ),
            "expert_label_decision_repair_candidate_entry_ids": (
                expert_label_repair_entry_ids
            ),
            "expert_label_decision_repair_candidate_count": (
                expert_label_repair_candidate_count
            ),
            "expert_label_decision_repair_candidate_entry_id_count_matches": (
                expert_label_repair_entry_id_count_matches
            ),
            "expert_label_decision_repair_candidates_missing_entry_ids": (
                missing_expert_label_repair_entry_ids
            ),
            "expert_label_decision_repair_candidates_countable_label_candidate_count": (
                expert_label_repair_countable_count
            ),
            "expert_label_decision_repair_guardrail_audit_present": (
                expert_label_repair_guardrail_present
            ),
            "expert_label_decision_repair_guardrail_priority_repair_row_count": (
                expert_label_repair_guardrail_meta.get("priority_repair_row_count")
            ),
            "expert_label_decision_repair_guardrail_local_evidence_review_only_count": (
                expert_label_repair_guardrail_meta.get(
                    "local_expected_family_evidence_review_only_count"
                )
            ),
            "expert_label_decision_repair_guardrail_countable_label_candidate_count": (
                expert_label_repair_guardrail_countable_count
            ),
            "expert_label_decision_repair_guardrail_ready": (
                expert_label_repair_guardrail_meta.get("guardrail_ready")
            ),
            "expert_label_decision_local_evidence_gap_audit_present": (
                expert_label_local_gap_present
            ),
            "expert_label_decision_local_evidence_gap_audit_ready": (
                expert_label_local_gap_meta.get("audit_ready")
            ),
            "expert_label_decision_local_evidence_gap_audit_audited_entry_count": (
                expert_label_local_gap_meta.get("audited_entry_count")
            ),
            "expert_label_decision_local_evidence_gap_audit_missing_priority_entry_ids": (
                expert_label_local_gap_missing_ids
            ),
            "expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count": (
                expert_label_local_gap_countable_count
            ),
            "expert_label_decision_local_evidence_gap_class_counts": (
                expert_label_local_gap_meta.get("local_evidence_gap_class_counts", {})
            ),
            "expert_label_decision_local_evidence_review_export_present": (
                expert_label_local_export_present
            ),
            "expert_label_decision_local_evidence_review_export_ready": (
                expert_label_local_export_meta.get("export_ready")
            ),
            "expert_label_decision_local_evidence_review_export_exported_count": (
                expert_label_local_export_count
            ),
            "expert_label_decision_local_evidence_review_export_all_source_rows_exported": (
                expert_label_local_export_meta.get("all_source_rows_exported")
            ),
            "expert_label_decision_local_evidence_review_export_countable_label_candidate_count": (
                expert_label_local_export_countable_count
            ),
            "expert_label_decision_local_evidence_review_export_decision_counts": (
                expert_label_local_export_decision_counts
            ),
            "expert_label_decision_local_evidence_repair_resolution_present": (
                expert_label_local_resolution_present
            ),
            "expert_label_decision_local_evidence_repair_resolution_ready": (
                expert_label_local_resolution_meta.get("resolution_ready")
            ),
            "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count": (
                expert_label_local_resolution_resolved_count
            ),
            "expert_label_decision_local_evidence_repair_resolution_resolved_entry_ids": (
                _sorted_entry_ids(
                    expert_label_local_resolution_meta.get("resolved_entry_ids", [])
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_remaining_open_entry_count": (
                int(
                    expert_label_local_resolution_meta.get(
                        "remaining_open_entry_count", 0
                    )
                    or 0
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count": (
                expert_label_local_resolution_countable_count
            ),
            "explicit_alternate_residue_position_requests_present": (
                alternate_residue_request_present
            ),
            "explicit_alternate_residue_position_requests_ready": (
                alternate_residue_request_meta.get("sourcing_request_ready")
            ),
            "explicit_alternate_residue_position_requests_expected_count": (
                expected_alternate_residue_request_count
            ),
            "explicit_alternate_residue_position_requests_count": (
                alternate_residue_request_count
            ),
            "explicit_alternate_residue_position_request_entry_ids": (
                _sorted_entry_ids(
                    alternate_residue_request_meta.get("request_entry_ids", [])
                )
            ),
            "explicit_alternate_residue_position_requests_countable_label_candidate_count": (
                alternate_residue_request_countable_count
            ),
            "review_only_import_safety_audit_present": import_safety_present,
            "review_only_import_safety_audit_ready": (
                import_safety_meta.get("countable_import_safe")
            ),
            "review_only_import_safety_audit_artifact_count": (
                import_safety_meta.get("artifact_count")
            ),
            "review_only_import_safety_audit_total_new_countable_label_count": (
                import_safety_new_count
            ),
            "review_only_import_safety_audit_unsafe_artifacts": (
                import_safety_meta.get("unsafe_artifacts", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_present": (
                atp_family_expansion_present
            ),
            "atp_phosphoryl_transfer_family_expansion_ready": (
                atp_family_expansion_ready
            ),
            "atp_phosphoryl_transfer_family_expansion_mapped_family_ids": (
                atp_family_expansion_meta.get("mapped_required_family_ids", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_unmapped_family_ids": (
                atp_family_expansion_meta.get("unmapped_required_family_ids", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_countable_label_candidate_count": (
                atp_family_expansion_countable_count
            ),
            "accepted_review_debt_deferral_audit_present": deferral_present,
            "accepted_review_debt_deferral_audit_ready": (
                deferral_meta.get("deferral_ready")
            ),
            "accepted_review_debt_deferral_audit_deferred_entry_count": (
                deferral_meta.get("deferred_entry_count")
            ),
            "accepted_review_debt_deferral_audit_countable_label_candidate_count": (
                deferral_countable_count
            ),
            "accepted_review_debt_deferral_audit_accepted_overlap_count": (
                deferral_overlap_count
            ),
            "accepted_review_debt_deferral_audit_strict_remap_guardrail_entry_ids": (
                _sorted_entry_ids(
                    deferral_meta.get("strict_remap_guardrail_entry_ids", [])
                )
            ),
            "accepted_review_debt_deferral_audit_unclassified_new_review_debt_entry_ids": (
                _sorted_entry_ids(
                    deferral_meta.get("unclassified_new_review_debt_entry_ids", [])
                )
            ),
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
    review_evidence_gaps: dict[str, Any] | None = None,
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
    baseline_entry_ids = {label.entry_id for label in baseline_labels}
    new_countable_entry_ids = {
        label.entry_id for label in countable_labels if label.entry_id not in baseline_entry_ids
    }
    review_gap_entry_ids: set[str] = set()
    reaction_mismatch_entry_ids: set[str] = set()
    if review_evidence_gaps:
        for row in review_evidence_gaps.get("rows", []):
            if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
                continue
            entry_id = str(row["entry_id"])
            if row.get("decision_action") == "mark_needs_more_evidence" or bool(
                row.get("gap_reasons")
            ):
                review_gap_entry_ids.add(entry_id)
            mismatch_reasons = _remap_local_reaction_substrate_mismatch_reasons(
                entry_name=str(row.get("entry_name", "")),
                mechanism_text_snippets=row.get("mechanism_text_snippets", []),
                top1_fingerprint_id=row.get("top1_fingerprint_id"),
            )
            if mismatch_reasons:
                reaction_mismatch_entry_ids.add(entry_id)
    accepted_review_gap_ids = sorted(
        new_countable_entry_ids & review_gap_entry_ids,
        key=_entry_id_sort_key,
    )
    accepted_reaction_mismatch_ids = sorted(
        new_countable_entry_ids & reaction_mismatch_entry_ids,
        key=_entry_id_sort_key,
    )
    accepted_new_label_entry_ids = sorted(new_countable_entry_ids, key=_entry_id_sort_key)
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
    if review_evidence_gaps is not None:
        gates["accepted_labels_have_no_review_evidence_gaps"] = not accepted_review_gap_ids
        gates["accepted_labels_have_no_reaction_substrate_mismatches"] = (
            not accepted_reaction_mismatch_ids
        )
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "label_batch_acceptance_check",
            "baseline_label_count": baseline_count,
            "review_state_label_count": len(review_state_labels),
            "countable_label_count": countable_count,
            "accepted_new_label_count": max(0, countable_count - baseline_count),
            "accepted_new_label_entry_ids": accepted_new_label_entry_ids,
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
            "accepted_review_gap_count": len(accepted_review_gap_ids),
            "accepted_review_gap_entry_ids": accepted_review_gap_ids,
            "accepted_reaction_substrate_mismatch_count": len(
                accepted_reaction_mismatch_ids
            ),
            "accepted_reaction_substrate_mismatch_entry_ids": (
                accepted_reaction_mismatch_ids
            ),
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


def summarize_label_factory_batches(
    acceptance_checks: list[tuple[str, dict[str, Any]]],
    gate_checks: list[tuple[str, dict[str, Any]]] | None = None,
    active_learning_queues: list[tuple[str, dict[str, Any]]] | None = None,
    scaling_quality_audits: list[tuple[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    gate_by_batch = {
        _artifact_batch_id(name): artifact
        for name, artifact in gate_checks or []
        if _artifact_batch_id(name)
    }
    queue_by_batch = {
        _artifact_batch_id(name): artifact
        for name, artifact in active_learning_queues or []
        if _artifact_batch_id(name)
    }
    scaling_audit_by_batch = {
        _artifact_batch_id(name): artifact
        for name, artifact in scaling_quality_audits or []
        if _artifact_batch_id(name)
    }
    rows: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    for name, artifact in acceptance_checks:
        batch_id = _artifact_batch_id(name) or str(len(rows) + 1)
        metadata = artifact.get("metadata", {})
        gate = gate_by_batch.get(batch_id, {})
        gate_meta = gate.get("metadata", {}) if isinstance(gate, dict) else {}
        queue = queue_by_batch.get(batch_id, {})
        queue_meta = queue.get("metadata", {}) if isinstance(queue, dict) else {}
        scaling_audit = scaling_audit_by_batch.get(batch_id, {})
        scaling_meta = (
            scaling_audit.get("metadata", {}) if isinstance(scaling_audit, dict) else {}
        )
        scaling_blockers = (
            list(scaling_audit.get("blockers", []))
            if isinstance(scaling_audit, dict)
            else []
        )
        scaling_review_warnings = (
            list(scaling_audit.get("review_warnings", []))
            if isinstance(scaling_audit, dict)
            else []
        )
        scaling_accepted_debt_count = int(
            scaling_meta.get("accepted_new_debt_count", 0) or 0
        )
        scaling_omitted_underrepresented = list(
            scaling_meta.get("omitted_underrepresented_queue_entry_ids", []) or []
        )
        scaling_unclassified_debt = list(
            scaling_meta.get("unclassified_new_review_debt_entry_ids", []) or []
        )
        scaling_quality_ready = None
        if scaling_audit:
            scaling_quality_ready = (
                not scaling_blockers
                and scaling_accepted_debt_count == 0
                and not scaling_omitted_underrepresented
                and not scaling_unclassified_debt
            )
        row_blockers = list(artifact.get("blockers", []))
        if not metadata.get("accepted_for_counting", False):
            row_blockers.append("batch_not_accepted_for_counting")
        if gate_meta and not gate_meta.get("automation_ready_for_next_label_batch", False):
            row_blockers.append("factory_gate_not_ready")
        if queue_meta and not queue_meta.get("all_unlabeled_rows_retained", True):
            row_blockers.append("unlabeled_rows_omitted_from_active_queue")
        if scaling_quality_ready is False:
            row_blockers.append("scaling_quality_audit_not_ready")
        row = {
            "batch": batch_id,
            "source": name,
            "accepted_for_counting": bool(metadata.get("accepted_for_counting", False)),
            "accepted_new_label_count": int(metadata.get("accepted_new_label_count", 0) or 0),
            "baseline_label_count": int(metadata.get("baseline_label_count", 0) or 0),
            "countable_label_count": int(metadata.get("countable_label_count", 0) or 0),
            "review_state_label_count": int(metadata.get("review_state_label_count", 0) or 0),
            "pending_review_count": int(metadata.get("pending_review_count", 0) or 0),
            "hard_negative_count": int(metadata.get("hard_negative_count", 0) or 0),
            "near_miss_count": int(metadata.get("near_miss_count", 0) or 0),
            "out_of_scope_false_non_abstentions": int(
                metadata.get("out_of_scope_false_non_abstentions", 0) or 0
            ),
            "actionable_in_scope_failure_count": int(
                metadata.get("actionable_in_scope_failure_count", 0) or 0
            ),
            "factory_gate_ready": bool(
                metadata.get(
                    "factory_gate_ready",
                    gate_meta.get("automation_ready_for_next_label_batch", False),
                )
            ),
            "gate_count": gate_meta.get("gate_count"),
            "passed_gate_count": gate_meta.get("passed_gate_count"),
            "family_guardrail_reaction_substrate_mismatch_count": gate_meta.get(
                "family_guardrail_reaction_substrate_mismatch_count"
            ),
            "reaction_substrate_mismatch_review_export_present": gate_meta.get(
                "reaction_substrate_mismatch_review_export_present"
            ),
            "reaction_substrate_mismatch_review_export_missing_count": len(
                gate_meta.get(
                    "reaction_substrate_mismatch_review_export_missing_entry_ids",
                )
                or []
            )
            if gate_meta
            else None,
            "active_queue_expert_label_decision_count": gate_meta.get(
                "active_queue_expert_label_decision_count"
            ),
            "expert_label_decision_review_export_present": gate_meta.get(
                "expert_label_decision_review_export_present"
            ),
            "expert_label_decision_review_export_missing_count": len(
                gate_meta.get(
                    "expert_label_decision_review_export_missing_entry_ids",
                )
                or []
            )
            if gate_meta
            else None,
            "expert_label_decision_review_export_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_review_export_countable_label_candidate_count"
                )
            ),
            "expert_label_decision_repair_candidates_present": gate_meta.get(
                "expert_label_decision_repair_candidates_present"
            ),
            "expert_label_decision_repair_candidates_missing_count": len(
                gate_meta.get(
                    "expert_label_decision_repair_candidates_missing_entry_ids",
                )
                or []
            )
            if gate_meta
            else None,
            "expert_label_decision_repair_candidates_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_repair_candidates_countable_label_candidate_count"
                )
            ),
            "expert_label_decision_repair_guardrail_audit_present": gate_meta.get(
                "expert_label_decision_repair_guardrail_audit_present"
            ),
            "expert_label_decision_repair_guardrail_priority_repair_row_count": (
                gate_meta.get(
                    "expert_label_decision_repair_guardrail_priority_repair_row_count"
                )
            ),
            "expert_label_decision_repair_guardrail_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_repair_guardrail_countable_label_candidate_count"
                )
            ),
            "expert_label_decision_local_evidence_gap_audit_present": gate_meta.get(
                "expert_label_decision_local_evidence_gap_audit_present"
            ),
            "expert_label_decision_local_evidence_gap_audit_ready": gate_meta.get(
                "expert_label_decision_local_evidence_gap_audit_ready"
            ),
            "expert_label_decision_local_evidence_gap_audit_audited_entry_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_gap_audit_audited_entry_count"
                )
            ),
            "expert_label_decision_local_evidence_gap_audit_missing_count": len(
                gate_meta.get(
                    "expert_label_decision_local_evidence_gap_audit_missing_priority_entry_ids",
                )
                or []
            )
            if gate_meta
            else None,
            "expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count"
                )
            ),
            "expert_label_decision_local_evidence_review_export_present": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_review_export_present"
                )
            ),
            "expert_label_decision_local_evidence_review_export_ready": gate_meta.get(
                "expert_label_decision_local_evidence_review_export_ready"
            ),
            "expert_label_decision_local_evidence_review_export_exported_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_review_export_exported_count"
                )
            ),
            "expert_label_decision_local_evidence_review_export_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_review_export_countable_label_candidate_count"
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_present": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_repair_resolution_present"
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_ready": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_repair_resolution_ready"
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count"
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count": (
                gate_meta.get(
                    "expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count"
                )
            ),
            "explicit_alternate_residue_position_requests_present": (
                gate_meta.get("explicit_alternate_residue_position_requests_present")
            ),
            "explicit_alternate_residue_position_requests_ready": (
                gate_meta.get("explicit_alternate_residue_position_requests_ready")
            ),
            "explicit_alternate_residue_position_requests_count": (
                gate_meta.get("explicit_alternate_residue_position_requests_count")
            ),
            "explicit_alternate_residue_position_requests_countable_label_candidate_count": (
                gate_meta.get(
                    "explicit_alternate_residue_position_requests_countable_label_candidate_count"
                )
            ),
            "review_only_import_safety_audit_present": gate_meta.get(
                "review_only_import_safety_audit_present"
            ),
            "review_only_import_safety_audit_ready": gate_meta.get(
                "review_only_import_safety_audit_ready"
            ),
            "review_only_import_safety_audit_total_new_countable_label_count": (
                gate_meta.get(
                    "review_only_import_safety_audit_total_new_countable_label_count"
                )
            ),
            "accepted_review_debt_deferral_audit_present": gate_meta.get(
                "accepted_review_debt_deferral_audit_present"
            ),
            "accepted_review_debt_deferral_audit_ready": gate_meta.get(
                "accepted_review_debt_deferral_audit_ready"
            ),
            "accepted_review_debt_deferral_audit_deferred_entry_count": (
                gate_meta.get(
                    "accepted_review_debt_deferral_audit_deferred_entry_count"
                )
            ),
            "accepted_review_debt_deferral_audit_countable_label_candidate_count": (
                gate_meta.get(
                    "accepted_review_debt_deferral_audit_countable_label_candidate_count"
                )
            ),
            "accepted_review_debt_deferral_audit_accepted_overlap_count": (
                gate_meta.get(
                    "accepted_review_debt_deferral_audit_accepted_overlap_count"
                )
            ),
            "active_queue_unlabeled_count": queue_meta.get("total_unlabeled_candidate_count"),
            "active_queue_unlabeled_omitted": queue_meta.get("unlabeled_omitted_by_max_rows"),
            "active_queue_all_unlabeled_retained": queue_meta.get("all_unlabeled_rows_retained"),
            "scaling_quality_audit_present": bool(scaling_audit),
            "scaling_quality_ready": scaling_quality_ready,
            "scaling_quality_recommendation": scaling_meta.get("audit_recommendation"),
            "scaling_quality_blocker_count": len(scaling_blockers),
            "scaling_quality_blockers": scaling_blockers,
            "scaling_quality_review_warnings": scaling_review_warnings,
            "scaling_quality_accepted_new_debt_count": scaling_accepted_debt_count
            if scaling_audit
            else None,
            "scaling_quality_unclassified_new_debt_count": len(scaling_unclassified_debt)
            if scaling_audit
            else None,
            "scaling_quality_omitted_underrepresented_count": len(
                scaling_omitted_underrepresented
            )
            if scaling_audit
            else None,
            "scaling_quality_issue_class_counts": scaling_meta.get("issue_class_counts", {}),
            "blockers": sorted(set(row_blockers)),
        }
        rows.append(row)
        if row["blockers"]:
            blockers.append(
                {
                    "batch": batch_id,
                    "source": name,
                    "blockers": row["blockers"],
                }
            )
    rows = sorted(rows, key=lambda row: _entry_id_sort_key(f"m_csa:{row['batch']}"))
    latest = rows[-1] if rows else {}
    return {
        "metadata": {
            "method": "label_factory_batch_summary",
            "batch_count": len(rows),
            "accepted_batch_count": sum(1 for row in rows if row["accepted_for_counting"]),
            "total_accepted_new_label_count": sum(
                int(row["accepted_new_label_count"]) for row in rows
            ),
            "latest_batch": latest.get("batch"),
            "latest_countable_label_count": latest.get("countable_label_count", 0),
            "latest_pending_review_count": latest.get("pending_review_count", 0),
            "latest_reaction_substrate_mismatch_review_export_present": latest.get(
                "reaction_substrate_mismatch_review_export_present"
            ),
            "latest_reaction_substrate_mismatch_review_export_missing_count": latest.get(
                "reaction_substrate_mismatch_review_export_missing_count"
            ),
            "latest_active_queue_expert_label_decision_count": latest.get(
                "active_queue_expert_label_decision_count"
            ),
            "latest_expert_label_decision_review_export_present": latest.get(
                "expert_label_decision_review_export_present"
            ),
            "latest_expert_label_decision_review_export_missing_count": latest.get(
                "expert_label_decision_review_export_missing_count"
            ),
            "latest_expert_label_decision_review_export_countable_label_candidate_count": latest.get(
                "expert_label_decision_review_export_countable_label_candidate_count"
            ),
            "latest_expert_label_decision_repair_candidates_present": latest.get(
                "expert_label_decision_repair_candidates_present"
            ),
            "latest_expert_label_decision_repair_candidates_missing_count": latest.get(
                "expert_label_decision_repair_candidates_missing_count"
            ),
            "latest_expert_label_decision_repair_candidates_countable_label_candidate_count": latest.get(
                "expert_label_decision_repair_candidates_countable_label_candidate_count"
            ),
            "latest_expert_label_decision_repair_guardrail_audit_present": latest.get(
                "expert_label_decision_repair_guardrail_audit_present"
            ),
            "latest_expert_label_decision_repair_guardrail_priority_repair_row_count": latest.get(
                "expert_label_decision_repair_guardrail_priority_repair_row_count"
            ),
            "latest_expert_label_decision_repair_guardrail_countable_label_candidate_count": latest.get(
                "expert_label_decision_repair_guardrail_countable_label_candidate_count"
            ),
            "latest_expert_label_decision_local_evidence_gap_audit_present": latest.get(
                "expert_label_decision_local_evidence_gap_audit_present"
            ),
            "latest_expert_label_decision_local_evidence_gap_audit_ready": latest.get(
                "expert_label_decision_local_evidence_gap_audit_ready"
            ),
            "latest_expert_label_decision_local_evidence_gap_audit_audited_entry_count": latest.get(
                "expert_label_decision_local_evidence_gap_audit_audited_entry_count"
            ),
            "latest_expert_label_decision_local_evidence_gap_audit_missing_count": latest.get(
                "expert_label_decision_local_evidence_gap_audit_missing_count"
            ),
            "latest_expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count": latest.get(
                "expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count"
            ),
            "latest_expert_label_decision_local_evidence_review_export_present": latest.get(
                "expert_label_decision_local_evidence_review_export_present"
            ),
            "latest_expert_label_decision_local_evidence_review_export_ready": latest.get(
                "expert_label_decision_local_evidence_review_export_ready"
            ),
            "latest_expert_label_decision_local_evidence_review_export_exported_count": latest.get(
                "expert_label_decision_local_evidence_review_export_exported_count"
            ),
            "latest_expert_label_decision_local_evidence_review_export_countable_label_candidate_count": latest.get(
                "expert_label_decision_local_evidence_review_export_countable_label_candidate_count"
            ),
            "latest_expert_label_decision_local_evidence_repair_resolution_present": latest.get(
                "expert_label_decision_local_evidence_repair_resolution_present"
            ),
            "latest_expert_label_decision_local_evidence_repair_resolution_ready": latest.get(
                "expert_label_decision_local_evidence_repair_resolution_ready"
            ),
            "latest_expert_label_decision_local_evidence_repair_resolution_resolved_entry_count": latest.get(
                "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count"
            ),
            "latest_expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count": latest.get(
                "expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count"
            ),
            "latest_explicit_alternate_residue_position_requests_present": latest.get(
                "explicit_alternate_residue_position_requests_present"
            ),
            "latest_explicit_alternate_residue_position_requests_ready": latest.get(
                "explicit_alternate_residue_position_requests_ready"
            ),
            "latest_explicit_alternate_residue_position_requests_count": latest.get(
                "explicit_alternate_residue_position_requests_count"
            ),
            "latest_explicit_alternate_residue_position_requests_countable_label_candidate_count": latest.get(
                "explicit_alternate_residue_position_requests_countable_label_candidate_count"
            ),
            "latest_review_only_import_safety_audit_present": latest.get(
                "review_only_import_safety_audit_present"
            ),
            "latest_review_only_import_safety_audit_ready": latest.get(
                "review_only_import_safety_audit_ready"
            ),
            "latest_review_only_import_safety_audit_total_new_countable_label_count": latest.get(
                "review_only_import_safety_audit_total_new_countable_label_count"
            ),
            "latest_accepted_review_debt_deferral_audit_present": latest.get(
                "accepted_review_debt_deferral_audit_present"
            ),
            "latest_accepted_review_debt_deferral_audit_ready": latest.get(
                "accepted_review_debt_deferral_audit_ready"
            ),
            "latest_accepted_review_debt_deferral_audit_deferred_entry_count": latest.get(
                "accepted_review_debt_deferral_audit_deferred_entry_count"
            ),
            "latest_accepted_review_debt_deferral_audit_countable_label_candidate_count": latest.get(
                "accepted_review_debt_deferral_audit_countable_label_candidate_count"
            ),
            "latest_accepted_review_debt_deferral_audit_accepted_overlap_count": latest.get(
                "accepted_review_debt_deferral_audit_accepted_overlap_count"
            ),
            "all_batches_accepted_for_counting": all(
                row["accepted_for_counting"] for row in rows
            )
            if rows
            else False,
            "all_factory_gates_ready": all(row["factory_gate_ready"] for row in rows)
            if rows
            else False,
            "all_zero_hard_negatives": all(row["hard_negative_count"] == 0 for row in rows)
            if rows
            else False,
            "all_zero_near_misses": all(row["near_miss_count"] == 0 for row in rows)
            if rows
            else False,
            "all_zero_false_non_abstentions": all(
                row["out_of_scope_false_non_abstentions"] == 0 for row in rows
            )
            if rows
            else False,
            "all_zero_actionable_in_scope_failures": all(
                row["actionable_in_scope_failure_count"] == 0 for row in rows
            )
            if rows
            else False,
            "all_active_queues_retain_unlabeled_candidates": all(
                row["active_queue_all_unlabeled_retained"] is not False for row in rows
            )
            if rows
            else False,
            "scaling_quality_audit_count": sum(
                1 for row in rows if row["scaling_quality_audit_present"]
            ),
            "latest_scaling_quality_audit_present": bool(
                latest.get("scaling_quality_audit_present", False)
            ),
            "latest_scaling_quality_recommendation": latest.get(
                "scaling_quality_recommendation"
            ),
            "latest_scaling_quality_review_warnings": latest.get(
                "scaling_quality_review_warnings", []
            ),
            "all_supplied_scaling_quality_audits_ready": all(
                row["scaling_quality_ready"] is not False
                for row in rows
                if row["scaling_quality_audit_present"]
            )
            if rows
            else False,
            "blocker_count": len(blockers),
            "next_batch_rule": (
                "open the next label tranche only when every accepted batch has "
                "zero hard negatives, zero near misses, zero false non-abstentions, "
                "zero actionable in-scope failures, ready factory gates, and active "
                "queues that retain all unlabeled candidates; for preview batches, "
                "also attach the scaling-quality audit and resolve any audit blocker"
            ),
        },
        "rows": rows,
        "blockers": blockers,
    }


def _artifact_batch_id(name: str) -> str | None:
    matches = re.findall(r"(?<!\d)(\d{2,5})(?!\d)", str(name))
    return matches[-1] if matches else None


def check_label_review_resolution(
    baseline_labels: list[MechanismLabel],
    review_state_labels: list[MechanismLabel],
    countable_labels: list[MechanismLabel],
    review_artifact: dict[str, Any],
    label_expansion_candidates: dict[str, Any],
    label_factory_gate: dict[str, Any],
    baseline_label_count: int | None = None,
) -> dict[str, Any]:
    baseline_count = baseline_label_count if baseline_label_count is not None else len(baseline_labels)
    baseline_ids = {label.entry_id for label in baseline_labels}
    review_state_by_entry = {label.entry_id: label for label in review_state_labels}
    countable_by_entry = {label.entry_id: label for label in countable_labels}
    candidate_ids = sorted(
        {
            str(row.get("entry_id"))
            for row in label_expansion_candidates.get("rows", [])
            if isinstance(row, dict)
            and isinstance(row.get("entry_id"), str)
            and row.get("entry_id") not in baseline_ids
        },
        key=_entry_id_sort_key,
    )
    decisions_by_entry: dict[str, str] = {}
    decision_counts: Counter = Counter()
    for item in review_artifact.get("review_items", []):
        if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
            continue
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            continue
        action = str(decision.get("action", "no_decision"))
        decision_counts[action] += 1
        if action != "no_decision":
            decisions_by_entry[str(item["entry_id"])] = action

    resolving_actions = {"accept_label", "mark_needs_more_evidence", "reject_label"}
    unresolved_candidate_ids = [
        entry_id
        for entry_id in candidate_ids
        if decisions_by_entry.get(entry_id) not in resolving_actions
    ]
    accepted_entry_ids = sorted(
        [entry_id for entry_id, action in decisions_by_entry.items() if action == "accept_label"],
        key=_entry_id_sort_key,
    )
    needs_more_evidence_entry_ids = sorted(
        [
            entry_id
            for entry_id, action in decisions_by_entry.items()
            if action == "mark_needs_more_evidence"
        ],
        key=_entry_id_sort_key,
    )
    rejected_entry_ids = sorted(
        [entry_id for entry_id, action in decisions_by_entry.items() if action == "reject_label"],
        key=_entry_id_sort_key,
    )
    needs_more_evidence_not_imported = [
        entry_id
        for entry_id in needs_more_evidence_entry_ids
        if review_state_by_entry.get(entry_id) is None
        or review_state_by_entry[entry_id].review_status != "needs_expert_review"
    ]
    accepted_missing_from_countable = [
        entry_id for entry_id in accepted_entry_ids if entry_id not in countable_by_entry
    ]
    gates = {
        "review_state_preserves_baseline": len(review_state_labels) >= baseline_count,
        "countable_registry_preserves_baseline": len(countable_labels) >= baseline_count,
        "no_pending_review_in_countable": not any(
            label.review_status == "needs_expert_review" for label in countable_labels
        ),
        "review_decisions_cover_unlabeled_candidates": not unresolved_candidate_ids,
        "needs_more_evidence_imported": not needs_more_evidence_not_imported,
        "accepted_decisions_countable": not accepted_missing_from_countable,
        "countable_growth_matches_acceptances": len(countable_labels)
        <= baseline_count + len(accepted_entry_ids),
        "factory_gate_ready": bool(
            label_factory_gate.get("metadata", {}).get("automation_ready_for_next_label_batch")
        ),
    }
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "label_review_resolution_check",
            "baseline_label_count": baseline_count,
            "review_state_label_count": len(review_state_labels),
            "countable_label_count": len(countable_labels),
            "candidate_count": len(candidate_ids),
            "candidate_entry_ids": candidate_ids,
            "accepted_entry_ids": accepted_entry_ids,
            "needs_more_evidence_entry_ids": needs_more_evidence_entry_ids,
            "rejected_entry_ids": rejected_entry_ids,
            "accepted_new_label_count": max(0, len(countable_labels) - baseline_count),
            "remaining_unresolved_candidate_count": len(unresolved_candidate_ids),
            "remaining_unresolved_candidate_ids": unresolved_candidate_ids,
            "needs_more_evidence_not_imported": needs_more_evidence_not_imported,
            "accepted_missing_from_countable": accepted_missing_from_countable,
            "decision_counts": dict(sorted(decision_counts.items())),
            "resolved_for_scaling": not blockers,
            "resolution_rule": (
                "remaining label-expansion candidates must have an accept, reject, "
                "or needs-more-evidence decision before the next tranche opens; "
                "needs-more-evidence records stay out of the countable benchmark"
            ),
        },
        "gates": gates,
        "blockers": blockers,
    }


def analyze_review_evidence_gaps(
    retrieval: dict[str, Any],
    review_artifact: dict[str, Any],
) -> dict[str, Any]:
    results_by_entry = {
        result.get("entry_id"): result
        for result in retrieval.get("results", [])
        if isinstance(result, dict) and isinstance(result.get("entry_id"), str)
    }
    fingerprints_by_id = {
        fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()
    }
    rows: list[dict[str, Any]] = []
    for item in review_artifact.get("review_items", []):
        if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
            continue
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            continue
        action = str(decision.get("action", "no_decision"))
        if action == "no_decision":
            continue
        entry_id = str(item["entry_id"])
        result = results_by_entry.get(entry_id, {})
        queue_context = item.get("queue_context", {})
        if not isinstance(queue_context, dict):
            queue_context = {}
        fingerprint_id = decision.get("fingerprint_id") or queue_context.get(
            "top1_fingerprint_id"
        )
        fingerprint = fingerprints_by_id.get(str(fingerprint_id), {})
        coverage = _cofactor_coverage_row_parts(result, fingerprint) if fingerprint else {}
        top = result.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_score = float(
            top1.get(
                "score",
                queue_context.get("top1_score", 0.0),
            )
            or 0.0
        )
        threshold = float(queue_context.get("abstain_threshold", 0.0) or 0.0)
        target_rank, target = _target_fingerprint_hit(top, str(fingerprint_id))
        target_score = (
            round(float(target.get("score", 0.0) or 0.0), 4)
            if isinstance(target, dict)
            else None
        )
        coverage_status = str(coverage.get("coverage_status", "unknown"))
        gap_reasons = []
        if action == "mark_needs_more_evidence":
            gap_reasons.append("review_marked_needs_more_evidence")
        if coverage_status == "expected_structure_only":
            gap_reasons.append("expected_cofactor_not_local")
        elif coverage_status == "expected_absent_from_structure":
            gap_reasons.append("expected_cofactor_absent_from_structure")
        if threshold and top1_score < threshold:
            gap_reasons.append("top1_below_abstention_threshold")
        if fingerprint_id and target_rank != 1:
            gap_reasons.append("target_not_top1")
        counterevidence = sorted(
            set(
                [
                    str(reason)
                    for reason in queue_context.get("counterevidence_reasons", [])
                    if str(reason)
                ]
                + _fingerprint_component_scores(target or top1).get(
                    "counterevidence_reasons", []
                )
            )
        )
        if counterevidence:
            gap_reasons.append("counterevidence_present")
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": item.get("entry_name") or result.get("entry_name"),
                "decision_action": action,
                "decision_review_status": decision.get("review_status"),
                "target_fingerprint_id": fingerprint_id,
                "target_rank": target_rank,
                "target_score": target_score,
                "top1_fingerprint_id": top1.get(
                    "fingerprint_id",
                    queue_context.get("top1_fingerprint_id"),
                ),
                "top1_score": round(top1_score, 4),
                "abstain_threshold": threshold,
                "coverage_status": coverage_status,
                "expected_cofactor_families": coverage.get(
                    "expected_cofactor_families", []
                ),
                "local_cofactor_families": coverage.get("local_cofactor_families", []),
                "structure_cofactor_families": coverage.get(
                    "structure_cofactor_families", []
                ),
                "matching_structure_ligands": coverage.get(
                    "matching_structure_ligands", []
                ),
                "nearest_expected_ligand_distance_angstrom": coverage.get(
                    "nearest_expected_ligand_distance_angstrom"
                ),
                "proximal_ligand_codes": coverage.get("proximal_ligand_codes", []),
                "structure_ligand_codes": coverage.get("structure_ligand_codes", []),
                "counterevidence_reasons": counterevidence,
                "gap_reasons": sorted(set(gap_reasons)),
                "decision_rationale": decision.get("rationale"),
                "mechanism_text_snippets": result.get("mechanism_text_snippets")
                or queue_context.get("mechanism_text_snippets", []),
            }
        )
    gap_reason_counts = Counter(reason for row in rows for reason in row["gap_reasons"])
    coverage_counts = Counter(str(row["coverage_status"]) for row in rows)
    return {
        "metadata": {
            "method": "review_evidence_gap_analysis",
            "reviewed_decision_count": len(rows),
            "gap_count": sum(1 for row in rows if row["gap_reasons"]),
            "needs_more_evidence_count": sum(
                1 for row in rows if row["decision_action"] == "mark_needs_more_evidence"
            ),
            "needs_more_evidence_entry_ids": sorted(
                (
                    row["entry_id"]
                    for row in rows
                    if row["decision_action"] == "mark_needs_more_evidence"
                ),
                key=_entry_id_sort_key,
            ),
            "coverage_status_counts": dict(sorted(coverage_counts.items())),
            "gap_reason_counts": dict(sorted(gap_reason_counts.items())),
            "audit_rule": (
                "review deferrals must preserve the local evidence gap rather "
                "than silently counting structure-wide or text-only support"
            ),
        },
        "rows": sorted(rows, key=lambda row: _entry_id_sort_key(row["entry_id"])),
    }


def summarize_review_debt(
    review_evidence_gaps: dict[str, Any],
    active_learning_queue: dict[str, Any] | None = None,
    baseline_review_debt: dict[str, Any] | None = None,
    max_rows: int = 25,
) -> dict[str, Any]:
    queue_rank_by_entry: dict[str, int] = {}
    queue_score_by_entry: dict[str, float] = {}
    if active_learning_queue:
        for row in active_learning_queue.get("rows", []):
            if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
                continue
            entry_id = str(row["entry_id"])
            queue_rank_by_entry[entry_id] = int(row.get("rank", 0) or 0)
            queue_score_by_entry[entry_id] = float(row.get("review_score", 0.0) or 0.0)
    baseline_meta = (baseline_review_debt or {}).get("metadata", {})
    baseline_debt_ids = {
        str(entry_id)
        for entry_id in baseline_meta.get("review_debt_entry_ids", [])
        if isinstance(entry_id, str)
    } or {
        str(row.get("entry_id"))
        for row in (baseline_review_debt or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    debt_rows: list[dict[str, Any]] = []
    for row in review_evidence_gaps.get("rows", []):
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        gap_reasons = [str(reason) for reason in row.get("gap_reasons", [])]
        action = str(row.get("decision_action", ""))
        if action != "mark_needs_more_evidence" and not gap_reasons:
            continue
        entry_id = str(row["entry_id"])
        coverage_status = str(row.get("coverage_status", "unknown"))
        priority_score = _review_debt_priority_score(
            gap_reasons,
            coverage_status,
            queue_rank_by_entry.get(entry_id),
        )
        debt_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "priority_score": round(priority_score, 4),
                "active_queue_rank": queue_rank_by_entry.get(entry_id),
                "active_queue_review_score": (
                    round(queue_score_by_entry[entry_id], 4)
                    if entry_id in queue_score_by_entry
                    else None
                ),
                "debt_status": (
                    "carried" if entry_id in baseline_debt_ids else "new"
                )
                if baseline_review_debt
                else None,
                "decision_action": action,
                "coverage_status": coverage_status,
                "gap_reasons": sorted(set(gap_reasons)),
                "counterevidence_reasons": row.get("counterevidence_reasons", []),
                "target_fingerprint_id": row.get("target_fingerprint_id"),
                "top1_fingerprint_id": row.get("top1_fingerprint_id"),
                "top1_score": row.get("top1_score"),
                "target_score": row.get("target_score"),
                "recommended_next_action": _review_debt_next_action(
                    gap_reasons,
                    coverage_status,
                ),
            }
        )
    ranked_rows = sorted(
        debt_rows,
        key=lambda row: (-float(row["priority_score"]), _entry_id_sort_key(row["entry_id"])),
    )
    gap_reason_counts = Counter(reason for row in debt_rows for reason in row["gap_reasons"])
    coverage_counts = Counter(str(row["coverage_status"]) for row in debt_rows)
    next_action_counts = Counter(str(row["recommended_next_action"]) for row in debt_rows)
    debt_status_counts = Counter(
        str(row["debt_status"]) for row in debt_rows if row["debt_status"] is not None
    )
    next_action_counts_by_status: dict[str, dict[str, int]] = {}
    for status in ("carried", "new"):
        status_counts = Counter(
            str(row["recommended_next_action"])
            for row in debt_rows
            if row.get("debt_status") == status
        )
        if status_counts:
            next_action_counts_by_status[status] = dict(sorted(status_counts.items()))
    debt_entry_ids = sorted(
        (str(row["entry_id"]) for row in debt_rows),
        key=_entry_id_sort_key,
    )
    carried_debt_entry_ids = sorted(
        (
            str(row["entry_id"])
            for row in debt_rows
            if row.get("debt_status") == "carried"
        ),
        key=_entry_id_sort_key,
    )
    new_debt_entry_ids = sorted(
        (
            str(row["entry_id"])
            for row in debt_rows
            if row.get("debt_status") == "new"
        ),
        key=_entry_id_sort_key,
    )
    return {
        "metadata": {
            "method": "review_debt_summary",
            "source_method": review_evidence_gaps.get("metadata", {}).get("method"),
            "review_debt_count": len(debt_rows),
            "review_debt_entry_ids": debt_entry_ids,
            "carried_review_debt_entry_ids": carried_debt_entry_ids,
            "new_review_debt_entry_ids": new_debt_entry_ids,
            "needs_more_evidence_count": sum(
                1 for row in debt_rows if row["decision_action"] == "mark_needs_more_evidence"
            ),
            "prioritized_count": min(max_rows, len(ranked_rows)),
            "gap_reason_counts": dict(sorted(gap_reason_counts.items())),
            "coverage_status_counts": dict(sorted(coverage_counts.items())),
            "recommended_next_action_counts": dict(sorted(next_action_counts.items())),
            "debt_status_counts": dict(sorted(debt_status_counts.items())),
            "recommended_next_action_counts_by_debt_status": next_action_counts_by_status,
            "new_review_debt_count": debt_status_counts.get("new", 0),
            "carried_review_debt_count": debt_status_counts.get("carried", 0),
            "active_queue_rows_linked": sum(
                1 for row in debt_rows if row["active_queue_rank"] is not None
            ),
            "triage_rule": (
                "prioritize review debt with local/structure-wide cofactor gaps, "
                "counterevidence, below-threshold retrieval, family mismatches, and "
                "high active-learning rank"
            ),
        },
        "rows": ranked_rows[:max_rows],
    }


def analyze_review_debt_remediation(
    review_debt: dict[str, Any],
    review_evidence_gaps: dict[str, Any],
    *,
    graph: dict[str, Any] | None = None,
    geometry: dict[str, Any] | None = None,
    debt_status: str = "new",
    max_rows: int | None = None,
) -> dict[str, Any]:
    """Plan concrete follow-up checks for review-debt rows without counting labels."""
    if debt_status not in {"new", "carried", "all"}:
        raise ValueError("debt_status must be one of: new, carried, all")

    debt_meta = review_debt.get("metadata", {})
    new_ids = _sorted_entry_ids(debt_meta.get("new_review_debt_entry_ids", []))
    carried_ids = _sorted_entry_ids(debt_meta.get("carried_review_debt_entry_ids", []))
    all_ids = _sorted_entry_ids(debt_meta.get("review_debt_entry_ids", []))
    if not all_ids:
        all_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in review_debt.get("rows", [])
            if isinstance(row, dict)
        )
    if debt_status == "new":
        selected_ids = new_ids
    elif debt_status == "carried":
        selected_ids = carried_ids
    else:
        selected_ids = all_ids

    selected_set = set(selected_ids)
    debt_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in review_debt.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    gap_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in review_evidence_gaps.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    graph_context_by_entry = _review_debt_graph_context_by_entry(graph)
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in (geometry or {}).get("entries", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for entry_id in selected_ids:
        gap_row = gap_rows_by_entry.get(entry_id, {"entry_id": entry_id})
        debt_row = debt_rows_by_entry.get(entry_id, {})
        graph_context = graph_context_by_entry.get(entry_id, {})
        geometry_row = geometry_by_entry.get(entry_id, {})
        gap_reasons = [str(reason) for reason in gap_row.get("gap_reasons", [])]
        coverage_status = str(gap_row.get("coverage_status", "unknown"))
        priority_score = debt_row.get("priority_score")
        if priority_score is None:
            priority_score = _review_debt_priority_score(
                gap_reasons,
                coverage_status,
                debt_row.get("active_queue_rank"),
            )
        selected_pdb_id = geometry_row.get("pdb_id")
        pdb_structure_ids = graph_context.get("pdb_structure_ids", [])
        alternate_pdb_ids = [
            pdb_id for pdb_id in pdb_structure_ids if pdb_id != selected_pdb_id
        ]
        residue_position_counts = graph_context.get("pdb_residue_position_counts", {})
        residue_positions = graph_context.get("pdb_residue_positions", {})
        candidate_position_counts = {
            pdb_id: int(residue_position_counts.get(pdb_id, 0) or 0)
            for pdb_id in pdb_structure_ids
        }
        alternate_position_counts = {
            pdb_id: int(residue_position_counts.get(pdb_id, 0) or 0)
            for pdb_id in alternate_pdb_ids
        }
        expected_families = _sorted_strings(gap_row.get("expected_cofactor_families", []))
        local_families = _sorted_strings(gap_row.get("local_cofactor_families", []))
        structure_families = _sorted_strings(
            gap_row.get("structure_cofactor_families", [])
        )
        row = {
            "entry_id": entry_id,
            "entry_name": gap_row.get("entry_name") or debt_row.get("entry_name"),
            "debt_status": _review_debt_status(entry_id, new_ids, carried_ids),
            "priority_score": round(float(priority_score or 0.0), 4),
            "recommended_next_action": debt_row.get("recommended_next_action")
            or _review_debt_next_action(gap_reasons, coverage_status),
            "remediation_bucket": _review_debt_remediation_bucket(
                gap_reasons,
                coverage_status,
                geometry_row=geometry_row,
                alternate_pdb_count=len(alternate_pdb_ids),
            ),
            "coverage_status": coverage_status,
            "gap_reasons": sorted(set(gap_reasons)),
            "counterevidence_reasons": gap_row.get("counterevidence_reasons", []),
            "target_fingerprint_id": gap_row.get("target_fingerprint_id"),
            "top1_fingerprint_id": gap_row.get("top1_fingerprint_id"),
            "top1_score": gap_row.get("top1_score"),
            "target_score": gap_row.get("target_score"),
            "expected_cofactor_families": expected_families,
            "local_cofactor_families": local_families,
            "structure_cofactor_families": structure_families,
            "matching_structure_ligands": gap_row.get("matching_structure_ligands", []),
            "nearest_expected_ligand_distance_angstrom": gap_row.get(
                "nearest_expected_ligand_distance_angstrom"
            ),
            "proximal_ligand_codes": _sorted_strings(gap_row.get("proximal_ligand_codes", [])),
            "structure_ligand_codes": _sorted_strings(gap_row.get("structure_ligand_codes", [])),
            "selected_pdb_id": selected_pdb_id,
            "geometry_status": geometry_row.get("status"),
            "resolved_residue_count": geometry_row.get("resolved_residue_count"),
            "missing_positions": geometry_row.get("missing_positions"),
            "reference_uniprot_ids": graph_context.get("reference_uniprot_ids", []),
            "candidate_pdb_structure_count": len(pdb_structure_ids),
            "candidate_pdb_structure_ids": pdb_structure_ids,
            "candidate_pdb_residue_position_counts": candidate_position_counts,
            "candidate_pdb_residue_positions": {
                pdb_id: residue_positions.get(pdb_id, [])
                for pdb_id in pdb_structure_ids
                if residue_positions.get(pdb_id)
            },
            "candidate_pdb_with_residue_positions_count": sum(
                1 for count in candidate_position_counts.values() if count > 0
            ),
            "alternate_pdb_count": len(alternate_pdb_ids),
            "alternate_pdb_ids": alternate_pdb_ids,
            "alternate_pdb_residue_position_counts": alternate_position_counts,
            "alternate_pdb_with_residue_positions_count": sum(
                1 for count in alternate_position_counts.values() if count > 0
            ),
            "selected_pdb_residue_position_count": int(
                residue_position_counts.get(str(selected_pdb_id), 0) or 0
            )
            if selected_pdb_id
            else 0,
            "alphafold_structure_ids": graph_context.get("alphafold_structure_ids", []),
            "cofactor_gap_requires_local_evidence": bool(
                set(expected_families) - set(local_families)
            ),
            "selected_structure_has_expected_family": bool(
                set(expected_families) & set(structure_families)
            ),
            "selected_active_site_has_expected_family": bool(
                set(expected_families) & set(local_families)
            ),
        }
        rows.append(row)

    ranked_rows = sorted(
        rows,
        key=lambda row: (-float(row["priority_score"]), _entry_id_sort_key(row["entry_id"])),
    )
    if max_rows is not None and max_rows > 0:
        output_rows = ranked_rows[:max_rows]
    else:
        output_rows = ranked_rows

    missing_gap_ids = sorted(selected_set - set(gap_rows_by_entry), key=_entry_id_sort_key)
    missing_graph_ids = sorted(
        (
            row["entry_id"]
            for row in ranked_rows
            if not row["reference_uniprot_ids"] and not row["candidate_pdb_structure_ids"]
        ),
        key=_entry_id_sort_key,
    )
    missing_geometry_ids = sorted(
        (row["entry_id"] for row in ranked_rows if row["geometry_status"] is None),
        key=_entry_id_sort_key,
    )
    remediation_counts = Counter(str(row["remediation_bucket"]) for row in ranked_rows)
    coverage_counts = Counter(str(row["coverage_status"]) for row in ranked_rows)
    gap_reason_counts = Counter(reason for row in ranked_rows for reason in row["gap_reasons"])
    expected_family_counts = Counter(
        family for row in ranked_rows for family in row["expected_cofactor_families"]
    )
    structure_availability_counts = Counter(
        _review_debt_structure_availability(row) for row in ranked_rows
    )
    alternate_position_gap_entry_ids = sorted(
        (
            row["entry_id"]
            for row in ranked_rows
            if int(row.get("alternate_pdb_count", 0) or 0) > 0
            and int(row.get("alternate_pdb_with_residue_positions_count", 0) or 0) == 0
        ),
        key=_entry_id_sort_key,
    )
    selected_position_gap_entry_ids = sorted(
        (
            row["entry_id"]
            for row in ranked_rows
            if row.get("selected_pdb_id")
            and int(row.get("selected_pdb_residue_position_count", 0) or 0) == 0
        ),
        key=_entry_id_sort_key,
    )

    return {
        "metadata": {
            "method": "review_debt_remediation_plan",
            "source_review_debt_method": debt_meta.get("method"),
            "source_review_gap_method": review_evidence_gaps.get("metadata", {}).get("method"),
            "debt_status_filter": debt_status,
            "requested_entry_count": len(selected_ids),
            "emitted_row_count": len(output_rows),
            "all_requested_entries_have_gap_detail": not missing_gap_ids,
            "missing_gap_detail_entry_ids": missing_gap_ids,
            "missing_graph_context_entry_ids": missing_graph_ids,
            "missing_geometry_entry_ids": missing_geometry_ids,
            "remediation_bucket_counts": dict(sorted(remediation_counts.items())),
            "coverage_status_counts": dict(sorted(coverage_counts.items())),
            "gap_reason_counts": dict(sorted(gap_reason_counts.items())),
            "expected_cofactor_family_counts": dict(sorted(expected_family_counts.items())),
            "structure_availability_counts": dict(
                sorted(structure_availability_counts.items())
            ),
            "alternate_pdb_position_gap_entry_count": len(
                alternate_position_gap_entry_ids
            ),
            "alternate_pdb_position_gap_entry_ids": alternate_position_gap_entry_ids,
            "selected_pdb_position_gap_entry_count": len(
                selected_position_gap_entry_ids
            ),
            "selected_pdb_position_gap_entry_ids": selected_position_gap_entry_ids,
            "new_review_debt_entry_ids": new_ids,
            "carried_review_debt_entry_ids": carried_ids,
            "triage_rule": (
                "keep review-debt rows out of the countable benchmark; inspect "
                "selected-structure cofactor gaps against alternate PDB availability, "
                "active-site mapping status, and graph reference-protein context before "
                "promoting any additional labels"
            ),
        },
        "rows": output_rows,
    }


def scan_review_debt_alternate_structures(
    remediation_plan: dict[str, Any],
    *,
    max_entries: int = 5,
    max_structures_per_entry: int = 6,
    cif_fetcher=fetch_pdb_cif,
    inventory_by_pdb: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if max_entries < 1:
        raise ValueError("max_entries must be positive")
    if max_structures_per_entry < 1:
        raise ValueError("max_structures_per_entry must be positive")

    scan_buckets = {
        "alternate_pdb_ligand_scan",
        "local_mapping_or_structure_selection_review",
    }
    candidate_rows = [
        row
        for row in remediation_plan.get("rows", [])
        if isinstance(row, dict) and row.get("remediation_bucket") in scan_buckets
    ]
    selected_rows = candidate_rows[:max_entries]
    inventory_cache: dict[str, dict[str, Any]] = {
        str(pdb_id).upper(): dict(inventory)
        for pdb_id, inventory in (inventory_by_pdb or {}).items()
    }
    output_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = []

    for row in selected_rows:
        entry_id = str(row.get("entry_id"))
        selected_pdb_id = str(row.get("selected_pdb_id") or "").upper()
        candidate_pdb_ids = _review_debt_scan_pdb_ids(row)
        residue_position_counts = {
            str(pdb_id).upper(): int(count or 0)
            for pdb_id, count in (
                row.get("candidate_pdb_residue_position_counts", {}) or {}
            ).items()
        }
        residue_positions_by_pdb = {
            str(pdb_id).upper(): positions
            for pdb_id, positions in (
                row.get("candidate_pdb_residue_positions", {}) or {}
            ).items()
            if isinstance(positions, list)
        }
        scanned_pdb_ids = candidate_pdb_ids[:max_structures_per_entry]
        unscanned_pdb_ids = candidate_pdb_ids[max_structures_per_entry:]
        expected_families = set(_sorted_strings(row.get("expected_cofactor_families", [])))
        structure_hits: list[dict[str, Any]] = []
        for pdb_id in scanned_pdb_ids:
            atoms: list[dict[str, Any]] | None = None
            remap_result: dict[str, Any] = {
                "positions": [],
                "basis": None,
                "warnings": [],
            }
            try:
                inventory = inventory_cache.get(pdb_id)
                if inventory is None:
                    atoms = parse_atom_site_loop(cif_fetcher(pdb_id))
                    inventory = structure_ligand_inventory_from_atoms(atoms)
                    inventory_cache[pdb_id] = inventory
            except Exception as exc:  # network/source errors become artifact evidence
                failure = {
                    "entry_id": entry_id,
                    "pdb_id": pdb_id,
                    "error": str(exc),
                }
                fetch_failures.append(failure)
                structure_hits.append(
                    {
                        "pdb_id": pdb_id,
                        "fetch_error": str(exc),
                        "ligand_codes": [],
                        "cofactor_families": [],
                        "expected_family_hits": [],
                        "is_selected_structure": pdb_id == selected_pdb_id,
                        "residue_position_count": int(
                            residue_position_counts.get(pdb_id, 0) or 0
                        ),
                        "usable_residue_position_count": int(
                            residue_position_counts.get(pdb_id, 0) or 0
                        ),
                        "remapped_residue_position_count": 0,
                        "residue_position_source": (
                            "mcsa_explicit"
                            if int(residue_position_counts.get(pdb_id, 0) or 0) > 0
                            else "none"
                        ),
                        "residue_position_remap_basis": None,
                        "residue_position_remap_warnings": [],
                    }
                )
                continue
            families = set(_sorted_strings(inventory.get("cofactor_families", [])))
            expected_hits = sorted(expected_families & families)
            local_positions_by_pdb = residue_positions_by_pdb
            explicit_position_count = int(residue_position_counts.get(pdb_id, 0) or 0)
            if explicit_position_count == 0:
                if atoms is None and _review_debt_reference_residue_positions(
                    residue_positions_by_pdb,
                    selected_pdb_id,
                ):
                    try:
                        atoms = parse_atom_site_loop(cif_fetcher(pdb_id))
                    except Exception as exc:
                        remap_result = {
                            "positions": [],
                            "basis": None,
                            "warnings": [f"residue_remap_fetch_failed:{exc}"],
                        }
                if atoms is not None:
                    remap_result = _review_debt_infer_residue_positions(
                        atoms,
                        residue_positions_by_pdb,
                        selected_pdb_id=selected_pdb_id,
                    )
                    if remap_result.get("positions"):
                        local_positions_by_pdb = {
                            **residue_positions_by_pdb,
                            pdb_id: list(remap_result.get("positions", [])),
                        }
            local_context = _review_debt_local_ligand_context(
                atoms,
                pdb_id,
                local_positions_by_pdb,
                cif_fetcher=cif_fetcher,
                inventory_cache=inventory_cache,
            )
            local_families = set(
                _sorted_strings(local_context.get("cofactor_families", []))
            )
            local_expected_hits = sorted(expected_families & local_families)
            remapped_position_count = len(remap_result.get("positions", []) or [])
            residue_position_source = "none"
            if explicit_position_count > 0:
                residue_position_source = "mcsa_explicit"
            elif remapped_position_count > 0:
                residue_position_source = "selected_position_remap"
            structure_hits.append(
                {
                    "pdb_id": pdb_id,
                    "ligand_codes": _sorted_strings(inventory.get("ligand_codes", [])),
                    "cofactor_families": sorted(families),
                    "expected_family_hits": expected_hits,
                    "local_ligand_codes": _sorted_strings(
                        local_context.get("ligand_codes", [])
                    ),
                    "local_cofactor_families": sorted(local_families),
                    "local_expected_family_hits": local_expected_hits,
                    "local_resolved_residue_count": local_context.get(
                        "resolved_residue_count"
                    ),
                    "is_selected_structure": pdb_id == selected_pdb_id,
                    "residue_position_count": int(
                        residue_position_counts.get(pdb_id, 0) or 0
                    ),
                    "usable_residue_position_count": (
                        explicit_position_count or remapped_position_count
                    ),
                    "remapped_residue_position_count": remapped_position_count,
                    "residue_position_source": residue_position_source,
                    "residue_position_remap_basis": remap_result.get("basis"),
                    "residue_position_remap_warnings": remap_result.get("warnings", []),
                }
            )
        selected_hit = any(
            hit.get("is_selected_structure") and hit.get("expected_family_hits")
            for hit in structure_hits
        )
        alternate_hit = any(
            not hit.get("is_selected_structure") and hit.get("expected_family_hits")
            for hit in structure_hits
        )
        local_hit = any(hit.get("local_expected_family_hits") for hit in structure_hits)
        remapped_hit = any(
            hit.get("local_expected_family_hits")
            and hit.get("residue_position_source") == "selected_position_remap"
            for hit in structure_hits
        )
        output_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "remediation_bucket": row.get("remediation_bucket"),
                "expected_cofactor_families": sorted(expected_families),
                "selected_pdb_id": selected_pdb_id or None,
                "candidate_pdb_count": len(candidate_pdb_ids),
                "selected_structure_has_expected_family": bool(
                    row.get("selected_structure_has_expected_family")
                ),
                "selected_active_site_has_expected_family": bool(
                    row.get("selected_active_site_has_expected_family")
                ),
                "alternate_pdb_with_residue_positions_count": int(
                    row.get("alternate_pdb_with_residue_positions_count", 0) or 0
                ),
                "scanned_pdb_ids": scanned_pdb_ids,
                "unscanned_pdb_ids": unscanned_pdb_ids,
                "scanned_pdb_residue_position_counts": {
                    pdb_id: int(residue_position_counts.get(pdb_id, 0) or 0)
                    for pdb_id in scanned_pdb_ids
                },
                "scanned_pdb_remapped_residue_position_counts": {
                    pdb_id: sum(
                        int(hit.get("remapped_residue_position_count", 0) or 0)
                        for hit in structure_hits
                        if hit.get("pdb_id") == pdb_id
                    )
                    for pdb_id in scanned_pdb_ids
                },
                "scanned_pdb_usable_residue_position_counts": {
                    pdb_id: sum(
                        int(hit.get("usable_residue_position_count", 0) or 0)
                        for hit in structure_hits
                        if hit.get("pdb_id") == pdb_id
                    )
                    for pdb_id in scanned_pdb_ids
                },
                "structure_hits": structure_hits,
                "selected_structure_expected_family_observed": bool(selected_hit),
                "alternate_structure_expected_family_observed": bool(alternate_hit),
                "local_active_site_expected_family_observed": bool(local_hit),
                "local_active_site_expected_family_observed_from_remap": bool(
                    remapped_hit
                ),
                "alternate_pdb_with_remapped_positions_count": sum(
                    1
                    for hit in structure_hits
                    if not hit.get("is_selected_structure")
                    and int(hit.get("remapped_residue_position_count", 0) or 0) > 0
                ),
                "scan_outcome": _review_debt_scan_outcome(
                    selected_hit=bool(selected_hit),
                    alternate_hit=bool(alternate_hit),
                    candidate_pdb_count=len(candidate_pdb_ids),
                    unscanned_pdb_count=len(unscanned_pdb_ids),
                ),
            }
        )

    outcome_counts = Counter(str(row["scan_outcome"]) for row in output_rows)
    expected_hit_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if row["selected_structure_expected_family_observed"]
            or row["alternate_structure_expected_family_observed"]
        ),
        key=_entry_id_sort_key,
    )
    structure_wide_hit_only_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if (
                row["selected_structure_expected_family_observed"]
                or row["alternate_structure_expected_family_observed"]
            )
            and not row["local_active_site_expected_family_observed"]
        ),
        key=_entry_id_sort_key,
    )
    local_hit_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if row["local_active_site_expected_family_observed"]
        ),
        key=_entry_id_sort_key,
    )
    remapped_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if any(
                int(hit.get("remapped_residue_position_count", 0) or 0) > 0
                for hit in row.get("structure_hits", [])
            )
        ),
        key=_entry_id_sort_key,
    )
    alternate_remapped_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if int(row.get("alternate_pdb_with_remapped_positions_count", 0) or 0) > 0
        ),
        key=_entry_id_sort_key,
    )
    remapped_local_hit_entry_ids = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if row.get("local_active_site_expected_family_observed_from_remap")
        ),
        key=_entry_id_sort_key,
    )
    remap_basis_counts = Counter(
        str(hit.get("residue_position_remap_basis"))
        for row in output_rows
        for hit in row.get("structure_hits", [])
        if int(hit.get("remapped_residue_position_count", 0) or 0) > 0
        and hit.get("residue_position_remap_basis")
    )
    remap_warning_counts = Counter(
        str(warning)
        for row in output_rows
        for hit in row.get("structure_hits", [])
        for warning in hit.get("residue_position_remap_warnings", [])
        if warning
    )
    alternate_without_usable_positions = sorted(
        (
            row["entry_id"]
            for row in output_rows
            if any(
                not hit.get("is_selected_structure")
                for hit in row.get("structure_hits", [])
            )
            and not any(
                not hit.get("is_selected_structure")
                and int(hit.get("usable_residue_position_count", 0) or 0) > 0
                for hit in row.get("structure_hits", [])
            )
        ),
        key=_entry_id_sort_key,
    )
    return {
        "metadata": {
            "method": "review_debt_alternate_structure_scan",
            "source_method": remediation_plan.get("metadata", {}).get("method"),
            "candidate_entry_count": len(candidate_rows),
            "scanned_entry_count": len(output_rows),
            "unscanned_candidate_entry_count": max(0, len(candidate_rows) - len(output_rows)),
            "max_entries": max_entries,
            "max_structures_per_entry": max_structures_per_entry,
            "scanned_structure_count": sum(len(row["scanned_pdb_ids"]) for row in output_rows),
            "unscanned_structure_count": sum(
                len(row["unscanned_pdb_ids"]) for row in output_rows
            ),
            "all_candidate_structures_scanned": all(
                not row["unscanned_pdb_ids"] for row in output_rows
            )
            and len(candidate_rows) == len(output_rows),
            "fetch_failure_count": len(fetch_failures),
            "fetch_failures": fetch_failures,
            "expected_family_hit_entry_ids": expected_hit_entry_ids,
            "local_expected_family_hit_entry_ids": local_hit_entry_ids,
            "remapped_residue_position_entry_ids": remapped_entry_ids,
            "alternate_pdb_remapped_residue_position_entry_ids": (
                alternate_remapped_entry_ids
            ),
            "local_expected_family_hit_from_remap_entry_ids": (
                remapped_local_hit_entry_ids
            ),
            "remapped_residue_position_structure_count": sum(
                1
                for row in output_rows
                for hit in row.get("structure_hits", [])
                if int(hit.get("remapped_residue_position_count", 0) or 0) > 0
            ),
            "alternate_pdb_remapped_residue_position_structure_count": sum(
                int(row.get("alternate_pdb_with_remapped_positions_count", 0) or 0)
                for row in output_rows
            ),
            "residue_position_remap_basis_counts": dict(
                sorted(remap_basis_counts.items())
            ),
            "residue_position_remap_warning_counts": dict(
                sorted(remap_warning_counts.items())
            ),
            "alternate_pdb_without_usable_residue_position_entry_count": len(
                alternate_without_usable_positions
            ),
            "alternate_pdb_without_usable_residue_position_entry_ids": (
                alternate_without_usable_positions
            ),
            "structure_wide_hit_without_local_support_entry_ids": (
                structure_wide_hit_only_entry_ids
            ),
            "scan_outcome_counts": dict(sorted(outcome_counts.items())),
            "scan_rule": (
                "bounded structure-wide ligand scan for selected high-priority "
                "review-debt rows; hits are cofactor-source evidence for review, "
                "not countable label acceptance"
            ),
        },
        "rows": output_rows,
    }


def summarize_review_debt_remap_leads(
    alternate_structure_scan: dict[str, Any],
    *,
    remediation_plan: dict[str, Any] | None = None,
    review_evidence_gaps: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Summarize review-only alternate-structure remap leads."""
    remediation_by_entry = {
        str(row.get("entry_id")): row
        for row in (remediation_plan or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    gap_by_entry = {
        str(row.get("entry_id")): row
        for row in (review_evidence_gaps or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for row in alternate_structure_scan.get("rows", []):
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        entry_id = str(row["entry_id"])
        hits = [hit for hit in row.get("structure_hits", []) if isinstance(hit, dict)]
        local_hits = [hit for hit in hits if hit.get("local_expected_family_hits")]
        remapped_hits = [
            hit
            for hit in hits
            if int(hit.get("remapped_residue_position_count", 0) or 0) > 0
        ]
        remapped_local_hits = [
            hit
            for hit in local_hits
            if hit.get("residue_position_source") == "selected_position_remap"
        ]
        structure_wide_only_hits = [
            hit
            for hit in hits
            if hit.get("expected_family_hits") and not hit.get("local_expected_family_hits")
        ]
        if not (local_hits or remapped_hits or structure_wide_only_hits):
            continue

        remediation_row = remediation_by_entry.get(entry_id, {})
        gap_row = gap_by_entry.get(entry_id, {})
        if remapped_local_hits:
            lead_type = "local_expected_family_hit_from_remap"
            recommended_action = "verify_remapped_local_evidence_before_review_import"
        elif local_hits:
            lead_type = "local_expected_family_hit"
            recommended_action = "verify_local_evidence_before_review_import"
        elif structure_wide_only_hits:
            lead_type = "structure_wide_hit_without_local_support"
            recommended_action = "inspect_active_site_mapping_or_structure_selection"
        else:
            lead_type = "remapped_positions_without_expected_family_hit"
            recommended_action = "use_remapped_positions_for_next_local_evidence_scan"

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name")
                or remediation_row.get("entry_name")
                or gap_row.get("entry_name"),
                "lead_type": lead_type,
                "recommended_next_action": recommended_action,
                "countable_label_candidate": False,
                "review_policy": (
                    "alternate-structure remaps and ligand hits are review-only; "
                    "do not count labels until review import and factory gates "
                    "clear unresolved evidence gaps"
                ),
                "debt_status": remediation_row.get("debt_status"),
                "remediation_bucket": row.get("remediation_bucket")
                or remediation_row.get("remediation_bucket"),
                "coverage_status": remediation_row.get("coverage_status")
                or gap_row.get("coverage_status"),
                "gap_reasons": remediation_row.get("gap_reasons")
                or gap_row.get("gap_reasons", []),
                "expected_cofactor_families": _sorted_strings(
                    row.get("expected_cofactor_families", [])
                ),
                "local_expected_family_hit_pdb_ids": _sorted_strings(
                    hit.get("pdb_id") for hit in local_hits
                ),
                "local_expected_family_hit_from_remap_pdb_ids": _sorted_strings(
                    hit.get("pdb_id") for hit in remapped_local_hits
                ),
                "structure_wide_hit_without_local_support_pdb_ids": _sorted_strings(
                    hit.get("pdb_id") for hit in structure_wide_only_hits
                ),
                "remapped_residue_position_pdb_ids": _sorted_strings(
                    hit.get("pdb_id") for hit in remapped_hits
                ),
                "remapped_residue_position_structure_count": len(remapped_hits),
                "remap_basis_counts": dict(
                    sorted(
                        Counter(
                            str(hit.get("residue_position_remap_basis"))
                            for hit in remapped_hits
                            if hit.get("residue_position_remap_basis")
                        ).items()
                    )
                ),
                "local_ligand_codes": _sorted_strings(
                    code
                    for hit in local_hits
                    for code in hit.get("local_ligand_codes", [])
                ),
                "local_expected_ligand_codes": _ligand_codes_matching_families(
                    (
                        code
                        for hit in local_hits
                        for code in hit.get("local_ligand_codes", [])
                    ),
                    row.get("expected_cofactor_families", []),
                ),
                "local_cofactor_families": _sorted_strings(
                    family
                    for hit in local_hits
                    for family in hit.get("local_cofactor_families", [])
                ),
                "structure_ligand_codes": _sorted_strings(
                    code for hit in hits for code in hit.get("ligand_codes", [])
                ),
                "structure_expected_ligand_codes": _ligand_codes_matching_families(
                    (code for hit in hits for code in hit.get("ligand_codes", [])),
                    row.get("expected_cofactor_families", []),
                ),
                "hit_summaries": [
                    {
                        "pdb_id": hit.get("pdb_id"),
                        "is_selected_structure": bool(hit.get("is_selected_structure")),
                        "residue_position_source": hit.get("residue_position_source"),
                        "residue_position_remap_basis": hit.get(
                            "residue_position_remap_basis"
                        ),
                        "usable_residue_position_count": int(
                            hit.get("usable_residue_position_count", 0) or 0
                        ),
                        "remapped_residue_position_count": int(
                            hit.get("remapped_residue_position_count", 0) or 0
                        ),
                        "expected_family_hits": _sorted_strings(
                            hit.get("expected_family_hits", [])
                        ),
                        "local_expected_family_hits": _sorted_strings(
                            hit.get("local_expected_family_hits", [])
                        ),
                        "local_ligand_codes": _sorted_strings(
                            hit.get("local_ligand_codes", [])
                        ),
                    }
                    for hit in hits
                    if hit.get("expected_family_hits")
                    or hit.get("local_expected_family_hits")
                    or int(hit.get("remapped_residue_position_count", 0) or 0) > 0
                ],
            }
        )

    lead_priority = {
        "local_expected_family_hit_from_remap": 0,
        "local_expected_family_hit": 1,
        "structure_wide_hit_without_local_support": 2,
        "remapped_positions_without_expected_family_hit": 3,
    }
    rows = sorted(
        rows,
        key=lambda row: (
            lead_priority.get(str(row.get("lead_type")), 99),
            _entry_id_sort_key(str(row.get("entry_id"))),
        ),
    )
    lead_type_counts = Counter(str(row.get("lead_type")) for row in rows)
    local_from_remap_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if row.get("lead_type") == "local_expected_family_hit_from_remap"
    )
    local_hit_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if str(row.get("lead_type")).startswith("local_expected_family_hit")
    )
    return {
        "metadata": {
            "method": "review_debt_remap_lead_summary",
            "source_scan_method": alternate_structure_scan.get("metadata", {}).get(
                "method"
            ),
            "lead_count": len(rows),
            "lead_type_counts": dict(sorted(lead_type_counts.items())),
            "local_expected_family_hit_entry_ids": local_hit_ids,
            "local_expected_family_hit_from_remap_entry_ids": local_from_remap_ids,
            "countable_label_candidate_count": 0,
            "review_rule": (
                "remapped local cofactor evidence can prioritize review but cannot "
                "make a label countable without review import, evidence-gap "
                "clearance, and label-factory gate acceptance"
            ),
        },
        "rows": rows,
    }


def audit_review_debt_remap_local_leads(
    remap_leads: dict[str, Any],
    *,
    remediation_plan: dict[str, Any] | None = None,
    review_evidence_gaps: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify remap-local evidence leads before any review import."""
    remediation_by_entry = {
        str(row.get("entry_id")): row
        for row in (remediation_plan or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    gap_by_entry = {
        str(row.get("entry_id")): row
        for row in (review_evidence_gaps or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for row in remap_leads.get("rows", []):
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        if row.get("lead_type") != "local_expected_family_hit_from_remap":
            continue

        entry_id = str(row["entry_id"])
        remediation_row = remediation_by_entry.get(entry_id, {})
        gap_row = gap_by_entry.get(entry_id, {})
        gap_reasons = _sorted_strings(
            row.get("gap_reasons")
            or remediation_row.get("gap_reasons")
            or gap_row.get("gap_reasons", [])
        )
        counterevidence_reasons = _sorted_strings(
            remediation_row.get("counterevidence_reasons", [])
        )
        counterevidence_present = (
            "counterevidence_present" in set(gap_reasons)
            or bool(counterevidence_reasons)
        )
        selected_active_site_has_expected_family = bool(
            remediation_row.get("selected_active_site_has_expected_family")
        )
        selected_structure_has_expected_family = bool(
            remediation_row.get("selected_structure_has_expected_family")
        )
        coverage_status = str(
            remediation_row.get("coverage_status")
            or row.get("coverage_status")
            or gap_row.get("coverage_status")
            or ""
        )
        top1_fingerprint_id = (
            remediation_row.get("top1_fingerprint_id") or gap_row.get("top1_fingerprint_id")
        )
        reaction_mismatch_reasons = _remap_local_reaction_substrate_mismatch_reasons(
            entry_name=str(
                row.get("entry_name")
                or remediation_row.get("entry_name")
                or gap_row.get("entry_name")
                or ""
            ),
            mechanism_text_snippets=gap_row.get("mechanism_text_snippets", []),
            top1_fingerprint_id=top1_fingerprint_id,
        )

        selected_structure_gap_reasons: list[str] = []
        if coverage_status == "expected_absent_from_structure":
            selected_structure_gap_reasons.append(
                "selected_structure_missing_expected_cofactor_family"
            )
        if not selected_active_site_has_expected_family:
            selected_structure_gap_reasons.append(
                "selected_active_site_expected_family_absent"
            )
        if not selected_structure_has_expected_family:
            selected_structure_gap_reasons.append(
                "selected_structure_expected_family_absent"
            )

        alternate_explicit_position_count = int(
            remediation_row.get("alternate_pdb_with_residue_positions_count", 0) or 0
        )
        local_hit_pdb_ids = _sorted_strings(
            row.get("local_expected_family_hit_pdb_ids", [])
        )
        remap_local_hit_pdb_ids = _sorted_strings(
            row.get("local_expected_family_hit_from_remap_pdb_ids", [])
        )
        all_local_hits_from_remap = bool(remap_local_hit_pdb_ids) and (
            local_hit_pdb_ids == remap_local_hit_pdb_ids
        )
        strict_remap_guardrail_required = (
            all_local_hits_from_remap and alternate_explicit_position_count == 0
        )

        if counterevidence_present:
            audit_decision = "expert_family_boundary_review_required"
            decision_reason = (
                "counterevidence remains after alternate-structure local remap hits"
            )
            recommended_resolution = "expert_review"
        elif reaction_mismatch_reasons:
            audit_decision = "expert_reaction_substrate_review_required"
            decision_reason = (
                "reaction or substrate text conflicts with the top ontology family"
            )
            recommended_resolution = "expert_review"
        elif selected_structure_gap_reasons:
            audit_decision = "local_structure_selection_rule_candidate"
            decision_reason = (
                "selected structure lacks expected local cofactor but alternate "
                "structures have remap-local expected-family hits"
            )
            recommended_resolution = "local_structure_selection_review"
        else:
            audit_decision = "stricter_remap_guardrail_required"
            decision_reason = (
                "remap-local evidence must be verified before review import"
            )
            recommended_resolution = "remap_evidence_verification"

        counting_blockers = set(gap_reasons)
        counting_blockers.add("review_marked_needs_more_evidence")
        if strict_remap_guardrail_required:
            counting_blockers.add("local_evidence_from_conservative_remap_only")
            counting_blockers.add("alternate_pdb_lacks_explicit_mcsa_positions")
        if selected_structure_gap_reasons:
            counting_blockers.update(selected_structure_gap_reasons)
        if counterevidence_present:
            counting_blockers.add("counterevidence_present")
        counting_blockers.update(reaction_mismatch_reasons)

        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name")
                or remediation_row.get("entry_name")
                or gap_row.get("entry_name"),
                "audit_decision": audit_decision,
                "decision_reason": decision_reason,
                "recommended_resolution": recommended_resolution,
                "countable_label_candidate": False,
                "counting_blockers": sorted(counting_blockers),
                "strict_remap_guardrail_required": strict_remap_guardrail_required,
                "selected_pdb_id": remediation_row.get("selected_pdb_id"),
                "selected_structure_gap_reasons": sorted(set(selected_structure_gap_reasons)),
                "selected_active_site_has_expected_family": (
                    selected_active_site_has_expected_family
                ),
                "selected_structure_has_expected_family": (
                    selected_structure_has_expected_family
                ),
                "alternate_pdb_with_explicit_residue_positions_count": (
                    alternate_explicit_position_count
                ),
                "candidate_pdb_with_explicit_residue_positions_count": int(
                    remediation_row.get(
                        "candidate_pdb_with_residue_positions_count", 0
                    )
                    or 0
                ),
                "local_expected_family_hit_from_remap_pdb_ids": (
                    remap_local_hit_pdb_ids
                ),
                "local_expected_family_hit_pdb_ids": local_hit_pdb_ids,
                "local_expected_ligand_codes": _sorted_strings(
                    row.get("local_expected_ligand_codes", [])
                ),
                "expected_cofactor_families": _sorted_strings(
                    row.get("expected_cofactor_families", [])
                ),
                "remap_basis_counts": dict(row.get("remap_basis_counts", {})),
                "remapped_residue_position_structure_count": int(
                    row.get("remapped_residue_position_structure_count", 0) or 0
                ),
                "counterevidence_present": counterevidence_present,
                "counterevidence_reasons": counterevidence_reasons,
                "reaction_substrate_mismatch_reasons": reaction_mismatch_reasons,
                "gap_reasons": gap_reasons,
                "target_fingerprint_id": remediation_row.get("target_fingerprint_id"),
                "target_score": remediation_row.get("target_score")
                if remediation_row.get("target_score") is not None
                else gap_row.get("target_score"),
                "top1_fingerprint_id": top1_fingerprint_id,
                "top1_score": remediation_row.get("top1_score")
                if remediation_row.get("top1_score") is not None
                else gap_row.get("top1_score"),
                "review_policy": (
                    "local expected-family hits from conservative alternate-PDB "
                    "residue remaps remain review-only; they cannot clear review "
                    "debt or count labels without explicit expert/import evidence "
                    "and a passing label-factory gate"
                ),
            }
        )

    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))
    decision_counts = Counter(str(row.get("audit_decision")) for row in rows)
    expert_review_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if row.get("audit_decision") == "expert_family_boundary_review_required"
    )
    structure_rule_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if row.get("audit_decision") == "local_structure_selection_rule_candidate"
    )
    expert_reaction_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if row.get("audit_decision") == "expert_reaction_substrate_review_required"
    )
    strict_guardrail_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in rows
        if row.get("strict_remap_guardrail_required")
    )
    return {
        "metadata": {
            "method": "review_debt_remap_local_lead_audit",
            "source_summary_method": remap_leads.get("metadata", {}).get("method"),
            "audited_entry_count": len(rows),
            "audited_entry_ids": _sorted_entry_ids(row.get("entry_id") for row in rows),
            "decision_counts": dict(sorted(decision_counts.items())),
            "expert_family_boundary_review_entry_ids": expert_review_ids,
            "expert_reaction_substrate_review_entry_ids": expert_reaction_ids,
            "local_structure_selection_rule_candidate_entry_ids": structure_rule_ids,
            "strict_remap_guardrail_entry_ids": strict_guardrail_ids,
            "countable_label_candidate_count": 0,
            "decision_rule": (
                "counterevidence routes remap-local leads to expert review; "
                "otherwise selected-structure cofactor absence makes them local "
                "structure-selection review candidates, with conservative remap "
                "evidence kept non-countable until explicit review/import evidence "
                "and factory gates clear"
            ),
        },
        "rows": rows,
    }


def audit_structure_selection_holo_preference(
    alternate_structure_scan: dict[str, Any],
    *,
    min_usable_residue_positions: int = 1,
    prefer_mcsa_explicit_over_remap: bool = True,
) -> dict[str, Any]:
    """Recommend reselecting the canonical reference PDB when the currently
    selected structure is apo for an expected cofactor family while at least
    one alternate PDB carries the family locally at the active site.

    Source data: a v3_review_debt_alternate_structure_scan_*.json artifact
    (per-entry list of candidate PDBs with local cofactor evidence). No
    network calls; no geometry-feature mutation. Recommendations are advisory
    and must be applied by a separate structure-reselection step, followed by
    geometry-feature regeneration for the affected entries.

    Decision rule: swap when (a) the selected structure lacks the expected
    cofactor family at the active site, (b) at least one alternate PDB has
    the expected family locally with usable residue positions >=
    min_usable_residue_positions, and (c) selection tiebreak prefers
    mcsa_explicit residue source over conservative remap when
    prefer_mcsa_explicit_over_remap=True.
    """
    rows: list[dict[str, Any]] = []
    swap_recommended_ids: list[str] = []
    already_holo_ids: list[str] = []
    no_holo_alternate_ids: list[str] = []
    no_expected_families_ids: list[str] = []
    residue_position_source_counts: dict[str, int] = {}

    for raw_row in alternate_structure_scan.get("rows", []):
        if not isinstance(raw_row, dict):
            continue
        entry_id = raw_row.get("entry_id")
        if not isinstance(entry_id, str):
            continue

        expected_families = set(
            _sorted_strings(raw_row.get("expected_cofactor_families", []))
        )
        current_selected_pdb_id = raw_row.get("selected_pdb_id")
        selected_active_site_has_expected_family = bool(
            raw_row.get("selected_active_site_has_expected_family")
        )
        selected_structure_has_expected_family = bool(
            raw_row.get("selected_structure_has_expected_family")
        )

        out_row: dict[str, Any] = {
            "entry_id": entry_id,
            "entry_name": raw_row.get("entry_name"),
            "expected_cofactor_families": sorted(expected_families),
            "current_selected_pdb_id": current_selected_pdb_id,
            "selected_active_site_has_expected_family": (
                selected_active_site_has_expected_family
            ),
            "selected_structure_has_expected_family": (
                selected_structure_has_expected_family
            ),
            "recommendation": "no_swap_no_holo_alternate",
            "recommendation_rationale": "",
            "recommended_pdb_id": None,
            "recommended_pdb_local_expected_family_hits": [],
            "recommended_pdb_local_ligand_codes": [],
            "recommended_pdb_local_resolved_residue_count": 0,
            "recommended_pdb_usable_residue_position_count": 0,
            "recommended_pdb_residue_position_source": None,
            "alternative_holo_candidate_count": 0,
            "alternative_holo_candidate_pdb_ids": [],
        }

        if not expected_families:
            out_row["recommendation"] = "no_swap_missing_expected_families"
            out_row["recommendation_rationale"] = (
                "Entry has no expected_cofactor_families recorded; nothing to prefer."
            )
            no_expected_families_ids.append(entry_id)
            rows.append(out_row)
            continue

        if selected_active_site_has_expected_family:
            out_row["recommendation"] = "no_swap_already_holo"
            out_row["recommendation_rationale"] = (
                f"Selected PDB {current_selected_pdb_id} already has expected "
                "cofactor family at active site; no swap needed."
            )
            already_holo_ids.append(entry_id)
            rows.append(out_row)
            continue

        structure_hits = raw_row.get("structure_hits") or []
        holo_candidates: list[dict[str, Any]] = []
        for hit in structure_hits:
            if not isinstance(hit, dict):
                continue
            if hit.get("is_selected_structure"):
                continue
            hit_families = set(
                _sorted_strings(hit.get("local_expected_family_hits", []))
            )
            if not hit_families & expected_families:
                continue
            usable_positions = int(hit.get("usable_residue_position_count", 0) or 0)
            if usable_positions < min_usable_residue_positions:
                continue
            holo_candidates.append(hit)

        out_row["alternative_holo_candidate_count"] = len(holo_candidates)
        out_row["alternative_holo_candidate_pdb_ids"] = sorted(
            str(h.get("pdb_id", "")) for h in holo_candidates if h.get("pdb_id")
        )

        if not holo_candidates:
            out_row["recommendation"] = "no_swap_no_holo_alternate"
            out_row["recommendation_rationale"] = (
                f"Selected PDB {current_selected_pdb_id} lacks expected cofactor "
                f"family {sorted(expected_families)} at active site, and no "
                "scanned alternate PDB provides it with sufficient residue "
                "support."
            )
            no_holo_alternate_ids.append(entry_id)
            rows.append(out_row)
            continue

        def _candidate_sort_key(hit: dict[str, Any]) -> tuple[int, int, int, str]:
            source = str(hit.get("residue_position_source") or "")
            local_resolved = int(hit.get("local_resolved_residue_count", 0) or 0)
            usable = int(hit.get("usable_residue_position_count", 0) or 0)
            pdb_id = str(hit.get("pdb_id") or "")
            if prefer_mcsa_explicit_over_remap:
                source_rank = 0 if source == "mcsa_explicit" else 1
                return (source_rank, -local_resolved, -usable, pdb_id)
            return (0, -local_resolved, -usable, pdb_id)

        best = sorted(holo_candidates, key=_candidate_sort_key)[0]
        best_pdb = str(best.get("pdb_id") or "")
        best_source = str(best.get("residue_position_source") or "")
        local_hits = _sorted_strings(best.get("local_expected_family_hits", []))
        local_ligands = _sorted_strings(best.get("local_ligand_codes", []))
        local_resolved = int(best.get("local_resolved_residue_count", 0) or 0)
        usable = int(best.get("usable_residue_position_count", 0) or 0)
        source_key = best_source or "unspecified"
        residue_position_source_counts[source_key] = (
            residue_position_source_counts.get(source_key, 0) + 1
        )
        swap_recommended_ids.append(entry_id)
        out_row.update(
            {
                "recommendation": "swap_selected_structure",
                "recommended_pdb_id": best_pdb,
                "recommended_pdb_local_expected_family_hits": local_hits,
                "recommended_pdb_local_ligand_codes": local_ligands,
                "recommended_pdb_local_resolved_residue_count": local_resolved,
                "recommended_pdb_usable_residue_position_count": usable,
                "recommended_pdb_residue_position_source": best_source or None,
                "recommendation_rationale": (
                    f"Selected PDB {current_selected_pdb_id} is apo for "
                    f"expected cofactor family {sorted(expected_families)} at "
                    f"active site. Alternate {best_pdb} carries local "
                    f"expected_family_hits={local_hits} with {usable} usable "
                    f"residue positions via {source_key} mapping. Recommend "
                    f"swapping the canonical reference structure to {best_pdb} "
                    "and regenerating geometry features for this entry."
                ),
            }
        )
        rows.append(out_row)

    rows.sort(key=lambda row: _entry_id_sort_key(str(row.get("entry_id", ""))))

    return {
        "metadata": {
            "method": "structure_selection_holo_preference_audit",
            "source_method": str(
                (alternate_structure_scan.get("metadata") or {}).get("method")
                or "review_debt_alternate_structure_scan"
            ),
            "min_usable_residue_positions": min_usable_residue_positions,
            "prefer_mcsa_explicit_over_remap": prefer_mcsa_explicit_over_remap,
            "audited_entry_count": len(rows),
            "swap_recommended_count": len(swap_recommended_ids),
            "swap_recommended_entry_ids": sorted(
                swap_recommended_ids, key=_entry_id_sort_key
            ),
            "already_holo_entry_count": len(already_holo_ids),
            "already_holo_entry_ids": sorted(already_holo_ids, key=_entry_id_sort_key),
            "no_holo_alternate_entry_count": len(no_holo_alternate_ids),
            "no_holo_alternate_entry_ids": sorted(
                no_holo_alternate_ids, key=_entry_id_sort_key
            ),
            "no_expected_cofactor_families_entry_count": len(no_expected_families_ids),
            "no_expected_cofactor_families_entry_ids": sorted(
                no_expected_families_ids, key=_entry_id_sort_key
            ),
            "swap_residue_position_source_counts": dict(
                sorted(residue_position_source_counts.items())
            ),
            "decision_rule": (
                "Recommend swapping the canonical reference PDB to a scanned "
                "alternate when (a) the selected structure lacks the expected "
                "cofactor family at the active site, (b) at least one alternate "
                "PDB has the expected family locally with usable residue "
                "positions >= min_usable_residue_positions, and (c) selection "
                "tiebreak prefers mcsa_explicit residue source over conservative "
                "remap when prefer_mcsa_explicit_over_remap=True. "
                "Recommendations are advisory; applying them requires "
                "regenerating geometry features and dependent label/audit "
                "artifacts for the affected entries."
            ),
        },
        "rows": rows,
    }


def summarize_review_debt_structure_selection_candidates(
    remap_local_lead_audit: dict[str, Any],
    alternate_structure_scan: dict[str, Any],
    *,
    remediation_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Summarize review-only local structure-selection candidates."""
    scan_by_entry = {
        str(row.get("entry_id")): row
        for row in alternate_structure_scan.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    remediation_by_entry = {
        str(row.get("entry_id")): row
        for row in (remediation_plan or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for audit_row in remap_local_lead_audit.get("rows", []):
        if not isinstance(audit_row, dict) or not isinstance(
            audit_row.get("entry_id"), str
        ):
            continue
        if audit_row.get("audit_decision") != "local_structure_selection_rule_candidate":
            continue
        entry_id = str(audit_row["entry_id"])
        scan_row = scan_by_entry.get(entry_id, {})
        remediation_row = remediation_by_entry.get(entry_id, {})
        candidate_pdb_ids = _sorted_strings(
            audit_row.get("local_expected_family_hit_from_remap_pdb_ids", [])
        )
        candidate_hits = [
            hit
            for hit in scan_row.get("structure_hits", [])
            if isinstance(hit, dict) and hit.get("pdb_id") in set(candidate_pdb_ids)
        ]
        candidate_summaries = [
            {
                "pdb_id": hit.get("pdb_id"),
                "residue_position_source": hit.get("residue_position_source"),
                "residue_position_remap_basis": hit.get(
                    "residue_position_remap_basis"
                ),
                "usable_residue_position_count": int(
                    hit.get("usable_residue_position_count", 0) or 0
                ),
                "remapped_residue_position_count": int(
                    hit.get("remapped_residue_position_count", 0) or 0
                ),
                "expected_family_hits": _sorted_strings(
                    hit.get("expected_family_hits", [])
                ),
                "local_expected_family_hits": _sorted_strings(
                    hit.get("local_expected_family_hits", [])
                ),
                "local_ligand_codes": _sorted_strings(hit.get("local_ligand_codes", [])),
                "structure_ligand_codes": _sorted_strings(hit.get("ligand_codes", [])),
            }
            for hit in candidate_hits
        ]
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": audit_row.get("entry_name")
                or remediation_row.get("entry_name")
                or scan_row.get("entry_name"),
                "selected_pdb_id": audit_row.get("selected_pdb_id")
                or remediation_row.get("selected_pdb_id")
                or scan_row.get("selected_pdb_id"),
                "selected_structure_gap_reasons": _sorted_strings(
                    audit_row.get("selected_structure_gap_reasons", [])
                ),
                "selected_active_site_has_expected_family": bool(
                    audit_row.get("selected_active_site_has_expected_family")
                ),
                "selected_structure_has_expected_family": bool(
                    audit_row.get("selected_structure_has_expected_family")
                ),
                "candidate_pdb_ids": candidate_pdb_ids,
                "candidate_hit_count": len(candidate_summaries),
                "candidate_hits": candidate_summaries,
                "candidate_local_ligand_codes": _sorted_strings(
                    code
                    for hit in candidate_summaries
                    for code in hit.get("local_ligand_codes", [])
                    if code
                ),
                "candidate_local_expected_ligand_codes": _ligand_codes_matching_families(
                    (
                        code
                        for hit in candidate_summaries
                        for code in hit.get("local_ligand_codes", [])
                    ),
                    audit_row.get("expected_cofactor_families", []),
                ),
                "expected_cofactor_families": _sorted_strings(
                    audit_row.get("expected_cofactor_families", [])
                ),
                "local_expected_ligand_codes": _sorted_strings(
                    audit_row.get("local_expected_ligand_codes", [])
                ),
                "alternate_pdb_with_explicit_residue_positions_count": int(
                    audit_row.get(
                        "alternate_pdb_with_explicit_residue_positions_count", 0
                    )
                    or 0
                ),
                "strict_remap_guardrail_required": bool(
                    audit_row.get("strict_remap_guardrail_required")
                ),
                "countable_label_candidate": False,
                "recommended_next_action": (
                    "review_selected_structure_replacement_before_review_import"
                ),
                "review_policy": (
                    "candidate alternate structures may inform a local "
                    "structure-selection rule, but conservative remap-local "
                    "ligand hits are review-only and cannot make labels "
                    "countable without explicit review/import evidence and "
                    "passing factory gates"
                ),
            }
        )

    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))
    return {
        "metadata": {
            "method": "review_debt_structure_selection_candidate_summary",
            "source_audit_method": remap_local_lead_audit.get("metadata", {}).get(
                "method"
            ),
            "source_scan_method": alternate_structure_scan.get("metadata", {}).get(
                "method"
            ),
            "candidate_count": len(rows),
            "candidate_entry_ids": _sorted_entry_ids(row.get("entry_id") for row in rows),
            "strict_remap_guardrail_entry_ids": _sorted_entry_ids(
                row.get("entry_id")
                for row in rows
                if row.get("strict_remap_guardrail_required")
            ),
            "countable_label_candidate_count": 0,
            "review_rule": (
                "structure-selection candidates are review-only until explicit "
                "alternate-structure residue evidence or expert review clears "
                "the selected-structure cofactor gap and label-factory gates pass"
            ),
        },
        "rows": rows,
    }


def audit_reaction_substrate_mismatches(
    *,
    review_evidence_gaps: dict[str, Any] | None = None,
    active_learning_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Find review rows where text suggests reaction class mismatch."""
    by_entry: dict[str, dict[str, Any]] = {}
    source_names_by_entry: dict[str, set[str]] = defaultdict(set)
    for source_name, artifact in [
        ("review_evidence_gaps", review_evidence_gaps),
        ("active_learning_queue", active_learning_queue),
    ]:
        for row in (artifact or {}).get("rows", []):
            if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
                continue
            entry_id = str(row["entry_id"])
            merged = by_entry.setdefault(entry_id, {})
            merged.update({key: value for key, value in row.items() if value is not None})
            source_names_by_entry[entry_id].add(source_name)

    rows: list[dict[str, Any]] = []
    for entry_id, row in by_entry.items():
        reasons = _remap_local_reaction_substrate_mismatch_reasons(
            entry_name=str(row.get("entry_name", "")),
            mechanism_text_snippets=row.get("mechanism_text_snippets", []),
            top1_fingerprint_id=row.get("top1_fingerprint_id"),
        )
        if not reasons:
            continue
        atp_family_assignment = _atp_phosphoryl_transfer_family_assignment(
            entry_name=row.get("entry_name", ""),
            mechanism_text_snippets=row.get("mechanism_text_snippets", []),
            top1_fingerprint_id=row.get("top1_fingerprint_id"),
        )
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": row.get("entry_name"),
                "source_artifacts": sorted(source_names_by_entry.get(entry_id, [])),
                "top1_fingerprint_id": row.get("top1_fingerprint_id"),
                "top1_ontology_family": row.get("top1_ontology_family")
                or fingerprint_family(str(row.get("top1_fingerprint_id"))),
                "top1_score": row.get("top1_score"),
                "target_fingerprint_id": row.get("target_fingerprint_id"),
                "decision_action": row.get("decision_action"),
                "decision_review_status": row.get("decision_review_status"),
                "source_recommended_action": row.get("recommended_action"),
                "recommended_action": "expert_reaction_substrate_review",
                "rank": row.get("rank"),
                "label_state": row.get("label_state"),
                "current_label_type": row.get("current_label_type"),
                "mismatch_reasons": reasons,
                "atp_phosphoryl_transfer_family": atp_family_assignment,
                "atp_phosphoryl_transfer_family_id": _atp_family_id_from_assignment(
                    atp_family_assignment
                ),
                "mechanism_text_snippets": row.get("mechanism_text_snippets", []),
                "countable_label_candidate": False,
                "review_policy": (
                    "reaction/substrate text that conflicts with the top ontology "
                    "family must be expert-reviewed before any label can count"
                ),
            }
        )

    rows = sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))))
    reason_counts = Counter(
        reason for row in rows for reason in row.get("mismatch_reasons", [])
    )
    top1_counts = Counter(str(row.get("top1_fingerprint_id")) for row in rows)
    atp_family_counts = Counter(
        str(row.get("atp_phosphoryl_transfer_family_id"))
        for row in rows
        if row.get("atp_phosphoryl_transfer_family_id")
    )
    return {
        "metadata": {
            "method": "reaction_substrate_mismatch_audit",
            "mismatch_count": len(rows),
            "mismatch_entry_ids": _sorted_entry_ids(row.get("entry_id") for row in rows),
            "mismatch_reason_counts": dict(sorted(reason_counts.items())),
            "top1_fingerprint_counts": dict(sorted(top1_counts.items())),
            "atp_phosphoryl_transfer_family_counts": dict(
                sorted(atp_family_counts.items())
            ),
            "atp_phosphoryl_transfer_family_boundary_count": sum(
                atp_family_counts.values()
            ),
            "countable_label_candidate_count": 0,
            "review_rule": (
                "keyword-level reaction/substrate mismatch signals are review "
                "triage only; they cannot reject or accept labels without expert "
                "or rule-backed review"
            ),
        },
        "rows": rows,
    }


def build_reaction_substrate_mismatch_review_export(
    *,
    reaction_substrate_mismatch_audit: dict[str, Any],
    family_propagation_guardrails: dict[str, Any],
    labels: list[MechanismLabel],
) -> dict[str, Any]:
    """Build a dedicated expert-review export for reaction/substrate mismatches."""
    labels_by_entry = {label.entry_id: label for label in labels}
    audit_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in reaction_substrate_mismatch_audit.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    guardrail_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in family_propagation_guardrails.get("rows", [])
        if isinstance(row, dict)
        and isinstance(row.get("entry_id"), str)
        and row.get("reaction_substrate_mismatch_reasons")
    }
    entry_ids = _sorted_entry_ids(
        set(audit_rows_by_entry) | set(guardrail_rows_by_entry)
    )

    context_rows: list[dict[str, Any]] = []
    for entry_id in entry_ids:
        audit_row = audit_rows_by_entry.get(entry_id, {})
        guardrail_row = guardrail_rows_by_entry.get(entry_id, {})
        label = labels_by_entry.get(entry_id)
        mismatch_reasons = _sorted_strings(
            _sorted_strings(audit_row.get("mismatch_reasons", []))
            + _sorted_strings(
                guardrail_row.get("reaction_substrate_mismatch_reasons", [])
            )
        )
        source_artifacts = set(_sorted_strings(audit_row.get("source_artifacts", [])))
        if audit_row:
            source_artifacts.add("reaction_substrate_mismatch_audit")
        if guardrail_row:
            source_artifacts.add("family_propagation_guardrails")
        label_state = (
            guardrail_row.get("label_state")
            or audit_row.get("label_state")
            or ("labeled" if label else "unlabeled")
        )
        top1_fingerprint_id = (
            guardrail_row.get("top1_fingerprint_id")
            or audit_row.get("top1_fingerprint_id")
        )
        top1_ontology_family = (
            guardrail_row.get("top1_ontology_family")
            or audit_row.get("top1_ontology_family")
            or (
                fingerprint_family(str(top1_fingerprint_id))
                if top1_fingerprint_id
                else None
            )
        )
        atp_family_assignment = (
            guardrail_row.get("atp_phosphoryl_transfer_family")
            if isinstance(guardrail_row.get("atp_phosphoryl_transfer_family"), dict)
            else audit_row.get("atp_phosphoryl_transfer_family")
            if isinstance(audit_row.get("atp_phosphoryl_transfer_family"), dict)
            else _atp_phosphoryl_transfer_family_assignment(
                entry_name=guardrail_row.get("entry_name")
                or audit_row.get("entry_name")
                or "",
                mechanism_text_snippets=guardrail_row.get("mechanism_text_snippets")
                or audit_row.get("mechanism_text_snippets", []),
                top1_fingerprint_id=top1_fingerprint_id,
            )
        )
        current_label_type = (
            label.label_type
            if label
            else guardrail_row.get("current_label_type")
            or audit_row.get("current_label_type")
        )
        context_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": guardrail_row.get("entry_name")
                or audit_row.get("entry_name"),
                "resolution_lane": (
                    "labeled_propagation_block_review"
                    if label_state == "labeled"
                    else "unlabeled_pending_review"
                ),
                "label_state": label_state,
                "current_label_type": current_label_type,
                "current_fingerprint_id": label.fingerprint_id if label else None,
                "current_review_status": label.review_status if label else None,
                "current_tier": label.tier if label else None,
                "target_fingerprint_id": guardrail_row.get("target_fingerprint_id")
                or audit_row.get("target_fingerprint_id"),
                "target_ontology_family": guardrail_row.get("target_ontology_family"),
                "top1_fingerprint_id": top1_fingerprint_id,
                "top1_ontology_family": top1_ontology_family,
                "top1_score": guardrail_row.get("top1_score")
                if guardrail_row.get("top1_score") is not None
                else audit_row.get("top1_score"),
                "propagation_decision": guardrail_row.get("propagation_decision"),
                "propagation_blockers": _sorted_strings(
                    guardrail_row.get("propagation_blockers", [])
                ),
                "mismatch_reasons": mismatch_reasons,
                "atp_phosphoryl_transfer_family": atp_family_assignment,
                "atp_phosphoryl_transfer_family_id": _atp_family_id_from_assignment(
                    atp_family_assignment
                ),
                "source_artifacts": sorted(source_artifacts),
                "source_recommended_action": audit_row.get("source_recommended_action"),
                "recommended_action": "expert_reaction_substrate_review",
                "recommended_resolution": (
                    "expert_review_before_ontology_split_or_countable_label"
                ),
                "mechanism_text_snippets": guardrail_row.get("mechanism_text_snippets")
                or audit_row.get("mechanism_text_snippets", []),
                "countable_label_candidate": False,
                "review_policy": (
                    "route both labeled and unlabeled reaction/substrate mismatch "
                    "lanes to expert review before adding an ontology-family rule "
                    "or accepting more countable labels"
                ),
            }
        )

    label_state_counts = Counter(str(row.get("label_state")) for row in context_rows)
    current_label_type_counts = Counter(
        str(row.get("current_label_type") or "unlabeled") for row in context_rows
    )
    labeled_seed_mismatch_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in context_rows
        if row.get("label_state") == "labeled"
        and row.get("current_label_type") != "out_of_scope"
    )
    reason_counts = Counter(
        reason for row in context_rows for reason in row.get("mismatch_reasons", [])
    )
    top1_counts = Counter(
        str(row.get("top1_fingerprint_id"))
        for row in context_rows
        if row.get("top1_fingerprint_id")
    )
    atp_family_counts = Counter(
        str(row.get("atp_phosphoryl_transfer_family_id"))
        for row in context_rows
        if row.get("atp_phosphoryl_transfer_family_id")
    )
    audit_entry_ids = _sorted_entry_ids(audit_rows_by_entry)
    guardrail_entry_ids = _sorted_entry_ids(guardrail_rows_by_entry)
    export_entry_ids = _sorted_entry_ids(row.get("entry_id") for row in context_rows)
    return {
        "metadata": {
            "method": "reaction_substrate_mismatch_review_export",
            "source_audit_method": reaction_substrate_mismatch_audit.get(
                "metadata", {}
            ).get("method"),
            "source_family_guardrail_method": family_propagation_guardrails.get(
                "metadata", {}
            ).get("method"),
            "exported_count": len(context_rows),
            "exported_entry_ids": export_entry_ids,
            "reaction_audit_mismatch_count": len(audit_entry_ids),
            "reaction_audit_mismatch_entry_ids": audit_entry_ids,
            "family_guardrail_mismatch_count": len(guardrail_entry_ids),
            "family_guardrail_mismatch_entry_ids": guardrail_entry_ids,
            "all_reaction_audit_mismatches_exported": set(audit_entry_ids).issubset(
                set(export_entry_ids)
            ),
            "all_family_guardrail_mismatches_exported": set(
                guardrail_entry_ids
            ).issubset(set(export_entry_ids)),
            "label_state_counts": dict(sorted(label_state_counts.items())),
            "current_label_type_counts": dict(
                sorted(current_label_type_counts.items())
            ),
            "labeled_seed_mismatch_count": len(labeled_seed_mismatch_entry_ids),
            "labeled_seed_mismatch_entry_ids": labeled_seed_mismatch_entry_ids,
            "mismatch_reason_counts": dict(sorted(reason_counts.items())),
            "top1_fingerprint_counts": dict(sorted(top1_counts.items())),
            "atp_phosphoryl_transfer_family_counts": dict(
                sorted(atp_family_counts.items())
            ),
            "atp_phosphoryl_transfer_family_boundary_count": sum(
                atp_family_counts.values()
            ),
            "countable_label_candidate_count": 0,
            "ontology_rule_decision": "defer_new_family_rule_until_expert_review",
            "recommended_path": "expert_reaction_substrate_review_before_ontology_split",
            "decision_schema": {
                "action": [
                    "accept_label",
                    "mark_needs_more_evidence",
                    "reject_label",
                    "no_decision",
                ],
                "reaction_substrate_resolution": [
                    "confirm_current_label_or_out_of_scope",
                    "assign_existing_fingerprint",
                    "requires_new_ontology_family",
                    "needs_more_evidence",
                ],
                "review_status": [
                    "expert_reviewed",
                    "needs_expert_review",
                ],
            },
            "review_rule": (
                "keyword-level kinase or ATP phosphoryl-transfer mismatch is "
                "not enough to create a new ontology family or count a label; "
                "export every mismatch lane for expert reaction/substrate review"
            ),
            "countable_import_rule": (
                "accepted mismatch-export rows must be explicitly expert_reviewed "
                "and carry a non-needs_more_evidence reaction/substrate resolution "
                "before import-countable-label-review can count them"
            ),
        },
        "review_items": [
            {
                "rank": index,
                "entry_id": row["entry_id"],
                "entry_name": row.get("entry_name"),
                "current_label": labels_by_entry[row["entry_id"]].to_dict()
                if row["entry_id"] in labels_by_entry
                else None,
                "mismatch_context": row,
                "review_question": (
                    "Does this entry represent kinase, ATP phosphoryl-transfer, "
                    "or another non-hydrolytic reaction class that should remain "
                    "out of scope, use an existing seed fingerprint, or require "
                    "a new ontology family before any countable label is accepted?"
                ),
                "decision": {
                    "action": "no_decision",
                    "label_type": row.get("current_label_type"),
                    "fingerprint_id": row.get("current_fingerprint_id"),
                    "tier": row.get("current_tier") or "bronze",
                    "confidence": "medium",
                    "reviewer": None,
                    "rationale": None,
                    "evidence_score": None,
                    "review_status": "expert_reviewed",
                    "reaction_substrate_resolution": "needs_more_evidence",
                },
            }
            for index, row in enumerate(context_rows, start=1)
        ],
    }


def _remap_local_reaction_substrate_mismatch_reasons(
    *,
    entry_name: str,
    mechanism_text_snippets: Any,
    top1_fingerprint_id: Any,
) -> list[str]:
    if top1_fingerprint_id != "metal_dependent_hydrolase":
        return []
    text = " ".join(
        [entry_name, *[str(snippet) for snippet in _sorted_strings(mechanism_text_snippets)]]
    ).lower()
    reasons: list[str] = []
    if "kinase" in text:
        reasons.append("kinase_name_with_hydrolase_top1")
    atp_phosphoryl_context = "atp" in text and any(
        term in text
        for term in [
            "gamma phosph",
            "terminal phosphate",
            "phosphoryl group",
            "phosphate group of atp",
            "phosphorous of atp",
        ]
    )
    transfer_language = any(
        term in text
        for term in [
            "transfer",
            "transferred",
            "phosphorylated",
            "inline displacement",
            "in-line displacement",
            "attacks the gamma",
            "attack on the gamma",
            "attack to the beta",
        ]
    )
    hydrolysis_language = any(
        term in text for term in ["hydrolysis", "hydrolytic", "water", "lytic water"]
    )
    if atp_phosphoryl_context and transfer_language and not hydrolysis_language:
        reasons.append("atp_phosphoryl_transfer_text_with_hydrolase_top1")
    return reasons


def _normalize_atp_phosphoryl_family_hint(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    if not text:
        return None
    normalized = re.sub(r"[^a-z0-9]+", " ", text).strip()
    compact = normalized.replace(" ", "")
    for alias, family_id in ATP_PHOSPHORYL_FAMILY_HINT_ALIASES.items():
        alias_normalized = re.sub(r"[^a-z0-9]+", " ", alias.lower()).strip()
        if alias_normalized and alias_normalized in normalized:
            return family_id
        if alias_normalized.replace(" ", "") and alias_normalized.replace(" ", "") in compact:
            return family_id
    return None


def _atp_phosphoryl_transfer_family_assignment(
    *,
    entry_name: Any = "",
    mechanism_text_snippets: Any = None,
    top1_fingerprint_id: Any = None,
    future_family_hint: Any = None,
    require_mismatch_signal: bool = True,
) -> dict[str, Any] | None:
    """Conservatively map ATP/phosphoryl-transfer review lanes to target families."""
    hint_family_id = _normalize_atp_phosphoryl_family_hint(future_family_hint)
    if hint_family_id:
        return _atp_family_assignment_row(
            family_id=hint_family_id,
            evidence_sources=["expert_review_future_fingerprint_family_hint"],
            support_level="expert_review_supported_family_boundary",
        )

    snippets = _sorted_strings(mechanism_text_snippets or [])
    mismatch_reasons = _remap_local_reaction_substrate_mismatch_reasons(
        entry_name=str(entry_name or ""),
        mechanism_text_snippets=snippets,
        top1_fingerprint_id=top1_fingerprint_id,
    )
    if require_mismatch_signal and not mismatch_reasons:
        return None
    text = " ".join([str(entry_name or ""), *snippets]).lower()
    for family_id, patterns in ATP_PHOSPHORYL_FAMILY_TEXT_PATTERNS:
        if any(pattern in text for pattern in patterns):
            return _atp_family_assignment_row(
                family_id=family_id,
                evidence_sources=[
                    "reaction_substrate_mismatch_text_signature",
                    *mismatch_reasons,
                ],
                support_level="review_lane_text_signature_only",
            )
    return None


def _atp_family_assignment_row(
    *,
    family_id: str,
    evidence_sources: list[str],
    support_level: str,
) -> dict[str, Any]:
    return {
        "family_id": family_id,
        "family_name": ATP_PHOSPHORYL_TRANSFER_FAMILY_NAMES[family_id],
        "parent_family_id": ATP_PHOSPHORYL_PARENT_FAMILY_ID,
        "support_level": support_level,
        "evidence_sources": _sorted_strings(evidence_sources),
        "countable_label_candidate": False,
        "review_rule": (
            "ATP/phosphoryl-transfer family mapping is ontology boundary "
            "evidence only; unsupported rows stay review-only and cannot be "
            "counted as hydrolase labels."
        ),
    }


def _atp_family_id_from_assignment(assignment: dict[str, Any] | None) -> str | None:
    if not isinstance(assignment, dict):
        return None
    family_id = assignment.get("family_id")
    return str(family_id) if isinstance(family_id, str) and family_id else None


def _ligand_codes_matching_families(
    ligand_codes: Any,
    expected_families: Any,
) -> list[str]:
    families = set(_sorted_strings(expected_families))
    if not families:
        return []
    matches: set[str] = set()
    for code in _sorted_strings(ligand_codes):
        normalized = code.upper()
        if "metal_ion" in families and normalized in METAL_ION_CODES:
            matches.add(normalized)
        mapped_family = COFACTOR_LIGAND_MAP.get(normalized)
        if mapped_family in families:
            matches.add(normalized)
    return sorted(matches)


def _review_debt_priority_score(
    gap_reasons: list[str],
    coverage_status: str,
    active_queue_rank: int | None,
) -> float:
    score = float(len(set(gap_reasons)))
    if coverage_status == "expected_absent_from_structure":
        score += 2.0
    elif coverage_status == "expected_structure_only":
        score += 1.5
    if "counterevidence_present" in gap_reasons:
        score += 1.0
    if "target_not_top1" in gap_reasons:
        score += 1.0
    if "top1_below_abstention_threshold" in gap_reasons:
        score += 0.75
    if active_queue_rank:
        score += max(0.0, 1.0 - min(active_queue_rank, 100) / 100.0)
    return score


def _review_debt_next_action(gap_reasons: list[str], coverage_status: str) -> str:
    reasons = set(gap_reasons)
    if coverage_status == "expected_absent_from_structure":
        return "inspect_alternate_structure_or_cofactor_source"
    if coverage_status == "expected_structure_only":
        return "verify_local_cofactor_or_active_site_mapping"
    if "target_not_top1" in reasons or "counterevidence_present" in reasons:
        return "expert_family_boundary_review"
    if "top1_below_abstention_threshold" in reasons:
        return "keep_abstained_until_stronger_evidence"
    return "expert_review_decision_needed"


def _review_debt_remediation_bucket(
    gap_reasons: list[str],
    coverage_status: str,
    *,
    geometry_row: dict[str, Any],
    alternate_pdb_count: int,
) -> str:
    reasons = set(gap_reasons)
    geometry_status = str(geometry_row.get("status", "unknown"))
    if geometry_status not in {"ok", "unknown"}:
        return "active_site_mapping_repair"
    if coverage_status == "expected_structure_only":
        return "local_mapping_or_structure_selection_review"
    if (
        coverage_status == "expected_absent_from_structure"
        or "expected_cofactor_absent_from_structure" in reasons
    ):
        if alternate_pdb_count > 0:
            return "alternate_pdb_ligand_scan"
        return "external_cofactor_source_review"
    if "target_not_top1" in reasons or "counterevidence_present" in reasons:
        return "expert_family_boundary_review"
    if "top1_below_abstention_threshold" in reasons:
        return "retrieval_threshold_evidence_review"
    return "expert_label_decision"


def _review_debt_status(
    entry_id: str,
    new_ids: list[str],
    carried_ids: list[str],
) -> str | None:
    if entry_id in set(new_ids):
        return "new"
    if entry_id in set(carried_ids):
        return "carried"
    return None


def _review_debt_graph_context_by_entry(
    graph: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    if not isinstance(graph, dict):
        return {}
    nodes = graph.get("nodes", [])
    node_by_id = {
        str(node.get("id")): node
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    proteins_by_entry: dict[str, set[str]] = {}
    structures_by_protein: dict[str, set[str]] = {}
    residue_position_counts_by_entry: dict[str, Counter] = {}
    residue_positions_by_entry: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for node in nodes:
        if not isinstance(node, dict) or node.get("type") != "catalytic_residue":
            continue
        node_id = str(node.get("id", ""))
        if ":residue:" not in node_id:
            continue
        entry_id = node_id.split(":residue:", 1)[0]
        counter = residue_position_counts_by_entry.setdefault(entry_id, Counter())
        pdb_ids_for_residue: set[str] = set()
        for position in node.get("structure_positions", []):
            if not isinstance(position, dict) or not position.get("pdb_id"):
                continue
            pdb_id = str(position.get("pdb_id", "")).upper()
            pdb_ids_for_residue.add(pdb_id)
            residue_positions_by_entry.setdefault(entry_id, {}).setdefault(pdb_id, []).append(
                {
                    "residue_node_id": node_id,
                    "chain_name": position.get("chain_name"),
                    "code": position.get("code"),
                    "resid": position.get("resid"),
                    "roles": node.get("roles", []),
                }
            )
        for pdb_id in pdb_ids_for_residue:
            counter[pdb_id] += 1
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = edge.get("source")
        target = edge.get("target")
        predicate = edge.get("predicate")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if predicate == "has_reference_protein" and source.startswith("m_csa:"):
            proteins_by_entry.setdefault(source, set()).add(target)
        elif predicate == "has_structure" and source.startswith("uniprot:"):
            structures_by_protein.setdefault(source, set()).add(target)

    context: dict[str, dict[str, Any]] = {}
    for entry_id, proteins in proteins_by_entry.items():
        structures = sorted(
            {
                structure
                for protein_id in proteins
                for structure in structures_by_protein.get(protein_id, set())
            },
            key=str,
        )
        pdb_ids: list[str] = []
        alphafold_ids: list[str] = []
        for structure_id in structures:
            node = node_by_id.get(structure_id, {})
            source = str(node.get("structure_source", ""))
            raw_id = str(node.get("structure_id") or structure_id.split(":", 1)[-1])
            if structure_id.startswith("pdb:") or source == "pdb":
                pdb_ids.append(raw_id.upper())
            elif structure_id.startswith("alphafold:") or source == "alphafold_db":
                alphafold_ids.append(raw_id)
        context[entry_id] = {
            "reference_uniprot_ids": _sorted_strings(
                protein.split(":", 1)[-1] for protein in proteins
            ),
            "pdb_structure_ids": _sorted_strings(pdb_ids),
            "alphafold_structure_ids": _sorted_strings(alphafold_ids),
            "pdb_residue_position_counts": dict(
                sorted(residue_position_counts_by_entry.get(entry_id, {}).items())
            ),
            "pdb_residue_positions": {
                pdb_id: positions
                for pdb_id, positions in sorted(
                    residue_positions_by_entry.get(entry_id, {}).items()
                )
            },
        }
    return context


def _review_debt_structure_availability(row: dict[str, Any]) -> str:
    if int(row.get("candidate_pdb_structure_count", 0) or 0) == 0:
        if row.get("alphafold_structure_ids"):
            return "alphafold_only"
        return "no_structure_context"
    if int(row.get("alternate_pdb_count", 0) or 0) > 0:
        return "selected_plus_alternate_pdb"
    return "selected_pdb_only"


def _review_debt_reference_residue_positions(
    residue_positions_by_pdb: dict[str, list[dict[str, Any]]],
    selected_pdb_id: str,
) -> list[dict[str, Any]]:
    selected = str(selected_pdb_id or "").upper()
    if selected:
        selected_positions = _review_debt_normalized_residue_positions(
            residue_positions_by_pdb.get(selected, [])
        )
        if selected_positions:
            return selected_positions
    for _pdb_id, positions in sorted(residue_positions_by_pdb.items()):
        normalized = _review_debt_normalized_residue_positions(positions)
        if normalized:
            return normalized
    return []


def _review_debt_normalized_residue_positions(
    positions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for position in positions:
        if not isinstance(position, dict):
            continue
        chain_name = position.get("chain_name")
        resid = position.get("resid")
        code = position.get("code")
        if chain_name in {None, "", ".", "?"}:
            continue
        if resid in {None, "", ".", "?"}:
            continue
        if code in {None, "", ".", "?"}:
            continue
        normalized.append(
            {
                **position,
                "chain_name": str(chain_name),
                "resid": str(resid),
                "code": str(code).upper(),
            }
        )
    return normalized


def _review_debt_infer_residue_positions(
    atoms: list[dict[str, Any]],
    residue_positions_by_pdb: dict[str, list[dict[str, Any]]],
    *,
    selected_pdb_id: str,
) -> dict[str, Any]:
    reference_positions = _review_debt_reference_residue_positions(
        residue_positions_by_pdb,
        selected_pdb_id,
    )
    if not reference_positions:
        return {
            "positions": [],
            "basis": None,
            "warnings": ["no_reference_residue_positions"],
        }

    direct_positions = _review_debt_positions_matching_atoms(atoms, reference_positions)
    if direct_positions:
        return {
            "positions": direct_positions,
            "basis": "same_chain_residue_id",
            "warnings": [],
        }

    chain_remap = _review_debt_chain_remapped_positions(atoms, reference_positions)
    if chain_remap.get("positions"):
        return chain_remap

    unique_remap = _review_debt_unique_residue_id_remapped_positions(
        atoms,
        reference_positions,
    )
    if unique_remap.get("positions"):
        return unique_remap

    warnings = ["no_conservative_residue_position_remap"]
    warnings.extend(chain_remap.get("warnings", []))
    warnings.extend(unique_remap.get("warnings", []))
    return {"positions": [], "basis": None, "warnings": sorted(set(warnings))}


def _review_debt_positions_matching_atoms(
    atoms: list[dict[str, Any]],
    positions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for position in positions:
        residue_atoms = select_residue_atoms(
            atoms,
            chain_name=position.get("chain_name"),
            resid=position.get("resid"),
            code=position.get("code"),
        )
        if not residue_atoms:
            return []
        resolved.append(dict(position))
    return resolved


def _review_debt_chain_remapped_positions(
    atoms: list[dict[str, Any]],
    reference_positions: list[dict[str, Any]],
) -> dict[str, Any]:
    reference_chains = {
        str(position.get("chain_name"))
        for position in reference_positions
        if position.get("chain_name")
    }
    if len(reference_chains) != 1:
        return {
            "positions": [],
            "basis": None,
            "warnings": ["reference_positions_span_multiple_chains"],
        }

    matches: list[tuple[str, list[dict[str, Any]]]] = []
    for chain_name in _review_debt_protein_chain_ids(atoms):
        remapped = [
            {
                **position,
                "chain_name": chain_name,
            }
            for position in reference_positions
        ]
        if _review_debt_positions_matching_atoms(atoms, remapped):
            matches.append((chain_name, remapped))

    if len(matches) == 1:
        return {
            "positions": matches[0][1],
            "basis": "same_residue_id_chain_remap",
            "warnings": [],
        }
    if len(matches) > 1:
        return {
            "positions": [],
            "basis": None,
            "warnings": ["ambiguous_same_residue_id_chain_remap"],
        }
    return {"positions": [], "basis": None, "warnings": []}


def _review_debt_unique_residue_id_remapped_positions(
    atoms: list[dict[str, Any]],
    reference_positions: list[dict[str, Any]],
) -> dict[str, Any]:
    remapped: list[dict[str, Any]] = []
    for position in reference_positions:
        matching_chains: list[str] = []
        for chain_name in _review_debt_protein_chain_ids(atoms):
            candidate = {**position, "chain_name": chain_name}
            if _review_debt_positions_matching_atoms(atoms, [candidate]):
                matching_chains.append(chain_name)
        unique_chains = sorted(set(matching_chains))
        if len(unique_chains) != 1:
            return {
                "positions": [],
                "basis": None,
                "warnings": ["ambiguous_or_missing_unique_residue_id_code_remap"],
            }
        remapped.append({**position, "chain_name": unique_chains[0]})
    return {
        "positions": remapped,
        "basis": "unique_residue_id_code_remap",
        "warnings": [],
    }


def _review_debt_protein_chain_ids(atoms: list[dict[str, Any]]) -> list[str]:
    chains: set[str] = set()
    for atom in atoms:
        code = str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()
        if code not in STANDARD_AMINO_ACIDS:
            continue
        for value in [atom.get("auth_asym_id"), atom.get("label_asym_id")]:
            if value not in {None, "", ".", "?"}:
                chains.add(str(value))
    return sorted(chains)


def _review_debt_scan_pdb_ids(row: dict[str, Any]) -> list[str]:
    ordered: list[str] = []
    selected = row.get("selected_pdb_id")
    if selected:
        ordered.append(str(selected).upper())
    for pdb_id in row.get("alternate_pdb_ids", []):
        normalized = str(pdb_id).upper()
        if normalized and normalized not in ordered:
            ordered.append(normalized)
    for pdb_id in row.get("candidate_pdb_structure_ids", []):
        normalized = str(pdb_id).upper()
        if normalized and normalized not in ordered:
            ordered.append(normalized)
    return ordered


def _review_debt_local_ligand_context(
    atoms: list[dict[str, Any]] | None,
    pdb_id: str,
    residue_positions_by_pdb: dict[str, list[dict[str, Any]]],
    *,
    cif_fetcher=fetch_pdb_cif,
    inventory_cache: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    positions = residue_positions_by_pdb.get(pdb_id, [])
    if not positions:
        return {
            "ligand_codes": [],
            "cofactor_families": [],
            "resolved_residue_count": 0,
        }
    if atoms is None:
        try:
            atoms = parse_atom_site_loop(cif_fetcher(pdb_id))
            if inventory_cache is not None and pdb_id not in inventory_cache:
                inventory_cache[pdb_id] = structure_ligand_inventory_from_atoms(atoms)
        except Exception:
            return {
                "ligand_codes": [],
                "cofactor_families": [],
                "resolved_residue_count": 0,
            }
    resolved: list[dict[str, Any]] = []
    for position in positions:
        if not isinstance(position, dict):
            continue
        if not position.get("chain_name") or position.get("resid") in {None, "", ".", "?"}:
            continue
        residue_atoms = select_residue_atoms(
            atoms,
            chain_name=position.get("chain_name"),
            resid=position.get("resid"),
            code=position.get("code"),
        )
        if not residue_atoms:
            continue
        resolved.append(
            {
                "residue_node_id": position.get("residue_node_id"),
                "code": position.get("code"),
                "chain_name": position.get("chain_name"),
                "resid": position.get("resid"),
                "centroid": residue_centroid(residue_atoms),
                "ca": atom_position(residue_atoms, "CA"),
                "roles": position.get("roles", []),
            }
        )
    context = ligand_context_from_atoms(atoms, resolved)
    return {
        **context,
        "resolved_residue_count": len(resolved),
    }


def _review_debt_scan_outcome(
    *,
    selected_hit: bool,
    alternate_hit: bool,
    candidate_pdb_count: int,
    unscanned_pdb_count: int,
) -> str:
    if alternate_hit:
        return "alternate_structure_has_expected_cofactor_candidate"
    if selected_hit:
        return "selected_structure_has_expected_cofactor_candidate"
    if candidate_pdb_count == 0:
        return "no_pdb_candidates_for_structure_scan"
    if unscanned_pdb_count > 0:
        return "no_hit_in_scanned_structures_continue_scan"
    return "no_expected_cofactor_in_scanned_structures"


def _sorted_entry_ids(values: Any) -> list[str]:
    if values is None or isinstance(values, str):
        return []
    try:
        iterable = list(values)
    except TypeError:
        return []
    return sorted(
        (str(value) for value in iterable if isinstance(value, str) and value),
        key=_entry_id_sort_key,
    )


def _sorted_strings(values: Any) -> list[str]:
    if isinstance(values, str):
        values = [values]
    if values is None:
        return []
    try:
        iterable = list(values)
    except TypeError:
        return []
    return sorted({str(value) for value in iterable if str(value)})


def check_label_preview_promotion_readiness(
    preview_acceptance: dict[str, Any],
    preview_summary: dict[str, Any],
    preview_review_debt: dict[str, Any],
    current_review_debt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    acceptance_meta = preview_acceptance.get("metadata", {})
    preview_summary_meta = preview_summary.get("metadata", {})
    preview_debt_meta = preview_review_debt.get("metadata", {})
    current_debt_meta = current_review_debt.get("metadata", {}) if current_review_debt else {}
    preview_debt_count = int(preview_debt_meta.get("review_debt_count", 0) or 0)
    current_debt_count = int(current_debt_meta.get("review_debt_count", 0) or 0)
    preview_needs_more = int(preview_debt_meta.get("needs_more_evidence_count", 0) or 0)
    current_needs_more = int(current_debt_meta.get("needs_more_evidence_count", 0) or 0)
    preview_new_debt_ids = [
        str(entry_id)
        for entry_id in preview_debt_meta.get("new_review_debt_entry_ids", [])
        if isinstance(entry_id, str)
    ]
    preview_carried_debt_ids = [
        str(entry_id)
        for entry_id in preview_debt_meta.get("carried_review_debt_entry_ids", [])
        if isinstance(entry_id, str)
    ]
    next_actions_by_status = preview_debt_meta.get(
        "recommended_next_action_counts_by_debt_status", {}
    )
    preview_new_action_counts = (
        dict(sorted(next_actions_by_status.get("new", {}).items()))
        if isinstance(next_actions_by_status, dict)
        and isinstance(next_actions_by_status.get("new"), dict)
        else {}
    )
    preview_carried_action_counts = (
        dict(sorted(next_actions_by_status.get("carried", {}).items()))
        if isinstance(next_actions_by_status, dict)
        and isinstance(next_actions_by_status.get("carried"), dict)
        else {}
    )
    preview_summary_blocker_count = int(
        preview_summary_meta.get(
            "blocker_count",
            len(preview_summary.get("blockers", []))
            if isinstance(preview_summary.get("blockers", []), list)
            else 0,
        )
        or 0
    )
    summary_countable_count = preview_summary_meta.get("latest_countable_label_count")
    summary_accepted_count = preview_summary_meta.get("total_accepted_new_label_count")
    summary_matches_acceptance = (
        (
            summary_countable_count is not None
            and int(summary_countable_count or 0)
            == int(acceptance_meta.get("countable_label_count", 0) or 0)
        )
        and (
            summary_accepted_count is not None
            and int(summary_accepted_count or 0)
            == int(acceptance_meta.get("accepted_new_label_count", 0) or 0)
        )
    )
    gates = {
        "preview_acceptance_passed": bool(acceptance_meta.get("accepted_for_counting")),
        "preview_summary_has_no_blockers": preview_summary_blocker_count == 0,
        "preview_summary_matches_acceptance": summary_matches_acceptance,
        "preview_summary_retains_unlabeled_candidates": preview_summary_meta.get(
            "all_active_queues_retain_unlabeled_candidates"
        )
        is True,
        "preview_zero_hard_negatives": int(
            acceptance_meta.get("hard_negative_count", 0) or 0
        )
        == 0,
        "preview_zero_near_misses": int(acceptance_meta.get("near_miss_count", 0) or 0) == 0,
        "preview_zero_false_non_abstentions": int(
            acceptance_meta.get("out_of_scope_false_non_abstentions", 0) or 0
        )
        == 0,
        "preview_zero_actionable_in_scope_failures": int(
            acceptance_meta.get("actionable_in_scope_failure_count", 0) or 0
        )
        == 0,
        "preview_debt_summary_present": preview_debt_meta.get("method") == "review_debt_summary",
    }
    blockers = [name for name, passed in gates.items() if not passed]
    review_warnings: list[str] = []
    if current_review_debt and preview_debt_count > current_debt_count:
        review_warnings.append("review_debt_count_increased")
    if current_review_debt and preview_needs_more > current_needs_more:
        review_warnings.append("needs_more_evidence_count_increased")
    if int(acceptance_meta.get("pending_review_count", 0) or 0) > 0:
        review_warnings.append("pending_review_rows_remain")
    mechanically_ready = not blockers
    recommendation = (
        "review_before_promoting"
        if mechanically_ready and review_warnings
        else "promote_if_policy_allows"
        if mechanically_ready
        else "do_not_promote"
    )
    return {
        "metadata": {
            "method": "label_preview_promotion_readiness",
            "mechanically_ready": mechanically_ready,
            "promotion_recommendation": recommendation,
            "accepted_new_label_count": acceptance_meta.get("accepted_new_label_count"),
            "preview_countable_label_count": acceptance_meta.get("countable_label_count"),
            "preview_pending_review_count": acceptance_meta.get("pending_review_count"),
            "preview_review_debt_count": preview_debt_count,
            "preview_new_review_debt_count": int(
                preview_debt_meta.get("new_review_debt_count", 0) or 0
            ),
            "preview_carried_review_debt_count": int(
                preview_debt_meta.get("carried_review_debt_count", 0) or 0
            ),
            "preview_new_review_debt_entry_ids": preview_new_debt_ids,
            "preview_carried_review_debt_entry_ids": preview_carried_debt_ids,
            "preview_new_review_debt_next_action_counts": preview_new_action_counts,
            "preview_carried_review_debt_next_action_counts": preview_carried_action_counts,
            "current_review_debt_count": current_debt_count if current_review_debt else None,
            "review_debt_delta": (
                preview_debt_count - current_debt_count if current_review_debt else None
            ),
            "preview_needs_more_evidence_count": preview_needs_more,
            "current_needs_more_evidence_count": (
                current_needs_more if current_review_debt else None
            ),
            "needs_more_evidence_delta": (
                preview_needs_more - current_needs_more if current_review_debt else None
            ),
            "policy": (
                "mechanical acceptance is not the same as promotion; increased "
                "review debt or pending review rows should be inspected before "
                "copying preview countable labels into the canonical registry"
            ),
        },
        "gates": gates,
        "blockers": blockers,
        "review_warnings": review_warnings,
    }


def audit_label_scaling_quality(
    acceptance: dict[str, Any],
    readiness: dict[str, Any],
    review_debt: dict[str, Any],
    review_evidence_gaps: dict[str, Any],
    active_learning_queue: dict[str, Any],
    family_propagation_guardrails: dict[str, Any],
    hard_negatives: dict[str, Any],
    decision_batch: dict[str, Any] | None = None,
    structure_mapping: dict[str, Any] | None = None,
    expert_review_export: dict[str, Any] | None = None,
    sequence_clusters: dict[str, Any] | None = None,
    alternate_structure_scan: dict[str, Any] | None = None,
    remap_local_lead_audit: dict[str, Any] | None = None,
    reaction_substrate_mismatch_audit: dict[str, Any] | None = None,
    reaction_substrate_mismatch_review_export: dict[str, Any] | None = None,
    expert_label_decision_review_export: dict[str, Any] | None = None,
    expert_label_decision_repair_candidates: dict[str, Any] | None = None,
    expert_label_decision_repair_guardrail_audit: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_gap_audit: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_review_export: dict[str, Any] | None = None,
    expert_label_decision_local_evidence_repair_resolution: dict[str, Any] | None = None,
    explicit_alternate_residue_position_requests: dict[str, Any] | None = None,
    review_only_import_safety_audit: dict[str, Any] | None = None,
    atp_phosphoryl_transfer_family_expansion: dict[str, Any] | None = None,
    batch_id: str | None = None,
) -> dict[str, Any]:
    acceptance_meta = acceptance.get("metadata", {})
    readiness_meta = readiness.get("metadata", {})
    debt_meta = review_debt.get("metadata", {})
    family_meta = family_propagation_guardrails.get("metadata", {})
    hard_meta = hard_negatives.get("metadata", {})
    mapping_meta = (structure_mapping or {}).get("metadata", {})
    alternate_scan_meta = (alternate_structure_scan or {}).get("metadata", {})
    remap_local_meta = (remap_local_lead_audit or {}).get("metadata", {})
    reaction_mismatch_meta = (reaction_substrate_mismatch_audit or {}).get("metadata", {})
    reaction_mismatch_export_meta = (
        reaction_substrate_mismatch_review_export or {}
    ).get("metadata", {})
    expert_label_decision_export_meta = (
        expert_label_decision_review_export or {}
    ).get("metadata", {})
    expert_label_decision_repair_meta = (
        expert_label_decision_repair_candidates or {}
    ).get("metadata", {})
    expert_label_decision_repair_guardrail_meta = (
        expert_label_decision_repair_guardrail_audit or {}
    ).get("metadata", {})
    expert_label_decision_local_gap_meta = (
        expert_label_decision_local_evidence_gap_audit or {}
    ).get("metadata", {})
    expert_label_decision_local_export_meta = (
        expert_label_decision_local_evidence_review_export or {}
    ).get("metadata", {})
    expert_label_decision_local_resolution_meta = (
        expert_label_decision_local_evidence_repair_resolution or {}
    ).get("metadata", {})
    alternate_residue_request_meta = (
        explicit_alternate_residue_position_requests or {}
    ).get("metadata", {})
    import_safety_meta = (review_only_import_safety_audit or {}).get("metadata", {})
    atp_family_expansion_meta = (
        atp_phosphoryl_transfer_family_expansion or {}
    ).get("metadata", {})
    new_debt_ids = sorted(
        (
            str(entry_id)
            for entry_id in debt_meta.get("new_review_debt_entry_ids", [])
            if isinstance(entry_id, str)
        ),
        key=_entry_id_sort_key,
    )
    gap_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in review_evidence_gaps.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    guardrail_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in family_propagation_guardrails.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    mapping_rows_by_entry = {
        str(row.get("entry_id")): row
        for row in (structure_mapping or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    decision_action_by_entry: dict[str, str] = {}
    if decision_batch:
        for item in decision_batch.get("review_items", []):
            if not isinstance(item, dict) or not isinstance(item.get("entry_id"), str):
                continue
            decision = item.get("decision", {})
            if isinstance(decision, dict):
                decision_action_by_entry[str(item["entry_id"])] = str(
                    decision.get("action", "no_decision")
                )
    accepted_decision_ids = sorted(
        (
            entry_id
            for entry_id, action in decision_action_by_entry.items()
            if action == "accept_label"
        ),
        key=_entry_id_sort_key,
    )
    accepted_new_debt_ids = sorted(
        set(new_debt_ids) & set(accepted_decision_ids),
        key=_entry_id_sort_key,
    )
    accepted_clean_ids = sorted(
        set(accepted_decision_ids) - set(new_debt_ids),
        key=_entry_id_sort_key,
    )
    duplicate_audit_entry_ids = sorted(
        set(new_debt_ids) | set(accepted_decision_ids),
        key=_entry_id_sort_key,
    )
    sequence_cluster_by_entry = _sequence_cluster_by_entry(sequence_clusters)
    duplicate_cluster_counts: Counter = Counter(
        sequence_cluster_by_entry[entry_id]
        for entry_id in duplicate_audit_entry_ids
        if entry_id in sequence_cluster_by_entry
    )
    overrepresented_sequence_clusters = {
        cluster_id: count
        for cluster_id, count in duplicate_cluster_counts.items()
        if count > 1
    }
    near_duplicate_entry_ids = sorted(
        (
            entry_id
            for entry_id in duplicate_audit_entry_ids
            if sequence_cluster_by_entry.get(entry_id) in overrepresented_sequence_clusters
        ),
        key=_entry_id_sort_key,
    )
    sequence_cluster_missing_entry_count = (
        len(
            [
                entry_id
                for entry_id in duplicate_audit_entry_ids
                if entry_id not in sequence_cluster_by_entry
            ]
        )
        if sequence_clusters is not None
        else None
    )
    if sequence_clusters is None:
        near_duplicate_audit_status = "not_assessed_no_sequence_cluster_artifact"
    elif not sequence_cluster_by_entry:
        near_duplicate_audit_status = "not_assessed_sequence_cluster_artifact_empty"
    elif near_duplicate_entry_ids:
        near_duplicate_audit_status = "observed"
    else:
        near_duplicate_audit_status = "not_observed_in_sequence_cluster_artifact"

    issue_rows: list[dict[str, Any]] = []
    for entry_id in new_debt_ids:
        gap_row = gap_rows_by_entry.get(entry_id, {"entry_id": entry_id})
        guardrail_row = guardrail_rows_by_entry.get(entry_id, {})
        mapping_row = mapping_rows_by_entry.get(entry_id, {})
        action = decision_action_by_entry.get(entry_id) or str(
            gap_row.get("decision_action", "unknown")
        )
        issue_classes = _label_scaling_issue_classes(
            gap_row,
            family_guardrail_row=guardrail_row,
            structure_mapping_row=mapping_row,
            decision_action=action,
        )
        issue_rows.append(
            {
                "entry_id": entry_id,
                "entry_name": gap_row.get("entry_name") or guardrail_row.get("entry_name"),
                "decision_action": action,
                "decision_review_status": gap_row.get("decision_review_status"),
                "issue_classes": issue_classes,
                "gap_reasons": gap_row.get("gap_reasons", []),
                "counterevidence_reasons": gap_row.get("counterevidence_reasons", []),
                "coverage_status": gap_row.get("coverage_status"),
                "target_fingerprint_id": gap_row.get("target_fingerprint_id"),
                "top1_fingerprint_id": gap_row.get("top1_fingerprint_id"),
                "top1_score": gap_row.get("top1_score"),
                "family_propagation_blockers": guardrail_row.get("propagation_blockers", []),
                "structure_mapping_status": mapping_row.get("status"),
            }
        )

    issue_class_counts = Counter(
        issue_class for row in issue_rows for issue_class in row["issue_classes"]
    )
    active_family_counts = Counter(
        str(row.get("top1_ontology_family"))
        for row in active_learning_queue.get("rows", [])
        if isinstance(row, dict) and row.get("top1_ontology_family")
    )
    active_total = sum(active_family_counts.values())
    dominant_family = active_family_counts.most_common(1)[0] if active_family_counts else None
    dominant_family_fraction = (
        round(dominant_family[1] / active_total, 4)
        if dominant_family and active_total
        else 0.0
    )
    queue_concentrated = bool(
        dominant_family and active_total >= 10 and dominant_family_fraction >= 0.6
    )
    hard_family_counts = Counter(
        {
            str(fingerprint): int(count)
            for fingerprint, count in hard_meta.get("top1_fingerprint_counts", {}).items()
        }
    )
    near_miss_family_counts = Counter(
        {
            str(fingerprint): int(count)
            for fingerprint, count in hard_meta.get("near_miss_top1_fingerprint_counts", {}).items()
        }
    )
    family_blocker_counts = Counter(
        {
            str(name): int(count)
            for name, count in family_meta.get("blocker_counts", {}).items()
        }
    )
    exported_review_entry_ids = {
        str(item.get("entry_id"))
        for item in (expert_review_export or {}).get("review_items", [])
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    }
    underrepresented_queue_entry_ids = sorted(
        (
            str(row.get("entry_id"))
            for row in active_learning_queue.get("rows", [])
            if isinstance(row, dict)
            and isinstance(row.get("entry_id"), str)
            and dominant_family
            and row.get("top1_ontology_family")
            and str(row.get("top1_ontology_family")) != dominant_family[0]
        ),
        key=_entry_id_sort_key,
    )
    omitted_underrepresented_entry_ids = sorted(
        set(underrepresented_queue_entry_ids) - exported_review_entry_ids,
        key=_entry_id_sort_key,
    )
    review_export_retains_underrepresented = (
        not queue_concentrated
        or (bool(expert_review_export) and not omitted_underrepresented_entry_ids)
    )
    unclassified_new_debt_ids = sorted(
        (row["entry_id"] for row in issue_rows if not row["issue_classes"]),
        key=_entry_id_sort_key,
    )
    gates = {
        "zero_hard_negatives": int(hard_meta.get("hard_negative_count", 0) or 0) == 0,
        "zero_near_misses": int(hard_meta.get("near_miss_count", 0) or 0) == 0,
        "zero_false_non_abstentions": int(
            acceptance_meta.get("out_of_scope_false_non_abstentions", 0) or 0
        )
        == 0,
        "zero_actionable_in_scope_failures": int(
            acceptance_meta.get("actionable_in_scope_failure_count", 0) or 0
        )
        == 0,
        "active_queue_retains_unlabeled_candidates": active_learning_queue.get(
            "metadata", {}
        ).get("all_unlabeled_rows_retained")
        is True,
        "family_guardrails_present": family_meta.get("method")
        == "family_propagation_guardrail_audit",
        "new_review_debt_rows_classified": not unclassified_new_debt_ids,
        "accepted_new_labels_without_review_debt": not accepted_new_debt_ids,
        "review_export_retains_underrepresented_families": review_export_retains_underrepresented,
    }
    blockers = [name for name, passed in gates.items() if not passed]
    review_warnings: list[str] = []
    if queue_concentrated:
        review_warnings.append("active_learning_queue_concentrated_by_top1_family")
    if issue_class_counts:
        review_warnings.append("new_review_debt_has_scaling_failure_modes")
    if int(mapping_meta.get("issue_count", 0) or 0) > 0:
        review_warnings.append("structure_mapping_issues_present")
    if near_duplicate_audit_status in {
        "not_assessed_no_sequence_cluster_artifact",
        "not_assessed_sequence_cluster_artifact_empty",
    }:
        review_warnings.append("sequence_cluster_artifact_missing_for_near_duplicate_audit")
    elif near_duplicate_audit_status == "observed":
        review_warnings.append("candidate_entries_share_sequence_clusters")
    alternate_scan_fetch_failure_count = int(
        alternate_scan_meta.get("fetch_failure_count", 0) or 0
    )
    alternate_scan_expected_hits = _sorted_entry_ids(
        alternate_scan_meta.get("expected_family_hit_entry_ids", [])
    )
    alternate_scan_local_hits = _sorted_entry_ids(
        alternate_scan_meta.get("local_expected_family_hit_entry_ids", [])
    )
    alternate_scan_remapped_positions = _sorted_entry_ids(
        alternate_scan_meta.get("remapped_residue_position_entry_ids", [])
    )
    alternate_scan_alternate_remapped_positions = _sorted_entry_ids(
        alternate_scan_meta.get(
            "alternate_pdb_remapped_residue_position_entry_ids", []
        )
    )
    alternate_scan_remapped_local_hits = _sorted_entry_ids(
        alternate_scan_meta.get("local_expected_family_hit_from_remap_entry_ids", [])
    )
    alternate_scan_structure_wide_hits = _sorted_entry_ids(
        alternate_scan_meta.get(
            "structure_wide_hit_without_local_support_entry_ids", []
        )
    )
    if alternate_scan_fetch_failure_count > 0:
        review_warnings.append("alternate_structure_scan_fetch_failures")
    if alternate_scan_structure_wide_hits:
        review_warnings.append("alternate_structure_hits_lack_local_support")
    remap_local_audit_present = (
        remap_local_meta.get("method") == "review_debt_remap_local_lead_audit"
    )
    remap_local_countable_candidate_count = int(
        remap_local_meta.get("countable_label_candidate_count", 0) or 0
    )
    remap_local_strict_guardrail_ids = _sorted_entry_ids(
        remap_local_meta.get("strict_remap_guardrail_entry_ids", [])
    )
    remap_local_expert_review_ids = _sorted_entry_ids(
        remap_local_meta.get("expert_family_boundary_review_entry_ids", [])
    )
    remap_local_reaction_review_ids = _sorted_entry_ids(
        remap_local_meta.get("expert_reaction_substrate_review_entry_ids", [])
    )
    remap_local_structure_rule_ids = _sorted_entry_ids(
        remap_local_meta.get("local_structure_selection_rule_candidate_entry_ids", [])
    )
    gates["remap_local_leads_remain_review_only"] = (
        not remap_local_audit_present or remap_local_countable_candidate_count == 0
    )
    blockers = [name for name, passed in gates.items() if not passed]
    if remap_local_countable_candidate_count > 0:
        review_warnings.append("remap_local_lead_audit_countable_candidates")
    if remap_local_strict_guardrail_ids:
        review_warnings.append("remap_local_leads_require_strict_guardrail")
    reaction_mismatch_audit_present = (
        reaction_mismatch_meta.get("method") == "reaction_substrate_mismatch_audit"
    )
    reaction_mismatch_audit_entry_ids = _sorted_entry_ids(
        reaction_mismatch_meta.get("mismatch_entry_ids", [])
    )
    family_reaction_mismatch_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in family_propagation_guardrails.get("rows", [])
        if isinstance(row, dict) and row.get("reaction_substrate_mismatch_reasons")
    )
    expected_reaction_mismatch_review_entry_ids = _sorted_entry_ids(
        set(reaction_mismatch_audit_entry_ids)
        | set(family_reaction_mismatch_entry_ids)
    )
    reaction_mismatch_review_export_present = (
        reaction_mismatch_export_meta.get("method")
        == "reaction_substrate_mismatch_review_export"
    )
    reaction_mismatch_review_export_entry_ids = _sorted_entry_ids(
        reaction_mismatch_export_meta.get("exported_entry_ids", [])
    )
    if reaction_substrate_mismatch_review_export and not reaction_mismatch_review_export_entry_ids:
        reaction_mismatch_review_export_entry_ids = _sorted_entry_ids(
            item.get("entry_id")
            for item in reaction_substrate_mismatch_review_export.get(
                "review_items", []
            )
            if isinstance(item, dict)
        )
    reaction_mismatch_review_export_missing_entry_ids = _sorted_entry_ids(
        set(expected_reaction_mismatch_review_entry_ids)
        - set(reaction_mismatch_review_export_entry_ids)
    )
    if reaction_mismatch_review_export_present:
        gates["reaction_substrate_mismatch_review_export_retains_mismatch_lanes"] = (
            not reaction_mismatch_review_export_missing_entry_ids
        )
        blockers = [name for name, passed in gates.items() if not passed]
    if reaction_mismatch_audit_entry_ids:
        review_warnings.append("reaction_substrate_mismatch_audit_hits")
    if expected_reaction_mismatch_review_entry_ids and not reaction_mismatch_review_export_present:
        review_warnings.append("reaction_substrate_mismatch_review_export_missing")
    elif reaction_mismatch_review_export_missing_entry_ids:
        review_warnings.append("reaction_substrate_mismatch_review_export_incomplete")

    active_expert_label_decision_entry_ids = _sorted_entry_ids(
        row.get("entry_id")
        for row in active_learning_queue.get("rows", [])
        if isinstance(row, dict)
        and isinstance(row.get("entry_id"), str)
        and row.get("recommended_action") == "expert_label_decision_needed"
    )
    expert_label_decision_export_present = (
        expert_label_decision_export_meta.get("method")
        == "expert_label_decision_review_export"
    )
    expert_label_decision_export_entry_ids = _sorted_entry_ids(
        expert_label_decision_export_meta.get("exported_entry_ids", [])
    )
    if expert_label_decision_review_export and not expert_label_decision_export_entry_ids:
        expert_label_decision_export_entry_ids = _sorted_entry_ids(
            item.get("entry_id")
            for item in expert_label_decision_review_export.get("review_items", [])
            if isinstance(item, dict)
        )
    expert_label_decision_export_missing_entry_ids = _sorted_entry_ids(
        set(active_expert_label_decision_entry_ids)
        - set(expert_label_decision_export_entry_ids)
    )
    expert_label_decision_export_countable_count = int(
        expert_label_decision_export_meta.get("countable_label_candidate_count", 0)
        or 0
    )
    expert_label_decision_export_decision_counts = (
        expert_label_decision_export_meta.get("decision_counts", {})
    )
    expert_label_decision_repair_present = (
        expert_label_decision_repair_meta.get("method")
        == "expert_label_decision_repair_candidate_summary"
    )
    expert_label_decision_repair_entry_ids = _sorted_entry_ids(
        expert_label_decision_repair_meta.get("candidate_entry_ids", [])
    )
    if (
        expert_label_decision_repair_candidates
        and not expert_label_decision_repair_entry_ids
    ):
        expert_label_decision_repair_entry_ids = _sorted_entry_ids(
            row.get("entry_id")
            for row in expert_label_decision_repair_candidates.get("rows", [])
            if isinstance(row, dict)
        )
    expert_label_decision_repair_candidate_count = int(
        expert_label_decision_repair_meta.get("candidate_count", 0) or 0
    )
    expert_label_decision_repair_entry_id_count_matches = (
        expert_label_decision_repair_candidate_count
        == len(expert_label_decision_repair_entry_ids)
    )
    expert_label_decision_repair_missing_entry_ids = _sorted_entry_ids(
        set(active_expert_label_decision_entry_ids)
        - set(expert_label_decision_repair_entry_ids)
    )
    expert_label_decision_repair_countable_count = int(
        expert_label_decision_repair_meta.get("countable_label_candidate_count", 0)
        or 0
    )
    expert_label_decision_repair_guardrail_present = (
        expert_label_decision_repair_guardrail_meta.get("method")
        == "expert_label_decision_repair_guardrail_audit"
    )
    expert_label_decision_repair_guardrail_countable_count = int(
        expert_label_decision_repair_guardrail_meta.get(
            "countable_label_candidate_count", 0
        )
        or 0
    )
    expert_label_decision_local_gap_present = (
        expert_label_decision_local_gap_meta.get("method")
        == "expert_label_decision_local_evidence_gap_audit"
    )
    expert_label_decision_local_gap_countable_count = int(
        expert_label_decision_local_gap_meta.get(
            "countable_label_candidate_count", 0
        )
        or 0
    )
    expert_label_decision_local_gap_missing_entry_ids = _sorted_entry_ids(
        expert_label_decision_local_gap_meta.get("missing_priority_entry_ids", [])
    )
    expert_label_decision_local_gap_audited_count = int(
        expert_label_decision_local_gap_meta.get("audited_entry_count", 0) or 0
    )
    expert_label_decision_priority_repair_count = int(
        expert_label_decision_repair_guardrail_meta.get("priority_repair_row_count", 0)
        or 0
    )
    expert_label_decision_local_export_present = (
        expert_label_decision_local_export_meta.get("method")
        == "expert_label_decision_local_evidence_review_export"
    )
    expert_label_decision_local_export_count = int(
        expert_label_decision_local_export_meta.get("exported_count", 0) or 0
    )
    expert_label_decision_local_export_countable_count = int(
        expert_label_decision_local_export_meta.get(
            "countable_label_candidate_count", 0
        )
        or 0
    )
    expert_label_decision_local_export_decision_counts = (
        expert_label_decision_local_export_meta.get("decision_counts", {})
    )
    if not isinstance(expert_label_decision_local_export_decision_counts, dict):
        expert_label_decision_local_export_decision_counts = {}
    expert_label_decision_local_export_no_decision_count = int(
        expert_label_decision_local_export_decision_counts.get("no_decision", 0) or 0
    )
    expert_label_decision_local_resolution_present = (
        expert_label_decision_local_resolution_meta.get("method")
        == "expert_label_decision_local_evidence_repair_resolution"
    )
    expert_label_decision_local_resolution_countable_count = int(
        expert_label_decision_local_resolution_meta.get(
            "countable_label_candidate_count", 0
        )
        or 0
    )
    expert_label_decision_local_resolution_resolved_count = int(
        expert_label_decision_local_resolution_meta.get("resolved_entry_count", 0)
        or 0
    )
    alternate_residue_request_present = (
        alternate_residue_request_meta.get("method")
        == "explicit_alternate_residue_position_sourcing_requests"
    )
    alternate_residue_request_count = int(
        alternate_residue_request_meta.get("request_count", 0) or 0
    )
    alternate_residue_request_countable_count = int(
        alternate_residue_request_meta.get("countable_label_candidate_count", 0) or 0
    )
    import_safety_present = (
        import_safety_meta.get("method") == "review_only_import_safety_audit"
    )
    import_safety_new_count = int(
        import_safety_meta.get("total_new_countable_label_count", 0) or 0
    )
    atp_family_expansion_present = (
        atp_family_expansion_meta.get("method")
        == "atp_phosphoryl_transfer_family_expansion"
    )
    atp_family_expansion_countable_count = int(
        atp_family_expansion_meta.get("countable_label_candidate_count", 0) or 0
    )
    atp_family_expansion_ready = (
        not atp_phosphoryl_transfer_family_expansion
        or (
            atp_family_expansion_present
            and bool(atp_family_expansion_meta.get("boundary_guardrail_ready"))
            and bool(atp_family_expansion_meta.get("all_required_families_present"))
            and bool(
                atp_family_expansion_meta.get(
                    "all_required_family_relationships_declared"
                )
            )
            and bool(
                atp_family_expansion_meta.get(
                    "all_required_families_have_scope_notes"
                )
            )
            and not atp_family_expansion_meta.get("unmapped_required_family_ids", [])
            and atp_family_expansion_countable_count == 0
        )
    )
    local_gap_action_counts = expert_label_decision_local_gap_meta.get(
        "recommended_action_counts", {}
    )
    if not isinstance(local_gap_action_counts, dict):
        local_gap_action_counts = {}
    expected_alternate_residue_request_count = int(
        local_gap_action_counts.get(
            "source_explicit_alternate_structure_residue_positions", 0
        )
        or 0
    )
    if active_expert_label_decision_entry_ids:
        gates["expert_label_decision_review_export_retains_review_only_lanes"] = (
            expert_label_decision_export_present
            and not expert_label_decision_export_missing_entry_ids
            and expert_label_decision_export_countable_count == 0
            and bool(expert_label_decision_export_meta.get("export_ready", True))
            and int(
                expert_label_decision_export_decision_counts.get("no_decision", 0)
                or 0
            )
            == int(expert_label_decision_export_meta.get("exported_count", 0) or 0)
        )
        gates["expert_label_decision_repair_candidates_cover_review_only_lanes"] = (
            expert_label_decision_repair_present
            and expert_label_decision_repair_candidate_count
            >= len(active_expert_label_decision_entry_ids)
            and expert_label_decision_repair_entry_id_count_matches
            and not expert_label_decision_repair_missing_entry_ids
            and expert_label_decision_repair_countable_count == 0
        )
        gates[
            "expert_label_decision_repair_guardrail_keeps_priority_lanes_non_countable"
        ] = (
            expert_label_decision_repair_guardrail_present
            and bool(expert_label_decision_repair_guardrail_meta.get("guardrail_ready"))
            and bool(
                expert_label_decision_repair_guardrail_meta.get(
                    "all_priority_lanes_non_countable"
                )
            )
            and expert_label_decision_repair_guardrail_countable_count == 0
        )
        if expert_label_decision_priority_repair_count > 0:
            gates["expert_label_decision_local_evidence_gaps_audited"] = (
                expert_label_decision_local_gap_present
                and bool(expert_label_decision_local_gap_meta.get("audit_ready"))
                and bool(
                    expert_label_decision_local_gap_meta.get(
                        "priority_rows_accounted_for"
                    )
                )
                and not expert_label_decision_local_gap_missing_entry_ids
                and expert_label_decision_local_gap_countable_count == 0
                and expert_label_decision_local_gap_audited_count
                >= expert_label_decision_priority_repair_count
            )
            gates["expert_label_decision_local_evidence_review_export_ready"] = (
                expert_label_decision_local_export_present
                and bool(expert_label_decision_local_export_meta.get("export_ready"))
                and bool(
                    expert_label_decision_local_export_meta.get(
                        "all_source_rows_exported"
                    )
                )
                and expert_label_decision_local_export_count
                >= expert_label_decision_local_gap_audited_count
                and expert_label_decision_local_export_countable_count == 0
                and expert_label_decision_local_export_no_decision_count
                == expert_label_decision_local_export_count
            )
        if expert_label_decision_local_evidence_repair_resolution is not None:
            gates[
                "expert_label_decision_local_evidence_repair_resolution_ready"
            ] = (
                expert_label_decision_local_resolution_present
                and bool(
                    expert_label_decision_local_resolution_meta.get(
                        "resolution_ready"
                    )
                )
                and expert_label_decision_local_resolution_resolved_count > 0
                and expert_label_decision_local_resolution_countable_count == 0
                and bool(
                    expert_label_decision_local_resolution_meta.get(
                        "all_resolved_rows_non_countable"
                    )
                )
            )
        if explicit_alternate_residue_position_requests is not None:
            gates["explicit_alternate_residue_position_requests_ready"] = (
                expected_alternate_residue_request_count == 0
                or (
                    alternate_residue_request_present
                    and bool(
                        alternate_residue_request_meta.get("sourcing_request_ready")
                    )
                    and alternate_residue_request_count
                    >= expected_alternate_residue_request_count
                    and alternate_residue_request_countable_count == 0
                )
            )
        if review_only_import_safety_audit is not None:
            gates["review_only_import_safety_audit_ready"] = (
                import_safety_present
                and bool(import_safety_meta.get("countable_import_safe"))
                and import_safety_new_count == 0
            )
        if atp_phosphoryl_transfer_family_expansion is not None:
            gates["atp_phosphoryl_transfer_family_expansion_ready"] = (
                atp_family_expansion_ready
            )
        blockers = [name for name, passed in gates.items() if not passed]
    if active_expert_label_decision_entry_ids and not expert_label_decision_export_present:
        review_warnings.append("expert_label_decision_review_export_missing")
    elif expert_label_decision_export_missing_entry_ids:
        review_warnings.append("expert_label_decision_review_export_incomplete")
    if active_expert_label_decision_entry_ids:
        review_warnings.append("expert_label_decision_rows_require_external_review")
    if (
        active_expert_label_decision_entry_ids
        and not expert_label_decision_repair_present
    ):
        review_warnings.append("expert_label_decision_repair_candidates_missing")
    elif expert_label_decision_repair_missing_entry_ids:
        review_warnings.append("expert_label_decision_repair_candidates_incomplete")
    if (
        active_expert_label_decision_entry_ids
        and not expert_label_decision_repair_guardrail_present
    ):
        review_warnings.append("expert_label_decision_repair_guardrail_audit_missing")
    elif expert_label_decision_repair_guardrail_countable_count:
        review_warnings.append(
            "expert_label_decision_repair_guardrail_countable_candidates"
        )
    elif expert_label_decision_repair_guardrail_meta.get("priority_repair_row_count"):
        review_warnings.append(
            "expert_label_decision_priority_repair_lanes_review_only"
        )
    if (
        active_expert_label_decision_entry_ids
        and expert_label_decision_priority_repair_count > 0
        and not expert_label_decision_local_gap_present
    ):
        review_warnings.append("expert_label_decision_local_evidence_gap_audit_missing")
    elif expert_label_decision_local_gap_missing_entry_ids:
        review_warnings.append("expert_label_decision_local_evidence_gap_audit_incomplete")
    elif expert_label_decision_local_gap_meta.get("local_evidence_gap_class_counts"):
        review_warnings.append(
            "expert_label_decision_local_evidence_gaps_remain_review_only"
        )
    if (
        active_expert_label_decision_entry_ids
        and expert_label_decision_priority_repair_count > 0
        and not expert_label_decision_local_export_present
    ):
        review_warnings.append(
            "expert_label_decision_local_evidence_review_export_missing"
        )
    elif (
        expert_label_decision_local_export_present
        and not expert_label_decision_local_export_meta.get("export_ready")
    ):
        review_warnings.append(
            "expert_label_decision_local_evidence_review_export_not_ready"
        )
    if (
        expert_label_decision_local_evidence_repair_resolution is not None
        and not expert_label_decision_local_resolution_present
    ):
        review_warnings.append(
            "expert_label_decision_local_evidence_repair_resolution_missing"
        )
    elif expert_label_decision_local_resolution_countable_count:
        review_warnings.append(
            "expert_label_decision_local_evidence_repair_resolution_countable_candidates"
        )
    if (
        explicit_alternate_residue_position_requests is not None
        and not alternate_residue_request_present
    ):
        review_warnings.append("explicit_alternate_residue_position_requests_missing")
    elif alternate_residue_request_countable_count:
        review_warnings.append(
            "explicit_alternate_residue_position_requests_countable_candidates"
        )
    if review_only_import_safety_audit is not None and not import_safety_present:
        review_warnings.append("review_only_import_safety_audit_missing")
    elif import_safety_new_count:
        review_warnings.append("review_only_import_safety_audit_found_countable_growth")
    if (
        atp_phosphoryl_transfer_family_expansion is not None
        and not atp_family_expansion_present
    ):
        review_warnings.append("atp_phosphoryl_transfer_family_expansion_missing")
    elif atp_phosphoryl_transfer_family_expansion is not None and not atp_family_expansion_ready:
        review_warnings.append("atp_phosphoryl_transfer_family_expansion_not_ready")

    reaction_failure_mode = _scaling_failure_mode_summary(
        "reaction_direction_or_substrate_class_mismatch",
        issue_rows,
        "reaction_or_substrate_class_mismatch",
        "not_observed_in_new_review_debt",
        extra_evidence={
            "reaction_substrate_mismatch_audit_present": (
                reaction_mismatch_audit_present
            ),
            "reaction_substrate_mismatch_audit_entry_ids": (
                reaction_mismatch_audit_entry_ids
            ),
            "reaction_substrate_mismatch_audit_reason_counts": (
                reaction_mismatch_meta.get("mismatch_reason_counts", {})
            ),
        },
    )
    if reaction_mismatch_audit_entry_ids:
        combined_reaction_ids = _sorted_entry_ids(
            set(reaction_failure_mode.get("entry_ids", []))
            | set(reaction_mismatch_audit_entry_ids)
        )
        reaction_failure_mode["status"] = "observed"
        reaction_failure_mode["issue_count"] = len(combined_reaction_ids)
        reaction_failure_mode["entry_ids"] = combined_reaction_ids
        reaction_failure_mode["evidence"]["entry_ids"] = combined_reaction_ids

    failure_modes = [
        _scaling_failure_mode_summary(
            "ontology_node_scope_pressure",
            issue_rows,
            "ontology_scope_pressure",
            "not_observed_in_new_review_debt",
        ),
        _scaling_failure_mode_summary(
            "sibling_mechanism_confusion",
            issue_rows,
            "sibling_mechanism_confusion",
            "not_observed_in_new_review_debt",
        ),
        _scaling_failure_mode_summary(
            "family_propagation_cross_boundary",
            issue_rows,
            "family_propagation_boundary",
            "guardrails_present_no_new_cross_boundary_debt",
            extra_evidence={
                "guardrail_blocker_counts": dict(sorted(family_blocker_counts.items())),
            },
        ),
        {
            "id": "sequence_family_leakage",
            "status": "guardrail_active",
            "issue_count": 0,
            "entry_ids": [],
            "evidence": {
                "local_proxy_rule": family_meta.get("local_proxy_rule"),
                "source_guardrails": family_meta.get("source_guardrails", []),
            },
        },
        {
            "id": "overcounted_paralogs_or_near_duplicates",
            "status": near_duplicate_audit_status,
            "issue_count": len(near_duplicate_entry_ids),
            "entry_ids": near_duplicate_entry_ids,
            "evidence": {
                "audited_entry_ids": duplicate_audit_entry_ids,
                "entry_to_sequence_cluster": {
                    entry_id: sequence_cluster_by_entry[entry_id]
                    for entry_id in duplicate_audit_entry_ids
                    if entry_id in sequence_cluster_by_entry
                },
                "overrepresented_sequence_cluster_counts": dict(
                    sorted(overrepresented_sequence_clusters.items())
                ),
                "sequence_cluster_missing_entry_count": sequence_cluster_missing_entry_count,
                "reason": None
                if sequence_clusters is not None
                else (
                    "current local artifacts do not include sequence-cluster "
                    "membership; keep this as an explicit audit gap before "
                    "larger-scale propagation"
                ),
            },
        },
        _scaling_failure_mode_summary(
            "cofactor_family_ambiguity",
            issue_rows,
            "cofactor_family_ambiguity",
            "not_observed_in_new_review_debt",
        ),
        _scaling_failure_mode_summary(
            "multi_domain_or_mixed_evidence",
            issue_rows,
            "multi_domain_or_mixed_evidence",
            "not_observed_in_new_review_debt",
        ),
        reaction_failure_mode,
        {
            "id": "atp_phosphoryl_transfer_family_boundary",
            "status": "guardrail_clean"
            if atp_family_expansion_ready
            else "not_assessed"
            if atp_phosphoryl_transfer_family_expansion is None
            else "observed_needs_repair",
            "issue_count": len(
                atp_family_expansion_meta.get("mapped_required_family_ids", [])
                or []
            )
            if atp_family_expansion_ready
            else int(
                atp_family_expansion_meta.get("unsupported_mapping_count", 0) or 0
            ),
            "entry_ids": [
                str(row.get("entry_id"))
                for row in (atp_phosphoryl_transfer_family_expansion or {}).get(
                    "rows", []
                )
                if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
            ],
            "evidence": {
                "expansion_present": atp_family_expansion_present,
                "mapped_required_family_ids": atp_family_expansion_meta.get(
                    "mapped_required_family_ids", []
                ),
                "unmapped_required_family_ids": atp_family_expansion_meta.get(
                    "unmapped_required_family_ids", []
                ),
                "countable_label_candidate_count": (
                    atp_family_expansion_countable_count
                ),
                "boundary_guardrail_ready": atp_family_expansion_meta.get(
                    "boundary_guardrail_ready"
                ),
            },
        },
        _scaling_failure_mode_summary(
            "active_site_residue_remapping_error",
            issue_rows,
            "active_site_mapping_gap",
            "not_observed_in_new_review_debt",
            extra_evidence={
                "structure_mapping_issue_count": mapping_meta.get("issue_count"),
                "structure_mapping_status_counts": mapping_meta.get("status_counts", {}),
            },
        ),
        {
            "id": "conservative_remap_local_evidence_without_explicit_alt_positions",
            "status": "observed"
            if remap_local_strict_guardrail_ids
            else "not_observed"
            if remap_local_audit_present
            else "not_assessed_no_remap_local_lead_audit",
            "issue_count": len(remap_local_strict_guardrail_ids),
            "entry_ids": remap_local_strict_guardrail_ids,
            "evidence": {
                "remap_local_lead_audit_present": remap_local_audit_present,
                "expert_family_boundary_review_entry_ids": remap_local_expert_review_ids,
                "expert_reaction_substrate_review_entry_ids": (
                    remap_local_reaction_review_ids
                ),
                "local_structure_selection_rule_candidate_entry_ids": (
                    remap_local_structure_rule_ids
                ),
                "countable_label_candidate_count": (
                    remap_local_countable_candidate_count
                ),
                "review_rule": remap_local_meta.get("decision_rule"),
            },
        },
        _scaling_failure_mode_summary(
            "structure_sequence_id_mismatch",
            issue_rows,
            "structure_sequence_id_mismatch",
            "not_observed_in_new_review_debt",
            extra_evidence={
                "structure_mapping_issue_count": mapping_meta.get("issue_count"),
                "structure_mapping_status_counts": mapping_meta.get("status_counts", {}),
            },
        ),
        {
            "id": "hard_negatives_concentrated_in_one_family",
            "status": "not_observed_zero_hard_negatives"
            if not hard_family_counts and not near_miss_family_counts
            else "observed",
            "issue_count": sum(hard_family_counts.values()) + sum(near_miss_family_counts.values()),
            "entry_ids": [],
            "evidence": {
                "hard_negative_top1_fingerprint_counts": dict(
                    sorted(hard_family_counts.items())
                ),
                "near_miss_top1_fingerprint_counts": dict(
                    sorted(near_miss_family_counts.items())
                ),
            },
        },
        {
            "id": "review_queue_collapse_to_one_chemistry",
            "status": "observed" if queue_concentrated else "not_observed",
            "issue_count": dominant_family[1] if queue_concentrated and dominant_family else 0,
            "entry_ids": [],
            "evidence": {
                "active_queue_top1_ontology_family_counts": dict(
                    sorted(active_family_counts.items())
                ),
                "dominant_family": dominant_family[0] if dominant_family else None,
                "dominant_family_fraction": dominant_family_fraction,
                "underrepresented_queue_entry_count": len(underrepresented_queue_entry_ids),
                "omitted_underrepresented_queue_entry_ids": omitted_underrepresented_entry_ids,
            },
        },
        {
            "id": "expert_label_decision_review_only_debt",
            "status": "observed"
            if active_expert_label_decision_entry_ids
            else "not_observed",
            "issue_count": len(active_expert_label_decision_entry_ids),
            "entry_ids": active_expert_label_decision_entry_ids,
            "evidence": {
                "expert_label_decision_review_export_present": (
                    expert_label_decision_export_present
                ),
                "exported_entry_ids": expert_label_decision_export_entry_ids,
                "missing_entry_ids": expert_label_decision_export_missing_entry_ids,
                "countable_label_candidate_count": (
                    expert_label_decision_export_countable_count
                ),
                "quality_risk_flag_counts": (
                    expert_label_decision_export_meta.get(
                        "quality_risk_flag_counts", {}
                    )
                ),
                "repair_candidates_present": expert_label_decision_repair_present,
                "repair_candidate_entry_ids": expert_label_decision_repair_entry_ids,
                "repair_candidate_count": (
                    expert_label_decision_repair_candidate_count
                ),
                "repair_candidate_entry_id_count_matches": (
                    expert_label_decision_repair_entry_id_count_matches
                ),
                "repair_missing_entry_ids": (
                    expert_label_decision_repair_missing_entry_ids
                ),
                "repair_bucket_counts": (
                    expert_label_decision_repair_meta.get("repair_bucket_counts", {})
                ),
                "repair_countable_label_candidate_count": (
                    expert_label_decision_repair_countable_count
                ),
                "repair_guardrail_audit_present": (
                    expert_label_decision_repair_guardrail_present
                ),
                "repair_guardrail_priority_repair_row_count": (
                    expert_label_decision_repair_guardrail_meta.get(
                        "priority_repair_row_count"
                    )
                ),
                "repair_guardrail_local_evidence_review_only_entry_ids": (
                    expert_label_decision_repair_guardrail_meta.get(
                        "local_expected_family_evidence_review_only_entry_ids",
                        [],
                    )
                ),
                "repair_guardrail_countable_label_candidate_count": (
                    expert_label_decision_repair_guardrail_countable_count
                ),
                "local_evidence_gap_audit_present": (
                    expert_label_decision_local_gap_present
                ),
                "local_evidence_gap_audit_ready": (
                    expert_label_decision_local_gap_meta.get("audit_ready")
                ),
                "local_evidence_gap_audited_entry_count": (
                    expert_label_decision_local_gap_audited_count
                ),
                "local_evidence_gap_missing_entry_ids": (
                    expert_label_decision_local_gap_missing_entry_ids
                ),
                "local_evidence_gap_class_counts": (
                    expert_label_decision_local_gap_meta.get(
                        "local_evidence_gap_class_counts", {}
                    )
                ),
                "local_evidence_gap_countable_label_candidate_count": (
                    expert_label_decision_local_gap_countable_count
                ),
                "local_evidence_review_export_present": (
                    expert_label_decision_local_export_present
                ),
                "local_evidence_review_export_ready": (
                    expert_label_decision_local_export_meta.get("export_ready")
                ),
                "local_evidence_review_export_exported_count": (
                    expert_label_decision_local_export_count
                ),
                "local_evidence_review_export_countable_label_candidate_count": (
                    expert_label_decision_local_export_countable_count
                ),
                "local_evidence_repair_resolution_present": (
                    expert_label_decision_local_resolution_present
                ),
                "local_evidence_repair_resolution_ready": (
                    expert_label_decision_local_resolution_meta.get(
                        "resolution_ready"
                    )
                ),
                "local_evidence_repair_resolution_resolved_entry_count": (
                    expert_label_decision_local_resolution_resolved_count
                ),
                "local_evidence_repair_resolution_resolved_entry_ids": (
                    expert_label_decision_local_resolution_meta.get(
                        "resolved_entry_ids", []
                    )
                ),
                "local_evidence_repair_resolution_remaining_open_entry_count": (
                    expert_label_decision_local_resolution_meta.get(
                        "remaining_open_entry_count"
                    )
                ),
                "local_evidence_repair_resolution_countable_label_candidate_count": (
                    expert_label_decision_local_resolution_countable_count
                ),
                "explicit_alternate_residue_position_requests_present": (
                    alternate_residue_request_present
                ),
                "explicit_alternate_residue_position_requests_ready": (
                    alternate_residue_request_meta.get("sourcing_request_ready")
                ),
                "explicit_alternate_residue_position_requests_expected_count": (
                    expected_alternate_residue_request_count
                ),
                "explicit_alternate_residue_position_requests_count": (
                    alternate_residue_request_count
                ),
                "explicit_alternate_residue_position_request_entry_ids": (
                    alternate_residue_request_meta.get("request_entry_ids", [])
                ),
                "explicit_alternate_residue_position_requests_countable_label_candidate_count": (
                    alternate_residue_request_countable_count
                ),
                "review_only_import_safety_audit_present": import_safety_present,
                "review_only_import_safety_audit_ready": (
                    import_safety_meta.get("countable_import_safe")
                ),
                "review_only_import_safety_audit_artifact_count": (
                    import_safety_meta.get("artifact_count")
                ),
                "review_only_import_safety_audit_total_new_countable_label_count": (
                    import_safety_new_count
                ),
                "review_only_import_safety_audit_unsafe_artifacts": (
                    import_safety_meta.get("unsafe_artifacts", [])
                ),
                "review_only_rule": expert_label_decision_export_meta.get(
                    "review_only_rule"
                ),
            },
        },
        _scaling_failure_mode_summary(
            "text_leakage_without_mechanistic_evidence",
            issue_rows,
            "text_leakage_risk",
            "not_observed_in_new_review_debt",
        ),
    ]
    audit_recommendation = (
        "do_not_promote_until_quality_repair"
        if blockers
        else str(readiness_meta.get("promotion_recommendation") or "promotion_quality_audit_clean")
    )
    return {
        "metadata": {
            "method": "label_scaling_quality_audit",
            "batch_id": batch_id,
            "source_acceptance_method": acceptance_meta.get("method"),
            "readiness_recommendation": readiness_meta.get("promotion_recommendation"),
            "audit_recommendation": audit_recommendation,
            "new_review_debt_count": len(new_debt_ids),
            "new_review_debt_entry_ids": new_debt_ids,
            "accepted_new_debt_count": len(accepted_new_debt_ids),
            "accepted_new_debt_entry_ids": accepted_new_debt_ids,
            "accepted_clean_label_count": len(accepted_clean_ids),
            "accepted_clean_label_entry_ids": accepted_clean_ids,
            "unclassified_new_review_debt_entry_ids": unclassified_new_debt_ids,
            "underrepresented_queue_entry_count": len(underrepresented_queue_entry_ids),
            "omitted_underrepresented_queue_entry_ids": omitted_underrepresented_entry_ids,
            "near_duplicate_audit_status": near_duplicate_audit_status,
            "near_duplicate_entry_ids": near_duplicate_entry_ids,
            "sequence_cluster_missing_entry_count": sequence_cluster_missing_entry_count,
            "alternate_structure_scan_present": alternate_scan_meta.get("method")
            == "review_debt_alternate_structure_scan",
            "alternate_structure_scan_expected_family_hit_entry_ids": (
                alternate_scan_expected_hits
            ),
            "alternate_structure_scan_local_expected_family_hit_entry_ids": (
                alternate_scan_local_hits
            ),
            "alternate_structure_scan_remapped_residue_position_entry_ids": (
                alternate_scan_remapped_positions
            ),
            "alternate_structure_scan_alternate_pdb_remapped_residue_position_entry_ids": (
                alternate_scan_alternate_remapped_positions
            ),
            "alternate_structure_scan_local_expected_family_hit_from_remap_entry_ids": (
                alternate_scan_remapped_local_hits
            ),
            "alternate_structure_scan_remapped_residue_position_structure_count": int(
                alternate_scan_meta.get("remapped_residue_position_structure_count", 0)
                or 0
            ),
            "alternate_structure_scan_alternate_pdb_remapped_residue_position_structure_count": int(
                alternate_scan_meta.get(
                    "alternate_pdb_remapped_residue_position_structure_count", 0
                )
                or 0
            ),
            "alternate_structure_scan_structure_wide_hit_without_local_support_entry_ids": (
                alternate_scan_structure_wide_hits
            ),
            "alternate_structure_scan_fetch_failure_count": (
                alternate_scan_fetch_failure_count
            ),
            "remap_local_lead_audit_present": remap_local_audit_present,
            "remap_local_lead_audit_countable_label_candidate_count": (
                remap_local_countable_candidate_count
            ),
            "remap_local_lead_audit_strict_guardrail_entry_ids": (
                remap_local_strict_guardrail_ids
            ),
            "remap_local_lead_audit_expert_family_boundary_review_entry_ids": (
                remap_local_expert_review_ids
            ),
            "remap_local_lead_audit_expert_reaction_substrate_review_entry_ids": (
                remap_local_reaction_review_ids
            ),
            "remap_local_lead_audit_local_structure_selection_rule_candidate_entry_ids": (
                remap_local_structure_rule_ids
            ),
            "family_guardrail_reaction_substrate_mismatch_count": int(
                family_meta.get("reaction_substrate_mismatch_count", 0) or 0
            ),
            "family_guardrail_reaction_substrate_mismatch_reason_counts": (
                family_meta.get("reaction_substrate_mismatch_reason_counts", {})
            ),
            "family_guardrail_reaction_substrate_mismatch_label_state_counts": (
                family_meta.get("reaction_substrate_mismatch_label_state_counts", {})
            ),
            "reaction_substrate_mismatch_audit_present": (
                reaction_mismatch_audit_present
            ),
            "reaction_substrate_mismatch_audit_entry_ids": (
                reaction_mismatch_audit_entry_ids
            ),
            "reaction_substrate_mismatch_audit_count": int(
                reaction_mismatch_meta.get("mismatch_count", 0) or 0
            ),
            "reaction_substrate_mismatch_review_export_present": (
                reaction_mismatch_review_export_present
            ),
            "reaction_substrate_mismatch_review_export_entry_ids": (
                reaction_mismatch_review_export_entry_ids
            ),
            "reaction_substrate_mismatch_review_export_missing_entry_ids": (
                reaction_mismatch_review_export_missing_entry_ids
            ),
            "expected_reaction_substrate_mismatch_review_entry_ids": (
                expected_reaction_mismatch_review_entry_ids
            ),
            "reaction_substrate_mismatch_review_export_recommended_path": (
                reaction_mismatch_export_meta.get("recommended_path")
            ),
            "active_queue_expert_label_decision_entry_ids": (
                active_expert_label_decision_entry_ids
            ),
            "expert_label_decision_review_export_present": (
                expert_label_decision_export_present
            ),
            "expert_label_decision_review_export_entry_ids": (
                expert_label_decision_export_entry_ids
            ),
            "expert_label_decision_review_export_missing_entry_ids": (
                expert_label_decision_export_missing_entry_ids
            ),
            "expert_label_decision_review_export_countable_label_candidate_count": (
                expert_label_decision_export_countable_count
            ),
            "expert_label_decision_review_export_quality_risk_flag_counts": (
                expert_label_decision_export_meta.get("quality_risk_flag_counts", {})
            ),
            "expert_label_decision_repair_candidates_present": (
                expert_label_decision_repair_present
            ),
            "expert_label_decision_repair_candidate_entry_ids": (
                expert_label_decision_repair_entry_ids
            ),
            "expert_label_decision_repair_candidate_count": (
                expert_label_decision_repair_candidate_count
            ),
            "expert_label_decision_repair_candidate_entry_id_count_matches": (
                expert_label_decision_repair_entry_id_count_matches
            ),
            "expert_label_decision_repair_candidates_missing_entry_ids": (
                expert_label_decision_repair_missing_entry_ids
            ),
            "expert_label_decision_repair_candidates_countable_label_candidate_count": (
                expert_label_decision_repair_countable_count
            ),
            "expert_label_decision_repair_bucket_counts": (
                expert_label_decision_repair_meta.get("repair_bucket_counts", {})
            ),
            "expert_label_decision_repair_guardrail_audit_present": (
                expert_label_decision_repair_guardrail_present
            ),
            "expert_label_decision_repair_guardrail_priority_repair_row_count": (
                expert_label_decision_repair_guardrail_meta.get(
                    "priority_repair_row_count"
                )
            ),
            "expert_label_decision_repair_guardrail_local_evidence_review_only_count": (
                expert_label_decision_repair_guardrail_meta.get(
                    "local_expected_family_evidence_review_only_count"
                )
            ),
            "expert_label_decision_repair_guardrail_countable_label_candidate_count": (
                expert_label_decision_repair_guardrail_countable_count
            ),
            "expert_label_decision_local_evidence_gap_audit_present": (
                expert_label_decision_local_gap_present
            ),
            "expert_label_decision_local_evidence_gap_audit_ready": (
                expert_label_decision_local_gap_meta.get("audit_ready")
            ),
            "expert_label_decision_local_evidence_gap_audit_audited_entry_count": (
                expert_label_decision_local_gap_audited_count
            ),
            "expert_label_decision_local_evidence_gap_audit_missing_entry_ids": (
                expert_label_decision_local_gap_missing_entry_ids
            ),
            "expert_label_decision_local_evidence_gap_audit_countable_label_candidate_count": (
                expert_label_decision_local_gap_countable_count
            ),
            "expert_label_decision_local_evidence_gap_class_counts": (
                expert_label_decision_local_gap_meta.get(
                    "local_evidence_gap_class_counts", {}
                )
            ),
            "expert_label_decision_local_evidence_review_export_present": (
                expert_label_decision_local_export_present
            ),
            "expert_label_decision_local_evidence_review_export_ready": (
                expert_label_decision_local_export_meta.get("export_ready")
            ),
            "expert_label_decision_local_evidence_review_export_exported_count": (
                expert_label_decision_local_export_count
            ),
            "expert_label_decision_local_evidence_review_export_all_source_rows_exported": (
                expert_label_decision_local_export_meta.get(
                    "all_source_rows_exported"
                )
            ),
            "expert_label_decision_local_evidence_review_export_countable_label_candidate_count": (
                expert_label_decision_local_export_countable_count
            ),
            "expert_label_decision_local_evidence_review_export_decision_counts": (
                expert_label_decision_local_export_decision_counts
            ),
            "expert_label_decision_local_evidence_repair_resolution_present": (
                expert_label_decision_local_resolution_present
            ),
            "expert_label_decision_local_evidence_repair_resolution_ready": (
                expert_label_decision_local_resolution_meta.get("resolution_ready")
            ),
            "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count": (
                expert_label_decision_local_resolution_resolved_count
            ),
            "expert_label_decision_local_evidence_repair_resolution_resolved_entry_ids": (
                expert_label_decision_local_resolution_meta.get("resolved_entry_ids", [])
            ),
            "expert_label_decision_local_evidence_repair_resolution_remaining_open_entry_count": (
                expert_label_decision_local_resolution_meta.get(
                    "remaining_open_entry_count"
                )
            ),
            "expert_label_decision_local_evidence_repair_resolution_countable_label_candidate_count": (
                expert_label_decision_local_resolution_countable_count
            ),
            "explicit_alternate_residue_position_requests_present": (
                alternate_residue_request_present
            ),
            "explicit_alternate_residue_position_requests_ready": (
                alternate_residue_request_meta.get("sourcing_request_ready")
            ),
            "explicit_alternate_residue_position_requests_expected_count": (
                expected_alternate_residue_request_count
            ),
            "explicit_alternate_residue_position_requests_count": (
                alternate_residue_request_count
            ),
            "explicit_alternate_residue_position_request_entry_ids": (
                alternate_residue_request_meta.get("request_entry_ids", [])
            ),
            "explicit_alternate_residue_position_requests_countable_label_candidate_count": (
                alternate_residue_request_countable_count
            ),
            "review_only_import_safety_audit_present": import_safety_present,
            "review_only_import_safety_audit_ready": (
                import_safety_meta.get("countable_import_safe")
            ),
            "review_only_import_safety_audit_artifact_count": (
                import_safety_meta.get("artifact_count")
            ),
            "review_only_import_safety_audit_total_new_countable_label_count": (
                import_safety_new_count
            ),
            "review_only_import_safety_audit_unsafe_artifacts": (
                import_safety_meta.get("unsafe_artifacts", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_present": (
                atp_family_expansion_present
            ),
            "atp_phosphoryl_transfer_family_expansion_ready": (
                atp_family_expansion_ready
            ),
            "atp_phosphoryl_transfer_family_expansion_mapped_family_ids": (
                atp_family_expansion_meta.get("mapped_required_family_ids", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_unmapped_family_ids": (
                atp_family_expansion_meta.get("unmapped_required_family_ids", [])
            ),
            "atp_phosphoryl_transfer_family_expansion_countable_label_candidate_count": (
                atp_family_expansion_countable_count
            ),
            "issue_class_counts": dict(sorted(issue_class_counts.items())),
            "audit_rule": (
                "before promoting a preview batch, classify new ontology, "
                "family-propagation, cofactor, mapping, queue-composition, "
                "hard-negative, and text-leakage failure modes; accepted labels "
                "with unresolved review debt are not promotion-ready"
            ),
        },
        "gates": gates,
        "blockers": blockers,
        "review_warnings": review_warnings,
        "failure_modes": failure_modes,
        "rows": issue_rows,
    }


def _label_scaling_issue_classes(
    row: dict[str, Any],
    *,
    family_guardrail_row: dict[str, Any],
    structure_mapping_row: dict[str, Any],
    decision_action: str,
) -> list[str]:
    gap_reasons = {str(reason) for reason in row.get("gap_reasons", []) if str(reason)}
    counterevidence = {
        str(reason) for reason in row.get("counterevidence_reasons", []) if str(reason)
    }
    coverage_status = str(row.get("coverage_status", "unknown"))
    target = row.get("target_fingerprint_id")
    top1 = row.get("top1_fingerprint_id")
    target_family = fingerprint_family(str(target)) if isinstance(target, str) else None
    top1_family = fingerprint_family(str(top1)) if isinstance(top1, str) else None
    guardrail_blockers = {
        str(blocker)
        for blocker in family_guardrail_row.get("propagation_blockers", [])
        if str(blocker)
    }
    rationale = str(row.get("decision_rationale", ""))
    mapping_status = str(structure_mapping_row.get("status", "ok"))
    text = " ".join(
        [
            str(row.get("entry_name", "")),
            rationale,
            " ".join(str(snippet) for snippet in row.get("mechanism_text_snippets", [])),
        ]
    ).lower()
    issue_classes: set[str] = set()
    if (
        "top1_below_abstention_threshold" in gap_reasons
        or "target_not_top1" in gap_reasons
        or (decision_action == "mark_needs_more_evidence" and "boundary" in rationale)
        or (decision_action == "accept_label" and gap_reasons)
    ):
        issue_classes.add("ontology_scope_pressure")
    if (
        isinstance(target, str)
        and isinstance(top1, str)
        and target != top1
        and target_family
        and target_family == top1_family
    ):
        issue_classes.add("sibling_mechanism_confusion")
    if (
        (target_family and top1_family and target_family != top1_family)
        or "target_family_top1_family_mismatch" in guardrail_blockers
        or "close_cross_family_top1_top2" in guardrail_blockers
    ):
        issue_classes.add("family_propagation_boundary")
    if (
        coverage_status in {"expected_absent_from_structure", "expected_structure_only"}
        or any("cofactor" in reason or "heme" in reason or "flavin" in reason or "metal" in reason for reason in counterevidence)
    ):
        issue_classes.add("cofactor_family_ambiguity")
    if "domain" in text or len(row.get("structure_cofactor_families", []) or []) > 1:
        issue_classes.add("multi_domain_or_mixed_evidence")
    if (
        "reaction_substrate_mismatch" in guardrail_blockers
        or _has_reaction_or_substrate_mismatch(text, str(top1 or ""), str(target or ""))
    ):
        issue_classes.add("reaction_or_substrate_class_mismatch")
    if (
        mapping_status not in {"ok", "None"}
        or "fewer_than_three_resolved_residues" in rationale
        or "geometry_status_not_ok" in rationale
    ):
        issue_classes.add("active_site_mapping_gap")
    if mapping_status in {"no_structure_positions", "structure_fetch_failed"}:
        issue_classes.add("structure_sequence_id_mismatch")
    if decision_action == "accept_label" and (
        gap_reasons
        or counterevidence
        or coverage_status in COFACTOR_EVIDENCE_LIMITED_STATUSES
    ):
        issue_classes.add("text_leakage_risk")
    if decision_action == "mark_needs_more_evidence" and counterevidence:
        issue_classes.add("text_leakage_risk")
    if (
        decision_action == "mark_needs_more_evidence"
        and "review_marked_needs_more_evidence" in gap_reasons
        and not issue_classes
    ):
        issue_classes.add("expert_review_decision_needed")
    return sorted(issue_classes)


def _has_reaction_or_substrate_mismatch(text: str, top1: str, target: str) -> bool:
    fingerprint_text = f"{top1} {target}".lower()
    redox_terms = ("oxid", "reduct", "redox", "hydride", "electron", "dioxygenase")
    transfer_terms = ("kinase", "phosphotransferase", "ligase", "transferase")
    hydrolysis_terms = ("hydrolase", "hydrolysis", "glycosidic", "peptidase", "esterase")
    if "hydrolase" in fingerprint_text and any(term in text for term in redox_terms):
        return True
    if "hydrolase" in fingerprint_text and any(term in text for term in transfer_terms):
        return True
    if (
        ("flavin" in fingerprint_text or "heme" in fingerprint_text)
        and any(term in text for term in hydrolysis_terms)
    ):
        return True
    return False


def _scaling_failure_mode_summary(
    mode_id: str,
    rows: list[dict[str, Any]],
    issue_class: str,
    clean_status: str,
    extra_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matching_rows = [
        row for row in rows if issue_class in set(row.get("issue_classes", []))
    ]
    entry_ids = sorted(
        (str(row["entry_id"]) for row in matching_rows),
        key=_entry_id_sort_key,
    )
    evidence: dict[str, Any] = {
        "issue_class": issue_class,
        "entry_ids": entry_ids,
    }
    if extra_evidence:
        evidence.update(extra_evidence)
    return {
        "id": mode_id,
        "status": "observed" if matching_rows else clean_status,
        "issue_count": len(matching_rows),
        "entry_ids": entry_ids,
        "evidence": evidence,
    }


def _sequence_cluster_by_entry(sequence_clusters: dict[str, Any] | None) -> dict[str, str]:
    if not isinstance(sequence_clusters, dict):
        return {}
    cluster_by_entry: dict[str, str] = {}
    row_keys = ("rows", "items", "entries", "results")
    cluster_keys = (
        "id",
        "sequence_cluster_id",
        "cluster_id",
        "uniref_cluster_id",
        "sequence_family_id",
        "representative_id",
    )
    for row_key in row_keys:
        rows = sequence_clusters.get(row_key)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
                continue
            cluster_id = next(
                (
                    str(row[key])
                    for key in cluster_keys
                    if row.get(key) is not None and str(row.get(key))
                ),
                None,
            )
            if cluster_id:
                cluster_by_entry[str(row["entry_id"])] = cluster_id
    clusters = sequence_clusters.get("clusters")
    if isinstance(clusters, dict):
        for cluster_id, members in clusters.items():
            for member in (members if isinstance(members, list) else []):
                if isinstance(member, str):
                    cluster_by_entry[member] = str(cluster_id)
                elif isinstance(member, dict) and isinstance(member.get("entry_id"), str):
                    cluster_by_entry[str(member["entry_id"])] = str(cluster_id)
    elif isinstance(clusters, list):
        for cluster in clusters:
            if not isinstance(cluster, dict):
                continue
            cluster_id = next(
                (
                    str(cluster[key])
                    for key in cluster_keys
                    if cluster.get(key) is not None and str(cluster.get(key))
                ),
                None,
            )
            members = cluster.get("entry_ids") or cluster.get("members") or []
            if not cluster_id or not isinstance(members, list):
                continue
            for member in members:
                if isinstance(member, str):
                    cluster_by_entry[member] = cluster_id
                elif isinstance(member, dict) and isinstance(member.get("entry_id"), str):
                    cluster_by_entry[str(member["entry_id"])] = cluster_id
    return cluster_by_entry


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
        entry_name = str(result.get("entry_name") or entry.get("entry_name") or "")
        mechanism_text_snippets = result.get("mechanism_text_snippets") or entry.get(
            "mechanism_text_snippets", []
        )
        reaction_mismatch_reasons = _remap_local_reaction_substrate_mismatch_reasons(
            entry_name=entry_name,
            mechanism_text_snippets=mechanism_text_snippets,
            top1_fingerprint_id=top1_id,
        )
        atp_family_assignment = _atp_phosphoryl_transfer_family_assignment(
            entry_name=entry_name,
            mechanism_text_snippets=mechanism_text_snippets,
            top1_fingerprint_id=top1_id,
        )
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
            reaction_substrate_mismatch_reasons=reaction_mismatch_reasons,
            atp_phosphoryl_transfer_family_assignment=atp_family_assignment,
        )
        decision = _family_propagation_decision(label, blockers)
        if label and decision == "direct_label_no_propagation_issue":
            continue
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": entry_name,
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
                "reaction_substrate_mismatch_reasons": reaction_mismatch_reasons,
                "atp_phosphoryl_transfer_family": atp_family_assignment,
                "atp_phosphoryl_transfer_family_id": _atp_family_id_from_assignment(
                    atp_family_assignment
                ),
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
                "mechanism_text_snippets": mechanism_text_snippets,
            }
        )
    all_ranked_rows = sorted(
        rows,
        key=lambda row: (
            _family_decision_priority(row["propagation_decision"]),
            _entry_id_sort_key(row["entry_id"]),
        ),
    )
    ranked_rows = all_ranked_rows[:max_rows]
    selected_entry_ids = {row["entry_id"] for row in ranked_rows}
    priority_added_rows = [
        row
        for row in all_ranked_rows[max_rows:]
        if row.get("reaction_substrate_mismatch_reasons")
        and row["entry_id"] not in selected_entry_ids
    ]
    ranked_rows.extend(priority_added_rows)
    decision_counts = Counter(row["propagation_decision"] for row in ranked_rows)
    blocker_counts = Counter(
        blocker for row in ranked_rows for blocker in row["propagation_blockers"]
    )
    reaction_mismatch_reason_counts = Counter(
        reason
        for row in ranked_rows
        for reason in row.get("reaction_substrate_mismatch_reasons", [])
    )
    reaction_mismatch_label_state_counts = Counter(
        str(row.get("label_state"))
        for row in ranked_rows
        if row.get("reaction_substrate_mismatch_reasons")
    )
    atp_family_counts = Counter(
        str(row.get("atp_phosphoryl_transfer_family_id"))
        for row in ranked_rows
        if row.get("atp_phosphoryl_transfer_family_id")
    )
    return {
        "metadata": {
            "method": "family_propagation_guardrail_audit",
            "audited_count": len(rows),
            "reported_count": len(ranked_rows),
            "max_rows": max_rows,
            "priority_added_count": len(priority_added_rows),
            "priority_inclusion_rule": (
                "always retain reaction/substrate mismatch blockers even when "
                "they rank below max_rows"
            ),
            "ontology_version": ontology.get("version"),
            "decision_counts": dict(sorted(decision_counts.items())),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "reaction_substrate_mismatch_count": sum(
                1 for row in ranked_rows if row.get("reaction_substrate_mismatch_reasons")
            ),
            "reaction_substrate_mismatch_reason_counts": dict(
                sorted(reaction_mismatch_reason_counts.items())
            ),
            "reaction_substrate_mismatch_label_state_counts": dict(
                sorted(reaction_mismatch_label_state_counts.items())
            ),
            "atp_phosphoryl_transfer_family_counts": dict(
                sorted(atp_family_counts.items())
            ),
            "atp_phosphoryl_transfer_family_boundary_count": sum(
                atp_family_counts.values()
            ),
            "source_guardrails": ontology.get("propagation_guardrails", []),
            "local_proxy_rule": (
                "when UniRef, CATH, or InterPro evidence is unavailable, mechanism text, "
                "ligand/cofactor context, pocket geometry, and reaction/substrate "
                "mismatch signals can prioritize or block propagation but cannot "
                "promote beyond bronze by themselves"
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
    review_meta = review_artifact.get("metadata", {})
    reaction_mismatch_review_only = (
        review_meta.get("method") == "reaction_substrate_mismatch_review_export"
        or review_meta.get("source_method")
        == "reaction_substrate_mismatch_review_export"
        or bool(review_meta.get("reaction_substrate_mismatch_review_only"))
    )
    expert_label_decision_review_only = (
        review_meta.get("method") == "expert_label_decision_review_export"
        or review_meta.get("source_method") == "expert_label_decision_review_export"
        or bool(review_meta.get("expert_label_decision_review_only"))
    )
    local_evidence_gap_review_only = (
        review_meta.get("method")
        == "expert_label_decision_local_evidence_review_export"
        or review_meta.get("source_method")
        == "expert_label_decision_local_evidence_review_export"
        or bool(review_meta.get("local_evidence_gap_review_only"))
    )
    for item in countable_review.get("review_items", []):
        if not isinstance(item, dict):
            continue
        decision = item.get("decision", {})
        if not isinstance(decision, dict):
            continue
        reaction_resolution = decision.get("reaction_substrate_resolution")
        if (
            decision.get("action") != "accept_label"
            or decision.get("review_status", "expert_reviewed") not in COUNTABLE_REVIEW_STATUSES
            or expert_label_decision_review_only
            or local_evidence_gap_review_only
            or (
                reaction_mismatch_review_only
                and (
                    bool(review_meta.get("reaction_substrate_mismatch_review_only"))
                    or decision.get("review_status") != "expert_reviewed"
                    or reaction_resolution in {None, "needs_more_evidence"}
                )
            )
        ):
            item["decision"] = {**decision, "action": "no_decision"}
    return import_expert_review_decisions(labels, countable_review)


def audit_review_only_import_safety(
    labels: list[MechanismLabel],
    review_artifacts: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    """Audit that review-only decision artifacts do not add countable labels."""
    baseline_entry_ids = {label.entry_id for label in labels}
    rows: list[dict[str, Any]] = []
    for name, artifact in review_artifacts:
        metadata = artifact.get("metadata", {})
        imported = import_countable_review_decisions(labels, artifact)
        imported_entry_ids = {label.entry_id for label in imported}
        new_entry_ids = _sorted_entry_ids(imported_entry_ids - baseline_entry_ids)
        review_only_flags = {
            "reaction_substrate_mismatch_review_only": bool(
                metadata.get("reaction_substrate_mismatch_review_only")
            )
            or metadata.get("method") == "reaction_substrate_mismatch_review_export"
            or metadata.get("source_method")
            == "reaction_substrate_mismatch_review_export",
            "expert_label_decision_review_only": bool(
                metadata.get("expert_label_decision_review_only")
            )
            or metadata.get("method") == "expert_label_decision_review_export"
            or metadata.get("source_method") == "expert_label_decision_review_export",
            "local_evidence_gap_review_only": bool(
                metadata.get("local_evidence_gap_review_only")
            )
            or metadata.get("method")
            == "expert_label_decision_local_evidence_review_export"
            or metadata.get("source_method")
            == "expert_label_decision_local_evidence_review_export",
        }
        is_review_only = any(review_only_flags.values())
        rows.append(
            {
                "artifact": name,
                "method": metadata.get("method"),
                "source_method": metadata.get("source_method"),
                "review_only_flags": review_only_flags,
                "decision_counts": metadata.get("decision_counts", {}),
                "baseline_label_count": len(labels),
                "countable_import_label_count": len(imported),
                "new_countable_label_count": len(new_entry_ids),
                "new_countable_entry_ids": new_entry_ids,
                "countable_import_safe": (not is_review_only) or not new_entry_ids,
                "review_only_rule": (
                    "review-only artifacts must not add benchmark labels through "
                    "countable import"
                )
                if is_review_only
                else None,
            }
        )
    unsafe_rows = [row for row in rows if not row["countable_import_safe"]]
    review_only_rows = [row for row in rows if any(row["review_only_flags"].values())]
    return {
        "metadata": {
            "method": "review_only_import_safety_audit",
            "artifact_count": len(rows),
            "review_only_artifact_count": len(review_only_rows),
            "unsafe_artifact_count": len(unsafe_rows),
            "unsafe_artifacts": [row["artifact"] for row in unsafe_rows],
            "total_new_countable_label_count": sum(
                int(row["new_countable_label_count"]) for row in rows
            ),
            "countable_import_safe": not unsafe_rows,
        },
        "rows": rows,
    }


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
    reaction_substrate_mismatch_reasons: list[str] | None = None,
    atp_phosphoryl_transfer_family_assignment: dict[str, Any] | None = None,
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
    reaction_substrate_mismatch_value = 1.0 if reaction_substrate_mismatch_reasons else 0.0
    atp_family_boundary_value = (
        1.0 if atp_phosphoryl_transfer_family_assignment is not None else 0.0
    )
    return {
        "uncertainty": round(1.4 * uncertainty, 4),
        "impact": round(1.1 * impact, 4),
        "novelty": round(0.7 * novelty + unlabeled_bonus, 4),
        "hard_negative_value": round(1.2 * hard_negative_value, 4),
        "evidence_conflict": round(1.5 * evidence_conflict, 4),
        "family_boundary_value": round(1.1 * family_boundary_value, 4),
        "reaction_substrate_mismatch_value": round(
            1.3 * reaction_substrate_mismatch_value, 4
        ),
        "atp_phosphoryl_family_boundary_value": round(
            1.25 * atp_family_boundary_value, 4
        ),
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
    structural_blockers = {
        blocker
        for blocker in blockers
        if blocker
        in {
            "status_ok",
            "geometry_status_not_ok",
            "resolved_at_least_three_residues",
            "fewer_than_three_resolved_residues",
            "has_pairwise_geometry",
            "missing_pairwise_geometry",
        }
    }

    cobalamin_hint = (
        "cobalamin" in text
        or "co-c5" in text
        or "adenosylcobalamin" in text
        or entry_id == "m_csa:494"
    )
    metal_hydrolysis_hint = top1 == "metal_dependent_hydrolase" and _has_metal_hydrolysis_text(
        text,
        entry_name,
    )
    ser_his_text_hint = _has_ser_his_hydrolase_text(text, entry_name)
    ser_his_metal_boundary = (
        top1 == "metal_dependent_hydrolase"
        and top1_score >= threshold
        and ser_his_text_hint
        and not _has_metal_catalysis_text(text, entry_name)
    )
    non_hydrolytic_metal_boundary = (
        top1 == "metal_dependent_hydrolase"
        and top1_score >= threshold
        and not metal_hydrolysis_hint
    )
    ser_his_hydrolase_hint = (
        top1 == "ser_his_acid_hydrolase"
        and top1_score >= threshold
        and not _has_clear_nonhydrolytic_text(text, entry_name)
        and ser_his_text_hint
    )
    supported_seed = (
        top1_score >= threshold
        and top1
        and cofactor_level != "absent"
        and not counterevidence
        and not structural_blockers
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
    if (
        top1_score >= threshold
        and top1
        and cofactor_level != "absent"
        and not counterevidence
        and structural_blockers
    ):
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": top1,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has retrieval support for {top1}, but selected "
                "active-site geometry is not sufficiently resolved; keep this "
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
    if ser_his_metal_boundary:
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "ser_his_acid_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has Ser-His hydrolase mechanism text, but top "
                f"retrieval favored metal_dependent_hydrolase at {top1_score:.4f} "
                "without explicit metal-catalysis text; keep this candidate in "
                "expert review before counting it."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if non_hydrolytic_metal_boundary:
        boundary_context = (
            " mechanism text supports non-hydrolytic transfer, redox, lyase, "
            "or peroxide chemistry."
            if _has_clear_nonhydrolytic_text(text, entry_name)
            else " the review context lacks explicit hydrolysis text."
        )
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} is a high-scoring metal-hydrolase boundary "
                f"control at {top1_score:.4f};{boundary_context} Keep this "
                "candidate in expert review rather than counting it as either "
                "a seed label or a safe out-of-scope negative."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if (
        top1 == "metal_dependent_hydrolase"
        and top1_score >= threshold
        and cofactor_level != "ligand_supported"
    ):
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "metal_dependent_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has metal-dependent hydrolase retrieval support "
                f"at {top1_score:.4f}, but the current review context reports "
                f"{cofactor_level} metal evidence rather than local ligand support; "
                "keep this candidate in expert review before counting it."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if ser_his_hydrolase_hint and counterevidence:
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "ser_his_acid_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} has Ser-His hydrolase mechanism text and retrieval "
                f"support at {top1_score:.4f}, but counterevidence remains: "
                f"{', '.join(sorted(counterevidence))}. Keep this candidate in "
                "expert review before counting it."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if ser_his_hydrolase_hint:
        return {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "ser_his_acid_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} is provisionally assigned to ser_his_acid_hydrolase: "
                f"retrieval score {top1_score:.4f} clears the {threshold:.4f} floor "
                "and mechanism text supports a Ser-His-Asp/Glu hydrolase triad."
            ),
            "evidence_score": 0.67,
            "review_status": "automation_curated",
        }
    if top1 == "ser_his_acid_hydrolase" and top1_score >= threshold:
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} is a high-scoring Ser-His hydrolase boundary "
                f"candidate at {top1_score:.4f}, but the review context lacks "
                "explicit Ser-His-Asp/Glu triad or alpha-beta hydrolase text; "
                "keep this candidate in expert review before counting it."
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
    if top1_score >= threshold:
        rationale_bits = [
            f"{entry_name} is a non-abstaining boundary candidate: top retrieval "
            f"{top1 or 'none'} scored {top1_score:.4f}, above the {threshold:.4f} "
            "floor, but current automation rules do not support a countable seed "
            "assignment.",
        ]
        if counterevidence:
            rationale_bits.append(
                "Counterevidence: " + ", ".join(sorted(counterevidence)) + "."
            )
        if blockers:
            rationale_bits.append("Review blockers: " + ", ".join(sorted(blockers)) + ".")
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": " ".join(rationale_bits),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }

    cofactor_sensitive_top1 = top1 in {
        "cobalamin_radical_rearrangement",
        "flavin_dehydrogenase_reductase",
        "flavin_monooxygenase",
        "heme_peroxidase_oxidase",
        "metal_dependent_hydrolase",
    }
    evidence_limited_negative = (
        bool(blockers)
        or bool(counterevidence)
        or (cofactor_sensitive_top1 and cofactor_level in {"absent", "structure_only", "role_inferred"})
    )
    cofactor_supported_low_score_negative = (
        top1_score < threshold
        and cofactor_sensitive_top1
        and cofactor_level == "ligand_supported"
        and _has_cofactor_sensitive_seed_text(top1, text, entry_name)
    )
    if top1_score < threshold and evidence_limited_negative:
        rationale_bits = [
            f"{entry_name} remains below the {threshold:.4f} abstention floor, "
            "but it is not a clean countable out-of-scope negative.",
        ]
        if cofactor_sensitive_top1 and cofactor_level in {"absent", "structure_only", "role_inferred"}:
            rationale_bits.append(
                f"Selected-structure cofactor evidence for {top1} is {cofactor_level}."
            )
        if counterevidence:
            rationale_bits.append(
                "Counterevidence: " + ", ".join(sorted(counterevidence)) + "."
            )
        if blockers:
            rationale_bits.append("Review blockers: " + ", ".join(sorted(blockers)) + ".")
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": " ".join(rationale_bits),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }
    if cofactor_supported_low_score_negative:
        return {
            "action": "mark_needs_more_evidence",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": reviewer,
            "rationale": (
                f"{entry_name} remains below the {threshold:.4f} abstention floor, "
                f"but local {cofactor_level} evidence and mechanism text match "
                f"{top1}; keep this candidate in expert review rather than "
                "counting it as a clean out-of-scope negative."
            ),
            "evidence_score": 0.55,
            "review_status": "needs_expert_review",
        }

    confidence = "low" if blockers else "medium"
    rationale_bits = [
        f"{entry_name} is provisionally outside the current seed fingerprints.",
    ]
    if top1_score < threshold:
        rationale_bits.append(
            f"Top retrieval {top1 or 'none'} scored {top1_score:.4f}, below the {threshold:.4f} floor."
        )
    else:
        rationale_bits.append(
            f"Top retrieval {top1 or 'none'} scored {top1_score:.4f}, but current automation rules do not support a countable seed assignment."
        )
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


def _has_metal_hydrolysis_text(text: str, entry_name: str) -> bool:
    combined = f"{entry_name.lower()} {text}"
    direct_terms = {
        "hydrolase",
        "hydrolysis",
        "hydrolyses",
        "hydrolyzes",
        "hydrolysed",
        "hydrolyzed",
        "phosphatase",
        "phosphodiesterase",
        "nuclease",
        "ribonuclease",
        "deoxyribonuclease",
        "esterase",
        "lipase",
        "phospholipase",
    }
    water_attack_terms = {
        "water attacks",
        "water attack",
        "nucleophilic water",
        "metal-activated water",
        "attacking nucleophilic hydroxide",
    }
    return any(term in combined for term in direct_terms | water_attack_terms)


def _has_cofactor_sensitive_seed_text(
    fingerprint_id: str,
    text: str,
    entry_name: str,
) -> bool:
    combined = f"{entry_name.lower()} {text}"
    if fingerprint_id == "heme_peroxidase_oxidase":
        return any(
            term in combined
            for term in {"heme", "haem", "peroxidase", "oxidase"}
        )
    if fingerprint_id in {
        "flavin_dehydrogenase_reductase",
        "flavin_monooxygenase",
    }:
        return any(
            term in combined
            for term in {
                "dehydrogenase",
                "fad",
                "flavin",
                "fmn",
                "monooxygenase",
            }
        )
    if fingerprint_id == "cobalamin_radical_rearrangement":
        return any(
            term in combined
            for term in {"adenosylcobalamin", "b12", "cobalamin"}
        )
    if fingerprint_id == "metal_dependent_hydrolase":
        return _has_metal_hydrolysis_text(text, entry_name)
    return False


def _has_ser_his_hydrolase_text(text: str, entry_name: str) -> bool:
    combined = f"{entry_name.lower()} {text}"
    return any(
        term in combined
        for term in {
            "ser-his",
            "ser his",
            "ser-his-asp",
            "ser-his-glu",
            "serine hydrolase",
            "catalytic triad",
            "triad mechanism",
            "alpha-beta hydrolase",
            "lipase",
        }
    ) or (
        ("ser" in combined or "serine" in combined)
        and ("his" in combined or "histidine" in combined)
        and any(term in combined for term in {"nucleophile", "deprotonates", "base"})
    )


def _has_metal_catalysis_text(text: str, entry_name: str) -> bool:
    combined = f"{entry_name.lower()} {text}"
    return any(
        term in combined
        for term in {
            "zinc",
            "zn",
            "mg2",
            "mg(2",
            "magnesium",
            "mn",
            "manganese",
            "metal ion",
            "metal centre",
            "metal center",
            "metal-dependent",
            "metal dependent",
        }
    )


def _has_clear_nonhydrolytic_text(text: str, entry_name: str) -> bool:
    combined = f"{entry_name.lower()} {text}"
    boundary_terms = {
        "transferase",
        "glycosyltransferase",
        "galactosyltransferase",
        "methyltransferase",
        "hydride transfer",
        "dehydrogenase",
        "reductase",
        "oxidase",
        "catalase",
        "hydrogen peroxide",
        "peroxide",
        "lyase",
        "hydratase",
        "dehydratase",
        "synthase",
        "synthetase",
        "epimerase",
        "isomerase",
        "decarboxylase",
        "carboxylase",
        "dioxygenase",
        "monooxygenase",
    }
    return any(term in combined for term in boundary_terms)


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
    reaction_substrate_mismatch_reasons: list[str] | None = None,
    atp_phosphoryl_transfer_family_assignment: dict[str, Any] | None = None,
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
    if reaction_substrate_mismatch_reasons:
        blockers.append("reaction_substrate_mismatch")
    if atp_phosphoryl_transfer_family_assignment is not None:
        blockers.append("atp_phosphoryl_transfer_family_boundary")
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
