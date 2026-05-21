#!/usr/bin/env python3
"""Source-published non-peptide substrate literature follow-up.

This bounded helper searches article metadata for full-length/folded protein
substrate phosphoacceptor language, maps compact article records to RCSB PDB
IDs by DOI/title/direct PDB token, and emits review-only candidate rows for
fresh mapped structures with plausible local geometry.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import current_release_epk_followup as current
import guarded_phrase_candidate_rows as guarded


LANE_ID = "epk_positive_evidence"
SCHEMA_VERSION = guarded.SCHEMA_VERSION
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
PDB_ID_RE = re.compile(r"\b[0-9][A-Za-z0-9]{3}\b")


@dataclass(frozen=True)
class LiteratureSurface:
    surface_id: str
    query: str
    page_size: int = 10


LITERATURE_SURFACES = [
    LiteratureSurface(
        "full_length_substrate_phosphorylation_site_pdb_2015_2026",
        '("protein kinase" AND "full-length substrate" AND "phosphorylation site" AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "protein_substrate_phosphoacceptor_transfer_analog_pdb_2015_2026",
        '("protein kinase" AND "protein substrate" AND phosphoacceptor AND '
        '("AMP-PNP" OR ATPgammaS OR "ATP-gamma-S" OR "metal fluoride") AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "kinase_substrate_complex_full_length_transfer_analog_pdb_2015_2026",
        '("kinase-substrate complex" AND "full-length" AND '
        '("AMP-PNP" OR ATPgammaS OR "metal fluoride") AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "folded_protein_substrate_phosphorylation_site_structure_2015_2026",
        '("folded protein substrate" AND kinase AND "phosphorylation site" AND structure) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "braf_mek_source_site_transfer_analog_pdb_2015_2026",
        '(BRAF AND MEK AND (Ser218 OR Ser222) AND (ATPgammaS OR "AMP-PNP" OR ATP) AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "mek_erk_source_site_transfer_analog_pdb_2015_2026",
        '(MEK AND ERK AND (Tyr204 OR Thr202 OR "activation loop") AND '
        '("AMP-PNP" OR ATPgammaS OR ATP) AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "pink1_ubiquitin_ser65_transfer_analog_pdb_2015_2026",
        '(PINK1 AND ubiquitin AND Ser65 AND ("AMP-PNP" OR ATPgammaS OR ATP) AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "limk1_cofilin_ser3_transfer_analog_pdb_2015_2026",
        '(LIMK1 AND cofilin AND Ser3 AND ("AMP-PNP" OR ATPgammaS OR ATP) AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
    LiteratureSurface(
        "cdk_activating_kinase_cdk_tloop_transfer_analog_pdb_2015_2026",
        '("CDK-activating kinase" AND CDK AND ("T-loop" OR Thr160 OR Thr161) AND '
        '("AMP-PNP" OR ATPgammaS OR ATP) AND PDB) '
        "AND FIRST_PDATE:[2015-01-01 TO 2026-12-31]",
    ),
]


def compact_pdb_tokens(text: str) -> list[str]:
    tokens = {match.upper() for match in PDB_ID_RE.findall(text)}
    return sorted(token for token in tokens if any(char.isalpha() for char in token))


def europepmc_search(surface: LiteratureSurface, date_from: str, date_to: str) -> dict[str, Any]:
    query = surface.query.replace("2015-01-01 TO 2026-12-31", f"{date_from} TO {date_to}")
    params = urllib.parse.urlencode(
        {
            "query": query,
            "format": "json",
            "pageSize": surface.page_size,
            "resultType": "core",
        }
    )
    source_url = f"{EUROPE_PMC_URL}?{params}"
    data = current.fetch_json(source_url, timeout=30)
    results = data.get("resultList", {}).get("result", [])
    articles = []
    for rank, row in enumerate(results, start=1):
        title = html.unescape(row.get("title") or "")
        abstract = html.unescape(row.get("abstractText") or "")
        text = f"{title} {abstract}"
        lower = text.lower()
        articles.append(
            {
                "rank": rank,
                "title": title,
                "doi": row.get("doi"),
                "pmid": row.get("pmid"),
                "pmcid": row.get("pmcid"),
                "pub_year": row.get("pubYear"),
                "journal": row.get("journalTitle"),
                "direct_pdb_ids_in_title_or_abstract": compact_pdb_tokens(text),
                "source_term_flags": {
                    "full_length": "full-length" in lower or "full length" in lower,
                    "protein_substrate": "protein substrate" in lower,
                    "phosphorylation_site": "phosphorylation site" in lower,
                    "phosphoacceptor": "phosphoacceptor" in lower,
                    "amp_pnp": "amp-pnp" in lower or "amppnp" in lower,
                    "atpgammas": "atpgammas" in lower or "atp-gamma-s" in lower,
                    "metal_fluoride": "metal fluoride" in lower,
                    "pdb": "pdb" in lower,
                },
            }
        )
    return {
        "surface_id": surface.surface_id,
        "query_or_source": f"Europe PMC: {query}",
        "source_url": source_url,
        "hit_count": data.get("hitCount"),
        "returned_count": len(articles),
        "articles": articles,
    }


def rcsb_maps_for_article(article: dict[str, Any]) -> list[dict[str, Any]]:
    maps = []
    doi = article.get("doi")
    title = article.get("title") or ""
    if doi:
        maps.append(current.rcsb_full_text_ids(str(doi), rows=20))
    if title:
        maps.append(current.rcsb_full_text_ids(title, rows=20))
    for pdb_id in article.get("direct_pdb_ids_in_title_or_abstract", []):
        maps.append(
            {
                "query_or_source": f"Europe PMC title/abstract direct PDB token: {pdb_id}",
                "returned_count": 1,
                "total_count": 1,
                "pdb_ids": [pdb_id],
            }
        )
    return maps


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    max_articles: int,
    max_unique_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
    include_prior_seen: bool,
    date_from: str,
    date_to: str,
) -> dict[str, Any]:
    generated_at = current.now_iso()
    prior_pdb_ids = guarded.collect_prior_pdb_ids(artifacts_dir, out)
    literature_surfaces = []
    article_records = []
    rcsb_maps_by_article = []
    seen_articles: set[tuple[str | None, str]] = set()
    seen_pdbs: dict[str, list[dict[str, Any]]] = {}
    skipped_prior_seen: dict[str, list[dict[str, Any]]] = {}

    for surface in LITERATURE_SURFACES:
        result = europepmc_search(surface, date_from, date_to)
        literature_surfaces.append(result)
        for article in result["articles"]:
            key = (article.get("doi") or article.get("pmid"), article.get("title") or "")
            if key in seen_articles or len(article_records) >= max_articles:
                continue
            seen_articles.add(key)
            article_record = {**article, "literature_surface_id": result["surface_id"]}
            maps = rcsb_maps_for_article(article_record)
            article_record["rcsb_map_count"] = len(maps)
            article_record["rcsb_mapped_pdb_ids"] = sorted({p for item in maps for p in item["pdb_ids"]})
            article_records.append(article_record)
            rcsb_maps_by_article.append(
                {
                    "article_title": article_record.get("title"),
                    "doi": article_record.get("doi"),
                    "pmid": article_record.get("pmid"),
                    "literature_surface_id": result["surface_id"],
                    "rcsb_maps": maps,
                }
            )
            for item in maps:
                for pdb_id in item["pdb_ids"]:
                    hit = {
                        "literature_surface_id": result["surface_id"],
                        "article_title": article_record.get("title"),
                        "doi": article_record.get("doi"),
                        "pmid": article_record.get("pmid"),
                        "query_or_source": item["query_or_source"],
                    }
                    if pdb_id in prior_pdb_ids and not include_prior_seen:
                        skipped_prior_seen.setdefault(pdb_id, []).append(hit)
                        continue
                    if pdb_id not in seen_pdbs and len(seen_pdbs) >= max_unique_pdb_ids:
                        continue
                    seen_pdbs.setdefault(pdb_id, []).append(hit)
            if sleep_seconds:
                time.sleep(sleep_seconds)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    candidate_rows = []
    for pdb_id, search_hits in sorted(seen_pdbs.items()):
        try:
            row = guarded.scan_pdb_id_guarded(
                pdb_id,
                search_hits,
                max_cif_bytes=max_cif_bytes,
                row_timeout_seconds=row_timeout_seconds,
            )
            row["prior_lane_artifact_seen"] = pdb_id in prior_pdb_ids
            row["prior_lane_artifact_sources_sample"] = prior_pdb_ids.get(pdb_id, [])[:5]
            rows.append(row)
            candidate_rows.extend(guarded.candidate_rows_from_scan(row, prior_pdb_ids))
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
                    "pdb_id": pdb_id,
                    "search_hits": search_hits,
                    "candidate_status": "fetch_or_parse_failed_review_only",
                    "fetch_error": repr(exc),
                    "prior_lane_artifact_seen": pdb_id in prior_pdb_ids,
                    "prior_lane_artifact_sources_sample": prior_pdb_ids.get(pdb_id, [])[:5],
                    "review_only": True,
                    "countable_label_candidate": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                    "epk_score_computed": False,
                    "ready_for_production_scoring": False,
                    "ready_for_label_import": False,
                    "target_family_id": guarded.TARGET_FAMILY_ID,
                    "target_fingerprint_id_if_future_gated": guarded.TARGET_FINGERPRINT_ID,
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    coordinate_state_counts: dict[str, int] = {}
    for row in rows:
        status = row["candidate_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    for candidate in candidate_rows:
        state = candidate["coordinate_state"]
        coordinate_state_counts[state] = coordinate_state_counts.get(state, 0) + 1

    folded_fresh = [
        candidate["candidate_id"]
        for candidate in candidate_rows
        if "folded_protein" in candidate["signal_tags"]
    ]
    evidence_for = []
    if candidate_rows:
        evidence_for.append(
            f"Source-published literature mapping emitted {len(candidate_rows)} fresh candidate-level rows."
        )
    if folded_fresh:
        evidence_for.append(
            "Fresh folded-protein candidate rows need source adjudication: "
            + ", ".join(folded_fresh[:10])
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Source-published non-peptide literature surfaces mapped no fresh candidate-level local geometry rows."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "source_published_nonpeptide_literature_followup",
            "schema_version": SCHEMA_VERSION,
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": guarded.TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": guarded.TARGET_FINGERPRINT_ID,
            "literature_surface_count": len(literature_surfaces),
            "literature_date_range": {"from": date_from, "to": date_to},
            "articles_reviewed": len(article_records),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "candidate_evidence_rows_emitted": len(candidate_rows),
            "fresh_candidate_evidence_rows_emitted": len(candidate_rows),
            "coordinate_state_counts": coordinate_state_counts,
            "prior_lane_pdb_id_count": len(prior_pdb_ids),
            "skipped_prior_seen_pdb_id_count": len(skipped_prior_seen),
            "skipped_prior_seen_pdb_ids_sample": sorted(skipped_prior_seen)[:80],
            "include_prior_seen": include_prior_seen,
            "max_articles": max_articles,
            "max_unique_pdb_ids": max_unique_pdb_ids,
            "max_cif_bytes": max_cif_bytes,
            "row_timeout_seconds": row_timeout_seconds,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Candidate evidence rows are discovery/source-review rows only. "
                "Source context is separated from source-free geometry and cannot "
                "be used as a production predictive feature."
            ),
            "source_urls": [
                EUROPE_PMC_URL,
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_POLYMER_ENTITY_URL,
                current.scout.RCSB_CIF_URL,
            ],
        },
        "literature_surfaces": literature_surfaces,
        "article_records": article_records,
        "rcsb_maps_by_article": rcsb_maps_by_article,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "candidate_evidence_rows": candidate_rows,
        "source_review_summary": {
            "primary_outcome": "candidate_evidence_rows_emitted" if candidate_rows else "search_surface_exhausted",
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(candidate_rows),
            "evidence_for": evidence_for,
            "evidence_against": [
                "No production-positive ePK claim is allowed; all candidate rows remain review-only abstentions.",
                "Source context is recorded separately from source-free geometry and must not be used as a predictive coordinate feature.",
                "Prior lane PDB IDs were skipped by default so this surface tests fresh source-published structure leads.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "If fresh rows exist, source-adjudicate them before any future frozen policy. "
                "If none exist, keep this source-published non-peptide surface exhausted until "
                "new PDB IDs or publication metadata appear."
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
    parser.add_argument("--max-articles", type=int, default=40)
    parser.add_argument("--max-unique-pdb-ids", type=int, default=50)
    parser.add_argument("--max-cif-bytes", type=int, default=25_000_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=45)
    parser.add_argument("--sleep-seconds", type=float, default=0.03)
    parser.add_argument("--include-prior-seen", action="store_true")
    parser.add_argument("--date-from", default="2015-01-01")
    parser.add_argument("--date-to", default="2026-12-31")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.artifacts_dir,
        args.max_articles,
        args.max_unique_pdb_ids,
        args.max_cif_bytes,
        args.row_timeout_seconds,
        args.sleep_seconds,
        args.include_prior_seen,
        args.date_from,
        args.date_to,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "articles_reviewed": artifact["metadata"]["articles_reviewed"],
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "candidate_evidence_rows_emitted": artifact["metadata"][
                    "candidate_evidence_rows_emitted"
                ],
                "coordinate_state_counts": artifact["metadata"]["coordinate_state_counts"],
                "skipped_prior_seen_pdb_id_count": artifact["metadata"][
                    "skipped_prior_seen_pdb_id_count"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
