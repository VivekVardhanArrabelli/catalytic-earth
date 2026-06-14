"""Novelty / saturation admission gate for the climb's incoming supply.

The 2026-06-10 governor measured the missing dimension: we had deduped only on
EXACT accession / sequence-SHA, so near-duplicate orthologs and lane saturation
flowed straight in (16.3% of measurable expansion rows sit in near-duplicate
clusters; the OOS kinase/peroxidase lanes are saturated). The governor was a
*report*. This is the *gate* it implies -- an online, non-destructive filter that
sits AFTER the exact-dup screen and decides, per candidate, whether it adds genuine
diversity or merely re-saturates an already-full cluster.

It reuses the governor's cluster key
``(fingerprint_or_scope, full_EC, organism, sequence_length_bin)`` (single source
of truth -- the extractors are imported from ``coverage_redundancy_audit``) plus
reaction-id novelty, and folds in the balance policy: HOLE / under-floor
fingerprints are admitted greedily (we need their volume), over-cap fingerprints
are rejected unless they bring genuinely new chemistry (a new reaction), and
balanced fingerprints admit only novel rows while throttling redundant orthologs
beyond a per-cluster cap.

Three surfaces:

1. ``build_diversity_state`` -- the occupied-cluster / per-fingerprint
   reaction+organism state from the current registries.
2. ``evaluate_candidate`` / ``evaluate_batch`` -- the gate. Operates on
   registry-shaped label dicts (exactly what an engine preview's ``applied_labels``
   are), so it plugs directly into the existing
   ``apply-external-annotation-anchored-import`` path: feed a preview's
   ``applied_labels`` through the gate, apply only the ADMIT set.
3. ``self_audit`` -- retrospectively runs the gate over the existing 1,710
   expansion labels (seeded with the frozen benchmark only) to quantify how much
   of what we already imported the policy would have throttled/rejected as
   redundant -- a concrete read on baked-in redundancy.

NON-DESTRUCTIVE: this module writes no registry and emits no labels. It produces an
admit/throttle/reject decision report; the apply step (separate, authorized) is
what actually writes.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .coverage_redundancy_audit import (
    ALL_FINGERPRINTS,
    DEFAULT_CAP_CEILING,
    DEFAULT_HOLE_THRESHOLD,
    DEFAULT_TARGET_FLOOR,
    _full_ec_signature,
    _load_json,
    _organism,
    _reaction_ids,
    _sequence_length,
    _sequence_length_bin,
)

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# How many near-duplicate rows (same cluster key) are allowed before further
# additions to that cluster are throttled as redundant orthologs.
DEFAULT_PER_CLUSTER_CAP = 3

# Optional hard ceiling on labels per distinct Rhea reaction within a scope. This is
# the durable systemic counterpart to the reaction-aware family cap: it stops a single
# reaction from accumulating endless organism/sequence orthologs even when each new
# row carries a new organism. ``None`` keeps the gate's historical behavior (no
# per-reaction ceiling) so retrospective replays are unchanged; forward callers
# (runners, the saturation trim) pass a concrete value (~10-15). It is enforced only
# once a fingerprint is at/above the floor, so single-reaction mechanisms can still
# reach the 100-floor before the ceiling bites -- it bounds depth ABOVE what reaction
# diversity earns, it does not drop single-reaction mechanisms.
DEFAULT_PER_REACTION_CAP: int | None = None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _scope(row: dict[str, Any]) -> str:
    return row.get("fingerprint_id") or "out_of_scope"


def cluster_key(row: dict[str, Any]) -> tuple[str, tuple[str, ...], str | None, str]:
    """The governor's near-duplicate cluster key for a registry-shaped row."""
    return (
        _scope(row),
        _full_ec_signature(row),
        _organism(row),
        _sequence_length_bin(_sequence_length(row)),
    )


class DiversityState:
    """Mutable diversity bookkeeping the gate reads and updates as it admits."""

    def __init__(self) -> None:
        self.cluster_counts: Counter = Counter()
        self.fingerprint_counts: Counter = Counter()
        self.reactions_by_scope: dict[str, set[str]] = defaultdict(set)
        self.organisms_by_scope: dict[str, set[str]] = defaultdict(set)
        # scope -> {reaction_id: occupancy} for the per-reaction ceiling
        self.reaction_counts_by_scope: dict[str, Counter] = defaultdict(Counter)

    def absorb(self, row: dict[str, Any]) -> None:
        scope = _scope(row)
        self.cluster_counts[cluster_key(row)] += 1
        if row.get("label_type") == "seed_fingerprint" and row.get("fingerprint_id"):
            self.fingerprint_counts[row["fingerprint_id"]] += 1
        reactions = _reaction_ids(row)
        self.reactions_by_scope[scope].update(reactions)
        for rid in reactions:
            self.reaction_counts_by_scope[scope][rid] += 1
        org = _organism(row)
        if org:
            self.organisms_by_scope[scope].add(org)

    def snapshot(self) -> dict[str, Any]:
        return {
            "distinct_clusters": len(self.cluster_counts),
            "fingerprint_counts": dict(sorted(self.fingerprint_counts.items())),
            "distinct_reactions_by_scope": {
                k: len(v) for k, v in sorted(self.reactions_by_scope.items())
            },
        }


def build_diversity_state(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
) -> DiversityState:
    state = DiversityState()
    for row in frozen:
        state.absorb(row)
    for row in expansion:
        state.absorb(row)
    return state


def evaluate_candidate(
    candidate: dict[str, Any],
    state: DiversityState,
    *,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    per_reaction_cap: int | None = DEFAULT_PER_REACTION_CAP,
) -> dict[str, Any]:
    """Decide ADMIT / THROTTLE / REJECT for one candidate (post exact-dedup).

    Decisions (the gate never writes; this is an advisory partition):
    - ``admit``           -- adds diversity (new cluster, or hole/under-floor volume).
    - ``throttle``        -- a redundant ortholog: its cluster is already at the
                             per-cluster cap and it brings no new reaction/organism;
                             or every reaction it carries is already at the
                             per-reaction ceiling (and the fingerprint is past floor).
    - ``reject``          -- an over-cap fingerprint with no new chemistry.
    """
    scope = _scope(candidate)
    key = cluster_key(candidate)
    cluster_occupancy = state.cluster_counts.get(key, 0)
    reactions = set(_reaction_ids(candidate))
    org = _organism(candidate)
    is_seed = candidate.get("label_type") == "seed_fingerprint" and candidate.get(
        "fingerprint_id"
    )
    fp = candidate.get("fingerprint_id") if is_seed else None
    fp_count = state.fingerprint_counts.get(fp, 0) if fp else None

    new_reaction = bool(reactions - state.reactions_by_scope.get(scope, set()))
    new_organism = bool(org and org not in state.organisms_by_scope.get(scope, set()))
    new_cluster = cluster_occupancy == 0
    novelty_score = round(
        0.5 * new_cluster + 0.35 * new_reaction + 0.15 * new_organism, 3
    )

    # Balance status of the candidate's fingerprint (seed only).
    if fp is not None and fp_count is not None:
        if fp_count <= hole_threshold:
            balance = "hole"
        elif fp_count < target_floor:
            balance = "under_floor"
        elif fp_count > cap_ceiling:
            balance = "over_cap"
        else:
            balance = "balanced"
    else:
        balance = "out_of_scope"

    redundant = (not new_cluster) and cluster_occupancy >= per_cluster_cap and (
        not new_reaction
    ) and (not new_organism)

    # --- decision policy --------------------------------------------------
    if balance in ("hole", "under_floor"):
        # we need this fingerprint's volume; admit unless it is a pure redundant
        # ortholog (cluster already saturated, no new reaction/organism)
        if redundant:
            decision, reason = "throttle", "needed_fingerprint_but_redundant_ortholog"
        else:
            decision, reason = "admit", f"closes_{balance}_fingerprint"
    elif balance == "over_cap":
        if new_reaction:
            decision, reason = "admit", "over_cap_but_new_reaction_chemistry"
        else:
            decision, reason = "reject", "fingerprint_over_cap_no_new_chemistry"
    else:  # balanced seed OR out_of_scope
        if new_cluster or new_reaction or new_organism:
            if cluster_occupancy >= per_cluster_cap and not (new_reaction or new_organism):
                decision, reason = "throttle", "cluster_saturated_only_marginal_novelty"
            else:
                decision, reason = "admit", "adds_diversity"
        else:
            decision, reason = "throttle", "redundant_no_novelty_signal"

    # --- per-reaction ceiling (durable systemic fix) ----------------------
    # Once a fingerprint is at/above floor, a row that only deepens already-saturated
    # reactions (no new reaction) is throttled even if its organism is new -- this is
    # how "no single reaction dominates even when the organism is new" is enforced.
    # Hole/under-floor families are exempt so they can still reach the floor.
    reaction_occupancy = (
        {r: state.reaction_counts_by_scope.get(scope, {}).get(r, 0) for r in reactions}
        if reactions
        else {}
    )
    per_reaction_saturated = (
        per_reaction_cap is not None
        and reactions
        and not new_reaction
        and balance not in ("hole", "under_floor")
        and all(occ >= per_reaction_cap for occ in reaction_occupancy.values())
    )
    if per_reaction_saturated and decision == "admit":
        decision, reason = "throttle", "reaction_saturated_per_reaction_cap"

    return {
        "entry_id": candidate.get("entry_id"),
        "decision": decision,
        "reason": reason,
        "scope": scope,
        "balance": balance,
        "cluster_occupancy_before": cluster_occupancy,
        "per_cluster_cap": per_cluster_cap,
        "new_cluster": new_cluster,
        "new_reaction": new_reaction,
        "new_organism": new_organism,
        "novelty_score": novelty_score,
        "per_reaction_cap": per_reaction_cap,
        "per_reaction_saturated": per_reaction_saturated,
        "max_reaction_occupancy_before": (
            max(reaction_occupancy.values()) if reaction_occupancy else 0
        ),
    }


def evaluate_batch(
    candidates: list[dict[str, Any]],
    state: DiversityState,
    *,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    per_reaction_cap: int | None = DEFAULT_PER_REACTION_CAP,
    update_state_on_admit: bool = True,
) -> dict[str, Any]:
    """Partition a candidate batch, updating state so within-batch dups also gate.

    Hole/under-floor candidates are evaluated first so scarce-fingerprint volume is
    admitted before the per-cluster budget is spent on common lanes.
    """
    def _priority(row: dict[str, Any]) -> int:
        fp = row.get("fingerprint_id")
        cnt = state.fingerprint_counts.get(fp, 0) if fp else None
        if cnt is None:
            return 3
        if cnt <= hole_threshold:
            return 0
        if cnt < target_floor:
            return 1
        return 2

    ordered = sorted(enumerate(candidates), key=lambda item: (_priority(item[1]), item[0]))

    decisions = []
    counts: Counter = Counter()
    reason_counts: Counter = Counter()
    admitted_rows = []
    for _, candidate in ordered:
        result = evaluate_candidate(
            candidate,
            state,
            per_cluster_cap=per_cluster_cap,
            target_floor=target_floor,
            cap_ceiling=cap_ceiling,
            hole_threshold=hole_threshold,
            per_reaction_cap=per_reaction_cap,
        )
        decisions.append(result)
        counts[result["decision"]] += 1
        reason_counts[result["reason"]] += 1
        if result["decision"] == "admit":
            admitted_rows.append(candidate)
            if update_state_on_admit:
                state.absorb(candidate)

    return {
        "candidates": len(candidates),
        "decision_counts": dict(sorted(counts.items())),
        "reason_counts": dict(sorted(reason_counts.items())),
        "admit_entry_ids": [r.get("entry_id") for r in admitted_rows],
        "decisions": decisions,
    }


def self_audit(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
    *,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    per_reaction_cap: int | None = DEFAULT_PER_REACTION_CAP,
) -> dict[str, Any]:
    """Replay the existing expansion through the gate (seeded with frozen only).

    Quantifies how much baked-in redundancy the policy would have throttled if it
    had been live during the expansion. Read-only -- nothing is removed.
    """
    state = DiversityState()
    for row in frozen:
        state.absorb(row)
    # Evaluate expansion in registry order WITHOUT the balance reordering -- this is
    # a retrospective replay, so we score each row against the state built from
    # everything admitted before it.
    decisions: Counter = Counter()
    reason_counts: Counter = Counter()
    throttled_by_scope: Counter = Counter()
    sample: list[dict[str, Any]] = []
    for row in expansion:
        result = evaluate_candidate(
            row,
            state,
            per_cluster_cap=per_cluster_cap,
            target_floor=target_floor,
            cap_ceiling=cap_ceiling,
            hole_threshold=hole_threshold,
            per_reaction_cap=per_reaction_cap,
        )
        decisions[result["decision"]] += 1
        reason_counts[result["reason"]] += 1
        if result["decision"] != "admit":
            throttled_by_scope[result["scope"]] += 1
            if len(sample) < 15:
                sample.append(result)
        state.absorb(row)
    total = len(expansion)
    non_admit = total - decisions.get("admit", 0)
    return {
        "expansion_rows": total,
        "decision_counts": dict(sorted(decisions.items())),
        "reason_counts": dict(sorted(reason_counts.items())),
        "would_not_readmit": non_admit,
        "would_not_readmit_fraction": round(non_admit / total, 4) if total else 0.0,
        "non_admit_by_scope_top": dict(throttled_by_scope.most_common(12)),
        "non_admit_samples": sample,
    }


def build_novelty_admission_gate_audit(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
    *,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    per_reaction_cap: int | None = DEFAULT_PER_REACTION_CAP,
) -> dict[str, Any]:
    state = build_diversity_state(frozen, expansion)
    audit = self_audit(
        frozen,
        expansion,
        per_cluster_cap=per_cluster_cap,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        hole_threshold=hole_threshold,
        per_reaction_cap=per_reaction_cap,
    )
    return {
        "audit": "novelty_admission_gate",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "policy": {
            "per_cluster_cap": per_cluster_cap,
            "target_floor": target_floor,
            "cap_ceiling": cap_ceiling,
            "hole_threshold": hole_threshold,
            "per_reaction_cap": per_reaction_cap,
            "cluster_key": "(fingerprint_or_scope, full_ec, organism, sequence_length_bin)",
            "decision_model": (
                "post exact-dedup gate: hole/under-floor admit unless redundant "
                "ortholog; over-cap reject unless new reaction; balanced/OOS admit "
                "only on novelty, throttle saturated clusters"
            ),
        },
        "current_state": state.snapshot(),
        "self_audit": audit,
        "usage": (
            "feed an engine preview's applied_labels through evaluate_batch against "
            "build_diversity_state(frozen, expansion); apply only the ADMIT set via "
            "apply-external-annotation-anchored-import"
        ),
        "guardrails": {
            "frozen_benchmark_written": False,
            "expansion_registry_written": False,
            "labels_emitted": 0,
            "gate_is_advisory_apply_step_is_separate": True,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    sa = audit["self_audit"]
    p = audit["policy"]
    lines = [
        "# Novelty / Saturation Admission Gate",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "An online, non-destructive filter that sits AFTER the exact "
        "accession/sequence-SHA screen and admits incoming candidates only when "
        "they add diversity -- closing the near-duplicate / lane-saturation gap the "
        "governor measured. Writes no registry; emits no labels.",
        "",
        "## Policy",
        "",
        f"- Cluster key: {p['cluster_key']}.",
        f"- Per-cluster cap {p['per_cluster_cap']}; floor {p['target_floor']}; cap "
        f"ceiling {p['cap_ceiling']}; hole threshold {p['hole_threshold']}.",
        f"- {p['decision_model']}.",
        "",
        "## Retrospective self-audit (existing expansion replayed through the gate)",
        "",
        f"- Expansion rows: {sa['expansion_rows']}.",
        f"- Decisions: {sa['decision_counts']}.",
        f"- Would NOT re-admit (redundant under policy): {sa['would_not_readmit']} "
        f"({sa['would_not_readmit_fraction']}).",
        f"- Reasons: {sa['reason_counts']}.",
        f"- Non-admit concentration by scope: {sa['non_admit_by_scope_top']}.",
        "",
        "## Usage",
        "",
        f"- {audit['usage']}.",
        "",
        "## Guardrails",
        "",
        f"- Frozen benchmark written: {audit['guardrails']['frozen_benchmark_written']}.",
        f"- Labels emitted: {audit['guardrails']['labels_emitted']}.",
        "- The gate is advisory; the authorized apply step is what writes.",
        "",
    ]
    return "\n".join(lines)


def write_novelty_admission_gate_audit(
    *,
    out_path: Path,
    report_path: Path | None = None,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    per_reaction_cap: int | None = DEFAULT_PER_REACTION_CAP,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_novelty_admission_gate_audit(
        frozen,
        expansion,
        per_cluster_cap=per_cluster_cap,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        hole_threshold=hole_threshold,
        per_reaction_cap=per_reaction_cap,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
