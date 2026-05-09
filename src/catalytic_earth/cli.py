from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import fetch_mcsa_sample, fetch_rhea_sample
from .fingerprints import build_mechanism_demo, load_fingerprints
from .graph import build_seed_graph, build_v1_graph, summarize_graph
from .geometry_retrieval import write_geometry_retrieval
from .labels import (
    analyze_geometry_score_margins,
    analyze_out_of_scope_failures,
    analyze_structure_mapping_issues,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    evaluate_geometry_retrieval,
    label_summary,
    load_labels,
    sweep_abstention_thresholds,
)
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


def cmd_validate(_: argparse.Namespace) -> int:
    sources = load_sources()
    fingerprints = load_fingerprints()
    labels = load_labels()
    print(f"Validated {len(sources)} source records")
    print(f"Validated {len(fingerprints)} mechanism fingerprints")
    print(f"Validated {len(labels)} curated mechanism labels")
    return 0


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
        f"{args.out} ({controls['metadata']['hard_negative_count']} controls)"
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


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


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
