from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import (
    MechanismLabel,
    analyze_out_of_scope_failures,
    classify_out_of_scope_failure,
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

    def test_analyze_out_of_scope_failures(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for in-scope",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for out-of-scope",
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
                        {
                            "fingerprint_id": "flavin_monooxygenase",
                            "score": 0.84,
                            "residue_match_fraction": 0.1,
                            "role_match_fraction": 0.2,
                            "cofactor_context_score": 0.85,
                            "substrate_pocket_score": 0.2,
                            "compactness_score": 0.5,
                        }
                    ],
                },
            ]
        }
        analysis = analyze_out_of_scope_failures(retrieval, labels, abstain_threshold=0.75)
        self.assertEqual(analysis["metadata"]["false_non_abstentions"], 1)
        self.assertEqual(analysis["rows"][0]["evidence_pattern"], "cofactor_dominant")
        self.assertEqual(analysis["metadata"]["max_false_non_abstention_score"], 0.84)
        self.assertEqual(
            analysis["metadata"]["recommended_threshold_for_zero_current_false_non_abstentions"],
            0.85,
        )

    def test_classify_out_of_scope_failure_near_threshold(self) -> None:
        category = classify_out_of_scope_failure(
            {"score": 0.76, "residue_match_fraction": 0.9, "role_match_fraction": 0.9},
            abstain_threshold=0.75,
        )
        self.assertEqual(category, "near_threshold")


if __name__ == "__main__":
    unittest.main()
