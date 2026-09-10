"""Build source-bound deposit contexts from declarative mmCIF selections.

The projector preserves exact selected source rows and may invoke the shared
biological-assembly projector for declared coordinate selections.  Scientific
interpretations remain data: the runtime only checks that each assertion cites
declared row, atom-selection, or distance-pair identifiers.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Any

from .atlas_assembly_context import project_assembly
from .atlas_primary_source_check import parse_mmcif_categories
from .canonical_hash import canonical_file_sha256
from .atlas_transformations import _validate_graph, transformation_payload_sha256


SPEC_SCHEMA_VERSION = "catalytic-earth.deposit-context-spec.v1"
BUNDLE_SCHEMA_VERSION = "catalytic-earth.deposit-context.v1"
REVIEW_SCHEMA_VERSION = "catalytic-earth.deposit-context-review.v1"
REVIEW_DECISION = "accept_source_scoped_deposit_context"

_SPEC_FIELDS = {
    "schema_version",
    "packet_id",
    "source_binding",
    "row_selections",
    "interpretation",
}
_SOURCE_BINDING_FIELDS = {"path", "sha256"}
_ROW_SELECTION_FIELDS = {
    "selection_id",
    "category",
    "match",
    "expected_row_count",
}
_INTERPRETATION_FIELDS = {"assertions", "not_established"}
_ASSERTION_FIELDS = {
    "assertion_id",
    "status",
    "statement",
    "supporting_selection_ids",
}
_ASSERTION_STATUSES = {
    "computed_coordinate_description",
    "deposited_source_assertion",
    "project_interpretation",
    "unresolved_source_conflict",
}
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic finite JSON bytes used for generated projections."""

    try:
        return (
            json.dumps(
                value,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("deposit context must be finite plain JSON") from exc


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    _require(
        isinstance(value, list) and (not nonempty or bool(value)),
        f"{label} must be a{' nonempty' if nonempty else 'n'} array",
    )
    return value


def _exact(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    row = _object(value, label)
    actual = set(row)
    _require(
        actual == fields,
        f"{label} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return row


def _text(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{label} must be nonempty text",
    )
    return value


def _identifier(value: Any, label: str) -> str:
    result = _text(value, label)
    _require(_ID_RE.fullmatch(result) is not None, f"{label} is invalid")
    return result


def _safe_bound_path(
    binding: Any, *, repo_root: Path, label: str = "source binding"
) -> tuple[dict[str, str], Path]:
    row = _exact(binding, _SOURCE_BINDING_FIELDS, label)
    relative = _text(row["path"], f"{label}.path")
    posix = PurePosixPath(relative)
    windows = PureWindowsPath(relative)
    _require(
        "\\" not in relative
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and relative == posix.as_posix()
        and "." not in posix.parts
        and ".." not in posix.parts,
        f"{label}.path must be a safe repository-relative POSIX path",
    )
    digest = row["sha256"]
    _require(
        isinstance(digest, str) and _SHA_RE.fullmatch(digest) is not None,
        f"{label}.sha256 must be a lowercase SHA-256",
    )
    path = (repo_root / Path(posix)).resolve()
    _require(
        repo_root in path.parents and path.is_file(),
        f"{label} is missing or outside the repository",
    )
    _require(
        canonical_file_sha256(path) == digest,
        f"{label} hash differs",
    )
    return {"path": relative, "sha256": digest}, path


def _row_projections(
    selections: Any, *, tables: dict[str, list[dict[str, str]]]
) -> tuple[list[dict[str, Any]], set[str]]:
    declarations = _array(selections, "row_selections", nonempty=True)
    projections: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, raw in enumerate(declarations):
        label = f"row_selections[{index}]"
        declaration = _exact(raw, _ROW_SELECTION_FIELDS, label)
        selection_id = _identifier(
            declaration["selection_id"], f"{label}.selection_id"
        )
        _require(selection_id not in identifiers, "row selection IDs repeat")
        identifiers.add(selection_id)
        category = _text(declaration["category"], f"{label}.category")
        _require(category == category.lower(), f"{label}.category must be lowercase")
        _require(category in tables, f"{label}.category is unsupported")
        source_rows = tables[category]
        _require(source_rows, f"{label}.category has no deposited rows")

        match = _object(declaration["match"], f"{label}.match")
        _require(
            all(isinstance(key, str) and bool(key) for key in match),
            f"{label}.match fields must be nonempty strings",
        )
        _require(
            all(isinstance(value, str) for value in match.values()),
            f"{label}.match values must be raw mmCIF strings",
        )
        for field in match:
            _require(
                all(field in row for row in source_rows),
                f"{label}.match field {field!r} is absent from deposited {category} rows",
            )
        expected = declaration["expected_row_count"]
        _require(
            type(expected) is int and expected > 0,
            f"{label}.expected_row_count must be a positive integer",
        )
        matched = [
            row
            for row in source_rows
            if all(row[field] == value for field, value in match.items())
        ]
        _require(
            len(matched) == expected,
            f"{label} selected {len(matched)} rows; expected {expected}",
        )
        projections.append(
            {
                "selection_id": selection_id,
                "category": category,
                "match": copy.deepcopy(match),
                "expected_row_count": expected,
                "rows": copy.deepcopy(matched),
            }
        )
    return projections, identifiers


def _assembly_projection(
    spec: dict[str, Any], *, cif_text: str
) -> tuple[dict[str, Any] | None, set[str]]:
    if "assembly_spec" not in spec:
        return None, set()
    assembly_spec = _object(spec["assembly_spec"], "assembly_spec")
    projection = project_assembly(cif_text, assembly_spec)
    identifiers: list[str] = []
    for index, selection in enumerate(
        _array(assembly_spec.get("selections"), "assembly_spec.selections")
    ):
        row = _object(selection, f"assembly_spec.selections[{index}]")
        identifiers.append(
            _identifier(
                row.get("selection_id"),
                f"assembly_spec.selections[{index}].selection_id",
            )
        )
    for index, pair in enumerate(
        _array(assembly_spec.get("distance_pairs"), "assembly_spec.distance_pairs")
    ):
        row = _object(pair, f"assembly_spec.distance_pairs[{index}]")
        identifiers.append(
            _identifier(
                row.get("pair_id"),
                f"assembly_spec.distance_pairs[{index}].pair_id",
            )
        )
    _require(
        len(identifiers) == len(set(identifiers)),
        "assembly selection and distance-pair IDs repeat",
    )
    return projection, set(identifiers)


def _interpretation(value: Any, *, declared_ids: set[str]) -> dict[str, Any]:
    interpretation = _exact(value, _INTERPRETATION_FIELDS, "interpretation")
    assertions = _array(
        interpretation["assertions"], "interpretation.assertions", nonempty=True
    )
    assertion_ids: set[str] = set()
    for index, raw in enumerate(assertions):
        label = f"interpretation.assertions[{index}]"
        assertion = _exact(raw, _ASSERTION_FIELDS, label)
        assertion_id = _identifier(assertion["assertion_id"], f"{label}.assertion_id")
        _require(assertion_id not in assertion_ids, "interpretation assertion IDs repeat")
        assertion_ids.add(assertion_id)
        _require(
            assertion["status"] in _ASSERTION_STATUSES,
            f"{label}.status is unsupported",
        )
        _text(assertion["statement"], f"{label}.statement")
        support = _array(
            assertion["supporting_selection_ids"],
            f"{label}.supporting_selection_ids",
            nonempty=True,
        )
        _require(
            all(isinstance(item, str) and _ID_RE.fullmatch(item) for item in support),
            f"{label}.supporting_selection_ids are invalid",
        )
        _require(
            len(support) == len(set(support)),
            f"{label}.supporting_selection_ids repeat",
        )
        missing = set(support) - declared_ids
        _require(
            not missing,
            f"{label} references undeclared selection IDs {sorted(missing)}",
        )
    boundaries = _array(
        interpretation["not_established"],
        "interpretation.not_established",
        nonempty=True,
    )
    _require(
        all(isinstance(item, str) and bool(item.strip()) for item in boundaries),
        "interpretation.not_established entries must be nonempty text",
    )
    _require(
        len(boundaries) == len(set(boundaries)),
        "interpretation.not_established entries repeat",
    )
    return copy.deepcopy(interpretation)


def _component_side(side: dict[str, Any], tables: dict) -> dict:
    """Resolve a complete dictionary and one explicitly identified instance."""
    _exact(side, {"component_id", "label_asym_id", "model_id", "site_id"}, "component side")
    _require(all(isinstance(v, str) and v.strip() and v not in {"?", "."}
                 for v in side.values()), "component selectors must be nonmissing raw strings")
    comp, asym = side["component_id"], side["label_asym_id"]
    atoms = [r for r in tables["_chem_comp_atom"] if r["comp_id"] == comp]
    bonds = [r for r in tables["_chem_comp_bond"] if r["comp_id"] == comp]
    by_id = {r["atom_id"]: r for r in atoms}
    _require(bool(atoms) and len(by_id) == len(atoms), "missing or duplicate component atoms")
    _require(bool(bonds), "component bond dictionary is missing")
    _require(all(r.get("pdbx_stereo_config") in {"N", "R", "S"} for r in atoms),
             "component atom stereochemistry is unspecified or unsupported")
    _require(all(r.get("type_symbol") not in {None, "?", "."} and
                 r.get("pdbx_aromatic_flag") in {"Y", "N"} for r in atoms),
             "component element or aromaticity is unspecified")
    edges = {}
    for row in bonds:
        key = tuple(sorted((row["atom_id_1"], row["atom_id_2"])))
        _require(key[0] != key[1] and set(key) <= set(by_id) and key not in edges,
                 "invalid or duplicate component bond")
        _require(row.get("value_order") in {"sing", "doub", "trip", "arom"} and
                 row.get("pdbx_stereo_config") in {"N", "E", "Z"} and
                 row.get("pdbx_aromatic_flag") in {"Y", "N"},
                 "component bond order or stereochemistry is unsupported")
        edges[key] = {k: v for k, v in row.items()
                      if k not in {"comp_id", "atom_id_1", "atom_id_2", "pdbx_ordinal"}}
    instances = [r for r in tables["_pdbx_nonpoly_scheme"]
                 if r["asym_id"] == asym and r["mon_id"] == comp]
    _require(len(instances) == 1, "component instance is missing or ambiguous")
    instance = instances[0]
    def insertion(value):
        return None if value in {"?", "."} else value
    coords = [r for r in tables["_atom_site"] if r["label_asym_id"] == asym and
              r["label_comp_id"] == comp and r["pdbx_pdb_model_num"] == side["model_id"]]
    coordinate_ids = {r["label_atom_id"] for r in coords}
    _require(bool(coords) and len(coordinate_ids) == len(coords),
             "missing coordinates or unresolved alternative conformers")
    _require(all(r["label_alt_id"] == "." for r in coords),
             "alternative conformer comparison is not implemented")
    _require(coordinate_ids <= set(by_id), "coordinate atom is absent from dictionary")
    heavy = {a for a, r in by_id.items() if r["type_symbol"] != "H"}
    _require(heavy <= coordinate_ids, "coordinate instance lacks dictionary heavy atoms")
    _require(all(r["type_symbol"] == by_id[r["label_atom_id"]]["type_symbol"] and
                 r["auth_asym_id"] == instance["pdb_strand_id"] and
                 r["auth_seq_id"] == instance["pdb_seq_num"] and
                 r["auth_comp_id"] == instance["pdb_mon_id"] and
                 insertion(r["pdbx_pdb_ins_code"]) == insertion(instance["pdb_ins_code"]) and
                 r["label_entity_id"] == instance["entity_id"] for r in coords),
             "coordinate element or instance numbering differs")
    sites = [r for r in tables["_struct_site"] if r["id"] == side["site_id"]]
    _require(len(sites) == 1, "component site is missing or ambiguous")
    site = sites[0]
    _require((site["pdbx_auth_asym_id"], site["pdbx_auth_comp_id"], site["pdbx_auth_seq_id"]) ==
             (instance["pdb_strand_id"], instance["pdb_mon_id"], instance["pdb_seq_num"]) and
             insertion(site["pdbx_auth_ins_code"]) == insertion(instance["pdb_ins_code"]),
             "site belongs to another component instance")
    members = [r for r in tables["_struct_site_gen"] if r["site_id"] == side["site_id"]]
    _require(len(members) == int(site["pdbx_num_residues"]), "incomplete deposited site membership")
    connections = []
    for row in tables["_struct_conn"]:
        partners = [n for n in (1, 2) if row[f"ptnr{n}_label_asym_id"] == asym and
                    row[f"ptnr{n}_label_comp_id"] == comp]
        if partners:
            _require(len(partners) == 1, "intra-instance connection requires separate treatment")
            n = partners[0]
            _require(row[f"ptnr{n}_label_atom_id"] in coordinate_ids,
                     "connection endpoint lacks selected coordinates")
            connections.append({"instance_partner": n, "source_row": copy.deepcopy(row)})
    return {"selector": copy.deepcopy(side), "dictionary_atoms": atoms,
            "dictionary_bonds": bonds, "instance": instance, "coordinate_atoms": coords,
            "dictionary_only_atom_ids": sorted(set(by_id) - coordinate_ids),
            "site": site, "site_members": members, "external_connections": connections,
            "atoms": by_id, "edges": edges}


def _component_comparisons(declarations: Any, tables: dict) -> list[dict]:
    results = []
    ids = set()
    for declaration in _array(declarations, "component_comparisons", nonempty=True):
        _exact(declaration, {"comparison_id", "left", "right", "atom_map"}, "component comparison")
        identifier = _identifier(declaration["comparison_id"], "comparison_id")
        _require(identifier not in ids, "component comparison IDs repeat")
        ids.add(identifier)
        left, right = [_component_side(declaration[key], tables) for key in ("left", "right")]
        _require(left["selector"]["component_id"] != right["selector"]["component_id"],
                 "stereo comparison requires distinct component dictionaries")
        mapping = _object(declaration["atom_map"], "atom_map")
        _require(set(mapping) == set(left["atoms"]) and
                 len(set(mapping.values())) == len(mapping) and
                 set(mapping.values()) == set(right["atoms"]),
                 "atom map must be a complete dictionary bijection including hydrogen")
        stereo = []
        for a, b in mapping.items():
            l, r = left["atoms"][a], right["atoms"][b]
            ignored = {"comp_id", "atom_id", "pdbx_ordinal", "pdbx_stereo_config"}
            _require({k: v for k, v in l.items() if k not in ignored} ==
                     {k: v for k, v in r.items() if k not in ignored},
                     "mapped component atom properties differ")
            if l["pdbx_stereo_config"] != r["pdbx_stereo_config"]:
                _require({l["pdbx_stereo_config"], r["pdbx_stereo_config"]} == {"R", "S"},
                         "stereochemistry is not an explicit R/S inversion")
                stereo.append({"left_atom_id": a, "right_atom_id": b,
                               "left": l["pdbx_stereo_config"], "right": r["pdbx_stereo_config"]})
        mapped_edges = {tuple(sorted(mapping[a] for a in key)): value
                        for key, value in left["edges"].items()}
        _require(mapped_edges == right["edges"], "mapped component bond graphs differ")
        _require(bool(stereo), "component dictionaries have no explicit stereo inversion")
        # These are literal deposited record comparisons, not normalized
        # environments. Preserve all endpoint, distance, alt, insertion and
        # uncertainty tokens; chemical atom mapping does not map physical sites.
        same_connections = left["external_connections"] == right["external_connections"]
        same_site = left["site"]["id"] == right["site"]["id"]
        same_model = left["selector"]["model_id"] == right["selector"]["model_id"]
        same_members = left["site_members"] == right["site_members"]
        reasons = []
        if not same_site:
            reasons.append("distinct_deposited_site_records")
        if not same_connections:
            reasons.append("different_deposited_external_connection_inventories")
        if not same_model:
            reasons.append("distinct_deposited_models")
        if not same_members:
            reasons.append("different_deposited_site_membership_records")
        for side in (left, right):
            del side["atoms"], side["edges"]
        results.append({"comparison_id": identifier,
            "relation_scope": "deposited_component_dictionary_graph_and_stereo_tokens",
            "atom_map_provenance": "project_declared_and_validated_against_complete_deposited_dictionaries",
            "complete_dictionary_atom_bijection": True, "mapped_bond_graph_equal": True,
            "atom_map": copy.deepcopy(mapping), "stereo_inversions": stereo,
            "unchanged_stereocenters": [a for a, b in mapping.items()
                if next(r for r in left["dictionary_atoms"] if r["atom_id"] == a)["pdbx_stereo_config"] in {"R", "S"}
                and a not in {r["left_atom_id"] for r in stereo}],
            "left": left, "right": right,
            "same_deposited_environment_comparison": {"status": "refused" if reasons else "not_established",
                "same_site_record": same_site, "same_external_connection_inventory": same_connections,
                "same_model": same_model, "physical_site_equivalence": "not_established",
                "same_site_membership_records": same_members,
                "refusal_reasons": reasons,
                "scope": "Exact source-token comparisons in one deposit only; even matching records do not establish physical site, state or geometry equivalence."},
            "not_established": ["Coordinate-derived absolute stereochemistry or observed ligand hydrogen positions",
                "Bound protonation, enantiopurity, a physical atom map or an observed reaction trajectory",
                "Equivalent catalytic geometry, reacting solution state, assay preparation or measured function"]})
    return results


def _reaction_state_comparisons(declarations: Any, tables: dict, repo_root: Path) -> list[dict]:
    """Join reviewed depiction locators to dictionary instances without normalization.

    Explicit source H must be mapped, but omitted/implicit H is never invented.
    This diagnostic deliberately cannot establish full chemical-state identity.
    """
    results = []
    for declaration in _array(declarations, "reaction_state_comparisons", nonempty=True):
        _exact(declaration, {"comparison_id", "source", "component", "map_alternatives"},
               "reaction-state comparison")
        identifier = _identifier(declaration["comparison_id"], "comparison_id")
        source = _exact(declaration["source"],
                        {"binding", "transformation_id", "state", "atom_ids"}, "reaction source")
        binding, path = _safe_bound_path(source["binding"], repo_root=repo_root)
        payload = json.loads(path.read_text(encoding="utf-8"))
        review = payload.get("review", {})
        _require(review.get("status") == "accepted" and
                 review.get("reviewed_payload_sha256") == transformation_payload_sha256(payload),
                 "reaction source is not a reviewed transformation payload")
        for source_binding in payload["source_bindings"]:
            _safe_bound_path({k: source_binding[k] for k in ("path", "sha256")},
                             repo_root=repo_root, label="transformation dependency")
        matches = [r for r in payload.get("transformations", [])
                   if r.get("transformation_id") == source["transformation_id"]]
        _require(len(matches) == 1, "reaction transformation is missing or ambiguous")
        item = matches[0]
        _require(source["state"] in {"before", "after"}, "reaction state must be before or after")
        graph = _validate_graph(item["panel_correspondence"][source["state"] + "_graph"], "reaction graph")
        selected = _array(source["atom_ids"], "reaction atom_ids", nonempty=True)
        atoms = {a["atom_id"]: a for a in graph["atoms"]}
        _require(all(isinstance(a, str) for a in selected) and len(set(selected)) == len(selected)
                 and set(selected) <= set(atoms), "reaction atom selection is invalid")
        selected = set(selected)
        # Require exactly one complete depicted covalent component, not a
        # convenient crop that drops a substituent or explicit proton.
        reached = {next(iter(selected))}
        while True:
            expanded = reached | {a for b in graph["bonds"] if reached & set(b["atom_ids"])
                                  for a in b["atom_ids"]}
            if expanded == reached:
                break
            reached = expanded
        _require(reached == selected, "reaction selection must be one complete covalent component")
        atoms = {a: atoms[a] for a in sorted(selected)}
        bonds = [b for b in graph["bonds"] if set(b["atom_ids"]) <= selected]
        component = _component_side(declaration["component"], tables)
        alternatives = []
        map_ids, seen_maps = set(), set()
        for alternative in _array(declaration["map_alternatives"], "map_alternatives", nonempty=True):
            _exact(alternative, {"map_id", "atom_map"}, "reaction map alternative")
            map_id = _identifier(alternative["map_id"], "map_id")
            mapping = _object(alternative["atom_map"], "atom_map")
            _require(all(isinstance(a, str) and isinstance(b, str) for a, b in mapping.items()),
                     "reaction atom map must contain string locators")
            signature = tuple(sorted(mapping.items()))
            _require(map_id not in map_ids and signature not in seen_maps, "reaction maps repeat")
            map_ids.add(map_id)
            seen_maps.add(signature)
            _require(set(mapping) == selected and len(set(mapping.values())) == len(mapping)
                     and set(mapping.values()) <= set(component["atoms"]),
                     "reaction map must cover every selected source node including explicit H")
            unmapped = set(component["atoms"]) - set(mapping.values())
            _require(all(component["atoms"][a]["type_symbol"] == "H" for a in unmapped),
                     "reaction map must cover all dictionary heavy atoms")
            _require(all(a["element"] == component["atoms"][mapping[k]]["type_symbol"]
                         for k, a in atoms.items()), "mapped reaction elements differ")
            mapped_edges = {tuple(sorted(mapping[a] for a in b["atom_ids"])): b for b in bonds}
            target_edges = {edge: row for edge, row in component["edges"].items()
                            if set(edge) <= set(mapping.values())}
            _require(set(mapped_edges) == set(target_edges), "mapped reaction topology differs")
            order_differences = [{"source_atom_ids": mapped_edges[e]["atom_ids"],
                "dictionary_atom_ids": list(e), "source_order": mapped_edges[e]["order"],
                "dictionary_order": target_edges[e]["value_order"],
                "dictionary_aromatic_flag": target_edges[e]["pdbx_aromatic_flag"]}
                for e in sorted(mapped_edges)
                if {1: "sing", 2: "doub", 3: "trip"}[mapped_edges[e]["order"]]
                   != target_edges[e]["value_order"]]
            _require(all(d["dictionary_aromatic_flag"] == "Y" for d in order_differences),
                     "mapped non-aromatic bond orders differ; this locator comparison cannot equate them")
            properties = []
            for atom_id, atom in atoms.items():
                target = component["atoms"][mapping[atom_id]]
                charge = target.get("charge")
                charge_known = charge not in {None, "?", "."}
                _require(not charge_known or re.fullmatch(r"[+-]?\d+", charge) is not None,
                         "dictionary charge is malformed")
                properties.append({"source_atom_id": atom_id, "dictionary_atom_id": mapping[atom_id],
                    "source_formal_charge": atom["formal_charge"], "dictionary_charge_token": charge,
                    "formal_charge_equal": atom["formal_charge"] == int(charge) if charge_known else None,
                    "source_stereochemistry": atom["stereochemistry"],
                    "dictionary_stereochemistry": target["pdbx_stereo_config"],
                    "assigned_stereochemistry_token_equal": atom["stereochemistry"] == target["pdbx_stereo_config"]
                        if atom["stereochemistry"] in {"R", "S"} and target["pdbx_stereo_config"] in {"R", "S"} else None})
            alternatives.append({"map_id": map_id, "atom_map": copy.deepcopy(mapping),
                "mapped_element_and_topology_equal": True,
                "complete_dictionary_atom_bijection": not unmapped,
                "literal_mapped_bond_orders_equal": not order_differences,
                "bond_order_differences": order_differences, "atom_property_comparisons": properties,
                "unmapped_dictionary_atom_ids": sorted(unmapped),
                "unmapped_dictionary_bonds": [r for r in component["dictionary_bonds"]
                    if {r["atom_id_1"], r["atom_id_2"]} & unmapped]})
        canonical = item.get("canonical_input_correspondence") if source["state"] == "before" else None
        if canonical is not None:
            canonical_maps = [{r["canonical_atom_id"]: r["before_atom_id"]
                               for r in alt["canonical_to_before"]}
                              for alt in canonical["map_alternatives"]]
            heavy = {a for a, row in atoms.items() if row["element"] != "H"}
            canonical_range = set(canonical_maps[0].values())
            _require(all(set(m.values()) == canonical_range for m in canonical_maps)
                     and heavy <= canonical_range <= selected,
                     "selected component does not cover the canonical participant")
            baseline = alternatives[0]["atom_map"]
            expected = set()
            for canonical_map in canonical_maps:
                composed = {canonical_map[c]: baseline[canonical_maps[0][c]]
                            for c in canonical_maps[0]}
                composed.update({a: baseline[a] for a in selected - canonical_range})
                expected.add(tuple(sorted(composed.items())))
            _require(seen_maps == expected and len(alternatives) == canonical["remote_symmetry"]["full_map_count"],
                     "reaction maps must preserve every reviewed canonical symmetry alternative")
        del component["atoms"], component["edges"]
        results.append({"comparison_id": identifier,
            "relation_scope": "reviewed_source_depiction_to_deposited_dictionary_locators",
            "source": {"binding": binding, "transformation_id": item["transformation_id"],
                "state": source["state"], "state_binding": item["state_pair"][source["state"]],
                "record_binding": item["record_binding"], "proposal_binding": item["proposal_binding"],
                "canonical_reaction_binding": item.get("canonical_reaction_binding"),
                "canonical_input_correspondence": item.get("canonical_input_correspondence")
                    if source["state"] == "before" else None,
                "source_bindings": payload["source_bindings"],
                "graph": {"source_graph_id": graph["graph_id"],
                    "selection_scope": "one_complete_depicted_covalent_component",
                    "atom_id_scope": graph["atom_id_scope"], "atoms": list(atoms.values()), "bonds": bonds},
                "representation_boundaries": item["panel_correspondence"]["representation_boundaries"],
                "stereochemistry_review": item["panel_correspondence"].get("stereochemistry"),
                "mandatory_abstentions": item["mandatory_abstentions"]},
            "component": component, "map_alternatives": alternatives,
            "canonical_symmetry_alternatives_preserved": True if canonical is not None else None,
            "identity_request": {"status": "refused", "chemical_state_identity": "not_established",
                "reason": "Depiction topology and selected stereo tokens cannot establish full chemical state; implicit H, source aromaticity and complete stereochemistry are not compared, and missing dictionary charge remains unknown.",
                "hydrogen_scope": "All explicit source H retained; unmatched dictionary H are not evidence that source implicit H are absent.",
                "stereochemistry_scope": "Only reviewed source atom R/S symbols are compared to dictionary atom R/S symbols; raw source wedges and dictionary bond-stereo conventions are not compared.",
                "physical_atom_map": False, "productive_geometry_transfer": False}})
    return results


def build_deposit_context(
    spec: dict[str, Any], *, source_path: Path, repo_root: Path | None = None
) -> dict[str, Any]:
    """Build one deterministic deposit context from a validated bound source."""

    required = set(_SPEC_FIELDS)
    allowed = required | {"assembly_spec", "component_comparisons", "reaction_state_comparisons"}
    top = _object(spec, "deposit-context spec")
    _require(
        required <= set(top) <= allowed,
        "deposit-context spec fields differ; "
        f"missing={sorted(required - set(top))}, extra={sorted(set(top) - allowed)}",
    )
    _require(
        top["schema_version"] == SPEC_SCHEMA_VERSION,
        "unsupported deposit-context spec",
    )
    packet_id = _identifier(top["packet_id"], "packet_id")
    binding = _exact(top["source_binding"], _SOURCE_BINDING_FIELDS, "source_binding")
    _require(
        canonical_file_sha256(source_path) == binding["sha256"],
        "source binding hash differs",
    )
    try:
        cif_text = (gzip.decompress(source_path.read_bytes()).decode("utf-8", errors="strict")
                    if source_path.suffix == ".gz" else
                    source_path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError) as exc:
        raise ValueError("deposit source is not readable UTF-8 mmCIF") from exc
    tables = parse_mmcif_categories(cif_text)
    rows, row_ids = _row_projections(top["row_selections"], tables=tables)
    assembly, assembly_ids = _assembly_projection(top, cif_text=cif_text)
    overlap = row_ids & assembly_ids
    _require(
        not overlap,
        f"selection IDs repeat across row and assembly declarations: {sorted(overlap)}",
    )
    reaction_comparisons = None
    comparison_ids = set()
    if "reaction_state_comparisons" in top:
        _require(repo_root is not None, "reaction comparisons require an explicit repository root")
        reaction_comparisons = _reaction_state_comparisons(top["reaction_state_comparisons"], tables, repo_root.resolve())
        comparison_ids = {r["comparison_id"] for r in reaction_comparisons}
        _require(len(comparison_ids) == len(reaction_comparisons) and
                 not comparison_ids & (row_ids | assembly_ids |
                    {r["comparison_id"] for r in top.get("component_comparisons", [])}),
                 "reaction comparison IDs repeat or collide")
    interpretation = _interpretation(
        top["interpretation"], declared_ids=row_ids | assembly_ids | comparison_ids
    )
    bundle = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "packet_id": packet_id,
        "spec_payload_sha256": hashlib.sha256(canonical_json_bytes(top)).hexdigest(),
        "source_binding": copy.deepcopy(binding),
        "row_selection_count": len(rows),
        "selected_row_count": sum(len(row["rows"]) for row in rows),
        "row_selections": rows,
        "assembly_projection": assembly,
        "interpretation": interpretation,
        "claim_boundary": {
            "source_rows": (
                "parsed values from hash-bound mmCIF rows selected by declared "
                "string equality and count"
            ),
            "coordinate_geometry": (
                "declared assembly atoms and Euclidean distances; no bond or joint-state inference"
                if assembly is not None
                else "not projected"
            ),
            "interpretation": (
                "explicitly supplied project statements requiring source review; "
                "not semantically validated or inferred by runtime"
            ),
            "does_not_establish": [
                "chemical normalization or ligand equivalence",
                "reaction, mechanism, source-step, or catalytic-role applicability",
                "productive geometry, solution population, rate, or design competence",
            ],
        },
    }
    if "component_comparisons" in top:
        bundle["component_comparisons"] = _component_comparisons(top["component_comparisons"], tables)
    if reaction_comparisons is not None:
        bundle["reaction_state_comparisons"] = reaction_comparisons
    canonical_json_bytes(bundle)
    return bundle


def _packet_path(packet: Path, *, repo_root: Path) -> Path:
    candidate = packet if packet.is_absolute() else repo_root / packet
    result = candidate.resolve()
    _require(
        repo_root in result.parents and result.is_dir(),
        "deposit-context packet is missing or outside the repository",
    )
    return result


def load_and_build_deposit_context(
    packet: Path, repo_root: Path
) -> dict[str, Any]:
    """Load a repository packet and build its deterministic projection."""

    root = repo_root.resolve()
    _require(root.is_dir(), "repo_root is not a directory")
    packet_path = _packet_path(Path(packet), repo_root=root)
    spec_path = packet_path / "spec.json"
    _require(spec_path.is_file(), "deposit-context spec.json is missing")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    binding, source_path = _safe_bound_path(
        _object(spec, "deposit-context spec").get("source_binding"),
        repo_root=root,
    )
    result = build_deposit_context(spec, source_path=source_path, repo_root=root)
    _require(result["source_binding"] == binding, "source binding changed during build")
    return result


def check_deposit_context(packet: Path, repo_root: Path) -> dict[str, Any]:
    """Rebuild a packet and require exact projection and source-review pins."""

    root = repo_root.resolve()
    packet_path = _packet_path(Path(packet), repo_root=root)
    result = load_and_build_deposit_context(packet_path, root)
    projection_path = packet_path / "projection.json"
    review_path = packet_path / "review.json"
    _require(projection_path.is_file(), "deposit-context projection.json is missing")
    _require(review_path.is_file(), "deposit-context review.json is missing")
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    _require(projection == result, "deposit-context projection is stale")
    review = _object(
        json.loads(review_path.read_text(encoding="utf-8")),
        "deposit-context review",
    )
    _require(
        review.get("schema_version") == REVIEW_SCHEMA_VERSION,
        "deposit-context review schema differs",
    )
    _require(
        review.get("decision") == REVIEW_DECISION,
        "deposit-context review decision differs",
    )
    source_path = _safe_bound_path(
        json.loads((packet_path / "spec.json").read_text(encoding="utf-8"))[
            "source_binding"
        ],
        repo_root=root,
    )[1]
    expected_pins = {
        "spec.json": canonical_file_sha256(packet_path / "spec.json"),
        "projection.json": canonical_file_sha256(projection_path),
        "source": canonical_file_sha256(source_path),
    }
    _require(
        review.get("reviewed_sha256") == expected_pins,
        "deposit-context source-review pins are stale",
    )
    return result
