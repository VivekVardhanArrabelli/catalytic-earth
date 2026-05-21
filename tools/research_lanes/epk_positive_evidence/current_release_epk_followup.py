#!/usr/bin/env python3
"""Current-release ePK positive-evidence follow-up.

Bounded review-only search for current/future ePK evidence. This helper:

- re-checks publication/source metadata for the 23FC ATR-ATRIP/Chk1 lead,
- scans the current release-date exact ligand surface, and
- backfills a narrow no-source-term recent-release surface to catch sparse
  RCSB text annotations.

Coordinates are fetched transiently and summarized compactly. No raw coordinate
dumps, production labels, thresholds, registries, fingerprints, migrations, or
production scoring artifacts are written.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import canonical_epk_ligand_search as canonical
import epk_evidence_search as scout
import transition_analog_seed_family_followup as transition


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
COMP_ID_ATTR = "rcsb_chem_comp_container_identifiers.comp_id"
EC_LINEAGE_ATTR = "rcsb_polymer_entity.rcsb_ec_lineage.id"
PFAM_ATTR = "rcsb_polymer_entity_annotation.annotation_id"
RELEASE_DATE_ATTR = "rcsb_accession_info.initial_release_date"


@dataclass(frozen=True)
class Surface:
    surface_id: str
    date_from: str
    date_to: str
    ligand_mode: str
    source_query: str | None = None
    rows: int = 40
    start: int = 0


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


def text_term(attribute: str, value: Any, operator: str = "exact_match") -> dict[str, Any]:
    return {
        "type": "terminal",
        "service": "text",
        "parameters": {"attribute": attribute, "operator": operator, "value": value},
    }


def full_text(value: str) -> dict[str, Any]:
    return {"type": "terminal", "service": "full_text", "parameters": {"value": value}}


def group(operator: str, nodes: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "group", "logical_operator": operator, "nodes": nodes}


def comp_group(values: list[str]) -> dict[str, Any]:
    return group("or", [text_term(COMP_ID_ATTR, value) for value in values])


def family_group() -> dict[str, Any]:
    return group(
        "or",
        [
            text_term(PFAM_ATTR, "PF00069"),
            text_term(PFAM_ATTR, "PF07714"),
            text_term(EC_LINEAGE_ATTR, "2.7.11"),
            text_term(EC_LINEAGE_ATTR, "2.7.10"),
        ],
    )


def ligand_nodes(ligand_mode: str) -> list[dict[str, Any]]:
    if ligand_mode == "gamma":
        return [comp_group(["ATP", "ANP", "ACP", "AGS"]), comp_group(["MG", "MN"])]
    if ligand_mode == "transition":
        return [text_term(COMP_ID_ATTR, "ADP"), comp_group(["AF3", "ALF", "BEF", "MGF"])]
    raise ValueError(f"unsupported ligand mode: {ligand_mode}")


def surface_query(surface: Surface) -> dict[str, Any]:
    nodes = [
        family_group(),
        text_term(RELEASE_DATE_ATTR, {"from": surface.date_from, "to": surface.date_to}, "range"),
        *ligand_nodes(surface.ligand_mode),
    ]
    if surface.source_query:
        nodes.append(full_text(surface.source_query))
    return group("and", nodes)


def search_surface(surface: Surface) -> dict[str, Any]:
    payload = {
        "query": surface_query(surface),
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": surface.start, "rows": surface.rows},
            "results_content_type": ["experimental"],
        },
    }
    result = fetch_json(RCSB_SEARCH_URL, payload=payload)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    ligand_label = (
        "ATP/ANP/ACP/AGS+MG/MN"
        if surface.ligand_mode == "gamma"
        else "ADP+AF3/ALF/BEF/MGF"
    )
    source_label = f" AND full_text='{surface.source_query}'" if surface.source_query else ""
    return {
        "surface_id": surface.surface_id,
        "query_or_source": (
            "RCSB advanced: "
            f"released {surface.date_from}..{surface.date_to} AND canonical ePK "
            f"AND {ligand_label}{source_label}"
        ),
        "date_from": surface.date_from,
        "date_to": surface.date_to,
        "ligand_mode": surface.ligand_mode,
        "source_query": surface.source_query,
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def compact_scheme_match(row: dict[str, str]) -> dict[str, str | None]:
    return {
        "asym_id": row.get("asym_id"),
        "entity_id": row.get("entity_id"),
        "seq_id": row.get("seq_id"),
        "mon_id": row.get("mon_id"),
        "pdb_seq_num": row.get("pdb_seq_num"),
        "auth_seq_num": row.get("auth_seq_num"),
        "pdb_mon_id": row.get("pdb_mon_id"),
        "auth_mon_id": row.get("auth_mon_id"),
        "pdb_strand_id": row.get("pdb_strand_id"),
        "hetero": row.get("hetero"),
    }


def polymer_lengths(metadata: dict[str, Any]) -> dict[str, int | None]:
    lengths: dict[str, int | None] = {}
    for entity_id in metadata.get("polymer_entities", {}):
        pdb_id = metadata["pdb_id"]
        try:
            entity = fetch_json(scout.RCSB_POLYMER_ENTITY_URL.format(pdb_id=pdb_id, entity_id=entity_id))
            seq = entity.get("entity_poly", {}).get("pdbx_seq_one_letter_code_can") or ""
            lengths[str(entity_id)] = len("".join(seq.split())) if seq else None
        except Exception:  # noqa: BLE001 - noncritical context field.
            lengths[str(entity_id)] = None
    return lengths


def add_entity_lengths(row: dict[str, Any]) -> None:
    lengths = polymer_lengths(row)
    row["polymer_entity_lengths"] = lengths
    for hit in row.get("heteromeric_candidate_hits", []):
        hit["candidate_entity_length"] = lengths.get(str(hit.get("candidate_entity_id")))
    for hit in row.get("transition_analog_candidate_hits", []):
        hit["candidate_entity_length"] = lengths.get(str(hit.get("candidate_entity_id")))


def add_sequence_scheme_matches(row: dict[str, Any], cif_text: str) -> None:
    scheme_rows = scout.extract_loop(cif_text, "pdbx_poly_seq_scheme")
    for hit_list_name in ("heteromeric_candidate_hits", "transition_analog_candidate_hits"):
        for hit in row.get(hit_list_name, []):
            entity_id = str(hit.get("candidate_entity_id"))
            chain = hit.get("candidate_chain_name")
            auth_seq = str(hit.get("candidate_auth_seq_id"))
            label_seq = str(hit.get("candidate_label_seq_id"))
            residue_code = hit.get("candidate_residue_code")
            matches = []
            for scheme in scheme_rows:
                if str(scheme.get("entity_id")) != entity_id:
                    continue
                if scheme.get("pdb_strand_id") != chain:
                    continue
                sequence_match = (
                    scheme.get("auth_seq_num") == auth_seq
                    or scheme.get("pdb_seq_num") == auth_seq
                    or scheme.get("seq_id") == label_seq
                )
                residue_match = residue_code in {
                    scheme.get("mon_id"),
                    scheme.get("pdb_mon_id"),
                    scheme.get("auth_mon_id"),
                }
                if sequence_match and residue_match:
                    matches.append(compact_scheme_match(scheme))
            hit["candidate_sequence_scheme_matches"] = matches
            hit["candidate_source_mapped"] = bool(matches)


def is_nonpeptide_candidate(hit: dict[str, Any]) -> bool:
    description = (hit.get("candidate_entity_description") or "").lower()
    length = hit.get("candidate_entity_length")
    if "peptide" in description or "pseudo" in description or "inhibitor" in description:
        return False
    return bool(length and length >= 50)


def classify_row(row: dict[str, Any]) -> str:
    canonical_local = [
        hit
        for hit in row.get("heteromeric_candidate_hits", [])
        if hit.get("has_local_mg_or_mn")
    ]
    transition_local = [
        hit
        for hit in row.get("transition_analog_candidate_hits", [])
        if hit.get("has_local_mg_or_mn")
    ]
    all_local = canonical_local + transition_local
    if any(is_nonpeptide_candidate(hit) for hit in all_local):
        return "local_metal_nonpeptide_candidate_source_validation_pending_review_only"
    if all_local:
        return "local_metal_peptide_or_short_candidate_review_only"
    if row.get("heteromeric_candidate_hits") or row.get("transition_analog_candidate_hits"):
        return "no_local_metal_or_short_candidate_review_only"
    if row.get("terminal_donor_atom_count") or row.get("transition_analog_group_count"):
        return "donor_or_analog_without_heteromeric_acceptor_review_only"
    return "no_active_donor_or_transition_analog_review_only"


def compact_europepmc_query(query: str, page_size: int = 3) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {"query": query, "format": "json", "pageSize": page_size, "resultType": "core"}
    )
    url = f"{EUROPE_PMC_URL}?{params}"
    try:
        data = fetch_json(url, timeout=30)
    except Exception as exc:  # noqa: BLE001 - compact source validation artifact.
        return {"query": query, "source_url": url, "fetch_error": repr(exc)}
    results = data.get("resultList", {}).get("result", [])
    return {
        "query": query,
        "source_url": url,
        "result_count": len(results),
        "results": [
            {
                "title": row.get("title"),
                "doi": row.get("doi"),
                "pmid": row.get("pmid"),
                "pub_year": row.get("pubYear"),
                "journal": row.get("journalTitle"),
            }
            for row in results
        ],
    }


def rcsb_full_text_ids(query: str, rows: int = 10) -> dict[str, Any]:
    payload = {
        "query": full_text(query),
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "results_content_type": ["experimental"],
        },
    }
    result = fetch_json(RCSB_SEARCH_URL, payload=payload)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    return {
        "query_or_source": f"RCSB full_text: {query}",
        "returned_count": len(ids),
        "total_count": result.get("total_count", len(ids)),
        "pdb_ids": ids,
    }


def recheck_23fc() -> dict[str, Any]:
    entry_url = scout.RCSB_ENTRY_URL.format(pdb_id="23FC")
    entry = fetch_json(entry_url)
    citation = (entry.get("citation") or [{}])[0]
    accession = entry.get("rcsb_accession_info") or {}
    exact_title = "Cryo-EM structure of human ATR-ATRIP complex with ATPgammaS and Chk1"
    europepmc_checks = [
        compact_europepmc_query(f'TITLE:"{exact_title}"'),
        compact_europepmc_query('"23FC" ATR Chk1'),
        compact_europepmc_query('"ATR-ATRIP" "ATPgammaS" Chk1'),
        compact_europepmc_query('"ATR-ATRIP" "ATPgammaS" "Chk1"'),
    ]
    sibling_checks = [
        rcsb_full_text_ids("ATR ATRIP Chk1 ATPgammaS", 10),
        rcsb_full_text_ids("human ATR-ATRIP complex ATPgammaS Chk1", 10),
        rcsb_full_text_ids(exact_title, 10),
    ]
    has_publication_ids = bool(
        citation.get("pdbx_database_id_PubMed") or citation.get("pdbx_database_id_pub_med")
        or citation.get("pdbx_database_id_DOI") or citation.get("pdbx_database_id_doi")
    )
    europepmc_exact_hits = [
        check
        for check in europepmc_checks
        if not check.get("fetch_error") and check.get("result_count", 0) > 0
    ]
    return {
        "pdb_id": "23FC",
        "source_urls": [
            "https://www.rcsb.org/structure/23FC",
            entry_url,
            EUROPE_PMC_URL,
        ],
        "accession_info": {
            "deposit_date": accession.get("deposit_date"),
            "initial_release_date": accession.get("initial_release_date"),
            "revision_date": accession.get("revision_date"),
            "status_code": accession.get("status_code"),
        },
        "citation": {
            "title": citation.get("title"),
            "year": citation.get("year"),
            "pdbx_database_id_pub_med": citation.get("pdbx_database_id_PubMed")
            or citation.get("pdbx_database_id_pub_med"),
            "pdbx_database_id_doi": citation.get("pdbx_database_id_DOI")
            or citation.get("pdbx_database_id_doi"),
        },
        "publication_metadata_present_in_rcsb": has_publication_ids,
        "europepmc_checks": europepmc_checks,
        "europepmc_publication_metadata_present": bool(europepmc_exact_hits),
        "sibling_checks": sibling_checks,
        "sibling_pdb_ids": sorted({pdb_id for check in sibling_checks for pdb_id in check["pdb_ids"]}),
        "review_decision": (
            "publication_metadata_now_available_review_needed"
            if has_publication_ids or europepmc_exact_hits
            else "publication_metadata_still_absent_review_only_23fc_status_unchanged"
        ),
    }


def scan_pdb_id(pdb_id: str, search_hits: list[dict[str, Any]]) -> dict[str, Any]:
    metadata = scout.compact_entry_metadata(pdb_id)
    cif_text = scout.fetch_text(scout.RCSB_CIF_URL.format(pdb_id=pdb_id))
    canonical_scan = canonical.scan_cif_for_canonical_candidates(cif_text)
    transition_scan = transition.scan_transition_analog_candidates(cif_text)
    row = {
        **metadata,
        "search_hits": search_hits,
        "review_only": True,
        "countable_label_candidate": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "target_family_id": TARGET_FAMILY_ID,
        "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
        **canonical_scan,
        **transition_scan,
    }
    canonical.merge_hit_entity_context(row)
    transition.merge_entity_context(row)
    add_entity_lengths(row)
    add_sequence_scheme_matches(row, cif_text)
    row["candidate_status"] = classify_row(row)
    return row


def build_surfaces(current_from: str, current_to: str, backfill_from: str) -> list[Surface]:
    source_terms = [
        "substrate phosphorylation",
        "full-length substrate",
        "phosphoacceptor substrate",
    ]
    surfaces: list[Surface] = []
    for ligand_mode in ("gamma", "transition"):
        surfaces.append(
            Surface(
                f"current_release_{ligand_mode}_any",
                current_from,
                current_to,
                ligand_mode,
                None,
                50,
            )
        )
        for term in source_terms:
            safe_term = term.replace(" ", "_").replace("-", "_")
            surfaces.append(
                Surface(
                    f"current_release_{ligand_mode}_{safe_term}",
                    current_from,
                    current_to,
                    ligand_mode,
                    term,
                    50,
                )
            )
        surfaces.append(
            Surface(
                f"recent_backfill_{ligand_mode}_any_no_source_term",
                backfill_from,
                current_to,
                ligand_mode,
                None,
                60,
            )
        )
    return surfaces


def build_artifact(
    out: Path,
    current_from: str,
    current_to: str,
    backfill_from: str,
    max_unique: int,
    sleep_seconds: float,
) -> dict[str, Any]:
    generated_at = now_iso()
    source_recheck = recheck_23fc()
    search_results = []
    seen: dict[str, list[dict[str, Any]]] = {}
    for surface in build_surfaces(current_from, current_to, backfill_from):
        result = search_surface(surface)
        search_results.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1 + surface.start):
            if pdb_id not in seen and len(seen) >= max_unique:
                continue
            seen.setdefault(pdb_id, []).append(
                {"surface_id": surface.surface_id, "rank": rank, "query_or_source": result["query_or_source"]}
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    for pdb_id, search_hits in seen.items():
        try:
            rows.append(scan_pdb_id(pdb_id, search_hits))
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
    current_release_ids = sorted(
        {
            pdb_id
            for result in search_results
            if result["date_from"] == current_from and result["date_to"] == current_to
            for pdb_id in result["pdb_ids"]
        }
    )
    evidence_for = []
    if source_recheck["review_decision"] == "publication_metadata_now_available_review_needed":
        evidence_for.append("23FC publication metadata appears to be newly available and needs review.")
    if nonpeptide:
        evidence_for.append(
            "Current/recent release exact-ligand surfaces found local-metal non-peptide candidates: "
            + ", ".join(nonpeptide)
            + "."
        )
    if short_or_peptide:
        evidence_for.append(
            "Current/recent release exact-ligand surfaces found review-only short/peptide candidates: "
            + ", ".join(short_or_peptide)
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "23FC publication metadata remains absent and current/recent exact-ligand surfaces added no local-metal candidate."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "current_release_epk_followup",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "current_release_date_range": {"from": current_from, "to": current_to},
            "recent_backfill_date_range": {"from": backfill_from, "to": current_to},
            "max_unique_pdb_ids": max_unique,
            "search_surface_count": len(search_results),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_results),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_results),
            "current_release_unique_pdb_ids": current_release_ids,
            "current_release_unique_count": len(current_release_ids),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_nonpeptide_candidate_pdb_ids": nonpeptide,
            "local_metal_peptide_or_short_candidate_pdb_ids": short_or_peptide,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Current-release/recent-backfill search only. It does not create labels, "
                "scores, thresholds, fingerprints, migrations, or production claims."
            ),
            "source_urls": [
                RCSB_SEARCH_URL,
                scout.RCSB_ENTRY_URL,
                scout.RCSB_POLYMER_ENTITY_URL,
                scout.RCSB_CIF_URL,
                EUROPE_PMC_URL,
            ],
        },
        "source_recheck_23fc": source_recheck,
        "search_surfaces": search_results,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": (
                "next_query_defined"
                if nonpeptide
                else "evidence_for"
                if short_or_peptide or source_recheck["review_decision"] == "publication_metadata_now_available_review_needed"
                else "search_surface_exhausted"
            ),
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(nonpeptide),
            "evidence_for": evidence_for,
            "evidence_against": [
                "No clean non-topology-confounded folded-protein canonical ePK substrate positive was promoted.",
                "23FC remains review-only unless publication metadata and folded-substrate context become available.",
                "Current release-date rows require source-mapped non-peptide acceptor geometry before any follow-up.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "Do not change production labels, thresholds, registries, fingerprints, migrations, "
                "or scoring. If current-release rows remain empty, next search should move to a "
                "bounded source-text literature pass over newly published kinase-substrate structures."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--current-from", default="2026-05-21")
    parser.add_argument("--current-to", default="2026-05-21")
    parser.add_argument("--backfill-from", default="2026-05-13")
    parser.add_argument("--max-unique", type=int, default=80)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.current_from,
        args.current_to,
        args.backfill_from,
        args.max_unique,
        args.sleep_seconds,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "current_release_unique_count": artifact["metadata"]["current_release_unique_count"],
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "local_metal_nonpeptide_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_nonpeptide_candidate_pdb_ids"
                ],
                "local_metal_peptide_or_short_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_peptide_or_short_candidate_pdb_ids"
                ],
                "publication_metadata_present_in_rcsb": artifact["source_recheck_23fc"][
                    "publication_metadata_present_in_rcsb"
                ],
                "europepmc_publication_metadata_present": artifact["source_recheck_23fc"][
                    "europepmc_publication_metadata_present"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
