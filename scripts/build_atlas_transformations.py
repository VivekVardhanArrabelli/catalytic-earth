"""Package reviewed state transformations for dependency-free offline queries."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas_transformations import validate_transformations


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = ROOT / "data/atlas/transformations/m0187"
    value = json.loads((source / "transformations.json").read_text(encoding="utf-8"))
    atlas10 = json.loads((ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json").read_text(encoding="utf-8"))
    summary = validate_transformations(value, atlas10_bundle=atlas10, repo_root=ROOT)
    raw = canonical_bytes(value)
    attribution = (source / "SOURCE_ATTRIBUTION.md").read_bytes()
    expected = {
        "schema_version": "catalytic-earth.transformation-package.v1",
        "transformations_sha256": hashlib.sha256(raw).hexdigest(),
        "attribution_sha256": hashlib.sha256(attribution).hexdigest(),
    }
    outputs = {
        "transformations.json": raw,
        "attribution.md": attribution,
        "expected.json": canonical_bytes(expected),
    }
    for name, content in outputs.items():
        path = ROOT / "src/catalytic_earth/transformation_data" / name
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                raise SystemExit(f"transformation output is stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
