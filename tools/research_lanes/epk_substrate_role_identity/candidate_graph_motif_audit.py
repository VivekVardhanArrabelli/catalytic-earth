#!/usr/bin/env python3
"""Audit source-free ePK candidate graph motif collisions.

This lane-local helper consumes existing compact candidate evidence plus the
metal/transfer overlay. It emits gamma-site and PDB graph motif rows without
fetching coordinates, writing raw structures, or creating another scalar rescue
rule. Review labels are used only after source-free motif grouping.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from folded_nterminal_stress_eval import (
    FORBIDDEN_PREDICTIVE_FEATURES,
    LANE_ID,
    append_jsonl,
    utc_now,
    write_json,
)


ARTIFACT_ID = "epk_candidate_graph_motif_audit_v1_20260521"
SOURCE_CANDIDATE_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_evidence_v1_20260521.json"
)
SOURCE_TRANSFER_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_gamma_metal_transfer_geometry_probe_v1_20260521.json"
)
SOURCE_CONFLICT_ARTIFACT = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_conflict_decision_v1_20260521.json"
)
LEDGER_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_substrate_role_identity_runs.jsonl"
)
DEFAULT_OUTPUT_PATH = Path(
    "artifacts/research_lanes/epk_substrate_role_identity/"
    "epk_candidate_graph_motif_audit_v1_20260521.json"
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

HARD_CASE_PDBS = {
    "1L0O",
    "1QHA",
    "3QHR",
    "3QHW",
    "3TM0",
    "7B56",
    "9UUR",
    "9UUX",
    "9UW4",
}

SAME_CHAIN_METAL_STRESS_COUNTEREXAMPLES = {
    "3FGU",
    "5XD6",
    "6U1D",
    "6U1E",
    "9OAN",
    "9UW4",
}


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row["source_free_evidence"]


def review_label(row: dict[str, Any]) -> str:
    return row["review_context_for_evaluation_only"]["evaluation_label"]


def is_positive(label: str) -> bool:
    return label == "positive_true_substrate_acceptor"


def label_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(
        sorted(
            Counter(
                row["review_context_for_evaluation_only"]["evaluation_label"]
                for row in rows
            ).items()
        )
    )


def collision_class(labels: list[str]) -> str:
    positives = sum(1 for label in labels if is_positive(label))
    negatives = len(labels) - positives
    if positives and negatives:
        return "mixed_positive_counterexample_motif"
    if positives:
        return "positive_only_motif"
    return "counterexample_only_motif"


def stable_signature_id(fields: dict[str, Any]) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def count_class(value: int | None) -> str:
    if value is None:
        return "count_unavailable"
    if value == 0:
        return "zero"
    if value == 1:
        return "one"
    if value <= 3:
        return "two_or_three"
    return "four_or_more"


def topology_class(e: dict[str, Any]) -> str:
    if e.get("same_chain_topology"):
        return "same_chain_topology"
    if e.get("cross_chain_topology"):
        return "cross_chain_topology"
    return "no_candidate_topology"


def acceptor_residue_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_is_tyr") or e.get("acceptor_residue_code") == "TYR":
        return "tyr_acceptor"
    if e.get("acceptor_residue_code") in {"SER", "THR"}:
        return "ser_thr_acceptor"
    if e.get("acceptor_residue_code") is None:
        return "no_acceptor_residue"
    return "other_acceptor_residue"


def acceptor_terminal_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_resolved_n_terminal_internal_fragment_like"):
        return "n_terminal_internal_fragment_like"
    if e.get("acceptor_resolved_n_terminal_auth_terminal_like"):
        return "n_terminal_auth_terminal_like"
    if e.get("acceptor_is_n_terminal_sty"):
        return "resolved_n_terminal_sty_without_auth_terminal_support"
    return "not_resolved_n_terminal_sty"


def acceptor_chain_size_class(e: dict[str, Any]) -> str:
    if e.get("acceptor_chain_is_short_peptide_like"):
        return "short_peptide_like_acceptor_chain"
    if e.get("acceptor_chain_is_folded_like"):
        return "folded_like_acceptor_chain"
    return "acceptor_chain_size_unclassified"


def ligand_acceptor_relation_class(e: dict[str, Any]) -> str:
    value = e.get("ligand_acceptor_same_sequence_entity")
    if value is True:
        return "same_sequence_entity"
    if value is False:
        return "different_sequence_entity"
    return "sequence_entity_relation_unavailable"


def nested_value(mapping: dict[str, Any], path: list[str], default: str) -> Any:
    value: Any = mapping
    for key in path:
        if not isinstance(value, dict):
            return default
        value = value.get(key)
    if value is None:
        return default
    return value


def candidate_parts(candidate_id: str) -> tuple[str, str]:
    try:
        _, gamma_part, acceptor_part = candidate_id.split("|", 2)
    except ValueError:
        return "gamma=unparsed", "acceptor=unparsed"
    return gamma_part, acceptor_part


def gamma_site_id(row: dict[str, Any]) -> str:
    gamma_part, _ = candidate_parts(row["candidate_id"])
    return f"{row['pdb_id']}|{gamma_part}"


def compact_candidate_digest(row: dict[str, Any]) -> dict[str, Any]:
    e = evidence(row)
    transfer = e.get("phosphate_transfer_geometry", {})
    metal = e.get("gamma_metal_geometry", {})
    return {
        "candidate_id": row["candidate_id"],
        "coordinate_state": e.get("coordinate_state"),
        "source_coordinate_state": e.get("source_coordinate_state"),
        "blocker_class": e.get("blocker_class"),
        "source_blocker_class": e.get("source_blocker_class"),
        "candidate_role_class": e.get("candidate_role_class"),
        "topology_class": topology_class(e),
        "reciprocal_context_class": e.get("reciprocal_context_class"),
        "acceptor_residue_class": acceptor_residue_class(e),
        "acceptor_terminal_class": acceptor_terminal_class(e),
        "acceptor_chain_size_class": acceptor_chain_size_class(e),
        "ligand_acceptor_relation_class": ligand_acceptor_relation_class(e),
        "gamma_metal_shell_class": metal.get("gamma_metal_shell_class"),
        "transfer_geometry_status": transfer.get("transfer_geometry_status"),
        "acceptor_gamma_bridge_angle_class": transfer.get(
            "acceptor_gamma_bridge_angle_class"
        ),
        "distance_transfer_class": (
            "within_preexisting_transfer_geometry_6a"
            if e.get("distance_angstrom") is not None and e["distance_angstrom"] <= 6.0
            else "outside_or_unavailable_preexisting_transfer_geometry_6a"
        ),
    }


def overlay_transfer_evidence(
    candidate_payload: dict[str, Any],
    transfer_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    transfer_rows = {
        row["candidate_id"]: row
        for row in (
            transfer_payload["candidate_transfer_geometry_rows"]
            + transfer_payload["state_only_rows"]
        )
    }
    merged = []
    for row in (
        candidate_payload["candidate_evidence_rows"]
        + candidate_payload["state_only_rows"]
    ):
        merged_row = json.loads(json.dumps(row))
        overlay = transfer_rows.get(row["candidate_id"])
        if overlay:
            overlay_evidence = evidence(overlay)
            base = evidence(merged_row)
            for key in (
                "coordinate_state",
                "blocker_class",
                "source_coordinate_state",
                "source_blocker_class",
                "gamma_metal_geometry",
                "phosphate_transfer_geometry",
            ):
                if key in overlay_evidence:
                    base[key] = overlay_evidence[key]
        merged.append(merged_row)
    return merged


def grouped_by(rows: list[dict[str, Any]], key_fn: Any) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[key_fn(row)].append(row)
    return dict(sorted(grouped.items()))


def gamma_signature_fields(rows: list[dict[str, Any]]) -> dict[str, Any]:
    digests = [compact_candidate_digest(row) for row in rows]
    role_counter = Counter(digest["candidate_role_class"] for digest in digests)
    blocker_counter = Counter(digest["blocker_class"] for digest in digests)
    topology_counter = Counter(digest["topology_class"] for digest in digests)
    return {
        "coordinate_state_set": sorted(
            {str(digest["coordinate_state"]) for digest in digests}
        ),
        "source_coordinate_state_set": sorted(
            {str(digest["source_coordinate_state"]) for digest in digests}
        ),
        "blocker_class_set": sorted({str(digest["blocker_class"]) for digest in digests}),
        "candidate_role_class_set": sorted(
            {str(digest["candidate_role_class"]) for digest in digests}
        ),
        "topology_class_set": sorted({str(digest["topology_class"]) for digest in digests}),
        "reciprocal_context_class_set": sorted(
            {str(digest["reciprocal_context_class"]) for digest in digests}
        ),
        "acceptor_residue_class_set": sorted(
            {str(digest["acceptor_residue_class"]) for digest in digests}
        ),
        "acceptor_terminal_class_set": sorted(
            {str(digest["acceptor_terminal_class"]) for digest in digests}
        ),
        "acceptor_chain_size_class_set": sorted(
            {str(digest["acceptor_chain_size_class"]) for digest in digests}
        ),
        "ligand_acceptor_relation_class_set": sorted(
            {str(digest["ligand_acceptor_relation_class"]) for digest in digests}
        ),
        "gamma_metal_shell_class_set": sorted(
            {str(digest["gamma_metal_shell_class"]) for digest in digests}
        ),
        "candidate_edge_count_class": count_class(len(rows)),
        "unblocked_candidate_count_class": count_class(blocker_counter.get("none", 0)),
        "topology_ambiguity_count_class": count_class(
            blocker_counter.get("topology_ambiguity", 0)
        ),
        "geometry_blocked_count_class": count_class(
            blocker_counter.get("active_gamma_geometry", 0)
        ),
        "same_chain_candidate_count_class": count_class(
            topology_counter.get("same_chain_topology", 0)
        ),
        "cross_chain_candidate_count_class": count_class(
            topology_counter.get("cross_chain_topology", 0)
        ),
        "strict_auth_candidate_count_class": count_class(
            role_counter.get("strict_auth_terminal_guard_candidate", 0)
        ),
        "reciprocal_folded_tyr_candidate_count_class": count_class(
            role_counter.get("reciprocal_folded_tyr_candidate", 0)
        ),
        "internal_fragment_candidate_count_class": count_class(
            blocker_counter.get("internal_fragment_mimicry", 0)
        ),
    }


def gamma_graph_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_rows = [row for row in rows if "gamma=none" not in row["candidate_id"]]
    graph_rows = []
    for site_id, site_rows in grouped_by(candidate_rows, gamma_site_id).items():
        fields = gamma_signature_fields(site_rows)
        signature_id = stable_signature_id(fields)
        pdb_id = site_rows[0]["pdb_id"]
        labels = [review_label(row) for row in site_rows]
        graph_rows.append(
            {
                "row_schema": "epk_gamma_site_graph_motif_v1",
                "gamma_site_id": site_id,
                "pdb_id": pdb_id,
                "source_free_gamma_graph_signature_id": signature_id,
                "source_free_gamma_graph_signature_fields": fields,
                "candidate_count": len(site_rows),
                "candidate_ids": sorted(row["candidate_id"] for row in site_rows),
                "candidate_graph_digest": [
                    compact_candidate_digest(row)
                    for row in sorted(site_rows, key=lambda item: item["candidate_id"])
                ],
                "hard_case": pdb_id in HARD_CASE_PDBS,
                "same_chain_metal_stress_counterexample": (
                    pdb_id in SAME_CHAIN_METAL_STRESS_COUNTEREXAMPLES
                ),
                "review_context_for_evaluation_only": {
                    "evaluation_label": labels[0],
                    "evaluation_group": site_rows[0]["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "evaluation_label_used_only_after_graph_grouping": True,
                },
            }
        )
    return sorted(graph_rows, key=lambda row: (row["pdb_id"], row["gamma_site_id"]))


def state_only_graph_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    state_rows = [row for row in rows if "gamma=none" in row["candidate_id"]]
    graph_rows = []
    for row in state_rows:
        e = evidence(row)
        fields = {
            "coordinate_state": e.get("coordinate_state"),
            "blocker_class": e.get("blocker_class"),
            "availability_class": e.get("availability_class"),
            "terminal_gamma_equivalent_atom_available": e.get(
                "terminal_gamma_equivalent_atom_available"
            ),
            "ligand_state_class": e.get("ligand_state"),
            "candidate_edge_count_class": count_class(0),
        }
        graph_rows.append(
            {
                "row_schema": "epk_state_materialization_graph_motif_v1",
                "gamma_site_id": f"{row['pdb_id']}|gamma=none",
                "pdb_id": row["pdb_id"],
                "source_free_state_graph_signature_id": stable_signature_id(fields),
                "source_free_state_graph_signature_fields": fields,
                "candidate_count": 0,
                "candidate_ids": [row["candidate_id"]],
                "hard_case": row["pdb_id"] in HARD_CASE_PDBS,
                "review_context_for_evaluation_only": {
                    "evaluation_label": review_label(row),
                    "evaluation_group": row["review_context_for_evaluation_only"][
                        "evaluation_group"
                    ],
                    "evaluation_label_used_only_after_graph_grouping": True,
                },
            }
        )
    return sorted(graph_rows, key=lambda row: row["pdb_id"])


def graph_group_rows(
    rows: list[dict[str, Any]],
    signature_key: str,
    fields_key: str,
    row_schema: str,
) -> list[dict[str, Any]]:
    groups = []
    for signature_id, grouped_rows in grouped_by(
        rows,
        lambda row: row[signature_key],
    ).items():
        labels = [
            row["review_context_for_evaluation_only"]["evaluation_label"]
            for row in grouped_rows
        ]
        pdb_ids = sorted({row["pdb_id"] for row in grouped_rows})
        groups.append(
            {
                "row_schema": row_schema,
                signature_key: signature_id,
                fields_key: grouped_rows[0][fields_key],
                "row_count": len(grouped_rows),
                "pdb_count": len(pdb_ids),
                "pdb_ids": pdb_ids,
                "hard_case_pdb_ids": sorted(set(pdb_ids) & HARD_CASE_PDBS),
                "same_chain_metal_stress_counterexample_pdb_ids": sorted(
                    set(pdb_ids) & SAME_CHAIN_METAL_STRESS_COUNTEREXAMPLES
                ),
                "graph_row_ids": sorted(
                    row.get("gamma_site_id", row.get("pdb_id"))
                    for row in grouped_rows
                ),
                "collision_class_for_evaluation_only": collision_class(labels),
                "review_label_counts_for_evaluation_only": dict(
                    sorted(Counter(labels).items())
                ),
            }
        )
    return sorted(
        groups,
        key=lambda row: (
            row["collision_class_for_evaluation_only"]
            != "mixed_positive_counterexample_motif",
            -row["row_count"],
            row[signature_key],
        ),
    )


def conflict_decision_by_pdb(conflict_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["pdb_id"]: row for row in conflict_payload["candidate_conflict_rows"]}


def pdb_graph_signature_fields(
    pdb_id: str,
    site_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    conflict_row: dict[str, Any],
) -> dict[str, Any]:
    site_fields = [
        row["source_free_gamma_graph_signature_fields"] for row in site_rows
    ]
    return {
        "gamma_site_count_class": count_class(len(site_rows)),
        "state_materialization_row_count_class": count_class(len(state_rows)),
        "gamma_site_signature_id_set": sorted(
            row["source_free_gamma_graph_signature_id"] for row in site_rows
        ),
        "state_graph_signature_id_set": sorted(
            row["source_free_state_graph_signature_id"] for row in state_rows
        ),
        "coordinate_state_set": sorted(
            {
                state
                for fields in site_fields
                for state in fields.get("coordinate_state_set", [])
            }
            | {
                row["source_free_state_graph_signature_fields"]["coordinate_state"]
                for row in state_rows
            }
        ),
        "blocker_class_set": sorted(
            {
                blocker
                for fields in site_fields
                for blocker in fields.get("blocker_class_set", [])
            }
            | {
                row["source_free_state_graph_signature_fields"]["blocker_class"]
                for row in state_rows
            }
        ),
        "candidate_role_class_set": sorted(
            {
                role
                for fields in site_fields
                for role in fields.get("candidate_role_class_set", [])
            }
        ),
        "topology_class_set": sorted(
            {
                topology
                for fields in site_fields
                for topology in fields.get("topology_class_set", [])
            }
        ),
        "conflict_class": conflict_row["conflict_class"],
        "source_free_decision_class": conflict_row["source_free_decision_class"],
    }


def pdb_graph_rows(
    gamma_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    conflict_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    conflict_by_pdb = conflict_decision_by_pdb(conflict_payload)
    gamma_by_pdb = grouped_by(gamma_rows, lambda row: row["pdb_id"])
    state_by_pdb = grouped_by(state_rows, lambda row: row["pdb_id"])
    all_pdb_ids = sorted(set(conflict_by_pdb) | set(gamma_by_pdb) | set(state_by_pdb))
    output_rows = []
    for pdb_id in all_pdb_ids:
        conflict_row = conflict_by_pdb[pdb_id]
        fields = pdb_graph_signature_fields(
            pdb_id,
            gamma_by_pdb.get(pdb_id, []),
            state_by_pdb.get(pdb_id, []),
            conflict_row,
        )
        output_rows.append(
            {
                "row_schema": "epk_pdb_candidate_graph_motif_v1",
                "pdb_id": pdb_id,
                "source_free_pdb_graph_signature_id": stable_signature_id(fields),
                "source_free_pdb_graph_signature_fields": fields,
                "gamma_site_graph_row_ids": sorted(
                    row["gamma_site_id"] for row in gamma_by_pdb.get(pdb_id, [])
                ),
                "state_graph_row_ids": sorted(
                    row["gamma_site_id"] for row in state_by_pdb.get(pdb_id, [])
                ),
                "hard_case": pdb_id in HARD_CASE_PDBS,
                "same_chain_metal_stress_counterexample": (
                    pdb_id in SAME_CHAIN_METAL_STRESS_COUNTEREXAMPLES
                ),
                "conflict_class": conflict_row["conflict_class"],
                "source_free_decision_class": conflict_row[
                    "source_free_decision_class"
                ],
                "review_context_for_evaluation_only": {
                    "evaluation_label": conflict_row[
                        "review_context_for_evaluation_only"
                    ]["evaluation_label"],
                    "evaluation_group": conflict_row[
                        "review_context_for_evaluation_only"
                    ]["evaluation_group"],
                    "evaluation_label_used_only_after_graph_grouping": True,
                },
            }
        )
    return output_rows


def mixed_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        group
        for group in groups
        if group["collision_class_for_evaluation_only"]
        == "mixed_positive_counterexample_motif"
    ]


def mixed_groups_by_blocker(groups: list[dict[str, Any]]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for group in mixed_groups(groups):
        for blocker in group["source_free_gamma_graph_signature_fields"].get(
            "blocker_class_set",
            ["blocker_unavailable"],
        ):
            counter[str(blocker)] += 1
    return dict(sorted(counter.items()))


def confusion_from_conflict_decisions(conflict_payload: dict[str, Any]) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {
        "true_positive": [],
        "false_positive": [],
        "true_negative": [],
        "false_negative": [],
        "abstained_positive": [],
        "abstained_negative": [],
    }
    for row in conflict_payload["candidate_conflict_rows"]:
        actual_positive = is_positive(
            row["review_context_for_evaluation_only"]["evaluation_label"]
        )
        decision = row["source_free_decision_class"]
        if decision == "source_free_structural_support_review_only":
            outcome = "true_positive" if actual_positive else "false_positive"
        elif decision == "source_free_blocked_counterevidence_review_only":
            outcome = "false_negative" if actual_positive else "true_negative"
        else:
            outcome = "abstained_positive" if actual_positive else "abstained_negative"
        buckets[outcome].append(row["pdb_id"])
    return {
        "confusion_matrix": {key: len(value) for key, value in buckets.items()},
        "pdb_ids_by_outcome": {key: sorted(value) for key, value in buckets.items()},
    }


def hard_case_digest(
    gamma_groups: list[dict[str, Any]],
    pdb_groups: list[dict[str, Any]],
) -> dict[str, Any]:
    hard_gamma_groups = [
        group
        for group in mixed_groups(gamma_groups)
        if set(group["hard_case_pdb_ids"]) & HARD_CASE_PDBS
    ][:12]
    hard_pdb_groups = [
        group
        for group in mixed_groups(pdb_groups)
        if set(group["hard_case_pdb_ids"]) & HARD_CASE_PDBS
    ][:12]
    return {
        "mixed_gamma_graph_hard_case_groups": hard_gamma_groups,
        "mixed_pdb_graph_hard_case_groups": hard_pdb_groups,
        "hard_reciprocal_trio": {
            "pdb_ids": ["9UUR", "9UUX", "9UW4"],
            "interpretation": (
                "The graph motif audit treats the reciprocal Tyr trio as "
                "topology biology ambiguity: graph structure can route review "
                "but does not identify the true substrate role source-free."
            ),
        },
    }


def build_payload(
    workflow_started_at: str,
    git_sync_status: str,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    candidate_payload = load_json(SOURCE_CANDIDATE_ARTIFACT)
    transfer_payload = load_json(SOURCE_TRANSFER_ARTIFACT)
    conflict_payload = load_json(SOURCE_CONFLICT_ARTIFACT)
    rows = overlay_transfer_evidence(candidate_payload, transfer_payload)
    gamma_rows = gamma_graph_rows(rows)
    state_rows = state_only_graph_rows(rows)
    pdb_rows = pdb_graph_rows(gamma_rows, state_rows, conflict_payload)
    gamma_groups = graph_group_rows(
        gamma_rows,
        "source_free_gamma_graph_signature_id",
        "source_free_gamma_graph_signature_fields",
        "epk_gamma_site_graph_motif_group_v1",
    )
    state_groups = graph_group_rows(
        state_rows,
        "source_free_state_graph_signature_id",
        "source_free_state_graph_signature_fields",
        "epk_state_materialization_graph_motif_group_v1",
    )
    pdb_groups = graph_group_rows(
        pdb_rows,
        "source_free_pdb_graph_signature_id",
        "source_free_pdb_graph_signature_fields",
        "epk_pdb_candidate_graph_motif_group_v1",
    )
    rule_eval = confusion_from_conflict_decisions(conflict_payload)
    mixed_gamma_groups = mixed_groups(gamma_groups)
    mixed_pdb_groups = mixed_groups(pdb_groups)
    mixed_gamma_pdb_ids = sorted(
        {pdb_id for group in mixed_gamma_groups for pdb_id in group["pdb_ids"]}
    )
    mixed_pdb_graph_pdb_ids = sorted(
        {pdb_id for group in mixed_pdb_groups for pdb_id in group["pdb_ids"]}
    )

    primary_outcome = "candidate_evidence_rows_emitted"
    if primary_outcome not in PRIMARY_OUTCOMES:
        raise ValueError(f"invalid primary outcome: {primary_outcome}")

    ended_at = utc_now()
    measured_minutes = round(
        (parse_dt(ended_at) - parse_dt(workflow_started_at)).total_seconds() / 60.0,
        2,
    )

    coordinate_states = Counter(
        str(evidence(row).get("coordinate_state")) for row in rows
    )
    blocker_counts = Counter(str(evidence(row).get("blocker_class")) for row in rows)

    run_record = {
        "lane_id": LANE_ID,
        "started_at": workflow_started_at,
        "ended_at": ended_at,
        "measured_minutes": measured_minutes,
        "hypothesis": (
            "A non-scalar source-free graph motif over gamma sites, candidate "
            "roles, topology, coordinate state, and metal materialization can "
            "reduce uncertainty by showing whether ambiguity is localized to "
            "specific gamma-site/PDB graph structures without making unsafe "
            "non-abstaining substrate-role calls."
        ),
        "diagnostic_rows_added_or_reused": {
            "added_this_run": [],
            "reused_from_candidate_evidence_artifact": (
                candidate_payload["metadata"]["candidate_pair_row_count"]
                + candidate_payload["metadata"]["state_only_row_count"]
            ),
            "reused_from_conflict_decision_artifact": len(
                conflict_payload["candidate_conflict_rows"]
            ),
            "total_pdbs_reused": len(conflict_payload["candidate_conflict_rows"]),
        },
        "candidate_evidence_rows_emitted": {
            "source_free_gamma_site_graph_rows_emitted": len(gamma_rows),
            "source_free_state_materialization_graph_rows_emitted": len(state_rows),
            "source_free_pdb_graph_rows_emitted": len(pdb_rows),
            "source_free_gamma_site_graph_group_rows_emitted": len(gamma_groups),
            "source_free_state_graph_group_rows_emitted": len(state_groups),
            "source_free_pdb_graph_group_rows_emitted": len(pdb_groups),
            "source_candidate_pair_rows_reused": candidate_payload["metadata"][
                "candidate_pair_row_count"
            ],
            "source_state_only_rows_reused": candidate_payload["metadata"][
                "state_only_row_count"
            ],
        },
        "coordinate_states_observed": dict(sorted(coordinate_states.items())),
        "source_free_features_tested": [
            "gamma-site candidate graph motif over role, topology, blocker, and coordinate-state sets",
            "metal-materialization coordinate-state overlay reused as graph node state",
            "candidate edge count classes without new scalar cutoffs",
            "PDB graph motif over gamma-site signature sets plus state materialization rows",
            "post-grouping collision audit with review labels used only after source-free grouping",
        ],
        "forbidden_features_respected": FORBIDDEN_PREDICTIVE_FEATURES,
        "rule_results": {
            "gamma_site_graph_motif_collision_audit_v1": {
                "rule_id": "gamma_site_graph_motif_collision_audit_v1",
                "rule_description": (
                    "Audit-only grouping of source-free gamma-site candidate "
                    "graph motifs. This is review-routing evidence, not a "
                    "production substrate-role identity rule."
                ),
                "gamma_site_graph_row_count": len(gamma_rows),
                "gamma_site_graph_group_count": len(gamma_groups),
                "mixed_gamma_site_graph_group_count": len(mixed_gamma_groups),
                "mixed_gamma_site_graph_pdb_count": len(mixed_gamma_pdb_ids),
                "mixed_gamma_groups_by_blocker_class": mixed_groups_by_blocker(
                    gamma_groups
                ),
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
            "pdb_graph_motif_collision_audit_v1": {
                "rule_id": "pdb_graph_motif_collision_audit_v1",
                "rule_description": (
                    "Audit-only grouping of source-free PDB graph motifs. "
                    "Existing conflict decisions remain abstaining for topology "
                    "and state-specific substrate biology."
                ),
                "pdb_graph_row_count": len(pdb_rows),
                "pdb_graph_group_count": len(pdb_groups),
                "mixed_pdb_graph_group_count": len(mixed_pdb_groups),
                "mixed_pdb_graph_pdb_count": len(mixed_pdb_graph_pdb_ids),
                "confusion_matrix": rule_eval["confusion_matrix"],
                "pdb_ids_by_outcome": rule_eval["pdb_ids_by_outcome"],
                "clears_diagnostic_tranche": False,
                "production_claim_allowed": False,
            },
        },
        "confusion_matrix": rule_eval["confusion_matrix"],
        "decisive_counterexamples": {
            "mixed_gamma_site_graph_pdb_ids": mixed_gamma_pdb_ids,
            "mixed_pdb_graph_pdb_ids": mixed_pdb_graph_pdb_ids,
            "same_chain_metal_stress_counterexamples_in_mixed_gamma_groups": sorted(
                set(mixed_gamma_pdb_ids) & SAME_CHAIN_METAL_STRESS_COUNTEREXAMPLES
            ),
            "hard_case_collision_digest": hard_case_digest(gamma_groups, pdb_groups),
        },
        "false_positive_analysis": {
            "candidate_conflict_abstention_false_positive_pdb_ids": rule_eval[
                "pdb_ids_by_outcome"
            ]["false_positive"],
            "interpretation": (
                "The graph audit does not introduce new non-abstaining calls; "
                "mixed motifs remain blocker evidence and are not promoted to "
                "substrate-role identity."
            ),
        },
        "false_negative_analysis": {
            "candidate_conflict_abstention_false_negative_pdb_ids": rule_eval[
                "pdb_ids_by_outcome"
            ]["false_negative"],
            "abstained_positive_pdb_ids": rule_eval["pdb_ids_by_outcome"][
                "abstained_positive"
            ],
            "interpretation": (
                "Abstained positives remain state-specific product/ADP or "
                "topology cases. Graph motifs localize the blocker but do not "
                "supply biological substrate-role identity source-free."
            ),
        },
        "blocker_classification": {
            "primary_outcome": primary_outcome,
            "classification": "blocker_not_cleared_biology_ambiguity",
            "coordinate_state_counts": dict(sorted(coordinate_states.items())),
            "blocker_class_counts": dict(sorted(blocker_counts.items())),
            "mixed_gamma_site_graph_group_count": len(mixed_gamma_groups),
            "mixed_pdb_graph_group_count": len(mixed_pdb_groups),
            "interpretation": (
                "Graph motifs reduce uncertainty by identifying motif-level "
                "review buckets, but they do not clear substrate-role identity. "
                "Topology and product-state biology still require source-reviewed "
                "adjudication."
            ),
        },
        "next_query": (
            "Do not run another scalar rescue. If this lane resumes, require a "
            "new source-free modality beyond candidate graph topology, metal "
            "materialization, coordinate certainty, exposure, orientation, and "
            "sequence context; otherwise preserve the source-reviewed "
            "adjudication requirement."
        ),
        "primary_outcome": primary_outcome,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "recommendation": (
            "Keep graph motif rows as compact review-only blocker evidence. Do "
            "not claim ePK production readiness, import labels, calibrate "
            "thresholds, or promote topology/state conflicts into production "
            "substrate-role calls."
        ),
        "git_sync_status": git_sync_status,
    }

    return {
        "metadata": {
            "artifact_id": ARTIFACT_ID,
            "created_at": ended_at,
            "workflow_started_at": workflow_started_at,
            "lane_id": LANE_ID,
            "method": "source_free_candidate_graph_motif_collision_audit",
            "review_only": True,
            "source_free_evidence_separated_from_review_context": True,
            "source_labels_used_only_after_graph_grouping": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "threshold_calibrated": False,
            "candidate_specific_threshold_tuning": False,
            "raw_coordinate_files_written": False,
            "forbidden_predictive_features": FORBIDDEN_PREDICTIVE_FEATURES,
            "source_candidate_artifact": str(SOURCE_CANDIDATE_ARTIFACT),
            "source_transfer_artifact": str(SOURCE_TRANSFER_ARTIFACT),
            "source_conflict_artifact": str(SOURCE_CONFLICT_ARTIFACT),
            "output_path": str(output_path),
            "primary_outcome": primary_outcome,
        },
        "hypothesis": run_record["hypothesis"],
        "feature_definitions": {
            "gamma_site_graph_motif": (
                "A source-free categorical graph over one terminal gamma node "
                "and its candidate acceptor edges. It records role, topology, "
                "blocker, coordinate-state, and metal-shell sets plus coarse "
                "edge-count classes."
            ),
            "pdb_candidate_graph_motif": (
                "A source-free PDB-level graph over gamma-site motif signatures "
                "and state materialization rows."
            ),
            "collision_audit_scope": (
                "Review-only blocker evidence. Review labels are used only after "
                "source-free grouping to detect motif collisions."
            ),
        },
        "source_free_gamma_site_graph_rows": gamma_rows,
        "source_free_state_materialization_graph_rows": state_rows,
        "source_free_pdb_graph_rows": pdb_rows,
        "source_free_gamma_site_graph_groups": gamma_groups,
        "source_free_state_materialization_graph_groups": state_groups,
        "source_free_pdb_graph_groups": pdb_groups,
        "summary": {
            "gamma_site_graph_row_count": len(gamma_rows),
            "gamma_site_graph_group_count": len(gamma_groups),
            "mixed_gamma_site_graph_group_count": len(mixed_gamma_groups),
            "mixed_gamma_site_graph_pdb_count": len(mixed_gamma_pdb_ids),
            "state_materialization_graph_row_count": len(state_rows),
            "state_materialization_graph_group_count": len(state_groups),
            "pdb_graph_row_count": len(pdb_rows),
            "pdb_graph_group_count": len(pdb_groups),
            "mixed_pdb_graph_group_count": len(mixed_pdb_groups),
            "mixed_pdb_graph_pdb_count": len(mixed_pdb_graph_pdb_ids),
            "mixed_gamma_groups_by_blocker_class": mixed_groups_by_blocker(
                gamma_groups
            ),
            "coordinate_state_counts": dict(sorted(coordinate_states.items())),
            "blocker_class_counts": dict(sorted(blocker_counts.items())),
            "gamma_graph_label_counts": label_counts(gamma_rows),
            "pdb_graph_label_counts": label_counts(pdb_rows),
        },
        "rules": list(run_record["rule_results"].values()),
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
