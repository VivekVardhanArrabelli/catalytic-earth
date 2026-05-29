from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.bin_targeted_expansion import build_bin_targeted_expansion_plan


class BinTargetedExpansionTests(unittest.TestCase):
    def test_plan_reports_gaps_without_marking_import_ready(self) -> None:
        wave1 = {
            "per_bin_results": {
                "no_reliable_structure": {
                    "row_ids": ["m_csa:1"],
                    "track_results": {
                        "geometry_baseline_reexport": {
                            "row_count": 1,
                            "primary_support_count": 1,
                            "primary_abstention_count": 0,
                            "primary_accuracy_available": 1.0,
                            "oos_or_secondary_support_count": 0,
                            "oos_or_secondary_false_positive_rate_available": None,
                        }
                    },
                },
                "low_structure_neighborhood_near_orphan": {
                    "row_ids": ["m_csa:2"],
                    "track_results": {
                        "geometry_baseline_reexport": {
                            "row_count": 1,
                            "primary_support_count": 1,
                            "primary_abstention_count": 0,
                            "primary_accuracy_available": 1.0,
                            "oos_or_secondary_support_count": 0,
                            "oos_or_secondary_false_positive_rate_available": None,
                        }
                    },
                },
            }
        }
        slice_contract = {
            "rows": [
                {
                    "entry_id": "m_csa:2",
                    "structural_neighborhood_bin": (
                        "low_structure_neighborhood_near_orphan"
                    ),
                    "split_assignment": "heldout",
                    "current_fingerprint_id": "metal",
                    "use_reason": "test",
                }
            ]
        }
        readiness = {
            "rows": [
                {
                    "allowed_use": "external_materialization_needed_before_feature_extraction",
                    "candidate_id": "mh_001",
                    "source_group": "external_router_priority",
                }
            ]
        }

        plan = build_bin_targeted_expansion_plan(
            wave1_audit=wave1,
            slice_contract=slice_contract,
            readiness_matrix=readiness,
            target_primary_n=3,
            target_oos_n=2,
        )

        self.assertFalse(plan["guardrails"]["label_import_performed"])
        self.assertEqual(plan["recommendation"]["near_orphan_oos_gap"], 2)
        self.assertEqual(
            plan["recommendation"]["first_batch"],
            "near_orphan_oos_control_materialization",
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in plan["candidate_rows"])
        )


if __name__ == "__main__":
    unittest.main()
