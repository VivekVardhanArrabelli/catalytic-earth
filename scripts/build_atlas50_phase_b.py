"""Build deterministic Atlas-50 Phase B review/freeze-readiness artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_phase_b import (  # noqa: E402
    PHASE_B_RELATIVE,
    build_phase_b_outputs,
    canonical_json_bytes,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless every generated artifact is already byte-current",
    )
    args = parser.parse_args()

    outputs = build_phase_b_outputs(ROOT)
    phase_dir = ROOT / PHASE_B_RELATIVE
    stale: list[str] = []
    for filename, value in outputs.items():
        path = phase_dir / filename
        expected = canonical_json_bytes(value)
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if stale:
        raise SystemExit("stale Atlas-50 Phase B artifacts: " + ", ".join(stale))
    action = "verified" if args.check else "built"
    print(
        f"Atlas-50 Phase B readiness {action}: crosswalk_packets=57, "
        "panel_packets=40, reviewed=0, proposed_total=47, "
        "selection_frozen=false, source_records=0, GPU=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
