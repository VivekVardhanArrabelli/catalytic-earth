#!/usr/bin/env python3
"""Run/apply the silver geometry-confirmation gate for materialized rows."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.silver_geometry_confirmation_run import (  # noqa: E402
    DEFAULT_GEOMETRY_ABSTAIN_THRESHOLD,
    DEFAULT_OUT,
    DEFAULT_REPORT,
    write_silver_geometry_confirmation_run,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument(
        "--expansion-registry",
        default="data/registries/external_bronze_labels.json",
    )
    parser.add_argument(
        "--frozen-benchmark",
        default="data/registries/curated_mechanism_labels.json",
    )
    parser.add_argument("--cohesion-threshold", type=float, default=0.92)
    parser.add_argument("--min-exact-residues", type=int, default=2)
    parser.add_argument(
        "--abstain-threshold",
        type=float,
        default=DEFAULT_GEOMETRY_ABSTAIN_THRESHOLD,
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    audit = write_silver_geometry_confirmation_run(
        out_path=Path(args.out),
        report_path=Path(args.report) if args.report else None,
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=Path(args.frozen_benchmark),
        cohesion_threshold=args.cohesion_threshold,
        min_exact_residues=args.min_exact_residues,
        abstain_threshold=args.abstain_threshold,
        apply=args.apply,
    )
    c = audit["counts"]
    print(
        f"Wrote {args.out} (ready {c['ready_for_geometry_confirmation_run']}; "
        f"pass {c['pass_geometry_confirmation']}; hold "
        f"{c['hold_geometry_confirmation']}; silver flips applied "
        f"{c['silver_flips_applied']}; frozen sha unchanged "
        f"{audit['frozen_benchmark_byte_unchanged']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
