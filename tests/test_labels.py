from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import (
    MechanismLabel,
    analyze_geometry_score_margins,
    analyze_out_of_scope_failures,
    analyze_structure_mapping_issues,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    classify_out_of_scope_failure,
    compare_threshold_policies,
    evaluate_geometry_retrieval,
    label_summary,
    load_labels,
    select_threshold,
    sweep_abstention_thresholds,
)


class LabelTests(unittest.TestCase):
    def test_load_labels(self) -> None:
        labels = load_labels()
        self.assertEqual(len(labels), 36)
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
        self.assertEqual(evaluation["metadata"]["top3_retained_accuracy_in_scope"], 1.0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate"], 1.0)
        self.assertEqual(evaluation["metadata"]["out_of_scope_abstention_rate"], 1.0)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions"], 0)

        sweep = sweep_abstention_thresholds(retrieval, labels, thresholds=[0.0, 0.7, 1.0])
        self.assertEqual(sweep["metadata"]["threshold_count"], 3)
        self.assertIn("selected", sweep)
        self.assertIn("legacy_selected", sweep)
        self.assertIn("retained_top3_reference", sweep)
        self.assertEqual(sweep["metadata"]["selected_threshold"], 0.7)
        self.assertEqual(sweep["metadata"]["retained_top3_reference_threshold"], 0.7)
        self.assertEqual(sweep["metadata"]["selection_comparison"]["same_threshold"], True)
        self.assertTrue(
            sweep["metadata"]["selection_comparison"]["zero_false_preserves_retained_top3"]
        )

        auto_sweep = sweep_abstention_thresholds(retrieval, labels)
        self.assertGreater(auto_sweep["metadata"]["threshold_count"], 21)
        self.assertEqual(auto_sweep["metadata"]["selected_threshold"], 0.2001)
        self.assertEqual(
            auto_sweep["metadata"]["selection_comparison"][
                "selected_top3_retained_accuracy_in_scope_evaluable"
            ],
            1.0,
        )

        margins = analyze_geometry_score_margins(retrieval, labels)
        self.assertEqual(margins["metadata"]["min_in_scope_top1_score"], 0.8)
        self.assertEqual(margins["metadata"]["max_out_of_scope_top1_score"], 0.2)
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
            ]
        )
        self.assertEqual(margins["metadata"]["out_of_scope_entries_at_or_above_min_in_scope"], 0)
        self.assertEqual(margins["limiting_in_scope_rows"][0]["entry_id"], "m_csa:1")

        controls = build_hard_negative_controls(retrieval, labels)
        self.assertEqual(controls["metadata"]["hard_negative_count"], 0)
        controls = build_hard_negative_controls(retrieval, labels, score_floor=0.1)
        self.assertEqual(controls["metadata"]["hard_negative_count"], 1)
        self.assertEqual(controls["rows"][0]["negative_control_type"], "score_overlap_with_in_scope_positive")

        expansion = build_label_expansion_candidates(
            {
                "entries": [
                    {
                        "entry_id": "m_csa:1",
                        "status": "ok",
                        "resolved_residue_count": 3,
                    },
                    {
                        "entry_id": "m_csa:3",
                        "pdb_id": "1XYZ",
                        "status": "ok",
                        "resolved_residue_count": 3,
                        "pairwise_distances_angstrom": [{"distance": 5.0}],
                        "pocket_context": {"nearby_residue_count": 2},
                    },
                ]
            },
            {
                "results": [
                    {
                        "entry_id": "m_csa:3",
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.6,
                                "cofactor_evidence_level": "ligand_supported",
                            }
                        ],
                    }
                ]
            },
            labels,
        )
        self.assertEqual(expansion["metadata"]["candidate_count"], 1)
        self.assertEqual(expansion["metadata"]["ready_for_label_review_count"], 1)
        self.assertEqual(expansion["rows"][0]["entry_id"], "m_csa:3")
        self.assertEqual(expansion["rows"][0]["readiness_blockers"], [])

        mapping_issues = analyze_structure_mapping_issues(
            {
                "entries": [
                    {"entry_id": "m_csa:1", "status": "ok"},
                    {
                        "entry_id": "m_csa:2",
                        "pdb_id": "2XYZ",
                        "status": "partial",
                        "resolved_residue_count": 1,
                        "missing_positions": 2,
                        "missing_position_details": [
                            {
                                "expected_code": "MG",
                                "observed_codes_at_position": ["HOH"],
                                "resid": 401,
                            }
                        ],
                    },
                    {
                        "entry_id": "m_csa:4",
                        "pdb_id": "4XYZ",
                        "status": "no_resolved_residues",
                        "resolved_residue_count": 0,
                        "missing_positions": 3,
                    },
                ]
            },
            labels,
        )
        self.assertEqual(mapping_issues["metadata"]["issue_count"], 2)
        self.assertEqual(mapping_issues["metadata"]["labeled_issue_count"], 1)
        self.assertEqual(mapping_issues["metadata"]["status_counts"]["partial"], 1)
        self.assertEqual(mapping_issues["metadata"]["label_type_counts"]["out_of_scope"], 1)
        self.assertEqual(mapping_issues["metadata"]["label_type_counts"]["unlabeled"], 1)
        self.assertEqual(mapping_issues["metadata"]["missing_expected_code_counts"]["MG"], 1)
        self.assertEqual(
            mapping_issues["metadata"]["observed_code_at_missing_position_counts"]["HOH"],
            1,
        )
        self.assertEqual(mapping_issues["rows"][0]["entry_id"], "m_csa:2")

    def test_threshold_policy_prefers_zero_false_non_abstentions(self) -> None:
        rows = [
            {
                "abstain_threshold": 0.35,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 0.5,
                "out_of_scope_false_non_abstentions": 2,
                "in_scope_retention_rate": 1.0,
                "top3_retained_accuracy_in_scope": 1.0,
            },
            {
                "abstain_threshold": 0.55,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 0.75,
                "out_of_scope_false_non_abstentions": 1,
                "in_scope_retention_rate": 1.0,
                "top3_retained_accuracy_in_scope": 1.0,
            },
            {
                "abstain_threshold": 0.75,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 1.0,
                "out_of_scope_false_non_abstentions": 0,
                "in_scope_retention_rate": 0.0,
                "top3_retained_accuracy_in_scope": 0.0,
            },
            {
                "abstain_threshold": 0.8,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 1.0,
                "out_of_scope_false_non_abstentions": 0,
                "in_scope_retention_rate": 0.0,
                "top3_retained_accuracy_in_scope": 0.0,
            },
        ]
        selected = select_threshold(rows)
        self.assertIsNotNone(selected)
        self.assertEqual(selected["abstain_threshold"], 0.75)

        comparison = compare_threshold_policies(selected, rows[0], rows[1])
        self.assertFalse(comparison["same_threshold"])
        self.assertFalse(comparison["zero_false_preserves_retained_top3"])
        self.assertFalse(comparison["zero_false_preserves_in_scope_retention"])
        self.assertEqual(comparison["selected_out_of_scope_false_non_abstentions"], 0)
        self.assertEqual(comparison["legacy_out_of_scope_false_non_abstentions"], 2)
        self.assertEqual(comparison["retained_top3_reference_threshold"], 0.55)

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
