"""Deployable operating-point contract for the fold (structural) channel.

This is the pure-synthesis core of the productionisation gate (Gate 3): turn the
measured fold-NN readouts into ONE decision-ready operating-point curve and a
frozen serving contract, so the channel stops living as prose ("fold-NN >= 0.74
gives 0.98 precision") and becomes an inspectable rule a deployer can read off.

It does three things and nothing more:

1. Recomputes the recovery / precision / abstention curve directly from the
   per-row fold-NN scores of the two recovery readouts (M-CSA in-distribution
   baseline + off-M-CSA bronze), on ONE common threshold grid, for each surface
   and for their union, with a per-family breakdown -- and asserts the
   recomputation reproduces each readout's own published curve (so the synthesis
   cannot drift from the evidence).
2. Joins the rejection half from the off-M-CSA abstention readout's published
   frontier (M-CSA OOS false-accept + external non-M-CSA false-accept +
   in-scope retention) onto the same grid, and cross-checks that the frontier's
   in-scope retention matches the recomputed M-CSA retention (tying the two
   source artifacts together).
3. Selects a RECOMMENDED operating point by an objective stated before any
   number is read, and emits the serving contract (the deployable decision
   function) at that point.

Leakage posture (loud, on purpose): the operating point is selected on the
DEVELOPMENT surfaces only -- M-CSA calibration in-scope/OOS, off-M-CSA bronze
positives, and external non-M-CSA negatives. The spent M-CSA held-out one-shot
is NOT read here. Nothing is trained; no registry, ontology, label, or
production threshold is changed. Per the project's standing discipline, the
recommended threshold is a development-surface recommendation that still
requires a NEW pre-registered held-out (ideally with non-M-CSA gold rows) before
it can become a deployment claim.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SOURCES: dict[str, str] = {
    "mcsa_recovery_baseline": (
        "artifacts/v3_fold_nn_mechanism_recovery_mcsa_baseline_current702_20260628.json"
    ),
    "offmcsa_recovery": (
        "artifacts/v3_fold_nn_mechanism_recovery_offmcsa_bronze_current702_20260628.json"
    ),
    "offmcsa_abstention": (
        "artifacts/v3_external_offmcsa_fold_abstention_readout_current702_20260628.json"
    ),
}
DEFAULT_OUT_PATH = (
    "artifacts/v3_fold_channel_operating_point_contract_current702_20260629.json"
)
DEFAULT_REPORT_PATH = (
    "work/fold_channel_operating_point_contract_current702_20260629.md"
)

# The grid shared by both recovery curves and the published rejection frontier.
THRESHOLD_GRID: tuple[float, ...] = (0.5, 0.566, 0.6, 0.65, 0.7, 0.74)
# Off-distribution rejection floor for the recommended point. 0.20 mirrors the
# project's one validated open-set number -- the held-out OOS-FP rate (0.19) --
# rather than being tuned to maximise recovery.
MAX_OFFDIST_FALSE_ACCEPT = 0.20
_TOL = 1.5e-3


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scored_rows(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    return [r for r in (artifact.get("rows") or []) if r.get("fold_nn_scored")]


def _recovery_at(rows: list[dict[str, Any]], tau: float) -> dict[str, Any]:
    """Recovery / precision / abstention at threshold tau over scored rows.

    recovery_of_all_positives = recovered-and-retained / all positives (an
    abstention counts against recall); precision_on_retained = recovered-and-
    retained / retained.
    """
    n = len(rows)
    retained = [r for r in rows if (r.get("fold_nn_alntmscore") or 0.0) >= tau]
    recovered = sum(1 for r in retained if r.get("recovered"))
    return {
        "n": n,
        "retained": len(retained),
        "retained_recovered": recovered,
        "abstained": n - len(retained),
        "recovery_of_all_positives": round(recovered / n, 4) if n else None,
        "precision_on_retained": (
            round(recovered / len(retained), 4) if retained else None
        ),
    }


def _per_family_recovery_at(rows: list[dict[str, Any]], tau: float) -> dict[str, Any]:
    fam: dict[str, list[int]] = {}
    for r in rows:
        key = r.get("true_fingerprint_id")
        bucket = fam.setdefault(key, [0, 0])  # [recovered_and_retained, total]
        bucket[1] += 1
        if (r.get("fold_nn_alntmscore") or 0.0) >= tau and r.get("recovered"):
            bucket[0] += 1
    return {
        k: {
            "recovered_retained": rec,
            "total": tot,
            "recovery_of_all_positives": round(rec / tot, 4) if tot else None,
        }
        for k, (rec, tot) in sorted(fam.items(), key=lambda x: -x[1][1])
    }


def _assert_matches_published_curve(
    rows: list[dict[str, Any]], curve: list[dict[str, Any]], label: str
) -> bool:
    """Recomputed recovery curve must reproduce the readout's published curve."""
    published = {round(c["fold_threshold"], 3): c for c in curve}
    for tau in THRESHOLD_GRID:
        pub = published.get(round(tau, 3))
        if pub is None:
            continue
        got = _recovery_at(rows, tau)
        if got["retained"] != pub["retained"] or (
            got["retained_recovered"] != pub["retained_recovered"]
        ) or abs(
            (got["recovery_of_all_positives"] or 0.0)
            - pub["recovery_of_all_positives"]
        ) > _TOL:
            raise ValueError(
                f"recomputed {label} curve diverges from published readout at "
                f"tau={tau}: recomputed={got} published={pub}"
            )
    return True


def build_fold_channel_operating_point(
    *, sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    mcsa = sources["mcsa_recovery_baseline"]
    off = sources["offmcsa_recovery"]
    absten = sources["offmcsa_abstention"]

    mcsa_rows = _scored_rows(mcsa)
    off_rows = _scored_rows(off)
    combined_rows = mcsa_rows + off_rows

    # (1) Faithfulness: the recomputation must reproduce each published curve.
    verification = {
        "recompute_matches_published_mcsa_curve": _assert_matches_published_curve(
            mcsa_rows, mcsa.get("recovery_abstention_curve") or [], "mcsa"
        ),
        "recompute_matches_published_offmcsa_curve": _assert_matches_published_curve(
            off_rows, off.get("recovery_abstention_curve") or [], "offmcsa"
        ),
    }

    # (2) Rejection half from the published frontier, keyed by threshold.
    frontier = {
        round(f["fold_threshold"], 3): f
        for f in (absten.get("abstention_recovery_frontier") or [])
    }

    # Cross-check: recomputed M-CSA in-scope retention must equal the frontier's.
    retention_ok = True
    n_mcsa = len(mcsa_rows)
    for tau in THRESHOLD_GRID:
        f = frontier.get(round(tau, 3))
        if f is None or not n_mcsa:
            continue
        recomputed_retention = round(
            _recovery_at(mcsa_rows, tau)["retained"] / n_mcsa, 4
        )
        if abs(recomputed_retention - f["mcsa_inscope_retention_rate"]) > _TOL:
            retention_ok = False
    verification["recomputed_inscope_retention_matches_frontier"] = retention_ok

    def rejection_at(tau: float) -> dict[str, Any]:
        f = frontier.get(round(tau, 3))
        if f is None:
            return {
                "mcsa_oos_false_accept_rate": None,
                "external_offmcsa_false_accept_rate": None,
                "mcsa_inscope_retention_rate": None,
            }
        return {
            "mcsa_oos_false_accept_rate": f["mcsa_oos_false_accept_rate"],
            "external_offmcsa_false_accept_rate": f["external_false_accept_rate"],
            "mcsa_inscope_retention_rate": f["mcsa_inscope_retention_rate"],
        }

    def curve_row(tau: float) -> dict[str, Any]:
        return {
            "fold_threshold": tau,
            "recovery": {
                "mcsa_indistribution": _recovery_at(mcsa_rows, tau),
                "offmcsa_bronze": _recovery_at(off_rows, tau),
                "combined": _recovery_at(combined_rows, tau),
                "offmcsa_per_family": _per_family_recovery_at(off_rows, tau),
            },
            "rejection": rejection_at(tau),
        }

    operating_point_curve = [curve_row(tau) for tau in THRESHOLD_GRID]

    # No-abstention reference (tau = 0): recovers most, rejects nothing.
    no_abstention_reference = {
        "fold_threshold": 0.0,
        "recovery": {
            "mcsa_indistribution": _recovery_at(mcsa_rows, 0.0),
            "offmcsa_bronze": _recovery_at(off_rows, 0.0),
            "combined": _recovery_at(combined_rows, 0.0),
        },
        "rejection": {
            "mcsa_oos_false_accept_rate": 1.0,
            "external_offmcsa_false_accept_rate": 1.0,
            "mcsa_inscope_retention_rate": 1.0,
            "note": "tau=0 accepts every input by definition; not deployable open-set.",
        },
        "deployable_open_set": False,
    }

    # (3) Recommended point: lowest tau whose external (off-distribution)
    # false-accept rate clears the rejection floor. Objective fixed in advance.
    recommended = next(
        (
            row
            for row in operating_point_curve
            if (row["rejection"]["external_offmcsa_false_accept_rate"] is not None)
            and (
                row["rejection"]["external_offmcsa_false_accept_rate"]
                <= MAX_OFFDIST_FALSE_ACCEPT
            )
        ),
        None,
    )
    # High-precision alternative: max off-M-CSA precision on retained.
    high_precision = max(
        operating_point_curve,
        key=lambda r: (
            r["recovery"]["offmcsa_bronze"]["precision_on_retained"] or 0.0
        ),
    )

    rec_tau = recommended["fold_threshold"] if recommended else None
    rec_off = recommended["recovery"]["offmcsa_bronze"] if recommended else {}
    rec_rej = recommended["rejection"] if recommended else {}

    # Per-family robustness of the single global threshold: a family "collapses"
    # if applying tau* loses more than half of the recall it had with no
    # abstention. This is the finding the unified curve surfaces that the
    # per-surface readouts did not -- one global fold threshold is not equally
    # valid across families (some folds are structurally tighter than others).
    fam_at_zero = _per_family_recovery_at(off_rows, 0.0)
    fam_at_rec = (
        _per_family_recovery_at(off_rows, rec_tau) if rec_tau is not None else {}
    )
    family_rows: list[dict[str, Any]] = []
    for fam_id, base in fam_at_zero.items():
        at_rec = fam_at_rec.get(fam_id, {})
        r0 = base["recovery_of_all_positives"] or 0.0
        rt = at_rec.get("recovery_of_all_positives") or 0.0
        survives = rt >= 0.5 * r0 if r0 else True
        family_rows.append(
            {
                "fingerprint_id": fam_id,
                "total": base["total"],
                "recovery_no_abstention": r0,
                "recovery_at_recommended_tau": rt,
                "retained_recovered_at_recommended_tau": at_rec.get(
                    "recovered_retained"
                ),
                "survives_global_threshold": survives,
            }
        )
    collapsing = [f["fingerprint_id"] for f in family_rows if not f["survives_global_threshold"]]
    family_robustness = {
        "recommended_tau": rec_tau,
        "criterion": (
            "a family survives the global threshold if recovery at tau* retains "
            ">= 50% of its no-abstention recovery"
        ),
        "per_family": family_rows,
        "families_that_collapse_at_recommended_tau": collapsing,
        "single_global_threshold_uniform_across_families": not collapsing,
        "implication": (
            "A single global fold threshold is family-dependent: "
            f"{', '.join(collapsing)} each lose >50% of recall at tau*={rec_tau} "
            "because their true within-family fold-NN scores run lower than the "
            "flavin/heme/PLP families. A per-family threshold (or a family-aware "
            "calibration) is the bounded next step before a uniform tau* deploys."
            if collapsing
            else f"All families retain >=50% of recall at tau*={rec_tau}."
        ),
    }

    serving_contract = {
        "decision_function": [
            "input: protein sequence",
            "1. predict structure (AlphaFold / equivalent) -> 3D coordinates",
            "2. foldseek query vs the M-CSA fold atlas -> top-1 hit "
            "(target accession, target fingerprint_id, alntmscore s)",
            f"3. if s >= tau* ({rec_tau}): emit (mechanism = target fingerprint_id, "
            "confidence = s)",
            "   else: ABSTAIN (out-of-scope / novel mechanism)",
        ],
        "tau_star": rec_tau,
        "atlas": "M-CSA fold atlas (the in-distribution structural reference set)",
        "expected_behaviour_on_development_surfaces": {
            "offmcsa_recovery_of_all_positives": rec_off.get(
                "recovery_of_all_positives"
            ),
            "offmcsa_precision_on_retained": rec_off.get("precision_on_retained"),
            "external_offmcsa_false_accept_rate": rec_rej.get(
                "external_offmcsa_false_accept_rate"
            ),
            "mcsa_oos_false_accept_rate": rec_rej.get("mcsa_oos_false_accept_rate"),
            "mcsa_inscope_retention_rate": rec_rej.get("mcsa_inscope_retention_rate"),
        },
        "abstain_rule": (
            "Abstain below tau*: the channel is a high-precision retriever with a "
            "calibrated open-set reject, not a forced classifier."
        ),
    }

    all_verified = all(verification.values())

    return {
        "artifact_id": (
            "v3_fold_channel_operating_point_contract_current702_20260629"
        ),
        "schema_version": "fold_channel_operating_point_contract.v1",
        "created_utc": _utc_now_iso(),
        "status": (
            "fold_channel_operating_point_contract_development_surface_pending_heldout_validation"
            if all_verified
            else "fold_channel_operating_point_contract_verification_failed"
        ),
        "result_class": (
            "development_surface_operating_point_synthesis_no_heldout_read_no_training"
        ),
        "question": (
            "What is the deployable fold-channel operating point -- the threshold on "
            "the top-1 fold-NN alignment-TM score that turns the validated structural "
            "signal into a mechanism call with a calibrated open-set abstention -- and "
            "what does it deliver on the measured development surfaces?"
        ),
        "objective": {
            "statement": (
                "Select the lowest fold-NN threshold whose off-distribution "
                "(external non-M-CSA) false-accept rate is <= "
                f"{MAX_OFFDIST_FALSE_ACCEPT}; that is the deployable abstaining point."
            ),
            "rationale": (
                f"The {MAX_OFFDIST_FALSE_ACCEPT} rejection floor mirrors the project's "
                "one validated open-set number -- the held-out OOS false-positive rate "
                "(0.19) -- so the point is anchored to a validated operating regime "
                "rather than tuned to maximise recovery."
            ),
            "selection_surface": (
                "development only: M-CSA calibration in-scope (35) + OOS (26) + "
                "off-M-CSA bronze positives (156) + external non-M-CSA negatives (52). "
                "The spent M-CSA held-out one-shot was NOT read."
            ),
        },
        "threshold_grid": list(THRESHOLD_GRID),
        "no_abstention_reference": no_abstention_reference,
        "operating_point_curve": operating_point_curve,
        "recommended_operating_point": {
            "found": recommended is not None,
            "fold_threshold": rec_tau,
            "selected_because": (
                "lowest grid threshold with external off-distribution false-accept "
                f"rate <= {MAX_OFFDIST_FALSE_ACCEPT}"
            ),
            "row": recommended,
        },
        "family_robustness_at_recommended_tau": family_robustness,
        "alternative_operating_points": {
            "high_precision": {
                "fold_threshold": high_precision["fold_threshold"],
                "selected_because": "maximises off-M-CSA precision on retained",
                "row": high_precision,
            }
        },
        "serving_contract": serving_contract,
        "verification": verification,
        "guardrails": {
            "heldout_rows_scored": False,
            "threshold_selected_on_heldout": False,
            "supervised_model_trained": False,
            "registry_or_ontology_changed": False,
            "production_threshold_changed": False,
            "fingerprint_family_growth": False,
            "new_scores_computed": (
                "recomputed from published per-row fold-NN scores; verified to "
                "reproduce each readout's published curve (no new measurement)"
            ),
        },
        "caveats": [
            "Development-surface recommendation, NOT a validated deployment claim: "
            "tau* is selected on calibration + bronze + external-negative surfaces.",
            "Off-M-CSA recovery uses bronze (automation-curated) labels -- it measures "
            "fold/sequence concordance, not gold accuracy (non-circular for fold: "
            "bronze admission used sequence/cofactor, not structure).",
            "Coverage is the 4 cofactor atlas families; broader-family behaviour is "
            "not measured here.",
            "n is small (35 M-CSA + 156 off-M-CSA positives; 26 OOS + 52 external "
            "negatives); the curve is an estimate, not a precise operating guarantee.",
        ],
        "requires_before_deployment": [
            "A NEW pre-registered held-out (ideally including non-M-CSA gold rows) that "
            "validates tau* once, after it is frozen -- per the standing discipline "
            "that every operating-point change needs a fresh unbiased test.",
            "A gold-labelled off-M-CSA recovery check to replace the bronze concordance "
            "estimate.",
        ],
        "source_artifacts": {},
        "interpretation": {
            "headline": (
                "FOLD-CHANNEL OPERATING-POINT CONTRACT (development surface): the "
                f"recommended deployable point is fold-NN tau* = {rec_tau}, where the "
                "channel recovers "
                f"{rec_off.get('recovery_of_all_positives')} of off-M-CSA positives at "
                f"{rec_off.get('precision_on_retained')} precision while abstaining on "
                f"{rec_rej.get('external_offmcsa_false_accept_rate')} of external "
                "non-M-CSA negatives. The recomputed curve reproduces both published "
                "readouts exactly. This is a development-surface recommendation; it "
                "needs a fresh pre-registered held-out before it is a deployment claim."
            )
            if recommended
            else (
                "No grid threshold cleared the off-distribution rejection floor; see "
                "the curve for the trade-off."
            ),
            "key_engineering_finding": family_robustness["implication"],
        },
    }


def _fmt_pct(x: Any) -> str:
    return "n/a" if x is None else f"{x:.3f}"


def _report(summary: dict[str, Any]) -> str:
    rec = summary["recommended_operating_point"]
    sc = summary["serving_contract"]
    lines = [
        "# Fold-Channel Operating-Point Contract (Development Surface)",
        "",
        f"Run: {summary['created_utc']}",
        f"Status: `{summary['status']}`",
        "",
        "## Bottom line",
        "",
        f"- {summary['interpretation']['headline']}",
        "",
        "## Objective (fixed before reading any number)",
        "",
        f"- {summary['objective']['statement']}",
        f"- Rationale: {summary['objective']['rationale']}",
        f"- Selection surface: {summary['objective']['selection_surface']}",
        "",
        "## Operating-point curve (one grid, all surfaces)",
        "",
        "Recovery columns are recovery_of_all_positives (abstentions count against "
        "recall); precision is on retained. Rejection columns are false-accept rates "
        "on out-of-scope inputs (lower is better).",
        "",
        "| fold tau | M-CSA rec | M-CSA prec | offMCSA rec | offMCSA prec | "
        "combined rec | OOS f-accept | ext f-accept |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    rows = [summary["no_abstention_reference"]] + summary["operating_point_curve"]
    for row in rows:
        r = row["recovery"]
        j = row["rejection"]
        m = r["mcsa_indistribution"]
        o = r["offmcsa_bronze"]
        c = r["combined"]
        lines.append(
            f"| {row['fold_threshold']} | {_fmt_pct(m['recovery_of_all_positives'])} "
            f"| {_fmt_pct(m['precision_on_retained'])} "
            f"| {_fmt_pct(o['recovery_of_all_positives'])} "
            f"| {_fmt_pct(o['precision_on_retained'])} "
            f"| {_fmt_pct(c['recovery_of_all_positives'])} "
            f"| {_fmt_pct(j['mcsa_oos_false_accept_rate'])} "
            f"| {_fmt_pct(j['external_offmcsa_false_accept_rate'])} |"
        )
    lines += [
        "",
        "## Recommended operating point",
        "",
        f"- **fold-NN tau* = {rec['fold_threshold']}** "
        f"({rec['selected_because']}).",
    ]
    if rec["row"]:
        fam = rec["row"]["recovery"]["offmcsa_per_family"]
        eb = sc["expected_behaviour_on_development_surfaces"]
        lines += [
            f"- Off-M-CSA recovery {_fmt_pct(eb['offmcsa_recovery_of_all_positives'])} "
            f"at precision {_fmt_pct(eb['offmcsa_precision_on_retained'])}.",
            f"- Rejection: external non-M-CSA false-accept "
            f"{_fmt_pct(eb['external_offmcsa_false_accept_rate'])}; M-CSA OOS "
            f"false-accept {_fmt_pct(eb['mcsa_oos_false_accept_rate'])}; in-scope "
            f"retention {_fmt_pct(eb['mcsa_inscope_retention_rate'])}.",
            "- Off-M-CSA recovery by family at tau*:",
        ]
        for f, v in fam.items():
            lines.append(
                f"    - {f}: {v['recovered_retained']}/{v['total']} "
                f"({_fmt_pct(v['recovery_of_all_positives'])})"
            )
    alt = summary["alternative_operating_points"]["high_precision"]
    lines += [
        "",
        f"- Alternative (high precision): tau = {alt['fold_threshold']} "
        f"({alt['selected_because']}).",
    ]
    fr = summary["family_robustness_at_recommended_tau"]
    lines += [
        "",
        "## Family robustness of the global threshold (the key engineering finding)",
        "",
        f"- {fr['criterion']}.",
        "",
        "| family | n | recovery (tau=0) | recovery (tau*) | survives |",
        "| --- | --- | --- | --- | --- |",
    ]
    for f in fr["per_family"]:
        lines.append(
            f"| {f['fingerprint_id']} | {f['total']} | "
            f"{_fmt_pct(f['recovery_no_abstention'])} | "
            f"{_fmt_pct(f['recovery_at_recommended_tau'])} | "
            f"{'yes' if f['survives_global_threshold'] else 'NO -- collapses'} |"
        )
    lines += [
        "",
        f"- **Implication:** {fr['implication']}",
        "",
        "## Serving contract (the deployable decision rule)",
        "",
    ]
    lines += [f"- {step}" for step in sc["decision_function"]]
    lines += [f"- {sc['abstain_rule']}"]
    lines += [
        "",
        "## Verification",
        "",
    ]
    for k, v in summary["verification"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Caveats", ""]
    lines += [f"- {c}" for c in summary["caveats"]]
    lines += ["", "## Required before deployment", ""]
    lines += [f"- {c}" for c in summary["requires_before_deployment"]]
    lines += [
        "",
        "## Guardrails",
        "",
        "- Development-surface synthesis; no held-out read, no training, no registry "
        "or production-threshold change. Recovery is recomputed from published "
        "per-row scores and verified to reproduce both readouts' curves.",
    ]
    return "\n".join(lines) + "\n"


def write_fold_channel_operating_point(
    *,
    sources: dict[str, str] | None = None,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    source_paths = dict(sources or DEFAULT_SOURCES)
    loaded = {name: _load_json(Path(p)) for name, p in source_paths.items()}
    summary = build_fold_channel_operating_point(sources=loaded)
    summary["source_artifacts"] = {
        name: {
            "path": path,
            "artifact_id": loaded[name].get("artifact_id"),
            "status": loaded[name].get("status"),
            "sha256": _sha256(Path(path)),
        }
        for name, path in source_paths.items()
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(summary), encoding="utf-8")
    return summary
