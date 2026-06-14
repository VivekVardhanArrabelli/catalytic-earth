"""Source trust tiers + N-of-M corroboration policy + the SEPARATE honest counters.

The breadth scout established that reviewed Swiss-Prot alone (under the current handles) cannot
supply 10k diverse positive bronze. The agreed response (user direction, 2026-06-12) is NOT to
redefine 10k to make a number work, but to expand HONESTLY along two axes with discipline:

  1. evidence-handle expansion WITHIN reviewed Swiss-Prot (see `evidence_handle_expansion.py`), then
  2. source expansion BEYOND reviewed Swiss-Prot, admitted only through trust tiers with
     escalating multi-corroborator requirements.

This module is the durable, leakage-safe POLICY the future admission engine consumes. It writes no
registry and creates no labels; it encodes:

- `SOURCE_TRUST_TIERS` — tiers 0..4. Only 0-2 are bronze-eligible; the further from reviewed
  Swiss-Prot, the more independent corroborators required. Tiers 3-4 (cluster/model projection) are
  HYPOTHESES, never countable bronze unless upgraded by evidence.
- `CORROBORATOR_AXES` — the independent evidence axes a candidate can satisfy. The N-of-M rule
  (`evaluate_corroboration`) requires a tier-specific minimum of DISTINCT axes.
- `HONEST_COUNTER_AXES` — the separate counters that must NEVER be merged into one victory number
  (positive_bronze / oos_bronze / silver_ready / silver_confirmed / projected). `build_counter_ledger`
  reports each separately from the registries.

Discipline preserved (unchanged): EC / protein-name / UniProt prose stay in `excluded_context` and
are never predictive features; every candidate (any tier) still passes dedup vs BOTH registries, the
governor, the novelty gate, the source-trust gate, and the label-schema / leakage gate. Trust tiers
ADD a gate; they never remove one.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import load_json

from .coverage_redundancy_audit import (
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)

ARTIFACT_ID = "v3_source_trust_tier_policy_current702"
SCHEMA_VERSION = "source_trust_tiers.v1"

# COUNTED corroborator axes -- independent MECHANISM evidence. A candidate "satisfies" an axis when
# it carries that annotated/structural evidence; the N-of-M rule counts DISTINCT satisfied axes.
# EC is deliberately NOT here: EC decides SCOPE only (fetch / stratification / excluded_context) and
# must never count toward corroboration -- a row's EC alone cannot make it a corroborated mechanism
# label. (Rhea, by contrast, IS mechanism evidence: the reaction transformation / participants.)
CORROBORATOR_AXES: tuple[str, ...] = (
    "rhea_reaction_or_participant_pattern", # Rhea reaction transformation / participant (mechanism, NOT EC)
    "cofactor_or_cosubstrate",              # cofactor comment OR cosubstrate (e.g. NAD(P)) keyword/ligand
    "active_site_motif_or_residue_role",    # active-site / binding-site residue or sequence motif
    "domain_or_family_profile",             # Pfam/InterPro/family signature or functional keyword
    "sequence_cluster_proximity_to_anchor", # UniRef/cluster proximity to a trusted bronze/silver anchor
    "structure_or_pocket_support",          # AFDB/PDB coordinate or active-site pocket geometry
)

# Allowed scope axes that are NEVER counted toward corroboration. EC stays a first-class
# SCOPE / fetch / stratification signal and lives in excluded_context; it is recognized here so that
# passing it is not an "unknown axis" error, but it can never satisfy any part of the N-of-M rule.
NON_COUNTED_SCOPE_AXES: tuple[str, ...] = (
    "ec_scope_hint",                        # EC class: fetch / scope / stratification only, never counted
)

# Trust tiers. `bronze_eligible` gates whether a tier may ever produce a COUNTABLE bronze label.
# `min_independent_corroborators` is the N in the N-of-M rule (M = len(CORROBORATOR_AXES)). Tiers
# 3-4 are hypotheses: bronze_eligible False, and they may only become bronze by being UPGRADED into
# a lower tier once enough independent evidence is attached (`upgrade_only`).
SOURCE_TRUST_TIERS: dict[str, dict[str, Any]] = {
    "source_tier_0": {
        "name": "reviewed Swiss-Prot annotation",
        "description": (
            "Reviewed UniProtKB/Swiss-Prot with EC/Rhea/cofactor/active-site annotation -- the "
            "current annotation-anchored basis (incl. the broadened evidence handles)."
        ),
        "bronze_eligible": True,
        "min_independent_corroborators": 1,
        "upgrade_only": False,
    },
    "source_tier_1": {
        "name": "curated external enzyme/reaction source",
        "description": (
            "Curated external source (e.g. M-CSA / BRENDA-grade) with a stable accession AND "
            "explicit reaction evidence; cross-referenced to a UniProt accession."
        ),
        "bronze_eligible": True,
        "min_independent_corroborators": 2,
        "upgrade_only": False,
    },
    "source_tier_2": {
        "name": "unreviewed UniProt/TrEMBL with multiple independent corroborators",
        "description": (
            "Unreviewed TrEMBL admitted ONLY with multiple independent corroborators -- stronger "
            "corroboration than reviewed Swiss-Prot, because the annotation is not expert-curated."
        ),
        "bronze_eligible": True,
        "min_independent_corroborators": 3,
        "upgrade_only": False,
    },
    "source_tier_3": {
        "name": "UniRef/cluster propagation from a trusted anchor",
        "description": (
            "Label propagated across a UniRef/sequence cluster from a trusted bronze/silver anchor. "
            "A HYPOTHESIS, not countable bronze; may be upgraded to tier 0-2 if independent evidence "
            "is attached to the specific entry."
        ),
        "bronze_eligible": False,
        "min_independent_corroborators": 3,
        "upgrade_only": True,
    },
    "source_tier_4": {
        "name": "model/projected mechanism hypothesis",
        "description": (
            "A model- or projection-derived mechanism hypothesis. NEVER countable bronze; tracked "
            "separately as a projected/provisional hypothesis until upgraded by evidence."
        ),
        "bronze_eligible": False,
        "min_independent_corroborators": 4,
        "upgrade_only": True,
    },
}

# The separate honest counters. These MUST NOT be merged into a single victory number -- positives,
# OOS, and silver depth are different axes; projections are not yet real. (User direction 2026-06-12.)
HONEST_COUNTER_AXES: tuple[str, ...] = (
    "positive_bronze_count",
    "oos_bronze_count",
    "silver_ready_count",
    "silver_confirmed_count",
    "projected_provisional_count",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def evaluate_corroboration(
    *,
    source_tier: str,
    present_axes: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    """Apply the tier-specific N-of-M corroboration rule to a candidate's evidence axes.

    Returns an admit/hold verdict. A tier that is not bronze-eligible can never ADMIT as bronze
    (its verdict is `hold_hypothesis_not_countable_bronze`), regardless of axis count.
    """
    if source_tier not in SOURCE_TRUST_TIERS:
        raise ValueError(
            f"{source_tier!r} is not a known source trust tier; choose from "
            f"{tuple(SOURCE_TRUST_TIERS)}"
        )
    tier = SOURCE_TRUST_TIERS[source_tier]
    distinct_axes = sorted({a for a in present_axes if a in CORROBORATOR_AXES})
    # EC (and any non-counted scope axis) is recognized but never counts toward N-of-M.
    scope_hint_axes = sorted({a for a in present_axes if a in NON_COUNTED_SCOPE_AXES})
    unknown_axes = sorted(
        {
            a
            for a in present_axes
            if a not in CORROBORATOR_AXES and a not in NON_COUNTED_SCOPE_AXES
        }
    )
    required = int(tier["min_independent_corroborators"])
    meets_n_of_m = len(distinct_axes) >= required

    if not tier["bronze_eligible"]:
        decision = "hold_hypothesis_not_countable_bronze"
    elif meets_n_of_m:
        decision = "admit_bronze_candidate_pending_governor_and_novelty_gate"
    else:
        decision = "hold_insufficient_independent_corroboration"

    return {
        "source_tier": source_tier,
        "bronze_eligible_tier": bool(tier["bronze_eligible"]),
        "required_independent_corroborators": required,
        "distinct_corroborator_axes": distinct_axes,
        "distinct_corroborator_count": len(distinct_axes),
        "scope_hint_axes_present_not_counted": scope_hint_axes,
        "unknown_axes_ignored": unknown_axes,
        "meets_n_of_m": meets_n_of_m,
        "decision": decision,
        "still_requires": [
            "dedup_vs_both_registries",
            "coverage_redundancy_governor",
            "novelty_admission_gate",
            "label_schema_and_leakage_gate",
        ],
    }


def _counter_from_registries(
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute each honest counter SEPARATELY from the two registries (never summed together)."""
    combined = list(frozen_benchmark_payload) + list(expansion_payload)

    def is_positive(row: dict[str, Any]) -> bool:
        return row.get("label_type") == "seed_fingerprint"

    def is_oos(row: dict[str, Any]) -> bool:
        return row.get("label_type") == "out_of_scope"

    def tier(row: dict[str, Any]) -> str:
        return str(row.get("tier") or "")

    positive_bronze = sum(1 for r in combined if is_positive(r) and tier(r) == "bronze")
    oos_bronze = sum(1 for r in combined if is_oos(r) and tier(r) == "bronze")
    silver_ready = sum(1 for r in combined if tier(r) == "silver_ready")
    silver_confirmed = sum(1 for r in combined if tier(r) in ("silver", "silver_confirmed"))
    projected = sum(1 for r in combined if tier(r) in ("projected", "provisional", "hypothesis"))

    return {
        "positive_bronze_count": positive_bronze,
        "oos_bronze_count": oos_bronze,
        "silver_ready_count": silver_ready,
        "silver_confirmed_count": silver_confirmed,
        "projected_provisional_count": projected,
        "_note": (
            "These are reported SEPARATELY and must never be merged into one number. Silver tiers "
            "are 0 today (bronze->silver promotion is a deferred, per-row earned signal); projected "
            "is 0 today (no tier-3/4 hypotheses are imported as labels)."
        ),
    }


def build_source_trust_tier_policy(
    *,
    frozen_benchmark_payload: list[dict[str, Any]] | None = None,
    expansion_payload: list[dict[str, Any]] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    """Emit the trust-tier / corroboration policy + the current honest counter ledger."""
    created = created_utc or _utc_now_iso()
    ledger = (
        _counter_from_registries(frozen_benchmark_payload or [], expansion_payload or [])
        if frozen_benchmark_payload is not None or expansion_payload is not None
        else None
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_policy_spec_no_registry_or_labels_written",
        "purpose": (
            "Durable policy for honest growth beyond reviewed Swiss-Prot: source trust tiers with "
            "escalating N-of-M corroboration, and the separate honest counters that must never be "
            "merged into one victory number."
        ),
        "principles": [
            "Do NOT redefine 10k to make a number work; positives, OOS, and silver depth are "
            "different axes and stay separately counted.",
            "Fix within-Swiss-Prot evidence handles BEFORE expanding source classes (see "
            "evidence_handle_expansion).",
            "Only tiers 0-2 are bronze-eligible; the further from reviewed Swiss-Prot, the more "
            "independent corroborators required. Tiers 3-4 are hypotheses, not countable bronze.",
            "Trust tiers ADD a gate; the governor, novelty gate, dedup, and leakage gate stay "
            "mandatory for every candidate.",
            "EC / protein-name / UniProt prose stay in excluded_context, never predictive features.",
            "EC stays allowed for fetch / scope / stratification, but is NEVER a counted "
            "corroborator: EC alone cannot satisfy N-of-M. Mechanism evidence (Rhea, cofactor, "
            "active-site, domain, cluster, structure) is what corroborates.",
        ],
        "source_trust_tiers": SOURCE_TRUST_TIERS,
        "corroborator_axes": list(CORROBORATOR_AXES),
        "corroborator_axis_count_M": len(CORROBORATOR_AXES),
        "non_counted_scope_axes": list(NON_COUNTED_SCOPE_AXES),
        "ec_is_scope_only_not_a_counted_corroborator": True,
        "honest_counter_axes": list(HONEST_COUNTER_AXES),
        "honest_counters_must_not_be_merged": True,
        "current_honest_counter_ledger": ledger,
    }


def write_source_trust_tier_policy(
    *,
    out_path: Path,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
) -> dict[str, Any]:
    """Build the policy + current ledger and write it (non-destructive)."""
    frozen_path = Path(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    frozen = load_json(frozen_path) if frozen_path.exists() else []
    expansion = load_json(expansion_path) if expansion_path.exists() else []
    policy = build_source_trust_tier_policy(
        frozen_benchmark_payload=frozen,
        expansion_payload=expansion,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return policy
