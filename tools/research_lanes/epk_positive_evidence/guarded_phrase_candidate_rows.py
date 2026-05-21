#!/usr/bin/env python3
"""Guarded phrase continuation that emits candidate-level ePK evidence rows.

This helper follows the review-only positive-evidence lane contract. It starts
from source-rich phrase surfaces, applies pre-CIF RCSB filters for canonical ePK
family plus exact nucleotide/metal or transition-analog ligand context, skips
PDB IDs already seen in prior lane artifacts by default, then transiently scans
mmCIF coordinates and writes compact candidate-level summaries.

No raw coordinate dumps, labels, thresholds, production scores, registries,
fingerprints, migrations, or production claims are written.
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import current_release_epk_followup as current


LANE_ID = "epk_positive_evidence"
SCHEMA_VERSION = "epk_candidate_evidence_v1"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
PDB_ID_RE = re.compile(r"^[0-9][A-Za-z0-9]{3}$")


@dataclass(frozen=True)
class GuardedSurface:
    surface_id: str
    phrase: str
    ligand_mode: str
    rows: int = 100
    start: int = 0
    rationale: str = ""


PHRASE_CONTINUATION_SURFACES = [
    GuardedSurface(
        "protein_kinase_precatalytic_substrate_atp_gamma_rows1_100",
        "protein kinase pre-catalytic substrate ATP",
        "gamma",
        100,
        0,
        "Prior run returned 232 phrase rows but hit the global CIF cap before this surface.",
    ),
    GuardedSurface(
        "protein_kinase_precatalytic_substrate_atp_gamma_rows101_200",
        "protein kinase pre-catalytic substrate ATP",
        "gamma",
        100,
        100,
        "Continuation page for the capped precatalytic phrase surface.",
    ),
    GuardedSurface(
        "protein_kinase_precatalytic_substrate_atp_gamma_rows201_232",
        "protein kinase pre-catalytic substrate ATP",
        "gamma",
        100,
        200,
        "Tail page for the capped precatalytic phrase surface.",
    ),
    GuardedSurface(
        "protein_kinase_precatalytic_substrate_atp_transition_rows1_100",
        "protein kinase pre-catalytic substrate ATP",
        "transition",
        100,
        0,
        "Transition-analog pass with the same source phrase and ADP+metal-fluoride context.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_bound_amp_pnp_gamma",
        "protein kinase substrate-bound AMP-PNP",
        "gamma",
        100,
        0,
        "Prior run returned 43 phrase rows but did not reach this surface before the CIF cap.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_bound_amp_pnp_transition",
        "protein kinase substrate-bound AMP-PNP",
        "transition",
        100,
        0,
        "Transition-analog pass for the substrate-bound AMP-PNP source phrase.",
    ),
]


ACTIVE_GAMMA_SOURCE_SURFACES = [
    GuardedSurface(
        "protein_kinase_substrate_peptide_amp_pnp_magnesium_gamma",
        "protein kinase substrate peptide AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets explicit substrate-peptide AMP-PNP/Mg source wording under exact canonical ePK filters.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_peptide_atpgammas_magnesium_gamma",
        "protein kinase substrate peptide ATPgammaS magnesium",
        "gamma",
        100,
        0,
        "Targets ATPgammaS spelling not covered by exact AGS ligand searches alone.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_peptide_atp_gamma_s_magnesium_gamma",
        "protein kinase substrate peptide ATP gamma S magnesium",
        "gamma",
        100,
        0,
        "Targets spaced ATP gamma S source wording for active-gamma analog complexes.",
    ),
    GuardedSurface(
        "protein_kinase_ternary_complex_substrate_atp_gamma",
        "protein kinase ternary complex substrate ATP",
        "gamma",
        100,
        0,
        "Targets ternary-complex wording that may describe kinase-substrate-nucleotide states.",
    ),
    GuardedSurface(
        "protein_kinase_michaelis_complex_substrate_atp_gamma",
        "protein kinase Michaelis complex substrate ATP",
        "gamma",
        100,
        0,
        "Targets Michaelis-complex wording with exact active-gamma ligand/metal filters.",
    ),
    GuardedSurface(
        "protein_kinase_prereactive_substrate_atp_gamma",
        "protein kinase pre-reactive substrate ATP",
        "gamma",
        100,
        0,
        "Targets pre-reactive wording distinct from the exhausted pre-catalytic surface.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_peptide_transition_state_mimic_transition",
        "protein kinase substrate peptide transition state mimic",
        "transition",
        100,
        0,
        "Targets peptide transition-state mimic wording with exact ADP+metal-fluoride filters.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_peptide_adp_metal_fluoride_transition",
        "protein kinase substrate peptide ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets ADP metal-fluoride phrase variants for candidate-level transition-analog rows.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_protein_amp_pnp_magnesium_gamma",
        "protein kinase substrate protein AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets folded-protein substrate wording with AMP-PNP/Mg source context.",
    ),
    GuardedSurface(
        "protein_kinase_protein_substrate_atp_magnesium_gamma",
        "protein kinase protein substrate ATP magnesium",
        "gamma",
        100,
        0,
        "Targets folded-protein substrate wording with ATP/Mg source context.",
    ),
    GuardedSurface(
        "protein_kinase_protein_substrate_atp_magnesium_gamma_rows101_185",
        "protein kinase protein substrate ATP magnesium",
        "gamma",
        100,
        100,
        "Second page for the broad folded-protein ATP/Mg source surface.",
    ),
    GuardedSurface(
        "kinase_substrate_phosphoacceptor_atp_magnesium_gamma",
        "kinase substrate phosphoacceptor ATP magnesium",
        "gamma",
        100,
        0,
        "Targets explicit phosphoacceptor wording under active-gamma filters.",
    ),
    GuardedSurface(
        "tyrosine_kinase_substrate_peptide_amp_pnp_magnesium_gamma",
        "tyrosine kinase substrate peptide AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets Tyr-kinase substrate peptide AMP-PNP/Mg wording.",
    ),
]


BOUND_STATE_SOURCE_SURFACES = [
    GuardedSurface(
        "protein_kinase_substrate_bound_amp_pnp_space_gamma",
        "protein kinase substrate bound AMP PNP",
        "gamma",
        100,
        0,
        "Targets substrate bound wording without hyphenation or nucleotide hyphenation.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_bound_amp_pnp_hyphen_gamma",
        "protein kinase substrate bound AMP-PNP",
        "gamma",
        100,
        0,
        "Targets substrate bound wording without a substrate-bound hyphen.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_bound_atp_gamma",
        "protein kinase substrate bound ATP",
        "gamma",
        100,
        0,
        "Targets active-gamma substrate-bound wording independent of AMP-PNP.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_complex_amp_pnp_magnesium_gamma",
        "protein kinase substrate complex AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets kinase-substrate complex wording with AMP-PNP/Mg.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_complex_atp_magnesium_gamma",
        "protein kinase substrate complex ATP magnesium",
        "gamma",
        100,
        0,
        "Targets kinase-substrate complex wording with ATP/Mg.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_complex_atp_magnesium_gamma_rows101_200",
        "protein kinase substrate complex ATP magnesium",
        "gamma",
        100,
        100,
        "Second page for kinase-substrate complex ATP/Mg wording.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_complex_atp_gamma_s_magnesium_gamma",
        "protein kinase substrate complex ATP gamma S magnesium",
        "gamma",
        100,
        0,
        "Targets kinase-substrate complex ATP gamma S wording.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_complex_adp_metal_fluoride_transition",
        "protein kinase substrate complex ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets kinase-substrate complex transition-analog wording.",
    ),
    GuardedSurface(
        "kinase_substrate_complex_atp_magnesium_gamma",
        "kinase-substrate complex ATP magnesium",
        "gamma",
        100,
        0,
        "Targets hyphenated kinase-substrate complex wording with ATP/Mg.",
    ),
    GuardedSurface(
        "kinase_substrate_complex_amp_pnp_magnesium_gamma",
        "kinase-substrate complex AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets hyphenated kinase-substrate complex wording with AMP-PNP/Mg.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_trapped_atp_gamma",
        "protein kinase substrate trapped ATP",
        "gamma",
        100,
        0,
        "Targets substrate-trapped wording distinct from substrate-trapping.",
    ),
    GuardedSurface(
        "protein_kinase_substrate_capture_atp_gamma",
        "protein kinase substrate capture ATP",
        "gamma",
        100,
        0,
        "Targets substrate-capture wording under active-gamma filters.",
    ),
]


SURFACE_SETS = {
    "bound_state_source_terms": BOUND_STATE_SOURCE_SURFACES,
    "phrase_continuation": PHRASE_CONTINUATION_SURFACES,
    "active_gamma_source_terms": ACTIVE_GAMMA_SOURCE_SURFACES,
}

DEFAULT_SURFACES = PHRASE_CONTINUATION_SURFACES


def collect_prior_pdb_ids(artifacts_dir: Path, out: Path) -> dict[str, list[str]]:
    prior: dict[str, list[str]] = {}

    def add(pdb_id: Any, source: Path) -> None:
        if not isinstance(pdb_id, str):
            return
        token = pdb_id.upper()
        if PDB_ID_RE.match(token):
            prior.setdefault(token, []).append(str(source))

    def walk(value: Any, source: Path) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key == "pdb_id":
                    add(nested, source)
                elif key == "pdb_ids" and isinstance(nested, list):
                    for item in nested:
                        add(item, source)
                else:
                    walk(nested, source)
        elif isinstance(value, list):
            for nested in value:
                walk(nested, source)

    for path in sorted(artifacts_dir.glob("*.json")):
        if path.resolve() == out.resolve():
            continue
        try:
            payload = json.loads(path.read_text())
        except Exception:  # noqa: BLE001 - prior artifact indexing is best effort.
            continue
        walk(payload, path)
    return prior


def surface_query(surface: GuardedSurface) -> dict[str, Any]:
    return current.group(
        "and",
        [
            current.full_text(surface.phrase),
            current.family_group(),
            *current.ligand_nodes(surface.ligand_mode),
        ],
    )


def search_surface(surface: GuardedSurface) -> dict[str, Any]:
    payload = {
        "query": surface_query(surface),
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": surface.start, "rows": surface.rows},
            "results_content_type": ["experimental"],
        },
    }
    result = current.fetch_json(current.RCSB_SEARCH_URL, payload=payload)
    ids = [row["identifier"].upper() for row in result.get("result_set", [])]
    ligand_label = (
        "ATP/ANP/ACP/AGS+MG/MN"
        if surface.ligand_mode == "gamma"
        else "ADP+AF3/ALF/BEF/MGF"
    )
    return {
        "surface_id": surface.surface_id,
        "query_or_source": (
            "RCSB advanced guarded phrase: "
            f"full_text='{surface.phrase}' AND canonical ePK AND {ligand_label}"
        ),
        "phrase": surface.phrase,
        "ligand_mode": surface.ligand_mode,
        "rationale": surface.rationale,
        "start": surface.start,
        "requested_rows": surface.rows,
        "total_count": result.get("total_count", len(ids)),
        "returned_count": len(ids),
        "pdb_ids": ids,
    }


def cif_content_length(pdb_id: str, timeout: int = 15) -> int | None:
    request = urllib.request.Request(
        current.scout.RCSB_CIF_URL.format(pdb_id=pdb_id),
        method="HEAD",
        headers={"User-Agent": "catalytic-earth-epk-positive-evidence/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            header = response.headers.get("Content-Length")
    except Exception:  # noqa: BLE001 - size guard is best effort.
        return None
    if not header:
        return None
    try:
        return int(header)
    except ValueError:
        return None


class RowTimeoutError(TimeoutError):
    pass


def _timeout_handler(_signum: int, _frame: Any) -> None:
    raise RowTimeoutError("row scan exceeded per-row timeout")


def scan_pdb_id_guarded(
    pdb_id: str,
    search_hits: list[dict[str, Any]],
    max_cif_bytes: int,
    row_timeout_seconds: int,
) -> dict[str, Any]:
    cif_size = cif_content_length(pdb_id)
    if cif_size is not None and cif_size > max_cif_bytes:
        return {
            "pdb_id": pdb_id,
            "search_hits": search_hits,
            "candidate_status": "cif_too_large_skipped_review_only",
            "cif_content_length_bytes": cif_size,
            "max_cif_bytes": max_cif_bytes,
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
    previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(row_timeout_seconds)
    try:
        row = current.scan_pdb_id(pdb_id, search_hits)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)
    if cif_size is not None:
        row["cif_content_length_bytes"] = cif_size
    return row


def candidate_kind(hit: dict[str, Any]) -> str:
    description = (hit.get("candidate_entity_description") or "").lower()
    length = hit.get("candidate_entity_length")
    if "peptide" in description or "pseudo" in description or "inhibitor" in description:
        return "peptide_or_short"
    if length and length >= 50:
        return "folded_protein"
    if description:
        return "folded_protein_length_unknown"
    return "short_or_unknown"


def discovery_score(hit: dict[str, Any], state: str, prior_seen: bool) -> float:
    score = 0.2
    if hit.get("has_local_mg_or_mn"):
        score += 0.2
    if hit.get("candidate_source_mapped"):
        score += 0.15
    if candidate_kind(hit) == "folded_protein":
        score += 0.15
    elif candidate_kind(hit) == "folded_protein_length_unknown":
        score += 0.1
    distance = (
        hit.get("nearest_terminal_distance_angstrom") or hit.get("nearest_gamma_distance_angstrom")
        if state == "active_gamma"
        else hit.get("nearest_analog_distance_angstrom")
    )
    if isinstance(distance, (int, float)) and distance <= 4.0:
        score += 0.1
    if state == "transition_analog":
        score -= 0.05
    if prior_seen:
        score -= 0.05
    return round(max(0.0, min(score, 0.85)), 3)


def source_context(row: dict[str, Any], hit: dict[str, Any], prior_sources: list[str]) -> dict[str, Any]:
    citation = row.get("citation") or {}
    return {
        "structure_title": row.get("title"),
        "citation_title": citation.get("title"),
        "citation_year": citation.get("year"),
        "citation_pubmed_id": citation.get("pdbx_database_id_pub_med"),
        "citation_doi": citation.get("pdbx_database_id_doi"),
        "candidate_entity_description": hit.get("candidate_entity_description"),
        "candidate_entity_uniprot_ids": hit.get("candidate_entity_uniprot_ids", []),
        "associated_kinase_entity_description": hit.get("terminal_associated_entity_description")
        or hit.get("gamma_associated_entity_description")
        or hit.get("analog_associated_entity_description"),
        "associated_kinase_entity_uniprot_ids": hit.get("terminal_associated_entity_uniprot_ids", [])
        or hit.get("gamma_associated_entity_uniprot_ids", [])
        or hit.get("analog_associated_entity_uniprot_ids", []),
        "candidate_sequence_scheme_matches": hit.get("candidate_sequence_scheme_matches", []),
        "candidate_source_mapped": bool(hit.get("candidate_source_mapped")),
        "search_hits": row.get("search_hits", []),
        "prior_lane_artifact_sources_sample": prior_sources[:5],
    }


def blocker_tags(hit: dict[str, Any], state: str, prior_seen: bool) -> list[str]:
    blockers = [
        "review_only_lane",
        "source_review_not_predictive_coordinate_feature",
        "production_policy_abstain",
    ]
    if prior_seen:
        blockers.append("prior_lane_artifact_seen")
    if not hit.get("has_local_mg_or_mn"):
        blockers.append("no_local_mg_or_mn")
    if not hit.get("candidate_source_mapped"):
        blockers.append("candidate_residue_not_sequence_scheme_mapped")
    kind = candidate_kind(hit)
    if kind == "folded_protein_length_unknown":
        blockers.append("candidate_entity_length_unknown")
    elif kind != "folded_protein":
        blockers.append("peptide_short_or_unknown_substrate_context")
    if state == "transition_analog":
        blockers.append("transition_or_product_analog_state_not_countable")
    return blockers


def signal_tags(hit: dict[str, Any], state: str, prior_seen: bool) -> list[str]:
    tags = [SCHEMA_VERSION, state, "discovery_only_not_predictive"]
    tags.append(candidate_kind(hit))
    tags.append("local_metal" if hit.get("has_local_mg_or_mn") else "no_local_metal")
    tags.append("source_mapped" if hit.get("candidate_source_mapped") else "source_mapping_pending")
    if prior_seen:
        tags.append("repeat_lane_candidate")
    return tags


def canonical_candidate_row(
    row: dict[str, Any],
    hit: dict[str, Any],
    hit_index: int,
    prior_seen: bool,
    prior_sources: list[str],
) -> dict[str, Any]:
    state = "active_gamma"
    terminal_ligand_code = hit.get("terminal_ligand_code") or hit.get("gamma_ligand_code")
    terminal_atom_name = hit.get("terminal_atom_name") or hit.get("gamma_atom_name")
    terminal_chain_name = hit.get("terminal_chain_name") or hit.get("gamma_chain_name")
    terminal_auth_seq_id = hit.get("terminal_auth_seq_id") or hit.get("gamma_auth_seq_id")
    associated_chain_name = hit.get("terminal_associated_polymer_chain_name") or hit.get(
        "gamma_associated_polymer_chain_name"
    )
    associated_entity_id = hit.get("terminal_associated_polymer_entity_id") or hit.get(
        "gamma_associated_polymer_entity_id"
    )
    terminal_chain_name = terminal_chain_name or associated_chain_name or "unknown_chain"
    terminal_auth_seq_id = (
        terminal_auth_seq_id
        or (f"associated_entity_{associated_entity_id}" if associated_entity_id else None)
        or "unknown_ligand_instance"
    )
    distance = hit.get("nearest_terminal_distance_angstrom") or hit.get(
        "nearest_gamma_distance_angstrom"
    )
    candidate_id = (
        f"{row['pdb_id']}:active_gamma:"
        f"{terminal_ligand_code}:{terminal_chain_name}:{terminal_auth_seq_id}:"
        f"{hit.get('candidate_chain_name')}:{hit.get('candidate_auth_seq_id')}:{hit_index}"
    )
    geometry = {
        "coordinate_state": state,
        "terminal_ligand_code": terminal_ligand_code,
        "terminal_atom_name": terminal_atom_name,
        "terminal_chain_name": terminal_chain_name,
        "terminal_auth_seq_id": terminal_auth_seq_id,
        "donor_role": hit.get("donor_role"),
        "terminal_associated_polymer_chain_name": associated_chain_name,
        "terminal_associated_polymer_entity_id": associated_entity_id,
        "terminal_instance_inferred_from_associated_polymer": not bool(
            hit.get("terminal_chain_name")
            or hit.get("gamma_chain_name")
            or hit.get("terminal_auth_seq_id")
            or hit.get("gamma_auth_seq_id")
        ),
        "candidate_residue_code": hit.get("candidate_residue_code"),
        "candidate_atom_name": hit.get("candidate_atom_name"),
        "candidate_chain_name": hit.get("candidate_chain_name"),
        "candidate_auth_seq_id": hit.get("candidate_auth_seq_id"),
        "candidate_label_seq_id": hit.get("candidate_label_seq_id"),
        "nearest_terminal_distance_angstrom": distance,
        "has_local_mg_or_mn": bool(hit.get("has_local_mg_or_mn")),
        "local_metals": hit.get("local_metals", []),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "candidate_id": candidate_id,
        "pdb_id": row["pdb_id"],
        "coordinate_state": state,
        "source_free_geometry": geometry,
        "source_context": source_context(row, hit, prior_sources),
        "discovery_signal_score": discovery_score(hit, state, prior_seen),
        "signal_tags": signal_tags(hit, state, prior_seen),
        "blockers": blocker_tags(hit, state, prior_seen),
        "claim_status": "candidate_review_only_non_countable",
        "policy_decision": "review_only_abstain",
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "countable_label_candidate": False,
        "target_family_id": TARGET_FAMILY_ID,
        "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
    }


def transition_candidate_row(
    row: dict[str, Any],
    hit: dict[str, Any],
    hit_index: int,
    prior_seen: bool,
    prior_sources: list[str],
) -> dict[str, Any]:
    state = "transition_analog"
    candidate_id = (
        f"{row['pdb_id']}:transition_analog:"
        f"{hit.get('analog_ligand_code')}:{hit.get('analog_chain_name')}:{hit.get('analog_auth_seq_id')}:"
        f"{hit.get('candidate_chain_name')}:{hit.get('candidate_auth_seq_id')}:{hit_index}"
    )
    geometry = {
        "coordinate_state": state,
        "analog_ligand_code": hit.get("analog_ligand_code"),
        "analog_chain_name": hit.get("analog_chain_name"),
        "analog_auth_seq_id": hit.get("analog_auth_seq_id"),
        "nearest_analog_atom": hit.get("nearest_analog_atom"),
        "candidate_residue_code": hit.get("candidate_residue_code"),
        "candidate_atom_name": hit.get("candidate_atom_name"),
        "candidate_chain_name": hit.get("candidate_chain_name"),
        "candidate_auth_seq_id": hit.get("candidate_auth_seq_id"),
        "candidate_label_seq_id": hit.get("candidate_label_seq_id"),
        "nearest_analog_distance_angstrom": hit.get("nearest_analog_distance_angstrom"),
        "has_local_mg_or_mn": bool(hit.get("has_local_mg_or_mn")),
        "local_metals": hit.get("local_metals", []),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "candidate_id": candidate_id,
        "pdb_id": row["pdb_id"],
        "coordinate_state": state,
        "source_free_geometry": geometry,
        "source_context": source_context(row, hit, prior_sources),
        "discovery_signal_score": discovery_score(hit, state, prior_seen),
        "signal_tags": signal_tags(hit, state, prior_seen),
        "blockers": blocker_tags(hit, state, prior_seen),
        "claim_status": "candidate_review_only_non_countable",
        "policy_decision": "review_only_abstain",
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "countable_label_candidate": False,
        "target_family_id": TARGET_FAMILY_ID,
        "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
    }


def candidate_rows_from_scan(
    row: dict[str, Any],
    prior_pdb_ids: dict[str, list[str]],
) -> list[dict[str, Any]]:
    prior_sources = prior_pdb_ids.get(row["pdb_id"], [])
    prior_seen = bool(prior_sources)
    candidates: list[dict[str, Any]] = []
    for index, hit in enumerate(row.get("heteromeric_candidate_hits", []), start=1):
        candidates.append(canonical_candidate_row(row, hit, index, prior_seen, prior_sources))
    for index, hit in enumerate(row.get("transition_analog_candidate_hits", []), start=1):
        candidates.append(transition_candidate_row(row, hit, index, prior_seen, prior_sources))
    return candidates


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    surface_set_name: str,
    surfaces: list[GuardedSurface],
    max_unique_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
    include_prior_seen: bool,
    ignore_prior_pdb_ids: list[str],
) -> dict[str, Any]:
    generated_at = current.now_iso()
    prior_pdb_ids = collect_prior_pdb_ids(artifacts_dir, out)
    for pdb_id in ignore_prior_pdb_ids:
        prior_pdb_ids.pop(pdb_id.upper(), None)
    search_surfaces = []
    seen: dict[str, list[dict[str, Any]]] = {}
    skipped_prior_seen: dict[str, list[dict[str, Any]]] = {}

    for surface in surfaces:
        result = search_surface(surface)
        search_surfaces.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1 + surface.start):
            hit = {
                "surface_id": result["surface_id"],
                "rank": rank,
                "query_or_source": result["query_or_source"],
                "rationale": result["rationale"],
            }
            if pdb_id in prior_pdb_ids and not include_prior_seen:
                skipped_prior_seen.setdefault(pdb_id, []).append(hit)
                continue
            if pdb_id not in seen and len(seen) >= max_unique_pdb_ids:
                continue
            seen.setdefault(pdb_id, []).append(hit)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    candidate_rows = []
    for pdb_id, search_hits in seen.items():
        try:
            row = scan_pdb_id_guarded(pdb_id, search_hits, max_cif_bytes, row_timeout_seconds)
            row["prior_lane_artifact_seen"] = pdb_id in prior_pdb_ids
            row["prior_lane_artifact_sources_sample"] = prior_pdb_ids.get(pdb_id, [])[:5]
            rows.append(row)
            candidate_rows.extend(candidate_rows_from_scan(row, prior_pdb_ids))
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            row = {
                "pdb_id": pdb_id,
                "search_hits": search_hits,
                "candidate_status": "fetch_or_parse_failed_review_only",
                "fetch_error": repr(exc),
                "prior_lane_artifact_seen": pdb_id in prior_pdb_ids,
                "prior_lane_artifact_sources_sample": prior_pdb_ids.get(pdb_id, [])[:5],
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
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(row)
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    coordinate_state_counts: dict[str, int] = {}
    for row in rows:
        status = row["candidate_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    for candidate in candidate_rows:
        state = candidate["coordinate_state"]
        coordinate_state_counts[state] = coordinate_state_counts.get(state, 0) + 1

    fresh_candidate_rows = [
        candidate
        for candidate in candidate_rows
        if "prior_lane_artifact_seen" not in candidate["blockers"]
    ]
    folded_fresh = [
        candidate["candidate_id"]
        for candidate in fresh_candidate_rows
        if "folded_protein" in candidate["signal_tags"]
    ]

    evidence_for = []
    if fresh_candidate_rows:
        evidence_for.append(
            f"Guarded phrase surfaces emitted {len(fresh_candidate_rows)} fresh candidate-level rows."
        )
    if folded_fresh:
        evidence_for.append(
            "Fresh folded-protein candidate rows need source adjudication: "
            + ", ".join(folded_fresh[:10])
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Guarded phrase surfaces produced no fresh candidate-level geometry rows after pre-CIF filters."
        )

    evidence_against = [
        "No production-positive ePK claim is allowed; all candidate rows remain review-only abstentions.",
        "Source context is recorded separately from source-free geometry and must not be used as a predictive coordinate feature.",
    ]
    if not fresh_candidate_rows:
        evidence_against.append(
            f"The guarded {surface_set_name} surface set is exhausted for fresh candidate rows under canonical ePK plus exact ligand/metal prefilters."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "guarded_phrase_candidate_rows",
            "schema_version": SCHEMA_VERSION,
            "surface_set": surface_set_name,
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "search_surface_count": len(search_surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_surfaces),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_surfaces),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "candidate_evidence_rows_emitted": len(candidate_rows),
            "fresh_candidate_evidence_rows_emitted": len(fresh_candidate_rows),
            "coordinate_state_counts": coordinate_state_counts,
            "prior_lane_pdb_id_count": len(prior_pdb_ids),
            "skipped_prior_seen_pdb_id_count": len(skipped_prior_seen),
            "skipped_prior_seen_pdb_ids_sample": sorted(skipped_prior_seen)[:80],
            "include_prior_seen": include_prior_seen,
            "ignore_prior_pdb_ids": sorted({pdb_id.upper() for pdb_id in ignore_prior_pdb_ids}),
            "max_unique_pdb_ids": max_unique_pdb_ids,
            "max_cif_bytes": max_cif_bytes,
            "row_timeout_seconds": row_timeout_seconds,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Candidate evidence rows are discovery/source-review rows only. "
                "Source context is separated from source-free geometry and cannot be "
                "used as a production predictive feature."
            ),
            "source_urls": [
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_POLYMER_ENTITY_URL,
                current.scout.RCSB_CIF_URL,
            ],
        },
        "search_surfaces": search_surfaces,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "candidate_evidence_rows": candidate_rows,
        "source_review_summary": {
            "primary_outcome": (
                "candidate_evidence_rows_emitted"
                if fresh_candidate_rows
                else "search_surface_exhausted"
            ),
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(fresh_candidate_rows),
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "counterexamples_found": [],
            "recommendation": (
                "If fresh rows exist, source-adjudicate them manually before any future frozen policy. "
                "If none exist, keep the guarded phrase continuation exhausted until a new RCSB release "
                "or new publication metadata appears."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_positive_evidence"),
    )
    parser.add_argument("--max-unique-pdb-ids", type=int, default=80)
    parser.add_argument("--max-cif-bytes", type=int, default=25_000_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=45)
    parser.add_argument("--sleep-seconds", type=float, default=0.03)
    parser.add_argument("--include-prior-seen", action="store_true")
    parser.add_argument("--ignore-prior-pdb-id", action="append", default=[])
    parser.add_argument("--surface-set", choices=sorted(SURFACE_SETS), default="phrase_continuation")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.artifacts_dir,
        args.surface_set,
        SURFACE_SETS[args.surface_set],
        args.max_unique_pdb_ids,
        args.max_cif_bytes,
        args.row_timeout_seconds,
        args.sleep_seconds,
        args.include_prior_seen,
        args.ignore_prior_pdb_id,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "candidate_evidence_rows_emitted": artifact["metadata"]["candidate_evidence_rows_emitted"],
                "fresh_candidate_evidence_rows_emitted": artifact["metadata"][
                    "fresh_candidate_evidence_rows_emitted"
                ],
                "coordinate_state_counts": artifact["metadata"]["coordinate_state_counts"],
                "skipped_prior_seen_pdb_id_count": artifact["metadata"]["skipped_prior_seen_pdb_id_count"],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
