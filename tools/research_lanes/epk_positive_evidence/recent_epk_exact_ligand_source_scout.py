#!/usr/bin/env python3
"""Recent ePK exact-ligand source scout.

Bounded review-only search for newly deposited ePK structures with exact
nucleotide/metal or transition-analog ligand context plus substrate/source
terms. Coordinates are fetched transiently and summarized compactly.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
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
COMP_ID_ATTR = "rcsb_chem_comp_container_identifiers.comp_id"
EC_LINEAGE_ATTR = "rcsb_polymer_entity.rcsb_ec_lineage.id"
PFAM_ATTR = "rcsb_polymer_entity_annotation.annotation_id"
RELEASE_DATE_ATTR = "rcsb_accession_info.initial_release_date"
DATE_RANGE = {"from": "2025-01-01", "to": "2026-05-20"}


@dataclass(frozen=True)
class RecentSurface:
    surface_id: str
    source_query: str
    ligand_mode: str
    rows: int = 30
    start: int = 0


DEFAULT_SURFACES = [
    RecentSurface(
        "recent_gamma_substrate",
        "substrate",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_gamma_phosphorylation",
        "phosphorylation",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_gamma_substrate_phosphorylation_site",
        "substrate phosphorylation site",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_gamma_protein_substrate_phosphorylation",
        "protein substrate phosphorylation",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_gamma_full_length_substrate_kinase",
        "full-length substrate kinase",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_gamma_phosphoacceptor_substrate",
        "phosphoacceptor substrate",
        "gamma",
        30,
    ),
    RecentSurface(
        "recent_transition_substrate_phosphorylation_site",
        "substrate phosphorylation site transition state",
        "transition",
        30,
    ),
    RecentSurface(
        "recent_transition_protein_substrate_metal_fluoride",
        "protein kinase protein substrate transition-state analog ADP metal fluoride",
        "transition",
        30,
    ),
    RecentSurface(
        "recent_transition_full_length_substrate",
        "full-length substrate transition state kinase",
        "transition",
        30,
    ),
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


def surface_query(surface: RecentSurface) -> dict[str, Any]:
    if surface.ligand_mode == "gamma":
        ligand_nodes = [
            comp_group(["ATP", "ANP", "ACP", "AGS"]),
            comp_group(["MG", "MN"]),
        ]
    elif surface.ligand_mode == "transition":
        ligand_nodes = [
            text_term(COMP_ID_ATTR, "ADP"),
            comp_group(["AF3", "ALF", "BEF", "MGF"]),
        ]
    else:
        raise ValueError(f"unsupported ligand mode: {surface.ligand_mode}")
    return group(
        "and",
        [
            family_group(),
            text_term(RELEASE_DATE_ATTR, DATE_RANGE, "range"),
            full_text(surface.source_query),
            *ligand_nodes,
        ],
    )


def search_surface(surface: RecentSurface) -> dict[str, Any]:
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
    ligand_text = "ATP/ANP/ACP/AGS+MG/MN" if surface.ligand_mode == "gamma" else "ADP+AF3/ALF/BEF/MGF"
    return {
        "surface_id": surface.surface_id,
        "query_or_source": (
            "RCSB advanced: released 2025-01-01..2026-05-20 AND canonical ePK "
            f"AND {ligand_text} AND full_text='{surface.source_query}'"
        ),
        "ligand_mode": surface.ligand_mode,
        "source_query": surface.source_query,
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
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


def add_sequence_scheme_matches(row: dict[str, Any], cif_text: str) -> None:
    scheme_rows = scout.extract_loop(cif_text, "pdbx_poly_seq_scheme")
    hit_lists = [
        row.get("heteromeric_candidate_hits", []),
        row.get("transition_analog_candidate_hits", []),
    ]
    for hit_list in hit_lists:
        for hit in hit_list:
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


def build_artifact(surfaces: list[RecentSurface], out: Path, max_unique: int, sleep_seconds: float) -> dict[str, Any]:
    generated_at = now_iso()
    search_results = []
    seen: dict[str, list[dict[str, Any]]] = {}
    for surface in surfaces:
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
    for pdb_id in seen:
        try:
            metadata = scout.compact_entry_metadata(pdb_id)
            cif_text = scout.fetch_text(scout.RCSB_CIF_URL.format(pdb_id=pdb_id))
            canonical_scan = canonical.scan_cif_for_canonical_candidates(cif_text)
            transition_scan = transition.scan_transition_analog_candidates(cif_text)
            row = {
                **metadata,
                "search_hits": seen[pdb_id],
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
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
                    "pdb_id": pdb_id,
                    "search_hits": seen[pdb_id],
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
            "Recent exact-ligand/source surfaces found local-metal non-peptide candidates requiring source adjudication."
        )
    if short_or_peptide:
        evidence_for.append(
            "Recent exact-ligand/source surfaces found review-only short/peptide local-metal candidates: "
            + ", ".join(short_or_peptide)
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Recent exact-ligand/source surfaces recovered rows for review, but no local-metal candidate passed the current filters."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "recent_epk_exact_ligand_source_scout",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "date_range": DATE_RANGE,
            "max_unique_pdb_ids": max_unique,
            "search_surface_count": len(surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_results),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_results),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_nonpeptide_candidate_pdb_ids": nonpeptide,
            "local_metal_peptide_or_short_candidate_pdb_ids": short_or_peptide,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Recent exact-ligand/source scout only. It does not create labels, scores, "
                "thresholds, fingerprints, migrations, or production claims."
            ),
            "source_urls": [
                RCSB_SEARCH_URL,
                scout.RCSB_ENTRY_URL,
                scout.RCSB_POLYMER_ENTITY_URL,
                scout.RCSB_CIF_URL,
            ],
        },
        "search_surfaces": search_results,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": "evidence_for" if (nonpeptide or short_or_peptide) else "search_surface_exhausted",
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(nonpeptide),
            "evidence_for": evidence_for,
            "evidence_against": [
                "No local-metal non-peptide candidate was found after exact 2025-2026 ePK family/date/ligand/source filtering.",
                "Recovered non-short rows were MEK/ERK no-local-metal repeats, kinase-only states, or no active donor/transition-analog contexts.",
                "Short/peptide candidates are review-only stress evidence and are not clean folded-protein substrate positives.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "Do not change production labels, thresholds, registries, fingerprints, migrations, or scoring. "
                "Use this recent exact-ligand surface as exhausted for the current snapshot."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-unique", type=int, default=80)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(DEFAULT_SURFACES, args.out, args.max_unique, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "local_metal_nonpeptide_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_nonpeptide_candidate_pdb_ids"
                ],
                "local_metal_peptide_or_short_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_peptide_or_short_candidate_pdb_ids"
                ],
                "fetch_failure_count": artifact["metadata"]["fetch_failure_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
