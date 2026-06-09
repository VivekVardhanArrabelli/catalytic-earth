from __future__ import annotations

import hashlib
import unittest

from catalytic_earth.cli import build_parser
from catalytic_earth.external_bulk_scaleout_wave2 import (
    TERMINAL_STATES,
    build_external_bulk_scaleout_wave2,
    build_external_bulk_scaleout_wave2_provisional_import_preview,
    render_external_bulk_scaleout_wave2_report,
)


def _search_record(
    accession: str,
    *,
    sequence: str,
    ec_numbers: list[str] | None = None,
    pdb_ids: list[str] | None = None,
    alphafold_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "accession": accession,
        "reviewed": "reviewed",
        "protein_name": f"{accession} enzyme",
        "organism": "Test organism",
        "length": len(sequence),
        "sequence": sequence,
        "ec_numbers": ec_numbers or [],
        "pdb_ids": pdb_ids or [],
        "alphafold_ids": alphafold_ids or [],
    }


def _active_entry(accession: str, *, with_rhea: bool = True) -> dict[str, object]:
    return {
        "record": {
            "accession": accession,
            "entry_type": "UniProtKB reviewed (Swiss-Prot)",
            "sequence_length": 8,
            "active_site_features": [
                {
                    "feature_type": "Active site",
                    "begin": 3,
                    "end": 3,
                    "description": "Proton acceptor",
                    "ligand_name": None,
                    "ligand_id": None,
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
                    "ec_number": "3.1.3.1",
                    "cross_references": [{"database": "Rhea", "id": "RHEA:12345"}],
                    "evidence": [{"evidence_code": "ECO:0000269"}],
                }
            ]
            if with_rhea
            else [],
            "cofactor_comments": [],
        }
    }


class ExternalBulkScaleoutWave2Tests(unittest.TestCase):
    def test_routes_preview_duplicates_control_and_source_blocker(self) -> None:
        lanes = (
            {
                "lane_id": "positive",
                "target_family_lane": "metal hydrolase",
                "wave2_lane_group": "metal_hydrolase",
                "review_story_lane": "metal hydrolase",
                "boundary_role": "source_candidate",
                "mechanism_axis_focus": "metal_activated_water_hydrolysis",
                "query": "positive query",
            },
            {
                "lane_id": "control",
                "target_family_lane": "lyase controls",
                "wave2_lane_group": "lyase_isomerase_amidase_deaminase_controls",
                "review_story_lane": "lyase/isomerase/amidase/deaminase controls",
                "boundary_role": "lyase_isomerase_amidase_deaminase_control",
                "mechanism_axis_focus": "control",
                "query": "control query",
            },
        )
        by_query = {
            "positive query": [
                _search_record(
                    "PREADY",
                    sequence="MREADY",
                    ec_numbers=["3.1.3.1"],
                    pdb_ids=["1ABC"],
                    alphafold_ids=["PREADY"],
                ),
                _search_record(
                    "PDUP",
                    sequence="MDUP",
                    ec_numbers=["3.1.3.1"],
                    alphafold_ids=["PDUP"],
                ),
                _search_record(
                    "PPRIOR",
                    sequence="MPRIOR",
                    ec_numbers=["3.1.3.1"],
                    alphafold_ids=["PPRIOR"],
                ),
                _search_record(
                    "PBLOCK",
                    sequence="MBLOCK",
                    ec_numbers=["3.1.3.1"],
                    alphafold_ids=["PBLOCK"],
                ),
            ],
            "control query": [
                _search_record(
                    "PCTRL",
                    sequence="MCTRL",
                    ec_numbers=["4.2.1.1"],
                    alphafold_ids=["PCTRL"],
                )
            ],
        }

        def query_fetcher(query: str, size: int, max_pages: int) -> dict[str, object]:
            return {
                "metadata": {
                    "url": f"https://uniprot.test/{query}",
                    "record_count": len(by_query[query]),
                    "pages_fetched": max_pages,
                },
                "records": by_query[query][:size],
            }

        def entry_fetcher(accession: str) -> dict[str, object]:
            if accession == "PBLOCK":
                raise TimeoutError("entry timeout")
            return _active_entry(accession)

        artifact = build_external_bulk_scaleout_wave2(
            current_manifest_payload={
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "accession": "PDUP",
                        "sequence_sha256": hashlib.sha256(b"MDUP").hexdigest(),
                    }
                ]
            },
            label_registry_payload=[],
            prior_payloads=[
                {
                    "artifact_id": "prior",
                    "rows": [
                        {
                            "candidate_id": "uniprot:PPRIOR",
                            "accession": "PPRIOR",
                        }
                    ],
                }
            ],
            created_utc="2026-06-09T00:00:00Z",
            lane_queries=lanes,
            max_records_per_query=10,
            max_pages_per_query=2,
            max_candidates=10,
            max_candidates_per_lane=10,
            target_unique_non_duplicate_candidates=1,
            entry_fetch_workers=2,
            query_fetcher=query_fetcher,
            entry_fetcher=entry_fetcher,
            fetch_rhea_fallback=False,
        )

        self.assertTrue(artifact["validation_checks"]["passed"])
        by_accession = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(
            by_accession["PREADY"]["terminal_state"],
            "provisional_external_countable_preflight_candidate",
        )
        self.assertEqual(
            by_accession["PDUP"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(
            by_accession["PPRIOR"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(
            by_accession["PCTRL"]["terminal_state"], "reject/OOS_preserve_signal"
        )
        self.assertEqual(
            by_accession["PBLOCK"]["terminal_state"], "hard_blocked_with_next_action"
        )
        self.assertEqual(set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES), set())
        self.assertEqual(artifact["counts"]["provisional_import_preview_rows"], 1)
        self.assertEqual(artifact["counts"]["api_failure_rows"], 1)

        preview = build_external_bulk_scaleout_wave2_provisional_import_preview(
            artifact
        )
        self.assertEqual(preview["candidate_count"], 1)
        self.assertFalse(preview["rows"][0]["ready_for_production_label_import"])

        report = render_external_bulk_scaleout_wave2_report(artifact)
        self.assertIn("External Bulk Scaleout Wave 2", report)
        self.assertIn("Next Mechanical Continuation", report)

    def test_cli_parser_defaults_for_wave2_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["build-external-bulk-scaleout-wave2"])
        self.assertEqual(args.max_candidates, 9000)
        self.assertEqual(args.max_records_per_query, 250)
        self.assertEqual(args.target_unique_non_duplicate_candidates, 2500)
        self.assertIn("scaleout_wave2_current702_20260609", args.out)


if __name__ == "__main__":
    unittest.main()
