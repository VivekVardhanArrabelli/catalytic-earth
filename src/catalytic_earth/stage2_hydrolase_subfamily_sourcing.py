"""Stage-2 sourcing for the metal_dependent_hydrolase v2 sub-families (non-destructive).

`docs/scaling_plan_to_10k.md` Stage 2 grows the ontology -- the real 10k lever, since
8 fingerprints x 250 cap ~= 2,000 positives is the honest ceiling of the v1 family set.
The on-ramp is splitting the coarse, over-cap `metal_dependent_hydrolase` umbrella into
four mechanistically-distinct v2 sub-families, separated by reaction-center bond change
(not by metal alone):

- `metallopeptidase`                 -- peptide C-N hydrolysis        (EC 3.4.24/17/11)
- `metallophosphoesterase_nuclease`  -- phosphodiester P-O hydrolysis (EC 3.1.4, 3.1.1x-3.1.3x nucleases)
- `metallophosphomonoesterase`       -- phosphomonoester P-O hydrolysis (EC 3.1.3)
- `metallo_amidohydrolase_deaminase` -- non-peptide amide/amidine C-N (EC 3.5.2/4/1)

Each carries a catalytic divalent metal; the EC-class disambiguation rules added to
`external_cofactor_ec_disambiguation.DISAMBIGUATION_RULES` enforce the bond-change
distinction, and the metal requirement excludes Ser/Cys peptidases and Cys-based
protein-tyrosine phosphatases (which carry no catalytic metal).

This module is **orchestration only** -- it chains the same tested pipeline the Stage-1
runner uses, and adds no new label logic:

    fetch_uniprot_query / fetch_uniprot_entry      (adapters, live UniProt REST)
      -> build_external_source_ingestion_pilot     (sub-family EC/metal lanes -> rows)
      -> build_cofactor_ec_disambiguation          (metal+EC scope, _build_label, dedup
                                                     vs BOTH registries, multi-signal held)
      -> evaluate_batch                            (novelty gate: new cluster/reaction/org)
      -> cap guard                                 (never push a sub-family over the cap)
      -> non-destructive preview artifact
      -> (apply, separate/authorized) apply_external_annotation_anchored_import_to_registry

Guardrails inherited from the reused engines and asserted on the output:
- scope decided from reviewed Swiss-Prot/EC/Rhea/cofactor annotation ONLY; EC / protein
  name / prose stay in `excluded_context`, never predictive features;
- `tier=bronze`, `review_status=automation_curated`; uniprot namespace;
- the frozen current702 benchmark registry is never written (expansion only);
- new labels deduped vs BOTH registries; multi-fingerprint-signal rows stay held;
- this module writes only an `artifacts/` preview + `work/` report. Appending to the
  expansion registry is the separate, explicitly authorized `apply` step.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query
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
from .stage1_hole_sourcing import (
    DEFAULT_TARGET_FLOOR,
    _bridge_pilot_rows_for_disambiguation,
    _fingerprint_counts,
)

ARTIFACT_ID = "v3_stage2_hydrolase_subfamily_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"

# Each sub-family is sourced by NARROW EC + metal-cofactor subqueries (the 2026-06-09
# page-depth lesson: split into subqueries, do not deepen paging). cc_cofactor/keyword
# filters bias the fetch toward annotated-metal rows; the authoritative scope decision
# is still the metal+EC disambiguation rule, and dedup runs vs BOTH registries so the
# existing metal_dependent_hydrolase accessions are not re-imported under a new id.
SUBFAMILY_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    "metallopeptidase": (
        {
            "lane_id": "metallopeptidase_ec_3_4_24",
            "target_family_lane": "metallopeptidase",
            "query": (
                "(reviewed:true) AND (ec:3.4.24.*) AND "
                "((keyword:Metalloprotease) OR (keyword:Zinc) OR (cc_cofactor:zinc))"
            ),
        },
        {
            "lane_id": "metallopeptidase_ec_3_4_17",
            "target_family_lane": "metallopeptidase",
            "query": (
                "(reviewed:true) AND (ec:3.4.17.*) AND "
                "((keyword:Metalloprotease) OR (keyword:Zinc) OR (cc_cofactor:zinc))"
            ),
        },
        {
            "lane_id": "metallopeptidase_ec_3_4_11",
            "target_family_lane": "metallopeptidase",
            "query": (
                "(reviewed:true) AND (ec:3.4.11.*) AND "
                "((keyword:Zinc) OR (keyword:Manganese) OR (cc_cofactor:zinc) OR "
                "(cc_cofactor:manganese))"
            ),
        },
    ),
    "metallophosphoesterase_nuclease": (
        {
            "lane_id": "metallophosphoesterase_ec_3_1_4",
            "target_family_lane": "metallophosphoesterase/nuclease",
            "query": (
                "(reviewed:true) AND (ec:3.1.4.*) AND "
                "((keyword:Metal-binding) OR (cc_cofactor:magnesium) OR "
                "(cc_cofactor:manganese))"
            ),
        },
        {
            "lane_id": "metallonuclease_ec_3_1_21_22",
            "target_family_lane": "metallophosphoesterase/nuclease",
            "query": (
                "(reviewed:true) AND ((ec:3.1.21.*) OR (ec:3.1.22.*)) AND "
                "((keyword:Nuclease) OR (keyword:Metal-binding) OR "
                "(cc_cofactor:magnesium))"
            ),
        },
        {
            "lane_id": "metallonuclease_ec_3_1_26_27",
            "target_family_lane": "metallophosphoesterase/nuclease",
            "query": (
                "(reviewed:true) AND ((ec:3.1.26.*) OR (ec:3.1.27.*)) AND "
                "((keyword:Nuclease) OR (keyword:Metal-binding) OR "
                "(cc_cofactor:magnesium) OR (cc_cofactor:manganese))"
            ),
        },
        {
            "lane_id": "metallonuclease_ec_3_1_11_31",
            "target_family_lane": "metallophosphoesterase/nuclease",
            "query": (
                "(reviewed:true) AND ((ec:3.1.11.*) OR (ec:3.1.31.*)) AND "
                "((keyword:Nuclease) OR (keyword:Metal-binding) OR "
                "(cc_cofactor:magnesium))"
            ),
        },
    ),
    "metallophosphomonoesterase": (
        {
            "lane_id": "metallophosphomonoesterase_ec_3_1_3_zn_mg",
            "target_family_lane": "metallophosphomonoesterase",
            "query": (
                "(reviewed:true) AND (ec:3.1.3.*) AND "
                "((cc_cofactor:zinc) OR (cc_cofactor:magnesium) OR (keyword:Zinc) OR "
                "(keyword:Magnesium))"
            ),
        },
        {
            "lane_id": "metallophosphomonoesterase_ec_3_1_3_mn_fe",
            "target_family_lane": "metallophosphomonoesterase",
            "query": (
                "(reviewed:true) AND (ec:3.1.3.*) AND "
                "((cc_cofactor:manganese) OR (cc_cofactor:iron) OR (keyword:Manganese) OR "
                "(keyword:Iron))"
            ),
        },
        {
            "lane_id": "metallophosphomonoesterase_ec_3_1_3_metalbinding",
            "target_family_lane": "metallophosphomonoesterase",
            "query": (
                "(reviewed:true) AND (ec:3.1.3.*) AND (keyword:Metal-binding)"
            ),
        },
        {
            "lane_id": "metallophosphomonoesterase_subclasses_phosphatase_nucleotidase",
            "target_family_lane": "metallophosphomonoesterase",
            "query": (
                "(reviewed:true) AND "
                "((ec:3.1.3.1) OR (ec:3.1.3.2) OR (ec:3.1.3.5) OR (ec:3.1.3.6)) AND "
                "((cc_cofactor:zinc) OR (cc_cofactor:magnesium) OR "
                "(cc_cofactor:manganese) OR (keyword:Metal-binding))"
            ),
        },
        {
            "lane_id": "metallophosphomonoesterase_subclasses_had_ppp",
            "target_family_lane": "metallophosphomonoesterase",
            "query": (
                "(reviewed:true) AND "
                "((ec:3.1.3.16) OR (ec:3.1.3.25) OR (ec:3.1.3.3) OR (ec:3.1.3.11)) AND "
                "((cc_cofactor:zinc) OR (cc_cofactor:magnesium) OR "
                "(cc_cofactor:manganese) OR (keyword:Metal-binding))"
            ),
        },
    ),
    "metallo_amidohydrolase_deaminase": (
        {
            "lane_id": "metallo_amidohydrolase_ec_3_5_2",
            "target_family_lane": "metallo amidohydrolase/deaminase",
            "query": (
                "(reviewed:true) AND (ec:3.5.2.*) AND "
                "((keyword:Zinc) OR (cc_cofactor:zinc) OR (keyword:Metal-binding))"
            ),
        },
        {
            "lane_id": "metallo_deaminase_ec_3_5_4",
            "target_family_lane": "metallo amidohydrolase/deaminase",
            "query": (
                "(reviewed:true) AND (ec:3.5.4.*) AND "
                "((keyword:Zinc) OR (cc_cofactor:zinc) OR (keyword:Metal-binding))"
            ),
        },
        {
            "lane_id": "metallo_amidohydrolase_ec_3_5_1",
            "target_family_lane": "metallo amidohydrolase/deaminase",
            "query": (
                "(reviewed:true) AND (ec:3.5.1.*) AND "
                "((keyword:Zinc) OR (cc_cofactor:zinc))"
            ),
        },
    ),
}

SUBFAMILIES: tuple[str, ...] = tuple(SUBFAMILY_LANE_QUERIES)


def _lane_queries_for(subfamilies: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    lanes: list[dict[str, str]] = []
    for subfamily in subfamilies:
        if subfamily not in SUBFAMILY_LANE_QUERIES:
            raise ValueError(
                f"{subfamily!r} is not a Stage-2 metal-hydrolase sub-family; "
                f"choose from {SUBFAMILIES}"
            )
        lanes.extend(SUBFAMILY_LANE_QUERIES[subfamily])
    return tuple(lanes)


def build_stage2_hydrolase_subfamily_sourcing(
    *,
    subfamilies: tuple[str, ...] = SUBFAMILIES,
    max_records_per_lane: int = 60,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
) -> dict[str, Any]:
    """Source the metal-hydrolase v2 sub-families; return a non-destructive preview."""
    created = created_utc or _utc_now_iso()
    subfamilies = tuple(subfamilies)
    lane_queries = _lane_queries_for(subfamilies)

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

    # 2. Cofactor/EC disambiguation over the fresh rows (authoritative dedup vs BOTH
    #    registries; multi-fingerprint-signal rows stay held; EC for scope only).
    index = build_current702_reference_index(
        current_manifest_payload=current_manifest_payload,
        frozen_benchmark_payload=frozen_benchmark_payload,
        expansion_payload=expansion_payload,
    )
    disambig = build_cofactor_ec_disambiguation(
        pools=[
            {
                "pool": "stage2_hydrolase_subfamily_fresh_fetch",
                "path": "stage2_hydrolase_subfamily_fresh_fetch",
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
    )
    admit_ids = set(gate["admit_entry_ids"])
    gate_admitted = [
        label for label in disambiguated_labels if label.get("entry_id") in admit_ids
    ]
    throttled = [
        label for label in disambiguated_labels if label.get("entry_id") not in admit_ids
    ]

    # 3b. Cap guard. Stage 2 sources NEW sub-families to the FLOOR; it must never
    #     manufacture an OVER-CAP fingerprint. Trim each sub-family's admitted set so
    #     projected combined never exceeds cap_ceiling; the surplus stays held.
    combined_counts = _fingerprint_counts(frozen_benchmark_payload) + _fingerprint_counts(
        expansion_payload
    )
    admitted: list[dict[str, Any]] = []
    cap_trimmed: list[dict[str, Any]] = []
    kept_per_fp: Counter = Counter()
    for label in gate_admitted:
        fp = label.get("fingerprint_id")
        if combined_counts.get(fp, 0) + kept_per_fp[fp] >= cap_ceiling:
            cap_trimmed.append(label)
            continue
        kept_per_fp[fp] += 1
        admitted.append(label)
    cap_trimmed_counts = _fingerprint_counts(cap_trimmed)

    # 4. Per-sub-family floor projection from the (cap-guarded) admitted set.
    admitted_counts = _fingerprint_counts(admitted)
    floor_projection = {}
    for subfamily in subfamilies:
        before = combined_counts.get(subfamily, 0)
        added = admitted_counts.get(subfamily, 0)
        projected = before + added
        floor_projection[subfamily] = {
            "combined_before": before,
            "admitted_this_run": added,
            "projected_combined": projected,
            "deficit_to_floor_before": max(target_floor - before, 0),
            "deficit_to_floor_after": max(target_floor - projected, 0),
            "floor_reached": projected >= target_floor,
            "cap_ceiling": cap_ceiling,
            "held_at_cap_this_run": cap_trimmed_counts.get(subfamily, 0),
            "projected_over_cap": projected > cap_ceiling,
        }

    combined_total = len(frozen_benchmark_payload) + len(expansion_payload)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "stage": "scaling_plan_to_10k:stage_2_grow_the_ontology",
        "split_of": "metal_dependent_hydrolase",
        "subfamilies_sourced": list(subfamilies),
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "multi_fingerprint_signal_rows_held": True,
            "novelty_gated_against_both_registries": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
            "no_new_labels_added_to_coarse_umbrella": True,
            "deploy_missing_active_site_context_per_subfamily": "metal",
            "per_fingerprint_cap_ceiling_enforced": cap_ceiling,
            "no_fingerprint_pushed_over_cap": all(
                not p["projected_over_cap"] for p in floor_projection.values()
            ),
        },
        "floor_projection": floor_projection,
        "counts": {
            "lanes_queried": len(lane_queries),
            "max_records_per_lane": max_records_per_lane,
            "fetched_candidate_rows": pilot["candidate_count"],
            "disambiguated_bronze_labels": len(disambiguated_labels),
            "novelty_admitted_labels": len(admitted),
            "novelty_throttled_or_rejected": len(throttled),
            "gate_admitted_before_cap_guard": len(gate_admitted),
            "held_at_cap_ceiling": len(cap_trimmed),
            "held_at_cap_ceiling_by_fingerprint": dict(sorted(cap_trimmed_counts.items())),
            "admitted_fingerprint_counts": dict(sorted(admitted_counts.items())),
            "disambiguation_hold_count": disambig["counts"]["hold_count"],
            "disambiguation_skip_count": disambig["counts"]["skip_count"],
            "current_combined_labels": combined_total,
            "projected_combined_labels_if_merged": combined_total + len(admitted),
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
            "Review floor_projection + novelty_gate, then on explicit authorization "
            "append `applied_labels` to data/registries/external_bronze_labels.json via "
            "`apply-external-annotation-anchored-import` (frozen current702 never "
            "written). Held/throttled rows are the next batch."
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
        "# Stage-2 Hydrolase Sub-Family Sourcing — metal_dependent_hydrolase v2 split"
        " (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for the four metal_dependent_hydrolase",
        "v2 sub-families via the existing fetch -> metal/EC disambiguation -> novelty-gate",
        "-> cap-guard pipeline. EC/name/prose are scope-only (never predictive); tier=bronze;",
        "the frozen current702 benchmark is NOT written. No new labels go to the coarse",
        "metal_dependent_hydrolase umbrella.",
        "",
        "## Result",
        "",
        f"- Sub-families sourced: {', '.join(audit['subfamilies_sourced'])}.",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
        f"- Fetched candidate rows: {c['fetched_candidate_rows']}.",
        f"- Disambiguated bronze labels: {c['disambiguated_bronze_labels']} "
        f"(held {c['disambiguation_hold_count']}, skipped {c['disambiguation_skip_count']}).",
        f"- **Novelty-admitted labels: {c['novelty_admitted_labels']}** "
        f"(throttled/rejected {c['novelty_throttled_or_rejected']}; held@cap "
        f"{c['held_at_cap_ceiling']}).",
        f"- Combined registry {c['current_combined_labels']} -> "
        f"**{c['projected_combined_labels_if_merged']}** if merged.",
        "",
        "## Floor projection (100-label floor)",
        "",
        "| Sub-family | combined before | admitted | projected | floor reached | held@cap |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for subfamily, proj in audit["floor_projection"].items():
        lines.append(
            f"| {subfamily} | {proj['combined_before']} | {proj['admitted_this_run']} | "
            f"{proj['projected_combined']} | {proj['floor_reached']} | "
            f"{proj.get('held_at_cap_this_run', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Novelty gate",
            "",
            f"- Decisions: {audit['novelty_gate']['decision_counts']}.",
            f"- Reasons: {audit['novelty_gate']['reason_counts']}.",
            "",
            "## Guardrails",
            "",
            f"- Curated registry written: {audit['guardrails']['curated_registry_written']}.",
            "- EC scope-only / never predictive: "
            f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
            "- No new labels added to the coarse umbrella: "
            f"{audit['guardrails']['no_new_labels_added_to_coarse_umbrella']}.",
            "- Deploy-missing active-site context per sub-family: "
            f"{audit['guardrails']['deploy_missing_active_site_context_per_subfamily']}.",
            "- All new labels bronze / automation_curated; novelty-gated vs both "
            "registries; heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_stage2_hydrolase_subfamily_sourcing(
    *,
    out_path: Path,
    report_path: Path | None = None,
    subfamilies: tuple[str, ...] = SUBFAMILIES,
    max_records_per_lane: int = 60,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
) -> dict[str, Any]:
    """Build the preview and write it (non-destructive: no registry is touched)."""
    expansion_path = Path(expansion_registry_path)
    audit = build_stage2_hydrolase_subfamily_sourcing(
        subfamilies=subfamilies,
        max_records_per_lane=max_records_per_lane,
        current_manifest_payload=_read_json(Path(current_manifest_path)),
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        target_floor=target_floor,
        per_cluster_cap=per_cluster_cap,
        cap_ceiling=cap_ceiling,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
