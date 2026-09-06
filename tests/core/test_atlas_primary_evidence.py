from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli
from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.atlas_primary_evidence import (
    PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE,
    canonical_annotation_payload_sha256,
    validate_primary_evidence,
)
from catalytic_earth.canonical_hash import canonical_file_sha256
from catalytic_earth.core_cli import main, verified_primary_evidence, verified_source_drafts


ROOT = Path(__file__).resolve().parents[2]
RAW_2QUT = (
    "data/atlas/source_drafts/batches/aldolase-transketolase/"
    "review/primary_sources/2QUT.cif"
)
M0222_V1_ANNOTATION_SHA256 = (
    "b3ec318c98396833ade49cca3d811ef202066fa1c36ad8f60c4c1cb5f6cd9792"
)


def _valid_sidecar(bundle: dict) -> dict:
    record = next(item for item in bundle["records"] if item["mcsa_id"] == "M0222")
    source_sha256 = canonical_file_sha256(ROOT / RAW_2QUT)
    sidecar = {
        "schema_version": "catalytic-earth.atlas-primary-evidence.v1",
        "annotation_set_id": "atlas-primary-evidence:aldolase-transketolase:v1",
        "batch_id": "aldolase-transketolase",
        "status": "reviewed_primary_evidence_annotations_not_mechanism_expansion",
        "source_bindings": [
            {"path": RAW_2QUT, "sha256": source_sha256},
        ],
        "annotations": [
            {
                "annotation_id": "primary-observation:m0222:2qut-dhap-enamine",
                "record_binding": {
                    "record_id": record["record_id"],
                    "mcsa_id": record["mcsa_id"],
                    "source_snapshot_sha256": record["source"]["snapshot_sha256"],
                },
                "annotation_kind": "primary_structure_observation",
                "target_scope": "record_only",
                "claim": {
                    "statement": (
                        "2QUT directly supports a covalently bound DHAP-derived "
                        "enamine at rabbit aldolase author Lys229."
                    ),
                    "observed_state": {
                        "description": "covalently bound DHAP-derived enamine",
                        "identity_scope": "structure_bound_adduct_source_description",
                        "normalized_chebi_id": None,
                    },
                    "structure_site": {
                        "pdb_id": "2QUT",
                        "chain_id": "A",
                        "author_residue_name": "LYS",
                        "author_residue_number": 229,
                    },
                    "sequence_mapping": {
                        "status": "source_supported",
                        "uniprot_id": "P00883",
                        "sequence_position": 230,
                        "evidence_ids": ["evidence:2qut-cif"],
                    },
                    "direct_evidence_ids": ["evidence:2qut-cif"],
                    "corroborating_evidence_ids": ["evidence:1j4e-citation"],
                },
                "evidence": [
                    {
                        "evidence_id": "evidence:2qut-cif",
                        "evidence_role": "direct_support",
                        "source_kind": "primary_structure_record",
                        "source_id": "RCSB:2QUT",
                        "uri": "https://files.rcsb.org/download/2QUT.cif",
                        "citation": "RCSB PDB 2QUT",
                        "experimental_context": (
                            "Rabbit muscle aldolase structure containing a bound "
                            "DHAP-derived enamine."
                        ),
                        "source_sha256": source_sha256,
                    },
                    {
                        "evidence_id": "evidence:1j4e-citation",
                        "evidence_role": "corroboration_only",
                        "source_kind": "primary_structure_record",
                        "source_id": "RCSB:1J4E",
                        "uri": "https://www.rcsb.org/structure/1J4E",
                        "citation": "RCSB PDB 1J4E",
                        "experimental_context": (
                            "Separate engineered, reductively trapped rabbit "
                            "aldolase structure cited only as corroboration."
                        ),
                        "source_sha256": None,
                    },
                ],
                "limits": [
                    {
                        "limit_id": "bound_adduct_free_species_equivalence",
                        "status": "abstained",
                        "statement": (
                            "The bound adduct is not asserted to be a free ChEBI "
                            "participant."
                        ),
                    },
                    {
                        "limit_id": "full_source_step_trajectory",
                        "status": "abstained",
                        "statement": (
                            "The observation does not establish the full M-CSA "
                            "Step 1 trajectory."
                        ),
                    },
                    {
                        "limit_id": "protein_wide_proposal_applicability",
                        "status": "abstained",
                        "statement": (
                            "The observation does not establish protein-wide "
                            "applicability of the proposal."
                        ),
                    },
                    {
                        "limit_id": "source_prose_scheme_conflicts",
                        "status": "under_review",
                        "statement": (
                            "M-CSA prose and scheme substrate conflicts remain "
                            "unresolved."
                        ),
                    },
                ],
                "scope_effect": {
                    "record_evidence_tier_changed": False,
                    "allowed_operations_changed": False,
                    "mechanism_scope_expanded": False,
                    "source_step_trajectory_claimed": False,
                    "proposal_applicability_claimed": False,
                },
            },
        ],
        "review": {
            "reviewed_on": "2026-09-05",
            "annotation_payload_sha256": "0" * 64,
            "update_rule": PRIMARY_EVIDENCE_REVIEW_UPDATE_RULE,
            "reviewer_kind": "same_model_computational_agents",
            "same_model_agents": True,
            "blind_review": False,
            "statistically_independent": False,
            "correlated_error_risk": True,
            "human_reviewers": 0,
            "domain_expert_review_claimed": False,
        },
    }
    sidecar["review"]["annotation_payload_sha256"] = (
        canonical_annotation_payload_sha256(sidecar)
    )
    return sidecar


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()


def _repin(sidecar: dict) -> None:
    sidecar["review"]["annotation_payload_sha256"] = (
        canonical_annotation_payload_sha256(sidecar)
    )


def _valid_v2_sidecar(bundle: dict) -> dict:
    sidecar = verified_primary_evidence(
        "aldolase-transketolase", bundle=bundle
    )
    assert sidecar is not None
    assert sidecar["schema_version"] == "catalytic-earth.atlas-primary-evidence.v2"
    return copy.deepcopy(sidecar)


class PrimaryEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = verified_source_drafts("aldolase-transketolase")

    def test_validates_exact_source_and_review_bindings(self):
        sidecar = _valid_sidecar(self.bundle)

        result = validate_primary_evidence(
            sidecar, bundle=self.bundle, repo_root=ROOT
        )

        self.assertEqual(result["annotation_count"], 1)
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["record_ids"], [
            "atlas50-draft:m0222:source-scoped-mechanism-draft"
        ])
        self.assertEqual(
            result["annotation_payload_sha256"],
            sidecar["review"]["annotation_payload_sha256"],
        )

    def test_v2_validates_proposal_context_and_preserves_the_v1_annotation(self):
        sidecar = _valid_v2_sidecar(self.bundle)

        summary = validate_primary_evidence(
            sidecar, bundle=self.bundle, repo_root=ROOT
        )

        self.assertEqual(summary["annotation_count"], 2)
        self.assertEqual(
            [annotation["record_binding"]["mcsa_id"] for annotation in sidecar["annotations"]],
            ["M0219", "M0222"],
        )
        self.assertEqual(
            _canonical_sha256(sidecar["annotations"][1]),
            M0222_V1_ANNOTATION_SHA256,
        )

    def test_v2_rejects_wrong_proposal_or_compiled_reference(self):
        for field, value, message in (
            ("source_mechanism_id", 1, "proposal ID differs"),
            ("reference_pubmed_id", "9398292", "proposal reference PMID is absent"),
        ):
            with self.subTest(field=field):
                sidecar = _valid_v2_sidecar(self.bundle)
                sidecar["annotations"][0]["proposal_binding"][field] = value
                _repin(sidecar)
                with self.assertRaisesRegex(ValueError, message):
                    validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_v2_rejects_site_mapping_that_differs_from_bound_projection(self):
        sidecar = _valid_v2_sidecar(self.bundle)
        sidecar["annotations"][0]["claim"]["site_mappings"][0][
            "uniprot_sequence_position"
        ] = 999
        _repin(sidecar)

        with self.assertRaisesRegex(ValueError, "site mappings differ"):
            validate_primary_evidence(sidecar, bundle=self.bundle, repo_root=ROOT)

    def test_v2_rejects_wrong_paper_identity_and_artifact_binding(self):
        sidecar = _valid_v2_sidecar(self.bundle)
        paper = sidecar["annotations"][0]["evidence"][1]
        paper["source_id"] = "PubMed:33828999"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "lacks unique direct"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = _valid_v2_sidecar(self.bundle)
        paper = sidecar["annotations"][0]["evidence"][1]
        structure_binding = next(
            binding
            for binding in sidecar["source_bindings"]
            if binding["binding_id"] == "primary:RCSB:4KXV:mmCIF"
        )
        paper["source_binding_id"] = structure_binding["binding_id"]
        paper["source_sha256"] = structure_binding["sha256"]
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "paper evidence binding lacks a PMID locator"):
            validate_primary_evidence(sidecar, bundle=self.bundle, repo_root=ROOT)

    def test_v2_requires_nonexpanding_support_scope_and_limits(self):
        sidecar = _valid_v2_sidecar(self.bundle)
        sidecar["annotations"][0]["claim"]["support_scope"]["residue_roles"] = (
            "experimentally_validated"
        )
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "support scope overclaims"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = _valid_v2_sidecar(self.bundle)
        sidecar["annotations"][0]["limits"] = sidecar["annotations"][0]["limits"][1:]
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "required proposal-context boundary"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_v2_query_finds_protein_context_without_mutating_inputs(self):
        sidecar = _valid_v2_sidecar(self.bundle)
        before_bundle = copy.deepcopy(self.bundle)
        before_sidecar = copy.deepcopy(sidecar)

        result = query_source_drafts(
            self.bundle, text="P29401", primary_evidence=sidecar
        )

        self.assertEqual([record["mcsa_id"] for record in result["records"]], ["M0219"])
        annotation = result["records"][0]["primary_evidence_annotations"][0]
        self.assertEqual(annotation["proposal_binding"]["source_mechanism_id"], 2)
        self.assertEqual(
            annotation["claim"]["support_scope"]["residue_roles"],
            "computational_only",
        )
        self.assertEqual(self.bundle, before_bundle)
        self.assertEqual(sidecar, before_sidecar)

    def test_rejects_stale_record_source_binding(self):
        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["record_binding"]["source_snapshot_sha256"] = (
            "0" * 64
        )
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )

        with self.assertRaisesRegex(ValueError, "source snapshot binding is stale"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_claim_edit_without_new_review(self):
        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["claim"]["statement"] += " Changed."

        with self.assertRaisesRegex(ValueError, "reviewed annotation payload changed"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_unbound_direct_evidence_and_missing_bound_file(self):
        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["evidence"][0]["source_sha256"] = "1" * 64
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )
        with self.assertRaisesRegex(ValueError, "unbound source digest"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = _valid_sidecar(self.bundle)
        sidecar["source_bindings"][0]["path"] = RAW_2QUT + ".missing"
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )
        with self.assertRaisesRegex(ValueError, r"source_bindings\[0\] is missing"):
            validate_primary_evidence(sidecar, bundle=self.bundle, repo_root=ROOT)

    def test_rejects_cross_platform_absolute_and_traversal_paths(self):
        for invalid_path in (
            "/tmp/2QUT.cif",
            "../2QUT.cif",
            r"review\primary_sources\2QUT.cif",
            r"C:\review\2QUT.cif",
            "C:/review/2QUT.cif",
            "review//primary_sources/2QUT.cif",
        ):
            with self.subTest(path=invalid_path):
                sidecar = _valid_sidecar(self.bundle)
                sidecar["source_bindings"][0]["path"] = invalid_path
                sidecar["review"]["annotation_payload_sha256"] = (
                    canonical_annotation_payload_sha256(sidecar)
                )
                with self.assertRaisesRegex(ValueError, "repository-relative"):
                    validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_free_species_identity_and_scope_promotion(self):
        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["claim"]["observed_state"][
            "normalized_chebi_id"
        ] = "CHEBI:57642"
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )
        with self.assertRaisesRegex(ValueError, "free ChEBI participant"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["scope_effect"][
            "source_step_trajectory_claimed"
        ] = True
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )
        with self.assertRaisesRegex(ValueError, "attempts to expand"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_independence_and_human_review_overclaims(self):
        for field, value, message in (
            ("same_model_agents", False, "same-model"),
            ("blind_review", True, "informed"),
            ("statistically_independent", True, "statistical independence"),
            ("correlated_error_risk", False, "correlated-error"),
            ("human_reviewers", 1, "human review"),
            ("domain_expert_review_claimed", True, "domain-expert"),
        ):
            with self.subTest(field=field):
                sidecar = _valid_sidecar(self.bundle)
                sidecar["review"][field] = value
                with self.assertRaisesRegex(ValueError, message):
                    validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_supported_sequence_mapping_requires_direct_evidence(self):
        sidecar = _valid_sidecar(self.bundle)
        sidecar["annotations"][0]["claim"]["sequence_mapping"]["evidence_ids"] = [
            "evidence:1j4e-citation"
        ]
        sidecar["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(sidecar)
        )

        with self.assertRaisesRegex(ValueError, "requires direct evidence"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_packaged_loader_returns_the_reviewed_annotation(self):
        sidecar = verified_primary_evidence(
            "aldolase-transketolase", bundle=self.bundle
        )

        self.assertIsNotNone(sidecar)
        assert sidecar is not None
        self.assertEqual(
            sidecar["review"]["annotation_payload_sha256"],
            "575b0772268a6dd2b6e733d8e811eb9956c991fea6f88d0b167504594a4b2eb6",
        )
        packaged_raw = core_cli._resource_bytes(
            "draft_data/aldolase_transketolase_primary_evidence.json"
        )
        expected = json.loads(
            core_cli._resource_bytes(
                "draft_data/aldolase_transketolase_expected.json"
            )
        )
        self.assertEqual(
            hashlib.sha256(packaged_raw).hexdigest(),
            expected["primary_evidence_sha256"],
        )
        validate_primary_evidence(sidecar, bundle=self.bundle, repo_root=ROOT)

    def test_source_binding_edits_require_review_and_deterministic_order(self):
        sidecar = verified_primary_evidence(
            "aldolase-transketolase", bundle=self.bundle
        )
        assert sidecar is not None
        changed = copy.deepcopy(sidecar)
        changed["source_bindings"][0]["sha256"] = "1" * 64
        with self.assertRaisesRegex(ValueError, "reviewed annotation payload changed"):
            validate_primary_evidence(changed, bundle=self.bundle)

        reordered = copy.deepcopy(sidecar)
        reordered["source_bindings"] = list(reversed(reordered["source_bindings"]))
        reordered["review"]["annotation_payload_sha256"] = (
            canonical_annotation_payload_sha256(reordered)
        )
        with self.assertRaisesRegex(ValueError, "unique and sorted"):
            validate_primary_evidence(reordered, bundle=self.bundle)

    def test_packaged_loader_rejects_bytes_outside_the_package_pin(self):
        original = core_cli._resource_bytes

        def changed_resource(relative_path: str) -> bytes:
            raw = original(relative_path)
            if relative_path == "draft_data/aldolase_transketolase_primary_evidence.json":
                return raw + b" "
            return raw

        with patch(
            "catalytic_earth.core_cli._resource_bytes", side_effect=changed_resource
        ), self.assertRaisesRegex(ValueError, "primary evidence package differs"):
            verified_primary_evidence("aldolase-transketolase", bundle=self.bundle)

    def test_default_package_has_no_primary_evidence_sidecar(self):
        self.assertIsNone(verified_primary_evidence("default"))

    def test_sidecar_cannot_be_applied_to_another_bundle(self):
        sidecar = _valid_sidecar(self.bundle)

        with self.assertRaisesRegex(ValueError, "sidecar batch/bundle differs"):
            validate_primary_evidence(
                sidecar, bundle=verified_source_drafts("default")
            )

    def test_query_sidecar_is_additive_searchable_and_nonmutating(self):
        sidecar = _valid_sidecar(self.bundle)
        before_bundle = copy.deepcopy(self.bundle)
        before_sidecar = copy.deepcopy(sidecar)

        without = query_source_drafts(self.bundle, mcsa_id="M0222")
        compact = query_source_drafts(
            self.bundle, mcsa_id="M0222", primary_evidence=sidecar
        )
        full = query_source_drafts(
            self.bundle,
            mcsa_id="M0222",
            include_steps=True,
            primary_evidence=sidecar,
        )
        searched = query_source_drafts(
            self.bundle, text="DHAP-derived enamine", primary_evidence=sidecar
        )

        self.assertEqual(without["schema_version"], "catalytic-earth.source-draft-query.v1")
        self.assertNotIn("primary_evidence", without)
        self.assertNotIn("primary_evidence_annotations", without["records"][0])
        self.assertEqual(compact["schema_version"], "catalytic-earth.source-draft-query.v2")
        additive = copy.deepcopy(compact)
        additive["schema_version"] = "catalytic-earth.source-draft-query.v1"
        additive.pop("primary_evidence")
        for record in additive["records"]:
            record.pop("primary_evidence_annotations")
        self.assertEqual(additive, without)
        self.assertEqual(
            compact["records"][0]["primary_evidence_annotations"],
            full["records"][0]["primary_evidence_annotations"],
        )
        self.assertEqual([record["mcsa_id"] for record in searched["records"]], ["M0222"])
        self.assertEqual(self.bundle, before_bundle)
        self.assertEqual(sidecar, before_sidecar)

    def test_query_keeps_unannotated_records_with_empty_annotation_lists(self):
        result = query_source_drafts(
            self.bundle, mcsa_id="M0052", primary_evidence=_valid_sidecar(self.bundle)
        )

        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["records"][0]["primary_evidence_annotations"], [])

    def test_cli_loads_primary_evidence_and_searches_its_text(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(
                [
                    "atlas-drafts",
                    "--batch",
                    "aldolase-transketolase",
                    "--text",
                    "DHAP-derived covalent moiety",
                ]
            )
        result = json.loads(output.getvalue())

        self.assertEqual(code, 0)
        self.assertEqual(result["schema_version"], "catalytic-earth.source-draft-query.v2")
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["records"][0]["mcsa_id"], "M0222")
        self.assertEqual(
            result["primary_evidence"]["annotation_payload_sha256"],
            "575b0772268a6dd2b6e733d8e811eb9956c991fea6f88d0b167504594a4b2eb6",
        )
        annotation = result["records"][0]["primary_evidence_annotations"][0]
        self.assertIsNone(
            annotation["claim"]["observed_state"]["normalized_chebi_id"]
        )


if __name__ == "__main__":
    unittest.main()
