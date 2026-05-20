#!/usr/bin/env python3
"""Bounded RCSB ePK positive-evidence scout.

This helper intentionally writes compact summaries only. Coordinate files are
fetched transiently and are not persisted.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
RCSB_POLYMER_ENTITY_URL = (
    "https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}"
)
RCSB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"

DONOR_GAMMA_ATOMS = {
    "ATP": {"PG"},
    "ANP": {"PG"},
    "ACP": {"PG"},
    "AGS": {"PG"},
}
ACCEPTOR_ATOMS = {
    "SER": {"OG"},
    "THR": {"OG1"},
    "TYR": {"OH"},
}
METAL_CODES = {"MG", "MN"}


@dataclass(frozen=True)
class SearchSurface:
    surface_id: str
    query: str
    rows: int
    start: int = 0


DEFAULT_SURFACES = [
    SearchSurface(
        "rcsb_fulltext_protein_kinase_substrate_protein_phosphoacceptor_amp_pnp_all",
        "protein kinase substrate protein phosphoacceptor AMP-PNP",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_protein_kinase_substrate_protein_phosphoacceptor_anp_all",
        "protein kinase substrate protein phosphoacceptor ANP",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_protein_kinase_substrate_protein_phosphoacceptor_atp_first30",
        "protein kinase substrate protein phosphoacceptor ATP",
        30,
    ),
    SearchSurface(
        "rcsb_fulltext_ser_thr_kinase_substrate_protein_anp_mg_first40",
        "serine threonine protein kinase substrate protein ANP magnesium",
        40,
    ),
    SearchSurface(
        "rcsb_fulltext_ser_thr_kinase_substrate_protein_anp_mg_rows41_80",
        "serine threonine protein kinase substrate protein ANP magnesium",
        40,
        start=40,
    ),
    SearchSurface(
        "rcsb_fulltext_ser_thr_kinase_substrate_protein_anp_mg_rows81_120",
        "serine threonine protein kinase substrate protein ANP magnesium",
        40,
        start=80,
    ),
    SearchSurface(
        "rcsb_fulltext_ser_thr_kinase_substrate_protein_anp_mg_rows121_133",
        "serine threonine protein kinase substrate protein ANP magnesium",
        40,
        start=120,
    ),
    SearchSurface(
        "rcsb_fulltext_kinase_substrate_residue_amp_pnp_mg_protein_all",
        "kinase substrate residue AMP-PNP magnesium protein",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_protein_kinase_full_length_substrate_anp_mg_all",
        "protein kinase full-length substrate ANP magnesium",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_protein_kinase_full_length_substrate_atp_mg_all",
        "protein kinase full-length substrate ATP magnesium",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_protein_kinase_full_length_substrate_amp_pnp_mg_all",
        "protein kinase full-length substrate AMP-PNP magnesium",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_full_length_protein_substrate_kinase_anp_all",
        "full-length protein substrate kinase ANP",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_tyrosine_kinase_substrate_protein_phosphoacceptor_atp_all",
        "tyrosine protein kinase substrate protein phosphoacceptor ATP",
        100,
    ),
    SearchSurface(
        "rcsb_fulltext_tyrosine_kinase_substrate_residue_amp_pnp_mg_protein_all",
        "tyrosine kinase substrate residue AMP-PNP magnesium protein",
        100,
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


def fetch_text(url: str, *, timeout: int = 60) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def search_rcsb(surface: SearchSurface) -> dict[str, Any]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": surface.query},
        },
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
        "query_or_source": f"RCSB full_text: {surface.query}",
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def cif_tokens(text: str) -> Iterable[str]:
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        if c == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c in ("'", '"'):
            quote = c
            i += 1
            start = i
            while i < n and text[i] != quote:
                i += 1
            yield text[start:i]
            i += 1
            continue
        start = i
        while i < n and not text[i].isspace():
            i += 1
        yield text[start:i]


def extract_loop(text: str, category: str) -> list[dict[str, str]]:
    tokens = list(cif_tokens(text))
    rows: list[dict[str, str]] = []
    i = 0
    category_prefix = f"_{category}."
    while i < len(tokens):
        if tokens[i] != "loop_":
            i += 1
            continue
        i += 1
        tags: list[str] = []
        while i < len(tokens) and tokens[i].startswith("_"):
            tags.append(tokens[i])
            i += 1
        values: list[str] = []
        while i < len(tokens):
            token = tokens[i]
            if token == "loop_" or token.startswith("data_") or token.startswith("save_"):
                break
            if token.startswith("_") and tags and len(values) % len(tags) == 0:
                break
            values.append(token)
            i += 1
        if tags and tags[0].startswith(category_prefix):
            width = len(tags)
            cleaned_tags = [tag.split(".", 1)[1] for tag in tags]
            for start in range(0, len(values) - (len(values) % width), width):
                rows.append(dict(zip(cleaned_tags, values[start : start + width])))
    return rows


def as_float(value: str | None) -> float | None:
    if value in (None, ".", "?"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def norm(value: str | None) -> str | None:
    if value in (None, ".", "?"):
        return None
    return value


def dist(a: dict[str, Any], b: dict[str, Any]) -> float:
    return math.sqrt(
        (a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2 + (a["z"] - b["z"]) ** 2
    )


def atom_from_row(row: dict[str, str]) -> dict[str, Any] | None:
    x = as_float(row.get("Cartn_x"))
    y = as_float(row.get("Cartn_y"))
    z = as_float(row.get("Cartn_z"))
    if x is None or y is None or z is None:
        return None
    model = norm(row.get("pdbx_PDB_model_num"))
    if model not in (None, "1"):
        return None
    alt_id = norm(row.get("label_alt_id"))
    if alt_id not in (None, "A"):
        return None
    return {
        "group": row.get("group_PDB"),
        "atom": (norm(row.get("auth_atom_id")) or norm(row.get("label_atom_id")) or "").upper(),
        "label_atom": (norm(row.get("label_atom_id")) or "").upper(),
        "comp": (norm(row.get("auth_comp_id")) or norm(row.get("label_comp_id")) or "").upper(),
        "label_comp": (norm(row.get("label_comp_id")) or "").upper(),
        "chain": norm(row.get("auth_asym_id")) or norm(row.get("label_asym_id")),
        "label_asym_id": norm(row.get("label_asym_id")),
        "entity_id": norm(row.get("label_entity_id")),
        "auth_seq_id": norm(row.get("auth_seq_id")),
        "label_seq_id": norm(row.get("label_seq_id")),
        "x": x,
        "y": y,
        "z": z,
    }


def ligand_key(atom: dict[str, Any]) -> tuple[str | None, str, str | None]:
    return (atom.get("label_asym_id"), atom["comp"], atom.get("auth_seq_id"))


def nearest_polymer_entity(
    ligand_atoms: list[dict[str, Any]], polymer_atoms: list[dict[str, Any]]
) -> dict[str, Any] | None:
    if not ligand_atoms or not polymer_atoms:
        return None
    ligand_chain = ligand_atoms[0].get("chain")
    same_author_chain_atoms = [
        atom for atom in polymer_atoms if ligand_chain is not None and atom.get("chain") == ligand_chain
    ]
    if same_author_chain_atoms:
        best_same_chain = min(
            (
                (dist(ligand_atom, polymer_atom), polymer_atom)
                for ligand_atom in ligand_atoms
                for polymer_atom in same_author_chain_atoms
            ),
            key=lambda item: item[0],
        )
        return {
            "distance_angstrom": round(best_same_chain[0], 3),
            "chain": best_same_chain[1].get("chain"),
            "entity_id": best_same_chain[1].get("entity_id"),
            "association_basis": "ligand_author_chain_matches_polymer_author_chain",
        }
    best: tuple[float, dict[str, Any]] | None = None
    informative_atoms = [
        atom for atom in ligand_atoms if atom["atom"] not in {"PG", "O1G", "O2G", "O3G"}
    ] or ligand_atoms
    for ligand_atom in informative_atoms:
        for polymer_atom in polymer_atoms:
            d = dist(ligand_atom, polymer_atom)
            if best is None or d < best[0]:
                best = (d, polymer_atom)
    if best is None:
        return None
    return {
        "distance_angstrom": round(best[0], 3),
        "chain": best[1].get("chain"),
        "entity_id": best[1].get("entity_id"),
        "association_basis": "nearest_ligand_atom_to_polymer_atom",
    }


def local_metals(gamma_atom: dict[str, Any], metal_atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metals = []
    for metal in metal_atoms:
        d = dist(gamma_atom, metal)
        if d <= 5.0:
            metals.append(
                {
                    "metal_code": metal["comp"],
                    "chain": metal.get("chain"),
                    "auth_seq_id": metal.get("auth_seq_id"),
                    "distance_angstrom": round(d, 3),
                }
            )
    metals.sort(key=lambda item: item["distance_angstrom"])
    return metals[:6]


def scan_cif_for_candidates(cif_text: str) -> dict[str, Any]:
    atoms = [atom for row in extract_loop(cif_text, "atom_site") if (atom := atom_from_row(row))]
    polymer_atoms = [atom for atom in atoms if atom["group"] == "ATOM"]
    ligand_atoms = [atom for atom in atoms if atom["group"] == "HETATM"]
    metals = [atom for atom in ligand_atoms if atom["comp"] in METAL_CODES]
    ligand_atoms_by_key: dict[tuple[str | None, str, str | None], list[dict[str, Any]]] = {}
    for atom in ligand_atoms:
        ligand_atoms_by_key.setdefault(ligand_key(atom), []).append(atom)

    gamma_atoms = [
        atom
        for atom in ligand_atoms
        if atom["comp"] in DONOR_GAMMA_ATOMS
        and atom["atom"] in DONOR_GAMMA_ATOMS[atom["comp"]]
    ]
    acceptor_atoms = [
        atom
        for atom in polymer_atoms
        if atom["comp"] in ACCEPTOR_ATOMS and atom["atom"] in ACCEPTOR_ATOMS[atom["comp"]]
    ]

    hits: list[dict[str, Any]] = []
    gamma_records: list[dict[str, Any]] = []
    for gamma in gamma_atoms:
        associated = nearest_polymer_entity(ligand_atoms_by_key.get(ligand_key(gamma), []), polymer_atoms)
        metals_near_gamma = local_metals(gamma, metals)
        gamma_entity = associated.get("entity_id") if associated else None
        gamma_chain = associated.get("chain") if associated else None
        heteromeric_acceptors = [
            acceptor
            for acceptor in acceptor_atoms
            if not (gamma_entity is not None and acceptor.get("entity_id") == gamma_entity)
            and not (gamma_chain is not None and acceptor.get("chain") == gamma_chain)
        ]
        nearest_heteromeric_acceptor = None
        if heteromeric_acceptors:
            nearest_distance, nearest_acceptor = min(
                ((dist(gamma, acceptor), acceptor) for acceptor in heteromeric_acceptors),
                key=lambda item: item[0],
            )
            nearest_heteromeric_acceptor = {
                "candidate_residue_code": nearest_acceptor["comp"],
                "candidate_atom_name": nearest_acceptor["atom"],
                "candidate_chain_name": nearest_acceptor.get("chain"),
                "candidate_entity_id": nearest_acceptor.get("entity_id"),
                "candidate_auth_seq_id": nearest_acceptor.get("auth_seq_id"),
                "candidate_label_seq_id": nearest_acceptor.get("label_seq_id"),
                "nearest_gamma_distance_angstrom": round(nearest_distance, 3),
            }
        gamma_records.append(
            {
                "gamma_ligand_code": gamma["comp"],
                "gamma_atom_name": gamma["atom"],
                "gamma_chain_name": gamma.get("chain"),
                "gamma_auth_seq_id": gamma.get("auth_seq_id"),
                "associated_polymer_chain_name": associated.get("chain") if associated else None,
                "associated_polymer_entity_id": associated.get("entity_id") if associated else None,
                "associated_polymer_distance_angstrom": associated.get("distance_angstrom") if associated else None,
                "associated_polymer_basis": associated.get("association_basis") if associated else None,
                "local_metals": metals_near_gamma,
                "nearest_heteromeric_acceptor": nearest_heteromeric_acceptor,
            }
        )
        for acceptor in heteromeric_acceptors:
            d = dist(gamma, acceptor)
            if d <= 6.0:
                hits.append(
                    {
                        "candidate_residue_code": acceptor["comp"],
                        "candidate_atom_name": acceptor["atom"],
                        "candidate_chain_name": acceptor.get("chain"),
                        "candidate_entity_id": acceptor.get("entity_id"),
                        "candidate_auth_seq_id": acceptor.get("auth_seq_id"),
                        "candidate_label_seq_id": acceptor.get("label_seq_id"),
                        "gamma_ligand_code": gamma["comp"],
                        "gamma_atom_name": gamma["atom"],
                        "gamma_chain_name": gamma.get("chain"),
                        "gamma_auth_seq_id": gamma.get("auth_seq_id"),
                        "gamma_associated_polymer_chain_name": gamma_chain,
                        "gamma_associated_polymer_entity_id": gamma_entity,
                        "nearest_gamma_distance_angstrom": round(d, 3),
                        "local_metals": metals_near_gamma,
                    }
                )
    hits.sort(key=lambda item: item["nearest_gamma_distance_angstrom"])
    return {
        "atom_count_model_1": len(atoms),
        "donor_gamma_atom_count": len(gamma_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "gamma_records": gamma_records,
        "heteromeric_candidate_hits": hits,
    }


def compact_entry_metadata(pdb_id: str) -> dict[str, Any]:
    entry = fetch_json(RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    container = entry.get("rcsb_entry_container_identifiers", {})
    entity_ids = container.get("polymer_entity_ids", []) or []
    citation = {}
    citations = entry.get("citation") or []
    if citations:
        primary = citations[0]
        citation = {
            "title": primary.get("title"),
            "year": primary.get("year"),
            "pdbx_database_id_pub_med": primary.get("pdbx_database_id_pub_med"),
            "pdbx_database_id_doi": primary.get("pdbx_database_id_doi"),
        }
    polymer_entities: dict[str, Any] = {}
    for entity_id in entity_ids:
        try:
            entity = fetch_json(RCSB_POLYMER_ENTITY_URL.format(pdb_id=pdb_id, entity_id=entity_id))
        except (urllib.error.URLError, TimeoutError):
            continue
        identifiers = entity.get("rcsb_polymer_entity_container_identifiers", {})
        polymer_entities[str(entity_id)] = {
            "description": (
                entity.get("rcsb_polymer_entity", {}).get("pdbx_description")
                or entity.get("entity_poly", {}).get("pdbx_description")
            ),
            "auth_asym_ids": identifiers.get("auth_asym_ids", []),
            "uniprot_ids": identifiers.get("uniprot_ids", []),
            "polymer_type": entity.get("entity_poly", {}).get("rcsb_entity_polymer_type"),
        }
    return {
        "pdb_id": pdb_id,
        "title": entry.get("struct", {}).get("title"),
        "experimental_method": [method.get("method") for method in entry.get("exptl", [])],
        "citation": citation,
        "polymer_entities": polymer_entities,
    }


def merge_hit_entity_context(row: dict[str, Any]) -> None:
    entities = row.get("polymer_entities", {})
    for hit in row.get("heteromeric_candidate_hits", []):
        candidate_entity = entities.get(str(hit.get("candidate_entity_id")), {})
        gamma_entity = entities.get(str(hit.get("gamma_associated_polymer_entity_id")), {})
        hit["candidate_entity_description"] = candidate_entity.get("description")
        hit["candidate_entity_uniprot_ids"] = candidate_entity.get("uniprot_ids", [])
        hit["gamma_associated_entity_description"] = gamma_entity.get("description")
        hit["gamma_associated_entity_uniprot_ids"] = gamma_entity.get("uniprot_ids", [])


def build_artifact(surfaces: list[SearchSurface], out: Path, sleep_seconds: float) -> dict[str, Any]:
    generated_at = now_iso()
    search_results = []
    seen: dict[str, list[dict[str, Any]]] = {}
    for surface in surfaces:
        result = search_rcsb(surface)
        search_results.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1):
            seen.setdefault(pdb_id, []).append(
                {"surface_id": surface.surface_id, "rank": rank, "query_or_source": result["query_or_source"]}
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for pdb_id in sorted(seen):
        try:
            metadata = compact_entry_metadata(pdb_id)
            cif_text = fetch_text(RCSB_CIF_URL.format(pdb_id=pdb_id))
            scan = scan_cif_for_candidates(cif_text)
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
            if row["heteromeric_candidate_hits"]:
                row["candidate_status"] = "heteromeric_candidate_source_validation_pending_review_only"
            elif row["donor_gamma_atom_count"]:
                row["candidate_status"] = "no_heteromeric_candidate_hit_review_only"
            else:
                row["candidate_status"] = "no_active_gamma_donor_atom_review_only"
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - research artifact keeps failures compact.
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

    candidate_rows = [row for row in rows if row.get("heteromeric_candidate_hits")]
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["candidate_status"]] = status_counts.get(row["candidate_status"], 0) + 1
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "epk_positive_evidence_bounded_rcsb_scout",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "search_surface_count": len(surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_results),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_results),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "heteromeric_candidate_pdb_ids": [row["pdb_id"] for row in candidate_rows],
            "heteromeric_candidate_structure_count": len(candidate_rows),
            "ready_to_measure_gamma_acceptor_distance": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "This lane-local scout uses RCSB full-text surfaces plus transient mmCIF "
                "geometry to identify source-validation leads only. It does not create "
                "labels, scores, thresholds, fingerprints, or production claims."
            ),
            "source_urls": [
                RCSB_SEARCH_URL,
                "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}",
                "https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}",
                RCSB_CIF_URL,
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
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(DEFAULT_SURFACES, args.out, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "heteromeric_candidate_pdb_ids": artifact["metadata"][
                    "heteromeric_candidate_pdb_ids"
                ],
                "fetch_failure_count": artifact["metadata"]["fetch_failure_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
