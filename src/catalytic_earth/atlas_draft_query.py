"""Offline retrieval of source-scoped drafts with their evidence boundaries."""
from __future__ import annotations

import copy
import json
from typing import Any, Sequence

from .atlas_draft_index import match_source_participants


def query_source_drafts(
    bundle: dict[str, Any], *, mcsa_id: str | None = None,
    assembly: str | None = None, text: str | None = None,
    include_steps: bool = False,
    participants: Sequence[str] = (), reactants: Sequence[str] = (),
    products: Sequence[str] = (),
) -> dict[str, Any]:
    """Intersect record filters and exact source participants, retaining evidence."""
    chemical_matches = match_source_participants(
        bundle, participants=participants, reactants=reactants, products=products,
    )
    results = []
    for record in bundle["records"]:
        if record["record_id"] not in chemical_matches["matches"]:
            continue
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
        result["participant_matches"] = chemical_matches["matches"][record["record_id"]]
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
        "filters": {
            "mcsa_id": mcsa_id, "assembly": assembly, "text": text,
            **chemical_matches["filters"],
        },
        "query_semantics": {
            "participant_match_scope": "source_record_reaction_context",
            "filter_combination": "all_clauses_within_one_record",
            "chemical_identity": "exact_source_chebi_identifier_without_ontology_expansion",
            "side": "left_or_right_in_the_source_drawing_not_physiological_direction",
            "proposal_applicability": "record_context_does_not_ground_each_proposal_or_step",
            "shared_participant_implies_reaction_equivalence": False,
        },
        "source_steps_included": include_steps,
        "record_count": len(results),
        "records": results,
        "claim_boundary": bundle["claim_boundary"],
        "review_independence": bundle["review_independence"],
    }
