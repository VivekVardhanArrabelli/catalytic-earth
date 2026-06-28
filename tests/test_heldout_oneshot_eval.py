from __future__ import annotations

import unittest

import catalytic_earth.heldout_oneshot_eval as hoe


def _split() -> dict:
    return {"split_records": [{"entry_id": "m_csa:1"}]}


def _labels() -> dict:
    return {
        "rows": [
            {"entry_id": "m_csa:1", "sequence_id": "P1", "fingerprint_id": "fpA"},
            {"entry_id": "m_csa:3", "sequence_id": "P3", "fingerprint_id": "fpA"},
            {"entry_id": "m_csa:4", "sequence_id": "P4", "fingerprint_id": None},
        ]
    }


def _frozen_sha() -> str:
    frozen = hoe.build_frozen_heldout_set(
        split_manifest=_split(),
        label_manifest=_labels(),
        heldout_structure_accessions={"P3", "P4"},
    )
    return frozen["sha256"]


def _prereg(sha: str) -> dict:
    return {
        "artifact_id": "prereg",
        "frozen_heldout_set": {"sha256": sha},
        "success_bar": {
            "primary_pass_criteria": "recovery >= 0.70 AND OOS FP rate <= 0.40",
            "calibration_reference": {
                "inscope_recovery": "30/35 (0.857)",
                "oos_false_positive_rate": "8/26 (0.308)",
            },
        },
    }


class _StubRouter:
    def __init__(self, point: dict, coverage: dict | None = None):
        self.point = point
        self.coverage = coverage or {}

    def __call__(self, **kwargs):
        # confirm the executor selects the heldout split
        assert kwargs["split_assignment"] == "heldout"
        return {
            "operating_points_by_split": {
                "calibration": {"fused_frozen_threshold": self.point}
            },
            "coverage": self.coverage,
        }


def _run(point, sha=None):
    sha = sha or _frozen_sha()
    return hoe.run_heldout_oneshot_eval(
        preregistration=_prereg(sha),
        split_manifest=_split(),
        label_manifest=_labels(),
        graph={},
        experimental_geometry_features={},
        channel={},
        heldout_coordinate_dirs=[],
    )


class HeldoutOneshotEvalTests(unittest.TestCase):
    def setUp(self):
        self._orig = hoe.build_cofactor_fusion_operating_point
        # heldout structure accessions come from dirs; patch to a fixed set
        self._orig_acc = hoe._heldout_structure_accessions
        hoe._heldout_structure_accessions = lambda dirs: {"P3", "P4"}

    def tearDown(self):
        hoe.build_cofactor_fusion_operating_point = self._orig
        hoe._heldout_structure_accessions = self._orig_acc

    def test_sha_mismatch_refuses_to_run(self) -> None:
        hoe.build_cofactor_fusion_operating_point = _StubRouter(
            {"inscope_correct": 1, "inscope_total": 1, "oos_false_positives": 0, "oos_total": 1}
        )
        with self.assertRaises(AssertionError):
            _run(point=None, sha="deadbeef")

    def test_pass_when_rates_meet_bar(self) -> None:
        hoe.build_cofactor_fusion_operating_point = _StubRouter(
            {"inscope_correct": 30, "inscope_total": 35, "oos_false_positives": 8, "oos_total": 26}
        )
        result = _run(point=None)
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["heldout_result"]["inscope_recovery_rate"], round(30 / 35, 4))
        self.assertTrue(result["preregistration"]["sha256_verified"])

    def test_fail_when_recovery_below_bar(self) -> None:
        hoe.build_cofactor_fusion_operating_point = _StubRouter(
            {"inscope_correct": 20, "inscope_total": 35, "oos_false_positives": 5, "oos_total": 26}
        )
        result = _run(point=None)
        self.assertEqual(result["verdict"], "FAIL")

    def test_fail_when_oos_fp_above_bar(self) -> None:
        hoe.build_cofactor_fusion_operating_point = _StubRouter(
            {"inscope_correct": 30, "inscope_total": 35, "oos_false_positives": 14, "oos_total": 26}
        )
        result = _run(point=None)
        self.assertEqual(result["verdict"], "FAIL")  # 14/26 = 0.538 > 0.40


if __name__ == "__main__":
    unittest.main()
