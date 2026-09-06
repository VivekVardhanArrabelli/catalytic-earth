"""Query partial source-panel comparisons with their unresolved coverage."""

from __future__ import annotations

import copy
from typing import Any

from .atlas_partial_panels import validate_panel_comparisons
from .atlas_transformation_query import normalize_mcsa_id


def query_panel_comparisons(
    value: dict[str, Any], *, atlas10_bundle: dict[str, Any],
    mcsa_id: str | None = None,
) -> dict[str, Any]:
    summary = validate_panel_comparisons(value, atlas10_bundle=atlas10_bundle)
    mcsa_id = normalize_mcsa_id(mcsa_id)
    selected = [row for row in value["comparisons"]
                if mcsa_id is None or row["record_binding"]["mcsa_id"] == mcsa_id]
    return {
        "schema_version": "catalytic-earth.partial-panel-query.v1",
        "comparison_set_id": value["comparison_set_id"],
        "comparison_payload_sha256": summary["comparison_payload_sha256"],
        "filters": {"mcsa_id": mcsa_id},
        "comparison_count": len(selected),
        "comparisons": copy.deepcopy(selected),
        "review": copy.deepcopy(value["review"]),
        "source_bindings": copy.deepcopy(value["source_bindings"]),
        "query_semantics": {
            "counted_object": "reviewed_partial_source_panel_comparison",
            "count_is_complete_transition_count": False,
            "count_is_complete_mechanism_count": False,
            "unmatched_nodes": "unresolved_correspondence_not_atom_creation_or_deletion",
            "cross_step_composition": "not_asserted",
            "flow_coverage_basis": "declared_proposed_edits_not_exhaustive_chemical_interpretation",
            "source_arrow_endpoint_coverage": "complete",
            "empty_result": "no_matching_reviewed_comparison_not_absence_of_chemistry",
        },
    }
