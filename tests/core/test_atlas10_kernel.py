from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas10_kernel import (
    build_atlas10_runtime_result,
    canonical_sha256,
    execute_atlas10_query,
    validate_atlas10_kernel,
)
from catalytic_earth.atlas10_selection import load_atlas10_selection


ROOT = Path(__file__).resolve().parents[2]
ATLAS_ROOT = ROOT / "data/atlas/atlas10"
KERNEL_PATH = ATLAS_ROOT / "kernel.json"
INHERITED_PATH = ROOT / "data/atlas/atlas3/kernel.json"
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
EXPECTED_PATH = ATLAS_ROOT / "queries/runtime_expected.json"
QUERY_PATHS = {
    "atlas10.query.convergent-strategy": ATLAS_ROOT / "queries/convergent_strategy.sql",
    "atlas10.query.shared-fold-divergent-chemistry": (
        ATLAS_ROOT / "queries/shared_fold_divergent_chemistry.sql"
    ),
}


class Atlas10KernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.kernel = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))
        cls.inherited = json.loads(INHERITED_PATH.read_text(encoding="utf-8"))
        cls.selection = load_atlas10_selection(SELECTION_PATH)
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        cls.queries = {
            query_id: path.read_text(encoding="utf-8")
            for query_id, path in QUERY_PATHS.items()
        }

    def test_ten_case_surface_and_source_chemistry_counts_validate(self) -> None:
        summary = validate_atlas10_kernel(
            self.kernel,
            selection=self.selection,
            source_manifest=self.manifest,
            inherited_kernel=self.inherited,
        )
        self.assertEqual(summary["case_count"], 10)
        self.assertEqual(summary["record_count"], 30)
        self.assertEqual(summary["documented_rhea_gaps"], 3)
        self.assertEqual(summary["non_detailed_abstentions"], 1)
        self.assertEqual(summary["source_mechanism_steps"], 21)
        self.assertEqual(summary["source_electron_flows"], 61)

    def test_relationship_queries_match_frozen_expected_rows(self) -> None:
        runtime = build_atlas10_runtime_result(
            self.kernel, self.inherited, self.queries
        )
        self.assertEqual(
            runtime["relationship_query_results"],
            self.expected["relationship_query_results"],
        )
        self.assertEqual(
            canonical_sha256(runtime), self.expected["runtime_result_sha256"]
        )

    def test_convergence_query_preserves_unrelated_folds_and_engineered_warning(self) -> None:
        rows = self.expected["relationship_query_results"][
            "atlas10.query.convergent-strategy"
        ]
        by_case = {row["case_id"]: row for row in rows}
        self.assertEqual(len(by_case), 2)
        self.assertEqual(
            by_case["atlas10.trypsin-fusarium.serine-protease"][
                "fold_classification_ids"
            ],
            "CATH:2.40.10.10",
        )
        subtilisin = by_case[
            "atlas10.subtilisin-bpn-bacillus.serine-protease"
        ]
        self.assertEqual(subtilisin["fold_classification_ids"], "CATH:3.40.50.200")
        self.assertIn("1S01[engineered_source_reference", subtilisin["source_applicability"])
        self.assertIn("1SUP[direct", subtilisin["source_applicability"])
        self.assertIn("record=NULL", subtilisin["reaction_or_source_gap"])

    def test_divergent_query_preserves_extra_domain_and_null_fingerprint(self) -> None:
        rows = self.expected["relationship_query_results"][
            "atlas10.query.shared-fold-divergent-chemistry"
        ]
        mal = next(
            row
            for row in rows
            if row["case_id"]
            == "atlas10.methylaspartate-lyase-ctetanomorphum.enolate"
        )
        self.assertIn("CATH:3.20.20.120", mal["fold_classification_ids"])
        self.assertIn("CATH:3.30.390.10", mal["fold_classification_ids"])
        self.assertTrue(mal["historical_fingerprint_bridge"].startswith("NULL;"))
        self.assertIn("inferred=1", mal["mechanism_steps_or_abstention"])

    def test_non_detailed_cyclophilin_has_zero_steps_and_machine_abstention(self) -> None:
        record = next(
            item
            for item in self.kernel["follow_on_records"]
            if item["case_id"] == "atlas10.cyclophilin-a-human.isomerization"
            and item["object_type"] == "mechanism_hypothesis"
        )
        self.assertEqual(record["mechanism_granularity"], "non_detailed")
        self.assertEqual(record["mechanism_proposals"][0]["mechanism_steps"], [])
        self.assertEqual(
            record["mechanism_proposals"][0]["scheme_retrieval_issues"][0]["status"],
            "source_link_missing_http_404",
        )
        self.assertTrue(record["detail_abstention"]["required"])
        self.assertIn(
            "ordered_elementary_steps",
            record["detail_abstention"]["unsupported_fields"],
        )

    def test_empty_source_roles_are_preserved_without_fabrication(self) -> None:
        record = next(
            item
            for item in self.kernel["follow_on_records"]
            if item["case_id"] == "atlas10.hewl-chicken.covalent-glycosidase"
            and item["object_type"] == "source_annotation"
        )
        sites = {site["site_id"]: site for site in record["sites"]}
        self.assertEqual(sites["P00698:N64"]["roles"], [])
        self.assertEqual(sites["P00698:D66"]["roles"], [])

    def test_fabricating_cyclophilin_steps_fails_closed(self) -> None:
        changed = copy.deepcopy(self.kernel)
        record = next(
            item
            for item in changed["follow_on_records"]
            if item["case_id"] == "atlas10.cyclophilin-a-human.isomerization"
            and item["object_type"] == "source_annotation"
        )
        record["mechanism_proposals"][0]["mechanism_steps"] = [{}]
        with self.assertRaisesRegex(ValueError, "fabricates detail"):
            validate_atlas10_kernel(
                changed,
                selection=self.selection,
                source_manifest=self.manifest,
                inherited_kernel=self.inherited,
            )

    def test_query_surface_rejects_multiple_statements(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one SELECT"):
            execute_atlas10_query(
                self.kernel, self.inherited, "SELECT 1; SELECT 2;"
            )


if __name__ == "__main__":
    unittest.main()
