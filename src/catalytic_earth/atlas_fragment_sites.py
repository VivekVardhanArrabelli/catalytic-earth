"""Reviewed source-fragment membership beside reference-site functional evidence.

The fragment rule is deliberately separate from the direct endpoint-label query.
It traverses heavy-atom covalent bonds only, never assigns a PDB atom name, and
requires a unique source alias and the exact selected step's catalyst mapping.
"""
from __future__ import annotations

import copy
import hashlib
import json
import xml.etree.ElementTree as ET
from typing import Any, Callable

from .atlas10_source_adapters import parse_mcsa_scheme_flows
from .atlas_context_candidates import _ContextReview, _parse_panel
from .atlas_partial_panels import _raw_panel
from .atlas_transformation_sites import (
    _RESIDUE_LABEL_RE, _THREE_TO_ONE, _canonical_sha256, _mcsa_evidence,
    _records, _require, _resolve_labeled_site, query_transformation_sites,
)

SCHEMA_VERSION = "catalytic-earth.source-fragment-sites.v1"


def _bytes_sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _one(rows: list[Any], message: str) -> Any:
    _require(len(rows) == 1, message)
    return rows[0]


def _scheme(source: dict, step: dict) -> dict:
    return _one([
        row for row in source["step_schemes"]
        if row["step_id"] == step["source_step_id"]
        and row["content_sha256"] == step["source_scheme_sha256"]
    ], "source fragment step/scheme is not unique")


def derive_fragment_site(source: dict, record: dict, step: dict, atom_id: str) -> dict:
    """Derive a residue-fragment relation; callers bind the exact reviewed inputs."""
    scheme = _scheme(source, step)
    try:
        opaque, projected = _parse_panel(
            scheme["content_utf8"], scheme["content_sha256"], "source fragment"
        )
    except _ContextReview as error:
        raise ValueError(f"source fragment requires review: {error.code}") from error
    graph, nodes = _raw_panel(projected, "source fragment")
    atoms = {row["atom_id"]: row for row in graph["atoms"]}
    annotations = {row["atom_id"]: row for row in nodes}
    _require(atom_id in atoms, "source fragment atom is absent")
    flows = parse_mcsa_scheme_flows(scheme)["electron_flows"]
    _require(flows == step["electron_flows"], "source fragment flows differ from selected step")
    root = ET.fromstring(scheme["content_utf8"])
    parents = {child: parent for parent in root.iter() for child in parent}
    qualified = {}
    for raw in root.iter():
        if raw.tag.rsplit("}", 1)[-1] != "atom":
            continue
        parent = parents.get(raw)
        while parent is not None and parent.tag.rsplit("}", 1)[-1] != "molecule":
            parent = parents.get(parent)
        _require(parent is not None and parent.get("molID"), "source atom lacks molecule identity")
        qualified[raw.get("id")] = parent.get("molID") + "." + raw.get("id")
    for bond in graph["bonds"]:
        left, right = bond["atom_ids"]
        _require(qualified[left].rsplit(".", 1)[0] == qualified[right].rsplit(".", 1)[0],
                 "source fragment covalent bond crosses molecule identities")
    witnesses, references = [], set()
    for flow in flows:
        occurrences = [a for point in (flow["source_point"], flow["target_point"])
                       for a in point["atoms"]
                       if a["source_atom_ref"].rsplit(".", 1)[-1] == atom_id]
        for point in (flow["source_point"], flow["target_point"]):
            for descriptor in point["atoms"]:
                ref = descriptor["source_atom_ref"]
                _require(qualified.get(ref.rsplit(".", 1)[-1]) == ref,
                         "source fragment flow molecule identity differs")
        if occurrences:
            witnesses.append(copy.deepcopy(flow))
            references.update(a["source_atom_ref"] for a in occurrences)
            _require(all(a["element"] == atoms[atom_id]["element"]
                         and (a.get("formal_charge") is None or a["formal_charge"] == atoms[atom_id]["formal_charge"])
                         for a in occurrences), "source fragment endpoint element or charge differs")
    _require(len(references) == 1, "source fragment endpoint lacks one molecule-qualified flow reference")
    heavy = {key for key, atom in atoms.items() if atom["element"] != "H"}
    adjacency = {key: set() for key in heavy}
    for bond in graph["bonds"]:
        left, right = bond["atom_ids"]
        if left in heavy and right in heavy:
            adjacency[left].add(right)
            adjacency[right].add(left)
    component, pending = set(), [atom_id] if atom_id in heavy else []
    while pending:
        current = pending.pop()
        if current not in component:
            component.add(current)
            pending.extend(adjacency[current] - component)
    ordered = [key for key in atoms if key in component]
    aliases = [row for row in nodes if row["atom_id"] in component
               and row["mrv_alias"] is not None]
    label = {"status": "not_resolved", "raw_semantic_labels": [],
             "residue_label": None, "reason": None}
    own = annotations[atom_id]
    if atoms[atom_id]["element"] in {"H", "R"} or own["mrv_alias"] is not None or own["rgroup_ref"] is not None:
        label["reason"] = "hydrogen_alias_or_pseudoatom_is_not_a_residue_atom_anchor"
    elif len(aliases) != 1:
        label["reason"] = "source_fragment_does_not_have_one_alias_anchor"
    elif any(annotations[key]["mrv_extra_label"] is not None
             or annotations[key]["rgroup_ref"] is not None
             or atoms[key]["element"] == "R" for key in component):
        label["reason"] = "source_fragment_has_other_identity_labels_or_pseudoatoms"
    else:
        alias = aliases[0]["mrv_alias"]
        parsed = _RESIDUE_LABEL_RE.fullmatch("res:" + alias)
        if parsed is None or parsed.group("residue") not in _THREE_TO_ONE:
            label["reason"] = "unsupported_source_fragment_residue_alias"
        elif sum(row["mrv_alias"] == alias for row in nodes) != 1:
            label["reason"] = "source_residue_alias_is_not_unique_in_panel"
        else:
            label.update(status="unique_source_fragment_alias", residue_label={
                "raw_label": alias, "residue_name": parsed.group("residue"),
                "author_position": int(parsed.group("position")),
                "author_chain_id": parsed.group("chain"),
            })
    site, protein = _resolve_labeled_site(
        record, step, label, source["record_id"],
        allowed_label_status="unique_source_fragment_alias",
        match_basis="unique_fragment_mrv_alias_plus_step_catalyst_site_plus_direct_pdb_author_residue",
    )
    return {
        "source_step_id": step["source_step_id"], "source_atom_id": atom_id,
        "source_atom_ref": next(iter(references)),
        "source_scheme_sha256": scheme["content_sha256"],
        "source_flow_witnesses": witnesses,
        "fragment": {
            "basis": "heavy_atom_covalent_connected_component",
            "atom_ids": ordered,
            "atoms": [copy.deepcopy(atoms[key]) for key in ordered],
            "annotations": [copy.deepcopy(annotations[key]) for key in ordered],
            "bonds": [copy.deepcopy(bond) for bond in graph["bonds"]
                      if set(bond["atom_ids"]) <= component],
            "alias_anchors": copy.deepcopy(aliases),
            "boundary_bonds": [copy.deepcopy(bond) for bond in graph["bonds"]
                               if len(set(bond["atom_ids"]) & component) == 1],
            "opaque_panel_context": opaque,
        },
        "source_residue_label": label,
        "source_record_residue_mapping": site,
        "protein_structure_context": protein,
        "source_step": copy.deepcopy(step),
        "deposited_atom_identity": {"status": "not_asserted", "atom_name": None},
    }


def _validate_bundle(bundle: dict, atlas10: dict, evidence_query: dict) -> dict:
    spec, review = bundle["spec"], bundle["review"]
    _require(spec["schema_version"] == SCHEMA_VERSION, "source fragment schema differs")
    _require(review["status"] == "source_reviewed_computational"
             and review["spec_sha256"] == _canonical_sha256(spec)
             and review["independent_human_validation"] is False
             and review["experimental_validation"] is False,
             "source fragment review is stale or exceeds scope")
    _require(spec["atlas10_bundle_sha256"] == _canonical_sha256(atlas10),
             "source fragment Atlas10 binding differs")
    _require(spec["evidence_payload_sha256"] == evidence_query["evidence_payload_sha256"],
             "source fragment functional evidence binding differs")
    _require(evidence_query["schema_version"] == "catalytic-earth.mechanism-evidence-query.v1",
             "source fragment evidence query schema differs")
    matches = evidence_query["matches"]
    _require(evidence_query["case_count"] == len(matches)
             and evidence_query["matched_observation_count"] == sum(len(row["matched_observations"]) for row in matches),
             "source fragment evidence query counts differ")
    case_ids = [row["case"]["case_id"] for row in matches]
    _require(len(case_ids) == len(set(case_ids)), "source fragment evidence cases repeat")
    for match in matches:
        case = match["case"]
        _require(case["case_id"] == spec["evidence_case_id"]
                 and case["transformation_binding"] == spec["transformation_binding"],
                 "source fragment evidence case or transformation binding differs")
        _require(_canonical_sha256(case) == spec["evidence_case_sha256"],
                 "source fragment evidence case content differs")
        filters = evidence_query["filters"]
        expected = [row for row in case["observations"]
                    if (filters["variant"] is None or row["variant"]["variant_id"] == filters["variant"])
                    and (filters["endpoint"] is None or row["endpoint"]["kind"] == filters["endpoint"])]
        _require(match["matched_observations"] == expected
                 and match["matched_observation_ids"] == [row["observation_id"] for row in expected],
                 "source fragment filtered observations differ from the bound case")
    sources = {}
    for binding in spec["source_bindings"]:
        source_id = binding["source_id"]
        _require(source_id not in sources, "source fragment source IDs repeat")
        raw = bundle["source_snapshots_utf8"][source_id].encode("utf-8")
        _require(_bytes_sha(raw) == binding["sha256"], "source fragment source hash differs")
        source = json.loads(raw)
        _require(source["source"] == "M-CSA" and source["record_id"] == source_id,
                 "source fragment source identity differs")
        sources[source_id] = source
    _require(set(sources) == set(bundle["source_snapshots_utf8"]),
             "source fragment package contains unbound sources")
    return sources


def query_fragment_sites(bundle: dict, *, atlas10_bundle: dict, evidence_query: dict,
                         transformation_values: dict) -> dict:
    """Compose reviewed source membership with existing filtered reference evidence."""
    sources = _validate_bundle(bundle, atlas10_bundle, evidence_query)
    transformed = query_transformation_sites(transformation_values, atlas10_bundle=atlas10_bundle)
    binding = bundle["spec"]["transformation_binding"]
    transformation = _one([
        match for match in transformed["matches"]
        if match["transformation_set_id"] == binding["transformation_set_id"]
        and match["transformation_payload_sha256"] == binding["transformation_payload_sha256"]
        and match["transformation"]["transformation_id"] == binding["transformation_id"]
        and match["transformation"]["record_binding"]["mcsa_id"] == binding["mcsa_id"]
    ], "source fragment reviewed transformation binding differs")
    bindings = {row["source_id"]: row for row in bundle["spec"]["source_bindings"]}
    relations, seen = [], set()
    for request in bundle["spec"]["requests"]:
        relation_id = request["relation_id"]
        _require(relation_id not in seen, "source fragment relation IDs repeat")
        seen.add(relation_id)
        source = sources[request["source_id"]]
        record = _one([row for row in _records(atlas10_bundle)
                       if row.get("record_id") == request["record_id"]
                       and row.get("evidence_tier") == 2], "source fragment record is not unique Tier2")
        _require(_mcsa_evidence(record, source["record_id"])["snapshot_sha256"]
                 == bindings[source["record_id"]]["sha256"], "source fragment record binding differs")
        proposal = _one([row for row in record["mechanism_proposals"]
                         if row["proposal_id"] == request["proposal_id"]
                         and row["source_record_id"] == source["record_id"]],
                        "source fragment proposal is not unique")
        step = _one([row for row in proposal["mechanism_steps"]
                     if row["source_step_id"] == request["source_step_id"]],
                    "source fragment step is not unique")
        scheme = _scheme(source, step)
        _require(scheme["mechanism_id"] == proposal["source_mechanism_id"]
                 and _bytes_sha(scheme["content_utf8"].encode("utf-8")) == step["source_scheme_sha256"],
                 "source fragment scheme/proposal binding differs")
        relation = derive_fragment_site(source, record, step, request["source_atom_id"])
        _require(relation["source_atom_ref"] == request["source_atom_ref"],
                 "source fragment request molecule-qualified atom differs")
        relation.update(relation_id=relation_id, source_id=source["record_id"],
                        record_id=record["record_id"], proposal_id=proposal["proposal_id"])
        site = relation["source_record_residue_mapping"]["site_record"]
        observations, cases = [], []
        if site is not None:
            for match in evidence_query["matches"]:
                case = match["case"]
                if case["record_binding"]["record_id"] != record["record_id"] or case["proposal_binding"]["proposal_id"] != proposal["proposal_id"]:
                    continue
                if (case["site_context_binding"]["site_id"] != site["site_id"]
                        or case["applicability"]["uniprot_id"] != site["uniprot_id"]):
                    continue
                direct_ids = {row["evidence_id"] for row in case["evidence_references"]
                              if row["applicability"] == "direct"}
                selected = [row for row in match["matched_observations"]
                            if direct_ids.intersection(row["evidence_ids"])
                            and row["variant"]["variant_id"] == case["focal_variant_id"]
                            and row["variant"]["uniprot_id"] == site["uniprot_id"]
                            and any(sub["wild_type_residue"] == _THREE_TO_ONE[site["residue_name"]]
                                    and sub["sequence_position"] == site["sequence_position"]
                                    for sub in row["variant"]["substitutions"])]
                if selected:
                    observations.extend(copy.deepcopy(selected))
                    cases.append(case["case_id"])
        bound_transformation = transformation["transformation"]
        _require(bound_transformation["record_binding"]["record_id"] == record["record_id"]
                 and bound_transformation["proposal_binding"]["proposal_id"] == proposal["proposal_id"],
                 "source fragment request differs from the reviewed transformation proposal")
        if step["source_step_id"] == transformation["before_step"]["source_step_id"]:
            changed = _one([row for row in transformation["changed_source_atoms"]
                            if row["source_atom_id"] == request["source_atom_id"]],
                           "source fragment atom is not a reviewed changed before atom")
            _require(set(changed["source_flow_ids"]) <= {row["flow_id"] for row in relation["source_flow_witnesses"]},
                     "source fragment reviewed edit flow differs")
            relation["transformation_context"] = {
                "status": "reviewed_changed_before_atom", "binding": copy.deepcopy(binding),
                "changed_atom_witness": copy.deepcopy(changed),
            }
        else:
            relation["transformation_context"] = {
                "status": "source_step_only_not_a_reviewed_transition", "binding": None,
                "changed_atom_witness": None,
            }
        relation["functional_evidence"] = {
            "relationship": "reference_site_context_not_exact_assayed_construct",
            "evidence_payload_sha256": evidence_query["evidence_payload_sha256"],
            "case_ids": cases, "matched_observations": observations,
            "source_arrow_experimentally_validated": False,
        }
        relations.append(relation)
    return {
        "schema_version": SCHEMA_VERSION, "relation_count": len(relations),
        "resolved_relation_count": sum(row["source_record_residue_mapping"]["site_id"] is not None for row in relations),
        "relations": relations, "review": copy.deepcopy(bundle["review"]),
        "source_bindings": copy.deepcopy(bundle["spec"]["source_bindings"]),
        "query_semantics": {
            "counted_object": "source_fragment_reference_site_relation",
            "observation_filters_apply_to": "copied_observations_not_source_relations",
            "direct_endpoint_label_query_changed": False,
            "source_residue_role_is_atom_role": False,
            "chemical_residue_identity_inferred_from_graph_alone": False,
            "stereochemistry_or_coordination_interpreted": False,
            "exact_assayed_construct_identity": False,
            "deposited_atom_identity": False,
            "nondetection_is_numeric_zero": False,
            "exchange_is_racemization": False,
            "source_arrow_experimentally_validated": False,
            "empty_observation_match": "no_matching_retained_observation_not_absence_of_activity",
        },
    }


def build_fragment_sites(spec: dict, review: dict, load_bytes: Callable[[str], bytes],
                         *, atlas10_bundle: dict, evidence_query: dict,
                         transformation_values: dict) -> dict:
    """Build reproducibly from manually reviewed source and implementation bindings."""
    for path, digest in review["implementation_bindings"].items():
        _require(_bytes_sha(load_bytes(path)) == digest, f"source fragment review binding differs: {path}")
    bundle = {"spec": spec, "review": review, "source_snapshots_utf8": {
        row["source_id"]: load_bytes(row["path"]).decode("utf-8") for row in spec["source_bindings"]
    }}
    query_fragment_sites(bundle, atlas10_bundle=atlas10_bundle, evidence_query=evidence_query,
                         transformation_values=transformation_values)
    return bundle
