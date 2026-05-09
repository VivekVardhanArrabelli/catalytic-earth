from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.performance import run_local_performance_suite


class PerformanceTests(unittest.TestCase):
    def test_run_local_performance_suite(self) -> None:
        graph = ROOT / "artifacts" / "v1_graph.json"
        geometry = ROOT / "artifacts" / "v3_geometry_features.json"
        retrieval = ROOT / "artifacts" / "v3_geometry_retrieval.json"
        report = run_local_performance_suite(graph, geometry, retrieval, iterations=1)
        self.assertEqual(report["metadata"]["iterations"], 1)
        self.assertIsInstance(report["metadata"]["selected_abstain_threshold"], float)
        self.assertGreaterEqual(len(report["benchmarks"]), 8)
        self.assertIn(
            "analyze_structure_mapping_issues",
            {benchmark["name"] for benchmark in report["benchmarks"]},
        )
        self.assertIn(
            "analyze_cofactor_coverage",
            {benchmark["name"] for benchmark in report["benchmarks"]},
        )
        self.assertIn(
            "analyze_cofactor_abstention_policy",
            {benchmark["name"] for benchmark in report["benchmarks"]},
        )
        self.assertIn(
            "analyze_seed_family_performance",
            {benchmark["name"] for benchmark in report["benchmarks"]},
        )
        self.assertIn("mean_ms", report["benchmarks"][0])


if __name__ == "__main__":
    unittest.main()
