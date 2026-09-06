from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import unittest

from catalytic_earth import core_cli
from catalytic_earth.atlas_draft_catalog import query_source_draft_batches
from catalytic_earth.atlas_draft_query import query_source_drafts


class ObservedStateQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        names = ("default", "aldolase-transketolase", "plp-pyruvoyl")
        cls.bundles = {name: core_cli.verified_source_drafts(name) for name in names}
        cls.evidence = {
            name: core_cli.verified_primary_evidence(name, bundle=bundle)
            for name, bundle in cls.bundles.items()
        }
        cls.bundle = cls.bundles["plp-pyruvoyl"]
        cls.primary = cls.evidence["plp-pyruvoyl"]
        cls.steps = core_cli.verified_step_evidence("plp-pyruvoyl", bundle=cls.bundle)

    def query(self, **kwargs):
        return query_source_drafts(self.bundle, primary_evidence=self.primary, **kwargs)

    def test_state_filters_require_one_typed_annotation_and_exact_component(self):
        analogue = self.query(observed_states=["bound_ligand_analogue"], observed_components=[" PDD "])
        self.assertEqual([r["mcsa_id"] for r in analogue["records"]], ["M0213"])
        self.assertEqual(analogue["observed_state_context_count"], 1)
        self.assertEqual(analogue["filters"]["observed_components"], ["pdd"])
        self.assertEqual(self.query(observed_components=["PDD", "PLV"])["record_count"], 0)
        self.assertEqual(self.query(observed_states=["bound_ligand_analogue", "bound_ligand_adduct"])["record_count"], 0)
        self.assertEqual(self.query(observed_components=["PLP"])["record_count"], 0)
        self.assertEqual(self.query(observed_components=["PDD", "pdd"])["record_count"], 1)

    def test_structure_and_step_intersection_retains_record_only_scope(self):
        joined = self.query(
            step_evidence=self.steps, observed_states=["bound_ligand_adduct"],
            enzyme_contexts=["extra_enzymatic"],
        )
        self.assertEqual([r["mcsa_id"] for r in joined["records"]], ["M0186"])
        record = joined["records"][0]
        self.assertEqual([a["step_binding"]["source_step_id"] for a in record["step_evidence_annotations"]], [6, 7])
        self.assertFalse(joined["query_semantics"]["observed_state_grounds_step"])
        self.assertFalse(record["observed_state_contexts"][0]["claim"]["observed_state_grounds_step"])
        self.assertTrue(all(a["context"]["chemical_context"]["value"] == "unresolved"
                            for a in record["step_evidence_annotations"]))
        self.assertEqual(self.query(step_evidence=self.steps, observed_components=["PYR"], cofactors=["PLP"])["record_count"], 0)

    def test_compact_and_full_keep_source_disagreement_and_namespace_witnesses(self):
        original = copy.deepcopy((self.bundle, self.primary))
        compact = self.query(include_observed_state_context=True)
        full = self.query(include_observed_state_context=True, include_steps=True)
        self.assertEqual(compact["record_count"], 4)
        self.assertEqual(compact["observed_state_context_count"], 3)
        self.assertEqual(compact["primary_evidence"]["source_bindings"], self.primary["source_bindings"])
        for left, right in zip(compact["records"], full["records"]):
            self.assertEqual(left["observed_state_contexts"], right["observed_state_contexts"])
            self.assertEqual(left["primary_evidence_annotations"], right["primary_evidence_annotations"])
            for annotation in left["observed_state_contexts"]:
                self.assertTrue(annotation["projection_excerpt"]["locators"])
                self.assertTrue(annotation["projection_excerpt"]["support_edges"])
        claims = {r["mcsa_id"]: r["observed_state_contexts"][0]["claim"]
                  for r in compact["records"] if r["observed_state_contexts"]}
        self.assertEqual(claims["M0186"]["chemical_reconciliation"]["status"], "unresolved_source_description_vs_deposit")
        self.assertEqual(claims["M0186"]["observed_entity"]["state_kind"], "bound_ligand_adduct")
        instance = next(i for i in claims["M0213"]["structure_instances"] if i["atom_author_chain_id"] == "B")
        self.assertEqual(instance["atom_author_residue_number"], 1390)
        self.assertEqual(instance["source_author_residue_number"], 390)
        self.assertIsNone(instance["label_seq_id"])
        self.assertTrue(all(c["observed_entity"]["normalized_chebi_id"] is None for c in claims.values()))
        pyruvoyl = next(r for r in compact["records"] if r["mcsa_id"] == "M0049")
        edges = pyruvoyl["observed_state_contexts"][0]["projection_excerpt"]["support_edges"]
        self.assertTrue({"direct_structure_observation", "curated_identity_support", "cross_source_curated_projection"}
                        <= {edge["support_status"] for edge in edges})
        self.assertEqual((self.bundle, self.primary), original)

    def test_untyped_legacy_annotations_are_preserved_without_inferred_classification(self):
        from tests.core.test_atlas_primary_evidence import _valid_v2_sidecar

        catalog = query_source_draft_batches(
            self.bundles, primary_evidence_by_batch=self.evidence,
            include_observed_state_context=True,
        )
        self.assertEqual(catalog["searched_record_count"], 11)
        self.assertEqual(catalog["record_count"], 11)
        self.assertEqual(catalog["observed_state_context_count"], 4)
        additional = next(b["result"] for b in catalog["batches"] if b["batch_id"] == "aldolase-transketolase")
        self.assertEqual(additional["observed_state_context_count"], 1)
        self.assertEqual(additional["query_semantics"]["legacy_primary_annotation_state_classification"], "not_inferred")
        for record in additional["records"]:
            expected = [a for a in self.evidence["aldolase-transketolase"]["annotations"]
                        if a["record_binding"]["record_id"] == record["record_id"]]
            self.assertEqual(record["primary_evidence_annotations"], expected)
            if record["mcsa_id"] == "M0219":
                self.assertEqual(record["observed_state_contexts"], [])
        old_bundle = self.bundles["aldolase-transketolase"]
        legacy = query_source_drafts(
            old_bundle, primary_evidence=_valid_v2_sidecar(old_bundle),
            observed_states=["protein_ligand_covalent_adduct"],
        )
        self.assertEqual(legacy["record_count"], 0)
        filtered = query_source_draft_batches(
            self.bundles, primary_evidence_by_batch=self.evidence, observed_components=["PDD"],
        )
        self.assertEqual(filtered["record_count"], 1)

    def test_covalent_comparison_keeps_unknown_order_and_dictionary_instance_distinction(self):
        kwargs = {"primary_evidence_by_batch": self.evidence,
                  "observed_states": ["protein_ligand_covalent_adduct"]}
        result = query_source_draft_batches(self.bundles, observed_components=["13P"], **kwargs)
        rows = [r for b in result["batches"] for r in b["result"]["records"]]
        self.assertEqual([r["mcsa_id"] for r in rows], ["M0222"])
        self.assertEqual(result["observed_state_context_count"], 1)
        annotation = rows[0]["observed_state_contexts"][0]
        attachments = annotation["claim"]["protein_attachments"]
        self.assertEqual(len(attachments), 4)
        self.assertEqual({a["ligand_endpoint"]["label_asym_id"] for a in attachments}, {"E", "F", "G", "H"})
        self.assertTrue(all(a["source_bond_order_code"] is None and a["source_bond_order_token"] == "?"
                            and a["raw_conn_type"] == "covale" for a in attachments))
        observations = {o["observation_kind"]: o for o in annotation["claim"]["chemical_observations"]}
        self.assertEqual(observations["deposited_component_dictionary_bond_order"]["source_bond_order_code"], "doub")
        self.assertEqual(observations["deposited_modeled_instance_atom_inventory"]["omitted_atom_ids"], ["O2"])
        self.assertIsNone(annotation["claim"]["observed_entity"]["normalized_chebi_id"])
        self.assertFalse(result["query_semantics"]["observed_state_grounds_step"])
        for component in ("DHAP", "CHEBI:57642", "PDD"):
            with self.subTest(component=component):
                self.assertEqual(query_source_draft_batches(self.bundles, observed_components=[component], **kwargs)["record_count"], 0)
        self.assertEqual(query_source_draft_batches(
            self.bundles, step_evidence_by_batch={"plp-pyruvoyl": self.steps},
            cofactors=["PLP"], **kwargs,
        )["record_count"], 0)

    def test_additive_pyruvoyl_context_does_not_rewrite_or_double_count_old_observation(self):
        annotation = next(a for a in self.primary["annotations"]
                          if a["annotation_id"] == "m0049.1pya.processed-pyruvoyl-site")
        digest = hashlib.sha256(json.dumps(annotation, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(digest, "bcb0dd4a591550b71659a4e6e64c58680f9f27ea6ef30e1fb3763f56e9407fd4")
        result = self.query(mcsa_id="M0049", include_observed_state_context=True)
        self.assertEqual(result["observed_state_context_count"], 1)
        self.assertIn(annotation, result["records"][0]["primary_evidence_annotations"])
        self.assertFalse(result["query_semantics"]["observed_state_context_count_is_independent_observation_count"])

    def test_cli_opt_in_and_invalid_filters_fail_without_source_annotations(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-drafts", "--batch", "all", "--observed-component", "PDD"]), 0)
        self.assertEqual(json.loads(output.getvalue())["observed_state_context_count"], 1)
        self.assertNotIn("observed_state_context_count", self.query())
        for kwargs in ({"observed_states": ""}, {"observed_components": None},
                       {"observed_states": ["native"]}, {"observed_components": [" "]},
                       {"observed_components": ["PDD,PLV"]}, {"include_observed_state_context": "false"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                query_source_drafts(self.bundles["default"], **kwargs)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            core_cli.build_parser().parse_args(["atlas-drafts", "--observed-component", "PDD,PLV"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
