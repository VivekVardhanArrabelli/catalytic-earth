#!/usr/bin/env python3
"""Backfill the deploy-input SEQUENCE onto expansion bronze labels (non-destructive).

The expansion atlas (data/registries/external_bronze_labels.json) stored only the UniProt
handle + length, never the sequence -- so the one input a deployed model predicts FROM was
absent for every expansion row. This fetches the reviewed UniProt sequence by accession and
records it under `evidence.sequence_provenance` (sequence, sha256, length, source accession,
retrieval provenance, retrieved_utc).

The sequence is stored DATA, never a predictive feature: the leakage wall (EC / protein name
/ UniProt prose) is unchanged and `predictive_evidence` stays []. Row counts are UNCHANGED
(a block is added in place). The frozen current702 benchmark is NEVER written; the writer
refuses to target it. A preview run is non-destructive (summary artifact + work report only);
`--apply` writes the SEPARATE expansion registry via the canonical compact serializer.

A small fetch cache under the git-ignored data/cache/ lets a preview run and a later --apply
run share one network pass.

Requires live UniProt egress.

Usage:
    PYTHONPATH=src python scripts/backfill_label_sequences.py            # preview only
    PYTHONPATH=src python scripts/backfill_label_sequences.py --apply    # preview + write registry
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import UNIPROT_SEARCH_URL, USER_AGENT  # noqa: E402
from catalytic_earth.label_sequence_backfill import (  # noqa: E402
    DEFAULT_FETCH_CACHE_PATH,
    DEFAULT_OUT,
    DEFAULT_REPORT,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    write_label_sequence_backfill,
)


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=accession:P0A6P9&fields=accession,sequence&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument(
        "--expansion-registry", default=str(EXPANSION_REGISTRY_PATH)
    )
    parser.add_argument("--cache", default=str(DEFAULT_FETCH_CACHE_PATH))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the backfilled sequences into the expansion registry",
    )
    parser.add_argument(
        "--skip-egress-check",
        action="store_true",
        help="do not preflight UniProt reachability",
    )
    args = parser.parse_args()

    if not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: UniProt REST is not reachable from this environment "
            f"({UNIPROT_SEARCH_URL} did not return 2xx). Run where the network policy "
            "allows UniProt egress, or pass --skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    summary = write_label_sequence_backfill(
        out_path=Path(args.out),
        report_path=Path(args.report),
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        apply=args.apply,
        cache_path=Path(args.cache) if args.cache else None,
    )

    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; "
        f"expansion labels {c['expansion_labels']}; needed fetch {c['needed_fetch']}; "
        f"backfilled {c['backfilled_this_run']}; already {c['already_backfilled']}; "
        f"fetch-missing {c['fetch_missing']}; length-conflicts {c['length_conflicts']}; "
        f"coverage {c['coverage_fraction_after'] * 100:.1f}%)."
    )
    if summary["fetch_failure_count"]:
        print(f"  fetch_failures: {summary['fetch_failure_count']} (see artifact)")

    if args.apply:
        print(
            f"APPLIED: expansion registry written = {summary['expansion_registry_written']}; "
            f"frozen benchmark written = {summary['frozen_benchmark_registry_written']}; "
            f"path = {summary.get('expansion_registry_path')}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
