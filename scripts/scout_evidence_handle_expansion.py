#!/usr/bin/env python3
"""Evidence-handle expansion scout (scaling_plan_to_10k) — non-destructive recon.

Measures, per family, how much reviewed-Swiss-Prot supply the import gate recovers when the
corroborator handle is broadened beyond cc_cofactor to keyword / binding-site / active-site
annotation. This is the within-Swiss-Prot fix to do BEFORE expanding source classes (the NAD(P)
case: cc_cofactor reaches ~7 of ~7800 reviewed EC 1.1.1 entries; keyword:NAD/NADP reaches ~7700).
Writes a verdict artifact + work report. NO registry is written and NO labels are created.

Requires live UniProt egress (cheap x-total-results header counts only).

Usage:
    PYTHONPATH=src python scripts/scout_evidence_handle_expansion.py
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
from catalytic_earth.evidence_handle_expansion import (  # noqa: E402
    write_evidence_handle_expansion,
)

DEFAULT_OUT = "artifacts/v3_evidence_handle_expansion_current702.json"
DEFAULT_REPORT = "work/evidence_handle_expansion_current702.md"


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--skip-egress-check", action="store_true")
    args = parser.parse_args()

    if not args.skip_egress_check and not _egress_ok():
        print(
            "ERROR: UniProt REST is not reachable from this environment "
            f"({UNIPROT_SEARCH_URL} did not return 2xx). Run where the network policy "
            "allows UniProt egress, or pass --skip-egress-check to attempt anyway.",
            file=sys.stderr,
        )
        return 2

    audit = write_evidence_handle_expansion(
        out_path=Path(args.out),
        report_path=Path(args.report),
    )
    c = audit["counts"]
    print(
        f"Wrote {args.out} ({audit['status']}; "
        f"{c['families_probed']} families probed; "
        f"{c['handle_blocked_families_unlocked_by_better_handle']} unlocked by a better handle; "
        f"supply uplift {c['total_reviewed_supply_uplift_over_current_handles']}; "
        f"reachable positive-bronze uplift {c['total_reachable_positive_bronze_uplift']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
