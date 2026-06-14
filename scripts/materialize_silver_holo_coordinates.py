#!/usr/bin/env python3
"""Materialize verified local holo PDB coordinates for silver-ready rows.

Preview by default. With ``--apply`` it writes only the external registry and keeps
silver tier changes blocked until explicit PDB residue mappings plus geometry confirmation
exist.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.silver_holo_coordinate_materialization import (  # noqa: E402
    DEFAULT_COORDINATE_DIR,
    DEFAULT_OUT,
    DEFAULT_REPORT,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    write_silver_holo_coordinate_materialization,
)


def _frozen_sha() -> str:
    path = Path(FROZEN_BENCHMARK_PATH)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--expansion-registry", default=str(EXPANSION_REGISTRY_PATH))
    parser.add_argument("--coordinate-dir", default=str(DEFAULT_COORDINATE_DIR))
    parser.add_argument(
        "--fetch-limit",
        type=int,
        default=0,
        help="maximum missing PDB mmCIFs to fetch from RCSB; 0 reuses local files only",
    )
    parser.add_argument("--cohesion-threshold", type=float, default=0.92)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    sha_before = _frozen_sha()
    summary = write_silver_holo_coordinate_materialization(
        out_path=Path(args.out),
        report_path=Path(args.report) if args.report else None,
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        coordinate_dir=Path(args.coordinate_dir),
        apply=args.apply,
        fetch_limit=args.fetch_limit,
        cohesion_threshold=args.cohesion_threshold,
    )
    sha_after = _frozen_sha()
    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; silver-ready "
        f"{c['silver_ready_input_rows']}; reused "
        f"{c['reused_existing_artifact_coordinate']}; fetched "
        f"{c['fetched_and_materialized_coordinate']}; registry updates "
        f"{c['registry_coordinate_updates']}; verified-after "
        f"{c['verified_local_coordinates_after']}; deferred "
        f"{c['deferred_over_fetch_limit']})."
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
