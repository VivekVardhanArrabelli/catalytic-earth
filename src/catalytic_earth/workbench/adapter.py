"""Narrow adapter between the packaged Atlas queries and the Workbench UI.

This module adds no scientific content. It calls the same verified loaders and
the same query functions that ``catalytic-earth``'s own subcommands call, in
process, and reshapes their output for rendering. No scientific value is
copied by hand into source code here or in the frontend: every number, label,
identifier and caveat the UI shows is read out of a live query result at
request time.

The scientific core is treated as read-only. Nothing in this package mutates
packaged data, review hashes or expected-value files.
"""

from __future__ import annotations

import json
from typing import Any

from ..core_cli import (
    ATLAS10_EXPECTED,
    ATLAS10_KERNEL,
    _canonical_sha,
    _resource_bytes,
    verified_candidate_events,
    verified_mechanism_evidence,
    verified_transformations,
)
from .layout import compute_layout

__all__ = [
    "AdapterError",
    "MECHANISMS",
    "evidence_view",
    "mechanism_list",
    "pattern_query",
    "sites_view",
    "transformation_view",
]


class AdapterError(ValueError):
    """Raised when a request cannot be served from packaged data."""


#: Mechanisms exposed by the Workbench. Both are driven by the same code path;
#: neither has a hard-coded scientific page.
MECHANISMS: dict[str, dict[str, str]] = {
    "M0187": {
        "mcsa_id": "M0187",
        "short_name": "Mandelate racemase",
        "summary": "Depicted substrate to depicted intermediate (mechanism 1, step 1 to step 2).",
    },
    "M0173": {
        "mcsa_id": "M0173",
        "short_name": "Trypsin",
        "summary": "Depicted enzyme-substrate covalent addition (mechanism 1, step 1 to step 2).",
    },
}


def _atlas10_bundle() -> dict[str, Any]:
    """Load the Atlas-10 kernel with the same check the CLI applies."""
    bundle = json.loads(_resource_bytes(ATLAS10_KERNEL))
    expected = json.loads(_resource_bytes(ATLAS10_EXPECTED))
    if _canonical_sha(bundle) != expected.get("kernel_sha256"):
        raise AdapterError("Atlas-10 context differs from the packaged expectation")
    return bundle


def mechanism_list() -> dict[str, Any]:
    """Return the selectable mechanisms."""
    return {"mechanisms": [dict(entry) for entry in MECHANISMS.values()]}


def _edit_label(edit: dict[str, Any]) -> str:
    """Describe one graph edit without inventing chemistry."""
    operation = edit.get("operation")
    atoms = " - ".join(str(value) for value in edit.get("atom_ids", []))
    before, after = edit.get("before"), edit.get("after")
    if operation == "remove_bond":
        return f"break bond {atoms}"
    if operation == "add_bond":
        return f"form bond {atoms}"
    if operation == "set_bond_order":
        return f"bond {atoms}: order {before} to {after}"
    if operation == "set_formal_charge":
        return f"atom {atoms}: formal charge {before} to {after}"
    if operation == "set_stereochemistry":
        return f"atom {atoms}: stereochemistry {before!r} to {after!r}"
    return f"{operation} {atoms}"


def transformation_view(mcsa_id: str) -> dict[str, Any]:
    """Build the replay view model for one reviewed transformation.

    The graphs, edits, flow bindings, abstentions, scope and review status are
    taken verbatim from ``query_transformations``. Only the atom positions are
    added, and they are explicitly marked as a computed layout.
    """
    from ..atlas_transformation_query import (
        TRANSFORMATION_SETS,
        normalize_mcsa_id,
        query_transformations,
    )

    key = normalize_mcsa_id(mcsa_id)
    if key not in MECHANISMS or key not in TRANSFORMATION_SETS:
        raise AdapterError(f"no packaged transformation set for {mcsa_id!r}")

    result = query_transformations(
        verified_transformations(key), atlas10_bundle=_atlas10_bundle(), mcsa_id=key
    )
    if not result.get("transformations"):
        raise AdapterError(f"no reviewed transition returned for {key}")

    transformation = result["transformations"][0]
    panel = transformation["panel_correspondence"]
    before_graph, after_graph = panel["before_graph"], panel["after_graph"]

    layout = compute_layout(
        before_graph["atoms"], [before_graph["bonds"], after_graph["bonds"]]
    )

    edits = [dict(edit, label=_edit_label(edit)) for edit in panel["graph_edits"]]
    flows = panel.get("source_flow_bindings", [])

    return {
        "abstentions": transformation.get("mandatory_abstentions", []),
        "after_graph": after_graph,
        "before_graph": before_graph,
        "edits": edits,
        "layout": layout,
        "mechanism": dict(MECHANISMS[key]),
        "query_semantics": result.get("query_semantics", {}),
        "record_binding": transformation.get("record_binding", {}),
        "replay": panel.get("replay", {}),
        "replay_semantics": {
            "kind": "symbolic_replay_of_published_source_proposal",
            "not": [
                "molecular_dynamics_trajectory",
                "observed_turnover",
                "physical_atom_identity",
                "time_resolved_measurement",
            ],
            "note": (
                "Stepping the edits replays a published source-depiction "
                "proposal as a symbolic graph edit sequence. It is not a "
                "molecular trajectory and shows no physical motion."
            ),
        },
        "representation_boundaries": panel.get("representation_boundaries", []),
        "review": result.get("review", {}),
        "schema_version": result.get("schema_version"),
        "scope_effect": transformation.get("scope_effect", {}),
        "source_bindings": result.get("source_bindings", []),
        "source_flow_bindings": flows,
        "state_pair": transformation.get("state_pair", {}),
        "status": panel.get("status"),
        "transformation_id": transformation.get("transformation_id"),
        "transformation_set_id": result.get("transformation_set_id"),
    }


def sites_view(mcsa_id: str) -> dict[str, Any]:
    """Return the changed source atoms of one mechanism and their site links.

    This is the ``atlas-transformation-sites`` query. A changed depiction node
    is linked to a catalytic site only where the reviewed source annotation
    labels that atom explicitly; every other changed node is returned as
    unresolved rather than guessed.
    """
    from ..atlas_transformation_query import TRANSFORMATION_SETS, normalize_mcsa_id
    from ..atlas_transformation_sites import query_transformation_sites

    key = normalize_mcsa_id(mcsa_id)
    if key not in MECHANISMS:
        raise AdapterError(f"no packaged transformation set for {mcsa_id!r}")

    result = query_transformation_sites(
        {name: verified_transformations(name) for name in TRANSFORMATION_SETS},
        atlas10_bundle=_atlas10_bundle(),
        mcsa_id=key,
    )

    atoms: list[dict[str, Any]] = []
    coverage: dict[str, Any] = {}
    for match in result.get("matches", []):
        coverage = match.get("coverage", {}) or coverage
        for atom in match.get("changed_source_atoms", []):
            mapping = atom.get("source_record_residue_mapping", {}) or {}
            structure = atom.get("protein_structure_context", {}) or {}
            atoms.append(
                {
                    "deposited_atom_identity": atom.get("deposited_atom_identity", {}),
                    "edit_ids": atom.get("edit_ids", []),
                    "element": atom.get("element"),
                    "formal_charge": atom.get("formal_charge"),
                    "protein_structure_context": structure,
                    "residue_label": atom.get("source_residue_label", {}) or {},
                    "site_id": mapping.get("site_id"),
                    "site_mapping": mapping,
                    "source_atom_id": atom.get("source_atom_id"),
                    "source_flow_ids": atom.get("source_flow_ids", []),
                    "status": (structure.get("status") or "not_resolved"),
                }
            )

    return {
        "atoms": atoms,
        "changed_source_atom_count": result.get("changed_source_atom_count"),
        "coverage": coverage,
        "mcsa_id": key,
        "query_semantics": result.get("query_semantics", {}),
        "resolved_source_atom_count": result.get("resolved_source_atom_count"),
        "schema_version": result.get("schema_version"),
        "unresolved_source_atom_count": result.get("unresolved_source_atom_count"),
    }


def _fragment_relation_view(relation: dict[str, Any]) -> dict[str, Any]:
    """Reshape one source-fragment relation, keeping its resolution status."""
    fragment = relation.get("fragment", {})
    annotations = {
        str(entry["atom_id"]): entry for entry in fragment.get("annotations", [])
    }
    retained: dict[str, list[float]] = {}
    for atom_id, entry in annotations.items():
        x2, y2 = entry.get("x2"), entry.get("y2")
        if x2 is not None and y2 is not None:
            retained[atom_id] = [float(x2), float(y2)]

    mapping = relation.get("source_record_residue_mapping", {}) or {}
    structure = relation.get("protein_structure_context", {}) or {}
    functional = relation.get("functional_evidence", {}) or {}

    return {
        "aliases": [
            {"atom_id": entry["atom_id"], "mrv_alias": entry.get("mrv_alias")}
            for entry in fragment.get("alias_anchors", [])
        ],
        "atoms": fragment.get("atoms", []),
        "bonds": fragment.get("bonds", []),
        "boundary_bonds": fragment.get("boundary_bonds", []),
        "deposited_atom_identity": relation.get("deposited_atom_identity", {}),
        "fragment_basis": fragment.get("basis"),
        "functional_evidence": {
            "case_ids": functional.get("case_ids", []),
            "matched_observations": functional.get("matched_observations", []),
            "relationship": functional.get("relationship"),
            "source_arrow_experimentally_validated": functional.get(
                "source_arrow_experimentally_validated"
            ),
        },
        "protein_structure_context": structure,
        "relation_id": relation.get("relation_id"),
        "residue_label": relation.get("source_residue_label", {}),
        "retained_depiction_coordinates": {
            "coordinates": retained,
            "semantics": {
                "kind": "retained_source_panel_depiction_coordinates",
                "note": (
                    "These x2/y2 values are the retained source drawing "
                    "coordinates for this fragment. They are depiction "
                    "coordinates, not measured molecular geometry."
                ),
                "units": "source_depiction_units",
            },
        },
        "site_id": mapping.get("site_id"),
        "site_mapping": mapping,
        "source_atom_id": relation.get("source_atom_id"),
        "source_flow_witnesses": relation.get("source_flow_witnesses", []),
        "source_step_id": relation.get("source_step_id"),
        "transformation_context": relation.get("transformation_context", {}),
    }


def evidence_view(
    variant: str | None = None, endpoint: str | None = None
) -> dict[str, Any]:
    """Run the mechanism-evidence query with its source-fragment relations."""
    from ..atlas_fragment_sites import query_fragment_sites
    from ..atlas_mechanism_evidence import query_mechanism_evidence

    bundle = _atlas10_bundle()
    transformation_values = {"M0187": verified_transformations("M0187")}
    result = query_mechanism_evidence(
        verified_mechanism_evidence(),
        atlas10_bundle=bundle,
        transformation_values=transformation_values,
        variant=variant or None,
        endpoint=endpoint or None,
    )
    fragments = query_fragment_sites(
        json.loads(_resource_bytes("mechanism_evidence_data/source_fragments.json")),
        atlas10_bundle=bundle,
        evidence_query=result,
        transformation_values=transformation_values,
    )

    observations: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    for match in result.get("matches", []):
        case = match.get("case", {})
        cases.append(
            {
                "adjudication": case.get("adjudication", {}),
                "alternatives": case.get("alternatives", []),
                "applicability": case.get("applicability", {}),
                "case_id": case.get("case_id"),
                "discriminants": case.get("discriminants", []),
                "mandatory_abstentions": case.get("mandatory_abstentions", []),
                "question": case.get("question"),
                "scope_effect": case.get("scope_effect", {}),
                "site_context_binding": case.get("site_context_binding", {}),
                "transformation_binding": case.get("transformation_binding", {}),
            }
        )
        for observation in match.get("matched_observations", []):
            observations.append(dict(observation, case_id=case.get("case_id")))

    return {
        "cases": cases,
        "endpoint_kinds": sorted(
            {
                str((entry.get("endpoint") or {}).get("kind"))
                for entry in observations
                if (entry.get("endpoint") or {}).get("kind")
            }
        ),
        "evidence_set_id": result.get("evidence_set_id"),
        "filters": result.get("filters", {}),
        "matched_observation_count": result.get("matched_observation_count"),
        "observations": observations,
        "query_semantics": result.get("query_semantics", {}),
        "relations": [
            _fragment_relation_view(relation)
            for relation in fragments.get("relations", [])
        ],
        "relation_counts": {
            "reference_annotation": fragments.get("reference_annotation_count"),
            "resolved": fragments.get("resolved_relation_count"),
            "total": fragments.get("relation_count"),
        },
        "review": result.get("review", {}),
        "schema_version": result.get("schema_version"),
        "source_bindings": result.get("source_bindings", []),
        "fragment_query_semantics": fragments.get("query_semantics", {}),
        "fragment_review": fragments.get("review", {}),
    }


_MAX_CLAUSES = 8


def pattern_query(
    clauses: list[dict[str, Any]],
    mcsa_id: str | None = None,
    support: str = "after_graph_confirmed",
) -> dict[str, Any]:
    """Run a validated shared-atom pattern query against the candidate catalog.

    Clause values are validated here before reaching the matcher, which applies
    its own grammar and search-budget rules.
    """
    from ..atlas_candidate_patterns import query_candidate_patterns

    if not isinstance(clauses, list) or not clauses:
        raise AdapterError("at least one clause is required")
    if len(clauses) > _MAX_CLAUSES:
        raise AdapterError(f"at most {_MAX_CLAUSES} clauses are allowed")

    normalised: list[dict[str, Any]] = []
    for clause in clauses:
        if not isinstance(clause, dict):
            raise AdapterError("each clause must be an object")
        kind = clause.get("kind")
        if kind not in {"bond", "charge"}:
            raise AdapterError("clause kind must be 'bond' or 'charge'")
        elements = clause.get("elements")
        variables = clause.get("variables")
        width = 2 if kind == "bond" else 1
        if not isinstance(elements, list) or len(elements) != width:
            raise AdapterError(f"{kind} clause needs {width} element(s)")
        if not isinstance(variables, list) or len(variables) != width:
            raise AdapterError(f"{kind} clause needs {width} variable(s)")
        try:
            before = int(clause["before"])
            after = int(clause["after"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AdapterError("clause before/after must be integers") from exc
        normalised.append(
            {
                "after": after,
                "before": before,
                "elements": [str(value) for value in elements],
                "kind": kind,
                "variables": [str(value) for value in variables],
            }
        )

    if support not in {"after_graph_confirmed", "source_arrow_only", "any"}:
        raise AdapterError(f"unsupported support filter {support!r}")

    try:
        result = query_candidate_patterns(
            verified_candidate_events(),
            clauses=normalised,
            mcsa_id=(mcsa_id or None),
            support=support,
        )
    except ValueError as exc:
        raise AdapterError(str(exc)) from exc

    return {
        "binding_count": result.get("binding_count"),
        "candidate_count": result.get("candidate_count"),
        "catalog_id": result.get("catalog_id"),
        "catalog_sha256": result.get("catalog_sha256"),
        "filters": result.get("filters", {}),
        "matches": result.get("matches", []),
        "query_semantics": result.get("query_semantics", {}),
        "schema_version": result.get("schema_version"),
        "status": result.get("status"),
    }
