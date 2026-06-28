from __future__ import annotations

import unittest

from catalytic_earth.cofactor_precision_contract import (
    _legacy_v1_compatible,
    build_current57_cofactor_precision_contract,
)


def _inscope(entry_id, *, true, called, score):
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": true,
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _oos(entry_id, *, called, score):
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": None,
        "fused": {"top1_fingerprint_id": called, "top1_score": score},
    }


def _current(rows, oos):
    return {
        "artifact_id": "current57",
        "inputs": {"frozen_router_threshold": 0.4115},
        "row_details_by_split": {
            "calibration": {"inscope_rows": rows, "oos_rows": oos},
            "train": {"inscope_rows": rows, "oos_rows": oos},
        },
    }


def _trusted():
    return {
        "artifact_id": "trusted_june9",
        "operating_points_by_split": {
            "calibration": {
                "fused_frozen_threshold": {
                    "inscope_correct": 3,
                    "inscope_total": 3,
                    "oos_false_positives": 2,
                    "oos_total": 3,
                }
            }
        },
        "dial_comparison": {
            "threshold_dial_matching_suppression_precision": {
                "threshold": 0.44,
                "inscope_correct": 3,
                "inscope_total": 3,
                "oos_false_positives": 1,
                "oos_total": 3,
            }
        },
    }


class CofactorPrecisionContractTests(unittest.TestCase):
    def test_legacy_projection_is_metal_umbrella_only(self) -> None:
        self.assertTrue(
            _legacy_v1_compatible(
                true_fingerprint_id="metal_dependent_hydrolase",
                called_fingerprint_id="metallo_amidohydrolase_deaminase",
            )
        )
        self.assertFalse(
            _legacy_v1_compatible(
                true_fingerprint_id="ser_his_acid_hydrolase",
                called_fingerprint_id="alpha_beta_hydrolase_esterase_lipase",
            )
        )

    def test_contract_fail_closes_when_trusted_bar_unreachable(self) -> None:
        rows = [
            _inscope(
                "in1",
                true="metal_dependent_hydrolase",
                called="metallo_amidohydrolase_deaminase",
                score=0.9,
            ),
            _inscope(
                "in2",
                true="metal_dependent_hydrolase",
                called="metallophosphomonoesterase",
                score=0.8,
            ),
            _inscope(
                "in3",
                true="plp_dependent_enzyme",
                called="metallophosphomonoesterase",
                score=0.7,
            ),
        ]
        oos = [
            _oos("oo1", called="metallo_amidohydrolase_deaminase", score=0.85),
            _oos("oo2", called="metallophosphomonoesterase", score=0.75),
        ]
        contract = build_current57_cofactor_precision_contract(
            current_operating_point=_current(rows, oos),
            trusted_precision=_trusted(),
            ontology={"families": []},
        )

        self.assertEqual(
            contract["status"],
            "blocked_current57_cofactor_precision_contract_not_deployable",
        )
        cal = contract["calibration_summary"]
        self.assertEqual(
            cal["legacy_v1_compatible_fused_current57_at_frozen_threshold"][
                "inscope_correct"
            ],
            2,
        )
        self.assertEqual(cal["taxonomy_version_recovered_count"], 2)
        self.assertEqual(
            contract["selection_rule"]["decision"],
            "fail_closed_keep_atlas_engine_blocked_on_current57_cofactor_surface",
        )
        self.assertIsNone(contract["selection_rule"]["selected_threshold"])

    def test_contract_records_eligible_threshold_for_review(self) -> None:
        rows = [
            _inscope(
                "in1",
                true="metal_dependent_hydrolase",
                called="metallo_amidohydrolase_deaminase",
                score=0.9,
            ),
            _inscope(
                "in2",
                true="plp_dependent_enzyme",
                called="plp_dependent_enzyme",
                score=0.8,
            ),
            _inscope(
                "in3",
                true="ser_his_acid_hydrolase",
                called="ser_his_acid_hydrolase",
                score=0.7,
            ),
        ]
        oos = [_oos("oo1", called="metallo_amidohydrolase_deaminase", score=0.2)]
        contract = build_current57_cofactor_precision_contract(
            current_operating_point=_current(rows, oos),
            trusted_precision=_trusted(),
            ontology={"families": []},
        )

        self.assertEqual(
            contract["status"], "eligible_current57_threshold_contract_found"
        )
        self.assertEqual(contract["selection_rule"]["selected_threshold"], 0.4115)


if __name__ == "__main__":
    unittest.main()
