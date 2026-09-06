"""Evidence-bound computational permissions for draft development only.

This is a permissions/integrity gate, not an automatic judge of scientific truth.
Semantic resolutions are inspectable agent assessments bound to their inputs.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .atlas_draft_batch import DEFAULT_BATCH, DraftBatchPaths
from .atlas50_state_probe import (
    SUCCESSOR_REPORT_SCHEMA_VERSION,
    declared_probe_case_ids,
    validate_state_probe,
)
from .atlas50_crosswalk_v2 import validate_change_map, validate_crosswalk_v2
from .canonical_hash import canonical_file_sha256

DIRECTORY = Path("data/atlas/atlas50/development_gate")
ADJUDICATIONS = "data/atlas/atlas50/development_gate/adjudications.json"
POLICY = "data/governance/computational_review_policy.json"
CROSSWALK = "data/atlas/atlas50/crosswalk_v2/crosswalk.json"
CROSSWALK_CHANGE_MAP = "data/atlas/atlas50/crosswalk_v2/change_map.json"
CROSSWALK_MANIFEST = "data/atlas/atlas50/crosswalk_v2/manifest.json"
PROBE = "data/atlas/atlas50/state_probe/report.json"
PROBE_SPEC = "data/atlas/atlas50/state_probe/spec.json"
CHALLENGE = "data/atlas/atlas50/computational_review/source_challenge_20260905.json"
REQUIRED_INPUTS = {
    ADJUDICATIONS,
    POLICY,
    CROSSWALK,
    CROSSWALK_CHANGE_MAP,
    PROBE,
    CHALLENGE,
}
STATE_BASIS_INPUTS = {
    "atlas10_kernel": "data/atlas/atlas10/kernel.json",
    "atlas3_kernel": "data/atlas/atlas3/kernel.json",
    "candidate_spec": "data/atlas/atlas50/phase_a/candidate_spec.json",
    "computational_panel_review": "data/atlas/atlas50/computational_review/panel_review.json",
    "mechanism_record_v3_schema": "src/catalytic_earth/schemas/mechanism-record-v3.schema.json",
}
OPERATIONS = {"corrected_crosswalk_development", "source_annotation",
              "source_scoped_mechanism_draft", "exact_reaction_instance"}
CASE_ID_ORDER = ("M0064", "M0106", "M0107", "M0212", "M0753", "M0970")
CASE_IDS = set(CASE_ID_ORDER)
CASE_OPERATIONS = OPERATIONS - {"corrected_crosswalk_development"}
FORBIDDEN_CLAIMS = {"independent_validation_claim_permitted",
                    "experimental_validation_claim_permitted",
                    "gold_label_admission_permitted",
                    "protected_registry_expansion_permitted",
                    "frozen_phase_b_completion_permitted"}
BINDING_UPDATE_RULE = (
    "Do not automatically refresh these pins after input changes. Repeat "
    "source-to-decision review and adjudication first."
)
STATUS_REVIEW_INDEPENDENCE = {
    "reviewer_kind": "same_model_computational_agents",
    "blind_review": False,
    "statistically_independent": False,
    "correlated_error_risk": True,
    "independent_human_reviewer_count": 0,
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    return value


def _strings(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{context} must contain nonempty strings",
    )
    _require(len(value) == len(set(value)), f"{context} contains duplicates")
    _require(len(value) >= minimum, f"{context} is incomplete")
    return value


def _exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    _require(set(value) == expected, f"{context} fields differ")


def _structured_abstentions(value: Any, context: str) -> list[dict[str, str]]:
    _require(isinstance(value, list), f"{context} must be an array")
    result: list[dict[str, str]] = []
    clause_ids: set[str] = set()
    for index, item in enumerate(value):
        item_context = f"{context}[{index}]"
        clause = _object(item, item_context)
        _exact_keys(clause, {"clause_id", "reason"}, item_context)
        clause_id = clause.get("clause_id")
        reason = clause.get("reason")
        _require(isinstance(clause_id, str) and clause_id, f"{item_context}: clause_id missing")
        _require(isinstance(reason, str) and reason, f"{item_context}: reason missing")
        _require(clause_id not in clause_ids, f"{context} repeats clause {clause_id}")
        clause_ids.add(clause_id)
        result.append({"clause_id": clause_id, "reason": reason})
    return result


def _canonical_object_set(values: list[dict[str, Any]]) -> set[bytes]:
    """Compare structured clauses without relying on dictionary key order."""

    return {canonical_bytes(value) for value in values}


def _read(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            _require(key not in result, f"duplicate key {key}")
            result[key] = value
        return result
    def nonfinite(value: str) -> None:
        raise ValueError(f"non-finite JSON {value}")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                       parse_constant=nonfinite)
    _require(isinstance(value, dict), f"object required: {path}")
    return value


def validate_policy(policy: dict[str, Any]) -> None:
    _require(policy.get("schema_version") == "catalytic-earth.computational-development-policy.v1",
             "unsupported development policy")
    _require(policy.get("human_submission_required_for_development") is False,
             "development policy must explicitly separate human validation")
    _require(policy.get("agent_consensus_is_evidence") is False,
             "agent consensus cannot authorize science")
    _require(policy.get("correlated_agent_errors_possible") is True,
             "agent independence cannot be assumed")
    for key in FORBIDDEN_CLAIMS:
        _require(policy.get(key) is False, f"forbidden claim authority: {key}")
    allowed_operations = _strings(
        policy.get("allowed_operations"), "policy.allowed_operations", minimum=1
    )
    _require(set(allowed_operations) == OPERATIONS, "operation authority differs")
    access = _object(policy.get("source_access"), "policy.source_access")
    _require(access.get("public_primary_sources_only") is True and
             access.get("paid_services_permitted") is False and
             access.get("gpu_jobs_permitted") is False, "source access differs")
    for key, ceiling in (("maximum_requests_per_batch", 100),
                         ("maximum_download_bytes_per_batch", 30 * 1024 * 1024)):
        value = access.get(key)
        _require(type(value) is int and 0 < value <= ceiling, f"invalid bounded budget: {key}")


def _required_inputs(batch: DraftBatchPaths) -> set[str]:
    if batch == DEFAULT_BATCH:
        return set(REQUIRED_INPUTS)
    return {
        batch.adjudications_path.as_posix(),
        POLICY,
        CROSSWALK,
        CROSSWALK_CHANGE_MAP,
        batch.probe_report_path.as_posix(),
        batch.probe_spec_path.as_posix(),
        batch.challenge_path.as_posix(),
    }


def validate_review_bindings(
    value: dict[str, Any], *, batch: DraftBatchPaths = DEFAULT_BATCH
) -> dict[str, str]:
    _exact_keys(
        value,
        {"schema_version", "date", "inputs", "update_rule"},
        "review bindings",
    )
    _require(
        value.get("schema_version")
        == "catalytic-earth.computational-review-bindings.v1",
        "unsupported review bindings",
    )
    _require(
        isinstance(value.get("date"), str)
        and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value["date"])),
        "review binding date is invalid",
    )
    _require(
        value.get("update_rule") == BINDING_UPDATE_RULE,
        "review bindings must prohibit automatic pin refresh",
    )
    bindings = _object(value.get("inputs"), "review bindings inputs")
    _require(set(bindings) == _required_inputs(batch), "review binding inputs differ")
    for name, expected in bindings.items():
        _require(
            isinstance(expected, str) and bool(re.fullmatch(r"[a-f0-9]{64}", expected)),
            f"invalid binding: {name}",
        )
    return bindings


def _validate_probe(
    probe: dict[str, Any],
    *,
    case_id_order: tuple[str, ...] = CASE_ID_ORDER,
    batch: DraftBatchPaths = DEFAULT_BATCH,
) -> dict[str, dict[str, Any]]:
    expected_schema = (
        "catalytic-earth.atlas50-state-probe.v1"
        if batch == DEFAULT_BATCH
        else SUCCESSOR_REPORT_SCHEMA_VERSION
    )
    _require(
        probe.get("schema_version") == expected_schema,
        "unsupported state probe",
    )
    _require(
        probe.get("status")
        == "computational_development_review_not_mechanism_compilation",
        "state probe status overclaims",
    )
    independence = _object(
        probe.get("review_independence"), "state probe review_independence"
    )
    _require(independence.get("same_model_agents") is True, "state probe must disclose same-model review")
    _require(independence.get("blind_review") is False, "state probe review was informed, not blind")
    _require(
        independence.get("statistical_independence_claimed") is False,
        "state probe cannot claim statistical independence",
    )
    _require(independence.get("human_reviewers") == 0, "state probe cannot claim human review")
    _require(
        independence.get("domain_expert_review_claimed") is False,
        "state probe cannot claim domain-expert review",
    )
    warning = independence.get("correlation_warning")
    _require(
        isinstance(warning, str) and "correlated" in warning.lower(),
        "state probe must preserve correlated-error warning",
    )
    summary = _object(probe.get("summary"), "state probe summary")
    _require(summary.get("mechanisms_compiled") == 0, "state probe cannot claim compiled mechanisms")
    _require(summary.get("frozen_artifacts_modified") is False, "state probe cannot modify frozen artifacts")
    _require(
        summary.get("full_panel_review_recovered") is False,
        "state probe cannot claim recovered panel review",
    )

    evidence_rows = probe.get("evidence")
    _require(isinstance(evidence_rows, list) and evidence_rows, "state probe evidence missing")
    evidence_ids: list[str] = []
    for index, evidence in enumerate(evidence_rows):
        item = _object(evidence, f"state probe evidence[{index}]")
        evidence_id = item.get("evidence_id")
        _require(isinstance(evidence_id, str) and evidence_id, "state probe evidence ID missing")
        evidence_ids.append(evidence_id)
    _require(len(evidence_ids) == len(set(evidence_ids)), "state probe evidence IDs repeat")

    cases = probe.get("cases")
    _require(isinstance(cases, list), "state probe cases must be an array")
    _require(
        probe.get("case_count") == len(cases) == len(case_id_order),
        "state probe case count differs from its declared cases",
    )
    _require(
        tuple(case.get("mcsa_id") if isinstance(case, dict) else None for case in cases)
        == case_id_order,
        "state probe case order or IDs differ",
    )
    if batch != DEFAULT_BATCH:
        _require(
            probe.get("declared_case_ids") == list(case_id_order),
            "successor probe declaration differs",
        )
    by_id: dict[str, dict[str, Any]] = {}
    for case in cases:
        context = case["mcsa_id"]
        allowed = _strings(
            case.get("allowed_operations"),
            f"{context}: state probe allowed_operations",
            minimum=1,
        )
        _require(set(allowed) <= CASE_OPERATIONS, f"{context}: invalid probed operation")
        scopes = _strings(case.get("allowed_scope"), f"{context}: allowed_scope", minimum=1)
        _require(all(len(scope) >= 30 for scope in scopes), f"{context}: allowed scope is incomplete")
        case_evidence = _strings(
            case.get("evidence_ids"), f"{context}: state probe evidence_ids", minimum=1
        )
        _require(
            set(case_evidence) <= set(evidence_ids),
            f"{context}: state probe cites unknown evidence",
        )
        _structured_abstentions(
            case.get("mandatory_abstentions"),
            f"{context}: state probe mandatory_abstentions",
        )
        by_id[context] = case
    return by_id


def _claim_concerns(claim: dict[str, Any], mcsa_id: str) -> bool:
    subjects = claim["subject_ids"]
    return mcsa_id in subjects or f"atlas50.candidate.{mcsa_id.lower()}" in subjects


def _validate_challenge(
    challenge: dict[str, Any],
    *,
    case_ids: set[str] = CASE_IDS,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    _require(
        challenge.get("schema_version") == "catalytic-earth.atlas50-source-challenge.v1",
        "unsupported source challenge",
    )
    _require(
        challenge.get("status") == "computational_development_review_complete",
        "source challenge status differs",
    )
    boundary = _object(challenge.get("review_boundary"), "source challenge review_boundary")
    _require(boundary.get("blind_review") is False, "source challenge was informed, not blind")
    _require(boundary.get("correlated_error_risk") is True, "source challenge must disclose correlated errors")
    _require(
        boundary.get("statistically_independent") is False,
        "source challenge cannot claim statistical independence",
    )
    _require(
        boundary.get("human_or_domain_expert_review_claimed") is False,
        "source challenge cannot claim human or expert review",
    )
    _require(
        boundary.get("independent_validation_or_gold_status_conferred") is False,
        "source challenge cannot confer independent or gold status",
    )
    _require(
        isinstance(boundary.get("reviewer_class"), str)
        and "same-model" in boundary["reviewer_class"].lower(),
        "source challenge must identify same-model reviewers",
    )

    claims = challenge.get("claims")
    _require(isinstance(claims, list) and claims, "challenge claims missing")
    seen_claim_ids: set[str] = set()
    for index, claim_value in enumerate(claims):
        claim = _object(claim_value, f"challenge claims[{index}]")
        claim_id = claim.get("claim_id")
        _require(isinstance(claim_id, str) and claim_id, "invalid challenge claim identifier")
        _require(claim_id not in seen_claim_ids, "challenge claim identifiers repeat")
        seen_claim_ids.add(claim_id)
        _strings(claim.get("subject_ids"), f"{claim_id}: subject_ids", minimum=1)
        _require(
            claim.get("verdict") in {"supported", "contradicted", "insufficient"},
            f"{claim_id}: invalid challenge verdict",
        )
        _require(type(claim.get("objection_resolved")) is bool, f"{claim_id}: objection status missing")
        evidence = claim.get("evidence")
        _require(isinstance(evidence, list) and evidence, f"{claim_id}: no source-backed challenge")
        for evidence_index, evidence_value in enumerate(evidence):
            item = _object(evidence_value, f"{claim_id}: evidence[{evidence_index}]")
            _require(
                isinstance(item.get("type"), str)
                and item["type"]
                and isinstance(item.get("finding"), str)
                and item["finding"],
                f"{claim_id}: malformed challenge evidence",
            )
            url = item.get("url")
            path = item.get("path")
            has_url = isinstance(url, str) and bool(re.fullmatch(r"https://[^\s]+", url))
            has_path = (
                isinstance(path, str)
                and path
                and not Path(path).is_absolute()
                and ".." not in Path(path).parts
            )
            _require(has_url or has_path, f"{claim_id}: challenge evidence has no valid locator")

    cross_review = _object(challenge.get("cross_review"), "source challenge cross_review")
    material = cross_review.get("material_open_objections")
    _require(isinstance(material, list), "material open objections must be an array")
    for index, objection_value in enumerate(material):
        context = f"material open objections[{index}]"
        objection = _object(objection_value, context)
        blocks = _strings(objection.get("blocks"), f"{context}.blocks", minimum=1)
        permitted = _strings(objection.get("permitted"), f"{context}.permitted")
        subjects = _strings(objection.get("subject_ids"), f"{context}.subject_ids", minimum=1)
        _require(set(blocks) <= CASE_OPERATIONS, f"{context}: invalid blocking operation")
        _require(set(permitted) <= CASE_OPERATIONS, f"{context}: invalid permitted operation")
        _require(not (set(blocks) & set(permitted)), f"{context}: operation both blocked and permitted")
        _require(
            isinstance(objection.get("objection"), str) and objection["objection"],
            f"{context}: reason missing",
        )
        valid_subject_ids = case_ids | {
            f"atlas50.candidate.{mcsa_id.lower()}" for mcsa_id in case_ids
        }
        _require(any(subject in valid_subject_ids for subject in subjects),
                 f"{context}: no disputed case subject")
    return claims, material


def _compact_json_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_transitive_review_pins(
    root: Path,
    challenge: dict[str, Any],
    direct_bindings: dict[str, str],
    *,
    batch: DraftBatchPaths = DEFAULT_BATCH,
    case_id_order: tuple[str, ...] = CASE_ID_ORDER,
) -> None:
    """Require the files reviewed by the challenge, including transitive inputs."""

    cross_review = _object(challenge.get("cross_review"), "source challenge cross_review")
    artifacts = cross_review.get("artifacts_checked")
    _require(isinstance(artifacts, list), "source challenge artifact reviews missing")
    by_family: dict[str, dict[str, Any]] = {}
    for index, artifact_value in enumerate(artifacts):
        artifact = _object(artifact_value, f"artifacts_checked[{index}]")
        family = artifact.get("artifact_family")
        _require(isinstance(family, str) and family, "reviewed artifact family missing")
        _require(family not in by_family, f"reviewed artifact family repeats: {family}")
        by_family[family] = artifact

    probe_paths = (
        batch.probe_report_path.as_posix(),
        batch.probe_spec_path.as_posix(),
    )
    requirements: dict[str, dict[str, Any]] = {
        "atlas50_crosswalk_v2": {
            "result": "accepted_after_corrections",
            "paths": (CROSSWALK, CROSSWALK_CHANGE_MAP, CROSSWALK_MANIFEST),
        },
        "atlas50_state_probe": {
            "result": (
                "accepted_after_provenance_correction"
                if batch == DEFAULT_BATCH
                else "accepted_with_explicit_abstentions"
            ),
            "paths": probe_paths,
        },
    }
    if batch != DEFAULT_BATCH:
        new_case_ids = [
            case_id for case_id in case_id_order if case_id not in CASE_IDS
        ]
        _require(new_case_ids, "successor review has no newly declared cases")
        requirements["atlas_source_batch"] = {
            "result": "accepted_with_explicit_abstentions",
            "paths": tuple(
                (batch.sources_directory / f"{case_id}.json").as_posix()
                for case_id in new_case_ids
            ),
        }
    for family, requirement in requirements.items():
        _require(family in by_family, f"source challenge did not review {family}")
        artifact = by_family[family]
        _require(
            artifact.get("result") == requirement["result"],
            f"source challenge did not accept {family}",
        )
        paths = _strings(artifact.get("paths"), f"{family}.paths", minimum=1)
        relative_by_name: dict[str, str] = {}
        for relative in paths:
            parsed = Path(relative)
            _require(
                not parsed.is_absolute() and ".." not in parsed.parts,
                f"{family}: invalid reviewed path",
            )
            _require(parsed.name not in relative_by_name, f"{family}: ambiguous reviewed basename")
            relative_by_name[parsed.name] = relative
        pins = _object(artifact.get("pinned_file_sha256"), f"{family}.pinned_file_sha256")
        expected_names = {Path(relative).name for relative in requirement["paths"]}
        _require(set(pins) == expected_names, f"{family}: reviewed pin set differs")
        for relative in requirement["paths"]:
            basename = Path(relative).name
            _require(
                relative_by_name.get(basename) == relative,
                f"{family}: reviewed path differs for {basename}",
            )
            expected = pins.get(basename)
            _require(
                isinstance(expected, str) and bool(re.fullmatch(r"[a-f0-9]{64}", expected)),
                f"{family}: invalid reviewed hash for {basename}",
            )
            _require(
                canonical_file_sha256(root / relative) == expected,
                f"source-challenge reviewed input changed: {relative}",
            )
            if relative in direct_bindings:
                _require(
                    direct_bindings[relative] == expected,
                    f"direct and source-challenge bindings differ: {relative}",
                )

    manifest = _read(root / CROSSWALK_MANIFEST)
    _require(
        manifest.get("schema_version")
        == "catalytic-earth.atlas50-crosswalk-v2-manifest.v1",
        "unsupported crosswalk manifest",
    )
    _require(manifest.get("frozen_phase_a_or_b_modified") is False, "crosswalk manifest modifies frozen phases")
    _require(manifest.get("protected_registry_modified") is False, "crosswalk manifest modifies protected registry")
    _require(manifest.get("independent_human_review_claimed") is False, "crosswalk manifest claims human review")
    _require(manifest.get("experimental_validation_claimed") is False, "crosswalk manifest claims experimental validation")
    manifest_outputs = manifest.get("outputs")
    _require(isinstance(manifest_outputs, list), "crosswalk manifest outputs missing")
    output_hashes: dict[str, str] = {}
    for item_value in manifest_outputs:
        item = _object(item_value, "crosswalk manifest output")
        name, digest = item.get("path"), item.get("sha256")
        _require(
            isinstance(name, str)
            and name in {Path(CROSSWALK).name, Path(CROSSWALK_CHANGE_MAP).name}
            and isinstance(digest, str)
            and bool(re.fullmatch(r"[a-f0-9]{64}", digest)),
            "invalid crosswalk manifest output",
        )
        _require(name not in output_hashes, "duplicate crosswalk manifest output")
        output_hashes[name] = digest
    _require(
        set(output_hashes) == {Path(CROSSWALK).name, Path(CROSSWALK_CHANGE_MAP).name},
        "crosswalk manifest output set differs",
    )
    for relative in (CROSSWALK, CROSSWALK_CHANGE_MAP):
        _require(
            canonical_file_sha256(root / relative) == output_hashes[Path(relative).name],
            f"crosswalk manifest output changed: {relative}",
        )
    manifest_inputs = manifest.get("inputs")
    _require(isinstance(manifest_inputs, list) and manifest_inputs, "crosswalk manifest inputs missing")
    seen_inputs: set[str] = set()
    for item_value in manifest_inputs:
        item = _object(item_value, "crosswalk manifest input")
        relative, digest = item.get("path"), item.get("sha256")
        _require(
            isinstance(relative, str)
            and relative
            and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts,
            "invalid crosswalk manifest input path",
        )
        _require(
            isinstance(digest, str) and bool(re.fullmatch(r"[a-f0-9]{64}", digest)),
            f"invalid crosswalk manifest input hash: {relative}",
        )
        _require(relative not in seen_inputs, "duplicate crosswalk manifest input")
        seen_inputs.add(relative)
        _require(
            canonical_file_sha256(root / relative) == digest,
            f"crosswalk manifest input changed: {relative}",
        )

    probe = _read(root / batch.probe_report_path)
    probe_spec = _read(root / batch.probe_spec_path)
    _require(
        probe.get("spec_sha256") == _compact_json_sha256(probe_spec),
        "state probe spec binding differs",
    )
    basis = _object(probe.get("basis_inputs"), "state probe basis_inputs")
    _require(set(basis) == set(STATE_BASIS_INPUTS), "state probe basis input set differs")
    for name, relative in STATE_BASIS_INPUTS.items():
        _require(
            basis.get(name) == canonical_file_sha256(root / relative),
            f"state probe basis input changed: {relative}",
        )


def validate_adjudications(
    value: dict[str, Any],
    probe: dict[str, Any],
    challenge: dict[str, Any],
    *,
    case_id_order: tuple[str, ...] = CASE_ID_ORDER,
    batch: DraftBatchPaths = DEFAULT_BATCH,
    repo_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require(value.get("schema_version") == "catalytic-earth.computational-adjudications.v1",
             "unsupported adjudications")
    _require(value.get("human_review") is False, "adjudication cannot claim human review")
    _require(value.get("independent_review") is False, "same-model adjudication is not independent")
    _require(value.get("same_model_family") is True, "same-model adjudication must be disclosed")
    _require(value.get("correlated_errors_possible") is True, "correlated adjudication errors must be disclosed")
    _require(value.get("blind_review") is False, "adjudication was informed, not blind")
    by_id = _validate_probe(
        probe, case_id_order=case_id_order, batch=batch
    )
    claims, material_objections = _validate_challenge(
        challenge, case_ids=set(case_id_order)
    )
    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    resolutions = value.get("cases", [])
    _require(isinstance(resolutions, list), "adjudication cases must be an array")
    _require(
        tuple(row.get("mcsa_id") if isinstance(row, dict) else None for row in resolutions)
        == case_id_order,
        "adjudications must cover the declared cases in probe order",
    )
    if batch != DEFAULT_BATCH:
        _require(repo_root is not None, "successor adjudication validation requires repo_root")
        inheritance = _object(
            value.get("inheritance"), "adjudication inheritance"
        )
        _exact_keys(
            inheritance,
            {
                "adjudications_path",
                "adjudications_sha256",
                "inherited_case_ids",
            },
            "adjudication inheritance",
        )
        _require(
            inheritance["adjudications_path"]
            == DEFAULT_BATCH.adjudications_path.as_posix(),
            "successor adjudication inheritance path differs",
        )
        inherited_case_ids = tuple(inheritance["inherited_case_ids"])
        _require(
            inherited_case_ids == CASE_ID_ORDER,
            "successor must inherit the exact legacy adjudication cases",
        )
        base_path = Path(repo_root) / DEFAULT_BATCH.adjudications_path
        _require(
            inheritance["adjudications_sha256"]
            == canonical_file_sha256(base_path),
            "successor legacy adjudication pin differs",
        )
        base = _read(base_path)
        _require(
            resolutions[: len(inherited_case_ids)] == base["cases"],
            "successor changed an inherited adjudication case",
        )
    result = []
    for row in resolutions:
        source = by_id[row["mcsa_id"]]
        context = row["mcsa_id"]
        allowed = _strings(row.get("allowed_operations"), f"{context}: allowed_operations", minimum=1)
        _require(set(allowed) <= CASE_OPERATIONS, f"{context}: invalid operations")
        _require(set(allowed) <= set(source["allowed_operations"]),
                 f"{context}: adjudication exceeds probed operations")
        source_scope = " ".join(source["allowed_scope"])
        _require(row.get("scope") == source_scope, f"{context}: scope differs from state probe")

        source_abstentions = _structured_abstentions(
            source.get("mandatory_abstentions"),
            f"{context}: state probe mandatory_abstentions",
        )
        abstentions = _structured_abstentions(
            row.get("mandatory_abstentions"), f"{context}: mandatory_abstentions"
        )
        _require(
            _canonical_object_set(source_abstentions)
            <= _canonical_object_set(abstentions),
            f"{context}: source abstentions or reasons differ",
        )

        row_evidence = _strings(row.get("evidence_ids"), f"{context}: evidence_ids", minimum=1)
        _require(row_evidence == source["evidence_ids"], f"{context}: probe evidence binding differs")

        expected_claim_ids = [claim["claim_id"] for claim in claims if _claim_concerns(claim, context)]
        evidence = _strings(
            row.get("challenge_claim_ids"), f"{context}: challenge_claim_ids", minimum=1
        )
        _require(evidence == expected_claim_ids, f"{context}: challenge evidence coverage differs")
        for claim_id in evidence:
            claim = claim_by_id[claim_id]
            _require(_claim_concerns(claim, context), f"{claim_id}: challenge does not concern {context}")
            _require(
                any(isinstance(item.get("url"), str) and item["url"].startswith("https://")
                    for item in claim["evidence"]),
                f"{claim_id}: no external source-backed challenge",
            )
        _require(isinstance(row.get("resolution"), str) and len(row["resolution"]) >= 60,
                 f"{context}: evidence-linked resolution required")
        objections = row.get("open_objections")
        _require(isinstance(objections, list), f"{context}: objections must be explicit")
        blocked: set[str] = set()
        seen_objections: set[bytes] = set()
        for index, objection_value in enumerate(objections):
            objection = _object(objection_value, f"{context}: open_objections[{index}]")
            _exact_keys(objection, {"reason", "blocks"}, f"{context}: open_objections[{index}]")
            blocks = _strings(
                objection.get("blocks"), f"{context}: open_objections[{index}].blocks", minimum=1
            )
            _require(isinstance(objection.get("reason"), str) and objection["reason"],
                     f"{context}: objection reason missing")
            _require(set(blocks) <= CASE_OPERATIONS,
                     f"{context}: objection blocking scope missing")
            _require(not (set(allowed) & set(blocks)),
                     f"{context}: unresolved objection blocks requested operation")
            canonical = canonical_bytes(objection)
            _require(canonical not in seen_objections, f"{context}: duplicate objection")
            seen_objections.add(canonical)
            blocked.update(blocks)

        expected_blocked = CASE_OPERATIONS - set(allowed)
        _require(blocked == expected_blocked, f"{context}: unavailable operations lack explicit objections")
        relevant_material = [
            objection
            for objection in material_objections
            if context in objection["subject_ids"]
            or f"atlas50.candidate.{context.lower()}" in objection["subject_ids"]
        ]
        for objection in relevant_material:
            _require(
                set(objection["blocks"]) <= blocked,
                f"{context}: material source-challenge objection was bypassed",
            )
            _require(
                set(allowed) <= set(objection["permitted"]),
                f"{context}: adjudication exceeds material objection scope",
            )
        if any(not claim_by_id[claim_id]["objection_resolved"] for claim_id in evidence):
            _require(relevant_material, f"{context}: unresolved challenge lacks a material objection")
        result.append({"mcsa_id": context, "allowed_operations": allowed,
                       "scope": row["scope"], "mandatory_abstentions": abstentions,
                       "open_objections": objections,
                       "challenge_claim_ids": evidence,
                       "evidence_ids": row_evidence})
    return result


def build_development_status(
    repo_root: Path, *, batch: DraftBatchPaths = DEFAULT_BATCH
) -> dict[str, Any]:
    root = Path(repo_root)
    policy = _read(root / POLICY)
    validate_policy(policy)
    manifest = _read(root / batch.review_bindings_path)
    bindings = validate_review_bindings(manifest, batch=batch)
    for name, expected in bindings.items():
        _require(canonical_file_sha256(root / name) == expected, f"review input changed: {name}")
    crosswalk = _read(root / CROSSWALK)
    change_map = _read(root / CROSSWALK_CHANGE_MAP)
    validate_crosswalk_v2(crosswalk)
    validate_change_map(change_map, crosswalk)
    _require(
        crosswalk.get("status")
        == "computational_provisional_not_human_or_experimental_review",
        "corrected crosswalk status overclaims",
    )
    probe_spec = _read(root / batch.probe_spec_path)
    probe = _read(root / batch.probe_report_path)
    case_id_order = declared_probe_case_ids(probe_spec, batch=batch)
    basis_inputs = {
        name: canonical_file_sha256(root / relative)
        for name, relative in STATE_BASIS_INPUTS.items()
    }
    validate_state_probe(
        probe,
        spec=probe_spec,
        candidate_spec=_read(root / STATE_BASIS_INPUTS["candidate_spec"]),
        panel_review=_read(root / STATE_BASIS_INPUTS["computational_panel_review"]),
        mechanism_v3_schema=_read(root / STATE_BASIS_INPUTS["mechanism_record_v3_schema"]),
        atlas3_kernel=_read(root / STATE_BASIS_INPUTS["atlas3_kernel"]),
        atlas10_kernel=_read(root / STATE_BASIS_INPUTS["atlas10_kernel"]),
        basis_inputs=basis_inputs,
        batch=batch,
        repo_root=root,
    )
    challenge = _read(root / batch.challenge_path)
    _validate_transitive_review_pins(
        root,
        challenge,
        bindings,
        batch=batch,
        case_id_order=case_id_order,
    )
    adjudications = _read(root / batch.adjudications_path)
    cases = validate_adjudications(
        adjudications,
        probe,
        challenge,
        case_id_order=case_id_order,
        batch=batch,
        repo_root=root,
    )
    return {
        "schema_version": "catalytic-earth.computational-development-status.v1",
        "policy_id": policy["policy_id"],
        "status": "open_for_scoped_development",
        "human_review_wait_blocks_development": False,
        "human_review_completed": False,
        "independent_validation_established": False,
        "experimental_validation_established": False,
        "frozen_phase_b_completed": False,
        "protected_registry_expansion_permitted": False,
        "global_operations": ["corrected_crosswalk_development"],
        "input_bindings": bindings,
        "adjudications_sha256": bindings[batch.adjudications_path.as_posix()],
        "review_independence": dict(STATUS_REVIEW_INDEPENDENCE),
        "cases": cases,
        "source_access": policy["source_access"],
        "scope_boundary": "Operations apply only to the declared source-scoped units; partial passes are not full candidate admission or validated mechanisms.",
        "validation_boundary": "This gate checks permissions, pinned evidence and explicit objections. It cannot authenticate scientific correctness or make correlated agents statistically independent."
    }


def require_operation(
    repo_root: Path,
    operation: str,
    mcsa_id: str | None = None,
    *,
    batch: DraftBatchPaths = DEFAULT_BATCH,
) -> None:
    """Check pinned inputs anew; a caller-supplied status cannot grant authority."""
    status = build_development_status(repo_root, batch=batch)
    _require(operation in OPERATIONS, "operation is outside computational development authority")
    if mcsa_id is None:
        _require(operation in status.get("global_operations", []), "operation requires a scoped case")
    else:
        case = next((row for row in status.get("cases", []) if row["mcsa_id"] == mcsa_id), None)
        _require(case is not None and operation in case["allowed_operations"],
                 f"operation not authorized for {mcsa_id}")
