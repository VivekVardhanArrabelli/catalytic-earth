from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import MechanismLabel
from catalytic_earth.learned_retrieval import build_learned_retrieval_manifest


class LearnedRetrievalTests(unittest.TestCase):
    def test_manifest_keeps_review_rows_out_of_training_labels(self) -> None:
        geometry = {
            "metadata": {"artifact": "active_site_geometry_features"},
            "entries": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "labeled hydrolase",
                    "status": "ok",
                    "pdb_id": "1ABC",
                    "resolved_residue_count": 3,
                    "residues": [{"code": "Ser"}, {"code": "His"}, {"code": "Asp"}],
                    "pairwise_distances_angstrom": [{}, {}, {}],
                    "ligand_context": {
                        "cofactor_families": ["metal"],
                        "structure_cofactor_families": ["metal"],
                    },
                    "pocket_context": {"descriptors": {"polar_fraction": 0.2}},
                },
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "review-only row",
                    "status": "ok",
                    "resolved_residue_count": 2,
                    "residues": [{"code": "Cys"}, {"code": "His"}],
                },
            ],
        }
        retrieval = {
            "metadata": {"method": "geometry_aware_seed_fingerprint_retrieval"},
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.7}
                    ],
                }
            ],
        }
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="ser_his_acid_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="test",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="cobalamin_radical_rearrangement",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="test",
                review_status="needs_expert_review",
            ),
        ]

        manifest = build_learned_retrieval_manifest(geometry, retrieval, labels)

        self.assertEqual(manifest["metadata"]["eligible_entry_count"], 1)
        rows = {row["entry_id"]: row for row in manifest["rows"]}
        self.assertTrue(rows["m_csa:1"]["countable_training_label"])
        self.assertFalse(rows["m_csa:2"]["countable_training_label"])
        self.assertIn(
            "label_not_countable_review_status",
            rows["m_csa:2"]["eligibility_blockers"],
        )
        self.assertEqual(
            rows["m_csa:1"]["heuristic_baseline_control"]["top1_score"],
            0.7,
        )


if __name__ == "__main__":
    unittest.main()
