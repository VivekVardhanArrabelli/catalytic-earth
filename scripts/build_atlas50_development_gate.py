"""Build/check scoped computational development permissions from pinned reviews."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas50_development_gate import DIRECTORY, build_development_status, canonical_bytes
from catalytic_earth.atlas_draft_batch import BATCHES, resolve_batch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--batch", choices=sorted(BATCHES), default="default")
    args = parser.parse_args()
    batch = resolve_batch(args.batch)
    result = build_development_status(ROOT, batch=batch)
    output = ROOT / batch.status_path
    raw = canonical_bytes(result)
    if args.check:
        if not output.exists() or output.read_bytes() != raw:
            raise SystemExit("computational development status differs; review inputs/resolutions first")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw)
    print("Computational development open for declared scopes; human validation remains unclaimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
