#!/usr/bin/env python3
"""Review-only ePK reciprocal entity-context probe.

This lane-local helper tests whether source-free reciprocal chain/entity
context can distinguish true ePK substrate hydroxyls from kinase-like or
ATPase-like structural mimics. It reuses compact diagnostic rows from prior
lane artifacts, fetches coordinates only in memory to derive chain sequence
hashes and ligand occupancy, and writes compact reduced evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    utc_now,
    write_json,
    append_jsonl,
)
from substrate_role_identity_eval import (
    ACTIVE_GAMMA_CODES,
    METAL_CODES,
    NUCLEOTIDE_LIKE_CODES,
    compact_atom,
    fetch_pdb_text,
    parse_pdb_atoms,
    chain_residue_maps,
)


ARTIFACT_ID = "epk_reciprocal_entity_context_probe_v1_20260520"
SOURCE_ARTIFACTS = [
    Path(
        "artifacts/research_lanes/epk_substrate_role_identity/"
        "epk_folded_nterminal_auth_terminal_stress_20260520.json"
    ),
    Path(
        "artifacts/research_lanes/epk_substrate_role_identity/"
        "epk_auth_terminal_guard_generalization_v2_20260520.json"
    ),
]


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def chain_sequence_hashes(
    residues_by_chain: dict[str, list[tuple[str, str, str, str]]],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for chain_id, residues in residues_by_chain.items():
        sequence = "|".join(residue[-1] for residue in residues)
        result[chain_id] = {
            "resolved_residue_count": len(residues),
            "residue_name_sequence_sha1_12": hashlib.sha1(sequence.encode("utf-8")).hexdigest()[:12],
        }
    return result


def residue_identity(atom: dict[str, Any]) -> tuple[str, str, str, str]:
    return atom["chain"], atom["resseq"], atom["icode"], atom["resname"]


def unique_compact_residues(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: OrderedDict[tuple[str, str, str, str], dict[str, Any]] = OrderedDict()
    for atom in atoms:
        by_key.setdefault(residue_identity(atom), compact_atom(atom))
    return list(by_key.values())


def source_free_chain_context(pdb_id: str) -> dict[str, Any]:
    text, fetch_error = fetch_pdb_text(pdb_id)
    if text is None:
        return {
            "sequence_context_fetch_status": "error",
            "sequence_context_fetch_error": fetch_error,
            "chain_sequence_hashes": {},
            "active_gamma_residues_by_chain": {},
            "nucleotide_or_metal_residue_counts_by_chain": {},
        }

    atoms = parse_pdb_atoms(text)
    hetero_atoms = [atom for atom in atoms if atom["record"] == "HETATM"]
    residues_by_chain, _ = chain_residue_maps(atoms)
    gamma_atoms = [
        atom
        for atom in hetero_atoms
        if atom["resname"] in ACTIVE_GAMMA_CODES and atom["atom_name"] in {"PG", "P3"}
    ]
    nucleotide_or_metal_atoms = [
        atom
        for atom in hetero_atoms
        if atom["resname"] in NUCLEOTIDE_LIKE_CODES or atom["resname"] in METAL_CODES
    ]

    active_gamma_by_chain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for residue in unique_compact_residues(gamma_atoms):
        active_gamma_by_chain[residue["chain_id"]].append(residue)

    nucleotide_or_metal_counts = Counter(
        residue["chain_id"] for residue in unique_compact_residues(nucleotide_or_metal_atoms)
    )
    return {
        "sequence_context_fetch_status": "ok",
        "sequence_context_fetch_error": None,
        "chain_sequence_hashes": chain_sequence_hashes(residues_by_chain),
        "active_gamma_residues_by_chain": dict(sorted(active_gamma_by_chain.items())),
        "nucleotide_or_metal_residue_counts_by_chain": dict(sorted(nucleotide_or_metal_counts.items())),
    }


def reciprocal_context_class(candidate: dict[str, Any], chain_context: dict[str, Any]) -> str:
    ligand_chain = candidate.get("terminal_gamma_ligand_chain")
    acceptor_chain = candidate.get("candidate_acceptor_chain")
    if not ligand_chain or not acceptor_chain:
        return "missing_chain_context"
    if ligand_chain == acceptor_chain:
        return "same_chain_gamma_hydroxyl"

    chain_hashes = chain_context["chain_sequence_hashes"]
    ligand_hash = chain_hashes.get(ligand_chain, {}).get("residue_name_sequence_sha1_12")
    acceptor_hash = chain_hashes.get(acceptor_chain, {}).get("residue_name_sequence_sha1_12")
    same_entity = bool(ligand_hash and acceptor_hash and ligand_hash == acceptor_hash)
    active_gamma_count = len(chain_context["active_gamma_residues_by_chain"].get(acceptor_chain, []))
    nucleotide_or_metal_count = chain_context["nucleotide_or_metal_residue_counts_by_chain"].get(
        acceptor_chain, 0
    )

    if same_entity:
        return "same_sequence_entity_cross_chain"
    if active_gamma_count:
        return "reciprocal_active_gamma_different_entity"
    if nucleotide_or_metal_count:
        return "reciprocal_nucleotide_or_metal_different_entity"
    return "asymmetric_cross_chain_acceptor"


def enrich_candidate(candidate: dict[str, Any] | None, chain_context: dict[str, Any]) -> dict[str, Any] | None:
    if candidate is None:
        return None
    enriched = dict(candidate)
    ligand_chain = candidate.get("terminal_gamma_ligand_chain")
    acceptor_chain = candidate.get("candidate_acceptor_chain")
    chain_hashes = chain_context["chain_sequence_hashes"]
    ligand_hash = chain_hashes.get(ligand_chain or "", {})
    acceptor_hash = chain_hashes.get(acceptor_chain or "", {})
    ligand_len = ligand_hash.get("resolved_residue_count")
    acceptor_len = acceptor_hash.get("resolved_residue_count")
    length_ratio = None
    if ligand_len and acceptor_len:
        length_ratio = round(max(ligand_len, acceptor_len) / min(ligand_len, acceptor_len), 3)
    enriched.update(
        {
            "ligand_chain_sequence_sha1_12": ligand_hash.get("residue_name_sequence_sha1_12"),
            "candidate_chain_sequence_sha1_12": acceptor_hash.get("residue_name_sequence_sha1_12"),
            "ligand_acceptor_same_sequence_entity": bool(
                ligand_hash
                and acceptor_hash
                and ligand_hash.get("residue_name_sequence_sha1_12")
                == acceptor_hash.get("residue_name_sequence_sha1_12")
            ),
            "ligand_acceptor_resolved_length_ratio": length_ratio,
            "ligand_chain_active_gamma_count": len(
                chain_context["active_gamma_residues_by_chain"].get(ligand_chain or "", [])
            ),
            "candidate_chain_active_gamma_count": len(
                chain_context["active_gamma_residues_by_chain"].get(acceptor_chain or "", [])
            ),
            "candidate_chain_nucleotide_or_metal_residue_count": chain_context[
                "nucleotide_or_metal_residue_counts_by_chain"
            ].get(acceptor_chain or "", 0),
        }
    )
    enriched["reciprocal_context_class"] = reciprocal_context_class(enriched, chain_context)
    return enriched


def load_source_rows() -> list[dict[str, Any]]:
    rows_by_id: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for artifact_path in SOURCE_ARTIFACTS:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        artifact_id = payload["metadata"]["artifact_id"]
        for row in payload["diagnostic_rows"]:
            if row["pdb_id"] in rows_by_id:
                continue
            rows_by_id[row["pdb_id"]] = {
                "source_artifact_id": artifact_id,
                "source_artifact_path": str(artifact_path),
                **row,
            }
    return list(rows_by_id.values())


def auth_guard_identity_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return features.get("nearest_strict_auth_terminal_guard_candidate")


def strict_identity_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    return features.get("nearest_strict_cross_chain_candidate")


def folded_tyr_rescue_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    for candidate in features.get("reciprocal_enriched_candidates_within_8a", []):
        if candidate["distance_angstrom"] > 6.0:
            continue
        if not candidate.get("cross_chain_topology"):
            continue
        if not candidate.get("candidate_acceptor_is_tyr"):
            continue
        if not candidate.get("candidate_acceptor_chain_is_folded_like"):
            continue
        if candidate.get("ligand_acceptor_same_sequence_entity"):
            continue
        if candidate.get("reciprocal_context_class") not in {
            "reciprocal_active_gamma_different_entity",
            "reciprocal_nucleotide_or_metal_different_entity",
        }:
            continue
        return candidate
    return None


def asymmetric_guard_candidate(features: dict[str, Any]) -> dict[str, Any] | None:
    candidate = features.get("nearest_strict_auth_terminal_guard_candidate")
    if candidate and candidate.get("reciprocal_context_class") == "asymmetric_cross_chain_acceptor":
        return candidate
    return None


def enrich_row(row: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    chain_context = source_free_chain_context(row["pdb_id"])
    source_features = row["structure_features"]
    enriched_candidates = [
        enrich_candidate(candidate, chain_context)
        for candidate in source_features.get("nearest_hydroxyl_pair_candidates_within_8a", [])
    ]
    enriched_candidates = [candidate for candidate in enriched_candidates if candidate is not None]

    features = {
        "ligand_state": source_features.get("ligand_state"),
        "terminal_gamma_equivalent_atom_available": source_features.get(
            "terminal_gamma_equivalent_atom_available"
        ),
        "nearest_protein_hydroxyl_distance_angstrom": source_features.get(
            "nearest_protein_hydroxyl_distance_angstrom"
        ),
        "polymer_chain_count": source_features.get("polymer_chain_count"),
        "polymer_entity_count_sequence_proxy": source_features.get(
            "polymer_entity_count_sequence_proxy"
        ),
        "chain_sequence_hashes": chain_context["chain_sequence_hashes"],
        "active_gamma_residues_by_chain": chain_context["active_gamma_residues_by_chain"],
        "nucleotide_or_metal_residue_counts_by_chain": chain_context[
            "nucleotide_or_metal_residue_counts_by_chain"
        ],
        "sequence_context_fetch_status": chain_context["sequence_context_fetch_status"],
        "sequence_context_fetch_error": chain_context["sequence_context_fetch_error"],
        "reciprocal_enriched_candidates_within_8a": enriched_candidates[:8],
    }
    features["nearest_strict_cross_chain_candidate"] = enrich_candidate(
        source_features.get("nearest_strict_cross_chain_candidate"), chain_context
    )
    features["nearest_strict_auth_terminal_guard_candidate"] = enrich_candidate(
        source_features.get("nearest_strict_auth_terminal_guard_candidate"), chain_context
    )
    features["nearest_reciprocal_asymmetric_guard_candidate"] = asymmetric_guard_candidate(features)
    features["nearest_reciprocal_folded_tyr_rescue_candidate"] = folded_tyr_rescue_candidate(features)

    return {
        "pdb_id": row["pdb_id"],
        "evaluation_label": row["evaluation_label"],
        "evaluation_group": row["evaluation_group"],
        "evaluation_label_source": row.get("evaluation_label_source"),
        "evaluation_label_used_only_for_eval": True,
        "source_artifact_id": row["source_artifact_id"],
        "feature_extraction_started_after": workflow_started_at,
        "source_free_feature_only": True,
        "forbidden_predictive_features_excluded": FORBIDDEN_PREDICTIVE_FEATURES,
        "fetch_status": row.get("fetch_status"),
        "fetch_error": row.get("fetch_error"),
        "pdb_sha256_12": row.get("pdb_sha256_12"),
        "atom_count_model1": row.get("atom_count_model1"),
        "structure_features": features,
    }


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def rule_strict_baseline(features: dict[str, Any]) -> bool:
    return bool(strict_identity_candidate(features))


def rule_auth_guard(features: dict[str, Any]) -> bool:
    return bool(auth_guard_identity_candidate(features))


def rule_permissive(features: dict[str, Any]) -> bool:
    distance = features["nearest_protein_hydroxyl_distance_angstrom"]
    return bool(features["terminal_gamma_equivalent_atom_available"] and distance is not None and distance <= 6.0)


def rule_reciprocal_asymmetric_guard(features: dict[str, Any]) -> bool:
    return bool(features["nearest_reciprocal_asymmetric_guard_candidate"])


def rule_reciprocal_folded_tyr_rescue(features: dict[str, Any]) -> bool:
    return bool(
        auth_guard_identity_candidate(features)
        or features["nearest_reciprocal_folded_tyr_rescue_candidate"]
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
    "reciprocal_asymmetric_guarded_strict_v1": {
        "description": (
            "Auth-guard strict candidate must also be a different-chain, different-sequence "
            "acceptor with no reciprocal active-gamma, nucleotide, or metal context on the "
            "acceptor chain."
        ),
        "function": rule_reciprocal_asymmetric_guard,
    },
    "reciprocal_folded_tyr_rescue_v1": {
        "description": (
            "Auth-guard strict positives plus a review-only rescue for folded cross-chain "
            "Tyr candidates within 6 A when ligand and acceptor chains are different "
            "sequence entities and the acceptor chain has reciprocal nucleotide/gamma context."
        ),
        "function": rule_reciprocal_folded_tyr_rescue,
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
        if rule_id == "reciprocal_folded_tyr_rescue_v1" and features[
            "nearest_reciprocal_folded_tyr_rescue_candidate"
        ]:
            return "reciprocal_folded_tyr_counterexample"
        strict_candidate = features.get("nearest_strict_cross_chain_candidate")
        if strict_candidate and strict_candidate.get("candidate_resolved_n_terminal_internal_fragment_like"):
            return "internal_fragment_n_terminal_mimicry"
        if features.get("nearest_protein_hydroxyl_distance_angstrom") is not None:
            return "nearest_hydroxyl_role_ambiguity"
        return "biological_role_ambiguity"
    if is_positive(row) and not predicted_positive:
        rescue_candidate = features["nearest_reciprocal_folded_tyr_rescue_candidate"]
        if rescue_candidate and rule_id != "reciprocal_folded_tyr_rescue_v1":
            return "reciprocal_folded_tyr_context"
        candidates = features.get("reciprocal_enriched_candidates_within_8a", [])
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


def context_class_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    all_counts: Counter[str] = Counter()
    by_label: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        label_bucket = "positive" if is_positive(row) else "counterexample"
        seen_for_row = set()
        for candidate in row["structure_features"].get("reciprocal_enriched_candidates_within_8a", []):
            context_class = candidate["reciprocal_context_class"]
            all_counts[context_class] += 1
            seen_for_row.add(context_class)
        for context_class in seen_for_row:
            by_label[label_bucket][context_class] += 1
    return {
        "candidate_context_class_counts": dict(sorted(all_counts.items())),
        "row_context_class_presence_by_label": {
            label: dict(sorted(counts.items())) for label, counts in sorted(by_label.items())
        },
    }


def probe_rows(rows: list[dict[str, Any]], pdb_ids: list[str]) -> list[dict[str, Any]]:
    by_id = {row["pdb_id"]: row for row in rows}
    probes = []
    for pdb_id in pdb_ids:
        row = by_id[pdb_id]
        features = row["structure_features"]
        probes.append(
            {
                "pdb_id": pdb_id,
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "ligand_state": features["ligand_state"],
                "nearest_distance_angstrom": features["nearest_protein_hydroxyl_distance_angstrom"],
                "strict_auth_terminal_guard_candidate": features[
                    "nearest_strict_auth_terminal_guard_candidate"
                ],
                "reciprocal_folded_tyr_rescue_candidate": features[
                    "nearest_reciprocal_folded_tyr_rescue_candidate"
                ],
                "candidate_contexts_within_8a": [
                    {
                        "distance_angstrom": candidate["distance_angstrom"],
                        "terminal_gamma_ligand_chain": candidate["terminal_gamma_ligand_chain"],
                        "candidate_acceptor_chain": candidate["candidate_acceptor_chain"],
                        "candidate_acceptor_residue_code": candidate["candidate_acceptor_residue_code"],
                        "candidate_acceptor_auth_seq_id_int": candidate[
                            "candidate_acceptor_auth_seq_id_int"
                        ],
                        "candidate_acceptor_chain_length": candidate[
                            "candidate_acceptor_chain_length"
                        ],
                        "ligand_chain_length": candidate["ligand_chain_length"],
                        "candidate_chain_active_gamma_count": candidate[
                            "candidate_chain_active_gamma_count"
                        ],
                        "candidate_chain_nucleotide_or_metal_residue_count": candidate[
                            "candidate_chain_nucleotide_or_metal_residue_count"
                        ],
                        "ligand_acceptor_same_sequence_entity": candidate[
                            "ligand_acceptor_same_sequence_entity"
                        ],
                        "ligand_acceptor_resolved_length_ratio": candidate[
                            "ligand_acceptor_resolved_length_ratio"
                        ],
                        "reciprocal_context_class": candidate["reciprocal_context_class"],
                    }
                    for candidate in features.get("reciprocal_enriched_candidates_within_8a", [])
                ],
            }
        )
    return probes


def select_primary_outcome(rule_results: list[dict[str, Any]]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results):
        return "blocker_cleared_source_free"
    rescue = next(result for result in rule_results if result["rule_id"] == "reciprocal_folded_tyr_rescue_v1")
    if rescue["failure_mode_counts"].get("reciprocal_folded_tyr_counterexample"):
        return "counterexample_found"
    guarded = next(result for result in rule_results if result["rule_id"] == "reciprocal_asymmetric_guarded_strict_v1")
    if guarded["failure_mode_counts"].get("reciprocal_catalytic_context_ambiguity"):
        return "blocker_not_cleared_biology_ambiguity"
    return "blocker_not_cleared_method_weakness"


def build_payload(workflow_started_at: str) -> dict[str, Any]:
    source_rows = load_source_rows()
    rows = [enrich_row(row, workflow_started_at) for row in source_rows]
    rule_results = [confusion_for_rule(rows, rule_id, rule_spec) for rule_id, rule_spec in RULES.items()]
    outcome = select_primary_outcome(rule_results)
    if outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {outcome}")
    fetch_counts = Counter(row["fetch_status"] for row in rows)
    sequence_fetch_counts = Counter(
        row["structure_features"]["sequence_context_fetch_status"] for row in rows
    )
    auth = next(result for result in rule_results if result["rule_id"] == "strict_auth_terminal_guard_v1")
    rescue = next(result for result in rule_results if result["rule_id"] == "reciprocal_folded_tyr_rescue_v1")
    guarded = next(result for result in rule_results if result["rule_id"] == "reciprocal_asymmetric_guarded_strict_v1")
    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": utc_now(),
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_reciprocal_entity_context_probe",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_artifacts": [str(path) for path in SOURCE_ARTIFACTS],
            "frozen_row_count": len(rows),
            "materialized_row_count": sum(1 for row in rows if row["fetch_status"] == "ok"),
            "fetch_status_counts": dict(sorted(fetch_counts.items())),
            "sequence_context_fetch_status_counts": dict(sorted(sequence_fetch_counts.items())),
            "primary_outcome": outcome,
        },
        "hypothesis": (
            "A source-free reciprocal chain/entity feature should identify true kinase "
            "substrate acceptors if real substrate chains are asymmetric to the nucleotide "
            "chain, while controls should be same-chain, same-entity, or reciprocal "
            "nucleotide-bearing mimics. A folded-Tyr rescue tests whether different-entity "
            "reciprocal kinase context can safely recover MEK/ERK-like false negatives."
        ),
        "feature_definitions": {
            "chain_sequence_hashes": (
                "SHA1-12 hashes of resolved residue-name sequences by chain; full sequences are not stored."
            ),
            "ligand_acceptor_same_sequence_entity": (
                "Selected gamma chain and hydroxyl chain have identical resolved residue-name sequence hashes."
            ),
            "candidate_chain_active_gamma_count": (
                "Count of active gamma-capable nucleotide residues with PG/P3 atoms on the candidate acceptor chain."
            ),
            "candidate_chain_nucleotide_or_metal_residue_count": (
                "Count of source-free nucleotide-like or metal HETATM residues on the candidate acceptor chain."
            ),
            "reciprocal_context_class": (
                "same_chain_gamma_hydroxyl, same_sequence_entity_cross_chain, "
                "reciprocal_active_gamma_different_entity, "
                "reciprocal_nucleotide_or_metal_different_entity, or "
                "asymmetric_cross_chain_acceptor."
            ),
        },
        "diagnostic_rows": rows,
        "rules": rule_results,
        "context_class_summary": context_class_counts(rows),
        "counterexample_probe": probe_rows(rows, ["9UUR", "9UUX", "9UW4", "7B56", "3TM0", "1L0O"]),
        "blocker_classification": {
            "primary_outcome": outcome,
            "reciprocal_signal": (
                "The asymmetric guard does not improve over the auth-terminal strict baseline; "
                "it keeps peptide-like positives but cannot recover reciprocal folded kinase "
                "contexts or product-state positives."
            ),
            "counterexample_signal": (
                "The folded-Tyr reciprocal rescue recovers 9UUR and 9UUX but also admits "
                "9UW4, which has the same source-free reciprocal folded-Tyr context class."
            ),
            "historical_comparator_assessment": (
                "Prior lane artifacts continue to show that comparable ePK substrate-role "
                "blockers have not cleared with structure-only nearest-atom, topology, "
                "terminal-index, or reciprocal-context rules; source-reviewed evidence has "
                "remained necessary for adjudication while excluded from predictive features."
            ),
        },
        "rule_delta": {
            "auth_guard_false_negatives": auth["pdb_ids_by_outcome"]["false_negative"],
            "reciprocal_guard_false_negatives": guarded["pdb_ids_by_outcome"]["false_negative"],
            "folded_tyr_rescue_true_positives_added": sorted(
                set(rescue["pdb_ids_by_outcome"]["true_positive"])
                - set(auth["pdb_ids_by_outcome"]["true_positive"])
            ),
            "folded_tyr_rescue_false_positives_added": sorted(
                set(rescue["pdb_ids_by_outcome"]["false_positive"])
                - set(auth["pdb_ids_by_outcome"]["false_positive"])
            ),
        },
    }


def ledger_record(payload: dict[str, Any], workflow_started_at: str, started_at: str) -> dict[str, Any]:
    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(started_at)).total_seconds() / 60.0, 2)
    by_rule = {rule["rule_id"]: rule for rule in payload["rules"]}
    rescue = by_rule["reciprocal_folded_tyr_rescue_v1"]
    guarded = by_rule["reciprocal_asymmetric_guarded_strict_v1"]
    return {
        "lane_id": LANE_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": payload["hypothesis"],
        "diagnostic_rows_added_or_reused": {
            "total": payload["metadata"]["frozen_row_count"],
            "reused_from_terminal_index_stress": 30,
            "reused_from_nonoverlap_generalization": 24,
            "added_this_run": [],
        },
        "source_free_features_tested": [
            "resolved chain residue-name sequence hashes",
            "ligand/acceptor same-sequence entity flag",
            "acceptor-chain active-gamma occupancy",
            "acceptor-chain nucleotide-or-metal occupancy",
            "reciprocal context class",
            "reciprocal asymmetric guarded strict rule",
            "reciprocal folded-Tyr rescue rule",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": by_rule,
        "confusion_matrix": rescue["confusion_matrix"],
        "decisive_counterexamples": {
            "9UW4": (
                "False positive under reciprocal_folded_tyr_rescue_v1; source-free "
                "features match the recovered 9UUR/9UUX folded Tyr context."
            ),
            "7B56": (
                "Still blocked by auth-terminal guard as an internal-fragment N-terminal mimic; "
                "reciprocal context is not needed for this row."
            ),
        },
        "false_positive_analysis": {
            "reciprocal_folded_tyr_rescue_false_positives": rescue["pdb_ids_by_outcome"]["false_positive"],
            "interpretation": (
                "Different-entity reciprocal folded Tyr context is not decisive: it recovers "
                "true positives 9UUR/9UUX but also admits 9UW4."
            ),
        },
        "false_negative_analysis": {
            "reciprocal_asymmetric_guard_false_negatives": guarded["pdb_ids_by_outcome"]["false_negative"],
            "reciprocal_folded_tyr_rescue_false_negatives": rescue["pdb_ids_by_outcome"]["false_negative"],
            "failure_mode_counts": rescue["failure_mode_counts"],
            "interpretation": (
                "Product/analog rows without terminal gamma and same-chain/autophosphorylation-like "
                "topology remain unresolved by reciprocal entity context."
            ),
        },
        "blocker_classification": payload["blocker_classification"],
        "next_query": (
            "Run a cheap burial/local solvent exposure probe on the same combined diagnostic "
            "set to test whether candidate exposure separates 9UW4 from 9UUR/9UUX and "
            "whether product-state rows remain fundamentally unavailable."
        ),
        "primary_outcome": payload["metadata"]["primary_outcome"],
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Treat reciprocal entity context as "
            "review-only ambiguity evidence; it does not identify substrate role without "
            "source-reviewed adjudication."
        ),
        "git_sync_status": (
            "git fetch/pull were blocked by sandbox permission errors writing linked-worktree "
            "FETCH_HEAD; local HEAD, stale origin ref, and git ls-remote all matched before work."
        ),
        "workflow_started_at": workflow_started_at,
        "artifact_path": f"artifacts/research_lanes/epk_substrate_role_identity/{ARTIFACT_ID}.json",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--artifact-dir", default="artifacts/research_lanes/epk_substrate_role_identity")
    parser.add_argument("--append-ledger", action="store_true")
    args = parser.parse_args(argv)

    artifact_dir = Path(args.artifact_dir)
    payload = build_payload(args.workflow_started_at)
    artifact_path = artifact_dir / f"{ARTIFACT_ID}.json"
    write_json(artifact_path, payload)
    if args.append_ledger:
        append_jsonl(
            artifact_dir / "epk_substrate_role_identity_runs.jsonl",
            ledger_record(payload, args.workflow_started_at, args.started_at),
        )
    print(
        json.dumps(
            {
                "artifact_path": str(artifact_path),
                "primary_outcome": payload["metadata"]["primary_outcome"],
                "rule_delta": payload["rule_delta"],
                "fetch_status_counts": payload["metadata"]["fetch_status_counts"],
                "sequence_context_fetch_status_counts": payload["metadata"][
                    "sequence_context_fetch_status_counts"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
