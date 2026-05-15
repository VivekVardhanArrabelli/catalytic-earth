from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adapters import fetch_mcsa_sample, fetch_rhea_sample
from .automation import acquire_automation_lock, inspect_automation_lock, release_automation_lock
from .fingerprints import build_mechanism_demo, load_fingerprints
from .graph import build_seed_graph, build_sequence_cluster_proxy, build_v1_graph, summarize_graph
from .geometry_retrieval import write_geometry_retrieval
from .geometry_reports import write_geometry_slice_summary
from .generalization import (
    aggregate_foldseek_tm_score_query_chunks,
    audit_foldseek_tm_score_split_repair,
    audit_foldseek_tm_score_target_failure,
    build_sequence_distance_holdout_split_repair_candidate,
    build_sequence_distance_holdout_split_redesign_candidate,
    build_foldseek_coordinate_readiness,
    build_foldseek_tm_score_all_materializable_signal,
    build_foldseek_tm_score_query_chunk_signal,
    build_foldseek_tm_score_signal,
    build_sequence_distance_holdout_eval,
    project_foldseek_tm_score_split_repair,
)
from .learned_retrieval import build_learned_retrieval_manifest
from .labels import (
    analyze_cofactor_abstention_policy,
    analyze_cofactor_coverage,
    analyze_geometry_score_margins,
    analyze_in_scope_failures,
    analyze_seed_family_performance,
    analyze_out_of_scope_failures,
    analyze_review_evidence_gaps,
    analyze_review_debt_remediation,
    analyze_structure_mapping_issues,
    audit_expert_label_decision_local_evidence_gaps,
    audit_accepted_review_debt_deferrals,
    audit_expert_label_decision_repair_guardrails,
    audit_label_scaling_quality,
    audit_mechanism_ontology_gaps,
    audit_reaction_substrate_mismatches,
    audit_review_only_import_safety,
    audit_sequence_similarity_failure_sets,
    audit_review_debt_remap_local_leads,
    audit_structure_selection_holo_preference,
    build_active_learning_review_queue,
    build_adversarial_negative_controls,
    build_atp_phosphoryl_transfer_family_expansion,
    build_expert_label_decision_local_evidence_review_export,
    build_expert_label_decision_review_export,
    build_expert_review_export,
    build_family_propagation_guardrails,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    build_label_factory_audit,
    build_explicit_alternate_residue_position_requests,
    build_provisional_review_decision_batch,
    build_reaction_substrate_mismatch_review_export,
    build_selected_pdb_override_plan,
    check_label_batch_acceptance,
    check_label_factory_gates,
    check_label_preview_promotion_readiness,
    check_label_review_resolution,
    countable_benchmark_labels,
    evaluate_geometry_retrieval,
    apply_label_factory_actions,
    import_expert_review_decisions,
    import_countable_review_decisions,
    LabelFactoryGateInputs,
    label_summary,
    load_labels,
    migrate_label_registry_records,
    scan_review_debt_alternate_structures,
    resolve_expert_label_decision_local_evidence_repair_lanes,
    summarize_expert_label_decision_repair_candidates,
    summarize_expert_label_decision_local_evidence_repair_plan,
    summarize_label_factory_batches,
    summarize_review_debt,
    summarize_review_debt_remap_leads,
    summarize_review_debt_structure_selection_candidates,
    sweep_abstention_thresholds,
)
from .ontology import load_mechanism_ontology
from .models import RegistryError
from .performance import write_local_performance_suite
from .progress import WorkEntry, append_work_entry, write_progress_report
from .source_limits import audit_source_scale_limits
from .sources import build_source_ledger, load_sources
from .structure import write_geometry_features
from .transfer_scope import (
    audit_external_source_active_site_evidence_sample,
    audit_external_source_active_site_sourcing_export,
    audit_external_source_active_site_sourcing_queue,
    audit_external_source_active_site_sourcing_resolution,
    audit_external_source_binding_context_mapping_sample,
    audit_external_source_binding_context_repair_plan,
    audit_external_source_broad_ec_disambiguation,
    audit_external_source_candidate_manifest,
    audit_external_source_candidate_sample,
    audit_external_source_heuristic_control_queue,
    audit_external_source_heuristic_control_scores,
    audit_external_source_failure_modes,
    audit_external_source_lane_balance,
    audit_external_source_reaction_evidence_sample,
    audit_external_source_representation_control_comparison,
    audit_external_source_representation_control_manifest,
    audit_external_source_representation_backend_plan,
    audit_external_source_representation_backend_sample,
    audit_external_source_representation_backend_stability,
    audit_external_source_pilot_representation_adjudication,
    audit_external_source_sequence_alignment_verification,
    audit_external_source_backend_sequence_search,
    audit_external_source_sequence_reference_screen,
    audit_external_source_sequence_search_export,
    audit_external_source_sequence_holdouts,
    audit_external_source_sequence_neighborhood_sample,
    audit_external_source_structure_mapping_plan,
    audit_external_source_structure_mapping_sample,
    audit_external_source_control_repair_plan,
    audit_external_source_import_readiness,
    audit_external_source_transfer_blocker_matrix,
    build_external_ood_calibration_plan,
    build_external_source_active_site_gap_source_requests,
    build_external_source_active_site_sourcing_export,
    build_external_source_active_site_sourcing_queue,
    build_external_source_active_site_sourcing_resolution,
    build_external_source_binding_context_mapping_sample,
    build_external_source_binding_context_repair_plan,
    build_external_source_candidate_manifest,
    build_external_source_candidate_sample,
    build_external_source_active_site_evidence_queue,
    build_external_source_active_site_evidence_sample,
    build_external_source_control_repair_plan,
    build_external_source_evidence_plan,
    build_external_source_evidence_request_export,
    build_external_source_heuristic_control_queue,
    build_external_source_heuristic_control_scores,
    build_external_source_pilot_active_site_evidence_decisions,
    build_external_source_pilot_candidate_priority,
    build_external_source_pilot_evidence_packet,
    build_external_source_pilot_evidence_dossiers,
    build_external_source_pilot_review_decision_export,
    build_external_source_pilot_success_criteria,
    build_external_source_structure_mapping_plan,
    build_external_source_structure_mapping_sample,
    build_external_source_query_manifest,
    build_external_source_reaction_evidence_sample,
    build_external_source_representation_control_comparison,
    build_external_source_representation_control_manifest,
    build_external_source_representation_backend_plan,
    build_external_source_pilot_representation_backend_plan,
    build_external_source_representation_backend_sample,
    build_external_source_sequence_alignment_verification,
    build_external_source_backend_sequence_search,
    build_external_source_sequence_search_export,
    build_external_source_sequence_neighborhood_plan,
    build_external_source_sequence_neighborhood_sample,
    build_external_source_transfer_manifest,
    build_external_source_transfer_blocker_matrix,
    check_external_source_transfer_gates,
    ExternalSourceTransferGateInputs,
    validate_external_transfer_artifact_path_lineage,
)
from .v2 import (
    build_mechanism_benchmark,
    detect_inconsistencies,
    load_graph,
    mine_dark_hydrolase_candidates,
    run_baseline_retrieval,
    write_candidate_dossiers,
    write_v2_report,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


_LABEL_FACTORY_GATE_SLICE_ID_RE = re.compile(
    r"_(\d+)(?=(?:_[A-Za-z0-9]+)*\.json$)"
)
_LABEL_FACTORY_GATE_LINEAGE_EXEMPTIONS = {
    "atp_phosphoryl_transfer_family_expansion": (
        "historical ATP-family boundary-control artifact; it is ontology scope "
        "context and may predate the current label-factory slice"
    )
}


def _infer_label_factory_gate_slice_id(path: str | None) -> int | None:
    if not path:
        return None
    matches = _LABEL_FACTORY_GATE_SLICE_ID_RE.findall(Path(path).name)
    return int(matches[-1]) if matches else None


_LABEL_FACTORY_GATE_PAYLOAD_SLICE_KEYS = (
    "slice_id",
    "source_slice_id",
    "target_slice_id",
    "label_slice_id",
)
_LABEL_FACTORY_GATE_PAYLOAD_BATCH_KEYS = ("batch_id", "label_batch_id")


def _parse_label_factory_payload_lineage_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        match = re.match(r"^(\d+)(?:\D|$)", value.strip())
        if match:
            return int(match.group(1))
    return None


def _label_factory_gate_payload_lineage(artifact: dict[str, Any]) -> dict[str, int]:
    metadata = artifact.get("metadata", {})
    if not isinstance(metadata, dict):
        return {}

    lineage: dict[str, int] = {}
    for key in _LABEL_FACTORY_GATE_PAYLOAD_SLICE_KEYS:
        parsed = _parse_label_factory_payload_lineage_int(metadata.get(key))
        if parsed is not None:
            lineage[f"metadata.{key}"] = parsed
    for key in _LABEL_FACTORY_GATE_PAYLOAD_BATCH_KEYS:
        parsed = _parse_label_factory_payload_lineage_int(metadata.get(key))
        if parsed is not None:
            lineage[f"metadata.{key}"] = parsed

    artifact_lineage = metadata.get("artifact_lineage")
    if isinstance(artifact_lineage, dict):
        parsed = _parse_label_factory_payload_lineage_int(
            artifact_lineage.get("slice_id")
        )
        if parsed is not None:
            lineage["metadata.artifact_lineage.slice_id"] = parsed
    return lineage


def _label_factory_gate_payload_digest(artifact: dict[str, Any]) -> str:
    serialized = json.dumps(artifact, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def _validate_label_factory_gate_cli_lineage(
    *,
    labels_path: str,
    required_artifacts: dict[str, str],
    optional_artifacts: dict[str, str | None],
    loaded_artifacts: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifact_paths: dict[str, str] = {
        field_name: str(path)
        for field_name, path in {
            **required_artifacts,
            **{name: path for name, path in optional_artifacts.items() if path},
        }.items()
    }
    artifact_slice_ids: dict[str, int] = {}
    payload_slice_ids: dict[str, dict[str, int]] = {}
    payload_digests: dict[str, str] = {}
    payload_methods: dict[str, str] = {}
    missing_slice_id_artifacts: list[str] = []
    exempted_artifacts: dict[str, dict[str, Any]] = {}
    slice_members: dict[int, set[str]] = {}

    for field_name, path in artifact_paths.items():
        slice_id = _infer_label_factory_gate_slice_id(path)
        artifact = (loaded_artifacts or {}).get(field_name)
        payload_lineage: dict[str, int] = {}
        payload_slice_id: int | None = None
        if artifact is not None:
            metadata = artifact.get("metadata", {})
            if isinstance(metadata, dict) and isinstance(metadata.get("method"), str):
                payload_methods[field_name] = str(metadata["method"])
            payload_digests[field_name] = _label_factory_gate_payload_digest(artifact)
            payload_lineage = _label_factory_gate_payload_lineage(artifact)
            if payload_lineage:
                payload_slice_ids[field_name] = dict(sorted(payload_lineage.items()))
                payload_values = set(payload_lineage.values())
                if len(payload_values) > 1:
                    details = ", ".join(
                        f"{key}={value}"
                        for key, value in sorted(payload_lineage.items())
                    )
                    raise ValueError(
                        "mismatched label-factory gate artifact lineage: "
                        f"{field_name} payload declares conflicting slice ids: "
                        f"{details}"
                    )
                payload_slice_id = next(iter(payload_values))
        if field_name in _LABEL_FACTORY_GATE_LINEAGE_EXEMPTIONS:
            exempted_artifacts[field_name] = {
                "path": path,
                "slice_id": slice_id,
                "payload_slice_ids": payload_lineage,
                "reason": _LABEL_FACTORY_GATE_LINEAGE_EXEMPTIONS[field_name],
            }
            continue
        if (
            payload_slice_id is not None
            and slice_id is not None
            and payload_slice_id != slice_id
        ):
            raise ValueError(
                "mismatched label-factory gate artifact lineage: "
                f"{field_name} payload slice id {payload_slice_id} conflicts "
                f"with path slice id {slice_id}"
            )
        if slice_id is None:
            if payload_slice_id is None:
                missing_slice_id_artifacts.append(field_name)
                continue
            artifact_slice_ids[field_name] = payload_slice_id
            slice_members.setdefault(payload_slice_id, set()).add(field_name)
        else:
            artifact_slice_ids[field_name] = slice_id
            slice_members.setdefault(slice_id, set()).add(field_name)

    labels_slice_id = _infer_label_factory_gate_slice_id(labels_path)
    if labels_slice_id is not None:
        artifact_slice_ids["labels"] = labels_slice_id
        slice_members.setdefault(labels_slice_id, set()).add("labels")

    if len(slice_members) > 1:
        details = "; ".join(
            f"{slice_id}: {', '.join(sorted(names))}"
            for slice_id, names in sorted(slice_members.items())
        )
        raise ValueError(
            "mismatched label-factory gate artifact lineage: "
            f"expected one non-exempt slice id across gate inputs, saw {details}"
        )

    return {
        "method": "label_factory_gate_cli_lineage_validation",
        "slice_id": next(iter(slice_members), None),
        "artifact_slice_ids": dict(sorted(artifact_slice_ids.items())),
        "payload_slice_ids": dict(sorted(payload_slice_ids.items())),
        "payload_methods": dict(sorted(payload_methods.items())),
        "payload_digests": dict(sorted(payload_digests.items())),
        "artifact_paths": dict(sorted(artifact_paths.items())),
        "missing_slice_id_artifacts": sorted(missing_slice_id_artifacts),
        "exempted_artifacts": dict(sorted(exempted_artifacts.items())),
    }


def _validate_label_scaling_quality_cli_lineage(
    *,
    required_artifacts: dict[str, str],
    optional_artifacts: dict[str, str | None],
    loaded_artifacts: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    try:
        lineage = _validate_label_factory_gate_cli_lineage(
            labels_path="",
            required_artifacts=required_artifacts,
            optional_artifacts=optional_artifacts,
            loaded_artifacts=loaded_artifacts,
        )
    except ValueError as exc:
        raise ValueError(
            str(exc).replace(
                "label-factory gate artifact lineage",
                "label-scaling quality artifact lineage",
            )
        ) from exc
    return {
        **lineage,
        "method": "label_scaling_quality_cli_lineage_validation",
        "blocker_removed": "artifact_graph_consistency_for_label_scaling_quality",
    }


def _validate_label_batch_acceptance_cli_lineage(
    *,
    countable_labels_path: str,
    review_state_labels_path: str,
    required_artifacts: dict[str, str],
    optional_artifacts: dict[str, str | None],
    loaded_artifacts: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    try:
        lineage = _validate_label_factory_gate_cli_lineage(
            labels_path=countable_labels_path,
            required_artifacts=required_artifacts,
            optional_artifacts={
                **optional_artifacts,
                "review_state_labels": review_state_labels_path,
            },
            loaded_artifacts=loaded_artifacts,
        )
    except ValueError as exc:
        raise ValueError(
            str(exc).replace(
                "label-factory gate artifact lineage",
                "label-batch acceptance artifact lineage",
            )
        ) from exc
    return {
        **lineage,
        "method": "label_batch_acceptance_cli_lineage_validation",
        "blocker_removed": "artifact_graph_consistency_for_label_batch_acceptance",
    }


def write_label_registry(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write("[\n")
        for index, record in enumerate(records):
            suffix = "," if index < len(records) - 1 else ""
            handle.write(f"  {json.dumps(record, sort_keys=True, separators=(',', ':'))}{suffix}\n")
        handle.write("]\n")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _git_output(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_worktree_dirty(repo_root: Path) -> bool:
    return bool(_git_output(repo_root, "status", "--porcelain"))


def _git_merge_in_progress(repo_root: Path) -> bool:
    merge_head = _git_output(repo_root, "rev-parse", "--git-path", "MERGE_HEAD")
    return (repo_root / merge_head).exists()


def _git_head_synced_with_origin_main(repo_root: Path) -> bool:
    head = _git_output(repo_root, "rev-parse", "HEAD")
    origin_main = _git_output(repo_root, "rev-parse", "origin/main")
    return head == origin_main


def cmd_validate(_: argparse.Namespace) -> int:
    sources = load_sources()
    fingerprints = load_fingerprints()
    ontology = load_mechanism_ontology()
    labels = load_labels()
    print(f"Validated {len(sources)} source records")
    print(f"Validated {len(fingerprints)} mechanism fingerprints")
    print(f"Validated {len(ontology['families'])} mechanism ontology families")
    print(f"Validated {len(labels)} curated mechanism labels")
    return 0


def cmd_automation_lock(args: argparse.Namespace) -> int:
    lock_dir = Path(args.lock_dir)
    repo_root = Path(args.repo_root)
    stale_after_seconds = args.stale_after_minutes * 60
    if args.lock_action == "status":
        result = inspect_automation_lock(
            lock_dir,
            stale_after_seconds=stale_after_seconds,
        )
        print(json.dumps(result.as_dict(), sort_keys=True))
        return 0
    if args.lock_action == "acquire":
        worktree_dirty = args.worktree_dirty
        if not args.skip_worktree_check:
            worktree_dirty = worktree_dirty or _git_worktree_dirty(repo_root)
        result = acquire_automation_lock(
            lock_dir,
            started_at=args.started_at or _utc_now_iso(),
            stale_after_seconds=stale_after_seconds,
            worktree_dirty=worktree_dirty,
        )
        print(json.dumps(result.as_dict(), sort_keys=True))
        return 0 if result.acquired else 3
    if args.lock_action == "release":
        blocked: list[str] = []
        if args.require_clean and _git_worktree_dirty(repo_root):
            blocked.append("worktree_dirty")
        if args.require_no_merge and _git_merge_in_progress(repo_root):
            blocked.append("merge_in_progress")
        if args.require_synced and not _git_head_synced_with_origin_main(repo_root):
            blocked.append("head_not_equal_origin_main")
        if blocked:
            payload = {
                "released": False,
                "lock_dir": str(lock_dir),
                "status": "release_blocked",
                "blockers": blocked,
            }
            print(json.dumps(payload, sort_keys=True))
            return 4
        release_automation_lock(lock_dir)
        print(json.dumps({"released": True, "lock_dir": str(lock_dir)}, sort_keys=True))
        return 0
    raise ValueError(f"unknown automation lock action: {args.lock_action}")


def cmd_build_ledger(args: argparse.Namespace) -> int:
    sources = load_sources()
    ledger = build_source_ledger(sources)
    write_json(Path(args.out), ledger)
    print(f"Wrote source ledger to {args.out}")
    return 0


def cmd_fingerprint_demo(args: argparse.Namespace) -> int:
    fingerprints = load_fingerprints()
    demo = build_mechanism_demo(fingerprints)
    write_json(Path(args.out), demo)
    print(f"Wrote mechanism demo to {args.out}")
    return 0


def cmd_fetch_rhea_sample(args: argparse.Namespace) -> int:
    sample = fetch_rhea_sample(limit=args.limit)
    write_json(Path(args.out), sample)
    print(f"Wrote {sample['metadata']['record_count']} Rhea records to {args.out}")
    return 0


def cmd_fetch_mcsa_sample(args: argparse.Namespace) -> int:
    ids = [int(item.strip()) for item in args.ids.split(",") if item.strip()]
    sample = fetch_mcsa_sample(ids=ids)
    write_json(Path(args.out), sample)
    print(f"Wrote {sample['metadata']['record_count']} M-CSA records to {args.out}")
    return 0


def cmd_build_seed_graph(args: argparse.Namespace) -> int:
    ids = [int(item.strip()) for item in args.mcsa_ids.split(",") if item.strip()]
    graph = build_seed_graph(ids)
    write_json(Path(args.out), graph)
    print(
        "Wrote seed graph to "
        f"{args.out} ({graph['metadata']['node_count']} nodes, {graph['metadata']['edge_count']} edges)"
    )
    return 0


def cmd_build_v1_graph(args: argparse.Namespace) -> int:
    graph = build_v1_graph(max_mcsa=args.max_mcsa, page_size=args.page_size)
    write_json(Path(args.out), graph)
    print(
        "Wrote v1 graph to "
        f"{args.out} ({graph['metadata']['node_count']} nodes, {graph['metadata']['edge_count']} edges)"
    )
    return 0


def cmd_graph_summary(args: argparse.Namespace) -> int:
    with Path(args.graph).open("r", encoding="utf-8") as handle:
        graph = json.load(handle)
    summary = summarize_graph(graph)
    write_json(Path(args.out), summary)
    print(f"Wrote graph summary to {args.out}")
    return 0


def cmd_build_sequence_cluster_proxy(args: argparse.Namespace) -> int:
    with Path(args.graph).open("r", encoding="utf-8") as handle:
        graph = json.load(handle)
    artifact = build_sequence_cluster_proxy(graph, entry_ids=set(args.entry_id or []))
    write_json(Path(args.out), artifact)
    print(
        "Wrote sequence cluster proxy to "
        f"{args.out} ({artifact['metadata']['entry_count']} entries, "
        f"{artifact['metadata']['duplicate_cluster_count']} duplicate clusters)"
    )
    return 0


def cmd_build_sequence_distance_holdout_eval(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    geometry = None
    if args.geometry:
        with Path(args.geometry).open("r", encoding="utf-8") as handle:
            geometry = json.load(handle)
    labels = load_labels(Path(args.labels))
    artifact = build_sequence_distance_holdout_eval(
        retrieval=retrieval,
        labels=labels,
        sequence_clusters=sequence_clusters,
        geometry=geometry,
        slice_id=args.slice_id,
        abstain_threshold=args.abstain_threshold,
        holdout_fraction=args.holdout_fraction,
        min_holdout_rows=args.min_holdout_rows,
        sequence_fasta=args.sequence_fasta,
        sequence_identity_backend=args.sequence_identity_backend,
        sequence_identity_threshold=args.sequence_identity_threshold,
        sequence_identity_coverage=args.sequence_identity_coverage,
        compute_max_train_test_identity=not args.skip_max_train_test_identity,
        mmseqs_binary=args.mmseqs_binary,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote sequence/fold-distance holdout evaluation to "
        f"{args.out} ({artifact['metadata']['heldout_count']} held out, "
        f"{artifact['metrics']['heldout']['out_of_scope_false_non_abstentions']} "
        "held-out false non-abstentions)"
    )
    return 0


def cmd_build_foldseek_coordinate_readiness(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    labels = load_labels(Path(args.labels))
    geometry = None
    if args.geometry:
        with Path(args.geometry).open("r", encoding="utf-8") as handle:
            geometry = json.load(handle)
    sequence_holdout = None
    if args.sequence_holdout:
        with Path(args.sequence_holdout).open("r", encoding="utf-8") as handle:
            sequence_holdout = json.load(handle)
    artifact = build_foldseek_coordinate_readiness(
        retrieval=retrieval,
        labels=labels,
        geometry=geometry,
        sequence_holdout=sequence_holdout,
        slice_id=args.slice_id,
        foldseek_binary=args.foldseek_binary,
        coordinate_dir=args.coordinate_dir,
        max_coordinate_files=args.max_coordinate_files,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek coordinate readiness to "
        f"{args.out} ({artifact['metadata']['materialized_coordinate_count']} "
        "coordinates staged, "
        f"tm_score_split_computed={artifact['metadata']['tm_score_split_computed']})"
    )
    return 0


def cmd_build_foldseek_tm_score_signal(args: argparse.Namespace) -> int:
    with Path(args.readiness).open("r", encoding="utf-8") as handle:
        readiness = json.load(handle)
    artifact = build_foldseek_tm_score_signal(
        readiness=readiness,
        readiness_path=args.readiness,
        slice_id=args.slice_id,
        foldseek_binary=args.foldseek_binary,
        max_staged_coordinates=args.max_staged_coordinates,
        prior_staged_coordinate_count=args.prior_staged_coordinate_count,
        threads=args.threads,
        keep_all_rows=not args.summary_only,
        max_reported_rows=args.max_reported_rows,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score signal to "
        f"{args.out} ({artifact['metadata']['staged_coordinate_count']} "
        "staged coordinates, "
        f"{artifact['metadata']['pair_count']} pair rows, "
        f"tm_score_split_computed={artifact['metadata']['tm_score_split_computed']})"
    )
    return 0


def cmd_build_foldseek_tm_score_all_materializable_signal(args: argparse.Namespace) -> int:
    with Path(args.readiness).open("r", encoding="utf-8") as handle:
        readiness = json.load(handle)
    artifact = build_foldseek_tm_score_all_materializable_signal(
        readiness=readiness,
        readiness_path=args.readiness,
        slice_id=args.slice_id,
        foldseek_binary=args.foldseek_binary,
        max_runtime_seconds=args.max_runtime_seconds,
        threads=args.threads,
        threshold=args.threshold,
        max_reported_pairs=args.max_reported_pairs,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote all-materializable Foldseek TM-score signal to "
        f"{args.out} ({artifact['metadata']['staged_coordinate_count']} "
        "staged coordinates, "
        f"{artifact['metadata']['pair_count']} pair rows, "
        f"run_status={artifact['metadata']['foldseek_run_status']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_build_foldseek_tm_score_query_chunk_signal(args: argparse.Namespace) -> int:
    with Path(args.readiness).open("r", encoding="utf-8") as handle:
        readiness = json.load(handle)
    artifact = build_foldseek_tm_score_query_chunk_signal(
        readiness=readiness,
        readiness_path=args.readiness,
        slice_id=args.slice_id,
        foldseek_binary=args.foldseek_binary,
        chunk_index=args.chunk_index,
        chunk_size=args.chunk_size,
        max_runtime_seconds=args.max_runtime_seconds,
        threads=args.threads,
        threshold=args.threshold,
        max_reported_pairs=args.max_reported_pairs,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score query chunk signal to "
        f"{args.out} (chunk {artifact['metadata']['query_chunk_index'] + 1}/"
        f"{artifact['metadata']['query_chunk_count']}, "
        f"{artifact['metadata']['query_staged_coordinate_count']} query coordinates, "
        f"{artifact['metadata']['pair_count']} pair rows, "
        f"run_status={artifact['metadata']['foldseek_run_status']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_aggregate_foldseek_tm_score_query_chunks(args: argparse.Namespace) -> int:
    chunks = []
    for chunk_path in args.chunks:
        with Path(chunk_path).open("r", encoding="utf-8") as handle:
            chunks.append(json.load(handle))
    artifact = aggregate_foldseek_tm_score_query_chunks(
        chunks=chunks,
        chunk_paths=args.chunks,
        slice_id=args.slice_id,
        threshold=args.threshold,
        max_reported_pairs=args.max_reported_pairs,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score query chunk aggregate to "
        f"{args.out} ({artifact['metadata']['completed_query_chunk_count']}/"
        f"{artifact['metadata']['query_chunk_count']} chunks, "
        f"{artifact['metadata']['completed_query_coordinate_count']} query coordinates, "
        f"{artifact['metadata']['pair_count']} pair rows, "
        f"max_tm={artifact['metadata']['max_observed_train_test_tm_score']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_audit_foldseek_tm_score_target_failure(args: argparse.Namespace) -> int:
    with Path(args.signal).open("r", encoding="utf-8") as handle:
        signal = json.load(handle)
    artifact = audit_foldseek_tm_score_target_failure(
        signal=signal,
        signal_path=args.signal,
        threshold=args.threshold,
        max_blocking_pairs=args.max_blocking_pairs,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score target-failure audit to "
        f"{args.out} ("
        f"{artifact['metadata']['violating_unique_structure_pair_count']} "
        "blocking structure pairs, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_audit_foldseek_tm_score_split_repair(args: argparse.Namespace) -> int:
    with Path(args.target_failure).open("r", encoding="utf-8") as handle:
        target_failure = json.load(handle)
    with Path(args.sequence_holdout).open("r", encoding="utf-8") as handle:
        sequence_holdout = json.load(handle)
    artifact = audit_foldseek_tm_score_split_repair(
        target_failure=target_failure,
        sequence_holdout=sequence_holdout,
        target_failure_path=args.target_failure,
        sequence_holdout_path=args.sequence_holdout,
        threshold=args.threshold,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score split-repair plan to "
        f"{args.out} ("
        f"{artifact['metadata']['repair_candidate_pair_count']} repair-candidate "
        "pairs, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_project_foldseek_tm_score_split_repair(args: argparse.Namespace) -> int:
    with Path(args.signal).open("r", encoding="utf-8") as handle:
        signal = json.load(handle)
    with Path(args.repair_plan).open("r", encoding="utf-8") as handle:
        repair_plan = json.load(handle)
    artifact = project_foldseek_tm_score_split_repair(
        signal=signal,
        repair_plan=repair_plan,
        signal_path=args.signal,
        repair_plan_path=args.repair_plan,
        threshold=args.threshold,
        max_reported_pairs=args.max_reported_pairs,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote Foldseek TM-score split-repair projection to "
        f"{args.out} (projected max train/test TM-score="
        f"{artifact['metadata']['projected_max_observed_train_test_tm_score']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_build_sequence_distance_holdout_split_repair_candidate(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_holdout).open("r", encoding="utf-8") as handle:
        sequence_holdout = json.load(handle)
    with Path(args.repair_plan).open("r", encoding="utf-8") as handle:
        repair_plan = json.load(handle)
    projection = None
    if args.projection:
        with Path(args.projection).open("r", encoding="utf-8") as handle:
            projection = json.load(handle)
    artifact = build_sequence_distance_holdout_split_repair_candidate(
        sequence_holdout=sequence_holdout,
        repair_plan=repair_plan,
        projection=projection,
        sequence_holdout_path=args.sequence_holdout,
        repair_plan_path=args.repair_plan,
        projection_path=args.projection,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote sequence holdout split-repair candidate to "
        f"{args.out} (heldout_count="
        f"{artifact['metadata']['repaired_heldout_count']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_build_sequence_distance_holdout_split_redesign_candidate(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_holdout).open("r", encoding="utf-8") as handle:
        sequence_holdout = json.load(handle)
    with Path(args.split_repair_plan).open("r", encoding="utf-8") as handle:
        split_repair_plan = json.load(handle)
    artifact = build_sequence_distance_holdout_split_redesign_candidate(
        sequence_holdout=sequence_holdout,
        split_repair_plan=split_repair_plan,
        sequence_holdout_path=args.sequence_holdout,
        split_repair_plan_path=args.split_repair_plan,
        threshold=args.threshold,
    )
    write_json(Path(args.out), artifact)
    print(
        "Wrote sequence holdout split-redesign candidate to "
        f"{args.out} (heldout_count="
        f"{artifact['metadata']['redesigned_heldout_count']}, "
        "observed_blockers_after_redesign="
        f"{artifact['metadata']['projected_observed_blocking_pair_count_after_redesign']}, "
        "full_tm_score_holdout_claim_permitted="
        f"{artifact['metadata']['full_tm_score_holdout_claim_permitted']})"
    )
    return 0


def cmd_audit_source_scale_limits(args: argparse.Namespace) -> int:
    with Path(args.graph).open("r", encoding="utf-8") as handle:
        graph = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    prior_graph = None
    if args.prior_graph:
        with Path(args.prior_graph).open("r", encoding="utf-8") as handle:
            prior_graph = json.load(handle)
    review_debt = None
    if args.review_debt:
        with Path(args.review_debt).open("r", encoding="utf-8") as handle:
            review_debt = json.load(handle)
    label_expansion_candidates = None
    if args.label_expansion_candidates:
        with Path(args.label_expansion_candidates).open("r", encoding="utf-8") as handle:
            label_expansion_candidates = json.load(handle)
    audit = audit_source_scale_limits(
        graph,
        labels,
        target_source_entries=args.target_source_entries,
        public_target_countable_labels=args.public_target_countable_labels,
        prior_graph=prior_graph,
        review_debt=review_debt,
        label_expansion_candidates=label_expansion_candidates,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote source scale limit audit to "
        f"{args.out} ({audit['metadata']['recommendation']})"
    )
    return 0


def cmd_build_external_source_transfer_manifest(args: argparse.Namespace) -> int:
    with Path(args.source_scale_audit).open("r", encoding="utf-8") as handle:
        source_scale_audit = json.load(handle)
    with Path(args.learned_retrieval_manifest).open("r", encoding="utf-8") as handle:
        learned_retrieval_manifest = json.load(handle)
    with Path(args.sequence_similarity_failure_sets).open("r", encoding="utf-8") as handle:
        sequence_similarity_failure_sets = json.load(handle)
    with Path(args.ontology_gap_audit).open("r", encoding="utf-8") as handle:
        ontology_gap_audit = json.load(handle)
    with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
        active_learning_queue = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    manifest = build_external_source_transfer_manifest(
        source_scale_audit=source_scale_audit,
        learned_retrieval_manifest=learned_retrieval_manifest,
        sequence_similarity_failure_sets=sequence_similarity_failure_sets,
        ontology_gap_audit=ontology_gap_audit,
        active_learning_queue=active_learning_queue,
        labels=labels,
    )
    write_json(Path(args.out), manifest)
    print(
        "Wrote external source transfer manifest to "
        f"{args.out} ({manifest['metadata']['manifest_recommendation']})"
    )
    return 0


def cmd_build_external_source_query_manifest(args: argparse.Namespace) -> int:
    with Path(args.transfer_manifest).open("r", encoding="utf-8") as handle:
        transfer_manifest = json.load(handle)
    with Path(args.ontology_gap_audit).open("r", encoding="utf-8") as handle:
        ontology_gap_audit = json.load(handle)
    manifest = build_external_source_query_manifest(
        transfer_manifest=transfer_manifest,
        ontology_gap_audit=ontology_gap_audit,
        max_lanes=args.max_lanes,
    )
    write_json(Path(args.out), manifest)
    print(
        "Wrote external source query manifest to "
        f"{args.out} ({manifest['metadata']['lane_count']} lanes)"
    )
    return 0


def cmd_build_external_ood_calibration_plan(args: argparse.Namespace) -> int:
    with Path(args.query_manifest).open("r", encoding="utf-8") as handle:
        query_manifest = json.load(handle)
    with Path(args.sequence_similarity_failure_sets).open("r", encoding="utf-8") as handle:
        sequence_similarity_failure_sets = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    plan = build_external_ood_calibration_plan(
        query_manifest=query_manifest,
        sequence_similarity_failure_sets=sequence_similarity_failure_sets,
        labels=labels,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external OOD calibration plan to "
        f"{args.out} ({plan['metadata']['lane_count']} lanes)"
    )
    return 0


def cmd_build_external_source_candidate_sample(args: argparse.Namespace) -> int:
    with Path(args.query_manifest).open("r", encoding="utf-8") as handle:
        query_manifest = json.load(handle)
    sample = build_external_source_candidate_sample(
        query_manifest=query_manifest,
        max_records_per_lane=args.max_records_per_lane,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source candidate sample to "
        f"{args.out} ({sample['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_audit_external_source_candidate_sample(args: argparse.Namespace) -> int:
    with Path(args.candidate_sample).open("r", encoding="utf-8") as handle:
        candidate_sample = json.load(handle)
    audit = audit_external_source_candidate_sample(candidate_sample)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sample guardrail audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_candidate_manifest(args: argparse.Namespace) -> int:
    with Path(args.candidate_sample).open("r", encoding="utf-8") as handle:
        candidate_sample = json.load(handle)
    with Path(args.ood_calibration_plan).open("r", encoding="utf-8") as handle:
        ood_calibration_plan = json.load(handle)
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    with Path(args.sequence_similarity_failure_sets).open(
        "r", encoding="utf-8"
    ) as handle:
        sequence_similarity_failure_sets = json.load(handle)
    with Path(args.transfer_manifest).open("r", encoding="utf-8") as handle:
        transfer_manifest = json.load(handle)
    manifest = build_external_source_candidate_manifest(
        candidate_sample=candidate_sample,
        ood_calibration_plan=ood_calibration_plan,
        sequence_clusters=sequence_clusters,
        sequence_similarity_failure_sets=sequence_similarity_failure_sets,
        transfer_manifest=transfer_manifest,
    )
    write_json(Path(args.out), manifest)
    print(
        "Wrote external source candidate manifest to "
        f"{args.out} ({manifest['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_audit_external_source_candidate_manifest(args: argparse.Namespace) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    audit = audit_external_source_candidate_manifest(candidate_manifest)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source candidate manifest audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_audit_external_source_sequence_holdouts(args: argparse.Namespace) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    audit = audit_external_source_sequence_holdouts(
        candidate_manifest=candidate_manifest,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sequence holdout audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_evidence_plan(args: argparse.Namespace) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    with Path(args.candidate_manifest_audit).open("r", encoding="utf-8") as handle:
        candidate_manifest_audit = json.load(handle)
    plan = build_external_source_evidence_plan(
        candidate_manifest=candidate_manifest,
        candidate_manifest_audit=candidate_manifest_audit,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source evidence plan to "
        f"{args.out} ({plan['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_build_external_source_evidence_request_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.evidence_plan).open("r", encoding="utf-8") as handle:
        evidence_plan = json.load(handle)
    export = build_external_source_evidence_request_export(
        evidence_plan=evidence_plan,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote external source evidence request export to "
        f"{args.out} ({export['metadata']['exported_count']} rows)"
    )
    return 0


def cmd_build_external_source_active_site_evidence_queue(
    args: argparse.Namespace,
) -> int:
    with Path(args.evidence_plan).open("r", encoding="utf-8") as handle:
        evidence_plan = json.load(handle)
    queue = build_external_source_active_site_evidence_queue(
        evidence_plan=evidence_plan,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), queue)
    print(
        "Wrote external source active-site evidence queue to "
        f"{args.out} ({queue['metadata']['exported_ready_candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_active_site_evidence_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_evidence_queue).open("r", encoding="utf-8") as handle:
        active_site_evidence_queue = json.load(handle)
    sample = build_external_source_active_site_evidence_sample(
        active_site_evidence_queue=active_site_evidence_queue,
        max_candidates=args.max_candidates,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source active-site evidence sample to "
        f"{args.out} ({sample['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_audit_external_source_active_site_evidence_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    audit = audit_external_source_active_site_evidence_sample(
        active_site_evidence_sample
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source active-site evidence audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_heuristic_control_queue(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    queue = build_external_source_heuristic_control_queue(
        active_site_evidence_sample=active_site_evidence_sample,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), queue)
    print(
        "Wrote external source heuristic control queue to "
        f"{args.out} ({queue['metadata']['exported_ready_candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_heuristic_control_queue(
    args: argparse.Namespace,
) -> int:
    with Path(args.heuristic_control_queue).open("r", encoding="utf-8") as handle:
        heuristic_control_queue = json.load(handle)
    audit = audit_external_source_heuristic_control_queue(heuristic_control_queue)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source heuristic control queue audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_structure_mapping_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    with Path(args.heuristic_control_queue).open("r", encoding="utf-8") as handle:
        heuristic_control_queue = json.load(handle)
    plan = build_external_source_structure_mapping_plan(
        active_site_evidence_sample=active_site_evidence_sample,
        heuristic_control_queue=heuristic_control_queue,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source structure mapping plan to "
        f"{args.out} ({plan['metadata']['ready_mapping_candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_structure_mapping_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.structure_mapping_plan).open("r", encoding="utf-8") as handle:
        structure_mapping_plan = json.load(handle)
    audit = audit_external_source_structure_mapping_plan(structure_mapping_plan)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source structure mapping plan audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_structure_mapping_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.structure_mapping_plan).open("r", encoding="utf-8") as handle:
        structure_mapping_plan = json.load(handle)
    sample = build_external_source_structure_mapping_sample(
        structure_mapping_plan=structure_mapping_plan,
        max_candidates=args.max_candidates,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source structure mapping sample to "
        f"{args.out} ({sample['metadata']['mapped_candidate_count']} mapped)"
    )
    return 0


def cmd_audit_external_source_structure_mapping_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.structure_mapping_sample).open("r", encoding="utf-8") as handle:
        structure_mapping_sample = json.load(handle)
    audit = audit_external_source_structure_mapping_sample(structure_mapping_sample)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source structure mapping sample audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_heuristic_control_scores(
    args: argparse.Namespace,
) -> int:
    with Path(args.structure_mapping_sample).open("r", encoding="utf-8") as handle:
        structure_mapping_sample = json.load(handle)
    scores = build_external_source_heuristic_control_scores(
        structure_mapping_sample=structure_mapping_sample,
        top_k=args.top_k,
    )
    write_json(Path(args.out), scores)
    print(
        "Wrote external source heuristic control scores to "
        f"{args.out} ({scores['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_audit_external_source_heuristic_control_scores(
    args: argparse.Namespace,
) -> int:
    with Path(args.heuristic_control_scores).open("r", encoding="utf-8") as handle:
        heuristic_control_scores = json.load(handle)
    audit = audit_external_source_heuristic_control_scores(heuristic_control_scores)
    write_json(Path(args.out), audit)
    print(
        "Wrote external source heuristic control scores audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_audit_external_source_failure_modes(args: argparse.Namespace) -> int:
    with Path(args.active_site_evidence_sample_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        active_site_evidence_sample_audit = json.load(handle)
    with Path(args.heuristic_control_queue).open("r", encoding="utf-8") as handle:
        heuristic_control_queue = json.load(handle)
    with Path(args.heuristic_control_scores_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        heuristic_control_scores_audit = json.load(handle)
    with Path(args.structure_mapping_sample_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        structure_mapping_sample_audit = json.load(handle)
    audit = audit_external_source_failure_modes(
        active_site_evidence_sample_audit=active_site_evidence_sample_audit,
        heuristic_control_queue=heuristic_control_queue,
        heuristic_control_scores_audit=heuristic_control_scores_audit,
        structure_mapping_sample_audit=structure_mapping_sample_audit,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source failure mode audit to "
        f"{args.out} ({audit['metadata']['failure_mode_count']} modes)"
    )
    return 0


def cmd_build_external_source_control_repair_plan(args: argparse.Namespace) -> int:
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    with Path(args.heuristic_control_scores).open("r", encoding="utf-8") as handle:
        heuristic_control_scores = json.load(handle)
    with Path(args.heuristic_control_scores_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        heuristic_control_scores_audit = json.load(handle)
    with Path(args.external_failure_mode_audit).open("r", encoding="utf-8") as handle:
        external_failure_mode_audit = json.load(handle)
    plan = build_external_source_control_repair_plan(
        active_site_evidence_sample=active_site_evidence_sample,
        heuristic_control_scores=heuristic_control_scores,
        heuristic_control_scores_audit=heuristic_control_scores_audit,
        external_failure_mode_audit=external_failure_mode_audit,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source control repair plan to "
        f"{args.out} ({plan['metadata']['repair_row_count']} rows)"
    )
    return 0


def cmd_audit_external_source_control_repair_plan(args: argparse.Namespace) -> int:
    with Path(args.control_repair_plan).open("r", encoding="utf-8") as handle:
        control_repair_plan = json.load(handle)
    with Path(args.external_failure_mode_audit).open("r", encoding="utf-8") as handle:
        external_failure_mode_audit = json.load(handle)
    audit = audit_external_source_control_repair_plan(
        control_repair_plan=control_repair_plan,
        external_failure_mode_audit=external_failure_mode_audit,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source control repair plan audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_binding_context_repair_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    with Path(args.control_repair_plan).open("r", encoding="utf-8") as handle:
        control_repair_plan = json.load(handle)
    plan = build_external_source_binding_context_repair_plan(
        active_site_evidence_sample=active_site_evidence_sample,
        control_repair_plan=control_repair_plan,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source binding-context repair plan to "
        f"{args.out} ({plan['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_binding_context_repair_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.binding_context_repair_plan).open(
        "r", encoding="utf-8"
    ) as handle:
        binding_context_repair_plan = json.load(handle)
    audit = audit_external_source_binding_context_repair_plan(
        binding_context_repair_plan
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source binding-context repair audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_binding_context_mapping_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.binding_context_repair_plan).open(
        "r", encoding="utf-8"
    ) as handle:
        binding_context_repair_plan = json.load(handle)
    sample = build_external_source_binding_context_mapping_sample(
        binding_context_repair_plan=binding_context_repair_plan,
        max_candidates=args.max_candidates,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source binding-context mapping sample to "
        f"{args.out} ({sample['metadata']['mapped_candidate_count']} mapped)"
    )
    return 0


def cmd_audit_external_source_binding_context_mapping_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.binding_context_mapping_sample).open(
        "r", encoding="utf-8"
    ) as handle:
        binding_context_mapping_sample = json.load(handle)
    audit = audit_external_source_binding_context_mapping_sample(
        binding_context_mapping_sample
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source binding-context mapping audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_representation_control_manifest(
    args: argparse.Namespace,
) -> int:
    with Path(args.structure_mapping_sample).open("r", encoding="utf-8") as handle:
        structure_mapping_sample = json.load(handle)
    with Path(args.heuristic_control_scores).open("r", encoding="utf-8") as handle:
        heuristic_control_scores = json.load(handle)
    with Path(args.control_repair_plan).open("r", encoding="utf-8") as handle:
        control_repair_plan = json.load(handle)
    manifest = build_external_source_representation_control_manifest(
        structure_mapping_sample=structure_mapping_sample,
        heuristic_control_scores=heuristic_control_scores,
        control_repair_plan=control_repair_plan,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), manifest)
    print(
        "Wrote external source representation control manifest to "
        f"{args.out} ({manifest['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_representation_control_manifest(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_control_manifest).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_control_manifest = json.load(handle)
    audit = audit_external_source_representation_control_manifest(
        representation_control_manifest
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source representation control audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_representation_control_comparison(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_control_manifest).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_control_manifest = json.load(handle)
    with Path(args.heuristic_control_scores).open("r", encoding="utf-8") as handle:
        heuristic_control_scores = json.load(handle)
    with Path(args.reaction_evidence_sample).open("r", encoding="utf-8") as handle:
        reaction_evidence_sample = json.load(handle)
    comparison = build_external_source_representation_control_comparison(
        representation_control_manifest=representation_control_manifest,
        heuristic_control_scores=heuristic_control_scores,
        reaction_evidence_sample=reaction_evidence_sample,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), comparison)
    print(
        "Wrote external source representation control comparison to "
        f"{args.out} ({comparison['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_representation_control_comparison(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_control_comparison).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_control_comparison = json.load(handle)
    audit = audit_external_source_representation_control_comparison(
        representation_control_comparison
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source representation control comparison audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_representation_backend_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_control_manifest).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_control_manifest = json.load(handle)
    with Path(args.representation_control_comparison).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_control_comparison = json.load(handle)
    with Path(args.sequence_search_export).open("r", encoding="utf-8") as handle:
        sequence_search_export = json.load(handle)
    plan = build_external_source_representation_backend_plan(
        representation_control_manifest=representation_control_manifest,
        representation_control_comparison=representation_control_comparison,
        sequence_search_export=sequence_search_export,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source representation backend plan to "
        f"{args.out} ({plan['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_pilot_representation_backend_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.pilot_candidate_priority).open("r", encoding="utf-8") as handle:
        pilot_candidate_priority = json.load(handle)
    with Path(args.sequence_search_export).open("r", encoding="utf-8") as handle:
        sequence_search_export = json.load(handle)
    plan = build_external_source_pilot_representation_backend_plan(
        pilot_candidate_priority=pilot_candidate_priority,
        sequence_search_export=sequence_search_export,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source pilot representation backend plan to "
        f"{args.out} ({plan['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_representation_backend_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_backend_plan).open("r", encoding="utf-8") as handle:
        representation_backend_plan = json.load(handle)
    audit = audit_external_source_representation_backend_plan(
        representation_backend_plan
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source representation backend plan audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_representation_backend_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_backend_plan).open("r", encoding="utf-8") as handle:
        representation_backend_plan = json.load(handle)
    with Path(args.sequence_neighborhood_sample).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_sample = json.load(handle)
    sample = build_external_source_representation_backend_sample(
        representation_backend_plan=representation_backend_plan,
        sequence_neighborhood_sample=sequence_neighborhood_sample,
        max_rows=args.max_rows,
        top_k=args.top_k,
        embedding_backend=args.embedding_backend,
        model_name=args.model_name,
        local_files_only=args.local_files_only,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source representation backend sample to "
        f"{args.out} ({sample['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_representation_backend_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.representation_backend_sample).open(
        "r", encoding="utf-8"
    ) as handle:
        representation_backend_sample = json.load(handle)
    audit = audit_external_source_representation_backend_sample(
        representation_backend_sample
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source representation backend sample audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_audit_external_source_representation_backend_stability(
    args: argparse.Namespace,
) -> int:
    with Path(args.baseline_representation_backend_sample).open(
        "r", encoding="utf-8"
    ) as handle:
        baseline_representation_backend_sample = json.load(handle)
    with Path(args.comparison_representation_backend_sample).open(
        "r", encoding="utf-8"
    ) as handle:
        comparison_representation_backend_sample = json.load(handle)
    audit = audit_external_source_representation_backend_stability(
        baseline_representation_backend_sample=(
            baseline_representation_backend_sample
        ),
        comparison_representation_backend_sample=(
            comparison_representation_backend_sample
        ),
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source representation backend stability audit to "
        f"{args.out} (status={audit['metadata']['stability_status']})"
    )
    return 0


def cmd_audit_external_source_pilot_representation_adjudication(
    args: argparse.Namespace,
) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "pilot_candidate_priority",
            "pilot_representation_backend_sample",
            "pilot_representation_stability_audit",
            "pilot_active_site_evidence_decisions",
        ),
        blocker_removed=(
            "selected_pilot_representation_controls_adjudicated_from_stability"
        ),
    )
    audit = audit_external_source_pilot_representation_adjudication(
        pilot_candidate_priority=artifact_payloads["pilot_candidate_priority"],
        pilot_representation_backend_sample=artifact_payloads[
            "pilot_representation_backend_sample"
        ],
        pilot_representation_stability_audit=artifact_payloads[
            "pilot_representation_stability_audit"
        ],
        pilot_active_site_evidence_decisions=artifact_payloads[
            "pilot_active_site_evidence_decisions"
        ],
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source pilot representation adjudication to "
        f"{args.out} ("
        f"{audit['metadata']['representation_control_unresolved_count']} "
        "unresolved representation rows)"
    )
    return 0


def cmd_audit_external_source_broad_ec_disambiguation(
    args: argparse.Namespace,
) -> int:
    with Path(args.control_repair_plan).open("r", encoding="utf-8") as handle:
        control_repair_plan = json.load(handle)
    with Path(args.reaction_evidence_sample).open("r", encoding="utf-8") as handle:
        reaction_evidence_sample = json.load(handle)
    audit = audit_external_source_broad_ec_disambiguation(
        control_repair_plan=control_repair_plan,
        reaction_evidence_sample=reaction_evidence_sample,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source broad-EC disambiguation audit to "
        f"{args.out} ({audit['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_active_site_gap_source_requests(
    args: argparse.Namespace,
) -> int:
    with Path(args.control_repair_plan).open("r", encoding="utf-8") as handle:
        control_repair_plan = json.load(handle)
    with Path(args.binding_context_repair_plan).open("r", encoding="utf-8") as handle:
        binding_context_repair_plan = json.load(handle)
    with Path(args.binding_context_mapping_sample).open(
        "r", encoding="utf-8"
    ) as handle:
        binding_context_mapping_sample = json.load(handle)
    requests = build_external_source_active_site_gap_source_requests(
        control_repair_plan=control_repair_plan,
        binding_context_repair_plan=binding_context_repair_plan,
        binding_context_mapping_sample=binding_context_mapping_sample,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), requests)
    print(
        "Wrote external source active-site gap source requests to "
        f"{args.out} ({requests['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_sequence_neighborhood_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    with Path(args.sequence_holdout_audit).open("r", encoding="utf-8") as handle:
        sequence_holdout_audit = json.load(handle)
    plan = build_external_source_sequence_neighborhood_plan(
        candidate_manifest=candidate_manifest,
        sequence_holdout_audit=sequence_holdout_audit,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote external source sequence neighborhood plan to "
        f"{args.out} ({plan['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_sequence_neighborhood_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_neighborhood_plan).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_plan = json.load(handle)
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    sample = build_external_source_sequence_neighborhood_sample(
        sequence_neighborhood_plan=sequence_neighborhood_plan,
        sequence_clusters=sequence_clusters,
        labels=labels,
        max_external_rows=args.max_external_rows,
        max_reference_sequences=args.max_reference_sequences,
        top_k=args.top_k,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source sequence neighborhood sample to "
        f"{args.out} ({sample['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_sequence_neighborhood_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_neighborhood_sample).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_sample = json.load(handle)
    audit = audit_external_source_sequence_neighborhood_sample(
        sequence_neighborhood_sample
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sequence neighborhood sample audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_sequence_alignment_verification(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_neighborhood_sample).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_sample = json.load(handle)
    verification = build_external_source_sequence_alignment_verification(
        sequence_neighborhood_sample=sequence_neighborhood_sample,
        top_k=args.top_k,
        max_pairs=args.max_pairs,
        max_alignment_cells=args.max_alignment_cells,
    )
    write_json(Path(args.out), verification)
    print(
        "Wrote external source sequence alignment verification to "
        f"{args.out} ({verification['metadata']['verified_pair_count']} pairs)"
    )
    return 0


def cmd_audit_external_source_sequence_alignment_verification(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_alignment_verification).open(
        "r", encoding="utf-8"
    ) as handle:
        sequence_alignment_verification = json.load(handle)
    audit = audit_external_source_sequence_alignment_verification(
        sequence_alignment_verification
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sequence alignment verification audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_audit_external_source_sequence_reference_screen(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_neighborhood_sample).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_sample = json.load(handle)
    with Path(args.sequence_alignment_verification).open(
        "r", encoding="utf-8"
    ) as handle:
        sequence_alignment_verification = json.load(handle)
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    audit = audit_external_source_sequence_reference_screen(
        sequence_neighborhood_sample=sequence_neighborhood_sample,
        sequence_alignment_verification=sequence_alignment_verification,
        sequence_clusters=sequence_clusters,
        labels=labels,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sequence reference screen audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_backend_sequence_search(
    args: argparse.Namespace,
) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        labels = json.load(handle)
    search = build_external_source_backend_sequence_search(
        candidate_manifest=candidate_manifest,
        sequence_clusters=sequence_clusters,
        labels=labels,
        reference_fasta=args.reference_fasta,
        external_fasta_out=args.external_fasta_out,
        reference_fasta_out=args.reference_fasta_out,
        result_tsv_out=args.result_tsv_out,
        backend=args.backend,
        mmseqs_binary=args.mmseqs_binary,
        diamond_binary=args.diamond_binary,
        blastp_binary=args.blastp_binary,
        makeblastdb_binary=args.makeblastdb_binary,
        identity_threshold=args.identity_threshold,
        coverage_threshold=args.coverage_threshold,
        exact_identity_threshold=args.exact_identity_threshold,
        exact_coverage_threshold=args.exact_coverage_threshold,
        max_rows=args.max_rows,
        top_k=args.top_k,
    )
    write_json(Path(args.out), search)
    print(
        "Wrote external source backend sequence search to "
        f"{args.out} ({search['metadata']['backend_name']}, "
        f"{search['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_backend_sequence_search(
    args: argparse.Namespace,
) -> int:
    with Path(args.backend_sequence_search).open("r", encoding="utf-8") as handle:
        backend_sequence_search = json.load(handle)
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    audit = audit_external_source_backend_sequence_search(
        backend_sequence_search=backend_sequence_search,
        candidate_manifest=candidate_manifest,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source backend sequence search audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_sequence_search_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_neighborhood_plan).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_plan = json.load(handle)
    with Path(args.sequence_neighborhood_sample).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_sample = json.load(handle)
    with Path(args.sequence_alignment_verification).open(
        "r", encoding="utf-8"
    ) as handle:
        sequence_alignment_verification = json.load(handle)
    sequence_reference_screen_audit = None
    if args.sequence_reference_screen_audit:
        with Path(args.sequence_reference_screen_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            sequence_reference_screen_audit = json.load(handle)
    export = build_external_source_sequence_search_export(
        sequence_neighborhood_plan=sequence_neighborhood_plan,
        sequence_neighborhood_sample=sequence_neighborhood_sample,
        sequence_alignment_verification=sequence_alignment_verification,
        sequence_reference_screen_audit=sequence_reference_screen_audit,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote external source sequence search export to "
        f"{args.out} ({export['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_sequence_search_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.sequence_search_export).open("r", encoding="utf-8") as handle:
        sequence_search_export = json.load(handle)
    with Path(args.sequence_neighborhood_plan).open("r", encoding="utf-8") as handle:
        sequence_neighborhood_plan = json.load(handle)
    audit = audit_external_source_sequence_search_export(
        sequence_search_export=sequence_search_export,
        sequence_neighborhood_plan=sequence_neighborhood_plan,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source sequence search export audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_active_site_sourcing_queue(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_gap_source_requests).open(
        "r", encoding="utf-8"
    ) as handle:
        active_site_gap_source_requests = json.load(handle)
    with Path(args.external_import_readiness_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        external_import_readiness_audit = json.load(handle)
    sequence_alignment_verification = None
    if args.sequence_alignment_verification:
        with Path(args.sequence_alignment_verification).open(
            "r", encoding="utf-8"
        ) as handle:
            sequence_alignment_verification = json.load(handle)
    queue = build_external_source_active_site_sourcing_queue(
        active_site_gap_source_requests=active_site_gap_source_requests,
        external_import_readiness_audit=external_import_readiness_audit,
        sequence_alignment_verification=sequence_alignment_verification,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), queue)
    print(
        "Wrote external source active-site sourcing queue to "
        f"{args.out} ({queue['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_active_site_sourcing_queue(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_sourcing_queue).open("r", encoding="utf-8") as handle:
        active_site_sourcing_queue = json.load(handle)
    with Path(args.external_import_readiness_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        external_import_readiness_audit = json.load(handle)
    audit = audit_external_source_active_site_sourcing_queue(
        active_site_sourcing_queue=active_site_sourcing_queue,
        external_import_readiness_audit=external_import_readiness_audit,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source active-site sourcing queue audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_active_site_sourcing_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_sourcing_queue).open("r", encoding="utf-8") as handle:
        active_site_sourcing_queue = json.load(handle)
    with Path(args.active_site_gap_source_requests).open(
        "r", encoding="utf-8"
    ) as handle:
        active_site_gap_source_requests = json.load(handle)
    with Path(args.active_site_evidence_sample).open("r", encoding="utf-8") as handle:
        active_site_evidence_sample = json.load(handle)
    with Path(args.reaction_evidence_sample).open("r", encoding="utf-8") as handle:
        reaction_evidence_sample = json.load(handle)
    export = build_external_source_active_site_sourcing_export(
        active_site_sourcing_queue=active_site_sourcing_queue,
        active_site_gap_source_requests=active_site_gap_source_requests,
        active_site_evidence_sample=active_site_evidence_sample,
        reaction_evidence_sample=reaction_evidence_sample,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote external source active-site sourcing export to "
        f"{args.out} ({export['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_active_site_sourcing_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_sourcing_export).open("r", encoding="utf-8") as handle:
        active_site_sourcing_export = json.load(handle)
    with Path(args.active_site_sourcing_queue).open("r", encoding="utf-8") as handle:
        active_site_sourcing_queue = json.load(handle)
    audit = audit_external_source_active_site_sourcing_export(
        active_site_sourcing_export=active_site_sourcing_export,
        active_site_sourcing_queue=active_site_sourcing_queue,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source active-site sourcing export audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_active_site_sourcing_resolution(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_sourcing_export).open("r", encoding="utf-8") as handle:
        active_site_sourcing_export = json.load(handle)
    resolution = build_external_source_active_site_sourcing_resolution(
        active_site_sourcing_export=active_site_sourcing_export,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), resolution)
    print(
        "Wrote external source active-site sourcing resolution to "
        f"{args.out} ({resolution['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_active_site_sourcing_resolution(
    args: argparse.Namespace,
) -> int:
    with Path(args.active_site_sourcing_resolution).open(
        "r", encoding="utf-8"
    ) as handle:
        active_site_sourcing_resolution = json.load(handle)
    with Path(args.active_site_sourcing_export).open("r", encoding="utf-8") as handle:
        active_site_sourcing_export = json.load(handle)
    audit = audit_external_source_active_site_sourcing_resolution(
        active_site_sourcing_resolution=active_site_sourcing_resolution,
        active_site_sourcing_export=active_site_sourcing_export,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source active-site sourcing resolution audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_transfer_blocker_matrix(
    args: argparse.Namespace,
) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "candidate_manifest",
            "external_import_readiness_audit",
            "active_site_sourcing_export",
            "sequence_search_export",
            "representation_backend_plan",
            "backend_sequence_search",
            "active_site_sourcing_resolution",
            "representation_backend_sample",
        ),
        blocker_removed="artifact_graph_consistency_for_external_blocker_matrix",
    )
    matrix = build_external_source_transfer_blocker_matrix(
        candidate_manifest=artifact_payloads["candidate_manifest"],
        external_import_readiness_audit=artifact_payloads[
            "external_import_readiness_audit"
        ],
        active_site_sourcing_export=artifact_payloads["active_site_sourcing_export"],
        sequence_search_export=artifact_payloads["sequence_search_export"],
        representation_backend_plan=artifact_payloads["representation_backend_plan"],
        backend_sequence_search=artifact_payloads["backend_sequence_search"],
        active_site_sourcing_resolution=artifact_payloads[
            "active_site_sourcing_resolution"
        ],
        representation_backend_sample=artifact_payloads[
            "representation_backend_sample"
        ],
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), matrix)
    print(
        "Wrote external source transfer blocker matrix to "
        f"{args.out} ({matrix['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_audit_external_source_transfer_blocker_matrix(
    args: argparse.Namespace,
) -> int:
    with Path(args.transfer_blocker_matrix).open("r", encoding="utf-8") as handle:
        transfer_blocker_matrix = json.load(handle)
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    audit = audit_external_source_transfer_blocker_matrix(
        transfer_blocker_matrix=transfer_blocker_matrix,
        candidate_manifest=candidate_manifest,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source transfer blocker matrix audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_external_source_pilot_candidate_priority(args: argparse.Namespace) -> int:
    with Path(args.transfer_blocker_matrix).open("r", encoding="utf-8") as handle:
        transfer_blocker_matrix = json.load(handle)
    priority = build_external_source_pilot_candidate_priority(
        transfer_blocker_matrix,
        max_candidates=args.max_candidates,
        max_per_lane=args.max_per_lane,
    )
    write_json(Path(args.out), priority)
    print(
        "Wrote external source pilot candidate priority to "
        f"{args.out} ({priority['metadata']['selected_candidate_count']} selected)"
    )
    return 0


def cmd_build_external_source_pilot_review_decision_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.pilot_candidate_priority).open("r", encoding="utf-8") as handle:
        pilot_candidate_priority = json.load(handle)
    export = build_external_source_pilot_review_decision_export(
        pilot_candidate_priority=pilot_candidate_priority,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote external source pilot review-decision export to "
        f"{args.out} ({export['metadata']['candidate_count']} review items)"
    )
    return 0


def cmd_audit_external_source_import_readiness(args: argparse.Namespace) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "candidate_manifest",
            "active_site_evidence_sample",
            "heuristic_control_scores",
            "representation_control_comparison",
            "active_site_gap_source_requests",
            "sequence_neighborhood_sample",
            "sequence_alignment_verification",
            "backend_sequence_search",
        ),
        blocker_removed="artifact_graph_consistency_for_external_import_readiness",
    )
    audit = audit_external_source_import_readiness(
        candidate_manifest=artifact_payloads["candidate_manifest"],
        active_site_evidence_sample=artifact_payloads["active_site_evidence_sample"],
        heuristic_control_scores=artifact_payloads["heuristic_control_scores"],
        representation_control_comparison=artifact_payloads[
            "representation_control_comparison"
        ],
        active_site_gap_source_requests=artifact_payloads[
            "active_site_gap_source_requests"
        ],
        sequence_neighborhood_sample=artifact_payloads["sequence_neighborhood_sample"],
        sequence_alignment_verification=artifact_payloads[
            "sequence_alignment_verification"
        ],
        backend_sequence_search=artifact_payloads["backend_sequence_search"],
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source import readiness audit to "
        f"{args.out} ({audit['metadata']['candidate_count']} rows)"
    )
    return 0


def cmd_build_external_source_pilot_evidence_packet(args: argparse.Namespace) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "pilot_candidate_priority",
            "active_site_sourcing_export",
            "sequence_search_export",
            "backend_sequence_search",
        ),
        blocker_removed="artifact_graph_consistency_for_external_pilot_packet",
    )
    packet = build_external_source_pilot_evidence_packet(
        pilot_candidate_priority=artifact_payloads["pilot_candidate_priority"],
        active_site_sourcing_export=artifact_payloads["active_site_sourcing_export"],
        sequence_search_export=artifact_payloads["sequence_search_export"],
        backend_sequence_search=artifact_payloads["backend_sequence_search"],
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), packet)
    print(
        "Wrote external source pilot evidence packet to "
        f"{args.out} ({packet['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_build_external_source_pilot_evidence_dossiers(
    args: argparse.Namespace,
) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "pilot_evidence_packet",
            "active_site_evidence_sample",
            "active_site_sourcing_resolution",
            "reaction_evidence_sample",
            "sequence_alignment_verification",
            "representation_backend_sample",
            "heuristic_control_scores",
            "structure_mapping_sample",
            "transfer_blocker_matrix",
            "external_import_readiness_audit",
        ),
        blocker_removed="artifact_graph_consistency_for_external_pilot_dossiers",
    )
    pilot_evidence_packet = artifact_payloads["pilot_evidence_packet"]
    active_site_evidence_sample = artifact_payloads["active_site_evidence_sample"]
    active_site_sourcing_resolution = artifact_payloads[
        "active_site_sourcing_resolution"
    ]
    reaction_evidence_sample = artifact_payloads["reaction_evidence_sample"]
    sequence_alignment_verification = artifact_payloads[
        "sequence_alignment_verification"
    ]
    representation_backend_sample = artifact_payloads["representation_backend_sample"]
    heuristic_control_scores = artifact_payloads["heuristic_control_scores"]
    structure_mapping_sample = artifact_payloads["structure_mapping_sample"]
    transfer_blocker_matrix = artifact_payloads["transfer_blocker_matrix"]
    external_import_readiness_audit = artifact_payloads["external_import_readiness_audit"]
    dossiers = build_external_source_pilot_evidence_dossiers(
        pilot_evidence_packet=pilot_evidence_packet,
        active_site_evidence_sample=active_site_evidence_sample,
        active_site_sourcing_resolution=active_site_sourcing_resolution,
        reaction_evidence_sample=reaction_evidence_sample,
        sequence_alignment_verification=sequence_alignment_verification,
        representation_backend_sample=representation_backend_sample,
        heuristic_control_scores=heuristic_control_scores,
        structure_mapping_sample=structure_mapping_sample,
        transfer_blocker_matrix=transfer_blocker_matrix,
        external_import_readiness_audit=external_import_readiness_audit,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), dossiers)
    print(
        "Wrote external source pilot evidence dossiers to "
        f"{args.out} ({dossiers['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_build_external_source_pilot_active_site_evidence_decisions(
    args: argparse.Namespace,
) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "pilot_evidence_dossiers",
            "pilot_evidence_packet",
            "active_site_sourcing_resolution",
            "reaction_evidence_sample",
            "backend_sequence_search",
            "pilot_representation_backend_sample",
            "transfer_blocker_matrix",
        ),
        blocker_removed="external_pilot_active_site_source_status_ambiguity",
    )
    decisions = build_external_source_pilot_active_site_evidence_decisions(
        pilot_evidence_dossiers=artifact_payloads["pilot_evidence_dossiers"],
        pilot_evidence_packet=artifact_payloads["pilot_evidence_packet"],
        active_site_sourcing_resolution=artifact_payloads[
            "active_site_sourcing_resolution"
        ],
        reaction_evidence_sample=artifact_payloads["reaction_evidence_sample"],
        backend_sequence_search=artifact_payloads["backend_sequence_search"],
        pilot_representation_backend_sample=artifact_payloads[
            "pilot_representation_backend_sample"
        ],
        transfer_blocker_matrix=artifact_payloads["transfer_blocker_matrix"],
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), decisions)
    print(
        "Wrote external source pilot active-site evidence decisions to "
        f"{args.out} ({decisions['metadata']['candidate_count']} candidates)"
    )
    return 0


def cmd_build_external_source_pilot_success_criteria(
    args: argparse.Namespace,
) -> int:
    artifact_payloads, artifact_lineage = _load_external_lineaged_artifacts(
        args,
        (
            "pilot_candidate_priority",
            "pilot_review_decision_export",
            "pilot_active_site_evidence_decisions",
            "external_import_readiness_audit",
            "external_transfer_gate",
            "pilot_representation_adjudication",
        ),
        blocker_removed="external_pilot_success_criteria_defined",
    )
    criteria = build_external_source_pilot_success_criteria(
        pilot_candidate_priority=artifact_payloads["pilot_candidate_priority"],
        pilot_review_decision_export=artifact_payloads[
            "pilot_review_decision_export"
        ],
        pilot_active_site_evidence_decisions=artifact_payloads[
            "pilot_active_site_evidence_decisions"
        ],
        external_import_readiness_audit=artifact_payloads[
            "external_import_readiness_audit"
        ],
        external_transfer_gate=artifact_payloads["external_transfer_gate"],
        pilot_representation_adjudication=artifact_payloads.get(
            "pilot_representation_adjudication"
        ),
        min_import_ready_rows=args.min_import_ready_rows,
        max_rows=args.max_rows,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), criteria)
    print(
        "Wrote external source pilot success criteria to "
        f"{args.out} (status={criteria['metadata']['pilot_status']})"
    )
    return 0


def cmd_check_external_source_transfer_gates(args: argparse.Namespace) -> int:
    artifact_names = tuple(
        name
        for name in ExternalSourceTransferGateInputs.__dataclass_fields__
        if name != "artifact_path_lineage"
    )
    artifact_paths = {name: getattr(args, name, None) for name in artifact_names}
    artifact_payloads = {
        name: read_json_object(Path(path)) if path else None
        for name, path in artifact_paths.items()
    }
    artifact_path_lineage = validate_external_transfer_artifact_path_lineage(
        artifact_paths,
        artifact_payloads,
        fail_fast=True,
    )
    artifact_payloads["artifact_path_lineage"] = artifact_path_lineage
    gates = check_external_source_transfer_gates(
        ExternalSourceTransferGateInputs(**artifact_payloads)
    )
    write_json(Path(args.out), gates)
    print(
        "Wrote external source transfer gate check to "
        f"{args.out} ({gates['metadata']['passed_gate_count']}/"
        f"{gates['metadata']['gate_count']} gates)"
    )
    return 0


def cmd_build_external_source_reaction_evidence_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.evidence_request_export).open("r", encoding="utf-8") as handle:
        evidence_request_export = json.load(handle)
    sample = build_external_source_reaction_evidence_sample(
        evidence_request_export=evidence_request_export,
        max_candidates=args.max_candidates,
        max_reactions_per_ec=args.max_reactions_per_ec,
    )
    write_json(Path(args.out), sample)
    print(
        "Wrote external source reaction evidence sample to "
        f"{args.out} ({sample['metadata']['reaction_record_count']} reactions)"
    )
    return 0


def cmd_audit_external_source_reaction_evidence_sample(
    args: argparse.Namespace,
) -> int:
    with Path(args.reaction_evidence_sample).open("r", encoding="utf-8") as handle:
        reaction_evidence_sample = json.load(handle)
    audit = audit_external_source_reaction_evidence_sample(
        reaction_evidence_sample
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source reaction evidence audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_audit_external_source_lane_balance(args: argparse.Namespace) -> int:
    with Path(args.candidate_manifest).open("r", encoding="utf-8") as handle:
        candidate_manifest = json.load(handle)
    audit = audit_external_source_lane_balance(
        candidate_manifest=candidate_manifest,
        min_lanes=args.min_lanes,
        max_dominant_lane_fraction=args.max_dominant_lane_fraction,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote external source lane-balance audit to "
        f"{args.out} (clean={audit['metadata']['guardrail_clean']})"
    )
    return 0


def cmd_build_v2_benchmark(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph))
    benchmark = build_mechanism_benchmark(graph)
    write_json(Path(args.out), benchmark)
    print(f"Wrote {benchmark['metadata']['record_count']} benchmark records to {args.out}")
    return 0


def cmd_run_baseline(args: argparse.Namespace) -> int:
    with Path(args.benchmark).open("r", encoding="utf-8") as handle:
        benchmark = json.load(handle)
    baseline = run_baseline_retrieval(benchmark)
    write_json(Path(args.out), baseline)
    print(f"Wrote baseline results to {args.out}")
    return 0


def cmd_detect_inconsistencies(args: argparse.Namespace) -> int:
    graph = load_graph(Path(args.graph))
    inconsistencies = detect_inconsistencies(graph)
    write_json(Path(args.out), inconsistencies)
    print(f"Wrote {inconsistencies['metadata']['issue_count']} issues to {args.out}")
    return 0


def cmd_mine_dark_hydrolases(args: argparse.Namespace) -> int:
    candidates = mine_dark_hydrolase_candidates(limit=args.limit)
    write_json(Path(args.out), candidates)
    print(f"Wrote {candidates['metadata']['record_count']} candidates to {args.out}")
    return 0


def cmd_write_dossiers(args: argparse.Namespace) -> int:
    with Path(args.candidates).open("r", encoding="utf-8") as handle:
        candidates = json.load(handle)
    written = write_candidate_dossiers(candidates, Path(args.out_dir), top=args.top)
    print(f"Wrote {len(written)} dossiers to {args.out_dir}")
    return 0


def cmd_write_v2_report(args: argparse.Namespace) -> int:
    with Path(args.graph_summary).open("r", encoding="utf-8") as handle:
        graph_summary = json.load(handle)
    with Path(args.benchmark).open("r", encoding="utf-8") as handle:
        benchmark = json.load(handle)
    with Path(args.baseline).open("r", encoding="utf-8") as handle:
        baseline = json.load(handle)
    with Path(args.inconsistencies).open("r", encoding="utf-8") as handle:
        inconsistencies = json.load(handle)
    with Path(args.candidates).open("r", encoding="utf-8") as handle:
        candidates = json.load(handle)
    report = write_v2_report(
        graph_summary=graph_summary,
        benchmark=benchmark,
        baseline=baseline,
        inconsistencies=inconsistencies,
        candidates=candidates,
    )
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(report, encoding="utf-8")
    print(f"Wrote V2 report to {args.out}")
    return 0


def cmd_build_geometry_features(args: argparse.Namespace) -> int:
    features = write_geometry_features(
        graph_path=Path(args.graph),
        out_path=Path(args.out),
        max_entries=args.max_entries,
        reuse_existing_path=Path(args.reuse_existing) if args.reuse_existing else None,
        selected_pdb_overrides_path=(
            Path(args.selected_pdb_overrides) if args.selected_pdb_overrides else None
        ),
    )
    print(
        "Wrote geometry features to "
        f"{args.out} ({features['metadata']['entry_count']} entries, "
        f"{features['metadata']['entries_with_pairwise_geometry']} with pairwise geometry)"
    )
    return 0


def cmd_run_geometry_retrieval(args: argparse.Namespace) -> int:
    artifact = write_geometry_retrieval(
        geometry_path=Path(args.geometry),
        out_path=Path(args.out),
        top_k=args.top_k,
    )
    print(
        "Wrote geometry retrieval to "
        f"{args.out} ({artifact['metadata']['entry_count']} entries)"
    )
    return 0


def cmd_label_summary(args: argparse.Namespace) -> int:
    labels = load_labels(Path(args.labels))
    write_json(Path(args.out), label_summary(labels))
    print(f"Wrote label summary to {args.out}")
    return 0


def cmd_migrate_label_registry(args: argparse.Namespace) -> int:
    with Path(args.labels).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("label registry must be a list")
    migrated = migrate_label_registry_records(data)
    write_label_registry(Path(args.out), migrated)
    print(f"Wrote migrated label registry to {args.out} ({len(migrated)} labels)")
    return 0


def cmd_filter_countable_labels(args: argparse.Namespace) -> int:
    labels = load_labels(Path(args.labels))
    countable = countable_benchmark_labels(labels)
    non_countable_count = len(labels) - len(countable)
    if non_countable_count and not args.allow_pending_review:
        print(
            "Refusing to filter a registry with "
            f"{non_countable_count} non-countable review records; use "
            "import-countable-label-review for label-review batches or pass "
            "--allow-pending-review for an intentional lossy filter."
        )
        return 2
    write_label_registry(Path(args.out), [label.to_dict() for label in countable])
    print(f"Wrote countable label registry to {args.out} ({len(countable)} labels)")
    return 0


def cmd_evaluate_geometry_labels(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    evaluation = evaluate_geometry_retrieval(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
    )
    write_json(Path(args.out), evaluation)
    print(
        "Wrote geometry label evaluation to "
        f"{args.out} ({evaluation['metadata']['evaluated_count']} entries)"
    )
    return 0


def cmd_calibrate_abstention(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    thresholds = (
        None
        if args.thresholds == "auto"
        else [float(item) for item in args.thresholds.split(",") if item.strip()]
    )
    calibration = sweep_abstention_thresholds(
        retrieval,
        load_labels(Path(args.labels)),
        thresholds=thresholds,
    )
    write_json(Path(args.out), calibration)
    print(
        "Wrote abstention calibration to "
        f"{args.out} (selected={calibration['metadata']['selected_threshold']})"
    )
    return 0


def cmd_analyze_geometry_failures(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_out_of_scope_failures(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote geometry failure analysis to "
        f"{args.out} ({analysis['metadata']['false_non_abstentions']} false non-abstentions)"
    )
    return 0


def cmd_analyze_in_scope_failures(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_in_scope_failures(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote in-scope geometry failure analysis to "
        f"{args.out} ({analysis['metadata']['failure_count']} failures)"
    )
    return 0


def cmd_analyze_cofactor_coverage(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_cofactor_coverage(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote cofactor coverage analysis to "
        f"{args.out} ({analysis['metadata']['evaluated_in_scope_count']} in-scope entries)"
    )
    return 0


def cmd_analyze_cofactor_policy(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_cofactor_abstention_policy(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
        absent_penalties=_parse_float_list(args.absent_penalties),
        structure_only_penalties=_parse_float_list(args.structure_only_penalties),
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote cofactor policy analysis to "
        f"{args.out} ({analysis['metadata']['recommendation']})"
    )
    return 0


def cmd_analyze_seed_family_performance(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_seed_family_performance(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote seed-family performance audit to "
        f"{args.out} ({analysis['metadata']['in_scope_family_count']} families)"
    )
    return 0


def cmd_analyze_geometry_score_margins(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    analysis = analyze_geometry_score_margins(
        retrieval,
        load_labels(Path(args.labels)),
        near_margin=args.near_margin,
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote geometry score margin analysis to "
        f"{args.out} (gap={analysis['metadata']['score_separation_gap']})"
    )
    return 0


def cmd_build_hard_negative_controls(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    controls = build_hard_negative_controls(
        retrieval,
        load_labels(Path(args.labels)),
        score_floor=args.score_floor,
        near_margin=args.near_margin,
    )
    write_json(Path(args.out), controls)
    print(
        "Wrote hard negative controls to "
        f"{args.out} ({controls['metadata']['hard_negative_count']} controls, "
        f"{controls['metadata']['near_miss_count']} near misses)"
    )
    return 0


def cmd_build_label_expansion_candidates(args: argparse.Namespace) -> int:
    with Path(args.geometry).open("r", encoding="utf-8") as handle:
        geometry = json.load(handle)
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    candidates = build_label_expansion_candidates(
        geometry,
        retrieval,
        load_labels(Path(args.labels)),
    )
    write_json(Path(args.out), candidates)
    print(
        "Wrote label expansion candidates to "
        f"{args.out} ({candidates['metadata']['ready_for_label_review_count']} ready)"
    )
    return 0


def cmd_build_label_factory_audit(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    hard_negatives = None
    if args.hard_negatives:
        with Path(args.hard_negatives).open("r", encoding="utf-8") as handle:
            hard_negatives = json.load(handle)
    adversarial_negatives = None
    if args.adversarial_negatives:
        with Path(args.adversarial_negatives).open("r", encoding="utf-8") as handle:
            adversarial_negatives = json.load(handle)
    audit = build_label_factory_audit(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
        hard_negative_controls=hard_negatives,
        adversarial_negatives=adversarial_negatives,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote label factory audit to "
        f"{args.out} ({audit['metadata']['promote_to_silver_count']} promotions)"
    )
    return 0


def cmd_apply_label_factory_actions(args: argparse.Namespace) -> int:
    with Path(args.label_factory_audit).open("r", encoding="utf-8") as handle:
        audit = json.load(handle)
    applied = apply_label_factory_actions(load_labels(Path(args.labels)), audit)
    write_json(Path(args.out), applied)
    print(
        "Wrote applied label factory actions to "
        f"{args.out} ({applied['metadata']['output_label_count']} labels)"
    )
    return 0


def cmd_build_active_learning_queue(args: argparse.Namespace) -> int:
    with Path(args.geometry).open("r", encoding="utf-8") as handle:
        geometry = json.load(handle)
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    factory = None
    if args.label_factory_audit:
        with Path(args.label_factory_audit).open("r", encoding="utf-8") as handle:
            factory = json.load(handle)
    queue = build_active_learning_review_queue(
        geometry,
        retrieval,
        load_labels(Path(args.labels)),
        label_factory_audit=factory,
        abstain_threshold=args.abstain_threshold,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), queue)
    print(
        "Wrote active-learning review queue to "
        f"{args.out} ({queue['metadata']['queued_count']} queued)"
    )
    return 0


def cmd_build_adversarial_negatives(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    controls = build_adversarial_negative_controls(
        retrieval,
        load_labels(Path(args.labels)),
        abstain_threshold=args.abstain_threshold,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), controls)
    print(
        "Wrote adversarial negative controls to "
        f"{args.out} ({controls['metadata']['control_count']} controls)"
    )
    return 0


def cmd_export_label_review(args: argparse.Namespace) -> int:
    with Path(args.queue).open("r", encoding="utf-8") as handle:
        queue = json.load(handle)
    export = build_expert_review_export(
        queue,
        load_labels(Path(args.labels)),
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote expert review export to "
        f"{args.out} ({export['metadata']['exported_count']} items)"
    )
    return 0


def cmd_build_expert_label_decision_review_export(args: argparse.Namespace) -> int:
    with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
        queue = json.load(handle)
    review_debt = None
    if args.review_debt:
        with Path(args.review_debt).open("r", encoding="utf-8") as handle:
            review_debt = json.load(handle)
    mismatch_export = None
    if args.reaction_substrate_mismatch_review_export:
        with Path(args.reaction_substrate_mismatch_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            mismatch_export = json.load(handle)
    export = build_expert_label_decision_review_export(
        active_learning_queue=queue,
        labels=load_labels(Path(args.labels)),
        review_debt=review_debt,
        reaction_substrate_mismatch_review_export=mismatch_export,
    )
    write_json(Path(args.out), export)
    print(
        "Wrote expert-label decision review export to "
        f"{args.out} ({export['metadata']['exported_count']} items)"
    )
    return 0


def cmd_summarize_expert_label_decision_repair_candidates(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_review_export).open(
        "r", encoding="utf-8"
    ) as handle:
        export = json.load(handle)
    remediation = None
    if args.review_debt_remediation:
        with Path(args.review_debt_remediation).open("r", encoding="utf-8") as handle:
            remediation = json.load(handle)
    structure_mapping = None
    if args.structure_mapping:
        with Path(args.structure_mapping).open("r", encoding="utf-8") as handle:
            structure_mapping = json.load(handle)
    alternate_scan = None
    if args.alternate_structure_scan:
        with Path(args.alternate_structure_scan).open("r", encoding="utf-8") as handle:
            alternate_scan = json.load(handle)
    summary = summarize_expert_label_decision_repair_candidates(
        export,
        review_debt_remediation=remediation,
        structure_mapping=structure_mapping,
        alternate_structure_scan=alternate_scan,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), summary)
    print(
        "Wrote expert-label decision repair candidates to "
        f"{args.out} ({summary['metadata']['emitted_row_count']} rows)"
    )
    return 0


def cmd_audit_expert_label_decision_repair_guardrails(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_repair_candidates).open(
        "r", encoding="utf-8"
    ) as handle:
        repair_candidates = json.load(handle)
    remap_local_lead_audit = None
    if args.remap_local_lead_audit:
        with Path(args.remap_local_lead_audit).open("r", encoding="utf-8") as handle:
            remap_local_lead_audit = json.load(handle)
    audit = audit_expert_label_decision_repair_guardrails(
        repair_candidates,
        remap_local_lead_audit=remap_local_lead_audit,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote expert-label decision repair guardrail audit to "
        f"{args.out} ({audit['metadata']['priority_repair_row_count']} rows)"
    )
    return 0


def cmd_audit_expert_label_decision_local_evidence_gaps(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_repair_guardrail_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        repair_guardrail_audit = json.load(handle)
    repair_candidates = None
    if args.expert_label_decision_repair_candidates:
        with Path(args.expert_label_decision_repair_candidates).open(
            "r", encoding="utf-8"
        ) as handle:
            repair_candidates = json.load(handle)
    audit = audit_expert_label_decision_local_evidence_gaps(
        repair_guardrail_audit,
        expert_label_decision_repair_candidates=repair_candidates,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote expert-label decision local-evidence gap audit to "
        f"{args.out} ({audit['metadata']['audited_entry_count']} rows)"
    )
    return 0


def cmd_build_expert_label_decision_local_evidence_review_export(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_local_evidence_gap_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        local_gap_audit = json.load(handle)
    export = build_expert_label_decision_local_evidence_review_export(
        local_gap_audit,
        load_labels(Path(args.labels)),
    )
    write_json(Path(args.out), export)
    print(
        "Wrote expert-label local-evidence review export to "
        f"{args.out} ({export['metadata']['exported_count']} items)"
    )
    return 0


def cmd_summarize_expert_label_decision_local_evidence_repair_plan(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_local_evidence_gap_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        local_gap_audit = json.load(handle)
    review_export = None
    if args.expert_label_decision_local_evidence_review_export:
        with Path(args.expert_label_decision_local_evidence_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            review_export = json.load(handle)
    plan = summarize_expert_label_decision_local_evidence_repair_plan(
        local_gap_audit,
        local_evidence_review_export=review_export,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote expert-label local-evidence repair plan to "
        f"{args.out} ({plan['metadata']['planned_entry_count']} rows)"
    )
    return 0


def cmd_resolve_expert_label_decision_local_evidence_repair_lanes(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_local_evidence_repair_plan).open(
        "r", encoding="utf-8"
    ) as handle:
        repair_plan = json.load(handle)
    local_gap_audit = None
    if args.expert_label_decision_local_evidence_gap_audit:
        with Path(args.expert_label_decision_local_evidence_gap_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            local_gap_audit = json.load(handle)
    local_review_export = None
    if args.expert_label_decision_local_evidence_review_export:
        with Path(args.expert_label_decision_local_evidence_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            local_review_export = json.load(handle)
    mismatch_export = None
    if args.reaction_substrate_mismatch_review_export:
        with Path(args.reaction_substrate_mismatch_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            mismatch_export = json.load(handle)
    mismatch_decision_batch = None
    if args.reaction_substrate_mismatch_decision_batch:
        with Path(args.reaction_substrate_mismatch_decision_batch).open(
            "r", encoding="utf-8"
        ) as handle:
            mismatch_decision_batch = json.load(handle)
    entry_ids = (
        [part.strip() for part in args.entry_ids.split(",") if part.strip()]
        if args.entry_ids
        else None
    )
    resolution = resolve_expert_label_decision_local_evidence_repair_lanes(
        repair_plan,
        local_evidence_gap_audit=local_gap_audit,
        local_evidence_review_export=local_review_export,
        reaction_substrate_mismatch_review_export=mismatch_export,
        reaction_substrate_mismatch_decision_batch=mismatch_decision_batch,
        entry_ids=entry_ids,
    )
    write_json(Path(args.out), resolution)
    print(
        "Wrote expert-label local-evidence repair-lane resolution to "
        f"{args.out} ({resolution['metadata']['resolved_entry_count']} resolved)"
    )
    return 0


def cmd_build_explicit_alternate_residue_position_requests(
    args: argparse.Namespace,
) -> int:
    with Path(args.expert_label_decision_local_evidence_repair_plan).open(
        "r", encoding="utf-8"
    ) as handle:
        repair_plan = json.load(handle)
    remediation = None
    if args.review_debt_remediation:
        with Path(args.review_debt_remediation).open("r", encoding="utf-8") as handle:
            remediation = json.load(handle)
    graph = None
    if args.graph:
        with Path(args.graph).open("r", encoding="utf-8") as handle:
            graph = json.load(handle)
    requests = build_explicit_alternate_residue_position_requests(
        repair_plan,
        review_debt_remediation=remediation,
        graph=graph,
    )
    write_json(Path(args.out), requests)
    print(
        "Wrote alternate residue-position sourcing requests to "
        f"{args.out} ({requests['metadata']['request_count']} requests)"
    )
    return 0


def cmd_audit_accepted_review_debt_deferrals(args: argparse.Namespace) -> int:
    with Path(args.review_debt).open("r", encoding="utf-8") as handle:
        review_debt = json.load(handle)
    with Path(args.acceptance).open("r", encoding="utf-8") as handle:
        acceptance = json.load(handle)
    scaling_quality = None
    if args.scaling_quality_audit:
        with Path(args.scaling_quality_audit).open("r", encoding="utf-8") as handle:
            scaling_quality = json.load(handle)
    local_gap = None
    if args.expert_label_decision_local_evidence_gap_audit:
        with Path(args.expert_label_decision_local_evidence_gap_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            local_gap = json.load(handle)
    local_export = None
    if args.expert_label_decision_local_evidence_review_export:
        with Path(args.expert_label_decision_local_evidence_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            local_export = json.load(handle)
    repair_plan = None
    if args.expert_label_decision_local_evidence_repair_plan:
        with Path(args.expert_label_decision_local_evidence_repair_plan).open(
            "r", encoding="utf-8"
        ) as handle:
            repair_plan = json.load(handle)
    repair_resolution = None
    if args.expert_label_decision_local_evidence_repair_resolution:
        with Path(args.expert_label_decision_local_evidence_repair_resolution).open(
            "r", encoding="utf-8"
        ) as handle:
            repair_resolution = json.load(handle)
    alternate_requests = None
    if args.explicit_alternate_residue_position_requests:
        with Path(args.explicit_alternate_residue_position_requests).open(
            "r", encoding="utf-8"
        ) as handle:
            alternate_requests = json.load(handle)
    remap_local_audit = None
    if args.remap_local_lead_audit:
        with Path(args.remap_local_lead_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            remap_local_audit = json.load(handle)
    import_safety = None
    if args.review_only_import_safety_audit:
        with Path(args.review_only_import_safety_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            import_safety = json.load(handle)
    audit = audit_accepted_review_debt_deferrals(
        review_debt,
        acceptance,
        scaling_quality_audit=scaling_quality,
        local_evidence_gap_audit=local_gap,
        local_evidence_review_export=local_export,
        local_evidence_repair_plan=repair_plan,
        local_evidence_repair_resolution=repair_resolution,
        explicit_alternate_residue_position_requests=alternate_requests,
        remap_local_lead_audit=remap_local_audit,
        review_only_import_safety_audit=import_safety,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote accepted review-debt deferral audit to "
        f"{args.out} ({audit['metadata']['deferred_entry_count']} deferred)"
    )
    return 0


def cmd_audit_mechanism_ontology_gaps(args: argparse.Namespace) -> int:
    with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
        queue = json.load(handle)
    repair_candidates = None
    if args.expert_label_decision_repair_candidates:
        with Path(args.expert_label_decision_repair_candidates).open(
            "r", encoding="utf-8"
        ) as handle:
            repair_candidates = json.load(handle)
    family_guardrails = None
    if args.family_propagation_guardrails:
        with Path(args.family_propagation_guardrails).open(
            "r", encoding="utf-8"
        ) as handle:
            family_guardrails = json.load(handle)
    local_gap_audit = None
    if args.expert_label_decision_local_evidence_gap_audit:
        with Path(args.expert_label_decision_local_evidence_gap_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            local_gap_audit = json.load(handle)
    audit = audit_mechanism_ontology_gaps(
        queue,
        expert_label_decision_repair_candidates=repair_candidates,
        family_propagation_guardrails=family_guardrails,
        expert_label_decision_local_evidence_gap_audit=local_gap_audit,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote mechanism ontology gap audit to "
        f"{args.out} ({audit['metadata']['candidate_scope_signal_count']} rows)"
    )
    return 0


def cmd_build_atp_phosphoryl_transfer_family_expansion(args: argparse.Namespace) -> int:
    with Path(args.reaction_substrate_mismatch_decision_batch).open(
        "r", encoding="utf-8"
    ) as handle:
        decision_batch = json.load(handle)
    mismatch_export = None
    if args.reaction_substrate_mismatch_review_export:
        with Path(args.reaction_substrate_mismatch_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            mismatch_export = json.load(handle)
    family_guardrails = None
    if args.family_propagation_guardrails:
        with Path(args.family_propagation_guardrails).open(
            "r", encoding="utf-8"
        ) as handle:
            family_guardrails = json.load(handle)
    active_queue = None
    if args.active_learning_queue:
        with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
            active_queue = json.load(handle)
    adversarial_negatives = None
    if args.adversarial_negatives:
        with Path(args.adversarial_negatives).open("r", encoding="utf-8") as handle:
            adversarial_negatives = json.load(handle)
    expansion = build_atp_phosphoryl_transfer_family_expansion(
        reaction_substrate_mismatch_decision_batch=decision_batch,
        reaction_substrate_mismatch_review_export=mismatch_export,
        family_propagation_guardrails=family_guardrails,
        active_learning_queue=active_queue,
        adversarial_negatives=adversarial_negatives,
    )
    write_json(Path(args.out), expansion)
    print(
        "Wrote ATP/phosphoryl-transfer family expansion to "
        f"{args.out} (ready={expansion['metadata']['boundary_guardrail_ready']})"
    )
    return 0


def cmd_build_learned_retrieval_manifest(args: argparse.Namespace) -> int:
    with Path(args.geometry).open("r", encoding="utf-8") as handle:
        geometry = json.load(handle)
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    ontology_gap_audit = None
    if args.ontology_gap_audit:
        with Path(args.ontology_gap_audit).open("r", encoding="utf-8") as handle:
            ontology_gap_audit = json.load(handle)
    manifest = build_learned_retrieval_manifest(
        geometry,
        retrieval,
        load_labels(Path(args.labels)),
        ontology_gap_audit=ontology_gap_audit,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), manifest)
    print(
        "Wrote learned retrieval manifest to "
        f"{args.out} ({manifest['metadata']['eligible_entry_count']} eligible entries)"
    )
    return 0


def cmd_audit_sequence_similarity_failure_sets(args: argparse.Namespace) -> int:
    with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
        sequence_clusters = json.load(handle)
    active_queue = None
    if args.active_learning_queue:
        with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
            active_queue = json.load(handle)
    audit = audit_sequence_similarity_failure_sets(
        sequence_clusters,
        load_labels(Path(args.labels)),
        active_learning_queue=active_queue,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote sequence similarity failure set audit to "
        f"{args.out} ({audit['metadata']['duplicate_cluster_count']} clusters)"
    )
    return 0


def cmd_import_label_review(args: argparse.Namespace) -> int:
    with Path(args.review).open("r", encoding="utf-8") as handle:
        review = json.load(handle)
    imported = import_expert_review_decisions(load_labels(Path(args.labels)), review)
    write_label_registry(Path(args.out), [label.to_dict() for label in imported])
    print(f"Wrote imported label registry to {args.out} ({len(imported)} labels)")
    return 0


def cmd_import_countable_label_review(args: argparse.Namespace) -> int:
    with Path(args.review).open("r", encoding="utf-8") as handle:
        review = json.load(handle)
    imported = import_countable_review_decisions(load_labels(Path(args.labels)), review)
    write_label_registry(Path(args.out), [label.to_dict() for label in imported])
    print(f"Wrote countable imported label registry to {args.out} ({len(imported)} labels)")
    return 0


def cmd_audit_review_only_import_safety(args: argparse.Namespace) -> int:
    audit = audit_review_only_import_safety(
        load_labels(Path(args.labels)),
        _load_named_json_artifacts(args.review),
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote review-only import safety audit to "
        f"{args.out} (safe={audit['metadata']['countable_import_safe']})"
    )
    return 0


def cmd_build_review_decision_batch(args: argparse.Namespace) -> int:
    with Path(args.review).open("r", encoding="utf-8") as handle:
        review = json.load(handle)
    batch = build_provisional_review_decision_batch(
        review,
        batch_id=args.batch_id,
        reviewer=args.reviewer,
        max_boundary_controls=args.max_boundary_controls,
        entry_ids=set(args.entry_id or []),
    )
    write_json(Path(args.out), batch)
    print(
        "Wrote provisional review decision batch to "
        f"{args.out} ({batch['metadata']['decision_counts']})"
    )
    return 0


def cmd_check_label_review_resolution(args: argparse.Namespace) -> int:
    with Path(args.review).open("r", encoding="utf-8") as handle:
        review = json.load(handle)
    with Path(args.label_expansion_candidates).open("r", encoding="utf-8") as handle:
        candidates = json.load(handle)
    with Path(args.label_factory_gate).open("r", encoding="utf-8") as handle:
        label_factory_gate = json.load(handle)
    check = check_label_review_resolution(
        baseline_labels=load_labels(Path(args.baseline_labels)),
        review_state_labels=load_labels(Path(args.review_state_labels)),
        countable_labels=load_labels(Path(args.countable_labels)),
        review_artifact=review,
        label_expansion_candidates=candidates,
        label_factory_gate=label_factory_gate,
        baseline_label_count=args.baseline_label_count,
    )
    write_json(Path(args.out), check)
    print(
        "Wrote label review resolution check to "
        f"{args.out} (resolved={check['metadata']['resolved_for_scaling']})"
    )
    return 0


def cmd_analyze_review_evidence_gaps(args: argparse.Namespace) -> int:
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    with Path(args.review).open("r", encoding="utf-8") as handle:
        review = json.load(handle)
    analysis = analyze_review_evidence_gaps(retrieval, review)
    write_json(Path(args.out), analysis)
    print(
        "Wrote review evidence gap analysis to "
        f"{args.out} ({analysis['metadata']['gap_count']} gaps)"
    )
    return 0


def cmd_summarize_review_debt(args: argparse.Namespace) -> int:
    with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
        review_gaps = json.load(handle)
    queue = None
    if args.active_learning_queue:
        with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
            queue = json.load(handle)
    baseline_debt = None
    if args.baseline_review_debt:
        with Path(args.baseline_review_debt).open("r", encoding="utf-8") as handle:
            baseline_debt = json.load(handle)
    summary = summarize_review_debt(
        review_gaps,
        active_learning_queue=queue,
        baseline_review_debt=baseline_debt,
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), summary)
    print(
        "Wrote review debt summary to "
        f"{args.out} ({summary['metadata']['review_debt_count']} rows)"
    )
    return 0


def cmd_analyze_review_debt_remediation(args: argparse.Namespace) -> int:
    with Path(args.review_debt).open("r", encoding="utf-8") as handle:
        review_debt = json.load(handle)
    with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
        review_gaps = json.load(handle)
    graph = None
    if args.graph:
        with Path(args.graph).open("r", encoding="utf-8") as handle:
            graph = json.load(handle)
    geometry = None
    if args.geometry:
        with Path(args.geometry).open("r", encoding="utf-8") as handle:
            geometry = json.load(handle)
    max_rows = args.max_rows if args.max_rows > 0 else None
    plan = analyze_review_debt_remediation(
        review_debt,
        review_gaps,
        graph=graph,
        geometry=geometry,
        debt_status=args.debt_status,
        max_rows=max_rows,
    )
    write_json(Path(args.out), plan)
    print(
        "Wrote review debt remediation plan to "
        f"{args.out} ({plan['metadata']['emitted_row_count']} rows)"
    )
    return 0


def cmd_scan_review_debt_alternate_structures(args: argparse.Namespace) -> int:
    with Path(args.remediation).open("r", encoding="utf-8") as handle:
        remediation = json.load(handle)
    scan = scan_review_debt_alternate_structures(
        remediation,
        max_entries=args.max_entries,
        max_structures_per_entry=args.max_structures_per_entry,
    )
    write_json(Path(args.out), scan)
    print(
        "Wrote review debt alternate-structure scan to "
        f"{args.out} ({scan['metadata']['scanned_structure_count']} structures)"
    )
    return 0


def cmd_summarize_review_debt_remap_leads(args: argparse.Namespace) -> int:
    with Path(args.alternate_structure_scan).open("r", encoding="utf-8") as handle:
        scan = json.load(handle)
    remediation = None
    if args.remediation:
        with Path(args.remediation).open("r", encoding="utf-8") as handle:
            remediation = json.load(handle)
    review_gaps = None
    if args.review_evidence_gaps:
        with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
            review_gaps = json.load(handle)
    summary = summarize_review_debt_remap_leads(
        scan,
        remediation_plan=remediation,
        review_evidence_gaps=review_gaps,
    )
    write_json(Path(args.out), summary)
    print(
        "Wrote review debt remap lead summary to "
        f"{args.out} ({summary['metadata']['lead_count']} leads)"
    )
    return 0


def cmd_audit_review_debt_remap_local_leads(args: argparse.Namespace) -> int:
    with Path(args.remap_leads).open("r", encoding="utf-8") as handle:
        remap_leads = json.load(handle)
    remediation = None
    if args.remediation:
        with Path(args.remediation).open("r", encoding="utf-8") as handle:
            remediation = json.load(handle)
    review_gaps = None
    if args.review_evidence_gaps:
        with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
            review_gaps = json.load(handle)
    audit = audit_review_debt_remap_local_leads(
        remap_leads,
        remediation_plan=remediation,
        review_evidence_gaps=review_gaps,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote review debt remap-local lead audit to "
        f"{args.out} ({audit['metadata']['audited_entry_count']} entries)"
    )
    return 0


def cmd_audit_structure_selection_holo_preference(
    args: argparse.Namespace,
) -> int:
    with Path(args.alternate_structure_scan).open("r", encoding="utf-8") as handle:
        scan = json.load(handle)
    audit = audit_structure_selection_holo_preference(
        scan,
        min_usable_residue_positions=args.min_usable_residue_positions,
        prefer_mcsa_explicit_over_remap=args.prefer_mcsa_explicit_over_remap,
    )
    write_json(Path(args.out), audit)
    meta = audit["metadata"]
    print(
        "Wrote structure-selection holo-preference audit to "
        f"{args.out} ({meta['audited_entry_count']} entries; "
        f"{meta['swap_recommended_count']} swap recommendations, "
        f"{meta['already_holo_entry_count']} already holo, "
        f"{meta['no_holo_alternate_entry_count']} no holo alternate)"
    )
    return 0


def cmd_build_selected_pdb_overrides(args: argparse.Namespace) -> int:
    with Path(args.holo_preference_audit).open("r", encoding="utf-8") as handle:
        holo_preference_audit = json.load(handle)
    with Path(args.remediation).open("r", encoding="utf-8") as handle:
        remediation = json.load(handle)
    entry_ids = _split_csv(args.entry_ids)
    skip_entry_ids = _split_csv(args.skip_entry_ids)
    plan = build_selected_pdb_override_plan(
        holo_preference_audit,
        remediation,
        entry_ids=entry_ids,
        skip_entry_ids=skip_entry_ids,
        source_audit=args.holo_preference_audit,
        source_remediation=args.remediation,
    )
    write_json(Path(args.out), plan)
    meta = plan["metadata"]
    print(
        "Wrote selected-PDB override plan to "
        f"{args.out} ({meta['ready_to_apply_count']} ready, "
        f"{meta['skipped_entry_count']} skipped, "
        f"{meta['blocked_entry_count']} blocked)"
    )
    return 0


def cmd_summarize_review_debt_structure_selection_candidates(
    args: argparse.Namespace,
) -> int:
    with Path(args.remap_local_lead_audit).open("r", encoding="utf-8") as handle:
        remap_local_audit = json.load(handle)
    with Path(args.alternate_structure_scan).open("r", encoding="utf-8") as handle:
        alternate_scan = json.load(handle)
    remediation = None
    if args.remediation:
        with Path(args.remediation).open("r", encoding="utf-8") as handle:
            remediation = json.load(handle)
    summary = summarize_review_debt_structure_selection_candidates(
        remap_local_audit,
        alternate_scan,
        remediation_plan=remediation,
    )
    write_json(Path(args.out), summary)
    print(
        "Wrote review debt structure-selection candidates to "
        f"{args.out} ({summary['metadata']['candidate_count']} entries)"
    )
    return 0


def cmd_audit_reaction_substrate_mismatches(args: argparse.Namespace) -> int:
    review_gaps = None
    if args.review_evidence_gaps:
        with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
            review_gaps = json.load(handle)
    queue = None
    if args.active_learning_queue:
        with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
            queue = json.load(handle)
    audit = audit_reaction_substrate_mismatches(
        review_evidence_gaps=review_gaps,
        active_learning_queue=queue,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote reaction/substrate mismatch audit to "
        f"{args.out} ({audit['metadata']['mismatch_count']} rows)"
    )
    return 0


def cmd_build_reaction_substrate_mismatch_review_export(args: argparse.Namespace) -> int:
    with Path(args.reaction_substrate_mismatch_audit).open(
        "r", encoding="utf-8"
    ) as handle:
        reaction_mismatch_audit = json.load(handle)
    with Path(args.family_propagation_guardrails).open("r", encoding="utf-8") as handle:
        family_guardrails = json.load(handle)
    export = build_reaction_substrate_mismatch_review_export(
        reaction_substrate_mismatch_audit=reaction_mismatch_audit,
        family_propagation_guardrails=family_guardrails,
        labels=load_labels(Path(args.labels)),
    )
    write_json(Path(args.out), export)
    print(
        "Wrote reaction/substrate mismatch review export to "
        f"{args.out} ({export['metadata']['exported_count']} items)"
    )
    return 0


def cmd_check_label_preview_promotion(args: argparse.Namespace) -> int:
    with Path(args.preview_acceptance).open("r", encoding="utf-8") as handle:
        acceptance = json.load(handle)
    with Path(args.preview_summary).open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    with Path(args.preview_review_debt).open("r", encoding="utf-8") as handle:
        preview_debt = json.load(handle)
    current_debt = None
    if args.current_review_debt:
        with Path(args.current_review_debt).open("r", encoding="utf-8") as handle:
            current_debt = json.load(handle)
    readiness = check_label_preview_promotion_readiness(
        acceptance,
        summary,
        preview_debt,
        current_review_debt=current_debt,
    )
    write_json(Path(args.out), readiness)
    print(
        "Wrote label preview promotion readiness to "
        f"{args.out} ({readiness['metadata']['promotion_recommendation']})"
    )
    return 0


def cmd_audit_label_scaling_quality(args: argparse.Namespace) -> int:
    required_artifacts = {
        "acceptance": args.acceptance,
        "readiness": args.readiness,
        "review_debt": args.review_debt,
        "review_evidence_gaps": args.review_evidence_gaps,
        "active_learning_queue": args.active_learning_queue,
        "family_propagation_guardrails": args.family_propagation_guardrails,
        "hard_negatives": args.hard_negatives,
    }
    optional_artifacts = {
        "decision_batch": args.decision_batch,
        "structure_mapping": args.structure_mapping,
        "expert_review_export": args.expert_review_export,
        "sequence_clusters": args.sequence_clusters,
        "alternate_structure_scan": args.alternate_structure_scan,
        "remap_local_lead_audit": args.remap_local_lead_audit,
        "reaction_substrate_mismatch_audit": args.reaction_substrate_mismatch_audit,
        "reaction_substrate_mismatch_review_export": (
            args.reaction_substrate_mismatch_review_export
        ),
        "expert_label_decision_review_export": (
            args.expert_label_decision_review_export
        ),
        "expert_label_decision_repair_candidates": (
            args.expert_label_decision_repair_candidates
        ),
        "expert_label_decision_repair_guardrail_audit": (
            args.expert_label_decision_repair_guardrail_audit
        ),
        "expert_label_decision_local_evidence_gap_audit": (
            args.expert_label_decision_local_evidence_gap_audit
        ),
        "expert_label_decision_local_evidence_review_export": (
            args.expert_label_decision_local_evidence_review_export
        ),
        "expert_label_decision_local_evidence_repair_resolution": (
            args.expert_label_decision_local_evidence_repair_resolution
        ),
        "explicit_alternate_residue_position_requests": (
            args.explicit_alternate_residue_position_requests
        ),
        "review_only_import_safety_audit": args.review_only_import_safety_audit,
        "atp_phosphoryl_transfer_family_expansion": (
            args.atp_phosphoryl_transfer_family_expansion
        ),
    }
    with Path(args.acceptance).open("r", encoding="utf-8") as handle:
        acceptance = json.load(handle)
    with Path(args.readiness).open("r", encoding="utf-8") as handle:
        readiness = json.load(handle)
    with Path(args.review_debt).open("r", encoding="utf-8") as handle:
        review_debt = json.load(handle)
    with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
        review_gaps = json.load(handle)
    with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
        queue = json.load(handle)
    with Path(args.family_propagation_guardrails).open("r", encoding="utf-8") as handle:
        guardrails = json.load(handle)
    with Path(args.hard_negatives).open("r", encoding="utf-8") as handle:
        hard_negatives = json.load(handle)
    decision_batch = None
    if args.decision_batch:
        with Path(args.decision_batch).open("r", encoding="utf-8") as handle:
            decision_batch = json.load(handle)
    structure_mapping = None
    if args.structure_mapping:
        with Path(args.structure_mapping).open("r", encoding="utf-8") as handle:
            structure_mapping = json.load(handle)
    expert_review_export = None
    if args.expert_review_export:
        with Path(args.expert_review_export).open("r", encoding="utf-8") as handle:
            expert_review_export = json.load(handle)
    sequence_clusters = None
    if args.sequence_clusters:
        with Path(args.sequence_clusters).open("r", encoding="utf-8") as handle:
            sequence_clusters = json.load(handle)
    alternate_structure_scan = None
    if args.alternate_structure_scan:
        with Path(args.alternate_structure_scan).open("r", encoding="utf-8") as handle:
            alternate_structure_scan = json.load(handle)
    remap_local_lead_audit = None
    if args.remap_local_lead_audit:
        with Path(args.remap_local_lead_audit).open("r", encoding="utf-8") as handle:
            remap_local_lead_audit = json.load(handle)
    reaction_mismatch_audit = None
    if args.reaction_substrate_mismatch_audit:
        with Path(args.reaction_substrate_mismatch_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            reaction_mismatch_audit = json.load(handle)
    reaction_mismatch_review_export = None
    if args.reaction_substrate_mismatch_review_export:
        with Path(args.reaction_substrate_mismatch_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            reaction_mismatch_review_export = json.load(handle)
    expert_label_decision_review_export = None
    if args.expert_label_decision_review_export:
        with Path(args.expert_label_decision_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_review_export = json.load(handle)
    expert_label_decision_repair_candidates = None
    if args.expert_label_decision_repair_candidates:
        with Path(args.expert_label_decision_repair_candidates).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_repair_candidates = json.load(handle)
    expert_label_decision_repair_guardrail_audit = None
    if args.expert_label_decision_repair_guardrail_audit:
        with Path(args.expert_label_decision_repair_guardrail_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_repair_guardrail_audit = json.load(handle)
    expert_label_decision_local_evidence_gap_audit = None
    if args.expert_label_decision_local_evidence_gap_audit:
        with Path(args.expert_label_decision_local_evidence_gap_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_local_evidence_gap_audit = json.load(handle)
    expert_label_decision_local_evidence_review_export = None
    if args.expert_label_decision_local_evidence_review_export:
        with Path(args.expert_label_decision_local_evidence_review_export).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_local_evidence_review_export = json.load(handle)
    expert_label_decision_local_evidence_repair_resolution = None
    if args.expert_label_decision_local_evidence_repair_resolution:
        with Path(args.expert_label_decision_local_evidence_repair_resolution).open(
            "r", encoding="utf-8"
        ) as handle:
            expert_label_decision_local_evidence_repair_resolution = json.load(handle)
    alternate_residue_requests = None
    if args.explicit_alternate_residue_position_requests:
        with Path(args.explicit_alternate_residue_position_requests).open(
            "r", encoding="utf-8"
        ) as handle:
            alternate_residue_requests = json.load(handle)
    review_only_import_safety = None
    if args.review_only_import_safety_audit:
        with Path(args.review_only_import_safety_audit).open(
            "r", encoding="utf-8"
        ) as handle:
            review_only_import_safety = json.load(handle)
    atp_family_expansion = None
    if args.atp_phosphoryl_transfer_family_expansion:
        with Path(args.atp_phosphoryl_transfer_family_expansion).open(
            "r", encoding="utf-8"
        ) as handle:
            atp_family_expansion = json.load(handle)
    loaded_artifacts = {
        "acceptance": acceptance,
        "readiness": readiness,
        "review_debt": review_debt,
        "review_evidence_gaps": review_gaps,
        "active_learning_queue": queue,
        "family_propagation_guardrails": guardrails,
        "hard_negatives": hard_negatives,
    }
    loaded_artifacts.update(
        {
            name: artifact
            for name, artifact in {
                "decision_batch": decision_batch,
                "structure_mapping": structure_mapping,
                "expert_review_export": expert_review_export,
                "sequence_clusters": sequence_clusters,
                "alternate_structure_scan": alternate_structure_scan,
                "remap_local_lead_audit": remap_local_lead_audit,
                "reaction_substrate_mismatch_audit": reaction_mismatch_audit,
                "reaction_substrate_mismatch_review_export": (
                    reaction_mismatch_review_export
                ),
                "expert_label_decision_review_export": (
                    expert_label_decision_review_export
                ),
                "expert_label_decision_repair_candidates": (
                    expert_label_decision_repair_candidates
                ),
                "expert_label_decision_repair_guardrail_audit": (
                    expert_label_decision_repair_guardrail_audit
                ),
                "expert_label_decision_local_evidence_gap_audit": (
                    expert_label_decision_local_evidence_gap_audit
                ),
                "expert_label_decision_local_evidence_review_export": (
                    expert_label_decision_local_evidence_review_export
                ),
                "expert_label_decision_local_evidence_repair_resolution": (
                    expert_label_decision_local_evidence_repair_resolution
                ),
                "explicit_alternate_residue_position_requests": (
                    alternate_residue_requests
                ),
                "review_only_import_safety_audit": review_only_import_safety,
                "atp_phosphoryl_transfer_family_expansion": atp_family_expansion,
            }.items()
            if artifact is not None
        }
    )
    artifact_lineage = _validate_label_scaling_quality_cli_lineage(
        required_artifacts=required_artifacts,
        optional_artifacts=optional_artifacts,
        loaded_artifacts=loaded_artifacts,
    )
    audit = audit_label_scaling_quality(
        acceptance,
        readiness,
        review_debt,
        review_gaps,
        queue,
        guardrails,
        hard_negatives,
        decision_batch=decision_batch,
        structure_mapping=structure_mapping,
        expert_review_export=expert_review_export,
        sequence_clusters=sequence_clusters,
        alternate_structure_scan=alternate_structure_scan,
        remap_local_lead_audit=remap_local_lead_audit,
        reaction_substrate_mismatch_audit=reaction_mismatch_audit,
        reaction_substrate_mismatch_review_export=reaction_mismatch_review_export,
        expert_label_decision_review_export=expert_label_decision_review_export,
        expert_label_decision_repair_candidates=(
            expert_label_decision_repair_candidates
        ),
        expert_label_decision_repair_guardrail_audit=(
            expert_label_decision_repair_guardrail_audit
        ),
        expert_label_decision_local_evidence_gap_audit=(
            expert_label_decision_local_evidence_gap_audit
        ),
        expert_label_decision_local_evidence_review_export=(
            expert_label_decision_local_evidence_review_export
        ),
        expert_label_decision_local_evidence_repair_resolution=(
            expert_label_decision_local_evidence_repair_resolution
        ),
        explicit_alternate_residue_position_requests=alternate_residue_requests,
        review_only_import_safety_audit=review_only_import_safety,
        atp_phosphoryl_transfer_family_expansion=atp_family_expansion,
        batch_id=args.batch_id,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), audit)
    print(
        "Wrote label scaling quality audit to "
        f"{args.out} ({audit['metadata']['audit_recommendation']})"
    )
    return 0


def cmd_check_label_factory_gates(args: argparse.Namespace) -> int:
    required_artifacts = {
        "label_factory_audit": args.label_factory_audit,
        "applied_label_factory": args.applied_label_factory,
        "active_learning_queue": args.active_learning_queue,
        "adversarial_negatives": args.adversarial_negatives,
        "expert_review_export": args.expert_review_export,
        "family_propagation_guardrails": args.family_propagation_guardrails,
    }
    optional_artifacts = {
        "reaction_substrate_mismatch_review_export": (
            args.reaction_substrate_mismatch_review_export
        ),
        "expert_label_decision_review_export": (
            args.expert_label_decision_review_export
        ),
        "expert_label_decision_repair_candidates": (
            args.expert_label_decision_repair_candidates
        ),
        "expert_label_decision_repair_guardrail_audit": (
            args.expert_label_decision_repair_guardrail_audit
        ),
        "expert_label_decision_local_evidence_gap_audit": (
            args.expert_label_decision_local_evidence_gap_audit
        ),
        "expert_label_decision_local_evidence_review_export": (
            args.expert_label_decision_local_evidence_review_export
        ),
        "expert_label_decision_local_evidence_repair_resolution": (
            args.expert_label_decision_local_evidence_repair_resolution
        ),
        "explicit_alternate_residue_position_requests": (
            args.explicit_alternate_residue_position_requests
        ),
        "review_only_import_safety_audit": args.review_only_import_safety_audit,
        "atp_phosphoryl_transfer_family_expansion": (
            args.atp_phosphoryl_transfer_family_expansion
        ),
        "accepted_review_debt_deferral_audit": (
            args.accepted_review_debt_deferral_audit
        ),
    }
    gate_artifacts = {
        field_name: read_json_object(Path(path))
        for field_name, path in required_artifacts.items()
    }
    gate_artifacts.update(
        {
            field_name: read_json_object(Path(path))
            for field_name, path in optional_artifacts.items()
            if path
        }
    )
    artifact_lineage = _validate_label_factory_gate_cli_lineage(
        labels_path=args.labels,
        required_artifacts=required_artifacts,
        optional_artifacts=optional_artifacts,
        loaded_artifacts=gate_artifacts,
    )
    gates = check_label_factory_gates(
        LabelFactoryGateInputs(
            labels=load_labels(Path(args.labels)),
            artifact_lineage=artifact_lineage,
            **gate_artifacts,
        )
    )
    write_json(Path(args.out), gates)
    print(
        "Wrote label factory gate check to "
        f"{args.out} (ready={gates['metadata']['automation_ready_for_next_label_batch']})"
    )
    return 0


def cmd_check_label_batch_acceptance(args: argparse.Namespace) -> int:
    required_artifacts = {
        "evaluation": args.evaluation,
        "hard_negatives": args.hard_negatives,
        "in_scope_failures": args.in_scope_failures,
        "label_factory_gate": args.label_factory_gate,
    }
    optional_artifacts = {
        "review_evidence_gaps": args.review_evidence_gaps,
    }
    with Path(args.evaluation).open("r", encoding="utf-8") as handle:
        evaluation = json.load(handle)
    with Path(args.hard_negatives).open("r", encoding="utf-8") as handle:
        hard_negatives = json.load(handle)
    with Path(args.in_scope_failures).open("r", encoding="utf-8") as handle:
        in_scope_failures = json.load(handle)
    with Path(args.label_factory_gate).open("r", encoding="utf-8") as handle:
        label_factory_gate = json.load(handle)
    review_gaps = None
    if args.review_evidence_gaps:
        with Path(args.review_evidence_gaps).open("r", encoding="utf-8") as handle:
            review_gaps = json.load(handle)
    loaded_artifacts = {
        "evaluation": evaluation,
        "hard_negatives": hard_negatives,
        "in_scope_failures": in_scope_failures,
        "label_factory_gate": label_factory_gate,
    }
    if review_gaps is not None:
        loaded_artifacts["review_evidence_gaps"] = review_gaps
    artifact_lineage = _validate_label_batch_acceptance_cli_lineage(
        countable_labels_path=args.countable_labels,
        review_state_labels_path=args.review_state_labels,
        required_artifacts=required_artifacts,
        optional_artifacts=optional_artifacts,
        loaded_artifacts=loaded_artifacts,
    )
    check = check_label_batch_acceptance(
        baseline_labels=load_labels(Path(args.baseline_labels)),
        review_state_labels=load_labels(Path(args.review_state_labels)),
        countable_labels=load_labels(Path(args.countable_labels)),
        evaluation=evaluation,
        hard_negatives=hard_negatives,
        in_scope_failures=in_scope_failures,
        label_factory_gate=label_factory_gate,
        review_evidence_gaps=review_gaps,
        baseline_label_count=args.baseline_label_count,
        artifact_lineage=artifact_lineage,
    )
    write_json(Path(args.out), check)
    print(
        "Wrote label batch acceptance check to "
        f"{args.out} (accepted={check['metadata']['accepted_for_counting']})"
    )
    return 0


def _load_named_json_artifacts(paths: list[str]) -> list[tuple[str, dict[str, object]]]:
    artifacts: list[tuple[str, dict[str, object]]] = []
    for raw_path in paths:
        path = Path(raw_path)
        with path.open("r", encoding="utf-8") as handle:
            artifacts.append((path.name, json.load(handle)))
    return artifacts


def _load_external_lineaged_artifacts(
    args: argparse.Namespace,
    artifact_names: tuple[str, ...],
    *,
    blocker_removed: str,
) -> tuple[dict[str, dict[str, Any] | None], dict[str, Any]]:
    artifact_paths = {name: getattr(args, name, None) for name in artifact_names}
    artifact_payloads = {
        name: read_json_object(Path(path)) if path else None
        for name, path in artifact_paths.items()
    }
    artifact_lineage = {
        **validate_external_transfer_artifact_path_lineage(
            artifact_paths,
            artifact_payloads,
            fail_fast=True,
        ),
        "blocker_removed": blocker_removed,
    }
    return artifact_payloads, artifact_lineage


def cmd_summarize_label_factory_batches(args: argparse.Namespace) -> int:
    summary = summarize_label_factory_batches(
        _load_named_json_artifacts(args.acceptance),
        gate_checks=_load_named_json_artifacts(args.gate),
        active_learning_queues=_load_named_json_artifacts(args.active_learning_queue),
        scaling_quality_audits=_load_named_json_artifacts(args.scaling_quality_audit),
    )
    write_json(Path(args.out), summary)
    print(
        "Wrote label factory batch summary to "
        f"{args.out} ({summary['metadata']['batch_count']} batches)"
    )
    return 0


def cmd_build_family_propagation_guardrails(args: argparse.Namespace) -> int:
    with Path(args.geometry).open("r", encoding="utf-8") as handle:
        geometry = json.load(handle)
    with Path(args.retrieval).open("r", encoding="utf-8") as handle:
        retrieval = json.load(handle)
    guardrails = build_family_propagation_guardrails(
        geometry,
        retrieval,
        load_labels(Path(args.labels)),
        max_rows=args.max_rows,
    )
    write_json(Path(args.out), guardrails)
    print(
        "Wrote family propagation guardrails to "
        f"{args.out} ({guardrails['metadata']['reported_count']} rows)"
    )
    return 0


def cmd_analyze_structure_mapping_issues(args: argparse.Namespace) -> int:
    with Path(args.geometry).open("r", encoding="utf-8") as handle:
        geometry = json.load(handle)
    analysis = analyze_structure_mapping_issues(
        geometry,
        load_labels(Path(args.labels)),
    )
    write_json(Path(args.out), analysis)
    print(
        "Wrote structure mapping issues to "
        f"{args.out} ({analysis['metadata']['issue_count']} issues)"
    )
    return 0


def cmd_perf_suite(args: argparse.Namespace) -> int:
    report = write_local_performance_suite(
        graph_path=Path(args.graph),
        geometry_path=Path(args.geometry),
        retrieval_path=Path(args.retrieval),
        out_path=Path(args.out),
        iterations=args.iterations,
    )
    print(
        "Wrote performance report to "
        f"{args.out} ({len(report['benchmarks'])} benchmarks, {args.iterations} iterations)"
    )
    return 0


def cmd_summarize_geometry_slices(args: argparse.Namespace) -> int:
    summary = write_geometry_slice_summary(
        artifact_dir=Path(args.artifact_dir),
        out_path=Path(args.out),
    )
    print(
        "Wrote geometry slice summary to "
        f"{args.out} ({summary['metadata']['slice_count']} slices)"
    )
    return 0


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_float_list(value: str) -> list[float] | None:
    if value == "default":
        return None
    return [float(item) for item in value.split(",") if item.strip()]


def cmd_log_work(args: argparse.Namespace) -> int:
    entry = WorkEntry.create(
        stage=args.stage,
        task=args.task,
        minutes=args.minutes,
        artifacts=_split_csv(args.artifacts),
        evidence=_split_csv(args.evidence),
        time_mode=args.time_mode,
        started_at=args.started_at,
        ended_at=args.ended_at,
        measured_minutes=args.measured_minutes,
        scope_adjustment=args.scope_adjustment,
        expectation_update=args.expectation_update,
        commit=args.commit,
        notes=args.notes,
    )
    append_work_entry(entry, Path(args.log))
    print(f"Logged {entry.minutes} minutes for {entry.stage}: {entry.task}")
    return 0


def cmd_progress_report(args: argparse.Namespace) -> int:
    write_progress_report(Path(args.log), Path(args.out))
    print(f"Wrote progress report to {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalytic-earth",
        description="Mechanism-first enzyme atlas scaffold",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate seed registries")
    validate.set_defaults(func=cmd_validate)

    automation_lock = subparsers.add_parser(
        "automation-lock",
        help="acquire, inspect, or release the local automation run lock",
    )
    automation_lock.add_argument(
        "--lock-dir",
        default=".git/catalytic-earth-automation.lock",
        help="atomic lock directory path",
    )
    automation_lock.add_argument("--repo-root", default=".", help="repository root for git checks")
    automation_lock.add_argument("--stale-after-minutes", type=float, default=90.0)
    lock_actions = automation_lock.add_subparsers(dest="lock_action", required=True)
    lock_acquire = lock_actions.add_parser("acquire", help="create the lock atomically")
    lock_acquire.add_argument("--started-at", default=None)
    lock_acquire.add_argument(
        "--worktree-dirty",
        action="store_true",
        help="force dirty-worktree handling for stale lock recovery",
    )
    lock_acquire.add_argument(
        "--skip-worktree-check",
        action="store_true",
        help="do not call git status before stale-lock handling",
    )
    lock_acquire.set_defaults(func=cmd_automation_lock)
    lock_status = lock_actions.add_parser("status", help="report current lock state")
    lock_status.set_defaults(func=cmd_automation_lock)
    lock_release = lock_actions.add_parser("release", help="remove the lock after safety checks")
    lock_release.add_argument("--require-clean", action="store_true")
    lock_release.add_argument("--require-no-merge", action="store_true")
    lock_release.add_argument("--require-synced", action="store_true")
    lock_release.set_defaults(func=cmd_automation_lock)

    ledger = subparsers.add_parser("build-ledger", help="build source ledger artifact")
    ledger.add_argument("--out", default="artifacts/source_ledger.json")
    ledger.set_defaults(func=cmd_build_ledger)

    demo = subparsers.add_parser("fingerprint-demo", help="build mechanism demo artifact")
    demo.add_argument("--out", default="artifacts/mechanism_demo.json")
    demo.set_defaults(func=cmd_fingerprint_demo)

    rhea = subparsers.add_parser("fetch-rhea-sample", help="fetch a small Rhea sample")
    rhea.add_argument("--limit", type=int, default=25)
    rhea.add_argument("--out", default="artifacts/rhea_sample.json")
    rhea.set_defaults(func=cmd_fetch_rhea_sample)

    mcsa = subparsers.add_parser("fetch-mcsa-sample", help="fetch a small M-CSA entry sample")
    mcsa.add_argument("--ids", default="1,2,3")
    mcsa.add_argument("--out", default="artifacts/mcsa_sample.json")
    mcsa.set_defaults(func=cmd_fetch_mcsa_sample)

    graph = subparsers.add_parser(
        "build-seed-graph",
        help="build a small catalytic graph from M-CSA entries and Rhea reactions",
    )
    graph.add_argument("--mcsa-ids", default="1,2,3")
    graph.add_argument("--out", default="artifacts/seed_graph.json")
    graph.set_defaults(func=cmd_build_seed_graph)

    v1_graph = subparsers.add_parser(
        "build-v1-graph",
        help="build a mechanism-centered graph from M-CSA, Rhea, and UniProt",
    )
    v1_graph.add_argument("--max-mcsa", type=int, default=50)
    v1_graph.add_argument("--page-size", type=int, default=50)
    v1_graph.add_argument("--out", default="artifacts/v1_graph.json")
    v1_graph.set_defaults(func=cmd_build_v1_graph)

    summary = subparsers.add_parser("graph-summary", help="summarize a graph artifact")
    summary.add_argument("--graph", default="artifacts/v1_graph.json")
    summary.add_argument("--out", default="artifacts/v1_graph_summary.json")
    summary.set_defaults(func=cmd_graph_summary)

    sequence_clusters = subparsers.add_parser(
        "build-sequence-cluster-proxy",
        help="build a local exact-UniProt sequence-cluster proxy from a graph artifact",
    )
    sequence_clusters.add_argument("--graph", default="artifacts/v1_graph.json")
    sequence_clusters.add_argument("--entry-id", action="append", default=[])
    sequence_clusters.add_argument(
        "--out",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    sequence_clusters.set_defaults(func=cmd_build_sequence_cluster_proxy)

    sequence_holdout = subparsers.add_parser(
        "build-sequence-distance-holdout-eval",
        help=(
            "evaluate geometry retrieval on a proxy sequence/fold-distance "
            "held-out partition"
        ),
    )
    sequence_holdout.add_argument("--slice-id", required=True)
    sequence_holdout.add_argument(
        "--retrieval",
        default="artifacts/v3_geometry_retrieval.json",
    )
    sequence_holdout.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    sequence_holdout.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    sequence_holdout.add_argument("--geometry", default=None)
    sequence_holdout.add_argument("--abstain-threshold", type=float, default=0.4115)
    sequence_holdout.add_argument("--holdout-fraction", type=float, default=0.2)
    sequence_holdout.add_argument("--min-holdout-rows", type=int, default=40)
    sequence_holdout.add_argument(
        "--sequence-fasta",
        default=None,
        help=(
            "optional amino-acid FASTA keyed by m_csa entry ids or reference "
            "UniProt accessions for real MMseqs2 sequence-identity clustering"
        ),
    )
    sequence_holdout.add_argument(
        "--sequence-identity-backend",
        choices=("auto", "mmseqs", "proxy"),
        default="auto",
    )
    sequence_holdout.add_argument(
        "--sequence-identity-threshold",
        type=float,
        default=0.30,
    )
    sequence_holdout.add_argument(
        "--sequence-identity-coverage",
        type=float,
        default=0.80,
    )
    sequence_holdout.add_argument("--mmseqs-binary", default="mmseqs")
    sequence_holdout.add_argument(
        "--skip-max-train-test-identity",
        action="store_true",
        help="skip MMseqs2 train-vs-heldout identity search after clustering",
    )
    sequence_holdout.add_argument(
        "--out",
        default="artifacts/v3_sequence_distance_holdout_eval.json",
    )
    sequence_holdout.set_defaults(func=cmd_build_sequence_distance_holdout_eval)

    foldseek_readiness = subparsers.add_parser(
        "build-foldseek-coordinate-readiness",
        help=(
            "stage a bounded selected-coordinate set and report Foldseek "
            "readiness without computing a TM-score split"
        ),
    )
    foldseek_readiness.add_argument("--slice-id", required=True)
    foldseek_readiness.add_argument(
        "--retrieval",
        default="artifacts/v3_geometry_retrieval_1000.json",
    )
    foldseek_readiness.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    foldseek_readiness.add_argument(
        "--geometry",
        default="artifacts/v3_geometry_features_1000.json",
    )
    foldseek_readiness.add_argument(
        "--sequence-holdout",
        default=None,
        help="optional sequence-distance holdout artifact to define evaluated rows",
    )
    foldseek_readiness.add_argument(
        "--foldseek-binary",
        default="foldseek",
        help="Foldseek binary name or explicit path, used only for version provenance",
    )
    foldseek_readiness.add_argument(
        "--coordinate-dir",
        default="artifacts/foldseek_coordinates",
        help="directory for bounded staged mmCIF coordinate sidecars",
    )
    foldseek_readiness.add_argument(
        "--max-coordinate-files",
        type=int,
        default=0,
        help="maximum unique selected structures to fetch and stage; 0 records readiness only",
    )
    foldseek_readiness.add_argument(
        "--out",
        default="artifacts/v3_foldseek_coordinate_readiness.json",
    )
    foldseek_readiness.set_defaults(func=cmd_build_foldseek_coordinate_readiness)

    foldseek_tm_signal = subparsers.add_parser(
        "build-foldseek-tm-score-signal",
        help=(
            "run a bounded Foldseek all-vs-all search over already staged "
            "coordinates and write a partial review-only TM-score signal"
        ),
    )
    foldseek_tm_signal.add_argument("--slice-id", required=True)
    foldseek_tm_signal.add_argument(
        "--readiness",
        default="artifacts/v3_foldseek_coordinate_readiness_1000.json",
        help="Foldseek coordinate-readiness artifact with staged coordinate sidecars",
    )
    foldseek_tm_signal.add_argument(
        "--foldseek-binary",
        default="/private/tmp/catalytic-foldseek-env/bin/foldseek",
        help="explicit Foldseek binary path for version provenance and easy-search",
    )
    foldseek_tm_signal.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_signal_1000_staged25.json",
    )
    foldseek_tm_signal.add_argument(
        "--max-staged-coordinates",
        type=int,
        default=None,
        help=(
            "optional deterministic cap on staged coordinates included in the "
            "Foldseek easy-search signal; omitted means all staged coordinates"
        ),
    )
    foldseek_tm_signal.add_argument(
        "--prior-staged-coordinate-count",
        type=int,
        default=None,
        help=(
            "optional previous partial-signal staged-coordinate count to record "
            "when a larger bounded Foldseek signal removes that ceiling"
        ),
    )
    foldseek_tm_signal.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Foldseek thread count for easy-search",
    )
    foldseek_tm_signal.add_argument(
        "--summary-only",
        action="store_true",
        help=(
            "retain compact top train/test and target-violation rows while "
            "streaming aggregate pair counts, instead of serializing every "
            "Foldseek pair row"
        ),
    )
    foldseek_tm_signal.add_argument(
        "--max-reported-rows",
        type=int,
        default=200,
        help="maximum pair rows retained when --summary-only is used",
    )
    foldseek_tm_signal.set_defaults(func=cmd_build_foldseek_tm_score_signal)

    foldseek_all_materializable = subparsers.add_parser(
        "build-foldseek-tm-score-all-materializable-signal",
        help=(
            "run Foldseek over every staged materializable selected coordinate "
            "and write a compact review-only TM-score split summary"
        ),
    )
    foldseek_all_materializable.add_argument("--slice-id", required=True)
    foldseek_all_materializable.add_argument(
        "--readiness",
        default="artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json",
        help="Foldseek coordinate-readiness artifact with all staged coordinate sidecars",
    )
    foldseek_all_materializable.add_argument(
        "--foldseek-binary",
        default="/private/tmp/catalytic-foldseek-env/bin/foldseek",
        help="explicit Foldseek binary path for version provenance and easy-search",
    )
    foldseek_all_materializable.add_argument(
        "--max-runtime-seconds",
        type=int,
        default=None,
        help="optional wall-clock timeout for the Foldseek easy-search command",
    )
    foldseek_all_materializable.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Foldseek thread count to record and pass to easy-search",
    )
    foldseek_all_materializable.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold for train/test TM-score pairs",
    )
    foldseek_all_materializable.add_argument(
        "--max-reported-pairs",
        type=int,
        default=20,
        help="maximum top train/test and blocking pair summaries to keep",
    )
    foldseek_all_materializable.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json",
    )
    foldseek_all_materializable.set_defaults(
        func=cmd_build_foldseek_tm_score_all_materializable_signal
    )

    foldseek_query_chunk = subparsers.add_parser(
        "build-foldseek-tm-score-query-chunk-signal",
        help=(
            "run one resumable Foldseek query chunk against all staged "
            "materializable selected coordinates"
        ),
    )
    foldseek_query_chunk.add_argument("--slice-id", required=True)
    foldseek_query_chunk.add_argument(
        "--readiness",
        default="artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json",
        help="Foldseek coordinate-readiness artifact with all staged coordinate sidecars",
    )
    foldseek_query_chunk.add_argument(
        "--foldseek-binary",
        default="/private/tmp/catalytic-foldseek-env/bin/foldseek",
        help="explicit Foldseek binary path for version provenance and easy-search",
    )
    foldseek_query_chunk.add_argument(
        "--chunk-index",
        type=int,
        default=0,
        help="zero-based deterministic query chunk index",
    )
    foldseek_query_chunk.add_argument(
        "--chunk-size",
        type=int,
        default=12,
        help="number of staged coordinates to use as queries in this chunk",
    )
    foldseek_query_chunk.add_argument(
        "--max-runtime-seconds",
        type=int,
        default=None,
        help="optional wall-clock timeout for this Foldseek query chunk",
    )
    foldseek_query_chunk.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Foldseek thread count to record and pass to easy-search",
    )
    foldseek_query_chunk.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold for train/test TM-score pairs",
    )
    foldseek_query_chunk.add_argument(
        "--max-reported-pairs",
        type=int,
        default=20,
        help="maximum top train/test and blocking pair summaries to keep",
    )
    foldseek_query_chunk.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000.json",
    )
    foldseek_query_chunk.set_defaults(
        func=cmd_build_foldseek_tm_score_query_chunk_signal
    )

    foldseek_query_chunk_aggregate = subparsers.add_parser(
        "aggregate-foldseek-tm-score-query-chunks",
        help=(
            "aggregate completed resumable Foldseek query chunk signals "
            "without claiming a full TM-score holdout"
        ),
    )
    foldseek_query_chunk_aggregate.add_argument("--slice-id", required=True)
    foldseek_query_chunk_aggregate.add_argument(
        "--chunks",
        nargs="+",
        required=True,
        help="Foldseek query chunk signal artifacts to aggregate",
    )
    foldseek_query_chunk_aggregate.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold for train/test TM-score pairs",
    )
    foldseek_query_chunk_aggregate.add_argument(
        "--max-reported-pairs",
        type=int,
        default=30,
        help="maximum top train/test and blocking pair summaries to keep",
    )
    foldseek_query_chunk_aggregate.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate.json",
    )
    foldseek_query_chunk_aggregate.set_defaults(
        func=cmd_aggregate_foldseek_tm_score_query_chunks
    )

    foldseek_target_failure = subparsers.add_parser(
        "audit-foldseek-tm-score-target-failure",
        help=(
            "summarize the exact Foldseek train/test TM-score pairs that "
            "block the current <0.7 holdout target"
        ),
    )
    foldseek_target_failure.add_argument(
        "--signal",
        default="artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json",
        help="Foldseek TM-score signal artifact to audit",
    )
    foldseek_target_failure.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold; pairs at or above this value block the target",
    )
    foldseek_target_failure.add_argument(
        "--max-blocking-pairs",
        type=int,
        default=20,
        help="maximum unique blocking structure pairs to include",
    )
    foldseek_target_failure.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_target_failure_audit.json",
    )
    foldseek_target_failure.set_defaults(
        func=cmd_audit_foldseek_tm_score_target_failure
    )

    foldseek_split_repair = subparsers.add_parser(
        "audit-foldseek-tm-score-split-repair",
        help=(
            "plan conservative split repairs for observed Foldseek train/test "
            "TM-score target failures without applying the repair"
        ),
    )
    foldseek_split_repair.add_argument(
        "--target-failure",
        default="artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json",
        help="Foldseek TM-score target-failure audit artifact",
    )
    foldseek_split_repair.add_argument(
        "--sequence-holdout",
        default="artifacts/v3_sequence_distance_holdout_eval_1000.json",
        help="sequence-distance holdout artifact defining row partitions",
    )
    foldseek_split_repair.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold; pairs at or above this value need repair",
    )
    foldseek_split_repair.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_split_repair_plan.json",
    )
    foldseek_split_repair.set_defaults(func=cmd_audit_foldseek_tm_score_split_repair)

    foldseek_split_projection = subparsers.add_parser(
        "project-foldseek-tm-score-split-repair",
        help=(
            "project a proposed split repair across existing Foldseek signal rows "
            "without mutating the sequence holdout"
        ),
    )
    foldseek_split_projection.add_argument(
        "--signal",
        default="artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json",
        help="Foldseek TM-score signal artifact to reclassify in projection",
    )
    foldseek_split_projection.add_argument(
        "--repair-plan",
        default="artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json",
        help="Foldseek split-repair plan artifact",
    )
    foldseek_split_projection.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold for the projected train/test pairs",
    )
    foldseek_split_projection.add_argument(
        "--max-reported-pairs",
        type=int,
        default=20,
        help="maximum projected top train/test pairs and blockers to include",
    )
    foldseek_split_projection.add_argument(
        "--out",
        default="artifacts/v3_foldseek_tm_score_split_repair_projection.json",
    )
    foldseek_split_projection.set_defaults(
        func=cmd_project_foldseek_tm_score_split_repair
    )

    sequence_split_repair_candidate = subparsers.add_parser(
        "build-sequence-distance-holdout-split-repair-candidate",
        help=(
            "apply a Foldseek split-repair plan to a candidate copy of the "
            "sequence-distance holdout"
        ),
    )
    sequence_split_repair_candidate.add_argument(
        "--sequence-holdout",
        default="artifacts/v3_sequence_distance_holdout_eval_1000.json",
        help="source sequence-distance holdout artifact",
    )
    sequence_split_repair_candidate.add_argument(
        "--repair-plan",
        default="artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json",
        help="Foldseek split-repair plan artifact",
    )
    sequence_split_repair_candidate.add_argument(
        "--projection",
        default="artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json",
        help="optional Foldseek split-repair projection artifact",
    )
    sequence_split_repair_candidate.add_argument(
        "--out",
        default="artifacts/v3_sequence_distance_holdout_split_repair_candidate.json",
    )
    sequence_split_repair_candidate.set_defaults(
        func=cmd_build_sequence_distance_holdout_split_repair_candidate
    )

    sequence_split_redesign_candidate = subparsers.add_parser(
        "build-sequence-distance-holdout-split-redesign-candidate",
        help=(
            "apply a review-only Foldseek query-chunk split redesign to a "
            "candidate sequence-distance holdout"
        ),
    )
    sequence_split_redesign_candidate.add_argument(
        "--sequence-holdout",
        default="artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json",
        help="source candidate sequence-distance holdout artifact",
    )
    sequence_split_redesign_candidate.add_argument(
        "--split-repair-plan",
        default="artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json",
        help="Foldseek query-chunk split-repair plan artifact",
    )
    sequence_split_redesign_candidate.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="exclusive target threshold for observed Foldseek blocker pairs",
    )
    sequence_split_redesign_candidate.add_argument(
        "--out",
        default="artifacts/v3_sequence_distance_holdout_split_redesign_candidate.json",
    )
    sequence_split_redesign_candidate.set_defaults(
        func=cmd_build_sequence_distance_holdout_split_redesign_candidate
    )

    source_scale_limits = subparsers.add_parser(
        "audit-source-scale-limits",
        help="audit whether the current source slice can support the next scale target",
    )
    source_scale_limits.add_argument("--graph", default="artifacts/v1_graph.json")
    source_scale_limits.add_argument(
        "--prior-graph",
        default=None,
        help="previous accepted graph slice for new-entry diffing",
    )
    source_scale_limits.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    source_scale_limits.add_argument("--review-debt", default=None)
    source_scale_limits.add_argument("--label-expansion-candidates", default=None)
    source_scale_limits.add_argument("--target-source-entries", type=int, required=True)
    source_scale_limits.add_argument(
        "--public-target-countable-labels",
        type=int,
        default=10000,
    )
    source_scale_limits.add_argument(
        "--out",
        default="artifacts/v3_source_scale_limit_audit.json",
    )
    source_scale_limits.set_defaults(func=cmd_audit_source_scale_limits)

    transfer_manifest = subparsers.add_parser(
        "build-external-source-transfer-manifest",
        help="scope external-source label transfer without creating countable labels",
    )
    transfer_manifest.add_argument(
        "--source-scale-audit",
        default="artifacts/v3_source_scale_limit_audit.json",
    )
    transfer_manifest.add_argument(
        "--learned-retrieval-manifest",
        default="artifacts/v3_learned_retrieval_manifest.json",
    )
    transfer_manifest.add_argument(
        "--sequence-similarity-failure-sets",
        default="artifacts/v3_sequence_similarity_failure_sets.json",
    )
    transfer_manifest.add_argument(
        "--ontology-gap-audit",
        default="artifacts/v3_mechanism_ontology_gap_audit.json",
    )
    transfer_manifest.add_argument(
        "--active-learning-queue",
        default="artifacts/v3_active_learning_review_queue.json",
    )
    transfer_manifest.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    transfer_manifest.add_argument(
        "--out",
        default="artifacts/v3_external_source_transfer_manifest.json",
    )
    transfer_manifest.set_defaults(func=cmd_build_external_source_transfer_manifest)

    transfer_queries = subparsers.add_parser(
        "build-external-source-query-manifest",
        help="draft non-countable external-source query lanes from ontology gaps",
    )
    transfer_queries.add_argument(
        "--transfer-manifest",
        default="artifacts/v3_external_source_transfer_manifest.json",
    )
    transfer_queries.add_argument(
        "--ontology-gap-audit",
        default="artifacts/v3_mechanism_ontology_gap_audit.json",
    )
    transfer_queries.add_argument("--max-lanes", type=int, default=8)
    transfer_queries.add_argument(
        "--out",
        default="artifacts/v3_external_source_query_manifest.json",
    )
    transfer_queries.set_defaults(func=cmd_build_external_source_query_manifest)

    external_ood = subparsers.add_parser(
        "build-external-ood-calibration-plan",
        help="plan OOD controls before external-source label transfer",
    )
    external_ood.add_argument(
        "--query-manifest",
        default="artifacts/v3_external_source_query_manifest.json",
    )
    external_ood.add_argument(
        "--sequence-similarity-failure-sets",
        default="artifacts/v3_sequence_similarity_failure_sets.json",
    )
    external_ood.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    external_ood.add_argument(
        "--out",
        default="artifacts/v3_external_ood_calibration_plan.json",
    )
    external_ood.set_defaults(func=cmd_build_external_ood_calibration_plan)

    external_sample = subparsers.add_parser(
        "build-external-source-candidate-sample",
        help="fetch a bounded non-countable external-source candidate sample",
    )
    external_sample.add_argument(
        "--query-manifest",
        default="artifacts/v3_external_source_query_manifest.json",
    )
    external_sample.add_argument("--max-records-per-lane", type=int, default=5)
    external_sample.add_argument(
        "--out",
        default="artifacts/v3_external_source_candidate_sample.json",
    )
    external_sample.set_defaults(func=cmd_build_external_source_candidate_sample)

    external_sample_audit = subparsers.add_parser(
        "audit-external-source-candidate-sample",
        help="verify external-source samples remain non-countable",
    )
    external_sample_audit.add_argument(
        "--candidate-sample",
        default="artifacts/v3_external_source_candidate_sample.json",
    )
    external_sample_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_candidate_sample_audit.json",
    )
    external_sample_audit.set_defaults(func=cmd_audit_external_source_candidate_sample)

    external_candidate_manifest = subparsers.add_parser(
        "build-external-source-candidate-manifest",
        help="attach external-source candidates to OOD and sequence controls",
    )
    external_candidate_manifest.add_argument(
        "--candidate-sample",
        default="artifacts/v3_external_source_candidate_sample.json",
    )
    external_candidate_manifest.add_argument(
        "--ood-calibration-plan",
        default="artifacts/v3_external_ood_calibration_plan.json",
    )
    external_candidate_manifest.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    external_candidate_manifest.add_argument(
        "--sequence-similarity-failure-sets",
        default="artifacts/v3_sequence_similarity_failure_sets.json",
    )
    external_candidate_manifest.add_argument(
        "--transfer-manifest",
        default="artifacts/v3_external_source_transfer_manifest.json",
    )
    external_candidate_manifest.add_argument(
        "--out",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_candidate_manifest.set_defaults(
        func=cmd_build_external_source_candidate_manifest
    )

    external_candidate_manifest_audit = subparsers.add_parser(
        "audit-external-source-candidate-manifest",
        help="verify external-source candidate manifests remain review-only",
    )
    external_candidate_manifest_audit.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_candidate_manifest_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_candidate_manifest_audit.json",
    )
    external_candidate_manifest_audit.set_defaults(
        func=cmd_audit_external_source_candidate_manifest
    )

    external_sequence_holdouts = subparsers.add_parser(
        "audit-external-source-sequence-holdouts",
        help="audit external sequence overlap holdouts and near-duplicate search debt",
    )
    external_sequence_holdouts.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_sequence_holdouts.add_argument("--max-rows", type=int, default=100)
    external_sequence_holdouts.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_holdout_audit.json",
    )
    external_sequence_holdouts.set_defaults(
        func=cmd_audit_external_source_sequence_holdouts
    )

    external_lane_balance = subparsers.add_parser(
        "audit-external-source-lane-balance",
        help="check external-source candidate lanes for review queue collapse",
    )
    external_lane_balance.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_lane_balance.add_argument("--min-lanes", type=int, default=3)
    external_lane_balance.add_argument(
        "--max-dominant-lane-fraction",
        type=float,
        default=0.6,
    )
    external_lane_balance.add_argument(
        "--out",
        default="artifacts/v3_external_source_lane_balance_audit.json",
    )
    external_lane_balance.set_defaults(func=cmd_audit_external_source_lane_balance)

    external_evidence_plan = subparsers.add_parser(
        "build-external-source-evidence-plan",
        help="plan review-only evidence collection for external-source candidates",
    )
    external_evidence_plan.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_evidence_plan.add_argument(
        "--candidate-manifest-audit",
        default="artifacts/v3_external_source_candidate_manifest_audit.json",
    )
    external_evidence_plan.add_argument(
        "--out",
        default="artifacts/v3_external_source_evidence_plan.json",
    )
    external_evidence_plan.set_defaults(func=cmd_build_external_source_evidence_plan)

    external_evidence_request_export = subparsers.add_parser(
        "build-external-source-evidence-request-export",
        help="export review-only evidence requests for external-source candidates",
    )
    external_evidence_request_export.add_argument(
        "--evidence-plan",
        default="artifacts/v3_external_source_evidence_plan.json",
    )
    external_evidence_request_export.add_argument("--max-rows", type=int, default=50)
    external_evidence_request_export.add_argument(
        "--out",
        default="artifacts/v3_external_source_evidence_request_export.json",
    )
    external_evidence_request_export.set_defaults(
        func=cmd_build_external_source_evidence_request_export
    )

    external_active_site_queue = subparsers.add_parser(
        "build-external-source-active-site-evidence-queue",
        help="prioritize review-only external candidates for active-site evidence",
    )
    external_active_site_queue.add_argument(
        "--evidence-plan",
        default="artifacts/v3_external_source_evidence_plan.json",
    )
    external_active_site_queue.add_argument("--max-rows", type=int, default=50)
    external_active_site_queue.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_evidence_queue.json",
    )
    external_active_site_queue.set_defaults(
        func=cmd_build_external_source_active_site_evidence_queue
    )

    external_active_site_sample = subparsers.add_parser(
        "build-external-source-active-site-evidence-sample",
        help="fetch bounded UniProt active-site evidence for external candidates",
    )
    external_active_site_sample.add_argument(
        "--active-site-evidence-queue",
        default="artifacts/v3_external_source_active_site_evidence_queue.json",
    )
    external_active_site_sample.add_argument("--max-candidates", type=int, default=8)
    external_active_site_sample.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_active_site_sample.set_defaults(
        func=cmd_build_external_source_active_site_evidence_sample
    )

    external_active_site_sample_audit = subparsers.add_parser(
        "audit-external-source-active-site-evidence-sample",
        help="verify external active-site evidence samples remain review-only",
    )
    external_active_site_sample_audit.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_active_site_sample_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_evidence_sample_audit.json",
    )
    external_active_site_sample_audit.set_defaults(
        func=cmd_audit_external_source_active_site_evidence_sample
    )

    external_heuristic_queue = subparsers.add_parser(
        "build-external-source-heuristic-control-queue",
        help="queue external candidates for review-only heuristic control scoring",
    )
    external_heuristic_queue.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_heuristic_queue.add_argument("--max-rows", type=int, default=25)
    external_heuristic_queue.add_argument(
        "--out",
        default="artifacts/v3_external_source_heuristic_control_queue.json",
    )
    external_heuristic_queue.set_defaults(
        func=cmd_build_external_source_heuristic_control_queue
    )

    external_heuristic_queue_audit = subparsers.add_parser(
        "audit-external-source-heuristic-control-queue",
        help="verify external heuristic control queues remain review-only",
    )
    external_heuristic_queue_audit.add_argument(
        "--heuristic-control-queue",
        default="artifacts/v3_external_source_heuristic_control_queue.json",
    )
    external_heuristic_queue_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_heuristic_control_queue_audit.json",
    )
    external_heuristic_queue_audit.set_defaults(
        func=cmd_audit_external_source_heuristic_control_queue
    )

    external_structure_mapping_plan = subparsers.add_parser(
        "build-external-source-structure-mapping-plan",
        help="plan review-only structure mapping for external candidates",
    )
    external_structure_mapping_plan.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_structure_mapping_plan.add_argument(
        "--heuristic-control-queue",
        default="artifacts/v3_external_source_heuristic_control_queue.json",
    )
    external_structure_mapping_plan.add_argument("--max-rows", type=int, default=25)
    external_structure_mapping_plan.add_argument(
        "--out",
        default="artifacts/v3_external_source_structure_mapping_plan.json",
    )
    external_structure_mapping_plan.set_defaults(
        func=cmd_build_external_source_structure_mapping_plan
    )

    external_structure_mapping_plan_audit = subparsers.add_parser(
        "audit-external-source-structure-mapping-plan",
        help="verify external structure-mapping plans remain review-only",
    )
    external_structure_mapping_plan_audit.add_argument(
        "--structure-mapping-plan",
        default="artifacts/v3_external_source_structure_mapping_plan.json",
    )
    external_structure_mapping_plan_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_structure_mapping_plan_audit.json",
    )
    external_structure_mapping_plan_audit.set_defaults(
        func=cmd_audit_external_source_structure_mapping_plan
    )

    external_structure_mapping_sample = subparsers.add_parser(
        "build-external-source-structure-mapping-sample",
        help="resolve a bounded review-only external structure mapping sample",
    )
    external_structure_mapping_sample.add_argument(
        "--structure-mapping-plan",
        default="artifacts/v3_external_source_structure_mapping_plan.json",
    )
    external_structure_mapping_sample.add_argument(
        "--max-candidates", type=int, default=4
    )
    external_structure_mapping_sample.add_argument(
        "--out",
        default="artifacts/v3_external_source_structure_mapping_sample.json",
    )
    external_structure_mapping_sample.set_defaults(
        func=cmd_build_external_source_structure_mapping_sample
    )

    external_structure_mapping_sample_audit = subparsers.add_parser(
        "audit-external-source-structure-mapping-sample",
        help="verify external structure mapping samples remain review-only",
    )
    external_structure_mapping_sample_audit.add_argument(
        "--structure-mapping-sample",
        default="artifacts/v3_external_source_structure_mapping_sample.json",
    )
    external_structure_mapping_sample_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_structure_mapping_sample_audit.json",
    )
    external_structure_mapping_sample_audit.set_defaults(
        func=cmd_audit_external_source_structure_mapping_sample
    )

    external_heuristic_scores = subparsers.add_parser(
        "build-external-source-heuristic-control-scores",
        help="score external structure mappings with the heuristic retrieval control",
    )
    external_heuristic_scores.add_argument(
        "--structure-mapping-sample",
        default="artifacts/v3_external_source_structure_mapping_sample.json",
    )
    external_heuristic_scores.add_argument("--top-k", type=int, default=5)
    external_heuristic_scores.add_argument(
        "--out",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_heuristic_scores.set_defaults(
        func=cmd_build_external_source_heuristic_control_scores
    )

    external_heuristic_scores_audit = subparsers.add_parser(
        "audit-external-source-heuristic-control-scores",
        help="verify external heuristic control scores remain review-only",
    )
    external_heuristic_scores_audit.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_heuristic_scores_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_heuristic_control_scores_audit.json",
    )
    external_heuristic_scores_audit.set_defaults(
        func=cmd_audit_external_source_heuristic_control_scores
    )

    external_failure_modes = subparsers.add_parser(
        "audit-external-source-failure-modes",
        help="summarize review-only external transfer failure modes",
    )
    external_failure_modes.add_argument(
        "--active-site-evidence-sample-audit",
        default="artifacts/v3_external_source_active_site_evidence_sample_audit.json",
    )
    external_failure_modes.add_argument(
        "--heuristic-control-queue",
        default="artifacts/v3_external_source_heuristic_control_queue.json",
    )
    external_failure_modes.add_argument(
        "--heuristic-control-scores-audit",
        default="artifacts/v3_external_source_heuristic_control_scores_audit.json",
    )
    external_failure_modes.add_argument(
        "--structure-mapping-sample-audit",
        default="artifacts/v3_external_source_structure_mapping_sample_audit.json",
    )
    external_failure_modes.add_argument(
        "--out",
        default="artifacts/v3_external_source_failure_mode_audit.json",
    )
    external_failure_modes.set_defaults(func=cmd_audit_external_source_failure_modes)

    external_control_repair = subparsers.add_parser(
        "build-external-source-control-repair-plan",
        help="plan review-only repairs for external active-site and heuristic controls",
    )
    external_control_repair.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_control_repair.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_control_repair.add_argument(
        "--heuristic-control-scores-audit",
        default="artifacts/v3_external_source_heuristic_control_scores_audit.json",
    )
    external_control_repair.add_argument(
        "--external-failure-mode-audit",
        default="artifacts/v3_external_source_failure_mode_audit.json",
    )
    external_control_repair.add_argument("--max-rows", type=int, default=100)
    external_control_repair.add_argument(
        "--out",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_control_repair.set_defaults(
        func=cmd_build_external_source_control_repair_plan
    )

    external_control_repair_audit = subparsers.add_parser(
        "audit-external-source-control-repair-plan",
        help="verify external control repair plans remain review-only",
    )
    external_control_repair_audit.add_argument(
        "--control-repair-plan",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_control_repair_audit.add_argument(
        "--external-failure-mode-audit",
        default="artifacts/v3_external_source_failure_mode_audit.json",
    )
    external_control_repair_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_control_repair_plan_audit.json",
    )
    external_control_repair_audit.set_defaults(
        func=cmd_audit_external_source_control_repair_plan
    )

    external_binding_context_repair = subparsers.add_parser(
        "build-external-source-binding-context-repair-plan",
        help="collect review-only binding context for active-site-gap external rows",
    )
    external_binding_context_repair.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_binding_context_repair.add_argument(
        "--control-repair-plan",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_binding_context_repair.add_argument("--max-rows", type=int, default=100)
    external_binding_context_repair.add_argument(
        "--out",
        default="artifacts/v3_external_source_binding_context_repair_plan.json",
    )
    external_binding_context_repair.set_defaults(
        func=cmd_build_external_source_binding_context_repair_plan
    )

    external_binding_context_repair_audit = subparsers.add_parser(
        "audit-external-source-binding-context-repair-plan",
        help="verify binding-context repair plans remain review-only",
    )
    external_binding_context_repair_audit.add_argument(
        "--binding-context-repair-plan",
        default="artifacts/v3_external_source_binding_context_repair_plan.json",
    )
    external_binding_context_repair_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_binding_context_repair_plan_audit.json",
    )
    external_binding_context_repair_audit.set_defaults(
        func=cmd_audit_external_source_binding_context_repair_plan
    )

    external_binding_context_mapping = subparsers.add_parser(
        "build-external-source-binding-context-mapping-sample",
        help="map review-only binding context for active-site-gap external rows",
    )
    external_binding_context_mapping.add_argument(
        "--binding-context-repair-plan",
        default="artifacts/v3_external_source_binding_context_repair_plan.json",
    )
    external_binding_context_mapping.add_argument(
        "--max-candidates", type=int, default=10
    )
    external_binding_context_mapping.add_argument(
        "--out",
        default="artifacts/v3_external_source_binding_context_mapping_sample.json",
    )
    external_binding_context_mapping.set_defaults(
        func=cmd_build_external_source_binding_context_mapping_sample
    )

    external_binding_context_mapping_audit = subparsers.add_parser(
        "audit-external-source-binding-context-mapping-sample",
        help="verify binding-context mapping samples remain review-only",
    )
    external_binding_context_mapping_audit.add_argument(
        "--binding-context-mapping-sample",
        default="artifacts/v3_external_source_binding_context_mapping_sample.json",
    )
    external_binding_context_mapping_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_binding_context_mapping_sample_audit.json",
    )
    external_binding_context_mapping_audit.set_defaults(
        func=cmd_audit_external_source_binding_context_mapping_sample
    )

    external_representation_control = subparsers.add_parser(
        "build-external-source-representation-control-manifest",
        help="expose review-only external controls for future representation scoring",
    )
    external_representation_control.add_argument(
        "--structure-mapping-sample",
        default="artifacts/v3_external_source_structure_mapping_sample.json",
    )
    external_representation_control.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_representation_control.add_argument(
        "--control-repair-plan",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_representation_control.add_argument("--max-rows", type=int, default=100)
    external_representation_control.add_argument(
        "--out",
        default="artifacts/v3_external_source_representation_control_manifest.json",
    )
    external_representation_control.set_defaults(
        func=cmd_build_external_source_representation_control_manifest
    )

    external_representation_control_audit = subparsers.add_parser(
        "audit-external-source-representation-control-manifest",
        help="verify external representation controls remain review-only",
    )
    external_representation_control_audit.add_argument(
        "--representation-control-manifest",
        default="artifacts/v3_external_source_representation_control_manifest.json",
    )
    external_representation_control_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_representation_control_manifest_audit.json",
    )
    external_representation_control_audit.set_defaults(
        func=cmd_audit_external_source_representation_control_manifest
    )

    external_representation_comparison = subparsers.add_parser(
        "build-external-source-representation-control-comparison",
        help="compare review-only external representation controls to heuristic baseline",
    )
    external_representation_comparison.add_argument(
        "--representation-control-manifest",
        default="artifacts/v3_external_source_representation_control_manifest.json",
    )
    external_representation_comparison.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_representation_comparison.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_representation_comparison.add_argument(
        "--max-rows", type=int, default=100
    )
    external_representation_comparison.add_argument(
        "--out",
        default="artifacts/v3_external_source_representation_control_comparison.json",
    )
    external_representation_comparison.set_defaults(
        func=cmd_build_external_source_representation_control_comparison
    )

    external_representation_comparison_audit = subparsers.add_parser(
        "audit-external-source-representation-control-comparison",
        help="verify external representation-control comparisons remain review-only",
    )
    external_representation_comparison_audit.add_argument(
        "--representation-control-comparison",
        default="artifacts/v3_external_source_representation_control_comparison.json",
    )
    external_representation_comparison_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_representation_control_comparison_audit.json"
        ),
    )
    external_representation_comparison_audit.set_defaults(
        func=cmd_audit_external_source_representation_control_comparison
    )

    external_representation_backend_plan = subparsers.add_parser(
        "build-external-source-representation-backend-plan",
        help="plan review-only real representation backend controls",
    )
    external_representation_backend_plan.add_argument(
        "--representation-control-manifest",
        default="artifacts/v3_external_source_representation_control_manifest.json",
    )
    external_representation_backend_plan.add_argument(
        "--representation-control-comparison",
        default="artifacts/v3_external_source_representation_control_comparison.json",
    )
    external_representation_backend_plan.add_argument(
        "--sequence-search-export",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_representation_backend_plan.add_argument("--max-rows", type=int, default=100)
    external_representation_backend_plan.add_argument(
        "--out",
        default="artifacts/v3_external_source_representation_backend_plan.json",
    )
    external_representation_backend_plan.set_defaults(
        func=cmd_build_external_source_representation_backend_plan
    )

    external_pilot_representation_backend_plan = subparsers.add_parser(
        "build-external-source-pilot-representation-backend-plan",
        help="plan review-only sequence representation controls for selected pilot rows",
    )
    external_pilot_representation_backend_plan.add_argument(
        "--pilot-candidate-priority",
        default="artifacts/v3_external_source_pilot_candidate_priority.json",
    )
    external_pilot_representation_backend_plan.add_argument(
        "--sequence-search-export",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_pilot_representation_backend_plan.add_argument(
        "--max-rows", type=int, default=10
    )
    external_pilot_representation_backend_plan.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_pilot_representation_backend_plan.json"
        ),
    )
    external_pilot_representation_backend_plan.set_defaults(
        func=cmd_build_external_source_pilot_representation_backend_plan
    )

    external_representation_backend_plan_audit = subparsers.add_parser(
        "audit-external-source-representation-backend-plan",
        help="verify external representation backend plans remain review-only",
    )
    external_representation_backend_plan_audit.add_argument(
        "--representation-backend-plan",
        default="artifacts/v3_external_source_representation_backend_plan.json",
    )
    external_representation_backend_plan_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_representation_backend_plan_audit.json",
    )
    external_representation_backend_plan_audit.set_defaults(
        func=cmd_audit_external_source_representation_backend_plan
    )

    external_representation_backend_sample = subparsers.add_parser(
        "build-external-source-representation-backend-sample",
        help="compute a review-only sequence representation control",
    )
    external_representation_backend_sample.add_argument(
        "--representation-backend-plan",
        default="artifacts/v3_external_source_representation_backend_plan.json",
    )
    external_representation_backend_sample.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_representation_backend_sample.add_argument(
        "--max-rows", type=int, default=100
    )
    external_representation_backend_sample.add_argument("--top-k", type=int, default=3)
    external_representation_backend_sample.add_argument(
        "--embedding-backend",
        default="deterministic_sequence_kmer_control",
        choices=(
            "deterministic_sequence_kmer_control",
            "esm2",
            "esm2_t6_8m_ur50d",
            "esm2_t12_35m_ur50d",
            "esm2_t30_150m_ur50d",
            "esm2_t33_650m_ur50d",
        ),
    )
    external_representation_backend_sample.add_argument(
        "--model-name",
        default="facebook/esm2_t6_8M_UR50D",
    )
    external_representation_backend_sample.add_argument(
        "--local-files-only",
        action="store_true",
        help="only use locally cached model files; do not download ESM-2 weights",
    )
    external_representation_backend_sample.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_representation_backend_sample.json"
        ),
    )
    external_representation_backend_sample.set_defaults(
        func=cmd_build_external_source_representation_backend_sample
    )

    external_representation_backend_sample_audit = subparsers.add_parser(
        "audit-external-source-representation-backend-sample",
        help="verify computed external representation samples remain review-only",
    )
    external_representation_backend_sample_audit.add_argument(
        "--representation-backend-sample",
        default=(
            "artifacts/"
            "v3_external_source_representation_backend_sample.json"
        ),
    )
    external_representation_backend_sample_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_representation_backend_sample_audit.json"
        ),
    )
    external_representation_backend_sample_audit.set_defaults(
        func=cmd_audit_external_source_representation_backend_sample
    )

    external_representation_backend_stability_audit = subparsers.add_parser(
        "audit-external-source-representation-backend-stability",
        help="compare review-only representation samples across embedding backends",
    )
    external_representation_backend_stability_audit.add_argument(
        "--baseline-representation-backend-sample",
        default="artifacts/v3_external_source_representation_backend_sample.json",
    )
    external_representation_backend_stability_audit.add_argument(
        "--comparison-representation-backend-sample",
        default=(
            "artifacts/"
            "v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample.json"
        ),
    )
    external_representation_backend_stability_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_representation_backend_stability_audit.json"
        ),
    )
    external_representation_backend_stability_audit.set_defaults(
        func=cmd_audit_external_source_representation_backend_stability
    )

    external_pilot_representation_adjudication = subparsers.add_parser(
        "audit-external-source-pilot-representation-adjudication",
        help=(
            "adjudicate selected pilot representation controls from 8M versus "
            "largest-feasible ESM-2 stability evidence"
        ),
    )
    external_pilot_representation_adjudication.add_argument(
        "--pilot-candidate-priority",
        default="artifacts/v3_external_source_pilot_candidate_priority_1025.json",
    )
    external_pilot_representation_adjudication.add_argument(
        "--pilot-representation-backend-sample",
        default=(
            "artifacts/"
            "v3_external_source_pilot_representation_backend_sample_1025.json"
        ),
    )
    external_pilot_representation_adjudication.add_argument(
        "--pilot-representation-stability-audit",
        default=(
            "artifacts/"
            "v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_"
            "stability_audit_1025.json"
        ),
    )
    external_pilot_representation_adjudication.add_argument(
        "--pilot-active-site-evidence-decisions",
        default=(
            "artifacts/"
            "v3_external_source_pilot_active_site_evidence_decisions_1025.json"
        ),
    )
    external_pilot_representation_adjudication.add_argument(
        "--max-rows", type=int, default=10
    )
    external_pilot_representation_adjudication.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_pilot_representation_adjudication_1025.json"
        ),
    )
    external_pilot_representation_adjudication.set_defaults(
        func=cmd_audit_external_source_pilot_representation_adjudication
    )

    external_broad_ec_audit = subparsers.add_parser(
        "audit-external-source-broad-ec-disambiguation",
        help="narrow broad external EC repair rows to review-only reaction context",
    )
    external_broad_ec_audit.add_argument(
        "--control-repair-plan",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_broad_ec_audit.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_broad_ec_audit.add_argument("--max-rows", type=int, default=100)
    external_broad_ec_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_broad_ec_disambiguation_audit.json",
    )
    external_broad_ec_audit.set_defaults(
        func=cmd_audit_external_source_broad_ec_disambiguation
    )

    external_active_site_gap_sources = subparsers.add_parser(
        "build-external-source-active-site-gap-source-requests",
        help="export review-only sourcing requests for external active-site gaps",
    )
    external_active_site_gap_sources.add_argument(
        "--control-repair-plan",
        default="artifacts/v3_external_source_control_repair_plan.json",
    )
    external_active_site_gap_sources.add_argument(
        "--binding-context-repair-plan",
        default="artifacts/v3_external_source_binding_context_repair_plan.json",
    )
    external_active_site_gap_sources.add_argument(
        "--binding-context-mapping-sample",
        default="artifacts/v3_external_source_binding_context_mapping_sample.json",
    )
    external_active_site_gap_sources.add_argument("--max-rows", type=int, default=100)
    external_active_site_gap_sources.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_gap_source_requests.json",
    )
    external_active_site_gap_sources.set_defaults(
        func=cmd_build_external_source_active_site_gap_source_requests
    )

    external_sequence_neighborhood = subparsers.add_parser(
        "build-external-source-sequence-neighborhood-plan",
        help="prepare review-only near-duplicate sequence controls for external rows",
    )
    external_sequence_neighborhood.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_sequence_neighborhood.add_argument(
        "--sequence-holdout-audit",
        default="artifacts/v3_external_source_sequence_holdout_audit.json",
    )
    external_sequence_neighborhood.add_argument("--max-rows", type=int, default=100)
    external_sequence_neighborhood.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_neighborhood_plan.json",
    )
    external_sequence_neighborhood.set_defaults(
        func=cmd_build_external_source_sequence_neighborhood_plan
    )

    external_sequence_neighborhood_sample = subparsers.add_parser(
        "build-external-source-sequence-neighborhood-sample",
        help="run a bounded review-only sequence-neighborhood control screen",
    )
    external_sequence_neighborhood_sample.add_argument(
        "--sequence-neighborhood-plan",
        default="artifacts/v3_external_source_sequence_neighborhood_plan.json",
    )
    external_sequence_neighborhood_sample.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    external_sequence_neighborhood_sample.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    external_sequence_neighborhood_sample.add_argument(
        "--max-external-rows", type=int, default=30
    )
    external_sequence_neighborhood_sample.add_argument(
        "--max-reference-sequences", type=int, default=1000
    )
    external_sequence_neighborhood_sample.add_argument("--top-k", type=int, default=3)
    external_sequence_neighborhood_sample.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_sequence_neighborhood_sample.set_defaults(
        func=cmd_build_external_source_sequence_neighborhood_sample
    )

    external_sequence_neighborhood_sample_audit = subparsers.add_parser(
        "audit-external-source-sequence-neighborhood-sample",
        help="verify sequence-neighborhood screens remain review-only controls",
    )
    external_sequence_neighborhood_sample_audit.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_sequence_neighborhood_sample_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_sequence_neighborhood_sample_audit.json"
        ),
    )
    external_sequence_neighborhood_sample_audit.set_defaults(
        func=cmd_audit_external_source_sequence_neighborhood_sample
    )

    external_sequence_alignment = subparsers.add_parser(
        "build-external-source-sequence-alignment-verification",
        help="verify sequence-neighborhood top hits with bounded alignments",
    )
    external_sequence_alignment.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_sequence_alignment.add_argument("--top-k", type=int, default=3)
    external_sequence_alignment.add_argument("--max-pairs", type=int, default=120)
    external_sequence_alignment.add_argument(
        "--max-alignment-cells", type=int, default=1500000
    )
    external_sequence_alignment.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_alignment_verification.json",
    )
    external_sequence_alignment.set_defaults(
        func=cmd_build_external_source_sequence_alignment_verification
    )

    external_sequence_alignment_audit = subparsers.add_parser(
        "audit-external-source-sequence-alignment-verification",
        help="verify bounded sequence-alignment checks remain review-only",
    )
    external_sequence_alignment_audit.add_argument(
        "--sequence-alignment-verification",
        default="artifacts/v3_external_source_sequence_alignment_verification.json",
    )
    external_sequence_alignment_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_sequence_alignment_verification_audit.json"
        ),
    )
    external_sequence_alignment_audit.set_defaults(
        func=cmd_audit_external_source_sequence_alignment_verification
    )

    external_sequence_reference_screen_audit = subparsers.add_parser(
        "audit-external-source-sequence-reference-screen",
        help="verify current countable-reference sequence screen coverage",
    )
    external_sequence_reference_screen_audit.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_sequence_reference_screen_audit.add_argument(
        "--sequence-alignment-verification",
        default="artifacts/v3_external_source_sequence_alignment_verification.json",
    )
    external_sequence_reference_screen_audit.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    external_sequence_reference_screen_audit.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    external_sequence_reference_screen_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_reference_screen_audit.json",
    )
    external_sequence_reference_screen_audit.set_defaults(
        func=cmd_audit_external_source_sequence_reference_screen
    )

    external_backend_sequence_search = subparsers.add_parser(
        "build-external-source-backend-sequence-search",
        help="run a real backend external-vs-current-reference sequence search",
    )
    external_backend_sequence_search.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_backend_sequence_search.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy.json",
    )
    external_backend_sequence_search.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    external_backend_sequence_search.add_argument(
        "--reference-fasta",
        default="artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta",
    )
    external_backend_sequence_search.add_argument(
        "--external-fasta-out",
        default="artifacts/v3_external_source_backend_sequence_search_external.fasta",
    )
    external_backend_sequence_search.add_argument(
        "--reference-fasta-out",
        default="artifacts/v3_external_source_backend_sequence_search_reference.fasta",
    )
    external_backend_sequence_search.add_argument(
        "--result-tsv-out",
        default="artifacts/v3_external_source_backend_sequence_search.tsv",
    )
    external_backend_sequence_search.add_argument(
        "--backend", choices=("auto", "mmseqs", "diamond", "blastp"), default="auto"
    )
    external_backend_sequence_search.add_argument("--mmseqs-binary", default="mmseqs")
    external_backend_sequence_search.add_argument("--diamond-binary", default="diamond")
    external_backend_sequence_search.add_argument("--blastp-binary", default="blastp")
    external_backend_sequence_search.add_argument(
        "--makeblastdb-binary", default="makeblastdb"
    )
    external_backend_sequence_search.add_argument(
        "--identity-threshold", type=float, default=0.90
    )
    external_backend_sequence_search.add_argument(
        "--coverage-threshold", type=float, default=0.80
    )
    external_backend_sequence_search.add_argument(
        "--exact-identity-threshold", type=float, default=0.999
    )
    external_backend_sequence_search.add_argument(
        "--exact-coverage-threshold", type=float, default=0.98
    )
    external_backend_sequence_search.add_argument("--max-rows", type=int, default=100)
    external_backend_sequence_search.add_argument("--top-k", type=int, default=5)
    external_backend_sequence_search.add_argument(
        "--out",
        default="artifacts/v3_external_source_backend_sequence_search.json",
    )
    external_backend_sequence_search.set_defaults(
        func=cmd_build_external_source_backend_sequence_search
    )

    external_backend_sequence_search_audit = subparsers.add_parser(
        "audit-external-source-backend-sequence-search",
        help="verify real backend sequence-search artifacts remain review-only",
    )
    external_backend_sequence_search_audit.add_argument(
        "--backend-sequence-search",
        default="artifacts/v3_external_source_backend_sequence_search.json",
    )
    external_backend_sequence_search_audit.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_backend_sequence_search_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_backend_sequence_search_audit.json",
    )
    external_backend_sequence_search_audit.set_defaults(
        func=cmd_audit_external_source_backend_sequence_search
    )

    external_sequence_search_export = subparsers.add_parser(
        "build-external-source-sequence-search-export",
        help="build review-only complete near-duplicate sequence-search packets",
    )
    external_sequence_search_export.add_argument(
        "--sequence-neighborhood-plan",
        default="artifacts/v3_external_source_sequence_neighborhood_plan.json",
    )
    external_sequence_search_export.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_sequence_search_export.add_argument(
        "--sequence-alignment-verification",
        default="artifacts/v3_external_source_sequence_alignment_verification.json",
    )
    external_sequence_search_export.add_argument(
        "--sequence-reference-screen-audit",
        default=None,
    )
    external_sequence_search_export.add_argument("--max-rows", type=int, default=100)
    external_sequence_search_export.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_sequence_search_export.set_defaults(
        func=cmd_build_external_source_sequence_search_export
    )

    external_sequence_search_export_audit = subparsers.add_parser(
        "audit-external-source-sequence-search-export",
        help="verify external sequence-search exports remain review-only",
    )
    external_sequence_search_export_audit.add_argument(
        "--sequence-search-export",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_sequence_search_export_audit.add_argument(
        "--sequence-neighborhood-plan",
        default="artifacts/v3_external_source_sequence_neighborhood_plan.json",
    )
    external_sequence_search_export_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_sequence_search_export_audit.json",
    )
    external_sequence_search_export_audit.set_defaults(
        func=cmd_audit_external_source_sequence_search_export
    )

    external_import_readiness = subparsers.add_parser(
        "audit-external-source-import-readiness",
        help="summarize remaining review-only blockers before external label import",
    )
    external_import_readiness.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_import_readiness.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_import_readiness.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_import_readiness.add_argument(
        "--representation-control-comparison",
        default="artifacts/v3_external_source_representation_control_comparison.json",
    )
    external_import_readiness.add_argument(
        "--active-site-gap-source-requests",
        default="artifacts/v3_external_source_active_site_gap_source_requests.json",
    )
    external_import_readiness.add_argument(
        "--sequence-neighborhood-sample",
        default="artifacts/v3_external_source_sequence_neighborhood_sample.json",
    )
    external_import_readiness.add_argument(
        "--sequence-alignment-verification",
        default=None,
    )
    external_import_readiness.add_argument(
        "--backend-sequence-search",
        default=None,
    )
    external_import_readiness.add_argument("--max-rows", type=int, default=100)
    external_import_readiness.add_argument(
        "--out",
        default="artifacts/v3_external_source_import_readiness_audit.json",
    )
    external_import_readiness.set_defaults(
        func=cmd_audit_external_source_import_readiness
    )

    external_active_site_sourcing = subparsers.add_parser(
        "build-external-source-active-site-sourcing-queue",
        help="prioritize review-only active-site sourcing for external gaps",
    )
    external_active_site_sourcing.add_argument(
        "--active-site-gap-source-requests",
        default="artifacts/v3_external_source_active_site_gap_source_requests.json",
    )
    external_active_site_sourcing.add_argument(
        "--external-import-readiness-audit",
        default="artifacts/v3_external_source_import_readiness_audit.json",
    )
    external_active_site_sourcing.add_argument(
        "--sequence-alignment-verification",
        default=None,
    )
    external_active_site_sourcing.add_argument("--max-rows", type=int, default=100)
    external_active_site_sourcing.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_sourcing_queue.json",
    )
    external_active_site_sourcing.set_defaults(
        func=cmd_build_external_source_active_site_sourcing_queue
    )

    external_active_site_sourcing_audit = subparsers.add_parser(
        "audit-external-source-active-site-sourcing-queue",
        help="verify external active-site sourcing queues remain review-only",
    )
    external_active_site_sourcing_audit.add_argument(
        "--active-site-sourcing-queue",
        default="artifacts/v3_external_source_active_site_sourcing_queue.json",
    )
    external_active_site_sourcing_audit.add_argument(
        "--external-import-readiness-audit",
        default="artifacts/v3_external_source_import_readiness_audit.json",
    )
    external_active_site_sourcing_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_active_site_sourcing_queue_audit.json"
        ),
    )
    external_active_site_sourcing_audit.set_defaults(
        func=cmd_audit_external_source_active_site_sourcing_queue
    )

    external_active_site_sourcing_export = subparsers.add_parser(
        "build-external-source-active-site-sourcing-export",
        help="build review-only source packets for external active-site gaps",
    )
    external_active_site_sourcing_export.add_argument(
        "--active-site-sourcing-queue",
        default="artifacts/v3_external_source_active_site_sourcing_queue.json",
    )
    external_active_site_sourcing_export.add_argument(
        "--active-site-gap-source-requests",
        default="artifacts/v3_external_source_active_site_gap_source_requests.json",
    )
    external_active_site_sourcing_export.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_active_site_sourcing_export.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_active_site_sourcing_export.add_argument("--max-rows", type=int, default=100)
    external_active_site_sourcing_export.add_argument(
        "--out",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_active_site_sourcing_export.set_defaults(
        func=cmd_build_external_source_active_site_sourcing_export
    )

    external_active_site_sourcing_export_audit = subparsers.add_parser(
        "audit-external-source-active-site-sourcing-export",
        help="verify external active-site sourcing exports remain review-only",
    )
    external_active_site_sourcing_export_audit.add_argument(
        "--active-site-sourcing-export",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_active_site_sourcing_export_audit.add_argument(
        "--active-site-sourcing-queue",
        default="artifacts/v3_external_source_active_site_sourcing_queue.json",
    )
    external_active_site_sourcing_export_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_active_site_sourcing_export_audit.json"
        ),
    )
    external_active_site_sourcing_export_audit.set_defaults(
        func=cmd_audit_external_source_active_site_sourcing_export
    )

    external_active_site_sourcing_resolution = subparsers.add_parser(
        "build-external-source-active-site-sourcing-resolution",
        help="resolve active-site sourcing packets against UniProt feature evidence",
    )
    external_active_site_sourcing_resolution.add_argument(
        "--active-site-sourcing-export",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_active_site_sourcing_resolution.add_argument(
        "--max-rows", type=int, default=100
    )
    external_active_site_sourcing_resolution.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_active_site_sourcing_resolution.json"
        ),
    )
    external_active_site_sourcing_resolution.set_defaults(
        func=cmd_build_external_source_active_site_sourcing_resolution
    )

    external_active_site_sourcing_resolution_audit = subparsers.add_parser(
        "audit-external-source-active-site-sourcing-resolution",
        help="verify external active-site sourcing resolutions remain review-only",
    )
    external_active_site_sourcing_resolution_audit.add_argument(
        "--active-site-sourcing-resolution",
        default=(
            "artifacts/"
            "v3_external_source_active_site_sourcing_resolution.json"
        ),
    )
    external_active_site_sourcing_resolution_audit.add_argument(
        "--active-site-sourcing-export",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_active_site_sourcing_resolution_audit.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_active_site_sourcing_resolution_audit.json"
        ),
    )
    external_active_site_sourcing_resolution_audit.set_defaults(
        func=cmd_audit_external_source_active_site_sourcing_resolution
    )

    external_transfer_blocker_matrix = subparsers.add_parser(
        "build-external-source-transfer-blocker-matrix",
        help="join external transfer blocker packets into a review-only matrix",
    )
    external_transfer_blocker_matrix.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_transfer_blocker_matrix.add_argument(
        "--external-import-readiness-audit",
        default="artifacts/v3_external_source_import_readiness_audit.json",
    )
    external_transfer_blocker_matrix.add_argument(
        "--active-site-sourcing-export",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_transfer_blocker_matrix.add_argument(
        "--active-site-sourcing-resolution",
        default=None,
    )
    external_transfer_blocker_matrix.add_argument(
        "--sequence-search-export",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_transfer_blocker_matrix.add_argument(
        "--representation-backend-plan",
        default="artifacts/v3_external_source_representation_backend_plan.json",
    )
    external_transfer_blocker_matrix.add_argument(
        "--backend-sequence-search",
        default=None,
    )
    external_transfer_blocker_matrix.add_argument(
        "--representation-backend-sample",
        default=None,
    )
    external_transfer_blocker_matrix.add_argument("--max-rows", type=int, default=100)
    external_transfer_blocker_matrix.add_argument(
        "--out",
        default="artifacts/v3_external_source_transfer_blocker_matrix.json",
    )
    external_transfer_blocker_matrix.set_defaults(
        func=cmd_build_external_source_transfer_blocker_matrix
    )

    external_transfer_blocker_matrix_audit = subparsers.add_parser(
        "audit-external-source-transfer-blocker-matrix",
        help="verify external transfer blocker matrices remain review-only",
    )
    external_transfer_blocker_matrix_audit.add_argument(
        "--transfer-blocker-matrix",
        default="artifacts/v3_external_source_transfer_blocker_matrix.json",
    )
    external_transfer_blocker_matrix_audit.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_transfer_blocker_matrix_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_transfer_blocker_matrix_audit.json",
    )
    external_transfer_blocker_matrix_audit.set_defaults(
        func=cmd_audit_external_source_transfer_blocker_matrix
    )

    external_pilot_priority = subparsers.add_parser(
        "build-external-source-pilot-candidate-priority",
        help="rank review-only external candidates for a focused pilot worklist",
    )
    external_pilot_priority.add_argument(
        "--transfer-blocker-matrix",
        default="artifacts/v3_external_source_transfer_blocker_matrix.json",
    )
    external_pilot_priority.add_argument("--max-candidates", type=int, default=10)
    external_pilot_priority.add_argument("--max-per-lane", type=int, default=2)
    external_pilot_priority.add_argument(
        "--out",
        default="artifacts/v3_external_source_pilot_candidate_priority.json",
    )
    external_pilot_priority.set_defaults(
        func=cmd_build_external_source_pilot_candidate_priority
    )

    external_pilot_review_export = subparsers.add_parser(
        "build-external-source-pilot-review-decision-export",
        help="export no-decision review packets for selected external pilot rows",
    )
    external_pilot_review_export.add_argument(
        "--pilot-candidate-priority",
        default="artifacts/v3_external_source_pilot_candidate_priority.json",
    )
    external_pilot_review_export.add_argument("--max-rows", type=int, default=10)
    external_pilot_review_export.add_argument(
        "--out",
        default="artifacts/v3_external_source_pilot_review_decision_export.json",
    )
    external_pilot_review_export.set_defaults(
        func=cmd_build_external_source_pilot_review_decision_export
    )

    external_pilot_evidence_packet = subparsers.add_parser(
        "build-external-source-pilot-evidence-packet",
        help="join source targets for selected external pilot rows",
    )
    external_pilot_evidence_packet.add_argument(
        "--pilot-candidate-priority",
        default="artifacts/v3_external_source_pilot_candidate_priority.json",
    )
    external_pilot_evidence_packet.add_argument(
        "--active-site-sourcing-export",
        default="artifacts/v3_external_source_active_site_sourcing_export.json",
    )
    external_pilot_evidence_packet.add_argument(
        "--sequence-search-export",
        default="artifacts/v3_external_source_sequence_search_export.json",
    )
    external_pilot_evidence_packet.add_argument(
        "--backend-sequence-search",
        default=None,
    )
    external_pilot_evidence_packet.add_argument("--max-rows", type=int, default=10)
    external_pilot_evidence_packet.add_argument(
        "--out",
        default="artifacts/v3_external_source_pilot_evidence_packet.json",
    )
    external_pilot_evidence_packet.set_defaults(
        func=cmd_build_external_source_pilot_evidence_packet
    )

    external_pilot_dossiers = subparsers.add_parser(
        "build-external-source-pilot-evidence-dossiers",
        help="assemble per-candidate review evidence dossiers for selected pilot rows",
    )
    external_pilot_dossiers.add_argument(
        "--pilot-evidence-packet",
        default="artifacts/v3_external_source_pilot_evidence_packet.json",
    )
    external_pilot_dossiers.add_argument(
        "--active-site-evidence-sample",
        default="artifacts/v3_external_source_active_site_evidence_sample.json",
    )
    external_pilot_dossiers.add_argument(
        "--active-site-sourcing-resolution",
        default="artifacts/v3_external_source_active_site_sourcing_resolution.json",
    )
    external_pilot_dossiers.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_pilot_dossiers.add_argument(
        "--sequence-alignment-verification",
        default="artifacts/v3_external_source_sequence_alignment_verification.json",
    )
    external_pilot_dossiers.add_argument(
        "--representation-backend-sample",
        default="artifacts/v3_external_source_representation_backend_sample.json",
    )
    external_pilot_dossiers.add_argument(
        "--heuristic-control-scores",
        default="artifacts/v3_external_source_heuristic_control_scores.json",
    )
    external_pilot_dossiers.add_argument(
        "--structure-mapping-sample",
        default="artifacts/v3_external_source_structure_mapping_sample.json",
    )
    external_pilot_dossiers.add_argument(
        "--transfer-blocker-matrix",
        default="artifacts/v3_external_source_transfer_blocker_matrix.json",
    )
    external_pilot_dossiers.add_argument(
        "--external-import-readiness-audit",
        default=None,
    )
    external_pilot_dossiers.add_argument(
        "--out",
        default="artifacts/v3_external_source_pilot_evidence_dossiers.json",
    )
    external_pilot_dossiers.set_defaults(
        func=cmd_build_external_source_pilot_evidence_dossiers
    )

    external_pilot_active_site_decisions = subparsers.add_parser(
        "build-external-source-pilot-active-site-evidence-decisions",
        help=(
            "classify active-site evidence status for selected external pilot rows "
            "without import decisions"
        ),
    )
    external_pilot_active_site_decisions.add_argument(
        "--pilot-evidence-dossiers",
        default="artifacts/v3_external_source_pilot_evidence_dossiers_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--pilot-evidence-packet",
        default="artifacts/v3_external_source_pilot_evidence_packet_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--active-site-sourcing-resolution",
        default="artifacts/v3_external_source_active_site_sourcing_resolution_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--backend-sequence-search",
        default="artifacts/v3_external_source_backend_sequence_search_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--pilot-representation-backend-sample",
        default=(
            "artifacts/"
            "v3_external_source_pilot_representation_backend_sample_1025.json"
        ),
    )
    external_pilot_active_site_decisions.add_argument(
        "--transfer-blocker-matrix",
        default="artifacts/v3_external_source_transfer_blocker_matrix_1025.json",
    )
    external_pilot_active_site_decisions.add_argument(
        "--max-rows", type=int, default=10
    )
    external_pilot_active_site_decisions.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_external_source_pilot_active_site_evidence_decisions_1025.json"
        ),
    )
    external_pilot_active_site_decisions.set_defaults(
        func=cmd_build_external_source_pilot_active_site_evidence_decisions
    )

    external_pilot_success = subparsers.add_parser(
        "build-external-source-pilot-success-criteria",
        help="define measurable success criteria for selected external pilot rows",
    )
    external_pilot_success.add_argument(
        "--pilot-candidate-priority",
        default="artifacts/v3_external_source_pilot_candidate_priority_1025.json",
    )
    external_pilot_success.add_argument(
        "--pilot-review-decision-export",
        default=(
            "artifacts/v3_external_source_pilot_review_decision_export_1025.json"
        ),
    )
    external_pilot_success.add_argument(
        "--pilot-active-site-evidence-decisions",
        default=(
            "artifacts/"
            "v3_external_source_pilot_active_site_evidence_decisions_1025.json"
        ),
    )
    external_pilot_success.add_argument(
        "--external-import-readiness-audit",
        default="artifacts/v3_external_source_import_readiness_audit_1025.json",
    )
    external_pilot_success.add_argument(
        "--external-transfer-gate",
        default="artifacts/v3_external_source_transfer_gate_check_1025.json",
    )
    external_pilot_success.add_argument(
        "--pilot-representation-adjudication",
        default=None,
        help=(
            "optional selected-pilot representation adjudication artifact "
            "built from backend stability evidence"
        ),
    )
    external_pilot_success.add_argument("--max-rows", type=int, default=10)
    external_pilot_success.add_argument(
        "--min-import-ready-rows", type=int, default=1
    )
    external_pilot_success.add_argument(
        "--out",
        default="artifacts/v3_external_source_pilot_success_criteria_1025.json",
    )
    external_pilot_success.set_defaults(
        func=cmd_build_external_source_pilot_success_criteria
    )

    external_transfer_gate = subparsers.add_parser(
        "check-external-source-transfer-gates",
        help="gate review-only external-source transfer artifacts before import work",
    )
    external_transfer_gate.add_argument(
        "--transfer-manifest",
        default="artifacts/v3_external_source_transfer_manifest.json",
    )
    external_transfer_gate.add_argument(
        "--query-manifest",
        default="artifacts/v3_external_source_query_manifest.json",
    )
    external_transfer_gate.add_argument(
        "--ood-calibration-plan",
        default="artifacts/v3_external_ood_calibration_plan.json",
    )
    external_transfer_gate.add_argument(
        "--candidate-sample-audit",
        default="artifacts/v3_external_source_candidate_sample_audit.json",
    )
    external_transfer_gate.add_argument(
        "--candidate-manifest",
        default="artifacts/v3_external_source_candidate_manifest.json",
    )
    external_transfer_gate.add_argument(
        "--candidate-manifest-audit",
        default="artifacts/v3_external_source_candidate_manifest_audit.json",
    )
    external_transfer_gate.add_argument(
        "--lane-balance-audit",
        default="artifacts/v3_external_source_lane_balance_audit.json",
    )
    external_transfer_gate.add_argument(
        "--evidence-plan",
        default="artifacts/v3_external_source_evidence_plan.json",
    )
    external_transfer_gate.add_argument(
        "--evidence-request-export",
        default="artifacts/v3_external_source_evidence_request_export.json",
    )
    external_transfer_gate.add_argument(
        "--review-only-import-safety-audit",
        default="artifacts/v3_external_source_review_only_import_safety_audit.json",
    )
    external_transfer_gate.add_argument(
        "--active-site-evidence-queue",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-evidence-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-evidence-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--heuristic-control-queue",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--heuristic-control-queue-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--structure-mapping-plan",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--structure-mapping-plan-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--structure-mapping-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--structure-mapping-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--heuristic-control-scores",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--heuristic-control-scores-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--external-failure-mode-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--external-control-repair-plan",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--external-control-repair-plan-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--reaction-evidence-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--reaction-evidence-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-control-manifest",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-control-manifest-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-control-comparison",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-control-comparison-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-backend-plan",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-backend-plan-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-backend-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--representation-backend-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--broad-ec-disambiguation-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-gap-source-requests",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-neighborhood-plan",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-neighborhood-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-neighborhood-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-alignment-verification",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-alignment-verification-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-reference-screen-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-search-export",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-search-export-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-backend-search",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--external-import-readiness-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-queue",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-queue-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-export",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-export-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-resolution",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--active-site-sourcing-resolution-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--transfer-blocker-matrix",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--transfer-blocker-matrix-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-candidate-priority",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-review-decision-export",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-evidence-packet",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-evidence-dossiers",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-active-site-evidence-decisions",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--pilot-representation-backend-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--binding-context-repair-plan",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--binding-context-repair-plan-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--binding-context-mapping-sample",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--binding-context-mapping-sample-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--sequence-holdout-audit",
        default=None,
    )
    external_transfer_gate.add_argument(
        "--out",
        default="artifacts/v3_external_source_transfer_gate_check.json",
    )
    external_transfer_gate.set_defaults(func=cmd_check_external_source_transfer_gates)

    external_reaction_sample = subparsers.add_parser(
        "build-external-source-reaction-evidence-sample",
        help="fetch bounded Rhea reaction context for external-source candidates",
    )
    external_reaction_sample.add_argument(
        "--evidence-request-export",
        default="artifacts/v3_external_source_evidence_request_export.json",
    )
    external_reaction_sample.add_argument("--max-candidates", type=int, default=10)
    external_reaction_sample.add_argument(
        "--max-reactions-per-ec", type=int, default=3
    )
    external_reaction_sample.add_argument(
        "--out",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_reaction_sample.set_defaults(
        func=cmd_build_external_source_reaction_evidence_sample
    )

    external_reaction_sample_audit = subparsers.add_parser(
        "audit-external-source-reaction-evidence-sample",
        help="verify external reaction evidence samples remain review-only",
    )
    external_reaction_sample_audit.add_argument(
        "--reaction-evidence-sample",
        default="artifacts/v3_external_source_reaction_evidence_sample.json",
    )
    external_reaction_sample_audit.add_argument(
        "--out",
        default="artifacts/v3_external_source_reaction_evidence_sample_audit.json",
    )
    external_reaction_sample_audit.set_defaults(
        func=cmd_audit_external_source_reaction_evidence_sample
    )

    benchmark = subparsers.add_parser(
        "build-v2-benchmark",
        help="build mechanism-level benchmark records from a v1 graph",
    )
    benchmark.add_argument("--graph", default="artifacts/v1_graph.json")
    benchmark.add_argument("--out", default="artifacts/v2_benchmark.json")
    benchmark.set_defaults(func=cmd_build_v2_benchmark)

    baseline = subparsers.add_parser(
        "run-baseline",
        help="run seed fingerprint retrieval baseline on a V2 benchmark",
    )
    baseline.add_argument("--benchmark", default="artifacts/v2_benchmark.json")
    baseline.add_argument("--out", default="artifacts/v2_baseline.json")
    baseline.set_defaults(func=cmd_run_baseline)

    inconsistency = subparsers.add_parser(
        "detect-inconsistencies",
        help="detect graph annotation inconsistencies",
    )
    inconsistency.add_argument("--graph", default="artifacts/v1_graph.json")
    inconsistency.add_argument("--out", default="artifacts/v2_inconsistencies.json")
    inconsistency.set_defaults(func=cmd_detect_inconsistencies)

    mining = subparsers.add_parser(
        "mine-dark-hydrolases",
        help="run a bounded unreviewed hydrolase mining campaign",
    )
    mining.add_argument("--limit", type=int, default=100)
    mining.add_argument("--out", default="artifacts/v2_dark_hydrolase_candidates.json")
    mining.set_defaults(func=cmd_mine_dark_hydrolases)

    dossiers = subparsers.add_parser(
        "write-dossiers",
        help="write top candidate dossiers from a mining artifact",
    )
    dossiers.add_argument("--candidates", default="artifacts/v2_dark_hydrolase_candidates.json")
    dossiers.add_argument("--out-dir", default="artifacts/v2_dossiers")
    dossiers.add_argument("--top", type=int, default=10)
    dossiers.set_defaults(func=cmd_write_dossiers)

    v2_report = subparsers.add_parser("write-v2-report", help="write paper-style V2 report")
    v2_report.add_argument("--graph-summary", default="artifacts/v1_graph_summary.json")
    v2_report.add_argument("--benchmark", default="artifacts/v2_benchmark.json")
    v2_report.add_argument("--baseline", default="artifacts/v2_baseline.json")
    v2_report.add_argument("--inconsistencies", default="artifacts/v2_inconsistencies.json")
    v2_report.add_argument("--candidates", default="artifacts/v2_dark_hydrolase_candidates.json")
    v2_report.add_argument("--out", default="docs/v2_report.md")
    v2_report.set_defaults(func=cmd_write_v2_report)

    geometry = subparsers.add_parser(
        "build-geometry-features",
        help="compute active-site residue geometry from PDB mmCIF files",
    )
    geometry.add_argument("--graph", default="artifacts/v1_graph.json")
    geometry.add_argument("--max-entries", type=int, default=20)
    geometry.add_argument(
        "--reuse-existing",
        default=None,
        help="reuse matching entry rows from an existing geometry artifact",
    )
    geometry.add_argument(
        "--selected-pdb-overrides",
        default=None,
        help="apply a selected-PDB override plan with explicit residue positions",
    )
    geometry.add_argument("--out", default="artifacts/v3_geometry_features.json")
    geometry.set_defaults(func=cmd_build_geometry_features)

    geom_retrieval = subparsers.add_parser(
        "run-geometry-retrieval",
        help="rank seed mechanism fingerprints using active-site geometry features",
    )
    geom_retrieval.add_argument("--geometry", default="artifacts/v3_geometry_features.json")
    geom_retrieval.add_argument("--top-k", type=int, default=5)
    geom_retrieval.add_argument("--out", default="artifacts/v3_geometry_retrieval.json")
    geom_retrieval.set_defaults(func=cmd_run_geometry_retrieval)

    labels = subparsers.add_parser("label-summary", help="summarize curated mechanism labels")
    labels.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    labels.add_argument("--out", default="artifacts/v3_label_summary.json")
    labels.set_defaults(func=cmd_label_summary)

    migrate_labels = subparsers.add_parser(
        "migrate-label-registry",
        help="rewrite labels with explicit tier, review, and evidence fields",
    )
    migrate_labels.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    migrate_labels.add_argument("--out", default="data/registries/curated_mechanism_labels.json")
    migrate_labels.set_defaults(func=cmd_migrate_label_registry)

    countable_labels = subparsers.add_parser(
        "filter-countable-labels",
        help=(
            "write labels already eligible for benchmark counting; use "
            "import-countable-label-review for review-state batch imports"
        ),
    )
    countable_labels.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    countable_labels.add_argument("--out", default="artifacts/v3_countable_labels.json")
    countable_labels.add_argument(
        "--allow-pending-review",
        action="store_true",
        help="allow intentionally dropping pending/rejected review records",
    )
    countable_labels.set_defaults(func=cmd_filter_countable_labels)

    label_eval = subparsers.add_parser(
        "evaluate-geometry-labels",
        help="evaluate geometry-aware retrieval against curated mechanism labels",
    )
    label_eval.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    label_eval.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    label_eval.add_argument("--abstain-threshold", type=float, default=0.7)
    label_eval.add_argument("--out", default="artifacts/v3_geometry_label_eval.json")
    label_eval.set_defaults(func=cmd_evaluate_geometry_labels)

    calibration = subparsers.add_parser(
        "calibrate-abstention",
        help="sweep abstention thresholds for geometry label evaluation",
    )
    calibration.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    calibration.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    calibration.add_argument(
        "--thresholds",
        default="auto",
        help="comma-separated thresholds or 'auto' for score-boundary candidates",
    )
    calibration.add_argument("--out", default="artifacts/v3_abstention_calibration.json")
    calibration.set_defaults(func=cmd_calibrate_abstention)

    failures = subparsers.add_parser(
        "analyze-geometry-failures",
        help="categorize out-of-scope false non-abstentions by evidence pattern",
    )
    failures.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    failures.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    failures.add_argument("--abstain-threshold", type=float, default=0.75)
    failures.add_argument("--out", default="artifacts/v3_geometry_failure_analysis.json")
    failures.set_defaults(func=cmd_analyze_geometry_failures)

    in_scope_failures = subparsers.add_parser(
        "analyze-in-scope-failures",
        help="categorize in-scope positives that are misranked or abstained",
    )
    in_scope_failures.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    in_scope_failures.add_argument(
        "--labels", default="data/registries/curated_mechanism_labels.json"
    )
    in_scope_failures.add_argument("--abstain-threshold", type=float, default=0.7)
    in_scope_failures.add_argument("--out", default="artifacts/v3_in_scope_failure_analysis.json")
    in_scope_failures.set_defaults(func=cmd_analyze_in_scope_failures)

    cofactor_coverage = subparsers.add_parser(
        "analyze-cofactor-coverage",
        help="summarize expected cofactor coverage for in-scope mechanism labels",
    )
    cofactor_coverage.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    cofactor_coverage.add_argument(
        "--labels", default="data/registries/curated_mechanism_labels.json"
    )
    cofactor_coverage.add_argument("--abstain-threshold", type=float, default=0.7)
    cofactor_coverage.add_argument("--out", default="artifacts/v3_cofactor_coverage.json")
    cofactor_coverage.set_defaults(func=cmd_analyze_cofactor_coverage)

    cofactor_policy = subparsers.add_parser(
        "analyze-cofactor-policy",
        help="sweep cofactor-evidence score penalties against abstention guardrails",
    )
    cofactor_policy.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    cofactor_policy.add_argument(
        "--labels", default="data/registries/curated_mechanism_labels.json"
    )
    cofactor_policy.add_argument("--abstain-threshold", type=float, default=0.7)
    cofactor_policy.add_argument(
        "--absent-penalties",
        default="default",
        help="comma-separated penalties for missing expected structure-wide cofactors",
    )
    cofactor_policy.add_argument(
        "--structure-only-penalties",
        default="default",
        help="comma-separated penalties for expected cofactors outside the local site",
    )
    cofactor_policy.add_argument("--out", default="artifacts/v3_cofactor_policy.json")
    cofactor_policy.set_defaults(func=cmd_analyze_cofactor_policy)

    family_performance = subparsers.add_parser(
        "analyze-seed-family-performance",
        help="summarize retrieval quality by curated seed fingerprint family",
    )
    family_performance.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    family_performance.add_argument(
        "--labels", default="data/registries/curated_mechanism_labels.json"
    )
    family_performance.add_argument("--abstain-threshold", type=float, default=0.7)
    family_performance.add_argument(
        "--out",
        default="artifacts/v3_seed_family_performance.json",
    )
    family_performance.set_defaults(func=cmd_analyze_seed_family_performance)

    score_margins = subparsers.add_parser(
        "analyze-geometry-score-margins",
        help="analyze score overlap between in-scope positives and out-of-scope labels",
    )
    score_margins.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    score_margins.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    score_margins.add_argument("--near-margin", type=float, default=0.02)
    score_margins.add_argument("--out", default="artifacts/v3_geometry_score_margins.json")
    score_margins.set_defaults(func=cmd_analyze_geometry_score_margins)

    hard_negatives = subparsers.add_parser(
        "build-hard-negative-controls",
        help="select out-of-scope labels that overlap positive score ranges",
    )
    hard_negatives.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    hard_negatives.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    hard_negatives.add_argument("--score-floor", type=float, default=None)
    hard_negatives.add_argument("--near-margin", type=float, default=0.01)
    hard_negatives.add_argument("--out", default="artifacts/v3_hard_negative_controls.json")
    hard_negatives.set_defaults(func=cmd_build_hard_negative_controls)

    label_candidates = subparsers.add_parser(
        "build-label-expansion-candidates",
        help="rank unlabeled geometry entries for the next curated label pass",
    )
    label_candidates.add_argument("--geometry", default="artifacts/v3_geometry_features_40.json")
    label_candidates.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_40.json")
    label_candidates.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    label_candidates.add_argument("--out", default="artifacts/v3_label_expansion_candidates.json")
    label_candidates.set_defaults(func=cmd_build_label_expansion_candidates)

    label_factory = subparsers.add_parser(
        "build-label-factory-audit",
        help="apply deterministic label-tier promotion/demotion rules",
    )
    label_factory.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_475.json")
    label_factory.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    label_factory.add_argument("--abstain-threshold", type=float, default=0.4115)
    label_factory.add_argument("--hard-negatives", default=None)
    label_factory.add_argument("--adversarial-negatives", default=None)
    label_factory.add_argument("--out", default="artifacts/v3_label_factory_audit.json")
    label_factory.set_defaults(func=cmd_build_label_factory_audit)

    apply_factory = subparsers.add_parser(
        "apply-label-factory-actions",
        help="materialize label-factory promotions/review statuses into a registry artifact",
    )
    apply_factory.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    apply_factory.add_argument("--label-factory-audit", default="artifacts/v3_label_factory_audit_475.json")
    apply_factory.add_argument("--out", default="artifacts/v3_label_factory_applied_labels.json")
    apply_factory.set_defaults(func=cmd_apply_label_factory_actions)

    active_queue = subparsers.add_parser(
        "build-active-learning-queue",
        help="rank label candidates and weak labels for expert review",
    )
    active_queue.add_argument("--geometry", default="artifacts/v3_geometry_features_500.json")
    active_queue.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_500.json")
    active_queue.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    active_queue.add_argument("--label-factory-audit", default=None)
    active_queue.add_argument("--abstain-threshold", type=float, default=0.4115)
    active_queue.add_argument("--max-rows", type=int, default=100)
    active_queue.add_argument("--out", default="artifacts/v3_active_learning_review_queue.json")
    active_queue.set_defaults(func=cmd_build_active_learning_queue)

    adversarial_negatives = subparsers.add_parser(
        "build-adversarial-negatives",
        help="mine out-of-scope controls that stress label-factory guardrails",
    )
    adversarial_negatives.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_475.json")
    adversarial_negatives.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    adversarial_negatives.add_argument("--abstain-threshold", type=float, default=0.4115)
    adversarial_negatives.add_argument("--max-rows", type=int, default=100)
    adversarial_negatives.add_argument("--out", default="artifacts/v3_adversarial_negative_controls.json")
    adversarial_negatives.set_defaults(func=cmd_build_adversarial_negatives)

    review_export = subparsers.add_parser(
        "export-label-review",
        help="export active-learning queue rows for expert decision import",
    )
    review_export.add_argument("--queue", default="artifacts/v3_active_learning_review_queue.json")
    review_export.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    review_export.add_argument("--max-rows", type=int, default=25)
    review_export.add_argument("--out", default="artifacts/v3_expert_review_export.json")
    review_export.set_defaults(func=cmd_export_label_review)

    expert_label_decision_export = subparsers.add_parser(
        "build-expert-label-decision-review-export",
        help="export active-queue expert-label decision rows without countable decisions",
    )
    expert_label_decision_export.add_argument(
        "--active-learning-queue",
        default="artifacts/v3_active_learning_review_queue.json",
    )
    expert_label_decision_export.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    expert_label_decision_export.add_argument("--review-debt", default=None)
    expert_label_decision_export.add_argument(
        "--reaction-substrate-mismatch-review-export",
        default=None,
    )
    expert_label_decision_export.add_argument(
        "--out",
        default="artifacts/v3_expert_label_decision_review_export.json",
    )
    expert_label_decision_export.set_defaults(
        func=cmd_build_expert_label_decision_review_export
    )

    expert_label_decision_repair = subparsers.add_parser(
        "summarize-expert-label-decision-repair-candidates",
        help="prioritize review-only expert-label decision rows for evidence repair",
    )
    expert_label_decision_repair.add_argument(
        "--expert-label-decision-review-export",
        default="artifacts/v3_expert_label_decision_review_export.json",
    )
    expert_label_decision_repair.add_argument("--review-debt-remediation", default=None)
    expert_label_decision_repair.add_argument("--structure-mapping", default=None)
    expert_label_decision_repair.add_argument("--alternate-structure-scan", default=None)
    expert_label_decision_repair.add_argument("--max-rows", type=int, default=30)
    expert_label_decision_repair.add_argument(
        "--out",
        default="artifacts/v3_expert_label_decision_repair_candidates.json",
    )
    expert_label_decision_repair.set_defaults(
        func=cmd_summarize_expert_label_decision_repair_candidates
    )

    expert_label_decision_repair_guardrail = subparsers.add_parser(
        "audit-expert-label-decision-repair-guardrails",
        help="audit priority expert-label repair lanes as non-countable evidence work",
    )
    expert_label_decision_repair_guardrail.add_argument(
        "--expert-label-decision-repair-candidates",
        default="artifacts/v3_expert_label_decision_repair_candidates.json",
    )
    expert_label_decision_repair_guardrail.add_argument(
        "--remap-local-lead-audit",
        default=None,
    )
    expert_label_decision_repair_guardrail.add_argument(
        "--out",
        default="artifacts/v3_expert_label_decision_repair_guardrail_audit.json",
    )
    expert_label_decision_repair_guardrail.set_defaults(
        func=cmd_audit_expert_label_decision_repair_guardrails
    )

    expert_label_decision_local_gaps = subparsers.add_parser(
        "audit-expert-label-decision-local-evidence-gaps",
        help="classify local-evidence gaps in priority expert-label repair lanes",
    )
    expert_label_decision_local_gaps.add_argument(
        "--expert-label-decision-repair-guardrail-audit",
        default="artifacts/v3_expert_label_decision_repair_guardrail_audit.json",
    )
    expert_label_decision_local_gaps.add_argument(
        "--expert-label-decision-repair-candidates",
        default=None,
    )
    expert_label_decision_local_gaps.add_argument(
        "--out",
        default="artifacts/v3_expert_label_decision_local_evidence_gap_audit.json",
    )
    expert_label_decision_local_gaps.set_defaults(
        func=cmd_audit_expert_label_decision_local_evidence_gaps
    )

    expert_label_decision_local_export = subparsers.add_parser(
        "build-expert-label-decision-local-evidence-review-export",
        help="export priority expert-label local-evidence gaps for review",
    )
    expert_label_decision_local_export.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default="artifacts/v3_expert_label_decision_local_evidence_gap_audit.json",
    )
    expert_label_decision_local_export.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    expert_label_decision_local_export.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_expert_label_decision_local_evidence_review_export.json"
        ),
    )
    expert_label_decision_local_export.set_defaults(
        func=cmd_build_expert_label_decision_local_evidence_review_export
    )

    expert_label_decision_local_plan = subparsers.add_parser(
        "summarize-expert-label-decision-local-evidence-repair-plan",
        help="prioritize non-countable local-evidence repair lanes",
    )
    expert_label_decision_local_plan.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default="artifacts/v3_expert_label_decision_local_evidence_gap_audit.json",
    )
    expert_label_decision_local_plan.add_argument(
        "--expert-label-decision-local-evidence-review-export",
        default=None,
    )
    expert_label_decision_local_plan.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_expert_label_decision_local_evidence_repair_plan.json"
        ),
    )
    expert_label_decision_local_plan.set_defaults(
        func=cmd_summarize_expert_label_decision_local_evidence_repair_plan
    )

    expert_label_decision_local_resolution = subparsers.add_parser(
        "resolve-expert-label-decision-local-evidence-repair-lanes",
        help=(
            "resolve non-countable local-evidence repair lanes with external "
            "reaction/substrate decisions"
        ),
    )
    expert_label_decision_local_resolution.add_argument(
        "--expert-label-decision-local-evidence-repair-plan",
        default=(
            "artifacts/"
            "v3_expert_label_decision_local_evidence_repair_plan.json"
        ),
    )
    expert_label_decision_local_resolution.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default=None,
    )
    expert_label_decision_local_resolution.add_argument(
        "--expert-label-decision-local-evidence-review-export",
        default=None,
    )
    expert_label_decision_local_resolution.add_argument(
        "--reaction-substrate-mismatch-review-export",
        default=None,
    )
    expert_label_decision_local_resolution.add_argument(
        "--reaction-substrate-mismatch-decision-batch",
        default=None,
    )
    expert_label_decision_local_resolution.add_argument("--entry-ids", default=None)
    expert_label_decision_local_resolution.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_expert_label_decision_local_evidence_repair_resolution.json"
        ),
    )
    expert_label_decision_local_resolution.set_defaults(
        func=cmd_resolve_expert_label_decision_local_evidence_repair_lanes
    )

    alternate_residue_requests = subparsers.add_parser(
        "build-explicit-alternate-residue-position-requests",
        help="build non-countable requests for alternate-PDB residue positions",
    )
    alternate_residue_requests.add_argument(
        "--expert-label-decision-local-evidence-repair-plan",
        default=(
            "artifacts/"
            "v3_expert_label_decision_local_evidence_repair_plan.json"
        ),
    )
    alternate_residue_requests.add_argument(
        "--review-debt-remediation",
        default=None,
    )
    alternate_residue_requests.add_argument("--graph", default=None)
    alternate_residue_requests.add_argument(
        "--out",
        default=(
            "artifacts/"
            "v3_explicit_alternate_residue_position_requests.json"
        ),
    )
    alternate_residue_requests.set_defaults(
        func=cmd_build_explicit_alternate_residue_position_requests
    )

    review_debt_deferrals = subparsers.add_parser(
        "audit-accepted-review-debt-deferrals",
        help="confirm accepted-batch review-debt rows remain explicitly non-countable",
    )
    review_debt_deferrals.add_argument(
        "--review-debt",
        default="artifacts/v3_review_debt_summary_preview.json",
    )
    review_debt_deferrals.add_argument(
        "--acceptance",
        default="artifacts/v3_label_batch_acceptance_check.json",
    )
    review_debt_deferrals.add_argument("--scaling-quality-audit", default=None)
    review_debt_deferrals.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default=None,
    )
    review_debt_deferrals.add_argument(
        "--expert-label-decision-local-evidence-review-export",
        default=None,
    )
    review_debt_deferrals.add_argument(
        "--expert-label-decision-local-evidence-repair-plan",
        default=None,
    )
    review_debt_deferrals.add_argument(
        "--expert-label-decision-local-evidence-repair-resolution",
        default=None,
    )
    review_debt_deferrals.add_argument(
        "--explicit-alternate-residue-position-requests",
        default=None,
    )
    review_debt_deferrals.add_argument("--remap-local-lead-audit", default=None)
    review_debt_deferrals.add_argument(
        "--review-only-import-safety-audit",
        default=None,
    )
    review_debt_deferrals.add_argument(
        "--out",
        default="artifacts/v3_accepted_review_debt_deferral_audit.json",
    )
    review_debt_deferrals.set_defaults(
        func=cmd_audit_accepted_review_debt_deferrals
    )

    ontology_gap_audit = subparsers.add_parser(
        "audit-mechanism-ontology-gaps",
        help="summarize review-only mechanism scope pressure beyond current ontology",
    )
    ontology_gap_audit.add_argument(
        "--active-learning-queue",
        default="artifacts/v3_active_learning_review_queue.json",
    )
    ontology_gap_audit.add_argument(
        "--expert-label-decision-repair-candidates",
        default=None,
    )
    ontology_gap_audit.add_argument(
        "--family-propagation-guardrails",
        default=None,
    )
    ontology_gap_audit.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default=None,
    )
    ontology_gap_audit.add_argument("--max-rows", type=int, default=60)
    ontology_gap_audit.add_argument(
        "--out",
        default="artifacts/v3_mechanism_ontology_gap_audit.json",
    )
    ontology_gap_audit.set_defaults(func=cmd_audit_mechanism_ontology_gaps)

    atp_family_expansion = subparsers.add_parser(
        "build-atp-phosphoryl-transfer-family-expansion",
        help="map expert-reviewed ATP/phosphoryl-transfer mismatch lanes to ontology families",
    )
    atp_family_expansion.add_argument(
        "--reaction-substrate-mismatch-decision-batch",
        default="artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json",
    )
    atp_family_expansion.add_argument(
        "--reaction-substrate-mismatch-review-export",
        default=None,
    )
    atp_family_expansion.add_argument("--family-propagation-guardrails", default=None)
    atp_family_expansion.add_argument("--active-learning-queue", default=None)
    atp_family_expansion.add_argument("--adversarial-negatives", default=None)
    atp_family_expansion.add_argument(
        "--out",
        default="artifacts/v3_atp_phosphoryl_transfer_family_expansion.json",
    )
    atp_family_expansion.set_defaults(
        func=cmd_build_atp_phosphoryl_transfer_family_expansion
    )

    learned_retrieval_manifest = subparsers.add_parser(
        "build-learned-retrieval-manifest",
        help="build a representation-learning interface with heuristic controls",
    )
    learned_retrieval_manifest.add_argument(
        "--geometry",
        default="artifacts/v3_geometry_features_700.json",
    )
    learned_retrieval_manifest.add_argument(
        "--retrieval",
        default="artifacts/v3_geometry_retrieval_700.json",
    )
    learned_retrieval_manifest.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    learned_retrieval_manifest.add_argument("--ontology-gap-audit", default=None)
    learned_retrieval_manifest.add_argument("--max-rows", type=int, default=120)
    learned_retrieval_manifest.add_argument(
        "--out",
        default="artifacts/v3_learned_retrieval_manifest.json",
    )
    learned_retrieval_manifest.set_defaults(
        func=cmd_build_learned_retrieval_manifest
    )

    sequence_failure_audit = subparsers.add_parser(
        "audit-sequence-similarity-failure-sets",
        help="prepare exact-reference sequence-cluster controls for propagation audits",
    )
    sequence_failure_audit.add_argument(
        "--sequence-clusters",
        default="artifacts/v3_sequence_cluster_proxy_700.json",
    )
    sequence_failure_audit.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    sequence_failure_audit.add_argument("--active-learning-queue", default=None)
    sequence_failure_audit.add_argument(
        "--out",
        default="artifacts/v3_sequence_similarity_failure_sets.json",
    )
    sequence_failure_audit.set_defaults(
        func=cmd_audit_sequence_similarity_failure_sets
    )

    review_import = subparsers.add_parser(
        "import-label-review",
        help="apply expert review decisions to a label registry copy",
    )
    review_import.add_argument("--review", default="artifacts/v3_expert_review_export.json")
    review_import.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    review_import.add_argument("--out", default="artifacts/v3_imported_labels.json")
    review_import.set_defaults(func=cmd_import_label_review)

    countable_review_import = subparsers.add_parser(
        "import-countable-label-review",
        help="apply only accepted countable review decisions to a label registry copy",
    )
    countable_review_import.add_argument("--review", default="artifacts/v3_expert_review_export.json")
    countable_review_import.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    countable_review_import.add_argument("--out", default="artifacts/v3_countable_imported_labels.json")
    countable_review_import.set_defaults(func=cmd_import_countable_label_review)

    review_only_import_safety = subparsers.add_parser(
        "audit-review-only-import-safety",
        help="verify review-only decision artifacts do not add countable labels",
    )
    review_only_import_safety.add_argument(
        "--review",
        action="append",
        required=True,
        help="review or decision artifact to audit; repeatable",
    )
    review_only_import_safety.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    review_only_import_safety.add_argument(
        "--out",
        default="artifacts/v3_review_only_import_safety_audit.json",
    )
    review_only_import_safety.set_defaults(
        func=cmd_audit_review_only_import_safety
    )

    decision_batch = subparsers.add_parser(
        "build-review-decision-batch",
        help="fill an expert-review export copy with provisional label-factory decisions",
    )
    decision_batch.add_argument("--review", default="artifacts/v3_expert_review_export.json")
    decision_batch.add_argument("--batch-id", default="provisional_batch")
    decision_batch.add_argument("--reviewer", default="automation_label_factory")
    decision_batch.add_argument("--max-boundary-controls", type=int, default=5)
    decision_batch.add_argument(
        "--entry-id",
        action="append",
        default=[],
        help="limit the generated decision batch to a specific review entry; repeatable",
    )
    decision_batch.add_argument("--out", default="artifacts/v3_review_decision_batch.json")
    decision_batch.set_defaults(func=cmd_build_review_decision_batch)

    gate_check = subparsers.add_parser(
        "check-label-factory-gates",
        help="verify label-factory artifacts before the next label batch",
    )
    gate_check.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    gate_check.add_argument("--label-factory-audit", default="artifacts/v3_label_factory_audit_500.json")
    gate_check.add_argument("--applied-label-factory", default="artifacts/v3_label_factory_applied_labels_500.json")
    gate_check.add_argument("--active-learning-queue", default="artifacts/v3_active_learning_review_queue_500.json")
    gate_check.add_argument("--adversarial-negatives", default="artifacts/v3_adversarial_negative_controls_500.json")
    gate_check.add_argument("--expert-review-export", default="artifacts/v3_expert_review_export_500.json")
    gate_check.add_argument("--family-propagation-guardrails", default="artifacts/v3_family_propagation_guardrails_500.json")
    gate_check.add_argument("--reaction-substrate-mismatch-review-export", default=None)
    gate_check.add_argument("--expert-label-decision-review-export", default=None)
    gate_check.add_argument("--expert-label-decision-repair-candidates", default=None)
    gate_check.add_argument("--expert-label-decision-repair-guardrail-audit", default=None)
    gate_check.add_argument("--expert-label-decision-local-evidence-gap-audit", default=None)
    gate_check.add_argument("--expert-label-decision-local-evidence-review-export", default=None)
    gate_check.add_argument("--expert-label-decision-local-evidence-repair-resolution", default=None)
    gate_check.add_argument("--explicit-alternate-residue-position-requests", default=None)
    gate_check.add_argument("--review-only-import-safety-audit", default=None)
    gate_check.add_argument("--atp-phosphoryl-transfer-family-expansion", default=None)
    gate_check.add_argument("--accepted-review-debt-deferral-audit", default=None)
    gate_check.add_argument("--out", default="artifacts/v3_label_factory_gate_check.json")
    gate_check.set_defaults(func=cmd_check_label_factory_gates)

    batch_acceptance = subparsers.add_parser(
        "check-label-batch-acceptance",
        help="verify an accepted label-review batch before benchmark counting",
    )
    batch_acceptance.add_argument("--baseline-labels", default="data/registries/curated_mechanism_labels.json")
    batch_acceptance.add_argument("--baseline-label-count", type=int, default=None)
    batch_acceptance.add_argument("--review-state-labels", default="artifacts/v3_imported_labels_batch.json")
    batch_acceptance.add_argument("--countable-labels", default="artifacts/v3_countable_labels_batch.json")
    batch_acceptance.add_argument("--evaluation", default="artifacts/v3_geometry_label_eval_batch.json")
    batch_acceptance.add_argument("--hard-negatives", default="artifacts/v3_hard_negative_controls_batch.json")
    batch_acceptance.add_argument("--in-scope-failures", default="artifacts/v3_in_scope_failure_analysis_batch.json")
    batch_acceptance.add_argument("--label-factory-gate", default="artifacts/v3_label_factory_gate_check_batch.json")
    batch_acceptance.add_argument("--review-evidence-gaps", default=None)
    batch_acceptance.add_argument("--out", default="artifacts/v3_label_batch_acceptance_check.json")
    batch_acceptance.set_defaults(func=cmd_check_label_batch_acceptance)

    batch_summary = subparsers.add_parser(
        "summarize-label-factory-batches",
        help="summarize accepted label-factory batches and scaling guardrails",
    )
    batch_summary.add_argument(
        "--acceptance",
        action="append",
        required=True,
        help="label batch acceptance artifact; repeat for each batch",
    )
    batch_summary.add_argument(
        "--gate",
        action="append",
        default=[],
        help="label factory gate artifact; repeat for matching batches",
    )
    batch_summary.add_argument(
        "--active-learning-queue",
        action="append",
        default=[],
        help="active-learning queue artifact; repeat for matching batches",
    )
    batch_summary.add_argument(
        "--scaling-quality-audit",
        action="append",
        default=[],
        help="scaling-quality audit artifact; repeat for matching preview batches",
    )
    batch_summary.add_argument("--out", default="artifacts/v3_label_factory_batch_summary.json")
    batch_summary.set_defaults(func=cmd_summarize_label_factory_batches)

    review_resolution = subparsers.add_parser(
        "check-label-review-resolution",
        help="verify that remaining review candidates were accepted, rejected, or deferred",
    )
    review_resolution.add_argument("--baseline-labels", default="data/registries/curated_mechanism_labels.json")
    review_resolution.add_argument("--baseline-label-count", type=int, default=None)
    review_resolution.add_argument("--review", default="artifacts/v3_review_decision_batch.json")
    review_resolution.add_argument("--review-state-labels", default="artifacts/v3_imported_labels_batch.json")
    review_resolution.add_argument("--countable-labels", default="artifacts/v3_countable_labels_batch.json")
    review_resolution.add_argument("--label-expansion-candidates", default="artifacts/v3_label_expansion_candidates_500.json")
    review_resolution.add_argument("--label-factory-gate", default="artifacts/v3_label_factory_gate_check_500.json")
    review_resolution.add_argument("--out", default="artifacts/v3_label_review_resolution_check.json")
    review_resolution.set_defaults(func=cmd_check_label_review_resolution)

    review_gaps = subparsers.add_parser(
        "analyze-review-evidence-gaps",
        help="audit accepted or deferred review decisions against retrieval evidence gaps",
    )
    review_gaps.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_500.json")
    review_gaps.add_argument("--review", default="artifacts/v3_review_decision_batch.json")
    review_gaps.add_argument("--out", default="artifacts/v3_review_evidence_gaps.json")
    review_gaps.set_defaults(func=cmd_analyze_review_evidence_gaps)

    review_debt = subparsers.add_parser(
        "summarize-review-debt",
        help="prioritize pending review evidence gaps for the next label-factory pass",
    )
    review_debt.add_argument(
        "--review-evidence-gaps",
        default="artifacts/v3_review_evidence_gaps.json",
    )
    review_debt.add_argument("--active-learning-queue", default=None)
    review_debt.add_argument("--baseline-review-debt", default=None)
    review_debt.add_argument("--max-rows", type=int, default=25)
    review_debt.add_argument("--out", default="artifacts/v3_review_debt_summary.json")
    review_debt.set_defaults(func=cmd_summarize_review_debt)

    review_debt_remediation = subparsers.add_parser(
        "analyze-review-debt-remediation",
        help="plan concrete remediation checks for pending review-debt rows",
    )
    review_debt_remediation.add_argument(
        "--review-debt",
        default="artifacts/v3_review_debt_summary.json",
    )
    review_debt_remediation.add_argument(
        "--review-evidence-gaps",
        default="artifacts/v3_review_evidence_gaps.json",
    )
    review_debt_remediation.add_argument("--graph", default=None)
    review_debt_remediation.add_argument("--geometry", default=None)
    review_debt_remediation.add_argument(
        "--debt-status",
        choices=["new", "carried", "all"],
        default="new",
    )
    review_debt_remediation.add_argument(
        "--max-rows",
        type=int,
        default=0,
        help="optional row cap; 0 emits all requested debt rows",
    )
    review_debt_remediation.add_argument(
        "--out",
        default="artifacts/v3_review_debt_remediation.json",
    )
    review_debt_remediation.set_defaults(func=cmd_analyze_review_debt_remediation)

    alternate_scan = subparsers.add_parser(
        "scan-review-debt-alternate-structures",
        help="scan bounded alternate PDB structures for review-debt cofactor evidence",
    )
    alternate_scan.add_argument(
        "--remediation",
        default="artifacts/v3_review_debt_remediation.json",
    )
    alternate_scan.add_argument("--max-entries", type=int, default=5)
    alternate_scan.add_argument("--max-structures-per-entry", type=int, default=6)
    alternate_scan.add_argument(
        "--out",
        default="artifacts/v3_review_debt_alternate_structure_scan.json",
    )
    alternate_scan.set_defaults(func=cmd_scan_review_debt_alternate_structures)

    remap_leads = subparsers.add_parser(
        "summarize-review-debt-remap-leads",
        help="summarize review-only alternate-structure remap leads",
    )
    remap_leads.add_argument(
        "--alternate-structure-scan",
        default="artifacts/v3_review_debt_alternate_structure_scan.json",
    )
    remap_leads.add_argument("--remediation", default=None)
    remap_leads.add_argument("--review-evidence-gaps", default=None)
    remap_leads.add_argument(
        "--out",
        default="artifacts/v3_review_debt_remap_leads.json",
    )
    remap_leads.set_defaults(func=cmd_summarize_review_debt_remap_leads)

    remap_local_audit = subparsers.add_parser(
        "audit-review-debt-remap-local-leads",
        help="audit remap-local review-debt leads before review import",
    )
    remap_local_audit.add_argument(
        "--remap-leads",
        default="artifacts/v3_review_debt_remap_leads.json",
    )
    remap_local_audit.add_argument("--remediation", default=None)
    remap_local_audit.add_argument("--review-evidence-gaps", default=None)
    remap_local_audit.add_argument(
        "--out",
        default="artifacts/v3_review_debt_remap_local_lead_audit.json",
    )
    remap_local_audit.set_defaults(func=cmd_audit_review_debt_remap_local_leads)

    holo_preference = subparsers.add_parser(
        "audit-structure-selection-holo-preference",
        help=(
            "recommend reselecting the canonical reference PDB when the "
            "selected structure is apo for the expected cofactor family while "
            "a holo alternate exists"
        ),
    )
    holo_preference.add_argument(
        "--alternate-structure-scan",
        default="artifacts/v3_review_debt_alternate_structure_scan.json",
    )
    holo_preference.add_argument(
        "--min-usable-residue-positions",
        type=int,
        default=1,
        help="minimum usable residue positions required on the recommended PDB",
    )
    holo_preference.add_argument(
        "--prefer-mcsa-explicit-over-remap",
        dest="prefer_mcsa_explicit_over_remap",
        action="store_true",
        default=True,
        help="prefer alternates with mcsa_explicit residue positions over remapped ones (default)",
    )
    holo_preference.add_argument(
        "--no-prefer-mcsa-explicit-over-remap",
        dest="prefer_mcsa_explicit_over_remap",
        action="store_false",
        help="treat mcsa_explicit and remap-sourced positions equally",
    )
    holo_preference.add_argument(
        "--out",
        default="artifacts/v3_structure_selection_holo_preference_audit.json",
    )
    holo_preference.set_defaults(func=cmd_audit_structure_selection_holo_preference)

    selected_pdb_overrides = subparsers.add_parser(
        "build-selected-pdb-overrides",
        help="build a provenance-bearing selected-PDB override plan",
    )
    selected_pdb_overrides.add_argument(
        "--holo-preference-audit",
        default="artifacts/v3_structure_selection_holo_preference_audit_700.json",
    )
    selected_pdb_overrides.add_argument(
        "--remediation",
        default="artifacts/v3_review_debt_remediation_700_all.json",
    )
    selected_pdb_overrides.add_argument(
        "--entry-ids",
        default=None,
        help="comma-separated entry ids to apply from the holo-preference audit",
    )
    selected_pdb_overrides.add_argument(
        "--skip-entry-ids",
        default=None,
        help="comma-separated entry ids to preserve as skipped policy cases",
    )
    selected_pdb_overrides.add_argument(
        "--out",
        default="artifacts/v3_selected_pdb_override_plan.json",
    )
    selected_pdb_overrides.set_defaults(func=cmd_build_selected_pdb_overrides)

    structure_selection = subparsers.add_parser(
        "summarize-review-debt-structure-selection-candidates",
        help="summarize review-only local structure-selection candidates",
    )
    structure_selection.add_argument(
        "--remap-local-lead-audit",
        default="artifacts/v3_review_debt_remap_local_lead_audit.json",
    )
    structure_selection.add_argument(
        "--alternate-structure-scan",
        default="artifacts/v3_review_debt_alternate_structure_scan.json",
    )
    structure_selection.add_argument("--remediation", default=None)
    structure_selection.add_argument(
        "--out",
        default="artifacts/v3_review_debt_structure_selection_candidates.json",
    )
    structure_selection.set_defaults(
        func=cmd_summarize_review_debt_structure_selection_candidates
    )

    reaction_mismatch = subparsers.add_parser(
        "audit-reaction-substrate-mismatches",
        help="triage text-level reaction/substrate mismatch risks",
    )
    reaction_mismatch.add_argument("--review-evidence-gaps", default=None)
    reaction_mismatch.add_argument("--active-learning-queue", default=None)
    reaction_mismatch.add_argument(
        "--out",
        default="artifacts/v3_reaction_substrate_mismatch_audit.json",
    )
    reaction_mismatch.set_defaults(func=cmd_audit_reaction_substrate_mismatches)

    reaction_mismatch_export = subparsers.add_parser(
        "build-reaction-substrate-mismatch-review-export",
        help="export all reaction/substrate mismatch lanes for expert review",
    )
    reaction_mismatch_export.add_argument(
        "--reaction-substrate-mismatch-audit",
        default="artifacts/v3_reaction_substrate_mismatch_audit.json",
    )
    reaction_mismatch_export.add_argument(
        "--family-propagation-guardrails",
        default="artifacts/v3_family_propagation_guardrails.json",
    )
    reaction_mismatch_export.add_argument(
        "--labels",
        default="data/registries/curated_mechanism_labels.json",
    )
    reaction_mismatch_export.add_argument(
        "--out",
        default="artifacts/v3_reaction_substrate_mismatch_review_export.json",
    )
    reaction_mismatch_export.set_defaults(
        func=cmd_build_reaction_substrate_mismatch_review_export
    )

    preview_promotion = subparsers.add_parser(
        "check-label-preview-promotion",
        help="separate mechanical preview acceptance from promotion readiness",
    )
    preview_promotion.add_argument(
        "--preview-acceptance",
        default="artifacts/v3_label_batch_acceptance_check_preview.json",
    )
    preview_promotion.add_argument(
        "--preview-summary",
        default="artifacts/v3_label_factory_preview_summary.json",
    )
    preview_promotion.add_argument(
        "--preview-review-debt",
        default="artifacts/v3_review_debt_summary_preview.json",
    )
    preview_promotion.add_argument("--current-review-debt", default=None)
    preview_promotion.add_argument(
        "--out",
        default="artifacts/v3_label_preview_promotion_readiness.json",
    )
    preview_promotion.set_defaults(func=cmd_check_label_preview_promotion)

    scaling_quality = subparsers.add_parser(
        "audit-label-scaling-quality",
        help="classify preview scaling failure modes before label promotion",
    )
    scaling_quality.add_argument("--batch-id", default=None)
    scaling_quality.add_argument(
        "--acceptance",
        default="artifacts/v3_label_batch_acceptance_check_preview.json",
    )
    scaling_quality.add_argument(
        "--readiness",
        default="artifacts/v3_label_preview_promotion_readiness.json",
    )
    scaling_quality.add_argument(
        "--review-debt",
        default="artifacts/v3_review_debt_summary_preview.json",
    )
    scaling_quality.add_argument(
        "--review-evidence-gaps",
        default="artifacts/v3_review_evidence_gaps_preview.json",
    )
    scaling_quality.add_argument(
        "--active-learning-queue",
        default="artifacts/v3_active_learning_review_queue_preview.json",
    )
    scaling_quality.add_argument(
        "--family-propagation-guardrails",
        default="artifacts/v3_family_propagation_guardrails_preview.json",
    )
    scaling_quality.add_argument(
        "--hard-negatives",
        default="artifacts/v3_hard_negative_controls_preview.json",
    )
    scaling_quality.add_argument("--decision-batch", default=None)
    scaling_quality.add_argument("--structure-mapping", default=None)
    scaling_quality.add_argument("--expert-review-export", default=None)
    scaling_quality.add_argument("--sequence-clusters", default=None)
    scaling_quality.add_argument("--alternate-structure-scan", default=None)
    scaling_quality.add_argument("--remap-local-lead-audit", default=None)
    scaling_quality.add_argument("--reaction-substrate-mismatch-audit", default=None)
    scaling_quality.add_argument(
        "--reaction-substrate-mismatch-review-export",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-review-export",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-repair-candidates",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-repair-guardrail-audit",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-local-evidence-gap-audit",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-local-evidence-review-export",
        default=None,
    )
    scaling_quality.add_argument(
        "--expert-label-decision-local-evidence-repair-resolution",
        default=None,
    )
    scaling_quality.add_argument(
        "--explicit-alternate-residue-position-requests",
        default=None,
    )
    scaling_quality.add_argument("--review-only-import-safety-audit", default=None)
    scaling_quality.add_argument("--atp-phosphoryl-transfer-family-expansion", default=None)
    scaling_quality.add_argument(
        "--out",
        default="artifacts/v3_label_scaling_quality_audit.json",
    )
    scaling_quality.set_defaults(func=cmd_audit_label_scaling_quality)

    family_guardrails = subparsers.add_parser(
        "build-family-propagation-guardrails",
        help="audit ontology-family propagation blockers and local proxy evidence",
    )
    family_guardrails.add_argument("--geometry", default="artifacts/v3_geometry_features_500.json")
    family_guardrails.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval_500.json")
    family_guardrails.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    family_guardrails.add_argument("--max-rows", type=int, default=200)
    family_guardrails.add_argument("--out", default="artifacts/v3_family_propagation_guardrails.json")
    family_guardrails.set_defaults(func=cmd_build_family_propagation_guardrails)

    mapping_issues = subparsers.add_parser(
        "analyze-structure-mapping-issues",
        help="summarize non-OK geometry entries and missing residue mappings",
    )
    mapping_issues.add_argument("--geometry", default="artifacts/v3_geometry_features_40.json")
    mapping_issues.add_argument("--labels", default="data/registries/curated_mechanism_labels.json")
    mapping_issues.add_argument("--out", default="artifacts/v3_structure_mapping_issues_40.json")
    mapping_issues.set_defaults(func=cmd_analyze_structure_mapping_issues)

    perf = subparsers.add_parser(
        "perf-suite",
        help="run local artifact performance checks",
    )
    perf.add_argument("--graph", default="artifacts/v1_graph.json")
    perf.add_argument("--geometry", default="artifacts/v3_geometry_features.json")
    perf.add_argument("--retrieval", default="artifacts/v3_geometry_retrieval.json")
    perf.add_argument("--iterations", type=int, default=5)
    perf.add_argument("--out", default="artifacts/perf_report.json")
    perf.set_defaults(func=cmd_perf_suite)

    slice_summary = subparsers.add_parser(
        "summarize-geometry-slices",
        help="summarize geometry evaluation, margin, and control artifacts across slices",
    )
    slice_summary.add_argument("--artifact-dir", default="artifacts")
    slice_summary.add_argument("--out", default="artifacts/v3_geometry_slice_summary.json")
    slice_summary.set_defaults(func=cmd_summarize_geometry_slices)

    log_work = subparsers.add_parser("log-work", help="append a timed work entry")
    log_work.add_argument("--stage", required=True, help="milestone stage, for example v0 or v1")
    log_work.add_argument("--task", required=True)
    log_work.add_argument("--minutes", type=int, required=True)
    log_work.add_argument(
        "--time-mode",
        choices=["estimate", "measured", "corrected"],
        default="estimate",
    )
    log_work.add_argument("--started-at", default=None, help="ISO timestamp for measured work start")
    log_work.add_argument("--ended-at", default=None, help="ISO timestamp for measured work end")
    log_work.add_argument("--measured-minutes", type=float, default=None)
    log_work.add_argument("--artifacts", default="", help="comma-separated artifact references")
    log_work.add_argument("--evidence", default="", help="comma-separated evidence references")
    log_work.add_argument("--scope-adjustment", default=None)
    log_work.add_argument("--expectation-update", default=None)
    log_work.add_argument("--commit", default=None)
    log_work.add_argument("--notes", default=None)
    log_work.add_argument("--log", default="work/progress_log.jsonl")
    log_work.set_defaults(func=cmd_log_work)

    progress = subparsers.add_parser("progress-report", help="generate work/status.md")
    progress.add_argument("--log", default="work/progress_log.jsonl")
    progress.add_argument("--out", default="work/status.md")
    progress.set_defaults(func=cmd_progress_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except RegistryError as exc:
        parser.exit(2, f"registry error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
