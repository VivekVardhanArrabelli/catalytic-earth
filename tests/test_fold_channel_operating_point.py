from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.fold_channel_operating_point import (
    THRESHOLD_GRID,
    build_fold_channel_operating_point,
    write_fold_channel_operating_point,
)


def _curve_for(rows: list[dict]) -> list[dict]:
    """Published recovery curve that matches the rows by construction."""
    n = len(rows)
    curve = []
    for tau in THRESHOLD_GRID:
        retained = [r for r in rows if r["fold_nn_alntmscore"] >= tau]
        rr = sum(1 for r in retained if r["recovered"])
        curve.append(
            {
                "fold_threshold": tau,
                "retained": len(retained),
                "retained_recovered": rr,
                "recovery_of_all_positives": round(rr / n, 4),
                "precision_on_retained": (
                    round(rr / len(retained), 4) if retained else None
                ),
                "abstained": n - len(retained),
            }
        )
    return curve


def _mcsa_rows() -> list[dict]:
    return [
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.90, "recovered": True, "true_fingerprint_id": "fpA"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.70, "recovered": True, "true_fingerprint_id": "fpA"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.60, "recovered": False, "true_fingerprint_id": "fpA"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.55, "recovered": True, "true_fingerprint_id": "fpB"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.40, "recovered": False, "true_fingerprint_id": "fpB"},
    ]


def _off_rows() -> list[dict]:
    # 'flavin' holds at high tau; 'metal' true hits are low-scoring -> collapses.
    return [
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.90, "recovered": True, "true_fingerprint_id": "flavin"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.80, "recovered": True, "true_fingerprint_id": "flavin"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.55, "recovered": True, "true_fingerprint_id": "metal"},
        {"fold_nn_scored": True, "fold_nn_alntmscore": 0.52, "recovered": True, "true_fingerprint_id": "metal"},
    ]


def _frontier(mcsa_rows: list[dict]) -> list[dict]:
    n = len(mcsa_rows)
    # External false-accept set so that tau=0.6 is the first <= 0.20 point.
    ext = {0.5: 0.70, 0.566: 0.50, 0.6: 0.20, 0.65: 0.10, 0.7: 0.05, 0.74: 0.02}
    out = []
    for tau in THRESHOLD_GRID:
        retained = sum(1 for r in mcsa_rows if r["fold_nn_alntmscore"] >= tau)
        out.append(
            {
                "fold_threshold": tau,
                "mcsa_oos_false_accept_rate": ext[tau],
                "external_false_accept_rate": ext[tau],
                "mcsa_inscope_retention_rate": round(retained / n, 4),
            }
        )
    return out


def _sources() -> dict:
    mcsa = _mcsa_rows()
    off = _off_rows()
    return {
        "mcsa_recovery_baseline": {
            "rows": mcsa,
            "recovery_abstention_curve": _curve_for(mcsa),
        },
        "offmcsa_recovery": {
            "rows": off,
            "recovery_abstention_curve": _curve_for(off),
        },
        "offmcsa_abstention": {
            "abstention_recovery_frontier": _frontier(mcsa),
        },
    }


class FoldChannelOperatingPointTests(unittest.TestCase):
    def test_verification_passes_on_consistent_sources(self) -> None:
        s = build_fold_channel_operating_point(sources=_sources())
        self.assertTrue(all(s["verification"].values()))
        self.assertEqual(
            s["status"],
            "fold_channel_operating_point_contract_development_surface_pending_heldout_validation",
        )

    def test_recommended_point_is_lowest_tau_under_rejection_floor(self) -> None:
        s = build_fold_channel_operating_point(sources=_sources())
        # external false-accept first drops to <= 0.20 at tau=0.6 in the fixture.
        self.assertTrue(s["recommended_operating_point"]["found"])
        self.assertEqual(s["recommended_operating_point"]["fold_threshold"], 0.6)
        self.assertEqual(s["serving_contract"]["tau_star"], 0.6)

    def test_combined_recovery_aggregates_both_surfaces(self) -> None:
        s = build_fold_channel_operating_point(sources=_sources())
        row0 = s["no_abstention_reference"]["recovery"]["combined"]
        # 3 recovered of 5 mcsa + 4 of 4 off = 7 of 9.
        self.assertEqual(row0["n"], 9)
        self.assertEqual(row0["retained_recovered"], 7)

    def test_family_collapse_is_flagged(self) -> None:
        s = build_fold_channel_operating_point(sources=_sources())
        fr = s["family_robustness_at_recommended_tau"]
        # At tau*=0.6 the two 'metal' hits (0.55, 0.52) drop out -> collapse.
        self.assertIn("metal", fr["families_that_collapse_at_recommended_tau"])
        self.assertNotIn("flavin", fr["families_that_collapse_at_recommended_tau"])
        self.assertFalse(fr["single_global_threshold_uniform_across_families"])

    def test_verification_raises_when_curve_diverges(self) -> None:
        s = _sources()
        # Corrupt the published M-CSA curve so recompute cannot reproduce it.
        s["mcsa_recovery_baseline"]["recovery_abstention_curve"][0][
            "retained_recovered"
        ] = 999
        with self.assertRaises(ValueError):
            build_fold_channel_operating_point(sources=s)

    def test_guardrails_assert_no_leakage(self) -> None:
        s = build_fold_channel_operating_point(sources=_sources())
        g = s["guardrails"]
        self.assertFalse(g["heldout_rows_scored"])
        self.assertFalse(g["threshold_selected_on_heldout"])
        self.assertFalse(g["supervised_model_trained"])
        self.assertFalse(g["registry_or_ontology_changed"])
        self.assertFalse(g["production_threshold_changed"])

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            srcs = {}
            for name, payload in _sources().items():
                p = root / f"{name}.json"
                p.write_text(json.dumps(payload), encoding="utf-8")
                srcs[name] = str(p)
            out = root / "contract.json"
            report = root / "contract.md"
            summary = write_fold_channel_operating_point(
                sources=srcs, out_path=out, report_path=report
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            text = report.read_text(encoding="utf-8")
            self.assertIn("Serving contract", text)
            self.assertIn("Family robustness", text)
            self.assertEqual(len(summary["source_artifacts"]), len(srcs))
            self.assertIn(
                "sha256", next(iter(summary["source_artifacts"].values()))
            )


if __name__ == "__main__":
    unittest.main()
