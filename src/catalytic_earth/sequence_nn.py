from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .labels import MechanismLabel


PRIMARY_BENCHMARK_PREFIX = "primary_supervised_metric"
SECONDARY_BENCHMARK_PREFIX = "secondary_ood_probe"
OOS_BENCHMARK_PREFIX = "oos_tier"


def build_sequence_nn_label_manifest_and_compliance(
    *,
    labels: list[MechanismLabel],
    fingerprints: list[Any],
    coherence_audit: dict[str, Any],
    eval_contract: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    label_registry_path: Path,
    fingerprint_registry_path: Path,
    coherence_audit_path: Path,
    eval_contract_path: Path,
    sequence_manifest_path: Path,
    split_artifact_path: Path,
    label_manifest_out: Path,
    predictions_out: Path,
    metrics_out: Path,
    compliance_out: Path,
) -> dict[str, Any]:
    """Build the sequence-NN label manifest and fail-closed contract checks.

    The sequence-NN benchmark may only run when the frozen current-label split
    covers every manifest row. This function intentionally returns no prediction
    or metric rows when that prerequisite fails.
    """

    label_manifest = build_sequence_nn_label_manifest(
        labels=labels,
        eval_contract=eval_contract,
        sequence_manifest=sequence_manifest,
        split_artifact=split_artifact,
        label_registry_path=label_registry_path,
        fingerprint_registry_path=fingerprint_registry_path,
        coherence_audit_path=coherence_audit_path,
        eval_contract_path=eval_contract_path,
        sequence_manifest_path=sequence_manifest_path,
        split_artifact_path=split_artifact_path,
    )
    compliance = build_sequence_nn_eval_contract_compliance(
        labels=labels,
        fingerprints=fingerprints,
        coherence_audit=coherence_audit,
        eval_contract=eval_contract,
        sequence_manifest=sequence_manifest,
        split_artifact=split_artifact,
        label_manifest=label_manifest,
        label_registry_path=label_registry_path,
        fingerprint_registry_path=fingerprint_registry_path,
        coherence_audit_path=coherence_audit_path,
        eval_contract_path=eval_contract_path,
        sequence_manifest_path=sequence_manifest_path,
        split_artifact_path=split_artifact_path,
        label_manifest_out=label_manifest_out,
        predictions_out=predictions_out,
        metrics_out=metrics_out,
        compliance_out=compliance_out,
    )
    return {
        "label_manifest": label_manifest,
        "compliance": compliance,
    }


def build_sequence_nn_label_manifest(
    *,
    labels: list[MechanismLabel],
    eval_contract: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    label_registry_path: Path,
    fingerprint_registry_path: Path,
    coherence_audit_path: Path,
    eval_contract_path: Path,
    sequence_manifest_path: Path,
    split_artifact_path: Path,
) -> dict[str, Any]:
    label_by_entry = {label.entry_id: label for label in labels}
    sequence_rows_by_entry = _rows_by_entry(sequence_manifest)
    split_rows_by_entry = _rows_by_entry(split_artifact)
    primary_fingerprint_ids = _string_list(eval_contract.get("primary_fingerprints"))
    secondary_probe_by_fingerprint = _secondary_probe_by_fingerprint(eval_contract)
    canary_by_entry = _canary_by_entry(eval_contract)

    rows: list[dict[str, Any]] = []
    for label in sorted(labels, key=lambda item: _entry_id_sort_key(item.entry_id)):
        sequence_row = sequence_rows_by_entry.get(label.entry_id, {})
        split_row = split_rows_by_entry.get(label.entry_id, {})
        sequence_records = _sequence_records(sequence_row)
        primary_sequence_record = sequence_records[0] if sequence_records else {}
        oos_tier, oos_source = _oos_tier_for_label(
            label,
            canary_by_entry=canary_by_entry,
            secondary_probe_by_fingerprint=secondary_probe_by_fingerprint,
        )
        probe_role = _probe_role_for_label(
            label,
            oos_tier=oos_tier,
            secondary_probe_by_fingerprint=secondary_probe_by_fingerprint,
        )
        benchmark_role = _benchmark_role_for_label(
            label,
            primary_fingerprint_ids=primary_fingerprint_ids,
            secondary_probe_by_fingerprint=secondary_probe_by_fingerprint,
            oos_tier=oos_tier,
        )
        canary = canary_by_entry.get(label.entry_id, {})
        split_assignment = split_row.get("partition")
        rows.append(
            {
                "entry_id": label.entry_id,
                "label_type": label.label_type,
                "fingerprint_id": label.fingerprint_id,
                "mechanism_fingerprint_id": label.fingerprint_id,
                "benchmark_role": benchmark_role,
                "sequence_id": primary_sequence_record.get("sequence_id"),
                "accession": primary_sequence_record.get("accession"),
                "sequence_sha256": primary_sequence_record.get("sequence_sha256"),
                "sequence_record_count": int(
                    sequence_row.get("sequence_record_count")
                    or len(sequence_records)
                    or 0
                ),
                "sequence_coverage_status": sequence_row.get("coverage_status"),
                "sequence_records": sequence_records,
                "split_assignment": split_assignment,
                "split_assignment_source": (
                    "sequence_distance_holdout_eval_current702_repaired"
                    if split_assignment
                    else None
                ),
                "mmseqs30_subfamily_cluster_id": split_row.get(
                    "real_sequence_identity_cluster_id"
                ),
                "sequence_cluster_id": split_row.get("sequence_cluster_id"),
                "real_sequence_accessions": _string_list(
                    split_row.get("real_sequence_accessions")
                ),
                "oos_tier": oos_tier,
                "oos_tier_assignment_source": oos_source,
                "probe_role": probe_role,
                "canary_expected_eval_role": canary.get("expected_eval_role"),
                "canary_expected_behavior": canary.get("expected_behavior"),
                "canary_reason": canary.get("reason"),
                "manifest_status": (
                    "ready_for_sequence_nn"
                    if sequence_records and split_assignment
                    else "blocked_missing_sequence_or_split"
                ),
            }
        )

    label_ids = set(label_by_entry)
    sequence_ids = set(sequence_rows_by_entry)
    split_ids = set(split_rows_by_entry)
    missing_sequence = sorted(label_ids - sequence_ids, key=_entry_id_sort_key)
    missing_split = sorted(label_ids - split_ids, key=_entry_id_sort_key)
    extra_sequence = sorted(sequence_ids - label_ids, key=_entry_id_sort_key)
    extra_split = sorted(split_ids - label_ids, key=_entry_id_sort_key)
    role_counts = Counter(str(row["benchmark_role"]) for row in rows)
    split_counts = Counter(str(row.get("split_assignment") or "missing") for row in rows)
    oos_tier_counts = Counter(
        str(row.get("oos_tier") or "unknown_oos")
        for row in rows
        if row.get("label_type") == "out_of_scope"
    )
    diagnostic_tier_or_probe_counts = Counter(
        str(row.get("oos_tier") or "not_oos") for row in rows
    )
    status = (
        "blocked_split_incomplete"
        if missing_split
        else "blocked_sequence_manifest_incomplete"
        if missing_sequence
        else "ready_for_sequence_nn"
    )

    return {
        "metadata": {
            "schema_version": "sequence_nn_label_manifest.v1",
            "artifact_id": "v3_sequence_nn_label_manifest_current702_20260525",
            "status": status,
            "current_label_count": len(labels),
            "row_count": len(rows),
            "mechanism_fingerprint_version": eval_contract.get(
                "mechanism_fingerprint_version"
            ),
            "eval_contract_artifact": str(eval_contract_path),
            "eval_contract_sha256": _sha256(eval_contract_path),
            "sequence_manifest_artifact": str(sequence_manifest_path),
            "sequence_manifest_sha256": _sha256(sequence_manifest_path),
            "split_artifact": str(split_artifact_path),
            "split_artifact_sha256": _sha256(split_artifact_path),
            "label_registry_artifact": str(label_registry_path),
            "label_registry_sha256": _sha256(label_registry_path),
            "fingerprint_registry_artifact": str(fingerprint_registry_path),
            "fingerprint_registry_sha256": _sha256(fingerprint_registry_path),
            "coherence_audit_artifact": str(coherence_audit_path),
            "coherence_audit_sha256": _sha256(coherence_audit_path),
            "primary_fingerprint_ids": primary_fingerprint_ids,
            "secondary_ood_probe_fingerprint_ids": list(
                secondary_probe_by_fingerprint
            ),
            "label_registry_edited": False,
            "model_training_performed": False,
            "plm_embeddings_computed": False,
            "leakage_contract": "no EC/name/prose/expert-note predictive features",
            "sequence_manifest_missing_entry_count": len(missing_sequence),
            "sequence_manifest_missing_entry_ids": missing_sequence,
            "split_assignment_missing_entry_count": len(missing_split),
            "split_assignment_missing_entry_ids": missing_split,
            "extra_sequence_manifest_entry_count": len(extra_sequence),
            "extra_sequence_manifest_entry_ids": extra_sequence,
            "extra_split_entry_count": len(extra_split),
            "extra_split_entry_ids": extra_split,
            "benchmark_role_counts": dict(sorted(role_counts.items())),
            "split_assignment_counts": dict(sorted(split_counts.items())),
            "out_of_scope_tier_counts": dict(sorted(oos_tier_counts.items())),
            "diagnostic_tier_or_probe_counts": dict(
                sorted(diagnostic_tier_or_probe_counts.items())
            ),
        },
        "rows": rows,
    }


def build_sequence_nn_eval_contract_compliance(
    *,
    labels: list[MechanismLabel],
    fingerprints: list[Any],
    coherence_audit: dict[str, Any],
    eval_contract: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    label_manifest: dict[str, Any],
    label_registry_path: Path,
    fingerprint_registry_path: Path,
    coherence_audit_path: Path,
    eval_contract_path: Path,
    sequence_manifest_path: Path,
    split_artifact_path: Path,
    label_manifest_out: Path,
    predictions_out: Path,
    metrics_out: Path,
    compliance_out: Path,
) -> dict[str, Any]:
    del fingerprint_registry_path, coherence_audit_path, compliance_out
    manifest_metadata = label_manifest.get("metadata", {})
    sequence_metadata = sequence_manifest.get("metadata", {})
    split_metadata = split_artifact.get("metadata", {})
    primary_fingerprint_ids = _string_list(eval_contract.get("primary_fingerprints"))
    secondary_probe_ids = [
        str(row.get("fingerprint_id"))
        for row in eval_contract.get("secondary_ood_probe_fingerprints", [])
        if isinstance(row, dict) and row.get("fingerprint_id")
    ]
    blockers = _sequence_nn_blockers(
        labels=labels,
        fingerprints=fingerprints,
        coherence_audit=coherence_audit,
        eval_contract=eval_contract,
        sequence_manifest=sequence_manifest,
        split_artifact=split_artifact,
        label_manifest=label_manifest,
    )
    status = "blocked_before_sequence_nn_metrics" if blockers else "ready_for_sequence_nn_metrics"
    split_missing = _string_list(
        manifest_metadata.get("split_assignment_missing_entry_ids")
    )
    sequence_missing = _string_list(
        manifest_metadata.get("sequence_manifest_missing_entry_ids")
    )
    split_counts = manifest_metadata.get("split_assignment_counts", {})
    canary_ids = [
        str(row.get("entry_id"))
        for row in eval_contract.get("canary_examples", {}).get("examples", [])
        if isinstance(row, dict) and row.get("entry_id")
    ]
    split_missing_canaries = sorted(set(canary_ids) & set(split_missing), key=_entry_id_sort_key)

    return {
        "metadata": {
            "schema_version": "sequence_nn_eval_contract_compliance.v1",
            "artifact_id": "v3_sequence_nn_eval_contract_compliance_current702_20260525",
            "status": status,
            "current_label_count": len(labels),
            "mechanism_fingerprint_version": eval_contract.get(
                "mechanism_fingerprint_version"
            ),
            "eval_contract_artifact": str(eval_contract_path),
            "eval_contract_sha256": _sha256(eval_contract_path),
            "sequence_manifest_artifact": str(sequence_manifest_path),
            "sequence_manifest_sha256": _sha256(sequence_manifest_path),
            "split_artifact": str(split_artifact_path),
            "split_artifact_sha256": _sha256(split_artifact_path),
            "label_registry_artifact": str(label_registry_path),
            "label_registry_sha256": _sha256(label_registry_path),
            "label_manifest_artifact": str(label_manifest_out),
            "predictions_artifact_blocked": str(predictions_out),
            "metrics_artifact_blocked": str(metrics_out),
            "backend_tool_version": split_metadata.get("backend_version"),
            "backend_name": split_metadata.get("backend"),
            "primary_fingerprint_ids": primary_fingerprint_ids,
            "secondary_ood_probe_fingerprint_ids": secondary_probe_ids,
            "out_of_scope_tier_counts": manifest_metadata.get(
                "out_of_scope_tier_counts", {}
            ),
            "leakage_contract": "no EC/name/prose/expert-note predictive features",
            "label_registry_edited": False,
            "model_training_performed": False,
            "plm_embeddings_computed": False,
            "prediction_metrics_reported": False,
        },
        "blockers": blockers,
        "coverage_summary": {
            "label_manifest_row_count": manifest_metadata.get("row_count"),
            "sequence_covered_label_count": sequence_metadata.get(
                "sequence_covered_label_count"
            ),
            "sequence_manifest_missing_entry_count": len(sequence_missing),
            "sequence_manifest_missing_entry_ids": sequence_missing,
            "split_assignment_covered_label_count": len(labels) - len(split_missing),
            "split_assignment_missing_entry_count": len(split_missing),
            "split_assignment_missing_entry_ids": split_missing,
            "split_assignment_counts": split_counts,
        },
        "split_quality_summary": {
            "split_artifact_complete_for_current702": not split_missing,
            "split_artifact_label_registry_count": split_metadata.get(
                "label_registry_count"
            ),
            "split_artifact_evaluated_count": split_metadata.get("evaluated_count"),
            "heldout_count": split_metadata.get("heldout_count"),
            "in_distribution_count": split_metadata.get("in_distribution_count"),
            "sequence_identity_backend_available": split_metadata.get(
                "sequence_identity_backend_available"
            ),
            "sequence_identity_target_achieved": split_metadata.get(
                "sequence_identity_target_achieved"
            ),
            "max_observed_train_test_identity": split_metadata.get(
                "max_observed_train_test_identity"
            ),
            "sequence_missing_entry_count": split_metadata.get(
                "sequence_missing_entry_count"
            ),
            "partition_rule": split_metadata.get("partition_rule"),
        },
        "primary_seed_metrics": {
            "status": "not_reported_split_blocked" if blockers else "not_computed",
            "reason": "sequence-NN metrics require split assignments for all current702 labels",
        },
        "per_fingerprint_metrics": {
            fingerprint_id: {
                "status": "not_reported_split_blocked" if blockers else "not_computed"
            }
            for fingerprint_id in primary_fingerprint_ids
        },
        "oos_abstention_diagnostics": {
            "status": "not_reported_split_blocked" if blockers else "not_computed",
            "tiers_required": ["far_oos", "near_oos", "boundary_oos", "unknown_oos"],
            "secondary_probe_fingerprint_ids": secondary_probe_ids,
        },
        "diversity_stratified_accuracy": {
            "status": "not_reported_split_blocked" if blockers else "not_computed",
            "required_axis": (
                eval_contract.get("diversity_stratified_accuracy_policy", {})
                .get("primary_diversity_axis", {})
                .get("name")
            ),
        },
        "canary_predictions": {
            "status": "not_reported_split_blocked" if blockers else "not_computed",
            "canary_count": len(canary_ids),
            "split_missing_canary_entry_count": len(split_missing_canaries),
            "split_missing_canary_entry_ids": split_missing_canaries,
        },
        "failure_modes_and_next_actions": [
            {
                "failure_mode": "current702_split_rows_do_not_cover_label_manifest",
                "affected_entry_ids": split_missing,
                "next_action": (
                    "regenerate or repair the current702 sequence split so every "
                    "sequence-manifest row has a partition before running MMseqs "
                    "nearest-neighbor predictions"
                ),
            }
        ]
        if blockers
        else [],
        "blocked_outputs": {
            "predictions_jsonl": str(predictions_out),
            "metrics_json": str(metrics_out),
            "reason": "not written because split completeness gate failed",
        },
    }


def _sequence_nn_blockers(
    *,
    labels: list[MechanismLabel],
    fingerprints: list[Any],
    coherence_audit: dict[str, Any],
    eval_contract: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    label_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    manifest_metadata = label_manifest.get("metadata", {})
    sequence_metadata = sequence_manifest.get("metadata", {})
    split_metadata = split_artifact.get("metadata", {})
    label_count = len(labels)
    if sequence_metadata.get("current_label_count") != label_count:
        blockers.append(
            {
                "reason": "sequence_manifest_current_label_count_mismatch",
                "observed": sequence_metadata.get("current_label_count"),
                "expected": label_count,
            }
        )
    if sequence_metadata.get("missing_sequence_entry_count") not in {0, None}:
        blockers.append(
            {
                "reason": "sequence_manifest_reports_missing_sequences",
                "missing_entry_ids": sequence_metadata.get(
                    "missing_sequence_entry_ids", []
                ),
            }
        )
    if split_metadata.get("label_registry_count") != label_count:
        blockers.append(
            {
                "reason": "split_artifact_label_registry_count_mismatch",
                "observed": split_metadata.get("label_registry_count"),
                "expected": label_count,
            }
        )
    if split_metadata.get("sequence_identity_target_achieved") is not True:
        blockers.append(
            {
                "reason": "split_artifact_sequence_identity_target_not_achieved",
                "observed": split_metadata.get("sequence_identity_target_achieved"),
            }
        )
    missing_split_ids = _string_list(
        manifest_metadata.get("split_assignment_missing_entry_ids")
    )
    if missing_split_ids:
        blockers.append(
            {
                "reason": "split_artifact_missing_current_label_rows",
                "missing_entry_count": len(missing_split_ids),
                "missing_entry_ids": missing_split_ids,
                "observed_split_row_count": len(split_artifact.get("rows", []) or []),
                "expected_label_manifest_row_count": label_count,
            }
        )
    missing_sequence_ids = _string_list(
        manifest_metadata.get("sequence_manifest_missing_entry_ids")
    )
    if missing_sequence_ids:
        blockers.append(
            {
                "reason": "sequence_manifest_missing_current_label_rows",
                "missing_entry_count": len(missing_sequence_ids),
                "missing_entry_ids": missing_sequence_ids,
            }
        )
    expected_primary = _string_list(eval_contract.get("primary_fingerprints"))
    observed_primary = _string_list(
        coherence_audit.get("fingerprints_kept_for_primary_metric")
    )
    if observed_primary and expected_primary and observed_primary != expected_primary:
        blockers.append(
            {
                "reason": "coherence_audit_primary_fingerprints_mismatch_contract",
                "observed": observed_primary,
                "expected": expected_primary,
            }
        )
    fingerprint_count = len(fingerprints)
    if fingerprint_count != 8:
        blockers.append(
            {
                "reason": "fingerprint_registry_count_mismatch",
                "observed": fingerprint_count,
                "expected": 8,
            }
        )
    return blockers


def _rows_by_entry(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in artifact.get("rows", []) or []:
        if not isinstance(row, dict) or not row.get("entry_id"):
            continue
        rows[str(row["entry_id"])] = row
    return rows


def _sequence_records(sequence_row: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for record in sequence_row.get("sequence_records", []) or []:
        if not isinstance(record, dict):
            continue
        sequence_id = record.get("accession_or_structure_id")
        records.append(
            {
                "sequence_id": sequence_id,
                "accession": sequence_id,
                "sequence_sha256": record.get("sequence_sha256"),
                "sequence_length": record.get("sequence_length"),
                "sequence_source_type": record.get("sequence_source_type"),
            }
        )
    return sorted(
        records,
        key=lambda row: (
            str(row.get("sequence_id") or ""),
            str(row.get("sequence_sha256") or ""),
        ),
    )


def _benchmark_role_for_label(
    label: MechanismLabel,
    *,
    primary_fingerprint_ids: list[str],
    secondary_probe_by_fingerprint: dict[str, dict[str, Any]],
    oos_tier: str | None,
) -> str:
    if label.label_type == "out_of_scope":
        return f"{OOS_BENCHMARK_PREFIX}::{oos_tier or 'unknown_oos'}"
    if label.fingerprint_id in primary_fingerprint_ids:
        return f"{PRIMARY_BENCHMARK_PREFIX}::{label.fingerprint_id}"
    if label.fingerprint_id in secondary_probe_by_fingerprint:
        return f"{SECONDARY_BENCHMARK_PREFIX}::{label.fingerprint_id}"
    return "unsupported_fingerprint_or_label_role"


def _oos_tier_for_label(
    label: MechanismLabel,
    *,
    canary_by_entry: dict[str, dict[str, Any]],
    secondary_probe_by_fingerprint: dict[str, dict[str, Any]],
) -> tuple[str | None, str | None]:
    if label.fingerprint_id in secondary_probe_by_fingerprint:
        row = secondary_probe_by_fingerprint[str(label.fingerprint_id)]
        return str(row.get("oos_tier") or "unknown_oos"), "eval_contract_secondary_probe"
    if label.label_type != "out_of_scope":
        return None, None
    expected_role = str(canary_by_entry.get(label.entry_id, {}).get("expected_eval_role") or "")
    if expected_role.startswith(f"{OOS_BENCHMARK_PREFIX}::"):
        return expected_role.split("::", 1)[1], "eval_contract_oos_canary"
    return "unknown_oos", "fail_closed_unknown_full_oos_tier_assignment_pending"


def _probe_role_for_label(
    label: MechanismLabel,
    *,
    oos_tier: str | None,
    secondary_probe_by_fingerprint: dict[str, dict[str, Any]],
) -> str | None:
    if label.fingerprint_id in secondary_probe_by_fingerprint:
        return str(
            secondary_probe_by_fingerprint[str(label.fingerprint_id)].get("probe_role")
            or ""
        )
    if label.label_type == "out_of_scope":
        return f"{oos_tier or 'unknown_oos'}_abstention_diagnostic"
    return None


def _secondary_probe_by_fingerprint(eval_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row["fingerprint_id"]): row
        for row in eval_contract.get("secondary_ood_probe_fingerprints", []) or []
        if isinstance(row, dict) and row.get("fingerprint_id")
    }


def _canary_by_entry(eval_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row["entry_id"]): row
        for row in eval_contract.get("canary_examples", {}).get("examples", []) or []
        if isinstance(row, dict) and row.get("entry_id")
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([A-Za-z_]+):(\d+)", str(entry_id))
    if match:
        return (match.group(1), int(match.group(2)), "")
    prefix, _, suffix = str(entry_id).partition(":")
    return (prefix, 10**9, suffix)
