from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli
from catalytic_earth.atlas_transformation_query import query_transformations
from catalytic_earth.atlas_transformations import apply_graph_edits, replay_graph_edits


class TransformationQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = core_cli.verified_transformations()
        cls.atlas10 = json.loads(core_cli._resource_bytes(core_cli.ATLAS10_KERNEL))

    def query(self, **kwargs):
        return query_transformations(self.value, atlas10_bundle=self.atlas10, **kwargs)

    def test_query_delivers_replayable_chemical_change(self):
        result = self.query(mcsa_id=" m0187 ")
        self.assertEqual(result["schema_version"], "catalytic-earth.transformation-query.v1")
        self.assertEqual(result["filters"], {"mcsa_id": "M0187"})
        self.assertEqual(result["transformation_count"], 1)
        row = result["transformations"][0]
        panel = row["panel_correspondence"]
        self.assertTrue(replay_graph_edits(panel["before_graph"], panel["graph_edits"],
                                          panel["after_graph"], panel["replay"]["atom_map"]))
        changed = apply_graph_edits(panel["before_graph"], panel["graph_edits"])
        atoms = {a["atom_id"]: a for a in changed["atoms"]}
        self.assertEqual(atoms["a58"]["formal_charge"], 1)
        self.assertEqual(atoms["a63"]["formal_charge"], -1)
        self.assertIsNone(atoms["a9"]["stereochemistry"])
        bonds = {frozenset(b["atom_ids"]): b["order"] for b in changed["bonds"]}
        self.assertEqual(bonds[frozenset(("a8", "a9"))], 2)
        self.assertEqual(bonds[frozenset(("a8", "a10"))], 1)
        self.assertEqual(bonds[frozenset(("a10", "a65"))], 1)
        self.assertEqual(bonds[frozenset(("a58", "a66"))], 1)
        self.assertNotIn(frozenset(("a63", "a65")), bonds)
        self.assertNotIn(frozenset(("a9", "a66")), bonds)
        self.assertEqual(len(row["canonical_input_correspondence"]["map_alternatives"]), 2)
        self.assertEqual(len(panel["chemical_map_alternatives"]), 2)
        self.assertFalse(row["scope_effect"]["canonical_product_correspondence"])
        self.assertFalse(result["query_semantics"]["count_is_complete_mechanism_count"])

    def test_empty_result_is_scoped_and_invalid_identifiers_reject(self):
        result = self.query(mcsa_id="M0213")
        self.assertEqual(result["transformation_count"], 0)
        self.assertEqual(result["transformations"], [])
        self.assertIn("not_absence_of_chemistry", result["query_semantics"]["empty_result"])
        for value in ("", "0187", "M0187,M0213", 187, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.query(mcsa_id=value)

    def test_result_does_not_mutate_reviewed_input(self):
        original = copy.deepcopy(self.value)
        result = self.query()
        result["transformations"][0]["panel_correspondence"]["graph_edits"].clear()
        result["source_bindings"].clear()
        result["review"].clear()
        self.assertEqual(self.value, original)

    def test_package_and_attribution_integrity(self):
        original = core_cli._resource_bytes
        for suffix, message in (("transformations.json", "transformation package differs"),
                                ("attribution.md", "transformation attribution differs")):
            def changed_resource(path):
                raw = original(path)
                return raw + b" " if path == "transformation_data/" + suffix else raw

            with self.subTest(suffix=suffix), patch.object(core_cli, "_resource_bytes", side_effect=changed_resource):
                with self.assertRaisesRegex(ValueError, message):
                    core_cli.verified_transformations()

    def test_cli_output_and_legacy_atlas10_result(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "transformation.json"
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(core_cli.main([
                    "atlas-transformations", "--mcsa-id", "M0187", "--output", str(target),
                ]), 0)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), self.query(mcsa_id="M0187"))
            self.assertEqual(target.read_bytes(), stream.getvalue().encode("utf-8"))
        legacy = core_cli.verified_atlas10_result()
        self.assertEqual(legacy["runtime_result_sha256"],
                         "57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb")
        self.assertEqual(legacy["record_count"], 30)
