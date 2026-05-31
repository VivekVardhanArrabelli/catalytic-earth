"""Unit tests for the D11 two-channel abstention gate.

Pure-stdlib synthetic tests plus optional integration smoke against the persisted
ESM2-150M embeddings, cofactor sidecar, and experimental geometry retrieval.
"""

from __future__ import annotations

from pathlib import Path

from catalytic_earth.mechanism_abstention_gate_eval import (
    _atlas_percentile,
    _auc_in_gt_oos,
    _geometry_regime,
    build_mechanism_abstention_gate_eval,
    build_mechanism_deployment_abstention_gate_eval,
    compute_deployment_gate,
    compute_two_channel_gate,
    load_geometry_role_scores,
)

ESM = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
COF = Path("artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json")
GEO = Path("artifacts/v3_geometry_retrieval_1025.json")
PREDICTED = Path("artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json")


def test_auc_bounds():
    assert _auc_in_gt_oos([2.0], [1.0]) == 1.0
    assert _auc_in_gt_oos([1.0], [1.0]) == 0.5
    assert _auc_in_gt_oos([], [1.0]) is None


def test_atlas_percentile_monotone():
    pct = _atlas_percentile(lambda e: float(e), ["1", "2", "3", "4"])
    assert pct("0") == 0.0
    assert pct("4") == 1.0
    assert pct("2") < pct("3")


def test_geometry_regime_detection():
    assert _geometry_regime(Path("x/v3_geometry_retrieval_1025.json")) == "experimental_geometry_teacher"
    assert _geometry_regime(Path("x/v3_predicted_geometry_retrieval.json")) == "predicted_geometry_deployment"


def _synthetic():
    def row(eid, split, fp, emb):
        return {"entry_id": eid, "embedding": emb, "split_assignment": split, "true_fingerprint_id": fp}
    rows = {}
    for i in range(4):
        rows[f"a{i}"] = row(f"a{i}", "in_distribution", "f1", [1.0 + 0.01 * i, 0.0])
        rows[f"b{i}"] = row(f"b{i}", "in_distribution", "f2", [0.0, 1.0 + 0.01 * i])
    rows["q1"] = row("q1", "heldout", "f1", [0.98, 0.02])
    rows["q2"] = row("q2", "heldout", "f2", [0.02, 0.98])
    rows["o1"] = row("o1", "heldout", None, [0.5, 0.5])
    rows["o2"] = row("o2", "heldout", None, [0.4, 0.6])
    cof = {e: {"flavin": 0.1, "heme": 0.1, "plp": 0.1} for e in rows}
    # in-scope queries have high geometry role-agreement; OOS low.
    geo = {e: {"score": 0.8, "role_match_fraction": 0.9} for e in rows}
    geo["o1"] = {"score": 0.3, "role_match_fraction": 0.1}
    geo["o2"] = {"score": 0.3, "role_match_fraction": 0.1}
    return rows, cof, geo


def test_compute_two_channel_gate_runs_and_stratifies():
    rows, cof, geo = _synthetic()
    res = compute_two_channel_gate(rows, cof, geo)
    assert res["status"] == "computed"
    assert res["counts"] == {
        "atlas": 8, "inscope": 2, "oos": 2, "confounded_oos": 0, "agnostic_oos": 2}
    assert set(res["channels"]) == {
        "cofactor_augmented", "geometry_score_x_role",
        "combined_mean", "combined_min_concordance"}


def test_insufficient_rows_handled():
    rows = {"a0": {"entry_id": "a0", "embedding": [1.0], "split_assignment": "in_distribution",
                   "true_fingerprint_id": "f1"}}
    res = compute_two_channel_gate(rows, {"a0": {"flavin": 0.1}}, {"a0": {"score": 0.5, "role_match_fraction": 0.5}})
    assert res["status"] == "insufficient_rows"


def test_integration_gate_clears_bar_if_present():
    if not (ESM.exists() and COF.exists() and GEO.exists()):
        return
    audit = build_mechanism_abstention_gate_eval(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF, geometry_retrieval_path=GEO
    )
    res = audit["result"]
    assert res["counts"]["confounded_oos"] == 8
    # The two-channel gate clears the 0.75 de novo precondition bar on teacher geometry.
    assert res["clears_abstention_bar"] is True
    # The combination rescues the confounded set well above the cofactor channel alone.
    assert (
        res["channels"]["combined_mean"]["confounded"]
        > res["channels"]["cofactor_augmented"]["confounded"]
    )
    assert audit["geometry_regime"] == "experimental_geometry_teacher"


def test_integration_geometry_role_scores_present_if_artifact():
    if not GEO.exists():
        return
    scores = load_geometry_role_scores(GEO)
    assert len(scores) > 100
    any_row = next(iter(scores.values()))
    assert "score" in any_row and "role_match_fraction" in any_row


def test_compute_deployment_gate_no_atlas_synthetic():
    # Deployment gate needs no atlas; in-scope high in both channels, OOS low.
    def row(eid, split, fp):
        return {"entry_id": eid, "embedding": [0.0], "split_assignment": split,
                "true_fingerprint_id": fp}
    plm = {
        "q1": row("q1", "heldout", "f1"), "q2": row("q2", "heldout", "f2"),
        "o1": row("o1", "heldout", None), "o2": row("o2", "heldout", None),
    }
    geom = {"q1": {"score": 0.9, "role_match_fraction": 0.8},
            "q2": {"score": 0.85, "role_match_fraction": 0.7},
            "o1": {"score": 0.2, "role_match_fraction": 0.1},
            "o2": {"score": 0.25, "role_match_fraction": 0.1}}
    cof = {"q1": {"flavin": 0.8}, "q2": {"heme": 0.7},
           "o1": {"flavin": 0.1}, "o2": {"plp": 0.1}}
    res = compute_deployment_gate(plm, cof, geom)
    assert res["status"] == "computed"
    assert res["counts"] == {"inscope": 2, "oos": 2, "confounded_oos": 0, "agnostic_oos": 2}
    # Perfect separation -> AUC 1.0 on the combined mean.
    assert res["channels"]["combined_mean"]["all"] == 1.0
    assert res["clears_abstention_bar"] is True


def test_integration_deployment_gate_clears_bar_if_present():
    if not (ESM.exists() and COF.exists() and PREDICTED.exists()):
        return
    audit = build_mechanism_deployment_abstention_gate_eval(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF,
        predicted_geometry_audit_path=PREDICTED,
    )
    res = audit["result"]
    assert res["status"] == "computed"
    # Deployment-valid (predicted/apo geometry), held-out only, no atlas.
    assert res["counts"]["inscope"] == 47 and res["counts"]["oos"] == 79
    # The de novo precondition is met on the deployment regime.
    assert res["clears_abstention_bar"] is True
    # Geometry confidence is the safest single channel (no stratum below chance);
    # the cofactor channel is fooled on the confounded OOS subset.
    assert res["safest_channel_no_stratum_below_chance"] == "geometry_top1_score"
    assert res["channels"]["cofactor_max_score"]["confounded"] < 0.5
    assert res["channels"]["geometry_top1_score"]["confounded"] >= 0.75
    # AUC does not imply a usable operating point: at >=90% in-scope retention the
    # blind mean-combined gate abstains on NONE of the confounded rows, while the
    # geometry-led gate keeps them safe (>0).
    op = res["operating_points_at_90pct_retention"]
    assert op["combined_mean"]["confounded_abstain_recall"] == 0.0
    assert op["geometry_led"]["confounded_abstain_recall"] > 0.0
    # Operating curve is monotone non-decreasing in OOS abstain-recall as threshold rises.
    curve = res["geometry_led_operating_curve"]
    recalls = [r["oos_abstain_recall"] for r in curve]
    assert recalls == sorted(recalls)
    # Per-channel rule gate: the cofactor lift helps at the relaxed 85% retention
    # floor (the feature overlap forbids a useful 90%-retention operating point).
    pc = res["per_channel_rule_gate"]
    assert pc["best_at_90pct_retention"] is None
    assert pc["best_at_85pct_retention"] is not None
    assert pc["cofactor_lift_oos_recall_at_85pct"] > 0.0
    assert (
        pc["best_at_85pct_retention"]["oos_abstain_recall"]
        > pc["geometry_only_at_85pct_retention"]["oos_abstain_recall"]
    )
