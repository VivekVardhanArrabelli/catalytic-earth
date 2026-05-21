#!/usr/bin/env python3
"""Emit compact source-free ePK gamma/acceptor candidate evidence rows.

This lane-local helper enumerates candidate-level structural evidence from the
frozen diagnostic tranche. It separates source-free coordinate evidence from
review labels, fetches PDB coordinates in memory only for compact coordinate
certainty metrics, and writes no raw coordinate dumps.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from coordinate_certainty_probe import (
    coordinate_certainty_class,
    fetch_pdb_text_with_retries,
    matching_atom_variants,
    parse_pdb_atoms_with_certainty,
    preferred_atom,
    stats_for_atom,
)
from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_candidate_evidence_v1_20260521"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_active_site_orientation_asymmetry_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)

PRIMARY_OUTCOMES = {
    "candidate_evidence_rows_emitted",
    "blocker_cleared_source_free",
    "blocker_not_cleared_data_scarcity",
    "blocker_not_cleared_method_weakness",
    "blocker_not_cleared_biology_ambiguity",
    "counterexample_found",
    "next_query_defined",
}

BLOCKER_CLASSES = {
    "active_gamma_geometry",
    "product_state_evidence",
    "substrate_analog_evidence",
    "split_state_evidence",
    "topology_ambiguity",
    "substrate_role_identity",
    "internal_fragment_mimicry",
    "ligand_materialization",
    "source_leakage",
    "wetlab_only_biology",
    "none",
}

COORDINATE_STATES = {
    "active_gamma",
    "product_state",
    "adp_state",
    "substrate_acceptor_analog_state",
    "split_state",
    "ligand_absent",
    "metal_absent",
    "unavailable_coordinate_state",
    "ambiguous_coordinate_state",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_source_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    return payload["diagnostic_rows"]


def atom_id(atom: dict[str, Any] | None) -> str:
    if not atom:
        return "none"
    icode = atom.get("icode") or ""
    return (
        f"{atom.get('chain_id')}:{atom.get('residue_code')}"
        f"{atom.get('auth_seq_id')}{icode}:{atom.get('atom_name')}"
    )


def candidate_id(pdb_id: str, candidate: dict[str, Any]) -> str:
    gamma = atom_id(candidate.get("terminal_gamma_equivalent_atom"))
    acceptor = atom_id(candidate.get("nearest_protein_hydroxyl_atom"))
    return f"{pdb_id}|gamma={gamma}|acceptor={acceptor}"


def compact_atom(atom: dict[str, Any] | None) -> dict[str, Any] | None:
    if not atom:
        return None
    return {
        "atom_name": atom.get("atom_name"),
        "residue_code": atom.get("residue_code"),
        "chain_id": atom.get("chain_id"),
        "auth_seq_id": atom.get("auth_seq_id"),
        "icode": atom.get("icode"),
    }


def coordinate_state(ligand_state: str | None, terminal_gamma_available: bool) -> str:
    if ligand_state is None:
        return "unavailable_coordinate_state"
    if ligand_state.startswith("active_gamma_capable") and terminal_gamma_available:
        return "active_gamma"
    if ligand_state == "no_nucleotide_like_ligand_detected":
        return "ligand_absent"
    if ligand_state.startswith("nucleotide_like_without_terminal_gamma:ADP"):
        return "adp_state"
    if ligand_state.startswith("nucleotide_like_without_terminal_gamma:"):
        return "ambiguous_coordinate_state"
    if not terminal_gamma_available:
        return "unavailable_coordinate_state"
    return "ambiguous_coordinate_state"


def row_availability_class(features: dict[str, Any]) -> str:
    if not features.get("terminal_gamma_equivalent_atom_available"):
        state = features.get("ligand_state") or ""
        if state.startswith("nucleotide_like_without_terminal_gamma:ADP"):
            return "phosphotransfer_gamma_unavailable_adp_state"
        if state.startswith("nucleotide_like_without_terminal_gamma:"):
            return "phosphotransfer_gamma_unavailable_ambiguous_ligand_state"
        if state == "no_nucleotide_like_ligand_detected":
            return "phosphotransfer_gamma_unavailable_ligand_absent"
        return "phosphotransfer_gamma_unavailable_unknown_state"
    if features.get("nearest_strict_auth_terminal_guard_candidate"):
        return "claimable_by_auth_guard_strict_context"
    strict = features.get("nearest_strict_cross_chain_candidate")
    if strict and strict.get("candidate_resolved_n_terminal_internal_fragment_like"):
        return "blocked_internal_fragment_n_terminal_mimic"
    if features.get("nearest_reciprocal_folded_tyr_rescue_candidate"):
        return "ambiguous_reciprocal_folded_tyr_context"
    for candidate in features.get("orientation_enriched_candidates_within_8a", []):
        if candidate.get("same_chain_topology") and candidate.get("distance_angstrom") is not None:
            if candidate["distance_angstrom"] <= 6.0:
                return "ambiguous_same_chain_autophosphorylation_like_context"
    if features.get("orientation_enriched_candidates_within_8a"):
        return "hydroxyl_near_gamma_but_no_claimable_identity_context"
    return "terminal_gamma_available_but_no_near_hydroxyl_candidate"


def classify_blocker(
    row: dict[str, Any],
    candidate: dict[str, Any] | None,
    state: str,
    coordinate_certainty: str | None = None,
) -> str:
    if state in {"product_state", "adp_state"}:
        return "product_state_evidence"
    if state == "substrate_acceptor_analog_state":
        return "substrate_analog_evidence"
    if state == "split_state":
        return "split_state_evidence"
    if state in {"ligand_absent", "unavailable_coordinate_state", "ambiguous_coordinate_state"}:
        return "ligand_materialization"
    if state == "metal_absent":
        return "active_gamma_geometry"
    if candidate is None:
        return "active_gamma_geometry"
    if candidate.get("candidate_resolved_n_terminal_internal_fragment_like") and not candidate.get(
        "candidate_acceptor_chain_is_short_peptide_like"
    ):
        return "internal_fragment_mimicry"
    distance = candidate.get("distance_angstrom")
    if distance is None or distance > 6.0:
        return "active_gamma_geometry"
    if coordinate_certainty in {"unavailable_atom_not_resolved", "unavailable_fetch_error"}:
        return "ligand_materialization"
    reciprocal = candidate.get("reciprocal_context_class") or ""
    if candidate.get("same_chain_topology") or reciprocal.startswith("reciprocal_"):
        return "topology_ambiguity"
    if candidate.get("cross_chain_topology") and not candidate.get("ligand_acceptor_same_sequence_entity"):
        if candidate.get("candidate_resolved_n_terminal_auth_terminal_like"):
            return "none"
        if candidate.get("candidate_acceptor_chain_is_short_peptide_like"):
            return "none"
    if candidate.get("candidate_acceptor_chain_is_folded_like") and not candidate.get(
        "candidate_acceptor_chain_is_short_peptide_like"
    ):
        return "substrate_role_identity"
    return "none"


def candidate_role_class(features: dict[str, Any], candidate: dict[str, Any]) -> str:
    strict_auth = features.get("nearest_strict_auth_terminal_guard_candidate")
    strict_cross = features.get("nearest_strict_cross_chain_candidate")
    reciprocal = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
    cid = candidate_id("_", candidate).split("|", 1)[1]
    if strict_auth and candidate_id("_", strict_auth).split("|", 1)[1] == cid:
        return "strict_auth_terminal_guard_candidate"
    if strict_cross and candidate_id("_", strict_cross).split("|", 1)[1] == cid:
        return "strict_cross_chain_candidate"
    if reciprocal and candidate_id("_", reciprocal).split("|", 1)[1] == cid:
        return "reciprocal_folded_tyr_candidate"
    if candidate.get("same_chain_topology"):
        return "same_chain_candidate"
    return "near_hydroxyl_candidate"


def compact_orientation(candidate: dict[str, Any]) -> dict[str, Any]:
    orientation = candidate.get("active_site_orientation_features", {})
    return {
        "orientation_support_class": orientation.get("orientation_support_class"),
        "orientation_status": orientation.get("orientation_status"),
        "gamma_to_hydroxyl_distance_angstrom": orientation.get("gamma_to_hydroxyl_distance_angstrom"),
        "hydroxyl_anchor_to_gamma_angle_degrees": orientation.get(
            "hydroxyl_anchor_to_gamma_angle_degrees"
        ),
        "gamma_site_protein_heavy_atom_count_within_6a_excluding_ligand": orientation.get(
            "gamma_site_protein_heavy_atom_count_within_6a_excluding_ligand"
        ),
        "gamma_site_ligand_chain_heavy_atom_count_within_6a": orientation.get(
            "gamma_site_ligand_chain_heavy_atom_count_within_6a"
        ),
        "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a": orientation.get(
            "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a_excluding_same_residue"
        ),
        "hydroxyl_gamma_facing_asymmetry_index_within_6a": orientation.get(
            "hydroxyl_gamma_facing_asymmetry_index_within_6a"
        ),
    }


def compact_exposure(candidate: dict[str, Any]) -> dict[str, Any]:
    exposure = candidate.get("local_exposure_features", {})
    return {
        "local_exposure_profile_class": exposure.get("local_exposure_profile_class"),
        "local_exposure_status": exposure.get("local_exposure_status"),
        "open_shell_fraction_3a_excluding_same_residue": exposure.get(
            "open_shell_fraction_3a_excluding_same_residue"
        ),
        "open_shell_fraction_5a_excluding_same_residue": exposure.get(
            "open_shell_fraction_5a_excluding_same_residue"
        ),
        "protein_heavy_atom_count_within_6a_excluding_same_residue": exposure.get(
            "protein_heavy_atom_count_within_6a_excluding_same_residue"
        ),
        "other_chain_protein_heavy_atom_count_within_6a_excluding_same_residue": exposure.get(
            "other_chain_protein_heavy_atom_count_within_6a_excluding_same_residue"
        ),
        "same_chain_protein_heavy_atom_count_within_6a_excluding_same_residue": exposure.get(
            "same_chain_protein_heavy_atom_count_within_6a_excluding_same_residue"
        ),
        "water_oxygen_count_within_6a": exposure.get("water_oxygen_count_within_6a"),
        "nucleotide_or_metal_heavy_atom_count_within_6a_excluding_selected_gamma_residue": exposure.get(
            "nucleotide_or_metal_heavy_atom_count_within_6a_excluding_selected_gamma_residue"
        ),
    }


class CoordinateCertaintyCache:
    def __init__(self, workflow_started_at: str) -> None:
        self.workflow_started_at = workflow_started_at
        self._atom_cache: dict[str, tuple[list[dict[str, Any]] | None, str | None]] = {}

    def atoms_for_pdb(self, pdb_id: str) -> tuple[list[dict[str, Any]] | None, str | None]:
        if pdb_id not in self._atom_cache:
            text, fetch_error = fetch_pdb_text_with_retries(pdb_id)
            if text is None:
                self._atom_cache[pdb_id] = (None, fetch_error)
            else:
                self._atom_cache[pdb_id] = (parse_pdb_atoms_with_certainty(text), None)
            time.sleep(0.05)
        return self._atom_cache[pdb_id]

    def stats_for_candidate(self, pdb_id: str, candidate: dict[str, Any]) -> dict[str, Any]:
        atoms, fetch_error = self.atoms_for_pdb(pdb_id)
        if atoms is None:
            return {
                "coordinate_certainty_status": "fetch_error",
                "coordinate_certainty_fetch_error": fetch_error,
                "coordinate_certainty_class": "unavailable_fetch_error",
                "feature_extraction_started_after": self.workflow_started_at,
                "acceptor_coordinate_certainty": None,
                "terminal_gamma_coordinate_certainty": None,
            }
        acceptor_variants = matching_atom_variants(atoms, candidate.get("nearest_protein_hydroxyl_atom"))
        gamma_variants = matching_atom_variants(atoms, candidate.get("terminal_gamma_equivalent_atom"))
        acceptor_atom = preferred_atom(acceptor_variants)
        gamma_atom = preferred_atom(gamma_variants)
        acceptor_stats = stats_for_atom(acceptor_atom, atoms, acceptor_variants)
        gamma_stats = stats_for_atom(gamma_atom, atoms, gamma_variants)
        return {
            "coordinate_certainty_status": "ok",
            "coordinate_certainty_class": coordinate_certainty_class(acceptor_stats, gamma_stats),
            "feature_extraction_started_after": self.workflow_started_at,
            "acceptor_coordinate_certainty": acceptor_stats,
            "terminal_gamma_coordinate_certainty": gamma_stats,
        }


def compact_certainty_stats(stats: dict[str, Any] | None) -> dict[str, Any] | None:
    if not stats:
        return None
    return {
        "atom_resolved": stats.get("atom_resolved"),
        "occupancy": stats.get("occupancy"),
        "b_factor": stats.get("b_factor"),
        "altloc_variant_count": stats.get("altloc_variant_count"),
        "altlocs": stats.get("altlocs"),
        "same_residue_heavy_atom_count": stats.get("same_residue_heavy_atom_count"),
        "local_8a_heavy_atom_count_for_b_context": stats.get(
            "local_8a_heavy_atom_count_for_b_context"
        ),
        "same_chain_b_factor_median": stats.get("same_chain_b_factor_median"),
        "same_residue_b_factor_median": stats.get("same_residue_b_factor_median"),
        "local_8a_b_factor_median": stats.get("local_8a_b_factor_median"),
        "protein_b_factor_median": stats.get("protein_b_factor_median"),
        "nonwater_hetero_b_factor_median": stats.get("nonwater_hetero_b_factor_median"),
        "b_factor_to_same_chain_median_ratio": stats.get("b_factor_to_same_chain_median_ratio"),
        "b_factor_to_local_8a_median_ratio": stats.get("b_factor_to_local_8a_median_ratio"),
        "b_factor_to_protein_median_ratio": stats.get("b_factor_to_protein_median_ratio"),
        "local_8a_robust_b_zscore": stats.get("local_8a_robust_b_zscore"),
    }


def evidence_row(
    row: dict[str, Any],
    diagnostic_row_index: int,
    candidate: dict[str, Any],
    candidate_rank: int,
    certainty_cache: CoordinateCertaintyCache,
) -> dict[str, Any]:
    features = row["structure_features"]
    state = coordinate_state(
        features.get("ligand_state"),
        bool(features.get("terminal_gamma_equivalent_atom_available")),
    )
    certainty = certainty_cache.stats_for_candidate(row["pdb_id"], candidate)
    blocker = classify_blocker(row, candidate, state, certainty.get("coordinate_certainty_class"))
    if blocker not in BLOCKER_CLASSES:
        raise ValueError(f"unexpected blocker class: {blocker}")
    if state not in COORDINATE_STATES:
        raise ValueError(f"unexpected coordinate state: {state}")

    return {
        "row_schema": "epk_candidate_evidence_v1",
        "candidate_id": candidate_id(row["pdb_id"], candidate),
        "pdb_id": row["pdb_id"],
        "diagnostic_row_index": diagnostic_row_index,
        "candidate_rank_within_8a": candidate_rank,
        "source_free_evidence": {
            "coordinate_state": state,
            "blocker_class": blocker,
            "candidate_role_class": candidate_role_class(features, candidate),
            "ligand_state": features.get("ligand_state"),
            "availability_class": row_availability_class(features),
            "terminal_gamma_equivalent_atom_available": features.get(
                "terminal_gamma_equivalent_atom_available"
            ),
            "distance_angstrom": candidate.get("distance_angstrom"),
            "nearest_protein_hydroxyl_distance_angstrom": features.get(
                "nearest_protein_hydroxyl_distance_angstrom"
            ),
            "terminal_gamma_atom": compact_atom(candidate.get("terminal_gamma_equivalent_atom")),
            "acceptor_atom": compact_atom(candidate.get("nearest_protein_hydroxyl_atom")),
            "acceptor_residue_code": candidate.get("candidate_acceptor_residue_code"),
            "acceptor_auth_seq_id_int": candidate.get("candidate_acceptor_auth_seq_id_int"),
            "acceptor_residue_ordinal_in_chain": candidate.get(
                "candidate_acceptor_residue_ordinal_in_chain"
            ),
            "acceptor_chain_length": candidate.get("candidate_acceptor_chain_length"),
            "acceptor_chain_is_short_peptide_like": candidate.get(
                "candidate_acceptor_chain_is_short_peptide_like"
            ),
            "acceptor_chain_is_folded_like": candidate.get("candidate_acceptor_chain_is_folded_like"),
            "acceptor_is_tyr": candidate.get("candidate_acceptor_is_tyr"),
            "acceptor_is_n_terminal_sty": candidate.get("candidate_acceptor_is_n_terminal_sty"),
            "acceptor_auth_seq_minus_resolved_ordinal": candidate.get(
                "candidate_acceptor_auth_seq_minus_resolved_ordinal"
            ),
            "acceptor_resolved_n_terminal_auth_terminal_like": candidate.get(
                "candidate_resolved_n_terminal_auth_terminal_like"
            ),
            "acceptor_resolved_n_terminal_internal_fragment_like": candidate.get(
                "candidate_resolved_n_terminal_internal_fragment_like"
            ),
            "same_chain_topology": candidate.get("same_chain_topology"),
            "cross_chain_topology": candidate.get("cross_chain_topology"),
            "ligand_acceptor_same_sequence_entity": candidate.get(
                "ligand_acceptor_same_sequence_entity"
            ),
            "reciprocal_context_class": candidate.get("reciprocal_context_class"),
            "candidate_chain_active_gamma_count": candidate.get("candidate_chain_active_gamma_count"),
            "candidate_chain_nucleotide_or_metal_residue_count": candidate.get(
                "candidate_chain_nucleotide_or_metal_residue_count"
            ),
            "candidate_chain_has_own_nucleotide_or_metal": candidate.get(
                "candidate_chain_has_own_nucleotide_or_metal"
            ),
            "ligand_chain_active_gamma_count": candidate.get("ligand_chain_active_gamma_count"),
            "polymer_chain_count": features.get("polymer_chain_count"),
            "polymer_entity_count_sequence_proxy": features.get(
                "polymer_entity_count_sequence_proxy"
            ),
            "orientation": compact_orientation(candidate),
            "exposure": compact_exposure(candidate),
            "coordinate_certainty": {
                "coordinate_certainty_status": certainty.get("coordinate_certainty_status"),
                "coordinate_certainty_class": certainty.get("coordinate_certainty_class"),
                "coordinate_certainty_fetch_error": certainty.get("coordinate_certainty_fetch_error"),
                "acceptor_coordinate_certainty": compact_certainty_stats(
                    certainty.get("acceptor_coordinate_certainty")
                ),
                "terminal_gamma_coordinate_certainty": compact_certainty_stats(
                    certainty.get("terminal_gamma_coordinate_certainty")
                ),
            },
        },
        "review_context_for_evaluation_only": {
            "evaluation_label": row["evaluation_label"],
            "evaluation_group": row["evaluation_group"],
            "evaluation_label_used_only_for_eval": row.get("evaluation_label_used_only_for_eval", True),
            "source_artifact_id": row.get("source_artifact_id"),
        },
    }


def state_only_row(row: dict[str, Any], diagnostic_row_index: int) -> dict[str, Any]:
    features = row["structure_features"]
    state = coordinate_state(
        features.get("ligand_state"),
        bool(features.get("terminal_gamma_equivalent_atom_available")),
    )
    blocker = classify_blocker(row, None, state)
    return {
        "row_schema": "epk_candidate_evidence_v1_state_only",
        "candidate_id": f"{row['pdb_id']}|gamma=none|acceptor=none",
        "pdb_id": row["pdb_id"],
        "diagnostic_row_index": diagnostic_row_index,
        "source_free_evidence": {
            "coordinate_state": state,
            "blocker_class": blocker,
            "ligand_state": features.get("ligand_state"),
            "availability_class": row_availability_class(features),
            "terminal_gamma_equivalent_atom_available": features.get(
                "terminal_gamma_equivalent_atom_available"
            ),
            "nearest_protein_hydroxyl_distance_angstrom": features.get(
                "nearest_protein_hydroxyl_distance_angstrom"
            ),
            "candidate_count_within_8a": len(features.get("orientation_enriched_candidates_within_8a", [])),
            "polymer_chain_count": features.get("polymer_chain_count"),
            "polymer_entity_count_sequence_proxy": features.get(
                "polymer_entity_count_sequence_proxy"
            ),
        },
        "review_context_for_evaluation_only": {
            "evaluation_label": row["evaluation_label"],
            "evaluation_group": row["evaluation_group"],
            "evaluation_label_used_only_for_eval": row.get("evaluation_label_used_only_for_eval", True),
            "source_artifact_id": row.get("source_artifact_id"),
        },
    }


def confusion_for_candidate_flag(rows: list[dict[str, Any]], rule_id: str) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    for row in rows:
        evidence = row["source_free_evidence"]
        predicted_positive = (
            evidence["coordinate_state"] == "active_gamma"
            and evidence["blocker_class"] == "none"
        )
        actual_positive = row["review_context_for_evaluation_only"]["evaluation_label"] == (
            "positive_true_substrate_acceptor"
        )
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        buckets[outcome].append(row["candidate_id"])
        decisions.append(
            {
                "candidate_id": row["candidate_id"],
                "pdb_id": row["pdb_id"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "blocker_class": evidence["blocker_class"],
                "coordinate_state": evidence["coordinate_state"],
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": (
            "Candidate-row sanity flag: active-gamma rows with no structural blocker. "
            "This is not a production substrate-role identity rule."
        ),
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": {
            outcome: sorted({candidate_id.split("|", 1)[0] for candidate_id in ids})
            for outcome, ids in buckets.items()
        },
        "candidate_ids_by_outcome": buckets,
        "decisions": decisions,
        "clears_diagnostic_tranche": False,
        "production_claim_allowed": False,
    }


def summarize_counter(rows: list[dict[str, Any]], path: list[str]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value: Any = row
        for key in path:
            value = value.get(key, {}) if isinstance(value, dict) else {}
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def hard_case_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    wanted = {"7B56", "9UUR", "9UUX", "9UW4", "3QHR", "3QHW", "1L0O", "3TM0", "1QHA"}
    result: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["pdb_id"] not in wanted:
            continue
        evidence = row["source_free_evidence"]
        result.setdefault(row["pdb_id"], []).append(
            {
                "candidate_id": row["candidate_id"],
                "coordinate_state": evidence["coordinate_state"],
                "blocker_class": evidence["blocker_class"],
                "candidate_role_class": evidence.get("candidate_role_class"),
                "distance_angstrom": evidence.get("distance_angstrom"),
                "reciprocal_context_class": evidence.get("reciprocal_context_class"),
                "same_chain_topology": evidence.get("same_chain_topology"),
                "coordinate_certainty_class": evidence.get("coordinate_certainty", {}).get(
                    "coordinate_certainty_class"
                ),
            }
        )
    return {key: value for key, value in sorted(result.items())}


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    source_rows = load_source_rows()
    certainty_cache = CoordinateCertaintyCache(workflow_started_at)
    candidate_rows: list[dict[str, Any]] = []
    state_only_rows: list[dict[str, Any]] = []
    for diagnostic_index, row in enumerate(source_rows):
        candidates = row["structure_features"].get("orientation_enriched_candidates_within_8a", [])
        if not candidates:
            state_only_rows.append(state_only_row(row, diagnostic_index))
            continue
        for rank, candidate in enumerate(candidates, start=1):
            candidate_rows.append(evidence_row(row, diagnostic_index, candidate, rank, certainty_cache))

    candidate_ids = [row["candidate_id"] for row in candidate_rows]
    duplicate_candidate_ids = sorted(
        candidate_id for candidate_id, count in Counter(candidate_ids).items() if count > 1
    )
    sanity_rule = confusion_for_candidate_flag(candidate_rows, "candidate_no_blocker_sanity_flag_v1")
    primary_outcome = "candidate_evidence_rows_emitted"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0, 2)
    coordinate_state_counts = summarize_counter(candidate_rows, ["source_free_evidence", "coordinate_state"])
    state_only_coordinate_counts = summarize_counter(
        state_only_rows, ["source_free_evidence", "coordinate_state"]
    )
    blocker_counts = summarize_counter(candidate_rows, ["source_free_evidence", "blocker_class"])
    state_only_blocker_counts = summarize_counter(
        state_only_rows, ["source_free_evidence", "blocker_class"]
    )
    combined_blocker_counter = Counter(blocker_counts)
    combined_blocker_counter.update(state_only_blocker_counts)
    combined_blocker_counts = dict(sorted(combined_blocker_counter.items()))
    certainty_counts = summarize_counter(
        candidate_rows,
        ["source_free_evidence", "coordinate_certainty", "coordinate_certainty_class"],
    )
    hard_rows = hard_case_rows(candidate_rows + state_only_rows)

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "A first-class candidate evidence table can preserve source-free gamma/acceptor "
            "structural evidence and classify blockers without turning review-only source "
            "context into predictive input."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_active_site_orientation_probe": len(source_rows),
            "total": len(source_rows),
        },
        "candidate_evidence_rows_emitted": {
            "candidate_pair_rows": len(candidate_rows),
            "state_only_rows": len(state_only_rows),
            "total_rows_in_artifact": len(candidate_rows) + len(state_only_rows),
            "duplicate_candidate_ids": duplicate_candidate_ids,
        },
        "coordinate_states_observed": {
            "candidate_pair_rows": coordinate_state_counts,
            "state_only_rows": state_only_coordinate_counts,
        },
        "source_free_features_tested": [
            "candidate-level gamma ligand/atom and acceptor residue/atom identity from coordinate records",
            "terminal gamma-equivalent coordinate state taxonomy",
            "gamma-to-hydroxyl distance and candidate rank within 8 A",
            "same-chain/cross-chain topology and same-sequence entity proxy",
            "auth-terminal versus internal-fragment N-terminal acceptor evidence",
            "reciprocal active-gamma context class",
            "local exposure compact counts and open-shell fractions",
            "active-site orientation compact asymmetry counts and angle",
            "candidate-level coordinate certainty: occupancy, altloc count, B-factor ratios",
            "candidate-level blocker class taxonomy",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            sanity_rule["rule_id"]: {
                "rule_description": sanity_rule["rule_description"],
                "confusion_matrix": sanity_rule["confusion_matrix"],
                "pdb_ids_by_outcome": sanity_rule["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": sanity_rule["clears_diagnostic_tranche"],
                "production_claim_allowed": sanity_rule["production_claim_allowed"],
            }
        },
        "confusion_matrix": sanity_rule["confusion_matrix"],
        "decisive_counterexamples": {
            "hard_case_rows": hard_rows,
            "duplicate_candidate_ids": duplicate_candidate_ids,
            "coordinate_certainty_counts": certainty_counts,
            "candidate_pair_blocker_counts": blocker_counts,
            "state_only_blocker_counts": state_only_blocker_counts,
            "combined_blocker_counts": combined_blocker_counts,
        },
        "false_positive_analysis": {
            "candidate_no_blocker_sanity_flag_false_positive_pdb_ids": sanity_rule[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "interpretation": (
                "The candidate evidence table is intentionally not a production rule. "
                "No-blocker candidate flags remain evaluation-only sanity checks; source-free "
                "candidate evidence alone still cannot assign biological substrate role in "
                "ambiguous topology families."
            ),
        },
        "false_negative_analysis": {
            "candidate_no_blocker_sanity_flag_false_negative_pdb_ids": sanity_rule[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "state_only_positive_rows": [
                row["pdb_id"]
                for row in state_only_rows
                if row["review_context_for_evaluation_only"]["evaluation_label"]
                == "positive_true_substrate_acceptor"
            ],
            "interpretation": (
                "Product/ADP positives have state-only evidence rather than active terminal "
                "gamma transfer geometry, and reciprocal/same-chain positives retain "
                "topology or substrate-role identity blockers."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "candidate_pair_blocker_counts": blocker_counts,
            "state_only_blocker_counts": state_only_blocker_counts,
            "combined_blocker_counts": combined_blocker_counts,
            "classification": (
                "Candidate rows make the blocker explicit: active-gamma geometry and "
                "coordinate certainty are source-free structural evidence, but topology "
                "and substrate-role identity blockers remain review-only biology ambiguity."
            ),
            "hard_case_assessment": (
                "7B56 remains internal-fragment mimicry, 9UUR/9UUX/9UW4 remain reciprocal "
                "folded-chain topology ambiguity, product/ADP rows are state-specific "
                "review-only evidence, and 3TM0 remains same-chain/autophosphorylation-like."
            ),
        },
        "next_query": (
            "Use the candidate evidence table for review triage and blocker reporting; do "
            "not add more scalar source-free probes unless a genuinely new evidence modality "
            "is introduced."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Preserve candidate-level source-free "
            "evidence rows as review-only substrate-role identity support and keep "
            "source-reviewed adjudication for product/ADP, reciprocal folded-chain, and "
            "same-chain/autophosphorylation-like cases."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "candidate_level_source_free_gamma_acceptor_evidence_rows",
            "review_only": True,
            "source_free_evidence_separated_from_review_context": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifact": str(SOURCE_ARTIFACT),
            "output_path": str(output_path),
            "diagnostic_row_count": len(source_rows),
            "candidate_pair_row_count": len(candidate_rows),
            "state_only_row_count": len(state_only_rows),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "candidate_id": (
                "PDB plus terminal gamma ligand atom and protein hydroxyl acceptor atom. "
                "State-only rows use gamma=none and acceptor=none when no gamma/acceptor "
                "pair is materialized."
            ),
            "coordinate_state": (
                "First-class source-free resolved coordinate state inferred from compact "
                "ligand atom availability, not from title, prose, mechanism labels, or "
                "curated substrate names."
            ),
            "blocker_class": (
                "Candidate-level blocker taxonomy used for review triage; not a production "
                "substrate-role identity decision."
            ),
        },
        "coordinate_state_counts": {
            "candidate_pair_rows": coordinate_state_counts,
            "state_only_rows": state_only_coordinate_counts,
        },
        "blocker_class_counts": blocker_counts,
        "state_only_blocker_class_counts": state_only_blocker_counts,
        "combined_blocker_class_counts": combined_blocker_counts,
        "coordinate_certainty_counts": certainty_counts,
        "candidate_evidence_rows": candidate_rows,
        "state_only_rows": state_only_rows,
        "rules": [sanity_rule],
        "run_record": run_record,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--git-sync-status", required=True)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    payload = build_payload(args.workflow_started_at, args.git_sync_status, output_path)
    write_json(output_path, payload)
    if args.append_ledger:
        append_jsonl(LEDGER_PATH, payload["run_record"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
