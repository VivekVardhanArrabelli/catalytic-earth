from __future__ import annotations

from collections import Counter
from typing import Any, Callable
from urllib.request import Request, urlopen

from .adapters import fetch_rhea_by_ec, fetch_uniprot_entry, fetch_uniprot_query
from .structure import (
    atom_position,
    fetch_pdb_cif,
    ligand_context_from_atoms,
    pairwise_distances,
    parse_atom_site_loop,
    pocket_context_from_atoms,
    residue_centroid,
    select_residue_atoms,
)
from .geometry_retrieval import run_geometry_retrieval


ALPHAFOLD_CIF_URL = "https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v{version}.cif"
ALPHAFOLD_MODEL_VERSIONS = (6, 5, 4, 3, 2, 1)
USER_AGENT = "CatalyticEarth/0.0.1 research prototype"


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
                (
                    "exclude entries that collapse into existing exact-reference "
                    "duplicate clusters before benchmark split assignment"
                ),
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
            (
                "Keep all transfer candidates non-countable until factory gates "
                "pass on an explicit decision artifact."
            ),
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


def build_external_source_active_site_evidence_sample(
    *,
    active_site_evidence_queue: dict[str, Any],
    max_candidates: int = 8,
    fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
) -> dict[str, Any]:
    """Fetch bounded UniProt feature evidence for ready external candidates."""
    queue_rows = [
        row
        for row in active_site_evidence_queue.get("rows", [])
        if isinstance(row, dict)
    ]
    ready_rows = [
        row
        for row in queue_rows
        if row.get("queue_status") == "ready_for_active_site_evidence"
    ]
    skipped_queue_rows = len(queue_rows) - len(ready_rows)
    selected_rows = ready_rows[:max_candidates]
    candidate_summaries: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    active_site_feature_count = 0
    binding_site_feature_count = 0
    catalytic_activity_count = 0
    cofactor_comment_count = 0

    for row in selected_rows:
        accession = _normalize_accession(row.get("accession"))
        if not accession:
            continue
        try:
            payload = fetcher(accession)
        except Exception as exc:  # pragma: no cover - exercised by live artifacts
            fetch_failures.append(
                {
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        record = payload.get("record", payload)
        if not isinstance(record, dict):
            fetch_failures.append(
                {
                    "accession": accession,
                    "error_type": "ValueError",
                    "error": "UniProt feature payload did not contain a record",
                }
            )
            continue
        active_features = [
            feature
            for feature in record.get("active_site_features", []) or []
            if isinstance(feature, dict)
        ]
        binding_features = [
            feature
            for feature in record.get("binding_site_features", []) or []
            if isinstance(feature, dict)
        ]
        catalytic_comments = [
            comment
            for comment in record.get("catalytic_activity_comments", []) or []
            if isinstance(comment, dict)
        ]
        cofactor_comments = [
            comment
            for comment in record.get("cofactor_comments", []) or []
            if isinstance(comment, dict)
        ]
        active_site_feature_count += len(active_features)
        binding_site_feature_count += len(binding_features)
        catalytic_activity_count += len(catalytic_comments)
        cofactor_comment_count += len(cofactor_comments)
        evidence_status = _external_active_site_evidence_status(
            active_features=active_features,
            binding_features=binding_features,
            catalytic_comments=catalytic_comments,
        )
        status_counts[evidence_status] += 1
        blockers = _external_active_site_evidence_blockers(
            queue_row=row,
            active_features=active_features,
            catalytic_comments=catalytic_comments,
        )
        candidate_summaries.append(
            {
                "accession": accession,
                "active_site_feature_count": len(active_features),
                "alphafold_ids_sample": list(row.get("alphafold_ids", []) or [])[:5],
                "binding_site_feature_count": len(binding_features),
                "blockers": blockers,
                "broad_or_incomplete_ec_numbers": row.get(
                    "broad_or_incomplete_ec_numbers", []
                ),
                "catalytic_activity_count": len(catalytic_comments),
                "cofactor_comment_count": len(cofactor_comments),
                "countable_label_candidate": False,
                "evidence_status": evidence_status,
                "lane_id": row.get("lane_id"),
                "pdb_ids_sample": list(row.get("pdb_ids", []) or [])[:10],
                "protein_name": row.get("protein_name"),
                "queue_rank": row.get("rank"),
                "ready_for_label_import": False,
                "scope_signal": row.get("scope_signal"),
                "specific_ec_numbers": row.get("specific_ec_numbers", []),
                "uniprot_entry_name": record.get("entry_name"),
                "uniprot_review_status": record.get("entry_type"),
            }
        )
        for feature in active_features + binding_features:
            evidence_rows.append(
                _external_active_site_feature_row(
                    accession=accession,
                    queue_row=row,
                    feature=feature,
                )
            )

    candidate_count = len(candidate_summaries)
    return {
        "metadata": {
            "method": "external_source_active_site_evidence_sample",
            "source_method": active_site_evidence_queue.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_candidates": max_candidates,
            "ready_queue_candidate_count": len(ready_rows),
            "candidate_count": candidate_count,
            "candidate_with_active_site_feature_count": sum(
                1
                for summary in candidate_summaries
                if summary["active_site_feature_count"] > 0
            ),
            "candidate_with_binding_site_feature_count": sum(
                1
                for summary in candidate_summaries
                if summary["binding_site_feature_count"] > 0
            ),
            "candidate_with_catalytic_activity_count": sum(
                1
                for summary in candidate_summaries
                if summary["catalytic_activity_count"] > 0
            ),
            "active_site_feature_count": active_site_feature_count,
            "binding_site_feature_count": binding_site_feature_count,
            "catalytic_activity_count": catalytic_activity_count,
            "cofactor_comment_count": cofactor_comment_count,
            "feature_evidence_row_count": len(evidence_rows),
            "fetch_failure_count": len(fetch_failures),
            "skipped_queue_row_count": skipped_queue_rows,
            "evidence_status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "UniProt active-site feature evidence is review context only; "
                "external candidates remain non-countable until heuristic "
                "controls, decisions, and full label-factory gates pass"
            ),
        },
        "candidate_summaries": candidate_summaries,
        "rows": evidence_rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "active_site_features_not_mapped_to_candidate_structure",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "not_label_factory_gated",
        ],
    }


def audit_external_source_active_site_evidence_sample(
    active_site_evidence_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify external active-site evidence samples remain review-only context."""
    summaries = [
        row
        for row in active_site_evidence_sample.get("candidate_summaries", [])
        if isinstance(row, dict)
    ]
    rows = [
        row
        for row in active_site_evidence_sample.get("rows", [])
        if isinstance(row, dict)
    ]
    countable_items = [
        row
        for row in summaries + rows
        if row.get("countable_label_candidate") is not False
    ]
    import_ready_items = [
        row for row in summaries + rows if row.get("ready_for_label_import") is not False
    ]
    non_context_rows = [
        row for row in rows if row.get("evidence_status") != "uniprot_feature_context_only"
    ]
    active_site_feature_gap_count = sum(
        1
        for row in summaries
        if int(row.get("active_site_feature_count", 0) or 0) == 0
    )
    blockers: list[str] = []
    if not summaries:
        blockers.append("empty_active_site_evidence_sample")
    if countable_items:
        blockers.append("active_site_evidence_rows_marked_countable")
    if import_ready_items:
        blockers.append("active_site_evidence_rows_marked_ready_for_import")
    if non_context_rows:
        blockers.append("active_site_evidence_rows_missing_review_only_status")
    return {
        "metadata": {
            "method": "external_source_active_site_evidence_guardrail_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_items),
            "candidate_count": len(summaries),
            "feature_evidence_row_count": len(rows),
            "import_ready_item_count": len(import_ready_items),
            "non_context_row_count": len(non_context_rows),
            "active_site_feature_gap_count": active_site_feature_gap_count,
            "fetch_failure_count": active_site_evidence_sample.get(
                "metadata", {}
            ).get("fetch_failure_count", 0),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "active-site feature evidence requires structure mapping, "
                "heuristic controls, decisions, and label-factory gates before "
                "any external label import"
            )
        ],
    }


def build_external_source_heuristic_control_queue(
    *,
    active_site_evidence_sample: dict[str, Any],
    max_rows: int = 25,
) -> dict[str, Any]:
    """Queue external candidates for future heuristic geometry controls."""
    summaries = [
        row
        for row in active_site_evidence_sample.get("candidate_summaries", [])
        if isinstance(row, dict)
    ]
    ready_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()

    for summary in summaries:
        lane_id = str(summary.get("lane_id") or "unknown")
        lane_counts[lane_id] += 1
        active_site_count = int(summary.get("active_site_feature_count", 0) or 0)
        catalytic_count = int(summary.get("catalytic_activity_count", 0) or 0)
        broad_ec_numbers = list(summary.get("broad_or_incomplete_ec_numbers") or [])
        if active_site_count == 0:
            queue_status = "defer_active_site_feature_gap"
        elif catalytic_count == 0:
            queue_status = "defer_catalytic_activity_gap"
        elif broad_ec_numbers:
            queue_status = "defer_broad_ec_disambiguation"
        else:
            queue_status = "ready_for_heuristic_control_prototype"
        status_counts[queue_status] += 1
        queue_row = {
            "accession": summary.get("accession"),
            "active_site_feature_count": active_site_count,
            "alphafold_ids_sample": summary.get("alphafold_ids_sample", []),
            "binding_site_feature_count": summary.get("binding_site_feature_count", 0),
            "blockers": _external_heuristic_control_blockers(queue_status),
            "broad_or_incomplete_ec_numbers": broad_ec_numbers,
            "catalytic_activity_count": catalytic_count,
            "countable_label_candidate": False,
            "lane_id": summary.get("lane_id"),
            "pdb_ids_sample": summary.get("pdb_ids_sample", []),
            "protein_name": summary.get("protein_name"),
            "queue_rank": summary.get("queue_rank"),
            "queue_status": queue_status,
            "ready_for_label_import": False,
            "scope_signal": summary.get("scope_signal"),
            "specific_ec_numbers": summary.get("specific_ec_numbers", []),
        }
        if queue_status == "ready_for_heuristic_control_prototype":
            ready_rows.append(queue_row)
        else:
            deferred_rows.append(queue_row)

    ready_rows = sorted(
        ready_rows,
        key=lambda row: (
            -int(row.get("active_site_feature_count", 0) or 0),
            str(row.get("accession") or ""),
        ),
    )
    rows = []
    for rank, row in enumerate(ready_rows[:max_rows], start=1):
        item = dict(row)
        item["heuristic_control_rank"] = rank
        rows.append(item)
    return {
        "metadata": {
            "method": "external_source_heuristic_control_queue",
            "source_method": active_site_evidence_sample.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "ready_for_heuristic_control_execution": bool(rows),
            "countable_label_candidate_count": 0,
            "candidate_count": len(summaries),
            "ready_candidate_count": len(ready_rows),
            "exported_ready_candidate_count": len(rows),
            "deferred_candidate_count": len(deferred_rows),
            "max_rows": max_rows,
            "omitted_ready_candidate_count": max(len(ready_rows) - len(rows), 0),
            "queue_status_counts": dict(sorted(status_counts.items())),
            "lane_counts": dict(sorted(lane_counts.items())),
            "review_only_rule": (
                "this queue identifies external candidates ready for heuristic "
                "control scoring only; it cannot create countable labels"
            ),
        },
        "rows": rows,
        "deferred_rows": deferred_rows,
        "blockers": [
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_heuristic_control_queue(
    heuristic_control_queue: dict[str, Any],
) -> dict[str, Any]:
    """Verify heuristic-control queues remain non-countable review work."""
    rows = [
        row
        for section in ("rows", "deferred_rows")
        for row in heuristic_control_queue.get(section, [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    metadata = heuristic_control_queue.get("metadata", {})
    candidate_count = int(metadata.get("candidate_count", 0) or 0)
    ready_count = int(metadata.get("ready_candidate_count", 0) or 0)
    deferred_count = int(metadata.get("deferred_candidate_count", 0) or 0)
    blockers: list[str] = []
    if candidate_count == 0:
        blockers.append("empty_heuristic_control_queue")
    if candidate_count != ready_count + deferred_count:
        blockers.append("heuristic_control_queue_count_mismatch")
    if countable_rows:
        blockers.append("heuristic_control_rows_marked_countable")
    if import_ready_rows:
        blockers.append("heuristic_control_rows_marked_ready_for_import")
    return {
        "metadata": {
            "method": "external_source_heuristic_control_queue_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": candidate_count,
            "ready_candidate_count": ready_count,
            "deferred_candidate_count": deferred_count,
            "import_ready_row_count": len(import_ready_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "heuristic-control readiness is not a label decision; external "
                "rows still require scores, review decisions, and factory gates"
            )
        ],
    }


def build_external_source_structure_mapping_plan(
    *,
    active_site_evidence_sample: dict[str, Any],
    heuristic_control_queue: dict[str, Any],
    max_rows: int = 25,
) -> dict[str, Any]:
    """Plan structure mapping for external candidates with residue evidence."""
    feature_rows_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in active_site_evidence_sample.get("rows", []) or []:
        if not isinstance(row, dict) or row.get("feature_type") != "Active site":
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            feature_rows_by_accession.setdefault(accession, []).append(row)
    queue_rows = [
        row
        for section in ("rows", "deferred_rows")
        for row in heuristic_control_queue.get(section, [])
        if isinstance(row, dict)
    ]
    planned_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for row in queue_rows:
        accession = _normalize_accession(row.get("accession"))
        active_site_positions = [
            {
                "begin": feature.get("begin"),
                "description": feature.get("description"),
                "end": feature.get("end"),
                "evidence": feature.get("evidence", []),
            }
            for feature in feature_rows_by_accession.get(accession, [])
        ]
        pdb_ids = list(row.get("pdb_ids_sample", []) or [])
        alphafold_ids = list(row.get("alphafold_ids_sample", []) or [])
        if row.get("queue_status") != "ready_for_heuristic_control_prototype":
            mapping_status = "defer_before_structure_mapping"
        elif not active_site_positions:
            mapping_status = "defer_active_site_positions_missing"
        elif not (pdb_ids or alphafold_ids):
            mapping_status = "defer_structure_reference_missing"
        else:
            mapping_status = "ready_for_structure_mapping"
        status_counts[mapping_status] += 1
        mapping_row = {
            "accession": accession,
            "active_site_positions": active_site_positions,
            "active_site_position_count": len(active_site_positions),
            "alphafold_ids_sample": alphafold_ids,
            "blockers": _external_structure_mapping_blockers(mapping_status),
            "countable_label_candidate": False,
            "heuristic_control_rank": row.get("heuristic_control_rank"),
            "lane_id": row.get("lane_id"),
            "mapping_status": mapping_status,
            "pdb_ids_sample": pdb_ids,
            "protein_name": row.get("protein_name"),
            "ready_for_label_import": False,
            "scope_signal": row.get("scope_signal"),
            "specific_ec_numbers": row.get("specific_ec_numbers", []),
            "structure_mapping_rule": (
                "map UniProt active-site positions onto PDB or AlphaFold "
                "candidate structures before heuristic geometry scoring"
            ),
            "upstream_queue_blockers": row.get("blockers", []),
            "upstream_queue_status": row.get("queue_status"),
        }
        if mapping_status == "ready_for_structure_mapping":
            planned_rows.append(mapping_row)
        else:
            deferred_rows.append(mapping_row)
    planned_rows = planned_rows[:max_rows]
    return {
        "metadata": {
            "method": "external_source_structure_mapping_plan",
            "source_method": heuristic_control_queue.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "ready_for_structure_mapping": bool(planned_rows),
            "countable_label_candidate_count": 0,
            "candidate_count": len(queue_rows),
            "ready_mapping_candidate_count": len(planned_rows),
            "deferred_mapping_candidate_count": len(deferred_rows),
            "max_rows": max_rows,
            "mapping_status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "structure mapping plans prepare heuristic controls only and "
                "do not create countable labels"
            ),
        },
        "rows": planned_rows,
        "deferred_rows": deferred_rows,
        "blockers": [
            "structure_mapping_not_computed",
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_structure_mapping_plan(
    structure_mapping_plan: dict[str, Any],
) -> dict[str, Any]:
    """Verify external structure-mapping plans remain non-countable."""
    rows = [
        row
        for section in ("rows", "deferred_rows")
        for row in structure_mapping_plan.get(section, [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_position_rows = [
        row
        for row in structure_mapping_plan.get("rows", [])
        if isinstance(row, dict) and not row.get("active_site_positions")
    ]
    metadata = structure_mapping_plan.get("metadata", {})
    candidate_count = int(metadata.get("candidate_count", 0) or 0)
    ready_count = int(metadata.get("ready_mapping_candidate_count", 0) or 0)
    deferred_count = int(metadata.get("deferred_mapping_candidate_count", 0) or 0)
    blockers: list[str] = []
    if candidate_count == 0:
        blockers.append("empty_structure_mapping_plan")
    if candidate_count != ready_count + deferred_count:
        blockers.append("structure_mapping_plan_count_mismatch")
    if countable_rows:
        blockers.append("structure_mapping_rows_marked_countable")
    if import_ready_rows:
        blockers.append("structure_mapping_rows_marked_ready_for_import")
    if missing_position_rows:
        blockers.append("structure_mapping_ready_rows_missing_active_site_positions")
    return {
        "metadata": {
            "method": "external_source_structure_mapping_plan_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": candidate_count,
            "ready_mapping_candidate_count": ready_count,
            "deferred_mapping_candidate_count": deferred_count,
            "import_ready_row_count": len(import_ready_rows),
            "ready_rows_missing_position_count": len(missing_position_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "structure mapping is only a precursor to heuristic controls; "
                "external rows still require decisions and full factory gates"
            )
        ],
    }


def build_external_source_structure_mapping_sample(
    *,
    structure_mapping_plan: dict[str, Any],
    max_candidates: int = 4,
    cif_fetcher: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Resolve a bounded external active-site mapping sample on structures."""
    fetcher = cif_fetcher or fetch_external_structure_cif
    plan_rows = [
        row for row in structure_mapping_plan.get("rows", []) if isinstance(row, dict)
    ][:max_candidates]
    entries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    for row in plan_rows:
        accession = _normalize_accession(row.get("accession"))
        structure_source, structure_id = _external_structure_choice(row)
        if not structure_source or not structure_id:
            entry = _external_structure_mapping_failure_entry(
                row=row,
                status="structure_reference_missing",
                error="no PDB or AlphaFold structure handle available",
            )
            entries.append(entry)
            status_counts[entry["status"]] += 1
            continue
        try:
            atoms = parse_atom_site_loop(fetcher(structure_source, structure_id))
        except Exception as exc:  # pragma: no cover - exercised by live artifacts
            fetch_failures.append(
                {
                    "accession": accession,
                    "structure_source": structure_source,
                    "structure_id": structure_id,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            entry = _external_structure_mapping_failure_entry(
                row=row,
                status="structure_fetch_failed",
                error=str(exc),
                structure_source=structure_source,
                structure_id=structure_id,
            )
            entries.append(entry)
            status_counts[entry["status"]] += 1
            continue
        resolved = []
        missing_positions = []
        for position in row.get("active_site_positions", []) or []:
            residue_atoms = select_residue_atoms(
                atoms,
                chain_name=None,
                resid=position.get("begin"),
                code=None,
            )
            if not residue_atoms:
                missing_positions.append(position)
                continue
            first_atom = residue_atoms[0]
            resolved.append(
                {
                    "residue_node_id": f"uniprot:{accession}:{position.get('begin')}",
                    "code": first_atom.get("auth_comp_id")
                    or first_atom.get("label_comp_id"),
                    "chain_name": first_atom.get("auth_asym_id")
                    or first_atom.get("label_asym_id"),
                    "resid": position.get("begin"),
                    "atom_count": len(residue_atoms),
                    "centroid": residue_centroid(residue_atoms),
                    "ca": atom_position(residue_atoms, "CA"),
                    "roles": _external_active_site_roles(position),
                }
            )
        status = "ok" if resolved else "active_site_positions_unresolved"
        entry = {
            "accession": accession,
            "countable_label_candidate": False,
            "entry_id": f"uniprot:{accession}",
            "lane_id": row.get("lane_id"),
            "ligand_context": ligand_context_from_atoms(atoms, resolved),
            "missing_active_site_positions": missing_positions,
            "pairwise_distances_angstrom": pairwise_distances(resolved),
            "pocket_context": pocket_context_from_atoms(atoms, resolved),
            "protein_name": row.get("protein_name"),
            "ready_for_label_import": False,
            "resolved_residue_count": len(resolved),
            "residue_count": len(row.get("active_site_positions", []) or []),
            "residues": resolved,
            "scope_signal": row.get("scope_signal"),
            "specific_ec_numbers": row.get("specific_ec_numbers", []),
            "status": status,
            "structure_id": structure_id,
            "structure_source": structure_source,
        }
        entries.append(entry)
        status_counts[status] += 1
    ok_count = sum(1 for entry in entries if entry.get("status") == "ok")
    return {
        "metadata": {
            "method": "external_source_structure_mapping_sample",
            "source_method": structure_mapping_plan.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "ready_for_heuristic_control_scoring": ok_count > 0,
            "countable_label_candidate_count": 0,
            "candidate_count": len(entries),
            "mapped_candidate_count": ok_count,
            "fetch_failure_count": len(fetch_failures),
            "max_candidates": max_candidates,
            "status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "external structure mapping samples are heuristic-control "
                "inputs only and cannot create countable labels"
            ),
        },
        "entries": entries,
        "fetch_failures": fetch_failures,
        "blockers": [
            "heuristic_control_scores_not_computed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_structure_mapping_sample(
    structure_mapping_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify external structure mapping samples remain review-only controls."""
    entries = [
        entry
        for entry in structure_mapping_sample.get("entries", [])
        if isinstance(entry, dict)
    ]
    countable_entries = [
        entry for entry in entries if entry.get("countable_label_candidate") is not False
    ]
    import_ready_entries = [
        entry for entry in entries if entry.get("ready_for_label_import") is not False
    ]
    unresolved_entries = [
        entry for entry in entries if entry.get("status") != "ok"
    ]
    blockers: list[str] = []
    if not entries:
        blockers.append("empty_structure_mapping_sample")
    if countable_entries:
        blockers.append("structure_mapping_sample_entries_marked_countable")
    if import_ready_entries:
        blockers.append("structure_mapping_sample_entries_marked_ready_for_import")
    return {
        "metadata": {
            "method": "external_source_structure_mapping_sample_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_entries),
            "candidate_count": len(entries),
            "mapped_candidate_count": sum(
                1 for entry in entries if entry.get("status") == "ok"
            ),
            "unresolved_candidate_count": len(unresolved_entries),
            "import_ready_entry_count": len(import_ready_entries),
            "fetch_failure_count": structure_mapping_sample.get("metadata", {}).get(
                "fetch_failure_count", 0
            ),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "mapped external structures still require heuristic scoring, "
                "review decisions, and full label-factory gates before import"
            )
        ],
    }


def build_external_source_heuristic_control_scores(
    *,
    structure_mapping_sample: dict[str, Any],
    top_k: int = 5,
) -> dict[str, Any]:
    """Run seed-fingerprint retrieval as a review-only external control."""
    retrieval = run_geometry_retrieval(structure_mapping_sample, top_k=top_k)
    entry_index = {
        str(entry.get("entry_id")): entry
        for entry in structure_mapping_sample.get("entries", [])
        if isinstance(entry, dict) and entry.get("entry_id")
    }
    results = []
    top1_counts: Counter[str] = Counter()
    for result in retrieval.get("results", []):
        entry = entry_index.get(str(result.get("entry_id")), {})
        top_fingerprints = result.get("top_fingerprints", [])
        top1 = top_fingerprints[0].get("fingerprint_id") if top_fingerprints else None
        if top1:
            top1_counts[str(top1)] += 1
        results.append(
            {
                **result,
                "countable_label_candidate": False,
                "external_control_status": "heuristic_control_only",
                "external_lane_id": entry.get("lane_id"),
                "external_scope_signal": entry.get("scope_signal"),
                "protein_name": entry.get("protein_name"),
                "ready_for_label_import": False,
                "scope_top1_mismatch": _external_scope_top1_mismatch(
                    entry.get("scope_signal"), str(top1 or "")
                ),
                "specific_ec_numbers": entry.get("specific_ec_numbers", []),
                "structure_id": entry.get("structure_id"),
                "structure_source": entry.get("structure_source"),
            }
        )
    return {
        "metadata": {
            "method": "external_source_heuristic_control_scores",
            "source_method": structure_mapping_sample.get("metadata", {}).get(
                "method"
            ),
            "retrieval_method": retrieval.get("metadata", {}).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(results),
            "top_k": top_k,
            "top1_fingerprint_counts": dict(sorted(top1_counts.items())),
            "review_only_rule": (
                "external heuristic scores are controls for review decisions, "
                "not label imports"
            ),
        },
        "results": results,
        "blockers": [
            "external_decision_artifact_not_built",
            "external_ood_calibration_not_applied",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_heuristic_control_scores(
    heuristic_control_scores: dict[str, Any],
    max_dominant_top1_fraction: float = 0.6,
) -> dict[str, Any]:
    """Verify external heuristic score artifacts cannot be imported as labels."""
    results = [
        result
        for result in heuristic_control_scores.get("results", [])
        if isinstance(result, dict)
    ]
    top1_counts: Counter[str] = Counter()
    for result in results:
        top_fingerprints = result.get("top_fingerprints", [])
        if top_fingerprints:
            top1 = top_fingerprints[0].get("fingerprint_id")
            if top1:
                top1_counts[str(top1)] += 1
    dominant_top1, dominant_count = (
        top1_counts.most_common(1)[0] if top1_counts else (None, 0)
    )
    dominant_fraction = dominant_count / len(results) if results else 0.0
    countable_results = [
        result for result in results if result.get("countable_label_candidate") is not False
    ]
    import_ready_results = [
        result for result in results if result.get("ready_for_label_import") is not False
    ]
    scope_mismatch_count = sum(
        1 for result in results if result.get("scope_top1_mismatch")
    )
    blockers: list[str] = []
    if not results:
        blockers.append("empty_heuristic_control_scores")
    if countable_results:
        blockers.append("heuristic_control_scores_marked_countable")
    if import_ready_results:
        blockers.append("heuristic_control_scores_marked_ready_for_import")
    control_findings = []
    if dominant_fraction > max_dominant_top1_fraction:
        control_findings.append("heuristic_control_top1_fingerprint_collapse")
    if (
        dominant_top1 == "metal_dependent_hydrolase"
        and dominant_fraction > max_dominant_top1_fraction
    ):
        control_findings.append("heuristic_control_metal_hydrolase_collapse")
    if scope_mismatch_count:
        control_findings.append("heuristic_control_scope_top1_mismatch")
    return {
        "metadata": {
            "method": "external_source_heuristic_control_scores_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_results),
            "candidate_count": len(results),
            "dominant_top1_fingerprint": dominant_top1,
            "dominant_top1_fraction": round(dominant_fraction, 4),
            "max_dominant_top1_fraction": max_dominant_top1_fraction,
            "scope_top1_mismatch_count": scope_mismatch_count,
            "import_ready_result_count": len(import_ready_results),
            "control_finding_count": len(control_findings),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "control_findings": control_findings,
        "warnings": [
            (
                "heuristic control scores require OOD calibration, decisions, "
                "and full factory gates before any external label import"
            )
        ],
    }


def audit_external_source_failure_modes(
    *,
    active_site_evidence_sample_audit: dict[str, Any],
    heuristic_control_queue: dict[str, Any],
    heuristic_control_scores_audit: dict[str, Any],
    structure_mapping_sample_audit: dict[str, Any],
) -> dict[str, Any]:
    """Summarize external-transfer failure modes before label decisions."""
    heuristic_status_counts = heuristic_control_queue.get("metadata", {}).get(
        "queue_status_counts", {}
    )
    active_site_gap_count = int(
        active_site_evidence_sample_audit.get("metadata", {}).get(
            "active_site_feature_gap_count", 0
        )
        or 0
    )
    broad_ec_defer_count = int(
        heuristic_status_counts.get("defer_broad_ec_disambiguation", 0) or 0
    )
    unresolved_mapping_count = int(
        structure_mapping_sample_audit.get("metadata", {}).get(
            "unresolved_candidate_count", 0
        )
        or 0
    )
    control_findings = [
        str(item)
        for item in heuristic_control_scores_audit.get("control_findings", [])
    ]
    rows = []
    if active_site_gap_count:
        rows.append(
            {
                "failure_mode": "external_active_site_feature_gap",
                "row_count": active_site_gap_count,
                "recommended_action": (
                    "keep rows non-countable and source active-site positions "
                    "or alternate curated evidence"
                ),
            }
        )
    if broad_ec_defer_count:
        rows.append(
            {
                "failure_mode": "external_broad_ec_disambiguation_needed",
                "row_count": broad_ec_defer_count,
                "recommended_action": (
                    "resolve broad EC context before structure mapping or "
                    "heuristic-control interpretation"
                ),
            }
        )
    if unresolved_mapping_count:
        rows.append(
            {
                "failure_mode": "external_structure_mapping_unresolved",
                "row_count": unresolved_mapping_count,
                "recommended_action": (
                    "repair structure fetch or residue-position mapping before "
                    "heuristic-control scoring"
                ),
            }
        )
    for finding in control_findings:
        rows.append(
            {
                "failure_mode": finding,
                "row_count": heuristic_control_scores_audit.get("metadata", {}).get(
                    "candidate_count", 0
                ),
                "recommended_action": (
                    "treat external heuristic scores as a retrieval-control "
                    "failure signal; do not create labels until ontology or "
                    "representation controls separate the lane"
                ),
            }
        )
    return {
        "metadata": {
            "method": "external_source_failure_mode_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "failure_mode_count": len(rows),
            "active_site_feature_gap_count": active_site_gap_count,
            "broad_ec_disambiguation_count": broad_ec_defer_count,
            "heuristic_control_finding_count": len(control_findings),
            "structure_mapping_unresolved_count": unresolved_mapping_count,
            "guardrail_clean": True,
        },
        "rows": rows,
        "blockers": [],
        "warnings": [
            (
                "failure-mode rows are review-only controls and must block "
                "external label import until repaired or explicitly deferred"
            )
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
    active_site_evidence_sample: dict[str, Any] | None = None,
    active_site_evidence_sample_audit: dict[str, Any] | None = None,
    heuristic_control_queue: dict[str, Any] | None = None,
    heuristic_control_queue_audit: dict[str, Any] | None = None,
    structure_mapping_plan: dict[str, Any] | None = None,
    structure_mapping_plan_audit: dict[str, Any] | None = None,
    structure_mapping_sample: dict[str, Any] | None = None,
    structure_mapping_sample_audit: dict[str, Any] | None = None,
    heuristic_control_scores: dict[str, Any] | None = None,
    heuristic_control_scores_audit: dict[str, Any] | None = None,
    external_failure_mode_audit: dict[str, Any] | None = None,
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
    if active_site_evidence_sample is not None:
        sample_meta = active_site_evidence_sample.get("metadata", {})
        sample_items = [
            row
            for section in ("candidate_summaries", "rows")
            for row in active_site_evidence_sample.get(section, [])
            if isinstance(row, dict)
        ]
        queue_ready_count = (
            int(
                active_site_evidence_queue.get("metadata", {}).get(
                    "ready_candidate_count", 0
                )
                or 0
            )
            if active_site_evidence_queue is not None
            else None
        )
        sample_count = int(sample_meta.get("candidate_count", 0) or 0)
        sample_count_within_queue = (
            queue_ready_count is None or sample_count <= queue_ready_count
        )
        gates["active_site_evidence_sample_review_only"] = (
            sample_meta.get("ready_for_label_import") is False
            and sample_meta.get("countable_label_candidate_count") == 0
            and sample_count > 0
            and sample_count_within_queue
            and all(row.get("countable_label_candidate") is False for row in sample_items)
            and all(row.get("ready_for_label_import") is False for row in sample_items)
        )
    if active_site_evidence_sample_audit is not None:
        audit_meta = active_site_evidence_sample_audit.get("metadata", {})
        gates["active_site_evidence_sample_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("countable_label_candidate_count") == 0
            and audit_meta.get("ready_for_label_import") is False
        )
    if heuristic_control_queue is not None:
        queue_meta = heuristic_control_queue.get("metadata", {})
        queue_rows = [
            row
            for section in ("rows", "deferred_rows")
            for row in heuristic_control_queue.get(section, [])
            if isinstance(row, dict)
        ]
        ready_count = int(queue_meta.get("ready_candidate_count", 0) or 0)
        deferred_count = int(queue_meta.get("deferred_candidate_count", 0) or 0)
        candidate_count = int(queue_meta.get("candidate_count", 0) or 0)
        gates["heuristic_control_queue_review_only"] = (
            queue_meta.get("ready_for_label_import") is False
            and queue_meta.get("countable_label_candidate_count") == 0
            and queue_meta.get("ready_for_heuristic_control_execution") is True
            and candidate_count == ready_count + deferred_count
            and all(row.get("countable_label_candidate") is False for row in queue_rows)
            and all(row.get("ready_for_label_import") is False for row in queue_rows)
        )
    if heuristic_control_queue_audit is not None:
        audit_meta = heuristic_control_queue_audit.get("metadata", {})
        gates["heuristic_control_queue_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("countable_label_candidate_count") == 0
            and audit_meta.get("ready_for_label_import") is False
        )
    if structure_mapping_plan is not None:
        plan_meta = structure_mapping_plan.get("metadata", {})
        plan_rows = [
            row
            for section in ("rows", "deferred_rows")
            for row in structure_mapping_plan.get(section, [])
            if isinstance(row, dict)
        ]
        ready_count = int(plan_meta.get("ready_mapping_candidate_count", 0) or 0)
        deferred_count = int(
            plan_meta.get("deferred_mapping_candidate_count", 0) or 0
        )
        candidate_count = int(plan_meta.get("candidate_count", 0) or 0)
        gates["structure_mapping_plan_review_only"] = (
            plan_meta.get("ready_for_label_import") is False
            and plan_meta.get("countable_label_candidate_count") == 0
            and plan_meta.get("ready_for_structure_mapping") is True
            and candidate_count == ready_count + deferred_count
            and all(row.get("countable_label_candidate") is False for row in plan_rows)
            and all(row.get("ready_for_label_import") is False for row in plan_rows)
        )
    if structure_mapping_plan_audit is not None:
        audit_meta = structure_mapping_plan_audit.get("metadata", {})
        gates["structure_mapping_plan_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("countable_label_candidate_count") == 0
            and audit_meta.get("ready_for_label_import") is False
        )
    if structure_mapping_sample is not None:
        sample_meta = structure_mapping_sample.get("metadata", {})
        entries = [
            entry
            for entry in structure_mapping_sample.get("entries", [])
            if isinstance(entry, dict)
        ]
        gates["structure_mapping_sample_review_only"] = (
            sample_meta.get("ready_for_label_import") is False
            and sample_meta.get("countable_label_candidate_count") == 0
            and sample_meta.get("ready_for_heuristic_control_scoring") is True
            and all(
                entry.get("countable_label_candidate") is False for entry in entries
            )
            and all(entry.get("ready_for_label_import") is False for entry in entries)
        )
    if structure_mapping_sample_audit is not None:
        audit_meta = structure_mapping_sample_audit.get("metadata", {})
        gates["structure_mapping_sample_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("countable_label_candidate_count") == 0
            and audit_meta.get("ready_for_label_import") is False
        )
    if heuristic_control_scores is not None:
        score_meta = heuristic_control_scores.get("metadata", {})
        score_results = [
            result
            for result in heuristic_control_scores.get("results", [])
            if isinstance(result, dict)
        ]
        gates["heuristic_control_scores_review_only"] = (
            score_meta.get("ready_for_label_import") is False
            and score_meta.get("countable_label_candidate_count") == 0
            and score_meta.get("candidate_count") == len(score_results)
            and len(score_results) > 0
            and all(
                result.get("countable_label_candidate") is False
                for result in score_results
            )
            and all(
                result.get("ready_for_label_import") is False
                for result in score_results
            )
        )
    if heuristic_control_scores_audit is not None:
        audit_meta = heuristic_control_scores_audit.get("metadata", {})
        gates["heuristic_control_scores_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("countable_label_candidate_count") == 0
            and audit_meta.get("ready_for_label_import") is False
        )
    if external_failure_mode_audit is not None:
        audit_meta = external_failure_mode_audit.get("metadata", {})
        gates["external_failure_mode_audit_review_only"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
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
            "active_site_evidence_sampled_candidate_count": (
                active_site_evidence_sample.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if active_site_evidence_sample is not None
                else 0
            ),
            "active_site_feature_supported_candidate_count": (
                active_site_evidence_sample.get("metadata", {}).get(
                    "candidate_with_active_site_feature_count", 0
                )
                if active_site_evidence_sample is not None
                else 0
            ),
            "active_site_feature_gap_count": (
                active_site_evidence_sample_audit.get("metadata", {}).get(
                    "active_site_feature_gap_count", 0
                )
                if active_site_evidence_sample_audit is not None
                else 0
            ),
            "heuristic_control_ready_candidate_count": (
                heuristic_control_queue.get("metadata", {}).get(
                    "ready_candidate_count", 0
                )
                if heuristic_control_queue is not None
                else 0
            ),
            "heuristic_control_deferred_candidate_count": (
                heuristic_control_queue.get("metadata", {}).get(
                    "deferred_candidate_count", 0
                )
                if heuristic_control_queue is not None
                else 0
            ),
            "structure_mapping_ready_candidate_count": (
                structure_mapping_plan.get("metadata", {}).get(
                    "ready_mapping_candidate_count", 0
                )
                if structure_mapping_plan is not None
                else 0
            ),
            "structure_mapping_deferred_candidate_count": (
                structure_mapping_plan.get("metadata", {}).get(
                    "deferred_mapping_candidate_count", 0
                )
                if structure_mapping_plan is not None
                else 0
            ),
            "structure_mapping_sampled_candidate_count": (
                structure_mapping_sample.get("metadata", {}).get("candidate_count", 0)
                if structure_mapping_sample is not None
                else 0
            ),
            "structure_mapping_sample_mapped_candidate_count": (
                structure_mapping_sample.get("metadata", {}).get(
                    "mapped_candidate_count", 0
                )
                if structure_mapping_sample is not None
                else 0
            ),
            "heuristic_control_scored_candidate_count": (
                heuristic_control_scores.get("metadata", {}).get("candidate_count", 0)
                if heuristic_control_scores is not None
                else 0
            ),
            "external_failure_mode_count": (
                external_failure_mode_audit.get("metadata", {}).get(
                    "failure_mode_count", 0
                )
                if external_failure_mode_audit is not None
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


def _external_active_site_evidence_status(
    *,
    active_features: list[dict[str, Any]],
    binding_features: list[dict[str, Any]],
    catalytic_comments: list[dict[str, Any]],
) -> str:
    if active_features and catalytic_comments:
        return "active_site_and_catalytic_activity_context_found"
    if active_features:
        return "active_site_feature_context_found"
    if binding_features or catalytic_comments:
        return "binding_or_reaction_context_only"
    return "active_site_feature_missing"


def _external_active_site_evidence_blockers(
    *,
    queue_row: dict[str, Any],
    active_features: list[dict[str, Any]],
    catalytic_comments: list[dict[str, Any]],
) -> list[str]:
    blockers = [
        "active_site_features_not_mapped_to_candidate_structure",
        "heuristic_control_scores_not_computed",
        "external_decision_artifact_not_built",
        "not_label_factory_gated",
    ]
    if not active_features:
        blockers.append("uniprot_active_site_feature_missing")
    if not catalytic_comments:
        blockers.append("uniprot_catalytic_activity_comment_missing")
    if queue_row.get("broad_or_incomplete_ec_numbers"):
        blockers.append("specific_reaction_disambiguation_for_broad_ec")
    return blockers


def _external_active_site_feature_row(
    *,
    accession: str,
    queue_row: dict[str, Any],
    feature: dict[str, Any],
) -> dict[str, Any]:
    return {
        "accession": accession,
        "begin": feature.get("begin"),
        "countable_label_candidate": False,
        "description": feature.get("description"),
        "end": feature.get("end"),
        "evidence": feature.get("evidence", []),
        "evidence_status": "uniprot_feature_context_only",
        "feature_type": feature.get("feature_type"),
        "lane_id": queue_row.get("lane_id"),
        "ligand_id": feature.get("ligand_id"),
        "ligand_name": feature.get("ligand_name"),
        "ligand_note": feature.get("ligand_note"),
        "queue_rank": queue_row.get("rank"),
        "ready_for_label_import": False,
        "scope_signal": queue_row.get("scope_signal"),
    }


def _external_heuristic_control_blockers(queue_status: str) -> list[str]:
    blockers = [
        "heuristic_control_scores_not_computed",
        "external_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if queue_status == "defer_active_site_feature_gap":
        blockers.append("uniprot_active_site_feature_missing")
    elif queue_status == "defer_catalytic_activity_gap":
        blockers.append("uniprot_catalytic_activity_comment_missing")
    elif queue_status == "defer_broad_ec_disambiguation":
        blockers.append("specific_reaction_disambiguation_for_broad_ec")
    return blockers


def _external_structure_mapping_blockers(mapping_status: str) -> list[str]:
    blockers = [
        "structure_mapping_not_computed",
        "heuristic_control_scores_not_computed",
        "external_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if mapping_status == "defer_before_structure_mapping":
        blockers.append("upstream_evidence_or_disambiguation_deferred")
    elif mapping_status == "defer_active_site_positions_missing":
        blockers.append("uniprot_active_site_feature_missing")
    elif mapping_status == "defer_structure_reference_missing":
        blockers.append("external_structure_reference_missing")
    return blockers


def fetch_external_structure_cif(structure_source: str, structure_id: str) -> str:
    if structure_source == "alphafold":
        errors: list[str] = []
        for version in ALPHAFOLD_MODEL_VERSIONS:
            request = Request(
                ALPHAFOLD_CIF_URL.format(accession=structure_id, version=version),
                headers={"User-Agent": USER_AGENT},
            )
            try:
                with urlopen(request, timeout=30) as response:
                    return response.read().decode("utf-8", errors="replace")
            except Exception as exc:  # pragma: no cover - live-source fallback
                errors.append(f"v{version}:{type(exc).__name__}")
                continue
        raise ValueError(
            f"AlphaFold CIF fetch failed for {structure_id} across versions "
            f"{', '.join(errors)}"
        )
    if structure_source == "pdb":
        return fetch_pdb_cif(structure_id)
    raise ValueError(f"unsupported structure source: {structure_source}")


def _external_structure_choice(row: dict[str, Any]) -> tuple[str | None, str | None]:
    alphafold_ids = [
        _normalize_alphafold_model_accession(item)
        for item in row.get("alphafold_ids_sample", [])
        if _normalize_alphafold_model_accession(item)
    ]
    if alphafold_ids:
        return "alphafold", alphafold_ids[0]
    pdb_ids = [
        str(item).strip().upper()
        for item in row.get("pdb_ids_sample", [])
        if str(item).strip()
    ]
    if pdb_ids:
        return "pdb", pdb_ids[0]
    return None, None


def _normalize_alphafold_model_accession(value: Any) -> str:
    text = str(value or "").strip()
    if text.startswith("AF-") and "-F1" in text:
        return text.removeprefix("AF-").split("-F1", 1)[0]
    return text


def _external_structure_mapping_failure_entry(
    *,
    row: dict[str, Any],
    status: str,
    error: str,
    structure_source: str | None = None,
    structure_id: str | None = None,
) -> dict[str, Any]:
    accession = _normalize_accession(row.get("accession"))
    return {
        "accession": accession,
        "countable_label_candidate": False,
        "entry_id": f"uniprot:{accession}",
        "error": error,
        "lane_id": row.get("lane_id"),
        "ligand_context": {},
        "missing_active_site_positions": row.get("active_site_positions", []),
        "pairwise_distances_angstrom": [],
        "pocket_context": {},
        "protein_name": row.get("protein_name"),
        "ready_for_label_import": False,
        "resolved_residue_count": 0,
        "residue_count": len(row.get("active_site_positions", []) or []),
        "residues": [],
        "scope_signal": row.get("scope_signal"),
        "specific_ec_numbers": row.get("specific_ec_numbers", []),
        "status": status,
        "structure_id": structure_id,
        "structure_source": structure_source,
    }


def _external_active_site_roles(position: dict[str, Any]) -> list[str]:
    roles = ["uniprot_active_site_feature"]
    description = str(position.get("description") or "").strip()
    if description:
        roles.append(description)
    return roles


def _external_scope_top1_mismatch(scope_signal: Any, top1_fingerprint: str) -> bool:
    scope = str(scope_signal or "")
    if not scope or not top1_fingerprint:
        return False
    if scope in {
        "isomerase",
        "lyase",
        "oxidoreductase_long_tail",
        "transferase_methyl",
        "transferase_phosphoryl",
    }:
        return top1_fingerprint in {
            "metal_dependent_hydrolase",
            "ser_his_acid_hydrolase",
        }
    return False


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
