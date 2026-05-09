from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import fetch_mcsa_sample, fetch_rhea_sample
from .fingerprints import build_mechanism_demo, load_fingerprints
from .graph import build_seed_graph
from .models import RegistryError
from .progress import WorkEntry, append_work_entry, write_progress_report
from .sources import build_source_ledger, load_sources


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
