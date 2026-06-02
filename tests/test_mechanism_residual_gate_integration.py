"""Unit tests for the D11 Lever 2 residual -> rule-gate integration.

Pure-stdlib synthetic tests for the residual-threshold grid, the confounded-safe
three-channel rule gate, and the two-/three-channel comparison invariants, plus an
optional gated integration smoke against the persisted artifacts.
"""

from __future__ import annotations

import os
from pathlib import Path

from catalytic_earth.mechanism_residual_gate_integration import (
    _residual_threshold_candidates,
    build_residual_gate_integration_eval,
    compute_residual_gate_integration,
)

ESM = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
COF = Path("artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json")
PREDICTED = Path("artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json")


def test_residual_threshold_candidates_bounded_with_disable_sentinel():
    cands = _residual_threshold_candidates([3.0, 1.0, 2.0, 2.0, 5.0])
    assert cands[:-1] == [1.0, 2.0, 3.0, 5.0]  # sorted unique
    assert cands[-1] > 5.0  # sentinel above max disables the residual term
    big = _residual_threshold_candidates([float(i) for i in range(500)])
    assert len(big) <= 61  # bounded grid + sentinel


def _synthetic_inputs():
    rows: dict[str, dict] = {}
    base = {"f1": [3.0, 0.0, 0.0], "f2": [0.0, 3.0, 0.0], "f3": [0.0, 0.0, 3.0], "f4": [2.1, 2.1, 0.0]}
    i = 0
    for cls, b in base.items():
        for j in range(5):
            rows[f"a{i}"] = {
                "entry_id": f"a{i}",
                "embedding": [b[k] + (0.04 * j if k == 2 else 0.0) for k in range(3)] + [0.0, 0.0],
                "split_assignment": "in_distribution",
                "true_fingerprint_id": cls,
            }
            i += 1
    classes = list(base)
    for q in range(16):
        b = base[classes[q % len(classes)]]
        rows[f"q{q}"] = {
            "entry_id": f"q{q}",
            "embedding": [b[k] * 0.95 for k in range(3)] + [0.0, 0.0],
            "split_assignment": "heldout",
            "true_fingerprint_id": classes[q % len(classes)],
        }
    for o in range(16):
        rows[f"o{o}"] = {
            "entry_id": f"o{o}",
            "embedding": [1.0, 1.0, 1.0, 4.0 + 0.1 * o, 4.0],
            "split_assignment": "heldout",
            "true_fingerprint_id": None,
        }
    # even OOS read as cofactor-confounded (strong cofactor signature)
    cof = {}
    for e in rows:
        hot = e.startswith("o") and (int(e[1:]) % 2 == 0)
        cof[e] = {"flavin": 0.9 if hot else 0.05, "heme": 0.05, "plp": 0.05}
    # geometry: in-scope confident; OOS partly overlapping so a lift channel has headroom
    geo = {}
    for e in rows:
        if rows[e]["true_fingerprint_id"]:
            geo[e] = {"score": 0.6, "role_match_fraction": 0.9}
        else:
            geo[e] = {"score": 0.45, "role_match_fraction": 0.5}
    return rows, cof, geo


def test_compute_integration_invariants_and_structure():
    rows, cof, geo = _synthetic_inputs()
    res = compute_residual_gate_integration(rows, cof, geo)
    assert res["status"] == "computed"
    # residual channel separates out-of-span OOS from on-span in-scope
    assert res["channels_auc"]["out_of_span_residual"]["all"] >= 0.7
    # three-channel search space contains the two-channel gate -> never worse
    for floor_key, pf in res["per_retention_floor"].items():
        two = pf["two_channel_geometry_cofactor"]
        three = pf["three_channel_with_residual_agnostic_lift"]
        if two and three:
            assert three["oos_abstain_recall"] >= two["oos_abstain_recall"] - 1e-9
            # confounded-safe by construction: the residual term never fires on
            # confounded rows (cof >= signature), so confounded abstention is gated by
            # geometry alone -- it cannot DROP below the two-channel value unless the
            # optimizer lowers tg (which the verdict's safety flag reports).
    # saturation evidence + cross-check fields are present and well-formed
    sat = res["residual_atlas_saturation"]
    assert set(sat) >= {"fraction_above_atlas_max", "atlas_percentile_calibration_saturates"}
    v = res["verdict"]
    assert "pass_at_operative_floor" in v
    assert isinstance(v["residual_cross_check_vs_embedding_eval"], bool)
    # verdict booleans resolve at the operative floor
    vf = res["verdict_by_floor"][res["operative_floor"]]
    for key in ("residual_adds_oos_lift", "confounded_safety_preserved", "pass"):
        assert vf[key] is None or isinstance(vf[key], bool)


def test_insufficient_rows_and_atlas_handled():
    # no held-out OOS -> insufficient_rows
    rows = {
        "a0": {"entry_id": "a0", "embedding": [1.0, 0.0], "split_assignment": "in_distribution",
               "true_fingerprint_id": "f1"},
        "q0": {"entry_id": "q0", "embedding": [1.0, 0.0], "split_assignment": "heldout",
               "true_fingerprint_id": "f1"},
    }
    cof = {e: {"flavin": 0.1} for e in rows}
    geo = {e: {"score": 0.5, "role_match_fraction": 0.5} for e in rows}
    assert compute_residual_gate_integration(rows, cof, geo)["status"] == "insufficient_rows"


def test_integration_gate_if_present():
    if not (ESM.exists() and COF.exists() and PREDICTED.exists()):
        return
    if not os.environ.get("CATALYTIC_RUN_SLOW"):
        return  # atlas eigendecomposition + 3D grid is slow; opt-in only
    audit, result = build_residual_gate_integration_eval(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF, predicted_geometry_audit_path=PREDICTED
    )
    assert result["status"] == "computed"
    assert result["counts"] == {
        "inscope": 47, "oos": 79, "confounded_oos": 6, "agnostic_oos": 73, "atlas": 184}
    # the residual channel reproduces the confirmed signal
    assert abs(result["channels_auc"]["out_of_span_residual"]["all"] - 0.72098) < 0.01
    assert result["verdict"]["residual_cross_check_vs_embedding_eval"] is True
    # operative floor is 85% (the two-channel gate has no >=90% point)
    assert result["operative_floor"] == "85pct_retention"
    vf = result["verdict_by_floor"]["85pct_retention"]
    # two-channel reproduces the committed baseline; residual adds a confounded-safe lift
    assert vf["two_channel_oos_abstain_recall"] == 0.3038
    assert vf["three_channel_oos_abstain_recall"] > vf["two_channel_oos_abstain_recall"]
    assert vf["confounded_safety_preserved"] is True
    assert vf["pass"] is True
    # the residual threshold is research-grade: held-out rows saturate the atlas range
    assert result["residual_atlas_saturation"]["atlas_percentile_calibration_saturates"] is True
