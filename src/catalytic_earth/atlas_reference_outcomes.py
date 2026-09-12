"""Compose reviewed reference fragments and primary outcomes without new observations.

The declarations choose source providers and existing comparisons. This consumer
checks identity correspondence; scientific applicability still requires review.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .atlas_fragment_sites import build_fragment_sites, query_fragment_sites
from .atlas_mechanism_evidence import query_mechanism_evidence
from .atlas_perturbations import SPEC_PATH as PROJECTION_PATH, pointer, project
from .atlas_transformation_sites import _THREE_TO_ONE

SPEC_PATH = "data/atlas/reference_outcomes/spec.json"
REVIEW_PATH = "data/atlas/reference_outcomes/review.json"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError("reference outcome join: " + message)


def _raw(root: Path, relative: str) -> bytes:
    path = (root / relative).resolve()
    _require(path.is_relative_to(root.resolve()), "binding escapes repository")
    return path.read_bytes().replace(b"\r\n", b"\n")


def _bound(root: Path, binding: dict) -> dict:
    raw = _raw(root, binding["path"])
    _require(hashlib.sha256(raw).hexdigest() == binding["sha256"],
             "source binding differs: " + binding["path"])
    return json.loads(raw)


def _index(rows: list[dict], field: str) -> dict:
    indexed = {row[field]: row for row in rows}
    _require(len(indexed) == len(rows), "duplicate " + field)
    return indexed


def _fragment_query(root: Path, context: dict) -> dict:
    bundle = _bound(root, context["fragment_bundle"])
    atlas = _bound(root, context["atlas_bundle"])
    evidence = _bound(root, context["evidence"])
    transformations = {key: _bound(root, value)
                       for key, value in context["transformations"].items()}
    evidence_query = query_mechanism_evidence(
        evidence, atlas10_bundle=atlas, transformation_values=transformations,
    )
    rebuilt = build_fragment_sites(
        bundle["spec"], bundle["review"], lambda path: _raw(root, path),
        atlas10_bundle=atlas, evidence_query=evidence_query,
        transformation_values=transformations,
    )
    _require(rebuilt == bundle, "fragment package differs from reviewed sources")
    return query_fragment_sites(
        bundle, atlas10_bundle=atlas, evidence_query=evidence_query,
        transformation_values=transformations,
    )


def _join(link: dict, fragment: dict, view: dict, sources: dict) -> dict:
    """Join one exact, single-substitution study context; never parse activity prose."""
    primary_id = link["primary_source"]
    primary = sources[primary_id]
    site = pointer(primary, link["site_pointer"])
    study = pointer(primary, link["study_pointer"])
    primary_source = pointer(primary, link["primary_source_pointer"])
    citation = {key: pointer(primary_source, path)
                for key, path in link["citation_pointers"].items()}
    _require(set(citation) == {"PubMed", "DOI"}
             and all(isinstance(value, str) and value for value in citation.values()),
             "exact primary PMID and DOI are required")
    context = fragment.get("reference_annotation_context", {})
    _require(context.get("status") == "source_database_annotation_at_reference_site",
             "reference annotation is unresolved")
    annotation = context["annotation"]
    mapped = context["reference_site_mapping"]["site_record"]
    _require(mapped is not None, "reference site is unresolved")
    position = site["sequence_position"]
    original, alternative = site["reference_residue"], site["alternative_residue"]
    _require(type(position) is int and position > 0
             and original in _THREE_TO_ONE.values()
             and alternative in _THREE_TO_ONE.values() and original != alternative,
             "invalid single-substitution identity")
    variant = f"{original}{position}{alternative}"
    identity = {key: site[key] for key in ("uniprot_id", "reference_site_id",
                "reference_residue", "sequence_position", "alternative_residue")}
    identity.update(variant=variant, study_id=study, **citation)
    _require(identity == link["expected_identity"], "declared identity differs from primary context")
    _require(site["uniprot_id"] == mapped["uniprot_id"] == annotation["uniprot_id"]
             and site["reference_site_id"] == mapped["site_id"] == annotation["site_id"]
             and position == mapped["sequence_position"]
             and original == _THREE_TO_ONE[mapped["residue_name"]],
             "reference accession, residue, position or site differs")
    _require(site["source_binding"] == {key: context["source_binding"][key]
                                       for key in ("path", "sha256")}
             and site["feature_index"] == annotation["feature_index"]
             and site["feature_pointer"] == f"/features/{annotation['feature_index']}",
             "reference snapshot or feature differs")
    feature = annotation["feature"]
    exact = {"value": position, "modifier": "EXACT"}
    _require(feature["type"] == "Mutagenesis"
             and feature["location"] == {"start": exact, "end": exact}
             and feature["alternativeSequence"]["originalSequence"] == original
             and feature["alternativeSequence"]["alternativeSequences"] == [alternative],
             "point-mutagenesis substitution differs")
    _require(site["citation_match"] == citation
             and any(row["source"] == "PubMed" and row["id"] == citation["PubMed"]
                     for row in feature["evidences"]),
             "feature evidence or primary citation differs")
    reference_source = sources["reference_snapshot"]
    reference = pointer(reference_source, site["citation_pointer"])
    _require(type(site["reference_index"]) is int
             and site["citation_pointer"] == f"/references/{site['reference_index']}",
             "reference index differs")
    _require(reference in annotation["cited_reference_metadata"],
             "reference citation was not attached to the feature")
    for key, value in citation.items():
        matches = [row["id"] for row in reference["citation"]["citationCrossReferences"]
                   if row["database"] == key]
        _require(matches == [value], "primary citation is absent, ambiguous or different")

    _require(link["construct_id"] in view["constructs"], "unknown construct")
    construct = view["constructs"][link["construct_id"]]
    _require(construct["perturbation"] == construct["source_record"]["perturbation"] == [variant]
             and construct["provider"]["source"] == primary_id
             and pointer(primary, construct["provider"]["pointer"]) == construct["source_record"],
             "construct perturbation or primary provider differs")
    _require(construct["source_record"]["construct_id"] == construct["source_construct_id"]
             == link["source_construct_id"],
             "source-named construct differs")
    comparisons = _index(view["comparisons"], "id")
    rows = _index(view["observations"], "id")
    ids = link["comparison_ids"]
    _require(bool(ids) and len(ids) == len(set(ids)) and set(ids) <= set(comparisons),
             "comparison selection is empty, repeated or unknown")
    selected_comparisons = [comparisons[key] for key in ids]
    _require(all(row["study_id"] == study for row in selected_comparisons),
             "comparison study differs")
    _require(all(row["operation"] == "unassessed" and row["roles"] == {}
                 and row["source_discriminant_assessed"] is True
                 and row["arithmetic_requested"] is False and row["eligible"] is False
                 and all(row[key] is None for key in ("value", "unit", "uncertainty"))
                 for row in selected_comparisons),
             "selected context is not an assessed no-arithmetic relation")
    observation_ids = {key for row in selected_comparisons
                       for key in [*row["roles"].values(), *row.get("context_observations", [])]}
    _require(bool(observation_ids) and observation_ids <= set(rows),
             "comparison has no bound outcomes")
    declared_ids = link["observation_ids"]
    _require(len(declared_ids) == len(set(declared_ids))
             and set(declared_ids) == observation_ids, "declared outcome membership differs")
    selected = [row for row in view["observations"] if row["id"] in observation_ids]
    _require(all(row["study_id"] == study and row["construct_id"] == link["construct_id"]
                 and row["perturbation"] == [variant] for row in selected),
             "outcome study, construct or perturbation differs")
    used_sources = {row["provider"]["source"] for row in selected}
    _require(used_sources == set(link["outcome_sources"]),
             "outcome source is unbound or unused")
    for source_id, declaration in link["outcome_sources"].items():
        source = sources[source_id]
        _require(pointer(source, declaration["study_pointer"]) == study,
                 "outcome source study differs")
        if source_id != primary_id:
            _require(pointer(source, declaration["primary_binding_pointer"])
                     == view["sources"][primary_id]
                     and pointer(source, declaration["primary_source_pointer"])
                     == link["primary_source_pointer"],
                     "outcome source does not bind the same primary evidence")
            source_context = pointer(source, declaration["construct_context_pointer"])
            _require(source_context["source_binding"] == view["sources"][primary_id]
                     and source_context["pointer"] == construct["provider"]["pointer"],
                     "outcome source construct context differs")
    for row in selected:
        source = sources[row["provider"]["source"]]
        _require(pointer(source, row["provider"]["pointer"]) == row["source_record"]
                 and row["source_record"]["construct_id"] == construct["source_construct_id"],
                 "outcome row differs from its source construct")

    return {
        "id": link["id"], "status": "reference_site_variant_citation_join",
        "reference_site_id": site["reference_site_id"], "variant": variant,
        "study_id": study, "citation_match": citation,
        "fragment_relation": deepcopy(fragment),
        "primary_site_context": deepcopy(site), "construct": deepcopy(construct),
        "matched_observations": deepcopy(selected),
        "comparisons": deepcopy(selected_comparisons),
        "identity_scope": "reference_site_and_source_named_variant_not_exact_assayed_specimen",
        "selected_step_declares_site": context["selected_step_declares_site"],
        "deposited_atom_identity": False, "exact_assayed_construct_identity": False,
        "source_arrow_experimentally_validated": False,
        "primary_outcomes_assign_step_or_atom_role": False,
        "new_arithmetic_performed": False,
    }


def _compose(root: Path, spec: dict, view: dict, site_id: str | None = None) -> dict:
    _require(spec["schema_version"] == "catalytic-earth.reference-outcome-links.v1",
             "unsupported declaration schema")
    _index(spec["links"], "id")
    contexts = {key: _fragment_query(root, value)
                for key, value in spec["fragment_contexts"].items()}
    results = []
    for link in spec["links"]:
        _require(link["fragment_context_id"] in contexts, "unknown fragment context")
        relations = _index(contexts[link["fragment_context_id"]]["relations"], "relation_id")
        _require(link["fragment_relation_id"] in relations, "unknown fragment relation")
        fragment = relations[link["fragment_relation_id"]]
        needed = {link["primary_source"], *link["outcome_sources"]}
        _require(needed <= set(view["sources"]), "unknown primary outcome source")
        sources = {key: _bound(root, view["sources"][key]) for key in needed}
        site = pointer(sources[link["primary_source"]], link["site_pointer"])
        sources["reference_snapshot"] = _bound(root, site["source_binding"])
        joined = _join(link, fragment, view, sources)
        if site_id is None or joined["reference_site_id"] == site_id:
            results.append(joined)
    return {
        "schema_version": "catalytic-earth.reference-outcome-query.v1",
        "scope": spec["scope"], "filters": {"reference_site_id": site_id},
        "matches": results, "relation_count": len(results),
        "empty_match": "no_declared_reviewed_join_not_absence_of_functional_evidence",
        "new_observations": 0, "new_experiments": 0,
        "independent_human_validation": False,
    }


def _acceptance_payload(result: dict, view: dict, projection: dict) -> dict:
    """Bind the unfiltered answer and its selected scientific context, not atlas totals."""
    rows = [row for match in result["matches"] for row in match["matched_observations"]]
    outcome_sources = {row["provider"]["source"] for row in rows}
    source_ids = set(outcome_sources)
    _require(source_ids <= set(projection["evidence_context"]),
             "selected source has no declared scientific context")
    contexts = {key: projection["evidence_context"][key] for key in sorted(source_ids)}
    source_ids.update(ref["source"] for match in result["matches"]
                      for comparison in match["comparisons"] for ref in comparison["evidence"])
    source_ids.update(ref["source"] for refs in contexts.values() for ref in refs)
    return {
        "composition": result,
        "constructs": {key: view["constructs"][key] for key in sorted(
            {row[field] for row in rows for field in ("construct_id", "background_id")})},
        "assays": {key: view["assays"][key] for key in sorted({row["assay_id"] for row in rows})},
        "substrates": {key: view["substrates"][key]
                       for key in sorted({row["substrate_id"] for row in rows})},
        "evidence_context": {key: {"providers": refs, "values": view["evidence_context"][key]}
                             for key, refs in contexts.items()},
        "source_bindings": {key: view["sources"][key] for key in sorted(source_ids)},
        "source_witnesses": [witness for witness in view["source_witnesses"]
                             if any(ref["source"] in outcome_sources for ref in witness["source_bindings"])],
    }


def _acceptance_sha256(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def query_reference_outcomes(root: Path, *, site_id: str | None = None) -> dict:
    """Verify both existing evidence planes, then compose the reviewed declarations."""
    view = project(root)
    review = json.loads(_raw(root, REVIEW_PATH))
    _require(review["status"] == "source_reviewed_computational"
             and review["independent_human_validation"] is False
             and review["experimental_validation"] is False, "review is not accepted")
    required = {SPEC_PATH, "src/catalytic_earth/atlas_reference_outcomes.py",
                "scripts/query_atlas_perturbations.py"}
    _require(required <= set(review["reviewed_bindings"]), "review omits a public consumer")
    for path, digest in review["reviewed_bindings"].items():
        _require(hashlib.sha256(_raw(root, path)).hexdigest() == digest,
                 "review binding differs: " + path)
    try:
        result = _compose(root, json.loads(_raw(root, SPEC_PATH)), view)
        payload = _acceptance_payload(result, view, json.loads(_raw(root, PROJECTION_PATH)))
        for binding in payload["source_bindings"].values():
            _require(review["reviewed_bindings"].get(binding["path"]) == binding["sha256"],
                     "review omits selected source: " + binding["path"])
        _require(_acceptance_sha256(payload) == review.get("accepted_scientific_payload_sha256"),
                 "reviewed scientific composition differs; renewed local review required")
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("reference outcome join: malformed or unbound declaration") from error
    # Even an empty selection must first validate every declared scientific relation.
    if site_id is not None:
        result["matches"] = [match for match in result["matches"]
                             if match["reference_site_id"] == site_id]
    result["filters"]["reference_site_id"] = site_id
    result["relation_count"] = len(result["matches"])
    result["primary_projection_bindings"] = {
        path: hashlib.sha256(_raw(root, path)).hexdigest() for path in
        ("data/atlas/perturbations/projection.json", "data/atlas/perturbations/review.json")
    }
    source_ids = {row["provider"]["source"] for match in result["matches"]
                  for row in match["matched_observations"]}
    result["primary_source_bindings"] = {key: deepcopy(view["sources"][key]) for key in sorted(source_ids)}
    result["source_witnesses"] = [deepcopy(witness) for witness in view["source_witnesses"]
                                  if any(binding["source"] in source_ids
                                         for binding in witness["source_bindings"])]
    result["source_witness_cache_status"] = view["source_witness_cache_status"]
    result["review"] = review
    return result
