from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli
from catalytic_earth.atlas_transformation_query import query_transformation_sets, query_transformations
from catalytic_earth.atlas_transformations import apply_graph_edits, replay_graph_edits


class TransformationCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.values = {key: core_cli.verified_transformations(key) for key in ("M0173", "M0187")}
        cls.atlas10 = json.loads(core_cli._resource_bytes(core_cli.ATLAS10_KERNEL))

    def query(self, **kwargs):
        return query_transformation_sets(self.values, atlas10_bundle=self.atlas10, **kwargs)

    def cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-transformations", *args]), 0)
        return json.loads(output.getvalue())

    def test_trypsin_query_contains_executable_addition_and_source_groups(self):
        result = self.cli("--mcsa-id", " m0173 ")
        self.assertEqual(result["schema_version"], "catalytic-earth.transformation-query.v2")
        self.assertEqual(result["query_semantics"]["correspondence_kind"], "project_reviewed_panel_locator_alignment")
        self.assertEqual(result["transformation_count"], 1)
        row = result["transformations"][0]
        self.assertEqual(row["correspondence_kind"], "source_panel_only")
        self.assertNotIn("canonical_input_correspondence", row)
        self.assertEqual(row["source_context"]["canonical_participant_correspondence"], "not_asserted")
        self.assertEqual(set(row["source_context"]["source_r_groups"]["element_r_atom_ids"]), {"a9", "a11"})
        panel = row["panel_correspondence"]
        self.assertEqual(len(panel["before_graph"]["atoms"]), 50)
        self.assertEqual(len(panel["graph_edits"]), 6)
        self.assertTrue(replay_graph_edits(panel["before_graph"], panel["graph_edits"],
                                          panel["after_graph"], panel["replay"]["atom_map"]))
        changed = apply_graph_edits(panel["before_graph"], panel["graph_edits"])
        bonds = {frozenset(item["atom_ids"]): item["order"] for item in changed["bonds"]}
        atoms = {item["atom_id"]: item for item in changed["atoms"]}
        self.assertEqual(bonds[frozenset(("a3", "a44"))], 1)
        self.assertEqual(bonds[frozenset(("a3", "a10"))], 1)
        self.assertEqual(bonds[frozenset(("a21", "a50"))], 1)
        self.assertNotIn(frozenset(("a44", "a50")), bonds)
        self.assertEqual(atoms["a10"]["formal_charge"], -1)
        self.assertEqual(atoms["a21"]["formal_charge"], 1)
        self.assertEqual(atoms["a9"]["element"], "R")
        self.assertTrue(all(item["stereochemistry"] is None for item in changed["atoms"]))
        self.assertTrue(row["scope_effect"]["source_depiction_transition"])
        self.assertFalse(row["scope_effect"]["exact_physical_peptide_identity"])

    def test_catalog_preserves_each_set_review_and_exact_filter_scope(self):
        result = self.cli("--all")
        self.assertEqual(result, self.query())
        self.assertEqual(result["schema_version"], "catalytic-earth.transformation-catalog-query.v1")
        self.assertEqual(result["transformation_count"], 2)
        self.assertEqual(result["searched_transformation_count"], 2)
        self.assertFalse(result["query_semantics"]["cross_set_evidence_join"])
        for item in result["sets"]:
            direct = query_transformations(self.values[item["mcsa_id"]], atlas10_bundle=self.atlas10)
            self.assertEqual(item["result"], direct)
        filtered = self.cli("--all", "--mcsa-id", "M0173")
        self.assertEqual(filtered["transformation_count"], 1)
        self.assertEqual([item["result"]["transformation_count"] for item in filtered["sets"]], [1, 0])
        self.assertEqual(self.cli("--all", "--mcsa-id", "M0213")["transformation_count"], 0)
        self.assertEqual(self.cli("--mcsa-id", "M0213")["transformation_count"], 0)

    def test_m0187_package_and_single_set_output_remain_compatible(self):
        digest = hashlib.sha256(core_cli._resource_bytes("transformation_data/transformations.json")).hexdigest()
        self.assertEqual(digest, "02135996931cd366945fad1773b1ca067f13cb609a17a56862ebfc91f5d28fa3")
        self.assertEqual(self.cli(), query_transformations(self.values["M0187"], atlas10_bundle=self.atlas10))
        self.assertEqual(self.cli("--mcsa-id", "M0187"), query_transformations(
            self.values["M0187"], atlas10_bundle=self.atlas10, mcsa_id="M0187"))
        self.assertEqual(self.cli()["schema_version"], "catalytic-earth.transformation-query.v1")

    def test_catalog_results_do_not_mutate_evidence_and_keys_cannot_mislabel_sets(self):
        original = copy.deepcopy(self.values)
        result = self.query()
        result["sets"][0]["result"]["transformations"].clear()
        result["sets"][0]["result"]["review"].clear()
        self.assertEqual(self.values, original)
        bad = {"M0173": self.values["M0187"]}
        with self.assertRaises(ValueError):
            query_transformation_sets(bad, atlas10_bundle=self.atlas10, mcsa_id="M0213")
        for values in ({}, {"unknown": self.values["M0173"]}):
            with self.assertRaises(ValueError):
                query_transformation_sets(values, atlas10_bundle=self.atlas10)

    def test_new_package_hash_and_output_file(self):
        original = core_cli._resource_bytes
        def altered(path):
            raw = original(path)
            return raw + b" " if path == "transformation_data/m0173_transformations.json" else raw
        with patch.object(core_cli, "_resource_bytes", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "transformation package differs"):
                core_cli.verified_transformations("M0173")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "catalog.json"
            result = self.cli("--all", "--output", str(target))
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), result)
