from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.v2 import (
    build_mechanism_benchmark,
    detect_inconsistencies,
    run_baseline_retrieval,
    write_candidate_dossiers,
    write_v2_report,
)


class V2Tests(unittest.TestCase):
    def sample_graph(self) -> dict:
        return {
            "nodes": [
                {"id": "m_csa:1", "type": "m_csa_entry", "name": "serine hydrolase"},
                {"id": "ec:1.1.1.1", "type": "ec_number", "ec_number": "1.1.1.1"},
                {"id": "rhea:RHEA:1", "type": "rhea_reaction", "rhea_id": "RHEA:1"},
                {
                    "id": "uniprot:P12345",
                    "type": "protein",
                    "ec_numbers": [],
                    "accession": "P12345",
                },
                {
                    "id": "m_csa:1:residue:1",
                    "type": "catalytic_residue",
                    "roles": ["nucleophile", "proton acceptor"],
                    "sequence_positions": [{"code": "Ser"}],
                },
                {
                    "id": "m_csa:1:mechanism:1",
                    "type": "mechanism_text",
                    "text": "serine attacks an acyl bond",
                },
            ],
            "edges": [
                {"source": "m_csa:1", "target": "ec:1.1.1.1", "predicate": "has_ec"},
                {"source": "ec:1.1.1.1", "target": "rhea:RHEA:1", "predicate": "maps_to_reaction"},
                {
                    "source": "m_csa:1",
                    "target": "uniprot:P12345",
                    "predicate": "has_reference_protein",
                },
                {
                    "source": "m_csa:1",
                    "target": "m_csa:1:residue:1",
                    "predicate": "has_catalytic_residue",
                },
                {
                    "source": "m_csa:1",
                    "target": "m_csa:1:mechanism:1",
                    "predicate": "has_mechanism_text",
                },
            ],
        }

    def test_benchmark_and_baseline(self) -> None:
        benchmark = build_mechanism_benchmark(self.sample_graph())
        self.assertEqual(benchmark["metadata"]["record_count"], 1)
        record = benchmark["records"][0]
        self.assertIn("ec_node_ids", record["blocked_leakage_fields"])
        self.assertNotIn("ec_numbers", record["allowed_features"])

        baseline = run_baseline_retrieval(benchmark)
        self.assertEqual(baseline["metadata"]["record_count"], 1)
        self.assertTrue(baseline["results"][0]["leakage_control_checked"])

    def test_inconsistency_detection(self) -> None:
        issues = detect_inconsistencies(self.sample_graph())
        issue_types = {issue["issue_type"] for issue in issues["issues"]}
        self.assertIn("ec_mismatch", issue_types)
        self.assertIn("missing_structure_cross_reference", issue_types)

    def test_dossiers_and_report(self) -> None:
        candidates = {
            "metadata": {"record_count": 1},
            "candidates": [
                {
                    "accession": "P12345",
                    "protein_name": "putative hydrolase",
                    "organism": "Example",
                    "length": 250,
                    "score": 7,
                    "reviewed": "unreviewed",
                    "motif_count": 1,
                    "motifs": [{"motif": "GASAG", "start": 10, "end": 14}],
                    "evidence": ["example evidence"],
                    "uncertainty": ["example uncertainty"],
                    "mechanistic_hypothesis": "possible hydrolase",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            written = write_candidate_dossiers(candidates, Path(tmpdir), top=1)
            self.assertEqual(len(written), 1)
            self.assertIn("Validation Boundary", Path(written[0]).read_text())

        report = write_v2_report(
            graph_summary={"node_count": 1, "edge_count": 1, "node_types": {"protein": 1}},
            benchmark={"metadata": {"record_count": 1, "leakage_control": "blocked"}},
            baseline={"metadata": {"method": "baseline", "fingerprint_count": 6}},
            inconsistencies={"metadata": {"issue_count": 1, "issue_types": {"ec_mismatch": 1}}},
            candidates=candidates,
        )
        self.assertIn("Catalytic Earth V2 Research Report", report)
        self.assertIn("P12345", report)


if __name__ == "__main__":
    unittest.main()
