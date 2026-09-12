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
DEFAULT_PRIMARY_EVIDENCE_PATH = (
    ROOT / "data/atlas/atlas50/development_gate/primary_evidence_annotations.json"
)
RAW_2QUT = (
    "data/atlas/source_drafts/batches/aldolase-transketolase/"
    "review/primary_sources/2QUT.cif"
)
M0222_V1_ANNOTATION_SHA256 = (
    "b3ec318c98396833ade49cca3d811ef202066fa1c36ad8f60c4c1cb5f6cd9792"
)
CURRENT_PRIMARY_PAYLOAD_SHA256 = (
    "1a39745fe852e5cebb7b764d8d7f4969dadf80d57c4210e006c4c455fdbc9bbf"
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


def _source_chemical_identity_sidecar() -> dict:
    return json.loads(DEFAULT_PRIMARY_EVIDENCE_PATH.read_text(encoding="utf-8"))


def _valid_v2_sidecar(bundle: dict) -> dict:
    sidecar = verified_primary_evidence(
        "aldolase-transketolase", bundle=bundle
    )
    assert sidecar is not None
    sidecar = copy.deepcopy(sidecar)
    if sidecar["schema_version"] == "catalytic-earth.atlas-primary-evidence.v3":
        # Recover the exact earlier contract, including its original source
        # metadata, so new package contents cannot erase v2 regression coverage.
        sidecar["schema_version"] = "catalytic-earth.atlas-primary-evidence.v2"
        sidecar["annotation_set_id"] = "atlas-primary-evidence.aldolase-transketolase.2026-09-06.v2"
        sidecar["annotations"] = [a for a in sidecar["annotations"]
                                  if a["annotation_kind"] != "primary_observed_state_context"]
        for annotation in sidecar["annotations"]:
            annotation["limits"] = [limit for limit in annotation["limits"]
                                    if limit["limit_id"] != "mobile_catalyst_pose"]
        sidecar["source_bindings"] = [b for b in sidecar["source_bindings"]
                                     if "/observed_state_v3/" not in b["path"]
                                     and "/mobile_tail_20260909/" not in b["path"]]
        sidecar["review"]["reviewed_on"] = "2026-09-06"
        _repin(sidecar)
    assert sidecar["schema_version"] == "catalytic-earth.atlas-primary-evidence.v2"
    assert canonical_annotation_payload_sha256(sidecar) == (
        "575b0772268a6dd2b6e733d8e811eb9956c991fea6f88d0b167504594a4b2eb6"
    )
    return sidecar


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
            CURRENT_PRIMARY_PAYLOAD_SHA256,
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

    def test_default_package_has_reviewed_primary_evidence_sidecar(self):
        bundle = verified_source_drafts("default")
        sidecar = verified_primary_evidence("default", bundle=bundle)

        self.assertIsNotNone(sidecar)
        assert sidecar is not None
        self.assertEqual(
            sidecar["review"]["annotation_payload_sha256"],
            "6c4f586431a361a98d78174aef9f066e18eb2ede2fc58468044e6254197071b7",
        )

    def test_loader_retains_no_sidecar_fallback(self):
        expected = json.loads(core_cli._resource_bytes("draft_data/source_drafts_expected.json"))
        expected.pop("primary_evidence_sha256", None)
        expected_raw = json.dumps(expected).encode("utf-8")

        with patch("catalytic_earth.core_cli._resource_bytes", return_value=expected_raw):
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
            CURRENT_PRIMARY_PAYLOAD_SHA256,
        )
        annotation = next(a for a in result["records"][0]["primary_evidence_annotations"]
                          if a["annotation_id"] == "m0222.2qut.dhap-derived-covalent-moiety")
        self.assertIsNone(
            annotation["claim"]["observed_state"]["normalized_chebi_id"]
        )


class SourceChemicalIdentityQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = verified_source_drafts("default")
        cls.sidecar = _source_chemical_identity_sidecar()

    def test_validates_exact_source_step_atom_and_primary_projection(self):
        summary = validate_primary_evidence(
            self.sidecar,
            bundle=self.bundle,
            repo_root=ROOT,
        )

        self.assertEqual(summary["schema_version"], "catalytic-earth.atlas-primary-evidence.v4")
        self.assertEqual(summary["annotation_count"], 1)
        annotation = self.sidecar["annotations"][0]
        self.assertEqual(annotation["step_binding"]["source_step_id"], 12)
        self.assertEqual(
            annotation["source_chemistry_binding"],
            {
                "source_step_summary": (
                    "In a nucleophilic substitution reaction the cental nitrogen "
                    "atom of the cofactor reforms one of its bonds to the one of "
                    "the iron centres."
                ),
                "flow_id": "o52",
                "flow_endpoint": "source_point",
                "source_atom_ref": "m1.a83",
                "source_element": "N",
            },
        )
        self.assertFalse(annotation["claim"]["current_constraint_usable"])

    def test_query_attaches_qualification_to_exact_expanded_step(self):
        bundle_before = copy.deepcopy(self.bundle)
        sidecar_before = copy.deepcopy(self.sidecar)

        compact = query_source_drafts(
            self.bundle,
            mcsa_id="M0212",
            primary_evidence=self.sidecar,
        )
        expanded = query_source_drafts(
            self.bundle,
            mcsa_id="M0212",
            include_steps=True,
            primary_evidence=self.sidecar,
        )

        for result in (compact, expanded):
            self.assertEqual(
                result["schema_version"], "catalytic-earth.source-draft-query.v7"
            )
            self.assertEqual(result["source_chemical_identity_qualification_count"], 1)
            self.assertFalse(
                result["records"][0]["primary_evidence_annotations"][0]["claim"]
                ["current_constraint_usable"]
            )
            self.assertEqual(
                {binding["artifact_kind"] for binding in result["primary_evidence"]["source_bindings"]},
                {"primary_source_projection", "source_record_snapshot"},
            )
        self.assertNotIn("mechanism_steps", compact["records"][0]["mechanism_proposals"][0])
        steps = expanded["records"][0]["mechanism_proposals"][0]["mechanism_steps"]
        qualified_steps = [
            step for step in steps if "source_chemical_identity_qualifications" in step
        ]
        self.assertEqual([step["source_step_id"] for step in qualified_steps], [12])
        qualification = qualified_steps[0]["source_chemical_identity_qualifications"]
        self.assertEqual(qualification, self.sidecar["annotations"])
        flow = next(flow for flow in qualified_steps[0]["electron_flows"] if flow["flow_id"] == "o52")
        self.assertEqual(flow["source_point"]["atoms"][0]["source_atom_ref"], "m1.a83")
        self.assertEqual(flow["source_point"]["atoms"][0]["element"], "N")
        unaffected_flow = next(
            flow
            for flow in qualified_steps[0]["electron_flows"]
            if flow["flow_id"] == "o51"
        )
        self.assertEqual(
            unaffected_flow["source_point"]["atoms"][0],
            {
                "source_atom_ref": "m1.a34",
                "element": "N",
                "formal_charge": 1,
                "semantic_labels": ["chebi:17997"],
            },
        )
        self.assertEqual(self.bundle, bundle_before)
        self.assertEqual(self.sidecar, sidecar_before)

    def test_default_cli_compact_and_steps_expose_the_bound_qualification(self):
        outputs = []
        for extra_args in ([], ["--steps"]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["atlas-drafts", "--mcsa-id", "M0212", *extra_args])
            self.assertEqual(code, 0)
            outputs.append(json.loads(output.getvalue()))

        for result in outputs:
            self.assertEqual(result["source_chemical_identity_qualification_count"], 1)
            annotation = result["records"][0]["primary_evidence_annotations"][0]
            self.assertFalse(annotation["claim"]["current_constraint_usable"])
        steps = outputs[1]["records"][0]["mechanism_proposals"][0]["mechanism_steps"]
        step = next(step for step in steps if step["source_step_id"] == 12)
        self.assertFalse(
            step["source_chemical_identity_qualifications"][0]["claim"]
            ["current_constraint_usable"]
        )

    def test_rejects_stale_step_scheme_summary_atom_element_and_evidence_digest(self):
        mutations = (
            (
                "step",
                lambda row: row["step_binding"].__setitem__("source_step_id", 11),
                "step binding is absent or mixed",
            ),
            (
                "scheme",
                lambda row: row["step_binding"].__setitem__(
                    "source_scheme_sha256", "0" * 64
                ),
                "source scheme binding is stale",
            ),
            (
                "summary",
                lambda row: row["source_chemistry_binding"].__setitem__(
                    "source_step_summary", "changed"
                ),
                "source step summary is stale",
            ),
            (
                "atom",
                lambda row: row["source_chemistry_binding"].__setitem__(
                    "source_atom_ref", "m1.a34"
                ),
                "source atom binding is absent or mixed",
            ),
            (
                "element",
                lambda row: row["source_chemistry_binding"].__setitem__(
                    "source_element", "C"
                ),
                "source element differs",
            ),
            (
                "primary evidence digest",
                lambda row: row["evidence"][0].__setitem__("source_sha256", "0" * 64),
                "binding ID/hash pair differs",
            ),
        )
        for label, mutate, message in mutations:
            with self.subTest(label=label):
                sidecar = copy.deepcopy(self.sidecar)
                mutate(sidecar["annotations"][0])
                _repin(sidecar)
                with self.assertRaisesRegex(ValueError, message):
                    validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_coherent_wrong_flow_atom_without_reviewed_selector_change(self):
        sidecar = copy.deepcopy(self.sidecar)
        chemistry = sidecar["annotations"][0]["source_chemistry_binding"]
        chemistry["flow_id"] = "o51"
        chemistry["source_atom_ref"] = "m1.a34"
        _repin(sidecar)

        with self.assertRaisesRegex(
            ValueError,
            "source_depiction_target differs from the annotation selectors",
        ):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_coherent_wrong_flow_atom_and_excerpt_against_projection(self):
        sidecar = copy.deepcopy(self.sidecar)
        annotation = sidecar["annotations"][0]
        for chemistry in (
            annotation["source_chemistry_binding"],
            annotation["projection_excerpt"]["source_depiction_target"][
                "source_chemistry_binding"
            ],
        ):
            chemistry["flow_id"] = "o51"
            chemistry["source_atom_ref"] = "m1.a34"
        _repin(sidecar)

        with self.assertRaisesRegex(
            ValueError,
            "source depiction target differs from the reviewed excerpt",
        ):
            validate_primary_evidence(
                sidecar,
                bundle=self.bundle,
                repo_root=ROOT,
            )

    def test_rejects_reenabled_constraint_or_invented_correction(self):
        sidecar = copy.deepcopy(self.sidecar)
        sidecar["annotations"][0]["claim"]["current_constraint_usable"] = True
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "cannot expose the contradicted"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = copy.deepcopy(self.sidecar)
        sidecar["annotations"][0]["claim"]["primary_supported_element"] = "N"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "does not contradict"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = copy.deepcopy(self.sidecar)
        sidecar["annotations"][0]["claim"]["corrected_source_atom_ref"] = "m1.a83"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "fields differ"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

        sidecar = copy.deepcopy(self.sidecar)
        sidecar["annotations"][0]["limits"] = [
            limit
            for limit in sidecar["annotations"][0]["limits"]
            if limit["limit_id"] != "corrected_atom_mapping"
        ]
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "omit a required"):
            validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_projection_claim_drift_against_bound_repository_projection(self):
        mutations = (
            (
                "supported element",
                lambda annotation: (
                    annotation["claim"].__setitem__("primary_supported_element", "O"),
                    annotation["projection_excerpt"]["reported_system"].__setitem__(
                        "supported_element", "O"
                    ),
                ),
                "reported system differs from the reviewed excerpt",
            ),
            (
                "projection ID",
                lambda annotation: annotation["projection_binding"].__setitem__(
                    "projection_id", "primary:Spatzal2011:changed"
                ),
                "projection ID differs",
            ),
            (
                "finding locator",
                lambda annotation: annotation["projection_excerpt"][
                    "finding_locators"
                ][0].__setitem__("source_locator", "/changed"),
                "finding locators differ from the reviewed excerpt",
            ),
        )
        for label, mutate, message in mutations:
            with self.subTest(label=label):
                sidecar = copy.deepcopy(self.sidecar)
                mutate(sidecar["annotations"][0])
                _repin(sidecar)
                with self.assertRaisesRegex(ValueError, message):
                    validate_primary_evidence(
                        sidecar,
                        bundle=self.bundle,
                        repo_root=ROOT,
                    )

    def test_rejects_projection_source_id_or_uri_drift_portably(self):
        mutations = (
            ("source ID", "source_id", "PMID:99999999"),
            ("source URI", "uri", "https://example.invalid/article"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                sidecar = copy.deepcopy(self.sidecar)
                sidecar["annotations"][0]["evidence"][0][field] = value
                _repin(sidecar)
                with self.assertRaisesRegex(
                    ValueError,
                    "direct evidence source identity differs from the projection excerpt",
                ):
                    validate_primary_evidence(sidecar, bundle=self.bundle)

    def test_rejects_recomputed_projection_digest_against_repository_bytes(self):
        sidecar = copy.deepcopy(self.sidecar)
        projection_binding = next(
            binding
            for binding in sidecar["source_bindings"]
            if binding["artifact_kind"] == "primary_source_projection"
        )
        projection_binding["sha256"] = "0" * 64
        sidecar["annotations"][0]["evidence"][0]["source_sha256"] = "0" * 64
        _repin(sidecar)

        with self.assertRaisesRegex(ValueError, "source hash differs"):
            validate_primary_evidence(
                sidecar,
                bundle=self.bundle,
                repo_root=ROOT,
            )


if __name__ == "__main__":
    unittest.main()
