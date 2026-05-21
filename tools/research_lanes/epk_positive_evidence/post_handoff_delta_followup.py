#!/usr/bin/env python3
"""Post-handoff delta follow-up for ePK positive evidence.

This helper is intentionally narrow. It checks whether a new RCSB release row,
RCSB revision row, 23FC publication metadata, or same-day source-publication
record creates fresh candidate-level ePK evidence after the previous handoff.

It keeps source review separate from source-free geometry, scans only fresh
mapped PDB IDs by default, and writes compact review-only artifacts. It does
not write raw coordinates, production labels, scores, thresholds, registries,
fingerprints, migrations, or readiness claims.
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
REVISION_DATE_ATTR = "rcsb_accession_info.revision_date"
PDB_ID_RE = re.compile(r"\b[0-9][A-Za-z0-9]{3}\b")
CROSSREF_WORKS_URL = "https://api.crossref.org/works"


@dataclass(frozen=True)
class DeltaSurface:
    surface_id: str
    date_attr: str
    date_from: str
    date_to: str
    ligand_mode: str
    source_query: str | None = None
    rows: int = 50


@dataclass(frozen=True)
class PublicationSurface:
    surface_id: str
    query: str
    page_size: int = 5


def compact_pdb_tokens(text: str) -> list[str]:
    tokens = {match.upper() for match in PDB_ID_RE.findall(text)}
    return sorted(token for token in tokens if any(char.isalpha() for char in token))


def range_surface_query(surface: DeltaSurface) -> dict[str, Any]:
    nodes = [
        current.family_group(),
        current.text_term(
            surface.date_attr,
            {"from": surface.date_from, "to": surface.date_to},
            "range",
        ),
        *current.ligand_nodes(surface.ligand_mode),
    ]
    if surface.source_query:
        nodes.append(current.full_text(surface.source_query))
    return current.group("and", nodes)


def search_delta_surface(surface: DeltaSurface) -> dict[str, Any]:
    payload = {
        "query": range_surface_query(surface),
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": surface.rows},
            "results_content_type": ["experimental"],
        },
    }
    ligand_label = (
        "ATP/ANP/ACP/AGS+MG/MN"
        if surface.ligand_mode == "gamma"
        else "ADP+AF3/ALF/BEF/MGF"
    )
    source_label = f" AND full_text='{surface.source_query}'" if surface.source_query else ""
    query_or_source = (
        "RCSB advanced: "
        f"{surface.date_attr} {surface.date_from}..{surface.date_to} "
        f"AND canonical ePK AND {ligand_label}{source_label}"
    )
    try:
        result = current.fetch_json(current.RCSB_SEARCH_URL, payload=payload)
        ids = [row["identifier"].upper() for row in result.get("result_set", [])]
        return {
            "surface_id": surface.surface_id,
            "query_or_source": query_or_source,
            "date_attr": surface.date_attr,
            "date_from": surface.date_from,
            "date_to": surface.date_to,
            "ligand_mode": surface.ligand_mode,
            "source_query": surface.source_query,
            "returned_count": len(ids),
            "total_count": result.get("total_count", len(ids)),
            "pdb_ids": ids,
        }
    except Exception as exc:  # noqa: BLE001 - compact outage/blocker field.
        return {
            "surface_id": surface.surface_id,
            "query_or_source": query_or_source,
            "date_attr": surface.date_attr,
            "date_from": surface.date_from,
            "date_to": surface.date_to,
            "ligand_mode": surface.ligand_mode,
            "source_query": surface.source_query,
            "returned_count": 0,
            "total_count": 0,
            "pdb_ids": [],
            "fetch_error": repr(exc),
        }


def publication_surfaces() -> list[PublicationSurface]:
    return [
        PublicationSurface(
            "same_day_full_length_substrate_phosphosite_pdb",
            '("protein kinase" AND "full-length substrate" AND "phosphorylation site" AND PDB)',
        ),
        PublicationSurface(
            "same_day_protein_substrate_transfer_analog_pdb",
            '("protein kinase" AND "protein substrate" AND '
            '(phosphoacceptor OR "phosphorylation site") AND '
            '("AMP-PNP" OR ATPgammaS OR "ATP-gamma-S" OR "metal fluoride") AND PDB)',
        ),
        PublicationSurface(
            "same_day_kinase_substrate_complex_transfer_analog_pdb",
            '("kinase-substrate complex" AND ("AMP-PNP" OR ATPgammaS OR ATP OR "metal fluoride") AND PDB)',
        ),
        PublicationSurface(
            "same_day_folded_substrate_structure_phosphosite",
            '("folded protein substrate" AND kinase AND ("phosphorylation site" OR phosphoacceptor) AND structure)',
        ),
    ]


def crossref_publication_surfaces() -> list[PublicationSurface]:
    return [
        PublicationSurface(
            "crossref_same_day_full_length_substrate_phosphosite_pdb",
            '"protein kinase" "full-length substrate" "phosphorylation site" PDB',
        ),
        PublicationSurface(
            "crossref_same_day_protein_substrate_transfer_analog_pdb",
            '"protein kinase" "protein substrate" phosphoacceptor "AMP-PNP" PDB',
        ),
        PublicationSurface(
            "crossref_same_day_kinase_substrate_complex_transfer_analog_pdb",
            '"kinase-substrate complex" "AMP-PNP" PDB',
        ),
        PublicationSurface(
            "crossref_same_day_folded_substrate_structure_phosphosite",
            '"folded protein substrate" kinase "phosphorylation site" structure',
        ),
    ]


def europepmc_publication_search(
    surface: PublicationSurface,
    date_from: str,
    date_to: str,
) -> dict[str, Any]:
    query = f"{surface.query} AND FIRST_PDATE:[{date_from} TO {date_to}]"
    params = urllib.parse.urlencode(
        {
            "query": query,
            "format": "json",
            "pageSize": surface.page_size,
            "resultType": "core",
        }
    )
    source_url = f"{current.EUROPE_PMC_URL}?{params}"
    try:
        data = current.fetch_json(source_url, timeout=30)
    except Exception as exc:  # noqa: BLE001 - compact outage/blocker field.
        return {
            "surface_id": surface.surface_id,
            "query_or_source": f"Europe PMC: {query}",
            "source_url": source_url,
            "hit_count": None,
            "returned_count": 0,
            "articles": [],
            "fetch_error": repr(exc),
        }
    articles = []
    for rank, row in enumerate(data.get("resultList", {}).get("result", []), start=1):
        title = html.unescape(row.get("title") or "")
        abstract = html.unescape(row.get("abstractText") or "")
        text = f"{title} {abstract}"
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


def crossref_publication_search(
    surface: PublicationSurface,
    date_from: str,
    date_to: str,
) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "query.bibliographic": surface.query,
            "filter": f"from-pub-date:{date_from},until-pub-date:{date_to}",
            "rows": surface.page_size,
        }
    )
    source_url = f"{CROSSREF_WORKS_URL}?{params}"
    try:
        data = current.fetch_json(source_url, timeout=30)
    except Exception as exc:  # noqa: BLE001 - compact outage/blocker field.
        return {
            "surface_id": surface.surface_id,
            "query_or_source": f"Crossref: {surface.query} pub-date {date_from}..{date_to}",
            "source_url": source_url,
            "hit_count": None,
            "returned_count": 0,
            "articles": [],
            "fetch_error": repr(exc),
        }
    articles = []
    for rank, row in enumerate(data.get("message", {}).get("items", []), start=1):
        titles = row.get("title") or []
        title = html.unescape(titles[0] if titles else "")
        doi = row.get("DOI")
        doi_text = str(doi or "")
        is_pdb_dataset_doi = doi_text.lower().startswith("10.2210/pdb")
        token_text = f"{title} {doi_text if is_pdb_dataset_doi else ''}"
        articles.append(
            {
                "rank": rank,
                "title": title,
                "doi": doi,
                "pmid": None,
                "pmcid": None,
                "pub_year": None,
                "journal": row.get("container-title", [None])[0]
                if isinstance(row.get("container-title"), list)
                else row.get("container-title"),
                "crossref_type": row.get("type"),
                "publisher": row.get("publisher"),
                "is_pdb_dataset_doi": is_pdb_dataset_doi,
                "direct_pdb_ids_in_title_or_abstract": compact_pdb_tokens(token_text),
            }
        )
    return {
        "surface_id": surface.surface_id,
        "query_or_source": f"Crossref: {surface.query} pub-date {date_from}..{date_to}",
        "source_url": source_url,
        "hit_count": data.get("message", {}).get("total-results"),
        "returned_count": len(articles),
        "articles": articles,
    }


def rcsb_maps_for_article(article: dict[str, Any]) -> list[dict[str, Any]]:
    maps = []
    doi = article.get("doi")
    title = article.get("title")
    if doi:
        maps.append(current.rcsb_full_text_ids(str(doi), rows=20))
    if title:
        maps.append(current.rcsb_full_text_ids(str(title), rows=20))
    for pdb_id in article.get("direct_pdb_ids_in_title_or_abstract", []):
        maps.append(
            {
                "query_or_source": f"Source title/abstract direct PDB token: {pdb_id}",
                "returned_count": 1,
                "total_count": 1,
                "pdb_ids": [pdb_id],
            }
        )
    return maps


def compact_entry_citation(pdb_id: str) -> dict[str, Any]:
    try:
        entry = current.fetch_json(current.scout.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    except Exception as exc:  # noqa: BLE001 - compact metadata failure.
        return {"pdb_id": pdb_id, "fetch_error": repr(exc)}
    citation = (entry.get("citation") or [{}])[0]
    accession = entry.get("rcsb_accession_info") or {}
    return {
        "pdb_id": pdb_id,
        "title": entry.get("struct", {}).get("title"),
        "initial_release_date": accession.get("initial_release_date"),
        "revision_date": accession.get("revision_date"),
        "citation_title": citation.get("title"),
        "citation_year": citation.get("year"),
        "citation_pubmed_id": citation.get("pdbx_database_id_PubMed")
        or citation.get("pdbx_database_id_pub_med"),
        "citation_doi": citation.get("pdbx_database_id_DOI")
        or citation.get("pdbx_database_id_doi"),
    }


def build_delta_surfaces(date_from: str, date_to: str) -> list[DeltaSurface]:
    source_terms = [
        None,
        "substrate phosphorylation",
        "full-length substrate",
        "phosphoacceptor substrate",
        "kinase-substrate complex",
    ]
    surfaces = []
    for date_attr in (current.RELEASE_DATE_ATTR, REVISION_DATE_ATTR):
        attr_label = "initial_release" if date_attr == current.RELEASE_DATE_ATTR else "revision"
        for ligand_mode in ("gamma", "transition"):
            for term in source_terms:
                safe_term = "any" if term is None else term.replace(" ", "_").replace("-", "_")
                surfaces.append(
                    DeltaSurface(
                        f"post_handoff_{attr_label}_{ligand_mode}_{safe_term}",
                        date_attr,
                        date_from,
                        date_to,
                        ligand_mode,
                        term,
                    )
                )
    return surfaces


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    date_from: str,
    date_to: str,
    max_unique_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
) -> dict[str, Any]:
    generated_at = current.now_iso()
    prior_pdb_ids = guarded.collect_prior_pdb_ids(artifacts_dir, out)
    source_recheck_23fc = current.recheck_23fc()
    search_surfaces = []
    literature_surfaces = []
    crossref_surfaces = []
    article_records = []
    rcsb_maps_by_article = []
    fresh_seen: dict[str, list[dict[str, Any]]] = {}
    skipped_prior_seen: dict[str, list[dict[str, Any]]] = {}

    for surface in build_delta_surfaces(date_from, date_to):
        result = search_delta_surface(surface)
        search_surfaces.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1):
            hit = {
                "surface_id": result["surface_id"],
                "rank": rank,
                "query_or_source": result["query_or_source"],
            }
            if pdb_id in prior_pdb_ids:
                skipped_prior_seen.setdefault(pdb_id, []).append(hit)
                continue
            if pdb_id not in fresh_seen and len(fresh_seen) >= max_unique_pdb_ids:
                continue
            fresh_seen.setdefault(pdb_id, []).append(hit)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    seen_articles: set[tuple[str | None, str]] = set()
    for surface in publication_surfaces():
        result = europepmc_publication_search(surface, date_from, date_to)
        literature_surfaces.append(result)
        for article in result["articles"]:
            key = (article.get("doi") or article.get("pmid"), article.get("title") or "")
            if key in seen_articles:
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
                        "surface_id": result["surface_id"],
                        "article_title": article_record.get("title"),
                        "doi": article_record.get("doi"),
                        "pmid": article_record.get("pmid"),
                        "query_or_source": item["query_or_source"],
                    }
                    if pdb_id in prior_pdb_ids:
                        skipped_prior_seen.setdefault(pdb_id, []).append(hit)
                        continue
                    if pdb_id not in fresh_seen and len(fresh_seen) >= max_unique_pdb_ids:
                        continue
                    fresh_seen.setdefault(pdb_id, []).append(hit)
            if sleep_seconds:
                time.sleep(sleep_seconds)

    for surface in crossref_publication_surfaces():
        result = crossref_publication_search(surface, date_from, date_to)
        crossref_surfaces.append(result)
        for article in result["articles"]:
            key = (article.get("doi") or article.get("pmid"), article.get("title") or "")
            if key in seen_articles:
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
                        "surface_id": result["surface_id"],
                        "article_title": article_record.get("title"),
                        "doi": article_record.get("doi"),
                        "pmid": article_record.get("pmid"),
                        "query_or_source": item["query_or_source"],
                    }
                    if pdb_id in prior_pdb_ids:
                        skipped_prior_seen.setdefault(pdb_id, []).append(hit)
                        continue
                    if pdb_id not in fresh_seen and len(fresh_seen) >= max_unique_pdb_ids:
                        continue
                    fresh_seen.setdefault(pdb_id, []).append(hit)
            if sleep_seconds:
                time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    candidate_rows = []
    for pdb_id, search_hits in sorted(fresh_seen.items()):
        try:
            row = guarded.scan_pdb_id_guarded(
                pdb_id,
                search_hits,
                max_cif_bytes=max_cif_bytes,
                row_timeout_seconds=row_timeout_seconds,
            )
            row["prior_lane_artifact_seen"] = False
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
                    "review_only": True,
                    "countable_label_candidate": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                    "epk_score_computed": False,
                    "ready_for_production_scoring": False,
                    "ready_for_label_import": False,
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    coordinate_state_counts: dict[str, int] = {}
    for candidate in candidate_rows:
        state = candidate["coordinate_state"]
        coordinate_state_counts[state] = coordinate_state_counts.get(state, 0) + 1

    status_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("candidate_status", "unknown_review_only")
        status_counts[status] = status_counts.get(status, 0) + 1

    prior_metadata_sample = [
        compact_entry_citation(pdb_id)
        for pdb_id in sorted(skipped_prior_seen)[:25]
    ]

    surface_errors = [
        {
            "surface_id": result["surface_id"],
            "fetch_error": result["fetch_error"],
        }
        for result in search_surfaces + literature_surfaces + crossref_surfaces
        if result.get("fetch_error")
    ]
    publication_now_available = (
        source_recheck_23fc["publication_metadata_present_in_rcsb"]
        or source_recheck_23fc["europepmc_publication_metadata_present"]
    )
    fresh_ids = sorted(fresh_seen)
    prior_ids = sorted(skipped_prior_seen)

    evidence_for = []
    evidence_against = []
    if publication_now_available:
        evidence_for.append("23FC publication metadata appears to be available and needs source review.")
    else:
        evidence_against.append("23FC publication metadata remains absent in RCSB and Europe PMC checks.")
    if candidate_rows:
        evidence_for.append(
            f"Post-handoff delta surfaces emitted {len(candidate_rows)} candidate evidence row(s)."
        )
    else:
        evidence_against.append("Post-handoff delta surfaces emitted zero candidate evidence rows.")
    if fresh_ids:
        evidence_for.append(
            "Fresh mapped PDB IDs were scanned from post-handoff delta surfaces: "
            + ", ".join(fresh_ids)
            + "."
        )
    else:
        evidence_against.append(
            "No genuinely new PDB ID appeared in current-date release, revision, or same-day publication surfaces."
        )
    if prior_ids:
        evidence_for.append(
            f"Prior-seen current-date/revision/source-publication IDs were observed and skipped as non-new: {len(prior_ids)}."
        )

    primary_outcome = "candidate_evidence_rows_emitted" if candidate_rows else "search_surface_exhausted"
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "schema_version": SCHEMA_VERSION,
            "method": "post_handoff_delta_followup",
            "generated_at": generated_at,
            "date_range": {"from": date_from, "to": date_to},
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "epk_score_computed": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "max_unique_pdb_ids": max_unique_pdb_ids,
            "fresh_unique_pdb_ids": fresh_ids,
            "fresh_unique_pdb_id_count": len(fresh_ids),
            "prior_seen_pdb_ids_observed_count": len(prior_ids),
            "prior_seen_pdb_ids_observed_sample": prior_ids[:50],
            "rows_reviewed": len(rows),
            "candidate_evidence_rows_emitted": len(candidate_rows),
            "coordinate_state_counts": coordinate_state_counts,
            "candidate_status_counts": status_counts,
            "surface_error_count": len(surface_errors),
            "source_urls": [
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_CIF_URL,
                current.EUROPE_PMC_URL,
                CROSSREF_WORKS_URL,
            ],
        },
        "source_recheck_23fc": source_recheck_23fc,
        "search_surfaces": search_surfaces,
        "literature_surfaces": literature_surfaces,
        "crossref_surfaces": crossref_surfaces,
        "article_records": article_records,
        "rcsb_maps_by_article": rcsb_maps_by_article,
        "skipped_prior_seen": skipped_prior_seen,
        "prior_seen_metadata_sample": prior_metadata_sample,
        "fetch_failures": fetch_failures,
        "surface_errors": surface_errors,
        "rows": rows,
        "candidate_evidence_rows": candidate_rows,
        "source_review_summary": {
            "primary_outcome": primary_outcome,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "search_surface_exhausted": not bool(candidate_rows),
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "counterexamples_found": [],
            "recommendation": (
                "Keep this as review-only delta evidence. If no fresh IDs or publication "
                "metadata appear, wait for the next RCSB release or genuinely new source "
                "metadata before rerunning exhausted broad surfaces."
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
        default=Path("artifacts/research_lanes/epk_positive_evidence"),
        type=Path,
    )
    parser.add_argument("--date-from", default="2026-05-21")
    parser.add_argument("--date-to", default="2026-05-21")
    parser.add_argument("--max-unique-pdb-ids", type=int, default=20)
    parser.add_argument("--max-cif-bytes", type=int, default=2_500_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=20)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.artifacts_dir,
        args.date_from,
        args.date_to,
        args.max_unique_pdb_ids,
        args.max_cif_bytes,
        args.row_timeout_seconds,
        args.sleep_seconds,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "fresh_unique_pdb_id_count": artifact["metadata"]["fresh_unique_pdb_id_count"],
                "rows_reviewed": artifact["metadata"]["rows_reviewed"],
                "candidate_evidence_rows_emitted": artifact["metadata"][
                    "candidate_evidence_rows_emitted"
                ],
                "coordinate_state_counts": artifact["metadata"]["coordinate_state_counts"],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
                "surface_error_count": artifact["metadata"]["surface_error_count"],
                "publication_metadata_present_in_rcsb": artifact["source_recheck_23fc"][
                    "publication_metadata_present_in_rcsb"
                ],
                "europepmc_publication_metadata_present": artifact["source_recheck_23fc"][
                    "europepmc_publication_metadata_present"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
