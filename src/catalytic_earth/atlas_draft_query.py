"""Offline retrieval of source-scoped drafts with their evidence boundaries."""
from __future__ import annotations

import copy
import json
from typing import Any

from .atlas_drafts import validate_source_drafts


def query_source_drafts(
    bundle: dict[str, Any], *, mcsa_id: str | None = None,
    assembly: str | None = None, text: str | None = None,
    include_steps: bool = False,
) -> dict[str, Any]:
    """Filter actual source records; a compact result still retains abstentions."""
    validate_source_drafts(bundle)
    results = []
    for record in bundle["records"]:
        if mcsa_id is not None and record["mcsa_id"].upper() != mcsa_id.upper():
            continue
        if assembly is not None and record["state_context"]["assembly"]["mode"] != assembly:
            continue
        if text is not None and text.casefold() not in json.dumps(
            {key: record[key] for key in (
                "label", "source_scope", "state_context", "reaction_context",
                "mechanism_proposals", "mandatory_abstentions",
            )}, ensure_ascii=False,
        ).casefold():
            continue
        result = copy.deepcopy(record)
        if not include_steps:
            for proposal in result["mechanism_proposals"]:
                steps = proposal.pop("mechanism_steps")
                proposal["source_step_count"] = len(steps)
                proposal["source_electron_flow_count"] = sum(
                    len(step["electron_flows"]) for step in steps
                )
        results.append(result)
    return {
        "schema_version": "catalytic-earth.source-draft-query.v1",
        "bundle_id": bundle["bundle_id"],
        "selection": copy.deepcopy(bundle["selection"]),
        "filters": {"mcsa_id": mcsa_id, "assembly": assembly, "text": text},
        "source_steps_included": include_steps,
        "record_count": len(results),
        "records": results,
        "claim_boundary": bundle["claim_boundary"],
        "review_independence": bundle["review_independence"],
    }
