"""Validated record-level primary-evidence annotations for Atlas drafts.

Annotations are an additive query sidecar.  They cannot change a source draft's
evidence tier, permissions, mechanism scope, proposals, or source steps.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .atlas_drafts import validate_source_drafts
from .canonical_hash import canonical_file_sha256


PRIMARY_EVIDENCE_SCHEMA_V1 = "catalytic-earth.atlas-primary-evidence.v1"
PRIMARY_EVIDENCE_SCHEMA_VERSION = "catalytic-earth.atlas-primary-evidence.v2"
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
_PROPOSAL_CONTEXT_ANNOTATION_FIELDS = _ANNOTATION_FIELDS | {
    "proposal_binding",
    "projection_binding",
}
_SCOPE_EFFECT_FIELDS = {
    "record_evidence_tier_changed",
    "allowed_operations_changed",
    "mechanism_scope_expanded",
    "source_step_trajectory_claimed",
    "proposal_applicability_claimed",
}
_PROTEIN_SUPPORT_SCOPE = {
    "protein_identity": "primary_structure_supported",
    "chain_mapping": "primary_structure_supported",
    "site_mapping": "primary_structure_supported",
    "residue_roles": "computational_only",
    "protonation_states": "computational_only",
    "full_mechanism": "not_validated",
}
_PROPOSAL_CONTEXT_LIMITS = {
    "catalytic_role_validation": "abstained",
    "protonation_state_validation": "abstained",
    "full_mechanism_validation": "abstained",
    "exact_reaction_instance": "abstained",
}
_PROJECTION_SCHEMA_VERSION = (
    "catalytic-earth.primary-protein-context-projection.v1"
)


@dataclass(frozen=True)
class _SourceBindings:
    by_id: dict[str, dict[str, Any]]
    by_digest: dict[str, dict[str, Any]]
    resolved_paths: dict[str, Path]


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
    value: Any,
    *,
    schema_version: str,
    repo_root: str | Path | None,
) -> _SourceBindings:
    _require(isinstance(value, list) and value, "source_bindings must be nonempty")
    paths: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    by_digest: dict[str, dict[str, Any]] = {}
    resolved_paths: dict[str, Path] = {}
    root = Path(repo_root).resolve() if repo_root is not None else None
    for index, raw_binding in enumerate(value):
        context = f"source_bindings[{index}]"
        fields = {"path", "sha256"}
        if schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION:
            fields |= {"binding_id", "artifact_kind"}
        binding = _exact(raw_binding, fields, context)
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
        _require(digest not in by_digest, f"{context} repeats a source digest")
        if schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION:
            binding_id = _string(binding["binding_id"], f"{context}.binding_id")
            _require(binding_id not in by_id, f"{context} repeats binding_id")
            _require(
                binding["artifact_kind"]
                in {
                    "primary_source",
                    "project_projection",
                    "source_inventory",
                    "attribution",
                },
                f"{context}.artifact_kind is invalid",
            )
        else:
            binding_id = relative.as_posix()
        by_id[binding_id] = binding
        by_digest[digest] = binding
        if root is not None:
            path = (root / Path(relative)).resolve()
            _require(root in path.parents and path.is_file(), f"{context} is missing")
            _require(
                canonical_file_sha256(path) == digest,
                f"{context} source hash differs",
            )
            resolved_paths[binding_id] = path
    _require(paths == sorted(set(paths)), "source_bindings must be unique and sorted")
    return _SourceBindings(
        by_id=by_id,
        by_digest=by_digest,
        resolved_paths=resolved_paths,
    )


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


def _bound_record(
    binding_value: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    context: str,
) -> tuple[str, dict[str, Any]]:
    binding = _exact(
        binding_value,
        {"record_id", "mcsa_id", "source_snapshot_sha256"},
        context,
    )
    record_id = _string(binding["record_id"], f"{context}.record_id")
    mcsa_id = _string(binding["mcsa_id"], f"{context}.mcsa_id")
    _require(_MCSA_RE.fullmatch(mcsa_id) is not None, f"{context} has invalid M-CSA ID")
    _sha256(binding["source_snapshot_sha256"], f"{context}.source_snapshot_sha256")
    record = record_by_id.get(record_id)
    _require(record is not None, f"{context} targets an unknown draft record")
    _require(record["mcsa_id"] == mcsa_id, f"{context} record/M-CSA identity differs")
    _require(
        record["source"]["snapshot_sha256"] == binding["source_snapshot_sha256"],
        f"{context} source snapshot binding is stale",
    )
    return record_id, record


def _validate_limits_and_scope(
    annotation: dict[str, Any],
    context: str,
    *,
    required_limits: dict[str, str] | None = None,
) -> None:
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
    if required_limits is not None:
        actual = {limit["limit_id"]: limit["status"] for limit in limits}
        _require(
            all(actual.get(limit_id) == status for limit_id, status in required_limits.items()),
            f"{context}.limits omit a required proposal-context boundary",
        )

    scope_effect = _exact(
        annotation["scope_effect"], _SCOPE_EFFECT_FIELDS, f"{context}.scope_effect"
    )
    _require(
        all(scope_effect[field] is False for field in _SCOPE_EFFECT_FIELDS),
        f"{context} attempts to expand the source record",
    )


def _validate_structure_annotation(
    raw_annotation: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    source_bindings: _SourceBindings,
    schema_version: str,
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

    record_id, _ = _bound_record(
        annotation["record_binding"],
        record_by_id=record_by_id,
        context=f"{context}.record_binding",
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
                source_sha in source_bindings.by_digest,
                f"{evidence_context} cites an unbound source digest",
            )
            if (
                schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION
                and item["evidence_role"] == "direct_support"
            ):
                _require(
                    source_bindings.by_digest[source_sha]["artifact_kind"]
                    == "primary_source",
                    f"{evidence_context} direct support must bind a primary source",
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

    _validate_limits_and_scope(annotation, context)
    return annotation_id, record_id


def _site_mappings(value: Any, context: str) -> list[dict[str, Any]]:
    _require(isinstance(value, list) and value, f"{context} must be nonempty")
    sites: list[dict[str, Any]] = []
    keys: list[tuple[int, str]] = []
    for index, raw_site in enumerate(value):
        site_context = f"{context}[{index}]"
        site = _exact(
            raw_site,
            {"residue_name", "author_residue_number", "uniprot_sequence_position"},
            site_context,
        )
        residue_name = _string(site["residue_name"], f"{site_context}.residue_name")
        _require(
            len(residue_name) == 3 and residue_name.isalpha(),
            f"{site_context}.residue_name must be a three-letter residue name",
        )
        for field in ("author_residue_number", "uniprot_sequence_position"):
            _require(
                type(site[field]) is int and site[field] > 0,
                f"{site_context}.{field} must be a positive integer",
            )
        sites.append(site)
        keys.append((site["author_residue_number"], residue_name))
    _require(len(keys) == len(set(keys)), f"{context} contains duplicate sites")
    _require(keys == sorted(keys), f"{context} must be deterministically ordered")
    return sites


def _validate_context_evidence(
    evidence_value: Any,
    *,
    claim: dict[str, Any],
    source_bindings: _SourceBindings,
    context: str,
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    _require(
        isinstance(evidence_value, list) and evidence_value,
        f"{context}.evidence is incomplete",
    )
    evidence_by_id: dict[str, dict[str, Any]] = {}
    direct_binding_ids: set[str] = set()
    for index, raw_evidence in enumerate(evidence_value):
        evidence_context = f"{context}.evidence[{index}]"
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
                "source_binding_id",
                "source_sha256",
            },
            evidence_context,
        )
        evidence_id = _string(item["evidence_id"], f"{evidence_context}.evidence_id")
        _require(evidence_id not in evidence_by_id, f"{context} repeats evidence_id")
        role = item["evidence_role"]
        _require(
            role in {"direct_support", "corroboration_only"},
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
        _string(item["experimental_context"], f"{evidence_context}.experimental_context")
        binding_id = item["source_binding_id"]
        source_sha = item["source_sha256"]
        _require(
            (binding_id is None) == (source_sha is None),
            f"{evidence_context} source binding ID and hash must both be set or null",
        )
        if binding_id is not None:
            _string(binding_id, f"{evidence_context}.source_binding_id")
            _sha256(source_sha, f"{evidence_context}.source_sha256")
            binding = source_bindings.by_id.get(binding_id)
            _require(binding is not None, f"{evidence_context} cites an unknown binding ID")
            _require(
                binding["sha256"] == source_sha,
                f"{evidence_context} binding ID/hash pair differs",
            )
            _require(
                binding["artifact_kind"] == "primary_source",
                f"{evidence_context} evidence must bind a primary source",
            )
            if role == "direct_support":
                direct_binding_ids.add(binding_id)
        _require(
            role != "direct_support" or binding_id is not None,
            f"{evidence_context} direct support requires a bound primary source",
        )
        evidence_by_id[evidence_id] = item

    direct_ids = _strings(
        claim["direct_evidence_ids"], f"{context}.claim.direct_evidence_ids", minimum=1
    )
    corroborating_ids = _strings(
        claim["corroborating_evidence_ids"],
        f"{context}.claim.corroborating_evidence_ids",
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
    return evidence_by_id, direct_binding_ids


def _validate_projection_context(
    projection_binding: dict[str, Any],
    *,
    record_binding: dict[str, Any],
    proposal_binding: dict[str, Any],
    protein_context: dict[str, Any],
    site_mappings: list[dict[str, Any]],
    direct_binding_ids: set[str],
    structure_evidence_binding_id: str,
    paper_evidence_binding_id: str,
    source_bindings: _SourceBindings,
    context: str,
) -> None:
    binding_id = _string(projection_binding["binding_id"], f"{context}.binding_id")
    binding = source_bindings.by_id.get(binding_id)
    _require(binding is not None, f"{context} cites an unknown projection binding")
    _require(
        binding["artifact_kind"] == "project_projection",
        f"{context} must bind a project projection",
    )
    projection_id = _string(
        projection_binding["projection_id"], f"{context}.projection_id"
    )
    context_id = _string(projection_binding["context_id"], f"{context}.context_id")
    projection_path = source_bindings.resolved_paths.get(binding_id)
    if projection_path is None:
        return
    projection = _exact(
        json.loads(projection_path.read_text(encoding="utf-8")),
        {
            "schema_version",
            "projection_id",
            "context_id",
            "proposal_binding",
            "source_bindings",
            "protein_context",
            "sites",
            "support_scope",
            "limits",
            "locators",
        },
        f"{context} source",
    )
    _require(
        projection["schema_version"] == _PROJECTION_SCHEMA_VERSION,
        f"{context} source schema is unsupported",
    )
    _require(projection["projection_id"] == projection_id, f"{context} ID differs")
    _require(projection["context_id"] == context_id, f"{context} context ID differs")

    projected_proposal = _exact(
        projection["proposal_binding"],
        {
            "record_id",
            "mcsa_id",
            "proposal_id",
            "source_mechanism_id",
            "reference",
        },
        f"{context} source.proposal_binding",
    )
    projected_reference = _exact(
        projected_proposal["reference"],
        {"doi", "pubmed_id", "pmc_id"},
        f"{context} source.proposal_binding.reference",
    )
    _string(projected_reference["doi"], f"{context} source reference DOI")
    _string(projected_reference["pmc_id"], f"{context} source reference PMC ID")
    _require(
        {
            "record_id": projected_proposal["record_id"],
            "mcsa_id": projected_proposal["mcsa_id"],
        }
        == {
            "record_id": record_binding["record_id"],
            "mcsa_id": record_binding["mcsa_id"],
        },
        f"{context} source record binding differs",
    )
    _require(
        {
            "proposal_id": projected_proposal["proposal_id"],
            "source_mechanism_id": projected_proposal["source_mechanism_id"],
            "reference_pubmed_id": projected_reference["pubmed_id"],
        }
        == proposal_binding,
        f"{context} source proposal binding differs",
    )

    projection_sources = projection["source_bindings"]
    _require(
        isinstance(projection_sources, list) and projection_sources,
        f"{context} source bindings are incomplete",
    )
    projection_source_ids: list[str] = []
    for index, raw_source in enumerate(projection_sources):
        source_context = f"{context} source.source_bindings[{index}]"
        source = _exact(raw_source, {"binding_id", "path", "sha256"}, source_context)
        source_id = _string(source["binding_id"], f"{source_context}.binding_id")
        _string(source["path"], f"{source_context}.path")
        _sha256(source["sha256"], f"{source_context}.sha256")
        _require(source_id not in projection_source_ids, f"{context} source binding repeats")
        top_binding = source_bindings.by_id.get(source_id)
        _require(top_binding is not None, f"{context} source binding is not declared")
        _require(
            {key: top_binding[key] for key in ("path", "sha256")}
            == {key: source[key] for key in ("path", "sha256")},
            f"{context} source binding differs from its declaration",
        )
        projection_source_ids.append(source_id)
    _require(
        [source["path"] for source in projection_sources]
        == sorted(source["path"] for source in projection_sources),
        f"{context} source bindings are not ordered",
    )
    _require(
        direct_binding_ids <= set(projection_source_ids),
        f"{context} direct evidence is absent from the projection sources",
    )

    projected_protein = _exact(
        projection["protein_context"],
        {
            "pdb_id",
            "entity_id",
            "author_chain_id",
            "struct_asym_id",
            "organism",
            "taxonomy_id",
            "uniprot_accession",
            "mapped_interval",
            "construct_length",
            "expression_tag_interval",
        },
        f"{context} source.protein_context",
    )
    for field in ("pdb_id", "entity_id", "author_chain_id", "struct_asym_id", "organism", "uniprot_accession"):
        _string(projected_protein[field], f"{context} source.protein_context.{field}")
    for field in ("taxonomy_id", "construct_length"):
        _require(
            type(projected_protein[field]) is int and projected_protein[field] > 0,
            f"{context} source.protein_context.{field} is invalid",
        )
    mapped_interval = _exact(
        projected_protein["mapped_interval"],
        {"structure", "author", "uniprot"},
        f"{context} source.protein_context.mapped_interval",
    )
    for name, interval in [
        *mapped_interval.items(),
        ("expression_tag", projected_protein["expression_tag_interval"]),
    ]:
        _require(
            isinstance(interval, list)
            and len(interval) == 2
            and all(type(value) is int and value > 0 for value in interval)
            and interval[0] <= interval[1],
            f"{context} source.protein_context.{name} interval is invalid",
        )
    projected_compact_protein = {
        "pdb_id": projected_protein["pdb_id"],
        "chain_id": projected_protein["author_chain_id"],
        "uniprot_id": projected_protein["uniprot_accession"],
    }
    _require(
        projected_compact_protein == protein_context,
        f"{context} protein context differs",
    )

    raw_sites = projection["sites"]
    _require(isinstance(raw_sites, list) and raw_sites, f"{context} source sites are empty")
    projected_sites: list[dict[str, Any]] = []
    for index, raw_site in enumerate(raw_sites):
        site_context = f"{context} source.sites[{index}]"
        site = _exact(
            raw_site,
            {
                "residue_name",
                "author_residue_number",
                "label_seq_id",
                "uniprot_position",
                "locator_ids",
            },
            site_context,
        )
        _string(site["residue_name"], f"{site_context}.residue_name")
        for field in ("author_residue_number", "label_seq_id", "uniprot_position"):
            _require(
                type(site[field]) is int and site[field] > 0,
                f"{site_context}.{field} is invalid",
            )
        _strings(site["locator_ids"], f"{site_context}.locator_ids", minimum=1)
        projected_sites.append(
            {
                "residue_name": site["residue_name"],
                "author_residue_number": site["author_residue_number"],
                "uniprot_sequence_position": site["uniprot_position"],
            }
        )
    _require(
        projected_sites == site_mappings,
        f"{context} site mappings differ",
    )
    _require(
        projection["support_scope"] == _PROTEIN_SUPPORT_SCOPE,
        f"{context} source support scope differs",
    )
    _require(
        isinstance(projection["limits"], list) and projection["limits"],
        f"{context} source limits are empty",
    )
    raw_locators = projection["locators"]
    _require(isinstance(raw_locators, list) and raw_locators, f"{context} source locators are empty")
    locators: dict[str, dict[str, Any]] = {}
    for index, raw_locator in enumerate(raw_locators):
        locator_context = f"{context} source.locators[{index}]"
        locator = _exact(
            raw_locator,
            {
                "locator_id",
                "source_binding_id",
                "source_format",
                "selector",
                "physical_lines",
                "extracted_values",
                "supports",
            },
            locator_context,
        )
        locator_id = _string(locator["locator_id"], f"{locator_context}.locator_id")
        _require(locator_id not in locators, f"{context} source repeats locator_id")
        locator_source_id = _string(
            locator["source_binding_id"], f"{locator_context}.source_binding_id"
        )
        _require(
            locator_source_id in projection_source_ids,
            f"{locator_context} cites an undeclared source",
        )
        _string(locator["source_format"], f"{locator_context}.source_format")
        _object(locator["selector"], f"{locator_context}.selector")
        _object(locator["extracted_values"], f"{locator_context}.extracted_values")
        _require(
            isinstance(locator["physical_lines"], list)
            and locator["physical_lines"]
            and all(type(line) is int and line > 0 for line in locator["physical_lines"]),
            f"{locator_context}.physical_lines are invalid",
        )
        _string(locator["supports"], f"{locator_context}.supports")
        locators[locator_id] = locator
    for site_index, site in enumerate(raw_sites):
        _require(
            set(site["locator_ids"]) <= set(locators),
            f"{context} source.sites[{site_index}] cites an unknown locator",
        )
    _require(
        any(
            locator["source_binding_id"] == structure_evidence_binding_id
            and locator["extracted_values"].get("entry_id") == protein_context["pdb_id"]
            for locator in locators.values()
        ),
        f"{context} structure evidence binding lacks an identity locator",
    )
    _require(
        any(
            locator["source_binding_id"] == paper_evidence_binding_id
            and str(locator["extracted_values"].get("pubmed_id"))
            == proposal_binding["reference_pubmed_id"]
            for locator in locators.values()
        ),
        f"{context} paper evidence binding lacks a PMID locator",
    )


def _validate_proposal_context_annotation(
    raw_annotation: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    source_bindings: _SourceBindings,
    context: str,
) -> tuple[str, str]:
    annotation = _exact(raw_annotation, _PROPOSAL_CONTEXT_ANNOTATION_FIELDS, context)
    annotation_id = _string(annotation["annotation_id"], f"{context}.annotation_id")
    _require(
        annotation["annotation_kind"] == "source_proposal_protein_context",
        f"{context}.annotation_kind is unsupported",
    )
    _require(
        annotation["target_scope"] == "source_proposal_only",
        f"{context} target scope is invalid",
    )
    record_id, record = _bound_record(
        annotation["record_binding"],
        record_by_id=record_by_id,
        context=f"{context}.record_binding",
    )

    proposal_binding = _exact(
        annotation["proposal_binding"],
        {"proposal_id", "source_mechanism_id", "reference_pubmed_id"},
        f"{context}.proposal_binding",
    )
    proposal_id = _string(
        proposal_binding["proposal_id"], f"{context}.proposal_binding.proposal_id"
    )
    source_mechanism_id = proposal_binding["source_mechanism_id"]
    _require(
        type(source_mechanism_id) is int and source_mechanism_id > 0,
        f"{context}.proposal_binding.source_mechanism_id must be a positive integer",
    )
    reference_pubmed_id = _string(
        proposal_binding["reference_pubmed_id"],
        f"{context}.proposal_binding.reference_pubmed_id",
    )
    _require(reference_pubmed_id.isdigit(), f"{context} reference PMID is invalid")
    proposals = [
        proposal
        for proposal in record["mechanism_proposals"]
        if proposal["source_mechanism_id"] == source_mechanism_id
    ]
    _require(len(proposals) == 1, f"{context} source mechanism binding is absent")
    proposal = proposals[0]
    _require(proposal["proposal_id"] == proposal_id, f"{context} proposal ID differs")
    _require(
        reference_pubmed_id
        in {reference["pubmed_id"] for reference in proposal["source_references"]},
        f"{context} proposal reference PMID is absent",
    )

    projection_binding = _exact(
        annotation["projection_binding"],
        {"binding_id", "projection_id", "context_id"},
        f"{context}.projection_binding",
    )
    claim = _exact(
        annotation["claim"],
        {
            "statement",
            "protein_context",
            "site_mappings",
            "support_scope",
            "direct_evidence_ids",
            "corroborating_evidence_ids",
        },
        f"{context}.claim",
    )
    _string(claim["statement"], f"{context}.claim.statement")
    protein_context = _exact(
        claim["protein_context"],
        {"pdb_id", "chain_id", "uniprot_id"},
        f"{context}.claim.protein_context",
    )
    _require(
        isinstance(protein_context["pdb_id"], str)
        and _PDB_RE.fullmatch(protein_context["pdb_id"]),
        f"{context} structure PDB ID is invalid",
    )
    _string(protein_context["chain_id"], f"{context}.claim.protein_context.chain_id")
    _require(
        isinstance(protein_context["uniprot_id"], str)
        and _UNIPROT_RE.fullmatch(protein_context["uniprot_id"]) is not None,
        f"{context} protein context UniProt ID is invalid",
    )
    sites = _site_mappings(claim["site_mappings"], f"{context}.claim.site_mappings")
    support_scope = _exact(
        claim["support_scope"], set(_PROTEIN_SUPPORT_SCOPE), f"{context}.claim.support_scope"
    )
    _require(
        support_scope == _PROTEIN_SUPPORT_SCOPE,
        f"{context} protein-context support scope overclaims",
    )
    evidence_by_id, direct_binding_ids = _validate_context_evidence(
        annotation["evidence"],
        claim=claim,
        source_bindings=source_bindings,
        context=context,
    )
    expected_sources = (
        ("primary_structure_record", f"RCSB PDB:{protein_context['pdb_id']}"),
        ("primary_research_article", f"PubMed:{reference_pubmed_id}"),
    )
    direct_source_rows: list[dict[str, Any]] = []
    for source_kind, source_id in expected_sources:
        matches = [
            item
            for item in evidence_by_id.values()
            if item["evidence_role"] == "direct_support"
            and item["source_kind"] == source_kind
            and item["source_id"] == source_id
        ]
        _require(
            len(matches) == 1,
            f"{context} lacks unique direct structure or proposal-reference evidence",
        )
        direct_source_rows.append(matches[0])
    _require(
        all(item["source_binding_id"] is not None for item in direct_source_rows),
        f"{context} direct source binding is absent",
    )
    _validate_projection_context(
        projection_binding,
        record_binding=annotation["record_binding"],
        proposal_binding=proposal_binding,
        protein_context=protein_context,
        site_mappings=sites,
        direct_binding_ids=direct_binding_ids,
        structure_evidence_binding_id=direct_source_rows[0]["source_binding_id"],
        paper_evidence_binding_id=direct_source_rows[1]["source_binding_id"],
        source_bindings=source_bindings,
        context=f"{context}.projection_binding",
    )
    _validate_limits_and_scope(
        annotation, context, required_limits=_PROPOSAL_CONTEXT_LIMITS
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
    schema_version = sidecar["schema_version"]
    _require(
        schema_version in {PRIMARY_EVIDENCE_SCHEMA_V1, PRIMARY_EVIDENCE_SCHEMA_VERSION},
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

    source_bindings = _validate_source_bindings(
        sidecar["source_bindings"],
        schema_version=schema_version,
        repo_root=repo_root,
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
        annotation_context = f"annotations[{index}]"
        annotation_object = _object(raw_annotation, annotation_context)
        if annotation_object.get("annotation_kind") == "primary_structure_observation":
            annotation_id, record_id = _validate_structure_annotation(
                raw_annotation,
                record_by_id=record_by_id,
                source_bindings=source_bindings,
                schema_version=schema_version,
                context=annotation_context,
            )
        elif (
            schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION
            and annotation_object.get("annotation_kind")
            == "source_proposal_protein_context"
        ):
            annotation_id, record_id = _validate_proposal_context_annotation(
                raw_annotation,
                record_by_id=record_by_id,
                source_bindings=source_bindings,
                context=annotation_context,
            )
        else:
            raise ValueError(f"{annotation_context}.annotation_kind is unsupported")
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
