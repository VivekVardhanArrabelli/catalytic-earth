#!/usr/bin/env python3
"""Map silver-ready UniProt residue positions to explicit PDB chain/residue positions.

Preview by default. With ``--apply`` it writes only the external registry and does not
run geometry confirmation or change tiers.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.silver_pdb_residue_mapping import (  # noqa: E402
    DEFAULT_OUT,
    DEFAULT_REPORT,
    EXPANSION_REGISTRY_PATH,
    FROZEN_BENCHMARK_PATH,
    write_silver_pdb_residue_mapping,
)


def _frozen_sha() -> str:
    path = Path(FROZEN_BENCHMARK_PATH)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--expansion-registry", default=str(EXPANSION_REGISTRY_PATH))
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--cohesion-threshold", type=float, default=0.92)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    sha_before = _frozen_sha()
    summary = write_silver_pdb_residue_mapping(
        out_path=Path(args.out),
        report_path=Path(args.report) if args.report else None,
        expansion_registry_path=Path(args.expansion_registry),
        frozen_benchmark_path=FROZEN_BENCHMARK_PATH,
        apply=args.apply,
        limit=args.limit,
        cohesion_threshold=args.cohesion_threshold,
    )
    sha_after = _frozen_sha()
    c = summary["counts"]
    print(
        f"Wrote {args.out} ({summary['status']}; silver-ready "
        f"{c['silver_ready_input_rows']}; attempted-local "
        f"{c['rows_attempted_with_local_coordinates']}; rows-mapped "
        f"{c['rows_mapped']}; residues-mapped {c['residues_mapped']}; "
        f"missing-local {c['missing_local_coordinate']})."
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
