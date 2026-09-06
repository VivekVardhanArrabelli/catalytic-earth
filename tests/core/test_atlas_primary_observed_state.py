from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


from catalytic_earth import atlas_primary_evidence as PRIMARY
from catalytic_earth.canonical_hash import canonical_file_sha256


REPO = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    return canonical_file_sha256(path)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy(target_root: Path, relative: str, source: Path) -> dict:
    target = target_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    return {"path": relative, "sha256": _sha256(target)}


def _fixture_file(target_root: Path, relative: str, content: bytes) -> dict:
    target = target_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return {"path": relative, "sha256": _sha256(target)}


def _bundle() -> dict:
    return json.loads(
        (REPO / "src/catalytic_earth/draft_data/plp_pyruvoyl.json").read_text(
            encoding="utf-8"
        )
    )


def _record(bundle: dict, mcsa_id: str) -> dict:
    return next(row for row in bundle["records"] if row["mcsa_id"] == mcsa_id)


def _record_binding(record: dict) -> dict:
    return {
        "record_id": record["record_id"],
        "mcsa_id": record["mcsa_id"],
        "source_snapshot_sha256": record["source"]["snapshot_sha256"],
    }


def _scope_effect() -> dict:
    return {
        "record_evidence_tier_changed": False,
        "allowed_operations_changed": False,
        "mechanism_scope_expanded": False,
        "source_step_trajectory_claimed": False,
        "proposal_applicability_claimed": False,
    }


def _limits(*extra: tuple[str, str]) -> list[dict]:
    rows = [
        {
            "limit_id": "chemical_identity_beyond_source",
            "status": "abstained",
            "statement": "No free-participant or unsourced chemical identity is assigned.",
        },
        {
            "limit_id": "exact_reaction_instance",
            "status": "abstained",
            "statement": "The structure does not close the exact reaction instance.",
        },
        {
            "limit_id": "mechanism_applicability",
            "status": "abstained",
            "statement": "The record-level observation does not validate a proposal.",
        },
        {
            "limit_id": "state_trajectory",
            "status": "abstained",
            "statement": "No temporal trajectory or atom-mapped transition is observed.",
        },
    ]
    rows.extend(
        {"limit_id": limit_id, "status": "abstained", "statement": statement}
        for limit_id, statement in extra
    )
    return rows


def _review() -> dict:
    return {
        "reviewed_on": "2026-09-06",
        "annotation_payload_sha256": "0" * 64,
        "update_rule": PRIMARY.PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE,
        "reviewer_kind": "same_model_computational_agents",
        "same_model_agents": True,
        "blind_review": False,
        "statistically_independent": False,
        "correlated_error_risk": True,
        "human_reviewers": 0,
        "domain_expert_review_claimed": False,
    }


def _repin(sidecar: dict) -> None:
    sidecar["review"]["annotation_payload_sha256"] = (
        PRIMARY.canonical_annotation_payload_sha256(sidecar)
    )


def _projection_binding(projection: dict) -> dict:
    return {
        "binding_id": "project:observed-state-projection",
        "projection_id": projection["projection_id"],
        "context_id": projection["context_id"],
    }


def _source_binding(binding_id: str, artifact_kind: str, row: dict) -> dict:
    return {
        "binding_id": binding_id,
        "artifact_kind": artifact_kind,
        "path": row["path"],
        "sha256": row["sha256"],
    }


def _projection_source(binding: dict) -> dict:
    return {key: binding[key] for key in ("binding_id", "path", "sha256")}


def _evidence(
    evidence_id: str,
    role: str,
    source_kind: str,
    source_id: str,
    binding: dict,
) -> dict:
    return {
        "evidence_id": evidence_id,
        "evidence_role": role,
        "source_kind": source_kind,
        "source_id": source_id,
        "uri": "https://example.invalid/" + evidence_id.replace(":", "/"),
        "citation": "Captured source fixture for " + source_id,
        "experimental_context": "Scope is restricted to the typed projection.",
        "source_binding_id": binding["binding_id"],
        "source_sha256": binding["sha256"],
    }


def _locator(
    locator_id: str,
    binding_id: str,
    source_format: str,
    extracted_values: dict,
) -> dict:
    return {
        "locator_id": locator_id,
        "source_binding_id": binding_id,
        "source_format": source_format,
        "selector": {"fixture_selector": locator_id},
        "physical_lines": [1],
        "extracted_values": extracted_values,
        "supports": locator_id.replace("-", " "),
    }


def _materialize_projection(root: Path, sidecar: dict, projection: dict) -> None:
    projection_path = root / "evidence/observed_state_projection.json"
    _write_json(projection_path, projection)
    binding = next(
        row
        for row in sidecar["source_bindings"]
        if row["binding_id"] == "project:observed-state-projection"
    )
    binding["sha256"] = _sha256(projection_path)
    _repin(sidecar)


def _m0049_fixture(root: Path) -> tuple[dict, dict, dict]:
    bundle = _bundle()
    record = _record(bundle, "M0049")
    cif_row = _fixture_file(
        root, "evidence/1PYA.cif", b"data_1PYA\n# synthetic binding fixture\n"
    )
    source_row = _copy(
        root,
        "evidence/M0049.json",
        REPO / "data/atlas/source_drafts/batches/plp-pyruvoyl/sources/M0049.json",
    )
    uniprot_row = _fixture_file(
        root,
        "evidence/UniProt_P00862.json",
        b'{"primaryAccession":"P00862"}\n',
    )
    projection_path = root / "evidence/observed_state_projection.json"
    projection_path.write_text("{}\n", encoding="utf-8")
    projection_row = {
        "path": "evidence/observed_state_projection.json",
        "sha256": _sha256(projection_path),
    }
    cif_binding = _source_binding("primary:RCSB:1PYA:mmCIF", "primary_source", cif_row)
    source_binding = _source_binding(
        "source:M-CSA:M0049:snapshot", "source_record_snapshot", source_row
    )
    uniprot_binding = _source_binding(
        "curated:UniProt:P00862", "curated_reference", uniprot_row
    )
    project_binding = _source_binding(
        "project:observed-state-projection", "project_projection", projection_row
    )
    structure_context = {
        "pdb_id": "1PYA",
        "model_id": 1,
        "protein_entity_ids": ["2"],
        "protein_label_asym_ids": ["F"],
        "protein_author_chain_ids": ["F"],
        "curated_protein_accession": "P00862",
    }
    entity = {
        "state_kind": "polymer_modified_component",
        "entity_context": "polymer_component",
        "entity_id": "2",
        "source_component_id": "PYR",
        "source_description": "PYRUVIC ACID",
        "chemical_context": "processed_state",
        "attachment_context": "polymer_integrated",
        "normalized_chebi_id": None,
    }
    instance = {
        "label_asym_id": "F",
        "label_entity_id": "2",
        "label_component_id": "PYR",
        "label_seq_id": 1,
        "atom_author_chain_id": "F",
        "atom_author_component_id": "PYR",
        "atom_author_residue_number": 82,
        "source_author_component_id": None,
        "source_author_residue_number": None,
        "structure_site_id": None,
    }
    canonical = {"accession": "P00862", "residue_name": "SER", "sequence_position": 83}
    source_alias = {
        "source_assertion_id": "atlas-draft.m0049.source-residue-7",
        "pdb_id": "1PYA",
        "chain_id": "F",
        "label_position": 1,
        "author_position": 1,
        "residue_code": "X",
        "ptm_name": "Pyr",
    }
    crosswalk = {
        "status": "cross_source_curated_projection",
        "relationship": "precursor_residue_to_processed_component",
        "structure_instance_index": 0,
        "canonical_site": canonical,
        "source_record_alias": source_alias,
        "author_number_mapping_status": "not_asserted",
        "support_edge_ids": [
            "edge:curated-canonical-site",
            "edge:deposited-structure-state",
            "edge:cross-source-correspondence",
        ],
    }
    evidence = [
        _evidence(
            "evidence:1pya-cif",
            "direct_support",
            "primary_structure_record",
            "RCSB PDB:1PYA",
            cif_binding,
        ),
        _evidence(
            "evidence:m0049-source",
            "source_record_only",
            "official_source_record",
            "M-CSA:M0049",
            source_binding,
        ),
        _evidence(
            "evidence:p00862-curated",
            "curated_identity_support",
            "curated_protein_record",
            "UniProtKB:P00862",
            uniprot_binding,
        ),
    ]
    next(
        item for item in evidence if item["evidence_role"] == "source_record_only"
    )["uri"] = record["source"]["uri"]
    projection_sources = sorted(
        map(_projection_source, [cif_binding, source_binding, uniprot_binding]),
        key=lambda row: row["path"],
    )
    locators = [
        _locator(
            "locator:1pya-pyr",
            cif_binding["binding_id"],
            "mmcif",
            {"label_asym_id": "F", "label_seq_id": 1, "author_residue_number": 82},
        ),
        _locator(
            "locator:m0049-pyr1f-ser83",
            source_binding["binding_id"],
            "json",
            {"source_record_alias": source_alias, "canonical_site": canonical},
        ),
        _locator(
            "locator:p00862-ser83",
            uniprot_binding["binding_id"],
            "json",
            {"canonical_site": canonical, "description": "Pyruvic acid (Ser)"},
        ),
    ]
    chemical_observations = [
        {
            "observation_id": "observation:deposited-pyr-state",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_component_state",
            "source_description": "1PYA chain F contains PYR at label 1 and author 82.",
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:1pya-cif"],
            "support_edge_ids": ["edge:deposited-structure-state"],
        }
    ]
    chemical_reconciliation = {
        "status": "not_required",
        "statement": "The deposited component and curated precursor site remain separate evidence edges.",
    }
    projection = {
        "schema_version": "catalytic-earth.primary-observed-state-projection.v1",
        "projection_id": "primary-observed-state:M0049:1PYA:PYR",
        "context_id": "1pya-chain-f-pyr-label1-p00862-ser83",
        "record_binding": _record_binding(record),
        "source_bindings": projection_sources,
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": [instance],
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": chemical_reconciliation,
        "support_edges": [
            {
                "edge_id": "edge:deposited-structure-state",
                "edge_kind": "deposited_structure_state",
                "support_status": "direct_structure_observation",
                "source_binding_ids": [cif_binding["binding_id"]],
                "locator_ids": ["locator:1pya-pyr"],
                "extracted_values": {
                    "entity_context": entity["entity_context"],
                    "entity_id": entity["entity_id"],
                    "source_component_id": entity["source_component_id"],
                    "source_description": entity["source_description"],
                    "structure_instances": [instance],
                },
            },
            {
                "edge_id": "edge:curated-canonical-site",
                "edge_kind": "curated_canonical_site",
                "support_status": "curated_identity_support",
                "source_binding_ids": [uniprot_binding["binding_id"]],
                "locator_ids": ["locator:p00862-ser83"],
                "extracted_values": {"canonical_site": canonical},
            },
            {
                "edge_id": "edge:cross-source-correspondence",
                "edge_kind": "cross_source_correspondence",
                "support_status": "cross_source_curated_projection",
                "source_binding_ids": [
                    cif_binding["binding_id"],
                    source_binding["binding_id"],
                    uniprot_binding["binding_id"],
                ],
                "locator_ids": [
                    "locator:1pya-pyr",
                    "locator:m0049-pyr1f-ser83",
                    "locator:p00862-ser83",
                ],
                "extracted_values": {
                    "relationship": crosswalk["relationship"],
                    "structure_instance_index": 0,
                    "canonical_site": canonical,
                    "source_record_alias": source_alias,
                    "author_number_mapping_status": "not_asserted",
                },
            },
        ],
        "locators": locators,
        "limits": [
            "The CIF observes author PYR82/label PYR1; M-CSA author position 1 is not projected onto it.",
            "The cross-source projection does not claim a precursor-cleavage trajectory.",
        ],
    }
    claim = {
        "statement": (
            "1PYA deposits chain-F PYR label 1/author 82; the reviewed cross-source "
            "projection relates that processed component to curated P00862 Ser83."
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": [instance],
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": chemical_reconciliation,
        "direct_evidence_ids": ["evidence:1pya-cif"],
        "curated_identity_evidence_ids": ["evidence:p00862-curated"],
        "source_record_evidence_ids": ["evidence:m0049-source"],
        "corroborating_evidence_ids": [],
        "observed_state_grounds_step": False,
    }
    annotation = {
        "annotation_id": "m0049.1pya.processed-pyruvoyl-crosswalk",
        "record_binding": _record_binding(record),
        "annotation_kind": "primary_observed_state_context",
        "target_scope": "record_only",
        "projection_binding": _projection_binding(projection),
        "projection_excerpt": {
            "support_edges": projection["support_edges"],
            "locators": projection["locators"],
        },
        "claim": claim,
        "evidence": evidence,
        "limits": _limits(
            (
                "numbering_namespaces",
                "PDB author 82, PDB label 1, M-CSA author 1, and P00862 83 remain distinct.",
            ),
        ),
        "scope_effect": _scope_effect(),
    }
    sidecar = {
        "schema_version": "catalytic-earth.atlas-primary-evidence.v3",
        "annotation_set_id": "atlas-primary-evidence:plp-pyruvoyl:v3-test",
        "batch_id": "plp-pyruvoyl",
        "status": "reviewed_primary_evidence_annotations_not_mechanism_expansion",
        "source_bindings": sorted(
            [cif_binding, source_binding, uniprot_binding, project_binding],
            key=lambda row: row["path"],
        ),
        "annotations": [annotation],
        "review": _review(),
    }
    _materialize_projection(root, sidecar, projection)
    return bundle, sidecar, projection


def _m0213_fixture(root: Path) -> tuple[dict, dict, dict]:
    bundle = _bundle()
    record = _record(bundle, "M0213")
    cif_row = _fixture_file(
        root, "evidence/1L6G.cif", b"data_1L6G\n# synthetic binding fixture\n"
    )
    article_row = _fixture_file(
        root,
        "evidence/PubMed_11886871_projection.json",
        b'{"pubmed_id":"11886871","designation":"reaction intermediate analog"}\n',
    )
    uniprot_row = _fixture_file(
        root,
        "evidence/UniProt_P10724.json",
        b'{"primaryAccession":"P10724"}\n',
    )
    projection_path = root / "evidence/observed_state_projection.json"
    projection_path.write_text("{}\n", encoding="utf-8")
    projection_row = {
        "path": "evidence/observed_state_projection.json",
        "sha256": _sha256(projection_path),
    }
    cif_binding = _source_binding("primary:RCSB:1L6G:mmCIF", "primary_source", cif_row)
    article_binding = _source_binding(
        "projection:PubMed:11886871:abstract",
        "primary_source_projection",
        article_row,
    )
    uniprot_binding = _source_binding(
        "curated:UniProt:P10724", "curated_reference", uniprot_row
    )
    project_binding = _source_binding(
        "project:observed-state-projection", "project_projection", projection_row
    )
    structure_context = {
        "pdb_id": "1L6G",
        "model_id": 1,
        "protein_entity_ids": ["1"],
        "protein_label_asym_ids": ["A", "B"],
        "protein_author_chain_ids": ["A", "B"],
        "curated_protein_accession": "P10724",
    }
    entity = {
        "state_kind": "bound_ligand_analogue",
        "entity_context": "nonpolymer_component",
        "entity_id": "2",
        "source_component_id": "PDD",
        "source_description": "N-(5'-PHOSPHOPYRIDOXYL)-D-ALANINE",
        "chemical_context": "source_designated_analogue",
        "attachment_context": "absent_from_deposited_struct_conn",
        "normalized_chebi_id": None,
    }
    instances = [
        {
            "label_asym_id": "C",
            "label_entity_id": "2",
            "label_component_id": "PDD",
            "label_seq_id": None,
            "atom_author_chain_id": "A",
            "atom_author_component_id": "PDD",
            "atom_author_residue_number": 390,
            "source_author_component_id": "PDA",
            "source_author_residue_number": 390,
            "structure_site_id": "AC1",
        },
        {
            "label_asym_id": "D",
            "label_entity_id": "2",
            "label_component_id": "PDD",
            "label_seq_id": None,
            "atom_author_chain_id": "B",
            "atom_author_component_id": "PDD",
            "atom_author_residue_number": 1390,
            "source_author_component_id": "PDA",
            "source_author_residue_number": 390,
            "structure_site_id": "AC2",
        },
    ]
    crosswalk = {
        "status": "not_asserted",
        "relationship": "not_asserted",
        "structure_instance_index": None,
        "canonical_site": None,
        "source_record_alias": None,
        "author_number_mapping_status": "not_asserted",
        "support_edge_ids": [],
    }
    evidence = [
        _evidence(
            "evidence:1l6g-cif",
            "direct_support",
            "primary_structure_record",
            "RCSB PDB:1L6G",
            cif_binding,
        ),
        _evidence(
            "evidence:11886871-article",
            "direct_support",
            "primary_research_article",
            "PubMed:11886871",
            article_binding,
        ),
        _evidence(
            "evidence:p10724-curated",
            "curated_identity_support",
            "curated_protein_record",
            "UniProtKB:P10724",
            uniprot_binding,
        ),
    ]
    locators = [
        _locator(
            "locator:1l6g-pdd-instances",
            cif_binding["binding_id"],
            "mmcif",
            {"entity_id": "2", "component_id": "PDD", "instances": instances},
        ),
        _locator(
            "locator:1l6g-struct-conn",
            cif_binding["binding_id"],
            "mmcif",
            {
                "struct_conn_row_count": 4,
                "matching_component_row_count": 0,
                "connected_component_ids": ["KCX", "LEU", "MET"],
            },
        ),
        _locator(
            "locator:11886871-analogue",
            article_binding["binding_id"],
            "pubmed_xml",
            {"component_id": "PDD", "designation": "reaction intermediate analog"},
        ),
        _locator(
            "locator:p10724-1l6g",
            uniprot_binding["binding_id"],
            "json",
            {"accession": "P10724", "pdb_id": "1L6G", "chains": "A/B=1-388"},
        ),
    ]
    chemical_observations = [
        {
            "observation_id": "observation:deposited-pdd-state",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_component_state",
            "source_description": "1L6G deposits two PDD nonpolymer instances.",
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:1l6g-cif"],
            "support_edge_ids": ["edge:deposited-structure-state"],
        },
        {
            "observation_id": "observation:primary-analogue-description",
            "source_scope": "primary_research_article",
            "observation_kind": "primary_article_state_description",
            "source_description": "The source article designates PLP-D-Ala as a reaction-intermediate analogue.",
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:11886871-article"],
            "support_edge_ids": ["edge:primary-article-analogue"],
        },
    ]
    chemical_reconciliation = {
        "status": "source_scopes_separated",
        "statement": "The deposited PDD identity and primary-article analogue designation are retained as separate observations.",
    }
    projection = {
        "schema_version": "catalytic-earth.primary-observed-state-projection.v1",
        "projection_id": "primary-observed-state:M0213:1L6G:PDD",
        "context_id": "1l6g-pdd-bound-d-alanine-analogue",
        "record_binding": _record_binding(record),
        "source_bindings": sorted(
            map(_projection_source, [cif_binding, article_binding, uniprot_binding]),
            key=lambda row: row["path"],
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": instances,
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": chemical_reconciliation,
        "support_edges": [
            {
                "edge_id": "edge:deposited-structure-state",
                "edge_kind": "deposited_structure_state",
                "support_status": "direct_structure_observation",
                "source_binding_ids": [cif_binding["binding_id"]],
                "locator_ids": ["locator:1l6g-pdd-instances"],
                "extracted_values": {
                    "entity_context": entity["entity_context"],
                    "entity_id": entity["entity_id"],
                    "source_component_id": entity["source_component_id"],
                    "source_description": entity["source_description"],
                    "structure_instances": instances,
                },
            },
            {
                "edge_id": "edge:primary-article-analogue",
                "edge_kind": "primary_article_analogue_designation",
                "support_status": "source_designated_analogue",
                "source_binding_ids": [article_binding["binding_id"]],
                "locator_ids": ["locator:11886871-analogue"],
                "extracted_values": {
                    "source_component_id": "PDD",
                    "chemical_context": "source_designated_analogue",
                },
            },
            {
                "edge_id": "edge:deposited-connection-inventory",
                "edge_kind": "deposited_connection_inventory",
                "support_status": "absent_from_deposited_struct_conn",
                "source_binding_ids": [cif_binding["binding_id"]],
                "locator_ids": ["locator:1l6g-struct-conn"],
                "extracted_values": {
                    "queried_component_id": "PDD",
                    "attachment_context": "absent_from_deposited_struct_conn",
                    "struct_conn_row_count": 4,
                    "matching_component_row_count": 0,
                    "connected_component_ids": ["KCX", "LEU", "MET"],
                },
            },
            {
                "edge_id": "edge:curated-protein-identity",
                "edge_kind": "curated_protein_identity",
                "support_status": "curated_identity_support",
                "source_binding_ids": [uniprot_binding["binding_id"]],
                "locator_ids": ["locator:p10724-1l6g"],
                "extracted_values": {"accession": "P10724", "pdb_id": "1L6G"},
            },
        ],
        "locators": locators,
        "limits": [
            "Absence is confined to the deposited struct_conn table; no general physical noncovalency is inferred.",
            "The analogue does not validate a native external aldimine, quinoid, role, protonation, direction, or trajectory.",
        ],
    }
    claim = {
        "statement": (
            "1L6G deposits two PDD instances and PMID 11886871 identifies "
            "phosphopyridoxyl-D-alanine as a reaction-intermediate analogue; "
            "no PDD-protein connection occurs in the deposited struct_conn table."
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": instances,
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": chemical_reconciliation,
        "direct_evidence_ids": ["evidence:1l6g-cif", "evidence:11886871-article"],
        "curated_identity_evidence_ids": ["evidence:p10724-curated"],
        "source_record_evidence_ids": [],
        "corroborating_evidence_ids": [],
        "observed_state_grounds_step": False,
    }
    annotation = {
        "annotation_id": "m0213.1l6g.pdd-bound-analogue",
        "record_binding": _record_binding(record),
        "annotation_kind": "primary_observed_state_context",
        "target_scope": "record_only",
        "projection_binding": _projection_binding(projection),
        "projection_excerpt": {
            "support_edges": projection["support_edges"],
            "locators": projection["locators"],
        },
        "claim": claim,
        "evidence": evidence,
        "limits": _limits(
            (
                "deposited_connection_scope",
                "No PDD row occurs in deposited struct_conn; this is not a general physical noncovalency assertion.",
            ),
            (
                "native_intermediate_scope",
                "The primary article calls this an analogue, not an observed native transient.",
            ),
        ),
        "scope_effect": _scope_effect(),
    }
    sidecar = {
        "schema_version": "catalytic-earth.atlas-primary-evidence.v3",
        "annotation_set_id": "atlas-primary-evidence:plp-pyruvoyl:v3-test",
        "batch_id": "plp-pyruvoyl",
        "status": "reviewed_primary_evidence_annotations_not_mechanism_expansion",
        "source_bindings": sorted(
            [cif_binding, article_binding, uniprot_binding, project_binding],
            key=lambda row: row["path"],
        ),
        "annotations": [annotation],
        "review": _review(),
    }
    _materialize_projection(root, sidecar, projection)
    return bundle, sidecar, projection


def _m0186_fixture(root: Path) -> tuple[dict, dict, dict]:
    bundle = _bundle()
    record = _record(bundle, "M0186")
    cif_row = _fixture_file(
        root, "evidence/1PWH.cif", b"data_1PWH\n# synthetic binding fixture\n"
    )
    article_row = _fixture_file(
        root,
        "evidence/PubMed_14596599_projection.json",
        (
            b'{"pubmed_id":"14596599","description":'
            b'"PLP-OMS aldimine; dehydration did not occur"}\n'
        ),
    )
    projection_path = root / "evidence/observed_state_projection.json"
    projection_path.write_text("{}\n", encoding="utf-8")
    cif_binding = _source_binding(
        "primary:RCSB:1PWH:mmCIF", "primary_source", cif_row
    )
    article_binding = _source_binding(
        "projection:PubMed:14596599:abstract",
        "primary_source_projection",
        article_row,
    )
    project_binding = _source_binding(
        "project:observed-state-projection",
        "project_projection",
        {"path": "evidence/observed_state_projection.json", "sha256": _sha256(projection_path)},
    )
    structure_context = {
        "pdb_id": "1PWH",
        "model_id": 1,
        "protein_entity_ids": ["1"],
        "protein_label_asym_ids": ["A"],
        "protein_author_chain_ids": ["A"],
        "curated_protein_accession": None,
    }
    entity = {
        "state_kind": "bound_ligand_adduct",
        "entity_context": "nonpolymer_component",
        "entity_id": "3",
        "source_component_id": "PLV",
        "source_description": "O-phosphonopyridoxyl-serine adduct",
        "chemical_context": "source_described_bound_adduct",
        "attachment_context": "absent_from_deposited_struct_conn",
        "normalized_chebi_id": None,
    }
    instance = {
        "label_asym_id": "F",
        "label_entity_id": "3",
        "label_component_id": "PLV",
        "label_seq_id": None,
        "atom_author_chain_id": "A",
        "atom_author_component_id": "PLV",
        "atom_author_residue_number": 328,
        "source_author_component_id": None,
        "source_author_residue_number": None,
        "structure_site_id": None,
    }
    crosswalk = {
        "status": "not_asserted",
        "relationship": "not_asserted",
        "structure_instance_index": None,
        "canonical_site": None,
        "source_record_alias": None,
        "author_number_mapping_status": "not_asserted",
        "support_edge_ids": [],
    }
    evidence = [
        _evidence(
            "evidence:1pwh-cif",
            "direct_support",
            "primary_structure_record",
            "RCSB PDB:1PWH",
            cif_binding,
        ),
        _evidence(
            "evidence:14596599-article",
            "direct_support",
            "primary_research_article",
            "PubMed:14596599",
            article_binding,
        ),
    ]
    locators = [
        _locator(
            "locator:1pwh-plv-bond",
            cif_binding["binding_id"],
            "mmcif",
            {"component_id": "PLV", "atom_id_1": "N", "atom_id_2": "C4A", "value_order": "sing"},
        ),
        _locator(
            "locator:1pwh-plv-instance",
            cif_binding["binding_id"],
            "mmcif",
            {"entity_id": "3", "component_id": "PLV", "instances": [instance]},
        ),
        _locator(
            "locator:1pwh-struct-conn",
            cif_binding["binding_id"],
            "mmcif",
            {
                "struct_conn_row_count": 26,
                "matching_component_row_count": 0,
                "connected_component_ids": ["ALA", "GLU", "GLY", "K", "LEU", "SER", "VAL"],
            },
        ),
        _locator(
            "locator:14596599-bound-adduct",
            article_binding["binding_id"],
            "source_projection_json",
            {
                "description": "PLP-OMS aldimine",
                "dehydration_status": "did_not_occur",
            },
        ),
    ]
    chemical_observations = [
        {
            "observation_id": "observation:deposited-plv-bond",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_component_bond_order",
            "source_description": "The deposited PLV component dictionary records N-C4A value_order sing.",
            "source_bond_order_code": "sing",
            "evidence_ids": ["evidence:1pwh-cif"],
            "support_edge_ids": ["edge:deposited-component-bond-order"],
        },
        {
            "observation_id": "observation:primary-aldimine-description",
            "source_scope": "primary_research_article",
            "observation_kind": "primary_article_state_description",
            "source_description": "The primary abstract describes a PLP-OMS aldimine and says dehydration did not occur.",
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:14596599-article"],
            "support_edge_ids": ["edge:primary-article-bound-adduct"],
        },
    ]
    reconciliation = {
        "status": "unresolved_source_description_vs_deposit",
        "statement": "The paper description and deposited component bond-order token are separate observations; their exact chemical identity and bond-order relationship is unresolved.",
    }
    edges = [
        {
            "edge_id": "edge:deposited-component-bond-order",
            "edge_kind": "deposited_component_bond_order",
            "support_status": "direct_structure_observation",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:1pwh-plv-bond"],
            "extracted_values": {
                "source_component_id": "PLV",
                "source_bond_order_code": "sing",
                "source_description": chemical_observations[0]["source_description"],
            },
        },
        {
            "edge_id": "edge:deposited-connection-inventory",
            "edge_kind": "deposited_connection_inventory",
            "support_status": "absent_from_deposited_struct_conn",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:1pwh-struct-conn"],
            "extracted_values": {
                "queried_component_id": "PLV",
                "attachment_context": "absent_from_deposited_struct_conn",
                "struct_conn_row_count": 26,
                "matching_component_row_count": 0,
                "connected_component_ids": ["ALA", "GLU", "GLY", "K", "LEU", "SER", "VAL"],
            },
        },
        {
            "edge_id": "edge:deposited-structure-state",
            "edge_kind": "deposited_structure_state",
            "support_status": "direct_structure_observation",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:1pwh-plv-instance"],
            "extracted_values": {
                "entity_context": entity["entity_context"],
                "entity_id": entity["entity_id"],
                "source_component_id": entity["source_component_id"],
                "source_description": entity["source_description"],
                "structure_instances": [instance],
            },
        },
        {
            "edge_id": "edge:primary-article-bound-adduct",
            "edge_kind": "primary_article_bound_adduct_description",
            "support_status": "source_described_bound_adduct",
            "source_binding_ids": [article_binding["binding_id"]],
            "locator_ids": ["locator:14596599-bound-adduct"],
            "extracted_values": {
                "source_component_id": "PLV",
                "chemical_context": "source_described_bound_adduct",
            },
        },
    ]
    projection = {
        "schema_version": "catalytic-earth.primary-observed-state-projection.v1",
        "projection_id": "primary-observed-state:M0186:1PWH:PLV",
        "context_id": "1pwh-plv-source-described-bound-adduct",
        "record_binding": _record_binding(record),
        "source_bindings": sorted(
            map(_projection_source, [cif_binding, article_binding]),
            key=lambda row: row["path"],
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": [instance],
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": reconciliation,
        "support_edges": edges,
        "locators": locators,
        "limits": [
            "The primary-source aldimine description and deposited sing bond-order token are not normalized into one chemical identity.",
            "Absence is confined to deposited struct_conn rows and does not assert physical noncovalency.",
        ],
    }
    claim = {
        "statement": "1PWH deposits PLV, while the primary abstract describes a PLP-OMS aldimine without dehydration; the relationship remains chemically unresolved.",
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": [instance],
        "site_crosswalk": crosswalk,
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": reconciliation,
        "direct_evidence_ids": ["evidence:14596599-article", "evidence:1pwh-cif"],
        "curated_identity_evidence_ids": [],
        "source_record_evidence_ids": [],
        "corroborating_evidence_ids": [],
        "observed_state_grounds_step": False,
    }
    annotation = {
        "annotation_id": "m0186.1pwh.plv-bound-adduct",
        "record_binding": _record_binding(record),
        "annotation_kind": "primary_observed_state_context",
        "target_scope": "record_only",
        "projection_binding": _projection_binding(projection),
        "projection_excerpt": {"support_edges": edges, "locators": locators},
        "claim": claim,
        "evidence": evidence,
        "limits": _limits(
            (
                "paper_deposit_chemical_reconciliation",
                "The paper description and deposited component bond order remain unreconciled.",
            ),
        ),
        "scope_effect": _scope_effect(),
    }
    sidecar = {
        "schema_version": "catalytic-earth.atlas-primary-evidence.v3",
        "annotation_set_id": "atlas-primary-evidence:plp-pyruvoyl:v3-test",
        "batch_id": "plp-pyruvoyl",
        "status": "reviewed_primary_evidence_annotations_not_mechanism_expansion",
        "source_bindings": sorted(
            [cif_binding, article_binding, project_binding], key=lambda row: row["path"]
        ),
        "annotations": [annotation],
        "review": _review(),
    }
    _materialize_projection(root, sidecar, projection)
    return bundle, sidecar, projection


class PrimaryObservedStateTests(unittest.TestCase):
    def test_projected_fixtures_validate_with_windows_text_line_endings(self) -> None:
        def write_crlf_json(path: Path, value: object) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = json.dumps(value, indent=2, sort_keys=True) + "\n"
            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))

        # Emulate Windows writes before the fixture computes any source pins.
        # Changing line endings only after pinning would miss the original bug.
        with patch(__name__ + "._write_json", side_effect=write_crlf_json):
            for fixture in (_m0049_fixture, _m0186_fixture, _m0213_fixture):
                with self.subTest(fixture=fixture.__name__), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    bundle, sidecar, _ = fixture(root)
                    result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
                    self.assertEqual(result["annotation_count"], 1)

    def test_existing_v1_annotation_is_preserved_and_schema_remains_accepted(self) -> None:
        bundle = _bundle()
        sidecar = json.loads(
            (
                REPO
                / "data/atlas/source_drafts/batches/plp-pyruvoyl/"
                "review/primary_evidence_annotations.json"
            ).read_text(encoding="utf-8")
        )
        before = copy.deepcopy(sidecar)
        result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=REPO)
        self.assertEqual(result["schema_version"], "catalytic-earth.atlas-primary-evidence.v3")
        self.assertEqual(sidecar, before)
        inherited = next(
            row
            for row in sidecar["annotations"]
            if row["annotation_id"] == "m0049.1pya.processed-pyruvoyl-site"
        )
        self.assertEqual(
            hashlib.sha256(
                json.dumps(
                    inherited,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest(),
            "bcb0dd4a591550b71659a4e6e64c58680f9f27ea6ef30e1fb3763f56e9407fd4",
        )

        legacy = copy.deepcopy(sidecar)
        legacy["schema_version"] = "catalytic-earth.atlas-primary-evidence.v1"
        legacy["annotation_set_id"] = "atlas-primary-evidence:plp-pyruvoyl:v1-test"
        legacy["source_bindings"] = [
            {"path": row["path"], "sha256": row["sha256"]}
            for row in sidecar["source_bindings"]
        ]
        legacy["annotations"] = [inherited]
        _repin(legacy)
        legacy_result = PRIMARY.validate_primary_evidence(
            legacy, bundle=bundle, repo_root=REPO
        )
        self.assertEqual(
            legacy_result["schema_version"], "catalytic-earth.atlas-primary-evidence.v1"
        )

    def test_existing_v2_sidecar_validates_without_mutation(self) -> None:
        from tests.core.test_atlas_primary_evidence import _valid_v2_sidecar

        bundle = json.loads(
            (REPO / "src/catalytic_earth/draft_data/aldolase_transketolase.json").read_text(
                encoding="utf-8"
            )
        )
        sidecar = _valid_v2_sidecar(bundle)
        before = copy.deepcopy(sidecar)
        result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=REPO)
        self.assertEqual(result["schema_version"], "catalytic-earth.atlas-primary-evidence.v2")
        self.assertEqual(sidecar, before)
        m0222 = next(row for row in sidecar["annotations"] if row["annotation_id"].startswith("m0222"))
        self.assertEqual(m0222, next(row for row in before["annotations"] if row["annotation_id"] == m0222["annotation_id"]))

    def test_m0049_exact_cross_source_edges_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0049_fixture(root)
            result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            self.assertEqual(result["annotation_count"], 1)
            self.assertEqual(result["record_ids"], [_record(bundle, "M0049")["record_id"]])

    def test_m0049_claim_tampering_fails_projection_or_source_binding(self) -> None:
        mutations = [
            ("PDB author position", lambda row: row["claim"]["structure_instances"][0].__setitem__("atom_author_residue_number", 1)),
            ("PDB label position", lambda row: row["claim"]["structure_instances"][0].__setitem__("label_seq_id", 82)),
            ("canonical Ser position", lambda row: row["claim"]["site_crosswalk"]["canonical_site"].__setitem__("sequence_position", 82)),
            ("author namespace mapping", lambda row: row["claim"]["site_crosswalk"].__setitem__("author_number_mapping_status", "source_supported")),
        ]
        for label, mutate in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                bundle, sidecar, _ = _m0049_fixture(root)
                mutate(sidecar["annotations"][0])
                _repin(sidecar)
                with self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0049_source_alias_cannot_be_rewritten_with_a_new_projection_pin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, projection = _m0049_fixture(root)
            crosswalk = sidecar["annotations"][0]["claim"]["site_crosswalk"]
            crosswalk["source_record_alias"]["author_position"] = 82
            projected = projection["site_crosswalk"]
            projected["source_record_alias"]["author_position"] = 82
            edge = next(
                row
                for row in projection["support_edges"]
                if row["edge_kind"] == "cross_source_correspondence"
            )
            edge["extracted_values"]["source_record_alias"]["author_position"] = 82
            _materialize_projection(root, sidecar, projection)
            with self.assertRaisesRegex(ValueError, "source structure alias differs"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0049_crosswalk_cannot_select_another_deposited_namespace(self) -> None:
        def change_chain(annotation: dict) -> None:
            instance = annotation["claim"]["structure_instances"][0]
            instance["label_asym_id"] = "B"
            instance["atom_author_chain_id"] = "B"
            annotation["claim"]["structure_context"]["protein_label_asym_ids"] = ["B"]
            annotation["claim"]["structure_context"]["protein_author_chain_ids"] = ["B"]

        mutations = [
            (change_chain, "differs from its source alias"),
            (
                lambda annotation: annotation["claim"]["structure_instances"][0].__setitem__(
                    "label_seq_id", 2
                ),
                "differs from its source alias",
            ),
            (
                lambda annotation: annotation["claim"]["structure_context"].__setitem__(
                    "pdb_id", "2PYA"
                ),
                "structure/source-alias PDB identity differs",
            ),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as temporary:
                bundle, sidecar, _ = _m0049_fixture(Path(temporary))
                mutate(sidecar["annotations"][0])
                _repin(sidecar)
                with self.assertRaisesRegex(ValueError, message):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

        with tempfile.TemporaryDirectory() as temporary:
            bundle, sidecar, _ = _m0049_fixture(Path(temporary))
            annotation = sidecar["annotations"][0]
            annotation["claim"]["structure_instances"][0]["label_asym_id"] = "B"
            annotation["claim"]["structure_context"]["protein_label_asym_ids"] = ["B"]
            _repin(sidecar)
            # The M-CSA chain field is an author-chain assertion. A separately
            # projected label-asym ID may differ without changing that edge.
            PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

    def test_curated_identity_cannot_replace_direct_structure_support(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0049_fixture(root)
            evidence = sidecar["annotations"][0]["evidence"]
            direct = next(row for row in evidence if row["evidence_role"] == "direct_support")
            direct["evidence_role"] = "curated_identity_support"
            sidecar["annotations"][0]["claim"]["direct_evidence_ids"] = []
            sidecar["annotations"][0]["claim"]["curated_identity_evidence_ids"].append(
                direct["evidence_id"]
            )
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "curated identity support"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0049_crosswalk_requires_curated_and_source_record_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0049_fixture(root)
            annotation = sidecar["annotations"][0]
            curated_id = annotation["claim"]["curated_identity_evidence_ids"][0]
            annotation["evidence"] = [row for row in annotation["evidence"] if row["evidence_id"] != curated_id]
            annotation["claim"]["curated_identity_evidence_ids"] = []
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "curated.*evidence"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0213_exact_nonpolymer_instances_and_analogue_scope_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0213_fixture(root)
            result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            self.assertEqual(result["record_ids"], [_record(bundle, "M0213")["record_id"]])

            runtime_result = PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)
            self.assertEqual(runtime_result, result)

    def test_m0213_instance_namespace_tampering_fails(self) -> None:
        mutations = [
            ("null label sequence", lambda row: row.__setitem__("label_seq_id", 1)),
            ("label asym", lambda row: row.__setitem__("label_asym_id", "C")),
            ("atom author number", lambda row: row.__setitem__("atom_author_residue_number", 390)),
            ("source author number", lambda row: row.__setitem__("source_author_residue_number", 1390)),
        ]
        for label, mutate in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                bundle, sidecar, _ = _m0213_fixture(root)
                mutate(sidecar["annotations"][0]["claim"]["structure_instances"][1])
                _repin(sidecar)
                with self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0213_aggregate_covalent_count_cannot_claim_pdd_connection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, projection = _m0213_fixture(root)
            edge = next(
                row
                for row in projection["support_edges"]
                if row["edge_kind"] == "deposited_connection_inventory"
            )
            edge["extracted_values"]["matching_component_row_count"] = 4
            edge["extracted_values"]["connected_component_ids"].append("PDD")
            _materialize_projection(root, sidecar, projection)
            with self.assertRaisesRegex(ValueError, "deposited connection inventory differs"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0213_analogue_requires_primary_article_edge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, projection = _m0213_fixture(root)
            projection["support_edges"] = [
                row
                for row in projection["support_edges"]
                if row["edge_kind"] != "primary_article_analogue_designation"
            ]
            sidecar["annotations"][0]["projection_excerpt"]["support_edges"] = (
                projection["support_edges"]
            )
            _materialize_projection(root, sidecar, projection)
            with self.assertRaisesRegex(ValueError, "cites unknown support edges"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0213_analogue_requires_primary_article_even_without_repository_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0213_fixture(root)
            annotation = sidecar["annotations"][0]
            annotation["evidence"] = [
                row
                for row in annotation["evidence"]
                if row["source_kind"] != "primary_research_article"
            ]
            annotation["claim"]["direct_evidence_ids"] = ["evidence:1l6g-cif"]
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "lacks direct primary-article evidence"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

    def test_observed_state_cannot_be_native_or_step_grounding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0213_fixture(root)
            sidecar["annotations"][0]["claim"]["observed_state_grounds_step"] = True
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "cannot ground a source step"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0213_fixture(root)
            sidecar["annotations"][0]["claim"]["observed_entity"]["state_kind"] = "native_intermediate"
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "state_kind is unsupported"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0186_preserves_article_and_deposit_chemistry_as_separate_observations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0186_fixture(root)
            result = PRIMARY.validate_primary_evidence(
                sidecar, bundle=bundle, repo_root=root
            )
            claim = sidecar["annotations"][0]["claim"]
            self.assertEqual(result["record_ids"], [_record(bundle, "M0186")["record_id"]])
            self.assertEqual(
                [row["source_scope"] for row in claim["chemical_observations"]],
                ["deposited_structure", "primary_research_article"],
            )
            self.assertEqual(
                claim["chemical_observations"][0]["source_bond_order_code"],
                "sing",
            )
            self.assertEqual(
                claim["chemical_reconciliation"]["status"],
                "unresolved_source_description_vs_deposit",
            )

    def test_m0186_article_and_deposit_evidence_edges_cannot_be_substituted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0186_fixture(root)
            observations = sidecar["annotations"][0]["claim"]["chemical_observations"]
            observations[0]["evidence_ids"] = ["evidence:14596599-article"]
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "deposited-structure evidence"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

        with tempfile.TemporaryDirectory() as temporary:
            bundle, sidecar, _ = _m0186_fixture(Path(temporary))
            excerpt = sidecar["annotations"][0]["projection_excerpt"]
            bond_edge = next(
                row
                for row in excerpt["support_edges"]
                if row["edge_kind"] == "deposited_component_bond_order"
            )
            bond_edge["source_binding_ids"] = [
                "projection:PubMed:14596599:abstract"
            ]
            bond_edge["locator_ids"] = ["locator:14596599-bound-adduct"]
            _repin(sidecar)
            with self.assertRaisesRegex(ValueError, "direct primary structure"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, projection = _m0186_fixture(root)
            bond_observation = sidecar["annotations"][0]["claim"]["chemical_observations"][0]
            bond_observation["source_bond_order_code"] = "doub"
            projection["chemical_observations"][0]["source_bond_order_code"] = "doub"
            sidecar["annotations"][0]["projection_excerpt"]["support_edges"] = projection[
                "support_edges"
            ]
            _materialize_projection(root, sidecar, projection)
            with self.assertRaisesRegex(ValueError, "bond-order observation differs"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_m0186_potassium_instance_count_cannot_replace_connection_row_count(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, projection = _m0186_fixture(root)
            connection = next(
                row
                for row in projection["support_edges"]
                if row["edge_kind"] == "deposited_connection_inventory"
            )
            connection["extracted_values"]["struct_conn_row_count"] = 4
            sidecar["annotations"][0]["projection_excerpt"]["support_edges"] = projection[
                "support_edges"
            ]
            _materialize_projection(root, sidecar, projection)
            with self.assertRaisesRegex(ValueError, "connection locator differs"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_projection_and_source_hash_tampering_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle, sidecar, _ = _m0213_fixture(root)
            path = root / "evidence/1L6G.cif"
            path.write_bytes(path.read_bytes() + b"\n# tamper\n")
            with self.assertRaisesRegex(ValueError, "source hash differs"):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_malformed_observed_state_values_fail_as_value_errors(self) -> None:
        mutations = [
            lambda annotation: annotation["claim"].__setitem__("observed_entity", None),
            lambda annotation: annotation["projection_excerpt"].__setitem__(
                "support_edges", None
            ),
            lambda annotation: annotation["claim"]["structure_instances"][0].__setitem__(
                "label_seq_id", "none"
            ),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as temporary:
                bundle, sidecar, _ = _m0213_fixture(Path(temporary))
                mutate(sidecar["annotations"][0])
                _repin(sidecar)
                with self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)


if __name__ == "__main__":
    unittest.main()
