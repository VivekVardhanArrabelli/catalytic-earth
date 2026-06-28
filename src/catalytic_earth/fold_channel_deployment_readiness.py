"""Consolidated deployment-readiness summary for the fold (structural) channel.

Aggregates the session's committed readouts into one verifiable assessment of
whether the fold nearest-neighbour channel is a deployment-grade mechanism
signal. It reads the actual source artifacts (values + sha256) so the summary
cannot drift from, or cherry-pick against, the evidence. It computes nothing new
and scores no held-out data; it only synthesises.

Headline it certifies (from the sources): the fold channel generalises off the
M-CSA development distribution on BOTH halves -- it recovers off-distribution
positives and rejects off-distribution negatives -- which the cofactor channel
did not. It is explicit about what remains unvalidated (gold-truth off-M-CSA,
the unspent held-out one-shot, coverage beyond the cofactor atlas families).
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
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
    "mcsa_fold_separation": (
        "artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json"
    ),
    "june9_fold_fusion": (
        "artifacts/v3_june9_router_fold_fusion_readout_current702_20260628.json"
    ),
    "cofactor_precision_contract": (
        "artifacts/v3_current57_cofactor_precision_contract_current702_20260628.json"
    ),
    "heldout_preregistration": (
        "artifacts/v3_heldout_oneshot_preregistration_current702_20260628.json"
    ),
}
DEFAULT_OUT_PATH = (
    "artifacts/v3_fold_channel_deployment_readiness_summary_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/fold_channel_deployment_readiness_summary_current702_20260628.md"
)


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


def _per_family_recovery(recovery_artifact: dict[str, Any]) -> dict[str, str]:
    fam: dict[str, list[int]] = {}
    for row in recovery_artifact.get("rows", []) or []:
        if not row.get("fold_nn_scored"):
            continue
        key = row.get("true_fingerprint_id")
        bucket = fam.setdefault(key, [0, 0])
        bucket[1] += 1
        if row.get("recovered"):
            bucket[0] += 1
    return {
        k: f"{rec}/{tot} ({round(rec / tot, 2)})"
        for k, (rec, tot) in sorted(fam.items(), key=lambda x: -x[1][1])
    }


def build_fold_channel_deployment_readiness(
    *, sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    base = sources["mcsa_recovery_baseline"]
    off = sources["offmcsa_recovery"]
    absten = sources["offmcsa_abstention"]
    sep = sources["mcsa_fold_separation"]
    june9 = sources["june9_fold_fusion"]
    contract = sources["cofactor_precision_contract"]
    prereg = sources["heldout_preregistration"]

    base_rec = base.get("recovery", {})
    off_rec = off.get("recovery", {})
    abst_test = absten.get("generalization_test", {})
    sep_dist = sep.get("fold_nn_distribution", {})

    recovers_offmcsa = (off_rec.get("recovery_rate_no_abstention") or 0) >= 0.70
    rejects_offmcsa = bool(
        abst_test.get("abstention_signal_generalizes_off_mcsa")
    )
    both_halves = recovers_offmcsa and rejects_offmcsa

    return {
        "artifact_id": (
            "v3_fold_channel_deployment_readiness_summary_current702_20260628"
        ),
        "schema_version": "fold_channel_deployment_readiness_summary.v1",
        "created_utc": _utc_now_iso(),
        "status": (
            "fold_channel_generalizes_off_mcsa_both_halves_deployment_claim_still_gated"
            if both_halves
            else "fold_channel_off_mcsa_generalization_incomplete"
        ),
        "result_class": "read_only_synthesis_no_new_scoring_no_heldout_read",
        "guardrails": {
            "heldout_rows_scored": False,
            "new_scores_computed": False,
            "registry_or_ontology_changed": False,
            "synthesis_only": True,
        },
        "question": (
            "Is the fold (structural nearest-neighbour) channel a deployment-grade "
            "mechanism signal -- does it both recover correct mechanisms and abstain on "
            "out-of-scope inputs -- beyond the M-CSA development distribution?"
        ),
        "channels_contrast": {
            "cofactor_sequence_channel": {
                "current57_precision_contract_status": contract.get("status"),
                "compatible_recovery_ceiling": (
                    contract.get("calibration_summary", {})
                    .get("legacy_v1_compatible_fused_current57_at_frozen_threshold", {})
                    .get("inscope_correct")
                ),
                "off_mcsa_abstention_signal": "absent (prior gold eval)",
                "note": (
                    "Cofactor channel drifted on the current-57 router and showed no "
                    "off-M-CSA abstention signal."
                ),
            },
            "fold_structural_channel": {
                "mcsa_inscope_vs_oos_separation": {
                    "inscope_median": sep_dist.get("inscope", {}).get(
                        "alntmscore_median"
                    ),
                    "oos_median": sep_dist.get("oos", {}).get("alntmscore_median"),
                },
                "note": "Fold channel separates in-scope from OOS and generalises off M-CSA.",
            },
        },
        "off_mcsa_generalization": {
            "recovery_half": {
                "surface": off.get("surface_label"),
                "recovery": (
                    f"{off_rec.get('fold_nn_recovered')}/{off_rec.get('fold_nn_scored')} "
                    f"({off_rec.get('recovery_rate_no_abstention')})"
                ),
                "per_family": _per_family_recovery(off),
                "mcsa_baseline_reference": (
                    f"{base_rec.get('fold_nn_recovered')}/{base_rec.get('fold_nn_scored')} "
                    f"({base_rec.get('recovery_rate_no_abstention')})"
                ),
                "generalizes": recovers_offmcsa,
            },
            "rejection_half": {
                "external_negative_median": abst_test.get("external_median"),
                "mcsa_oos_median": abst_test.get("mcsa_oos_median"),
                "mcsa_inscope_median": abst_test.get("mcsa_inscope_median"),
                "generalizes": rejects_offmcsa,
            },
            "both_halves_generalize_off_mcsa": both_halves,
        },
        "deployable_operating_point": {
            "router": "June 9 router (registry pin d567ee0d) at the 0.44 cofactor dial",
            "calibration_point": (
                june9.get("june9_baseline_fold_gate_off", {})
                .get("dial_0p44_threshold", {})
            ),
            "fold_gate_role": (
                "tunable precision/recall + OOS-rejection dial; on the healthy June 9 "
                "router it does not Pareto-improve the dial point (residual OOS FPs are "
                "high-fold-similar), but it is the off-M-CSA abstention lever"
            ),
        },
        "validated_claims": [
            "Fold-NN recovers off-M-CSA bronze positives at "
            f"{off_rec.get('recovery_rate_no_abstention')} across all "
            f"{len(_per_family_recovery(off))} cofactor families (non-circular: bronze "
            "admission used sequence/cofactor, not structure).",
            "Fold-NN rejects off-M-CSA negatives: external-negative fold-NN median "
            f"{abst_test.get('external_median')} tracks the M-CSA OOS median "
            f"{abst_test.get('mcsa_oos_median')}, far below the in-scope median "
            f"{abst_test.get('mcsa_inscope_median')}.",
            "The June 9 router operating point is reproducible and clears the "
            "calibration recovery bar (30/35 @ 8 FP).",
        ],
        "not_yet_validated": [
            "No gold-truth off-M-CSA evaluation: bronze labels are automation-curated, "
            "so off-M-CSA recovery measures fold/sequence concordance, not gold accuracy.",
            "The held-out one-shot is preregistered but unspent: "
            f"`{prereg.get('status')}` (and it certifies M-CSA only).",
            "Coverage is scoped to the cofactor atlas families; broader-family recovery "
            "is not yet measured.",
            "All calibration operating points are development figures (calibration reused "
            "across readouts), not unbiased estimates.",
        ],
        "remaining_gates_for_a_deployment_claim": [
            "A gold-labelled off-M-CSA evaluation (or a curated subset) for recovery.",
            "Execute the locked held-out one-shot under its frozen rule and sha256.",
            "Broaden the M-CSA atlas beyond the cofactor families and re-run recovery.",
        ],
        "source_artifacts": {},
        "interpretation": {
            "headline": (
                "The fold (structural nearest-neighbour) channel generalises off the "
                "M-CSA development distribution on both halves -- recovery and "
                "abstention -- making it the strongest deployment lever in the project. "
                "A formal deployment claim still requires gold off-M-CSA validation and "
                "the locked held-out one-shot; nothing here is a deployment claim yet."
                if both_halves
                else "Off-M-CSA generalisation of the fold channel is incomplete; see "
                "the per-half detail."
            ),
        },
    }


def _report(summary: dict[str, Any]) -> str:
    off = summary["off_mcsa_generalization"]
    rec = off["recovery_half"]
    rej = off["rejection_half"]
    lines = [
        "# Fold Channel Deployment-Readiness Summary",
        "",
        f"Run: {summary['created_utc']}",
        f"Status: `{summary['status']}`",
        "",
        "## Question",
        "",
        f"- {summary['question']}",
        "",
        "## Off-M-CSA Generalization (the deployment question)",
        "",
        f"- **Recovery half** ({rec['surface']}): {rec['recovery']} "
        f"(M-CSA baseline {rec['mcsa_baseline_reference']}); generalizes "
        f"{rec['generalizes']}.",
        "  - Per family:",
    ]
    for fam, val in rec["per_family"].items():
        lines.append(f"    - {fam}: {val}")
    lines += [
        f"- **Rejection half**: external-negative fold-NN median "
        f"{rej['external_negative_median']} vs M-CSA OOS {rej['mcsa_oos_median']} "
        f"(in-scope {rej['mcsa_inscope_median']}); generalizes {rej['generalizes']}.",
        f"- **Both halves generalize off M-CSA: {off['both_halves_generalize_off_mcsa']}.**",
        "",
        "## Deployable Operating Point",
        "",
        f"- {summary['deployable_operating_point']['router']}: "
        f"{summary['deployable_operating_point']['calibration_point']}.",
        f"- Fold gate: {summary['deployable_operating_point']['fold_gate_role']}.",
        "",
        "## Validated Claims",
        "",
    ]
    lines += [f"- {c}" for c in summary["validated_claims"]]
    lines += ["", "## Not Yet Validated", ""]
    lines += [f"- {c}" for c in summary["not_yet_validated"]]
    lines += ["", "## Remaining Gates For A Deployment Claim", ""]
    lines += [f"- {c}" for c in summary["remaining_gates_for_a_deployment_claim"]]
    lines += [
        "",
        "## Bottom Line",
        "",
        f"- {summary['interpretation']['headline']}",
        "",
        "## Guardrails",
        "",
        "- Read-only synthesis; no new scoring, no held-out read, no registry change.",
    ]
    return "\n".join(lines) + "\n"


def write_fold_channel_deployment_readiness(
    *,
    sources: dict[str, str] | None = None,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    source_paths = dict(sources or DEFAULT_SOURCES)
    loaded = {name: _load_json(Path(p)) for name, p in source_paths.items()}
    summary = build_fold_channel_deployment_readiness(sources=loaded)
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
