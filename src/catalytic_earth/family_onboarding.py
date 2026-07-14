"""Declarative, proposal-only family onboarding through one shared engine."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .execution_context import ExecutionContext


SCHEMA_VERSION = "catalytic-earth.family-onboarding.v1"


@dataclass(frozen=True)
class SourceQuery:
    source_id: str
    release: str
    query: str
    role: str


@dataclass(frozen=True)
class FamilyOnboardingSpec:
    schema_version: str
    family_id: str
    definition_version: str
    counted_object: str
    source_queries: tuple[SourceQuery, ...]
    positive_evidence_required: tuple[str, ...]
    counterevidence_required: tuple[str, ...]
    oos_contract: str
    exclusion_rules: tuple[str, ...]
    output_namespace: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "FamilyOnboardingSpec":
        expected_fields = {
            "schema_version",
            "family_id",
            "definition_version",
            "counted_object",
            "source_queries",
            "positive_evidence_required",
            "counterevidence_required",
            "oos_contract",
            "exclusion_rules",
            "output_namespace",
        }
        if not isinstance(value, dict) or set(value) != expected_fields:
            raise ValueError("family onboarding fields must match the versioned schema exactly")
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported family onboarding schema")
        family_id = value.get("family_id")
        if not isinstance(family_id, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", family_id):
            raise ValueError("family_id must be lower snake case")
        if value.get("counted_object") != "mechanism_family/fingerprint":
            raise ValueError("onboarding must explicitly count a mechanism family/fingerprint")
        queries_raw = value.get("source_queries")
        if not isinstance(queries_raw, list) or not queries_raw:
            raise ValueError("at least one source query is required")
        queries: list[SourceQuery] = []
        for query in queries_raw:
            if not isinstance(query, dict) or set(query) != {"source_id", "release", "query", "role"}:
                raise ValueError("source query fields must be exact")
            if any(not isinstance(item, str) or not item for item in query.values()):
                raise ValueError("source query fields must be non-empty strings")
            queries.append(SourceQuery(**query))
        lists: dict[str, tuple[str, ...]] = {}
        for field in (
            "positive_evidence_required",
            "counterevidence_required",
            "exclusion_rules",
        ):
            raw = value.get(field)
            if not isinstance(raw, list) or not raw or any(
                not isinstance(item, str) or not item for item in raw
            ):
                raise ValueError(f"{field} must contain non-empty strings")
            lists[field] = tuple(raw)
        for field in ("definition_version", "oos_contract", "output_namespace"):
            if not isinstance(value.get(field), str) or not value[field]:
                raise ValueError(f"{field} is required")
        if not value["output_namespace"].startswith("proposals/families/"):
            raise ValueError("family onboarding outputs must remain in proposals/families/")
        return cls(
            schema_version=SCHEMA_VERSION,
            family_id=family_id,
            definition_version=value["definition_version"],
            counted_object=value["counted_object"],
            source_queries=tuple(queries),
            positive_evidence_required=lists["positive_evidence_required"],
            counterevidence_required=lists["counterevidence_required"],
            oos_contract=value["oos_contract"],
            exclusion_rules=lists["exclusion_rules"],
            output_namespace=value["output_namespace"],
        )


def load_family_onboarding_spec(path: Path) -> tuple[FamilyOnboardingSpec, str]:
    raw = Path(path).read_bytes()
    return FamilyOnboardingSpec.from_dict(json.loads(raw)), hashlib.sha256(raw).hexdigest()


def build_family_onboarding_plan(
    spec: FamilyOnboardingSpec,
    *,
    spec_sha256: str,
    current_family_ids: set[str],
    expansion_frozen: bool,
    context: ExecutionContext,
) -> dict[str, Any]:
    is_new = spec.family_id not in current_family_ids
    blockers: list[str] = []
    if expansion_frozen and is_new:
        blockers.append("truth_reset_expansion_freeze_blocks_new_family")
    if len({query.source_id for query in spec.source_queries}) < 2:
        blockers.append("fewer_than_two_declared_source_axes")
    return {
        "schema_version": "catalytic-earth.family-onboarding-plan.v1",
        "family_id": spec.family_id,
        "definition_version": spec.definition_version,
        "counted_object": spec.counted_object,
        "created_utc": context.now_utc_iso(),
        "seed": context.seed,
        "spec_sha256": spec_sha256,
        "output_namespace": spec.output_namespace,
        "proposal_only": True,
        "registry_write_authorized": False,
        "is_new_family": is_new,
        "source_query_count": len(spec.source_queries),
        "source_ids": sorted({query.source_id for query in spec.source_queries}),
        "positive_evidence_required": list(spec.positive_evidence_required),
        "counterevidence_required": list(spec.counterevidence_required),
        "oos_contract": spec.oos_contract,
        "exclusion_rules": list(spec.exclusion_rules),
        "status": "blocked" if blockers else "proposal_ready_for_source_review",
        "blockers": blockers,
    }
