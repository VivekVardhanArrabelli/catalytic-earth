"""Unit tests for the D11 novelty-abstention (de novo precondition) eval.

Pure-stdlib synthetic tests plus an optional integration smoke against the
persisted ESM2-150M embeddings and the cofactor score sidecar. No models, no
network.
"""

from __future__ import annotations

import json
from pathlib import Path

from catalytic_earth.mechanism_novelty_abstention_eval import (
    _auc_in_gt_oos,
    _orthonormal_betweenclass_basis,
    build_mechanism_novelty_abstention_eval,
    compute_cofactor_augmented_signals,
    compute_novelty_signals,
    load_cofactor_scores,
)

ESM = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
COF = Path("artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json")


def test_auc_in_gt_oos_bounds():
    assert _auc_in_gt_oos([3.0, 2.0], [1.0, 0.0]) == 1.0
    assert _auc_in_gt_oos([0.0, 1.0], [2.0, 3.0]) == 0.0
    assert _auc_in_gt_oos([1.0], [1.0]) == 0.5
    assert _auc_in_gt_oos([], [1.0]) == 0.0


def test_orthonormal_basis_is_orthonormal():
    centroids = [[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [1.0, 1.0, 0.0]]
    basis = _orthonormal_betweenclass_basis(centroids, [0.0, 0.0, 0.0])
    # third centroid is in the span of the first two -> rank 2.
    assert len(basis) == 2
    dot = sum(a * b for a, b in zip(basis[0], basis[1]))
    assert abs(dot) < 1e-9
    for vec in basis:
        norm = sum(x * x for x in vec) ** 0.5
        assert abs(norm - 1.0) < 1e-9


def _synthetic_rows():
    # Two atlas classes separated on dim 0; in-scope queries near a class, OOS far.
    def row(eid, split, fp, emb):
        return {"entry_id": eid, "embedding": emb, "split_assignment": split, "true_fingerprint_id": fp}
    rows = {}
    for i in range(4):
        rows[f"a{i}"] = row(f"a{i}", "in_distribution", "f1", [1.0 + 0.01 * i, 0.0, 0.0])
        rows[f"b{i}"] = row(f"b{i}", "in_distribution", "f2", [0.0, 1.0 + 0.01 * i, 0.0])
    rows["q1"] = row("q1", "heldout", "f1", [0.98, 0.02, 0.0])
    rows["q2"] = row("q2", "heldout", "f2", [0.02, 0.98, 0.0])
    rows["o1"] = row("o1", "heldout", None, [0.0, 0.0, 1.0])
    rows["o2"] = row("o2", "heldout", None, [0.0, 0.0, 0.9])
    return rows


def test_compute_novelty_signals_separates_when_oos_is_far():
    res = compute_novelty_signals(_synthetic_rows())
    assert res["status"] == "computed"
    assert res["counts"] == {"atlas": 8, "inscope": 2, "oos": 2}
    # OOS sits orthogonal to both classes -> nearest-centroid cosine should separate.
    assert res["signals"]["nearest_centroid_cosine"]["auc_in_gt_oos"] == 1.0


def test_cofactor_augmented_signals_handle_missing_rows():
    rows = _synthetic_rows()
    cof = {e: {"flavin": 0.1, "heme": 0.1, "plp": 0.1} for e in rows}
    out = compute_cofactor_augmented_signals(rows, cof)
    assert out["status"] == "computed"
    assert set(out["signals"]) == {
        "cofactor_max_raw_score",
        "augmented_nearest_centroid",
        "augmented_centroid_margin",
    }


def test_integration_bare_plm_is_near_chance_if_present():
    if not ESM.exists():
        return
    audit = build_mechanism_novelty_abstention_eval(esm2_150m_path=ESM)
    res = audit["result"]
    assert res["counts"]["atlas"] == 184
    # Bare PLM cannot abstain on novelty: best AUC well under the usable bar.
    assert res["best_auc"] < 0.75
    assert res["abstention_status"] == "unsolved_by_unsupervised_distance"


def test_integration_cofactor_helps_but_insufficient_if_present():
    if not (ESM.exists() and COF.exists()):
        return
    audit = build_mechanism_novelty_abstention_eval(
        esm2_150m_path=ESM, cofactor_sidecar_path=COF
    )
    cof = audit["cofactor_augmented_result"]
    assert cof["status"] == "computed"
    # Cofactor augmentation moves the signal up but does not yet clear the bar.
    assert cof["best_auc"] > audit["result"]["best_auc"]
    assert cof["best_auc"] < 0.75
    assert audit["interpretation"]["cofactor_augmentation_helps_but_insufficient"] is True


def test_load_cofactor_scores_shape_if_present():
    if not COF.exists():
        return
    scores = load_cofactor_scores(COF)
    assert len(scores) == 702
    any_entry = next(iter(scores.values()))
    assert set(any_entry) == {"flavin", "heme", "plp"}
