"""Compare declared source-panel graphs and complete electron-flow endpoints.

This repository query checks supplied depiction-locator maps; it does not infer
physical atom identity, a reaction trajectory, or equivalent enzyme function.
All case selections and proposed correspondences belong in the input data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_source_adapters import parse_mcsa_scheme_flows
from catalytic_earth.atlas_context_candidates import _parse_panel
from catalytic_earth.atlas_partial_panels import _raw_panel
from catalytic_earth.canonical_hash import canonical_file_sha256


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _read_bound(root, binding):
    path = (root / binding["path"]).resolve()
    _require(path.is_relative_to(root.resolve()), "bound path leaves repository")
    raw = path.read_bytes()
    _require(canonical_file_sha256(path) == binding["sha256"], "bound file hash differs")
    return json.loads(raw)


def _panel(root, sources, side):
    _require(set(side) == {"source_id", "mechanism_id", "step_id", "scheme_sha256",
                           "component_labels", "excluded_atoms"}, "source-side fields differ")
    binding = sources[side["source_id"]]
    snapshot = _read_bound(root, binding["snapshot"])
    record_bundle = _read_bound(root, binding["records"])
    records = [r for r in record_bundle["records"] if r["record_id"] == binding["record_id"]]
    _require(len(records) == 1, "record binding is ambiguous or missing")
    record = records[0]
    _require(side["source_id"] == snapshot["record_id"], "displayed source identity differs")
    _require(record["mcsa_id"] == snapshot["record_id"], "source and record identities differ")
    _require(record["source"]["snapshot_sha256"] == binding["snapshot"]["sha256"],
             "compiled record belongs to another source snapshot")
    schemes = [s for s in snapshot["step_schemes"] if
               s["mechanism_id"] == side["mechanism_id"] and s["step_id"] == side["step_id"]]
    _require(len(schemes) == 1, "source step is ambiguous or missing")
    scheme = schemes[0]
    _require(scheme["content_sha256"] == side["scheme_sha256"], "scheme binding differs")
    _require(hashlib.sha256(scheme["content_utf8"].encode()).hexdigest() == side["scheme_sha256"],
             "scheme content hash differs")
    context, projected = _parse_panel(scheme["content_utf8"], side["scheme_sha256"], side["source_id"])
    graph, metadata = _raw_panel(projected, side["source_id"])
    atoms = {a["atom_id"]: a for a in graph["atoms"]}
    neighbors = {a: set() for a in atoms}
    for bond in graph["bonds"]:
        a, b = bond["atom_ids"]
        neighbors[a].add(b)
        neighbors[b].add(a)
    selected = set()
    for label in side["component_labels"]:
        seeds = {a["atom_id"] for a in metadata if a["mrv_extra_label"] == label}
        _require(bool(seeds), "component label has no source atom")
        component, pending = set(), [next(iter(seeds))]
        while pending:
            atom = pending.pop()
            if atom not in component:
                component.add(atom)
                pending.extend(neighbors[atom] - component)
        _require(seeds <= component, "component label spans disconnected fragments")
        selected.update(component)
    full_selected = set(selected)
    exclusions = {a["atom_id"]: a for a in side["excluded_atoms"]}
    _require(len(exclusions) == len(side["excluded_atoms"]), "repeated excluded atom")
    _require(set(exclusions) <= selected, "excluded atom lies outside selected components")
    _require(all(a.get("reason") for a in exclusions.values()), "excluded atom lacks reason")
    selected -= set(exclusions)
    _require(bool(selected), "empty compared graph")
    flows = parse_mcsa_scheme_flows(scheme)["electron_flows"]
    _require(bool(flows), "source step has no electron flows")
    endpoints = {a["source_atom_ref"].rsplit(".", 1)[-1]
                 for f in flows for key in ("source_point", "target_point") for a in f[key]["atoms"]}
    _require(endpoints <= selected, "comparison omits a source electron-flow endpoint")
    _require(len({f["flow_id"] for f in flows}) == len(flows), "source flow IDs repeat")
    raw_atoms = {a.get("id"): a for a in ET.fromstring(scheme["content_utf8"]).iter("atom")}
    # Preserve raw electronic/isotope/placeholder tokens; no valence or H completion.
    signatures = {a: (atoms[a]["element"], atoms[a]["formal_charge"],
                      raw_atoms[a].get("isotope"), raw_atoms[a].get("lonePair"),
                      raw_atoms[a].get("rgroupRef"), bool(raw_atoms[a].get("mrvAlias")))
                  for a in selected}
    bonds = {tuple(sorted(b["atom_ids"])): b["order"] for b in graph["bonds"]
             if set(b["atom_ids"]) <= selected}
    boundary = [b for b in graph["bonds"] if len(set(b["atom_ids"]) & selected) == 1]
    # Stereo at a compared atom needs an explicit richer relation, never silent removal.
    _require(not any(set(b["ordered_atom_refs2"]) & selected for b in context["bond_stereo"]),
             "compared graph touches uninterpreted source stereochemistry")
    proposals = [p for p in record["mechanism_proposals"]
                 if p["source_mechanism_id"] == side["mechanism_id"]]
    _require(len(proposals) == 1, "compiled proposal binding differs")
    steps = [s for s in proposals[0]["mechanism_steps"] if s["source_step_id"] == side["step_id"]]
    _require(len(steps) == 1 and steps[0]["source_scheme_sha256"] == side["scheme_sha256"],
             "compiled step binding differs")
    _require(steps[0]["electron_flows"] == flows, "compiled and raw source flows differ")
    return {"atoms": signatures, "bonds": bonds, "flows": flows, "selected": selected,
            "full_selected": full_selected, "context": context, "boundary": boundary,
            "excluded_atoms": [{**row, "source_attributes": dict(raw_atoms[a].attrib)}
                               for a, row in exclusions.items()],
            "metadata": [a for a in metadata if a["atom_id"] in full_selected],
            "summary": steps[0]["summary"], "scope": record["source_scope"],
            "abstentions": record["mandatory_abstentions"]}


def _flow_signature(flow, mapping):
    return tuple((flow[key]["point_kind"], tuple(sorted(
        mapping[a["source_atom_ref"].rsplit(".", 1)[-1]] for a in flow[key]["atoms"]
    ))) for key in ("source_point", "target_point"))


def compare(data, root=ROOT, relation_id=None):
    _require(data["schema_version"] == "catalytic-earth.source-step-correspondences.v1", "unsupported schema")
    _require(isinstance(data["relations"], list) and bool(data["relations"]), "no relations to check")
    _require(isinstance(data["limitations"], list) and bool(data["limitations"])
             and all(isinstance(v, str) and v.strip() for v in data["limitations"]),
             "declared limitations are missing or invalid")
    attribution = data["attribution"]
    _require(set(attribution) == {"source", "license", "citation", "source_urls", "changes"}
             and all(attribution.values()), "source attribution is incomplete")
    rows = []
    seen = set()
    verified_source_ids = set()
    for relation in data["relations"]:
        _require(set(relation) == {"id", "left", "right", "mappings", "limitations"},
                 "relation fields differ; findings must be derived by the query")
        _require(isinstance(relation["limitations"], list)
                 and all(isinstance(v, str) and v.strip() for v in relation["limitations"]),
                 "declared relation limitations are invalid")
        _require(relation["id"] not in seen, "relation IDs repeat")
        seen.add(relation["id"])
        if relation_id is not None and relation["id"] != relation_id:
            continue
        left, right = [_panel(root, data["sources"], relation[side]) for side in ("left", "right")]
        verified_source_ids.update(relation[side]["source_id"] for side in ("left", "right"))
        _require(bool(relation["mappings"]), "no declared map")
        mapping_keys = set()
        checked = []
        endpoint_maps = set()
        for proposal in relation["mappings"]:
            mapping = proposal["atom_map"]
            _require(set(mapping) == left["selected"] and set(mapping.values()) == right["selected"]
                     and len(mapping) == len(set(mapping.values())), "atom map is not a complete bijection")
            key = tuple(sorted(mapping.items()))
            _require(key not in mapping_keys, "duplicate declared atom map")
            mapping_keys.add(key)
            _require(all(left["atoms"][a] == right["atoms"][b] for a, b in mapping.items()),
                     "mapped atom chemistry or raw electronic tokens differ")
            mapped_bonds = {tuple(sorted(mapping[a] for a in pair)): order for pair, order in left["bonds"].items()}
            _require(mapped_bonds == right["bonds"], "mapped covalent graph differs")
            flow_map = proposal["flow_map"]
            lf, rf = [{f["flow_id"]: f for f in panel["flows"]} for panel in (left, right)]
            _require(set(flow_map) == set(lf) and set(flow_map.values()) == set(rf)
                     and len(flow_map) == len(set(flow_map.values())), "flow map is not a complete bijection")
            identity = {a: a for a in right["selected"]}
            _require(all(_flow_signature(lf[a], mapping) == _flow_signature(rf[b], identity)
                         for a, b in flow_map.items()), "directed electron-flow endpoints differ")
            endpoints = {a["source_atom_ref"].rsplit(".", 1)[-1]
                         for flow in lf.values() for point in ("source_point", "target_point")
                         for a in flow[point]["atoms"]}
            endpoint_maps.add(tuple(sorted((a, mapping[a]) for a in endpoints)))
            checked.append({"atom_map": mapping, "flow_map": flow_map})
        sides = {}
        for name, panel in (("left", left), ("right", right)):
            sides[name] = {"binding": relation[name], "source_step_summary": panel["summary"],
                           "selected_atom_count": len(panel["full_selected"]),
                           "compared_atom_count": len(panel["selected"]),
                           "compared_bond_count": len(panel["bonds"]),
                           "excluded_atoms": panel["excluded_atoms"],
                           "uncompared_boundary_bonds": panel["boundary"],
                           "source_atom_metadata": panel["metadata"],
                           "opaque_context_not_compared": panel["context"],
                           "record_source_scope": panel["scope"], "mandatory_abstentions": panel["abstentions"]}
        complete = not left["excluded_atoms"] and not right["excluded_atoms"]
        rows.append({"id": relation["id"],
                     "finding": ("Complete selected covalent actor graphs correspond; all directed source-arrow endpoints are preserved."
                                 if complete else "Partial selected covalent actor graphs correspond; all directed source-arrow endpoints are preserved and excluded atoms remain explicit."),
                     "complete_selected_covalent_actor_graphs": complete,
                     "all_source_flow_endpoints_preserved": True,
                     "reaction_endpoint_map_invariant_across_declared_maps": len(endpoint_maps) == 1,
                     "declared_maps_checked": len(checked), "all_isomorphisms_enumerated_by_query": False,
                     "mappings": checked, **sides, "declared_limitations": relation["limitations"]})
    _require(relation_id is None or bool(rows), "unknown relation ID")
    return {"schema_version": "catalytic-earth.source-step-correspondence-query.v1",
            "evidence_kind": "checked_source_depiction_correspondence",
            "physical_atom_map": False, "after_state_replay": False,
            "whole_mechanism_equivalence": False, "independent_validation": False,
            "attribution": attribution,
            "source_bindings": {key: data["sources"][key] for key in sorted(verified_source_ids)},
            "relations": rows,
            "declared_limitations": data["limitations"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--relation")
    args = parser.parse_args()
    print(json.dumps(compare(json.loads(args.spec.read_text()), relation_id=args.relation), indent=2))


if __name__ == "__main__":
    main()
