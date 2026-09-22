"""Fixed opt-in queries over unreviewed raw-stereo transition candidates.

The installed package contains compiled covalent projections and the exact raw
context delta that blocked the ordinary context-candidate path.  It does not
contain the retained M-CSA snapshot bytes.  Repository tests reconstruct every
compiled row from those retained bytes; installed-wheel validation checks the
compiled payload, its source-draft binding, and its derivation fingerprints.

This module deliberately does not widen the frozen candidate-event catalog or
the default pattern query.  Its only query entry point is private and loads a
fixed packaged payload rather than accepting caller-supplied candidate rows.
"""

from __future__ import annotations

from collections import Counter
import copy
import hashlib
from importlib.resources import files
import json
import re
from typing import Any

from .atlas_candidate_events import _event, canonical_bytes
from .atlas_candidate_extraction import (
    _decode_snapshot,
    _select_steps,
    _standard_edits,
    extract_panel_candidate,
)
from .atlas_candidate_patterns import (
    _WorkBudget,
    _matches_for_rows,
    _query_semantics,
    _validate_query_inputs,
)
from .atlas_context_candidates import (
    _parse_panel,
    _private_snapshot,
    _strict_snapshot,
    extract_context_panel_candidate,
)
from .atlas_drafts import validate_source_drafts
from .atlas_partial_panels import (
    _unique_locator_map,
    _validate_flow_rows,
    _validate_nodes,
    derive_partial_panel_coverage,
)
from .atlas_transformations import _validate_graph


SCHEMA_VERSION = "catalytic-earth.stereo-transition-source-candidates.v1"
QUERY_SCHEMA_VERSION = (
    "catalytic-earth.candidate-pattern-query.opt-in-source-candidates.v1"
)
PACKAGE_ID = "atlas-raw-stereo-transition-source-candidates-v1"

_DATA_PREFIX = "candidate_event_data/"
_PAYLOAD_NAME = "stereo_transition_candidates.json"
_ATTRIBUTION_NAME = "stereo_transition_attribution.md"
_EXPECTED_NAME = "stereo_transition_expected.json"
_DRAFT_NAME = "plp_pyruvoyl.json"
_DRAFT_PATH = "src/catalytic_earth/draft_data/plp_pyruvoyl.json"

_SHA = re.compile(r"[0-9a-f]{64}")
_MCSA_ID = re.compile(r"M[0-9]{4}")
_SUPPORTS = ("after_graph_confirmed", "source_arrow_only")

_AUDIT_BOUNDARY = {
    "computationally_checked": True,
    "audit_independence": "same_model_only",
    "independent_scientific_review": False,
    "reviewed_evidence": False,
    "stereochemistry_interpreted": False,
    "achirality_inferred": False,
    "development_material": True,
    "held_out_transfer_claim": False,
    "original_source_bytes_packaged": False,
    "original_source_hashes_recomputed_at_runtime": False,
}

_ROW_SCOPE = {
    "unreviewed_source_candidate": True,
    "computationally_checked": True,
    "same_model_audit_only": True,
    "independent_scientific_review": False,
    "reviewed_evidence": False,
    "physical_atom_map": False,
    "canonical_participant_correspondence": False,
    "stereochemistry_interpreted": False,
    "achirality_inferred": False,
    "development_material": True,
    "held_out_transfer_claim": False,
    "complete_mechanism_path": False,
    "experimentally_validated": False,
}

_PANEL_SCOPE = {
    "unreviewed_candidate": True,
    "reviewed_evidence": False,
    "physical_atom_map": False,
    "canonical_participant_correspondence": False,
    "source_omission_is_atom_deletion": False,
    "synthesized_product_graph": False,
    "stereochemistry_assignment": False,
    "lone_pair_annotations_replayed": False,
    "complete_mechanism_path": False,
    "experimentally_validated": False,
}

_DECLARATION_KEYS = {
    "candidate_id",
    "record_id",
    "mechanism_id",
    "before_step_id",
    "source_snapshot_sha256",
    "before_scheme_sha256",
    "after_scheme_sha256",
}
_RAW_BINDING_KEYS = {
    "provider",
    "record_id",
    "snapshot_sha256",
    "mechanism_id",
    "before_step_id",
    "after_step_id",
    "before_scheme_sha256",
    "after_scheme_sha256",
}
_ROW_KEYS = {
    "candidate_id",
    "source_kind",
    "declaration",
    "raw_source_binding",
    "raw_context_candidate_id",
    "raw_context_transition",
    "source_context_sha256",
    "source_context",
    "candidate_sha256",
    "event_count",
    "support_counts",
    "events",
    "candidate",
    "derivation",
    "scope",
}
_PAYLOAD_KEYS = {
    "schema_version",
    "package_id",
    "status",
    "audit_boundary",
    "source_draft_binding",
    "candidate_count",
    "candidates",
}
_PANEL_CANDIDATE_KEYS = {
    "schema_version",
    "candidate_id",
    "status",
    "extraction_status",
    "source_binding",
    "source_panels",
    "correspondence",
    "proposed_graph_edits",
    "source_flow_bindings",
    "coverage",
    "diagnostics",
    "scope_effect",
}
_DERIVATION_KEYS = {
    "raw_context_candidate_sha256",
    "projected_candidate_sha256",
    "raw_context_transition_sha256",
    "source_context_sha256",
    "events_sha256",
}
_TRANSITION_KEYS = {
    "diagnostic",
    "direction",
    "before",
    "after",
    "mapped_endpoint_bindings",
    "touches_proposed_covalent_edit",
    "blocked_context_assessment",
    "interpretation",
}
_SOURCE_CONTEXT_KEYS = {
    "source_draft_bundle_id",
    "record_binding",
    "proposal_binding",
    "source_scope",
    "step_bindings",
    "mandatory_abstentions",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _exact(value: dict[str, Any], keys: set[str], label: str) -> None:
    _require(set(value) == keys, f"{label} fields differ")


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
    return value


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and value != "", f"{label} must be nonempty text")
    return value


def _integer(value: Any, label: str) -> int:
    _require(type(value) is int, f"{label} must be an integer")
    return value


def _digest(value: Any, label: str) -> str:
    text = _string(value, label)
    _require(_SHA.fullmatch(text) is not None, f"{label} must be a lowercase SHA256")
    return text


def _sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _resource_bytes(relative_path: str) -> bytes:
    return files("catalytic_earth").joinpath(relative_path).read_bytes()


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_keys,
            parse_constant=lambda item: (_ for _ in ()).throw(
                ValueError(f"unsupported JSON numeric constant: {item}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is not strict UTF-8 JSON") from error
    return _object(value, label)


def _validate_declaration(value: Any) -> dict[str, Any]:
    row = _object(value, "declaration")
    _exact(row, _DECLARATION_KEYS, "declaration")
    record_id = _string(row["record_id"], "declaration.record_id")
    _require(_MCSA_ID.fullmatch(record_id) is not None, "declaration record ID differs")
    mechanism_id = _integer(row["mechanism_id"], "declaration.mechanism_id")
    before_step = _integer(row["before_step_id"], "declaration.before_step_id")
    _require(mechanism_id > 0 and before_step > 0, "declaration step identity differs")
    expected_id = (
        f"panel-candidate:{record_id}:mechanism-{mechanism_id}:"
        f"steps-{before_step}-{before_step + 1}"
    )
    _require(row["candidate_id"] == expected_id, "declaration candidate ID differs")
    for key in (
        "source_snapshot_sha256",
        "before_scheme_sha256",
        "after_scheme_sha256",
    ):
        _digest(row[key], f"declaration.{key}")
    return row


def _raw_binding(declaration: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": "M-CSA",
        "record_id": declaration["record_id"],
        "snapshot_sha256": declaration["source_snapshot_sha256"],
        "mechanism_id": declaration["mechanism_id"],
        "before_step_id": declaration["before_step_id"],
        "after_step_id": declaration["before_step_id"] + 1,
        "before_scheme_sha256": declaration["before_scheme_sha256"],
        "after_scheme_sha256": declaration["after_scheme_sha256"],
    }


def _source_context(
    binding: dict[str, Any], draft_bundle: dict[str, Any]
) -> dict[str, Any]:
    validate_source_drafts(draft_bundle)
    records = [
        row for row in draft_bundle["records"]
        if row["mcsa_id"] == binding["record_id"]
    ]
    _require(len(records) == 1, "source candidate draft record is missing or repeated")
    record = records[0]
    _require(
        record["source"]["snapshot_sha256"] == binding["snapshot_sha256"],
        "source candidate snapshot binding differs from the compiled draft",
    )
    proposals = [
        row for row in record["mechanism_proposals"]
        if row["source_mechanism_id"] == binding["mechanism_id"]
    ]
    _require(len(proposals) == 1, "source candidate draft proposal is missing or repeated")
    proposal = proposals[0]
    _require(
        proposal["source_record_id"] == binding["record_id"],
        "source candidate draft proposal belongs to another record",
    )
    compiled_steps = {
        row["source_step_id"]: row for row in proposal["mechanism_steps"]
    }
    _require(
        len(compiled_steps) == len(proposal["mechanism_steps"]),
        "source candidate draft proposal repeats a source step",
    )
    steps: list[dict[str, Any]] = []
    for role, step_id, sha_key in (
        ("before", binding["before_step_id"], "before_scheme_sha256"),
        ("after", binding["after_step_id"], "after_scheme_sha256"),
    ):
        step = compiled_steps.get(step_id)
        _require(step is not None, "source candidate panel is absent from the compiled draft")
        _require(
            step["source_scheme_sha256"] == binding[sha_key],
            "source candidate panel hash differs from the compiled draft",
        )
        steps.append({
            "role": role,
            "source_kind": "source_draft_step",
            "step_id": step["step_id"],
            "source_step_id": step_id,
            "scheme_sha256": binding[sha_key],
            "summary": step["summary"],
            "is_inferred": step["is_inferred"],
        })
    return {
        "source_draft_bundle_id": draft_bundle["bundle_id"],
        "record_binding": {
            "record_id": record["record_id"],
            "mcsa_id": record["mcsa_id"],
        },
        "proposal_binding": {
            "proposal_id": proposal["proposal_id"],
            "source_mechanism_id": proposal["source_mechanism_id"],
        },
        "source_scope": record["source_scope"],
        "step_bindings": steps,
        "mandatory_abstentions": copy.deepcopy(record["mandatory_abstentions"]),
    }


def _checked_transition(
    *,
    diagnostic: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    candidate: dict[str, Any],
    assessment: dict[str, Any],
) -> dict[str, Any]:
    _require(
        diagnostic == {
            "code": "opaque_context_changed",
            "detail": "bond_stereo rows change, reverse, repeat, or reorder across the locator map",
        },
        "raw context transition diagnostic differs",
    )
    for side, row in (("before", before), ("after", after)):
        _require(
            set(row) == {
                "scheme_sha256", "bond_stereo", "atom_parity", "bond_conventions",
            }
            and row["atom_parity"] == []
            and row["bond_conventions"] == []
            and isinstance(row["bond_stereo"], list),
            f"raw context {side} fields differ",
        )
    before_rows = before["bond_stereo"]
    after_rows = after["bond_stereo"]
    _require(
        (len(before_rows), len(after_rows)) in {(1, 0), (0, 1)},
        "raw context transition must be one W/H appearance or disappearance",
    )
    direction = "disappearance" if before_rows else "appearance"
    special = (before_rows or after_rows)[0]
    _require(
        set(special) == {
            "bond_id", "ordered_atom_refs2", "order_token", "raw_text", "raw_attributes",
        }
        and special["raw_text"] in {"W", "H"}
        and special["raw_attributes"] == {}
        and special["order_token"] in {"1", "2", "3"},
        "raw context transition uses an unsupported bondStereo row",
    )
    refs = special["ordered_atom_refs2"]
    _require(
        isinstance(refs, list) and len(refs) == 2
        and all(isinstance(item, str) for item in refs),
        "raw context transition endpoints differ",
    )
    source_side = "before_graph" if direction == "disappearance" else "after_graph"
    source_bonds = candidate["source_panels"][source_side]["bonds"]
    matching_bonds = [bond for bond in source_bonds if bond["atom_ids"] == refs]
    _require(
        len(matching_bonds) == 1
        and str(matching_bonds[0]["order"]) == special["order_token"],
        "raw context transition does not bind the declared projected bond/order",
    )
    atom_map = candidate["correspondence"]["atom_map"]
    forward = {row["before_atom_id"]: row["after_atom_id"] for row in atom_map}
    inverse = {right: left for left, right in forward.items()}
    if direction == "disappearance":
        _require(set(refs) <= set(forward), "disappearing raw context endpoints are unmapped")
        mapped = [
            {"before_atom_id": atom_id, "after_atom_id": forward[atom_id]}
            for atom_id in refs
        ]
        before_special = set(refs)
    else:
        _require(set(refs) <= set(inverse), "appearing raw context endpoints are unmapped")
        mapped = [
            {"before_atom_id": inverse[atom_id], "after_atom_id": atom_id}
            for atom_id in refs
        ]
        before_special = {inverse[item] for item in refs}
    edit_atoms = {
        atom_id
        for edit in candidate["proposed_graph_edits"]
        for atom_id in edit["atom_ids"]
    }
    _require(
        bool(before_special & edit_atoms),
        "raw context transition does not touch a proposed covalent edit endpoint",
    )
    before_special_atoms = {
        atom_id for item in before_rows for atom_id in item["ordered_atom_refs2"]
    }
    after_special_atoms = {
        atom_id for item in after_rows for atom_id in item["ordered_atom_refs2"]
    }
    expected_assessment = {
        "status": "needs_review",
        "before_counts": {
            "bond_stereo": len(before_rows),
            "atom_parity": 0,
            "bond_conventions": 0,
        },
        "after_counts": {
            "bond_stereo": len(after_rows),
            "atom_parity": 0,
            "bond_conventions": 0,
        },
        "matched_counts": {},
        "special_before_atom_ids": [
            atom["atom_id"]
            for atom in candidate["source_panels"]["before_graph"]["atoms"]
            if atom["atom_id"] in before_special_atoms
        ],
        "special_after_atom_ids": [
            atom["atom_id"]
            for atom in candidate["source_panels"]["after_graph"]["atoms"]
            if atom["atom_id"] in after_special_atoms
        ],
        "all_references_mapped": True,
        "ordered_metadata_preserved": False,
        "before_special_boundary_bonds": [],
        "after_special_boundary_bonds": [],
        "no_special_boundary_bonds": None,
        "proposed_edit_endpoints_disjoint": None,
        "reason": "bond_stereo rows change, reverse, repeat, or reorder across the locator map",
    }
    _require(assessment == expected_assessment, "raw context blocker assessment differs")
    return {
        "diagnostic": copy.deepcopy(diagnostic),
        "direction": direction,
        "before": copy.deepcopy(before),
        "after": copy.deepcopy(after),
        "mapped_endpoint_bindings": mapped,
        "touches_proposed_covalent_edit": True,
        "blocked_context_assessment": copy.deepcopy(assessment),
        "interpretation": (
            "raw_W_or_H_drawing_token_transition_only_not_stereochemical_assignment"
        ),
    }


def _transition(
    blocked: dict[str, Any], projected: dict[str, Any]
) -> dict[str, Any]:
    _require(
        blocked["status"] == "unreviewed"
        and blocked["extraction_status"] == "needs_review"
        and len(blocked["diagnostics"]) == 1,
        "raw context candidate does not have the expected blocker",
    )
    context = _object(blocked["opaque_source_context"], "opaque_source_context")
    return _checked_transition(
        diagnostic=_object(blocked["diagnostics"][0], "raw context diagnostic"),
        before=_object(context.get("before"), "opaque_source_context.before"),
        after=_object(context.get("after"), "opaque_source_context.after"),
        candidate=projected,
        assessment=_object(
            blocked["context_preservation"], "blocked context assessment"
        ),
    )


def _derive_row(
    raw_snapshot: bytes,
    declaration: dict[str, Any],
    verified_draft_bundle: dict[str, Any],
) -> dict[str, Any]:
    """Reconstruct one compiled row from retained repository source bytes."""

    declared = copy.deepcopy(_validate_declaration(declaration))
    _require(
        hashlib.sha256(raw_snapshot).hexdigest() == declared["source_snapshot_sha256"],
        "retained source snapshot differs from its declaration",
    )
    strict = _strict_snapshot(raw_snapshot)
    decoded, record_id = _decode_snapshot(raw_snapshot)
    _require(strict == decoded, "strict and ordinary source decoders differ")
    _require(record_id == declared["record_id"], "retained source record differs")
    before, after = _select_steps(
        strict, declared["mechanism_id"], declared["before_step_id"]
    )
    _require(
        before["content_sha256"] == declared["before_scheme_sha256"]
        and after["content_sha256"] == declared["after_scheme_sha256"],
        "retained source panel hashes differ from the declaration",
    )
    blocked = extract_context_panel_candidate(
        raw_snapshot,
        mechanism_id=declared["mechanism_id"],
        before_step_id=declared["before_step_id"],
    )
    before_context, before_projection = _parse_panel(
        before["content_utf8"], before["content_sha256"], "before"
    )
    after_context, after_projection = _parse_panel(
        after["content_utf8"], after["content_sha256"], "after"
    )
    _require(
        blocked["opaque_source_context"] == {
            "before": before_context,
            "after": after_context,
        },
        "raw context capture differs from the explicit panel parse",
    )
    private_snapshot = _private_snapshot(
        strict,
        declared["mechanism_id"],
        {
            before["step_id"]: before_projection,
            after["step_id"]: after_projection,
        },
    )
    projected = extract_panel_candidate(
        private_snapshot,
        mechanism_id=declared["mechanism_id"],
        before_step_id=declared["before_step_id"],
    )
    _require(
        projected["candidate_id"] == declared["candidate_id"]
        and projected["status"] == "unreviewed"
        and projected["extraction_status"] == "candidate"
        and projected["diagnostics"] == [],
        "covalent projection did not yield the declared unreviewed candidate",
    )
    raw_binding = _raw_binding(declared)
    _require(
        blocked["source_binding"] == raw_binding,
        "raw context candidate source binding differs",
    )
    source_context = _source_context(raw_binding, verified_draft_bundle)
    transition = _transition(blocked, projected)
    before_atoms = {
        atom["atom_id"]: atom
        for atom in projected["source_panels"]["before_graph"]["atoms"]
    }
    events = [
        _event(projected["candidate_id"], edit, before_atoms)
        for edit in projected["proposed_graph_edits"]
    ]
    support_counts_raw = Counter(item["support"] for item in events)
    support_counts = {
        support: support_counts_raw.get(support, 0) for support in _SUPPORTS
    }
    candidate_sha = _sha(projected)
    context_sha = _sha(source_context)
    transition_sha = _sha(transition)
    events_sha = _sha(events)
    blocked_sha = _sha(blocked)
    return {
        "candidate_id": projected["candidate_id"],
        "source_kind": "raw_stereo_transition_candidate",
        "declaration": declared,
        "raw_source_binding": raw_binding,
        "raw_context_candidate_id": blocked["candidate_id"],
        "raw_context_transition": transition,
        "source_context_sha256": context_sha,
        "source_context": source_context,
        "candidate_sha256": candidate_sha,
        "event_count": len(events),
        "support_counts": support_counts,
        "events": events,
        "candidate": projected,
        "derivation": {
            "raw_context_candidate_sha256": blocked_sha,
            "projected_candidate_sha256": candidate_sha,
            "raw_context_transition_sha256": transition_sha,
            "source_context_sha256": context_sha,
            "events_sha256": events_sha,
        },
        "scope": copy.deepcopy(_ROW_SCOPE),
    }


def _validate_transition(
    value: Any,
    candidate: dict[str, Any],
    raw_binding: dict[str, Any],
) -> dict[str, Any]:
    row = _object(value, "raw_context_transition")
    _exact(row, _TRANSITION_KEYS, "raw_context_transition")
    before = _object(row["before"], "raw_context_transition.before")
    after = _object(row["after"], "raw_context_transition.after")
    _require(
        before.get("scheme_sha256") == raw_binding["before_scheme_sha256"]
        and after.get("scheme_sha256") == raw_binding["after_scheme_sha256"],
        "raw context panel binding differs",
    )
    checked = _checked_transition(
        diagnostic=_object(row["diagnostic"], "raw_context_transition.diagnostic"),
        before=before,
        after=after,
        candidate=candidate,
        assessment=_object(
            row["blocked_context_assessment"], "blocked_context_assessment"
        ),
    )
    _require(checked == row, "compiled raw context transition derivation differs")
    return row


def _validate_row(value: Any, draft_bundle: dict[str, Any]) -> dict[str, Any]:
    row = _object(value, "stereo transition candidate")
    _exact(row, _ROW_KEYS, "stereo transition candidate")
    declaration = _validate_declaration(row["declaration"])
    _require(
        row["candidate_id"] == declaration["candidate_id"]
        and row["source_kind"] == "raw_stereo_transition_candidate",
        "stereo transition candidate identity differs",
    )
    raw_binding = _object(row["raw_source_binding"], "raw_source_binding")
    _exact(raw_binding, _RAW_BINDING_KEYS, "raw_source_binding")
    _require(raw_binding == _raw_binding(declaration), "raw source binding differs")
    expected_context_id = (
        f"panel-context-candidate:{declaration['record_id']}:"
        f"mechanism-{declaration['mechanism_id']}:"
        f"steps-{declaration['before_step_id']}-{declaration['before_step_id'] + 1}"
    )
    _require(
        row["raw_context_candidate_id"] == expected_context_id,
        "raw context candidate ID differs",
    )
    source_context = _object(row["source_context"], "source_context")
    _exact(source_context, _SOURCE_CONTEXT_KEYS, "source_context")
    expected_context = _source_context(raw_binding, draft_bundle)
    _require(source_context == expected_context, "compiled source context differs")
    _require(
        row["source_context_sha256"] == _sha(source_context),
        "compiled source context hash differs",
    )

    candidate = _object(row["candidate"], "candidate")
    _exact(candidate, _PANEL_CANDIDATE_KEYS, "candidate")
    _require(
        candidate["schema_version"] == "catalytic-earth.panel-candidate.v1"
        and candidate["candidate_id"] == row["candidate_id"]
        and candidate["status"] == "unreviewed"
        and candidate["extraction_status"] == "candidate"
        and candidate["diagnostics"] == []
        and candidate["scope_effect"] == _PANEL_SCOPE,
        "compiled projected candidate boundary differs",
    )
    projected_binding = _object(candidate["source_binding"], "candidate.source_binding")
    _exact(projected_binding, _RAW_BINDING_KEYS, "candidate.source_binding")
    _require(
        projected_binding["provider"] == raw_binding["provider"] == "M-CSA"
        and projected_binding["record_id"] == raw_binding["record_id"]
        and projected_binding["mechanism_id"] == raw_binding["mechanism_id"]
        and projected_binding["before_step_id"] == raw_binding["before_step_id"]
        and projected_binding["after_step_id"] == raw_binding["after_step_id"],
        "projected candidate selects another source pair",
    )
    for key in (
        "snapshot_sha256", "before_scheme_sha256", "after_scheme_sha256"
    ):
        _digest(projected_binding[key], f"candidate.source_binding.{key}")
    _require(
        projected_binding["snapshot_sha256"] != raw_binding["snapshot_sha256"],
        "covalent projection is misrepresented as the raw source snapshot",
    )
    _require(
        row["candidate_sha256"] == _sha(candidate),
        "compiled projected candidate hash differs",
    )
    panels = _object(candidate["source_panels"], "candidate.source_panels")
    _exact(
        panels,
        {"before_graph", "after_graph", "before_nodes", "after_nodes"},
        "candidate.source_panels",
    )
    before_graph = _validate_graph(
        copy.deepcopy(panels["before_graph"]), "candidate.before_graph"
    )
    after_graph = _validate_graph(
        copy.deepcopy(panels["after_graph"]), "candidate.after_graph"
    )
    before_nodes = _validate_nodes(
        copy.deepcopy(panels["before_nodes"]), before_graph, "candidate.before_nodes"
    )
    after_nodes = _validate_nodes(
        copy.deepcopy(panels["after_nodes"]), after_graph, "candidate.after_nodes"
    )
    before_atoms = {
        atom["atom_id"]: atom for atom in before_graph["atoms"]
    }
    _require(bool(before_atoms), "compiled projected candidate has no before atoms")
    _require(
        all(atom.get("stereochemistry") is None for atom in before_atoms.values())
        and all(
            atom.get("stereochemistry") is None
            for atom in after_graph["atoms"]
        ),
        "compiled projected candidate asserts stereochemistry",
    )
    correspondence = _object(candidate["correspondence"], "candidate.correspondence")
    _require(
        correspondence.get("method") == "unique_exact_source_position_and_identity"
        and correspondence.get("interpretation")
        == "project_unreviewed_panel_alignment_not_physical_atom_map"
        and correspondence.get("ambiguous_matches") == []
        and isinstance(correspondence.get("atom_map"), list)
        and bool(correspondence["atom_map"]),
        "compiled projected correspondence differs",
    )
    _require(
        correspondence["atom_map"]
        == _unique_locator_map(before_graph, after_graph, before_nodes, after_nodes),
        "compiled projected correspondence is not the exhaustive unique locator map",
    )
    edits = _array(candidate["proposed_graph_edits"], "candidate.proposed_graph_edits")
    _require(bool(edits), "compiled projected candidate has no edits")
    derived_events = [
        _event(candidate["candidate_id"], edit, before_atoms) for edit in edits
    ]
    _require(row["events"] == derived_events, "compiled literal event rows differ")
    _require(
        row["event_count"] == len(derived_events),
        "compiled literal event count differs",
    )
    counts = Counter(item["support"] for item in derived_events)
    expected_counts = {support: counts.get(support, 0) for support in _SUPPORTS}
    _require(row["support_counts"] == expected_counts, "compiled support counts differ")
    atom_map = correspondence["atom_map"]
    before_count = len(before_graph["atoms"])
    after_count = len(after_graph["atoms"])
    _require(
        len(atom_map) < before_count or len(atom_map) < after_count,
        "stereo transition adapter expects an explicitly partial covalent projection",
    )
    standard_edits = _standard_edits(edits)
    _validate_flow_rows(
        candidate["source_flow_bindings"],
        standard_edits,
        source_step_id=raw_binding["before_step_id"],
    )
    derived_coverage = derive_partial_panel_coverage(
        before_graph,
        after_graph,
        atom_map,
        standard_edits,
        candidate["source_flow_bindings"],
    )
    _require(
        candidate["coverage"] == derived_coverage
        and derived_coverage["projection_replays_exactly"] is True
        and derived_coverage["full_panel_replay_asserted"] is False,
        "compiled projected coverage differs",
    )
    confirmed_ids = [
        edit["edit_id"]
        for edit in edits
        if edit["support"] == "after_graph_confirmed"
    ]
    arrow_only_ids = [
        edit["edit_id"]
        for edit in edits
        if edit["support"] == "source_arrow_only"
    ]
    _require(
        confirmed_ids == derived_coverage["replayed_edit_ids"]
        and arrow_only_ids == derived_coverage["after_graph_unverified_edit_ids"],
        "compiled edit support labels differ from mapped-node coverage",
    )
    transition = _validate_transition(
        row["raw_context_transition"], candidate, raw_binding
    )
    derivation = _object(row["derivation"], "derivation")
    _exact(derivation, _DERIVATION_KEYS, "derivation")
    for key in _DERIVATION_KEYS:
        _digest(derivation[key], f"derivation.{key}")
    _require(
        derivation["projected_candidate_sha256"] == _sha(candidate)
        and derivation["raw_context_transition_sha256"] == _sha(transition)
        and derivation["source_context_sha256"] == _sha(source_context)
        and derivation["events_sha256"] == _sha(derived_events),
        "compiled derivation fingerprints differ",
    )
    _require(row["scope"] == _ROW_SCOPE, "stereo transition candidate scope differs")
    return row


def _validate_payload(
    value: Any,
    draft_bundle: dict[str, Any],
    *,
    draft_bundle_sha256: str,
) -> dict[str, Any]:
    payload = _object(value, "stereo transition source candidates")
    _exact(payload, _PAYLOAD_KEYS, "stereo transition source candidates")
    _require(
        payload["schema_version"] == SCHEMA_VERSION
        and payload["package_id"] == PACKAGE_ID
        and payload["status"] == "unreviewed",
        "stereo transition source-candidate package identity differs",
    )
    _require(payload["audit_boundary"] == _AUDIT_BOUNDARY, "audit boundary differs")
    draft_binding = _object(payload["source_draft_binding"], "source_draft_binding")
    _exact(draft_binding, {"bundle_id", "path", "sha256"}, "source_draft_binding")
    _require(
        draft_binding == {
            "bundle_id": draft_bundle["bundle_id"],
            "path": _DRAFT_PATH,
            "sha256": draft_bundle_sha256,
        },
        "source-draft package binding differs",
    )
    rows = _array(payload["candidates"], "candidates")
    _require(
        bool(rows) and payload["candidate_count"] == len(rows),
        "stereo transition source-candidate count differs",
    )
    seen: set[str] = set()
    for raw in rows:
        row = _validate_row(raw, draft_bundle)
        candidate_id = row["candidate_id"]
        _require(candidate_id not in seen, "stereo transition candidate repeats")
        seen.add(candidate_id)
    return {
        "package_id": payload["package_id"],
        "candidate_count": len(rows),
        "candidate_ids": sorted(seen),
    }


def _load_verified_draft_bundle() -> tuple[dict[str, Any], str]:
    # Import locally so the fixed-resource loader can reuse the installed core
    # verification path without creating a module-import cycle.
    from .core_cli import verified_source_drafts

    raw = _resource_bytes("draft_data/" + _DRAFT_NAME)
    return verified_source_drafts("plp-pyruvoyl"), hashlib.sha256(raw).hexdigest()


def _load_packaged() -> tuple[dict[str, Any], dict[str, Any]]:
    expected = _strict_json(
        _resource_bytes(_DATA_PREFIX + _EXPECTED_NAME),
        "stereo transition expected file",
    )
    _require(
        expected.get("schema_version")
        == "catalytic-earth.stereo-transition-source-candidate-package.v1"
        and expected.get("package_id") == PACKAGE_ID,
        "unsupported stereo transition source-candidate package",
    )
    raw = _resource_bytes(_DATA_PREFIX + _PAYLOAD_NAME)
    attribution = _resource_bytes(_DATA_PREFIX + _ATTRIBUTION_NAME)
    package_sha = hashlib.sha256(raw).hexdigest()
    _require(
        package_sha == expected.get("payload_sha256"),
        "stereo transition candidate payload differs from its expected hash",
    )
    _require(
        hashlib.sha256(attribution).hexdigest()
        == expected.get("attribution_sha256"),
        "stereo transition attribution differs from its expected hash",
    )
    payload = _strict_json(raw, "stereo transition candidate payload")
    _require(
        canonical_bytes(payload) == raw,
        "stereo transition candidate payload is not canonical JSON",
    )
    draft_bundle, draft_sha = _load_verified_draft_bundle()
    summary = _validate_payload(
        payload, draft_bundle, draft_bundle_sha256=draft_sha
    )
    _require(
        expected.get("candidate_count") == summary["candidate_count"]
        and expected.get("candidate_ids") == summary["candidate_ids"],
        "stereo transition admitted identities differ from the expected file",
    )
    return payload, {**summary, "package_sha256": package_sha}


def _query_with_packaged_stereo_transitions(
    value: dict[str, Any],
    *,
    clauses: list[dict[str, Any]],
    mcsa_id: str | None = None,
    support: str = "after_graph_confirmed",
) -> dict[str, Any]:
    """Opt in to the fixed compiled rows while retaining separate identities."""

    catalog_summary, normalized, normalized_mcsa = _validate_query_inputs(
        value, clauses=clauses, mcsa_id=mcsa_id, support=support
    )
    payload, witness_summary = _load_packaged()
    budget = _WorkBudget()
    raw_base_matches = _matches_for_rows(
        value["candidates"], normalized, support, normalized_mcsa, budget
    )
    raw_witness_matches = _matches_for_rows(
        payload["candidates"], normalized, support, normalized_mcsa, budget
    )
    base_matches = [
        {
            "source_kind": "frozen_v1_catalog",
            "source_id": catalog_summary["catalog_id"],
            **copy.deepcopy(match),
        }
        for match in raw_base_matches
    ]
    witness_matches = [
        {
            "source_kind": "raw_stereo_transition_candidates",
            "source_id": witness_summary["package_id"],
            **copy.deepcopy(match),
        }
        for match in raw_witness_matches
    ]
    matches = [*base_matches, *witness_matches]
    source_match_counts = {
        "frozen_v1_catalog": {
            "matched_candidate_count": len(base_matches),
            "binding_count": sum(len(item["bindings"]) for item in base_matches),
        },
        "raw_stereo_transition_candidates": {
            "matched_candidate_count": len(witness_matches),
            "binding_count": sum(
                len(item["bindings"]) for item in witness_matches
            ),
        },
    }
    return {
        "schema_version": QUERY_SCHEMA_VERSION,
        "status": "unreviewed",
        "sources": {
            "frozen_v1_catalog": {
                "catalog_id": catalog_summary["catalog_id"],
                "catalog_sha256": catalog_summary["catalog_sha256"],
                "catalog_candidate_count": len(value["candidates"]),
            },
            "raw_stereo_transition_candidates": {
                "package_id": witness_summary["package_id"],
                "package_sha256": witness_summary["package_sha256"],
                "admitted_candidate_ids": witness_summary["candidate_ids"],
                "source_candidate_count": witness_summary["candidate_count"],
                **copy.deepcopy(_AUDIT_BOUNDARY),
            },
        },
        "filters": {
            "clauses": copy.deepcopy(normalized),
            "mcsa_id": normalized_mcsa,
            "support": support,
        },
        "query_semantics": {
            **_query_semantics(),
            "source_union_is_catalog": False,
            "raw_stereo_transition_is_interpreted": False,
            "raw_source_bindings_are_packaged_provenance": True,
            "original_source_hashes_recomputed_at_runtime": False,
        },
        "matched_candidate_count": len(matches),
        "binding_count": sum(len(match["bindings"]) for match in matches),
        "source_match_counts": source_match_counts,
        "matches": matches,
    }


__all__: list[str] = []
