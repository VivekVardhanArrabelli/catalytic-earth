#!/usr/bin/env python3
"""Build a non-destructive high-yield family lane factory scout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import UNIPROT_SEARCH_URL, USER_AGENT  # noqa: E402
from catalytic_earth.high_yield_family_lane_factory import (  # noqa: E402
    write_high_yield_family_lane_factory,
)

DEFAULT_OUT = "artifacts/v3_high_yield_family_lane_factory_current702_20260614.json"
DEFAULT_REPORT = "work/high_yield_family_lane_factory_current702_20260614.md"


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=ec:4.2.3.*&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
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

    audit = write_high_yield_family_lane_factory(
        out_path=Path(args.out),
        report_path=Path(args.report),
    )
    c = audit["counts"]
    print(
        f"Wrote {args.out} ({audit['status']}; "
        f"{c['candidate_families_ranked']} families ranked; "
        f"ready existing lanes >=150: {c['ready_existing_lanes_ge_150']}; "
        f"blocked high-yield lanes: {c['high_yield_blocked_new_or_infra']}; "
        f"top projected clean admits: {c['projected_clean_admits_top_family']})."
    )
    print(f"NEXT: {audit['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
