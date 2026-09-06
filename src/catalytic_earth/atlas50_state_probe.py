"""Generic, source-bound representation probe for disputed Atlas-50 cases.

The probe is deliberately smaller than a mechanism record compiler.  It asks
whether a requested operation can be expressed with typed component, carrier,
or polymer state fields using only cited source assertions.  Missing state is
kept as an abstention; it is never filled from enzyme-family knowledge.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .atlas_draft_batch import DEFAULT_BATCH, DraftBatchPaths


SPEC_SCHEMA_VERSION = "catalytic-earth.atlas50-state-probe-spec.v1"
REPORT_SCHEMA_VERSION = "catalytic-earth.atlas50-state-probe.v1"
SUCCESSOR_SPEC_SCHEMA_VERSION = "catalytic-earth.atlas50-state-probe-spec.v2"
SUCCESSOR_REPORT_SCHEMA_VERSION = "catalytic-earth.atlas50-state-probe.v2"
COMPILER_VERSION = "catalytic-earth.atlas50-state-probe-compiler.v1"

TARGET_MCSA_IDS = ("M0064", "M0106", "M0107", "M0212", "M0753", "M0970")
DISPOSITIONS = ("PASS", "SCOPED_PASS", "ABSTAIN")
CLAUSE_STATUSES = ("satisfied", "abstained")
SCOPE_STATUSES = ("candidate_scope", "source_narrowed")
REVIEW_RECOMMENDATIONS = (
    "accept_proposed_include",
    "revise_with_evidence",
    "accept_fail_closed_exclusion",
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_UNIPROT_RE = re.compile(r"^[A-Z0-9]{6,10}$")
_PDB_RE = re.compile(r"^[0-9][A-Z0-9]{3}$")


# Clause names describe information, not enzyme families.  An operation is
# allowed only when every clause listed for it is source-grounded.
CONTRACTS: dict[str, dict[str, Any]] = {
    "component_state": {
        "purpose": (
            "Represent source-identified components, their association mode, "
            "and only the component states or transitions the cited source asserts."
        ),
        "clauses": (
            "component_identities",
            "assembly_mode",
            "state_claim_provenance",
            "scope_boundary",
            "complete_target_state",
        ),
        "operation_requirements": {
            "source_annotation": (
                "component_identities",
                "scope_boundary",
            ),
            "source_scoped_mechanism_draft": (
                "component_identities",
                "assembly_mode",
                "state_claim_provenance",
                "scope_boundary",
            ),
        },
    },
    "tethered_carrier_reaction_instance": {
        "purpose": (
            "Separate catalyst identity, carrier-owner role, covalently tethered "
            "reactant/product states, attachment site, and structural localization."
        ),
        "clauses": (
            "enzyme_source_identity",
            "carrier_owner_role",
            "carrier_reactant_state",
            "carrier_product_state",
            "carrier_state_transition",
            "carrier_host_identity",
            "attachment_site",
            "structure_localization",
            "reaction_provenance",
        ),
        "operation_requirements": {
            "source_annotation": (
                "enzyme_source_identity",
                "reaction_provenance",
            ),
            "source_scoped_mechanism_draft": (
                "enzyme_source_identity",
                "carrier_owner_role",
                "carrier_reactant_state",
                "carrier_product_state",
                "carrier_state_transition",
                "reaction_provenance",
            ),
            "exact_reaction_instance": (
                "enzyme_source_identity",
                "carrier_owner_role",
                "carrier_reactant_state",
                "carrier_product_state",
                "carrier_state_transition",
                "carrier_host_identity",
                "attachment_site",
                "structure_localization",
                "reaction_provenance",
            ),
        },
    },
    "polymer_topology": {
        "purpose": (
            "Separate polymer identity from before/after topology, chain-length "
            "variables, initiation or elongation, and processivity."
        ),
        "clauses": (
            "catalyst_identity",
            "polymer_reactant_identity",
            "polymer_product_identity",
            "reaction_event",
            "topology_before",
            "topology_after",
            "chain_length_before",
            "chain_length_after",
            "initiation_or_elongation",
            "processivity",
            "reaction_provenance",
        ),
        "operation_requirements": {
            "source_annotation": (
                "catalyst_identity",
                "polymer_reactant_identity",
                "reaction_provenance",
            ),
            "source_scoped_mechanism_draft": (
                "catalyst_identity",
                "polymer_reactant_identity",
                "polymer_product_identity",
                "reaction_event",
                "topology_before",
                "topology_after",
                "reaction_provenance",
            ),
            "exact_reaction_instance": (
                "catalyst_identity",
                "polymer_reactant_identity",
                "polymer_product_identity",
                "reaction_event",
                "topology_before",
                "topology_after",
                "chain_length_before",
                "chain_length_after",
                "initiation_or_elongation",
                "processivity",
                "reaction_provenance",
            ),
        },
    },
}

REPRESENTATION_FIELDS = {
    "components",
    "assembly",
    "state_transitions",
    "tethered_carrier",
    "polymer_topology",
}


def canonical_json_bytes(value: Any) -> bytes:
    """Return repository-canonical JSON bytes."""

    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    """Hash a value using compact, key-sorted JSON."""

    payload = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    """Hash a repository input after normalizing text newlines."""

    payload = Path(path).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _exact_keys(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    actual = set(value)
    _require(
        actual == expected,
        f"{context} keys differ: missing={sorted(expected - actual)}, "
        f"extra={sorted(actual - expected)}",
    )
    return value


def _string_list(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(len(value) >= minimum, f"{context} must contain at least {minimum} items")
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{context} must contain non-empty strings",
    )
    _require(len(value) == len(set(value)), f"{context} contains duplicates")
    return value


def _candidate_index(candidate_spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["mcsa_id"]: row for row in candidate_spec["candidates"]}


def _panel_indexes(
    panel_review: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = {row["mcsa_id"]: row for row in panel_review["rows"]}
    findings = {
        row["mcsa_id"]: row for row in panel_review["decision_relevant_findings"]
    }
    return rows, findings


def _validate_receipts(
    spec: dict[str, Any], *, batch: DraftBatchPaths
) -> set[str]:
    ids: set[str] = set()
    total_bytes = 0
    for index, receipt in enumerate(spec["source_receipts"]):
        context = f"source_receipts[{index}]"
        _exact_keys(
            receipt,
            {
                "receipt_id",
                "source",
                "url",
                "retrieved_on",
                "bytes",
                "sha256",
                "raw_response_committed",
            },
            context,
        )
        _require(receipt["receipt_id"] not in ids, f"{context} repeats receipt_id")
        ids.add(receipt["receipt_id"])
        _require(isinstance(receipt["source"], str) and receipt["source"], f"{context} source is empty")
        _require(isinstance(receipt["url"], str) and receipt["url"].startswith("https://"), f"{context} URL must be HTTPS")
        _require(
            isinstance(receipt["retrieved_on"], str)
            and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", receipt["retrieved_on"])),
            f"{context} retrieval date differs",
        )
        if batch == DEFAULT_BATCH:
            _require(
                receipt["retrieved_on"] == spec["generated_on"],
                f"{context} retrieval date differs",
            )
        _require(isinstance(receipt["bytes"], int) and receipt["bytes"] > 0, f"{context} bytes are invalid")
        _require(bool(_SHA256_RE.fullmatch(receipt["sha256"])), f"{context} SHA-256 is invalid")
        _require(
            type(receipt["raw_response_committed"]) is bool,
            f"{context} raw-response status is invalid",
        )
        if batch == DEFAULT_BATCH:
            _require(
                receipt["raw_response_committed"] is False,
                f"{context} must not commit raw source bodies",
            )
        total_bytes += receipt["bytes"]
    _require(total_bytes < 30 * 1024 * 1024, "external source checks exceed 30 MiB")
    return ids


def _validate_evidence(spec: dict[str, Any], receipt_ids: set[str]) -> set[str]:
    ids: set[str] = set()
    allowed_kinds = {
        "official_database_record",
        "primary_paper_metadata_and_abstract",
        "inherited_official_receipt",
    }
    for index, item in enumerate(spec["evidence"]):
        context = f"evidence[{index}]"
        _exact_keys(
            item,
            {
                "evidence_id",
                "source_kind",
                "source_id",
                "source_record_id",
                "uri",
                "receipt_ids",
                "supports",
            },
            context,
        )
        _require(item["evidence_id"] not in ids, f"{context} repeats evidence_id")
        ids.add(item["evidence_id"])
        _require(item["source_kind"] in allowed_kinds, f"{context} source_kind is invalid")
        _require(isinstance(item["source_id"], str) and item["source_id"], f"{context} source_id is empty")
        _require(isinstance(item["source_record_id"], str) and item["source_record_id"], f"{context} source_record_id is empty")
        _require(isinstance(item["uri"], str) and item["uri"].startswith("https://"), f"{context} URI must be HTTPS")
        linked_receipts = _string_list(item["receipt_ids"], f"{context}.receipt_ids")
        _require(set(linked_receipts).issubset(receipt_ids), f"{context} references an unknown receipt")
        if item["source_kind"] != "inherited_official_receipt":
            _require(linked_receipts, f"{context} requires a direct receipt")
        _string_list(item["supports"], f"{context}.supports", minimum=1)
    return ids


def _validate_state_catalog(
    catalog: Any, evidence_ids: set[str], context: str
) -> dict[str, dict[str, Any]]:
    _require(isinstance(catalog, list), f"{context} must be an array")
    output: dict[str, dict[str, Any]] = {}
    for index, state in enumerate(catalog):
        item_context = f"{context}[{index}]"
        _exact_keys(
            state,
            {"state_id", "source_token", "name", "resolution", "evidence_ids"},
            item_context,
        )
        _require(
            state["resolution"] in {"resolved_identifier", "source_proposal_label", "unresolved_placeholder"},
            f"{item_context} resolution is invalid",
        )
        if state["resolution"] == "unresolved_placeholder":
            _require(state["state_id"] is None, f"{item_context} placeholder cannot have a resolved state_id")
        else:
            _require(isinstance(state["state_id"], str) and state["state_id"], f"{item_context} state_id is required")
            _require(state["state_id"] not in output, f"{item_context} repeats state_id")
            output[state["state_id"]] = state
        _require(isinstance(state["source_token"], str) and state["source_token"], f"{item_context} source_token is empty")
        _require(isinstance(state["name"], str), f"{item_context} name must be text")
        links = _string_list(state["evidence_ids"], f"{item_context}.evidence_ids", minimum=1)
        _require(set(links).issubset(evidence_ids), f"{item_context} cites unknown evidence")
    return output


def _validate_representation(
    value: Any,
    *,
    source_uniprot_ids: set[str],
    state_index: dict[str, dict[str, Any]],
    evidence_ids: set[str],
    context: str,
) -> None:
    representation = _exact_keys(value, REPRESENTATION_FIELDS, context)
    components = representation["components"]
    _require(isinstance(components, list) and components, f"{context}.components must be non-empty")
    component_ids: set[str] = set()
    for index, component in enumerate(components):
        item_context = f"{context}.components[{index}]"
        _exact_keys(
            component,
            {
                "component_id",
                "component_kind",
                "source_identifiers",
                "role",
                "identity_scope",
                "evidence_ids",
            },
            item_context,
        )
        component_id = component["component_id"]
        _require(isinstance(component_id, str) and component_id, f"{item_context} component_id is empty")
        _require(component_id not in component_ids, f"{item_context} repeats component_id")
        component_ids.add(component_id)
        _require(
            component["component_kind"]
            in {"protein", "protein_role", "cofactor", "metallocluster", "redox_partner", "polymer"},
            f"{item_context} component_kind is invalid",
        )
        _require(
            component["identity_scope"]
            in {"source_identity", "source_defined", "context_only", "role_only"},
            f"{item_context} identity_scope is invalid",
        )
        identifiers = component["source_identifiers"]
        _require(isinstance(identifiers, list), f"{item_context}.source_identifiers must be an array")
        for identifier_index, identifier in enumerate(identifiers):
            identifier_context = f"{item_context}.source_identifiers[{identifier_index}]"
            _exact_keys(identifier, {"namespace", "accession"}, identifier_context)
            _require(identifier["namespace"] in {"UniProtKB", "ChEBI", "M-CSA", "PDB"}, f"{identifier_context} namespace is invalid")
            _require(isinstance(identifier["accession"], str) and identifier["accession"], f"{identifier_context} accession is empty")
            if identifier["namespace"] == "UniProtKB" and component["identity_scope"] == "source_identity":
                _require(identifier["accession"] in source_uniprot_ids, f"{identifier_context} invents a source identity")
        if component["identity_scope"] in {"source_identity", "context_only"}:
            _require(identifiers, f"{item_context} exact/context identity needs an identifier")
        _require(isinstance(component["role"], str) and component["role"], f"{item_context} role is empty")
        links = _string_list(component["evidence_ids"], f"{item_context}.evidence_ids", minimum=1)
        _require(set(links).issubset(evidence_ids), f"{item_context} cites unknown evidence")

    assembly = _exact_keys(
        representation["assembly"],
        {"mode", "member_component_ids", "assertion_scope", "evidence_ids", "note"},
        f"{context}.assembly",
    )
    _require(
        assembly["mode"]
        in {"single_source_component", "fixed_multisubunit", "cycle_coupled_association", "external_carrier_encounter"},
        f"{context}.assembly mode is invalid",
    )
    members = _string_list(assembly["member_component_ids"], f"{context}.assembly.member_component_ids", minimum=1)
    _require(set(members).issubset(component_ids), f"{context}.assembly references an unknown component")
    _require(
        assembly["assertion_scope"] in {"source_assertion", "source_mechanism_proposal", "source_scope_boundary"},
        f"{context}.assembly assertion_scope is invalid",
    )
    links = _string_list(assembly["evidence_ids"], f"{context}.assembly.evidence_ids", minimum=1)
    _require(set(links).issubset(evidence_ids), f"{context}.assembly cites unknown evidence")
    _require(isinstance(assembly["note"], str) and assembly["note"], f"{context}.assembly note is empty")

    transitions = representation["state_transitions"]
    _require(isinstance(transitions, list), f"{context}.state_transitions must be an array")
    transition_ids: set[str] = set()
    for index, transition in enumerate(transitions):
        item_context = f"{context}.state_transitions[{index}]"
        _exact_keys(
            transition,
            {
                "transition_id",
                "subject_component_ids",
                "before_state_id",
                "after_state_id",
                "transition_kind",
                "assertion_scope",
                "evidence_ids",
            },
            item_context,
        )
        _require(transition["transition_id"] not in transition_ids, f"{item_context} repeats transition_id")
        transition_ids.add(transition["transition_id"])
        subjects = _string_list(transition["subject_component_ids"], f"{item_context}.subject_component_ids", minimum=1)
        _require(set(subjects).issubset(component_ids), f"{item_context} references an unknown component")
        for field in ("before_state_id", "after_state_id"):
            _require(transition[field] in state_index, f"{item_context}.{field} invents a state")
        _require(
            transition["transition_kind"]
            in {"redox", "nucleotide_hydrolysis", "carrier_loading"},
            f"{item_context} transition_kind is invalid",
        )
        _require(
            transition["assertion_scope"] in {"source_reaction", "source_mechanism_proposal", "primary_source_observation"},
            f"{item_context} assertion_scope is invalid",
        )
        links = _string_list(transition["evidence_ids"], f"{item_context}.evidence_ids", minimum=1)
        _require(set(links).issubset(evidence_ids), f"{item_context} cites unknown evidence")

    carrier = representation["tethered_carrier"]
    if carrier is not None:
        _exact_keys(
            carrier,
            {
                "owner_component_id",
                "attachment_residue",
                "attachment_site",
                "reactant_state_id",
                "product_state_id",
                "structure_component_ids",
                "status",
                "evidence_ids",
            },
            f"{context}.tethered_carrier",
        )
        _require(carrier["owner_component_id"] in component_ids, f"{context}.tethered_carrier owner is unknown")
        _require(carrier["reactant_state_id"] in state_index, f"{context}.tethered_carrier reactant state is invented")
        _require(carrier["product_state_id"] in state_index, f"{context}.tethered_carrier product state is invented")
        _require(carrier["status"] in {"source_scoped", "complete"}, f"{context}.tethered_carrier status is invalid")
        for component_id in _string_list(carrier["structure_component_ids"], f"{context}.tethered_carrier.structure_component_ids"):
            _require(component_id in component_ids, f"{context}.tethered_carrier structure component is unknown")
        _require(isinstance(carrier["attachment_residue"], str) and carrier["attachment_residue"], f"{context}.tethered_carrier attachment_residue is empty")
        _require(carrier["attachment_site"] is None or isinstance(carrier["attachment_site"], str), f"{context}.tethered_carrier attachment_site is invalid")
        links = _string_list(carrier["evidence_ids"], f"{context}.tethered_carrier.evidence_ids", minimum=1)
        _require(set(links).issubset(evidence_ids), f"{context}.tethered_carrier cites unknown evidence")

    polymer = representation["polymer_topology"]
    if polymer is not None:
        _exact_keys(
            polymer,
            {
                "polymer_component_id",
                "reactant_state_id",
                "product_state_id",
                "source_product_placeholder",
                "reaction_event",
                "topology_before",
                "topology_after",
                "chain_length_before",
                "chain_length_after",
                "initiation_or_elongation",
                "processivity",
                "status",
                "evidence_ids",
            },
            f"{context}.polymer_topology",
        )
        _require(polymer["polymer_component_id"] in component_ids, f"{context}.polymer_topology component is unknown")
        _require(polymer["reactant_state_id"] in state_index, f"{context}.polymer_topology reactant state is invented")
        if polymer["product_state_id"] is not None:
            _require(polymer["product_state_id"] in state_index, f"{context}.polymer_topology product state is invented")
        _require(polymer["status"] in {"source_scoped", "abstained"}, f"{context}.polymer_topology status is invalid")
        for field in (
            "source_product_placeholder",
            "reaction_event",
            "topology_before",
            "topology_after",
            "chain_length_before",
            "chain_length_after",
            "initiation_or_elongation",
            "processivity",
        ):
            _require(polymer[field] is None or isinstance(polymer[field], str), f"{context}.polymer_topology.{field} is invalid")
        links = _string_list(polymer["evidence_ids"], f"{context}.polymer_topology.evidence_ids", minimum=1)
        _require(set(links).issubset(evidence_ids), f"{context}.polymer_topology cites unknown evidence")


def declared_probe_case_ids(
    spec: dict[str, Any], *, batch: DraftBatchPaths = DEFAULT_BATCH
) -> tuple[str, ...]:
    """Return the exact ordered cases declared by a validated probe generation."""

    cases = spec.get("cases")
    _require(isinstance(cases, list), "probe cases must be an array")
    observed = tuple(
        case.get("mcsa_id") if isinstance(case, dict) else None for case in cases
    )
    if batch == DEFAULT_BATCH:
        _require(
            spec.get("schema_version") == SPEC_SCHEMA_VERSION,
            "unsupported probe spec schema",
        )
        _require(observed == TARGET_MCSA_IDS, "probe case order or IDs differ")
        return TARGET_MCSA_IDS

    _require(
        spec.get("schema_version") == SUCCESSOR_SPEC_SCHEMA_VERSION,
        "unsupported successor probe spec schema",
    )
    declared = spec.get("declared_case_ids")
    _require(isinstance(declared, list) and declared, "successor case declaration is missing")
    case_ids = tuple(declared)
    _require(
        all(isinstance(value, str) and _MCSA_RE.fullmatch(value) for value in case_ids),
        "successor case declaration contains an invalid M-CSA ID",
    )
    _require(len(case_ids) == len(set(case_ids)), "successor case declaration repeats an ID")
    _require(observed == case_ids, "successor cases differ from the declared order")
    inheritance = spec.get("inheritance")
    _require(isinstance(inheritance, dict), "successor probe inheritance is missing")
    _exact_keys(
        inheritance,
        {
            "base_batch_id",
            "probe_spec_path",
            "probe_spec_sha256",
            "probe_report_path",
            "probe_report_sha256",
            "inherited_case_ids",
        },
        "inheritance",
    )
    _require(inheritance["base_batch_id"] == DEFAULT_BATCH.batch_id, "successor base batch differs")
    _require(
        inheritance["probe_spec_path"] == DEFAULT_BATCH.probe_spec_path.as_posix()
        and inheritance["probe_report_path"] == DEFAULT_BATCH.probe_report_path.as_posix(),
        "successor probe inheritance paths differ",
    )
    for key in ("probe_spec_sha256", "probe_report_sha256"):
        _require(
            isinstance(inheritance[key], str)
            and bool(_SHA256_RE.fullmatch(inheritance[key])),
            f"inheritance.{key} is invalid",
        )
    inherited = tuple(inheritance["inherited_case_ids"])
    _require(inherited == TARGET_MCSA_IDS, "successor must inherit the exact legacy cases")
    _require(case_ids[: len(inherited)] == inherited, "successor must preserve legacy case order")
    _require(len(case_ids) > len(inherited), "successor must declare at least one new case")
    return case_ids


def validate_probe_spec(
    spec: dict[str, Any],
    *,
    candidate_spec: dict[str, Any],
    panel_review: dict[str, Any],
    batch: DraftBatchPaths = DEFAULT_BATCH,
) -> None:
    """Validate exact source identity, contract coverage, and abstentions."""

    fields = {
        "schema_version",
        "spec_id",
        "status",
        "generated_on",
        "claim_boundary",
        "review_independence",
        "source_receipts",
        "evidence",
        "cases",
    }
    if batch != DEFAULT_BATCH:
        fields |= {"declared_case_ids", "inheritance"}
    _exact_keys(spec, fields, "spec")
    case_ids = declared_probe_case_ids(spec, batch=batch)
    _require(spec["status"] == "bounded_computational_development_review_input", "probe spec status overclaims")
    _string_list(spec["claim_boundary"], "claim_boundary", minimum=1)
    independence = _exact_keys(
        spec["review_independence"],
        {
            "computational_roles",
            "same_model_agents",
            "blind_review",
            "statistical_independence_claimed",
            "human_reviewers",
            "domain_expert_review_claimed",
            "correlation_warning",
        },
        "review_independence",
    )
    _string_list(independence["computational_roles"], "review_independence.computational_roles", minimum=2)
    _require(independence["same_model_agents"] is True, "same-model correlation must be disclosed")
    _require(independence["blind_review"] is False, "informed source challenge cannot be called blind")
    _require(independence["statistical_independence_claimed"] is False, "computational agreement cannot claim statistical independence")
    _require(independence["human_reviewers"] == 0, "probe cannot claim human review")
    _require(independence["domain_expert_review_claimed"] is False, "probe cannot claim domain-expert review")
    _require(
        isinstance(independence["correlation_warning"], str)
        and "correlated" in independence["correlation_warning"].lower(),
        "review independence must state correlated-error risk",
    )
    receipt_ids = _validate_receipts(spec, batch=batch)
    evidence_ids = _validate_evidence(spec, receipt_ids)

    candidates = _candidate_index(candidate_spec)
    panel_rows, panel_findings = _panel_indexes(panel_review)
    cases = spec["cases"]
    inherited_case_ids = set(TARGET_MCSA_IDS) if batch != DEFAULT_BATCH else set(case_ids)

    candidate_ids: set[str] = set()
    for index, case in enumerate(cases):
        context = f"cases[{index}]"
        _exact_keys(
            case,
            {
                "candidate_id",
                "mcsa_id",
                "label",
                "contract_kind",
                "target_operation",
                "scope_status",
                "review_recommendation",
                "allowed_scope",
                "clause_results",
                "source_extract",
                "representation",
            },
            context,
        )
        mcsa_id = case["mcsa_id"]
        _require(bool(_MCSA_RE.fullmatch(mcsa_id)), f"{context} M-CSA ID is invalid")
        _require(case["candidate_id"] not in candidate_ids, f"{context} repeats candidate_id")
        candidate_ids.add(case["candidate_id"])
        _require(
            mcsa_id in candidates and mcsa_id in panel_rows,
            f"{context} lacks frozen source/review identity",
        )
        if mcsa_id in inherited_case_ids:
            _require(mcsa_id in panel_findings, f"{context} lacks inherited panel finding")
        frozen = candidates[mcsa_id]
        panel_row = panel_rows[mcsa_id]
        _require(case["candidate_id"] == f"atlas50.candidate.{mcsa_id.lower()}", f"{context} candidate_id differs")
        _require(case["candidate_id"] == panel_row["candidate_id"], f"{context} panel candidate_id differs")
        _require(case["label"] == frozen["label"] == panel_row["label"], f"{context} label differs")
        contract = CONTRACTS.get(case["contract_kind"])
        _require(contract is not None, f"{context} contract_kind is invalid")
        _require(case["target_operation"] in contract["operation_requirements"], f"{context} target operation is invalid for contract")
        _require(case["scope_status"] in SCOPE_STATUSES, f"{context} scope_status is invalid")
        _require(case["review_recommendation"] in REVIEW_RECOMMENDATIONS, f"{context} review recommendation is invalid")
        _string_list(case["allowed_scope"], f"{context}.allowed_scope", minimum=1)

        source_extract = _exact_keys(
            case["source_extract"],
            {"uniprot_ids", "pdb_ids", "state_catalog"},
            f"{context}.source_extract",
        )
        uniprot_ids = _string_list(source_extract["uniprot_ids"], f"{context}.source_extract.uniprot_ids", minimum=1)
        pdb_ids = _string_list(source_extract["pdb_ids"], f"{context}.source_extract.pdb_ids", minimum=1)
        _require(all(_UNIPROT_RE.fullmatch(item) for item in uniprot_ids), f"{context} contains an invalid UniProt ID")
        _require(all(_PDB_RE.fullmatch(item) for item in pdb_ids), f"{context} contains an invalid PDB ID")
        _require(set(uniprot_ids) == set(frozen["uniprot_ids"]), f"{context} invents or omits M-CSA protein identity")
        _require({item.lower() for item in pdb_ids} == set(frozen["pdb_ids"]), f"{context} invents or omits source PDB identity")
        state_index = _validate_state_catalog(source_extract["state_catalog"], evidence_ids, f"{context}.source_extract.state_catalog")

        clauses = case["clause_results"]
        _require(isinstance(clauses, list), f"{context}.clause_results must be an array")
        expected_clauses = tuple(contract["clauses"])
        _require(tuple(item.get("clause_id") for item in clauses) == expected_clauses, f"{context} clause coverage/order differs")
        for clause_index, clause in enumerate(clauses):
            clause_context = f"{context}.clause_results[{clause_index}]"
            _exact_keys(clause, {"clause_id", "status", "reason", "evidence_ids"}, clause_context)
            _require(clause["status"] in CLAUSE_STATUSES, f"{clause_context} status is invalid")
            _require(isinstance(clause["reason"], str) and clause["reason"], f"{clause_context} reason is empty")
            links = _string_list(clause["evidence_ids"], f"{clause_context}.evidence_ids")
            _require(set(links).issubset(evidence_ids), f"{clause_context} cites unknown evidence")
            if clause["status"] == "satisfied":
                _require(links, f"{clause_context} positive claim lacks evidence")

        _validate_representation(
            case["representation"],
            source_uniprot_ids=set(uniprot_ids),
            state_index=state_index,
            evidence_ids=evidence_ids,
            context=f"{context}.representation",
        )


def _contract_for_output() -> dict[str, Any]:
    return {
        kind: {
            "purpose": value["purpose"],
            "clauses": list(value["clauses"]),
            "operation_requirements": {
                operation: list(clauses)
                for operation, clauses in value["operation_requirements"].items()
            },
        }
        for kind, value in CONTRACTS.items()
    }


def _evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    contract = CONTRACTS[case["contract_kind"]]
    satisfied = [
        item["clause_id"]
        for item in case["clause_results"]
        if item["status"] == "satisfied"
    ]
    missing = [
        item["clause_id"]
        for item in case["clause_results"]
        if item["status"] == "abstained"
    ]
    satisfied_set = set(satisfied)
    allowed_operations = [
        operation
        for operation, requirements in contract["operation_requirements"].items()
        if set(requirements).issubset(satisfied_set)
    ]
    if case["target_operation"] not in allowed_operations:
        disposition = "ABSTAIN"
    elif case["scope_status"] == "source_narrowed" or missing:
        disposition = "SCOPED_PASS"
    else:
        disposition = "PASS"
    mandatory_abstentions = [
        {
            "clause_id": item["clause_id"],
            "reason": item["reason"],
        }
        for item in case["clause_results"]
        if item["status"] == "abstained"
    ]
    return {
        "candidate_id": case["candidate_id"],
        "mcsa_id": case["mcsa_id"],
        "label": case["label"],
        "contract_kind": case["contract_kind"],
        "target_operation": case["target_operation"],
        "scope_status": case["scope_status"],
        "disposition": disposition,
        "review_recommendation": case["review_recommendation"],
        "allowed_operations": allowed_operations,
        "allowed_scope": case["allowed_scope"],
        "satisfied_clauses": satisfied,
        "missing_clauses": missing,
        "mandatory_abstentions": mandatory_abstentions,
        "evidence_ids": sorted(
            {
                evidence_id
                for item in case["clause_results"]
                for evidence_id in item["evidence_ids"]
            }
        ),
        "source_extract": case["source_extract"],
        "representation": case["representation"],
    }


def _v3_compatibility(
    schema: dict[str, Any], atlas3_kernel: dict[str, Any], atlas10_kernel: dict[str, Any]
) -> dict[str, Any]:
    properties = schema["properties"]
    reaction = schema["$defs"]["reaction"]
    participant = schema["$defs"]["participant"]
    proposal = schema["$defs"]["mechanism_proposal"]
    _require(schema.get("additionalProperties") is False, "v3 must remain closed-world for this audit")
    _require(reaction["properties"]["source_id"].get("const") == "Rhea", "v3 reaction source boundary changed")
    _require(proposal["properties"]["components_summary"].get("type") == "string", "v3 component summary is no longer prose-only")
    missing = [field for field in sorted(REPRESENTATION_FIELDS) if field not in properties]
    _require(missing == sorted(REPRESENTATION_FIELDS), "v3 unexpectedly contains state-probe fields")
    return {
        "status": "sidecar_probe_requires_schema_decision_before_kernel_compilation",
        "available_boundary_fields": [
            "biological_scope.uniprot_ids",
            "reaction.participants",
            "mechanism_proposals.components_summary",
            "uncertainties",
            "detail_abstention",
            "claim_boundary",
        ],
        "missing_structured_fields": missing,
        "verified_constraints": [
            "The v3 top-level object rejects undeclared properties.",
            "The v3 reaction source is fixed to Rhea.",
            f"The v3 participant identifier pattern is {participant['properties']['participant_id']['pattern']} and cannot encode M0970 placeholder X00676.",
            "The v3 component summary is prose, so it cannot preserve typed component/state applicability by itself.",
        ],
        "kernel_evidence": {
            "atlas3": {
                "kernel_schema_version": atlas3_kernel["schema_version"],
                "record_schema_versions": sorted(
                    {record["schema_version"] for record in atlas3_kernel["records"]}
                ),
                "case_count": atlas3_kernel["case_count"],
                "record_count": atlas3_kernel["record_count"],
            },
            "atlas10": {
                "kernel_schema_version": atlas10_kernel["schema_version"],
                "record_schema_versions": sorted(
                    {
                        record["schema_version"]
                        for record in atlas10_kernel["follow_on_records"]
                    }
                ),
                "case_count": atlas10_kernel["case_count"],
                "record_count": atlas10_kernel["record_count"],
            },
        },
    }


def build_state_probe(
    spec: dict[str, Any],
    *,
    candidate_spec: dict[str, Any],
    panel_review: dict[str, Any],
    mechanism_v3_schema: dict[str, Any],
    atlas3_kernel: dict[str, Any],
    atlas10_kernel: dict[str, Any],
    basis_inputs: dict[str, str],
    batch: DraftBatchPaths = DEFAULT_BATCH,
) -> dict[str, Any]:
    """Build a deterministic representation report for a declared batch."""

    validate_probe_spec(
        spec,
        candidate_spec=candidate_spec,
        panel_review=panel_review,
        batch=batch,
    )
    case_ids = declared_probe_case_ids(spec, batch=batch)
    cases = [_evaluate_case(case) for case in spec["cases"]]
    counts = Counter(case["disposition"] for case in cases)
    operation_counts = Counter(
        operation for case in cases for operation in case["allowed_operations"]
    )
    receipt_bytes = sum(item["bytes"] for item in spec["source_receipts"])
    report = {
        "schema_version": (
            REPORT_SCHEMA_VERSION
            if batch == DEFAULT_BATCH
            else SUCCESSOR_REPORT_SCHEMA_VERSION
        ),
        "report_id": (
            "atlas50.state-probe.2026-09-05"
            if batch == DEFAULT_BATCH
            else f"atlas50.state-probe.{batch.batch_id}.{spec['generated_on']}"
        ),
        "generated_on": spec["generated_on"],
        "status": "computational_development_review_not_mechanism_compilation",
        "compiler_version": COMPILER_VERSION,
        "claim_boundary": spec["claim_boundary"],
        "review_independence": spec["review_independence"],
        "basis_inputs": basis_inputs,
        "spec_sha256": canonical_sha256(spec),
        "contract": _contract_for_output(),
        "v3_compatibility": _v3_compatibility(
            mechanism_v3_schema, atlas3_kernel, atlas10_kernel
        ),
        "external_source_checks": {
            "response_bytes": receipt_bytes,
            "limit_bytes": 30 * 1024 * 1024,
            "gpu_hours": 0,
            "raw_source_bodies_committed": any(
                receipt["raw_response_committed"]
                for receipt in spec["source_receipts"]
            ),
            "receipts": spec["source_receipts"],
        },
        "case_count": len(cases),
        "summary": {
            "disposition_counts": {
                disposition: counts[disposition] for disposition in DISPOSITIONS
            },
            "allowed_operation_counts": dict(sorted(operation_counts.items())),
            "full_panel_review_recovered": False,
            "mechanisms_compiled": 0,
            "frozen_artifacts_modified": False,
        },
        "evidence": spec["evidence"],
        "cases": cases,
    }
    if batch != DEFAULT_BATCH:
        report["declared_case_ids"] = list(case_ids)
        report["inheritance"] = spec["inheritance"]
    return report


def validate_successor_probe_inheritance(
    spec: dict[str, Any],
    report: dict[str, Any],
    *,
    repo_root: str | Path,
    batch: DraftBatchPaths,
) -> None:
    """Verify that a successor carries the pinned legacy cases unchanged."""

    if batch == DEFAULT_BATCH:
        return
    root = Path(repo_root)
    inheritance = spec["inheritance"]
    base_spec_path = root / DEFAULT_BATCH.probe_spec_path
    base_report_path = root / DEFAULT_BATCH.probe_report_path
    _require(
        file_sha256(base_spec_path) == inheritance["probe_spec_sha256"],
        "successor legacy probe-spec pin differs",
    )
    _require(
        file_sha256(base_report_path) == inheritance["probe_report_sha256"],
        "successor legacy probe-report pin differs",
    )
    base_spec = json.loads(base_spec_path.read_text(encoding="utf-8"))
    base_report = json.loads(base_report_path.read_text(encoding="utf-8"))
    inherited_count = len(inheritance["inherited_case_ids"])
    _require(
        spec["cases"][:inherited_count] == base_spec["cases"],
        "successor changed an inherited probe-spec case",
    )
    _require(
        report["cases"][:inherited_count] == base_report["cases"],
        "successor changed an inherited probe-report case",
    )


def validate_state_probe(
    report: dict[str, Any],
    *,
    spec: dict[str, Any],
    candidate_spec: dict[str, Any],
    panel_review: dict[str, Any],
    mechanism_v3_schema: dict[str, Any],
    atlas3_kernel: dict[str, Any],
    atlas10_kernel: dict[str, Any],
    basis_inputs: dict[str, str],
    batch: DraftBatchPaths = DEFAULT_BATCH,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate a report by rebuilding it from the source-bound spec."""

    expected = build_state_probe(
        spec,
        candidate_spec=candidate_spec,
        panel_review=panel_review,
        mechanism_v3_schema=mechanism_v3_schema,
        atlas3_kernel=atlas3_kernel,
        atlas10_kernel=atlas10_kernel,
        basis_inputs=basis_inputs,
        batch=batch,
    )
    _require(report == expected, "state probe differs from deterministic source-bound build")
    if batch != DEFAULT_BATCH and repo_root is not None:
        validate_successor_probe_inheritance(
            spec, report, repo_root=repo_root, batch=batch
        )
    return {
        "case_count": report["case_count"],
        **report["summary"]["disposition_counts"],
        "external_response_bytes": report["external_source_checks"]["response_bytes"],
    }
