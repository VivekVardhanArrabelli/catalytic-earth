"""Broadened-handle sourcing for glycoside hydrolases."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query
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
    DEFAULT_PER_CLUSTER_CAP,
    build_diversity_state,
    evaluate_batch,
)
from .stage1_hole_sourcing import (
    DEFAULT_TARGET_FLOOR,
    _bridge_pilot_rows_for_disambiguation,
    _fingerprint_counts,
)

ARTIFACT_ID = "v3_glycoside_hydrolase_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"

FAMILY = "glycoside_hydrolase"
FAMILIES: tuple[str, ...] = (FAMILY,)
DEFAULT_GLYCOSIDE_HYDROLASE_CAP_CEILING = 150

FAMILY_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    FAMILY: (
        {
            "lane_id": "glycoside_hydrolase_reviewed_ec_3_2_1",
            "target_family_lane": FAMILY,
            "query": (
                "(reviewed:true) AND (ec:3.2.1.*) AND "
                "((keyword:Glycosidase) OR (protein_name:glycosidase) OR "
                "(protein_name:glucosidase) OR (protein_name:galactosidase) OR "
                "(protein_name:xylanase) OR (protein_name:cellulase) OR "
                "(protein_name:amylase) OR (protein_name:mannosidase)) NOT "
                "((ec:2.4.*) OR (ec:4.*) OR (protein_name:transferase) OR "
                "(protein_name:lyase) OR (protein_name:phosphorylase) OR "
                "(protein_name:transglycosylase))"
            ),
        },
    )
}
ALTERNATE_NAME_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    FAMILY: (
        {
            "lane_id": "glycoside_hydrolase_reviewed_chitinase_glucanase_name",
            "target_family_lane": FAMILY,
            "query": (
                "(reviewed:true) AND (ec:3.2.1.*) AND "
                "((protein_name:chitinase) OR (protein_name:\"beta-glucanase\") OR "
                "(protein_name:\"glycoside hydrolase\") OR "
                "(protein_name:\"glycosyl hydrolase\")) NOT "
                "((ec:2.4.*) OR (ec:4.*) OR (protein_name:transferase) OR "
                "(protein_name:lyase) OR (protein_name:phosphorylase) OR "
                "(protein_name:transglycosylase))"
            ),
        },
    )
}


def _lane_queries_for(
    families: tuple[str, ...],
    *,
    include_alternate_name_lanes: bool = False,
    only_alternate_name_lanes: bool = False,
) -> tuple[dict[str, str], ...]:
    lanes: list[dict[str, str]] = []
    for family in families:
        if family not in FAMILY_LANE_QUERIES:
            raise ValueError(f"{family!r} is not a glycoside hydrolase family")
        if include_alternate_name_lanes or only_alternate_name_lanes:
            lanes.extend(ALTERNATE_NAME_LANE_QUERIES[family])
        if not only_alternate_name_lanes:
            lanes.extend(FAMILY_LANE_QUERIES[family])
    return tuple(lanes)


def build_glycoside_hydrolase_sourcing(
    *,
    families: tuple[str, ...] = FAMILIES,
    max_records_per_lane: int = 80,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_GLYCOSIDE_HYDROLASE_CAP_CEILING,
    record_offset_per_lane: int = 0,
    record_limit_per_lane: int | None = None,
    query_pages_per_lane: int = 1,
    include_alternate_name_lanes: bool = False,
    only_alternate_name_lanes: bool = False,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    families = tuple(families)
    lane_queries = _lane_queries_for(
        families,
        include_alternate_name_lanes=include_alternate_name_lanes,
        only_alternate_name_lanes=only_alternate_name_lanes,
    )
    caps_by_family = {family: cap_ceiling for family in families}
    if query_pages_per_lane < 1:
        raise ValueError("query_pages_per_lane must be positive")
    if query_pages_per_lane == 1:
        paged_query_fetcher = query_fetcher
    else:
        def paged_query_fetcher(query: str, size: int) -> dict[str, Any]:
            return query_fetcher(query, size, max_pages=query_pages_per_lane)  # type: ignore[misc]

    pilot = build_external_source_ingestion_pilot(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=list(frozen_benchmark_payload) + list(expansion_payload),
        created_utc=created,
        max_records_per_lane=max_records_per_lane,
        record_offset_per_lane=record_offset_per_lane,
        record_limit_per_lane=record_limit_per_lane,
        lane_queries=lane_queries,
        query_fetcher=paged_query_fetcher,
        entry_fetcher=entry_fetcher,
        rhea_fetcher=rhea_fetcher,
    )
    index = build_current702_reference_index(
        current_manifest_payload=current_manifest_payload,
        frozen_benchmark_payload=frozen_benchmark_payload,
        expansion_payload=expansion_payload,
    )
    disambig = build_cofactor_ec_disambiguation(
        pools=[
            {
                "pool": "glycoside_hydrolase_broadened_handle_fresh_fetch",
                "path": "glycoside_hydrolase_broadened_handle_fresh_fetch",
                "rows": _bridge_pilot_rows_for_disambiguation(pilot["rows"]),
            }
        ],
        registry=expansion_payload,
        index=index,
    )

    family_set = set(families)
    target_labels = [
        label for label in disambig["applied_labels"] if label.get("fingerprint_id") in family_set
    ]
    off_target_labels = [
        label
        for label in disambig["applied_labels"]
        if label.get("fingerprint_id") not in family_set
    ]

    state = build_diversity_state(frozen_benchmark_payload, expansion_payload)
    gate = evaluate_batch(
        target_labels,
        state,
        per_cluster_cap=per_cluster_cap,
        target_floor=target_floor,
    )
    admit_ids = set(gate["admit_entry_ids"])
    gate_admitted = [label for label in target_labels if label.get("entry_id") in admit_ids]
    throttled = [label for label in target_labels if label.get("entry_id") not in admit_ids]

    combined_counts = _fingerprint_counts(frozen_benchmark_payload) + _fingerprint_counts(
        expansion_payload
    )
    admitted: list[dict[str, Any]] = []
    cap_trimmed: list[dict[str, Any]] = []
    kept_per_fp: Counter = Counter()
    for label in gate_admitted:
        fp = label.get("fingerprint_id")
        cap = caps_by_family.get(fp, cap_ceiling)
        if combined_counts.get(fp, 0) + kept_per_fp[fp] >= cap:
            cap_trimmed.append(label)
            continue
        kept_per_fp[fp] += 1
        admitted.append(label)

    cap_trimmed_counts = _fingerprint_counts(cap_trimmed)
    admitted_counts = _fingerprint_counts(admitted)
    off_target_counts = _fingerprint_counts(off_target_labels)

    floor_projection = {}
    for family in families:
        before = combined_counts.get(family, 0)
        added = admitted_counts.get(family, 0)
        projected = before + added
        cap = caps_by_family[family]
        floor_projection[family] = {
            "combined_before": before,
            "admitted_this_run": added,
            "projected_combined": projected,
            "deficit_to_floor_before": max(target_floor - before, 0),
            "deficit_to_floor_after": max(target_floor - projected, 0),
            "floor_reached": projected >= target_floor,
            "cap_ceiling": cap,
            "chemistry_confusable": True,
            "held_at_cap_this_run": cap_trimmed_counts.get(family, 0),
            "projected_over_cap": projected > cap,
            "deploy_missing_active_site_context": DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT.get(
                family
            ),
        }

    combined_total = len(frozen_benchmark_payload) + len(expansion_payload)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_glycosidase_active_site_annotation",
        "stage": "scaling_plan_to_10k:wire_glycoside_hydrolase_broadened_handle",
        "families_sourced": list(families),
        "deploy_missing_active_site_context_per_family": {
            family: DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT.get(family) for family in families
        },
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_keyword_glycosidase_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "glycoside_hydrolase_handles_scope_admission_only": True,
            "broadened_handles_never_predictive_features": True,
            "ec_never_a_counted_corroborator": True,
            "trust_tier_n_of_m_requires_at_least_one_mechanism_axis": True,
            "transferase_phosphorylase_lyase_side_ec_guard": True,
            "off_target_fingerprint_matches_held": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "multi_fingerprint_signal_rows_held": True,
            "alternate_name_source_lanes_enabled": include_alternate_name_lanes,
            "only_alternate_name_source_lanes_enabled": only_alternate_name_lanes,
            "novelty_gated_against_both_registries": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
            "per_fingerprint_cap_ceiling_enforced_per_family": dict(
                sorted(caps_by_family.items())
            ),
            "no_fingerprint_pushed_over_cap": all(
                not p["projected_over_cap"] for p in floor_projection.values()
            ),
        },
        "floor_projection": floor_projection,
        "counts": {
            "lanes_queried": len(lane_queries),
            "max_records_per_lane": max_records_per_lane,
            "record_offset_per_lane": record_offset_per_lane,
            "record_limit_per_lane": record_limit_per_lane,
            "query_pages_per_lane": query_pages_per_lane,
            "alternate_name_lanes_enabled": include_alternate_name_lanes,
            "only_alternate_name_lanes_enabled": only_alternate_name_lanes,
            "fetched_candidate_rows": pilot["candidate_count"],
            "mechanism_corroborated_bronze_labels": len(target_labels),
            "off_target_fingerprint_matches_held": len(off_target_labels),
            "off_target_fingerprint_counts": dict(sorted(off_target_counts.items())),
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
            "Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, "
            "and cap gates pass, append `applied_labels` to "
            "data/registries/external_bronze_labels.json via "
            "`apply-external-annotation-anchored-import` with frozen current702 sha checks."
        ),
        "applied_labels": admitted,
        "off_target_fingerprint_matches_sample": [
            {"entry_id": label.get("entry_id"), "fingerprint_id": label.get("fingerprint_id")}
            for label in off_target_labels[:50]
        ],
        "throttled_or_rejected_sample": [
            {"entry_id": label.get("entry_id"), "fingerprint_id": label.get("fingerprint_id")}
            for label in throttled[:50]
        ],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Glycoside Hydrolase Sourcing - broadened evidence handles",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for EC 3.2.1 glycoside hydrolases via",
        "glycosidase family text, reviewed glycosidic-bond hydrolysis reaction context,",
        "and active-/binding-site acid/base or nucleophile annotations. EC / keyword /",
        "reaction text are scope-admission only, never predictive; transferase,",
        "transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-signal rows",
        "are guarded out.",
        "",
        "## Result",
        "",
        f"- Families sourced: {', '.join(audit['families_sourced'])}.",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
        f"- Query pages per lane: {c['query_pages_per_lane']}.",
        f"- Per-lane record window: offset {c['record_offset_per_lane']}, "
        f"limit {c['record_limit_per_lane']}.",
        f"- Fetched candidate rows: {c['fetched_candidate_rows']}.",
        f"- Target mechanism-corroborated bronze labels: {c['mechanism_corroborated_bronze_labels']} "
        f"(off-target held {c['off_target_fingerprint_matches_held']}; disambiguation holds "
        f"{c['disambiguation_hold_count']}; skipped {c['disambiguation_skip_count']}).",
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
            "## Disambiguation holds",
            "",
            f"- Hold reasons: {c.get('disambiguation_hold_reason_counts', {})}.",
            f"- Off-target held counts: {c.get('off_target_fingerprint_counts', {})}.",
            "",
            "## Guardrails",
            "",
            f"- Curated registry written: {audit['guardrails']['curated_registry_written']}.",
            "- EC scope-only / never predictive: "
            f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
            "- Glycoside hydrolase handles scope-admission only, never predictive: "
            f"{audit['guardrails']['broadened_handles_never_predictive_features']}.",
            "- EC never a counted corroborator: "
            f"{audit['guardrails']['ec_never_a_counted_corroborator']}.",
            "- Transferase/phosphorylase/lyase/side-EC guard: "
            f"{audit['guardrails']['transferase_phosphorylase_lyase_side_ec_guard']}.",
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


def write_glycoside_hydrolase_sourcing(
    *,
    out_path: Path,
    report_path: Path | None = None,
    families: tuple[str, ...] = FAMILIES,
    max_records_per_lane: int = 80,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_GLYCOSIDE_HYDROLASE_CAP_CEILING,
    record_offset_per_lane: int = 0,
    record_limit_per_lane: int | None = None,
    query_pages_per_lane: int = 1,
    include_alternate_name_lanes: bool = False,
    only_alternate_name_lanes: bool = False,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    audit = build_glycoside_hydrolase_sourcing(
        families=families,
        max_records_per_lane=max_records_per_lane,
        current_manifest_payload=_read_json(Path(current_manifest_path)),
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        target_floor=target_floor,
        per_cluster_cap=per_cluster_cap,
        cap_ceiling=cap_ceiling,
        record_offset_per_lane=record_offset_per_lane,
        record_limit_per_lane=record_limit_per_lane,
        query_pages_per_lane=query_pages_per_lane,
        include_alternate_name_lanes=include_alternate_name_lanes,
        only_alternate_name_lanes=only_alternate_name_lanes,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
