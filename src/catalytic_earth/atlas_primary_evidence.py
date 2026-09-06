"""Validated record-level primary-evidence annotations for Atlas drafts.

Annotations are an additive query sidecar.  They cannot change a source draft's
evidence tier, permissions, mechanism scope, proposals, or source steps.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .atlas_drafts import validate_source_drafts
from .canonical_hash import canonical_file_sha256


PRIMARY_EVIDENCE_SCHEMA_V1 = "catalytic-earth.atlas-primary-evidence.v1"
PRIMARY_EVIDENCE_SCHEMA_V2 = "catalytic-earth.atlas-primary-evidence.v2"
PRIMARY_EVIDENCE_SCHEMA_VERSION = "catalytic-earth.atlas-primary-evidence.v3"
PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE = (
    "Do not automatically refresh this pin after annotation changes. "
    "Repeat source-to-claim primary-evidence review first."
)
PRIMARY_EVIDENCE_STATUS = (
    "reviewed_primary_evidence_annotations_not_mechanism_expansion"
)
PRIMARY_EVIDENCE_REVIEWER_KIND = "same_model_computational_agents"
PRIMARY_OBSERVED_STATE_KINDS = frozenset(
    {
        "polymer_modified_component",
        "bound_ligand_analogue",
        "bound_ligand_adduct",
        "protein_ligand_covalent_adduct",
    }
)

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
_OBSERVED_STATE_CONTEXT_ANNOTATION_FIELDS = _ANNOTATION_FIELDS | {
    "projection_binding",
    "projection_excerpt",
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
_OBSERVED_STATE_PROJECTION_SCHEMA_VERSION = (
    "catalytic-earth.primary-observed-state-projection.v1"
)
_OBSERVED_STATE_REQUIRED_LIMITS = {
    "chemical_identity_beyond_source": "abstained",
    "exact_reaction_instance": "abstained",
    "mechanism_applicability": "abstained",
    "state_trajectory": "abstained",
}

_TYPED_BINDING_SCHEMA_VERSIONS = {
    PRIMARY_EVIDENCE_SCHEMA_V2,
    PRIMARY_EVIDENCE_SCHEMA_VERSION,
}


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
    try:
        raw = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("primary-evidence payload must be canonical JSON") from exc
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
        if schema_version in _TYPED_BINDING_SCHEMA_VERSIONS:
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
        if schema_version in _TYPED_BINDING_SCHEMA_VERSIONS:
            binding_id = _string(binding["binding_id"], f"{context}.binding_id")
            _require(binding_id not in by_id, f"{context} repeats binding_id")
            allowed_artifact_kinds = {
                "primary_source",
                "project_projection",
                "source_inventory",
                "attribution",
            }
            if schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION:
                allowed_artifact_kinds |= {
                    "curated_reference",
                    "primary_source_projection",
                    "source_record_snapshot",
                }
            _require(
                binding["artifact_kind"] in allowed_artifact_kinds,
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
                schema_version in _TYPED_BINDING_SCHEMA_VERSIONS
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


def _optional_positive_int(value: Any, context: str) -> int | None:
    _require(
        value is None or (type(value) is int and value > 0),
        f"{context} must be null or a positive integer",
    )
    return value


def _validate_observed_structure_context(value: Any, context: str) -> dict[str, Any]:
    result = _exact(
        value,
        {
            "pdb_id",
            "model_id",
            "protein_entity_ids",
            "protein_label_asym_ids",
            "protein_author_chain_ids",
            "curated_protein_accession",
        },
        context,
    )
    _require(
        isinstance(result["pdb_id"], str) and _PDB_RE.fullmatch(result["pdb_id"]),
        f"{context}.pdb_id is invalid",
    )
    _require(
        type(result["model_id"]) is int and result["model_id"] > 0,
        f"{context}.model_id must be a positive integer",
    )
    for field in (
        "protein_entity_ids",
        "protein_label_asym_ids",
        "protein_author_chain_ids",
    ):
        values = _strings(result[field], f"{context}.{field}", minimum=1)
        _require(values == sorted(values), f"{context}.{field} must be ordered")
    accession = result["curated_protein_accession"]
    _require(
        accession is None
        or (isinstance(accession, str) and _UNIPROT_RE.fullmatch(accession) is not None),
        f"{context}.curated_protein_accession is invalid",
    )
    return result


def _validate_observed_entity(value: Any, context: str) -> dict[str, Any]:
    result = _exact(
        value,
        {
            "state_kind",
            "entity_context",
            "entity_id",
            "source_component_id",
            "source_description",
            "chemical_context",
            "attachment_context",
            "normalized_chebi_id",
        },
        context,
    )
    state_kind = result["state_kind"]
    _require(
        state_kind in PRIMARY_OBSERVED_STATE_KINDS,
        f"{context}.state_kind is unsupported",
    )
    _require(
        result["entity_context"] in {"polymer_component", "nonpolymer_component"},
        f"{context}.entity_context is invalid",
    )
    _string(result["entity_id"], f"{context}.entity_id")
    _string(result["source_component_id"], f"{context}.source_component_id")
    _string(result["source_description"], f"{context}.source_description")
    _require(
        result["chemical_context"]
        in {
            "processed_state",
            "source_designated_analogue",
            "source_described_bound_adduct",
            "deposit_described_bound_intermediate",
        },
        f"{context}.chemical_context is invalid",
    )
    _require(
        result["attachment_context"]
        in {
            "polymer_integrated",
            "absent_from_deposited_struct_conn",
            "deposited_covalent_connection",
        },
        f"{context}.attachment_context is invalid",
    )
    _require(
        result["normalized_chebi_id"] is None,
        f"{context} cannot turn a deposited state into a free ChEBI participant",
    )
    required_pair = {
        "polymer_modified_component": (
            "polymer_component",
            "processed_state",
            "polymer_integrated",
        ),
        "bound_ligand_analogue": (
            "nonpolymer_component",
            "source_designated_analogue",
            "absent_from_deposited_struct_conn",
        ),
        "bound_ligand_adduct": (
            "nonpolymer_component",
            "source_described_bound_adduct",
            "absent_from_deposited_struct_conn",
        ),
        "protein_ligand_covalent_adduct": (
            "nonpolymer_component",
            "deposit_described_bound_intermediate",
            "deposited_covalent_connection",
        ),
    }[state_kind]
    _require(
        (
            result["entity_context"],
            result["chemical_context"],
            result["attachment_context"],
        )
        == required_pair,
        f"{context} state/context combination overclaims or is inconsistent",
    )
    return result


def _validate_chemical_observations(
    value: Any,
    *,
    observed_entity: dict[str, Any],
    context: str,
) -> list[dict[str, Any]]:
    """Validate separately scoped source descriptions without reconciling them."""

    _require(isinstance(value, list) and value, f"{context} must be nonempty")
    observations: list[dict[str, Any]] = []
    observation_ids: list[str] = []
    allowed_pairs = {
        "deposited_component_state": "deposited_structure",
        "deposited_component_bond_order": "deposited_structure",
        "deposited_component_dictionary_bond_order": "deposited_structure",
        "deposited_modeled_instance_atom_inventory": "deposited_structure",
        "deposited_state_description": "deposited_structure",
        "primary_article_state_description": "primary_research_article",
    }
    for index, raw_observation in enumerate(value):
        observation_context = f"{context}[{index}]"
        raw_observation_object = _object(raw_observation, observation_context)
        kind = raw_observation_object.get("observation_kind")
        observation_fields = {
            "observation_id",
            "source_scope",
            "observation_kind",
            "source_description",
            "source_bond_order_code",
            "evidence_ids",
            "support_edge_ids",
        }
        if kind == "deposited_component_dictionary_bond_order":
            observation_fields.add("source_atom_ids")
        elif kind == "deposited_modeled_instance_atom_inventory":
            observation_fields.update({"modeled_instance_indices", "omitted_atom_ids"})
        observation = _exact(
            raw_observation_object,
            observation_fields,
            observation_context,
        )
        observation_id = _string(
            observation["observation_id"], f"{observation_context}.observation_id"
        )
        _require(
            observation_id not in observation_ids,
            f"{context} repeats observation_id",
        )
        observation_ids.append(observation_id)
        kind = observation["observation_kind"]
        _require(kind in allowed_pairs, f"{observation_context}.observation_kind is invalid")
        _require(
            observation["source_scope"] == allowed_pairs[kind],
            f"{observation_context} source scope differs from observation kind",
        )
        _string(
            observation["source_description"],
            f"{observation_context}.source_description",
        )
        bond_order = observation["source_bond_order_code"]
        if kind in {
            "deposited_component_bond_order",
            "deposited_component_dictionary_bond_order",
        }:
            _require(
                isinstance(bond_order, str)
                and bool(re.fullmatch(r"[A-Za-z0-9_.+-]+", bond_order)),
                f"{observation_context}.source_bond_order_code is invalid",
            )
        else:
            _require(
                bond_order is None,
                f"{observation_context} cannot assign a deposited bond-order code",
            )
        if kind == "deposited_component_dictionary_bond_order":
            atom_ids = _strings(
                observation["source_atom_ids"],
                f"{observation_context}.source_atom_ids",
                minimum=2,
            )
            _require(
                len(atom_ids) == 2,
                f"{observation_context}.source_atom_ids must name one source bond",
            )
        elif kind == "deposited_modeled_instance_atom_inventory":
            indices = observation["modeled_instance_indices"]
            _require(
                isinstance(indices, list)
                and indices
                and all(type(item) is int and item >= 0 for item in indices)
                and indices == sorted(set(indices)),
                f"{observation_context}.modeled_instance_indices are invalid",
            )
            omitted = _strings(
                observation["omitted_atom_ids"],
                f"{observation_context}.omitted_atom_ids",
                minimum=1,
            )
            _require(
                omitted == sorted(omitted),
                f"{observation_context}.omitted_atom_ids must be ordered",
            )
        _strings(
            observation["evidence_ids"],
            f"{observation_context}.evidence_ids",
            minimum=1,
        )
        _strings(
            observation["support_edge_ids"],
            f"{observation_context}.support_edge_ids",
            minimum=1,
        )
        observations.append(observation)
    _require(
        observation_ids == sorted(observation_ids),
        f"{context} must be deterministically ordered",
    )

    kinds = {item["observation_kind"] for item in observations}
    state_kind = observed_entity["state_kind"]
    if state_kind == "polymer_modified_component":
        required = {"deposited_component_state"}
    elif state_kind == "bound_ligand_analogue":
        required = {
            "deposited_component_state",
            "primary_article_state_description",
        }
    elif state_kind == "bound_ligand_adduct":
        required = {
            "deposited_component_bond_order",
            "primary_article_state_description",
        }
    else:
        required = {
            "deposited_component_state",
            "deposited_state_description",
        }
        conflict_kinds = {
            "deposited_component_dictionary_bond_order",
            "deposited_modeled_instance_atom_inventory",
        }
        _require(
            not (kinds & conflict_kinds) or conflict_kinds <= kinds,
            f"{context} must preserve dictionary and modeled-instance scopes together",
        )
    _require(
        required <= kinds,
        f"{context} observations do not preserve the state-specific source scopes",
    )
    return observations


def _validate_chemical_reconciliation(
    value: Any,
    *,
    observed_entity: dict[str, Any],
    context: str,
) -> dict[str, Any]:
    result = _exact(value, {"status", "statement"}, context)
    allowed_statuses = {
        "polymer_modified_component": {"not_required"},
        "bound_ligand_analogue": {"source_scopes_separated"},
        "bound_ligand_adduct": {
            "source_scopes_separated",
            "unresolved_source_description_vs_deposit",
        },
        "protein_ligand_covalent_adduct": {
            "source_scopes_separated",
            "unresolved_component_dictionary_vs_bound_instance_and_connection",
        },
    }[observed_entity["state_kind"]]
    _require(
        result["status"] in allowed_statuses,
        f"{context}.status does not preserve the source boundary",
    )
    _string(result["statement"], f"{context}.statement")
    return result


def _validate_structure_instances(value: Any, context: str) -> list[dict[str, Any]]:
    _require(isinstance(value, list) and value, f"{context} must be nonempty")
    result: list[dict[str, Any]] = []
    keys: list[tuple[str, str, int]] = []
    for index, raw_instance in enumerate(value):
        instance_context = f"{context}[{index}]"
        instance = _exact(
            raw_instance,
            {
                "label_asym_id",
                "label_entity_id",
                "label_component_id",
                "label_seq_id",
                "atom_author_chain_id",
                "atom_author_component_id",
                "atom_author_residue_number",
                "source_author_component_id",
                "source_author_residue_number",
                "structure_site_id",
            },
            instance_context,
        )
        for field in (
            "label_asym_id",
            "label_entity_id",
            "label_component_id",
            "atom_author_chain_id",
            "atom_author_component_id",
        ):
            _string(instance[field], f"{instance_context}.{field}")
        _optional_positive_int(instance["label_seq_id"], f"{instance_context}.label_seq_id")
        _require(
            type(instance["atom_author_residue_number"]) is int
            and instance["atom_author_residue_number"] > 0,
            f"{instance_context}.atom_author_residue_number is invalid",
        )
        source_author_component = instance["source_author_component_id"]
        source_author_number = instance["source_author_residue_number"]
        _require(
            (source_author_component is None) == (source_author_number is None),
            f"{instance_context} source-author component/number must both be set or null",
        )
        if source_author_component is not None:
            _string(
                source_author_component,
                f"{instance_context}.source_author_component_id",
            )
            _optional_positive_int(
                source_author_number,
                f"{instance_context}.source_author_residue_number",
            )
        structure_site_id = instance["structure_site_id"]
        _require(
            structure_site_id is None
            or (isinstance(structure_site_id, str) and bool(structure_site_id)),
            f"{instance_context}.structure_site_id is invalid",
        )
        result.append(instance)
        keys.append(
            (
                instance["label_asym_id"],
                instance["label_component_id"],
                instance["atom_author_residue_number"],
            )
        )
    _require(len(keys) == len(set(keys)), f"{context} contains duplicate instances")
    _require(keys == sorted(keys), f"{context} must be deterministically ordered")
    return result


def _validate_attachment_endpoint(
    value: Any,
    *,
    polymer: bool,
    context: str,
) -> dict[str, Any]:
    result = _exact(
        value,
        {
            "label_asym_id",
            "label_entity_id",
            "label_component_id",
            "label_seq_id",
            "atom_author_chain_id",
            "atom_author_component_id",
            "atom_author_residue_number",
            "atom_name",
        },
        context,
    )
    for field in (
        "label_asym_id",
        "label_entity_id",
        "label_component_id",
        "atom_author_chain_id",
        "atom_author_component_id",
        "atom_name",
    ):
        _string(result[field], f"{context}.{field}")
    label_seq_id = _optional_positive_int(
        result["label_seq_id"], f"{context}.label_seq_id"
    )
    _require(
        (label_seq_id is not None) is polymer,
        f"{context}.label_seq_id differs from the endpoint namespace",
    )
    _require(
        type(result["atom_author_residue_number"]) is int
        and result["atom_author_residue_number"] > 0,
        f"{context}.atom_author_residue_number is invalid",
    )
    return result


def _attachment_edge_values(attachment: dict[str, Any]) -> dict[str, Any]:
    return {
        key: attachment[key]
        for key in (
            "connection_id",
            "raw_conn_type",
            "observed_instance_index",
            "ligand_endpoint",
            "protein_endpoint",
            "distance_angstrom",
            "source_bond_order_code",
            "source_bond_order_token",
        )
    }


def _attachment_locator_values(attachment: dict[str, Any]) -> dict[str, Any]:
    result = _attachment_edge_values(attachment)
    result.pop("observed_instance_index")
    result.pop("source_bond_order_code")
    return result


def _validate_protein_attachments(
    value: Any,
    *,
    structure_context: dict[str, Any],
    structure_instances: list[dict[str, Any]],
    context: str,
) -> list[dict[str, Any]]:
    """Validate exact deposited connections without assigning canonical sites."""

    _require(isinstance(value, list) and value, f"{context} must be nonempty")
    attachments: list[dict[str, Any]] = []
    attachment_ids: list[str] = []
    connection_ids: list[str] = []
    instance_indices: list[int] = []
    support_edge_ids: list[str] = []
    for index, raw_attachment in enumerate(value):
        attachment_context = f"{context}[{index}]"
        attachment = _exact(
            raw_attachment,
            {
                "attachment_id",
                "connection_id",
                "raw_conn_type",
                "observed_instance_index",
                "ligand_endpoint",
                "protein_endpoint",
                "distance_angstrom",
                "source_bond_order_code",
                "source_bond_order_token",
                "support_edge_ids",
            },
            attachment_context,
        )
        attachment_id = _string(
            attachment["attachment_id"], f"{attachment_context}.attachment_id"
        )
        connection_id = _string(
            attachment["connection_id"], f"{attachment_context}.connection_id"
        )
        _require(
            attachment["raw_conn_type"] == "covale",
            f"{attachment_context}.raw_conn_type is not deposited covalent",
        )
        instance_index = attachment["observed_instance_index"]
        _require(
            type(instance_index) is int
            and 0 <= instance_index < len(structure_instances),
            f"{attachment_context}.observed_instance_index is invalid",
        )
        ligand_endpoint = _validate_attachment_endpoint(
            attachment["ligand_endpoint"],
            polymer=False,
            context=f"{attachment_context}.ligand_endpoint",
        )
        protein_endpoint = _validate_attachment_endpoint(
            attachment["protein_endpoint"],
            polymer=True,
            context=f"{attachment_context}.protein_endpoint",
        )
        instance = structure_instances[instance_index]
        _require(
            ligand_endpoint
            == {
                "label_asym_id": instance["label_asym_id"],
                "label_entity_id": instance["label_entity_id"],
                "label_component_id": instance["label_component_id"],
                "label_seq_id": instance["label_seq_id"],
                "atom_author_chain_id": instance["atom_author_chain_id"],
                "atom_author_component_id": instance["atom_author_component_id"],
                "atom_author_residue_number": instance["atom_author_residue_number"],
                "atom_name": ligand_endpoint["atom_name"],
            },
            f"{attachment_context} ligand endpoint differs from its observed instance",
        )
        _require(
            protein_endpoint["label_asym_id"]
            in structure_context["protein_label_asym_ids"]
            and protein_endpoint["label_entity_id"]
            in structure_context["protein_entity_ids"]
            and protein_endpoint["atom_author_chain_id"]
            in structure_context["protein_author_chain_ids"],
            f"{attachment_context} protein endpoint differs from structure context",
        )
        distance = attachment["distance_angstrom"]
        _require(
            type(distance) in {int, float}
            and math.isfinite(distance)
            and distance > 0,
            f"{attachment_context}.distance_angstrom is invalid",
        )
        _require(
            attachment["source_bond_order_code"] is None
            and attachment["source_bond_order_token"] == "?",
            f"{attachment_context} must preserve unknown deposited bond order",
        )
        edge_ids = _strings(
            attachment["support_edge_ids"],
            f"{attachment_context}.support_edge_ids",
            minimum=1,
        )
        _require(
            len(edge_ids) == 1,
            f"{attachment_context} must bind one exact deposited connection edge",
        )
        attachment_ids.append(attachment_id)
        connection_ids.append(connection_id)
        instance_indices.append(instance_index)
        support_edge_ids.extend(edge_ids)
        attachments.append(attachment)

    _require(
        len(attachment_ids) == len(set(attachment_ids)),
        f"{context} repeats attachment_id",
    )
    _require(
        len(connection_ids) == len(set(connection_ids)),
        f"{context} repeats connection_id",
    )
    _require(
        len(support_edge_ids) == len(set(support_edge_ids)),
        f"{context} reuses a deposited connection edge",
    )
    _require(
        instance_indices == list(range(len(structure_instances))),
        f"{context} must cover every observed instance exactly once in source order",
    )
    return attachments


def _validate_canonical_site(value: Any, context: str) -> dict[str, Any]:
    result = _exact(value, {"accession", "residue_name", "sequence_position"}, context)
    _require(
        isinstance(result["accession"], str)
        and _UNIPROT_RE.fullmatch(result["accession"]) is not None,
        f"{context}.accession is invalid",
    )
    residue_name = _string(result["residue_name"], f"{context}.residue_name")
    _require(
        len(residue_name) == 3 and residue_name.isalpha() and residue_name.isupper(),
        f"{context}.residue_name must be an uppercase three-letter code",
    )
    _require(
        type(result["sequence_position"]) is int
        and result["sequence_position"] > 0,
        f"{context}.sequence_position is invalid",
    )
    return result


def _validate_source_record_alias(value: Any, context: str) -> dict[str, Any]:
    result = _exact(
        value,
        {
            "source_assertion_id",
            "pdb_id",
            "chain_id",
            "label_position",
            "author_position",
            "residue_code",
            "ptm_name",
        },
        context,
    )
    _string(result["source_assertion_id"], f"{context}.source_assertion_id")
    _require(
        isinstance(result["pdb_id"], str) and _PDB_RE.fullmatch(result["pdb_id"]),
        f"{context}.pdb_id is invalid",
    )
    _string(result["chain_id"], f"{context}.chain_id")
    for field in ("label_position", "author_position"):
        _require(
            type(result[field]) is int and result[field] > 0,
            f"{context}.{field} is invalid",
        )
    _string(result["residue_code"], f"{context}.residue_code")
    _string(result["ptm_name"], f"{context}.ptm_name")
    return result


def _validate_site_crosswalk(
    value: Any,
    *,
    structure_instances: list[dict[str, Any]],
    context: str,
) -> dict[str, Any]:
    result = _exact(
        value,
        {
            "status",
            "relationship",
            "structure_instance_index",
            "canonical_site",
            "source_record_alias",
            "author_number_mapping_status",
            "support_edge_ids",
        },
        context,
    )
    support_edge_ids = _strings(result["support_edge_ids"], f"{context}.support_edge_ids")
    if result["status"] == "not_asserted":
        _require(
            result["relationship"] == "not_asserted"
            and result["structure_instance_index"] is None
            and result["canonical_site"] is None
            and result["source_record_alias"] is None
            and result["author_number_mapping_status"] == "not_asserted"
            and not support_edge_ids,
            f"{context} unresolved crosswalk contains a mapping claim",
        )
        return result
    _require(
        result["status"] == "cross_source_curated_projection",
        f"{context}.status is invalid",
    )
    _require(
        result["relationship"]
        in {
            "precursor_residue_to_processed_component",
            "same_residue_sequence_correspondence",
        },
        f"{context}.relationship is invalid",
    )
    instance_index = result["structure_instance_index"]
    _require(
        type(instance_index) is int and 0 <= instance_index < len(structure_instances),
        f"{context}.structure_instance_index is invalid",
    )
    _validate_canonical_site(result["canonical_site"], f"{context}.canonical_site")
    _validate_source_record_alias(
        result["source_record_alias"], f"{context}.source_record_alias"
    )
    selected_instance = structure_instances[instance_index]
    source_alias = result["source_record_alias"]
    _require(
        selected_instance["atom_author_chain_id"] == source_alias["chain_id"]
        and selected_instance["label_seq_id"] == source_alias["label_position"],
        f"{context} selected structure instance differs from its source alias",
    )
    _require(
        result["author_number_mapping_status"] == "not_asserted",
        f"{context} cannot project a source author number onto the PDB author namespace",
    )
    _require(len(support_edge_ids) >= 3, f"{context} lacks decomposed support edges")
    return result


def _validate_crosswalk_against_source_record(
    crosswalk: dict[str, Any],
    *,
    record: dict[str, Any],
    context: str,
) -> None:
    """Bind a declared cross-source edge to the compiled source assertion.

    This deliberately checks only fields preserved by the generic source-draft
    record.  The project projection and its manual review remain responsible
    for primary-structure and curated-record locators.
    """

    if crosswalk["status"] == "not_asserted":
        return
    alias = crosswalk["source_record_alias"]
    matches = [
        assertion
        for assertion in record["source_residue_assertions"]
        if assertion["assertion_id"] == alias["source_assertion_id"]
    ]
    _require(len(matches) == 1, f"{context} source assertion is absent")
    assertion = matches[0]
    structure_matches = [
        location
        for location in assertion["source_structure_locations"]
        if location["pdb_id"] == alias["pdb_id"]
        and location["chain_id"] == alias["chain_id"]
        and location["label_position"] == alias["label_position"]
        and location["author_position"] == alias["author_position"]
        and location["residue_name"].upper() == alias["residue_code"].upper()
    ]
    _require(
        len(structure_matches) == 1,
        f"{context} source structure alias differs from the compiled assertion",
    )
    canonical = crosswalk["canonical_site"]
    sequence_matches = [
        location
        for location in assertion["source_sequence_locations"]
        if location["uniprot_id"] == canonical["accession"]
        and location["sequence_position"] == canonical["sequence_position"]
        and location["residue_name"].upper() == canonical["residue_name"]
    ]
    _require(
        len(sequence_matches) == 1,
        f"{context} canonical site differs from the compiled source assertion",
    )


def _validate_observed_context_evidence(
    evidence_value: Any,
    *,
    claim: dict[str, Any],
    record: dict[str, Any],
    source_bindings: _SourceBindings,
    context: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]], dict[str, set[str]]]:
    _require(
        isinstance(evidence_value, list) and evidence_value,
        f"{context}.evidence is incomplete",
    )
    evidence_by_id: dict[str, dict[str, Any]] = {}
    ids_by_role: dict[str, set[str]] = {
        "direct_support": set(),
        "curated_identity_support": set(),
        "source_record_only": set(),
        "corroboration_only": set(),
    }
    bindings_by_role: dict[str, set[str]] = {role: set() for role in ids_by_role}
    allowed_kinds = {
        "primary_structure_record",
        "primary_research_article",
        "curated_protein_record",
        "official_source_record",
        "official_structure_metadata",
        "curated_chemical_component_record",
    }
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
        _require(role in ids_by_role, f"{evidence_context}.evidence_role is invalid")
        source_kind = item["source_kind"]
        _require(source_kind in allowed_kinds, f"{evidence_context}.source_kind is invalid")
        _string(item["source_id"], f"{evidence_context}.source_id")
        uri = _string(item["uri"], f"{evidence_context}.uri")
        _require(uri.startswith("https://"), f"{evidence_context}.uri must use HTTPS")
        _string(item["citation"], f"{evidence_context}.citation")
        _string(item["experimental_context"], f"{evidence_context}.experimental_context")
        binding_id = _string(
            item["source_binding_id"], f"{evidence_context}.source_binding_id"
        )
        source_sha = _sha256(item["source_sha256"], f"{evidence_context}.source_sha256")
        binding = source_bindings.by_id.get(binding_id)
        _require(binding is not None, f"{evidence_context} cites an unknown binding ID")
        _require(
            binding["sha256"] == source_sha,
            f"{evidence_context} binding ID/hash pair differs",
        )
        artifact_kind = binding["artifact_kind"]
        if role == "direct_support":
            if source_kind == "primary_structure_record":
                _require(
                    artifact_kind == "primary_source",
                    f"{evidence_context} direct structure support must bind deposited source bytes",
                )
            else:
                _require(
                    source_kind == "primary_research_article"
                    and artifact_kind
                    in {"primary_source", "primary_source_projection"},
                    f"{evidence_context} article support must bind source bytes or an audited source projection",
                )
        elif role == "curated_identity_support":
            _require(
                source_kind == "curated_protein_record"
                and artifact_kind == "curated_reference",
                f"{evidence_context} curated identity support is not primary research evidence",
            )
        elif role == "source_record_only":
            _require(
                source_kind == "official_source_record"
                and artifact_kind == "source_record_snapshot"
                and source_sha == record["source"]["snapshot_sha256"],
                f"{evidence_context} source-record evidence differs from the bound draft snapshot",
            )
        else:
            _require(
                source_kind
                in {"official_structure_metadata", "curated_chemical_component_record"},
                f"{evidence_context} corroboration kind is unsupported",
            )
        evidence_by_id[evidence_id] = item
        ids_by_role[role].add(evidence_id)
        bindings_by_role[role].add(binding_id)

    partition_fields = {
        "direct_support": "direct_evidence_ids",
        "curated_identity_support": "curated_identity_evidence_ids",
        "source_record_only": "source_record_evidence_ids",
        "corroboration_only": "corroborating_evidence_ids",
    }
    for role, field in partition_fields.items():
        ids = _strings(claim[field], f"{context}.claim.{field}")
        _require(set(ids) == ids_by_role[role], f"{context}.claim.{field} differs")
    _require(ids_by_role["direct_support"], f"{context} lacks direct observed-state evidence")
    return evidence_by_id, ids_by_role, bindings_by_role


def _validate_observed_state_projection(
    projection_binding: dict[str, Any],
    projection_excerpt: dict[str, Any],
    *,
    record_binding: dict[str, Any],
    structure_context: dict[str, Any],
    observed_entity: dict[str, Any],
    structure_instances: list[dict[str, Any]],
    protein_attachments: list[dict[str, Any]] | None,
    site_crosswalk: dict[str, Any],
    chemical_observations: list[dict[str, Any]],
    chemical_reconciliation: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    ids_by_role: dict[str, set[str]],
    bindings_by_role: dict[str, set[str]],
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
    projection_id = _string(projection_binding["projection_id"], f"{context}.projection_id")
    context_id = _string(projection_binding["context_id"], f"{context}.context_id")
    excerpt = _exact(
        projection_excerpt,
        {"support_edges", "locators"},
        f"{context}.excerpt",
    )
    projection_path = source_bindings.resolved_paths.get(binding_id)
    projection_source_ids: list[str]
    if projection_path is None:
        projection = None
        projection_source_ids = list(source_bindings.by_id)
    else:
        projection_fields = {
            "schema_version",
            "projection_id",
            "context_id",
            "record_binding",
            "source_bindings",
            "structure_context",
            "observed_entity",
            "structure_instances",
            "site_crosswalk",
            "chemical_observations",
            "chemical_reconciliation",
            "support_edges",
            "locators",
            "limits",
        }
        if observed_entity["state_kind"] == "protein_ligand_covalent_adduct":
            projection_fields.add("protein_attachments")
        projection = _exact(
            json.loads(projection_path.read_text(encoding="utf-8")),
            projection_fields,
            f"{context} source",
        )
        _require(
            projection["schema_version"] == _OBSERVED_STATE_PROJECTION_SCHEMA_VERSION,
            f"{context} source schema is unsupported",
        )
        _require(projection["projection_id"] == projection_id, f"{context} ID differs")
        _require(projection["context_id"] == context_id, f"{context} context ID differs")
        _require(
            projection["record_binding"] == record_binding,
            f"{context} source record binding differs",
        )

        projection_sources = projection["source_bindings"]
        _require(
            isinstance(projection_sources, list) and projection_sources,
            f"{context} source bindings are incomplete",
        )
        projection_source_ids = []
        projection_source_paths: list[str] = []
        for index, raw_source in enumerate(projection_sources):
            source_context = f"{context} source.source_bindings[{index}]"
            source = _exact(raw_source, {"binding_id", "path", "sha256"}, source_context)
            source_id = _string(source["binding_id"], f"{source_context}.binding_id")
            path = _string(source["path"], f"{source_context}.path")
            _sha256(source["sha256"], f"{source_context}.sha256")
            _require(
                source_id not in projection_source_ids,
                f"{context} source binding repeats",
            )
            top_binding = source_bindings.by_id.get(source_id)
            _require(top_binding is not None, f"{context} source binding is not declared")
            _require(
                {key: top_binding[key] for key in ("path", "sha256")}
                == {key: source[key] for key in ("path", "sha256")},
                f"{context} source binding differs from its declaration",
            )
            projection_source_ids.append(source_id)
            projection_source_paths.append(path)
        _require(
            projection_source_paths == sorted(projection_source_paths),
            f"{context} source bindings are not ordered",
        )
    evidence_binding_ids = {
        evidence["source_binding_id"] for evidence in evidence_by_id.values()
    }
    _require(
        evidence_binding_ids <= set(projection_source_ids),
        f"{context} annotation evidence is absent from projection sources",
    )

    if projection is not None:
        projected_structure = _validate_observed_structure_context(
            projection["structure_context"], f"{context} source.structure_context"
        )
        projected_entity = _validate_observed_entity(
            projection["observed_entity"], f"{context} source.observed_entity"
        )
        projected_instances = _validate_structure_instances(
            projection["structure_instances"], f"{context} source.structure_instances"
        )
        if projected_entity["state_kind"] == "protein_ligand_covalent_adduct":
            projected_attachments = _validate_protein_attachments(
                projection["protein_attachments"],
                structure_context=projected_structure,
                structure_instances=projected_instances,
                context=f"{context} source.protein_attachments",
            )
        else:
            projected_attachments = None
        projected_crosswalk = _validate_site_crosswalk(
            projection["site_crosswalk"],
            structure_instances=projected_instances,
            context=f"{context} source.site_crosswalk",
        )
        projected_observations = _validate_chemical_observations(
            projection["chemical_observations"],
            observed_entity=projected_entity,
            context=f"{context} source.chemical_observations",
        )
        projected_reconciliation = _validate_chemical_reconciliation(
            projection["chemical_reconciliation"],
            observed_entity=projected_entity,
            context=f"{context} source.chemical_reconciliation",
        )
        _require(
            projected_structure == structure_context,
            f"{context} structure context differs",
        )
        _require(projected_entity == observed_entity, f"{context} observed entity differs")
        _require(projected_instances == structure_instances, f"{context} instances differ")
        _require(
            projected_attachments == protein_attachments,
            f"{context} protein attachments differ",
        )
        _require(projected_crosswalk == site_crosswalk, f"{context} site crosswalk differs")
        _require(
            projected_observations == chemical_observations,
            f"{context} chemical observations differ",
        )
        _require(
            projected_reconciliation == chemical_reconciliation,
            f"{context} chemical reconciliation differs",
        )
        _require(
            projection["support_edges"] == excerpt["support_edges"]
            and projection["locators"] == excerpt["locators"],
            f"{context} packaged projection excerpt differs",
        )

    raw_locators = excerpt["locators"]
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
        locator_source = _string(
            locator["source_binding_id"], f"{locator_context}.source_binding_id"
        )
        _require(
            locator_source in projection_source_ids,
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

    raw_edges = excerpt["support_edges"]
    _require(isinstance(raw_edges, list) and raw_edges, f"{context} source support edges are empty")
    edges: dict[str, dict[str, Any]] = {}
    structure_direct_bindings = {
        item["source_binding_id"]
        for item in evidence_by_id.values()
        if item["evidence_role"] == "direct_support"
        and item["source_kind"] == "primary_structure_record"
    }
    article_direct_bindings = {
        item["source_binding_id"]
        for item in evidence_by_id.values()
        if item["evidence_role"] == "direct_support"
        and item["source_kind"] == "primary_research_article"
    }
    expected_status = {
        "deposited_structure_state": "direct_structure_observation",
        "deposited_component_bond_order": "direct_structure_observation",
        "curated_canonical_site": "curated_identity_support",
        "cross_source_correspondence": "cross_source_curated_projection",
        "primary_article_analogue_designation": "source_designated_analogue",
        "primary_article_bound_adduct_description": "source_described_bound_adduct",
        "primary_article_bound_intermediate_description": "source_described_bound_intermediate",
        "deposited_state_description": "deposit_described_bound_intermediate",
        "deposited_covalent_connection": "direct_structure_observation",
        "deposited_component_dictionary_bond_order": "direct_structure_observation",
        "deposited_modeled_instance_atom_inventory": "direct_structure_observation",
        "deposited_connection_inventory": "absent_from_deposited_struct_conn",
        "curated_protein_identity": "curated_identity_support",
    }
    for index, raw_edge in enumerate(raw_edges):
        edge_context = f"{context} source.support_edges[{index}]"
        edge = _exact(
            raw_edge,
            {
                "edge_id",
                "edge_kind",
                "support_status",
                "source_binding_ids",
                "locator_ids",
                "extracted_values",
            },
            edge_context,
        )
        edge_id = _string(edge["edge_id"], f"{edge_context}.edge_id")
        _require(edge_id not in edges, f"{context} source repeats edge_id")
        edge_kind = edge["edge_kind"]
        _require(edge_kind in expected_status, f"{edge_context}.edge_kind is invalid")
        _require(
            edge["support_status"] == expected_status[edge_kind],
            f"{edge_context}.support_status is invalid",
        )
        edge_sources = _strings(
            edge["source_binding_ids"], f"{edge_context}.source_binding_ids", minimum=1
        )
        edge_locators = _strings(edge["locator_ids"], f"{edge_context}.locator_ids", minimum=1)
        _require(
            set(edge_sources) <= set(projection_source_ids),
            f"{edge_context} cites an undeclared source",
        )
        _require(
            set(edge_locators) <= set(locators),
            f"{edge_context} cites an unknown locator",
        )
        _require(
            {locators[locator_id]["source_binding_id"] for locator_id in edge_locators}
            <= set(edge_sources),
            f"{edge_context} locator/source bindings differ",
        )
        extracted = _object(edge["extracted_values"], f"{edge_context}.extracted_values")
        artifact_kinds = {
            source_bindings.by_id[source_id]["artifact_kind"] for source_id in edge_sources
        }
        if edge_kind in {
            "deposited_structure_state",
            "deposited_component_bond_order",
            "deposited_component_dictionary_bond_order",
            "deposited_modeled_instance_atom_inventory",
            "deposited_state_description",
            "deposited_covalent_connection",
            "deposited_connection_inventory",
        }:
            _require(
                artifact_kinds == {"primary_source"}
                and set(edge_sources) <= structure_direct_bindings,
                f"{edge_context} must use direct primary structure evidence",
            )
        elif edge_kind in {
            "primary_article_analogue_designation",
            "primary_article_bound_adduct_description",
            "primary_article_bound_intermediate_description",
        }:
            _require(
                len(artifact_kinds) == 1
                and artifact_kinds
                <= {"primary_source", "primary_source_projection"}
                and set(edge_sources) <= article_direct_bindings,
                f"{edge_context} requires direct primary-article evidence",
            )
        elif edge_kind in {"curated_canonical_site", "curated_protein_identity"}:
            _require(
                artifact_kinds == {"curated_reference"}
                and set(edge_sources) <= bindings_by_role["curated_identity_support"],
                f"{edge_context} must use curated identity evidence",
            )
        else:
            _require(
                artifact_kinds
                == {"primary_source", "curated_reference", "source_record_snapshot"},
                f"{edge_context} must preserve structure, curated, and source-record edges",
            )
            _require(
                any(source in bindings_by_role["direct_support"] for source in edge_sources)
                and any(source in bindings_by_role["curated_identity_support"] for source in edge_sources)
                and any(source in bindings_by_role["source_record_only"] for source in edge_sources),
                f"{edge_context} evidence roles are incomplete",
            )
        edge["extracted_values"] = extracted
        edges[edge_id] = edge

    expected_observation_edges = {
        "deposited_component_state": {"deposited_structure_state"},
        "deposited_component_bond_order": {"deposited_component_bond_order"},
        "deposited_component_dictionary_bond_order": {
            "deposited_component_dictionary_bond_order"
        },
        "deposited_modeled_instance_atom_inventory": {
            "deposited_modeled_instance_atom_inventory"
        },
        "deposited_state_description": {"deposited_state_description"},
        "primary_article_state_description": {
            "primary_article_analogue_designation"
            if observed_entity["chemical_context"] == "source_designated_analogue"
            else (
                "primary_article_bound_adduct_description"
                if observed_entity["chemical_context"] == "source_described_bound_adduct"
                else "primary_article_bound_intermediate_description"
            )
        },
    }
    for observation in chemical_observations:
        observation_context = (
            f"{context} chemical observation {observation['observation_id']}"
        )
        _require(
            set(observation["evidence_ids"]) <= set(evidence_by_id),
            f"{observation_context} cites unknown evidence",
        )
        evidence_rows = [evidence_by_id[item] for item in observation["evidence_ids"]]
        if observation["source_scope"] == "deposited_structure":
            _require(
                all(
                    item["evidence_role"] == "direct_support"
                    and item["source_kind"] == "primary_structure_record"
                    for item in evidence_rows
                ),
                f"{observation_context} must use direct deposited-structure evidence",
            )
        else:
            _require(
                all(
                    item["evidence_role"] == "direct_support"
                    and item["source_kind"] == "primary_research_article"
                    for item in evidence_rows
                ),
                f"{observation_context} must use direct primary-article evidence",
            )
        _require(
            set(observation["support_edge_ids"]) <= set(edges),
            f"{observation_context} cites unknown support edges",
        )
        observation_edges = [edges[item] for item in observation["support_edge_ids"]]
        _require(
            {item["edge_kind"] for item in observation_edges}
            == expected_observation_edges[observation["observation_kind"]],
            f"{observation_context} support-edge scope differs",
        )
        evidence_bindings = {
            item["source_binding_id"] for item in evidence_rows
        }
        _require(
            all(set(item["source_binding_ids"]) <= evidence_bindings for item in observation_edges),
            f"{observation_context} edge/evidence bindings differ",
        )

    bond_observations = [
        item
        for item in chemical_observations
        if item["observation_kind"] == "deposited_component_bond_order"
    ]
    if bond_observations:
        bond_edges = [
            edge
            for edge in edges.values()
            if edge["edge_kind"] == "deposited_component_bond_order"
        ]
        _require(len(bond_edges) == 1, f"{context} lacks one deposited bond-order edge")
        _require(
            bond_edges[0]["extracted_values"]
            == {
                "source_component_id": observed_entity["source_component_id"],
                "source_bond_order_code": bond_observations[0][
                    "source_bond_order_code"
                ],
                "source_description": bond_observations[0]["source_description"],
            },
            f"{context} deposited bond-order observation differs",
        )
        _require(
            any(
                locators[locator_id]["extracted_values"].get("component_id")
                == observed_entity["source_component_id"]
                and locators[locator_id]["extracted_values"].get("value_order")
                == bond_observations[0]["source_bond_order_code"]
                for locator_id in bond_edges[0]["locator_ids"]
            ),
            f"{context} deposited bond-order locator differs",
        )

    if observed_entity["state_kind"] == "protein_ligand_covalent_adduct":
        dictionary_observations = [
            item
            for item in chemical_observations
            if item["observation_kind"]
            == "deposited_component_dictionary_bond_order"
        ]
        inventory_observations = [
            item
            for item in chemical_observations
            if item["observation_kind"]
            == "deposited_modeled_instance_atom_inventory"
        ]
        description_observations = [
            item
            for item in chemical_observations
            if item["observation_kind"] == "deposited_state_description"
        ]
        _require(
            len(description_observations) == 1,
            f"{context} requires one deposit-description observation",
        )
        _require(
            len(dictionary_observations) == len(inventory_observations) <= 1,
            f"{context} dictionary and modeled-instance observations differ",
        )
        if (
            chemical_reconciliation["status"]
            == "unresolved_component_dictionary_vs_bound_instance_and_connection"
        ):
            _require(
                len(dictionary_observations) == 1,
                f"{context} unresolved dictionary/instance scope lacks both observations",
            )
        description_observation = description_observations[0]
        observation_expectations = {
            "deposited_state_description": {
                "source_component_id": observed_entity["source_component_id"],
                "chemical_context": "deposit_described_bound_intermediate",
                "source_description": description_observation["source_description"],
            },
        }
        if dictionary_observations:
            dictionary_observation = dictionary_observations[0]
            inventory_observation = inventory_observations[0]
            _require(
                inventory_observation["modeled_instance_indices"]
                == list(range(len(structure_instances))),
                f"{context} modeled-instance inventory does not cover every instance",
            )
            _require(
                set(dictionary_observation["source_atom_ids"])
                & set(inventory_observation["omitted_atom_ids"]),
                f"{context} does not identify the dictionary/instance atom-scope difference",
            )
            observation_expectations.update(
                {
                    "deposited_component_dictionary_bond_order": {
                        "source_component_id": observed_entity["source_component_id"],
                        "scope": "generic_component_dictionary",
                        "source_atom_ids": dictionary_observation["source_atom_ids"],
                        "source_bond_order_code": dictionary_observation[
                            "source_bond_order_code"
                        ],
                        "source_description": dictionary_observation[
                            "source_description"
                        ],
                    },
                    "deposited_modeled_instance_atom_inventory": {
                        "source_component_id": observed_entity["source_component_id"],
                        "scope": "modeled_deposited_instances",
                        "modeled_instance_indices": inventory_observation[
                            "modeled_instance_indices"
                        ],
                        "omitted_atom_ids": inventory_observation["omitted_atom_ids"],
                        "source_description": inventory_observation[
                            "source_description"
                        ],
                    },
                }
            )
        for edge_kind, expected_values in observation_expectations.items():
            matching_edges = [
                edge for edge in edges.values() if edge["edge_kind"] == edge_kind
            ]
            _require(
                len(matching_edges) == 1
                and matching_edges[0]["extracted_values"] == expected_values,
                f"{context} {edge_kind} edge differs",
            )
            _require(
                any(
                    locators[locator_id]["extracted_values"] == expected_values
                    for locator_id in matching_edges[0]["locator_ids"]
                ),
                f"{context} {edge_kind} locator differs",
            )

        _require(
            protein_attachments is not None,
            f"{context} lacks typed protein attachments",
        )
        connection_edges = {
            edge["edge_id"]: edge
            for edge in edges.values()
            if edge["edge_kind"] == "deposited_covalent_connection"
        }
        _require(
            set(connection_edges)
            == {
                attachment["support_edge_ids"][0]
                for attachment in protein_attachments
            },
            f"{context} connection edges do not cover attachments one-to-one",
        )
        for attachment in protein_attachments:
            edge = connection_edges[attachment["support_edge_ids"][0]]
            _require(
                edge["extracted_values"] == _attachment_edge_values(attachment),
                f"{context} connection edge differs from attachment",
            )
            _require(
                any(
                    locators[locator_id]["extracted_values"]
                    == _attachment_locator_values(attachment)
                    for locator_id in edge["locator_ids"]
                ),
                f"{context} connection locator differs from attachment",
            )
            _require(
                not inventory_observations
                or attachment["ligand_endpoint"]["atom_name"]
                not in inventory_observations[0]["omitted_atom_ids"],
                f"{context} connection uses an atom absent from modeled instances",
            )

    structure_edges = [
        edge for edge in edges.values() if edge["edge_kind"] == "deposited_structure_state"
    ]
    _require(len(structure_edges) == 1, f"{context} requires one deposited-state edge")
    _require(
        structure_edges[0]["extracted_values"]
        == {
            "entity_context": observed_entity["entity_context"],
            "entity_id": observed_entity["entity_id"],
            "source_component_id": observed_entity["source_component_id"],
            "source_description": observed_entity["source_description"],
            "structure_instances": structure_instances,
        },
        f"{context} deposited-state edge differs",
    )

    if site_crosswalk["status"] == "cross_source_curated_projection":
        _require(
            set(site_crosswalk["support_edge_ids"]) <= set(edges),
            f"{context} crosswalk cites an unknown support edge",
        )
        crosswalk_edges = [edges[edge_id] for edge_id in site_crosswalk["support_edge_ids"]]
        _require(
            {edge["support_status"] for edge in crosswalk_edges}
            == {
                "direct_structure_observation",
                "curated_identity_support",
                "cross_source_curated_projection",
            },
            f"{context} crosswalk edges do not decompose source support",
        )
        cross_edges = [
            edge for edge in crosswalk_edges if edge["edge_kind"] == "cross_source_correspondence"
        ]
        _require(len(cross_edges) == 1, f"{context} crosswalk lacks one correspondence edge")
        _require(
            cross_edges[0]["extracted_values"]
            == {
                "relationship": site_crosswalk["relationship"],
                "structure_instance_index": site_crosswalk["structure_instance_index"],
                "canonical_site": site_crosswalk["canonical_site"],
                "source_record_alias": site_crosswalk["source_record_alias"],
                "author_number_mapping_status": "not_asserted",
            },
            f"{context} cross-source correspondence differs",
        )

    if observed_entity["chemical_context"] == "source_designated_analogue":
        analogue_edges = [
            edge
            for edge in edges.values()
            if edge["edge_kind"] == "primary_article_analogue_designation"
        ]
        _require(len(analogue_edges) == 1, f"{context} lacks primary analogue designation")
        _require(
            analogue_edges[0]["extracted_values"]
            == {
                "source_component_id": observed_entity["source_component_id"],
                "chemical_context": "source_designated_analogue",
            },
            f"{context} analogue designation differs",
        )

    if observed_entity["chemical_context"] == "source_described_bound_adduct":
        description_edges = [
            edge
            for edge in edges.values()
            if edge["edge_kind"] == "primary_article_bound_adduct_description"
        ]
        _require(
            len(description_edges) == 1,
            f"{context} lacks primary bound-adduct description",
        )
        _require(
            description_edges[0]["extracted_values"]
            == {
                "source_component_id": observed_entity["source_component_id"],
                "chemical_context": "source_described_bound_adduct",
            },
            f"{context} bound-adduct description differs",
        )

    if observed_entity["chemical_context"] == "deposit_described_bound_intermediate":
        article_observations = [
            item
            for item in chemical_observations
            if item["observation_kind"] == "primary_article_state_description"
        ]
        article_edges = [
            edge
            for edge in edges.values()
            if edge["edge_kind"] == "primary_article_bound_intermediate_description"
        ]
        _require(
            len(article_edges) == len(article_observations),
            f"{context} primary-article descriptions and edges differ",
        )
        if article_observations:
            _require(
                len(article_observations) == 1
                and article_edges[0]["extracted_values"]
                == {
                    "source_component_id": observed_entity["source_component_id"],
                    "chemical_context": "source_described_bound_intermediate",
                    "source_description": article_observations[0]["source_description"],
                },
                f"{context} primary bound-intermediate description differs",
            )

    if observed_entity["attachment_context"] == "absent_from_deposited_struct_conn":
        connection_edges = [
            edge
            for edge in edges.values()
            if edge["edge_kind"] == "deposited_connection_inventory"
        ]
        _require(len(connection_edges) == 1, f"{context} lacks deposited connection inventory")
        connection_values = _exact(
            connection_edges[0]["extracted_values"],
            {
                "queried_component_id",
                "attachment_context",
                "struct_conn_row_count",
                "matching_component_row_count",
                "connected_component_ids",
            },
            f"{context} connection edge",
        )
        _require(
            connection_values["queried_component_id"]
            == observed_entity["source_component_id"]
            and connection_values["attachment_context"]
            == "absent_from_deposited_struct_conn"
            and type(connection_values["struct_conn_row_count"]) is int
            and connection_values["struct_conn_row_count"] >= 0
            and connection_values["matching_component_row_count"] == 0,
            f"{context} deposited connection inventory differs",
        )
        connected_components = _strings(
            connection_values["connected_component_ids"],
            f"{context} connection edge.connected_component_ids",
        )
        _require(
            observed_entity["source_component_id"] not in connected_components,
            f"{context} connection inventory contains the observed component",
        )
        _require(
            any(
                all(
                    locators[locator_id]["extracted_values"].get(field)
                    == connection_values[field]
                    for field in (
                        "struct_conn_row_count",
                        "matching_component_row_count",
                        "connected_component_ids",
                    )
                )
                for locator_id in connection_edges[0]["locator_ids"]
            ),
            f"{context} deposited connection locator differs",
        )

    if projection is not None:
        _strings(projection["limits"], f"{context} source.limits", minimum=1)


def _validate_observed_state_context_annotation(
    raw_annotation: Any,
    *,
    record_by_id: dict[str, dict[str, Any]],
    source_bindings: _SourceBindings,
    context: str,
) -> tuple[str, str]:
    annotation = _exact(raw_annotation, _OBSERVED_STATE_CONTEXT_ANNOTATION_FIELDS, context)
    annotation_id = _string(annotation["annotation_id"], f"{context}.annotation_id")
    _require(
        annotation["annotation_kind"] == "primary_observed_state_context",
        f"{context}.annotation_kind is unsupported",
    )
    _require(
        annotation["target_scope"] == "record_only",
        f"{context} cannot target a proposal or source step",
    )
    record_id, record = _bound_record(
        annotation["record_binding"],
        record_by_id=record_by_id,
        context=f"{context}.record_binding",
    )
    projection_binding = _exact(
        annotation["projection_binding"],
        {"binding_id", "projection_id", "context_id"},
        f"{context}.projection_binding",
    )
    raw_claim = _object(annotation["claim"], f"{context}.claim")
    claim_fields = {
        "statement",
        "structure_context",
        "observed_entity",
        "structure_instances",
        "site_crosswalk",
        "chemical_observations",
        "chemical_reconciliation",
        "direct_evidence_ids",
        "curated_identity_evidence_ids",
        "source_record_evidence_ids",
        "corroborating_evidence_ids",
        "observed_state_grounds_step",
    }
    raw_entity = raw_claim.get("observed_entity")
    if (
        isinstance(raw_entity, dict)
        and raw_entity.get("state_kind") == "protein_ligand_covalent_adduct"
    ):
        claim_fields.add("protein_attachments")
    claim = _exact(raw_claim, claim_fields, f"{context}.claim")
    _string(claim["statement"], f"{context}.claim.statement")
    _require(
        claim["observed_state_grounds_step"] is False,
        f"{context} record-level observed state cannot ground a source step",
    )
    structure_context = _validate_observed_structure_context(
        claim["structure_context"], f"{context}.claim.structure_context"
    )
    observed_entity = _validate_observed_entity(
        claim["observed_entity"], f"{context}.claim.observed_entity"
    )
    instances = _validate_structure_instances(
        claim["structure_instances"], f"{context}.claim.structure_instances"
    )
    _require(
        all(instance["label_entity_id"] == observed_entity["entity_id"] for instance in instances),
        f"{context} instance/entity identity differs",
    )
    _require(
        all(
            instance["label_component_id"] == observed_entity["source_component_id"]
            for instance in instances
        ),
        f"{context} instance/component identity differs",
    )
    _require(
        all(
            instance["atom_author_chain_id"]
            in structure_context["protein_author_chain_ids"]
            for instance in instances
        ),
        f"{context} instance/protein author-chain context differs",
    )
    if observed_entity["entity_context"] == "polymer_component":
        _require(
            all(
                instance["label_seq_id"] is not None
                and instance["label_asym_id"]
                in structure_context["protein_label_asym_ids"]
                for instance in instances
            ),
            f"{context} polymer component lacks a label sequence position",
        )
    else:
        _require(
            all(instance["label_seq_id"] is None for instance in instances),
            f"{context} nonpolymer component must preserve null label sequence IDs",
        )
    if observed_entity["state_kind"] == "protein_ligand_covalent_adduct":
        protein_attachments = _validate_protein_attachments(
            claim["protein_attachments"],
            structure_context=structure_context,
            structure_instances=instances,
            context=f"{context}.claim.protein_attachments",
        )
    else:
        protein_attachments = None
    site_crosswalk = _validate_site_crosswalk(
        claim["site_crosswalk"],
        structure_instances=instances,
        context=f"{context}.claim.site_crosswalk",
    )
    chemical_observations = _validate_chemical_observations(
        claim["chemical_observations"],
        observed_entity=observed_entity,
        context=f"{context}.claim.chemical_observations",
    )
    chemical_reconciliation = _validate_chemical_reconciliation(
        claim["chemical_reconciliation"],
        observed_entity=observed_entity,
        context=f"{context}.claim.chemical_reconciliation",
    )
    _validate_crosswalk_against_source_record(
        site_crosswalk,
        record=record,
        context=f"{context}.claim.site_crosswalk",
    )
    if site_crosswalk["status"] == "cross_source_curated_projection":
        _require(
            structure_context["curated_protein_accession"]
            == site_crosswalk["canonical_site"]["accession"],
            f"{context} structure/canonical accession differs",
        )
        _require(
            structure_context["pdb_id"]
            == site_crosswalk["source_record_alias"]["pdb_id"],
            f"{context} structure/source-alias PDB identity differs",
        )
    if observed_entity["state_kind"] == "protein_ligand_covalent_adduct":
        _require(
            site_crosswalk["status"] == "not_asserted",
            f"{context} ligand site crosswalk cannot encode a protein attachment mapping",
        )
    evidence_by_id, ids_by_role, bindings_by_role = _validate_observed_context_evidence(
        annotation["evidence"],
        claim=claim,
        record=record,
        source_bindings=source_bindings,
        context=context,
    )
    structure_evidence = [
        item
        for item in evidence_by_id.values()
        if item["source_kind"] == "primary_structure_record"
        and item["evidence_role"] == "direct_support"
    ]
    _require(
        len(structure_evidence) == 1
        and structure_evidence[0]["source_id"]
        == f"RCSB PDB:{structure_context['pdb_id']}",
        f"{context} lacks exact direct primary-structure evidence",
    )
    if observed_entity["chemical_context"] in {
        "source_designated_analogue",
        "source_described_bound_adduct",
    }:
        _require(
            any(
                item["source_kind"] == "primary_research_article"
                and item["evidence_role"] == "direct_support"
                for item in evidence_by_id.values()
            ),
            f"{context} source-described chemical context lacks direct primary-article evidence",
        )
    if structure_context["curated_protein_accession"] is not None:
        _require(
            any(
                item["evidence_role"] == "curated_identity_support"
                and item["source_id"]
                == f"UniProtKB:{structure_context['curated_protein_accession']}"
                for item in evidence_by_id.values()
            ),
            f"{context} curated protein identity lacks curated evidence",
        )
    if site_crosswalk["status"] == "cross_source_curated_projection":
        _require(
            ids_by_role["curated_identity_support"]
            and any(
                item["evidence_role"] == "source_record_only"
                and item["source_id"] == f"M-CSA:{record['mcsa_id']}"
                and item["uri"] == record["source"]["uri"]
                for item in evidence_by_id.values()
            ),
            f"{context} cross-source mapping lacks curated or source-record evidence",
        )
    _validate_observed_state_projection(
        projection_binding,
        annotation["projection_excerpt"],
        record_binding=annotation["record_binding"],
        structure_context=structure_context,
        observed_entity=observed_entity,
        structure_instances=instances,
        protein_attachments=protein_attachments,
        site_crosswalk=site_crosswalk,
        chemical_observations=chemical_observations,
        chemical_reconciliation=chemical_reconciliation,
        evidence_by_id=evidence_by_id,
        ids_by_role=ids_by_role,
        bindings_by_role=bindings_by_role,
        source_bindings=source_bindings,
        context=f"{context}.projection_binding",
    )
    required_limits = dict(_OBSERVED_STATE_REQUIRED_LIMITS)
    if observed_entity["state_kind"] == "protein_ligand_covalent_adduct":
        required_limits["bound_moiety_bond_order"] = "abstained"
        if (
            chemical_reconciliation["status"]
            == "unresolved_component_dictionary_vs_bound_instance_and_connection"
        ):
            required_limits["component_dictionary_vs_modeled_instance"] = "abstained"
    _validate_limits_and_scope(
        annotation,
        context,
        required_limits=required_limits,
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
        schema_version
        in {
            PRIMARY_EVIDENCE_SCHEMA_V1,
            PRIMARY_EVIDENCE_SCHEMA_V2,
            PRIMARY_EVIDENCE_SCHEMA_VERSION,
        },
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
            schema_version in {PRIMARY_EVIDENCE_SCHEMA_V2, PRIMARY_EVIDENCE_SCHEMA_VERSION}
            and annotation_object.get("annotation_kind")
            == "source_proposal_protein_context"
        ):
            annotation_id, record_id = _validate_proposal_context_annotation(
                raw_annotation,
                record_by_id=record_by_id,
                source_bindings=source_bindings,
                context=annotation_context,
            )
        elif (
            schema_version == PRIMARY_EVIDENCE_SCHEMA_VERSION
            and annotation_object.get("annotation_kind")
            == "primary_observed_state_context"
        ):
            annotation_id, record_id = _validate_observed_state_context_annotation(
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
