"""Compile evidence-bounded M-CSA source drafts into mechanism-record v4.

The compiler is intentionally source generic: the source manifest selects the
records and requested operation, while the development gate supplies the
allowed scope.  No enzyme-family branch in this module can grant permission.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

BUNDLE_SCHEMA_VERSION = "catalytic-earth.atlas-source-draft-bundle.v1"
RECORD_SCHEMA_VERSION = "catalytic-earth.mechanism-record.v4"
COMPILER_VERSION = "catalytic-earth.atlas-source-draft-compiler.v1"

GATE_PATH = Path("data/atlas/atlas50/development_gate/status.json")
PROBE_PATH = Path("data/atlas/atlas50/state_probe/report.json")
SCHEMA_PATH = Path("src/catalytic_earth/schemas/mechanism-record-v4.schema.json")

STATE_CONTEXT_FIELDS = {
    "components",
    "assembly",
    "state_transitions",
    "tethered_carrier",
    "polymer_topology",
}
OPERATIONS = {"source_annotation", "source_scoped_mechanism_draft"}
OBJECT_TYPES = OPERATIONS
STATUS_BY_OPERATION = {
    "source_annotation": "source_transcription",
    "source_scoped_mechanism_draft": "source_scoped_draft",
}
PROPOSAL_SCOPE_BY_OPERATION = {
    "source_annotation": "source_transcription",
    "source_scoped_mechanism_draft": "bounded_source_scoped",
}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MCSA_RE = re.compile(r"^M[0-9]{4}$")


def _source_inference_flag(source_step_text: str) -> bool | None:
    """Transcribe only an explicit source ``inferred`` tag.

    ``None`` means that the source does not classify the step. Hedging such as
    "thought" is not converted into either True or False.
    """

    return True if re.search(r"\binferred\b", source_step_text, re.IGNORECASE) else None


def canonical_json_bytes(value: Any) -> bytes:
    """Return the canonical bytes used by the draft package builder."""

    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _value_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            output[key] = value
        return output

    def reject_nonfinite(value: str) -> None:
        raise ValueError(f"non-finite JSON value {value!r} in {path}")

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _exact(value: Any, fields: set[str], context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    actual = set(value)
    _require(
        actual == fields,
        f"{context} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return value


def _string(value: Any, context: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{context} must be text")
    return value


def _strings(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    _require(
        isinstance(value, list)
        and len(value) >= minimum
        and all(isinstance(item, str) and item.strip() for item in value)
        and len(value) == len(set(value)),
        f"{context} must be a unique string array",
    )
    return value


def _sha(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{context} must be a lowercase SHA-256",
    )
    return value


def _positive_int(value: Any, context: str) -> int:
    _require(
        isinstance(value, int) and not isinstance(value, bool) and value > 0,
        f"{context} must be a positive integer",
    )
    return value


def _manifest_record_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = manifest.get("records")
    _require(isinstance(records, list), "source manifest records must be an array")
    output: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        context = f"source manifest records[{index}]"
        _require(isinstance(record, dict), f"{context} must be an object")
        _require(record.get("source_id") == "M-CSA", f"{context} source must be M-CSA")
        record_id = record.get("record_id")
        _require(
            isinstance(record_id, str) and _MCSA_RE.fullmatch(record_id) is not None,
            f"{context} has an invalid M-CSA identifier",
        )
        _require(record_id not in output, f"source manifest repeats {record_id}")
        output[record_id] = record
    return output


def _reaction_context(entry: dict[str, Any], mcsa_id: str) -> dict[str, Any]:
    participants: list[dict[str, Any]] = []
    compounds = entry.get("compounds")
    _require(isinstance(compounds, list), f"{mcsa_id} compounds must be an array")
    for index, compound in enumerate(compounds, 1):
        context = f"{mcsa_id} compound[{index - 1}]"
        _require(isinstance(compound, dict), f"{context} must be an object")
        source_token_raw = compound.get("chebi_id")
        _require(source_token_raw is not None, f"{context} lacks a source compound token")
        source_token = str(source_token_raw)
        side = {"reactant": "left", "product": "right"}.get(compound.get("type"))
        _require(side is not None, f"{context} has an unsupported reaction side")
        count = compound.get("count")
        _positive_int(count, f"{context}.count")
        name = _string(compound.get("name"), f"{context}.name")
        participants.append(
            {
                "source_row_index": index,
                "source_compound_token": source_token,
                "normalized_chebi_id": (
                    f"CHEBI:{source_token}" if source_token.isdigit() else None
                ),
                "name": name,
                "side": side,
                "source_count": count,
            }
        )
    _require(participants, f"{mcsa_id} source reaction has no participants")
    ec_numbers = entry.get("ec_numbers")
    _require(isinstance(ec_numbers, list), f"{mcsa_id} EC numbers must be an array")
    return {
        "source_id": "M-CSA",
        "source_record_id": mcsa_id,
        "assertion_scope": "source_reported_reaction_context",
        "canonical_reaction": False,
        "balanced_net_reaction": False,
        "exact_reaction_instance": False,
        "ec_numbers": sorted(
            {str(item) for item in ec_numbers if isinstance(item, (str, int)) and str(item)}
        ),
        "participants": participants,
    }


def _source_references(raw: Any, context: str) -> list[dict[str, Any]]:
    _require(isinstance(raw, list), f"{context} references must be an array")
    output: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        item_context = f"{context}.references[{index}]"
        _require(isinstance(item, dict), f"{item_context} must be an object")
        title = item.get("title")
        _require(title is None or isinstance(title, str), f"{item_context}.title is invalid")
        doi = item.get("doi")
        pubmed_id = item.get("pubmed_id")
        _require(doi is None or isinstance(doi, str), f"{item_context}.doi is invalid")
        _require(
            pubmed_id is None or isinstance(pubmed_id, (str, int)),
            f"{item_context}.pubmed_id is invalid",
        )
        evidence_types = item.get("evidence_types", [])
        _require(
            isinstance(evidence_types, list)
            and all(isinstance(value, str) and value for value in evidence_types),
            f"{item_context}.evidence_types is invalid",
        )
        output.append(
            {
                "title": title,
                "doi": doi,
                "pubmed_id": str(pubmed_id) if pubmed_id is not None else None,
                "evidence_types": sorted(set(evidence_types)),
            }
        )
    return output


def _mechanism_proposals(
    entry: dict[str, Any], mcsa_id: str, *, requested_operation: str
) -> list[dict[str, Any]]:
    from .atlas10_source_adapters import parse_mcsa_scheme_flows

    mechanisms = entry.get("mechanisms")
    scheme_index = entry.get("scheme_index")
    _require(isinstance(mechanisms, list) and mechanisms, f"{mcsa_id} mechanisms missing")
    _require(isinstance(scheme_index, dict), f"{mcsa_id} scheme index missing")
    output: list[dict[str, Any]] = []
    observed_ids: set[int] = set()
    for mechanism in sorted(mechanisms, key=lambda value: value.get("mechanism_id", 0)):
        _require(isinstance(mechanism, dict), f"{mcsa_id} mechanism must be an object")
        mechanism_id = _positive_int(
            mechanism.get("mechanism_id"), f"{mcsa_id}.mechanism_id"
        )
        _require(mechanism_id not in observed_ids, f"{mcsa_id} repeats mechanism {mechanism_id}")
        observed_ids.add(mechanism_id)
        rating = mechanism.get("rating")
        _require(
            isinstance(rating, int)
            and not isinstance(rating, bool)
            and 0 <= rating <= 3,
            f"{mcsa_id} mechanism {mechanism_id} rating is invalid",
        )
        is_detailed = mechanism.get("is_detailed")
        _require(isinstance(is_detailed, bool), f"{mcsa_id} mechanism detail flag is invalid")
        steps = mechanism.get("steps")
        _require(isinstance(steps, list), f"{mcsa_id} mechanism steps must be an array")
        mechanism_steps: list[dict[str, Any]] = []
        terminal_ids: list[int] = []
        issues: list[dict[str, Any]] = []
        source_step_ids: set[int] = set()
        for source_step in steps:
            _require(isinstance(source_step, dict), f"{mcsa_id} source step is invalid")
            source_step_id = _positive_int(
                source_step.get("step_id"), f"{mcsa_id}.source_step_id"
            )
            _require(
                source_step_id not in source_step_ids,
                f"{mcsa_id} mechanism {mechanism_id} repeats step {source_step_id}",
            )
            source_step_ids.add(source_step_id)
            key = (mechanism_id, source_step_id)
            _require(key in scheme_index, f"{mcsa_id} lacks source scheme {key}")
            scheme_wrapper = scheme_index[key]
            flow_parse_status = scheme_wrapper.get("flow_parse_status")
            if flow_parse_status == "source_curved_arrows_preserved":
                parsed = parse_mcsa_scheme_flows(scheme_wrapper)
                _require(
                    scheme_wrapper.get("electron_flow_count")
                    == len(parsed["electron_flows"]),
                    f"{mcsa_id} scheme {key} flow count differs",
                )
            elif flow_parse_status in {
                "source_flow_parse_abstention",
                "source_scheme_unavailable",
            }:
                parsed = {
                    "scheme_status": flow_parse_status,
                    "scheme_sha256": scheme_wrapper.get("content_sha256"),
                    "electron_flows": [],
                }
            else:
                raise ValueError(f"{mcsa_id} scheme {key} lacks a flow-parse disposition")
            scheme_status = _string(
                parsed.get("scheme_status"), f"{mcsa_id} scheme {key} status"
            )
            flows = parsed.get("electron_flows")
            _require(isinstance(flows, list), f"{mcsa_id} scheme {key} flows are invalid")
            scheme_sha = parsed.get("scheme_sha256")
            _require(
                scheme_sha is None
                or (isinstance(scheme_sha, str) and _SHA256_RE.fullmatch(scheme_sha)),
                f"{mcsa_id} scheme {key} hash is invalid",
            )
            source_url = scheme_wrapper.get("source_url")
            _string(source_url, f"{mcsa_id} scheme {key} URL")
            if source_step.get("is_product") is True:
                terminal_ids.append(source_step_id)
                if scheme_status != "source_curved_arrows_preserved":
                    reason = (
                        "The terminal source scheme was unavailable; its source step "
                        "identity is retained without electron flow."
                        if scheme_status == "source_scheme_unavailable"
                        else "The terminal source scheme is retained, but conservative "
                        f"electron-flow parsing abstained: {scheme_wrapper.get('flow_parse_error')}"
                    )
                    issues.append(
                        {
                            "source_step_id": source_step_id,
                            "status": scheme_status,
                            "source_url": source_url,
                            "reason": reason,
                        }
                    )
                continue
            if scheme_status != "source_curved_arrows_preserved" or not flows:
                reason = (
                    "The linked source scheme was unavailable; step text is retained but "
                    "electron flow is withheld."
                    if scheme_status == "source_scheme_unavailable"
                    else "The parsed source scheme contains no electron-flow arrows; none are inferred."
                )
                if scheme_status == "source_flow_parse_abstention":
                    parse_error = scheme_wrapper.get("flow_parse_error")
                    _string(parse_error, f"{mcsa_id} scheme {key} parse error")
                    reason = (
                        "The source scheme is retained, but conservative electron-flow "
                        f"parsing abstained: {parse_error}"
                    )
                issues.append(
                    {
                        "source_step_id": source_step_id,
                        "status": scheme_status,
                        "source_url": source_url,
                        "reason": reason,
                    }
                )
            summary = _string(
                source_step.get("description"),
                f"{mcsa_id} mechanism {mechanism_id} step {source_step_id} summary",
            )
            mechanism_steps.append(
                {
                    "step_id": (
                        f"atlas-draft.{mcsa_id.lower()}.mechanism-{mechanism_id}."
                        f"step-{source_step_id}"
                    ),
                    "order": len(mechanism_steps) + 1,
                    "summary": summary,
                    "source_step_id": source_step_id,
                    "is_inferred": _source_inference_flag(summary),
                    "evidence_ids": [f"source:M-CSA:{mcsa_id}"],
                    "source_scheme_sha256": scheme_sha,
                    "scheme_status": scheme_status,
                    "electron_flows": copy.deepcopy(flows),
                    "electron_flow_semantics": (
                        "source_ordered_curved_arrow_endpoints_not_atom_mapped_bond_edits"
                    ),
                    "electron_flow_abstention": (
                        None
                        if flows
                        else next(
                            issue["reason"]
                            for issue in issues
                            if issue["source_step_id"] == source_step_id
                        )
                    ),
                    "atom_mapping_status": "not_inferred",
                    "bond_edit_status": "not_compiled_from_unmapped_source_scheme",
                }
            )
        structured_status = "source_non_detailed_no_ordered_mechanism_claim"
        if is_detailed:
            structured_status = (
                "source_steps_preserved_with_flow_abstentions"
                if issues
                else "source_curved_arrows_preserved_no_atom_mapping_inference"
            )
        output.append(
            {
                "proposal_id": f"atlas-draft.{mcsa_id.lower()}.mechanism-{mechanism_id}",
                "source_id": "M-CSA",
                "source_record_id": mcsa_id,
                "source_mechanism_id": mechanism_id,
                "rating": rating,
                "is_detailed": is_detailed,
                "proposal_scope": PROPOSAL_SCOPE_BY_OPERATION[requested_operation],
                "components_summary": _string(
                    mechanism.get("components_summary"),
                    f"{mcsa_id} mechanism {mechanism_id} components summary",
                ),
                "mechanism_text": _string(
                    mechanism.get("mechanism_text"),
                    f"{mcsa_id} mechanism {mechanism_id} text",
                ),
                "source_references": _source_references(
                    mechanism.get("references", []),
                    f"{mcsa_id}.mechanism-{mechanism_id}",
                ),
                "mechanism_steps": mechanism_steps,
                "terminal_state_source_step_ids": terminal_ids,
                "structured_detail_status": structured_status,
                "scheme_retrieval_issues": issues,
            }
        )
    return output


def _residue_assertions(
    entry: dict[str, Any], mcsa_id: str
) -> list[dict[str, Any]]:
    residues = entry.get("residues")
    _require(isinstance(residues, list), f"{mcsa_id} residues must be an array")
    output: list[dict[str, Any]] = []
    for index, residue in enumerate(residues, 1):
        context = f"{mcsa_id}.residues[{index - 1}]"
        _require(isinstance(residue, dict), f"{context} must be an object")
        role_labels = sorted(
            {
                role["function"]
                for role in residue.get("roles", [])
                if isinstance(role, dict)
                and isinstance(role.get("function"), str)
                and role["function"]
            }
        )
        sequence_locations: list[dict[str, Any]] = []
        for location in residue.get("residue_sequences", []):
            _require(isinstance(location, dict), f"{context} sequence location is invalid")
            sequence_locations.append(
                {
                    "uniprot_id": location.get("uniprot_id"),
                    "residue_name": location.get("code"),
                    "sequence_position": location.get("resid"),
                    "is_reference": bool(location.get("is_reference")),
                }
            )
        structure_locations: list[dict[str, Any]] = []
        for location in residue.get("residue_chains", []):
            _require(isinstance(location, dict), f"{context} structure location is invalid")
            structure_locations.append(
                {
                    "pdb_id": (
                        str(location.get("pdb_id", "")).upper()
                        if location.get("pdb_id") is not None
                        else None
                    ),
                    "chain_id": (
                        location.get("auth_chain_name")
                        or location.get("assembly_chain_name")
                        or location.get("chain_name")
                    ),
                    "author_position": location.get("auth_resid"),
                    "label_position": location.get("resid"),
                    "residue_name": location.get("code"),
                    "is_reference": bool(location.get("is_reference")),
                }
            )
        output.append(
            {
                "assertion_id": f"atlas-draft.{mcsa_id.lower()}.source-residue-{index}",
                "assertion_scope": "mcsa_source_transcription_not_independently_mapped",
                "source_role_labels": role_labels,
                "source_roles_summary": residue.get("roles_summary") or None,
                "source_sequence_locations": sequence_locations,
                "source_structure_locations": structure_locations,
                "mapping_status": "source_transcription_not_coordinate_verified",
            }
        )
    return output


def _source_step_inventory(entry: dict[str, Any], mcsa_id: str) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    scheme_index = entry["scheme_index"]
    for mechanism in entry["mechanisms"]:
        mechanism_id = mechanism["mechanism_id"]
        for step in mechanism["steps"]:
            source_step_id = step["step_id"]
            wrapper = scheme_index[(mechanism_id, source_step_id)]
            inventory.append(
                {
                    "source_mechanism_id": mechanism_id,
                    "source_step_id": source_step_id,
                    "is_terminal_state": step["is_product"],
                    "flow_parse_status": wrapper["flow_parse_status"],
                    "source_scheme_sha256": wrapper["content_sha256"],
                    "electron_flow_count": wrapper["electron_flow_count"],
                }
            )
    return inventory


def _source_record(
    record: dict[str, Any], entry: dict[str, Any], mcsa_id: str
) -> dict[str, Any]:
    required = {
        "uri",
        "retrieval_status",
        "snapshot_sha256",
        "snapshot_bytes",
        "retrieved_at",
        "entry_response_sha256",
        "license",
        "attribution",
        "change_notice",
        "probe_identity",
    }
    _require(required <= set(record), f"source manifest record {mcsa_id} is incomplete")
    return {
        "source_id": "M-CSA",
        "source_record_id": mcsa_id,
        "uri": record["uri"],
        "retrieval_status": record["retrieval_status"],
        "snapshot_sha256": record["snapshot_sha256"],
        "snapshot_bytes": record["snapshot_bytes"],
        "retrieved_at": record["retrieved_at"],
        "entry_response_sha256": record["entry_response_sha256"],
        "license": record["license"],
        "attribution": record["attribution"],
        "change_notice": record["change_notice"],
        "probe_identity": copy.deepcopy(record["probe_identity"]),
        "source_step_inventory": _source_step_inventory(entry, mcsa_id),
    }


def _case_control(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "mcsa_id": case["mcsa_id"],
        "scope": case["scope"],
        "allowed_operations": case["allowed_operations"],
        "mandatory_abstentions": case["mandatory_abstentions"],
    }


def _record(
    *,
    entry: dict[str, Any],
    manifest_record: dict[str, Any],
    gate_case: dict[str, Any],
    probe_case: dict[str, Any],
    requested_operation: str,
    source_manifest_sha256: str,
    source_snapshot_set_sha256: str,
    input_bindings: dict[str, str],
) -> dict[str, Any]:
    mcsa_id = gate_case["mcsa_id"]
    case_id = probe_case["candidate_id"]
    mandatory_abstentions = copy.deepcopy(gate_case["mandatory_abstentions"])
    role_conflicts = sorted(
        item["clause_id"]
        for item in mandatory_abstentions
        if "role" in item["clause_id"]
    )
    object_suffix = (
        "source-annotation"
        if requested_operation == "source_annotation"
        else "source-scoped-mechanism-draft"
    )
    source = _source_record(manifest_record, entry, mcsa_id)
    proposals = _mechanism_proposals(
        entry, mcsa_id, requested_operation=requested_operation
    )
    residue_assertions = _residue_assertions(entry, mcsa_id)
    state_context = copy.deepcopy(probe_case["representation"])
    record = {
        "schema_version": RECORD_SCHEMA_VERSION,
        "record_id": f"atlas50-draft:{mcsa_id.lower()}:{object_suffix}",
        "case_id": case_id,
        "mcsa_id": mcsa_id,
        "label": f"{probe_case['label']} — {object_suffix.replace('-', ' ')}",
        "object_type": requested_operation,
        "evidence_tier": 1,
        "status": STATUS_BY_OPERATION[requested_operation],
        "source_scope": gate_case["scope"],
        "reaction_context": _reaction_context(entry, mcsa_id),
        "state_context": state_context,
        "mechanism_proposals": proposals,
        "source_residue_assertions": residue_assertions,
        "residue_role_resolution": {
            "status": (
                "source_conflict_unresolved"
                if role_conflicts
                else "source_transcription_only_not_independently_adjudicated"
            ),
            "abstention_clause_ids": role_conflicts,
        },
        "mandatory_abstentions": mandatory_abstentions,
        "source": source,
        "claim_boundary": {
            "supports": [
                "A queryable transcription of the selected M-CSA proposals and source reaction context.",
                gate_case["scope"],
            ],
            "does_not_support": [
                "A canonical or independently balanced net reaction.",
                "An exact reaction instance, atom-mapped bond edits, or a complete observed turnover trajectory.",
                "Tier-2 protein/site grounding, independent review, or experimental validation.",
            ],
        },
        "provenance": {
            "compiler_version": COMPILER_VERSION,
            "requested_operation": requested_operation,
            "allowed_operations": copy.deepcopy(gate_case["allowed_operations"]),
            "case_control_sha256": _value_sha256(_case_control(gate_case)),
            "source_snapshot_sha256": source["snapshot_sha256"],
            "source_manifest_sha256": source_manifest_sha256,
            "source_snapshot_set_sha256": source_snapshot_set_sha256,
            "development_gate_status_sha256": input_bindings[
                "development_gate_status"
            ],
            "state_probe_report_sha256": input_bindings["state_probe_report"],
            "source_projection_sha256": _value_sha256(
                {
                    "reaction_context": _reaction_context(entry, mcsa_id),
                    "mechanism_proposals": proposals,
                    "source_residue_assertions": residue_assertions,
                }
            ),
            "state_context_sha256": _value_sha256(state_context),
        },
    }
    return record


def _summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    object_counts = Counter(record["object_type"] for record in records)
    proposal_count = sum(len(record["mechanism_proposals"]) for record in records)
    detailed = sum(
        proposal["is_detailed"]
        for record in records
        for proposal in record["mechanism_proposals"]
    )
    steps = [
        step
        for record in records
        for proposal in record["mechanism_proposals"]
        for step in proposal["mechanism_steps"]
    ]
    return {
        "selected_case_count": len(records),
        "record_count": len(records),
        "source_annotation_count": object_counts["source_annotation"],
        "source_scoped_mechanism_draft_count": object_counts[
            "source_scoped_mechanism_draft"
        ],
        "evidence_tier_counts": {"1": len(records)},
        "mechanism_proposal_count": proposal_count,
        "detailed_mechanism_proposal_count": detailed,
        "non_detailed_mechanism_proposal_count": proposal_count - detailed,
        "source_mechanism_step_count": len(steps),
        "source_electron_flow_count": sum(len(step["electron_flows"]) for step in steps),
        "steps_with_electron_flow_abstention": sum(
            step["electron_flow_abstention"] is not None for step in steps
        ),
        "canonical_reaction_count": 0,
        "exact_reaction_instance_count": 0,
        "tier_2_record_count": 0,
        "independently_validated_record_count": 0,
    }


def _build_source_drafts(
    *,
    source_manifest: dict[str, Any],
    entries: dict[str, dict[str, Any]],
    development_gate: dict[str, Any],
    state_probe: dict[str, Any],
    input_bindings: dict[str, str],
) -> dict[str, Any]:
    """Pure compiler used by the repository builder and focused tests."""

    selection = source_manifest.get("selection")
    _require(isinstance(selection, dict), "source manifest selection is missing")
    requested_operation = selection.get("requested_operation")
    _require(requested_operation in OPERATIONS, "unsupported requested draft operation")
    record_ids = _strings(selection.get("record_ids"), "selection.record_ids", minimum=1)
    _require(
        all(_MCSA_RE.fullmatch(value) for value in record_ids),
        "selection contains an invalid M-CSA identifier",
    )
    _require(set(record_ids) == set(entries), "loaded source entries differ from selection")
    manifest_records = _manifest_record_index(source_manifest)
    _require(
        set(record_ids) == set(manifest_records),
        "source manifest records differ from selection",
    )
    gate_cases = {
        case["mcsa_id"]: case for case in development_gate.get("cases", [])
    }
    probe_cases = {case["mcsa_id"]: case for case in state_probe.get("cases", [])}
    _require(
        set(record_ids) <= set(gate_cases) and set(record_ids) <= set(probe_cases),
        "selected source lacks gate or state-probe control",
    )
    source_manifest_sha256 = _value_sha256(source_manifest)
    source_snapshot_set_sha256 = _sha(
        source_manifest.get("snapshot_set_sha256"), "source snapshot-set hash"
    )
    expected_bindings = {
        "development_gate_status",
        "state_probe_report",
        "source_manifest",
        "record_schema",
    }
    _exact(input_bindings, expected_bindings, "input_bindings")
    for key, value in input_bindings.items():
        _sha(value, f"input_bindings.{key}")
    _require(
        input_bindings["source_manifest"] == source_manifest_sha256,
        "source manifest input binding differs",
    )
    records: list[dict[str, Any]] = []
    case_bindings: list[dict[str, Any]] = []
    for mcsa_id in record_ids:
        entry = entries[mcsa_id]
        _require(entry.get("record_id") == mcsa_id, f"parsed source identity differs for {mcsa_id}")
        gate_case = gate_cases[mcsa_id]
        allowed = gate_case.get("allowed_operations")
        _require(
            isinstance(allowed, list) and requested_operation in allowed,
            f"development gate denies {requested_operation} for {mcsa_id}",
        )
        probe_case = probe_cases[mcsa_id]
        _require(
            probe_case.get("candidate_id") == f"atlas50.candidate.{mcsa_id.lower()}",
            f"state-probe candidate identity differs for {mcsa_id}",
        )
        record = _record(
            entry=entry,
            manifest_record=manifest_records[mcsa_id],
            gate_case=gate_case,
            probe_case=probe_case,
            requested_operation=requested_operation,
            source_manifest_sha256=source_manifest_sha256,
            source_snapshot_set_sha256=source_snapshot_set_sha256,
            input_bindings=input_bindings,
        )
        records.append(record)
        case_bindings.append(
            {
                "mcsa_id": mcsa_id,
                "case_control_sha256": record["provenance"]["case_control_sha256"],
                "source_snapshot_sha256": record["source"]["snapshot_sha256"],
            }
        )
    bundle = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "bundle_id": "atlas50.source-scoped-mechanism-drafts",
        "record_schema_version": RECORD_SCHEMA_VERSION,
        "source_manifest_sha256": source_manifest_sha256,
        "source_snapshot_set_sha256": source_snapshot_set_sha256,
        "input_bindings": copy.deepcopy(input_bindings),
        "selection": {
            "basis": _string(selection.get("basis"), "selection.basis"),
            "requested_operation": requested_operation,
            "record_ids": list(record_ids),
            "case_bindings": case_bindings,
        },
        "records": records,
        "summary": _summary(records),
        "claim_boundary": {
            "supports": [
                "Versioned source-scoped M-CSA draft records selected and bounded by the computational development gate."
            ],
            "does_not_support": [
                "Canonical balanced reaction compilation or exact reaction instances.",
                "Protein/site-grounded Tier-2 records, independent review, or experimental validation.",
                "Writes to protected registries or completion of frozen Atlas-50 Phase B."
            ],
        },
        "review_independence": copy.deepcopy(
            development_gate.get("review_independence")
        ),
    }
    validate_source_drafts(bundle)
    return bundle


def build_source_drafts(repo_root: str | Path) -> dict[str, Any]:
    """Build v4 records from offline source snapshots and live gate inputs."""

    root = Path(repo_root)
    # Kept local so importing the wheel-side validator never requires source
    # acquisition code or repository data.
    from .atlas_draft_sources import load_draft_sources
    from .atlas50_development_gate import build_development_status
    from .canonical_hash import canonical_file_sha256

    source_manifest, entries = load_draft_sources(root)
    gate = build_development_status(root)
    committed_gate = _read_json(root / GATE_PATH)
    _require(
        committed_gate == gate,
        "committed computational development status is stale",
    )
    state_probe = _read_json(root / PROBE_PATH)
    source_manifest_sha256 = _value_sha256(source_manifest)
    input_bindings = {
        "development_gate_status": canonical_file_sha256(root / GATE_PATH),
        "state_probe_report": canonical_file_sha256(root / PROBE_PATH),
        "source_manifest": source_manifest_sha256,
        "record_schema": canonical_file_sha256(root / SCHEMA_PATH),
    }
    return _build_source_drafts(
        source_manifest=source_manifest,
        entries=entries,
        development_gate=gate,
        state_probe=state_probe,
        input_bindings=input_bindings,
    )


def _validate_claim_boundary(value: Any, context: str) -> None:
    boundary = _exact(value, {"supports", "does_not_support"}, context)
    _strings(boundary["supports"], f"{context}.supports", minimum=1)
    _strings(boundary["does_not_support"], f"{context}.does_not_support", minimum=1)


def _validate_electron_flows(value: Any, context: str) -> None:
    _require(isinstance(value, list), f"{context} must be an array")
    for flow_index, flow in enumerate(value):
        flow_context = f"{context}[{flow_index}]"
        flow = _exact(
            flow,
            {"flow_id", "source_point", "target_point", "ordering_semantics"},
            flow_context,
        )
        _string(flow["flow_id"], f"{flow_context}.flow_id")
        _require(
            flow["ordering_semantics"]
            == "source_file_order_not_independently_inferred",
            f"{flow_context} overstates electron-flow ordering",
        )
        for side in ("source_point", "target_point"):
            point_context = f"{flow_context}.{side}"
            point = _exact(flow[side], {"point_kind", "atoms"}, point_context)
            _require(
                point["point_kind"] in {"electron_base_atom", "atom_set"},
                f"{point_context} kind is invalid",
            )
            _require(
                isinstance(point["atoms"], list) and point["atoms"],
                f"{point_context}.atoms must be non-empty",
            )
            for atom_index, atom in enumerate(point["atoms"]):
                atom_context = f"{point_context}.atoms[{atom_index}]"
                atom = _exact(
                    atom,
                    {"source_atom_ref", "element", "formal_charge", "semantic_labels"},
                    atom_context,
                )
                _string(atom["source_atom_ref"], f"{atom_context}.source_atom_ref")
                _string(atom["element"], f"{atom_context}.element")
                _require(
                    atom["formal_charge"] is None
                    or (
                        isinstance(atom["formal_charge"], int)
                        and not isinstance(atom["formal_charge"], bool)
                    ),
                    f"{atom_context}.formal_charge is invalid",
                )
                _strings(atom["semantic_labels"], f"{atom_context}.semantic_labels")


def _validate_state_context(value: Any, context: str) -> None:
    state = _exact(value, STATE_CONTEXT_FIELDS, context)
    components = state["components"]
    _require(isinstance(components, list) and components, f"{context}.components missing")
    component_ids: set[str] = set()
    for index, component in enumerate(components):
        item_context = f"{context}.components[{index}]"
        component = _exact(
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
        component_id = _string(component["component_id"], f"{item_context}.component_id")
        _require(component_id not in component_ids, f"{context} repeats component {component_id}")
        component_ids.add(component_id)
        _require(
            component["component_kind"]
            in {"protein", "protein_role", "cofactor", "metallocluster", "redox_partner", "polymer"},
            f"{item_context}.component_kind is invalid",
        )
        _require(
            component["identity_scope"]
            in {"source_identity", "source_defined", "context_only", "role_only"},
            f"{item_context}.identity_scope is invalid",
        )
        _string(component["role"], f"{item_context}.role")
        _strings(component["evidence_ids"], f"{item_context}.evidence_ids", minimum=1)
        _require(
            isinstance(component["source_identifiers"], list),
            f"{item_context}.source_identifiers must be an array",
        )
        for identity_index, identity in enumerate(component["source_identifiers"]):
            identity = _exact(
                identity,
                {"namespace", "accession"},
                f"{item_context}.source_identifiers[{identity_index}]",
            )
            _string(identity["namespace"], f"{item_context}.source identifier namespace")
            _string(identity["accession"], f"{item_context}.source identifier accession")
    assembly = _exact(
        state["assembly"],
        {"mode", "member_component_ids", "assertion_scope", "evidence_ids", "note"},
        f"{context}.assembly",
    )
    _require(
        assembly["mode"]
        in {"single_source_component", "fixed_multisubunit", "cycle_coupled_association", "external_carrier_encounter"},
        f"{context}.assembly mode is invalid",
    )
    members = _strings(
        assembly["member_component_ids"],
        f"{context}.assembly.member_component_ids",
        minimum=1,
    )
    _require(set(members) <= component_ids, f"{context}.assembly references unknown components")
    _string(assembly["assertion_scope"], f"{context}.assembly.assertion_scope")
    _strings(assembly["evidence_ids"], f"{context}.assembly.evidence_ids", minimum=1)
    _string(assembly["note"], f"{context}.assembly.note")
    transitions = state["state_transitions"]
    _require(isinstance(transitions, list), f"{context}.state_transitions must be an array")
    transition_ids: set[str] = set()
    for index, transition in enumerate(transitions):
        item_context = f"{context}.state_transitions[{index}]"
        transition = _exact(
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
        transition_id = _string(transition["transition_id"], f"{item_context}.transition_id")
        _require(transition_id not in transition_ids, f"{context} repeats transition {transition_id}")
        transition_ids.add(transition_id)
        subjects = _strings(
            transition["subject_component_ids"],
            f"{item_context}.subject_component_ids",
            minimum=1,
        )
        _require(set(subjects) <= component_ids, f"{item_context} references unknown components")
        for key in ("before_state_id", "after_state_id", "transition_kind", "assertion_scope"):
            _string(transition[key], f"{item_context}.{key}")
        _strings(transition["evidence_ids"], f"{item_context}.evidence_ids", minimum=1)
    carrier = state["tethered_carrier"]
    if carrier is not None:
        carrier = _exact(
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
        _require(
            carrier["owner_component_id"] in component_ids,
            f"{context}.tethered_carrier owner is unknown",
        )
        for key in ("attachment_residue", "reactant_state_id", "product_state_id", "status"):
            _string(carrier[key], f"{context}.tethered_carrier.{key}")
        _require(
            carrier["attachment_site"] is None
            or isinstance(carrier["attachment_site"], str),
            f"{context}.tethered_carrier attachment site is invalid",
        )
        structure_ids = _strings(
            carrier["structure_component_ids"],
            f"{context}.tethered_carrier.structure_component_ids",
        )
        _require(set(structure_ids) <= component_ids, f"{context}.tethered_carrier structure identity is unknown")
        _strings(carrier["evidence_ids"], f"{context}.tethered_carrier.evidence_ids", minimum=1)
    polymer = state["polymer_topology"]
    if polymer is not None:
        polymer = _exact(
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
        _require(
            polymer["polymer_component_id"] in component_ids,
            f"{context}.polymer_topology component is unknown",
        )
        _string(polymer["reactant_state_id"], f"{context}.polymer_topology.reactant_state_id")
        for key in (
            "product_state_id",
            "source_product_placeholder",
            "reaction_event",
            "topology_before",
            "topology_after",
            "chain_length_before",
            "chain_length_after",
            "initiation_or_elongation",
            "processivity",
        ):
            _require(
                polymer[key] is None or isinstance(polymer[key], str),
                f"{context}.polymer_topology.{key} is invalid",
            )
        _string(polymer["status"], f"{context}.polymer_topology.status")
        _strings(polymer["evidence_ids"], f"{context}.polymer_topology.evidence_ids", minimum=1)


def _validate_record(record: Any, *, bundle: dict[str, Any], context: str) -> None:
    record = _exact(
        record,
        {
            "schema_version",
            "record_id",
            "case_id",
            "mcsa_id",
            "label",
            "object_type",
            "evidence_tier",
            "status",
            "source_scope",
            "reaction_context",
            "state_context",
            "mechanism_proposals",
            "source_residue_assertions",
            "residue_role_resolution",
            "mandatory_abstentions",
            "source",
            "claim_boundary",
            "provenance",
        },
        context,
    )
    _require(record["schema_version"] == RECORD_SCHEMA_VERSION, f"{context} schema differs")
    _string(record["record_id"], f"{context}.record_id")
    _string(record["case_id"], f"{context}.case_id")
    mcsa_id = record["mcsa_id"]
    _require(isinstance(mcsa_id, str) and _MCSA_RE.fullmatch(mcsa_id), f"{context} M-CSA ID is invalid")
    _string(record["label"], f"{context}.label")
    operation = record["object_type"]
    _require(operation in OBJECT_TYPES, f"{context} object type is invalid")
    _require(record["evidence_tier"] == 1, f"{context} must remain Tier 1")
    _require(record["status"] == STATUS_BY_OPERATION[operation], f"{context} status differs")
    _string(record["source_scope"], f"{context}.source_scope")
    reaction = _exact(
        record["reaction_context"],
        {
            "source_id",
            "source_record_id",
            "assertion_scope",
            "canonical_reaction",
            "balanced_net_reaction",
            "exact_reaction_instance",
            "ec_numbers",
            "participants",
        },
        f"{context}.reaction_context",
    )
    _require(
        reaction["source_id"] == "M-CSA"
        and reaction["source_record_id"] == mcsa_id
        and reaction["assertion_scope"] == "source_reported_reaction_context",
        f"{context} reaction source identity differs",
    )
    for flag in ("canonical_reaction", "balanced_net_reaction", "exact_reaction_instance"):
        _require(reaction[flag] is False, f"{context} overclaims {flag}")
    _strings(reaction["ec_numbers"], f"{context}.reaction_context.ec_numbers")
    participants = reaction["participants"]
    _require(isinstance(participants, list) and participants, f"{context} participants missing")
    for index, participant in enumerate(participants, 1):
        item_context = f"{context}.reaction_context.participants[{index - 1}]"
        participant = _exact(
            participant,
            {
                "source_row_index",
                "source_compound_token",
                "normalized_chebi_id",
                "name",
                "side",
                "source_count",
            },
            item_context,
        )
        _require(participant["source_row_index"] == index, f"{item_context} order differs")
        token = _string(participant["source_compound_token"], f"{item_context}.source_compound_token")
        expected_chebi = f"CHEBI:{token}" if token.isdigit() else None
        _require(participant["normalized_chebi_id"] == expected_chebi, f"{item_context} ChEBI normalization differs")
        _string(participant["name"], f"{item_context}.name")
        _require(participant["side"] in {"left", "right"}, f"{item_context}.side is invalid")
        _positive_int(participant["source_count"], f"{item_context}.source_count")
    _validate_state_context(record["state_context"], f"{context}.state_context")
    proposals = record["mechanism_proposals"]
    _require(isinstance(proposals, list) and proposals, f"{context} proposals missing")
    mechanism_ids: set[int] = set()
    for proposal_index, proposal in enumerate(proposals):
        proposal_context = f"{context}.mechanism_proposals[{proposal_index}]"
        proposal = _exact(
            proposal,
            {
                "proposal_id",
                "source_id",
                "source_record_id",
                "source_mechanism_id",
                "rating",
                "is_detailed",
                "proposal_scope",
                "components_summary",
                "mechanism_text",
                "source_references",
                "mechanism_steps",
                "terminal_state_source_step_ids",
                "structured_detail_status",
                "scheme_retrieval_issues",
            },
            proposal_context,
        )
        _string(proposal["proposal_id"], f"{proposal_context}.proposal_id")
        _require(
            proposal["source_id"] == "M-CSA"
            and proposal["source_record_id"] == mcsa_id,
            f"{proposal_context} source identity differs",
        )
        mechanism_id = _positive_int(
            proposal["source_mechanism_id"], f"{proposal_context}.source_mechanism_id"
        )
        _require(mechanism_id not in mechanism_ids, f"{context} repeats mechanism {mechanism_id}")
        mechanism_ids.add(mechanism_id)
        _require(
            isinstance(proposal["rating"], int)
            and not isinstance(proposal["rating"], bool)
            and 0 <= proposal["rating"] <= 3,
            f"{proposal_context}.rating is invalid",
        )
        _require(isinstance(proposal["is_detailed"], bool), f"{proposal_context}.is_detailed is invalid")
        _require(
            proposal["proposal_scope"] == PROPOSAL_SCOPE_BY_OPERATION[operation],
            f"{proposal_context} proposal scope exceeds record operation",
        )
        _string(proposal["components_summary"], f"{proposal_context}.components_summary")
        _string(proposal["mechanism_text"], f"{proposal_context}.mechanism_text")
        references = proposal["source_references"]
        _require(isinstance(references, list), f"{proposal_context}.source_references is invalid")
        for reference in references:
            _exact(reference, {"title", "doi", "pubmed_id", "evidence_types"}, f"{proposal_context}.reference")
            _require(reference["title"] is None or isinstance(reference["title"], str), f"{proposal_context} reference title is invalid")
            _require(reference["doi"] is None or isinstance(reference["doi"], str), f"{proposal_context} reference DOI is invalid")
            _require(reference["pubmed_id"] is None or isinstance(reference["pubmed_id"], str), f"{proposal_context} reference PubMed ID is invalid")
            _strings(reference["evidence_types"], f"{proposal_context}.reference.evidence_types")
        steps = proposal["mechanism_steps"]
        _require(isinstance(steps, list), f"{proposal_context}.mechanism_steps is invalid")
        source_step_ids: set[int] = set()
        for step_index, step in enumerate(steps, 1):
            step_context = f"{proposal_context}.mechanism_steps[{step_index - 1}]"
            step = _exact(
                step,
                {
                    "step_id",
                    "order",
                    "summary",
                    "source_step_id",
                    "is_inferred",
                    "evidence_ids",
                    "source_scheme_sha256",
                    "scheme_status",
                    "electron_flows",
                    "electron_flow_semantics",
                    "electron_flow_abstention",
                    "atom_mapping_status",
                    "bond_edit_status",
                },
                step_context,
            )
            _string(step["step_id"], f"{step_context}.step_id")
            _require(step["order"] == step_index, f"{step_context} order is not contiguous")
            _string(step["summary"], f"{step_context}.summary")
            source_step_id = _positive_int(step["source_step_id"], f"{step_context}.source_step_id")
            _require(source_step_id not in source_step_ids, f"{proposal_context} repeats source step")
            source_step_ids.add(source_step_id)
            _require(
                step["is_inferred"] is _source_inference_flag(step["summary"]),
                f"{step_context}.is_inferred differs from the explicit source tag",
            )
            _strings(step["evidence_ids"], f"{step_context}.evidence_ids", minimum=1)
            if step["source_scheme_sha256"] is not None:
                _sha(step["source_scheme_sha256"], f"{step_context}.source_scheme_sha256")
            _string(step["scheme_status"], f"{step_context}.scheme_status")
            _validate_electron_flows(step["electron_flows"], f"{step_context}.electron_flows")
            _require(
                step["electron_flow_semantics"]
                == "source_ordered_curved_arrow_endpoints_not_atom_mapped_bond_edits",
                f"{step_context} electron-flow semantics differ",
            )
            _require(step["atom_mapping_status"] == "not_inferred", f"{step_context} invents an atom map")
            _require(
                step["bond_edit_status"]
                == "not_compiled_from_unmapped_source_scheme",
                f"{step_context} invents bond edits",
            )
            if step["electron_flows"]:
                _require(step["electron_flow_abstention"] is None, f"{step_context} flow abstention is inconsistent")
            else:
                _string(step["electron_flow_abstention"], f"{step_context}.electron_flow_abstention")
        terminal_ids = proposal["terminal_state_source_step_ids"]
        _require(
            isinstance(terminal_ids, list)
            and all(isinstance(item, int) and not isinstance(item, bool) and item > 0 for item in terminal_ids)
            and len(terminal_ids) == len(set(terminal_ids)),
            f"{proposal_context}.terminal_state_source_step_ids is invalid",
        )
        _require(not (source_step_ids & set(terminal_ids)), f"{proposal_context} terminal step duplicated")
        _require(
            proposal["structured_detail_status"]
            in {
                "source_curved_arrows_preserved_no_atom_mapping_inference",
                "source_steps_preserved_with_flow_abstentions",
                "source_non_detailed_no_ordered_mechanism_claim",
            },
            f"{proposal_context} structured detail status is invalid",
        )
        issues = proposal["scheme_retrieval_issues"]
        _require(isinstance(issues, list), f"{proposal_context}.scheme_retrieval_issues is invalid")
        for issue in issues:
            issue = _exact(issue, {"source_step_id", "status", "source_url", "reason"}, f"{proposal_context}.scheme_issue")
            _positive_int(issue["source_step_id"], f"{proposal_context}.scheme_issue.source_step_id")
            _string(issue["status"], f"{proposal_context}.scheme_issue.status")
            _string(issue["source_url"], f"{proposal_context}.scheme_issue.source_url")
            _string(issue["reason"], f"{proposal_context}.scheme_issue.reason")
        if proposal["is_detailed"] and any(step["electron_flow_abstention"] for step in steps):
            _require(
                proposal["structured_detail_status"] == "source_steps_preserved_with_flow_abstentions",
                f"{proposal_context} hides a flow abstention",
            )
        if not proposal["is_detailed"]:
            _require(
                proposal["structured_detail_status"]
                == "source_non_detailed_no_ordered_mechanism_claim",
                f"{proposal_context} overstates non-detailed source content",
            )
    residues = record["source_residue_assertions"]
    _require(isinstance(residues, list), f"{context}.source_residue_assertions is invalid")
    for index, residue in enumerate(residues, 1):
        residue_context = f"{context}.source_residue_assertions[{index - 1}]"
        residue = _exact(
            residue,
            {
                "assertion_id",
                "assertion_scope",
                "source_role_labels",
                "source_roles_summary",
                "source_sequence_locations",
                "source_structure_locations",
                "mapping_status",
            },
            residue_context,
        )
        _string(residue["assertion_id"], f"{residue_context}.assertion_id")
        _require(
            residue["assertion_scope"]
            == "mcsa_source_transcription_not_independently_mapped",
            f"{residue_context} scope overclaims mapping",
        )
        _strings(residue["source_role_labels"], f"{residue_context}.source_role_labels")
        _require(
            residue["source_roles_summary"] is None
            or isinstance(residue["source_roles_summary"], str),
            f"{residue_context}.source_roles_summary is invalid",
        )
        for field in ("source_sequence_locations", "source_structure_locations"):
            _require(isinstance(residue[field], list), f"{residue_context}.{field} is invalid")
        _require(
            residue["mapping_status"] == "source_transcription_not_coordinate_verified",
            f"{residue_context} overclaims residue mapping",
        )
    abstentions = record["mandatory_abstentions"]
    _require(isinstance(abstentions, list), f"{context}.mandatory_abstentions is invalid")
    clause_ids: list[str] = []
    for abstention in abstentions:
        abstention = _exact(abstention, {"clause_id", "reason"}, f"{context}.mandatory_abstention")
        clause_ids.append(_string(abstention["clause_id"], f"{context}.abstention.clause_id"))
        _string(abstention["reason"], f"{context}.abstention.reason")
    _require(len(clause_ids) == len(set(clause_ids)), f"{context} repeats an abstention clause")
    role_resolution = _exact(
        record["residue_role_resolution"],
        {"status", "abstention_clause_ids"},
        f"{context}.residue_role_resolution",
    )
    role_clauses = sorted(value for value in clause_ids if "role" in value)
    _require(
        role_resolution["abstention_clause_ids"] == role_clauses,
        f"{context} residue-role conflict binding differs",
    )
    expected_role_status = (
        "source_conflict_unresolved"
        if role_clauses
        else "source_transcription_only_not_independently_adjudicated"
    )
    _require(role_resolution["status"] == expected_role_status, f"{context} residue roles overclaim resolution")
    source = _exact(
        record["source"],
        {
            "source_id",
            "source_record_id",
            "uri",
            "retrieval_status",
            "snapshot_sha256",
            "snapshot_bytes",
            "retrieved_at",
            "entry_response_sha256",
            "license",
            "attribution",
            "change_notice",
            "probe_identity",
            "source_step_inventory",
        },
        f"{context}.source",
    )
    _require(source["source_id"] == "M-CSA" and source["source_record_id"] == mcsa_id, f"{context} source differs")
    for field in ("uri", "retrieval_status", "retrieved_at", "license", "attribution", "change_notice"):
        _string(source[field], f"{context}.source.{field}")
    _sha(source["snapshot_sha256"], f"{context}.source.snapshot_sha256")
    _sha(source["entry_response_sha256"], f"{context}.source.entry_response_sha256")
    _positive_int(source["snapshot_bytes"], f"{context}.source.snapshot_bytes")
    probe_identity = _exact(
        source["probe_identity"],
        {
            "mcsa_id",
            "source_entry_url",
            "mechanism_ids",
            "mechanism_step_ids",
            "source_step_count",
            "terminal_source_step_keys",
        },
        f"{context}.source.probe_identity",
    )
    _require(probe_identity["mcsa_id"] == int(mcsa_id[1:]), f"{context} probe identity differs")
    _string(probe_identity["source_entry_url"], f"{context}.source.probe_identity.source_entry_url")
    expected_mechanism_ids = probe_identity["mechanism_ids"]
    _require(
        isinstance(expected_mechanism_ids, list)
        and expected_mechanism_ids == sorted(mechanism_ids),
        f"{context} source mechanism alternatives differ",
    )
    step_sets = probe_identity["mechanism_step_ids"]
    _require(isinstance(step_sets, list), f"{context} source step identity is invalid")
    expected_step_ids: dict[int, list[int]] = {}
    for item in step_sets:
        item = _exact(item, {"mechanism_id", "step_ids"}, f"{context}.source.probe_step_set")
        mechanism_id = _positive_int(item["mechanism_id"], f"{context}.source.probe_step_set.mechanism_id")
        _require(
            isinstance(item["step_ids"], list)
            and item["step_ids"]
            and all(isinstance(value, int) and not isinstance(value, bool) and value > 0 for value in item["step_ids"])
            and len(item["step_ids"]) == len(set(item["step_ids"])),
            f"{context} source step IDs are invalid",
        )
        expected_step_ids[mechanism_id] = item["step_ids"]
    _require(set(expected_step_ids) == mechanism_ids, f"{context} source step mechanisms differ")
    proposals_by_id = {item["source_mechanism_id"]: item for item in proposals}
    for mechanism_id, expected_ids in expected_step_ids.items():
        proposal = proposals_by_id[mechanism_id]
        actual_ids = [step["source_step_id"] for step in proposal["mechanism_steps"]]
        actual_ids += proposal["terminal_state_source_step_ids"]
        _require(
            sorted(actual_ids) == sorted(expected_ids),
            f"{context} omits or invents source steps for mechanism {mechanism_id}",
        )
    _require(
        probe_identity["source_step_count"] == sum(len(value) for value in expected_step_ids.values()),
        f"{context} source step count differs",
    )
    expected_terminal_keys = sorted(
        (
            item["mechanism_id"],
            item["step_id"],
        )
        for item in probe_identity["terminal_source_step_keys"]
    )
    actual_terminal_keys = sorted(
        (proposal["source_mechanism_id"], source_step_id)
        for proposal in proposals
        for source_step_id in proposal["terminal_state_source_step_ids"]
    )
    _require(actual_terminal_keys == expected_terminal_keys, f"{context} terminal source steps differ")
    inventory = source["source_step_inventory"]
    _require(isinstance(inventory, list), f"{context}.source.source_step_inventory is invalid")
    inventory_index: dict[tuple[int, int], dict[str, Any]] = {}
    for item in inventory:
        item = _exact(
            item,
            {
                "source_mechanism_id",
                "source_step_id",
                "is_terminal_state",
                "flow_parse_status",
                "source_scheme_sha256",
                "electron_flow_count",
            },
            f"{context}.source.source_step_inventory[]",
        )
        key = (
            _positive_int(item["source_mechanism_id"], f"{context}.inventory.mechanism_id"),
            _positive_int(item["source_step_id"], f"{context}.inventory.step_id"),
        )
        _require(key not in inventory_index, f"{context} repeats a source step inventory key")
        _require(isinstance(item["is_terminal_state"], bool), f"{context} terminal flag is invalid")
        _string(item["flow_parse_status"], f"{context}.inventory.flow_parse_status")
        if item["source_scheme_sha256"] is not None:
            _sha(item["source_scheme_sha256"], f"{context}.inventory.source_scheme_sha256")
        _require(
            item["electron_flow_count"] is None
            or (
                isinstance(item["electron_flow_count"], int)
                and not isinstance(item["electron_flow_count"], bool)
                and item["electron_flow_count"] >= 0
            ),
            f"{context} source flow count is invalid",
        )
        inventory_index[key] = item
    _require(
        set(inventory_index)
        == {(mechanism_id, step_id) for mechanism_id, ids in expected_step_ids.items() for step_id in ids},
        f"{context} source step inventory coverage differs",
    )
    for proposal in proposals:
        mechanism_id = proposal["source_mechanism_id"]
        for step in proposal["mechanism_steps"]:
            expected = inventory_index[(mechanism_id, step["source_step_id"])]
            _require(expected["is_terminal_state"] is False, f"{context} emits a terminal step as chemistry")
            _require(step["scheme_status"] == expected["flow_parse_status"], f"{context} step parse status differs")
            _require(step["source_scheme_sha256"] == expected["source_scheme_sha256"], f"{context} step scheme hash differs")
            if expected["electron_flow_count"] is not None:
                _require(
                    len(step["electron_flows"]) == expected["electron_flow_count"],
                    f"{context} omits or invents source electron flows",
                )
    _validate_claim_boundary(record["claim_boundary"], f"{context}.claim_boundary")
    provenance = _exact(
        record["provenance"],
        {
            "compiler_version",
            "requested_operation",
            "allowed_operations",
            "case_control_sha256",
            "source_snapshot_sha256",
            "source_manifest_sha256",
            "source_snapshot_set_sha256",
            "development_gate_status_sha256",
            "state_probe_report_sha256",
            "source_projection_sha256",
            "state_context_sha256",
        },
        f"{context}.provenance",
    )
    _require(provenance["compiler_version"] == COMPILER_VERSION, f"{context} compiler differs")
    _require(provenance["requested_operation"] == operation, f"{context} requested operation differs")
    allowed_operations = _strings(provenance["allowed_operations"], f"{context}.allowed_operations", minimum=1)
    _require(set(allowed_operations) <= OPERATIONS and operation in allowed_operations, f"{context} operation lacks permission")
    for key in (
        "case_control_sha256",
        "source_snapshot_sha256",
        "source_manifest_sha256",
        "source_snapshot_set_sha256",
        "development_gate_status_sha256",
        "state_probe_report_sha256",
        "source_projection_sha256",
        "state_context_sha256",
    ):
        _sha(provenance[key], f"{context}.provenance.{key}")
    _require(provenance["source_snapshot_sha256"] == source["snapshot_sha256"], f"{context} source hash binding differs")
    _require(provenance["source_manifest_sha256"] == bundle["source_manifest_sha256"], f"{context} manifest binding differs")
    _require(provenance["source_snapshot_set_sha256"] == bundle["source_snapshot_set_sha256"], f"{context} snapshot-set binding differs")
    _require(provenance["development_gate_status_sha256"] == bundle["input_bindings"]["development_gate_status"], f"{context} gate binding differs")
    _require(provenance["state_probe_report_sha256"] == bundle["input_bindings"]["state_probe_report"], f"{context} probe binding differs")
    expected_case_control = {
        "mcsa_id": mcsa_id,
        "scope": record["source_scope"],
        "allowed_operations": provenance["allowed_operations"],
        "mandatory_abstentions": record["mandatory_abstentions"],
    }
    _require(
        provenance["case_control_sha256"] == _value_sha256(expected_case_control),
        f"{context} scope or abstention binding differs",
    )
    _require(
        provenance["source_projection_sha256"]
        == _value_sha256(
            {
                "reaction_context": record["reaction_context"],
                "mechanism_proposals": record["mechanism_proposals"],
                "source_residue_assertions": record["source_residue_assertions"],
            }
        ),
        f"{context} source projection binding differs",
    )
    _require(
        provenance["state_context_sha256"] == _value_sha256(record["state_context"]),
        f"{context} state-context binding differs",
    )


def validate_source_drafts(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate a self-contained draft bundle without repository or network access."""

    bundle = _exact(
        bundle,
        {
            "schema_version",
            "bundle_id",
            "record_schema_version",
            "source_manifest_sha256",
            "source_snapshot_set_sha256",
            "input_bindings",
            "selection",
            "records",
            "summary",
            "claim_boundary",
            "review_independence",
        },
        "bundle",
    )
    _require(bundle["schema_version"] == BUNDLE_SCHEMA_VERSION, "unsupported source-draft bundle schema")
    _string(bundle["bundle_id"], "bundle.bundle_id")
    _require(bundle["record_schema_version"] == RECORD_SCHEMA_VERSION, "bundle record schema differs")
    _sha(bundle["source_manifest_sha256"], "bundle.source_manifest_sha256")
    _sha(bundle["source_snapshot_set_sha256"], "bundle.source_snapshot_set_sha256")
    bindings = _exact(
        bundle["input_bindings"],
        {"development_gate_status", "state_probe_report", "source_manifest", "record_schema"},
        "bundle.input_bindings",
    )
    for key, value in bindings.items():
        _sha(value, f"bundle.input_bindings.{key}")
    _require(bindings["source_manifest"] == bundle["source_manifest_sha256"], "bundle manifest hash differs")
    selection = _exact(
        bundle["selection"],
        {"basis", "requested_operation", "record_ids", "case_bindings"},
        "bundle.selection",
    )
    _string(selection["basis"], "bundle.selection.basis")
    requested_operation = selection["requested_operation"]
    _require(requested_operation in OPERATIONS, "bundle selection operation is unsupported")
    record_ids = _strings(selection["record_ids"], "bundle.selection.record_ids", minimum=1)
    _require(all(_MCSA_RE.fullmatch(value) for value in record_ids), "bundle selection ID is invalid")
    records = bundle["records"]
    _require(isinstance(records, list), "bundle.records must be an array")
    _require(len(records) == len(record_ids), "bundle record count differs from selection")
    for index, record in enumerate(records):
        _validate_record(record, bundle=bundle, context=f"bundle.records[{index}]")
    _require([record["mcsa_id"] for record in records] == record_ids, "bundle record order or coverage differs")
    _require(all(record["object_type"] == requested_operation for record in records), "bundle mixes unrequested operations")
    _require(len({record["record_id"] for record in records}) == len(records), "bundle repeats record_id")
    case_bindings = selection["case_bindings"]
    _require(isinstance(case_bindings, list) and len(case_bindings) == len(records), "bundle case bindings differ")
    expected_case_bindings = [
        {
            "mcsa_id": record["mcsa_id"],
            "case_control_sha256": record["provenance"]["case_control_sha256"],
            "source_snapshot_sha256": record["source"]["snapshot_sha256"],
        }
        for record in records
    ]
    _require(case_bindings == expected_case_bindings, "bundle case/source bindings differ")
    _require(bundle["summary"] == _summary(records), "bundle summary differs from records")
    _validate_claim_boundary(bundle["claim_boundary"], "bundle.claim_boundary")
    review = _exact(
        bundle["review_independence"],
        {
            "reviewer_kind",
            "blind_review",
            "statistically_independent",
            "correlated_error_risk",
            "independent_human_reviewer_count",
        },
        "bundle.review_independence",
    )
    _require(review["reviewer_kind"] == "same_model_computational_agents", "reviewer kind differs")
    _require(review["blind_review"] is False, "bundle incorrectly claims blind review")
    _require(review["statistically_independent"] is False, "bundle incorrectly claims independence")
    _require(review["correlated_error_risk"] is True, "bundle hides correlated error risk")
    _require(review["independent_human_reviewer_count"] == 0, "bundle incorrectly claims human review")
    return copy.deepcopy(bundle["summary"])
