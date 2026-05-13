from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.source_limits import audit_source_scale_limits


ROOT = Path(__file__).resolve().parents[1]


class SourceScaleLimitTests(unittest.TestCase):
    def test_audit_flags_source_limit_before_target(self) -> None:
        graph = {
            "metadata": {"mcsa": {"record_count": 3}},
            "nodes": [
                {"id": "m_csa:1", "type": "m_csa_entry"},
                {"id": "m_csa:2", "type": "m_csa_entry"},
                {"id": "m_csa:5", "type": "m_csa_entry"},
            ],
        }
        prior_graph = {
            "metadata": {"mcsa": {"record_count": 2}},
            "nodes": [
                {"id": "m_csa:1", "type": "m_csa_entry"},
                {"id": "m_csa:2", "type": "m_csa_entry"},
            ],
        }
        labels = [
            {
                "entry_id": "m_csa:1",
                "label_type": "seed_fingerprint",
                "review_status": "automation_curated",
            },
            {
                "entry_id": "m_csa:2",
                "label_type": "out_of_scope",
                "review_status": "automation_curated",
            },
            {
                "entry_id": "m_csa:5",
                "label_type": "seed_fingerprint",
                "review_status": "needs_expert_review",
            },
        ]
        review_debt = {"metadata": {"review_debt_count": 1, "new_review_debt_count": 1}}
        candidates = {"rows": [{"entry_id": "m_csa:5"}]}

        audit = audit_source_scale_limits(
            graph,
            labels,
            target_source_entries=5,
            public_target_countable_labels=10,
            prior_graph=prior_graph,
            review_debt=review_debt,
            label_expansion_candidates=candidates,
        )

        metadata = audit["metadata"]
        self.assertEqual(metadata["observed_source_entries"], 3)
        self.assertEqual(metadata["source_entry_gap"], 2)
        self.assertTrue(metadata["source_limit_reached"])
        self.assertEqual(metadata["new_source_entry_ids"], ["m_csa:5"])
        self.assertEqual(metadata["countable_label_count"], 2)
        self.assertEqual(metadata["public_label_gap"], 8)
        self.assertEqual(metadata["review_debt_count"], 1)
        self.assertIn("m_csa_only_scaling_cannot_reach_public_label_target", audit["blockers"])

    def test_audit_source_scale_limits_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            graph = root / "graph.json"
            labels = root / "labels.json"
            out = root / "source_limit.json"
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"mcsa": {"record_count": 1}},
                        "nodes": [{"id": "m_csa:1", "type": "m_csa_entry"}],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "label_type": "seed_fingerprint",
                            "review_status": "automation_curated",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-source-scale-limits",
                    "--graph",
                    str(graph),
                    "--labels",
                    str(labels),
                    "--target-source-entries",
                    "2",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(payload["metadata"]["source_limit_reached"])
