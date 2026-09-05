"""Build/check scoped computational development permissions from pinned reviews."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas50_development_gate import DIRECTORY, build_development_status, canonical_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build_development_status(ROOT)
    output = ROOT / DIRECTORY / "status.json"
    raw = canonical_bytes(result)
    if args.check:
        if not output.exists() or output.read_bytes() != raw:
            raise SystemExit("computational development status differs; review inputs/resolutions first")
    else:
        output.write_bytes(raw)
    print("Computational development open for declared scopes; human validation remains unclaimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
