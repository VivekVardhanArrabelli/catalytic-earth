from __future__ import annotations

import contextlib
import copy
import io
import json
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli
from catalytic_earth.atlas_draft_catalog import query_source_draft_batches
from catalytic_earth.atlas_draft_query import query_source_drafts


class StepQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = core_cli.verified_source_drafts("plp-pyruvoyl")
        cls.primary = core_cli.verified_primary_evidence("plp-pyruvoyl", bundle=cls.bundle)
        cls.sidecar = core_cli.verified_step_evidence(
            "plp-pyruvoyl", bundle=cls.bundle, primary_evidence=cls.primary,
        )
        if cls.sidecar is None:
            raise AssertionError("reviewed step annotations are missing")

    def query(self, **kwargs):
        return query_source_drafts(
            self.bundle, primary_evidence=self.primary,
            step_evidence=self.sidecar, **kwargs,
        )

    def test_cofactor_source_labels_keep_plp_and_pyruvoyl_distinct(self):
        plp = self.query(cofactors=[" PLP "])
        self.assertEqual({r["mcsa_id"] for r in plp["records"]}, {"M0066", "M0186", "M0213"})
        pyruvoyl = self.query(cofactors=["pyruvoyl"])
        self.assertEqual([r["mcsa_id"] for r in pyruvoyl["records"]], ["M0049"])
        for record in plp["records"] + pyruvoyl["records"]:
            self.assertEqual(record["evidence_tier"], 1)
            self.assertTrue(record["mandatory_abstentions"])
            self.assertTrue(record["step_evidence_annotations"])
        self.assertEqual(self.query(cofactors=["PLP", "pyruvoyl"])["record_count"], 0)

    def test_extra_enzymatic_steps_do_not_inherit_cofactor_from_record(self):
        result = self.query(enzyme_contexts=["extra_enzymatic"])
        self.assertEqual([r["mcsa_id"] for r in result["records"]], ["M0186"])
        rows = result["records"][0]["step_evidence_annotations"]
        self.assertEqual([a["step_binding"]["source_step_id"] for a in rows], [6, 7])
        self.assertNotEqual(rows[0]["step_binding"]["source_scheme_sha256"],
                            rows[1]["step_binding"]["source_scheme_sha256"])
        self.assertEqual(self.query(cofactors=["PLP"], enzyme_contexts=["extra_enzymatic"])["record_count"], 0)
        self.assertEqual(self.query(cofactors=["pyruvoyl"], source_assertions=["explicitly_inferred"])["record_count"], 0)

    def test_inferred_roles_are_not_whole_step_inferences(self):
        rows = {
            (r["mcsa_id"], a["step_binding"]["source_step_id"]): a
            for r in self.query(source_assertions=["explicitly_inferred"])["records"]
            for a in r["step_evidence_annotations"]
        }
        self.assertEqual(set(rows), {("M0049", 7), ("M0186", 4)})
        self.assertEqual(rows[("M0049", 7)]["context"]["source_assertion"]["scope"], "whole_step")
        self.assertEqual(rows[("M0186", 4)]["context"]["source_assertion"]["scope"], "stated_detail_only")
        assumed = self.query(source_assertions=["explicitly_assumed"])
        self.assertEqual([r["mcsa_id"] for r in assumed["records"]], ["M0186"])
        row = assumed["records"][0]["step_evidence_annotations"][0]
        self.assertEqual(row["step_binding"]["source_step_id"], 5)
        self.assertEqual(row["context"]["source_assertion"]["scope"], "stated_detail_only")
        self.assertFalse(assumed["query_semantics"]["source_silent_implies_observed"])

    def test_compact_full_keep_all_step_witnesses_and_do_not_mutate_inputs(self):
        originals = copy.deepcopy((self.bundle, self.primary, self.sidecar))
        compact, full = self.query(), self.query(include_steps=True)
        self.assertEqual(compact["step_evidence_match_count"], 32)
        for left, right in zip(compact["records"], full["records"]):
            self.assertEqual(left["step_evidence_annotations"], right["step_evidence_annotations"])
            self.assertEqual(left["step_evidence_source_context"], right["step_evidence_source_context"])
            self.assertEqual(left["mandatory_abstentions"], right["mandatory_abstentions"])
            self.assertNotIn("mechanism_steps", left["mechanism_proposals"][0])
            self.assertIn("mechanism_steps", right["mechanism_proposals"][0])
        self.assertEqual((self.bundle, self.primary, self.sidecar), originals)
        racemase = next(r for r in compact["records"] if r["mcsa_id"] == "M0213")
        step_three = next(a for a in racemase["step_evidence_annotations"]
                          if a["step_binding"]["source_step_id"] == 3)
        self.assertEqual(step_three["context"]["source_assertion"]["status"], "source_silent")
        self.assertTrue({"protonating_species", "step_3_evidence_basis"}
                        <= {item["limit_id"] for item in step_three["limitations"]})
        tyrosine = next(r for r in step_three["context"]["roles"]
                        if r["actor_label"] == "Tyr265B")
        self.assertEqual(tyrosine["direction"], "source_forward_order")
        self.assertIn("deprotonates the alpha carbon", tyrosine["role_text"])
        serine = next(r for r in compact["records"] if r["mcsa_id"] == "M0186")
        summary = next(s["source_step_summary"] for s in serine["step_evidence_source_context"]["steps"]
                       if s["step_binding"]["source_step_id"] == 3)
        self.assertIn("would not occur", summary)
        self.assertIn("not necessarily the water", summary)

    def test_unannotated_batches_do_not_satisfy_step_filters(self):
        bundles = {name: core_cli.verified_source_drafts(name)
                   for name in ("default", "aldolase-transketolase", "plp-pyruvoyl")}
        result = query_source_draft_batches(
            bundles, step_evidence_by_batch={"plp-pyruvoyl": self.sidecar},
            primary_evidence_by_batch={"plp-pyruvoyl": self.primary},
            cofactors=[" PLP "],
        )
        self.assertEqual(result["searched_record_count"], 11)
        self.assertEqual(result["record_count"], 3)
        self.assertEqual(result["step_evidence_batch_ids"], ["plp-pyruvoyl"])
        self.assertEqual(result["filters"]["cofactors"], ["plp"])
        self.assertTrue(all(b["result"]["record_count"] == 0 for b in result["batches"]
                            if b["batch_id"] != "plp-pyruvoyl"))

    def test_package_pin_and_cli_opt_in(self):
        def run(*args):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(core_cli.main(["atlas-drafts", "--batch", "plp-pyruvoyl", *args]), 0)
            return json.loads(stream.getvalue())

        legacy, enhanced = run(), run("--step-evidence")
        self.assertNotIn("step_evidence", legacy)
        self.assertEqual(enhanced["step_evidence_match_count"], 32)
        self.assertEqual(run("--step-enzyme-context", "extra_enzymatic")["step_evidence_match_count"], 2)
        original_resource = core_cli._resource_bytes

        def changed_resource(path):
            raw = original_resource(path)
            return raw + b" " if path.endswith("_step_evidence.json") else raw

        with patch.object(core_cli, "_resource_bytes", side_effect=changed_resource):
            with self.assertRaisesRegex(ValueError, "step evidence package differs"):
                core_cli.verified_step_evidence("plp-pyruvoyl", bundle=self.bundle)

    def test_malformed_filters_reject_even_without_an_annotation_package(self):
        for name, value in (("cofactors", ""), ("enzyme_contexts", None),
                            ("source_assertions", "")):
            with self.subTest(name=name), self.assertRaises(ValueError):
                query_source_drafts(self.bundle, **{name: value})
        for label in (" ", "PLP,pyruvoyl"):
            with self.subTest(label=label), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    core_cli.build_parser().parse_args(["atlas-drafts", "--step-cofactor", label])
                self.assertEqual(raised.exception.code, 2)

    def test_pyruvoyl_structure_keeps_author_and_processed_chain_namespaces(self):
        self.assertIsNotNone(self.primary)
        annotation = next(a for a in self.primary["annotations"]
                          if a["annotation_id"] == "m0049.1pya.processed-pyruvoyl-site")
        self.assertEqual(annotation["target_scope"], "record_only")
        self.assertEqual(annotation["claim"]["structure_site"], {
            "pdb_id": "1PYA", "chain_id": "F",
            "author_residue_name": "PYR", "author_residue_number": 82,
        })
        self.assertEqual(annotation["claim"]["sequence_mapping"]["status"], "not_asserted")
        self.assertIsNone(annotation["claim"]["sequence_mapping"]["sequence_position"])
        self.assertTrue({"numbering_namespaces", "standard_alignment_offset",
                         "precursor_maturation_mechanism", "source_substrate_identity"}
                        <= {item["limit_id"] for item in annotation["limits"]})
        result = self.query(mcsa_id="M0049")
        self.assertIn(annotation, result["records"][0]["primary_evidence_annotations"])
        self.assertTrue(all(a["context"]["chemical_context"]["value"] == "unresolved"
                            for a in result["records"][0]["step_evidence_annotations"]))


if __name__ == "__main__":
    unittest.main()
