"""Small, wheel-installed, deterministic Catalytic Earth core command."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from importlib.resources import files
from pathlib import Path
from typing import Any, Sequence

from .atlas10_kernel import build_atlas10_runtime_result
from .atlas_kernel import build_atlas3_runtime_result, canonical_sha256
from .schema import MechanismRecord, SCHEMA_VERSION


GOLDEN_INPUT = "release_data/golden_input_v1.json"
GOLDEN_EXPECTED = "release_data/golden_expected_v1.json"
ATLAS3_KERNEL = "atlas_data/atlas3_kernel.json"
ATLAS3_QUERY = "atlas_data/case_truth_summary.sql"
ATLAS3_EXPECTED = "atlas_data/case_truth_summary_expected.json"
ATLAS10_KERNEL = "atlas_data/atlas10_kernel.json"
ATLAS10_CONVERGENT_QUERY = "atlas_data/atlas10_convergent_strategy.sql"
ATLAS10_DIVERGENT_QUERY = "atlas_data/atlas10_shared_fold_divergent_chemistry.sql"
ATLAS10_EXPECTED = "atlas_data/atlas10_runtime_expected.json"


def _resource_bytes(relative_path: str) -> bytes:
    return files("catalytic_earth").joinpath(relative_path).read_bytes()


def _canonical_sha(value: Any) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_golden_result() -> dict[str, Any]:
    raw = _resource_bytes(GOLDEN_INPUT)
    payload = json.loads(raw)
    if payload.get("schema_version") != "catalytic-earth.golden-input.v1":
        raise ValueError("unsupported golden input schema")
    records = [MechanismRecord.from_dict(row) for row in payload.get("records", [])]
    if not records or not all(record.fixture_only for record in records):
        raise ValueError("golden input must contain fixture-only records")
    record_ids = [record.record_id for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("golden input record IDs must be unique")
    result = {
        "schema_version": "catalytic-earth.golden-result.v1",
        "mechanism_record_schema": SCHEMA_VERSION,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "record_count": len(records),
        "record_ids": sorted(record_ids),
        "object_type_counts": dict(sorted(Counter(r.object_type for r in records).items())),
        "evidence_tier_counts": dict(
            sorted(Counter(str(r.evidence_tier) for r in records).items())
        ),
        "negative_observation_count": sum(
            r.object_type == "experimental_observation" and r.outcome == "negative"
            for r in records
        ),
        "fixture_only": True,
        "seed": 0,
        "network_used": False,
        "external_binary_used": False,
        "accelerator_used": False,
    }
    return result


def verified_golden_result() -> dict[str, Any]:
    result = build_golden_result()
    expected = json.loads(_resource_bytes(GOLDEN_EXPECTED))
    digest = _canonical_sha(result)
    expected_digest = expected.get("result_sha256")
    if digest != expected_digest:
        raise ValueError(
            f"golden result hash mismatch: expected {expected_digest}, computed {digest}"
        )
    return {
        **result,
        "result_sha256": digest,
        "matches_expected": True,
        "what_it_claims": expected["what_it_claims"],
        "what_it_does_not_claim": expected["what_it_does_not_claim"],
    }


def verified_atlas3_result() -> dict[str, Any]:
    """Reproduce the first biological kernel and its local truth-boundary query."""
    kernel = json.loads(_resource_bytes(ATLAS3_KERNEL))
    query_sql = _resource_bytes(ATLAS3_QUERY).decode("utf-8")
    expected = json.loads(_resource_bytes(ATLAS3_EXPECTED))
    result = build_atlas3_runtime_result(kernel, query_sql)
    digest = canonical_sha256(result)
    checks = {
        "kernel_sha256": result["kernel_sha256"],
        "query_sha256": result["query_sha256"],
        "runtime_result_sha256": digest,
        "query_rows": result["query_rows"],
    }
    if any(expected.get(field) != value for field, value in checks.items()):
        raise ValueError("Atlas-3 kernel/query result differs from the packaged expectation")
    return {
        **result,
        "runtime_result_sha256": digest,
        "matches_expected": True,
        "what_it_claims": expected["what_it_claims"],
        "what_it_does_not_claim": expected["what_it_does_not_claim"],
    }


def verified_atlas10_result() -> dict[str, Any]:
    """Reproduce the immutable Atlas-3 plus seven-case Atlas-10 query surface."""
    inherited_kernel = json.loads(_resource_bytes(ATLAS3_KERNEL))
    kernel = json.loads(_resource_bytes(ATLAS10_KERNEL))
    queries = {
        "atlas10.query.convergent-strategy": _resource_bytes(
            ATLAS10_CONVERGENT_QUERY
        ).decode("utf-8"),
        "atlas10.query.shared-fold-divergent-chemistry": _resource_bytes(
            ATLAS10_DIVERGENT_QUERY
        ).decode("utf-8"),
    }
    expected = json.loads(_resource_bytes(ATLAS10_EXPECTED))
    result = build_atlas10_runtime_result(kernel, inherited_kernel, queries)
    digest = canonical_sha256(result)
    checks = {
        "kernel_sha256": result["kernel_sha256"],
        "inherited_kernel_sha256": result["inherited_kernel_sha256"],
        "query_sha256": result["query_sha256"],
        "runtime_result_sha256": digest,
        "relationship_query_results": result["relationship_query_results"],
    }
    if any(expected.get(field) != value for field, value in checks.items()):
        raise ValueError("Atlas-10 kernel/query result differs from the packaged expectation")
    return {
        **result,
        "runtime_result_sha256": digest,
        "matches_expected": True,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalytic-earth",
        description="Deterministic, dependency-free Catalytic Earth core",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    reproduce = subparsers.add_parser(
        "reproduce", help="reproduce and verify the canonical fixture result"
    )
    reproduce.add_argument("--output", type=Path, help="optional JSON output path")
    atlas3 = subparsers.add_parser(
        "atlas3", help="reproduce the first three-case biological Atlas kernel"
    )
    atlas3.add_argument("--output", type=Path, help="optional JSON output path")
    atlas10 = subparsers.add_parser(
        "atlas10", help="reproduce the ten-case Atlas relationship-query surface"
    )
    atlas10.add_argument("--output", type=Path, help="optional JSON output path")
    subparsers.add_parser("claims", help="print the exact golden-result claim boundary")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "reproduce":
        result = verified_golden_result()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas3":
        result = verified_atlas3_result()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas10":
        result = verified_atlas10_result()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "claims":
        expected = json.loads(_resource_bytes(GOLDEN_EXPECTED))
        print(expected["what_it_claims"])
        print(expected["what_it_does_not_claim"])
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
