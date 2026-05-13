from __future__ import annotations

from typing import Any


def audit_source_scale_limits(
    graph: dict[str, Any],
    labels: list[dict[str, Any]],
    *,
    target_source_entries: int,
    public_target_countable_labels: int = 10000,
    prior_graph: dict[str, Any] | None = None,
    review_debt: dict[str, Any] | None = None,
    label_expansion_candidates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Summarize whether the current source slice can support the next scale target."""
    entry_ids = _mcsa_entry_ids(graph)
    prior_entry_ids = _mcsa_entry_ids(prior_graph) if prior_graph else []
    new_entry_ids = sorted(
        set(entry_ids) - set(prior_entry_ids),
        key=_entry_sort_key,
    )
    observed_source_entries = _source_record_count(graph, fallback=len(entry_ids))
    countable_label_count = _countable_label_count(labels)
    review_debt_meta = review_debt.get("metadata", {}) if review_debt else {}
    candidate_rows = (
        label_expansion_candidates.get("rows", [])
        if label_expansion_candidates
        else []
    )

    source_entry_gap = max(target_source_entries - observed_source_entries, 0)
    public_label_gap = max(public_target_countable_labels - countable_label_count, 0)
    source_limit_reached = observed_source_entries < target_source_entries
    m_csa_only_public_target_blocked = (
        observed_source_entries < public_target_countable_labels
    )
    blockers: list[str] = []
    if source_limit_reached:
        blockers.append("source_has_fewer_entries_than_requested_tranche")
    if m_csa_only_public_target_blocked:
        blockers.append("m_csa_only_scaling_cannot_reach_public_label_target")
    if review_debt_meta.get("new_review_debt_count", 0):
        blockers.append("new_review_debt_requires_repair_or_deferral")
    if not new_entry_ids:
        blockers.append("no_new_source_entries_available")

    if source_limit_reached:
        recommendation = "stop_m_csa_only_tranche_growth_and_scope_external_source_transfer"
    elif review_debt_meta.get("new_review_debt_count", 0):
        recommendation = "repair_or_defer_review_debt_before_promotion"
    else:
        recommendation = "continue_bounded_factory_gated_scaling"

    return {
        "metadata": {
            "method": "source_scale_limit_audit",
            "source": "m_csa",
            "target_source_entries": target_source_entries,
            "observed_source_entries": observed_source_entries,
            "source_entry_gap": source_entry_gap,
            "source_limit_reached": source_limit_reached,
            "prior_source_entries": len(prior_entry_ids) if prior_graph else None,
            "new_source_entry_count": len(new_entry_ids),
            "new_source_entry_ids": new_entry_ids,
            "countable_label_count": countable_label_count,
            "public_target_countable_labels": public_target_countable_labels,
            "public_label_gap": public_label_gap,
            "m_csa_only_public_target_blocked": m_csa_only_public_target_blocked,
            "review_debt_count": review_debt_meta.get("review_debt_count"),
            "new_review_debt_count": review_debt_meta.get("new_review_debt_count"),
            "label_expansion_candidate_count": len(candidate_rows),
            "blocker_count": len(blockers),
            "recommendation": recommendation,
        },
        "blockers": blockers,
        "next_actions": [
            (
                "Do not promote the current preview unless label-factory "
                "acceptance adds clean countable labels."
            ),
            "Treat further scaling beyond the available M-CSA slice as a new methodology.",
            (
                "Scope UniProt or SwissProt transfer with out-of-distribution "
                "calibration, sequence-similarity failure sets, and the "
                "existing heuristic baseline as a control."
            ),
        ],
    }


def _mcsa_entry_ids(graph: dict[str, Any] | None) -> list[str]:
    if not graph:
        return []
    ids = [
        str(node.get("id"))
        for node in graph.get("nodes", [])
        if isinstance(node, dict)
        and node.get("type") == "m_csa_entry"
        and isinstance(node.get("id"), str)
    ]
    return sorted(ids, key=_entry_sort_key)


def _source_record_count(graph: dict[str, Any], *, fallback: int) -> int:
    metadata = graph.get("metadata", {})
    if isinstance(metadata, dict):
        mcsa = metadata.get("mcsa")
        if isinstance(mcsa, dict):
            count = mcsa.get("record_count")
            if isinstance(count, int):
                return count
    return fallback


def _countable_label_count(labels: list[dict[str, Any]]) -> int:
    count = 0
    for label in labels:
        if not isinstance(label, dict):
            continue
        if label.get("review_status") not in {"automation_curated", "expert_reviewed"}:
            continue
        if label.get("label_type") not in {"seed_fingerprint", "out_of_scope"}:
            continue
        count += 1
    return count


def _entry_sort_key(entry_id: str) -> tuple[int, str]:
    if entry_id.startswith("m_csa:"):
        suffix = entry_id.split(":", 1)[1]
        if suffix.isdigit():
            return (int(suffix), entry_id)
    return (10**12, entry_id)
