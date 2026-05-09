from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import fetch_mcsa_sample, fetch_rhea_sample
from .fingerprints import build_mechanism_demo, load_fingerprints
from .graph import build_seed_graph, build_v1_graph, summarize_graph
from .models import RegistryError
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
    print(f"Validated {len(sources)} source records")
    print(f"Validated {len(fingerprints)} mechanism fingerprints")
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

    log_work = subparsers.add_parser("log-work", help="append a timed work entry")
    log_work.add_argument("--stage", required=True, help="milestone stage, for example v0 or v1")
    log_work.add_argument("--task", required=True)
    log_work.add_argument("--minutes", type=int, required=True)
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
