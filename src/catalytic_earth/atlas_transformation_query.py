"""Retrieve reviewed transformations with their complete graph witnesses."""

from __future__ import annotations

import copy
import re
from typing import Any

from .atlas_transformations import validate_transformations


# Explicit reviewed inputs, never a scan of potentially unfinished source folders.
TRANSFORMATION_SETS = {
    "M0187": {"source_directory": "data/atlas/transformations/m0187", "package_prefix": ""},
    "M0173": {"source_directory": "data/atlas/transformations/m0173", "package_prefix": "m0173_"},
}


def normalize_mcsa_id(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"M[0-9]{4}", value.strip().upper()):
        raise ValueError("mcsa_id must be an exact M-CSA identifier such as M0187")
    return value.strip().upper()


def query_transformations(
    value: dict[str, Any], *, atlas10_bundle: dict[str, Any],
    mcsa_id: str | None = None,
) -> dict[str, Any]:
    summary = validate_transformations(value, atlas10_bundle=atlas10_bundle)
    mcsa_id = normalize_mcsa_id(mcsa_id)
    selected = [row for row in value["transformations"]
                if mcsa_id is None or row["record_binding"]["mcsa_id"] == mcsa_id]
    source_only = value["schema_version"] == "catalytic-earth.transformations.v2"
    return {
        "schema_version": "catalytic-earth.transformation-query.v2" if source_only else "catalytic-earth.transformation-query.v1",
        "transformation_set_id": summary["transformation_set_id"],
        "transformation_payload_sha256": summary["transformation_payload_sha256"],
        "filters": {"mcsa_id": mcsa_id},
        "transformation_count": len(selected),
        "transformations": copy.deepcopy(selected),
        "review": copy.deepcopy(value["review"]),
        "source_bindings": copy.deepcopy(value["source_bindings"]),
        "query_semantics": {
            "counted_object": "reviewed_depicted_state_transition",
            "correspondence_kind": "project_reviewed_panel_locator_alignment" if source_only else "project_computed_graph_correspondence",
            "count_is_complete_mechanism_count": False,
            "empty_result": "no_matching_reviewed_transition_not_absence_of_chemistry",
        },
    }


def query_transformation_sets(
    values: dict[str, dict[str, Any]], *, atlas10_bundle: dict[str, Any],
    mcsa_id: str | None = None,
) -> dict[str, Any]:
    """Query separate reviewed sets without merging their evidence or review pins."""
    if not isinstance(values, dict) or not values:
        raise ValueError("at least one transformation set is required")
    if any(not isinstance(key, str) or key not in TRANSFORMATION_SETS for key in values):
        raise ValueError("unknown transformation set")
    mcsa_id = normalize_mcsa_id(mcsa_id)
    results = []
    seen_ids: set[str] = set()
    for key in sorted(values):
        value = values[key]
        result = query_transformations(value, atlas10_bundle=atlas10_bundle, mcsa_id=mcsa_id)
        for row in value["transformations"]:
            if row["record_binding"]["mcsa_id"] != key:
                raise ValueError("transformation set key does not match its source record")
            if row["transformation_id"] in seen_ids:
                raise ValueError("a transformation occurs in multiple selected sets")
            seen_ids.add(row["transformation_id"])
        results.append({"mcsa_id": key, "result": result})
    return {
        "schema_version": "catalytic-earth.transformation-catalog-query.v1",
        "searched_set_ids": [item["result"]["transformation_set_id"] for item in results],
        "searched_transformation_count": len(seen_ids),
        "transformation_count": sum(item["result"]["transformation_count"] for item in results),
        "filters": {"mcsa_id": mcsa_id},
        "sets": results,
        "query_semantics": {
            "set_combination": "independent_queries_with_original_review_and_source_provenance",
            "cross_set_evidence_join": False,
            "count_is_complete_mechanism_count": False,
            "empty_result": "no_matching_reviewed_transition_not_absence_of_chemistry",
        },
    }
