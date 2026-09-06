from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from catalytic_earth import atlas_primary_evidence as PRIMARY
from catalytic_earth.canonical_hash import canonical_file_sha256


REPO = Path(__file__).resolve().parents[2]


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _source_file(root: Path, relative: str, content: bytes) -> dict:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {"path": relative, "sha256": canonical_file_sha256(path)}


def _binding(binding_id: str, artifact_kind: str, row: dict) -> dict:
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
    source_kind: str,
    source_id: str,
    binding: dict,
) -> dict:
    return {
        "evidence_id": evidence_id,
        "evidence_role": "direct_support",
        "source_kind": source_kind,
        "source_id": source_id,
        "uri": "https://example.invalid/" + evidence_id.replace(":", "/"),
        "citation": "Synthetic exact-locator fixture for " + source_id,
        "experimental_context": "Only the explicitly projected source wording is supported.",
        "source_binding_id": binding["binding_id"],
        "source_sha256": binding["sha256"],
    }


def _locator(
    locator_id: str,
    binding_id: str,
    extracted_values: dict,
) -> dict:
    return {
        "locator_id": locator_id,
        "source_binding_id": binding_id,
        "source_format": "mmcif" if "2qut" in binding_id else "json",
        "selector": {"fixture": locator_id},
        "physical_lines": [1],
        "extracted_values": extracted_values,
        "supports": locator_id.replace(":", " "),
    }


def _scope_effect() -> dict:
    return {
        "record_evidence_tier_changed": False,
        "allowed_operations_changed": False,
        "mechanism_scope_expanded": False,
        "source_step_trajectory_claimed": False,
        "proposal_applicability_claimed": False,
    }


def _review() -> dict:
    return {
        "reviewed_on": "2026-09-06",
        "annotation_payload_sha256": "0" * 64,
        "update_rule": PRIMARY.PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE,
        "reviewer_kind": PRIMARY.PRIMARY_EVIDENCE_REVIEWER_KIND,
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


def _endpoint_from_instance(instance: dict, atom_name: str) -> dict:
    return {
        "label_asym_id": instance["label_asym_id"],
        "label_entity_id": instance["label_entity_id"],
        "label_component_id": instance["label_component_id"],
        "label_seq_id": instance["label_seq_id"],
        "atom_author_chain_id": instance["atom_author_chain_id"],
        "atom_author_component_id": instance["atom_author_component_id"],
        "atom_author_residue_number": instance["atom_author_residue_number"],
        "atom_name": atom_name,
    }


def _edge_values(attachment: dict) -> dict:
    return {
        key: copy.deepcopy(attachment[key])
        for key in (
            "connection_id",
            "raw_conn_type",
            "observed_instance_index",
            "ligand_endpoint",
            "protein_endpoint",
            "distance_angstrom",
            "source_bond_order_code",
            "source_bond_order_token",
        )
    }


def _locator_values(attachment: dict) -> dict:
    result = _edge_values(attachment)
    result.pop("observed_instance_index")
    result.pop("source_bond_order_code")
    return result


def _fixture(root: Path) -> tuple[dict, dict, dict]:
    bundle = json.loads(
        (REPO / "src/catalytic_earth/draft_data/aldolase_transketolase.json").read_text(
            encoding="utf-8"
        )
    )
    record = next(row for row in bundle["records"] if row["mcsa_id"] == "M0222")
    record_binding = {
        "record_id": record["record_id"],
        "mcsa_id": "M0222",
        "source_snapshot_sha256": record["source"]["snapshot_sha256"],
    }

    cif_row = _source_file(root, "evidence/2QUT.cif", b"data_2QUT\n# exact source fixture\n")
    article_row = _source_file(
        root,
        "evidence/PMID_17728250_projection.json",
        b'{"source":"PubMed:17728250","scope":"source wording only"}\r\n',
    )
    projection_row = _source_file(root, "evidence/projection.json", b"{}\r\n")
    cif_binding = _binding("primary:RCSB:2QUT:mmCIF", "primary_source", cif_row)
    article_binding = _binding(
        "primary:PubMed:17728250:projection",
        "primary_source_projection",
        article_row,
    )
    project_binding = _binding(
        "project:M0222:2QUT:observed-state-projection",
        "project_projection",
        projection_row,
    )

    structure_context = {
        "pdb_id": "2QUT",
        "model_id": 1,
        "protein_entity_ids": ["1"],
        "protein_label_asym_ids": ["A", "B", "C", "D"],
        "protein_author_chain_ids": ["A", "B", "C", "D"],
        "curated_protein_accession": None,
    }
    entity = {
        "state_kind": "protein_ligand_covalent_adduct",
        "entity_context": "nonpolymer_component",
        "entity_id": "2",
        "source_component_id": "13P",
        "source_description": "1,3-DIHYDROXYACETONEPHOSPHATE",
        "chemical_context": "deposit_described_bound_intermediate",
        "attachment_context": "deposited_covalent_connection",
        "normalized_chebi_id": None,
    }
    instances = []
    for label_chain, author_chain, author_number, site_id in (
        ("E", "A", 3001, "AC1"),
        ("F", "B", 3002, "AC2"),
        ("G", "C", 3003, "AC3"),
        ("H", "D", 3004, "AC4"),
    ):
        instances.append(
            {
                "label_asym_id": label_chain,
                "label_entity_id": "2",
                "label_component_id": "13P",
                "label_seq_id": None,
                "atom_author_chain_id": author_chain,
                "atom_author_component_id": "13P",
                "atom_author_residue_number": author_number,
                "source_author_component_id": "13P",
                "source_author_residue_number": author_number,
                "structure_site_id": site_id,
            }
        )

    attachments = []
    for index, (instance, distance) in enumerate(
        zip(instances, (1.478, 1.477, 1.477, 1.479), strict=True)
    ):
        author_chain = instance["atom_author_chain_id"]
        attachments.append(
            {
                "attachment_id": f"attachment:2qut:{index + 1}",
                "connection_id": f"covale{index + 1}",
                "raw_conn_type": "covale",
                "observed_instance_index": index,
                "ligand_endpoint": _endpoint_from_instance(instance, "C2"),
                "protein_endpoint": {
                    "label_asym_id": author_chain,
                    "label_entity_id": "1",
                    "label_component_id": "LYS",
                    "label_seq_id": 229,
                    "atom_author_chain_id": author_chain,
                    "atom_author_component_id": "LYS",
                    "atom_author_residue_number": 229,
                    "atom_name": "NZ",
                },
                "distance_angstrom": distance,
                "source_bond_order_code": None,
                "source_bond_order_token": "?",
                "support_edge_ids": [f"edge:connection:covale{index + 1}"],
            }
        )

    evidence = [
        _evidence(
            "evidence:2qut-cif",
            "primary_structure_record",
            "RCSB PDB:2QUT",
            cif_binding,
        ),
        _evidence(
            "evidence:17728250-article-projection",
            "primary_research_article",
            "PubMed:17728250",
            article_binding,
        ),
    ]

    dictionary_values = {
        "source_component_id": "13P",
        "scope": "generic_component_dictionary",
        "source_atom_ids": ["C2", "O2"],
        "source_bond_order_code": "doub",
        "source_description": "The generic 13P dictionary records C2-O2 as doub.",
    }
    inventory_values = {
        "source_component_id": "13P",
        "scope": "modeled_deposited_instances",
        "modeled_instance_indices": [0, 1, 2, 3],
        "omitted_atom_ids": ["O2"],
        "source_description": "Every modeled 13P instance omits O2.",
    }
    deposit_description_values = {
        "source_component_id": "13P",
        "chemical_context": "deposit_described_bound_intermediate",
        "source_description": (
            "The 2QUT title and deposit remark describe a DHAP enamine intermediate."
        ),
    }
    article_description_values = {
        "source_component_id": "13P",
        "chemical_context": "source_described_bound_intermediate",
        "source_description": (
            "PMID 17728250 describes trapping an enamine at Lys229 in native aldolase."
        ),
    }
    structure_values = {
        "entity_context": entity["entity_context"],
        "entity_id": entity["entity_id"],
        "source_component_id": entity["source_component_id"],
        "source_description": entity["source_description"],
        "structure_instances": instances,
    }

    chemical_observations = [
        {
            "observation_id": "observation:component-dictionary-bond",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_component_dictionary_bond_order",
            "source_description": dictionary_values["source_description"],
            "source_bond_order_code": "doub",
            "source_atom_ids": ["C2", "O2"],
            "evidence_ids": ["evidence:2qut-cif"],
            "support_edge_ids": ["edge:component-dictionary-bond"],
        },
        {
            "observation_id": "observation:deposited-description",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_state_description",
            "source_description": deposit_description_values["source_description"],
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:2qut-cif"],
            "support_edge_ids": ["edge:deposited-description"],
        },
        {
            "observation_id": "observation:modeled-instance-inventory",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_modeled_instance_atom_inventory",
            "source_description": inventory_values["source_description"],
            "source_bond_order_code": None,
            "modeled_instance_indices": [0, 1, 2, 3],
            "omitted_atom_ids": ["O2"],
            "evidence_ids": ["evidence:2qut-cif"],
            "support_edge_ids": ["edge:modeled-instance-inventory"],
        },
        {
            "observation_id": "observation:primary-article-description",
            "source_scope": "primary_research_article",
            "observation_kind": "primary_article_state_description",
            "source_description": article_description_values["source_description"],
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:17728250-article-projection"],
            "support_edge_ids": ["edge:primary-article-description"],
        },
        {
            "observation_id": "observation:structure-state",
            "source_scope": "deposited_structure",
            "observation_kind": "deposited_component_state",
            "source_description": "2QUT deposits four 13P nonpolymer instances.",
            "source_bond_order_code": None,
            "evidence_ids": ["evidence:2qut-cif"],
            "support_edge_ids": ["edge:structure-state"],
        },
    ]

    locators = [
        _locator(
            "locator:component-dictionary-bond",
            cif_binding["binding_id"],
            dictionary_values,
        ),
        _locator(
            "locator:deposited-description",
            cif_binding["binding_id"],
            deposit_description_values,
        ),
        _locator(
            "locator:modeled-instance-inventory",
            cif_binding["binding_id"],
            inventory_values,
        ),
        _locator(
            "locator:primary-article-description",
            article_binding["binding_id"],
            article_description_values,
        ),
        _locator(
            "locator:structure-state",
            cif_binding["binding_id"],
            {"source_component_id": "13P", "instance_count": 4},
        ),
    ]
    for attachment in attachments:
        locators.append(
            _locator(
                "locator:" + attachment["connection_id"],
                cif_binding["binding_id"],
                _locator_values(attachment),
            )
        )

    edges = [
        {
            "edge_id": "edge:component-dictionary-bond",
            "edge_kind": "deposited_component_dictionary_bond_order",
            "support_status": "direct_structure_observation",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:component-dictionary-bond"],
            "extracted_values": dictionary_values,
        },
        {
            "edge_id": "edge:deposited-description",
            "edge_kind": "deposited_state_description",
            "support_status": "deposit_described_bound_intermediate",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:deposited-description"],
            "extracted_values": deposit_description_values,
        },
        {
            "edge_id": "edge:modeled-instance-inventory",
            "edge_kind": "deposited_modeled_instance_atom_inventory",
            "support_status": "direct_structure_observation",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:modeled-instance-inventory"],
            "extracted_values": inventory_values,
        },
        {
            "edge_id": "edge:primary-article-description",
            "edge_kind": "primary_article_bound_intermediate_description",
            "support_status": "source_described_bound_intermediate",
            "source_binding_ids": [article_binding["binding_id"]],
            "locator_ids": ["locator:primary-article-description"],
            "extracted_values": article_description_values,
        },
        {
            "edge_id": "edge:structure-state",
            "edge_kind": "deposited_structure_state",
            "support_status": "direct_structure_observation",
            "source_binding_ids": [cif_binding["binding_id"]],
            "locator_ids": ["locator:structure-state"],
            "extracted_values": structure_values,
        },
    ]
    for attachment in attachments:
        edges.append(
            {
                "edge_id": attachment["support_edge_ids"][0],
                "edge_kind": "deposited_covalent_connection",
                "support_status": "direct_structure_observation",
                "source_binding_ids": [cif_binding["binding_id"]],
                "locator_ids": ["locator:" + attachment["connection_id"]],
                "extracted_values": _edge_values(attachment),
            }
        )

    reconciliation = {
        "status": "unresolved_component_dictionary_vs_bound_instance_and_connection",
        "statement": (
            "Dictionary C2-O2 doub, modeled O2 omission, and connection order ? remain separate."
        ),
    }
    projection = {
        "schema_version": "catalytic-earth.primary-observed-state-projection.v1",
        "projection_id": "primary-observed-state:M0222:2QUT:13P",
        "context_id": "2qut-four-13p-lys229-connections",
        "record_binding": record_binding,
        "source_bindings": sorted(
            map(_projection_source, [cif_binding, article_binding]),
            key=lambda row: row["path"],
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": instances,
        "protein_attachments": attachments,
        "site_crosswalk": {
            "status": "not_asserted",
            "relationship": "not_asserted",
            "structure_instance_index": None,
            "canonical_site": None,
            "source_record_alias": None,
            "author_number_mapping_status": "not_asserted",
            "support_edge_ids": [],
        },
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": reconciliation,
        "support_edges": edges,
        "locators": locators,
        "limits": [
            "The deposit description is distinct from connection and bond-order facts.",
            "Generic dictionary C2-O2 doub is not assigned to modeled bound instances.",
        ],
    }
    claim = {
        "statement": (
            "2QUT deposits four 13P instances, each connected from C2 to a chain-matched "
            "Lys229 NZ; the deposit description and unknown connection order remain distinct."
        ),
        "structure_context": structure_context,
        "observed_entity": entity,
        "structure_instances": instances,
        "protein_attachments": attachments,
        "site_crosswalk": projection["site_crosswalk"],
        "chemical_observations": chemical_observations,
        "chemical_reconciliation": reconciliation,
        "direct_evidence_ids": [
            "evidence:2qut-cif",
            "evidence:17728250-article-projection",
        ],
        "curated_identity_evidence_ids": [],
        "source_record_evidence_ids": [],
        "corroborating_evidence_ids": [],
        "observed_state_grounds_step": False,
    }
    annotation = {
        "annotation_id": "m0222.2qut.four-chain-covalent-13p-context",
        "record_binding": record_binding,
        "annotation_kind": "primary_observed_state_context",
        "target_scope": "record_only",
        "claim": claim,
        "evidence": evidence,
        "limits": [
            {
                "limit_id": limit_id,
                "status": "abstained",
                "statement": statement,
            }
            for limit_id, statement in (
                ("bound_moiety_bond_order", "The deposited connection order is unknown."),
                (
                    "chemical_identity_beyond_source",
                    "No free ChEBI identity or protonation is assigned.",
                ),
                (
                    "component_dictionary_vs_modeled_instance",
                    "Generic 13P C2-O2 doub is not a modeled attachment bond.",
                ),
                ("exact_reaction_instance", "The exact reaction instance is unresolved."),
                ("mechanism_applicability", "No source proposal is validated."),
                ("state_trajectory", "No source step or trajectory is grounded."),
            )
        ],
        "scope_effect": _scope_effect(),
        "projection_binding": {
            "binding_id": project_binding["binding_id"],
            "projection_id": projection["projection_id"],
            "context_id": projection["context_id"],
        },
        "projection_excerpt": {"support_edges": edges, "locators": locators},
    }
    sidecar = {
        "schema_version": PRIMARY.PRIMARY_EVIDENCE_SCHEMA_VERSION,
        "annotation_set_id": "atlas-primary-evidence:aldolase-transketolase:v3-covalent-test",
        "batch_id": "aldolase-transketolase",
        "status": PRIMARY.PRIMARY_EVIDENCE_STATUS,
        "source_bindings": sorted(
            [cif_binding, article_binding, project_binding], key=lambda row: row["path"]
        ),
        "annotations": [annotation],
        "review": _review(),
    }
    projection_path = root / project_binding["path"]
    _write_json(projection_path, projection)
    project_binding["sha256"] = canonical_file_sha256(projection_path)
    _repin(sidecar)
    return bundle, sidecar, projection


def _rewrite_projection(root: Path, sidecar: dict, projection: dict) -> None:
    binding = next(
        row
        for row in sidecar["source_bindings"]
        if row["artifact_kind"] == "project_projection"
    )
    projection_path = root / binding["path"]
    _write_json(projection_path, projection)
    binding["sha256"] = canonical_file_sha256(projection_path)
    _repin(sidecar)


class PrimaryCovalentStateTests(unittest.TestCase):
    def test_exact_four_instance_connections_validate_and_preserve_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, _ = _fixture(root)
            result = PRIMARY.validate_primary_evidence(
                sidecar, bundle=bundle, repo_root=root
            )
            self.assertEqual(result["annotation_count"], 1)
            claim = sidecar["annotations"][0]["claim"]
            self.assertEqual(
                [row["connection_id"] for row in claim["protein_attachments"]],
                ["covale1", "covale2", "covale3", "covale4"],
            )
            self.assertTrue(
                all(row["source_bond_order_code"] is None for row in claim["protein_attachments"])
            )
            self.assertEqual(claim["site_crosswalk"]["status"], "not_asserted")
            self.assertFalse(claim["observed_state_grounds_step"])

    def test_unmirrored_swapped_chain_or_ligand_endpoint_is_rejected(self) -> None:
        for mutate in (
            lambda row: row["protein_endpoint"].__setitem__("atom_author_chain_id", "B"),
            lambda row: row["ligand_endpoint"].__setitem__("atom_author_residue_number", 3002),
            lambda row: row["ligand_endpoint"].__setitem__("label_asym_id", "F"),
        ):
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bundle, sidecar, _ = _fixture(root)
                mutate(sidecar["annotations"][0]["claim"]["protein_attachments"][0])
                _repin(sidecar)
                with self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

    def test_every_instance_requires_one_unique_connection(self) -> None:
        for mutation in ("drop", "duplicate_index", "reuse_edge"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bundle, sidecar, _ = _fixture(root)
                rows = sidecar["annotations"][0]["claim"]["protein_attachments"]
                if mutation == "drop":
                    rows.pop()
                elif mutation == "duplicate_index":
                    rows[1]["observed_instance_index"] = 0
                else:
                    rows[1]["support_edge_ids"] = rows[0]["support_edge_ids"][:]
                _repin(sidecar)
                with self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(sidecar, bundle=bundle)

    def test_global_connection_inventory_cannot_replace_instance_connections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, projection = _fixture(root)
            edge = next(
                row
                for row in projection["support_edges"]
                if row["edge_id"] == "edge:connection:covale1"
            )
            edge.update(
                {
                    "edge_kind": "deposited_connection_inventory",
                    "support_status": "absent_from_deposited_struct_conn",
                    "extracted_values": {
                        "queried_component_id": "PDD",
                        "attachment_context": "absent_from_deposited_struct_conn",
                        "struct_conn_row_count": 4,
                        "matching_component_row_count": 0,
                        "connected_component_ids": ["KCX", "LEU", "MET"],
                    },
                }
            )
            sidecar["annotations"][0]["projection_excerpt"]["support_edges"] = copy.deepcopy(
                projection["support_edges"]
            )
            _rewrite_projection(root, sidecar, projection)
            with self.assertRaises(ValueError):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_dictionary_double_and_omitted_o2_cannot_set_attachment_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, projection = _fixture(root)
            claim_attachment = sidecar["annotations"][0]["claim"]["protein_attachments"][0]
            projection_attachment = projection["protein_attachments"][0]
            for row in (claim_attachment, projection_attachment):
                row["source_bond_order_code"] = "doub"
                row["source_bond_order_token"] = "doub"
            connection_edge = next(
                row
                for row in projection["support_edges"]
                if row["edge_id"] == "edge:connection:covale1"
            )
            connection_edge["extracted_values"] = _edge_values(projection_attachment)
            connection_locator = next(
                row
                for row in projection["locators"]
                if row["locator_id"] == "locator:covale1"
            )
            connection_locator["extracted_values"] = _locator_values(projection_attachment)
            sidecar["annotations"][0]["projection_excerpt"] = {
                "support_edges": copy.deepcopy(projection["support_edges"]),
                "locators": copy.deepcopy(projection["locators"]),
            }
            _rewrite_projection(root, sidecar, projection)
            with self.assertRaises(ValueError):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_dictionary_and_modeled_instance_scopes_cannot_be_collapsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, projection = _fixture(root)
            observations = sidecar["annotations"][0]["claim"]["chemical_observations"]
            inventory = next(
                row
                for row in observations
                if row["observation_kind"] == "deposited_modeled_instance_atom_inventory"
            )
            inventory["omitted_atom_ids"] = ["N9"]
            projection["chemical_observations"] = copy.deepcopy(observations)
            inventory_edge = next(
                row
                for row in projection["support_edges"]
                if row["edge_kind"] == "deposited_modeled_instance_atom_inventory"
            )
            inventory_edge["extracted_values"]["omitted_atom_ids"] = ["N9"]
            inventory_locator = next(
                row
                for row in projection["locators"]
                if row["locator_id"] == "locator:modeled-instance-inventory"
            )
            inventory_locator["extracted_values"]["omitted_atom_ids"] = ["N9"]
            sidecar["annotations"][0]["projection_excerpt"] = {
                "support_edges": copy.deepcopy(projection["support_edges"]),
                "locators": copy.deepcopy(projection["locators"]),
            }
            _rewrite_projection(root, sidecar, projection)
            with self.assertRaises(ValueError):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_deposit_description_cannot_be_replaced_by_connectivity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, projection = _fixture(root)
            observations = sidecar["annotations"][0]["claim"]["chemical_observations"]
            observations[:] = [
                row for row in observations if row["observation_kind"] != "deposited_state_description"
            ]
            projection["chemical_observations"] = copy.deepcopy(observations)
            projection["support_edges"] = [
                row
                for row in projection["support_edges"]
                if row["edge_kind"] != "deposited_state_description"
            ]
            sidecar["annotations"][0]["projection_excerpt"]["support_edges"] = copy.deepcopy(
                projection["support_edges"]
            )
            _rewrite_projection(root, sidecar, projection)
            with self.assertRaises(ValueError):
                PRIMARY.validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)

    def test_covalent_context_remains_record_only_and_never_grounds_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle, sidecar, _ = _fixture(root)
            annotation = sidecar["annotations"][0]
            for field, value in (
                ("target_scope", "source_step"),
                ("observed_state_grounds_step", True),
            ):
                tampered = copy.deepcopy(sidecar)
                if field == "target_scope":
                    tampered["annotations"][0][field] = value
                else:
                    tampered["annotations"][0]["claim"][field] = value
                _repin(tampered)
                with self.subTest(field=field), self.assertRaises(ValueError):
                    PRIMARY.validate_primary_evidence(tampered, bundle=bundle)


if __name__ == "__main__":
    unittest.main()
