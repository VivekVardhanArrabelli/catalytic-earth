from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas_kernel import run_atlas3_query, validate_atlas3_kernel
from catalytic_earth.atlas_selection import load_atlas3_selection


ROOT = Path(__file__).resolve().parents[2]
KERNEL_PATH = ROOT / "data/atlas/atlas3/kernel.json"
QUERY_PATH = ROOT / "data/atlas/atlas3/queries/case_truth_summary.sql"
EXPECTED_PATH = ROOT / "data/atlas/atlas3/queries/case_truth_summary_expected.json"
SELECTION_PATH = ROOT / "data/atlas/atlas3_selection.json"
MANIFEST_PATH = ROOT / "data/atlas/atlas3/source_manifest.json"


class AtlasKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.kernel = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))
        cls.query = QUERY_PATH.read_text(encoding="utf-8")
        cls.expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        cls.selection = load_atlas3_selection(SELECTION_PATH)
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_nine_objects_validate_against_selection_and_source_manifest(self) -> None:
        summary = validate_atlas3_kernel(
            self.kernel,
            selection=self.selection,
            source_manifest=self.manifest,
        )
        self.assertEqual(summary["case_count"], 3)
        self.assertEqual(summary["record_count"], 9)
        self.assertEqual(
            summary["object_type_counts"],
            {
                "mechanism_hypothesis": 3,
                "net_reaction": 3,
                "source_mechanism": 3,
            },
        )

    def test_local_query_matches_the_frozen_expected_rows(self) -> None:
        rows = run_atlas3_query(self.kernel, self.query)
        self.assertEqual(rows, self.expected["query_rows"])

    def test_mnsod_refuses_same_ec_cu_zn_mechanism_transfer(self) -> None:
        source = next(
            record
            for record in self.kernel["records"]
            if record["case_id"] == "atlas3.mnsod-ecoli.redox"
            and record["object_type"] == "source_mechanism"
        )
        hypothesis = next(
            record
            for record in self.kernel["records"]
            if record["case_id"] == "atlas3.mnsod-ecoli.redox"
            and record["object_type"] == "mechanism_hypothesis"
        )
        self.assertEqual(source["status"], "abstained_no_direct_source_mechanism")
        self.assertEqual(source["mechanism_steps"], [])
        self.assertEqual(source["sites"], [])
        self.assertNotIn("P00445", json.dumps(hypothesis["sites"]))
        self.assertNotIn("2JCW", json.dumps(hypothesis["sites"]))

    def test_numbering_crosswalks_are_explicit(self) -> None:
        hypotheses = {
            record["case_id"]: record
            for record in self.kernel["records"]
            if record["object_type"] == "mechanism_hypothesis"
        }
        mnsod_sites = {site["site_id"]: site for site in hypotheses["atlas3.mnsod-ecoli.redox"]["sites"]}
        self.assertEqual(mnsod_sites["P00448:H27"]["pdb_mapping"]["author_position"], 26)
        tem_sites = {site["site_id"]: site for site in hypotheses["atlas3.tem1-ecoli.covalent"]["sites"]}
        self.assertEqual(tem_sites["P62593:S68"]["pdb_mapping"]["author_position"], 70)
        self.assertEqual(tem_sites["P62593:S68"]["pdb_mapping"]["label_position"], 45)

    def test_fabricating_mnsod_source_steps_fails_closed(self) -> None:
        changed = copy.deepcopy(self.kernel)
        source = next(
            record
            for record in changed["records"]
            if record["case_id"] == "atlas3.mnsod-ecoli.redox"
            and record["object_type"] == "source_mechanism"
        )
        source["mechanism_steps"] = [
            {
                "step_id": "fabricated.same-ec.step",
                "order": 1,
                "summary": "A structurally valid but scientifically forbidden imported step.",
                "transformation": "same_ec_transfer",
                "catalyst_site_ids": [],
                "evidence_ids": [source["evidence"][0]["evidence_id"]],
                "confidence": "source_curated",
                "source_step_id": 1,
            }
        ]
        with self.assertRaisesRegex(ValueError, "must remain empty"):
            validate_atlas3_kernel(changed)


if __name__ == "__main__":
    unittest.main()
