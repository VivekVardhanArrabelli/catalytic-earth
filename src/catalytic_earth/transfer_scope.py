from __future__ import annotations

from collections import Counter
from typing import Any, Callable

from .adapters import fetch_uniprot_query


def build_external_source_transfer_manifest(
    *,
    source_scale_audit: dict[str, Any],
    learned_retrieval_manifest: dict[str, Any],
    sequence_similarity_failure_sets: dict[str, Any],
    ontology_gap_audit: dict[str, Any],
    active_learning_queue: dict[str, Any],
    labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Scope the next non-M-CSA scaling method without creating labels."""
    source_meta = source_scale_audit.get("metadata", {})
    learned_meta = learned_retrieval_manifest.get("metadata", {})
    sequence_meta = sequence_similarity_failure_sets.get("metadata", {})
    ontology_meta = ontology_gap_audit.get("metadata", {})
    active_rows = active_learning_queue.get("rows", [])
    family_counts = Counter(
        str(row.get("top1_ontology_family") or row.get("ontology_family") or "unknown")
        for row in active_rows
        if isinstance(row, dict)
    )
    issue_counts = _issue_class_counts(active_rows)
    countable_label_count = _countable_label_count(labels)

    source_limit_reached = bool(source_meta.get("source_limit_reached"))
    transfer_blockers = [
        "external_source_ingestion_not_implemented",
        "external_out_of_distribution_calibration_not_built",
        "external_sequence_similarity_failure_sets_not_built",
    ]
    if source_limit_reached:
        transfer_blockers.insert(0, "m_csa_source_limit_reached")

    recommendation = (
        "prototype_external_source_transfer_before_next_count_growth"
        if source_limit_reached
        else "continue_m_csa_batches_before_external_transfer"
    )

    return {
        "metadata": {
            "method": "external_source_transfer_scope_manifest",
            "source_scale_recommendation": source_meta.get("recommendation"),
            "manifest_recommendation": recommendation,
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "current_countable_label_count": countable_label_count,
            "public_target_countable_labels": source_meta.get(
                "public_target_countable_labels", 10000
            ),
            "public_label_gap": max(
                int(source_meta.get("public_target_countable_labels", 10000) or 10000)
                - countable_label_count,
                0,
            ),
            "m_csa_observed_source_entries": source_meta.get("observed_source_entries"),
            "m_csa_target_source_entries": source_meta.get("target_source_entries"),
            "m_csa_source_limit_reached": source_limit_reached,
            "learned_retrieval_eligible_row_count": learned_meta.get(
                "eligible_row_count"
            ),
            "heuristic_control_required": True,
            "sequence_duplicate_cluster_count": sequence_meta.get(
                "duplicate_cluster_count"
            ),
            "ontology_gap_row_count": ontology_meta.get("row_count")
            or len(ontology_gap_audit.get("rows", [])),
            "active_queue_row_count": len(active_rows),
            "active_queue_top1_family_counts": dict(sorted(family_counts.items())),
            "active_queue_issue_class_counts": dict(sorted(issue_counts.items())),
            "blocker_count": len(transfer_blockers),
        },
        "source_plan": {
            "candidate_source": "UniProtKB/Swiss-Prot reviewed enzyme records",
            "minimum_fields": [
                "accession",
                "protein_name",
                "organism_name",
                "sequence",
                "ec",
                "reviewed",
                "xref_pdb",
                "xref_alphafolddb",
            ],
            "initial_filters": [
                "reviewed:true",
                "enzyme-annotated records with sequence and structure reference coverage",
                "exclude entries that collapse into existing exact-reference duplicate clusters before benchmark split assignment",
            ],
        },
        "required_guardrails": [
            "Keep heuristic geometry retrieval as the required control.",
            "Build external out-of-distribution calibration before countable import.",
            "Build external sequence-similarity failure sets before propagation.",
            "Route mechanism or family-boundary conflicts through review-only artifacts.",
            "Run the full label-factory gate before any external-source label counts.",
        ],
        "blockers": transfer_blockers,
        "next_actions": [
            "Implement a read-only external-source candidate manifest before importing labels.",
            "Attach OOD fold and sequence-similarity controls to the external manifest.",
            "Keep all transfer candidates non-countable until factory gates pass on an explicit decision artifact.",
        ],
    }


def build_external_source_query_manifest(
    *,
    transfer_manifest: dict[str, Any],
    ontology_gap_audit: dict[str, Any],
    max_lanes: int = 8,
) -> dict[str, Any]:
    """Create non-countable external-source query lanes from ontology pressure."""
    rows = ontology_gap_audit.get("rows", [])
    signal_counts: Counter[str] = Counter()
    exemplars: dict[str, list[str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id", ""))
        for signal in row.get("scope_signals", []) or []:
            signal = str(signal)
            signal_counts[signal] += 1
            exemplars.setdefault(signal, [])
            if entry_id and len(exemplars[signal]) < 10:
                exemplars[signal].append(entry_id)

    lane_rows = []
    for rank, (signal, count) in enumerate(signal_counts.most_common(max_lanes), start=1):
        lane_rows.append(
            {
                "rank": rank,
                "lane_id": f"external_source:{signal}",
                "scope_signal": signal,
                "trigger_row_count": count,
                "exemplar_entry_ids": exemplars.get(signal, []),
                "source_query_draft": _query_for_scope_signal(signal),
                "candidate_source": "UniProtKB/Swiss-Prot reviewed enzyme records",
                "countable_label_candidate": False,
                "required_controls": [
                    "external_ood_calibration",
                    "sequence_similarity_failure_set",
                    "mechanism_ontology_boundary_review",
                    "label_factory_gate",
                ],
            }
        )

    transfer_meta = transfer_manifest.get("metadata", {})
    return {
        "metadata": {
            "method": "external_source_query_manifest",
            "source_transfer_manifest_recommendation": transfer_meta.get(
                "manifest_recommendation"
            ),
            "ready_for_bounded_fetch": bool(lane_rows),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "lane_count": len(lane_rows),
            "max_lanes": max_lanes,
            "source_limit_reached": transfer_meta.get("m_csa_source_limit_reached"),
            "query_status": "draft_queries_only_not_executed",
        },
        "rows": lane_rows,
        "blockers": [
            "queries_not_fetched",
            "external_ood_calibration_not_built",
            "external_sequence_similarity_failure_sets_not_built",
            "external_candidates_not_factory_gated",
        ],
    }


def build_external_ood_calibration_plan(
    *,
    query_manifest: dict[str, Any],
    sequence_similarity_failure_sets: dict[str, Any],
    labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Plan external-source OOD checks before any label transfer can count."""
    query_rows = query_manifest.get("rows", [])
    sequence_meta = sequence_similarity_failure_sets.get("metadata", {})
    rows = []
    for row in query_rows:
        if not isinstance(row, dict):
            continue
        rows.append(
            {
                "lane_id": row.get("lane_id"),
                "scope_signal": row.get("scope_signal"),
                "source_query_draft": row.get("source_query_draft"),
                "countable_label_candidate": False,
                "calibration_controls": [
                    "exact_sequence_cluster_exclusion",
                    "near_duplicate_manual_review",
                    "family_holdout_split",
                    "source_text_leakage_check",
                    "abstention_threshold_recalibration",
                    "heuristic_retrieval_control_comparison",
                ],
                "promotion_rule": (
                    "external candidates remain review-only until calibrated "
                    "OOD controls and label-factory gates pass"
                ),
            }
        )
    return {
        "metadata": {
            "method": "external_ood_calibration_plan",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "lane_count": len(rows),
            "current_countable_label_count": _countable_label_count(labels),
            "sequence_duplicate_cluster_count": sequence_meta.get(
                "duplicate_cluster_count"
            ),
            "requires_external_candidate_fetch": True,
            "requires_embedding_or_structure_representation": True,
            "requires_heuristic_control": True,
        },
        "rows": rows,
        "blockers": [
            "external_candidates_not_fetched",
            "external_ood_scores_not_computed",
            "external_sequence_similarity_failure_sets_not_built",
            "external_abstention_threshold_not_calibrated",
        ],
    }


def build_external_source_candidate_sample(
    *,
    query_manifest: dict[str, Any],
    max_records_per_lane: int = 5,
    fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
) -> dict[str, Any]:
    """Fetch a bounded read-only external-source sample for transfer planning."""
    rows: list[dict[str, Any]] = []
    lane_summaries: list[dict[str, Any]] = []
    seen_accessions: set[str] = set()
    fetch_failures: list[dict[str, str]] = []
    for lane in query_manifest.get("rows", []):
        if not isinstance(lane, dict):
            continue
        query = str(lane.get("source_query_draft") or "").strip()
        lane_id = str(lane.get("lane_id") or "")
        if not query or not lane_id:
            continue
        try:
            payload = fetcher(query, max_records_per_lane)
        except Exception as exc:  # pragma: no cover - exercised by live artifacts
            fetch_failures.append(
                {
                    "lane_id": lane_id,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        lane_record_count = 0
        for record in payload.get("records", []):
            if not isinstance(record, dict):
                continue
            accession = str(record.get("accession") or "")
            if not accession or accession in seen_accessions:
                continue
            seen_accessions.add(accession)
            lane_record_count += 1
            rows.append(
                {
                    "lane_id": lane_id,
                    "scope_signal": lane.get("scope_signal"),
                    "source_query_draft": query,
                    "accession": accession,
                    "entry_name": record.get("entry_name"),
                    "protein_name": record.get("protein_name"),
                    "organism": record.get("organism"),
                    "length": record.get("length"),
                    "reviewed": record.get("reviewed"),
                    "ec_numbers": record.get("ec_numbers", []),
                    "pdb_ids": record.get("pdb_ids", []),
                    "alphafold_ids": record.get("alphafold_ids", []),
                    "countable_label_candidate": False,
                    "review_status": "external_source_unreviewed_by_label_factory",
                }
            )
        lane_summaries.append(
            {
                "lane_id": lane_id,
                "source_query_draft": query,
                "record_count": lane_record_count,
            }
        )
    return {
        "metadata": {
            "method": "external_source_candidate_sample",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_records_per_lane": max_records_per_lane,
            "lane_count": len(lane_summaries),
            "candidate_count": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "deduplication_key": "uniprot_accession",
            "sample_rule": "read_only_non_countable_transfer_planning_sample",
        },
        "lane_summaries": lane_summaries,
        "rows": rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "not_mapped_to_m_csa_active_site_evidence",
            "no_external_ood_calibration_scores",
            "not_reviewed_by_label_factory",
            "not_countable_without_explicit_decision_artifact",
        ],
    }


def audit_external_source_candidate_sample(
    candidate_sample: dict[str, Any],
) -> dict[str, Any]:
    """Guard against treating external-source samples as benchmark labels."""
    rows = [row for row in candidate_sample.get("rows", []) if isinstance(row, dict)]
    non_countable = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    reviewed_count = sum(
        1 for row in rows if str(row.get("reviewed")).lower() == "reviewed"
    )
    ec_supported_count = sum(1 for row in rows if row.get("ec_numbers"))
    structure_supported_count = sum(
        1 for row in rows if row.get("pdb_ids") or row.get("alphafold_ids")
    )
    duplicate_accessions = _duplicate_accessions(rows)
    blockers: list[str] = []
    if non_countable:
        blockers.append("external_rows_marked_countable")
    if duplicate_accessions:
        blockers.append("duplicate_external_accessions")
    if not rows:
        blockers.append("empty_external_candidate_sample")
    return {
        "metadata": {
            "method": "external_source_candidate_sample_guardrail_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(non_countable),
            "candidate_count": len(rows),
            "reviewed_count": reviewed_count,
            "ec_supported_count": ec_supported_count,
            "structure_supported_count": structure_supported_count,
            "duplicate_accession_count": len(duplicate_accessions),
            "duplicate_accessions": duplicate_accessions,
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "external candidates require OOD calibration and label-factory "
                "review before any countable import"
            )
        ],
    }


def _query_for_scope_signal(signal: str) -> str:
    query_by_signal = {
        "transferase_phosphoryl": (
            "(reviewed:true) AND (ec:2.7.* OR protein_name:kinase OR "
            "protein_name:phosphotransferase)"
        ),
        "lyase": "(reviewed:true) AND (ec:4.* OR protein_name:lyase)",
        "isomerase": "(reviewed:true) AND (ec:5.* OR protein_name:isomerase)",
        "oxidoreductase_long_tail": (
            "(reviewed:true) AND (ec:1.*) NOT (protein_name:flavin OR "
            "protein_name:heme)"
        ),
        "methyltransferase": (
            "(reviewed:true) AND (ec:2.1.1.* OR protein_name:methyltransferase)"
        ),
        "transferase_methyl": (
            "(reviewed:true) AND (ec:2.1.1.* OR protein_name:methyltransferase)"
        ),
        "glycan_chemistry": (
            "(reviewed:true) AND (ec:2.4.* OR ec:3.2.* OR "
            "protein_name:glycosyltransferase OR protein_name:glycosidase)"
        ),
    }
    return query_by_signal.get(signal, f"(reviewed:true) AND ({signal})")


def _issue_class_counts(rows: list[Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        if not isinstance(row, dict):
            continue
        issue_classes = row.get("issue_classes") or row.get("quality_risk_flags") or []
        if isinstance(issue_classes, list):
            for issue in issue_classes:
                counts[str(issue)] += 1
    return counts


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


def _duplicate_accessions(rows: list[dict[str, Any]]) -> list[str]:
    counts = Counter(str(row.get("accession") or "") for row in rows)
    return sorted(accession for accession, count in counts.items() if accession and count > 1)
