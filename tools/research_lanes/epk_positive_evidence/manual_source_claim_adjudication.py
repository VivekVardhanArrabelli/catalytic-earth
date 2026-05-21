#!/usr/bin/env python3
"""Manually adjudicate source-claim-unconfirmed ePK candidate rows.

This lane helper follows up the seven candidate rows that were already
source-mapped by `candidate_source_adjudication.py` but still lacked a clear
source claim. It records compact source surfaces and candidate-level manual
decisions only. It does not write raw coordinates, raw article text,
production labels, scoring features, thresholds, registries, fingerprints, or
migration artifacts.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE_ID = "epk_positive_evidence"
SCHEMA_VERSION = "epk_candidate_manual_source_adjudication_v1"
INPUT_PATH = Path(
    "artifacts/research_lanes/epk_positive_evidence/"
    "candidate_source_adjudication_all_20260521.json"
)
OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_positive_evidence/"
    "manual_source_claim_adjudication_20260521.json"
)
RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
RCSB_POLYMER_ENTITY_URL = "https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}"
EUROPEPMC_SEARCH_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
PMC_ARTICLE_URL = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/{accession}.json"
USER_AGENT = "catalytic-earth-epk-positive-evidence/1.0"
PMC_USER_AGENT = "Mozilla/5.0 (compatible; catalytic-earth-epk-positive-evidence/1.0)"

TARGET_CANDIDATE_IDS = [
    "1L3R:transition_analog:AF3:E:400:I:21:1",
    "4DFX:active_gamma:ANP:E:402:I:21:1",
    "4DG0:active_gamma:ANP:E:402:I:21:1",
    "4EKK:active_gamma:ANP:B:associated_entity_1:D:6:3",
    "7B56:active_gamma:ANP:B:401:A:822:1",
    "7KL1:active_gamma:ATP:C:1401:A:176:2",
    "7KL1:active_gamma:ATP:D:1401:B:176:1",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_json(url: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 30, user_agent: str = USER_AGENT) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def parse_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


def compact_rcsb_entry(pdb_id: str) -> dict[str, Any]:
    url = RCSB_ENTRY_URL.format(pdb_id=pdb_id)
    try:
        entry = fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - compact source check artifact.
        return {"pdb_id": pdb_id, "source_url": url, "fetch_error": repr(exc)}
    citation = (entry.get("citation") or [{}])[0]
    return {
        "pdb_id": pdb_id,
        "source_url": url,
        "structure_title": (entry.get("struct") or {}).get("title"),
        "citation_title": citation.get("title"),
        "citation_doi": citation.get("pdbx_database_id_doi")
        or citation.get("pdbx_database_id_DOI"),
        "citation_pubmed_id": citation.get("pdbx_database_id_pub_med")
        or citation.get("pdbx_database_id_PubMed"),
        "citation_year": citation.get("year"),
        "deposition_date": (entry.get("rcsb_accession_info") or {}).get("deposit_date"),
        "initial_release_date": (entry.get("rcsb_accession_info") or {}).get(
            "initial_release_date"
        ),
    }


def compact_polymer_entities(pdb_id: str) -> dict[str, Any]:
    entry_url = RCSB_ENTRY_URL.format(pdb_id=pdb_id)
    try:
        entry = fetch_json(entry_url)
    except Exception as exc:  # noqa: BLE001 - compact source check artifact.
        return {"pdb_id": pdb_id, "entry_source_url": entry_url, "fetch_error": repr(exc)}
    entity_ids = (entry.get("rcsb_entry_container_identifiers") or {}).get(
        "polymer_entity_ids", []
    )
    entities = []
    for entity_id in entity_ids:
        entity_url = RCSB_POLYMER_ENTITY_URL.format(pdb_id=pdb_id, entity_id=entity_id)
        try:
            entity = fetch_json(entity_url)
        except Exception as exc:  # noqa: BLE001 - compact source check artifact.
            entities.append(
                {"entity_id": entity_id, "source_url": entity_url, "fetch_error": repr(exc)}
            )
            continue
        identifiers = entity.get("rcsb_polymer_entity_container_identifiers") or {}
        entities.append(
            {
                "entity_id": entity_id,
                "source_url": entity_url,
                "description": (entity.get("rcsb_polymer_entity") or {}).get(
                    "pdbx_description"
                ),
                "sample_sequence_length": (entity.get("entity_poly") or {}).get(
                    "rcsb_sample_sequence_length"
                ),
                "auth_asym_ids": identifiers.get("auth_asym_ids", []),
                "asym_ids": identifiers.get("asym_ids", []),
                "uniprot_ids": identifiers.get("uniprot_ids", []),
                "reference_sequence_identifiers": identifiers.get(
                    "reference_sequence_identifiers", []
                ),
                "alignments": entity.get("rcsb_polymer_entity_align", []),
                "raw_sequence_stored": False,
            }
        )
    return {"pdb_id": pdb_id, "entry_source_url": entry_url, "polymer_entities": entities}


def compact_europepmc_query(query: str, page_size: int = 3) -> dict[str, Any]:
    url = EUROPEPMC_SEARCH_URL + "?" + urllib.parse.urlencode(
        {
            "query": query,
            "format": "json",
            "pageSize": page_size,
            "resultType": "core",
        }
    )
    try:
        payload = fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - compact source check artifact.
        return {"query": query, "source_url": url, "fetch_error": repr(exc)}
    rows = []
    for result in (payload.get("resultList") or {}).get("result", [])[:page_size]:
        rows.append(
            {
                "id": result.get("id"),
                "pmid": result.get("pmid"),
                "pmcid": result.get("pmcid"),
                "doi": result.get("doi"),
                "title": result.get("title"),
                "pub_year": result.get("pubYear"),
                "is_open_access": result.get("isOpenAccess"),
                "in_europe_pmc": result.get("inEPMC"),
            }
        )
    return {
        "query": query,
        "source_url": url,
        "hit_count": payload.get("hitCount"),
        "results": rows,
    }


def article_term_counts(pmcid: str, terms: list[str]) -> dict[str, Any]:
    url = PMC_ARTICLE_URL.format(pmcid=pmcid)
    try:
        html = fetch_text(url, user_agent=PMC_USER_AGENT)
    except Exception as exc:  # noqa: BLE001 - compact source check artifact.
        return {"pmcid": pmcid, "source_url": url, "fetch_error": repr(exc)}
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    counts = {
        term: len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
        for term in terms
    }
    return {
        "pmcid": pmcid,
        "source_url": url,
        "text_length_checked": len(text),
        "term_counts": {term: count for term, count in counts.items() if count},
        "raw_text_stored": False,
    }


def compact_uniprot_site_check(accession: str, positions: list[int]) -> dict[str, Any]:
    url = UNIPROT_URL.format(accession=urllib.parse.quote(accession))
    try:
        payload = fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - compact source check artifact.
        return {
            "accession": accession,
            "positions": sorted(positions),
            "source_url": url,
            "fetch_error": repr(exc),
        }
    wanted = set(positions)
    features = []
    for feature in payload.get("features", []) or []:
        location = feature.get("location") or {}
        start = parse_int((location.get("start") or {}).get("value"))
        end = parse_int((location.get("end") or {}).get("value"))
        if start is None or end is None:
            continue
        if not any(start <= position <= end for position in wanted):
            continue
        evidences = []
        for evidence in (feature.get("evidences") or [])[:5]:
            evidences.append(
                {
                    "evidence_code": evidence.get("evidenceCode"),
                    "source": evidence.get("source"),
                    "id": evidence.get("id"),
                }
            )
        features.append(
            {
                "type": feature.get("type"),
                "description": feature.get("description"),
                "begin": start,
                "end": end,
                "evidences": evidences,
            }
        )
    protein = payload.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {})
    return {
        "accession": accession,
        "positions": sorted(wanted),
        "source_url": url,
        "protein_name": protein.get("value"),
        "features_at_positions": features,
    }


def load_target_rows() -> list[dict[str, Any]]:
    payload = json.loads(INPUT_PATH.read_text())
    by_id = {row["candidate_id"]: row for row in payload["adjudicated_candidate_rows"]}
    missing = [candidate_id for candidate_id in TARGET_CANDIDATE_IDS if candidate_id not in by_id]
    if missing:
        raise SystemExit(f"missing target candidate rows: {missing}")
    return [by_id[candidate_id] for candidate_id in TARGET_CANDIDATE_IDS]


def decision_for_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    if candidate_id.startswith("1L3R:"):
        return {
            "manual_source_claim_status": "source_supported_transition_or_pseudosubstrate_review_only",
            "manual_claim_summary": (
                "RCSB and literature metadata identify 1L3R as a PKA transition-state "
                "mimic; open PKA follow-up text maps 1L3R to an SP20/PKI-derived "
                "substrate peptide context with Ser21 discussed as the substrate serine."
            ),
            "source_support_level": "review_only_positive_support",
            "manual_signal_tags": [
                "manual_source_supported",
                "transition_mimic",
                "pki_derived_sp20_peptide",
                "peptide_or_short_non_countable",
            ],
            "manual_blockers": [
                "transition_or_product_analog_state_not_countable",
                "peptide_short_or_unknown_substrate_context",
                "review_only_lane",
            ],
        }
    if candidate_id.startswith("4DFX:") or candidate_id.startswith("4DG0:"):
        return {
            "manual_source_claim_status": "source_supported_sp20_substrate_peptide_review_only",
            "manual_claim_summary": (
                "The primary structures are PKA/SP20/AMP-PNP ternary complexes. "
                "Open follow-up PKA phosphoryl-transfer text describes SP20 as a "
                "PKI-derived peptide mutated from inhibitor to substrate and cites "
                "4DG0 as substrate-bound active-site context; 4DFX is the same "
                "SP20/AMP-PNP/Mg ternary family."
            ),
            "source_support_level": "review_only_positive_support",
            "manual_signal_tags": [
                "manual_source_supported",
                "sp20_substrate_peptide",
                "active_gamma",
                "local_metal",
                "peptide_or_short_non_countable",
            ],
            "manual_blockers": [
                "peptide_short_or_unknown_substrate_context",
                "review_only_lane",
            ],
        }
    if candidate_id == "4EKK:active_gamma:ANP:B:associated_entity_1:D:6:3":
        return {
            "manual_source_claim_status": "source_refuted_adjacent_nonphosphosite_no_local_metal_review_only",
            "manual_claim_summary": (
                "The candidate maps to GSK3-beta Thr8, adjacent to the source-supported "
                "Akt/GSK3 Ser9 site. UniProt feature context supports Ser9, not Thr8; "
                "this row also lacks local Mg/Mn, so it remains non-countable negative "
                "support for candidate-level residue specificity."
            ),
            "source_support_level": "evidence_against_candidate_claim",
            "manual_signal_tags": [
                "manual_source_refuted",
                "adjacent_nonphosphosite",
                "no_local_metal",
                "residue_specificity_counterexample",
            ],
            "manual_blockers": [
                "candidate_residue_not_source_phosphosite",
                "no_local_mg_or_mn",
                "review_only_lane",
            ],
        }
    if candidate_id.startswith("7B56:"):
        return {
            "manual_source_claim_status": "source_absent_actinin_binding_context_review_only",
            "manual_claim_summary": (
                "RCSB exposes a CaMKII/alpha-actinin AMPPNP structure without article "
                "DOI/PubMed metadata. Exact Europe PMC Ser822/7B56 surfaces found no "
                "phosphoacceptor claim, and later CaMKII/actinin preprint and "
                "peer-reviewed article metadata frame the complex as structural "
                "actinin binding rather than an alpha-actinin Ser822 transfer-state "
                "substrate claim."
            ),
            "source_support_level": "source_absent_or_unconfirmed",
            "manual_signal_tags": [
                "manual_source_unconfirmed",
                "actinin_binding_context",
                "no_exact_ser822_source_claim",
                "active_gamma_local_geometry_non_countable",
            ],
            "manual_blockers": [
                "source_claim_absent",
                "candidate_mapping_not_sifts_confirmed_for_auth_ser822",
                "review_only_lane",
            ],
        }
    if candidate_id.startswith("7KL1:"):
        return {
            "manual_source_claim_status": "counterexample_wrong_acceptor_or_donor_ownership_review_only",
            "manual_claim_summary": (
                "The source-supported substrate context is GluN2B, specifically a "
                "phosphomimetic S1303D peptide in 7KL1. The candidate rows instead "
                "map the acceptor to CaMKII Thr176 inside the kinase domain, so they "
                "are donor/acceptor ownership false positives rather than substrate "
                "phosphoacceptor evidence."
            ),
            "source_support_level": "counterexample",
            "manual_signal_tags": [
                "manual_counterexample",
                "wrong_acceptor_chain",
                "donor_ownership_confounded",
                "glun2b_s1303d_phosphomimetic_context",
            ],
            "manual_blockers": [
                "candidate_residue_is_kinase_domain_not_substrate_site",
                "source_substrate_is_glun2b_s1303d_not_camkii_thr176",
                "review_only_lane",
            ],
        }
    raise ValueError(f"unhandled candidate: {candidate_id}")


def build_candidate_row(candidate: dict[str, Any]) -> dict[str, Any]:
    decision = decision_for_candidate(candidate)
    return {
        "schema_version": SCHEMA_VERSION,
        "input_schema_version": candidate.get("schema_version"),
        "lane_id": LANE_ID,
        "candidate_id": candidate["candidate_id"],
        "pdb_id": candidate["pdb_id"],
        "coordinate_state": candidate["coordinate_state"],
        "prior_source_adjudication_status": candidate.get("source_adjudication_status"),
        **decision,
        "policy_decision": "review_only_abstain",
        "claim_status": "candidate_review_only_non_countable",
        "countable_label_candidate": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "ready_for_label_import": False,
        "ready_for_production_scoring": False,
        "source_review_not_predictive_coordinate_feature": True,
        "source_free_geometry": candidate.get("source_free_geometry"),
        "source_context": {
            "structure_title": candidate.get("source_context", {}).get("structure_title"),
            "citation_title": candidate.get("source_context", {}).get("citation_title"),
            "citation_doi": candidate.get("source_context", {}).get("citation_doi"),
            "citation_pubmed_id": candidate.get("source_context", {}).get("citation_pubmed_id"),
            "candidate_entity_description": candidate.get("source_context", {}).get(
                "candidate_entity_description"
            ),
            "associated_kinase_entity_description": candidate.get("source_context", {}).get(
                "associated_kinase_entity_description"
            ),
            "candidate_position_hints": candidate.get("source_context", {}).get(
                "candidate_position_hints"
            ),
            "uniprot_feature_checks": candidate.get("source_context", {}).get(
                "uniprot_feature_checks"
            ),
        },
    }


def build_source_surfaces() -> dict[str, Any]:
    rcsb_ids = sorted({candidate_id.split(":")[0] for candidate_id in TARGET_CANDIDATE_IDS})
    return {
        "rcsb_entry_metadata": [compact_rcsb_entry(pdb_id) for pdb_id in rcsb_ids],
        "rcsb_polymer_entity_context": [
            compact_polymer_entities(pdb_id) for pdb_id in rcsb_ids
        ],
        "europepmc_metadata_queries": [
            compact_europepmc_query('DOI:"10.1038/nsb780"'),
            compact_europepmc_query(
                '"1L3R" "PKI" "Ser21"'
            ),
            compact_europepmc_query('DOI:"10.1016/j.jmb.2012.05.021"'),
            compact_europepmc_query('"4DFX" OR "4DG0" "SP20" "AMP-PNP"'),
            compact_europepmc_query('DOI:"10.1126/scisignal.2002618"'),
            compact_europepmc_query('"GSK3 beta" "Thr8" Akt phosphorylation'),
            compact_europepmc_query('"GSK3 beta" "Ser9" Akt phosphorylation'),
            compact_europepmc_query('"7B56" "Ser822"'),
            compact_europepmc_query('"alpha-actinin-2" "Ser822" phosphorylation'),
            compact_europepmc_query('"CaMKII" "alpha-actinin" "Ser822"'),
            compact_europepmc_query('DOI:"10.1523/JNEUROSCI.0795-25.2025"'),
            compact_europepmc_query(
                '"Widely used CaMKII regulatory segment mutations cause tight actinin binding" "7B56"'
            ),
            compact_europepmc_query(
                '"CaMKII binds both substrates and activators at the active site"'
            ),
            compact_europepmc_query('"7KL1" "GluN2B" "S1303D"'),
        ],
        "pmc_term_checks": [
            article_term_counts(
                "PMC4505467",
                [
                    "1L3R",
                    "PKI",
                    "SP20",
                    "Ser21",
                    "transition state",
                    "substrate",
                    "ADP",
                    "MgF",
                ],
            ),
            article_term_counts(
                "PMC3663052",
                [
                    "1L3R",
                    "4DG0",
                    "PKI",
                    "SP20",
                    "Ser21",
                    "transition state",
                    "substrate",
                    "AMP-PNP",
                ],
            ),
            article_term_counts(
                "PMC3597442",
                [
                    "4DFX",
                    "4DG0",
                    "SP20",
                    "AMP-PNP",
                    "PKI",
                    "Ser21",
                    "substrate",
                    "ternary",
                ],
            ),
            article_term_counts(
                "PMC9336311",
                [
                    "7KL1",
                    "GluN2B",
                    "S1303D",
                    "Thr176",
                    "actinin",
                    "substrate",
                    "gamma phosphate",
                    "covalent bond",
                ],
            ),
        ],
        "uniprot_site_authority_checks": [
            compact_uniprot_site_check("P63249", [22]),
            compact_uniprot_site_check("P63248", [22]),
            compact_uniprot_site_check("P49841", [8, 9]),
            compact_uniprot_site_check("P35609", [822]),
            compact_uniprot_site_check("Q9UQM7", [176]),
            compact_uniprot_site_check("Q13224", [1303]),
        ],
    }


def summarize(rows: list[dict[str, Any]], source_surfaces: dict[str, Any]) -> dict[str, Any]:
    state_counts = Counter(row["coordinate_state"] for row in rows)
    status_counts = Counter(row["manual_source_claim_status"] for row in rows)
    source_supported = [
        row["candidate_id"]
        for row in rows
        if row["source_support_level"] == "review_only_positive_support"
    ]
    counterexamples = [
        row["candidate_id"]
        for row in rows
        if row["source_support_level"] == "counterexample"
        or row["source_support_level"] == "evidence_against_candidate_claim"
    ]
    absent = [
        row["candidate_id"]
        for row in rows
        if row["source_support_level"] == "source_absent_or_unconfirmed"
    ]
    exact_zero_surfaces = []
    for query in source_surfaces["europepmc_metadata_queries"]:
        if query.get("hit_count") == 0:
            exact_zero_surfaces.append(query["query"])
    return {
        "primary_outcome": "evidence_for",
        "candidate_rows_reviewed": len(rows),
        "candidate_evidence_rows_emitted": 0,
        "source_supported_review_only_candidate_ids": source_supported,
        "counterexample_or_refuted_candidate_ids": counterexamples,
        "source_absent_or_unconfirmed_candidate_ids": absent,
        "coordinate_state_counts": dict(sorted(state_counts.items())),
        "manual_status_counts": dict(sorted(status_counts.items())),
        "evidence_for": [
            "1L3R is source-supported as a PKA transition-state/pseudosubstrate SP20/PKI-derived peptide row, but remains transition-analog review-only.",
            "4DFX and 4DG0 are source-supported as PKA/SP20/AMP-PNP local-metal peptide rows; SP20 support is review-only and non-countable.",
        ],
        "evidence_against": [
            "4EKK D:6 maps to GSK3-beta Thr8, adjacent to source-supported Ser9, and lacks local Mg/Mn.",
            "7KL1 candidate rows map the acceptor to CaMKII Thr176 while the source-supported substrate context is GluN2B S1303D, so donor/acceptor ownership is confounded.",
            "7B56 retains source-absent status: no exact Ser822/CaMKII-actinin source claim was found, and RCSB has no article DOI/PubMed metadata for the structure.",
            "No folded-protein local-metal active-gamma row was upgraded to countable or production-ready evidence.",
        ],
        "counterexamples_found": [
            "7KL1 wrong acceptor/donor-ownership CaMKII Thr176 rows",
            "4EKK GSK3 Thr8 adjacent-nonphosphosite/no-local-metal row",
        ],
        "search_surface_exhausted": True,
        "explicit_zero_hit_source_surfaces": exact_zero_surfaces,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Treat 1L3R/4DFX/4DG0 as review-only peptide/transition support, "
            "7KL1 and 4EKK D6 as candidate-level counterexamples, and 7B56 as "
            "source-absent local-geometry evidence. Do not import labels, tune "
            "thresholds, edit registries/fingerprints, run production scoring, or "
            "claim ePK readiness."
        ),
        "next_query": (
            "At the next RCSB weekly release, rerun current-date and 2026 "
            "canonical ePK exact-ligand surfaces plus the 23FC publication "
            "metadata check. If no new release/metadata appears, prioritize new "
            "PDB IDs with source-published non-peptide substrate phosphoacceptor "
            "mapping and exact ATP/ANP/ACP/AGS+MG/MN or ADP+AF3/ALF/BEF/MGF "
            "context; do not revisit the seven manually adjudicated rows unless "
            "new source metadata appears."
        ),
    }


def main() -> None:
    candidate_rows = [build_candidate_row(row) for row in load_target_rows()]
    source_surfaces = build_source_surfaces()
    payload = {
        "metadata": {
            "schema_version": SCHEMA_VERSION,
            "lane_id": LANE_ID,
            "generated_at": now_iso(),
            "input_artifact": str(INPUT_PATH),
            "target_candidate_ids": TARGET_CANDIDATE_IDS,
            "method": "manual_source_claim_adjudication",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinates_written": False,
            "raw_article_text_stored": False,
            "source_review_not_predictive_coordinate_feature": True,
        },
        "source_surfaces": source_surfaces,
        "manual_adjudicated_candidate_rows": candidate_rows,
        "summary": summarize(candidate_rows, source_surfaces),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
