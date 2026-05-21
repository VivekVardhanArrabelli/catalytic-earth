#!/usr/bin/env python3
"""Stress source-valid ePK seed and geometry-prefiltered non-ePK controls.

This lane helper follows the source-valid seed query from the false-positive
hunter handoff. It uses full-text/component search only to collect a bounded
candidate pool, then requires polymer/entity evidence for the ePK seed buckets.
For non-ePK contaminants it prefilters v4 contexts by local gamma-to-acceptor
geometry before invoking the review-only materializer.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import shlex
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import auth_namespace_edge_case_stress as ns
import orc_mcm_multisite_guard_stress as orc
import v4_entry_level_assembly_guard_stress as entry_guard
import v4_high_order_epk_atpase_overblock_stress as high_order


LANE_ID = "epk_false_positive_hunter"
DISTANCE_CUTOFF_ANGSTROM = 6.0
MG_DISTANCE_CUTOFF_ANGSTROM = 4.5
MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID = 25
MATERIALIZER_GAMMA_CODES = {"ACP", "ANP", "ATP", "DTP"}
ACCEPTOR_ATOMS = {"SER": "OG", "THR": "OG1", "TYR": "OH"}
REGRESSION_GATE_PATH = Path(
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "epk_candidate_evidence_v1_regression_gate_20260521_033057Z.json"
)
PRIOR_CONTAMINANT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_false_positive_hunter/"
    "v4_entry_level_epk_overblock_later_offset_contaminant_stress_20260521_030753Z.json"
)

EPK_ENTITY_SEED_QUERIES = [
    {"name": "raf_mek_atp", "phrase": "RAF MEK", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "raf_mek_anp", "phrase": "RAF MEK", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "braf_mek_atp", "phrase": "BRAF MEK", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "braf_mek_anp", "phrase": "BRAF MEK", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "mek_erk_atp", "phrase": "MEK ERK", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "mek_erk_anp", "phrase": "MEK ERK", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "jnk_atp", "phrase": "JNK kinase", "ligand": "ATP", "start": 0, "rows": 40},
    {"name": "jnk_anp", "phrase": "JNK kinase", "ligand": "ANP", "start": 0, "rows": 40},
    {"name": "c_jun_n_terminal_kinase_atp", "phrase": "c-Jun N-terminal kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "cdk_cyclin_atp", "phrase": "CDK cyclin", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "cdk_cyclin_anp", "phrase": "CDK cyclin", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "cyclin_dependent_kinase_cyclin_atp", "phrase": "cyclin-dependent kinase cyclin", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "receptor_tyrosine_kinase_dimer_atp", "phrase": "receptor tyrosine kinase dimer", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "receptor_tyrosine_kinase_dimer_anp", "phrase": "receptor tyrosine kinase dimer", "ligand": "ANP", "start": 0, "rows": 45},
    {"name": "egfr_kinase_dimer_atp", "phrase": "EGFR kinase dimer", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "insulin_receptor_kinase_atp", "phrase": "insulin receptor kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "insulin_receptor_kinase_anp", "phrase": "insulin receptor kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mtor_kinase_atp", "phrase": "mTOR kinase", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtor_kinase_anp", "phrase": "mTOR kinase", "ligand": "ANP", "start": 0, "rows": 35},
    {"name": "mtorc1_atp", "phrase": "mTORC1", "ligand": "ATP", "start": 0, "rows": 35},
    {"name": "mtorc2_atp", "phrase": "mTORC2", "ligand": "ATP", "start": 0, "rows": 35},
]

NON_EPK_CONTAMINANT_QUERIES = [
    {"name": "protein_kinase_peptide_atp_300", "phrase": "protein kinase peptide", "ligand": "ATP", "start": 300, "rows": 45},
    {"name": "protein_kinase_peptide_anp_150", "phrase": "protein kinase peptide", "ligand": "ANP", "start": 150, "rows": 45},
    {"name": "substrate_peptide_kinase_atp_160", "phrase": "substrate peptide kinase", "ligand": "ATP", "start": 160, "rows": 45},
    {"name": "map_kinase_substrate_peptide_atp_40", "phrase": "MAP kinase substrate peptide", "ligand": "ATP", "start": 40, "rows": 45},
    {"name": "aaa_atpase_tyrosine_atp", "phrase": "AAA+ ATPase tyrosine", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "abc_transporter_tyrosine_atp", "phrase": "ABC transporter tyrosine ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "helicase_tyrosine_atp", "phrase": "helicase tyrosine ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "dynein_tyrosine_atp", "phrase": "dynein tyrosine ATP", "ligand": "ATP", "start": 0, "rows": 45},
    {"name": "vcp_p97_tyrosine_atp", "phrase": "VCP p97 tyrosine ATP", "ligand": "ATP", "start": 0, "rows": 35},
]

KINASE_ENTITY_TOKENS = [
    "protein kinase",
    "tyrosine kinase",
    "serine/threonine-protein kinase",
    "serine/threonine protein kinase",
    "cyclin-dependent kinase",
    "mitogen-activated protein kinase",
    "map kinase",
    "raf kinase",
    "receptor tyrosine kinase",
    "mechanistic target of rapamycin",
    "mtor",
]


def now_utc() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def add_id(
    ordered: list[str],
    id_to_queries: dict[str, list[str]],
    pdb_id: str,
    query_name: str,
) -> None:
    normalized = str(pdb_id).upper()
    id_to_queries[normalized].append(query_name)
    if normalized not in ordered:
        ordered.append(normalized)


def load_prior_contaminant_ids(repo_root: Path) -> list[str]:
    path = repo_root / PRIOR_CONTAMINANT_ARTIFACT
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    ids = []
    for row in payload.get("entry_review_rows", []) or []:
        if row.get("epk_query_non_epk_v4_contaminant_review_only"):
            pdb_id = str(row.get("pdb_id") or "").upper()
            if pdb_id and pdb_id not in ids:
                ids.append(pdb_id)
    return ids


def collect_ids(
    repo_root: Path,
    *,
    max_unique_ids: int,
    epk_quota: int,
    contaminant_quota: int,
) -> tuple[list[str], dict[str, list[str]], dict[str, str], dict[str, int]]:
    ordered: list[str] = []
    id_to_queries: dict[str, list[str]] = defaultdict(list)
    query_errors: dict[str, str] = {}
    query_counts: dict[str, int] = {}
    surface_ids: dict[str, list[str]] = {
        "epk_entity_seed_text": [],
        "non_epk_contaminant_text": [],
    }

    fixed_ids = sorted(
        high_order.PRIOR_KNOWN_EPK_POSITIVE_IDS
        | high_order.PRIOR_ORC_COUNTEREXAMPLE_IDS
        | high_order.PRESSURE_IDS
    )
    for pdb_id in fixed_ids:
        add_id(ordered, id_to_queries, pdb_id, "fixed_prior_positive_counterexample_or_pressure")

    for pdb_id in load_prior_contaminant_ids(repo_root):
        add_id(
            surface_ids["non_epk_contaminant_text"],
            id_to_queries,
            pdb_id,
            "prior_epk_query_non_epk_v4_contaminant_seed",
        )
    query_counts["prior_epk_query_non_epk_v4_contaminant_seed"] = len(
        surface_ids["non_epk_contaminant_text"]
    )

    for surface, queries in [
        ("epk_entity_seed_text", EPK_ENTITY_SEED_QUERIES),
        ("non_epk_contaminant_text", NON_EPK_CONTAMINANT_QUERIES),
    ]:
        for query in queries:
            name = str(query["name"])
            try:
                ids = entry_guard.component_full_text_query(query)
                query_counts[f"{surface}:{name}"] = len(ids)
            except Exception as exc:  # pragma: no cover - network evidence
                ids = []
                query_counts[f"{surface}:{name}"] = 0
                query_errors[f"{surface}:{name}"] = repr(exc)
            for pdb_id in ids:
                add_id(
                    surface_ids[surface],
                    id_to_queries,
                    pdb_id,
                    f"{surface}:{name}:{query['phrase']}:{query['ligand']}:start_{query['start']}",
                )
            time.sleep(0.12)

    for pdb_id in surface_ids["epk_entity_seed_text"][:epk_quota]:
        add_id(ordered, id_to_queries, pdb_id, "selected_epk_entity_seed_surface")
    for pdb_id in surface_ids["non_epk_contaminant_text"][:contaminant_quota]:
        add_id(ordered, id_to_queries, pdb_id, "selected_non_epk_contaminant_surface")

    query_counts["fixed_control_ids"] = len(fixed_ids)
    query_counts["epk_entity_seed_unique_ids_available"] = len(
        surface_ids["epk_entity_seed_text"]
    )
    query_counts["epk_entity_seed_selected_quota"] = epk_quota
    query_counts["non_epk_contaminant_unique_ids_available"] = len(
        surface_ids["non_epk_contaminant_text"]
    )
    query_counts["non_epk_contaminant_selected_quota"] = contaminant_quota
    return ordered[:max_unique_ids], id_to_queries, query_errors, query_counts


def mmcif_loop_rows(cif_text: str, prefix: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [line.rstrip("\n") for line in cif_text.splitlines()]
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        index += 1
        tags: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("_"):
            tags.append(lines[index].strip())
            index += 1
        if not tags or not all(tag.startswith(prefix) for tag in tags):
            continue
        while index < len(lines):
            line = lines[index].strip()
            if not line or line == "#":
                break
            if line == "loop_" or line.startswith("_") or line.startswith("data_"):
                break
            try:
                values = shlex.split(line)
            except ValueError:
                values = line.split()
            if len(values) >= len(tags):
                rows.append(
                    {
                        tag.removeprefix(prefix): values[pos]
                        for pos, tag in enumerate(tags)
                        if pos < len(values)
                    }
                )
            index += 1
    return rows


def compact_entity_rows(cif_text: str) -> list[dict[str, str]]:
    entity_rows = mmcif_loop_rows(cif_text, "_entity.")
    compact = []
    for row in entity_rows:
        description = row.get("pdbx_description")
        if description in {None, "", ".", "?"}:
            continue
        compact.append(
            {
                "entity_id": str(row.get("id") or ""),
                "type": str(row.get("type") or ""),
                "description": str(description),
            }
        )
    return compact


def compact_chain_accessions(cif_text: str) -> dict[str, list[str]]:
    accessions: dict[str, list[str]] = defaultdict(list)
    for row in mmcif_loop_rows(cif_text, "_struct_ref_seq."):
        accession = str(row.get("pdbx_db_accession") or "")
        strand_ids = str(row.get("pdbx_strand_id") or "")
        if accession in {"", ".", "?"}:
            continue
        for chain_id in [part.strip() for part in strand_ids.split(",")]:
            if chain_id and accession not in accessions[chain_id]:
                accessions[chain_id].append(accession)
    return {chain: sorted(values) for chain, values in sorted(accessions.items())}


def family_buckets_from_entities(entity_rows: list[dict[str, str]]) -> list[str]:
    entity_text = " ".join(row["description"] for row in entity_rows).lower()
    buckets = []
    has_raf = any(token in entity_text for token in ["braf", "craf", "raf1", "raf kinase"])
    has_mek = any(
        token in entity_text
        for token in ["mek", "map2k", "mitogen-activated protein kinase kinase"]
    )
    has_erk = any(token in entity_text for token in ["erk", "mapk1", "mapk3"])
    if has_raf and (has_mek or has_erk):
        buckets.append("raf_mek_erk_entity")
    if has_mek and has_erk:
        buckets.append("mek_erk_entity")
    if any(
        token in entity_text
        for token in ["jnk", "c-jun n-terminal kinase", "mapk8", "mapk9", "mapk10"]
    ):
        buckets.append("jnk_entity")
    if ("cyclin-dependent kinase" in entity_text or "cdk" in entity_text) and (
        "cyclin" in entity_text
    ):
        buckets.append("cdk_cyclin_entity")
    if any(
        token in entity_text
        for token in [
            "receptor tyrosine kinase",
            "insulin receptor",
            "epidermal growth factor receptor",
            "egfr",
            "fgfr",
            "vegfr",
            "pdgfr",
            "proto-oncogene tyrosine-protein kinase kit",
            "hepatocyte growth factor receptor",
        ]
    ):
        buckets.append("receptor_tyrosine_kinase_entity")
    if any(
        token in entity_text
        for token in [
            "mechanistic target of rapamycin",
            "mammalian target of rapamycin",
            "mtor",
            "raptor",
            "rictor",
        ]
    ):
        buckets.append("mtorc_entity")
    return sorted(set(buckets))


def kinase_tokens_from_entities(entity_rows: list[dict[str, str]]) -> list[str]:
    entity_text = " ".join(row["description"] for row in entity_rows).lower()
    return sorted(token for token in KINASE_ENTITY_TOKENS if token in entity_text)


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper().replace('"', "")


def preferred_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def preferred_seq_id(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_seq_id") or atom.get("label_seq_id") or "")


def distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    return math.sqrt(
        (float(left["Cartn_x"]) - float(right["Cartn_x"])) ** 2
        + (float(left["Cartn_y"]) - float(right["Cartn_y"])) ** 2
        + (float(left["Cartn_z"]) - float(right["Cartn_z"])) ** 2
    )


def local_substrate_geometry(cif_text: str) -> dict[str, Any]:
    atoms, parse_meta = ns.parse_atom_site_raw(cif_text)
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and (atom_code(atom) == "MG" or str(atom.get("type_symbol") or "").upper() == "MG")
    ]
    gamma_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom.get("type_symbol") == "P"
        and atom_code(atom) in MATERIALIZER_GAMMA_CODES
        and atom_name(atom) == "PG"
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "ATOM"
        and ACCEPTOR_ATOMS.get(atom_code(atom)) == atom_name(atom)
    ]
    hits: list[dict[str, Any]] = []
    chain_pairs: list[tuple[str, str]] = []
    for gamma_atom in gamma_atoms:
        mg_distances = [distance(gamma_atom, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        for acceptor in acceptor_atoms:
            d = distance(gamma_atom, acceptor)
            if d > DISTANCE_CUTOFF_ANGSTROM:
                continue
            residue = atom_code(acceptor)
            seq_id = ns.optional_int(preferred_seq_id(acceptor))
            tyrosine = residue == "TYR"
            n_terminal = bool(
                residue in ACCEPTOR_ATOMS
                and seq_id is not None
                and seq_id <= MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
            )
            if not (tyrosine or n_terminal):
                continue
            candidate_chain = preferred_chain(acceptor)
            gamma_chain = preferred_chain(gamma_atom)
            if candidate_chain and gamma_chain:
                chain_pairs.append((candidate_chain, gamma_chain))
            hits.append(
                {
                    "candidate_chain_name": candidate_chain,
                    "candidate_auth_seq_id": preferred_seq_id(acceptor),
                    "candidate_residue_code": residue,
                    "candidate_atom_name": atom_name(acceptor),
                    "candidate_label_entity_id": acceptor.get("label_entity_id"),
                    "gamma_associated_polymer_chain_name": gamma_chain,
                    "gamma_label_entity_id": gamma_atom.get("label_entity_id"),
                    "gamma_ligand_code": atom_code(gamma_atom),
                    "gamma_atom_name": atom_name(gamma_atom),
                    "nearest_gamma_distance_angstrom": round(d, 3),
                    "nearest_mg_distance_angstrom": (
                        round(nearest_mg, 3) if nearest_mg is not None else None
                    ),
                    "tyrosine_acceptor": tyrosine,
                    "n_terminal_acceptor": n_terminal,
                    "near_mg": bool(
                        nearest_mg is not None
                        and nearest_mg <= MG_DISTANCE_CUTOFF_ANGSTROM
                    ),
                }
            )
    same_chain = any(candidate == gamma for candidate, gamma in chain_pairs)
    reciprocal = any(
        left_candidate == right_gamma
        and left_gamma == right_candidate
        and left_candidate != left_gamma
        for index, (left_candidate, left_gamma) in enumerate(chain_pairs)
        for right_candidate, right_gamma in chain_pairs[index + 1 :]
    )
    hits.sort(
        key=lambda hit: (
            0 if hit["tyrosine_acceptor"] else 1,
            0 if hit["near_mg"] else 1,
            float(hit["nearest_gamma_distance_angstrom"]),
        )
    )
    return {
        "parse_meta": parse_meta,
        "local_gamma_acceptor_substrate_geometry_hit_count": len(hits),
        "local_gamma_acceptor_substrate_geometry_topology_clear": bool(
            hits and not (same_chain or reciprocal)
        ),
        "local_same_chain_topology_detected": same_chain,
        "local_reciprocal_cross_chain_topology_detected": reciprocal,
        "local_geometry_hits": hits[:8],
    }


def load_regression_gate(repo_root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    path = repo_root / REGRESSION_GATE_PATH
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    lookup: dict[tuple[str, str], dict[str, Any]] = {}
    for row in payload.get("rows", []) or []:
        pdb_id = str(row.get("pdb_id") or "").upper()
        context = str(row.get("coordinate_context") or "deposited_atom_site")
        if pdb_id:
            lookup[(pdb_id, context)] = row
    return lookup


def annotate_entry(
    entry: dict[str, Any],
    context_rows: list[dict[str, Any]],
    deposited_cif: str,
) -> dict[str, Any]:
    entity_rows = compact_entity_rows(deposited_cif)
    if not entity_rows:
        entity_rows = [
            {
                "entity_id": "",
                "type": "polymer_or_nonpolymer_from_existing_parser",
                "description": str(description),
            }
            for description in entry.get("entity_descriptions_compact", [])
            if str(description)
        ]
    chain_accessions = compact_chain_accessions(deposited_cif)
    family_buckets = family_buckets_from_entities(entity_rows)
    kinase_tokens = kinase_tokens_from_entities(entity_rows)
    context_groups = set(entry.get("query_names", []))
    source_seed_surface = any("epk_entity_seed_text:" in value for value in context_groups)
    contaminant_surface = any(
        "non_epk_contaminant_text:" in value
        or value == "prior_epk_query_non_epk_v4_contaminant_seed"
        for value in context_groups
    )
    any_context_v4 = bool(
        entry.get("entry_level_any_context_v4_guard_hit_review_only")
        or any(row.get("v4_oligomeric_atp_terminals_no_mg_required_hit") for row in context_rows)
    )
    source_seed = bool(
        source_seed_surface
        and any_context_v4
        and family_buckets
        and entry.get("probable_epk_from_context")
    )
    non_epk_contaminant = bool(
        contaminant_surface
        and any_context_v4
        and not source_seed
        and not entry.get("probable_epk_from_context")
        and not entry.get("deposited_orc_mcm_role_tokens")
    )
    annotated = dict(entry)
    annotated.update(
        {
            "polymer_entity_evidence": {
                "entity_rows_compact": entity_rows[:18],
                "chain_accessions_compact": chain_accessions,
                "kinase_entity_tokens": kinase_tokens,
                "family_buckets_from_entities": family_buckets,
            },
            "source_valid_epk_seed_review_candidate": source_seed,
            "source_valid_epk_seed_family_buckets": family_buckets,
            "non_epk_v4_contaminant_prefilter_candidate": non_epk_contaminant,
        }
    )
    return annotated


def context_selection_priority(selected: dict[str, Any]) -> tuple[int, str, str]:
    entry = selected["entry_row"]
    context = selected["context_row"]
    source_seed = bool(entry.get("source_valid_epk_seed_review_candidate"))
    non_epk = bool(entry.get("non_epk_v4_contaminant_prefilter_candidate"))
    assembly = context["coordinate_context"] != "deposited_atom_site"
    context_v4 = bool(context.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))
    local_geom = bool(
        context.get("local_substrate_geometry", {}).get(
            "local_gamma_acceptor_substrate_geometry_hit_count"
        )
    )
    if source_seed and assembly and context_v4:
        priority = 0
    elif source_seed and context_v4:
        priority = 1
    elif source_seed and assembly:
        priority = 2
    elif source_seed:
        priority = 3
    elif non_epk and context_v4 and local_geom:
        priority = 4
    elif non_epk and local_geom:
        priority = 5
    elif entry.get("known_orc_counterexample_input"):
        priority = 6
    elif entry.get("known_epk_positive_input"):
        priority = 7
    else:
        priority = 8
    return priority, str(entry["pdb_id"]), str(context["coordinate_context"])


def select_contexts(
    entry_rows: list[dict[str, Any]],
    context_rows_by_pdb: dict[str, list[dict[str, Any]]],
    *,
    max_materializer_contexts: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for entry in entry_rows:
        contexts = context_rows_by_pdb.get(entry["pdb_id"], [])
        source_seed = bool(entry.get("source_valid_epk_seed_review_candidate"))
        non_epk = bool(entry.get("non_epk_v4_contaminant_prefilter_candidate"))
        fixed_control = bool(
            entry.get("known_epk_positive_input") or entry.get("known_orc_counterexample_input")
        )
        if source_seed:
            for context in contexts:
                selected.append({"entry_row": entry, "context_row": context})
        elif non_epk:
            for context in contexts:
                geometry = context.get("local_substrate_geometry", {})
                if (
                    context.get("v4_oligomeric_atp_terminals_no_mg_required_hit")
                    and int(geometry.get("local_gamma_acceptor_substrate_geometry_hit_count") or 0) > 0
                ):
                    selected.append({"entry_row": entry, "context_row": context})
        elif fixed_control:
            for context in contexts:
                if context.get("v4_oligomeric_atp_terminals_no_mg_required_hit"):
                    selected.append({"entry_row": entry, "context_row": context})
                elif entry.get("known_orc_counterexample_input") and context.get(
                    "deposited_v4_context_below_chain_floor"
                ):
                    selected.append({"entry_row": entry, "context_row": context})

    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for row in selected:
        key = (row["entry_row"]["pdb_id"], row["context_row"]["coordinate_context"])
        unique.setdefault(key, row)
    return sorted(unique.values(), key=context_selection_priority)[:max_materializer_contexts]


def materializer_decision(
    repo_root: Path,
    started_at: str,
    entry: dict[str, Any],
    context_row: dict[str, Any],
    cif_text: str,
    regression_gate_lookup: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    row = entry_guard.materializer_context_summary(
        repo_root=repo_root,
        started_at=started_at,
        entry=entry,
        context_row=context_row,
        cif_text=cif_text,
    )
    pdb_id = str(entry["pdb_id"]).upper()
    context = str(context_row["coordinate_context"])
    gate_row = regression_gate_lookup.get((pdb_id, context))
    topology_clear = bool(row.get("topology_clear_substrate_mode_hit"))
    substrate_hit_count = int(row.get("substrate_mode_materializer_hit_count") or 0)
    source_seed = bool(entry.get("source_valid_epk_seed_review_candidate"))
    non_epk = bool(entry.get("non_epk_v4_contaminant_prefilter_candidate"))
    context_v4 = bool(context_row.get("v4_oligomeric_atp_terminals_no_mg_required_hit"))
    entry_guard_hit = bool(entry.get("entry_level_any_context_v4_guard_hit_review_only"))
    topology_ambiguous = bool(row.get("topology_ambiguity_counteraxis_hit"))

    if source_seed and topology_clear and entry_guard_hit:
        decision = "source_valid_epk_seed_overblock_risk_by_entry_level_guard_review_only"
    elif source_seed and topology_clear:
        decision = "source_valid_epk_seed_materializer_hit_retained_review_only"
    elif source_seed and substrate_hit_count and topology_ambiguous:
        decision = "source_valid_epk_seed_hit_existing_topology_blocked_review_only"
    elif source_seed:
        decision = "source_valid_epk_seed_no_substrate_mode_materializer_hit_review_only"
    elif non_epk and topology_clear and context_v4:
        decision = "geometry_prefiltered_non_epk_counterexample_blocked_by_context_v4_review_only"
    elif non_epk and topology_clear and entry_guard_hit:
        decision = "geometry_prefiltered_non_epk_counterexample_closed_by_entry_level_guard_review_only"
    elif non_epk and topology_clear:
        decision = "geometry_prefiltered_non_epk_counterexample_residual_review_only"
    elif non_epk and substrate_hit_count and topology_ambiguous:
        decision = "geometry_prefiltered_non_epk_hit_existing_topology_blocked_review_only"
    elif non_epk:
        decision = "geometry_prefiltered_non_epk_no_materializer_hit_after_prefilter_review_only"
    else:
        decision = str(row.get("entry_level_guard_stress_decision") or "fixed_control_context_review_only")

    row.update(
        {
            "source_valid_epk_seed_review_candidate": source_seed,
            "source_valid_epk_seed_family_buckets": entry.get(
                "source_valid_epk_seed_family_buckets", []
            ),
            "polymer_entity_evidence": entry.get("polymer_entity_evidence", {}),
            "non_epk_v4_contaminant_prefilter_candidate": non_epk,
            "local_substrate_geometry": context_row.get("local_substrate_geometry", {}),
            "regression_gate_joined": bool(gate_row),
            "regression_gate_control_class": (
                gate_row.get("control_class") if isinstance(gate_row, dict) else None
            ),
            "regression_gate_expected_policy_decision": (
                gate_row.get("expected_policy_decision") if isinstance(gate_row, dict) else None
            ),
            "regression_gate_guard_blocker_class": (
                gate_row.get("guard_blocker_class") if isinstance(gate_row, dict) else None
            ),
            "source_valid_geometry_prefilter_stress_decision": decision,
            "unsafe_nonabstention_after_expected_policy": bool(
                decision == "geometry_prefiltered_non_epk_counterexample_residual_review_only"
            ),
        }
    )
    return row


def compact_ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(row["pdb_id"]) for row in rows if row.get(key))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-unique-ids", type=int, default=360)
    parser.add_argument("--epk-quota", type=int, default=220)
    parser.add_argument("--contaminant-quota", type=int, default=120)
    parser.add_argument("--max-materializer-contexts", type=int, default=240)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ordered_ids, id_to_queries, query_errors, query_counts = collect_ids(
        repo_root,
        max_unique_ids=args.max_unique_ids,
        epk_quota=args.epk_quota,
        contaminant_quota=args.contaminant_quota,
    )
    regression_gate_lookup = load_regression_gate(repo_root)

    entry_rows: list[dict[str, Any]] = []
    context_rows_by_pdb: dict[str, list[dict[str, Any]]] = {}
    cif_text_by_pdb_context: dict[tuple[str, str], str] = {}
    fetch_errors: dict[str, str] = {}

    for index, pdb_id in enumerate(ordered_ids, start=1):
        try:
            entry_row, context_rows, cif_by_context = entry_guard.fetch_entry_contexts(
                pdb_id,
                index,
                id_to_queries.get(pdb_id, []),
            )
            for context_row in context_rows:
                context = context_row["coordinate_context"]
                geometry = local_substrate_geometry(cif_by_context[context])
                context_row["local_substrate_geometry"] = geometry
                context_row["regression_gate_fixture_joined"] = bool(
                    regression_gate_lookup.get((pdb_id, context))
                )
            annotated = annotate_entry(
                entry_row,
                context_rows,
                cif_by_context["deposited_atom_site"],
            )
            entry_rows.append(annotated)
            context_rows_by_pdb[pdb_id] = context_rows
            for context, cif_text in cif_by_context.items():
                cif_text_by_pdb_context[(pdb_id, context)] = cif_text
        except Exception as exc:  # pragma: no cover - network evidence
            fetch_errors[pdb_id] = repr(exc)
        if index % 20 == 0:
            print(
                json.dumps(
                    {
                        "progress_entries_reviewed": len(entry_rows),
                        "progress_fetch_errors": len(fetch_errors),
                        "last_index": index,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        time.sleep(0.05)

    selected_contexts = select_contexts(
        entry_rows,
        context_rows_by_pdb,
        max_materializer_contexts=args.max_materializer_contexts,
    )
    materializer_rows: list[dict[str, Any]] = []
    materializer_context_errors: dict[str, str] = {}
    for index, selected in enumerate(selected_contexts, start=1):
        entry = selected["entry_row"]
        context_row = selected["context_row"]
        key = (entry["pdb_id"], context_row["coordinate_context"])
        try:
            materializer_rows.append(
                materializer_decision(
                    repo_root,
                    args.started_at,
                    entry,
                    context_row,
                    cif_text_by_pdb_context[key],
                    regression_gate_lookup,
                )
            )
        except Exception as exc:  # pragma: no cover - network evidence
            materializer_context_errors[f"{key[0]}:{key[1]}"] = repr(exc)
        if index % 25 == 0:
            print(
                json.dumps(
                    {
                        "progress_materializer_contexts": index,
                        "progress_materializer_errors": len(materializer_context_errors),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        time.sleep(0.03)

    context_rows = [row for rows in context_rows_by_pdb.values() for row in rows]
    source_seed_rows = [
        row for row in entry_rows if row.get("source_valid_epk_seed_review_candidate")
    ]
    contaminant_rows = [
        row for row in entry_rows if row.get("non_epk_v4_contaminant_prefilter_candidate")
    ]
    geometry_prefilter_context_rows = [
        row
        for row in context_rows
        if int(
            row.get("local_substrate_geometry", {}).get(
                "local_gamma_acceptor_substrate_geometry_hit_count"
            )
            or 0
        )
        > 0
    ]
    non_epk_materialized_rows = [
        row
        for row in materializer_rows
        if row.get("non_epk_v4_contaminant_prefilter_candidate")
    ]
    source_epk_materialized_rows = [
        row for row in materializer_rows if row.get("source_valid_epk_seed_review_candidate")
    ]
    overblock_rows = [
        row
        for row in materializer_rows
        if row.get("source_valid_geometry_prefilter_stress_decision")
        == "source_valid_epk_seed_overblock_risk_by_entry_level_guard_review_only"
    ]
    residual_rows = [
        row
        for row in materializer_rows
        if row.get("source_valid_geometry_prefilter_stress_decision")
        == "geometry_prefiltered_non_epk_counterexample_residual_review_only"
    ]
    blocked_rows = [
        row
        for row in materializer_rows
        if row.get("source_valid_geometry_prefilter_stress_decision")
        in {
            "geometry_prefiltered_non_epk_counterexample_blocked_by_context_v4_review_only",
            "geometry_prefiltered_non_epk_counterexample_closed_by_entry_level_guard_review_only",
        }
    ]
    decision_counts = Counter(
        str(row.get("source_valid_geometry_prefilter_stress_decision") or "")
        for row in materializer_rows
    )
    ended_at = now_utc()
    output = {
        "metadata": {
            "lane_id": LANE_ID,
            "started_at": args.started_at,
            "ended_at": ended_at,
            "method": "source_valid_epk_seed_geometry_prefilter_stress",
            "rule_under_attack": (
                "entry-level any-context v4 guard overblock risk on polymer/entity "
                "classified ePK ATP/ANP assemblies plus unsafe materializer "
                "non-abstention on geometry-prefiltered non-ePK v4 contaminants"
            ),
            "query_surface": {
                "epk_entity_seed_queries": EPK_ENTITY_SEED_QUERIES,
                "non_epk_contaminant_queries": NON_EPK_CONTAMINANT_QUERIES,
                "prior_contaminant_artifact": str(PRIOR_CONTAMINANT_ARTIFACT),
                "regression_gate_artifact": str(REGRESSION_GATE_PATH),
                "max_unique_ids": args.max_unique_ids,
                "epk_quota": args.epk_quota,
                "contaminant_quota": args.contaminant_quota,
                "max_assemblies_per_entry": entry_guard.MAX_ASSEMBLIES_PER_ENTRY,
                "max_materializer_contexts": args.max_materializer_contexts,
                "candidate_threshold_angstrom": DISTANCE_CUTOFF_ANGSTROM,
                "max_n_terminal_acceptor_auth_seq_id": MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
            },
            "query_result_counts": query_counts,
            "query_errors": query_errors,
            "unique_pdb_ids_review_surface_count": len(ordered_ids),
            "entry_rows_reviewed": len(entry_rows),
            "coordinate_context_rows_reviewed": len(context_rows),
            "fetch_error_count": len(fetch_errors),
            "source_valid_epk_seed_entry_count": len(source_seed_rows),
            "source_valid_epk_seed_pdb_ids": compact_ids(
                source_seed_rows, "source_valid_epk_seed_review_candidate"
            ),
            "source_valid_epk_family_bucket_counts": dict(
                sorted(
                    Counter(
                        bucket
                        for row in source_seed_rows
                        for bucket in row.get("source_valid_epk_seed_family_buckets", [])
                    ).items()
                )
            ),
            "non_epk_v4_contaminant_prefilter_entry_count": len(contaminant_rows),
            "non_epk_v4_contaminant_prefilter_pdb_ids": compact_ids(
                contaminant_rows, "non_epk_v4_contaminant_prefilter_candidate"
            ),
            "local_geometry_prefilter_context_count": len(geometry_prefilter_context_rows),
            "materializer_context_input_count": len(selected_contexts),
            "materializer_context_error_count": len(materializer_context_errors),
            "materialized_source_valid_epk_context_count": len(source_epk_materialized_rows),
            "materialized_non_epk_prefiltered_context_count": len(non_epk_materialized_rows),
            "source_valid_epk_entry_level_overblock_risk_count": len(overblock_rows),
            "source_valid_epk_entry_level_overblock_risk_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}" for row in overblock_rows
            ),
            "geometry_prefiltered_non_epk_blocked_counterexample_count": len(blocked_rows),
            "geometry_prefiltered_non_epk_blocked_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}" for row in blocked_rows
            ),
            "geometry_prefiltered_non_epk_residual_counterexample_count": len(
                residual_rows
            ),
            "geometry_prefiltered_non_epk_residual_counterexample_pdb_contexts": sorted(
                f"{row['pdb_id']}:{row['coordinate_context']}" for row in residual_rows
            ),
            "unsafe_nonabstention_count": len(residual_rows),
            "regression_gate_joined_materializer_row_count": sum(
                1 for row in materializer_rows if row.get("regression_gate_joined")
            ),
            "custom_stress_decision_counts": dict(sorted(decision_counts.items())),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "ready_for_label_import": False,
            "ready_for_production_scoring": False,
            "epk_score_computed": False,
            "external_hard_negative_reaudit_scored": False,
        },
        "fetch_errors": fetch_errors,
        "materializer_context_errors": materializer_context_errors,
        "entry_review_rows": entry_rows,
        "coordinate_context_review_rows": context_rows,
        "selected_materializer_context_rows": [
            {
                "pdb_id": selected["entry_row"]["pdb_id"],
                "coordinate_context": selected["context_row"]["coordinate_context"],
                "context_priority": context_selection_priority(selected)[0],
            }
            for selected in selected_contexts
        ],
        "custom_materializer_rows": materializer_rows,
        "source_valid_epk_entry_level_overblock_risk_rows": overblock_rows,
        "geometry_prefiltered_non_epk_blocked_counterexample_rows": blocked_rows,
        "geometry_prefiltered_non_epk_residual_counterexample_rows": residual_rows,
        "warnings": [
            "Review-only lane artifact; no production labels, thresholds, registries, fingerprints, migrations, or scoring.",
            "Search terms collect candidate pools only; ePK seed status requires polymer/entity evidence in the deposited mmCIF.",
            "Non-ePK v4 contaminants are materialized only after compact local gamma-to-acceptor geometry prefiltering.",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
