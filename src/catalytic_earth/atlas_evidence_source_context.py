"""Source-scoped deposit context beside, and separate from, assay observations.

The source-format adapter checks retained mmCIF declarations. The query joins
an accepted annotation to an exact primary citation and reported variant; it
never makes a deposited model into an additional functional observation.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import PurePosixPath, PureWindowsPath
import re
from typing import Any, Callable

from .atlas_primary_source_check import parse_mmcif_categories


SPEC_SCHEMA = "catalytic-earth.mechanism-source-context-spec.v1"
BUNDLE_SCHEMA = "catalytic-earth.mechanism-source-contexts.v1"
QUERY_SCHEMA = "catalytic-earth.mechanism-source-context-query.v1"
PRIMARY_OBSERVATION_FIELDS = (
    "observation_id", "variant", "substrate", "endpoint", "conditions", "result",
    "comparator_variant_id",
)
_FINDING_STATUSES = {
    "deposited_source_assertion", "deposited_model_and_source_interpretation_separated",
    "unresolved_source_conflict",
}
_AA = dict(zip(
    "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
    "ARNDCQEGHILKMFPSTWYV",
))
_DISPLAY_FIELDS = (
    "annotation_id", "claim_id", "pdb_id", "source_binding", "source_relation",
    "source_rows", "findings", "ligand_instances", "not_established",
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _one(rows: list[dict], **fields: Any) -> dict:
    selected = [row for row in rows if all(row.get(key) == value for key, value in fields.items())]
    _require(len(selected) == 1, f"source-context relation must identify one row: {fields}")
    return selected[0]


def _bound_bytes(binding: dict, read_bytes: Callable[[str], bytes]) -> bytes:
    path = binding["path"]
    posix, windows = PurePosixPath(path), PureWindowsPath(path)
    _require(
        bool(path) and "\\" not in path and not posix.is_absolute()
        and not windows.drive and ".." not in posix.parts and path == posix.as_posix(),
        "source-context path must be repository-relative",
    )
    raw = read_bytes(path)
    _require(hashlib.sha256(raw).hexdigest() == binding["sha256"], "source-context bound source hash differs")
    return raw


def _deposit_difference(annotation: dict) -> dict:
    relation, rows = annotation["source_relation"], annotation["source_rows"]
    citation = _one(rows["_citation"], id="primary")
    _require(
        (citation["pdbx_database_id_pubmed"], citation["pdbx_database_id_doi"])
        == (relation["primary_pmid"], relation["doi"]),
        "deposit primary citation differs from source relation",
    )
    entity = _one(rows["_entity"], id=relation["protein_entity_id"])
    _require(entity["type"] == "polymer" and entity["pdbx_mutation"] == relation["variant"],
             "deposit entity variant differs")
    reference = _one(rows["_struct_ref"], entity_id=entity["id"], db_name="UNP",
                     pdbx_db_accession=relation["reference_accession"])
    alignment = _one(rows["_struct_ref_seq"], ref_id=reference["id"],
                     pdbx_strand_id=relation["author_chain_id"],
                     pdbx_db_accession=relation["reference_accession"],
                     pdbx_pdb_id_code=annotation["pdb_id"])
    difference = _one(
        rows["_struct_ref_seq_dif"], align_id=alignment["align_id"],
        pdbx_pdb_strand_id=relation["author_chain_id"],
        pdbx_seq_db_accession_code=relation["reference_accession"],
        pdbx_seq_db_name="UNP", pdbx_pdb_id_code=annotation["pdb_id"],
        seq_num=str(relation["deposited_sequence_position"]),
        pdbx_seq_db_seq_num=str(relation["reference_sequence_position"]),
        mon_id=relation["deposited_residue"], db_mon_id=relation["reference_residue"],
        details="engineered mutation",
    )
    variant = re.fullmatch(r"([A-Z])([1-9][0-9]*)([A-Z])", relation["variant"])
    _require(variant is not None, "source context requires a declared single substitution")
    _require(
        variant.groups() == (_AA.get(difference["db_mon_id"]),
                             difference["pdbx_seq_db_seq_num"], _AA.get(difference["mon_id"])),
        "deposited substitution differs from reference variant",
    )
    return difference


def audit_deposited_annotation(annotation: dict, raw_cif: bytes) -> None:
    """Recheck source rows and individual ligand instances; do not interpret prose."""
    binding = annotation["source_binding"]
    _require(len(raw_cif) == binding["uncompressed_bytes"]
             and hashlib.sha256(raw_cif).hexdigest() == binding["uncompressed_sha256"],
             "uncompressed deposit differs from source binding")
    tables = parse_mmcif_categories(raw_cif.decode("utf-8"))
    _one(tables["_entry"], id=annotation["pdb_id"])
    for category, expected in annotation["source_rows"].items():
        actual = tables[category]
        if category == "_citation":
            actual = [row for row in actual if row["id"] == "primary"]
        elif category == "_entity":
            actual = [row for row in actual if row["id"] == annotation["source_relation"]["protein_entity_id"]]
        _require(actual == expected, f"annotation source rows differ from retained deposit: {category}")
    difference = _deposit_difference(annotation)
    relation = annotation["source_relation"]
    residue = [row for row in tables["_atom_site"]
               if row["auth_asym_id"] == relation["author_chain_id"]
               and row["label_entity_id"] == relation["protein_entity_id"]
               and row["label_seq_id"] == difference["seq_num"]]
    _require(bool(residue) and {row["label_comp_id"] for row in residue} == {difference["mon_id"]}
             and {row["auth_seq_id"] for row in residue} == {difference["pdbx_auth_seq_num"]},
             "deposited variant coordinate identity differs")
    seen = set()
    for ligand in annotation["ligand_instances"]:
        component, instance = ligand["component"], ligand["instance"]
        key = (instance["asym_id"], instance["pdb_seq_num"], instance["pdb_ins_code"])
        _require(key not in seen, "deposited ligand instances repeat")
        seen.add(key)
        _require(component in tables["_chem_comp"] and instance in tables["_pdbx_nonpoly_scheme"]
                 and component["id"] == instance["mon_id"], "deposited ligand identity differs")
        atoms = [row for row in tables["_atom_site"]
                 if row["label_asym_id"] == instance["asym_id"]
                 and row["auth_seq_id"] == instance["pdb_seq_num"]
                 and row["auth_asym_id"] == instance["pdb_strand_id"]
                 and row["label_comp_id"] == component["id"]]
        _require(bool(atoms) and len(atoms) == ligand["modeled_coordinate_atom_count"]
                 and sorted({row["occupancy"] for row in atoms}) == ligand["deposited_occupancy_tokens"]
                 and sorted({row["label_alt_id"] for row in atoms}) == ligand["deposited_alternative_tokens"],
                 "deposited ligand instance tokens differ")


def _context_relation(context: dict, entry: dict, evidence: dict) -> tuple[dict, list[str]]:
    annotation, review = context["annotation"], context["annotation_review"]
    _require(_sha(annotation) == entry["annotation_binding"]["sha256"]
             and _sha(review) == entry["review_binding"]["sha256"], "source-context review binding differs")
    _require(annotation["schema_version"] == "catalytic-earth.source-structure-followup.v1"
             and annotation["status"] == "source_scoped_annotation_not_integrated_into_observation_query"
             and review["schema_version"] == "catalytic-earth.source-annotation-review.v1"
             and review["decision"] == "accept_source_scoped_annotation"
             and review["open_source_objections"] == [], "source annotation is not accepted")
    _require(review["reviewed_sha256"].get(PurePosixPath(entry["annotation_binding"]["path"]).name)
             == _sha(annotation), "source annotation changed after review")
    _require(review["reviewed_sha256"].get(PurePosixPath(annotation["source_binding"]["path"]).name)
             == annotation["source_binding"]["sha256"], "deposit changed after annotation review")
    _require(annotation["existing_case_binding"]["sha256"] == _sha(evidence),
             "source-context existing evidence binding differs")
    _require(annotation["claim_id"] == entry["claim_id"], "source-context claim binding differs")
    _require(annotation["source_relation"]["reference_scope"]
             == "deposition-declared UniProt alignment, not independently verified assay construct",
             "deposited reference cannot establish assay construct identity")
    _require(isinstance(annotation["not_established"], list) and bool(annotation["not_established"])
             and all(isinstance(item, str) and item.strip() for item in annotation["not_established"]),
             "deposited context requires explicit source and inference abstentions")
    _require(bool(annotation["findings"])
             and all(row["status"] in _FINDING_STATUSES for row in annotation["findings"]),
             "deposited context has an unsupported observation or interpretation status")
    _require(set(entry["required_finding_statuses"]) <= _FINDING_STATUSES
             and {row["status"] for row in annotation["findings"]} == set(entry["required_finding_statuses"]),
             "reviewed source finding roles were removed or changed")
    _require(len({row["finding_id"] for row in annotation["findings"]}) == len(annotation["findings"]),
             "source-context finding identifiers repeat")
    _require(all(isinstance(row["chemical_identity_scope"], str) and row["chemical_identity_scope"].strip()
                 for row in annotation["ligand_instances"]), "ligand chemical identity scope is absent")
    case = _one(evidence["cases"], case_id=entry["case_id"])
    reference = _one(case["evidence_references"], evidence_id=entry["evidence_id"])
    binding = _one(evidence["source_bindings"], binding_id=reference["source_binding_id"])
    projection = context["primary_projection"]
    _require(binding["artifact_kind"] == "primary_source_projection"
             and binding["sha256"] == _sha(projection), "source-context primary projection binding differs")
    relation = annotation["source_relation"]
    _require(reference["source_id"] == projection["source_id"] == "PubMed"
             and reference["source_record_id"] == projection["source_record_id"] == "PMID:" + relation["primary_pmid"]
             and projection["doi"] == relation["doi"], "deposit and primary evidence citation differ")
    difference = _deposit_difference(annotation)
    expected_variant = {
        "uniprot_id": relation["reference_accession"], "variant_id": relation["variant"],
        "substitutions": [{"wild_type_residue": _AA[difference["db_mon_id"]],
                           "sequence_position": relation["reference_sequence_position"],
                           "mutant_residue": _AA[difference["mon_id"]]}],
    }
    observations = [row for row in case["observations"]
                    if entry["evidence_id"] in row["evidence_ids"] and row["variant"] == expected_variant]
    _require(bool(observations), "deposit has no exact primary-evidence variant relation")
    for row in observations:
        projected = _one(projection["observations"], observation_id=row["observation_id"])
        _require(projected == {key: row[key] for key in PRIMARY_OBSERVATION_FIELDS},
                 "source-context observation differs from primary projection")
    return case, [row["observation_id"] for row in observations]


def validate_source_contexts(bundle: dict, evidence: dict) -> None:
    _require(bundle.get("schema_version") == BUNDLE_SCHEMA, "unsupported source-context bundle")
    spec = bundle["spec"]
    _require(spec.get("schema_version") == SPEC_SCHEMA and spec["evidence_binding"]["sha256"] == _sha(evidence),
             "source-context specification belongs to different evidence")
    _require(isinstance(bundle["contexts"], list) and bool(bundle["contexts"])
             and len(bundle["contexts"]) == len(spec["contexts"]), "source-context inventory differs")
    seen = set()
    for entry, context in zip(spec["contexts"], bundle["contexts"]):
        _require(context["annotation"]["existing_case_binding"] == spec["evidence_binding"],
                 "source-context existing evidence path or hash differs")
        _context_relation(context, entry, evidence)
        key = (entry["case_id"], context["annotation"]["annotation_id"])
        _require(key not in seen, "source-context case/annotation relation repeats")
        seen.add(key)


def build_source_contexts(spec: dict, evidence: dict, read_bytes: Callable[[str], bytes]) -> dict:
    _require(_bound_bytes(spec["evidence_binding"], read_bytes) == canonical_bytes(evidence),
             "source-context evidence file differs")
    contexts = []
    for entry in spec["contexts"]:
        annotation = json.loads(_bound_bytes(entry["annotation_binding"], read_bytes))
        review = json.loads(_bound_bytes(entry["review_binding"], read_bytes))
        review_directory = PurePosixPath(entry["review_binding"]["path"]).parent
        for name, digest in review["reviewed_sha256"].items():
            _require(PurePosixPath(name).name == name and "\\" not in name,
                     "reviewed source filenames must be local")
            _bound_bytes({"path": str(review_directory / name), "sha256": digest}, read_bytes)
        compressed = _bound_bytes(annotation["source_binding"], read_bytes)
        audit_deposited_annotation(annotation, gzip.decompress(compressed))
        case = _one(evidence["cases"], case_id=entry["case_id"])
        reference = _one(case["evidence_references"], evidence_id=entry["evidence_id"])
        binding = _one(evidence["source_bindings"], binding_id=reference["source_binding_id"])
        contexts.append({"annotation": annotation, "annotation_review": review,
                         "primary_projection": json.loads(_bound_bytes(binding, read_bytes))})
    bundle = {"schema_version": BUNDLE_SCHEMA, "spec": copy.deepcopy(spec), "contexts": contexts}
    validate_source_contexts(bundle, evidence)
    return bundle


def query_source_contexts(bundle: dict, evidence: dict, *, variant: str | None = None) -> dict:
    """Variant filters apply to context; observation endpoint filters do not."""
    validate_source_contexts(bundle, evidence)
    if variant is not None:
        _require(isinstance(variant, str), "source-context variant must be text")
        variant = variant.strip().upper()
        _require(re.fullmatch(r"WT|[A-Z][1-9][0-9]*[A-Z]", variant) is not None,
                 "source-context variant must be WT or an exact substitution")
    matches = []
    for entry, context in zip(bundle["spec"]["contexts"], bundle["contexts"]):
        annotation = context["annotation"]
        if variant is not None and variant != annotation["source_relation"]["variant"]:
            continue
        case, observation_ids = _context_relation(context, entry, evidence)
        matches.append({
            "case": copy.deepcopy(case), "related_evidence_id": entry["evidence_id"],
            "citation_variant_related_observation_ids": observation_ids,
            "source_type": "PDB_deposit", "context_kind": "deposited_variant",
            "relation": {
                "relation_kind": "exact_primary_citation_and_reported_variant",
                "asserted_equivalences": ["same_primary_citation_pmid_and_doi",
                                          "same_reported_variant_label_and_substitution"],
                "unresolved_equivalences": ["exact_assayed_construct_and_preparation_identity",
                                            "crystal_to_assay_physical_state_identity",
                                            "deposited_gene_source_to_assayed_organism_identity"],
                "reference_accession_scope": "deposition_declared_reference_and_atlas_context_not_abstract_declared_assay_identity",
            },
            "source_context": copy.deepcopy({key: annotation[key] for key in _DISPLAY_FIELDS}),
            "provenance": copy.deepcopy({"annotation_binding": entry["annotation_binding"],
                                          "review_binding": entry["review_binding"],
                                          "evidence_binding": bundle["spec"]["evidence_binding"],
                                          "reviewed_at_utc": context["annotation_review"]["reviewed_at_utc"],
                                          "review_process": context["annotation_review"]["review_process"]}),
        })
    return {
        "schema_version": QUERY_SCHEMA, "filters": {"variant": variant},
        "context_count": len(matches), "matches": matches,
        "query_semantics": {
            "counted_object": "source_scoped_deposited_variant_context",
            "endpoint_filter_applies": False,
            "endpoint_filter_scope": "original_abstract_observations_only",
            "citation_variant_related_observation_ids_scope": "all_same_citation_and_variant_observations_not_endpoint_filtered",
            "case_and_adjudication_preserved": True,
            "context_membership_satisfies_observation_filter": False,
            "context_count_is_observation_count": False,
            "deposited_model_is_additional_functional_observation": False,
            "bound_ligand_protonation_established": False,
            "depositor_product_origin_is_functional_observation": False,
            "assay_specimen_identity_established": False,
            "organism_conflict_resolved": False,
            "empty_result": "no_matching_retained_context_not_absence_of_a_deposit_or_behavior",
        },
    }
