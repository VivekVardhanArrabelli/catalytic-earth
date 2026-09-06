"""Offline retrieval of source-scoped drafts with their evidence boundaries."""
from __future__ import annotations

import copy
import json
from typing import Any, Sequence

from .atlas_draft_index import match_source_participants
from .atlas_primary_evidence import validate_primary_evidence


def query_source_drafts(
    bundle: dict[str, Any], *, mcsa_id: str | None = None,
    assembly: str | None = None, text: str | None = None,
    include_steps: bool = False,
    participants: Sequence[str] = (), reactants: Sequence[str] = (),
    products: Sequence[str] = (),
    primary_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Intersect record filters and exact source participants, retaining evidence."""
    primary_summary = None
    annotations_by_record: dict[str, list[dict[str, Any]]] = {}
    if primary_evidence is not None:
        primary_summary = validate_primary_evidence(primary_evidence, bundle=bundle)
        for annotation in primary_evidence["annotations"]:
            record_id = annotation["record_binding"]["record_id"]
            annotations_by_record.setdefault(record_id, []).append(annotation)
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
        text_fields: dict[str, Any] = {
            key: record[key] for key in (
                "label", "source_scope", "state_context", "reaction_context",
                "mechanism_proposals", "mandatory_abstentions",
            )
        }
        if primary_evidence is not None:
            text_fields["primary_evidence_annotations"] = annotations_by_record.get(
                record["record_id"], []
            )
        if text is not None and text.casefold() not in json.dumps(
            text_fields, ensure_ascii=False
        ).casefold():
            continue
        result = copy.deepcopy(record)
        result["participant_matches"] = chemical_matches["matches"][record["record_id"]]
        if primary_evidence is not None:
            result["primary_evidence_annotations"] = copy.deepcopy(
                annotations_by_record.get(record["record_id"], [])
            )
        if not include_steps:
            for proposal in result["mechanism_proposals"]:
                steps = proposal.pop("mechanism_steps")
                proposal["source_step_count"] = len(steps)
                proposal["source_electron_flow_count"] = sum(
                    len(step["electron_flows"]) for step in steps
                )
        results.append(result)
    output = {
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
    if primary_evidence is not None:
        review = primary_evidence["review"]
        output["schema_version"] = "catalytic-earth.source-draft-query.v2"
        output["primary_evidence"] = {
            "annotation_set_id": primary_summary["annotation_set_id"],
            "annotation_payload_sha256": primary_summary[
                "annotation_payload_sha256"
            ],
            "review_independence": {
                key: copy.deepcopy(review[key])
                for key in (
                    "reviewer_kind",
                    "same_model_agents",
                    "blind_review",
                    "statistically_independent",
                    "correlated_error_risk",
                    "human_reviewers",
                    "domain_expert_review_claimed",
                )
            },
        }
    return output
