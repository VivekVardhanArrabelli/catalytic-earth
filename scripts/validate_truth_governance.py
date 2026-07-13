from __future__ import annotations

from pathlib import Path

from catalytic_earth.truth_guard import validate_truth_governance


def main() -> int:
    result = validate_truth_governance(Path("."))
    print(
        "Validated truth governance: "
        f"{result['claims']} claims, {result['exposure_events']} exposure events, "
        f"{result['exposure_surfaces']} surfaces, "
        f"freeze_active={bool(result['expansion_freeze_active'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
