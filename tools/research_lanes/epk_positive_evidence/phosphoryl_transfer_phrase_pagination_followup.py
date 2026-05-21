#!/usr/bin/env python3
"""Bounded RCSB phrase-pagination follow-up for ePK positive evidence.

This review-only helper targets phrase surfaces that were either only partly
paged in prior lane artifacts or use narrower substrate-trapping/nonhydrolyzable
ATP language. It fetches coordinates transiently, writes compact summaries only,
and does not create labels, scores, thresholds, fingerprints, migrations, or
production claims.
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import current_release_epk_followup as current


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
PDB_ID_RE = re.compile(r"^[0-9][A-Za-z0-9]{3}$")


@dataclass(frozen=True)
class PhraseSurface:
    surface_id: str
    query: str
    rows: int
    start: int = 0
    rationale: str = ""


DEFAULT_SURFACES = [
    PhraseSurface(
        "transition_state_pdb_phosphorylation_rows51_98",
        "kinase substrate transition state PDB phosphorylation",
        50,
        50,
        "Completes the previously first-50-only transition-state phrase page.",
    ),
    PhraseSurface(
        "phosphoryl_transfer_complex_rows101_200",
        "kinase substrate complex phosphoryl transfer",
        100,
        100,
        "Pages the prior broad phosphoryl-transfer phrase surface beyond the first 100 rows.",
    ),
    PhraseSurface(
        "phosphoryl_transfer_complex_rows201_298",
        "kinase substrate complex phosphoryl transfer",
        100,
        200,
        "Completes the bounded tail of the prior broad phosphoryl-transfer phrase surface.",
    ),
    PhraseSurface(
        "protein_kinase_nonhydrolyzable_atp_substrate",
        "protein kinase nonhydrolyzable ATP substrate",
        80,
        0,
        "Targets source wording for ATP analog states without relying on ligand aliases.",
    ),
    PhraseSurface(
        "protein_kinase_substrate_trapping_atp",
        "protein kinase substrate trapping ATP",
        80,
        0,
        "Targets substrate-trapping language that can describe Michaelis-like complexes.",
    ),
    PhraseSurface(
        "protein_kinase_precatalytic_substrate_atp",
        "protein kinase pre-catalytic substrate ATP",
        80,
        0,
        "Targets precatalytic wording not covered by current-release exact-ligand surfaces.",
    ),
    PhraseSurface(
        "protein_kinase_substrate_bound_amp_pnp",
        "protein kinase substrate-bound AMP-PNP",
        80,
        0,
        "Targets hyphenated substrate-bound AMP-PNP wording.",
    ),
]


def search_surface(surface: PhraseSurface) -> dict[str, Any]:
    payload = {
        "query": current.full_text(surface.query),
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": surface.start, "rows": surface.rows},
            "results_content_type": ["experimental"],
        },
    }
    result = current.fetch_json(current.RCSB_SEARCH_URL, payload=payload)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    return {
        "surface_id": surface.surface_id,
        "query_or_source": f"RCSB full_text: {surface.query}",
        "rationale": surface.rationale,
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def collect_prior_pdb_ids(artifacts_dir: Path, out: Path) -> dict[str, list[str]]:
    prior: dict[str, list[str]] = {}

    def add(pdb_id: Any, source: Path) -> None:
        if not isinstance(pdb_id, str):
            return
        token = pdb_id.upper()
        if PDB_ID_RE.match(token):
            prior.setdefault(token, []).append(str(source))

    def walk(value: Any, source: Path) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key == "pdb_id":
                    add(nested, source)
                elif key == "pdb_ids" and isinstance(nested, list):
                    for item in nested:
                        add(item, source)
                else:
                    walk(nested, source)
        elif isinstance(value, list):
            for nested in value:
                walk(nested, source)

    for path in sorted(artifacts_dir.glob("*.json")):
        if path.resolve() == out.resolve():
            continue
        try:
            payload = json.loads(path.read_text())
        except Exception:  # noqa: BLE001 - prior artifact indexing is auxiliary.
            continue
        walk(payload, path)
    return prior


def fresh_status(row: dict[str, Any], prior_pdb_ids: dict[str, list[str]]) -> None:
    pdb_id = row["pdb_id"]
    row["prior_lane_artifact_seen"] = pdb_id in prior_pdb_ids
    row["prior_lane_artifact_sources_sample"] = prior_pdb_ids.get(pdb_id, [])[:5]


def cif_content_length(pdb_id: str, timeout: int = 15) -> int | None:
    request = urllib.request.Request(
        current.scout.RCSB_CIF_URL.format(pdb_id=pdb_id),
        method="HEAD",
        headers={"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            header = response.headers.get("Content-Length")
    except Exception:  # noqa: BLE001 - size guard is best effort.
        return None
    if not header:
        return None
    try:
        return int(header)
    except ValueError:
        return None


class RowTimeoutError(TimeoutError):
    pass


def _timeout_handler(_signum: int, _frame: Any) -> None:
    raise RowTimeoutError("row scan exceeded per-row timeout")


def scan_pdb_id_guarded(
    pdb_id: str,
    search_hits: list[dict[str, Any]],
    max_cif_bytes: int,
    row_timeout_seconds: int,
) -> dict[str, Any]:
    cif_size = cif_content_length(pdb_id)
    if cif_size is not None and cif_size > max_cif_bytes:
        return {
            "pdb_id": pdb_id,
            "search_hits": search_hits,
            "candidate_status": "cif_too_large_skipped_review_only",
            "cif_content_length_bytes": cif_size,
            "max_cif_bytes": max_cif_bytes,
            "review_only": True,
            "countable_label_candidate": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
        }
    previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(row_timeout_seconds)
    try:
        row = current.scan_pdb_id(pdb_id, search_hits)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)
    if cif_size is not None:
        row["cif_content_length_bytes"] = cif_size
    return row


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    max_unique_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
) -> dict[str, Any]:
    generated_at = current.now_iso()
    prior_pdb_ids = collect_prior_pdb_ids(artifacts_dir, out)
    search_surfaces = []
    seen: dict[str, list[dict[str, Any]]] = {}

    for surface in DEFAULT_SURFACES:
        result = search_surface(surface)
        search_surfaces.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1 + surface.start):
            if pdb_id not in seen and len(seen) >= max_unique_pdb_ids:
                continue
            seen.setdefault(pdb_id, []).append(
                {
                    "surface_id": result["surface_id"],
                    "rank": rank,
                    "query_or_source": result["query_or_source"],
                    "rationale": result["rationale"],
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    for pdb_id, search_hits in seen.items():
        try:
            row = scan_pdb_id_guarded(pdb_id, search_hits, max_cif_bytes, row_timeout_seconds)
            fresh_status(row, prior_pdb_ids)
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            row = {
                "pdb_id": pdb_id,
                "search_hits": search_hits,
                "candidate_status": "fetch_or_parse_failed_review_only",
                "fetch_error": repr(exc),
                "review_only": True,
                "countable_label_candidate": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "epk_score_computed": False,
                "ready_for_production_scoring": False,
                "ready_for_label_import": False,
                "target_family_id": TARGET_FAMILY_ID,
                "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            }
            fresh_status(row, prior_pdb_ids)
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(row)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    fresh_status_counts: dict[str, int] = {}
    for row in rows:
        status = row["candidate_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        if not row.get("prior_lane_artifact_seen"):
            fresh_status_counts[status] = fresh_status_counts.get(status, 0) + 1

    nonpeptide = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_nonpeptide_candidate_source_validation_pending_review_only"
    ]
    short_or_peptide = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_peptide_or_short_candidate_review_only"
    ]
    fresh_nonpeptide = [row["pdb_id"] for row in rows if row["pdb_id"] in nonpeptide and not row["prior_lane_artifact_seen"]]
    fresh_short_or_peptide = [
        row["pdb_id"] for row in rows if row["pdb_id"] in short_or_peptide and not row["prior_lane_artifact_seen"]
    ]

    evidence_for = []
    if fresh_nonpeptide:
        evidence_for.append(
            "Fresh phrase-pagination local-metal non-peptide candidates requiring source adjudication: "
            + ", ".join(fresh_nonpeptide)
            + "."
        )
    if fresh_short_or_peptide:
        evidence_for.append(
            "Fresh phrase-pagination review-only short/peptide local-metal candidates: "
            + ", ".join(fresh_short_or_peptide)
            + "."
        )
    if not evidence_for and (nonpeptide or short_or_peptide):
        evidence_for.append(
            "Phrase-pagination recovered only prior lane local-metal candidates: "
            + ", ".join(sorted(set(nonpeptide + short_or_peptide)))
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Phrase-pagination surfaces returned structures but no local-metal ePK substrate candidate."
        )

    evidence_against = [
        "No clean folded-protein ePK transfer-state positive is promoted by this phrase-pagination scout.",
        "Fresh structures without local-metal non-peptide candidate geometry remain negative for the lane objective.",
    ]
    if fresh_nonpeptide:
        evidence_against.append(
            "Fresh local-metal non-peptide candidates are source-validation leads only, not production-positive evidence."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "phosphoryl_transfer_phrase_pagination_followup",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "search_surface_count": len(search_surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_surfaces),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_surfaces),
            "unique_pdb_ids_reviewed": len(rows),
            "fresh_unique_pdb_ids_reviewed": sum(1 for row in rows if not row.get("prior_lane_artifact_seen")),
            "fetch_failure_count": len(fetch_failures),
            "max_cif_bytes": max_cif_bytes,
            "row_timeout_seconds": row_timeout_seconds,
            "candidate_status_counts": status_counts,
            "fresh_candidate_status_counts": fresh_status_counts,
            "local_metal_nonpeptide_candidate_pdb_ids": nonpeptide,
            "local_metal_peptide_or_short_candidate_pdb_ids": short_or_peptide,
            "fresh_local_metal_nonpeptide_candidate_pdb_ids": fresh_nonpeptide,
            "fresh_local_metal_peptide_or_short_candidate_pdb_ids": fresh_short_or_peptide,
            "prior_lane_pdb_id_count": len(prior_pdb_ids),
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Phrase pagination/source discovery only. It does not create labels, scores, "
                "thresholds, fingerprints, migrations, or production claims."
            ),
            "source_urls": [
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_CIF_URL,
            ],
        },
        "search_surfaces": search_surfaces,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": (
                "next_query_defined"
                if fresh_nonpeptide
                else "evidence_for"
                if fresh_short_or_peptide
                else "search_surface_exhausted"
            ),
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(fresh_nonpeptide or fresh_short_or_peptide),
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "counterexamples_found": [],
            "recommendation": (
                "Source-map any fresh non-peptide local-metal candidate before upgrade; otherwise treat "
                "these paged phrase surfaces as exhausted for clean folded-protein ePK positives."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_positive_evidence"),
    )
    parser.add_argument("--max-unique-pdb-ids", type=int, default=140)
    parser.add_argument("--max-cif-bytes", type=int, default=25_000_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=45)
    parser.add_argument("--sleep-seconds", type=float, default=0.03)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.artifacts_dir,
        args.max_unique_pdb_ids,
        args.max_cif_bytes,
        args.row_timeout_seconds,
        args.sleep_seconds,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "fresh_unique_pdb_ids_reviewed": artifact["metadata"]["fresh_unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "fresh_candidate_status_counts": artifact["metadata"]["fresh_candidate_status_counts"],
                "fresh_local_metal_nonpeptide_candidate_pdb_ids": artifact["metadata"][
                    "fresh_local_metal_nonpeptide_candidate_pdb_ids"
                ],
                "fresh_local_metal_peptide_or_short_candidate_pdb_ids": artifact["metadata"][
                    "fresh_local_metal_peptide_or_short_candidate_pdb_ids"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
