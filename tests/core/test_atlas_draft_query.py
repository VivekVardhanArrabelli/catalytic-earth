from __future__ import annotations

import contextlib
import copy
import io
import json
import unittest

from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.core_cli import main, verified_source_drafts


class SourceDraftQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = verified_source_drafts()

    def test_assembly_filter_distinguishes_fixed_from_cycling_components(self):
        fixed = query_source_drafts(self.bundle, assembly="fixed_multisubunit")
        cycling = query_source_drafts(self.bundle, assembly="cycle_coupled_association")
        self.assertEqual([r["mcsa_id"] for r in fixed["records"]], ["M0107"])
        self.assertEqual([r["mcsa_id"] for r in cycling["records"]], ["M0212"])

    def test_compact_result_preserves_hisf_scope_and_conflict(self):
        result = query_source_drafts(self.bundle, mcsa_id="m0753")
        record = result["records"][0]
        self.assertEqual(record["evidence_tier"], 1)
        self.assertTrue(any(a["clause_id"] == "resolved_aspartate_roles"
                            for a in record["mandatory_abstentions"]))
        self.assertIn("HisF", record["source_scope"])
        source = next(r for r in self.bundle["records"] if r["mcsa_id"] == "M0753")
        self.assertEqual(record["source_residue_assertions"], source["source_residue_assertions"])
        self.assertIn("source_step_count", record["mechanism_proposals"][0])
        self.assertNotIn("mechanism_steps", record["mechanism_proposals"][0])

    def test_step_expansion_does_not_mutate_shared_package(self):
        before = copy.deepcopy(self.bundle)
        full = query_source_drafts(self.bundle, mcsa_id="M0107", include_steps=True)
        compact = query_source_drafts(self.bundle, mcsa_id="M0107")
        for whole, brief in zip(full["records"][0]["mechanism_proposals"],
                                compact["records"][0]["mechanism_proposals"]):
            self.assertEqual(len(whole["mechanism_steps"]), brief["source_step_count"])
        self.assertEqual(before, self.bundle)

    def test_empty_result_is_not_a_source_absence_claim(self):
        result = query_source_drafts(self.bundle, mcsa_id="M9999")
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["claim_boundary"], self.bundle["claim_boundary"])
        self.assertEqual(result["selection"], self.bundle["selection"])
        self.assertEqual(result["selection"]["record_ids"], ["M0106", "M0107", "M0212", "M0753"])
        self.assertEqual(result["selection"]["requested_operation"], "source_scoped_mechanism_draft")

    def test_cli_retrieves_carrier_chemistry_with_abstentions(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["atlas-drafts", "--mcsa-id", "M0106", "--text", "lipoyl"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result["record_count"], 1)
        clauses = {a["clause_id"] for a in result["records"][0]["mandatory_abstentions"]}
        self.assertTrue({"carrier_host_identity", "attachment_site", "structure_localization"} <= clauses)


if __name__ == "__main__":
    unittest.main()
