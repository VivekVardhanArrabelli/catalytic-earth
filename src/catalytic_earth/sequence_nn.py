from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .generalization import (
    _compute_mmseqs_train_test_identity,
    _real_sequence_identity_split,
)
from .labels import MechanismLabel


PRIMARY_BENCHMARK_PREFIX = "primary_supervised_metric"
SECONDARY_BENCHMARK_PREFIX = "secondary_ood_probe"
OOS_BENCHMARK_PREFIX = "oos_tier"
SEQUENCE_NN_MODEL_ID = "deterministic_3mer_jaccard_sequence_nn.v1"
SEQUENCE_NN_KMER_SIZE = 3


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
    artifacts: dict[str, Any] = {
        "label_manifest": label_manifest,
        "compliance": compliance,
    }
    if not compliance.get("blockers"):
        predictions, metrics = build_sequence_nn_predictions_and_metrics(
            label_manifest=label_manifest,
            sequence_manifest=sequence_manifest,
            split_artifact=split_artifact,
            eval_contract=eval_contract,
            label_manifest_out=label_manifest_out,
            predictions_out=predictions_out,
            metrics_out=metrics_out,
            sequence_manifest_path=sequence_manifest_path,
            split_artifact_path=split_artifact_path,
        )
        compliance = _attach_sequence_nn_metrics_to_compliance(
            compliance=compliance,
            metrics=metrics,
            predictions_out=predictions_out,
            metrics_out=metrics_out,
        )
        artifacts["compliance"] = compliance
        artifacts["predictions"] = predictions
        artifacts["metrics"] = metrics
    return artifacts


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
    missing_split_details = _missing_split_details(
        label_manifest=label_manifest,
        missing_entry_ids=split_missing,
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
        "split_assignment_blocker": {
            "status": "blocked_split_incomplete" if split_missing else "passed",
            "reason": (
                "repaired current702 sequence split does not cover every label row"
                if split_missing
                else None
            ),
            "split_artifact_row_count": len(split_artifact.get("rows", []) or []),
            "expected_label_manifest_row_count": len(labels),
            "split_artifact_evaluated_count": split_metadata.get("evaluated_count"),
            "split_artifact_sequence_entry_coverage_count": split_metadata.get(
                "sequence_entry_coverage_count"
            ),
            "split_artifact_sequence_missing_entry_count": split_metadata.get(
                "sequence_missing_entry_count"
            ),
            "missing_current_label_row_count": len(split_missing),
            "missing_current_label_rows": missing_split_details,
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
                "affected_rows": missing_split_details,
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


def repair_sequence_split_assignments(
    *,
    label_manifest: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    split_artifact_path: Path,
    repaired_split_out: Path,
    repair_out: Path,
    sequence_identity_threshold: float = 0.30,
    sequence_identity_coverage: float = 0.80,
    mmseqs_binary: str = "mmseqs",
) -> dict[str, Any]:
    """Repair current-label split assignments for sequence-covered non-eval rows.

    The sequence-distance holdout artifact is produced from geometry retrieval
    rows. This repair keeps the original retrieval metrics intact while adding
    split-assignment rows for current labels that have sequence coverage but no
    geometry retrieval row, then rechecks the sequence-hard train/test identity.
    """

    label_rows = _rows_by_entry(label_manifest)
    sequence_rows = _rows_by_entry(sequence_manifest)
    split_rows = _rows_by_entry(split_artifact)
    missing_entry_ids = sorted(set(label_rows) - set(split_rows), key=_entry_id_sort_key)
    split_metadata = split_artifact.get("metadata", {})
    sequence_fasta = _sequence_fasta_path_from_source(split_metadata.get("sequence_source"))
    root_cause = {
        entry_id: (
            "split artifact writer builds rows from geometry retrieval results; "
            "this current-label row has repaired sequence coverage but no "
            "geometry retrieval result row, so it was omitted from split rows"
        )
        for entry_id in missing_entry_ids
    }

    before = {
        "path": str(split_artifact_path),
        "sha256": _sha256(split_artifact_path),
        "row_count": len(split_artifact.get("rows", []) or []),
        "label_registry_count": split_metadata.get("label_registry_count"),
        "sequence_entry_coverage_count": split_metadata.get(
            "sequence_entry_coverage_count"
        ),
        "sequence_missing_entry_count": split_metadata.get(
            "sequence_missing_entry_count"
        ),
        "heldout_count": split_metadata.get("heldout_count"),
        "in_distribution_count": split_metadata.get("in_distribution_count"),
        "max_observed_train_test_identity": split_metadata.get(
            "max_observed_train_test_identity"
        ),
        "sequence_identity_target_achieved": split_metadata.get(
            "sequence_identity_target_achieved"
        ),
        "missing_label_manifest_entry_count": len(missing_entry_ids),
        "missing_label_manifest_entry_ids": missing_entry_ids,
    }

    repair_artifact: dict[str, Any] = {
        "metadata": {
            "schema_version": "sequence_split_assignment_repair.v1",
            "artifact_id": "v3_sequence_split_assignment_repair_current702_20260525",
            "status": "blocked_before_repair",
            "label_registry_edited": False,
            "model_training_performed": False,
            "plm_embeddings_computed": False,
            "leakage_contract": "no EC/name/prose/expert-note predictive features",
        },
        "repaired_entry_ids": missing_entry_ids,
        "root_cause_by_entry": root_cause,
        "split_assignment_by_entry": {},
        "split_artifact_before": before,
        "split_artifact_after": {
            "path": str(repaired_split_out),
            "sha256": None,
        },
        "max_observed_train_test_identity_before": split_metadata.get(
            "max_observed_train_test_identity"
        ),
        "max_observed_train_test_identity_after": None,
        "sequence_identity_target_achieved": False,
        "label_registry_edited": False,
        "blockers": [],
    }
    if not missing_entry_ids:
        repaired_split = copy.deepcopy(split_artifact)
        repair_artifact["metadata"]["status"] = "no_missing_split_assignments"
        repair_artifact["sequence_identity_target_achieved"] = bool(
            split_metadata.get("sequence_identity_target_achieved")
        )
        repair_artifact["max_observed_train_test_identity_after"] = split_metadata.get(
            "max_observed_train_test_identity"
        )
        return {"repaired_split": repaired_split, "repair": repair_artifact}
    if not sequence_fasta:
        repair_artifact["metadata"]["status"] = "blocked_sequence_fasta_not_resolved"
        repair_artifact["blockers"].append("split_artifact_sequence_source_fasta_missing")
        return {"repaired_split": copy.deepcopy(split_artifact), "repair": repair_artifact}

    sequence_rows_for_clustering = [
        {
            "entry_id": entry_id,
            "reference_uniprot_ids": _sequence_manifest_reference_accessions(
                entry_id=entry_id,
                sequence_row=sequence_rows.get(entry_id, {}),
                split_row=split_rows.get(entry_id, {}),
            ),
        }
        for entry_id in sorted(label_rows, key=_entry_id_sort_key)
    ]
    real_split = _real_sequence_identity_split(
        rows=sequence_rows_for_clustering,
        sequence_rows_by_entry={},
        sequence_fasta=sequence_fasta,
        slice_id="current702_split_assignment_repair",
        backend="mmseqs",
        threshold=sequence_identity_threshold,
        coverage=sequence_identity_coverage,
        mmseqs_binary=mmseqs_binary,
    )
    if not real_split.get("usable"):
        repair_artifact["metadata"]["status"] = "blocked_sequence_identity_clustering_failed"
        repair_artifact["blockers"].append(
            real_split.get("fallback_backend")
            or "sequence_identity_clustering_unavailable"
        )
        repair_artifact["sequence_identity_cluster_metadata"] = _public_real_split_metadata(
            real_split
        )
        return {"repaired_split": copy.deepcopy(split_artifact), "repair": repair_artifact}

    existing_partitions_by_cluster: dict[str, set[str]] = defaultdict(set)
    existing_entries_by_cluster: dict[str, list[str]] = defaultdict(list)
    for entry_id, row in split_rows.items():
        cluster_id = real_split["entry_clusters"].get(entry_id)
        partition = row.get("partition")
        if cluster_id and partition in {"heldout", "in_distribution"}:
            existing_partitions_by_cluster[cluster_id].add(str(partition))
            existing_entries_by_cluster[cluster_id].append(entry_id)

    repaired_rows = list(copy.deepcopy(split_artifact.get("rows", []) or []))
    split_assignment_by_entry: dict[str, dict[str, Any]] = {}
    blockers: list[str] = []
    for entry_id in missing_entry_ids:
        cluster_id = real_split["entry_clusters"].get(entry_id)
        if not cluster_id:
            blockers.append(f"missing_mmseqs_cluster_for:{entry_id}")
            continue
        cluster_partitions = sorted(existing_partitions_by_cluster.get(cluster_id, set()))
        if len(cluster_partitions) > 1:
            blockers.append(f"cluster_spans_existing_partitions:{entry_id}:{cluster_id}")
            continue
        partition = "heldout" if cluster_partitions == ["heldout"] else "in_distribution"
        assignment = {
            "entry_id": entry_id,
            "partition": partition,
            "real_sequence_identity_cluster_id": cluster_id,
            "cluster_existing_partitions": cluster_partitions,
            "cluster_existing_entry_ids": sorted(
                existing_entries_by_cluster.get(cluster_id, []),
                key=_entry_id_sort_key,
            ),
            "sequence_accessions": real_split["sequence_accessions_by_entry"].get(
                entry_id, []
            ),
            "sequence_record_count": real_split[
                "sequence_record_counts_by_entry"
            ].get(entry_id, 0),
            "assignment_rule": (
                "inherit_heldout_when_cluster_already_heldout_else_in_distribution"
            ),
        }
        split_assignment_by_entry[entry_id] = assignment
        repaired_rows.append(
            _split_assignment_repair_row(
                entry_id=entry_id,
                label_row=label_rows.get(entry_id, {}),
                sequence_row=sequence_rows.get(entry_id, {}),
                assignment=assignment,
            )
        )

    if blockers:
        repair_artifact["metadata"]["status"] = "blocked_split_assignment_repair"
        repair_artifact["blockers"] = blockers
        repair_artifact["split_assignment_by_entry"] = split_assignment_by_entry
        return {"repaired_split": copy.deepcopy(split_artifact), "repair": repair_artifact}

    heldout_entry_ids = {
        str(row.get("entry_id"))
        for row in repaired_rows
        if isinstance(row, dict) and row.get("partition") == "heldout"
    }
    train_test_identity = _compute_mmseqs_train_test_identity(
        records_by_id=real_split["records_by_id"],
        heldout_entry_ids=heldout_entry_ids,
        slice_id="current702_split_assignment_repair",
        threshold=sequence_identity_threshold,
        coverage=sequence_identity_coverage,
        mmseqs_binary=mmseqs_binary,
        prior_commands=real_split.get("backend_commands", []),
    )
    target_achieved = _identity_target_achieved(
        train_test_identity=train_test_identity,
        threshold=sequence_identity_threshold,
    )
    partition_counts = _partition_counts(repaired_rows)
    repaired_split = copy.deepcopy(split_artifact)
    repaired_split["rows"] = sorted(
        repaired_rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id")))
    )
    repaired_metadata = copy.deepcopy(split_metadata)
    repaired_metadata.update(
        {
            "artifact_id": (
                "v3_sequence_distance_holdout_eval_1025_current702_"
                "split_assignment_repaired_20260525"
            ),
            "source_split_artifact": str(split_artifact_path),
            "source_split_artifact_sha256": before["sha256"],
            "split_assignment_repair_artifact": str(repair_out),
            "split_assignment_row_count": len(repaired_rows),
            "split_assignment_repaired_entry_count": len(missing_entry_ids),
            "split_assignment_repaired_entry_ids": missing_entry_ids,
            "non_evaluated_split_assignment_repair_count": len(missing_entry_ids),
            "metric_evaluated_count": split_metadata.get("evaluated_count"),
            "evaluated_count": len(repaired_rows),
            "heldout_count": partition_counts.get("heldout", 0),
            "in_distribution_count": partition_counts.get("in_distribution", 0),
            "sequence_entry_coverage_count": real_split.get(
                "sequence_entry_coverage_count"
            ),
            "sequence_missing_entry_count": real_split.get(
                "sequence_missing_entry_count"
            ),
            "sequence_missing_entry_ids": real_split.get("sequence_missing_entry_ids", []),
            "real_sequence_identity_record_cluster_count": real_split.get(
                "record_cluster_count"
            ),
            "real_sequence_identity_entry_cluster_count": real_split.get(
                "entry_cluster_count"
            ),
            "heldout_entry_ids": sorted(heldout_entry_ids, key=_entry_id_sort_key),
            "heldout_cluster_ids": sorted(
                {
                    str(real_split["entry_clusters"].get(entry_id))
                    for entry_id in heldout_entry_ids
                    if real_split["entry_clusters"].get(entry_id)
                }
            ),
            "max_observed_train_test_identity": train_test_identity.get(
                "max_observed_train_test_identity"
            ),
            "max_observed_train_test_identity_computable": bool(
                train_test_identity.get("max_observed_train_test_identity_computable")
            ),
            "max_observed_train_test_identity_alignment_count": train_test_identity.get(
                "max_observed_train_test_identity_alignment_count", 0
            ),
            "target_identity_achieved": target_achieved,
            "sequence_identity_target_achieved": target_achieved,
            "backend_command": real_split.get("backend_command"),
            "backend_commands": train_test_identity.get(
                "backend_commands", real_split.get("backend_commands", [])
            ),
            "backend_resolved_path": real_split.get("backend_resolved_path"),
            "backend_version": real_split.get("backend_version"),
            "partition_notes": list(split_metadata.get("partition_notes", []) or [])
            + [
                "non-evaluated current-label rows with repaired sequences were "
                "assigned by whole MMseqs cluster; singleton/new clusters were "
                "assigned in_distribution"
            ],
            "split_assignment_counts": partition_counts,
            "geometry_metric_rows_exclude_non_evaluated_split_repairs": True,
        }
    )
    repaired_split["metadata"] = repaired_metadata

    repair_artifact["metadata"]["status"] = (
        "repaired" if target_achieved else "blocked_sequence_identity_target_failed"
    )
    repair_artifact["split_assignment_by_entry"] = split_assignment_by_entry
    repair_artifact["split_artifact_after"].update(
        {
            "row_count": len(repaired_rows),
            "label_registry_count": repaired_metadata.get("label_registry_count"),
            "sequence_entry_coverage_count": repaired_metadata.get(
                "sequence_entry_coverage_count"
            ),
            "sequence_missing_entry_count": repaired_metadata.get(
                "sequence_missing_entry_count"
            ),
            "heldout_count": repaired_metadata.get("heldout_count"),
            "in_distribution_count": repaired_metadata.get("in_distribution_count"),
        }
    )
    repair_artifact["max_observed_train_test_identity_after"] = train_test_identity.get(
        "max_observed_train_test_identity"
    )
    repair_artifact["sequence_identity_target_achieved"] = target_achieved
    repair_artifact["sequence_identity_cluster_metadata"] = _public_real_split_metadata(
        real_split
    )
    if not target_achieved:
        repair_artifact["blockers"].append(
            "adding repaired rows would violate the <=0.30 train/test sequence identity target"
        )
    return {"repaired_split": repaired_split, "repair": repair_artifact}


def build_sequence_nn_predictions_and_metrics(
    *,
    label_manifest: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    eval_contract: dict[str, Any],
    label_manifest_out: Path,
    predictions_out: Path,
    metrics_out: Path,
    sequence_manifest_path: Path,
    split_artifact_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest_rows = [
        row
        for row in label_manifest.get("rows", []) or []
        if isinstance(row, dict) and row.get("entry_id")
    ]
    sequence_fasta = _sequence_fasta_path_from_source(
        split_artifact.get("metadata", {}).get("sequence_source")
    )
    fasta_sequences = _load_sequence_nn_fasta_sequences(sequence_fasta)
    prepared: list[dict[str, Any]] = []
    missing_sequence_entry_ids: list[str] = []
    for row in manifest_rows:
        sequence = _sequence_for_manifest_row(row, fasta_sequences)
        if not sequence:
            missing_sequence_entry_ids.append(str(row["entry_id"]))
            continue
        prepared.append(
            {
                "entry_id": str(row["entry_id"]),
                "split_assignment": str(row.get("split_assignment") or ""),
                "label_type": row.get("label_type"),
                "fingerprint_id": row.get("fingerprint_id"),
                "label_group": _label_group_from_manifest_row(row),
                "benchmark_role": row.get("benchmark_role"),
                "oos_tier": row.get("oos_tier"),
                "probe_role": row.get("probe_role"),
                "mmseqs30_subfamily_cluster_id": row.get(
                    "mmseqs30_subfamily_cluster_id"
                ),
                "sequence_id": row.get("sequence_id"),
                "sequence_sha256": row.get("sequence_sha256"),
                "kmers": _kmers(sequence, SEQUENCE_NN_KMER_SIZE),
            }
        )

    train_rows = [
        row for row in prepared if row["split_assignment"] == "in_distribution"
    ]
    heldout_rows = [row for row in prepared if row["split_assignment"] == "heldout"]
    predictions: list[dict[str, Any]] = []
    if train_rows and heldout_rows:
        for heldout in sorted(heldout_rows, key=lambda row: _entry_id_sort_key(row["entry_id"])):
            nearest = _nearest_kmer_train_row(heldout, train_rows)
            similarity = _jaccard(heldout["kmers"], nearest["kmers"])
            predicted_label_group = nearest["label_group"]
            true_label_group = heldout["label_group"]
            out_of_scope = true_label_group == "out_of_scope"
            predicted_fingerprint = (
                None if predicted_label_group == "out_of_scope" else predicted_label_group
            )
            predictions.append(
                {
                    "schema_version": "sequence_nn_prediction.v1",
                    "model_id": SEQUENCE_NN_MODEL_ID,
                    "entry_id": heldout["entry_id"],
                    "split_assignment": heldout["split_assignment"],
                    "benchmark_role": heldout["benchmark_role"],
                    "label_type": heldout["label_type"],
                    "true_fingerprint_id": heldout["fingerprint_id"],
                    "true_label_group": true_label_group,
                    "oos_tier": heldout["oos_tier"],
                    "probe_role": heldout["probe_role"],
                    "sequence_id": heldout["sequence_id"],
                    "sequence_sha256": heldout["sequence_sha256"],
                    "nearest_train_entry_id": nearest["entry_id"],
                    "nearest_train_label_group": nearest["label_group"],
                    "nearest_train_fingerprint_id": nearest["fingerprint_id"],
                    "nearest_train_benchmark_role": nearest["benchmark_role"],
                    "nearest_train_mmseqs30_subfamily_cluster_id": nearest.get(
                        "mmseqs30_subfamily_cluster_id"
                    ),
                    "jaccard_similarity": round(similarity, 4),
                    "predicted_label_group": predicted_label_group,
                    "predicted_fingerprint_id": predicted_fingerprint,
                    "abstained": predicted_label_group == "out_of_scope",
                    "exact_label_match": true_label_group == predicted_label_group,
                    "top1_correct": (
                        bool(heldout["fingerprint_id"])
                        and heldout["fingerprint_id"] == predicted_fingerprint
                    ),
                    "out_of_scope_false_positive": (
                        out_of_scope and predicted_label_group != "out_of_scope"
                    ),
                    "predictive_inputs": ["amino_acid_sequence_only"],
                    "forbidden_inputs_used": [],
                }
            )

    metrics = _sequence_nn_metrics(
        predictions=predictions,
        prepared_rows=prepared,
        train_rows=train_rows,
        heldout_rows=heldout_rows,
        missing_sequence_entry_ids=missing_sequence_entry_ids,
        label_manifest=label_manifest,
        sequence_manifest=sequence_manifest,
        split_artifact=split_artifact,
        eval_contract=eval_contract,
        label_manifest_out=label_manifest_out,
        predictions_out=predictions_out,
        metrics_out=metrics_out,
        sequence_manifest_path=sequence_manifest_path,
        split_artifact_path=split_artifact_path,
        sequence_fasta=sequence_fasta,
    )
    return predictions, metrics


def _attach_sequence_nn_metrics_to_compliance(
    *,
    compliance: dict[str, Any],
    metrics: dict[str, Any],
    predictions_out: Path,
    metrics_out: Path,
) -> dict[str, Any]:
    updated = copy.deepcopy(compliance)
    metadata = updated.setdefault("metadata", {})
    metadata["status"] = "sequence_nn_metrics_reported"
    metadata["prediction_metrics_reported"] = True
    metadata["predictions_artifact"] = str(predictions_out)
    metadata["metrics_artifact"] = str(metrics_out)
    metadata.pop("predictions_artifact_blocked", None)
    metadata.pop("metrics_artifact_blocked", None)
    updated["primary_seed_metrics"] = metrics.get("primary_seed_metrics", {})
    updated["per_fingerprint_metrics"] = metrics.get("per_fingerprint_metrics", {})
    updated["oos_abstention_diagnostics"] = metrics.get(
        "oos_abstention_diagnostics", {}
    )
    updated["diversity_stratified_accuracy"] = metrics.get(
        "diversity_stratified_accuracy", {}
    )
    updated["canary_predictions"] = metrics.get("canary_predictions", {})
    updated["failure_modes_and_next_actions"] = []
    updated["blocked_outputs"] = {}
    return updated


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


def _missing_split_details(
    *,
    label_manifest: dict[str, Any],
    missing_entry_ids: list[str],
) -> list[dict[str, Any]]:
    manifest_rows = {
        str(row.get("entry_id")): row
        for row in label_manifest.get("rows", []) or []
        if isinstance(row, dict) and row.get("entry_id")
    }
    details: list[dict[str, Any]] = []
    for entry_id in sorted(missing_entry_ids, key=_entry_id_sort_key):
        row = manifest_rows.get(entry_id, {})
        details.append(
            {
                "entry_id": entry_id,
                "label_type": row.get("label_type"),
                "fingerprint_id": row.get("fingerprint_id"),
                "benchmark_role": row.get("benchmark_role"),
                "sequence_id": row.get("sequence_id"),
                "accession": row.get("accession"),
                "sequence_sha256": row.get("sequence_sha256"),
                "sequence_coverage_status": row.get("sequence_coverage_status"),
                "sequence_record_count": row.get("sequence_record_count"),
                "oos_tier": row.get("oos_tier"),
                "probe_role": row.get("probe_role"),
                "manifest_status": row.get("manifest_status"),
                "blocker": "missing_partition_in_split_artifact",
            }
        )
    return details


def _sequence_nn_metrics(
    *,
    predictions: list[dict[str, Any]],
    prepared_rows: list[dict[str, Any]],
    train_rows: list[dict[str, Any]],
    heldout_rows: list[dict[str, Any]],
    missing_sequence_entry_ids: list[str],
    label_manifest: dict[str, Any],
    sequence_manifest: dict[str, Any],
    split_artifact: dict[str, Any],
    eval_contract: dict[str, Any],
    label_manifest_out: Path,
    predictions_out: Path,
    metrics_out: Path,
    sequence_manifest_path: Path,
    split_artifact_path: Path,
    sequence_fasta: str | None,
) -> dict[str, Any]:
    primary_fingerprints = _string_list(eval_contract.get("primary_fingerprints"))
    prediction_by_entry = {row["entry_id"]: row for row in predictions}
    primary_predictions = [
        row
        for row in predictions
        if row.get("benchmark_role", "").startswith(f"{PRIMARY_BENCHMARK_PREFIX}::")
    ]
    in_scope_predictions = [
        row for row in predictions if row.get("true_label_group") != "out_of_scope"
    ]
    out_of_scope_predictions = [
        row for row in predictions if row.get("true_label_group") == "out_of_scope"
    ]
    exact_matches = sum(1 for row in predictions if row.get("exact_label_match"))
    in_scope_exact = sum(1 for row in in_scope_predictions if row.get("exact_label_match"))
    oos_false_positive = sum(
        1 for row in out_of_scope_predictions if row.get("out_of_scope_false_positive")
    )
    similarities = [
        float(row["jaccard_similarity"])
        for row in predictions
        if isinstance(row.get("jaccard_similarity"), (int, float))
    ]
    per_fingerprint = {
        fingerprint_id: _per_fingerprint_metric(predictions, fingerprint_id)
        for fingerprint_id in primary_fingerprints
    }
    oos_diagnostics = _oos_diagnostics(predictions)
    diversity = _diversity_metrics(
        predictions=predictions,
        prepared_rows=prepared_rows,
        train_rows=train_rows,
        primary_fingerprints=primary_fingerprints,
        eval_contract=eval_contract,
    )
    canary_predictions = _canary_prediction_report(
        eval_contract=eval_contract,
        prediction_by_entry=prediction_by_entry,
        prepared_rows=prepared_rows,
    )
    return {
        "metadata": {
            "schema_version": "sequence_nn_metrics.v1",
            "artifact_id": "v3_sequence_nn_metrics_current702_20260525",
            "status": "computed_current702_sequence_nn_baseline",
            "model_id": SEQUENCE_NN_MODEL_ID,
            "kmer_size": SEQUENCE_NN_KMER_SIZE,
            "training_mode": "none_nearest_neighbor_lookup_only",
            "predictive_inputs": ["amino_acid_sequence_only"],
            "forbidden_inputs_used": [],
            "leakage_contract": "no EC/name/prose/expert-note predictive features",
            "label_registry_edited": False,
            "model_training_performed": False,
            "plm_embeddings_computed": False,
            "label_manifest_artifact": str(label_manifest_out),
            "label_manifest_sha256": _json_payload_sha256(label_manifest),
            "sequence_manifest_artifact": str(sequence_manifest_path),
            "sequence_manifest_sha256": _sha256(sequence_manifest_path),
            "split_artifact": str(split_artifact_path),
            "split_artifact_sha256": _sha256(split_artifact_path),
            "predictions_artifact": str(predictions_out),
            "metrics_artifact": str(metrics_out),
            "sequence_fasta": sequence_fasta,
            "label_manifest_row_count": label_manifest.get("metadata", {}).get(
                "row_count"
            ),
            "sequence_covered_label_count": sequence_manifest.get("metadata", {}).get(
                "sequence_covered_label_count"
            ),
            "split_assignment_counts": label_manifest.get("metadata", {}).get(
                "split_assignment_counts", {}
            ),
            "train_sequence_count": len(train_rows),
            "heldout_sequence_count": len(heldout_rows),
            "prediction_count": len(predictions),
            "missing_sequence_entry_count": len(missing_sequence_entry_ids),
            "missing_sequence_entry_ids": sorted(
                missing_sequence_entry_ids, key=_entry_id_sort_key
            ),
            "sequence_identity_target_achieved": split_artifact.get(
                "metadata", {}
            ).get("sequence_identity_target_achieved"),
            "max_observed_train_test_identity": split_artifact.get("metadata", {}).get(
                "max_observed_train_test_identity"
            ),
        },
        "headline_metrics": {
            "exact_label_accuracy_all": _fraction(exact_matches, len(predictions)),
            "exact_label_accuracy_in_scope": _fraction(
                in_scope_exact, len(in_scope_predictions)
            ),
            "primary_supervised_accuracy": _fraction(
                sum(1 for row in primary_predictions if row.get("top1_correct")),
                len(primary_predictions),
            ),
            "out_of_scope_false_positive_rate_no_threshold": _fraction(
                oos_false_positive, len(out_of_scope_predictions)
            ),
            "mean_nearest_jaccard_similarity": _mean(similarities),
            "max_nearest_jaccard_similarity": max(similarities)
            if similarities
            else None,
        },
        "primary_seed_metrics": {
            "status": "computed",
            "support_count": len(primary_predictions),
            "accuracy": _fraction(
                sum(1 for row in primary_predictions if row.get("top1_correct")),
                len(primary_predictions),
            ),
            "fingerprint_ids": primary_fingerprints,
        },
        "per_fingerprint_metrics": per_fingerprint,
        "oos_abstention_diagnostics": oos_diagnostics,
        "diversity_stratified_accuracy": diversity,
        "canary_predictions": canary_predictions,
        "limitations": [
            "deterministic 3-mer Jaccard nearest neighbor is a smoke baseline, not a trained representation model",
            "no EC, name, prose, or expert-note fields are used as predictive features",
            "no threshold calibration or learned embedding performance is claimed",
        ],
    }


def _per_fingerprint_metric(
    predictions: list[dict[str, Any]], fingerprint_id: str
) -> dict[str, Any]:
    rows = [
        row
        for row in predictions
        if row.get("benchmark_role") == f"{PRIMARY_BENCHMARK_PREFIX}::{fingerprint_id}"
    ]
    correct = sum(1 for row in rows if row.get("top1_correct"))
    return {
        "status": "computed" if rows else "underpowered_no_heldout_rows",
        "heldout_row_count": len(rows),
        "top1_accuracy": _fraction(correct, len(rows)),
        "underpowered": len(rows) < 5,
        "correct_count": correct,
    }


def _oos_diagnostics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    oos_rows = [row for row in predictions if row.get("true_label_group") == "out_of_scope"]
    by_tier: dict[str, dict[str, Any]] = {}
    for tier in sorted({str(row.get("oos_tier") or "unknown_oos") for row in oos_rows}):
        tier_rows = [row for row in oos_rows if str(row.get("oos_tier") or "unknown_oos") == tier]
        false_positive = sum(1 for row in tier_rows if row.get("out_of_scope_false_positive"))
        by_tier[tier] = {
            "row_count": len(tier_rows),
            "abstention_rate": _fraction(
                sum(1 for row in tier_rows if row.get("abstained")),
                len(tier_rows),
            ),
            "false_positive_rate_no_threshold": _fraction(
                false_positive, len(tier_rows)
            ),
            "false_positive_count": false_positive,
        }
    secondary_rows = [
        row
        for row in predictions
        if str(row.get("benchmark_role") or "").startswith(f"{SECONDARY_BENCHMARK_PREFIX}::")
    ]
    return {
        "status": "computed",
        "out_of_scope_heldout_count": len(oos_rows),
        "false_positive_count": sum(
            1 for row in oos_rows if row.get("out_of_scope_false_positive")
        ),
        "false_positive_rate_no_threshold": _fraction(
            sum(1 for row in oos_rows if row.get("out_of_scope_false_positive")),
            len(oos_rows),
        ),
        "by_oos_tier": by_tier,
        "secondary_probe_heldout_count": len(secondary_rows),
        "secondary_probe_rows": [
            {
                "entry_id": row.get("entry_id"),
                "benchmark_role": row.get("benchmark_role"),
                "predicted_label_group": row.get("predicted_label_group"),
                "abstained": row.get("abstained"),
                "jaccard_similarity": row.get("jaccard_similarity"),
            }
            for row in secondary_rows
        ],
    }


def _diversity_metrics(
    *,
    predictions: list[dict[str, Any]],
    prepared_rows: list[dict[str, Any]],
    train_rows: list[dict[str, Any]],
    primary_fingerprints: list[str],
    eval_contract: dict[str, Any],
) -> dict[str, Any]:
    prediction_by_entry = {row["entry_id"]: row for row in predictions}
    train_thresholds = {
        fingerprint_id: _train_diversity_thresholds(train_rows, fingerprint_id)
        for fingerprint_id in primary_fingerprints
    }
    by_fingerprint: dict[str, dict[str, Any]] = {}
    for fingerprint_id in primary_fingerprints:
        heldout_rows = [
            row
            for row in prepared_rows
            if row["split_assignment"] == "heldout" and row["label_group"] == fingerprint_id
        ]
        thresholds = train_thresholds[fingerprint_id]
        bin_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in heldout_rows:
            nearest_similarity = _nearest_same_fingerprint_different_cluster_similarity(
                row=row,
                train_rows=train_rows,
                fingerprint_id=fingerprint_id,
            )
            diversity_bin = _diversity_bin(nearest_similarity, thresholds)
            prediction = prediction_by_entry.get(row["entry_id"], {})
            bin_rows[diversity_bin].append(prediction)
        by_fingerprint[fingerprint_id] = {
            "row_count_by_diversity_bin": {
                name: len(rows) for name, rows in sorted(bin_rows.items())
            },
            "accuracy_or_recall_by_diversity_bin": {
                name: _fraction(
                    sum(1 for pred in rows if pred.get("top1_correct")),
                    len(rows),
                )
                for name, rows in sorted(bin_rows.items())
            },
            "macro_F1_contribution_by_bin_when_powered": {
                name: "underpowered_or_not_computed"
                for name in sorted(bin_rows)
            },
            "subfamily_count_train_vs_eval": {
                "train": len(
                    {
                        str(row.get("mmseqs30_subfamily_cluster_id"))
                        for row in train_rows
                        if row["label_group"] == fingerprint_id
                        and row.get("mmseqs30_subfamily_cluster_id")
                    }
                ),
                "eval": len(
                    {
                        str(row.get("mmseqs30_subfamily_cluster_id"))
                        for row in heldout_rows
                        if row.get("mmseqs30_subfamily_cluster_id")
                    }
                ),
            },
            "underpowered_cell_flags": [
                name for name, rows in sorted(bin_rows.items()) if len(rows) < 5
            ],
            "train_only_similarity_thresholds": thresholds,
        }
    return {
        "status": "computed",
        "required_axis": (
            eval_contract.get("diversity_stratified_accuracy_policy", {})
            .get("primary_diversity_axis", {})
            .get("name")
        ),
        "by_fingerprint": by_fingerprint,
    }


def _canary_prediction_report(
    *,
    eval_contract: dict[str, Any],
    prediction_by_entry: dict[str, dict[str, Any]],
    prepared_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    prepared_by_entry = {row["entry_id"]: row for row in prepared_rows}
    rows: list[dict[str, Any]] = []
    for canary in eval_contract.get("canary_examples", {}).get("examples", []) or []:
        if not isinstance(canary, dict) or not canary.get("entry_id"):
            continue
        entry_id = str(canary["entry_id"])
        prediction = prediction_by_entry.get(entry_id)
        prepared = prepared_by_entry.get(entry_id, {})
        rows.append(
            {
                "entry_id": entry_id,
                "expected_eval_role": canary.get("expected_eval_role"),
                "expected_behavior": canary.get("expected_behavior"),
                "split_assignment": prepared.get("split_assignment"),
                "prediction_status": "reported" if prediction else "not_heldout",
                "predicted_label_group": (prediction or {}).get("predicted_label_group"),
                "abstained": (prediction or {}).get("abstained"),
                "top1_correct": (prediction or {}).get("top1_correct"),
            }
        )
    return {
        "status": "computed",
        "canary_count": len(rows),
        "reported_canary_count": sum(1 for row in rows if row["prediction_status"] == "reported"),
        "rows": rows,
    }


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


def _sequence_fasta_path_from_source(sequence_source: Any) -> str | None:
    if not isinstance(sequence_source, str):
        return None
    if not sequence_source.startswith("fasta:"):
        return None
    return sequence_source.split(";", 1)[0].removeprefix("fasta:")


def _load_sequence_nn_fasta_sequences(sequence_fasta: str | None) -> dict[str, str]:
    if not sequence_fasta:
        return {}
    path = Path(sequence_fasta)
    if not path.exists():
        return {}
    sequences: dict[str, str] = {}
    header: str | None = None
    chunks: list[str] = []

    def flush() -> None:
        if header is None:
            return
        sequence = _normalise_sequence("".join(chunks))
        if not sequence:
            return
        for key in _sequence_fasta_keys(header):
            sequences.setdefault(key, sequence)

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                flush()
                header = line[1:].strip()
                chunks = []
            else:
                chunks.append(line)
    flush()
    return sequences


def _sequence_fasta_keys(header: str) -> list[str]:
    keys: set[str] = set()
    pipe_match = re.match(r"^(?:sp|tr)\|([A-Za-z0-9]+)\|", header)
    if pipe_match:
        keys.add(pipe_match.group(1))
    for token in re.split(r"[\s|,;]+", header):
        if re.fullmatch(r"[A-Z][A-Z0-9]{5,9}", token):
            keys.add(token)
    keys.update(re.findall(r"m_csa:\d+", header))
    keys.update(re.findall(r"uniprot:[A-Z][A-Z0-9]{5,9}", header))
    return sorted(keys, key=_entry_id_sort_key)


def _sequence_for_manifest_row(
    row: dict[str, Any], fasta_sequences: dict[str, str]
) -> str | None:
    for record in row.get("sequence_records", []) or []:
        if not isinstance(record, dict):
            continue
        accession = record.get("accession") or record.get("sequence_id")
        if accession and str(accession) in fasta_sequences:
            return fasta_sequences[str(accession)]
    for accession in row.get("real_sequence_accessions", []) or []:
        if str(accession) in fasta_sequences:
            return fasta_sequences[str(accession)]
    entry_id = row.get("entry_id")
    if entry_id and str(entry_id) in fasta_sequences:
        return fasta_sequences[str(entry_id)]
    return None


def _sequence_manifest_reference_accessions(
    *,
    entry_id: str,
    sequence_row: dict[str, Any],
    split_row: dict[str, Any],
) -> list[str]:
    accessions: list[str] = []
    for accession in sequence_row.get("reference_uniprot_ids", []) or []:
        if accession and str(accession) not in accessions:
            accessions.append(str(accession))
    for record in sequence_row.get("sequence_records", []) or []:
        if not isinstance(record, dict):
            continue
        accession = record.get("accession_or_structure_id")
        if accession and str(accession) not in accessions:
            accessions.append(str(accession))
    for accession in split_row.get("reference_uniprot_ids", []) or []:
        if accession and str(accession) not in accessions:
            accessions.append(str(accession))
    for accession in split_row.get("real_sequence_accessions", []) or []:
        if accession and str(accession) not in accessions:
            accessions.append(str(accession))
    if entry_id.startswith("uniprot:"):
        accession = entry_id.split(":", 1)[1]
        if accession not in accessions:
            accessions.append(accession)
    return accessions


def _label_group_from_manifest_row(row: dict[str, Any]) -> str:
    fingerprint_id = row.get("fingerprint_id")
    if fingerprint_id:
        return str(fingerprint_id)
    return "out_of_scope"


def _split_assignment_repair_row(
    *,
    entry_id: str,
    label_row: dict[str, Any],
    sequence_row: dict[str, Any],
    assignment: dict[str, Any],
) -> dict[str, Any]:
    reference_accessions = _sequence_manifest_reference_accessions(
        entry_id=entry_id,
        sequence_row=sequence_row,
        split_row={},
    )
    return {
        "entry_id": entry_id,
        "entry_name": sequence_row.get("entry_name") or label_row.get("entry_id"),
        "label_type": label_row.get("label_type"),
        "target_fingerprint_id": label_row.get("fingerprint_id"),
        "label_group": _label_group_from_manifest_row(label_row),
        "top1_fingerprint_id": None,
        "top1_score": 0.0,
        "top1_correct": False,
        "top3_correct": False,
        "abstained": True,
        "evaluable": False,
        "status": "not_evaluated_sequence_split_assignment_repaired",
        "resolved_residue_count": 0,
        "sequence_cluster_id": (
            f"sequence_coverage_repair:{entry_id}"
            if not reference_accessions
            else f"uniprot:{reference_accessions[0]}"
        ),
        "sequence_cluster_entry_count": 1,
        "reference_uniprot_ids": reference_accessions,
        "selected_structure_proxy_id": "not_evaluated",
        "active_site_geometry_proxy_bucket": "not_evaluated",
        "distance_proxy_note": (
            "split assignment repaired for a current-label row with sequence "
            "coverage but no geometry retrieval result"
        ),
        "selected_structure_proxy_count": 0,
        "active_site_geometry_proxy_bucket_count": 0,
        "low_neighborhood_proxy_score": 0,
        "low_similarity_proxy_pass": True,
        "fold_divergence_proxy_pass": True,
        "partition": assignment["partition"],
        "real_sequence_identity_cluster_id": assignment[
            "real_sequence_identity_cluster_id"
        ],
        "real_sequence_identity_available": True,
        "real_sequence_record_count": assignment.get("sequence_record_count", 0),
        "real_sequence_accessions": assignment.get("sequence_accessions", []),
        "real_sequence_identity_note": (
            "mmseqs2_sequence_identity_cluster_repaired_assignment"
        ),
        "split_assignment_repair": {
            "source": "v3_sequence_split_assignment_repair_current702_20260525",
            "assignment_rule": assignment.get("assignment_rule"),
            "cluster_existing_partitions": assignment.get(
                "cluster_existing_partitions", []
            ),
            "cluster_existing_entry_ids": assignment.get(
                "cluster_existing_entry_ids", []
            ),
        },
    }


def _partition_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        str(row.get("partition") or "missing")
        for row in rows
        if isinstance(row, dict)
    )
    return dict(sorted(counts.items()))


def _identity_target_achieved(
    *, train_test_identity: dict[str, Any], threshold: float
) -> bool:
    if not train_test_identity.get("max_observed_train_test_identity_computable"):
        return False
    observed = train_test_identity.get("max_observed_train_test_identity")
    if observed is None:
        return True
    return float(observed) <= threshold


def _public_real_split_metadata(real_split: dict[str, Any]) -> dict[str, Any]:
    return {
        "usable": bool(real_split.get("usable")),
        "backend_resolved_path": real_split.get("backend_resolved_path"),
        "backend_version": real_split.get("backend_version"),
        "sequence_source": real_split.get("sequence_source"),
        "sequence_count": real_split.get("sequence_count"),
        "sequence_entry_coverage_count": real_split.get(
            "sequence_entry_coverage_count"
        ),
        "sequence_missing_entry_count": real_split.get("sequence_missing_entry_count"),
        "sequence_missing_entry_ids": real_split.get("sequence_missing_entry_ids", []),
        "record_cluster_count": real_split.get("record_cluster_count"),
        "entry_cluster_count": real_split.get("entry_cluster_count"),
        "limitations": real_split.get("limitations", []),
    }


def _nearest_kmer_train_row(
    heldout: dict[str, Any], train_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    return sorted(
        train_rows,
        key=lambda train: (
            -_jaccard(heldout["kmers"], train["kmers"]),
            _entry_id_sort_key(train["entry_id"]),
        ),
    )[0]


def _train_diversity_thresholds(
    train_rows: list[dict[str, Any]], fingerprint_id: str
) -> dict[str, Any]:
    similarities: list[float] = []
    fingerprint_train = [row for row in train_rows if row["label_group"] == fingerprint_id]
    for row in fingerprint_train:
        similarity = _nearest_same_fingerprint_different_cluster_similarity(
            row=row,
            train_rows=[
                other for other in fingerprint_train if other["entry_id"] != row["entry_id"]
            ],
            fingerprint_id=fingerprint_id,
        )
        if similarity is not None:
            similarities.append(similarity)
    if not similarities:
        return {
            "status": "far_open_set_only",
            "far_threshold": None,
            "close_threshold": None,
            "train_similarity_count": 0,
        }
    ordered = sorted(similarities)
    far_threshold = _quantile_nearest_rank(ordered, 1 / 3)
    close_threshold = _quantile_nearest_rank(ordered, 2 / 3)
    return {
        "status": "computed",
        "far_threshold": round(far_threshold, 4),
        "close_threshold": round(close_threshold, 4),
        "train_similarity_count": len(ordered),
    }


def _nearest_same_fingerprint_different_cluster_similarity(
    *,
    row: dict[str, Any],
    train_rows: list[dict[str, Any]],
    fingerprint_id: str,
) -> float | None:
    source_cluster = row.get("mmseqs30_subfamily_cluster_id")
    candidates = [
        train
        for train in train_rows
        if train["label_group"] == fingerprint_id
        and train.get("mmseqs30_subfamily_cluster_id") != source_cluster
    ]
    if not candidates:
        return None
    return max(_jaccard(row["kmers"], train["kmers"]) for train in candidates)


def _diversity_bin(similarity: float | None, thresholds: dict[str, Any]) -> str:
    if similarity is None or thresholds.get("status") != "computed":
        return "far_open_set"
    far = float(thresholds["far_threshold"])
    close = float(thresholds["close_threshold"])
    if similarity < far:
        return "far"
    if similarity >= close:
        return "close"
    return "medium"


def _quantile_nearest_rank(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    index = max(0, min(len(values) - 1, int(round((len(values) - 1) * quantile))))
    return values[index]


def _kmers(sequence: str, kmer_size: int) -> set[str]:
    clean = _normalise_sequence(sequence) or ""
    if len(clean) <= kmer_size:
        return {clean} if clean else set()
    return {clean[index : index + kmer_size] for index in range(len(clean) - kmer_size + 1)}


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _fraction(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def _normalise_sequence(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    sequence = re.sub(r"[^A-Za-z]", "", value).upper()
    return sequence or None


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


def _json_payload_sha256(payload: object) -> str:
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([A-Za-z_]+):(\d+)", str(entry_id))
    if match:
        return (match.group(1), int(match.group(2)), "")
    prefix, _, suffix = str(entry_id).partition(":")
    return (prefix, 10**9, suffix)
