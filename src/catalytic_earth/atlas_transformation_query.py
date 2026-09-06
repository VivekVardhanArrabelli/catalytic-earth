"""Retrieve reviewed transformations with their complete graph witnesses."""

from __future__ import annotations

import copy
import re
from typing import Any

from .atlas_transformations import validate_transformations


def query_transformations(
    value: dict[str, Any], *, atlas10_bundle: dict[str, Any],
    mcsa_id: str | None = None,
) -> dict[str, Any]:
    summary = validate_transformations(value, atlas10_bundle=atlas10_bundle)
    if mcsa_id is not None:
        if not isinstance(mcsa_id, str) or not re.fullmatch(r"M[0-9]{4}", mcsa_id.strip().upper()):
            raise ValueError("mcsa_id must be an exact M-CSA identifier such as M0187")
        mcsa_id = mcsa_id.strip().upper()
    selected = [row for row in value["transformations"]
                if mcsa_id is None or row["record_binding"]["mcsa_id"] == mcsa_id]
    return {
        "schema_version": "catalytic-earth.transformation-query.v1",
        "transformation_set_id": summary["transformation_set_id"],
        "transformation_payload_sha256": summary["transformation_payload_sha256"],
        "filters": {"mcsa_id": mcsa_id},
        "transformation_count": len(selected),
        "transformations": copy.deepcopy(selected),
        "review": copy.deepcopy(value["review"]),
        "source_bindings": copy.deepcopy(value["source_bindings"]),
        "query_semantics": {
            "counted_object": "reviewed_depicted_state_transition",
            "correspondence_kind": "project_computed_graph_correspondence",
            "count_is_complete_mechanism_count": False,
            "empty_result": "no_matching_reviewed_transition_not_absence_of_chemistry",
        },
    }
