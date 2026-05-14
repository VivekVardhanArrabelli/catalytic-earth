from __future__ import annotations

import hashlib
import re
import shlex
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .labels import MechanismLabel, label_summary


CLUSTERING_TOOL_CANDIDATES = ("foldseek", "mmseqs", "blastp", "diamond")
SEQUENCE_FIELD_NAMES = (
    "sequence",
    "protein_sequence",
    "amino_acid_sequence",
    "reference_sequence",
)
MMSEQS_CLUSTER_COVERAGE_MODE = 0


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
            "clustering_backend": backend,
            "clustering_tool_status": tool_status,
            "backend_command": real_split.get("backend_command"),
            "backend_commands": real_split.get("backend_commands", []),
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
            "sequence_identity_target_achieved": target_achieved,
            "sequence_identity_limitations": _sequence_identity_limitations(
                real_split=real_split,
                train_test_identity=train_test_identity,
                sequence_identity_threshold=sequence_identity_threshold,
            ),
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


def _run_backend_command(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"{_command_string(command)} failed with exit code {completed.returncode}: {stderr[:1000]}"
        )


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


def _mmseqs_float(value: float) -> str:
    return f"{float(value):.4g}"


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
