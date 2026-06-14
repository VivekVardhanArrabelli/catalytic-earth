"""Reaction-saturation trim: a non-destructive backward cleanup of the climb.

The governor (``coverage_redundancy_audit``) and the online novelty gate
(``novelty_admission_gate``) keep *forward* growth diverse. This module is the
*backward* counterpart: it measures the reaction-saturation already baked into the
expansion registry and previews a reaction- and sequence-diverse trim down to each
family's **reaction-aware cap** (``clamp(rate * distinct_reactions, floor,
ceiling)``).

The problem it cleans up (measured 2026-06-14): a handful of genuinely
single-reaction families (e.g. Mn/Fe superoxide dismutase: 166 labels / 1 distinct
Rhea reaction / 160 organisms; ATP/sugar/deoxynucleoside/NDP/GHMP kinases) grew to
~150 labels that are real, distinct, leakage-clean orthologs but add only
organism/sequence breadth -- NOT reaction/mechanism diversity. That is the
lowest-quality organic growth ("chasing volume manufactures redundancy"). The honest
tension respected here: the 100-floor itself forces ~100 labels onto a genuinely
single-reaction mechanism, so the fix bounds a family's depth ABOVE what its reaction
diversity earns -- it never drops single-reaction mechanisms below the floor.

Discipline (non-negotiable, mirrors the rest of the climb):

- The frozen ``curated_mechanism_labels.json`` (702) is NEVER written. Trimming only
  ever removes rows from the SEPARATE expansion registry
  ``external_bronze_labels.json``.
- This module is a PREVIEW: ``build_*`` / ``write_*`` write only ``artifacts/`` +
  ``work/`` and emit no registry. The registry REWRITE
  (``apply_reaction_saturation_trim_to_registry``) is a separate, explicitly
  authorized step; it drops only the demoted ``entry_id`` set and re-validates every
  KEPT label through ``MechanismLabel.from_dict``.
- Demotion is a DIVERSITY-QUALITY lever, not reconstruction (the separate
  silver/deploy axis). Fewer, more-diverse labels is a WIN; the 7742/7915 headline is
  not protected. Demoted rows are bronze, never frozen.
- Selection ranks by DIVERSITY, never metadata recency: it keeps >=1 row per distinct
  reaction first (so reaction/mechanism coverage is fully preserved), then maximizes
  organism / sequence-length / near-duplicate-cluster spread, using the governor's
  ``(fingerprint, full-EC, organism, length-bin)`` near-dup proxy. Local mmseqs
  sequence clustering is the stronger dedup when available; this offline proxy is the
  metadata-only stand-in.
- EC / name / lane stay coverage-accounting only, never predictive. The trim reads
  ``mechanism_evidence`` (Rhea) for reaction accounting only.
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
    DEFAULT_REACTION_CAP_RATE,
    DEFAULT_SATURATION_RATIO_THRESHOLD,
    DEFAULT_TARGET_FLOOR,
    _full_ec_signature,
    _gini,
    _load_json,
    _normalized_entropy,
    _organism,
    _reaction_ids,
    _sequence_length,
    _sequence_length_bin,
    reaction_aware_cap,
)
from .novelty_admission_gate import cluster_key
from .registry_io import load_json, write_registry_payload
from .source_trust_tiers import _counter_from_registries

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# Reactions are stored as ``RHEA:NNNN`` tuples; rows with no concrete Rhea reaction
# are grouped under this sentinel so they still get at least one representative kept.
_NO_REACTION = "RHEA:NONE"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_features(row: dict[str, Any]) -> dict[str, Any]:
    """The diversity features the selection ranks on (metadata-only)."""
    rxns = _reaction_ids(row) or (_NO_REACTION,)
    return {
        "entry_id": str(row.get("entry_id")),
        "reactions": tuple(rxns),
        "organism": _organism(row),
        "length_bin": _sequence_length_bin(_sequence_length(row)),
        "cluster_key": cluster_key(row),
    }


def select_diverse_keep(
    rows: list[dict[str, Any]],
    cap: int,
) -> dict[str, Any]:
    """Pick a reaction- and sequence-diverse KEEP subset of size <= ``cap``.

    Deterministic, diversity-ranked (never recency-ranked):

    1. **Reaction coverage first.** For every distinct reaction, keep one
       representative (the one whose cluster/organism/length is least represented in
       the keep set so far). This guarantees the family's full reaction/mechanism
       diversity survives the trim -- only redundant orthologs are demoted.
    2. **Diversity fill.** Fill the remaining budget by repeatedly taking the
       unselected row that adds the most NEW (cluster, organism, length-bin) coverage,
       tie-broken toward the least-occupied cluster, then ``entry_id``. Near-duplicate
       orthologs (same cluster key) score lowest and are demoted first.

    Returns the kept/demoted ``entry_id`` lists plus the diversity the keep set
    retains. If ``len(rows) <= cap`` everything is kept.
    """
    feats = sorted((_row_features(r) for r in rows), key=lambda f: f["entry_id"])
    all_ids = [f["entry_id"] for f in feats]
    if len(feats) <= cap:
        return {
            "kept": all_ids,
            "demoted": [],
            "kept_distinct_reactions": len(
                {rx for f in feats for rx in f["reactions"]} - {_NO_REACTION}
            ),
            "kept_distinct_organisms": len({f["organism"] for f in feats if f["organism"]}),
        }

    by_id = {f["entry_id"]: f for f in feats}
    kept: list[str] = []
    kept_set: set[str] = set()
    seen_clusters: Counter = Counter()
    seen_orgs: set = set()
    seen_lengths: set = set()
    covered_reactions: set[str] = set()

    def _absorb(fid: str) -> None:
        f = by_id[fid]
        kept.append(fid)
        kept_set.add(fid)
        seen_clusters[f["cluster_key"]] += 1
        if f["organism"]:
            seen_orgs.add(f["organism"])
        seen_lengths.add(f["length_bin"])
        covered_reactions.update(f["reactions"])

    def _marginal_key(f: dict[str, Any]) -> tuple:
        """Higher diversity sorts first; ties break toward emptier clusters then id."""
        new_cluster = f["cluster_key"] not in seen_clusters
        new_org = bool(f["organism"]) and f["organism"] not in seen_orgs
        new_len = f["length_bin"] not in seen_lengths
        score = (2 if new_cluster else 0) + (1 if new_org else 0) + (1 if new_len else 0)
        return (-score, seen_clusters.get(f["cluster_key"], 0), f["entry_id"])

    # 1. reaction coverage -- one representative per distinct reaction
    distinct_reactions = sorted({rx for f in feats for rx in f["reactions"]})
    for rx in distinct_reactions:
        if len(kept) >= cap:
            break
        if rx in covered_reactions:
            continue
        candidates = [
            f for f in feats if f["entry_id"] not in kept_set and rx in f["reactions"]
        ]
        if not candidates:
            continue
        best = min(candidates, key=_marginal_key)
        _absorb(best["entry_id"])

    # 2. diversity fill
    while len(kept) < cap:
        remaining = [f for f in feats if f["entry_id"] not in kept_set]
        if not remaining:
            break
        best = min(remaining, key=_marginal_key)
        _absorb(best["entry_id"])

    demoted = [fid for fid in all_ids if fid not in kept_set]
    return {
        "kept": sorted(kept),
        "demoted": sorted(demoted),
        "kept_distinct_reactions": len(covered_reactions - {_NO_REACTION}),
        "kept_distinct_organisms": len(seen_orgs),
    }


def _seed_rows_by_fingerprint(expansion: list[dict[str, Any]]) -> dict[str, list[dict]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expansion:
        if row.get("label_type") == "seed_fingerprint" and row.get("fingerprint_id"):
            out[row["fingerprint_id"]].append(row)
    return out


def _fingerprint_seed_counts(rows: list[dict[str, Any]]) -> Counter:
    counts: Counter = Counter()
    for row in rows:
        fp = row.get("fingerprint_id")
        if fp and row.get("label_type") == "seed_fingerprint":
            counts[fp] += 1
    return counts


def _projected_gini_entropy(
    frozen: list[dict[str, Any]],
    kept_seed_counts: Counter,
) -> tuple[float, float]:
    """Combined per-fingerprint Gini/entropy if the demoted rows were removed."""
    frozen_seed = _fingerprint_seed_counts(frozen)
    families = set(ALL_FINGERPRINTS) | set(frozen_seed) | set(kept_seed_counts)
    combined = [frozen_seed.get(fp, 0) + kept_seed_counts.get(fp, 0) for fp in families]
    return _gini(combined), _normalized_entropy(combined)


def build_reaction_saturation_trim(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
    *,
    reaction_cap_rate: int = DEFAULT_REACTION_CAP_RATE,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    saturation_ratio_threshold: float = DEFAULT_SATURATION_RATIO_THRESHOLD,
    created_utc: str | None = None,
) -> dict[str, Any]:
    """Preview a reaction-saturation trim over the expansion registry (no write).

    A family is TRIMMED when it is both (a) reaction-saturated -- its
    labels-per-distinct-reaction exceeds ``saturation_ratio_threshold`` -- and (b)
    over its reaction-aware cap. Each such family is trimmed down to
    ``reaction_aware_cap(distinct_reactions)`` by keeping a reaction- and
    sequence-diverse subset; the rest are demoted (removed from the expansion
    registry on a later authorized apply). Families that are over the reaction-aware
    cap but below the saturation ratio are reported as NEAR-saturated and left
    untouched at this threshold.
    """
    created = created_utc or _utc_now_iso()
    seed_by_fp = _seed_rows_by_fingerprint(expansion)
    frozen_seed = _fingerprint_seed_counts(frozen)

    families: list[dict[str, Any]] = []
    near_saturated: list[dict[str, Any]] = []
    all_demoted_ids: list[str] = []
    keep_demote_by_family: dict[str, dict[str, list[str]]] = {}

    # consider every fingerprint actually present in the expansion (data-driven, so a
    # newly-added family not yet in the governor's signature list is still measured)
    present = sorted(seed_by_fp.keys())
    for fp in present:
        rows = seed_by_fp[fp]
        n = len(rows)
        distinct_rx = len({rx for r in rows for rx in _reaction_ids(r)})
        labels_per_rx = round(n / distinct_rx, 2) if distinct_rx else None
        cap = reaction_aware_cap(
            distinct_rx,
            rate=reaction_cap_rate,
            floor=target_floor,
            ceiling=cap_ceiling,
        )
        over_cap = n > cap
        ratio_saturated = labels_per_rx is not None and labels_per_rx > saturation_ratio_threshold

        record = {
            "fingerprint": fp,
            "current_seed_labels": n,
            "distinct_reactions": distinct_rx,
            "labels_per_distinct_reaction": labels_per_rx,
            "reaction_aware_cap": cap,
            "over_reaction_aware_cap": over_cap,
        }

        if over_cap and ratio_saturated:
            selection = select_diverse_keep(rows, cap)
            kept_ids = selection["kept"]
            demoted_ids = selection["demoted"]
            all_demoted_ids.extend(demoted_ids)
            keep_demote_by_family[fp] = {"keep": kept_ids, "demote": demoted_ids}
            projected_lpr = (
                round(len(kept_ids) / distinct_rx, 2) if distinct_rx else None
            )
            record.update(
                {
                    "action": "TRIM",
                    "kept": len(kept_ids),
                    "demoted": len(demoted_ids),
                    "projected_labels_per_distinct_reaction": projected_lpr,
                    "kept_distinct_reactions": selection["kept_distinct_reactions"],
                    "reaction_diversity_preserved": (
                        selection["kept_distinct_reactions"] == distinct_rx
                    ),
                    "kept_distinct_organisms": selection["kept_distinct_organisms"],
                    "current_organisms": len(
                        {_organism(r) for r in rows if _organism(r)}
                    ),
                    "demoted_entry_ids": demoted_ids,
                }
            )
            families.append(record)
        elif over_cap:
            record["action"] = "NEAR_SATURATED_HOLD"
            near_saturated.append(record)

    # projected separate honest counters (positives drop by the demoted seed rows)
    demoted_id_set = set(all_demoted_ids)
    kept_expansion = [
        r for r in expansion if str(r.get("entry_id")) not in demoted_id_set
    ]
    counters_before = _counter_from_registries(frozen, expansion)
    counters_after = _counter_from_registries(frozen, kept_expansion)

    kept_seed_counts = _fingerprint_seed_counts(kept_expansion)
    current_seed_counts = _fingerprint_seed_counts(expansion)
    gini_before, entropy_before = _projected_gini_entropy(frozen, current_seed_counts)
    gini_after, entropy_after = _projected_gini_entropy(frozen, kept_seed_counts)

    total_demoted = len(all_demoted_ids)
    return {
        "audit": "reaction_saturation_trim",
        "created_utc": created,
        "status": "ok",
        "non_destructive": True,
        "applied": False,
        "policy": {
            "reaction_cap_rate": reaction_cap_rate,
            "target_floor": target_floor,
            "cap_ceiling": cap_ceiling,
            "saturation_ratio_threshold": saturation_ratio_threshold,
            "reaction_aware_cap_formula": "clamp(rate * distinct_reactions, floor, ceiling)",
            "selection": (
                "diversity-ranked: >=1 row per distinct reaction first (reaction "
                "diversity fully preserved), then maximize organism/length/cluster "
                "spread via the (fingerprint, full-EC, organism, length-bin) near-dup "
                "proxy; near-duplicate orthologs demoted first. Never recency-ranked. "
                "Local mmseqs sequence clustering is the stronger dedup when available."
            ),
        },
        "totals": {
            "frozen_current702": len(frozen),
            "expansion_before": len(expansion),
            "expansion_after": len(kept_expansion),
            "combined_before": len(frozen) + len(expansion),
            "combined_after": len(frozen) + len(kept_expansion),
            "families_trimmed": len(families),
            "rows_demoted": total_demoted,
            "near_saturated_held": len(near_saturated),
        },
        "trimmed_families": families,
        "near_saturated_families": near_saturated,
        "keep_demote_by_family": keep_demote_by_family,
        "demoted_entry_ids": sorted(demoted_id_set),
        "projected_diversity": {
            "fingerprint_gini_before": gini_before,
            "fingerprint_gini_after": gini_after,
            "fingerprint_normalized_entropy_before": entropy_before,
            "fingerprint_normalized_entropy_after": entropy_after,
            "gini_note": (
                "Fingerprint Gini measures COUNT evenness, not mechanism diversity. It "
                "rises after the trim BY DESIGN: single-reaction families are bounded "
                "to the floor while reaction-rich families keep their earned depth, so "
                "label depth becomes proportional to reaction diversity (the goal). The "
                "true quality metric is labels-per-distinct-reaction, which drops to the "
                "reaction-aware cap in every trimmed family (see projected_labels_per_"
                "distinct_reaction per family)."
            ),
        },
        "separate_honest_counters": {
            "before": counters_before,
            "after": counters_after,
            "note": (
                "counters stay SEPARATE (positive_bronze / oos_bronze / silver_ready / "
                "silver_confirmed / projected) -- never merged into one number. Only "
                "positive_bronze_count drops (by the demoted seed positives); oos and "
                "silver are untouched."
            ),
        },
        "guardrails": {
            "frozen_benchmark_written": False,
            "expansion_registry_written": False,
            "labels_emitted": 0,
            "demoted_rows_are_bronze_not_frozen": True,
            "ec_lane_used_for_coverage_accounting_only_never_predictive": True,
            "metadata_only_no_network_no_mmseqs_no_embeddings": True,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    t = audit["totals"]
    p = audit["policy"]
    pd = audit["projected_diversity"]
    cb = audit["separate_honest_counters"]["before"]
    ca = audit["separate_honest_counters"]["after"]
    lines = [
        "# Reaction-Saturation Trim (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Backward cleanup of the lowest-quality organic growth: families that grew "
        "deep on organism/sequence breadth but NOT reaction/mechanism diversity. "
        "Trims each reaction-saturated family down to its reaction-aware cap "
        f"(`{p['reaction_aware_cap_formula']}`, rate {p['reaction_cap_rate']}, floor "
        f"{p['target_floor']}, ceiling {p['cap_ceiling']}) by keeping a reaction- and "
        "sequence-diverse subset. PREVIEW ONLY -- writes no registry; the frozen 702 "
        "benchmark is never touched.",
        "",
        f"- Families trimmed: {t['families_trimmed']}; rows demoted: "
        f"{t['rows_demoted']}; expansion {t['expansion_before']} -> "
        f"{t['expansion_after']}; combined {t['combined_before']} -> "
        f"{t['combined_after']}.",
        f"- Near-saturated held (over reaction-aware cap but below ratio "
        f"{p['saturation_ratio_threshold']}): {t['near_saturated_held']}.",
        "",
        "## Selection",
        "",
        f"- {p['selection']}",
        "",
        "## Per-family keep / demote",
        "",
        "| family | current | distinct rxn | labels/rxn now | reaction-aware cap | kept | demoted | labels/rxn after | rxn diversity preserved |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for f in audit["trimmed_families"]:
        lines.append(
            f"| {f['fingerprint']} | {f['current_seed_labels']} | "
            f"{f['distinct_reactions']} | {f['labels_per_distinct_reaction']} | "
            f"{f['reaction_aware_cap']} | {f['kept']} | {f['demoted']} | "
            f"{f['projected_labels_per_distinct_reaction']} | "
            f"{f['reaction_diversity_preserved']} |"
        )
    if audit["near_saturated_families"]:
        lines.extend(
            [
                "",
                "### Near-saturated (over reaction-aware cap, below ratio threshold -- not trimmed)",
                "",
                "| family | current | distinct rxn | labels/rxn | reaction-aware cap |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for f in audit["near_saturated_families"]:
            lines.append(
                f"| {f['fingerprint']} | {f['current_seed_labels']} | "
                f"{f['distinct_reactions']} | {f['labels_per_distinct_reaction']} | "
                f"{f['reaction_aware_cap']} |"
            )
    lines.extend(
        [
            "",
            "## Projected diversity (combined per-fingerprint)",
            "",
            f"- Fingerprint Gini: {pd['fingerprint_gini_before']} -> "
            f"{pd['fingerprint_gini_after']}.",
            f"- Normalized entropy: "
            f"{pd['fingerprint_normalized_entropy_before']} -> "
            f"{pd['fingerprint_normalized_entropy_after']}.",
            f"- Note: {pd['gini_note']}",
            "",
            "## Separate honest counters (before -> after; never merged)",
            "",
            f"- positive_bronze_count: {cb['positive_bronze_count']} -> "
            f"{ca['positive_bronze_count']}.",
            f"- oos_bronze_count: {cb['oos_bronze_count']} -> "
            f"{ca['oos_bronze_count']}.",
            f"- silver_ready_count: {cb['silver_ready_count']} -> "
            f"{ca['silver_ready_count']}.",
            f"- silver_confirmed_count: {cb['silver_confirmed_count']} -> "
            f"{ca['silver_confirmed_count']}.",
            f"- projected_provisional_count: {cb['projected_provisional_count']} -> "
            f"{ca['projected_provisional_count']}.",
            "",
            "## Guardrails",
            "",
            "- Frozen benchmark written: "
            f"{audit['guardrails']['frozen_benchmark_written']}.",
            "- Expansion registry written: "
            f"{audit['guardrails']['expansion_registry_written']}.",
            "- Demoted rows are bronze, never frozen; demotion is a diversity-quality "
            "lever, not reconstruction.",
            "- Metadata-only: no network, no mmseqs, no embeddings.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reaction_saturation_trim(
    *,
    out_path: Path,
    report_path: Path | None = None,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    reaction_cap_rate: int = DEFAULT_REACTION_CAP_RATE,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    saturation_ratio_threshold: float = DEFAULT_SATURATION_RATIO_THRESHOLD,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_reaction_saturation_trim(
        frozen,
        expansion,
        reaction_cap_rate=reaction_cap_rate,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        saturation_ratio_threshold=saturation_ratio_threshold,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit


def apply_reaction_saturation_trim_to_registry(
    *,
    preview_path: Path,
    expansion_registry_path: Path,
    frozen_benchmark_registry_path: Path,
) -> dict[str, Any]:
    """Rewrite the expansion registry dropping ONLY the preview's demoted entry_ids.

    Non-destructive in the project's sense: the frozen current702 benchmark is never
    written; only the SEPARATE expansion registry is rewritten, removing exactly the
    demoted rows. Every KEPT label is re-validated through ``MechanismLabel.from_dict``
    before the registry is written, so a malformed kept row aborts the rewrite. This
    is the explicitly-authorized apply step -- the preview never calls it.
    """
    from .labels import MechanismLabel

    preview = load_json(preview_path)
    if preview.get("audit") != "reaction_saturation_trim":
        raise ValueError(
            "preview is not a reaction_saturation_trim artifact; refusing to apply"
        )
    demote_ids = {str(eid) for eid in preview.get("demoted_entry_ids", [])}

    frozen = _load_json(frozen_benchmark_registry_path)
    frozen_count_before = len(frozen)
    expansion_path = Path(expansion_registry_path)
    existing = _load_json(expansion_path) if expansion_path.exists() else []

    kept: list[dict[str, Any]] = []
    removed = 0
    for row in existing:
        if str(row.get("entry_id")) in demote_ids:
            removed += 1
            continue
        # re-validate every kept label through the canonical schema/leakage gate
        MechanismLabel.from_dict(row)
        kept.append(row)

    missing = demote_ids - {str(r.get("entry_id")) for r in existing}
    expansion_path.parent.mkdir(parents=True, exist_ok=True)
    write_result = write_registry_payload(expansion_path, kept)

    # the frozen benchmark is never written by this path -- assert it is untouched
    frozen_after = _load_json(frozen_benchmark_registry_path)
    return {
        "applied": True,
        "frozen_benchmark_registry_written": False,
        "frozen_benchmark_labels_before": frozen_count_before,
        "frozen_benchmark_labels_after": len(frozen_after),
        "expansion_registry_before": len(existing),
        "rows_removed": removed,
        "expansion_registry_after": len(kept),
        "demoted_ids_not_found": sorted(missing),
        "all_kept_revalidated": True,
        "expansion_registry_path": str(expansion_path),
        "expansion_registry_storage": write_result,
    }
