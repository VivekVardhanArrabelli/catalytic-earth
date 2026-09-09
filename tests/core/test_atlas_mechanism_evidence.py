from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_mechanism_evidence import (
    canonical_mechanism_evidence_payload_sha256,
    query_mechanism_evidence,
    validate_mechanism_evidence,
)
from catalytic_earth.atlas_transformation_sites import query_transformation_sites
from catalytic_earth.atlas_evidence_source_context import (
    audit_deposited_annotation, build_source_contexts, canonical_bytes,
    query_source_contexts, validate_source_contexts,
)
from scripts.build_atlas_mechanism_evidence import validate_source_projections


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "data/atlas/mechanism_evidence/m0187/evidence.json"
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"
TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0187/transformations.json"


def _observation(value: dict, observation_id: str) -> dict:
    return next(
        row
        for row in value["cases"][0]["observations"]
        if row["observation_id"] == observation_id
    )


def _repin(value: dict) -> None:
    value["review"]["evidence_payload_sha256"] = (
        canonical_mechanism_evidence_payload_sha256(value)
    )


class MechanismEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.value = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))
        self.transformations = {
            "M0187": json.loads(TRANSFORMATIONS.read_text(encoding="utf-8"))
        }

    def validate(self, value: dict | None = None) -> dict:
        return validate_mechanism_evidence(
            self.value if value is None else value,
            atlas10_bundle=self.atlas10,
            transformation_values=self.transformations,
        )

    def query(self, **filters) -> dict:
        return query_mechanism_evidence(
            self.value,
            atlas10_bundle=self.atlas10,
            transformation_values=self.transformations,
            **filters,
        )

    def test_exact_endpoint_evidence_keeps_censoring_direction_and_comparators(self):
        summary = self.validate()
        self.assertEqual((summary["case_count"], summary["observation_count"]), (1, 6))

        racemization = _observation(self.value, "H297N-racemization")
        self.assertEqual(racemization["endpoint"]["net_direction"], None)
        self.assertEqual(racemization["conditions"], [])
        self.assertEqual(
            racemization["result"],
            {
                "detection_limit": None,
                "detection_limit_unit": None,
                "reported_relation": None,
                "result_class": "not_detected",
                "unit": None,
                "value": None,
            },
        )

        s_exchange = _observation(self.value, "H297N-S-exchange")
        r_exchange = _observation(self.value, "H297N-R-exchange")
        self.assertEqual(
            [(row["name"], row["value"], row["unit"]) for row in s_exchange["conditions"]],
            [("pD", 7.5, None), ("solvent", "D2O", None)],
        )
        self.assertEqual(r_exchange["conditions"], s_exchange["conditions"])
        self.assertIsNone(s_exchange["endpoint"]["net_direction"])
        self.assertIsNone(r_exchange["endpoint"]["net_direction"])
        self.assertEqual(
            (s_exchange["result"]["value"], s_exchange["comparator_variant_id"]),
            (3.3, "WT"),
        )
        self.assertEqual(r_exchange["result"]["result_class"], "not_detected")

        structure = _observation(self.value, "H297N-structure")
        self.assertEqual(structure["substrate"], {"name": None, "identifier": None, "enantiomer": None})
        self.assertIsNone(structure["comparator_variant_id"])
        self.assertEqual(structure["result"]["result_class"], "no_detectable_difference")

        expected_k166r = {
            "K166R-R-to-S-turnover": ("R", "R_to_S", 5000),
            "K166R-S-to-R-turnover": ("S", "S_to_R", 1000),
        }
        for observation_id, expected in expected_k166r.items():
            with self.subTest(observation_id=observation_id):
                row = _observation(self.value, observation_id)
                self.assertEqual(
                    (row["substrate"]["enantiomer"], row["endpoint"]["net_direction"], row["result"]["value"]),
                    expected,
                )
                self.assertIsNone(row["comparator_variant_id"])
                self.assertEqual(
                    row["result"]["reported_relation"],
                    "fold_reduction_reference_unspecified_in_inspected_abstract",
                )

    def test_source_projection_gate_binds_all_six_typed_observations(self):
        self.assertEqual(
            validate_source_projections(self.value, repo_root=ROOT),
            {
                "request_count": 2,
                "response_bytes": 16968,
                "raw_abstract_witnesses_checked": False,
            },
        )
        case = self.value["cases"][0]
        self.assertEqual(
            {
                row["evidence_id"]: (row["applicability"], row["source_completeness"])
                for row in case["evidence_references"]
            },
            {
                "paper:PMID:1909893": ("direct", "abstract_truncated"),
                "paper:PMID:7893690": ("contextual", "abstract_truncated"),
            },
        )

    def test_query_filters_observations_but_preserves_the_complete_case(self):
        baseline = copy.deepcopy(self.value)
        expected = {
            (): (1, 6),
            (("variant", "H297N"),): (1, 4),
            (("variant", "K166R"),): (1, 2),
            (("endpoint", "turnover"),): (1, 3),
            (("endpoint", "isotope_exchange"),): (1, 2),
            (("variant", "K166R"), ("endpoint", "structure")): (0, 0),
        }
        for filter_items, counts in expected.items():
            with self.subTest(filters=filter_items):
                result = self.query(**dict(filter_items))
                self.assertEqual((result["case_count"], result["matched_observation_count"]), counts)

        result = self.query(variant="h297n", endpoint="ISOTOPE_EXCHANGE")
        [match] = result["matches"]
        self.assertEqual(
            match["matched_observation_ids"],
            ["H297N-S-exchange", "H297N-R-exchange"],
        )
        self.assertEqual(match["case"]["adjudication"], self.value["cases"][0]["adjudication"])
        self.assertFalse(result["query_semantics"]["nondetection_is_numeric_zero"])
        self.assertFalse(result["query_semantics"]["upstream_transformation_or_site_evidence_changed"])

        match["case"]["observations"].clear()
        match["matched_observations"][0]["result"]["value"] = 999
        result["source_bindings"].clear()
        self.assertEqual(self.value, baseline)

    def test_result_and_direction_types_cannot_promote_nondetection_or_exchange(self):
        mutations = []

        numeric_zero = copy.deepcopy(self.value)
        _observation(numeric_zero, "H297N-racemization")["result"].update(
            {"value": 0, "unit": "s-1"}
        )
        mutations.append(numeric_zero)

        directional_exchange = copy.deepcopy(self.value)
        _observation(directional_exchange, "H297N-S-exchange")["endpoint"]["net_direction"] = "S_to_R"
        mutations.append(directional_exchange)

        unnamed_wt = copy.deepcopy(self.value)
        _observation(unnamed_wt, "K166R-R-to-S-turnover")["comparator_variant_id"] = "WT"
        mutations.append(unnamed_wt)

        missing_wt = copy.deepcopy(self.value)
        _observation(missing_wt, "H297N-S-exchange")["comparator_variant_id"] = None
        mutations.append(missing_wt)

        for index, changed in enumerate(mutations):
            with self.subTest(index=index):
                _repin(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)

    def test_source_projection_rejects_coherent_but_unsupported_fact_changes(self):
        mutations = []

        copied_conditions = copy.deepcopy(self.value)
        _observation(copied_conditions, "H297N-racemization")["conditions"] = copy.deepcopy(
            _observation(copied_conditions, "H297N-S-exchange")["conditions"]
        )
        mutations.append(copied_conditions)

        swapped_enantiomer = copy.deepcopy(self.value)
        _observation(swapped_enantiomer, "H297N-S-exchange")["substrate"]["enantiomer"] = "R"
        mutations.append(swapped_enantiomer)

        swapped_direction = copy.deepcopy(self.value)
        _observation(swapped_direction, "K166R-R-to-S-turnover")["endpoint"]["net_direction"] = "S_to_R"
        mutations.append(swapped_direction)

        changed_factor = copy.deepcopy(self.value)
        _observation(changed_factor, "K166R-S-to-R-turnover")["result"]["value"] = 5000
        mutations.append(changed_factor)

        invented_assay_floor = copy.deepcopy(self.value)
        _observation(invented_assay_floor, "H297N-racemization")["result"].update(
            {"detection_limit": 0.01, "detection_limit_unit": "s-1"}
        )
        mutations.append(invented_assay_floor)

        for index, changed in enumerate(mutations):
            with self.subTest(index=index):
                _repin(changed)
                self.validate(changed)
                with self.assertRaisesRegex(ValueError, "typed observation differs"):
                    validate_source_projections(changed, repo_root=ROOT)

    def test_focal_conclusion_requires_direct_focal_evidence(self):
        contextual_basis = copy.deepcopy(self.value)
        case = contextual_basis["cases"][0]
        boundary = next(
            row for row in case["discriminants"]
            if row["discriminant_id"] == "K166R-boundary"
        )
        next(
            row for row in boundary["alternative_assessments"]
            if row["alternative_id"] == "endpoint-selective-impairment"
        )["relation"] = "supports"
        case["adjudication"]["basis_discriminant_ids"] = ["K166R-boundary"]
        _repin(contextual_basis)
        with self.assertRaisesRegex(ValueError, "focal-variant direct-evidence"):
            self.validate(contextual_basis)

        contextual_focal = copy.deepcopy(self.value)
        contextual_focal["cases"][0]["evidence_references"][0]["applicability"] = "contextual"
        _repin(contextual_focal)
        with self.assertRaisesRegex(ValueError, "focal-variant observation requires direct"):
            self.validate(contextual_focal)

        direct_control = copy.deepcopy(self.value)
        direct_control["cases"][0]["evidence_references"][1]["applicability"] = "direct"
        _repin(direct_control)
        with self.assertRaisesRegex(ValueError, "non-focal variant observations must remain contextual"):
            self.validate(direct_control)

    def test_focal_variant_cannot_drift_from_the_reference_site(self):
        changed = copy.deepcopy(self.value)
        case = changed["cases"][0]
        case["focal_variant_id"] = "H298N"
        for observation in case["observations"]:
            if observation["variant"]["variant_id"] != "H297N":
                continue
            observation["variant"]["variant_id"] = "H298N"
            observation["variant"]["substitutions"][0]["sequence_position"] = 298
        _repin(changed)
        with self.assertRaisesRegex(ValueError, "focal variant does not match"):
            self.validate(changed)

    def test_reference_site_does_not_become_an_assayed_construct_or_changed_atom_link(self):
        case = self.value["cases"][0]
        self.assertEqual(case["focal_variant_id"], "H297N")
        self.assertEqual(
            case["site_context_binding"],
            {
                "assayed_construct_identity_status": "reference_protein_context_not_exact_assayed_construct",
                "atlas10_bundle_sha256": "27c2f16477911db206f1ff67cfc4c54aa150877e59dc31a7c1ff32dcca4a049e",
                "changed_source_atom_link_status": "unresolved_no_explicit_source_residue_label",
                "deposited_atom_identity_status": "not_asserted",
                "relationship": "before_step_declared_catalyst_site",
                "site_id": "P11444:H297",
            },
        )
        site_query = query_transformation_sites(
            self.transformations, atlas10_bundle=self.atlas10, mcsa_id="M0187"
        )
        self.assertEqual(
            (
                site_query["changed_source_atom_count"],
                site_query["resolved_source_atom_count"],
                site_query["unresolved_source_atom_count"],
            ),
            (7, 0, 7),
        )

        wrong_site = copy.deepcopy(self.value)
        wrong_site["cases"][0]["site_context_binding"]["site_id"] = "P11444:K166"
        _repin(wrong_site)
        with self.assertRaises(ValueError):
            self.validate(wrong_site)

        exact_construct = copy.deepcopy(self.value)
        exact_construct["cases"][0]["site_context_binding"]["assayed_construct_identity_status"] = "exact"
        _repin(exact_construct)
        with self.assertRaisesRegex(ValueError, "exact assayed-construct identity"):
            self.validate(exact_construct)

    def test_scope_and_manual_review_pin_prevent_upstream_promotion(self):
        case = self.value["cases"][0]
        self.assertTrue(all(value is False for value in case["scope_effect"].values()))
        abstentions = {row["abstention_id"] for row in case["mandatory_abstentions"]}
        self.assertTrue(
            {
                "conditions-and-nondetection",
                "exchange-not-racemization",
                "timing-and-intermediate",
                "protein-construct-identity",
                "structure-applicability",
                "source-atom-correspondence",
                "K166R-context",
            }
            <= abstentions
        )

        promoted = copy.deepcopy(self.value)
        promoted["cases"][0]["scope_effect"]["observed_intermediate_claimed"] = True
        _repin(promoted)
        with self.assertRaisesRegex(ValueError, "unsupported scope"):
            self.validate(promoted)

        stale = copy.deepcopy(self.value)
        stale["cases"][0]["adjudication"]["statement"] += " Changed after review."
        with self.assertRaisesRegex(ValueError, "reviewed mechanistic-evidence payload changed"):
            self.validate(stale)

    def test_required_scientific_boundaries_and_source_hashes_cannot_be_rebound(self):
        missing_boundary = copy.deepcopy(self.value)
        abstentions = missing_boundary["cases"][0]["mandatory_abstentions"]
        abstentions[:] = [
            row for row in abstentions
            if row["abstention_id"] != "conditions-and-nondetection"
        ]
        _repin(missing_boundary)
        with self.assertRaisesRegex(ValueError, "required source or inference abstention"):
            self.validate(missing_boundary)

        rebound_source = copy.deepcopy(self.value)
        rebound_source["source_bindings"][0]["sha256"] = "0" * 64
        _repin(rebound_source)
        self.validate(rebound_source)
        with self.assertRaisesRegex(ValueError, "source hash differs"):
            validate_source_projections(rebound_source, repo_root=ROOT)

    def source_contexts(self):
        return json.loads((ROOT / "src/catalytic_earth/mechanism_evidence_data/source_contexts.json").read_text(encoding="utf-8"))

    def repin_context(self, bundle, evidence=None):
        """Challenge semantic checks after all mutable assertion pins agree."""
        evidence = self.value if evidence is None else evidence
        entry, context = bundle["spec"]["contexts"][0], bundle["contexts"][0]
        evidence_sha = hashlib.sha256(canonical_bytes(evidence)).hexdigest()
        bundle["spec"]["evidence_binding"]["sha256"] = evidence_sha
        context["annotation"]["existing_case_binding"]["sha256"] = evidence_sha
        digest = hashlib.sha256(canonical_bytes(context["annotation"])).hexdigest()
        entry["annotation_binding"]["sha256"] = digest
        context["annotation_review"]["reviewed_sha256"]["annotation.json"] = digest
        entry["review_binding"]["sha256"] = hashlib.sha256(canonical_bytes(context["annotation_review"])).hexdigest()

    def test_primary_projection_requires_all_observation_fields_after_repin(self):
        bundle, evidence = self.source_contexts(), copy.deepcopy(self.value)
        projection = bundle["contexts"][0]["primary_projection"]
        projection["observations"] = [{"observation_id": row["observation_id"]} for row in projection["observations"]]
        binding = next(row for row in evidence["source_bindings"] if row["binding_id"] == "primary:PMID:7893690")
        binding["sha256"] = hashlib.sha256(canonical_bytes(projection)).hexdigest()
        _repin(evidence)
        self.repin_context(bundle, evidence)
        with self.assertRaisesRegex(ValueError, "observation differs from primary projection"):
            validate_source_contexts(bundle, evidence)

    def test_reviewed_scope_cannot_be_promoted_by_refreshing_hashes(self):
        mutations = [
            lambda row: row.update(status="measured_turnover"),
            lambda row: row["source_relation"].update(reference_scope="exact assayed construct identity"),
            lambda row: row.update(not_established=[]),
            lambda row: row.update(claim_id="CE-019"),
            lambda row: row["findings"][1].update(status="observed_functional_turnover"),
            lambda row: row.update(findings=[f for f in row["findings"] if f["status"] != "unresolved_source_conflict"]),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                bundle = self.source_contexts()
                mutate(bundle["contexts"][0]["annotation"])
                self.repin_context(bundle)
                with self.assertRaises(ValueError):
                    validate_source_contexts(bundle, self.value)

    def test_bound_sources_are_byte_exact_before_json_decode(self):
        bundle = self.source_contexts()
        def changed(path):
            raw = (ROOT / path).read_bytes()
            return raw if path.endswith(".gz") else raw.replace(b"\n", b"\r\n")
        with self.assertRaisesRegex(ValueError, "source hash differs"):
            build_source_contexts(bundle["spec"], self.value, changed)

    def test_deposit_context_is_separate_from_observations_and_retains_uncertainty(self):
        bundle = self.source_contexts()
        baseline = copy.deepcopy(bundle)
        result = self.query(variant="K166R", endpoint="structure", source_contexts=bundle)
        self.assertEqual((result["case_count"], result["matched_observation_count"]), (0, 0))
        contextual = result["source_context_query"]
        self.assertEqual(contextual["context_count"], 1)
        self.assertFalse(contextual["query_semantics"]["endpoint_filter_applies"])
        [match] = contextual["matches"]
        self.assertEqual(match["case"], self.value["cases"][0])
        self.assertEqual(match["citation_variant_related_observation_ids"], ["K166R-R-to-S-turnover", "K166R-S-to-R-turnover"])
        self.assertIn("exact_assayed_construct_and_preparation_identity", match["relation"]["unresolved_equivalences"])
        context = match["source_context"]
        self.assertEqual(context["pdb_id"], "1MDL")
        self.assertEqual(context["source_relation"]["variant"], "K166R")
        self.assertEqual([(r["component"]["id"], r["instance"]["asym_id"], r["instance"]["pdb_seq_num"])
                          for r in context["ligand_instances"]], [("RMN", "C", "398"), ("SMN", "D", "399")])
        self.assertEqual(context["source_rows"]["_entity_src_gen"][0]["pdbx_gene_src_scientific_name"], "Pseudomonas aeruginosa")
        self.assertTrue(any(r["status"] == "unresolved_source_conflict" for r in context["findings"]))
        self.assertIn("PRESUMABLY", context["source_rows"]["_pdbx_entry_details"][0]["compound_details"])
        self.assertTrue(context["not_established"])
        match["case"]["observations"].clear()
        context["findings"].clear()
        self.assertEqual(bundle, baseline)
        self.assertEqual(len(self.value["cases"][0]["observations"]), 6)

    def test_context_variant_filter_cannot_leak_to_focal_variant(self):
        for variant, count in ((None, 1), ("k166r", 1), ("H297N", 0), ("WT", 0)):
            with self.subTest(variant=variant):
                context = query_source_contexts(self.source_contexts(), self.value, variant=variant)
                self.assertEqual(context["context_count"], count)
        for endpoint in (None, "turnover", "isotope_exchange", "structure"):
            baseline = self.query(variant="K166R", endpoint=endpoint)
            included = self.query(variant="K166R", endpoint=endpoint, source_contexts=self.source_contexts())
            self.assertEqual(included.pop("source_context_query")["context_count"], 1)
            self.assertEqual(included, baseline)

    def test_context_rejects_wrong_case_source_and_primary_projection(self):
        mutations = []
        other_evidence = self.source_contexts()
        other_evidence["spec"]["contexts"][0]["evidence_id"] = "paper:PMID:1909893"
        mutations.append(other_evidence)
        other_case = self.source_contexts()
        other_case["spec"]["contexts"][0]["case_id"] += ".wrong"
        mutations.append(other_case)
        altered_projection = self.source_contexts()
        altered_projection["contexts"][0]["primary_projection"]["doi"] = "10.0/unrelated"
        mutations.append(altered_projection)
        altered_annotation = self.source_contexts()
        altered_annotation["contexts"][0]["annotation"]["source_relation"]["variant"] = "H297N"
        mutations.append(altered_annotation)
        duplicate = self.source_contexts()
        duplicate["contexts"].append(copy.deepcopy(duplicate["contexts"][0]))
        duplicate["spec"]["contexts"].append(copy.deepcopy(duplicate["spec"]["contexts"][0]))
        mutations.append(duplicate)
        for index, changed in enumerate(mutations):
            with self.subTest(index=index), self.assertRaises(ValueError):
                validate_source_contexts(changed, self.value)

    def test_coherent_annotation_repin_cannot_bypass_retained_deposit(self):
        bundle = self.source_contexts()
        entry, context = bundle["spec"]["contexts"][0], bundle["contexts"][0]
        changed = context["annotation"]
        changed["source_rows"]["_entity_src_gen"][0]["pdbx_gene_src_scientific_name"] = "Pseudomonas putida"
        raw = canonical_bytes(changed)
        entry["annotation_binding"]["sha256"] = hashlib.sha256(raw).hexdigest()
        review = context["annotation_review"]
        review["reviewed_sha256"]["annotation.json"] = entry["annotation_binding"]["sha256"]
        review_raw = canonical_bytes(review)
        entry["review_binding"]["sha256"] = hashlib.sha256(review_raw).hexdigest()
        overrides = {entry["annotation_binding"]["path"]: raw, entry["review_binding"]["path"]: review_raw}
        with self.assertRaisesRegex(ValueError, "source rows differ"):
            build_source_contexts(bundle["spec"], self.value,
                                  lambda path: overrides.get(path) or (ROOT / path).read_bytes())

    def test_citation_swap_with_refreshed_pins_still_requires_the_same_variant(self):
        bundle = self.source_contexts()
        entry, context = bundle["spec"]["contexts"][0], bundle["contexts"][0]
        entry["evidence_id"] = "paper:PMID:1909893"
        context["primary_projection"] = json.loads((ROOT / "data/atlas/mechanism_evidence/m0187/pmid_1909893_projection.json").read_text(encoding="utf-8"))
        annotation = context["annotation"]
        annotation["source_relation"].update(primary_pmid="1909893", doi=context["primary_projection"]["doi"])
        annotation["source_rows"]["_citation"][0].update(
            pdbx_database_id_pubmed="1909893", pdbx_database_id_doi=context["primary_projection"]["doi"],
        )
        digest = hashlib.sha256(canonical_bytes(annotation)).hexdigest()
        entry["annotation_binding"]["sha256"] = digest
        context["annotation_review"]["reviewed_sha256"]["annotation.json"] = digest
        entry["review_binding"]["sha256"] = hashlib.sha256(canonical_bytes(context["annotation_review"])).hexdigest()
        with self.assertRaisesRegex(ValueError, "no exact primary-evidence variant relation"):
            validate_source_contexts(bundle, self.value)

    def test_coherent_h297n_rebinding_cannot_replace_the_retained_k166r_deposit(self):
        bundle = self.source_contexts()
        entry, context = bundle["spec"]["contexts"][0], bundle["contexts"][0]
        entry["evidence_id"] = "paper:PMID:1909893"
        annotation = context["annotation"]
        h297n = json.loads((ROOT / "data/atlas/mechanism_evidence/m0187/pmid_1909893_projection.json").read_text(encoding="utf-8"))
        context["primary_projection"] = h297n
        annotation["source_relation"].update(
            primary_pmid="1909893", doi=h297n["doi"], variant="H297N",
            deposited_sequence_position=297, reference_sequence_position=297,
            deposited_residue="ASN", reference_residue="HIS",
        )
        annotation["source_rows"]["_citation"][0].update(
            pdbx_database_id_pubmed="1909893", pdbx_database_id_doi=h297n["doi"],
        )
        annotation["source_rows"]["_entity"][0]["pdbx_mutation"] = "H297N"
        annotation["source_rows"]["_struct_ref_seq_dif"][0].update(
            seq_num="297", pdbx_auth_seq_num="297", pdbx_seq_db_seq_num="297", mon_id="ASN", db_mon_id="HIS",
        )
        self.repin_context(bundle)
        overrides = {
            entry["annotation_binding"]["path"]: canonical_bytes(annotation),
            entry["review_binding"]["path"]: canonical_bytes(context["annotation_review"]),
        }
        with self.assertRaisesRegex(ValueError, "source rows differ.*_citation"):
            build_source_contexts(bundle["spec"], self.value,
                                  lambda path: overrides.get(path) or (ROOT / path).read_bytes())

    def test_ligand_instances_are_not_matched_by_component_name_alone(self):
        annotation = self.source_contexts()["contexts"][0]["annotation"]
        raw = gzip.decompress((ROOT / annotation["source_binding"]["path"]).read_bytes())
        annotation["ligand_instances"][0]["instance"]["asym_id"] = "D"
        with self.assertRaisesRegex(ValueError, "ligand identity differs"):
            audit_deposited_annotation(annotation, raw)


if __name__ == "__main__":
    unittest.main()
