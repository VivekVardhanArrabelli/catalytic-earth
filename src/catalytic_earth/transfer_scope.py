from __future__ import annotations

import json
import re
import hashlib
import os
import shlex
import shutil
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
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
UNIPROT_ENTRY_URL = "https://rest.uniprot.org/uniprotkb"
REPRESENTATION_PREDICTIVE_FEATURE_SOURCES = (
    "sequence_embedding_cosine",
    "sequence_length_coverage",
)
REPRESENTATION_REVIEW_CONTEXT_FIELDS = (
    "heuristic_baseline_control",
    "nearest_reference",
    "scope_signal",
    "sequence_search_task",
)
EXTERNAL_PILOT_IMPORT_REVIEW_REQUIREMENTS = (
    "curated_active_site_residue_evidence",
    "specific_reaction_or_mechanism_evidence",
    "complete_near_duplicate_sequence_search",
    "leakage_safe_representation_control",
    "review_decision",
    "full_label_factory_gate",
)
REPRESENTATION_LEAKAGE_PRONE_PREDICTIVE_TERMS = (
    "accession",
    "ec",
    "entry_id",
    "fingerprint",
    "label",
    "mechanism",
    "rhea",
    "scope_signal",
    "source_target",
    "text",
)
DEFAULT_ESM2_BACKEND = "esm2_t6_8m_ur50d"
ESM2_BACKEND_MODEL_NAMES = {
    "esm2_t6_8m_ur50d": "facebook/esm2_t6_8M_UR50D",
    "esm2_t12_35m_ur50d": "facebook/esm2_t12_35M_UR50D",
    "esm2_t30_150m_ur50d": "facebook/esm2_t30_150M_UR50D",
    "esm2_t33_650m_ur50d": "facebook/esm2_t33_650M_UR50D",
}
ESM2_BACKEND_EXPECTED_DIMENSIONS = {
    "esm2_t6_8m_ur50d": 320,
    "esm2_t12_35m_ur50d": 480,
    "esm2_t30_150m_ur50d": 640,
    "esm2_t33_650m_ur50d": 1280,
}
ESM2_BACKEND_SCALE_LABELS = {
    "esm2_t6_8m_ur50d": "8M",
    "esm2_t12_35m_ur50d": "35M",
    "esm2_t30_150m_ur50d": "150M",
    "esm2_t33_650m_ur50d": "650M",
}
ESM2_BACKEND_FALLBACK_ORDER = (
    "esm2_t33_650m_ur50d",
    "esm2_t30_150m_ur50d",
    "esm2_t12_35m_ur50d",
    "esm2_t6_8m_ur50d",
)
ESM2_BACKEND_WEIGHT_FILENAMES = (
    "model.safetensors",
    "pytorch_model.bin",
    "tf_model.h5",
    "flax_model.msgpack",
)
EXTERNAL_TRANSFER_GATE_INPUT_CONTRACT = "ExternalSourceTransferGateInputs.v1"
EXTERNAL_TRANSFER_GATE_REQUIRED_FIELDS = (
    "transfer_manifest",
    "query_manifest",
    "ood_calibration_plan",
    "candidate_sample_audit",
    "candidate_manifest",
    "candidate_manifest_audit",
    "lane_balance_audit",
    "evidence_plan",
    "evidence_request_export",
    "review_only_import_safety_audit",
)
EXTERNAL_TRANSFER_CANDIDATE_LINEAGE_FIELDS = (
    "evidence_plan",
    "evidence_request_export",
    "active_site_evidence_queue",
    "active_site_evidence_sample",
    "heuristic_control_queue",
    "structure_mapping_plan",
    "structure_mapping_sample",
    "heuristic_control_scores",
    "external_control_repair_plan",
    "reaction_evidence_sample",
    "representation_control_manifest",
    "representation_control_comparison",
    "representation_backend_plan",
    "representation_backend_sample",
    "active_site_gap_source_requests",
    "sequence_neighborhood_plan",
    "sequence_neighborhood_sample",
    "sequence_alignment_verification",
    "sequence_reference_screen_audit",
    "sequence_search_export",
    "sequence_backend_search",
    "external_import_readiness_audit",
    "active_site_sourcing_queue",
    "active_site_sourcing_export",
    "active_site_sourcing_resolution",
    "transfer_blocker_matrix",
    "pilot_candidate_priority",
    "pilot_review_decision_export",
    "pilot_evidence_packet",
    "pilot_evidence_dossiers",
    "pilot_active_site_evidence_decisions",
    "pilot_representation_backend_sample",
    "binding_context_repair_plan",
    "binding_context_mapping_sample",
    "sequence_holdout_audit",
)
_EXTERNAL_TRANSFER_ARTIFACT_SLICE_RE = re.compile(
    r"_(\d+)(?=(?:_[A-Za-z0-9]+)*\.json$)"
)
_EXTERNAL_TRANSFER_PAYLOAD_LINEAGE_KEYS = (
    "slice_id",
    "source_slice_id",
    "target_slice_id",
    "label_slice_id",
    "batch_id",
    "label_batch_id",
)


@dataclass(frozen=True)
class ExternalSourceTransferGateInputs:
    transfer_manifest: dict[str, Any]
    query_manifest: dict[str, Any]
    ood_calibration_plan: dict[str, Any]
    candidate_sample_audit: dict[str, Any]
    candidate_manifest: dict[str, Any]
    candidate_manifest_audit: dict[str, Any]
    lane_balance_audit: dict[str, Any]
    evidence_plan: dict[str, Any]
    evidence_request_export: dict[str, Any]
    review_only_import_safety_audit: dict[str, Any]
    active_site_evidence_queue: dict[str, Any] | None = None
    active_site_evidence_sample: dict[str, Any] | None = None
    active_site_evidence_sample_audit: dict[str, Any] | None = None
    heuristic_control_queue: dict[str, Any] | None = None
    heuristic_control_queue_audit: dict[str, Any] | None = None
    structure_mapping_plan: dict[str, Any] | None = None
    structure_mapping_plan_audit: dict[str, Any] | None = None
    structure_mapping_sample: dict[str, Any] | None = None
    structure_mapping_sample_audit: dict[str, Any] | None = None
    heuristic_control_scores: dict[str, Any] | None = None
    heuristic_control_scores_audit: dict[str, Any] | None = None
    external_failure_mode_audit: dict[str, Any] | None = None
    external_control_repair_plan: dict[str, Any] | None = None
    external_control_repair_plan_audit: dict[str, Any] | None = None
    reaction_evidence_sample: dict[str, Any] | None = None
    reaction_evidence_sample_audit: dict[str, Any] | None = None
    representation_control_manifest: dict[str, Any] | None = None
    representation_control_manifest_audit: dict[str, Any] | None = None
    representation_control_comparison: dict[str, Any] | None = None
    representation_control_comparison_audit: dict[str, Any] | None = None
    representation_backend_plan: dict[str, Any] | None = None
    representation_backend_plan_audit: dict[str, Any] | None = None
    representation_backend_sample: dict[str, Any] | None = None
    representation_backend_sample_audit: dict[str, Any] | None = None
    broad_ec_disambiguation_audit: dict[str, Any] | None = None
    active_site_gap_source_requests: dict[str, Any] | None = None
    sequence_neighborhood_plan: dict[str, Any] | None = None
    sequence_neighborhood_sample: dict[str, Any] | None = None
    sequence_neighborhood_sample_audit: dict[str, Any] | None = None
    sequence_alignment_verification: dict[str, Any] | None = None
    sequence_alignment_verification_audit: dict[str, Any] | None = None
    sequence_reference_screen_audit: dict[str, Any] | None = None
    sequence_search_export: dict[str, Any] | None = None
    sequence_search_export_audit: dict[str, Any] | None = None
    sequence_backend_search: dict[str, Any] | None = None
    external_import_readiness_audit: dict[str, Any] | None = None
    active_site_sourcing_queue: dict[str, Any] | None = None
    active_site_sourcing_queue_audit: dict[str, Any] | None = None
    active_site_sourcing_export: dict[str, Any] | None = None
    active_site_sourcing_export_audit: dict[str, Any] | None = None
    active_site_sourcing_resolution: dict[str, Any] | None = None
    active_site_sourcing_resolution_audit: dict[str, Any] | None = None
    transfer_blocker_matrix: dict[str, Any] | None = None
    transfer_blocker_matrix_audit: dict[str, Any] | None = None
    pilot_candidate_priority: dict[str, Any] | None = None
    pilot_review_decision_export: dict[str, Any] | None = None
    pilot_evidence_packet: dict[str, Any] | None = None
    pilot_evidence_dossiers: dict[str, Any] | None = None
    pilot_active_site_evidence_decisions: dict[str, Any] | None = None
    pilot_representation_backend_sample: dict[str, Any] | None = None
    binding_context_repair_plan: dict[str, Any] | None = None
    binding_context_repair_plan_audit: dict[str, Any] | None = None
    binding_context_mapping_sample: dict[str, Any] | None = None
    binding_context_mapping_sample_audit: dict[str, Any] | None = None
    sequence_holdout_audit: dict[str, Any] | None = None
    artifact_path_lineage: dict[str, Any] | None = None

    def candidate_lineage_artifacts(self) -> dict[str, dict[str, Any] | None]:
        return {
            field_name: getattr(self, field_name)
            for field_name in EXTERNAL_TRANSFER_CANDIDATE_LINEAGE_FIELDS
        }


def validate_external_source_transfer_gate_inputs(
    gate_inputs: ExternalSourceTransferGateInputs,
) -> None:
    required_non_objects = sorted(
        field_name
        for field_name in EXTERNAL_TRANSFER_GATE_REQUIRED_FIELDS
        if not isinstance(getattr(gate_inputs, field_name), dict)
    )
    optional_non_objects = sorted(
        field_name
        for field_name in ExternalSourceTransferGateInputs.__dataclass_fields__
        if field_name not in EXTERNAL_TRANSFER_GATE_REQUIRED_FIELDS
        and field_name != "artifact_path_lineage"
        and getattr(gate_inputs, field_name) is not None
        and not isinstance(getattr(gate_inputs, field_name), dict)
    )
    if required_non_objects:
        raise ValueError(
            "external transfer gate required inputs must be JSON objects: "
            + ", ".join(required_non_objects)
        )
    if optional_non_objects:
        raise ValueError(
            "external transfer gate optional inputs must be JSON objects when present: "
            + ", ".join(optional_non_objects)
        )
    if (
        gate_inputs.artifact_path_lineage is not None
        and not isinstance(gate_inputs.artifact_path_lineage, dict)
    ):
        raise ValueError(
            "external transfer gate artifact_path_lineage must be a JSON object"
        )


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


def build_external_source_pilot_representation_backend_plan(
    *,
    pilot_candidate_priority: dict[str, Any],
    sequence_search_export: dict[str, Any],
    max_rows: int = 10,
) -> dict[str, Any]:
    """Plan sequence-embedding controls for selected pilot rows."""
    sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_search_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    missing_sequence_export: list[str] = []
    for priority_row in pilot_candidate_priority.get("rows", []) or []:
        if not isinstance(priority_row, dict):
            continue
        if (
            priority_row.get("pilot_selection_status")
            != "selected_for_review_pilot"
        ):
            continue
        accession = _normalize_accession(priority_row.get("accession"))
        if not accession:
            continue
        if len(rows) >= max_rows:
            break
        sequence = sequence_by_accession.get(accession, {})
        if not sequence:
            missing_sequence_export.append(accession)
        sequence_search_context = priority_row.get("sequence_search", {})
        if not isinstance(sequence_search_context, dict):
            sequence_search_context = {}
        sequence_task = (
            sequence.get("search_task")
            or sequence_search_context.get("search_task")
            or "missing_sequence_search_export"
        )
        scope_signal = _external_pilot_scope_signal(priority_row)
        comparison_status = _external_pilot_representation_comparison_status(
            priority_row
        )
        readiness_status = _external_pilot_representation_backend_status(
            sequence_task
        )
        status_counts[readiness_status] += 1
        entry_id = priority_row.get("entry_id") or f"uniprot:{accession}"
        heuristic_status = (
            "required_missing"
            if "heuristic_control_not_scored"
            in set(priority_row.get("blockers", []) or [])
            else "required_attached"
        )
        rows.append(
            {
                "accession": accession,
                "backend_readiness_status": readiness_status,
                "blockers": _external_representation_backend_blockers(
                    readiness_status
                ),
                "comparison_status": comparison_status,
                "countable_label_candidate": False,
                "embedding_status": "backend_plan_only_not_computed",
                "entry_id": entry_id,
                "feature_summary": {
                    "pilot_priority_score": priority_row.get("pilot_priority_score"),
                    "pilot_selection_status": priority_row.get(
                        "pilot_selection_status"
                    ),
                },
                "heuristic_baseline_control": {
                    "scope_top1_mismatch": (
                        "heuristic_scope_top1_mismatch"
                        in set(priority_row.get("blockers", []) or [])
                    ),
                    "top1_fingerprint_id": None,
                    "top1_score": None,
                },
                "lane_id": priority_row.get("lane_id"),
                "pilot_representation_control": True,
                "ready_for_label_import": False,
                "recommended_backends": _external_representation_backend_options(
                    scope_signal=scope_signal,
                    comparison_status=comparison_status,
                ),
                "required_inputs": [
                    {
                        "input_type": "candidate_sequence",
                        "status": "required_not_embedded",
                        "source_id": accession,
                    },
                    {
                        "input_type": "sequence_search_control",
                        "status": sequence_task,
                        "source_id": accession,
                    },
                    {
                        "input_type": "heuristic_baseline_scores",
                        "status": heuristic_status,
                        "source_id": entry_id,
                    },
                ],
                "review_status": "representation_backend_plan_review_only",
                "scope_signal": scope_signal,
                "sequence_search_task": sequence_task,
            }
        )

    blockers: list[str] = []
    if missing_sequence_export:
        blockers.append("pilot_representation_sequence_search_export_missing")
    return {
        "metadata": {
            "method": "external_source_pilot_representation_backend_plan",
            "blocker_removed": "external_pilot_representation_sample_coverage",
            "source_pilot_candidate_priority_method": pilot_candidate_priority.get(
                "metadata", {}
            ).get("method"),
            "source_sequence_search_export_method": sequence_search_export.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "selected_candidate_count": pilot_candidate_priority.get(
                "metadata", {}
            ).get("selected_candidate_count", len(rows)),
            "max_rows": max_rows,
            "embedding_status": "backend_plan_only_not_computed",
            "backend_readiness_status_counts": dict(sorted(status_counts.items())),
            "sequence_search_blocked_count": sum(
                1
                for row in rows
                if row["backend_readiness_status"]
                == "blocked_until_sequence_search_complete"
            ),
            "heuristic_baseline_missing_count": sum(
                1
                for row in rows
                for item in row.get("required_inputs", [])
                if item.get("input_type") == "heuristic_baseline_scores"
                and item.get("status") == "required_missing"
            ),
            "missing_sequence_export_accessions": sorted(missing_sequence_export),
            "review_only_rule": (
                "pilot representation plans compute sequence-embedding controls "
                "only; they do not replace heuristic controls, sequence-search "
                "completion, review decisions, or label-factory gates"
            ),
        },
        "rows": rows,
        "blockers": blockers
        + [
            "external_embeddings_not_computed",
            "representation_backend_not_selected",
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "pilot representation plans are review-only and cannot authorize "
                "countable external label import"
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


def build_external_source_representation_backend_sample(
    *,
    representation_backend_plan: dict[str, Any],
    sequence_neighborhood_sample: dict[str, Any],
    max_rows: int = 100,
    top_k: int = 3,
    similarity_alert_threshold: float = 0.95,
    embedding_backend: str = "deterministic_sequence_kmer_control",
    model_name: str = ESM2_BACKEND_MODEL_NAMES[DEFAULT_ESM2_BACKEND],
    local_files_only: bool = False,
    fallback_to_largest_local_esm2: bool = True,
    allow_larger_model_smoke: bool = False,
    larger_model_smoke_accession_limit: int = 2,
    fetcher: Callable[[list[str]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute a review-only sequence representation control."""
    sample_started = time.perf_counter()
    fetch = fetcher or _fetch_uniprot_sequence_records
    sequence_rows_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_neighborhood_sample.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    plan_rows = [
        row
        for row in representation_backend_plan.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    ][:max_rows]
    candidate_accessions = [
        _normalize_accession(row.get("accession")) for row in plan_rows
    ]
    reference_accessions = sorted(
        {
            _normalize_accession(match.get("reference_accession"))
            for accession in candidate_accessions
            for match in (
                sequence_rows_by_accession.get(accession, {}).get("top_matches", [])
                or []
            )[:top_k]
            if isinstance(match, dict)
            and _normalize_accession(match.get("reference_accession"))
        }
    )
    requested_accessions = sorted(set(candidate_accessions) | set(reference_accessions))
    fetch_failures: list[dict[str, str]] = []
    try:
        sequence_payload = fetch(requested_accessions)
    except Exception as exc:  # pragma: no cover - live network failure path
        sequence_payload = {"metadata": {}, "records": []}
        fetch_failures.append({"error_type": type(exc).__name__, "error": str(exc)})
    records_by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in sequence_payload.get("records", []) or []
        if isinstance(record, dict) and _normalize_accession(record.get("accession"))
    }
    embedding_payload = _compute_sequence_embedding_payload(
        records_by_accession=records_by_accession,
        accessions=requested_accessions,
        embedding_backend=embedding_backend,
        model_name=model_name,
        local_files_only=local_files_only,
        fallback_to_largest_local_esm2=fallback_to_largest_local_esm2,
        allow_larger_model_smoke=allow_larger_model_smoke,
        larger_model_smoke_accession_limit=larger_model_smoke_accession_limit,
    )
    embeddings_by_accession = embedding_payload["embeddings_by_accession"]

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    alert_count = 0
    reference_pair_count = 0
    learned_complete_count = 0
    disagreement_rows: list[dict[str, Any]] = []
    for plan_row in plan_rows:
        accession = _normalize_accession(plan_row.get("accession"))
        sequence_row = sequence_rows_by_accession.get(accession, {})
        candidate_sequence = _clean_sequence(
            records_by_accession.get(accession, {}).get("sequence")
        )
        candidate_embedding = embeddings_by_accession.get(accession)
        reference_scores: list[dict[str, Any]] = []
        for match in (sequence_row.get("top_matches", []) or [])[:top_k]:
            if not isinstance(match, dict):
                continue
            reference_accession = _normalize_accession(match.get("reference_accession"))
            reference_sequence = _clean_sequence(
                records_by_accession.get(reference_accession, {}).get("sequence")
            )
            if not reference_accession or not reference_sequence or not candidate_embedding:
                continue
            score = _embedding_cosine_similarity(
                candidate_embedding,
                embeddings_by_accession.get(reference_accession),
            )
            reference_scores.append(
                {
                    "embedding_cosine": round(score, 4),
                    "embedding_backend": embedding_payload["metadata"]["embedding_backend"],
                    "length_coverage": round(
                        _sequence_length_coverage(candidate_sequence, reference_sequence),
                        4,
                    ),
                    "matched_m_csa_entry_ids": match.get("matched_m_csa_entry_ids", []),
                    "reference_accession": reference_accession,
                    "screen_near_duplicate_score": match.get("near_duplicate_score"),
                }
            )
        reference_scores.sort(
            key=lambda item: (
                -float(item.get("embedding_cosine", 0.0) or 0.0),
                str(item.get("reference_accession") or ""),
            )
        )
        best_score = (
            float(reference_scores[0].get("embedding_cosine", 0.0) or 0.0)
            if reference_scores
            else 0.0
        )
        leakage_flags = _external_representation_sample_leakage_flags(
            plan_row=plan_row,
            reference_scores=reference_scores,
        )
        status = _external_representation_backend_sample_status(
            candidate_sequence=candidate_sequence,
            reference_scores=reference_scores,
            backend_readiness_status=str(
                plan_row.get("backend_readiness_status") or ""
            ),
            embedding_backend=embedding_payload["metadata"]["embedding_backend"],
            similarity_alert_threshold=similarity_alert_threshold,
        )
        if (
            embedding_payload["metadata"]["embedding_backend"]
            != "deterministic_sequence_kmer_control"
            and not embedding_payload["metadata"].get("embedding_backend_available")
        ):
            status = "embedding_backend_unavailable"
        status_counts[status] += 1
        if status == "representation_near_duplicate_holdout":
            alert_count += 1
        if status == "learned_representation_sample_complete":
            learned_complete_count += 1
        reference_pair_count += len(reference_scores)
        heuristic_top1 = (
            plan_row.get("heuristic_baseline_control", {}) or {}
        ).get("top1_fingerprint_id")
        nearest_reference_entry_ids = (
            (reference_scores[0] if reference_scores else {}).get(
                "matched_m_csa_entry_ids", []
            )
            or []
        )
        disagreement_status = _representation_heuristic_disagreement_status(
            heuristic_top1=heuristic_top1,
            representation_status=status,
            nearest_reference_entry_ids=nearest_reference_entry_ids,
            plan_row=plan_row,
        )
        if disagreement_status != "no_disagreement_signal":
            disagreement_rows.append(
                {
                    "accession": accession,
                    "entry_id": plan_row.get("entry_id") or f"uniprot:{accession}",
                    "heuristic_top1_fingerprint_id": heuristic_top1,
                    "learned_or_proxy_backend_status": status,
                    "leakage_flags": leakage_flags,
                    "nearest_reference_entry_ids": nearest_reference_entry_ids,
                    "representation_heuristic_disagreement_status": disagreement_status,
                    "top_embedding_cosine": round(best_score, 4),
                }
            )
        rows.append(
            {
                "accession": accession,
                "backend_status": status,
                "blockers": _external_representation_backend_sample_blockers(
                    status=status,
                    embedding_backend=embedding_payload["metadata"]["embedding_backend"],
                ),
                "candidate_sequence_length": len(candidate_sequence),
                "comparison_status": plan_row.get("comparison_status"),
                "countable_label_candidate": False,
                "embedding_backend": embedding_payload["metadata"]["embedding_backend"],
                "requested_embedding_backend": embedding_payload["metadata"].get(
                    "requested_embedding_backend", embedding_backend
                ),
                "computed_embedding_backend": embedding_payload["metadata"].get(
                    "computed_embedding_backend",
                    embedding_payload["metadata"].get("embedding_backend"),
                ),
                "fallback_used": embedding_payload["metadata"].get(
                    "fallback_used", False
                ),
                "fallback_reason": embedding_payload["metadata"].get(
                    "fallback_reason"
                ),
                "larger_model_readiness_status": (
                    "requested_backend_unavailable_fallback_used"
                    if embedding_payload["metadata"].get("fallback_used")
                    else embedding_payload["metadata"].get(
                        "backend_feasibility_status"
                    )
                ),
                "embedding_status": "computed_review_only",
                "embedding_vector_dimension": embedding_payload["metadata"].get(
                    "embedding_vector_dimension"
                ),
                "embedding_warning": embedding_payload["warnings_by_accession"].get(
                    accession
                ),
                "entry_id": plan_row.get("entry_id") or f"uniprot:{accession}",
                "heuristic_baseline_control": plan_row.get(
                    "heuristic_baseline_control", {}
                ),
                "lane_id": plan_row.get("lane_id"),
                "nearest_reference": reference_scores[0] if reference_scores else None,
                "leakage_flags": leakage_flags,
                "predictive_feature_sources": list(
                    REPRESENTATION_PREDICTIVE_FEATURE_SOURCES
                ),
                "ready_for_label_import": False,
                "reference_scores": reference_scores,
                "review_status": "representation_backend_sample_review_only",
                "review_context_fields": list(REPRESENTATION_REVIEW_CONTEXT_FIELDS),
                "scope_signal": plan_row.get("scope_signal"),
                "sequence_search_task": plan_row.get("sequence_search_task"),
                "top_embedding_cosine": round(best_score, 4),
            }
        )

    return {
        "metadata": {
            "method": "external_source_representation_backend_sample",
            "blocker_removed": (
                "computes a bounded learned or proxy representation sample "
                "for external pilot readiness while preserving heuristic "
                "geometry retrieval as the baseline"
            ),
            "source_representation_backend_plan_method": (
                representation_backend_plan.get("metadata", {}).get("method")
            ),
            "source_sequence_neighborhood_sample_method": (
                sequence_neighborhood_sample.get("metadata", {}).get("method")
            ),
            "source_fetch_method": sequence_payload.get("metadata", {}).get("source"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "top_k": top_k,
            "embedding_backend": embedding_payload["metadata"]["embedding_backend"],
            "requested_embedding_backend": embedding_payload["metadata"].get(
                "requested_embedding_backend", embedding_backend
            ),
            "computed_embedding_backend": embedding_payload["metadata"].get(
                "computed_embedding_backend",
                embedding_payload["metadata"].get("embedding_backend"),
            ),
            "model_name": embedding_payload["metadata"].get("model_name"),
            "requested_model_name": embedding_payload["metadata"].get(
                "requested_model_name", model_name
            ),
            "local_files_only": embedding_payload["metadata"].get("local_files_only"),
            "embedding_status": "computed_review_only",
            "predictive_feature_policy": (
                "representation status is computed from sequence embeddings "
                "and sequence length coverage only; identifiers, EC/Rhea, "
                "mechanism text, labels, and heuristic fingerprint ids are "
                "review context or holdout context only"
            ),
            "predictive_feature_sources": list(REPRESENTATION_PREDICTIVE_FEATURE_SOURCES),
            "review_context_fields": list(REPRESENTATION_REVIEW_CONTEXT_FIELDS),
            "embedding_backend_available": embedding_payload["metadata"].get(
                "embedding_backend_available"
            ),
            "embedding_vector_dimension": embedding_payload["metadata"].get(
                "embedding_vector_dimension"
            ),
            "embedding_failure_count": embedding_payload["metadata"].get(
                "embedding_failure_count",
                0,
            ),
            "embedding_elapsed_seconds": embedding_payload["metadata"].get(
                "embedding_elapsed_seconds"
            ),
            "model_load_elapsed_seconds": embedding_payload["metadata"].get(
                "model_load_elapsed_seconds"
            ),
            "model_load_status": embedding_payload["metadata"].get(
                "model_load_status"
            ),
            "model_load_failure_type": embedding_payload["metadata"].get(
                "model_load_failure_type"
            ),
            "model_load_failure": embedding_payload["metadata"].get(
                "model_load_failure"
            ),
            "backend_feasibility_status": embedding_payload["metadata"].get(
                "backend_feasibility_status"
            ),
            "expected_embedding_vector_dimension": embedding_payload["metadata"].get(
                "expected_embedding_vector_dimension"
            ),
            "embedding_backend_model_family": embedding_payload["metadata"].get(
                "embedding_backend_model_family"
            ),
            "embedding_backend_parameter_count": embedding_payload["metadata"].get(
                "embedding_backend_parameter_count"
            ),
            "attempted_embedding_backend": embedding_payload["metadata"].get(
                "attempted_embedding_backend"
            ),
            "requested_expected_embedding_vector_dimension": (
                embedding_payload["metadata"].get(
                    "requested_expected_embedding_vector_dimension"
                )
            ),
            "requested_embedding_backend_available": (
                embedding_payload["metadata"].get(
                    "requested_embedding_backend_available"
                )
            ),
            "requested_backend_feasibility_status": embedding_payload[
                "metadata"
            ].get("requested_backend_feasibility_status"),
            "requested_backend_local_cache_status": embedding_payload[
                "metadata"
            ].get("requested_backend_local_cache_status"),
            "requested_backend_weights_cached": embedding_payload["metadata"].get(
                "requested_backend_weights_cached"
            ),
            "requested_backend_cache_snapshot_count": embedding_payload[
                "metadata"
            ].get("requested_backend_cache_snapshot_count"),
            "requested_backend_smoke_status": embedding_payload["metadata"].get(
                "requested_backend_smoke_status"
            ),
            "requested_model_load_status": embedding_payload["metadata"].get(
                "requested_model_load_status"
            ),
            "requested_model_load_failure_type": embedding_payload["metadata"].get(
                "requested_model_load_failure_type"
            ),
            "requested_model_load_failure": embedding_payload["metadata"].get(
                "requested_model_load_failure"
            ),
            "requested_embedding_failure_count": embedding_payload["metadata"].get(
                "requested_embedding_failure_count"
            ),
            "fallback_used": embedding_payload["metadata"].get("fallback_used", False),
            "fallback_selected_backend": embedding_payload["metadata"].get(
                "fallback_selected_backend"
            ),
            "fallback_reason": embedding_payload["metadata"].get("fallback_reason"),
            "fallback_attempts": embedding_payload["metadata"].get(
                "fallback_attempts", []
            ),
            "blocker_not_removed": embedding_payload["metadata"].get(
                "blocker_not_removed"
            ),
            "largest_supported_embedding_backend": embedding_payload["metadata"].get(
                "largest_supported_embedding_backend"
            ),
            "largest_feasible_embedding_backend": embedding_payload["metadata"].get(
                "largest_feasible_embedding_backend"
            ),
            "fallback_not_computed_reason": embedding_payload["metadata"].get(
                "fallback_not_computed_reason"
            ),
            "requested_accession_count": len(requested_accessions),
            "fetched_accession_count": len(records_by_accession),
            "reference_pair_count": reference_pair_count,
            "similarity_alert_threshold": similarity_alert_threshold,
            "representation_near_duplicate_alert_count": alert_count,
            "learned_representation_complete_count": learned_complete_count,
            "learned_vs_heuristic_disagreement_count": len(disagreement_rows),
            "heuristic_contrast_required_count": sum(
                1
                for row in rows
                if (
                    row.get("heuristic_baseline_control", {}).get(
                        "scope_top1_mismatch"
                    )
                    or row.get("heuristic_baseline_control", {}).get(
                        "top1_fingerprint_id"
                    )
                    == "metal_dependent_hydrolase"
                )
            ),
            "fetch_failure_count": len(fetch_failures),
            "backend_status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "computed representation samples are controls only; they do "
                "not replace sequence-search, review-decision, or factory gates"
            ),
            "elapsed_seconds": round(time.perf_counter() - sample_started, 4),
        },
        "rows": rows,
        "learned_vs_heuristic_disagreements": disagreement_rows,
        "fetch_failures": fetch_failures,
        "embedding_failures": embedding_payload["embedding_failures"],
        "requested_embedding_failures": embedding_payload.get(
            "requested_embedding_failures", []
        ),
        "blockers": [
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            *embedding_payload["warnings"],
            "computed representation controls are not expert evidence",
        ],
    }


def _external_representation_sample_leakage_flags(
    *,
    plan_row: dict[str, Any],
    reference_scores: list[dict[str, Any]],
) -> list[str]:
    flags: list[str] = []
    heuristic_control = plan_row.get("heuristic_baseline_control", {})
    if isinstance(heuristic_control, dict) and heuristic_control.get("top1_fingerprint_id"):
        flags.append("heuristic_fingerprint_id_review_context_only")
    if any(score.get("matched_m_csa_entry_ids") for score in reference_scores):
        flags.append("matched_m_csa_reference_ids_holdout_context_only")
    if plan_row.get("scope_signal"):
        flags.append("source_scope_signal_review_context_only")
    return sorted(set(flags))


def audit_external_source_representation_backend_sample(
    representation_backend_sample: dict[str, Any],
) -> dict[str, Any]:
    """Verify computed representation backend samples remain review-only."""
    rows = [
        row
        for row in representation_backend_sample.get("rows", []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_backend_status = [row for row in rows if not row.get("backend_status")]
    missing_review_status = [
        row
        for row in rows
        if row.get("review_status") != "representation_backend_sample_review_only"
    ]
    missing_predictive_sources = [
        row
        for row in rows
        if row.get("predictive_feature_sources")
        != list(REPRESENTATION_PREDICTIVE_FEATURE_SOURCES)
    ]
    leakage_context_unmarked = [
        row
        for row in rows
        if (
            (row.get("heuristic_baseline_control") or row.get("nearest_reference"))
            and not row.get("leakage_flags")
        )
    ]
    metadata = representation_backend_sample.get("metadata", {})
    embedding_backend = metadata.get("embedding_backend")
    requested_backend = metadata.get("requested_embedding_backend")
    esm2_metadata_required = (
        embedding_backend in ESM2_BACKEND_MODEL_NAMES
        or requested_backend in ESM2_BACKEND_MODEL_NAMES
    )
    missing_availability_metadata: list[str] = []
    if esm2_metadata_required:
        for field_name in (
            "backend_feasibility_status",
            "expected_embedding_vector_dimension",
            "embedding_elapsed_seconds",
            "model_load_status",
            "requested_embedding_backend",
            "requested_expected_embedding_vector_dimension",
            "requested_backend_feasibility_status",
            "requested_backend_local_cache_status",
            "requested_backend_smoke_status",
            "requested_embedding_failure_count",
            "fallback_used",
        ):
            if field_name not in metadata:
                missing_availability_metadata.append(field_name)
    unavailable_metadata_missing = []
    if metadata.get("embedding_backend_available") is False:
        for field_name in (
            "backend_feasibility_status",
            "model_load_status",
            "embedding_failure_count",
        ):
            if field_name not in metadata:
                unavailable_metadata_missing.append(field_name)
    fallback_metadata_missing = []
    if metadata.get("fallback_used") is True:
        for field_name in (
            "fallback_selected_backend",
            "fallback_reason",
            "fallback_attempts",
            "requested_backend_feasibility_status",
            "requested_model_load_status",
            "requested_embedding_failure_count",
            "blocker_not_removed",
        ):
            if not metadata.get(field_name):
                fallback_metadata_missing.append(field_name)
    dimension_mismatch = False
    expected_dimension = metadata.get("expected_embedding_vector_dimension")
    observed_dimension = metadata.get("embedding_vector_dimension")
    if (
        metadata.get("embedding_backend_available") is True
        and isinstance(expected_dimension, int)
        and observed_dimension != expected_dimension
    ):
        dimension_mismatch = True
    predictive_sources = _representation_predictive_sources_from(metadata)
    for row in rows:
        predictive_sources.extend(_representation_predictive_sources_from(row))
    leakage_prone_predictive_sources = sorted(
        {
            source
            for source in predictive_sources
            if _representation_predictive_source_is_leakage_prone(source)
        }
    )
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_representation_backend_sample")
    if metadata.get("embedding_status") != "computed_review_only":
        blockers.append("representation_backend_sample_embedding_status_invalid")
    if countable_rows:
        blockers.append("representation_backend_sample_rows_marked_countable")
    if import_ready_rows:
        blockers.append("representation_backend_sample_rows_marked_ready_for_import")
    if missing_backend_status:
        blockers.append("representation_backend_sample_rows_missing_backend_status")
    if missing_review_status:
        blockers.append("representation_backend_sample_rows_not_review_only")
    if metadata.get("predictive_feature_sources") != list(
        REPRESENTATION_PREDICTIVE_FEATURE_SOURCES
    ):
        blockers.append("representation_backend_sample_predictive_policy_missing")
    if missing_predictive_sources:
        blockers.append("representation_backend_sample_rows_missing_predictive_sources")
    if leakage_context_unmarked:
        blockers.append("representation_backend_sample_leakage_context_unmarked")
    if leakage_prone_predictive_sources:
        blockers.append("representation_backend_sample_leakage_prone_predictive_sources")
    if missing_availability_metadata:
        blockers.append("representation_backend_sample_availability_metadata_missing")
    if unavailable_metadata_missing:
        blockers.append("representation_backend_sample_unavailable_metadata_missing")
    if fallback_metadata_missing:
        blockers.append("representation_backend_sample_fallback_metadata_missing")
    if dimension_mismatch:
        blockers.append("representation_backend_sample_dimension_mismatch")
    return {
        "metadata": {
            "method": "external_source_representation_backend_sample_audit",
            "blocker_removed": (
                "verifies computed representation sample rows remain "
                "review-only and non-countable before external pilot import"
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "embedding_status": metadata.get("embedding_status"),
            "embedding_backend": metadata.get("embedding_backend"),
            "requested_embedding_backend": metadata.get("requested_embedding_backend"),
            "requested_backend_feasibility_status": metadata.get(
                "requested_backend_feasibility_status"
            ),
            "requested_backend_local_cache_status": metadata.get(
                "requested_backend_local_cache_status"
            ),
            "requested_backend_smoke_status": metadata.get(
                "requested_backend_smoke_status"
            ),
            "requested_embedding_failure_count": metadata.get(
                "requested_embedding_failure_count"
            ),
            "expected_embedding_vector_dimension": metadata.get(
                "expected_embedding_vector_dimension"
            ),
            "requested_expected_embedding_vector_dimension": metadata.get(
                "requested_expected_embedding_vector_dimension"
            ),
            "embedding_elapsed_seconds": metadata.get("embedding_elapsed_seconds"),
            "model_load_status": metadata.get("model_load_status"),
            "fallback_used": metadata.get("fallback_used", False),
            "fallback_selected_backend": metadata.get("fallback_selected_backend"),
            "fallback_reason": metadata.get("fallback_reason"),
            "availability_metadata_missing_fields": sorted(
                missing_availability_metadata
            ),
            "unavailable_metadata_missing_fields": sorted(
                unavailable_metadata_missing
            ),
            "fallback_metadata_missing_fields": sorted(fallback_metadata_missing),
            "embedding_dimension_matches_expected": not dimension_mismatch,
            "import_ready_row_count": len(import_ready_rows),
            "missing_backend_status_row_count": len(missing_backend_status),
            "missing_review_only_status_row_count": len(missing_review_status),
            "missing_predictive_sources_row_count": len(missing_predictive_sources),
            "leakage_context_unmarked_row_count": len(leakage_context_unmarked),
            "leakage_prone_predictive_sources": leakage_prone_predictive_sources,
            "predictive_feature_sources": metadata.get("predictive_feature_sources"),
            "representation_near_duplicate_alert_count": metadata.get(
                "representation_near_duplicate_alert_count", 0
            ),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "computed representation backend samples are review-only "
                "controls and cannot authorize external label import"
            )
        ],
    }


def audit_external_source_representation_backend_stability(
    *,
    baseline_representation_backend_sample: dict[str, Any],
    comparison_representation_backend_sample: dict[str, Any],
) -> dict[str, Any]:
    """Compare learned representation samples without making either countable."""
    baseline_rows_by_accession = _representation_sample_rows_by_accession(
        baseline_representation_backend_sample
    )
    comparison_rows_by_accession = _representation_sample_rows_by_accession(
        comparison_representation_backend_sample
    )
    baseline_disagreements = _representation_sample_disagreements_by_accession(
        baseline_representation_backend_sample
    )
    comparison_disagreements = _representation_sample_disagreements_by_accession(
        comparison_representation_backend_sample
    )
    shared_accessions = sorted(
        set(baseline_rows_by_accession) & set(comparison_rows_by_accession)
    )
    rows: list[dict[str, Any]] = []
    nearest_reference_changed_count = 0
    nearest_reference_entry_ids_changed_count = 0
    disagreement_status_changed_count = 0
    fingerprint_context_changed_count = 0
    comparison_unavailable_count = 0

    for accession in shared_accessions:
        baseline_row = baseline_rows_by_accession[accession]
        comparison_row = comparison_rows_by_accession[accession]
        baseline_nearest = baseline_row.get("nearest_reference") or {}
        comparison_nearest = comparison_row.get("nearest_reference") or {}
        baseline_reference = _normalize_accession(
            baseline_nearest.get("reference_accession")
        )
        comparison_reference = _normalize_accession(
            comparison_nearest.get("reference_accession")
        )
        baseline_reference_entry_ids = sorted(
            str(entry_id)
            for entry_id in baseline_nearest.get("matched_m_csa_entry_ids", []) or []
            if entry_id
        )
        comparison_reference_entry_ids = sorted(
            str(entry_id)
            for entry_id in comparison_nearest.get("matched_m_csa_entry_ids", [])
            or []
            if entry_id
        )
        baseline_disagreement = baseline_disagreements.get(accession, {})
        comparison_disagreement = comparison_disagreements.get(accession, {})
        baseline_disagreement_status = str(
            baseline_disagreement.get("representation_heuristic_disagreement_status")
            or "no_disagreement_signal"
        )
        comparison_disagreement_status = str(
            comparison_disagreement.get("representation_heuristic_disagreement_status")
            or "no_disagreement_signal"
        )
        baseline_fingerprint = (
            baseline_row.get("heuristic_baseline_control", {}) or {}
        ).get("top1_fingerprint_id")
        comparison_fingerprint = (
            comparison_row.get("heuristic_baseline_control", {}) or {}
        ).get("top1_fingerprint_id")
        nearest_reference_stable = baseline_reference == comparison_reference
        nearest_reference_entry_ids_stable = (
            baseline_reference_entry_ids == comparison_reference_entry_ids
        )
        disagreement_status_stable = (
            baseline_disagreement_status == comparison_disagreement_status
        )
        fingerprint_context_stable = baseline_fingerprint == comparison_fingerprint
        flags: list[str] = []
        if not nearest_reference_stable:
            flags.append("nearest_reference_changed")
            nearest_reference_changed_count += 1
        if not nearest_reference_entry_ids_stable:
            flags.append("nearest_reference_entry_ids_changed")
            nearest_reference_entry_ids_changed_count += 1
        if not disagreement_status_stable:
            flags.append("heuristic_disagreement_status_changed")
            disagreement_status_changed_count += 1
        if not fingerprint_context_stable:
            flags.append("heuristic_fingerprint_context_changed")
            fingerprint_context_changed_count += 1
        if comparison_row.get("backend_status") == "embedding_backend_unavailable":
            flags.append("comparison_embedding_backend_unavailable")
            comparison_unavailable_count += 1
        if comparison_row.get("fallback_used") is True:
            flags.append("comparison_embedding_backend_fallback_used")
        rows.append(
            {
                "accession": accession,
                "baseline_backend_status": baseline_row.get("backend_status"),
                "baseline_embedding_backend": baseline_row.get("embedding_backend"),
                "baseline_heuristic_disagreement_status": (
                    baseline_disagreement_status
                ),
                "baseline_nearest_reference_accession": baseline_reference,
                "baseline_nearest_reference_entry_ids": baseline_reference_entry_ids,
                "baseline_top_embedding_cosine": baseline_row.get(
                    "top_embedding_cosine"
                ),
                "comparison_backend_status": comparison_row.get("backend_status"),
                "comparison_embedding_backend": comparison_row.get(
                    "embedding_backend"
                ),
                "comparison_requested_embedding_backend": comparison_row.get(
                    "requested_embedding_backend"
                ),
                "comparison_fallback_used": comparison_row.get(
                    "fallback_used", False
                ),
                "comparison_fallback_reason": comparison_row.get("fallback_reason"),
                "comparison_heuristic_disagreement_status": (
                    comparison_disagreement_status
                ),
                "comparison_nearest_reference_accession": comparison_reference,
                "comparison_nearest_reference_entry_ids": (
                    comparison_reference_entry_ids
                ),
                "comparison_top_embedding_cosine": comparison_row.get(
                    "top_embedding_cosine"
                ),
                "countable_label_candidate": False,
                "heuristic_top1_fingerprint_id": baseline_fingerprint,
                "nearest_reference_stable": nearest_reference_stable,
                "nearest_reference_entry_ids_stable": (
                    nearest_reference_entry_ids_stable
                ),
                "heuristic_disagreement_status_stable": disagreement_status_stable,
                "heuristic_fingerprint_context_stable": fingerprint_context_stable,
                "ready_for_label_import": False,
                "review_status": "representation_backend_stability_audit_review_only",
                "stability_flags": flags,
            }
        )

    baseline_meta = baseline_representation_backend_sample.get("metadata", {})
    comparison_meta = comparison_representation_backend_sample.get("metadata", {})
    all_sample_rows = [
        row
        for sample in (
            baseline_representation_backend_sample,
            comparison_representation_backend_sample,
        )
        for row in sample.get("rows", []) or []
        if isinstance(row, dict)
    ]
    countable_rows = [
        row for row in all_sample_rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in all_sample_rows if row.get("ready_for_label_import") is not False
    ]
    blockers: list[str] = []
    if countable_rows:
        blockers.append("representation_stability_rows_marked_countable")
    if import_ready_rows:
        blockers.append("representation_stability_rows_marked_ready_for_import")
    if not rows:
        blockers.append("empty_representation_backend_stability_audit")
    if comparison_meta.get("embedding_backend_available") is not True:
        stability_status = "comparison_backend_unavailable"
    elif comparison_meta.get("fallback_used") is True and (
        nearest_reference_changed_count
        or nearest_reference_entry_ids_changed_count
        or disagreement_status_changed_count
        or fingerprint_context_changed_count
    ):
        stability_status = "fallback_changed"
    elif comparison_meta.get("fallback_used") is True:
        stability_status = "fallback_stable"
    elif (
        nearest_reference_changed_count
        or nearest_reference_entry_ids_changed_count
        or disagreement_status_changed_count
        or fingerprint_context_changed_count
    ):
        stability_status = "changed"
    else:
        stability_status = "stable"
    return {
        "metadata": {
            "method": "external_source_representation_backend_stability_audit",
            "blocker_removed": (
                "compares baseline and upgraded learned representation controls "
                "without changing countable labels"
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "baseline_candidate_count": baseline_meta.get("candidate_count", 0),
            "comparison_candidate_count": comparison_meta.get("candidate_count", 0),
            "shared_candidate_count": len(rows),
            "baseline_embedding_backend": baseline_meta.get("embedding_backend"),
            "comparison_embedding_backend": comparison_meta.get("embedding_backend"),
            "comparison_requested_embedding_backend": comparison_meta.get(
                "requested_embedding_backend"
            ),
            "baseline_model_name": baseline_meta.get("model_name"),
            "comparison_model_name": comparison_meta.get("model_name"),
            "comparison_requested_model_name": comparison_meta.get(
                "requested_model_name"
            ),
            "baseline_embedding_vector_dimension": baseline_meta.get(
                "embedding_vector_dimension"
            ),
            "comparison_embedding_vector_dimension": comparison_meta.get(
                "embedding_vector_dimension"
            ),
            "comparison_expected_embedding_vector_dimension": comparison_meta.get(
                "expected_embedding_vector_dimension"
            ),
            "comparison_requested_expected_embedding_vector_dimension": (
                comparison_meta.get("requested_expected_embedding_vector_dimension")
            ),
            "baseline_embedding_backend_available": baseline_meta.get(
                "embedding_backend_available"
            ),
            "comparison_embedding_backend_available": comparison_meta.get(
                "embedding_backend_available"
            ),
            "comparison_backend_feasibility_status": comparison_meta.get(
                "backend_feasibility_status"
            ),
            "comparison_requested_backend_feasibility_status": comparison_meta.get(
                "requested_backend_feasibility_status"
            ),
            "comparison_requested_backend_local_cache_status": comparison_meta.get(
                "requested_backend_local_cache_status"
            ),
            "comparison_requested_backend_smoke_status": comparison_meta.get(
                "requested_backend_smoke_status"
            ),
            "comparison_requested_embedding_failure_count": comparison_meta.get(
                "requested_embedding_failure_count", 0
            ),
            "comparison_fallback_used": comparison_meta.get("fallback_used", False),
            "comparison_fallback_selected_backend": comparison_meta.get(
                "fallback_selected_backend"
            ),
            "comparison_fallback_reason": comparison_meta.get("fallback_reason"),
            "comparison_blocker_not_removed": comparison_meta.get(
                "blocker_not_removed"
            ),
            "comparison_largest_supported_embedding_backend": comparison_meta.get(
                "largest_supported_embedding_backend"
            ),
            "comparison_largest_feasible_embedding_backend": comparison_meta.get(
                "largest_feasible_embedding_backend"
            ),
            "comparison_fallback_not_computed_reason": comparison_meta.get(
                "fallback_not_computed_reason"
            ),
            "comparison_embedding_failure_count": comparison_meta.get(
                "embedding_failure_count", 0
            ),
            "comparison_embedding_elapsed_seconds": comparison_meta.get(
                "embedding_elapsed_seconds"
            ),
            "nearest_reference_stable_count": len(rows)
            - nearest_reference_changed_count,
            "nearest_reference_changed_count": nearest_reference_changed_count,
            "nearest_reference_entry_ids_stable_count": len(rows)
            - nearest_reference_entry_ids_changed_count,
            "nearest_reference_entry_ids_changed_count": (
                nearest_reference_entry_ids_changed_count
            ),
            "heuristic_disagreement_status_stable_count": len(rows)
            - disagreement_status_changed_count,
            "heuristic_disagreement_status_changed_count": (
                disagreement_status_changed_count
            ),
            "heuristic_fingerprint_context_stable_count": len(rows)
            - fingerprint_context_changed_count,
            "heuristic_fingerprint_context_changed_count": (
                fingerprint_context_changed_count
            ),
            "comparison_embedding_backend_unavailable_row_count": (
                comparison_unavailable_count
            ),
            "stability_status": stability_status,
            "guardrail_clean": not blockers,
        },
        "rows": rows,
        "blockers": blockers,
        "warnings": [
            (
                "representation backend stability audits compare sequence-derived "
                "controls only; they cannot authorize external label import"
            )
        ],
    }


def _representation_sample_rows_by_accession(
    representation_backend_sample: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    rows_by_accession: dict[str, dict[str, Any]] = {}
    for row in representation_backend_sample.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            rows_by_accession[accession] = row
    return rows_by_accession


def _representation_sample_disagreements_by_accession(
    representation_backend_sample: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    rows_by_accession: dict[str, dict[str, Any]] = {}
    for row in (
        representation_backend_sample.get("learned_vs_heuristic_disagreements", [])
        or []
    ):
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if accession:
            rows_by_accession[accession] = row
    return rows_by_accession


def _representation_predictive_source_is_leakage_prone(source: str) -> bool:
    normalized = source.lower()
    return any(
        term in normalized
        for term in REPRESENTATION_LEAKAGE_PRONE_PREDICTIVE_TERMS
    )


def _representation_predictive_sources_from(payload: dict[str, Any]) -> list[str]:
    sources = payload.get("predictive_feature_sources", [])
    if isinstance(sources, str):
        return [sources]
    if isinstance(sources, (list, tuple)):
        return [str(source) for source in sources]
    return []


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
    inactive_replacements = sequence_payload.get("metadata", {}).get(
        "inactive_accession_replacements", {}
    )
    if not isinstance(inactive_replacements, dict):
        inactive_replacements = {}
    reference_records: list[dict[str, Any]] = []
    resolved_reference_accessions: set[str] = set()
    inactive_reference_resolutions: dict[str, list[str]] = {}
    missing_reference_sequence_accessions: list[str] = []
    for accession in reference_accessions:
        record = records_by_accession.get(accession)
        if record and _clean_sequence(record.get("sequence")):
            reference_records.append(
                {
                    "record": record,
                    "requested_reference_accession": accession,
                    "resolved_reference_accession": accession,
                    "reference_accession_resolution": "primary_accession",
                }
            )
            resolved_reference_accessions.add(accession)
            continue
        replacement_records: list[dict[str, Any]] = []
        for replacement in inactive_replacements.get(accession, []) or []:
            replacement_accession = _normalize_accession(replacement)
            replacement_record = records_by_accession.get(replacement_accession)
            if replacement_record and _clean_sequence(
                replacement_record.get("sequence")
            ):
                replacement_records.append(replacement_record)
        if replacement_records:
            resolved_reference_accessions.add(accession)
            inactive_reference_resolutions[accession] = [
                _normalize_accession(record.get("accession"))
                for record in replacement_records
                if _normalize_accession(record.get("accession"))
            ]
            for replacement_record in replacement_records:
                reference_records.append(
                    {
                        "record": replacement_record,
                        "requested_reference_accession": accession,
                        "resolved_reference_accession": _normalize_accession(
                            replacement_record.get("accession")
                        ),
                        "reference_accession_resolution": (
                            "inactive_accession_replacement"
                        ),
                    }
                )
            continue
        missing_reference_sequence_accessions.append(accession)

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
            for reference_context in reference_records:
                reference_record = reference_context["record"]
                reference_accession = _normalize_accession(
                    reference_context.get("resolved_reference_accession")
                    or reference_record.get("accession")
                )
                requested_reference_accession = _normalize_accession(
                    reference_context.get("requested_reference_accession")
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
                        reference_entry_ids_by_accession.get(
                            requested_reference_accession or reference_accession,
                            set(),
                        )
                    ),
                    identity_alert_threshold=identity_alert_threshold,
                    coverage_alert_threshold=coverage_alert_threshold,
                    kmer_alert_threshold=kmer_alert_threshold,
                )
                if match:
                    if requested_reference_accession != reference_accession:
                        match["requested_reference_accession"] = (
                            requested_reference_accession
                        )
                        match["reference_accession_resolution"] = (
                            reference_context.get("reference_accession_resolution")
                        )
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
            "reference_sequence_count": len(resolved_reference_accessions),
            "reference_sequence_record_count": len(reference_records),
            "expected_reference_accession_count": len(reference_accessions),
            "missing_reference_sequence_count": len(
                missing_reference_sequence_accessions
            ),
            "missing_reference_sequence_accessions": (
                missing_reference_sequence_accessions[:25]
            ),
            "inactive_reference_accession_resolution_count": len(
                inactive_reference_resolutions
            ),
            "inactive_reference_accession_resolutions": dict(
                sorted(inactive_reference_resolutions.items())
            ),
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


def audit_external_source_sequence_reference_screen(
    *,
    sequence_neighborhood_sample: dict[str, Any],
    sequence_alignment_verification: dict[str, Any],
    sequence_clusters: dict[str, Any],
    labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Verify the local countable-reference screen is complete for pilot triage."""
    countable_entry_ids = _countable_label_entry_ids(labels)
    expected_reference_accessions: set[str] = set()
    for row in sequence_clusters.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("entry_id") or "") not in countable_entry_ids:
            continue
        expected_reference_accessions.update(
            _normalize_accession(accession)
            for accession in row.get("reference_uniprot_ids", []) or []
            if _normalize_accession(accession)
        )

    sample_rows = [
        row
        for row in sequence_neighborhood_sample.get("rows", []) or []
        if isinstance(row, dict)
    ]
    alignment_rows = [
        row
        for row in sequence_alignment_verification.get("rows", []) or []
        if isinstance(row, dict)
    ]
    alignments_by_pair = {
        (
            _normalize_accession(row.get("accession")),
            _normalize_accession(row.get("reference_accession")),
        ): row
        for row in alignment_rows
        if _normalize_accession(row.get("accession"))
        and _normalize_accession(row.get("reference_accession"))
    }

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    incomplete_accessions: list[str] = []
    alert_accessions: list[str] = []
    for sample_row in sample_rows:
        accession = _normalize_accession(sample_row.get("accession"))
        top_matches = [
            match
            for match in sample_row.get("top_matches", []) or []
            if isinstance(match, dict)
            and _normalize_accession(match.get("reference_accession"))
        ]
        expected_pairs = [
            (accession, _normalize_accession(match.get("reference_accession")))
            for match in top_matches
        ]
        checked_alignments = [
            alignments_by_pair[pair]
            for pair in expected_pairs
            if pair in alignments_by_pair
        ]
        missing_pairs = [
            pair[1] for pair in expected_pairs if pair not in alignments_by_pair
        ]
        has_alignment_alert = any(
            row.get("verification_status")
            in {
                "alignment_exact_reference_holdout",
                "alignment_near_duplicate_candidate_holdout",
            }
            for row in checked_alignments
        )
        screen_status = str(sample_row.get("screen_status") or "")
        if screen_status == "preexisting_sequence_holdout_retained":
            status = "preexisting_sequence_holdout_retained"
            alert_accessions.append(accession)
        elif not top_matches:
            status = "current_reference_screen_missing_top_hits"
            incomplete_accessions.append(accession)
        elif missing_pairs:
            status = "current_reference_top_hit_alignment_incomplete"
            incomplete_accessions.append(accession)
        elif has_alignment_alert or screen_status == "near_duplicate_candidate_holdout":
            status = "current_reference_near_duplicate_holdout"
            alert_accessions.append(accession)
        else:
            status = "current_reference_top_hits_aligned_no_alert"
        status_counts[status] += 1
        rows.append(
            {
                "accession": accession,
                "countable_label_candidate": False,
                "current_reference_screen_status": status,
                "entry_id": sample_row.get("entry_id") or f"uniprot:{accession}",
                "ready_for_label_import": False,
                "reference_top_hit_count": len(top_matches),
                "review_status": "sequence_reference_screen_audit_review_only",
                "top_hit_alignment_checked_count": len(checked_alignments),
                "top_hit_alignment_missing_reference_accessions": missing_pairs,
            }
        )

    metadata = sequence_neighborhood_sample.get("metadata", {})
    expected_candidate_count = int(metadata.get("candidate_count", 0) or 0)
    sample_reference_count = int(metadata.get("reference_sequence_count", 0) or 0)
    missing_reference_count = int(
        metadata.get(
            "missing_reference_sequence_count",
            max(0, len(expected_reference_accessions) - sample_reference_count),
        )
        or 0
    )
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_current_reference_sequence_screen")
    if expected_candidate_count and len(rows) != expected_candidate_count:
        blockers.append("current_reference_sequence_screen_candidate_count_mismatch")
    if (
        sample_reference_count < len(expected_reference_accessions)
        or missing_reference_count
    ):
        blockers.append("current_reference_sequence_screen_incomplete")
    if int(metadata.get("fetch_failure_count", 0) or 0) != 0:
        blockers.append("current_reference_sequence_fetch_failures")
    if int(metadata.get("missing_external_sequence_count", 0) or 0) != 0:
        blockers.append("current_reference_external_sequences_missing")
    if incomplete_accessions:
        blockers.append("current_reference_top_hit_alignment_incomplete")

    return {
        "metadata": {
            "method": "external_source_sequence_reference_screen_audit",
            "blocker_target": "external_pilot_current_reference_near_duplicate_screen",
            "blocker_removed": (
                "external_pilot_current_reference_near_duplicate_screen"
                if not blockers
                else None
            ),
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "expected_candidate_count": expected_candidate_count,
            "expected_reference_accession_count": len(expected_reference_accessions),
            "screened_reference_sequence_count": sample_reference_count,
            "missing_reference_sequence_count": missing_reference_count,
            "missing_reference_sequence_accessions": metadata.get(
                "missing_reference_sequence_accessions", []
            ),
            "inactive_reference_accession_resolutions": metadata.get(
                "inactive_reference_accession_resolutions", {}
            ),
            "alignment_verified_pair_count": len(alignment_rows),
            "current_reference_screen_complete": not blockers,
            "current_reference_near_duplicate_alert_candidate_count": len(
                sorted(set(alert_accessions))
            ),
            "incomplete_candidate_count": len(sorted(set(incomplete_accessions))),
            "screen_status_counts": dict(sorted(status_counts.items())),
            "guardrail_clean": not blockers,
            "review_only_rule": (
                "this audit only verifies the bounded current countable-reference "
                "screen; UniRef or all-vs-all near-duplicate search remains "
                "required before external import"
            ),
        },
        "rows": sorted(rows, key=lambda row: str(row.get("accession") or "")),
        "blockers": blockers,
        "warnings": [
            (
                "current-reference sequence screening is a review-only control "
                "and cannot authorize external label import"
            )
        ],
    }


def build_external_source_sequence_search_export(
    *,
    sequence_neighborhood_plan: dict[str, Any],
    sequence_neighborhood_sample: dict[str, Any],
    sequence_alignment_verification: dict[str, Any],
    sequence_reference_screen_audit: dict[str, Any] | None = None,
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
    reference_screen_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (sequence_reference_screen_audit or {}).get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    reference_screen_meta = (sequence_reference_screen_audit or {}).get("metadata", {})
    reference_screen_complete = (
        reference_screen_meta.get("current_reference_screen_complete") is True
        and reference_screen_meta.get("guardrail_clean") is True
    )

    rows: list[dict[str, Any]] = []
    search_task_counts: Counter[str] = Counter()
    current_reference_screen_complete_count = 0
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
        reference_screen_row = reference_screen_by_accession.get(accession, {})
        current_reference_status = str(
            reference_screen_row.get("current_reference_screen_status") or ""
        )
        if (
            reference_screen_complete
            and current_reference_status
            == "current_reference_top_hits_aligned_no_alert"
        ):
            current_reference_screen_complete_count += 1
        search_task_counts[search_task] += 1
        top_matches = list(sample_row.get("top_matches") or [])[:10]
        rows.append(
            {
                "accession": accession,
                "alignment_status": alignment_status,
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
                "current_reference_screen": {
                    "current_reference_screen_complete": (
                        reference_screen_complete
                        and bool(current_reference_status)
                        and current_reference_status
                        != "current_reference_top_hit_alignment_incomplete"
                    ),
                    "status": current_reference_status or None,
                },
                "source_targets": _external_sequence_search_source_targets(
                    accession=accession,
                    top_matches=top_matches,
                ),
                "top_matches": top_matches,
                "blockers": _external_sequence_search_export_blockers(
                    search_task,
                    current_reference_screen_complete=(
                        reference_screen_complete
                        and current_reference_status
                        == "current_reference_top_hits_aligned_no_alert"
                    ),
                ),
            }
        )

    rows = rows[:max_rows]
    blocker_counts = Counter(
        blocker
        for row in rows
        for blocker in row.get("blockers", []) or []
        if blocker
    )
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
            "source_sequence_reference_screen_audit_method": (
                reference_screen_meta.get("method")
            ),
            "ready_for_label_import": False,
            "complete_near_duplicate_search_required": True,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "current_reference_screen_complete_candidate_count": (
                current_reference_screen_complete_count
            ),
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
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "blocker_removed": (
                "external_pilot_current_reference_near_duplicate_screen"
                if current_reference_screen_complete_count
                else None
            ),
            "review_only_rule": (
                "sequence-search exports are OOD control worklists and cannot "
                "create countable labels or import-ready rows"
            ),
        },
        "rows": rows,
        "blockers": sorted(blocker_counts),
        "warnings": [
            (
                "bounded sequence screens and top-hit alignments are not a "
                "complete near-duplicate search; keep external rows non-countable"
            )
        ],
    }


def build_external_source_backend_sequence_search(
    *,
    candidate_manifest: dict[str, Any],
    sequence_clusters: dict[str, Any],
    labels: list[dict[str, Any]],
    reference_fasta: str,
    external_fasta_out: str,
    reference_fasta_out: str,
    result_tsv_out: str,
    backend: str = "auto",
    mmseqs_binary: str = "mmseqs",
    diamond_binary: str = "diamond",
    blastp_binary: str = "blastp",
    makeblastdb_binary: str = "makeblastdb",
    identity_threshold: float = 0.90,
    coverage_threshold: float = 0.80,
    exact_identity_threshold: float = 0.999,
    exact_coverage_threshold: float = 0.98,
    max_rows: int = 100,
    top_k: int = 5,
    fetcher: Callable[[list[str]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run a real backend external-vs-current-reference sequence search."""
    manifest_rows = [
        row
        for row in candidate_manifest.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    ][:max_rows]
    external_accessions = sorted(
        {_normalize_accession(row.get("accession")) for row in manifest_rows}
    )
    fetch = fetcher or _fetch_uniprot_sequence_records
    external_fetch_failures: list[dict[str, str]] = []
    try:
        external_payload = fetch(external_accessions)
    except Exception as exc:  # pragma: no cover - live network failure path
        external_payload = {"metadata": {}, "records": []}
        external_fetch_failures.append(
            {"error_type": type(exc).__name__, "error": str(exc)}
        )
    external_records_by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in external_payload.get("records", []) or []
        if isinstance(record, dict)
        and _normalize_accession(record.get("accession"))
        and _clean_sequence(record.get("sequence"))
    }

    countable_entry_ids = _countable_label_entry_ids(labels)
    reference_entry_ids_by_accession: dict[str, set[str]] = {}
    for row in sequence_clusters.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id") or "")
        if entry_id not in countable_entry_ids:
            continue
        for accession in row.get("reference_uniprot_ids", []) or []:
            normalized = _normalize_accession(accession)
            if normalized:
                reference_entry_ids_by_accession.setdefault(normalized, set()).add(
                    entry_id
                )
    requested_reference_accessions = sorted(reference_entry_ids_by_accession)
    parsed_reference_fasta = _parse_sequence_fasta(Path(reference_fasta))
    reference_fasta_records_by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in parsed_reference_fasta
        if _normalize_accession(record.get("accession"))
        and _clean_sequence(record.get("sequence"))
    }
    missing_reference_accessions = [
        accession
        for accession in requested_reference_accessions
        if accession not in reference_fasta_records_by_accession
    ]
    reference_fetch_failures: list[dict[str, str]] = []
    reference_replacement_records_by_accession: dict[str, dict[str, Any]] = {}
    inactive_reference_resolutions: dict[str, list[str]] = {}
    if missing_reference_accessions:
        try:
            reference_payload = fetch(missing_reference_accessions)
        except Exception as exc:  # pragma: no cover - live network failure path
            reference_payload = {"metadata": {}, "records": []}
            reference_fetch_failures.append(
                {"error_type": type(exc).__name__, "error": str(exc)}
            )
        reference_replacement_records_by_accession = {
            _normalize_accession(record.get("accession")): record
            for record in reference_payload.get("records", []) or []
            if isinstance(record, dict)
            and _normalize_accession(record.get("accession"))
            and _clean_sequence(record.get("sequence"))
        }
        inactive_replacements = reference_payload.get("metadata", {}).get(
            "inactive_accession_replacements", {}
        )
        if isinstance(inactive_replacements, dict):
            inactive_reference_resolutions = {
                _normalize_accession(accession): [
                    _normalize_accession(replacement)
                    for replacement in replacements
                    if _normalize_accession(replacement)
                ]
                for accession, replacements in inactive_replacements.items()
                if _normalize_accession(accession)
            }

    external_sequence_records: dict[str, dict[str, Any]] = {}
    missing_external_sequence_accessions: list[str] = []
    for accession in external_accessions:
        record = external_records_by_accession.get(accession)
        sequence = _clean_sequence((record or {}).get("sequence"))
        if not sequence:
            missing_external_sequence_accessions.append(accession)
            continue
        record_id = _external_sequence_record_id("ext", accession)
        external_sequence_records[record_id] = {
            "accession": accession,
            "record_id": record_id,
            "sequence": sequence,
        }

    reference_sequence_records: dict[str, dict[str, Any]] = {}
    unresolved_reference_sequence_accessions: list[str] = []
    for accession in requested_reference_accessions:
        fasta_record = reference_fasta_records_by_accession.get(accession)
        if fasta_record:
            record_id = _external_sequence_record_id("ref", accession)
            reference_sequence_records[record_id] = {
                "accession": accession,
                "matched_m_csa_entry_ids": sorted(
                    reference_entry_ids_by_accession.get(accession, set()),
                    key=_external_entry_id_sort_key,
                ),
                "record_id": record_id,
                "reference_accession_resolution": "source_reference_fasta",
                "requested_reference_accession": accession,
                "resolved_reference_accession": accession,
                "sequence": _clean_sequence(fasta_record.get("sequence")),
            }
            continue
        replacement_accessions = inactive_reference_resolutions.get(accession, [])
        direct_record = reference_replacement_records_by_accession.get(accession)
        if direct_record:
            replacement_accessions = [accession]
        replacement_records_added = 0
        for replacement_accession in replacement_accessions:
            replacement_record = reference_replacement_records_by_accession.get(
                replacement_accession
            )
            replacement_sequence = _clean_sequence(
                (replacement_record or {}).get("sequence")
            )
            if not replacement_sequence:
                continue
            record_id = _external_sequence_record_id(
                "ref", accession, replacement_accession
            )
            reference_sequence_records[record_id] = {
                "accession": replacement_accession,
                "matched_m_csa_entry_ids": sorted(
                    reference_entry_ids_by_accession.get(accession, set()),
                    key=_external_entry_id_sort_key,
                ),
                "record_id": record_id,
                "reference_accession_resolution": (
                    "primary_accession"
                    if replacement_accession == accession
                    else "inactive_accession_replacement"
                ),
                "requested_reference_accession": accession,
                "resolved_reference_accession": replacement_accession,
                "sequence": replacement_sequence,
            }
            replacement_records_added += 1
        if not replacement_records_added:
            unresolved_reference_sequence_accessions.append(accession)

    external_fasta_path = Path(external_fasta_out).resolve()
    reference_fasta_path = Path(reference_fasta_out).resolve()
    result_tsv_path = Path(result_tsv_out).resolve()
    _write_sequence_fasta(external_fasta_path, external_sequence_records.values())
    _write_sequence_fasta(reference_fasta_path, reference_sequence_records.values())
    backend_result = _run_external_sequence_search_backend(
        external_fasta=external_fasta_path,
        reference_fasta=reference_fasta_path,
        result_tsv=result_tsv_path,
        backend=backend,
        mmseqs_binary=mmseqs_binary,
        diamond_binary=diamond_binary,
        blastp_binary=blastp_binary,
        makeblastdb_binary=makeblastdb_binary,
        coverage_threshold=coverage_threshold,
    )
    alignments = _external_sequence_search_alignments(
        backend_result.get("alignment_rows", []),
        external_sequence_records=external_sequence_records,
        reference_sequence_records=reference_sequence_records,
    )
    alignments_by_accession: dict[str, list[dict[str, Any]]] = {}
    for alignment in alignments:
        alignments_by_accession.setdefault(
            _normalize_accession(alignment.get("accession")), []
        ).append(alignment)
    for accession_alignments in alignments_by_accession.values():
        accession_alignments.sort(
            key=lambda row: (
                -float(row.get("identity", 0.0) or 0.0),
                -float(row.get("min_coverage", 0.0) or 0.0),
                -float(row.get("bits", 0.0) or 0.0),
                str(row.get("reference_accession") or ""),
            )
        )

    manifest_by_accession = {
        _normalize_accession(row.get("accession")): row for row in manifest_rows
    }
    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    exact_reference_rows: list[dict[str, Any]] = []
    near_duplicate_rows: list[dict[str, Any]] = []
    no_signal_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    max_identity: float | None = None
    for accession in sorted(manifest_by_accession):
        manifest_row = manifest_by_accession[accession]
        similarity_control = (
            manifest_row.get("external_source_controls", {}).get(
                "sequence_similarity_control", {}
            )
            if isinstance(manifest_row.get("external_source_controls"), dict)
            else {}
        )
        top_hits = alignments_by_accession.get(accession, [])[:top_k]
        if top_hits:
            local_max = max(float(hit.get("identity", 0.0) or 0.0) for hit in top_hits)
            max_identity = local_max if max_identity is None else max(max_identity, local_max)
        exact_overlap = bool(similarity_control.get("exact_reference_overlap"))
        exact_hit = next(
            (
                hit
                for hit in top_hits
                if hit.get("reference_accession") == accession
                and float(hit.get("identity", 0.0) or 0.0) >= exact_identity_threshold
                and float(hit.get("query_coverage", 0.0) or 0.0)
                >= exact_coverage_threshold
                and float(hit.get("target_coverage", 0.0) or 0.0)
                >= exact_coverage_threshold
            ),
            None,
        )
        near_duplicate_hits = [
            hit
            for hit in top_hits
            if float(hit.get("identity", 0.0) or 0.0) >= identity_threshold
            and float(hit.get("query_coverage", 0.0) or 0.0) >= coverage_threshold
            and float(hit.get("target_coverage", 0.0) or 0.0) >= coverage_threshold
        ]
        if accession in missing_external_sequence_accessions:
            search_status = "external_sequence_missing"
            blockers = [
                "external_sequence_missing_for_backend_search",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        elif not backend_result.get("backend_available"):
            search_status = "backend_unavailable"
            blockers = [
                "real_sequence_search_backend_unavailable",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        elif not backend_result.get("backend_succeeded"):
            search_status = "backend_failed"
            blockers = [
                "real_sequence_search_backend_failed",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        elif exact_overlap or exact_hit is not None:
            search_status = "exact_reference_holdout"
            blockers = [
                "sequence_holdout_control_not_resolved",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        elif near_duplicate_hits:
            search_status = "near_duplicate_holdout"
            blockers = [
                "near_duplicate_sequence_holdout",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        else:
            search_status = "no_near_duplicate_signal"
            blockers = [
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ]
        status_counts[search_status] += 1
        row = {
            "accession": accession,
            "backend_name": backend_result.get("backend_name"),
            "backend_search_complete": bool(
                backend_result.get("backend_succeeded")
                and search_status
                in {
                    "exact_reference_holdout",
                    "near_duplicate_holdout",
                    "no_near_duplicate_signal",
                }
            ),
            "blockers": blockers,
            "countable_label_candidate": False,
            "entry_id": manifest_row.get("entry_id") or f"uniprot:{accession}",
            "exact_reference_overlap": exact_overlap,
            "external_sequence_length": len(
                external_sequence_records.get(
                    _external_sequence_record_id("ext", accession), {}
                ).get("sequence", "")
            ),
            "lane_id": manifest_row.get("lane_id"),
            "matched_m_csa_entry_ids": similarity_control.get(
                "matched_m_csa_entry_ids", []
            ),
            "max_external_vs_reference_identity": (
                round(max(float(hit.get("identity", 0.0) or 0.0) for hit in top_hits), 4)
                if top_hits
                else None
            ),
            "near_duplicate_hit_count": len(near_duplicate_hits),
            "protein_name": manifest_row.get("protein_name"),
            "ready_for_label_import": False,
            "review_status": "external_backend_sequence_search_review_only",
            "scope_signal": manifest_row.get("scope_signal"),
            "search_status": search_status,
            "top_hits": top_hits,
        }
        rows.append(row)
        if search_status == "exact_reference_holdout":
            exact_reference_rows.append(row)
        elif search_status == "near_duplicate_holdout":
            near_duplicate_rows.append(row)
        elif search_status == "no_near_duplicate_signal":
            no_signal_rows.append(row)
        else:
            failure_rows.append(row)

    row_blocker_counts = Counter(
        blocker for row in rows for blocker in row.get("blockers", []) or []
    )
    limitations = list(backend_result.get("limitations", []))
    limitations.extend(
        [
            (
                "bounded search compares the 30-row external pilot against current "
                "accepted countable reference sequences only; no UniRef database was "
                "downloaded or searched"
            ),
            (
                "backend no-signal rows remove complete-search debt for the bounded "
                "current-reference pilot screen only; exact and near-duplicate rows "
                "remain holdout controls"
            ),
            "Foldseek/TM-score structural duplicate screening is not computed here",
        ]
    )
    return {
        "metadata": {
            "method": "external_source_backend_sequence_search",
            "backend_requested": backend,
            "backend_name": backend_result.get("backend_name"),
            "backend_version": backend_result.get("backend_version"),
            "backend_available": bool(backend_result.get("backend_available")),
            "backend_succeeded": bool(backend_result.get("backend_succeeded")),
            "backend_commands": backend_result.get("backend_commands", []),
            "backend_result_tsv": str(result_tsv_out),
            "blocker_removed": "complete_uniref_or_all_vs_all_near_duplicate_search_required",
            "blocker_removed_for_status": "no_near_duplicate_signal",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "import_ready_row_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "expected_external_sequence_count": len(external_accessions),
            "external_sequence_count": len(external_sequence_records),
            "external_sequence_source": external_payload.get("metadata", {}).get(
                "source"
            ),
            "missing_external_sequence_count": len(
                missing_external_sequence_accessions
            ),
            "missing_external_sequence_accessions": missing_external_sequence_accessions,
            "current_reference_accession_count": len(requested_reference_accessions),
            "current_reference_sequence_count": len(reference_sequence_records),
            "reference_fasta_record_count": len(parsed_reference_fasta),
            "missing_reference_sequence_count": len(
                unresolved_reference_sequence_accessions
            ),
            "missing_reference_sequence_accessions": (
                unresolved_reference_sequence_accessions
            ),
            "inactive_reference_accession_resolutions": (
                inactive_reference_resolutions
            ),
            "identity_threshold": identity_threshold,
            "coverage_threshold": coverage_threshold,
            "exact_identity_threshold": exact_identity_threshold,
            "exact_coverage_threshold": exact_coverage_threshold,
            "exact_reference_row_count": len(exact_reference_rows),
            "near_duplicate_row_count": len(near_duplicate_rows),
            "no_signal_row_count": len(no_signal_rows),
            "failure_row_count": len(failure_rows),
            "alignment_row_count": len(alignments),
            "max_external_vs_reference_identity": (
                round(max_identity, 4) if max_identity is not None else None
            ),
            "search_status_counts": dict(sorted(status_counts.items())),
            "row_blocker_counts": dict(sorted(row_blocker_counts.items())),
            "sequence_source_artifacts": {
                "candidate_manifest": candidate_manifest.get("metadata", {}).get(
                    "method"
                ),
                "sequence_clusters": sequence_clusters.get("metadata", {}).get(
                    "method"
                ),
                "reference_fasta": reference_fasta,
                "generated_external_fasta": external_fasta_out,
                "generated_reference_fasta": reference_fasta_out,
            },
            "limitations": limitations,
            "review_only_rule": (
                "real backend sequence-search evidence is review-only and cannot "
                "make external rows countable or import-ready"
            ),
        },
        "rows": rows,
        "exact_reference_rows": exact_reference_rows,
        "near_duplicate_rows": near_duplicate_rows,
        "no_signal_rows": no_signal_rows,
        "failure_rows": failure_rows,
        "fetch_failures": external_fetch_failures + reference_fetch_failures,
        "blockers": sorted(row_blocker_counts),
        "warnings": [
            (
                "the backend search removes bounded current-reference sequence-search "
                "debt only for no-signal rows; active-site evidence, representation "
                "controls, review decisions, and factory gates remain required"
            )
        ],
    }


def audit_external_source_backend_sequence_search(
    *,
    backend_sequence_search: dict[str, Any],
    candidate_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Verify backend sequence-search results remain real and review-only."""
    rows = [
        row
        for row in backend_sequence_search.get("rows", []) or []
        if isinstance(row, dict)
    ]
    manifest_accessions = {
        _normalize_accession(row.get("accession"))
        for row in candidate_manifest.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    row_accessions = {
        _normalize_accession(row.get("accession"))
        for row in rows
        if _normalize_accession(row.get("accession"))
    }
    exact_manifest_accessions = {
        _normalize_accession(row.get("accession"))
        for row in candidate_manifest.get("rows", []) or []
        if isinstance(row, dict)
        and _normalize_accession(row.get("accession"))
        and isinstance(row.get("external_source_controls"), dict)
        and (
            row.get("external_source_controls", {})
            .get("sequence_similarity_control", {})
            .get("exact_reference_overlap")
            is True
        )
    }
    exact_result_accessions = {
        _normalize_accession(row.get("accession"))
        for row in backend_sequence_search.get("exact_reference_rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    metadata = backend_sequence_search.get("metadata", {})
    real_backend = str(metadata.get("backend_name") or "") in {
        "mmseqs2_easy_search",
        "diamond_blastp",
        "blastp",
    }
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_review_only_rows = [
        row
        for row in rows
        if row.get("review_status")
        != "external_backend_sequence_search_review_only"
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_backend_sequence_search")
    if not real_backend or metadata.get("backend_succeeded") is not True:
        blockers.append("backend_sequence_search_not_real_or_not_successful")
    if metadata.get("method") != "external_source_backend_sequence_search":
        blockers.append("backend_sequence_search_wrong_method")
    if row_accessions != manifest_accessions:
        blockers.append("backend_sequence_search_candidate_mismatch")
    if countable_rows:
        blockers.append("backend_sequence_search_rows_marked_countable")
    if import_ready_rows:
        blockers.append("backend_sequence_search_rows_marked_ready_for_import")
    if missing_review_only_rows:
        blockers.append("backend_sequence_search_rows_not_review_only")
    if not exact_manifest_accessions.issubset(exact_result_accessions):
        blockers.append("backend_sequence_search_lost_exact_reference_holdouts")
    return {
        "metadata": {
            "method": "external_source_backend_sequence_search_audit",
            "backend_name": metadata.get("backend_name"),
            "backend_version": metadata.get("backend_version"),
            "backend_succeeded": bool(metadata.get("backend_succeeded")),
            "real_backend": real_backend,
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "import_ready_row_count": len(import_ready_rows),
            "candidate_count": len(rows),
            "expected_candidate_count": len(manifest_accessions),
            "exact_reference_manifest_count": len(exact_manifest_accessions),
            "exact_reference_result_count": len(exact_result_accessions),
            "no_signal_row_count": metadata.get("no_signal_row_count", 0),
            "near_duplicate_row_count": metadata.get("near_duplicate_row_count", 0),
            "failure_row_count": metadata.get("failure_row_count", 0),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "backend sequence-search audits verify review-only evidence only; "
                "they do not authorize external label import"
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


def build_external_source_active_site_sourcing_resolution(
    *,
    active_site_sourcing_export: dict[str, Any],
    max_rows: int = 100,
    fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
) -> dict[str, Any]:
    """Resolve active-site source packets against UniProt feature evidence only."""
    source_rows = [
        row
        for row in active_site_sourcing_export.get("rows", []) or []
        if isinstance(row, dict)
    ][:max_rows]
    rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    explicit_active_site_count = 0
    binding_context_only_count = 0
    primary_source_required_count = 0
    evidence_reference_count = 0

    for source_row in source_rows:
        accession = _normalize_accession(source_row.get("accession"))
        if not accession:
            continue
        record: dict[str, Any] = {}
        try:
            payload = fetcher(accession)
            candidate = payload.get("record", payload)
            if isinstance(candidate, dict):
                record = candidate
            else:
                raise ValueError("UniProt payload did not contain a record")
        except Exception as exc:  # pragma: no cover - live network failure path
            fetch_failures.append(
                {
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )

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
        status = _external_active_site_sourcing_resolution_status(
            active_features=active_features,
            binding_features=binding_features,
            catalytic_comments=catalytic_comments,
            fetch_failed=not bool(record),
        )
        status_counts[status] += 1
        if active_features:
            explicit_active_site_count += 1
        elif binding_features or (
            source_row.get("active_site_gap_request_status")
            == "binding_context_mapped_ready_for_active_site_sourcing"
        ):
            binding_context_only_count += 1
        else:
            primary_source_required_count += 1
        evidence_reference_count += _external_feature_evidence_reference_count(
            active_features + binding_features
        )
        rows.append(
            {
                "accession": accession,
                "active_site_gap_request_status": source_row.get(
                    "active_site_gap_request_status"
                ),
                "active_site_source_status": status,
                "blockers": _external_active_site_sourcing_resolution_blockers(
                    status
                ),
                "binding_site_feature_count": len(binding_features),
                "catalytic_activity_count": len(catalytic_comments),
                "countable_label_candidate": False,
                "entry_id": source_row.get("entry_id") or f"uniprot:{accession}",
                "explicit_active_site_feature_count": len(active_features),
                "lane_id": source_row.get("lane_id"),
                "protein_name": source_row.get("protein_name"),
                "queue_status": source_row.get("queue_status"),
                "ready_for_label_import": False,
                "review_status": "active_site_sourcing_resolution_review_only",
                "scope_signal": source_row.get("scope_signal"),
                "source_task": source_row.get("source_task"),
                "sourced_active_site_positions": _external_sourced_active_site_positions(
                    active_features
                ),
                "uniprot_entry_name": record.get("entry_name"),
                "uniprot_review_status": record.get("entry_type"),
            }
        )

    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_resolution",
            "source_active_site_sourcing_method": active_site_sourcing_export.get(
                "metadata", {}
            ).get("method"),
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "explicit_active_site_source_count": explicit_active_site_count,
            "binding_context_only_count": binding_context_only_count,
            "primary_source_required_count": primary_source_required_count,
            "import_ready_row_count": len(import_ready_rows),
            "fetch_failure_count": len(fetch_failures),
            "feature_evidence_reference_count": evidence_reference_count,
            "active_site_source_status_counts": dict(sorted(status_counts.items())),
            "review_only_rule": (
                "active-site sourcing resolutions summarize source evidence only; "
                "they cannot create countable labels or import-ready rows"
            ),
        },
        "rows": rows,
        "fetch_failures": fetch_failures,
        "blockers": [
            "external_review_decision_artifact_not_built",
            "full_label_factory_gate_not_run",
        ],
        "warnings": [
            (
                "explicit active-site positions, when present, still require "
                "mapping, review decisions, and the full label-factory gate"
            )
        ],
    }


def audit_external_source_active_site_sourcing_resolution(
    *,
    active_site_sourcing_resolution: dict[str, Any],
    active_site_sourcing_export: dict[str, Any],
) -> dict[str, Any]:
    """Verify active-site sourcing resolutions remain review-only evidence."""
    rows = [
        row
        for row in active_site_sourcing_resolution.get("rows", []) or []
        if isinstance(row, dict)
    ]
    expected_count = int(
        active_site_sourcing_export.get("metadata", {}).get("candidate_count", 0) or 0
    )
    countable_rows = [
        row for row in rows if row.get("countable_label_candidate") is not False
    ]
    import_ready_rows = [
        row for row in rows if row.get("ready_for_label_import") is not False
    ]
    missing_status_rows = [row for row in rows if not row.get("active_site_source_status")]
    missing_review_status_rows = [
        row
        for row in rows
        if row.get("review_status") != "active_site_sourcing_resolution_review_only"
    ]
    blockers: list[str] = []
    if not rows:
        blockers.append("empty_active_site_sourcing_resolution")
    if expected_count and len(rows) != expected_count:
        blockers.append("active_site_sourcing_resolution_missing_export_rows")
    if countable_rows:
        blockers.append("active_site_sourcing_resolution_rows_marked_countable")
    if import_ready_rows:
        blockers.append("active_site_sourcing_resolution_rows_marked_ready_for_import")
    if missing_status_rows:
        blockers.append("active_site_sourcing_resolution_rows_missing_source_status")
    if missing_review_status_rows:
        blockers.append("active_site_sourcing_resolution_rows_not_review_only")
    return {
        "metadata": {
            "method": "external_source_active_site_sourcing_resolution_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_export_candidate_count": expected_count,
            "import_ready_row_count": len(import_ready_rows),
            "missing_source_status_row_count": len(missing_status_rows),
            "missing_review_only_status_row_count": len(missing_review_status_rows),
            "explicit_active_site_source_count": active_site_sourcing_resolution.get(
                "metadata", {}
            ).get("explicit_active_site_source_count", 0),
            "fetch_failure_count": active_site_sourcing_resolution.get(
                "metadata", {}
            ).get("fetch_failure_count", 0),
            "guardrail_clean": not blockers,
        },
        "blockers": blockers,
        "warnings": [
            (
                "active-site source resolutions are review-only and cannot "
                "authorize external label import"
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
    backend_sequence_search: dict[str, Any] | None = None,
    max_rows: int = 100,
    artifact_lineage: dict[str, Any] | None = None,
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
    backend_sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (backend_sequence_search or {}).get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
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
            backend_sequence_search=backend_sequence_by_accession.get(accession),
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
                "backend_sequence_search_status": (
                    backend_sequence_by_accession.get(accession, {}).get(
                        "search_status"
                    )
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
            "backend_sequence_search_candidate_count": len(
                backend_sequence_by_accession
            ),
            "backend_sequence_no_signal_count": sum(
                1
                for row in backend_sequence_by_accession.values()
                if row.get("search_status") == "no_near_duplicate_signal"
            ),
            "source_backend_sequence_search_method": (
                (backend_sequence_search or {}).get("metadata", {}).get("method")
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
            "artifact_lineage": artifact_lineage or {},
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
    backend_sequence_search: dict[str, Any] | None = None,
    active_site_sourcing_resolution: dict[str, Any] | None = None,
    representation_backend_sample: dict[str, Any] | None = None,
    max_rows: int = 100,
    artifact_lineage: dict[str, Any] | None = None,
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
    backend_sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (backend_sequence_search or {}).get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    active_site_resolution_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (active_site_sourcing_resolution or {}).get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    backend_sample_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (representation_backend_sample or {}).get("rows", []) or []
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
        active_site_resolution = active_site_resolution_by_accession.get(accession)
        backend_sample = backend_sample_by_accession.get(accession)
        blockers = _external_transfer_blocker_matrix_blockers(
            readiness=readiness,
            active_site=active_site,
            sequence=sequence,
            backend=backend,
            backend_sequence_search=backend_sequence_by_accession.get(accession),
            active_site_resolution=active_site_resolution,
            backend_sample=backend_sample,
        )
        prioritized_action = _external_transfer_blocker_matrix_next_action(
            readiness=readiness,
            active_site=active_site,
            sequence=sequence,
            backend=backend,
            backend_sequence_search=backend_sequence_by_accession.get(accession),
            active_site_resolution=active_site_resolution,
            backend_sample=backend_sample,
        )
        rows.append(
            {
                "accession": accession,
                "active_site_sourcing": _external_transfer_blocker_matrix_active_site(
                    active_site,
                    active_site_resolution=active_site_resolution,
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
                    _external_transfer_blocker_matrix_backend(
                        backend,
                        backend_sample=backend_sample,
                    )
                ),
                "review_status": "external_transfer_blocker_matrix_review_only",
                "scope_signal": manifest_row.get("scope_signal"),
                "sequence_search": _external_transfer_blocker_matrix_sequence(
                    sequence,
                    backend_sequence_search=backend_sequence_by_accession.get(
                        accession
                    ),
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
            "source_active_site_sourcing_resolution_method": (
                (active_site_sourcing_resolution or {}).get("metadata", {}).get("method")
            ),
            "source_sequence_search_method": sequence_search_export.get(
                "metadata", {}
            ).get("method"),
            "source_representation_backend_method": representation_backend_plan.get(
                "metadata", {}
            ).get("method"),
            "source_representation_backend_sample_method": (
                (representation_backend_sample or {}).get("metadata", {}).get("method")
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "active_site_sourcing_export_candidate_count": len(
                active_site_by_accession
            ),
            "active_site_sourcing_resolution_candidate_count": len(
                active_site_resolution_by_accession
            ),
            "sequence_search_export_candidate_count": len(sequence_by_accession),
            "backend_sequence_search_candidate_count": len(
                backend_sequence_by_accession
            ),
            "backend_sequence_search_no_signal_count": sum(
                1
                for row in backend_sequence_by_accession.values()
                if row.get("search_status") == "no_near_duplicate_signal"
            ),
            "backend_sequence_search_exact_reference_count": sum(
                1
                for row in backend_sequence_by_accession.values()
                if row.get("search_status") == "exact_reference_holdout"
            ),
            "source_backend_sequence_search_method": (
                (backend_sequence_search or {}).get("metadata", {}).get("method")
            ),
            "representation_backend_plan_candidate_count": len(backend_by_accession),
            "representation_backend_sample_candidate_count": len(
                backend_sample_by_accession
            ),
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
            "artifact_lineage": artifact_lineage or {},
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
    manifest_accessions = sorted(
        {
            _normalize_accession(row.get("accession"))
            for row in candidate_manifest.get("rows", []) or []
            if isinstance(row, dict) and _normalize_accession(row.get("accession"))
        }
    )
    matrix_accessions = sorted(
        {
            _normalize_accession(row.get("accession"))
            for row in rows
            if _normalize_accession(row.get("accession"))
        }
    )
    missing_manifest_accessions = sorted(set(manifest_accessions) - set(matrix_accessions))
    extra_matrix_accessions = sorted(set(matrix_accessions) - set(manifest_accessions))
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
    active_site_resolution_rows = [
        row
        for row in rows
        if row.get("active_site_sourcing", {}).get("resolution_status")
    ]
    representation_sample_rows = [
        row
        for row in rows
        if row.get("representation_backend", {}).get("sample_backend_status")
    ]
    representation_near_duplicate_rows = [
        row
        for row in representation_sample_rows
        if row.get("representation_backend", {}).get("sample_near_duplicate_alert")
        is True
    ]
    blockers: list[str] = []
    metadata = transfer_blocker_matrix.get("metadata", {})
    expected_active_site_resolution_count = int(
        metadata.get("active_site_sourcing_resolution_candidate_count", 0) or 0
    )
    expected_representation_sample_count = int(
        metadata.get("representation_backend_sample_candidate_count", 0) or 0
    )
    if not rows:
        blockers.append("empty_external_transfer_blocker_matrix")
    if expected_candidate_count and len(rows) != expected_candidate_count:
        blockers.append("external_transfer_blocker_matrix_missing_candidates")
    if manifest_accessions and (
        missing_manifest_accessions or extra_matrix_accessions
    ):
        blockers.append("external_transfer_blocker_matrix_candidate_lineage_mismatch")
    if (
        candidate_manifest.get("metadata", {}).get("method")
        and metadata.get("source_candidate_manifest_method")
        != candidate_manifest.get("metadata", {}).get("method")
    ):
        blockers.append("external_transfer_blocker_matrix_source_method_mismatch")
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
    if (
        expected_active_site_resolution_count
        and len(active_site_resolution_rows) != expected_active_site_resolution_count
    ):
        blockers.append(
            "external_transfer_blocker_matrix_active_site_resolution_mismatch"
        )
    if (
        expected_representation_sample_count
        and len(representation_sample_rows) != expected_representation_sample_count
    ):
        blockers.append(
            "external_transfer_blocker_matrix_representation_sample_mismatch"
        )
    return {
        "metadata": {
            "method": "external_source_transfer_blocker_matrix_audit",
            "ready_for_label_import": False,
            "countable_label_candidate_count": len(countable_rows),
            "candidate_count": len(rows),
            "expected_candidate_count": expected_candidate_count,
            "manifest_accession_count": len(manifest_accessions),
            "matrix_accession_count": len(matrix_accessions),
            "missing_manifest_accessions": missing_manifest_accessions,
            "extra_matrix_accessions": extra_matrix_accessions,
            "source_candidate_manifest_method": metadata.get(
                "source_candidate_manifest_method"
            ),
            "expected_candidate_manifest_method": candidate_manifest.get(
                "metadata", {}
            ).get("method"),
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
            "active_site_resolution_row_count": len(active_site_resolution_rows),
            "expected_active_site_resolution_row_count": (
                expected_active_site_resolution_count
            ),
            "representation_sample_row_count": len(representation_sample_rows),
            "expected_representation_sample_row_count": (
                expected_representation_sample_count
            ),
            "representation_near_duplicate_alert_count": len(
                representation_near_duplicate_rows
            ),
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


def build_external_source_pilot_candidate_priority(
    transfer_blocker_matrix: dict[str, Any],
    *,
    max_candidates: int = 10,
    max_per_lane: int = 2,
) -> dict[str, Any]:
    """Rank external candidates for the first focused review pilot.

    The output is a review worklist, not an import decision. It favors rows with
    fewer scientific blockers while preserving lane diversity and explicitly
    carrying the next blocker that prevents countable import.
    """
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    if max_per_lane < 1:
        raise ValueError("max_per_lane must be positive")

    ranked_rows: list[dict[str, Any]] = []
    for row in transfer_blocker_matrix.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        accession = _normalize_accession(row.get("accession"))
        if not accession:
            continue
        blockers = sorted(
            str(blocker) for blocker in row.get("blockers", []) or [] if blocker
        )
        lane_id = str(row.get("lane_id") or "unknown")
        representation = row.get("representation_backend", {}) or {}
        sequence = row.get("sequence_search", {}) or {}
        active_site = row.get("active_site_sourcing", {}) or {}
        pilot_priority_blockers = _external_pilot_candidate_selection_blockers(
            blockers=blockers,
            representation=representation,
        )
        priority_score = _external_pilot_candidate_priority_score(
            row=row,
            blockers=blockers,
        )
        ranked_rows.append(
            {
                "accession": accession,
                "active_site_sourcing": active_site,
                "blockers": blockers,
                "countable_label_candidate": False,
                "entry_id": row.get("entry_id") or f"uniprot:{accession}",
                "eligible_for_review_pilot": not pilot_priority_blockers,
                "lane_id": lane_id,
                "leakage_provenance": _external_pilot_leakage_provenance(row),
                "pilot_priority_score": priority_score,
                "pilot_priority_blockers": pilot_priority_blockers,
                "prioritized_action": row.get("prioritized_action"),
                "protein_name": row.get("protein_name"),
                "ready_for_label_import": False,
                "readiness_status": row.get("readiness_status"),
                "representation_backend": representation,
                "review_status": "external_pilot_candidate_priority_review_only",
                "selection_rationale": _external_pilot_candidate_rationale(
                    row=row,
                    blockers=blockers,
                    priority_score=priority_score,
                ),
                "sequence_search": sequence,
            }
        )

    ranked_rows.sort(
        key=lambda row: (
            not bool(row.get("eligible_for_review_pilot")),
            -float(row.get("pilot_priority_score", 0.0) or 0.0),
            str(row.get("lane_id") or ""),
            str(row.get("accession") or ""),
        )
    )

    lane_counts: Counter[str] = Counter()
    selected_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    for row in ranked_rows:
        lane_id = str(row.get("lane_id") or "unknown")
        if not row.get("eligible_for_review_pilot"):
            deferred_rows.append(
                {
                    **row,
                    "pilot_selection_status": "deferred_by_holdout_or_near_duplicate",
                }
            )
        elif (
            len(selected_rows) < max_candidates
            and lane_counts[lane_id] < max_per_lane
        ):
            row = {**row, "pilot_selection_status": "selected_for_review_pilot"}
            selected_rows.append(row)
            lane_counts[lane_id] += 1
        else:
            deferred_rows.append(
                {**row, "pilot_selection_status": "deferred_by_rank_or_lane_balance"}
            )

    selected_accessions = [row["accession"] for row in selected_rows]
    return {
        "metadata": {
            "method": "external_source_pilot_candidate_priority",
            "source_method": transfer_blocker_matrix.get("metadata", {}).get(
                "method"
            ),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(ranked_rows),
            "eligible_candidate_count": sum(
                1 for row in ranked_rows if row.get("eligible_for_review_pilot")
            ),
            "holdout_or_near_duplicate_deferred_count": sum(
                1 for row in ranked_rows if row.get("pilot_priority_blockers")
            ),
            "max_candidates": max_candidates,
            "max_per_lane": max_per_lane,
            "selected_candidate_count": len(selected_rows),
            "selected_accessions": selected_accessions,
            "selected_lane_counts": dict(sorted(lane_counts.items())),
            "blocker_removed": "external_pilot_candidate_ranking",
            "predictive_feature_sources": [
                "blocker_names",
                "blocker_count",
                "sequence_alignment_status",
                "active_site_sourcing_status",
                "representation_backend_status",
                "representation_near_duplicate_alert",
                "lane_balance",
            ],
            "leakage_policy": {
                "text_or_label_fields_used_for_priority": False,
                "excluded_predictive_fields": [
                    "mechanism_text",
                    "label",
                    "source_label",
                    "target_label",
                    "ec_number",
                    "ec",
                    "rhea_id",
                    "rhea_ids",
                    "reaction_text",
                    "mechanism_summary",
                ],
                "review_context_only": [
                    "protein_name",
                    "prioritized_action",
                    "blockers",
                    "sequence_search",
                    "active_site_sourcing",
                    "representation_backend",
                ],
            },
            "selection_rule": (
                "rank review-only external candidates by fewer import blockers, "
                "clean sequence-holdout status, non-near-duplicate representation "
                "sample status, active-site sourcing readiness, and lane balance; "
                "defer exact sequence holdouts and near-duplicate alerts; do not "
                "mark any candidate countable or import-ready"
            ),
        },
        "rows": selected_rows,
        "deferred_rows": deferred_rows,
        "warnings": [
            (
                "pilot priority rows are a review worklist only; complete "
                "near-duplicate sequence search, active-site evidence, review "
                "decisions, and full label-factory gates remain required"
            )
        ],
    }


def _external_pilot_leakage_provenance(row: dict[str, Any]) -> dict[str, Any]:
    excluded_fields = [
        "mechanism_text",
        "label",
        "source_label",
        "target_label",
        "ec_number",
        "ec",
        "rhea_id",
        "rhea_ids",
        "reaction_text",
        "mechanism_summary",
    ]
    present_review_context = [
        field for field in excluded_fields if row.get(field) not in (None, "", [])
    ]
    return {
        "predictive_feature_sources": [
            "blocker_names",
            "sequence_alignment_status",
            "active_site_sourcing_status",
            "representation_backend_status",
            "representation_near_duplicate_alert",
        ],
        "present_text_or_label_context_fields": present_review_context,
        "text_or_label_fields_used_for_priority": False,
    }


def build_external_source_pilot_review_decision_export(
    *,
    pilot_candidate_priority: dict[str, Any],
    max_rows: int = 10,
) -> dict[str, Any]:
    """Export no-decision review packets for selected external pilot candidates."""
    if max_rows < 1:
        raise ValueError("max_rows must be positive")
    selected_rows = [
        row
        for row in pilot_candidate_priority.get("rows", []) or []
        if isinstance(row, dict)
        and row.get("pilot_selection_status") == "selected_for_review_pilot"
    ][:max_rows]

    review_items: list[dict[str, Any]] = []
    for rank, row in enumerate(selected_rows, start=1):
        accession = _normalize_accession(row.get("accession"))
        blockers = sorted(
            str(blocker) for blocker in row.get("blockers", []) or [] if blocker
        )
        review_items.append(
            {
                "accession": accession,
                "active_site_sourcing": row.get("active_site_sourcing", {}),
                "blockers": blockers,
                "countable_label_candidate": False,
                "decision": {
                    "decision_status": "no_decision",
                    "external_source_resolution": "needs_more_evidence",
                    "ready_for_label_import": False,
                    "reviewer": "",
                    "reviewed_at": "",
                    "rationale": "",
                    "proposed_fingerprint_id": "",
                    "proposed_label_tier": "",
                },
                "entry_id": row.get("entry_id") or f"uniprot:{accession}",
                "lane_id": row.get("lane_id"),
                "pilot_priority_score": row.get("pilot_priority_score"),
                "pilot_selection_status": row.get("pilot_selection_status"),
                "protein_name": row.get("protein_name"),
                "rank": rank,
                "ready_for_label_import": False,
                "representation_backend": row.get("representation_backend", {}),
                "review_requirements": list(
                    EXTERNAL_PILOT_IMPORT_REVIEW_REQUIREMENTS
                ),
                "review_status": "external_pilot_review_decision_no_decision",
                "sequence_search": row.get("sequence_search", {}),
            }
        )

    return {
        "metadata": {
            "method": "external_source_pilot_review_decision_export",
            "source_method": pilot_candidate_priority.get("metadata", {}).get(
                "method"
            ),
            "blocker_removed": "external_pilot_review_decision_export_scaffold",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(review_items),
            "max_rows": max_rows,
            "decision_status_counts": {"no_decision": len(review_items)},
            "completed_decision_count": 0,
            "review_only": True,
        },
        "review_items": review_items,
        "warnings": [
            (
                "pilot review-decision exports are no-decision packets only; "
                "they do not authorize countable import"
            )
        ],
    }


def build_external_source_pilot_evidence_packet(
    *,
    pilot_candidate_priority: dict[str, Any],
    active_site_sourcing_export: dict[str, Any],
    sequence_search_export: dict[str, Any],
    backend_sequence_search: dict[str, Any] | None = None,
    max_rows: int = 10,
    artifact_lineage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Join source-review targets for the selected external pilot rows."""
    if max_rows < 1:
        raise ValueError("max_rows must be positive")

    selected_rows = [
        row
        for row in pilot_candidate_priority.get("rows", []) or []
        if isinstance(row, dict)
        and row.get("pilot_selection_status") == "selected_for_review_pilot"
    ][:max_rows]
    active_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in active_site_sourcing_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in sequence_search_export.get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }
    backend_sequence_by_accession = {
        _normalize_accession(row.get("accession")): row
        for row in (backend_sequence_search or {}).get("rows", []) or []
        if isinstance(row, dict) and _normalize_accession(row.get("accession"))
    }

    rows: list[dict[str, Any]] = []
    missing_sequence_accessions: list[str] = []
    missing_required_active_site_accessions: list[str] = []
    source_type_counts: Counter[str] = Counter()
    active_site_packet_count = 0
    sequence_packet_count = 0
    target_count = 0

    for rank, priority_row in enumerate(selected_rows, start=1):
        accession = _normalize_accession(priority_row.get("accession"))
        active_row = active_by_accession.get(accession)
        sequence_row = sequence_by_accession.get(accession)
        backend_sequence_row = backend_sequence_by_accession.get(accession)
        active_site_context = priority_row.get("active_site_sourcing", {}) or {}
        active_site_task = str(active_site_context.get("source_task") or "")
        requires_active_site_packet = (
            active_site_task
            and active_site_task != "not_active_site_sourcing_row"
        )
        if sequence_row is None:
            missing_sequence_accessions.append(accession)
        if requires_active_site_packet and active_row is None:
            missing_required_active_site_accessions.append(accession)

        source_targets: list[dict[str, Any]] = []
        for target in (sequence_row or {}).get("source_targets", []) or []:
            if isinstance(target, dict):
                source_targets.append({**target, "evidence_track": "sequence_search"})
        for target in (active_row or {}).get("source_targets", []) or []:
            if isinstance(target, dict):
                source_targets.append({**target, "evidence_track": "active_site"})

        for target in source_targets:
            source_type_counts[str(target.get("source_type") or "unknown")] += 1
        target_count += len(source_targets)
        if active_row is not None:
            active_site_packet_count += 1
        if sequence_row is not None:
            sequence_packet_count += 1

        row_blockers = sorted(
            {
                str(blocker)
                for blocker in priority_row.get("blockers", []) or []
                if blocker
            }
        )
        if sequence_row is None:
            row_blockers.append("selected_pilot_sequence_packet_missing")
        if requires_active_site_packet and active_row is None:
            row_blockers.append("selected_pilot_active_site_packet_missing")
        sequence_context = _external_pilot_sequence_packet_context(
            sequence_row=sequence_row,
            priority_sequence=priority_row.get("sequence_search", {}),
            backend_sequence_row=backend_sequence_row,
        )

        rows.append(
            {
                "accession": accession,
                "active_site_sourcing": active_row
                or active_site_context
                or {"source_task": "not_active_site_sourcing_row"},
                "blockers": sorted(set(row_blockers)),
                "countable_label_candidate": False,
                "entry_id": priority_row.get("entry_id") or f"uniprot:{accession}",
                "lane_id": priority_row.get("lane_id"),
                "pilot_priority_score": priority_row.get("pilot_priority_score"),
                "pilot_selection_status": priority_row.get("pilot_selection_status"),
                "protein_name": priority_row.get("protein_name"),
                "rank": rank,
                "ready_for_label_import": False,
                "representation_backend": priority_row.get(
                    "representation_backend", {}
                ),
                "review_status": "external_pilot_evidence_packet_review_only",
                "review_requirements": list(
                    EXTERNAL_PILOT_IMPORT_REVIEW_REQUIREMENTS
                ),
                "sequence_search": sequence_context,
                "source_targets": source_targets,
            }
        )

    guardrail_clean = (
        not missing_sequence_accessions
        and not missing_required_active_site_accessions
        and all(row.get("source_targets") for row in rows)
        and all(not row.get("countable_label_candidate") for row in rows)
        and all(not row.get("ready_for_label_import") for row in rows)
    )
    blockers: list[str] = []
    if missing_sequence_accessions:
        blockers.append("selected_pilot_sequence_packets_missing")
    if missing_required_active_site_accessions:
        blockers.append("selected_pilot_active_site_packets_missing")
    if any(not row.get("source_targets") for row in rows):
        blockers.append("selected_pilot_source_targets_missing")

    return {
        "metadata": {
            "method": "external_source_pilot_evidence_packet",
            "source_pilot_candidate_priority_method": (
                pilot_candidate_priority.get("metadata", {}).get("method")
            ),
            "source_active_site_sourcing_export_method": (
                active_site_sourcing_export.get("metadata", {}).get("method")
            ),
            "source_sequence_search_export_method": (
                sequence_search_export.get("metadata", {}).get("method")
            ),
            "source_backend_sequence_search_method": (
                (backend_sequence_search or {}).get("metadata", {}).get("method")
            ),
            "blocker_removed": "external_pilot_source_packet_consolidation",
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "selected_accessions": [row["accession"] for row in rows],
            "active_site_sourcing_packet_count": active_site_packet_count,
            "sequence_search_packet_count": sequence_packet_count,
            "backend_sequence_search_packet_count": sum(
                1
                for row in rows
                if (row.get("sequence_search") or {}).get("backend_search_status")
            ),
            "backend_sequence_search_no_signal_count": sum(
                1
                for row in rows
                if (row.get("sequence_search") or {}).get("backend_search_status")
                == "no_near_duplicate_signal"
            ),
            "source_target_count": target_count,
            "source_target_type_counts": dict(sorted(source_type_counts.items())),
            "missing_sequence_export_accessions": sorted(missing_sequence_accessions),
            "missing_required_active_site_export_accessions": sorted(
                missing_required_active_site_accessions
            ),
            "artifact_lineage": artifact_lineage or {},
            "guardrail_clean": guardrail_clean,
            "blockers": blockers,
            "review_only": True,
        },
        "rows": rows,
        "warnings": [
            (
                "pilot evidence packets consolidate source targets only; they do "
                "not complete review decisions or authorize countable import"
            )
        ],
    }


def _external_pilot_sequence_packet_context(
    *,
    sequence_row: dict[str, Any] | None,
    priority_sequence: Any,
    backend_sequence_row: dict[str, Any] | None,
) -> dict[str, Any]:
    sequence_context = (
        dict(sequence_row)
        if isinstance(sequence_row, dict)
        else dict(priority_sequence)
        if isinstance(priority_sequence, dict)
        else {}
    )
    decision = sequence_context.get("decision")
    if isinstance(decision, dict) and "decision_status" not in sequence_context:
        sequence_context["decision_status"] = decision.get("decision_status")
    if backend_sequence_row:
        sequence_context.update(
            {
                "backend_name": backend_sequence_row.get("backend_name"),
                "backend_search_complete": backend_sequence_row.get(
                    "backend_search_complete"
                ),
                "backend_search_status": backend_sequence_row.get("search_status"),
                "backend_max_external_vs_reference_identity": (
                    backend_sequence_row.get("max_external_vs_reference_identity")
                ),
                "backend_sequence_search": {
                    "backend_name": backend_sequence_row.get("backend_name"),
                    "backend_search_complete": backend_sequence_row.get(
                        "backend_search_complete"
                    ),
                    "max_external_vs_reference_identity": backend_sequence_row.get(
                        "max_external_vs_reference_identity"
                    ),
                    "review_status": backend_sequence_row.get("review_status"),
                    "search_status": backend_sequence_row.get("search_status"),
                },
            }
        )
    return sequence_context


def build_external_source_pilot_evidence_dossiers(
    *,
    pilot_evidence_packet: dict[str, Any],
    active_site_evidence_sample: dict[str, Any],
    active_site_sourcing_resolution: dict[str, Any],
    reaction_evidence_sample: dict[str, Any],
    sequence_alignment_verification: dict[str, Any],
    representation_backend_sample: dict[str, Any],
    heuristic_control_scores: dict[str, Any],
    structure_mapping_sample: dict[str, Any],
    transfer_blocker_matrix: dict[str, Any],
    external_import_readiness_audit: dict[str, Any] | None = None,
    artifact_lineage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble per-candidate review dossiers for the selected external pilot."""

    active_site_features = _external_rows_by_accession(active_site_evidence_sample)
    active_site_sourcing = _external_first_row_by_accession(
        active_site_sourcing_resolution
    )
    reactions = _external_rows_by_accession(reaction_evidence_sample)
    alignments = _external_rows_by_accession(sequence_alignment_verification)
    representation = _external_first_row_by_accession(representation_backend_sample)
    heuristic = _external_first_row_by_accession(heuristic_control_scores)
    structure = _external_first_row_by_accession(structure_mapping_sample)
    matrix = _external_first_row_by_accession(transfer_blocker_matrix)
    readiness = _external_first_row_by_accession(external_import_readiness_audit or {})

    rows: list[dict[str, Any]] = []
    for packet_row in pilot_evidence_packet.get("rows", []) or []:
        if not isinstance(packet_row, dict):
            continue
        accession = _normalize_accession(packet_row.get("accession"))
        if not accession:
            continue
        active_rows = active_site_features.get(accession, [])
        reaction_rows = reactions.get(accession, [])
        alignment_rows = alignments.get(accession, [])
        matrix_row = matrix.get(accession, {})
        readiness_row = readiness.get(accession, {})
        representation_row = representation.get(accession, {})
        heuristic_row = heuristic.get(accession, {})
        structure_row = structure.get(accession, {})
        sourcing_row = active_site_sourcing.get(accession, {})
        blockers = _external_pilot_dossier_blockers(
            packet_row=packet_row,
            active_site_rows=active_rows,
            reaction_rows=reaction_rows,
            matrix_row=matrix_row,
            readiness_row=readiness_row,
            representation_row=representation_row,
            sourcing_row=sourcing_row,
            alignment_rows=alignment_rows,
        )
        row = {
            "rank": packet_row.get("rank"),
            "accession": accession,
            "entry_id": packet_row.get("entry_id") or f"uniprot:{accession}",
            "protein_name": packet_row.get("protein_name"),
            "lane_id": packet_row.get("lane_id"),
            "countable_label_candidate": False,
            "ready_for_label_import": False,
            "review_status": "external_pilot_evidence_dossier_review_only",
            "pilot_priority_score": packet_row.get("pilot_priority_score"),
            "prioritized_action": matrix_row.get("prioritized_action")
            or packet_row.get("prioritized_action"),
            "readiness_status": readiness_row.get("readiness_status")
            or matrix_row.get("readiness_status")
            or packet_row.get("readiness_status"),
            "active_site_evidence": _external_pilot_active_site_summary(
                feature_rows=active_rows,
                sourcing_row=sourcing_row,
            ),
            "reaction_evidence": _external_pilot_reaction_summary(reaction_rows),
            "sequence_evidence": _external_pilot_sequence_summary(
                packet_row=packet_row,
                alignment_rows=alignment_rows,
            ),
            "structure_mapping": _external_pilot_structure_summary(structure_row),
            "heuristic_control": _external_pilot_heuristic_summary(heuristic_row),
            "representation_control": _external_pilot_representation_summary(
                representation_row
            ),
            "remaining_blockers": blockers,
            "evidence_dossier_status": (
                "blocked_before_import" if blockers else "ready_for_review_decision"
            ),
        }
        rows.append(row)

    active_site_ready_count = sum(
        1
        for row in rows
        if row["active_site_evidence"]["explicit_active_site_feature_count"] > 0
    )
    reaction_context_count = sum(
        1 for row in rows if row["reaction_evidence"]["reaction_record_count"] > 0
    )
    representation_sample_count = sum(
        1
        for row in rows
        if row["representation_control"]["backend_status"] not in (None, "missing")
    )
    local_blocker_counts = Counter(
        blocker
        for row in rows
        for blocker in row["remaining_blockers"]
        if blocker.startswith("pilot_")
    )
    return {
        "metadata": {
            "method": "external_source_pilot_evidence_dossier",
            "blocker_removed": "external_pilot_per_candidate_evidence_dossier_assembly",
            "review_policy": {
                "semantics": "review_only_non_countable",
                "expert_review_status": "no_decision",
                "countable_import_rule": (
                    "external candidates require explicit active-site evidence, "
                    "specific reaction or mechanism review, complete sequence "
                    "near-duplicate controls, leakage-safe representation "
                    "controls, review decisions, and full label-factory gates"
                ),
            },
            "source_pilot_evidence_packet_method": pilot_evidence_packet.get(
                "metadata", {}
            ).get("method"),
            "source_transfer_blocker_matrix_method": transfer_blocker_matrix.get(
                "metadata", {}
            ).get("method"),
            "source_representation_backend_sample_method": (
                representation_backend_sample.get("metadata", {}).get("method")
            ),
            "artifact_lineage": artifact_lineage or {},
            "candidate_count": len(rows),
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "review_only": True,
            "active_site_feature_supported_candidate_count": active_site_ready_count,
            "reaction_context_candidate_count": reaction_context_count,
            "representation_sample_candidate_count": representation_sample_count,
            "candidate_with_remaining_blocker_count": sum(
                1 for row in rows if row["remaining_blockers"]
            ),
            "local_evidence_blocker_counts": dict(sorted(local_blocker_counts.items())),
            "pilot_explicit_active_site_evidence_missing_count": local_blocker_counts.get(
                "pilot_explicit_active_site_evidence_missing", 0
            ),
            "pilot_specific_reaction_context_missing_count": local_blocker_counts.get(
                "pilot_specific_reaction_context_missing", 0
            ),
            "pilot_sequence_near_duplicate_alert_count": local_blocker_counts.get(
                "pilot_sequence_near_duplicate_alert_present", 0
            ),
            "selected_accessions": [row["accession"] for row in rows],
        },
        "rows": sorted(rows, key=lambda row: (int(row.get("rank") or 9999), row["accession"])),
        "warnings": [
            (
                "dossiers assemble existing review evidence only; they do not "
                "complete expert decisions or authorize countable import"
            )
        ],
    }


def build_external_source_pilot_active_site_evidence_decisions(
    *,
    pilot_evidence_dossiers: dict[str, Any],
    pilot_evidence_packet: dict[str, Any],
    active_site_sourcing_resolution: dict[str, Any],
    reaction_evidence_sample: dict[str, Any],
    backend_sequence_search: dict[str, Any],
    pilot_representation_backend_sample: dict[str, Any],
    transfer_blocker_matrix: dict[str, Any],
    max_rows: int = 10,
    artifact_lineage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify pilot active-site evidence without making review decisions."""
    if max_rows < 1:
        raise ValueError("max_rows must be positive")

    packets = _external_first_row_by_accession(pilot_evidence_packet)
    sourcing = _external_first_row_by_accession(active_site_sourcing_resolution)
    reactions = _external_rows_by_accession(reaction_evidence_sample)
    sequence = _external_first_row_by_accession(backend_sequence_search)
    representation = _external_first_row_by_accession(
        pilot_representation_backend_sample
    )
    matrix = _external_first_row_by_accession(transfer_blocker_matrix)

    rows: list[dict[str, Any]] = []
    for dossier in (pilot_evidence_dossiers.get("rows", []) or [])[:max_rows]:
        if not isinstance(dossier, dict):
            continue
        accession = _normalize_accession(dossier.get("accession"))
        if not accession:
            continue
        packet_row = packets.get(accession, {})
        sourcing_row = sourcing.get(accession, {})
        reaction_rows = reactions.get(accession, [])
        sequence_row = sequence.get(accession, {})
        representation_row = representation.get(accession, {})
        matrix_row = matrix.get(accession, {})
        active_site_summary = dossier.get("active_site_evidence", {})
        if not isinstance(active_site_summary, dict):
            active_site_summary = {}
        reaction_status = _external_pilot_reaction_evidence_status(
            dossier.get("reaction_evidence", {}),
            reaction_rows,
        )
        sequence_status = _external_pilot_sequence_decision_status(
            dossier.get("sequence_evidence", {}),
            sequence_row,
        )
        representation_status = _external_pilot_representation_decision_status(
            dossier.get("representation_control", {}),
            representation_row,
            matrix_row,
        )
        source_category = _external_pilot_active_site_source_category(
            active_site_summary,
            sourcing_row,
        )
        decision_status = _external_pilot_active_site_decision_status(
            source_category=source_category,
            sequence_status=sequence_status,
        )
        blockers = _external_pilot_active_site_decision_blockers(
            dossier=dossier,
            source_category=source_category,
            reaction_status=reaction_status,
            sequence_status=sequence_status,
            representation_status=representation_status,
        )
        rows.append(
            {
                "rank": dossier.get("rank"),
                "accession": accession,
                "entry_id": dossier.get("entry_id") or f"uniprot:{accession}",
                "protein_name": dossier.get("protein_name"),
                "lane_id": dossier.get("lane_id"),
                "selected_for_review_pilot": True,
                "pilot_selection_status": (
                    packet_row.get("pilot_selection_status")
                    or "selected_for_review_pilot"
                ),
                "countable_label_candidate": False,
                "ready_for_label_import": False,
                "review_status": (
                    "external_pilot_active_site_evidence_decision_review_only"
                ),
                "decision_class": "review_only_evidence_status",
                "active_site_evidence_decision_status": decision_status,
                "active_site_evidence_source_category": source_category,
                "active_site_source_status": (
                    sourcing_row.get("active_site_source_status")
                    or active_site_summary.get("sourcing_status")
                ),
                "explicit_active_site_feature_count": int(
                    active_site_summary.get("explicit_active_site_feature_count", 0)
                    or 0
                ),
                "sourced_active_site_position_count": int(
                    active_site_summary.get("sourced_active_site_position_count", 0)
                    or len(sourcing_row.get("sourced_active_site_positions", []) or [])
                ),
                "binding_site_feature_count": int(
                    active_site_summary.get("binding_site_feature_count", 0)
                    or sourcing_row.get("binding_site_feature_count", 0)
                    or 0
                ),
                "active_site_feature_positions": active_site_summary.get(
                    "feature_positions", []
                ),
                "reaction_mechanism_evidence_status": reaction_status,
                "reaction_record_count": int(
                    (dossier.get("reaction_evidence", {}) or {}).get(
                        "reaction_record_count", 0
                    )
                    or len(reaction_rows)
                ),
                "specific_reaction_record_count": int(
                    (dossier.get("reaction_evidence", {}) or {}).get(
                        "specific_reaction_record_count", 0
                    )
                    or sum(
                        1
                        for row in reaction_rows
                        if row.get("ec_specificity") == "specific"
                    )
                ),
                "rhea_ids": (dossier.get("reaction_evidence", {}) or {}).get(
                    "rhea_ids", []
                ),
                "sequence_holdout_backend_search_status": sequence_status,
                "backend_sequence_search_status": sequence_row.get("search_status")
                or (dossier.get("sequence_evidence", {}) or {}).get(
                    "backend_search_status"
                ),
                "backend_sequence_search_complete": sequence_row.get(
                    "backend_search_complete"
                )
                if sequence_row
                else (dossier.get("sequence_evidence", {}) or {}).get(
                    "backend_search_complete"
                ),
                "backend_sequence_backend_name": sequence_row.get("backend_name")
                or (dossier.get("sequence_evidence", {}) or {}).get("backend_name"),
                "broader_duplicate_screening_status": (
                    "broader_duplicate_screening_required"
                ),
                "representation_control_status": representation_status,
                "representation_backend_status": representation_row.get(
                    "backend_status"
                )
                or (dossier.get("representation_control", {}) or {}).get(
                    "backend_status"
                ),
                "representation_comparison_status": representation_row.get(
                    "comparison_status"
                )
                or (dossier.get("representation_control", {}) or {}).get(
                    "comparison_status"
                ),
                "import_readiness_blockers": blockers,
                "next_action": _external_pilot_active_site_decision_next_action(
                    source_category=source_category,
                    sequence_status=sequence_status,
                    representation_status=representation_status,
                ),
            }
        )

    status_counts = Counter(
        row["active_site_evidence_decision_status"] for row in rows
    )
    source_counts = Counter(row["active_site_evidence_source_category"] for row in rows)
    reaction_counts = Counter(row["reaction_mechanism_evidence_status"] for row in rows)
    sequence_counts = Counter(row["sequence_holdout_backend_search_status"] for row in rows)
    representation_counts = Counter(row["representation_control_status"] for row in rows)
    blocker_counts = Counter(
        blocker for row in rows for blocker in row["import_readiness_blockers"]
    )
    return {
        "metadata": {
            "method": "external_source_pilot_active_site_evidence_decisions",
            "blocker_removed": (
                "external_pilot_active_site_source_status_ambiguity"
            ),
            "blocker_not_removed": [
                "explicit_active_site_residue_sources_absent",
                "broader_duplicate_screening_required",
                "external_review_decision_artifact_not_built",
                "full_label_factory_gate_not_run",
            ],
            "source_pilot_evidence_dossiers_method": pilot_evidence_dossiers.get(
                "metadata", {}
            ).get("method"),
            "source_pilot_evidence_packet_method": pilot_evidence_packet.get(
                "metadata", {}
            ).get("method"),
            "source_active_site_sourcing_resolution_method": (
                active_site_sourcing_resolution.get("metadata", {}).get("method")
            ),
            "source_reaction_evidence_sample_method": reaction_evidence_sample.get(
                "metadata", {}
            ).get("method"),
            "source_backend_sequence_search_method": backend_sequence_search.get(
                "metadata", {}
            ).get("method"),
            "source_representation_backend_sample_method": (
                pilot_representation_backend_sample.get("metadata", {}).get("method")
            ),
            "source_transfer_blocker_matrix_method": transfer_blocker_matrix.get(
                "metadata", {}
            ).get("method"),
            "artifact_lineage": artifact_lineage or {},
            "review_only": True,
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
            "import_ready_row_count": 0,
            "completed_decision_count": 0,
            "accepted_decision_count": 0,
            "candidate_count": len(rows),
            "max_rows": max_rows,
            "selected_accessions": [row["accession"] for row in rows],
            "decision_status_counts": dict(sorted(status_counts.items())),
            "active_site_evidence_source_category_counts": dict(
                sorted(source_counts.items())
            ),
            "reaction_mechanism_evidence_status_counts": dict(
                sorted(reaction_counts.items())
            ),
            "sequence_holdout_backend_search_status_counts": dict(
                sorted(sequence_counts.items())
            ),
            "representation_control_status_counts": dict(
                sorted(representation_counts.items())
            ),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "candidate_with_import_readiness_blocker_count": sum(
                1 for row in rows if row["import_readiness_blockers"]
            ),
            "explicit_active_site_source_present_count": source_counts.get(
                "explicit_active_site_source_present", 0
            ),
            "no_explicit_active_site_source_count": len(rows)
            - source_counts.get("explicit_active_site_source_present", 0),
            "broader_duplicate_screening_required_count": sum(
                1
                for row in rows
                if row["broader_duplicate_screening_status"]
                == "broader_duplicate_screening_required"
            ),
        },
        "rows": sorted(
            rows, key=lambda row: (int(row.get("rank") or 9999), row["accession"])
        ),
        "warnings": [
            (
                "pilot active-site evidence decisions classify source evidence only; "
                "they are not accepted review decisions and cannot authorize import"
            )
        ],
    }


def _external_pilot_active_site_source_category(
    active_site_summary: dict[str, Any],
    sourcing_row: dict[str, Any],
) -> str:
    explicit_count = int(
        active_site_summary.get("explicit_active_site_feature_count", 0) or 0
    ) + int(active_site_summary.get("sourced_active_site_position_count", 0) or 0)
    explicit_count += len(sourcing_row.get("sourced_active_site_positions", []) or [])
    if explicit_count > 0:
        return "explicit_active_site_source_present"
    status = str(
        sourcing_row.get("active_site_source_status")
        or active_site_summary.get("sourcing_status")
        or ""
    )
    binding_count = int(active_site_summary.get("binding_site_feature_count", 0) or 0)
    binding_count += int(sourcing_row.get("binding_site_feature_count", 0) or 0)
    if "binding" in status or binding_count > 0:
        return "binding_context_only"
    if "reaction_context_only" in status:
        return "reaction_context_only"
    return "no_explicit_active_site_source"


def _external_pilot_active_site_decision_status(
    *,
    source_category: str,
    sequence_status: str,
) -> str:
    if sequence_status == "sequence_holdout":
        return "sequence_holdout"
    return source_category


def _external_pilot_reaction_evidence_status(
    reaction_summary: Any,
    reaction_rows: list[dict[str, Any]],
) -> str:
    summary = reaction_summary if isinstance(reaction_summary, dict) else {}
    specific_count = int(summary.get("specific_reaction_record_count", 0) or 0)
    if specific_count == 0:
        specific_count = sum(
            1 for row in reaction_rows if row.get("ec_specificity") == "specific"
        )
    if specific_count > 0:
        return "specific_reaction_context_present"
    reaction_count = int(summary.get("reaction_record_count", 0) or 0) or len(
        reaction_rows
    )
    if reaction_count > 0:
        return "reaction_context_only"
    return "reaction_or_mechanism_evidence_missing"


def _external_pilot_sequence_decision_status(
    sequence_summary: Any,
    backend_sequence_row: dict[str, Any],
) -> str:
    summary = sequence_summary if isinstance(sequence_summary, dict) else {}
    backend_status = str(
        backend_sequence_row.get("search_status")
        or summary.get("backend_search_status")
        or ""
    )
    if backend_status in {"exact_reference_holdout", "near_duplicate_holdout"}:
        return "sequence_holdout"
    if int(summary.get("alignment_alert_count", 0) or 0) > 0:
        return "sequence_holdout"
    backend_complete = backend_sequence_row.get("backend_search_complete")
    if backend_complete is None:
        backend_complete = summary.get("backend_search_complete")
    if backend_complete is True and backend_status == "no_near_duplicate_signal":
        return "current_reference_backend_no_signal"
    return "backend_sequence_search_incomplete"


def _external_pilot_representation_decision_status(
    representation_summary: Any,
    representation_row: dict[str, Any],
    matrix_row: dict[str, Any],
) -> str:
    summary = representation_summary if isinstance(representation_summary, dict) else {}
    blockers = {
        str(blocker)
        for blocker in (matrix_row.get("blockers", []) or [])
        + (representation_row.get("blockers", []) or [])
        + (summary.get("blockers", []) or [])
        if blocker
    }
    backend_status = str(
        representation_row.get("backend_status")
        or summary.get("backend_status")
        or ""
    )
    comparison_status = str(
        representation_row.get("comparison_status")
        or summary.get("comparison_status")
        or ""
    )
    if backend_status == "representation_near_duplicate_holdout":
        return "representation_near_duplicate_holdout"
    if any(blocker.startswith("representation_control_") for blocker in blockers):
        return "representation_control_issue"
    if backend_status in {"", "missing"}:
        return "representation_control_issue"
    if comparison_status in {
        "proxy_consistent_with_heuristic_scope",
        "pilot_sequence_embedding_control",
        "pilot_sequence_embedding_without_feature_proxy_comparison",
    }:
        return "pilot_representation_control_review_only"
    return "representation_control_issue"


def _external_pilot_active_site_decision_blockers(
    *,
    dossier: dict[str, Any],
    source_category: str,
    reaction_status: str,
    sequence_status: str,
    representation_status: str,
) -> list[str]:
    blockers = {
        str(blocker) for blocker in dossier.get("remaining_blockers", []) or [] if blocker
    }
    if source_category != "explicit_active_site_source_present":
        blockers.add("explicit_active_site_residue_sources_absent")
    if reaction_status != "specific_reaction_context_present":
        blockers.add("specific_reaction_or_mechanism_evidence_missing")
    if sequence_status == "sequence_holdout":
        blockers.add("sequence_holdout")
    elif sequence_status != "current_reference_backend_no_signal":
        blockers.add("backend_sequence_search_incomplete")
    blockers.add("broader_duplicate_screening_required")
    if representation_status in {
        "representation_control_issue",
        "representation_near_duplicate_holdout",
    }:
        blockers.add(representation_status)
    blockers.add("external_review_decision_artifact_not_built")
    blockers.add("full_label_factory_gate_not_run")
    return sorted(blockers)


def _external_pilot_active_site_decision_next_action(
    *,
    source_category: str,
    sequence_status: str,
    representation_status: str,
) -> str:
    if sequence_status == "sequence_holdout":
        return "keep_sequence_holdout_out_of_import_batch"
    if source_category == "binding_context_only":
        return "curate_primary_literature_or_pdb_active_site_sources"
    if source_category != "explicit_active_site_source_present":
        return "source_explicit_active_site_residue_positions"
    if representation_status in {
        "representation_control_issue",
        "representation_near_duplicate_holdout",
    }:
        return "compute_or_attach_real_representation_control"
    return "complete_broader_duplicate_screening_before_review_decision"


def _external_rows_by_accession(artifact: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows_by_accession: dict[str, list[dict[str, Any]]] = {}
    for row in _external_artifact_candidate_rows(artifact):
        accession = _external_row_accession(row)
        if accession:
            rows_by_accession.setdefault(accession, []).append(row)
    return rows_by_accession


def _external_first_row_by_accession(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        accession: rows[0]
        for accession, rows in _external_rows_by_accession(artifact).items()
        if rows
    }


def _external_row_accession(row: dict[str, Any]) -> str:
    accession = _normalize_accession(row.get("accession"))
    if not accession and isinstance(row.get("external_source_context"), dict):
        accession = _normalize_accession(
            row.get("external_source_context", {}).get("accession")
        )
    if not accession:
        entry_id = str(row.get("entry_id") or "")
        if entry_id.startswith("uniprot:"):
            accession = _normalize_accession(entry_id.split(":", 1)[1])
    return accession


def _external_pilot_active_site_summary(
    *,
    feature_rows: list[dict[str, Any]],
    sourcing_row: dict[str, Any],
) -> dict[str, Any]:
    active_rows = [
        row
        for row in feature_rows
        if str(row.get("feature_type") or "").lower() == "active site"
    ]
    binding_rows = [
        row
        for row in feature_rows
        if str(row.get("feature_type") or "").lower() == "binding site"
    ]
    return {
        "explicit_active_site_feature_count": len(active_rows),
        "binding_site_feature_count": len(binding_rows)
        or int(sourcing_row.get("binding_site_feature_count", 0) or 0),
        "sourcing_status": sourcing_row.get("active_site_source_status"),
        "sourced_active_site_position_count": len(
            sourcing_row.get("sourced_active_site_positions", []) or []
        ),
        "source_task": sourcing_row.get("source_task"),
        "feature_positions": [
            {
                "begin": row.get("begin"),
                "end": row.get("end"),
                "description": row.get("description"),
                "evidence": row.get("evidence", []),
            }
            for row in active_rows[:5]
        ],
    }


def _external_pilot_reaction_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    specific_rows = [
        row for row in rows if row.get("ec_specificity") == "specific"
    ]
    broad_rows = [
        row for row in rows if row.get("ec_specificity") != "specific"
    ]
    return {
        "reaction_record_count": len(rows),
        "specific_reaction_record_count": len(specific_rows),
        "broad_or_incomplete_reaction_record_count": len(broad_rows),
        "ec_numbers": sorted({str(row.get("ec_number")) for row in rows if row.get("ec_number")}),
        "rhea_ids": sorted({str(row.get("rhea_id")) for row in rows if row.get("rhea_id")})[:8],
        "sample_equations": [row.get("equation") for row in specific_rows[:3] if row.get("equation")],
    }


def _external_pilot_sequence_summary(
    *,
    packet_row: dict[str, Any],
    alignment_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    sequence_packet = packet_row.get("sequence_search", {}) or {}
    alert_rows = [
        row
        for row in alignment_rows
        if row.get("verification_status")
        in {
            "alignment_exact_reference_holdout",
            "alignment_near_duplicate_candidate_holdout",
        }
    ]
    top_rows = sorted(
        alignment_rows,
        key=lambda row: (
            -float(row.get("alignment_identity", 0.0) or 0.0),
            str(row.get("reference_accession") or ""),
        ),
    )[:3]
    return {
        "search_task": sequence_packet.get("search_task"),
        "decision_status": sequence_packet.get("decision_status"),
        "backend_name": sequence_packet.get("backend_name"),
        "backend_search_complete": sequence_packet.get("backend_search_complete"),
        "backend_search_status": sequence_packet.get("backend_search_status"),
        "backend_max_external_vs_reference_identity": sequence_packet.get(
            "backend_max_external_vs_reference_identity"
        ),
        "alignment_checked_pair_count": len(alignment_rows),
        "alignment_alert_count": len(alert_rows),
        "top_alignment_hits": [
            {
                "reference_accession": row.get("reference_accession"),
                "alignment_identity": row.get("alignment_identity"),
                "length_coverage": row.get("length_coverage"),
                "verification_status": row.get("verification_status"),
                "matched_m_csa_entry_ids": row.get("matched_m_csa_entry_ids", []),
            }
            for row in top_rows
        ],
    }


def _external_pilot_structure_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": row.get("status") or "not_mapped_for_heuristic_control",
        "structure_id": row.get("structure_id"),
        "structure_source": row.get("structure_source"),
        "resolved_residue_count": int(row.get("resolved_residue_count", 0) or 0),
        "missing_active_site_positions": row.get("missing_active_site_positions", []),
    }


def _external_pilot_heuristic_summary(row: dict[str, Any]) -> dict[str, Any]:
    top = [
        item for item in (row.get("top_fingerprints", []) or []) if isinstance(item, dict)
    ]
    top1 = top[0] if top else {}
    return {
        "scored": bool(top),
        "top1_fingerprint_id": top1.get("fingerprint_id"),
        "top1_score": top1.get("score"),
        "scope_top1_mismatch": row.get("scope_top1_mismatch"),
    }


def _external_pilot_representation_summary(row: dict[str, Any]) -> dict[str, Any]:
    nearest = row.get("nearest_reference", {}) if isinstance(row, dict) else {}
    if not isinstance(nearest, dict):
        nearest = {}
    return {
        "backend_status": row.get("backend_status") or "missing",
        "embedding_status": row.get("embedding_status"),
        "top_embedding_cosine": row.get("top_embedding_cosine"),
        "comparison_status": row.get("comparison_status"),
        "nearest_reference_accession": nearest.get("reference_accession"),
        "nearest_reference_entry_id": nearest.get("entry_id"),
        "blockers": row.get("blockers", []) if isinstance(row, dict) else [],
    }


def _external_pilot_dossier_blockers(
    *,
    packet_row: dict[str, Any],
    active_site_rows: list[dict[str, Any]],
    reaction_rows: list[dict[str, Any]],
    matrix_row: dict[str, Any],
    readiness_row: dict[str, Any],
    representation_row: dict[str, Any],
    sourcing_row: dict[str, Any],
    alignment_rows: list[dict[str, Any]],
) -> list[str]:
    blockers: set[str] = set()
    for row in (packet_row, matrix_row, readiness_row, representation_row, sourcing_row):
        for blocker in row.get("blockers", []) or []:
            blockers.add(str(blocker))
    backend_no_signal = _external_pilot_backend_no_signal(
        packet_row=packet_row,
        matrix_row=matrix_row,
        readiness_row=readiness_row,
    )
    explicit_active_site_count = sum(
        1
        for row in active_site_rows
        if str(row.get("feature_type") or "").lower() == "active site"
    ) + len(sourcing_row.get("sourced_active_site_positions", []) or [])
    if explicit_active_site_count == 0:
        blockers.add("pilot_explicit_active_site_evidence_missing")
    if not any(row.get("ec_specificity") == "specific" for row in reaction_rows):
        blockers.add("pilot_specific_reaction_context_missing")
    if not alignment_rows and not backend_no_signal:
        blockers.add("complete_near_duplicate_sequence_search_not_completed")
    if any(
        row.get("verification_status")
        in {
            "alignment_exact_reference_holdout",
            "alignment_near_duplicate_candidate_holdout",
        }
        for row in alignment_rows
    ):
        blockers.add("pilot_sequence_near_duplicate_alert_present")
    representation_status = representation_row.get("backend_status")
    if representation_status in (None, "missing"):
        blockers.add("representation_backend_sample_missing_for_candidate")
    else:
        for stale_representation_blocker in (
            "external_embeddings_not_computed",
            "representation_backend_not_selected",
            "representation_backend_plan_missing_or_not_eligible",
        ):
            blockers.discard(stale_representation_blocker)
    if backend_no_signal:
        for stale_sequence_blocker in (
            "complete_near_duplicate_search_required",
            "complete_near_duplicate_reference_search_not_completed",
            "complete_near_duplicate_sequence_search_not_completed",
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
        ):
            blockers.discard(stale_sequence_blocker)
    return sorted(blockers)


def _external_pilot_backend_no_signal(
    *,
    packet_row: dict[str, Any],
    matrix_row: dict[str, Any],
    readiness_row: dict[str, Any],
) -> bool:
    packet_sequence = packet_row.get("sequence_search", {})
    if not isinstance(packet_sequence, dict):
        packet_sequence = {}
    matrix_sequence = matrix_row.get("sequence_search", {})
    if not isinstance(matrix_sequence, dict):
        matrix_sequence = {}
    backend_statuses = {
        str(packet_sequence.get("backend_search_status") or ""),
        str(matrix_sequence.get("backend_search_status") or ""),
        str(readiness_row.get("backend_sequence_search_status") or ""),
    }
    return "no_near_duplicate_signal" in backend_statuses


def _external_pilot_candidate_selection_blockers(
    *,
    blockers: list[str],
    representation: dict[str, Any],
) -> list[str]:
    blocker_set = set(blockers)
    pilot_blockers: list[str] = []
    if "exact_sequence_holdout" in blocker_set:
        pilot_blockers.append("exact_sequence_holdout")
    if "sequence_alignment_near_duplicate_candidate_holdout" in blocker_set:
        pilot_blockers.append("sequence_alignment_near_duplicate_candidate_holdout")
    if "representation_near_duplicate_control_holdout" in blocker_set:
        pilot_blockers.append("representation_near_duplicate_control_holdout")
    if representation.get("sample_near_duplicate_alert") is True:
        pilot_blockers.append("representation_sample_near_duplicate_alert")
    return sorted(set(pilot_blockers))


def _external_transfer_candidate_lineage(
    candidate_manifest: dict[str, Any],
    artifacts: dict[str, dict[str, Any] | None],
) -> dict[str, Any]:
    manifest_accessions = _external_artifact_accessions(candidate_manifest)
    unexpected_accessions: dict[str, list[str]] = {}
    missing_accessions: dict[str, list[str]] = {}
    count_mismatch_artifacts: list[str] = []
    checked_artifacts: list[str] = []

    for artifact_name, artifact in artifacts.items():
        if artifact is None:
            continue
        accessions = _external_artifact_accessions(artifact)
        if not accessions:
            continue
        checked_artifacts.append(artifact_name)
        extras = sorted(accessions - manifest_accessions)
        if extras:
            unexpected_accessions[artifact_name] = extras

        metadata = artifact.get("metadata", {}) if isinstance(artifact, dict) else {}
        candidate_count = metadata.get("candidate_count")
        try:
            candidate_count_int = int(candidate_count)
        except (TypeError, ValueError):
            candidate_count_int = None
        if candidate_count_int is not None and candidate_count_int != len(accessions):
            count_mismatch_artifacts.append(artifact_name)

        if manifest_accessions and candidate_count_int == len(manifest_accessions):
            missing = sorted(manifest_accessions - accessions)
            if missing:
                missing_accessions[artifact_name] = missing

    blockers: list[str] = []
    if unexpected_accessions:
        blockers.append("external_transfer_candidate_lineage_unexpected_accessions")
    if missing_accessions:
        blockers.append("external_transfer_candidate_lineage_missing_accessions")
    if count_mismatch_artifacts:
        blockers.append("external_transfer_candidate_lineage_count_mismatch")

    return {
        "method": "external_transfer_candidate_lineage_validation",
        "candidate_manifest_accession_count": len(manifest_accessions),
        "checked_artifacts": sorted(checked_artifacts),
        "unexpected_accessions": unexpected_accessions,
        "missing_accessions": missing_accessions,
        "count_mismatch_artifacts": sorted(count_mismatch_artifacts),
        "blockers": blockers,
        "guardrail_clean": not blockers,
    }


def validate_external_transfer_artifact_path_lineage(
    artifact_paths: dict[str, str | None],
    loaded_artifacts: dict[str, dict[str, Any] | None] | None = None,
    *,
    fail_fast: bool = False,
) -> dict[str, Any]:
    """Validate that high-fan-in external-transfer inputs share one slice lineage."""

    path_slice_ids: dict[str, int] = {}
    payload_slice_ids: dict[str, dict[str, int]] = {}
    payload_methods: dict[str, str] = {}
    artifact_paths_present: dict[str, str] = {}
    missing_slice_id_artifacts: list[str] = []
    conflicting_payload_artifacts: dict[str, dict[str, int]] = {}
    payload_path_mismatch_artifacts: dict[str, dict[str, int]] = {}
    slice_members: dict[int, set[str]] = {}

    for artifact_name, path in artifact_paths.items():
        if not path:
            continue
        path_string = str(path)
        artifact_paths_present[artifact_name] = path_string
        path_slice_id = _infer_external_transfer_slice_id(path_string)
        if path_slice_id is not None:
            path_slice_ids[artifact_name] = path_slice_id
            slice_members.setdefault(path_slice_id, set()).add(artifact_name)

        artifact = (loaded_artifacts or {}).get(artifact_name)
        payload_lineage = (
            _external_transfer_payload_lineage(artifact)
            if isinstance(artifact, dict)
            else {}
        )
        if isinstance(artifact, dict):
            metadata = artifact.get("metadata", {})
            if isinstance(metadata, dict) and isinstance(metadata.get("method"), str):
                payload_methods[artifact_name] = str(metadata["method"])
        if payload_lineage:
            payload_slice_ids[artifact_name] = dict(sorted(payload_lineage.items()))
            payload_values = set(payload_lineage.values())
            if len(payload_values) > 1:
                conflicting_payload_artifacts[artifact_name] = dict(
                    sorted(payload_lineage.items())
                )
            else:
                payload_slice_id = next(iter(payload_values))
                if path_slice_id is None:
                    slice_members.setdefault(payload_slice_id, set()).add(
                        artifact_name
                    )
                elif payload_slice_id != path_slice_id:
                    payload_path_mismatch_artifacts[artifact_name] = {
                        "path_slice_id": path_slice_id,
                        "payload_slice_id": payload_slice_id,
                    }
        elif path_slice_id is None:
            missing_slice_id_artifacts.append(artifact_name)

    blockers: list[str] = []
    if len(slice_members) > 1:
        blockers.append("external_transfer_artifact_path_slice_mismatch")
    if conflicting_payload_artifacts:
        blockers.append("external_transfer_artifact_payload_conflicting_slice_ids")
    if payload_path_mismatch_artifacts:
        blockers.append("external_transfer_artifact_payload_path_slice_mismatch")

    lineage = {
        "method": "external_transfer_artifact_path_lineage_validation",
        "slice_id": next(iter(slice_members), None) if len(slice_members) == 1 else None,
        "artifact_paths": dict(sorted(artifact_paths_present.items())),
        "path_slice_ids": dict(sorted(path_slice_ids.items())),
        "payload_slice_ids": dict(sorted(payload_slice_ids.items())),
        "payload_methods": dict(sorted(payload_methods.items())),
        "missing_slice_id_artifacts": sorted(missing_slice_id_artifacts),
        "conflicting_payload_artifacts": dict(
            sorted(conflicting_payload_artifacts.items())
        ),
        "payload_path_mismatch_artifacts": dict(
            sorted(payload_path_mismatch_artifacts.items())
        ),
        "slice_members": {
            str(slice_id): sorted(names)
            for slice_id, names in sorted(slice_members.items())
        },
        "blockers": blockers,
        "guardrail_clean": not blockers,
    }
    if fail_fast and blockers:
        details = "; ".join(
            f"{slice_id}: {', '.join(sorted(names))}"
            for slice_id, names in sorted(slice_members.items())
        )
        raise ValueError(
            "mismatched external transfer artifact lineage: "
            f"{', '.join(blockers)}"
            + (f" ({details})" if details else "")
        )
    return lineage


def _infer_external_transfer_slice_id(path: str | None) -> int | None:
    if not path:
        return None
    matches = _EXTERNAL_TRANSFER_ARTIFACT_SLICE_RE.findall(str(path).split("/")[-1])
    return int(matches[-1]) if matches else None


def _external_transfer_payload_lineage(
    artifact: dict[str, Any],
) -> dict[str, int]:
    metadata = artifact.get("metadata", {})
    if not isinstance(metadata, dict):
        return {}
    lineage: dict[str, int] = {}
    for key in _EXTERNAL_TRANSFER_PAYLOAD_LINEAGE_KEYS:
        parsed = _parse_external_transfer_lineage_int(metadata.get(key))
        if parsed is not None:
            lineage[f"metadata.{key}"] = parsed
    artifact_lineage = metadata.get("artifact_lineage")
    if isinstance(artifact_lineage, dict):
        for key in _EXTERNAL_TRANSFER_PAYLOAD_LINEAGE_KEYS:
            parsed = _parse_external_transfer_lineage_int(artifact_lineage.get(key))
            if parsed is not None:
                lineage[f"metadata.artifact_lineage.{key}"] = parsed
    return lineage


def _parse_external_transfer_lineage_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        match = re.match(r"^(\d+)(?:\D|$)", value.strip())
        if match:
            return int(match.group(1))
    return None


def _merge_external_transfer_lineage(
    candidate_lineage: dict[str, Any],
    artifact_path_lineage: dict[str, Any] | None,
) -> dict[str, Any]:
    if not artifact_path_lineage:
        return candidate_lineage
    blockers = sorted(
        set(candidate_lineage.get("blockers", []))
        | set(artifact_path_lineage.get("blockers", []))
    )
    return {
        **candidate_lineage,
        "artifact_path_lineage": artifact_path_lineage,
        "blockers": blockers,
        "guardrail_clean": not blockers,
    }


def _external_artifact_accessions(artifact: dict[str, Any]) -> set[str]:
    accessions: set[str] = set()
    for row in _external_artifact_candidate_rows(artifact):
        accession = _normalize_accession(row.get("accession"))
        if not accession and isinstance(row.get("external_source_context"), dict):
            accession = _normalize_accession(
                row.get("external_source_context", {}).get("accession")
            )
        if not accession:
            entry_id = str(row.get("entry_id") or "")
            if entry_id.startswith("uniprot:"):
                accession = _normalize_accession(entry_id.split(":", 1)[1])
        if accession:
            accessions.add(accession)
    return accessions


def _external_artifact_candidate_rows(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in (
        "rows",
        "deferred_rows",
        "candidate_summaries",
        "entries",
        "results",
        "review_items",
    ):
        values = artifact.get(key, []) if isinstance(artifact, dict) else []
        if isinstance(values, list):
            rows.extend(row for row in values if isinstance(row, dict))
    return rows


def _external_pilot_candidate_priority_score(
    *,
    row: dict[str, Any],
    blockers: list[str],
) -> float:
    blocker_set = set(blockers)
    score = 100.0
    score -= 2.0 * len(blocker_set)
    if "exact_sequence_holdout" in blocker_set:
        score -= 60.0
    if "sequence_alignment_near_duplicate_candidate_holdout" in blocker_set:
        score -= 35.0
    if "complete_near_duplicate_search_required" in blocker_set:
        score -= 8.0
    if "external_active_site_feature_gap" in blocker_set:
        score -= 12.0
    if "external_active_site_evidence_not_sampled" in blocker_set:
        score -= 16.0
    if "heuristic_metal_hydrolase_collapse" in blocker_set:
        score -= 10.0
    if "heuristic_scope_top1_mismatch" in blocker_set:
        score -= 8.0
    if any("broad_ec" in blocker for blocker in blocker_set):
        score -= 10.0
    representation = row.get("representation_backend", {}) or {}
    if representation.get("sample_near_duplicate_alert") is True:
        score -= 25.0
    elif (
        representation.get("sample_backend_status")
        == "learned_representation_sample_complete"
    ):
        score += 8.0
    active_site = row.get("active_site_sourcing", {}) or {}
    if active_site.get("queue_status") == "ready_for_curated_active_site_sourcing":
        score += 6.0
    if (
        active_site.get("source_task")
        == "curate_active_site_positions_from_mapped_binding_context"
    ):
        score += 4.0
    sequence = row.get("sequence_search", {}) or {}
    if sequence.get("alignment_status") == "alignment_no_near_duplicate_signal":
        score += 4.0
    return round(score, 3)


def _external_pilot_candidate_rationale(
    *,
    row: dict[str, Any],
    blockers: list[str],
    priority_score: float,
) -> str:
    action = row.get("prioritized_action") or "complete_external_review"
    blocker_count = len(blockers)
    representation = row.get("representation_backend", {}) or {}
    active_site = row.get("active_site_sourcing", {}) or {}
    sequence = row.get("sequence_search", {}) or {}
    return (
        f"score={priority_score}; next_action={action}; blockers={blocker_count}; "
        f"active_site_source_task={active_site.get('source_task')}; "
        f"sequence_status={sequence.get('alignment_status')}; "
        f"representation_status={representation.get('sample_backend_status')}"
    )


def _external_pilot_review_only_gate_checks(
    *,
    pilot_candidate_priority: dict[str, Any] | None,
    pilot_review_decision_export: dict[str, Any] | None,
    pilot_evidence_packet: dict[str, Any] | None,
    pilot_evidence_dossiers: dict[str, Any] | None,
    pilot_active_site_evidence_decisions: dict[str, Any] | None,
    pilot_representation_backend_sample: dict[str, Any] | None,
) -> dict[str, bool]:
    """Validate pilot artifacts without authorizing import or count growth."""

    gates: dict[str, bool] = {}
    selected_pilot_accessions: set[str] = set()
    if pilot_candidate_priority is not None:
        priority_meta = pilot_candidate_priority.get("metadata", {})
        priority_rows = _external_artifact_candidate_rows(pilot_candidate_priority)
        selected_rows = [
            row
            for row in priority_rows
            if row.get("pilot_selection_status") == "selected_for_review_pilot"
        ]
        selected_pilot_accessions = {
            accession
            for accession in (
                _normalize_accession(row.get("accession")) for row in selected_rows
            )
            if accession
        }
        max_candidates = int(
            priority_meta.get("max_candidates", len(selected_rows)) or 0
        )
        max_per_lane = int(
            priority_meta.get("max_per_lane", len(selected_rows)) or 0
        )
        selected_lane_counts: dict[str, int] = {}
        for row in selected_rows:
            lane_id = str(row.get("lane_id") or "")
            selected_lane_counts[lane_id] = selected_lane_counts.get(lane_id, 0) + 1
        leakage_policy = priority_meta.get("leakage_policy", {})
        if not isinstance(leakage_policy, dict):
            leakage_policy = {}
        gates["external_pilot_candidate_priority_review_only"] = (
            priority_meta.get("ready_for_label_import") is False
            and priority_meta.get("countable_label_candidate_count") == 0
            and int(priority_meta.get("selected_candidate_count", 0) or 0)
            == len(selected_rows)
            and len(selected_rows) > 0
            and len(selected_rows) <= max_candidates
            and all(count <= max_per_lane for count in selected_lane_counts.values())
            and leakage_policy.get("text_or_label_fields_used_for_priority")
            is False
            and all(
                row.get("countable_label_candidate") is False
                for row in selected_rows
            )
            and all(row.get("ready_for_label_import") is False for row in selected_rows)
            and all(row.get("eligible_for_review_pilot") is True for row in selected_rows)
            and all(not row.get("pilot_priority_blockers") for row in selected_rows)
            and all(
                row.get("review_status")
                == "external_pilot_candidate_priority_review_only"
                for row in selected_rows
            )
            and all(
                (row.get("leakage_provenance") or {}).get(
                    "text_or_label_fields_used_for_priority"
                )
                is False
                for row in selected_rows
            )
        )
    if pilot_review_decision_export is not None:
        review_meta = pilot_review_decision_export.get("metadata", {})
        review_items = _external_artifact_candidate_rows(pilot_review_decision_export)
        expected_review_count = (
            pilot_candidate_priority.get("metadata", {}).get("selected_candidate_count")
            if pilot_candidate_priority is not None
            else len(review_items)
        )
        gates["external_pilot_review_decision_export_no_decision"] = (
            review_meta.get("ready_for_label_import") is False
            and review_meta.get("review_only") is True
            and review_meta.get("countable_label_candidate_count") == 0
            and review_meta.get("completed_decision_count") == 0
            and int(review_meta.get("candidate_count", 0) or 0) == len(review_items)
            and int(review_meta.get("candidate_count", 0) or 0)
            == int(expected_review_count or 0)
            and len(review_items) > 0
            and review_meta.get("decision_status_counts", {}).get("no_decision")
            == len(review_items)
            and all(
                row.get("countable_label_candidate") is False for row in review_items
            )
            and all(row.get("ready_for_label_import") is False for row in review_items)
            and all(
                (row.get("decision") or {}).get("decision_status") == "no_decision"
                for row in review_items
            )
            and all(
                (row.get("decision") or {}).get("ready_for_label_import") is False
                for row in review_items
            )
            and all(
                set(EXTERNAL_PILOT_IMPORT_REVIEW_REQUIREMENTS)
                <= set(row.get("review_requirements", []) or [])
                for row in review_items
            )
        )
    if pilot_evidence_packet is not None:
        packet_meta = pilot_evidence_packet.get("metadata", {})
        packet_rows = _external_artifact_candidate_rows(pilot_evidence_packet)
        expected_packet_count = (
            pilot_review_decision_export.get("metadata", {}).get("candidate_count")
            if pilot_review_decision_export is not None
            else (
                pilot_candidate_priority.get("metadata", {}).get(
                    "selected_candidate_count"
                )
                if pilot_candidate_priority is not None
                else len(packet_rows)
            )
        )
        gates["external_pilot_evidence_packet_review_only"] = (
            packet_meta.get("ready_for_label_import") is False
            and packet_meta.get("review_only") is True
            and packet_meta.get("guardrail_clean") is True
            and packet_meta.get("countable_label_candidate_count") == 0
            and int(packet_meta.get("candidate_count", 0) or 0) == len(packet_rows)
            and int(packet_meta.get("candidate_count", 0) or 0)
            == int(expected_packet_count or 0)
            and len(packet_rows) > 0
            and int(packet_meta.get("sequence_search_packet_count", 0) or 0)
            == len(packet_rows)
            and int(packet_meta.get("source_target_count", 0) or 0) > 0
            and not packet_meta.get("missing_sequence_export_accessions")
            and not packet_meta.get("missing_required_active_site_export_accessions")
            and all(
                row.get("countable_label_candidate") is False for row in packet_rows
            )
            and all(row.get("ready_for_label_import") is False for row in packet_rows)
            and all(
                row.get("review_status")
                == "external_pilot_evidence_packet_review_only"
                for row in packet_rows
            )
            and all(row.get("source_targets") for row in packet_rows)
            and all(
                row.get("sequence_search", {})
                .get("decision", {})
                .get("decision_status")
                == "no_decision"
                for row in packet_rows
            )
            and all(
                set(EXTERNAL_PILOT_IMPORT_REVIEW_REQUIREMENTS)
                <= set(row.get("review_requirements", []) or [])
                for row in packet_rows
            )
        )
    if pilot_representation_backend_sample is not None:
        sample_meta = pilot_representation_backend_sample.get("metadata", {})
        sample_rows = _external_artifact_candidate_rows(
            pilot_representation_backend_sample
        )
        sample_accessions = {
            accession
            for accession in (
                _normalize_accession(row.get("accession")) for row in sample_rows
            )
            if accession
        }
        expected_accessions = selected_pilot_accessions or sample_accessions
        allowed_predictive_sources = {
            "sequence_embedding_cosine",
            "sequence_length_coverage",
        }
        sample_predictive_sources = set(
            sample_meta.get("predictive_feature_sources") or []
        )
        gates["external_pilot_representation_sample_review_only"] = (
            sample_meta.get("ready_for_label_import") is False
            and sample_meta.get("countable_label_candidate_count") == 0
            and sample_meta.get("embedding_status") == "computed_review_only"
            and sample_meta.get("embedding_backend_available") is True
            and int(sample_meta.get("candidate_count", 0) or 0) == len(sample_rows)
            and int(sample_meta.get("candidate_count", 0) or 0)
            == len(expected_accessions)
            and len(sample_rows) > 0
            and sample_accessions == expected_accessions
            and bool(sample_predictive_sources)
            and sample_predictive_sources <= allowed_predictive_sources
            and all(
                row.get("countable_label_candidate") is False for row in sample_rows
            )
            and all(row.get("ready_for_label_import") is False for row in sample_rows)
            and all(
                row.get("review_status") == "representation_backend_sample_review_only"
                for row in sample_rows
            )
            and all(
                row.get("embedding_status") == "computed_review_only"
                for row in sample_rows
            )
            and all(
                set(row.get("predictive_feature_sources") or [])
                <= allowed_predictive_sources
                for row in sample_rows
            )
            and all(
                row.get("backend_status")
                in {
                    "learned_representation_sample_complete",
                    "representation_near_duplicate_holdout",
                }
                for row in sample_rows
            )
        )
    if pilot_evidence_dossiers is not None:
        dossier_meta = pilot_evidence_dossiers.get("metadata", {})
        dossier_rows = _external_artifact_candidate_rows(pilot_evidence_dossiers)
        expected_dossier_count = (
            pilot_evidence_packet.get("metadata", {}).get("candidate_count")
            if pilot_evidence_packet is not None
            else len(dossier_rows)
        )
        gates["external_pilot_evidence_dossiers_review_only"] = (
            dossier_meta.get("ready_for_label_import") is False
            and dossier_meta.get("review_only") is True
            and dossier_meta.get("countable_label_candidate_count") == 0
            and int(dossier_meta.get("candidate_count", 0) or 0) == len(dossier_rows)
            and int(dossier_meta.get("candidate_count", 0) or 0)
            == int(expected_dossier_count or 0)
            and len(dossier_rows) > 0
            and all(
                row.get("countable_label_candidate") is False for row in dossier_rows
            )
            and all(row.get("ready_for_label_import") is False for row in dossier_rows)
            and all(
                row.get("review_status")
                == "external_pilot_evidence_dossier_review_only"
                for row in dossier_rows
            )
            and all(row.get("active_site_evidence") for row in dossier_rows)
            and all(row.get("reaction_evidence") for row in dossier_rows)
            and all(row.get("sequence_evidence") for row in dossier_rows)
            and all(row.get("representation_control") for row in dossier_rows)
            and all(
                row.get("evidence_dossier_status")
                in {"blocked_before_import", "ready_for_review_decision"}
                for row in dossier_rows
            )
        )
    if pilot_active_site_evidence_decisions is not None:
        decision_meta = pilot_active_site_evidence_decisions.get("metadata", {})
        decision_rows = _external_artifact_candidate_rows(
            pilot_active_site_evidence_decisions
        )
        decision_accessions = {
            accession
            for accession in (
                _normalize_accession(row.get("accession")) for row in decision_rows
            )
            if accession
        }
        expected_decision_accessions = selected_pilot_accessions or decision_accessions
        allowed_source_categories = {
            "explicit_active_site_source_present",
            "binding_context_only",
            "reaction_context_only",
            "no_explicit_active_site_source",
        }
        allowed_decision_statuses = allowed_source_categories | {"sequence_holdout"}
        gates["external_pilot_active_site_evidence_decisions_review_only"] = (
            decision_meta.get("method")
            == "external_source_pilot_active_site_evidence_decisions"
            and decision_meta.get("blocker_removed")
            == "external_pilot_active_site_source_status_ambiguity"
            and decision_meta.get("ready_for_label_import") is False
            and decision_meta.get("review_only") is True
            and decision_meta.get("countable_label_candidate_count") == 0
            and decision_meta.get("import_ready_row_count") == 0
            and decision_meta.get("completed_decision_count") == 0
            and decision_meta.get("accepted_decision_count") == 0
            and int(decision_meta.get("candidate_count", 0) or 0)
            == len(decision_rows)
            and int(decision_meta.get("candidate_count", 0) or 0)
            == len(expected_decision_accessions)
            and decision_accessions == expected_decision_accessions
            and len(decision_rows) > 0
            and int(
                decision_meta.get(
                    "candidate_with_import_readiness_blocker_count", 0
                )
                or 0
            )
            == len(decision_rows)
            and all(
                row.get("countable_label_candidate") is False for row in decision_rows
            )
            and all(row.get("ready_for_label_import") is False for row in decision_rows)
            and all(
                row.get("review_status")
                == "external_pilot_active_site_evidence_decision_review_only"
                for row in decision_rows
            )
            and all(
                row.get("decision_class") == "review_only_evidence_status"
                for row in decision_rows
            )
            and all(
                row.get("active_site_evidence_source_category")
                in allowed_source_categories
                for row in decision_rows
            )
            and all(
                row.get("active_site_evidence_decision_status")
                in allowed_decision_statuses
                for row in decision_rows
            )
            and all(row.get("import_readiness_blockers") for row in decision_rows)
            and all(
                row.get("broader_duplicate_screening_status")
                == "broader_duplicate_screening_required"
                for row in decision_rows
            )
        )
    return gates


def _coerce_external_source_transfer_gate_inputs(
    gate_inputs: ExternalSourceTransferGateInputs | None,
    **kwargs: dict[str, Any] | None,
) -> ExternalSourceTransferGateInputs:
    if gate_inputs is not None:
        if any(value is not None for value in kwargs.values()):
            raise ValueError(
                "external transfer gate accepts either "
                f"{EXTERNAL_TRANSFER_GATE_INPUT_CONTRACT} or keyword artifacts, not both"
            )
        validate_external_source_transfer_gate_inputs(gate_inputs)
        return gate_inputs
    missing = sorted(
        field_name
        for field_name in EXTERNAL_TRANSFER_GATE_REQUIRED_FIELDS
        if kwargs.get(field_name) is None
    )
    if missing:
        raise ValueError(
            "missing external transfer gate inputs: " + ", ".join(missing)
        )
    coerced = ExternalSourceTransferGateInputs(**kwargs)  # type: ignore[arg-type]
    validate_external_source_transfer_gate_inputs(coerced)
    return coerced


def check_external_source_transfer_gates(
    gate_inputs: ExternalSourceTransferGateInputs | None = None,
    *,
    transfer_manifest: dict[str, Any] | None = None,
    query_manifest: dict[str, Any] | None = None,
    ood_calibration_plan: dict[str, Any] | None = None,
    candidate_sample_audit: dict[str, Any] | None = None,
    candidate_manifest: dict[str, Any] | None = None,
    candidate_manifest_audit: dict[str, Any] | None = None,
    lane_balance_audit: dict[str, Any] | None = None,
    evidence_plan: dict[str, Any] | None = None,
    evidence_request_export: dict[str, Any] | None = None,
    review_only_import_safety_audit: dict[str, Any] | None = None,
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
    representation_backend_sample: dict[str, Any] | None = None,
    representation_backend_sample_audit: dict[str, Any] | None = None,
    broad_ec_disambiguation_audit: dict[str, Any] | None = None,
    active_site_gap_source_requests: dict[str, Any] | None = None,
    sequence_neighborhood_plan: dict[str, Any] | None = None,
    sequence_neighborhood_sample: dict[str, Any] | None = None,
    sequence_neighborhood_sample_audit: dict[str, Any] | None = None,
    sequence_alignment_verification: dict[str, Any] | None = None,
    sequence_alignment_verification_audit: dict[str, Any] | None = None,
    sequence_reference_screen_audit: dict[str, Any] | None = None,
    sequence_search_export: dict[str, Any] | None = None,
    sequence_search_export_audit: dict[str, Any] | None = None,
    external_import_readiness_audit: dict[str, Any] | None = None,
    active_site_sourcing_queue: dict[str, Any] | None = None,
    active_site_sourcing_queue_audit: dict[str, Any] | None = None,
    active_site_sourcing_export: dict[str, Any] | None = None,
    active_site_sourcing_export_audit: dict[str, Any] | None = None,
    active_site_sourcing_resolution: dict[str, Any] | None = None,
    active_site_sourcing_resolution_audit: dict[str, Any] | None = None,
    transfer_blocker_matrix: dict[str, Any] | None = None,
    transfer_blocker_matrix_audit: dict[str, Any] | None = None,
    pilot_candidate_priority: dict[str, Any] | None = None,
    pilot_review_decision_export: dict[str, Any] | None = None,
    pilot_evidence_packet: dict[str, Any] | None = None,
    pilot_evidence_dossiers: dict[str, Any] | None = None,
    pilot_active_site_evidence_decisions: dict[str, Any] | None = None,
    pilot_representation_backend_sample: dict[str, Any] | None = None,
    binding_context_repair_plan: dict[str, Any] | None = None,
    binding_context_repair_plan_audit: dict[str, Any] | None = None,
    binding_context_mapping_sample: dict[str, Any] | None = None,
    binding_context_mapping_sample_audit: dict[str, Any] | None = None,
    sequence_holdout_audit: dict[str, Any] | None = None,
    artifact_path_lineage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Gate external-source transfer artifacts before future label import work."""
    gate_inputs = _coerce_external_source_transfer_gate_inputs(
        gate_inputs,
        transfer_manifest=transfer_manifest,
        query_manifest=query_manifest,
        ood_calibration_plan=ood_calibration_plan,
        candidate_sample_audit=candidate_sample_audit,
        candidate_manifest=candidate_manifest,
        candidate_manifest_audit=candidate_manifest_audit,
        lane_balance_audit=lane_balance_audit,
        evidence_plan=evidence_plan,
        evidence_request_export=evidence_request_export,
        review_only_import_safety_audit=review_only_import_safety_audit,
        active_site_evidence_queue=active_site_evidence_queue,
        active_site_evidence_sample=active_site_evidence_sample,
        active_site_evidence_sample_audit=active_site_evidence_sample_audit,
        heuristic_control_queue=heuristic_control_queue,
        heuristic_control_queue_audit=heuristic_control_queue_audit,
        structure_mapping_plan=structure_mapping_plan,
        structure_mapping_plan_audit=structure_mapping_plan_audit,
        structure_mapping_sample=structure_mapping_sample,
        structure_mapping_sample_audit=structure_mapping_sample_audit,
        heuristic_control_scores=heuristic_control_scores,
        heuristic_control_scores_audit=heuristic_control_scores_audit,
        external_failure_mode_audit=external_failure_mode_audit,
        external_control_repair_plan=external_control_repair_plan,
        external_control_repair_plan_audit=external_control_repair_plan_audit,
        reaction_evidence_sample=reaction_evidence_sample,
        reaction_evidence_sample_audit=reaction_evidence_sample_audit,
        representation_control_manifest=representation_control_manifest,
        representation_control_manifest_audit=representation_control_manifest_audit,
        representation_control_comparison=representation_control_comparison,
        representation_control_comparison_audit=representation_control_comparison_audit,
        representation_backend_plan=representation_backend_plan,
        representation_backend_plan_audit=representation_backend_plan_audit,
        representation_backend_sample=representation_backend_sample,
        representation_backend_sample_audit=representation_backend_sample_audit,
        broad_ec_disambiguation_audit=broad_ec_disambiguation_audit,
        active_site_gap_source_requests=active_site_gap_source_requests,
        sequence_neighborhood_plan=sequence_neighborhood_plan,
        sequence_neighborhood_sample=sequence_neighborhood_sample,
        sequence_neighborhood_sample_audit=sequence_neighborhood_sample_audit,
        sequence_alignment_verification=sequence_alignment_verification,
        sequence_alignment_verification_audit=sequence_alignment_verification_audit,
        sequence_reference_screen_audit=sequence_reference_screen_audit,
        sequence_search_export=sequence_search_export,
        sequence_search_export_audit=sequence_search_export_audit,
        external_import_readiness_audit=external_import_readiness_audit,
        active_site_sourcing_queue=active_site_sourcing_queue,
        active_site_sourcing_queue_audit=active_site_sourcing_queue_audit,
        active_site_sourcing_export=active_site_sourcing_export,
        active_site_sourcing_export_audit=active_site_sourcing_export_audit,
        active_site_sourcing_resolution=active_site_sourcing_resolution,
        active_site_sourcing_resolution_audit=active_site_sourcing_resolution_audit,
        transfer_blocker_matrix=transfer_blocker_matrix,
        transfer_blocker_matrix_audit=transfer_blocker_matrix_audit,
        pilot_candidate_priority=pilot_candidate_priority,
        pilot_review_decision_export=pilot_review_decision_export,
        pilot_evidence_packet=pilot_evidence_packet,
        pilot_evidence_dossiers=pilot_evidence_dossiers,
        pilot_active_site_evidence_decisions=pilot_active_site_evidence_decisions,
        pilot_representation_backend_sample=pilot_representation_backend_sample,
        binding_context_repair_plan=binding_context_repair_plan,
        binding_context_repair_plan_audit=binding_context_repair_plan_audit,
        binding_context_mapping_sample=binding_context_mapping_sample,
        binding_context_mapping_sample_audit=binding_context_mapping_sample_audit,
        sequence_holdout_audit=sequence_holdout_audit,
        artifact_path_lineage=artifact_path_lineage,
    )
    transfer_manifest = gate_inputs.transfer_manifest
    query_manifest = gate_inputs.query_manifest
    ood_calibration_plan = gate_inputs.ood_calibration_plan
    candidate_sample_audit = gate_inputs.candidate_sample_audit
    candidate_manifest = gate_inputs.candidate_manifest
    candidate_manifest_audit = gate_inputs.candidate_manifest_audit
    lane_balance_audit = gate_inputs.lane_balance_audit
    evidence_plan = gate_inputs.evidence_plan
    evidence_request_export = gate_inputs.evidence_request_export
    review_only_import_safety_audit = gate_inputs.review_only_import_safety_audit
    active_site_evidence_queue = gate_inputs.active_site_evidence_queue
    active_site_evidence_sample = gate_inputs.active_site_evidence_sample
    active_site_evidence_sample_audit = gate_inputs.active_site_evidence_sample_audit
    heuristic_control_queue = gate_inputs.heuristic_control_queue
    heuristic_control_queue_audit = gate_inputs.heuristic_control_queue_audit
    structure_mapping_plan = gate_inputs.structure_mapping_plan
    structure_mapping_plan_audit = gate_inputs.structure_mapping_plan_audit
    structure_mapping_sample = gate_inputs.structure_mapping_sample
    structure_mapping_sample_audit = gate_inputs.structure_mapping_sample_audit
    heuristic_control_scores = gate_inputs.heuristic_control_scores
    heuristic_control_scores_audit = gate_inputs.heuristic_control_scores_audit
    external_failure_mode_audit = gate_inputs.external_failure_mode_audit
    external_control_repair_plan = gate_inputs.external_control_repair_plan
    external_control_repair_plan_audit = gate_inputs.external_control_repair_plan_audit
    reaction_evidence_sample = gate_inputs.reaction_evidence_sample
    reaction_evidence_sample_audit = gate_inputs.reaction_evidence_sample_audit
    representation_control_manifest = gate_inputs.representation_control_manifest
    representation_control_manifest_audit = (
        gate_inputs.representation_control_manifest_audit
    )
    representation_control_comparison = gate_inputs.representation_control_comparison
    representation_control_comparison_audit = (
        gate_inputs.representation_control_comparison_audit
    )
    representation_backend_plan = gate_inputs.representation_backend_plan
    representation_backend_plan_audit = gate_inputs.representation_backend_plan_audit
    representation_backend_sample = gate_inputs.representation_backend_sample
    representation_backend_sample_audit = (
        gate_inputs.representation_backend_sample_audit
    )
    broad_ec_disambiguation_audit = gate_inputs.broad_ec_disambiguation_audit
    active_site_gap_source_requests = gate_inputs.active_site_gap_source_requests
    sequence_neighborhood_plan = gate_inputs.sequence_neighborhood_plan
    sequence_neighborhood_sample = gate_inputs.sequence_neighborhood_sample
    sequence_neighborhood_sample_audit = gate_inputs.sequence_neighborhood_sample_audit
    sequence_alignment_verification = gate_inputs.sequence_alignment_verification
    sequence_alignment_verification_audit = (
        gate_inputs.sequence_alignment_verification_audit
    )
    sequence_reference_screen_audit = gate_inputs.sequence_reference_screen_audit
    sequence_search_export = gate_inputs.sequence_search_export
    sequence_search_export_audit = gate_inputs.sequence_search_export_audit
    sequence_backend_search = gate_inputs.sequence_backend_search
    external_import_readiness_audit = gate_inputs.external_import_readiness_audit
    active_site_sourcing_queue = gate_inputs.active_site_sourcing_queue
    active_site_sourcing_queue_audit = gate_inputs.active_site_sourcing_queue_audit
    active_site_sourcing_export = gate_inputs.active_site_sourcing_export
    active_site_sourcing_export_audit = gate_inputs.active_site_sourcing_export_audit
    active_site_sourcing_resolution = gate_inputs.active_site_sourcing_resolution
    active_site_sourcing_resolution_audit = (
        gate_inputs.active_site_sourcing_resolution_audit
    )
    transfer_blocker_matrix = gate_inputs.transfer_blocker_matrix
    transfer_blocker_matrix_audit = gate_inputs.transfer_blocker_matrix_audit
    pilot_candidate_priority = gate_inputs.pilot_candidate_priority
    pilot_review_decision_export = gate_inputs.pilot_review_decision_export
    pilot_evidence_packet = gate_inputs.pilot_evidence_packet
    pilot_evidence_dossiers = gate_inputs.pilot_evidence_dossiers
    pilot_active_site_evidence_decisions = (
        gate_inputs.pilot_active_site_evidence_decisions
    )
    pilot_representation_backend_sample = (
        gate_inputs.pilot_representation_backend_sample
    )
    binding_context_repair_plan = gate_inputs.binding_context_repair_plan
    binding_context_repair_plan_audit = gate_inputs.binding_context_repair_plan_audit
    binding_context_mapping_sample = gate_inputs.binding_context_mapping_sample
    binding_context_mapping_sample_audit = (
        gate_inputs.binding_context_mapping_sample_audit
    )
    sequence_holdout_audit = gate_inputs.sequence_holdout_audit
    artifact_path_lineage = gate_inputs.artifact_path_lineage
    candidate_lineage = _merge_external_transfer_lineage(
        _external_transfer_candidate_lineage(
            candidate_manifest,
            gate_inputs.candidate_lineage_artifacts(),
        ),
        artifact_path_lineage,
    )
    gates = {
        "external_transfer_candidate_lineage_consistent": bool(
            candidate_lineage.get("guardrail_clean")
        ),
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
    if representation_backend_sample is not None:
        sample_meta = representation_backend_sample.get("metadata", {})
        sample_rows = [
            row
            for row in representation_backend_sample.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_sample_count = (
            representation_backend_plan.get("metadata", {}).get("candidate_count")
            if representation_backend_plan is not None
            else len(sample_rows)
        )
        gates["representation_backend_sample_review_only"] = (
            sample_meta.get("ready_for_label_import") is False
            and sample_meta.get("countable_label_candidate_count") == 0
            and sample_meta.get("embedding_status") == "computed_review_only"
            and (
                sample_meta.get("embedding_backend")
                == "deterministic_sequence_kmer_control"
                or sample_meta.get("embedding_backend") in ESM2_BACKEND_MODEL_NAMES
            )
            and (
                sample_meta.get("embedding_backend")
                == "deterministic_sequence_kmer_control"
                or (
                    sample_meta.get("embedding_backend_available") is True
                    and int(sample_meta.get("embedding_failure_count", 0) or 0) == 0
                )
            )
            and int(sample_meta.get("candidate_count", 0) or 0) == len(sample_rows)
            and int(sample_meta.get("candidate_count", 0) or 0)
            == int(expected_sample_count or 0)
            and len(sample_rows) > 0
            and all(row.get("countable_label_candidate") is False for row in sample_rows)
            and all(row.get("ready_for_label_import") is False for row in sample_rows)
            and all(
                row.get("review_status") == "representation_backend_sample_review_only"
                for row in sample_rows
            )
            and all(row.get("backend_status") for row in sample_rows)
        )
    if representation_backend_sample_audit is not None:
        sample_audit_meta = representation_backend_sample_audit.get("metadata", {})
        gates["representation_backend_sample_audit_guardrail_clean"] = (
            sample_audit_meta.get("guardrail_clean") is True
            and sample_audit_meta.get("ready_for_label_import") is False
            and sample_audit_meta.get("countable_label_candidate_count") == 0
            and sample_audit_meta.get("embedding_status") == "computed_review_only"
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
    if sequence_reference_screen_audit is not None:
        reference_screen_meta = sequence_reference_screen_audit.get("metadata", {})
        reference_screen_rows = [
            row
            for row in sequence_reference_screen_audit.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_reference_screen_count = (
            sequence_neighborhood_sample.get("metadata", {}).get("candidate_count")
            if sequence_neighborhood_sample is not None
            else candidate_manifest.get("metadata", {}).get("candidate_count", 0)
        )
        expected_reference_sequence_count = (
            sequence_neighborhood_sample.get("metadata", {}).get(
                "reference_sequence_count"
            )
            if sequence_neighborhood_sample is not None
            else reference_screen_meta.get("screened_reference_sequence_count")
        )
        gates["sequence_reference_screen_audit_guardrail_clean"] = (
            reference_screen_meta.get("guardrail_clean") is True
            and reference_screen_meta.get("ready_for_label_import") is False
            and reference_screen_meta.get("countable_label_candidate_count") == 0
            and reference_screen_meta.get("complete_near_duplicate_search_required")
            is True
            and reference_screen_meta.get("current_reference_screen_complete") is True
            and reference_screen_meta.get("missing_reference_sequence_count") == 0
            and reference_screen_meta.get("incomplete_candidate_count") == 0
            and reference_screen_meta.get("blocker_removed")
            == "external_pilot_current_reference_near_duplicate_screen"
            and int(reference_screen_meta.get("candidate_count", 0) or 0)
            == len(reference_screen_rows)
            and int(reference_screen_meta.get("candidate_count", 0) or 0)
            == int(expected_reference_screen_count or 0)
            and int(
                reference_screen_meta.get("screened_reference_sequence_count", 0) or 0
            )
            == int(expected_reference_sequence_count or 0)
            and len(reference_screen_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in reference_screen_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in reference_screen_rows
            )
            and all(
                row.get("review_status")
                == "sequence_reference_screen_audit_review_only"
                for row in reference_screen_rows
            )
            and all(
                row.get("current_reference_screen_status")
                for row in reference_screen_rows
            )
        )
    if sequence_search_export is not None:
        search_export_meta = sequence_search_export.get("metadata", {})
        search_export_rows = [
            row
            for row in sequence_search_export.get("rows", []) or []
            if isinstance(row, dict)
        ]
        reference_screen_meta = (
            sequence_reference_screen_audit.get("metadata", {})
            if sequence_reference_screen_audit is not None
            else {}
        )
        reference_screen_rows = [
            row
            for row in (sequence_reference_screen_audit or {}).get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_reference_screen_complete_count = sum(
            1
            for row in reference_screen_rows
            if row.get("current_reference_screen_status")
            == "current_reference_top_hits_aligned_no_alert"
        )
        reference_screen_export_consistent = sequence_reference_screen_audit is None or (
            search_export_meta.get("source_sequence_reference_screen_audit_method")
            == reference_screen_meta.get("method")
            and search_export_meta.get("blocker_removed")
            == reference_screen_meta.get("blocker_removed")
            and int(
                search_export_meta.get(
                    "current_reference_screen_complete_candidate_count", 0
                )
                or 0
            )
            == expected_reference_screen_complete_count
            and all(row.get("current_reference_screen") for row in search_export_rows)
        )
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
            and reference_screen_export_consistent
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
    if sequence_backend_search is not None:
        backend_search_meta = sequence_backend_search.get("metadata", {})
        backend_search_rows = [
            row
            for row in sequence_backend_search.get("rows", []) or []
            if isinstance(row, dict)
        ]
        gates["sequence_backend_search_review_only"] = (
            backend_search_meta.get("method")
            == "external_source_backend_sequence_search"
            and backend_search_meta.get("backend_succeeded") is True
            and backend_search_meta.get("backend_name")
            in {"mmseqs2_easy_search", "diamond_blastp", "blastp"}
            and backend_search_meta.get("ready_for_label_import") is False
            and backend_search_meta.get("countable_label_candidate_count") == 0
            and backend_search_meta.get("import_ready_row_count") == 0
            and int(backend_search_meta.get("candidate_count", 0) or 0)
            == len(backend_search_rows)
            and int(backend_search_meta.get("candidate_count", 0) or 0)
            == int(candidate_manifest.get("metadata", {}).get("candidate_count", 0) or 0)
            and int(backend_search_meta.get("no_signal_row_count", 0) or 0) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in backend_search_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in backend_search_rows
            )
            and all(
                row.get("review_status")
                == "external_backend_sequence_search_review_only"
                for row in backend_search_rows
            )
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
    if active_site_sourcing_resolution is not None:
        resolution_meta = active_site_sourcing_resolution.get("metadata", {})
        resolution_rows = [
            row
            for row in active_site_sourcing_resolution.get("rows", []) or []
            if isinstance(row, dict)
        ]
        expected_resolution_count = (
            active_site_sourcing_export.get("metadata", {}).get("candidate_count")
            if active_site_sourcing_export is not None
            else len(resolution_rows)
        )
        gates["active_site_sourcing_resolution_review_only"] = (
            resolution_meta.get("ready_for_label_import") is False
            and resolution_meta.get("countable_label_candidate_count") == 0
            and int(resolution_meta.get("candidate_count", 0) or 0)
            == len(resolution_rows)
            and int(resolution_meta.get("candidate_count", 0) or 0)
            == int(expected_resolution_count or 0)
            and len(resolution_rows) > 0
            and all(
                row.get("countable_label_candidate") is False
                for row in resolution_rows
            )
            and all(
                row.get("ready_for_label_import") is False
                for row in resolution_rows
            )
            and all(
                row.get("review_status")
                == "active_site_sourcing_resolution_review_only"
                for row in resolution_rows
            )
            and all(row.get("active_site_source_status") for row in resolution_rows)
        )
    if active_site_sourcing_resolution_audit is not None:
        resolution_audit_meta = active_site_sourcing_resolution_audit.get(
            "metadata", {}
        )
        gates["active_site_sourcing_resolution_audit_guardrail_clean"] = (
            resolution_audit_meta.get("guardrail_clean") is True
            and resolution_audit_meta.get("ready_for_label_import") is False
            and resolution_audit_meta.get("countable_label_candidate_count") == 0
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
        expected_matrix_resolution_count = int(
            (
                active_site_sourcing_resolution.get("metadata", {}).get(
                    "candidate_count"
                )
                if active_site_sourcing_resolution is not None
                else matrix_meta.get(
                    "active_site_sourcing_resolution_candidate_count", 0
                )
            )
            or 0
        )
        expected_matrix_sample_count = int(
            (
                representation_backend_sample.get("metadata", {}).get(
                    "candidate_count"
                )
                if representation_backend_sample is not None
                else matrix_meta.get("representation_backend_sample_candidate_count", 0)
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
        if active_site_sourcing_resolution is not None:
            matrix_resolution_rows = [
                row
                for row in matrix_rows
                if row.get("active_site_sourcing", {}).get("resolution_status")
            ]
            gates[
                "external_transfer_blocker_matrix_active_site_resolution_integrated"
            ] = (
                int(
                    matrix_meta.get(
                        "active_site_sourcing_resolution_candidate_count", 0
                    )
                    or 0
                )
                == expected_matrix_resolution_count
                and len(matrix_resolution_rows) == expected_matrix_resolution_count
            )
        if representation_backend_sample is not None:
            matrix_sample_rows = [
                row
                for row in matrix_rows
                if row.get("representation_backend", {}).get("sample_backend_status")
            ]
            gates[
                "external_transfer_blocker_matrix_representation_sample_integrated"
            ] = (
                int(
                    matrix_meta.get("representation_backend_sample_candidate_count", 0)
                    or 0
                )
                == expected_matrix_sample_count
                and len(matrix_sample_rows) == expected_matrix_sample_count
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
    gates.update(
        _external_pilot_review_only_gate_checks(
            pilot_candidate_priority=pilot_candidate_priority,
            pilot_review_decision_export=pilot_review_decision_export,
            pilot_evidence_packet=pilot_evidence_packet,
            pilot_evidence_dossiers=pilot_evidence_dossiers,
            pilot_active_site_evidence_decisions=(
                pilot_active_site_evidence_decisions
            ),
            pilot_representation_backend_sample=pilot_representation_backend_sample,
        )
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
            "gate_input_contract": EXTERNAL_TRANSFER_GATE_INPUT_CONTRACT,
            "artifact_lineage": candidate_lineage,
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
            "representation_backend_sample_candidate_count": (
                representation_backend_sample.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if representation_backend_sample is not None
                else 0
            ),
            "representation_backend_sample_reference_pair_count": (
                representation_backend_sample.get("metadata", {}).get(
                    "reference_pair_count", 0
                )
                if representation_backend_sample is not None
                else 0
            ),
            "representation_backend_sample_near_duplicate_alert_count": (
                representation_backend_sample.get("metadata", {}).get(
                    "representation_near_duplicate_alert_count", 0
                )
                if representation_backend_sample is not None
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
            "sequence_reference_screen_candidate_count": (
                sequence_reference_screen_audit.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if sequence_reference_screen_audit is not None
                else 0
            ),
            "sequence_reference_screened_reference_sequence_count": (
                sequence_reference_screen_audit.get("metadata", {}).get(
                    "screened_reference_sequence_count", 0
                )
                if sequence_reference_screen_audit is not None
                else 0
            ),
            "sequence_reference_screen_incomplete_candidate_count": (
                sequence_reference_screen_audit.get("metadata", {}).get(
                    "incomplete_candidate_count", 0
                )
                if sequence_reference_screen_audit is not None
                else 0
            ),
            "sequence_reference_screen_current_reference_complete": (
                sequence_reference_screen_audit.get("metadata", {}).get(
                    "current_reference_screen_complete", False
                )
                if sequence_reference_screen_audit is not None
                else False
            ),
            "sequence_reference_screen_blocker_removed": (
                sequence_reference_screen_audit.get("metadata", {}).get(
                    "blocker_removed"
                )
                if sequence_reference_screen_audit is not None
                else None
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
            "sequence_backend_search_candidate_count": (
                sequence_backend_search.get("metadata", {}).get("candidate_count", 0)
                if sequence_backend_search is not None
                else 0
            ),
            "sequence_backend_search_no_signal_count": (
                sequence_backend_search.get("metadata", {}).get(
                    "no_signal_row_count", 0
                )
                if sequence_backend_search is not None
                else 0
            ),
            "sequence_backend_search_exact_reference_count": (
                sequence_backend_search.get("metadata", {}).get(
                    "exact_reference_row_count", 0
                )
                if sequence_backend_search is not None
                else 0
            ),
            "sequence_backend_search_backend_name": (
                sequence_backend_search.get("metadata", {}).get("backend_name")
                if sequence_backend_search is not None
                else None
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
            "active_site_sourcing_resolution_candidate_count": (
                active_site_sourcing_resolution.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if active_site_sourcing_resolution is not None
                else 0
            ),
            "active_site_sourcing_resolution_explicit_source_count": (
                active_site_sourcing_resolution.get("metadata", {}).get(
                    "explicit_active_site_source_count", 0
                )
                if active_site_sourcing_resolution is not None
                else 0
            ),
            "active_site_sourcing_resolution_fetch_failure_count": (
                active_site_sourcing_resolution_audit.get("metadata", {}).get(
                    "fetch_failure_count", 0
                )
                if active_site_sourcing_resolution_audit is not None
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
            "external_transfer_blocker_matrix_active_site_resolution_count": (
                transfer_blocker_matrix.get("metadata", {}).get(
                    "active_site_sourcing_resolution_candidate_count", 0
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
            "external_transfer_blocker_matrix_representation_sample_count": (
                transfer_blocker_matrix.get("metadata", {}).get(
                    "representation_backend_sample_candidate_count", 0
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
            "external_pilot_selected_candidate_count": (
                pilot_candidate_priority.get("metadata", {}).get(
                    "selected_candidate_count", 0
                )
                if pilot_candidate_priority is not None
                else 0
            ),
            "external_pilot_review_completed_decision_count": (
                pilot_review_decision_export.get("metadata", {}).get(
                    "completed_decision_count", 0
                )
                if pilot_review_decision_export is not None
                else 0
            ),
            "external_pilot_evidence_packet_source_target_count": (
                pilot_evidence_packet.get("metadata", {}).get("source_target_count", 0)
                if pilot_evidence_packet is not None
                else 0
            ),
            "external_pilot_dossier_remaining_blocker_count": (
                pilot_evidence_dossiers.get("metadata", {}).get(
                    "candidate_with_remaining_blocker_count", 0
                )
                if pilot_evidence_dossiers is not None
                else 0
            ),
            "external_pilot_active_site_decision_candidate_count": (
                pilot_active_site_evidence_decisions.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if pilot_active_site_evidence_decisions is not None
                else 0
            ),
            "external_pilot_active_site_decision_explicit_source_count": (
                pilot_active_site_evidence_decisions.get("metadata", {}).get(
                    "explicit_active_site_source_present_count", 0
                )
                if pilot_active_site_evidence_decisions is not None
                else 0
            ),
            "external_pilot_active_site_decision_no_explicit_source_count": (
                pilot_active_site_evidence_decisions.get("metadata", {}).get(
                    "no_explicit_active_site_source_count", 0
                )
                if pilot_active_site_evidence_decisions is not None
                else 0
            ),
            "external_pilot_representation_sample_candidate_count": (
                pilot_representation_backend_sample.get("metadata", {}).get(
                    "candidate_count", 0
                )
                if pilot_representation_backend_sample is not None
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


def _external_pilot_representation_backend_status(sequence_task: str) -> str:
    if sequence_task == "keep_sequence_holdout_control":
        return "blocked_by_sequence_holdout_control"
    if sequence_task != "run_complete_uniref_or_all_vs_all_near_duplicate_search":
        return "blocked_until_sequence_search_complete"
    return "ready_for_backend_selection_not_embedding"


def _external_pilot_scope_signal(row: dict[str, Any]) -> str:
    scope_signal = str(row.get("scope_signal") or "").strip()
    if scope_signal:
        return scope_signal
    lane_id = str(row.get("lane_id") or "")
    if lane_id.startswith("external_source:"):
        return lane_id.split(":", 1)[1]
    return lane_id or "unknown"


def _external_pilot_representation_comparison_status(row: dict[str, Any]) -> str:
    blockers = set(str(blocker) for blocker in row.get("blockers", []) or [])
    if (
        "representation_control_proxy_boundary_case_requires_glycan_hydrolase_split"
        in blockers
    ):
        return "proxy_boundary_case_requires_glycan_hydrolase_split"
    if "representation_control_proxy_flags_metal_hydrolase_collapse" in blockers:
        return "proxy_flags_metal_hydrolase_collapse"
    if "representation_control_proxy_flags_scope_top1_mismatch" in blockers:
        return "proxy_flags_scope_top1_mismatch"
    if "representation_control_not_compared" in blockers:
        return "pilot_sequence_embedding_without_feature_proxy_comparison"
    return "pilot_sequence_embedding_control"


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


def _external_representation_backend_sample_status(
    *,
    candidate_sequence: str,
    reference_scores: list[dict[str, Any]],
    backend_readiness_status: str,
    embedding_backend: str,
    similarity_alert_threshold: float,
) -> str:
    if backend_readiness_status != "ready_for_backend_selection_not_embedding":
        return "blocked_by_backend_plan_readiness"
    if not candidate_sequence:
        return "candidate_sequence_missing"
    if not reference_scores:
        return "reference_sequences_missing"
    best = reference_scores[0]
    if (
        float(best.get("embedding_cosine", 0.0) or 0.0)
        >= similarity_alert_threshold
        and float(best.get("length_coverage", 0.0) or 0.0) >= 0.9
    ):
        return "representation_near_duplicate_holdout"
    if embedding_backend != "deterministic_sequence_kmer_control":
        return "learned_representation_sample_complete"
    return "sequence_kmer_embedding_control_complete"


def _external_representation_backend_sample_blockers(
    *, status: str, embedding_backend: str
) -> list[str]:
    blockers = [
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if embedding_backend == "deterministic_sequence_kmer_control":
        blockers.insert(0, "learned_or_structure_language_embedding_not_run")
    if status == "representation_near_duplicate_holdout":
        blockers.insert(0, "representation_near_duplicate_control_holdout")
    elif status == "candidate_sequence_missing":
        blockers.insert(0, "candidate_sequence_missing")
    elif status == "reference_sequences_missing":
        blockers.insert(0, "reference_sequences_missing")
    elif status == "blocked_by_backend_plan_readiness":
        blockers.insert(0, "representation_backend_plan_not_ready")
    elif status == "embedding_backend_unavailable":
        blockers.insert(0, "representation_embedding_backend_unavailable")
    return blockers


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


def _external_entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    match = re.match(r"^([^:]+):(\d+)$", str(entry_id))
    if match:
        return (match.group(1), int(match.group(2)), "")
    return (str(entry_id), -1, str(entry_id))


def _external_sequence_record_id(
    prefix: str, accession: str, resolved_accession: str | None = None
) -> str:
    values = [prefix, accession]
    if resolved_accession and resolved_accession != accession:
        values.append(resolved_accession)
    return "__".join(
        re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_") for value in values
    )


def _parse_sequence_fasta(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    header: str | None = None
    sequence_parts: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append(
                        _sequence_fasta_record_from_parts(header, sequence_parts)
                    )
                header = line[1:].strip()
                sequence_parts = []
            else:
                sequence_parts.append(line)
    if header is not None:
        records.append(_sequence_fasta_record_from_parts(header, sequence_parts))
    return records


def _sequence_fasta_record_from_parts(
    header: str, sequence_parts: list[str]
) -> dict[str, Any]:
    record_id = header.split(None, 1)[0]
    return {
        "accession": _sequence_fasta_accession(record_id),
        "header": header,
        "record_id": record_id,
        "sequence": _clean_sequence("".join(sequence_parts)),
    }


def _sequence_fasta_accession(record_id: str) -> str:
    fields = record_id.split("|")
    if len(fields) >= 2 and fields[1]:
        return _normalize_accession(fields[1])
    return _normalize_accession(record_id)


def _write_sequence_fasta(path: Path, records: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in sorted(records, key=lambda item: str(item.get("record_id") or "")):
            record_id = str(record.get("record_id") or "")
            sequence = _clean_sequence(record.get("sequence"))
            if not record_id or not sequence:
                continue
            handle.write(f">{record_id}\n")
            for index in range(0, len(sequence), 60):
                handle.write(sequence[index : index + 60] + "\n")


def _run_external_sequence_search_backend(
    *,
    external_fasta: Path,
    reference_fasta: Path,
    result_tsv: Path,
    backend: str,
    mmseqs_binary: str,
    diamond_binary: str,
    blastp_binary: str,
    makeblastdb_binary: str,
    coverage_threshold: float,
) -> dict[str, Any]:
    requested = backend.strip().lower()
    if requested == "auto":
        backend_order = ("mmseqs", "diamond", "blastp")
    elif requested in {"mmseqs", "diamond", "blastp"}:
        backend_order = (requested,)
    else:
        return {
            "alignment_rows": [],
            "backend_available": False,
            "backend_commands": [],
            "backend_name": None,
            "backend_succeeded": False,
            "backend_version": None,
            "limitations": [f"unsupported sequence search backend: {backend}"],
        }

    failures: list[str] = []
    for backend_name in backend_order:
        try:
            if backend_name == "mmseqs":
                result = _run_mmseqs_external_sequence_search(
                    external_fasta=external_fasta,
                    reference_fasta=reference_fasta,
                    result_tsv=result_tsv,
                    binary=mmseqs_binary,
                    coverage_threshold=coverage_threshold,
                )
            elif backend_name == "diamond":
                result = _run_diamond_external_sequence_search(
                    external_fasta=external_fasta,
                    reference_fasta=reference_fasta,
                    result_tsv=result_tsv,
                    binary=diamond_binary,
                )
            else:
                result = _run_blastp_external_sequence_search(
                    external_fasta=external_fasta,
                    reference_fasta=reference_fasta,
                    result_tsv=result_tsv,
                    blastp_binary=blastp_binary,
                    makeblastdb_binary=makeblastdb_binary,
                )
            if result.get("backend_succeeded"):
                if failures:
                    result["limitations"] = [
                        *failures,
                        *result.get("limitations", []),
                    ]
                return result
            failures.extend(result.get("limitations", []))
        except (OSError, RuntimeError, ValueError) as exc:
            failures.append(f"{backend_name} sequence search failed: {exc}")
    return {
        "alignment_rows": [],
        "backend_available": False,
        "backend_commands": [],
        "backend_name": None,
        "backend_succeeded": False,
        "backend_version": None,
        "limitations": failures or ["no supported sequence search backend available"],
    }


def _run_mmseqs_external_sequence_search(
    *,
    external_fasta: Path,
    reference_fasta: Path,
    result_tsv: Path,
    binary: str,
    coverage_threshold: float,
) -> dict[str, Any]:
    binary_path = shutil.which(binary)
    if not binary_path:
        return {
            "alignment_rows": [],
            "backend_available": False,
            "backend_commands": [],
            "backend_name": "mmseqs2_easy_search",
            "backend_succeeded": False,
            "backend_version": None,
            "limitations": [f"MMseqs2 binary not found: {binary}"],
        }
    workdir = _external_sequence_search_workdir(
        "mmseqs", external_fasta, reference_fasta
    )
    tmp_dir = workdir / "tmp"
    result_tsv.parent.mkdir(parents=True, exist_ok=True)
    command = [
        binary_path,
        "easy-search",
        str(external_fasta),
        str(reference_fasta),
        str(result_tsv),
        str(tmp_dir),
        "--format-output",
        "query,target,pident,alnlen,evalue,bits",
        "--min-seq-id",
        "0.0",
        "-c",
        _external_backend_float(coverage_threshold),
        "--cov-mode",
        "0",
        "--max-seqs",
        "10000",
        "--threads",
        "1",
    ]
    _run_external_backend_command(command, cwd=workdir)
    return {
        "alignment_rows": _parse_external_sequence_search_tsv(result_tsv),
        "backend_available": True,
        "backend_commands": [_external_command_string(command)],
        "backend_name": "mmseqs2_easy_search",
        "backend_succeeded": True,
        "backend_version": _external_backend_version(binary_path),
        "limitations": [
            (
                "MMseqs2 easy-search reports heuristic local alignments at the "
                "configured coverage threshold; it is not an exhaustive dynamic "
                "programming matrix for every low-identity pair"
            )
        ],
    }


def _run_diamond_external_sequence_search(
    *,
    external_fasta: Path,
    reference_fasta: Path,
    result_tsv: Path,
    binary: str,
) -> dict[str, Any]:
    binary_path = shutil.which(binary)
    if not binary_path:
        return {
            "alignment_rows": [],
            "backend_available": False,
            "backend_commands": [],
            "backend_name": "diamond_blastp",
            "backend_succeeded": False,
            "backend_version": None,
            "limitations": [f"DIAMOND binary not found: {binary}"],
        }
    workdir = _external_sequence_search_workdir(
        "diamond", external_fasta, reference_fasta
    )
    db_path = workdir / "reference.dmnd"
    result_tsv.parent.mkdir(parents=True, exist_ok=True)
    makedb_cmd = [binary_path, "makedb", "--in", str(reference_fasta), "-d", str(db_path)]
    blastp_cmd = [
        binary_path,
        "blastp",
        "-q",
        str(external_fasta),
        "-d",
        str(db_path),
        "-o",
        str(result_tsv),
        "-f",
        "6",
        "qseqid",
        "sseqid",
        "pident",
        "length",
        "evalue",
        "bitscore",
        "--threads",
        "1",
        "--max-target-seqs",
        "10000",
    ]
    _run_external_backend_command(makedb_cmd, cwd=workdir)
    _run_external_backend_command(blastp_cmd, cwd=workdir)
    return {
        "alignment_rows": _parse_external_sequence_search_tsv(result_tsv),
        "backend_available": True,
        "backend_commands": [
            _external_command_string(makedb_cmd),
            _external_command_string(blastp_cmd),
        ],
        "backend_name": "diamond_blastp",
        "backend_succeeded": True,
        "backend_version": _external_backend_version(binary_path),
        "limitations": [
            "DIAMOND is a fallback local-alignment backend; no UniRef database is searched"
        ],
    }


def _run_blastp_external_sequence_search(
    *,
    external_fasta: Path,
    reference_fasta: Path,
    result_tsv: Path,
    blastp_binary: str,
    makeblastdb_binary: str,
) -> dict[str, Any]:
    blastp_path = shutil.which(blastp_binary)
    makeblastdb_path = shutil.which(makeblastdb_binary)
    missing = [
        name
        for name, path in (
            (blastp_binary, blastp_path),
            (makeblastdb_binary, makeblastdb_path),
        )
        if not path
    ]
    if missing:
        return {
            "alignment_rows": [],
            "backend_available": False,
            "backend_commands": [],
            "backend_name": "blastp",
            "backend_succeeded": False,
            "backend_version": None,
            "limitations": [f"BLAST+ binary not found: {', '.join(missing)}"],
        }
    workdir = _external_sequence_search_workdir(
        "blastp", external_fasta, reference_fasta
    )
    db_path = workdir / "reference"
    result_tsv.parent.mkdir(parents=True, exist_ok=True)
    makedb_cmd = [
        str(makeblastdb_path),
        "-in",
        str(reference_fasta),
        "-dbtype",
        "prot",
        "-out",
        str(db_path),
    ]
    blastp_cmd = [
        str(blastp_path),
        "-query",
        str(external_fasta),
        "-db",
        str(db_path),
        "-outfmt",
        "6 qseqid sseqid pident length evalue bitscore",
        "-out",
        str(result_tsv),
        "-num_threads",
        "1",
        "-max_target_seqs",
        "10000",
    ]
    _run_external_backend_command(makedb_cmd, cwd=workdir)
    _run_external_backend_command(blastp_cmd, cwd=workdir)
    return {
        "alignment_rows": _parse_external_sequence_search_tsv(result_tsv),
        "backend_available": True,
        "backend_commands": [
            _external_command_string(makedb_cmd),
            _external_command_string(blastp_cmd),
        ],
        "backend_name": "blastp",
        "backend_succeeded": True,
        "backend_version": _external_backend_version(str(blastp_path)),
        "limitations": [
            "BLASTP is a fallback local-alignment backend; no UniRef database is searched"
        ],
    }


def _external_sequence_search_workdir(
    backend_name: str, external_fasta: Path, reference_fasta: Path
) -> Path:
    digest = hashlib.sha256()
    for path in (external_fasta, reference_fasta):
        digest.update(path.read_bytes())
    workdir = Path("/private/tmp") / (
        f"catalytic-earth-external-sequence-{backend_name}-"
        f"{digest.hexdigest()[:16]}"
    )
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir


def _run_external_backend_command(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit code {completed.returncode}"
        raise RuntimeError(f"{_external_command_string(command)} failed: {detail}")


def _parse_external_sequence_search_tsv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            fields = raw_line.rstrip("\n").split("\t")
            if len(fields) < 6:
                continue
            try:
                pident = float(fields[2])
                alnlen = int(float(fields[3]))
                evalue = float(fields[4])
                bits = float(fields[5])
            except ValueError:
                continue
            rows.append(
                {
                    "query_id": fields[0],
                    "target_id": fields[1],
                    "pident": pident,
                    "alnlen": alnlen,
                    "evalue": evalue,
                    "bits": bits,
                }
            )
    return rows


def _external_sequence_search_alignments(
    alignment_rows: list[dict[str, Any]],
    *,
    external_sequence_records: dict[str, dict[str, Any]],
    reference_sequence_records: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    alignments: list[dict[str, Any]] = []
    for row in alignment_rows:
        query_id = str(row.get("query_id") or "")
        target_id = str(row.get("target_id") or "")
        external_record = external_sequence_records.get(query_id)
        reference_record = reference_sequence_records.get(target_id)
        if not external_record or not reference_record:
            continue
        query_len = len(_clean_sequence(external_record.get("sequence")))
        target_len = len(_clean_sequence(reference_record.get("sequence")))
        alnlen = int(row.get("alnlen", 0) or 0)
        query_coverage = (alnlen / query_len) if query_len else 0.0
        target_coverage = (alnlen / target_len) if target_len else 0.0
        identity = float(row.get("pident", 0.0) or 0.0) / 100.0
        alignments.append(
            {
                "accession": external_record.get("accession"),
                "alignment_length": alnlen,
                "bits": round(float(row.get("bits", 0.0) or 0.0), 4),
                "evalue": row.get("evalue"),
                "external_length": query_len,
                "identity": round(identity, 4),
                "matched_m_csa_entry_ids": reference_record.get(
                    "matched_m_csa_entry_ids", []
                ),
                "min_coverage": round(min(query_coverage, target_coverage), 4),
                "query_coverage": round(query_coverage, 4),
                "reference_accession": reference_record.get(
                    "resolved_reference_accession"
                ),
                "reference_accession_resolution": reference_record.get(
                    "reference_accession_resolution"
                ),
                "reference_length": target_len,
                "requested_reference_accession": reference_record.get(
                    "requested_reference_accession"
                ),
                "target_coverage": round(target_coverage, 4),
            }
        )
    return alignments


def _external_backend_version(binary: str) -> str | None:
    for flag in ("version", "-version"):
        try:
            completed = subprocess.run(
                [binary, flag],
                text=True,
                capture_output=True,
                check=False,
            )
        except OSError:
            return None
        if completed.returncode == 0:
            return (completed.stdout.strip() or completed.stderr.strip()) or None
    return None


def _external_command_string(command: list[str]) -> str:
    return shlex.join(command)


def _external_backend_float(value: float) -> str:
    return f"{float(value):.4g}"


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
    inactive_accession_replacements: dict[str, list[str]] = {}
    by_accession = {
        _normalize_accession(record.get("accession")): record
        for record in records
        if _normalize_accession(record.get("accession"))
    }
    missing_accessions = sorted(
        accession
        for accession in cleaned
        if accession not in by_accession
        or not _clean_sequence(by_accession[accession].get("sequence"))
    )
    replacement_accessions: set[str] = set()
    inactive_fetch_failures: list[dict[str, str]] = []
    for accession in missing_accessions:
        try:
            inactive_payload = _fetch_uniprot_entry_payload(accession)
        except Exception as exc:  # pragma: no cover - live network failure path
            inactive_fetch_failures.append(
                {
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            continue
        replacements = _inactive_uniprot_replacements(inactive_payload)
        if replacements:
            inactive_accession_replacements[accession] = replacements
            replacement_accessions.update(replacements)
    replacement_accessions = replacement_accessions - set(by_accession)
    for batch in _batch_items(sorted(replacement_accessions), 20):
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
                "request_type": "inactive_accession_replacement",
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
            "inactive_accession_replacements": dict(
                sorted(inactive_accession_replacements.items())
            ),
            "inactive_accession_replacement_count": len(
                inactive_accession_replacements
            ),
            "inactive_accession_fetch_failures": inactive_fetch_failures,
        },
        "records": [by_accession[accession] for accession in sorted(by_accession)],
    }


def _fetch_uniprot_entry_payload(accession: str) -> dict[str, Any]:
    request = Request(
        f"{UNIPROT_ENTRY_URL}/{accession}.json",
        headers={"User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    return payload if isinstance(payload, dict) else {}


def _inactive_uniprot_replacements(payload: dict[str, Any]) -> list[str]:
    if str(payload.get("entryType") or "").lower() != "inactive":
        return []
    inactive_reason = payload.get("inactiveReason")
    if not isinstance(inactive_reason, dict):
        return []
    return sorted(
        {
            _normalize_accession(accession)
            for accession in inactive_reason.get("mergeDemergeTo", []) or []
            if _normalize_accession(accession)
        }
    )


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


def _sequence_kmer_embedding(
    sequence: str,
    *,
    kmer_size: int = 3,
) -> dict[str, float]:
    cleaned = _clean_sequence(sequence)
    if not cleaned:
        return {}
    counts: Counter[str] = Counter()
    for amino_acid in cleaned:
        counts[f"aa:{amino_acid}"] += 1
    if len(cleaned) < kmer_size:
        counts[f"kmer:{cleaned}"] += 1
    else:
        for index in range(len(cleaned) - kmer_size + 1):
            counts[f"kmer:{cleaned[index:index + kmer_size]}"] += 1
    total = sum(counts.values()) or 1
    return {token: count / total for token, count in counts.items()}


def _sparse_cosine_similarity(
    left: dict[str, float],
    right: dict[str, float],
) -> float:
    if not left or not right:
        return 0.0
    shared = set(left) & set(right)
    dot = sum(left[token] * right[token] for token in shared)
    left_norm = sum(value * value for value in left.values()) ** 0.5
    right_norm = sum(value * value for value in right.values()) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def _embedding_cosine_similarity(left: Any, right: Any) -> float:
    if not left or not right:
        return 0.0
    if isinstance(left, dict) and isinstance(right, dict):
        return _sparse_cosine_similarity(left, right)
    if isinstance(left, list) and isinstance(right, list):
        return _dense_cosine_similarity(left, right)
    return 0.0


def _dense_cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(float(a) * float(b) for a, b in zip(left, right))
    left_norm = sum(float(value) * float(value) for value in left) ** 0.5
    right_norm = sum(float(value) * float(value) for value in right) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def _compute_sequence_embedding_payload(
    *,
    records_by_accession: dict[str, dict[str, Any]],
    accessions: list[str],
    embedding_backend: str,
    model_name: str,
    local_files_only: bool = False,
    fallback_to_largest_local_esm2: bool = True,
    allow_larger_model_smoke: bool = False,
    larger_model_smoke_accession_limit: int = 2,
) -> dict[str, Any]:
    started = time.perf_counter()
    backend = _normalized_embedding_backend(embedding_backend)
    if backend == "deterministic_sequence_kmer_control":
        embeddings = {
            accession: _sequence_kmer_embedding(
                _clean_sequence(records_by_accession.get(accession, {}).get("sequence"))
            )
            for accession in accessions
            if _clean_sequence(records_by_accession.get(accession, {}).get("sequence"))
        }
        return {
            "metadata": {
                "embedding_backend": backend,
                "embedding_backend_available": True,
                "embedding_vector_dimension": None,
                "model_name": None,
                "requested_model_name": model_name,
                "local_files_only": local_files_only,
                "embedding_failure_count": 0,
                "embedding_elapsed_seconds": round(time.perf_counter() - started, 4),
                "model_load_elapsed_seconds": 0.0,
                "model_load_status": "not_applicable",
                "backend_feasibility_status": "computed",
                "expected_embedding_vector_dimension": None,
                "embedding_backend_model_family": "deterministic_sequence_kmer",
                "embedding_backend_parameter_count": None,
                "requested_embedding_backend": backend,
                "requested_backend_feasibility_status": "computed",
                "requested_backend_local_cache_status": "not_applicable",
                "requested_backend_smoke_status": "not_applicable",
                "requested_expected_embedding_vector_dimension": None,
                "requested_embedding_failure_count": 0,
                "fallback_used": False,
                "fallback_selected_backend": None,
                "fallback_reason": None,
                "fallback_attempts": [],
            },
            "embeddings_by_accession": embeddings,
            "warnings_by_accession": {},
            "embedding_failures": [],
            "warnings": [
                (
                    "the deterministic k-mer backend is a computed baseline "
                    "control, not a learned representation model"
                )
            ],
        }
    if backend not in ESM2_BACKEND_MODEL_NAMES:
        return {
            "metadata": {
                "embedding_backend": backend,
                "embedding_backend_available": False,
                "embedding_vector_dimension": None,
                "model_name": model_name,
                "requested_model_name": model_name,
                "local_files_only": local_files_only,
                "embedding_failure_count": len(accessions),
                "embedding_elapsed_seconds": round(time.perf_counter() - started, 4),
                "model_load_elapsed_seconds": 0.0,
                "model_load_status": "not_attempted",
                "backend_feasibility_status": "unsupported_backend",
                "expected_embedding_vector_dimension": None,
                "embedding_backend_model_family": None,
                "embedding_backend_parameter_count": None,
                "requested_embedding_backend": backend,
                "requested_backend_feasibility_status": "unsupported_backend",
                "requested_backend_local_cache_status": "not_applicable",
                "requested_backend_smoke_status": "not_applicable",
                "requested_expected_embedding_vector_dimension": None,
                "requested_embedding_failure_count": len(accessions),
                "fallback_used": False,
                "fallback_selected_backend": None,
                "fallback_reason": None,
                "fallback_attempts": [],
            },
            "embeddings_by_accession": {},
            "warnings_by_accession": {},
            "embedding_failures": [
                {
                    "accession": accession,
                    "error_type": "UnsupportedBackend",
                    "error": f"unsupported embedding backend: {embedding_backend}",
                }
                for accession in accessions
            ],
            "warnings": [f"unsupported embedding backend: {embedding_backend}"],
        }
    resolved_model_name = _resolved_esm2_model_name(
        backend=backend, requested_model_name=model_name
    )
    if (
        local_files_only
        and fallback_to_largest_local_esm2
        and backend != DEFAULT_ESM2_BACKEND
    ):
        return _compute_esm2_embeddings_with_local_fallback(
            records_by_accession=records_by_accession,
            accessions=accessions,
            requested_backend=backend,
            requested_model_name=resolved_model_name,
            allow_larger_model_smoke=allow_larger_model_smoke,
            larger_model_smoke_accession_limit=larger_model_smoke_accession_limit,
            started=started,
        )
    if backend == DEFAULT_ESM2_BACKEND:
        return _compute_esm2_t6_embeddings(
            records_by_accession=records_by_accession,
            accessions=accessions,
            model_name=resolved_model_name,
            local_files_only=local_files_only,
        )
    return _compute_esm2_embeddings(
        records_by_accession=records_by_accession,
        accessions=accessions,
        backend=backend,
        model_name=resolved_model_name,
        local_files_only=local_files_only,
    )


def _resolved_esm2_model_name(*, backend: str, requested_model_name: str) -> str:
    requested = str(requested_model_name or "").strip()
    if not requested:
        return ESM2_BACKEND_MODEL_NAMES[backend]
    default_model = ESM2_BACKEND_MODEL_NAMES[DEFAULT_ESM2_BACKEND]
    if requested == default_model and backend != DEFAULT_ESM2_BACKEND:
        return ESM2_BACKEND_MODEL_NAMES[backend]
    return requested


def _esm2_backend_metadata(backend: str) -> dict[str, Any]:
    return {
        "attempted_embedding_backend": backend,
        "expected_embedding_vector_dimension": ESM2_BACKEND_EXPECTED_DIMENSIONS.get(
            backend
        ),
        "embedding_backend_model_family": "ESM-2",
        "embedding_backend_parameter_count": ESM2_BACKEND_SCALE_LABELS.get(backend),
        "supported_embedding_backends": list(ESM2_BACKEND_MODEL_NAMES),
        "largest_supported_embedding_backend": "esm2_t33_650m_ur50d",
    }


def _normalized_embedding_backend(value: str) -> str:
    normalized = str(value or "").strip()
    normalized_key = normalized.lower()
    aliases = {
        "esm2": DEFAULT_ESM2_BACKEND,
        "esm-2": DEFAULT_ESM2_BACKEND,
        "esm2_8m": "esm2_t6_8m_ur50d",
        "esm2-8m": "esm2_t6_8m_ur50d",
        "esm2_t6_8m_ur50d": "esm2_t6_8m_ur50d",
        "facebook/esm2_t6_8m_ur50d": "esm2_t6_8m_ur50d",
        "esm2_35m": "esm2_t12_35m_ur50d",
        "esm2-35m": "esm2_t12_35m_ur50d",
        "esm2_t12_35m_ur50d": "esm2_t12_35m_ur50d",
        "facebook/esm2_t12_35m_ur50d": "esm2_t12_35m_ur50d",
        "esm2_150m": "esm2_t30_150m_ur50d",
        "esm2-150m": "esm2_t30_150m_ur50d",
        "esm2_t30_150m_ur50d": "esm2_t30_150m_ur50d",
        "facebook/esm2_t30_150m_ur50d": "esm2_t30_150m_ur50d",
        "esm2_650m": "esm2_t33_650m_ur50d",
        "esm2-650m": "esm2_t33_650m_ur50d",
        "esm2_t33_650m_ur50d": "esm2_t33_650m_ur50d",
        "facebook/esm2_t33_650m_ur50d": "esm2_t33_650m_ur50d",
    }
    return aliases.get(
        normalized_key, normalized or "deterministic_sequence_kmer_control"
    )


def _compute_esm2_embeddings_with_local_fallback(
    *,
    records_by_accession: dict[str, dict[str, Any]],
    accessions: list[str],
    requested_backend: str,
    requested_model_name: str,
    allow_larger_model_smoke: bool,
    larger_model_smoke_accession_limit: int,
    started: float,
) -> dict[str, Any]:
    requested_cache = _esm2_model_local_cache_status(requested_model_name)
    requested_smoke_status = "not_attempted_weights_not_cached"
    requested_backend_feasibility_status = "model_unavailable_locally"
    requested_model_load_status = "not_attempted_cache_missing"
    requested_model_load_failure_type = "ModelWeightsNotCached"
    requested_model_load_failure = (
        "requested ESM-2 weights are not present in the local Hugging Face cache"
    )
    requested_failures = _esm2_backend_failures(
        accessions=accessions,
        error_type=requested_model_load_failure_type,
        error=requested_model_load_failure,
    )
    fallback_reason = "requested_backend_uncached_local_files_only"

    if requested_cache["weights_cached"]:
        if allow_larger_model_smoke:
            smoke_limit = max(1, int(larger_model_smoke_accession_limit or 1))
            smoke_accessions = accessions[:smoke_limit]
            smoke_payload = _compute_esm2_embeddings(
                records_by_accession=records_by_accession,
                accessions=smoke_accessions,
                backend=requested_backend,
                model_name=requested_model_name,
                local_files_only=True,
            )
            requested_smoke_status = (
                "smoke_sample_computed"
                if smoke_payload["metadata"].get("embedding_backend_available")
                else "smoke_sample_failed"
            )
            requested_backend_feasibility_status = smoke_payload["metadata"].get(
                "backend_feasibility_status", "smoke_sample_failed"
            )
            requested_model_load_status = smoke_payload["metadata"].get(
                "model_load_status"
            )
            requested_model_load_failure_type = smoke_payload["metadata"].get(
                "model_load_failure_type"
            )
            requested_model_load_failure = smoke_payload["metadata"].get(
                "model_load_failure"
            )
            requested_failures = smoke_payload.get("embedding_failures", [])
            if smoke_payload["metadata"].get("embedding_backend_available"):
                return _attach_esm2_request_context(
                    payload=smoke_payload,
                    requested_backend=requested_backend,
                    requested_model_name=requested_model_name,
                    requested_cache=requested_cache,
                    requested_backend_feasibility_status="smoke_sample_computed",
                    requested_smoke_status=requested_smoke_status,
                    requested_model_load_status=requested_model_load_status,
                    requested_model_load_failure_type=requested_model_load_failure_type,
                    requested_model_load_failure=requested_model_load_failure,
                    requested_embedding_failure_count=len(requested_failures),
                    requested_embedding_failures=requested_failures,
                    fallback_used=False,
                    fallback_reason=None,
                    fallback_attempts=[],
                    fallback_not_computed_reason=(
                        "bounded_smoke_sample_only_full_650m_sample_not_computed"
                    ),
                    backend_feasibility_status="smoke_sample_computed",
                    started=started,
                )
        else:
            requested_smoke_status = "not_attempted_smoke_not_allowed"
            requested_backend_feasibility_status = (
                "cached_but_smoke_not_explicitly_allowed"
            )
            requested_model_load_status = "not_attempted_smoke_not_allowed"
            requested_model_load_failure_type = "LargerModelSmokeNotAllowed"
            requested_model_load_failure = (
                "requested ESM-2 weights appear cached, but larger-model smoke "
                "execution was not explicitly allowed"
            )
            requested_failures = _esm2_backend_failures(
                accessions=accessions,
                error_type=requested_model_load_failure_type,
                error=requested_model_load_failure,
            )
            fallback_reason = "requested_backend_smoke_not_explicitly_allowed"

    fallback_attempts: list[dict[str, Any]] = []
    for fallback_backend in _esm2_local_fallback_backends(requested_backend):
        fallback_model_name = ESM2_BACKEND_MODEL_NAMES[fallback_backend]
        fallback_cache = _esm2_model_local_cache_status(fallback_model_name)
        attempt: dict[str, Any] = {
            "embedding_backend": fallback_backend,
            "model_name": fallback_model_name,
            "expected_embedding_vector_dimension": (
                ESM2_BACKEND_EXPECTED_DIMENSIONS.get(fallback_backend)
            ),
            "local_cache_status": fallback_cache["local_cache_status"],
            "weights_cached": fallback_cache["weights_cached"],
            "attempted_model_load": False,
            "embedding_backend_available": False,
            "backend_feasibility_status": "skipped_cache_missing",
        }
        should_attempt = fallback_cache["weights_cached"] or (
            fallback_backend == DEFAULT_ESM2_BACKEND
        )
        if not should_attempt:
            fallback_attempts.append(attempt)
            continue
        attempt["attempted_model_load"] = True
        fallback_payload = _compute_esm2_embeddings(
            records_by_accession=records_by_accession,
            accessions=accessions,
            backend=fallback_backend,
            model_name=fallback_model_name,
            local_files_only=True,
        )
        fallback_meta = fallback_payload["metadata"]
        attempt.update(
            {
                "embedding_backend_available": fallback_meta.get(
                    "embedding_backend_available"
                ),
                "embedding_failure_count": fallback_meta.get(
                    "embedding_failure_count", 0
                ),
                "embedding_vector_dimension": fallback_meta.get(
                    "embedding_vector_dimension"
                ),
                "model_load_status": fallback_meta.get("model_load_status"),
                "model_load_failure_type": fallback_meta.get(
                    "model_load_failure_type"
                ),
                "backend_feasibility_status": fallback_meta.get(
                    "backend_feasibility_status"
                ),
            }
        )
        fallback_attempts.append(attempt)
        if fallback_meta.get("embedding_backend_available"):
            return _attach_esm2_request_context(
                payload=fallback_payload,
                requested_backend=requested_backend,
                requested_model_name=requested_model_name,
                requested_cache=requested_cache,
                requested_backend_feasibility_status=(
                    requested_backend_feasibility_status
                ),
                requested_smoke_status=requested_smoke_status,
                requested_model_load_status=requested_model_load_status,
                requested_model_load_failure_type=requested_model_load_failure_type,
                requested_model_load_failure=requested_model_load_failure,
                requested_embedding_failure_count=len(requested_failures),
                requested_embedding_failures=requested_failures,
                fallback_used=True,
                fallback_reason=fallback_reason,
                fallback_attempts=fallback_attempts,
                fallback_not_computed_reason=None,
                backend_feasibility_status=(
                    "fallback_computed_requested_model_unavailable_locally"
                    if requested_smoke_status == "not_attempted_weights_not_cached"
                    else "fallback_computed_requested_smoke_not_allowed"
                ),
                started=started,
            )

    return _esm2_local_unavailable_payload(
        accessions=accessions,
        backend=requested_backend,
        model_name=requested_model_name,
        local_files_only=True,
        started=started,
        requested_cache=requested_cache,
        requested_backend_feasibility_status=requested_backend_feasibility_status,
        requested_smoke_status=requested_smoke_status,
        requested_model_load_status=requested_model_load_status,
        requested_model_load_failure_type=requested_model_load_failure_type,
        requested_model_load_failure=requested_model_load_failure,
        requested_embedding_failures=requested_failures,
        fallback_attempts=fallback_attempts,
        fallback_not_computed_reason=(
            "no_supported_esm2_backend_available_in_local_cache"
        ),
    )


def _attach_esm2_request_context(
    *,
    payload: dict[str, Any],
    requested_backend: str,
    requested_model_name: str,
    requested_cache: dict[str, Any],
    requested_backend_feasibility_status: str,
    requested_smoke_status: str,
    requested_model_load_status: str | None,
    requested_model_load_failure_type: str | None,
    requested_model_load_failure: str | None,
    requested_embedding_failure_count: int,
    requested_embedding_failures: list[dict[str, str]],
    fallback_used: bool,
    fallback_reason: str | None,
    fallback_attempts: list[dict[str, Any]],
    fallback_not_computed_reason: str | None,
    backend_feasibility_status: str,
    started: float,
) -> dict[str, Any]:
    metadata = payload["metadata"]
    actual_backend = metadata.get("embedding_backend")
    metadata.update(
        {
            "requested_embedding_backend": requested_backend,
            "requested_model_name": requested_model_name,
            "requested_expected_embedding_vector_dimension": (
                ESM2_BACKEND_EXPECTED_DIMENSIONS.get(requested_backend)
            ),
            "requested_embedding_backend_available": (
                requested_backend == actual_backend
                and metadata.get("embedding_backend_available") is True
            ),
            "requested_backend_feasibility_status": (
                requested_backend_feasibility_status
            ),
            "requested_backend_local_cache_status": requested_cache[
                "local_cache_status"
            ],
            "requested_backend_weights_cached": requested_cache["weights_cached"],
            "requested_backend_cache_snapshot_count": requested_cache[
                "snapshot_count"
            ],
            "requested_backend_smoke_status": requested_smoke_status,
            "requested_model_load_status": requested_model_load_status,
            "requested_model_load_failure_type": requested_model_load_failure_type,
            "requested_model_load_failure": requested_model_load_failure,
            "requested_embedding_failure_count": requested_embedding_failure_count,
            "computed_embedding_backend": actual_backend,
            "fallback_used": fallback_used,
            "fallback_selected_backend": actual_backend if fallback_used else None,
            "fallback_reason": fallback_reason,
            "fallback_attempts": fallback_attempts,
            "fallback_not_computed_reason": fallback_not_computed_reason,
            "backend_feasibility_status": backend_feasibility_status,
            "largest_feasible_embedding_backend": (
                actual_backend
                if metadata.get("embedding_backend_available")
                else metadata.get("largest_feasible_embedding_backend")
            ),
            "elapsed_seconds_including_fallback": round(
                time.perf_counter() - started, 4
            ),
        }
    )
    if fallback_used:
        metadata["attempted_embedding_backend"] = requested_backend
        metadata["blocker_not_removed"] = (
            "requested_650m_or_larger_representation_backend_not_computed"
        )
    payload["requested_embedding_failures"] = requested_embedding_failures
    return payload


def _esm2_local_unavailable_payload(
    *,
    accessions: list[str],
    backend: str,
    model_name: str,
    local_files_only: bool,
    started: float,
    requested_cache: dict[str, Any],
    requested_backend_feasibility_status: str,
    requested_smoke_status: str,
    requested_model_load_status: str | None,
    requested_model_load_failure_type: str | None,
    requested_model_load_failure: str | None,
    requested_embedding_failures: list[dict[str, str]],
    fallback_attempts: list[dict[str, Any]],
    fallback_not_computed_reason: str,
) -> dict[str, Any]:
    return {
        "metadata": {
            "embedding_backend": backend,
            "embedding_backend_available": False,
            "embedding_vector_dimension": None,
            "model_name": model_name,
            "requested_model_name": model_name,
            "local_files_only": local_files_only,
            "embedding_failure_count": len(accessions),
            "embedding_elapsed_seconds": round(time.perf_counter() - started, 4),
            "model_load_elapsed_seconds": 0.0,
            "model_load_status": requested_model_load_status,
            "model_load_failure_type": requested_model_load_failure_type,
            "model_load_failure": requested_model_load_failure,
            "backend_feasibility_status": "model_unavailable_locally",
            "largest_feasible_embedding_backend": None,
            "fallback_not_computed_reason": fallback_not_computed_reason,
            "requested_embedding_backend": backend,
            "requested_expected_embedding_vector_dimension": (
                ESM2_BACKEND_EXPECTED_DIMENSIONS.get(backend)
            ),
            "requested_embedding_backend_available": False,
            "requested_backend_feasibility_status": (
                requested_backend_feasibility_status
            ),
            "requested_backend_local_cache_status": requested_cache[
                "local_cache_status"
            ],
            "requested_backend_weights_cached": requested_cache["weights_cached"],
            "requested_backend_cache_snapshot_count": requested_cache[
                "snapshot_count"
            ],
            "requested_backend_smoke_status": requested_smoke_status,
            "requested_model_load_status": requested_model_load_status,
            "requested_model_load_failure_type": requested_model_load_failure_type,
            "requested_model_load_failure": requested_model_load_failure,
            "requested_embedding_failure_count": len(requested_embedding_failures),
            "computed_embedding_backend": None,
            "fallback_used": False,
            "fallback_selected_backend": None,
            "fallback_reason": None,
            "fallback_attempts": fallback_attempts,
            "blocker_not_removed": (
                "requested_650m_or_larger_representation_backend_not_computed"
            ),
            **_esm2_backend_metadata(backend),
        },
        "embeddings_by_accession": {},
        "warnings_by_accession": {},
        "embedding_failures": requested_embedding_failures,
        "requested_embedding_failures": requested_embedding_failures,
        "warnings": [
            (
                "requested ESM-2 backend was unavailable locally and no "
                "supported local fallback could be computed"
            )
        ],
    }


def _esm2_local_fallback_backends(requested_backend: str) -> list[str]:
    try:
        requested_index = ESM2_BACKEND_FALLBACK_ORDER.index(requested_backend)
    except ValueError:
        return [DEFAULT_ESM2_BACKEND]
    return list(ESM2_BACKEND_FALLBACK_ORDER[requested_index + 1 :])


def _esm2_backend_failures(
    *,
    accessions: list[str],
    error_type: str,
    error: str,
) -> list[dict[str, str]]:
    return [
        {
            "accession": accession,
            "error_type": error_type,
            "error": error,
        }
        for accession in accessions
    ]


def _esm2_model_local_cache_status(model_name: str) -> dict[str, Any]:
    if not model_name:
        return {
            "model_name": model_name,
            "local_cache_checked": True,
            "local_cache_status": "model_name_missing",
            "weights_cached": False,
            "config_cached": False,
            "tokenizer_cached": False,
            "snapshot_count": 0,
            "cache_root_count": 0,
        }
    cache_dir_name = "models--" + model_name.replace("/", "--")
    snapshots: list[Path] = []
    for cache_root in _huggingface_hub_cache_roots():
        model_cache_dir = cache_root / cache_dir_name
        snapshot_dir = model_cache_dir / "snapshots"
        if snapshot_dir.is_dir():
            snapshots.extend(
                snapshot
                for snapshot in snapshot_dir.iterdir()
                if snapshot.is_dir()
            )
    config_cached = any((snapshot / "config.json").exists() for snapshot in snapshots)
    weights_cached = any(
        any((snapshot / filename).exists() for filename in ESM2_BACKEND_WEIGHT_FILENAMES)
        for snapshot in snapshots
    )
    tokenizer_cached = any(
        any(
            (snapshot / filename).exists()
            for filename in ("tokenizer.json", "tokenizer_config.json", "vocab.txt")
        )
        for snapshot in snapshots
    )
    if weights_cached and config_cached:
        local_cache_status = "weights_cached"
    elif weights_cached:
        local_cache_status = "weights_cached_config_missing"
    elif config_cached or tokenizer_cached:
        local_cache_status = "metadata_cached_without_weights"
    else:
        local_cache_status = "not_cached"
    return {
        "model_name": model_name,
        "local_cache_checked": True,
        "local_cache_status": local_cache_status,
        "weights_cached": weights_cached,
        "config_cached": config_cached,
        "tokenizer_cached": tokenizer_cached,
        "snapshot_count": len(snapshots),
        "cache_root_count": len(_huggingface_hub_cache_roots()),
    }


def _huggingface_hub_cache_roots() -> list[Path]:
    roots: list[Path] = []
    for env_name in ("HUGGINGFACE_HUB_CACHE", "TRANSFORMERS_CACHE"):
        env_value = os.environ.get(env_name)
        if env_value:
            roots.append(Path(env_value).expanduser())
    hf_home = Path(os.environ.get("HF_HOME", "~/.cache/huggingface")).expanduser()
    roots.append(hf_home / "hub")
    roots.append(Path("~/.cache/huggingface/hub").expanduser())
    unique_roots: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            unique_roots.append(root)
            seen.add(key)
    return unique_roots


def _compute_esm2_t6_embeddings(
    *,
    records_by_accession: dict[str, dict[str, Any]],
    accessions: list[str],
    model_name: str,
    local_files_only: bool = False,
) -> dict[str, Any]:
    return _compute_esm2_embeddings(
        records_by_accession=records_by_accession,
        accessions=accessions,
        backend=DEFAULT_ESM2_BACKEND,
        model_name=model_name,
        local_files_only=local_files_only,
    )


def _compute_esm2_embeddings(
    *,
    records_by_accession: dict[str, dict[str, Any]],
    accessions: list[str],
    backend: str,
    model_name: str,
    local_files_only: bool = False,
) -> dict[str, Any]:
    started = time.perf_counter()
    load_started = time.perf_counter()
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(
            model_name, local_files_only=local_files_only
        )
        model = AutoModel.from_pretrained(
            model_name, local_files_only=local_files_only
        )
        model.eval()
        model_load_elapsed = round(time.perf_counter() - load_started, 4)
    except Exception as exc:  # pragma: no cover - depends on local model stack/cache
        model_load_elapsed = round(time.perf_counter() - load_started, 4)
        return {
            "metadata": {
                "embedding_backend": backend,
                "embedding_backend_available": False,
                "embedding_vector_dimension": None,
                "model_name": model_name,
                "requested_model_name": model_name,
                "local_files_only": local_files_only,
                "embedding_failure_count": len(accessions),
                "embedding_elapsed_seconds": round(time.perf_counter() - started, 4),
                "model_load_elapsed_seconds": model_load_elapsed,
                "model_load_status": "failed",
                "model_load_failure_type": type(exc).__name__,
                "model_load_failure": str(exc),
                "backend_feasibility_status": (
                    "model_unavailable_locally"
                    if local_files_only
                    else "model_load_failed"
                ),
                "largest_feasible_embedding_backend": None,
                "fallback_not_computed_reason": (
                    "local_files_only_prevents_downloading_uncached_model"
                    if local_files_only
                    else "model_load_failed_before_embedding"
                ),
                "requested_embedding_backend": backend,
                "requested_backend_feasibility_status": (
                    "model_unavailable_locally"
                    if local_files_only
                    else "model_load_failed"
                ),
                "requested_backend_local_cache_status": (
                    _esm2_model_local_cache_status(model_name)["local_cache_status"]
                    if local_files_only
                    else "not_checked"
                ),
                "requested_backend_weights_cached": (
                    _esm2_model_local_cache_status(model_name)["weights_cached"]
                    if local_files_only
                    else None
                ),
                "requested_backend_smoke_status": "not_applicable",
                "requested_expected_embedding_vector_dimension": (
                    ESM2_BACKEND_EXPECTED_DIMENSIONS.get(backend)
                ),
                "requested_embedding_failure_count": len(accessions),
                "requested_embedding_backend_available": False,
                "computed_embedding_backend": None,
                "fallback_used": False,
                "fallback_selected_backend": None,
                "fallback_reason": None,
                "fallback_attempts": [],
                **_esm2_backend_metadata(backend),
            },
            "embeddings_by_accession": {},
            "warnings_by_accession": {},
            "embedding_failures": [
                {
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                for accession in accessions
            ],
            "warnings": [
                f"ESM-2 backend could not be loaded locally: {type(exc).__name__}: {exc}"
            ],
        }

    embeddings: dict[str, list[float]] = {}
    warnings_by_accession: dict[str, str] = {}
    failures: list[dict[str, str]] = []
    vector_dimension: int | None = None
    for accession in accessions:
        sequence = _clean_sequence(records_by_accession.get(accession, {}).get("sequence"))
        if not sequence:
            failures.append(
                {
                    "accession": accession,
                    "error_type": "MissingSequence",
                    "error": "no sequence available for embedding",
                }
            )
            continue
        try:
            if len(sequence) > 1022:
                warnings_by_accession[accession] = "sequence_truncated_to_1022_residues"
            inputs = tokenizer(
                sequence,
                return_tensors="pt",
                truncation=True,
                max_length=1022,
            )
            with torch.no_grad():
                outputs = model(**inputs)
            hidden = outputs.last_hidden_state[0]
            mask = inputs["attention_mask"][0].bool()
            true_positions = mask.nonzero(as_tuple=False).flatten()
            if len(true_positions) > 2:
                mask[true_positions[0]] = False
                mask[true_positions[-1]] = False
            selected = hidden[mask]
            if selected.numel() == 0:
                selected = hidden[inputs["attention_mask"][0].bool()]
            vector = selected.mean(dim=0).detach().cpu().tolist()
            vector_dimension = len(vector)
            embeddings[accession] = [float(value) for value in vector]
        except Exception as exc:  # pragma: no cover - model runtime dependent
            failures.append(
                {
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
    return {
        "metadata": {
            "embedding_backend": backend,
            "embedding_backend_available": bool(embeddings),
            "embedding_vector_dimension": vector_dimension,
            "model_name": model_name,
            "requested_model_name": model_name,
            "local_files_only": local_files_only,
            "embedding_failure_count": len(failures),
            "embedding_elapsed_seconds": round(time.perf_counter() - started, 4),
            "model_load_elapsed_seconds": model_load_elapsed,
            "model_load_status": "loaded",
            "backend_feasibility_status": (
                "computed"
                if len(embeddings) == len(accessions)
                else "partially_computed"
                if embeddings
                else "embedding_runtime_failed"
            ),
            "largest_feasible_embedding_backend": backend if embeddings else None,
            "fallback_not_computed_reason": None if embeddings else "embedding_runtime_failed",
            "requested_embedding_backend": backend,
            "requested_backend_feasibility_status": (
                "computed"
                if len(embeddings) == len(accessions)
                else "partially_computed"
                if embeddings
                else "embedding_runtime_failed"
            ),
            "requested_backend_local_cache_status": (
                _esm2_model_local_cache_status(model_name)["local_cache_status"]
                if local_files_only
                else "not_checked"
            ),
            "requested_backend_weights_cached": (
                _esm2_model_local_cache_status(model_name)["weights_cached"]
                if local_files_only
                else None
            ),
            "requested_backend_smoke_status": "not_applicable",
            "requested_expected_embedding_vector_dimension": (
                ESM2_BACKEND_EXPECTED_DIMENSIONS.get(backend)
            ),
            "requested_embedding_failure_count": len(failures),
            "requested_embedding_backend_available": bool(embeddings),
            "computed_embedding_backend": backend if embeddings else None,
            "fallback_used": False,
            "fallback_selected_backend": None,
            "fallback_reason": None,
            "fallback_attempts": [],
            **_esm2_backend_metadata(backend),
        },
        "embeddings_by_accession": embeddings,
        "warnings_by_accession": warnings_by_accession,
        "embedding_failures": failures,
        "warnings": [
            (
                "ESM-2 embeddings are computed review-only controls; they do "
                "not replace active-site evidence, sequence-search completion, "
                "expert decisions, or factory gates"
            )
        ],
    }


def _representation_heuristic_disagreement_status(
    *,
    heuristic_top1: Any,
    representation_status: str,
    nearest_reference_entry_ids: list[Any],
    plan_row: dict[str, Any],
) -> str:
    comparison_status = str(plan_row.get("comparison_status") or "")
    if representation_status == "representation_near_duplicate_holdout":
        return "representation_near_duplicate_overrides_heuristic_review"
    if heuristic_top1 == "metal_dependent_hydrolase" and "boundary" in comparison_status:
        return "heuristic_metal_hydrolase_boundary_contrast_priority"
    if nearest_reference_entry_ids and plan_row.get("sequence_search_task"):
        return "learned_nearest_reference_requires_sequence_review"
    return "no_disagreement_signal"


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


def _external_sequence_search_export_blockers(
    search_task: str,
    *,
    current_reference_screen_complete: bool = False,
) -> list[str]:
    blockers = [
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if search_task == "keep_sequence_holdout_control":
        blockers.insert(0, "sequence_holdout_control_not_resolved")
    elif current_reference_screen_complete:
        blockers.insert(
            0,
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
        )
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


def _external_active_site_sourcing_resolution_status(
    *,
    active_features: list[dict[str, Any]],
    binding_features: list[dict[str, Any]],
    catalytic_comments: list[dict[str, Any]],
    fetch_failed: bool,
) -> str:
    if fetch_failed:
        return "source_fetch_failed"
    if active_features:
        return "explicit_uniprot_active_site_positions_found"
    if binding_features and catalytic_comments:
        return "binding_and_reaction_context_only_no_active_site_positions"
    if binding_features:
        return "binding_context_only_no_active_site_positions"
    if catalytic_comments:
        return "reaction_context_only_no_active_site_positions"
    return "no_uniprot_active_site_or_binding_context_found"


def _external_active_site_sourcing_resolution_blockers(status: str) -> list[str]:
    blockers = [
        "external_review_decision_artifact_not_built",
        "full_label_factory_gate_not_run",
    ]
    if status == "explicit_uniprot_active_site_positions_found":
        blockers.insert(0, "active_site_positions_need_mapping_and_review")
    elif status == "source_fetch_failed":
        blockers.insert(0, "active_site_source_fetch_failed")
    else:
        blockers.insert(0, "explicit_active_site_residue_sources_absent")
    return blockers


def _external_sourced_active_site_positions(
    active_features: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    for feature in active_features:
        if not isinstance(feature, dict):
            continue
        positions.append(
            {
                "begin": feature.get("begin"),
                "end": feature.get("end"),
                "description": feature.get("description"),
                "evidence": feature.get("evidence", []),
            }
        )
    return positions


def _external_feature_evidence_reference_count(
    features: list[dict[str, Any]],
) -> int:
    seen: set[tuple[str, str, str]] = set()
    for feature in features:
        if not isinstance(feature, dict):
            continue
        feature_type = str(feature.get("feature_type") or "")
        for evidence in feature.get("evidence", []) or []:
            if not isinstance(evidence, dict):
                continue
            source = str(evidence.get("source") or "")
            evidence_id = str(evidence.get("id") or "")
            evidence_code = str(evidence.get("evidence_code") or "")
            if source or evidence_id or evidence_code:
                seen.add((feature_type, source, evidence_id or evidence_code))
    return len(seen)


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
    backend_sequence_search: dict[str, Any] | None = None,
) -> list[str]:
    blockers: list[str] = []
    sequence_status = str((sequence or {}).get("screen_status") or "")
    backend_status = str((backend_sequence_search or {}).get("search_status") or "")
    backend_complete = bool(
        (backend_sequence_search or {}).get("backend_search_complete")
    )
    if (
        sequence_status == "preexisting_sequence_holdout_retained"
        or backend_status == "exact_reference_holdout"
    ):
        blockers.append("exact_sequence_holdout")
    elif (
        sequence_status == "near_duplicate_candidate_holdout"
        or backend_status == "near_duplicate_holdout"
    ):
        blockers.append("near_duplicate_candidate_holdout")
    elif backend_status in {"backend_unavailable", "backend_failed"}:
        blockers.append("complete_near_duplicate_search_required")
    elif backend_complete and backend_status == "no_near_duplicate_signal":
        pass
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
    backend_sequence_search: dict[str, Any] | None = None,
    active_site_resolution: dict[str, Any] | None = None,
    backend_sample: dict[str, Any] | None = None,
) -> list[str]:
    blockers: list[str] = []
    backend_removes_sequence_search = _backend_sequence_search_removes_blocker(
        backend_sequence_search
    )
    blockers.extend(
        str(blocker)
        for blocker in readiness.get("blockers", []) or []
        if not (
            backend_removes_sequence_search
            and blocker == "complete_near_duplicate_search_required"
        )
    )
    if active_site is not None:
        blockers.extend(
            str(blocker) for blocker in active_site.get("blockers", []) or []
        )
    if active_site_resolution is not None:
        blockers.extend(
            str(blocker)
            for blocker in active_site_resolution.get("blockers", []) or []
        )
    if sequence is not None:
        blockers.extend(
            str(blocker)
            for blocker in sequence.get("blockers", []) or []
            if not (
                backend_removes_sequence_search
                and blocker
                in {
                    "complete_uniref_or_all_vs_all_near_duplicate_search_required",
                    "complete_near_duplicate_reference_search_not_completed",
                }
            )
        )
    else:
        blockers.append("sequence_search_export_missing")
    if backend is not None:
        blockers.extend(str(blocker) for blocker in backend.get("blockers", []) or [])
    else:
        blockers.append("representation_backend_plan_missing_or_not_eligible")
    if backend_sample is not None:
        blockers.extend(
            str(blocker) for blocker in backend_sample.get("blockers", []) or []
        )
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
    backend_sequence_search: dict[str, Any] | None = None,
    active_site_resolution: dict[str, Any] | None = None,
    backend_sample: dict[str, Any] | None = None,
) -> str:
    if active_site is not None:
        source_task = str(active_site.get("source_task") or "")
        if source_task == "find_primary_active_site_or_residue_role_source":
            return "find_primary_active_site_or_residue_role_source"
        if active_site_resolution is not None and str(
            active_site_resolution.get("active_site_source_status") or ""
        ).endswith("_no_active_site_positions"):
            return "curate_primary_literature_or_pdb_active_site_sources"
        if source_task:
            return "complete_active_site_source_review_packet"
    search_task = str((sequence or {}).get("search_task") or "")
    if search_task == "keep_sequence_holdout_control":
        return "keep_sequence_holdout_out_of_import_batch"
    if search_task and not _backend_sequence_search_removes_blocker(
        backend_sequence_search
    ):
        return "complete_near_duplicate_sequence_search"
    backend_sample_status = str((backend_sample or {}).get("backend_status") or "")
    if backend_sample_status == "representation_near_duplicate_holdout":
        return "keep_representation_near_duplicate_out_of_import_batch"
    if backend is not None:
        return "select_and_run_real_representation_backend"
    return str(
        readiness.get("next_action")
        or "complete_external_review_prerequisites_before_decision"
    )


def _external_transfer_blocker_matrix_active_site(
    active_site: dict[str, Any] | None,
    *,
    active_site_resolution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if active_site is None:
        return {
            "source_task": "not_active_site_sourcing_row",
            "decision_status": None,
            "source_target_count": 0,
            "resolution_status": (
                (active_site_resolution or {}).get("active_site_source_status")
            ),
        }
    return {
        "source_task": active_site.get("source_task"),
        "decision_status": (active_site.get("decision") or {}).get("decision_status"),
        "queue_status": active_site.get("queue_status"),
        "resolution_status": (
            (active_site_resolution or {}).get("active_site_source_status")
        ),
        "sourced_active_site_position_count": len(
            (active_site_resolution or {}).get("sourced_active_site_positions", [])
            or []
        ),
        "source_target_count": len(active_site.get("source_targets", []) or []),
    }


def _external_transfer_blocker_matrix_sequence(
    sequence: dict[str, Any] | None,
    *,
    backend_sequence_search: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if sequence is None:
        return {
            "backend_name": (backend_sequence_search or {}).get("backend_name"),
            "backend_search_status": (backend_sequence_search or {}).get(
                "search_status"
            ),
            "search_task": None,
            "decision_status": None,
            "source_target_count": 0,
        }
    return {
        "alignment_status": sequence.get("alignment_status"),
        "backend_name": (backend_sequence_search or {}).get("backend_name"),
        "backend_search_status": (backend_sequence_search or {}).get("search_status"),
        "backend_max_external_vs_reference_identity": (
            (backend_sequence_search or {}).get("max_external_vs_reference_identity")
        ),
        "decision_status": (sequence.get("decision") or {}).get("decision_status"),
        "search_task": sequence.get("search_task"),
        "source_target_count": len(sequence.get("source_targets", []) or []),
    }


def _backend_sequence_search_removes_blocker(
    backend_sequence_search: dict[str, Any] | None,
) -> bool:
    if not backend_sequence_search:
        return False
    return (
        backend_sequence_search.get("backend_search_complete") is True
        and backend_sequence_search.get("search_status") == "no_near_duplicate_signal"
        and backend_sequence_search.get("backend_name")
        in {"mmseqs2_easy_search", "diamond_blastp", "blastp"}
    )


def _external_transfer_blocker_matrix_backend(
    backend: dict[str, Any] | None,
    *,
    backend_sample: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if backend is None:
        return {
            "backend_readiness_status": "not_backend_eligible_yet",
            "embedding_status": "not_planned",
            "sample_backend_status": (backend_sample or {}).get("backend_status"),
            "sample_embedding_status": (backend_sample or {}).get("embedding_status"),
            "recommended_backend_count": 0,
            "required_input_count": 0,
        }
    nearest_reference = (backend_sample or {}).get("nearest_reference") or {}
    return {
        "backend_readiness_status": backend.get("backend_readiness_status"),
        "embedding_status": backend.get("embedding_status"),
        "sample_backend_status": (backend_sample or {}).get("backend_status"),
        "sample_embedding_status": (backend_sample or {}).get("embedding_status"),
        "sample_near_duplicate_alert": (
            (backend_sample or {}).get("backend_status")
            == "representation_near_duplicate_holdout"
        ),
        "sample_nearest_reference_accession": nearest_reference.get(
            "reference_accession"
        ),
        "sample_top_embedding_cosine": (backend_sample or {}).get(
            "top_embedding_cosine"
        ),
        "recommended_backend_count": len(backend.get("recommended_backends", []) or []),
        "required_input_count": len(backend.get("required_inputs", []) or []),
        "sequence_search_task": backend.get("sequence_search_task"),
    }
