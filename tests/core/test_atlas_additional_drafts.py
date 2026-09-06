"""Source-scope and installed-query checks for the second reviewed draft batch."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.core_cli import main, verified_source_drafts


BATCH = "aldolase-transketolase"


class AdditionalSourceDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = verified_source_drafts(BATCH)

    def test_batches_remain_separately_bound(self):
        original = verified_source_drafts()
        self.assertEqual(original["selection"]["record_ids"], ["M0106", "M0107", "M0212", "M0753"])
        self.assertEqual(self.bundle["selection"]["record_ids"], ["M0052", "M0219", "M0222"])
        self.assertNotEqual(original["bundle_id"], self.bundle["bundle_id"])
        self.assertNotEqual(original["source_manifest_sha256"], self.bundle["source_manifest_sha256"])
        self.assertTrue(all(r["evidence_tier"] == 1 for r in self.bundle["records"]))

    def test_shared_aldolase_participants_preserve_distinct_source_chemistry(self):
        result = query_source_drafts(
            self.bundle, reactants=("57642", "59776"), products=("49299",), include_steps=True,
        )
        records = {r["mcsa_id"]: r for r in result["records"]}
        self.assertEqual(set(records), {"M0052", "M0222"})
        self.assertEqual(len(records["M0052"]["mechanism_proposals"][0]["mechanism_steps"]), 4)
        self.assertEqual(len(records["M0222"]["mechanism_proposals"][0]["mechanism_steps"]), 10)
        for record in records.values():
            self.assertEqual(len(record["participant_matches"]), 3)
            for flag in ("canonical_reaction", "balanced_net_reaction", "exact_reaction_instance"):
                self.assertIs(record["reaction_context"][flag], False)
        self.assertFalse(result["query_semantics"]["shared_participant_implies_reaction_equivalence"])

    def test_source_conflicts_survive_compact_queries(self):
        expected = {
            "M0222": {"step_1_substrate_identity", "protein_specific_mechanism_applicability"},
            "M0219": {
                "proposal_specific_reaction_context", "proposal_protein_applicability",
                "native_divalent_metal_identity", "typed_cofactor_redox_state",
            },
        }
        for mcsa_id, clauses in expected.items():
            with self.subTest(mcsa_id=mcsa_id):
                record = query_source_drafts(self.bundle, mcsa_id=mcsa_id)["records"][0]
                self.assertTrue(clauses <= {a["clause_id"] for a in record["mandatory_abstentions"]})
                self.assertTrue(record["source_residue_assertions"])
                self.assertEqual(record["state_context"]["state_transitions"], [])

    def test_transketolase_proposals_are_retained_without_combining_contexts(self):
        record = query_source_drafts(self.bundle, mcsa_id="M0219", include_steps=True)["records"][0]
        self.assertEqual([p["source_mechanism_id"] for p in record["mechanism_proposals"]], [1, 2])
        self.assertEqual([len(p["mechanism_steps"]) for p in record["mechanism_proposals"]], [7, 5])
        self.assertTrue(all(p["source_references"] for p in record["mechanism_proposals"]))
        self.assertEqual(record["state_context"]["assembly"]["mode"], "single_source_component")

    def test_cli_selects_new_batch_and_keeps_the_query_universe(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["atlas-drafts", "--batch", BATCH, "--reactant", "57642"])
        query = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual({r["mcsa_id"] for r in query["records"]}, {"M0052", "M0222"})
        self.assertEqual(query["selection"], self.bundle["selection"])


if __name__ == "__main__":
    unittest.main()
