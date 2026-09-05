#!/usr/bin/env python3
"""Build or verify the bounded Atlas-50 state representation probe."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_state_probe import (  # noqa: E402
    build_state_probe,
    canonical_json_bytes,
    file_sha256,
    validate_state_probe,
)


STATE_ROOT = ROOT / "data/atlas/atlas50/state_probe"
SPEC_PATH = STATE_ROOT / "spec.json"
REPORT_PATH = STATE_ROOT / "report.json"
CANDIDATE_SPEC_PATH = ROOT / "data/atlas/atlas50/phase_a/candidate_spec.json"
PANEL_REVIEW_PATH = (
    ROOT / "data/atlas/atlas50/computational_review/panel_review.json"
)
MECHANISM_V3_SCHEMA_PATH = (
    ROOT / "src/catalytic_earth/schemas/mechanism-record-v3.schema.json"
)
ATLAS3_KERNEL_PATH = ROOT / "data/atlas/atlas3/kernel.json"
ATLAS10_KERNEL_PATH = ROOT / "data/atlas/atlas10/kernel.json"

INPUT_PATHS = {
    "candidate_spec": CANDIDATE_SPEC_PATH,
    "computational_panel_review": PANEL_REVIEW_PATH,
    "mechanism_record_v3_schema": MECHANISM_V3_SCHEMA_PATH,
    "atlas3_kernel": ATLAS3_KERNEL_PATH,
    "atlas10_kernel": ATLAS10_KERNEL_PATH,
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict[str, Any]:
    spec = _load(SPEC_PATH)
    candidate_spec = _load(CANDIDATE_SPEC_PATH)
    panel_review = _load(PANEL_REVIEW_PATH)
    mechanism_schema = _load(MECHANISM_V3_SCHEMA_PATH)
    atlas3 = _load(ATLAS3_KERNEL_PATH)
    atlas10 = _load(ATLAS10_KERNEL_PATH)
    basis_inputs = {
        name: file_sha256(path) for name, path in sorted(INPUT_PATHS.items())
    }
    return build_state_probe(
        spec,
        candidate_spec=candidate_spec,
        panel_review=panel_review,
        mechanism_v3_schema=mechanism_schema,
        atlas3_kernel=atlas3,
        atlas10_kernel=atlas10,
        basis_inputs=basis_inputs,
    )


def verify(report: dict[str, Any]) -> dict[str, Any]:
    spec = _load(SPEC_PATH)
    return validate_state_probe(
        report,
        spec=spec,
        candidate_spec=_load(CANDIDATE_SPEC_PATH),
        panel_review=_load(PANEL_REVIEW_PATH),
        mechanism_v3_schema=_load(MECHANISM_V3_SCHEMA_PATH),
        atlas3_kernel=_load(ATLAS3_KERNEL_PATH),
        atlas10_kernel=_load(ATLAS10_KERNEL_PATH),
        basis_inputs={
            name: file_sha256(path) for name, path in sorted(INPUT_PATHS.items())
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the committed report is byte-current",
    )
    args = parser.parse_args()

    expected = build()
    payload = canonical_json_bytes(expected)
    if args.check:
        if not REPORT_PATH.is_file():
            raise SystemExit(f"missing generated report: {REPORT_PATH}")
        if REPORT_PATH.read_bytes() != payload:
            raise SystemExit("Atlas-50 state probe report is stale")
        summary = verify(_load(REPORT_PATH))
        print(json.dumps(summary, sort_keys=True))
        return 0

    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_bytes(payload)
    summary = verify(expected)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
