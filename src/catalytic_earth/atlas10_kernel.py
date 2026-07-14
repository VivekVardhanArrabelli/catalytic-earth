"""Strict Atlas-10 v3 records, inherited-kernel binding, and local query runtime."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from typing import Any

from .atlas10_selection import FOLLOW_ON_CASE_IDS, validate_atlas10_selection
from .atlas_kernel import validate_atlas3_kernel


KERNEL_SCHEMA_VERSION = "catalytic-earth.atlas10-kernel.v1"
RECORD_SCHEMA_VERSION = "catalytic-earth.mechanism-record.v3"
COMPILER_VERSION = "catalytic-earth.atlas10-compiler.v1"
RUNTIME_SCHEMA_VERSION = "catalytic-earth.atlas10-runtime-result.v1"
OBJECT_TIERS = {
    "reaction_or_source_gap": 0,
    "source_annotation": 1,
    "mechanism_hypothesis": 2,
}
OBJECT_STATUSES = {
    "reaction_or_source_gap": {"source_assertion", "documented_source_gap"},
    "source_annotation": {
        "curated_source_annotation",
        "curated_non_detailed_annotation",
    },
    "mechanism_hypothesis": {
        "bounded_hypothesis",
        "bounded_non_detailed_hypothesis",
    },
}
RECORD_FIELDS = {
    "biological_scope",
    "case_id",
    "claim_boundary",
    "counterevidence",
    "detail_abstention",
    "evidence",
    "evidence_tier",
    "fixture_only",
    "label",
    "mechanism_granularity",
    "mechanism_proposals",
    "object_type",
    "provenance",
    "reaction",
    "record_id",
    "schema_version",
    "sites",
    "status",
    "structures",
    "uncertainties",
}
SCOPE_FIELDS = {
    "assay_candidate",
    "case_label",
    "direct_pdb_ids",
    "ec_number",
    "fingerprint_bridge",
    "fold_classification_ids",
    "organism",
    "relationship_group_ids",
    "uniprot_ids",
}
REACTION_FIELDS = {
    "directionality",
    "ec_number",
    "equation",
    "gap_context",
    "participants",
    "source_id",
    "source_query",
    "source_record_id",
    "source_status",
}
PARTICIPANT_FIELDS = {
    "name",
    "participant_id",
    "participant_type",
    "reactive_part_id",
    "side",
    "source_accession",
    "source_count_values",
    "source_row_count",
    "source_scope",
    "stoichiometry",
}
PROPOSAL_FIELDS = {
    "annotation_texts",
    "components_summary",
    "is_detailed",
    "mechanism_steps",
    "mechanism_text",
    "preferred",
    "proposal_id",
    "proposal_scope",
    "rating",
    "scheme_retrieval_issues",
    "source_id",
    "source_mechanism_id",
    "source_record_id",
    "structured_detail_status",
    "terminal_state_source_step_ids",
}
STEP_FIELDS = {
    "atom_mapping_status",
    "bond_edit_status",
    "catalyst_site_ids",
    "electron_flow_semantics",
    "electron_flows",
    "evidence_ids",
    "is_inferred",
    "order",
    "source_scheme_sha256",
    "source_step_id",
    "step_id",
    "summary",
}
FLOW_FIELDS = {"flow_id", "ordering_semantics", "source_point", "target_point"}
POINT_FIELDS = {"atoms", "point_kind"}
ATOM_FIELDS = {"element", "formal_charge", "semantic_labels", "source_atom_ref"}
SITE_FIELDS = {
    "evidence_ids",
    "mapping_status",
    "notes",
    "numbering_system",
    "pdb_mappings",
    "residue_name",
    "roles",
    "sequence_position",
    "site_id",
    "uniprot_id",
}
MAPPING_FIELDS = {
    "applicability",
    "author_position",
    "chain_id",
    "label_position",
    "mapping_basis",
    "numbering_note",
    "pdb_id",
}
STRUCTURE_FIELDS = {
    "applicability",
    "context_flags",
    "evidence_ids",
    "experimental_method",
    "limitation",
    "pdb_id",
    "resolution_angstrom",
    "uniprot_chain_ranges",
}
EVIDENCE_FIELDS = {
    "applicability",
    "evidence_id",
    "evidence_role",
    "retrieval_status",
    "snapshot_sha256",
    "source_id",
    "source_record_id",
    "uri",
}
COUNTER_FIELDS = {
    "counterevidence_id",
    "disposition",
    "effect",
    "evidence_ids",
    "summary",
}
UNCERTAINTY_FIELDS = {"abstention", "status", "summary", "uncertainty_id"}
ABSTENTION_FIELDS = {
    "reason",
    "required",
    "source_basis_evidence_ids",
    "unsupported_fields",
}
BOUNDARY_FIELDS = {"does_not_support", "supports"}
PROVENANCE_FIELDS = {
    "compilation_spec_sha256",
    "compiler_version",
    "selection_sha256",
    "source_snapshot_set_sha256",
}


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _exact(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{context} keys differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    return value


def _string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string")
    return value


def _strings(value: Any, context: str, *, allow_empty: bool = True) -> list[str]:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item.strip() for item in value)
        or len(value) != len(set(value))
    ):
        qualifier = "non-empty " if not allow_empty else ""
        raise ValueError(f"{context} must be a unique {qualifier}string list")
    return value


def _positive_int(value: Any, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{context} must be a positive integer")
    return value


def _sha(value: Any, context: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{context} must be a lowercase SHA-256")
    return value


def _source_key(raw: str) -> tuple[str, str]:
    if not isinstance(raw, str) or "::" not in raw:
        raise ValueError(f"invalid source key: {raw!r}")
    source_id, record_id = raw.split("::", 1)
    if not source_id or not record_id:
        raise ValueError(f"invalid source key: {raw!r}")
    return source_id, record_id


def _evidence_id(source_id: str, record_id: str) -> str:
    return f"source:{source_id}:{record_id}"


def validate_atlas10_compilation_spec(
    value: Any,
    *,
    selection: dict[str, Any],
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    spec = _exact(
        value,
        {
            "cases",
            "claim_boundary",
            "compilation_policies",
            "compiler_version",
            "inherited_kernel",
            "record_schema_version",
            "relationships",
            "schema_version",
            "selection_sha256",
            "source_snapshot_set_sha256",
        },
        "compilation_spec",
    )
    selection_summary = validate_atlas10_selection(selection)
    if spec["schema_version"] != "catalytic-earth.atlas10-compilation-spec.v1":
        raise ValueError("unsupported Atlas-10 compilation spec")
    if spec["compiler_version"] != COMPILER_VERSION:
        raise ValueError("compilation spec compiler version differs")
    if spec["record_schema_version"] != RECORD_SCHEMA_VERSION:
        raise ValueError("compilation spec record schema differs")
    if spec["selection_sha256"] != selection_summary["selection_sha256"]:
        raise ValueError("compilation spec is not bound to the frozen selection")
    if spec["source_snapshot_set_sha256"] != source_manifest["snapshot_set_sha256"]:
        raise ValueError("compilation spec is not bound to the source package")
    inherited = _exact(
        spec["inherited_kernel"],
        {"case_count", "file_sha256", "immutable", "path", "record_count", "schema_version"},
        "compilation_spec.inherited_kernel",
    )
    if inherited != {
        "path": "data/atlas/atlas3/kernel.json",
        "file_sha256": "0733a029b3eaa0900ff4124276c2060f94204ce3f3bf0b9bcf2c80e7589d674b",
        "schema_version": "catalytic-earth.atlas3-kernel.v1",
        "case_count": 3,
        "record_count": 9,
        "immutable": True,
    }:
        raise ValueError("compilation spec inherited Atlas-3 binding differs")
    policies = spec["compilation_policies"]
    if not isinstance(policies, dict) or len(policies) < 8:
        raise ValueError("compilation spec policies are incomplete")
    for key, text in policies.items():
        _string(key, "compilation policy key")
        _string(text, f"compilation_policies.{key}")
    cases = spec["cases"]
    if not isinstance(cases, list) or len(cases) != 7:
        raise ValueError("compilation spec requires seven follow-on cases")
    expected_case_ids = [case["case_id"] for case in selection["follow_on_cases"]]
    if [case.get("case_id") for case in cases] != expected_case_ids:
        raise ValueError("compilation spec case order differs from selection")
    expected_case_fields = {
        "case_id",
        "expected_granularity",
        "expected_ratings",
        "hypothesis_policy",
        "mcsa_record_id",
        "mechanism_ids",
        "preferred_mechanism_ids",
        "reaction_policy",
        "structure_contexts",
        "structured_chemistry_policy",
    }
    for index, case in enumerate(cases):
        item = _exact(case, expected_case_fields, f"compilation_spec.cases[{index}]")
        mechanism_ids = item["mechanism_ids"]
        preferred_ids = item["preferred_mechanism_ids"]
        if (
            not isinstance(mechanism_ids, list)
            or not mechanism_ids
            or any(not isinstance(identifier, int) or identifier <= 0 for identifier in mechanism_ids)
            or len(mechanism_ids) != len(set(mechanism_ids))
        ):
            raise ValueError(f"compilation_spec.cases[{index}].mechanism_ids are invalid")
        if not isinstance(preferred_ids, list) or not preferred_ids or not set(
            preferred_ids
        ).issubset(mechanism_ids):
            raise ValueError(f"compilation_spec.cases[{index}].preferred mechanisms differ")
        ratings = item["expected_ratings"]
        if not isinstance(ratings, dict) or set(ratings) != {str(value) for value in mechanism_ids}:
            raise ValueError(f"compilation_spec.cases[{index}].expected ratings differ")
        for rating in ratings.values():
            if not isinstance(rating, int) or isinstance(rating, bool) or not 0 <= rating <= 3:
                raise ValueError(f"compilation_spec.cases[{index}] has an invalid rating")
        selected = selection["follow_on_cases"][index]
        if item["mcsa_record_id"] != selected["source_mechanism_contract"]["mcsa_record_id"]:
            raise ValueError(f"compilation_spec.cases[{index}] M-CSA record differs")
        structures = item["structure_contexts"]
        expected_pdb = {
            handle["record_id"]: handle["applicability"]
            for handle in selected["source_handles"]
            if handle["source_id"] == "PDB"
        }
        if not isinstance(structures, list) or {
            context.get("pdb_id"): context.get("applicability") for context in structures
        } != expected_pdb:
            raise ValueError(f"compilation_spec.cases[{index}] structure contexts differ")
        for structure_index, context in enumerate(structures):
            structure = _exact(
                context,
                {"applicability", "context_flags", "limitation", "pdb_id"},
                f"compilation_spec.cases[{index}].structure_contexts[{structure_index}]",
            )
            _strings(structure["context_flags"], "structure context flags", allow_empty=False)
            _string(structure["limitation"], "structure context limitation")
    relationships = spec["relationships"]
    if not isinstance(relationships, list) or len(relationships) != 2:
        raise ValueError("compilation spec must define two relationships")
    selected_groups = {item["group_id"]: item for item in selection["relationship_groups"]}
    for index, relationship in enumerate(relationships):
        item = _exact(
            relationship,
            {
                "case_ids",
                "comparison_boundary",
                "group_id",
                "member_distinctions",
                "relationship_type",
                "shared_features",
            },
            f"compilation_spec.relationships[{index}]",
        )
        selected = selected_groups.get(item["group_id"])
        if selected is None or item["relationship_type"] != selected["relationship_type"]:
            raise ValueError("compilation relationship identity differs from selection")
        if item["case_ids"] != selected["case_ids"]:
            raise ValueError("compilation relationship members differ from selection")
        for feature in [*item["shared_features"], *item["member_distinctions"]]:
            if not isinstance(feature, dict):
                raise ValueError("relationship feature must be an object")
            for source_key in feature.get("evidence_keys", []):
                _source_key(source_key)
    boundary = _exact(spec["claim_boundary"], BOUNDARY_FIELDS, "compilation_spec.claim_boundary")
    _strings(boundary["supports"], "compilation_spec.claim_boundary.supports", allow_empty=False)
    _strings(
        boundary["does_not_support"],
        "compilation_spec.claim_boundary.does_not_support",
        allow_empty=False,
    )
    return {
        "schema_version": spec["schema_version"],
        "case_count": 7,
        "relationship_count": 2,
        "compilation_spec_sha256": canonical_sha256(spec),
    }


def _validate_claim_boundary(value: Any, context: str) -> None:
    boundary = _exact(value, BOUNDARY_FIELDS, context)
    _strings(boundary["supports"], f"{context}.supports", allow_empty=False)
    _strings(boundary["does_not_support"], f"{context}.does_not_support", allow_empty=False)


def _validate_reaction(value: Any, context: str) -> None:
    reaction = _exact(value, REACTION_FIELDS, context)
    if reaction["source_id"] != "Rhea":
        raise ValueError(f"{context}.source_id must be Rhea")
    status = reaction["source_status"]
    if status not in {"direct_record", "documented_query_gap"}:
        raise ValueError(f"{context}.source_status is unsupported")
    _string(reaction["source_query"], f"{context}.source_query")
    _string(reaction["ec_number"], f"{context}.ec_number")
    if status == "direct_record":
        _string(reaction["source_record_id"], f"{context}.source_record_id")
        _string(reaction["equation"], f"{context}.equation")
        if reaction["directionality"] != "undirected" or reaction["gap_context"] is not None:
            raise ValueError(f"{context} direct-record fields differ")
    else:
        if (
            reaction["source_record_id"] is not None
            or reaction["equation"] is not None
            or reaction["directionality"] != "unknown_no_direct_record"
        ):
            raise ValueError(f"{context} gap fields differ")
        gap = _exact(
            reaction["gap_context"],
            {"interpretation", "query_result_count", "query_snapshot_kind"},
            f"{context}.gap_context",
        )
        if gap["query_result_count"] != 0 or gap["query_snapshot_kind"] != "official_zero_row_tsv":
            raise ValueError(f"{context}.gap_context differs")
        _string(gap["interpretation"], f"{context}.gap_context.interpretation")
    participants = reaction["participants"]
    if not isinstance(participants, list) or len(participants) < 2:
        raise ValueError(f"{context}.participants must contain source-scoped participants")
    participant_keys: set[tuple[str, str]] = set()
    for index, raw in enumerate(participants):
        participant = _exact(raw, PARTICIPANT_FIELDS, f"{context}.participants[{index}]")
        identifier = _string(
            participant["participant_id"], f"{context}.participants[{index}].participant_id"
        )
        if not identifier.startswith(("CHEBI:", "RHEA-COMP:")):
            raise ValueError(f"{context}.participants[{index}] identifier is unsupported")
        _string(participant["name"], f"{context}.participants[{index}].name")
        _string(participant["source_scope"], f"{context}.participants[{index}].source_scope")
        _string(
            participant["source_accession"],
            f"{context}.participants[{index}].source_accession",
        )
        if participant["side"] not in {"left", "right"}:
            raise ValueError(f"{context}.participants[{index}].side differs")
        _positive_int(participant["stoichiometry"], f"{context}.participants[{index}].stoichiometry")
        _positive_int(
            participant["source_row_count"], f"{context}.participants[{index}].source_row_count"
        )
        counts = participant["source_count_values"]
        if not isinstance(counts, list) or not counts or any(
            not isinstance(item, int) or item <= 0 for item in counts
        ):
            raise ValueError(f"{context}.participants[{index}].source_count_values differ")
        if len(counts) != participant["source_row_count"]:
            raise ValueError(f"{context}.participants[{index}] source row counts disagree")
        if participant["reactive_part_id"] is not None:
            reactive = _string(
                participant["reactive_part_id"],
                f"{context}.participants[{index}].reactive_part_id",
            )
            if not reactive.startswith("CHEBI:"):
                raise ValueError(f"{context}.participants[{index}] reactive part differs")
        key = identifier, participant["side"]
        if key in participant_keys:
            raise ValueError(f"{context}.participants repeats {key}")
        participant_keys.add(key)


def _validate_flows(value: Any, context: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{context} must preserve at least one source electron flow")
    flow_ids: set[str] = set()
    for index, raw in enumerate(value):
        flow = _exact(raw, FLOW_FIELDS, f"{context}[{index}]")
        flow_id = _string(flow["flow_id"], f"{context}[{index}].flow_id")
        if flow_id in flow_ids:
            raise ValueError(f"{context} repeats {flow_id}")
        flow_ids.add(flow_id)
        if flow["ordering_semantics"] != "source_file_order_not_independently_inferred":
            raise ValueError(f"{context}[{index}] ordering semantics differ")
        for point_name in ("source_point", "target_point"):
            point = _exact(flow[point_name], POINT_FIELDS, f"{context}[{index}].{point_name}")
            if point["point_kind"] not in {"electron_base_atom", "atom_set"}:
                raise ValueError(f"{context}[{index}].{point_name}.point_kind differs")
            atoms = point["atoms"]
            if not isinstance(atoms, list) or not atoms:
                raise ValueError(f"{context}[{index}].{point_name}.atoms must be non-empty")
            for atom_index, raw_atom in enumerate(atoms):
                atom = _exact(
                    raw_atom,
                    ATOM_FIELDS,
                    f"{context}[{index}].{point_name}.atoms[{atom_index}]",
                )
                _string(atom["source_atom_ref"], "source atom reference")
                _string(atom["element"], "source atom element")
                if atom["formal_charge"] is not None and not isinstance(
                    atom["formal_charge"], int
                ):
                    raise ValueError("source atom formal charge must be integer or null")
                _strings(atom["semantic_labels"], "source atom semantic labels")


def _validate_proposals(
    value: Any,
    *,
    object_type: str,
    evidence_ids: set[str],
    site_ids: set[str],
    context: str,
) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{context} must be a list")
    if object_type != "reaction_or_source_gap" and not value:
        raise ValueError(f"{context} must preserve its source annotation")
    proposal_ids: set[str] = set()
    for proposal_index, raw in enumerate(value):
        proposal_context = f"{context}[{proposal_index}]"
        proposal = _exact(raw, PROPOSAL_FIELDS, proposal_context)
        proposal_id = _string(proposal["proposal_id"], f"{proposal_context}.proposal_id")
        if proposal_id in proposal_ids:
            raise ValueError(f"{context} repeats {proposal_id}")
        proposal_ids.add(proposal_id)
        if proposal["source_id"] != "M-CSA":
            raise ValueError(f"{proposal_context}.source_id must be M-CSA")
        source_record_id = _string(
            proposal["source_record_id"], f"{proposal_context}.source_record_id"
        )
        if _evidence_id("M-CSA", source_record_id) not in evidence_ids:
            raise ValueError(f"{proposal_context} lacks M-CSA evidence")
        _positive_int(proposal["source_mechanism_id"], f"{proposal_context}.source_mechanism_id")
        if not isinstance(proposal["rating"], int) or not 0 <= proposal["rating"] <= 3:
            raise ValueError(f"{proposal_context}.rating differs")
        if not isinstance(proposal["is_detailed"], bool) or not isinstance(
            proposal["preferred"], bool
        ):
            raise ValueError(f"{proposal_context} booleans differ")
        expected_scope = (
            "source_curated"
            if object_type == "source_annotation"
            else "bounded_hypothesis_projection"
        )
        if proposal["proposal_scope"] != expected_scope:
            raise ValueError(f"{proposal_context}.proposal_scope differs")
        _string(proposal["components_summary"], f"{proposal_context}.components_summary")
        _string(proposal["mechanism_text"], f"{proposal_context}.mechanism_text")
        _strings(proposal["annotation_texts"], f"{proposal_context}.annotation_texts")
        terminals = proposal["terminal_state_source_step_ids"]
        if not isinstance(terminals, list) or any(
            not isinstance(item, int) or item <= 0 for item in terminals
        ) or len(terminals) != len(set(terminals)):
            raise ValueError(f"{proposal_context}.terminal states differ")
        issues = proposal["scheme_retrieval_issues"]
        if not isinstance(issues, list):
            raise ValueError(f"{proposal_context}.scheme_retrieval_issues must be a list")
        steps = proposal["mechanism_steps"]
        if not proposal["is_detailed"]:
            if (
                steps
                or not proposal["annotation_texts"]
                or proposal["structured_detail_status"] != "abstained_non_detailed_source"
            ):
                raise ValueError(f"{proposal_context} fabricates detail for a non-detailed source")
            if len(issues) != 1 or issues[0].get("status") != "source_link_missing_http_404":
                raise ValueError(f"{proposal_context} does not preserve its missing source scheme")
            continue
        if proposal["structured_detail_status"] != (
            "source_curved_arrows_preserved_no_atom_mapping_inference"
        ) or issues:
            raise ValueError(f"{proposal_context} detailed-source status differs")
        if not isinstance(steps, list) or not steps:
            raise ValueError(f"{proposal_context} detailed source has no steps")
        step_ids: set[str] = set()
        for step_index, raw_step in enumerate(steps):
            step_context = f"{proposal_context}.mechanism_steps[{step_index}]"
            step = _exact(raw_step, STEP_FIELDS, step_context)
            step_id = _string(step["step_id"], f"{step_context}.step_id")
            if step_id in step_ids or step["order"] != step_index + 1:
                raise ValueError(f"{proposal_context} step IDs/order differ")
            step_ids.add(step_id)
            _string(step["summary"], f"{step_context}.summary")
            _positive_int(step["source_step_id"], f"{step_context}.source_step_id")
            if not isinstance(step["is_inferred"], bool):
                raise ValueError(f"{step_context}.is_inferred must be boolean")
            catalysts = _strings(step["catalyst_site_ids"], f"{step_context}.catalyst_site_ids")
            if not set(catalysts).issubset(site_ids):
                raise ValueError(f"{step_context}.catalyst sites do not resolve")
            step_evidence = _strings(
                step["evidence_ids"], f"{step_context}.evidence_ids", allow_empty=False
            )
            if not set(step_evidence).issubset(evidence_ids):
                raise ValueError(f"{step_context}.evidence does not resolve")
            _sha(step["source_scheme_sha256"], f"{step_context}.source_scheme_sha256")
            _validate_flows(step["electron_flows"], f"{step_context}.electron_flows")
            if step["electron_flow_semantics"] != (
                "source_ordered_curved_arrow_endpoints_not_atom_mapped_bond_edits"
            ):
                raise ValueError(f"{step_context}.electron flow semantics differ")
            if step["atom_mapping_status"] != "not_inferred" or step[
                "bond_edit_status"
            ] != "not_compiled_from_unmapped_source_scheme":
                raise ValueError(f"{step_context} overclaims structured chemistry")


def _validate_record(
    value: Any,
    index: int,
    *,
    wrapper: dict[str, Any],
    manifest_records: dict[tuple[str, str], dict[str, Any]],
    manifest_bindings: dict[tuple[str, str, str], dict[str, Any]],
) -> None:
    context = f"kernel.follow_on_records[{index}]"
    record = _exact(value, RECORD_FIELDS, context)
    if record["schema_version"] != RECORD_SCHEMA_VERSION:
        raise ValueError(f"{context}.schema_version differs")
    _string(record["record_id"], f"{context}.record_id")
    case_id = record["case_id"]
    if case_id not in FOLLOW_ON_CASE_IDS:
        raise ValueError(f"{context}.case_id is outside the follow-on set")
    object_type = record["object_type"]
    if object_type not in OBJECT_TIERS or record["evidence_tier"] != OBJECT_TIERS[object_type]:
        raise ValueError(f"{context}.object type/tier differ")
    if record["status"] not in OBJECT_STATUSES[object_type]:
        raise ValueError(f"{context}.status differs from its object type")
    _string(record["label"], f"{context}.label")
    if record["fixture_only"] is not False:
        raise ValueError(f"{context} cannot be a fixture")
    if record["mechanism_granularity"] not in {
        "not_applicable",
        "detailed",
        "detailed_with_alternatives",
        "non_detailed",
    }:
        raise ValueError(f"{context}.mechanism_granularity differs")

    scope = _exact(record["biological_scope"], SCOPE_FIELDS, f"{context}.biological_scope")
    for field in ("case_label", "organism", "ec_number"):
        _string(scope[field], f"{context}.biological_scope.{field}")
    for field in (
        "uniprot_ids",
        "direct_pdb_ids",
        "fold_classification_ids",
    ):
        _strings(scope[field], f"{context}.biological_scope.{field}", allow_empty=False)
    _strings(scope["relationship_group_ids"], f"{context}.biological_scope.relationship_group_ids")
    if scope["assay_candidate"] is not False:
        raise ValueError(f"{context} cannot start a new assay")
    bridge = _exact(
        scope["fingerprint_bridge"],
        {"fingerprint_id", "registry_write", "use"},
        f"{context}.biological_scope.fingerprint_bridge",
    )
    if bridge["use"] != "historical_crosswalk_only_not_evidence" or bridge[
        "registry_write"
    ] is not False:
        raise ValueError(f"{context} fingerprint bridge enters the evidence chain")
    _validate_reaction(record["reaction"], f"{context}.reaction")

    evidence = record["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ValueError(f"{context}.evidence must be non-empty")
    evidence_ids: set[str] = set()
    for evidence_index, raw in enumerate(evidence):
        evidence_context = f"{context}.evidence[{evidence_index}]"
        item = _exact(raw, EVIDENCE_FIELDS, evidence_context)
        evidence_id = _string(item["evidence_id"], f"{evidence_context}.evidence_id")
        if evidence_id in evidence_ids:
            raise ValueError(f"{context}.evidence repeats {evidence_id}")
        evidence_ids.add(evidence_id)
        key = item["source_id"], item["source_record_id"]
        source_record = manifest_records.get(key)
        binding = manifest_bindings.get((case_id, *key))
        if source_record is None or binding is None:
            raise ValueError(f"{evidence_context} is absent from the case source surface")
        expected = {
            "evidence_id": _evidence_id(*key),
            "source_id": key[0],
            "source_record_id": key[1],
            "evidence_role": binding["evidence_role"],
            "applicability": binding["applicability"],
            "uri": source_record["uri"],
            "retrieval_status": source_record["retrieval_status"],
            "snapshot_sha256": source_record["snapshot_sha256"],
        }
        if item != expected:
            raise ValueError(f"{evidence_context} differs from source manifest/binding")

    sites = record["sites"]
    if not isinstance(sites, list):
        raise ValueError(f"{context}.sites must be a list")
    site_ids: set[str] = set()
    for site_index, raw in enumerate(sites):
        site_context = f"{context}.sites[{site_index}]"
        site = _exact(raw, SITE_FIELDS, site_context)
        site_id = _string(site["site_id"], f"{site_context}.site_id")
        if site_id in site_ids:
            raise ValueError(f"{context}.sites repeats {site_id}")
        site_ids.add(site_id)
        for field in ("uniprot_id", "residue_name", "notes"):
            _string(site[field], f"{site_context}.{field}")
        _positive_int(site["sequence_position"], f"{site_context}.sequence_position")
        if site["numbering_system"] != "UniProt natural sequence" or site[
            "mapping_status"
        ] != "source_and_coordinate_verified":
            raise ValueError(f"{site_context} numbering/mapping status differ")
        # M-CSA can identify a catalytic-context residue without assigning a
        # role string.  Preserve that absence instead of manufacturing a role.
        _strings(site["roles"], f"{site_context}.roles")
        site_evidence = _strings(
            site["evidence_ids"], f"{site_context}.evidence_ids", allow_empty=False
        )
        if not set(site_evidence).issubset(evidence_ids):
            raise ValueError(f"{site_context}.evidence does not resolve")
        mappings = site["pdb_mappings"]
        if not isinstance(mappings, list) or not mappings:
            raise ValueError(f"{site_context}.pdb_mappings must be non-empty")
        mapping_keys: set[tuple[str, str]] = set()
        for mapping_index, raw_mapping in enumerate(mappings):
            mapping = _exact(
                raw_mapping,
                MAPPING_FIELDS,
                f"{site_context}.pdb_mappings[{mapping_index}]",
            )
            key = (
                _string(mapping["pdb_id"], "PDB mapping identifier"),
                _string(mapping["chain_id"], "PDB mapping chain"),
            )
            if key in mapping_keys:
                raise ValueError(f"{site_context}.pdb_mappings repeats {key}")
            mapping_keys.add(key)
            _positive_int(mapping["author_position"], "PDB mapping author position")
            _positive_int(mapping["label_position"], "PDB mapping label position")
            if mapping["applicability"] not in {"direct", "engineered_source_reference"}:
                raise ValueError(f"{site_context} mapping applicability differs")
            if mapping["mapping_basis"] not in {
                "mcsa_reference_and_coordinate",
                "uniprot_chain_range_and_coordinate",
            }:
                raise ValueError(f"{site_context} mapping basis differs")
            _string(mapping["numbering_note"], "PDB mapping numbering note")

    structures = record["structures"]
    if not isinstance(structures, list):
        raise ValueError(f"{context}.structures must be a list")
    structure_ids: set[str] = set()
    for structure_index, raw in enumerate(structures):
        structure_context = f"{context}.structures[{structure_index}]"
        structure = _exact(raw, STRUCTURE_FIELDS, structure_context)
        pdb_id = _string(structure["pdb_id"], f"{structure_context}.pdb_id")
        if pdb_id in structure_ids:
            raise ValueError(f"{context}.structures repeats {pdb_id}")
        structure_ids.add(pdb_id)
        if structure["applicability"] not in {"direct", "engineered_source_reference"}:
            raise ValueError(f"{structure_context}.applicability differs")
        _strings(structure["context_flags"], f"{structure_context}.context_flags", allow_empty=False)
        _string(structure["limitation"], f"{structure_context}.limitation")
        if structure["experimental_method"] is not None:
            _string(structure["experimental_method"], f"{structure_context}.experimental_method")
        if structure["resolution_angstrom"] is not None and (
            not isinstance(structure["resolution_angstrom"], (int, float))
            or structure["resolution_angstrom"] <= 0
        ):
            raise ValueError(f"{structure_context}.resolution differs")
        ranges = structure["uniprot_chain_ranges"]
        if not isinstance(ranges, list):
            raise ValueError(f"{structure_context}.uniprot_chain_ranges must be a list")
        structure_evidence = _strings(
            structure["evidence_ids"], f"{structure_context}.evidence_ids", allow_empty=False
        )
        if not set(structure_evidence).issubset(evidence_ids):
            raise ValueError(f"{structure_context}.evidence does not resolve")

    _validate_proposals(
        record["mechanism_proposals"],
        object_type=object_type,
        evidence_ids=evidence_ids,
        site_ids=site_ids,
        context=f"{context}.mechanism_proposals",
    )
    if object_type == "reaction_or_source_gap" and (sites or structures):
        raise ValueError(f"{context} Tier 0 cannot contain sites or structures")
    if object_type == "reaction_or_source_gap" and record["mechanism_granularity"] != (
        "not_applicable"
    ):
        raise ValueError(f"{context} Tier 0 mechanism granularity differs")

    for collection_name, fields, id_field in (
        ("counterevidence", COUNTER_FIELDS, "counterevidence_id"),
        ("uncertainties", UNCERTAINTY_FIELDS, "uncertainty_id"),
    ):
        collection = record[collection_name]
        if not isinstance(collection, list):
            raise ValueError(f"{context}.{collection_name} must be a list")
        seen: set[str] = set()
        for item_index, raw_item in enumerate(collection):
            item_context = f"{context}.{collection_name}[{item_index}]"
            item = _exact(raw_item, fields, item_context)
            identifier = _string(item[id_field], f"{item_context}.{id_field}")
            if identifier in seen:
                raise ValueError(f"{context}.{collection_name} repeats {identifier}")
            seen.add(identifier)
            _string(item["summary"], f"{item_context}.summary")
            if collection_name == "counterevidence":
                refs = _strings(item["evidence_ids"], f"{item_context}.evidence_ids", allow_empty=False)
                if not set(refs).issubset(evidence_ids):
                    raise ValueError(f"{item_context}.evidence does not resolve")
                _string(item["effect"], f"{item_context}.effect")
                _string(item["disposition"], f"{item_context}.disposition")
            else:
                if item["status"] != "open":
                    raise ValueError(f"{item_context}.status must remain open")
                _string(item["abstention"], f"{item_context}.abstention")

    abstention = _exact(record["detail_abstention"], ABSTENTION_FIELDS, f"{context}.detail_abstention")
    if abstention["required"] is not True:
        raise ValueError(f"{context}.detail_abstention must be required")
    _string(abstention["reason"], f"{context}.detail_abstention.reason")
    _strings(
        abstention["unsupported_fields"],
        f"{context}.detail_abstention.unsupported_fields",
        allow_empty=False,
    )
    basis = _strings(
        abstention["source_basis_evidence_ids"],
        f"{context}.detail_abstention.source_basis_evidence_ids",
        allow_empty=False,
    )
    if not set(basis).issubset(evidence_ids):
        raise ValueError(f"{context}.detail_abstention evidence does not resolve")
    _validate_claim_boundary(record["claim_boundary"], f"{context}.claim_boundary")
    provenance = _exact(record["provenance"], PROVENANCE_FIELDS, f"{context}.provenance")
    expected_provenance = {
        "selection_sha256": wrapper["selection_sha256"],
        "source_snapshot_set_sha256": wrapper["source_snapshot_set_sha256"],
        "compilation_spec_sha256": wrapper["compilation_spec_sha256"],
        "compiler_version": wrapper["compiler_version"],
    }
    if provenance != expected_provenance:
        raise ValueError(f"{context}.provenance differs from wrapper")


def validate_atlas10_kernel(
    value: Any,
    *,
    selection: dict[str, Any],
    source_manifest: dict[str, Any],
    inherited_kernel: dict[str, Any] | None = None,
) -> dict[str, Any]:
    kernel = _exact(
        value,
        {
            "case_count",
            "claim_boundary",
            "compilation_spec_sha256",
            "compiler_version",
            "follow_on_case_count",
            "follow_on_record_count",
            "follow_on_records",
            "inherited_kernel",
            "record_count",
            "relationships",
            "schema_version",
            "selection_sha256",
            "source_manifest_retrieved_at",
            "source_snapshot_set_sha256",
        },
        "kernel",
    )
    if kernel["schema_version"] != KERNEL_SCHEMA_VERSION or kernel[
        "compiler_version"
    ] != COMPILER_VERSION:
        raise ValueError("unsupported Atlas-10 kernel/compiler version")
    for field in ("selection_sha256", "source_snapshot_set_sha256", "compilation_spec_sha256"):
        _sha(kernel[field], f"kernel.{field}")
    selection_summary = validate_atlas10_selection(selection)
    if kernel["selection_sha256"] != selection_summary["selection_sha256"]:
        raise ValueError("kernel is not bound to the Atlas-10 selection")
    if kernel["source_snapshot_set_sha256"] != source_manifest["snapshot_set_sha256"]:
        raise ValueError("kernel is not bound to the Atlas-10 source package")
    if kernel["source_manifest_retrieved_at"] != source_manifest["retrieved_at"]:
        raise ValueError("kernel/source manifest retrieval timestamps differ")
    inherited = _exact(
        kernel["inherited_kernel"],
        {"case_count", "file_sha256", "immutable", "path", "record_count", "schema_version"},
        "kernel.inherited_kernel",
    )
    if inherited != {
        "path": "data/atlas/atlas3/kernel.json",
        "file_sha256": "0733a029b3eaa0900ff4124276c2060f94204ce3f3bf0b9bcf2c80e7589d674b",
        "schema_version": "catalytic-earth.atlas3-kernel.v1",
        "case_count": 3,
        "record_count": 9,
        "immutable": True,
    }:
        raise ValueError("kernel inherited Atlas-3 binding differs")
    if inherited_kernel is not None:
        validate_atlas3_kernel(inherited_kernel)
        if inherited_kernel.get("case_count") != 3 or inherited_kernel.get("record_count") != 9:
            raise ValueError("inherited Atlas-3 kernel counts differ")
    if (
        kernel["case_count"] != 10
        or kernel["record_count"] != 30
        or kernel["follow_on_case_count"] != 7
        or kernel["follow_on_record_count"] != 21
    ):
        raise ValueError("Atlas-10 case/record counts differ")
    _validate_claim_boundary(kernel["claim_boundary"], "kernel.claim_boundary")

    manifest_records = {
        (record["source_id"], record["record_id"]): record
        for record in source_manifest["records"]
    }
    manifest_bindings = {
        (binding["case_id"], binding["source_id"], binding["record_id"]): binding
        for binding in source_manifest["bindings"]
    }
    records = kernel["follow_on_records"]
    if not isinstance(records, list) or len(records) != 21:
        raise ValueError("kernel.follow_on_records must contain exactly 21 objects")
    for index, record in enumerate(records):
        _validate_record(
            record,
            index,
            wrapper=kernel,
            manifest_records=manifest_records,
            manifest_bindings=manifest_bindings,
        )
    record_ids = [record["record_id"] for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Atlas-10 follow-on record IDs are not unique")
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_case[record["case_id"]].append(record)
    if tuple(by_case) != FOLLOW_ON_CASE_IDS:
        raise ValueError("Atlas-10 follow-on case order differs")
    selected_cases = {case["case_id"]: case for case in selection["follow_on_cases"]}
    source_gaps = 0
    non_detailed = 0
    source_steps = 0
    source_flows = 0
    for case_id in FOLLOW_ON_CASE_IDS:
        case_records = by_case[case_id]
        if len(case_records) != 3:
            raise ValueError(f"{case_id} must contain exactly three truth objects")
        objects = {record["object_type"]: record for record in case_records}
        if set(objects) != set(OBJECT_TIERS):
            raise ValueError(f"{case_id} object types differ")
        if any(record["reaction"] != case_records[0]["reaction"] for record in case_records[1:]):
            raise ValueError(f"{case_id} records disagree on reaction/source gap")
        if any(
            record["biological_scope"] != case_records[0]["biological_scope"]
            for record in case_records[1:]
        ):
            raise ValueError(f"{case_id} records disagree on biological scope")
        selected = selected_cases[case_id]
        hypothesis = objects["mechanism_hypothesis"]
        if hypothesis["record_id"] != selected["target_record_id"]:
            raise ValueError(f"{case_id} hypothesis record ID differs from selection")
        scope = hypothesis["biological_scope"]
        expected_scope = {
            "case_label": selected["label"],
            "organism": selected["organism"],
            "ec_number": selected["ec_number"],
            "uniprot_ids": sorted(
                handle["record_id"]
                for handle in selected["source_handles"]
                if handle["source_id"] == "UniProtKB"
            ),
            "direct_pdb_ids": sorted(
                handle["record_id"]
                for handle in selected["source_handles"]
                if handle["source_id"] == "PDB" and handle["applicability"] == "direct"
            ),
            "fold_classification_ids": selected["fold_classification_ids"],
            "relationship_group_ids": selected["relationship_group_ids"],
            "assay_candidate": False,
            "fingerprint_bridge": selected["fingerprint_bridge"],
        }
        if scope != expected_scope:
            raise ValueError(f"{case_id} biological scope differs from selection")
        reaction = hypothesis["reaction"]
        observed_participants = {
            item["participant_id"] for item in reaction["participants"]
        } | {
            item["reactive_part_id"]
            for item in reaction["participants"]
            if item["reactive_part_id"] is not None
        }
        if observed_participants != set(selected["reaction_participant_ids"]):
            raise ValueError(f"{case_id} reaction participant scope differs from selection")
        if reaction["source_status"] == "documented_query_gap":
            source_gaps += 1
        if hypothesis["mechanism_granularity"] == "non_detailed":
            non_detailed += 1
            for record in (objects["source_annotation"], hypothesis):
                if any(
                    proposal["mechanism_steps"] for proposal in record["mechanism_proposals"]
                ):
                    raise ValueError(f"{case_id} fabricates non-detailed mechanism steps")
        source_annotation = objects["source_annotation"]
        for proposal in source_annotation["mechanism_proposals"]:
            source_steps += len(proposal["mechanism_steps"])
            source_flows += sum(
                len(step["electron_flows"]) for step in proposal["mechanism_steps"]
            )
    if (source_gaps, non_detailed, source_steps, source_flows) != (3, 1, 21, 61):
        raise ValueError("Atlas-10 gap/granularity/source-chemistry counts differ")

    relationships = kernel["relationships"]
    if not isinstance(relationships, list) or len(relationships) != 2:
        raise ValueError("Atlas-10 must contain exactly two relationship projections")
    selected_relationships = {
        item["group_id"]: item for item in selection["relationship_groups"]
    }
    for index, relationship in enumerate(relationships):
        item = _exact(
            relationship,
            {
                "case_ids",
                "comparison_boundary",
                "group_id",
                "member_distinctions",
                "relationship_type",
                "shared_features",
            },
            f"kernel.relationships[{index}]",
        )
        selected = selected_relationships.get(item["group_id"])
        if selected is None or item["case_ids"] != selected["case_ids"] or item[
            "relationship_type"
        ] != selected["relationship_type"]:
            raise ValueError("kernel relationship differs from selection")
        group_evidence_ids = {
            evidence["evidence_id"]
            for case_id in item["case_ids"]
            for evidence in next(
                record
                for record in by_case[case_id]
                if record["object_type"] == "mechanism_hypothesis"
            )["evidence"]
        }
        for feature in [*item["shared_features"], *item["member_distinctions"]]:
            expected_fields = (
                {"evidence_keys", "feature_id", "label"}
                if "case_id" not in feature
                else {"case_id", "evidence_keys", "feature_id", "label", "site_ids"}
            )
            _exact(feature, expected_fields, "relationship feature")
            _string(feature["feature_id"], "relationship feature ID")
            _string(feature["label"], "relationship feature label")
            resolved_evidence = {
                _evidence_id(*_source_key(key)) for key in feature["evidence_keys"]
            }
            if not resolved_evidence.issubset(group_evidence_ids):
                raise ValueError("relationship feature evidence does not resolve")
            if "case_id" in feature:
                if feature["case_id"] not in item["case_ids"]:
                    raise ValueError("relationship member feature has the wrong case")
                hypothesis_sites = {
                    site["site_id"]
                    for site in next(
                        record
                        for record in by_case[feature["case_id"]]
                        if record["object_type"] == "mechanism_hypothesis"
                    )["sites"]
                }
                if not set(feature["site_ids"]).issubset(hypothesis_sites):
                    raise ValueError("relationship member feature sites do not resolve")
        _string(item["comparison_boundary"], "relationship comparison boundary")
    return {
        "schema_version": KERNEL_SCHEMA_VERSION,
        "case_count": 10,
        "record_count": 30,
        "follow_on_case_count": 7,
        "follow_on_record_count": 21,
        "documented_rhea_gaps": source_gaps,
        "non_detailed_abstentions": non_detailed,
        "source_mechanism_steps": source_steps,
        "source_electron_flows": source_flows,
        "relationship_count": len(relationships),
        "kernel_sha256": canonical_sha256(kernel),
    }


def materialize_atlas10_sqlite(
    kernel: dict[str, Any], inherited_kernel: dict[str, Any]
) -> sqlite3.Connection:
    """Materialize the mixed v2/v3 ten-case surface in dependency-free SQLite."""
    validate_atlas3_kernel(inherited_kernel)
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE cases (
            case_id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            organism TEXT NOT NULL,
            ec_number TEXT NOT NULL,
            generation TEXT NOT NULL,
            reaction_status TEXT NOT NULL,
            mechanism_granularity TEXT NOT NULL,
            hypothesis_record_id TEXT NOT NULL,
            fingerprint_id TEXT,
            fingerprint_use TEXT,
            registry_write INTEGER
        );
        CREATE TABLE records (
            record_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            object_type TEXT NOT NULL,
            evidence_tier INTEGER NOT NULL,
            status TEXT NOT NULL,
            schema_version TEXT NOT NULL
        );
        CREATE TABLE reactions (
            case_id TEXT PRIMARY KEY,
            source_status TEXT NOT NULL,
            source_record_id TEXT,
            source_query TEXT NOT NULL,
            equation TEXT
        );
        CREATE TABLE participants (
            case_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            reactive_part_id TEXT,
            side TEXT NOT NULL,
            name TEXT NOT NULL,
            source_scope TEXT NOT NULL,
            source_row_count INTEGER NOT NULL,
            source_count_values TEXT NOT NULL
        );
        CREATE TABLE proposals (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            proposal_id TEXT NOT NULL,
            source_mechanism_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            is_detailed INTEGER NOT NULL,
            preferred INTEGER NOT NULL,
            step_count INTEGER NOT NULL,
            electron_flow_count INTEGER NOT NULL
        );
        CREATE TABLE mechanism_steps (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            proposal_id TEXT NOT NULL,
            step_id TEXT NOT NULL,
            step_order INTEGER NOT NULL,
            summary TEXT NOT NULL,
            is_inferred INTEGER NOT NULL,
            catalyst_site_ids TEXT NOT NULL,
            electron_flow_count INTEGER NOT NULL
        );
        CREATE TABLE sites (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            site_id TEXT NOT NULL,
            residue_name TEXT NOT NULL,
            sequence_position INTEGER NOT NULL,
            roles TEXT NOT NULL,
            mappings TEXT NOT NULL
        );
        CREATE TABLE structures (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            pdb_id TEXT NOT NULL,
            applicability TEXT NOT NULL,
            context_flags TEXT NOT NULL,
            limitation TEXT NOT NULL
        );
        CREATE TABLE uncertainties (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            uncertainty_id TEXT NOT NULL,
            summary TEXT NOT NULL,
            abstention TEXT NOT NULL
        );
        CREATE TABLE counterevidence (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            counterevidence_id TEXT NOT NULL,
            summary TEXT NOT NULL,
            effect TEXT NOT NULL,
            disposition TEXT NOT NULL,
            evidence_ids TEXT NOT NULL
        );
        CREATE TABLE detail_abstentions (
            record_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            unsupported_fields TEXT NOT NULL,
            source_basis_evidence_ids TEXT NOT NULL
        );
        CREATE TABLE claim_boundaries (
            record_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            supports TEXT NOT NULL,
            does_not_support TEXT NOT NULL
        );
        CREATE TABLE provenance (
            record_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            selection_sha256 TEXT NOT NULL,
            source_snapshot_set_sha256 TEXT NOT NULL,
            compilation_spec_sha256 TEXT NOT NULL,
            compiler_version TEXT NOT NULL
        );
        CREATE TABLE folds (
            case_id TEXT NOT NULL,
            fold_classification_id TEXT NOT NULL,
            PRIMARY KEY (case_id, fold_classification_id)
        );
        CREATE TABLE evidence (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            evidence_id TEXT NOT NULL,
            applicability TEXT NOT NULL,
            evidence_role TEXT NOT NULL
        );
        CREATE TABLE relationships (
            group_id TEXT PRIMARY KEY,
            relationship_type TEXT NOT NULL,
            comparison_boundary TEXT NOT NULL
        );
        CREATE TABLE relationship_members (
            group_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            PRIMARY KEY (group_id, case_id)
        );
        CREATE TABLE relationship_features (
            group_id TEXT NOT NULL,
            feature_kind TEXT NOT NULL,
            case_id TEXT,
            feature_id TEXT NOT NULL,
            label TEXT NOT NULL,
            site_ids TEXT NOT NULL,
            evidence_keys TEXT NOT NULL
        );
        """
    )
    for record in inherited_kernel["records"]:
        connection.execute(
            "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                record["object_type"],
                record["evidence_tier"],
                record["status"],
                record["schema_version"],
            ),
        )
    inherited_by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in inherited_kernel["records"]:
        inherited_by_case[record["case_id"]].append(record)
    for case_id in sorted(inherited_by_case):
        hypothesis = next(
            record
            for record in inherited_by_case[case_id]
            if record["object_type"] == "mechanism_hypothesis"
        )
        scope = hypothesis["biological_scope"]
        connection.execute(
            "INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                case_id,
                scope["case_label"],
                scope["organism"],
                scope["ec_number"],
                "atlas3_inherited",
                "direct_record",
                "legacy_v2_detailed_or_abstained",
                hypothesis["record_id"],
                None,
                None,
                None,
            ),
        )
        reaction = hypothesis["reaction"]
        connection.execute(
            "INSERT INTO reactions VALUES (?, ?, ?, ?, ?)",
            (
                case_id,
                "direct_record",
                reaction["source_record_id"],
                "id:" + reaction["source_record_id"].split(":", 1)[1],
                reaction["equation"],
            ),
        )
    follow_on_by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in kernel["follow_on_records"]:
        follow_on_by_case[record["case_id"]].append(record)
        connection.execute(
            "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                record["object_type"],
                record["evidence_tier"],
                record["status"],
                record["schema_version"],
            ),
        )
        for proposal in record["mechanism_proposals"]:
            connection.execute(
                "INSERT INTO proposals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    proposal["proposal_id"],
                    proposal["source_mechanism_id"],
                    proposal["rating"],
                    int(proposal["is_detailed"]),
                    int(proposal["preferred"]),
                    len(proposal["mechanism_steps"]),
                    sum(len(step["electron_flows"]) for step in proposal["mechanism_steps"]),
                ),
            )
            for step in proposal["mechanism_steps"]:
                connection.execute(
                    "INSERT INTO mechanism_steps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        record["record_id"],
                        record["case_id"],
                        proposal["proposal_id"],
                        step["step_id"],
                        step["order"],
                        step["summary"],
                        int(step["is_inferred"]),
                        "|".join(step["catalyst_site_ids"]),
                        len(step["electron_flows"]),
                    ),
                )
        for site in record["sites"]:
            mapping_text = "|".join(
                f"{item['pdb_id']}:{item['chain_id']}:{item['author_position']}:{item['label_position']}:{item['applicability']}"
                for item in site["pdb_mappings"]
            )
            connection.execute(
                "INSERT INTO sites VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    site["site_id"],
                    site["residue_name"],
                    site["sequence_position"],
                    "|".join(site["roles"]),
                    mapping_text,
                ),
            )
        for structure in record["structures"]:
            connection.execute(
                "INSERT INTO structures VALUES (?, ?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    structure["pdb_id"],
                    structure["applicability"],
                    "|".join(structure["context_flags"]),
                    structure["limitation"],
                ),
            )
        for uncertainty in record["uncertainties"]:
            connection.execute(
                "INSERT INTO uncertainties VALUES (?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    uncertainty["uncertainty_id"],
                    uncertainty["summary"],
                    uncertainty["abstention"],
                ),
            )
        for counter in record["counterevidence"]:
            connection.execute(
                "INSERT INTO counterevidence VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    counter["counterevidence_id"],
                    counter["summary"],
                    counter["effect"],
                    counter["disposition"],
                    "|".join(counter["evidence_ids"]),
                ),
            )
        abstention = record["detail_abstention"]
        connection.execute(
            "INSERT INTO detail_abstentions VALUES (?, ?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                abstention["reason"],
                "|".join(abstention["unsupported_fields"]),
                "|".join(abstention["source_basis_evidence_ids"]),
            ),
        )
        boundary = record["claim_boundary"]
        connection.execute(
            "INSERT INTO claim_boundaries VALUES (?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                "|".join(boundary["supports"]),
                "|".join(boundary["does_not_support"]),
            ),
        )
        record_provenance = record["provenance"]
        connection.execute(
            "INSERT INTO provenance VALUES (?, ?, ?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                record_provenance["selection_sha256"],
                record_provenance["source_snapshot_set_sha256"],
                record_provenance["compilation_spec_sha256"],
                record_provenance["compiler_version"],
            ),
        )
        for evidence in record["evidence"]:
            connection.execute(
                "INSERT INTO evidence VALUES (?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["case_id"],
                    evidence["evidence_id"],
                    evidence["applicability"],
                    evidence["evidence_role"],
                ),
            )
    for case_id in FOLLOW_ON_CASE_IDS:
        hypothesis = next(
            record
            for record in follow_on_by_case[case_id]
            if record["object_type"] == "mechanism_hypothesis"
        )
        scope = hypothesis["biological_scope"]
        reaction = hypothesis["reaction"]
        connection.execute(
            "INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                case_id,
                scope["case_label"],
                scope["organism"],
                scope["ec_number"],
                "atlas10_follow_on",
                reaction["source_status"],
                hypothesis["mechanism_granularity"],
                hypothesis["record_id"],
                scope["fingerprint_bridge"]["fingerprint_id"],
                scope["fingerprint_bridge"]["use"],
                int(scope["fingerprint_bridge"]["registry_write"]),
            ),
        )
        connection.executemany(
            "INSERT INTO folds VALUES (?, ?)",
            [
                (case_id, fold_id)
                for fold_id in scope["fold_classification_ids"]
            ],
        )
        connection.execute(
            "INSERT INTO reactions VALUES (?, ?, ?, ?, ?)",
            (
                case_id,
                reaction["source_status"],
                reaction["source_record_id"],
                reaction["source_query"],
                reaction["equation"],
            ),
        )
        for participant in reaction["participants"]:
            connection.execute(
                "INSERT INTO participants VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    case_id,
                    participant["participant_id"],
                    participant["reactive_part_id"],
                    participant["side"],
                    participant["name"],
                    participant["source_scope"],
                    participant["source_row_count"],
                    ",".join(str(value) for value in participant["source_count_values"]),
                ),
            )
    for relationship in kernel["relationships"]:
        connection.execute(
            "INSERT INTO relationships VALUES (?, ?, ?)",
            (
                relationship["group_id"],
                relationship["relationship_type"],
                relationship["comparison_boundary"],
            ),
        )
        connection.executemany(
            "INSERT INTO relationship_members VALUES (?, ?)",
            [(relationship["group_id"], case_id) for case_id in relationship["case_ids"]],
        )
        for feature in relationship["shared_features"]:
            connection.execute(
                "INSERT INTO relationship_features VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    relationship["group_id"],
                    "shared",
                    None,
                    feature["feature_id"],
                    feature["label"],
                    "",
                    "|".join(feature["evidence_keys"]),
                ),
            )
        for feature in relationship["member_distinctions"]:
            connection.execute(
                "INSERT INTO relationship_features VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    relationship["group_id"],
                    "member_distinction",
                    feature["case_id"],
                    feature["feature_id"],
                    feature["label"],
                    "|".join(feature["site_ids"]),
                    "|".join(feature["evidence_keys"]),
                ),
            )
    connection.commit()
    return connection


def execute_atlas10_query(
    kernel: dict[str, Any], inherited_kernel: dict[str, Any], query_sql: str
) -> list[dict[str, Any]]:
    if not isinstance(query_sql, str) or not query_sql.strip():
        raise ValueError("Atlas-10 query must be non-empty SQL")
    stripped = query_sql.strip()
    if not stripped.lower().startswith("select") or not sqlite3.complete_statement(
        stripped if stripped.endswith(";") else stripped + ";"
    ):
        raise ValueError("Atlas-10 query surface accepts exactly one SELECT statement")
    statement = stripped[:-1].rstrip() if stripped.endswith(";") else stripped
    connection = materialize_atlas10_sqlite(kernel, inherited_kernel)
    try:
        try:
            # sqlite3.execute rejects a second statement even when it appears
            # after a syntactically valid SELECT; unlike string splitting, it
            # also understands semicolons inside quoted output text.
            cursor = connection.execute(statement)
        except sqlite3.ProgrammingError as exc:
            raise ValueError(
                "Atlas-10 query surface accepts exactly one SELECT statement"
            ) from exc
        columns = [description[0] for description in cursor.description or []]
        return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
    finally:
        connection.close()


def build_atlas10_runtime_result(
    kernel: dict[str, Any],
    inherited_kernel: dict[str, Any],
    queries: dict[str, str],
) -> dict[str, Any]:
    validate_atlas3_kernel(inherited_kernel)
    if set(queries) != {
        "atlas10.query.convergent-strategy",
        "atlas10.query.shared-fold-divergent-chemistry",
    }:
        raise ValueError("Atlas-10 runtime requires the two frozen relationship queries")
    query_results = {
        query_id: execute_atlas10_query(kernel, inherited_kernel, sql)
        for query_id, sql in sorted(queries.items())
    }
    source_annotations = [
        record
        for record in kernel["follow_on_records"]
        if record["object_type"] == "source_annotation"
    ]
    return {
        "schema_version": RUNTIME_SCHEMA_VERSION,
        "kernel_sha256": canonical_sha256(kernel),
        "inherited_kernel_sha256": canonical_sha256(inherited_kernel),
        "query_sha256": {
            query_id: hashlib.sha256(sql.encode("utf-8")).hexdigest()
            for query_id, sql in sorted(queries.items())
        },
        "case_count": 10,
        "record_count": 30,
        "follow_on_case_count": 7,
        "follow_on_record_count": 21,
        "documented_rhea_gap_count": sum(
            record["reaction"]["source_status"] == "documented_query_gap"
            for record in source_annotations
        ),
        "non_detailed_abstention_count": sum(
            record["mechanism_granularity"] == "non_detailed"
            for record in source_annotations
        ),
        "source_mechanism_step_count": sum(
            len(proposal["mechanism_steps"])
            for record in source_annotations
            for proposal in record["mechanism_proposals"]
        ),
        "source_electron_flow_count": sum(
            len(step["electron_flows"])
            for record in source_annotations
            for proposal in record["mechanism_proposals"]
            for step in proposal["mechanism_steps"]
        ),
        "relationship_query_results": query_results,
        "network_used": False,
        "external_binary_used": False,
        "accelerator_used": False,
        "what_it_claims": kernel["claim_boundary"]["supports"],
        "what_it_does_not_claim": kernel["claim_boundary"]["does_not_support"],
    }
