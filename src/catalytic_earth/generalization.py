from __future__ import annotations

import hashlib
import shutil
from collections import Counter, defaultdict
from typing import Any

from .labels import MechanismLabel, label_summary


CLUSTERING_TOOL_CANDIDATES = ("foldseek", "mmseqs", "blastp", "diamond")


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
) -> dict[str, Any]:
    """Evaluate retrieval on a proxy low-sequence/fold-neighborhood holdout.

    This command is intentionally honest about what the local repo can compute:
    if real clustering tools are absent, the partition is a deterministic proxy
    based on exact UniProt reference clusters and selected-structure context.
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

    heldout_ids, partition_notes = _select_holdout_entry_ids(
        result_rows,
        holdout_fraction=holdout_fraction,
        min_holdout_rows=min_holdout_rows,
    )
    for row in result_rows:
        row["partition"] = "heldout" if row["entry_id"] in heldout_ids else "in_distribution"

    heldout_rows = [row for row in result_rows if row["partition"] == "heldout"]
    in_distribution_rows = [
        row for row in result_rows if row["partition"] == "in_distribution"
    ]
    all_metrics = _partition_metrics(result_rows)
    heldout_metrics = _partition_metrics(heldout_rows)
    in_distribution_metrics = _partition_metrics(in_distribution_rows)
    tool_status = {tool: bool(shutil.which(tool)) for tool in CLUSTERING_TOOL_CANDIDATES}
    real_tool_available = any(tool_status.values())
    backend = (
        "real_clustering_tool_available_not_invoked_by_proxy_command"
        if real_tool_available
        else "deterministic_local_proxy_no_foldseek_mmseqs2_blast_or_diamond"
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
            "real_sequence_identity_computed": False,
            "real_tm_score_computed": False,
            "sequence_identity_target": "<=0.30 when real clustering/alignment is available",
            "tm_score_target": "<0.70 when Foldseek/TM-score is available",
            "proxy_limitation": (
                "Exact UniProt reference clusters, selected PDB identifiers, "
                "and active-site geometry buckets are low-neighborhood proxies; "
                "they do not replace all-vs-all sequence identity, MMseqs2, "
                "Foldseek, or TM-score clustering."
            ),
            "partition_rule": (
                "stratified deterministic holdout by label/fingerprint group, "
                "prioritizing singleton exact UniProt reference clusters, "
                "singleton selected structures, and rare active-site geometry "
                "proxy buckets"
            ),
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
