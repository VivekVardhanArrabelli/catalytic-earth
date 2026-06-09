from __future__ import annotations

import hashlib
import unittest

from catalytic_earth.cli import build_parser
from catalytic_earth.external_scaleout_near_orphan_diversity import (
    TERMINAL_STATES,
    build_external_scaleout_near_orphan_diversity_import_ready_preview,
    build_external_scaleout_near_orphan_diversity_shard,
    render_external_scaleout_near_orphan_diversity_report,
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
        "protein_name": f"{accession} diversity enzyme",
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
    cofactor_name: str = "magnesium",
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
                    "description": "Catalytic residue",
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
                    "reaction": "test diversity reaction",
                    "ec_number": "4.2.3.1",
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
                                "id": "CHEBI:25107",
                            },
                            "evidence": [{"evidence_code": "ECO:0000269"}],
                        }
                    ]
                }
            ],
        }
    }


class ExternalScaleoutNearOrphanDiversityTests(unittest.TestCase):
    def test_routes_import_ready_provisional_duplicate_no_structure_and_oos(self) -> None:
        lanes = (
            {
                "lane_id": "source",
                "target_family_lane": "terpene synthase/lyase",
                "diversity_bin": "terpene_lyase",
                "boundary_class": "terpene_lyase_isomerase_transferase",
                "boundary_role": "sparse_family_source_candidate",
                "import_route": "import_ready_preview",
                "query": "source query",
            },
            {
                "lane_id": "near",
                "target_family_lane": "near-orphan/no-reliable-structure",
                "diversity_bin": "near_orphan_low_annotation",
                "boundary_class": "near_orphan_no_reliable_structure",
                "boundary_role": "near_orphan_source_candidate",
                "import_route": "provisional",
                "query": "near query",
            },
            {
                "lane_id": "oos",
                "target_family_lane": "ATPase/transporter OOS hard negative",
                "diversity_bin": "transport_atpase_oos",
                "boundary_class": "oos_hard_negative_abstention_probe",
                "boundary_role": "oos_hard_negative",
                "import_route": "reject",
                "query": "oos query",
            },
        )
        search_by_query = {
            "source query": [
                _search_record(
                    "PREADY",
                    sequence="MREADY",
                    ec_numbers=["4.2.3.1"],
                    alphafold_ids=["PREADY"],
                ),
                _search_record(
                    "PPRIOR",
                    sequence="MPRIOR",
                    ec_numbers=["4.2.3.1"],
                    alphafold_ids=["PPRIOR"],
                ),
                _search_record(
                    "PDUP",
                    sequence="MDUP",
                    ec_numbers=["4.2.3.1"],
                    alphafold_ids=["PDUP"],
                ),
            ],
            "near query": [
                _search_record(
                    "PPROV",
                    sequence="MPROV",
                    ec_numbers=["4.2.3.1"],
                    alphafold_ids=["PPROV"],
                ),
                _search_record("PNOSTR", sequence="MNOSTR", ec_numbers=["4.2.3.1"]),
            ],
            "oos query": [
                _search_record(
                    "POOS",
                    sequence="MOOS",
                    ec_numbers=["6.3.1.1"],
                    alphafold_ids=["POOS"],
                )
            ],
        }

        def query_fetcher(query: str, size: int) -> dict[str, object]:
            return {
                "metadata": {"url": f"https://uniprot.test/{query}", "query": query},
                "records": search_by_query[query][:size],
            }

        artifact = build_external_scaleout_near_orphan_diversity_shard(
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
            entry_fetcher=_entry,
            fetch_rhea_fallback=False,
        )

        by_accession = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(by_accession["PREADY"]["terminal_state"], "import_ready_preview")
        self.assertEqual(
            by_accession["PPROV"]["terminal_state"],
            "provisional_external_countable_preflight_candidate",
        )
        self.assertEqual(
            by_accession["PPRIOR"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(
            by_accession["PDUP"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(by_accession["POOS"]["terminal_state"], "reject/OOS_preserve_signal")
        self.assertEqual(
            by_accession["PNOSTR"]["terminal_state"],
            "coordinate_repair_candidate",
        )
        self.assertTrue(
            by_accession["PNOSTR"]["no_structure_route"][
                "explicit_no_structure_or_provenance_route"
            ]
        )
        self.assertEqual(set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES), set())
        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertEqual(artifact["counts"]["import_ready_preview_rows"], 1)
        self.assertEqual(
            artifact["counts"][
                "provisional_external_countable_preflight_candidate_rows"
            ],
            1,
        )
        self.assertEqual(artifact["counts"]["reject_oos_preserve_signal_rows"], 1)

        preview = build_external_scaleout_near_orphan_diversity_import_ready_preview(
            artifact
        )
        self.assertEqual(preview["candidate_count"], 1)
        self.assertFalse(preview["rows"][0]["ready_for_production_label_import"])

        report = render_external_scaleout_near_orphan_diversity_report(artifact)
        self.assertIn("Diversity Bins", report)
        self.assertIn("No-structure/no-reliable-structure rows", report)

    def test_cli_parser_defaults_for_near_orphan_diversity_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            ["build-external-scaleout-near-orphan-diversity-shard"]
        )
        self.assertEqual(args.max_candidates, 4500)
        self.assertEqual(args.entry_fetch_workers, 12)
        self.assertIn("near_orphan_diversity", args.out)


if __name__ == "__main__":
    unittest.main()
