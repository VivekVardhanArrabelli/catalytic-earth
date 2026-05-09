from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.graph import assemble_knowledge_graph, build_seed_graph, summarize_graph


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
                    "reference_uniprot_ids": ["P12345"],
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

    def test_assemble_knowledge_graph(self) -> None:
        graph = assemble_knowledge_graph(
            mcsa_records=[
                {
                    "mcsa_id": 1,
                    "enzyme_name": "example enzyme",
                    "reference_uniprot_id": "P12345",
                    "ec_numbers": ["1.1.1.1"],
                    "reaction_ec": "1.1.1.1",
                    "mechanism_count": 1,
                    "residue_count": 1,
                    "compound_count": 2,
                    "catalytic_residues": [
                        {
                            "roles_summary": "proton acceptor",
                            "roles": [{"function": "proton acceptor"}],
                            "sequence_positions": [{"uniprot_id": "P12345", "code": "His", "resid": 10}],
                            "structure_positions": [{"pdb_id": "1abc", "chain_name": "A"}],
                        }
                    ],
                    "mechanism_summaries": [
                        {"mechanism_id": 7, "is_detailed": True, "text": "example"}
                    ],
                }
            ],
            rhea_by_ec={
                "1.1.1.1": {
                    "records": [
                        {"rhea_id": "RHEA:1", "equation": "A = B", "ec_number": "1.1.1.1"}
                    ]
                }
            },
            uniprot_records=[
                {
                    "accession": "P12345",
                    "entry_name": "EXAMPLE",
                    "protein_name": "Example",
                    "organism": "Example organism",
                    "length": 100,
                    "ec_numbers": ["1.1.1.1"],
                    "pdb_ids": ["1ABC"],
                    "alphafold_ids": ["P12345"],
                }
            ],
        )
        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertIn("uniprot:P12345", node_ids)
        self.assertIn("pdb:1ABC", node_ids)
        self.assertIn("alphafold:P12345", node_ids)
        self.assertIn("m_csa:1:mechanism:7", node_ids)
        self.assertEqual(graph["metadata"]["schema_version"], "0.1.0")
        self.assertGreater(graph["summary"]["provenance_sources"]["m_csa"], 0)

    def test_summary_counts(self) -> None:
        summary = summarize_graph(
            {
                "nodes": [{"id": "a", "type": "protein", "provenance": [{"source": "uniprot"}]}],
                "edges": [{"source": "a", "target": "b", "predicate": "has_structure"}],
            }
        )
        self.assertEqual(summary["node_types"]["protein"], 1)
        self.assertEqual(summary["edge_predicates"]["has_structure"], 1)


if __name__ == "__main__":
    unittest.main()
