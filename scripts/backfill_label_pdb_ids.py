#!/usr/bin/env python3
"""Backfill UniProt PDB cross-reference IDs onto external labels.

Preview by default. With ``--apply`` it writes only the separate external registry and
prints the frozen current702 SHA before/after.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import UNIPROT_SEARCH_URL, USER_AGENT  # noqa: E402
from catalytic_earth.label_pdb_id_backfill import (  # noqa: E402
    DEFAULT_OUT,
    DEFAULT_REPORT,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    write_label_pdb_id_backfill,
)


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=accession:P0A6P9&fields=accession,xref_pdb&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def _frozen_sha() -> str:
    path = Path(FROZEN_BENCHMARK_PATH)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--expansion-registry", default=str(EXPANSION_REGISTRY_PATH))
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skip-egress-check", action="store_true")
    args = parser.parse_args()

    if not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: UniProt REST is not reachable. Run where egress is allowed, or pass "
            "--skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    sha_before = _frozen_sha()
    summary = write_label_pdb_id_backfill(
        out_path=Path(args.out),
        report_path=Path(args.report),
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        apply=args.apply,
        limit=args.limit,
    )
    sha_after = _frozen_sha()
    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; queried {c['accessions_queried']}; "
        f"backfilled {c['backfilled_pdb_rows_this_run']}; already {c['already_had_pdb_ids']}; "
        f"without-xref {c['uniprot_record_without_pdb_xref']}; deferred {c['deferred_over_limit']})."
    )
    print(f"frozen current702 sha256 before={sha_before} after={sha_after}")
    if args.apply:
        print(
            f"APPLIED: expansion registry written={summary['expansion_registry_written']}; "
            f"frozen benchmark written={summary['frozen_benchmark_registry_written']}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
