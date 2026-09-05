#!/usr/bin/env python3
"""Build or byte-check the computationally provisional Atlas-50 crosswalk v2."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_crosswalk_v2 import (  # noqa: E402
    OUTPUT_RELATIVE,
    build_crosswalk_v2_outputs,
    canonical_json_bytes,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless every generated v2 artifact is byte-current",
    )
    args = parser.parse_args()

    outputs = build_crosswalk_v2_outputs(ROOT)
    output_dir = ROOT / OUTPUT_RELATIVE
    stale: list[str] = []
    for filename, value in outputs.items():
        path = output_dir / filename
        expected = canonical_json_bytes(value)
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if stale:
        raise SystemExit("stale Atlas-50 crosswalk v2 artifacts: " + ", ".join(stale))

    crosswalk = outputs["crosswalk.json"]
    action = "verified" if args.check else "built"
    counts = crosswalk["classification_counts"]
    print(
        f"Atlas-50 crosswalk v2 {action}: rows={crosswalk['row_count']}, "
        f"provisional={crosswalk['row_count'] - counts['unresolved']}, "
        f"unresolved={counts['unresolved']}, human_review=0, experimental=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
