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


class ReactionCorrespondenceQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = core_cli.verified_source_drafts("plp-pyruvoyl")
        cls.primary = core_cli.verified_primary_evidence("plp-pyruvoyl", bundle=cls.bundle)
        cls.sidecar = core_cli.verified_reaction_correspondence("plp-pyruvoyl", bundle=cls.bundle)
        if cls.sidecar is None:
            raise AssertionError("reviewed reaction correspondence is missing")

    def query(self, **kwargs):
        return query_source_drafts(
            self.bundle, primary_evidence=self.primary,
            reaction_correspondence=self.sidecar, **kwargs,
        )

    def test_exact_forward_filter_retains_conflicts_without_reverse_or_form_aliases(self):
        result = self.query(mcsa_id="M0213", reactants=["57972"], products=["57416"])
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["schema_version"], "catalytic-earth.source-draft-query.v6")
        annotation = result["records"][0]["curated_reaction_correspondences"][0]
        self.assertEqual(annotation["curated_reaction"]["selected_directed_id"], "RHEA:20250")
        self.assertEqual(annotation["curated_reaction"]["selected_direction_code"], "LR")
        depiction = annotation["terminal_depiction"]
        self.assertEqual(depiction["alanine_fragment_raw_source_labels"], ["chebi:57972"])
        self.assertEqual(depiction["all_panel_trajectory_status"], "not_asserted")
        diagnostic = depiction["endpoint_diagnostic"]
        self.assertEqual([diagnostic[side]["computed_cip"] for side in ("initial", "terminal")], ["R", "S"])
        self.assertEqual([diagnostic[side]["fragment_formal_charge"] for side in ("initial", "terminal")], [-1, -1])
        self.assertTrue(all(value is False for value in annotation["scope_effect"].values()))
        for filters in ({"reactants": ["57416"], "products": ["57972"]},
                        {"reactants": ["16977"]}, {"products": ["15570"]}):
            with self.subTest(filters=filters):
                self.assertEqual(self.query(mcsa_id="M0213", **filters)["record_count"], 0)

    def test_compact_full_keep_correction_and_do_not_mutate_inputs(self):
        before = copy.deepcopy((self.bundle, self.primary, self.sidecar))
        compact, full = self.query(), self.query(include_steps=True)
        self.assertEqual(compact["curated_reaction_correspondence_count"], 1)
        for left, right in zip(compact["records"], full["records"]):
            self.assertEqual(left["curated_reaction_correspondences"], right["curated_reaction_correspondences"])
            self.assertEqual(left["mandatory_abstentions"], right["mandatory_abstentions"])
            self.assertEqual(left["evidence_tier"], 1)
        self.assertEqual((self.bundle, self.primary, self.sidecar), before)
        compact["records"][0]["curated_reaction_correspondences"].append({"mutation": True})
        self.assertEqual((self.bundle, self.primary, self.sidecar), before)

    def test_without_sidecar_legacy_library_result_is_unchanged(self):
        old = query_source_drafts(self.bundle, primary_evidence=self.primary)
        explicit_none = query_source_drafts(self.bundle, primary_evidence=self.primary, reaction_correspondence=None)
        self.assertEqual(old, explicit_none)
        self.assertNotIn("curated_reaction_correspondence", old)
        self.assertTrue(all("curated_reaction_correspondences" not in row for row in old["records"]))
        for name in ("default", "aldolase-transketolase"):
            self.assertIsNone(core_cli.verified_reaction_correspondence(name))

    def test_catalog_provenance_and_empty_match_do_not_drop_correction_metadata(self):
        bundles = {name: core_cli.verified_source_drafts(name)
                   for name in ("default", "aldolase-transketolase", "plp-pyruvoyl")}
        result = query_source_draft_batches(
            bundles, reaction_correspondence_by_batch={"plp-pyruvoyl": self.sidecar},
            mcsa_id="M0213",
        )
        self.assertEqual(result["schema_version"], "catalytic-earth.source-draft-catalog-query.v4")
        self.assertEqual(result["searched_record_count"], 11)
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["curated_reaction_correspondence_count"], 1)
        empty = self.query(mcsa_id="M9999")
        self.assertEqual(empty["curated_reaction_correspondence_count"], 0)
        self.assertEqual(empty["curated_reaction_correspondence"]["review"], self.sidecar["review"])
        with self.assertRaisesRegex(ValueError, "unselected source batch"):
            query_source_draft_batches({"default": bundles["default"]},
                                      reaction_correspondence_by_batch={"plp-pyruvoyl": self.sidecar})

    def test_cli_automatically_attaches_reviewed_correction_and_fails_on_changed_package(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-drafts", "--batch", "plp-pyruvoyl", "--mcsa-id", "M0213"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["curated_reaction_correspondence_count"], 1)
        self.assertFalse(result["query_semantics"]["curated_reaction_assigns_depicted_species"])
        self.assertFalse(result["query_semantics"]["curated_reaction_validates_source_steps"])
        original = core_cli._resource_bytes

        def changed(path):
            raw = original(path)
            return raw + b" " if path.endswith("_reaction_correspondence.json") else raw

        with patch.object(core_cli, "_resource_bytes", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "reaction correspondence package differs"):
                core_cli.verified_reaction_correspondence("plp-pyruvoyl", bundle=self.bundle)


if __name__ == "__main__":
    unittest.main()
