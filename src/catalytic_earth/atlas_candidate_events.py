"""Literal event indexing for unreviewed source-panel candidates.

The catalog retains every accepted context-candidate payload and every source
edit witness.  Its signatures remove panel-local atom identifiers only; they
do not assert mechanistic equivalence, shared atoms between clauses, or missing
chemistry when a query is empty.
"""

from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any


CATALOG_SCHEMA_VERSION = "catalytic-earth.candidate-event-catalog.v1"
QUERY_SCHEMA_VERSION = "catalytic-earth.candidate-event-query.v1"
CATALOG_ID = "atlas-context-candidate-events-v1"

_CANDIDATE_SCHEMA_VERSION = "catalytic-earth.context-panel-candidate.v1"
_SUPPORTS = ("after_graph_confirmed", "source_arrow_only")
_SUPPORT_FILTERS = frozenset((*_SUPPORTS, "any"))
_SHA = re.compile(r"[0-9a-f]{64}")
_MCSA_ID = re.compile(r"M[0-9]{4}")
_ELEMENTS = frozenset(
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co "
    "Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb "
    "Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os "
    "Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md "
    "No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()
)
_GRAPH_ELEMENTS = _ELEMENTS | {"R"}
_CATALOG_IMPLEMENTATION_PATHS = {
    "scripts/build_atlas_candidate_events.py",
    "src/catalytic_earth/atlas_candidate_events.py",
}

_CATALOG_KEYS = {
    "schema_version", "catalog_id", "status", "provenance", "candidate_count",
    "event_count", "support_counts", "scope", "candidates",
}
_ROW_KEYS = {
    "candidate_id", "candidate_sha256", "source_context_sha256",
    "source_context", "event_count", "support_counts", "events", "candidate",
}
_EVENT_KEYS = {
    "event_id", "edit_id", "support", "source_edit", "signature",
}
_CANDIDATE_KEYS = {
    "schema_version", "candidate_id", "status", "extraction_status",
    "source_binding", "source_panels", "correspondence",
    "proposed_graph_edits", "source_flow_bindings", "coverage", "diagnostics",
    "scope_effect", "opaque_source_context", "context_preservation",
}
_SOURCE_BINDING_KEYS = {
    "provider", "record_id", "snapshot_sha256", "mechanism_id",
    "before_step_id", "after_step_id", "before_scheme_sha256",
    "after_scheme_sha256",
}
_EDIT_KEYS = {
    "edit_id", "operation", "atom_ids", "before", "after",
    "source_flow_id", "support",
}
_GRAPH_KEYS = {"graph_id", "atom_id_scope", "atoms", "bonds"}
_ATOM_KEYS = {"atom_id", "element", "formal_charge", "stereochemistry"}
_BOND_KEYS = {"atom_ids", "order"}
_PROVENANCE_INPUT_KEYS = {
    "context_scan", "source_draft_bundles", "candidate_contexts",
    "catalog_implementation_sha256",
}
_PROVENANCE_KEYS = {
    "context_scan", "source_draft_bundles", "candidate_context_bindings",
    "catalog_implementation_sha256",
}
_SCAN_KEYS = {
    "schema_version", "path", "sha256", "source_registry_sha256",
    "baseline_scan_sha256", "implementation_sha256",
}
_BUNDLE_KEYS = {"bundle_id", "path", "sha256"}
_CONTEXT_INPUT_KEYS = {
    "candidate_id", "candidate_sha256", "source_context_sha256",
    "source_context",
}
_CONTEXT_BINDING_KEYS = {
    "candidate_id", "candidate_sha256", "source_context_sha256",
}
_SOURCE_CONTEXT_KEYS = {
    "source_draft_bundle_id", "record_binding", "proposal_binding",
    "source_scope", "step_bindings", "mandatory_abstentions",
}
_STEP_KEYS = {
    "role", "source_kind", "step_id", "source_step_id", "scheme_sha256",
    "summary", "is_inferred",
}
_CATALOG_SCOPE = {
    "counted_object": "unreviewed_source_panel_edit_event",
    "literal_element_and_state_signatures": True,
    "atom_identifiers_in_signatures": False,
    "events_are_reviewed_evidence": False,
    "shared_signature_implies_mechanism_equivalence": False,
    "candidate_count_is_validated_transition_count": False,
    "empty_result_implies_absence_of_chemistry": False,
}
_REQUIRED_CANDIDATE_SCOPE = {
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
    "opaque_annotations_preserved": True,
    "stereochemistry_interpreted": False,
    "coordination_chemistry_interpreted": False,
    "covalent_graph_excludes_convention_bonds": True,
    "full_source_electronic_state_replayed": False,
}


def canonical_bytes(value: Any) -> bytes:
    """Return the canonical JSON rendering used by the frozen candidate scan."""

    try:
        rendered = json.dumps(
            value, sort_keys=True, indent=2, allow_nan=False,
        ) + "\n"
    except (TypeError, ValueError) as error:
        raise ValueError("value is not canonical JSON") from error
    return rendered.encode("utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
    return value


def _exact(value: dict[str, Any], keys: set[str], label: str) -> None:
    _require(set(value) == keys, f"{label} fields differ")


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and value != "", f"{label} must be a nonempty string")
    return value


def _integer(value: Any, label: str) -> int:
    _require(type(value) is int, f"{label} must be an integer")
    return value


def _digest(value: Any, label: str) -> str:
    text = _string(value, label)
    _require(_SHA.fullmatch(text) is not None, f"{label} must be a lowercase SHA256")
    return text


def _safe_path(value: Any, label: str) -> str:
    text = _string(value, label)
    path = Path(text)
    _require(
        not path.is_absolute() and "\\" not in text and ".." not in path.parts,
        f"{label} must be a safe relative path",
    )
    return text


def _support_counts(events: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(event["support"] for event in events)
    return {support: counts.get(support, 0) for support in _SUPPORTS}


def _validate_graph(value: Any, label: str) -> dict[str, Any]:
    graph = _object(value, label)
    _exact(graph, _GRAPH_KEYS, label)
    _string(graph["graph_id"], f"{label}.graph_id")
    _string(graph["atom_id_scope"], f"{label}.atom_id_scope")
    atoms = _array(graph["atoms"], f"{label}.atoms")
    _require(bool(atoms), f"{label}.atoms is empty")
    atom_ids: set[str] = set()
    for index, raw in enumerate(atoms):
        row_label = f"{label}.atoms[{index}]"
        atom = _object(raw, row_label)
        _exact(atom, _ATOM_KEYS, row_label)
        atom_id = _string(atom["atom_id"], f"{row_label}.atom_id")
        element = _string(atom["element"], f"{row_label}.element")
        _require(atom_id not in atom_ids, f"{label} repeats atom {atom_id}")
        _require(element in _GRAPH_ELEMENTS, f"{row_label}.element is not a supported source atom token")
        _integer(atom["formal_charge"], f"{row_label}.formal_charge")
        _require(atom["stereochemistry"] is None, f"{row_label}.stereochemistry must remain unasserted")
        atom_ids.add(atom_id)
    pairs: set[tuple[str, str]] = set()
    for index, raw in enumerate(_array(graph["bonds"], f"{label}.bonds")):
        row_label = f"{label}.bonds[{index}]"
        bond = _object(raw, row_label)
        _exact(bond, _BOND_KEYS, row_label)
        refs = _array(bond["atom_ids"], f"{row_label}.atom_ids")
        _require(
            len(refs) == 2 and all(isinstance(item, str) and item in atom_ids for item in refs)
            and refs[0] != refs[1],
            f"{row_label} endpoints are invalid",
        )
        pair = tuple(sorted(refs))
        _require(pair not in pairs, f"{label} repeats a bond")
        pairs.add(pair)
        order = _integer(bond["order"], f"{row_label}.order")
        _require(order in {1, 2, 3}, f"{row_label}.order is unsupported")
    return graph


def _validate_candidate(value: Any) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    candidate = _object(value, "candidate")
    _exact(candidate, _CANDIDATE_KEYS, "candidate")
    _require(candidate["schema_version"] == _CANDIDATE_SCHEMA_VERSION, "unsupported candidate schema")
    candidate_id = _string(candidate["candidate_id"], "candidate.candidate_id")
    _require(candidate["status"] == "unreviewed", "candidate status must be unreviewed")
    _require(candidate["extraction_status"] == "candidate", "catalog accepts only successful candidates")
    _require(candidate["diagnostics"] == [], "accepted candidate diagnostics must be empty")

    binding = _object(candidate["source_binding"], "candidate.source_binding")
    _exact(binding, _SOURCE_BINDING_KEYS, "candidate.source_binding")
    _require(binding["provider"] == "M-CSA", "candidate provider differs")
    record_id = _string(binding["record_id"], "candidate.source_binding.record_id")
    _require(_MCSA_ID.fullmatch(record_id) is not None, "candidate record ID is invalid")
    mechanism_id = _integer(binding["mechanism_id"], "candidate.source_binding.mechanism_id")
    before_step = _integer(binding["before_step_id"], "candidate.source_binding.before_step_id")
    after_step = _integer(binding["after_step_id"], "candidate.source_binding.after_step_id")
    _require(mechanism_id > 0 and before_step > 0 and after_step == before_step + 1, "candidate source steps are not adjacent")
    for key in ("snapshot_sha256", "before_scheme_sha256", "after_scheme_sha256"):
        _digest(binding[key], f"candidate.source_binding.{key}")
    expected_id = (
        f"panel-context-candidate:{record_id}:mechanism-{mechanism_id}:"
        f"steps-{before_step}-{after_step}"
    )
    _require(candidate_id == expected_id, "candidate ID differs from source binding")

    panels = _object(candidate["source_panels"], "candidate.source_panels")
    _exact(panels, {"before_graph", "after_graph", "before_nodes", "after_nodes"}, "candidate.source_panels")
    before_graph = _validate_graph(panels["before_graph"], "candidate.before_graph")
    _validate_graph(panels["after_graph"], "candidate.after_graph")
    _array(panels["before_nodes"], "candidate.before_nodes")
    _array(panels["after_nodes"], "candidate.after_nodes")
    _object(candidate["correspondence"], "candidate.correspondence")
    _array(candidate["source_flow_bindings"], "candidate.source_flow_bindings")
    _object(candidate["coverage"], "candidate.coverage")
    _object(candidate["opaque_source_context"], "candidate.opaque_source_context")
    _object(candidate["context_preservation"], "candidate.context_preservation")
    scope = _object(candidate["scope_effect"], "candidate.scope_effect")
    _require(scope == _REQUIRED_CANDIDATE_SCOPE, "candidate scope differs from the accepted unreviewed boundary")

    atoms = {atom["atom_id"]: atom for atom in before_graph["atoms"]}
    return candidate, atoms


def _event(candidate_id: str, raw: Any, atoms: dict[str, dict[str, Any]]) -> dict[str, Any]:
    edit = _object(raw, "candidate edit")
    _exact(edit, _EDIT_KEYS, "candidate edit")
    edit_id = _string(edit["edit_id"], "candidate edit.edit_id")
    operation = _string(edit["operation"], "candidate edit.operation")
    _string(edit["source_flow_id"], "candidate edit.source_flow_id")
    support = _string(edit["support"], "candidate edit.support")
    _require(support in _SUPPORTS, "candidate edit support is unsupported")
    atom_ids = _array(edit["atom_ids"], "candidate edit.atom_ids")
    before = _integer(edit["before"], "candidate edit.before")
    after = _integer(edit["after"], "candidate edit.after")
    _require(before != after, "candidate edit is a no-op")

    if operation in {"add_bond", "remove_bond", "set_bond_order"}:
        _require(
            len(atom_ids) == 2 and atom_ids[0] != atom_ids[1]
            and all(isinstance(item, str) and item in atoms for item in atom_ids),
            "candidate bond edit endpoints are invalid",
        )
        _require(before in {0, 1, 2, 3} and after in {0, 1, 2, 3}, "candidate bond edit values are unsupported")
        if operation == "add_bond":
            _require(before == 0 and after > 0, "add_bond values differ")
        elif operation == "remove_bond":
            _require(before > 0 and after == 0, "remove_bond values differ")
        else:
            _require(before > 0 and after > 0, "set_bond_order values differ")
        signature = {
            "kind": "bond",
            "elements": sorted(atoms[item]["element"] for item in atom_ids),
            "before": before,
            "after": after,
        }
    else:
        _require(operation == "set_formal_charge", "candidate edit operation is unsupported")
        _require(
            len(atom_ids) == 1 and isinstance(atom_ids[0], str) and atom_ids[0] in atoms,
            "candidate charge edit endpoint is invalid",
        )
        signature = {
            "kind": "charge",
            "elements": [atoms[atom_ids[0]]["element"]],
            "before": before,
            "after": after,
        }
    return {
        "event_id": f"{candidate_id}:{edit_id}",
        "edit_id": edit_id,
        "support": support,
        "source_edit": copy.deepcopy(edit),
        "signature": signature,
    }


def _validate_source_context(
    value: Any,
    candidate: dict[str, Any],
    bundle_ids: set[str],
) -> dict[str, Any]:
    context = _object(value, "source_context")
    _exact(context, _SOURCE_CONTEXT_KEYS, "source_context")
    bundle_id = _string(context["source_draft_bundle_id"], "source_context.source_draft_bundle_id")
    _require(bundle_id in bundle_ids, "source context names an unbound draft bundle")
    binding = candidate["source_binding"]

    record = _object(context["record_binding"], "source_context.record_binding")
    _exact(record, {"record_id", "mcsa_id"}, "source_context.record_binding")
    _string(record["record_id"], "source_context.record_binding.record_id")
    mcsa_id = _string(record["mcsa_id"], "source_context.record_binding.mcsa_id")
    _require(mcsa_id == binding["record_id"], "source context record differs from candidate")

    proposal = _object(context["proposal_binding"], "source_context.proposal_binding")
    _exact(proposal, {"proposal_id", "source_mechanism_id"}, "source_context.proposal_binding")
    _string(proposal["proposal_id"], "source_context.proposal_binding.proposal_id")
    _require(
        _integer(proposal["source_mechanism_id"], "source_context.proposal_binding.source_mechanism_id")
        == binding["mechanism_id"],
        "source context proposal differs from candidate",
    )
    _string(context["source_scope"], "source_context.source_scope")

    steps = _array(context["step_bindings"], "source_context.step_bindings")
    _require(len(steps) == 2, "source context must bind before and after panels")
    for index, (raw, role, step_id, sha_key) in enumerate(zip(
        steps,
        ("before", "after"),
        (binding["before_step_id"], binding["after_step_id"]),
        ("before_scheme_sha256", "after_scheme_sha256"),
    )):
        row = _object(raw, f"source_context.step_bindings[{index}]")
        _exact(row, _STEP_KEYS, f"source_context.step_bindings[{index}]")
        _require(row["role"] == role, "source context step roles or order differ")
        _require(
            _integer(row["source_step_id"], f"source_context.step_bindings[{index}].source_step_id") == step_id,
            "source context step ID differs from candidate",
        )
        _require(row["scheme_sha256"] == binding[sha_key], "source context scheme hash differs from candidate")
        _digest(row["scheme_sha256"], f"source_context.step_bindings[{index}].scheme_sha256")
        _string(row["summary"], f"source_context.step_bindings[{index}].summary")
        kind = _string(
            row["source_kind"],
            f"source_context.step_bindings[{index}].source_kind",
        )
        _require(kind in {"source_draft_step", "mcsa_terminal_state"}, "source context step kind is unsupported")
        if kind == "source_draft_step":
            _string(row["step_id"], f"source_context.step_bindings[{index}].step_id")
            _require(row["is_inferred"] is None or type(row["is_inferred"]) is bool, "source draft inferred status must be boolean or null")
        else:
            _require(row["step_id"] is None and row["is_inferred"] is None, "terminal state cannot masquerade as a draft step")

    abstentions = _array(context["mandatory_abstentions"], "source_context.mandatory_abstentions")
    seen: set[str] = set()
    for index, raw in enumerate(abstentions):
        row = _object(raw, f"source_context.mandatory_abstentions[{index}]")
        _exact(row, {"clause_id", "reason"}, f"source_context.mandatory_abstentions[{index}]")
        clause_id = _string(row["clause_id"], f"source_context.mandatory_abstentions[{index}].clause_id")
        _string(row["reason"], f"source_context.mandatory_abstentions[{index}].reason")
        _require(clause_id not in seen, "source context repeats an abstention")
        seen.add(clause_id)
    return context


def _validate_scan(value: Any) -> dict[str, Any]:
    scan = _object(value, "provenance.context_scan")
    _exact(scan, _SCAN_KEYS, "provenance.context_scan")
    _require(scan["schema_version"] == "catalytic-earth.context-candidate-scan.v1", "unsupported context scan provenance")
    _safe_path(scan["path"], "provenance.context_scan.path")
    for key in ("sha256", "source_registry_sha256", "baseline_scan_sha256"):
        _digest(scan[key], f"provenance.context_scan.{key}")
    implementation = _object(scan["implementation_sha256"], "provenance.context_scan.implementation_sha256")
    _require(bool(implementation), "context scan implementation provenance is empty")
    for path, digest in implementation.items():
        _safe_path(path, "context scan implementation path")
        _digest(digest, f"context scan implementation hash for {path}")
    return scan


def _validate_bundles(value: Any) -> tuple[list[dict[str, Any]], set[str]]:
    bundles = _array(value, "provenance.source_draft_bundles")
    _require(bool(bundles), "source draft bundle provenance is empty")
    ids: set[str] = set()
    paths: set[str] = set()
    for index, raw in enumerate(bundles):
        row = _object(raw, f"provenance.source_draft_bundles[{index}]")
        _exact(row, _BUNDLE_KEYS, f"provenance.source_draft_bundles[{index}]")
        bundle_id = _string(row["bundle_id"], f"provenance.source_draft_bundles[{index}].bundle_id")
        path = _safe_path(row["path"], f"provenance.source_draft_bundles[{index}].path")
        _digest(row["sha256"], f"provenance.source_draft_bundles[{index}].sha256")
        _require(bundle_id not in ids and path not in paths, "source draft bundles repeat")
        ids.add(bundle_id)
        paths.add(path)
    return bundles, ids


def _validate_implementation(value: Any) -> dict[str, str]:
    implementation = _object(value, "provenance.catalog_implementation_sha256")
    _require(
        set(implementation) == _CATALOG_IMPLEMENTATION_PATHS,
        "catalog implementation provenance is incomplete",
    )
    for path, digest in implementation.items():
        _safe_path(path, "catalog implementation path")
        _digest(digest, f"catalog implementation hash for {path}")
    return implementation


def _build(
    candidates: list[dict[str, Any]],
    provenance: dict[str, Any],
) -> dict[str, Any]:
    _exact(provenance, _PROVENANCE_INPUT_KEYS, "provenance")
    scan = _validate_scan(provenance["context_scan"])
    bundles, bundle_ids = _validate_bundles(provenance["source_draft_bundles"])
    implementation = _validate_implementation(
        provenance["catalog_implementation_sha256"]
    )
    contexts = _array(provenance["candidate_contexts"], "provenance.candidate_contexts")
    _require(len(contexts) == len(candidates), "candidate context count differs")

    rows: list[dict[str, Any]] = []
    context_bindings: list[dict[str, Any]] = []
    seen_candidates: set[str] = set()
    seen_events: set[str] = set()
    used_bundle_ids: set[str] = set()
    for index, (raw_candidate, raw_context) in enumerate(zip(candidates, contexts)):
        candidate, atoms = _validate_candidate(raw_candidate)
        candidate_id = candidate["candidate_id"]
        _require(candidate_id not in seen_candidates, "catalog repeats a candidate")
        seen_candidates.add(candidate_id)
        context_row = _object(raw_context, f"provenance.candidate_contexts[{index}]")
        _exact(context_row, _CONTEXT_INPUT_KEYS, f"provenance.candidate_contexts[{index}]")
        _require(context_row["candidate_id"] == candidate_id, "candidate context order or ID differs")
        candidate_sha = hashlib.sha256(canonical_bytes(candidate)).hexdigest()
        _digest(context_row["candidate_sha256"], f"provenance.candidate_contexts[{index}].candidate_sha256")
        _require(context_row["candidate_sha256"] == candidate_sha, "candidate differs from frozen scan hash")
        source_context = _validate_source_context(context_row["source_context"], candidate, bundle_ids)
        used_bundle_ids.add(source_context["source_draft_bundle_id"])
        source_context_sha = hashlib.sha256(canonical_bytes(source_context)).hexdigest()
        _digest(context_row["source_context_sha256"], f"provenance.candidate_contexts[{index}].source_context_sha256")
        _require(context_row["source_context_sha256"] == source_context_sha, "source context hash differs")

        edits = _array(candidate["proposed_graph_edits"], "candidate.proposed_graph_edits")
        _require(bool(edits), "accepted candidate has no proposed edits")
        events: list[dict[str, Any]] = []
        edit_ids: set[str] = set()
        for edit in edits:
            event = _event(candidate_id, edit, atoms)
            _require(event["edit_id"] not in edit_ids, "candidate edit IDs repeat")
            _require(event["event_id"] not in seen_events, "catalog event IDs repeat")
            edit_ids.add(event["edit_id"])
            seen_events.add(event["event_id"])
            events.append(event)
        counts = _support_counts(events)
        rows.append({
            "candidate_id": candidate_id,
            "candidate_sha256": candidate_sha,
            "source_context_sha256": source_context_sha,
            "source_context": copy.deepcopy(source_context),
            "event_count": len(events),
            "support_counts": counts,
            "events": events,
            "candidate": copy.deepcopy(candidate),
        })
        context_bindings.append({
            "candidate_id": candidate_id,
            "candidate_sha256": candidate_sha,
            "source_context_sha256": source_context_sha,
        })

    _require(used_bundle_ids == bundle_ids, "source draft bundle provenance is unused or incomplete")

    all_events = [event for row in rows for event in row["events"]]
    return {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "catalog_id": CATALOG_ID,
        "status": "unreviewed",
        "provenance": {
            "context_scan": copy.deepcopy(scan),
            "source_draft_bundles": copy.deepcopy(bundles),
            "candidate_context_bindings": context_bindings,
            "catalog_implementation_sha256": copy.deepcopy(implementation),
        },
        "candidate_count": len(rows),
        "event_count": len(all_events),
        "support_counts": _support_counts(all_events),
        "scope": copy.deepcopy(_CATALOG_SCOPE),
        "candidates": rows,
    }


def build_candidate_event_catalog(
    candidates: list[dict[str, Any]],
    *,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    """Build a deterministic literal event index from accepted candidates."""

    candidate_rows = _array(candidates, "candidates")
    _require(bool(candidate_rows), "candidates is empty")
    return _build(copy.deepcopy(candidate_rows), copy.deepcopy(_object(provenance, "provenance")))


def validate_candidate_event_catalog(value: Any) -> dict[str, Any]:
    """Validate and rederive every event row and catalog count."""

    catalog = _object(value, "candidate event catalog")
    _exact(catalog, _CATALOG_KEYS, "candidate event catalog")
    _require(catalog["schema_version"] == CATALOG_SCHEMA_VERSION, "unsupported candidate event catalog")
    _require(catalog["catalog_id"] == CATALOG_ID, "candidate event catalog ID differs")
    _require(catalog["status"] == "unreviewed", "candidate event catalog status differs")
    _require(catalog["scope"] == _CATALOG_SCOPE, "candidate event catalog scope differs")
    rows = _array(catalog["candidates"], "candidate event catalog.candidates")
    provenance = _object(catalog["provenance"], "candidate event catalog.provenance")
    _exact(provenance, _PROVENANCE_KEYS, "candidate event catalog.provenance")
    bindings = _array(provenance["candidate_context_bindings"], "candidate context bindings")
    _require(len(bindings) == len(rows), "candidate context binding count differs")
    contexts = []
    candidates = []
    for index, (raw_row, raw_binding) in enumerate(zip(rows, bindings)):
        row = _object(raw_row, f"candidate event catalog.candidates[{index}]")
        _exact(row, _ROW_KEYS, f"candidate event catalog.candidates[{index}]")
        binding = _object(raw_binding, f"candidate context bindings[{index}]")
        _exact(binding, _CONTEXT_BINDING_KEYS, f"candidate context bindings[{index}]")
        contexts.append({**copy.deepcopy(binding), "source_context": copy.deepcopy(row["source_context"])})
        candidates.append(copy.deepcopy(row["candidate"]))
    rebuilt = _build(candidates, {
        "context_scan": copy.deepcopy(provenance["context_scan"]),
        "source_draft_bundles": copy.deepcopy(provenance["source_draft_bundles"]),
        "catalog_implementation_sha256": copy.deepcopy(
            provenance["catalog_implementation_sha256"]
        ),
        "candidate_contexts": contexts,
    })
    _require(canonical_bytes(catalog) == canonical_bytes(rebuilt), "candidate event catalog derivation differs")
    records = {row["candidate"]["source_binding"]["record_id"] for row in rows}
    return {
        "catalog_id": catalog["catalog_id"],
        "catalog_sha256": hashlib.sha256(canonical_bytes(catalog)).hexdigest(),
        "candidate_count": catalog["candidate_count"],
        "event_count": catalog["event_count"],
        "support_counts": copy.deepcopy(catalog["support_counts"]),
        "record_count": len(records),
    }


def _normalize_clause(raw: Any, index: int) -> dict[str, Any]:
    label = f"clauses[{index}]"
    clause = _object(raw, label)
    _exact(clause, {"kind", "elements", "before", "after"}, label)
    kind = _string(clause["kind"], f"{label}.kind")
    _require(kind in {"bond", "charge"}, f"{label}.kind is unsupported")
    elements = _array(clause["elements"], f"{label}.elements")
    expected_length = 2 if kind == "bond" else 1
    _require(len(elements) == expected_length, f"{label}.elements has the wrong length")
    normalized_elements = []
    for item in elements:
        token = _string(item, f"{label}.elements")
        _require(token == token.strip() and token in _ELEMENTS, f"{label} uses an invalid exact element token")
        normalized_elements.append(token)
    if kind == "bond":
        normalized_elements.sort()
    before = _integer(clause["before"], f"{label}.before")
    after = _integer(clause["after"], f"{label}.after")
    _require(before != after, f"{label} is a no-op")
    if kind == "bond":
        _require(before in {0, 1, 2, 3} and after in {0, 1, 2, 3}, f"{label} bond values are unsupported")
    return {"kind": kind, "elements": normalized_elements, "before": before, "after": after}


def _normalize_clauses(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    rows = _array(value, "clauses")
    unique: dict[bytes, dict[str, Any]] = {}
    for index, raw in enumerate(rows):
        clause = _normalize_clause(raw, index)
        unique[canonical_bytes(clause)] = clause
    return [unique[key] for key in sorted(unique)]


def query_candidate_events(
    value: Any,
    *,
    clauses: list[dict[str, Any]] | None = None,
    mcsa_id: str | None = None,
    support: str = "after_graph_confirmed",
) -> dict[str, Any]:
    """Match literal event clauses with AND scope inside one candidate."""

    summary = validate_candidate_event_catalog(value)
    catalog = _object(value, "candidate event catalog")
    normalized_clauses = _normalize_clauses(clauses)
    _require(isinstance(support, str) and support in _SUPPORT_FILTERS, "support filter is unsupported")
    if mcsa_id is not None:
        _require(isinstance(mcsa_id, str), "mcsa_id must be a string or null")
        mcsa_id = mcsa_id.strip().upper()
        _require(_MCSA_ID.fullmatch(mcsa_id) is not None, "mcsa_id must be an exact M-CSA identifier")

    matches = []
    for row in catalog["candidates"]:
        if mcsa_id is not None and row["candidate"]["source_binding"]["record_id"] != mcsa_id:
            continue
        eligible = [
            event for event in row["events"]
            if support == "any" or event["support"] == support
        ]
        if not eligible:
            continue
        witnesses = []
        matched = True
        for clause in normalized_clauses:
            events = [event for event in eligible if event["signature"] == clause]
            if not events:
                matched = False
                break
            witnesses.append({
                "clause": copy.deepcopy(clause),
                "events": copy.deepcopy(events),
            })
        if matched:
            matches.append({
                "candidate_row": copy.deepcopy(row),
                "eligible_support_events": copy.deepcopy(eligible),
                "clause_witnesses": witnesses,
            })

    return {
        "schema_version": QUERY_SCHEMA_VERSION,
        "catalog_id": summary["catalog_id"],
        "catalog_sha256": summary["catalog_sha256"],
        "status": "unreviewed",
        "provenance": copy.deepcopy(catalog["provenance"]),
        "filters": {
            "mcsa_id": mcsa_id,
            "support": support,
            "clauses": normalized_clauses,
        },
        "query_semantics": {
            "clause_combination": "all_clauses_within_one_candidate",
            "clauses_require_one_shared_event": False,
            "clauses_imply_shared_atoms": False,
            "repeated_identical_clauses": "set_semantics",
            "signature_identity": "literal_element_and_before_after_tuple_only",
            "shared_signature_implies_mechanism_equivalence": False,
            "empty_result": "no_matching_candidate_event_not_absence_of_chemistry",
        },
        "candidate_count": len(matches),
        "selected_support_event_count": sum(len(match["eligible_support_events"]) for match in matches),
        "matched_witness_count": sum(
            len(witness["events"])
            for match in matches for witness in match["clause_witnesses"]
        ),
        "matches": matches,
    }


__all__ = [
    "CATALOG_SCHEMA_VERSION",
    "QUERY_SCHEMA_VERSION",
    "build_candidate_event_catalog",
    "canonical_bytes",
    "query_candidate_events",
    "validate_candidate_event_catalog",
]
