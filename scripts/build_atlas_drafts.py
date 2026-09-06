"""Compile offline source drafts and their wheel assets, or check exact bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas_drafts import build_source_drafts, validate_source_drafts
from catalytic_earth.atlas_draft_batch import BATCHES, DEFAULT_BATCH, resolve_batch


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--batch", choices=sorted(BATCHES), default="default")
    args = parser.parse_args()
    batch = resolve_batch(args.batch)
    bundle = build_source_drafts(ROOT, batch=batch)
    summary = validate_source_drafts(bundle)
    payload = canonical_bytes(bundle)
    attribution = (ROOT / batch.attribution_path).read_bytes()
    expected = canonical_bytes({
        "schema_version": "catalytic-earth.source-drafts-package.v1",
        "bundle_sha256": hashlib.sha256(payload).hexdigest(),
        "attribution_sha256": hashlib.sha256(attribution).hexdigest(),
    })
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    outputs = {
        batch.records_path.as_posix(): payload,
        f"src/catalytic_earth/draft_data/{stem}.json": payload,
        f"src/catalytic_earth/draft_data/{stem}_expected.json": expected,
        f"src/catalytic_earth/draft_data/{stem}_attribution.md": attribution,
    }
    for relative, raw in outputs.items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != raw:
                raise SystemExit(f"source draft output is stale: {relative}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
