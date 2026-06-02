"""Unit tests for the D11 Lever 2 learned mechanism-feature embedding.

Pure-stdlib synthetic tests for the linear algebra, the atlas-fit feature space,
the novelty signals, and the operating-point machinery, plus an optional
integration smoke against the persisted artifacts (gated behind CATALYTIC_RUN_SLOW
because the full 184-row atlas eigendecomposition takes ~2 minutes).
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from catalytic_earth.mechanism_feature_embedding import (
    MechanismFeatureSpace,
    _auc_in_gt_oos,
    _operating_point,
    _symmetric_jacobi,
    build_mechanism_feature_embedding_eval,
    compute_mechanism_feature_embedding,
)

ESM = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
COF = Path("artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json")
PREDICTED = Path("artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json")


# --------------------------------------------------------------------------- #
# Linear algebra
# --------------------------------------------------------------------------- #
def test_symmetric_jacobi_reconstructs_matrix():
    a = [[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
    vals, vecs = _symmetric_jacobi(a)
    # eigenvalues sorted descending
    assert vals == sorted(vals, reverse=True)
    # eigenvectors orthonormal
    for i in range(3):
        col_i = [vecs[r][i] for r in range(3)]
        assert abs(math.fsum(x * x for x in col_i) - 1.0) < 1e-6
        for j in range(i + 1, 3):
            col_j = [vecs[r][j] for r in range(3)]
            assert abs(math.fsum(x * y for x, y in zip(col_i, col_j))) < 1e-6
    # A = sum_k lambda_k v_k v_k^T
    for r in range(3):
        for c in range(3):
            recon = math.fsum(vals[k] * vecs[r][k] * vecs[c][k] for k in range(3))
            assert abs(recon - a[r][c]) < 1e-6


def test_auc_in_gt_oos_bounds():
    assert _auc_in_gt_oos([2.0], [1.0]) == 1.0
    assert _auc_in_gt_oos([1.0], [1.0]) == 0.5
    assert _auc_in_gt_oos([0.0], [1.0]) == 0.0
    assert _auc_in_gt_oos([], [1.0]) is None


def test_operating_point_fixes_retention_and_reads_recall():
    # in-scope score high (0.9..1.0), OOS score low (0.1..0.4): a threshold can
    # retain all in-scope while abstaining on most OOS.
    inscope = ["i0", "i1", "i2", "i3", "i4"]
    oos = ["o0", "o1", "o2", "o3"]
    # o3 sits INSIDE the in-scope band, so catching it would cost retention; with 5
    # in-scope rows, >=90% retention permits zero in-scope abstentions.
    scores = {"i0": 0.9, "i1": 0.92, "i2": 0.95, "i3": 0.97, "i4": 1.0,
              "o0": 0.1, "o1": 0.2, "o2": 0.3, "o3": 0.99}
    op = _operating_point(lambda e: scores[e], inscope, oos, [], oos)
    assert op is not None
    assert op["inscope_retain_recall"] >= 0.90
    # 3 of 4 OOS are below the in-scope band -> recall 0.75 at full retention.
    assert op["oos_abstain_recall"] == 0.75


def test_operating_point_none_without_both_pools():
    assert _operating_point(lambda e: 0.0, ["a"], [], [], []) is None


# --------------------------------------------------------------------------- #
# Atlas-fit feature space + novelty signals
# --------------------------------------------------------------------------- #
def _synthetic_space():
    """Atlas lives in dims 0-3 (3 separated classes); dims 4-5 carry zero atlas
    variance, so any energy there is OUT OF SPAN."""
    vectors = []
    labels = []
    base = {"f1": [3.0, 0.0, 0.0, 0.0], "f2": [0.0, 3.0, 0.0, 0.0], "f3": [0.0, 0.0, 3.0, 0.0]}
    for cls, b in base.items():
        for d in range(4):
            jitter = [b[k] + (0.1 * d if k == 3 else 0.0) for k in range(4)]
            vectors.append(jitter + [0.0, 0.0])  # dims 4,5 = 0 on the atlas
            labels.append(cls)
    return MechanismFeatureSpace(vectors, labels)


def test_feature_space_excludes_zero_variance_dims_and_is_full_rank_on_span():
    space = _synthetic_space()
    assert 1 <= space.pca_dim <= 4  # dims 4,5 carry no atlas variance
    assert len(space.whiten) == space.pca_dim
    assert len(space.classes) == 3
    assert space.condition_number >= 1.0


def test_residual_flags_out_of_span_rows():
    space = _synthetic_space()
    in_span = space.transform([2.9, 0.0, 0.0, 0.05, 0.0, 0.0])  # near class f1, on the atlas span
    out_span = space.transform([2.9, 0.0, 0.0, 0.05, 5.0, 5.0])  # same, but mass in dims 4,5
    assert out_span["residual_energy"] > in_span["residual_energy"]
    # neg_residual: higher = looks more like known chemistry
    assert space.neg_residual(in_span["residual_energy"]) > space.neg_residual(out_span["residual_energy"])


def test_nearest_prototype_prefers_in_class():
    space = _synthetic_space()
    near_f1 = space.transform([3.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    between = space.transform([1.5, 1.5, 0.0, 0.0, 0.0, 0.0])  # between f1 and f2
    assert space.neg_nearest_prototype(near_f1["whitened"]) > space.neg_nearest_prototype(between["whitened"])


# --------------------------------------------------------------------------- #
# End-to-end compute on a small synthetic surface
# --------------------------------------------------------------------------- #
def _synthetic_rows():
    rows: dict[str, dict] = {}
    base = {"f1": [3.0, 0.0, 0.0], "f2": [0.0, 3.0, 0.0], "f3": [0.0, 0.0, 3.0]}
    i = 0
    for cls, b in base.items():
        for _ in range(4):
            rows[f"a{i}"] = {"entry_id": f"a{i}", "embedding": b + [0.0, 0.0],
                             "split_assignment": "in_distribution", "true_fingerprint_id": cls}
            i += 1
    # held-out in-scope: on the atlas span, near a class
    rows["q0"] = {"entry_id": "q0", "embedding": [2.8, 0.0, 0.0, 0.0, 0.0],
                  "split_assignment": "heldout", "true_fingerprint_id": "f1"}
    rows["q1"] = {"entry_id": "q1", "embedding": [0.0, 2.8, 0.0, 0.0, 0.0],
                  "split_assignment": "heldout", "true_fingerprint_id": "f2"}
    rows["q2"] = {"entry_id": "q2", "embedding": [0.0, 0.0, 2.8, 0.0, 0.0],
                  "split_assignment": "heldout", "true_fingerprint_id": "f3"}
    # held-out OOS: energy in the out-of-span dims 3,4
    for j in range(4):
        rows[f"o{j}"] = {"entry_id": f"o{j}", "embedding": [1.0, 1.0, 1.0, 4.0 + j, 4.0],
                         "split_assignment": "heldout", "true_fingerprint_id": None}
    cof = {e: {"flavin": 0.1, "heme": 0.1, "plp": 0.1} for e in rows}  # all agnostic
    geo = {e: {"score": 0.85 if rows[e]["true_fingerprint_id"] else 0.3,
               "role_match_fraction": 0.9} for e in rows}
    return rows, cof, geo


def test_compute_end_to_end_synthetic():
    rows, cof, geo = _synthetic_rows()
    res = compute_mechanism_feature_embedding(rows, cof, geo)
    assert res["status"] == "computed"
    assert res["counts"]["deployment_pool"]["inscope"] == 3
    assert res["counts"]["deployment_pool"]["oos"] == 4
    # the residual signal should separate out-of-span OOS from in-span in-scope.
    resid = res["deployment_pool_signals"]["learned_out_of_span_residual"]
    assert resid["auc_all"] is not None and resid["auc_all"] >= 0.75
    # verdict structure is present and the baseline was recomputed live.
    v = res["verdict"]
    assert v["primary_signal"] == "learned_combined_primary"
    assert v["overall"] in {"beats_baseline", "mixed", "does_not_beat_baseline"}
    assert res["top1_score_baseline_deployment"]["auc_all"] is not None
    # a row-keyed embedding exists for every row.
    assert set(res["row_embedding"]) == set(rows)


def test_insufficient_atlas_handled():
    rows = {"a0": {"entry_id": "a0", "embedding": [1.0, 0.0], "split_assignment": "in_distribution",
                   "true_fingerprint_id": "f1"}}
    res = compute_mechanism_feature_embedding(rows, {}, {})
    assert res["status"] == "insufficient_atlas"


# --------------------------------------------------------------------------- #
# Optional integration smoke against the persisted artifacts (slow; gated)
# --------------------------------------------------------------------------- #
def test_integration_documented_result_if_present():
    if not (ESM.exists() and COF.exists() and PREDICTED.exists()):
        return
    if not os.environ.get("CATALYTIC_RUN_SLOW"):
        return  # the full atlas eigendecomposition is ~2 minutes; opt-in only
    audit, result = build_mechanism_feature_embedding_eval(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF, predicted_geometry_audit_path=PREDICTED
    )
    r = audit["result"]
    assert r["status"] == "computed"
    assert r["space"]["pca_dim"] == 128
    assert r["counts"]["deployment_pool"] == {
        "inscope": 47, "oos": 79, "confounded": 6, "agnostic": 73}
    # The geometry baseline reproduces the documented 0.757.
    assert abs(r["top1_score_baseline_deployment"]["auc_all"] - 0.757) < 0.01
    v = r["verdict"]
    # Predeclared primary (combined) does NOT beat the baseline -- the clean negative.
    assert v["overall"] == "does_not_beat_baseline"
    assert v["primary_beats_top1_score_by_auc"] is False
    # The out-of-span residual is the exploratory lead and beats baseline at the
    # operating point, but is NOT safe on the confounded subset.
    exp = v["exploratory_best_single_signal"]
    assert exp["best_single_signal"] == "learned_out_of_span_residual"
    assert exp["beats_baseline_at_operating_point"] is True
    assert exp["safe_on_confounded_vs_baseline"] is False
    assert exp["role"] == "complementary_lift_channel_not_replacement_gate"
