"""Broadened-handle sourcing for biotin-dependent carboxylases."""

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

ARTIFACT_ID = "v3_biotin_dependent_carboxylase_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"

FAMILY = "biotin_dependent_carboxylase"
FAMILIES: tuple[str, ...] = (FAMILY,)

# Rhea-first floor-closure scout: reviewed UniProt entries mapped to the
# ATP/hydrogencarbonate carboxylation reactions for EC 6.4.1 plus the
# biotin-carboxylase half-reaction RHEA:13501 / EC 6.3.4.14. This is source
# supply only; EC/Rhea/name handles remain excluded-context admission evidence.
_RHEA_CARBOXYLATION_IDS = (
    "11308",  # acetyl-CoA carboxylase, EC 6.4.1.2
    "13501",  # biotin carboxylase half-reaction, EC 6.3.4.14
    "13589",  # 3-methylcrotonyl-CoA carboxylase, EC 6.4.1.4
    "17701",  # geranoyl-CoA carboxylase, EC 6.4.1.5
    "18385",  # acetone carboxylase, EC 6.4.1.6
    "20425",  # 2-oxoglutarate carboxylase, EC 6.4.1.7
    "20844",  # pyruvate carboxylase, EC 6.4.1.1
    "23720",  # propionyl-CoA carboxylase, EC 6.4.1.3
    "28647",  # acetophenone carboxylase, EC 6.4.1.8
    "65292",  # butan-2-one carboxylase, EC 6.4.1.6
)
_RHEA_CARBOXYLATION_QUERY = " OR ".join(
    f"(rhea:{rhea_id})" for rhea_id in _RHEA_CARBOXYLATION_IDS
)

# EC 6.4.1 / 6.3.4 scopes reviewed biotin carboxylase candidates only.
# Admission requires non-EC biotin/biotinyl-Lys context, Rhea ATP/hydrogencarbonate/
# carboxybiotin participant text, carboxylase family text, or active-/binding-site
# mechanism evidence. Kinases, non-biotin ATP amide ligases, hydrolases, transferase
# side rows, non-scope side ECs, and multi-fingerprint rows are held.
FAMILY_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    FAMILY: (
        {
            "lane_id": "biotin_carboxylase_reviewed_ec_6_4_1",
            "target_family_lane": FAMILY,
            "query": (
                "(reviewed:true) AND (ec:6.4.1.*) AND "
                "((keyword:Biotin) OR (protein_name:biotin) OR "
                "(protein_name:carboxylase) OR (cc_cofactor:biotin))"
            ),
        },
        {
            "lane_id": "biotin_carboxylase_reviewed_ec_6_3_4",
            "target_family_lane": FAMILY,
            "query": (
                "(reviewed:true) AND (ec:6.3.4.*) AND "
                "((keyword:Biotin) OR (protein_name:biotin) OR "
                "(protein_name:carboxylase) OR (cc_cofactor:biotin))"
            ),
        },
    )
}
FLOOR_CLOSURE_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    FAMILY: (
        {
            "lane_id": "biotin_carboxylase_reviewed_rhea_carboxylation_floor_closure",
            "target_family_lane": FAMILY,
            "query": (
                f"(reviewed:true) AND ({_RHEA_CARBOXYLATION_QUERY}) AND "
                "((keyword:Biotin) OR (protein_name:biotin) OR "
                "(protein_name:carboxylase) OR (protein_name:carboxyltransferase) OR "
                "(cc_cofactor:biotin))"
            ),
        },
    )
}
ALTERNATE_FLOOR_CLOSURE_LANE_QUERIES: dict[str, tuple[dict[str, str], ...]] = {
    FAMILY: (
        {
            "lane_id": "biotin_carboxylase_reviewed_rhea_carboxylation_no_name_filter",
            "target_family_lane": FAMILY,
            "query": f"(reviewed:true) AND ({_RHEA_CARBOXYLATION_QUERY})",
        },
        {
            "lane_id": "biotin_carboxylase_reviewed_raw_ec_6_4_1_no_biotin_filter",
            "target_family_lane": FAMILY,
            "query": "(reviewed:true) AND (ec:6.4.1.*)",
        },
        {
            "lane_id": "biotin_carboxylase_reviewed_ec_6_3_4_carboxylase_no_biotin_filter",
            "target_family_lane": FAMILY,
            "query": "(reviewed:true) AND (ec:6.3.4.*) AND (protein_name:carboxylase)",
        },
    )
}


def _lane_queries_for(
    families: tuple[str, ...],
    *,
    include_floor_closure_lanes: bool = False,
    include_alternate_floor_closure_lanes: bool = False,
) -> tuple[dict[str, str], ...]:
    lanes: list[dict[str, str]] = []
    for family in families:
        if family not in FAMILY_LANE_QUERIES:
            raise ValueError(f"{family!r} is not a biotin carboxylase sourcing family")
        if include_floor_closure_lanes:
            lanes.extend(FLOOR_CLOSURE_LANE_QUERIES[family])
        if include_alternate_floor_closure_lanes:
            lanes.extend(ALTERNATE_FLOOR_CLOSURE_LANE_QUERIES[family])
        lanes.extend(FAMILY_LANE_QUERIES[family])
    return tuple(lanes)


def build_biotin_dependent_carboxylase_sourcing(
    *,
    families: tuple[str, ...] = FAMILIES,
    max_records_per_lane: int = 80,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = 150,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    rhea_fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
    include_floor_closure_lanes: bool = False,
    include_alternate_floor_closure_lanes: bool = False,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
    families = tuple(families)
    lane_queries = _lane_queries_for(
        families,
        include_floor_closure_lanes=include_floor_closure_lanes,
        include_alternate_floor_closure_lanes=include_alternate_floor_closure_lanes,
    )
    caps_by_family = {family: cap_ceiling for family in families}

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
    index = build_current702_reference_index(
        current_manifest_payload=current_manifest_payload,
        frozen_benchmark_payload=frozen_benchmark_payload,
        expansion_payload=expansion_payload,
    )
    disambig = build_cofactor_ec_disambiguation(
        pools=[
            {
                "pool": "biotin_dependent_carboxylase_broadened_handle_fresh_fetch",
                "path": "biotin_dependent_carboxylase_broadened_handle_fresh_fetch",
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
        "evidence_basis": "reviewed_swissprot_ec_rhea_biotin_carboxylase_annotation",
        "stage": "scaling_plan_to_10k:wire_biotin_dependent_carboxylase_broadened_handle",
        "families_sourced": list(families),
        "deploy_missing_active_site_context_per_family": {
            family: DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT.get(family) for family in families
        },
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_keyword_reaction_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "biotin_carboxylase_handles_scope_admission_only": True,
            "broadened_handles_never_predictive_features": True,
            "ec_never_a_counted_corroborator": True,
            "trust_tier_n_of_m_requires_at_least_one_mechanism_axis": True,
            "kinase_ligase_hydrolase_transferase_side_ec_boundary_guard": True,
            "off_target_fingerprint_matches_held": True,
            "rhea_first_floor_closure_source_lane_enabled": include_floor_closure_lanes,
            "alternate_floor_closure_source_lanes_enabled": (
                include_alternate_floor_closure_lanes
            ),
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
            "no_fingerprint_pushed_over_cap": all(
                not p["projected_over_cap"] for p in floor_projection.values()
            ),
        },
        "floor_projection": floor_projection,
        "counts": {
            "lanes_queried": len(lane_queries),
            "rhea_first_floor_closure_lanes_enabled": include_floor_closure_lanes,
            "alternate_floor_closure_lanes_enabled": include_alternate_floor_closure_lanes,
            "max_records_per_lane": max_records_per_lane,
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
            "data/registries/external_bronze_labels.json via the family script `--apply` "
            "with frozen current702 sha checks."
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
        "# Biotin-Dependent Carboxylase Sourcing - broadened evidence handles",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for EC 6.4.1 / 6.3.4 biotin carboxylases",
        "via biotin or biotinyl-Lys context, Rhea ATP/hydrogencarbonate/carboxybiotin",
        "participant evidence, carboxylase family text, and active-/binding-site annotations.",
        "EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;",
        "kinase, non-biotin ATP ligase, hydrolase, transferase side-EC, non-scope side-EC,",
        "and off-target fingerprint rows are guarded or held.",
        "",
        "## Result",
        "",
        f"- Families sourced: {', '.join(audit['families_sourced'])}.",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
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
        "## Floor projection (100-label floor; chemistry-confusable cap 150)",
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
            "- Biotin carboxylase handles scope-admission only, never predictive: "
            f"{audit['guardrails']['broadened_handles_never_predictive_features']}.",
            "- EC never a counted corroborator: "
            f"{audit['guardrails']['ec_never_a_counted_corroborator']}.",
            "- Kinase/non-biotin ATP ligase/hydrolase/transferase/side-EC boundary guards: "
            f"{audit['guardrails']['kinase_ligase_hydrolase_transferase_side_ec_boundary_guard']}.",
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


def write_biotin_dependent_carboxylase_sourcing(
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
    cap_ceiling: int = 150,
    include_floor_closure_lanes: bool = False,
    include_alternate_floor_closure_lanes: bool = False,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    audit = build_biotin_dependent_carboxylase_sourcing(
        families=families,
        max_records_per_lane=max_records_per_lane,
        current_manifest_payload=_read_json(Path(current_manifest_path)),
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        target_floor=target_floor,
        per_cluster_cap=per_cluster_cap,
        cap_ceiling=cap_ceiling,
        include_floor_closure_lanes=include_floor_closure_lanes,
        include_alternate_floor_closure_lanes=include_alternate_floor_closure_lanes,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
