#!/usr/bin/env python3
"""Source the cofactorless ser_his_acid_hydrolase hole end to end.

Fetches reviewed serine-hydrolase Swiss-Prot rows (EC 3.4.21/3.4.16/3.1.1, ACT_SITE
annotated, no cofactor), stages the AlphaFoldDB v6 predicted coordinate, confirms the
Ser/Cys/Thr-His-Asp/Glu catalytic triad against the annotated ACT_SITE, novelty-gates,
and writes a NON-DESTRUCTIVE preview. With --apply it appends the novelty-admitted
labels to the SEPARATE expansion registry; the frozen current702 benchmark is never
written. Requires live UniProt + AlphaFoldDB egress. See
docs/stage1_hole_sourcing_runbook.md.

Usage:
    PYTHONPATH=src python scripts/source_ser_his_hole.py            # preview only
    PYTHONPATH=src python scripts/source_ser_his_hole.py --apply    # preview + append
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
from catalytic_earth.external_annotation_anchored_import import (  # noqa: E402
    apply_external_annotation_anchored_import_to_registry,
)
from catalytic_earth.external_scaleout_bronze_import import (  # noqa: E402
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)
from catalytic_earth.ser_his_hole_sourcing import (  # noqa: E402
    ALPHAFOLD_CIF_URL,
    write_ser_his_hole_sourcing,
)

DEFAULT_OUT = "artifacts/v3_ser_his_hole_sourcing_preview_current702.json"
DEFAULT_REPORT = "work/ser_his_hole_sourcing_current702.md"


def _url_ok(url: str) -> bool:
    try:
        request = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def _egress_ok() -> tuple[bool, bool]:
    uniprot = _url_ok(f"{UNIPROT_SEARCH_URL}?query=ec:3.4.21.1&format=tsv&size=1")
    # P00760 (bovine trypsin) is a stable AFDB v6 entry used only as a reachability probe.
    afdb = _url_ok(ALPHAFOLD_CIF_URL.format(accession="P00760"))
    return uniprot, afdb


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-records-per-lane", type=int, default=60)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="append the novelty-admitted bronze labels to the expansion registry",
    )
    parser.add_argument(
        "--skip-egress-check",
        action="store_true",
        help="do not preflight UniProt/AlphaFoldDB reachability",
    )
    args = parser.parse_args()

    if not args.skip_egress_check:
        uniprot_ok, afdb_ok = _egress_ok()
        if not (uniprot_ok and afdb_ok):
            print(
                "ERROR: required egress unreachable "
                f"(UniProt 2xx: {uniprot_ok}; AlphaFoldDB 2xx: {afdb_ok}). The ser_his "
                "hole needs BOTH live UniProt (annotation) and AlphaFoldDB (coordinates). "
                "Run where the network policy allows both, or pass --skip-egress-check.",
                file=sys.stderr,
            )
            return 2

    audit = write_ser_his_hole_sourcing(
        out_path=Path(args.out),
        report_path=Path(args.report),
        max_records_per_lane=args.max_records_per_lane,
    )

    c = audit["counts"]
    proj = audit["floor_projection"]["ser_his_acid_hydrolase"]
    print(
        f"Wrote {args.out} ({audit['status']}; "
        f"fetched {c['fetched_candidate_rows']} rows; staged {c['coordinates_staged']} "
        f"coordinates; triad-confirmed {c['triad_confirmed_labels']}; "
        f"novelty-admitted {c['novelty_admitted_labels']}; "
        f"combined {c['current_combined_labels']} -> "
        f"{c['projected_combined_labels_if_merged']} if merged)."
    )
    print(
        f"  ser_his_acid_hydrolase: {proj['combined_before']} -> {proj['projected_combined']} "
        f"(floor reached: {proj['floor_reached']})"
    )
    if c["coordinate_failure_count"]:
        print(f"  afdb coordinate unavailable: {c['coordinate_failure_count']} (see artifact)")

    if args.apply:
        if not audit["applied_labels"]:
            print("Nothing to apply (0 novelty-admitted labels).")
            return 0
        summary = apply_external_annotation_anchored_import_to_registry(
            preview_path=Path(args.out),
            expansion_registry_path=DEFAULT_EXPANSION_REGISTRY_PATH,
            frozen_benchmark_registry_path=DEFAULT_FROZEN_BENCHMARK_PATH,
        )
        print(
            f"APPLIED: appended {summary['appended']} bronze "
            f"(skipped {summary['duplicate_skipped']} dup); expansion "
            f"{summary['expansion_registry_before']} -> {summary['expansion_registry_after']}; "
            f"combined total {summary['combined_total_labels']}; "
            f"frozen benchmark written: {summary['frozen_benchmark_registry_written']}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
