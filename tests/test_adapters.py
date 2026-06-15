from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth import adapters
from catalytic_earth.adapters import (
    build_mcsa_entries_url,
    build_mcsa_page_url,
    build_rhea_ec_url,
    build_rhea_sample_url,
    build_uniprot_accessions_url,
    build_uniprot_query_url,
    fetch_uniprot_query,
    normalize_mcsa_entries,
    normalize_rhea_tsv,
    normalize_uniprot_tsv,
)


class AdapterTests(unittest.TestCase):
    def test_rhea_url_and_normalization(self) -> None:
        url = build_rhea_sample_url(3)
        self.assertIn("format=tsv", url)
        ec_url = build_rhea_ec_url("5.1.1.3")
        self.assertIn("ec%3A5.1.1.3", ec_url)

        records = normalize_rhea_tsv(
            "Reaction identifier\tEquation\tEC number\tEnzymes\n"
            "RHEA:1\tA = B\tEC:1.1.1.1\t12\n"
        )
        self.assertEqual(records[0]["rhea_id"], "RHEA:1")
        self.assertEqual(records[0]["ec_number"], "1.1.1.1")
        self.assertEqual(records[0]["mapped_enzyme_count"], 12)

    def test_mcsa_url_and_normalization(self) -> None:
        url = build_mcsa_entries_url([1, 2])
        self.assertIn("entries.mcsa_ids=1%2C2", url)
        page_url = build_mcsa_page_url(page=2, page_size=5)
        self.assertIn("page=2", page_url)
        self.assertIn("page_size=5", page_url)

        records = normalize_mcsa_entries(
            {
                "results": [
                    {
                        "mcsa_id": 1,
                        "enzyme_name": "example enzyme",
                        "reference_uniprot_id": "P12345, Q99999",
                        "all_ecs": ["1.1.1.1"],
                        "reaction": {
                            "ec": "1.1.1.1",
                            "compounds": [{"name": "A"}, {"name": "B"}],
                            "mechanisms": [
                                {
                                    "mechanism_id": 1,
                                    "is_detailed": True,
                                    "mechanism_text": "example mechanism",
                                }
                            ],
                        },
                        "residues": [
                            {
                                "roles_summary": "proton acceptor",
                                "roles": [{"function_type": "interaction", "function": "proton acceptor"}],
                                "residue_sequences": [{"uniprot_id": "P12345", "code": "His", "resid": 10}],
                                "residue_chains": [{"pdb_id": "1abc", "chain_name": "A", "code": "His", "resid": 10}],
                            }
                        ],
                    }
                ]
            }
        )
        self.assertEqual(records[0]["mcsa_id"], 1)
        self.assertEqual(records[0]["reference_uniprot_ids"], ["P12345", "Q99999"])
        self.assertEqual(records[0]["compound_count"], 2)
        self.assertEqual(records[0]["catalytic_residues"][0]["sequence_positions"][0]["code"], "His")

    def test_uniprot_url_and_normalization(self) -> None:
        url = build_uniprot_accessions_url(["P56868", "P0A9K9"])
        self.assertIn("format=tsv", url)
        paged_url = build_uniprot_query_url("reviewed:true", size=50, offset=100)
        self.assertIn("offset=100", paged_url)
        records = normalize_uniprot_tsv(
            "Entry\tEntry Name\tProtein names\tOrganism\tLength\tEC number\tPDB\tAlphaFoldDB\n"
            "P56868\tMURI_AQUPY\tGlutamate racemase\tAquifex pyrophilus\t254\t5.1.1.3\t1B73;1B74;\tP56868;\n"
        )
        self.assertEqual(records[0]["accession"], "P56868")
        self.assertEqual(records[0]["length"], 254)
        self.assertEqual(records[0]["pdb_ids"], ["1B73", "1B74"])
        self.assertEqual(records[0]["alphafold_ids"], ["P56868"])

    def test_fetch_uniprot_query_honors_initial_offset(self) -> None:
        fetched_urls: list[str] = []

        def fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            accession = f"P{len(fetched_urls):05d}"
            return (
                "Entry\tEntry Name\tProtein names\tOrganism\tLength\tEC number\tPDB\tAlphaFoldDB\n"
                f"{accession}\tENTRY_{len(fetched_urls)}\tExample\tOrganism\t10\t\t\t\n"
            )

        with patch.object(adapters, "_fetch_text", side_effect=fake_fetch):
            payload = fetch_uniprot_query("reviewed:true", size=1, max_pages=2, offset=5)

        self.assertEqual([page["offset"] for page in payload["metadata"]["pages"]], [5, 6])
        self.assertIn("offset=5", fetched_urls[0])
        self.assertIn("offset=6", fetched_urls[1])
        self.assertEqual([record["accession"] for record in payload["records"]], ["P00001", "P00002"])


if __name__ == "__main__":
    unittest.main()
