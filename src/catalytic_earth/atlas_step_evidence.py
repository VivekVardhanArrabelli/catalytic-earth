"""Evidence-bounded context annotations for exact Atlas source steps.

This module adds reviewed, queryable context around an immutable source-draft
step.  It does not compile atom maps or bond edits, validate an electron-flow
trajectory, or broaden the source draft's permissions or evidence tier.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Sequence

from .atlas_drafts import validate_source_drafts
from .atlas_primary_evidence import validate_primary_evidence


STEP_EVIDENCE_SCHEMA_VERSION = "catalytic-earth.atlas-step-evidence.v1"
STEP_EVIDENCE_STATUS = "reviewed_source_step_context_not_mechanism_expansion"
STEP_EVIDENCE_REVIEWER_KIND = "same_model_computational_agents"
STEP_EVIDENCE_REVIEW_UPDATE_RULE = (
    "Do not automatically refresh this pin after step-context changes. "
    "Repeat source-to-annotation review first."
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_BATCH_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

_TOP_LEVEL_FIELDS = {
    "schema_version",
    "annotation_set_id",
    "batch_id",
    "status",
    "primary_evidence_binding",
    "annotations",
    "review",
}
_ANNOTATION_FIELDS = {
    "annotation_id",
    "record_binding",
    "step_binding",
    "context",
    "primary_annotation_ids",
    "limitations",
    "scope_effect",
}
_CONTEXT_FIELDS = {
    "cofactor_labels",
    "flow_endpoint_source_labels",
    "chemical_context",
    "enzyme_context",
    "source_assertion",
    "direction",
    "roles",
}
_SCOPE_EFFECT_FIELDS = {
    "record_evidence_tier_changed",
    "allowed_operations_changed",
    "whole_proposal_validated",
    "source_step_trajectory_validated",
    "atom_mapping_added",
    "bond_edits_added",
    "linked_primary_annotation_scope_expanded",
}
_REVIEW_FIELDS = {
    "reviewed_on",
    "annotation_payload_sha256",
    "update_rule",
    "reviewer_kind",
    "same_model_agents",
    "blind_review",
    "statistically_independent",
    "correlated_error_risk",
    "human_reviewers",
    "domain_expert_review_claimed",
}
_REQUIRED_LIMITS = {
    "source_step_trajectory",
    "atom_mapping",
    "bond_edits",
    "exact_reaction_instance",
    "whole_proposal_applicability",
}
_CHEMICAL_CONTEXTS = {
    "native",
    "analogue",
    "derivatized_or_trapped",
    "unresolved",
}
_ENZYME_CONTEXTS = {"active_site", "extra_enzymatic", "unresolved"}
_SOURCE_ASSERTIONS = {
    "explicitly_inferred",
    "explicitly_assumed",
    "source_silent",
}
_DIRECTIONS = {
    "source_forward_order",
    "source_reverse_order",
    "bidirectional",
    "unresolved",
}
_WITNESS_FIELDS = {"step_summary", "proposal_mechanism_text"}

_INFER_RE = re.compile(r"\binferred\b|\bwe\s+infer\b", re.IGNORECASE)
_ASSUME_RE = re.compile(r"\bassumed\b|\bwe\s+assume\b", re.IGNORECASE)
_WHOLE_STEP_INFER_RE = re.compile(
    r"\binferred\s+(?:reaction\s+)?step\b|\bstep\b[^.]{0,80}\binferred\b",
    re.IGNORECASE,
)
_EXTRA_ENZYME_RE = re.compile(
    r"\boutside\s+(?:the\s+)?(?:enzyme\s+)?active\s+site\b"
    r"|\breaction\s+occurs\s+outside\s+the\s+enzyme\b"
    r"|\bnot\s+enzyme[- ]catalysed\b",
    re.IGNORECASE,
)
_ACTIVE_SITE_RE = re.compile(
    r"\b(?:inside|within|in)\s+(?:the\s+)?(?:enzyme\s+)?active\s+site\b",
    re.IGNORECASE,
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    return value


def _exact(value: Any, fields: set[str], context: str) -> dict[str, Any]:
    result = _object(value, context)
    actual = set(result)
    _require(
        actual == fields,
        f"{context} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return result


def _string(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{context} must be nonempty text",
    )
    return value


def _sha256(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{context} must be a lowercase SHA-256",
    )
    return value


def _strings(value: Any, context: str) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(
        all(isinstance(item, str) and bool(item.strip()) for item in value),
        f"{context} must contain nonempty strings",
    )
    _require(len(value) == len(set(value)), f"{context} contains duplicates")
    return value


def canonical_step_evidence_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every sidecar field except its manually maintained review block."""

    _require(isinstance(value, dict), "step-evidence sidecar must be an object")
    payload = {key: item for key, item in value.items() if key != "review"}
    raw = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_review(value: Any, payload_sha256: str) -> dict[str, Any]:
    review = _exact(value, _REVIEW_FIELDS, "review")
    _require(
        isinstance(review["reviewed_on"], str)
        and _DATE_RE.fullmatch(review["reviewed_on"]) is not None,
        "review.reviewed_on must be an ISO date",
    )
    _require(
        _sha256(
            review["annotation_payload_sha256"],
            "review.annotation_payload_sha256",
        )
        == payload_sha256,
        "reviewed step-evidence payload changed",
    )
    _require(
        review["update_rule"] == STEP_EVIDENCE_REVIEW_UPDATE_RULE,
        "review must prohibit automatic scientific pin refresh",
    )
    _require(
        review["reviewer_kind"] == STEP_EVIDENCE_REVIEWER_KIND
        and review["same_model_agents"] is True,
        "review must disclose same-model computational agents",
    )
    _require(review["blind_review"] is False, "review was informed, not blind")
    _require(
        review["statistically_independent"] is False,
        "review cannot claim statistical independence",
    )
    _require(
        review["correlated_error_risk"] is True,
        "review must disclose correlated-error risk",
    )
    _require(
        type(review["human_reviewers"]) is int and review["human_reviewers"] == 0,
        "review must disclose zero human reviewers",
    )
    _require(
        review["domain_expert_review_claimed"] is False,
        "review cannot claim domain-expert review",
    )
    return review


def _expected_bundle_id(batch_id: str) -> str:
    bundle_id = "atlas50.source-scoped-mechanism-drafts"
    return bundle_id if batch_id == "default" else f"{bundle_id}.{batch_id}"


def _bound_record(
    value: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    context: str,
) -> tuple[str, dict[str, Any]]:
    binding = _exact(
        value,
        {"record_id", "mcsa_id", "source_snapshot_sha256"},
        context,
    )
    record_id = _string(binding["record_id"], f"{context}.record_id")
    mcsa_id = _string(binding["mcsa_id"], f"{context}.mcsa_id")
    _require(_MCSA_RE.fullmatch(mcsa_id) is not None, f"{context}.mcsa_id is invalid")
    snapshot_sha256 = _sha256(
        binding["source_snapshot_sha256"], f"{context}.source_snapshot_sha256"
    )
    record = record_by_id.get(record_id)
    _require(record is not None, f"{context} targets an unknown source-draft record")
    _require(record["mcsa_id"] == mcsa_id, f"{context} record/M-CSA identity differs")
    _require(
        record["source"]["snapshot_sha256"] == snapshot_sha256,
        f"{context} source snapshot binding is stale",
    )
    return record_id, record


def _bound_step(
    value: Any,
    *,
    record: dict[str, Any],
    context: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    binding = _exact(
        value,
        {
            "proposal_id",
            "source_mechanism_id",
            "step_id",
            "source_step_id",
            "source_scheme_sha256",
        },
        context,
    )
    proposal_id = _string(binding["proposal_id"], f"{context}.proposal_id")
    source_mechanism_id = binding["source_mechanism_id"]
    _require(
        type(source_mechanism_id) is int and source_mechanism_id > 0,
        f"{context}.source_mechanism_id must be a positive integer",
    )
    proposals = [
        proposal
        for proposal in record["mechanism_proposals"]
        if proposal["proposal_id"] == proposal_id
        and proposal["source_mechanism_id"] == source_mechanism_id
    ]
    _require(len(proposals) == 1, f"{context} proposal binding is absent or mixed")
    proposal = proposals[0]
    step_id = _string(binding["step_id"], f"{context}.step_id")
    source_step_id = binding["source_step_id"]
    _require(
        type(source_step_id) is int and source_step_id > 0,
        f"{context}.source_step_id must be a positive integer",
    )
    steps = [
        step
        for step in proposal["mechanism_steps"]
        if step["step_id"] == step_id and step["source_step_id"] == source_step_id
    ]
    _require(len(steps) == 1, f"{context} step binding is absent or mixed")
    step = steps[0]
    scheme_sha256 = _sha256(
        binding["source_scheme_sha256"], f"{context}.source_scheme_sha256"
    )
    _require(
        step["source_scheme_sha256"] == scheme_sha256,
        f"{context} source scheme binding is stale",
    )
    return proposal, step


def _source_text(
    witness: dict[str, Any],
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
) -> str:
    return (
        step["summary"]
        if witness["field"] == "step_summary"
        else proposal["mechanism_text"]
    )


def _validate_witness(
    value: Any,
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
    context: str,
    allowed_fields: set[str] = _WITNESS_FIELDS,
) -> dict[str, Any]:
    witness = _exact(value, {"field", "exact_text"}, context)
    _require(witness["field"] in allowed_fields, f"{context}.field is invalid")
    exact_text = _string(witness["exact_text"], f"{context}.exact_text")
    _require(
        exact_text in _source_text(witness, proposal=proposal, step=step),
        f"{context}.exact_text is absent from its bound source field",
    )
    return witness


def _flow_endpoint_source_labels(step: dict[str, Any]) -> list[str]:
    labels: set[str] = set()
    for flow in step["electron_flows"]:
        for endpoint in (flow["source_point"], flow["target_point"]):
            for atom in endpoint["atoms"]:
                labels.update(atom["semantic_labels"])
    return sorted(labels)


def _contains_exact_label(source_text: str, label: str) -> bool:
    """Return whether a source label occurs without adjoining word characters."""

    pattern = re.compile(rf"(?<!\w){re.escape(label)}(?!\w)")
    return pattern.search(source_text) is not None


def _validate_cofactor_labels(
    value: Any,
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
    context: str,
) -> list[dict[str, Any]]:
    _require(isinstance(value, list), f"{context} must be an array")
    normalized: list[str] = []
    output: list[dict[str, Any]] = []
    for index, raw_item in enumerate(value):
        item_context = f"{context}[{index}]"
        item = _exact(
            raw_item,
            {"label", "support_scope", "source_witness"},
            item_context,
        )
        label = _string(item["label"], f"{item_context}.label")
        _require(
            item["support_scope"] == "source_record_only",
            f"{item_context} cannot be promoted to primary evidence",
        )
        witness = _validate_witness(
            item["source_witness"],
            proposal=proposal,
            step=step,
            context=f"{item_context}.source_witness",
            allowed_fields={"step_summary"},
        )
        _require(
            label.strip().casefold() == witness["exact_text"].strip().casefold(),
            f"{item_context} label must reproduce its exact source text",
        )
        _require(
            _contains_exact_label(step["summary"], witness["exact_text"]),
            f"{item_context} label must be a complete source token",
        )
        canonical = label.strip().casefold()
        _require(canonical not in normalized, f"{context} repeats a label")
        normalized.append(canonical)
        output.append(item)
    _require(normalized == sorted(normalized), f"{context} must be sorted")
    return output


def _validate_qualified_context(
    value: Any,
    *,
    allowed_values: set[str],
    proposal: dict[str, Any],
    step: dict[str, Any],
    context: str,
    kind: str,
) -> dict[str, Any]:
    item = _exact(
        value,
        {"value", "support_scope", "source_witness"},
        context,
    )
    _require(item["value"] in allowed_values, f"{context}.value is invalid")
    if kind == "chemical":
        _require(
            item["value"] == "unresolved",
            f"{context} must remain unresolved until a typed chemical-context "
            "projection is supported",
        )
    if item["value"] == "unresolved":
        _require(
            item["support_scope"] == "abstained" and item["source_witness"] is None,
            f"{context} unresolved status must abstain without a witness",
        )
        return item
    _require(
        item["support_scope"] == "source_record_only",
        f"{context} positive context must remain source-record-only",
    )
    witness = _validate_witness(
        item["source_witness"],
        proposal=proposal,
        step=step,
        context=f"{context}.source_witness",
        allowed_fields={"step_summary"},
    )
    witness_text = witness["exact_text"]
    if item["value"] == "extra_enzymatic":
        _require(
            _EXTRA_ENZYME_RE.search(witness_text) is not None,
            f"{context} lacks an explicit extra-enzymatic witness",
        )
    else:
        _require(
            _ACTIVE_SITE_RE.search(witness_text) is not None
            and _EXTRA_ENZYME_RE.search(witness_text) is None,
            f"{context} lacks an explicit active-site witness",
        )
    return item


def _validate_source_assertion(
    value: Any,
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
    context: str,
) -> dict[str, Any]:
    item = _exact(
        value,
        {
            "status",
            "scope",
            "subject_text",
            "support_scope",
            "source_witness",
        },
        context,
    )
    status = item["status"]
    _require(status in _SOURCE_ASSERTIONS, f"{context}.status is invalid")
    _require(
        item["support_scope"] == "source_record_only",
        f"{context} must remain source-record-only",
    )
    summary = step["summary"]
    has_infer = _INFER_RE.search(summary) is not None
    has_assume = _ASSUME_RE.search(summary) is not None
    _require(not (has_infer and has_assume), f"{context} source qualifiers are ambiguous")
    if status == "source_silent":
        _require(
            not has_infer and not has_assume,
            f"{context} cannot call an explicit source qualifier silent",
        )
        _require(
            item["scope"] == "not_established"
            and item["subject_text"] is None
            and item["source_witness"] is None,
            f"{context} source-silent status must not claim a scope or witness",
        )
        return item

    expected_pattern = _INFER_RE if status == "explicitly_inferred" else _ASSUME_RE
    _require(
        has_infer if status == "explicitly_inferred" else has_assume,
        f"{context} qualifier differs from the source step",
    )
    witness = _validate_witness(
        item["source_witness"],
        proposal=proposal,
        step=step,
        context=f"{context}.source_witness",
        allowed_fields={"step_summary"},
    )
    _require(
        expected_pattern.search(witness["exact_text"]) is not None,
        f"{context} witness omits its source qualifier",
    )
    _require(
        item["scope"] in {"whole_step", "stated_detail_only"},
        f"{context}.scope is invalid for an explicit qualifier",
    )
    if item["scope"] == "whole_step":
        _require(
            status == "explicitly_inferred"
            and item["subject_text"] is None
            and _WHOLE_STEP_INFER_RE.search(witness["exact_text"]) is not None,
            f"{context} lacks an explicit whole-step inference witness",
        )
    else:
        subject_text = _string(item["subject_text"], f"{context}.subject_text")
        _require(
            subject_text in summary,
            f"{context}.subject_text is absent from the source step",
        )
    return item


def _validate_direction(
    value: Any,
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
    context: str,
) -> dict[str, Any]:
    item = _exact(
        value,
        {"value", "scope", "support_scope", "source_witness"},
        context,
    )
    _require(item["value"] in _DIRECTIONS, f"{context}.value is invalid")
    if item["value"] == "unresolved":
        _require(
            item["scope"] == "not_established"
            and item["support_scope"] == "abstained"
            and item["source_witness"] is None,
            f"{context} unresolved direction must abstain",
        )
        return item
    _require(
        item["support_scope"] == "source_record_only",
        f"{context} direction must remain source-record-only",
    )
    witness = _validate_witness(
        item["source_witness"],
        proposal=proposal,
        step=step,
        context=f"{context}.source_witness",
    )
    expected_scope = (
        "step_text" if witness["field"] == "step_summary" else "proposal_context"
    )
    _require(item["scope"] == expected_scope, f"{context}.scope differs from its witness")
    _require(
        re.search(r"\bdirection\b", witness["exact_text"], re.IGNORECASE) is not None,
        f"{context} direction is not explicit in its source witness",
    )
    return item


def _validate_roles(
    value: Any,
    *,
    proposal: dict[str, Any],
    step: dict[str, Any],
    direction_value: str,
    context: str,
) -> list[dict[str, Any]]:
    _require(isinstance(value, list), f"{context} must be an array")
    keys: list[tuple[str, str, str]] = []
    output: list[dict[str, Any]] = []
    for index, raw_item in enumerate(value):
        item_context = f"{context}[{index}]"
        item = _exact(
            raw_item,
            {
                "actor_label",
                "actor_mapping_status",
                "role_text",
                "direction",
                "support_scope",
                "source_witness",
            },
            item_context,
        )
        actor = _string(item["actor_label"], f"{item_context}.actor_label")
        role = _string(item["role_text"], f"{item_context}.role_text")
        _require(
            item["actor_mapping_status"] == "source_label_only",
            f"{item_context} cannot infer a protein or sequence mapping",
        )
        _require(item["direction"] in _DIRECTIONS, f"{item_context}.direction is invalid")
        _require(
            item["support_scope"] == "source_record_only",
            f"{item_context} role must remain source-record-only",
        )
        witness = _validate_witness(
            item["source_witness"],
            proposal=proposal,
            step=step,
            context=f"{item_context}.source_witness",
            allowed_fields={"step_summary"},
        )
        _require(
            actor in witness["exact_text"] and role in witness["exact_text"],
            f"{item_context} actor and role must be verbatim source text",
        )
        _require(
            item["direction"] == "unresolved"
            or item["direction"] == direction_value,
            f"{item_context}.direction differs from the step context",
        )
        key = (actor.casefold(), role.casefold(), item["direction"])
        _require(key not in keys, f"{context} repeats a role assertion")
        keys.append(key)
        output.append(item)
    _require(keys == sorted(keys), f"{context} must be sorted")
    return output


def _validate_limits_and_scope(annotation: dict[str, Any], context: str) -> None:
    limitations = annotation["limitations"]
    _require(
        isinstance(limitations, list) and limitations,
        f"{context}.limitations must be nonempty",
    )
    observed_ids: list[str] = []
    for index, raw_limit in enumerate(limitations):
        limit_context = f"{context}.limitations[{index}]"
        item = _exact(raw_limit, {"limit_id", "status", "statement"}, limit_context)
        limit_id = _string(item["limit_id"], f"{limit_context}.limit_id")
        _require(item["status"] == "abstained", f"{limit_context} must abstain")
        _string(item["statement"], f"{limit_context}.statement")
        _require(limit_id not in observed_ids, f"{context} repeats a limitation")
        observed_ids.append(limit_id)
    _require(observed_ids == sorted(observed_ids), f"{context}.limitations must be sorted")
    _require(
        _REQUIRED_LIMITS <= set(observed_ids),
        f"{context}.limitations omit required scope boundaries",
    )
    scope_effect = _exact(
        annotation["scope_effect"], _SCOPE_EFFECT_FIELDS, f"{context}.scope_effect"
    )
    _require(
        all(scope_effect[field] is False for field in _SCOPE_EFFECT_FIELDS),
        f"{context} attempts to expand source or primary evidence scope",
    )


def _primary_annotation_index(
    binding_value: Any,
    *,
    primary_evidence: dict[str, Any] | None,
    bundle: dict[str, Any],
    repo_root: str | Path | None,
) -> dict[str, dict[str, Any]]:
    if binding_value is None:
        _require(primary_evidence is None, "unbound primary-evidence input was supplied")
        return {}
    binding = _exact(
        binding_value,
        {"annotation_set_id", "annotation_payload_sha256"},
        "primary_evidence_binding",
    )
    _require(primary_evidence is not None, "bound primary evidence is missing")
    summary = validate_primary_evidence(
        primary_evidence, bundle=bundle, repo_root=repo_root
    )
    _require(
        binding["annotation_set_id"] == summary["annotation_set_id"],
        "primary annotation-set binding differs",
    )
    _require(
        _sha256(
            binding["annotation_payload_sha256"],
            "primary_evidence_binding.annotation_payload_sha256",
        )
        == summary["annotation_payload_sha256"],
        "primary annotation payload binding is stale",
    )
    index: dict[str, dict[str, Any]] = {}
    for annotation in primary_evidence["annotations"]:
        annotation_id = annotation["annotation_id"]
        _require(annotation_id not in index, "primary annotation IDs repeat")
        index[annotation_id] = annotation
    return index


def _validate_primary_links(
    value: Any,
    *,
    primary_by_id: dict[str, dict[str, Any]],
    record_id: str,
    proposal: dict[str, Any],
    context: str,
) -> None:
    annotation_ids = _strings(value, context)
    _require(annotation_ids == sorted(annotation_ids), f"{context} must be sorted")
    _require(
        bool(primary_by_id) or not annotation_ids,
        f"{context} requires a bound primary-evidence sidecar",
    )
    for annotation_id in annotation_ids:
        primary = primary_by_id.get(annotation_id)
        _require(primary is not None, f"{context} cites an unknown primary annotation")
        _require(
            primary["record_binding"]["record_id"] == record_id,
            f"{context} crosses source-draft records",
        )
        primary_proposal = primary.get("proposal_binding")
        if primary_proposal is not None:
            _require(
                primary_proposal["proposal_id"] == proposal["proposal_id"]
                and primary_proposal["source_mechanism_id"]
                == proposal["source_mechanism_id"],
                f"{context} crosses source mechanism proposals",
            )


def _validate_annotation(
    raw_annotation: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    primary_by_id: dict[str, dict[str, Any]],
    context: str,
) -> tuple[str, str, tuple[int, int]]:
    annotation = _exact(raw_annotation, _ANNOTATION_FIELDS, context)
    annotation_id = _string(annotation["annotation_id"], f"{context}.annotation_id")
    record_id, record = _bound_record(
        annotation["record_binding"], record_by_id=record_by_id, context=f"{context}.record_binding"
    )
    proposal, step = _bound_step(
        annotation["step_binding"], record=record, context=f"{context}.step_binding"
    )
    _validate_primary_links(
        annotation["primary_annotation_ids"],
        primary_by_id=primary_by_id,
        record_id=record_id,
        proposal=proposal,
        context=f"{context}.primary_annotation_ids",
    )
    step_context = _exact(annotation["context"], _CONTEXT_FIELDS, f"{context}.context")
    _validate_cofactor_labels(
        step_context["cofactor_labels"],
        proposal=proposal,
        step=step,
        context=f"{context}.context.cofactor_labels",
    )
    endpoint_labels = _strings(
        step_context["flow_endpoint_source_labels"],
        f"{context}.context.flow_endpoint_source_labels",
    )
    _require(
        endpoint_labels == _flow_endpoint_source_labels(step),
        f"{context}.context.flow_endpoint_source_labels differ from the compiled step",
    )
    _validate_qualified_context(
        step_context["chemical_context"],
        allowed_values=_CHEMICAL_CONTEXTS,
        proposal=proposal,
        step=step,
        context=f"{context}.context.chemical_context",
        kind="chemical",
    )
    _validate_qualified_context(
        step_context["enzyme_context"],
        allowed_values=_ENZYME_CONTEXTS,
        proposal=proposal,
        step=step,
        context=f"{context}.context.enzyme_context",
        kind="enzyme",
    )
    _validate_source_assertion(
        step_context["source_assertion"],
        proposal=proposal,
        step=step,
        context=f"{context}.context.source_assertion",
    )
    _validate_direction(
        step_context["direction"],
        proposal=proposal,
        step=step,
        context=f"{context}.context.direction",
    )
    _validate_roles(
        step_context["roles"],
        proposal=proposal,
        step=step,
        direction_value=step_context["direction"]["value"],
        context=f"{context}.context.roles",
    )
    _validate_limits_and_scope(annotation, context)
    return (
        annotation_id,
        record_id,
        (proposal["source_mechanism_id"], step["source_step_id"]),
    )


def validate_step_evidence(
    value: Any,
    *,
    bundle: dict[str, Any],
    primary_evidence: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate reviewed step context against one exact source-draft bundle."""

    validate_source_drafts(bundle)
    sidecar = _exact(value, _TOP_LEVEL_FIELDS, "step-evidence sidecar")
    _require(
        sidecar["schema_version"] == STEP_EVIDENCE_SCHEMA_VERSION,
        "unsupported step-evidence schema",
    )
    annotation_set_id = _string(sidecar["annotation_set_id"], "annotation_set_id")
    batch_id = _string(sidecar["batch_id"], "batch_id")
    _require(_BATCH_RE.fullmatch(batch_id) is not None, "batch_id is invalid")
    _require(
        bundle.get("bundle_id") == _expected_bundle_id(batch_id),
        "step-evidence batch/bundle differs",
    )
    _require(sidecar["status"] == STEP_EVIDENCE_STATUS, "sidecar status overclaims")
    primary_by_id = _primary_annotation_index(
        sidecar["primary_evidence_binding"],
        primary_evidence=primary_evidence,
        bundle=bundle,
        repo_root=repo_root,
    )
    payload_sha256 = canonical_step_evidence_payload_sha256(sidecar)
    review = _validate_review(sidecar["review"], payload_sha256)

    records = bundle["records"]
    record_by_id = {record["record_id"]: record for record in records}
    annotations = sidecar["annotations"]
    _require(isinstance(annotations, list) and annotations, "annotations must be nonempty")
    annotation_ids: set[str] = set()
    observed_order: list[tuple[str, int, int, str]] = []
    observed_steps: set[tuple[str, int, int]] = set()
    annotated_record_ids: set[str] = set()
    for index, raw_annotation in enumerate(annotations):
        annotation_id, record_id, step_key = _validate_annotation(
            raw_annotation,
            record_by_id=record_by_id,
            primary_by_id=primary_by_id,
            context=f"annotations[{index}]",
        )
        _require(annotation_id not in annotation_ids, "annotation IDs repeat")
        annotation_ids.add(annotation_id)
        source_mechanism_id, source_step_id = step_key
        record_step_key = (record_id, source_mechanism_id, source_step_id)
        _require(record_step_key not in observed_steps, "source steps are annotated twice")
        observed_steps.add(record_step_key)
        observed_order.append(
            (record_id, source_mechanism_id, source_step_id, annotation_id)
        )
        annotated_record_ids.add(record_id)
    _require(
        observed_order == sorted(observed_order),
        "annotations must follow record, mechanism, source-step, annotation order",
    )
    record_order = [
        record["record_id"]
        for record in records
        if record["record_id"] in annotated_record_ids
    ]
    return {
        "schema_version": sidecar["schema_version"],
        "annotation_set_id": annotation_set_id,
        "annotation_payload_sha256": payload_sha256,
        "annotation_count": len(annotations),
        "record_count": len(annotated_record_ids),
        "record_ids": record_order,
        "reviewed_on": review["reviewed_on"],
    }


def _filter_values(
    value: Sequence[str],
    *,
    context: str,
    allowed: set[str] | None = None,
) -> list[str]:
    _require(
        isinstance(value, (list, tuple)),
        f"{context} must be a list or tuple of strings",
    )
    normalized: list[str] = []
    for index, item in enumerate(value):
        text = _string(item, f"{context}[{index}]").strip().casefold()
        _require("," not in text, f"{context}[{index}] must contain one value")
        if allowed is not None:
            _require(text in allowed, f"{context}[{index}] is invalid")
        if text not in normalized:
            normalized.append(text)
    return sorted(normalized)


def normalize_step_filters(
    *,
    cofactors: Sequence[str] = (),
    enzyme_contexts: Sequence[str] = (),
    source_assertions: Sequence[str] = (),
) -> dict[str, list[str]]:
    """Normalize exact filters for callers that may not have a sidecar."""

    return {
        "cofactors": _filter_values(cofactors, context="cofactors"),
        "enzyme_contexts": _filter_values(
            enzyme_contexts, context="enzyme_contexts", allowed=_ENZYME_CONTEXTS
        ),
        "source_assertions": _filter_values(
            source_assertions, context="source_assertions", allowed=_SOURCE_ASSERTIONS
        ),
    }


def match_step_evidence(
    value: dict[str, Any],
    *,
    bundle: dict[str, Any],
    primary_evidence: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    cofactors: Sequence[str] = (),
    enzyme_contexts: Sequence[str] = (),
    source_assertions: Sequence[str] = (),
) -> dict[str, Any]:
    """Return exact source-step witnesses satisfying all clauses in one row."""

    validate_step_evidence(
        value,
        bundle=bundle,
        primary_evidence=primary_evidence,
        repo_root=repo_root,
    )
    filters = normalize_step_filters(
        cofactors=cofactors,
        enzyme_contexts=enzyme_contexts,
        source_assertions=source_assertions,
    )
    matches: dict[str, list[dict[str, Any]]] = {}
    for annotation in value["annotations"]:
        context = annotation["context"]
        labels = {
            item["label"].strip().casefold() for item in context["cofactor_labels"]
        }
        if not set(filters["cofactors"]) <= labels:
            continue
        if not all(
            requested == context["enzyme_context"]["value"]
            for requested in filters["enzyme_contexts"]
        ):
            continue
        if not all(
            requested == context["source_assertion"]["status"]
            for requested in filters["source_assertions"]
        ):
            continue
        record_id = annotation["record_binding"]["record_id"]
        matches.setdefault(record_id, []).append(copy.deepcopy(annotation))
    return {
        "filters": filters,
        "matches": matches,
        "query_semantics": {
            "filter_combination": "all_clauses_within_one_annotation_and_source_step",
            "cofactor_matching": "exact_same_step_source_text_label_trim_and_casefold_only",
            "flow_endpoint_labels_imply_cofactor_or_state_identity": False,
            "source_silent_implies_observed_or_not_inferred": False,
            "linked_primary_annotation_expands_step_scope": False,
            "atom_mapping_or_bond_edits_compiled": False,
        },
    }
