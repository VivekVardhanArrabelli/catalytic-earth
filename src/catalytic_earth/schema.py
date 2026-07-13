"""Versioned, typed interchange objects for the bounded atlas core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SCHEMA_VERSION = "catalytic-earth.mechanism-record.v1"
OBJECT_TYPES = {
    "net_reaction",
    "source_mechanism",
    "mechanism_hypothesis",
    "mechanism_family",
    "protein_annotation_record",
    "experimental_observation",
}


@dataclass(frozen=True)
class EvidenceReference:
    source_id: str
    source_release: str
    evidence_type: str
    source_record_id: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EvidenceReference":
        required = ("source_id", "source_release", "evidence_type", "source_record_id")
        if not isinstance(value, dict) or any(
            not isinstance(value.get(field), str) or not value[field] for field in required
        ):
            raise ValueError("evidence references require four non-empty string fields")
        return cls(**{field: value[field] for field in required})


@dataclass(frozen=True)
class MechanismRecord:
    schema_version: str
    record_id: str
    object_type: str
    evidence_tier: int
    label: str
    fixture_only: bool
    evidence: tuple[EvidenceReference, ...]
    mechanism_steps: tuple[str, ...]
    counterevidence: tuple[str, ...]
    outcome: str | None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "MechanismRecord":
        if not isinstance(value, dict):
            raise ValueError("mechanism record must be an object")
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"unsupported mechanism schema: {value.get('schema_version')!r}")
        if not isinstance(value.get("record_id"), str) or not value["record_id"]:
            raise ValueError("mechanism record requires record_id")
        if value.get("object_type") not in OBJECT_TYPES:
            raise ValueError(f"unsupported object_type: {value.get('object_type')!r}")
        tier = value.get("evidence_tier")
        if not isinstance(tier, int) or isinstance(tier, bool) or tier not in range(5):
            raise ValueError("evidence_tier must be an integer from 0 through 4")
        if not isinstance(value.get("label"), str) or not value["label"]:
            raise ValueError("mechanism record requires label")
        if not isinstance(value.get("fixture_only"), bool):
            raise ValueError("mechanism record fixture_only must be boolean")
        evidence_raw = value.get("evidence")
        if not isinstance(evidence_raw, list):
            raise ValueError("mechanism record evidence must be a list")
        steps = value.get("mechanism_steps", [])
        counterevidence = value.get("counterevidence", [])
        if not isinstance(steps, list) or any(not isinstance(item, str) for item in steps):
            raise ValueError("mechanism_steps must be strings")
        if not isinstance(counterevidence, list) or any(
            not isinstance(item, str) for item in counterevidence
        ):
            raise ValueError("counterevidence must be strings")
        outcome = value.get("outcome")
        if outcome is not None and outcome not in {"positive", "negative", "inconclusive"}:
            raise ValueError("outcome must be positive, negative, inconclusive, or null")
        if value["object_type"] == "experimental_observation" and outcome is None:
            raise ValueError("experimental observations require an outcome")
        return cls(
            schema_version=SCHEMA_VERSION,
            record_id=value["record_id"],
            object_type=value["object_type"],
            evidence_tier=tier,
            label=value["label"],
            fixture_only=value["fixture_only"],
            evidence=tuple(EvidenceReference.from_dict(item) for item in evidence_raw),
            mechanism_steps=tuple(steps),
            counterevidence=tuple(counterevidence),
            outcome=outcome,
        )
