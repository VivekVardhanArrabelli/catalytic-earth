"""Freeze Atlas-10 relationship-query expectations and packaged runtime assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ATLAS_ROOT = ROOT / "data/atlas/atlas10"
KERNEL_PATH = ATLAS_ROOT / "kernel.json"
INHERITED_KERNEL_PATH = ROOT / "data/atlas/atlas3/kernel.json"
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
ATTRIBUTION_PATH = ATLAS_ROOT / "SOURCE_ATTRIBUTION.md"
EXPECTED_PATH = ATLAS_ROOT / "queries/runtime_expected.json"
QUERY_PATHS = {
    "atlas10.query.convergent-strategy": ATLAS_ROOT / "queries/convergent_strategy.sql",
    "atlas10.query.shared-fold-divergent-chemistry": (
        ATLAS_ROOT / "queries/shared_fold_divergent_chemistry.sql"
    ),
}
PACKAGE_ROOT = ROOT / "src/catalytic_earth/atlas_data"
PACKAGE_KERNEL_PATH = PACKAGE_ROOT / "atlas10_kernel.json"
PACKAGE_EXPECTED_PATH = PACKAGE_ROOT / "atlas10_runtime_expected.json"
PACKAGE_ATTRIBUTION_PATH = PACKAGE_ROOT / "ATLAS10_SOURCE_ATTRIBUTION.md"
PACKAGE_QUERY_PATHS = {
    "atlas10.query.convergent-strategy": PACKAGE_ROOT / "atlas10_convergent_strategy.sql",
    "atlas10.query.shared-fold-divergent-chemistry": (
        PACKAGE_ROOT / "atlas10_shared_fold_divergent_chemistry.sql"
    ),
}
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_kernel import (  # noqa: E402
    build_atlas10_runtime_result,
    canonical_sha256,
    validate_atlas10_kernel,
)
from catalytic_earth.atlas10_selection import load_atlas10_selection  # noqa: E402
from catalytic_earth.atlas10_sources import load_atlas10_source_manifest  # noqa: E402


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _normalized_text(path: Path) -> str:
    value = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return value if value.endswith("\n") else value + "\n"


def build_expected(
    kernel: dict[str, Any], inherited_kernel: dict[str, Any], queries: dict[str, str]
) -> dict[str, Any]:
    runtime = build_atlas10_runtime_result(kernel, inherited_kernel, queries)
    return {
        "schema_version": "catalytic-earth.atlas10-expected.v1",
        "kernel_sha256": runtime["kernel_sha256"],
        "inherited_kernel_sha256": runtime["inherited_kernel_sha256"],
        "query_sha256": runtime["query_sha256"],
        "runtime_result_sha256": canonical_sha256(runtime),
        "relationship_query_results": runtime["relationship_query_results"],
        "what_it_claims": runtime["what_it_claims"],
        "what_it_does_not_claim": runtime["what_it_does_not_claim"],
    }


def _outputs() -> dict[Path, bytes]:
    selection = load_atlas10_selection(SELECTION_PATH)
    manifest = load_atlas10_source_manifest(
        MANIFEST_PATH, repo_root=ROOT, selection=selection
    )
    kernel = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))
    inherited_kernel = json.loads(INHERITED_KERNEL_PATH.read_text(encoding="utf-8"))
    validate_atlas10_kernel(
        kernel,
        selection=selection,
        source_manifest=manifest,
        inherited_kernel=inherited_kernel,
    )
    queries = {query_id: _normalized_text(path) for query_id, path in QUERY_PATHS.items()}
    expected = build_expected(kernel, inherited_kernel, queries)
    kernel_bytes = _json_bytes(kernel)
    expected_bytes = _json_bytes(expected)
    attribution_bytes = _normalized_text(ATTRIBUTION_PATH).encode("utf-8")
    outputs = {
        EXPECTED_PATH: expected_bytes,
        PACKAGE_KERNEL_PATH: kernel_bytes,
        PACKAGE_EXPECTED_PATH: expected_bytes,
        PACKAGE_ATTRIBUTION_PATH: attribution_bytes,
    }
    outputs.update(
        {
            PACKAGE_QUERY_PATHS[query_id]: sql.encode("utf-8")
            for query_id, sql in queries.items()
        }
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = _outputs()
    if args.check:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, expected in outputs.items()
            if not path.is_file() or path.read_bytes() != expected
        ]
        if stale:
            raise SystemExit(f"Atlas-10 runtime outputs are stale: {stale}")
        print("Atlas-10 runtime outputs are current")
        return 0
    for path, raw in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    expected = json.loads(outputs[EXPECTED_PATH])
    print(
        json.dumps(
            {
                "runtime_result_sha256": expected["runtime_result_sha256"],
                "query_row_counts": {
                    query_id: len(rows)
                    for query_id, rows in expected["relationship_query_results"].items()
                },
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
