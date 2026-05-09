from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.adapters import (
    build_mcsa_entries_url,
    build_rhea_ec_url,
    build_rhea_sample_url,
    normalize_mcsa_entries,
    normalize_rhea_tsv,
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

        records = normalize_mcsa_entries(
            {
                "results": [
                    {
                        "mcsa_id": 1,
                        "enzyme_name": "example enzyme",
                        "reference_uniprot_id": "P12345",
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
        self.assertEqual(records[0]["compound_count"], 2)
        self.assertEqual(records[0]["catalytic_residues"][0]["sequence_positions"][0]["code"], "His")


if __name__ == "__main__":
    unittest.main()
