#!/usr/bin/env python3
"""Source aminoglycoside acetyltransferase (AAC) bronze through broadened handles."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from pathlib import Path
from queue import Empty
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import UNIPROT_SEARCH_URL, USER_AGENT  # noqa: E402
from catalytic_earth.adapters import (  # noqa: E402
    fetch_rhea_by_ec,
    fetch_uniprot_entry,
    fetch_uniprot_query,
)
from catalytic_earth.aminoglycoside_acetyltransferase_sourcing import (  # noqa: E402
    FAMILIES,
    write_aminoglycoside_acetyltransferase_sourcing,
)
from catalytic_earth.external_annotation_anchored_import import (  # noqa: E402
    apply_external_annotation_anchored_import_to_registry,
)
from catalytic_earth.external_scaleout_bronze_import import (  # noqa: E402
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)

DEFAULT_OUT = "artifacts/v3_aminoglycoside_acetyltransferase_sourcing_preview_current702.json"
DEFAULT_REPORT = "work/aminoglycoside_acetyltransferase_sourcing_current702.md"


class _FetchTimeout(RuntimeError):
    pass


def _child_fetch(queue, func, args):
    try:
        queue.put(("ok", func(*args)))
    except Exception as exc:  # pragma: no cover - live fetch failure path
        queue.put(("err", type(exc).__name__, str(exc)))


def _with_timeout(timeout_seconds: int, func, *args):
    if timeout_seconds <= 0:
        return func(*args)
    ctx = mp.get_context("fork")
    queue = ctx.Queue(maxsize=1)
    proc = ctx.Process(target=_child_fetch, args=(queue, func, args))
    proc.start()
    try:
        status, *payload = queue.get(timeout=timeout_seconds)
    except Empty:
        proc.terminate()
        proc.join(2)
        raise _FetchTimeout(f"fetch exceeded {timeout_seconds}s timeout")
    proc.join(2)
    if proc.is_alive():
        proc.terminate()
        proc.join(2)
    if status == "ok":
        return payload[0]
    error_type, message = payload
    raise RuntimeError(f"{error_type}: {message}")


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=ec:2.3.1.*+AND+protein_name:aminoglycoside+AND+keyword:Acetyltransferase&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def _frozen_sha() -> str:
    path = Path(DEFAULT_FROZEN_BENCHMARK_PATH)
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--families",
        nargs="+",
        default=list(FAMILIES),
        choices=list(FAMILIES),
        help="which broadened-handle families to source; default = aminoglycoside_acetyltransferase",
    )
    parser.add_argument("--max-records-per-lane", type=int, default=260)
    parser.add_argument("--record-offset-per-lane", type=int, default=0)
    parser.add_argument("--record-limit-per-lane", type=int, default=None)
    parser.add_argument("--cap-ceiling", type=int, default=150)
    parser.add_argument("--lane-ids", nargs="+", default=None)
    parser.add_argument(
        "--fetch-timeout-seconds",
        type=int,
        default=0,
        help=(
            "optional per-query/per-entry/per-Rhea timeout; timed-out records are captured as "
            "fetch failures in the preview instead of hanging the run"
        ),
    )
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="append the novelty-admitted bronze labels to the expansion registry",
    )
    parser.add_argument(
        "--reuse-preview",
        action="store_true",
        help="with --apply, load the existing --out preview instead of refetching live sources",
    )
    parser.add_argument("--skip-egress-check", action="store_true")
    args = parser.parse_args()

    if args.reuse_preview and not args.apply:
        print("ERROR: --reuse-preview is only valid together with --apply.", file=sys.stderr)
        return 2

    if not args.reuse_preview and not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: UniProt REST is not reachable from this environment "
            f"({UNIPROT_SEARCH_URL} did not return 2xx). Run where the network policy "
            "allows UniProt egress, or pass --skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    if args.reuse_preview:
        audit = json.loads(Path(args.out).read_text(encoding="utf-8"))
    else:
        query_fetcher = (
            (lambda query, size: _with_timeout(args.fetch_timeout_seconds, fetch_uniprot_query, query, size))
            if args.fetch_timeout_seconds
            else fetch_uniprot_query
        )
        entry_fetcher = (
            (lambda accession: _with_timeout(args.fetch_timeout_seconds, fetch_uniprot_entry, accession))
            if args.fetch_timeout_seconds
            else fetch_uniprot_entry
        )
        rhea_fetcher = (
            (lambda ec_number, limit: _with_timeout(args.fetch_timeout_seconds, fetch_rhea_by_ec, ec_number, limit))
            if args.fetch_timeout_seconds
            else fetch_rhea_by_ec
        )
        audit = write_aminoglycoside_acetyltransferase_sourcing(
            out_path=Path(args.out),
            report_path=Path(args.report),
            families=tuple(args.families),
            max_records_per_lane=args.max_records_per_lane,
            record_offset_per_lane=args.record_offset_per_lane,
            record_limit_per_lane=args.record_limit_per_lane,
            lane_ids=tuple(args.lane_ids) if args.lane_ids else None,
            cap_ceiling=args.cap_ceiling,
            query_fetcher=query_fetcher,
            entry_fetcher=entry_fetcher,
            rhea_fetcher=rhea_fetcher,
        )

    c = audit["counts"]
    print(
        f"{'Loaded' if args.reuse_preview else 'Wrote'} {args.out} ({audit['status']}; "
        f"fetched {c['fetched_candidate_rows']} rows; "
        f"target mechanism-corroborated {c['mechanism_corroborated_bronze_labels']}; "
        f"off-target held {c['off_target_fingerprint_matches_held']}; "
        f"novelty-admitted {c['novelty_admitted_labels']}; "
        f"combined {c['current_combined_labels']} -> "
        f"{c['projected_combined_labels_if_merged']} if merged)."
    )
    for family, proj in audit["floor_projection"].items():
        print(
            f"  {family}: {proj['combined_before']} -> {proj['projected_combined']} "
            f"(cap {proj['cap_ceiling']}; floor reached: {proj['floor_reached']})"
        )

    if args.apply:
        if not audit["applied_labels"]:
            print("Nothing to apply (0 novelty-admitted labels).")
            return 0
        sha_before = _frozen_sha()
        print(f"  frozen current702 sha256 BEFORE apply: {sha_before}")
        summary = apply_external_annotation_anchored_import_to_registry(
            preview_path=Path(args.out),
            expansion_registry_path=DEFAULT_EXPANSION_REGISTRY_PATH,
            frozen_benchmark_registry_path=DEFAULT_FROZEN_BENCHMARK_PATH,
        )
        sha_after = _frozen_sha()
        print(
            f"APPLIED: appended {summary['appended']} bronze "
            f"(skipped {summary['duplicate_skipped']} dup); expansion "
            f"{summary['expansion_registry_before']} -> {summary['expansion_registry_after']}; "
            f"combined total {summary['combined_total_labels']}; "
            f"frozen benchmark written: {summary['frozen_benchmark_registry_written']}."
        )
        print(f"  frozen current702 sha256 AFTER apply:  {sha_after}")
        if sha_before != sha_after:
            print("ERROR: frozen current702 sha changed during apply.", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
