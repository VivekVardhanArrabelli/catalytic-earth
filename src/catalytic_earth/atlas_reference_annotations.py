"""Reference-site database features beside, rather than promoted into, observations."""
from __future__ import annotations

import copy
import hashlib
import json

from .atlas_transformation_sites import _require, _resolve_labeled_site, _THREE_TO_ONE


def reference_mutagenesis_context(
    *, record: dict, step: dict, label: dict, mcsa_id: str,
    binding: dict, snapshot_utf8: str, feature_index: int,
) -> dict:
    """Resolve one reviewed point-substitution feature at whole-record scope.

    Source prose remains opaque. Citation metadata or an evidence code alone cannot supply an
    assayed construct, endpoint, denominator, numeric parameter or step role.
    """
    raw = snapshot_utf8.encode("utf-8")
    _require(hashlib.sha256(raw).hexdigest() == binding["sha256"],
             "reference annotation source hash differs")
    source = json.loads(raw)
    accession = binding["uniprot_id"]
    _require(source.get("primaryAccession") == accession
             and binding["source_id"] == f"UniProtKB:{accession}",
             "reference annotation source identity differs")
    evidence = [row for row in record["evidence"]
                if row.get("evidence_id") == f"source:UniProtKB:{accession}"]
    _require(len(evidence) == 1
             and evidence[0].get("source_id") == "UniProtKB"
             and evidence[0].get("source_record_id") == accession
             and evidence[0].get("evidence_role") == "protein_identity"
             and evidence[0].get("applicability") == "direct"
             and evidence[0].get("retrieval_status") == "bundled_snapshot"
             and evidence[0].get("snapshot_sha256") == binding["sha256"],
             "reference annotation differs from the bound protein evidence")
    site, protein = _resolve_labeled_site(
        record, step, label, mcsa_id, site_scope="record",
        allowed_label_status="unique_source_fragment_alias",
        match_basis="unique_fragment_mrv_alias_plus_record_site_plus_direct_pdb_author_residue",
    )
    result = {
        "status": "not_resolved", "source_binding": copy.deepcopy(binding),
        "reference_site_mapping": site, "protein_structure_context": protein,
        "selected_step_declares_site": None, "annotation": None,
        "reason": site["reason"],
    }
    if site["site_record"] is None:
        return result
    matched = site["site_record"]
    _require(matched["uniprot_id"] == accession,
             "reference annotation site belongs to another protein")
    features = source.get("features")
    _require(isinstance(features, list) and type(feature_index) is int
             and 0 <= feature_index < len(features),
             "reference annotation feature index is invalid")
    feature = features[feature_index]
    position = matched["sequence_position"]
    exact = {"value": position, "modifier": "EXACT"}
    _require(feature.get("type") == "Mutagenesis"
             and feature.get("location") == {"start": exact, "end": exact},
             "reference annotation is not an exact point-mutagenesis feature at this site")
    sequence = source.get("sequence", {}).get("value")
    original = _THREE_TO_ONE[matched["residue_name"]]
    variant = feature.get("alternativeSequence", {})
    alternatives = variant.get("alternativeSequences")
    _require(isinstance(sequence, str) and 0 < position <= len(sequence)
             and sequence[position - 1] == original
             and variant.get("originalSequence") == original,
             "reference annotation wild-type residue or sequence differs")
    _require(isinstance(alternatives, list) and bool(alternatives)
             and all(isinstance(item, str) and len(item) == 1
                     and item in _THREE_TO_ONE.values() and item != original
                     for item in alternatives)
             and len(alternatives) == len(set(alternatives)),
             "reference annotation alternatives are not unique single-residue substitutions")
    _require(isinstance(feature.get("description"), str) and bool(feature["description"]),
             "reference annotation source statement is absent")
    feature_evidence = feature.get("evidences")
    _require(isinstance(feature_evidence, list) and bool(feature_evidence)
             and all(isinstance(row, dict)
                     and all(isinstance(row.get(key), str) and bool(row[key])
                             for key in ("evidenceCode", "source", "id"))
                     for row in feature_evidence),
             "reference annotation lacks source evidence")
    references = []
    for witness in feature_evidence:
        matches = [row for row in source.get("references", [])
                   if any(cross.get("database") == witness.get("source")
                          and cross.get("id") == witness.get("id")
                          for cross in row.get("citation", {}).get("citationCrossReferences", []))]
        _require(len(matches) == 1, "reference annotation citation is absent or ambiguous")
        if matches[0] not in references:
            references.append(copy.deepcopy(matches[0]))
    result.update(
        status="source_database_annotation_at_reference_site", reason=None,
        selected_step_declares_site=site["site_id"] in step["catalyst_site_ids"],
        annotation={
            "counted_object": "database_mutagenesis_annotation",
            "evidence_basis": "retained_uniprot_database_annotation",
            "uniprot_id": accession, "site_id": site["site_id"],
            "entry_audit": copy.deepcopy(source["entryAudit"]),
            "feature_index": feature_index, "feature": copy.deepcopy(feature),
            "cited_reference_metadata": references,
            "source_statement_interpretation": "retain_opaque_activity_statement_without_endpoint_or_denominator_inference",
            "interpreted_quantity": {
                "status": "not_assessed_from_database_annotation",
                "endpoint": None, "parameter": None, "value": None, "unit": None,
                "denominator": None, "reaction_direction": None,
                "assay_conditions": None, "uncertainty": None,
            },
            "exact_assayed_construct_identity": False,
            "primary_result_details_supplied_by_annotation": False,
            "source_arrow_experimentally_validated": False,
            "source_residue_roles_assign_atom_role": False,
        },
    )
    return result
