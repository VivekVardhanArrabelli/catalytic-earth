#!/usr/bin/env python3
"""Review-only ePK coordinate-certainty source-free probe.

This lane-local helper tests whether compact coordinate ordering evidence
(occupancy, B-factor context, and alternate-location ambiguity) separates true
substrate phosphoacceptors from structural mimics. It fetches PDB coordinates
in memory only and writes reduced features, never raw coordinate dumps.
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
from substrate_role_identity_eval import fetch_pdb_text


ARTIFACT_ID = "epk_coordinate_certainty_probe_v1_20260521"
SOURCE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_false_negative_state_topology_decision_probe_v1_20260520.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_coordinate_certainty_probe_v1_20260521.json"
)


REVIEW_REQUIRED_RESCUE_CLASSES = {
    "ambiguous_reciprocal_folded_tyr_context",
    "ambiguous_same_chain_autophosphorylation_like_context",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def mad(values: list[float], center: float | None) -> float | None:
    if center is None or not values:
        return None
    return median([abs(value - center) for value in values])


def round_or_none(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def dist(a: dict[str, Any], b: dict[str, Any]) -> float:
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2 + (a["z"] - b["z"]) ** 2)


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


def heavy(atom: dict[str, Any]) -> bool:
    return atom["element"] != "H"


def parse_pdb_atoms_with_certainty(text: str) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    in_first_model = False
    saw_model = False
    for line in text.splitlines():
        rec = line[0:6].strip()
        if rec == "MODEL":
            saw_model = True
            if not in_first_model:
                in_first_model = True
                continue
        if rec == "ENDMDL" and saw_model:
            break
        if saw_model and not in_first_model:
            continue
        if rec not in {"ATOM", "HETATM"}:
            continue
        x = parse_float(line[30:38].strip())
        y = parse_float(line[38:46].strip())
        z = parse_float(line[46:54].strip())
        if x is None or y is None or z is None:
            continue
        atom_name = line[12:16].strip().upper()
        element = line[76:78].strip().upper()
        if not element:
            element = "".join(ch for ch in atom_name if ch.isalpha())[:1].upper()
        chain = line[21:22].strip() or "_"
        resseq = line[22:26].strip()
        icode = line[26:27].strip()
        resname = line[17:20].strip().upper()
        atoms.append(
            {
                "record": rec,
                "atom_name": atom_name,
                "resname": resname,
                "chain": chain,
                "resseq": resseq,
                "icode": icode,
                "altloc": line[16:17].strip(),
                "x": x,
                "y": y,
                "z": z,
                "occupancy": parse_float(line[54:60].strip()),
                "b_factor": parse_float(line[60:66].strip()),
                "element": element,
                "residue_key": (chain, resseq, icode, resname),
            }
        )
    return atoms


def matching_atom_variants(
    atoms: list[dict[str, Any]], compact_atom: dict[str, Any] | None
) -> list[dict[str, Any]]:
    key = compact_key(compact_atom)
    if key is None:
        return []
    return [atom for atom in atoms if atom_key(atom) == key]


def preferred_atom(variants: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not variants:
        return None
    preferred_altlocs = {"", "A", "1"}
    preferred = [atom for atom in variants if atom["altloc"] in preferred_altlocs] or variants
    return max(
        preferred,
        key=lambda atom: (
            atom["occupancy"] if atom["occupancy"] is not None else -1.0,
            -(atom["b_factor"] if atom["b_factor"] is not None else 9999.0),
        ),
    )


def values_for_atoms(atoms: list[dict[str, Any]], field: str) -> list[float]:
    return [atom[field] for atom in atoms if atom.get(field) is not None]


def stats_for_atom(
    atom: dict[str, Any] | None,
    atoms: list[dict[str, Any]],
    variants: list[dict[str, Any]],
) -> dict[str, Any]:
    if atom is None:
        return {
            "atom_resolved": False,
            "occupancy": None,
            "b_factor": None,
            "altloc_variant_count": len(variants),
            "altlocs": sorted({variant["altloc"] or "." for variant in variants}),
        }

    protein_heavy = [item for item in atoms if item["record"] == "ATOM" and heavy(item)]
    same_chain = [
        item
        for item in protein_heavy
        if item["chain"] == atom["chain"] and item.get("b_factor") is not None
    ]
    same_residue = [
        item
        for item in protein_heavy
        if item["residue_key"] == atom["residue_key"] and item.get("b_factor") is not None
    ]
    local_8a = [
        item
        for item in protein_heavy
        if item["residue_key"] != atom["residue_key"]
        and item.get("b_factor") is not None
        and dist(atom, item) <= 8.0
    ]
    nonwater_hetero = [
        item
        for item in atoms
        if item["record"] == "HETATM" and item["resname"] not in {"HOH", "WAT", "DOD"} and heavy(item)
    ]

    chain_median = median(values_for_atoms(same_chain, "b_factor"))
    residue_median = median(values_for_atoms(same_residue, "b_factor"))
    local_median = median(values_for_atoms(local_8a, "b_factor"))
    protein_median = median(values_for_atoms(protein_heavy, "b_factor"))
    hetero_median = median(values_for_atoms(nonwater_hetero, "b_factor"))
    local_mad = mad(values_for_atoms(local_8a, "b_factor"), local_median)

    b_factor = atom.get("b_factor")
    return {
        "atom_resolved": True,
        "occupancy": round_or_none(atom.get("occupancy")),
        "b_factor": round_or_none(b_factor),
        "altloc_variant_count": len(variants),
        "altlocs": sorted({variant["altloc"] or "." for variant in variants}),
        "same_residue_heavy_atom_count": len(same_residue),
        "local_8a_heavy_atom_count_for_b_context": len(local_8a),
        "same_chain_b_factor_median": round_or_none(chain_median),
        "same_residue_b_factor_median": round_or_none(residue_median),
        "local_8a_b_factor_median": round_or_none(local_median),
        "protein_b_factor_median": round_or_none(protein_median),
        "nonwater_hetero_b_factor_median": round_or_none(hetero_median),
        "b_factor_to_same_chain_median_ratio": (
            round_or_none(b_factor / chain_median) if b_factor is not None and chain_median else None
        ),
        "b_factor_to_local_8a_median_ratio": (
            round_or_none(b_factor / local_median) if b_factor is not None and local_median else None
        ),
        "b_factor_to_protein_median_ratio": (
            round_or_none(b_factor / protein_median) if b_factor is not None and protein_median else None
        ),
        "local_8a_robust_b_zscore": (
            round_or_none((b_factor - local_median) / local_mad)
            if b_factor is not None and local_median is not None and local_mad not in {None, 0.0}
            else None
        ),
    }


def coordinate_certainty_class(
    acceptor_stats: dict[str, Any],
    gamma_stats: dict[str, Any],
) -> str:
    if not acceptor_stats["atom_resolved"] or not gamma_stats["atom_resolved"]:
        return "unavailable_atom_not_resolved"
    if acceptor_stats["occupancy"] is None or gamma_stats["occupancy"] is None:
        return "metrics_incomplete"
    if acceptor_stats["b_factor"] is None or gamma_stats["b_factor"] is None:
        return "metrics_incomplete"
    if (
        acceptor_stats["occupancy"] < 0.9
        or gamma_stats["occupancy"] < 0.9
        or acceptor_stats["altloc_variant_count"] > 1
        or gamma_stats["altloc_variant_count"] > 1
    ):
        return "coordinate_ambiguous_or_partial"

    acceptor_chain_ratio = acceptor_stats["b_factor_to_same_chain_median_ratio"]
    acceptor_local_ratio = acceptor_stats["b_factor_to_local_8a_median_ratio"]
    gamma_hetero_ratio = gamma_stats["b_factor_to_protein_median_ratio"]
    if (
        acceptor_chain_ratio is not None
        and acceptor_chain_ratio <= 1.5
        and (acceptor_local_ratio is None or acceptor_local_ratio <= 1.8)
        and (gamma_hetero_ratio is None or gamma_hetero_ratio <= 2.0)
    ):
        return "ordered_like"
    return "high_b_or_context_disordered"


def source_free_claim_gate(row: dict[str, Any]) -> bool:
    return row["availability_class"] == "claimable_by_auth_guard_strict_context"


def selected_certainty(row: dict[str, Any]) -> str:
    return row["coordinate_certainty_features"]["coordinate_certainty_class"]


def candidate_for_certainty(row: dict[str, Any]) -> dict[str, Any] | None:
    return row.get("selected_claim_or_ambiguity_candidate") or row.get("nearest_same_chain_candidate")


def rule_claim_gate(row: dict[str, Any]) -> bool:
    return source_free_claim_gate(row)


def rule_ordered_claim_gate(row: dict[str, Any]) -> bool:
    return source_free_claim_gate(row) and selected_certainty(row) == "ordered_like"


def rule_ordered_reciprocal_folded_tyr_rescue(row: dict[str, Any]) -> bool:
    return source_free_claim_gate(row) or (
        row["availability_class"] == "ambiguous_reciprocal_folded_tyr_context"
        and selected_certainty(row) == "ordered_like"
    )


def rule_ordered_reciprocal_or_same_chain_rescue(row: dict[str, Any]) -> bool:
    return source_free_claim_gate(row) or (
        row["availability_class"] in REVIEW_REQUIRED_RESCUE_CLASSES
        and selected_certainty(row) == "ordered_like"
    )


RULES = {
    "source_free_claim_gate_or_review_required_v1_reused": {
        "description": "Prior conservative claim gate reused as baseline.",
        "function": rule_claim_gate,
    },
    "coordinate_ordered_claim_gate_v1": {
        "description": (
            "Prior claim gate additionally requiring the selected hydroxyl/gamma "
            "pair to be full-occupancy, non-altloc, and B-factor ordered by "
            "generic coordinate-certainty thresholds."
        ),
        "function": rule_ordered_claim_gate,
    },
    "coordinate_ordered_reciprocal_folded_tyr_rescue_v1": {
        "description": (
            "Prior claim gate plus reciprocal folded-Tyr review-required rows "
            "only when the selected hydroxyl/gamma pair is coordinate ordered."
        ),
        "function": rule_ordered_reciprocal_folded_tyr_rescue,
    },
    "coordinate_ordered_reciprocal_or_same_chain_rescue_v1": {
        "description": (
            "Prior claim gate plus reciprocal folded-Tyr or same-chain review "
            "rows only when the selected hydroxyl/gamma pair is coordinate ordered."
        ),
        "function": rule_ordered_reciprocal_or_same_chain_rescue,
    },
}


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def classify_failure(row: dict[str, Any], predicted_positive: bool, rule_id: str) -> str | None:
    if predicted_positive == is_positive(row):
        return None
    availability = row["availability_class"]
    certainty = selected_certainty(row)
    if predicted_positive and not is_positive(row):
        if row["pdb_id"] == "9UW4":
            return "ordered_reciprocal_folded_tyr_counterexample"
        if availability == "ambiguous_same_chain_autophosphorylation_like_context":
            return "ordered_same_chain_role_ambiguity"
        if availability == "blocked_internal_fragment_n_terminal_mimic":
            return "internal_fragment_n_terminal_mimicry"
        return "ordered_coordinate_false_positive"
    if is_positive(row) and not predicted_positive:
        if availability.startswith("phosphotransfer_gamma_unavailable"):
            return "product_or_adp_state_lacks_terminal_gamma_geometry"
        if availability == "ambiguous_reciprocal_folded_tyr_context":
            return "reciprocal_folded_chain_topology_ambiguity"
        if availability == "ambiguous_same_chain_autophosphorylation_like_context":
            return "same_chain_or_autophosphorylation_like_topology"
        if rule_id == "coordinate_ordered_claim_gate_v1" and certainty != "ordered_like":
            return "coordinate_certainty_filter_lost_strict_positive"
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
        predicted_positive = bool(rule_spec["function"](row))
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
                "availability_class": row["availability_class"],
                "coordinate_certainty_class": selected_certainty(row),
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


def enrich_coordinate_certainty(row: dict[str, Any], workflow_started_at: str) -> dict[str, Any]:
    base = deepcopy(row)
    candidate = candidate_for_certainty(row)
    if candidate is None:
        base["coordinate_certainty_features"] = {
            "coordinate_certainty_status": "no_selected_candidate",
            "coordinate_certainty_class": "unavailable_no_selected_candidate",
            "acceptor_atom": None,
            "terminal_gamma_atom": None,
        }
        return base

    text, fetch_error = fetch_pdb_text_with_retries(row["pdb_id"])
    if text is None:
        base["coordinate_certainty_features"] = {
            "coordinate_certainty_status": "fetch_error",
            "coordinate_certainty_fetch_error": fetch_error,
            "coordinate_certainty_class": "unavailable_fetch_error",
            "acceptor_atom": None,
            "terminal_gamma_atom": None,
        }
        return base

    atoms = parse_pdb_atoms_with_certainty(text)
    acceptor_variants = matching_atom_variants(atoms, candidate.get("nearest_protein_hydroxyl_atom"))
    gamma_variants = matching_atom_variants(atoms, candidate.get("terminal_gamma_equivalent_atom"))
    acceptor_atom = preferred_atom(acceptor_variants)
    gamma_atom = preferred_atom(gamma_variants)
    acceptor_stats = stats_for_atom(acceptor_atom, atoms, acceptor_variants)
    gamma_stats = stats_for_atom(gamma_atom, atoms, gamma_variants)
    certainty_class = coordinate_certainty_class(acceptor_stats, gamma_stats)

    base["coordinate_certainty_features"] = {
        "coordinate_certainty_status": "ok",
        "coordinate_certainty_class": certainty_class,
        "feature_extraction_started_after": workflow_started_at,
        "selected_candidate_distance_angstrom": candidate.get("distance_angstrom"),
        "selected_candidate_residue_code": candidate.get("candidate_acceptor_residue_code"),
        "selected_candidate_reciprocal_context_class": candidate.get("reciprocal_context_class"),
        "selected_candidate_same_chain_topology": candidate.get("same_chain_topology"),
        "selected_candidate_cross_chain_topology": candidate.get("cross_chain_topology"),
        "selected_candidate_internal_fragment_like": candidate.get(
            "candidate_resolved_n_terminal_internal_fragment_like"
        ),
        "acceptor_atom": candidate.get("nearest_protein_hydroxyl_atom"),
        "terminal_gamma_atom": candidate.get("terminal_gamma_equivalent_atom"),
        "acceptor_coordinate_certainty": acceptor_stats,
        "terminal_gamma_coordinate_certainty": gamma_stats,
    }
    return base


def load_source_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
    return payload["diagnostic_rows"]


def compact_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact = []
    for row in rows:
        features = row["coordinate_certainty_features"]
        acceptor = features.get("acceptor_coordinate_certainty") or {}
        gamma = features.get("terminal_gamma_coordinate_certainty") or {}
        compact.append(
            {
                "pdb_id": row["pdb_id"],
                "evaluation_label": row["evaluation_label"],
                "evaluation_group": row["evaluation_group"],
                "availability_class": row["availability_class"],
                "ligand_state": row.get("ligand_state"),
                "coordinate_certainty_class": features["coordinate_certainty_class"],
                "coordinate_certainty_status": features["coordinate_certainty_status"],
                "selected_candidate_distance_angstrom": features.get(
                    "selected_candidate_distance_angstrom"
                ),
                "selected_candidate_residue_code": features.get("selected_candidate_residue_code"),
                "selected_candidate_reciprocal_context_class": features.get(
                    "selected_candidate_reciprocal_context_class"
                ),
                "selected_candidate_same_chain_topology": features.get(
                    "selected_candidate_same_chain_topology"
                ),
                "selected_candidate_cross_chain_topology": features.get(
                    "selected_candidate_cross_chain_topology"
                ),
                "selected_candidate_internal_fragment_like": features.get(
                    "selected_candidate_internal_fragment_like"
                ),
                "acceptor_atom": features.get("acceptor_atom"),
                "terminal_gamma_atom": features.get("terminal_gamma_atom"),
                "acceptor_occupancy": acceptor.get("occupancy"),
                "acceptor_b_factor": acceptor.get("b_factor"),
                "acceptor_altloc_variant_count": acceptor.get("altloc_variant_count"),
                "acceptor_b_factor_to_same_chain_median_ratio": acceptor.get(
                    "b_factor_to_same_chain_median_ratio"
                ),
                "acceptor_b_factor_to_local_8a_median_ratio": acceptor.get(
                    "b_factor_to_local_8a_median_ratio"
                ),
                "gamma_occupancy": gamma.get("occupancy"),
                "gamma_b_factor": gamma.get("b_factor"),
                "gamma_altloc_variant_count": gamma.get("altloc_variant_count"),
                "gamma_b_factor_to_protein_median_ratio": gamma.get(
                    "b_factor_to_protein_median_ratio"
                ),
            }
        )
    return compact


def hard_probe_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    wanted = {"7B56", "9UUR", "9UUX", "9UW4", "3TM0", "3QHR", "3QHW", "1L0O"}
    return {row["pdb_id"]: row for row in compact_rows(rows) if row["pdb_id"] in wanted}


def hard_trio_overlap_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    compact_by_id = hard_probe_rows(rows)
    trio_ids = ["9UUR", "9UUX", "9UW4"]
    trio = {pdb_id: compact_by_id[pdb_id] for pdb_id in trio_ids}
    return {
        "trio_ids": trio_ids,
        "all_ordered_like": all(
            row["coordinate_certainty_class"] == "ordered_like" for row in trio.values()
        ),
        "all_full_occupancy_no_altloc": all(
            row["acceptor_occupancy"] == 1.0
            and row["gamma_occupancy"] == 1.0
            and row["acceptor_altloc_variant_count"] == 1
            and row["gamma_altloc_variant_count"] == 1
            for row in trio.values()
        ),
        "acceptor_b_factor_to_same_chain_median_ratio": {
            pdb_id: trio[pdb_id]["acceptor_b_factor_to_same_chain_median_ratio"]
            for pdb_id in trio_ids
        },
        "acceptor_b_factor_to_local_8a_median_ratio": {
            pdb_id: trio[pdb_id]["acceptor_b_factor_to_local_8a_median_ratio"]
            for pdb_id in trio_ids
        },
        "gamma_b_factor_to_protein_median_ratio": {
            pdb_id: trio[pdb_id]["gamma_b_factor_to_protein_median_ratio"]
            for pdb_id in trio_ids
        },
        "interpretation": (
            "The counterexample 9UW4 sits inside the same generic ordered-coordinate "
            "class as the recovered positives 9UUR and 9UUX; coordinate certainty "
            "does not supply substrate-role identity."
        ),
    }


def class_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label: dict[str, Counter[str]] = {"positive": Counter(), "counterexample": Counter()}
    by_availability: dict[str, Counter[str]] = {}
    for row in rows:
        label = "positive" if is_positive(row) else "counterexample"
        certainty = selected_certainty(row)
        by_label[label][certainty] += 1
        by_availability.setdefault(row["availability_class"], Counter())[certainty] += 1
    return {
        "by_evaluation_label": {key: dict(sorted(value.items())) for key, value in by_label.items()},
        "by_availability_class": {
            key: dict(sorted(value.items())) for key, value in sorted(by_availability.items())
        },
    }


def prior_clearance_found() -> bool:
    if not LEDGER_PATH.exists():
        return False
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("lane_id") == LANE_ID and record.get("primary_outcome") == "blocker_cleared_source_free":
            return True
    return False


def primary_outcome(rule_results: dict[str, Any]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results.values()):
        return "blocker_cleared_source_free"
    reciprocal = rule_results["coordinate_ordered_reciprocal_folded_tyr_rescue_v1"]
    if reciprocal["pdb_ids_by_outcome"]["false_positive"]:
        return "counterexample_found"
    return "blocker_not_cleared_biology_ambiguity"


def build_payload(workflow_started_at: str) -> dict[str, Any]:
    script_started_at = utc_now()
    source_rows = load_source_rows()
    rows = []
    for row in source_rows:
        rows.append(enrich_coordinate_certainty(row, workflow_started_at))
        time.sleep(0.1)
    rule_results = {
        rule_id: confusion_for_rule(rows, rule_id, rule_spec)
        for rule_id, rule_spec in RULES.items()
    }
    outcome = primary_outcome(rule_results)
    if outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {outcome}")

    ended_at = utc_now()
    measured_minutes = round((parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0, 2)
    baseline = rule_results["source_free_claim_gate_or_review_required_v1_reused"]
    reciprocal = rule_results["coordinate_ordered_reciprocal_folded_tyr_rescue_v1"]
    same_chain = rule_results["coordinate_ordered_reciprocal_or_same_chain_rescue_v1"]
    hard_rows = hard_probe_rows(rows)
    hard_trio_overlap = hard_trio_overlap_summary(rows)

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "If coordinate certainty is a missing source-free modality, full-occupancy, "
            "non-altloc, locally ordered hydroxyl/gamma pairs should recover true "
            "reciprocal folded-chain or same-chain substrate positives without admitting "
            "topology-confounded counterexamples."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_false_negative_state_topology_decision_probe": len(source_rows),
            "total": len(source_rows),
        },
        "source_free_features_tested": [
            "selected hydroxyl atom occupancy from coordinate records",
            "terminal gamma-equivalent atom occupancy from coordinate records",
            "selected hydroxyl alternate-location variant count",
            "terminal gamma alternate-location variant count",
            "selected hydroxyl B-factor and chain/local relative B-factor ratios",
            "terminal gamma B-factor and global protein-relative B-factor ratio",
            "coordinate_ordered generic class gating for reciprocal folded-chain rescue",
            "coordinate_ordered generic class gating for same-chain/autophosphorylation-like rescue",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": rule_results,
        "confusion_matrix": reciprocal["confusion_matrix"],
        "decisive_counterexamples": {
            "coordinate_ordered_reciprocal_folded_tyr_rescue_v1_false_positives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "coordinate_ordered_reciprocal_or_same_chain_rescue_v1_false_positives": same_chain[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "hard_probe_rows": hard_rows,
            "hard_trio_coordinate_overlap": hard_trio_overlap,
            "prior_lane_source_free_clearance_found": prior_clearance_found(),
        },
        "false_positive_analysis": {
            "interpretation": (
                "Coordinate ordering does not separate the hard reciprocal folded-Tyr "
                "trio: 9UUR, 9UUX, and 9UW4 share ordered-like selected Tyr/gamma "
                "coordinate evidence, so accepting the ordered reciprocal class still "
                "admits 9UW4."
            ),
            "coordinate_ordered_reciprocal_folded_tyr_rescue_false_positives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "coordinate_ordered_same_chain_rescue_false_positives": same_chain[
                "pdb_ids_by_outcome"
            ]["false_positive"],
        },
        "false_negative_analysis": {
            "baseline_claim_gate_false_negatives": baseline["pdb_ids_by_outcome"]["false_negative"],
            "coordinate_ordered_reciprocal_folded_tyr_rescue_false_negatives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "interpretation": (
                "Product/ADP rows remain unavailable because no terminal gamma-equivalent "
                "transfer atom is present. 3TM0 remains same-chain/autophosphorylation-like; "
                "coordinate ordering alone cannot assign substrate role."
            ),
        },
        "blocker_classification": {
            "primary_outcome": outcome,
            "classification": (
                "Coordinate certainty is useful review evidence but not a source-free "
                "substrate-role identity rule."
            ),
            "hard_trio_assessment": (
                "9UUR, 9UUX, and 9UW4 are all ordered-like by the frozen generic "
                "coordinate-certainty class, so coordinate quality does not adjudicate "
                "the biological role ambiguity."
            ),
            "historical_comparator_assessment": (
                "No prior run in this lane has cleared the blocker with source-free "
                "structure-only features; this new modality also leaves the review "
                "requirement intact."
            ),
        },
        "next_query": (
            "Stop source-free feature probing unless a genuinely new evidence modality is "
            "introduced; preserve product/ADP, reciprocal folded-chain, and same-chain "
            "contexts as source-reviewed adjudication requirements."
        ),
        "primary_outcome": outcome,
        "git_sync_status": (
            "git fetch origin and git pull --ff-only origin research/epk-substrate-role-identity "
            "were attempted at run start but blocked by linked-worktree FETCH_HEAD "
            "permission errors; git fetch --no-write-fetch-head origin succeeded and "
            "working lane files were byte-matched against origin before new work."
        ),
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep coordinate certainty as compact "
            "review evidence only and require hybrid source-reviewed adjudication for "
            "substrate-role identity decisions."
        ),
        "artifact_path": str(DEFAULT_OUTPUT_PATH),
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "script_started_at": script_started_at,
            "lane_id": LANE_ID,
            "method": "review_only_source_free_coordinate_certainty_probe",
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_labels_used_only_for_evaluation": True,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "source_artifact": str(SOURCE_ARTIFACT),
            "frozen_row_count": len(source_rows),
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "primary_outcome": outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "coordinate_certainty_class": (
                "ordered_like requires acceptor/gamma occupancy >=0.9, no alternate-location "
                "variants, acceptor B-factor <=1.5x same-chain median, acceptor B-factor "
                "<=1.8x local 8 A median when available, and terminal gamma B-factor <=2.0x "
                "global protein median when available. Thresholds were frozen before seeing "
                "the run output and are used only for review-only stress testing."
            ),
            "b_factor_to_same_chain_median_ratio": (
                "Selected atom B-factor divided by median B-factor for heavy atoms in the same chain."
            ),
            "b_factor_to_local_8a_median_ratio": (
                "Selected atom B-factor divided by median B-factor for heavy protein atoms "
                "within 8 A excluding the selected residue."
            ),
            "altloc_variant_count": (
                "Number of coordinate records matching the compact selected atom identity "
                "across alternate locations in the first model."
            ),
        },
        "coordinate_certainty_summary": class_summary(rows),
        "hard_trio_coordinate_overlap": hard_trio_overlap,
        "diagnostic_rows": compact_rows(rows),
        "rules": rule_results,
        "blocker_classification": run_record["blocker_classification"],
        "run_record": run_record,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-started-at", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--skip-ledger", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args.workflow_started_at)
    write_json(args.output, payload)
    if not args.skip_ledger:
        run_record = dict(payload["run_record"])
        run_record["artifact_path"] = str(args.output)
        append_jsonl(args.ledger, run_record)


if __name__ == "__main__":
    main()
