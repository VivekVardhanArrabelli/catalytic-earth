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


def verified_source_drafts(batch_name: str = "default") -> dict[str, Any]:
    """Read the reviewed source projections without requiring a checkout or network."""
    from .atlas_drafts import validate_source_drafts
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    raw = _resource_bytes(f"draft_data/{stem}.json")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    attribution = _resource_bytes(f"draft_data/{stem}_attribution.md")
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if hashlib.sha256(raw).hexdigest() != expected.get("bundle_sha256"):
        raise ValueError("source draft package differs from its expected hash")
    if hashlib.sha256(attribution).hexdigest() != expected.get("attribution_sha256"):
        raise ValueError("source draft attribution differs from its expected hash")
    bundle = json.loads(raw)
    validate_source_drafts(bundle)
    return bundle


def _chebi_argument(value: str) -> str:
    from .atlas_draft_index import normalize_chebi_id

    try:
        return normalize_chebi_id(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def verified_primary_evidence(
    batch_name: str = "default", *, bundle: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load optional reviewed annotations separately from immutable source records."""
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch
    from .atlas_primary_evidence import validate_primary_evidence

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if "primary_evidence_sha256" not in expected:
        return None
    raw = _resource_bytes(f"draft_data/{stem}_primary_evidence.json")
    if hashlib.sha256(raw).hexdigest() != expected["primary_evidence_sha256"]:
        raise ValueError("primary evidence package differs from its expected hash")
    primary = json.loads(raw)
    validate_primary_evidence(
        primary, bundle=verified_source_drafts(batch_name) if bundle is None else bundle,
    )
    return primary


def build_parser() -> argparse.ArgumentParser:
    from .atlas_draft_batch import BATCHES

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
    drafts = subparsers.add_parser(
        "atlas-drafts", help="query source-scoped mechanisms, states and abstentions offline"
    )
    drafts.add_argument(
        "--batch", choices=sorted(BATCHES), default="default",
        help="select a separately reviewed source batch (default: original four records)",
    )
    drafts.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0107")
    drafts.add_argument("--assembly", help="filter the source-described assembly mode")
    drafts.add_argument("--text", help="search source chemistry and state descriptions")
    drafts.add_argument(
        "--participant", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require an exact source ChEBI participant on either side; repeat for AND",
    )
    drafts.add_argument(
        "--reactant", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require a ChEBI participant on the source's left side; repeat for AND",
    )
    drafts.add_argument(
        "--product", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require a ChEBI participant on the source's right side; repeat for AND",
    )
    drafts.add_argument("--steps", action="store_true", help="include source steps and electron flows")
    drafts.add_argument("--output", type=Path, help="optional JSON output path")
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
    if args.command == "atlas-drafts":
        from .atlas_draft_query import query_source_drafts

        bundle = verified_source_drafts(args.batch)
        result = query_source_drafts(
            bundle, mcsa_id=args.mcsa_id,
            assembly=args.assembly, text=args.text, include_steps=args.steps,
            participants=args.participant or (), reactants=args.reactant or (),
            products=args.product or (),
            primary_evidence=verified_primary_evidence(args.batch, bundle=bundle),
        )
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
