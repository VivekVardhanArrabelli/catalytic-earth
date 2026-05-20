#!/usr/bin/env python3
"""Review-only ePK local burial/solvent exposure probe.

This lane-local helper tests whether cheap source-free local exposure proxies
around candidate hydroxyl atoms can separate folded Tyr substrate positives
from topology-confounded counterexamples. Coordinates are fetched in memory
only; output is compact reduced evidence.
"""

from __future__ import annotations

import argparse
import json
import math
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
    METAL_CODES,
    NUCLEOTIDE_LIKE_CODES,
    WATER_CODES,
    dist,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_local_burial_solvent_exposure_probe_v1_20260520"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_reciprocal_entity_context_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_local_burial_solvent_exposure_probe_v1_20260520.json"
)

SHELL_DIRECTIONS = [
    tuple(component / math.sqrt(x * x + y * y + z * z) for component in (x, y, z))
    for x in (-1, 0, 1)
    for y in (-1, 0, 1)
    for z in (-1, 0, 1)
    if (x, y, z) != (0, 0, 0)
]


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def nearest_distance(center: dict[str, Any], atoms: list[dict[str, Any]]) -> float | None:
    best: float | None = None
    for atom in atoms:
        current = dist(center, atom)
        if best is None or current < best:
            best = current
    return round_or_none(best)


def count_within(center: dict[str, Any], atoms: list[dict[str, Any]], radius: float) -> int:
    return sum(1 for atom in atoms if dist(center, atom) <= radius)


def residue_keys_within(center: dict[str, Any], atoms: list[dict[str, Any]], radius: float) -> int:
    return len({atom["residue_key"] for atom in atoms if dist(center, atom) <= radius})


def open_shell_fraction(
    center: dict[str, Any],
    blockers: list[dict[str, Any]],
    shell_radius: float,
    blocker_radius: float = 1.8,
) -> float:
    open_count = 0
    for direction in SHELL_DIRECTIONS:
        shell_point = {
            "x": center["x"] + direction[0] * shell_radius,
            "y": center["y"] + direction[1] * shell_radius,
            "z": center["z"] + direction[2] * shell_radius,
        }
        blocked = any(dist(shell_point, atom) <= blocker_radius for atom in blockers)
        if not blocked:
            open_count += 1
    return round(open_count / len(SHELL_DIRECTIONS), 3)


def exposure_profile(features: dict[str, Any]) -> str:
    protein_6 = features["protein_heavy_atom_count_within_6a_excluding_same_residue"]
    open_3 = features["open_shell_fraction_3a_excluding_same_residue"]
    nearest_water = features["nearest_water_oxygen_distance_angstrom"]
    water_close = nearest_water is not None and nearest_water <= 4.0
    if protein_6 >= 28 and open_3 <= 0.25 and not water_close:
        return "buried_like"
    if protein_6 <= 18 or open_3 >= 0.45 or water_close:
        return "open_or_surface_like"
    return "intermediate"


def local_exposure_features(
    acceptor_atom: dict[str, Any] | None,
    gamma_atom: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    if acceptor_atom is None:
        return {
            "local_exposure_status": "candidate_atom_not_resolved",
            "local_exposure_profile_class": "unavailable",
        }

    atom_atoms = [atom for atom in atoms if atom["record"] == "ATOM" and heavy(atom)]
    hetero_atoms = [atom for atom in atoms if atom["record"] == "HETATM" and heavy(atom)]
    same_residue_key = acceptor_atom["residue_key"]
    gamma_residue_key = gamma_atom["residue_key"] if gamma_atom else None

    protein_excluding_self = [atom for atom in atom_atoms if atom is not acceptor_atom]
    protein_excluding_same_residue = [
        atom for atom in atom_atoms if atom["residue_key"] != same_residue_key
    ]
    same_chain_protein = [
        atom
        for atom in protein_excluding_same_residue
        if atom["chain"] == acceptor_atom["chain"]
    ]
    other_chain_protein = [
        atom
        for atom in protein_excluding_same_residue
        if atom["chain"] != acceptor_atom["chain"]
    ]
    water_oxygen = [
        atom for atom in hetero_atoms if atom["resname"] in WATER_CODES and atom["element"] == "O"
    ]
    nonwater_hetero = [
        atom
        for atom in hetero_atoms
        if atom["resname"] not in WATER_CODES and atom["residue_key"] != gamma_residue_key
    ]
    nucleotide_or_metal = [
        atom
        for atom in nonwater_hetero
        if atom["resname"] in NUCLEOTIDE_LIKE_CODES or atom["resname"] in METAL_CODES
    ]
    blockers = protein_excluding_same_residue + [
        atom for atom in nonwater_hetero if atom["resname"] not in NUCLEOTIDE_LIKE_CODES
    ]

    features = {
        "local_exposure_status": "ok",
        "protein_heavy_atom_count_within_4a_excluding_self_atom": count_within(
            acceptor_atom, protein_excluding_self, 4.0
        ),
        "protein_heavy_atom_count_within_5a_excluding_self_atom": count_within(
            acceptor_atom, protein_excluding_self, 5.0
        ),
        "protein_heavy_atom_count_within_6a_excluding_self_atom": count_within(
            acceptor_atom, protein_excluding_self, 6.0
        ),
        "protein_heavy_atom_count_within_8a_excluding_self_atom": count_within(
            acceptor_atom, protein_excluding_self, 8.0
        ),
        "protein_heavy_atom_count_within_10a_excluding_self_atom": count_within(
            acceptor_atom, protein_excluding_self, 10.0
        ),
        "protein_heavy_atom_count_within_4a_excluding_same_residue": count_within(
            acceptor_atom, protein_excluding_same_residue, 4.0
        ),
        "protein_heavy_atom_count_within_5a_excluding_same_residue": count_within(
            acceptor_atom, protein_excluding_same_residue, 5.0
        ),
        "protein_heavy_atom_count_within_6a_excluding_same_residue": count_within(
            acceptor_atom, protein_excluding_same_residue, 6.0
        ),
        "protein_heavy_atom_count_within_8a_excluding_same_residue": count_within(
            acceptor_atom, protein_excluding_same_residue, 8.0
        ),
        "protein_heavy_atom_count_within_10a_excluding_same_residue": count_within(
            acceptor_atom, protein_excluding_same_residue, 10.0
        ),
        "same_chain_protein_heavy_atom_count_within_6a_excluding_same_residue": count_within(
            acceptor_atom, same_chain_protein, 6.0
        ),
        "other_chain_protein_heavy_atom_count_within_6a_excluding_same_residue": count_within(
            acceptor_atom, other_chain_protein, 6.0
        ),
        "same_chain_protein_heavy_atom_count_within_8a_excluding_same_residue": count_within(
            acceptor_atom, same_chain_protein, 8.0
        ),
        "other_chain_protein_heavy_atom_count_within_8a_excluding_same_residue": count_within(
            acceptor_atom, other_chain_protein, 8.0
        ),
        "protein_residue_count_within_6a_excluding_same_residue": residue_keys_within(
            acceptor_atom, protein_excluding_same_residue, 6.0
        ),
        "other_chain_protein_residue_count_within_6a_excluding_same_residue": residue_keys_within(
            acceptor_atom, other_chain_protein, 6.0
        ),
        "nearest_same_chain_protein_heavy_atom_distance_angstrom": nearest_distance(
            acceptor_atom, same_chain_protein
        ),
        "nearest_other_chain_protein_heavy_atom_distance_angstrom": nearest_distance(
            acceptor_atom, other_chain_protein
        ),
        "nearest_water_oxygen_distance_angstrom": nearest_distance(acceptor_atom, water_oxygen),
        "water_oxygen_count_within_4a": count_within(acceptor_atom, water_oxygen, 4.0),
        "water_oxygen_count_within_6a": count_within(acceptor_atom, water_oxygen, 6.0),
        "water_oxygen_count_within_8a": count_within(acceptor_atom, water_oxygen, 8.0),
        "nearest_nonwater_hetero_heavy_atom_distance_angstrom": nearest_distance(
            acceptor_atom, nonwater_hetero
        ),
        "nonwater_hetero_heavy_atom_count_within_6a_excluding_selected_gamma_residue": count_within(
            acceptor_atom, nonwater_hetero, 6.0
        ),
        "nucleotide_or_metal_heavy_atom_count_within_6a_excluding_selected_gamma_residue": count_within(
            acceptor_atom, nucleotide_or_metal, 6.0
        ),
        "open_shell_fraction_3a_excluding_same_residue": open_shell_fraction(
            acceptor_atom, blockers, 3.0
        ),
        "open_shell_fraction_5a_excluding_same_residue": open_shell_fraction(
            acceptor_atom, blockers, 5.0
        ),
    }
    features["local_exposure_profile_class"] = exposure_profile(features)
    return features


def enrich_candidate(candidate: dict[str, Any] | None, atoms: list[dict[str, Any]]) -> dict[str, Any] | None:
    if candidate is None:
        return None
    enriched = deepcopy(candidate)
    gamma_atom = find_atom(atoms, candidate.get("terminal_gamma_equivalent_atom"))
    acceptor_atom = find_atom(atoms, candidate.get("nearest_protein_hydroxyl_atom"))
    enriched["local_exposure_features"] = local_exposure_features(acceptor_atom, gamma_atom, atoms)
    return enriched


def load_source_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    return payload["diagnostic_rows"]


def enrich_row(row: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text(row["pdb_id"])
    source_features = row["structure_features"]
    base_features = deepcopy(source_features)
    if text is None:
        base_features.update(
            {
                "local_exposure_fetch_status": "error",
                "local_exposure_fetch_error": fetch_error,
                "local_exposure_candidates_within_8a": [],
                "nearest_strict_cross_chain_candidate": None,
                "nearest_strict_auth_terminal_guard_candidate": None,
                "nearest_reciprocal_folded_tyr_rescue_candidate": None,
            }
        )
    else:
        atoms = parse_pdb_atoms(text)
        local_candidates = [
            enrich_candidate(candidate, atoms)
            for candidate in source_features.get("reciprocal_enriched_candidates_within_8a", [])
        ]
        local_candidates = [candidate for candidate in local_candidates if candidate is not None]
        base_features.update(
            {
                "local_exposure_fetch_status": "ok",
                "local_exposure_fetch_error": None,
                "local_exposure_candidates_within_8a": local_candidates,
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


def exposure_class(candidate: dict[str, Any] | None) -> str | None:
    if not candidate:
        return None
    return candidate.get("local_exposure_features", {}).get("local_exposure_profile_class")


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


def rule_local_open_shell_folded_tyr_rescue(features: dict[str, Any]) -> bool:
    if features.get("nearest_strict_auth_terminal_guard_candidate"):
        return True
    candidate = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
    return bool(candidate and exposure_class(candidate) != "buried_like")


def rule_local_burial_guarded_auth_strict(features: dict[str, Any]) -> bool:
    candidate = features.get("nearest_strict_auth_terminal_guard_candidate")
    return bool(candidate and exposure_class(candidate) != "buried_like")


def rule_water_or_open_permissive_nearest(features: dict[str, Any]) -> bool:
    if not rule_permissive(features):
        return False
    candidates = features.get("local_exposure_candidates_within_8a", [])
    if not candidates:
        return False
    candidate = candidates[0]
    exposure = candidate.get("local_exposure_features", {})
    nearest_water = exposure.get("nearest_water_oxygen_distance_angstrom")
    open_shell = exposure.get("open_shell_fraction_3a_excluding_same_residue")
    return bool(
        (nearest_water is not None and nearest_water <= 4.0)
        or (open_shell is not None and open_shell >= 0.45)
    )


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
    "local_open_shell_folded_tyr_rescue_v1": {
        "description": (
            "Auth-guard strict positives plus reciprocal folded-Tyr rescue candidates "
            "unless the hydroxyl exposure profile is buried_like."
        ),
        "function": rule_local_open_shell_folded_tyr_rescue,
    },
    "local_burial_guarded_auth_strict_v1": {
        "description": "Auth-guard strict positives rejected when their selected hydroxyl is buried_like.",
        "function": rule_local_burial_guarded_auth_strict,
    },
    "water_or_open_permissive_nearest_hydroxyl_v1": {
        "description": (
            "Permissive nearest-hydroxyl rule gated by either a water oxygen within "
            "4 A or open-shell fraction >=0.45 around the nearest hydroxyl."
        ),
        "function": rule_water_or_open_permissive_nearest,
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
            "local_open_shell_folded_tyr_rescue_v1",
        } and features.get("nearest_reciprocal_folded_tyr_rescue_candidate"):
            return "folded_tyr_topology_counterexample"
        strict_candidate = features.get("nearest_strict_cross_chain_candidate")
        if strict_candidate and strict_candidate.get("candidate_resolved_n_terminal_internal_fragment_like"):
            return "internal_fragment_n_terminal_mimicry"
        if features.get("nearest_protein_hydroxyl_distance_angstrom") is not None:
            return "nearest_hydroxyl_role_ambiguity"
        return "biological_role_ambiguity"
    if is_positive(row) and not predicted_positive:
        rescue_candidate = features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
        if rescue_candidate and exposure_class(rescue_candidate) == "buried_like":
            return "local_burial_rejected_folded_tyr_positive"
        if rescue_candidate:
            return "reciprocal_catalytic_context_ambiguity"
        candidates = features.get("local_exposure_candidates_within_8a", [])
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


def profile_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_counts: Counter[str] = Counter()
    row_presence_by_label: dict[str, Counter[str]] = {
        "positive": Counter(),
        "counterexample": Counter(),
    }
    selected_by_rule: dict[str, Counter[str]] = {
        "auth_guard_candidate": Counter(),
        "folded_tyr_rescue_candidate": Counter(),
    }
    for row in rows:
        label = "positive" if is_positive(row) else "counterexample"
        row_profiles = set()
        features = row["structure_features"]
        for candidate in features.get("local_exposure_candidates_within_8a", []):
            profile = exposure_class(candidate) or "unavailable"
            candidate_counts[profile] += 1
            row_profiles.add(profile)
        for profile in row_profiles:
            row_presence_by_label[label][profile] += 1
        for key, source_key in [
            ("auth_guard_candidate", "nearest_strict_auth_terminal_guard_candidate"),
            ("folded_tyr_rescue_candidate", "nearest_reciprocal_folded_tyr_rescue_candidate"),
        ]:
            profile = exposure_class(features.get(source_key))
            if profile:
                selected_by_rule[key][profile] += 1
    return {
        "candidate_profile_counts": dict(sorted(candidate_counts.items())),
        "row_profile_presence_by_label": {
            label: dict(sorted(counter.items())) for label, counter in row_presence_by_label.items()
        },
        "selected_candidate_profile_counts": {
            key: dict(sorted(counter.items())) for key, counter in selected_by_rule.items()
        },
    }


def probe_rows(rows: list[dict[str, Any]], pdb_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {row["pdb_id"]: row for row in rows}
    probes = []
    for pdb_id in pdb_ids:
        row = by_id[pdb_id]
        features = row["structure_features"]
        selected = features.get("nearest_reciprocal_folded_tyr_rescue_candidate") or features.get(
            "nearest_strict_auth_terminal_guard_candidate"
        ) or features.get(
            "nearest_strict_cross_chain_candidate"
        )
        probes.append(
            {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "ligand_state": features["ligand_state"],
                "nearest_distance_angstrom": features["nearest_protein_hydroxyl_distance_angstrom"],
                "selected_candidate": selected,
                "nearest_local_exposure_candidates_within_8a": [
                    {
                        "distance_angstrom": candidate["distance_angstrom"],
                        "terminal_gamma_ligand_chain": candidate["terminal_gamma_ligand_chain"],
                        "candidate_acceptor_chain": candidate["candidate_acceptor_chain"],
                        "candidate_acceptor_residue_code": candidate["candidate_acceptor_residue_code"],
                        "candidate_acceptor_auth_seq_id_int": candidate.get(
                            "candidate_acceptor_auth_seq_id_int"
                        ),
                        "reciprocal_context_class": candidate.get("reciprocal_context_class"),
                        "local_exposure_features": candidate.get("local_exposure_features"),
                    }
                    for candidate in features.get("local_exposure_candidates_within_8a", [])[:4]
                ],
            }
        )
    return probes


def selected_candidate_for_probe(row: dict[str, Any]) -> dict[str, Any] | None:
    features = row["structure_features"]
    return (
        features.get("nearest_reciprocal_folded_tyr_rescue_candidate")
        or features.get("nearest_strict_auth_terminal_guard_candidate")
        or features.get("nearest_strict_cross_chain_candidate")
    )


def trio_separability_scan(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {row["pdb_id"]: row for row in rows}
    positive_ids = ["9UUR", "9UUX"]
    counterexample_id = "9UW4"
    candidate_features: dict[str, dict[str, Any]] = {}
    for pdb_id in [*positive_ids, counterexample_id]:
        candidate = selected_candidate_for_probe(by_id[pdb_id])
        candidate_features[pdb_id] = (
            candidate.get("local_exposure_features", {}) if candidate else {}
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
            projection = posthoc_threshold_projection(rows, key, direction, threshold)
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
                        "projection_on_54_rows": projection,
                    },
                }
            )
    return {
        "positive_ids": positive_ids,
        "counterexample_id": counterexample_id,
        "candidate_features": candidate_features,
        "features_where_9uw4_outside_two_positive_range": outside_positive_range,
        "interpretation": (
            "Several scalar exposure proxies can separate 9UW4 from only the two "
            "source-reviewed folded-Tyr positives by post-hoc thresholds, but the "
            "accepted frozen profile class and rule do not separate them. These "
            "scalars are therefore review-only hypotheses, not a source-free identity rule."
        ),
    }


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
            value = candidate.get("local_exposure_features", {}).get(feature)
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


def select_primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    local_rescue = next(
        result for result in rule_results if result["rule_id"] == "local_open_shell_folded_tyr_rescue_v1"
    )
    if local_rescue["failure_mode_counts"].get("folded_tyr_topology_counterexample"):
        return "counterexample_found"
    if any(
        result["failure_mode_counts"].get("same_chain_or_autophosphorylation_like_topology")
        or result["failure_mode_counts"].get("reciprocal_catalytic_context_ambiguity")
        for result in rule_results
    ):
        return "blocker_not_cleared_biology_ambiguity"
    return "blocker_not_cleared_method_weakness"


def build_payload(workflow_started_at: str, ledger_started_at: str | None = None) -> dict[str, Any]:
    source_rows = load_source_rows()
    rows = [enrich_row(row, workflow_started_at) for row in source_rows]
    rule_results = [confusion_for_rule(rows, rule_id, rule_spec) for rule_id, rule_spec in RULES.items()]
    primary_outcome = select_primary_outcome(rule_results)
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    local_fetch_counts = Counter(
        row["structure_features"]["local_exposure_fetch_status"] for row in rows
    )
    strict = next(
        result
        for result in rule_results
        if result["rule_id"] == "strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1"
    )
    auth = next(result for result in rule_results if result["rule_id"] == "strict_auth_terminal_guard_v1")
    reciprocal = next(
        result for result in rule_results if result["rule_id"] == "reciprocal_folded_tyr_rescue_v1"
    )
    local_rescue = next(
        result for result in rule_results if result["rule_id"] == "local_open_shell_folded_tyr_rescue_v1"
    )
    local_guard = next(
        result for result in rule_results if result["rule_id"] == "local_burial_guarded_auth_strict_v1"
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
            "method": "review_only_source_free_local_burial_solvent_exposure_probe",
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
            "local_exposure_fetch_status_counts": dict(sorted(local_fetch_counts.items())),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": (
            "If true ePK substrate phosphoacceptor hydroxyls have a source-free local exposure "
            "pattern distinct from topology-confounded mimics, then cheap burial, water-contact, "
            "and open-shell proxies should recover folded Tyr positives while rejecting 9UW4 "
            "and without reintroducing 7B56."
        ),
        "feature_definitions": {
            "protein_heavy_atom_counts": (
                "Counts of model-1 protein heavy atoms within fixed radii of the candidate "
                "hydroxyl, with both self-atom and same-residue exclusions."
            ),
            "same_chain_other_chain_density": (
                "Protein heavy-atom and residue counts split by acceptor chain versus other chains."
            ),
            "water_and_heteroatom_proximity": (
                "Nearest water oxygen, water oxygen counts, nonwater heteroatom counts, and "
                "nucleotide/metal counts near the candidate hydroxyl."
            ),
            "open_shell_fraction": (
                "Fraction of 26 fixed directions at 3 A or 5 A from the hydroxyl not blocked "
                "within 1.8 A by protein heavy atoms outside the same residue or non-nucleotide hetero atoms."
            ),
            "local_exposure_profile_class": (
                "Frozen descriptive class: buried_like when >=28 protein heavy atoms within 6 A, "
                "open-shell fraction <=0.25, and no water oxygen within 4 A; open_or_surface_like "
                "when <=18 protein heavy atoms within 6 A, open-shell fraction >=0.45, or water "
                "within 4 A; otherwise intermediate."
            ),
        },
        "diagnostic_rows": rows,
        "rules": rule_results,
        "profile_summary": profile_summary(rows),
        "trio_separability_scan": trio_separability_scan(rows),
        "counterexample_probe": probe_rows(
            rows, ["9UUR", "9UUX", "9UW4", "7B56", "3QHR", "3QHW", "1L0O", "3TM0"]
        ),
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "local_exposure_signal": (
                "Local exposure features are useful audit descriptors, but the tested frozen "
                "profile rule does not provide a complete source-free substrate-role identity rule."
            ),
            "counterexample_signal": (
                "The hard comparison remains the reciprocal folded-Tyr trio 9UUR/9UUX/9UW4; "
                "all three are open_or_surface_like with the same 25 protein heavy atoms within "
                "6 A after same-residue exclusion, so broad burial/exposure class does not "
                "separate the counterexample from the positives."
            ),
            "historical_comparator_assessment": (
                "Comparable ePK substrate-role blockers in this lane have not cleared with "
                "structure-only nearest-atom, topology, terminal-index, reciprocal-context, "
                "or local exposure proxies; source-reviewed evidence remains necessary for "
                "adjudication while excluded from predictive features."
            ),
        },
        "rule_delta": {
            "strict_false_positives": strict["pdb_ids_by_outcome"]["false_positive"],
            "auth_guard_false_positives": auth["pdb_ids_by_outcome"]["false_positive"],
            "reciprocal_folded_tyr_rescue_false_positives": reciprocal["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "local_open_shell_rescue_false_positives": local_rescue["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "local_burial_guarded_auth_false_negatives": local_guard["pdb_ids_by_outcome"][
                "false_negative"
            ],
            "local_open_shell_true_positives_added_over_auth": sorted(
                set(local_rescue["pdb_ids_by_outcome"]["true_positive"])
                - set(auth["pdb_ids_by_outcome"]["true_positive"])
            ),
            "local_open_shell_false_positives_added_over_auth": sorted(
                set(local_rescue["pdb_ids_by_outcome"]["false_positive"])
                - set(auth["pdb_ids_by_outcome"]["false_positive"])
            ),
        },
        "run_record": {
            "lane_id": LANE_ID,
            "started_at": started_for_measure,
            "ended_at": ended_at,
            "measured_minutes": measured_minutes,
            "hypothesis": (
                "Local burial, water-contact, and open-shell exposure proxies can separate true "
                "folded Tyr substrate acceptors from topology-confounded mimics if structure-only "
                "substrate-role identity is recoverable."
            ),
            "diagnostic_rows_added_or_reused": {
                "reused_from_reciprocal_probe": len(rows),
                "added_this_run": [],
                "total": len(rows),
            },
            "source_free_features_tested": [
                "candidate hydroxyl protein heavy-atom counts within 4/5/6/8/10 A",
                "same-chain versus other-chain local protein density",
                "local protein residue counts near hydroxyl",
                "nearest water oxygen and water oxygen counts",
                "nonwater heteroatom and nucleotide/metal proximity",
                "26-direction open-shell vacancy fraction at 3 A and 5 A",
                "frozen local_exposure_profile_class",
                "local_open_shell_folded_tyr_rescue_v1 rule",
                "local_burial_guarded_auth_strict_v1 rule",
                "water_or_open_permissive_nearest_hydroxyl_v1 rule",
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
            "confusion_matrix": local_rescue["confusion_matrix"],
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
                "local_open_shell_folded_tyr_rescue": local_rescue["pdb_ids_by_outcome"][
                    "false_positive"
                ],
                "interpretation": (
                    "The frozen exposure-profile rescue still admits 9UW4. Several scalar "
                    "features separate 9UW4 from only 9UUR/9UUX by post-hoc thresholds, but "
                    "that would be candidate-specific tuning rather than a source-free identity rule."
                ),
            },
            "false_negative_analysis": {
                "auth_guard": auth["pdb_ids_by_outcome"]["false_negative"],
                "local_open_shell_folded_tyr_rescue": local_rescue["pdb_ids_by_outcome"][
                    "false_negative"
                ],
                "failure_mode_counts": local_rescue["failure_mode_counts"],
                "interpretation": (
                    "Remaining misses include product/analog state, same-chain or "
                    "autophosphorylation-like topology, and source-reviewed folded contexts "
                    "not encoded by a general exposure rule."
                ),
            },
            "blocker_classification": {
                "primary_outcome": primary_outcome,
                "classification": (
                    "Local exposure is review-only context; it does not establish source-free "
                    "substrate-role identity on the frozen 54-row diagnostic set."
                ),
            },
            "primary_outcome": primary_outcome,
            "next_query": (
                "Run a source-free acceptor-chain active-site orientation/asymmetry probe: compare "
                "candidate hydroxyl vector geometry to nucleotide gamma and nearby catalytic-chain "
                "density, especially 9UUR/9UUX/9UW4 and product-state false negatives."
            ),
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "recommendation": (
                "Do not claim ePK production readiness. Keep local exposure as review-only "
                "counterevidence and require source-reviewed adjudication for folded reciprocal "
                "or product/analog cases."
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
                "local_open_shell_confusion": payload["run_record"]["confusion_matrix"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
