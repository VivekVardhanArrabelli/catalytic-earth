from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import (
    MechanismLabel,
    evaluate_geometry_retrieval,
    label_summary,
    load_labels,
    sweep_abstention_thresholds,
)


class LabelTests(unittest.TestCase):
    def test_load_labels(self) -> None:
        labels = load_labels()
        self.assertEqual(len(labels), 20)
        summary = label_summary(labels)
        self.assertGreater(summary["by_type"]["seed_fingerprint"], 0)
        self.assertGreater(summary["by_type"]["out_of_scope"], 0)

    def test_invalid_label(self) -> None:
        with self.assertRaises(ValueError):
            MechanismLabel.from_dict(
                {
                    "entry_id": "m_csa:1",
                    "fingerprint_id": None,
                    "label_type": "seed_fingerprint",
                    "confidence": "high",
                    "rationale": "This rationale is long enough to pass length.",
                }
            )

    def test_evaluate_geometry_retrieval(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.2}
                    ],
                },
            ]
        }
        evaluation = evaluate_geometry_retrieval(retrieval, labels, abstain_threshold=0.7)
        self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope"], 1.0)
        self.assertEqual(evaluation["metadata"]["out_of_scope_abstention_rate"], 1.0)

        sweep = sweep_abstention_thresholds(retrieval, labels, thresholds=[0.0, 0.7, 1.0])
        self.assertEqual(sweep["metadata"]["threshold_count"], 3)
        self.assertIn("selected", sweep)


if __name__ == "__main__":
    unittest.main()
