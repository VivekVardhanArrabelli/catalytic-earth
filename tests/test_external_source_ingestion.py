from __future__ import annotations

import hashlib
import unittest

from catalytic_earth.external_source_ingestion import (
    build_external_source_ingestion_import_preview,
    build_external_source_ingestion_pilot,
    render_external_source_ingestion_report,
)


LANES = (
    {
        "lane_id": "test_lane",
        "target_family_lane": "phosphoryl transfer",
        "query": "test query",
    },
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


def _active_entry(accession: str) -> dict[str, object]:
    return {
        "record": {
            "accession": accession,
            "entry_type": "UniProtKB reviewed (Swiss-Prot)",
            "sequence_length": 4,
            "active_site_features": [
                {
                    "feature_type": "Active site",
                    "begin": 2,
                    "end": 2,
                    "description": "Nucleophile",
                    "ligand_name": None,
                    "ligand_id": None,
                    "ligand_note": None,
                    "evidence": [
                        {
                            "evidence_code": "ECO:0000269",
                            "source": "PubMed",
                            "id": "1",
                        }
                    ],
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
                    "ec_number": "2.7.1.26",
                    "cross_references": [{"database": "Rhea", "id": "RHEA:14357"}],
                    "evidence": [
                        {
                            "evidence_code": "ECO:0000269",
                            "source": "PubMed",
                            "id": "1",
                        }
                    ],
                }
            ],
            "cofactor_comments": [],
        }
    }


class ExternalSourceIngestionTests(unittest.TestCase):
    def test_routes_rows_to_preflight_duplicate_and_locator_states(self) -> None:
        current_manifest = {
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "accession": "PDUP",
                    "sequence_sha256": hashlib.sha256(b"MDUP").hexdigest(),
                    "real_sequence_accessions": ["PDUP"],
                    "sequence_records": [],
                }
            ]
        }
        labels = [{"entry_id": "uniprot:POLD"}]
        search_records = [
            _search_record(
                "PNEW",
                sequence="MNEW",
                ec_numbers=["2.7.1.26"],
                pdb_ids=["1ABC"],
                alphafold_ids=["PNEW"],
            ),
            _search_record(
                "PDUP",
                sequence="MDUP",
                ec_numbers=["2.7.1.26"],
                pdb_ids=["2ABC"],
                alphafold_ids=["PDUP"],
            ),
            _search_record("PLOC", sequence="MLOC", alphafold_ids=["PLOC"]),
        ]

        def query_fetcher(query: str, size: int) -> dict[str, object]:
            return {
                "metadata": {"url": "https://uniprot.test/search", "record_count": 3},
                "records": search_records[:size],
            }

        def entry_fetcher(accession: str) -> dict[str, object]:
            if accession == "PLOC":
                return {
                    "record": {
                        "accession": accession,
                        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
                        "active_site_features": [],
                        "binding_site_features": [],
                        "metal_binding_features": [],
                        "site_features": [],
                        "modified_residue_features": [],
                        "cross_link_features": [],
                        "catalytic_activity_comments": [],
                        "cofactor_comments": [],
                    }
                }
            return _active_entry(accession)

        artifact = build_external_source_ingestion_pilot(
            current_manifest_payload=current_manifest,
            label_registry_payload=labels,
            created_utc="2026-06-08T00:00:00Z",
            max_records_per_lane=3,
            lane_queries=LANES,
            query_fetcher=query_fetcher,
            entry_fetcher=entry_fetcher,
            fetch_rhea_fallback=False,
        )

        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertEqual(artifact["candidate_count"], 3)
        rows = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(
            rows["PNEW"]["terminal_state"],
            "external_countable_preflight_candidate",
        )
        self.assertEqual(
            rows["PDUP"]["terminal_state"],
            "blocked_duplicate_or_current_registry_conflict",
        )
        self.assertEqual(
            rows["PLOC"]["terminal_state"],
            "coordinate_ready_pending_locator",
        )
        self.assertFalse(rows["PNEW"]["guardrails"]["label_import_performed"])
        self.assertEqual(rows["PNEW"]["source_evidence_codes"], ["ECO:0000269"])

        preview = build_external_source_ingestion_import_preview(artifact)
        self.assertEqual(preview["candidate_count"], 1)
        self.assertFalse(preview["rows"][0]["ready_for_production_label_import"])

        report = render_external_source_ingestion_report(artifact)
        self.assertIn("External Source Ingestion Pilot", report)
        self.assertIn("external_countable_preflight_candidate", report)


if __name__ == "__main__":
    unittest.main()
