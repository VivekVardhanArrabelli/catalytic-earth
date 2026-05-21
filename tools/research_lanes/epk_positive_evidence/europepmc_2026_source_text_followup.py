#!/usr/bin/env python3
"""Europe PMC source-text follow-up for current ePK positive evidence.

This lane-local helper searches bounded 2025-2026 literature/source text for
kinase-substrate structures with ATP-gamma/AMP-PNP/metal-fluoride language,
maps article titles/DOIs back to RCSB full text, and transiently scans any
returned structures for local gamma-equivalent substrate geometry.
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


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
PDB_ID_RE = re.compile(r"\b[0-9][A-Za-z0-9]{3}\b")


@dataclass(frozen=True)
class LiteratureQuery:
    surface_id: str
    query: str
    page_size: int = 12


DEFAULT_QUERIES = [
    LiteratureQuery(
        "protein_kinase_substrate_transition_analog_pdb_2025_2026",
        '("protein kinase" AND substrate AND (ATPgammaS OR "ATP-gamma-S" OR "AMP-PNP" '
        'OR "metal fluoride" OR AlF3 OR BeF3) AND PDB) AND FIRST_PDATE:[2025-01-01 TO 2026-12-31]',
        12,
    ),
    LiteratureQuery(
        "kinase_substrate_transition_state_pdb_2025_2026",
        '("kinase-substrate" AND (ATPgammaS OR "AMP-PNP" OR "transition state") AND PDB) '
        "AND FIRST_PDATE:[2025-01-01 TO 2026-12-31]",
        12,
    ),
    LiteratureQuery(
        "protein_kinase_full_length_substrate_pdb_2025_2026",
        '("protein kinase" AND "full-length substrate" AND (ATP OR ANP OR AMP-PNP OR ATPgammaS) '
        "AND PDB) AND FIRST_PDATE:[2025-01-01 TO 2026-12-31]",
        12,
    ),
    LiteratureQuery(
        "protein_kinase_substrate_peptide_amp_pnp_pdb_2025_2026",
        '("protein kinase" AND "substrate peptide" AND ("AMP-PNP" OR ANP OR ATPgammaS) AND PDB) '
        "AND FIRST_PDATE:[2025-01-01 TO 2026-12-31]",
        12,
    ),
    LiteratureQuery(
        "folded_protein_substrate_kinase_structure_2025_2026",
        '("folded protein substrate" OR "protein substrate") AND kinase AND '
        '(ATPgammaS OR "AMP-PNP" OR "metal fluoride") AND structure AND '
        "FIRST_PDATE:[2025-01-01 TO 2026-12-31]",
        12,
    ),
    LiteratureQuery(
        "kinase_substrate_atpys_aliases_pdb_2025_2026",
        '(kinase AND substrate AND (ATPyS OR "ATP gamma S" OR "ATP-gamma-S" OR "ATP\\u03b3S") '
        "AND PDB) AND FIRST_PDATE:[2025-01-01 TO 2026-12-31]",
        12,
    ),
    LiteratureQuery(
        "protein_kinase_michaelis_precatalytic_substrate_pdb_2020_2026",
        '("protein kinase" AND substrate AND ("Michaelis complex" OR "pre-catalytic" OR precatalytic) '
        "AND PDB) AND FIRST_PDATE:[2020-01-01 TO 2026-12-31]",
        12,
    ),
]


def compact_pdb_tokens(text: str) -> list[str]:
    tokens = {match.upper() for match in PDB_ID_RE.findall(text)}
    return sorted(token for token in tokens if any(char.isalpha() for char in token))


def europepmc_search(surface: LiteratureQuery) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "query": surface.query,
            "format": "json",
            "pageSize": surface.page_size,
            "resultType": "core",
        }
    )
    source_url = f"{EUROPE_PMC_URL}?{params}"
    data = current.fetch_json(source_url, timeout=30)
    results = data.get("resultList", {}).get("result", [])
    rows = []
    for rank, row in enumerate(results, start=1):
        title = html.unescape(row.get("title") or "")
        abstract = html.unescape(row.get("abstractText") or "")
        text = f"{title} {abstract}"
        rows.append(
            {
                "rank": rank,
                "title": title,
                "doi": row.get("doi"),
                "pmid": row.get("pmid"),
                "pmcid": row.get("pmcid"),
                "pub_year": row.get("pubYear"),
                "journal": row.get("journalTitle"),
                "direct_pdb_ids_in_title_or_abstract": compact_pdb_tokens(text),
                "term_flags": {
                    "protein kinase": "protein kinase" in text.lower(),
                    "kinase-substrate": "kinase-substrate" in text.lower(),
                    "substrate": "substrate" in text.lower(),
                    "full-length": "full-length" in text.lower(),
                    "AMP-PNP": "amp-pnp" in text.lower(),
                    "ATPgammaS": "atpgammas" in text.lower() or "atp-gamma-s" in text.lower(),
                    "metal fluoride": "metal fluoride" in text.lower(),
                    "PDB": "pdb" in text.lower(),
                },
            }
        )
    return {
        "surface_id": surface.surface_id,
        "query_or_source": f"Europe PMC: {surface.query}",
        "source_url": source_url,
        "hit_count": data.get("hitCount"),
        "returned_count": len(rows),
        "articles": rows,
    }


def rcsb_article_maps(article: dict[str, Any]) -> list[dict[str, Any]]:
    maps = []
    title = article.get("title") or ""
    doi = article.get("doi")
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


def build_artifact(out: Path, max_articles: int, max_unique_pdb_ids: int, sleep_seconds: float) -> dict[str, Any]:
    generated_at = current.now_iso()
    literature_surfaces = []
    article_records = []
    seen_articles: set[tuple[str | None, str]] = set()
    rcsb_maps_by_article = []
    seen_pdbs: dict[str, list[dict[str, Any]]] = {}

    for surface in DEFAULT_QUERIES:
        result = europepmc_search(surface)
        literature_surfaces.append(result)
        for article in result["articles"]:
            key = (article.get("doi") or article.get("pmid"), article.get("title") or "")
            if key in seen_articles or len(article_records) >= max_articles:
                continue
            seen_articles.add(key)
            article_record = {**article, "literature_surface_id": result["surface_id"]}
            maps = rcsb_article_maps(article_record)
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
                    if pdb_id not in seen_pdbs and len(seen_pdbs) >= max_unique_pdb_ids:
                        continue
                    seen_pdbs.setdefault(pdb_id, []).append(
                        {
                            "literature_surface_id": result["surface_id"],
                            "article_title": article_record.get("title"),
                            "doi": article_record.get("doi"),
                            "pmid": article_record.get("pmid"),
                            "query_or_source": item["query_or_source"],
                        }
                    )
            if sleep_seconds:
                time.sleep(sleep_seconds)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    for pdb_id, search_hits in seen_pdbs.items():
        try:
            rows.append(current.scan_pdb_id(pdb_id, search_hits))
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
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
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["candidate_status"]] = status_counts.get(row["candidate_status"], 0) + 1
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

    evidence_for = []
    if nonpeptide:
        evidence_for.append(
            "Europe PMC source-text mapping found local-metal non-peptide candidates requiring source adjudication: "
            + ", ".join(nonpeptide)
            + "."
        )
    if short_or_peptide:
        evidence_for.append(
            "Europe PMC source-text mapping found review-only short/peptide local-metal candidates: "
            + ", ".join(short_or_peptide)
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Bounded Europe PMC source-text mapping produced articles and/or RCSB rows but no local-metal ePK substrate candidate."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "europepmc_2026_source_text_followup",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "max_articles": max_articles,
            "max_unique_pdb_ids": max_unique_pdb_ids,
            "literature_surface_count": len(literature_surfaces),
            "articles_reviewed": len(article_records),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_nonpeptide_candidate_pdb_ids": nonpeptide,
            "local_metal_peptide_or_short_candidate_pdb_ids": short_or_peptide,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Literature/source-text mapping only. It does not create labels, scores, "
                "thresholds, fingerprints, migrations, or production claims."
            ),
            "source_urls": [
                EUROPE_PMC_URL,
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_CIF_URL,
            ],
        },
        "literature_surfaces": literature_surfaces,
        "article_records": article_records,
        "rcsb_maps_by_article": rcsb_maps_by_article,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": "next_query_defined" if nonpeptide else "evidence_for" if short_or_peptide else "search_surface_exhausted",
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(nonpeptide or short_or_peptide),
            "evidence_for": evidence_for,
            "evidence_against": [
                "No clean folded-protein canonical ePK substrate transfer-state positive was promoted from this literature surface.",
                "RCSB title/DOI mapping is sparse for many current Europe PMC articles, so absent PDB mappings are not negative structural evidence.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "Continue bounded source-text searches only; source-map any future article-to-PDB hit with "
                "local-metal non-peptide geometry before treating it as evidence. Keep production paths closed."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-articles", type=int, default=50)
    parser.add_argument("--max-unique-pdb-ids", type=int, default=80)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.out, args.max_articles, args.max_unique_pdb_ids, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "articles_reviewed": artifact["metadata"]["articles_reviewed"],
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "local_metal_nonpeptide_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_nonpeptide_candidate_pdb_ids"
                ],
                "local_metal_peptide_or_short_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_peptide_or_short_candidate_pdb_ids"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
