#!/usr/bin/env python3
"""Seed-family follow-up for ePK transition-analog evidence.

This lane-local helper writes compact review-only summaries. It fetches RCSB
metadata and mmCIF files transiently, records source/residue maps for a bounded
seed set, and scans sibling/full-text surfaces for transition-analog proximity.
No coordinate dumps, labels, scores, thresholds, or production artifacts are
created.
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

import epk_evidence_search as scout


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

TRANSITION_ANALOG_CODES = {"AF3", "ALF", "BEF", "MGF"}
SOURCE_TERM_FLAGS = (
    "transition state",
    "aluminum fluoride",
    "magnesium",
    "manganese",
    "kinase",
    "substrate",
    "peptide",
    "inhibitor",
    "pseudosubstrate",
    "phosphorylation",
    "GSK-3",
    "Axin",
    "beta-catenin",
)


@dataclass(frozen=True)
class Surface:
    surface_id: str
    query: str
    rows: int = 25
    start: int = 0


SEED_RESIDUES = [
    {
        "pdb_id": "1L3R",
        "chain": "I",
        "auth_seq_id": "21",
        "expected_comp": "SER",
        "source_role": "PKI-alpha Ser21 in synthetic inhibitor/substrate-site peptide",
    },
    {
        "pdb_id": "5LIH",
        "chain": "F",
        "auth_seq_id": "11",
        "expected_comp": "SER",
        "source_role": "PKC epsilon pseudosubstrate Ser11 in synthetic peptide chain F",
    },
    {
        "pdb_id": "5LIH",
        "chain": "G",
        "auth_seq_id": "11",
        "expected_comp": "SER",
        "source_role": "PKC epsilon pseudosubstrate Ser11 in synthetic peptide chain G",
    },
    {
        "pdb_id": "4NU1",
        "chain": "A",
        "auth_seq_id": "9",
        "expected_comp": "SEP",
        "source_role": "GSK-3 beta autoinhibitory phosphorylated Ser9 product-state residue",
    },
    {
        "pdb_id": "8VMF",
        "chain": "C",
        "auth_seq_id": "45",
        "expected_comp": "ASP",
        "source_role": "beta-catenin S45D phosphomimetic residue, not a hydroxyl acceptor",
    },
]


DEFAULT_SURFACES = [
    Surface("doi_10_1038_nsb780", "10.1038/nsb780", 20),
    Surface("doi_10_1016_j_devcel_2016_07_018", "10.1016/j.devcel.2016.07.018", 20),
    Surface("doi_10_1126_scisignal_ado0881", "10.1126/scisignal.ado0881", 20),
    Surface(
        "gsk3_inhibition_source_title",
        "Structural basis of GSK-3 inhibition by N-terminal phosphorylation and by the Wnt receptor LRP6",
        25,
    ),
    Surface("gsk3_axin_transition_state_mimic", "GSK-3 Axin transition state mimic AF3", 25),
    Surface(
        "gsk3_beta_catenin_s45d_transition_state",
        "GSK-3 beta-catenin S45D transition-state mimic",
        25,
    ),
    Surface(
        "pka_pki_transition_state_mimic",
        "cAMP-dependent protein kinase PKI transition state mimic ADP AlF3",
        25,
    ),
    Surface(
        "pkciota_pseudosubstrate_transition_state",
        "PKC iota pseudosubstrate transition state analog AF3",
        25,
    ),
    Surface(
        "full_length_substrate_transition_state_af3",
        "protein kinase full-length substrate transition state aluminum fluoride",
        50,
    ),
    Surface(
        "folded_protein_substrate_transition_state_adp",
        "protein kinase folded protein substrate transition state mimic ADP",
        50,
    ),
    Surface(
        "protein_substrate_transition_analog_metal_fluoride",
        "protein kinase protein substrate transition-state analog ADP metal fluoride",
        50,
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


def search_surface(surface: Surface) -> dict[str, Any]:
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


def compact_europepmc_source(citation: dict[str, Any], pdb_id: str) -> dict[str, Any] | None:
    pmid = citation.get("pdbx_database_id_pub_med") or citation.get("pdbx_database_id_PubMed")
    doi = citation.get("pdbx_database_id_doi") or citation.get("pdbx_database_id_DOI")
    if pmid:
        query = f"EXT_ID:{pmid} SRC:MED"
    elif doi:
        query = f'DOI:"{doi}"'
    else:
        return None
    params = urllib.parse.urlencode({"query": query, "format": "json", "pageSize": 1, "resultType": "core"})
    url = f"{EUROPE_PMC_URL}?{params}"
    try:
        data = fetch_json(url, timeout=30)
    except Exception as exc:  # noqa: BLE001 - compact source validation artifact.
        return {"pdb_id": pdb_id, "source_url": url, "fetch_error": repr(exc)}
    results = data.get("resultList", {}).get("result", [])
    if not results:
        return {"pdb_id": pdb_id, "source_url": url, "result_count": 0}
    row = results[0]
    text = " ".join([row.get("title") or "", row.get("abstractText") or ""]).lower()
    return {
        "pdb_id": pdb_id,
        "source_url": url,
        "pmid": row.get("pmid"),
        "doi": row.get("doi"),
        "pub_year": row.get("pubYear"),
        "article_title": row.get("title"),
        "term_flags": {term: term.lower() in text for term in SOURCE_TERM_FLAGS},
    }


def local_metals_for_group(group_atoms: list[dict[str, Any]], metals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for metal in metals:
        best = min((scout.dist(atom, metal), atom) for atom in group_atoms)
        if best[0] <= 5.0:
            records.append(
                {
                    "metal_code": metal["comp"],
                    "chain": metal.get("chain"),
                    "auth_seq_id": metal.get("auth_seq_id"),
                    "nearest_analog_atom": best[1]["atom"],
                    "distance_angstrom": round(best[0], 3),
                }
            )
    records.sort(key=lambda item: item["distance_angstrom"])
    return records[:8]


def nearest_acceptor_record(
    group_atoms: list[dict[str, Any]], acceptors: list[dict[str, Any]]
) -> tuple[float, dict[str, Any], dict[str, Any]] | None:
    if not group_atoms or not acceptors:
        return None
    return min(
        ((scout.dist(analog_atom, acceptor), analog_atom, acceptor) for analog_atom in group_atoms for acceptor in acceptors),
        key=lambda item: item[0],
    )


def scan_transition_analog_candidates(cif_text: str) -> dict[str, Any]:
    atoms = [atom for row in scout.extract_loop(cif_text, "atom_site") if (atom := scout.atom_from_row(row))]
    polymer_atoms = [atom for atom in atoms if atom["group"] == "ATOM"]
    ligand_atoms = [atom for atom in atoms if atom["group"] == "HETATM"]
    metals = [atom for atom in ligand_atoms if atom["comp"] in scout.METAL_CODES]
    acceptor_atoms = [
        atom
        for atom in polymer_atoms
        if atom["comp"] in scout.ACCEPTOR_ATOMS and atom["atom"] in scout.ACCEPTOR_ATOMS[atom["comp"]]
    ]

    groups: dict[tuple[str | None, str, str | None], list[dict[str, Any]]] = {}
    for atom in ligand_atoms:
        if atom["comp"] in TRANSITION_ANALOG_CODES:
            groups.setdefault(scout.ligand_key(atom), []).append(atom)

    records: list[dict[str, Any]] = []
    hits: list[dict[str, Any]] = []
    for key, group_atoms in sorted(groups.items(), key=lambda item: (str(item[0][0]), item[0][1], str(item[0][2]))):
        analog_comp = key[1]
        associated = scout.nearest_polymer_entity(group_atoms, polymer_atoms)
        associated_entity = associated.get("entity_id") if associated else None
        associated_chain = associated.get("chain") if associated else None
        heteromeric_acceptors = [
            acceptor
            for acceptor in acceptor_atoms
            if not (associated_entity is not None and acceptor.get("entity_id") == associated_entity)
            and not (associated_chain is not None and acceptor.get("chain") == associated_chain)
        ]
        nearest = nearest_acceptor_record(group_atoms, heteromeric_acceptors)
        local_metals = local_metals_for_group(group_atoms, metals)
        nearest_record = None
        if nearest:
            distance, analog_atom, acceptor = nearest
            nearest_record = {
                "candidate_residue_code": acceptor["comp"],
                "candidate_atom_name": acceptor["atom"],
                "candidate_chain_name": acceptor.get("chain"),
                "candidate_entity_id": acceptor.get("entity_id"),
                "candidate_auth_seq_id": acceptor.get("auth_seq_id"),
                "candidate_label_seq_id": acceptor.get("label_seq_id"),
                "nearest_analog_atom": analog_atom["atom"],
                "nearest_analog_distance_angstrom": round(distance, 3),
            }
        record = {
            "analog_ligand_code": analog_comp,
            "analog_chain_name": group_atoms[0].get("chain"),
            "analog_auth_seq_id": group_atoms[0].get("auth_seq_id"),
            "analog_atom_names": sorted({atom["atom"] for atom in group_atoms}),
            "associated_polymer_chain_name": associated_chain,
            "associated_polymer_entity_id": associated_entity,
            "associated_polymer_distance_angstrom": associated.get("distance_angstrom") if associated else None,
            "local_metals": local_metals,
            "nearest_heteromeric_acceptor": nearest_record,
        }
        records.append(record)
        for acceptor in heteromeric_acceptors:
            nearest_hit = nearest_acceptor_record(group_atoms, [acceptor])
            if not nearest_hit:
                continue
            distance, analog_atom, _ = nearest_hit
            if distance <= 6.0:
                hits.append(
                    {
                        "analog_ligand_code": analog_comp,
                        "analog_chain_name": group_atoms[0].get("chain"),
                        "analog_auth_seq_id": group_atoms[0].get("auth_seq_id"),
                        "analog_associated_polymer_chain_name": associated_chain,
                        "analog_associated_polymer_entity_id": associated_entity,
                        "candidate_residue_code": acceptor["comp"],
                        "candidate_atom_name": acceptor["atom"],
                        "candidate_chain_name": acceptor.get("chain"),
                        "candidate_entity_id": acceptor.get("entity_id"),
                        "candidate_auth_seq_id": acceptor.get("auth_seq_id"),
                        "candidate_label_seq_id": acceptor.get("label_seq_id"),
                        "nearest_analog_atom": analog_atom["atom"],
                        "nearest_analog_distance_angstrom": round(distance, 3),
                        "local_metals": local_metals,
                        "has_local_mg_or_mn": bool(local_metals),
                    }
                )
    hits.sort(key=lambda item: (not item["has_local_mg_or_mn"], item["nearest_analog_distance_angstrom"]))
    return {
        "atom_count_model_1": len(atoms),
        "transition_analog_group_count": len(groups),
        "transition_analog_records": records,
        "transition_analog_candidate_hits": hits,
    }


def sequence_scheme_maps(cif_text: str, pdb_id: str) -> list[dict[str, Any]]:
    scheme_rows = scout.extract_loop(cif_text, "pdbx_poly_seq_scheme")
    maps = []
    for spec in SEED_RESIDUES:
        if spec["pdb_id"] != pdb_id:
            continue
        matches = []
        for row in scheme_rows:
            chain = row.get("pdb_strand_id")
            auth_seq = row.get("auth_seq_num") or row.get("pdb_seq_num")
            if chain == spec["chain"] and auth_seq == spec["auth_seq_id"]:
                matches.append(
                    {
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
                )
        maps.append({**spec, "scheme_matches": matches, "source_mapped": bool(matches)})
    return maps


def merge_entity_context(row: dict[str, Any]) -> None:
    entities = row.get("polymer_entities", {})
    for hit in row.get("transition_analog_candidate_hits", []):
        candidate_entity = entities.get(str(hit.get("candidate_entity_id")), {})
        analog_entity = entities.get(str(hit.get("analog_associated_polymer_entity_id")), {})
        hit["candidate_entity_description"] = candidate_entity.get("description")
        hit["candidate_entity_uniprot_ids"] = candidate_entity.get("uniprot_ids", [])
        hit["analog_associated_entity_description"] = analog_entity.get("description")
        hit["analog_associated_entity_uniprot_ids"] = analog_entity.get("uniprot_ids", [])
    for record in row.get("transition_analog_records", []):
        analog_entity = entities.get(str(record.get("associated_polymer_entity_id")), {})
        record["associated_entity_description"] = analog_entity.get("description")
        record["associated_entity_uniprot_ids"] = analog_entity.get("uniprot_ids", [])
        nearest = record.get("nearest_heteromeric_acceptor")
        if nearest:
            candidate_entity = entities.get(str(nearest.get("candidate_entity_id")), {})
            nearest["candidate_entity_description"] = candidate_entity.get("description")
            nearest["candidate_entity_uniprot_ids"] = candidate_entity.get("uniprot_ids", [])


def classify_row(row: dict[str, Any]) -> str:
    if not row.get("transition_analog_group_count"):
        return "no_transition_analog_group_review_only"
    if not row.get("transition_analog_candidate_hits"):
        return "no_heteromeric_transition_analog_candidate_review_only"
    local_hits = [hit for hit in row.get("transition_analog_candidate_hits", []) if hit.get("has_local_mg_or_mn")]
    if not local_hits:
        return "no_local_metal_transition_analog_candidate_review_only"
    descriptions = []
    for hit in local_hits:
        descriptions.append((hit.get("candidate_entity_description") or "").lower())
    if any("peptide" in description or "pseudo" in description or "inhibitor" in description for description in descriptions):
        return "local_metal_peptide_or_pseudosubstrate_candidate_review_only"
    return "local_metal_nonpeptide_candidate_source_validation_pending_review_only"


def source_review_summary(rows: list[dict[str, Any]], search_results: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["candidate_status"]] = statuses.get(row["candidate_status"], 0) + 1
    nonpeptide_candidates = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_nonpeptide_candidate_source_validation_pending_review_only"
    ]
    peptide_candidates = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_peptide_or_pseudosubstrate_candidate_review_only"
    ]
    return {
        "primary_outcome": "search_surface_exhausted",
        "production_claim_allowed": False,
        "search_surface_exhausted": True,
        "candidate_status_counts": statuses,
        "nonpeptide_local_metal_candidate_pdb_ids": nonpeptide_candidates,
        "peptide_or_pseudosubstrate_local_metal_candidate_pdb_ids": peptide_candidates,
        "evidence_for": [
            "1L3R and 5LIH remain source-mapped review-only peptide/pseudosubstrate transition-state positives with local metal.",
            "Same-paper and family searches recovered only peptide/pseudosubstrate local-metal positives, not a clean folded-protein substrate positive.",
        ],
        "evidence_against": [
            "No non-peptide folded substrate analog state with unmodified source-mapped Ser/Thr/Tyr acceptor near kinase-associated AF3/MGF/BEF/ALF and local Mg/Mn was found in this bounded sibling/family surface.",
            "4NU1 remains a phosphorylated GSK-3 Ser9 autoinhibitory/product-state near miss; 8VMF remains a beta-catenin S45D phosphomimetic near miss.",
        ],
        "counterexamples_found": [],
        "recommendation": (
            "Keep 1L3R/5LIH as review-only stress positives and keep 4NU1/8VMF as near-miss negatives. "
            "Do not change production labels, thresholds, registries, fingerprints, migrations, or scoring."
        ),
        "next_query": (
            "Search newly deposited 2025-2026 ePK structures by exact ligand families ATP/ANP/ADP plus "
            "MG/MN/AF3/MGF/BEF and source terms 'substrate'/'phosphorylation site', but require non-peptide "
            "substrate entity length and explicit kinase-site ligand ownership before CIF source mapping."
        ),
        "surfaces_reviewed": [surface["surface_id"] for surface in search_results],
    }


def build_artifact(surfaces: list[Surface], out: Path, max_unique: int, sleep_seconds: float) -> dict[str, Any]:
    generated_at = now_iso()
    search_results = []
    seen: dict[str, list[dict[str, Any]]] = {seed["pdb_id"]: [{"surface_id": "fixed_seed", "rank": 0, "query_or_source": "fixed seed from handoff"}] for seed in SEED_RESIDUES}
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
    europepmc_sources = []
    for pdb_id in seen:
        try:
            metadata = scout.compact_entry_metadata(pdb_id)
            cif_text = scout.fetch_text(scout.RCSB_CIF_URL.format(pdb_id=pdb_id))
            scan = scan_transition_analog_candidates(cif_text)
            row = {
                **metadata,
                "search_hits": seen[pdb_id],
                "seed_residue_source_maps": sequence_scheme_maps(cif_text, pdb_id),
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
            merge_entity_context(row)
            row["candidate_status"] = classify_row(row)
            rows.append(row)
            source = compact_europepmc_source(metadata.get("citation") or {}, pdb_id)
            if source:
                europepmc_sources.append(source)
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

    summary = source_review_summary(rows, search_results)
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "transition_analog_seed_family_followup",
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
            "candidate_status_counts": summary["candidate_status_counts"],
            "nonpeptide_local_metal_candidate_pdb_ids": summary["nonpeptide_local_metal_candidate_pdb_ids"],
            "peptide_or_pseudosubstrate_local_metal_candidate_pdb_ids": summary[
                "peptide_or_pseudosubstrate_local_metal_candidate_pdb_ids"
            ],
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Seed-family follow-up for 1L3R/5LIH/4NU1/8VMF. Same-paper, family, and "
                "non-peptide phrase surfaces are bounded; mmCIF coordinates are transient; "
                "output is source-validation evidence only."
            ),
            "source_urls": [
                RCSB_SEARCH_URL,
                scout.RCSB_ENTRY_URL,
                scout.RCSB_POLYMER_ENTITY_URL,
                scout.RCSB_CIF_URL,
                EUROPE_PMC_URL,
            ],
        },
        "search_surfaces": search_results,
        "europepmc_source_rows": europepmc_sources,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": summary,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-unique", type=int, default=100)
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
                "nonpeptide_local_metal_candidate_pdb_ids": artifact["metadata"][
                    "nonpeptide_local_metal_candidate_pdb_ids"
                ],
                "peptide_or_pseudosubstrate_local_metal_candidate_pdb_ids": artifact["metadata"][
                    "peptide_or_pseudosubstrate_local_metal_candidate_pdb_ids"
                ],
                "fetch_failure_count": artifact["metadata"]["fetch_failure_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
