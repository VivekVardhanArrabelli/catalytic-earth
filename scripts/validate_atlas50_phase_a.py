"""Validate the complete Atlas-50 Phase A precompilation package."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_phase_a import validate_phase_a_package  # noqa: E402


def main() -> int:
    summary = validate_phase_a_package(ROOT)
    print(
        "Atlas-50 Phase A contracts valid: "
        + ", ".join(f"{key}={value}" for key, value in summary.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
