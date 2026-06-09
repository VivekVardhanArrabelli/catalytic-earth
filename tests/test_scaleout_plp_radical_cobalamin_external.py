from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.scaleout_plp_radical_cobalamin_external import (
    TERMINAL_STATES,
    build_external_scaleout_import_ready_preview,
    build_external_scaleout_shard_plp_radical_cobalamin,
    render_external_scaleout_report,
    write_external_scaleout_shard_plp_radical_cobalamin,
)


LANES = (
    {
        "lane_id": "plp_test",
        "target_family_lane": "PLP test",
        "lane_group": "plp",
        "mechanism_axis_focus": "proton_transfer_test",
        "query": "plp query",
    },
    {
        "lane_id": "negative_test",
        "target_family_lane": "negative test",
        "lane_group": "adjacent_cofactor_confounded_negative",
        "mechanism_axis_focus": "negative_control_test",
        "query": "negative query",
    },
)


def _search_record(
    accession: str,
    *,
    sequence: str,
    pdb_ids: list[str] | None = None,
    alphafold_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "accession": accession,
        "reviewed": "reviewed",
        "protein_name": f"{accession} PLP enzyme",
        "organism": "Test organism",
        "length": len(sequence),
        "sequence": sequence,
        "ec_numbers": ["2.6.1.1"],
        "pdb_ids": pdb_ids or [],
        "alphafold_ids": alphafold_ids or [],
    }


def _entry(accession: str) -> dict[str, object]:
    return {
        "record": {
            "accession": accession,
            "entry_type": "UniProtKB reviewed (Swiss-Prot)",
            "sequence_length": 9,
            "active_site_features": [
                {
                    "feature_type": "Active site",
                    "begin": 3,
                    "end": 3,
                    "description": "PLP Schiff-base lysine",
                    "ligand_name": "pyridoxal phosphate",
                    "ligand_id": "ChEBI:CHEBI:597326",
                    "ligand_note": None,
                    "evidence": [{"evidence_code": "ECO:0000269"}],
                    "cross_references": [],
                }
            ],
            "binding_site_features": [],
            "metal_binding_features": [],
            "site_features": [],
            "modified_residue_features": [],
            "cross_link_features": [],
            "catalytic_activity_comments": [
                {
                    "reaction": "test reaction",
                    "ec_number": "2.6.1.1",
                    "cross_references": [{"database": "Rhea", "id": "RHEA:12345"}],
                    "evidence": [{"evidence_code": "ECO:0000269"}],
                }
            ],
            "cofactor_comments": [
                {
                    "cofactors": [
                        {
                            "name": "pyridoxal phosphate",
                            "cross_reference": "ChEBI:CHEBI:597326",
                            "evidence_codes": ["ECO:0000269"],
                        }
                    ]
                }
            ],
        }
    }


class PlpRadicalCobalaminExternalScaleoutTests(unittest.TestCase):
    def test_build_routes_import_ready_provisional_duplicate_and_negative(self) -> None:
        current_manifest = {"rows": []}
        labels: list[dict[str, object]] = []
        records_by_query = {
            "plp query": [
                _search_record("PREADY", sequence="MAAAKAAAC", pdb_ids=["1ABC"]),
                _search_record("PPROV", sequence="MCCCACCAC", alphafold_ids=["PPROV"]),
                _search_record("PDUP", sequence="MDDDD", pdb_ids=["2ABC"]),
            ],
            "negative query": [
                _search_record("PNEG", sequence="MNNNN", pdb_ids=["3ABC"]),
            ],
        }
        prior_payloads = [
            (
                "prior",
                {
                    "artifact_id": "prior_artifact",
                    "rows": [{"candidate_id": "uniprot:PDUP", "accession": "PDUP"}],
                },
            )
        ]

        def query_fetcher(query: str, size: int, max_pages: int) -> dict[str, object]:
            records = records_by_query[query]
            return {
                "metadata": {
                    "url": "https://uniprot.test/search",
                    "record_count": len(records),
                    "pages_fetched": max_pages,
                    "pages": [{"url": "https://uniprot.test/search"}],
                },
                "records": records[:size],
            }

        artifact = build_external_scaleout_shard_plp_radical_cobalamin(
            current_manifest_payload=current_manifest,
            label_registry_payload=labels,
            prior_external_payloads=prior_payloads,
            created_utc="2026-06-09T00:00:00Z",
            max_records_per_query=10,
            max_pages_per_query=2,
            max_candidates=10,
            target_candidate_floor=4,
            lane_queries=LANES,
            query_fetcher=query_fetcher,
            entry_fetcher=_entry,
            entry_fetch_workers=1,
        )

        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertEqual(artifact["candidate_count"], 4)
        rows = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(rows["PREADY"]["terminal_state"], "import_ready_preview")
        self.assertEqual(
            rows["PPROV"]["terminal_state"],
            "provisional_external_countable_preflight_candidate",
        )
        self.assertEqual(
            rows["PDUP"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(rows["PNEG"]["terminal_state"], "reject/OOS_preserve_signal")
        self.assertIn("proton_transfer_axis", rows["PREADY"]["mechanism_axis_coverage"])
        self.assertEqual(set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES), set())

        preview = build_external_scaleout_import_ready_preview(artifact)
        self.assertEqual(preview["candidate_count"], 1)
        self.assertFalse(preview["rows"][0]["ready_for_production_label_import"])

        report = render_external_scaleout_report(artifact)
        self.assertIn("Mechanism-Axis Coverage", report)
        self.assertIn("PLP test", report)

    def test_write_outputs_json_report_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            labels = root / "labels.json"
            out = root / "out.json"
            report = root / "report.md"
            preview = root / "preview.json"
            manifest.write_text(json.dumps({"rows": []}), encoding="utf-8")
            labels.write_text("[]", encoding="utf-8")

            def query_fetcher(query: str, size: int, max_pages: int) -> dict[str, object]:
                return {
                    "metadata": {"record_count": 1, "pages": [], "pages_fetched": 1},
                    "records": [_search_record("PREADY", sequence="MAAAK", pdb_ids=["1ABC"])],
                }

            artifact = build_external_scaleout_shard_plp_radical_cobalamin(
                current_manifest_payload={"rows": []},
                label_registry_payload=[],
                prior_external_payloads=[],
                created_utc="2026-06-09T00:00:00Z",
                max_records_per_query=5,
                max_pages_per_query=1,
                max_candidates=1,
                target_candidate_floor=1,
                lane_queries=LANES[:1],
                query_fetcher=query_fetcher,
                entry_fetcher=_entry,
                entry_fetch_workers=1,
            )
            out.write_text(json.dumps(artifact), encoding="utf-8")

            written = write_external_scaleout_shard_plp_radical_cobalamin(
                current_manifest_path=manifest,
                label_registry_path=labels,
                prior_external_paths=(),
                prior_external_branch_specs=(),
                out_path=out,
                report_path=report,
                import_ready_path=preview,
                created_utc="2026-06-09T00:00:00Z",
                max_records_per_query=5,
                max_pages_per_query=1,
                max_candidates=1,
                target_candidate_floor=1,
                entry_fetch_workers=1,
                lane_queries=LANES[:1],
                query_fetcher=query_fetcher,
                entry_fetcher=_entry,
            )

            self.assertEqual(written["candidate_count"], 1)
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertTrue(preview.exists())


if __name__ == "__main__":
    unittest.main()
