from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.graph import build_seed_graph


class GraphTests(unittest.TestCase):
    @patch("catalytic_earth.graph.fetch_rhea_by_ec")
    @patch("catalytic_earth.graph.fetch_mcsa_sample")
    def test_build_seed_graph(self, mock_mcsa, mock_rhea) -> None:
        mock_mcsa.return_value = {
            "metadata": {"source": "m_csa", "url": "mock", "record_count": 1},
            "records": [
                {
                    "mcsa_id": 1,
                    "enzyme_name": "example enzyme",
                    "reference_uniprot_id": "P12345",
                    "ec_numbers": ["1.1.1.1"],
                    "reaction_ec": "1.1.1.1",
                    "mechanism_count": 1,
                    "residue_count": 1,
                    "catalytic_residues": [
                        {
                            "roles_summary": "proton acceptor",
                            "roles": [{"function": "proton acceptor"}],
                            "sequence_positions": [{"uniprot_id": "P12345", "code": "His", "resid": 10}],
                        }
                    ],
                }
            ],
        }
        mock_rhea.return_value = {
            "metadata": {"source": "rhea", "url": "mock", "record_count": 1},
            "records": [
                {
                    "rhea_id": "RHEA:1",
                    "equation": "A = B",
                    "ec_number": "1.1.1.1",
                }
            ],
        }

        graph = build_seed_graph([1])
        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertIn("m_csa:1", node_ids)
        self.assertIn("ec:1.1.1.1", node_ids)
        self.assertIn("rhea:RHEA:1", node_ids)
        self.assertGreaterEqual(graph["metadata"]["edge_count"], 3)


if __name__ == "__main__":
    unittest.main()
