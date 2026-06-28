from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.fold_channel_deployment_readiness import (
    build_fold_channel_deployment_readiness,
    write_fold_channel_deployment_readiness,
)


def _sources(off_rate: float = 0.85, abstention_generalizes: bool = True) -> dict:
    return {
        "mcsa_recovery_baseline": {
            "recovery": {
                "fold_nn_recovered": 28,
                "fold_nn_scored": 35,
                "recovery_rate_no_abstention": 0.80,
            }
        },
        "offmcsa_recovery": {
            "surface_label": "offmcsa_bronze_high_confidence",
            "recovery": {
                "fold_nn_recovered": int(round(off_rate * 100)),
                "fold_nn_scored": 100,
                "recovery_rate_no_abstention": off_rate,
            },
            "rows": [
                {"fold_nn_scored": True, "recovered": True, "true_fingerprint_id": "fpA"},
                {"fold_nn_scored": True, "recovered": False, "true_fingerprint_id": "fpA"},
                {"fold_nn_scored": True, "recovered": True, "true_fingerprint_id": "fpB"},
            ],
        },
        "offmcsa_abstention": {
            "generalization_test": {
                "external_median": 0.574,
                "mcsa_oos_median": 0.566,
                "mcsa_inscope_median": 0.743,
                "abstention_signal_generalizes_off_mcsa": abstention_generalizes,
            }
        },
        "mcsa_fold_separation": {
            "fold_nn_distribution": {
                "inscope": {"alntmscore_median": 0.743},
                "oos": {"alntmscore_median": 0.566},
            }
        },
        "june9_fold_fusion": {
            "june9_baseline_fold_gate_off": {
                "dial_0p44_threshold": {
                    "inscope_correct": 30,
                    "inscope_total": 35,
                    "oos_false_positives": 8,
                    "oos_total": 26,
                }
            }
        },
        "cofactor_precision_contract": {
            "status": "blocked_current57_cofactor_precision_contract_not_deployable",
            "calibration_summary": {
                "legacy_v1_compatible_fused_current57_at_frozen_threshold": {
                    "inscope_correct": 26
                }
            },
        },
        "heldout_preregistration": {"status": "preregistered_not_yet_run"},
    }


class FoldChannelDeploymentReadinessTests(unittest.TestCase):
    def test_both_halves_generalize_when_recovery_and_rejection_hold(self) -> None:
        summary = build_fold_channel_deployment_readiness(sources=_sources())
        self.assertEqual(
            summary["status"],
            "fold_channel_generalizes_off_mcsa_both_halves_deployment_claim_still_gated",
        )
        off = summary["off_mcsa_generalization"]
        self.assertTrue(off["both_halves_generalize_off_mcsa"])
        self.assertTrue(off["recovery_half"]["generalizes"])
        self.assertTrue(off["rejection_half"]["generalizes"])
        # per-family computed from rows
        self.assertEqual(off["recovery_half"]["per_family"]["fpA"], "1/2 (0.5)")

    def test_incomplete_when_rejection_fails(self) -> None:
        summary = build_fold_channel_deployment_readiness(
            sources=_sources(abstention_generalizes=False)
        )
        self.assertEqual(
            summary["status"], "fold_channel_off_mcsa_generalization_incomplete"
        )
        self.assertFalse(
            summary["off_mcsa_generalization"]["both_halves_generalize_off_mcsa"]
        )

    def test_incomplete_when_recovery_below_threshold(self) -> None:
        summary = build_fold_channel_deployment_readiness(
            sources=_sources(off_rate=0.50)
        )
        self.assertFalse(
            summary["off_mcsa_generalization"]["recovery_half"]["generalizes"]
        )
        self.assertEqual(
            summary["status"], "fold_channel_off_mcsa_generalization_incomplete"
        )

    def test_deployment_claim_made_when_heldout_passes(self) -> None:
        srcs = _sources()
        srcs["heldout_oneshot_eval"] = {
            "artifact_id": "heldout_eval",
            "verdict": "PASS",
            "heldout_result": {
                "inscope_recovery": "35/47",
                "inscope_recovery_rate": 0.7447,
                "oos_false_positives": "15/79",
                "oos_false_positive_rate": 0.1899,
            },
        }
        summary = build_fold_channel_deployment_readiness(sources=srcs)
        self.assertEqual(
            summary["status"],
            "deployment_claim_made_mcsa_heldout_passed_offmcsa_generalizes",
        )
        self.assertTrue(summary["deployment_claim"]["made"])
        # held-out PASS removed from "not yet validated"
        joined = " ".join(summary["not_yet_validated"]).lower()
        self.assertNotIn("unspent", joined)

    def test_carries_not_yet_validated_caveats(self) -> None:
        summary = build_fold_channel_deployment_readiness(sources=_sources())
        joined = " ".join(summary["not_yet_validated"]).lower()
        self.assertIn("gold", joined)
        self.assertIn("held-out", joined)
        self.assertIn("calibration", joined)

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            srcs = {}
            for name, payload in _sources().items():
                p = root / f"{name}.json"
                p.write_text(json.dumps(payload), encoding="utf-8")
                srcs[name] = str(p)
            out = root / "summary.json"
            report = root / "summary.md"
            summary = write_fold_channel_deployment_readiness(
                sources=srcs, out_path=out, report_path=report
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertIn("Bottom Line", report.read_text(encoding="utf-8"))
            self.assertEqual(len(summary["source_artifacts"]), len(srcs))
            self.assertIn("sha256", next(iter(summary["source_artifacts"].values())))


if __name__ == "__main__":
    unittest.main()
