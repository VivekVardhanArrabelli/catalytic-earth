#!/usr/bin/env python3
"""Confirm HOLO experimental-PDB coordinates for bronze->silver promotion (non-destructive).

For each bronze seed label whose chemistry already corroborates its fingerprint and that
carries experimental `pdb_ids` + an annotated cofactor, this fetches the PDB mmCIF and checks
whether the annotated cofactor is present as a HETATM (the same holo test the promotion gate
uses). When it is, it records a sha-pinned `evidence.structure_provenance.holo_pdb_confirmation`
so the gate scores the row `silver_ready_pending_geometry_run`. The mmCIFs are regeneratable
from the PDB id and are NOT committed. The frozen current702 benchmark is NEVER written (its
sha is printed before/after).

A preview run is non-destructive (summary artifact + work report only); `--apply` writes the
SEPARATE expansion registry. A cache under the git-ignored data/cache/ makes runs resumable;
use `--limit` / `--per-fingerprint-cap` for chunked runs.

Requires live RCSB egress.

Usage:
    PYTHONPATH=src python scripts/promote_holo_structures.py                      # preview only
    PYTHONPATH=src python scripts/promote_holo_structures.py --per-fingerprint-cap 5
    PYTHONPATH=src python scripts/promote_holo_structures.py --limit 80 --apply
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
from catalytic_earth.holo_structure_promotion import (  # noqa: E402
    DEFAULT_CACHE_PATH,
    DEFAULT_OUT,
    DEFAULT_REPORT,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    RCSB_CIF_URL,
    write_holo_structure_promotion,
)


def _egress_ok() -> bool:
    try:
        request = Request(
            RCSB_CIF_URL.format(pdb_id="1CRN"),
            headers={"User-Agent": USER_AGENT},
            method="HEAD",
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public RCSB
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--expansion-registry", default=str(EXPANSION_REGISTRY_PATH))
    parser.add_argument("--cache", default=str(DEFAULT_CACHE_PATH))
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="cap NEW candidate rows fetched this run (for chunked/resumable runs)",
    )
    parser.add_argument(
        "--per-fingerprint-cap",
        type=int,
        default=None,
        help="cap candidate rows attempted per fingerprint (diverse, bounded preview)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the holo confirmation into the expansion registry",
    )
    parser.add_argument(
        "--skip-egress-check",
        action="store_true",
        help="do not preflight RCSB reachability",
    )
    args = parser.parse_args()

    if not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: RCSB is not reachable from this environment. Run where the network "
            "policy allows RCSB egress, or pass --skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    summary = write_holo_structure_promotion(
        out_path=Path(args.out),
        report_path=Path(args.report),
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        apply=args.apply,
        cache_path=Path(args.cache) if args.cache else None,
        limit=args.limit,
        per_fingerprint_cap=args.per_fingerprint_cap,
    )

    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; seed {c['seed_labels']}; "
        f"holo confirmed this run {c['holo_confirmed_this_run']}; already "
        f"{c['already_confirmed']}; no-holo {c['no_holo_pdb_found']}; "
        f"total confirmed after {c['rows_holo_confirmed_after']}; "
        f"rows fetched {c['rows_fetched_this_run']})."
    )
    print(
        f"frozen current702 sha256 before={summary['frozen_sha256_before']} "
        f"after={summary['frozen_sha256_after']} "
        f"byte_unchanged={summary['frozen_benchmark_byte_unchanged']}"
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
