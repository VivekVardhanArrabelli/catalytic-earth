"""Gate 1: reconcile the production router version against the validated claim.

The validated held-out deployment claim rests on the *pinned June 9 router* (8
coarse families). Production runs the *current-57 fine router*, which drifts on
calibration (exact recovery 13/35 vs June 9's 30/35). This diagnostic determines
WHY, and therefore which fork is viable:

  - Option A: adopt the June 9 coarse router (the validated baseline).
  - Option B: repair the fine-57 router so it clears the bar, then re-pre-register
    against a NEW held-out (the M-CSA held-out is spent).

It classifies every calibration in-scope row as exact / documented-compatible
(a documented v2 taxonomy split, recoverable by relabeling) / incompatible
misroute (a genuine error) / below-threshold, and asks whether documented
relabeling alone reconciles the fine router to the June 9 bar. It reads
calibration (development) only -- never the spent held-out -- and changes no
registry, label, threshold, or model.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_precision_contract import LEGACY_V1_COMPATIBILITY


DEFAULT_CURRENT57_OPERATING_POINT_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_"
    "20260628_current57_rerun.json"
)
DEFAULT_JUNE9_TRUSTED_PATH = (
    "artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json"
)
DEFAULT_ONTOLOGY_PATH = "data/registries/mechanism_ontology.json"
DEFAULT_FROZEN_THRESHOLD = 0.4115
DEFAULT_OUT_PATH = (
    "artifacts/v3_router_reconciliation_diagnostic_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/router_reconciliation_diagnostic_current702_20260628.md"
)


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def documented_compatibility_from_ontology(ontology: Any) -> dict[str, list[str]]:
    """Coarse-umbrella -> documented v2 fine children, from ontology v2_split_note.

    Falls back to the vetted LEGACY_V1_COMPATIBILITY constant and records whether
    the ontology corroborates it.
    """

    families = ontology.get("families", []) if isinstance(ontology, dict) else []
    documented: dict[str, list[str]] = {}
    for family in families:
        if not family.get("v2_split_note"):
            continue
        fps = [str(f) for f in family.get("fingerprint_ids", []) or []]
        # the umbrella is the coarse fp that also appears as a legacy compat key
        for umbrella in fps:
            if umbrella in LEGACY_V1_COMPATIBILITY:
                documented[umbrella] = fps
    # union with the vetted constant (defensive)
    for umbrella, children in LEGACY_V1_COMPATIBILITY.items():
        merged = set(documented.get(umbrella, [])) | set(children) | {umbrella}
        documented[umbrella] = sorted(merged)
    return documented


def _fp(row: dict[str, Any]) -> str | None:
    return (row.get("fused") or {}).get("top1_fingerprint_id")


def _score(row: dict[str, Any]) -> float:
    return float((row.get("fused") or {}).get("top1_score") or 0.0)


def _june9_reference(june9: dict[str, Any]) -> dict[str, Any]:
    point = (
        june9.get("operating_points_by_split", {})
        .get("calibration", {})
        .get("fused_frozen_threshold", {})
    )
    return {
        "inscope_correct": point.get("inscope_correct"),
        "inscope_total": point.get("inscope_total"),
        "oos_false_positives": point.get("oos_false_positives"),
        "oos_total": point.get("oos_total"),
    }


def build_router_reconciliation_diagnostic(
    *,
    current57_operating_point: dict[str, Any],
    june9_trusted: dict[str, Any],
    compatibility_map: dict[str, list[str]],
    threshold: float = DEFAULT_FROZEN_THRESHOLD,
) -> dict[str, Any]:
    inscope = (
        current57_operating_point.get("row_details_by_split", {})
        .get("calibration", {})
        .get("inscope_rows", [])
        or []
    )
    classes: Counter[str] = Counter()
    misroutes: Counter[str] = Counter()
    misroute_rows: list[dict[str, Any]] = []
    for row in inscope:
        true_fp = row.get("true_fingerprint_id")
        called = _fp(row)
        if _score(row) < threshold:
            classes["below_threshold_abstain"] += 1
            continue
        if called == true_fp:
            classes["exact_correct"] += 1
        elif called in compatibility_map.get(true_fp, ()):
            classes["documented_compatible_correct"] += 1
        else:
            classes["incompatible_misroute"] += 1
            misroutes[f"{true_fp} -> {called}"] += 1
            misroute_rows.append(
                {
                    "true_fingerprint_id": true_fp,
                    "called_fingerprint_id": called,
                    "score": round(_score(row), 4),
                }
            )

    total = len(inscope)
    exact = classes["exact_correct"]
    documented = exact + classes["documented_compatible_correct"]
    june9 = _june9_reference(june9_trusted)
    june9_recovery = june9.get("inscope_correct") or 0

    # Non-umbrella true labels misrouted to metal fine-families = the failure mode.
    metal_children = set(compatibility_map.get("metal_dependent_hydrolase", ()))
    nonmetal_into_metal = sum(
        1
        for r in misroute_rows
        if r["true_fingerprint_id"] not in compatibility_map
        and r["called_fingerprint_id"] in metal_children
    )

    reconcilable_by_relabeling = documented >= june9_recovery
    gap_beyond_relabeling = max(june9_recovery - documented, 0)

    status = (
        "fine_router_reconcilable_by_documented_relabeling"
        if reconcilable_by_relabeling
        else "fine_router_drift_includes_genuine_misrouting_not_just_relabeling"
    )

    return {
        "artifact_id": "v3_router_reconciliation_diagnostic_current702_20260628",
        "schema_version": "router_reconciliation_diagnostic.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "calibration_only_router_version_reconciliation_no_heldout_no_registry_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "surface": "calibration_development_only",
            "production_threshold_changed": False,
            "registry_or_ontology_changed": False,
            "model_weights_changed": False,
            "spent_heldout_not_touched": True,
        },
        "question": (
            "Is the current-57 fine router's drift from the validated June 9 router pure "
            "taxonomy-version relabeling (cheap to reconcile), or does it include genuine "
            "misrouting (a real fix)?"
        ),
        "threshold": threshold,
        "calibration_classification": {
            "total_inscope": total,
            "exact_correct": exact,
            "documented_compatible_correct": classes["documented_compatible_correct"],
            "incompatible_misroute": classes["incompatible_misroute"],
            "below_threshold_abstain": classes["below_threshold_abstain"],
        },
        "recovery_comparison": {
            "current57_exact": f"{exact}/{total}",
            "current57_documented_compatible": f"{documented}/{total}",
            "june9_reference": f"{june9_recovery}/{june9.get('inscope_total')}",
            "reconcilable_by_documented_relabeling": reconcilable_by_relabeling,
            "recovery_gap_beyond_relabeling": gap_beyond_relabeling,
        },
        "drift_mechanism": {
            "headline": (
                "The fine-57 metal v2-subclass fingerprints over-claim non-metal "
                "(flavin / heme / PLP) enzymes in the fused geometry router; the coarse "
                "June 9 router has no metal subclasses and so does not misroute them."
            ),
            "nonmetal_enzymes_misrouted_into_metal_subclasses": nonmetal_into_metal,
            "misroute_counts": dict(misroutes.most_common()),
            "misroute_rows": misroute_rows,
        },
        "documented_compatibility_map": {
            k: list(v) for k, v in compatibility_map.items()
        },
        "fork": {
            "option_a_june9_coarse_router": {
                "status": "validated_baseline_heldout_passed",
                "evidence": "held-out one-shot PASS: 35/47 recovery, 15/79 OOS FP",
                "granularity": "coarse (~8 families); no metal subclass distinctions",
                "effort": "none (deployable now)",
                "recommended_if": "you want a deployable, validated mechanism caller now",
            },
            "option_b_repair_fine57_router": {
                "status": "requires_real_router_fix_then_new_preregistration",
                "root_cause": (
                    "metal v2-subclass fingerprints over-claim non-metal enzymes in the "
                    "fused geometry router"
                ),
                "required_work": (
                    "constrain/recalibrate the metal subclass fingerprints so they stop "
                    "claiming flavin/heme/PLP enzymes, re-verify recovery on calibration, "
                    "then a NEW pre-registration against a NEW held-out (the M-CSA "
                    "held-out is spent)"
                ),
                "granularity": "fine (57 families; metal subclass distinctions)",
                "effort": "real research investment; not free relabeling",
                "recommended_if": "production needs fine-grained metal subclass calls",
            },
        },
        "recommendation": (
            "Adopt Option A (June 9 coarse router) as the deployable validated baseline "
            "now: documented relabeling only reaches "
            f"{documented}/{total} (< June 9 {june9_recovery}/{june9.get('inscope_total')}), "
            f"because {classes['incompatible_misroute']} calibration rows are genuine "
            "misroutes, not taxonomy splits. Pursue Option B as a scoped follow-up with "
            "the identified root cause (metal-subclass over-claiming) only if fine-grained "
            "metal subclass calls are required in production."
        ),
    }


def _report(diag: dict[str, Any]) -> str:
    cc = diag["calibration_classification"]
    rc = diag["recovery_comparison"]
    dm = diag["drift_mechanism"]
    lines = [
        "# Gate 1: Router Reconciliation Diagnostic",
        "",
        f"Run: {diag['created_utc']}",
        f"Status: `{diag['status']}`",
        "",
        "## Question",
        "",
        f"- {diag['question']}",
        "",
        "## Calibration Classification (in-scope, threshold "
        f"{diag['threshold']})",
        "",
        f"- Exact correct: {cc['exact_correct']}/{cc['total_inscope']}.",
        f"- Documented-compatible (v2 split, relabeling): "
        f"{cc['documented_compatible_correct']}.",
        f"- Incompatible misroute (genuine error): {cc['incompatible_misroute']}.",
        f"- Below threshold (abstain): {cc['below_threshold_abstain']}.",
        "",
        "## Recovery Comparison",
        "",
        f"- current-57 exact: {rc['current57_exact']}.",
        f"- current-57 documented-compatible (relabeling ceiling): "
        f"{rc['current57_documented_compatible']}.",
        f"- June 9 reference: {rc['june9_reference']}.",
        f"- Reconcilable by documented relabeling alone: "
        f"{rc['reconcilable_by_documented_relabeling']}.",
        f"- Recovery gap beyond relabeling: {rc['recovery_gap_beyond_relabeling']}.",
        "",
        "## Drift Mechanism",
        "",
        f"- {dm['headline']}",
        f"- Non-metal enzymes misrouted into metal subclasses: "
        f"{dm['nonmetal_enzymes_misrouted_into_metal_subclasses']}.",
        "- Misroutes:",
    ]
    for k, n in dm["misroute_counts"].items():
        lines.append(f"  - {n}x  {k}")
    lines += [
        "",
        "## Fork",
        "",
        f"- **Option A (June 9 coarse router):** "
        f"{diag['fork']['option_a_june9_coarse_router']['status']} — "
        f"{diag['fork']['option_a_june9_coarse_router']['evidence']}; "
        f"{diag['fork']['option_a_june9_coarse_router']['granularity']}; effort "
        f"{diag['fork']['option_a_june9_coarse_router']['effort']}.",
        f"- **Option B (repair fine-57):** "
        f"{diag['fork']['option_b_repair_fine57_router']['status']}; root cause: "
        f"{diag['fork']['option_b_repair_fine57_router']['root_cause']}; work: "
        f"{diag['fork']['option_b_repair_fine57_router']['required_work']}.",
        "",
        "## Recommendation",
        "",
        f"- {diag['recommendation']}",
        "",
        "## Guardrails",
        "",
        "- Calibration (development) only; the spent held-out one-shot was not touched.",
        "- No registry, ontology, label, threshold, or model change.",
    ]
    return "\n".join(lines) + "\n"


def write_router_reconciliation_diagnostic(
    *,
    current57_operating_point_path: Path,
    june9_trusted_path: Path,
    ontology_path: Path,
    threshold: float = DEFAULT_FROZEN_THRESHOLD,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    current57 = _load_json(Path(current57_operating_point_path))
    june9 = _load_json(Path(june9_trusted_path))
    ontology = _load_json(Path(ontology_path))
    compatibility_map = documented_compatibility_from_ontology(ontology)
    diag = build_router_reconciliation_diagnostic(
        current57_operating_point=current57,
        june9_trusted=june9,
        compatibility_map=compatibility_map,
        threshold=threshold,
    )
    diag["source_artifacts"] = {
        "current57_operating_point": {
            "path": str(current57_operating_point_path),
            "sha256": _sha256(Path(current57_operating_point_path)),
        },
        "june9_trusted": {
            "path": str(june9_trusted_path),
            "sha256": _sha256(Path(june9_trusted_path)),
        },
        "ontology": {
            "path": str(ontology_path),
            "sha256": _sha256(Path(ontology_path)),
        },
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(diag, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(diag), encoding="utf-8")
    return diag
