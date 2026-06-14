#!/usr/bin/env python3
"""Preview (and, with --apply, perform) the reaction-saturation trim.

Backward cleanup of the lowest-quality organic growth: families that grew deep on
organism/sequence breadth but NOT reaction/mechanism diversity (e.g. Mn/Fe superoxide
dismutase: 166 labels / 1 distinct Rhea reaction / 160 organisms). The trim keeps a
reaction- and sequence-diverse subset of each reaction-saturated family down to its
reaction-aware cap (clamp(rate * distinct_reactions, floor, ceiling)) and demotes the
redundant orthologs.

Offline + metadata-only: no network, no mmseqs, no embeddings. The default run is a
NON-DESTRUCTIVE preview that writes only artifacts/ + work/. --apply rewrites the
SEPARATE expansion registry (data/registries/external_bronze_labels.json), dropping
only the demoted entry_ids and re-validating every kept label; the frozen current702
benchmark (data/registries/curated_mechanism_labels.json) is NEVER written.

Usage:
    PYTHONPATH=src python scripts/trim_reaction_saturation.py            # preview only
    PYTHONPATH=src python scripts/trim_reaction_saturation.py --apply    # preview + rewrite
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.reaction_saturation_trim import (  # noqa: E402
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
    apply_reaction_saturation_trim_to_registry,
    write_reaction_saturation_trim,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "<missing>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="artifacts/v3_reaction_saturation_trim_preview_current702_20260614.json",
    )
    parser.add_argument(
        "--report",
        default="work/reaction_saturation_trim_preview_current702_20260614.md",
    )
    parser.add_argument("--frozen", default=str(DEFAULT_FROZEN_BENCHMARK_PATH))
    parser.add_argument("--expansion", default=str(DEFAULT_EXPANSION_REGISTRY_PATH))
    parser.add_argument("--reaction-cap-rate", type=int, default=8)
    parser.add_argument("--target-floor", type=int, default=100)
    parser.add_argument("--cap-ceiling", type=int, default=250)
    parser.add_argument("--saturation-ratio-threshold", type=float, default=10.0)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="rewrite the expansion registry, dropping the demoted rows (default: preview only)",
    )
    args = parser.parse_args()

    frozen_path = Path(args.frozen)
    expansion_path = Path(args.expansion)
    frozen_sha_before = _sha256(frozen_path)

    audit = write_reaction_saturation_trim(
        out_path=Path(args.out),
        report_path=Path(args.report),
        frozen_benchmark_path=frozen_path,
        expansion_registry_path=expansion_path,
        reaction_cap_rate=args.reaction_cap_rate,
        target_floor=args.target_floor,
        cap_ceiling=args.cap_ceiling,
        saturation_ratio_threshold=args.saturation_ratio_threshold,
    )
    t = audit["totals"]
    pd = audit["projected_diversity"]
    print(
        f"Reaction-saturation trim preview -> {args.out} "
        f"(rate {args.reaction_cap_rate}; floor {args.target_floor}; ceiling "
        f"{args.cap_ceiling}; ratio>{args.saturation_ratio_threshold})"
    )
    print(
        f"  families trimmed {t['families_trimmed']}; rows demoted {t['rows_demoted']}; "
        f"expansion {t['expansion_before']} -> {t['expansion_after']}; "
        f"combined {t['combined_before']} -> {t['combined_after']}"
    )
    print(
        f"  fingerprint Gini {pd['fingerprint_gini_before']} -> "
        f"{pd['fingerprint_gini_after']} "
        "(rises by design: depth now proportional to reaction diversity)"
    )
    for f in audit["trimmed_families"]:
        print(
            f"    {f['fingerprint']}: {f['current_seed_labels']} -> {f['kept']} "
            f"({f['distinct_reactions']} rxn, cap {f['reaction_aware_cap']}, "
            f"demote {f['demoted']}, labels/rxn {f['labels_per_distinct_reaction']} -> "
            f"{f['projected_labels_per_distinct_reaction']})"
        )
    cb = audit["separate_honest_counters"]["before"]
    ca = audit["separate_honest_counters"]["after"]
    print(
        f"  positive_bronze {cb['positive_bronze_count']} -> {ca['positive_bronze_count']}; "
        f"oos_bronze {cb['oos_bronze_count']} -> {ca['oos_bronze_count']} (separate, never merged)"
    )
    print(f"  frozen current702 sha256 (before): {frozen_sha_before}")

    if not args.apply:
        print("  PREVIEW ONLY -- no registry written. Re-run with --apply to rewrite.")
        return 0

    result = apply_reaction_saturation_trim_to_registry(
        preview_path=Path(args.out),
        expansion_registry_path=expansion_path,
        frozen_benchmark_registry_path=frozen_path,
    )
    frozen_sha_after = _sha256(frozen_path)
    print(
        f"  APPLIED -- expansion {result['expansion_registry_before']} -> "
        f"{result['expansion_registry_after']} (removed {result['rows_removed']}); "
        f"frozen written: {result['frozen_benchmark_registry_written']}"
    )
    print(f"  frozen current702 sha256 (after):  {frozen_sha_after}")
    if frozen_sha_before != frozen_sha_after:
        print("  ERROR: frozen current702 sha changed -- aborting", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
