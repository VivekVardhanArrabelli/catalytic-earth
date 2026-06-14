#!/usr/bin/env python3
"""Audit silver-ready rows for geometry-confirmation runnability.

This is deliberately non-destructive: it does not run/fake the geometry gate, write the
registry, or flip tiers. It reports which silver-ready rows still lack local holo
coordinates or explicit PDB residue mappings.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.silver_geometry_confirmation import (  # noqa: E402
    DEFAULT_OUT,
    DEFAULT_REPORT,
    write_silver_geometry_confirmation_audit,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument(
        "--expansion-registry",
        default="data/registries/external_bronze_labels.json",
    )
    parser.add_argument("--cohesion-threshold", type=float, default=0.92)
    parser.add_argument("--min-exact-residues", type=int, default=2)
    args = parser.parse_args()

    audit = write_silver_geometry_confirmation_audit(
        out_path=Path(args.out),
        report_path=Path(args.report) if args.report else None,
        expansion_registry_path=Path(args.expansion_registry),
        cohesion_threshold=args.cohesion_threshold,
        min_exact_residues=args.min_exact_residues,
    )
    c = audit["counts"]
    print(
        f"Wrote {args.out} ({audit['status']}; silver-ready "
        f"{c['silver_ready_input_rows']}; runnable "
        f"{c['ready_for_geometry_confirmation_run']}; blocked "
        f"{c['blocked_before_geometry_confirmation']}; silver flips "
        f"{c['silver_flips_applied']}; no registry written)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
