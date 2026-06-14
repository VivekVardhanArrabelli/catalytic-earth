"""Broadened-evidence-handle sourcing for the NAD(P)-dehydrogenase + glycosyltransferase
families (non-destructive).

`docs/scaling_plan_to_10k.md` (2026-06-12 update) and the evidence-handle scout established
that part of the apparent reviewed-Swiss-Prot shortage is an EVIDENCE-HANDLE problem, not a
supply problem: the import gate corroborated family scope mostly via the UniProt COFACTOR
comment, but many families annotate their defining evidence as a COSUBSTRATE / donor or a
functional KEYWORD. The decision-grade case: NAD(P) dehydrogenases (EC 1.1.1, ~7800 reviewed)
reach only ~7 under `cc_cofactor:nad/nadp` because NAD(P) is a *cosubstrate* (KW-0520/0521 +
Rhea participant), not a cofactor comment; `keyword:NAD/NADP` reaches ~7700.

This runner wires the BROADENED mechanism corroborators (cosubstrate / Rhea participant /
functional keyword / active-site presence) into the admission engine for two families whose
defining evidence is NOT a cofactor comment:

- `nad_p_dehydrogenase`  -- EC 1.1.1, SPLIT into capped EC-subclass lanes (the raw pool is
  huge and ortholog-padded). Corroborator: NAD(P) cosubstrate (Rhea nicotinamide participant
  or NAD/NADP keyword) + active-site/Rossmann. deploy-missing context = NAD(P) cosubstrate.
  Chemistry-confusable -> cap 150.
- `glycosyltransferase`  -- EC 2.4. Corroborator: sugar-nucleotide donor (Rhea participant)
  + Glycosyltransferase keyword. deploy-missing context = sugar-nucleotide donor. cap 250.

It is **orchestration only** -- it chains the same tested pipeline the Stage-1/Stage-2 runners
use, adding no new label logic:

    fetch_uniprot_query / fetch_uniprot_entry      (adapters, live UniProt REST)
      -> build_external_source_ingestion_pilot     (EC-subclass lanes -> canonical rows w/ keywords)
      -> build_cofactor_ec_disambiguation          (BROADENED mechanism corroborator + EC scope;
                                                     trust-tier N-of-M (>=1 mechanism axis) admits;
                                                     dedup vs BOTH registries; multi-signal held)
      -> evaluate_batch                            (novelty gate: new cluster/reaction/organism)
      -> per-fingerprint cap guard                 (150 confusable / 250 else; surplus held)
      -> non-destructive preview artifact
      -> (apply, separate/authorized) apply_external_annotation_anchored_import_to_registry

Guardrails inherited from the reused engines and asserted on the output:
- scope decided from reviewed Swiss-Prot/EC/Rhea/cofactor/cosubstrate/keyword annotation ONLY;
  EC / protein name / prose / keyword / cosubstrate stay in `excluded_context`, never predictive;
- `tier=bronze`, `review_status=automation_curated`; uniprot namespace;
- the frozen current702 benchmark registry is never written (expansion only);
- new labels deduped vs BOTH registries; multi-fingerprint-signal rows stay held;
- this module writes only an `artifacts/` preview + `work/` report. Appending to the
  expansion registry is the separate, explicitly authorized `apply` step.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query
from .breadth_feasibility_scout import CONFUSABLE_CAP
from .external_annotation_anchored_import import DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT
from .external_cofactor_ec_disambiguation import build_cofactor_ec_disambiguation
from .external_scaleout_bronze_import import (
    DEFAULT_CURRENT_MANIFEST_PATH,
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
    build_current702_reference_index,
)
from .external_source_ingestion import (
    _read_json,
    _utc_now_iso,
    build_external_source_ingestion_pilot,
)
from .novelty_admission_gate import (
    DEFAULT_CAP_CEILING,
    DEFAULT_PER_CLUSTER_CAP,
    build_diversity_state,
    evaluate_batch,
)
from .coverage_redundancy_audit import DEFAULT_REACTION_CAP_RATE
from .stage1_hole_sourcing import (
    DEFAULT_TARGET_FLOOR,
    _bridge_pilot_rows_for_disambiguation,
    _distinct_reactions_by_fingerprint,
    _fingerprint_counts,
    _reaction_aware_cap_guard,
)

ARTIFACT_ID = "v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"

# Each family maps 1:1 to a fingerprint. The fetch is split into NARROW EC-subclass lanes
# (the 2026-06-09 page-depth lesson + the scout's "huge, ortholog-padded pool" warning: split
# into subqueries, do not deepen paging). The keyword clause biases the fetch toward the
# annotated NAD(P) cosubstrate / Glycosyltransferase family; the AUTHORITATIVE scope decision
# is still the broadened mechanism corroborator + EC predicate in the disambiguation engine,
# and dedup runs vs BOTH registries.
FAMILY_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    "nad_p_dehydrogenase": (
        {
            "lane_id": "nad_p_dehydrogenase_ec_1_1_1_alcohol_aldehyde",
            "target_family_lane": "nad_p_dehydrogenase",
            "query": (
                "(reviewed:true) AND ((ec:1.1.1.1) OR (ec:1.1.1.2) OR (ec:1.1.1.71)) AND "
                "((keyword:NAD) OR (keyword:NADP))"
            ),
        },
        {
            "lane_id": "nad_p_dehydrogenase_ec_1_1_1_sugar_polyol",
            "target_family_lane": "nad_p_dehydrogenase",
            "query": (
                "(reviewed:true) AND ((ec:1.1.1.21) OR (ec:1.1.1.49) OR (ec:1.1.1.44)) AND "
                "((keyword:NAD) OR (keyword:NADP))"
            ),
        },
        {
            "lane_id": "nad_p_dehydrogenase_ec_1_1_1_organic_acid",
            "target_family_lane": "nad_p_dehydrogenase",
            "query": (
                "(reviewed:true) AND ((ec:1.1.1.27) OR (ec:1.1.1.37) OR (ec:1.1.1.42)) AND "
                "((keyword:NAD) OR (keyword:NADP))"
            ),
        },
        {
            "lane_id": "nad_p_dehydrogenase_ec_1_1_1_sdr_keto",
            "target_family_lane": "nad_p_dehydrogenase",
            "query": (
                "(reviewed:true) AND ((ec:1.1.1.100) OR (ec:1.1.1.35) OR (ec:1.1.1.30)) AND "
                "((keyword:NAD) OR (keyword:NADP))"
            ),
        },
        {
            "lane_id": "nad_p_dehydrogenase_ec_1_1_1_amino_acid_other",
            "target_family_lane": "nad_p_dehydrogenase",
            "query": (
                "(reviewed:true) AND ((ec:1.1.1.86) OR (ec:1.1.1.25) OR (ec:1.1.1.95)) AND "
                "((keyword:NAD) OR (keyword:NADP))"
            ),
        },
    ),
    "glycosyltransferase": (
        {
            "lane_id": "glycosyltransferase_ec_2_4_1_hexosyl",
            "target_family_lane": "glycosyltransferase",
            "query": "(reviewed:true) AND (ec:2.4.1.*) AND (keyword:Glycosyltransferase)",
        },
        {
            "lane_id": "glycosyltransferase_ec_2_4_2_pentosyl",
            "target_family_lane": "glycosyltransferase",
            "query": "(reviewed:true) AND (ec:2.4.2.*) AND (keyword:Glycosyltransferase)",
        },
        {
            "lane_id": "glycosyltransferase_ec_2_4_99_sialyl_other",
            "target_family_lane": "glycosyltransferase",
            "query": (
                "(reviewed:true) AND ((ec:2.4.99.*) OR (ec:2.4.3.*)) AND "
                "(keyword:Glycosyltransferase)"
            ),
        },
    ),
}

FAMILIES: tuple[str, ...] = tuple(FAMILY_LANE_QUERIES)

# Chemistry-confusable families fill to the 150 cap, not 250 (the Stage-2 cap lesson:
# filling chemistry-confusable families to the ceiling manufactures redundancy). NAD(P)
# dehydrogenases are confusable (the huge ortholog-padded SDR/MDR/AKR pool); glycosyl-
# transferases are a broad, diverse EC 2.4 space sourced toward the 250 ceiling.
CONFUSABLE_FAMILIES: frozenset[str] = frozenset({"nad_p_dehydrogenase"})


def _cap_for_family(family: str, *, cap_ceiling: int) -> int:
    return CONFUSABLE_CAP if family in CONFUSABLE_FAMILIES else cap_ceiling


def _lane_queries_for(families: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    lanes: list[dict[str, str]] = []
    for family in families:
        if family not in FAMILY_LANE_QUERIES:
            raise ValueError(
                f"{family!r} is not a broadened-handle family; choose from {FAMILIES}"
            )
        lanes.extend(FAMILY_LANE_QUERIES[family])
    return tuple(lanes)


def build_nad_glycosyltransferase_subfamily_sourcing(
    *,
    families: tuple[str, ...] = FAMILIES,
    max_records_per_lane: int = 60,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    per_reaction_cap: int | None = None,
    reaction_aware_caps: bool = False,
    reaction_cap_rate: int = DEFAULT_REACTION_CAP_RATE,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
) -> dict[str, Any]:
    """Source the broadened-handle families; return a non-destructive preview."""
    created = created_utc or _utc_now_iso()
    families = tuple(families)
    lane_queries = _lane_queries_for(families)
    caps_by_family = {f: _cap_for_family(f, cap_ceiling=cap_ceiling) for f in families}

    # 1. Fetch + build canonical candidate rows (live UniProt via injected fetchers).
    pilot = build_external_source_ingestion_pilot(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=list(frozen_benchmark_payload) + list(expansion_payload),
        created_utc=created,
        max_records_per_lane=max_records_per_lane,
        lane_queries=lane_queries,
        query_fetcher=query_fetcher,
        entry_fetcher=entry_fetcher,
        rhea_fetcher=rhea_fetcher,
    )

    # 2. Broadened mechanism corroborator + EC-scope disambiguation over the fresh rows
    #    (authoritative dedup vs BOTH registries; multi-fingerprint-signal rows stay held;
    #    EC for scope only; trust-tier N-of-M requires >=1 mechanism axis to admit).
    index = build_current702_reference_index(
        current_manifest_payload=current_manifest_payload,
        frozen_benchmark_payload=frozen_benchmark_payload,
        expansion_payload=expansion_payload,
    )
    disambig = build_cofactor_ec_disambiguation(
        pools=[
            {
                "pool": "nad_glycosyltransferase_broadened_handle_fresh_fetch",
                "path": "nad_glycosyltransferase_broadened_handle_fresh_fetch",
                "rows": _bridge_pilot_rows_for_disambiguation(pilot["rows"]),
            }
        ],
        registry=expansion_payload,
        index=index,
    )
    disambiguated_labels = disambig["applied_labels"]

    # 3. Novelty gate -- admit only labels that add diversity (state seeded from BOTH
    #    registries so orthologs already present are throttled, not re-imported).
    state = build_diversity_state(frozen_benchmark_payload, expansion_payload)
    gate = evaluate_batch(
        disambiguated_labels,
        state,
        per_cluster_cap=per_cluster_cap,
        target_floor=target_floor,
        per_reaction_cap=per_reaction_cap,
    )
    admit_ids = set(gate["admit_entry_ids"])
    gate_admitted = [
        label for label in disambiguated_labels if label.get("entry_id") in admit_ids
    ]
    throttled = [
        label for label in disambiguated_labels if label.get("entry_id") not in admit_ids
    ]

    # 3b. Per-fingerprint cap guard with a PER-FAMILY ceiling (150 confusable / 250 else).
    #     Trim each fingerprint's admitted set so projected combined never exceeds its cap;
    #     the surplus stays held (not imported). With reaction_aware_caps the per-family
    #     ceiling is further bounded by reaction diversity (clamp(rate*distinct_reactions,
    #     floor, per-family cap)).
    combined_counts = _fingerprint_counts(frozen_benchmark_payload) + _fingerprint_counts(
        expansion_payload
    )
    distinct_reactions_by_fp = _distinct_reactions_by_fingerprint(
        frozen_benchmark_payload, expansion_payload, gate_admitted
    )
    admitted, cap_trimmed, effective_caps = _reaction_aware_cap_guard(
        gate_admitted,
        combined_counts=combined_counts,
        base_cap_for=lambda fp: caps_by_family.get(fp, cap_ceiling),
        reaction_aware_caps=reaction_aware_caps,
        reaction_cap_rate=reaction_cap_rate,
        target_floor=target_floor,
        distinct_reactions_by_fp=distinct_reactions_by_fp,
    )
    cap_trimmed_counts = _fingerprint_counts(cap_trimmed)

    # 4. Per-family floor projection from the (cap-guarded) admitted set.
    admitted_counts = _fingerprint_counts(admitted)
    floor_projection = {}
    for family in families:
        before = combined_counts.get(family, 0)
        added = admitted_counts.get(family, 0)
        projected = before + added
        cap = caps_by_family[family]
        effective_cap = effective_caps.get(family, cap)
        floor_projection[family] = {
            "combined_before": before,
            "admitted_this_run": added,
            "projected_combined": projected,
            "deficit_to_floor_before": max(target_floor - before, 0),
            "deficit_to_floor_after": max(target_floor - projected, 0),
            "floor_reached": projected >= target_floor,
            "cap_ceiling": cap,
            "effective_cap": effective_cap,
            "distinct_reactions": distinct_reactions_by_fp.get(family, 0),
            "chemistry_confusable": family in CONFUSABLE_FAMILIES,
            "held_at_cap_this_run": cap_trimmed_counts.get(family, 0),
            "projected_over_cap": projected > cap,
            "projected_over_effective_cap": projected > effective_cap,
            "deploy_missing_active_site_context": DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT.get(
                family
            ),
        }

    floor_projection_total = sum(
        proj["projected_combined"] for proj in floor_projection.values()
    )
    combined_total = len(frozen_benchmark_payload) + len(expansion_payload)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_cosubstrate_keyword_annotation",
        "stage": "scaling_plan_to_10k:wire_broadened_evidence_handles_family_by_family",
        "families_sourced": list(families),
        "deploy_missing_active_site_context_per_family": {
            family: DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT.get(family) for family in families
        },
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_keyword_cosubstrate_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "broadened_handles_keyword_cosubstrate_binding_are_scope_admission_only": True,
            "broadened_handles_never_predictive_features": True,
            "ec_never_a_counted_corroborator": True,
            "trust_tier_n_of_m_requires_at_least_one_mechanism_axis": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "multi_fingerprint_signal_rows_held": True,
            "novelty_gated_against_both_registries": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
            "per_fingerprint_cap_ceiling_enforced_per_family": dict(
                sorted(caps_by_family.items())
            ),
            "reaction_aware_caps_enabled": reaction_aware_caps,
            "reaction_cap_rate": reaction_cap_rate if reaction_aware_caps else None,
            "per_reaction_cap_at_admission": per_reaction_cap,
            "no_fingerprint_pushed_over_cap": all(
                not p["projected_over_cap"] for p in floor_projection.values()
            ),
        },
        "floor_projection": floor_projection,
        "counts": {
            "lanes_queried": len(lane_queries),
            "max_records_per_lane": max_records_per_lane,
            "fetched_candidate_rows": pilot["candidate_count"],
            "mechanism_corroborated_bronze_labels": len(disambiguated_labels),
            "novelty_admitted_labels": len(admitted),
            "novelty_throttled_or_rejected": len(throttled),
            "gate_admitted_before_cap_guard": len(gate_admitted),
            "held_at_cap_ceiling": len(cap_trimmed),
            "held_at_cap_ceiling_by_fingerprint": dict(sorted(cap_trimmed_counts.items())),
            "admitted_fingerprint_counts": dict(sorted(admitted_counts.items())),
            "disambiguation_hold_count": disambig["counts"]["hold_count"],
            "disambiguation_hold_reason_counts": disambig["counts"].get(
                "hold_reason_counts", {}
            ),
            "disambiguation_skip_count": disambig["counts"]["skip_count"],
            "current_combined_labels": combined_total,
            "projected_combined_labels_if_merged": combined_total + len(admitted),
            "projected_family_label_total": floor_projection_total,
        },
        "novelty_gate": {
            "decision_counts": gate["decision_counts"],
            "reason_counts": gate["reason_counts"],
        },
        "disambiguation_counts": disambig["counts"],
        "lane_summaries": pilot["lane_summaries"],
        "fetch_failures": pilot["fetch_failures"],
        "fetch_failure_count": pilot["fetch_failure_count"],
        "next_action": (
            "Review floor_projection + novelty_gate, then on EXPLICIT authorization append "
            "`applied_labels` to data/registries/external_bronze_labels.json via "
            "`apply-external-annotation-anchored-import` (frozen current702 never written; "
            "print the frozen sha before/after). Held/throttled rows are the next batch."
        ),
        "applied_labels": admitted,
        "throttled_or_rejected_sample": [
            {"entry_id": label.get("entry_id"), "fingerprint_id": label.get("fingerprint_id")}
            for label in throttled[:50]
        ],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# NAD(P)-dehydrogenase + Glycosyltransferase Sourcing — broadened evidence handles"
        " (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for two families whose defining evidence is",
        "NOT a UniProt cofactor comment, via the broadened mechanism corroborator (cosubstrate /",
        "Rhea participant / functional keyword / active-site) + EC-scope predicate, then the",
        "novelty gate and a per-family cap guard. EC / keyword / cosubstrate are scope-only",
        "(never predictive); tier=bronze; the frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Families sourced: {', '.join(audit['families_sourced'])}.",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
        f"- Fetched candidate rows: {c['fetched_candidate_rows']}.",
        f"- Mechanism-corroborated bronze labels: {c['mechanism_corroborated_bronze_labels']} "
        f"(held {c['disambiguation_hold_count']}, skipped {c['disambiguation_skip_count']}).",
        f"- **Novelty-admitted labels: {c['novelty_admitted_labels']}** "
        f"(throttled/rejected {c['novelty_throttled_or_rejected']}; held@cap "
        f"{c['held_at_cap_ceiling']}).",
        f"- Combined registry {c['current_combined_labels']} -> "
        f"**{c['projected_combined_labels_if_merged']}** if merged.",
        "",
        "## Floor projection (100-label floor; per-family cap)",
        "",
        "| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for family, proj in audit["floor_projection"].items():
        lines.append(
            f"| {family} | {proj.get('deploy_missing_active_site_context')} | "
            f"{proj['combined_before']} | {proj['admitted_this_run']} | "
            f"{proj['projected_combined']} | {proj['cap_ceiling']} | "
            f"{proj['floor_reached']} | {proj.get('held_at_cap_this_run', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Novelty gate",
            "",
            f"- Decisions: {audit['novelty_gate']['decision_counts']}.",
            f"- Reasons: {audit['novelty_gate']['reason_counts']}.",
            "",
            "## Disambiguation holds (mechanism corroboration)",
            "",
            f"- Hold reasons: {c.get('disambiguation_hold_reason_counts', {})}.",
            "",
            "## Guardrails",
            "",
            f"- Curated registry written: {audit['guardrails']['curated_registry_written']}.",
            "- EC scope-only / never predictive: "
            f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
            "- Broadened handles (keyword/cosubstrate/binding) scope-admission only, never "
            f"predictive: {audit['guardrails']['broadened_handles_never_predictive_features']}.",
            "- EC never a counted corroborator: "
            f"{audit['guardrails']['ec_never_a_counted_corroborator']}.",
            "- Per-family cap ceiling: "
            f"{audit['guardrails']['per_fingerprint_cap_ceiling_enforced_per_family']}.",
            "- All new labels bronze / automation_curated; novelty-gated vs both registries; "
            "heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_nad_glycosyltransferase_subfamily_sourcing(
    *,
    out_path: Path,
    report_path: Path | None = None,
    families: tuple[str, ...] = FAMILIES,
    max_records_per_lane: int = 60,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    per_reaction_cap: int | None = None,
    reaction_aware_caps: bool = False,
    reaction_cap_rate: int = DEFAULT_REACTION_CAP_RATE,
) -> dict[str, Any]:
    """Build the preview and write it (non-destructive: no registry is touched)."""
    expansion_path = Path(expansion_registry_path)
    audit = build_nad_glycosyltransferase_subfamily_sourcing(
        families=families,
        max_records_per_lane=max_records_per_lane,
        current_manifest_payload=_read_json(Path(current_manifest_path)),
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        target_floor=target_floor,
        per_cluster_cap=per_cluster_cap,
        cap_ceiling=cap_ceiling,
        per_reaction_cap=per_reaction_cap,
        reaction_aware_caps=reaction_aware_caps,
        reaction_cap_rate=reaction_cap_rate,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
