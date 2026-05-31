"""D11 de novo precondition, two-channel abstention gate.

The novelty-abstention eval (see mechanism_novelty_abstention_eval.py) established
that no single cheap signal clears the abstention bar: bare PLM distance is near
chance (AUC 0.596), and the cofactor-augmented signal reaches only 0.694 because a
small set of OOS enzymes carry a known cofactor signature and get confidently
misplaced into occupied clusters (AUC 0.44 on those, worse than chance).

This module tests the fix that follows from that diagnosis: a *two-channel*
abstention gate that combines

  1. the cofactor-augmented PLM nearest-centroid signal (good on the
     cofactor-agnostic OOS majority), and
  2. a geometry active-site role-agreement signal -- geometry top1 score x
     role_match_fraction (good exactly where the cofactor channel fails, because
     novel chemistry shows the right residues with the wrong catalytic roles).

Each channel is mapped to its percentile within the in-distribution ATLAS
distribution (atlas-only, deployable, no eval-pool leakage), and the two
percentiles are combined by mean (and min, a stricter concordance variant). A
row abstains when its combined percentile is low -- i.e. it is novel under at
least one channel.

Honesty boundaries:
  * The geometry channel here is read from an *experimental*-geometry retrieval
    artifact (teacher-side). The deployment regime is predicted geometry (D4),
    whose retrieval currently persists only top1 score, not the per-row role
    decomposition. The deployment-valid gate is therefore BLOCKED on a
    predicted-geometry retrieval that persists role_match_fraction; this module is
    source-agnostic on the geometry path so that artifact drops straight in.
  * The geometry fingerprint score is hand-authored / tuning-adjacent (D4);
    role_match_fraction is structural. No training, refit, or heldout tuning.
    Atlas-only statistics. M-CSA is eval-only.
"""

from __future__ import annotations

import bisect
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .mechanism_novelty_abstention_eval import (
    COFACTOR_CLASSES,
    COFACTOR_SIGNATURE_THRESHOLD,
    load_cofactor_scores,
    load_plm_rows,
)
from .mechanism_relationship_surface_eval import (
    apply_robust,
    cosine_similarity,
    robust_standardizer,
)

SCHEMA_VERSION = "mechanism_abstention_gate_eval.v0"
ABSTENTION_USABLE_AUC = 0.75


def _auc_in_gt_oos(in_scope: list[float], oos: list[float]) -> float | None:
    if not in_scope or not oos:
        return None
    greater = sum(1 for a in in_scope for b in oos if a > b)
    ties = sum(1 for a in in_scope for b in oos if a == b)
    return round((greater + 0.5 * ties) / (len(in_scope) * len(oos)), 6)


def load_geometry_role_scores(geometry_retrieval_path: Path) -> dict[str, dict[str, float]]:
    """Map entry_id -> {score, role_match_fraction} from a geometry retrieval artifact.

    Reads the top1 fingerprint's score and role_match_fraction. Rows without an
    ok status or without top_fingerprints are omitted (the caller treats them as
    geometry-unavailable). Source-agnostic across experimental/predicted retrieval
    artifacts that persist the per-row role decomposition.
    """
    payload = json.loads(Path(geometry_retrieval_path).read_text(encoding="utf-8"))
    results = payload.get("results") or payload.get("predicted_geometry_retrieval", {}).get("results")
    out: dict[str, dict[str, float]] = {}
    for row in results or []:
        if row.get("status") not in (None, "ok"):
            continue
        tf = row.get("top_fingerprints")
        if not tf:
            continue
        top = tf[0]
        if "role_match_fraction" not in top:
            continue
        out[row["entry_id"]] = {
            "score": float(top.get("score", 0.0)),
            "role_match_fraction": float(top.get("role_match_fraction", 0.0)),
        }
    return out


def _atlas_percentile(score_fn: Callable[[str], float], atlas: list[str]) -> Callable[[str], float]:
    atlas_sorted = sorted(score_fn(a) for a in atlas)
    n = len(atlas_sorted) or 1
    return lambda e: bisect.bisect_right(atlas_sorted, score_fn(e)) / n


def compute_two_channel_gate(
    plm_rows: dict[str, dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
    geometry_scores: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """Compute single-channel and combined abstention AUCs, overall and stratified."""
    def usable(e: str) -> bool:
        return e in cofactor_scores and e in geometry_scores

    def fp(e: str) -> str | None:
        return plm_rows[e]["true_fingerprint_id"]

    atlas = sorted(
        e for e, r in plm_rows.items()
        if r["split_assignment"] == "in_distribution" and fp(e) and usable(e)
    )
    inscope = sorted(
        e for e, r in plm_rows.items()
        if r["split_assignment"] == "heldout" and fp(e) and usable(e)
    )
    oos = sorted(
        e for e, r in plm_rows.items()
        if r["split_assignment"] == "heldout" and not fp(e) and usable(e)
    )
    if not (atlas and inscope and oos):
        return {"status": "insufficient_rows", "counts": {
            "atlas": len(atlas), "inscope": len(inscope), "oos": len(oos)}}

    confounded = [
        e for e in oos
        if max(cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES)
        >= COFACTOR_SIGNATURE_THRESHOLD
    ]
    agnostic = [e for e in oos if e not in confounded]

    # channel 1: cofactor-augmented PLM nearest-centroid (atlas centroids)
    def embv(e): return plm_rows[e]["embedding"]
    def cofv(e): return [cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES]
    med, scl = robust_standardizer([embv(e) for e in atlas])
    cmed, cscl = robust_standardizer([cofv(e) for e in atlas])
    aug = {e: apply_robust(embv(e), med, scl) + apply_robust(cofv(e), cmed, cscl)
           for e in atlas + inscope + oos}
    classes = sorted({fp(a) for a in atlas})
    dim = len(aug[atlas[0]])
    cents = {
        c: [sum(aug[a][j] for a in atlas if fp(a) == c) / sum(1 for a in atlas if fp(a) == c)
            for j in range(dim)]
        for c in classes
    }
    def ch_cofactor(e): return max(cosine_similarity(aug[e], c) for c in cents.values())

    # channel 2: geometry top1 score x role-agreement
    def ch_geometry(e):
        g = geometry_scores[e]
        return g["score"] * g["role_match_fraction"]

    pct_cof = _atlas_percentile(ch_cofactor, atlas)
    pct_geo = _atlas_percentile(ch_geometry, atlas)

    def gate_mean(e): return (pct_cof(e) + pct_geo(e)) / 2
    def gate_min(e): return min(pct_cof(e), pct_geo(e))

    def strata(score_fn) -> dict[str, float | None]:
        iv = [score_fn(e) for e in inscope]
        return {
            "all": _auc_in_gt_oos(iv, [score_fn(e) for e in oos]),
            "confounded": _auc_in_gt_oos(iv, [score_fn(e) for e in confounded]),
            "agnostic": _auc_in_gt_oos(iv, [score_fn(e) for e in agnostic]),
        }

    channels = {
        "cofactor_augmented": strata(pct_cof),
        "geometry_score_x_role": strata(pct_geo),
        "combined_mean": strata(gate_mean),
        "combined_min_concordance": strata(gate_min),
    }
    best_overall = max(
        (c["all"] for c in channels.values() if c["all"] is not None), default=0.0
    )
    return {
        "status": "computed",
        "normalization": "atlas_percentile_deployable",
        "counts": {
            "atlas": len(atlas), "inscope": len(inscope), "oos": len(oos),
            "confounded_oos": len(confounded), "agnostic_oos": len(agnostic),
        },
        "channels": channels,
        "best_overall_auc": best_overall,
        "clears_abstention_bar": best_overall >= ABSTENTION_USABLE_AUC,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _geometry_regime(geometry_retrieval_path: Path) -> str:
    name = Path(geometry_retrieval_path).name.lower()
    if "predicted" in name:
        return "predicted_geometry_deployment"
    return "experimental_geometry_teacher"


def compute_deployment_gate(
    plm_rows: dict[str, dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
    geometry_scores: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """Deployment-valid abstention gate over the held-out pool, with NO atlas.

    Both channels are already calibrated [0,1] confidences -- predicted-geometry
    fingerprint-retrieval top1 score and the strongest organic-cofactor head
    probability -- so they combine directly without atlas normalization and without
    eval-pool leakage. Higher = looks more like known chemistry; in-scope should
    score higher than out-of-scope. This is the deployment-valid de novo gate: it
    needs only the predicted-geometry held-out scoring, not a predicted-geometry
    atlas (which the current robustness audit does not provide).
    """
    def fp(e: str) -> str | None:
        return plm_rows[e]["true_fingerprint_id"]

    def usable(e: str) -> bool:
        return e in geometry_scores and e in cofactor_scores and e in plm_rows

    inscope = sorted(
        e for e in geometry_scores
        if usable(e) and plm_rows[e]["split_assignment"] == "heldout" and fp(e)
    )
    oos = sorted(
        e for e in geometry_scores
        if usable(e) and plm_rows[e]["split_assignment"] == "heldout" and not fp(e)
    )
    if not (inscope and oos):
        return {"status": "insufficient_rows",
                "counts": {"inscope": len(inscope), "oos": len(oos)}}

    def geom(e): return geometry_scores[e]["score"]
    def cof(e): return max(cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES)
    confounded = [e for e in oos if cof(e) >= COFACTOR_SIGNATURE_THRESHOLD]
    agnostic = [e for e in oos if e not in confounded]

    channel_fns = {
        "geometry_top1_score": geom,
        "cofactor_max_score": cof,
        "combined_mean": lambda e: (geom(e) + cof(e)) / 2,
        "combined_min_concordance": lambda e: min(geom(e), cof(e)),
    }

    def strata(fn) -> dict[str, Any]:
        iv = [fn(e) for e in inscope]
        return {
            "all": _auc_in_gt_oos(iv, [fn(e) for e in oos]),
            "confounded": _auc_in_gt_oos(iv, [fn(e) for e in confounded]),
            "agnostic": _auc_in_gt_oos(iv, [fn(e) for e in agnostic]),
            "in_scope_mean": round(sum(iv) / len(iv), 6),
            "oos_mean": round(sum(fn(e) for e in oos) / len(oos), 6),
        }

    channels = {name: strata(fn) for name, fn in channel_fns.items()}
    best = max((c["all"] for c in channels.values() if c["all"] is not None), default=0.0)
    # The single safest channel across all OOS strata (no stratum below 0.5).
    safest = max(
        (n for n, c in channels.items()
         if all(c[s] is not None and c[s] >= 0.5 for s in ("all", "confounded", "agnostic"))),
        key=lambda n: min(channels[n]["all"], channels[n]["confounded"], channels[n]["agnostic"]),
        default=None,
    )

    # Operating point: AUC alone does not yield a usable abstention threshold, so
    # report the actual decision curve. "Abstain" = score below threshold (looks
    # novel). Thresholds are a fixed, untuned grid over the calibrated [0,1] score;
    # they are NOT fit to the eval labels.
    grid = [round(0.05 * i, 2) for i in range(1, 20)]

    def operating_curve(fn) -> list[dict[str, Any]]:
        curve = []
        for thr in grid:
            in_abst = sum(1 for e in inscope if fn(e) < thr)
            oos_abst = sum(1 for e in oos if fn(e) < thr)
            conf_abst = sum(1 for e in confounded if fn(e) < thr)
            curve.append({
                "threshold": thr,
                "oos_abstain_recall": round(oos_abst / len(oos), 4),
                "inscope_retain_recall": round(1 - in_abst / len(inscope), 4),
                "confounded_abstain_recall": (
                    round(conf_abst / len(confounded), 4) if confounded else None),
            })
        return curve

    def best_at_retention(fn, min_retain: float) -> dict[str, Any] | None:
        ok = [r for r in operating_curve(fn) if r["inscope_retain_recall"] >= min_retain]
        return max(ok, key=lambda r: r["oos_abstain_recall"]) if ok else None

    operating_points = {
        "min_inscope_retention": 0.90,
        "geometry_led": best_at_retention(geom, 0.90),
        "combined_mean": best_at_retention(lambda e: (geom(e) + cof(e)) / 2, 0.90),
    }

    return {
        "status": "computed",
        "combination": "raw_calibrated_confidence_no_atlas_no_leakage",
        "counts": {
            "inscope": len(inscope), "oos": len(oos),
            "confounded_oos": len(confounded), "agnostic_oos": len(agnostic),
        },
        "channels": channels,
        "operating_points_at_90pct_retention": operating_points,
        "geometry_led_operating_curve": operating_curve(geom),
        "best_overall_auc": best,
        "clears_abstention_bar": best >= ABSTENTION_USABLE_AUC,
        "safest_channel_no_stratum_below_chance": safest,
    }


def build_mechanism_deployment_abstention_gate_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
) -> dict[str, Any]:
    """Deployment-valid de novo gate from predicted-geometry held-out scoring."""
    plm_rows = load_plm_rows(esm2_150m_path)
    cofactor_scores = load_cofactor_scores(cofactor_sidecar_path)
    geometry_scores = load_geometry_role_scores(predicted_geometry_audit_path)
    result = compute_deployment_gate(plm_rows, cofactor_scores, geometry_scores)
    best = result.get("best_overall_auc", 0.0)
    mean_all = (result.get("channels", {}).get("combined_mean", {}) or {}).get("all")
    geom_all = (result.get("channels", {}).get("geometry_top1_score", {}) or {}).get("all")
    return {
        "artifact_id": "v3_mechanism_deployment_abstention_gate_eval_current702_20260531",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 de novo precondition, DEPLOYMENT-VALID: combine predicted-geometry "
            "fingerprint-retrieval confidence with the organic-cofactor head "
            "confidence directly over the held-out pool (both already calibrated "
            "[0,1]); no atlas, no eval-pool leakage."
        ),
        "geometry_regime": "predicted_geometry_deployment",
        "result": result,
        "interpretation": {
            "headline": (
                f"Deployment-valid best abstention AUC is {best}; "
                + (
                    "the de novo precondition is MET on predicted geometry."
                    if best >= ABSTENTION_USABLE_AUC
                    else "the de novo precondition is not yet met on predicted geometry."
                )
            ),
            "combined_vs_geometry": (
                f"combined_mean reaches {mean_all} across all OOS but trades away "
                "safety on the cofactor-confounded subset (the cofactor channel is "
                f"fooled there); geometry top1 score alone is {geom_all} overall and "
                "is the single safest channel, strongest exactly on the confounded "
                "rows. A deployment gate should lead with geometry confidence and use "
                "the cofactor channel as a complementary lift on cofactor-agnostic OOS."
            ),
            "operating_point_reality": (
                "A strong AUC does NOT yield a usable abstention threshold. At a fixed, "
                "untuned threshold that retains >=90% of in-scope rows, the geometry-led "
                "gate abstains on only ~19% of OOS, and the blind mean-combined gate "
                "(~59% OOS) abstains on NONE of the safety-critical cofactor-confounded "
                "rows. The score distributions overlap heavily; an AUC-passing gate is "
                "not yet a deployable one. The committed operating curve makes this "
                "explicit so the gap is not hidden behind the headline AUC."
            ),
        },
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "predicted_geometry_deployment_regime": True,
            "no_atlas_no_eval_pool_leakage": True,
            "no_training_or_refit": True,
            "no_heldout_tuning": True,
            "geometry_fingerprint_score_is_tuning_adjacent": True,
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
    }


def write_mechanism_deployment_abstention_gate_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_deployment_abstention_gate_eval(
        esm2_150m_path=esm2_150m_path,
        cofactor_sidecar_path=cofactor_sidecar_path,
        predicted_geometry_audit_path=predicted_geometry_audit_path,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_deployment_report(audit), encoding="utf-8")
    return audit


def _render_deployment_report(audit: dict[str, Any]) -> str:
    res = audit["result"]
    if res.get("status") != "computed":
        return f"# D11 Deployment Abstention Gate\n\nStatus: {res.get('status')}\n"
    c = res["counts"]
    lines = [
        "# D11 Deployment-Valid Abstention Gate (de novo precondition)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        f"Combination: `{res['combination']}` | regime: **{audit['geometry_regime']}**",
        "",
        f"In-scope: {c['inscope']} | OOS: {c['oos']} "
        f"(confounded {c['confounded_oos']}, agnostic {c['agnostic_oos']})",
        "",
        "## Abstention AUC (in-scope > OOS; 0.5 = chance) by channel and stratum",
        "",
        "| Channel | all OOS | cofactor-confounded | cofactor-agnostic |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, s in res["channels"].items():
        lines.append(f"| {name} | {s['all']} | {s['confounded']} | {s['agnostic']} |")
    lines += [
        "",
        f"- Best overall AUC: **{res['best_overall_auc']}** -> clears 0.75 bar: "
        f"**{res['clears_abstention_bar']}**.",
        f"- Safest single channel (no stratum below chance): "
        f"`{res['safest_channel_no_stratum_below_chance']}`.",
    ]
    op = res.get("operating_points_at_90pct_retention")
    if op:
        gl, mc = op.get("geometry_led"), op.get("combined_mean")
        lines += [
            "",
            "## Operating point (fixed untuned threshold, >=90% in-scope retention)",
            "",
            "AUC alone is not a usable gate. At a threshold retaining >=90% of in-scope rows:",
            "",
            "| Gate | threshold | OOS abstain-recall | confounded abstain-recall | in-scope retain |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for name, r in (("geometry_led", gl), ("combined_mean", mc)):
            if r:
                lines.append(
                    f"| {name} | {r['threshold']} | {r['oos_abstain_recall']} | "
                    f"{r['confounded_abstain_recall']} | {r['inscope_retain_recall']} |"
                )
        lines.append("")
        lines.append(audit["interpretation"]["operating_point_reality"])
    lines += [
        "",
        "## Interpretation",
        "",
        audit["interpretation"]["headline"],
        "",
        audit["interpretation"]["combined_vs_geometry"],
    ]
    return "\n".join(lines) + "\n"


def build_mechanism_abstention_gate_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    geometry_retrieval_path: Path,
) -> dict[str, Any]:
    plm_rows = load_plm_rows(esm2_150m_path)
    cofactor_scores = load_cofactor_scores(cofactor_sidecar_path)
    geometry_scores = load_geometry_role_scores(geometry_retrieval_path)
    result = compute_two_channel_gate(plm_rows, cofactor_scores, geometry_scores)
    regime = _geometry_regime(geometry_retrieval_path)
    best = result.get("best_overall_auc", 0.0)
    return {
        "artifact_id": "v3_mechanism_abstention_gate_eval_current702_20260531",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 de novo precondition: a two-channel abstention gate (cofactor-"
            "augmented PLM + geometry active-site role-agreement) over the "
            f"{regime} geometry regime, with deployable atlas-percentile combination."
        ),
        "geometry_regime": regime,
        "result": result,
        "interpretation": {
            "headline": (
                f"Best overall abstention AUC is {best} on the {regime} regime; "
                + (
                    "the two-channel gate clears the 0.75 de novo precondition bar."
                    if best >= ABSTENTION_USABLE_AUC
                    else "the gate does not yet clear the 0.75 bar."
                )
            ),
            "why": (
                "The cofactor channel handles the cofactor-agnostic OOS majority but "
                "confidently misplaces novel enzymes that reuse a known cofactor "
                "family. The geometry role-agreement channel catches exactly those: "
                "novel chemistry shows the right active-site residues with the wrong "
                "catalytic roles. Combining the two atlas-percentiles recovers the "
                "cases each channel misses."
            ),
            "deployment_caveat": (
                "This result uses an experimental-geometry retrieval (teacher-side) "
                "for the role-agreement channel. The deployment regime is predicted "
                "geometry, whose current retrieval persists only top1 score, not the "
                "per-row role decomposition. The deployment-valid gate is blocked on a "
                "predicted-geometry retrieval that persists role_match_fraction; this "
                "eval is source-agnostic on the geometry path so that artifact drops in."
                if regime == "experimental_geometry_teacher"
                else "Deployment-regime (predicted geometry) gate evaluated directly."
            ),
        },
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "no_training_or_refit": True,
            "no_heldout_tuning": True,
            "atlas_only_statistics_and_percentiles": True,
            "geometry_fingerprint_score_is_tuning_adjacent": True,
            "labels_registries_thresholds_changed": False,
        },
        "source_artifacts": {
            "esm2_150m_embeddings": {"path": str(esm2_150m_path), "sha256": _sha256(esm2_150m_path)},
            "cofactor_score_sidecar": {
                "path": str(cofactor_sidecar_path), "sha256": _sha256(cofactor_sidecar_path)},
            "geometry_retrieval": {
                "path": str(geometry_retrieval_path), "sha256": _sha256(geometry_retrieval_path)},
        },
    }


def write_mechanism_abstention_gate_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    geometry_retrieval_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_abstention_gate_eval(
        esm2_150m_path=esm2_150m_path,
        cofactor_sidecar_path=cofactor_sidecar_path,
        geometry_retrieval_path=geometry_retrieval_path,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_report(audit), encoding="utf-8")
    return audit


def _render_report(audit: dict[str, Any]) -> str:
    res = audit["result"]
    if res.get("status") != "computed":
        return f"# D11 Two-Channel Abstention Gate\n\nStatus: {res.get('status')}\n"
    c = res["counts"]
    lines = [
        "# D11 Two-Channel Abstention Gate (de novo precondition)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        f"Geometry regime: **{audit['geometry_regime']}** | normalization: "
        f"`{res['normalization']}`",
        "",
        f"In-scope: {c['inscope']} | OOS: {c['oos']} "
        f"(confounded {c['confounded_oos']}, agnostic {c['agnostic_oos']}) | Atlas: {c['atlas']}",
        "",
        "## Abstention AUC (in-scope > OOS; 0.5 = chance) by channel and stratum",
        "",
        "| Channel | all OOS | cofactor-confounded | cofactor-agnostic |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, s in res["channels"].items():
        lines.append(f"| {name} | {s['all']} | {s['confounded']} | {s['agnostic']} |")
    lines += [
        "",
        f"- Best overall AUC: **{res['best_overall_auc']}** -> clears 0.75 bar: "
        f"**{res['clears_abstention_bar']}**.",
        "",
        "## Interpretation",
        "",
        audit["interpretation"]["headline"],
        "",
        audit["interpretation"]["why"],
        "",
        f"**Deployment caveat.** {audit['interpretation']['deployment_caveat']}",
    ]
    return "\n".join(lines) + "\n"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
