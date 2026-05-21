#!/usr/bin/env python3
"""Source-adjudicate review-only ePK candidate evidence rows.

This helper reads `epk_candidate_evidence_v1` rows, selects a bounded priority
set, refreshes compact source context from RCSB/UniProt/Europe PMC, and emits
candidate-level source-adjudication rows. It does not write raw coordinates,
labels, production scores, thresholds, registries, fingerprints, migrations, or
production claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import current_release_epk_followup as current
import guarded_phrase_candidate_rows as guarded


LANE_ID = "epk_positive_evidence"
SCHEMA_VERSION = "epk_candidate_source_adjudication_v1"
INPUT_SCHEMA_VERSION = "epk_candidate_evidence_v1"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
DEFAULT_CANDIDATE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_positive_evidence/prior_candidate_evidence_rows_20260521.json"
)
UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/{accession}.json"
PDB_ID_RE = re.compile(r"^[0-9][A-Za-z0-9]{3}$")
NUMERIC_RE = re.compile(r"^-?\d+$")

ANCHOR_PDB_IDS = {
    "23FC",
    "5HVK",
    "9UUR",
    "9UUX",
    "3X2U",
    "3X2V",
    "3X2W",
    "1QMZ",
    "1L3R",
    "5LIH",
    "1HE1",
}

COUNTEREXAMPLE_TERMS = (
    "atp synthase",
    "atp-binding/permease",
    "abc transporter",
    "cydd",
    "cydc",
    "f1-atpase",
    "exoenzyme s",
    "exos",
    "human rac",
    "rac gtpase",
    "gap domain",
    "gtpase",
    "mcm2-7",
    "minichromosome maintenance",
    "mcm c-terminal aaa",
    "mcm helicase",
    "26s proteasome",
    "proteasome regulatory subunit",
    "aaa+ motor",
    "circadian clock protein kinase kaic",
)

SOURCE_SUPPORT_TERMS = (
    "substrate",
    "michaelis",
    "phosphorylation",
    "phospho",
    "pseudosubstrate",
    "peptide",
    "phospholamban",
    "cofilin",
    "p53",
    "chk1",
    "cdc6",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def fetch_json(url: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(
        url, headers={"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def compact_evidence(evidences: Any, limit: int = 5) -> list[dict[str, Any]]:
    if not isinstance(evidences, list):
        return []
    compact = []
    for item in evidences[:limit]:
        if isinstance(item, dict):
            compact.append(
                {
                    "evidence_code": item.get("evidenceCode"),
                    "source": item.get("source"),
                    "id": item.get("id"),
                }
            )
    return compact


def parse_int(value: Any) -> int | None:
    if value is None:
        return None
    token = str(value)
    if not NUMERIC_RE.match(token):
        return None
    return int(token)


def has_tag(row: dict[str, Any], tag: str) -> bool:
    return tag in row.get("signal_tags", [])


def candidate_kind(row: dict[str, Any]) -> str:
    tags = row.get("signal_tags", [])
    for tag in ("folded_protein", "folded_protein_length_unknown", "peptide_or_short", "short_or_unknown"):
        if tag in tags:
            return tag
    description = (row.get("source_context", {}).get("candidate_entity_description") or "").lower()
    if "peptide" in description or "pseudo" in description or "inhibitor" in description:
        return "peptide_or_short"
    return "unknown"


def row_priority(row: dict[str, Any]) -> int:
    pdb_id = row.get("pdb_id")
    if (
        row.get("coordinate_state") == "active_gamma"
        and has_tag(row, "local_metal")
        and has_tag(row, "source_mapping_pending")
    ):
        return 0
    if has_tag(row, "source_mapping_pending") and candidate_kind(row) in {
        "folded_protein",
        "folded_protein_length_unknown",
    }:
        return 1
    if pdb_id in ANCHOR_PDB_IDS:
        return 2
    return 9


def select_candidate_rows(
    rows: list[dict[str, Any]],
    max_pdb_ids: int,
    include_all: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    eligible = rows[:] if include_all else [row for row in rows if row_priority(row) < 9]
    eligible.sort(
        key=lambda row: (
            row_priority(row),
            row.get("pdb_id", ""),
            row.get("candidate_id", ""),
        )
    )
    selected: list[dict[str, Any]] = []
    selected_pdb_ids: set[str] = set()
    deferred: list[str] = []
    for row in eligible:
        pdb_id = str(row.get("pdb_id", "")).upper()
        if not PDB_ID_RE.match(pdb_id):
            continue
        if pdb_id not in selected_pdb_ids and len(selected_pdb_ids) >= max_pdb_ids:
            deferred.append(row.get("candidate_id", pdb_id))
            continue
        selected.append(row)
        selected_pdb_ids.add(pdb_id)
    sets = {
        "max_unique_pdb_ids": max_pdb_ids,
        "selected_unique_pdb_ids": sorted(selected_pdb_ids),
        "selected_candidate_row_count": len(selected),
        "deferred_candidate_ids": deferred,
        "priority_rule": [
            "active_gamma + local_metal + source_mapping_pending",
            "folded_protein/folded_protein_length_unknown + source_mapping_pending",
            "named stress anchors",
            "all candidate rows" if include_all else "other candidate rows deferred",
        ],
        "include_all_candidate_rows": include_all,
    }
    return selected, sets


def search_hits_for_pdb(rows: list[dict[str, Any]], pdb_id: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    seen: set[tuple[Any, Any, Any]] = set()
    for row in rows:
        if str(row.get("pdb_id", "")).upper() != pdb_id:
            continue
        for hit in row.get("source_context", {}).get("search_hits", []):
            key = (hit.get("surface_id"), hit.get("rank"), hit.get("query_or_source"))
            if key not in seen:
                seen.add(key)
                hits.append(hit)
    if not hits:
        hits.append(
            {
                "surface_id": "candidate_source_adjudication",
                "rank": None,
                "query_or_source": "prior epk_candidate_evidence_v1 source adjudication target",
            }
        )
    return hits


def scan_selected_pdb_ids(
    selected: list[dict[str, Any]],
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    scans: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    for pdb_id in sorted({str(row["pdb_id"]).upper() for row in selected}):
        try:
            scans[pdb_id] = guarded.scan_pdb_id_guarded(
                pdb_id,
                search_hits_for_pdb(selected, pdb_id),
                max_cif_bytes=max_cif_bytes,
                row_timeout_seconds=row_timeout_seconds,
            )
        except Exception as exc:  # noqa: BLE001 - source review artifact records compact failures.
            failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            scans[pdb_id] = {
                "pdb_id": pdb_id,
                "candidate_status": "source_refresh_failed_review_only",
                "fetch_error": repr(exc),
                "review_only": True,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "epk_score_computed": False,
                "ready_for_production_scoring": False,
                "ready_for_label_import": False,
            }
        if sleep_seconds:
            time.sleep(sleep_seconds)
    return scans, failures


def hit_lists_for_state(scan_row: dict[str, Any], coordinate_state: str) -> list[dict[str, Any]]:
    if coordinate_state == "transition_analog":
        return scan_row.get("transition_analog_candidate_hits", []) or []
    return scan_row.get("heteromeric_candidate_hits", []) or []


def match_candidate_to_refreshed_hit(
    candidate: dict[str, Any],
    scan_row: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not scan_row:
        return None
    geometry = candidate.get("source_free_geometry", {})
    state = candidate.get("coordinate_state")
    for hit in hit_lists_for_state(scan_row, state):
        if str(hit.get("candidate_chain_name")) != str(geometry.get("candidate_chain_name")):
            continue
        if str(hit.get("candidate_auth_seq_id")) != str(geometry.get("candidate_auth_seq_id")):
            continue
        if str(hit.get("candidate_residue_code")) != str(geometry.get("candidate_residue_code")):
            continue
        if str(hit.get("candidate_atom_name")) != str(geometry.get("candidate_atom_name")):
            continue
        if state == "transition_analog":
            if str(hit.get("analog_ligand_code")) != str(geometry.get("analog_ligand_code")):
                continue
        else:
            terminal_code = hit.get("terminal_ligand_code") or hit.get("gamma_ligand_code")
            if str(terminal_code) != str(geometry.get("terminal_ligand_code")):
                continue
        return hit
    return None


def polymer_entity_context(pdb_id: str, entity_id: Any) -> dict[str, Any]:
    if entity_id in (None, "", ".", "?"):
        return {"entity_id": entity_id, "fetch_error": "missing_entity_id"}
    url = current.scout.RCSB_POLYMER_ENTITY_URL.format(pdb_id=pdb_id, entity_id=entity_id)
    try:
        entity = current.fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - compact source context only.
        return {"entity_id": entity_id, "source_url": url, "fetch_error": repr(exc)}
    identifiers = entity.get("rcsb_polymer_entity_container_identifiers") or {}
    sequence = (entity.get("entity_poly") or {}).get("pdbx_seq_one_letter_code_can") or ""
    return {
        "entity_id": str(entity_id),
        "source_url": url,
        "sample_sequence_length": (entity.get("entity_poly") or {}).get("rcsb_sample_sequence_length")
        or len("".join(sequence.split())),
        "uniprot_ids": identifiers.get("uniprot_ids", []),
        "reference_sequence_identifiers": identifiers.get("reference_sequence_identifiers", []),
        "alignments": entity.get("rcsb_polymer_entity_align", []),
    }


def uniprot_positions_from_alignment(
    entity_context: dict[str, Any],
    sequence_scheme_matches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    for match in sequence_scheme_matches:
        seq_id = parse_int(match.get("seq_id"))
        if seq_id is None:
            continue
        for alignment in entity_context.get("alignments", []) or []:
            accession = alignment.get("reference_database_accession")
            database = alignment.get("reference_database_name")
            for region in alignment.get("aligned_regions", []) or []:
                entity_beg = parse_int(region.get("entity_beg_seq_id"))
                ref_beg = parse_int(region.get("ref_beg_seq_id"))
                length = parse_int(region.get("length"))
                if entity_beg is None or ref_beg is None or length is None:
                    continue
                if entity_beg <= seq_id < entity_beg + length:
                    positions.append(
                        {
                            "database": database,
                            "accession": accession,
                            "source": "RCSB_SIFTS_alignment",
                            "entity_seq_id": seq_id,
                            "uniprot_position": ref_beg + (seq_id - entity_beg),
                        }
                    )
    return positions


def candidate_position_hints(
    candidate: dict[str, Any],
    refreshed_hit: dict[str, Any] | None,
    entity_context: dict[str, Any],
) -> list[dict[str, Any]]:
    geometry = candidate.get("source_free_geometry", {})
    hints: list[dict[str, Any]] = []
    auth_pos = parse_int(geometry.get("candidate_auth_seq_id"))
    if auth_pos is not None:
        hints.append({"source": "candidate_auth_seq_id", "position": auth_pos})
    label_pos = parse_int(geometry.get("candidate_label_seq_id"))
    if label_pos is not None:
        hints.append({"source": "candidate_label_seq_id", "position": label_pos})
    matches = []
    if refreshed_hit:
        matches = refreshed_hit.get("candidate_sequence_scheme_matches", []) or []
        for match in matches:
            for field in ("auth_seq_num", "pdb_seq_num", "seq_id"):
                pos = parse_int(match.get(field))
                if pos is not None:
                    hints.append({"source": f"pdbx_poly_seq_scheme.{field}", "position": pos})
    for mapped in uniprot_positions_from_alignment(entity_context, matches):
        hints.append(mapped)
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[Any, Any, Any]] = set()
    for hint in hints:
        key = (hint.get("source"), hint.get("accession"), hint.get("uniprot_position") or hint.get("position"))
        if key not in seen:
            seen.add(key)
            deduped.append(hint)
    return deduped


def fetch_uniprot_features(accession: str, positions: list[int]) -> dict[str, Any]:
    url = UNIPROT_URL.format(accession=urllib.parse.quote(accession))
    try:
        payload = fetch_json(url, timeout=30)
    except urllib.error.HTTPError as exc:
        return {"accession": accession, "source_url": url, "fetch_error": f"HTTPError({exc.code})"}
    except Exception as exc:  # noqa: BLE001 - compact source context only.
        return {"accession": accession, "source_url": url, "fetch_error": repr(exc)}
    wanted = set(positions)
    features = []
    for feature in payload.get("features", []) or []:
        location = feature.get("location") or {}
        start = parse_int((location.get("start") or {}).get("value"))
        end = parse_int((location.get("end") or {}).get("value"))
        if start is None or end is None:
            continue
        if not any(start <= pos <= end for pos in wanted):
            continue
        features.append(
            {
                "type": feature.get("type"),
                "description": feature.get("description"),
                "begin": start,
                "end": end,
                "evidences": compact_evidence(feature.get("evidences")),
            }
        )
    protein = payload.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {})
    return {
        "accession": accession,
        "source_url": url,
        "protein_name": protein.get("value"),
        "queried_positions": sorted(wanted),
        "features_at_positions": features,
    }


def literature_checks(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    source = candidate.get("source_context", {})
    queries = []
    citation_title = source.get("citation_title")
    structure_title = source.get("structure_title")
    pdb_id = candidate.get("pdb_id")
    if citation_title:
        queries.append(f'TITLE:"{citation_title}"')
    if structure_title and structure_title != citation_title:
        queries.append(f'TITLE:"{structure_title}"')
    candidate_desc = source.get("candidate_entity_description")
    kinase_desc = source.get("associated_kinase_entity_description")
    if pdb_id and candidate_desc and kinase_desc:
        queries.append(f'"{pdb_id}" "{candidate_desc}" "{kinase_desc}"')
    compact = []
    for query in queries[:3]:
        compact.append(current.compact_europepmc_query(query, page_size=2))
    return compact


def hit_associated_description(hit: dict[str, Any] | None) -> Any:
    if not hit:
        return None
    return (
        hit.get("terminal_associated_entity_description")
        or hit.get("gamma_associated_entity_description")
        or hit.get("analog_associated_entity_description")
    )


def hit_associated_uniprot_ids(hit: dict[str, Any] | None) -> list[str]:
    if not hit:
        return []
    return (
        hit.get("terminal_associated_entity_uniprot_ids", [])
        or hit.get("gamma_associated_entity_uniprot_ids", [])
        or hit.get("analog_associated_entity_uniprot_ids", [])
        or []
    )


def enriched_source_context(
    candidate: dict[str, Any],
    scan_row: dict[str, Any] | None,
    refreshed_hit: dict[str, Any] | None,
) -> dict[str, Any]:
    source = candidate.get("source_context", {})
    scan_citation = (scan_row or {}).get("citation") or {}
    return {
        "structure_title": source.get("structure_title") or (scan_row or {}).get("title"),
        "citation_title": source.get("citation_title") or scan_citation.get("title"),
        "citation_year": source.get("citation_year") or scan_citation.get("year"),
        "citation_pubmed_id": source.get("citation_pubmed_id")
        or scan_citation.get("pdbx_database_id_pub_med")
        or scan_citation.get("pdbx_database_id_PubMed"),
        "citation_doi": source.get("citation_doi")
        or scan_citation.get("pdbx_database_id_doi")
        or scan_citation.get("pdbx_database_id_DOI"),
        "candidate_entity_description": source.get("candidate_entity_description")
        or (refreshed_hit or {}).get("candidate_entity_description"),
        "candidate_entity_uniprot_ids": source.get("candidate_entity_uniprot_ids", [])
        or (refreshed_hit or {}).get("candidate_entity_uniprot_ids", []),
        "associated_kinase_entity_description": source.get("associated_kinase_entity_description")
        or hit_associated_description(refreshed_hit),
        "associated_kinase_entity_uniprot_ids": source.get("associated_kinase_entity_uniprot_ids", [])
        or hit_associated_uniprot_ids(refreshed_hit),
        "original_candidate_source_mapped": bool(source.get("candidate_source_mapped")),
        "original_candidate_sequence_scheme_matches": source.get("candidate_sequence_scheme_matches", []),
    }


def text_blob(candidate: dict[str, Any]) -> str:
    source = candidate.get("source_context", {})
    pieces = [
        source.get("structure_title"),
        source.get("citation_title"),
        source.get("candidate_entity_description"),
        source.get("associated_kinase_entity_description"),
        candidate.get("pdb_id"),
    ]
    return " ".join(str(piece) for piece in pieces if piece).lower()


def has_phospho_feature(uniprot_checks: list[dict[str, Any]]) -> bool:
    for check in uniprot_checks:
        for feature in check.get("features_at_positions", []) or []:
            description = (feature.get("description") or "").lower()
            feature_type = (feature.get("type") or "").lower()
            if "phospho" in description or "phospho" in feature_type:
                return True
    return False


def has_kinase_domain_only_context(uniprot_checks: list[dict[str, Any]]) -> bool:
    """Detect kinase-domain self/ownership hits that lack a source phosphosite."""
    has_kinase_domain = False
    has_specific_phospho_or_site = False
    for check in uniprot_checks:
        for feature in check.get("features_at_positions", []) or []:
            description = (feature.get("description") or "").lower()
            feature_type = (feature.get("type") or "").lower()
            if "protein kinase" in description and feature_type == "domain":
                has_kinase_domain = True
            if "phospho" in description or feature_type == "modified residue":
                has_specific_phospho_or_site = True
    return has_kinase_domain and not has_specific_phospho_or_site


def has_source_support(candidate: dict[str, Any], uniprot_checks: list[dict[str, Any]]) -> bool:
    blob = text_blob(candidate)
    if has_kinase_domain_only_context(uniprot_checks):
        return False
    if any(term in blob for term in SOURCE_SUPPORT_TERMS):
        return True
    return has_phospho_feature(uniprot_checks)


def is_counterexample_context(candidate: dict[str, Any]) -> bool:
    blob = text_blob(candidate)
    return any(term in blob for term in COUNTEREXAMPLE_TERMS)


def source_adjudication_status(
    candidate: dict[str, Any],
    refreshed_hit: dict[str, Any] | None,
    uniprot_checks: list[dict[str, Any]],
) -> str:
    if is_counterexample_context(candidate):
        return "counterexample_or_non_epk_context_review_only"
    if has_kinase_domain_only_context(uniprot_checks):
        return "source_mapped_but_source_claim_unconfirmed_review_only"
    source_supported = has_source_support(candidate, uniprot_checks)
    source_mapped = bool(
        candidate.get("source_context", {}).get("candidate_source_mapped")
        or (refreshed_hit and refreshed_hit.get("candidate_source_mapped"))
    )
    local_metal = bool(candidate.get("source_free_geometry", {}).get("has_local_mg_or_mn"))
    kind = candidate_kind(candidate)
    state = candidate.get("coordinate_state")
    if state == "transition_analog" and source_supported:
        return "source_supported_transition_or_pseudosubstrate_review_only"
    if source_supported and local_metal and source_mapped and kind == "folded_protein":
        return "source_supported_folded_candidate_review_only"
    if source_supported and local_metal:
        return "source_supported_peptide_or_fragment_candidate_review_only"
    if source_supported and not local_metal:
        return "source_supported_but_no_local_metal_review_only"
    if source_mapped:
        return "source_mapped_but_source_claim_unconfirmed_review_only"
    return "source_mapping_or_claim_unresolved_review_only"


def adjudicate_candidate(
    candidate: dict[str, Any],
    scan_row: dict[str, Any] | None,
    include_literature: bool,
) -> dict[str, Any]:
    pdb_id = str(candidate.get("pdb_id")).upper()
    refreshed_hit = match_candidate_to_refreshed_hit(candidate, scan_row)
    merged_source = enriched_source_context(candidate, scan_row, refreshed_hit)
    entity_id = refreshed_hit.get("candidate_entity_id") if refreshed_hit else None
    entity_context = polymer_entity_context(pdb_id, entity_id) if entity_id else {"entity_id": None}
    position_hints = candidate_position_hints(candidate, refreshed_hit, entity_context)
    accessions = set(merged_source.get("candidate_entity_uniprot_ids", []) or [])
    accessions.update(entity_context.get("uniprot_ids", []) or [])
    uniprot_positions = [
        hint["uniprot_position"]
        for hint in position_hints
        if hint.get("uniprot_position") is not None
    ]
    auth_positions = [hint["position"] for hint in position_hints if hint.get("position") is not None]
    positions_for_uniprot = sorted(set(uniprot_positions or auth_positions))
    uniprot_checks = [
        fetch_uniprot_features(accession, positions_for_uniprot)
        for accession in sorted(accessions)
        if positions_for_uniprot
    ]
    candidate_for_status = {**candidate, "source_context": merged_source}
    status = source_adjudication_status(candidate_for_status, refreshed_hit, uniprot_checks)
    source_mapped_now = bool(
        merged_source.get("original_candidate_source_mapped")
        or (refreshed_hit and refreshed_hit.get("candidate_source_mapped"))
    )
    adjudication = {
        "schema_version": SCHEMA_VERSION,
        "input_schema_version": candidate.get("schema_version"),
        "lane_id": LANE_ID,
        "candidate_id": candidate.get("candidate_id"),
        "pdb_id": pdb_id,
        "coordinate_state": candidate.get("coordinate_state"),
        "source_adjudication_status": status,
        "policy_decision": "review_only_abstain",
        "claim_status": "candidate_review_only_non_countable",
        "countable_label_candidate": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "ready_for_label_import": False,
        "ready_for_production_scoring": False,
        "target_family_id": TARGET_FAMILY_ID,
        "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
        "source_free_geometry": candidate.get("source_free_geometry", {}),
        "original_signal_tags": candidate.get("signal_tags", []),
        "original_blockers": candidate.get("blockers", []),
        "source_context": {
            "structure_title": merged_source.get("structure_title"),
            "citation_title": merged_source.get("citation_title"),
            "citation_year": merged_source.get("citation_year"),
            "citation_pubmed_id": merged_source.get("citation_pubmed_id"),
            "citation_doi": merged_source.get("citation_doi"),
            "candidate_entity_description": merged_source.get("candidate_entity_description"),
            "candidate_entity_uniprot_ids": sorted(accessions),
            "associated_kinase_entity_description": merged_source.get(
                "associated_kinase_entity_description"
            ),
            "associated_kinase_entity_uniprot_ids": merged_source.get(
                "associated_kinase_entity_uniprot_ids",
                [],
            ),
            "original_candidate_source_mapped": bool(merged_source.get("original_candidate_source_mapped")),
            "refreshed_candidate_source_mapped": bool(refreshed_hit and refreshed_hit.get("candidate_source_mapped")),
            "source_mapped_after_refresh": source_mapped_now,
            "candidate_sequence_scheme_matches": (refreshed_hit or {}).get(
                "candidate_sequence_scheme_matches",
                merged_source.get("original_candidate_sequence_scheme_matches", []),
            ),
            "candidate_entity_context": entity_context,
            "candidate_position_hints": position_hints,
            "uniprot_feature_checks": uniprot_checks,
            "literature_checks": literature_checks(candidate_for_status) if include_literature else [],
            "source_review_not_predictive_coordinate_feature": True,
        },
    }
    return adjudication


def summarize(adjudicated_rows: list[dict[str, Any]], scans: dict[str, dict[str, Any]]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    state_counts: dict[str, int] = {}
    scan_status_counts: dict[str, int] = {}
    for row in adjudicated_rows:
        status = row["source_adjudication_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        state = row["coordinate_state"]
        state_counts[state] = state_counts.get(state, 0) + 1
    for scan in scans.values():
        status = scan.get("candidate_status", "unknown")
        scan_status_counts[status] = scan_status_counts.get(status, 0) + 1
    source_supported = [
        row["candidate_id"]
        for row in adjudicated_rows
        if row["source_adjudication_status"].startswith("source_supported")
    ]
    counterexamples = [
        row["candidate_id"]
        for row in adjudicated_rows
        if row["source_adjudication_status"] == "counterexample_or_non_epk_context_review_only"
    ]
    folded_supported = [
        row["candidate_id"]
        for row in adjudicated_rows
        if row["source_adjudication_status"] == "source_supported_folded_candidate_review_only"
    ]
    evidence_for = []
    if source_supported:
        evidence_for.append(
            f"Source-adjudicated {len(source_supported)} review-only candidate rows with source support; none are production labels."
        )
    if folded_supported:
        evidence_for.append(
            "Folded candidate source support was observed for: " + ", ".join(folded_supported[:10]) + "."
        )
    evidence_against = [
        "All adjudicated rows retain policy_decision=review_only_abstain and countable_label_candidate=false.",
        "Source context was recorded separately from source-free geometry and must not become a predictive coordinate feature.",
    ]
    if counterexamples:
        evidence_against.append(
            f"Counterexample/non-ePK ownership contexts remain present in {len(counterexamples)} candidate rows."
        )
    return {
        "status_counts": status_counts,
        "coordinate_state_counts": state_counts,
        "scan_candidate_status_counts": scan_status_counts,
        "source_supported_candidate_ids": source_supported,
        "counterexample_candidate_ids": counterexamples,
        "folded_source_supported_candidate_ids": folded_supported,
        "primary_outcome": "evidence_for" if source_supported else "evidence_against",
        "evidence_for": evidence_for
        or ["Bounded source adjudication completed without upgrading any candidate beyond review-only support."],
        "evidence_against": evidence_against,
        "counterexamples_found": counterexamples,
    }


def build_artifact(
    candidate_artifact: Path,
    out: Path,
    max_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
    include_literature: bool,
    include_all: bool,
) -> dict[str, Any]:
    generated_at = now_iso()
    payload = load_json(candidate_artifact)
    candidate_rows = payload.get("candidate_evidence_rows", [])
    selected, selection = select_candidate_rows(
        candidate_rows,
        max_pdb_ids=max_pdb_ids,
        include_all=include_all,
    )
    scans, scan_failures = scan_selected_pdb_ids(
        selected,
        max_cif_bytes=max_cif_bytes,
        row_timeout_seconds=row_timeout_seconds,
        sleep_seconds=sleep_seconds,
    )
    adjudicated_rows = []
    for row in selected:
        adjudicated_rows.append(
            adjudicate_candidate(
                row,
                scans.get(str(row.get("pdb_id", "")).upper()),
                include_literature=include_literature,
            )
        )
        if sleep_seconds:
            time.sleep(sleep_seconds)
    summary = summarize(adjudicated_rows, scans)
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "candidate_source_adjudication",
            "schema_version": SCHEMA_VERSION,
            "input_schema_version": INPUT_SCHEMA_VERSION,
            "generated_at": generated_at,
            "candidate_artifact": str(candidate_artifact),
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "candidate_rows_available": len(candidate_rows),
            "candidate_rows_reviewed": len(selected),
            "unique_pdb_ids_reviewed": len(selection["selected_unique_pdb_ids"]),
            "max_cif_bytes": max_cif_bytes,
            "row_timeout_seconds": row_timeout_seconds,
            "scan_failure_count": len(scan_failures),
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "review_only_rule": (
                "Source adjudication may support review-only evidence, but it is separated "
                "from source-free geometry and does not create predictive features or labels."
            ),
            "source_urls": [
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_POLYMER_ENTITY_URL,
                current.scout.RCSB_CIF_URL,
                current.EUROPE_PMC_URL,
                UNIPROT_URL,
            ],
        },
        "selection": selection,
        "scan_failures": scan_failures,
        "scan_status_by_pdb": {
            pdb_id: {
                "candidate_status": scan.get("candidate_status"),
                "cif_content_length_bytes": scan.get("cif_content_length_bytes"),
                "candidate_hit_count": len(scan.get("heteromeric_candidate_hits", []) or [])
                + len(scan.get("transition_analog_candidate_hits", []) or []),
                "fetch_error": scan.get("fetch_error"),
            }
            for pdb_id, scan in scans.items()
        },
        "adjudicated_candidate_rows": adjudicated_rows,
        "source_review_summary": {
            "primary_outcome": summary["primary_outcome"],
            "production_claim_allowed": False,
            "search_surface_exhausted": False,
            "status_counts": summary["status_counts"],
            "coordinate_state_counts": summary["coordinate_state_counts"],
            "scan_candidate_status_counts": summary["scan_candidate_status_counts"],
            "source_supported_candidate_ids": summary["source_supported_candidate_ids"],
            "folded_source_supported_candidate_ids": summary["folded_source_supported_candidate_ids"],
            "evidence_for": summary["evidence_for"],
            "evidence_against": summary["evidence_against"],
            "counterexamples_found": summary["counterexamples_found"],
            "recommendation": (
                "Use these adjudications only for review triage. Do not import labels, "
                "tune thresholds, edit registries/fingerprints, run production scoring, "
                "or claim ePK readiness."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-artifact", type=Path, default=DEFAULT_CANDIDATE_ARTIFACT)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-pdb-ids", type=int, default=30)
    parser.add_argument("--max-cif-bytes", type=int, default=18_000_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=35)
    parser.add_argument("--sleep-seconds", type=float, default=0.03)
    parser.add_argument("--skip-literature", action="store_true")
    parser.add_argument("--include-all", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        candidate_artifact=args.candidate_artifact,
        out=args.out,
        max_pdb_ids=args.max_pdb_ids,
        max_cif_bytes=args.max_cif_bytes,
        row_timeout_seconds=args.row_timeout_seconds,
        sleep_seconds=args.sleep_seconds,
        include_literature=not args.skip_literature,
        include_all=args.include_all,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "candidate_rows_reviewed": artifact["metadata"]["candidate_rows_reviewed"],
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "status_counts": artifact["source_review_summary"]["status_counts"],
                "source_supported_count": len(
                    artifact["source_review_summary"]["source_supported_candidate_ids"]
                ),
                "counterexample_count": len(
                    artifact["source_review_summary"]["counterexamples_found"]
                ),
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
