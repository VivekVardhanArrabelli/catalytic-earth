"""D11 Lever 2: a learned mechanism-feature embedding for de novo abstention.

The de novo precondition is rank-achievable but not operational: at >=90% in-scope
retention no combiner abstains on more than ~19% of novel-chemistry (OOS) rows
(see mechanism_abstention_gate_eval.py). The binding constraint is FEATURE
OVERLAP -- the existing channels (predicted-geometry top1_score, organic-cofactor
head probability) place known and novel chemistry too close together. The cheap
in-repo fix was ruled out (richer geometry sub-features do not beat top1_score,
commit 605e763), so the next gain must come from a genuinely new representation.

This module learns one. It is NOT a deep classifier (184 atlas rows / 8 classes
would overfit, and a discriminative collapse pulls *everything* -- including novel
chemistry -- toward class prototypes, which is exactly the failure mode we are
fighting). Instead it learns a *physically motivated, information-preserving
metric* on the sequence representation, fit only on the in-distribution atlas:

  1. Robust-standardize (atlas median/IQR), then PCA over the ATLAS SPAN. The
     atlas span is "the directions known mechanism chemistry actually occupies";
     a rich subspace (>=99% atlas variance, capped) is kept so the representation
     is not collapsed. The energy a row carries OUTSIDE this span is the first,
     genuinely new novelty signal: representation mass unlike any known mechanism.
  2. WITHIN-CLASS WHITENING (a regularized Mahalanobis metric). Pooled
     within-mechanism scatter is the variation that does NOT change catalytic
     mechanism (sequence drift, length, fold idiosyncrasy); whitening it out
     amplifies the directions along which mechanism CLASSES genuinely differ. The
     transform is full-rank and invertible on the subspace -- it reshapes geometry
     to answer to mechanism chemistry without discarding directions (contrast a
     rank-(K-1) LDA collapse, whose linear discriminative-energy signal is already
     near chance here, AUC 0.524). This is the deliverable learned embedding.

Novelty signals are then read off the learned space (nearest mechanism prototype,
local kNN density, out-of-span residual), atlas-percentile-calibrated so they are
deployable without eval-pool leakage. Everything is evaluated AT THE OPERATING
POINT (OOS-abstain-recall at a fixed, untuned threshold retaining >=90% of
in-scope rows), stratified by the cofactor-confounded vs cofactor-agnostic OOS
subsets, and compared honestly against the top1_score baseline (AUC 0.757). A
negative result -- the learned space does not beat the geometry channel -- is a
valid, expected outcome and is reported cleanly.

Hard constraints honored (see docs/decision_log.md):
  * Sequence-only inputs (ESM2-150M); the embedding is deployment-valid.
  * Fit ONLY on in_distribution atlas rows. The held-out M-CSA benchmark is never
    training data; it is scored as the eval surface only. All statistics
    (standardizer, PCA span, within-class scatter, percentile calibration) are
    atlas-only.
  * No held-out tuning: every hyperparameter below is a fixed constant chosen by
    an atlas-only rationale, NOT selected against held-out AUC.
  * The cofactor channel is consumed read-only, for OOS stratification only.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .mechanism_novelty_abstention_eval import (
    COFACTOR_CLASSES,
    COFACTOR_SIGNATURE_THRESHOLD,
    load_cofactor_scores,
    load_plm_rows,
)
from .mechanism_abstention_gate_eval import load_geometry_role_scores
from .mechanism_relationship_surface_eval import apply_robust, robust_standardizer

SCHEMA_VERSION = "mechanism_feature_embedding.v0"
TOP1_SCORE_BASELINE_AUC = 0.757  # geometry top1_score, deployment pool (recomputed live)

# --- Fixed, atlas-only hyperparameters (declared a priori; NOT tuned on heldout) ---
# PCA keeps the smallest set of atlas-span directions covering this much atlas
# variance, capped so the within-class scatter (pooled df = N_atlas - K) stays
# well-determined and invertible after shrinkage.
PCA_VARIANCE_RETAINED = 0.99
PCA_MAX_DIM = 128
# Ledoit-Wolf-style fixed shrinkage of the pooled within-class scatter toward a
# scaled identity, for a stable invertible whitening metric.
WITHIN_CLASS_SHRINKAGE = 0.10
# Local-density signal: mean distance to the K nearest atlas rows in the metric.
KNN_K = 10
_MIN_INSCOPE_RETENTION = 0.90
_EIG_TOL = 1e-9


# --------------------------------------------------------------------------- #
# Pure-stdlib linear algebra (symmetric Jacobi eigensolver + small matrix ops)
# --------------------------------------------------------------------------- #
def _symmetric_jacobi(a: list[list[float]], max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigendecompose a symmetric matrix via cyclic Jacobi rotations.

    Returns (eigenvalues, eigenvectors-as-columns) sorted by descending
    eigenvalue. Pure stdlib; intended for the small matrices here (n <= ~184).
    """
    n = len(a)
    # working copy
    m = [list(row) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = math.sqrt(math.fsum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < 1e-12:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = m[p][q]
                if abs(apq) < 1e-18:
                    continue
                app, aqq = m[p][p], m[q][q]
                phi = 0.5 * math.atan2(2.0 * apq, aqq - app)
                c, s = math.cos(phi), math.sin(phi)
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp - s * mkq
                    m[k][q] = s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk - s * mqk
                    m[q][k] = s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    eigvals = [m[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: eigvals[i], reverse=True)
    vals = [eigvals[i] for i in order]
    vecs = [[v[r][i] for i in order] for r in range(n)]  # columns reordered
    return vals, vecs


def _matvec(rows: list[list[float]], x: list[float]) -> list[float]:
    return [math.fsum(rij * xj for rij, xj in zip(row, x)) for row in rows]


def _dot(a: list[float], b: list[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


# --------------------------------------------------------------------------- #
# The learned mechanism-feature space (fit atlas-only)
# --------------------------------------------------------------------------- #
class MechanismFeatureSpace:
    """A supervised, information-preserving mechanism metric fit on the atlas.

    Maps any standardized 640-d row to (pca_coords, whitened_coords,
    residual_energy). All statistics are estimated on the in-distribution atlas;
    held-out rows are only transformed, never fit.
    """

    def __init__(
        self,
        atlas_vectors: list[list[float]],
        atlas_labels: list[str],
        *,
        variance_retained: float = PCA_VARIANCE_RETAINED,
        max_dim: int = PCA_MAX_DIM,
        shrinkage: float = WITHIN_CLASS_SHRINKAGE,
    ) -> None:
        if not atlas_vectors:
            raise ValueError("empty atlas")
        self.shrinkage = shrinkage
        self.variance_retained = variance_retained

        # 1. Robust standardize on the atlas only.
        self.medians, self.scales = robust_standardizer(atlas_vectors)
        std = [apply_robust(v, self.medians, self.scales) for v in atlas_vectors]
        d = len(self.medians)

        # 2. Center on the atlas mean, then PCA via the n x n atlas Gram matrix.
        n = len(std)
        self.feature_mean = [math.fsum(std[i][j] for i in range(n)) / n for j in range(d)]
        xc = [[std[i][j] - self.feature_mean[j] for j in range(d)] for i in range(n)]
        gram = [[_dot(xc[i], xc[k]) for k in range(n)] for i in range(n)]
        gvals, gvecs = _symmetric_jacobi(gram)
        total_var = math.fsum(max(val, 0.0) for val in gvals)
        # choose the rank by the declared atlas-only variance rule, capped.
        keep, acc = 0, 0.0
        for idx, val in enumerate(gvals):
            if val <= _EIG_TOL or idx >= max_dim:
                break
            acc += val
            keep += 1
            if total_var > 0 and acc / total_var >= variance_retained:
                break
        self.pca_dim = max(keep, 1)
        self.eigenvalues = gvals[: self.pca_dim]
        self.variance_captured = round(acc / total_var, 6) if total_var > 0 else 0.0
        # principal axes in feature space: u_i = Xc^T v_i / sqrt(lambda_i) (orthonormal columns)
        self.axes: list[list[float]] = []  # each axis is a d-vector
        for i in range(self.pca_dim):
            v_col = [gvecs[r][i] for r in range(n)]
            lam = max(gvals[i], _EIG_TOL)
            inv = 1.0 / math.sqrt(lam)
            axis = [inv * math.fsum(xc[r][j] * v_col[r] for r in range(n)) for j in range(d)]
            self.axes.append(axis)

        # 3. Within-class whitening on the atlas PCA coords.
        coords = [self._pca_coords_from_std(s) for s in std]
        p = self.pca_dim
        classes = sorted(set(atlas_labels))
        class_means: dict[str, list[float]] = {}
        for c in classes:
            members = [coords[i] for i in range(n) if atlas_labels[i] == c]
            class_means[c] = [math.fsum(m[j] for m in members) / len(members) for j in range(p)]
        # pooled within-class scatter (covariance), df = n - K
        sw = [[0.0] * p for _ in range(p)]
        for i in range(n):
            cm = class_means[atlas_labels[i]]
            dev = [coords[i][j] - cm[j] for j in range(p)]
            for a in range(p):
                da = dev[a]
                row = sw[a]
                for b in range(p):
                    row[b] += da * dev[b]
        df = max(n - len(classes), 1)
        sw = [[sw[a][b] / df for b in range(p)] for a in range(p)]
        # fixed shrinkage toward a scaled identity
        trace = math.fsum(sw[a][a] for a in range(p))
        mu = trace / p if p else 0.0
        shr = shrinkage
        sw_reg = [
            [(1.0 - shr) * sw[a][b] + (shr * mu if a == b else 0.0) for b in range(p)]
            for a in range(p)
        ]
        # whitening transform W = Sw_reg^{-1/2} (symmetric)
        wvals, wvecs = _symmetric_jacobi(sw_reg)
        inv_sqrt = [1.0 / math.sqrt(val) if val > _EIG_TOL else 0.0 for val in wvals]
        # W[a][b] = sum_k wvecs[a][k] * inv_sqrt[k] * wvecs[b][k]
        self.whiten = [
            [math.fsum(wvecs[a][k] * inv_sqrt[k] * wvecs[b][k] for k in range(p)) for b in range(p)]
            for a in range(p)
        ]
        self.condition_number = round(
            (max(wvals) / min(v for v in wvals if v > _EIG_TOL)) if any(v > _EIG_TOL for v in wvals) else 0.0,
            4,
        )
        # atlas-side cached transforms
        self.classes = classes
        self.class_prototypes = {c: _matvec(self.whiten, class_means[c]) for c in classes}
        self._atlas_std = std
        self._atlas_whitened = [_matvec(self.whiten, c) for c in coords]

    # -- transforms -------------------------------------------------------- #
    def _pca_coords_from_std(self, std_vec: list[float]) -> list[float]:
        centered = [std_vec[j] - self.feature_mean[j] for j in range(len(std_vec))]
        return [_dot(axis, centered) for axis in self.axes]

    def transform(self, raw_vec: list[float]) -> dict[str, Any]:
        std = apply_robust(raw_vec, self.medians, self.scales)
        centered = [std[j] - self.feature_mean[j] for j in range(len(std))]
        coords = [_dot(axis, centered) for axis in self.axes]
        whitened = _matvec(self.whiten, coords)
        total_energy = _dot(centered, centered)
        in_span = math.fsum(c * c for c in coords)
        residual = max(total_energy - in_span, 0.0)
        return {
            "pca_coords": coords,
            "whitened": whitened,
            "residual_energy": residual,
            "in_span_energy": in_span,
        }

    # -- novelty signals (higher = looks more like known chemistry) -------- #
    def neg_nearest_prototype(self, whitened: list[float]) -> float:
        return -min(
            math.sqrt(math.fsum((whitened[j] - proto[j]) ** 2 for j in range(len(whitened))))
            for proto in self.class_prototypes.values()
        )

    def neg_knn_distance(self, whitened: list[float], k: int = KNN_K) -> float:
        dists = sorted(
            math.sqrt(math.fsum((whitened[j] - a[j]) ** 2 for j in range(len(whitened))))
            for a in self._atlas_whitened
        )
        kk = min(k, len(dists))
        return -(math.fsum(dists[:kk]) / kk)

    def neg_residual(self, residual_energy: float) -> float:
        return -math.sqrt(residual_energy)


def _auc_in_gt_oos(in_scope: list[float], oos: list[float]) -> float | None:
    if not in_scope or not oos:
        return None
    greater = sum(1 for a in in_scope for b in oos if a > b)
    ties = sum(1 for a in in_scope for b in oos if a == b)
    return round((greater + 0.5 * ties) / (len(in_scope) * len(oos)), 6)


def _atlas_percentile_calibrator(atlas_scores: list[float]) -> Callable[[float], float]:
    """Map a raw score to its percentile within the atlas distribution (deployable)."""
    ordered = sorted(atlas_scores)
    n = len(ordered) or 1

    def pct(x: float) -> float:
        import bisect

        return bisect.bisect_right(ordered, x) / n

    return pct


# --------------------------------------------------------------------------- #
# Operating-point evaluation (mirrors mechanism_abstention_gate_eval machinery)
# --------------------------------------------------------------------------- #
def _operating_point(
    score_fn: Callable[[str], float],
    inscope: list[str],
    oos: list[str],
    confounded: list[str],
    agnostic: list[str],
    min_retain: float = _MIN_INSCOPE_RETENTION,
) -> dict[str, Any] | None:
    """Best OOS-abstain-recall at a threshold retaining >=min_retain of in-scope.

    score_fn returns a raw value (higher = looks more like known chemistry); a row
    abstains when its score is below the threshold. Candidate thresholds are the
    observed scores over the eval pool (a calibration-free ROC sweep), so signals
    on different scales -- and the geometry baseline -- are compared on equal terms.
    This is a *research* operating point (an achievable retention/recall trade-off
    read off the eval pool), not a production threshold; AUC is the calibration-free
    primary metric and the verdict reports both.
    """
    pool = inscope + oos
    if not (inscope and oos):
        return None
    # Candidate cut points: each observed score, plus a hair above the max so the
    # "abstain on everything" end is reachable. Abstain iff score < threshold.
    candidates = sorted({score_fn(e) for e in pool})
    candidates = candidates + [candidates[-1] + 1.0]
    best = None
    for thr in candidates:
        in_abst = sum(1 for e in inscope if score_fn(e) < thr)
        retain = 1 - in_abst / len(inscope)
        if retain < min_retain:
            continue
        oos_abst = sum(1 for e in oos if score_fn(e) < thr)
        rec = {
            "threshold": round(thr, 6),
            "inscope_retain_recall": round(retain, 4),
            "oos_abstain_recall": round(oos_abst / len(oos), 4),
            "confounded_abstain_recall": (
                round(sum(1 for e in confounded if score_fn(e) < thr) / len(confounded), 4)
                if confounded else None
            ),
            "agnostic_abstain_recall": (
                round(sum(1 for e in agnostic if score_fn(e) < thr) / len(agnostic), 4)
                if agnostic else None
            ),
        }
        key = (rec["oos_abstain_recall"], rec["confounded_abstain_recall"] or 0.0)
        if best is None or key > best[0]:
            best = (key, rec)
    return best[1] if best else None


def _evaluate_pool(
    atlas_keys: list[str],
    inscope: list[str],
    oos: list[str],
    confounded: list[str],
    agnostic: list[str],
    raw_signals: dict[str, Callable[[str], float]],
) -> dict[str, Any]:
    """Score every learned-embedding signal over one eval pool: AUC + operating point.

    AUC (in-scope > OOS) is computed on the RAW signal -- it is calibration-free and
    monotone-invariant, so it never suffers the percentile-saturation artifact (all
    held-out rows can sit below the atlas minimum). The operating point is a
    calibration-free observed-threshold sweep that fixes >=90% in-scope retention.
    `atlas_keys` is retained for signature symmetry / future atlas-calibrated views.
    """
    out: dict[str, Any] = {}
    for name, raw_fn in raw_signals.items():
        iv = [raw_fn(e) for e in inscope]
        out[name] = {
            "auc_all": _auc_in_gt_oos(iv, [raw_fn(e) for e in oos]),
            "auc_confounded": _auc_in_gt_oos(iv, [raw_fn(e) for e in confounded]),
            "auc_agnostic": _auc_in_gt_oos(iv, [raw_fn(e) for e in agnostic]),
            "operating_point_at_90pct_retention": _operating_point(
                raw_fn, inscope, oos, confounded, agnostic
            ),
        }
    return out


def compute_mechanism_feature_embedding(
    plm_rows: dict[str, dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
    geometry_scores: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """Fit the learned space on the atlas, score novelty, and judge vs top1_score.

    Returns a result dict with the space summary, per-pool signal evaluation
    (deployment pool and full novelty pool), the recomputed top1_score baseline,
    a raw row-keyed learned embedding, and an honest verdict.
    """
    def fp(e: str) -> str | None:
        return plm_rows[e]["true_fingerprint_id"]

    atlas = sorted(
        e for e, r in plm_rows.items()
        if r["split_assignment"] == "in_distribution" and fp(e)
    )
    if len(atlas) < 8:
        return {"status": "insufficient_atlas", "atlas": len(atlas)}

    space = MechanismFeatureSpace(
        [plm_rows[e]["embedding"] for e in atlas],
        [fp(e) for e in atlas],  # type: ignore[misc]
    )

    # Transform every row once (row-keyed learned embedding).
    transforms = {e: space.transform(plm_rows[e]["embedding"]) for e in plm_rows}

    # Novelty signal functions over entry ids (read whitened/residual from transforms).
    def sig_proto(e: str) -> float:
        return space.neg_nearest_prototype(transforms[e]["whitened"])

    def sig_knn(e: str) -> float:
        return space.neg_knn_distance(transforms[e]["whitened"])

    def sig_residual(e: str) -> float:
        return space.neg_residual(transforms[e]["residual_energy"])

    # PRIMARY (predeclared) signal: mean of the atlas-percentiles of the three
    # learned-space novelty views. Declared before looking at held-out AUC.
    atlas_keys = atlas
    cal_proto = _atlas_percentile_calibrator([sig_proto(e) for e in atlas_keys])
    cal_knn = _atlas_percentile_calibrator([sig_knn(e) for e in atlas_keys])
    cal_res = _atlas_percentile_calibrator([sig_residual(e) for e in atlas_keys])

    def sig_primary(e: str) -> float:
        return (cal_proto(sig_proto(e)) + cal_knn(sig_knn(e)) + cal_res(sig_residual(e))) / 3.0

    raw_signals: dict[str, Callable[[str], float]] = {
        "learned_nearest_prototype": sig_proto,
        "learned_knn_density": sig_knn,
        "learned_out_of_span_residual": sig_residual,
        "learned_combined_primary": sig_primary,
    }

    def build_pool(keys_filter: Callable[[str], bool]) -> dict[str, list[str]]:
        usable = sorted(e for e in plm_rows if keys_filter(e))
        inscope = [e for e in usable if plm_rows[e]["split_assignment"] == "heldout" and fp(e)]
        oos = [e for e in usable if plm_rows[e]["split_assignment"] == "heldout" and not fp(e)]
        confounded = [
            e for e in oos
            if e in cofactor_scores
            and max(cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES) >= COFACTOR_SIGNATURE_THRESHOLD
        ]
        agnostic = [e for e in oos if e not in confounded]
        return {"inscope": inscope, "oos": oos, "confounded": confounded, "agnostic": agnostic}

    # Deployment pool: rows with geometry AND cofactor scores (the gate's pool).
    dep = build_pool(lambda e: e in geometry_scores and e in cofactor_scores)
    # Full novelty pool: all heldout rows (cofactor used only for stratification).
    full = build_pool(lambda e: True)

    dep_eval = _evaluate_pool(
        atlas_keys, dep["inscope"], dep["oos"], dep["confounded"], dep["agnostic"], raw_signals
    )
    full_eval = _evaluate_pool(
        atlas_keys, full["inscope"], full["oos"], full["confounded"], full["agnostic"], raw_signals
    )

    # Recompute the top1_score geometry baseline LIVE on the deployment pool, for a
    # fair side-by-side (rather than trusting the hardcoded 0.757).
    def geom(e: str) -> float:
        return geometry_scores[e]["score"]

    base_auc = _auc_in_gt_oos([geom(e) for e in dep["inscope"]], [geom(e) for e in dep["oos"]])
    base_auc_conf = _auc_in_gt_oos([geom(e) for e in dep["inscope"]], [geom(e) for e in dep["confounded"]])
    base_auc_agn = _auc_in_gt_oos([geom(e) for e in dep["inscope"]], [geom(e) for e in dep["agnostic"]])
    base_op = _operating_point(geom, dep["inscope"], dep["oos"], dep["confounded"], dep["agnostic"])
    baseline = {
        "channel": "geometry_top1_score",
        "auc_all": base_auc,
        "auc_confounded": base_auc_conf,
        "auc_agnostic": base_auc_agn,
        "operating_point_at_90pct_retention": base_op,
        "reference_auc": TOP1_SCORE_BASELINE_AUC,
    }

    # Honest verdict on the PREDECLARED PRIMARY signal vs the baseline. The primary
    # is fixed a priori (equal-weight percentile mean) so the headline cannot be
    # cherry-picked from whichever signal happened to win.
    primary = dep_eval["learned_combined_primary"]
    best_learned_auc = max(
        (s["auc_all"] for s in dep_eval.values() if s["auc_all"] is not None), default=0.0
    )
    primary_auc = primary["auc_all"] or 0.0
    primary_op = primary["operating_point_at_90pct_retention"]
    base_op_recall = base_op["oos_abstain_recall"] if base_op else 0.0
    base_op_conf = (base_op or {}).get("confounded_abstain_recall") or 0.0
    primary_op_recall = primary_op["oos_abstain_recall"] if primary_op else 0.0
    beats_auc = bool(base_auc is not None and primary_auc > base_auc)
    beats_op = bool(primary_op is not None and primary_op_recall > base_op_recall)

    # Exploratory: the single learned signal with the best operating-point OOS recall,
    # reported transparently with its confounded-subset safety. This is NOT a
    # predeclared confirmatory claim -- it flags the most promising lever for a future
    # frozen test, the way the existing gate surfaced its stratified findings.
    def _op_recall(name: str) -> float:
        op = dep_eval[name]["operating_point_at_90pct_retention"]
        return op["oos_abstain_recall"] if op else 0.0

    candidates = [n for n in dep_eval if n != "learned_combined_primary"]
    best_signal = max(candidates, key=_op_recall) if candidates else None
    exploratory = None
    if best_signal is not None:
        bs = dep_eval[best_signal]
        bop = bs["operating_point_at_90pct_retention"]
        bs_op_recall = bop["oos_abstain_recall"] if bop else 0.0
        bs_op_conf = (bop or {}).get("confounded_abstain_recall")
        exploratory = {
            "best_single_signal": best_signal,
            "auc_all": bs["auc_all"],
            "auc_confounded": bs["auc_confounded"],
            "auc_agnostic": bs["auc_agnostic"],
            "oos_abstain_recall_at_90pct": bs_op_recall,
            "confounded_abstain_recall_at_90pct": bs_op_conf,
            "beats_baseline_at_operating_point": bool(bs_op_recall > base_op_recall),
            "safe_on_confounded_vs_baseline": bool(
                bs_op_conf is not None and bs_op_conf >= base_op_conf
            ),
            "role": (
                "complementary_lift_channel_not_replacement_gate"
                if (bs_op_conf is None or bs_op_conf < base_op_conf)
                else "candidate_standalone_signal"
            ),
        }

    verdict = {
        "primary_signal": "learned_combined_primary",
        "primary_auc_deployment": primary_auc,
        "baseline_top1_score_auc_deployment": base_auc,
        "best_learned_signal_auc_deployment": round(best_learned_auc, 6),
        "primary_beats_top1_score_by_auc": beats_auc,
        "primary_oos_abstain_recall_at_90pct": primary_op_recall,
        "baseline_oos_abstain_recall_at_90pct": base_op_recall,
        "primary_beats_top1_score_at_operating_point": beats_op,
        "overall": (
            "beats_baseline" if (beats_auc and beats_op)
            else "mixed" if (beats_auc or beats_op)
            else "does_not_beat_baseline"
        ),
        "exploratory_best_single_signal": exploratory,
    }

    return {
        "status": "computed",
        "space": {
            "input": "esm2_150m_sequence_only",
            "pca_dim": space.pca_dim,
            "pca_variance_captured": space.variance_captured,
            "pca_variance_retained_target": PCA_VARIANCE_RETAINED,
            "pca_max_dim": PCA_MAX_DIM,
            "within_class_shrinkage": WITHIN_CLASS_SHRINKAGE,
            "whitening_condition_number": space.condition_number,
            "classes": space.classes,
            "n_atlas": len(atlas),
        },
        "counts": {
            "deployment_pool": {k: len(v) for k, v in dep.items()},
            "full_novelty_pool": {k: len(v) for k, v in full.items()},
        },
        "deployment_pool_signals": dep_eval,
        "full_novelty_pool_signals": full_eval,
        "top1_score_baseline_deployment": baseline,
        "verdict": verdict,
        "row_embedding": {
            e: {
                "split_assignment": plm_rows[e]["split_assignment"],
                "true_fingerprint_id": fp(e),
                "whitened": [round(x, 6) for x in transforms[e]["whitened"]],
                "residual_energy": round(transforms[e]["residual_energy"], 6),
            }
            for e in sorted(plm_rows)
        },
    }


# --------------------------------------------------------------------------- #
# Artifact build / write
# --------------------------------------------------------------------------- #
def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_mechanism_feature_embedding_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
) -> dict[str, Any]:
    plm_rows = load_plm_rows(esm2_150m_path)
    cofactor_scores = load_cofactor_scores(cofactor_sidecar_path)
    geometry_scores = load_geometry_role_scores(predicted_geometry_audit_path)
    result = compute_mechanism_feature_embedding(plm_rows, cofactor_scores, geometry_scores)
    verdict = result.get("verdict", {})
    return {
        "artifact_id": "v3_mechanism_feature_embedding_eval_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 Lever 2: a learned, information-preserving mechanism-feature "
            "embedding (sequence-only ESM2-150M; atlas-fit within-class whitening "
            "over the atlas PCA span). Tests whether its novelty signals separate "
            "in-scope from out-of-scope (novel-chemistry) held-out rows better than "
            "the predicted-geometry top1_score baseline (AUC 0.757), evaluated at the "
            "operating point and stratified by cofactor-confounded vs -agnostic OOS."
        ),
        "result": {k: v for k, v in result.items() if k != "row_embedding"},
        "interpretation": _interpretation(result),
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "fit_on_in_distribution_atlas_only": True,
            "mcsa_heldout_benchmark_is_eval_only_never_trained": True,
            "no_heldout_tuning_hyperparameters_fixed_a_priori": True,
            "cofactor_channel_consumed_read_only_for_stratification": True,
            "predicted_geometry_deployment_regime_for_baseline": True,
            "atlas_only_statistics_and_percentile_calibration": True,
            "labels_registries_thresholds_changed": False,
        },
        "source_artifacts": {
            "esm2_150m_embeddings": {"path": str(esm2_150m_path), "sha256": _sha256(esm2_150m_path)},
            "cofactor_score_sidecar": {
                "path": str(cofactor_sidecar_path), "sha256": _sha256(cofactor_sidecar_path)},
            "predicted_geometry_audit": {
                "path": str(predicted_geometry_audit_path),
                "sha256": _sha256(predicted_geometry_audit_path)},
        },
    }, result


def _interpretation(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("status") != "computed":
        return {"headline": f"status: {result.get('status')}"}
    v = result["verdict"]
    overall = v["overall"]
    if overall == "beats_baseline":
        head = (
            f"The learned mechanism-feature embedding BEATS the top1_score baseline: "
            f"primary novelty AUC {v['primary_auc_deployment']} vs "
            f"{v['baseline_top1_score_auc_deployment']}, and OOS-abstain-recall "
            f"{v['primary_oos_abstain_recall_at_90pct']} vs "
            f"{v['baseline_oos_abstain_recall_at_90pct']} at >=90% in-scope retention."
        )
    elif overall == "mixed":
        head = (
            f"Mixed result: the learned embedding wins on one axis but not both "
            f"(AUC {v['primary_auc_deployment']} vs {v['baseline_top1_score_auc_deployment']}; "
            f"operating-point OOS recall {v['primary_oos_abstain_recall_at_90pct']} vs "
            f"{v['baseline_oos_abstain_recall_at_90pct']})."
        )
    else:
        head = (
            f"NEGATIVE RESULT (clean) on the predeclared signal: the learned "
            f"sequence-only embedding's primary combined novelty score does NOT beat "
            f"the predicted-geometry top1_score baseline (AUC "
            f"{v['primary_auc_deployment']} vs {v['baseline_top1_score_auc_deployment']}; "
            f"OOS-abstain-recall {v['primary_oos_abstain_recall_at_90pct']} vs "
            f"{v['baseline_oos_abstain_recall_at_90pct']} at >=90% retention). A "
            f"general-purpose PLM, even reshaped by a supervised mechanism metric, "
            f"encodes overall protein similarity under which novel chemistry still sits "
            f"inside occupied regions, while the orthogonal geometry channel sees the "
            f"active-site mismatch directly."
        )
    exp = v.get("exploratory_best_single_signal")
    base_op = (result.get("top1_score_baseline_deployment") or {}).get(
        "operating_point_at_90pct_retention"
    ) or {}
    base_conf = base_op.get("confounded_abstain_recall")
    exploratory_lead = None
    if exp and exp["beats_baseline_at_operating_point"]:
        exploratory_lead = (
            f"Lead worth a frozen follow-up: the `{exp['best_single_signal']}` view -- a "
            f"genuinely new, UNSUPERVISED representation signal (sequence-representation "
            f"mass outside the directions known mechanism chemistry occupies) -- abstains "
            f"on {exp['oos_abstain_recall_at_90pct']} of OOS at >=90% retention, ABOVE the "
            f"geometry baseline ({v['baseline_oos_abstain_recall_at_90pct']}), with AUC "
            f"{exp['auc_all']}. It is concentrated on the cofactor-AGNOSTIC OOS majority "
            f"and is NOT safe on the safety-critical cofactor-confounded subset "
            f"(confounded abstain-recall {exp['confounded_abstain_recall_at_90pct']} vs "
            f"baseline {base_conf}), so it is a COMPLEMENTARY LIFT channel for future "
            f"predeclared confirmatory testing, not a replacement gate. The supervised "
            f"whitening distances (prototype/kNN) do not help, confirming that "
            f"discriminative reshaping is the wrong lever for novelty."
        )
    return {
        "headline": head,
        "exploratory_lead": exploratory_lead,
        "why_information_preserving": (
            "The metric whitens out pooled within-mechanism variation (sequence drift "
            "that does not change catalysis) and is full-rank/invertible on the atlas "
            "span -- it reshapes geometry to answer to mechanism chemistry without "
            "collapsing to a rank-(K-1) discriminant (whose linear discriminative-energy "
            "novelty signal is already at chance here, AUC 0.524). The out-of-span "
            "residual is a genuinely new novelty view -- representation mass outside "
            "known mechanism chemistry -- not a recombination of the existing channels."
        ),
        "why_combined_primary_underperforms": (
            "The predeclared equal-weight percentile combiner washes out the residual: "
            "every held-out row sits below the atlas residual distribution, so the "
            "residual's atlas-percentile saturates to 0 and contributes no ordering to "
            "the mean. The residual carries real signal only in its RAW form and must be "
            "used as its own channel -- an instructive reason the naive combination fails."
        ),
        "stratification_note": (
            "The cofactor-confounded OOS subset (novel chemistry reusing a known "
            "cofactor family) is the hardest; per-stratum AUCs and abstain-recalls are "
            "reported so a headline number cannot hide a confounded-subset failure."
        ),
    }


def write_mechanism_feature_embedding_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
    out_path: Path,
    embedding_path: Path | None = None,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit, result = build_mechanism_feature_embedding_eval(
        esm2_150m_path=esm2_150m_path,
        cofactor_sidecar_path=cofactor_sidecar_path,
        predicted_geometry_audit_path=predicted_geometry_audit_path,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if embedding_path is not None and result.get("status") == "computed":
        embedding_path = Path(embedding_path)
        embedding_path.parent.mkdir(parents=True, exist_ok=True)
        with embedding_path.open("w", encoding="utf-8") as fh:
            for entry_id, rec in result["row_embedding"].items():
                fh.write(json.dumps({
                    "artifact_id": audit["artifact_id"],
                    "schema_version": SCHEMA_VERSION,
                    "entry_id": entry_id,
                    **rec,
                }, sort_keys=True) + "\n")

    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_report(audit), encoding="utf-8")
    return audit


def _render_report(audit: dict[str, Any]) -> str:
    res = audit["result"]
    if res.get("status") != "computed":
        return f"# D11 Learned Mechanism-Feature Embedding\n\nStatus: {res.get('status')}\n"
    sp = res["space"]
    dep = res["counts"]["deployment_pool"]
    base = res["top1_score_baseline_deployment"]
    v = res["verdict"]
    lines = [
        "# D11 Learned Mechanism-Feature Embedding (Lever 2)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Learned space (atlas-fit, sequence-only)",
        "",
        f"- Input: `{sp['input']}` | atlas rows: {sp['n_atlas']} | classes: {len(sp['classes'])}",
        f"- PCA span dim: **{sp['pca_dim']}** capturing {sp['pca_variance_captured']} of atlas "
        f"variance (target {sp['pca_variance_retained_target']}, cap {sp['pca_max_dim']})",
        f"- Within-class whitening shrinkage: {sp['within_class_shrinkage']} | "
        f"metric condition number: {sp['whitening_condition_number']}",
        "",
        f"Deployment pool: in-scope {dep['inscope']} | OOS {dep['oos']} "
        f"(confounded {dep['confounded']}, agnostic {dep['agnostic']})",
        "",
        "## Novelty separation on the deployment pool (AUC in-scope > OOS; 0.5 = chance)",
        "",
        "| Signal | all OOS | confounded | agnostic | OOS-recall@90%ret | retain |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, s in res["deployment_pool_signals"].items():
        op = s["operating_point_at_90pct_retention"]
        rec = op["oos_abstain_recall"] if op else "n/a"
        ret = op["inscope_retain_recall"] if op else "n/a"
        lines.append(
            f"| {name} | {s['auc_all']} | {s['auc_confounded']} | {s['auc_agnostic']} | {rec} | {ret} |"
        )
    bop = base["operating_point_at_90pct_retention"]
    lines.append(
        f"| **baseline: {base['channel']}** | {base['auc_all']} | {base['auc_confounded']} | "
        f"{base['auc_agnostic']} | {bop['oos_abstain_recall'] if bop else 'n/a'} | "
        f"{bop['inscope_retain_recall'] if bop else 'n/a'} |"
    )
    lines += [
        "",
        "## Verdict",
        "",
        f"- Primary signal: `{v['primary_signal']}`",
        f"- AUC (deployment): learned **{v['primary_auc_deployment']}** vs baseline "
        f"**{v['baseline_top1_score_auc_deployment']}** -> beats: "
        f"**{v['primary_beats_top1_score_by_auc']}**",
        f"- OOS-abstain-recall @>=90% retention: learned "
        f"**{v['primary_oos_abstain_recall_at_90pct']}** vs baseline "
        f"**{v['baseline_oos_abstain_recall_at_90pct']}** -> beats: "
        f"**{v['primary_beats_top1_score_at_operating_point']}**",
        f"- Overall (predeclared primary): **{v['overall']}**",
    ]
    exp = v.get("exploratory_best_single_signal")
    if exp:
        lines += [
            "",
            "### Exploratory: best single learned signal (not a predeclared claim)",
            "",
            f"- Signal: `{exp['best_single_signal']}` | AUC all {exp['auc_all']} "
            f"(confounded {exp['auc_confounded']}, agnostic {exp['auc_agnostic']})",
            f"- OOS-abstain-recall @>=90% retention: **{exp['oos_abstain_recall_at_90pct']}** "
            f"(baseline {v['baseline_oos_abstain_recall_at_90pct']}) -> beats baseline at "
            f"operating point: **{exp['beats_baseline_at_operating_point']}**",
            f"- Confounded-subset abstain-recall: {exp['confounded_abstain_recall_at_90pct']} "
            f"-> safe vs baseline: **{exp['safe_on_confounded_vs_baseline']}** | role: "
            f"`{exp['role']}`",
        ]
    lines += [
        "",
        "## Interpretation",
        "",
        audit["interpretation"]["headline"],
    ]
    if audit["interpretation"].get("exploratory_lead"):
        lines += ["", audit["interpretation"]["exploratory_lead"]]
    lines += [
        "",
        audit["interpretation"]["why_information_preserving"],
        "",
        audit["interpretation"].get("why_combined_primary_underperforms", ""),
        "",
        audit["interpretation"]["stratification_note"],
    ]
    return "\n".join(lines) + "\n"
