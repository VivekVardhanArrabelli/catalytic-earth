from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .adapters import fetch_mcsa_sample, fetch_rhea_sample
from .automation import acquire_automation_lock, inspect_automation_lock, release_automation_lock
from .fingerprints import build_mechanism_demo, load_fingerprints
from .graph import build_seed_graph, build_v1_graph, summarize_graph
from .geometry_retrieval import write_geometry_retrieval
from .geometry_reports import write_geometry_slice_summary
from .labels import (
    analyze_cofactor_abstention_policy,
    analyze_cofactor_coverage,
    analyze_geometry_score_margins,
    analyze_in_scope_failures,
    analyze_seed_family_performance,
    analyze_out_of_scope_failures,
    analyze_review_evidence_gaps,
    analyze_structure_mapping_issues,
    build_active_learning_review_queue,
    build_adversarial_negative_controls,
    build_expert_review_export,
    build_family_propagation_guardrails,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    build_label_factory_audit,
    build_provisional_review_decision_batch,
    check_label_batch_acceptance,
    check_label_factory_gates,
    check_label_preview_promotion_readiness,
    check_label_review_resolution,
    countable_benchmark_labels,
    evaluate_geometry_retrieval,
    apply_label_factory_actions,
    import_expert_review_decisions,
    import_countable_review_decisions,
    label_summary,
    load_labels,
    migrate_label_registry_records,
    summarize_label_factory_batches,
    summarize_review_debt,
    sweep_abstention_thresholds,
)
from .ontology import load_mechanism_ontology
from .models import RegistryError
from .performance import write_local_performance_suite
from .progress import WorkEntry, append_work_entry, write_progress_report
from .sources import build_source_ledger, load_sources
from .structure import write_geometry_features
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


def cmd_check_label_factory_gates(args: argparse.Namespace) -> int:
    with Path(args.label_factory_audit).open("r", encoding="utf-8") as handle:
        factory = json.load(handle)
    with Path(args.applied_label_factory).open("r", encoding="utf-8") as handle:
        applied = json.load(handle)
    with Path(args.active_learning_queue).open("r", encoding="utf-8") as handle:
        queue = json.load(handle)
    with Path(args.adversarial_negatives).open("r", encoding="utf-8") as handle:
        adversarial = json.load(handle)
    with Path(args.expert_review_export).open("r", encoding="utf-8") as handle:
        review_export = json.load(handle)
    with Path(args.family_propagation_guardrails).open("r", encoding="utf-8") as handle:
        family_guardrails = json.load(handle)
    gates = check_label_factory_gates(
        load_labels(Path(args.labels)),
        factory,
        applied,
        queue,
        adversarial,
        review_export,
        family_propagation_guardrails=family_guardrails,
    )
    write_json(Path(args.out), gates)
    print(
        "Wrote label factory gate check to "
        f"{args.out} (ready={gates['metadata']['automation_ready_for_next_label_batch']})"
    )
    return 0


def cmd_check_label_batch_acceptance(args: argparse.Namespace) -> int:
    with Path(args.evaluation).open("r", encoding="utf-8") as handle:
        evaluation = json.load(handle)
    with Path(args.hard_negatives).open("r", encoding="utf-8") as handle:
        hard_negatives = json.load(handle)
    with Path(args.in_scope_failures).open("r", encoding="utf-8") as handle:
        in_scope_failures = json.load(handle)
    with Path(args.label_factory_gate).open("r", encoding="utf-8") as handle:
        label_factory_gate = json.load(handle)
    check = check_label_batch_acceptance(
        baseline_labels=load_labels(Path(args.baseline_labels)),
        review_state_labels=load_labels(Path(args.review_state_labels)),
        countable_labels=load_labels(Path(args.countable_labels)),
        evaluation=evaluation,
        hard_negatives=hard_negatives,
        in_scope_failures=in_scope_failures,
        label_factory_gate=label_factory_gate,
        baseline_label_count=args.baseline_label_count,
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


def cmd_summarize_label_factory_batches(args: argparse.Namespace) -> int:
    summary = summarize_label_factory_batches(
        _load_named_json_artifacts(args.acceptance),
        gate_checks=_load_named_json_artifacts(args.gate),
        active_learning_queues=_load_named_json_artifacts(args.active_learning_queue),
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
    gate_check.add_argument("--label-factory-audit", default="artifacts/v3_label_factory_audit_475.json")
    gate_check.add_argument("--applied-label-factory", default="artifacts/v3_label_factory_applied_labels_475.json")
    gate_check.add_argument("--active-learning-queue", default="artifacts/v3_active_learning_review_queue_500.json")
    gate_check.add_argument("--adversarial-negatives", default="artifacts/v3_adversarial_negative_controls_475.json")
    gate_check.add_argument("--expert-review-export", default="artifacts/v3_expert_review_export_500.json")
    gate_check.add_argument("--family-propagation-guardrails", default="artifacts/v3_family_propagation_guardrails_500.json")
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
