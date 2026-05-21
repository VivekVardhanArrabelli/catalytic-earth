#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE_ID = "epk_policy_harness"
DEFAULT_PREFIX = "epk_fresh_adp_chemcomp_pagination_continuation_synthesis"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def timestamp_slug(timestamp: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "", timestamp)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def rel(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def surface_summary(
    root: Path,
    *,
    surface_path: Path,
    tranche_path: Path,
    result_path: Path,
) -> dict[str, Any]:
    surface = load_json(surface_path)
    tranche = load_json(tranche_path)
    result = load_json(result_path)
    surface_meta = surface.get("metadata", {})
    tranche_meta = tranche.get("metadata", {})
    result_meta = result.get("metadata", {})

    require(surface_meta.get("lane_id") == LANE_ID, f"{surface_path} wrong lane")
    require(tranche_meta.get("lane_id") == LANE_ID, f"{tranche_path} wrong lane")
    require(surface_meta.get("review_only") is True, f"{surface_path} not review-only")
    require(tranche_meta.get("review_only") is True, f"{tranche_path} not review-only")
    require(result_meta.get("review_only") is True, f"{result_path} not review-only")
    require(
        surface_meta.get("query_mode") == "chemcomp",
        f"{surface_path} is not a chemcomp surface",
    )
    require(
        tranche_meta.get("source_query_mode") == "chemcomp",
        f"{tranche_path} is not a chemcomp tranche",
    )
    require(
        tranche_meta.get("chem_comp_id") == "ADP",
        f"{tranche_path} is not an ADP continuation tranche",
    )
    require(
        surface_meta.get("candidate_ids_frozen_before_local_feature_review") is True,
        f"{surface_path} did not freeze candidate ids before local review",
    )
    require(
        surface_meta.get("source_free_local_features_computed_before_source_validation")
        is True,
        f"{surface_path} local features were not source-free before validation",
    )
    require(
        surface_meta.get("source_validation_review_only") is True,
        f"{surface_path} source validation is not review-only",
    )
    require(
        surface_meta.get("raw_coordinate_dump_written") is False,
        f"{surface_path} wrote raw coordinate dumps",
    )
    require(
        tranche_meta.get("raw_coordinate_dump_written") is False,
        f"{tranche_path} wrote raw coordinate dumps",
    )
    require(
        surface_meta.get("production_claim_allowed") is False
        and tranche_meta.get("production_claim_allowed") is False
        and result_meta.get("production_claim_allowed") is False,
        "production claim flag must stay false",
    )
    require(
        surface_meta.get("labels_or_fingerprints_changed") is False
        and tranche_meta.get("labels_or_fingerprints_changed") is False
        and result_meta.get("labels_or_fingerprints_changed") is False,
        "labels/fingerprints must stay unchanged",
    )
    require(
        result_meta.get("adp_product_query_context_tripwire_contract_enforced") is True,
        f"{result_path} did not enforce the ADP query-context tripwire",
    )
    require(
        result_meta.get("expected_decision_mismatch_count") == 0,
        f"{result_path} has expected-decision mismatches",
    )
    require(
        result_meta.get("counterexamples_found") == [],
        f"{result_path} found counterexamples",
    )
    require(
        result_meta.get("decision_counts") == {"review_only_abstain": len(tranche["rows"])},
        f"{result_path} did not abstain for every row",
    )
    for row in tranche.get("rows", []):
        require(row.get("ligand_context") == "ADP", f"{tranche_path} has non-ADP row")
        require(
            row.get("product_state_context") is True,
            f"{tranche_path} row lacks product-state context",
        )
        require(
            row.get("source_query_used_for_predictive_feature") is False,
            f"{tranche_path} row leaks source query",
        )
        require(
            row.get("source_validation_used_for_predictive_feature") is False,
            f"{tranche_path} row leaks source validation",
        )
        require(
            row.get("candidate_specific_source_repair") is False,
            f"{tranche_path} admits candidate-specific repair",
        )

    return {
        "surface": rel(surface_path, root),
        "surface_sha256": sha256_file(surface_path),
        "tranche": rel(tranche_path, root),
        "tranche_sha256": sha256_file(tranche_path),
        "result": rel(result_path, root),
        "result_sha256": sha256_file(result_path),
        "query_rows_requested": surface_meta.get("query_rows_requested"),
        "candidate_ids_reviewed": surface_meta.get("candidate_ids_reviewed", []),
        "candidate_count_reviewed": surface_meta.get("fresh_candidate_count_reviewed"),
        "adp_materialized_candidate_count": surface_meta.get(
            "adp_materialized_candidate_count"
        ),
        "adp_product_local_geometry_like_candidate_count": surface_meta.get(
            "adp_product_local_geometry_like_candidate_count"
        ),
        "fetch_failure_count": surface_meta.get("fetch_failure_count"),
        "tranche_row_count": len(tranche.get("rows", [])),
        "decision_counts": result_meta.get("decision_counts"),
        "primary_outcome": result_meta.get("primary_outcome"),
        "expected_decision_mismatch_count": result_meta.get(
            "expected_decision_mismatch_count"
        ),
        "counterexamples_found": result_meta.get("counterexamples_found", []),
        "raw_coordinate_dump_written": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
    }


def build_synthesis(args: argparse.Namespace) -> Path:
    root = Path(args.root).resolve()
    surfaces = [Path(path).resolve() for path in args.surface]
    tranches = [Path(path).resolve() for path in args.tranche]
    results = [Path(path).resolve() for path in args.result]
    require(surfaces, "at least one surface is required")
    require(
        len(surfaces) == len(tranches) == len(results),
        "surface, tranche, and result counts must match",
    )

    summaries = [
        surface_summary(
            root,
            surface_path=surface_path,
            tranche_path=tranche_path,
            result_path=result_path,
        )
        for surface_path, tranche_path, result_path in zip(surfaces, tranches, results)
    ]

    query_rows = [int(summary["query_rows_requested"]) for summary in summaries]
    require(query_rows == sorted(query_rows), "query row windows must be monotone")
    require(
        len(set(query_rows)) == len(query_rows),
        "query row windows must be distinct continuation windows",
    )

    all_ids: list[str] = []
    duplicated_ids: list[str] = []
    seen: set[str] = set()
    for summary in summaries:
        for pdb_id in summary["candidate_ids_reviewed"]:
            cleaned = str(pdb_id).upper()
            if cleaned in seen:
                duplicated_ids.append(cleaned)
            seen.add(cleaned)
            all_ids.append(cleaned)
    require(not duplicated_ids, f"duplicate candidate IDs: {sorted(duplicated_ids)}")

    decision_counts: Counter[str] = Counter()
    for summary in summaries:
        decision_counts.update(summary.get("decision_counts") or {})

    rows_reviewed = sum(int(summary["tranche_row_count"]) for summary in summaries)
    materialized_count = sum(
        int(summary["adp_materialized_candidate_count"]) for summary in summaries
    )
    geometry_like_count = sum(
        int(summary["adp_product_local_geometry_like_candidate_count"])
        for summary in summaries
    )
    candidate_count = sum(
        int(summary["candidate_count_reviewed"]) for summary in summaries
    )

    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    output_path = artifact_dir / f"{args.output_prefix}_{timestamp_slug(args.timestamp)}.json"
    payload = {
        "metadata": {
            "artifact_id": f"{args.output_prefix}_{timestamp_slug(args.timestamp)}",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "policy_version": "epk_review_only_policy_harness_v0_20260520",
            "hypothesis": (
                "Fresh ADP chem-comp pagination remains falsifiable only if every "
                "coordinate-materialized ADP/product-state row stays review-only "
                "and query/source context cannot become predictive across "
                "continuation windows."
            ),
            "surface_count": len(summaries),
            "candidate_count_reviewed": candidate_count,
            "unique_candidate_count_reviewed": len(seen),
            "adp_materialized_candidate_count": materialized_count,
            "adp_product_local_geometry_like_candidate_count": geometry_like_count,
            "rows_reviewed_by_policy_harness": rows_reviewed,
            "decision_counts": dict(sorted(decision_counts.items())),
            "expected_decision_mismatch_count": sum(
                int(summary["expected_decision_mismatch_count"])
                for summary in summaries
            ),
            "counterexamples_found": [
                counterexample
                for summary in summaries
                for counterexample in summary.get("counterexamples_found", [])
            ],
            "query_rows_requested_windows": query_rows,
            "candidate_ids_disjoint_across_surfaces": True,
            "candidate_ids_frozen_before_local_feature_review": True,
            "source_text_and_query_review_only": True,
            "adp_product_state_rows_review_only": True,
            "future_policy_activation_allowed": False,
            "search_surface_exhausted": False,
            "primary_outcome": "policy_frozen_review_only",
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "surfaces": summaries,
        "candidate_ids_reviewed": all_ids,
    }
    write_json(output_path, payload)
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Synthesize and validate frozen review-only ADP chem-comp pagination "
            "continuation surfaces."
        )
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--surface", action="append", required=True)
    parser.add_argument("--tranche", action="append", required=True)
    parser.add_argument("--result", action="append", required=True)
    parser.add_argument("--output-prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    output_path = build_synthesis(args)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
