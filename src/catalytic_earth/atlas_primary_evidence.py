"""Validated record-level primary-evidence annotations for Atlas drafts.

Annotations are an additive query sidecar.  They cannot change a source draft's
evidence tier, permissions, mechanism scope, proposals, or source steps.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .atlas_drafts import validate_source_drafts
from .canonical_hash import canonical_file_sha256


PRIMARY_EVIDENCE_SCHEMA_VERSION = "catalytic-earth.atlas-primary-evidence.v1"
PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE = (
    "Do not automatically refresh this pin after annotation changes. "
    "Repeat source-to-claim primary-evidence review first."
)
PRIMARY_EVIDENCE_STATUS = (
    "reviewed_primary_evidence_annotations_not_mechanism_expansion"
)
PRIMARY_EVIDENCE_REVIEWER_KIND = "same_model_computational_agents"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_PDB_RE = re.compile(r"^[0-9][A-Z0-9]{3}$")
_UNIPROT_RE = re.compile(r"^[A-Z0-9]{6,10}$")
_BATCH_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

_TOP_LEVEL_FIELDS = {
    "schema_version",
    "annotation_set_id",
    "batch_id",
    "status",
    "source_bindings",
    "annotations",
    "review",
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
_ANNOTATION_FIELDS = {
    "annotation_id",
    "record_binding",
    "annotation_kind",
    "target_scope",
    "claim",
    "evidence",
    "limits",
    "scope_effect",
}
_SCOPE_EFFECT_FIELDS = {
    "record_evidence_tier_changed",
    "allowed_operations_changed",
    "mechanism_scope_expanded",
    "source_step_trajectory_claimed",
    "proposal_applicability_claimed",
}


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
    _require(isinstance(value, str) and bool(value), f"{context} must be nonempty text")
    return value


def _strings(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(len(value) >= minimum, f"{context} is incomplete")
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{context} must contain nonempty strings",
    )
    _require(len(value) == len(set(value)), f"{context} contains duplicates")
    return value


def _sha256(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{context} must be a lowercase SHA-256",
    )
    return value


def canonical_annotation_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every sidecar field except the manually maintained review block."""

    _require(isinstance(value, dict), "primary-evidence sidecar must be an object")
    payload = {key: item for key, item in value.items() if key != "review"}
    raw = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_source_bindings(
    value: Any, *, repo_root: str | Path | None
) -> set[str]:
    _require(isinstance(value, list) and value, "source_bindings must be nonempty")
    paths: list[str] = []
    digests: set[str] = set()
    root = Path(repo_root).resolve() if repo_root is not None else None
    for index, raw_binding in enumerate(value):
        context = f"source_bindings[{index}]"
        binding = _exact(raw_binding, {"path", "sha256"}, context)
        relative_text = _string(binding["path"], f"{context}.path")
        windows_path = PureWindowsPath(relative_text)
        relative = PurePosixPath(relative_text)
        _require(
            "\\" not in relative_text
            and not relative.is_absolute()
            and not windows_path.is_absolute()
            and not windows_path.drive
            and relative_text == relative.as_posix()
            and "." not in relative.parts
            and ".." not in relative.parts,
            f"{context}.path must be repository-relative",
        )
        digest = _sha256(binding["sha256"], f"{context}.sha256")
        paths.append(relative.as_posix())
        _require(digest not in digests, f"{context} repeats a source digest")
        digests.add(digest)
        if root is not None:
            path = (root / Path(relative)).resolve()
            _require(root in path.parents and path.is_file(), f"{context} is missing")
            _require(
                canonical_file_sha256(path) == digest,
                f"{context} source hash differs",
            )
    _require(paths == sorted(set(paths)), "source_bindings must be unique and sorted")
    return digests


def _validate_review(review_value: Any, payload_sha256: str) -> dict[str, Any]:
    review = _exact(review_value, _REVIEW_FIELDS, "review")
    _require(
        isinstance(review["reviewed_on"], str)
        and _DATE_RE.fullmatch(review["reviewed_on"]) is not None,
        "review.reviewed_on must be an ISO date",
    )
    _require(
        _sha256(review["annotation_payload_sha256"], "review.annotation_payload_sha256")
        == payload_sha256,
        "reviewed annotation payload changed",
    )
    _require(
        review["update_rule"] == PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE,
        "review must prohibit automatic scientific pin refresh",
    )
    _require(
        review["reviewer_kind"] == PRIMARY_EVIDENCE_REVIEWER_KIND
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
        "review cannot claim human review",
    )
    _require(
        review["domain_expert_review_claimed"] is False,
        "review cannot claim domain-expert review",
    )
    return review


def _validate_annotation(
    raw_annotation: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    source_binding_digests: set[str],
    context: str,
) -> tuple[str, str]:
    annotation = _exact(raw_annotation, _ANNOTATION_FIELDS, context)
    annotation_id = _string(annotation["annotation_id"], f"{context}.annotation_id")
    _require(
        annotation["annotation_kind"] == "primary_structure_observation",
        f"{context}.annotation_kind is unsupported",
    )
    _require(
        annotation["target_scope"] == "record_only",
        f"{context} cannot target a proposal or source step",
    )

    binding = _exact(
        annotation["record_binding"],
        {"record_id", "mcsa_id", "source_snapshot_sha256"},
        f"{context}.record_binding",
    )
    record_id = _string(binding["record_id"], f"{context}.record_binding.record_id")
    mcsa_id = _string(binding["mcsa_id"], f"{context}.record_binding.mcsa_id")
    _require(_MCSA_RE.fullmatch(mcsa_id) is not None, f"{context} has invalid M-CSA ID")
    _sha256(
        binding["source_snapshot_sha256"],
        f"{context}.record_binding.source_snapshot_sha256",
    )
    record = record_by_id.get(record_id)
    _require(record is not None, f"{context} targets an unknown draft record")
    _require(record["mcsa_id"] == mcsa_id, f"{context} record/M-CSA identity differs")
    _require(
        record["source"]["snapshot_sha256"] == binding["source_snapshot_sha256"],
        f"{context} source snapshot binding is stale",
    )

    evidence = annotation["evidence"]
    _require(isinstance(evidence, list) and evidence, f"{context}.evidence is incomplete")
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for evidence_index, raw_evidence in enumerate(evidence):
        evidence_context = f"{context}.evidence[{evidence_index}]"
        item = _exact(
            raw_evidence,
            {
                "evidence_id",
                "evidence_role",
                "source_kind",
                "source_id",
                "uri",
                "citation",
                "experimental_context",
                "source_sha256",
            },
            evidence_context,
        )
        evidence_id = _string(item["evidence_id"], f"{evidence_context}.evidence_id")
        _require(evidence_id not in evidence_by_id, f"{context} repeats evidence_id")
        _require(
            item["evidence_role"] in {"direct_support", "corroboration_only"},
            f"{evidence_context}.evidence_role is invalid",
        )
        _require(
            item["source_kind"]
            in {"primary_structure_record", "primary_research_article"},
            f"{evidence_context}.source_kind is invalid",
        )
        _string(item["source_id"], f"{evidence_context}.source_id")
        uri = _string(item["uri"], f"{evidence_context}.uri")
        _require(uri.startswith("https://"), f"{evidence_context}.uri must use HTTPS")
        _string(item["citation"], f"{evidence_context}.citation")
        _string(
            item["experimental_context"],
            f"{evidence_context}.experimental_context",
        )
        source_sha = item["source_sha256"]
        if source_sha is not None:
            _sha256(source_sha, f"{evidence_context}.source_sha256")
            _require(
                source_sha in source_binding_digests,
                f"{evidence_context} cites an unbound source digest",
            )
        _require(
            item["evidence_role"] != "direct_support" or source_sha is not None,
            f"{evidence_context} direct support requires a bound source digest",
        )
        evidence_by_id[evidence_id] = item

    claim = _exact(
        annotation["claim"],
        {
            "statement",
            "observed_state",
            "structure_site",
            "sequence_mapping",
            "direct_evidence_ids",
            "corroborating_evidence_ids",
        },
        f"{context}.claim",
    )
    _string(claim["statement"], f"{context}.claim.statement")
    observed_state = _exact(
        claim["observed_state"],
        {"description", "identity_scope", "normalized_chebi_id"},
        f"{context}.claim.observed_state",
    )
    _string(observed_state["description"], f"{context}.claim.observed_state.description")
    _require(
        observed_state["identity_scope"]
        == "structure_bound_adduct_source_description",
        f"{context} observed state exceeds the structure-source description",
    )
    _require(
        observed_state["normalized_chebi_id"] is None,
        f"{context} cannot treat the bound adduct as a free ChEBI participant",
    )
    site = _exact(
        claim["structure_site"],
        {"pdb_id", "chain_id", "author_residue_name", "author_residue_number"},
        f"{context}.claim.structure_site",
    )
    _require(
        isinstance(site["pdb_id"], str) and _PDB_RE.fullmatch(site["pdb_id"]),
        f"{context} structure PDB ID is invalid",
    )
    _string(site["chain_id"], f"{context}.claim.structure_site.chain_id")
    _string(
        site["author_residue_name"],
        f"{context}.claim.structure_site.author_residue_name",
    )
    _require(
        type(site["author_residue_number"]) is int
        and site["author_residue_number"] > 0,
        f"{context} author residue number is invalid",
    )

    direct_ids = _strings(
        claim["direct_evidence_ids"], f"{context}.claim.direct_evidence_ids", minimum=1
    )
    corroborating_ids = _strings(
        claim["corroborating_evidence_ids"],
        f"{context}.claim.corroborating_evidence_ids",
    )
    _require(
        not (set(direct_ids) & set(corroborating_ids)),
        f"{context} evidence cannot be direct and corroborating",
    )
    expected_direct = {
        evidence_id
        for evidence_id, item in evidence_by_id.items()
        if item["evidence_role"] == "direct_support"
    }
    expected_corroborating = set(evidence_by_id) - expected_direct
    _require(set(direct_ids) == expected_direct, f"{context} direct evidence differs")
    _require(
        set(corroborating_ids) == expected_corroborating,
        f"{context} corroborating evidence differs",
    )

    mapping = _exact(
        claim["sequence_mapping"],
        {"status", "uniprot_id", "sequence_position", "evidence_ids"},
        f"{context}.claim.sequence_mapping",
    )
    mapping_evidence = _strings(
        mapping["evidence_ids"], f"{context}.claim.sequence_mapping.evidence_ids"
    )
    _require(
        set(mapping_evidence) <= set(evidence_by_id),
        f"{context} sequence mapping cites unknown evidence",
    )
    if mapping["status"] == "source_supported":
        _require(
            isinstance(mapping["uniprot_id"], str)
            and _UNIPROT_RE.fullmatch(mapping["uniprot_id"]) is not None,
            f"{context} supported sequence mapping lacks a UniProt ID",
        )
        _require(
            type(mapping["sequence_position"]) is int
            and mapping["sequence_position"] > 0,
            f"{context} supported sequence mapping lacks a position",
        )
        _require(mapping_evidence, f"{context} supported sequence mapping lacks evidence")
        _require(
            set(mapping_evidence) <= expected_direct,
            f"{context} supported sequence mapping requires direct evidence",
        )
    else:
        _require(
            mapping["status"] in {"under_review", "not_asserted"},
            f"{context} sequence mapping status is invalid",
        )
        _require(
            mapping["uniprot_id"] is None
            and mapping["sequence_position"] is None
            and not mapping_evidence,
            f"{context} unresolved sequence mapping contains a mapping claim",
        )

    limits = annotation["limits"]
    _require(isinstance(limits, list) and limits, f"{context}.limits must be nonempty")
    limit_ids: set[str] = set()
    for limit_index, raw_limit in enumerate(limits):
        limit_context = f"{context}.limits[{limit_index}]"
        limit = _exact(raw_limit, {"limit_id", "status", "statement"}, limit_context)
        limit_id = _string(limit["limit_id"], f"{limit_context}.limit_id")
        _require(limit_id not in limit_ids, f"{context} repeats limit_id")
        limit_ids.add(limit_id)
        _require(
            limit["status"] in {"abstained", "under_review"},
            f"{limit_context}.status is invalid",
        )
        _string(limit["statement"], f"{limit_context}.statement")

    scope_effect = _exact(
        annotation["scope_effect"], _SCOPE_EFFECT_FIELDS, f"{context}.scope_effect"
    )
    _require(
        all(scope_effect[field] is False for field in _SCOPE_EFFECT_FIELDS),
        f"{context} attempts to expand the source record",
    )
    return annotation_id, record_id


def validate_primary_evidence(
    value: Any,
    *,
    bundle: dict[str, Any],
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate an annotation sidecar against one exact source-draft bundle."""

    validate_source_drafts(bundle)
    sidecar = _exact(value, _TOP_LEVEL_FIELDS, "primary-evidence sidecar")
    _require(
        sidecar["schema_version"] == PRIMARY_EVIDENCE_SCHEMA_VERSION,
        "unsupported primary-evidence schema",
    )
    annotation_set_id = _string(sidecar["annotation_set_id"], "annotation_set_id")
    batch_id = _string(sidecar["batch_id"], "batch_id")
    _require(_BATCH_RE.fullmatch(batch_id) is not None, "batch_id is invalid")
    expected_bundle_id = "atlas50.source-scoped-mechanism-drafts"
    if batch_id != "default":
        expected_bundle_id += f".{batch_id}"
    _require(bundle.get("bundle_id") == expected_bundle_id, "sidecar batch/bundle differs")
    _require(sidecar["status"] == PRIMARY_EVIDENCE_STATUS, "sidecar status overclaims")

    source_digests = _validate_source_bindings(
        sidecar["source_bindings"], repo_root=repo_root
    )
    payload_sha256 = canonical_annotation_payload_sha256(sidecar)
    review = _validate_review(sidecar["review"], payload_sha256)

    records = bundle["records"]
    record_by_id = {record["record_id"]: record for record in records}
    annotations = sidecar["annotations"]
    _require(isinstance(annotations, list) and annotations, "annotations must be nonempty")
    observed_keys: list[tuple[str, str]] = []
    annotation_ids: set[str] = set()
    annotated_record_ids: set[str] = set()
    for index, raw_annotation in enumerate(annotations):
        annotation_id, record_id = _validate_annotation(
            raw_annotation,
            record_by_id=record_by_id,
            source_binding_digests=source_digests,
            context=f"annotations[{index}]",
        )
        _require(annotation_id not in annotation_ids, "annotation IDs repeat")
        annotation_ids.add(annotation_id)
        annotated_record_ids.add(record_id)
        observed_keys.append((record_id, annotation_id))
    _require(
        observed_keys == sorted(observed_keys),
        "annotations must be deterministically ordered by record and annotation ID",
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
