from __future__ import annotations

from collections import Counter
from typing import Any, Callable

from .adapters import fetch_rhea_by_ec, fetch_uniprot_query


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
            accession = _normalize_accession(record.get("accession"))
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


def build_external_source_candidate_manifest(
    *,
    candidate_sample: dict[str, Any],
    ood_calibration_plan: dict[str, Any],
    sequence_clusters: dict[str, Any],
    sequence_similarity_failure_sets: dict[str, Any],
    transfer_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Attach external-source samples to OOD and sequence-leakage controls."""
    sample_rows = [
        row for row in candidate_sample.get("rows", []) if isinstance(row, dict)
    ]
    ood_by_lane = {
        str(row.get("lane_id")): row
        for row in ood_calibration_plan.get("rows", [])
        if isinstance(row, dict) and row.get("lane_id")
    }
    sequence_index = _sequence_cluster_index(sequence_clusters)
    failure_cluster_ids = _sequence_failure_cluster_ids(sequence_similarity_failure_sets)
    duplicate_accessions = _duplicate_accessions(sample_rows)
    rows: list[dict[str, Any]] = []
    row_blocker_counts: Counter[str] = Counter()
    exact_overlap_count = 0
    failure_overlap_count = 0
    missing_ood_lane_count = 0
    structure_supported_count = 0
    reviewed_count = 0
    ec_supported_count = 0

    for row in sample_rows:
        accession = _normalize_accession(row.get("accession"))
        lane_id = str(row.get("lane_id") or "")
        ood_row = ood_by_lane.get(lane_id, {})
        calibration_controls = list(ood_row.get("calibration_controls") or [])
        sequence_matches = sequence_index.get(accession, [])
        sequence_cluster_ids = sorted(
            {str(match.get("sequence_cluster_id")) for match in sequence_matches}
        )
        failure_overlaps = sorted(set(sequence_cluster_ids) & failure_cluster_ids)
        has_structure_reference = bool(row.get("pdb_ids") or row.get("alphafold_ids"))
        is_reviewed = str(row.get("reviewed")).lower() == "reviewed"
        has_ec = bool(row.get("ec_numbers"))
        if sequence_matches:
            exact_overlap_count += 1
        if failure_overlaps:
            failure_overlap_count += 1
        if not calibration_controls:
            missing_ood_lane_count += 1
        if has_structure_reference:
            structure_supported_count += 1
        if is_reviewed:
            reviewed_count += 1
        if has_ec:
            ec_supported_count += 1

        blockers = _external_candidate_manifest_blockers(
            calibration_controls=calibration_controls,
            exact_reference_overlap=bool(sequence_matches),
            has_structure_reference=has_structure_reference,
        )
        row_blocker_counts.update(blockers)
        rows.append(
            {
                "accession": accession,
                "alphafold_ids": row.get("alphafold_ids", []),
                "blockers": blockers,
                "countable_label_candidate": False,
                "ec_numbers": row.get("ec_numbers", []),
                "entry_name": row.get("entry_name"),
                "external_source_controls": {
                    "heuristic_baseline_control_required": True,
                    "heuristic_control_status": "not_run_for_external_candidate",
                    "ood_calibration_controls": calibration_controls,
                    "ood_lane_present": bool(calibration_controls),
                    "promotion_rule": (
                        ood_row.get("promotion_rule")
                        or "external candidates remain review-only"
                    ),
                    "sequence_similarity_control": {
                        "cluster_source": sequence_clusters.get("metadata", {}).get(
                            "cluster_source"
                        ),
                        "exact_reference_overlap": bool(sequence_matches),
                        "matched_m_csa_entry_ids": sorted(
                            {
                                str(match.get("entry_id"))
                                for match in sequence_matches
                                if match.get("entry_id")
                            }
                        ),
                        "sequence_cluster_ids": sequence_cluster_ids,
                        "sequence_failure_set_overlap": bool(failure_overlaps),
                        "matched_failure_cluster_ids": failure_overlaps,
                        "review_rule": (
                            "exact or near-duplicate external candidates are "
                            "holdout/failure controls until mechanism evidence "
                            "and label-factory gates are explicit"
                        ),
                    },
                },
                "lane_id": lane_id,
                "length": row.get("length"),
                "organism": row.get("organism"),
                "pdb_ids": row.get("pdb_ids", []),
                "protein_name": row.get("protein_name"),
                "ready_for_label_import": False,
                "review_status": "external_source_review_only",
                "reviewed": row.get("reviewed"),
                "scope_signal": row.get("scope_signal"),
                "source_query_draft": row.get("source_query_draft"),
                "structure_reference_status": (
                    "pdb_or_alphafold_reference_present"
                    if has_structure_reference
                    else "missing_structure_reference"
                ),
            }
        )

    return {
        "metadata": {
            "method": "external_source_candidate_manifest",
            "source_sample_method": candidate_sample.get("metadata", {}).get("method"),
            "transfer_manifest_recommendation": transfer_manifest.get(
                "metadata", {}
            ).get("manifest_recommendation"),
            "ready_for_label_import": False,
            "ready_for_external_review": bool(rows)
            and not duplicate_accessions
            and missing_ood_lane_count == 0,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "lane_count": len({row.get("lane_id") for row in rows}),
            "ood_calibration_lane_count": len(ood_by_lane),
            "missing_ood_lane_count": missing_ood_lane_count,
            "heuristic_control_required": True,
            "heuristic_control_status": "not_run_for_external_candidates",
            "sequence_cluster_source": sequence_clusters.get("metadata", {}).get(
                "cluster_source"
            ),
            "sequence_failure_cluster_count": len(failure_cluster_ids),
            "exact_reference_overlap_count": exact_overlap_count,
            "sequence_failure_set_overlap_count": failure_overlap_count,
            "structure_supported_count": structure_supported_count,
            "reviewed_count": reviewed_count,
            "ec_supported_count": ec_supported_count,
            "duplicate_accession_count": len(duplicate_accessions),
            "duplicate_accessions": duplicate_accessions,
            "row_blocker_counts": dict(sorted(row_blocker_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "external_mechanism_evidence_not_attached",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
        ],
        "warnings": [
            (
                "this manifest is review-only transfer planning and must not be "
                "imported into the countable label registry"
            )
        ],
    }


def audit_external_source_candidate_manifest(
    candidate_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Verify a candidate manifest cannot be mistaken for label import input."""
    rows = [row for row in candidate_manifest.get("rows", []) if isinstance(row, dict)]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_heuristic_controls = [
        row
        for row in rows
        if not row.get("external_source_controls", {}).get(
            "heuristic_baseline_control_required"
        )
    ]
    missing_ood_controls = [
        row
        for row in rows
        if not row.get("external_source_controls", {}).get("ood_calibration_controls")
    ]
    missing_sequence_controls = [
        row
        for row in rows
        if not row.get("external_source_controls", {}).get(
            "sequence_similarity_control"
        )
    ]
    duplicate_accessions = _duplicate_accessions(rows)
    exact_overlap_count = sum(
        1
        for row in rows
        if row.get("external_source_controls", {})
        .get("sequence_similarity_control", {})
        .get("exact_reference_overlap")
    )
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_external_candidate_manifest")
    if countable_rows:
        blockers.append("external_manifest_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_manifest_rows_marked_ready_for_import")
    if missing_heuristic_controls:
        blockers.append("external_manifest_missing_heuristic_controls")
    if missing_ood_controls:
        blockers.append("external_manifest_missing_ood_controls")
    if missing_sequence_controls:
        blockers.append("external_manifest_missing_sequence_controls")
    if duplicate_accessions:
        blockers.append("duplicate_external_manifest_accessions")
    return {
        "metadata": {
            "method": "external_source_candidate_manifest_guardrail_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "import_ready_row_count": len(import_ready_rows),
            "missing_heuristic_control_count": len(missing_heuristic_controls),
            "missing_ood_control_count": len(missing_ood_controls),
            "missing_sequence_control_count": len(missing_sequence_controls),
            "duplicate_accession_count": len(duplicate_accessions),
            "duplicate_accessions": duplicate_accessions,
            "exact_reference_overlap_count": exact_overlap_count,
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "external candidate manifests are review-only and require "
                "separate evidence, decisions, and factory gates before import"
            )
        ],
    }


def build_external_source_evidence_plan(
    *,
    candidate_manifest: dict[str, Any],
    candidate_manifest_audit: dict[str, Any],
) -> dict[str, Any]:
    """Plan evidence collection needed before external candidates can be scored."""
    manifest_rows = [
        row for row in candidate_manifest.get("rows", []) if isinstance(row, dict)
    ]
    guardrail_clean = bool(
        candidate_manifest_audit.get("metadata", {}).get("guardrail_clean")
    )
    rows: list[dict[str, Any]] = []
    lane_counts: Counter[str] = Counter()
    next_action_counts: Counter[str] = Counter()
    required_evidence_counts: Counter[str] = Counter()
    exact_overlap_count = 0
    active_site_required_count = 0
    broad_ec_candidate_count = 0
    broad_ec_only_candidate_count = 0
    broad_ec_numbers_seen: set[str] = set()
    ec_specificity_counts: Counter[str] = Counter()

    for row in manifest_rows:
        lane_id = str(row.get("lane_id") or "")
        lane_counts[lane_id] += 1
        ec_numbers = [
            str(ec).strip()
            for ec in row.get("ec_numbers", []) or []
            if str(ec).strip()
        ]
        broad_ec_numbers = sorted(
            {ec for ec in ec_numbers if _ec_specificity(ec) == "broad_or_incomplete"}
        )
        specific_ec_numbers = sorted(
            {ec for ec in ec_numbers if _ec_specificity(ec) == "specific"}
        )
        if broad_ec_numbers:
            broad_ec_candidate_count += 1
            broad_ec_numbers_seen.update(broad_ec_numbers)
        if broad_ec_numbers and not specific_ec_numbers:
            broad_ec_only_candidate_count += 1
            ec_specificity_bucket = "broad_or_incomplete_ec_only"
        elif broad_ec_numbers:
            ec_specificity_bucket = "specific_and_broad_ec_context"
        elif specific_ec_numbers:
            ec_specificity_bucket = "specific_ec_only"
        else:
            ec_specificity_bucket = "missing_ec"
        ec_specificity_counts[ec_specificity_bucket] += 1
        sequence_control = row.get("external_source_controls", {}).get(
            "sequence_similarity_control", {}
        )
        exact_overlap = bool(sequence_control.get("exact_reference_overlap"))
        if exact_overlap:
            exact_overlap_count += 1
        active_site_required_count += 1
        required_evidence = [
            "curated_reaction_or_mechanism_evidence",
            "active_site_residue_positions",
            "structure_mapping_for_candidate",
            "heuristic_geometry_control_score",
            "external_ood_calibration_assignment",
            "sequence_similarity_holdout_or_exclusion",
            "review_decision_artifact",
            "full_label_factory_gate",
        ]
        if broad_ec_numbers:
            required_evidence.append("specific_reaction_disambiguation_for_broad_ec")
        if exact_overlap:
            next_action = "route_exact_reference_overlap_to_holdout_control"
        elif row.get("structure_reference_status") == "missing_structure_reference":
            next_action = "source_structure_reference_before_active_site_mapping"
        elif broad_ec_numbers and not specific_ec_numbers:
            next_action = "resolve_broad_or_incomplete_ec_before_active_site_mapping"
        else:
            next_action = "collect_active_site_and_mechanism_evidence"
        next_action_counts[next_action] += 1
        required_evidence_counts.update(required_evidence)
        rows.append(
            {
                "accession": row.get("accession"),
                "blockers": row.get("blockers", []),
                "broad_or_incomplete_ec_numbers": broad_ec_numbers,
                "countable_label_candidate": False,
                "ec_numbers": ec_numbers,
                "ec_specificity_bucket": ec_specificity_bucket,
                "evidence_collection_status": "not_started",
                "external_review_ready": guardrail_clean,
                "alphafold_ids": row.get("alphafold_ids", []),
                "lane_id": lane_id,
                "matched_m_csa_entry_ids": sequence_control.get(
                    "matched_m_csa_entry_ids", []
                ),
                "next_action": next_action,
                "pdb_ids": row.get("pdb_ids", []),
                "protein_name": row.get("protein_name"),
                "ready_for_label_import": False,
                "required_evidence": required_evidence,
                "scope_signal": row.get("scope_signal"),
                "sequence_similarity_bucket": (
                    "exact_reference_overlap_holdout"
                    if exact_overlap
                    else "requires_near_duplicate_search"
                ),
                "specific_ec_numbers": specific_ec_numbers,
                "structure_reference_status": row.get("structure_reference_status"),
            }
        )

    return {
        "metadata": {
            "method": "external_source_evidence_plan",
            "ready_for_label_import": False,
            "ready_for_evidence_collection": bool(rows) and guardrail_clean,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "lane_counts": dict(sorted(lane_counts.items())),
            "exact_reference_overlap_holdout_count": exact_overlap_count,
            "active_site_evidence_required_count": active_site_required_count,
            "broad_or_incomplete_ec_candidate_count": broad_ec_candidate_count,
            "broad_or_incomplete_ec_only_candidate_count": (
                broad_ec_only_candidate_count
            ),
            "broad_or_incomplete_ec_numbers": sorted(broad_ec_numbers_seen),
            "ec_specificity_counts": dict(sorted(ec_specificity_counts.items())),
            "next_action_counts": dict(sorted(next_action_counts.items())),
            "required_evidence_counts": dict(sorted(required_evidence_counts.items())),
            "source_manifest_guardrail_clean": guardrail_clean,
        },
        "rows": rows,
        "blockers": [
            "external_candidate_evidence_not_collected",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
        ],
        "warnings": [
            (
                "evidence plans define review work only and do not create "
                "countable external labels"
            )
        ],
    }


def build_external_source_evidence_request_export(
    *,
    evidence_plan: dict[str, Any],
    max_rows: int = 50,
) -> dict[str, Any]:
    """Export external-source evidence requests without label decisions."""
    plan_rows = [
        row for row in evidence_plan.get("rows", []) if isinstance(row, dict)
    ]
    rows = plan_rows[:max_rows]
    decision_counts = {"no_decision": len(rows)}
    return {
        "metadata": {
            "method": "external_source_evidence_request_export",
            "source_method": evidence_plan.get("metadata", {}).get("method"),
            "external_source_review_only": True,
            "exported_count": len(rows),
            "max_rows": max_rows,
            "omitted_by_max_rows": max(len(plan_rows) - len(rows), 0),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "decision_counts": decision_counts,
            "exact_reference_overlap_holdout_count": evidence_plan.get(
                "metadata", {}
            ).get("exact_reference_overlap_holdout_count", 0),
            "decision_schema": {
                "action": ["no_decision"],
                "external_source_resolution": ["needs_more_evidence"],
            },
            "review_only_rule": (
                "external evidence requests collect active-site and OOD evidence "
                "only; they cannot add benchmark labels through countable import"
            ),
        },
        "review_items": [
            {
                "rank": index,
                "entry_id": f"uniprot:{row.get('accession')}",
                "entry_name": row.get("accession"),
                "current_label": None,
                "external_source_context": row,
                "review_question": (
                    "Can curated reaction, active-site residue, structure-mapping, "
                    "OOD, sequence-holdout, and heuristic-control evidence be "
                    "assembled for this external source candidate?"
                ),
                "decision": {
                    "action": "no_decision",
                    "label_type": None,
                    "fingerprint_id": None,
                    "tier": "bronze",
                    "confidence": None,
                    "reviewer": None,
                    "rationale": None,
                    "evidence_score": None,
                    "review_status": "expert_reviewed",
                    "external_source_resolution": "needs_more_evidence",
                },
            }
            for index, row in enumerate(rows, start=1)
        ],
    }


def build_external_source_active_site_evidence_queue(
    *,
    evidence_plan: dict[str, Any],
    max_rows: int = 50,
) -> dict[str, Any]:
    """Prioritize review-only external candidates for active-site evidence work."""
    plan_rows = [
        row for row in evidence_plan.get("rows", []) if isinstance(row, dict)
    ]
    ready_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()
    broad_ec_candidate_count = 0

    for row in plan_rows:
        lane_id = str(row.get("lane_id") or "unknown")
        lane_counts[lane_id] += 1
        broad_ec_numbers = list(row.get("broad_or_incomplete_ec_numbers") or [])
        if broad_ec_numbers:
            broad_ec_candidate_count += 1
        next_action = str(row.get("next_action") or "")
        has_structure = bool(row.get("pdb_ids") or row.get("alphafold_ids"))
        has_specific_ec = bool(row.get("specific_ec_numbers"))
        if next_action == "route_exact_reference_overlap_to_holdout_control":
            queue_status = "defer_exact_reference_overlap_holdout"
        elif next_action == "resolve_broad_or_incomplete_ec_before_active_site_mapping":
            queue_status = "defer_broad_ec_disambiguation"
        elif not has_structure:
            queue_status = "defer_structure_reference_missing"
        elif not has_specific_ec:
            queue_status = "defer_specific_reaction_missing"
        else:
            queue_status = "ready_for_active_site_evidence"
        status_counts[queue_status] += 1
        queue_row = {
            "accession": row.get("accession"),
            "alphafold_ids": row.get("alphafold_ids", []),
            "broad_or_incomplete_ec_numbers": broad_ec_numbers,
            "countable_label_candidate": False,
            "ec_specificity_bucket": row.get("ec_specificity_bucket"),
            "lane_id": row.get("lane_id"),
            "matched_m_csa_entry_ids": row.get("matched_m_csa_entry_ids", []),
            "next_action": next_action,
            "pdb_ids": row.get("pdb_ids", []),
            "protein_name": row.get("protein_name"),
            "queue_status": queue_status,
            "ready_for_label_import": False,
            "required_evidence": row.get("required_evidence", []),
            "scope_signal": row.get("scope_signal"),
            "sequence_similarity_bucket": row.get("sequence_similarity_bucket"),
            "specific_ec_numbers": row.get("specific_ec_numbers", []),
        }
        if queue_status == "ready_for_active_site_evidence":
            ready_rows.append(queue_row)
        else:
            deferred_rows.append(queue_row)

    def priority_key(row: dict[str, Any]) -> tuple[int, str]:
        pdb_count = len(row.get("pdb_ids", []) or [])
        return (-pdb_count, str(row.get("accession") or ""))

    ready_rows = sorted(ready_rows, key=priority_key)
    exported_ready_rows = ready_rows[:max_rows]
    rows = []
    for rank, row in enumerate(exported_ready_rows, start=1):
        item = dict(row)
        item["rank"] = rank
        rows.append(item)

    return {
        "metadata": {
            "method": "external_source_active_site_evidence_queue",
            "source_method": evidence_plan.get("metadata", {}).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(plan_rows),
            "ready_candidate_count": len(ready_rows),
            "exported_ready_candidate_count": len(rows),
            "deferred_candidate_count": len(deferred_rows),
            "max_rows": max_rows,
            "omitted_ready_candidate_count": max(len(ready_rows) - len(rows), 0),
            "broad_or_incomplete_ec_candidate_count": broad_ec_candidate_count,
            "queue_status_counts": dict(sorted(status_counts.items())),
            "lane_counts": dict(sorted(lane_counts.items())),
            "review_only_rule": (
                "this queue prioritizes evidence collection only and cannot "
                "create countable external labels"
            ),
        },
        "rows": rows,
        "deferred_rows": deferred_rows,
        "blockers": [
            "active_site_positions_not_collected",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def check_external_source_transfer_gates(
    *,
    transfer_manifest: dict[str, Any],
    query_manifest: dict[str, Any],
    ood_calibration_plan: dict[str, Any],
    candidate_sample_audit: dict[str, Any],
    candidate_manifest: dict[str, Any],
    candidate_manifest_audit: dict[str, Any],
    lane_balance_audit: dict[str, Any],
    evidence_plan: dict[str, Any],
    evidence_request_export: dict[str, Any],
    review_only_import_safety_audit: dict[str, Any],
    active_site_evidence_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Gate external-source transfer artifacts before future label import work."""
    gates = {
        "transfer_manifest_blocks_label_import": (
            transfer_manifest.get("metadata", {}).get("ready_for_label_import")
            is False
            and transfer_manifest.get("metadata", {}).get(
                "countable_label_candidate_count"
            )
            == 0
        ),
        "query_manifest_blocks_label_import": (
            query_manifest.get("metadata", {}).get("ready_for_label_import") is False
            and query_manifest.get("metadata", {}).get(
                "countable_label_candidate_count"
            )
            == 0
        ),
        "ood_plan_requires_heuristic_control": (
            ood_calibration_plan.get("metadata", {}).get("ready_for_label_import")
            is False
            and ood_calibration_plan.get("metadata", {}).get(
                "requires_heuristic_control"
            )
            is True
        ),
        "candidate_sample_audit_guardrail_clean": bool(
            candidate_sample_audit.get("metadata", {}).get("guardrail_clean")
        )
        and candidate_sample_audit.get("metadata", {}).get(
            "countable_label_candidate_count"
        )
        == 0,
        "candidate_manifest_blocks_label_import": (
            candidate_manifest.get("metadata", {}).get("ready_for_label_import")
            is False
            and candidate_manifest.get("metadata", {}).get(
                "countable_label_candidate_count"
            )
            == 0
        ),
        "candidate_manifest_audit_guardrail_clean": bool(
            candidate_manifest_audit.get("metadata", {}).get("guardrail_clean")
        )
        and candidate_manifest_audit.get("metadata", {}).get(
            "countable_label_candidate_count"
        )
        == 0,
        "external_lane_balance_audit_guardrail_clean": bool(
            lane_balance_audit.get("metadata", {}).get("guardrail_clean")
        )
        and lane_balance_audit.get("metadata", {}).get(
            "countable_label_candidate_count"
        )
        == 0,
        "evidence_plan_blocks_label_import": (
            evidence_plan.get("metadata", {}).get("ready_for_label_import") is False
            and evidence_plan.get("metadata", {}).get("countable_label_candidate_count")
            == 0
        ),
        "evidence_request_export_review_only": (
            evidence_request_export.get("metadata", {}).get(
                "external_source_review_only"
            )
            is True
            and evidence_request_export.get("metadata", {}).get(
                "countable_label_candidate_count"
            )
            == 0
        ),
        "external_review_only_import_safety_clean": (
            review_only_import_safety_audit.get("metadata", {}).get(
                "countable_import_safe"
            )
            is True
            and review_only_import_safety_audit.get("metadata", {}).get(
                "total_new_countable_label_count"
            )
            == 0
        ),
    }
    if active_site_evidence_queue is not None:
        queue_meta = active_site_evidence_queue.get("metadata", {})
        queue_rows = [
            row
            for section in ("rows", "deferred_rows")
            for row in active_site_evidence_queue.get(section, [])
            if isinstance(row, dict)
        ]
        queue_candidate_count = queue_meta.get("candidate_count")
        evidence_candidate_count = evidence_plan.get("metadata", {}).get(
            "candidate_count"
        )
        ready_candidate_count = int(queue_meta.get("ready_candidate_count", 0) or 0)
        deferred_candidate_count = int(
            queue_meta.get("deferred_candidate_count", 0) or 0
        )
        candidate_count_matches_plan = (
            evidence_candidate_count is None
            or queue_candidate_count == evidence_candidate_count
        )
        gates["active_site_evidence_queue_review_only"] = (
            queue_meta.get("ready_for_label_import")
            is False
            and queue_meta.get("countable_label_candidate_count")
            == 0
            and queue_candidate_count
            == ready_candidate_count + deferred_candidate_count
            and candidate_count_matches_plan
            and all(row.get("countable_label_candidate") is False for row in queue_rows)
            and all(row.get("ready_for_label_import") is False for row in queue_rows)
        )
    blockers = [name for name, passed in gates.items() if not passed]
    return {
        "metadata": {
            "method": "external_source_transfer_gate_check",
            "gate_count": len(gates),
            "passed_gate_count": sum(1 for passed in gates.values() if passed),
            "ready_for_label_import": False,
            "ready_for_external_evidence_collection": (
                not blockers
                and bool(
                    evidence_plan.get("metadata", {}).get(
                        "ready_for_evidence_collection"
                    )
                )
            ),
            "countable_label_candidate_count": 0,
            "external_candidate_count": candidate_manifest.get("metadata", {}).get(
                "candidate_count", 0
            ),
            "exact_reference_overlap_holdout_count": evidence_plan.get(
                "metadata", {}
            ).get("exact_reference_overlap_holdout_count", 0),
            "external_lane_count": lane_balance_audit.get("metadata", {}).get(
                "lane_count", 0
            ),
            "external_dominant_lane_fraction": lane_balance_audit.get(
                "metadata", {}
            ).get("dominant_lane_fraction", 0.0),
            "active_site_ready_candidate_count": (
                active_site_evidence_queue.get("metadata", {}).get(
                    "ready_candidate_count", 0
                )
                if active_site_evidence_queue is not None
                else 0
            ),
            "active_site_deferred_candidate_count": (
                active_site_evidence_queue.get("metadata", {}).get(
                    "deferred_candidate_count", 0
                )
                if active_site_evidence_queue is not None
                else 0
            ),
            "heuristic_control_required": bool(
                candidate_manifest.get("metadata", {}).get(
                    "heuristic_control_required"
                )
            ),
            "blocker_count": len(blockers),
        },
        "gates": gates,
        "blockers": blockers,
        "warnings": [
            (
                "passing this gate authorizes review-only external evidence "
                "collection, not label import"
            )
        ],
    }


def build_external_source_reaction_evidence_sample(
    *,
    evidence_request_export: dict[str, Any],
    max_candidates: int = 10,
    max_reactions_per_ec: int = 3,
    fetcher: Callable[[str, int], dict[str, Any]] = fetch_rhea_by_ec,
) -> dict[str, Any]:
    """Fetch bounded reaction context for external candidates without labels."""
    review_items = [
        item
        for item in evidence_request_export.get("review_items", [])
        if isinstance(item, dict)
    ][:max_candidates]
    rows: list[dict[str, Any]] = []
    candidate_summaries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    queried_ec_numbers: set[str] = set()
    broad_ec_numbers: set[str] = set()
    for item in review_items:
        context = item.get("external_source_context", {})
        if not isinstance(context, dict):
            continue
        accession = _normalize_accession(context.get("accession"))
        ec_numbers = [
            str(ec).strip()
            for ec in context.get("ec_numbers", []) or []
            if str(ec).strip()
        ]
        candidate_record_count = 0
        candidate_broad_ec_numbers: list[str] = []
        for ec_number in ec_numbers:
            queried_ec_numbers.add(ec_number)
            ec_specificity = _ec_specificity(ec_number)
            if ec_specificity == "broad_or_incomplete":
                broad_ec_numbers.add(ec_number)
                candidate_broad_ec_numbers.append(ec_number)
            try:
                payload = fetcher(ec_number, max_reactions_per_ec)
            except Exception as exc:  # pragma: no cover - exercised by live artifacts
                fetch_failures.append(
                    {
                        "accession": accession,
                        "ec_number": ec_number,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )
                continue
            for reaction in payload.get("records", []):
                if not isinstance(reaction, dict):
                    continue
                candidate_record_count += 1
                rows.append(
                    {
                        "accession": accession,
                        "countable_label_candidate": False,
                        "ec_number": ec_number,
                        "ec_specificity": ec_specificity,
                        "entry_id": item.get("entry_id"),
                        "equation": reaction.get("equation"),
                        "evidence_status": "reaction_context_only",
                        "lane_id": context.get("lane_id"),
                        "mapped_enzyme_count": reaction.get("mapped_enzyme_count"),
                        "ready_for_label_import": False,
                        "rhea_id": reaction.get("rhea_id"),
                        "scope_signal": context.get("scope_signal"),
                    }
                )
        candidate_summaries.append(
            {
                "accession": accession,
                "broad_or_incomplete_ec_numbers": sorted(candidate_broad_ec_numbers),
                "ec_numbers": ec_numbers,
                "reaction_record_count": candidate_record_count,
            }
        )
    return {
        "metadata": {
            "method": "external_source_reaction_evidence_sample",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_candidates": max_candidates,
            "max_reactions_per_ec": max_reactions_per_ec,
            "candidate_count": len(review_items),
            "candidate_with_reaction_context_count": sum(
                1
                for summary in candidate_summaries
                if summary["reaction_record_count"] > 0
            ),
            "queried_ec_count": len(queried_ec_numbers),
            "broad_or_incomplete_ec_count": len(broad_ec_numbers),
            "broad_or_incomplete_ec_numbers": sorted(broad_ec_numbers),
            "reaction_record_count": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "review_only_rule": (
                "Rhea reaction context is evidence to review; it is not active-site "
                "mapping and cannot create countable labels"
            ),
        },
        "candidate_summaries": candidate_summaries,
        "rows": rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "reaction_context_not_mapped_to_candidate_active_site",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "not_label_factory_gated",
        ],
    }


def audit_external_source_reaction_evidence_sample(
    reaction_evidence_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify reaction-context rows remain review evidence, not labels."""
    rows = [
        row
        for row in reaction_evidence_sample.get("rows", [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    non_context_rows = [
        row for row in rows if row.get("evidence_status") != "reaction_context_only"
    ]
    broad_ec_rows = [
        row for row in rows if row.get("ec_specificity") == "broad_or_incomplete"
    ]
    blockers: list[str] = []
    if countable_rows:
        blockers.append("reaction_context_rows_marked_countable")
    if import_ready_rows:
        blockers.append("reaction_context_rows_marked_ready_for_import")
    if non_context_rows:
        blockers.append("reaction_context_rows_missing_review_only_status")
    if not rows:
        blockers.append("empty_reaction_evidence_sample")
    return {
        "metadata": {
            "method": "external_source_reaction_evidence_guardrail_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "reaction_record_count": len(rows),
            "import_ready_row_count": len(import_ready_rows),
            "non_context_row_count": len(non_context_rows),
            "broad_ec_context_row_count": len(broad_ec_rows),
            "broad_or_incomplete_ec_numbers": sorted(
                {str(row.get("ec_number")) for row in broad_ec_rows}
            ),
            "fetch_failure_count": reaction_evidence_sample.get("metadata", {}).get(
                "fetch_failure_count", 0
            ),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "reaction context requires active-site mapping and factory gates "
                "before any external label import"
            )
        ],
    }


def audit_external_source_lane_balance(
    *,
    candidate_manifest: dict[str, Any],
    min_lanes: int = 3,
    max_dominant_lane_fraction: float = 0.6,
) -> dict[str, Any]:
    """Check that external-source review work has not collapsed to one lane."""
    rows = [row for row in candidate_manifest.get("rows", []) if isinstance(row, dict)]
    lane_counts = Counter(str(row.get("lane_id") or "unknown") for row in rows)
    scope_counts = Counter(str(row.get("scope_signal") or "unknown") for row in rows)
    candidate_count = len(rows)
    dominant_lane, dominant_count = lane_counts.most_common(1)[0] if lane_counts else (None, 0)
    dominant_fraction = dominant_count / candidate_count if candidate_count else 0.0
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    blockers: list[str] = []
    if candidate_count == 0:
        blockers.append("empty_external_candidate_manifest")
    if len(lane_counts) < min_lanes:
        blockers.append("external_candidate_lane_count_below_floor")
    if dominant_fraction > max_dominant_lane_fraction:
        blockers.append("external_candidate_lane_collapse")
    if countable_rows:
        blockers.append("external_lane_audit_rows_marked_countable")
    return {
        "metadata": {
            "method": "external_source_lane_balance_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": candidate_count,
            "lane_count": len(lane_counts),
            "min_lanes": min_lanes,
            "dominant_lane": dominant_lane,
            "dominant_lane_fraction": round(dominant_fraction, 4),
            "max_dominant_lane_fraction": max_dominant_lane_fraction,
            "guardrail_clean": not blockers,
        },
        "lane_counts": dict(sorted(lane_counts.items())),
        "scope_signal_counts": dict(sorted(scope_counts.items())),
        "blockers": blockers,
        "warnings": [
            (
                "lane balance is a sampling guardrail only; it does not make "
                "external candidates countable"
            )
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
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import", False) is not False
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
    if import_ready_rows:
        blockers.append("external_rows_marked_ready_for_import")
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
            "import_ready_row_count": len(import_ready_rows),
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
    counts = Counter(_normalize_accession(row.get("accession")) for row in rows)
    return sorted(
        accession for accession, count in counts.items() if accession and count > 1
    )


def _normalize_accession(value: Any) -> str:
    return str(value or "").strip().upper()


def _ec_specificity(ec_number: str) -> str:
    parts = ec_number.split(".")
    if len(parts) != 4 or any(part in {"", "-"} for part in parts):
        return "broad_or_incomplete"
    return "specific"


def _sequence_cluster_index(
    sequence_clusters: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for row in sequence_clusters.get("rows", []):
        if not isinstance(row, dict):
            continue
        for accession in row.get("reference_uniprot_ids", []) or []:
            cleaned = _normalize_accession(accession)
            if cleaned:
                index.setdefault(cleaned, []).append(row)
    return index


def _sequence_failure_cluster_ids(
    sequence_similarity_failure_sets: dict[str, Any],
) -> set[str]:
    cluster_ids: set[str] = set()
    for row in sequence_similarity_failure_sets.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        cluster_id = row.get("sequence_cluster_id")
        if cluster_id:
            cluster_ids.add(str(cluster_id))
    return cluster_ids


def _external_candidate_manifest_blockers(
    *,
    calibration_controls: list[str],
    exact_reference_overlap: bool,
    has_structure_reference: bool,
) -> list[str]:
    blockers = [
        "external_mechanism_evidence_not_attached",
        "heuristic_control_scores_not_computed",
        "external_decision_artifact_not_built",
    ]
    if not calibration_controls:
        blockers.append("external_ood_lane_missing")
    if exact_reference_overlap:
        blockers.append("exact_sequence_cluster_overlap_existing_m_csa")
    if not has_structure_reference:
        blockers.append("external_structure_reference_missing")
    return blockers
