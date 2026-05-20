#!/usr/bin/env python3
"""Bounded PIKK/ATM-Tel1 metal-context follow-up for ePK positive evidence.

This helper writes compact review-only summaries. It fetches mmCIF files only
transiently and never stores coordinate dumps.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import epk_evidence_search as scout


LANE_ID = "epk_positive_evidence"
EUROPE_PMC_XML_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11933327/fullTextXML"
EUROPE_PMC_SUPP_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11933327/supplementaryFiles"


@dataclass(frozen=True)
class Surface:
    surface_id: str
    text: str
    rows: int = 25
    ligand: str | None = None
    metal: str | None = None
    note: str | None = None


SURFACES = [
    Surface(
        "exact_article_title_atm_tel1",
        "Asymmetric activation of dimeric ATM Tel1 kinase",
        rows=25,
        note="article-title sibling surface",
    ),
    Surface("atm_tel1_chk2_peptide_anp", "ATM Tel1 CHK2 peptide ANP"),
    Surface("atm_tel1_chk2_peptide_amp_pnp", "ATM Tel1 CHK2 peptide AMP-PNP"),
    Surface("atm_tel1_chk2_metal", "ATM Tel1 CHK2 magnesium"),
    Surface("full_length_chk2_atm_tel1", "full-length CHK2 ATM Tel1 substrate peptide"),
    Surface("pikk_substrate_peptide_amp_pnp_mg", "PIKK substrate peptide AMP-PNP magnesium"),
    Surface("pikk_substrate_peptide_anp_mg", "PIKK substrate peptide ANP magnesium"),
    Surface("pikk_kinase_substrate_peptide_anp_mg", "PIKK kinase substrate peptide ANP magnesium"),
    Surface("atr_mec1_substrate_peptide_amp_pnp_mg", "ATR Mec1 substrate peptide AMP-PNP magnesium"),
    Surface("dna_pk_substrate_peptide_amp_pnp_mg", "DNA-PK substrate peptide AMP-PNP magnesium"),
    Surface("mtor_substrate_peptide_amp_pnp_mg", "mTOR substrate peptide AMP-PNP magnesium"),
    Surface("atm_tel1_ligand_anp", "ATM Tel1", ligand="ANP"),
    Surface("atm_tel1_ligand_anp_mg", "ATM Tel1", ligand="ANP", metal="MG"),
    Surface("atm_tel1_ligand_ags_mg", "ATM Tel1", ligand="AGS", metal="MG"),
    Surface("chk2_peptide_ligand_anp", "CHK2 peptide", ligand="ANP"),
    Surface("pikk_peptide_ligand_anp_mg", "PIKK peptide substrate", ligand="ANP", metal="MG"),
    Surface("pikk_peptide_ligand_atp_mg", "PIKK peptide substrate", ligand="ATP", metal="MG"),
    Surface("mtor_peptide_ligand_anp_mg", "mTOR substrate peptide", ligand="ANP", metal="MG"),
    Surface("mtor_peptide_ligand_atp_mg", "mTOR substrate peptide", ligand="ATP", metal="MG"),
    Surface("mtor_peptide_ligand_ags", "mTOR substrate peptide", ligand="AGS"),
    Surface("smg1_upf1_ligand_anp_mg", "SMG1 UPF1 substrate", ligand="ANP", metal="MG"),
    Surface("smg1_upf1_ligand_atp_mg", "SMG1 UPF1 substrate", ligand="ATP", metal="MG"),
    Surface("smg1_upf1_amp_pnp_mg", "SMG1 UPF1 AMP-PNP magnesium"),
    Surface("dna_pkcs_ligand_anp_mg", "DNA-PKcs substrate", ligand="ANP", metal="MG"),
    Surface("dna_pkcs_ligand_atp_mg", "DNA-PKcs substrate", ligand="ATP", metal="MG"),
    Surface("dna_pkcs_ligand_ags_mg", "DNA-PKcs substrate", ligand="AGS", metal="MG"),
    Surface("atr_mec1_ligand_anp_mg", "ATR Mec1 substrate", ligand="ANP", metal="MG"),
    Surface("atr_mec1_ligand_atp_mg", "ATR Mec1 substrate", ligand="ATP", metal="MG"),
    Surface("atm_substrate_ligand_anp_mg", "ATM substrate peptide", ligand="ANP", metal="MG"),
    Surface("atm_substrate_ligand_ags_mg", "ATM substrate peptide", ligand="AGS", metal="MG"),
    Surface("mtor_4ebp1_ligand_anp_mg", "mTOR 4EBP1 substrate", ligand="ANP", metal="MG"),
    Surface("mtor_4ebp1_ligand_atp_mg", "mTOR 4EBP1 substrate", ligand="ATP", metal="MG"),
    Surface("pikk_full_length_substrate_ligand_anp_mg", "PIKK full-length substrate", ligand="ANP", metal="MG"),
    Surface("pikk_full_length_substrate_ligand_atp_mg", "PIKK full-length substrate", ligand="ATP", metal="MG"),
]


FIXED_REVIEW_IDS = ["9IZ0", "9IZ7"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def decode_response_json(req: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 204:
                return {"total_count": 0, "result_set": []}
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == 204:
            return {"total_count": 0, "result_set": []}
        raise
    if not body:
        return {"total_count": 0, "result_set": []}
    return json.loads(body)


def surface_payload(surface: Surface) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = [
        {"type": "terminal", "service": "full_text", "parameters": {"value": surface.text}}
    ]
    if surface.ligand:
        nodes.append(
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                    "operator": "exact_match",
                    "value": surface.ligand,
                },
            }
        )
    if surface.metal:
        nodes.append(
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                    "operator": "exact_match",
                    "value": surface.metal,
                },
            }
        )
    query = nodes[0] if len(nodes) == 1 else {"type": "group", "logical_operator": "and", "nodes": nodes}
    return {
        "query": query,
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": surface.rows},
            "results_content_type": ["experimental"],
        },
    }


def run_surface(surface: Surface) -> dict[str, Any]:
    payload = surface_payload(surface)
    req = urllib.request.Request(
        scout.RCSB_SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "catalytic-earth-epk-positive-evidence/1.0",
        },
    )
    result = decode_response_json(req)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    ligand_bits = [bit for bit in (surface.ligand, surface.metal) if bit]
    return {
        "surface_id": surface.surface_id,
        "query_or_source": "RCSB "
        + ("full_text + ligand" if ligand_bits else "full_text")
        + f": {surface.text}"
        + (f" [{' + '.join(ligand_bits)}]" if ligand_bits else ""),
        "note": surface.note,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def count_terms(text: str) -> dict[str, Any]:
    return {
        "amp_pnp_mentions": len(re.findall(r"AMP-PNP|AMPPNP", text, flags=re.I)),
        "anp_mentions": len(re.findall(r"\bANP\b", text)),
        "magnesium_word_mentions": len(re.findall(r"magnesium", text, flags=re.I)),
        "mg_exact_or_salt_mentions": len(re.findall(r"\bMg(?:2\+|Cl2|Cl)?\b", text)),
        "manganese_word_mentions": len(re.findall(r"manganese", text, flags=re.I)),
        "mn_exact_or_salt_mentions": len(re.findall(r"\bMn(?:2\+|Cl2|Cl)?\b", text)),
        "chk2_mentions": len(re.findall(r"\bCHK2\b", text)),
        "thr68_mentions": len(re.findall(r"Thr68|threonine \\(Thr68\\)", text, flags=re.I)),
        "pdb_9iz0_mentions": len(re.findall(r"\b9IZ0\b", text)),
        "pdb_9iz7_mentions": len(re.findall(r"\b9IZ7\b", text)),
    }


def count_reliable_supplement_terms(text: str, extraction_method: str) -> dict[str, Any]:
    counts = count_terms(text)
    if extraction_method == "strings":
        counts["mg_exact_or_salt_mentions"] = len(re.findall(r"\bMg(?:Cl2|Cl)\b", text))
        counts["mn_exact_or_salt_mentions"] = len(re.findall(r"\bMn(?:Cl2|Cl)\b", text))
        counts["single_token_mg_mn_note"] = (
            "Ignored bare Mg/Mn tokens because strings-based extraction also returns "
            "binary/compressed PDF noise."
        )
    return counts


def extract_supplement_text(zip_bytes: bytes) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="epk_pikk_supp_") as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        zip_path = tmp_dir / "supplementary.zip"
        zip_path.write_bytes(zip_bytes)
        with zipfile.ZipFile(zip_path) as zf:
            file_manifest = [
                {"filename": info.filename, "file_size": info.file_size}
                for info in zf.infolist()
            ]
            pdf_names = [info.filename for info in zf.infolist() if info.filename.lower().endswith(".pdf")]
            text = ""
            extraction_method = "no_pdf_found"
            if pdf_names:
                pdf_path = tmp_dir / Path(pdf_names[0]).name
                pdf_path.write_bytes(zf.read(pdf_names[0]))
                if shutil.which("pdftotext"):
                    txt_path = pdf_path.with_suffix(".txt")
                    subprocess.run(["pdftotext", str(pdf_path), str(txt_path)], check=False)
                    if txt_path.exists():
                        text = txt_path.read_text(errors="replace")
                        extraction_method = "pdftotext"
                if not text and shutil.which("strings"):
                    proc = subprocess.run(
                        ["strings", str(pdf_path)], text=True, capture_output=True, check=False
                    )
                    text = proc.stdout
                    extraction_method = "strings"
            return {
                "zip_byte_count": len(zip_bytes),
                "file_manifest": file_manifest,
                "pdf_names": pdf_names,
                "text_extraction_method": extraction_method,
                "term_counts": count_reliable_supplement_terms(text, extraction_method),
                "text_char_count": len(text),
            }


def nonpolymer_entities(pdb_id: str, entity_ids: list[str]) -> list[dict[str, Any]]:
    rows = []
    for entity_id in entity_ids:
        url = f"https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb_id}/{entity_id}"
        try:
            data = scout.fetch_json(url)
        except Exception as exc:  # noqa: BLE001 - compact source-failure record.
            rows.append({"entity_id": entity_id, "fetch_error": repr(exc)})
            continue
        ids = data.get("rcsb_nonpolymer_entity_container_identifiers", {})
        desc = data.get("rcsb_nonpolymer_entity", {})
        rows.append(
            {
                "entity_id": entity_id,
                "nonpolymer_comp_id": ids.get("nonpolymer_comp_id") or ids.get("chem_ref_def_id"),
                "auth_asym_ids": ids.get("auth_asym_ids", []),
                "description": desc.get("pdbx_description"),
                "molecule_count": desc.get("pdbx_number_of_molecules"),
            }
        )
    return rows


def status_from_scan(scan: dict[str, Any]) -> str:
    metal_hits = [
        hit for hit in scan.get("heteromeric_candidate_hits", []) if hit.get("local_metals")
    ]
    if metal_hits:
        return "local_metal_gamma_acceptor_candidate_source_map_pending_review_only"
    if scan.get("heteromeric_candidate_hits"):
        return "gamma_acceptor_candidate_without_local_metal_review_only"
    if any(record.get("local_metals") for record in scan.get("gamma_records", [])):
        return "local_metal_gamma_without_heteromeric_acceptor_review_only"
    if scan.get("donor_gamma_atom_count"):
        return "gamma_without_local_metal_or_heteromeric_acceptor_review_only"
    return "no_active_gamma_donor_review_only"


def compact_scan(scan: dict[str, Any]) -> dict[str, Any]:
    return {
        "atom_count_model_1": scan.get("atom_count_model_1"),
        "donor_gamma_atom_count": scan.get("donor_gamma_atom_count"),
        "acceptor_atom_count": scan.get("acceptor_atom_count"),
        "gamma_records": scan.get("gamma_records", []),
        "heteromeric_candidate_hits": scan.get("heteromeric_candidate_hits", []),
    }


def build_artifact(out: Path) -> dict[str, Any]:
    generated_at = now_iso()
    surfaces = [run_surface(surface) for surface in SURFACES]
    seen: dict[str, list[dict[str, Any]]] = {}
    for surface in surfaces:
        for rank, pdb_id in enumerate(surface["pdb_ids"], start=1):
            seen.setdefault(pdb_id, []).append(
                {
                    "surface_id": surface["surface_id"],
                    "rank": rank,
                    "query_or_source": surface["query_or_source"],
                }
            )
    for pdb_id in FIXED_REVIEW_IDS:
        seen.setdefault(pdb_id, []).append(
            {
                "surface_id": "fixed_followup_seed",
                "rank": 1,
                "query_or_source": "Fixed 9IZ0/9IZ7 source sibling review seed",
            }
        )

    article_xml = scout.fetch_text(EUROPE_PMC_XML_URL)
    source_checks = {
        "article_full_text_xml_url": EUROPE_PMC_XML_URL,
        "article_term_counts": count_terms(article_xml),
        "article_context_flags": {
            "maps_chk2_63_74": bool(re.search(r"CHK2<sup>63.*?74</sup>|CHK2\\D+63\\D+74", article_xml)),
            "maps_thr68_phosphoacceptor": bool(
                re.search(r"phospho-acceptor threonine \(Thr68\)", article_xml)
            ),
            "states_thr68_oriented_to_gamma_phosphate": bool(
                re.search(r"Thr68.*?gamma-phosphate|Thr68.*?γ-phosphate", article_xml, flags=re.I | re.S)
            ),
            "states_full_length_chk2_binding_without_pdb": bool(
                re.search(r"full-length CHK2", article_xml) and re.search(r"9IZ0", article_xml)
            ),
        },
        "supplementary_files_url": EUROPE_PMC_SUPP_URL,
        "supplementary_checks": extract_supplement_text(fetch_bytes(EUROPE_PMC_SUPP_URL)),
    }

    rows = []
    fetch_failures = []
    for pdb_id in sorted(seen):
        try:
            metadata = scout.compact_entry_metadata(pdb_id)
            entry = scout.fetch_json(scout.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
            nonpolymer_ids = (
                entry.get("rcsb_entry_container_identifiers", {}).get("non_polymer_entity_ids", [])
                or []
            )
            scan = scout.scan_cif_for_candidates(
                scout.fetch_text(scout.RCSB_CIF_URL.format(pdb_id=pdb_id))
            )
            row = {
                "pdb_id": pdb_id,
                "title": metadata.get("title"),
                "citation": metadata.get("citation"),
                "polymer_entities": metadata.get("polymer_entities"),
                "nonpolymer_entities": nonpolymer_entities(pdb_id, [str(item) for item in nonpolymer_ids]),
                "search_hits": seen[pdb_id],
                "candidate_status": status_from_scan(scan),
                "review_only": True,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "ready_for_label_import": False,
                "ready_for_production_scoring": False,
                **compact_scan(scan),
            }
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - compact source-failure record.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
                    "pdb_id": pdb_id,
                    "search_hits": seen[pdb_id],
                    "candidate_status": "fetch_or_parse_failed_review_only",
                    "fetch_error": repr(exc),
                    "review_only": True,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                    "ready_for_label_import": False,
                    "ready_for_production_scoring": False,
                }
            )

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["candidate_status"]] = status_counts.get(row["candidate_status"], 0) + 1

    local_metal_source_map_candidates = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_gamma_acceptor_candidate_source_map_pending_review_only"
    ]

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "pikk_atm_tel1_chk2_metal_context_followup",
            "generated_at": generated_at,
            "hypothesis": (
                "9IZ0 or sibling PIKK/ATM/Tel1 substrate structures may include local "
                "Mg/Mn or equivalent metal context that converts the source-mapped CHK2 "
                "peptide geometry into stronger review-only positive evidence."
            ),
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "surface_count": len(surfaces),
            "surface_rows_returned_total": sum(surface["returned_count"] for surface in surfaces),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_source_map_candidate_pdb_ids": local_metal_source_map_candidates,
            "local_metal_source_map_candidate_count": len(local_metal_source_map_candidates),
            "recommendation": (
                "Keep 9IZ0 as source-mapped peptide evidence with a no-local-metal caveat. "
                "Sibling ATM/Tel1 structures provide nucleotide/metal-only negatives, and "
                "the bounded PIKK ligand surfaces did not expose a source-mappable local "
                "metal/gamma acceptor candidate."
            ),
            "source_urls": [
                scout.RCSB_SEARCH_URL,
                scout.RCSB_ENTRY_URL,
                scout.RCSB_POLYMER_ENTITY_URL,
                scout.RCSB_CIF_URL,
                EUROPE_PMC_XML_URL,
                EUROPE_PMC_SUPP_URL,
            ],
        },
        "source_checks": source_checks,
        "search_surfaces": surfaces,
        "fetch_failures": fetch_failures,
        "rows": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.out)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "local_metal_source_map_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_source_map_candidate_pdb_ids"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
