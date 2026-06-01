"""Unit tests for the D11 Lever 2 out-of-span residual robustness + confirmatory test.

Pure-stdlib synthetic tests for the shared atlas decomposition, the cutoff-keep rule,
the residual-energy read, the permutation null, the score-independent fold split, and the
end-to-end compute, plus an optional gated integration smoke against the persisted
artifacts (the 184-row atlas eigendecomposition is slow, so it is opt-in).
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from catalytic_earth.mechanism_feature_embedding import _auc_in_gt_oos
from catalytic_earth.mechanism_feature_residual_robustness import (
    _atlas_pca_full,
    _auc_from_midranks,
    _confirmatory_split,
    _cutoff_sweep,
    _fold_of,
    _keep_for_cutoff,
    _midranks,
    _permutation_pvalue,
    _row_projection_energies,
    build_residual_robustness_audit,
    compute_residual_robustness,
    N_FOLDS,
)

ESM = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
COF = Path("artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json")
PREDICTED = Path("artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json")


# --------------------------------------------------------------------------- #
# Rank-based AUC matches the brute-force AUC (incl. ties) -- the perm engine relies on it
# --------------------------------------------------------------------------- #
def test_midrank_auc_matches_brute_force():
    import random

    rng = random.Random(11)
    for _ in range(150):
        a = [rng.gauss(1.0, 1.0) for _ in range(rng.randint(2, 10))]
        b = [rng.gauss(0.0, 1.0) for _ in range(rng.randint(2, 10))]
        mr = _midranks(a + b)
        fast = _auc_from_midranks(mr, list(range(len(a))), len(a), len(b))
        assert abs(round(fast, 6) - _auc_in_gt_oos(a, b)) < 1e-6
    # explicit tie case
    mr = _midranks([1.0, 1.0, 2.0, 2.0])
    fast = _auc_from_midranks(mr, [0, 2], 2, 2)
    assert abs(fast - _auc_in_gt_oos([1.0, 2.0], [1.0, 2.0])) < 1e-9


def test_permutation_pvalue_separated_and_overlapping():
    sep = _permutation_pvalue([5.0, 6.0, 7.0, 8.0], [0.0, 1.0, 2.0, 3.0], n_perm=500, seed=1)
    assert sep is not None and sep["observed_auc"] == 1.0 and sep["p_value"] < 0.05
    mix = _permutation_pvalue([1.0, 2.0, 3.0, 4.0], [1.5, 2.5, 3.5, 4.5], n_perm=500, seed=1)
    assert mix["p_value"] > 0.1  # no real separation -> not significant
    assert _permutation_pvalue([1.0], [], n_perm=10, seed=1) is None


# --------------------------------------------------------------------------- #
# Score-independent fold split
# --------------------------------------------------------------------------- #
def test_fold_split_deterministic_and_in_range():
    ids = [f"m_csa:{i}" for i in range(60)]
    f1 = [_fold_of(e) for e in ids]
    f2 = [_fold_of(e) for e in ids]
    assert f1 == f2  # deterministic
    assert all(0 <= f < N_FOLDS for f in f1)
    assert 0 < sum(f1) < len(ids)  # both folds populated


# --------------------------------------------------------------------------- #
# Cutoff-keep rule + residual energy read
# --------------------------------------------------------------------------- #
def test_keep_for_cutoff_monotonic_and_cap():
    eig = [10.0, 5.0, 3.0, 1.0, 0.5, 0.3, 0.2]
    total = sum(eig)
    dims = [_keep_for_cutoff(eig, total, c, max_dim=99)["pca_dim"] for c in (0.5, 0.9, 0.99)]
    assert dims[0] <= dims[1] <= dims[2]  # higher cutoff keeps >= dims
    # cap binds: 99% needs >3 dims but cap=2
    capped = _keep_for_cutoff(eig, total, 0.99, max_dim=2)
    assert capped["pca_dim"] == 2 and capped["cap_binds"] is True
    assert capped["uncapped_pca_dim_needed"] > 2


def test_row_projection_energies_monotone_residual():
    # atlas spans dims 0-2; build the shared decomposition
    base = {"c1": [3.0, 0.0, 0.0], "c2": [0.0, 3.0, 0.0], "c3": [0.0, 0.0, 3.0]}
    vecs = []
    for b in base.values():
        for j in range(4):
            vecs.append([b[k] + (0.05 * j if k == 0 else 0.0) for k in range(3)] + [0.0, 0.0])
    pca = _atlas_pca_full(vecs)
    # a row with mass in the out-of-span dims 3,4
    total, cum = _row_projection_energies(pca, [1.0, 1.0, 1.0, 5.0, 5.0])
    # cumulative in-span energy is non-decreasing and bounded by total
    assert all(cum[i] <= cum[i + 1] + 1e-9 for i in range(len(cum) - 1))
    assert cum[-1] <= total + 1e-6
    # residual = total - cum[k] is non-increasing in k, and stays large (out-of-span mass)
    resid = [max(total - c, 0.0) for c in cum]
    assert all(resid[i] >= resid[i + 1] - 1e-9 for i in range(len(resid) - 1))
    assert resid[-1] > 1.0  # dims 3,4 carry energy no atlas axis can absorb


# --------------------------------------------------------------------------- #
# End-to-end synthetic
# --------------------------------------------------------------------------- #
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
    # held-out in-scope: on the atlas span, near a class
    classes = list(base)
    for q in range(16):
        b = base[classes[q % len(classes)]]
        rows[f"q{q}"] = {
            "entry_id": f"q{q}",
            "embedding": [b[k] * 0.95 for k in range(3)] + [0.0, 0.0],
            "split_assignment": "heldout",
            "true_fingerprint_id": classes[q % len(classes)],
        }
    # held-out OOS: mass in the out-of-span dims 3,4
    for o in range(16):
        rows[f"o{o}"] = {
            "entry_id": f"o{o}",
            "embedding": [1.0, 1.0, 1.0, 4.0 + 0.1 * o, 4.0],
            "split_assignment": "heldout",
            "true_fingerprint_id": None,
        }
    # half the OOS read as cofactor-confounded so H3 has a populated subset
    cof = {}
    for e in rows:
        hot = e.startswith("o") and (int(e[1:]) % 2 == 0)
        cof[e] = {"flavin": 0.9 if hot else 0.05, "heme": 0.05, "plp": 0.05}
    geo = {
        e: {"score": 0.85 if rows[e]["true_fingerprint_id"] else 0.3, "role_match_fraction": 0.9}
        for e in rows
    }
    return rows, cof, geo


def test_compute_end_to_end_synthetic():
    rows, cof, geo = _synthetic_inputs()
    res = compute_residual_robustness(rows, cof, geo)
    assert res["status"] == "computed"
    # the residual cleanly separates out-of-span OOS from on-span in-scope
    sweep = res["pca_cutoff_sweep"]
    assert all(
        r["deployment_pool"]["auc_all"] is not None and r["deployment_pool"]["auc_all"] >= 0.9
        for r in sweep["per_cutoff"]
    )
    # S1 (all above the floor) and S2 (cutoff-stable) are plumbing properties of the clean
    # synthetic; S3 (agnostic > confounded, strict) is a real-data directional property --
    # synthetic OOS are statistically identical across the cofactor strata -- so `holds`
    # is only asserted to resolve to a bool here.
    assert sweep["S1_all_ge_min_auc"] is True
    assert sweep["S2_spread_within_band"] is True
    assert isinstance(sweep["holds"], bool)
    # confirmatory structure present; the held-out confirmation fold reproduces
    conf = res["confirmatory_split"]
    assert conf["confirmation_fold"]["auc_all"] is not None
    assert conf["design_echo_fold"]["auc_all"] is not None
    assert isinstance(conf["overall_pass"], bool)
    for key in ("sweep_holds", "confirmatory_pass", "residual_confirmed_as_lever"):
        assert isinstance(res["verdict"][key], bool)
    # anchor check is present (no committed reference to match on synthetic data)
    assert "anchor_check" in res


def test_cutoff_sweep_directional_structure():
    rows, cof, geo = _synthetic_inputs()
    from catalytic_earth.mechanism_feature_residual_robustness import _build_pools

    pools = _build_pools(rows, cof, geo)
    atlas = pools["atlas"]["atlas"]
    pca = _atlas_pca_full([rows[e]["embedding"] for e in atlas])
    energies = {e: _row_projection_energies(pca, rows[e]["embedding"]) for e in rows}
    sweep = _cutoff_sweep(pca, energies, pools)
    # every cutoff produced an all-OOS AUC and an agnostic/confounded breakdown
    for r in sweep["per_cutoff"]:
        assert r["deployment_pool"]["auc_all"] is not None
    assert set(sweep["deployment_auc_all_by_cutoff"]) == {"0.95", "0.97", "0.99"}


# --------------------------------------------------------------------------- #
# Optional integration smoke against the persisted artifacts (slow; gated)
# --------------------------------------------------------------------------- #
def test_integration_residual_robustness_if_present():
    if not (ESM.exists() and COF.exists() and PREDICTED.exists()):
        return
    if not os.environ.get("CATALYTIC_RUN_SLOW"):
        return  # the full atlas eigendecomposition is slow; opt-in only
    audit, result = build_residual_robustness_audit(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF, predicted_geometry_audit_path=PREDICTED
    )
    assert result["status"] == "computed"
    # deployment pool matches the embedding eval's pool exactly
    assert result["counts"]["deployment_pool"] == {
        "inscope": 47, "oos": 79, "confounded": 6, "agnostic": 73}
    # the 99%/128-dim sweep point reproduces the committed residual AUC 0.721
    assert result["anchor_check"]["reproduces_committed"] is True
    assert abs(result["anchor_check"]["deployed_residual_auc_deployment"] - 0.72098) < 0.005
    # the sweep evaluated all three cutoffs and produced a holds verdict (bool)
    sweep = result["pca_cutoff_sweep"]
    assert set(sweep["deployment_auc_all_by_cutoff"]) == {"0.95", "0.97", "0.99"}
    assert isinstance(sweep["holds"], bool)
    # the confirmatory split read both folds with a permutation p-value (bools resolved)
    conf = result["confirmatory_split"]
    assert conf["confirmation_fold"]["permutation"]["n_permutations"] == 2000
    assert isinstance(conf["overall_pass"], bool)
    assert isinstance(result["verdict"]["residual_confirmed_as_lever"], bool)
