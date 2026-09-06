"""Query separate source batches without manufacturing a combined source bundle."""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from typing import Any

from .atlas_draft_query import query_source_drafts


def query_source_draft_batches(
    bundles: Mapping[str, dict[str, Any]], *,
    primary_evidence_by_batch: Mapping[str, dict[str, Any] | None] | None = None,
    mcsa_id: str | None = None, assembly: str | None = None,
    text: str | None = None, include_steps: bool = False,
    participants: Sequence[str] = (), reactants: Sequence[str] = (),
    products: Sequence[str] = (), mechanism_components: Sequence[str] = (),
) -> dict[str, Any]:
    """Apply the same query independently to each named, validated source bundle.

    Every result retains its original selection and review metadata, including
    zero-result batches. Duplicate source records are rejected rather than
    silently merging versions or counting repeated records as new coverage.
    """
    if not isinstance(bundles, Mapping) or not bundles:
        raise ValueError("at least one named source batch is required")
    if any(not isinstance(name, str) or not name for name in bundles):
        raise ValueError("source batch names must be nonempty text")
    evidence = {} if primary_evidence_by_batch is None else primary_evidence_by_batch
    if not isinstance(evidence, Mapping) or set(evidence) - set(bundles):
        raise ValueError("primary evidence names an unselected source batch")

    results = []
    seen_record_ids: set[str] = set()
    seen_mcsa_ids: set[str] = set()
    for batch_id in sorted(bundles):
        bundle = bundles[batch_id]
        expected_id = "atlas50.source-scoped-mechanism-drafts"
        if batch_id != "default":
            expected_id += f".{batch_id}"
        if not isinstance(bundle, dict) or bundle.get("bundle_id") != expected_id:
            raise ValueError("batch name does not match its source bundle identity")
        result = query_source_drafts(
            bundle, mcsa_id=mcsa_id, assembly=assembly, text=text,
            include_steps=include_steps, participants=participants,
            reactants=reactants, products=products,
            mechanism_components=mechanism_components,
            primary_evidence=evidence.get(batch_id),
        )
        # Check the complete validated corpus, not just records that happened
        # to match this query; filters must not hide overlapping source sets.
        for record in bundle["records"]:
            if (record["record_id"] in seen_record_ids
                    or record["mcsa_id"] in seen_mcsa_ids):
                raise ValueError("a source record occurs in multiple selected batches")
            seen_record_ids.add(record["record_id"])
            seen_mcsa_ids.add(record["mcsa_id"])
        results.append({"batch_id": batch_id, "result": result})

    output = {
        "schema_version": "catalytic-earth.source-draft-catalog-query.v1",
        "searched_batch_ids": sorted(bundles),
        "searched_record_count": len(seen_record_ids),
        "record_count": sum(item["result"]["record_count"] for item in results),
        "filters": copy.deepcopy(results[0]["result"]["filters"]),
        "source_steps_included": include_steps,
        "query_semantics": {
            "batch_combination": "independent_queries_with_original_batch_provenance",
            "cross_batch_evidence_join": False,
            "shared_label_implies_mechanism_equivalence": False,
            "empty_result": "no_matching_source_annotation_in_selected_batches",
        },
        "batches": results,
    }
    if mechanism_components:
        output["mechanism_proposal_match_count"] = sum(
            len(record["mechanism_component_matches"])
            for item in results for record in item["result"]["records"]
        )
    return output
