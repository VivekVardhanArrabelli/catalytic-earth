#!/usr/bin/env python3
"""Source-map PKA/CFTR structures for ePK positive-evidence review.

This helper keeps all coordinate use transient. It records compact entry,
article, residue, and distance summaries only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE_ID = "epk_positive_evidence"
PDB_IDS = ["9DW4", "9DW5", "9DW7", "9DW8", "9DW9"]
ARTICLE_DOI = "10.1073/pnas.2409049121"
ARTICLE_PMID = "39495916"
ARTICLE_PMCID = "PMC11573500"
EUROPE_PMC_SEARCH_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EUROPE_PMC_FULL_TEXT_URL = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
)

CFTR_PKA_SITE_POSITIONS = [422, 660, 670, 686, 700, 712, 737, 753, 768, 795, 813]
CFTR_PKA_SITE_DOMAINS = {
    422: "NBD1 regulatory insertion",
    660: "R domain",
    670: "R domain",
    686: "R domain",
    700: "R domain",
    712: "R domain",
    737: "R domain",
    753: "R domain",
    768: "R domain",
    795: "R domain",
    813: "R domain",
}


@dataclass(frozen=True)
class RcsbSurface:
    surface_id: str
    query: str
    rows: int = 25


RCSB_SURFACES = [
    RcsbSurface(
        "rcsb_fulltext_pka_cftr_anp_dephosphorylated_phosphorylation",
        "PKA CFTR ANP dephosphorylated phosphorylation",
    ),
    RcsbSurface(
        "rcsb_fulltext_pka_cftr_amp_pnp_phosphorylation_site",
        "PKA CFTR AMP-PNP phosphorylation site",
    ),
    RcsbSurface(
        "rcsb_fulltext_pka_cftr_catalytic_stations",
        "PKA CFTR catalytic stations",
    ),
]


def load_epk_helper() -> Any:
    helper_path = Path(__file__).with_name("epk_evidence_search.py")
    spec = importlib.util.spec_from_file_location("epk_evidence_search", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["epk_evidence_search"] = module
    spec.loader.exec_module(module)
    return module


epk = load_epk_helper()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def search_rcsb(surface: RcsbSurface) -> dict[str, Any]:
    result = epk.search_rcsb(
        epk.SearchSurface(surface.surface_id, surface.query, surface.rows)
    )
    return result


def search_europe_pmc() -> dict[str, Any]:
    query = '"The structures of protein kinase A in complex with CFTR"'
    url = EUROPE_PMC_SEARCH_URL + "?" + urllib.parse.urlencode(
        {"query": query, "format": "json", "pageSize": 10}
    )
    data = epk.fetch_json(url, timeout=30)
    rows = []
    for row in data.get("resultList", {}).get("result", []):
        rows.append(
            {
                "pmid": row.get("pmid"),
                "pmcid": row.get("pmcid"),
                "doi": row.get("doi"),
                "title": row.get("title"),
                "journal": row.get("journalTitle"),
                "pubYear": row.get("pubYear"),
                "isOpenAccess": row.get("isOpenAccess"),
                "hasPDF": row.get("hasPDF"),
                "hasSuppl": row.get("hasSuppl"),
            }
        )
    return {
        "surface_id": "europepmc_pka_cftr_anp_dephosphorylated_phosphorylation",
        "query_or_source": f"Europe PMC: {query}",
        "returned_count": len(rows),
        "rows": rows,
        "source_url": url,
    }


def article_source_summary() -> dict[str, Any]:
    metadata_url = EUROPE_PMC_SEARCH_URL + "?" + urllib.parse.urlencode(
        {"query": f"DOI:{ARTICLE_DOI}", "format": "json", "pageSize": 3}
    )
    metadata = epk.fetch_json(metadata_url, timeout=30)
    full_text_url = EUROPE_PMC_FULL_TEXT_URL.format(pmcid=ARTICLE_PMCID)
    xml_text = epk.fetch_text(full_text_url, timeout=60)
    root = ET.fromstring(xml_text)
    article_text = " ".join(text.strip() for text in root.itertext() if text.strip())
    result_rows = metadata.get("resultList", {}).get("result", [])
    result = result_rows[0] if result_rows else {}
    return {
        "title": result.get("title"),
        "doi": result.get("doi") or ARTICLE_DOI,
        "pmid": result.get("pmid") or ARTICLE_PMID,
        "pmcid": result.get("pmcid") or ARTICLE_PMCID,
        "journal": result.get("journalTitle"),
        "pubYear": result.get("pubYear"),
        "isOpenAccess": result.get("isOpenAccess"),
        "hasPDF": result.get("hasPDF"),
        "hasSuppl": result.get("hasSuppl"),
        "article_metadata_url": metadata_url,
        "article_full_text_xml_url": full_text_url,
        "source_checks": {
            "reports_full_length_cftr_bound_to_pka_c": "full-length CFTR" in article_text
            and "PKA-C" in article_text,
            "reports_amp_pnp_nontransfer_sample": "AMP-PNP" in article_text
            and "not support phosphorylation" in article_text,
            "reports_r_domain_density_largely_missing": "density for the R domain is largely missing"
            in article_text,
            "reports_two_catalytic_stations": "two separate" in article_text
            and "catalytic stations" in article_text,
            "reports_site_i_and_site_ii_models": all(pdb_id in article_text for pdb_id in PDB_IDS),
        },
        "source_mapped_phosphorylation_sites": [
            {
                "residue": f"S{pos}",
                "auth_seq_id": pos,
                "domain": CFTR_PKA_SITE_DOMAINS[pos],
                "mapping_basis": (
                    "PNAS article maps ten R-domain sites in Fig. 1A and identifies S422 "
                    "in the NBD1 regulatory insertion as the eleventh PKA site."
                ),
            }
            for pos in CFTR_PKA_SITE_POSITIONS
        ],
    }


def polymer_entity_sets(metadata: dict[str, Any]) -> tuple[set[str], set[str]]:
    cftr_entities = set()
    pka_entities = set()
    for entity_id, entity in metadata.get("polymer_entities", {}).items():
        description = (entity.get("description") or "").lower()
        if "cystic fibrosis transmembrane conductance regulator" in description:
            cftr_entities.add(str(entity_id))
        if "protein kinase" in description and "catalytic subunit" in description:
            pka_entities.add(str(entity_id))
    return cftr_entities, pka_entities


def ligand_atom_groups(ligand_atoms: list[dict[str, Any]]) -> dict[tuple[str | None, str, str | None], list[dict[str, Any]]]:
    groups: dict[tuple[str | None, str, str | None], list[dict[str, Any]]] = {}
    for atom in ligand_atoms:
        groups.setdefault(epk.ligand_key(atom), []).append(atom)
    return groups


def atom_residue_number(atom: dict[str, Any]) -> int | None:
    value = atom.get("auth_seq_id")
    if value is None or not str(value).lstrip("-").isdigit():
        return None
    return int(value)


def int_or_none(value: str | None) -> int | None:
    if value is None or not str(value).lstrip("-").isdigit():
        return None
    return int(str(value))


def cftr_sequence_scheme(
    cif_text: str,
    cftr_entities: set[str],
) -> dict[tuple[str, int], dict[str, str]]:
    scheme = {}
    for row in epk.extract_loop(cif_text, "pdbx_poly_seq_scheme"):
        if str(row.get("entity_id")) not in cftr_entities:
            continue
        chain = epk.norm(row.get("pdb_strand_id")) or epk.norm(row.get("asym_id"))
        position = int_or_none(row.get("auth_seq_num")) or int_or_none(row.get("pdb_seq_num"))
        if chain is None or position is None:
            continue
        scheme[(chain, position)] = row
    return scheme


def unobserved_residue_map(cif_text: str) -> dict[tuple[str, int], dict[str, str]]:
    unobserved = {}
    for row in epk.extract_loop(cif_text, "pdbx_unobs_or_zero_occ_residues"):
        if epk.norm(row.get("PDB_model_num")) not in (None, "1"):
            continue
        chain = epk.norm(row.get("auth_asym_id"))
        position = int_or_none(row.get("auth_seq_id"))
        if chain is None or position is None:
            continue
        unobserved[(chain, position)] = row
    return unobserved


def residue_site_status(
    atoms: list[dict[str, Any]],
    chain: str,
    position: int,
    sequence_scheme: dict[tuple[str, int], dict[str, str]],
    unobserved_residues: dict[tuple[str, int], dict[str, str]],
) -> dict[str, Any]:
    residue_atoms = [atom for atom in atoms if atom_residue_number(atom) == position]
    scheme_row = sequence_scheme.get((chain, position))
    unobserved_row = unobserved_residues.get((chain, position))
    atom_names = sorted({atom["atom"] for atom in residue_atoms})
    residue_codes = sorted({atom["comp"] for atom in residue_atoms})
    has_acceptor = any(
        atom["comp"] in epk.ACCEPTOR_ATOMS and atom["atom"] in epk.ACCEPTOR_ATOMS[atom["comp"]]
        for atom in residue_atoms
    )
    if not residue_atoms:
        if unobserved_row:
            status = "unobserved_or_zero_occupancy_no_model_atoms"
        elif scheme_row:
            status = "in_sequence_scheme_but_no_model_atoms"
        else:
            status = "absent_from_chain_or_construct_no_model_atoms"
    elif has_acceptor:
        status = "acceptor_oxygen_modeled"
    else:
        status = "partial_or_backbone_only_no_acceptor_oxygen"
    return {
        "residue": f"S{position}",
        "auth_seq_id": position,
        "domain": CFTR_PKA_SITE_DOMAINS[position],
        "status": status,
        "sequence_scheme_present": bool(scheme_row),
        "sequence_scheme_mon_id": scheme_row.get("mon_id") if scheme_row else None,
        "sequence_scheme_auth_mon_id": scheme_row.get("auth_mon_id") if scheme_row else None,
        "unobserved_or_zero_occ_recorded": bool(unobserved_row),
        "unobserved_or_zero_occ_comp_id": unobserved_row.get("auth_comp_id")
        if unobserved_row
        else None,
        "unobserved_or_zero_occ_flag": unobserved_row.get("occupancy_flag")
        if unobserved_row
        else None,
        "residue_present_any_atom": bool(residue_atoms),
        "acceptor_oxygen_modeled": has_acceptor,
        "modeled_atom_count": len(atom_names),
        "modeled_atom_names": atom_names,
        "modeled_residue_codes": residue_codes,
    }


def nearest_distance(
    source_atom: dict[str, Any],
    candidate_atoms: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not candidate_atoms:
        return None
    distance, atom = min(
        ((epk.dist(source_atom, candidate), candidate) for candidate in candidate_atoms),
        key=lambda item: item[0],
    )
    return {
        "distance_angstrom": round(distance, 3),
        "chain": atom.get("chain"),
        "entity_id": atom.get("entity_id"),
        "residue_code": atom.get("comp"),
        "auth_seq_id": atom.get("auth_seq_id"),
        "atom_name": atom.get("atom"),
    }


def scan_pdb_entry(pdb_id: str) -> dict[str, Any]:
    metadata = epk.compact_entry_metadata(pdb_id)
    cif_text = epk.fetch_text(epk.RCSB_CIF_URL.format(pdb_id=pdb_id), timeout=60)
    atoms = [atom for row in epk.extract_loop(cif_text, "atom_site") if (atom := epk.atom_from_row(row))]
    polymer_atoms = [atom for atom in atoms if atom["group"] == "ATOM"]
    ligand_atoms = [atom for atom in atoms if atom["group"] == "HETATM"]
    ligand_groups = ligand_atom_groups(ligand_atoms)
    cftr_entities, pka_entities = polymer_entity_sets(metadata)
    sequence_scheme = cftr_sequence_scheme(cif_text, cftr_entities)
    unobserved_residues = unobserved_residue_map(cif_text)
    cftr_atoms = [
        atom for atom in polymer_atoms if str(atom.get("entity_id")) in cftr_entities
    ]
    pka_atoms = [
        atom for atom in polymer_atoms if str(atom.get("entity_id")) in pka_entities
    ]
    cftr_acceptor_atoms = [
        atom
        for atom in cftr_atoms
        if atom["comp"] in epk.ACCEPTOR_ATOMS and atom["atom"] in epk.ACCEPTOR_ATOMS[atom["comp"]]
    ]
    cftr_target_site_atoms = [
        atom for atom in cftr_atoms if atom_residue_number(atom) in CFTR_PKA_SITE_POSITIONS
    ]
    cftr_target_acceptor_atoms = [
        atom
        for atom in cftr_target_site_atoms
        if atom["comp"] in epk.ACCEPTOR_ATOMS and atom["atom"] in epk.ACCEPTOR_ATOMS[atom["comp"]]
    ]
    metals = [atom for atom in ligand_atoms if atom["comp"] in epk.METAL_CODES]
    pka_gamma_atoms = []
    all_gamma_atoms = [
        atom
        for atom in ligand_atoms
        if atom["comp"] in epk.DONOR_GAMMA_ATOMS
        and atom["atom"] in epk.DONOR_GAMMA_ATOMS[atom["comp"]]
    ]
    for gamma in all_gamma_atoms:
        associated = epk.nearest_polymer_entity(ligand_groups.get(epk.ligand_key(gamma), []), polymer_atoms)
        associated_entity = str(associated.get("entity_id")) if associated else None
        if associated_entity not in pka_entities:
            continue
        pka_gamma_atoms.append(
            {
                "gamma_ligand_code": gamma["comp"],
                "gamma_atom_name": gamma["atom"],
                "gamma_chain_name": gamma.get("chain"),
                "gamma_auth_seq_id": gamma.get("auth_seq_id"),
                "associated_polymer_chain_name": associated.get("chain") if associated else None,
                "associated_polymer_entity_id": associated_entity,
                "associated_polymer_distance_angstrom": associated.get("distance_angstrom")
                if associated
                else None,
                "local_metals": epk.local_metals(gamma, metals),
                "nearest_cftr_acceptor_any_site": nearest_distance(gamma, cftr_acceptor_atoms),
                "nearest_cftr_mapped_site_any_atom": nearest_distance(gamma, cftr_target_site_atoms),
                "nearest_cftr_mapped_site_acceptor": nearest_distance(
                    gamma, cftr_target_acceptor_atoms
                ),
            }
        )

    cftr_chains = []
    for chain in sorted({atom.get("chain") for atom in cftr_atoms if atom.get("chain")}):
        chain_atoms = [atom for atom in cftr_atoms if atom.get("chain") == chain]
        residue_numbers = sorted(
            {
                number
                for atom in chain_atoms
                if (number := atom_residue_number(atom)) is not None
            }
        )
        site_records = [
            residue_site_status(
                chain_atoms,
                chain,
                position,
                sequence_scheme,
                unobserved_residues,
            )
            for position in CFTR_PKA_SITE_POSITIONS
        ]
        cftr_chains.append(
            {
                "chain": chain,
                "entity_id": next((atom.get("entity_id") for atom in chain_atoms), None),
                "modeled_residue_count": len(residue_numbers),
                "auth_seq_id_min": residue_numbers[0] if residue_numbers else None,
                "auth_seq_id_max": residue_numbers[-1] if residue_numbers else None,
                "mapped_site_status_counts": {
                    status: sum(1 for site in site_records if site["status"] == status)
                    for status in sorted({site["status"] for site in site_records})
                },
                "mapped_sites": site_records,
            }
        )

    return {
        "pdb_id": pdb_id,
        "title": metadata.get("title"),
        "experimental_method": metadata.get("experimental_method"),
        "citation": metadata.get("citation"),
        "polymer_entities": metadata.get("polymer_entities"),
        "cftr_entity_ids": sorted(cftr_entities),
        "pka_entity_ids": sorted(pka_entities),
        "atom_count_model_1": len(atoms),
        "cftr_modeled_atom_count": len(cftr_atoms),
        "pka_modeled_atom_count": len(pka_atoms),
        "all_gamma_donor_count": len(all_gamma_atoms),
        "pka_gamma_donor_count": len(pka_gamma_atoms),
        "pka_gamma_donors": pka_gamma_atoms,
        "cftr_chains": cftr_chains,
        "source_review_status": classify_entry(pdb_id, pka_gamma_atoms, cftr_chains),
        "review_only": True,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
    }


def classify_entry(
    pdb_id: str,
    pka_gamma_atoms: list[dict[str, Any]],
    cftr_chains: list[dict[str, Any]],
) -> str:
    if not pka_gamma_atoms:
        return "no_pka_gamma_transfer_analog_in_model_review_only"
    any_acceptor = any(
        site["acceptor_oxygen_modeled"]
        for chain in cftr_chains
        for site in chain["mapped_sites"]
    )
    if not any_acceptor:
        return "source_mapped_cftr_sites_absent_or_no_acceptor_oxygen_review_only"
    any_local = any(
        donor.get("nearest_cftr_mapped_site_acceptor")
        and donor["nearest_cftr_mapped_site_acceptor"]["distance_angstrom"] <= 6.0
        for donor in pka_gamma_atoms
    )
    if any_local:
        return "mapped_cftr_acceptor_within_6a_source_validation_needed_review_only"
    return "mapped_cftr_acceptor_modeled_but_not_local_to_pka_gamma_review_only"


def build_artifact(out: Path, sleep_seconds: float) -> dict[str, Any]:
    generated_at = now_iso()
    rcsb_surfaces = []
    for surface in RCSB_SURFACES:
        rcsb_surfaces.append(search_rcsb(surface))
        if sleep_seconds:
            time.sleep(sleep_seconds)
    europe_pmc_surface = search_europe_pmc()
    if sleep_seconds:
        time.sleep(sleep_seconds)
    article = article_source_summary()
    rows = []
    fetch_failures = []
    for pdb_id in PDB_IDS:
        try:
            rows.append(scan_pdb_entry(pdb_id))
        except Exception as exc:  # noqa: BLE001 - compact research failure record.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    for row in rows:
        status = row["source_review_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "pka_cftr_source_mapped_site_review",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "target_pdb_ids": PDB_IDS,
            "target_article_doi": ARTICLE_DOI,
            "target_article_pmid": ARTICLE_PMID,
            "target_article_pmcid": ARTICLE_PMCID,
            "rcsb_surface_rows_returned_total": sum(
                surface["returned_count"] for surface in rcsb_surfaces
            ),
            "europe_pmc_rows_returned": europe_pmc_surface["returned_count"],
            "pdb_entries_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "source_review_status_counts": status_counts,
            "primary_result": (
                "The PKA/CFTR structures are source-relevant folded-protein substrate "
                "complexes, but they do not provide clean transfer-state positive "
                "evidence because source-mapped CFTR phosphorylation sites are absent, "
                "disordered, or lack modeled acceptor oxygen near PKA gamma."
            ),
        },
        "article_source": article,
        "search_surfaces": {
            "rcsb": rcsb_surfaces,
            "europe_pmc": europe_pmc_surface,
        },
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
    artifact = build_artifact(args.out, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "pdb_entries_reviewed": artifact["metadata"]["pdb_entries_reviewed"],
                "source_review_status_counts": artifact["metadata"][
                    "source_review_status_counts"
                ],
                "fetch_failure_count": artifact["metadata"]["fetch_failure_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
