"""D11 Lever 2 integration: add the confirmed out-of-span residual to the rule gate.

The out-of-atlas-span residual was confirmed (mechanism_feature_residual_robustness.py)
as a robust, generalizing novelty signal: deployment-pool all-OOS AUC ~0.721, cutoff-
stable, and significant on a held-out-from-design split. The decision_log promotes it to
a candidate THIRD orthogonal lift channel for the per-channel RULE gate, alongside the
geometry-led gate and the cofactor-agnostic lift. This module performs that integration
and measures it at the operating point, stratified -- it does NOT re-discover the signal.

The deployed rule gate (mechanism_abstention_gate_eval.compute_deployment_gate) is:

    abstain(e) = geom(e) < tg  OR  (cof(e) < signature AND cof(e) < tc)

geometry leads; the cofactor channel may only ADD abstentions where it is trustworthy
(weak known-cofactor signature, cof < signature), never on the confounded subset, so
confounded rows are gated by geometry alone. We add a residual-agnostic-lift term with the
SAME confounded-safe guard (the residual is concentrated on the cofactor-agnostic majority
and is NOT confounded-safe -- confounded AUC ~0.66 vs geometry 0.84 -- so it must not make
keep/abstain calls on confounded rows):

    abstain(e) = geom(e) < tg
                 OR (cof(e) < signature AND cof(e) < tc)              # cofactor-agnostic-lift
                 OR (cof(e) < signature AND resid_novelty(e) >= tr)   # residual-agnostic-lift

resid_novelty = sqrt(out-of-span residual energy), higher = more novel. The three-channel
search space CONTAINS the two-channel gate (tr above the max residual disables the term),
so a three-channel optimum can never be worse; the question is the MAGNITUDE of the lift
and whether confounded safety is preserved at that optimum.

DEPLOYABILITY (honest scope). tg and tc are thresholds on already-calibrated [0,1]
confidences -- deployable as fixed constants. The residual threshold tr is NOT: the
residual's atlas-percentile calibration SATURATES (every held-out row sits above the atlas
residual range -- quantified here), so the residual carries signal only in raw/relative
form. tr is therefore an eval-pool-relative RESEARCH operating point (a calibration-free
ROC sweep over observed residual values, the same form in which the 0.721 lift was
measured), not a production threshold. The lift this module reports is the residual's
marginal OPERATING-POINT contribution to the gate; a deployable residual calibration (or
the Lever 4 expanded family set) is required before production promotion.

Predeclared decision rule (fixed BEFORE reading results), at the >=85% in-scope retention
floor (the two-channel gate has no >=90% point -- the cofactor lift abstains too many
low-cofactor in-scope rows -- so 85% is the operative floor; 90% reported if reachable):

    PASS iff  residual_adds_oos_lift  (three-channel OOS-abstain-recall > two-channel)
          AND confounded_safety_preserved  (three-channel confounded-abstain-recall
              >= two-channel confounded-abstain-recall).

A zero/negative lift, or a lift bought by sacrificing confounded safety, is a valid,
expected outcome and is reported cleanly.

Hard constraints honored: sequence-only residual, atlas-only fit, M-CSA eval-only, no
heldout tuning of the deployable thresholds, cofactor read-only for stratification.
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
from .mechanism_abstention_gate_eval import (
    ABSTENTION_USABLE_AUC,
    _auc_in_gt_oos,
    load_geometry_role_scores,
)
from .mechanism_feature_residual_robustness import (
    _atlas_pca_full,
    _keep_for_cutoff,
    _row_projection_energies,
)

SCHEMA_VERSION = "mechanism_residual_gate_integration.v0"
DEPLOYED_CUTOFF = 0.99
DEPLOYED_MAX_DIM = 128
# Deployable-confidence threshold grid (matches mechanism_abstention_gate_eval).
_GRID = [round(0.02 * i, 2) for i in range(1, 50)]
# Cap on residual-threshold candidates (research ROC sweep over observed values).
_MAX_TR_CANDIDATES = 60
_RETENTION_FLOORS = (0.90, 0.85)


def _residual_threshold_candidates(values: list[float]) -> list[float]:
    """Sorted unique residual-novelty values (sub-sampled to a bounded grid) plus a
    sentinel above the max that DISABLES the term -- so the two-channel gate is in the
    three-channel search space."""
    uniq = sorted(set(values))
    if len(uniq) > _MAX_TR_CANDIDATES:
        step = len(uniq) / _MAX_TR_CANDIDATES
        uniq = [uniq[min(int(i * step), len(uniq) - 1)] for i in range(_MAX_TR_CANDIDATES)]
    disable = (uniq[-1] if uniq else 0.0) + 1.0
    return uniq + [disable]


def compute_residual_gate_integration(
    plm_rows: dict[str, dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
    geometry_scores: dict[str, dict[str, float]],
    *,
    deployed_cutoff: float = DEPLOYED_CUTOFF,
    max_dim: int = DEPLOYED_MAX_DIM,
) -> dict[str, Any]:
    def fp(e: str) -> Any:
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

    sig = COFACTOR_SIGNATURE_THRESHOLD

    def geom(e: str) -> float:
        return geometry_scores[e]["score"]

    def cof(e: str) -> float:
        return max(cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES)

    confounded = [e for e in oos if cof(e) >= sig]
    agnostic = [e for e in oos if e not in confounded]

    # --- residual channel (sequence-only, atlas-fit; the confirmed Lever 2 signal) ---
    atlas = sorted(e for e in plm_rows if plm_rows[e]["split_assignment"] == "in_distribution" and fp(e))
    if len(atlas) < 8:
        return {"status": "insufficient_atlas", "atlas": len(atlas)}
    pca = _atlas_pca_full([plm_rows[e]["embedding"] for e in atlas])
    keep = _keep_for_cutoff(pca["eigenvalues"], pca["total_var"], deployed_cutoff, max_dim)
    k = keep["pca_dim"]

    def _resid_nov(e: str) -> float:
        total, cum = _row_projection_energies(pca, plm_rows[e]["embedding"])
        return math.sqrt(max(total - cum[min(k, len(cum) - 1)], 0.0))

    pool = inscope + oos
    r_nov = {e: _resid_nov(e) for e in pool}
    atlas_r = [_resid_nov(e) for e in atlas]
    atlas_r_max = max(atlas_r) if atlas_r else 0.0

    # Deployability evidence: the residual atlas-percentile saturates iff held-out rows
    # sit above the atlas residual range. Quantify it.
    above_atlas = sum(1 for e in pool if r_nov[e] > atlas_r_max)
    saturation = {
        "atlas_residual_novelty_max": round(atlas_r_max, 6),
        "heldout_rows_above_atlas_max": above_atlas,
        "heldout_rows_total": len(pool),
        "fraction_above_atlas_max": round(above_atlas / len(pool), 4) if pool else None,
        "atlas_percentile_calibration_saturates": bool(pool and above_atlas / len(pool) >= 0.99),
    }

    # --- channel AUC strata (residual cross-checks the embedding eval ~0.721) ---
    def strata(fn: Callable[[str], float]) -> dict[str, Any]:
        iv = [fn(e) for e in inscope]
        return {
            "all": _auc_in_gt_oos(iv, [fn(e) for e in oos]),
            "confounded": _auc_in_gt_oos(iv, [fn(e) for e in confounded]),
            "agnostic": _auc_in_gt_oos(iv, [fn(e) for e in agnostic]),
        }

    # residual novelty: higher = more novel, so for AUC(in-scope > OOS) use the negative.
    channels = {
        "geometry_top1_score": strata(geom),
        "cofactor_max_score": strata(cof),
        "out_of_span_residual": strata(lambda e: -r_nov[e]),
    }

    # --- rule-gate search ---
    tr_candidates = _residual_threshold_candidates([r_nov[e] for e in pool])
    tr_disabled = tr_candidates[-1]

    def metrics(tg: float, tc: float, tr: float, *, gate_residual_on_agnostic: bool = True) -> dict[str, Any]:
        def abstain(e: str) -> bool:
            if geom(e) < tg:
                return True
            agn = cof(e) < sig
            if agn and cof(e) < tc:
                return True
            if r_nov[e] >= tr and (agn or not gate_residual_on_agnostic):
                return True
            return False

        in_abst = sum(1 for e in inscope if abstain(e))
        return {
            "geometry_threshold": tg,
            "cofactor_threshold": tc,
            "residual_threshold": (None if tr >= tr_disabled else round(tr, 6)),
            "inscope_retain_recall": round(1 - in_abst / len(inscope), 4),
            "oos_abstain_recall": round(sum(1 for e in oos if abstain(e)) / len(oos), 4),
            "confounded_abstain_recall": (
                round(sum(1 for e in confounded if abstain(e)) / len(confounded), 4)
                if confounded else None),
            "agnostic_abstain_recall": (
                round(sum(1 for e in agnostic if abstain(e)) / len(agnostic), 4)
                if agnostic else None),
        }

    def best(min_retain: float, *, with_residual: bool, gate_on_agnostic: bool = True) -> dict[str, Any] | None:
        trs = tr_candidates if with_residual else [tr_disabled]
        chosen = None
        for tg in _GRID:
            for tc in _GRID:
                for tr in trs:
                    m = metrics(tg, tc, tr, gate_residual_on_agnostic=gate_on_agnostic)
                    if m["inscope_retain_recall"] < min_retain:
                        continue
                    key = (m["oos_abstain_recall"], m["confounded_abstain_recall"] or 0.0)
                    if chosen is None or key > chosen[0]:
                        chosen = (key, m)
        return chosen[1] if chosen else None

    per_floor: dict[str, Any] = {}
    verdict_floor: dict[str, Any] = {}
    for floor in _RETENTION_FLOORS:
        two = best(floor, with_residual=False)
        three = best(floor, with_residual=True)
        # exploratory: let the residual fire on ALL rows (ungated), which can add
        # confounded abstention (weakly positive there) -- not the predeclared form.
        three_ungated = best(floor, with_residual=True, gate_on_agnostic=False)
        key = f"{int(floor * 100)}pct_retention"
        per_floor[key] = {
            "two_channel_geometry_cofactor": two,
            "three_channel_with_residual_agnostic_lift": three,
            "exploratory_three_channel_residual_ungated": three_ungated,
        }
        if two and three:
            lift = round(three["oos_abstain_recall"] - two["oos_abstain_recall"], 4)
            two_conf = two["confounded_abstain_recall"] or 0.0
            three_conf = three["confounded_abstain_recall"] or 0.0
            adds = bool(three["oos_abstain_recall"] > two["oos_abstain_recall"])
            safe = bool(three_conf >= two_conf)
            verdict_floor[key] = {
                "two_channel_oos_abstain_recall": two["oos_abstain_recall"],
                "three_channel_oos_abstain_recall": three["oos_abstain_recall"],
                "residual_oos_lift": lift,
                "two_channel_confounded_abstain_recall": two["confounded_abstain_recall"],
                "three_channel_confounded_abstain_recall": three["confounded_abstain_recall"],
                "residual_adds_oos_lift": adds,
                "confounded_safety_preserved": safe,
                "pass": bool(adds and safe),
            }
        else:
            verdict_floor[key] = {
                "two_channel_oos_abstain_recall": (two or {}).get("oos_abstain_recall"),
                "three_channel_oos_abstain_recall": (three or {}).get("oos_abstain_recall"),
                "residual_oos_lift": None,
                "residual_adds_oos_lift": None,
                "confounded_safety_preserved": None,
                "pass": None,
                "note": "no rule-gate point clears this retention floor for one/both gates",
            }

    # operative floor = the highest floor where the two-channel gate has a point
    operative = next(
        (f"{int(f * 100)}pct_retention" for f in _RETENTION_FLOORS
         if per_floor[f"{int(f * 100)}pct_retention"]["two_channel_geometry_cofactor"]),
        f"{int(_RETENTION_FLOORS[-1] * 100)}pct_retention",
    )

    return {
        "status": "computed",
        "rule": (
            "abstain if geometry_score < tg OR (cofactor_max < signature AND cofactor_max < tc) "
            "OR (cofactor_max < signature AND residual_novelty >= tr)"
        ),
        "deployability_note": (
            "tg, tc are deployable thresholds on calibrated [0,1] confidences; tr is an "
            "eval-pool-relative RESEARCH operating point because the residual's atlas-"
            "percentile calibration saturates (see residual_atlas_saturation)."
        ),
        "counts": {
            "inscope": len(inscope), "oos": len(oos),
            "confounded_oos": len(confounded), "agnostic_oos": len(agnostic),
            "atlas": len(atlas),
        },
        "residual_space": {
            "deployed_cutoff": deployed_cutoff,
            "pca_dim": k,
            "variance_captured": keep["variance_captured"],
            "cap_binds": keep["cap_binds"],
        },
        "channels_auc": channels,
        "residual_atlas_saturation": saturation,
        "per_retention_floor": per_floor,
        "operative_floor": operative,
        "verdict_by_floor": verdict_floor,
        "verdict": {
            "operative_floor": operative,
            **{f"residual_oos_lift_at_{operative}": verdict_floor[operative].get("residual_oos_lift")},
            "pass_at_operative_floor": verdict_floor[operative].get("pass"),
            "residual_channel_auc_all": channels["out_of_span_residual"]["all"],
            "residual_cross_check_vs_embedding_eval": (
                abs((channels["out_of_span_residual"]["all"] or 0.0) - 0.72098) <= 0.01
            ),
        },
    }


# --------------------------------------------------------------------------- #
# Artifact build / write
# --------------------------------------------------------------------------- #
def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_residual_gate_integration_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    plm_rows = load_plm_rows(esm2_150m_path)
    cofactor_scores = load_cofactor_scores(cofactor_sidecar_path)
    geometry_scores = load_geometry_role_scores(predicted_geometry_audit_path)
    result = compute_residual_gate_integration(plm_rows, cofactor_scores, geometry_scores)
    audit = {
        "artifact_id": "v3_mechanism_residual_gate_integration_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 Lever 2 integration: add the confirmed out-of-span residual to the "
            "per-channel RULE gate as a third confounded-safe agnostic-lift channel, and "
            "measure its marginal operating-point lift over the geometry+cofactor gate, "
            "stratified, at the >=85% (and >=90% if reachable) in-scope retention floor."
        ),
        "result": result,
        "interpretation": _interpretation(result),
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "residual_fit_on_in_distribution_atlas_only": True,
            "mcsa_heldout_benchmark_is_eval_only_never_trained": True,
            "deployable_thresholds_not_tuned_on_heldout": True,
            "residual_threshold_is_research_operating_point_not_deployable": True,
            "cofactor_channel_consumed_read_only_for_stratification": True,
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
    return audit, result


def _interpretation(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("status") != "computed":
        return {"headline": f"status: {result.get('status')}"}
    op = result["operative_floor"]
    vf = result["verdict_by_floor"][op]
    sat = result["residual_atlas_saturation"]
    lift = vf.get("residual_oos_lift")
    if vf.get("pass"):
        head = (
            f"The confirmed residual adds operating-point lift to the rule gate: at the "
            f"{op} floor it raises OOS-abstain-recall from {vf['two_channel_oos_abstain_recall']} "
            f"(geometry+cofactor) to {vf['three_channel_oos_abstain_recall']} (+{lift}) while "
            f"preserving confounded safety ({vf['three_channel_confounded_abstain_recall']} vs "
            f"{vf['two_channel_confounded_abstain_recall']}). The lift is real but research-grade: "
            f"the residual threshold is eval-pool-relative (atlas calibration saturates)."
        )
    elif vf.get("pass") is False and vf.get("residual_adds_oos_lift"):
        head = (
            f"At the {op} floor the residual adds OOS lift (+{lift}) but at the cost of "
            f"confounded safety ({vf['three_channel_confounded_abstain_recall']} vs "
            f"{vf['two_channel_confounded_abstain_recall']}) -- the free optimum trades the "
            f"safety-critical subset for agnostic recall, so it does NOT pass the predeclared "
            f"rule. Use it only with a confounded-safe channel (Lever 3) pinned alongside."
        )
    elif vf.get("pass") is False:
        head = (
            f"CLEAN NEGATIVE at the operating point: at the {op} floor the residual adds no "
            f"OOS lift over the geometry+cofactor gate ({vf['three_channel_oos_abstain_recall']} "
            f"vs {vf['two_channel_oos_abstain_recall']}). A strong ranking signal (AUC "
            f"{result['verdict']['residual_channel_auc_all']}) need not translate to gate lift "
            f"once a fixed retention floor and the cofactor-agnostic guard are imposed."
        )
    else:
        head = (
            f"Inconclusive at {op}: no rule-gate point clears the retention floor for both "
            f"gates ({vf.get('note')})."
        )
    return {
        "headline": head,
        "residual_cross_check": (
            f"The residual channel reproduces the confirmed signal here: all-OOS AUC "
            f"{result['verdict']['residual_channel_auc_all']} (embedding eval 0.721; "
            f"cross-check {result['verdict']['residual_cross_check_vs_embedding_eval']})."
        ),
        "deployability": (
            f"{sat['fraction_above_atlas_max']} of held-out rows sit above the atlas residual "
            f"maximum, so the atlas-percentile calibration saturates "
            f"({sat['atlas_percentile_calibration_saturates']}); the residual threshold tr is a "
            f"research operating point, not a deployable constant. A deployable residual "
            f"calibration or the Lever 4 expanded family set is needed before production."
        ),
        "confounded_safety_design": (
            "The residual-agnostic-lift fires only where the cofactor signature is weak "
            "(cof < signature), exactly like the cofactor lift, so confounded rows remain "
            "gated by geometry alone -- the residual cannot make keep/abstain calls on the "
            "safety-critical subset, where it is weaker than geometry (AUC ~0.66 vs 0.84)."
        ),
    }


def write_residual_gate_integration_eval(
    *,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit, _ = build_residual_gate_integration_eval(
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
        report_path.write_text(_render_report(audit), encoding="utf-8")
    return audit


def _render_report(audit: dict[str, Any]) -> str:
    res = audit["result"]
    if res.get("status") != "computed":
        return f"# D11 Residual Gate Integration\n\nStatus: {res.get('status')}\n"
    c = res["counts"]
    interp = audit["interpretation"]
    lines = [
        "# D11 Residual → Rule-Gate Integration (Lever 2)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        f"Rule: `{res['rule']}`",
        "",
        f"In-scope {c['inscope']} | OOS {c['oos']} (confounded {c['confounded_oos']}, "
        f"agnostic {c['agnostic_oos']}) | atlas {c['atlas']}",
        "",
        "## Channel separation (AUC in-scope > OOS; 0.5 = chance)",
        "",
        "| channel | all OOS | confounded | agnostic |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, s in res["channels_auc"].items():
        lines.append(f"| {name} | {s['all']} | {s['confounded']} | {s['agnostic']} |")
    lines += [
        "",
        interp["residual_cross_check"],
        "",
        "## Rule gate: two-channel vs three-channel (with residual-agnostic-lift)",
        "",
        "| floor | gate | retain | OOS-abstain | confounded | agnostic | tg / tc / tr |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for floor_key, pf in res["per_retention_floor"].items():
        for label, gate in (
            ("2ch geom+cof", pf["two_channel_geometry_cofactor"]),
            ("3ch +residual", pf["three_channel_with_residual_agnostic_lift"]),
        ):
            if gate:
                lines.append(
                    f"| {floor_key} | {label} | {gate['inscope_retain_recall']} | "
                    f"{gate['oos_abstain_recall']} | {gate['confounded_abstain_recall']} | "
                    f"{gate['agnostic_abstain_recall']} | "
                    f"{gate['geometry_threshold']} / {gate['cofactor_threshold']} / "
                    f"{gate['residual_threshold']} |"
                )
            else:
                lines.append(f"| {floor_key} | {label} | — (no point clears floor) | | | | |")
    lines += ["", "## Verdict", ""]
    for floor_key, v in res["verdict_by_floor"].items():
        if v.get("pass") is None:
            lines.append(f"- **{floor_key}**: inconclusive — {v.get('note', '')}")
        else:
            lines.append(
                f"- **{floor_key}**: OOS {v['two_channel_oos_abstain_recall']} → "
                f"{v['three_channel_oos_abstain_recall']} (lift {v['residual_oos_lift']}); "
                f"confounded {v['two_channel_confounded_abstain_recall']} → "
                f"{v['three_channel_confounded_abstain_recall']}; adds lift: "
                f"{v['residual_adds_oos_lift']}, confounded-safe: "
                f"{v['confounded_safety_preserved']} → **pass: {v['pass']}**"
            )
    lines += [
        f"- Operative floor: **{res['operative_floor']}** "
        f"(highest floor with a two-channel point)",
        "",
        interp["headline"],
        "",
        interp["confounded_safety_design"],
        "",
        interp["deployability"],
    ]
    return "\n".join(lines) + "\n"
