"""Derive source-residue site context for reviewed transformation edits.

This query joins only facts already present in computationally checked Atlas-10
records and reviewed transformation sets.  A source drawing node is never
treated as a deposited atom or as a physical atom identity across panels.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

from .atlas_transformation_query import query_transformation_sets


SCHEMA_VERSION = "catalytic-earth.transformation-site-query.v1"

_RESIDUE_LABEL_RE = re.compile(
    r"res:(?P<residue>[A-Z][a-z]{2})(?P<position>[1-9][0-9]*)(?P<chain>[A-Za-z][A-Za-z0-9_.-]*)"
)
_UNIPROT_SITE_RE = re.compile(
    r"(?P<uniprot>[A-Z0-9]+):(?P<residue>[A-Z])(?P<position>[1-9][0-9]*)"
)
_THREE_TO_ONE = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C",
    "Gln": "Q", "Glu": "E", "Gly": "G", "His": "H", "Ile": "I",
    "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F", "Pro": "P",
    "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _string_filter(value: Any, label: str) -> str | None:
    if value is None:
        return None
    _require(isinstance(value, str) and value and value == value.strip(),
             f"{label} must be exact nonempty text")
    return value


def _records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    _require(isinstance(bundle, dict), "atlas10_bundle must be an object")
    rows: list[dict[str, Any]] = []
    for key in ("records", "follow_on_records"):
        value = bundle.get(key)
        if isinstance(value, list):
            rows.extend(item for item in value if isinstance(item, dict))
    inherited = bundle.get("inherited_kernel")
    if isinstance(inherited, dict):
        rows.extend(_records(inherited))
    return rows


def _canonical_sha256(value: Any) -> str:
    try:
        raw = json.dumps(
            value, ensure_ascii=True, allow_nan=False,
            separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("atlas10_bundle must be canonical JSON data") from exc
    return hashlib.sha256(raw).hexdigest()


def _mcsa_evidence(record: dict[str, Any], mcsa_id: str) -> dict[str, Any]:
    rows = [
        row for row in record.get("evidence", [])
        if isinstance(row, dict)
        and row.get("source_id") == "M-CSA"
        and row.get("source_record_id") == mcsa_id
        and row.get("evidence_id") == f"source:M-CSA:{mcsa_id}"
        and row.get("evidence_role") == "source_mechanism"
        and row.get("applicability") == "direct"
        and row.get("retrieval_status") == "bundled_snapshot"
    ]
    _require(len(rows) == 1, "Atlas10 record lacks one exact M-CSA evidence row")
    return rows[0]


def _tier2_record(
    bundle: dict[str, Any], transformation: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    record_binding = transformation["record_binding"]
    proposal_binding = transformation["proposal_binding"]
    before = transformation["state_pair"]["before"]
    records = _records(bundle)
    bound_records = [
        row for row in records if row.get("record_id") == record_binding["record_id"]
    ]
    _require(len(bound_records) == 1, "transformation-bound Atlas10 record is not unique")
    bound_record = bound_records[0]
    bound_proposals = [
        row for row in bound_record.get("mechanism_proposals", [])
        if isinstance(row, dict)
        and row.get("proposal_id") == proposal_binding["proposal_id"]
        and row.get("source_mechanism_id") == proposal_binding["source_mechanism_id"]
        and row.get("source_record_id") == record_binding["mcsa_id"]
    ]
    _require(len(bound_proposals) == 1, "transformation-bound proposal is not unique")
    bound_steps = [
        row for row in bound_proposals[0].get("mechanism_steps", [])
        if isinstance(row, dict)
        and row.get("source_step_id") == before["source_step_id"]
        and row.get("step_id") == before["step_id"]
        and row.get("source_scheme_sha256") == before["scheme_sha256"]
    ]
    _require(len(bound_steps) == 1, "transformation-bound before step is not unique")
    bound_mcsa = _mcsa_evidence(bound_record, record_binding["mcsa_id"])
    _require(
        bound_mcsa.get("snapshot_sha256") == record_binding["source_snapshot_sha256"],
        "transformation-bound Atlas10 M-CSA evidence hash differs",
    )

    matches: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for record in records:
        if not (
            record.get("case_id") == record_binding["case_id"]
            and record.get("object_type") == "mechanism_hypothesis"
            and type(record.get("evidence_tier")) is int
            and record.get("evidence_tier") == 2
            and record.get("fixture_only") is False
        ):
            continue
        proposals = [
            row for row in record.get("mechanism_proposals", [])
            if isinstance(row, dict)
            and row.get("proposal_id") == proposal_binding["proposal_id"]
            and row.get("source_mechanism_id") == proposal_binding["source_mechanism_id"]
            and row.get("source_record_id") == record_binding["mcsa_id"]
        ]
        if len(proposals) != 1:
            continue
        steps = [
            row for row in proposals[0].get("mechanism_steps", [])
            if isinstance(row, dict)
            and row.get("source_step_id") == before["source_step_id"]
            and row.get("step_id") == before["step_id"]
            and row.get("source_scheme_sha256") == before["scheme_sha256"]
        ]
        if len(steps) == 1:
            matches.append((record, proposals[0], steps[0]))
    _require(
        len(matches) == 1,
        "transformation does not select one exact Tier-2 Atlas10 proposal and before step",
    )
    record, proposal, step = matches[0]
    tier2_mcsa = _mcsa_evidence(record, record_binding["mcsa_id"])
    _require(
        tier2_mcsa == bound_mcsa
        and tier2_mcsa.get("snapshot_sha256") == record_binding["source_snapshot_sha256"],
        "Tier-2 and transformation-bound M-CSA evidence differs",
    )
    _require(step == bound_steps[0], "Tier-2 before-step witness differs from the bound record")
    proposal_without_scope = {
        key: value for key, value in proposal.items() if key != "proposal_scope"
    }
    bound_without_scope = {
        key: value for key, value in bound_proposals[0].items() if key != "proposal_scope"
    }
    _require(
        proposal_without_scope == bound_without_scope,
        "Tier-2 proposal witness differs from the transformation-bound record",
    )
    for field in ("sites", "structures", "evidence", "biological_scope", "provenance"):
        _require(
            record.get(field) == bound_record.get(field),
            f"Tier-2 {field} differs from the transformation-bound record",
        )
    return record, proposal, step


def _changed_atoms(transformation: dict[str, Any]) -> list[dict[str, Any]]:
    panel = transformation["panel_correspondence"]
    graph_atoms = panel["before_graph"]["atoms"]
    _require(isinstance(graph_atoms, list), "before graph atoms must be an array")
    atom_by_id: dict[str, dict[str, Any]] = {}
    for atom in graph_atoms:
        _require(isinstance(atom, dict) and isinstance(atom.get("atom_id"), str),
                 "before graph atom is invalid")
        _require(atom["atom_id"] not in atom_by_id, "before graph atom IDs repeat")
        atom_by_id[atom["atom_id"]] = atom
    edits = panel["graph_edits"]
    _require(isinstance(edits, list), "graph edits must be an array")
    by_atom: dict[str, list[dict[str, Any]]] = {}
    for edit in edits:
        _require(isinstance(edit, dict), "graph edit must be an object")
        for atom_id in edit.get("atom_ids", []):
            _require(atom_id in atom_by_id, "graph edit references an unknown before atom")
            by_atom.setdefault(atom_id, []).append(edit)
    return [
        {"atom": atom, "edits": by_atom[atom["atom_id"]]}
        for atom in graph_atoms if atom["atom_id"] in by_atom
    ]


def _source_annotation_by_atom(transformation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    context = transformation.get("source_context")
    if not isinstance(context, dict):
        return {}
    annotations = context.get("source_atom_annotations")
    rows = annotations.get("rows") if isinstance(annotations, dict) else None
    if not isinstance(rows, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        _require(isinstance(row, dict) and isinstance(row.get("atom_id"), str),
                 "source atom annotation is invalid")
        _require(row["atom_id"] not in result, "source atom annotations repeat an atom")
        result[row["atom_id"]] = row
    return result


def _flow_witnesses(
    transformation: dict[str, Any], step: dict[str, Any], atom_id: str,
    atom: dict[str, Any], edits: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[str], str | None]:
    panel = transformation["panel_correspondence"]
    flow_bindings = panel["source_flow_bindings"]
    flow_by_id: dict[str, dict[str, Any]] = {}
    for flow in step.get("electron_flows", []):
        _require(isinstance(flow, dict) and isinstance(flow.get("flow_id"), str),
                 "Atlas10 before-step flow is invalid")
        _require(flow["flow_id"] not in flow_by_id, "Atlas10 before-step flow IDs repeat")
        flow_by_id[flow["flow_id"]] = flow
    binding_by_id: dict[str, dict[str, Any]] = {}
    for binding in flow_bindings:
        _require(isinstance(binding, dict) and isinstance(binding.get("flow_id"), str),
                 "source flow binding is invalid")
        _require(binding["flow_id"] not in binding_by_id, "source flow binding IDs repeat")
        binding_by_id[binding["flow_id"]] = binding

    edit_ids = [edit["edit_id"] for edit in edits]
    flow_ids = list(dict.fromkeys(edit["source_flow_id"] for edit in edits))
    witnesses: list[dict[str, Any]] = []
    full_refs: list[str] = []
    label_sets: list[tuple[str, ...]] = []
    for flow_id in flow_ids:
        binding = binding_by_id.get(flow_id)
        flow = flow_by_id.get(flow_id)
        _require(binding is not None and flow is not None,
                 "changed atom has an unbound source flow")
        occurrences: list[dict[str, Any]] = []
        for point_role in ("source_point", "target_point"):
            point = flow.get(point_role)
            _require(isinstance(point, dict) and isinstance(point.get("atoms"), list),
                     "Atlas10 flow point is invalid")
            for atom_index, descriptor in enumerate(point["atoms"]):
                _require(isinstance(descriptor, dict), "Atlas10 flow atom is invalid")
                raw_ref = descriptor.get("source_atom_ref")
                _require(isinstance(raw_ref, str) and raw_ref,
                         "Atlas10 flow atom lacks a source reference")
                molecule_ref, separator, local_ref = raw_ref.rpartition(".")
                _require(
                    separator == "." and bool(molecule_ref) and bool(local_ref),
                    "Atlas10 flow atom source reference is not fully qualified",
                )
                if local_ref != atom_id:
                    continue
                _require(descriptor.get("element") == atom.get("element"),
                         "Atlas10 flow atom element differs from the reviewed graph")
                flow_charge = descriptor.get("formal_charge")
                _require(
                    flow_charge is None or flow_charge == atom.get("formal_charge"),
                    "Atlas10 flow atom charge differs from the reviewed before graph",
                )
                labels = descriptor.get("semantic_labels")
                _require(
                    isinstance(labels, list)
                    and all(isinstance(item, str) and item for item in labels),
                    "Atlas10 flow atom semantic labels are invalid",
                )
                full_refs.append(raw_ref)
                label_sets.append(tuple(labels))
                occurrences.append({
                    "point_role": point_role,
                    "point_kind": point.get("point_kind"),
                    "atom_index": atom_index,
                    "atom": copy.deepcopy(descriptor),
                })
        _require(occurrences, "changed atom is absent from its bound source flow")
        witnesses.append({
            "source_step_id": binding["source_step_id"],
            "flow_id": flow_id,
            "bound_edit_ids": copy.deepcopy(binding["edit_ids"]),
            "changed_atom_edit_ids": [item for item in edit_ids if item in binding["edit_ids"]],
            "electron_flow": copy.deepcopy(flow),
            "source_atom_occurrences": occurrences,
        })
    unique_refs = list(dict.fromkeys(full_refs))
    unique_label_sets = list(dict.fromkeys(label_sets))
    if len(unique_refs) != 1:
        return witnesses, flow_ids, [], "ambiguous_molecule_qualified_source_atom_ref"
    if len(unique_label_sets) != 1:
        return witnesses, flow_ids, [], "conflicting_bound_flow_semantic_labels"
    return witnesses, flow_ids, list(unique_label_sets[0]), None


def _source_residue_label(
    atom_id: str, atom_element: str, semantic_labels: list[str], flow_reason: str | None,
    source_annotations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if flow_reason is not None:
        return {
            "status": "not_resolved", "raw_semantic_labels": semantic_labels,
            "residue_label": None, "reason": flow_reason,
        }
    residue_tokens = [label for label in semantic_labels if label.startswith("res:")]
    if not residue_tokens:
        return {
            "status": "not_resolved", "raw_semantic_labels": semantic_labels,
            "residue_label": None,
            "reason": "no_explicit_residue_label_on_bound_flow_atom",
        }
    parsed: list[dict[str, Any]] = []
    for token in residue_tokens:
        match = _RESIDUE_LABEL_RE.fullmatch(token)
        if match is None:
            return {
                "status": "not_resolved", "raw_semantic_labels": semantic_labels,
                "residue_label": None, "reason": "unsupported_explicit_residue_label",
            }
        parsed.append({
            "raw_label": token,
            "residue_name": match.group("residue"),
            "author_position": int(match.group("position")),
            "author_chain_id": match.group("chain"),
        })
    identities = {
        (row["residue_name"], row["author_position"], row["author_chain_id"])
        for row in parsed
    }
    if len(identities) != 1:
        return {
            "status": "not_resolved", "raw_semantic_labels": semantic_labels,
            "residue_label": None, "reason": "conflicting_explicit_residue_labels",
        }
    annotation = source_annotations.get(atom_id)
    if not isinstance(annotation, dict) or annotation.get("mrv_extra_label") not in residue_tokens:
        return {
            "status": "not_resolved", "raw_semantic_labels": semantic_labels,
            "residue_label": None, "reason": "residue_label_origin_not_preserved",
        }
    if (
        atom_element == "R"
        or annotation.get("mrv_alias") is not None
        or annotation.get("rgroup_ref") is not None
    ):
        return {
            "status": "not_resolved", "raw_semantic_labels": semantic_labels,
            "residue_label": None,
            "reason": "residue_label_on_aliased_or_pseudoatom_not_resolved",
        }
    return {
        "status": "explicit_bound_flow_mrv_extra_label",
        "raw_semantic_labels": semantic_labels,
        "residue_label": parsed[0],
        "reason": None,
    }


def _site_identity(site: dict[str, Any]) -> tuple[str, str, int]:
    site_id = site.get("site_id")
    match = _UNIPROT_SITE_RE.fullmatch(site_id) if isinstance(site_id, str) else None
    _require(match is not None, "Atlas10 catalyst site ID is invalid")
    residue_name = site.get("residue_name")
    sequence_position = site.get("sequence_position")
    _require(
        residue_name in _THREE_TO_ONE
        and _THREE_TO_ONE[residue_name] == match.group("residue")
        and type(sequence_position) is int
        and sequence_position == int(match.group("position"))
        and site.get("uniprot_id") == match.group("uniprot"),
        "Atlas10 catalyst site identity is internally inconsistent",
    )
    return match.group("uniprot"), residue_name, sequence_position


def _resolve_site(
    record: dict[str, Any], step: dict[str, Any], label: dict[str, Any], mcsa_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    return _resolve_labeled_site(
        record, step, label, mcsa_id,
        allowed_label_status="explicit_bound_flow_mrv_extra_label",
        match_basis="explicit_mrv_extra_residue_label_plus_step_catalyst_site_plus_direct_pdb_author_residue",
    )


def _resolve_labeled_site(
    record: dict[str, Any], step: dict[str, Any], label: dict[str, Any], mcsa_id: str,
    *, allowed_label_status: str, match_basis: str, site_scope: str = "selected_step",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Match a source label at an explicit step or whole-record residue scope."""
    _require(site_scope in {"selected_step", "record"}, "unsupported source site scope")
    unresolved_site = {
        "status": "not_resolved", "site_id": None, "match_basis": None,
        "site_record": None, "source_assertion_row_selection": "not_asserted",
        "reason": label["reason"],
    }
    unresolved_context = {
        "status": "not_resolved", "uniprot_id": None, "residue_name": None,
        "sequence_position": None, "numbering_system": None,
        "pdb_residue_mappings": [], "structures": [], "reason": label["reason"],
    }
    if label["status"] != allowed_label_status:
        return unresolved_site, unresolved_context

    catalyst_ids = step.get("catalyst_site_ids")
    _require(
        isinstance(catalyst_ids, list)
        and len(catalyst_ids) == len(set(catalyst_ids))
        and all(isinstance(item, str) and item for item in catalyst_ids),
        "Atlas10 before-step catalyst_site_ids are invalid",
    )
    sites = record.get("sites")
    _require(isinstance(sites, list), "Atlas10 record sites must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for site in sites:
        _require(isinstance(site, dict) and isinstance(site.get("site_id"), str),
                 "Atlas10 site is invalid")
        _require(site["site_id"] not in by_id, "Atlas10 site IDs repeat")
        _site_identity(site)
        mappings = site.get("pdb_mappings")
        _require(isinstance(mappings, list), "Atlas10 site PDB mappings must be an array")
        direct_locator_keys: set[tuple[str, str, int]] = set()
        for mapping in mappings:
            _require(isinstance(mapping, dict), "Atlas10 site PDB mapping is invalid")
            if mapping.get("applicability") != "direct":
                continue
            pdb_id = mapping.get("pdb_id")
            chain_id = mapping.get("chain_id")
            author_position = mapping.get("author_position")
            label_position = mapping.get("label_position")
            _require(
                isinstance(pdb_id, str) and bool(pdb_id)
                and isinstance(chain_id, str) and bool(chain_id)
                and type(author_position) is int and author_position > 0
                and type(label_position) is int and label_position > 0,
                "Atlas10 direct PDB residue mapping is invalid",
            )
            locator_key = (pdb_id, chain_id, author_position)
            _require(
                locator_key not in direct_locator_keys,
                "Atlas10 direct PDB residue mapping repeats an author locator",
            )
            direct_locator_keys.add(locator_key)
        by_id[site["site_id"]] = site
    _require(all(site_id in by_id for site_id in catalyst_ids),
             "Atlas10 step references an unknown catalyst site")

    residue = label["residue_label"]
    candidates: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    candidate_ids = catalyst_ids if site_scope == "selected_step" else list(by_id)
    for site_id in candidate_ids:
        site = by_id[site_id]
        matches = [
            row for row in site.get("pdb_mappings", [])
            if isinstance(row, dict)
            and row.get("applicability") == "direct"
            and row.get("author_position") == residue["author_position"]
            and row.get("chain_id") == residue["author_chain_id"]
            and site.get("residue_name") == residue["residue_name"]
        ]
        if matches:
            candidates.append((site, matches))
    if len(candidates) != 1:
        scope_name = "step_catalyst" if site_scope == "selected_step" else "record"
        reason = (f"no_{scope_name}_site_matches_explicit_residue_label" if not candidates
                  else f"multiple_{scope_name}_sites_match_explicit_residue_label")
        unresolved_site["reason"] = reason
        unresolved_context["reason"] = reason
        return unresolved_site, unresolved_context

    site, pdb_mappings = candidates[0]
    uniprot_id, residue_name, sequence_position = _site_identity(site)
    _require(site.get("mapping_status") == "source_and_coordinate_verified",
             "matched Atlas10 site lacks source-and-coordinate verification")
    evidence_ids = site.get("evidence_ids")
    _require(
        isinstance(evidence_ids, list)
        and f"source:M-CSA:{mcsa_id}" in evidence_ids
        and f"source:UniProtKB:{uniprot_id}" in evidence_ids,
        "matched Atlas10 site lacks its source or protein evidence",
    )
    structures: list[dict[str, Any]] = []
    structure_rows = record.get("structures")
    _require(isinstance(structure_rows, list), "Atlas10 record structures must be an array")
    for mapping in pdb_mappings:
        pdb_id = mapping.get("pdb_id")
        _require(f"source:PDB:{pdb_id}" in evidence_ids,
                 "matched Atlas10 site lacks its structure evidence")
        matches = [
            row for row in structure_rows
            if isinstance(row, dict)
            and row.get("pdb_id") == pdb_id
            and row.get("applicability") == "direct"
        ]
        _require(len(matches) == 1, "matched PDB residue lacks one direct structure context")
        ranges = matches[0].get("uniprot_chain_ranges")
        _require(
            isinstance(ranges, list)
            and any(
                isinstance(row, dict)
                and row.get("chain_id") == mapping.get("chain_id")
                and type(row.get("uniprot_start")) is int
                and type(row.get("uniprot_end")) is int
                and row["uniprot_start"] <= sequence_position <= row["uniprot_end"]
                for row in ranges
            ),
            "matched PDB residue lies outside the declared protein chain context",
        )
        structures.append(matches[0])
    return (
        {
            "status": ("unique_step_catalyst_site_match" if site_scope == "selected_step"
                       else "unique_record_site_match"),
            "site_id": site["site_id"],
            "match_basis": match_basis,
            "site_record": copy.deepcopy(site),
            "source_assertion_row_selection": "not_asserted",
            "reason": None,
        },
        {
            "status": "compiled_source_and_coordinate_verified_residue_context",
            "uniprot_id": uniprot_id,
            "residue_name": residue_name,
            "sequence_position": sequence_position,
            "numbering_system": site.get("numbering_system"),
            "pdb_residue_mappings": copy.deepcopy(pdb_mappings),
            "structures": copy.deepcopy(structures),
            "reason": None,
        },
    )


def _atom_row(
    transformation: dict[str, Any], record: dict[str, Any], step: dict[str, Any],
    changed: dict[str, Any], source_annotations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    atom = changed["atom"]
    edits = changed["edits"]
    witnesses, flow_ids, labels, flow_reason = _flow_witnesses(
        transformation, step, atom["atom_id"], atom, edits
    )
    source_label = _source_residue_label(
        atom["atom_id"], atom["element"], labels, flow_reason, source_annotations
    )
    site, protein = _resolve_site(
        record, step, source_label, transformation["record_binding"]["mcsa_id"]
    )
    return {
        "source_atom_id": atom["atom_id"],
        "element": atom["element"],
        "formal_charge": atom["formal_charge"],
        "edit_ids": [edit["edit_id"] for edit in edits],
        "source_flow_ids": flow_ids,
        "source_flow_witnesses": witnesses,
        "source_residue_label": source_label,
        "source_record_residue_mapping": site,
        "protein_structure_context": protein,
        "deposited_atom_identity": {
            "status": "not_asserted",
            "atom_name": None,
            "reason": (
                "a source depiction node is not equated to a deposited atom by this query"
            ),
        },
    }


def query_transformation_sites(
    values: dict[str, dict[str, Any]], *, atlas10_bundle: dict[str, Any],
    mcsa_id: str | None = None, source_atom_id: str | None = None,
    site_id: str | None = None,
) -> dict[str, Any]:
    """Join reviewed changed source nodes to explicit residue-site context."""
    source_atom_id = _string_filter(source_atom_id, "source_atom_id")
    site_id = _string_filter(site_id, "site_id")
    _require(
        site_id is None or _UNIPROT_SITE_RE.fullmatch(site_id) is not None,
        "site_id must be an exact protein site identifier such as P35049:S204",
    )
    _require(
        source_atom_id is None or mcsa_id is not None,
        "source_atom_id requires mcsa_id because source atom IDs are record-local",
    )
    source_query = query_transformation_sets(
        values, atlas10_bundle=atlas10_bundle, mcsa_id=mcsa_id
    )
    filters = {
        "mcsa_id": source_query["filters"]["mcsa_id"],
        "source_atom_id": source_atom_id,
        "site_id": site_id,
    }
    matches: list[dict[str, Any]] = []
    all_returned_atoms: list[dict[str, Any]] = []
    for set_item in source_query["sets"]:
        result = set_item["result"]
        for transformation in result["transformations"]:
            record, _proposal, step = _tier2_record(atlas10_bundle, transformation)
            source_annotations = _source_annotation_by_atom(transformation)
            all_rows = [
                _atom_row(transformation, record, step, changed, source_annotations)
                for changed in _changed_atoms(transformation)
            ]
            selected = [
                row for row in all_rows
                if (source_atom_id is None or row["source_atom_id"] == source_atom_id)
                and (
                    site_id is None
                    or row["source_record_residue_mapping"]["site_id"] == site_id
                )
            ]
            if not selected:
                continue
            resolved_all = sum(
                row["source_record_residue_mapping"]["status"]
                == "unique_step_catalyst_site_match" for row in all_rows
            )
            resolved_selected = sum(
                row["source_record_residue_mapping"]["status"]
                == "unique_step_catalyst_site_match" for row in selected
            )
            matches.append({
                "transformation_set_id": result["transformation_set_id"],
                "transformation_payload_sha256": result["transformation_payload_sha256"],
                "transformation": copy.deepcopy(transformation),
                "bound_atlas10_record": copy.deepcopy(record),
                "before_step": copy.deepcopy(step),
                "changed_source_atoms": copy.deepcopy(selected),
                "coverage": {
                    "total_changed_source_atom_count": len(all_rows),
                    "returned_changed_source_atom_count": len(selected),
                    "total_resolved_source_atom_count": resolved_all,
                    "total_unresolved_source_atom_count": len(all_rows) - resolved_all,
                    "returned_resolved_source_atom_count": resolved_selected,
                    "returned_unresolved_source_atom_count": len(selected) - resolved_selected,
                    "complete_changed_atom_site_coverage": resolved_all == len(all_rows),
                    "coverage_scope": "changed_before_graph_nodes_named_by_reviewed_edits",
                },
            })
            all_returned_atoms.extend(selected)
    resolved = sum(
        row["source_record_residue_mapping"]["status"]
        == "unique_step_catalyst_site_match" for row in all_returned_atoms
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "filters": filters,
        "source_transformation_query": copy.deepcopy(source_query),
        "match_count": len(matches),
        "changed_source_atom_count": len(all_returned_atoms),
        "resolved_source_atom_count": resolved,
        "unresolved_source_atom_count": len(all_returned_atoms) - resolved,
        "matches": matches,
        "query_semantics": {
            "changed_atom_basis": "before_graph_nodes_named_by_reviewed_graph_edits",
            "residue_label_basis": (
                "explicit_res_mrv_extra_label_on_the_same_bound_before_step_flow_atom"
            ),
            "site_join_basis": (
                "unique_step_declared_catalyst_site_and_direct_pdb_author_residue_mapping"
            ),
            "site_roles_apply_to": "source_record_residue_not_source_depiction_atom",
            "source_assertion_row_selected": False,
            "physical_cross_state_atom_correspondence": False,
            "deposited_atom_identity_asserted": False,
            "observed_intermediate_asserted": False,
            "transformation_trajectory_validated": False,
            "unlabeled_atom_adjacency_propagation": False,
            "atlas10_bundle_sha256": _canonical_sha256(atlas10_bundle),
            "empty_result": "no_matching_explicit_link_not_absence_of_catalytic_chemistry",
        },
    }


__all__ = ["SCHEMA_VERSION", "query_transformation_sites"]
