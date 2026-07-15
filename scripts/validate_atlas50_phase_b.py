"""Validate the Atlas-50 Phase B review/freeze-readiness package."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_phase_b import validate_phase_b_package  # noqa: E402


def main() -> int:
    summary = validate_phase_b_package(ROOT)
    print(
        "Atlas-50 Phase B readiness contracts valid: "
        + ", ".join(f"{key}={value}" for key, value in summary.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
