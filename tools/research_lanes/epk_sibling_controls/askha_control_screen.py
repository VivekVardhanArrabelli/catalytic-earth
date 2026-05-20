#!/usr/bin/env python3
"""Bounded sibling-control screen for ePK review-only research.

The script fetches candidate mmCIF files in memory, derives compact local
gamma-phosphate measurements, and writes a JSON evidence artifact. It does not
persist raw coordinate files.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"

FAMILY_CONFIGS = {
    "askha": {
        "family_id": "askha",
        "family_name": "ASKHA sugar and acetate kinases",
        "method": "epk_sibling_controls_askha_bounded_control_screen",
        "query_terms": [
            "glucokinase ATP magnesium",
            "glucokinase AMP-PNP magnesium",
            "hexokinase ATP magnesium",
            "hexokinase AMP-PNP magnesium",
            "acetate kinase ATP magnesium",
            "acetate kinase AMP-PNP",
        ],
        "seed_pdb_ids": [
            "3FGU",
            "1QHA",
            "1IG8",
            "1G99",
            "1V4S",
            "1V4T",
            "3A0I",
            "3F9M",
            "3FR0",
            "3GOI",
            "3H1V",
            "1TUU",
            "1TUY",
        ],
        "title_keywords": ("glucokinase", "hexokinase", "acetate kinase"),
        "prior_artifact_label": "seed_from_prior_askha_artifacts_or_graph_linked_alternates",
        "next_query": (
            "Run the same bounded source-free screen for dNK thymidine/deoxyguanosine kinase "
            "with gamma-capable nucleotide analogs and local Mg/Mn context."
        ),
    },
    "dnk": {
        "family_id": "dnk",
        "family_name": "Deoxynucleoside kinases",
        "method": "epk_sibling_controls_dnk_bounded_control_screen",
        "query_terms": [
            "thymidine kinase ATP magnesium",
            "thymidine kinase deoxythymidine triphosphate magnesium",
            "deoxyguanosine kinase DTP magnesium",
            "deoxyguanosine kinase ATP magnesium",
            "deoxycytidine kinase ATP magnesium",
            "deoxynucleoside kinase ATP magnesium",
        ],
        "seed_pdb_ids": [
            "2OCP",
            "1KIM",
            "1E2D",
            "1KI3",
            "2QQE",
            "2QQF",
        ],
        "title_keywords": (
            "thymidine kinase",
            "deoxyguanosine kinase",
            "deoxycytidine kinase",
            "deoxynucleoside kinase",
        ),
        "prior_artifact_label": "seed_from_prior_dnk_artifacts_or_graph_linked_alternates",
        "next_query": (
            "Run the same bounded source-free screen for GHKL histidine-kinase/PDK "
            "controls with gamma-capable nucleotide analogs and local Mg/Mn context."
        ),
    },
    "ghkl": {
        "family_id": "ghkl",
        "family_name": "GHKL/Bergerat ATP-binding kinases",
        "method": "epk_sibling_controls_ghkl_bounded_control_screen",
        "query_terms": [
            "histidine kinase ATP magnesium",
            "histidine kinase AMP-PNP magnesium",
            "CheA ATP magnesium",
            "CheA AMP-PNP magnesium",
            "pyruvate dehydrogenase kinase ATP magnesium",
            "pyruvate dehydrogenase kinase AMP-PNP magnesium",
        ],
        "seed_pdb_ids": [
            "1I58",
            "1I59",
            "1I5A",
            "1I5B",
            "1I5C",
            "3CRK",
            "3CRL",
            "1JM6",
            "1TQG",
        ],
        "title_keywords": (
            "histidine kinase",
            "chea",
            "pyruvate dehydrogenase kinase",
            "pyruvate dehydrogenase (acetyl-transferring) kinase",
        ),
        "prior_artifact_label": "seed_from_prior_ghkl_artifacts_or_graph_linked_alternates",
        "next_query": (
            "Run the same bounded source-free screen for GHMP mevalonate/homoserine/CDP-ME "
            "kinase controls with gamma-capable nucleotide analogs and local Mg/Mn context."
        ),
    },
    "ghmp": {
        "family_id": "ghmp",
        "family_name": "GHMP-superfamily kinases",
        "method": "epk_sibling_controls_ghmp_bounded_control_screen",
        "query_terms": [
            "mevalonate kinase ATP magnesium",
            "mevalonate kinase AMP-PNP magnesium",
            "phosphomevalonate kinase ATP magnesium",
            "homoserine kinase ATP magnesium",
            "CDP-ME kinase ATP magnesium",
            "4-(cytidine 5'-diphospho)-2-C-methyl-D-erythritol kinase AMP-PNP",
        ],
        "seed_pdb_ids": [
            "1OJ4",
            "1FWK",
            "2R42",
            "2OI2",
            "3GON",
            "3LL3",
        ],
        "title_keywords": (
            "mevalonate kinase",
            "phosphomevalonate kinase",
            "homoserine kinase",
            "cdp-me kinase",
            "cytidine 5'-diphospho",
            "methyl-d-erythritol kinase",
        ),
        "prior_artifact_label": "seed_from_prior_ghmp_artifacts_or_graph_linked_alternates",
        "next_query": (
            "Expand ATP-grasp beyond the two measured rows or rerun ASKHA/dNK/GHKL/GHMP "
            "screens with stricter nonpolymer-acceptor controls."
        ),
    },
    "atp_grasp": {
        "family_id": "atp_grasp",
        "family_name": "ATP-grasp ligases",
        "method": "epk_sibling_controls_atp_grasp_bounded_control_screen",
        "query_terms": [
            "D-alanine D-alanine ligase ATP magnesium",
            "D-alanine D-alanine ligase AMP-PNP magnesium",
            "D-alanine D-alanine ligase ADP phosphate magnesium",
            "D-alanine D-alanine ligase ADP phosphoryl phosphinate magnesium",
            "D-alanine D-alanine ligase ADP phosphoryl phosphonate magnesium",
            "D-Ala D-Ala ligase ATP magnesium",
            "D-Ala D-Ala ligase ADP phosphate magnesium",
            "glutathione synthase ATP magnesium",
            "glutathione synthetase AMP-PNP magnesium",
            "glycinamide ribonucleotide synthetase ATP magnesium",
            "PurD ATP magnesium",
            "biotin carboxylase ATP magnesium",
            "glutamate-cysteine ligase ATP magnesium",
            "Mur ligase ATP magnesium",
            "carbamoyl phosphate synthetase ATP magnesium",
            "carbamoyl phosphate synthetase ADP phosphate magnesium",
            "pseudomurein peptide ligase UDP phosphate magnesium",
            "ATP-grasp ligase ATP magnesium",
            "ATP-grasp ligase AMP-PNP magnesium",
            "ATP-grasp ligase ADP phosphate magnesium",
        ],
        "seed_pdb_ids": [
            "1EHI",
            "1IOV",
            "1IOW",
            "2DLN",
            "2ZDG",
            "3R5F",
            "5C1O",
            "5DOU",
            "6NO5",
            "6U1H",
            "6U1I",
            "6VR8",
            "7DRM",
            "7DRP",
        ],
        "title_keywords": (
            "d-alanine",
            "d-ala",
            "d-alanyl",
            "alanine ligase",
            "glutathione synthase",
            "glutathione synthetase",
            "glycinamide ribonucleotide synthetase",
            "glycinamide ribonucleotide transformylase",
            "ribonucleotide synthetase",
            "purt-encoded",
            "purD",
            "biotin carboxylase",
            "pyruvate carboxylase",
            "glutamate-cysteine ligase",
            "glutamate cysteine ligase",
            "gamma-glutamylcysteine synthetase",
            "glutathionylspermidine synthetase",
            "scgcl",
            "mur ligase",
            "murc",
            "murd",
            "mure",
            "murf",
            "carbamoyl phosphate synthetase",
            "cyanophycin synthetase",
            "folylpolyglutamate synthetase",
            "atp-grasp",
            "atp grasp",
        ),
        "prior_artifact_label": "seed_from_prior_atp_grasp_artifacts_or_graph_linked_alternates",
        "next_query": (
            "Rerun ATP-grasp with an explicit phosphorylated-acceptor/product-state branch "
            "for ADP plus phosphate or phosphorylated nonpolymer controls."
        ),
    },
    "pfka": {
        "family_id": "pfka",
        "family_name": "PfkA-fold phosphofructokinases",
        "method": "epk_sibling_controls_pfka_bounded_control_screen",
        "query_terms": [
            "phosphofructokinase ATP magnesium",
            "phosphofructokinase AMP-PNP magnesium",
            "phosphofructokinase fructose 6-phosphate ATP magnesium",
            "ATP-dependent phosphofructokinase ATP magnesium",
            "phosphofructokinase-1 ATP Mg",
            "PFK ATP magnesium",
        ],
        "seed_pdb_ids": [
            "3F5M",
            "4XYJ",
            "5XZ8",
            "8W2H",
            "8W2J",
        ],
        "title_keywords": (
            "phosphofructokinase",
            "phosphofructo kinase",
            "pfk",
        ),
        "prior_artifact_label": "seed_from_prior_pfka_homolog_gamma_distance_sample",
        "next_query": (
            "Run the source-free bounded sibling-control screen for PfkB/ribokinase-family "
            "kinases, then NDK if PfkB adds no new weak-rule stress."
        ),
    },
    "pfkb": {
        "family_id": "pfkb",
        "family_name": "PfkB/ribokinase-family kinases",
        "method": "epk_sibling_controls_pfkb_bounded_control_screen",
        "query_terms": [
            "ribokinase ATP magnesium",
            "ribokinase AMP-PNP magnesium",
            "adenosine kinase ATP magnesium",
            "aminoimidazole riboside kinase ATP magnesium",
            "phosphofructokinase-2 ATP magnesium",
            "thiazole kinase ATP magnesium",
            "PfkB family kinase ATP magnesium",
        ],
        "seed_pdb_ids": [
            "1ESQ",
            "1TZ6",
            "3CQD",
            "3IQ0",
            "3UMO",
            "3UMP",
            "3UQD",
            "3UQE",
            "6ILT",
        ],
        "title_keywords": (
            "ribokinase",
            "adenosine kinase",
            "aminoimidazole riboside kinase",
            "phosphofructokinase-2",
            "thiazole kinase",
            "pfkb",
            "ketohexokinase",
            "fructokinase",
        ),
        "prior_artifact_label": "seed_from_prior_pfkb_homolog_gamma_distance_sample",
        "next_query": (
            "Run the source-free bounded sibling-control screen for NDK ATP-state controls "
            "or extend PfkA/PfkB only if a new query term exposes additional metal-supported rows."
        ),
    },
}

GAMMA_CAPABLE_CODES = {"ATP", "ANP", "ACP", "AGS", "DTP", "GTP"}
PRODUCT_OR_PARTIAL_CODES = {"ADP", "AMP", "GDP", "UDP", "CDP"}
PHOSPHORYL_MIMIC_CODES = {"PO4", "PHY", "POB"}
METAL_CODES = {"MG", "MN"}
WATER_CODES = {"HOH", "WAT", "DOD"}
COMMON_NON_ACCEPTOR_CODES = {
    *GAMMA_CAPABLE_CODES,
    *PRODUCT_OR_PARTIAL_CODES,
    *METAL_CODES,
    *WATER_CODES,
    "NA",
    "K",
    "CL",
    "SO4",
    "PO4",
    "ACT",
    "GOL",
    "EDO",
    "PEG",
}
HYDROXYL_ATOMS = {
    ("SER", "OG"),
    ("THR", "OG1"),
    ("TYR", "OH"),
}
GAMMA_ATOM_NAMES = {"PG", "P3G", "P3", "PG1"}
PRODUCT_NUCLEOTIDE_BETA_ATOM_NAMES = {"PB", "P2B", "P2"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def post_json(url: str, payload: dict, timeout: int = 30) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "epk-sibling-control-screen/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def rcsb_full_text(term: str, rows: int) -> list[str]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": term},
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "return_all_hits": False,
            "sort": [{"sort_by": "score", "direction": "desc"}],
        },
    }
    data = post_json(RCSB_SEARCH_URL, payload)
    return [row["identifier"].upper() for row in data.get("result_set", [])]


def parse_struct_title(cif_text: str) -> str | None:
    lines = cif_text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("_struct.title"):
            continue
        try:
            tokens = shlex.split(stripped, posix=True)
        except ValueError:
            tokens = stripped.split(maxsplit=1)
        if len(tokens) > 1:
            return " ".join(tokens[1:]).strip()
        if idx + 1 < len(lines):
            next_line = lines[idx + 1].strip()
            if next_line.startswith(";"):
                collected = []
                for follow in lines[idx + 2 :]:
                    if follow.startswith(";"):
                        break
                    collected.append(follow.rstrip())
                return " ".join(collected).strip() or None
            if next_line and not next_line.startswith(("#", "_", "loop_")):
                try:
                    next_tokens = shlex.split(next_line, posix=True)
                except ValueError:
                    next_tokens = [next_line.strip("'\"")]
                return " ".join(next_tokens).strip() or None
    return None


def parse_atom_site(cif_text: str) -> list[dict]:
    lines = cif_text.splitlines()
    atoms: list[dict] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].strip() != "loop_":
            idx += 1
            continue
        field_idx = idx + 1
        fields: list[str] = []
        while field_idx < len(lines) and lines[field_idx].strip().startswith("_"):
            fields.append(lines[field_idx].strip())
            field_idx += 1
        if not fields or not all(field.startswith("_atom_site.") for field in fields[:1]):
            idx = field_idx
            continue
        if not any(field.startswith("_atom_site.") for field in fields):
            idx = field_idx
            continue
        row_len = len(fields)
        pending: list[str] = []
        row_idx = field_idx
        while row_idx < len(lines):
            stripped = lines[row_idx].strip()
            if not stripped:
                row_idx += 1
                continue
            if stripped == "#" or stripped == "loop_" or stripped.startswith("_"):
                break
            try:
                pending.extend(shlex.split(stripped, posix=True))
            except ValueError:
                pending.extend(stripped.split())
            while len(pending) >= row_len:
                row_tokens = pending[:row_len]
                del pending[:row_len]
                row = dict(zip(fields, row_tokens))
                if row.get("_atom_site.group_PDB") in {"ATOM", "HETATM"}:
                    atom = normalize_atom(row)
                    if atom is not None:
                        atoms.append(atom)
            row_idx += 1
        idx = row_idx
    return atoms


def normalize_atom(row: dict) -> dict | None:
    try:
        x = float(row.get("_atom_site.Cartn_x", "nan"))
        y = float(row.get("_atom_site.Cartn_y", "nan"))
        z = float(row.get("_atom_site.Cartn_z", "nan"))
    except ValueError:
        return None
    if not all(math.isfinite(v) for v in (x, y, z)):
        return None
    alt_id = row.get("_atom_site.label_alt_id", ".")
    if alt_id not in {".", "?", "A", "1"}:
        return None
    comp = (
        row.get("_atom_site.label_comp_id")
        or row.get("_atom_site.auth_comp_id")
        or ""
    ).upper()
    atom = (
        row.get("_atom_site.label_atom_id")
        or row.get("_atom_site.auth_atom_id")
        or ""
    ).upper()
    return {
        "group": row.get("_atom_site.group_PDB"),
        "element": (row.get("_atom_site.type_symbol") or "").upper(),
        "atom": atom,
        "comp": comp,
        "label_asym_id": row.get("_atom_site.label_asym_id"),
        "auth_asym_id": row.get("_atom_site.auth_asym_id"),
        "label_seq_id": row.get("_atom_site.label_seq_id"),
        "auth_seq_id": row.get("_atom_site.auth_seq_id"),
        "xyz": (x, y, z),
    }


def distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((a_i - b_i) ** 2 for a_i, b_i in zip(a, b)))


def compact_atom(atom: dict, distance_angstrom: float) -> dict:
    return {
        "distance_angstrom": round(distance_angstrom, 3),
        "comp": atom["comp"],
        "atom": atom["atom"],
        "auth_asym_id": atom["auth_asym_id"],
        "auth_seq_id": atom["auth_seq_id"],
        "label_asym_id": atom["label_asym_id"],
        "label_seq_id": atom["label_seq_id"],
    }


def atom_pairs(source_atoms: list[dict], target_atoms: list[dict]) -> list[tuple[float, dict, dict]]:
    pairs = [
        (distance(source["xyz"], target["xyz"]), source, target)
        for source in source_atoms
        for target in target_atoms
    ]
    pairs.sort(key=lambda row: row[0])
    return pairs


def compact_pair_rows(
    pairs: list[tuple[float, dict, dict]],
    source_prefix: str,
    target_prefix: str,
    limit: int = 5,
) -> list[dict]:
    rows = []
    for dist, source, target in pairs[:limit]:
        rows.append(
            {
                "distance_angstrom": round(dist, 3),
                f"{source_prefix}_comp": source["comp"],
                f"{source_prefix}_atom": source["atom"],
                f"{source_prefix}_auth_asym_id": source["auth_asym_id"],
                f"{source_prefix}_auth_seq_id": source["auth_seq_id"],
                f"{source_prefix}_label_asym_id": source["label_asym_id"],
                f"{source_prefix}_label_seq_id": source["label_seq_id"],
                f"{target_prefix}_comp": target["comp"],
                f"{target_prefix}_atom": target["atom"],
                f"{target_prefix}_auth_asym_id": target["auth_asym_id"],
                f"{target_prefix}_auth_seq_id": target["auth_seq_id"],
                f"{target_prefix}_label_asym_id": target["label_asym_id"],
                f"{target_prefix}_label_seq_id": target["label_seq_id"],
            }
        )
    return rows


def title_has_family_signal(title: str | None, config: dict) -> bool:
    if not title:
        return False
    lower = title.lower()
    return any(keyword in lower for keyword in config["title_keywords"])


def scan_structure(pdb_id: str, query_origins: list[str], config: dict) -> dict:
    pdb_id = pdb_id.upper()
    try:
        cif_text = fetch_text(RCSB_CIF_URL.format(pdb_id=pdb_id), timeout=45)
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "pdb_id": pdb_id,
            "fetch_status": f"fetch_failed:{type(exc).__name__}",
            "query_origins": query_origins,
            "review_status": "fetch_failed",
        }

    title = parse_struct_title(cif_text)
    atoms = parse_atom_site(cif_text)
    observed_ligand_codes = sorted(
        {atom["comp"] for atom in atoms if atom["group"] == "HETATM" and atom["comp"] not in WATER_CODES}
    )
    gamma_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["comp"] in GAMMA_CAPABLE_CODES
        and atom["atom"] in GAMMA_ATOM_NAMES
    ]
    protein_hydroxyl_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "ATOM" and (atom["comp"], atom["atom"]) in HYDROXYL_ATOMS
    ]
    nonpolymer_oxygen_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["element"] == "O"
        and atom["comp"] not in COMMON_NON_ACCEPTOR_CODES
    ]
    metal_atoms = [
        atom for atom in atoms if atom["group"] == "HETATM" and atom["comp"] in METAL_CODES
    ]
    product_codes = sorted({atom["comp"] for atom in atoms if atom["comp"] in PRODUCT_OR_PARTIAL_CODES})
    phosphoryl_mimic_codes = sorted(
        {atom["comp"] for atom in atoms if atom["comp"] in PHOSPHORYL_MIMIC_CODES}
    )
    phosphorylated_nonpolymer_codes = sorted(
        {
            atom["comp"]
            for atom in atoms
            if atom["comp"] in PHOSPHORYL_MIMIC_CODES
            and any(
                other["comp"] == atom["comp"] and other["group"] == "HETATM" and other["element"] == "C"
                for other in atoms
            )
        }
    )
    product_nucleotide_beta_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["comp"] in PRODUCT_OR_PARTIAL_CODES
        and atom["atom"] in PRODUCT_NUCLEOTIDE_BETA_ATOM_NAMES
    ]
    product_state_phosphoryl_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["comp"] in PHOSPHORYL_MIMIC_CODES
        and atom["element"] == "P"
    ]
    product_state_phosphoryl_oxygen_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["comp"] in PHOSPHORYL_MIMIC_CODES
        and atom["element"] == "O"
    ]
    product_state_nonpolymer_oxygen_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["element"] == "O"
        and atom["comp"] not in PRODUCT_OR_PARTIAL_CODES
        and atom["comp"] not in METAL_CODES
        and atom["comp"] not in WATER_CODES
    ]
    gamma_codes = sorted({atom["comp"] for atom in gamma_atoms})
    metal_codes = sorted({atom["comp"] for atom in metal_atoms})

    nearest_protein = []
    nearest_nonpolymer = []
    nearest_metal = []
    for gamma in gamma_atoms:
        for candidate in protein_hydroxyl_atoms:
            nearest_protein.append((distance(gamma["xyz"], candidate["xyz"]), gamma, candidate))
        for candidate in nonpolymer_oxygen_atoms:
            nearest_nonpolymer.append((distance(gamma["xyz"], candidate["xyz"]), gamma, candidate))
        for candidate in metal_atoms:
            nearest_metal.append((distance(gamma["xyz"], candidate["xyz"]), gamma, candidate))

    nearest_protein.sort(key=lambda row: row[0])
    nearest_nonpolymer.sort(key=lambda row: row[0])
    nearest_metal.sort(key=lambda row: row[0])

    nearest_product_phosphoryl_to_metal = atom_pairs(product_state_phosphoryl_atoms, metal_atoms)
    nearest_product_phosphoryl_to_product_beta = atom_pairs(
        product_state_phosphoryl_atoms, product_nucleotide_beta_atoms
    )
    nearest_product_phosphoryl_to_protein = atom_pairs(
        product_state_phosphoryl_atoms, protein_hydroxyl_atoms
    )
    nearest_product_phosphoryl_to_nonpolymer_oxygen = atom_pairs(
        product_state_phosphoryl_atoms, product_state_nonpolymer_oxygen_atoms
    )

    local_metal = [row for row in nearest_metal if row[0] <= 7.0]
    has_gamma = bool(gamma_atoms)
    has_local_metal = bool(local_metal)
    has_family_title_signal = title_has_family_signal(title, config)
    has_product_state_local_metal = (
        bool(nearest_product_phosphoryl_to_metal)
        and nearest_product_phosphoryl_to_metal[0][0] <= 7.0
    )
    product_state_control_candidate = (
        has_family_title_signal
        and bool(product_codes)
        and bool(product_state_phosphoryl_atoms)
        and has_product_state_local_metal
    )
    if product_state_control_candidate and phosphorylated_nonpolymer_codes:
        product_state_branch_status = (
            f"{config['family_id']}_phosphorylated_nonpolymer_product_control_review_only"
        )
    elif product_state_control_candidate and phosphoryl_mimic_codes:
        product_state_branch_status = (
            f"{config['family_id']}_adp_or_udp_phosphate_product_control_review_only"
        )
    elif has_family_title_signal and product_codes and phosphoryl_mimic_codes:
        product_state_branch_status = f"{config['family_id']}_product_phosphoryl_metal_gap_review_only"
    else:
        product_state_branch_status = None
    family_id = config["family_id"]
    if has_gamma and has_local_metal and has_family_title_signal:
        review_status = f"{family_id}_gamma_metal_control_candidate_review_only"
    elif has_gamma and has_family_title_signal:
        review_status = f"{family_id}_gamma_candidate_metal_gap_review_only"
    elif product_codes and has_family_title_signal:
        review_status = f"{family_id}_product_state_only_review_only"
    elif has_family_title_signal:
        review_status = f"{family_id}_no_gamma_context_review_only"
    else:
        review_status = f"outside_{family_id}_title_boundary_review_only"

    nearest_protein_distance = round(nearest_protein[0][0], 3) if nearest_protein else None
    nearest_nonpolymer_distance = round(nearest_nonpolymer[0][0], 3) if nearest_nonpolymer else None
    nearest_metal_distance = round(nearest_metal[0][0], 3) if nearest_metal else None
    nearest_product_phosphoryl_to_metal_distance = (
        round(nearest_product_phosphoryl_to_metal[0][0], 3)
        if nearest_product_phosphoryl_to_metal
        else None
    )
    nearest_product_phosphoryl_to_product_beta_distance = (
        round(nearest_product_phosphoryl_to_product_beta[0][0], 3)
        if nearest_product_phosphoryl_to_product_beta
        else None
    )
    nearest_product_phosphoryl_to_protein_hydroxyl_distance = (
        round(nearest_product_phosphoryl_to_protein[0][0], 3)
        if nearest_product_phosphoryl_to_protein
        else None
    )
    nearest_product_phosphoryl_to_nonpolymer_oxygen_distance = (
        round(nearest_product_phosphoryl_to_nonpolymer_oxygen[0][0], 3)
        if nearest_product_phosphoryl_to_nonpolymer_oxygen
        else None
    )
    weak_nearest_protein_hydroxyl_hit = (
        review_status == f"{family_id}_gamma_metal_control_candidate_review_only"
        and nearest_protein_distance is not None
        and nearest_protein_distance <= 6.0
    )
    weak_nearest_nonpolymer_oxygen_hit = (
        review_status == f"{family_id}_gamma_metal_control_candidate_review_only"
        and nearest_nonpolymer_distance is not None
        and nearest_nonpolymer_distance <= 6.0
    )
    weak_nearest_any_oxygen_hit = (
        review_status == f"{family_id}_gamma_metal_control_candidate_review_only"
        and min(
            [
                value
                for value in [nearest_protein_distance, nearest_nonpolymer_distance]
                if value is not None
            ]
            or [math.inf]
        )
        <= 6.0
    )

    return {
        "pdb_id": pdb_id,
        "fetch_status": "ok",
        "query_origins": query_origins,
        "structure_title": title,
        "family_id": family_id if has_family_title_signal else None,
        "family_name": config["family_name"] if has_family_title_signal else None,
        "review_status": review_status,
        "observed_ligand_codes": observed_ligand_codes,
        "gamma_capable_nucleotide_codes": gamma_codes,
        "product_or_partial_nucleotide_codes": product_codes,
        "phosphate_or_phosphoryl_mimic_codes": phosphoryl_mimic_codes,
        "phosphorylated_nonpolymer_ligand_codes": phosphorylated_nonpolymer_codes,
        "metal_ligand_codes": metal_codes,
        "gamma_atom_count": len(gamma_atoms),
        "metal_atom_count": len(metal_atoms),
        "product_nucleotide_beta_atom_count": len(product_nucleotide_beta_atoms),
        "product_state_phosphoryl_atom_count": len(product_state_phosphoryl_atoms),
        "product_state_phosphoryl_oxygen_atom_count": len(product_state_phosphoryl_oxygen_atoms),
        "nearest_gamma_to_metal_distance_angstrom": nearest_metal_distance,
        "nearest_gamma_to_protein_hydroxyl_distance_angstrom": nearest_protein_distance,
        "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom": nearest_nonpolymer_distance,
        "product_state_branch_status": product_state_branch_status,
        "product_state_control_candidate_review_only": product_state_control_candidate,
        "product_state_free_phosphate_control_review_only": (
            product_state_control_candidate and "PO4" in phosphoryl_mimic_codes
        ),
        "product_state_phosphorylated_nonpolymer_control_review_only": (
            product_state_control_candidate and bool(phosphorylated_nonpolymer_codes)
        ),
        "nearest_product_phosphoryl_to_metal_distance_angstrom": (
            nearest_product_phosphoryl_to_metal_distance
        ),
        "nearest_product_phosphoryl_to_product_beta_distance_angstrom": (
            nearest_product_phosphoryl_to_product_beta_distance
        ),
        "nearest_product_phosphoryl_to_protein_hydroxyl_distance_angstrom": (
            nearest_product_phosphoryl_to_protein_hydroxyl_distance
        ),
        "nearest_product_phosphoryl_to_nonpolymer_oxygen_distance_angstrom": (
            nearest_product_phosphoryl_to_nonpolymer_oxygen_distance
        ),
        "product_state_phosphoryl_to_metal_rows": compact_pair_rows(
            nearest_product_phosphoryl_to_metal,
            "phosphoryl",
            "metal",
        ),
        "product_state_phosphoryl_to_product_beta_rows": compact_pair_rows(
            nearest_product_phosphoryl_to_product_beta,
            "phosphoryl",
            "product_beta",
        ),
        "product_state_phosphoryl_to_protein_hydroxyl_rows": compact_pair_rows(
            nearest_product_phosphoryl_to_protein,
            "phosphoryl",
            "protein_hydroxyl",
        ),
        "product_state_phosphoryl_to_nonpolymer_oxygen_rows": compact_pair_rows(
            nearest_product_phosphoryl_to_nonpolymer_oxygen,
            "phosphoryl",
            "nonpolymer_oxygen",
        ),
        "nearest_protein_hydroxyl_rows": [
            {
                "gamma_ligand_code": gamma["comp"],
                "gamma_atom_name": gamma["atom"],
                **compact_atom(candidate, dist),
            }
            for dist, gamma, candidate in nearest_protein[:5]
        ],
        "nearest_nonpolymer_oxygen_rows": [
            {
                "gamma_ligand_code": gamma["comp"],
                "gamma_atom_name": gamma["atom"],
                **compact_atom(candidate, dist),
            }
            for dist, gamma, candidate in nearest_nonpolymer[:5]
        ],
        "weak_nearest_protein_hydroxyl_rule_hit_6a": weak_nearest_protein_hydroxyl_hit,
        "weak_nearest_nonpolymer_oxygen_rule_hit_6a": weak_nearest_nonpolymer_oxygen_hit,
        "weak_nearest_any_oxygen_rule_hit_6a": weak_nearest_any_oxygen_hit,
        "unified_rule_expected_blocker_source_free": (
            "nonpolymer_or_same_chain_local_oxygen_not_ePK_protein_substrate"
            if has_gamma and has_family_title_signal
            else None
        ),
        "countable_label_candidate": False,
        "production_scoring_admissible": False,
        "review_only": True,
        "epk_score_computed": False,
        "ready_for_label_import": False,
        "labels_or_fingerprints_changed": False,
    }


def build_candidate_ids(
    rows_per_query: int, max_structures: int, config: dict
) -> tuple[list[str], dict[str, list[str]], list[dict]]:
    origins: dict[str, list[str]] = defaultdict(list)
    query_records = []
    for term in config["query_terms"]:
        try:
            hits = rcsb_full_text(term, rows_per_query)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            query_records.append({"term": term, "status": f"query_failed:{type(exc).__name__}", "hits": []})
            continue
        query_records.append({"term": term, "status": "ok", "hits": hits})
        for hit in hits:
            origins[hit].append(term)
        time.sleep(0.1)
    for seed in config["seed_pdb_ids"]:
        origins[seed].append(config["prior_artifact_label"])
    ordered = []
    for seed in config["seed_pdb_ids"]:
        if seed in origins and seed not in ordered:
            ordered.append(seed)
    for record in query_records:
        for hit in record["hits"]:
            if hit not in ordered:
                ordered.append(hit)
    return ordered[:max_structures], origins, query_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--family", choices=sorted(FAMILY_CONFIGS), default="askha")
    parser.add_argument("--rows-per-query", type=int, default=8)
    parser.add_argument("--max-structures", type=int, default=32)
    args = parser.parse_args()

    config = FAMILY_CONFIGS[args.family]
    started_at = utc_now()
    candidate_ids, origins, query_records = build_candidate_ids(
        args.rows_per_query, args.max_structures, config
    )
    rows = [
        scan_structure(pdb_id, sorted(set(origins[pdb_id])), config)
        for pdb_id in candidate_ids
    ]
    controls = [
        row
        for row in rows
        if row.get("review_status")
        == f"{config['family_id']}_gamma_metal_control_candidate_review_only"
    ]
    weak_hits = [
        row
        for row in controls
        if row.get("weak_nearest_protein_hydroxyl_rule_hit_6a")
        or row.get("weak_nearest_any_oxygen_rule_hit_6a")
    ]
    weak_protein_hits = [
        row for row in controls if row.get("weak_nearest_protein_hydroxyl_rule_hit_6a")
    ]
    weak_nonpolymer_hits = [
        row for row in controls if row.get("weak_nearest_nonpolymer_oxygen_rule_hit_6a")
    ]
    distances = [
        row["nearest_gamma_to_protein_hydroxyl_distance_angstrom"]
        for row in controls
        if row.get("nearest_gamma_to_protein_hydroxyl_distance_angstrom") is not None
    ]
    product_state_rows = [
        row
        for row in rows
        if row.get("review_status") == f"{config['family_id']}_product_state_only_review_only"
    ]
    product_state_with_metal = [
        row for row in product_state_rows if row.get("metal_ligand_codes")
    ]
    product_state_with_phosphoryl_mimic = [
        row
        for row in product_state_with_metal
        if row.get("phosphate_or_phosphoryl_mimic_codes")
    ]
    product_state_branch_controls = [
        row for row in rows if row.get("product_state_control_candidate_review_only")
    ]
    product_state_free_phosphate_controls = [
        row for row in rows if row.get("product_state_free_phosphate_control_review_only")
    ]
    product_state_phosphorylated_nonpolymer_controls = [
        row
        for row in rows
        if row.get("product_state_phosphorylated_nonpolymer_control_review_only")
    ]
    status_counts = defaultdict(int)
    product_branch_status_counts = defaultdict(int)
    for row in rows:
        status_counts[row.get("review_status", "unknown")] += 1
        if row.get("product_state_branch_status"):
            product_branch_status_counts[row["product_state_branch_status"]] += 1

    artifact = {
        "metadata": {
            "method": config["method"],
            "created_at": utc_now(),
            "screen_started_at": started_at,
            "target_family_id": "epk",
            "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            "reviewed_sibling_family_id": config["family_id"],
            "reviewed_sibling_family_name": config["family_name"],
            "review_only": True,
            "production_claim_allowed": False,
            "production_scoring_admissible": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "rows_per_query": args.rows_per_query,
            "max_structures": args.max_structures,
            "candidate_structure_count": len(candidate_ids),
            "rows_reviewed": len(rows),
            f"{config['family_id']}_gamma_metal_control_count": len(controls),
            "weak_rule_counterexample_count": len(weak_hits),
            "weak_rule_counterexample_pdb_ids": [row["pdb_id"] for row in weak_hits],
            "weak_nearest_protein_hydroxyl_counterexample_count": len(weak_protein_hits),
            "weak_nearest_protein_hydroxyl_counterexample_pdb_ids": [
                row["pdb_id"] for row in weak_protein_hits
            ],
            "weak_nearest_nonpolymer_oxygen_counterexample_count": len(weak_nonpolymer_hits),
            "weak_nearest_nonpolymer_oxygen_counterexample_pdb_ids": [
                row["pdb_id"] for row in weak_nonpolymer_hits
            ],
            "product_state_only_row_count": len(product_state_rows),
            "product_state_with_metal_count": len(product_state_with_metal),
            "product_state_with_metal_pdb_ids": [
                row["pdb_id"] for row in product_state_with_metal
            ],
            "product_state_with_phosphoryl_mimic_count": len(product_state_with_phosphoryl_mimic),
            "product_state_with_phosphoryl_mimic_pdb_ids": [
                row["pdb_id"] for row in product_state_with_phosphoryl_mimic
            ],
            "product_state_branch_control_count": len(product_state_branch_controls),
            "product_state_branch_control_pdb_ids": [
                row["pdb_id"] for row in product_state_branch_controls
            ],
            "product_state_free_phosphate_control_count": len(product_state_free_phosphate_controls),
            "product_state_free_phosphate_control_pdb_ids": [
                row["pdb_id"] for row in product_state_free_phosphate_controls
            ],
            "product_state_phosphorylated_nonpolymer_control_count": len(
                product_state_phosphorylated_nonpolymer_controls
            ),
            "product_state_phosphorylated_nonpolymer_control_pdb_ids": [
                row["pdb_id"] for row in product_state_phosphorylated_nonpolymer_controls
            ],
            "review_status_counts": dict(sorted(status_counts.items())),
            "product_state_branch_status_counts": dict(sorted(product_branch_status_counts.items())),
            "nearest_protein_hydroxyl_min_angstrom": min(distances) if distances else None,
            "nearest_protein_hydroxyl_max_angstrom": max(distances) if distances else None,
            "primary_outcome": "counterexample_found" if weak_hits else "next_query_defined",
            "search_surface": (
                f"RCSB full_text bounded {config['family_id']} terms plus prior graph-linked seeds; "
                "candidate rows accepted only by in-memory mmCIF gamma-capable nucleotide, local Mg/Mn, "
                "and compact source-free local oxygen measurements"
            ),
            "query_terms": config["query_terms"],
            "seed_pdb_ids": config["seed_pdb_ids"],
            "candidate_pdb_ids": candidate_ids,
            "source_prior_artifacts": [
                "artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json",
                "artifacts/v3_epk_negative_control_gamma_distance_distribution_1025.json",
                "artifacts/v3_epk_sibling_negative_control_alternate_structure_plan_1025.json",
                "artifacts/v3_epk_sibling_negative_control_alternate_gamma_distance_sample_1025.json",
                "artifacts/v3_epk_unified_review_only_scoring_prototype_1025.json",
                "artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json",
                "artifacts/v3_epk_precount_gate_status_1025.json",
            ],
            "next_query": config["next_query"],
        },
        "query_records": query_records,
        "control_rows": controls,
        "rows": rows,
        "warnings": [
            "Review-only sibling-control evidence; not a calibrated ePK score, production threshold, registry edit, label import, or external hard-negative re-audit.",
            f"{config['family_id']} title/query terms route the candidate search, but control acceptance and weak-rule stress use only compact mmCIF-derived local ligand/coordinate evidence.",
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
