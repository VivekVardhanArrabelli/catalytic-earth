#!/usr/bin/env python3
"""Review-only ePK acceptor sequence-context source-free probe.

This helper tests whether residue context around the selected hydroxyl
candidate can resolve ePK substrate-role identity without source text. It
fetches PDB coordinates in memory only and writes compact sequence-window
features, not raw coordinates.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    PRIMARY_OUTCOMES,
    append_jsonl,
    utc_now,
    write_json,
)
from substrate_role_identity_eval import (
    chain_residue_maps,
    fetch_pdb_text,
    parse_pdb_atoms,
)


ARTIFACT_ID = "epk_sequence_context_probe_v1_20260521"
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
    "epk_sequence_context_probe_v1_20260521.json"
)


THREE_TO_ONE = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "SEC": "U",
    "PYL": "O",
}
HYDROXYL_ONE_LETTER = {"S", "T", "Y"}
BASIC = {"K", "R", "H"}
ACIDIC = {"D", "E"}
HYDROPHOBIC = {"A", "I", "L", "M", "F", "W", "V", "Y"}
POLAR = {"S", "T", "N", "Q", "C", "Y"}


AMBIGUOUS_RESCUE_CLASSES = {
    "ambiguous_reciprocal_folded_tyr_context",
    "ambiguous_same_chain_autophosphorylation_like_context",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_source_rows() -> list[dict[str, Any]]:
    return json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))["diagnostic_rows"]


def is_positive(row: dict[str, Any]) -> bool:
    return row["evaluation_label"] == "positive_true_substrate_acceptor"


def selected_candidate(row: dict[str, Any]) -> dict[str, Any] | None:
    selected = row.get("selected_claim_or_ambiguity_candidate")
    if selected:
        return selected
    same_chain = row.get("nearest_same_chain_candidate")
    if same_chain and same_chain.get("distance_angstrom") is not None:
        if same_chain["distance_angstrom"] <= 6.0:
            return same_chain
    return None


def residue_key_from_candidate(candidate: dict[str, Any]) -> tuple[str, str, str, str]:
    atom = candidate["nearest_protein_hydroxyl_atom"]
    return (
        atom["chain_id"],
        str(atom["auth_seq_id"]),
        atom.get("icode") or "",
        atom["residue_code"],
    )


def one_letter(residue_name: str | None) -> str:
    if residue_name is None:
        return "X"
    return THREE_TO_ONE.get(residue_name.upper(), "X")


def empty_sequence_context(status: str) -> dict[str, Any]:
    return {
        "sequence_context_status": status,
        "candidate_residue_one_letter": None,
        "candidate_window_3": None,
        "candidate_window_5": None,
        "candidate_window_3_with_positions": {},
        "candidate_window_5_with_positions": {},
        "candidate_plus1_residue": None,
        "candidate_minus1_residue": None,
        "candidate_plus2_residue": None,
        "candidate_minus2_residue": None,
        "basic_count_minus5_to_minus1": None,
        "basic_count_plus1_to_plus5": None,
        "acidic_count_minus5_to_plus5": None,
        "hydrophobic_count_minus5_to_plus5": None,
        "polar_count_minus5_to_plus5": None,
        "proline_plus1": None,
        "proline_plus2": None,
        "sty_proline_directed": None,
        "basic_cluster_near_acceptor": None,
        "acidic_cluster_near_acceptor": None,
        "charged_context_near_acceptor": None,
        "tyr_has_adjacent_pro_or_charged_context": None,
        "source_free_sequence_support_class": "unavailable",
    }


def sequence_context_for_candidate(
    pdb_id: str, candidate: dict[str, Any] | None
) -> dict[str, Any]:
    if not candidate:
        return {
            "pdb_id": pdb_id,
            "selected_candidate": None,
            "fetch_status": "not_needed_no_candidate",
            **empty_sequence_context("no_selected_candidate"),
        }

    text, fetch_error = fetch_pdb_text(pdb_id)
    compact_candidate = {
        "distance_angstrom": candidate.get("distance_angstrom"),
        "availability_class": None,
        "candidate_acceptor_residue_code": candidate.get("candidate_acceptor_residue_code"),
        "candidate_acceptor_chain": candidate.get("candidate_acceptor_chain"),
        "candidate_acceptor_auth_seq_id_int": candidate.get(
            "candidate_acceptor_auth_seq_id_int"
        ),
        "candidate_acceptor_residue_ordinal_in_chain": candidate.get(
            "candidate_acceptor_residue_ordinal_in_chain"
        ),
        "candidate_acceptor_chain_length": candidate.get("candidate_acceptor_chain_length"),
        "same_chain_topology": candidate.get("same_chain_topology"),
        "cross_chain_topology": candidate.get("cross_chain_topology"),
        "reciprocal_context_class": candidate.get("reciprocal_context_class"),
        "nearest_protein_hydroxyl_atom": candidate.get("nearest_protein_hydroxyl_atom"),
        "terminal_gamma_equivalent_atom": candidate.get("terminal_gamma_equivalent_atom"),
    }
    if text is None:
        return {
            "pdb_id": pdb_id,
            "selected_candidate": compact_candidate,
            "fetch_status": "error",
            "fetch_error": fetch_error,
            **empty_sequence_context("fetch_error"),
        }

    atoms = parse_pdb_atoms(text)
    residues_by_chain, _ = chain_residue_maps(atoms)
    key = residue_key_from_candidate(candidate)
    chain = key[0]
    residues = residues_by_chain.get(chain, [])
    try:
        index = residues.index(key)
    except ValueError:
        return {
            "pdb_id": pdb_id,
            "selected_candidate": compact_candidate,
            "fetch_status": "ok",
            **empty_sequence_context("candidate_residue_not_found_in_model1"),
        }

    offsets: dict[int, str] = {}
    residue_ids: dict[int, dict[str, Any] | None] = {}
    for offset in range(-5, 6):
        target_index = index + offset
        if 0 <= target_index < len(residues):
            residue = residues[target_index]
            code = one_letter(residue[3])
            residue_ids[offset] = {
                "chain_id": residue[0],
                "auth_seq_id": residue[1],
                "icode": residue[2] or None,
                "residue_code": residue[3],
                "one_letter": code,
            }
        else:
            code = "_"
            residue_ids[offset] = None
        offsets[offset] = code

    window_3 = "".join(offsets[offset] for offset in range(-3, 4))
    window_5 = "".join(offsets[offset] for offset in range(-5, 6))
    flank_minus = [offsets[offset] for offset in range(-5, 0)]
    flank_plus = [offsets[offset] for offset in range(1, 6)]
    neighborhood = flank_minus + flank_plus
    candidate_residue = offsets[0]
    basic_minus = sum(1 for code in flank_minus if code in BASIC)
    basic_plus = sum(1 for code in flank_plus if code in BASIC)
    acidic_total = sum(1 for code in neighborhood if code in ACIDIC)
    hydrophobic_total = sum(1 for code in neighborhood if code in HYDROPHOBIC)
    polar_total = sum(1 for code in neighborhood if code in POLAR)
    proline_plus1 = offsets[1] == "P"
    proline_plus2 = offsets[2] == "P"
    sty_proline = candidate_residue in {"S", "T"} and proline_plus1
    basic_cluster = basic_minus + basic_plus >= 2
    acidic_cluster = acidic_total >= 2
    charged_context = basic_cluster or acidic_cluster
    tyr_context = candidate_residue == "Y" and (
        offsets[-1] == "P"
        or proline_plus1
        or basic_minus + basic_plus >= 1
        or acidic_total >= 1
    )
    if sty_proline:
        support_class = "sty_plus1_proline_context"
    elif basic_cluster:
        support_class = "basic_cluster_context"
    elif acidic_cluster:
        support_class = "acidic_cluster_context"
    elif tyr_context:
        support_class = "tyr_adjacent_pro_or_charged_context"
    else:
        support_class = "no_generic_sequence_context_signal"

    return {
        "pdb_id": pdb_id,
        "selected_candidate": compact_candidate,
        "fetch_status": "ok",
        "sequence_context_status": "ok",
        "candidate_residue_one_letter": candidate_residue,
        "candidate_window_3": window_3,
        "candidate_window_5": window_5,
        "candidate_window_3_with_positions": {
            str(offset): residue_ids[offset] for offset in range(-3, 4)
        },
        "candidate_window_5_with_positions": {
            str(offset): residue_ids[offset] for offset in range(-5, 6)
        },
        "candidate_plus1_residue": offsets[1],
        "candidate_minus1_residue": offsets[-1],
        "candidate_plus2_residue": offsets[2],
        "candidate_minus2_residue": offsets[-2],
        "basic_count_minus5_to_minus1": basic_minus,
        "basic_count_plus1_to_plus5": basic_plus,
        "acidic_count_minus5_to_plus5": acidic_total,
        "hydrophobic_count_minus5_to_plus5": hydrophobic_total,
        "polar_count_minus5_to_plus5": polar_total,
        "proline_plus1": proline_plus1,
        "proline_plus2": proline_plus2,
        "sty_proline_directed": sty_proline,
        "basic_cluster_near_acceptor": basic_cluster,
        "acidic_cluster_near_acceptor": acidic_cluster,
        "charged_context_near_acceptor": charged_context,
        "tyr_has_adjacent_pro_or_charged_context": tyr_context,
        "source_free_sequence_support_class": support_class,
    }


def enrich_row(row: dict[str, Any]) -> dict[str, Any]:
    candidate = selected_candidate(row)
    context = sequence_context_for_candidate(row["pdb_id"], candidate)
    if context.get("selected_candidate"):
        context["selected_candidate"]["availability_class"] = row["availability_class"]
    return {
        "pdb_id": row["pdb_id"],
        "evaluation_label": row["evaluation_label"],
        "evaluation_group": row["evaluation_group"],
        "availability_class": row["availability_class"],
        "ligand_state": row["ligand_state"],
        "terminal_gamma_equivalent_atom_available": row[
            "terminal_gamma_equivalent_atom_available"
        ],
        "nearest_protein_hydroxyl_distance_angstrom": row[
            "nearest_protein_hydroxyl_distance_angstrom"
        ],
        "sequence_context": context,
    }


def claim_gate_reused(row: dict[str, Any]) -> bool:
    return row["availability_class"] == "claimable_by_auth_guard_strict_context"


def generic_sequence_support(row: dict[str, Any]) -> bool:
    return row["sequence_context"]["source_free_sequence_support_class"] != (
        "no_generic_sequence_context_signal"
    ) and row["sequence_context"]["source_free_sequence_support_class"] != "unavailable"


def proline_directed_support(row: dict[str, Any]) -> bool:
    return bool(row["sequence_context"]["sty_proline_directed"])


def charged_context_support(row: dict[str, Any]) -> bool:
    context = row["sequence_context"]
    return bool(
        context["basic_cluster_near_acceptor"]
        or context["acidic_cluster_near_acceptor"]
        or context["tyr_has_adjacent_pro_or_charged_context"]
    )


def rule_claim_gate(row: dict[str, Any]) -> bool:
    return claim_gate_reused(row)


def rule_reciprocal_generic_sequence_rescue(row: dict[str, Any]) -> bool:
    return claim_gate_reused(row) or (
        row["availability_class"] == "ambiguous_reciprocal_folded_tyr_context"
        and generic_sequence_support(row)
    )


def rule_ambiguous_generic_sequence_rescue(row: dict[str, Any]) -> bool:
    return claim_gate_reused(row) or (
        row["availability_class"] in AMBIGUOUS_RESCUE_CLASSES
        and generic_sequence_support(row)
    )


def rule_proline_directed_ambiguous_rescue(row: dict[str, Any]) -> bool:
    return claim_gate_reused(row) or (
        row["availability_class"] in AMBIGUOUS_RESCUE_CLASSES
        and proline_directed_support(row)
    )


def rule_charged_context_ambiguous_rescue(row: dict[str, Any]) -> bool:
    return claim_gate_reused(row) or (
        row["availability_class"] in AMBIGUOUS_RESCUE_CLASSES
        and charged_context_support(row)
    )


RuleFn = Callable[[dict[str, Any]], bool]


RULES: dict[str, dict[str, Any]] = {
    "source_free_claim_gate_or_review_required_v1_reused": {
        "description": "Prior conservative auth-guard claim gate reused as the no-false-positive baseline.",
        "function": rule_claim_gate,
    },
    "sequence_context_reciprocal_rescue_v1": {
        "description": (
            "Baseline plus reciprocal folded-Tyr rows when the selected acceptor has a "
            "generic source-free residue-context signal."
        ),
        "function": rule_reciprocal_generic_sequence_rescue,
    },
    "sequence_context_ambiguous_rescue_v1": {
        "description": (
            "Baseline plus reciprocal folded-Tyr or same-chain/autophosphorylation-like "
            "rows when the selected acceptor has any generic sequence-context signal."
        ),
        "function": rule_ambiguous_generic_sequence_rescue,
    },
    "sequence_context_proline_directed_rescue_v1": {
        "description": (
            "Baseline plus ambiguous rows only when the selected Ser/Thr has a +1 Pro "
            "source-free sequence context."
        ),
        "function": rule_proline_directed_ambiguous_rescue,
    },
    "sequence_context_charged_rescue_v1": {
        "description": (
            "Baseline plus ambiguous rows when the selected acceptor has a basic, acidic, "
            "or Tyr-adjacent charged residue-context signal."
        ),
        "function": rule_charged_context_ambiguous_rescue,
    },
}


def outcome_for(row: dict[str, Any], predicted_positive: bool) -> str:
    actual_positive = is_positive(row)
    if predicted_positive and actual_positive:
        return "true_positive"
    if predicted_positive and not actual_positive:
        return "false_positive"
    if not predicted_positive and actual_positive:
        return "false_negative"
    return "true_negative"


def failure_mode(row: dict[str, Any], predicted_positive: bool, rule_id: str) -> str | None:
    outcome = outcome_for(row, predicted_positive)
    if outcome in {"true_positive", "true_negative"}:
        return None
    availability = row["availability_class"]
    if outcome == "false_positive":
        if availability == "ambiguous_reciprocal_folded_tyr_context":
            return "sequence_context_shared_by_reciprocal_folded_tyr_counterexample"
        if availability == "ambiguous_same_chain_autophosphorylation_like_context":
            return "sequence_context_shared_by_same_chain_role_counterexample"
        if availability == "blocked_internal_fragment_n_terminal_mimic":
            return "internal_fragment_n_terminal_mimicry"
        return "sequence_context_role_ambiguity"
    if availability.startswith("phosphotransfer_gamma_unavailable"):
        return "product_or_adp_state_lacks_terminal_gamma_geometry"
    if availability == "ambiguous_reciprocal_folded_tyr_context":
        return "reciprocal_folded_chain_topology_ambiguity"
    if availability == "ambiguous_same_chain_autophosphorylation_like_context":
        return "same_chain_or_autophosphorylation_like_topology"
    if row["sequence_context"]["sequence_context_status"] != "ok":
        return "sequence_context_unavailable"
    return f"not_recovered_by_{rule_id}"


def confusion_for_rule(
    rows: list[dict[str, Any]], rule_id: str, rule_spec: dict[str, Any]
) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
    }
    failures: Counter[str] = Counter()
    decisions = []
    rule_fn: RuleFn = rule_spec["function"]
    for row in rows:
        predicted_positive = bool(rule_fn(row))
        outcome = outcome_for(row, predicted_positive)
        mode = failure_mode(row, predicted_positive, rule_id)
        if mode:
            failures[mode] += 1
        buckets[outcome].append(row["pdb_id"])
        decisions.append(
            {
                "pdb_id": row["pdb_id"],
                "actual_label": row["evaluation_label"],
                "predicted_positive": predicted_positive,
                "outcome": outcome,
                "failure_mode": mode,
                "availability_class": row["availability_class"],
                "sequence_support_class": row["sequence_context"][
                    "source_free_sequence_support_class"
                ],
                "candidate_window_5": row["sequence_context"]["candidate_window_5"],
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
        "failure_mode_counts": dict(sorted(failures.items())),
        "decisions": decisions,
        "clears_diagnostic_tranche": not buckets["false_positive"] and not buckets["false_negative"],
    }


def compact_rule_results(rule_results: dict[str, Any]) -> dict[str, Any]:
    return {
        rule_id: {
            "confusion_matrix": result["confusion_matrix"],
            "pdb_ids_by_outcome": result["pdb_ids_by_outcome"],
            "failure_mode_counts": result["failure_mode_counts"],
            "clears_diagnostic_tranche": result["clears_diagnostic_tranche"],
        }
        for rule_id, result in rule_results.items()
    }


def hard_trio_overlap(rows: list[dict[str, Any]]) -> dict[str, Any]:
    trio_ids = {"9UUR", "9UUX", "9UW4"}
    trio_rows = [row for row in rows if row["pdb_id"] in trio_ids]
    windows = {
        row["pdb_id"]: {
            "evaluation_label": row["evaluation_label"],
            "availability_class": row["availability_class"],
            "candidate_window_5": row["sequence_context"]["candidate_window_5"],
            "candidate_window_3": row["sequence_context"]["candidate_window_3"],
            "sequence_support_class": row["sequence_context"][
                "source_free_sequence_support_class"
            ],
            "selected_candidate": row["sequence_context"]["selected_candidate"],
        }
        for row in trio_rows
    }
    unique_windows = sorted(
        {
            row["sequence_context"]["candidate_window_5"]
            for row in trio_rows
            if row["sequence_context"]["candidate_window_5"] is not None
        }
    )
    return {
        "trio_rows": windows,
        "unique_candidate_window_5_count": len(unique_windows),
        "unique_candidate_window_5": unique_windows,
        "interpretation": (
            "If the positive reciprocal folded-Tyr rows and 9UW4 share the same selected "
            "acceptor sequence window, sequence context cannot separate them without "
            "adding non-sequence evidence or source-reviewed biological role labels."
        ),
    }


def support_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label: dict[str, Counter[str]] = {"positive": Counter(), "counterexample": Counter()}
    by_availability: dict[str, Counter[str]] = {}
    for row in rows:
        label_key = "positive" if is_positive(row) else "counterexample"
        support_class = row["sequence_context"]["source_free_sequence_support_class"]
        by_label[label_key][support_class] += 1
        by_availability.setdefault(row["availability_class"], Counter())[support_class] += 1
    return {
        "by_label": {key: dict(sorted(counter.items())) for key, counter in by_label.items()},
        "by_availability_class": {
            key: dict(sorted(counter.items())) for key, counter in sorted(by_availability.items())
        },
    }


def sequence_window_collision_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_window: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        window = row["sequence_context"]["candidate_window_5"]
        if not window:
            continue
        by_window.setdefault(window, []).append(
            {
                "pdb_id": row["pdb_id"],
                "evaluation_label": row["evaluation_label"],
                "availability_class": row["availability_class"],
                "sequence_support_class": row["sequence_context"][
                    "source_free_sequence_support_class"
                ],
            }
        )
    collisions = {}
    for window, members in sorted(by_window.items()):
        labels = {member["evaluation_label"] for member in members}
        if len(labels) < 2:
            continue
        collisions[window] = members
    return {
        "mixed_label_window_count": len(collisions),
        "mixed_label_windows": collisions,
        "interpretation": (
            "Exact resolved sequence windows that contain both positives and "
            "counterexamples cannot support a source-free substrate-role identity claim "
            "without additional non-sequence evidence."
        ),
    }


def primary_outcome(rule_results: dict[str, Any], hard_overlap: dict[str, Any]) -> str:
    if any(result["clears_diagnostic_tranche"] for result in rule_results.values()):
        return "blocker_cleared_source_free"
    reciprocal = rule_results["sequence_context_reciprocal_rescue_v1"]
    if reciprocal["pdb_ids_by_outcome"]["false_positive"]:
        return "counterexample_found"
    if hard_overlap["unique_candidate_window_5_count"] == 1:
        return "blocker_not_cleared_biology_ambiguity"
    return "blocker_not_cleared_method_weakness"


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


def build_payload(workflow_started_at: str) -> dict[str, Any]:
    script_started_at = utc_now()
    source_rows = load_source_rows()
    rows = []
    for row in source_rows:
        rows.append(enrich_row(row))
        time.sleep(0.05)
    rule_results = {
        rule_id: confusion_for_rule(rows, rule_id, spec)
        for rule_id, spec in RULES.items()
    }
    hard_overlap = hard_trio_overlap(rows)
    window_collisions = sequence_window_collision_summary(rows)
    outcome = primary_outcome(rule_results, hard_overlap)
    if outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {outcome}")

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )
    baseline = rule_results["source_free_claim_gate_or_review_required_v1_reused"]
    reciprocal = rule_results["sequence_context_reciprocal_rescue_v1"]
    ambiguous = rule_results["sequence_context_ambiguous_rescue_v1"]
    proline = rule_results["sequence_context_proline_directed_rescue_v1"]
    charged = rule_results["sequence_context_charged_rescue_v1"]

    false_positive_ids = sorted(
        {
            pdb_id
            for result in rule_results.values()
            for pdb_id in result["pdb_ids_by_outcome"]["false_positive"]
        }
    )
    false_negative_ids = sorted(
        {
            pdb_id
            for result in rule_results.values()
            for pdb_id in result["pdb_ids_by_outcome"]["false_negative"]
        }
    )

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "Source-free acceptor sequence context reconstructed from resolved PDB "
            "polymer coordinates can identify true kinase substrate phosphoacceptors "
            "among ambiguous reciprocal folded-chain and same-chain hydroxyl candidates."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_false_negative_state_topology_decision_probe": len(source_rows),
            "total": len(source_rows),
        },
        "source_free_features_tested": [
            "selected acceptor resolved polymer sequence window +/-3 and +/-5 residues",
            "candidate residue one-letter class from coordinate residue code",
            "plus-one and plus-two proline indicators",
            "basic residue counts upstream and downstream of acceptor",
            "acidic, hydrophobic, and polar residue counts around acceptor",
            "generic residue-chemistry support classes independent of source text",
            "sequence-context gates for reciprocal folded-chain and same-chain rescue",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": compact_rule_results(rule_results),
        "confusion_matrix": reciprocal["confusion_matrix"],
        "decisive_counterexamples": {
            "sequence_context_reciprocal_rescue_false_positives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "sequence_context_ambiguous_rescue_false_positives": ambiguous[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "hard_reciprocal_trio": ["9UUR", "9UUX", "9UW4"],
            "hard_trio_sequence_overlap": hard_overlap,
            "sequence_window_label_collisions": window_collisions,
            "prior_lane_source_free_clearance_found": prior_clearance_found(),
        },
        "false_positive_analysis": {
            "interpretation": (
                "The sequence-context rescue that recovers 9UUR and 9UUX also admits "
                "9UW4. 9UUR and 9UW4 share the exact selected Tyr204 resolved window, "
                "while 9UUX has a one-window-residue difference but the same Tyr204 "
                "residue-chemistry support class."
            ),
            "source_free_claim_gate_false_positives": baseline["pdb_ids_by_outcome"][
                "false_positive"
            ],
            "sequence_context_reciprocal_rescue_false_positives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "sequence_context_ambiguous_rescue_false_positives": ambiguous[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "sequence_context_proline_directed_false_positives": proline[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "sequence_context_charged_false_positives": charged["pdb_ids_by_outcome"][
                "false_positive"
            ],
        },
        "false_negative_analysis": {
            "source_free_claim_gate_false_negatives": baseline["pdb_ids_by_outcome"][
                "false_negative"
            ],
            "sequence_context_reciprocal_rescue_false_negatives": reciprocal[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "sequence_context_proline_directed_false_negatives": proline[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "interpretation": (
                "Product/ADP rows remain unavailable to terminal-gamma transfer geometry; "
                "strict proline-only sequence context avoids the 9UW4 reciprocal false "
                "positive but does not recover the reciprocal Tyr positives."
            ),
        },
        "blocker_classification": {
            "primary_outcome": outcome,
            "classification": (
                "Sequence context is useful compact review evidence, but it is not a "
                "source-free ePK substrate-role identity rule on the frozen diagnostic set."
            ),
            "hard_trio_assessment": (
                "9UUR, 9UUX, and 9UW4 share the selected Tyr204 residue-chemistry "
                "support class, and 9UUR/9UW4 share the exact resolved window. Any "
                "generic sequence-context rule accepting that reciprocal Tyr class "
                "recovers positives by also accepting the counterexample."
            ),
            "historical_comparator_assessment": (
                "Within this lane, no comparable ePK substrate-role blocker has cleared "
                "with source-free nearest-atom, terminal-index, reciprocal-context, "
                "local-exposure, active-site-orientation, state/topology, coordinate-"
                "certainty, or sequence-context features."
            ),
        },
        "next_query": (
            "Do not add more scalar source-free probes unless a genuinely new evidence "
            "modality is available; preserve product/ADP, reciprocal folded-chain, and "
            "same-chain/autophosphorylation-like cases as source-reviewed adjudication "
            "requirements."
        ),
        "primary_outcome": outcome,
        "git_sync_status": (
            "git fetch origin and git pull --ff-only origin research/epk-substrate-role-identity "
            "were attempted at run start but blocked by linked-worktree FETCH_HEAD "
            "permission errors; git fetch --no-write-fetch-head origin succeeded and "
            "working lane files were compared against origin-visible state before new work."
        ),
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Do not claim ePK production readiness. Keep sequence context as review-only "
            "evidence and require hybrid source-reviewed adjudication for substrate-role "
            "identity in ambiguous ePK cases."
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
            "method": "review_only_source_free_sequence_context_probe",
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
            "candidate_window_5": (
                "Resolved model-1 polymer residues at offsets -5..+5 around the selected "
                "candidate hydroxyl residue, derived only from coordinate residue records."
            ),
            "source_free_sequence_support_class": (
                "Frozen residue-chemistry classes: Ser/Thr +1 Pro, basic cluster, acidic "
                "cluster, Tyr with adjacent Pro or charged context, or no generic signal."
            ),
            "sequence_context_rescue_rules": (
                "Review-only stress rules that add sequence-context support to prior "
                "auth-guard claims for ambiguous reciprocal or same-chain rows."
            ),
        },
        "sequence_context_summary": support_summary(rows),
        "hard_trio_sequence_overlap": hard_overlap,
        "sequence_window_label_collisions": window_collisions,
        "diagnostic_rows": rows,
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
