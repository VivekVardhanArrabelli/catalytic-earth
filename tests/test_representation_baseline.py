from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import MechanismLabel
from catalytic_earth.representation_baseline import (
    build_representation_baseline_shootout_plan,
)


class RepresentationBaselineTests(unittest.TestCase):
    def test_plan_separates_roles_and_runs_bounded_kmer_smoke(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="expert anchor",
                review_status="expert_reviewed",
                tier="silver",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="ser_his_acid_hydrolase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="weak label",
            ),
            MechanismLabel(
                entry_id="m_csa:3",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="negative calibration",
            ),
        ]
        learned_manifest = {
            "metadata": {"label_registry_count": 2},
            "rows": [{"entry_id": "m_csa:1"}, {"entry_id": "m_csa:2"}],
        }
        sequence_holdout = {
            "metadata": {
                "method": "sequence_fold_distance_holdout_evaluation",
                "label_registry_count": 2,
                "heldout_count": 1,
                "in_distribution_count": 2,
                "evaluated_count": 3,
                "sequence_identity_backend_available": True,
                "sequence_identity_target_achieved": True,
            },
            "metrics": {
                "heldout": {
                    "evaluated_count": 1,
                    "in_scope_count": 1,
                    "out_of_scope_count": 0,
                    "top1_accuracy_in_scope": 1.0,
                    "top3_accuracy_in_scope": 1.0,
                    "out_of_scope_false_non_abstentions": 0,
                    "out_of_scope_abstention_rate": 1.0,
                }
            },
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "partition": "in_distribution",
                    "label_group": "metal_dependent_hydrolase",
                    "real_sequence_accessions": ["A1"],
                    "target_fingerprint_id": "metal_dependent_hydrolase",
                },
                {
                    "entry_id": "m_csa:3",
                    "partition": "in_distribution",
                    "label_group": "out_of_scope",
                    "real_sequence_accessions": ["A3"],
                    "target_fingerprint_id": None,
                },
                {
                    "entry_id": "m_csa:2",
                    "partition": "heldout",
                    "label_group": "ser_his_acid_hydrolase",
                    "real_sequence_accessions": ["A2"],
                    "target_fingerprint_id": "ser_his_acid_hydrolase",
                },
            ],
        }
        fasta = ">sp|A1|one\nACDEFGHIK\n>sp|A2|two\nACDEFGHIK\n>sp|A3|three\nYYYYYYYYY\n"

        plan = build_representation_baseline_shootout_plan(
            labels,
            learned_manifest=learned_manifest,
            sequence_holdout_eval=sequence_holdout,
            sequence_fasta_text=fasta,
        )

        self.assertTrue(plan["metadata"]["review_only"])
        self.assertFalse(plan["metadata"]["label_import_performed"])
        roles = plan["benchmark_spec"]["role_counts"]
        self.assertEqual(roles["high_trust_evaluation_calibration_anchor"], 1)
        self.assertEqual(roles["weak_supervision_only"], 1)
        self.assertEqual(roles["negative_ood_calibration"], 1)
        self.assertEqual(
            plan["benchmark_spec"]["registry_scope"][
                "labels_missing_from_learned_manifest_entry_ids"
            ],
            ["m_csa:3"],
        )

        kmer = {
            row["baseline_id"]: row for row in plan["baseline_matrix"]
        }["deterministic_3mer_jaccard_nearest_neighbor_smoke"]
        self.assertEqual(
            kmer["status"],
            "computed_existing_sequence_holdout_but_stale_for_current_registry",
        )
        self.assertEqual(kmer["predictive_inputs"], ["amino_acid_sequence_only"])
        self.assertEqual(kmer["forbidden_inputs_used"], [])
        self.assertEqual(kmer["metrics"]["exact_label_accuracy_in_scope"], 0.0)
        self.assertIn(
            "mechanism_text",
            plan["prediction_leakage_contract"]["forbidden_for_prediction_fields"],
        )


if __name__ == "__main__":
    unittest.main()
