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
from catalytic_earth.atlas_partial_panel_query import query_panel_comparisons


class PartialPanelQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = core_cli.verified_panel_comparisons()
        cls.atlas10 = json.loads(core_cli._resource_bytes(core_cli.ATLAS10_KERNEL))

    def cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(list(args)), 0)
        return json.loads(output.getvalue())

    def test_query_exposes_partial_edit_and_arrow_coverage(self):
        result = self.cli("atlas-panel-comparisons", "--mcsa-id", " m0173 ")
        self.assertEqual(result["schema_version"], "catalytic-earth.partial-panel-query.v1")
        self.assertEqual(result["comparison_count"], 1)
        self.assertFalse(result["query_semantics"]["count_is_complete_transition_count"])
        self.assertEqual(result["query_semantics"]["cross_step_composition"], "not_asserted")
        row = result["comparisons"][0]
        coverage = row["coverage"]
        self.assertEqual((coverage["before_node_count"], coverage["after_node_count"], coverage["mapped_node_count"]), (50, 42, 40))
        self.assertEqual(len(coverage["replayed_edit_ids"]), 3)
        self.assertEqual(len(coverage["after_graph_unverified_edit_ids"]), 3)
        self.assertEqual({item["flow_id"]: item["status"] for item in coverage["flow_coverage"]}, {
            "o24": "after_graph_unverified", "o25": "partially_replayed", "o26": "fully_replayed",
        })
        self.assertEqual((coverage["full_before_formal_charge"], coverage["full_after_formal_charge"]), (-1, 0))
        self.assertEqual((coverage["projected_before_formal_charge"], coverage["projected_after_formal_charge"]), (0, 0))
        self.assertFalse(row["scope_effect"]["omitted_nodes_are_deleted"])
        self.assertFalse(row["scope_effect"]["unverified_edits_are_after_graph_confirmed"])
        self.assertEqual(result["review"], self.value["review"])
        self.assertEqual(result["source_bindings"], self.value["source_bindings"])

    def test_empty_filter_preserves_provenance_and_invalid_identifier_fails(self):
        result = self.cli("atlas-panel-comparisons", "--mcsa-id", "M0187")
        self.assertEqual(result["comparison_count"], 0)
        self.assertEqual(result["comparisons"], [])
        self.assertEqual(result["review"], self.value["review"])
        with self.assertRaises(ValueError):
            query_panel_comparisons(self.value, atlas10_bundle=self.atlas10, mcsa_id="trypsin")

    def test_results_are_deep_copies_and_default_is_the_reviewed_set(self):
        original = copy.deepcopy(self.value)
        result = query_panel_comparisons(self.value, atlas10_bundle=self.atlas10)
        self.assertEqual(self.cli("atlas-panel-comparisons"), result)
        result["comparisons"][0]["coverage"]["unmatched_before_atom_ids"].clear()
        result["review"].clear()
        result["source_bindings"].clear()
        self.assertEqual(self.value, original)

    def test_partial_comparison_does_not_change_full_transformation_catalog(self):
        catalog = self.cli("atlas-transformations", "--all")
        self.assertEqual(catalog["transformation_count"], 2)
        self.assertEqual(catalog["searched_transformation_count"], 2)
        for path, expected in {
            "transformation_data/transformations.json": "02135996931cd366945fad1773b1ca067f13cb609a17a56862ebfc91f5d28fa3",
            "transformation_data/m0173_transformations.json": "b4150239ea101e22046d416c685bdf88a01a047b0c6b6d376f206a551644d82c",
        }.items():
            self.assertEqual(hashlib.sha256(core_cli._resource_bytes(path)).hexdigest(), expected)

    def test_package_and_attribution_corruption_fail_before_query(self):
        original = core_cli._resource_bytes
        for target in ("panel_comparison_data/comparisons.json", "panel_comparison_data/attribution.md"):
            with self.subTest(target=target):
                def altered(path):
                    data = original(path)
                    return data + b" " if path == target else data
                with patch.object(core_cli, "_resource_bytes", side_effect=altered):
                    with self.assertRaises(ValueError):
                        core_cli.verified_panel_comparisons()

    def test_output_file_contains_the_same_bounded_query(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "partial.json"
            result = self.cli("atlas-panel-comparisons", "--output", str(path))
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), result)
