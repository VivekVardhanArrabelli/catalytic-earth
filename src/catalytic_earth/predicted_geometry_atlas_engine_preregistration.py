"""Full-env check and preregistration for the predicted-geometry atlas engine.

This artifact is deliberately a contract, not a score rerun. It records whether
the local backend can run the deployment tools, hashes the existing leakage-safe
cofactor/fold surfaces, and fixes the next train/cal readout before any heldout
read is attempted.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CURRENT702_PATH = "data/registries/curated_mechanism_labels.json"
DEFAULT_COFACTOR_CHANNEL_PATH = (
    "artifacts/v3_cofactor_presence_calibration_current702_20260604.json"
)
DEFAULT_RECOVERY_PATH = (
    "artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json"
)
DEFAULT_COFACTOR_PRECISION_PATH = (
    "artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json"
)
DEFAULT_FOLD_CHANNEL_PATH = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601.json"
)
DEFAULT_FOLD_CONTRACT_AUDIT_PATH = (
    "artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json"
)
DEFAULT_FOLD_COORDINATE_PROVENANCE_PATH = (
    "artifacts/v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json"
)
DEFAULT_FOLD_THRESHOLD_CONTRACT_PATH = (
    "artifacts/v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.json"
)
DEFAULT_FOLD_POST_RERUN_CLOSURE_PATH = (
    "artifacts/v3_fold_augmented_post_rerun_deployment_closure_status_current702_20260603.json"
)
DEFAULT_FOLD_CONFOUNDED_CLOSURE_PATH = (
    "artifacts/v3_fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.json"
)
DEFAULT_SPLIT_MANIFEST_PATH = (
    "artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json"
)
DEFAULT_CURRENT_ROUTER_COFACTOR_RERUN_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260628_current57_rerun.json"
)
DEFAULT_COORDINATE_ROOT = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates"
)

PYTHON_MODULES = ("numpy", "torch", "sklearn", "pandas", "esm", "Bio", "biotite")
EXECUTABLES = ("mmseqs", "foldseek", "diamond")


def write_predicted_geometry_atlas_engine_preregistration(
    *,
    current702_path: Path,
    cofactor_channel_path: Path,
    recovery_path: Path,
    cofactor_precision_path: Path,
    fold_channel_path: Path,
    fold_contract_audit_path: Path,
    fold_coordinate_provenance_path: Path,
    fold_threshold_contract_path: Path,
    fold_post_rerun_closure_path: Path,
    fold_confounded_closure_path: Path,
    split_manifest_path: Path,
    coordinate_root: Path,
    out_path: Path,
    report_path: Path | None = None,
    current_router_cofactor_rerun_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_predicted_geometry_atlas_engine_preregistration(
        current702_path=current702_path,
        cofactor_channel_path=cofactor_channel_path,
        recovery_path=recovery_path,
        cofactor_precision_path=cofactor_precision_path,
        fold_channel_path=fold_channel_path,
        fold_contract_audit_path=fold_contract_audit_path,
        fold_coordinate_provenance_path=fold_coordinate_provenance_path,
        fold_threshold_contract_path=fold_threshold_contract_path,
        fold_post_rerun_closure_path=fold_post_rerun_closure_path,
        fold_confounded_closure_path=fold_confounded_closure_path,
        split_manifest_path=split_manifest_path,
        coordinate_root=coordinate_root,
        current_router_cofactor_rerun_path=current_router_cofactor_rerun_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit


def build_predicted_geometry_atlas_engine_preregistration(
    *,
    current702_path: Path,
    cofactor_channel_path: Path,
    recovery_path: Path,
    cofactor_precision_path: Path,
    fold_channel_path: Path,
    fold_contract_audit_path: Path,
    fold_coordinate_provenance_path: Path,
    fold_threshold_contract_path: Path,
    fold_post_rerun_closure_path: Path,
    fold_confounded_closure_path: Path,
    split_manifest_path: Path,
    coordinate_root: Path,
    current_router_cofactor_rerun_path: Path | None = None,
    module_status: dict[str, bool] | None = None,
    executable_status: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    sources = {
        "current702_registry": _artifact_summary(current702_path),
        "cofactor_channel": _artifact_summary(cofactor_channel_path),
        "in_distribution_recovery": _artifact_summary(recovery_path),
        "cofactor_precision": _artifact_summary(cofactor_precision_path),
        "predicted_structure_fold_channel": _artifact_summary(fold_channel_path),
        "fold_channel_contract_audit": _artifact_summary(fold_contract_audit_path),
        "fold_coordinate_provenance": _artifact_summary(fold_coordinate_provenance_path),
        "fold_threshold_contract": _artifact_summary(fold_threshold_contract_path),
        "fold_post_rerun_closure": _artifact_summary(fold_post_rerun_closure_path),
        "fold_confounded_closure": _artifact_summary(fold_confounded_closure_path),
        "split_manifest": _artifact_summary(split_manifest_path),
    }
    if current_router_cofactor_rerun_path is not None:
        sources["current_router_cofactor_rerun"] = _artifact_summary(
            current_router_cofactor_rerun_path
        )
    loaded = {
        name: _load_json_if_exists(Path(summary["path"]))
        for name, summary in sources.items()
        if name != "current702_registry"
    }
    modules = module_status if module_status is not None else _python_module_status()
    executables = (
        executable_status if executable_status is not None else _executable_status()
    )
    coordinate_bundles = _coordinate_bundle_status(coordinate_root)

    missing_required = [
        name
        for name in (
            "cofactor_channel",
            "in_distribution_recovery",
            "cofactor_precision",
            "predicted_structure_fold_channel",
            "fold_channel_contract_audit",
            "fold_coordinate_provenance",
            "fold_threshold_contract",
            "fold_post_rerun_closure",
            "fold_confounded_closure",
            "split_manifest",
        )
        if not sources[name]["exists"]
    ]
    existing_scored_fold_reusable = (
        not missing_required
        and loaded.get("predicted_structure_fold_channel", {}).get("status")
        in {"computed_all_heldout_foldseek_scores", "fold_channel_contract_passed_current702"}
        and _status_contains_pass_or_ready(loaded.get("fold_channel_contract_audit", {}))
        and coordinate_bundles["atlas_in_distribution"]["cif_count"] > 0
    )
    sequence_sidecars_reusable = (
        bool(modules.get("numpy"))
        and bool(modules.get("sklearn"))
        and sources["cofactor_channel"]["exists"]
        and sources["cofactor_precision"]["exists"]
    )
    full_new_fold_tm_runnable = bool(executables.get("foldseek", {}).get("available"))
    full_env_runnable = (
        sequence_sidecars_reusable
        and full_new_fold_tm_runnable
        and bool(modules.get("numpy"))
        and bool(modules.get("torch"))
    )

    status = _status(
        missing_required=missing_required,
        full_new_fold_tm_runnable=full_new_fold_tm_runnable,
        existing_scored_fold_reusable=existing_scored_fold_reusable,
        sequence_sidecars_reusable=sequence_sidecars_reusable,
    )

    recovery = _recovery_context(loaded.get("in_distribution_recovery", {}))
    cofactor_precision = _cofactor_precision_context(loaded.get("cofactor_precision", {}))
    current_router_rerun = _current_router_rerun_context(
        loaded.get("current_router_cofactor_rerun", {})
    )
    current_router_drift_detected = bool(
        current_router_rerun.get("current_router_drift_detected")
    )
    if current_router_drift_detected and status.startswith("preregistered"):
        status = "preregistered_cached_surface_blocked_current57_router_drift"
        if not full_new_fold_tm_runnable:
            status += "_new_foldseek_backend_blocked"
    fold_context = _fold_context(
        threshold_contract=loaded.get("fold_threshold_contract", {}),
        post_rerun_closure=loaded.get("fold_post_rerun_closure", {}),
        confounded_closure=loaded.get("fold_confounded_closure", {}),
    )

    return {
        "artifact_id": "v3_predicted_geometry_atlas_engine_preregistration_current702_20260628",
        "schema_version": "predicted_geometry_atlas_engine_preregistration.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "preregistration_and_full_env_capability_check_no_new_scores_no_heldout_read"
        ),
        "guardrails": {
            "heldout_rows_scored_now": False,
            "heldout_labels_read_now": False,
            "heldout_threshold_tuning_authorized": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "registries_or_ontologies_changed": False,
            "current702_registry_edited": False,
            "new_fingerprint_family_growth": False,
            "experimental_pdb_metadata_allowed_as_deployment_input": False,
            "ec_name_prose_or_fingerprint_used_as_predictive_features": False,
        },
        "runtime_capability": {
            "python_modules": modules,
            "executables": executables,
            "sequence_sidecars_reusable": sequence_sidecars_reusable,
            "existing_scored_fold_tm_surfaces_reusable": existing_scored_fold_reusable,
            "full_new_fold_tm_scoring_runnable": full_new_fold_tm_runnable,
            "full_env_runnable_for_new_end_to_end_scores": full_env_runnable,
            "blockers": _capability_blockers(
                modules=modules,
                executables=executables,
                sequence_sidecars_reusable=sequence_sidecars_reusable,
            ),
        },
        "source_artifacts": sources,
        "coordinate_bundles": coordinate_bundles,
        "preexisting_train_cal_context": {
            "cofactor_recovery": recovery,
            "cofactor_precision": cofactor_precision,
            "current_router_cofactor_rerun": current_router_rerun,
            "fold_tm_oos_safety": fold_context,
        },
        "preregistered_experiment": _preregistered_experiment(
            cofactor_threshold=cofactor_precision.get(
                "calibration_threshold_dial_matching_suppression_precision"
            ),
            fold_threshold=fold_context.get("fixed_threshold"),
            existing_scored_fold_reusable=existing_scored_fold_reusable,
            full_new_fold_tm_runnable=full_new_fold_tm_runnable,
            current_router_drift_detected=current_router_drift_detected,
        ),
        "decision": {
            "can_run_cached_surface_atlas_engine_readout_now": bool(
                existing_scored_fold_reusable
                and sequence_sidecars_reusable
                and not current_router_drift_detected
            ),
            "can_compute_new_fold_tm_scores_now": full_new_fold_tm_runnable,
            "current_router_drift_detected": current_router_drift_detected,
            "next_action": (
                "Resolve the current-router/fingerprint-surface drift before an "
                "atlas-engine readout: either freeze the intended June 9 router/"
                "fingerprint surface for cofactor precision, or preregister a new "
                "current-57-family cofactor precision rule on train/cal. Install "
                "or expose foldseek before any new Foldseek/TM scoring."
                if current_router_drift_detected
                else "Run the cached-surface train/cal atlas-engine readout under "
                "this contract; install or expose foldseek before any new "
                "Foldseek/TM scoring or coordinate expansion."
                if existing_scored_fold_reusable and sequence_sidecars_reusable
                else "Resolve missing preregistration source artifacts before any "
                "atlas-engine readout."
            ),
        },
    }


def _artifact_summary(path: Path) -> dict[str, Any]:
    path = Path(path)
    summary: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "sha256": _sha256(path) if path.exists() and path.is_file() else None,
    }
    if path.exists() and path.suffix == ".json":
        data = _load_json_if_exists(path)
        if isinstance(data, dict):
            summary["artifact_id"] = data.get("artifact_id")
            summary["status"] = data.get("status")
            summary["schema_version"] = data.get("schema_version")
    return summary


def _load_json_if_exists(path: Path) -> Any:
    path = Path(path)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _python_module_status() -> dict[str, bool]:
    return {name: importlib.util.find_spec(name) is not None for name in PYTHON_MODULES}


def _executable_status() -> dict[str, dict[str, Any]]:
    return {name: _one_executable_status(name) for name in EXECUTABLES}


def _one_executable_status(name: str) -> dict[str, Any]:
    resolved = shutil.which(name)
    if resolved is None:
        return {"available": False, "path": None, "version": None}
    version = None
    for args in ((name, "version"), (name, "--version")):
        try:
            proc = subprocess.run(
                args,
                check=False,
                text=True,
                capture_output=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        text = (proc.stdout or proc.stderr or "").strip()
        if text:
            version = text.splitlines()[0][:160]
            break
    return {"available": True, "path": resolved, "version": version}


def _coordinate_bundle_status(root: Path) -> dict[str, Any]:
    root = Path(root)
    bundles = {}
    for name in (
        "atlas_in_distribution",
        "confounded_proxy_train_cal_tranche_queries",
        "queries_all_heldout",
        "queries_cofactor_confounded_oos",
    ):
        path = root / name
        bundles[name] = {
            "path": str(path),
            "exists": path.exists(),
            "cif_count": len(list(path.glob("*.cif"))) if path.exists() else 0,
            "deployment_use_in_this_contract": name
            in {"atlas_in_distribution", "confounded_proxy_train_cal_tranche_queries"},
        }
    return bundles


def _status_contains_pass_or_ready(data: dict[str, Any]) -> bool:
    status = str(data.get("status") or "")
    return "pass" in status or "ready" in status or "computed" in status


def _status(
    *,
    missing_required: list[str],
    full_new_fold_tm_runnable: bool,
    existing_scored_fold_reusable: bool,
    sequence_sidecars_reusable: bool,
) -> str:
    if missing_required:
        return "blocked_missing_preregistration_source_artifacts"
    if not sequence_sidecars_reusable:
        return "blocked_sequence_channel_backend_or_sidecar_unavailable"
    if not existing_scored_fold_reusable:
        return "blocked_existing_scored_fold_tm_surface_not_reusable"
    if not full_new_fold_tm_runnable:
        return "preregistered_cached_surface_ready_new_foldseek_backend_blocked"
    return "preregistered_full_env_ready"


def _capability_blockers(
    *,
    modules: dict[str, bool],
    executables: dict[str, dict[str, Any]],
    sequence_sidecars_reusable: bool,
) -> list[str]:
    blockers = []
    if not sequence_sidecars_reusable:
        blockers.append("sequence_sidecars_or_numpy_sklearn_unavailable")
    if not modules.get("torch"):
        blockers.append("torch_missing_for_new_embedding_backends")
    if not modules.get("esm"):
        blockers.append("esm_missing_for_new_esm_embedding_generation")
    if not executables.get("foldseek", {}).get("available"):
        blockers.append("foldseek_missing_for_new_fold_tm_scoring")
    if not executables.get("mmseqs", {}).get("available"):
        blockers.append("mmseqs_missing_for_sequence_search_screens")
    return blockers


def _recovery_context(recovery: dict[str, Any]) -> dict[str, Any]:
    cal = recovery.get("readouts_by_split", {}).get("calibration", {})
    return {
        "surface": "calibration_out_of_sample_for_cofactor_channel",
        "experimental_correct": cal.get("experimental_correct"),
        "apo_correct": cal.get("apo_correct"),
        "fused_correct": cal.get("fused_correct"),
        "apo_lost_primary_rows": cal.get("apo_lost_primary_rows"),
        "fused_recovered_rows": cal.get("fused_recovered_rows"),
        "recovery_fraction_of_apo_loss": cal.get("recovery_fraction_of_apo_loss"),
        "fused_regressed_rows": cal.get("fused_regressed_rows"),
    }


def _cofactor_precision_context(precision: dict[str, Any]) -> dict[str, Any]:
    dial = precision.get("dial_comparison", {})
    match = dial.get("threshold_dial_matching_suppression_precision") or {}
    fused = dial.get("fused_frozen") or {}
    suppression = dial.get("suppression_dial") or {}
    return {
        "surface": dial.get("surface"),
        "fused_frozen": fused,
        "suppression_dial": suppression,
        "calibration_threshold_dial_matching_suppression_precision": match.get("threshold"),
        "threshold_match_readout": match,
        "threshold_dial_dominates_suppression_dial": dial.get(
            "threshold_dial_dominates_suppression_dial"
        ),
    }


def _current_router_rerun_context(rerun: dict[str, Any]) -> dict[str, Any]:
    if not rerun:
        return {
            "present": False,
            "current_router_drift_detected": False,
        }
    context = rerun.get("rerun_context", {})
    previous = context.get("previous_calibration_fused_frozen", {})
    current = context.get("current57_calibration_fused_frozen", {})
    drift = bool(previous and current and previous != current)
    return {
        "present": True,
        "artifact_id": rerun.get("artifact_id"),
        "status": rerun.get("status"),
        "current_router_drift_detected": drift,
        "previous_calibration_fused_frozen": previous,
        "current57_calibration_fused_frozen": current,
        "interpretation": context.get("interpretation"),
    }


def _fold_context(
    *,
    threshold_contract: dict[str, Any],
    post_rerun_closure: dict[str, Any],
    confounded_closure: dict[str, Any],
) -> dict[str, Any]:
    operating_point = confounded_closure.get("operating_point", {})
    fixed_threshold = (
        operating_point.get("fixed_threshold")
        or post_rerun_closure.get("fixed_threshold")
        or _expanded_contract_threshold(threshold_contract)
    )
    remaining = post_rerun_closure.get("remaining_blockers", [])
    return {
        "channel": operating_point.get("channel") or "combined_mean_geometry_fold",
        "fixed_threshold": fixed_threshold,
        "calibration_oos_abstain_recall": operating_point.get(
            "calibration_oos_abstain_recall"
        ),
        "calibration_oos_abstained": operating_point.get("calibration_oos_abstained"),
        "calibration_oos_total": operating_point.get("calibration_oos_total"),
        "heldout_confounded_oos_abstain_recall_prior_spent_readout": operating_point.get(
            "heldout_confounded_oos_abstain_recall"
        ),
        "heldout_confounded_oos_abstained_prior_spent_readout": operating_point.get(
            "heldout_confounded_oos_abstained"
        ),
        "heldout_confounded_oos_total_prior_spent_readout": operating_point.get(
            "heldout_confounded_oos_total"
        ),
        "remaining_production_blockers": remaining,
        "deployment_closed_now": post_rerun_closure.get("decision", {}).get(
            "deployment_closed_now"
        ),
    }


def _expanded_contract_threshold(contract: dict[str, Any]) -> float | None:
    primary = contract.get("primary_channel_readout", {})
    selected = primary.get("selected_at_90pct_calibration_in_scope_retention", {})
    return selected.get("threshold")


def _preregistered_experiment(
    *,
    cofactor_threshold: float | None,
    fold_threshold: float | None,
    existing_scored_fold_reusable: bool,
    full_new_fold_tm_runnable: bool,
    current_router_drift_detected: bool,
) -> dict[str, Any]:
    return {
        "name": "predicted_apo_atlas_engine_v1_train_cal_contract",
        "purpose": (
            "Advance predicted-apo deployment precision by composing the frozen "
            "cofactor reconstruction channel with the predicted-structure fold/TM "
            "channel on train/cal surfaces only."
        ),
        "surfaces": {
            "train": "in-sample reference only for the cofactor channel",
            "calibration": (
                "primary readout: in-scope recovery plus OOS false-positive/"
                "abstention diagnostics; no heldout rows"
            ),
            "heldout": "excluded; prior spent heldout numbers may be cited as context only",
        },
        "features_channels": [
            {
                "name": "predicted_apo_geometry_router",
                "inputs": "AlphaFoldDB-v6 predicted apo coordinates from staged local CIFs",
                "forbidden_inputs": "experimental bound ligands, PDB metadata, EC/name/prose",
            },
            {
                "name": "cofactor_reconstruction_channel",
                "inputs": (
                    "frozen sequence-embedding cofactor-presence artifact; structural "
                    "ligand-context supervision only"
                ),
                "action": "inject predicted cofactor families into ligand_context",
            },
            {
                "name": "fold_tm_channel",
                "inputs": (
                    "existing predicted-structure-vs-atlas Foldseek/TM scores when "
                    "available; new Foldseek scoring only if foldseek is installed"
                ),
                "action": "fail closed on missing fold/TM score",
            },
        ],
        "thresholds_and_selection_rule": {
            "cofactor_fused_router_threshold": cofactor_threshold,
            "fold_tm_combined_mean_geometry_fold_threshold": fold_threshold,
            "primary_selection_rule": (
                "On calibration rows, retain a primary call only when the "
                "cofactor-fused router score is at least the preregistered "
                "cofactor threshold and the fold/TM combined_mean_geometry_fold "
                "gate retains at its fixed threshold; otherwise abstain."
            ),
            "threshold_source": (
                "cofactor threshold is copied from the calibration threshold dial "
                "matching suppression precision; fold/TM threshold is copied from "
                "the existing expanded OOS-calibrated contract"
            ),
            "production_change": "none",
        },
        "metrics": [
            "calibration recovery fraction over apo-lost in-scope primaries",
            "calibration net in-scope recall retained after fusion plus fold/TM gate",
            "calibration OOS false-positive count and rate",
            "calibration OOS abstain recall",
            "coverage gaps and fail-closed missing-coordinate counts",
            "cofactor-confounded-neighborhood retained false positives",
            "remaining policy caveats such as P10746/fold-only rows",
        ],
        "done_bar": {
            "minimum_train_cal_gate": (
                "candidate keeps >=30/35 calibration in-scope cofactor-fused "
                "primaries while not increasing OOS FPs over the 0.44 cofactor "
                "threshold readout, and every missing fold/TM score is fail-closed"
            ),
            "heldout_gate": (
                "No heldout read is authorized by this artifact. A later heldout "
                "read requires this train/cal gate plus explicit user approval."
            ),
            "full_env_note": (
                "Cached scored fold/TM surfaces are enough for the next train/cal "
                "readout."
                if existing_scored_fold_reusable
                else "Existing scored fold/TM surfaces are not reusable yet."
            ),
            "new_fold_tm_note": (
                "New Foldseek/TM scoring can run in this environment."
                if full_new_fold_tm_runnable
                else "New Foldseek/TM scoring is blocked until foldseek is installed."
            ),
            "current_router_note": (
                "Current-57-family router drift is detected; freeze the intended "
                "router/fingerprint surface or preregister a current-57 precision "
                "rule before atlas-engine fusion."
                if current_router_drift_detected
                else "No current-router cofactor precision drift diagnostic is blocking."
            ),
        },
    }


def _report(audit: dict[str, Any]) -> str:
    cap = audit["runtime_capability"]
    cofactor = audit["preexisting_train_cal_context"]["cofactor_precision"]
    recovery = audit["preexisting_train_cal_context"]["cofactor_recovery"]
    fold = audit["preexisting_train_cal_context"]["fold_tm_oos_safety"]
    drift = audit["preexisting_train_cal_context"].get(
        "current_router_cofactor_rerun", {}
    )
    exp = audit["preregistered_experiment"]
    lines = [
        "# Predicted-Geometry Atlas Engine Preregistration",
        "",
        f"Run: {audit['created_utc']}",
        f"Status: `{audit['status']}`",
        "",
        "## Capability",
        "",
        f"- Existing scored fold/TM surfaces reusable: "
        f"{cap['existing_scored_fold_tm_surfaces_reusable']}.",
        f"- New Foldseek/TM scoring runnable: {cap['full_new_fold_tm_scoring_runnable']}.",
        f"- Sequence sidecars reusable: {cap['sequence_sidecars_reusable']}.",
        f"- Blockers: {', '.join(cap['blockers']) if cap['blockers'] else 'none'}.",
        "",
        "## Preexisting Train/Cal Context",
        "",
        f"- Cofactor recovery calibration: experimental "
        f"{recovery.get('experimental_correct')} -> apo {recovery.get('apo_correct')} "
        f"-> fused {recovery.get('fused_correct')}; recovered "
        f"{recovery.get('fused_recovered_rows')}/"
        f"{recovery.get('apo_lost_primary_rows')}.",
        f"- Cofactor precision threshold dial: "
        f"{cofactor.get('calibration_threshold_dial_matching_suppression_precision')} "
        f"(dominates suppression: "
        f"{cofactor.get('threshold_dial_dominates_suppression_dial')}).",
        f"- Fold/TM fixed threshold: {fold.get('fixed_threshold')}; calibration OOS "
        f"abstain {fold.get('calibration_oos_abstained')}/"
        f"{fold.get('calibration_oos_total')}.",
        f"- Current-router drift detected: "
        f"{drift.get('current_router_drift_detected', False)}.",
        "",
        "## Preregistered Next Readout",
        "",
        f"- Name: `{exp['name']}`.",
        f"- Selection rule: {exp['thresholds_and_selection_rule']['primary_selection_rule']}",
        f"- Done bar: {exp['done_bar']['minimum_train_cal_gate']}",
        "",
        "## Guardrails",
        "",
        "- No heldout rows are scored or read by this artifact.",
        "- No production threshold, model weight, registry, ontology, or fingerprint-family change is made.",
        f"- Next action: {audit['decision']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
