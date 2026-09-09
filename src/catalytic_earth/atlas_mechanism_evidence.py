"""Reviewed retrospective evidence for one bounded mechanistic conclusion.

This overlay binds published observations to immutable Atlas transformations
and site context.  It does not modify those inputs, infer a conclusion from
measurements, or turn retrospective source evidence into a new experiment.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import re
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any

from .atlas_transformation_query import normalize_mcsa_id, query_transformation_sets
from .atlas_transformation_sites import query_transformation_sites


SCHEMA_VERSION = "catalytic-earth.mechanism-evidence.v1"
QUERY_SCHEMA_VERSION = "catalytic-earth.mechanism-evidence-query.v1"
STATUS = "reviewed_retrospective_mechanistic_conclusion_not_upstream_revision"
REVIEW_UPDATE_RULE = (
    "Do not automatically refresh this pin after mechanistic-evidence changes. "
    "Repeat source-to-conclusion review first."
)

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_SITE_RE = re.compile(r"^([A-Z0-9]{6,10}):([A-Z])([1-9][0-9]*)$")
_VARIANT_RE = re.compile(r"^(?:WT|[A-Z][1-9][0-9]*[A-Z])$")
_SUBSTITUTION_VARIANT_RE = re.compile(r"^([A-Z])([1-9][0-9]*)([A-Z])$")
_TOP_FIELDS = {
    "schema_version", "evidence_set_id", "status", "source_bindings", "cases", "review",
}
_BINDING_FIELDS = {"binding_id", "artifact_kind", "path", "sha256"}
_CASE_FIELDS = {
    "case_id", "focal_variant_id", "record_binding", "proposal_binding", "transformation_binding",
    "site_context_binding", "question", "evidence_references", "alternatives",
    "observations", "discriminants", "adjudication", "applicability",
    "mandatory_abstentions", "scope_effect",
}
_RECORD_FIELDS = {"case_id", "mcsa_id", "record_id", "source_snapshot_sha256"}
_PROPOSAL_FIELDS = {"proposal_id", "source_mechanism_id"}
_TRANSFORMATION_FIELDS = {
    "mcsa_id", "transformation_set_id", "transformation_payload_sha256",
    "transformation_id",
}
_SITE_CONTEXT_FIELDS = {
    "atlas10_bundle_sha256", "site_id", "relationship",
    "changed_source_atom_link_status", "deposited_atom_identity_status",
    "assayed_construct_identity_status",
}
_QUESTION_FIELDS = {"question_id", "statement"}
_EVIDENCE_FIELDS = {
    "evidence_id", "source_binding_id", "source_id", "source_record_id",
    "evidence_kind", "applicability", "source_completeness",
}
_ALTERNATIVE_FIELDS = {"alternative_id", "statement"}
_OBSERVATION_FIELDS = {
    "observation_id", "evidence_ids", "variant", "substrate", "endpoint",
    "conditions", "result", "comparator_variant_id", "source_witnesses",
    "source_interpretation", "project_interpretation",
}
_VARIANT_FIELDS = {"uniprot_id", "variant_id", "substitutions"}
_SUBSTITUTION_FIELDS = {
    "wild_type_residue", "sequence_position", "mutant_residue",
}
_SUBSTRATE_FIELDS = {"name", "identifier", "enantiomer"}
_ENDPOINT_FIELDS = {"kind", "name", "net_direction"}
_CONDITION_FIELDS = {"condition_id", "name", "value", "unit"}
_RESULT_FIELDS = {
    "result_class", "value", "unit", "reported_relation", "detection_limit",
    "detection_limit_unit",
}
_WITNESS_FIELDS = {"evidence_id", "locator", "exact_text"}
_INTERPRETATION_FIELDS = {"status", "statement"}
_DISCRIMINANT_FIELDS = {
    "discriminant_id", "status", "observation_ids", "alternative_assessments",
}
_ASSESSMENT_FIELDS = {"alternative_id", "relation", "statement"}
_ADJUDICATION_FIELDS = {
    "claim_status", "selected_alternative_id", "statement",
    "basis_discriminant_ids", "unresolved_alternative_ids",
}
_APPLICABILITY_FIELDS = {
    "uniprot_id", "mcsa_id", "observation_ids", "scope", "other_proteins",
    "other_variants", "unreported_conditions",
}
_ABSTENTION_FIELDS = {"abstention_id", "reason"}
_SCOPE_FIELDS = {
    "atlas10_records_changed", "reviewed_transformations_changed",
    "transformation_review_scope_expanded", "changed_atom_site_link_added",
    "physical_atom_map_added", "deposited_atom_identity_added",
    "observed_intermediate_claimed", "complete_mechanism_validated",
    "prospective_prediction_claimed", "new_experiment_claimed",
    "independent_review_claimed", "statistical_confidence_claimed",
    "tier4_outcome_claimed",
}
_REVIEW_FIELDS = {
    "reviewed_on", "evidence_payload_sha256", "update_rule", "reviewer_kind",
    "same_model_agents", "blind_review", "statistically_independent",
    "correlated_error_risk", "human_reviewers", "domain_expert_review_claimed",
}
_ARTIFACT_KINDS = {
    "primary_source_projection", "acquisition_receipts", "source_inventory", "attribution",
}
_ENDPOINT_KINDS = {"turnover", "isotope_exchange", "structure"}
_RESULT_CLASSES = {
    "measured", "qualitative_detected", "not_detected", "no_detectable_difference",
}
_REPORTED_RELATIONS = {
    "fold_lower_than_wild_type",
    "fold_reduction_reference_unspecified_in_inspected_abstract",
}
_REQUIRED_ABSTENTIONS = {
    "abstract-depth",
    "conditions-and-nondetection",
    "timing-and-intermediate",
    "protein-construct-identity",
    "structure-applicability",
    "source-atom-correspondence",
    "review-scope",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    _require(isinstance(value, list) and (not nonempty or bool(value)), f"{label} must be a{' nonempty' if nonempty else 'n'} array")
    return value


def _exact(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    item = _object(value, label)
    actual = set(item)
    _require(
        actual == fields,
        f"{label} fields differ; missing={sorted(fields - actual)}, extra={sorted(actual - fields)}",
    )
    return item


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")
    return value


def _optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _string(value, label)


def _sha(value: Any, label: str) -> str:
    _require(isinstance(value, str) and _SHA_RE.fullmatch(value) is not None, f"{label} must be a lowercase SHA-256")
    return value


def _strings(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    rows = _array(value, label, nonempty=nonempty)
    _require(all(isinstance(row, str) and bool(row.strip()) for row in rows), f"{label} must contain nonempty strings")
    _require(len(rows) == len(set(rows)), f"{label} contains duplicates")
    return rows


def _number(value: Any, label: str) -> int | float:
    _require(type(value) in {int, float} and math.isfinite(value), f"{label} must be a finite number")
    return value


def _canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("mechanistic-evidence value must be canonical JSON data") from exc


def canonical_mechanism_evidence_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every declaration except the manually maintained review block."""
    _require(isinstance(value, dict), "mechanistic evidence must be an object")
    return hashlib.sha256(_canonical_json({key: item for key, item in value.items() if key != "review"})).hexdigest()


def _validate_bindings(value: Any) -> dict[str, dict[str, Any]]:
    rows = _array(value, "source_bindings", nonempty=True)
    by_id: dict[str, dict[str, Any]] = {}
    paths: set[str] = set()
    for index, raw in enumerate(rows):
        label = f"source_bindings[{index}]"
        row = _exact(raw, _BINDING_FIELDS, label)
        binding_id = _string(row["binding_id"], f"{label}.binding_id")
        _require(binding_id not in by_id, "source binding IDs repeat")
        _require(row["artifact_kind"] in _ARTIFACT_KINDS, f"{label}.artifact_kind is unsupported")
        path = _string(row["path"], f"{label}.path")
        posix = PurePosixPath(path)
        windows = PureWindowsPath(path)
        _require(
            "\\" not in path and not posix.is_absolute() and not windows.is_absolute()
            and not windows.drive and path == posix.as_posix() and ".." not in posix.parts,
            f"{label}.path must be a safe repository-relative POSIX path",
        )
        _require(path not in paths, "source binding paths repeat")
        paths.add(path)
        _sha(row["sha256"], f"{label}.sha256")
        by_id[binding_id] = row
    _require(any(row["artifact_kind"] == "primary_source_projection" for row in rows), "primary source projections are missing")
    _require(any(row["artifact_kind"] == "acquisition_receipts" for row in rows), "acquisition receipts are missing")
    return by_id


def _validate_review(value: Any, payload_sha: str) -> dict[str, Any]:
    review = _exact(value, _REVIEW_FIELDS, "review")
    reviewed_on = _string(review["reviewed_on"], "review.reviewed_on")
    try:
        dt.date.fromisoformat(reviewed_on)
    except ValueError as exc:
        raise ValueError("review.reviewed_on must be an ISO calendar date") from exc
    _require(review["evidence_payload_sha256"] == payload_sha, "reviewed mechanistic-evidence payload changed")
    _require(review["update_rule"] == REVIEW_UPDATE_RULE, "review update rule differs")
    _require(
        review["reviewer_kind"] == "same_model_computational_agents"
        and review["same_model_agents"] is True
        and review["blind_review"] is False
        and review["statistically_independent"] is False
        and review["correlated_error_risk"] is True
        and type(review["human_reviewers"]) is int
        and review["human_reviewers"] == 0
        and review["domain_expert_review_claimed"] is False,
        "review disclosure differs from the same-model non-independent review",
    )
    return review


def _validate_variant(value: Any, label: str) -> dict[str, Any]:
    row = _exact(value, _VARIANT_FIELDS, label)
    _string(row["uniprot_id"], f"{label}.uniprot_id")
    variant_id = _string(row["variant_id"], f"{label}.variant_id")
    _require(_VARIANT_RE.fullmatch(variant_id) is not None, f"{label}.variant_id is unsupported")
    substitutions = _array(row["substitutions"], f"{label}.substitutions")
    signatures: list[str] = []
    for index, raw in enumerate(substitutions):
        item_label = f"{label}.substitutions[{index}]"
        item = _exact(raw, _SUBSTITUTION_FIELDS, item_label)
        before = _string(item["wild_type_residue"], f"{item_label}.wild_type_residue")
        after = _string(item["mutant_residue"], f"{item_label}.mutant_residue")
        _require(len(before) == len(after) == 1 and before.isupper() and after.isupper(), f"{item_label} residues must be one-letter uppercase codes")
        position = item["sequence_position"]
        _require(type(position) is int and position > 0, f"{item_label}.sequence_position must be positive")
        signatures.append(f"{before}{position}{after}")
    _require(len(signatures) == len(set(signatures)), f"{label}.substitutions repeat")
    _require(
        (variant_id == "WT" and not signatures)
        or (variant_id != "WT" and signatures == [variant_id]),
        f"{label}.variant_id differs from its substitution",
    )
    return row


def _validate_result(value: Any, label: str) -> None:
    row = _exact(value, _RESULT_FIELDS, label)
    result_class = row["result_class"]
    _require(result_class in _RESULT_CLASSES, f"{label}.result_class is unsupported")
    numeric = row["value"]
    if numeric is not None:
        _number(numeric, f"{label}.value")
    unit = _optional_string(row["unit"], f"{label}.unit")
    relation = _optional_string(row["reported_relation"], f"{label}.reported_relation")
    limit = row["detection_limit"]
    if limit is not None:
        _number(limit, f"{label}.detection_limit")
    limit_unit = _optional_string(row["detection_limit_unit"], f"{label}.detection_limit_unit")
    _require((limit is None) == (limit_unit is None), f"{label} detection-limit value/unit must both be present or absent")
    if result_class == "measured":
        _require(numeric is not None and unit is not None and relation is not None, f"{label} measured result is incomplete")
        _require(relation in _REPORTED_RELATIONS, f"{label}.reported_relation is unsupported")
        _require(unit == "fold", f"{label} fold comparison must use the literal fold unit")
        _require(limit is None, f"{label} measured result cannot also be censored")
    else:
        _require(numeric is None and unit is None, f"{label} qualitative or censored result cannot carry a numeric value")
        _require(relation is None, f"{label} qualitative or censored result cannot carry a measured relation")
    if result_class != "not_detected":
        _require(limit is None, f"{label} only nondetection may carry a detection limit")


def _validate_observation(
    value: Any, label: str, evidence_ids: set[str], uniprot_id: str,
) -> dict[str, Any]:
    row = _exact(value, _OBSERVATION_FIELDS, label)
    _string(row["observation_id"], f"{label}.observation_id")
    refs = _strings(row["evidence_ids"], f"{label}.evidence_ids", nonempty=True)
    _require(set(refs) <= evidence_ids, f"{label}.evidence_ids do not resolve")
    variant = _validate_variant(row["variant"], f"{label}.variant")
    _require(variant["uniprot_id"] == uniprot_id, f"{label} protein differs from applicability")

    substrate = _exact(row["substrate"], _SUBSTRATE_FIELDS, f"{label}.substrate")
    endpoint = _exact(row["endpoint"], _ENDPOINT_FIELDS, f"{label}.endpoint")
    kind = endpoint["kind"]
    _require(kind in _ENDPOINT_KINDS, f"{label}.endpoint.kind is unsupported")
    _string(endpoint["name"], f"{label}.endpoint.name")
    _require(endpoint["net_direction"] in {None, "R_to_S", "S_to_R"}, f"{label}.endpoint.net_direction is unsupported")
    _require(kind == "turnover" or endpoint["net_direction"] is None, f"{label} non-turnover endpoint cannot assert net direction")
    if kind == "structure":
        _require(all(substrate[field] is None for field in _SUBSTRATE_FIELDS), f"{label} structure observation cannot imply a substrate complex")
    else:
        _string(substrate["name"], f"{label}.substrate.name")
        _optional_string(substrate["identifier"], f"{label}.substrate.identifier")
        _require(substrate["enantiomer"] in {None, "R", "S"}, f"{label}.substrate.enantiomer is unsupported")

    conditions = _array(row["conditions"], f"{label}.conditions")
    condition_ids: set[str] = set()
    for index, raw in enumerate(conditions):
        item_label = f"{label}.conditions[{index}]"
        item = _exact(raw, _CONDITION_FIELDS, item_label)
        condition_id = _string(item["condition_id"], f"{item_label}.condition_id")
        _require(condition_id not in condition_ids, f"{label}.condition IDs repeat")
        condition_ids.add(condition_id)
        _string(item["name"], f"{item_label}.name")
        _require(
            (isinstance(item["value"], str) and bool(item["value"].strip()))
            or (type(item["value"]) in {int, float} and math.isfinite(item["value"])),
            f"{item_label}.value must be nonempty text or a finite number",
        )
        _optional_string(item["unit"], f"{item_label}.unit")
    _validate_result(row["result"], f"{label}.result")
    comparator = row["comparator_variant_id"]
    if comparator is not None:
        _require(isinstance(comparator, str) and _VARIANT_RE.fullmatch(comparator) is not None, f"{label}.comparator_variant_id is unsupported")
    relation = row["result"]["reported_relation"]
    _require(
        (relation == "fold_lower_than_wild_type" and comparator == "WT")
        or (
            relation == "fold_reduction_reference_unspecified_in_inspected_abstract"
            and comparator is None
        )
        or relation is None,
        f"{label} comparator differs from the reported relation",
    )

    witnesses = _array(row["source_witnesses"], f"{label}.source_witnesses", nonempty=True)
    witness_keys: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(witnesses):
        item_label = f"{label}.source_witnesses[{index}]"
        item = _exact(raw, _WITNESS_FIELDS, item_label)
        _require(item["evidence_id"] in refs, f"{item_label}.evidence_id is outside the observation")
        key = (
            item["evidence_id"], _string(item["locator"], f"{item_label}.locator"),
            _string(item["exact_text"], f"{item_label}.exact_text"),
        )
        _require(key not in witness_keys, f"{label}.source_witnesses repeat")
        witness_keys.add(key)
    source_interpretation = row["source_interpretation"]
    if source_interpretation is not None:
        source_interpretation = _exact(source_interpretation, _INTERPRETATION_FIELDS, f"{label}.source_interpretation")
        _require(source_interpretation["status"] == "source_interpretation", f"{label}.source_interpretation status differs")
        _string(source_interpretation["statement"], f"{label}.source_interpretation.statement")
    project = _exact(row["project_interpretation"], _INTERPRETATION_FIELDS, f"{label}.project_interpretation")
    _require(project["status"] == "project_diagnostic", f"{label}.project_interpretation status differs")
    _string(project["statement"], f"{label}.project_interpretation.statement")
    return row


def _validate_upstream(
    case: dict[str, Any], atlas10_bundle: dict[str, Any], transformation_values: dict[str, dict[str, Any]],
    set_query: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    record = _exact(case["record_binding"], _RECORD_FIELDS, "record_binding")
    proposal = _exact(case["proposal_binding"], _PROPOSAL_FIELDS, "proposal_binding")
    binding = _exact(case["transformation_binding"], _TRANSFORMATION_FIELDS, "transformation_binding")
    mcsa_id = normalize_mcsa_id(record["mcsa_id"])
    _require(mcsa_id == record["mcsa_id"] == binding["mcsa_id"], "record/transformation M-CSA identifiers differ")
    _sha(record["source_snapshot_sha256"], "record_binding.source_snapshot_sha256")
    _sha(binding["transformation_payload_sha256"], "transformation_binding.transformation_payload_sha256")
    _require(type(proposal["source_mechanism_id"]) is int and proposal["source_mechanism_id"] > 0, "proposal source mechanism ID must be positive")
    selected_sets = [item["result"] for item in set_query["sets"] if item["mcsa_id"] == mcsa_id]
    _require(len(selected_sets) == 1, "conclusion does not select one reviewed transformation set")
    result = selected_sets[0]
    _require(
        result["transformation_set_id"] == binding["transformation_set_id"]
        and result["transformation_payload_sha256"] == binding["transformation_payload_sha256"],
        "transformation binding differs from the reviewed set",
    )
    rows = [row for row in result["transformations"] if row["transformation_id"] == binding["transformation_id"]]
    _require(len(rows) == 1, "conclusion does not select one reviewed transformation")
    transformation = rows[0]
    _require(transformation["record_binding"] == record, "conclusion record binding differs from transformation")
    _require(transformation["proposal_binding"] == proposal, "conclusion proposal binding differs from transformation")

    site = _exact(case["site_context_binding"], _SITE_CONTEXT_FIELDS, "site_context_binding")
    _sha(site["atlas10_bundle_sha256"], "site_context_binding.atlas10_bundle_sha256")
    _require(_SITE_RE.fullmatch(site["site_id"]) is not None, "site_context_binding.site_id is invalid")
    _require(
        site["relationship"] == "before_step_declared_catalyst_site"
        and site["changed_source_atom_link_status"] == "unresolved_no_explicit_source_residue_label"
        and site["deposited_atom_identity_status"] == "not_asserted",
        "site context exceeds the allowed residue-level relationship",
    )
    _require(
        site["assayed_construct_identity_status"]
        == "reference_protein_context_not_exact_assayed_construct",
        "site context falsely asserts exact assayed-construct identity",
    )
    site_query = query_transformation_sites(
        {mcsa_id: transformation_values[mcsa_id]}, atlas10_bundle=atlas10_bundle, mcsa_id=mcsa_id,
    )
    _require(site_query["query_semantics"]["atlas10_bundle_sha256"] == site["atlas10_bundle_sha256"], "Atlas10 site-context hash differs")
    site_matches = [
        item for item in site_query["matches"]
        if item["transformation"]["transformation_id"] == binding["transformation_id"]
    ]
    _require(len(site_matches) == 1, "site context does not select one transformation")
    site_match = site_matches[0]
    _require(site["site_id"] in site_match["before_step"]["catalyst_site_ids"], "site is not a declared catalyst for the transformation's before step")
    site_records = [row for row in site_match["bound_atlas10_record"]["sites"] if row["site_id"] == site["site_id"]]
    _require(len(site_records) == 1, "declared catalyst site is not unique in Atlas10")
    _require(
        not any(
            atom["source_record_residue_mapping"].get("site_id") == site["site_id"]
            for atom in site_match["changed_source_atoms"]
        ),
        "site context falsely preserves an unresolved changed-atom link",
    )
    return transformation, site_records[0]


def _validate_case(
    value: Any, bindings: dict[str, dict[str, Any]], atlas10_bundle: dict[str, Any],
    transformation_values: dict[str, dict[str, Any]], set_query: dict[str, Any],
) -> tuple[str, int]:
    case = _exact(value, _CASE_FIELDS, "case")
    case_id = _string(case["case_id"], "case.case_id")
    focal_variant_id = _string(case["focal_variant_id"], "case.focal_variant_id")
    focal_signature = _SUBSTITUTION_VARIANT_RE.fullmatch(focal_variant_id)
    _require(focal_signature is not None, "case.focal_variant_id must be one exact substitution")
    transformation, site_record = _validate_upstream(case, atlas10_bundle, transformation_values, set_query)
    _require(case_id == transformation["record_binding"]["case_id"], "case ID differs from the reviewed transformation")
    question = _exact(case["question"], _QUESTION_FIELDS, "question")
    _string(question["question_id"], "question.question_id")
    _string(question["statement"], "question.statement")

    evidence_rows = _array(case["evidence_references"], "evidence_references", nonempty=True)
    evidence_ids: set[str] = set()
    evidence_applicability: dict[str, str] = {}
    evidence_binding_ids: set[str] = set()
    for index, raw in enumerate(evidence_rows):
        label = f"evidence_references[{index}]"
        row = _exact(raw, _EVIDENCE_FIELDS, label)
        evidence_id = _string(row["evidence_id"], f"{label}.evidence_id")
        _require(evidence_id not in evidence_ids, "evidence reference IDs repeat")
        evidence_ids.add(evidence_id)
        binding_id = _string(row["source_binding_id"], f"{label}.source_binding_id")
        _require(binding_id in bindings and bindings[binding_id]["artifact_kind"] == "primary_source_projection", f"{label} does not bind a primary source projection")
        evidence_binding_ids.add(binding_id)
        for field in ("source_id", "source_record_id"):
            _string(row[field], f"{label}.{field}")
        _require(row["evidence_kind"] == "primary_paper_abstract", f"{label}.evidence_kind is unsupported")
        _require(row["applicability"] in {"direct", "contextual"}, f"{label}.applicability is unsupported")
        _require(row["source_completeness"] == "abstract_truncated", f"{label}.source_completeness differs from the retained source")
        evidence_applicability[evidence_id] = row["applicability"]
    primary_binding_ids = {
        binding_id for binding_id, row in bindings.items()
        if row["artifact_kind"] == "primary_source_projection"
    }
    _require(evidence_binding_ids == primary_binding_ids, "primary source projections must each have one or more evidence references")

    alternatives = _array(case["alternatives"], "alternatives", nonempty=True)
    _require(len(alternatives) >= 2, "a mechanistic conclusion requires at least two alternatives")
    alternative_ids: set[str] = set()
    for index, raw in enumerate(alternatives):
        label = f"alternatives[{index}]"
        row = _exact(raw, _ALTERNATIVE_FIELDS, label)
        alternative_id = _string(row["alternative_id"], f"{label}.alternative_id")
        _require(alternative_id not in alternative_ids, "alternative IDs repeat")
        alternative_ids.add(alternative_id)
        _string(row["statement"], f"{label}.statement")

    applicability = _exact(case["applicability"], _APPLICABILITY_FIELDS, "applicability")
    uniprot_id = _string(applicability["uniprot_id"], "applicability.uniprot_id")
    _require(site_record["uniprot_id"] == uniprot_id, "applicability protein differs from the site context")
    _require(applicability["mcsa_id"] == transformation["record_binding"]["mcsa_id"], "applicability M-CSA record differs")
    _string(applicability["scope"], "applicability.scope")
    _require(
        applicability["other_proteins"] is False
        and applicability["other_variants"] is False
        and applicability["unreported_conditions"] is False,
        "applicability cannot transfer beyond reported source scope",
    )

    observations = _array(case["observations"], "observations", nonempty=True)
    observation_ids: set[str] = set()
    observation_by_id: dict[str, dict[str, Any]] = {}
    focal_observation_count = 0
    used_evidence_ids: set[str] = set()
    for index, raw in enumerate(observations):
        row = _validate_observation(raw, f"observations[{index}]", evidence_ids, uniprot_id)
        observation_id = row["observation_id"]
        _require(observation_id not in observation_ids, "observation IDs repeat")
        observation_ids.add(observation_id)
        observation_by_id[observation_id] = row
        used_evidence_ids.update(row["evidence_ids"])
        if row["variant"]["variant_id"] == focal_variant_id:
            focal_observation_count += 1
            _require(
                any(evidence_applicability[item] == "direct" for item in row["evidence_ids"]),
                "each focal-variant observation requires direct primary evidence",
            )
        else:
            _require(
                all(evidence_applicability[item] == "contextual" for item in row["evidence_ids"]),
                "non-focal variant observations must remain contextual",
            )
    _require(focal_observation_count > 0, "focal variant has no observations")
    _require(used_evidence_ids == evidence_ids, "every evidence reference must support an observation")
    site_match = _SITE_RE.fullmatch(case["site_context_binding"]["site_id"])
    assert site_match is not None
    _require(
        uniprot_id == site_match.group(1)
        and focal_signature.group(1) == site_match.group(2)
        and int(focal_signature.group(2)) == int(site_match.group(3)),
        "focal variant does not match the bound reference catalyst site",
    )
    applicability_observations = _strings(applicability["observation_ids"], "applicability.observation_ids", nonempty=True)
    _require(set(applicability_observations) == observation_ids, "applicability must cover every observation exactly")

    discriminants = _array(case["discriminants"], "discriminants", nonempty=True)
    discriminant_ids: set[str] = set()
    covered_observations: set[str] = set()
    assessment_by_discriminant: dict[str, dict[str, str]] = {}
    observations_by_discriminant: dict[str, list[str]] = {}
    for index, raw in enumerate(discriminants):
        label = f"discriminants[{index}]"
        row = _exact(raw, _DISCRIMINANT_FIELDS, label)
        discriminant_id = _string(row["discriminant_id"], f"{label}.discriminant_id")
        _require(discriminant_id not in discriminant_ids, "discriminant IDs repeat")
        discriminant_ids.add(discriminant_id)
        _require(row["status"] == "retrospectively_observed", f"{label}.status differs")
        ids = _strings(row["observation_ids"], f"{label}.observation_ids", nonempty=True)
        _require(set(ids) <= observation_ids, f"{label}.observation_ids do not resolve")
        covered_observations.update(ids)
        observations_by_discriminant[discriminant_id] = ids
        assessments = _array(row["alternative_assessments"], f"{label}.alternative_assessments", nonempty=True)
        by_alternative: dict[str, str] = {}
        for assessment_index, raw_assessment in enumerate(assessments):
            assessment_label = f"{label}.alternative_assessments[{assessment_index}]"
            assessment = _exact(raw_assessment, _ASSESSMENT_FIELDS, assessment_label)
            alternative_id = _string(assessment["alternative_id"], f"{assessment_label}.alternative_id")
            _require(alternative_id in alternative_ids and alternative_id not in by_alternative, f"{assessment_label}.alternative_id is invalid or repeated")
            _require(assessment["relation"] in {"supports", "counters", "does_not_resolve"}, f"{assessment_label}.relation is unsupported")
            _string(assessment["statement"], f"{assessment_label}.statement")
            by_alternative[alternative_id] = assessment["relation"]
        _require(set(by_alternative) == alternative_ids, f"{label} must assess every alternative")
        assessment_by_discriminant[discriminant_id] = by_alternative
    _require(covered_observations == observation_ids, "every observation must participate in a discriminant")

    adjudication = _exact(case["adjudication"], _ADJUDICATION_FIELDS, "adjudication")
    _require(adjudication["claim_status"] in {"supported", "diagnostic", "unresolved"}, "adjudication.claim_status is unsupported")
    selected = adjudication["selected_alternative_id"]
    _require(selected is None or selected in alternative_ids, "adjudication selected alternative does not resolve")
    _require((selected is None) == (adjudication["claim_status"] == "unresolved"), "adjudication selected alternative/status differ")
    _string(adjudication["statement"], "adjudication.statement")
    basis = _strings(adjudication["basis_discriminant_ids"], "adjudication.basis_discriminant_ids", nonempty=selected is not None)
    _require(set(basis) <= discriminant_ids, "adjudication basis discriminants do not resolve")
    unresolved = _strings(adjudication["unresolved_alternative_ids"], "adjudication.unresolved_alternative_ids")
    _require(set(unresolved) <= alternative_ids and selected not in unresolved, "adjudication unresolved alternatives are invalid")
    if selected is not None:
        _require(any(assessment_by_discriminant[item][selected] == "supports" for item in basis), "selected alternative lacks supporting discriminant evidence")
        _require(
            any(
                assessment_by_discriminant[item][selected] == "supports"
                and any(
                    observation_by_id[observation_id]["variant"]["variant_id"]
                    == focal_variant_id
                    and any(
                        evidence_applicability[evidence_id] == "direct"
                        for evidence_id in observation_by_id[observation_id]["evidence_ids"]
                    )
                    for observation_id in observations_by_discriminant[item]
                )
                for item in basis
            ),
            "selected conclusion lacks a focal-variant direct-evidence discriminant",
        )

    abstentions = _array(case["mandatory_abstentions"], "mandatory_abstentions", nonempty=True)
    abstention_ids: set[str] = set()
    for index, raw in enumerate(abstentions):
        label = f"mandatory_abstentions[{index}]"
        row = _exact(raw, _ABSTENTION_FIELDS, label)
        abstention_id = _string(row["abstention_id"], f"{label}.abstention_id")
        _require(abstention_id not in abstention_ids, "mandatory abstention IDs repeat")
        abstention_ids.add(abstention_id)
        _string(row["reason"], f"{label}.reason")
    _require(
        _REQUIRED_ABSTENTIONS <= abstention_ids,
        "mechanistic-evidence case omits a required source or inference abstention",
    )
    scope = _exact(case["scope_effect"], _SCOPE_FIELDS, "scope_effect")
    _require(all(scope[field] is False for field in _SCOPE_FIELDS), "mechanistic-evidence overlay promotes an upstream or unsupported scope")
    return case_id, len(observations)


def validate_mechanism_evidence(
    value: Any, *, atlas10_bundle: dict[str, Any],
    transformation_values: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Validate one or more reviewed conclusions and all immutable joins."""
    data = _exact(value, _TOP_FIELDS, "mechanistic evidence")
    _require(data["schema_version"] == SCHEMA_VERSION and data["status"] == STATUS, "mechanistic-evidence schema/status differs")
    set_id = _string(data["evidence_set_id"], "evidence_set_id")
    _require(isinstance(transformation_values, dict) and bool(transformation_values), "transformation_values must be a nonempty mapping")
    set_query = query_transformation_sets(transformation_values, atlas10_bundle=atlas10_bundle)
    bindings = _validate_bindings(data["source_bindings"])
    cases = _array(data["cases"], "cases", nonempty=True)
    case_ids: set[str] = set()
    observation_count = 0
    for index, raw in enumerate(cases):
        case_id, count = _validate_case(raw, bindings, atlas10_bundle, transformation_values, set_query)
        _require(case_id not in case_ids, "mechanistic-evidence case IDs repeat")
        case_ids.add(case_id)
        observation_count += count
    payload_sha = canonical_mechanism_evidence_payload_sha256(data)
    review = _validate_review(data["review"], payload_sha)
    return {
        "evidence_set_id": set_id,
        "evidence_payload_sha256": payload_sha,
        "case_count": len(cases),
        "observation_count": observation_count,
        "reviewed_on": review["reviewed_on"],
    }


def _variant_filter(value: Any) -> str | None:
    if value is None:
        return None
    _require(isinstance(value, str), "variant must be an exact substitution such as H297N")
    result = value.strip().upper()
    _require(_VARIANT_RE.fullmatch(result) is not None, "variant must be WT or an exact substitution such as H297N")
    return result


def _endpoint_filter(value: Any) -> str | None:
    if value is None:
        return None
    _require(isinstance(value, str), "endpoint must be turnover, isotope_exchange, or structure")
    result = value.strip().lower()
    _require(result in _ENDPOINT_KINDS, "endpoint must be turnover, isotope_exchange, or structure")
    return result


def query_mechanism_evidence(
    value: dict[str, Any], *, atlas10_bundle: dict[str, Any],
    transformation_values: dict[str, dict[str, Any]], variant: str | None = None,
    endpoint: str | None = None,
    source_contexts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Filter source observations while preserving each complete adjudicated case."""
    summary = validate_mechanism_evidence(
        value, atlas10_bundle=atlas10_bundle, transformation_values=transformation_values,
    )
    variant = _variant_filter(variant)
    endpoint = _endpoint_filter(endpoint)
    matches: list[dict[str, Any]] = []
    matched_count = 0
    for case in value["cases"]:
        observations = [
            row for row in case["observations"]
            if (variant is None or row["variant"]["variant_id"] == variant)
            and (endpoint is None or row["endpoint"]["kind"] == endpoint)
        ]
        if not observations:
            continue
        matched_count += len(observations)
        matches.append({
            "case": copy.deepcopy(case),
            "matched_observation_ids": [row["observation_id"] for row in observations],
            "matched_observations": copy.deepcopy(observations),
        })
    result = {
        "schema_version": QUERY_SCHEMA_VERSION,
        "evidence_set_id": summary["evidence_set_id"],
        "evidence_payload_sha256": summary["evidence_payload_sha256"],
        "filters": {"variant": variant, "endpoint": endpoint},
        "case_count": len(matches),
        "matched_observation_count": matched_count,
        "matches": matches,
        "source_bindings": copy.deepcopy(value["source_bindings"]),
        "review": copy.deepcopy(value["review"]),
        "query_semantics": {
            "counted_object": "reviewed_retrospective_mechanistic_conclusion",
            "observation_filter_scope": "within_each_complete_adjudicated_case",
            "case_and_adjudication_preserved": True,
            "nondetection_is_numeric_zero": False,
            "published_observation_is_new_project_experiment": False,
            "selected_conclusion_is_statistical_confidence": False,
            "upstream_transformation_or_site_evidence_changed": False,
            "empty_result": "no_matching_source_observation_not_absence_of_catalytic_behavior",
        },
    }
    if source_contexts is not None:
        from .atlas_evidence_source_context import query_source_contexts

        result["source_context_query"] = query_source_contexts(source_contexts, value, variant=variant)
    return result


__all__ = [
    "QUERY_SCHEMA_VERSION", "REVIEW_UPDATE_RULE", "SCHEMA_VERSION", "STATUS",
    "canonical_mechanism_evidence_payload_sha256", "query_mechanism_evidence",
    "validate_mechanism_evidence",
]
