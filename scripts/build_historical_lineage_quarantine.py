#!/usr/bin/env python3
"""Inventory historical artifacts whose embedded lineage no longer matches.

This deliberately does not rewrite recorded hashes.  A downstream artifact
that was produced from older bytes must remain historical and release-blocked
until it is genuinely regenerated from declared inputs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.path_compat import io_path  # noqa: E402
from catalytic_earth.canonical_hash import (  # noqa: E402
    canonical_bytes_sha256,
    canonical_file_sha256,
    canonical_hash_mode,
)


DEFAULT_OUT = ROOT / "data" / "governance" / "historical_lineage_quarantine.json"

FOLD_AUGMENTED_ARTIFACTS = (
    "v3_fold_augmented_p07658_prediction_dispatch_packet_current702_20260604.json",
    "v3_fold_augmented_confounded_proxy_high_cofactor_acquisition_dispatch_packet_current702_20260604.json",
    "v3_fold_augmented_confounded_proxy_same_family_structural_acquisition_dispatch_packet_current702_20260604.json",
    "v3_fold_augmented_lever3_dispatch_readiness_summary_current702_20260604.json",
    "v3_fold_augmented_lever3_current_measured_readout_current702_20260604.json",
    "v3_fold_augmented_confounded_proxy_loose_same_family_pressure_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_evidence_sufficiency_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_channel_veto_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_residual_safety_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_cofactor_context_counteraxis_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_same_family_bandpass_counteraxis_contract_current702_20260604.json",
    "v3_fold_augmented_lever3_post_bandpass_deployment_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_public_route_refresh_after_bandpass_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_local_runtime_refresh_after_bandpass_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_exact_route_attempts_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_exact_route_attempt_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_operating_point_deployment_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_credential_route_preflight_current702_20260604.json",
    "v3_fold_augmented_lever3_deployment_input_gap_audit_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_local_input_inventory_audit_current702_20260604.json",
    "v3_fold_augmented_lever3_p07658_sequence_compatibility_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_confounded_safe_abstention_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_deployment_action_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_retained_residual_risk_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_descriptor_present_counteraxis_preflight_current702_20260604.json",
    "v3_fold_augmented_lever3_descriptor_generalization_counteraxis_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_retained_descriptor_rescue_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604.json",
    "v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_operating_point_closure_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_closure_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_operating_point_application_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_contract_readiness_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_contract_lineage_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_contract_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_manifest_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_manifest_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_stage_provenance_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_stage_provenance_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_route_class_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_route_class_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_route_class_provenance_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_route_class_provenance_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_transfer_safety_matrix_readout_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_transfer_safety_matrix_reproducibility_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_transfer_safety_application_audit_current702_20260605.json",
    "v3_fold_augmented_lever3_deployment_operator_transfer_safety_application_reproducibility_audit_current702_20260605.json",
)


def _sha256(path: str | Path) -> str:
    full_path = ROOT / path
    if io_path(full_path).exists():
        return canonical_file_sha256(full_path)
    raw = subprocess.check_output(["git", "show", f"HEAD:{Path(path).as_posix()}"], cwd=ROOT)
    return canonical_bytes_sha256(raw, path)


def _load(path: str | Path) -> Any:
    full_path = ROOT / path
    if io_path(full_path).exists():
        with io_path(full_path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(
        subprocess.check_output(
            ["git", "show", f"HEAD:{Path(path).as_posix()}"], cwd=ROOT
        )
    )


def _record_issue(
    rows: list[dict[str, Any]],
    *,
    artifact_path: str,
    edge_id: str,
    source_path: str,
    recorded_sha256: str | None,
) -> None:
    source_exists = io_path(ROOT / source_path).exists() or subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{Path(source_path).as_posix()}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0
    observed = _sha256(source_path) if source_exists else None
    normalized_recorded = str(recorded_sha256 or "").removeprefix("sha256:") or None
    if source_exists and observed == normalized_recorded:
        return
    rows.append(
        {
            "artifact_path": artifact_path,
            "artifact_sha256": _sha256(artifact_path),
            "edge_id": edge_id,
            "source_path": source_path,
            "recorded_source_sha256": normalized_recorded,
            "observed_source_sha256": observed,
            "hash_mode": canonical_hash_mode(source_path),
            "issue_type": "stale_source_hash" if source_exists else "missing_source",
            "release_eligible": False,
            "disposition": "historical_only_regenerate_do_not_rehash",
        }
    )


def _scan_standard_source_maps(rows: list[dict[str, Any]]) -> None:
    artifacts = [f"artifacts/{name}" for name in FOLD_AUGMENTED_ARTIFACTS]
    artifacts.extend(
        [
            "artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json",
            "artifacts/v3_wave1_representation_shootout_result_card_702_20260527_addendum.json",
        ]
    )
    for artifact_path in artifacts:
        artifact = _load(artifact_path)
        for edge_id, metadata in sorted(artifact.get("source_artifacts", {}).items()):
            if not isinstance(metadata, dict):
                continue
            if metadata.get("exists") is False:
                continue
            source_path = metadata.get("path") or edge_id
            if not isinstance(source_path, str):
                continue
            _record_issue(
                rows,
                artifact_path=artifact_path,
                edge_id=str(edge_id),
                source_path=source_path,
                recorded_sha256=metadata.get("sha256"),
            )


def _scan_review_workqueue(rows: list[dict[str, Any]]) -> None:
    artifact_path = "artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json"
    metadata = _load(artifact_path)["metadata"]
    for edge_id, source_path in sorted(metadata["source_artifacts"].items()):
        _record_issue(
            rows,
            artifact_path=artifact_path,
            edge_id=edge_id,
            source_path=source_path,
            recorded_sha256=metadata["source_sha256"].get(edge_id),
        )


def _scan_coherence_audit(rows: list[dict[str, Any]]) -> None:
    artifact_path = "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json"
    artifact = _load(artifact_path)
    _record_issue(
        rows,
        artifact_path=artifact_path,
        edge_id="label_registry_digest",
        source_path="data/registries/curated_mechanism_labels.json",
        recorded_sha256=artifact.get("label_registry_digest"),
    )


def _scan_swissmodel_manifest(rows: list[dict[str, Any]]) -> None:
    artifact_path = (
        "artifacts/v3_fold_augmented_confounded_proxy_swissmodel_coordinate_"
        "staging_manifest_current702_20260604.json"
    )
    artifact = _load(artifact_path)
    for row in artifact.get("rows", []):
        selected = row.get("selected_swissmodel_model")
        if not isinstance(selected, dict):
            continue
        _record_issue(
            rows,
            artifact_path=artifact_path,
            edge_id=f"{row.get('entry_id')}:staged_coordinate",
            source_path=selected["staged_coordinate_path"],
            recorded_sha256=selected.get("staged_coordinate_sha256"),
        )


def build_quarantine() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    _scan_standard_source_maps(rows)
    _scan_review_workqueue(rows)
    _scan_coherence_audit(rows)
    _scan_swissmodel_manifest(rows)
    rows.sort(key=lambda row: (row["artifact_path"], row["edge_id"], row["source_path"]))
    artifact_counts = Counter(row["artifact_path"] for row in rows)
    artifacts = [
        {
            "artifact_path": path,
            "artifact_sha256": _sha256(path),
            "issue_count": count,
            "release_eligible": False,
        }
        for path, count in sorted(artifact_counts.items())
    ]
    return {
        "schema_version": "catalytic-earth.historical-lineage-quarantine.v1",
        "metadata": {
            "issue_count": len(rows),
            "quarantined_artifact_count": len(artifacts),
            "issue_type_counts": dict(sorted(Counter(row["issue_type"] for row in rows).items())),
            "policy": (
                "Preserve recorded hashes. Quarantined artifacts are historical-only and "
                "must not enter a canonical release until genuinely regenerated from "
                "declared source bytes. Never update embedded hashes merely to make tests pass."
            ),
            "canonical_release_exclusion_required": True,
            "hash_rule": (
                "LF-normalized SHA-256 for declared repository text formats; "
                "byte-exact SHA-256 for binary formats"
            ),
        },
        "quarantined_artifacts": artifacts,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_quarantine()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.out.exists() or args.out.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"historical lineage quarantine is stale: {args.out}")
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8", newline="\n")
    print(
        "Historical lineage quarantine valid: "
        f"artifacts={payload['metadata']['quarantined_artifact_count']} "
        f"issues={payload['metadata']['issue_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
