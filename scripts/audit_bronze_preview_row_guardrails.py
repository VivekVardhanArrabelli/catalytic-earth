#!/usr/bin/env python3
"""Audit non-destructive bronze preview rows before any apply."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.bronze_preview_row_guardrails import (  # noqa: E402
    write_bronze_preview_row_guardrails,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report")
    parser.add_argument("--expected-fingerprint")
    parser.add_argument("--expected-source-tier")
    args = parser.parse_args()

    audit = write_bronze_preview_row_guardrails(
        preview_path=Path(args.preview),
        out_path=Path(args.out),
        report_path=Path(args.report) if args.report else None,
        expected_fingerprint=args.expected_fingerprint,
        expected_source_tier=args.expected_source_tier,
    )
    c = audit["counts"]
    print(
        f"Wrote {args.out} ({audit['status']}; audited "
        f"{c['preview_applied_label_rows']} rows; problem rows {c['problem_rows']})."
    )
    return 1 if c["problem_rows"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
