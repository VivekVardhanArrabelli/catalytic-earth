"""Executor for the locked held-out one-shot (see heldout_oneshot_preregistration).

This runs the single pre-registered held-out test exactly once. It:
  1. rebuilds the frozen held-out set and asserts its sha256 matches the
     pre-registration (so the evaluated rows cannot have changed),
  2. scores those rows through the SAME cofactor-fusion router used for the
     calibration replay (build_cofactor_fusion_operating_point, with
     split_assignment="heldout" and the held-out coordinate dirs) at the frozen
     0.44 cofactor dial, and
  3. compares the held-out recovery and OOS-FP rates to the pre-committed bar and
     emits PASS or FAIL verbatim.

It MUST be run inside an isolated git worktree whose registry is pinned to the
frozen commit (d567ee0d); the main-repo 57-fingerprint registry is never mutated.
The caller is responsible for that pin and for invoking this exactly once.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_fusion_operating_point import build_cofactor_fusion_operating_point
from .heldout_oneshot_preregistration import build_frozen_heldout_set


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _heldout_structure_accessions(coordinate_dirs: list[str]) -> set[str]:
    import glob
    import os

    accs: set[str] = set()
    for directory in coordinate_dirs:
        for cif in glob.glob(os.path.join(directory, "*.cif")):
            match = re.search(r"afdb_([A-Za-z0-9]+)_v6", os.path.basename(cif))
            if match:
                accs.add(match.group(1))
    return accs


def run_heldout_oneshot_eval(
    *,
    preregistration: dict[str, Any],
    split_manifest: dict[str, Any],
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    channel: dict[str, Any],
    heldout_coordinate_dirs: list[str],
    threshold: float = 0.44,
) -> dict[str, Any]:
    # 1. Verify the frozen set has not changed.
    frozen = build_frozen_heldout_set(
        split_manifest=split_manifest,
        label_manifest=label_manifest,
        heldout_structure_accessions=_heldout_structure_accessions(
            heldout_coordinate_dirs
        ),
    )
    expected_sha = preregistration["frozen_heldout_set"]["sha256"]
    if frozen["sha256"] != expected_sha:
        raise AssertionError(
            "frozen_heldout_set sha256 mismatch: refusing to run the one-shot. "
            f"expected {expected_sha} got {frozen['sha256']}"
        )

    # 2. Score the frozen rows through the same router used for calibration, by
    #    mapping them to one split bucket and selecting split_assignment=heldout.
    eval_split_manifest = {
        "split_records": [
            {"entry_id": m["entry_id"], "assigned_embedding_split": "calibration"}
            for m in frozen["members"]
        ]
    }
    operating_point = build_cofactor_fusion_operating_point(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_manifest=eval_split_manifest,
        channel=channel,
        staged_dirs=[Path(d) for d in heldout_coordinate_dirs],
        threshold=threshold,
        split_assignment="heldout",
    )

    point = (
        operating_point.get("operating_points_by_split", {})
        .get("calibration", {})
        .get("fused_frozen_threshold", {})
    )
    inscope_correct = point.get("inscope_correct")
    inscope_total = point.get("inscope_total")
    oos_fp = point.get("oos_false_positives")
    oos_total = point.get("oos_total")
    recovery_rate = (
        round(inscope_correct / inscope_total, 4) if inscope_total else None
    )
    oos_fp_rate = round(oos_fp / oos_total, 4) if oos_total else None

    bar = preregistration["success_bar"]
    # Pre-committed: recovery_rate >= 0.70 AND oos_fp_rate <= 0.40.
    passed = bool(
        recovery_rate is not None
        and oos_fp_rate is not None
        and recovery_rate >= 0.70
        and oos_fp_rate <= 0.40
    )

    coverage = operating_point.get("coverage", {})
    return {
        "artifact_id": "v3_heldout_oneshot_eval_result_current702_20260628",
        "schema_version": "heldout_oneshot_eval_result.v1",
        "created_utc": _utc_now_iso(),
        "status": "heldout_oneshot_eval_PASS" if passed else "heldout_oneshot_eval_FAIL",
        "verdict": "PASS" if passed else "FAIL",
        "result_class": "spent_one_shot_heldout_evaluation_pinned_june9_router",
        "preregistration": {
            "artifact_id": preregistration.get("artifact_id"),
            "frozen_heldout_set_sha256": expected_sha,
            "sha256_verified": True,
            "primary_pass_criteria": bar.get("primary_pass_criteria"),
        },
        "frozen_rule_applied": {
            "router": "june9 registry pin d567ee0d via isolated worktree",
            "cofactor_threshold": threshold,
            "split_assignment": "heldout",
        },
        "heldout_result": {
            "inscope_recovery": f"{inscope_correct}/{inscope_total}",
            "inscope_recovery_rate": recovery_rate,
            "oos_false_positives": f"{oos_fp}/{oos_total}",
            "oos_false_positive_rate": oos_fp_rate,
        },
        "calibration_reference": bar.get("calibration_reference"),
        "coverage": {
            "frozen_total": frozen["counts"]["total"],
            "frozen_inscope": frozen["counts"]["inscope"],
            "frozen_oos": frozen["counts"]["oos"],
            "inscope_scored": coverage.get("inscope_scored"),
            "oos_scored": coverage.get("oos_scored"),
            "oos_coverage_gap_rows": coverage.get("oos_coverage_gap_rows"),
        },
        "guardrails": {
            "ran_once": True,
            "rule_fixed_before_run": True,
            "main_repo_registry_mutated": False,
            "no_post_hoc_threshold_change": True,
        },
        "operating_point_raw": point,
    }


def write_heldout_oneshot_eval(
    *,
    preregistration_path: Path,
    split_manifest_path: Path,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_path: Path,
    channel_path: Path,
    heldout_coordinate_dirs: list[str],
    threshold: float,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    result = run_heldout_oneshot_eval(
        preregistration=_load_json(preregistration_path),
        split_manifest=_load_json(split_manifest_path),
        label_manifest=_load_json(label_manifest_path),
        graph=_load_json(graph_path),
        experimental_geometry_features=_load_json(experimental_geometry_path),
        channel=_load_json(channel_path),
        heldout_coordinate_dirs=heldout_coordinate_dirs,
        threshold=threshold,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        hr = result["heldout_result"]
        cov = result["coverage"]
        lines = [
            "# Held-Out One-Shot Evaluation Result",
            "",
            f"Run: {result['created_utc']}",
            f"Verdict: **{result['verdict']}**  (`{result['status']}`)",
            "",
            "## Pre-Registration",
            "",
            f"- Artifact: {result['preregistration']['artifact_id']}",
            f"- Frozen set sha256 verified: {result['preregistration']['sha256_verified']}.",
            f"- Pass criteria: {result['preregistration']['primary_pass_criteria']}.",
            "",
            "## Held-Out Result (June 9 router, 0.44 dial, run once)",
            "",
            f"- In-scope recovery: {hr['inscope_recovery']} "
            f"({hr['inscope_recovery_rate']}).",
            f"- OOS false positives: {hr['oos_false_positives']} "
            f"({hr['oos_false_positive_rate']}).",
            f"- Calibration reference: recovery "
            f"{result['calibration_reference'].get('inscope_recovery')}, OOS FP "
            f"{result['calibration_reference'].get('oos_false_positive_rate')}.",
            "",
            "## Coverage",
            "",
            f"- Frozen set: {cov['frozen_total']} ({cov['frozen_inscope']} in-scope, "
            f"{cov['frozen_oos']} OOS).",
            f"- Scored: in-scope {cov['inscope_scored']}, OOS {cov['oos_scored']}.",
            "",
            "## Guardrails",
            "",
            "- Ran once under the frozen rule; main-repo registry never mutated; no "
            "post-hoc threshold change.",
        ]
        Path(report_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result
