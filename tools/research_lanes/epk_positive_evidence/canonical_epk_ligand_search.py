#!/usr/bin/env python3
"""Domain/EC-filtered canonical ePK ligand scout.

This helper writes compact review-only summaries. It fetches mmCIF files
transiently, scans only bounded PDB IDs, and never writes coordinate dumps.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import epk_evidence_search as scout


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
COMP_ID_ATTR = "rcsb_chem_comp_container_identifiers.comp_id"
EC_LINEAGE_ATTR = "rcsb_polymer_entity.rcsb_ec_lineage.id"
PFAM_ATTR = "rcsb_polymer_entity_annotation.annotation_id"

EXCLUDED_CONTEXT_TERMS = {
    "abc",
    "aaa",
    "hsp70",
    "dnaj",
    "dnak",
    "bip",
    "lon",
    "bcs1",
    "clpx",
    "clpp",
    "clpxp",
    "cydc",
    "cyd",
    "msp1",
    "pcat",
    "transporter",
    "transport",
    "chaperone",
    "proteasome",
}


@dataclass(frozen=True)
class CanonicalSurface:
    surface_id: str
    filter_kind: str
    filter_value: str
    ligand: str
    metal: str
    rows: int = 25
    start: int = 0


DEFAULT_SURFACES = [
    CanonicalSurface("ec_2_7_11_atp_mg", "ec_lineage", "2.7.11", "ATP", "MG"),
    CanonicalSurface("ec_2_7_11_anp_mg", "ec_lineage", "2.7.11", "ANP", "MG"),
    CanonicalSurface("ec_2_7_11_acp_mg", "ec_lineage", "2.7.11", "ACP", "MG"),
    CanonicalSurface("ec_2_7_11_ags_mg", "ec_lineage", "2.7.11", "AGS", "MG"),
    CanonicalSurface("ec_2_7_10_atp_mg", "ec_lineage", "2.7.10", "ATP", "MG"),
    CanonicalSurface("ec_2_7_10_anp_mg", "ec_lineage", "2.7.10", "ANP", "MG"),
    CanonicalSurface("ec_2_7_10_acp_mg", "ec_lineage", "2.7.10", "ACP", "MG"),
    CanonicalSurface("ec_2_7_10_ags_mg", "ec_lineage", "2.7.10", "AGS", "MG"),
    CanonicalSurface("pfam_pkinase_atp_mg", "pfam", "PF00069", "ATP", "MG"),
    CanonicalSurface("pfam_pkinase_anp_mg", "pfam", "PF00069", "ANP", "MG"),
    CanonicalSurface("pfam_pkinase_acp_mg", "pfam", "PF00069", "ACP", "MG"),
    CanonicalSurface("pfam_pkinase_ags_mg", "pfam", "PF00069", "AGS", "MG"),
    CanonicalSurface("pfam_pkinase_tyr_atp_mg", "pfam", "PF07714", "ATP", "MG"),
    CanonicalSurface("pfam_pkinase_tyr_anp_mg", "pfam", "PF07714", "ANP", "MG"),
    CanonicalSurface("pfam_pkinase_tyr_acp_mg", "pfam", "PF07714", "ACP", "MG"),
    CanonicalSurface("pfam_pkinase_tyr_ags_mg", "pfam", "PF07714", "AGS", "MG"),
    CanonicalSurface("ec_2_7_11_atp_mn", "ec_lineage", "2.7.11", "ATP", "MN"),
    CanonicalSurface("ec_2_7_11_anp_mn", "ec_lineage", "2.7.11", "ANP", "MN"),
    CanonicalSurface("ec_2_7_10_atp_mn", "ec_lineage", "2.7.10", "ATP", "MN"),
    CanonicalSurface("ec_2_7_10_anp_mn", "ec_lineage", "2.7.10", "ANP", "MN"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def term(attribute: str, value: str) -> dict[str, Any]:
    return {
        "type": "terminal",
        "service": "text",
        "parameters": {"attribute": attribute, "operator": "exact_match", "value": value},
    }


def surface_query(surface: CanonicalSurface) -> dict[str, Any]:
    if surface.filter_kind == "ec_lineage":
        family_node = term(EC_LINEAGE_ATTR, surface.filter_value)
    elif surface.filter_kind == "pfam":
        family_node = term(PFAM_ATTR, surface.filter_value)
    else:
        raise ValueError(f"unsupported filter kind: {surface.filter_kind}")
    return {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            family_node,
            term(COMP_ID_ATTR, surface.ligand),
            term(COMP_ID_ATTR, surface.metal),
        ],
    }


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


def search_surface(surface: CanonicalSurface) -> dict[str, Any]:
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
    return {
        "surface_id": surface.surface_id,
        "filter_kind": surface.filter_kind,
        "filter_value": surface.filter_value,
        "ligand": surface.ligand,
        "metal": surface.metal,
        "query_or_source": (
            f"RCSB advanced: {surface.filter_kind}={surface.filter_value} "
            f"AND ligand={surface.ligand} AND metal={surface.metal}"
        ),
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def donor_atoms_by_key(ligand_atoms: list[dict[str, Any]]) -> dict[tuple[str | None, str, str | None], set[str]]:
    atoms_by_key: dict[tuple[str | None, str, str | None], set[str]] = {}
    for atom in ligand_atoms:
        atoms_by_key.setdefault(scout.ligand_key(atom), set()).add(atom["atom"])
    return atoms_by_key


def donor_role(atom: dict[str, Any], atoms_in_ligand: set[str]) -> str | None:
    comp = atom["comp"]
    name = atom["atom"]
    if comp in {"ATP", "ACP", "AGS"} and name == "PG":
        return "strict_pg_gamma"
    if comp == "ANP" and name == "PG":
        return "strict_anp_pg_gamma"
    if comp == "ANP" and name == "PB" and "PG" not in atoms_in_ligand:
        return "legacy_anp_pb_terminal_fallback"
    return None


def scan_cif_for_canonical_candidates(cif_text: str) -> dict[str, Any]:
    atoms = [
        atom
        for row in scout.extract_loop(cif_text, "atom_site")
        if (atom := scout.atom_from_row(row))
    ]
    polymer_atoms = [atom for atom in atoms if atom["group"] == "ATOM"]
    ligand_atoms = [atom for atom in atoms if atom["group"] == "HETATM"]
    metals = [atom for atom in ligand_atoms if atom["comp"] in scout.METAL_CODES]
    ligand_atoms_by_key: dict[tuple[str | None, str, str | None], list[dict[str, Any]]] = {}
    for atom in ligand_atoms:
        ligand_atoms_by_key.setdefault(scout.ligand_key(atom), []).append(atom)
    atom_names_by_key = donor_atoms_by_key(ligand_atoms)

    donor_atoms = []
    for atom in ligand_atoms:
        role = donor_role(atom, atom_names_by_key.get(scout.ligand_key(atom), set()))
        if role:
            donor_atoms.append({**atom, "donor_role": role})

    acceptor_atoms = [
        atom
        for atom in polymer_atoms
        if atom["comp"] in scout.ACCEPTOR_ATOMS and atom["atom"] in scout.ACCEPTOR_ATOMS[atom["comp"]]
    ]

    hits: list[dict[str, Any]] = []
    donor_records: list[dict[str, Any]] = []
    for donor in donor_atoms:
        associated = scout.nearest_polymer_entity(
            ligand_atoms_by_key.get(scout.ligand_key(donor), []), polymer_atoms
        )
        metals_near_donor = scout.local_metals(donor, metals)
        donor_entity = associated.get("entity_id") if associated else None
        donor_chain = associated.get("chain") if associated else None
        heteromeric_acceptors = [
            acceptor
            for acceptor in acceptor_atoms
            if not (donor_entity is not None and acceptor.get("entity_id") == donor_entity)
            and not (donor_chain is not None and acceptor.get("chain") == donor_chain)
        ]
        nearest_heteromeric_acceptor = None
        if heteromeric_acceptors:
            nearest_distance, nearest_acceptor = min(
                ((scout.dist(donor, acceptor), acceptor) for acceptor in heteromeric_acceptors),
                key=lambda item: item[0],
            )
            nearest_heteromeric_acceptor = {
                "candidate_residue_code": nearest_acceptor["comp"],
                "candidate_atom_name": nearest_acceptor["atom"],
                "candidate_chain_name": nearest_acceptor.get("chain"),
                "candidate_entity_id": nearest_acceptor.get("entity_id"),
                "candidate_auth_seq_id": nearest_acceptor.get("auth_seq_id"),
                "candidate_label_seq_id": nearest_acceptor.get("label_seq_id"),
                "nearest_terminal_distance_angstrom": round(nearest_distance, 3),
            }
        donor_records.append(
            {
                "terminal_ligand_code": donor["comp"],
                "terminal_atom_name": donor["atom"],
                "donor_role": donor["donor_role"],
                "terminal_chain_name": donor.get("chain"),
                "terminal_auth_seq_id": donor.get("auth_seq_id"),
                "associated_polymer_chain_name": associated.get("chain") if associated else None,
                "associated_polymer_entity_id": associated.get("entity_id") if associated else None,
                "associated_polymer_distance_angstrom": associated.get("distance_angstrom") if associated else None,
                "associated_polymer_basis": associated.get("association_basis") if associated else None,
                "local_metals": metals_near_donor,
                "nearest_heteromeric_acceptor": nearest_heteromeric_acceptor,
            }
        )
        for acceptor in heteromeric_acceptors:
            distance = scout.dist(donor, acceptor)
            if distance <= 6.0:
                hits.append(
                    {
                        "candidate_residue_code": acceptor["comp"],
                        "candidate_atom_name": acceptor["atom"],
                        "candidate_chain_name": acceptor.get("chain"),
                        "candidate_entity_id": acceptor.get("entity_id"),
                        "candidate_auth_seq_id": acceptor.get("auth_seq_id"),
                        "candidate_label_seq_id": acceptor.get("label_seq_id"),
                        "terminal_ligand_code": donor["comp"],
                        "terminal_atom_name": donor["atom"],
                        "donor_role": donor["donor_role"],
                        "terminal_chain_name": donor.get("chain"),
                        "terminal_auth_seq_id": donor.get("auth_seq_id"),
                        "terminal_associated_polymer_chain_name": donor_chain,
                        "terminal_associated_polymer_entity_id": donor_entity,
                        "nearest_terminal_distance_angstrom": round(distance, 3),
                        "local_metals": metals_near_donor,
                        "has_local_mg_or_mn": bool(metals_near_donor),
                    }
                )
    hits.sort(
        key=lambda item: (
            not item["has_local_mg_or_mn"],
            item["donor_role"] == "legacy_anp_pb_terminal_fallback",
            item["nearest_terminal_distance_angstrom"],
        )
    )
    return {
        "atom_count_model_1": len(atoms),
        "terminal_donor_atom_count": len(donor_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "terminal_donor_records": donor_records,
        "heteromeric_candidate_hits": hits,
    }


def category_items(cif_text: str, category: str) -> dict[str, str]:
    tokens = list(scout.cif_tokens(cif_text))
    prefix = f"_{category}."
    items: dict[str, str] = {}
    for index, token in enumerate(tokens[:-1]):
        if token.startswith(prefix):
            items[token.split(".", 1)[1]] = tokens[index + 1]
    return items


def compact_cif_metadata(pdb_id: str, cif_text: str, metadata_error: Exception) -> dict[str, Any]:
    struct = category_items(cif_text, "struct")
    citation_items = category_items(cif_text, "citation")
    entity_rows = scout.extract_loop(cif_text, "entity")
    entity_poly_rows = scout.extract_loop(cif_text, "entity_poly")
    scheme_rows = scout.extract_loop(cif_text, "pdbx_poly_seq_scheme")
    struct_ref_rows = scout.extract_loop(cif_text, "struct_ref")

    descriptions = {
        row.get("id"): row.get("pdbx_description") or row.get("details")
        for row in entity_rows
        if row.get("id")
    }
    poly_types = {
        row.get("entity_id"): row.get("type")
        for row in entity_poly_rows
        if row.get("entity_id")
    }
    auth_asym_ids: dict[str, set[str]] = {}
    for row in scheme_rows:
        entity_id = row.get("entity_id")
        auth_id = row.get("pdb_strand_id")
        if entity_id and auth_id not in (None, ".", "?"):
            auth_asym_ids.setdefault(entity_id, set()).add(auth_id)
    uniprot_ids: dict[str, set[str]] = {}
    for row in struct_ref_rows:
        entity_id = row.get("entity_id")
        accession = row.get("pdbx_db_accession")
        if (
            entity_id
            and accession not in (None, ".", "?")
            and (row.get("db_name") or "").upper() == "UNP"
        ):
            uniprot_ids.setdefault(entity_id, set()).add(accession)

    polymer_entities: dict[str, Any] = {}
    for entity_id in sorted(set(poly_types) | set(auth_asym_ids) | set(uniprot_ids)):
        polymer_entities[str(entity_id)] = {
            "description": descriptions.get(entity_id),
            "auth_asym_ids": sorted(auth_asym_ids.get(entity_id, set())),
            "uniprot_ids": sorted(uniprot_ids.get(entity_id, set())),
            "polymer_type": poly_types.get(entity_id),
        }

    citation = {
        "title": citation_items.get("title"),
        "year": citation_items.get("year"),
        "pdbx_database_id_pub_med": citation_items.get("pdbx_database_id_PubMed"),
        "pdbx_database_id_doi": citation_items.get("pdbx_database_id_DOI"),
    }
    return {
        "pdb_id": pdb_id,
        "title": struct.get("title"),
        "experimental_method": [],
        "citation": {key: value for key, value in citation.items() if value not in (None, ".", "?")},
        "polymer_entities": polymer_entities,
        "metadata_source": "mmcif_fallback",
        "metadata_fetch_error": repr(metadata_error),
    }


def context_terms(row: dict[str, Any]) -> list[str]:
    haystack = [row.get("title") or ""]
    citation = row.get("citation") or {}
    haystack.append(citation.get("title") or "")
    for entity in (row.get("polymer_entities") or {}).values():
        haystack.append(entity.get("description") or "")
    text = " ".join(haystack).lower()
    return sorted(term for term in EXCLUDED_CONTEXT_TERMS if term in text)


def merge_hit_entity_context(row: dict[str, Any]) -> None:
    entities = row.get("polymer_entities", {})
    for hit in row.get("heteromeric_candidate_hits", []):
        candidate_entity = entities.get(str(hit.get("candidate_entity_id")), {})
        terminal_entity = entities.get(str(hit.get("terminal_associated_polymer_entity_id")), {})
        hit["candidate_entity_description"] = candidate_entity.get("description")
        hit["candidate_entity_uniprot_ids"] = candidate_entity.get("uniprot_ids", [])
        hit["terminal_associated_entity_description"] = terminal_entity.get("description")
        hit["terminal_associated_entity_uniprot_ids"] = terminal_entity.get("uniprot_ids", [])


def build_artifact(
    surfaces: list[CanonicalSurface],
    out: Path,
    max_unique: int,
    sleep_seconds: float,
) -> dict[str, Any]:
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
                {
                    "surface_id": surface.surface_id,
                    "rank": rank,
                    "query_or_source": result["query_or_source"],
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for pdb_id in seen:
        try:
            cif_text = scout.fetch_text(scout.RCSB_CIF_URL.format(pdb_id=pdb_id))
            try:
                metadata = scout.compact_entry_metadata(pdb_id)
            except Exception as metadata_exc:  # noqa: BLE001 - keep evidence search moving.
                metadata = compact_cif_metadata(pdb_id, cif_text, metadata_exc)
            scan = scan_cif_for_canonical_candidates(cif_text)
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
                **scan,
            }
            merge_hit_entity_context(row)
            row["excluded_context_terms"] = context_terms(row)
            local_metal_hits = [
                hit for hit in row["heteromeric_candidate_hits"] if hit.get("has_local_mg_or_mn")
            ]
            if local_metal_hits and not row["excluded_context_terms"]:
                row["candidate_status"] = (
                    "local_metal_heteromeric_candidate_source_validation_pending_review_only"
                )
            elif row["heteromeric_candidate_hits"] and row["excluded_context_terms"]:
                row["candidate_status"] = "excluded_context_heteromeric_candidate_review_only"
            elif row["heteromeric_candidate_hits"]:
                row["candidate_status"] = "no_local_metal_heteromeric_candidate_review_only"
            elif row["terminal_donor_atom_count"]:
                row["candidate_status"] = "no_heteromeric_candidate_hit_review_only"
            else:
                row["candidate_status"] = "no_terminal_donor_atom_review_only"
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
    candidate_rows = [
        row
        for row in rows
        if row.get("candidate_status")
        == "local_metal_heteromeric_candidate_source_validation_pending_review_only"
    ]
    fallback_rows = [
        row
        for row in rows
        if any(
            hit.get("donor_role") == "legacy_anp_pb_terminal_fallback"
            for hit in row.get("heteromeric_candidate_hits", [])
        )
    ]
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "canonical_epk_domain_ec_ligand_metal_bounded_scout",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "max_unique_pdb_ids": max_unique,
            "search_surface_count": len(surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_results),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_results),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_candidate_pdb_ids": [row["pdb_id"] for row in candidate_rows],
            "local_metal_candidate_structure_count": len(candidate_rows),
            "legacy_anp_pb_fallback_candidate_pdb_ids": [row["pdb_id"] for row in fallback_rows],
            "excluded_context_terms": sorted(EXCLUDED_CONTEXT_TERMS),
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "This lane-local scout combines RCSB EC/Pfam canonical ePK filters "
                "with nucleotide and Mg/Mn ligand filters, then transiently scans "
                "mmCIF geometry for heteromeric Ser/Thr/Tyr acceptors. ANP PB is "
                "recorded only as explicit review-only fallback when no ANP PG atom "
                "exists in that ligand group. It does not create labels, scores, "
                "thresholds, fingerprints, or production claims."
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
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-unique", type=int, default=50)
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
                "local_metal_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_candidate_pdb_ids"
                ],
                "fetch_failure_count": artifact["metadata"]["fetch_failure_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
