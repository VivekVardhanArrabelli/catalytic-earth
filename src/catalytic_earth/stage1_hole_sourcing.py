"""Stage-1 hole sourcing for the scaling-plan-to-10k climb (non-destructive).

`docs/scaling_plan_to_10k.md` Stage 1 closes the governor's HOLE and UNDER-FLOOR
fingerprints to the 100-label floor. This module sources the **five cofactor-defined
Stage-1 fingerprints** end to end by chaining the existing, tested pipeline -- it
adds orchestration and fingerprint-targeted queries, not new label logic. The two
holes are `radical_sam_enzyme` and `cobalamin_radical_rearrangement`; the three
under-floor fingerprints are `flavin_monooxygenase`, `heme_peroxidase_oxidase`, and
`flavin_dehydrogenase_reductase`. (`ser_his_acid_hydrolase` is the third hole but is
cofactorless -- see below.) The chain:

    fetch_uniprot_query / fetch_uniprot_entry   (adapters, live UniProt REST)
      -> build_external_source_ingestion_pilot  (lane queries -> canonical rows)
      -> build_cofactor_ec_disambiguation       (fresh rows as a pool: cofactor+EC
                                                  scope, _build_label, dedup vs BOTH
                                                  registries, multi-signal rows held)
      -> evaluate_batch                          (novelty gate: admit only rows that
                                                  add a new cluster/reaction/organism)
      -> non-destructive preview artifact
      -> (apply, separate/authorized) apply_external_annotation_anchored_import_to_registry

The cofactorless `ser_his_acid_hydrolase` hole is deliberately NOT sourced here:
the cofactor/EC disambiguation engine structurally cannot reach it (there is no
catalytic cofactor to corroborate), and the plan routes it through the dedicated
`build-ser-his-triad-locator-scan` tool (the Ser/Cys-His-Asp triad locator +
acquisition contract, confirmed against coordinates). See
`docs/stage1_hole_sourcing_runbook.md`.

Guardrails inherited from the reused engines and asserted on the output:
- scope decided from reviewed Swiss-Prot/EC/Rhea/cofactor annotation ONLY; EC /
  protein name / prose stay in `excluded_context`, never predictive features;
- `tier=bronze`, `review_status=automation_curated`;
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

ARTIFACT_ID = "v3_stage1_hole_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"

DEFAULT_TARGET_FLOOR = 100

# The two cofactor-defined holes this runner sources. ser_his is intentionally
# absent (cofactorless -> dedicated triad-locator tool). Each lane is a NARROW
# EC/cofactor subquery, not a broad query with deep paging -- the 2026-06-09
# page-depth saturation lesson: split into subqueries, do not increase page depth.
HOLE_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    "radical_sam_enzyme": (
        {
            "lane_id": "radical_sam_ec_2_8_4",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (ec:2.8.4.*) AND "
                '((protein_name:"radical SAM") OR '
                '(cc_cofactor:"[4Fe-4S] cluster") OR '
                '(keyword:"S-adenosyl-L-methionine"))'
            ),
        },
        {
            "lane_id": "radical_sam_ec_4_1_99",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (ec:4.1.99.*) AND "
                '((cc_cofactor:"[4Fe-4S] cluster") OR '
                '(keyword:"S-adenosyl-L-methionine"))'
            ),
        },
        {
            "lane_id": "radical_sam_ec_1_97_1",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": "(reviewed:true) AND (ec:1.97.1.*)",
        },
        {
            "lane_id": "radical_sam_named",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": '(reviewed:true) AND (protein_name:"radical SAM")',
        },
        {
            "lane_id": "radical_sam_kw_sam_iron_sulfur",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND "
                '(keyword:"S-adenosyl-L-methionine") AND (keyword:"Iron-sulfur")'
            ),
        },
    ),
    "cobalamin_radical_rearrangement": (
        {
            "lane_id": "cobalamin_ec_5_4_99",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (ec:5.4.99.*) AND "
                "((keyword:Cobalamin) OR (cc_cofactor:cobalamin) OR "
                '(cc_cofactor:"adenosylcobalamin"))'
            ),
        },
        {
            "lane_id": "cobalamin_ec_5_4_3",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (ec:5.4.3.*) AND "
                "((keyword:Cobalamin) OR (cc_cofactor:cobalamin))"
            ),
        },
        {
            "lane_id": "cobalamin_ec_4_2_1_28_30",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND ((ec:4.2.1.28) OR (ec:4.2.1.30)) AND "
                "((keyword:Cobalamin) OR (cc_cofactor:cobalamin))"
            ),
        },
        {
            "lane_id": "cobalamin_ec_4_3_1_7",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (ec:4.3.1.7) AND "
                "((keyword:Cobalamin) OR (cc_cofactor:cobalamin))"
            ),
        },
        {
            "lane_id": "cobalamin_mutase_named",
            "target_family_lane": "radical-SAM/cobalamin",
            "query": (
                "(reviewed:true) AND (protein_name:mutase) AND "
                "((keyword:Cobalamin) OR (cc_cofactor:cobalamin) OR "
                '(cc_cofactor:"adenosylcobalamin"))'
            ),
        },
    ),
}

SOURCEABLE_HOLES: tuple[str, ...] = tuple(HOLE_LANE_QUERIES)

# The three cofactor-defined UNDER-FLOOR fingerprints (below the 100-label floor but
# not holes). Same engine, same guardrails as the holes -- only the lane queries
# differ. Each lane is a NARROW EC + cofactor subquery (the 2026-06-09 page-depth
# lesson: split into subqueries, do not deepen paging). Scope is still decided by the
# cofactor/EC disambiguation rules (heme + 1.11.1; flavin no-heme + 1.14.13/14 vs
# 1.3/1.6/1.8.1); cc_cofactor filters bias the fetch toward annotated-cofactor rows.
UNDER_FLOOR_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    "flavin_monooxygenase": (
        {
            "lane_id": "fmo_ec_1_14_13",
            "target_family_lane": "flavin-monooxygenase",
            "query": (
                "(reviewed:true) AND (ec:1.14.13.*) AND "
                "((cc_cofactor:FAD) OR (cc_cofactor:FMN))"
            ),
        },
        {
            "lane_id": "fmo_ec_1_14_14",
            "target_family_lane": "flavin-monooxygenase",
            "query": (
                "(reviewed:true) AND (ec:1.14.14.*) AND "
                "((cc_cofactor:FAD) OR (cc_cofactor:FMN))"
            ),
        },
        {
            "lane_id": "fmo_kw_monooxygenase_flavoprotein",
            "target_family_lane": "flavin-monooxygenase",
            "query": (
                "(reviewed:true) AND (ec:1.14.13.*) AND "
                "(keyword:Monooxygenase) AND (keyword:Flavoprotein)"
            ),
        },
    ),
    "heme_peroxidase_oxidase": (
        {
            "lane_id": "heme_peroxidase_ec_1_11_1_cofactor",
            "target_family_lane": "heme-peroxidase/oxidase",
            "query": (
                "(reviewed:true) AND (ec:1.11.1.*) AND "
                "((cc_cofactor:heme) OR (keyword:Heme))"
            ),
        },
        {
            "lane_id": "heme_peroxidase_ec_1_11_1_kw",
            "target_family_lane": "heme-peroxidase/oxidase",
            "query": "(reviewed:true) AND (ec:1.11.1.*) AND (keyword:Peroxidase)",
        },
    ),
    "flavin_dehydrogenase_reductase": (
        {
            "lane_id": "fdr_ec_1_3",
            "target_family_lane": "flavin-dehydrogenase/reductase",
            "query": (
                "(reviewed:true) AND (ec:1.3.*) AND "
                "((cc_cofactor:FAD) OR (cc_cofactor:FMN))"
            ),
        },
        {
            "lane_id": "fdr_ec_1_6",
            "target_family_lane": "flavin-dehydrogenase/reductase",
            "query": (
                "(reviewed:true) AND (ec:1.6.*) AND "
                "((cc_cofactor:FAD) OR (cc_cofactor:FMN))"
            ),
        },
        {
            "lane_id": "fdr_ec_1_8_1",
            "target_family_lane": "flavin-dehydrogenase/reductase",
            "query": (
                "(reviewed:true) AND (ec:1.8.1.*) AND "
                "((cc_cofactor:FAD) OR (cc_cofactor:FMN))"
            ),
        },
    ),
}

# All five cofactor-defined Stage-1 fingerprints this runner can source. ser_his is
# intentionally absent (cofactorless -> dedicated triad-locator tool).
STAGE1_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    **HOLE_LANE_QUERIES,
    **UNDER_FLOOR_LANE_QUERIES,
}

SOURCEABLE_FINGERPRINTS: tuple[str, ...] = tuple(STAGE1_LANE_QUERIES)


def _lane_queries_for(fingerprints: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    lanes: list[dict[str, str]] = []
    for fingerprint in fingerprints:
        if fingerprint not in STAGE1_LANE_QUERIES:
            raise ValueError(
                f"{fingerprint!r} is not a cofactor-sourceable Stage-1 fingerprint; "
                f"choose from {SOURCEABLE_FINGERPRINTS} "
                "(ser_his uses build-ser-his-triad-locator-scan)"
            )
        lanes.extend(STAGE1_LANE_QUERIES[fingerprint])
    return tuple(lanes)


def _bridge_pilot_rows_for_disambiguation(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Re-key the ingestion pilot's own current702 screen for the disambiguation engine.

    `build_external_source_ingestion_pilot` records its current702 duplicate screen
    under `duplicate_current_registry_conflict`, but the cofactor/EC engine's
    re-screen (`rerun_current702_duplicate_screen` -> `_upstream_current702_status`)
    reads the upstream verdict from `duplicate_status`. Without this re-keying every
    fresh pilot row is rejected as `upstream_current702_screen_not_confirmed`. This
    only exposes the pilot's existing verdict under the expected key; the
    authoritative accession/sequence re-check still runs against both registries.
    """
    bridged: list[dict[str, Any]] = []
    for row in rows:
        new = dict(row)
        screen = row.get("duplicate_current_registry_conflict")
        if isinstance(screen, dict):
            new["duplicate_status"] = screen
        bridged.append(new)
    return bridged


def _fingerprint_counts(labels: list[dict[str, Any]]) -> Counter:
    counts: Counter = Counter()
    for label in labels:
        fp = label.get("fingerprint_id")
        if fp and label.get("label_type") == "seed_fingerprint":
            counts[fp] += 1
    return counts


def build_stage1_hole_sourcing(
    *,
    holes: tuple[str, ...] = SOURCEABLE_FINGERPRINTS,
    max_records_per_lane: int = 50,
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
    """Source the cofactor-defined holes; return a non-destructive import preview.

    Steps (all reused, tested code except this orchestration):
    1. fetch reviewed Swiss-Prot rows for the hole lanes -> canonical candidate rows;
    2. cofactor/EC disambiguation -> bronze labels (held unless a single rule fires);
    3. novelty gate -> keep only labels that add a new cluster/reaction/organism;
    4. emit a preview whose ``applied_labels`` is the novelty-admitted set, ready for
       the existing ``apply-external-annotation-anchored-import`` step.
    """
    created = created_utc or _utc_now_iso()
    holes = tuple(holes)
    lane_queries = _lane_queries_for(holes)

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
                "pool": "stage1_hole_sourcing_fresh_fetch",
                "path": "stage1_hole_sourcing_fresh_fetch",
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

    # 3b. Cap guard. Stage 1 closes holes/under-floor to the FLOOR; it must never
    #     manufacture an OVER-CAP fingerprint. The novelty gate admits diverse rows
    #     greedily above the floor and even permits "over_cap_but_new_reaction_chemistry"
    #     admissions, so a high-yield space (e.g. flavin_dehydrogenase_reductase via
    #     EC 1.3/1.6/1.8.1) can be pushed past the 250 ceiling. Trim each fingerprint's
    #     admitted set so projected combined never exceeds cap_ceiling; the surplus stays
    #     held (a review queue), it is not imported.
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

    # 4. Per-fingerprint floor projection from the (cap-guarded) admitted set.
    admitted_counts = _fingerprint_counts(admitted)
    floor_projection = {}
    for hole in holes:
        before = combined_counts.get(hole, 0)
        added = admitted_counts.get(hole, 0)
        projected = before + added
        floor_projection[hole] = {
            "combined_before": before,
            "admitted_this_run": added,
            "projected_combined": projected,
            "deficit_to_floor_before": max(target_floor - before, 0),
            "deficit_to_floor_after": max(target_floor - projected, 0),
            "floor_reached": projected >= target_floor,
            "cap_ceiling": cap_ceiling,
            "held_at_cap_this_run": cap_trimmed_counts.get(hole, 0),
            "projected_over_cap": projected > cap_ceiling,
        }

    combined_total = len(frozen_benchmark_payload) + len(expansion_payload)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "stage": "scaling_plan_to_10k:stage_1_close_the_holes",
        "holes_sourced": list(holes),
        "ser_his_note": (
            "ser_his_acid_hydrolase is cofactorless and is NOT sourceable through this "
            "cofactor/EC engine; source it via build-ser-his-triad-locator-scan."
        ),
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
        "# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via",
        "the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.",
        "EC/name/prose are scope-only (never predictive); tier=bronze; the frozen",
        "current702 benchmark is NOT written. ser_his uses the triad-locator tool.",
        "",
        "## Result",
        "",
        f"- Holes sourced: {', '.join(audit['holes_sourced'])}.",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
        f"- Fetched candidate rows: {c['fetched_candidate_rows']}.",
        f"- Disambiguated bronze labels: {c['disambiguated_bronze_labels']} "
        f"(held {c['disambiguation_hold_count']}, skipped {c['disambiguation_skip_count']}).",
        f"- **Novelty-admitted labels: {c['novelty_admitted_labels']}** "
        f"(throttled/rejected {c['novelty_throttled_or_rejected']}).",
        f"- Combined registry {c['current_combined_labels']} -> "
        f"**{c['projected_combined_labels_if_merged']}** if merged.",
        "",
        "## Floor projection (100-label floor)",
        "",
        "| Fingerprint | combined before | admitted | projected | floor reached | held@cap | over cap |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for hole, proj in audit["floor_projection"].items():
        lines.append(
            f"| {hole} | {proj['combined_before']} | {proj['admitted_this_run']} | "
            f"{proj['projected_combined']} | {proj['floor_reached']} | "
            f"{proj.get('held_at_cap_this_run', 0)} | {proj.get('projected_over_cap', False)} |"
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
            "- All new labels bronze / automation_curated; novelty-gated vs both "
            "registries; heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_stage1_hole_sourcing(
    *,
    out_path: Path,
    report_path: Path | None = None,
    holes: tuple[str, ...] = SOURCEABLE_FINGERPRINTS,
    max_records_per_lane: int = 50,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
) -> dict[str, Any]:
    """Build the preview and write it (non-destructive: no registry is touched)."""
    expansion_path = Path(expansion_registry_path)
    audit = build_stage1_hole_sourcing(
        holes=holes,
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
