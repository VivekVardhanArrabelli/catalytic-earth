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
from catalytic_earth.atlas_transformation_query import TRANSFORMATION_SETS


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def build_set(key: str, atlas10: dict, *, check: bool) -> dict:
    spec = TRANSFORMATION_SETS[key]
    source = ROOT / spec["source_directory"]
    value = json.loads((source / "transformations.json").read_text(encoding="utf-8"))
    summary = validate_transformations(value, atlas10_bundle=atlas10, repo_root=ROOT)
    if any(row["record_binding"]["mcsa_id"] != key for row in value["transformations"]):
        raise ValueError("transformation set belongs to another source record")
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
        path = ROOT / "src/catalytic_earth/transformation_data" / (spec["package_prefix"] + name)
        if check:
            if not path.is_file() or path.read_bytes() != content:
                raise SystemExit(f"transformation output is stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mcsa-id", choices=sorted(TRANSFORMATION_SETS), help="build one reviewed set (default: all)")
    args = parser.parse_args()
    atlas10 = json.loads((ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json").read_text(encoding="utf-8"))
    keys = [args.mcsa_id] if args.mcsa_id else sorted(TRANSFORMATION_SETS)
    summaries = {key: build_set(key, atlas10, check=args.check) for key in keys}
    print(json.dumps(summaries, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
