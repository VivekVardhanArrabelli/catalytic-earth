#!/usr/bin/env python3
"""Wire the broadened evidence handles into the admission engine for the NAD(P)-dehydrogenase
+ glycosyltransferase families and source fresh annotation-anchored bronze (scaling_plan_to_10k).

These two families' defining evidence is NOT a UniProt cofactor comment but a dissociable
COSUBSTRATE / donor + functional keyword, so they need the broadened mechanism corroborator
(cosubstrate / Rhea participant / keyword / active-site) the engine now reads. The fetch is
split into capped EC-subclass lanes; each row runs fetch -> broadened-corroborator/EC
disambiguation -> novelty gate -> per-family cap guard, then writes a NON-DESTRUCTIVE preview.
With --apply it appends the novelty-admitted labels to the SEPARATE expansion registry
(data/registries/external_bronze_labels.json); the frozen current702 benchmark is never written
(the frozen sha is printed before/after apply).

Requires live UniProt egress. See docs/scaling_plan_to_10k.md (2026-06-12 update).

Usage:
    PYTHONPATH=src python scripts/source_nad_glycosyltransferase_families.py            # preview only
    PYTHONPATH=src python scripts/source_nad_glycosyltransferase_families.py --apply    # preview + append
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
from catalytic_earth.external_annotation_anchored_import import (  # noqa: E402
    apply_external_annotation_anchored_import_to_registry,
)
from catalytic_earth.external_scaleout_bronze_import import (  # noqa: E402
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)
from catalytic_earth.nad_glycosyltransferase_subfamily_sourcing import (  # noqa: E402
    FAMILIES,
    write_nad_glycosyltransferase_subfamily_sourcing,
)

DEFAULT_OUT = "artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json"
DEFAULT_REPORT = "work/nad_glycosyltransferase_subfamily_sourcing_current702.md"


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=ec:1.1.1.1&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def _frozen_sha() -> str:
    path = Path(DEFAULT_FROZEN_BENCHMARK_PATH)
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--families",
        nargs="+",
        default=list(FAMILIES),
        choices=list(FAMILIES),
        help="which broadened-handle families to source; default = both",
    )
    parser.add_argument("--max-records-per-lane", type=int, default=60)
    parser.add_argument(
        "--cap-ceiling",
        type=int,
        default=250,
        help=(
            "system cap ceiling for non-confusable families (default 250). Chemistry-"
            "confusable families (nad_p_dehydrogenase) are capped at 150 by the runner "
            "regardless, to keep reaction redundancy low."
        ),
    )
    parser.add_argument(
        "--reaction-aware-caps",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "earn each family's cap from its reaction diversity "
            "(clamp(rate*distinct_reactions, floor, per-family ceiling)) instead of a "
            "flat ceiling; on by default. --no-reaction-aware-caps restores the flat cap"
        ),
    )
    parser.add_argument(
        "--reaction-cap-rate",
        type=int,
        default=8,
        help="labels earned per distinct Rhea reaction for the reaction-aware cap",
    )
    parser.add_argument(
        "--per-reaction-cap",
        type=int,
        default=12,
        help=(
            "admission-time ceiling on labels per distinct Rhea reaction within a scope; "
            "pass a negative value to disable"
        ),
    )
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

    audit = write_nad_glycosyltransferase_subfamily_sourcing(
        out_path=Path(args.out),
        report_path=Path(args.report),
        families=tuple(args.families),
        max_records_per_lane=args.max_records_per_lane,
        cap_ceiling=args.cap_ceiling,
        reaction_aware_caps=args.reaction_aware_caps,
        reaction_cap_rate=args.reaction_cap_rate,
        per_reaction_cap=(args.per_reaction_cap if args.per_reaction_cap >= 0 else None),
    )

    c = audit["counts"]
    print(
        f"Wrote {args.out} ({audit['status']}; "
        f"fetched {c['fetched_candidate_rows']} rows; "
        f"mechanism-corroborated {c['mechanism_corroborated_bronze_labels']}; "
        f"novelty-admitted {c['novelty_admitted_labels']}; "
        f"combined {c['current_combined_labels']} -> "
        f"{c['projected_combined_labels_if_merged']} if merged)."
    )
    for family, proj in audit["floor_projection"].items():
        print(
            f"  {family}: {proj['combined_before']} -> {proj['projected_combined']} "
            f"(cap {proj['cap_ceiling']}; floor reached: {proj['floor_reached']})"
        )
    if audit["fetch_failure_count"]:
        print(f"  fetch_failures: {audit['fetch_failure_count']} (see artifact)")

    if args.apply:
        if not audit["applied_labels"]:
            print("Nothing to apply (0 novelty-admitted labels).")
            return 0
        sha_before = _frozen_sha()
        print(f"  frozen current702 sha256 BEFORE apply: {sha_before}")
        summary = apply_external_annotation_anchored_import_to_registry(
            preview_path=Path(args.out),
            expansion_registry_path=DEFAULT_EXPANSION_REGISTRY_PATH,
            frozen_benchmark_registry_path=DEFAULT_FROZEN_BENCHMARK_PATH,
        )
        sha_after = _frozen_sha()
        print(
            f"APPLIED: appended {summary['appended']} bronze "
            f"(skipped {summary['duplicate_skipped']} dup); expansion "
            f"{summary['expansion_registry_before']} -> {summary['expansion_registry_after']}; "
            f"combined total {summary['combined_total_labels']}; "
            f"frozen benchmark written: {summary['frozen_benchmark_registry_written']}."
        )
        print(f"  frozen current702 sha256 AFTER apply:  {sha_after}")
        print(
            "  frozen current702 UNCHANGED"
            if sha_before == sha_after
            else "  WARNING: frozen current702 sha CHANGED -- investigate before trusting"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
