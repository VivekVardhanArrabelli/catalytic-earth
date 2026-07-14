from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas10_selection import load_atlas10_selection
from catalytic_earth.atlas10_sources import validate_atlas10_source_manifest


ROOT = Path(__file__).resolve().parents[2]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
MANIFEST_PATH = ROOT / "data/atlas/atlas10/source_manifest.json"


class Atlas10SourceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selection = load_atlas10_selection(SELECTION_PATH)
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_manifest_preserves_bindings_and_unique_acquisitions(self) -> None:
        summary = validate_atlas10_source_manifest(
            self.manifest,
            repo_root=ROOT,
            selection=self.selection,
        )
        self.assertEqual(summary["case_bindings"], 45)
        self.assertEqual(summary["unique_source_records"], 44)
        self.assertEqual(summary["bundled_snapshots"], 36)
        self.assertEqual(summary["reference_only_handles"], 8)
        self.assertEqual(summary["documented_rhea_gaps"], 3)
        self.assertEqual(summary["external_requests_used"], 64)

    def test_shared_enolase_cath_record_is_acquired_once_and_bound_twice(self) -> None:
        record_key = ("CATH", "CATH:3.20.20.120")
        records = [
            record
            for record in self.manifest["records"]
            if (record["source_id"], record["record_id"]) == record_key
        ]
        bindings = [
            binding
            for binding in self.manifest["bindings"]
            if (binding["source_id"], binding["record_id"]) == record_key
        ]
        self.assertEqual(len(records), 1)
        self.assertEqual(len(bindings), 2)

    def test_rhea_gaps_are_content_bound_zero_row_queries(self) -> None:
        gaps = [
            record
            for record in self.manifest["records"]
            if record["retrieval_status"] == "bundled_query_gap_snapshot"
        ]
        self.assertEqual(len(gaps), 3)
        for record in gaps:
            value = json.loads((ROOT / record["snapshot_path"]).read_text(encoding="utf-8"))
            self.assertEqual(value["query_result_kind"], "documented_zero_row_query")
            self.assertEqual(value["rows"], [])

    def test_cyclophilin_source_granularity_is_not_inferred_from_rating(self) -> None:
        record = next(
            item
            for item in self.manifest["records"]
            if item["source_id"] == "M-CSA" and item["record_id"] == "M0189"
        )
        value = json.loads((ROOT / record["snapshot_path"]).read_text(encoding="utf-8"))
        mechanisms = value["entry"]["reaction"]["mechanisms"]
        self.assertEqual(len(mechanisms), 1)
        self.assertIs(mechanisms[0]["is_detailed"], False)

    def test_cyclophilin_rhea_macromolecule_parts_are_source_bound(self) -> None:
        record = next(
            item
            for item in self.manifest["records"]
            if item["source_id"] == "Rhea" and item["record_id"] == "RHEA:16237"
        )
        value = json.loads((ROOT / record["snapshot_path"]).read_text(encoding="utf-8"))
        observed = {
            (item["accession"], item["reactive_chebi_uri"])
            for item in value["participant_rows"]
        }
        self.assertEqual(
            observed,
            {
                ("GENERIC:10747", "http://purl.obolibrary.org/obo/CHEBI_83833"),
                ("GENERIC:10748", "http://purl.obolibrary.org/obo/CHEBI_83834"),
            },
        )

    def test_mcsa_curved_arrow_schemes_are_content_bound(self) -> None:
        records = [
            item for item in self.manifest["records"] if item["source_id"] == "M-CSA"
        ]
        schemes = []
        for record in records:
            value = json.loads((ROOT / record["snapshot_path"]).read_text(encoding="utf-8"))
            schemes.extend(value["step_schemes"])
        self.assertEqual(len(schemes), 29)
        bundled = [
            scheme
            for scheme in schemes
            if scheme["retrieval_status"] == "bundled_linked_scheme"
        ]
        missing = [
            scheme
            for scheme in schemes
            if scheme["retrieval_status"] == "source_link_missing_http_404"
        ]
        self.assertEqual(len(bundled), 28)
        self.assertTrue(
            all(scheme["content_utf8"].lstrip().startswith("<cml") for scheme in bundled)
        )
        self.assertEqual(
            [(item["mechanism_id"], item["step_id"], item["http_status"]) for item in missing],
            [(1, 1, 404)],
        )

    def test_snapshot_hash_tampering_fails_closed(self) -> None:
        changed = copy.deepcopy(self.manifest)
        bundled = next(
            record for record in changed["records"] if record["snapshot_sha256"] is not None
        )
        bundled["snapshot_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "snapshot_sha256 differs"):
            validate_atlas10_source_manifest(
                changed,
                repo_root=ROOT,
                selection=self.selection,
            )


if __name__ == "__main__":
    unittest.main()
