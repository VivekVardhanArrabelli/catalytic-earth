from __future__ import annotations

import hashlib
import unittest

from catalytic_earth.cli import build_parser
from catalytic_earth.external_scaleout_redox_cofactor_confounded import (
    TERMINAL_STATES,
    build_external_scaleout_redox_cofactor_confounded_import_ready_preview,
    build_external_scaleout_redox_cofactor_confounded_shard,
    render_external_scaleout_redox_cofactor_confounded_report,
)


def _search_record(
    accession: str,
    *,
    sequence: str,
    ec_numbers: list[str] | None = None,
    alphafold_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "accession": accession,
        "reviewed": "reviewed",
        "protein_name": f"{accession} redox enzyme",
        "organism": "Test organism",
        "length": len(sequence),
        "sequence": sequence,
        "ec_numbers": ec_numbers or [],
        "pdb_ids": [],
        "alphafold_ids": alphafold_ids or [],
    }


def _entry(
    accession: str,
    *,
    with_rhea: bool = True,
    with_feature: bool = True,
    cofactor_name: str = "FAD",
) -> dict[str, object]:
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
            ]
            if with_feature
            else [],
            "binding_site_features": [],
            "metal_binding_features": [],
            "site_features": [],
            "modified_residue_features": [],
            "cross_link_features": [],
            "catalytic_activity_comments": [
                {
                    "reaction": "test redox reaction",
                    "ec_number": "1.14.13.1",
                    "cross_references": [{"database": "Rhea", "id": "RHEA:12345"}],
                    "evidence": [{"evidence_code": "ECO:0000269"}],
                }
            ]
            if with_rhea
            else [],
            "cofactor_comments": [
                {
                    "cofactors": [
                        {
                            "name": cofactor_name,
                            "cross_reference": {
                                "database": "ChEBI",
                                "id": "CHEBI:16238",
                            },
                            "evidence": [{"evidence_code": "ECO:0000269"}],
                        }
                    ]
                }
            ],
        }
    }


class ExternalScaleoutRedoxCofactorConfoundedTests(unittest.TestCase):
    def test_routes_import_ready_prior_duplicate_oos_and_locator_ready(self) -> None:
        lanes = (
            {
                "lane_id": "positive",
                "target_family_lane": "flavin monooxygenase",
                "boundary_class": "flavin_monooxygenase_dehydrogenase_boundary",
                "boundary_role": "source_candidate",
                "query": "positive query",
            },
            {
                "lane_id": "oos",
                "target_family_lane": "dehydrogenase/reductase OOS boundary",
                "boundary_class": "dehydrogenase_reductase_boundary",
                "boundary_role": "cofactor_confounded_oos_negative",
                "query": "oos query",
            },
        )
        search_by_query = {
            "positive query": [
                _search_record(
                    "PREADY",
                    sequence="MREADY",
                    ec_numbers=["1.14.13.1"],
                    alphafold_ids=["PREADY"],
                ),
                _search_record(
                    "PPRIOR",
                    sequence="MPRIOR",
                    ec_numbers=["1.14.13.1"],
                    alphafold_ids=["PPRIOR"],
                ),
                _search_record(
                    "PDUP",
                    sequence="MDUP",
                    ec_numbers=["1.14.13.1"],
                    alphafold_ids=["PDUP"],
                ),
                _search_record("PLOC", sequence="MLOC", alphafold_ids=["PLOC"]),
            ],
            "oos query": [
                _search_record(
                    "POOS",
                    sequence="MOOS",
                    ec_numbers=["1.6.5.1"],
                    alphafold_ids=["POOS"],
                )
            ],
        }

        def query_fetcher(query: str, size: int) -> dict[str, object]:
            return {
                "metadata": {"url": f"https://uniprot.test/{query}", "query": query},
                "records": search_by_query[query][:size],
            }

        def entry_fetcher(accession: str) -> dict[str, object]:
            if accession == "PLOC":
                return _entry(accession, with_rhea=False)
            return _entry(accession)

        artifact = build_external_scaleout_redox_cofactor_confounded_shard(
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
                    "rows": [{"candidate_id": "uniprot:PPRIOR", "accession": "PPRIOR"}],
                }
            ],
            created_utc="2026-06-09T00:00:00Z",
            lane_queries=lanes,
            max_records_per_lane=10,
            max_candidates=10,
            target_unique_candidates=1,
            stretch_unique_candidates=1,
            entry_fetch_workers=2,
            query_fetcher=query_fetcher,
            entry_fetcher=entry_fetcher,
            fetch_rhea_fallback=False,
        )

        by_accession = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(by_accession["PREADY"]["terminal_state"], "import_ready_preview")
        self.assertEqual(
            by_accession["PPRIOR"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(
            by_accession["PDUP"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(by_accession["POOS"]["terminal_state"], "reject/OOS_preserve_signal")
        self.assertEqual(by_accession["PLOC"]["terminal_state"], "locator_ready_candidate")
        self.assertEqual(set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES), set())
        self.assertTrue(artifact["validation_checks"]["passed"])

        preview = build_external_scaleout_redox_cofactor_confounded_import_ready_preview(
            artifact
        )
        self.assertEqual(preview["candidate_count"], 1)
        self.assertFalse(preview["rows"][0]["ready_for_production_label_import"])

        report = render_external_scaleout_redox_cofactor_confounded_report(artifact)
        self.assertIn("Family-Selection Rationale", report)
        self.assertIn("Boundary Classes Covered", report)

    def test_cli_parser_defaults_for_redox_cofactor_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            ["build-external-scaleout-redox-cofactor-confounded-shard"]
        )
        self.assertEqual(args.max_candidates, 4200)
        self.assertEqual(args.entry_fetch_workers, 12)
        self.assertIn("redox_cofactor_confounded", args.out)


if __name__ == "__main__":
    unittest.main()
