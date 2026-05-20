#!/usr/bin/env python3
"""Review-only ePK active-site orientation/asymmetry probe.

This lane-local helper tests whether source-free geometry around the selected
hydroxyl, nucleotide gamma atom, and nearby protein density can distinguish
true kinase substrate phosphoacceptors from structural mimics. Coordinates are
fetched in memory only; output is compact reduced evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    append_jsonl,
    utc_now,
    write_json,
)
from substrate_role_identity_eval import (
    ACTIVE_GAMMA_CODES,
    METAL_CODES,
    NUCLEOTIDE_LIKE_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_active_site_orientation_asymmetry_probe_v1_20260520"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_local_burial_solvent_exposure_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_active_site_orientation_asymmetry_probe_v1_20260520.json"
)

ANCHOR_BY_HYDROXYL = {
    ("SER", "OG"): "CB",
    ("THR", "OG1"): "CB",
    ("TYR", "OH"): "CZ",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def fetch_pdb_text_with_retries(pdb_id: str, attempts: int = 3) -> tuple[str | None, str | None]:
    last_error = None
    for attempt in range(1, attempts + 1):
        text, error = fetch_pdb_text(pdb_id)
        if text is not None:
            return text, None
        last_error = error
        if attempt < attempts:
            time.sleep(2 * attempt)
    return None, last_error


def compact_key(compact_atom: dict[str, Any] | None) -> tuple[str, str, str, str, str] | None:
    if not compact_atom:
        return None
    return (
        compact_atom["atom_name"],
        compact_atom["residue_code"],
        compact_atom["chain_id"],
        compact_atom["auth_seq_id"],
        compact_atom.get("icode") or "",
    )


def atom_key(atom: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        atom["atom_name"],
        atom["resname"],
        atom["chain"],
        atom["resseq"],
        atom["icode"] or "",
    )


def find_atom(atoms: list[dict[str, Any]], compact_atom: dict[str, Any] | None) -> dict[str, Any] | None:
    key = compact_key(compact_atom)
    if key is None:
        return None
    for atom in atoms:
        if atom_key(atom) == key:
            return atom
    return None


def heavy(atom: dict[str, Any]) -> bool:
    return atom["element"] != "H"


def vector(a: dict[str, Any], b: dict[str, Any]) -> tuple[float, float, float]:
    return (b["x"] - a["x"], b["y"] - a["y"], b["z"] - a["z"])


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a: tuple[float, float, float]) -> float:
    return math.sqrt(dot(a, a))


def unit(a: tuple[float, float, float]) -> tuple[float, float, float] | None:
    length = norm(a)
    if length == 0:
        return None
    return (a[0] / length, a[1] / length, a[2] / length)


def angle_degrees(a: tuple[float, float, float], b: tuple[float, float, float]) -> float | None:
    a_len = norm(a)
    b_len = norm(b)
    if a_len == 0 or b_len == 0:
        return None
    cosine = max(-1.0, min(1.0, dot(a, b) / (a_len * b_len)))
    return round(math.degrees(math.acos(cosine)), 3)


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def attached_anchor_atom(acceptor_atom: dict[str, Any] | None, atoms: list[dict[str, Any]]) -> dict[str, Any] | None:
    if acceptor_atom is None:
        return None
    expected_name = ANCHOR_BY_HYDROXYL.get((acceptor_atom["resname"], acceptor_atom["atom_name"]))
    same_residue = [
        atom
        for atom in atoms
        if atom["record"] == "ATOM"
        and atom["residue_key"] == acceptor_atom["residue_key"]
        and heavy(atom)
        and atom is not acceptor_atom
    ]
    if expected_name:
        for atom in same_residue:
            if atom["atom_name"] == expected_name:
                return atom
    if not same_residue:
        return None
    return min(same_residue, key=lambda atom: dist(atom, acceptor_atom))


def count_atoms_in_radius(
    center: dict[str, Any],
    atoms: list[dict[str, Any]],
    radius: float,
) -> int:
    return sum(1 for atom in atoms if dist(center, atom) <= radius)


def nearest_distance(center: dict[str, Any], atoms: list[dict[str, Any]]) -> float | None:
    best: float | None = None
    for atom in atoms:
        current = dist(center, atom)
        if best is None or current < best:
            best = current
    return round_or_none(best)


def halfspace_counts(
    center: dict[str, Any],
    axis_unit: tuple[float, float, float] | None,
    atoms: list[dict[str, Any]],
    radius: float,
) -> dict[str, Any]:
    if axis_unit is None:
        return {
            "total": 0,
            "positive_halfspace": 0,
            "negative_halfspace": 0,
            "asymmetry_index": None,
        }
    positive = 0
    negative = 0
    for atom in atoms:
        if dist(center, atom) > radius:
            continue
        projection = dot(vector(center, atom), axis_unit)
        if projection >= 0:
            positive += 1
        else:
            negative += 1
    total = positive + negative
    return {
        "total": total,
        "positive_halfspace": positive,
        "negative_halfspace": negative,
        "asymmetry_index": round((positive - negative) / total, 3) if total else None,
    }


def orientation_support_class(features: dict[str, Any]) -> str:
    if features["orientation_status"] != "ok":
        return "unavailable"
    angle = features["hydroxyl_anchor_to_gamma_angle_degrees"]
    gamma_facing_other = features[
        "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a_excluding_same_residue"
    ]
    gamma_site_ligand = features["gamma_site_ligand_chain_heavy_atom_count_within_6a"]
    if angle is None:
        return "unavailable"
    if 70.0 <= angle <= 170.0 and gamma_facing_other >= 4 and gamma_site_ligand >= 8:
        return "gamma_facing_active_site_like"
    if angle < 45.0 or gamma_facing_other == 0:
        return "orientation_unsupported"
    return "intermediate"


def orientation_features(
    candidate: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    if candidate is None:
        return {
            "orientation_status": "candidate_unavailable",
            "orientation_support_class": "unavailable",
        }
    gamma_atom = find_atom(atoms, candidate.get("terminal_gamma_equivalent_atom"))
    acceptor_atom = find_atom(atoms, candidate.get("nearest_protein_hydroxyl_atom"))
    anchor_atom = attached_anchor_atom(acceptor_atom, atoms)
    if gamma_atom is None or acceptor_atom is None:
        return {
            "orientation_status": "gamma_or_acceptor_atom_not_resolved",
            "orientation_support_class": "unavailable",
        }

    atom_atoms = [atom for atom in atoms if atom["record"] == "ATOM" and heavy(atom)]
    hetero_atoms = [atom for atom in atoms if atom["record"] == "HETATM" and heavy(atom)]
    acceptor_residue_key = acceptor_atom["residue_key"]
    gamma_residue_key = gamma_atom["residue_key"]
    acceptor_chain = acceptor_atom["chain"]
    ligand_chain = gamma_atom["chain"]

    protein_excluding_acceptor_residue = [
        atom for atom in atom_atoms if atom["residue_key"] != acceptor_residue_key
    ]
    other_chain_protein = [
        atom for atom in protein_excluding_acceptor_residue if atom["chain"] != acceptor_chain
    ]
    ligand_chain_protein = [
        atom for atom in protein_excluding_acceptor_residue if atom["chain"] == ligand_chain
    ]
    acceptor_chain_protein = [
        atom for atom in protein_excluding_acceptor_residue if atom["chain"] == acceptor_chain
    ]
    gamma_site_protein = [
        atom
        for atom in atom_atoms
        if atom["residue_key"] != acceptor_residue_key and atom["chain"] != ligand_chain
    ]
    gamma_site_ligand_chain_protein = [
        atom
        for atom in atom_atoms
        if atom["chain"] == ligand_chain and atom["residue_key"] != acceptor_residue_key
    ]
    gamma_site_acceptor_chain_protein = [
        atom
        for atom in atom_atoms
        if atom["chain"] == acceptor_chain and atom["residue_key"] != acceptor_residue_key
    ]
    nonwater_nucleotide_or_metal = [
        atom
        for atom in hetero_atoms
        if atom["residue_key"] != gamma_residue_key
        and (atom["resname"] in NUCLEOTIDE_LIKE_CODES or atom["resname"] in METAL_CODES)
    ]
    other_gamma_atoms = [
        atom
        for atom in hetero_atoms
        if atom["residue_key"] != gamma_residue_key
        and atom["resname"] in ACTIVE_GAMMA_CODES
        and atom["atom_name"] in {"PG", "P3"}
    ]

    o_to_gamma_unit = unit(vector(acceptor_atom, gamma_atom))
    gamma_to_o_unit = unit(vector(gamma_atom, acceptor_atom))
    gamma_facing_all = halfspace_counts(
        acceptor_atom, o_to_gamma_unit, protein_excluding_acceptor_residue, 6.0
    )
    gamma_facing_other = halfspace_counts(acceptor_atom, o_to_gamma_unit, other_chain_protein, 6.0)
    gamma_facing_ligand = halfspace_counts(acceptor_atom, o_to_gamma_unit, ligand_chain_protein, 6.0)
    gamma_facing_acceptor = halfspace_counts(
        acceptor_atom, o_to_gamma_unit, acceptor_chain_protein, 6.0
    )
    gamma_axis_ligand = halfspace_counts(gamma_atom, gamma_to_o_unit, gamma_site_ligand_chain_protein, 6.0)
    gamma_axis_acceptor = halfspace_counts(
        gamma_atom, gamma_to_o_unit, gamma_site_acceptor_chain_protein, 6.0
    )

    anchor_angle = None
    anchor_distance = None
    if anchor_atom is not None:
        anchor_angle = angle_degrees(vector(acceptor_atom, anchor_atom), vector(acceptor_atom, gamma_atom))
        anchor_distance = round_or_none(dist(anchor_atom, acceptor_atom))

    gamma_site_total = count_atoms_in_radius(gamma_atom, gamma_site_protein, 6.0)
    gamma_site_ligand_total = count_atoms_in_radius(gamma_atom, gamma_site_ligand_chain_protein, 6.0)
    gamma_site_acceptor_total = count_atoms_in_radius(gamma_atom, gamma_site_acceptor_chain_protein, 6.0)
    density_ratio = None
    if gamma_site_acceptor_total or gamma_site_ligand_total:
        density_ratio = round(
            gamma_site_acceptor_total / max(1, gamma_site_ligand_total),
            3,
        )

    features = {
        "orientation_status": "ok",
        "hydroxyl_anchor_atom_name": anchor_atom["atom_name"] if anchor_atom else None,
        "hydroxyl_anchor_distance_angstrom": anchor_distance,
        "hydroxyl_anchor_to_gamma_angle_degrees": anchor_angle,
        "gamma_to_hydroxyl_distance_angstrom": round_or_none(dist(gamma_atom, acceptor_atom)),
        "hydroxyl_gamma_facing_protein_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_all[
            "positive_halfspace"
        ],
        "hydroxyl_backside_protein_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_all[
            "negative_halfspace"
        ],
        "hydroxyl_gamma_facing_asymmetry_index_within_6a": gamma_facing_all["asymmetry_index"],
        "hydroxyl_gamma_facing_other_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_other[
            "positive_halfspace"
        ],
        "hydroxyl_backside_other_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_other[
            "negative_halfspace"
        ],
        "hydroxyl_gamma_facing_ligand_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_ligand[
            "positive_halfspace"
        ],
        "hydroxyl_backside_ligand_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_ligand[
            "negative_halfspace"
        ],
        "hydroxyl_gamma_facing_acceptor_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_acceptor[
            "positive_halfspace"
        ],
        "hydroxyl_backside_acceptor_chain_heavy_atom_count_within_6a_excluding_same_residue": gamma_facing_acceptor[
            "negative_halfspace"
        ],
        "gamma_site_protein_heavy_atom_count_within_6a_excluding_ligand": gamma_site_total,
        "gamma_site_ligand_chain_heavy_atom_count_within_6a": gamma_site_ligand_total,
        "gamma_site_acceptor_chain_heavy_atom_count_within_6a_excluding_acceptor_residue": gamma_site_acceptor_total,
        "gamma_site_acceptor_to_ligand_density_ratio_within_6a": density_ratio,
        "gamma_site_ligand_chain_forward_axis_count_within_6a": gamma_axis_ligand["positive_halfspace"],
        "gamma_site_ligand_chain_back_axis_count_within_6a": gamma_axis_ligand["negative_halfspace"],
        "gamma_site_acceptor_chain_forward_axis_count_within_6a": gamma_axis_acceptor["positive_halfspace"],
        "gamma_site_acceptor_chain_back_axis_count_within_6a": gamma_axis_acceptor["negative_halfspace"],
        "nearest_other_nucleotide_or_metal_distance_to_hydroxyl_angstrom": nearest_distance(
            acceptor_atom, nonwater_nucleotide_or_metal
        ),
        "nearest_other_active_gamma_distance_to_hydroxyl_angstrom": nearest_distance(
            acceptor_atom, other_gamma_atoms
        ),
    }
    features["orientation_support_class"] = orientation_support_class(features)
    return features


def enrich_candidate(candidate: dict[str, Any] | None, atoms: list[dict[str, Any]]) -> dict[str, Any] | None:
    if candidate is None:
        return None
    enriched = deepcopy(candidate)
    enriched["active_site_orientation_features"] = orientation_features(candidate, atoms)
    return enriched


def load_source_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    return payload["diagnostic_rows"]


def enrich_row(row: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text_with_retries(row["pdb_id"])
    source_features = row["structure_features"]
    base_features = deepcopy(source_features)
    if text is None:
        base_features.update(
            {
                "active_site_orientation_fetch_status": "error",
                "active_site_orientation_fetch_error": fetch_error,
                "orientation_enriched_candidates_within_8a": [],
                "nearest_strict_cross_chain_candidate": None,
                "nearest_strict_auth_terminal_guard_candidate": None,
                "nearest_reciprocal_folded_tyr_rescue_candidate": None,
            }
        )
    else:
        atoms = parse_pdb_atoms(text)
        orientation_candidates = [
            enrich_candidate(candidate, atoms)
            for candidate in source_features.get("local_exposure_candidates_within_8a", [])
        ]
        orientation_candidates = [candidate for candidate in orientation_candidates if candidate is not None]
        base_features.update(
            {
                "active_site_orientation_fetch_status": "ok",
                "active_site_orientation_fetch_error": None,
                "orientation_enriched_candidates_within_8a": orientation_candidates,
                "nearest_strict_cross_chain_candidate": enrich_candidate(
                    source_features.get("nearest_strict_cross_chain_candidate"), atoms
                ),
                "nearest_strict_auth_terminal_guard_candidate": enrich_candidate(
                    source_features.get("nearest_strict_auth_terminal_guard_candidate"), atoms
                ),
                "nearest_reciprocal_folded_tyr_rescue_candidate": enrich_candidate(
                    source_features.get("nearest_reciprocal_folded_tyr_rescue_candidate"), atoms
                ),
            }
        )

    return {
        "pdb_id": row["pdb_id"],
        "evaluation_label": row["evaluation_label"],
        "evaluation_group": row["evaluation_group"],
        "evaluation_label_source": row.get("evaluation_label_source"),
        "evaluation_label_used_only_for_eval": True,
        "source_artifact_id": row.get("source_artifact_id"),
        "feature_extraction_started_after": workflow_started_at,
        "source_free_feature_only": True,
        "forbidden_predictive_features_excluded": FORBIDDEN_PREDICTIVE_FEATURES,
        "fetch_status": row.get("fetch_status"),
        "fetch_error": row.get("fetch_error"),
        "pdb_sha256_12": row.get("pdb_sha256_12"),
        "atom_count_model1": row.get("atom_count_model1"),
        "structure_features": base_features,
    }


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def orientation_class(candidate: dict[str, Any] | None) -> str | None:
    if not candidate:
        return None
    return candidate.get("active_site_orientation_features", {}).get("orientation_support_class")


def rule_strict_baseline(features: dict[str, Any]) -> bool:
    return bool(features.get("nearest_strict_cross_chain_candidate"))


def rule_auth_guard(features: dict[str, Any]) -> bool:
    return bool(features.get("nearest_strict_auth_terminal_guard_candidate"))


def rule_permissive(features: dict[str, Any]) -> bool:
    distance = features["nearest_protein_hydroxyl_distance_angstrom"]
    return bool(features["terminal_gamma_equivalent_atom_available"] and distance is not None and distance <= 6.0)


def rule_reciprocal_folded_tyr_rescue(features: dict[str, Any]) -> bool:
    return bool(
        features.get("nearest_strict_auth_terminal_guard_candidate")
        or features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
    )


def rule_orientation_supported_folded_tyr_rescue(features: dict[str, Any]) -> bool:
    if features.get("nearest_strict_auth_terminal_guard_candidate"):
        return True
    candidate = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
    return bool(candidate and orientation_class(candidate) == "gamma_facing_active_site_like")


def rule_orientation_guarded_auth_strict(features: dict[str, Any]) -> bool:
    candidate = features.get("nearest_strict_auth_terminal_guard_candidate")
    return bool(candidate and orientation_class(candidate) != "orientation_unsupported")


RULES = {
    "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1": {
        "description": "Existing strict source-free rule reused as baseline.",
        "function": rule_strict_baseline,
    },
    "strict_auth_terminal_guard_v1": {
        "description": "Existing strict rule plus source-free auth-terminal guard, reused as baseline.",
        "function": rule_auth_guard,
    },
    "permissive_nearest_hydroxyl_6a_v1": {
        "description": "PG/P3 gamma-equivalent present and nearest protein Ser/Thr/Tyr hydroxyl <=6.0 A.",
        "function": rule_permissive,
    },
    "reciprocal_folded_tyr_rescue_v1": {
        "description": "Prior reciprocal folded-Tyr rescue rule reused as the hard counterexample baseline.",
        "function": rule_reciprocal_folded_tyr_rescue,
    },
    "orientation_supported_folded_tyr_rescue_v1": {
        "description": (
            "Auth-guard strict positives plus reciprocal folded-Tyr rescue candidates "
            "whose source-free hydroxyl angle and active-site half-space density are "
            "gamma_facing_active_site_like."
        ),
        "function": rule_orientation_supported_folded_tyr_rescue,
    },
    "orientation_guarded_auth_strict_v1": {
        "description": (
            "Auth-guard strict positives rejected only when the selected hydroxyl has "
            "orientation_unsupported geometry."
        ),
        "function": rule_orientation_guarded_auth_strict,
    },
}


def classify_failure(row: dict[str, Any], predicted_positive: bool, rule_id: str) -> str | None:
    if predicted_positive == is_positive(row):
        return None
    features = row["structure_features"]
    if not features["terminal_gamma_equivalent_atom_available"]:
        if features["ligand_state"] and features["ligand_state"].startswith("nucleotide_like_without_terminal_gamma"):
            return "product_or_analog_state"
        return "structure_missing_gamma_equivalent"
    if predicted_positive and not is_positive(row):
        if rule_id in {
            "reciprocal_folded_tyr_rescue_v1",
            "orientation_supported_folded_tyr_rescue_v1",
        } and features.get("nearest_reciprocal_folded_tyr_rescue_candidate"):
            return "folded_tyr_orientation_counterexample"
        strict_candidate = features.get("nearest_strict_cross_chain_candidate")
        if strict_candidate and strict_candidate.get("candidate_resolved_n_terminal_internal_fragment_like"):
            return "internal_fragment_n_terminal_mimicry"
        if features.get("nearest_protein_hydroxyl_distance_angstrom") is not None:
            return "nearest_hydroxyl_role_ambiguity"
        return "biological_role_ambiguity"
    if is_positive(row) and not predicted_positive:
        rescue_candidate = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
        if rescue_candidate and rule_id == "orientation_supported_folded_tyr_rescue_v1":
            if orientation_class(rescue_candidate) != "gamma_facing_active_site_like":
                return "orientation_rule_rejected_folded_tyr_positive"
        if rescue_candidate:
            return "reciprocal_catalytic_context_ambiguity"
        candidates = features.get("orientation_enriched_candidates_within_8a", [])
        if any(candidate.get("same_chain_topology") for candidate in candidates):
            return "same_chain_or_autophosphorylation_like_topology"
        if any(
            candidate.get("reciprocal_context_class")
            in {
                "reciprocal_active_gamma_different_entity",
                "reciprocal_nucleotide_or_metal_different_entity",
            }
            for candidate in candidates
        ):
            return "reciprocal_catalytic_context_ambiguity"
        return "method_weakness"
    return "method_weakness"


def confusion_for_rule(rows: list[dict[str, Any]], rule_id: str, rule_spec: dict[str, Any]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    decisions = []
    failure_counts: Counter[str] = Counter()
    for row in rows:
        predicted_positive = bool(rule_spec["function"](row["structure_features"]))
        actual_positive = is_positive(row)
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        failure_mode = classify_failure(row, predicted_positive, rule_id)
        if failure_mode:
            failure_counts[failure_mode] += 1
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "failure_mode": failure_mode,
            }
        )
    return {
        "rule_id": rule_id,
        "rule_description": rule_spec["description"],
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "pdb_ids_by_outcome": buckets,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
    }


def selected_candidate_for_probe(row: dict[str, Any]) -> dict[str, Any] | None:
    features = row["structure_features"]
    return (
        features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
        or features.get("nearest_strict_auth_terminal_guard_candidate")
        or features.get("nearest_strict_cross_chain_candidate")
    )


def orientation_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_counts: Counter[str] = Counter()
    selected_counts: Counter[str] = Counter()
    row_presence_by_label: dict[str, Counter[str]] = {
        "positive": Counter(),
        "counterexample": Counter(),
    }
    for row in rows:
        label = "positive" if is_positive(row) else "counterexample"
        seen = set()
        for candidate in row["structure_features"].get("orientation_enriched_candidates_within_8a", []):
            cls = orientation_class(candidate) or "unavailable"
            candidate_counts[cls] += 1
            seen.add(cls)
        for cls in seen:
            row_presence_by_label[label][cls] += 1
        selected_cls = orientation_class(selected_candidate_for_probe(row))
        if selected_cls:
            selected_counts[selected_cls] += 1
    return {
        "candidate_orientation_class_counts": dict(sorted(candidate_counts.items())),
        "selected_candidate_orientation_class_counts": dict(sorted(selected_counts.items())),
        "row_orientation_class_presence_by_label": {
            label: dict(sorted(counter.items())) for label, counter in row_presence_by_label.items()
        },
    }


def probe_rows(rows: list[dict[str, Any]], pdb_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {row["pdb_id"]: row for row in rows}
    probes = []
    for pdb_id in pdb_ids:
        row = by_id[pdb_id]
        features = row["structure_features"]
        selected = selected_candidate_for_probe(row)
        probes.append(
            {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "ligand_state": features["ligand_state"],
                "nearest_distance_angstrom": features["nearest_protein_hydroxyl_distance_angstrom"],
                "selected_candidate": selected,
                "nearest_orientation_candidates_within_8a": [
                    {
                        "distance_angstrom": candidate["distance_angstrom"],
                        "terminal_gamma_ligand_chain": candidate["terminal_gamma_ligand_chain"],
                        "candidate_acceptor_chain": candidate["candidate_acceptor_chain"],
                        "candidate_acceptor_residue_code": candidate["candidate_acceptor_residue_code"],
                        "candidate_acceptor_auth_seq_id_int": candidate.get(
                            "candidate_acceptor_auth_seq_id_int"
                        ),
                        "reciprocal_context_class": candidate.get("reciprocal_context_class"),
                        "local_exposure_profile_class": candidate.get("local_exposure_features", {}).get(
                            "local_exposure_profile_class"
                        ),
                        "active_site_orientation_features": candidate.get(
                            "active_site_orientation_features"
                        ),
                    }
                    for candidate in features.get("orientation_enriched_candidates_within_8a", [])[:4]
                ],
            }
        )
    return probes


def remaining_false_negative_probe(rows: list[dict[str, Any]], false_negative_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {row["pdb_id"]: row for row in rows}
    probes = []
    for pdb_id in false_negative_ids:
        row = by_id[pdb_id]
        features = row["structure_features"]
        candidates = features.get("orientation_enriched_candidates_within_8a", [])
        nearest_candidate = candidates[0] if candidates else None
        probes.append(
            {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "ligand_state": features.get("ligand_state"),
                "terminal_gamma_equivalent_atom_available": features.get(
                    "terminal_gamma_equivalent_atom_available"
                ),
                "nearest_protein_hydroxyl_distance_angstrom": features.get(
                    "nearest_protein_hydroxyl_distance_angstrom"
                ),
                "polymer_chain_count": features.get("polymer_chain_count"),
                "polymer_entity_count_sequence_proxy": features.get(
                    "polymer_entity_count_sequence_proxy"
                ),
                "candidate_count_within_8a": len(candidates),
                "nearest_candidate_topology": None
                if nearest_candidate is None
                else {
                    "distance_angstrom": nearest_candidate.get("distance_angstrom"),
                    "same_chain_topology": nearest_candidate.get("same_chain_topology"),
                    "cross_chain_topology": nearest_candidate.get("cross_chain_topology"),
                    "candidate_acceptor_residue_code": nearest_candidate.get(
                        "candidate_acceptor_residue_code"
                    ),
                    "candidate_acceptor_chain_length": nearest_candidate.get(
                        "candidate_acceptor_chain_length"
                    ),
                    "candidate_acceptor_chain_is_short_peptide_like": nearest_candidate.get(
                        "candidate_acceptor_chain_is_short_peptide_like"
                    ),
                    "candidate_acceptor_chain_is_folded_like": nearest_candidate.get(
                        "candidate_acceptor_chain_is_folded_like"
                    ),
                    "reciprocal_context_class": nearest_candidate.get("reciprocal_context_class"),
                    "orientation_support_class": orientation_class(nearest_candidate),
                },
            }
        )
    return probes


def posthoc_threshold_projection(
    rows: list[dict[str, Any]],
    feature: str,
    direction: str,
    threshold: float,
) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    for row in rows:
        features = row["structure_features"]
        candidate = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
        passes_threshold = False
        if candidate:
            value = candidate.get("active_site_orientation_features", {}).get(feature)
            if isinstance(value, (int, float)):
                passes_threshold = value >= threshold if direction == "at_or_above" else value <= threshold
        predicted_positive = bool(
            features.get("nearest_strict_auth_terminal_guard_candidate")
            or (candidate and passes_threshold)
        )
        actual_positive = is_positive(row)
        if predicted_positive and actual_positive:
            outcome = "true_positive"
        elif predicted_positive and not actual_positive:
            outcome = "false_positive"
        elif not predicted_positive and actual_positive:
            outcome = "false_negative"
        else:
            outcome = "true_negative"
        buckets[outcome].append(row["pdb_id"])
    return {
        "confusion_matrix": {
            "true_positive": len(buckets["true_positive"]),
            "false_positive": len(buckets["false_positive"]),
            "true_negative": len(buckets["true_negative"]),
            "false_negative": len(buckets["false_negative"]),
        },
        "false_positive": buckets["false_positive"],
        "false_negative": buckets["false_negative"],
    }


def trio_separability_scan(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {row["pdb_id"]: row for row in rows}
    positive_ids = ["9UUR", "9UUX"]
    counterexample_id = "9UW4"
    candidate_features: dict[str, dict[str, Any]] = {}
    for pdb_id in [*positive_ids, counterexample_id]:
        candidate = selected_candidate_for_probe(by_id[pdb_id])
        candidate_features[pdb_id] = (
            candidate.get("active_site_orientation_features", {}) if candidate else {}
        )

    outside_positive_range = []
    common_keys = set(candidate_features[counterexample_id])
    for pdb_id in positive_ids:
        common_keys &= set(candidate_features[pdb_id])
    for key in sorted(common_keys):
        values = [candidate_features[pdb_id][key] for pdb_id in positive_ids]
        counter_value = candidate_features[counterexample_id][key]
        if not all(isinstance(value, (int, float)) for value in [*values, counter_value]):
            continue
        positive_min = min(values)
        positive_max = max(values)
        if counter_value < positive_min or counter_value > positive_max:
            if counter_value < positive_min:
                threshold = round((counter_value + positive_min) / 2, 3)
                direction = "at_or_above"
            else:
                threshold = round((counter_value + positive_max) / 2, 3)
                direction = "at_or_below"
            outside_positive_range.append(
                {
                    "feature": key,
                    "positive_values": dict(zip(positive_ids, values)),
                    "positive_min": positive_min,
                    "positive_max": positive_max,
                    "counterexample_value": counter_value,
                    "direction": "below_positive_range"
                    if counter_value < positive_min
                    else "above_positive_range",
                    "posthoc_threshold_not_for_prediction": {
                        "direction": direction,
                        "threshold": threshold,
                        "projection_on_54_rows": posthoc_threshold_projection(
                            rows, key, direction, threshold
                        ),
                    },
                }
            )
    return {
        "positive_ids": positive_ids,
        "counterexample_id": counterexample_id,
        "candidate_features": candidate_features,
        "features_where_9uw4_outside_two_positive_range": outside_positive_range,
        "interpretation": (
            "The scan is diagnostic only. Any scalar split discovered against the "
            "same hard trio is post-hoc candidate-specific tuning and is excluded "
            "from accepted predictive rules."
        ),
    }


def select_primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    orientation_rescue = next(
        result
        for result in rule_results
        if result["rule_id"] == "orientation_supported_folded_tyr_rescue_v1"
    )
    if orientation_rescue["failure_mode_counts"].get("folded_tyr_orientation_counterexample"):
        return "counterexample_found"
    if (
        orientation_rescue["failure_mode_counts"].get("orientation_rule_rejected_folded_tyr_positive")
        or orientation_rescue["failure_mode_counts"].get("reciprocal_catalytic_context_ambiguity")
    ):
        return "blocker_not_cleared_biology_ambiguity"
    return "blocker_not_cleared_method_weakness"


def build_payload(workflow_started_at: str, ledger_started_at: str | None = None) -> dict[str, Any]:
    source_rows = load_source_rows()
    rows = [enrich_row(row, workflow_started_at) for row in source_rows]
    rule_results = [confusion_for_rule(rows, rule_id, rule_spec) for rule_id, rule_spec in RULES.items()]
    orientation_fetch_counts = Counter(
        row["structure_features"]["active_site_orientation_fetch_status"] for row in rows
    )
    all_orientation_fetch_failed = orientation_fetch_counts.get("ok", 0) == 0
    primary_outcome = (
        "blocker_not_cleared_data_scarcity"
        if all_orientation_fetch_failed
        else select_primary_outcome(rule_results)
    )
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    strict = next(
        result
        for result in rule_results
        if result["rule_id"] == "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1"
    )
    auth = next(result for result in rule_results if result["rule_id"] == "strict_auth_terminal_guard_v1")
    reciprocal = next(
        result for result in rule_results if result["rule_id"] == "reciprocal_folded_tyr_rescue_v1"
    )
    orientation_rescue = next(
        result for result in rule_results if result["rule_id"] == "orientation_supported_folded_tyr_rescue_v1"
    )
    orientation_guard = next(
        result for result in rule_results if result["rule_id"] == "orientation_guarded_auth_strict_v1"
    )
    ended_at = utc_now()
    started_for_measure = ledger_started_at or workflow_started_at
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_for_measure)).total_seconds() / 60.0, 2)
    false_positive_ids = sorted(
        {
            pdb_id
            for result in rule_results
            for pdb_id in result["pdb_ids_by_outcome"]["false_positive"]
        }
    )
    false_negative_ids = sorted(
        {
            pdb_id
            for result in rule_results
            for pdb_id in result["pdb_ids_by_outcome"]["false_negative"]
        }
    )

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_active_site_orientation_asymmetry_probe",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifact": str(SOURCE_ARTIFACT),
            "frozen_row_count": len(rows),
            "materialized_row_count": sum(1 for row in rows if row["fetch_status"] == "ok"),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "active_site_orientation_fetch_status_counts": dict(sorted(orientation_fetch_counts.items())),
            "all_orientation_fetch_failed": all_orientation_fetch_failed,
            "primary_outcome": primary_outcome,
        },
        "hypothesis": (
            "If substrate-role identity is encoded by source-free active-site geometry, then "
            "true acceptor hydroxyls should show a gamma-facing sidechain orientation and "
            "asymmetric catalytic-chain density that recovers folded Tyr positives while "
            "rejecting topology-confounded mimics such as 9UW4."
        ),
        "feature_definitions": {
            "hydroxyl_anchor_to_gamma_angle_degrees": (
                "Angle at the candidate hydroxyl between the hydroxyl-to-anchor vector "
                "(Ser/Thr CB or Tyr CZ) and the hydroxyl-to-gamma vector."
            ),
            "hydroxyl_halfspace_counts": (
                "Protein heavy atoms within 6 A of the hydroxyl split into gamma-facing "
                "and backside half-spaces along the hydroxyl-to-gamma axis."
            ),
            "gamma_site_density": (
                "Protein heavy atoms within 6 A of the nucleotide gamma split by ligand "
                "chain, acceptor chain, and other chains; no titles or labels are used."
            ),
            "orientation_support_class": (
                "Frozen descriptive class: gamma_facing_active_site_like when the hydroxyl "
                "anchor angle is 70-170 degrees, at least 4 other-chain heavy atoms are "
                "gamma-facing within 6 A, and at least 8 ligand-chain protein heavy atoms "
                "occupy the catalytic gamma site within 6 A; orientation_unsupported when angle <45 "
                "or no other-chain atom is gamma-facing; otherwise intermediate."
            ),
        },
        "diagnostic_rows": rows,
        "rules": rule_results,
        "orientation_summary": orientation_summary(rows),
        "trio_separability_scan": trio_separability_scan(rows),
        "counterexample_probe": probe_rows(
            rows, ["9UUR", "9UUX", "9UW4", "7B56", "3QHR", "3QHW", "1L0O", "3TM0"]
        ),
        "remaining_false_negative_probe": remaining_false_negative_probe(
            rows, orientation_rescue["pdb_ids_by_outcome"]["false_negative"]
        ),
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "orientation_signal": (
                "The frozen active-site orientation support class is review-only context; "
                "it does not establish a complete source-free substrate-role identity rule "
                "on the 54-row diagnostic set."
            ),
            "counterexample_signal": (
                "The hard comparison remains the reciprocal folded-Tyr trio 9UUR/9UUX/9UW4; "
                "if 9UW4 shares the same accepted orientation class as positives, active-site "
                "orientation is insufficient without source-reviewed adjudication."
            ),
            "historical_comparator_assessment": (
                "Comparable ePK substrate-role blockers in this lane have not cleared with "
                "structure-only nearest-atom, topology, terminal-index, reciprocal-context, "
                "local-exposure, or active-site-orientation proxies; source-reviewed evidence "
                "remains necessary for adjudication while excluded from predictive features."
            ),
        },
        "rule_delta": {
            "strict_false_positives": strict["pdb_ids_by_outcome"]["false_positive"],
            "auth_guard_false_positives": auth["pdb_ids_by_outcome"]["false_positive"],
            "reciprocal_folded_tyr_rescue_false_positives": reciprocal["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "orientation_supported_rescue_false_positives": orientation_rescue["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "orientation_guarded_auth_false_negatives": orientation_guard["pdb_ids_by_outcome"][
                "false_negative"
            ],
            "orientation_supported_true_positives_added_over_auth": sorted(
                set(orientation_rescue["pdb_ids_by_outcome"]["true_positive"])
                - set(auth["pdb_ids_by_outcome"]["true_positive"])
            ),
            "orientation_supported_false_positives_added_over_auth": sorted(
                set(orientation_rescue["pdb_ids_by_outcome"]["false_positive"])
                - set(auth["pdb_ids_by_outcome"]["false_positive"])
            ),
        },
        "run_record": {
            "lane_id": LANE_ID,
            "started_at": started_for_measure,
            "ended_at": ended_at,
            "measured_minutes": measured_minutes,
            "hypothesis": (
                "Source-free active-site orientation/asymmetry features can distinguish true "
                "folded Tyr substrate acceptors from topology-confounded mimics if structure-only "
                "substrate-role identity is recoverable."
            ),
            "diagnostic_rows_added_or_reused": {
                "reused_from_local_exposure_probe": len(rows),
                "added_this_run": [],
                "total": len(rows),
            },
            "source_free_features_tested": [
                "hydroxyl anchor-to-gamma angle",
                "hydroxyl gamma-facing versus backside protein half-space counts",
                "ligand-chain, acceptor-chain, and other-chain density near the nucleotide gamma",
                "gamma-axis forward/back protein density split",
                "nearest other nucleotide/metal and active-gamma distances to the hydroxyl",
                "frozen orientation_support_class",
                "orientation_supported_folded_tyr_rescue_v1 rule",
                "orientation_guarded_auth_strict_v1 rule",
            ],
            "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
            "rule_results": {
                result["rule_id"]: {
                    "confusion_matrix": result["confusion_matrix"],
                    "pdb_ids_by_outcome": result["pdb_ids_by_outcome"],
                    "failure_mode_counts": result["failure_mode_counts"],
                    "clears_diagnostic_tranche": result["clears_diagnostic_tranche"],
                }
                for result in rule_results
            },
            "confusion_matrix": orientation_rescue["confusion_matrix"],
            "decisive_counterexamples": {
                "false_positive_ids_seen_across_rules": false_positive_ids,
                "false_negative_ids_seen_across_rules": false_negative_ids,
                "primary_probe_rows": ["9UUR", "9UUX", "9UW4", "7B56"],
            },
            "false_positive_analysis": {
                "strict_baseline": strict["pdb_ids_by_outcome"]["false_positive"],
                "auth_guard": auth["pdb_ids_by_outcome"]["false_positive"],
                "reciprocal_folded_tyr_rescue": reciprocal["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "orientation_supported_folded_tyr_rescue": orientation_rescue[
                    "pdb_ids_by_outcome"
                ]["false_positive"],
                "interpretation": (
                    "The orientation probe is accepted only as a frozen feature-family test. "
                    "Any scalar split learned from the hard trio is marked post-hoc and not "
                    "used for prediction."
                ),
            },
            "false_negative_analysis": {
                "auth_guard": auth["pdb_ids_by_outcome"]["false_negative"],
                "orientation_supported_folded_tyr_rescue": orientation_rescue[
                    "pdb_ids_by_outcome"
                ]["false_negative"],
                "failure_mode_counts": orientation_rescue["failure_mode_counts"],
                "interpretation": (
                    "Remaining misses are expected where no terminal gamma-equivalent is "
                    "resolved, where same-chain/autophosphorylation-like topology dominates, "
                    "or where folded reciprocal context is not encoded by a general frozen "
                    "orientation class."
                ),
            },
            "blocker_classification": {
                "primary_outcome": primary_outcome,
                "classification": (
                    "Active-site orientation/asymmetry could not be evaluated because all "
                    "coordinate refetches failed."
                    if all_orientation_fetch_failed
                    else "Active-site orientation/asymmetry is review-only context; it does not "
                    "establish source-free substrate-role identity on the frozen diagnostic set."
                ),
            },
            "primary_outcome": primary_outcome,
            "next_query": (
                "Retry the source-free active-site orientation/asymmetry probe when RCSB coordinate "
                "fetching is available."
                if all_orientation_fetch_failed
                else "Classify the remaining strict-rule false negatives by unavailable ligand state "
                "versus same-chain/autophosphorylation-like topology, then decide whether the "
                "lane should stop feature probing and preserve a source-reviewed adjudication "
                "requirement for ePK substrate-role identity."
            ),
            "data_source_status": (
                "all_orientation_coordinate_fetches_failed"
                if all_orientation_fetch_failed
                else "orientation_coordinate_fetches_available"
            ),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "recommendation": (
                "Do not claim ePK production readiness. Keep active-site orientation features "
                "as review-only ambiguity evidence and require hybrid source-reviewed "
                "adjudication for folded reciprocal or product/analog cases."
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--ledger-started-at")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    payload = build_payload(args.workflow_started_at, args.ledger_started_at)
    output_path = Path(args.output)
    write_json(output_path, payload)
    if args.append_ledger:
        append_jsonl(LEDGER_PATH, payload["run_record"])
    print(
        json.dumps(
            {
                "artifact": str(output_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "orientation_supported_confusion": payload["run_record"]["confusion_matrix"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
