"""Build and package the reviewed Atlas structural-context projection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_structural_context import (  # noqa: E402
    load_and_build_structural_context,
)
from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402


SOURCE = ROOT / "data/atlas/structural_context"
PACKAGE = ROOT / "src/catalytic_earth/structural_context_data"
SPEC = SOURCE / "spec.json"
BUNDLE = SOURCE / "bundle.json"
ATLAS10 = ROOT / "data/atlas/atlas10/kernel.json"


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _write_or_check(path: Path, raw: bytes, *, check: bool, label: str) -> None:
    if check:
        if not path.is_file() or path.read_bytes() != raw:
            raise SystemExit(f"{label} is stale: {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def _source_text_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").encode("utf-8")


def _safe_source_path(relative: str) -> Path:
    candidate = Path(relative)
    _require(
        "\\" not in relative
        and not candidate.is_absolute()
        and "." not in candidate.parts
        and ".." not in candidate.parts,
        "structural-context source binding path is unsafe",
    )
    path = (ROOT / candidate).resolve()
    _require(ROOT in path.parents and path.is_file(), "structural-context source binding is missing")
    return path


def _validate_declared_bindings(value: object) -> int:
    checked = 0
    if isinstance(value, dict):
        if set(value) == {"path", "sha256"}:
            path = _safe_source_path(value["path"])
            _require(
                canonical_file_sha256(path) == value["sha256"],
                "structural-context declared source binding hash differs",
            )
            return 1
        for item in value.values():
            checked += _validate_declared_bindings(item)
    elif isinstance(value, list):
        for item in value:
            checked += _validate_declared_bindings(item)
    return checked


def _reviewed_assets(bundle_raw: bytes) -> dict[str, bytes]:
    files = {
        "spec.json": _source_text_bytes(SPEC),
        "bundle.json": bundle_raw,
        "attribution.md": _source_text_bytes(SOURCE / "SOURCE_ATTRIBUTION.md"),
        "acquisition_receipts.json": _source_text_bytes(
            SOURCE / "acquisition_receipts.json"
        ),
    }
    review_path = SOURCE / "review.json"
    _require(review_path.is_file(), "structural-context review.json is missing")
    review_raw = _source_text_bytes(review_path)
    review = json.loads(review_raw)
    _require(
        review.get("spec_sha256") == hashlib.sha256(files["spec.json"]).hexdigest()
        and review.get("bundle_sha256") == hashlib.sha256(files["bundle.json"]).hexdigest(),
        "structural-context source review is stale; review pins are never refreshed automatically",
    )
    files["review.json"] = review_raw
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    binding_count = _validate_declared_bindings(spec)
    _require(binding_count >= 3, "structural-context declared source bindings are incomplete")
    bundle = load_and_build_structural_context(SPEC, ATLAS10, ROOT)
    bundle_raw = canonical_bytes(bundle)
    _write_or_check(
        BUNDLE,
        bundle_raw,
        check=args.check,
        label="structural-context source bundle",
    )

    assets = _reviewed_assets(bundle_raw)
    expected = {
        "schema_version": "catalytic-earth.atlas-structural-context-package.v1",
        "files": {
            name: hashlib.sha256(raw).hexdigest()
            for name, raw in sorted(assets.items())
        },
    }
    assets["expected.json"] = canonical_bytes(expected)
    for name, raw in assets.items():
        _write_or_check(
            PACKAGE / name,
            raw,
            check=args.check,
            label="structural-context package output",
        )

    print(
        json.dumps(
            {
                "context_count": bundle["context_count"],
                "site_count": bundle["site_count"],
                "distance_pair_count": bundle["distance_pair_count"],
                "distance_measurement_count": bundle["distance_measurement_count"],
                "declared_source_binding_count": binding_count,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
