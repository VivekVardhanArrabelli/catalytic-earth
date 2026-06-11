#!/usr/bin/env python3
"""Breadth feasibility scout (scaling_plan_to_10k) — non-destructive recon.

Answers, from reviewed Swiss-Prot, whether "10k diverse bronze" is reachable: how many
candidate mechanism families BEYOND the current 12 are mechanistically distinct, have
enough reviewed supply to reach the 100-floor, and are not redundant with an existing
fingerprint's EC/cofactor lane. Writes a verdict artifact + work report. NO registry is
written and NO labels are created.

Probes are cheap: the supply count is read from the UniProt `x-total-results` header (one
request per lane, no paging), and reaction diversity from a small EC-only sample. Requires
live UniProt egress.

Usage:
    PYTHONPATH=src python scripts/scout_breadth_feasibility.py
    PYTHONPATH=src python scripts/scout_breadth_feasibility.py --sample-size 200
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
from catalytic_earth.breadth_feasibility_scout import (  # noqa: E402
    write_breadth_feasibility_scout,
)

DEFAULT_OUT = "artifacts/v3_breadth_feasibility_scout_current702.json"
DEFAULT_REPORT = "work/breadth_feasibility_scout_current702.md"


def _egress_ok() -> bool:
    try:
        request = Request(
            f"{UNIPROT_SEARCH_URL}?query=ec:2.1.1.1&format=tsv&size=1",
            headers={"User-Agent": USER_AGENT},
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - public UniProt REST
            return 200 <= response.status < 300
    except (URLError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-size", type=int, default=200)
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

    audit = write_breadth_feasibility_scout(
        out_path=Path(args.out),
        report_path=Path(args.report),
        sample_size=args.sample_size,
    )

    c = audit["counts"]
    v = audit["verdict"]
    print(
        f"Wrote {args.out} ({audit['status']}; "
        f"{c['candidate_families_probed']} families probed; "
        f"{c['clean_families']} clean; "
        f"est. new clean bronze {c['estimated_new_clean_diverse_bronze']}; "
        f"projected positive bronze {c['projected_positive_bronze_clean_only']}; "
        f"gap to 10k {c['gap_to_10k_positive_bronze']})."
    )
    print(f"VERDICT: {v['verdict_code']}")
    print(f"  {v['recommendation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
