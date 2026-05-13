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


def audit_external_source_sequence_holdouts(
    *,
    candidate_manifest: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Make external exact-overlap and near-duplicate holdout work explicit."""
    manifest_rows = [
        row for row in candidate_manifest.get("rows", []) if isinstance(row, dict)
    ]
    rows: list[dict[str, Any]] = []
    lane_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    exact_overlap_count = 0
    failure_overlap_count = 0
    for row in manifest_rows:
        sequence_control = row.get("external_source_controls", {}).get(
            "sequence_similarity_control", {}
        )
        exact_overlap = bool(sequence_control.get("exact_reference_overlap"))
        failure_overlap = bool(sequence_control.get("sequence_failure_set_overlap"))
        if exact_overlap:
            holdout_status = "exact_reference_overlap_holdout"
            exact_overlap_count += 1
        elif failure_overlap:
            holdout_status = "sequence_failure_set_holdout"
            failure_overlap_count += 1
        else:
            holdout_status = "requires_near_duplicate_search"
        lane_id = str(row.get("lane_id") or "unknown")
        lane_counts[lane_id] += 1
        status_counts[holdout_status] += 1
        rows.append(
            {
                "accession": row.get("accession"),
                "blockers": _external_sequence_holdout_blockers(holdout_status),
                "countable_label_candidate": False,
                "holdout_status": holdout_status,
                "lane_id": row.get("lane_id"),
                "matched_failure_cluster_ids": sequence_control.get(
                    "matched_failure_cluster_ids", []
                ),
                "matched_m_csa_entry_ids": sequence_control.get(
                    "matched_m_csa_entry_ids", []
                ),
                "protein_name": row.get("protein_name"),
                "ready_for_label_import": False,
                "scope_signal": row.get("scope_signal"),
                "sequence_cluster_ids": sequence_control.get(
                    "sequence_cluster_ids", []
                ),
            }
        )
    rows = rows[:max_rows]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_external_sequence_holdout_audit")
    if countable_rows:
        blockers.append("external_sequence_holdout_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_sequence_holdout_rows_marked_ready_for_import")
    return {
        "metadata": {
            "method": "external_source_sequence_holdout_audit",
            "source_method": candidate_manifest.get("metadata", {}).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(manifest_rows),
            "emitted_row_count": len(rows),
            "max_rows": max_rows,
            "omitted_by_max_rows": max(len(manifest_rows) - len(rows), 0),
            "exact_reference_overlap_holdout_count": exact_overlap_count,
            "sequence_failure_set_holdout_count": failure_overlap_count,
            "near_duplicate_search_candidate_count": status_counts.get(
                "requires_near_duplicate_search", 0
            ),
            "lane_counts": dict(sorted(lane_counts.items())),
            "holdout_status_counts": dict(sorted(status_counts.items())),
            "guardrail_clean": not blockers,
            "review_only_rule": (
                "external sequence holdouts prevent sequence leakage and do "
                "not create labels"
            ),
        },
        "rows": rows,
        "blockers": blockers,
        "warnings": [
            (
                "near-duplicate search must be completed before any external "
                "label import decision"
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


def build_external_source_control_repair_plan(
    *,
    active_site_evidence_sample: dict[str, Any],
    heuristic_control_scores: dict[str, Any],
    heuristic_control_scores_audit: dict[str, Any],
    external_failure_mode_audit: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Turn external-transfer control failures into bounded non-countable repair work."""
    rows: list[dict[str, Any]] = []
    observed_failure_modes = [
        str(row.get("failure_mode"))
        for row in external_failure_mode_audit.get("rows", [])
        if isinstance(row, dict) and row.get("failure_mode")
    ]
    heuristic_findings = [
        str(item)
        for item in heuristic_control_scores_audit.get("control_findings", [])
    ]

    for summary in active_site_evidence_sample.get("candidate_summaries", []) or []:
        if not isinstance(summary, dict):
            continue
        active_site_count = int(summary.get("active_site_feature_count", 0) or 0)
        broad_ec_numbers = list(summary.get("broad_or_incomplete_ec_numbers") or [])
        if active_site_count == 0:
            row = _external_active_site_gap_repair_row(summary)
            rows.append(row)
        if broad_ec_numbers:
            row = _external_broad_ec_repair_row(summary)
            rows.append(row)

    for result in heuristic_control_scores.get("results", []) or []:
        if not isinstance(result, dict):
            continue
        top1 = _external_top1_fingerprint(result)
        if not top1:
            continue
        if (
            heuristic_findings
            or top1 == "metal_dependent_hydrolase"
            or bool(result.get("scope_top1_mismatch"))
        ):
            row = _external_heuristic_control_repair_row(
                result=result,
                heuristic_findings=heuristic_findings,
            )
            rows.append(row)

    rows = rows[:max_rows]
    row_type_counts = Counter(str(row.get("repair_type") or "unknown") for row in rows)
    repair_lane_counts = Counter(
        str(row.get("repair_lane") or "unknown") for row in rows
    )
    covered_failure_modes = _external_control_repair_coverage(
        rows=rows,
        observed_failure_modes=observed_failure_modes,
        heuristic_findings=heuristic_findings,
    )
    uncovered_failure_modes = [
        mode for mode in observed_failure_modes if mode not in covered_failure_modes
    ]
    active_site_gap_repair_count = sum(
        1 for row in rows if row.get("repair_type") == "active_site_feature_gap"
    )
    broad_ec_repair_count = sum(
        1 for row in rows if row.get("repair_type") == "broad_ec_disambiguation"
    )
    heuristic_repair_count = sum(
        1 for row in rows if row.get("repair_type") == "heuristic_control_failure"
    )
    return {
        "metadata": {
            "method": "external_source_control_repair_plan",
            "source_active_site_evidence_method": active_site_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "source_heuristic_scores_method": heuristic_control_scores.get(
                "metadata", {}
            ).get("method"),
            "source_failure_mode_method": external_failure_mode_audit.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_rows": max_rows,
            "repair_row_count": len(rows),
            "active_site_gap_repair_count": active_site_gap_repair_count,
            "broad_ec_disambiguation_repair_count": broad_ec_repair_count,
            "heuristic_control_repair_count": heuristic_repair_count,
            "scope_top1_mismatch_repair_count": sum(
                1
                for row in rows
                if row.get("repair_type") == "heuristic_control_failure"
                and row.get("scope_top1_mismatch")
            ),
            "metal_hydrolase_collapse_repair_count": sum(
                1
                for row in rows
                if row.get("repair_type") == "heuristic_control_failure"
                and row.get("top1_fingerprint") == "metal_dependent_hydrolase"
            ),
            "observed_failure_modes": observed_failure_modes,
            "covered_failure_modes": covered_failure_modes,
            "uncovered_failure_modes": uncovered_failure_modes,
            "repair_plan_complete_for_observed_failures": not uncovered_failure_modes,
            "row_type_counts": dict(sorted(row_type_counts.items())),
            "repair_lane_counts": dict(sorted(repair_lane_counts.items())),
            "review_only_rule": (
                "external repair plans convert control failures into review-only "
                "work items; they cannot create countable labels"
            ),
        },
        "rows": rows,
        "blockers": [
            "external_repair_work_not_completed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "repair rows are scoped evidence and representation work, not "
                "mechanism labels"
            )
        ],
    }


def audit_external_source_control_repair_plan(
    *,
    control_repair_plan: dict[str, Any],
    external_failure_mode_audit: dict[str, Any],
) -> dict[str, Any]:
    """Verify external control repair plans stay review-only and cover failures."""
    rows = [row for row in control_repair_plan.get("rows", []) if isinstance(row, dict)]
    metadata = control_repair_plan.get("metadata", {})
    failure_meta = external_failure_mode_audit.get("metadata", {})
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_next_evidence_rows = [
        row for row in rows if not row.get("required_next_evidence")
    ]
    blockers: list[str] = []
    if not rows and int(failure_meta.get("failure_mode_count", 0) or 0) > 0:
        blockers.append("external_control_repair_plan_empty")
    if countable_rows:
        blockers.append("external_control_repair_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_control_repair_rows_marked_ready_for_import")
    if missing_next_evidence_rows:
        blockers.append("external_control_repair_rows_missing_next_evidence")
    if metadata.get("repair_plan_complete_for_observed_failures") is not True:
        blockers.append("external_control_repair_plan_missing_failure_coverage")
    if (
        int(failure_meta.get("active_site_feature_gap_count", 0) or 0) > 0
        and int(metadata.get("active_site_gap_repair_count", 0) or 0) == 0
    ):
        blockers.append("active_site_feature_gaps_missing_repair_rows")
    if (
        int(failure_meta.get("broad_ec_disambiguation_count", 0) or 0) > 0
        and int(metadata.get("broad_ec_disambiguation_repair_count", 0) or 0) == 0
    ):
        blockers.append("broad_ec_disambiguation_missing_repair_rows")
    if (
        int(failure_meta.get("heuristic_control_finding_count", 0) or 0) > 0
        and int(metadata.get("heuristic_control_repair_count", 0) or 0) == 0
    ):
        blockers.append("heuristic_control_findings_missing_repair_rows")
    return {
        "metadata": {
            "method": "external_source_control_repair_plan_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "repair_row_count": len(rows),
            "import_ready_row_count": len(import_ready_rows),
            "missing_next_evidence_row_count": len(missing_next_evidence_rows),
            "observed_failure_mode_count": int(
                failure_meta.get("failure_mode_count", 0) or 0
            ),
            "covered_failure_mode_count": len(
                metadata.get("covered_failure_modes", []) or []
            ),
            "uncovered_failure_modes": metadata.get("uncovered_failure_modes", []),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "external control repairs are review-only prerequisites for "
                "future import decisions"
            )
        ],
    }


def build_external_source_binding_context_repair_plan(
    *,
    active_site_evidence_sample: dict[str, Any],
    control_repair_plan: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Collect binding-site context for active-site-gap external repair rows."""
    binding_rows_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in active_site_evidence_sample.get("rows", []) or []:
        if not isinstance(row, dict) or row.get("feature_type") != "Binding site":
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            binding_rows_by_accession.setdefault(accession, []).append(row)
    repair_rows = [
        row
        for row in control_repair_plan.get("rows", []) or []
        if isinstance(row, dict) and row.get("repair_type") == "active_site_feature_gap"
    ][:max_rows]
    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()
    binding_position_count = 0
    for repair_row in repair_rows:
        accession = _normalize_accession(repair_row.get("accession"))
        binding_features = binding_rows_by_accession.get(accession, [])
        binding_positions = [
            {
                "begin": feature.get("begin"),
                "description": feature.get("description"),
                "end": feature.get("end"),
                "evidence": feature.get("evidence", []),
                "ligand_id": feature.get("ligand_id"),
                "ligand_name": feature.get("ligand_name"),
                "ligand_note": feature.get("ligand_note"),
            }
            for feature in binding_features
        ]
        binding_position_count += len(binding_positions)
        if binding_positions:
            repair_status = "ready_for_binding_context_mapping"
        else:
            repair_status = "defer_binding_context_missing"
        status_counts[repair_status] += 1
        lane_counts[str(repair_row.get("lane_id") or "unknown")] += 1
        rows.append(
            {
                "accession": accession,
                "alphafold_ids_sample": repair_row.get("alphafold_ids_sample", []),
                "binding_position_count": len(binding_positions),
                "binding_positions": binding_positions,
                "blockers": _external_binding_context_repair_blockers(
                    repair_status
                ),
                "countable_label_candidate": False,
                "lane_id": repair_row.get("lane_id"),
                "pdb_ids_sample": repair_row.get("pdb_ids_sample", []),
                "protein_name": repair_row.get("protein_name"),
                "ready_for_label_import": False,
                "repair_lane": repair_row.get("repair_lane"),
                "repair_status": repair_status,
                "repair_type": "binding_context_for_active_site_gap",
                "required_next_evidence": [
                    "map binding-site positions to candidate structures as context only",
                    "source explicit active-site or catalytic residue positions before scoring",
                    "keep binding-only evidence non-countable until full gates pass",
                ],
                "scope_signal": repair_row.get("scope_signal"),
                "specific_ec_numbers": repair_row.get("specific_ec_numbers", []),
            }
        )
    return {
        "metadata": {
            "method": "external_source_binding_context_repair_plan",
            "source_active_site_evidence_method": active_site_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "source_control_repair_method": control_repair_plan.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_rows": max_rows,
            "candidate_count": len(rows),
            "ready_binding_context_candidate_count": sum(
                1
                for row in rows
                if row["repair_status"] == "ready_for_binding_context_mapping"
            ),
            "deferred_binding_context_candidate_count": sum(
                1
                for row in rows
                if row["repair_status"] != "ready_for_binding_context_mapping"
            ),
            "binding_position_count": binding_position_count,
            "repair_status_counts": dict(sorted(status_counts.items())),
            "lane_counts": dict(sorted(lane_counts.items())),
            "review_only_rule": (
                "binding context can prioritize active-site repair but cannot "
                "stand in for catalytic active-site evidence"
            ),
        },
        "rows": rows,
        "blockers": [
            "binding_context_not_mapped_to_structure",
            "active_site_positions_still_missing",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_binding_context_repair_plan(
    binding_context_repair_plan: dict[str, Any],
) -> dict[str, Any]:
    """Verify binding-context repair rows remain non-countable context."""
    rows = [
        row
        for row in binding_context_repair_plan.get("rows", [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_status_rows = [row for row in rows if not row.get("repair_status")]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_binding_context_repair_plan")
    if countable_rows:
        blockers.append("binding_context_repair_rows_marked_countable")
    if import_ready_rows:
        blockers.append("binding_context_repair_rows_marked_ready_for_import")
    if missing_status_rows:
        blockers.append("binding_context_repair_rows_missing_status")
    return {
        "metadata": {
            "method": "external_source_binding_context_repair_plan_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "ready_binding_context_candidate_count": binding_context_repair_plan.get(
                "metadata", {}
            ).get("ready_binding_context_candidate_count", 0),
            "deferred_binding_context_candidate_count": (
                binding_context_repair_plan.get("metadata", {}).get(
                    "deferred_binding_context_candidate_count", 0
                )
            ),
            "import_ready_row_count": len(import_ready_rows),
            "missing_status_row_count": len(missing_status_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "binding context repairs are evidence-collection work only and "
                "must not become countable labels"
            )
        ],
    }


def build_external_source_binding_context_mapping_sample(
    *,
    binding_context_repair_plan: dict[str, Any],
    max_candidates: int = 10,
    cif_fetcher: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Map binding-site repair positions onto structures as review-only context."""
    fetcher = cif_fetcher or fetch_external_structure_cif
    ready_rows = [
        row
        for row in binding_context_repair_plan.get("rows", [])
        if isinstance(row, dict)
        and row.get("repair_status") == "ready_for_binding_context_mapping"
    ][:max_candidates]
    entries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    for row in ready_rows:
        accession = _normalize_accession(row.get("accession"))
        structure_source, structure_id = _external_structure_choice(row)
        if not structure_source or not structure_id:
            entry = _external_binding_context_mapping_failure_entry(
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
            entry = _external_binding_context_mapping_failure_entry(
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
        for position in row.get("binding_positions", []) or []:
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
                    "atom_count": len(residue_atoms),
                    "ca": atom_position(residue_atoms, "CA"),
                    "centroid": residue_centroid(residue_atoms),
                    "chain_name": first_atom.get("auth_asym_id")
                    or first_atom.get("label_asym_id"),
                    "code": first_atom.get("auth_comp_id")
                    or first_atom.get("label_comp_id"),
                    "ligand_id": position.get("ligand_id"),
                    "ligand_name": position.get("ligand_name"),
                    "resid": position.get("begin"),
                    "residue_node_id": f"uniprot:{accession}:binding:{position.get('begin')}",
                    "roles": ["uniprot_binding_site_feature"],
                }
            )
        status = "ok" if resolved else "binding_positions_unresolved"
        entry = {
            "accession": accession,
            "binding_position_count": len(row.get("binding_positions", []) or []),
            "countable_label_candidate": False,
            "entry_id": f"uniprot:{accession}",
            "lane_id": row.get("lane_id"),
            "ligand_context": ligand_context_from_atoms(atoms, resolved),
            "missing_binding_positions": missing_positions,
            "pairwise_distances_angstrom": pairwise_distances(resolved),
            "pocket_context": pocket_context_from_atoms(atoms, resolved),
            "protein_name": row.get("protein_name"),
            "ready_for_label_import": False,
            "resolved_binding_position_count": len(resolved),
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
            "method": "external_source_binding_context_mapping_sample",
            "source_method": binding_context_repair_plan.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(entries),
            "mapped_candidate_count": ok_count,
            "fetch_failure_count": len(fetch_failures),
            "max_candidates": max_candidates,
            "status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "binding-context mapping is not active-site evidence and cannot "
                "create countable labels"
            ),
        },
        "entries": entries,
        "fetch_failures": fetch_failures,
        "blockers": [
            "active_site_positions_still_missing",
            "binding_context_not_label_evidence",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_binding_context_mapping_sample(
    binding_context_mapping_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify mapped binding context stays review-only."""
    entries = [
        entry
        for entry in binding_context_mapping_sample.get("entries", [])
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
        blockers.append("empty_binding_context_mapping_sample")
    if countable_entries:
        blockers.append("binding_context_mapping_entries_marked_countable")
    if import_ready_entries:
        blockers.append("binding_context_mapping_entries_marked_ready_for_import")
    return {
        "metadata": {
            "method": "external_source_binding_context_mapping_sample_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_entries),
            "candidate_count": len(entries),
            "mapped_candidate_count": sum(
                1 for entry in entries if entry.get("status") == "ok"
            ),
            "unresolved_candidate_count": len(unresolved_entries),
            "import_ready_entry_count": len(import_ready_entries),
            "fetch_failure_count": binding_context_mapping_sample.get(
                "metadata", {}
            ).get("fetch_failure_count", 0),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "binding-context mapping is only a repair aid for active-site "
                "feature gaps"
            )
        ],
    }


def build_external_source_representation_control_manifest(
    *,
    structure_mapping_sample: dict[str, Any],
    heuristic_control_scores: dict[str, Any],
    control_repair_plan: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Expose external mapped controls for a future learned representation path."""
    scores_by_entry = {
        str(row.get("entry_id")): row
        for row in heuristic_control_scores.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    repair_by_entry: dict[str, dict[str, Any]] = {}
    for row in control_repair_plan.get("rows", []) or []:
        if not isinstance(row, dict) or row.get("repair_type") != "heuristic_control_failure":
            continue
        entry_id = str(row.get("entry_id") or "")
        if entry_id:
            repair_by_entry[entry_id] = row

    rows: list[dict[str, Any]] = []
    for entry in structure_mapping_sample.get("entries", []) or []:
        if not isinstance(entry, dict) or not entry.get("entry_id"):
            continue
        entry_id = str(entry.get("entry_id"))
        score_row = scores_by_entry.get(entry_id, {})
        repair_row = repair_by_entry.get(entry_id, {})
        top1 = _external_top1_fingerprint(score_row)
        repair_lane = repair_row.get("repair_lane")
        ligand_context = entry.get("ligand_context", {})
        if not isinstance(ligand_context, dict):
            ligand_context = {}
        pocket_context = entry.get("pocket_context", {})
        if not isinstance(pocket_context, dict):
            pocket_context = {}
        pocket_descriptors = pocket_context.get("descriptors", {})
        if not isinstance(pocket_descriptors, dict):
            pocket_descriptors = {}
        eligible = (
            entry.get("status") == "ok"
            and int(entry.get("resolved_residue_count", 0) or 0) > 0
            and bool(score_row)
        )
        rows.append(
            {
                "accession": entry.get("accession"),
                "countable_label_candidate": False,
                "eligible_for_representation_control": eligible,
                "eligibility_blockers": _external_representation_control_blockers(
                    entry=entry,
                    score_row=score_row,
                ),
                "embedding_status": "not_computed_interface_only",
                "entry_id": entry_id,
                "external_control_label": "review_only_external_candidate",
                "feature_summary": {
                    "local_cofactor_families": ligand_context.get(
                        "cofactor_families", []
                    ),
                    "pairwise_distance_count": len(
                        entry.get("pairwise_distances_angstrom", [])
                    ),
                    "pocket_descriptor_names": sorted(pocket_descriptors),
                    "resolved_residue_count": entry.get("resolved_residue_count"),
                    "residue_codes": [
                        str(residue.get("code", "")).upper()
                        for residue in entry.get("residues", [])
                        if isinstance(residue, dict) and residue.get("code")
                    ],
                    "structure_id": entry.get("structure_id"),
                    "structure_source": entry.get("structure_source"),
                },
                "heuristic_baseline_control": {
                    "repair_lane": repair_lane,
                    "scope_top1_mismatch": bool(
                        score_row.get("scope_top1_mismatch")
                    ),
                    "top1_fingerprint_id": top1,
                    "top1_score": (
                        score_row.get("top_fingerprints", [{}])[0].get("score")
                        if score_row.get("top_fingerprints")
                        else None
                    ),
                },
                "lane_id": entry.get("lane_id"),
                "protein_name": entry.get("protein_name"),
                "ready_for_label_import": False,
                "scope_signal": entry.get("scope_signal"),
                "specific_ec_numbers": entry.get("specific_ec_numbers", []),
            }
        )

    rows = rows[:max_rows]
    top1_counts = Counter(
        str(row["heuristic_baseline_control"]["top1_fingerprint_id"])
        for row in rows
        if row["heuristic_baseline_control"].get("top1_fingerprint_id")
    )
    repair_lane_counts = Counter(
        str(row["heuristic_baseline_control"]["repair_lane"])
        for row in rows
        if row["heuristic_baseline_control"].get("repair_lane")
    )
    return {
        "metadata": {
            "method": "external_source_representation_control_manifest",
            "source_structure_mapping_method": structure_mapping_sample.get(
                "metadata", {}
            ).get("method"),
            "source_heuristic_scores_method": heuristic_control_scores.get(
                "metadata", {}
            ).get("method"),
            "source_control_repair_method": control_repair_plan.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "max_rows": max_rows,
            "candidate_count": len(rows),
            "eligible_control_count": sum(
                1 for row in rows if row["eligible_for_representation_control"]
            ),
            "ineligible_control_count": sum(
                1 for row in rows if not row["eligible_for_representation_control"]
            ),
            "scope_top1_mismatch_count": sum(
                1
                for row in rows
                if row["heuristic_baseline_control"]["scope_top1_mismatch"]
            ),
            "top1_fingerprint_counts": dict(sorted(top1_counts.items())),
            "repair_lane_counts": dict(sorted(repair_lane_counts.items())),
            "embedding_status": "not_computed_interface_only",
            "control_rule": (
                "external representation controls must be compared against the "
                "current heuristic geometry baseline before label decisions"
            ),
            "training_label_rule": (
                "external rows are review-only controls and are never countable "
                "training labels in this manifest"
            ),
        },
        "rows": rows,
        "blockers": [
            "external_embeddings_not_computed",
            "external_ood_calibration_not_applied",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
    }


def audit_external_source_representation_control_manifest(
    representation_control_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Verify external representation controls cannot be used as labels."""
    rows = [
        row
        for row in representation_control_manifest.get("rows", [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_heuristic_rows = [
        row for row in rows if not row.get("heuristic_baseline_control")
    ]
    metadata = representation_control_manifest.get("metadata", {})
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_external_representation_control_manifest")
    if countable_rows:
        blockers.append("external_representation_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_representation_rows_marked_ready_for_import")
    if missing_heuristic_rows:
        blockers.append("external_representation_rows_missing_heuristic_control")
    return {
        "metadata": {
            "method": "external_source_representation_control_manifest_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "eligible_control_count": metadata.get("eligible_control_count", 0),
            "import_ready_row_count": len(import_ready_rows),
            "missing_heuristic_control_row_count": len(missing_heuristic_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "representation-control rows are future scoring inputs, not "
                "external label decisions"
            )
        ],
    }


def build_external_source_representation_control_comparison(
    *,
    representation_control_manifest: dict[str, Any],
    heuristic_control_scores: dict[str, Any],
    reaction_evidence_sample: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Compare representation-control feature proxies with heuristic baseline calls."""
    scores_by_entry = {
        str(row.get("entry_id")): row
        for row in heuristic_control_scores.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    reaction_context_by_entry = _external_reaction_context_by_entry(
        reaction_evidence_sample
    )
    rows: list[dict[str, Any]] = []
    for manifest_row in representation_control_manifest.get("rows", []) or []:
        if not isinstance(manifest_row, dict) or not manifest_row.get("entry_id"):
            continue
        entry_id = str(manifest_row.get("entry_id"))
        score_row = scores_by_entry.get(entry_id, {})
        heuristic_control = manifest_row.get("heuristic_baseline_control", {})
        if not isinstance(heuristic_control, dict):
            heuristic_control = {}
        top1 = _external_top1_fingerprint(score_row) or heuristic_control.get(
            "top1_fingerprint_id"
        )
        scope_signal = str(
            manifest_row.get("scope_signal")
            or score_row.get("external_scope_signal")
            or ""
        )
        reaction_context = reaction_context_by_entry.get(
            entry_id, _empty_external_reaction_context(entry_id)
        )
        scope_mismatch = _external_scope_top1_mismatch(scope_signal, str(top1 or ""))
        comparison_status = _external_representation_proxy_status(
            scope_signal=scope_signal,
            top1_fingerprint=str(top1 or ""),
            reaction_context=reaction_context,
            scope_top1_mismatch=scope_mismatch,
        )
        rows.append(
            {
                "accession": manifest_row.get("accession"),
                "comparison_status": comparison_status,
                "countable_label_candidate": False,
                "embedding_status": "feature_proxy_no_embedding",
                "entry_id": entry_id,
                "feature_proxy_tokens": _external_representation_proxy_tokens(
                    manifest_row=manifest_row,
                    reaction_context=reaction_context,
                ),
                "heuristic_baseline_control": {
                    "scope_top1_mismatch": scope_mismatch,
                    "top1_fingerprint_id": top1,
                    "top1_score": heuristic_control.get("top1_score"),
                },
                "lane_id": manifest_row.get("lane_id"),
                "ready_for_label_import": False,
                "reaction_context": reaction_context,
                "recommended_representation_axes": _external_representation_axes(
                    scope_signal=scope_signal,
                    top1_fingerprint=str(top1 or ""),
                    reaction_context=reaction_context,
                    scope_top1_mismatch=scope_mismatch,
                ),
                "review_status": "representation_control_review_only",
                "scope_signal": scope_signal,
            }
        )

    rows = rows[:max_rows]
    status_counts = Counter(str(row["comparison_status"]) for row in rows)
    top1_counts = Counter(
        str(row["heuristic_baseline_control"].get("top1_fingerprint_id"))
        for row in rows
        if row["heuristic_baseline_control"].get("top1_fingerprint_id")
    )
    scope_counts = Counter(str(row.get("scope_signal") or "unknown") for row in rows)
    return {
        "metadata": {
            "method": "external_source_representation_control_comparison",
            "source_representation_control_method": representation_control_manifest.get(
                "metadata", {}
            ).get("method"),
            "source_heuristic_scores_method": heuristic_control_scores.get(
                "metadata", {}
            ).get("method"),
            "source_reaction_evidence_method": reaction_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "embedding_status": "feature_proxy_no_embedding",
            "comparison_rule": (
                "feature-proxy representation controls expose heuristic-collapse "
                "cases but do not compute embeddings or create labels"
            ),
            "scope_top1_mismatch_count": sum(
                1
                for row in rows
                if row["heuristic_baseline_control"].get("scope_top1_mismatch")
            ),
            "metal_hydrolase_collapse_flag_count": sum(
                1
                for row in rows
                if row["comparison_status"]
                == "proxy_flags_metal_hydrolase_collapse"
            ),
            "boundary_case_count": sum(
                1
                for row in rows
                if row["comparison_status"]
                == "proxy_boundary_case_requires_glycan_hydrolase_split"
            ),
            "reaction_context_missing_count": sum(
                1
                for row in rows
                if not row["reaction_context"].get("has_reaction_context")
            ),
            "comparison_status_counts": dict(sorted(status_counts.items())),
            "scope_signal_counts": dict(sorted(scope_counts.items())),
            "top1_fingerprint_counts": dict(sorted(top1_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "external_embeddings_not_computed",
            "external_ood_calibration_not_applied",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "representation-control comparisons are review-only diagnostics "
                "and cannot make external labels countable"
            )
        ],
    }


def audit_external_source_representation_control_comparison(
    representation_control_comparison: dict[str, Any],
) -> dict[str, Any]:
    """Guard against treating representation-control comparisons as labels."""
    rows = [
        row
        for row in representation_control_comparison.get("rows", [])
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_proxy_rows = [
        row for row in rows if not row.get("feature_proxy_tokens")
    ]
    missing_heuristic_rows = [
        row for row in rows if not row.get("heuristic_baseline_control")
    ]
    metadata = representation_control_comparison.get("metadata", {})
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_external_representation_control_comparison")
    if countable_rows:
        blockers.append("external_representation_comparison_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_representation_comparison_rows_marked_ready_for_import")
    if missing_proxy_rows:
        blockers.append("external_representation_comparison_rows_missing_proxy_tokens")
    if missing_heuristic_rows:
        blockers.append("external_representation_comparison_rows_missing_heuristic")
    return {
        "metadata": {
            "method": "external_source_representation_control_comparison_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "import_ready_row_count": len(import_ready_rows),
            "missing_proxy_token_row_count": len(missing_proxy_rows),
            "missing_heuristic_control_row_count": len(missing_heuristic_rows),
            "metal_hydrolase_collapse_flag_count": metadata.get(
                "metal_hydrolase_collapse_flag_count", 0
            ),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "representation-control comparison rows are future scoring "
                "diagnostics, not external label decisions"
            )
        ],
    }


def build_external_source_representation_backend_plan(
    *,
    representation_control_manifest: dict[str, Any],
    representation_control_comparison: dict[str, Any],
    sequence_search_export: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Plan real representation-control inputs while keeping embeddings absent."""
    comparison_by_entry = {
        str(row.get("entry_id")): row
        for row in representation_control_comparison.get("rows", []) or []
        if isinstance(row, dict) and row.get("entry_id")
    }
    sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_search_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for manifest_row in representation_control_manifest.get("rows", []) or []:
        if not isinstance(manifest_row, dict) or not manifest_row.get("entry_id"):
            continue
        entry_id = str(manifest_row.get("entry_id"))
        accession = _normalize_accession(manifest_row.get("accession"))
        comparison = comparison_by_entry.get(entry_id, {})
        sequence = sequence_by_accession.get(accession, {})
        readiness_status = _external_representation_backend_status(
            manifest_row=manifest_row,
            comparison=comparison,
            sequence=sequence,
        )
        status_counts[readiness_status] += 1
        rows.append(
            {
                "accession": accession,
                "backend_readiness_status": readiness_status,
                "blockers": _external_representation_backend_blockers(
                    readiness_status
                ),
                "comparison_status": comparison.get("comparison_status"),
                "countable_label_candidate": False,
                "embedding_status": "backend_plan_only_not_computed",
                "entry_id": entry_id,
                "feature_summary": manifest_row.get("feature_summary", {}),
                "heuristic_baseline_control": manifest_row.get(
                    "heuristic_baseline_control", {}
                ),
                "lane_id": manifest_row.get("lane_id"),
                "ready_for_label_import": False,
                "recommended_backends": _external_representation_backend_options(
                    scope_signal=str(manifest_row.get("scope_signal") or ""),
                    comparison_status=str(comparison.get("comparison_status") or ""),
                ),
                "required_inputs": _external_representation_required_inputs(
                    manifest_row=manifest_row,
                    sequence=sequence,
                ),
                "review_status": "representation_backend_plan_review_only",
                "scope_signal": manifest_row.get("scope_signal"),
                "sequence_search_task": sequence.get("search_task"),
            }
        )

    rows = rows[:max_rows]
    return {
        "metadata": {
            "method": "external_source_representation_backend_plan",
            "source_representation_control_method": (
                representation_control_manifest.get("metadata", {}).get("method")
            ),
            "source_representation_comparison_method": (
                representation_control_comparison.get("metadata", {}).get("method")
            ),
            "source_sequence_search_export_method": (
                sequence_search_export.get("metadata", {}).get("method")
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "eligible_control_count": sum(
                1
                for row in representation_control_manifest.get("rows", []) or []
                if isinstance(row, dict)
                and row.get("eligible_for_representation_control")
            ),
            "embedding_status": "backend_plan_only_not_computed",
            "backend_readiness_status_counts": dict(sorted(status_counts.items())),
            "sequence_search_blocked_count": sum(
                1
                for row in rows
                if row["backend_readiness_status"]
                == "blocked_until_sequence_search_complete"
            ),
            "heuristic_contrast_required_count": sum(
                1
                for row in rows
                if "active_site_contrastive_baseline"
                in row.get("recommended_backends", [])
            ),
            "review_only_rule": (
                "representation backend plans define inputs and controls only; "
                "they do not compute embeddings or create labels"
            ),
        },
        "rows": rows,
        "blockers": [
            "external_embeddings_not_computed",
            "representation_backend_not_selected",
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "real representation controls must be evaluated against the "
                "heuristic baseline and sequence-search controls before import"
            )
        ],
    }


def audit_external_source_representation_backend_plan(
    representation_backend_plan: dict[str, Any],
) -> dict[str, Any]:
    """Verify representation backend plans are controls, not labels."""
    rows = [
        row
        for row in representation_backend_plan.get("rows", []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_inputs = [row for row in rows if not row.get("required_inputs")]
    missing_backends = [row for row in rows if not row.get("recommended_backends")]
    missing_review_status = [
        row
        for row in rows
        if row.get("review_status") != "representation_backend_plan_review_only"
    ]
    metadata = representation_backend_plan.get("metadata", {})
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_representation_backend_plan")
    if metadata.get("embedding_status") != "backend_plan_only_not_computed":
        blockers.append("representation_backend_plan_embedding_status_invalid")
    if countable_rows:
        blockers.append("representation_backend_plan_rows_marked_countable")
    if import_ready_rows:
        blockers.append("representation_backend_plan_rows_marked_ready_for_import")
    if missing_inputs:
        blockers.append("representation_backend_plan_rows_missing_required_inputs")
    if missing_backends:
        blockers.append("representation_backend_plan_rows_missing_backend_options")
    if missing_review_status:
        blockers.append("representation_backend_plan_rows_not_review_only")
    return {
        "metadata": {
            "method": "external_source_representation_backend_plan_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "embedding_status": "backend_plan_only_not_computed",
            "import_ready_row_count": len(import_ready_rows),
            "missing_required_input_row_count": len(missing_inputs),
            "missing_backend_option_row_count": len(missing_backends),
            "missing_review_only_status_row_count": len(missing_review_status),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "representation backend plans are no-embedding control plans "
                "and cannot authorize label import"
            )
        ],
    }


def audit_external_source_broad_ec_disambiguation(
    *,
    control_repair_plan: dict[str, Any],
    reaction_evidence_sample: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Narrow broad external EC repair rows to specific reaction-context review."""
    reaction_context_by_entry = _external_reaction_context_by_entry(
        reaction_evidence_sample
    )
    rows: list[dict[str, Any]] = []
    for repair_row in control_repair_plan.get("rows", []) or []:
        if (
            not isinstance(repair_row, dict)
            or repair_row.get("repair_type") != "broad_ec_disambiguation"
        ):
            continue
        accession = str(repair_row.get("accession") or "")
        entry_id = str(repair_row.get("entry_id") or f"uniprot:{accession}")
        context = reaction_context_by_entry.get(
            entry_id, _empty_external_reaction_context(entry_id)
        )
        specific_count = len(context.get("specific_ec_numbers", []))
        if specific_count == 0:
            status = "specific_reaction_context_missing"
        elif specific_count == 1:
            status = "specific_reaction_context_available_for_review"
        else:
            status = "multiple_specific_reactions_need_substrate_selection"
        rows.append(
            {
                "accession": accession,
                "broad_or_incomplete_ec_numbers": list(
                    repair_row.get("broad_or_incomplete_ec_numbers") or []
                ),
                "countable_label_candidate": False,
                "disambiguation_status": status,
                "entry_id": entry_id,
                "lane_id": repair_row.get("lane_id"),
                "protein_name": repair_row.get("protein_name"),
                "reaction_context": context,
                "ready_for_label_import": False,
                "review_status": "broad_ec_disambiguation_review_only",
                "scope_signal": repair_row.get("scope_signal"),
                "specific_ec_numbers_from_repair": list(
                    repair_row.get("specific_ec_numbers") or []
                ),
                "specific_reaction_context_count": specific_count,
            }
        )

    rows = rows[:max_rows]
    status_counts = Counter(str(row["disambiguation_status"]) for row in rows)
    return {
        "metadata": {
            "method": "external_source_broad_ec_disambiguation_audit",
            "source_control_repair_method": control_repair_plan.get("metadata", {}).get(
                "method"
            ),
            "source_reaction_evidence_method": reaction_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "specific_context_available_count": sum(
                1 for row in rows if row["specific_reaction_context_count"] > 0
            ),
            "multiple_specific_context_count": sum(
                1
                for row in rows
                if row["disambiguation_status"]
                == "multiple_specific_reactions_need_substrate_selection"
            ),
            "guardrail_clean": True,
            "disambiguation_status_counts": dict(sorted(status_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "specific_reaction_context_not_active_site_evidence",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "specific reaction context can focus review but cannot replace "
                "active-site evidence or label-factory gates"
            )
        ],
    }


def build_external_source_active_site_gap_source_requests(
    *,
    control_repair_plan: dict[str, Any],
    binding_context_repair_plan: dict[str, Any],
    binding_context_mapping_sample: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Export concrete non-countable sourcing requests for external active-site gaps."""
    binding_repair_by_accession = {
        str(row.get("accession")): row
        for row in binding_context_repair_plan.get("rows", []) or []
        if isinstance(row, dict) and row.get("accession")
    }
    mapped_by_accession = {
        str(row.get("accession")): row
        for row in binding_context_mapping_sample.get("entries", []) or []
        if isinstance(row, dict) and row.get("accession")
    }
    rows: list[dict[str, Any]] = []
    for repair_row in control_repair_plan.get("rows", []) or []:
        if (
            not isinstance(repair_row, dict)
            or repair_row.get("repair_type") != "active_site_feature_gap"
        ):
            continue
        accession = str(repair_row.get("accession") or "")
        binding_repair = binding_repair_by_accession.get(accession, {})
        mapped = mapped_by_accession.get(accession, {})
        binding_position_count = int(
            binding_repair.get("binding_position_count", 0) or 0
        )
        mapped_binding_position_count = int(
            mapped.get("resolved_binding_position_count", 0) or 0
        )
        if mapped_binding_position_count:
            request_status = "binding_context_mapped_ready_for_active_site_sourcing"
        elif binding_position_count:
            request_status = "binding_context_available_needs_structure_mapping"
        elif int(repair_row.get("catalytic_activity_count", 0) or 0) > 0:
            request_status = "reaction_text_only_needs_curated_residue_source"
        else:
            request_status = "defer_until_active_site_or_binding_source_found"
        evidence_refs = _external_binding_evidence_references(binding_repair)
        rows.append(
            {
                "accession": accession,
                "alphafold_ids_sample": repair_row.get("alphafold_ids_sample", []),
                "binding_evidence_reference_count": len(evidence_refs),
                "binding_evidence_references": evidence_refs[:20],
                "binding_position_count": binding_position_count,
                "countable_label_candidate": False,
                "entry_id": f"uniprot:{accession}",
                "lane_id": repair_row.get("lane_id"),
                "mapped_binding_position_count": mapped_binding_position_count,
                "pdb_ids_sample": repair_row.get("pdb_ids_sample", []),
                "protein_name": repair_row.get("protein_name"),
                "ready_for_label_import": False,
                "request_status": request_status,
                "requested_evidence": [
                    "explicit catalytic or active-site residue positions",
                    "residue role annotations for mechanism interpretation",
                    "structure mapping for sourced catalytic positions",
                    "factory-gated decision artifact before any label import",
                ],
                "review_status": "active_site_gap_source_request_review_only",
                "scope_signal": repair_row.get("scope_signal"),
                "specific_ec_numbers": repair_row.get("specific_ec_numbers", []),
            }
        )

    rows = rows[:max_rows]
    status_counts = Counter(str(row["request_status"]) for row in rows)
    return {
        "metadata": {
            "method": "external_source_active_site_gap_source_requests",
            "source_control_repair_method": control_repair_plan.get("metadata", {}).get(
                "method"
            ),
            "source_binding_context_repair_method": binding_context_repair_plan.get(
                "metadata", {}
            ).get("method"),
            "source_binding_context_mapping_method": binding_context_mapping_sample.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "mapped_binding_context_request_count": sum(
                1 for row in rows if row["mapped_binding_position_count"] > 0
            ),
            "binding_context_missing_request_count": sum(
                1 for row in rows if row["binding_position_count"] == 0
            ),
            "request_status_counts": dict(sorted(status_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "active_site_positions_still_missing",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "active-site gap source requests are evidence-collection tasks "
                "and cannot create countable labels"
            )
        ],
    }


def build_external_source_sequence_neighborhood_plan(
    *,
    candidate_manifest: dict[str, Any],
    sequence_holdout_audit: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Prepare non-countable near-duplicate sequence controls for external rows."""
    manifest_by_accession = {
        str(row.get("accession")): row
        for row in candidate_manifest.get("rows", []) or []
        if isinstance(row, dict) and row.get("accession")
    }
    rows: list[dict[str, Any]] = []
    for holdout_row in sequence_holdout_audit.get("rows", []) or []:
        if not isinstance(holdout_row, dict) or not holdout_row.get("accession"):
            continue
        accession = str(holdout_row.get("accession"))
        manifest_row = manifest_by_accession.get(accession, {})
        holdout_status = str(holdout_row.get("holdout_status") or "")
        if holdout_status == "exact_reference_overlap_holdout":
            plan_status = "exact_reference_overlap_keep_as_holdout"
        elif holdout_status == "sequence_failure_set_holdout":
            plan_status = "sequence_failure_set_keep_as_holdout"
        else:
            plan_status = "near_duplicate_search_required_before_import"
        rows.append(
            {
                "accession": accession,
                "countable_label_candidate": False,
                "entry_id": f"uniprot:{accession}",
                "holdout_status": holdout_status,
                "lane_id": holdout_row.get("lane_id") or manifest_row.get("lane_id"),
                "matched_failure_cluster_ids": holdout_row.get(
                    "matched_failure_cluster_ids", []
                ),
                "matched_m_csa_entry_ids": holdout_row.get(
                    "matched_m_csa_entry_ids", []
                ),
                "near_duplicate_search_status": "not_run_request_only",
                "plan_status": plan_status,
                "protein_name": holdout_row.get("protein_name")
                or manifest_row.get("protein_name"),
                "ready_for_label_import": False,
                "requested_controls": [
                    "sequence identity search against countable M-CSA labels",
                    "near-duplicate family-holdout assignment",
                    "source-text leakage check before decision import",
                    "external factory gate after sequence controls are complete",
                ],
                "review_status": "sequence_neighborhood_review_only",
                "scope_signal": holdout_row.get("scope_signal")
                or manifest_row.get("scope_signal"),
                "sequence_cluster_ids": holdout_row.get("sequence_cluster_ids", []),
            }
        )

    rows = rows[:max_rows]
    status_counts = Counter(str(row["plan_status"]) for row in rows)
    return {
        "metadata": {
            "method": "external_source_sequence_neighborhood_plan",
            "source_candidate_manifest_method": candidate_manifest.get(
                "metadata", {}
            ).get("method"),
            "source_sequence_holdout_method": sequence_holdout_audit.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "exact_reference_overlap_holdout_count": sum(
                1
                for row in rows
                if row["plan_status"] == "exact_reference_overlap_keep_as_holdout"
            ),
            "near_duplicate_search_request_count": sum(
                1
                for row in rows
                if row["plan_status"] == "near_duplicate_search_required_before_import"
            ),
            "plan_status_counts": dict(sorted(status_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "near_duplicate_search_not_completed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "sequence-neighborhood plans are OOD controls and cannot create "
                "countable labels"
            )
        ],
    }


def build_external_source_sequence_neighborhood_sample(
    *,
    sequence_neighborhood_plan: dict[str, Any],
    sequence_clusters: dict[str, Any],
    labels: list[dict[str, Any]],
    max_external_rows: int = 30,
    max_reference_sequences: int = 1000,
    top_k: int = 3,
    identity_alert_threshold: float = 0.9,
    coverage_alert_threshold: float = 0.9,
    kmer_alert_threshold: float = 0.85,
    fetcher: Callable[[list[str]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run a bounded sequence-neighborhood control screen for external rows."""
    fetch = fetcher or _fetch_uniprot_sequence_records
    plan_rows = [
        row
        for row in sequence_neighborhood_plan.get("rows", [])
        if isinstance(row, dict) and row.get("accession")
    ][:max_external_rows]
    countable_entry_ids = _countable_label_entry_ids(labels)
    reference_accessions_by_entry: dict[str, list[str]] = {}
    reference_entry_ids_by_accession: dict[str, set[str]] = {}
    for row in sequence_clusters.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id") or "")
        if entry_id not in countable_entry_ids:
            continue
        references = [
            _normalize_accession(accession)
            for accession in row.get("reference_uniprot_ids", []) or []
            if _normalize_accession(accession)
        ]
        if not references:
            continue
        reference_accessions_by_entry[entry_id] = references
        for accession in references:
            reference_entry_ids_by_accession.setdefault(accession, set()).add(entry_id)

    reference_accessions = sorted(reference_entry_ids_by_accession)[:max_reference_sequences]
    external_accessions = sorted(
        {_normalize_accession(row.get("accession")) for row in plan_rows}
    )
    requested_accessions = sorted(set(external_accessions) | set(reference_accessions))
    fetch_failures: list[dict[str, str]] = []
    try:
        sequence_payload = fetch(requested_accessions)
    except Exception as exc:  # pragma: no cover - live network failure path
        sequence_payload = {"metadata": {}, "records": []}
        fetch_failures.append(
            {"error_type": type(exc).__name__, "error": str(exc)}
        )

    records_by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in sequence_payload.get("records", []) or []
        if isinstance(record, dict) and _normalize_accession(record.get("accession"))
    }
    reference_records = [
        records_by_accession[accession]
        for accession in reference_accessions
        if accession in records_by_accession
        and _clean_sequence(records_by_accession[accession].get("sequence"))
    ]

    rows: list[dict[str, Any]] = []
    top_hit_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    high_similarity_count = 0
    exact_holdout_count = 0
    no_hit_count = 0
    missing_external_sequence_count = 0
    for plan_row in plan_rows:
        accession = _normalize_accession(plan_row.get("accession"))
        external_record = records_by_accession.get(accession, {})
        external_sequence = _clean_sequence(external_record.get("sequence"))
        top_matches: list[dict[str, Any]] = []
        if external_sequence:
            for reference_record in reference_records:
                reference_accession = _normalize_accession(
                    reference_record.get("accession")
                )
                if not reference_accession:
                    continue
                match = _sequence_similarity_match(
                    external_accession=accession,
                    external_sequence=external_sequence,
                    reference_accession=reference_accession,
                    reference_sequence=_clean_sequence(
                        reference_record.get("sequence")
                    ),
                    matched_m_csa_entry_ids=sorted(
                        reference_entry_ids_by_accession.get(reference_accession, set())
                    ),
                    identity_alert_threshold=identity_alert_threshold,
                    coverage_alert_threshold=coverage_alert_threshold,
                    kmer_alert_threshold=kmer_alert_threshold,
                )
                if match:
                    top_matches.append(match)
            top_matches.sort(
                key=lambda match: (
                    -float(match.get("near_duplicate_score", 0.0) or 0.0),
                    str(match.get("reference_accession") or ""),
                )
            )
            top_matches = top_matches[:top_k]
        plan_status = str(plan_row.get("plan_status") or "")
        has_alert = any(match.get("near_duplicate_alert") for match in top_matches)
        if plan_status in {
            "exact_reference_overlap_keep_as_holdout",
            "sequence_failure_set_keep_as_holdout",
        }:
            screen_status = "preexisting_sequence_holdout_retained"
            exact_holdout_count += 1
        elif not external_sequence:
            screen_status = "external_sequence_missing"
            missing_external_sequence_count += 1
        elif has_alert:
            screen_status = "near_duplicate_candidate_holdout"
            high_similarity_count += 1
        else:
            screen_status = "no_high_similarity_hit_in_bounded_screen"
            no_hit_count += 1
        status_counts[screen_status] += 1
        row = {
            "accession": accession,
            "countable_label_candidate": False,
            "entry_id": f"uniprot:{accession}",
            "external_sequence_length": len(external_sequence) if external_sequence else 0,
            "holdout_status": plan_row.get("holdout_status"),
            "lane_id": plan_row.get("lane_id"),
            "matched_m_csa_entry_ids": plan_row.get("matched_m_csa_entry_ids", []),
            "near_duplicate_search_status": "bounded_sequence_screen_complete",
            "plan_status": plan_status,
            "protein_name": plan_row.get("protein_name"),
            "ready_for_label_import": False,
            "review_status": "sequence_neighborhood_screen_review_only",
            "scope_signal": plan_row.get("scope_signal"),
            "screen_status": screen_status,
            "sequence_cluster_ids": plan_row.get("sequence_cluster_ids", []),
            "top_matches": top_matches,
        }
        rows.append(row)
        for match in top_matches:
            top_hit_rows.append(
                {
                    "accession": accession,
                    "countable_label_candidate": False,
                    "ready_for_label_import": False,
                    **match,
                }
            )

    return {
        "metadata": {
            "method": "external_source_sequence_neighborhood_sample",
            "source_sequence_neighborhood_plan_method": sequence_neighborhood_plan.get(
                "metadata", {}
            ).get("method"),
            "source_sequence_cluster_method": sequence_clusters.get("metadata", {}).get(
                "method"
            ),
            "source_fetch_method": sequence_payload.get("metadata", {}).get("source"),
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_external_rows": max_external_rows,
            "max_reference_sequences": max_reference_sequences,
            "requested_accession_count": len(requested_accessions),
            "external_sequence_fetched_count": sum(
                1 for accession in external_accessions if accession in records_by_accession
            ),
            "reference_sequence_count": len(reference_records),
            "reference_entry_count": len(reference_accessions_by_entry),
            "top_hit_row_count": len(top_hit_rows),
            "high_similarity_candidate_count": high_similarity_count,
            "exact_or_failure_holdout_count": exact_holdout_count,
            "no_high_similarity_hit_count": no_hit_count,
            "missing_external_sequence_count": missing_external_sequence_count,
            "fetch_failure_count": len(fetch_failures),
            "identity_alert_threshold": identity_alert_threshold,
            "coverage_alert_threshold": coverage_alert_threshold,
            "kmer_alert_threshold": kmer_alert_threshold,
            "screen_status_counts": dict(sorted(status_counts.items())),
            "screen_rule": (
                "bounded unaligned sequence screen for external near-duplicate "
                "risk; this is an OOD control and cannot create labels"
            ),
        },
        "rows": rows,
        "top_hit_rows": top_hit_rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "full_alignment_or_uniref_search_not_completed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "high sequence similarity creates holdout/control debt; absence "
                "of a bounded-screen hit is not evidence for label import"
            )
        ],
    }


def audit_external_source_sequence_neighborhood_sample(
    sequence_neighborhood_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify sequence-neighborhood screens remain non-countable controls."""
    rows = [
        row
        for section in ("rows", "top_hit_rows")
        for row in sequence_neighborhood_sample.get(section, []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_status_rows = [
        row
        for row in sequence_neighborhood_sample.get("rows", []) or []
        if isinstance(row, dict) and not row.get("screen_status")
    ]
    metadata = sequence_neighborhood_sample.get("metadata", {})
    blockers: list[str] = []
    if not sequence_neighborhood_sample.get("rows"):
        blockers.append("empty_sequence_neighborhood_sample")
    if countable_rows:
        blockers.append("sequence_neighborhood_rows_marked_countable")
    if import_ready_rows:
        blockers.append("sequence_neighborhood_rows_marked_ready_for_import")
    if missing_status_rows:
        blockers.append("sequence_neighborhood_rows_missing_screen_status")
    return {
        "metadata": {
            "method": "external_source_sequence_neighborhood_sample_audit",
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": metadata.get("candidate_count", 0),
            "top_hit_row_count": metadata.get("top_hit_row_count", 0),
            "high_similarity_candidate_count": metadata.get(
                "high_similarity_candidate_count", 0
            ),
            "missing_external_sequence_count": metadata.get(
                "missing_external_sequence_count", 0
            ),
            "fetch_failure_count": metadata.get("fetch_failure_count", 0),
            "import_ready_row_count": len(import_ready_rows),
            "missing_status_row_count": len(missing_status_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "sequence-neighborhood screen findings are review-only OOD "
                "controls and cannot authorize external label import"
            )
        ],
    }


def build_external_source_sequence_alignment_verification(
    *,
    sequence_neighborhood_sample: dict[str, Any],
    top_k: int = 3,
    max_pairs: int = 120,
    max_alignment_cells: int = 1_500_000,
    identity_alert_threshold: float = 0.9,
    coverage_alert_threshold: float = 0.9,
    fetcher: Callable[[list[str]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Verify bounded sequence-neighborhood top hits with global edit identity."""
    fetch = fetcher or _fetch_uniprot_sequence_records
    candidate_pairs = _external_sequence_alignment_pairs(
        sequence_neighborhood_sample, top_k=top_k
    )[:max_pairs]
    requested_accessions = sorted(
        {
            accession
            for pair in candidate_pairs
            for accession in (
                _normalize_accession(pair.get("accession")),
                _normalize_accession(pair.get("reference_accession")),
            )
            if accession
        }
    )
    fetch_failures: list[dict[str, str]] = []
    try:
        sequence_payload = fetch(requested_accessions)
    except Exception as exc:  # pragma: no cover - live network failure path
        sequence_payload = {"metadata": {}, "records": []}
        fetch_failures.append(
            {"error_type": type(exc).__name__, "error": str(exc)}
        )
    records_by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in sequence_payload.get("records", []) or []
        if isinstance(record, dict) and _normalize_accession(record.get("accession"))
    }

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    alert_accessions: set[str] = set()
    alert_pair_count = 0
    missing_pair_count = 0
    deferred_pair_count = 0
    for pair in candidate_pairs:
        accession = _normalize_accession(pair.get("accession"))
        reference_accession = _normalize_accession(pair.get("reference_accession"))
        external_sequence = _clean_sequence(
            records_by_accession.get(accession, {}).get("sequence")
        )
        reference_sequence = _clean_sequence(
            records_by_accession.get(reference_accession, {}).get("sequence")
        )
        alignment_identity: float | None = None
        length_coverage = _sequence_length_coverage(external_sequence, reference_sequence)
        alignment_cell_count = len(external_sequence) * len(reference_sequence)
        if not external_sequence or not reference_sequence:
            verification_status = "sequence_missing_for_alignment"
            missing_pair_count += 1
        elif alignment_cell_count > max_alignment_cells:
            verification_status = "alignment_deferred_pair_too_large"
            deferred_pair_count += 1
        else:
            alignment_identity = _sequence_global_edit_identity(
                external_sequence, reference_sequence
            )
            if (
                alignment_identity >= identity_alert_threshold
                and length_coverage >= coverage_alert_threshold
            ):
                verification_status = "alignment_near_duplicate_candidate_holdout"
                alert_accessions.add(accession)
                alert_pair_count += 1
            else:
                verification_status = "alignment_no_near_duplicate_signal"
        status_counts[verification_status] += 1
        rows.append(
            {
                "accession": accession,
                "alignment_cell_count": alignment_cell_count,
                "alignment_identity": (
                    round(alignment_identity, 4)
                    if alignment_identity is not None
                    else None
                ),
                "countable_label_candidate": False,
                "entry_id": f"uniprot:{accession}",
                "external_length": len(external_sequence),
                "length_coverage": round(length_coverage, 4),
                "matched_m_csa_entry_ids": pair.get("matched_m_csa_entry_ids", []),
                "near_duplicate_score": pair.get("near_duplicate_score"),
                "ready_for_label_import": False,
                "reference_accession": reference_accession,
                "reference_length": len(reference_sequence),
                "review_status": "sequence_alignment_verification_review_only",
                "screen_near_duplicate_alert": bool(
                    pair.get("near_duplicate_alert")
                ),
                "verification_status": verification_status,
            }
        )

    return {
        "metadata": {
            "method": "external_source_sequence_alignment_verification",
            "source_sequence_neighborhood_sample_method": (
                sequence_neighborhood_sample.get("metadata", {}).get("method")
            ),
            "source_fetch_method": sequence_payload.get("metadata", {}).get("source"),
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": 0,
            "candidate_count": len({row["accession"] for row in rows}),
            "verified_pair_count": len(rows),
            "max_pairs": max_pairs,
            "top_k": top_k,
            "requested_accession_count": len(requested_accessions),
            "fetched_accession_count": len(records_by_accession),
            "alignment_alert_candidate_count": len(alert_accessions),
            "alignment_alert_pair_count": alert_pair_count,
            "missing_sequence_pair_count": missing_pair_count,
            "alignment_deferred_pair_count": deferred_pair_count,
            "fetch_failure_count": len(fetch_failures),
            "identity_alert_threshold": identity_alert_threshold,
            "coverage_alert_threshold": coverage_alert_threshold,
            "max_alignment_cells": max_alignment_cells,
            "verification_status_counts": dict(sorted(status_counts.items())),
            "verification_rule": (
                "bounded top-hit global edit-identity verification for "
                "sequence-neighborhood controls; it is not a complete UniRef "
                "or all-vs-all search and cannot create labels"
            ),
        },
        "rows": rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "complete_near_duplicate_reference_search_not_completed",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "alignment verification is a bounded review-only control; "
                "external candidates still require full sequence controls "
                "before any import decision"
            )
        ],
    }


def audit_external_source_sequence_alignment_verification(
    sequence_alignment_verification: dict[str, Any],
) -> dict[str, Any]:
    """Guard bounded alignment verification against label import use."""
    rows = [
        row
        for row in sequence_alignment_verification.get("rows", []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_status_rows = [row for row in rows if not row.get("verification_status")]
    metadata = sequence_alignment_verification.get("metadata", {})
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_sequence_alignment_verification")
    if countable_rows:
        blockers.append("sequence_alignment_rows_marked_countable")
    if import_ready_rows:
        blockers.append("sequence_alignment_rows_marked_ready_for_import")
    if missing_status_rows:
        blockers.append("sequence_alignment_rows_missing_status")
    if metadata.get("complete_near_duplicate_search_required") is not True:
        blockers.append("sequence_alignment_complete_search_flag_missing")
    return {
        "metadata": {
            "method": "external_source_sequence_alignment_verification_audit",
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": metadata.get("candidate_count", 0),
            "verified_pair_count": metadata.get("verified_pair_count", 0),
            "alignment_alert_candidate_count": metadata.get(
                "alignment_alert_candidate_count", 0
            ),
            "missing_sequence_pair_count": metadata.get(
                "missing_sequence_pair_count", 0
            ),
            "alignment_deferred_pair_count": metadata.get(
                "alignment_deferred_pair_count", 0
            ),
            "import_ready_row_count": len(import_ready_rows),
            "missing_status_row_count": len(missing_status_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "sequence alignment verification is review-only and cannot "
                "authorize external label import"
            )
        ],
    }


def build_external_source_sequence_search_export(
    *,
    sequence_neighborhood_plan: dict[str, Any],
    sequence_neighborhood_sample: dict[str, Any],
    sequence_alignment_verification: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Export complete near-duplicate sequence-search tasks as review-only work."""
    sample_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_neighborhood_sample.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    alignment_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in sequence_alignment_verification.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            alignment_by_accession.setdefault(accession, []).append(row)

    rows: list[dict[str, Any]] = []
    search_task_counts: Counter[str] = Counter()
    for plan_row in sequence_neighborhood_plan.get("rows", []) or []:
        if not isinstance(plan_row, dict):
            continue
        accession = _normalize_accession(plan_row.get("accession"))
        if not accession:
            continue
        sample_row = sample_by_accession.get(accession, {})
        alignment_rows = alignment_by_accession.get(accession, [])
        alignment_status = _external_sequence_alignment_status(alignment_rows)
        search_task = _external_sequence_search_task(
            plan_status=str(plan_row.get("plan_status") or ""),
            screen_status=str(sample_row.get("screen_status") or ""),
            alignment_status=alignment_status,
        )
        search_task_counts[search_task] += 1
        top_matches = list(sample_row.get("top_matches") or [])[:10]
        rows.append(
            {
                "accession": accession,
                "alignment_status": alignment_status,
                "blockers": _external_sequence_search_export_blockers(search_task),
                "countable_label_candidate": False,
                "decision": {
                    "decision_status": "no_decision",
                    "reviewer": "",
                    "reviewed_at": "",
                    "sequence_search_result": "",
                    "rationale": "",
                },
                "entry_id": plan_row.get("entry_id") or f"uniprot:{accession}",
                "holdout_status": plan_row.get("holdout_status"),
                "lane_id": plan_row.get("lane_id"),
                "matched_m_csa_entry_ids": plan_row.get("matched_m_csa_entry_ids", []),
                "plan_status": plan_row.get("plan_status"),
                "protein_name": plan_row.get("protein_name"),
                "ready_for_label_import": False,
                "review_status": "sequence_search_export_review_only",
                "scope_signal": plan_row.get("scope_signal"),
                "screen_status": sample_row.get("screen_status"),
                "search_task": search_task,
                "source_targets": _external_sequence_search_source_targets(
                    accession=accession,
                    top_matches=top_matches,
                ),
                "top_matches": top_matches,
            }
        )

    rows = rows[:max_rows]
    return {
        "metadata": {
            "method": "external_source_sequence_search_export",
            "source_sequence_neighborhood_plan_method": (
                sequence_neighborhood_plan.get("metadata", {}).get("method")
            ),
            "source_sequence_neighborhood_sample_method": (
                sequence_neighborhood_sample.get("metadata", {}).get("method")
            ),
            "source_sequence_alignment_method": (
                sequence_alignment_verification.get("metadata", {}).get("method")
            ),
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "decision_status_counts": {"no_decision": len(rows)},
            "search_task_counts": dict(sorted(search_task_counts.items())),
            "near_duplicate_search_request_count": sum(
                1
                for row in rows
                if row["search_task"]
                == "run_complete_uniref_or_all_vs_all_near_duplicate_search"
            ),
            "sequence_holdout_task_count": sum(
                1
                for row in rows
                if row["search_task"] == "keep_sequence_holdout_control"
            ),
            "source_target_count": sum(
                len(row.get("source_targets", []) or []) for row in rows
            ),
            "review_only_rule": (
                "sequence-search exports are OOD control worklists and cannot "
                "create countable labels or import-ready rows"
            ),
        },
        "rows": rows,
        "blockers": [
            "complete_near_duplicate_reference_search_not_completed",
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "bounded sequence screens and top-hit alignments are not a "
                "complete near-duplicate search; keep external rows non-countable"
            )
        ],
    }


def audit_external_source_sequence_search_export(
    *,
    sequence_search_export: dict[str, Any],
    sequence_neighborhood_plan: dict[str, Any],
) -> dict[str, Any]:
    """Verify complete sequence-search exports remain review-only worklists."""
    rows = [
        row
        for row in sequence_search_export.get("rows", []) or []
        if isinstance(row, dict)
    ]
    expected_candidate_count = int(
        sequence_neighborhood_plan.get("metadata", {}).get("candidate_count", 0)
        or 0
    )
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_targets = [row for row in rows if not row.get("source_targets")]
    missing_task = [row for row in rows if not row.get("search_task")]
    completed_decisions = [
        row
        for row in rows
        if (row.get("decision") or {}).get("decision_status") != "no_decision"
    ]
    missing_review_status = [
        row
        for row in rows
        if row.get("review_status") != "sequence_search_export_review_only"
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_sequence_search_export")
    if expected_candidate_count and len(rows) != expected_candidate_count:
        blockers.append("sequence_search_export_missing_plan_rows")
    if countable_rows:
        blockers.append("sequence_search_export_rows_marked_countable")
    if import_ready_rows:
        blockers.append("sequence_search_export_rows_marked_ready_for_import")
    if missing_targets:
        blockers.append("sequence_search_export_rows_missing_source_targets")
    if missing_task:
        blockers.append("sequence_search_export_rows_missing_search_task")
    if completed_decisions:
        blockers.append("sequence_search_export_contains_completed_decisions")
    if missing_review_status:
        blockers.append("sequence_search_export_rows_not_review_only")
    return {
        "metadata": {
            "method": "external_source_sequence_search_export_audit",
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_plan_candidate_count": expected_candidate_count,
            "import_ready_row_count": len(import_ready_rows),
            "missing_source_target_row_count": len(missing_targets),
            "missing_search_task_row_count": len(missing_task),
            "completed_decision_count": len(completed_decisions),
            "missing_review_only_status_row_count": len(missing_review_status),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "sequence-search exports are no-decision OOD control packets "
                "and must not be used as countable label registries"
            )
        ],
    }


def build_external_source_active_site_sourcing_queue(
    *,
    active_site_gap_source_requests: dict[str, Any],
    external_import_readiness_audit: dict[str, Any],
    sequence_alignment_verification: dict[str, Any] | None = None,
    max_rows: int = 100,
) -> dict[str, Any]:
    """Prioritize review-only active-site sourcing for external gap rows."""
    readiness_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in external_import_readiness_audit.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    alignment_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in (sequence_alignment_verification or {}).get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            alignment_by_accession.setdefault(accession, []).append(row)

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for request in active_site_gap_source_requests.get("rows", []) or []:
        if not isinstance(request, dict):
            continue
        accession = _normalize_accession(request.get("accession"))
        if not accession:
            continue
        request_status = str(request.get("request_status") or "")
        readiness = readiness_by_accession.get(accession, {})
        alignment_status = _external_sequence_alignment_status(
            alignment_by_accession.get(accession)
        )
        queue_status = _external_active_site_sourcing_queue_status(
            request_status=request_status,
            readiness_status=str(readiness.get("readiness_status") or ""),
            alignment_status=alignment_status,
        )
        status_counts[queue_status] += 1
        rows.append(
            {
                "accession": accession,
                "active_site_gap_request_status": request_status,
                "binding_evidence_reference_count": request.get(
                    "binding_evidence_reference_count", 0
                ),
                "countable_label_candidate": False,
                "entry_id": f"uniprot:{accession}",
                "lane_id": request.get("lane_id"),
                "mapped_binding_position_count": request.get(
                    "mapped_binding_position_count", 0
                ),
                "next_action": _external_active_site_sourcing_next_action(
                    queue_status
                ),
                "priority_score": _external_active_site_sourcing_priority_score(
                    queue_status=queue_status,
                    mapped_binding_position_count=int(
                        request.get("mapped_binding_position_count", 0) or 0
                    ),
                    binding_evidence_reference_count=int(
                        request.get("binding_evidence_reference_count", 0) or 0
                    ),
                ),
                "protein_name": request.get("protein_name"),
                "queue_status": queue_status,
                "ready_for_label_import": False,
                "readiness_status": readiness.get("readiness_status"),
                "requested_evidence": request.get("requested_evidence", []),
                "review_status": "active_site_sourcing_queue_review_only",
                "scope_signal": request.get("scope_signal"),
                "sequence_alignment_status": alignment_status,
                "specific_ec_numbers": request.get("specific_ec_numbers", []),
            }
        )

    rows.sort(
        key=lambda row: (
            -float(row.get("priority_score", 0.0) or 0.0),
            str(row.get("accession") or ""),
        )
    )
    rows = rows[:max_rows]
    status_counts = Counter(str(row["queue_status"]) for row in rows)
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_queue",
            "source_active_site_gap_request_method": (
                active_site_gap_source_requests.get("metadata", {}).get("method")
            ),
            "source_import_readiness_method": external_import_readiness_audit.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "ready_sourcing_candidate_count": sum(
                1
                for row in rows
                if row["queue_status"] == "ready_for_curated_active_site_sourcing"
            ),
            "text_source_candidate_count": sum(
                1
                for row in rows
                if row["queue_status"] == "needs_primary_active_site_source"
            ),
            "sequence_holdout_deferred_count": sum(
                1
                for row in rows
                if row["queue_status"] == "defer_sequence_holdout_before_sourcing"
            ),
            "queue_status_counts": dict(sorted(status_counts.items())),
        },
        "rows": rows,
        "blockers": [
            "explicit_active_site_residue_sources_not_collected",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "active-site sourcing queues are evidence-collection worklists "
                "and cannot create countable labels"
            )
        ],
    }


def audit_external_source_active_site_sourcing_queue(
    *,
    active_site_sourcing_queue: dict[str, Any],
    external_import_readiness_audit: dict[str, Any],
) -> dict[str, Any]:
    """Verify active-site sourcing queues cover gap rows without labels."""
    rows = [
        row
        for row in active_site_sourcing_queue.get("rows", []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_status_rows = [row for row in rows if not row.get("queue_status")]
    active_site_gap_count = int(
        external_import_readiness_audit.get("metadata", {}).get(
            "active_site_gap_count", 0
        )
        or 0
    )
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_active_site_sourcing_queue")
    if countable_rows:
        blockers.append("active_site_sourcing_rows_marked_countable")
    if import_ready_rows:
        blockers.append("active_site_sourcing_rows_marked_ready_for_import")
    if missing_status_rows:
        blockers.append("active_site_sourcing_rows_missing_status")
    if active_site_gap_count and len(rows) != active_site_gap_count:
        blockers.append("active_site_sourcing_queue_missing_gap_rows")
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_queue_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_active_site_gap_count": active_site_gap_count,
            "import_ready_row_count": len(import_ready_rows),
            "missing_status_row_count": len(missing_status_rows),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "active-site sourcing queues are review-only worklists and "
                "cannot authorize external label import"
            )
        ],
    }


def build_external_source_active_site_sourcing_export(
    *,
    active_site_sourcing_queue: dict[str, Any],
    active_site_gap_source_requests: dict[str, Any],
    active_site_evidence_sample: dict[str, Any],
    reaction_evidence_sample: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Build a review-only packet for sourcing external active-site residues."""
    request_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_gap_source_requests.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    summary_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_evidence_sample.get("candidate_summaries", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    binding_rows_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in active_site_evidence_sample.get("rows", []) or []:
        if not isinstance(row, dict) or row.get("feature_type") != "Binding site":
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            binding_rows_by_accession.setdefault(accession, []).append(row)
    reaction_context_by_entry = _external_reaction_context_by_entry(
        reaction_evidence_sample
    )

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    source_task_counts: Counter[str] = Counter()
    for queue_row in active_site_sourcing_queue.get("rows", []) or []:
        if not isinstance(queue_row, dict):
            continue
        accession = _normalize_accession(queue_row.get("accession"))
        if not accession:
            continue
        request = request_by_accession.get(accession, {})
        summary = summary_by_accession.get(accession, {})
        entry_id = str(queue_row.get("entry_id") or f"uniprot:{accession}")
        binding_rows = binding_rows_by_accession.get(accession, [])
        reaction_context = reaction_context_by_entry.get(
            entry_id, _empty_external_reaction_context(entry_id)
        )
        source_task = _external_active_site_sourcing_task(
            str(queue_row.get("queue_status") or "")
        )
        status_counts[str(queue_row.get("queue_status") or "unknown")] += 1
        source_task_counts[source_task] += 1
        evidence_refs = list(request.get("binding_evidence_references") or [])
        rows.append(
            {
                "accession": accession,
                "active_site_gap_request_status": request.get("request_status")
                or queue_row.get("active_site_gap_request_status"),
                "binding_context": {
                    "binding_feature_count": len(binding_rows),
                    "binding_positions": _external_binding_feature_positions(
                        binding_rows
                    )[:25],
                    "evidence_references": evidence_refs[:25],
                    "mapped_binding_position_count": queue_row.get(
                        "mapped_binding_position_count", 0
                    ),
                },
                "blockers": _external_active_site_sourcing_export_blockers(
                    str(queue_row.get("queue_status") or "")
                ),
                "countable_label_candidate": False,
                "decision": {
                    "decision_status": "no_decision",
                    "reviewer": "",
                    "reviewed_at": "",
                    "sourced_active_site_positions": [],
                    "rationale": "",
                },
                "entry_id": entry_id,
                "lane_id": queue_row.get("lane_id"),
                "priority_score": queue_row.get("priority_score"),
                "protein_name": queue_row.get("protein_name"),
                "queue_status": queue_row.get("queue_status"),
                "reaction_context": reaction_context,
                "ready_for_label_import": False,
                "review_status": "active_site_sourcing_export_review_only",
                "scope_signal": queue_row.get("scope_signal"),
                "sequence_alignment_status": queue_row.get(
                    "sequence_alignment_status"
                ),
                "source_task": source_task,
                "source_targets": _external_active_site_source_targets(
                    accession=accession,
                    summary=summary,
                    request=request,
                    reaction_context=reaction_context,
                ),
                "specific_ec_numbers": queue_row.get("specific_ec_numbers", []),
            }
        )

    rows = rows[:max_rows]
    target_count = sum(len(row.get("source_targets", []) or []) for row in rows)
    evidence_reference_count = sum(
        len(row.get("binding_context", {}).get("evidence_references", []) or [])
        for row in rows
    )
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_export",
            "source_active_site_sourcing_method": active_site_sourcing_queue.get(
                "metadata", {}
            ).get("method"),
            "source_active_site_gap_request_method": (
                active_site_gap_source_requests.get("metadata", {}).get("method")
            ),
            "source_active_site_evidence_method": active_site_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "source_reaction_evidence_method": reaction_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "decision_status_counts": {"no_decision": len(rows)},
            "source_task_counts": dict(sorted(source_task_counts.items())),
            "queue_status_counts": dict(sorted(status_counts.items())),
            "source_target_count": target_count,
            "binding_evidence_reference_count": evidence_reference_count,
            "review_only_rule": (
                "active-site sourcing exports are expert/source-review packets; "
                "they cannot create countable labels or import-ready rows"
            ),
        },
        "rows": rows,
        "blockers": [
            "explicit_active_site_residue_sources_not_collected",
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "sourced positions must be imported through a separate reviewed "
                "decision artifact and full label-factory gate before any label counts"
            )
        ],
    }


def audit_external_source_active_site_sourcing_export(
    *,
    active_site_sourcing_export: dict[str, Any],
    active_site_sourcing_queue: dict[str, Any],
) -> dict[str, Any]:
    """Verify active-site sourcing exports are complete, review-only packets."""
    rows = [
        row
        for row in active_site_sourcing_export.get("rows", []) or []
        if isinstance(row, dict)
    ]
    queue_candidate_count = int(
        active_site_sourcing_queue.get("metadata", {}).get("candidate_count", 0)
        or 0
    )
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_targets = [row for row in rows if not row.get("source_targets")]
    missing_task = [row for row in rows if not row.get("source_task")]
    completed_decisions = [
        row
        for row in rows
        if (row.get("decision") or {}).get("decision_status") != "no_decision"
    ]
    missing_review_status = [
        row
        for row in rows
        if row.get("review_status") != "active_site_sourcing_export_review_only"
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_active_site_sourcing_export")
    if queue_candidate_count and len(rows) != queue_candidate_count:
        blockers.append("active_site_sourcing_export_missing_queue_rows")
    if countable_rows:
        blockers.append("active_site_sourcing_export_rows_marked_countable")
    if import_ready_rows:
        blockers.append("active_site_sourcing_export_rows_marked_ready_for_import")
    if missing_targets:
        blockers.append("active_site_sourcing_export_rows_missing_source_targets")
    if missing_task:
        blockers.append("active_site_sourcing_export_rows_missing_source_task")
    if completed_decisions:
        blockers.append("active_site_sourcing_export_contains_completed_decisions")
    if missing_review_status:
        blockers.append("active_site_sourcing_export_rows_not_review_only")
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_export_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_queue_candidate_count": queue_candidate_count,
            "import_ready_row_count": len(import_ready_rows),
            "missing_source_target_row_count": len(missing_targets),
            "missing_source_task_row_count": len(missing_task),
            "completed_decision_count": len(completed_decisions),
            "missing_review_only_status_row_count": len(missing_review_status),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "active-site sourcing exports are no-decision work packets and "
                "must not be used as countable label registries"
            )
        ],
    }


def audit_external_source_import_readiness(
    *,
    candidate_manifest: dict[str, Any],
    active_site_evidence_sample: dict[str, Any],
    heuristic_control_scores: dict[str, Any],
    representation_control_comparison: dict[str, Any],
    active_site_gap_source_requests: dict[str, Any],
    sequence_neighborhood_sample: dict[str, Any],
    sequence_alignment_verification: dict[str, Any] | None = None,
    max_rows: int = 100,
) -> dict[str, Any]:
    """Summarize remaining external import blockers by candidate."""
    active_site_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_evidence_sample.get("candidate_summaries", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    heuristic_by_accession = {
        _normalize_accession(str(row.get("entry_id") or "").removeprefix("uniprot:")): row
        for row in heuristic_control_scores.get("results", []) or []
        if isinstance(row, dict)
        and _normalize_accession(str(row.get("entry_id") or "").removeprefix("uniprot:"))
    }
    representation_by_accession = {
        _normalize_accession(str(row.get("entry_id") or "").removeprefix("uniprot:")): row
        for row in representation_control_comparison.get("rows", []) or []
        if isinstance(row, dict)
        and _normalize_accession(str(row.get("entry_id") or "").removeprefix("uniprot:"))
    }
    active_site_gap_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_gap_source_requests.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_neighborhood_sample.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    sequence_alignment_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in (sequence_alignment_verification or {}).get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            sequence_alignment_by_accession.setdefault(accession, []).append(row)
    rows: list[dict[str, Any]] = []
    blocker_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for manifest_row in candidate_manifest.get("rows", []) or []:
        if not isinstance(manifest_row, dict):
            continue
        accession = _normalize_accession(manifest_row.get("accession"))
        if not accession:
            continue
        active_site = active_site_by_accession.get(accession)
        heuristic = heuristic_by_accession.get(accession)
        representation = representation_by_accession.get(accession)
        active_site_gap = active_site_gap_by_accession.get(accession)
        sequence = sequence_by_accession.get(accession)
        sequence_alignment = sequence_alignment_by_accession.get(accession)
        blockers = _external_import_readiness_blockers(
            manifest_row=manifest_row,
            active_site=active_site,
            heuristic=heuristic,
            representation=representation,
            active_site_gap=active_site_gap,
            sequence=sequence,
            sequence_alignment=sequence_alignment,
        )
        blocker_counts.update(blockers)
        readiness_status = _external_import_readiness_status(blockers)
        status_counts[readiness_status] += 1
        rows.append(
            {
                "accession": accession,
                "active_site_feature_count": (
                    active_site.get("active_site_feature_count") if active_site else 0
                ),
                "blockers": blockers,
                "countable_label_candidate": False,
                "entry_id": f"uniprot:{accession}",
                "heuristic_top1_fingerprint": _external_top1_fingerprint(
                    heuristic or {}
                ),
                "lane_id": manifest_row.get("lane_id"),
                "next_action": _external_import_readiness_next_action(blockers),
                "protein_name": manifest_row.get("protein_name"),
                "ready_for_label_import": False,
                "readiness_status": readiness_status,
                "representation_status": (
                    representation.get("comparison_status") if representation else None
                ),
                "review_status": "external_import_readiness_review_only",
                "scope_signal": manifest_row.get("scope_signal"),
                "sequence_screen_status": (
                    sequence.get("screen_status") if sequence else None
                ),
                "sequence_alignment_status": _external_sequence_alignment_status(
                    sequence_alignment
                ),
            }
        )

    rows = rows[:max_rows]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_external_import_readiness_audit")
    if countable_rows:
        blockers.append("external_import_readiness_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_import_readiness_rows_marked_ready_for_import")
    return {
        "metadata": {
            "method": "external_source_import_readiness_audit",
            "source_candidate_manifest_method": candidate_manifest.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "guardrail_clean": not blockers,
            "countable_label_candidate_count": len(countable_rows),
            "label_import_ready_count": len(import_ready_rows),
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "active_site_gap_count": blocker_counts.get(
                "external_active_site_feature_gap", 0
            ),
            "sequence_holdout_or_search_count": sum(
                1
                for row in rows
                if any(
                    blocker in row["blockers"]
                    for blocker in (
                        "exact_sequence_holdout",
                        "near_duplicate_candidate_holdout",
                        "sequence_alignment_near_duplicate_candidate_holdout",
                        "complete_near_duplicate_search_required",
                    )
                )
            ),
            "sequence_alignment_alert_count": blocker_counts.get(
                "sequence_alignment_near_duplicate_candidate_holdout", 0
            ),
            "sequence_alignment_incomplete_count": blocker_counts.get(
                "sequence_alignment_verification_incomplete", 0
            ),
            "heuristic_scope_mismatch_count": blocker_counts.get(
                "heuristic_scope_top1_mismatch", 0
            ),
            "representation_control_issue_count": sum(
                count
                for blocker, count in blocker_counts.items()
                if blocker.startswith("representation_control_")
            ),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "readiness_status_counts": dict(sorted(status_counts.items())),
            "readiness_rule": (
                "external candidates remain non-countable until active-site, "
                "sequence, heuristic, representation, review-decision, and "
                "label-factory gates all pass"
            ),
        },
        "rows": rows,
        "blockers": blockers,
        "warnings": [
            (
                "import-readiness audits prioritize external review work and "
                "must not be used as label registries"
            )
        ],
    }


def build_external_source_transfer_blocker_matrix(
    *,
    candidate_manifest: dict[str, Any],
    external_import_readiness_audit: dict[str, Any],
    active_site_sourcing_export: dict[str, Any],
    sequence_search_export: dict[str, Any],
    representation_backend_plan: dict[str, Any],
    max_rows: int = 100,
) -> dict[str, Any]:
    """Join external blocker packets into a candidate-level review matrix."""
    readiness_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in external_import_readiness_audit.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    active_site_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_sourcing_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_search_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    backend_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in representation_backend_plan.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }

    rows: list[dict[str, Any]] = []
    for manifest_row in candidate_manifest.get("rows", []) or []:
        if not isinstance(manifest_row, dict):
            continue
        accession = _normalize_accession(manifest_row.get("accession"))
        if not accession:
            continue
        readiness = readiness_by_accession.get(accession, {})
        active_site = active_site_by_accession.get(accession)
        sequence = sequence_by_accession.get(accession)
        backend = backend_by_accession.get(accession)
        blockers = _external_transfer_blocker_matrix_blockers(
            readiness=readiness,
            active_site=active_site,
            sequence=sequence,
            backend=backend,
        )
        prioritized_action = _external_transfer_blocker_matrix_next_action(
            readiness=readiness,
            active_site=active_site,
            sequence=sequence,
            backend=backend,
        )
        rows.append(
            {
                "accession": accession,
                "active_site_sourcing": _external_transfer_blocker_matrix_active_site(
                    active_site
                ),
                "blockers": blockers,
                "countable_label_candidate": False,
                "entry_id": manifest_row.get("entry_id") or f"uniprot:{accession}",
                "lane_id": manifest_row.get("lane_id"),
                "prioritized_action": prioritized_action,
                "protein_name": manifest_row.get("protein_name"),
                "ready_for_label_import": False,
                "readiness_status": readiness.get("readiness_status"),
                "representation_backend": (
                    _external_transfer_blocker_matrix_backend(backend)
                ),
                "review_status": "external_transfer_blocker_matrix_review_only",
                "scope_signal": manifest_row.get("scope_signal"),
                "sequence_search": _external_transfer_blocker_matrix_sequence(
                    sequence
                ),
            }
        )

    rows = rows[:max_rows]
    blocker_counts = Counter(
        blocker for row in rows for blocker in row.get("blockers", []) or []
    )
    lane_counts = Counter(str(row.get("lane_id") or "unknown") for row in rows)
    prioritized_action_counts = Counter(
        str(row.get("prioritized_action") or "unknown") for row in rows
    )
    dominant_action_count = max(prioritized_action_counts.values(), default=0)
    dominant_lane_count = max(lane_counts.values(), default=0)
    return {
        "metadata": {
            "method": "external_source_transfer_blocker_matrix",
            "source_candidate_manifest_method": candidate_manifest.get(
                "metadata", {}
            ).get("method"),
            "source_import_readiness_method": external_import_readiness_audit.get(
                "metadata", {}
            ).get("method"),
            "source_active_site_sourcing_method": active_site_sourcing_export.get(
                "metadata", {}
            ).get("method"),
            "source_sequence_search_method": sequence_search_export.get(
                "metadata", {}
            ).get("method"),
            "source_representation_backend_method": representation_backend_plan.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "active_site_sourcing_export_candidate_count": len(
                active_site_by_accession
            ),
            "sequence_search_export_candidate_count": len(sequence_by_accession),
            "representation_backend_plan_candidate_count": len(backend_by_accession),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "dominant_lane_fraction": (
                round(dominant_lane_count / len(rows), 4) if rows else 0.0
            ),
            "dominant_prioritized_action_fraction": (
                round(dominant_action_count / len(rows), 4) if rows else 0.0
            ),
            "lane_counts": dict(sorted(lane_counts.items())),
            "prioritized_action_counts": dict(sorted(prioritized_action_counts.items())),
            "review_only_rule": (
                "blocker matrices join review packets into a worklist only; "
                "they cannot create countable labels or import-ready rows"
            ),
        },
        "rows": rows,
        "blockers": [
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "the blocker matrix is a coordination artifact; complete source, "
                "sequence, representation, decision, and factory gates remain required"
            )
        ],
    }


def audit_external_source_transfer_blocker_matrix(
    *,
    transfer_blocker_matrix: dict[str, Any],
    candidate_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Verify the external blocker matrix is complete and non-countable."""
    rows = [
        row
        for row in transfer_blocker_matrix.get("rows", []) or []
        if isinstance(row, dict)
    ]
    expected_candidate_count = int(
        candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0
    )
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_blocker_rows = [row for row in rows if not row.get("blockers")]
    missing_review_status_rows = [
        row
        for row in rows
        if row.get("review_status") != "external_transfer_blocker_matrix_review_only"
    ]
    missing_sequence_rows = [
        row
        for row in rows
        if not row.get("sequence_search", {}).get("search_task")
    ]
    missing_action_rows = [row for row in rows if not row.get("prioritized_action")]
    completed_active_site_decisions = [
        row
        for row in rows
        if row.get("active_site_sourcing", {}).get("decision_status")
        not in (None, "no_decision")
    ]
    completed_sequence_decisions = [
        row
        for row in rows
        if row.get("sequence_search", {}).get("decision_status") != "no_decision"
    ]
    blockers: list[str] = []
    metadata = transfer_blocker_matrix.get("metadata", {})
    if not rows:
        blockers.append("empty_external_transfer_blocker_matrix")
    if expected_candidate_count and len(rows) != expected_candidate_count:
        blockers.append("external_transfer_blocker_matrix_missing_candidates")
    if countable_rows:
        blockers.append("external_transfer_blocker_matrix_rows_marked_countable")
    if import_ready_rows:
        blockers.append("external_transfer_blocker_matrix_rows_marked_ready_for_import")
    if missing_blocker_rows:
        blockers.append("external_transfer_blocker_matrix_rows_missing_blockers")
    if missing_review_status_rows:
        blockers.append("external_transfer_blocker_matrix_rows_not_review_only")
    if missing_sequence_rows:
        blockers.append("external_transfer_blocker_matrix_rows_missing_sequence_task")
    if missing_action_rows:
        blockers.append("external_transfer_blocker_matrix_rows_missing_next_action")
    if (
        len(rows) >= 5
        and float(metadata.get("dominant_prioritized_action_fraction", 0.0) or 0.0)
        > 0.8
    ):
        blockers.append("external_transfer_blocker_matrix_action_queue_collapsed")
    if (
        len(rows) >= 5
        and float(metadata.get("dominant_lane_fraction", 0.0) or 0.0) > 0.8
    ):
        blockers.append("external_transfer_blocker_matrix_lane_queue_collapsed")
    if completed_active_site_decisions:
        blockers.append("external_transfer_blocker_matrix_active_site_decisions_present")
    if completed_sequence_decisions:
        blockers.append("external_transfer_blocker_matrix_sequence_decisions_present")
    return {
        "metadata": {
            "method": "external_source_transfer_blocker_matrix_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_candidate_count": expected_candidate_count,
            "import_ready_row_count": len(import_ready_rows),
            "missing_blocker_row_count": len(missing_blocker_rows),
            "missing_review_only_status_row_count": len(missing_review_status_rows),
            "missing_sequence_task_row_count": len(missing_sequence_rows),
            "missing_prioritized_action_row_count": len(missing_action_rows),
            "dominant_prioritized_action_fraction": metadata.get(
                "dominant_prioritized_action_fraction", 0.0
            ),
            "dominant_lane_fraction": metadata.get("dominant_lane_fraction", 0.0),
            "completed_active_site_decision_count": len(
                completed_active_site_decisions
            ),
            "completed_sequence_decision_count": len(completed_sequence_decisions),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "external transfer blocker matrices are review-only worklists "
                "and cannot authorize external label import"
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
    external_control_repair_plan: dict[str, Any] | None = None,
    external_control_repair_plan_audit: dict[str, Any] | None = None,
    reaction_evidence_sample: dict[str, Any] | None = None,
    reaction_evidence_sample_audit: dict[str, Any] | None = None,
    representation_control_manifest: dict[str, Any] | None = None,
    representation_control_manifest_audit: dict[str, Any] | None = None,
    representation_control_comparison: dict[str, Any] | None = None,
    representation_control_comparison_audit: dict[str, Any] | None = None,
    representation_backend_plan: dict[str, Any] | None = None,
    representation_backend_plan_audit: dict[str, Any] | None = None,
    broad_ec_disambiguation_audit: dict[str, Any] | None = None,
    active_site_gap_source_requests: dict[str, Any] | None = None,
    sequence_neighborhood_plan: dict[str, Any] | None = None,
    sequence_neighborhood_sample: dict[str, Any] | None = None,
    sequence_neighborhood_sample_audit: dict[str, Any] | None = None,
    sequence_alignment_verification: dict[str, Any] | None = None,
    sequence_alignment_verification_audit: dict[str, Any] | None = None,
    sequence_search_export: dict[str, Any] | None = None,
    sequence_search_export_audit: dict[str, Any] | None = None,
    external_import_readiness_audit: dict[str, Any] | None = None,
    active_site_sourcing_queue: dict[str, Any] | None = None,
    active_site_sourcing_queue_audit: dict[str, Any] | None = None,
    active_site_sourcing_export: dict[str, Any] | None = None,
    active_site_sourcing_export_audit: dict[str, Any] | None = None,
    transfer_blocker_matrix: dict[str, Any] | None = None,
    transfer_blocker_matrix_audit: dict[str, Any] | None = None,
    binding_context_repair_plan: dict[str, Any] | None = None,
    binding_context_repair_plan_audit: dict[str, Any] | None = None,
    binding_context_mapping_sample: dict[str, Any] | None = None,
    binding_context_mapping_sample_audit: dict[str, Any] | None = None,
    sequence_holdout_audit: dict[str, Any] | None = None,
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
    if external_control_repair_plan is not None:
        repair_meta = external_control_repair_plan.get("metadata", {})
        repair_rows = [
            row
            for row in external_control_repair_plan.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["external_control_repair_plan_review_only"] = (
            repair_meta.get("ready_for_label_import") is False
            and repair_meta.get("countable_label_candidate_count") == 0
            and repair_meta.get("repair_plan_complete_for_observed_failures") is True
            and all(row.get("countable_label_candidate") is False for row in repair_rows)
            and all(row.get("ready_for_label_import") is False for row in repair_rows)
        )
    if external_control_repair_plan_audit is not None:
        audit_meta = external_control_repair_plan_audit.get("metadata", {})
        gates["external_control_repair_plan_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if reaction_evidence_sample is not None:
        reaction_meta = reaction_evidence_sample.get("metadata", {})
        reaction_rows = [
            row
            for row in reaction_evidence_sample.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["reaction_evidence_sample_review_only"] = (
            reaction_meta.get("ready_for_label_import") is False
            and reaction_meta.get("countable_label_candidate_count") == 0
            and int(reaction_meta.get("candidate_count", 0) or 0) > 0
            and all(row.get("countable_label_candidate") is False for row in reaction_rows)
            and all(row.get("ready_for_label_import") is False for row in reaction_rows)
            and all(
                row.get("evidence_status") == "reaction_context_only"
                for row in reaction_rows
            )
        )
    if reaction_evidence_sample_audit is not None:
        audit_meta = reaction_evidence_sample_audit.get("metadata", {})
        gates["reaction_evidence_sample_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if representation_control_manifest is not None:
        representation_meta = representation_control_manifest.get("metadata", {})
        representation_rows = [
            row
            for row in representation_control_manifest.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["representation_control_manifest_review_only"] = (
            representation_meta.get("ready_for_label_import") is False
            and representation_meta.get("countable_label_candidate_count") == 0
            and representation_meta.get("embedding_status")
            == "not_computed_interface_only"
            and len(representation_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in representation_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in representation_rows
            )
        )
    if representation_control_manifest_audit is not None:
        audit_meta = representation_control_manifest_audit.get("metadata", {})
        gates["representation_control_manifest_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if representation_control_comparison is not None:
        comparison_meta = representation_control_comparison.get("metadata", {})
        comparison_rows = [
            row
            for row in representation_control_comparison.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["representation_control_comparison_review_only"] = (
            comparison_meta.get("ready_for_label_import") is False
            and comparison_meta.get("countable_label_candidate_count") == 0
            and comparison_meta.get("embedding_status") == "feature_proxy_no_embedding"
            and int(comparison_meta.get("candidate_count", 0) or 0)
            == len(comparison_rows)
            and len(comparison_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in comparison_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in comparison_rows
            )
            and all(row.get("comparison_status") for row in comparison_rows)
            and all(row.get("feature_proxy_tokens") for row in comparison_rows)
        )
    if representation_control_comparison_audit is not None:
        audit_meta = representation_control_comparison_audit.get("metadata", {})
        gates["representation_control_comparison_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if representation_backend_plan is not None:
        backend_meta = representation_backend_plan.get("metadata", {})
        backend_rows = [
            row
            for row in representation_backend_plan.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_backend_count = (
            representation_control_manifest.get("metadata", {}).get("candidate_count")
            if representation_control_manifest is not None
            else len(backend_rows)
        )
        gates["representation_backend_plan_review_only"] = (
            backend_meta.get("ready_for_label_import") is False
            and backend_meta.get("countable_label_candidate_count") == 0
            and backend_meta.get("embedding_status") == "backend_plan_only_not_computed"
            and int(backend_meta.get("candidate_count", 0) or 0) == len(backend_rows)
            and int(backend_meta.get("candidate_count", 0) or 0)
            == int(expected_backend_count or 0)
            and len(backend_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in backend_rows
            )
            and all(row.get("ready_for_label_import") is False for row in backend_rows)
            and all(
                row.get("review_status") == "representation_backend_plan_review_only"
                for row in backend_rows
            )
            and all(row.get("required_inputs") for row in backend_rows)
            and all(row.get("recommended_backends") for row in backend_rows)
        )
    if representation_backend_plan_audit is not None:
        backend_audit_meta = representation_backend_plan_audit.get("metadata", {})
        gates["representation_backend_plan_audit_guardrail_clean"] = (
            backend_audit_meta.get("guardrail_clean") is True
            and backend_audit_meta.get("ready_for_label_import") is False
            and backend_audit_meta.get("countable_label_candidate_count") == 0
            and backend_audit_meta.get("embedding_status")
            == "backend_plan_only_not_computed"
        )
    if broad_ec_disambiguation_audit is not None:
        broad_meta = broad_ec_disambiguation_audit.get("metadata", {})
        broad_rows = [
            row
            for row in broad_ec_disambiguation_audit.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["broad_ec_disambiguation_audit_review_only"] = (
            broad_meta.get("guardrail_clean") is True
            and broad_meta.get("ready_for_label_import") is False
            and broad_meta.get("countable_label_candidate_count") == 0
            and int(broad_meta.get("candidate_count", 0) or 0) == len(broad_rows)
            and len(broad_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in broad_rows)
            and all(row.get("ready_for_label_import") is False for row in broad_rows)
            and all(row.get("disambiguation_status") for row in broad_rows)
        )
    if active_site_gap_source_requests is not None:
        source_meta = active_site_gap_source_requests.get("metadata", {})
        source_rows = [
            row
            for row in active_site_gap_source_requests.get("rows", [])
            if isinstance(row, dict)
        ]
        expected_gap_count = (
            active_site_evidence_sample_audit.get("metadata", {}).get(
                "active_site_feature_gap_count"
            )
            if active_site_evidence_sample_audit is not None
            else len(source_rows)
        )
        if expected_gap_count is None:
            expected_gap_count = len(source_rows)
        gates["active_site_gap_source_requests_review_only"] = (
            source_meta.get("ready_for_label_import") is False
            and source_meta.get("countable_label_candidate_count") == 0
            and int(source_meta.get("candidate_count", 0) or 0) == len(source_rows)
            and int(source_meta.get("candidate_count", 0) or 0)
            == int(expected_gap_count or 0)
            and len(source_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in source_rows)
            and all(row.get("ready_for_label_import") is False for row in source_rows)
            and all(row.get("request_status") for row in source_rows)
        )
    if sequence_neighborhood_plan is not None:
        sequence_plan_meta = sequence_neighborhood_plan.get("metadata", {})
        sequence_plan_rows = [
            row
            for row in sequence_neighborhood_plan.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["sequence_neighborhood_plan_review_only"] = (
            sequence_plan_meta.get("ready_for_label_import") is False
            and sequence_plan_meta.get("countable_label_candidate_count") == 0
            and int(sequence_plan_meta.get("candidate_count", 0) or 0)
            == int(candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0)
            and int(sequence_plan_meta.get("candidate_count", 0) or 0)
            == len(sequence_plan_rows)
            and len(sequence_plan_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in sequence_plan_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in sequence_plan_rows
            )
            and all(row.get("plan_status") for row in sequence_plan_rows)
        )
    if sequence_neighborhood_sample is not None:
        sequence_sample_meta = sequence_neighborhood_sample.get("metadata", {})
        sequence_sample_rows = [
            row
            for row in sequence_neighborhood_sample.get("rows", [])
            if isinstance(row, dict)
        ]
        plan_candidate_count = (
            int(
                sequence_neighborhood_plan.get("metadata", {}).get(
                    "candidate_count", 0
                )
                or 0
            )
            if sequence_neighborhood_plan is not None
            else len(sequence_sample_rows)
        )
        gates["sequence_neighborhood_sample_review_only"] = (
            sequence_sample_meta.get("ready_for_label_import") is False
            and sequence_sample_meta.get("countable_label_candidate_count") == 0
            and sequence_sample_meta.get("complete_near_duplicate_search_required")
            is True
            and int(sequence_sample_meta.get("candidate_count", 0) or 0)
            == len(sequence_sample_rows)
            and len(sequence_sample_rows) > 0
            and int(sequence_sample_meta.get("candidate_count", 0) or 0)
            <= plan_candidate_count
            and all(
                row.get("countable_label_candidate") is False
                for row in sequence_sample_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in sequence_sample_rows
            )
            and all(row.get("screen_status") for row in sequence_sample_rows)
        )
    if sequence_neighborhood_sample_audit is not None:
        sequence_sample_audit_meta = sequence_neighborhood_sample_audit.get(
            "metadata", {}
        )
        gates["sequence_neighborhood_sample_audit_guardrail_clean"] = (
            sequence_sample_audit_meta.get("guardrail_clean") is True
            and sequence_sample_audit_meta.get("ready_for_label_import") is False
            and sequence_sample_audit_meta.get("countable_label_candidate_count")
            == 0
            and sequence_sample_audit_meta.get("complete_near_duplicate_search_required")
            is True
        )
    if sequence_alignment_verification is not None:
        alignment_meta = sequence_alignment_verification.get("metadata", {})
        alignment_rows = [
            row
            for row in sequence_alignment_verification.get("rows", []) or []
            if isinstance(row, dict)
        ]
        gates["sequence_alignment_verification_review_only"] = (
            alignment_meta.get("ready_for_label_import") is False
            and alignment_meta.get("countable_label_candidate_count") == 0
            and alignment_meta.get("complete_near_duplicate_search_required") is True
            and int(alignment_meta.get("verified_pair_count", 0) or 0)
            == len(alignment_rows)
            and len(alignment_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in alignment_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in alignment_rows
            )
            and all(row.get("verification_status") for row in alignment_rows)
        )
    if sequence_alignment_verification_audit is not None:
        alignment_audit_meta = sequence_alignment_verification_audit.get(
            "metadata", {}
        )
        gates["sequence_alignment_verification_audit_guardrail_clean"] = (
            alignment_audit_meta.get("guardrail_clean") is True
            and alignment_audit_meta.get("ready_for_label_import") is False
            and alignment_audit_meta.get("countable_label_candidate_count") == 0
            and alignment_audit_meta.get("complete_near_duplicate_search_required")
            is True
        )
    if sequence_search_export is not None:
        search_export_meta = sequence_search_export.get("metadata", {})
        search_export_rows = [
            row
            for row in sequence_search_export.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_sequence_count = (
            sequence_neighborhood_plan.get("metadata", {}).get("candidate_count")
            if sequence_neighborhood_plan is not None
            else len(search_export_rows)
        )
        gates["sequence_search_export_review_only"] = (
            search_export_meta.get("ready_for_label_import") is False
            and search_export_meta.get("complete_near_duplicate_search_required")
            is True
            and search_export_meta.get("countable_label_candidate_count") == 0
            and int(search_export_meta.get("candidate_count", 0) or 0)
            == len(search_export_rows)
            and int(search_export_meta.get("candidate_count", 0) or 0)
            == int(expected_sequence_count or 0)
            and len(search_export_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in search_export_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in search_export_rows
            )
            and all(
                row.get("review_status") == "sequence_search_export_review_only"
                for row in search_export_rows
            )
            and all(row.get("source_targets") for row in search_export_rows)
            and all(row.get("search_task") for row in search_export_rows)
            and all(
                (row.get("decision") or {}).get("decision_status") == "no_decision"
                for row in search_export_rows
            )
        )
    if sequence_search_export_audit is not None:
        search_export_audit_meta = sequence_search_export_audit.get("metadata", {})
        gates["sequence_search_export_audit_guardrail_clean"] = (
            search_export_audit_meta.get("guardrail_clean") is True
            and search_export_audit_meta.get("ready_for_label_import") is False
            and search_export_audit_meta.get("complete_near_duplicate_search_required")
            is True
            and search_export_audit_meta.get("countable_label_candidate_count") == 0
            and search_export_audit_meta.get("completed_decision_count") == 0
        )
    if external_import_readiness_audit is not None:
        import_readiness_meta = external_import_readiness_audit.get("metadata", {})
        gates["external_import_readiness_audit_blocks_label_import"] = (
            import_readiness_meta.get("guardrail_clean") is True
            and import_readiness_meta.get("ready_for_label_import") is False
            and import_readiness_meta.get("countable_label_candidate_count") == 0
            and import_readiness_meta.get("label_import_ready_count") == 0
            and int(import_readiness_meta.get("candidate_count", 0) or 0)
            == int(candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0)
        )
    if active_site_sourcing_queue is not None:
        sourcing_meta = active_site_sourcing_queue.get("metadata", {})
        sourcing_rows = [
            row
            for row in active_site_sourcing_queue.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_gap_count = (
            external_import_readiness_audit.get("metadata", {}).get(
                "active_site_gap_count"
            )
            if external_import_readiness_audit is not None
            else len(sourcing_rows)
        )
        gates["active_site_sourcing_queue_review_only"] = (
            sourcing_meta.get("ready_for_label_import") is False
            and sourcing_meta.get("countable_label_candidate_count") == 0
            and int(sourcing_meta.get("candidate_count", 0) or 0)
            == len(sourcing_rows)
            and int(sourcing_meta.get("candidate_count", 0) or 0)
            == int(expected_gap_count or 0)
            and len(sourcing_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in sourcing_rows)
            and all(row.get("ready_for_label_import") is False for row in sourcing_rows)
            and all(row.get("queue_status") for row in sourcing_rows)
        )
    if active_site_sourcing_queue_audit is not None:
        sourcing_audit_meta = active_site_sourcing_queue_audit.get("metadata", {})
        gates["active_site_sourcing_queue_audit_guardrail_clean"] = (
            sourcing_audit_meta.get("guardrail_clean") is True
            and sourcing_audit_meta.get("ready_for_label_import") is False
            and sourcing_audit_meta.get("countable_label_candidate_count") == 0
        )
    if active_site_sourcing_export is not None:
        export_meta = active_site_sourcing_export.get("metadata", {})
        export_rows = [
            row
            for row in active_site_sourcing_export.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_sourcing_count = (
            active_site_sourcing_queue.get("metadata", {}).get("candidate_count")
            if active_site_sourcing_queue is not None
            else len(export_rows)
        )
        gates["active_site_sourcing_export_review_only"] = (
            export_meta.get("ready_for_label_import") is False
            and export_meta.get("countable_label_candidate_count") == 0
            and int(export_meta.get("candidate_count", 0) or 0) == len(export_rows)
            and int(export_meta.get("candidate_count", 0) or 0)
            == int(expected_sourcing_count or 0)
            and len(export_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in export_rows)
            and all(row.get("ready_for_label_import") is False for row in export_rows)
            and all(
                row.get("review_status") == "active_site_sourcing_export_review_only"
                for row in export_rows
            )
            and all(row.get("source_targets") for row in export_rows)
            and all(row.get("source_task") for row in export_rows)
            and all(
                (row.get("decision") or {}).get("decision_status") == "no_decision"
                for row in export_rows
            )
        )
    if active_site_sourcing_export_audit is not None:
        export_audit_meta = active_site_sourcing_export_audit.get("metadata", {})
        gates["active_site_sourcing_export_audit_guardrail_clean"] = (
            export_audit_meta.get("guardrail_clean") is True
            and export_audit_meta.get("ready_for_label_import") is False
            and export_audit_meta.get("countable_label_candidate_count") == 0
            and export_audit_meta.get("completed_decision_count") == 0
        )
    if transfer_blocker_matrix is not None:
        matrix_meta = transfer_blocker_matrix.get("metadata", {})
        matrix_rows = [
            row
            for row in transfer_blocker_matrix.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_matrix_count = int(
            candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0
        )
        expected_matrix_active_site_count = int(
            (
                active_site_sourcing_export.get("metadata", {}).get("candidate_count")
                if active_site_sourcing_export is not None
                else matrix_meta.get("active_site_sourcing_export_candidate_count")
            )
            or 0
        )
        expected_matrix_sequence_count = int(
            (
                sequence_search_export.get("metadata", {}).get("candidate_count")
                if sequence_search_export is not None
                else matrix_meta.get("sequence_search_export_candidate_count")
            )
            or 0
        )
        expected_matrix_representation_count = int(
            (
                representation_backend_plan.get("metadata", {}).get("candidate_count")
                if representation_backend_plan is not None
                else matrix_meta.get("representation_backend_plan_candidate_count")
            )
            or 0
        )
        gates["external_transfer_blocker_matrix_review_only"] = (
            matrix_meta.get("ready_for_label_import") is False
            and matrix_meta.get("countable_label_candidate_count") == 0
            and int(matrix_meta.get("candidate_count", 0) or 0) == len(matrix_rows)
            and int(matrix_meta.get("candidate_count", 0) or 0)
            == expected_matrix_count
            and int(
                matrix_meta.get("active_site_sourcing_export_candidate_count", 0)
                or 0
            )
            == expected_matrix_active_site_count
            and int(
                matrix_meta.get("sequence_search_export_candidate_count", 0) or 0
            )
            == expected_matrix_sequence_count
            and int(
                matrix_meta.get("representation_backend_plan_candidate_count", 0)
                or 0
            )
            == expected_matrix_representation_count
            and len(matrix_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in matrix_rows)
            and all(row.get("ready_for_label_import") is False for row in matrix_rows)
            and all(
                row.get("review_status")
                == "external_transfer_blocker_matrix_review_only"
                for row in matrix_rows
            )
            and all(row.get("blockers") for row in matrix_rows)
            and all(
                row.get("sequence_search", {}).get("search_task")
                for row in matrix_rows
            )
        )
    if transfer_blocker_matrix_audit is not None:
        matrix_audit_meta = transfer_blocker_matrix_audit.get("metadata", {})
        gates["external_transfer_blocker_matrix_audit_guardrail_clean"] = (
            matrix_audit_meta.get("guardrail_clean") is True
            and matrix_audit_meta.get("ready_for_label_import") is False
            and matrix_audit_meta.get("countable_label_candidate_count") == 0
            and matrix_audit_meta.get("completed_active_site_decision_count") == 0
            and matrix_audit_meta.get("completed_sequence_decision_count") == 0
        )
    if binding_context_repair_plan is not None:
        binding_meta = binding_context_repair_plan.get("metadata", {})
        binding_rows = [
            row
            for row in binding_context_repair_plan.get("rows", [])
            if isinstance(row, dict)
        ]
        gates["binding_context_repair_plan_review_only"] = (
            binding_meta.get("ready_for_label_import") is False
            and binding_meta.get("countable_label_candidate_count") == 0
            and len(binding_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in binding_rows)
            and all(row.get("ready_for_label_import") is False for row in binding_rows)
        )
    if binding_context_repair_plan_audit is not None:
        audit_meta = binding_context_repair_plan_audit.get("metadata", {})
        gates["binding_context_repair_plan_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if binding_context_mapping_sample is not None:
        mapping_meta = binding_context_mapping_sample.get("metadata", {})
        mapping_entries = [
            entry
            for entry in binding_context_mapping_sample.get("entries", [])
            if isinstance(entry, dict)
        ]
        gates["binding_context_mapping_sample_review_only"] = (
            mapping_meta.get("ready_for_label_import") is False
            and mapping_meta.get("countable_label_candidate_count") == 0
            and int(mapping_meta.get("candidate_count", 0) or 0) > 0
            and all(
                entry.get("countable_label_candidate") is False
                for entry in mapping_entries
            )
            and all(
                entry.get("ready_for_label_import") is False
                for entry in mapping_entries
            )
        )
    if binding_context_mapping_sample_audit is not None:
        audit_meta = binding_context_mapping_sample_audit.get("metadata", {})
        gates["binding_context_mapping_sample_audit_guardrail_clean"] = (
            audit_meta.get("guardrail_clean") is True
            and audit_meta.get("ready_for_label_import") is False
            and audit_meta.get("countable_label_candidate_count") == 0
        )
    if sequence_holdout_audit is not None:
        sequence_meta = sequence_holdout_audit.get("metadata", {})
        gates["external_sequence_holdout_audit_guardrail_clean"] = (
            sequence_meta.get("guardrail_clean") is True
            and sequence_meta.get("ready_for_label_import") is False
            and sequence_meta.get("countable_label_candidate_count") == 0
            and int(sequence_meta.get("candidate_count", 0) or 0)
            == int(candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0)
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
            "external_control_repair_row_count": (
                external_control_repair_plan.get("metadata", {}).get(
                    "repair_row_count", 0
                )
                if external_control_repair_plan is not None
                else 0
            ),
            "external_control_repair_complete": (
                external_control_repair_plan.get("metadata", {}).get(
                    "repair_plan_complete_for_observed_failures", False
                )
                if external_control_repair_plan is not None
                else False
            ),
            "reaction_evidence_candidate_count": (
                reaction_evidence_sample.get("metadata", {}).get("candidate_count", 0)
                if reaction_evidence_sample is not None
                else 0
            ),
            "reaction_evidence_record_count": (
                reaction_evidence_sample.get("metadata", {}).get(
                    "reaction_record_count", 0
                )
                if reaction_evidence_sample is not None
                else 0
            ),
            "reaction_broad_ec_context_row_count": (
                reaction_evidence_sample_audit.get("metadata", {}).get(
                    "broad_ec_context_row_count", 0
                )
                if reaction_evidence_sample_audit is not None
                else 0
            ),
            "representation_control_candidate_count": (
                representation_control_manifest.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if representation_control_manifest is not None
                else 0
            ),
            "representation_control_eligible_count": (
                representation_control_manifest.get("metadata", {}).get(
                    "eligible_control_count", 0
                )
                if representation_control_manifest is not None
                else 0
            ),
            "representation_control_scope_mismatch_count": (
                representation_control_manifest.get("metadata", {}).get(
                    "scope_top1_mismatch_count", 0
                )
                if representation_control_manifest is not None
                else 0
            ),
            "representation_control_comparison_candidate_count": (
                representation_control_comparison.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if representation_control_comparison is not None
                else 0
            ),
            "representation_control_comparison_scope_mismatch_count": (
                representation_control_comparison.get("metadata", {}).get(
                    "scope_top1_mismatch_count", 0
                )
                if representation_control_comparison is not None
                else 0
            ),
            "representation_control_comparison_metal_collapse_count": (
                representation_control_comparison.get("metadata", {}).get(
                    "metal_hydrolase_collapse_flag_count", 0
                )
                if representation_control_comparison is not None
                else 0
            ),
            "representation_backend_plan_candidate_count": (
                representation_backend_plan.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if representation_backend_plan is not None
                else 0
            ),
            "representation_backend_plan_sequence_blocked_count": (
                representation_backend_plan.get("metadata", {}).get(
                    "sequence_search_blocked_count", 0
                )
                if representation_backend_plan is not None
                else 0
            ),
            "representation_backend_plan_contrast_required_count": (
                representation_backend_plan.get("metadata", {}).get(
                    "heuristic_contrast_required_count", 0
                )
                if representation_backend_plan is not None
                else 0
            ),
            "broad_ec_disambiguation_candidate_count": (
                broad_ec_disambiguation_audit.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if broad_ec_disambiguation_audit is not None
                else 0
            ),
            "broad_ec_specific_context_available_count": (
                broad_ec_disambiguation_audit.get("metadata", {}).get(
                    "specific_context_available_count", 0
                )
                if broad_ec_disambiguation_audit is not None
                else 0
            ),
            "active_site_gap_source_request_count": (
                active_site_gap_source_requests.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if active_site_gap_source_requests is not None
                else 0
            ),
            "active_site_gap_mapped_binding_context_request_count": (
                active_site_gap_source_requests.get("metadata", {}).get(
                    "mapped_binding_context_request_count", 0
                )
                if active_site_gap_source_requests is not None
                else 0
            ),
            "sequence_neighborhood_plan_candidate_count": (
                sequence_neighborhood_plan.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if sequence_neighborhood_plan is not None
                else 0
            ),
            "sequence_neighborhood_near_duplicate_search_request_count": (
                sequence_neighborhood_plan.get("metadata", {}).get(
                    "near_duplicate_search_request_count", 0
                )
                if sequence_neighborhood_plan is not None
                else 0
            ),
            "sequence_neighborhood_sample_candidate_count": (
                sequence_neighborhood_sample.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if sequence_neighborhood_sample is not None
                else 0
            ),
            "sequence_neighborhood_reference_sequence_count": (
                sequence_neighborhood_sample.get("metadata", {}).get(
                    "reference_sequence_count", 0
                )
                if sequence_neighborhood_sample is not None
                else 0
            ),
            "sequence_neighborhood_high_similarity_candidate_count": (
                sequence_neighborhood_sample.get("metadata", {}).get(
                    "high_similarity_candidate_count", 0
                )
                if sequence_neighborhood_sample is not None
                else 0
            ),
            "sequence_neighborhood_screen_requires_complete_search": (
                sequence_neighborhood_sample.get("metadata", {}).get(
                    "complete_near_duplicate_search_required", False
                )
                if sequence_neighborhood_sample is not None
                else False
            ),
            "sequence_alignment_verified_pair_count": (
                sequence_alignment_verification.get("metadata", {}).get(
                    "verified_pair_count", 0
                )
                if sequence_alignment_verification is not None
                else 0
            ),
            "sequence_alignment_alert_candidate_count": (
                sequence_alignment_verification.get("metadata", {}).get(
                    "alignment_alert_candidate_count", 0
                )
                if sequence_alignment_verification is not None
                else 0
            ),
            "sequence_alignment_deferred_pair_count": (
                sequence_alignment_verification.get("metadata", {}).get(
                    "alignment_deferred_pair_count", 0
                )
                if sequence_alignment_verification is not None
                else 0
            ),
            "sequence_search_export_candidate_count": (
                sequence_search_export.get("metadata", {}).get("candidate_count", 0)
                if sequence_search_export is not None
                else 0
            ),
            "sequence_search_export_near_duplicate_request_count": (
                sequence_search_export.get("metadata", {}).get(
                    "near_duplicate_search_request_count", 0
                )
                if sequence_search_export is not None
                else 0
            ),
            "sequence_search_export_completed_decision_count": (
                sequence_search_export_audit.get("metadata", {}).get(
                    "completed_decision_count", 0
                )
                if sequence_search_export_audit is not None
                else 0
            ),
            "external_import_readiness_candidate_count": (
                external_import_readiness_audit.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if external_import_readiness_audit is not None
                else 0
            ),
            "external_import_readiness_active_site_gap_count": (
                external_import_readiness_audit.get("metadata", {}).get(
                    "active_site_gap_count", 0
                )
                if external_import_readiness_audit is not None
                else 0
            ),
            "external_import_readiness_representation_issue_count": (
                external_import_readiness_audit.get("metadata", {}).get(
                    "representation_control_issue_count", 0
                )
                if external_import_readiness_audit is not None
                else 0
            ),
            "active_site_sourcing_queue_candidate_count": (
                active_site_sourcing_queue.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if active_site_sourcing_queue is not None
                else 0
            ),
            "active_site_sourcing_ready_candidate_count": (
                active_site_sourcing_queue.get("metadata", {}).get(
                    "ready_sourcing_candidate_count", 0
                )
                if active_site_sourcing_queue is not None
                else 0
            ),
            "active_site_sourcing_text_source_candidate_count": (
                active_site_sourcing_queue.get("metadata", {}).get(
                    "text_source_candidate_count", 0
                )
                if active_site_sourcing_queue is not None
                else 0
            ),
            "active_site_sourcing_export_candidate_count": (
                active_site_sourcing_export.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if active_site_sourcing_export is not None
                else 0
            ),
            "active_site_sourcing_export_source_target_count": (
                active_site_sourcing_export.get("metadata", {}).get(
                    "source_target_count", 0
                )
                if active_site_sourcing_export is not None
                else 0
            ),
            "active_site_sourcing_export_completed_decision_count": (
                active_site_sourcing_export_audit.get("metadata", {}).get(
                    "completed_decision_count", 0
                )
                if active_site_sourcing_export_audit is not None
                else 0
            ),
            "external_transfer_blocker_matrix_candidate_count": (
                transfer_blocker_matrix.get("metadata", {}).get("candidate_count", 0)
                if transfer_blocker_matrix is not None
                else 0
            ),
            "external_transfer_blocker_matrix_sequence_count": (
                transfer_blocker_matrix.get("metadata", {}).get(
                    "sequence_search_export_candidate_count", 0
                )
                if transfer_blocker_matrix is not None
                else 0
            ),
            "external_transfer_blocker_matrix_active_site_count": (
                transfer_blocker_matrix.get("metadata", {}).get(
                    "active_site_sourcing_export_candidate_count", 0
                )
                if transfer_blocker_matrix is not None
                else 0
            ),
            "external_transfer_blocker_matrix_representation_count": (
                transfer_blocker_matrix.get("metadata", {}).get(
                    "representation_backend_plan_candidate_count", 0
                )
                if transfer_blocker_matrix is not None
                else 0
            ),
            "external_transfer_blocker_matrix_completed_decision_count": (
                (
                    transfer_blocker_matrix_audit.get("metadata", {}).get(
                        "completed_active_site_decision_count", 0
                    )
                    + transfer_blocker_matrix_audit.get("metadata", {}).get(
                        "completed_sequence_decision_count", 0
                    )
                )
                if transfer_blocker_matrix_audit is not None
                else 0
            ),
            "binding_context_ready_candidate_count": (
                binding_context_repair_plan.get("metadata", {}).get(
                    "ready_binding_context_candidate_count", 0
                )
                if binding_context_repair_plan is not None
                else 0
            ),
            "binding_context_deferred_candidate_count": (
                binding_context_repair_plan.get("metadata", {}).get(
                    "deferred_binding_context_candidate_count", 0
                )
                if binding_context_repair_plan is not None
                else 0
            ),
            "binding_context_position_count": (
                binding_context_repair_plan.get("metadata", {}).get(
                    "binding_position_count", 0
                )
                if binding_context_repair_plan is not None
                else 0
            ),
            "binding_context_mapping_sampled_candidate_count": (
                binding_context_mapping_sample.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if binding_context_mapping_sample is not None
                else 0
            ),
            "binding_context_mapping_mapped_candidate_count": (
                binding_context_mapping_sample.get("metadata", {}).get(
                    "mapped_candidate_count", 0
                )
                if binding_context_mapping_sample is not None
                else 0
            ),
            "sequence_holdout_exact_overlap_count": (
                sequence_holdout_audit.get("metadata", {}).get(
                    "exact_reference_overlap_holdout_count", 0
                )
                if sequence_holdout_audit is not None
                else 0
            ),
            "sequence_holdout_near_duplicate_search_count": (
                sequence_holdout_audit.get("metadata", {}).get(
                    "near_duplicate_search_candidate_count", 0
                )
                if sequence_holdout_audit is not None
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
    compatible_top1 = {
        "glycan_chemistry": {
            "metal_dependent_hydrolase",
            "ser_his_acid_hydrolase",
        },
        "oxidoreductase_long_tail": {
            "flavin_dehydrogenase_reductase",
            "heme_peroxidase_oxidase",
            "radical_sam_enzyme",
        },
    }
    if scope in compatible_top1:
        return top1_fingerprint not in compatible_top1[scope]
    if scope in {"isomerase", "lyase", "transferase_methyl", "transferase_phosphoryl"}:
        return True
    return False


def _external_active_site_gap_repair_row(summary: dict[str, Any]) -> dict[str, Any]:
    binding_count = int(summary.get("binding_site_feature_count", 0) or 0)
    catalytic_count = int(summary.get("catalytic_activity_count", 0) or 0)
    if binding_count:
        repair_lane = "map_binding_site_context_then_source_catalytic_positions"
        required_next_evidence = [
            "inspect UniProt binding-site positions as non-countable mapping context",
            "source explicit catalytic or active-site residue positions",
            "rerun structure mapping and heuristic controls after positions exist",
        ]
    elif catalytic_count:
        repair_lane = "source_catalytic_positions_from_curated_literature"
        required_next_evidence = [
            "source catalytic residue positions from curated literature or database cross-reference",
            "keep reaction text separate from active-site evidence",
            "rerun structure mapping and heuristic controls after positions exist",
        ]
    else:
        repair_lane = "defer_until_curated_active_site_or_structure_evidence"
        required_next_evidence = [
            "find curated active-site or binding-site evidence",
            "verify candidate structure reference before scoring",
            "rerun external evidence gates before any decision artifact",
        ]
    return {
        "accession": summary.get("accession"),
        "alphafold_ids_sample": summary.get("alphafold_ids_sample", []),
        "binding_site_feature_count": binding_count,
        "blockers": [
            "uniprot_active_site_feature_missing",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "catalytic_activity_count": catalytic_count,
        "countable_label_candidate": False,
        "lane_id": summary.get("lane_id"),
        "pdb_ids_sample": summary.get("pdb_ids_sample", []),
        "protein_name": summary.get("protein_name"),
        "ready_for_label_import": False,
        "repair_lane": repair_lane,
        "repair_type": "active_site_feature_gap",
        "required_next_evidence": required_next_evidence,
        "scope_signal": summary.get("scope_signal"),
        "specific_ec_numbers": summary.get("specific_ec_numbers", []),
    }


def _external_broad_ec_repair_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "accession": summary.get("accession"),
        "blockers": [
            "specific_reaction_disambiguation_for_broad_ec",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "broad_or_incomplete_ec_numbers": list(
            summary.get("broad_or_incomplete_ec_numbers") or []
        ),
        "countable_label_candidate": False,
        "lane_id": summary.get("lane_id"),
        "protein_name": summary.get("protein_name"),
        "ready_for_label_import": False,
        "repair_lane": "resolve_specific_reaction_context_before_scoring",
        "repair_type": "broad_ec_disambiguation",
        "required_next_evidence": [
            "replace broad or incomplete EC context with a specific reaction record",
            "confirm reaction direction and substrate class before interpreting heuristic controls",
            "keep broad-EC rows out of countable imports until the full factory gate passes",
        ],
        "scope_signal": summary.get("scope_signal"),
        "specific_ec_numbers": summary.get("specific_ec_numbers", []),
    }


def _external_heuristic_control_repair_row(
    *,
    result: dict[str, Any],
    heuristic_findings: list[str],
) -> dict[str, Any]:
    top1 = _external_top1_fingerprint(result)
    scope_signal = str(result.get("external_scope_signal") or "")
    if top1 == "metal_dependent_hydrolase" and scope_signal == "glycan_chemistry":
        repair_lane = "separate_glycan_chemistry_from_metal_hydrolase_boundary"
    elif top1 == "metal_dependent_hydrolase":
        repair_lane = "add_scope_specific_negative_control_and_representation_features"
    elif bool(result.get("scope_top1_mismatch")):
        repair_lane = "add_lane_specific_scope_contrastive_controls"
    else:
        repair_lane = "compare_heuristic_control_against_learned_representation"
    return {
        "accession": str(result.get("entry_id") or "").removeprefix("uniprot:"),
        "blockers": [
            "heuristic_control_failure_unresolved",
            "external_ood_calibration_not_applied",
            "external_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "control_findings": heuristic_findings,
        "countable_label_candidate": False,
        "entry_id": result.get("entry_id"),
        "lane_id": result.get("external_lane_id"),
        "protein_name": result.get("protein_name"),
        "ready_for_label_import": False,
        "repair_lane": repair_lane,
        "repair_type": "heuristic_control_failure",
        "required_next_evidence": [
            "add lane-specific adversarial negative controls",
            "compare heuristic scores against learned or structure-language representations",
            "audit ontology-family boundaries before any external decision artifact",
            "rerun external transfer gates after control separation improves",
        ],
        "scope_signal": scope_signal,
        "scope_top1_mismatch": bool(result.get("scope_top1_mismatch")),
        "specific_ec_numbers": result.get("specific_ec_numbers", []),
        "top1_fingerprint": top1,
    }


def _external_top1_fingerprint(result: dict[str, Any]) -> str | None:
    top_fingerprints = result.get("top_fingerprints", [])
    if not top_fingerprints:
        return None
    top1 = top_fingerprints[0]
    if not isinstance(top1, dict):
        return None
    fingerprint = top1.get("fingerprint_id")
    return str(fingerprint) if fingerprint else None


def _external_control_repair_coverage(
    *,
    rows: list[dict[str, Any]],
    observed_failure_modes: list[str],
    heuristic_findings: list[str],
) -> list[str]:
    covered: set[str] = set()
    if any(row.get("repair_type") == "active_site_feature_gap" for row in rows):
        covered.add("external_active_site_feature_gap")
    if any(row.get("repair_type") == "broad_ec_disambiguation" for row in rows):
        covered.add("external_broad_ec_disambiguation_needed")
    if any(row.get("repair_type") == "heuristic_control_failure" for row in rows):
        covered.update(heuristic_findings)
    return [mode for mode in observed_failure_modes if mode in covered]


def _external_representation_control_blockers(
    *,
    entry: dict[str, Any],
    score_row: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if entry.get("status") != "ok":
        blockers.append("structure_mapping_status_not_ok")
    if int(entry.get("resolved_residue_count", 0) or 0) <= 0:
        blockers.append("no_resolved_external_residue_positions")
    if not score_row:
        blockers.append("heuristic_control_score_missing")
    return blockers


def _external_reaction_context_by_entry(
    reaction_evidence_sample: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    contexts: dict[str, dict[str, Any]] = {}
    for row in reaction_evidence_sample.get("rows", []) or []:
        if not isinstance(row, dict) or not row.get("entry_id"):
            continue
        entry_id = str(row.get("entry_id"))
        context = contexts.setdefault(entry_id, _empty_external_reaction_context(entry_id))
        context["reaction_record_count"] += 1
        ec_number = str(row.get("ec_number") or "")
        if row.get("ec_specificity") == "specific" and ec_number:
            context["specific_ec_numbers"].append(ec_number)
        elif ec_number:
            context["broad_or_incomplete_ec_numbers"].append(ec_number)
        rhea_id = str(row.get("rhea_id") or "")
        if rhea_id:
            context["rhea_ids"].append(rhea_id)
    for context in contexts.values():
        context["specific_ec_numbers"] = sorted(set(context["specific_ec_numbers"]))
        context["broad_or_incomplete_ec_numbers"] = sorted(
            set(context["broad_or_incomplete_ec_numbers"])
        )
        context["rhea_ids"] = sorted(set(context["rhea_ids"]))
        context["has_reaction_context"] = context["reaction_record_count"] > 0
        context["has_specific_reaction_context"] = bool(context["specific_ec_numbers"])
        context["has_broad_ec_context"] = bool(context["broad_or_incomplete_ec_numbers"])
    return contexts


def _empty_external_reaction_context(entry_id: str) -> dict[str, Any]:
    return {
        "entry_id": entry_id,
        "broad_or_incomplete_ec_numbers": [],
        "has_broad_ec_context": False,
        "has_reaction_context": False,
        "has_specific_reaction_context": False,
        "reaction_record_count": 0,
        "rhea_ids": [],
        "specific_ec_numbers": [],
    }


def _external_representation_proxy_tokens(
    *,
    manifest_row: dict[str, Any],
    reaction_context: dict[str, Any],
) -> list[str]:
    feature_summary = manifest_row.get("feature_summary", {})
    if not isinstance(feature_summary, dict):
        feature_summary = {}
    tokens = [
        f"scope:{manifest_row.get('scope_signal') or 'unknown'}",
        f"lane:{manifest_row.get('lane_id') or 'unknown'}",
        f"resolved_residue_count:{feature_summary.get('resolved_residue_count') or 0}",
        (
            "reaction:specific"
            if reaction_context.get("has_specific_reaction_context")
            else "reaction:broad"
            if reaction_context.get("has_broad_ec_context")
            else "reaction:missing"
        ),
    ]
    for residue_code in sorted(
        {
            str(code).upper()
            for code in feature_summary.get("residue_codes", []) or []
            if code
        }
    ):
        tokens.append(f"active_site_residue:{residue_code}")
    for cofactor_family in sorted(
        {
            str(family)
            for family in feature_summary.get("local_cofactor_families", []) or []
            if family
        }
    ):
        tokens.append(f"local_cofactor:{cofactor_family}")
    if not any(token.startswith("local_cofactor:") for token in tokens):
        tokens.append("local_cofactor:none")
    for ec_number in reaction_context.get("specific_ec_numbers", [])[:5]:
        tokens.append(f"specific_ec:{ec_number}")
    for ec_number in reaction_context.get("broad_or_incomplete_ec_numbers", [])[:5]:
        tokens.append(f"broad_ec:{ec_number}")
    pocket_names = feature_summary.get("pocket_descriptor_names", []) or []
    for descriptor_name in sorted(str(name) for name in pocket_names if name)[:8]:
        tokens.append(f"pocket_descriptor:{descriptor_name}")
    return tokens


def _external_representation_proxy_status(
    *,
    scope_signal: str,
    top1_fingerprint: str,
    reaction_context: dict[str, Any],
    scope_top1_mismatch: bool,
) -> str:
    if not reaction_context.get("has_reaction_context"):
        return "needs_reaction_context_before_representation_comparison"
    if scope_top1_mismatch and top1_fingerprint == "metal_dependent_hydrolase":
        return "proxy_flags_metal_hydrolase_collapse"
    if scope_top1_mismatch:
        return "proxy_flags_scope_top1_mismatch"
    if scope_signal == "glycan_chemistry" and top1_fingerprint == "metal_dependent_hydrolase":
        return "proxy_boundary_case_requires_glycan_hydrolase_split"
    return "proxy_consistent_with_heuristic_scope"


def _external_representation_axes(
    *,
    scope_signal: str,
    top1_fingerprint: str,
    reaction_context: dict[str, Any],
    scope_top1_mismatch: bool,
) -> list[str]:
    axes = [
        "active_site_residue_token_axis",
        "pocket_composition_axis",
        "reaction_context_axis",
    ]
    if reaction_context.get("has_broad_ec_context"):
        axes.append("broad_ec_disambiguation_axis")
    if scope_signal in {"transferase_methyl", "transferase_phosphoryl"}:
        axes.append("transferase_reaction_class_axis")
    if scope_signal == "oxidoreductase_long_tail":
        axes.append("redox_cofactor_context_axis")
    if scope_signal in {"isomerase", "lyase"}:
        axes.append("non_hydrolytic_scope_axis")
    if scope_signal == "glycan_chemistry":
        axes.append("glycan_hydrolase_boundary_axis")
    if scope_top1_mismatch or top1_fingerprint == "metal_dependent_hydrolase":
        axes.append("heuristic_top1_contrast_axis")
    return sorted(set(axes))


def _external_representation_backend_status(
    *,
    manifest_row: dict[str, Any],
    comparison: dict[str, Any],
    sequence: dict[str, Any],
) -> str:
    if sequence.get("search_task") == "keep_sequence_holdout_control":
        return "blocked_by_sequence_holdout_control"
    if sequence.get("search_task") != "run_complete_uniref_or_all_vs_all_near_duplicate_search":
        return "blocked_until_sequence_search_complete"
    if not manifest_row.get("eligible_for_representation_control"):
        return "blocked_by_representation_input_gap"
    if not comparison.get("comparison_status"):
        return "blocked_until_feature_proxy_comparison_attached"
    return "ready_for_backend_selection_not_embedding"


def _external_representation_backend_blockers(readiness_status: str) -> list[str]:
    blockers = [
        "external_embeddings_not_computed",
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if readiness_status == "blocked_by_sequence_holdout_control":
        blockers.insert(0, "sequence_holdout_control_not_resolved")
    elif readiness_status == "blocked_until_sequence_search_complete":
        blockers.insert(0, "complete_near_duplicate_reference_search_not_completed")
    elif readiness_status == "blocked_by_representation_input_gap":
        blockers.insert(0, "representation_input_gap")
    elif readiness_status == "blocked_until_feature_proxy_comparison_attached":
        blockers.insert(0, "feature_proxy_comparison_missing")
    else:
        blockers.insert(0, "representation_backend_not_selected")
    return blockers


def _external_representation_backend_options(
    *,
    scope_signal: str,
    comparison_status: str,
) -> list[str]:
    options = [
        "sequence_language_model_embedding",
        "structure_or_active_site_language_model_embedding",
        "heuristic_geometry_baseline_control",
    ]
    if (
        comparison_status.startswith("proxy_flags_")
        or scope_signal in {"transferase_phosphoryl", "transferase_methyl"}
    ):
        options.append("active_site_contrastive_baseline")
    if scope_signal == "glycan_chemistry":
        options.append("glycan_boundary_contrastive_axis")
    if scope_signal == "oxidoreductase_long_tail":
        options.append("redox_cofactor_contrastive_axis")
    return sorted(set(options))


def _external_representation_required_inputs(
    *,
    manifest_row: dict[str, Any],
    sequence: dict[str, Any],
) -> list[dict[str, Any]]:
    accession = _normalize_accession(manifest_row.get("accession"))
    feature_summary = manifest_row.get("feature_summary", {})
    if not isinstance(feature_summary, dict):
        feature_summary = {}
    inputs = [
        {
            "input_type": "candidate_sequence",
            "status": "required_not_embedded",
            "source_id": accession,
        },
        {
            "input_type": "heuristic_baseline_scores",
            "status": "required_attached",
            "source_id": manifest_row.get("entry_id"),
        },
        {
            "input_type": "sequence_search_control",
            "status": sequence.get("search_task") or "required_not_complete",
            "source_id": accession,
        },
    ]
    structure_id = feature_summary.get("structure_id")
    if structure_id:
        inputs.append(
            {
                "input_type": "mapped_active_site_structure",
                "status": "required_not_embedded",
                "source_id": structure_id,
                "source_type": feature_summary.get("structure_source"),
            }
        )
    else:
        inputs.append(
            {
                "input_type": "mapped_active_site_structure",
                "status": "required_missing",
                "source_id": None,
            }
        )
    return inputs


def _external_binding_evidence_references(row: dict[str, Any]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str]] = set()
    refs: list[dict[str, str]] = []
    for position in row.get("binding_positions", []) or []:
        if not isinstance(position, dict):
            continue
        ligand_name = str(position.get("ligand_name") or "")
        for evidence in position.get("evidence", []) or []:
            if not isinstance(evidence, dict):
                continue
            source = str(evidence.get("source") or "")
            evidence_id = str(evidence.get("id") or "")
            if not source or not evidence_id:
                continue
            key = (source, evidence_id, ligand_name)
            if key in seen:
                continue
            seen.add(key)
            refs.append(
                {
                    "source": source,
                    "id": evidence_id,
                    "ligand_name": ligand_name,
                }
            )
    return refs


def _external_binding_context_repair_blockers(repair_status: str) -> list[str]:
    blockers = [
        "active_site_positions_still_missing",
        "external_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if repair_status == "ready_for_binding_context_mapping":
        blockers.append("binding_context_not_yet_mapped_to_structure")
    else:
        blockers.append("binding_context_missing")
    return blockers


def _external_binding_context_mapping_failure_entry(
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
        "binding_position_count": len(row.get("binding_positions", []) or []),
        "countable_label_candidate": False,
        "entry_id": f"uniprot:{accession}",
        "error": error,
        "lane_id": row.get("lane_id"),
        "ligand_context": {},
        "missing_binding_positions": row.get("binding_positions", []),
        "pairwise_distances_angstrom": [],
        "pocket_context": {},
        "protein_name": row.get("protein_name"),
        "ready_for_label_import": False,
        "resolved_binding_position_count": 0,
        "residues": [],
        "scope_signal": row.get("scope_signal"),
        "specific_ec_numbers": row.get("specific_ec_numbers", []),
        "status": status,
        "structure_id": structure_id,
        "structure_source": structure_source,
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
        if not isinstance(label, dict) and not hasattr(label, "entry_id"):
            continue
        if _label_field(label, "review_status") not in {
            "automation_curated",
            "expert_reviewed",
        }:
            continue
        if _label_field(label, "label_type") not in {
            "seed_fingerprint",
            "out_of_scope",
        }:
            continue
        count += 1
    return count


def _countable_label_entry_ids(labels: list[dict[str, Any]]) -> set[str]:
    entry_ids: set[str] = set()
    for label in labels:
        if not isinstance(label, dict) and not hasattr(label, "entry_id"):
            continue
        if _label_field(label, "review_status") not in {
            "automation_curated",
            "expert_reviewed",
        }:
            continue
        if _label_field(label, "label_type") not in {
            "seed_fingerprint",
            "out_of_scope",
        }:
            continue
        entry_id = str(_label_field(label, "entry_id") or "")
        if entry_id:
            entry_ids.add(entry_id)
    return entry_ids


def _label_field(label: Any, field: str) -> Any:
    if isinstance(label, dict):
        return label.get(field)
    return getattr(label, field, None)


def _duplicate_accessions(rows: list[dict[str, Any]]) -> list[str]:
    counts = Counter(_normalize_accession(row.get("accession")) for row in rows)
    return sorted(
        accession for accession, count in counts.items() if accession and count > 1
    )


def _normalize_accession(value: Any) -> str:
    return str(value or "").strip().upper()


def _clean_sequence(value: Any) -> str:
    return "".join(ch for ch in str(value or "").upper() if ch.isalpha())


def _fetch_uniprot_sequence_records(accessions: list[str]) -> dict[str, Any]:
    cleaned = sorted({_normalize_accession(accession) for accession in accessions})
    cleaned = [accession for accession in cleaned if accession]
    records: list[dict[str, Any]] = []
    batch_metadata: list[dict[str, Any]] = []
    for batch in _batch_items(cleaned, 20):
        query = "(" + " OR ".join(f"accession:{accession}" for accession in batch) + ")"
        payload = fetch_uniprot_query(query, size=len(batch))
        batch_records = [
            record
            for record in payload.get("records", []) or []
            if isinstance(record, dict)
        ]
        records.extend(batch_records)
        batch_metadata.append(
            {
                "requested_accession_count": len(batch),
                "record_count": len(batch_records),
            }
        )
    by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in records
        if _normalize_accession(record.get("accession"))
    }
    return {
        "metadata": {
            "source": "uniprot_sequence_batch_search",
            "requested_accession_count": len(cleaned),
            "record_count": len(by_accession),
            "batch_count": len(batch_metadata),
            "batches": batch_metadata,
        },
        "records": [by_accession[accession] for accession in sorted(by_accession)],
    }


def _batch_items(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def _sequence_similarity_match(
    *,
    external_accession: str,
    external_sequence: str,
    reference_accession: str,
    reference_sequence: str,
    matched_m_csa_entry_ids: list[str],
    identity_alert_threshold: float,
    coverage_alert_threshold: float,
    kmer_alert_threshold: float,
) -> dict[str, Any] | None:
    external_sequence = _clean_sequence(external_sequence)
    reference_sequence = _clean_sequence(reference_sequence)
    if not external_sequence or not reference_sequence:
        return None
    min_len = min(len(external_sequence), len(reference_sequence))
    max_len = max(len(external_sequence), len(reference_sequence))
    positional_matches = sum(
        1
        for left, right in zip(external_sequence[:min_len], reference_sequence[:min_len])
        if left == right
    )
    positional_identity = positional_matches / min_len if min_len else 0.0
    length_coverage = min_len / max_len if max_len else 0.0
    kmer_jaccard = _sequence_kmer_jaccard(external_sequence, reference_sequence)
    near_duplicate_score = max(positional_identity * length_coverage, kmer_jaccard)
    near_duplicate_alert = (
        positional_identity >= identity_alert_threshold
        and length_coverage >= coverage_alert_threshold
    ) or kmer_jaccard >= kmer_alert_threshold
    return {
        "external_accession": external_accession,
        "reference_accession": reference_accession,
        "matched_m_csa_entry_ids": matched_m_csa_entry_ids,
        "external_length": len(external_sequence),
        "reference_length": len(reference_sequence),
        "length_coverage": round(length_coverage, 4),
        "positional_identity": round(positional_identity, 4),
        "kmer_jaccard": round(kmer_jaccard, 4),
        "near_duplicate_score": round(near_duplicate_score, 4),
        "near_duplicate_alert": near_duplicate_alert,
        "review_status": "sequence_similarity_screen_review_only",
    }


def _external_sequence_alignment_pairs(
    sequence_neighborhood_sample: dict[str, Any],
    *,
    top_k: int,
) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for row in sequence_neighborhood_sample.get("top_hit_rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        reference_accession = _normalize_accession(row.get("reference_accession"))
        if accession and reference_accession:
            pairs.append(
                {
                    "accession": accession,
                    "reference_accession": reference_accession,
                    "matched_m_csa_entry_ids": row.get(
                        "matched_m_csa_entry_ids", []
                    ),
                    "near_duplicate_alert": row.get("near_duplicate_alert"),
                    "near_duplicate_score": row.get("near_duplicate_score"),
                }
            )
    if pairs:
        return pairs

    for row in sequence_neighborhood_sample.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        for match in (row.get("top_matches", []) or [])[:top_k]:
            if not isinstance(match, dict):
                continue
            reference_accession = _normalize_accession(
                match.get("reference_accession")
            )
            if not accession or not reference_accession:
                continue
            pairs.append(
                {
                    "accession": accession,
                    "reference_accession": reference_accession,
                    "matched_m_csa_entry_ids": match.get(
                        "matched_m_csa_entry_ids", []
                    ),
                    "near_duplicate_alert": match.get("near_duplicate_alert"),
                    "near_duplicate_score": match.get("near_duplicate_score"),
                }
            )
    return pairs


def _sequence_length_coverage(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return min(len(left), len(right)) / max(len(left), len(right))


def _sequence_global_edit_identity(left: str, right: str) -> float:
    left = _clean_sequence(left)
    right = _clean_sequence(right)
    if not left or not right:
        return 0.0
    previous = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current = [left_index] + [0] * len(right)
        for right_index, right_char in enumerate(right, start=1):
            substitution_cost = 0 if left_char == right_char else 1
            current[right_index] = min(
                previous[right_index] + 1,
                current[right_index - 1] + 1,
                previous[right_index - 1] + substitution_cost,
            )
        previous = current
    edit_distance = previous[-1]
    return max(0.0, 1.0 - (edit_distance / max(len(left), len(right))))


def _sequence_kmer_jaccard(
    external_sequence: str, reference_sequence: str, kmer_size: int = 5
) -> float:
    left = _sequence_kmers(external_sequence, kmer_size=kmer_size)
    right = _sequence_kmers(reference_sequence, kmer_size=kmer_size)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _sequence_kmers(sequence: str, *, kmer_size: int) -> set[str]:
    if len(sequence) < kmer_size:
        return {sequence} if sequence else set()
    return {sequence[index : index + kmer_size] for index in range(len(sequence) - kmer_size + 1)}


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


def _external_sequence_holdout_blockers(holdout_status: str) -> list[str]:
    blockers = [
        "external_ood_calibration_not_applied",
        "external_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if holdout_status == "exact_reference_overlap_holdout":
        blockers.append("exact_reference_overlap_existing_m_csa")
    elif holdout_status == "sequence_failure_set_holdout":
        blockers.append("sequence_failure_set_overlap")
    else:
        blockers.append("near_duplicate_search_not_completed")
    return blockers


def _external_sequence_alignment_status(
    sequence_alignment: list[dict[str, Any]] | None,
) -> str | None:
    if not sequence_alignment:
        return None
    statuses = {str(row.get("verification_status") or "") for row in sequence_alignment}
    if "alignment_near_duplicate_candidate_holdout" in statuses:
        return "alignment_near_duplicate_candidate_holdout"
    if "sequence_missing_for_alignment" in statuses:
        return "sequence_missing_for_alignment"
    if "alignment_deferred_pair_too_large" in statuses:
        return "alignment_deferred_pair_too_large"
    if "alignment_no_near_duplicate_signal" in statuses:
        return "alignment_no_near_duplicate_signal"
    return sorted(statuses)[0] if statuses else None


def _external_sequence_search_task(
    *,
    plan_status: str,
    screen_status: str,
    alignment_status: str | None,
) -> str:
    if plan_status in {
        "exact_reference_overlap_keep_as_holdout",
        "sequence_failure_set_keep_as_holdout",
    }:
        return "keep_sequence_holdout_control"
    if alignment_status == "alignment_near_duplicate_candidate_holdout":
        return "keep_sequence_holdout_control"
    if screen_status == "near_duplicate_candidate_holdout":
        return "keep_sequence_holdout_control"
    return "run_complete_uniref_or_all_vs_all_near_duplicate_search"


def _external_sequence_search_export_blockers(search_task: str) -> list[str]:
    blockers = [
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if search_task == "keep_sequence_holdout_control":
        blockers.insert(0, "sequence_holdout_control_not_resolved")
    else:
        blockers.insert(0, "complete_near_duplicate_reference_search_not_completed")
    return blockers


def _external_sequence_search_source_targets(
    *,
    accession: str,
    top_matches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = [
        {
            "source_type": "UniProtKB",
            "source_id": accession,
            "url": f"https://www.uniprot.org/uniprotkb/{accession}/entry",
            "purpose": "inspect candidate sequence and cross-references",
        },
        {
            "source_type": "UniRef",
            "source_id": accession,
            "url": f"https://www.uniprot.org/uniref?query={accession}",
            "purpose": "complete near-duplicate family search before import",
        },
    ]
    for match in top_matches:
        if not isinstance(match, dict):
            continue
        reference_accession = _normalize_accession(match.get("reference_accession"))
        if not reference_accession:
            continue
        targets.append(
            {
                "source_type": "UniProtKB",
                "source_id": reference_accession,
                "matched_m_csa_entry_ids": match.get("matched_m_csa_entry_ids", []),
                "near_duplicate_score": match.get("near_duplicate_score"),
                "url": (
                    "https://www.uniprot.org/uniprotkb/"
                    f"{reference_accession}/entry"
                ),
                "purpose": "inspect bounded-screen top hit as a sequence control",
            }
        )
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for target in targets:
        key = (str(target.get("source_type") or ""), str(target.get("source_id") or ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(target)
    return deduped


def _external_active_site_sourcing_queue_status(
    *,
    request_status: str,
    readiness_status: str,
    alignment_status: str | None,
) -> str:
    if (
        readiness_status == "blocked_by_sequence_holdout"
        or alignment_status == "alignment_near_duplicate_candidate_holdout"
    ):
        return "defer_sequence_holdout_before_sourcing"
    if request_status == "binding_context_mapped_ready_for_active_site_sourcing":
        return "ready_for_curated_active_site_sourcing"
    if request_status == "reaction_text_only_needs_curated_residue_source":
        return "needs_primary_active_site_source"
    if request_status:
        return f"defer_{request_status}"
    return "defer_missing_active_site_request_status"


def _external_active_site_sourcing_next_action(queue_status: str) -> str:
    if queue_status == "ready_for_curated_active_site_sourcing":
        return "source_catalytic_residue_positions_for_mapped_binding_context"
    if queue_status == "needs_primary_active_site_source":
        return "find_primary_active_site_or_residue_role_source"
    if queue_status == "defer_sequence_holdout_before_sourcing":
        return "keep_sequence_holdout_out_of_active_site_sourcing_batch"
    return "defer_until_required_context_is_available"


def _external_active_site_sourcing_task(queue_status: str) -> str:
    if queue_status == "ready_for_curated_active_site_sourcing":
        return "curate_active_site_positions_from_mapped_binding_context"
    if queue_status == "needs_primary_active_site_source":
        return "find_primary_active_site_or_residue_role_source"
    if queue_status == "defer_sequence_holdout_before_sourcing":
        return "defer_until_sequence_holdout_resolved"
    return "defer_until_required_context_is_available"


def _external_active_site_sourcing_export_blockers(queue_status: str) -> list[str]:
    blockers = [
        "explicit_active_site_residue_sources_not_collected",
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if queue_status == "defer_sequence_holdout_before_sourcing":
        blockers.insert(0, "sequence_holdout_unresolved")
    elif queue_status == "needs_primary_active_site_source":
        blockers.insert(0, "primary_active_site_source_required")
    elif queue_status != "ready_for_curated_active_site_sourcing":
        blockers.insert(0, "active_site_sourcing_context_incomplete")
    return blockers


def _external_binding_feature_positions(
    binding_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    positions = []
    for row in binding_rows:
        if not isinstance(row, dict):
            continue
        positions.append(
            {
                "begin": row.get("begin"),
                "end": row.get("end"),
                "ligand_id": row.get("ligand_id"),
                "ligand_name": row.get("ligand_name"),
                "evidence": row.get("evidence", []),
            }
        )
    return positions


def _external_active_site_source_targets(
    *,
    accession: str,
    summary: dict[str, Any],
    request: dict[str, Any],
    reaction_context: dict[str, Any],
) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = [
        {
            "source_type": "UniProtKB",
            "source_id": accession,
            "url": f"https://www.uniprot.org/uniprotkb/{accession}/entry",
            "purpose": "inspect feature table, catalytic activity, and evidence links",
        }
    ]
    for pdb_id in (request.get("pdb_ids_sample") or summary.get("pdb_ids_sample") or [])[:10]:
        if not pdb_id:
            continue
        targets.append(
            {
                "source_type": "PDB",
                "source_id": pdb_id,
                "url": f"https://www.rcsb.org/structure/{pdb_id}",
                "purpose": "inspect structure evidence for catalytic residue positions",
            }
        )
    for alphafold_id in (
        request.get("alphafold_ids_sample")
        or summary.get("alphafold_ids_sample")
        or []
    )[:5]:
        if not alphafold_id:
            continue
        targets.append(
            {
                "source_type": "AlphaFoldDB",
                "source_id": alphafold_id,
                "url": f"https://alphafold.ebi.ac.uk/entry/{accession}",
                "purpose": "map sourced residue positions after curated evidence exists",
            }
        )
    for ref in request.get("binding_evidence_references", []) or []:
        if not isinstance(ref, dict):
            continue
        source = str(ref.get("source") or "")
        source_id = str(ref.get("id") or "")
        if not source or not source_id:
            continue
        target = {
            "source_type": source,
            "source_id": source_id,
            "ligand_name": ref.get("ligand_name"),
            "purpose": "inspect binding-context source for catalytic residue evidence",
        }
        if source == "PubMed":
            target["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{source_id}/"
        elif source == "PDB":
            target["url"] = f"https://www.rcsb.org/structure/{source_id}"
        elif source == "UniProtKB":
            target["url"] = f"https://www.uniprot.org/uniprotkb/{source_id}/entry"
        targets.append(target)
    for rhea_id in reaction_context.get("rhea_ids", [])[:10]:
        targets.append(
            {
                "source_type": "Rhea",
                "source_id": rhea_id,
                "url": f"https://www.rhea-db.org/rhea/{str(rhea_id).removeprefix('RHEA:')}",
                "purpose": "check reaction context only; not active-site residue evidence",
            }
        )
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for target in targets:
        key = (str(target.get("source_type") or ""), str(target.get("source_id") or ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(target)
    return deduped


def _external_active_site_sourcing_priority_score(
    *,
    queue_status: str,
    mapped_binding_position_count: int,
    binding_evidence_reference_count: int,
) -> float:
    if queue_status == "defer_sequence_holdout_before_sourcing":
        return 0.0
    if queue_status == "ready_for_curated_active_site_sourcing":
        return 10.0 + min(mapped_binding_position_count, 10) + min(
            binding_evidence_reference_count, 5
        )
    if queue_status == "needs_primary_active_site_source":
        return 5.0
    return 1.0


def _external_import_readiness_blockers(
    *,
    manifest_row: dict[str, Any],
    active_site: dict[str, Any] | None,
    heuristic: dict[str, Any] | None,
    representation: dict[str, Any] | None,
    active_site_gap: dict[str, Any] | None,
    sequence: dict[str, Any] | None,
    sequence_alignment: list[dict[str, Any]] | None,
) -> list[str]:
    blockers: list[str] = []
    sequence_status = str((sequence or {}).get("screen_status") or "")
    if sequence_status == "preexisting_sequence_holdout_retained":
        blockers.append("exact_sequence_holdout")
    elif sequence_status == "near_duplicate_candidate_holdout":
        blockers.append("near_duplicate_candidate_holdout")
    elif sequence_status:
        blockers.append("complete_near_duplicate_search_required")
    else:
        blockers.append("sequence_neighborhood_screen_missing")
    alignment_status = _external_sequence_alignment_status(sequence_alignment)
    if alignment_status == "alignment_near_duplicate_candidate_holdout":
        blockers.append("sequence_alignment_near_duplicate_candidate_holdout")
    elif alignment_status in {
        "sequence_missing_for_alignment",
        "alignment_deferred_pair_too_large",
    }:
        blockers.append("sequence_alignment_verification_incomplete")

    if active_site is None:
        blockers.append("external_active_site_evidence_not_sampled")
    elif int(active_site.get("active_site_feature_count", 0) or 0) == 0:
        blockers.append("external_active_site_feature_gap")
    if active_site_gap is not None:
        request_status = str(active_site_gap.get("request_status") or "")
        blockers.append(f"active_site_gap_source_request:{request_status}")

    if heuristic is None:
        blockers.append("heuristic_control_not_scored")
    elif heuristic.get("scope_top1_mismatch"):
        blockers.append("heuristic_scope_top1_mismatch")
    top1 = _external_top1_fingerprint(heuristic or {})
    if top1 == "metal_dependent_hydrolase" and str(
        manifest_row.get("scope_signal") or ""
    ) != "hydrolysis":
        blockers.append("heuristic_metal_hydrolase_collapse")

    if representation is None:
        blockers.append("representation_control_not_compared")
    else:
        comparison_status = str(representation.get("comparison_status") or "")
        if comparison_status != "proxy_consistent_with_heuristic_scope":
            blockers.append(f"representation_control_{comparison_status}")

    blockers.extend(
        [
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ]
    )
    return blockers


def _external_import_readiness_status(blockers: list[str]) -> str:
    if any(
        blocker in blockers
        for blocker in (
            "exact_sequence_holdout",
            "near_duplicate_candidate_holdout",
            "sequence_alignment_near_duplicate_candidate_holdout",
        )
    ):
        return "blocked_by_sequence_holdout"
    if any(blocker.startswith("active_site_gap_source_request") for blocker in blockers):
        return "blocked_by_active_site_sourcing"
    if "external_active_site_feature_gap" in blockers:
        return "blocked_by_active_site_gap"
    if any(
        blocker in blockers
        for blocker in (
            "heuristic_scope_top1_mismatch",
            "heuristic_metal_hydrolase_collapse",
        )
    ):
        return "blocked_by_heuristic_control"
    if any(blocker.startswith("representation_control_") for blocker in blockers):
        return "blocked_by_representation_control"
    if "complete_near_duplicate_search_required" in blockers:
        return "blocked_by_sequence_search"
    return "blocked_by_review_decision_and_factory_gate"


def _external_import_readiness_next_action(blockers: list[str]) -> str:
    if any(
        blocker in blockers
        for blocker in (
            "exact_sequence_holdout",
            "near_duplicate_candidate_holdout",
            "sequence_alignment_near_duplicate_candidate_holdout",
        )
    ):
        return "keep_sequence_holdout_out_of_import_batch"
    if any(blocker.startswith("active_site_gap_source_request") for blocker in blockers):
        return "source_explicit_active_site_residue_positions"
    if "external_active_site_feature_gap" in blockers:
        return "resolve_active_site_feature_gap_before_mapping"
    if any(
        blocker in blockers
        for blocker in (
            "heuristic_scope_top1_mismatch",
            "heuristic_metal_hydrolase_collapse",
        )
    ):
        return "repair_heuristic_or_ontology_control_before_decision"
    if any(blocker.startswith("representation_control_") for blocker in blockers):
        return "compute_or_attach_real_representation_control"
    if "complete_near_duplicate_search_required" in blockers:
        return "complete_near_duplicate_sequence_search"
    return "build_review_decisions_only_after_factory_gates"


def _external_transfer_blocker_matrix_blockers(
    *,
    readiness: dict[str, Any],
    active_site: dict[str, Any] | None,
    sequence: dict[str, Any] | None,
    backend: dict[str, Any] | None,
) -> list[str]:
    blockers: list[str] = []
    blockers.extend(str(blocker) for blocker in readiness.get("blockers", []) or [])
    if active_site is not None:
        blockers.extend(
            str(blocker) for blocker in active_site.get("blockers", []) or []
        )
    if sequence is not None:
        blockers.extend(str(blocker) for blocker in sequence.get("blockers", []) or [])
    else:
        blockers.append("sequence_search_export_missing")
    if backend is not None:
        blockers.extend(str(blocker) for blocker in backend.get("blockers", []) or [])
    else:
        blockers.append("representation_backend_plan_missing_or_not_eligible")
    blockers.extend(
        [
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ]
    )
    deduped: list[str] = []
    seen: set[str] = set()
    for blocker in blockers:
        if not blocker or blocker in seen:
            continue
        seen.add(blocker)
        deduped.append(blocker)
    return deduped


def _external_transfer_blocker_matrix_next_action(
    *,
    readiness: dict[str, Any],
    active_site: dict[str, Any] | None,
    sequence: dict[str, Any] | None,
    backend: dict[str, Any] | None,
) -> str:
    if active_site is not None:
        source_task = str(active_site.get("source_task") or "")
        if source_task == "find_primary_active_site_or_residue_role_source":
            return "find_primary_active_site_or_residue_role_source"
        if source_task:
            return "complete_active_site_source_review_packet"
    search_task = str((sequence or {}).get("search_task") or "")
    if search_task == "keep_sequence_holdout_control":
        return "keep_sequence_holdout_out_of_import_batch"
    if search_task:
        return "complete_near_duplicate_sequence_search"
    if backend is not None:
        return "select_and_run_real_representation_backend"
    return str(
        readiness.get("next_action")
        or "complete_external_review_prerequisites_before_decision"
    )


def _external_transfer_blocker_matrix_active_site(
    active_site: dict[str, Any] | None,
) -> dict[str, Any]:
    if active_site is None:
        return {
            "source_task": "not_active_site_sourcing_row",
            "decision_status": None,
            "source_target_count": 0,
        }
    return {
        "source_task": active_site.get("source_task"),
        "decision_status": (active_site.get("decision") or {}).get("decision_status"),
        "queue_status": active_site.get("queue_status"),
        "source_target_count": len(active_site.get("source_targets", []) or []),
    }


def _external_transfer_blocker_matrix_sequence(
    sequence: dict[str, Any] | None,
) -> dict[str, Any]:
    if sequence is None:
        return {
            "search_task": None,
            "decision_status": None,
            "source_target_count": 0,
        }
    return {
        "alignment_status": sequence.get("alignment_status"),
        "decision_status": (sequence.get("decision") or {}).get("decision_status"),
        "search_task": sequence.get("search_task"),
        "source_target_count": len(sequence.get("source_targets", []) or []),
    }


def _external_transfer_blocker_matrix_backend(
    backend: dict[str, Any] | None,
) -> dict[str, Any]:
    if backend is None:
        return {
            "backend_readiness_status": "not_backend_eligible_yet",
            "embedding_status": "not_planned",
            "recommended_backend_count": 0,
            "required_input_count": 0,
        }
    return {
        "backend_readiness_status": backend.get("backend_readiness_status"),
        "embedding_status": backend.get("embedding_status"),
        "recommended_backend_count": len(backend.get("recommended_backends", []) or []),
        "required_input_count": len(backend.get("required_inputs", []) or []),
        "sequence_search_task": backend.get("sequence_search_task"),
    }
