"""Offline retrieval of source-scoped drafts with their evidence boundaries."""
from __future__ import annotations

import copy
import json
from collections.abc import Sequence
from typing import Any

from .atlas_draft_index import (
    match_source_mechanism_components,
    match_source_participants,
)
from .atlas_primary_evidence import validate_primary_evidence
from .atlas_step_evidence import match_step_evidence, normalize_step_filters


def normalize_observed_state_filters(
    *, observed_states: Sequence[str] = (), observed_components: Sequence[str] = (),
) -> dict[str, list[str]]:
    """Normalize explicit typed context filters without inferring chemistry."""
    from .atlas_primary_evidence import PRIMARY_OBSERVED_STATE_KINDS

    normalized = {}
    for name, values in (
        ("observed_states", observed_states), ("observed_components", observed_components),
    ):
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise ValueError(f"{name} must be an array of nonempty strings")
        labels = []
        for value in values:
            if not isinstance(value, str) or not value.strip() or "," in value:
                raise ValueError(f"{name} requires one nonempty label per clause")
            label = value.strip().casefold()
            if name == "observed_states" and label not in PRIMARY_OBSERVED_STATE_KINDS:
                raise ValueError(f"unknown observed state kind: {value}")
            labels.append(label)
        normalized[name] = sorted(set(labels))
    return normalized


def query_source_drafts(
    bundle: dict[str, Any], *, mcsa_id: str | None = None,
    assembly: str | None = None, text: str | None = None,
    include_steps: bool = False,
    participants: Sequence[str] = (), reactants: Sequence[str] = (),
    products: Sequence[str] = (),
    mechanism_components: Sequence[str] = (),
    primary_evidence: dict[str, Any] | None = None,
    step_evidence: dict[str, Any] | None = None,
    cofactors: Sequence[str] = (), enzyme_contexts: Sequence[str] = (),
    source_assertions: Sequence[str] = (),
    include_observed_state_context: bool = False,
    observed_states: Sequence[str] = (), observed_components: Sequence[str] = (),
) -> dict[str, Any]:
    """Intersect record filters and exact source witnesses, retaining evidence."""
    primary_summary = None
    annotations_by_record: dict[str, list[dict[str, Any]]] = {}
    if primary_evidence is not None:
        primary_summary = validate_primary_evidence(primary_evidence, bundle=bundle)
        for annotation in primary_evidence["annotations"]:
            record_id = annotation["record_binding"]["record_id"]
            annotations_by_record.setdefault(record_id, []).append(annotation)
    observed_filters = normalize_observed_state_filters(
        observed_states=observed_states, observed_components=observed_components,
    )
    if not isinstance(include_observed_state_context, bool):
        raise ValueError("include_observed_state_context must be a boolean")
    observed_filter_used = any(observed_filters.values())
    use_observed_context = include_observed_state_context or observed_filter_used
    observed_by_record = {}
    for record_id, annotations in annotations_by_record.items():
        observed_by_record[record_id] = [
            annotation for annotation in annotations
            if annotation["annotation_kind"] == "primary_observed_state_context"
            and all(label == annotation["claim"]["observed_entity"]["state_kind"].casefold()
                    for label in observed_filters["observed_states"])
            and all(label == annotation["claim"]["observed_entity"]["source_component_id"].casefold()
                    for label in observed_filters["observed_components"])
        ]
    chemical_matches = match_source_participants(
        bundle, participants=participants, reactants=reactants, products=products,
    )
    component_matches = match_source_mechanism_components(
        bundle, components=mechanism_components,
    )
    component_filter_used = bool(component_matches["filters"]["mechanism_components"])
    step_filters = normalize_step_filters(
        cofactors=cofactors, enzyme_contexts=enzyme_contexts,
        source_assertions=source_assertions,
    )
    step_filter_used = any(step_filters.values())
    step_matches = None
    if step_evidence is not None:
        step_matches = match_step_evidence(
            step_evidence, bundle=bundle,
            primary_evidence=(
                primary_evidence if step_evidence.get("primary_evidence_binding") is not None
                else None
            ),
            **step_filters,
        )
    results = []
    for record in bundle["records"]:
        if record["record_id"] not in chemical_matches["matches"]:
            continue
        if record["record_id"] not in component_matches["matches"]:
            continue
        if mcsa_id is not None and record["mcsa_id"].upper() != mcsa_id.upper():
            continue
        if assembly is not None and record["state_context"]["assembly"]["mode"] != assembly:
            continue
        record_observed_contexts = observed_by_record.get(record["record_id"], [])
        if observed_filter_used and not record_observed_contexts:
            continue
        record_step_matches = [] if step_matches is None else copy.deepcopy(
            step_matches["matches"].get(record["record_id"], [])
        )
        if component_filter_used and record_step_matches:
            proposal_ids = {
                item["proposal_id"] for item in component_matches["matches"][record["record_id"]]
            }
            record_step_matches = [
                item for item in record_step_matches
                if item["step_binding"]["proposal_id"] in proposal_ids
            ]
        if step_filter_used and not record_step_matches:
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
        if step_evidence is not None:
            text_fields["step_evidence_annotations"] = record_step_matches
        if text is not None and text.casefold() not in json.dumps(
            text_fields, ensure_ascii=False
        ).casefold():
            continue
        result = copy.deepcopy(record)
        result["participant_matches"] = chemical_matches["matches"][record["record_id"]]
        if component_filter_used:
            result["mechanism_component_matches"] = copy.deepcopy(
                component_matches["matches"][record["record_id"]]
            )
            if step_filter_used:
                matched_proposals = {
                    item["step_binding"]["proposal_id"] for item in record_step_matches
                }
                result["mechanism_component_matches"] = [
                    item for item in result["mechanism_component_matches"]
                    if item["proposal_id"] in matched_proposals
                ]
        if primary_evidence is not None:
            result["primary_evidence_annotations"] = copy.deepcopy(
                annotations_by_record.get(record["record_id"], [])
            )
        if use_observed_context:
            result["observed_state_contexts"] = copy.deepcopy(record_observed_contexts)
        if step_evidence is not None:
            result["step_evidence_annotations"] = record_step_matches
            # Keep the complete source wording in compact results as well.
            # Selected role fragments cannot carry every qualification in a
            # step, and proposal context must stay distinguishable from it.
            bindings = {item["step_binding"]["step_id"]: item["step_binding"]
                        for item in record_step_matches}
            witnessed_proposals = []
            witnessed_steps = []
            for proposal in record["mechanism_proposals"]:
                matched = [step for step in proposal["mechanism_steps"]
                           if step["step_id"] in bindings]
                if matched:
                    witnessed_proposals.append({
                        "proposal_id": proposal["proposal_id"],
                        "source_mechanism_id": proposal["source_mechanism_id"],
                        "source_mechanism_text": proposal["mechanism_text"],
                    })
                    witnessed_steps.extend({
                        "step_binding": copy.deepcopy(bindings[step["step_id"]]),
                        "source_step_summary": step["summary"],
                    } for step in matched)
            result["step_evidence_source_context"] = {
                "proposals": witnessed_proposals, "steps": witnessed_steps,
            }
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
    if component_filter_used:
        output["schema_version"] = "catalytic-earth.source-draft-query.v3"
        output["filters"].update(component_matches["filters"])
        output["query_semantics"].update(
            {
                "mechanism_component_match_scope": (
                    "all_requested_exact_source_labels_within_one_proposal"
                ),
                "mechanism_component_normalization": "trim_and_casefold_only",
                "mechanism_component_step_localization": "not_established",
                "mechanism_component_implies_conserved_function": False,
                "mechanism_component_implies_exact_reaction": False,
                "participant_match_grounds_matching_proposal": False,
            }
        )
    if step_evidence is not None or step_filter_used:
        output["schema_version"] = "catalytic-earth.source-draft-query.v4"
        output["filters"].update(step_filters)
        output["step_evidence"] = None if step_evidence is None else {
            "annotation_set_id": step_evidence["annotation_set_id"],
            "annotation_payload_sha256": step_evidence["review"]["annotation_payload_sha256"],
            "review": copy.deepcopy(step_evidence["review"]),
        }
        output["step_evidence_match_count"] = sum(
            len(record.get("step_evidence_annotations", [])) for record in results
        )
        output["query_semantics"].update({
            "step_context_match_scope": "all_step_filters_within_one_annotation_for_one_source_step",
            "step_and_component_match_scope": "same_source_proposal",
            "cofactor_identity": "exact_source_step_label_not_normalized_chemical_state",
            "primary_context_join": "linked_annotation_retains_its_original_scope",
            "source_silent_implies_observed": False,
            "participant_match_grounds_matching_step": False,
            "compact_step_context": "full_step_summaries_and_separate_proposal_text_without_arrows",
            "empty_step_result": "no_matching_reviewed_step_annotation_not_absence_of_chemistry",
        })
    if use_observed_context:
        output["schema_version"] = "catalytic-earth.source-draft-query.v5"
        if primary_evidence is not None:
            # Resolve excerpt and evidence binding IDs offline, including the
            # distinction between captured bytes and a scoped article projection.
            output["primary_evidence"]["source_bindings"] = copy.deepcopy(
                primary_evidence["source_bindings"]
            )
        output["filters"].update(observed_filters)
        output["observed_state_context_count"] = sum(
            len(record["observed_state_contexts"]) for record in results
        )
        output["query_semantics"].update({
            "observed_state_match_scope": "all_observed_state_filters_within_one_typed_record_annotation",
            "observed_component_identity": "exact_deposited_component_label_trim_and_casefold_only",
            "observed_state_and_step_join": "same_record_context_only",
            "observed_state_grounds_step": False,
            "observed_state_context_count_is_independent_observation_count": False,
            "legacy_primary_annotation_state_classification": "not_inferred",
            "empty_observed_state_result": "no_matching_reviewed_typed_annotation_not_absence_of_observation",
        })
    return output
