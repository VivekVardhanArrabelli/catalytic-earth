from __future__ import annotations

import hashlib
import re
import shlex
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

from .labels import MechanismLabel, label_summary


CLUSTERING_TOOL_CANDIDATES = ("foldseek", "mmseqs", "blastp", "diamond")
SEQUENCE_FIELD_NAMES = (
    "sequence",
    "protein_sequence",
    "amino_acid_sequence",
    "reference_sequence",
)
MMSEQS_CLUSTER_COVERAGE_MODE = 0
SUPPORTED_COORDINATE_STRUCTURE_SOURCES = {"pdb", "alphafold"}


def build_sequence_distance_holdout_eval(
    *,
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    sequence_clusters: dict[str, Any],
    geometry: dict[str, Any] | None = None,
    slice_id: str,
    abstain_threshold: float,
    holdout_fraction: float = 0.2,
    min_holdout_rows: int = 40,
    sequence_fasta: str | None = None,
    sequence_identity_backend: str = "auto",
    sequence_identity_threshold: float = 0.30,
    sequence_identity_coverage: float = 0.80,
    compute_max_train_test_identity: bool = True,
    mmseqs_binary: str = "mmseqs",
) -> dict[str, Any]:
    """Evaluate retrieval on a sequence-distance held-out partition.

    When an amino-acid FASTA or row-level sequences are available, MMseqs2 is
    used to cluster evaluated rows by real sequence identity. If not, the
    command falls back to the legacy deterministic local proxy and labels that
    limitation explicitly.
    """

    labels_by_entry = {label.entry_id: label for label in labels}
    geometry_by_entry = {
        str(entry.get("entry_id")): entry
        for entry in (geometry or {}).get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("entry_id"), str)
    }
    sequence_rows_by_entry, sequence_cluster_sizes = _sequence_cluster_indexes(
        sequence_clusters
    )
    result_rows = _evaluation_rows(
        retrieval=retrieval,
        labels_by_entry=labels_by_entry,
        geometry_by_entry=geometry_by_entry,
        sequence_rows_by_entry=sequence_rows_by_entry,
        sequence_cluster_sizes=sequence_cluster_sizes,
        abstain_threshold=abstain_threshold,
    )
    structure_counts = Counter(row["selected_structure_proxy_id"] for row in result_rows)
    geometry_bucket_counts = Counter(row["active_site_geometry_proxy_bucket"] for row in result_rows)
    for row in result_rows:
        row["selected_structure_proxy_count"] = int(
            structure_counts.get(row["selected_structure_proxy_id"], 0)
        )
        row["active_site_geometry_proxy_bucket_count"] = int(
            geometry_bucket_counts.get(row["active_site_geometry_proxy_bucket"], 0)
        )
        row["low_neighborhood_proxy_score"] = _low_neighborhood_proxy_score(row)
        row["low_similarity_proxy_pass"] = (
            row["sequence_cluster_entry_count"] == 1
            and row["selected_structure_proxy_count"] == 1
        )
        row["fold_divergence_proxy_pass"] = (
            row["selected_structure_proxy_count"] == 1
            and row["active_site_geometry_proxy_bucket_count"] <= 3
        )

    real_split = _real_sequence_identity_split(
        rows=result_rows,
        sequence_rows_by_entry=sequence_rows_by_entry,
        sequence_fasta=sequence_fasta,
        slice_id=str(slice_id),
        backend=sequence_identity_backend,
        threshold=sequence_identity_threshold,
        coverage=sequence_identity_coverage,
        mmseqs_binary=mmseqs_binary,
    )
    if real_split.get("usable"):
        for row in result_rows:
            entry_id = str(row["entry_id"])
            row["real_sequence_identity_cluster_id"] = real_split[
                "entry_clusters"
            ].get(entry_id, f"missing_sequence:{entry_id}")
            row["real_sequence_identity_available"] = entry_id in real_split[
                "entries_with_sequence"
            ]
            row["real_sequence_record_count"] = int(
                real_split["sequence_record_counts_by_entry"].get(entry_id, 0)
            )
            row["real_sequence_accessions"] = real_split[
                "sequence_accessions_by_entry"
            ].get(entry_id, [])
            row["real_sequence_identity_note"] = (
                "mmseqs2_sequence_identity_cluster"
                if row["real_sequence_identity_available"]
                else "missing_sequence_for_real_identity_backend"
            )
        heldout_ids, partition_notes = _select_holdout_entry_ids_by_real_clusters(
            result_rows,
            entry_clusters=real_split["entry_clusters"],
            holdout_fraction=holdout_fraction,
            min_holdout_rows=min_holdout_rows,
        )
    else:
        for row in result_rows:
            row["real_sequence_identity_cluster_id"] = None
            row["real_sequence_identity_available"] = False
            row["real_sequence_record_count"] = 0
            row["real_sequence_accessions"] = []
            row["real_sequence_identity_note"] = "real_sequence_identity_not_computed"
        heldout_ids, partition_notes = _select_holdout_entry_ids(
            result_rows,
            holdout_fraction=holdout_fraction,
            min_holdout_rows=min_holdout_rows,
        )
    for row in result_rows:
        row["partition"] = "heldout" if row["entry_id"] in heldout_ids else "in_distribution"

    train_test_identity = _empty_train_test_identity_metadata()
    if real_split.get("usable") and compute_max_train_test_identity:
        train_test_identity = _compute_mmseqs_train_test_identity(
            records_by_id=real_split["records_by_id"],
            heldout_entry_ids=heldout_ids,
            slice_id=str(slice_id),
            threshold=sequence_identity_threshold,
            coverage=sequence_identity_coverage,
            mmseqs_binary=mmseqs_binary,
            prior_commands=real_split["backend_commands"],
        )
        real_split["backend_commands"] = train_test_identity.get(
            "backend_commands", real_split["backend_commands"]
        )

    heldout_rows = [row for row in result_rows if row["partition"] == "heldout"]
    in_distribution_rows = [
        row for row in result_rows if row["partition"] == "in_distribution"
    ]
    all_metrics = _partition_metrics(result_rows)
    heldout_metrics = _partition_metrics(heldout_rows)
    in_distribution_metrics = _partition_metrics(in_distribution_rows)
    tool_status = {tool: bool(shutil.which(tool)) for tool in CLUSTERING_TOOL_CANDIDATES}
    heldout_cluster_ids = sorted(
        {
            str(row.get("real_sequence_identity_cluster_id"))
            for row in heldout_rows
            if row.get("real_sequence_identity_cluster_id")
        }
    )
    heldout_entry_ids = sorted(
        (str(row["entry_id"]) for row in heldout_rows),
        key=_entry_id_sort_key,
    )
    target_achieved = _sequence_identity_target_achieved(
        real_split=real_split,
        train_test_identity=train_test_identity,
        threshold=sequence_identity_threshold,
    )
    sequence_identity_limitations = _sequence_identity_limitations(
        real_split=real_split,
        train_test_identity=train_test_identity,
        sequence_identity_threshold=sequence_identity_threshold,
    )
    backend = (
        "mmseqs2_cluster_sequence_identity"
        if real_split.get("usable")
        else real_split.get("fallback_backend")
        or "deterministic_local_proxy_sequence_identity_not_computed"
    )

    return {
        "metadata": {
            "method": "sequence_fold_distance_holdout_evaluation",
            "slice_id": str(slice_id),
            "blocker_removed": (
                "reports held-out fingerprint retrieval behavior separately "
                "from in-distribution slice metrics before external-source import"
            ),
            "label_registry_count": len(labels),
            "retrieval_result_count": len(retrieval.get("results", []) or []),
            "evaluated_count": len(result_rows),
            "heldout_count": len(heldout_rows),
            "in_distribution_count": len(in_distribution_rows),
            "abstain_threshold": abstain_threshold,
            "holdout_fraction": holdout_fraction,
            "min_holdout_rows": min_holdout_rows,
            "backend": backend,
            "clustering_backend": backend,
            "clustering_tool_status": tool_status,
            "backend_command": real_split.get("backend_command"),
            "backend_commands": real_split.get("backend_commands", []),
            "backend_resolved_path": real_split.get("backend_resolved_path"),
            "backend_version": real_split.get("backend_version"),
            "sequence_source": real_split.get("sequence_source"),
            "sequence_count": real_split.get("sequence_count", 0),
            "sequence_entry_coverage_count": real_split.get(
                "sequence_entry_coverage_count", 0
            ),
            "sequence_missing_entry_count": real_split.get(
                "sequence_missing_entry_count", len(result_rows)
            ),
            "sequence_missing_entry_ids": real_split.get("sequence_missing_entry_ids", []),
            "cluster_threshold": sequence_identity_threshold,
            "sequence_identity_cluster_threshold": sequence_identity_threshold,
            "sequence_identity_cluster_coverage": sequence_identity_coverage,
            "sequence_identity_cluster_coverage_mode": MMSEQS_CLUSTER_COVERAGE_MODE,
            "sequence_identity_backend_requested": sequence_identity_backend,
            "sequence_identity_backend_available": bool(real_split.get("usable")),
            "real_sequence_identity_computed": bool(real_split.get("usable")),
            "real_sequence_identity_record_cluster_count": real_split.get(
                "record_cluster_count"
            ),
            "real_sequence_identity_entry_cluster_count": real_split.get(
                "entry_cluster_count"
            ),
            "heldout_cluster_ids": heldout_cluster_ids,
            "heldout_entry_ids": heldout_entry_ids,
            "max_observed_train_test_identity": train_test_identity.get(
                "max_observed_train_test_identity"
            ),
            "max_observed_train_test_identity_computable": bool(
                train_test_identity.get("max_observed_train_test_identity_computable")
            ),
            "max_observed_train_test_identity_alignment_count": train_test_identity.get(
                "max_observed_train_test_identity_alignment_count", 0
            ),
            "target_max_train_test_identity": sequence_identity_threshold,
            "target_identity_achieved": target_achieved,
            "sequence_identity_target_achieved": target_achieved,
            "limitations": sequence_identity_limitations,
            "sequence_identity_limitations": sequence_identity_limitations,
            "real_tm_score_computed": False,
            "sequence_identity_target": (
                f"<={sequence_identity_threshold:.2f} train/test sequence identity "
                "when real clustering/alignment is available"
            ),
            "tm_score_target": "<0.70 when Foldseek/TM-score is available",
            "proxy_limitation": (
                "Exact UniProt reference clusters, selected PDB identifiers, "
                "and active-site geometry buckets are low-neighborhood proxies; "
                "they do not replace all-vs-all sequence identity, MMseqs2, "
                "Foldseek, or TM-score clustering."
            ),
            "partition_rule": _partition_rule(real_split),
            "sequence_cluster_method": sequence_clusters.get("metadata", {}).get("method"),
            "sequence_cluster_source": sequence_clusters.get("metadata", {}).get(
                "cluster_source"
            ),
            "geometry_method": (geometry or {}).get("metadata", {}).get("method"),
            "proxy_pass_counts": {
                "low_similarity_proxy_pass": sum(
                    1 for row in result_rows if row["low_similarity_proxy_pass"]
                ),
                "fold_divergence_proxy_pass": sum(
                    1 for row in result_rows if row["fold_divergence_proxy_pass"]
                ),
                "heldout_low_similarity_proxy_pass": sum(
                    1 for row in heldout_rows if row["low_similarity_proxy_pass"]
                ),
                "heldout_fold_divergence_proxy_pass": sum(
                    1 for row in heldout_rows if row["fold_divergence_proxy_pass"]
                ),
            },
            "partition_notes": partition_notes,
            "label_summary": label_summary(labels),
        },
        "metrics": {
            "all": all_metrics,
            "heldout": heldout_metrics,
            "in_distribution": in_distribution_metrics,
        },
        "per_fingerprint_breakdowns": {
            "heldout": _per_fingerprint_breakdowns(heldout_rows),
            "in_distribution": _per_fingerprint_breakdowns(in_distribution_rows),
            "all": _per_fingerprint_breakdowns(result_rows),
        },
        "rows": sorted(result_rows, key=lambda row: _entry_id_sort_key(row["entry_id"])),
    }


def build_foldseek_coordinate_readiness(
    *,
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    slice_id: str,
    geometry: dict[str, Any] | None = None,
    sequence_holdout: dict[str, Any] | None = None,
    foldseek_binary: str = "foldseek",
    coordinate_dir: str | None = None,
    max_coordinate_files: int = 0,
    fetch_pdb_cif_fn: Callable[[str], str] | None = None,
    fetch_external_structure_cif_fn: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Build a review-only artifact for Foldseek coordinate readiness.

    The artifact stages at most ``max_coordinate_files`` unique selected
    structures. It does not compute a Foldseek/TM-score split and never emits
    countable or import-ready rows.
    """

    labels_by_entry = {label.entry_id: label for label in labels}
    geometry_by_entry = {
        str(entry.get("entry_id")): entry
        for entry in (geometry or {}).get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("entry_id"), str)
    }
    retrieval_by_entry = {
        str(result.get("entry_id")): result
        for result in retrieval.get("results", []) or []
        if isinstance(result, dict) and isinstance(result.get("entry_id"), str)
    }
    holdout_by_entry = {
        str(row.get("entry_id")): row
        for row in (sequence_holdout or {}).get("rows", []) or []
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    if holdout_by_entry:
        candidate_entry_ids = sorted(
            (entry_id for entry_id in holdout_by_entry if entry_id in labels_by_entry),
            key=_entry_id_sort_key,
        )
    else:
        candidate_entry_ids = sorted(
            (entry_id for entry_id in retrieval_by_entry if entry_id in labels_by_entry),
            key=_entry_id_sort_key,
        )

    rows: list[dict[str, Any]] = []
    unique_structures: dict[str, dict[str, Any]] = {}
    for entry_id in candidate_entry_ids:
        retrieval_row = retrieval_by_entry.get(entry_id, {})
        geometry_row = geometry_by_entry.get(entry_id, {})
        holdout_row = holdout_by_entry.get(entry_id, {})
        source, structure_id, source_field = _selected_coordinate_structure(
            retrieval_row=retrieval_row,
            geometry_row=geometry_row,
            holdout_row=holdout_row,
        )
        structure_key = (
            f"{source}:{structure_id}" if source and structure_id else "missing_selected_structure"
        )
        possible = bool(
            source in SUPPORTED_COORDINATE_STRUCTURE_SOURCES and structure_id
        )
        row = {
            "entry_id": entry_id,
            "entry_name": (
                retrieval_row.get("entry_name")
                or geometry_row.get("entry_name")
                or holdout_row.get("entry_name")
            ),
            "label_type": labels_by_entry[entry_id].label_type,
            "target_fingerprint_id": labels_by_entry[entry_id].fingerprint_id,
            "evaluated": True,
            "geometry_status": retrieval_row.get("status") or geometry_row.get("status"),
            "sequence_holdout_partition": holdout_row.get("partition"),
            "selected_structure_source": source,
            "selected_structure_id": structure_id,
            "selected_structure_key": structure_key,
            "selected_structure_source_field": source_field,
            "coordinate_materialization_possible": possible,
            "coordinate_materialization_status": (
                "pending_bounded_fetch" if possible else "missing_or_unsupported_structure"
            ),
            "coordinate_path": None,
            "fetch_error": None,
            "countable_label_candidate": False,
            "import_ready": False,
            "tm_score_split_member": False,
            "review_status": "review_only_non_countable",
        }
        if not possible:
            row.update(
                {
                    "tm_score_coordinate_exclusion_status": (
                        "excluded_missing_or_unsupported_selected_structure"
                    ),
                    "tm_score_coordinate_exclusion_reason": (
                        "missing_selected_coordinate_structure"
                        if not source and not structure_id
                        else "unsupported_selected_coordinate_source"
                    ),
                    "tm_score_coordinate_exclusion_evidence": {
                        "geometry_status": retrieval_row.get("status")
                        or geometry_row.get("status"),
                        "selected_structure_key": structure_key,
                        "selected_structure_source": source,
                        "selected_structure_id": structure_id,
                        "selected_structure_source_field": source_field,
                    },
                }
            )
        rows.append(row)
        if possible and structure_key not in unique_structures:
            unique_structures[structure_key] = {
                "source": source,
                "structure_id": structure_id,
                "structure_key": structure_key,
                "first_entry_id": entry_id,
                "entry_ids": [],
                "coordinate_path": None,
                "fetch_status": "not_requested",
                "fetch_error": None,
            }
        if possible:
            unique_structures[structure_key]["entry_ids"].append(entry_id)

    coordinate_dir_path = Path(coordinate_dir) if coordinate_dir else None
    fetch_limit = max(0, int(max_coordinate_files or 0))
    fetch_pdb = fetch_pdb_cif_fn
    fetch_external = fetch_external_structure_cif_fn
    if fetch_limit and coordinate_dir_path and (fetch_pdb is None or fetch_external is None):
        from .structure import fetch_pdb_cif
        from .transfer_scope import fetch_external_structure_cif

        fetch_pdb = fetch_pdb or fetch_pdb_cif
        fetch_external = fetch_external or fetch_external_structure_cif

    staged_keys = set(
        sorted(
            unique_structures,
            key=lambda key: _entry_id_sort_key(str(unique_structures[key]["first_entry_id"])),
        )[:fetch_limit]
    )
    if fetch_limit and coordinate_dir_path:
        coordinate_dir_path.mkdir(parents=True, exist_ok=True)
    for structure_key in sorted(unique_structures):
        structure = unique_structures[structure_key]
        if structure_key not in staged_keys:
            structure["fetch_status"] = (
                "not_requested_fetch_cap_reached" if fetch_limit else "not_requested"
            )
            continue
        if not coordinate_dir_path:
            structure["fetch_status"] = "not_requested_coordinate_dir_missing"
            continue
        source = str(structure["source"])
        structure_id = str(structure["structure_id"])
        coordinate_path = coordinate_dir_path / _coordinate_file_name(source, structure_id)
        try:
            if coordinate_path.exists():
                cif_text = coordinate_path.read_text(encoding="utf-8")
                if not cif_text.strip():
                    raise ValueError("existing coordinate file is empty")
                structure["fetch_status"] = "already_materialized"
            else:
                if source == "pdb":
                    if fetch_pdb is None:
                        raise ValueError("PDB coordinate fetcher is unavailable")
                    cif_text = fetch_pdb(structure_id)
                else:
                    if fetch_external is None:
                        raise ValueError("external coordinate fetcher is unavailable")
                    cif_text = fetch_external(source, structure_id)
                if not str(cif_text).strip():
                    raise ValueError("coordinate fetch returned empty content")
                coordinate_path.write_text(str(cif_text), encoding="utf-8")
                structure["fetch_status"] = "materialized"
            structure["coordinate_path"] = str(coordinate_path)
        except Exception as exc:  # pragma: no cover - live-source failure shape
            structure["fetch_status"] = "fetch_failed"
            structure["fetch_error"] = f"{type(exc).__name__}: {exc}"

    structures_by_key = unique_structures
    for row in rows:
        structure = structures_by_key.get(str(row["selected_structure_key"]))
        if not structure:
            continue
        row["coordinate_path"] = structure.get("coordinate_path")
        row["fetch_error"] = structure.get("fetch_error")
        fetch_status = str(structure.get("fetch_status"))
        if fetch_status in {"materialized", "already_materialized"}:
            row["coordinate_materialization_status"] = fetch_status
        elif fetch_status == "fetch_failed":
            row["coordinate_materialization_status"] = "fetch_failed"
        elif fetch_status == "not_requested_fetch_cap_reached":
            row["coordinate_materialization_status"] = "not_materialized_fetch_cap_reached"
        elif fetch_status == "not_requested_coordinate_dir_missing":
            row["coordinate_materialization_status"] = "not_materialized_coordinate_dir_missing"
        else:
            row["coordinate_materialization_status"] = "not_materialized_not_requested"

    foldseek_info = _foldseek_binary_info(foldseek_binary)
    materialized_keys = sorted(
        key
        for key, structure in structures_by_key.items()
        if structure.get("fetch_status") in {"materialized", "already_materialized"}
    )
    fetch_failures = [
        {
            "structure_key": key,
            "source": structure.get("source"),
            "structure_id": structure.get("structure_id"),
            "entry_ids": structure.get("entry_ids", []),
            "error": structure.get("fetch_error"),
        }
        for key, structure in sorted(structures_by_key.items())
        if structure.get("fetch_status") == "fetch_failed"
    ]
    missing_or_unsupported = [
        {
            "entry_id": row["entry_id"],
            "entry_name": row.get("entry_name"),
            "geometry_status": row.get("geometry_status"),
            "selected_structure_key": row["selected_structure_key"],
            "selected_structure_source": row["selected_structure_source"],
            "selected_structure_id": row["selected_structure_id"],
            "selected_structure_source_field": row.get(
                "selected_structure_source_field"
            ),
            "tm_score_coordinate_exclusion_status": row.get(
                "tm_score_coordinate_exclusion_status"
            ),
            "tm_score_coordinate_exclusion_reason": row.get(
                "tm_score_coordinate_exclusion_reason"
            ),
            "tm_score_coordinate_exclusion_evidence": row.get(
                "tm_score_coordinate_exclusion_evidence"
            ),
        }
        for row in rows
        if not row["coordinate_materialization_possible"]
    ]
    not_materialized = [
        {
            "structure_key": key,
            "source": structure.get("source"),
            "structure_id": structure.get("structure_id"),
            "entry_ids": structure.get("entry_ids", []),
            "fetch_status": structure.get("fetch_status"),
        }
        for key, structure in sorted(structures_by_key.items())
        if structure.get("fetch_status") not in {"materialized", "already_materialized"}
    ]

    all_possible_structures_materialized = (
        bool(structures_by_key)
        and len(materialized_keys) == len(structures_by_key)
        and not missing_or_unsupported
        and not fetch_failures
    )
    all_supported_structures_materialized = (
        bool(structures_by_key)
        and len(materialized_keys) == len(structures_by_key)
        and not fetch_failures
    )
    blocker_key = (
        "blocker_removed" if all_possible_structures_materialized and foldseek_info["available"]
        else "blocker_narrowed"
    )
    blocker_value = (
        "all evaluated selected coordinates are staged and Foldseek is available; TM-score split builder is still not run"
        if blocker_key == "blocker_removed"
        else "selected structure ids, Foldseek provenance, and bounded coordinate materialization status are explicit; remaining unstaged or failed coordinates block TM-score split computation"
    )
    blocker_removed = (
        "all currently materializable supported selected coordinates are staged "
        "and Foldseek is available; removes the unstaged selected-coordinate "
        "sidecar blocker"
        if all_supported_structures_materialized and foldseek_info["available"]
        else None
    )
    blockers_remaining = [
        "full Foldseek/TM-score split builder has not been run",
        "TM-score target checks remain unavailable until a Foldseek signal/split is computed",
    ]
    if not structures_by_key:
        blockers_remaining.append("no supported selected structures were discovered")
    if len(materialized_keys) < len(structures_by_key):
        blockers_remaining.append("supported selected structures remain unstaged")
    if missing_or_unsupported:
        blockers_remaining.append(
            "evaluated rows without supported selected structures are explicitly "
            "excluded from Foldseek coordinate materialization"
        )
    if fetch_failures:
        blockers_remaining.append("one or more selected coordinate fetches failed")
    if not foldseek_info["available"]:
        blockers_remaining.append(
            "Foldseek binary was not resolved or did not report a version"
        )

    limitations = [
        "review-only readiness artifact; it creates no countable labels and no import-ready rows",
        "tm_score_split_computed=false because Foldseek/TM-score clustering is not executed here",
        "coordinate materialization records selected structures only and does not validate catalytic function",
    ]
    if len(materialized_keys) < len(structures_by_key):
        limitations.append(
            "coordinate staging is capped and deterministic; unstaged supported "
            "structures remain TM-score blockers"
        )
    elif structures_by_key:
        limitations.append(
            "coordinate staging is deterministic; all currently materializable "
            "supported selected structures are staged"
        )
    if not foldseek_info["available"]:
        limitations.append("Foldseek binary was not resolved or did not report a version")
    if missing_or_unsupported:
        limitations.append(
            "some evaluated rows are explicitly excluded from Foldseek coordinate "
            "materialization because they lack supported selected PDB/AlphaFold "
            "structure identifiers"
        )
    if fetch_failures:
        limitations.append("one or more selected coordinate fetches failed")
    if not fetch_limit:
        limitations.append("coordinate fetching was not requested; set max_coordinate_files above zero to stage a bounded subset")

    metadata = {
        "method": "foldseek_coordinate_readiness",
        blocker_key: blocker_value,
        "blocker_removed": blocker_removed,
        "blockers_remaining": sorted(set(blockers_remaining)),
        "slice_id": str(slice_id),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "tm_score_split_computed": False,
        "full_tm_score_split_computed": False,
        "real_tm_score_computed": False,
        "label_registry_count": len(labels),
        "retrieval_result_count": len(retrieval.get("results", []) or []),
        "geometry_entry_count": len((geometry or {}).get("entries", []) or []),
        "sequence_holdout_row_count": len((sequence_holdout or {}).get("rows", []) or []),
        "evaluated_count": len(rows),
        "selected_entry_ids": [row["entry_id"] for row in rows],
        "selected_structure_count": len(structures_by_key),
        "selected_structure_ids": sorted(structures_by_key),
        "supported_structure_sources": sorted(SUPPORTED_COORDINATE_STRUCTURE_SOURCES),
        "coordinate_materialization_requested": bool(fetch_limit and coordinate_dir_path),
        "coordinate_materialization_possible_count": sum(
            1 for row in rows if row["coordinate_materialization_possible"]
        ),
        "coordinate_fetch_cap": fetch_limit,
        "coordinate_fetch_cap_applied": bool(
            fetch_limit and len(structures_by_key) > fetch_limit
        ),
        "coordinate_directory": str(coordinate_dir_path) if coordinate_dir_path else None,
        "materialized_coordinate_count": len(materialized_keys),
        "materialized_structure_ids": materialized_keys,
        "available_staged_coordinate_count": len(materialized_keys),
        "staged_coordinate_count": len(materialized_keys),
        "staged_structure_count": len(materialized_keys),
        "missing_or_unsupported_structure_count": len(missing_or_unsupported),
        "missing_or_unsupported_structures": missing_or_unsupported,
        "tm_score_coordinate_exclusion_count": len(missing_or_unsupported),
        "tm_score_coordinate_exclusions": missing_or_unsupported,
        "tm_score_coordinate_exclusion_policy": (
            "exclude rows lacking a supported selected coordinate structure from "
            "Foldseek coordinate materialization, keep them review-only and "
            "non-countable, and report the exclusion before any full TM-score "
            "holdout claim"
        ),
        "fetch_failure_count": len(fetch_failures),
        "fetch_failures": fetch_failures,
        "not_materialized_structure_count": len(not_materialized),
        "not_materialized_structures": not_materialized,
        "tm_signal_coordinate_cap_requested": None,
        "tm_signal_coordinate_cap_applied": False,
        "pair_count": 0,
        "mapped_pair_count": 0,
        "train_test_pair_count": 0,
        "heldout_in_distribution_pair_count": 0,
        "heldout_pair_count": 0,
        "in_distribution_pair_count": 0,
        "max_observed_train_test_tm_score": None,
        "max_observed_train_test_tm_score_computable": False,
        "threshold_target": "<0.7",
        "tm_score_target_achieved_for_computed_subset": None,
        "raw_name_mapping_unmapped_count": 0,
        "raw_name_mapping_unmapped_names": [],
        "foldseek_binary_requested": foldseek_info["requested"],
        "foldseek_binary_resolved": foldseek_info["resolved"],
        "foldseek_binary_available": foldseek_info["available"],
        "foldseek_version": foldseek_info["version"],
        "foldseek_version_command": foldseek_info["version_command"],
        "foldseek_command": foldseek_info["version_command"],
        "limitations": sorted(set(limitations)),
    }

    return {
        "metadata": metadata,
        "structures": [
            {
                "structure_key": key,
                "source": structure.get("source"),
                "structure_id": structure.get("structure_id"),
                "entry_ids": sorted(structure.get("entry_ids", []), key=_entry_id_sort_key),
                "coordinate_path": structure.get("coordinate_path"),
                "fetch_status": structure.get("fetch_status"),
                "fetch_error": structure.get("fetch_error"),
            }
            for key, structure in sorted(structures_by_key.items())
        ],
        "rows": sorted(rows, key=lambda row: _entry_id_sort_key(row["entry_id"])),
    }


def build_foldseek_tm_score_signal(
    *,
    readiness: dict[str, Any],
    slice_id: str | None = None,
    foldseek_binary: str = "/private/tmp/catalytic-foldseek-env/bin/foldseek",
    readiness_path: str | None = None,
    max_staged_coordinates: int | None = None,
    prior_staged_coordinate_count: int | None = None,
    threads: int = 1,
    keep_all_rows: bool = True,
    max_reported_rows: int = 200,
    tm_score_threshold: float = 0.7,
    runner: Callable[[list[str], Path], None] | None = None,
) -> dict[str, Any]:
    """Build a partial Foldseek TM-score signal for staged coordinates only.

    This deliberately does not compute or claim a full TM-score split. It only
    searches the coordinate files already staged by the readiness artifact.
    """

    metadata_in = readiness.get("metadata", {}) if isinstance(readiness, dict) else {}
    if not isinstance(metadata_in, dict):
        metadata_in = {}
    rows_in = readiness.get("rows", []) if isinstance(readiness, dict) else []
    structures_in = readiness.get("structures", []) if isinstance(readiness, dict) else []
    rows = [row for row in rows_in if isinstance(row, dict)]
    structures = [item for item in structures_in if isinstance(item, dict)]

    row_partitions_by_entry = {
        str(row.get("entry_id")): row.get("sequence_holdout_partition")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }
    row_structure_by_entry = {
        str(row.get("entry_id")): row.get("selected_structure_key")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }

    available_staged_structures = _staged_foldseek_structures(structures)
    coordinate_cap = (
        max(0, int(max_staged_coordinates))
        if max_staged_coordinates is not None
        else None
    )
    staged_structures = (
        available_staged_structures[:coordinate_cap]
        if coordinate_cap is not None and coordinate_cap > 0
        else available_staged_structures
    )
    cap_applied = bool(
        coordinate_cap is not None
        and coordinate_cap > 0
        and len(available_staged_structures) > coordinate_cap
    )
    alias_to_structure, alias_collisions = _foldseek_name_aliases(staged_structures)
    coordinate_dirs = sorted(
        {
            str(Path(str(structure["coordinate_path"])).parent)
            for structure in staged_structures
            if structure.get("coordinate_path")
        }
    )
    coordinate_dir = (
        str(Path(coordinate_dirs[0]).resolve()) if len(coordinate_dirs) == 1 else None
    )
    foldseek_info = _foldseek_binary_info(foldseek_binary)
    requested_slice_id = str(slice_id or metadata_in.get("slice_id") or "")
    command: list[str] | None = None
    command_string: str | None = None
    pair_rows: list[dict[str, Any]] = []
    pair_summary: dict[str, Any] | None = None
    run_status = "not_run"
    run_error: str | None = None

    if not foldseek_info["available"]:
        run_status = "foldseek_unavailable"
    elif len(staged_structures) < 2:
        run_status = "insufficient_staged_coordinates"
    elif coordinate_dir is None:
        run_status = "staged_coordinates_span_multiple_directories"
    else:
        digest = _coordinate_paths_digest(staged_structures)
        workdir = Path("/private/tmp") / (
            f"catalytic-earth-foldseek-tm-{requested_slice_id or 'slice'}-{digest}"
        )
        if workdir.exists():
            shutil.rmtree(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        search_coordinate_dir = Path(coordinate_dir)
        if cap_applied:
            search_coordinate_dir = workdir / "selected_coordinates"
            search_coordinate_dir.mkdir(parents=True, exist_ok=True)
            for structure in staged_structures:
                source_path = Path(str(structure["coordinate_path"]))
                target_path = search_coordinate_dir / source_path.name
                try:
                    target_path.symlink_to(source_path.resolve())
                except OSError:
                    shutil.copy2(source_path, target_path)
        result_tsv = workdir / "staged_tm_scores.tsv"
        tmpdir = workdir / "tmp"
        command = [
            str(foldseek_info["resolved"] or foldseek_binary),
            "easy-search",
            str(search_coordinate_dir),
            str(search_coordinate_dir),
            str(result_tsv),
            str(tmpdir),
            "--format-output",
            "query,target,qtmscore,ttmscore,alntmscore",
            "--exhaustive-search",
            "1",
            "--alignment-type",
            "1",
            "--tmalign-fast",
            "0",
            "--exact-tmscore",
            "1",
            "--threads",
            str(max(1, int(threads))),
            "-v",
            "1",
        ]
        command_string = _command_string(command)
        try:
            if runner is None:
                _run_backend_command(command, cwd=workdir)
            else:
                runner(command, workdir)
            if keep_all_rows:
                pair_rows = _parse_foldseek_tm_score_rows(
                    result_tsv=result_tsv,
                    alias_to_structure=alias_to_structure,
                    row_partitions_by_entry=row_partitions_by_entry,
                )
            else:
                pair_rows, pair_summary = _summarize_foldseek_tm_score_rows(
                    result_tsv=result_tsv,
                    alias_to_structure=alias_to_structure,
                    row_partitions_by_entry=row_partitions_by_entry,
                    threshold=tm_score_threshold,
                    max_reported_rows=max_reported_rows,
                )
            run_status = "completed"
        except (OSError, RuntimeError, ValueError) as exc:
            run_status = "foldseek_run_failed"
            run_error = f"{type(exc).__name__}: {exc}"

    if pair_summary is None:
        mapped_pair_count = sum(
            1
            for row in pair_rows
            if row.get("query_structure_key") and row.get("target_structure_key")
        )
        train_test_rows = [row for row in pair_rows if row.get("train_test_pair")]
        partition_pair_counts = _foldseek_partition_pair_counts(pair_rows)
        max_train_test_tm_score = None
        for row in train_test_rows:
            score = row.get("max_pair_tm_score")
            if score is None:
                continue
            max_train_test_tm_score = (
                float(score)
                if max_train_test_tm_score is None
                else max(max_train_test_tm_score, float(score))
            )
        unmapped_names = sorted(
            {
                str(name)
                for row in pair_rows
                for name, key in (
                    (row.get("raw_query_name"), row.get("query_structure_key")),
                    (row.get("raw_target_name"), row.get("target_structure_key")),
                )
                if name and not key
            }
        )
        pair_count = len(pair_rows)
        train_test_pair_count = len(train_test_rows)
        unique_unordered_nonself_pair_count = _unique_unordered_nonself_pair_count(
            pair_rows
        )
        target_violating_pair_count = sum(
            1
            for row in train_test_rows
            if (_parse_optional_float(row.get("max_pair_tm_score")) or 0.0)
            >= float(tm_score_threshold)
        )
    else:
        mapped_pair_count = int(pair_summary["mapped_pair_count"])
        train_test_rows = [row for row in pair_rows if row.get("train_test_pair")]
        partition_pair_counts = {
            "heldout_in_distribution_pair_count": int(
                pair_summary["heldout_in_distribution_pair_count"]
            ),
            "heldout_pair_count": int(pair_summary["heldout_pair_count"]),
            "in_distribution_pair_count": int(pair_summary["in_distribution_pair_count"]),
            "other_partition_pair_count": int(pair_summary["other_partition_pair_count"]),
        }
        max_train_test_tm_score = pair_summary.get("max_train_test_tm_score")
        unmapped_names = list(pair_summary.get("unmapped_names", []))
        pair_count = int(pair_summary["pair_count"])
        train_test_pair_count = int(pair_summary["train_test_pair_count"])
        unique_unordered_nonself_pair_count = int(
            pair_summary["unique_unordered_nonself_pair_count"]
        )
        target_violating_pair_count = int(
            pair_summary["target_violating_train_test_pair_row_count"]
        )
    selected_structure_count = int(
        metadata_in.get("selected_structure_count", len(structures)) or 0
    )
    evaluated_count = int(metadata_in.get("evaluated_count", len(rows)) or 0)
    materialization_possible_count = int(
        metadata_in.get("coordinate_materialization_possible_count", 0) or 0
    )
    materialized_coordinate_count = int(
        metadata_in.get(
            "materialized_coordinate_count", len(available_staged_structures)
        )
        or 0
    )
    missing_or_unsupported_structure_count = int(
        metadata_in.get("missing_or_unsupported_structure_count", 0) or 0
    )
    fetch_failure_count = int(metadata_in.get("fetch_failure_count", 0) or 0)
    not_materialized_structure_count = int(
        metadata_in.get("not_materialized_structure_count", 0) or 0
    )
    all_materializable_coordinate_coverage = (
        bool(staged_structures)
        and selected_structure_count == len(staged_structures)
        and fetch_failure_count == 0
        and not_materialized_structure_count == 0
        and not cap_applied
    )
    full_evaluated_coordinate_coverage = (
        all_materializable_coordinate_coverage
        and missing_or_unsupported_structure_count == 0
    )
    partial_signal = run_status == "completed" and bool(pair_rows)
    computed_tm_target_achieved = (
        max_train_test_tm_score is not None
        and max_train_test_tm_score < float(tm_score_threshold)
    )
    prior_coordinate_count = (
        max(0, int(prior_staged_coordinate_count))
        if prior_staged_coordinate_count is not None
        else None
    )
    staged_exceeds_prior = bool(
        partial_signal
        and prior_coordinate_count is not None
        and len(staged_structures) > prior_coordinate_count
    )
    remaining_to_full_signal_structure_count = max(
        0, selected_structure_count - len(staged_structures)
    )
    remaining_uncomputed_staged_coordinate_count = max(
        0, len(available_staged_structures) - len(staged_structures)
    )
    if full_evaluated_coordinate_coverage:
        coverage_status = "full_evaluated_coordinate_signal"
    elif all_materializable_coordinate_coverage:
        coverage_status = (
            "full_materializable_coordinate_signal_with_exclusions"
            if missing_or_unsupported_structure_count
            else "full_materializable_coordinate_signal"
        )
    else:
        coverage_status = "partial_staged_coordinate_signal"
    full_claim_blockers = [
        "this builder emits a TM-score signal, not a tested full TM-score split"
    ]
    if not partial_signal:
        full_claim_blockers.append("Foldseek TM-score signal did not complete with pair rows")
    if not full_evaluated_coordinate_coverage:
        full_claim_blockers.append("evaluated selected-coordinate coverage is partial")
    if missing_or_unsupported_structure_count:
        full_claim_blockers.append("one or more evaluated rows lacks a supported selected structure")
    if fetch_failure_count:
        full_claim_blockers.append("one or more selected coordinate fetches failed")
    if remaining_to_full_signal_structure_count:
        full_claim_blockers.append("selected structures remain outside the computed signal")
    if remaining_uncomputed_staged_coordinate_count:
        full_claim_blockers.append("available staged coordinates were excluded by the signal cap")
    if not computed_tm_target_achieved:
        full_claim_blockers.append(
            f"computed train/test TM-score target <{float(tm_score_threshold):.1f} is not achieved"
        )
    blockers_remaining = sorted(set(full_claim_blockers))
    limitations = [
        "partial staged-coordinate Foldseek signal only; it is not a full accepted-registry TM-score holdout",
        "tm_score_split_computed=false because no canonical full TM-score split is emitted here",
        "review-only artifact; it creates no countable labels and no import-ready rows",
        "Foldseek output names are mapped by exact filename/basename/stem/structure-metadata aliases or by an unambiguous generated PDB stem plus chain suffix; other differing raw names remain unmapped",
    ]
    if alias_collisions:
        limitations.append("one or more coordinate filename aliases were ambiguous and not used for raw-name mapping")
    if unmapped_names:
        limitations.append("one or more Foldseek raw query/target names could not be mapped safely to staged structures")
    if run_error:
        limitations.append("Foldseek easy-search did not complete; pairwise TM-score rows are unavailable")
    if not full_evaluated_coordinate_coverage:
        limitations.append("full evaluated-coordinate coverage is absent; full TM-score split remains blocked")
    if all_materializable_coordinate_coverage and missing_or_unsupported_structure_count:
        limitations.append(
            "all currently materializable selected coordinates were searched, but excluded rows without selected structures still block a full evaluated-coordinate claim"
        )
    if cap_applied:
        limitations.append("computed TM-score signal was capped below the available staged coordinate count")
    if max_train_test_tm_score is None:
        limitations.append("no mapped heldout/in_distribution pair was available to evaluate the <0.7 target")

    selected_staged_entry_ids = sorted(
        {
            str(entry_id)
            for structure in staged_structures
            for entry_id in structure.get("entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    computed_subset_structure_coverage = _safe_ratio(
        len(staged_structures), selected_structure_count
    )
    computed_subset_materialized_coverage = _safe_ratio(
        len(staged_structures), materialized_coordinate_count
    )
    computed_subset_evaluated_entry_coverage = _safe_ratio(
        len(selected_staged_entry_ids), evaluated_count
    )
    expanded_successful_signal = partial_signal and (
        len(staged_structures) > 25 or cap_applied
    )
    if partial_signal and all_materializable_coordinate_coverage:
        blocker_removed = (
            "removes the remaining staged-coordinate signal cap by running "
            f"Foldseek easy-search over all {len(staged_structures)} currently "
            "materializable selected coordinates; this remains review-only and "
            "non-countable"
        )
    elif staged_exceeds_prior:
        blocker_removed = (
            f"removes the previous expanded{prior_coordinate_count} partial-signal "
            f"ceiling by running Foldseek easy-search over {len(staged_structures)} "
            "staged coordinates; this remains review-only and non-countable"
        )
    elif expanded_successful_signal:
        blocker_removed = (
            "removes the staged25-only proof blocker when staged_coordinate_count "
            "exceeds 25 by running Foldseek easy-search over the expanded bounded "
            "coordinate subset; this remains review-only and non-countable"
        )
    else:
        blocker_removed = None

    metadata = {
        "method": "foldseek_tm_score_signal",
        "blocker_removed": blocker_removed,
        "blocker_not_removed": (
            "expanded Foldseek TM-score signal did not complete with pair rows; "
            "staged25-only computed signal remains the latest usable TM-score signal"
            if not expanded_successful_signal and len(staged_structures) > 25
            else None
        ),
        "blocker_narrowed": (
            "Foldseek TM-score signal computed for the coordinate sidecar; full "
            "evaluated-coordinate TM-score split remains blocked until excluded "
            "evaluated rows are resolved and a canonical split artifact is emitted"
        ),
        "slice_id": requested_slice_id,
        "readiness_artifact": readiness_path,
        "readiness_method": metadata_in.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "tm_score_split_computed": False,
        "full_tm_score_split_computed": False,
        "partial_tm_score_signal_computed": partial_signal,
        "partial_tm_score_signal_scope": "staged_coordinates_only",
        "real_tm_score_computed": False,
        "partial_real_tm_score_signal_computed": partial_signal,
        "all_materializable_coordinate_signal_computed": bool(
            partial_signal and all_materializable_coordinate_coverage
        ),
        "full_evaluated_coordinate_coverage": full_evaluated_coordinate_coverage,
        "all_materializable_coordinate_coverage": all_materializable_coordinate_coverage,
        "tm_score_signal_coverage_status": coverage_status,
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(full_claim_blockers)),
        "blockers_remaining": blockers_remaining,
        "threshold_target": f"<{float(tm_score_threshold):.1f}",
        "tm_score_threshold_target": f"<{float(tm_score_threshold):.1f}",
        "tm_score_target_achieved_for_computed_subset": computed_tm_target_achieved,
        "tm_score_target_evaluation_scope": "mapped heldout/in_distribution pairs in computed staged-coordinate subset only",
        "evaluated_count": evaluated_count,
        "selected_structure_count": selected_structure_count,
        "coordinate_materialization_possible_count": materialization_possible_count,
        "coordinate_fetch_cap": metadata_in.get("coordinate_fetch_cap"),
        "materialized_coordinate_count": materialized_coordinate_count,
        "available_staged_coordinate_count": len(available_staged_structures),
        "missing_or_unsupported_structure_count": missing_or_unsupported_structure_count,
        "missing_or_unsupported_structures": metadata_in.get(
            "missing_or_unsupported_structures", []
        ),
        "fetch_failure_count": fetch_failure_count,
        "fetch_failures": metadata_in.get("fetch_failures", []),
        "not_materialized_structure_count": not_materialized_structure_count,
        "not_materialized_structures": metadata_in.get("not_materialized_structures", []),
        "tm_signal_coordinate_cap_requested": coordinate_cap,
        "tm_signal_coordinate_cap_applied": cap_applied,
        "prior_staged_coordinate_count": prior_coordinate_count,
        "staged_coordinate_count_exceeds_prior": staged_exceeds_prior,
        "staged_coordinate_count": len(staged_structures),
        "staged_structure_count": len(staged_structures),
        "staged_entry_count": len(selected_staged_entry_ids),
        "selected_staged_entry_ids": selected_staged_entry_ids,
        "remaining_to_full_signal_structure_count": remaining_to_full_signal_structure_count,
        "remaining_uncomputed_staged_coordinate_count": remaining_uncomputed_staged_coordinate_count,
        "remaining_unstaged_supported_structure_count": not_materialized_structure_count,
        "computed_subset_structure_coverage": computed_subset_structure_coverage,
        "computed_subset_materialized_coverage": computed_subset_materialized_coverage,
        "computed_subset_evaluated_entry_coverage": computed_subset_evaluated_entry_coverage,
        "coordinate_directory": coordinate_dir,
        "coordinate_directories": coordinate_dirs,
        "pair_count": pair_count,
        "mapped_pair_count": mapped_pair_count,
        "train_test_pair_count": train_test_pair_count,
        "heldout_in_distribution_pair_count": partition_pair_counts[
            "heldout_in_distribution_pair_count"
        ],
        "heldout_pair_count": partition_pair_counts["heldout_pair_count"],
        "in_distribution_pair_count": partition_pair_counts[
            "in_distribution_pair_count"
        ],
        "other_partition_pair_count": partition_pair_counts["other_partition_pair_count"],
        "unique_unordered_nonself_pair_count": unique_unordered_nonself_pair_count,
        "target_violating_train_test_pair_row_count": target_violating_pair_count,
        "max_observed_train_test_tm_score": (
            round(max_train_test_tm_score, 4)
            if max_train_test_tm_score is not None
            else None
        ),
        "max_observed_train_test_tm_score_computable": max_train_test_tm_score is not None,
        "max_observed_train_test_tm_score_metric": (
            "max(qtmscore, ttmscore, alntmscore) across mapped heldout/in_distribution staged-coordinate pairs"
        ),
        "foldseek_binary_requested": foldseek_info["requested"],
        "foldseek_binary_resolved": foldseek_info["resolved"],
        "foldseek_binary_available": foldseek_info["available"],
        "foldseek_version": foldseek_info["version"],
        "foldseek_version_command": foldseek_info["version_command"],
        "foldseek_command": command_string,
        "foldseek_commands": [item for item in [foldseek_info["version_command"], command_string] if item],
        "foldseek_run_status": run_status,
        "foldseek_run_error": run_error,
        "foldseek_threads": max(1, int(threads)),
        "pair_rows_retained_policy": (
            "all_rows" if keep_all_rows else "summary_top_train_test_and_target_violations"
        ),
        "reported_pair_row_count": len(pair_rows),
        "omitted_pair_row_count": max(0, pair_count - len(pair_rows)),
        "max_reported_pair_rows": max(0, int(max_reported_rows)),
        "raw_name_mapping_unmapped_count": len(unmapped_names),
        "raw_name_mapping_unmapped_names": unmapped_names,
        "raw_name_mapping_alias_collision_count": len(alias_collisions),
        "raw_name_mapping_alias_collisions": alias_collisions,
        "limitations": sorted(set(limitations)),
    }

    return {
        "metadata": metadata,
        "staged_structures": [
            {
                **{
                    key: structure.get(key)
                    for key in (
                        "structure_key",
                        "source",
                        "structure_id",
                        "coordinate_path",
                        "fetch_status",
                    )
                },
                "entry_ids": sorted(
                    [str(entry_id) for entry_id in structure.get("entry_ids", [])],
                    key=_entry_id_sort_key,
                ),
                "entry_partitions": {
                    str(entry_id): row_partitions_by_entry.get(str(entry_id))
                    for entry_id in structure.get("entry_ids", [])
                },
            }
            for structure in staged_structures
        ],
        "rows": sorted(
            [
                {
                    **row,
                    "query_entry_structure_keys": {
                        entry_id: row_structure_by_entry.get(entry_id)
                        for entry_id in row.get("query_entry_ids", [])
                    },
                    "target_entry_structure_keys": {
                        entry_id: row_structure_by_entry.get(entry_id)
                        for entry_id in row.get("target_entry_ids", [])
                    },
                    "countable_label_candidate": False,
                    "import_ready": False,
                    "review_status": "review_only_non_countable",
                }
                for row in pair_rows
            ],
            key=lambda row: (
                str(row.get("raw_query_name") or ""),
                str(row.get("raw_target_name") or ""),
            ),
        ),
    }


def build_foldseek_tm_score_all_materializable_signal(
    *,
    readiness: dict[str, Any],
    slice_id: str | None = None,
    foldseek_binary: str = "/private/tmp/catalytic-foldseek-env/bin/foldseek",
    readiness_path: str | None = None,
    max_runtime_seconds: int | None = None,
    threads: int = 1,
    threshold: float = 0.7,
    max_reported_pairs: int = 20,
    runner: Callable[[list[str], Path], None] | None = None,
) -> dict[str, Any]:
    """Run a compact Foldseek TM-score summary over every staged coordinate.

    Unlike ``build_foldseek_tm_score_signal``, this path is intended for the
    all-materializable sidecar and does not emit every pair row into JSON. It
    keeps the full-run provenance and split summary small enough to commit.
    """

    metadata_in = readiness.get("metadata", {}) if isinstance(readiness, dict) else {}
    if not isinstance(metadata_in, dict):
        metadata_in = {}
    rows_in = readiness.get("rows", []) if isinstance(readiness, dict) else []
    structures_in = readiness.get("structures", []) if isinstance(readiness, dict) else []
    rows = [row for row in rows_in if isinstance(row, dict)]
    structures = [item for item in structures_in if isinstance(item, dict)]

    row_partitions_by_entry = {
        str(row.get("entry_id")): row.get("sequence_holdout_partition")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }
    row_structure_by_entry = {
        str(row.get("entry_id")): row.get("selected_structure_key")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }

    staged_structures = _staged_foldseek_structures(structures)
    alias_to_structure, alias_collisions = _foldseek_name_aliases(staged_structures)
    coordinate_dirs = sorted(
        {
            str(Path(str(structure["coordinate_path"])).parent)
            for structure in staged_structures
            if structure.get("coordinate_path")
        }
    )
    coordinate_dir = (
        str(Path(coordinate_dirs[0]).resolve()) if len(coordinate_dirs) == 1 else None
    )
    foldseek_info = _foldseek_binary_info(foldseek_binary)
    requested_slice_id = str(slice_id or metadata_in.get("slice_id") or "")
    command: list[str] | None = None
    command_string: str | None = None
    result_tsv: Path | None = None
    run_status = "not_run"
    run_error: str | None = None
    pair_summary = _empty_foldseek_tm_score_pair_summary()

    if not foldseek_info["available"]:
        run_status = "foldseek_unavailable"
    elif len(staged_structures) < 2:
        run_status = "insufficient_staged_coordinates"
    elif coordinate_dir is None:
        run_status = "staged_coordinates_span_multiple_directories"
    else:
        digest = _coordinate_paths_digest(staged_structures)
        workdir = Path("/private/tmp") / (
            f"catalytic-earth-foldseek-tm-all-{requested_slice_id or 'slice'}-{digest}"
        )
        if workdir.exists():
            shutil.rmtree(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        result_tsv = workdir / "all_materializable_tm_scores.tsv"
        tmpdir = workdir / "tmp"
        command = [
            str(foldseek_info["resolved"] or foldseek_binary),
            "easy-search",
            str(Path(coordinate_dir)),
            str(Path(coordinate_dir)),
            str(result_tsv),
            str(tmpdir),
            "--format-output",
            "query,target,qtmscore,ttmscore,alntmscore",
            "--exhaustive-search",
            "1",
            "--alignment-type",
            "1",
            "--tmalign-fast",
            "0",
            "--exact-tmscore",
            "1",
            "--threads",
            str(max(1, int(threads))),
            "-v",
            "1",
        ]
        command_string = _command_string(command)
        try:
            if runner is None:
                _run_backend_command(command, cwd=workdir, timeout=max_runtime_seconds)
            else:
                runner(command, workdir)
            pair_summary = _summarize_foldseek_tm_score_tsv(
                result_tsv=result_tsv,
                alias_to_structure=alias_to_structure,
                row_partitions_by_entry=row_partitions_by_entry,
                threshold=threshold,
                max_reported_pairs=max_reported_pairs,
            )
            run_status = "completed"
        except TimeoutError as exc:
            run_status = "foldseek_run_timeout"
            run_error = f"{type(exc).__name__}: {exc}"
        except (OSError, RuntimeError, ValueError) as exc:
            run_status = "foldseek_run_failed"
            run_error = f"{type(exc).__name__}: {exc}"

    selected_structure_count = int(
        metadata_in.get("selected_structure_count", len(structures)) or 0
    )
    evaluated_count = int(metadata_in.get("evaluated_count", len(rows)) or 0)
    materialization_possible_count = int(
        metadata_in.get("coordinate_materialization_possible_count", 0) or 0
    )
    materialized_coordinate_count = int(
        metadata_in.get("materialized_coordinate_count", len(staged_structures)) or 0
    )
    missing_or_unsupported_structure_count = int(
        metadata_in.get("missing_or_unsupported_structure_count", 0) or 0
    )
    fetch_failure_count = int(metadata_in.get("fetch_failure_count", 0) or 0)
    not_materialized_structure_count = int(
        metadata_in.get("not_materialized_structure_count", 0) or 0
    )
    all_materializable_coordinate_coverage = (
        bool(staged_structures)
        and len(staged_structures) == materialized_coordinate_count
        and not_materialized_structure_count == 0
        and fetch_failure_count == 0
    )
    full_evaluated_coordinate_coverage = (
        all_materializable_coordinate_coverage
        and selected_structure_count == len(staged_structures)
        and missing_or_unsupported_structure_count == 0
    )
    summary_completed = run_status == "completed" and pair_summary["pair_count"] > 0
    max_train_test_tm_score = pair_summary["max_observed_train_test_tm_score"]
    target_achieved = (
        max_train_test_tm_score is not None and max_train_test_tm_score < threshold
    )
    selected_staged_entry_ids = sorted(
        {
            str(entry_id)
            for structure in staged_structures
            for entry_id in structure.get("entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    coordinate_exclusions = metadata_in.get("missing_or_unsupported_structures", [])
    full_claim_blockers = [
        "review-only all-materializable TM-score signal is not a canonical full holdout claim"
    ]
    if not summary_completed:
        full_claim_blockers.append("Foldseek all-materializable signal did not complete with pair rows")
    if not full_evaluated_coordinate_coverage:
        full_claim_blockers.append("evaluated selected-coordinate coverage is partial")
    if missing_or_unsupported_structure_count:
        full_claim_blockers.append("one or more evaluated rows lacks a supported selected structure")
    if fetch_failure_count:
        full_claim_blockers.append("one or more selected coordinate fetches failed")
    if not_materialized_structure_count:
        full_claim_blockers.append("one or more materializable selected structures remain unstaged")
    if not target_achieved:
        full_claim_blockers.append("computed train/test TM-score target <0.7 is not achieved")
    limitations = [
        "review-only artifact; it creates no countable labels and no import-ready rows",
        "compact summary artifact; per-pair Foldseek rows are not emitted into repository JSON",
        "full_tm_score_holdout_claim_permitted=false until coordinate exclusions and canonical split policy are resolved",
    ]
    if metadata_in.get("sequence_holdout_artifact"):
        limitations.append(
            "sequence-holdout partition provenance is inherited from the readiness artifact"
        )
    if coordinate_exclusions:
        limitations.append("selected rows with no supported coordinate structures remain excluded from TM-score computation")
    if alias_collisions:
        limitations.append("one or more coordinate filename aliases were ambiguous and not used for raw-name mapping")
    if pair_summary["raw_name_mapping_unmapped_count"]:
        limitations.append("one or more Foldseek raw query/target names could not be mapped safely to staged structures")
    if run_error:
        limitations.append("Foldseek easy-search did not complete; all-materializable pairwise TM-score rows are unavailable")

    metadata = {
        "method": "foldseek_tm_score_all_materializable_signal",
        "blocker_removed": (
            "removes the capped-signal blocker by running Foldseek easy-search over all staged materializable coordinates"
            if summary_completed and all_materializable_coordinate_coverage
            else None
        ),
        "blocker_not_removed": (
            "all-materializable Foldseek TM-score signal did not complete"
            if not summary_completed
            else None
        ),
        "slice_id": requested_slice_id,
        "readiness_artifact": readiness_path,
        "readiness_method": metadata_in.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "tm_score_split_computed": summary_completed,
        "all_materializable_tm_score_signal_computed": summary_completed,
        "all_materializable_tm_score_split_computed": summary_completed,
        "full_tm_score_split_computed": False,
        "real_tm_score_computed": summary_completed,
        "full_evaluated_coordinate_coverage": full_evaluated_coordinate_coverage,
        "all_materializable_coordinate_coverage": all_materializable_coordinate_coverage,
        "tm_score_signal_coverage_status": (
            "all_materializable_coordinate_signal"
            if all_materializable_coordinate_coverage
            else "partial_materializable_coordinate_signal"
        ),
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(full_claim_blockers)),
        "blockers_remaining": sorted(set(full_claim_blockers)),
        "threshold_target": "<0.7",
        "tm_score_threshold": float(threshold),
        "tm_score_threshold_target": "<0.7",
        "tm_score_target_operator": "<",
        "tm_score_target_achieved": target_achieved,
        "tm_score_target_achieved_for_all_materializable_signal": target_achieved,
        "tm_score_target_evaluation_scope": (
            "mapped heldout/in_distribution pairs across every staged materializable selected coordinate"
        ),
        "evaluated_count": evaluated_count,
        "selected_structure_count": selected_structure_count,
        "coordinate_materialization_possible_count": materialization_possible_count,
        "coordinate_fetch_cap": metadata_in.get("coordinate_fetch_cap"),
        "materialized_coordinate_count": materialized_coordinate_count,
        "available_staged_coordinate_count": len(staged_structures),
        "staged_coordinate_count": len(staged_structures),
        "staged_structure_count": len(staged_structures),
        "staged_entry_count": len(selected_staged_entry_ids),
        "selected_staged_entry_ids": selected_staged_entry_ids,
        "missing_or_unsupported_structure_count": missing_or_unsupported_structure_count,
        "missing_or_unsupported_structures": coordinate_exclusions,
        "tm_score_coordinate_exclusion_count": missing_or_unsupported_structure_count,
        "tm_score_coordinate_exclusions": coordinate_exclusions,
        "fetch_failure_count": fetch_failure_count,
        "fetch_failures": metadata_in.get("fetch_failures", []),
        "not_materialized_structure_count": not_materialized_structure_count,
        "not_materialized_structures": metadata_in.get("not_materialized_structures", []),
        "remaining_uncomputed_staged_coordinate_count": 0 if summary_completed else len(staged_structures),
        "remaining_unstaged_supported_structure_count": not_materialized_structure_count,
        "computed_subset_structure_coverage": _safe_ratio(
            len(staged_structures), selected_structure_count
        ),
        "computed_subset_materialized_coverage": _safe_ratio(
            len(staged_structures), materialized_coordinate_count
        ),
        "computed_subset_evaluated_entry_coverage": _safe_ratio(
            len(selected_staged_entry_ids), evaluated_count
        ),
        "coordinate_directory": coordinate_dir,
        "coordinate_directories": coordinate_dirs,
        "foldseek_binary_requested": foldseek_info["requested"],
        "foldseek_binary_resolved": foldseek_info["resolved"],
        "foldseek_binary_available": foldseek_info["available"],
        "foldseek_version": foldseek_info["version"],
        "foldseek_version_command": foldseek_info["version_command"],
        "foldseek_command": command_string,
        "foldseek_commands": [item for item in [foldseek_info["version_command"], command_string] if item],
        "foldseek_run_status": run_status,
        "foldseek_run_error": run_error,
        "foldseek_max_runtime_seconds": max_runtime_seconds,
        "foldseek_threads": max(1, int(threads)),
        "foldseek_result_tsv_path": str(result_tsv) if result_tsv else None,
        "foldseek_result_tsv_size_bytes": (
            result_tsv.stat().st_size if result_tsv and result_tsv.exists() else None
        ),
        "raw_name_mapping_alias_collision_count": len(alias_collisions),
        "raw_name_mapping_alias_collisions": alias_collisions,
        "limitations": sorted(set(limitations)),
        **pair_summary,
    }

    return {
        "metadata": metadata,
        "staged_structures": [
            {
                **{
                    key: structure.get(key)
                    for key in (
                        "structure_key",
                        "source",
                        "structure_id",
                        "coordinate_path",
                        "fetch_status",
                    )
                },
                "entry_ids": sorted(
                    [str(entry_id) for entry_id in structure.get("entry_ids", [])],
                    key=_entry_id_sort_key,
                ),
                "entry_partitions": {
                    str(entry_id): row_partitions_by_entry.get(str(entry_id))
                    for entry_id in structure.get("entry_ids", [])
                },
                "entry_structure_keys": {
                    str(entry_id): row_structure_by_entry.get(str(entry_id))
                    for entry_id in structure.get("entry_ids", [])
                },
            }
            for structure in staged_structures
        ],
        "top_train_test_pairs": pair_summary["top_train_test_pairs"],
        "blocking_pairs": pair_summary["blocking_pairs"],
    }


def build_foldseek_tm_score_query_chunk_signal(
    *,
    readiness: dict[str, Any],
    slice_id: str | None = None,
    foldseek_binary: str = "/private/tmp/catalytic-foldseek-env/bin/foldseek",
    readiness_path: str | None = None,
    chunk_index: int = 0,
    chunk_size: int = 12,
    max_runtime_seconds: int | None = None,
    threads: int = 1,
    threshold: float = 0.7,
    max_reported_pairs: int = 20,
    runner: Callable[[list[str], Path], None] | None = None,
) -> dict[str, Any]:
    """Run one resumable Foldseek query chunk against all staged coordinates.

    The 672-coordinate all-vs-all exact TM-score run can exceed the automation
    window. This path keeps target coverage broad while bounding each run by a
    deterministic query slice that can later be aggregated without false full
    holdout claims.
    """

    metadata_in = readiness.get("metadata", {}) if isinstance(readiness, dict) else {}
    if not isinstance(metadata_in, dict):
        metadata_in = {}
    rows_in = readiness.get("rows", []) if isinstance(readiness, dict) else []
    structures_in = readiness.get("structures", []) if isinstance(readiness, dict) else []
    rows = [row for row in rows_in if isinstance(row, dict)]
    structures = [item for item in structures_in if isinstance(item, dict)]

    row_partitions_by_entry = {
        str(row.get("entry_id")): row.get("sequence_holdout_partition")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }
    row_structure_by_entry = {
        str(row.get("entry_id")): row.get("selected_structure_key")
        for row in rows
        if isinstance(row.get("entry_id"), str)
    }

    staged_structures = _staged_foldseek_structures(structures)
    total_staged = len(staged_structures)
    chunk_size_value = max(1, int(chunk_size))
    chunk_index_value = max(0, int(chunk_index))
    query_chunk_count = (
        (total_staged + chunk_size_value - 1) // chunk_size_value
        if total_staged
        else 0
    )
    if query_chunk_count and chunk_index_value >= query_chunk_count:
        raise ValueError(
            f"chunk_index {chunk_index_value} is outside {query_chunk_count} chunks"
        )
    chunk_start = chunk_index_value * chunk_size_value
    chunk_end = min(chunk_start + chunk_size_value, total_staged)
    query_structures = staged_structures[chunk_start:chunk_end]

    alias_to_structure, alias_collisions = _foldseek_name_aliases(staged_structures)
    coordinate_dirs = sorted(
        {
            str(Path(str(structure["coordinate_path"])).parent)
            for structure in staged_structures
            if structure.get("coordinate_path")
        }
    )
    coordinate_dir = (
        str(Path(coordinate_dirs[0]).resolve()) if len(coordinate_dirs) == 1 else None
    )
    foldseek_info = _foldseek_binary_info(foldseek_binary)
    requested_slice_id = str(slice_id or metadata_in.get("slice_id") or "")
    command: list[str] | None = None
    command_string: str | None = None
    result_tsv: Path | None = None
    query_coordinate_dir: Path | None = None
    run_status = "not_run"
    run_error: str | None = None
    pair_summary = _empty_foldseek_tm_score_pair_summary()

    if not foldseek_info["available"]:
        run_status = "foldseek_unavailable"
    elif len(staged_structures) < 2 or not query_structures:
        run_status = "insufficient_staged_coordinates"
    elif coordinate_dir is None:
        run_status = "staged_coordinates_span_multiple_directories"
    else:
        digest = _coordinate_paths_digest(staged_structures)
        workdir = Path("/private/tmp") / (
            "catalytic-earth-foldseek-tm-query-chunk-"
            f"{requested_slice_id or 'slice'}-{chunk_index_value:04d}-{digest}"
        )
        if workdir.exists():
            shutil.rmtree(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        query_coordinate_dir = workdir / "query_coordinates"
        query_coordinate_dir.mkdir(parents=True, exist_ok=True)
        for structure in query_structures:
            source_path = Path(str(structure["coordinate_path"]))
            target_path = query_coordinate_dir / source_path.name
            try:
                target_path.symlink_to(source_path.resolve())
            except OSError:
                shutil.copy2(source_path, target_path)
        result_tsv = workdir / f"query_chunk_{chunk_index_value:04d}_tm_scores.tsv"
        tmpdir = workdir / "tmp"
        command = [
            str(foldseek_info["resolved"] or foldseek_binary),
            "easy-search",
            str(query_coordinate_dir),
            str(Path(coordinate_dir)),
            str(result_tsv),
            str(tmpdir),
            "--format-output",
            "query,target,qtmscore,ttmscore,alntmscore",
            "--exhaustive-search",
            "1",
            "--alignment-type",
            "1",
            "--tmalign-fast",
            "0",
            "--exact-tmscore",
            "1",
            "--threads",
            str(max(1, int(threads))),
            "-v",
            "1",
        ]
        command_string = _command_string(command)
        try:
            if runner is None:
                _run_backend_command(command, cwd=workdir, timeout=max_runtime_seconds)
            else:
                runner(command, workdir)
            pair_summary = _summarize_foldseek_tm_score_tsv(
                result_tsv=result_tsv,
                alias_to_structure=alias_to_structure,
                row_partitions_by_entry=row_partitions_by_entry,
                threshold=threshold,
                max_reported_pairs=max_reported_pairs,
            )
            run_status = "completed"
        except TimeoutError as exc:
            run_status = "foldseek_run_timeout"
            run_error = f"{type(exc).__name__}: {exc}"
        except (OSError, RuntimeError, ValueError) as exc:
            run_status = "foldseek_run_failed"
            run_error = f"{type(exc).__name__}: {exc}"

    selected_structure_count = int(
        metadata_in.get("selected_structure_count", len(structures)) or 0
    )
    evaluated_count = int(metadata_in.get("evaluated_count", len(rows)) or 0)
    materialization_possible_count = int(
        metadata_in.get("coordinate_materialization_possible_count", 0) or 0
    )
    materialized_coordinate_count = int(
        metadata_in.get("materialized_coordinate_count", total_staged) or 0
    )
    missing_or_unsupported_structure_count = int(
        metadata_in.get("missing_or_unsupported_structure_count", 0) or 0
    )
    fetch_failure_count = int(metadata_in.get("fetch_failure_count", 0) or 0)
    not_materialized_structure_count = int(
        metadata_in.get("not_materialized_structure_count", 0) or 0
    )
    all_materializable_coordinate_coverage = (
        bool(staged_structures)
        and total_staged == materialized_coordinate_count
        and not_materialized_structure_count == 0
        and fetch_failure_count == 0
    )
    full_evaluated_coordinate_coverage = (
        all_materializable_coordinate_coverage
        and selected_structure_count == total_staged
        and missing_or_unsupported_structure_count == 0
    )
    summary_completed = run_status == "completed" and pair_summary["pair_count"] > 0
    max_train_test_tm_score = pair_summary["max_observed_train_test_tm_score"]
    target_achieved = (
        max_train_test_tm_score is not None and max_train_test_tm_score < threshold
    )
    query_staged_entry_ids = sorted(
        {
            str(entry_id)
            for structure in query_structures
            for entry_id in structure.get("entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    selected_staged_entry_ids = sorted(
        {
            str(entry_id)
            for structure in staged_structures
            for entry_id in structure.get("entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    coordinate_exclusions = metadata_in.get("missing_or_unsupported_structures", [])
    full_claim_blockers = [
        "review-only query-chunk TM-score signal is not a canonical full holdout claim",
        "all query chunks must complete and aggregate before a full all-materializable signal exists",
    ]
    if len(query_structures) < total_staged:
        full_claim_blockers.append("query chunk covers only part of the all-materializable query set")
    if not summary_completed:
        full_claim_blockers.append("Foldseek query chunk did not complete with pair rows")
    if not full_evaluated_coordinate_coverage:
        full_claim_blockers.append("evaluated selected-coordinate coverage is partial")
    if missing_or_unsupported_structure_count:
        full_claim_blockers.append("one or more evaluated rows lacks a supported selected structure")
    if fetch_failure_count:
        full_claim_blockers.append("one or more selected coordinate fetches failed")
    if not_materialized_structure_count:
        full_claim_blockers.append("one or more materializable selected structures remain unstaged")
    if not target_achieved:
        full_claim_blockers.append("computed query-chunk train/test TM-score target <0.7 is not achieved")

    limitations = [
        "review-only artifact; it creates no countable labels and no import-ready rows",
        "query chunk is resumable Foldseek evidence only; aggregate all chunks before evaluating a full all-materializable TM-score signal",
        "target coordinate coverage is all currently staged materializable coordinates, while query coverage is only this deterministic chunk",
        "full_tm_score_holdout_claim_permitted=false until chunk aggregation, coordinate exclusions, and canonical split policy are resolved",
    ]
    if coordinate_exclusions:
        limitations.append("selected rows with no supported coordinate structures remain excluded from TM-score computation")
    if alias_collisions:
        limitations.append("one or more coordinate filename aliases were ambiguous and not used for raw-name mapping")
    if pair_summary["raw_name_mapping_unmapped_count"]:
        limitations.append("one or more Foldseek raw query/target names could not be mapped safely to staged structures")
    if run_error:
        limitations.append("Foldseek easy-search did not complete for this query chunk")

    remaining_query_count_after_chunk = (
        max(0, total_staged - chunk_end) if summary_completed else total_staged
    )
    metadata = {
        "method": "foldseek_tm_score_query_chunk_signal",
        "blocker_removed": (
            "replaces the single unresumable all-materializable Foldseek timeout with one completed deterministic query chunk against all staged materializable coordinates"
            if summary_completed
            else None
        ),
        "blocker_not_removed": (
            "full all-materializable Foldseek aggregate remains incomplete until every query chunk completes and is aggregated"
        ),
        "slice_id": requested_slice_id,
        "readiness_artifact": readiness_path,
        "readiness_method": metadata_in.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "tm_score_split_computed": False,
        "all_materializable_tm_score_signal_computed": False,
        "all_materializable_query_chunk_signal_computed": summary_completed,
        "all_materializable_tm_score_split_computed": False,
        "full_tm_score_split_computed": False,
        "real_tm_score_computed": summary_completed,
        "full_evaluated_coordinate_coverage": full_evaluated_coordinate_coverage,
        "all_materializable_coordinate_coverage": all_materializable_coordinate_coverage,
        "tm_score_signal_coverage_status": "all_materializable_query_chunk_signal",
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(full_claim_blockers)),
        "blockers_remaining": sorted(set(full_claim_blockers)),
        "threshold_target": "<0.7",
        "tm_score_threshold": float(threshold),
        "tm_score_threshold_target": "<0.7",
        "tm_score_target_operator": "<",
        "tm_score_target_achieved": target_achieved,
        "tm_score_target_achieved_for_query_chunk": target_achieved,
        "tm_score_target_evaluation_scope": (
            "mapped heldout/in_distribution pairs from this query chunk against every staged materializable selected coordinate"
        ),
        "evaluated_count": evaluated_count,
        "selected_structure_count": selected_structure_count,
        "coordinate_materialization_possible_count": materialization_possible_count,
        "coordinate_fetch_cap": metadata_in.get("coordinate_fetch_cap"),
        "materialized_coordinate_count": materialized_coordinate_count,
        "available_staged_coordinate_count": total_staged,
        "target_staged_coordinate_count": total_staged,
        "staged_coordinate_count": total_staged,
        "staged_structure_count": total_staged,
        "query_chunk_index": chunk_index_value,
        "query_chunk_size": chunk_size_value,
        "query_chunk_count": query_chunk_count,
        "query_chunk_start": chunk_start,
        "query_chunk_end_exclusive": chunk_end,
        "query_staged_coordinate_count": len(query_structures),
        "query_staged_structure_count": len(query_structures),
        "query_staged_entry_count": len(query_staged_entry_ids),
        "query_staged_entry_ids": query_staged_entry_ids,
        "selected_staged_entry_ids": selected_staged_entry_ids,
        "missing_or_unsupported_structure_count": missing_or_unsupported_structure_count,
        "missing_or_unsupported_structures": coordinate_exclusions,
        "tm_score_coordinate_exclusion_count": missing_or_unsupported_structure_count,
        "tm_score_coordinate_exclusions": coordinate_exclusions,
        "fetch_failure_count": fetch_failure_count,
        "fetch_failures": metadata_in.get("fetch_failures", []),
        "not_materialized_structure_count": not_materialized_structure_count,
        "not_materialized_structures": metadata_in.get("not_materialized_structures", []),
        "remaining_uncomputed_staged_coordinate_count": remaining_query_count_after_chunk,
        "remaining_uncomputed_query_coordinate_count_after_this_chunk": remaining_query_count_after_chunk,
        "remaining_query_chunk_count_after_this_chunk": (
            max(0, query_chunk_count - chunk_index_value - 1)
            if summary_completed
            else query_chunk_count
        ),
        "remaining_unstaged_supported_structure_count": not_materialized_structure_count,
        "computed_subset_structure_coverage": _safe_ratio(
            len(query_structures), selected_structure_count
        ),
        "computed_subset_materialized_coverage": _safe_ratio(
            len(query_structures), materialized_coordinate_count
        ),
        "computed_subset_evaluated_entry_coverage": _safe_ratio(
            len(query_staged_entry_ids), evaluated_count
        ),
        "coordinate_directory": coordinate_dir,
        "coordinate_directories": coordinate_dirs,
        "query_coordinate_directory": str(query_coordinate_dir) if query_coordinate_dir else None,
        "foldseek_binary_requested": foldseek_info["requested"],
        "foldseek_binary_resolved": foldseek_info["resolved"],
        "foldseek_binary_available": foldseek_info["available"],
        "foldseek_version": foldseek_info["version"],
        "foldseek_version_command": foldseek_info["version_command"],
        "foldseek_command": command_string,
        "foldseek_commands": [item for item in [foldseek_info["version_command"], command_string] if item],
        "foldseek_run_status": run_status,
        "foldseek_run_error": run_error,
        "foldseek_max_runtime_seconds": max_runtime_seconds,
        "foldseek_threads": max(1, int(threads)),
        "foldseek_result_tsv_path": str(result_tsv) if result_tsv else None,
        "foldseek_result_tsv_size_bytes": (
            result_tsv.stat().st_size if result_tsv and result_tsv.exists() else None
        ),
        "raw_name_mapping_alias_collision_count": len(alias_collisions),
        "raw_name_mapping_alias_collisions": alias_collisions,
        "limitations": sorted(set(limitations)),
        **pair_summary,
    }

    return {
        "metadata": metadata,
        "query_staged_structures": [
            {
                **{
                    key: structure.get(key)
                    for key in (
                        "structure_key",
                        "source",
                        "structure_id",
                        "coordinate_path",
                        "fetch_status",
                    )
                },
                "entry_ids": sorted(
                    [str(entry_id) for entry_id in structure.get("entry_ids", [])],
                    key=_entry_id_sort_key,
                ),
                "entry_partitions": {
                    str(entry_id): row_partitions_by_entry.get(str(entry_id))
                    for entry_id in structure.get("entry_ids", [])
                },
                "entry_structure_keys": {
                    str(entry_id): row_structure_by_entry.get(str(entry_id))
                    for entry_id in structure.get("entry_ids", [])
                },
            }
            for structure in query_structures
        ],
        "top_train_test_pairs": pair_summary["top_train_test_pairs"],
        "blocking_pairs": pair_summary["blocking_pairs"],
    }


def aggregate_foldseek_tm_score_query_chunks(
    *,
    chunks: list[dict[str, Any]],
    chunk_paths: list[str] | None = None,
    slice_id: str | None = None,
    threshold: float = 0.7,
    max_reported_pairs: int = 30,
) -> dict[str, Any]:
    """Aggregate completed Foldseek query chunks without claiming a full holdout."""

    paths = chunk_paths or []
    chunk_records: list[dict[str, Any]] = []
    seen_indices: set[int] = set()
    duplicate_indices: set[int] = set()
    invalid_chunk_paths: list[str | None] = []
    reported_blocking_by_structure_pair: dict[tuple[str, str], dict[str, Any]] = {}
    reported_entry_pairs: set[tuple[str, str]] = set()
    top_train_test_pairs: list[dict[str, Any]] = []
    query_structure_keys: set[str] = set()
    attempted_query_structure_keys: set[str] = set()
    foldseek_versions: set[str] = set()
    foldseek_commands: list[str] = []
    coordinate_exclusions_by_entry: dict[str, dict[str, Any]] = {}

    expected_chunk_count = 0
    expected_chunk_size: int | None = None
    target_staged_coordinate_count = 0
    selected_structure_count = 0
    evaluated_count = 0
    materialized_coordinate_count = 0
    missing_or_unsupported_structure_count = 0
    full_evaluated_coordinate_coverage = True
    all_materializable_coordinate_coverage = True
    max_train_test_tm_score: float | None = None

    total_pair_count = 0
    total_mapped_pair_count = 0
    total_parse_error_count = 0
    total_train_test_pair_count = 0
    total_heldout_in_distribution_pair_count = 0
    total_heldout_pair_count = 0
    total_in_distribution_pair_count = 0
    total_other_partition_pair_count = 0
    total_violating_train_test_pair_row_count = 0
    total_raw_name_mapping_unmapped_count = 0
    chunk_summed_unique_unordered_nonself_pair_count = 0
    reported_blocking_limit_applied = False

    for position, chunk in enumerate(chunks):
        chunk_path = paths[position] if position < len(paths) else None
        metadata = chunk.get("metadata", {}) if isinstance(chunk, dict) else {}
        if (
            not isinstance(metadata, dict)
            or metadata.get("method") != "foldseek_tm_score_query_chunk_signal"
        ):
            invalid_chunk_paths.append(chunk_path)
            continue

        chunk_index = int(metadata.get("query_chunk_index", position) or 0)
        if chunk_index in seen_indices:
            duplicate_indices.add(chunk_index)
            continue
        seen_indices.add(chunk_index)
        completed = (
            metadata.get("foldseek_run_status") == "completed"
            and bool(metadata.get("all_materializable_query_chunk_signal_computed"))
        )
        expected_chunk_count = max(
            expected_chunk_count, int(metadata.get("query_chunk_count", 0) or 0)
        )
        if expected_chunk_size is None:
            expected_chunk_size = int(metadata.get("query_chunk_size", 0) or 0)
        target_staged_coordinate_count = max(
            target_staged_coordinate_count,
            int(metadata.get("target_staged_coordinate_count", 0) or 0),
        )
        selected_structure_count = max(
            selected_structure_count,
            int(metadata.get("selected_structure_count", 0) or 0),
        )
        evaluated_count = max(evaluated_count, int(metadata.get("evaluated_count", 0) or 0))
        materialized_coordinate_count = max(
            materialized_coordinate_count,
            int(metadata.get("materialized_coordinate_count", 0) or 0),
        )
        missing_or_unsupported_structure_count = max(
            missing_or_unsupported_structure_count,
            int(metadata.get("missing_or_unsupported_structure_count", 0) or 0),
        )
        full_evaluated_coordinate_coverage = (
            full_evaluated_coordinate_coverage
            and bool(metadata.get("full_evaluated_coordinate_coverage"))
        )
        all_materializable_coordinate_coverage = (
            all_materializable_coordinate_coverage
            and bool(metadata.get("all_materializable_coordinate_coverage"))
        )
        version = metadata.get("foldseek_version")
        if isinstance(version, str) and version:
            foldseek_versions.add(version)
        command = metadata.get("foldseek_command")
        if isinstance(command, str) and command:
            foldseek_commands.append(command)

        for exclusion in metadata.get("tm_score_coordinate_exclusions", []) or []:
            if not isinstance(exclusion, dict):
                continue
            entry_id = str(exclusion.get("entry_id") or "")
            if entry_id:
                coordinate_exclusions_by_entry[entry_id] = exclusion

        structures = (
            chunk.get("query_staged_structures", []) if isinstance(chunk, dict) else []
        )
        for structure in structures:
            if not isinstance(structure, dict):
                continue
            structure_key = structure.get("structure_key")
            if isinstance(structure_key, str) and structure_key:
                attempted_query_structure_keys.add(structure_key)
                if completed:
                    query_structure_keys.add(structure_key)

        if not completed:
            chunk_records.append(
                {
                    "chunk_index": chunk_index,
                    "chunk_path": chunk_path,
                    "completed": False,
                    "foldseek_run_status": metadata.get("foldseek_run_status"),
                    "query_staged_coordinate_count": metadata.get(
                        "query_staged_coordinate_count"
                    ),
                    "pair_count": metadata.get("pair_count"),
                    "train_test_pair_count": metadata.get("train_test_pair_count"),
                    "max_observed_train_test_tm_score": metadata.get(
                        "max_observed_train_test_tm_score"
                    ),
                    "tm_score_target_achieved_for_query_chunk": metadata.get(
                        "tm_score_target_achieved_for_query_chunk"
                    ),
                }
            )
            continue

        total_pair_count += int(metadata.get("pair_count", 0) or 0)
        total_mapped_pair_count += int(metadata.get("mapped_pair_count", 0) or 0)
        total_parse_error_count += int(metadata.get("parse_error_count", 0) or 0)
        total_train_test_pair_count += int(metadata.get("train_test_pair_count", 0) or 0)
        total_heldout_in_distribution_pair_count += int(
            metadata.get("heldout_in_distribution_pair_count", 0) or 0
        )
        total_heldout_pair_count += int(metadata.get("heldout_pair_count", 0) or 0)
        total_in_distribution_pair_count += int(
            metadata.get("in_distribution_pair_count", 0) or 0
        )
        total_other_partition_pair_count += int(
            metadata.get("other_partition_pair_count", 0) or 0
        )
        total_violating_train_test_pair_row_count += int(
            metadata.get("violating_train_test_pair_row_count", 0) or 0
        )
        total_raw_name_mapping_unmapped_count += int(
            metadata.get("raw_name_mapping_unmapped_count", 0) or 0
        )
        chunk_summed_unique_unordered_nonself_pair_count += int(
            metadata.get("unique_unordered_nonself_pair_count", 0) or 0
        )
        score = _parse_optional_float(metadata.get("max_observed_train_test_tm_score"))
        if score is not None:
            max_train_test_tm_score = (
                score
                if max_train_test_tm_score is None
                else max(max_train_test_tm_score, score)
            )

        blocking_pairs = [
            pair
            for pair in (
                chunk.get("blocking_pairs", metadata.get("blocking_pairs", []))
                if isinstance(chunk, dict)
                else []
            )
            if isinstance(pair, dict)
        ]
        if int(metadata.get("violating_unique_structure_pair_count", 0) or 0) > len(
            blocking_pairs
        ):
            reported_blocking_limit_applied = True
        for pair in blocking_pairs:
            query_key = _foldseek_blocking_pair_member_key(
                pair.get("query_structure_key"), pair.get("raw_query_name")
            )
            target_key = _foldseek_blocking_pair_member_key(
                pair.get("target_structure_key"), pair.get("raw_target_name")
            )
            structure_pair_key = tuple(sorted([query_key, target_key]))
            candidate = {
                **pair,
                "source_chunk_index": chunk_index,
                "source_chunk_path": chunk_path,
            }
            existing = reported_blocking_by_structure_pair.get(structure_pair_key)
            if existing is None or (
                _parse_optional_float(candidate.get("max_pair_tm_score")) or 0.0
            ) > (_parse_optional_float(existing.get("max_pair_tm_score")) or 0.0):
                reported_blocking_by_structure_pair[structure_pair_key] = candidate
            for query_entry_id in _string_list(pair.get("query_entry_ids")) or [
                "unmapped_query"
            ]:
                for target_entry_id in _string_list(pair.get("target_entry_ids")) or [
                    "unmapped_target"
                ]:
                    if query_entry_id != target_entry_id:
                        reported_entry_pairs.add(
                            tuple(sorted([query_entry_id, target_entry_id]))
                        )

        for pair in chunk.get("top_train_test_pairs", []) if isinstance(chunk, dict) else []:
            if isinstance(pair, dict):
                top_train_test_pairs.append(
                    {
                        **pair,
                        "source_chunk_index": chunk_index,
                        "source_chunk_path": chunk_path,
                    }
                )

        chunk_records.append(
            {
                "chunk_index": chunk_index,
                "chunk_path": chunk_path,
                "completed": True,
                "foldseek_run_status": metadata.get("foldseek_run_status"),
                "query_chunk_start": metadata.get("query_chunk_start"),
                "query_chunk_end_exclusive": metadata.get("query_chunk_end_exclusive"),
                "query_staged_coordinate_count": metadata.get(
                    "query_staged_coordinate_count"
                ),
                "pair_count": metadata.get("pair_count"),
                "train_test_pair_count": metadata.get("train_test_pair_count"),
                "max_observed_train_test_tm_score": metadata.get(
                    "max_observed_train_test_tm_score"
                ),
                "violating_train_test_pair_row_count": metadata.get(
                    "violating_train_test_pair_row_count"
                ),
                "violating_unique_structure_pair_count": metadata.get(
                    "violating_unique_structure_pair_count"
                ),
                "tm_score_target_achieved_for_query_chunk": metadata.get(
                    "tm_score_target_achieved_for_query_chunk"
                ),
            }
        )

    chunk_records.sort(key=lambda row: int(row.get("chunk_index", 0) or 0))
    completed_chunk_indices = [
        int(row["chunk_index"]) for row in chunk_records if row.get("completed")
    ]
    expected_indices = set(range(expected_chunk_count)) if expected_chunk_count else set()
    missing_chunk_indices = sorted(expected_indices - set(completed_chunk_indices))
    all_chunks_completed = bool(expected_chunk_count) and not missing_chunk_indices
    completed_query_coordinate_count = len(query_structure_keys)
    max_train_test_tm_score = (
        round(max_train_test_tm_score, 4)
        if max_train_test_tm_score is not None
        else None
    )
    target_achieved_for_completed_chunks = (
        max_train_test_tm_score is not None
        and max_train_test_tm_score < float(threshold)
    )

    blocking_pairs = list(reported_blocking_by_structure_pair.values())
    blocking_pairs.sort(
        key=lambda item: (
            -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
            str(item.get("query_structure_key") or ""),
            str(item.get("target_structure_key") or ""),
        )
    )
    top_train_test_pairs.sort(
        key=lambda item: (
            -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
            int(item.get("source_chunk_index", 0) or 0),
            str(item.get("query_structure_key") or ""),
            str(item.get("target_structure_key") or ""),
        )
    )
    reported_limit = max(1, int(max_reported_pairs))

    claim_blockers = [
        "review-only query-chunk aggregate is not a canonical full holdout claim",
        "canonical sequence split policy remains candidate-only until reviewed",
    ]
    if not all_chunks_completed:
        claim_blockers.append("one or more Foldseek query chunks remain uncomputed")
    if not full_evaluated_coordinate_coverage:
        claim_blockers.append("evaluated selected-coordinate coverage is partial")
    if missing_or_unsupported_structure_count:
        claim_blockers.append("one or more evaluated rows lacks a supported selected structure")
    if duplicate_indices:
        claim_blockers.append("duplicate query chunk indices were supplied")
    if invalid_chunk_paths:
        claim_blockers.append("one or more supplied chunk artifacts were invalid")
    if not target_achieved_for_completed_chunks:
        claim_blockers.append("completed query-chunk train/test TM-score target <0.7 is not achieved")

    limitations = [
        "review-only artifact; it creates no countable labels and no import-ready rows",
        "aggregate uses completed query-chunk artifacts and does not rerun Foldseek",
        "full all-materializable TM-score coverage requires every deterministic query chunk to complete",
        "reported blocking-pair details are limited by each source chunk artifact's reporting cap",
        "full_tm_score_holdout_claim_permitted=false until chunk aggregation, coordinate exclusions, and canonical split policy are resolved",
    ]
    if reported_blocking_limit_applied:
        limitations.append("one or more chunks reported fewer blocking-pair details than its unique violating-pair count")
    if coordinate_exclusions_by_entry:
        limitations.append("selected rows with no supported coordinate structures remain excluded from TM-score computation")

    metadata = {
        "method": "foldseek_tm_score_query_chunk_aggregate",
        "slice_id": str(slice_id or ""),
        "source_chunk_artifacts": [path for path in paths if path],
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "tm_score_split_computed": False,
        "all_materializable_tm_score_signal_computed": all_chunks_completed,
        "all_materializable_query_chunk_aggregate_computed": bool(completed_chunk_indices),
        "all_materializable_tm_score_split_computed": False,
        "full_tm_score_split_computed": False,
        "real_tm_score_computed": bool(completed_chunk_indices),
        "tm_score_signal_coverage_status": "all_materializable_query_chunk_aggregate",
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(claim_blockers)),
        "blockers_remaining": sorted(set(claim_blockers)),
        "threshold_target": "<0.7",
        "tm_score_threshold": float(threshold),
        "tm_score_threshold_target": "<0.7",
        "tm_score_target_operator": "<",
        "tm_score_target_achieved": all_chunks_completed
        and target_achieved_for_completed_chunks,
        "tm_score_target_achieved_for_completed_query_chunks": target_achieved_for_completed_chunks,
        "tm_score_target_evaluation_scope": (
            "mapped heldout/in_distribution pairs from completed query chunks against every staged materializable selected coordinate"
        ),
        "query_chunk_count": expected_chunk_count,
        "query_chunk_size": expected_chunk_size,
        "completed_query_chunk_count": len(completed_chunk_indices),
        "completed_query_chunk_indices": completed_chunk_indices,
        "missing_query_chunk_count": len(missing_chunk_indices),
        "missing_query_chunk_indices": missing_chunk_indices,
        "all_query_chunks_completed": all_chunks_completed,
        "duplicate_query_chunk_indices": sorted(duplicate_indices),
        "invalid_chunk_artifacts": invalid_chunk_paths,
        "target_staged_coordinate_count": target_staged_coordinate_count,
        "staged_coordinate_count": target_staged_coordinate_count,
        "selected_structure_count": selected_structure_count,
        "evaluated_count": evaluated_count,
        "materialized_coordinate_count": materialized_coordinate_count,
        "query_staged_coordinate_count": completed_query_coordinate_count,
        "query_staged_structure_count": completed_query_coordinate_count,
        "attempted_query_coordinate_count": len(attempted_query_structure_keys),
        "attempted_query_structure_count": len(attempted_query_structure_keys),
        "completed_query_coordinate_count": completed_query_coordinate_count,
        "remaining_uncomputed_query_coordinate_count": max(
            0, target_staged_coordinate_count - completed_query_coordinate_count
        ),
        "completed_query_coordinate_coverage": _safe_ratio(
            completed_query_coordinate_count, target_staged_coordinate_count
        ),
        "full_evaluated_coordinate_coverage": full_evaluated_coordinate_coverage,
        "all_materializable_coordinate_coverage": all_materializable_coordinate_coverage,
        "missing_or_unsupported_structure_count": missing_or_unsupported_structure_count,
        "missing_or_unsupported_structures": sorted(
            coordinate_exclusions_by_entry.values(),
            key=lambda item: _entry_id_sort_key(str(item.get("entry_id") or "")),
        ),
        "tm_score_coordinate_exclusion_count": len(coordinate_exclusions_by_entry),
        "tm_score_coordinate_exclusions": sorted(
            coordinate_exclusions_by_entry.values(),
            key=lambda item: _entry_id_sort_key(str(item.get("entry_id") or "")),
        ),
        "pair_count": total_pair_count,
        "mapped_pair_count": total_mapped_pair_count,
        "parse_error_count": total_parse_error_count,
        "train_test_pair_count": total_train_test_pair_count,
        "heldout_in_distribution_pair_count": total_heldout_in_distribution_pair_count,
        "heldout_pair_count": total_heldout_pair_count,
        "in_distribution_pair_count": total_in_distribution_pair_count,
        "other_partition_pair_count": total_other_partition_pair_count,
        "unique_unordered_nonself_pair_count": chunk_summed_unique_unordered_nonself_pair_count,
        "unique_unordered_nonself_pair_count_semantics": "sum_of_completed_chunk_counts_not_globally_deduplicated",
        "max_observed_train_test_tm_score": max_train_test_tm_score,
        "max_observed_train_test_tm_score_computable": max_train_test_tm_score is not None,
        "max_observed_train_test_tm_score_metric": (
            "max(qtmscore, ttmscore, alntmscore) across mapped heldout/in_distribution pairs in completed query chunks"
        ),
        "violating_train_test_pair_row_count": total_violating_train_test_pair_row_count,
        "violating_unique_structure_pair_count_reported": len(blocking_pairs),
        "violating_unique_structure_pair_count_sum_from_chunks": sum(
            int(row.get("violating_unique_structure_pair_count", 0) or 0)
            for row in chunk_records
            if row.get("completed")
        ),
        "violating_unique_entry_pair_count_reported": len(reported_entry_pairs),
        "reported_blocking_pair_limit_applied": reported_blocking_limit_applied,
        "max_reported_pairs": reported_limit,
        "raw_name_mapping_unmapped_count": total_raw_name_mapping_unmapped_count,
        "foldseek_versions": sorted(foldseek_versions),
        "foldseek_commands": foldseek_commands[:reported_limit],
        "foldseek_command_count": len(foldseek_commands),
        "limitations": sorted(set(limitations)),
    }
    return {
        "metadata": metadata,
        "chunks": chunk_records,
        "top_train_test_pairs": top_train_test_pairs[:reported_limit],
        "blocking_pairs": blocking_pairs[:reported_limit],
    }


def audit_foldseek_tm_score_target_failure(
    *,
    signal: dict[str, Any],
    signal_path: str | None = None,
    threshold: float = 0.7,
    max_blocking_pairs: int = 20,
) -> dict[str, Any]:
    """Summarize Foldseek train/test TM-score pairs that block the target.

    A single mapped train/test pair at or above the threshold is enough to
    disallow a current-split TM-score holdout pass. This audit keeps that
    evidence compact and explicit without claiming a full split.
    """

    metadata_in = signal.get("metadata", {}) if isinstance(signal, dict) else {}
    if not isinstance(metadata_in, dict):
        metadata_in = {}
    rows_in = signal.get("rows", []) if isinstance(signal, dict) else []
    rows = [row for row in rows_in if isinstance(row, dict)]
    threshold_value = float(threshold)

    train_test_rows = [
        row
        for row in rows
        if row.get("train_test_pair")
        and _parse_optional_float(row.get("max_pair_tm_score")) is not None
    ]
    violating_rows = [
        row
        for row in train_test_rows
        if (_parse_optional_float(row.get("max_pair_tm_score")) or 0.0)
        >= threshold_value
    ]

    best_by_structure_pair: dict[tuple[str, str], dict[str, Any]] = {}
    entry_pair_keys: set[tuple[str, str]] = set()
    for row in violating_rows:
        query_key = _foldseek_blocking_pair_member_key(
            row.get("query_structure_key"), row.get("raw_query_name")
        )
        target_key = _foldseek_blocking_pair_member_key(
            row.get("target_structure_key"), row.get("raw_target_name")
        )
        structure_pair_key = tuple(sorted((query_key, target_key)))
        if (
            structure_pair_key not in best_by_structure_pair
            or (_parse_optional_float(row.get("max_pair_tm_score")) or 0.0)
            > (
                _parse_optional_float(
                    best_by_structure_pair[structure_pair_key].get("max_pair_tm_score")
                )
                or 0.0
            )
        ):
            best_by_structure_pair[structure_pair_key] = row

        query_entries = [
            str(entry_id)
            for entry_id in row.get("query_entry_ids", [])
            if isinstance(entry_id, str)
        ]
        target_entries = [
            str(entry_id)
            for entry_id in row.get("target_entry_ids", [])
            if isinstance(entry_id, str)
        ]
        for query_entry in query_entries:
            for target_entry in target_entries:
                entry_pair_keys.add(tuple(sorted((query_entry, target_entry))))

    blocking_pairs = [
        _foldseek_blocking_pair_summary(row, threshold_value)
        for row in sorted(
            best_by_structure_pair.values(),
            key=lambda item: (
                -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
                str(
                    item.get("query_structure_key")
                    or item.get("raw_query_name")
                    or ""
                ),
                str(
                    item.get("target_structure_key")
                    or item.get("raw_target_name")
                    or ""
                ),
            ),
        )[: max(0, int(max_blocking_pairs))]
    ]

    max_train_test_tm_score = None
    for row in train_test_rows:
        score = _parse_optional_float(row.get("max_pair_tm_score"))
        if score is None:
            continue
        max_train_test_tm_score = (
            score
            if max_train_test_tm_score is None
            else max(max_train_test_tm_score, score)
        )
    target_blocked = bool(violating_rows)
    source_claim_blockers = [
        str(blocker)
        for blocker in metadata_in.get("full_tm_score_holdout_claim_blockers", [])
        if isinstance(blocker, str)
    ]
    claim_blockers = list(source_claim_blockers)
    if target_blocked:
        claim_blockers.append(
            "computed train/test TM-score target <0.7 is already violated in the computed subset"
        )
    if not metadata_in.get("full_tm_score_split_computed"):
        claim_blockers.append("full all-materializable TM-score split remains uncomputed")
    if metadata_in.get("tm_signal_coordinate_cap_applied"):
        claim_blockers.append("available staged coordinates were excluded by the signal cap")

    limitations = [
        "audit summarizes an existing Foldseek TM-score signal and does not run Foldseek",
        "review-only artifact; it creates no countable labels and no import-ready rows",
        "blocking pairs are evaluated against the current sequence-holdout train/test partition only",
    ]
    if metadata_in.get("tm_score_signal_coverage_status") != "full_evaluated_coordinate_signal":
        limitations.append(
            "source Foldseek signal is partial; additional pairs may add blockers but cannot remove an observed target violation"
        )
    if not target_blocked:
        limitations.append(
            "no target-violating train/test pair was observed in the supplied signal"
        )

    metadata = {
        "method": "foldseek_tm_score_target_failure_audit",
        "blocker_removed": (
            "identifies exact Foldseek train/test TM-score pair evidence that "
            "violates the current <0.7 target; the current sequence-holdout "
            "split cannot claim TM-score separation without split repair or "
            "explicit exclusion review"
            if target_blocked
            else None
        ),
        "blocker_not_removed": (
            "full all-materializable Foldseek/TM-score split remains uncomputed"
            if not metadata_in.get("full_tm_score_split_computed")
            else None
        ),
        "blockers_remaining": sorted(set(claim_blockers)),
        "slice_id": str(metadata_in.get("slice_id") or ""),
        "source_signal_artifact": signal_path,
        "source_signal_method": metadata_in.get("method"),
        "source_signal_foldseek_version": metadata_in.get("foldseek_version"),
        "source_signal_foldseek_command": metadata_in.get("foldseek_command"),
        "source_signal_run_status": metadata_in.get("foldseek_run_status"),
        "source_signal_staged_coordinate_count": metadata_in.get(
            "staged_coordinate_count"
        ),
        "source_signal_available_staged_coordinate_count": metadata_in.get(
            "available_staged_coordinate_count"
        ),
        "source_signal_remaining_uncomputed_staged_coordinate_count": metadata_in.get(
            "remaining_uncomputed_staged_coordinate_count"
        ),
        "source_signal_coverage_status": metadata_in.get(
            "tm_score_signal_coverage_status"
        ),
        "source_signal_full_tm_score_split_computed": bool(
            metadata_in.get("full_tm_score_split_computed")
        ),
        "source_signal_full_tm_score_holdout_claim_permitted": bool(
            metadata_in.get("full_tm_score_holdout_claim_permitted")
        ),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "threshold_target": "<0.7",
        "tm_score_threshold": threshold_value,
        "tm_score_target_operator": "<",
        "train_test_pair_count": len(train_test_rows),
        "violating_train_test_pair_row_count": len(violating_rows),
        "violating_unique_structure_pair_count": len(best_by_structure_pair),
        "violating_unique_entry_pair_count": len(entry_pair_keys),
        "max_reported_blocking_pairs": max(0, int(max_blocking_pairs)),
        "max_observed_train_test_tm_score": (
            round(max_train_test_tm_score, 4)
            if max_train_test_tm_score is not None
            else None
        ),
        "max_observed_train_test_tm_score_computable": max_train_test_tm_score is not None,
        "tm_score_target_achieved_for_computed_subset": (
            False
            if target_blocked
            else (
                max_train_test_tm_score < threshold_value
                if max_train_test_tm_score is not None
                else None
            )
        ),
        "current_sequence_holdout_split_tm_score_target_blocked": target_blocked,
        "split_repair_required_for_target": target_blocked,
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(claim_blockers)),
        "limitations": sorted(set(limitations)),
    }

    return {"metadata": metadata, "blocking_pairs": blocking_pairs}


def audit_foldseek_tm_score_split_repair(
    *,
    target_failure: dict[str, Any],
    sequence_holdout: dict[str, Any],
    target_failure_path: str | None = None,
    sequence_holdout_path: str | None = None,
    threshold: float = 0.7,
) -> dict[str, Any]:
    """Plan a conservative repair for observed Foldseek TM-score split failures.

    This does not rewrite the sequence holdout. It identifies whether each
    observed target-violating train/test pair has a concrete split-repair
    candidate that preserves held-out in-scope positives.
    """

    target_metadata = (
        target_failure.get("metadata", {}) if isinstance(target_failure, dict) else {}
    )
    if not isinstance(target_metadata, dict):
        target_metadata = {}
    holdout_metadata = (
        sequence_holdout.get("metadata", {})
        if isinstance(sequence_holdout, dict)
        else {}
    )
    if not isinstance(holdout_metadata, dict):
        holdout_metadata = {}

    holdout_rows = [
        row
        for row in (sequence_holdout.get("rows", []) if isinstance(sequence_holdout, dict) else [])
        if isinstance(row, dict)
    ]
    rows_by_entry = {
        str(row["entry_id"]): row
        for row in holdout_rows
        if isinstance(row.get("entry_id"), str)
    }
    blocking_pairs = [
        row
        for row in (
            target_failure.get("blocking_pairs", [])
            if isinstance(target_failure, dict)
            else []
        )
        if isinstance(row, dict) and row.get("violates_target")
    ]

    rows: list[dict[str, Any]] = []
    moved_heldout_entries: set[str] = set()
    manual_review_count = 0
    repair_candidate_count = 0
    moved_heldout_in_scope_count = 0
    moved_heldout_out_of_scope_count = 0

    for index, pair in enumerate(blocking_pairs, start=1):
        query_entries = _string_list(pair.get("query_entry_ids"))
        target_entries = _string_list(pair.get("target_entry_ids"))
        entry_ids = sorted(set(query_entries + target_entries), key=_entry_id_sort_key)
        missing_entries = [entry_id for entry_id in entry_ids if entry_id not in rows_by_entry]
        entry_rows = {entry_id: rows_by_entry.get(entry_id, {}) for entry_id in entry_ids}
        heldout_entries = [
            entry_id
            for entry_id in entry_ids
            if entry_rows.get(entry_id, {}).get("partition") == "heldout"
        ]
        in_distribution_entries = [
            entry_id
            for entry_id in entry_ids
            if entry_rows.get(entry_id, {}).get("partition") == "in_distribution"
        ]
        heldout_in_scope_entries = [
            entry_id
            for entry_id in heldout_entries
            if entry_rows.get(entry_id, {}).get("label_type") != "out_of_scope"
        ]
        heldout_out_of_scope_entries = [
            entry_id
            for entry_id in heldout_entries
            if entry_rows.get(entry_id, {}).get("label_type") == "out_of_scope"
        ]
        score = _parse_optional_float(pair.get("max_pair_tm_score"))
        score_blocks_target = score is not None and score >= float(threshold)

        if missing_entries:
            status = "requires_manual_review_missing_sequence_holdout_rows"
            action = "inspect_missing_sequence_holdout_rows_before_repartition"
            repair_candidate = False
        elif not score_blocks_target:
            status = "no_repair_needed_below_threshold"
            action = "keep_existing_partition_for_this_pair"
            repair_candidate = False
        elif not heldout_entries or not in_distribution_entries:
            status = "requires_manual_review_not_a_simple_train_test_pair"
            action = "inspect_pair_partition_before_repartition"
            repair_candidate = False
        elif heldout_in_scope_entries:
            status = "requires_manual_review_would_move_heldout_in_scope_rows"
            action = "design_new_stratified_partition_before_repartition"
            repair_candidate = False
        else:
            status = "repair_candidate_move_heldout_out_of_scope_entries_to_in_distribution"
            action = (
                "move_heldout_out_of_scope_entries_to_in_distribution_and_regenerate_"
                "sequence_holdout_metrics_before_any_tm_score_claim"
            )
            repair_candidate = True
            moved_heldout_entries.update(heldout_out_of_scope_entries)

        if repair_candidate:
            repair_candidate_count += 1
            moved_heldout_out_of_scope_count += len(heldout_out_of_scope_entries)
        else:
            manual_review_count += 1
        moved_heldout_in_scope_count += len(heldout_in_scope_entries)

        rows.append(
            {
                "blocking_pair_index": index,
                "blocking_pair_id": "|".join(entry_ids),
                "query_structure_key": pair.get("query_structure_key"),
                "target_structure_key": pair.get("target_structure_key"),
                "query_structure_id": pair.get("query_structure_id"),
                "target_structure_id": pair.get("target_structure_id"),
                "query_entry_ids": query_entries,
                "target_entry_ids": target_entries,
                "entry_ids": entry_ids,
                "missing_sequence_holdout_entry_ids": missing_entries,
                "current_partition_by_entry": {
                    entry_id: entry_rows.get(entry_id, {}).get("partition")
                    for entry_id in entry_ids
                },
                "label_type_by_entry": {
                    entry_id: entry_rows.get(entry_id, {}).get("label_type")
                    for entry_id in entry_ids
                },
                "label_group_by_entry": {
                    entry_id: entry_rows.get(entry_id, {}).get("label_group")
                    for entry_id in entry_ids
                },
                "top1_fingerprint_by_entry": {
                    entry_id: entry_rows.get(entry_id, {}).get("top1_fingerprint_id")
                    for entry_id in entry_ids
                },
                "selected_structure_proxy_by_entry": {
                    entry_id: entry_rows.get(entry_id, {}).get("selected_structure_proxy_id")
                    for entry_id in entry_ids
                },
                "heldout_entry_ids": heldout_entries,
                "in_distribution_entry_ids": in_distribution_entries,
                "heldout_in_scope_entry_ids": heldout_in_scope_entries,
                "heldout_out_of_scope_entry_ids": heldout_out_of_scope_entries,
                "proposed_entries_to_move_to_in_distribution": (
                    heldout_out_of_scope_entries if repair_candidate else []
                ),
                "projected_pair_partition_after_repair": (
                    "co_partitioned_in_distribution" if repair_candidate else None
                ),
                "max_pair_tm_score": pair.get("max_pair_tm_score"),
                "threshold": float(threshold),
                "target_operator": "<",
                "violates_target": score_blocks_target,
                "repair_candidate": repair_candidate,
                "repair_status": status,
                "recommended_repair_action": action,
                "review_status": "review_only_non_countable",
                "countable_label_candidate": False,
                "import_ready": False,
            }
        )

    heldout_count = int(holdout_metadata.get("heldout_count", 0) or 0)
    in_distribution_count = int(holdout_metadata.get("in_distribution_count", 0) or 0)
    heldout_in_scope_before = sum(
        1
        for row in holdout_rows
        if row.get("partition") == "heldout" and row.get("label_type") != "out_of_scope"
    )
    heldout_out_of_scope_before = sum(
        1
        for row in holdout_rows
        if row.get("partition") == "heldout" and row.get("label_type") == "out_of_scope"
    )
    projected_heldout_count = max(0, heldout_count - len(moved_heldout_entries))
    projected_in_distribution_count = in_distribution_count + len(moved_heldout_entries)
    projected_heldout_in_scope_count = max(
        0, heldout_in_scope_before - moved_heldout_in_scope_count
    )
    projected_heldout_out_of_scope_count = max(
        0, heldout_out_of_scope_before - moved_heldout_out_of_scope_count
    )
    all_pairs_have_repair_candidate = bool(blocking_pairs) and repair_candidate_count == len(
        blocking_pairs
    )
    projected_observed_blocking_pairs_after_repair = (
        0 if all_pairs_have_repair_candidate else len(blocking_pairs) - repair_candidate_count
    )
    target_blocked = bool(
        target_metadata.get("current_sequence_holdout_split_tm_score_target_blocked")
        or blocking_pairs
    )

    claim_blockers = [
        str(blocker)
        for blocker in target_metadata.get("full_tm_score_holdout_claim_blockers", [])
        if isinstance(blocker, str)
    ]
    claim_blockers.extend(
        [
            "split repair plan has not been applied to the sequence holdout",
            "sequence holdout metrics must be regenerated after any split repair",
            "full all-materializable TM-score split remains uncomputed",
        ]
    )
    if projected_observed_blocking_pairs_after_repair:
        claim_blockers.append(
            "one or more observed blocking pairs lacks a conservative repair candidate"
        )

    metadata = {
        "method": "foldseek_tm_score_split_repair_plan",
        "blocker_removed": (
            "turns the observed target-violating Foldseek train/test pair into a "
            "concrete split-repair candidate that preserves held-out in-scope positives"
            if all_pairs_have_repair_candidate
            else None
        ),
        "blocker_not_removed": "full all-materializable Foldseek/TM-score split remains uncomputed",
        "blockers_remaining": sorted(set(claim_blockers)),
        "slice_id": str(
            target_metadata.get("slice_id") or holdout_metadata.get("slice_id") or ""
        ),
        "target_failure_artifact": target_failure_path,
        "sequence_holdout_artifact": sequence_holdout_path,
        "source_target_failure_method": target_metadata.get("method"),
        "source_sequence_holdout_method": holdout_metadata.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "threshold_target": "<0.7",
        "tm_score_threshold": float(threshold),
        "tm_score_target_operator": "<",
        "current_sequence_holdout_split_tm_score_target_blocked": target_blocked,
        "split_repair_required_for_target": target_blocked,
        "observed_blocking_pair_count": len(blocking_pairs),
        "repair_candidate_pair_count": repair_candidate_count,
        "manual_review_pair_count": manual_review_count,
        "all_observed_blocking_pairs_have_repair_candidate": all_pairs_have_repair_candidate,
        "projected_observed_blocking_pair_count_after_repair": projected_observed_blocking_pairs_after_repair,
        "proposed_moved_heldout_entry_ids": sorted(
            moved_heldout_entries, key=_entry_id_sort_key
        ),
        "proposed_moved_heldout_entry_count": len(moved_heldout_entries),
        "proposed_moved_heldout_in_scope_entry_count": moved_heldout_in_scope_count,
        "proposed_moved_heldout_out_of_scope_entry_count": moved_heldout_out_of_scope_count,
        "heldout_count_before_repair": heldout_count,
        "projected_heldout_count_after_repair": projected_heldout_count,
        "in_distribution_count_before_repair": in_distribution_count,
        "projected_in_distribution_count_after_repair": projected_in_distribution_count,
        "heldout_in_scope_count_before_repair": heldout_in_scope_before,
        "projected_heldout_in_scope_count_after_repair": projected_heldout_in_scope_count,
        "heldout_out_of_scope_count_before_repair": heldout_out_of_scope_before,
        "projected_heldout_out_of_scope_count_after_repair": projected_heldout_out_of_scope_count,
        "sequence_holdout_metrics_need_regeneration_after_repair": bool(
            moved_heldout_entries
        ),
        "tm_score_signal_coverage_status": target_metadata.get(
            "source_signal_coverage_status"
        ),
        "source_signal_full_tm_score_split_computed": bool(
            target_metadata.get("source_signal_full_tm_score_split_computed")
        ),
        "source_signal_remaining_uncomputed_staged_coordinate_count": target_metadata.get(
            "source_signal_remaining_uncomputed_staged_coordinate_count"
        ),
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(claim_blockers)),
        "limitations": sorted(
            {
                "repair plan is not applied to the sequence holdout artifact",
                "review-only artifact; it creates no countable labels and no import-ready rows",
                "plan covers observed target-violating pairs in the supplied partial Foldseek signal only",
                "sequence holdout and downstream retrieval metrics must be regenerated before any repaired split can be evaluated",
                "full all-materializable Foldseek/TM-score split remains uncomputed",
            }
        ),
    }
    return {"metadata": metadata, "rows": rows}


def project_foldseek_tm_score_split_repair(
    *,
    signal: dict[str, Any],
    repair_plan: dict[str, Any],
    signal_path: str | None = None,
    repair_plan_path: str | None = None,
    threshold: float = 0.7,
    max_reported_pairs: int = 20,
) -> dict[str, Any]:
    """Project a proposed split repair across an existing Foldseek signal.

    The projection reclassifies pair partitions in memory only. It does not
    mutate the sequence holdout or rerun Foldseek.
    """

    signal_metadata = signal.get("metadata", {}) if isinstance(signal, dict) else {}
    if not isinstance(signal_metadata, dict):
        signal_metadata = {}
    repair_metadata = (
        repair_plan.get("metadata", {}) if isinstance(repair_plan, dict) else {}
    )
    if not isinstance(repair_metadata, dict):
        repair_metadata = {}

    moved_entries = sorted(
        {
            str(entry_id)
            for entry_id in repair_metadata.get("proposed_moved_heldout_entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    moved_entry_set = set(moved_entries)
    threshold_value = float(threshold)
    rows_in = [
        row
        for row in (signal.get("rows", []) if isinstance(signal, dict) else [])
        if isinstance(row, dict)
    ]

    source_train_test_count = 0
    source_violating_count = 0
    source_max_train_test_tm_score: float | None = None
    projected_train_test_rows: list[dict[str, Any]] = []
    projected_violating_rows: list[dict[str, Any]] = []
    projected_max_train_test_tm_score: float | None = None

    for row in rows_in:
        score = _parse_optional_float(row.get("max_pair_tm_score"))
        if row.get("train_test_pair"):
            source_train_test_count += 1
            if score is not None:
                source_max_train_test_tm_score = (
                    score
                    if source_max_train_test_tm_score is None
                    else max(source_max_train_test_tm_score, score)
                )
                if score >= threshold_value:
                    source_violating_count += 1

        query_entries = _string_list(row.get("query_entry_ids"))
        target_entries = _string_list(row.get("target_entry_ids"))
        query_partitions = _projected_partitions_after_entry_moves(
            row.get("query_partitions"), query_entries, moved_entry_set
        )
        target_partitions = _projected_partitions_after_entry_moves(
            row.get("target_partitions"), target_entries, moved_entry_set
        )
        projected_train_test = _partitions_are_train_test_pair(
            query_partitions, target_partitions
        )
        if not projected_train_test:
            continue
        projected_row = _foldseek_projected_pair_summary(
            row=row,
            query_partitions=query_partitions,
            target_partitions=target_partitions,
            threshold=threshold_value,
        )
        projected_train_test_rows.append(projected_row)
        if score is not None:
            projected_max_train_test_tm_score = (
                score
                if projected_max_train_test_tm_score is None
                else max(projected_max_train_test_tm_score, score)
            )
            if score >= threshold_value:
                projected_violating_rows.append(projected_row)

    projected_target_achieved = (
        projected_max_train_test_tm_score is not None
        and projected_max_train_test_tm_score < threshold_value
    )
    top_projected_pairs = sorted(
        projected_train_test_rows,
        key=lambda item: (
            -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
            str(item.get("query_structure_key") or ""),
            str(item.get("target_structure_key") or ""),
        ),
    )[: max(0, int(max_reported_pairs))]

    source_claim_blockers = [
        str(blocker)
        for blocker in signal_metadata.get("full_tm_score_holdout_claim_blockers", [])
        if isinstance(blocker, str)
    ]
    if projected_target_achieved:
        source_claim_blockers = [
            blocker
            for blocker in source_claim_blockers
            if "computed train/test TM-score target <0.7" not in blocker
        ]
    claim_blockers = source_claim_blockers + [
        "split repair projection has not been applied to the sequence holdout",
        "sequence holdout metrics must be regenerated after split repair",
        "downstream retrieval and holdout metrics must be recomputed after split repair",
        "full all-materializable TM-score split remains uncomputed",
    ]
    if projected_violating_rows:
        claim_blockers.append(
            "projected train/test TM-score target <0.7 is still violated in the computed subset"
        )
    if not moved_entries:
        claim_blockers.append("no held-out entries were proposed for split repair")

    metadata = {
        "method": "foldseek_tm_score_split_repair_projection",
        "blocker_removed": (
            "projects the split-repair candidate across the existing Foldseek signal; "
            "the computed subset has no remaining train/test TM-score target violations"
            if projected_target_achieved and not projected_violating_rows
            else None
        ),
        "blocker_not_removed": (
            "repair is projected only; sequence holdout metrics and full Foldseek split "
            "remain unregenerated"
        ),
        "blockers_remaining": sorted(set(claim_blockers)),
        "slice_id": str(
            signal_metadata.get("slice_id") or repair_metadata.get("slice_id") or ""
        ),
        "signal_artifact": signal_path,
        "repair_plan_artifact": repair_plan_path,
        "source_signal_method": signal_metadata.get("method"),
        "source_repair_plan_method": repair_metadata.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "threshold_target": "<0.7",
        "tm_score_threshold": threshold_value,
        "tm_score_target_operator": "<",
        "projection_only": True,
        "repair_applied_to_sequence_holdout": False,
        "sequence_holdout_metrics_regenerated": False,
        "proposed_moved_heldout_entry_ids": moved_entries,
        "proposed_moved_heldout_entry_count": len(moved_entries),
        "source_train_test_pair_count": source_train_test_count,
        "source_violating_train_test_pair_row_count": source_violating_count,
        "source_max_observed_train_test_tm_score": (
            round(source_max_train_test_tm_score, 4)
            if source_max_train_test_tm_score is not None
            else None
        ),
        "projected_train_test_pair_count": len(projected_train_test_rows),
        "projected_violating_train_test_pair_row_count": len(projected_violating_rows),
        "projected_max_observed_train_test_tm_score": (
            round(projected_max_train_test_tm_score, 4)
            if projected_max_train_test_tm_score is not None
            else None
        ),
        "projected_tm_score_target_achieved_for_computed_subset": projected_target_achieved,
        "computed_subset_target_blocker_removed_by_projection": (
            projected_target_achieved and not projected_violating_rows
        ),
        "source_signal_staged_coordinate_count": signal_metadata.get(
            "staged_coordinate_count"
        ),
        "source_signal_remaining_uncomputed_staged_coordinate_count": signal_metadata.get(
            "remaining_uncomputed_staged_coordinate_count"
        ),
        "source_signal_coverage_status": signal_metadata.get(
            "tm_score_signal_coverage_status"
        ),
        "source_signal_full_tm_score_split_computed": bool(
            signal_metadata.get("full_tm_score_split_computed")
        ),
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(claim_blockers)),
        "max_reported_pairs": max(0, int(max_reported_pairs)),
        "limitations": sorted(
            {
                "projection reclassifies existing Foldseek rows only and does not rerun Foldseek",
                "repair is not applied to the sequence holdout artifact",
                "sequence holdout and downstream retrieval metrics must be regenerated before any repaired split can be evaluated",
                "source Foldseek signal may be partial; an uncapped full split remains required",
                "review-only artifact; it creates no countable labels and no import-ready rows",
            }
        ),
    }
    return {
        "metadata": metadata,
        "projected_top_train_test_pairs": top_projected_pairs,
        "projected_blocking_pairs": projected_violating_rows[
            : max(0, int(max_reported_pairs))
        ],
    }


def build_sequence_distance_holdout_split_repair_candidate(
    *,
    sequence_holdout: dict[str, Any],
    repair_plan: dict[str, Any],
    projection: dict[str, Any] | None = None,
    sequence_holdout_path: str | None = None,
    repair_plan_path: str | None = None,
    projection_path: str | None = None,
) -> dict[str, Any]:
    """Apply a split-repair plan to a candidate copy of a sequence holdout."""

    source_metadata = (
        sequence_holdout.get("metadata", {})
        if isinstance(sequence_holdout, dict)
        else {}
    )
    if not isinstance(source_metadata, dict):
        source_metadata = {}
    repair_metadata = (
        repair_plan.get("metadata", {}) if isinstance(repair_plan, dict) else {}
    )
    if not isinstance(repair_metadata, dict):
        repair_metadata = {}
    projection_metadata = (
        (projection or {}).get("metadata", {}) if isinstance(projection, dict) else {}
    )
    if not isinstance(projection_metadata, dict):
        projection_metadata = {}

    moved_entries = sorted(
        {
            str(entry_id)
            for entry_id in repair_metadata.get("proposed_moved_heldout_entry_ids", [])
            if isinstance(entry_id, str)
        },
        key=_entry_id_sort_key,
    )
    moved_entry_set = set(moved_entries)
    rows_in = [
        row
        for row in (
            sequence_holdout.get("rows", [])
            if isinstance(sequence_holdout, dict)
            else []
        )
        if isinstance(row, dict)
    ]
    found_entries = {
        str(row.get("entry_id")) for row in rows_in if isinstance(row.get("entry_id"), str)
    }
    missing_moved_entries = [
        entry_id for entry_id in moved_entries if entry_id not in found_entries
    ]

    candidate_rows: list[dict[str, Any]] = []
    applied_entries: list[str] = []
    for row in rows_in:
        entry_id = str(row.get("entry_id") or "")
        source_partition = row.get("partition")
        candidate = dict(row)
        candidate["source_partition"] = source_partition
        candidate["split_repair_candidate_partition"] = source_partition
        candidate["split_repair_applied_to_candidate"] = False
        candidate["split_repair_reason"] = None
        if entry_id in moved_entry_set and source_partition == "heldout":
            candidate["partition"] = "in_distribution"
            candidate["split_repair_candidate_partition"] = "in_distribution"
            candidate["split_repair_applied_to_candidate"] = True
            candidate["split_repair_reason"] = (
                "foldseek_tm_score_split_repair_move_heldout_out_of_scope_to_in_distribution"
            )
            applied_entries.append(entry_id)
        candidate_rows.append(candidate)

    repaired_metrics = _sequence_holdout_partition_metrics(candidate_rows)
    source_metrics = _sequence_holdout_partition_metrics(rows_in)
    moved_cluster_ids = {
        str(row.get("real_sequence_identity_cluster_id") or "")
        for row in rows_in
        if row.get("entry_id") in moved_entry_set
        and row.get("real_sequence_identity_cluster_id")
    }
    remaining_heldout_cluster_ids = {
        str(row.get("real_sequence_identity_cluster_id") or "")
        for row in candidate_rows
        if row.get("partition") == "heldout"
        and row.get("real_sequence_identity_cluster_id")
    }
    split_cluster_ids = sorted(moved_cluster_ids & remaining_heldout_cluster_ids)
    sequence_identity_target_preserved = bool(
        source_metadata.get("sequence_identity_target_achieved")
        or source_metadata.get("target_identity_achieved")
    ) and not split_cluster_ids

    claim_blockers = [
        "candidate sequence holdout has not replaced the canonical sequence holdout",
        "full all-materializable TM-score split remains uncomputed",
        "downstream accepted-registry artifacts have not been rebuilt from this candidate holdout",
    ]
    if not projection_metadata.get("computed_subset_target_blocker_removed_by_projection"):
        claim_blockers.append(
            "Foldseek computed-subset target repair projection is absent or unresolved"
        )
    if split_cluster_ids:
        claim_blockers.append(
            "moving heldout entries would split one or more sequence-identity clusters"
        )
    if missing_moved_entries:
        claim_blockers.append("one or more proposed moved entries is missing from the holdout")

    metadata = {
        "method": "sequence_distance_holdout_split_repair_candidate",
        "blocker_removed": (
            "applies the Foldseek split-repair move to a candidate sequence-holdout copy "
            "and recomputes partition metrics without moving held-out in-scope rows"
            if applied_entries and not split_cluster_ids
            else None
        ),
        "blocker_not_removed": (
            "candidate holdout is not canonical and full Foldseek/TM-score split remains uncomputed"
        ),
        "blockers_remaining": sorted(set(claim_blockers)),
        "slice_id": str(
            source_metadata.get("slice_id") or repair_metadata.get("slice_id") or ""
        ),
        "sequence_holdout_artifact": sequence_holdout_path,
        "repair_plan_artifact": repair_plan_path,
        "projection_artifact": projection_path,
        "source_sequence_holdout_method": source_metadata.get("method"),
        "source_repair_plan_method": repair_metadata.get("method"),
        "source_projection_method": projection_metadata.get("method"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate_count": 0,
        "countable_label_count": 0,
        "import_ready_candidate_count": 0,
        "import_ready_row_count": 0,
        "ready_for_label_import": False,
        "canonical_holdout_replaced": False,
        "repair_candidate_applied": bool(applied_entries),
        "proposed_moved_heldout_entry_ids": moved_entries,
        "applied_moved_heldout_entry_ids": sorted(
            applied_entries, key=_entry_id_sort_key
        ),
        "missing_moved_heldout_entry_ids": missing_moved_entries,
        "source_heldout_count": source_metrics["heldout_count"],
        "repaired_heldout_count": repaired_metrics["heldout_count"],
        "source_in_distribution_count": source_metrics["in_distribution_count"],
        "repaired_in_distribution_count": repaired_metrics["in_distribution_count"],
        "source_heldout_in_scope_count": source_metrics["heldout_in_scope_count"],
        "repaired_heldout_in_scope_count": repaired_metrics["heldout_in_scope_count"],
        "source_heldout_out_of_scope_count": source_metrics[
            "heldout_out_of_scope_count"
        ],
        "repaired_heldout_out_of_scope_count": repaired_metrics[
            "heldout_out_of_scope_count"
        ],
        "source_heldout_out_of_scope_false_non_abstention_count": source_metrics[
            "heldout_out_of_scope_false_non_abstention_count"
        ],
        "repaired_heldout_out_of_scope_false_non_abstention_count": repaired_metrics[
            "heldout_out_of_scope_false_non_abstention_count"
        ],
        "source_heldout_in_scope_top1_accuracy": source_metrics[
            "heldout_in_scope_top1_accuracy"
        ],
        "repaired_heldout_in_scope_top1_accuracy": repaired_metrics[
            "heldout_in_scope_top1_accuracy"
        ],
        "source_heldout_in_scope_top3_accuracy": source_metrics[
            "heldout_in_scope_top3_accuracy"
        ],
        "repaired_heldout_in_scope_top3_accuracy": repaired_metrics[
            "heldout_in_scope_top3_accuracy"
        ],
        "source_heldout_in_scope_retention": source_metrics[
            "heldout_in_scope_retention"
        ],
        "repaired_heldout_in_scope_retention": repaired_metrics[
            "heldout_in_scope_retention"
        ],
        "moved_sequence_identity_cluster_ids": sorted(moved_cluster_ids),
        "remaining_heldout_sequence_identity_cluster_overlap_count": len(split_cluster_ids),
        "remaining_heldout_sequence_identity_cluster_overlaps": split_cluster_ids,
        "sequence_identity_target_preserved_by_cluster_partition": sequence_identity_target_preserved,
        "real_sequence_identity_recomputed": False,
        "foldseek_projection_target_achieved_for_computed_subset": projection_metadata.get(
            "projected_tm_score_target_achieved_for_computed_subset"
        ),
        "foldseek_projection_max_train_test_tm_score": projection_metadata.get(
            "projected_max_observed_train_test_tm_score"
        ),
        "foldseek_projection_violating_train_test_pair_row_count": projection_metadata.get(
            "projected_violating_train_test_pair_row_count"
        ),
        "full_tm_score_holdout_claim_permitted": False,
        "full_tm_score_holdout_claim_blockers": sorted(set(claim_blockers)),
        "limitations": sorted(
            {
                "candidate holdout is a repaired copy and does not replace canonical artifacts",
                "real sequence identity search is not rerun; cluster-partition risk is checked from existing row metadata",
                "Foldseek projection uses existing capped signal rows and does not rerun Foldseek",
                "full all-materializable Foldseek/TM-score split remains uncomputed",
                "review-only artifact; it creates no countable labels and no import-ready rows",
            }
        ),
    }
    return {"metadata": metadata, "rows": candidate_rows}


def _foldseek_blocking_pair_member_key(value: Any, fallback: Any) -> str:
    if isinstance(value, str) and value:
        return value
    if isinstance(fallback, str) and fallback:
        return f"raw:{fallback}"
    return "unmapped"


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _projected_partitions_after_entry_moves(
    partitions: Any, entry_ids: list[str], moved_entry_ids: set[str]
) -> list[str]:
    if any(entry_id in moved_entry_ids for entry_id in entry_ids):
        return ["in_distribution"]
    return sorted(set(_string_list(partitions)))


def _partitions_are_train_test_pair(
    query_partitions: list[str], target_partitions: list[str]
) -> bool:
    query_set = set(query_partitions)
    target_set = set(target_partitions)
    return (
        "heldout" in query_set
        and "in_distribution" in target_set
        or "in_distribution" in query_set
        and "heldout" in target_set
    )


def _foldseek_projected_pair_summary(
    *,
    row: dict[str, Any],
    query_partitions: list[str],
    target_partitions: list[str],
    threshold: float,
) -> dict[str, Any]:
    score = _parse_optional_float(row.get("max_pair_tm_score"))
    return {
        "query_structure_key": row.get("query_structure_key"),
        "target_structure_key": row.get("target_structure_key"),
        "query_structure_id": row.get("query_structure_id"),
        "target_structure_id": row.get("target_structure_id"),
        "query_entry_ids": _string_list(row.get("query_entry_ids")),
        "target_entry_ids": _string_list(row.get("target_entry_ids")),
        "source_query_partitions": _string_list(row.get("query_partitions")),
        "source_target_partitions": _string_list(row.get("target_partitions")),
        "projected_query_partitions": query_partitions,
        "projected_target_partitions": target_partitions,
        "raw_query_name": row.get("raw_query_name"),
        "raw_target_name": row.get("raw_target_name"),
        "qtmscore": row.get("qtmscore"),
        "ttmscore": row.get("ttmscore"),
        "alntmscore": row.get("alntmscore"),
        "max_pair_tm_score": row.get("max_pair_tm_score"),
        "threshold": threshold,
        "target_operator": "<",
        "violates_target_after_projection": (
            score is not None and score >= threshold
        ),
        "projected_train_test_pair": True,
        "source_train_test_pair": bool(row.get("train_test_pair")),
        "self_pair": bool(row.get("self_pair")),
        "source_signal_line_number": row.get("line_number"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate": False,
        "import_ready": False,
    }


def _sequence_holdout_partition_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    heldout_rows = [row for row in rows if row.get("partition") == "heldout"]
    in_distribution_rows = [
        row for row in rows if row.get("partition") == "in_distribution"
    ]
    heldout_in_scope = [
        row for row in heldout_rows if row.get("label_type") != "out_of_scope"
    ]
    heldout_out_of_scope = [
        row for row in heldout_rows if row.get("label_type") == "out_of_scope"
    ]
    return {
        "heldout_count": len(heldout_rows),
        "in_distribution_count": len(in_distribution_rows),
        "heldout_in_scope_count": len(heldout_in_scope),
        "heldout_out_of_scope_count": len(heldout_out_of_scope),
        "heldout_out_of_scope_false_non_abstention_count": sum(
            1 for row in heldout_out_of_scope if not row.get("abstained")
        ),
        "heldout_in_scope_top1_accuracy": _safe_ratio(
            sum(1 for row in heldout_in_scope if row.get("top1_correct")),
            len(heldout_in_scope),
        ),
        "heldout_in_scope_top3_accuracy": _safe_ratio(
            sum(1 for row in heldout_in_scope if row.get("top3_correct")),
            len(heldout_in_scope),
        ),
        "heldout_in_scope_retention": _safe_ratio(
            sum(1 for row in heldout_in_scope if not row.get("abstained")),
            len(heldout_in_scope),
        ),
    }


def _foldseek_blocking_pair_summary(
    row: dict[str, Any], threshold: float
) -> dict[str, Any]:
    return {
        "query_structure_key": row.get("query_structure_key"),
        "target_structure_key": row.get("target_structure_key"),
        "query_structure_id": row.get("query_structure_id"),
        "target_structure_id": row.get("target_structure_id"),
        "query_entry_ids": sorted(
            [
                str(entry_id)
                for entry_id in row.get("query_entry_ids", [])
                if isinstance(entry_id, str)
            ],
            key=_entry_id_sort_key,
        ),
        "target_entry_ids": sorted(
            [
                str(entry_id)
                for entry_id in row.get("target_entry_ids", [])
                if isinstance(entry_id, str)
            ],
            key=_entry_id_sort_key,
        ),
        "query_partitions": sorted(
            [
                str(partition)
                for partition in row.get("query_partitions", [])
                if isinstance(partition, str)
            ]
        ),
        "target_partitions": sorted(
            [
                str(partition)
                for partition in row.get("target_partitions", [])
                if isinstance(partition, str)
            ]
        ),
        "raw_query_name": row.get("raw_query_name"),
        "raw_target_name": row.get("raw_target_name"),
        "qtmscore": row.get("qtmscore"),
        "ttmscore": row.get("ttmscore"),
        "alntmscore": row.get("alntmscore"),
        "max_pair_tm_score": row.get("max_pair_tm_score"),
        "threshold": threshold,
        "target_operator": "<",
        "violates_target": True,
        "train_test_pair": bool(row.get("train_test_pair")),
        "self_pair": bool(row.get("self_pair")),
        "source_signal_line_number": row.get("line_number"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate": False,
        "import_ready": False,
    }


def _evaluation_rows(
    *,
    retrieval: dict[str, Any],
    labels_by_entry: dict[str, MechanismLabel],
    geometry_by_entry: dict[str, dict[str, Any]],
    sequence_rows_by_entry: dict[str, dict[str, Any]],
    sequence_cluster_sizes: dict[str, int],
    abstain_threshold: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in retrieval.get("results", []) or []:
        if not isinstance(result, dict):
            continue
        entry_id = str(result.get("entry_id") or "")
        label = labels_by_entry.get(entry_id)
        if not entry_id or not label:
            continue
        top = [item for item in (result.get("top_fingerprints", []) or []) if isinstance(item, dict)]
        top1 = top[0] if top else {}
        top1_id = top1.get("fingerprint_id")
        top1_score = float(top1.get("score", 0.0) or 0.0)
        top3_ids = [item.get("fingerprint_id") for item in top[:3]]
        abstained = top1_score < abstain_threshold
        target_id = label.fingerprint_id
        seq_row = sequence_rows_by_entry.get(entry_id, {})
        cluster_id = str(seq_row.get("sequence_cluster_id") or "missing_sequence_cluster")
        geometry_entry = geometry_by_entry.get(entry_id, {})
        selected_structure = _selected_structure_proxy_id(result, geometry_entry)
        geometry_bucket = _active_site_geometry_proxy_bucket(result, geometry_entry)
        label_group = target_id if target_id else "out_of_scope"
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": result.get("entry_name") or geometry_entry.get("entry_name"),
                "label_type": label.label_type,
                "target_fingerprint_id": target_id,
                "label_group": label_group,
                "top1_fingerprint_id": top1_id,
                "top1_score": round(top1_score, 4),
                "top1_correct": bool(target_id and top1_id == target_id),
                "top3_correct": bool(target_id and target_id in top3_ids),
                "abstained": abstained,
                "evaluable": _is_geometry_evaluable(result),
                "status": result.get("status"),
                "resolved_residue_count": int(result.get("resolved_residue_count", 0) or 0),
                "sequence_cluster_id": cluster_id,
                "sequence_cluster_entry_count": int(sequence_cluster_sizes.get(cluster_id, 0)),
                "reference_uniprot_ids": seq_row.get("reference_uniprot_ids", []),
                "selected_structure_proxy_id": selected_structure,
                "active_site_geometry_proxy_bucket": geometry_bucket,
                "distance_proxy_note": (
                    "proxy_only_exact_reference_cluster_and_structure_context; "
                    "sequence_identity_and_tm_score_not_computed"
                ),
            }
        )
    return rows


def _sequence_cluster_indexes(
    sequence_clusters: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    rows_by_entry: dict[str, dict[str, Any]] = {}
    for row in sequence_clusters.get("rows", []) or []:
        if not isinstance(row, dict) or not isinstance(row.get("entry_id"), str):
            continue
        rows_by_entry[str(row["entry_id"])] = row
    cluster_sizes: dict[str, int] = {}
    for cluster in sequence_clusters.get("clusters", []) or []:
        if not isinstance(cluster, dict):
            continue
        cluster_id = str(cluster.get("sequence_cluster_id") or "")
        if cluster_id:
            cluster_sizes[cluster_id] = int(cluster.get("entry_count", 0) or 0)
    if not cluster_sizes:
        counts = Counter(str(row.get("sequence_cluster_id") or "") for row in rows_by_entry.values())
        cluster_sizes.update({cluster_id: count for cluster_id, count in counts.items() if cluster_id})
    return rows_by_entry, cluster_sizes


def _real_sequence_identity_split(
    *,
    rows: list[dict[str, Any]],
    sequence_rows_by_entry: dict[str, dict[str, Any]],
    sequence_fasta: str | None,
    slice_id: str,
    backend: str,
    threshold: float,
    coverage: float,
    mmseqs_binary: str,
) -> dict[str, Any]:
    if backend == "proxy":
        return _proxy_real_split_metadata(
            rows=rows,
            sequence_fasta=sequence_fasta,
            fallback_backend="deterministic_local_proxy_requested",
            limitation="sequence_identity_backend=proxy was requested",
        )
    if backend not in {"auto", "mmseqs"}:
        return _proxy_real_split_metadata(
            rows=rows,
            sequence_fasta=sequence_fasta,
            fallback_backend="deterministic_local_proxy_unsupported_backend",
            limitation=f"unsupported sequence identity backend: {backend}",
        )

    mmseqs_path = shutil.which(mmseqs_binary)
    if not mmseqs_path:
        return _proxy_real_split_metadata(
            rows=rows,
            sequence_fasta=sequence_fasta,
            fallback_backend="deterministic_local_proxy_mmseqs2_unavailable",
            limitation=f"MMseqs2 binary not found: {mmseqs_binary}",
        )

    collected = _collect_sequence_records(
        rows=rows,
        sequence_rows_by_entry=sequence_rows_by_entry,
        sequence_fasta=sequence_fasta,
    )
    if len(collected["records_by_id"]) < 2:
        return _proxy_real_split_metadata(
            rows=rows,
            sequence_fasta=sequence_fasta,
            fallback_backend="deterministic_local_proxy_insufficient_sequences",
            limitation="fewer than two amino-acid sequence records were available",
            collected=collected,
        )

    digest = _sequence_records_digest(collected["records_by_id"])
    workdir = Path("/private/tmp") / f"catalytic-earth-mmseqs-{slice_id}-{digest}"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    commands: list[str] = []
    try:
        input_fasta = workdir / "input.fasta"
        seqdb = workdir / "seqdb"
        cluster_db = workdir / "clusterdb"
        cluster_tmp = workdir / "cluster_tmp"
        clusters_tsv = workdir / "clusters.tsv"
        _write_sequence_records_fasta(input_fasta, collected["records_by_id"])
        createdb_cmd = [mmseqs_path, "createdb", str(input_fasta), str(seqdb)]
        cluster_cmd = [
            mmseqs_path,
            "cluster",
            str(seqdb),
            str(cluster_db),
            str(cluster_tmp),
            "--min-seq-id",
            _mmseqs_float(threshold),
            "-c",
            _mmseqs_float(coverage),
            "--cov-mode",
            str(MMSEQS_CLUSTER_COVERAGE_MODE),
            "--threads",
            "1",
        ]
        createtsv_cmd = [
            mmseqs_path,
            "createtsv",
            str(seqdb),
            str(seqdb),
            str(cluster_db),
            str(clusters_tsv),
        ]
        for command in (createdb_cmd, cluster_cmd, createtsv_cmd):
            _run_backend_command(command, cwd=workdir)
            commands.append(_command_string(command))
        record_clusters = _parse_mmseqs_cluster_tsv(clusters_tsv)
        entry_clusters = _entry_clusters_from_record_clusters(
            record_clusters=record_clusters,
            records_by_id=collected["records_by_id"],
        )
        return {
            "usable": True,
            "backend_command": _command_string(cluster_cmd),
            "backend_commands": commands,
            "backend_resolved_path": mmseqs_path,
            "backend_version": _backend_version(mmseqs_path),
            "records_by_id": collected["records_by_id"],
            "sequence_source": collected["sequence_source"],
            "sequence_count": len(collected["records_by_id"]),
            "sequence_entry_coverage_count": len(collected["entries_with_sequence"]),
            "sequence_missing_entry_count": len(collected["missing_entry_ids"]),
            "sequence_missing_entry_ids": collected["missing_entry_ids"],
            "entries_with_sequence": collected["entries_with_sequence"],
            "sequence_record_counts_by_entry": collected[
                "sequence_record_counts_by_entry"
            ],
            "sequence_accessions_by_entry": collected["sequence_accessions_by_entry"],
            "record_cluster_count": len(record_clusters),
            "entry_cluster_count": len(set(entry_clusters.values())),
            "entry_clusters": entry_clusters,
            "limitations": collected["limitations"],
        }
    except (OSError, RuntimeError, ValueError) as exc:
        collected["limitations"].append(f"MMseqs2 clustering failed: {exc}")
        return _proxy_real_split_metadata(
            rows=rows,
            sequence_fasta=sequence_fasta,
            fallback_backend="deterministic_local_proxy_mmseqs2_failed",
            limitation=f"MMseqs2 clustering failed: {exc}",
            collected=collected,
        )


def _proxy_real_split_metadata(
    *,
    rows: list[dict[str, Any]],
    sequence_fasta: str | None,
    fallback_backend: str,
    limitation: str,
    collected: dict[str, Any] | None = None,
) -> dict[str, Any]:
    collected = collected or {
        "records_by_id": {},
        "sequence_source": _sequence_source_description(sequence_fasta, None),
        "entries_with_sequence": set(),
        "missing_entry_ids": sorted(
            (str(row["entry_id"]) for row in rows),
            key=_entry_id_sort_key,
        ),
        "sequence_record_counts_by_entry": {},
        "sequence_accessions_by_entry": {},
        "limitations": [],
    }
    limitations = list(collected.get("limitations", []))
    if limitation not in limitations:
        limitations.append(limitation)
    return {
        "usable": False,
        "fallback_backend": fallback_backend,
        "backend_command": None,
        "backend_commands": [],
        "backend_resolved_path": None,
        "backend_version": None,
        "records_by_id": collected.get("records_by_id", {}),
        "sequence_source": collected.get(
            "sequence_source", _sequence_source_description(sequence_fasta, None)
        ),
        "sequence_count": len(collected.get("records_by_id", {})),
        "sequence_entry_coverage_count": len(
            collected.get("entries_with_sequence", set())
        ),
        "sequence_missing_entry_count": len(collected.get("missing_entry_ids", [])),
        "sequence_missing_entry_ids": collected.get("missing_entry_ids", []),
        "entries_with_sequence": collected.get("entries_with_sequence", set()),
        "sequence_record_counts_by_entry": collected.get(
            "sequence_record_counts_by_entry", {}
        ),
        "sequence_accessions_by_entry": collected.get(
            "sequence_accessions_by_entry", {}
        ),
        "record_cluster_count": None,
        "entry_cluster_count": None,
        "entry_clusters": {},
        "limitations": limitations,
    }


def _collect_sequence_records(
    *,
    rows: list[dict[str, Any]],
    sequence_rows_by_entry: dict[str, dict[str, Any]],
    sequence_fasta: str | None,
) -> dict[str, Any]:
    fasta_records = _load_fasta_records(Path(sequence_fasta)) if sequence_fasta else None
    fasta_by_accession: dict[str, str] = {}
    fasta_by_entry: dict[str, str] = {}
    if fasta_records:
        for record in fasta_records:
            sequence = str(record["sequence"])
            for accession in record["accessions"]:
                fasta_by_accession.setdefault(accession, sequence)
            for entry_id in record["entry_ids"]:
                fasta_by_entry.setdefault(entry_id, sequence)

    records_by_id: dict[str, dict[str, Any]] = {}
    entries_with_sequence: set[str] = set()
    record_counts_by_entry: Counter[str] = Counter()
    accessions_by_entry: dict[str, set[str]] = defaultdict(set)
    limitations: list[str] = []
    if fasta_records:
        fallback_count = sum(
            1
            for record in fasta_records
            if "fallback_for_uniprot:" in str(record.get("header", ""))
        )
        if fallback_count:
            limitations.append(
                f"{fallback_count} FASTA records use selected-PDB sequence fallbacks for unavailable UniProt accessions"
            )

    for row in rows:
        entry_id = str(row["entry_id"])
        reference_accessions = [
            str(accession)
            for accession in row.get("reference_uniprot_ids", []) or []
            if accession
        ]
        row_sequence = _sequence_from_row(sequence_rows_by_entry.get(entry_id, {}))
        if row_sequence:
            accession = reference_accessions[0] if reference_accessions else None
            record_id = _sequence_record_id(entry_id, accession or "row_sequence")
            records_by_id[record_id] = {
                "record_id": record_id,
                "entry_id": entry_id,
                "accession": accession,
                "sequence": row_sequence,
                "source": "sequence_cluster_row",
            }
        for accession in reference_accessions:
            sequence = fasta_by_accession.get(accession)
            if not sequence:
                continue
            record_id = _sequence_record_id(entry_id, accession)
            records_by_id[record_id] = {
                "record_id": record_id,
                "entry_id": entry_id,
                "accession": accession,
                "sequence": sequence,
                "source": "fasta_reference_uniprot_accession",
            }
        if entry_id not in {
            str(record["entry_id"]) for record in records_by_id.values()
        }:
            sequence = fasta_by_entry.get(entry_id)
            if sequence:
                record_id = _sequence_record_id(entry_id, "entry_fasta")
                records_by_id[record_id] = {
                    "record_id": record_id,
                    "entry_id": entry_id,
                    "accession": None,
                    "sequence": sequence,
                    "source": "fasta_entry_id",
                }

    for record in records_by_id.values():
        entry_id = str(record["entry_id"])
        entries_with_sequence.add(entry_id)
        record_counts_by_entry[entry_id] += 1
        if record.get("accession"):
            accessions_by_entry[entry_id].add(str(record["accession"]))

    missing_entry_ids = sorted(
        (
            str(row["entry_id"])
            for row in rows
            if str(row["entry_id"]) not in entries_with_sequence
        ),
        key=_entry_id_sort_key,
    )
    if missing_entry_ids:
        limitations.append(
            "real sequence identity is unavailable for rows without amino-acid sequence records"
        )
    if fasta_records is None and not any(
        _sequence_from_row(sequence_rows_by_entry.get(str(row["entry_id"]), {}))
        for row in rows
    ):
        limitations.append(
            "no FASTA was supplied and sequence cluster rows do not contain amino-acid sequences"
        )

    return {
        "records_by_id": dict(sorted(records_by_id.items())),
        "sequence_source": _sequence_source_description(sequence_fasta, fasta_records),
        "entries_with_sequence": entries_with_sequence,
        "missing_entry_ids": missing_entry_ids,
        "sequence_record_counts_by_entry": {
            entry_id: int(count)
            for entry_id, count in sorted(record_counts_by_entry.items())
        },
        "sequence_accessions_by_entry": {
            entry_id: sorted(accessions)
            for entry_id, accessions in sorted(accessions_by_entry.items())
        },
        "limitations": limitations,
    }


def _sequence_from_row(row: dict[str, Any]) -> str | None:
    for field_name in SEQUENCE_FIELD_NAMES:
        sequence = _normalise_sequence(row.get(field_name))
        if sequence:
            return sequence
    return None


def _load_fasta_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        raise ValueError(f"sequence FASTA does not exist: {path}")
    header: str | None = None
    sequence_lines: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    _append_fasta_record(records, header, sequence_lines)
                header = line[1:].strip()
                sequence_lines = []
            else:
                sequence_lines.append(line)
    if header is not None:
        _append_fasta_record(records, header, sequence_lines)
    return records


def _append_fasta_record(
    records: list[dict[str, Any]], header: str, sequence_lines: list[str]
) -> None:
    sequence = _normalise_sequence("".join(sequence_lines))
    if not sequence:
        return
    records.append(
        {
            "header": header,
            "sequence": sequence,
            "accessions": _fasta_header_accessions(header),
            "entry_ids": _fasta_header_entry_ids(header),
        }
    )


def _fasta_header_accessions(header: str) -> list[str]:
    accessions: set[str] = set()
    pipe_match = re.match(r"^(?:sp|tr)\|([A-Za-z0-9]+)\|", header)
    if pipe_match:
        accessions.add(pipe_match.group(1))
    for token in re.split(r"[\s|,;]+", header):
        if re.fullmatch(r"[A-Z][A-Z0-9]{5,9}", token):
            accessions.add(token)
    return sorted(accessions)


def _fasta_header_entry_ids(header: str) -> list[str]:
    return sorted(set(re.findall(r"m_csa:\d+", header)), key=_entry_id_sort_key)


def _normalise_sequence(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    sequence = re.sub(r"[^A-Za-z]", "", value).upper()
    return sequence or None


def _sequence_source_description(
    sequence_fasta: str | None, fasta_records: list[dict[str, Any]] | None
) -> str:
    if sequence_fasta:
        record_count = len(fasta_records or [])
        return f"fasta:{sequence_fasta}; records={record_count}"
    return "sequence_cluster_rows"


def _sequence_record_id(entry_id: str, accession: str) -> str:
    safe_entry = re.sub(r"[^A-Za-z0-9]+", "_", entry_id).strip("_")
    safe_accession = re.sub(r"[^A-Za-z0-9]+", "_", accession).strip("_")
    return f"{safe_entry}__{safe_accession}"


def _sequence_records_digest(records_by_id: dict[str, dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record_id, record in sorted(records_by_id.items()):
        digest.update(record_id.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["sequence"]).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()[:12]


def _write_sequence_records_fasta(
    path: Path, records_by_id: dict[str, dict[str, Any]]
) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record_id, record in sorted(records_by_id.items()):
            handle.write(f">{record_id}\n")
            sequence = str(record["sequence"])
            for start in range(0, len(sequence), 80):
                handle.write(sequence[start : start + 80] + "\n")


def _parse_mmseqs_cluster_tsv(path: Path) -> dict[str, set[str]]:
    clusters: dict[str, set[str]] = defaultdict(set)
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            fields = raw_line.rstrip("\n").split("\t")
            if len(fields) < 2:
                continue
            representative, member = fields[0], fields[1]
            clusters[representative].add(representative)
            clusters[representative].add(member)
    return {cluster_id: members for cluster_id, members in sorted(clusters.items())}


def _entry_clusters_from_record_clusters(
    *,
    record_clusters: dict[str, set[str]],
    records_by_id: dict[str, dict[str, Any]],
) -> dict[str, str]:
    parent: dict[str, str] = {}

    def find(entry_id: str) -> str:
        parent.setdefault(entry_id, entry_id)
        if parent[entry_id] != entry_id:
            parent[entry_id] = find(parent[entry_id])
        return parent[entry_id]

    def union(a: str, b: str) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a == root_b:
            return
        winner, loser = sorted([root_a, root_b], key=_entry_id_sort_key)
        parent[loser] = winner

    for record in records_by_id.values():
        find(str(record["entry_id"]))
    for members in record_clusters.values():
        member_entries = sorted(
            {
                str(records_by_id[record_id]["entry_id"])
                for record_id in members
                if record_id in records_by_id
            },
            key=_entry_id_sort_key,
        )
        if not member_entries:
            continue
        first = member_entries[0]
        for entry_id in member_entries[1:]:
            union(first, entry_id)

    root_members: dict[str, list[str]] = defaultdict(list)
    for record in records_by_id.values():
        entry_id = str(record["entry_id"])
        root_members[find(entry_id)].append(entry_id)
    cluster_id_by_root: dict[str, str] = {}
    for root, members in root_members.items():
        canonical = sorted(set(members), key=_entry_id_sort_key)[0]
        cluster_id_by_root[root] = f"mmseqs30:{canonical}"
    return {
        entry_id: cluster_id_by_root[find(entry_id)]
        for entry_id in sorted(root_members, key=_entry_id_sort_key)
    } | {
        str(record["entry_id"]): cluster_id_by_root[find(str(record["entry_id"]))]
        for record in records_by_id.values()
    }


def _select_holdout_entry_ids_by_real_clusters(
    rows: list[dict[str, Any]],
    *,
    entry_clusters: dict[str, str],
    holdout_fraction: float,
    min_holdout_rows: int,
) -> tuple[set[str], list[str]]:
    if not rows:
        return set(), ["no_evaluation_rows_available"]
    target_total = min(
        len(rows),
        max(min_holdout_rows, round(len(rows) * holdout_fraction)),
    )
    rows_by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        entry_id = str(row["entry_id"])
        cluster_id = entry_clusters.get(entry_id, f"missing_sequence:{entry_id}")
        rows_by_cluster[cluster_id].append(row)

    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[str(row.get("label_group") or "unknown")].append(row)
    group_targets: dict[str, int] = {}
    for group, group_rows in sorted(by_group.items()):
        if len(group_rows) == 1:
            group_targets[group] = 1 if target_total >= len(by_group) else 0
        else:
            group_targets[group] = max(1, round(len(group_rows) * holdout_fraction))

    while sum(group_targets.values()) > target_total:
        reducible = [group for group, count in group_targets.items() if count > 1]
        if not reducible:
            break
        largest = max(
            reducible,
            key=lambda group: (group_targets[group], len(by_group[group]), group),
        )
        group_targets[largest] -= 1

    selected_clusters: set[str] = set()
    heldout_ids: set[str] = set()
    notes: list[str] = []
    for group, target in sorted(group_targets.items()):
        if target <= 0:
            continue
        group_heldout = 0
        candidate_clusters = [
            cluster_id
            for cluster_id, cluster_rows in rows_by_cluster.items()
            if cluster_id not in selected_clusters
            and any(str(row.get("label_group") or "unknown") == group for row in cluster_rows)
        ]
        for cluster_id in sorted(
            candidate_clusters,
            key=lambda cluster_id: _real_cluster_rank_key(cluster_id, rows_by_cluster[cluster_id]),
        ):
            if group_heldout >= target:
                break
            selected_clusters.add(cluster_id)
            cluster_ids = {str(row["entry_id"]) for row in rows_by_cluster[cluster_id]}
            heldout_ids.update(cluster_ids)
            group_heldout += sum(
                1
                for row in rows_by_cluster[cluster_id]
                if str(row.get("label_group") or "unknown") == group
            )
        if group_heldout < target:
            notes.append(
                f"{group}: sequence cluster units exhausted before group target {target}"
            )

    if len(heldout_ids) < target_total:
        remaining_clusters = [
            cluster_id
            for cluster_id in rows_by_cluster
            if cluster_id not in selected_clusters
        ]
        for cluster_id in sorted(
            remaining_clusters,
            key=lambda cluster_id: _real_cluster_rank_key(cluster_id, rows_by_cluster[cluster_id]),
        ):
            if len(heldout_ids) >= target_total:
                break
            selected_clusters.add(cluster_id)
            heldout_ids.update(str(row["entry_id"]) for row in rows_by_cluster[cluster_id])

    if len(heldout_ids) > target_total:
        notes.append(
            "heldout row count exceeds nominal target because sequence clusters are indivisible"
        )
    notes.append(
        "real sequence split selected whole MMseqs2 clusters; proxy low-neighborhood scores only rank candidate clusters"
    )
    return heldout_ids, notes


def _real_cluster_rank_key(cluster_id: str, rows: list[dict[str, Any]]) -> tuple[float, int, str, str]:
    average_proxy_score = sum(
        float(row.get("low_neighborhood_proxy_score", 0.0) or 0.0) for row in rows
    ) / max(len(rows), 1)
    payload = "|".join(sorted(str(row.get("entry_id") or "") for row in rows))
    return (
        -average_proxy_score,
        len(rows),
        hashlib.sha256((cluster_id + "|" + payload).encode("utf-8")).hexdigest(),
        cluster_id,
    )


def _empty_train_test_identity_metadata() -> dict[str, Any]:
    return {
        "max_observed_train_test_identity": None,
        "max_observed_train_test_identity_computable": False,
        "max_observed_train_test_identity_alignment_count": 0,
        "backend_commands": [],
        "limitations": [],
    }


def _compute_mmseqs_train_test_identity(
    *,
    records_by_id: dict[str, dict[str, Any]],
    heldout_entry_ids: set[str],
    slice_id: str,
    threshold: float,
    coverage: float,
    mmseqs_binary: str,
    prior_commands: list[str],
) -> dict[str, Any]:
    mmseqs_path = shutil.which(mmseqs_binary)
    if not mmseqs_path:
        return {
            **_empty_train_test_identity_metadata(),
            "limitations": [f"MMseqs2 binary not found: {mmseqs_binary}"],
            "backend_commands": prior_commands,
        }
    heldout_records = {
        record_id: record
        for record_id, record in records_by_id.items()
        if str(record["entry_id"]) in heldout_entry_ids
    }
    train_records = {
        record_id: record
        for record_id, record in records_by_id.items()
        if str(record["entry_id"]) not in heldout_entry_ids
    }
    if not heldout_records or not train_records:
        return {
            **_empty_train_test_identity_metadata(),
            "limitations": [
                "train/test identity search requires at least one train and one heldout sequence"
            ],
            "backend_commands": prior_commands,
        }
    digest = _sequence_records_digest(records_by_id) + "-" + _ids_digest(heldout_entry_ids)
    workdir = Path("/private/tmp") / f"catalytic-earth-mmseqs-search-{slice_id}-{digest}"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    commands = list(prior_commands)
    try:
        heldout_fasta = workdir / "heldout.fasta"
        train_fasta = workdir / "train.fasta"
        result_tsv = workdir / "train_test_identity.tsv"
        search_tmp = workdir / "search_tmp"
        _write_sequence_records_fasta(heldout_fasta, heldout_records)
        _write_sequence_records_fasta(train_fasta, train_records)
        search_cmd = [
            mmseqs_path,
            "easy-search",
            str(heldout_fasta),
            str(train_fasta),
            str(result_tsv),
            str(search_tmp),
            "--format-output",
            "query,target,pident,alnlen,qcov,tcov,evalue,bits",
            "--min-seq-id",
            "0.0",
            "-c",
            _mmseqs_float(coverage),
            "--cov-mode",
            str(MMSEQS_CLUSTER_COVERAGE_MODE),
            "--threads",
            "1",
        ]
        _run_backend_command(search_cmd, cwd=workdir)
        commands.append(_command_string(search_cmd))
        max_identity: float | None = None
        alignment_count = 0
        if result_tsv.exists():
            with result_tsv.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    fields = raw_line.rstrip("\n").split("\t")
                    if len(fields) < 3:
                        continue
                    try:
                        identity = float(fields[2]) / 100.0
                    except ValueError:
                        continue
                    alignment_count += 1
                    max_identity = (
                        identity
                        if max_identity is None
                        else max(max_identity, identity)
                    )
        return {
            "max_observed_train_test_identity": (
                round(max_identity, 4) if max_identity is not None else None
            ),
            "max_observed_train_test_identity_computable": True,
            "max_observed_train_test_identity_alignment_count": alignment_count,
            "backend_commands": commands,
            "limitations": [
                "MMseqs2 easy-search reports heuristic local alignments at the configured coverage; it is not an exhaustive Smith-Waterman all-vs-all matrix"
            ],
        }
    except (OSError, RuntimeError, ValueError) as exc:
        return {
            **_empty_train_test_identity_metadata(),
            "limitations": [f"MMseqs2 train/test identity search failed: {exc}"],
            "backend_commands": commands,
        }


def _sequence_identity_target_achieved(
    *,
    real_split: dict[str, Any],
    train_test_identity: dict[str, Any],
    threshold: float,
) -> bool:
    if not real_split.get("usable"):
        return False
    if int(real_split.get("sequence_missing_entry_count", 0) or 0) > 0:
        return False
    if not train_test_identity.get("max_observed_train_test_identity_computable"):
        return False
    max_identity = train_test_identity.get("max_observed_train_test_identity")
    return max_identity is None or float(max_identity) <= threshold


def _sequence_identity_limitations(
    *,
    real_split: dict[str, Any],
    train_test_identity: dict[str, Any],
    sequence_identity_threshold: float,
) -> list[str]:
    limitations = []
    limitations.extend(str(item) for item in real_split.get("limitations", []) or [])
    limitations.extend(
        str(item) for item in train_test_identity.get("limitations", []) or []
    )
    if real_split.get("usable"):
        limitations.append(
            "sequence-distance partitioning supersedes proxy cluster selection, but fold/TM-score distance is still not computed"
        )
        limitations.append(
            f"MMseqs2 clustering threshold is {sequence_identity_threshold:.2f}; connected clusters can hide within-cluster diversity and are not taxonomic or structural families"
        )
    else:
        limitations.append(
            "deterministic proxy partition is retained because real sequence identity was not computed"
        )
    return sorted(set(limitations))


def _partition_rule(real_split: dict[str, Any]) -> str:
    if real_split.get("usable"):
        return (
            "deterministic holdout by whole MMseqs2 sequence clusters at the "
            "configured identity threshold; label/fingerprint stratification is "
            "attempted by cluster units, and sequence separation takes precedence"
        )
    return (
        "stratified deterministic proxy holdout by label/fingerprint group, "
        "prioritizing singleton exact UniProt reference clusters, singleton "
        "selected structures, and rare active-site geometry proxy buckets"
    )


def _ids_digest(ids: set[str]) -> str:
    return hashlib.sha256("|".join(sorted(ids, key=_entry_id_sort_key)).encode("utf-8")).hexdigest()[:12]


def _run_backend_command(
    command: list[str], *, cwd: Path, timeout: int | None = None
) -> None:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(
            f"{_command_string(command)} exceeded {timeout} seconds"
        ) from exc
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"{_command_string(command)} failed with exit code {completed.returncode}: {stderr[:1000]}"
        )


def _staged_foldseek_structures(structures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    staged = []
    for structure in structures:
        coordinate_path = structure.get("coordinate_path")
        if not isinstance(coordinate_path, str) or not coordinate_path:
            continue
        path = Path(coordinate_path)
        if not path.exists() or not path.is_file():
            continue
        staged.append(
            {
                **structure,
                "coordinate_path": str(path),
                "entry_ids": [
                    str(entry_id)
                    for entry_id in structure.get("entry_ids", []) or []
                    if isinstance(entry_id, str)
                ],
            }
        )
    return sorted(
        staged,
        key=lambda item: (
            _entry_id_sort_key(str((item.get("entry_ids") or [""])[0])),
            str(item.get("structure_key") or ""),
        ),
    )


def _foldseek_name_aliases(
    staged_structures: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    aliases: dict[str, dict[str, Any]] = {}
    collisions: dict[str, list[str]] = defaultdict(list)
    for structure in staged_structures:
        coordinate_path = Path(str(structure.get("coordinate_path") or ""))
        raw_aliases = {
            str(coordinate_path),
            coordinate_path.name,
            coordinate_path.stem,
            *_foldseek_structure_metadata_aliases(structure),
        }
        for alias in sorted(raw_aliases):
            if not alias:
                continue
            existing = aliases.get(alias)
            if existing and existing.get("structure_key") != structure.get("structure_key"):
                collisions[alias].extend(
                    [
                        str(existing.get("structure_key")),
                        str(structure.get("structure_key")),
                    ]
                )
                aliases.pop(alias, None)
                continue
            if alias not in collisions:
                aliases[alias] = structure
    return aliases, [
        {"alias": alias, "structure_keys": sorted(set(keys))}
        for alias, keys in sorted(collisions.items())
    ]


def _foldseek_structure_metadata_aliases(structure: dict[str, Any]) -> set[str]:
    aliases: set[str] = set()
    structure_id = str(structure.get("structure_id") or "").strip()
    if structure_id:
        aliases.add(structure_id)
        aliases.add(structure_id.upper())
    structure_key = str(structure.get("structure_key") or "").strip()
    if structure_key:
        aliases.add(structure_key)
        if ":" in structure_key:
            source, source_id = structure_key.split(":", 1)
            source = source.strip()
            source_id = source_id.strip()
            if source_id:
                aliases.add(source_id)
                aliases.add(source_id.upper())
                if source.lower() == "pdb":
                    aliases.add(f"pdb_{source_id}")
                    aliases.add(f"pdb_{source_id.upper()}")
    source = str(structure.get("source") or "").strip()
    if source.lower() == "pdb" and structure_id:
        aliases.add(f"pdb_{structure_id}")
        aliases.add(f"pdb_{structure_id.upper()}")
    return {alias for alias in aliases if alias}


def _coordinate_paths_digest(staged_structures: list[dict[str, Any]]) -> str:
    paths = [
        str(structure.get("coordinate_path") or "")
        for structure in staged_structures
        if structure.get("coordinate_path")
    ]
    return hashlib.sha256("|".join(sorted(paths)).encode("utf-8")).hexdigest()[:12]


def _empty_foldseek_tm_score_pair_summary() -> dict[str, Any]:
    return {
        "pair_count": 0,
        "mapped_pair_count": 0,
        "parse_error_count": 0,
        "train_test_pair_count": 0,
        "heldout_in_distribution_pair_count": 0,
        "heldout_pair_count": 0,
        "in_distribution_pair_count": 0,
        "other_partition_pair_count": 0,
        "unique_unordered_nonself_pair_count": 0,
        "max_observed_train_test_tm_score": None,
        "max_observed_train_test_tm_score_computable": False,
        "max_observed_train_test_tm_score_metric": (
            "max(qtmscore, ttmscore, alntmscore) across mapped heldout/in_distribution staged-coordinate pairs"
        ),
        "violating_train_test_pair_row_count": 0,
        "violating_unique_structure_pair_count": 0,
        "violating_unique_entry_pair_count": 0,
        "raw_name_mapping_unmapped_count": 0,
        "raw_name_mapping_unmapped_names": [],
        "top_train_test_pairs": [],
        "blocking_pairs": [],
    }


def _summarize_foldseek_tm_score_rows(
    *,
    result_tsv: Path,
    alias_to_structure: dict[str, dict[str, Any]],
    row_partitions_by_entry: dict[str, Any],
    threshold: float,
    max_reported_rows: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    summary = _summarize_foldseek_tm_score_tsv(
        result_tsv=result_tsv,
        alias_to_structure=alias_to_structure,
        row_partitions_by_entry=row_partitions_by_entry,
        threshold=threshold,
        max_reported_pairs=max_reported_rows,
    )
    retained_rows_by_key: dict[tuple[Any, Any, Any], dict[str, Any]] = {}
    for row in summary["top_train_test_pairs"] + summary["blocking_pairs"]:
        retained_rows_by_key[
            (
                row.get("raw_query_name"),
                row.get("raw_target_name"),
                row.get("source_signal_line_number"),
            )
        ] = row
    compatible_summary = {
        "pair_count": summary["pair_count"],
        "mapped_pair_count": summary["mapped_pair_count"],
        "train_test_pair_count": summary["train_test_pair_count"],
        "heldout_in_distribution_pair_count": summary[
            "heldout_in_distribution_pair_count"
        ],
        "heldout_pair_count": summary["heldout_pair_count"],
        "in_distribution_pair_count": summary["in_distribution_pair_count"],
        "other_partition_pair_count": summary["other_partition_pair_count"],
        "unique_unordered_nonself_pair_count": summary[
            "unique_unordered_nonself_pair_count"
        ],
        "max_train_test_tm_score": summary["max_observed_train_test_tm_score"],
        "unmapped_names": summary["raw_name_mapping_unmapped_names"],
        "target_violating_train_test_pair_row_count": summary[
            "violating_train_test_pair_row_count"
        ],
    }
    return list(retained_rows_by_key.values()), compatible_summary


def _summarize_foldseek_tm_score_tsv(
    *,
    result_tsv: Path,
    alias_to_structure: dict[str, dict[str, Any]],
    row_partitions_by_entry: dict[str, Any],
    threshold: float,
    max_reported_pairs: int,
) -> dict[str, Any]:
    if not result_tsv.exists():
        raise ValueError(f"Foldseek result TSV was not created: {result_tsv}")

    summary = _empty_foldseek_tm_score_pair_summary()
    unique_nonself_pairs: set[tuple[str, str]] = set()
    raw_unmapped_names: set[str] = set()
    top_train_test_pairs: list[dict[str, Any]] = []
    blocking_by_structure_pair: dict[tuple[str, str], dict[str, Any]] = {}
    violating_entry_pairs: set[tuple[str, str]] = set()
    reported_limit = max(1, int(max_reported_pairs))

    with result_tsv.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if fields[:5] == ["query", "target", "qtmscore", "ttmscore", "alntmscore"]:
                continue
            if len(fields) < 5:
                summary["parse_error_count"] += 1
                if fields:
                    raw_unmapped_names.add(fields[0])
                if len(fields) > 1:
                    raw_unmapped_names.add(fields[1])
                continue
            query_raw, target_raw = fields[0], fields[1]
            query_structure, query_status = _map_foldseek_raw_name(
                query_raw, alias_to_structure
            )
            target_structure, target_status = _map_foldseek_raw_name(
                target_raw, alias_to_structure
            )
            query_entry_ids = _structure_entry_ids(query_structure)
            target_entry_ids = _structure_entry_ids(target_structure)
            query_partitions = sorted(
                {
                    str(row_partitions_by_entry.get(entry_id))
                    for entry_id in query_entry_ids
                    if row_partitions_by_entry.get(entry_id) is not None
                }
            )
            target_partitions = sorted(
                {
                    str(row_partitions_by_entry.get(entry_id))
                    for entry_id in target_entry_ids
                    if row_partitions_by_entry.get(entry_id) is not None
                }
            )
            qtmscore = _parse_optional_float(fields[2])
            ttmscore = _parse_optional_float(fields[3])
            alntmscore = _parse_optional_float(fields[4])
            max_pair_tm_score = _max_optional_float([qtmscore, ttmscore, alntmscore])
            row = {
                "line_number": line_number,
                "raw_query_name": query_raw,
                "raw_target_name": target_raw,
                "query_name_mapping_status": query_status,
                "target_name_mapping_status": target_status,
                "query_structure_key": (
                    query_structure.get("structure_key") if query_structure else None
                ),
                "target_structure_key": (
                    target_structure.get("structure_key") if target_structure else None
                ),
                "query_structure_id": (
                    query_structure.get("structure_id") if query_structure else None
                ),
                "target_structure_id": (
                    target_structure.get("structure_id") if target_structure else None
                ),
                "query_entry_ids": query_entry_ids,
                "target_entry_ids": target_entry_ids,
                "query_partitions": query_partitions,
                "target_partitions": target_partitions,
                "qtmscore": qtmscore,
                "ttmscore": ttmscore,
                "alntmscore": alntmscore,
                "max_pair_tm_score": max_pair_tm_score,
                "self_pair": bool(
                    query_structure
                    and target_structure
                    and query_structure.get("structure_key")
                    == target_structure.get("structure_key")
                ),
                "train_test_pair": _is_train_test_partition_pair(
                    query_partitions, target_partitions
                ),
            }
            summary["pair_count"] += 1
            if row["query_structure_key"] and row["target_structure_key"]:
                summary["mapped_pair_count"] += 1
            if not row["query_structure_key"]:
                raw_unmapped_names.add(query_raw)
            if not row["target_structure_key"]:
                raw_unmapped_names.add(target_raw)
            query_key = row["query_structure_key"] or f"raw:{query_raw}"
            target_key = row["target_structure_key"] or f"raw:{target_raw}"
            if query_key != target_key:
                unique_nonself_pairs.add(tuple(sorted([str(query_key), str(target_key)])))

            partitions = set(query_partitions) | set(target_partitions)
            if "heldout" in partitions and "in_distribution" in partitions:
                summary["heldout_in_distribution_pair_count"] += 1
            elif partitions == {"heldout"}:
                summary["heldout_pair_count"] += 1
            elif partitions == {"in_distribution"}:
                summary["in_distribution_pair_count"] += 1
            else:
                summary["other_partition_pair_count"] += 1

            if not row["train_test_pair"]:
                continue
            summary["train_test_pair_count"] += 1
            score = _parse_optional_float(max_pair_tm_score)
            if score is None:
                continue
            current_max = summary["max_observed_train_test_tm_score"]
            summary["max_observed_train_test_tm_score"] = (
                score if current_max is None else max(float(current_max), score)
            )
            top_train_test_pairs.append(_foldseek_train_test_pair_summary(row, threshold))
            top_train_test_pairs.sort(
                key=lambda item: (
                    -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
                    str(item.get("query_structure_key") or ""),
                    str(item.get("target_structure_key") or ""),
                )
            )
            del top_train_test_pairs[reported_limit:]
            if score < threshold:
                continue
            summary["violating_train_test_pair_row_count"] += 1
            query_pair_key = _foldseek_blocking_pair_member_key(
                row.get("query_structure_key"), row.get("raw_query_name")
            )
            target_pair_key = _foldseek_blocking_pair_member_key(
                row.get("target_structure_key"), row.get("raw_target_name")
            )
            structure_pair_key = tuple(sorted([query_pair_key, target_pair_key]))
            existing = blocking_by_structure_pair.get(structure_pair_key)
            if existing is None or (
                _parse_optional_float(row.get("max_pair_tm_score")) or 0.0
            ) > (_parse_optional_float(existing.get("max_pair_tm_score")) or 0.0):
                blocking_by_structure_pair[structure_pair_key] = row
            for query_entry_id in query_entry_ids or ["unmapped_query"]:
                for target_entry_id in target_entry_ids or ["unmapped_target"]:
                    if query_entry_id == target_entry_id:
                        continue
                    violating_entry_pairs.add(
                        tuple(sorted([str(query_entry_id), str(target_entry_id)]))
                    )

    blocking_pairs = [
        _foldseek_blocking_pair_summary(row, threshold)
        for row in blocking_by_structure_pair.values()
    ]
    blocking_pairs.sort(
        key=lambda item: (
            -(_parse_optional_float(item.get("max_pair_tm_score")) or 0.0),
            str(item.get("query_structure_key") or ""),
            str(item.get("target_structure_key") or ""),
        )
    )
    summary["max_observed_train_test_tm_score"] = (
        round(float(summary["max_observed_train_test_tm_score"]), 4)
        if summary["max_observed_train_test_tm_score"] is not None
        else None
    )
    summary["max_observed_train_test_tm_score_computable"] = (
        summary["max_observed_train_test_tm_score"] is not None
    )
    summary["unique_unordered_nonself_pair_count"] = len(unique_nonself_pairs)
    summary["violating_unique_structure_pair_count"] = len(blocking_by_structure_pair)
    summary["violating_unique_entry_pair_count"] = len(violating_entry_pairs)
    summary["raw_name_mapping_unmapped_count"] = len(raw_unmapped_names)
    summary["raw_name_mapping_unmapped_names"] = sorted(raw_unmapped_names)
    summary["top_train_test_pairs"] = top_train_test_pairs
    summary["blocking_pairs"] = blocking_pairs[:reported_limit]
    return summary


def _foldseek_train_test_pair_summary(
    row: dict[str, Any], threshold: float
) -> dict[str, Any]:
    score = _parse_optional_float(row.get("max_pair_tm_score"))
    return {
        "query_structure_key": row.get("query_structure_key"),
        "target_structure_key": row.get("target_structure_key"),
        "query_structure_id": row.get("query_structure_id"),
        "target_structure_id": row.get("target_structure_id"),
        "query_entry_ids": _structure_entry_ids_from_row(row, "query_entry_ids"),
        "target_entry_ids": _structure_entry_ids_from_row(row, "target_entry_ids"),
        "query_partitions": _string_list(row.get("query_partitions")),
        "target_partitions": _string_list(row.get("target_partitions")),
        "raw_query_name": row.get("raw_query_name"),
        "raw_target_name": row.get("raw_target_name"),
        "qtmscore": row.get("qtmscore"),
        "ttmscore": row.get("ttmscore"),
        "alntmscore": row.get("alntmscore"),
        "max_pair_tm_score": row.get("max_pair_tm_score"),
        "threshold": threshold,
        "target_operator": "<",
        "violates_target": score is not None and score >= threshold,
        "train_test_pair": True,
        "self_pair": bool(row.get("self_pair")),
        "source_signal_line_number": row.get("line_number"),
        "review_status": "review_only_non_countable",
        "countable_label_candidate": False,
        "import_ready": False,
    }


def _structure_entry_ids_from_row(row: dict[str, Any], key: str) -> list[str]:
    return sorted(
        [str(entry_id) for entry_id in row.get(key, []) if isinstance(entry_id, str)],
        key=_entry_id_sort_key,
    )


def _parse_foldseek_tm_score_rows(
    *,
    result_tsv: Path,
    alias_to_structure: dict[str, dict[str, Any]],
    row_partitions_by_entry: dict[str, Any],
) -> list[dict[str, Any]]:
    if not result_tsv.exists():
        raise ValueError(f"Foldseek result TSV was not created: {result_tsv}")
    rows: list[dict[str, Any]] = []
    with result_tsv.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if fields[:5] == ["query", "target", "qtmscore", "ttmscore", "alntmscore"]:
                continue
            rows.append(
                _parse_foldseek_tm_score_row(
                    line_number=line_number,
                    line=line,
                    fields=fields,
                    alias_to_structure=alias_to_structure,
                    row_partitions_by_entry=row_partitions_by_entry,
                )
            )
    return rows


def _summarize_foldseek_tm_score_rows(
    *,
    result_tsv: Path,
    alias_to_structure: dict[str, dict[str, Any]],
    row_partitions_by_entry: dict[str, Any],
    threshold: float,
    max_reported_rows: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not result_tsv.exists():
        raise ValueError(f"Foldseek result TSV was not created: {result_tsv}")

    threshold_value = float(threshold)
    report_limit = max(0, int(max_reported_rows))
    pair_count = 0
    mapped_pair_count = 0
    train_test_pair_count = 0
    target_violating_count = 0
    partition_pair_counts = _foldseek_partition_pair_counts([])
    max_train_test_tm_score: float | None = None
    unmapped_names: set[str] = set()
    unique_nonself_pairs: set[tuple[str, str]] = set()
    reported_by_line: dict[int, dict[str, Any]] = {}
    top_train_test_rows: list[dict[str, Any]] = []

    def keep_reported(row: dict[str, Any]) -> None:
        if report_limit <= 0:
            return
        line_number = row.get("line_number")
        if isinstance(line_number, int) and len(reported_by_line) < report_limit:
            reported_by_line[line_number] = row

    with result_tsv.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if fields[:5] == ["query", "target", "qtmscore", "ttmscore", "alntmscore"]:
                continue
            row = _parse_foldseek_tm_score_row(
                line_number=line_number,
                line=line,
                fields=fields,
                alias_to_structure=alias_to_structure,
                row_partitions_by_entry=row_partitions_by_entry,
            )
            pair_count += 1
            if row.get("query_structure_key") and row.get("target_structure_key"):
                mapped_pair_count += 1
            for name, key in (
                (row.get("raw_query_name"), row.get("query_structure_key")),
                (row.get("raw_target_name"), row.get("target_structure_key")),
            ):
                if name and not key:
                    unmapped_names.add(str(name))
            query_key = row.get("query_structure_key") or f"raw:{row.get('raw_query_name')}"
            target_key = row.get("target_structure_key") or f"raw:{row.get('raw_target_name')}"
            if query_key != target_key:
                unique_nonself_pairs.add(tuple(sorted([str(query_key), str(target_key)])))
            partitions = set(row.get("query_partitions") or []) | set(
                row.get("target_partitions") or []
            )
            if "heldout" in partitions and "in_distribution" in partitions:
                partition_pair_counts["heldout_in_distribution_pair_count"] += 1
            elif partitions == {"heldout"}:
                partition_pair_counts["heldout_pair_count"] += 1
            elif partitions == {"in_distribution"}:
                partition_pair_counts["in_distribution_pair_count"] += 1
            else:
                partition_pair_counts["other_partition_pair_count"] += 1

            if not row.get("train_test_pair"):
                continue
            train_test_pair_count += 1
            score = _parse_optional_float(row.get("max_pair_tm_score"))
            if score is None:
                continue
            max_train_test_tm_score = (
                score
                if max_train_test_tm_score is None
                else max(max_train_test_tm_score, score)
            )
            if score >= threshold_value:
                target_violating_count += 1
                keep_reported(row)
            top_train_test_rows.append(row)
            if len(top_train_test_rows) > max(20, report_limit * 3):
                top_train_test_rows = sorted(
                    top_train_test_rows,
                    key=lambda item: -(
                        _parse_optional_float(item.get("max_pair_tm_score")) or -1.0
                    ),
                )[:report_limit]

    for row in sorted(
        top_train_test_rows,
        key=lambda item: -(
            _parse_optional_float(item.get("max_pair_tm_score")) or -1.0
        ),
    )[:report_limit]:
        keep_reported(row)

    return (
        sorted(
            reported_by_line.values(),
            key=lambda row: (
                str(row.get("raw_query_name") or ""),
                str(row.get("raw_target_name") or ""),
            ),
        ),
        {
            "pair_count": pair_count,
            "mapped_pair_count": mapped_pair_count,
            "train_test_pair_count": train_test_pair_count,
            "target_violating_train_test_pair_row_count": target_violating_count,
            "heldout_in_distribution_pair_count": partition_pair_counts[
                "heldout_in_distribution_pair_count"
            ],
            "heldout_pair_count": partition_pair_counts["heldout_pair_count"],
            "in_distribution_pair_count": partition_pair_counts[
                "in_distribution_pair_count"
            ],
            "other_partition_pair_count": partition_pair_counts[
                "other_partition_pair_count"
            ],
            "unique_unordered_nonself_pair_count": len(unique_nonself_pairs),
            "max_train_test_tm_score": max_train_test_tm_score,
            "unmapped_names": sorted(unmapped_names),
        },
    )


def _parse_foldseek_tm_score_row(
    *,
    line_number: int,
    line: str,
    fields: list[str],
    alias_to_structure: dict[str, dict[str, Any]],
    row_partitions_by_entry: dict[str, Any],
) -> dict[str, Any]:
    if len(fields) < 5:
        return {
            "line_number": line_number,
            "raw_line": line,
            "parse_error": "expected at least 5 tab-separated Foldseek fields",
            "raw_query_name": fields[0] if fields else None,
            "raw_target_name": fields[1] if len(fields) > 1 else None,
            "query_structure_key": None,
            "target_structure_key": None,
            "query_name_mapping_status": "unparsed_row",
            "target_name_mapping_status": "unparsed_row",
            "train_test_pair": False,
        }

    query_raw, target_raw = fields[0], fields[1]
    query_structure, query_status = _map_foldseek_raw_name(
        query_raw, alias_to_structure
    )
    target_structure, target_status = _map_foldseek_raw_name(
        target_raw, alias_to_structure
    )
    query_entry_ids = _structure_entry_ids(query_structure)
    target_entry_ids = _structure_entry_ids(target_structure)
    query_partitions = sorted(
        {
            str(row_partitions_by_entry.get(entry_id))
            for entry_id in query_entry_ids
            if row_partitions_by_entry.get(entry_id) is not None
        }
    )
    target_partitions = sorted(
        {
            str(row_partitions_by_entry.get(entry_id))
            for entry_id in target_entry_ids
            if row_partitions_by_entry.get(entry_id) is not None
        }
    )
    qtmscore = _parse_optional_float(fields[2])
    ttmscore = _parse_optional_float(fields[3])
    alntmscore = _parse_optional_float(fields[4])
    max_pair_tm_score = _max_optional_float([qtmscore, ttmscore, alntmscore])
    return {
        "line_number": line_number,
        "raw_query_name": query_raw,
        "raw_target_name": target_raw,
        "query_name_mapping_status": query_status,
        "target_name_mapping_status": target_status,
        "query_structure_key": (
            query_structure.get("structure_key") if query_structure else None
        ),
        "target_structure_key": (
            target_structure.get("structure_key") if target_structure else None
        ),
        "query_structure_id": (
            query_structure.get("structure_id") if query_structure else None
        ),
        "target_structure_id": (
            target_structure.get("structure_id") if target_structure else None
        ),
        "query_coordinate_path": (
            query_structure.get("coordinate_path") if query_structure else None
        ),
        "target_coordinate_path": (
            target_structure.get("coordinate_path") if target_structure else None
        ),
        "query_entry_ids": query_entry_ids,
        "target_entry_ids": target_entry_ids,
        "query_partitions": query_partitions,
        "target_partitions": target_partitions,
        "qtmscore": qtmscore,
        "ttmscore": ttmscore,
        "alntmscore": alntmscore,
        "max_pair_tm_score": max_pair_tm_score,
        "self_pair": bool(
            query_structure
            and target_structure
            and query_structure.get("structure_key")
            == target_structure.get("structure_key")
        ),
        "train_test_pair": _is_train_test_partition_pair(
            query_partitions, target_partitions
        ),
    }


def _map_foldseek_raw_name(
    raw_name: str,
    alias_to_structure: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, str]:
    for alias in (raw_name, Path(raw_name).name, Path(raw_name).stem):
        if alias in alias_to_structure:
            return alias_to_structure[alias], "mapped_exact_alias"
    raw_basename = Path(raw_name).name
    chain_suffix_matches = {
        str(structure.get("structure_key")): structure
        for alias, structure in alias_to_structure.items()
        if "/" not in alias
        and "." not in alias
        and raw_basename.startswith(f"{alias}_")
    }
    if len(chain_suffix_matches) == 1:
        return next(iter(chain_suffix_matches.values())), "mapped_chain_suffix_alias"
    return None, "unmapped_raw_name"


def _structure_entry_ids(structure: dict[str, Any] | None) -> list[str]:
    if not structure:
        return []
    return sorted(
        [str(entry_id) for entry_id in structure.get("entry_ids", [])],
        key=_entry_id_sort_key,
    )


def _parse_optional_float(value: Any) -> float | None:
    try:
        return round(float(value), 4)
    except (TypeError, ValueError):
        return None


def _max_optional_float(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return max(present) if present else None


def _is_train_test_partition_pair(
    query_partitions: list[str],
    target_partitions: list[str],
) -> bool:
    partitions = set(query_partitions) | set(target_partitions)
    return "heldout" in partitions and "in_distribution" in partitions


def _foldseek_partition_pair_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "heldout_in_distribution_pair_count": 0,
        "heldout_pair_count": 0,
        "in_distribution_pair_count": 0,
        "other_partition_pair_count": 0,
    }
    for row in rows:
        partitions = set(row.get("query_partitions") or []) | set(
            row.get("target_partitions") or []
        )
        if "heldout" in partitions and "in_distribution" in partitions:
            counts["heldout_in_distribution_pair_count"] += 1
        elif partitions == {"heldout"}:
            counts["heldout_pair_count"] += 1
        elif partitions == {"in_distribution"}:
            counts["in_distribution_pair_count"] += 1
        else:
            counts["other_partition_pair_count"] += 1
    return counts


def _unique_unordered_nonself_pair_count(rows: list[dict[str, Any]]) -> int:
    pairs = set()
    for row in rows:
        query_key = row.get("query_structure_key") or f"raw:{row.get('raw_query_name')}"
        target_key = row.get("target_structure_key") or f"raw:{row.get('raw_target_name')}"
        if query_key == target_key:
            continue
        pairs.add(tuple(sorted([str(query_key), str(target_key)])))
    return len(pairs)


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(float(numerator) / float(denominator), 4)


def _backend_version(binary: str) -> str | None:
    try:
        completed = subprocess.run(
            [binary, "version"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return (completed.stdout.strip() or completed.stderr.strip()) or None


def _command_string(command: list[str]) -> str:
    return shlex.join(command)


def _foldseek_binary_info(foldseek_binary: str) -> dict[str, Any]:
    requested = str(foldseek_binary or "foldseek")
    if "/" in requested:
        candidate = Path(requested)
        resolved = str(candidate) if candidate.exists() else None
    else:
        resolved = shutil.which(requested)
    version = _backend_version(resolved) if resolved else None
    version_command = _command_string([resolved or requested, "version"])
    return {
        "requested": requested,
        "resolved": resolved,
        "available": bool(resolved and version),
        "version": version,
        "version_command": version_command,
    }


def _mmseqs_float(value: float) -> str:
    return f"{float(value):.4g}"


def _selected_coordinate_structure(
    *,
    retrieval_row: dict[str, Any],
    geometry_row: dict[str, Any],
    holdout_row: dict[str, Any],
) -> tuple[str | None, str | None, str | None]:
    for source_field, value in (
        ("sequence_holdout.selected_structure_proxy_id", holdout_row.get("selected_structure_proxy_id")),
        ("retrieval.selected_structure_proxy_id", retrieval_row.get("selected_structure_proxy_id")),
        ("geometry.selected_structure_proxy_id", geometry_row.get("selected_structure_proxy_id")),
    ):
        source, structure_id = _parse_selected_structure_key(value)
        if source and structure_id:
            return source, structure_id, source_field

    for source_field, value in (
        ("retrieval.pdb_id", retrieval_row.get("pdb_id")),
        ("geometry.pdb_id", geometry_row.get("pdb_id")),
    ):
        structure_id = _normalise_pdb_structure_id(value)
        if structure_id:
            return "pdb", structure_id, source_field

    for source_field, value in (
        ("retrieval.alphafold_id", retrieval_row.get("alphafold_id")),
        ("geometry.alphafold_id", geometry_row.get("alphafold_id")),
        ("retrieval.alphafold_accession", retrieval_row.get("alphafold_accession")),
        ("geometry.alphafold_accession", geometry_row.get("alphafold_accession")),
    ):
        structure_id = _normalise_alphafold_structure_id(value)
        if structure_id:
            return "alphafold", structure_id, source_field

    return None, None, None


def _parse_selected_structure_key(value: Any) -> tuple[str | None, str | None]:
    if not isinstance(value, str) or ":" not in value:
        return None, None
    source, _, raw_id = value.partition(":")
    source = source.strip().lower()
    raw_id = raw_id.strip()
    if source == "pdb":
        structure_id = _normalise_pdb_structure_id(raw_id)
    elif source == "alphafold":
        structure_id = _normalise_alphafold_structure_id(raw_id)
    else:
        structure_id = raw_id or None
    return (source or None), structure_id


def _normalise_pdb_structure_id(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip().upper()
    return cleaned or None


def _normalise_alphafold_structure_id(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if cleaned.startswith("AF-"):
        cleaned = cleaned[3:]
    cleaned = cleaned.split("-F1-model", 1)[0]
    return cleaned or None


def _coordinate_file_name(source: str, structure_id: str) -> str:
    safe_source = re.sub(r"[^A-Za-z0-9]+", "_", source).strip("_").lower()
    safe_id = re.sub(r"[^A-Za-z0-9]+", "_", structure_id).strip("_")
    return f"{safe_source}_{safe_id}.cif"


def _selected_structure_proxy_id(
    result: dict[str, Any], geometry_entry: dict[str, Any]
) -> str:
    pdb_id = result.get("pdb_id") or geometry_entry.get("pdb_id")
    if pdb_id:
        return f"pdb:{str(pdb_id).upper()}"
    return "missing_selected_structure"


def _active_site_geometry_proxy_bucket(
    result: dict[str, Any], geometry_entry: dict[str, Any]
) -> str:
    residue_codes = result.get("residue_codes") or [
        residue.get("code")
        for residue in geometry_entry.get("residues", []) or []
        if isinstance(residue, dict)
    ]
    residue_signature = "-".join(sorted(str(code).upper() for code in residue_codes if code))
    ligand_context = result.get("ligand_context") or geometry_entry.get("ligand_context") or {}
    cofactor_signature = "-".join(
        sorted(str(item) for item in ligand_context.get("cofactor_families", []) or [])
    )
    top = result.get("top_fingerprints", []) or []
    top1_id = top[0].get("fingerprint_id") if top and isinstance(top[0], dict) else "no_top1"
    distance_median = None
    if top and isinstance(top[0], dict):
        distance_summary = top[0].get("distance_summary") or {}
        distance_median = distance_summary.get("median")
    if distance_median is None:
        distances = [
            float(item.get("distance"))
            for item in geometry_entry.get("pairwise_distances_angstrom", []) or []
            if isinstance(item, dict) and item.get("distance") is not None
        ]
        if distances:
            distances.sort()
            distance_median = distances[len(distances) // 2]
    median_bucket = _numeric_bucket(distance_median, size=4.0, missing="median_missing")
    resolved_bucket = _numeric_bucket(
        result.get("resolved_residue_count", geometry_entry.get("resolved_residue_count")),
        size=2.0,
        missing="resolved_missing",
    )
    return "|".join(
        [
            f"top1:{top1_id}",
            f"residues:{residue_signature or 'none'}",
            f"cofactors:{cofactor_signature or 'none'}",
            f"median:{median_bucket}",
            f"resolved:{resolved_bucket}",
        ]
    )


def _numeric_bucket(value: Any, *, size: float, missing: str) -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return missing
    lower = int(numeric // size) * int(size)
    upper = lower + int(size)
    return f"{lower}-{upper}"


def _low_neighborhood_proxy_score(row: dict[str, Any]) -> float:
    sequence_score = 1.0 / max(int(row.get("sequence_cluster_entry_count", 0) or 0), 1)
    structure_score = 1.0 / max(int(row.get("selected_structure_proxy_count", 0) or 0), 1)
    geometry_score = 1.0 / max(int(row.get("active_site_geometry_proxy_bucket_count", 0) or 0), 1)
    return round(0.5 * sequence_score + 0.3 * structure_score + 0.2 * geometry_score, 4)


def _select_holdout_entry_ids(
    rows: list[dict[str, Any]],
    *,
    holdout_fraction: float,
    min_holdout_rows: int,
) -> tuple[set[str], list[str]]:
    if not rows:
        return set(), ["no_evaluation_rows_available"]
    target_total = min(
        len(rows),
        max(min_holdout_rows, round(len(rows) * holdout_fraction)),
    )
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[str(row.get("label_group") or "unknown")].append(row)

    heldout_ids: set[str] = set()
    notes: list[str] = []
    group_targets: dict[str, int] = {}
    for group, group_rows in sorted(by_group.items()):
        if len(group_rows) == 1:
            group_targets[group] = 1 if target_total >= len(by_group) else 0
            continue
        group_targets[group] = max(1, round(len(group_rows) * holdout_fraction))

    while sum(group_targets.values()) > target_total:
        reducible = [
            group
            for group, count in group_targets.items()
            if count > 1
        ]
        if not reducible:
            break
        largest = max(reducible, key=lambda group: (group_targets[group], len(by_group[group]), group))
        group_targets[largest] -= 1

    for group, group_rows in sorted(by_group.items()):
        target = group_targets.get(group, 0)
        if target <= 0:
            continue
        strict_candidates = [
            row
            for row in group_rows
            if row.get("low_similarity_proxy_pass") and row.get("fold_divergence_proxy_pass")
        ]
        candidate_pool = strict_candidates or group_rows
        if not strict_candidates:
            notes.append(
                f"{group}: relaxed partition because strict low-similarity/fold proxy rows were unavailable"
            )
        ranked = sorted(
            candidate_pool,
            key=lambda row: (
                -float(row.get("low_neighborhood_proxy_score", 0.0) or 0.0),
                _stable_partition_hash(row),
                _entry_id_sort_key(str(row.get("entry_id") or "")),
            ),
        )
        heldout_ids.update(str(row["entry_id"]) for row in ranked[:target])

    if len(heldout_ids) < target_total:
        remaining = [row for row in rows if row["entry_id"] not in heldout_ids]
        ranked_remaining = sorted(
            remaining,
            key=lambda row: (
                -float(row.get("low_neighborhood_proxy_score", 0.0) or 0.0),
                _stable_partition_hash(row),
                _entry_id_sort_key(str(row.get("entry_id") or "")),
            ),
        )
        heldout_ids.update(
            str(row["entry_id"]) for row in ranked_remaining[: target_total - len(heldout_ids)]
        )
    return heldout_ids, notes


def _stable_partition_hash(row: dict[str, Any]) -> str:
    payload = "|".join(
        [
            str(row.get("entry_id") or ""),
            str(row.get("sequence_cluster_id") or ""),
            str(row.get("selected_structure_proxy_id") or ""),
            str(row.get("active_site_geometry_proxy_bucket") or ""),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _partition_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    evaluable_rows = [row for row in rows if row.get("evaluable")]
    in_scope = [row for row in rows if row.get("label_type") == "seed_fingerprint"]
    out_scope = [row for row in rows if row.get("label_type") == "out_of_scope"]
    in_scope_evaluable = [row for row in evaluable_rows if row.get("label_type") == "seed_fingerprint"]
    out_scope_evaluable = [row for row in evaluable_rows if row.get("label_type") == "out_of_scope"]
    retained_in_scope = [row for row in in_scope if not row["abstained"]]
    retained_in_scope_evaluable = [
        row for row in in_scope_evaluable if not row["abstained"]
    ]
    return {
        "evaluated_count": len(rows),
        "evaluable_count": len(evaluable_rows),
        "in_scope_count": len(in_scope),
        "in_scope_evaluable_count": len(in_scope_evaluable),
        "out_of_scope_count": len(out_scope),
        "out_of_scope_evaluable_count": len(out_scope_evaluable),
        "retained_in_scope_count": len(retained_in_scope),
        "retained_in_scope_evaluable_count": len(retained_in_scope_evaluable),
        "top1_accuracy_in_scope": _ratio(sum(1 for row in in_scope if row["top1_correct"]), len(in_scope)),
        "top3_accuracy_in_scope": _ratio(sum(1 for row in in_scope if row["top3_correct"]), len(in_scope)),
        "top1_accuracy_among_retained_in_scope": _ratio(
            sum(1 for row in retained_in_scope if row["top1_correct"]),
            len(retained_in_scope),
        ),
        "top3_accuracy_among_retained_in_scope": _ratio(
            sum(1 for row in retained_in_scope if row["top3_correct"]),
            len(retained_in_scope),
        ),
        "top1_accuracy_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable if row["top1_correct"]),
            len(in_scope_evaluable),
        ),
        "top3_accuracy_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable if row["top3_correct"]),
            len(in_scope_evaluable),
        ),
        "top1_accuracy_among_retained_in_scope_evaluable": _ratio(
            sum(1 for row in retained_in_scope_evaluable if row["top1_correct"]),
            len(retained_in_scope_evaluable),
        ),
        "top3_accuracy_among_retained_in_scope_evaluable": _ratio(
            sum(1 for row in retained_in_scope_evaluable if row["top3_correct"]),
            len(retained_in_scope_evaluable),
        ),
        "top1_retained_accuracy_in_scope": _ratio(
            sum(1 for row in in_scope if row["top1_correct"] and not row["abstained"]),
            len(in_scope),
        ),
        "top3_retained_accuracy_in_scope": _ratio(
            sum(1 for row in in_scope if row["top3_correct"] and not row["abstained"]),
            len(in_scope),
        ),
        "top1_retained_accuracy_in_scope_evaluable": _ratio(
            sum(
                1
                for row in in_scope_evaluable
                if row["top1_correct"] and not row["abstained"]
            ),
            len(in_scope_evaluable),
        ),
        "top3_retained_accuracy_in_scope_evaluable": _ratio(
            sum(
                1
                for row in in_scope_evaluable
                if row["top3_correct"] and not row["abstained"]
            ),
            len(in_scope_evaluable),
        ),
        "retention_rate_in_scope": _ratio(sum(1 for row in in_scope if not row["abstained"]), len(in_scope)),
        "retention_rate_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable if not row["abstained"]),
            len(in_scope_evaluable),
        ),
        "abstention_rate_in_scope": _ratio(sum(1 for row in in_scope if row["abstained"]), len(in_scope)),
        "abstention_rate_in_scope_evaluable": _ratio(
            sum(1 for row in in_scope_evaluable if row["abstained"]),
            len(in_scope_evaluable),
        ),
        "out_of_scope_abstention_rate": _ratio(
            sum(1 for row in out_scope if row["abstained"]),
            len(out_scope),
        ),
        "out_of_scope_abstention_rate_evaluable": _ratio(
            sum(1 for row in out_scope_evaluable if row["abstained"]),
            len(out_scope_evaluable),
        ),
        "out_of_scope_false_non_abstentions": sum(
            1 for row in out_scope if not row["abstained"]
        ),
        "out_of_scope_false_non_abstentions_evaluable": sum(
            1 for row in out_scope_evaluable if not row["abstained"]
        ),
    }


def _per_fingerprint_breakdowns(rows: list[dict[str, Any]]) -> dict[str, Any]:
    in_scope_rows = [row for row in rows if row.get("label_type") == "seed_fingerprint"]
    out_scope_rows = [row for row in rows if row.get("label_type") == "out_of_scope"]
    by_target: dict[str, Any] = {}
    for fingerprint_id in sorted({str(row.get("target_fingerprint_id")) for row in in_scope_rows}):
        target_rows = [
            row for row in in_scope_rows if str(row.get("target_fingerprint_id")) == fingerprint_id
        ]
        by_target[fingerprint_id] = _partition_metrics(target_rows)
    by_out_scope_top1: dict[str, Any] = {}
    for fingerprint_id in sorted({str(row.get("top1_fingerprint_id")) for row in out_scope_rows}):
        top1_rows = [
            row for row in out_scope_rows if str(row.get("top1_fingerprint_id")) == fingerprint_id
        ]
        by_out_scope_top1[fingerprint_id] = {
            "evaluated_count": len(top1_rows),
            "evaluable_count": sum(1 for row in top1_rows if row.get("evaluable")),
            "abstention_rate": _ratio(
                sum(1 for row in top1_rows if row["abstained"]),
                len(top1_rows),
            ),
            "false_non_abstentions": sum(1 for row in top1_rows if not row["abstained"]),
            "false_non_abstentions_evaluable": sum(
                1 for row in top1_rows if row.get("evaluable") and not row["abstained"]
            ),
        }
    return {
        "in_scope_by_target_fingerprint": by_target,
        "out_of_scope_by_top1_fingerprint": by_out_scope_top1,
    }


def _is_geometry_evaluable(result: dict[str, Any]) -> bool:
    status = result.get("status")
    if status is None:
        return True
    return status == "ok" and int(result.get("resolved_residue_count", 0) or 0) > 0


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = entry_id.partition(":")
    try:
        numeric = int(suffix)
    except ValueError:
        numeric = 0
    return (prefix, numeric, entry_id)
