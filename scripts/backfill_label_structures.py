#!/usr/bin/env python3
"""Stage AlphaFoldDB v6 coordinates for expansion labels (non-destructive).

Track 1 / 1b. Derives the AFDB v6 handle from each expansion label's UniProt accession
(`AF-{acc}-F1-model_v6.cif`), fetches the predicted CIF, hashes it, and records
`evidence.structure_provenance.afdb_v6_coordinate` (handle + sha256 + provenance). The
CIFs are regeneratable from the handle and are NOT committed (staged to temp, discarded).
Structure is review-only mechanism context (a bronze->silver signal), never a predictive
feature. The frozen current702 benchmark is NEVER written.

A preview run is non-destructive (summary artifact + work report only); `--apply` writes
the SEPARATE expansion registry via the canonical compact serializer. A cache under the
git-ignored data/cache/ makes runs resumable; use `--limit` for chunked runs.

Requires live AlphaFoldDB egress.

Usage:
    PYTHONPATH=src python scripts/backfill_label_structures.py                 # preview only
    PYTHONPATH=src python scripts/backfill_label_structures.py --limit 500     # stage 500 then preview
    PYTHONPATH=src python scripts/backfill_label_structures.py --apply         # preview + write registry
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import USER_AGENT  # noqa: E402
from catalytic_earth.label_structure_backfill import (  # noqa: E402
    DEFAULT_OUT,
    DEFAULT_REPORT,
    DEFAULT_STRUCTURE_CACHE_PATH,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    write_label_structure_backfill,
)
from catalytic_earth.ser_his_hole_sourcing import ALPHAFOLD_CIF_URL  # noqa: E402


def _egress_ok() -> bool:
    try:
        request = Request(
            ALPHAFOLD_CIF_URL.format(accession="P0A6P9"),
            headers={"User-Agent": USER_AGENT},
            method="HEAD",
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public AFDB
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--expansion-registry", default=str(EXPANSION_REGISTRY_PATH))
    parser.add_argument("--cache", default=str(DEFAULT_STRUCTURE_CACHE_PATH))
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="cap NEW AFDB fetches this run (for chunked/resumable runs)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the staged coordinate provenance into the expansion registry",
    )
    parser.add_argument(
        "--skip-egress-check",
        action="store_true",
        help="do not preflight AlphaFoldDB reachability",
    )
    args = parser.parse_args()

    if not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: AlphaFoldDB is not reachable from this environment. Run where the "
            "network policy allows AFDB egress, or pass --skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    summary = write_label_structure_backfill(
        out_path=Path(args.out),
        report_path=Path(args.report),
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        apply=args.apply,
        cache_path=Path(args.cache) if args.cache else None,
        limit=args.limit,
    )

    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; expansion labels {c['expansion_labels']}; "
        f"staged {c['staged_this_run']}; already {c['already_staged']}; "
        f"unavailable {c['unavailable']}; deferred {c['deferred_over_limit']}; "
        f"fetches {c['fetched_this_run']}; coverage {c['coverage_fraction_after'] * 100:.1f}%)."
    )
    if args.apply:
        print(
            f"APPLIED: expansion registry written = {summary['expansion_registry_written']}; "
            f"frozen benchmark written = {summary['frozen_benchmark_registry_written']}; "
            f"path = {summary.get('expansion_registry_path')}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
