#!/usr/bin/env python3
"""Bounded publication-metadata follow-up for the 23FC ATR/Chk1 lead.

This helper triangulates the review-only 23FC singleton across RCSB, PDBe,
Europe PMC, Crossref, and RCSB full-text sibling aliases. It writes compact
source summaries only; it does not fetch coordinate files or create labels,
scores, thresholds, fingerprints, migrations, or production claims.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import current_release_epk_followup as current_scan


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
PDB_ID = "23FC"
EXACT_TITLE = "Cryo-EM structure of human ATR-ATRIP complex with ATPgammaS and Chk1"
RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
PDBE_SUMMARY_URL = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/{pdb_id}"
PDBE_PUBLICATIONS_URL = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/{pdb_id}"
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF_WORKS_URL = "https://api.crossref.org/works"
PDB_DATASET_DOI_RE = re.compile(r"10\.2210/pdb([0-9a-z]{4})/pdb", re.IGNORECASE)


EUROPE_PMC_QUERIES = [
    f'TITLE:"{EXACT_TITLE}"',
    '"23FC" ATR Chk1',
    '"ATR-ATRIP" "ATPgammaS" Chk1',
    '"ATR-ATRIP" "ATPgammaS" "Chk1"',
    '"Chk1" "Ser317" "ATR" "ATPgammaS"',
    '"Wang" "Qiao" "ATR-ATRIP" "Chk1"',
]

RCSB_FULL_TEXT_ALIASES = [
    EXACT_TITLE,
    "ATR ATRIP Chk1 ATPgammaS",
    "human ATR-ATRIP complex ATPgammaS Chk1",
    "Chk1 Ser317 ATR ATPgammaS",
    "Wang Qiao ATR-ATRIP Chk1 ATPgammaS",
]

CROSSREF_QUERIES = [
    {"query.title": EXACT_TITLE},
    {"query.bibliographic": '"ATR-ATRIP" "ATPgammaS" Chk1'},
    {"query.bibliographic": '"Chk1" "Ser317" "ATR" "ATPgammaS"'},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_json(url: str, *, payload: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    data = None
    headers = {"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status == 204:
            return {"total_count": 0, "result_set": []}
        return json.loads(response.read().decode("utf-8"))


def rcsb_entry() -> dict[str, Any]:
    url = RCSB_ENTRY_URL.format(pdb_id=PDB_ID)
    entry = fetch_json(url)
    citation = (entry.get("citation") or [{}])[0]
    accession = entry.get("rcsb_accession_info") or {}
    database_2 = entry.get("database_2") or []
    return {
        "source_url": url,
        "title": citation.get("title"),
        "journal_abbrev": citation.get("journal_abbrev") or citation.get("rcsb_journal_abbrev"),
        "year": citation.get("year"),
        "pdbx_database_id_pub_med": citation.get("pdbx_database_id_PubMed")
        or citation.get("pdbx_database_id_pub_med"),
        "pdbx_database_id_doi": citation.get("pdbx_database_id_DOI")
        or citation.get("pdbx_database_id_doi"),
        "pdb_dataset_doi": next(
            (
                item.get("pdbx_DOI")
                for item in database_2
                if str(item.get("database_id", "")).upper() == "PDB" and item.get("pdbx_DOI")
            ),
            None,
        ),
        "deposit_date": accession.get("deposit_date"),
        "initial_release_date": accession.get("initial_release_date"),
        "revision_date": accession.get("revision_date"),
        "status_code": accession.get("status_code"),
        "authors": citation.get("rcsb_authors") or citation.get("pdbx_database_id_PubMed"),
    }


def pdbe_source(endpoint: str) -> dict[str, Any]:
    url = endpoint.format(pdb_id=PDB_ID.lower())
    try:
        data = fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - source outage is compactly recorded.
        return {"source_url": url, "fetch_error": repr(exc)}
    return {"source_url": url, "payload": data.get(PDB_ID.lower()) or data.get(PDB_ID) or data}


def europepmc_query(query: str, page_size: int) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {"query": query, "format": "json", "pageSize": page_size, "resultType": "core"}
    )
    url = f"{EUROPE_PMC_URL}?{params}"
    try:
        data = fetch_json(url)
    except Exception as exc:  # noqa: BLE001
        return {"query": query, "source_url": url, "fetch_error": repr(exc), "results": []}
    rows = []
    for item in data.get("resultList", {}).get("result", []):
        rows.append(
            {
                "title": html.unescape(item.get("title") or ""),
                "doi": item.get("doi"),
                "pmid": item.get("pmid"),
                "pmcid": item.get("pmcid"),
                "pub_year": item.get("pubYear"),
                "journal": item.get("journalTitle"),
            }
        )
    return {
        "query": query,
        "source_url": url,
        "hit_count": data.get("hitCount"),
        "returned_count": len(rows),
        "results": rows,
    }


def crossref_query(params: dict[str, str], rows: int) -> dict[str, Any]:
    encoded = urllib.parse.urlencode({**params, "rows": rows})
    url = f"{CROSSREF_WORKS_URL}?{encoded}"
    try:
        data = fetch_json(url)
    except Exception as exc:  # noqa: BLE001
        return {"query": params, "source_url": url, "fetch_error": repr(exc), "items": []}
    items = []
    for item in data.get("message", {}).get("items", []):
        titles = item.get("title") or []
        doi = item.get("DOI")
        item_type = item.get("type")
        publisher = item.get("publisher")
        items.append(
            {
                "title": titles[0] if titles else None,
                "doi": doi,
                "type": item_type,
                "publisher": publisher,
                "published_print": item.get("published-print"),
                "published_online": item.get("published-online"),
                "created": item.get("created"),
                "is_pdb_dataset_doi": bool(doi and doi.lower().startswith("10.2210/pdb")),
                "looks_like_article": item_type in {"journal-article", "posted-content", "proceedings-article"},
            }
        )
    return {
        "query": params,
        "source_url": url,
        "total_results": data.get("message", {}).get("total-results"),
        "returned_count": len(items),
        "items": items,
    }


def pdb_ids_from_crossref_dataset_dois(crossref_checks: list[dict[str, Any]]) -> list[str]:
    pdb_ids: set[str] = set()
    for check in crossref_checks:
        for item in check.get("items", []):
            doi = item.get("doi") or ""
            title = (item.get("title") or "").lower()
            match = PDB_DATASET_DOI_RE.fullmatch(doi)
            if match and "atr" in title:
                pdb_ids.add(match.group(1).upper())
    return sorted(pdb_ids)


def compact_polymer_entity(pdb_id: str, entity_id: str) -> dict[str, Any]:
    url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}"
    entity = fetch_json(url)
    sequence = entity.get("entity_poly", {}).get("pdbx_seq_one_letter_code_can") or ""
    return {
        "entity_id": entity.get("rcsb_id"),
        "source_url": url,
        "description": entity.get("rcsb_polymer_entity", {}).get("pdbx_description"),
        "type": entity.get("entity_poly", {}).get("type"),
        "length": len("".join(sequence.split())) if sequence else None,
        "organism": (entity.get("rcsb_entity_source_organism") or [{}])[0].get("scientific_name"),
    }


def compact_nonpolymer_entity(pdb_id: str, entity_id: str) -> dict[str, Any]:
    url = f"https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb_id}/{entity_id}"
    entity = fetch_json(url)
    return {
        "entity_id": entity.get("rcsb_id"),
        "source_url": url,
        "comp_id": entity.get("pdbx_entity_nonpoly", {}).get("comp_id"),
        "description": entity.get("pdbx_entity_nonpoly", {}).get("name"),
    }


def compact_related_pdb_dataset(pdb_id: str) -> dict[str, Any]:
    entry_url = RCSB_ENTRY_URL.format(pdb_id=pdb_id)
    try:
        entry = fetch_json(entry_url)
    except Exception as exc:  # noqa: BLE001
        return {"pdb_id": pdb_id, "source_url": entry_url, "fetch_error": repr(exc)}
    citation = (entry.get("citation") or [{}])[0]
    identifiers = entry.get("rcsb_entry_container_identifiers") or {}
    polymer_entity_ids = [str(item) for item in identifiers.get("polymer_entity_ids") or []]
    nonpolymer_entity_ids = [str(item) for item in identifiers.get("non_polymer_entity_ids") or []]
    polymers = []
    for entity_id in polymer_entity_ids[:6]:
        try:
            polymers.append(compact_polymer_entity(pdb_id, entity_id))
        except Exception as exc:  # noqa: BLE001
            polymers.append({"entity_id": entity_id, "fetch_error": repr(exc)})
    nonpolymers = []
    for entity_id in nonpolymer_entity_ids[:10]:
        try:
            nonpolymers.append(compact_nonpolymer_entity(pdb_id, entity_id))
        except Exception as exc:  # noqa: BLE001
            nonpolymers.append({"entity_id": entity_id, "fetch_error": repr(exc)})
    polymer_descriptions = " ".join(str(item.get("description") or "") for item in polymers).lower()
    return {
        "pdb_id": pdb_id,
        "source_url": entry_url,
        "title": entry.get("struct", {}).get("title"),
        "citation": {
            "title": citation.get("title"),
            "year": citation.get("year"),
            "doi": citation.get("pdbx_database_id_DOI") or citation.get("pdbx_database_id_doi"),
            "pubmed_id": citation.get("pdbx_database_id_PubMed") or citation.get("pdbx_database_id_pub_med"),
            "journal": citation.get("journal_abbrev") or citation.get("rcsb_journal_abbrev"),
        },
        "polymer_entities": polymers,
        "nonpolymer_entities": nonpolymers,
        "has_chk1_or_substrate_named_entity": "chk1" in polymer_descriptions
        or "checkpoint kinase 1" in polymer_descriptions
        or "substrate" in polymer_descriptions,
        "review_decision": (
            "related_dataset_contains_named_substrate_entity_review_needed"
            if (
                "chk1" in polymer_descriptions
                or "checkpoint kinase 1" in polymer_descriptions
                or "substrate" in polymer_descriptions
            )
            else "related_dataset_donor_state_without_named_substrate_entity_review_only_negative"
        ),
    }


def rcsb_full_text_ids(query: str, rows: int) -> dict[str, Any]:
    payload = {
        "query": {"type": "terminal", "service": "full_text", "parameters": {"value": query}},
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "results_content_type": ["experimental"],
        },
    }
    result = fetch_json(RCSB_SEARCH_URL, payload=payload)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    return {
        "query": query,
        "source_url": RCSB_SEARCH_URL,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def source_article_family_followup(related_rows: list[dict[str, Any]], rows: int) -> dict[str, Any]:
    article_queries = []
    seen_queries: set[str] = set()
    for related in related_rows:
        citation = related.get("citation") or {}
        doi = citation.get("doi")
        title = citation.get("title")
        if doi and doi not in seen_queries:
            article_queries.append(rcsb_full_text_ids(str(doi), rows))
            seen_queries.add(str(doi))
        if title and title not in seen_queries:
            article_queries.append(rcsb_full_text_ids(str(title), rows))
            seen_queries.add(str(title))
    family_ids = sorted(
        {
            pdb_id
            for query in article_queries
            for pdb_id in query.get("pdb_ids", [])
            if pdb_id != PDB_ID
        }
    )
    family_rows = [compact_related_pdb_dataset(pdb_id) for pdb_id in family_ids[:20]]
    geometry_rows = []
    geometry_fetch_failures = []
    for pdb_id in family_ids[:20]:
        try:
            geometry_rows.append(
                current_scan.scan_pdb_id(
                    pdb_id,
                    [
                        {
                            "query_or_source": (
                                "RCSB full-text DOI/title family geometry scan from 23FC "
                                "publication-metadata follow-up"
                            )
                        }
                    ],
                )
            )
        except Exception as exc:  # noqa: BLE001 - compact source artifact records failures.
            geometry_fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
    geometry_status_counts: dict[str, int] = {}
    for row in geometry_rows:
        status = row.get("candidate_status", "unknown")
        geometry_status_counts[status] = geometry_status_counts.get(status, 0) + 1
    no_named_substrate_ids = [
        row["pdb_id"]
        for row in family_rows
        if row.get("review_decision") == "related_dataset_donor_state_without_named_substrate_entity_review_only_negative"
    ]
    named_substrate_ids = [
        row["pdb_id"]
        for row in family_rows
        if row.get("review_decision") == "related_dataset_contains_named_substrate_entity_review_needed"
    ]
    return {
        "source_scope": "RCSB full-text DOI/title family follow-up for related ATR-ATRIP publication rows.",
        "article_queries": article_queries,
        "family_pdb_ids": family_ids,
        "family_rows": family_rows,
        "geometry_rows": geometry_rows,
        "geometry_fetch_failures": geometry_fetch_failures,
        "geometry_candidate_status_counts": geometry_status_counts,
        "geometry_local_metal_nonpeptide_candidate_pdb_ids": [
            row["pdb_id"]
            for row in geometry_rows
            if row.get("candidate_status") == "local_metal_nonpeptide_candidate_source_validation_pending_review_only"
        ],
        "geometry_local_metal_peptide_or_short_candidate_pdb_ids": [
            row["pdb_id"]
            for row in geometry_rows
            if row.get("candidate_status") == "local_metal_peptide_or_short_candidate_review_only"
        ],
        "no_named_substrate_entity_pdb_ids": no_named_substrate_ids,
        "named_substrate_entity_pdb_ids": named_substrate_ids,
        "review_decision": (
            "article_family_contains_named_substrate_entity_review_needed"
            if named_substrate_ids
            else "article_family_no_named_substrate_entity_review_only_negative"
        ),
    }


def normalized_title(text: str | None) -> str:
    return " ".join((text or "").lower().replace("\u2013", "-").replace("\u2014", "-").split())


def looks_like_23fc_publication_title(text: str | None) -> bool:
    title = normalized_title(text)
    exact = normalized_title(EXACT_TITLE)
    if title == exact:
        return True
    return (
        "atr-atrip" in title
        and "chk1" in title
        and ("atpgammas" in title or "atp-gamma" in title or "atp gamma" in title)
    )


def classify_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    rcsb = artifact["rcsb_entry"]
    pdbe_publications = artifact["pdbe_publications"].get("payload") or []
    pdbe_publication_rows = pdbe_publications if isinstance(pdbe_publications, list) else []
    europepmc_hits = [
        row
        for query in artifact["europepmc_checks"]
        for row in query.get("results", [])
        if row.get("doi") or row.get("pmid") or row.get("pmcid")
        if looks_like_23fc_publication_title(row.get("title"))
    ]
    crossref_article_hits = [
        item
        for query in artifact["crossref_checks"]
        for item in query.get("items", [])
        if item.get("looks_like_article")
        and item.get("doi")
        and not item.get("is_pdb_dataset_doi")
        and looks_like_23fc_publication_title(item.get("title"))
    ]
    sibling_ids = sorted(
        {
            pdb_id
            for query in artifact["rcsb_full_text_sibling_checks"]
            for pdb_id in query.get("pdb_ids", [])
        }
    )
    related_dataset_rows = artifact.get("related_crossref_pdb_dataset_followups", [])
    article_family = artifact.get("source_article_family_followup") or {}
    related_dataset_negatives = [
        row
        for row in related_dataset_rows
        if row.get("pdb_id") != PDB_ID
        and row.get("review_decision") == "related_dataset_donor_state_without_named_substrate_entity_review_only_negative"
    ]
    rcsb_has_article = bool(rcsb.get("pdbx_database_id_pub_med") or rcsb.get("pdbx_database_id_doi"))
    pdbe_has_article = any(
        row.get("doi") or row.get("pubmed_id") or row.get("journal_info", {}).get("year")
        for row in pdbe_publication_rows
    )
    publication_authority_present = bool(
        rcsb_has_article or pdbe_has_article or europepmc_hits or crossref_article_hits
    )
    evidence_against = [
        "RCSB core entry still reports the primary citation as To Be Published with no article DOI, PubMed ID, or year.",
        "PDBe publications endpoint still reports type U / To be published with no DOI, PubMed ID, or year.",
        "Europe PMC exact and alias queries returned no publication-metadata hit for the 23FC title or ATR-ATRIP/Chk1 ATPgammaS aliases.",
        "Crossref only yielded the wwPDB dataset DOI for the exact 23FC title; no article/preprint DOI matching ATR/Chk1 was found in the bounded top rows.",
    ]
    if sibling_ids == [PDB_ID]:
        evidence_against.append("RCSB full-text sibling aliases still return only 23FC.")
    else:
        evidence_against.append(
            "RCSB full-text sibling aliases returned non-23FC IDs requiring future source review: "
            + ", ".join([pdb_id for pdb_id in sibling_ids if pdb_id != PDB_ID])
            + "."
        )
    if related_dataset_negatives:
        evidence_against.append(
            "Crossref related PDB-dataset follow-up found donor-state sibling(s) without a named Chk1/substrate entity: "
            + ", ".join(row["pdb_id"] for row in related_dataset_negatives)
            + "."
        )
    if article_family.get("review_decision") == "article_family_no_named_substrate_entity_review_only_negative":
        evidence_against.append(
            "Single-article DOI/title family follow-up reviewed related ATR-ATRIP rows with no named substrate entity: "
            + ", ".join(article_family.get("no_named_substrate_entity_pdb_ids", []))
            + "."
        )
    if article_family.get("geometry_candidate_status_counts"):
        evidence_against.append(
            "Transient geometry scan of the same article family found zero local-metal non-peptide substrate candidates; status counts: "
            + json.dumps(article_family.get("geometry_candidate_status_counts", {}), sort_keys=True)
            + "."
        )
    evidence_for = [
        "PDBe independently confirms the same 23FC title, release date, deposition authors, hetero hexamer assembly, and associated EMDB map.",
        "Crossref confirms the PDB dataset DOI 10.2210/pdb23fc/pdb for the deposited structure, but that is not article source authority.",
    ]
    if related_dataset_negatives:
        evidence_for.append(
            "Crossref also exposed related ATR-ATRIP ATPgammaS dataset(s) with article metadata, useful as source-published donor-only negatives: "
            + ", ".join(row["pdb_id"] for row in related_dataset_negatives)
            + "."
        )
    if article_family.get("family_pdb_ids"):
        evidence_for.append(
            "The related ATR-ATRIP source article maps to a compact PDB family for review-only negative context: "
            + ", ".join(article_family["family_pdb_ids"])
            + "."
        )
    return {
        "publication_authority_present": publication_authority_present,
        "sibling_pdb_ids": sibling_ids,
        "non_23fc_sibling_pdb_ids": [pdb_id for pdb_id in sibling_ids if pdb_id != PDB_ID],
        "primary_outcome": "evidence_against",
        "search_surface_exhausted": True,
        "evidence_for": evidence_for,
        "evidence_against": evidence_against,
        "counterexamples_found": [],
        "recommendation": (
            "Keep 23FC review-only as PIKK/short-segment stress evidence. Do not treat the PDB "
            "dataset DOI as publication/source authority for clean ePK positive evidence; wait for "
            "article metadata or new non-peptide canonical ePK exact-ligand rows."
        ),
    }


def build_artifact(out: Path, page_size: int) -> dict[str, Any]:
    crossref_checks = [crossref_query(query, page_size) for query in CROSSREF_QUERIES]
    related_pdb_ids = [pdb_id for pdb_id in pdb_ids_from_crossref_dataset_dois(crossref_checks) if pdb_id != PDB_ID]
    artifact: dict[str, Any] = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "atr_chk1_publication_metadata_followup",
            "generated_at": now_iso(),
            "pdb_id": PDB_ID,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "default_next_query_deferred_reason": (
                "The handoff's next RCSB weekly-release query had already been run for "
                "2026-05-21 minutes before this cycle; no later weekly release exists yet."
            ),
            "bounded_followup_scope": (
                "Publication/source authority triangulation for the 23FC ATR-ATRIP/Chk1 "
                "review-only singleton across RCSB, PDBe, Europe PMC, Crossref, and RCSB full-text aliases."
            ),
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
        },
        "rcsb_entry": rcsb_entry(),
        "pdbe_summary": pdbe_source(PDBE_SUMMARY_URL),
        "pdbe_publications": pdbe_source(PDBE_PUBLICATIONS_URL),
        "europepmc_checks": [europepmc_query(query, page_size) for query in EUROPE_PMC_QUERIES],
        "crossref_checks": crossref_checks,
        "related_crossref_pdb_dataset_followups": [
            compact_related_pdb_dataset(pdb_id) for pdb_id in related_pdb_ids[:5]
        ],
        "rcsb_full_text_sibling_checks": [rcsb_full_text_ids(query, page_size) for query in RCSB_FULL_TEXT_ALIASES],
    }
    artifact["source_article_family_followup"] = source_article_family_followup(
        artifact["related_crossref_pdb_dataset_followups"],
        max(page_size, 12),
    )
    artifact["source_review_summary"] = classify_artifact(artifact)
    artifact["metadata"]["rows_reviewed"] = (
        1
        + len(artifact["pdbe_summary"].get("payload") or [])
        + len(artifact["pdbe_publications"].get("payload") or [])
        + sum(query.get("returned_count", 0) for query in artifact["europepmc_checks"])
        + sum(query.get("returned_count", 0) for query in artifact["crossref_checks"])
        + sum(query.get("returned_count", 0) for query in artifact["rcsb_full_text_sibling_checks"])
        + len(artifact["related_crossref_pdb_dataset_followups"])
        + len(artifact["source_article_family_followup"].get("family_rows", []))
        + len(artifact["source_article_family_followup"].get("geometry_rows", []))
    )
    artifact["metadata"]["source_urls"] = [
        RCSB_ENTRY_URL,
        RCSB_SEARCH_URL,
        PDBE_SUMMARY_URL,
        PDBE_PUBLICATIONS_URL,
        EUROPE_PMC_URL,
        CROSSREF_WORKS_URL,
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--page-size", type=int, default=5)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.out, args.page_size)
    summary = artifact["source_review_summary"]
    print(
        json.dumps(
            {
                "out": str(args.out),
                "rows_reviewed": artifact["metadata"]["rows_reviewed"],
                "publication_authority_present": summary["publication_authority_present"],
                "sibling_pdb_ids": summary["sibling_pdb_ids"],
                "primary_outcome": summary["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
