from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .geometry_retrieval import score_entry_against_fingerprint


ORGANIC_COFACTOR_CLASSES = ("flavin", "heme", "plp")
SCORE_VECTOR_COMPONENTS = (
    "score",
    "residue_match_fraction",
    "role_match_fraction",
    "cofactor_context_score",
    "compactness_score",
    "substrate_pocket_score",
    "plp_ligand_anchor_score",
    "mechanistic_coherence_score",
    "counterevidence_penalty",
)
RANK_VARIANTS = ("cosine", "robust_l2")


def write_mechanism_relationship_eval(
    *,
    label_manifest_path: Path,
    current_labels_path: Path,
    ontology_path: Path,
    experimental_geometry_features_path: Path,
    predicted_geometry_audit_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    previous_eval_path: Path | None,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_relationship_eval(
        label_manifest=_load_json(label_manifest_path),
        current_labels=_load_json(current_labels_path),
        ontology=_load_json(ontology_path),
        experimental_geometry_features=_load_json(experimental_geometry_features_path),
        predicted_geometry_audit=_load_json(predicted_geometry_audit_path),
        selected_organic_cofactor_sidecar=_load_json(
            selected_organic_cofactor_sidecar_path
        ),
        previous_eval=_load_json(previous_eval_path)
        if previous_eval_path is not None and previous_eval_path.exists()
        else None,
        source_paths={
            "label_manifest": label_manifest_path,
            "current_labels": current_labels_path,
            "ontology": ontology_path,
            "experimental_geometry_features": experimental_geometry_features_path,
            "predicted_geometry_audit": predicted_geometry_audit_path,
            "selected_organic_cofactor_sidecar": selected_organic_cofactor_sidecar_path,
            "previous_eval": previous_eval_path,
        },
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit


def build_mechanism_relationship_eval(
    *,
    label_manifest: dict[str, Any],
    current_labels: list[dict[str, Any]],
    ontology: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    predicted_geometry_audit: dict[str, Any],
    selected_organic_cofactor_sidecar: dict[str, Any],
    previous_eval: dict[str, Any] | None = None,
    source_paths: dict[str, Path | None] | None = None,
) -> dict[str, Any]:
    current_rows = _current_rows(label_manifest, current_labels)
    family_by_fingerprint = _family_by_fingerprint(ontology)
    fingerprints = [fingerprint.to_dict() for fingerprint in load_fingerprints()]
    cofactor_sets = {
        str(fingerprint["id"]): _normalized_cofactor_set(fingerprint.get("cofactors", []))
        for fingerprint in fingerprints
    }
    cofactor_scores, cofactor_summary = _selected_organic_scores(
        selected_organic_cofactor_sidecar
    )
    tuning_adjacent_ids = _tuning_adjacent_ids(previous_eval)

    experimental_by_entry = _entries_by_id(experimental_geometry_features)
    predicted_geometry = predicted_geometry_audit.get("predicted_geometry_features", {})
    predicted_by_entry = _entries_by_id(predicted_geometry)

    candidate_rows = [
        row
        for row in current_rows
        if row.get("split_assignment") == "in_distribution"
        and row.get("fingerprint_id")
        and row["entry_id"] in experimental_by_entry
    ]
    query_rows = [
        row
        for row in current_rows
        if row.get("split_assignment") == "heldout"
        and row.get("fingerprint_id")
        and row["entry_id"] in predicted_by_entry
    ]

    candidate_score_vectors = _row_vectors(
        rows=candidate_rows,
        entries_by_id=experimental_by_entry,
        fingerprints=fingerprints,
        cofactor_scores=cofactor_scores,
        include_cofactor=False,
    )
    query_score_vectors = _row_vectors(
        rows=query_rows,
        entries_by_id=predicted_by_entry,
        fingerprints=fingerprints,
        cofactor_scores=cofactor_scores,
        include_cofactor=False,
    )
    candidate_augmented_vectors = _row_vectors(
        rows=candidate_rows,
        entries_by_id=experimental_by_entry,
        fingerprints=fingerprints,
        cofactor_scores=cofactor_scores,
        include_cofactor=True,
    )
    query_augmented_vectors = _row_vectors(
        rows=query_rows,
        entries_by_id=predicted_by_entry,
        fingerprints=fingerprints,
        cofactor_scores=cofactor_scores,
        include_cofactor=True,
    )

    baseline_surface = _evaluate_surface(
        source_id="predicted_query_vs_experimental_atlas_fingerprint_score_rerun",
        display_name="Predicted geometry score query vs experimental atlas score vector rerun",
        candidates=candidate_score_vectors,
        queries=query_score_vectors,
        family_by_fingerprint=family_by_fingerprint,
        cofactor_sets=cofactor_sets,
        tuning_adjacent_ids=tuning_adjacent_ids,
        include_cofactor=False,
        exclude_tuning_adjacent_queries=False,
    )
    augmented_surface = _evaluate_surface(
        source_id=(
            "predicted_query_vs_experimental_atlas_score_plus_selected_organic_cofactor"
        ),
        display_name=(
            "Predicted geometry score query plus selected organic cofactor sidecar "
            "vs experimental atlas"
        ),
        candidates=candidate_augmented_vectors,
        queries=query_augmented_vectors,
        family_by_fingerprint=family_by_fingerprint,
        cofactor_sets=cofactor_sets,
        tuning_adjacent_ids=tuning_adjacent_ids,
        include_cofactor=True,
        exclude_tuning_adjacent_queries=False,
    )
    augmented_non_tuning = _evaluate_surface(
        source_id=(
            "predicted_query_vs_experimental_atlas_score_plus_selected_organic_cofactor"
            "_non_tuning_adjacent_queries"
        ),
        display_name=augmented_surface["display_name"],
        candidates=candidate_augmented_vectors,
        queries=query_augmented_vectors,
        family_by_fingerprint=family_by_fingerprint,
        cofactor_sets=cofactor_sets,
        tuning_adjacent_ids=tuning_adjacent_ids,
        include_cofactor=True,
        exclude_tuning_adjacent_queries=True,
    )

    headline = _headline(baseline_surface, augmented_surface, augmented_non_tuning)
    return {
        "artifact_id": (
            "v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530"
        ),
        "schema_version": "mechanism_relationship_eval.cofactor_augmented.v1",
        "created_utc": _utc_now_iso(),
        "automation_id": "catalytic-earth-work-loop",
        "status": headline["status"],
        "scope": {
            "relationship_eval_only": True,
            "query_distribution": "AlphaFoldDB predicted heldout geometry",
            "candidate_atlas": "experimental in-distribution current702 geometry",
            "cofactor_input": (
                "persisted sequence-only selected organic cofactor scores for "
                "flavin/heme/PLP"
            ),
            "models_trained_or_refit": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "labels_registries_ontologies_imports_thresholds_mutated": False,
        },
        "guardrails": {
            "cofactor_scores_are_sequence_only": True,
            "cofactor_scores_source": cofactor_summary["selected_source_counts"],
            "cofactor_threshold_policy": "fixed_0_5_not_tuned_on_heldout",
            "feature_scaling_fit_on_candidates_only": True,
            "heldout_labels_used_only_for_final_relationship_metrics": True,
        },
        "counts": {
            "current702_rows": len(current_rows),
            "candidate_in_distribution_seed_rows": len(candidate_rows),
            "heldout_seed_query_rows_with_predicted_geometry": len(query_rows),
            "tuning_adjacent_ids_loaded": len(tuning_adjacent_ids),
        },
        "selected_organic_cofactor_sidecar": cofactor_summary,
        "feature_schema": {
            "fingerprint_score_components": list(SCORE_VECTOR_COMPONENTS),
            "fingerprint_count": len(fingerprints),
            "baseline_dimension": len(next(iter(candidate_score_vectors.values()))["vector"])
            if candidate_score_vectors
            else 0,
            "cofactor_augmented_dimensions": {
                "selected_scores": list(ORGANIC_COFACTOR_CLASSES),
                "fixed_threshold_indicators": [
                    f"{name}_fixed_0_5" for name in ORGANIC_COFACTOR_CLASSES
                ],
            },
            "cofactor_augmented_dimension": len(
                next(iter(candidate_augmented_vectors.values()))["vector"]
            )
            if candidate_augmented_vectors
            else 0,
        },
        "pre_registered_relationships": {
            "family_by_fingerprint": family_by_fingerprint,
            "cofactor_sets": cofactor_sets,
            "policy": {
                "candidate_pool": (
                    "in_distribution current seed-fingerprint rows with experimental "
                    "geometry vectors"
                ),
                "query_pool": (
                    "heldout current seed-fingerprint rows with AlphaFoldDB predicted "
                    "geometry vectors"
                ),
                "exact_neighbor": "candidate fingerprint equals query fingerprint",
                "family_neighbor": "exact neighbor or shared ontology family",
                "cofactor_neighbor": "shared normalized cofactor family",
            },
        },
        "relationship_rank_metrics": {
            baseline_surface["source_id"]: baseline_surface,
            augmented_surface["source_id"]: augmented_surface,
            augmented_non_tuning["source_id"]: augmented_non_tuning,
        },
        "headline": headline,
        "source_artifacts": _source_artifacts(source_paths or {}),
    }


def _current_rows(
    label_manifest: dict[str, Any],
    current_labels: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    labels_by_entry = {str(row.get("entry_id")): row for row in current_labels}
    rows: list[dict[str, Any]] = []
    for manifest_row in label_manifest.get("rows", []):
        if not isinstance(manifest_row, dict) or not manifest_row.get("entry_id"):
            continue
        entry_id = str(manifest_row["entry_id"])
        label = labels_by_entry.get(entry_id, {})
        rows.append(
            {
                "entry_id": entry_id,
                "split_assignment": manifest_row.get("split_assignment"),
                "manifest_benchmark_role": manifest_row.get("benchmark_role"),
                "manifest_fingerprint_id": manifest_row.get("fingerprint_id")
                or manifest_row.get("mechanism_fingerprint_id"),
                "fingerprint_id": label.get("fingerprint_id"),
                "label_type": label.get("label_type"),
                "current_benchmark_role": _current_benchmark_role(label),
                "oos_tier": manifest_row.get("oos_tier"),
                "probe_role": manifest_row.get("probe_role"),
            }
        )
    return rows


def _current_benchmark_role(label: dict[str, Any]) -> str:
    if label.get("label_type") == "seed_fingerprint":
        fingerprint_id = str(label.get("fingerprint_id") or "")
        if fingerprint_id in {
            "flavin_monooxygenase",
            "cobalamin_radical_rearrangement",
            "radical_sam_enzyme",
        }:
            return "secondary_probe"
        return "primary"
    return "out_of_scope"


def _family_by_fingerprint(ontology: dict[str, Any]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    for family in ontology.get("families", []):
        if not isinstance(family, dict):
            continue
        family_id = str(family.get("id") or "")
        for fingerprint_id in family.get("fingerprint_ids", []) or []:
            mapping[str(fingerprint_id)].append(family_id)
        for child in family.get("child_families", []) or []:
            if not isinstance(child, dict):
                continue
            child_id = str(child.get("id") or family_id)
            for fingerprint_id in child.get("fingerprint_ids", []) or []:
                mapping[str(fingerprint_id)].append(child_id)
    return {key: sorted(set(values)) for key, values in sorted(mapping.items())}


def _normalized_cofactor_set(cofactors: Any) -> list[str]:
    if not isinstance(cofactors, list):
        return []
    families = {_normalize_cofactor_family(str(cofactor)) for cofactor in cofactors}
    families.discard("")
    return sorted(families)


def _normalize_cofactor_family(value: str) -> str:
    text = value.lower().replace("-", "_")
    if any(term in text for term in ("fad", "fmn", "flavin")):
        return "flavin"
    if "heme" in text or "haem" in text:
        return "heme"
    if "pyridoxal" in text or text in {"plp", "pmp", "p5p"}:
        return "plp"
    if "cobalamin" in text or "vitamin_b12" in text:
        return "cobalamin"
    if "sam" in text or "adenosylmethionine" in text:
        return "sam"
    if "4fe_4s" in text or "fe_s" in text or "iron_sulfur" in text:
        return "fe_s_cluster"
    if any(term in text for term in ("zn", "mg", "mn", "fe(ii)", "metal", "ion")):
        return "metal_ion"
    if text in {"nad", "nadh", "nadp", "nadph"}:
        return "nad"
    return text.strip()


def _selected_organic_scores(
    selected_organic_cofactor_sidecar: dict[str, Any],
) -> tuple[dict[str, dict[str, float]], dict[str, Any]]:
    scores: dict[str, dict[str, float]] = defaultdict(dict)
    source_counts: Counter[str] = Counter()
    missing_flags: Counter[str] = Counter()
    null_scores: Counter[str] = Counter()
    by_class: Counter[str] = Counter()
    for record in selected_organic_cofactor_sidecar.get("row_class_records", []):
        if not isinstance(record, dict):
            continue
        entry_id = str(record.get("entry_id") or "")
        cofactor_class = str(record.get("cofactor_class") or record.get("class") or "")
        if not entry_id or cofactor_class not in ORGANIC_COFACTOR_CLASSES:
            continue
        by_class[cofactor_class] += 1
        score = record.get("selected_score")
        if score is None:
            null_scores[cofactor_class] += 1
            continue
        scores[entry_id][cofactor_class] = float(score)
        source_counts[str(record.get("selected_source") or "missing")] += 1
        for flag in record.get("missingness_flags") or []:
            missing_flags[str(flag)] += 1
    entries_with_all_scores = sum(
        1
        for entry_scores in scores.values()
        if all(name in entry_scores for name in ORGANIC_COFACTOR_CLASSES)
    )
    return dict(scores), {
        "artifact_id": selected_organic_cofactor_sidecar.get("artifact_id"),
        "status": selected_organic_cofactor_sidecar.get("status"),
        "row_class_records": sum(by_class.values()),
        "by_class": dict(sorted(by_class.items())),
        "null_scores_by_class": dict(sorted(null_scores.items())),
        "entries_with_all_scores": entries_with_all_scores,
        "selected_source_counts": dict(sorted(source_counts.items())),
        "missingness_flags": dict(sorted(missing_flags.items())),
        "fallback_caveat": (
            "Scores come from the ESM2-150M fallback selected sidecar; original "
            "t6/t12 selected sidecars remain unrecovered."
        ),
    }


def _entries_by_id(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(entry.get("entry_id")): entry
        for entry in payload.get("entries", [])
        if isinstance(entry, dict) and entry.get("entry_id")
    }


def _row_vectors(
    *,
    rows: list[dict[str, Any]],
    entries_by_id: dict[str, dict[str, Any]],
    fingerprints: list[dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
    include_cofactor: bool,
) -> dict[str, dict[str, Any]]:
    vectors: dict[str, dict[str, Any]] = {}
    for row in rows:
        entry_id = str(row["entry_id"])
        entry = entries_by_id.get(entry_id)
        if not entry:
            continue
        vector = _fingerprint_score_vector(entry, fingerprints)
        if include_cofactor:
            vector.extend(_cofactor_score_vector(entry_id, cofactor_scores))
        vectors[entry_id] = {
            "entry_id": entry_id,
            "fingerprint_id": row.get("fingerprint_id"),
            "split_assignment": row.get("split_assignment"),
            "current_benchmark_role": row.get("current_benchmark_role"),
            "vector": vector,
        }
    return vectors


def _fingerprint_score_vector(
    entry: dict[str, Any],
    fingerprints: list[dict[str, Any]],
) -> list[float]:
    vector: list[float] = []
    for fingerprint in sorted(fingerprints, key=lambda item: str(item.get("id"))):
        scored = score_entry_against_fingerprint(entry, fingerprint)
        for component in SCORE_VECTOR_COMPONENTS:
            vector.append(float(scored.get(component, 0.0) or 0.0))
    return vector


def _cofactor_score_vector(
    entry_id: str,
    cofactor_scores: dict[str, dict[str, float]],
) -> list[float]:
    entry_scores = cofactor_scores.get(entry_id, {})
    scores = [float(entry_scores.get(name, 0.0) or 0.0) for name in ORGANIC_COFACTOR_CLASSES]
    indicators = [1.0 if score >= 0.5 else 0.0 for score in scores]
    return scores + indicators


def _evaluate_surface(
    *,
    source_id: str,
    display_name: str,
    candidates: dict[str, dict[str, Any]],
    queries: dict[str, dict[str, Any]],
    family_by_fingerprint: dict[str, list[str]],
    cofactor_sets: dict[str, list[str]],
    tuning_adjacent_ids: set[str],
    include_cofactor: bool,
    exclude_tuning_adjacent_queries: bool,
) -> dict[str, Any]:
    query_items = list(queries.values())
    if exclude_tuning_adjacent_queries:
        query_items = [
            query
            for query in query_items
            if str(query["entry_id"]) not in tuning_adjacent_ids
        ]
    candidate_items = list(candidates.values())
    robust_scaler = _robust_scaler([item["vector"] for item in candidate_items])
    metrics_by_variant = {}
    per_fingerprint = {}
    samples_by_variant = {}
    for variant in RANK_VARIANTS:
        rankings = [
            _rank_query(
                query=query,
                candidates=candidate_items,
                variant=variant,
                robust_scaler=robust_scaler,
                family_by_fingerprint=family_by_fingerprint,
                cofactor_sets=cofactor_sets,
            )
            for query in query_items
        ]
        metrics_by_variant[variant] = _rank_metrics(rankings)
        per_fingerprint[variant] = _per_fingerprint_metrics(rankings)
        samples_by_variant[variant] = _samples(rankings)
    feature_dimension = (
        len(candidate_items[0]["vector"]) if candidate_items else 0
    )
    return {
        "source_id": source_id,
        "surface": "fingerprint_score_vector_with_optional_selected_organic_cofactor_scores",
        "display_name": display_name,
        "status": "complete" if query_items and candidate_items else "blocked_no_vectors",
        "include_selected_organic_cofactor_scores": include_cofactor,
        "exclude_tuning_adjacent_queries": exclude_tuning_adjacent_queries,
        "candidate_pool_count": len(candidate_items),
        "relationship_query_count": len(query_items),
        "feature_dimension": feature_dimension,
        "metrics_by_variant": metrics_by_variant,
        "per_fingerprint": per_fingerprint,
        "samples": samples_by_variant,
        "notes": (
            "No model was trained for this surface; robust_l2 scaling was fit on "
            "candidate in-distribution vectors only."
        ),
    }


def _rank_query(
    *,
    query: dict[str, Any],
    candidates: list[dict[str, Any]],
    variant: str,
    robust_scaler: dict[str, list[float]],
    family_by_fingerprint: dict[str, list[str]],
    cofactor_sets: dict[str, list[str]],
) -> dict[str, Any]:
    query_vector = query["vector"]
    candidate_scores: list[tuple[float, dict[str, Any]]] = []
    for candidate in candidates:
        if variant == "cosine":
            score = _cosine(query_vector, candidate["vector"])
        elif variant == "robust_l2":
            score = -_l2(
                _apply_scaler(query_vector, robust_scaler),
                _apply_scaler(candidate["vector"], robust_scaler),
            )
        else:
            raise ValueError(f"unknown rank variant: {variant}")
        candidate_scores.append((score, candidate))
    ranked = [
        candidate
        for _, candidate in sorted(
            candidate_scores,
            key=lambda item: (-item[0], str(item[1]["entry_id"])),
        )
    ]
    query_fp = str(query.get("fingerprint_id") or "")
    query_families = set(family_by_fingerprint.get(query_fp, []))
    query_cofactors = set(cofactor_sets.get(query_fp, []))
    rank_exact = None
    rank_family = None
    rank_cofactor = None
    top_neighbors: list[dict[str, Any]] = []
    for index, candidate in enumerate(ranked, start=1):
        candidate_fp = str(candidate.get("fingerprint_id") or "")
        candidate_families = set(family_by_fingerprint.get(candidate_fp, []))
        candidate_cofactors = set(cofactor_sets.get(candidate_fp, []))
        exact = bool(candidate_fp and candidate_fp == query_fp)
        family = exact or bool(query_families & candidate_families)
        cofactor = bool(query_cofactors and query_cofactors & candidate_cofactors)
        if rank_exact is None and exact:
            rank_exact = index
        if rank_family is None and family:
            rank_family = index
        if rank_cofactor is None and cofactor:
            rank_cofactor = index
        if index <= 5:
            top_neighbors.append(
                {
                    "entry_id": candidate["entry_id"],
                    "fingerprint_id": candidate_fp,
                    "relationship": "exact"
                    if exact
                    else "same_family"
                    if family
                    else "shared_cofactor"
                    if cofactor
                    else "unrelated",
                }
            )
    return {
        "entry_id": query["entry_id"],
        "fingerprint_id": query_fp,
        "rank_exact": rank_exact,
        "rank_family": rank_family,
        "rank_cofactor": rank_cofactor,
        "top5_neighbors": top_neighbors,
    }


def _rank_metrics(rankings: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(rankings)
    metrics: dict[str, Any] = {"query_count": count}
    for relation in ("exact", "family", "cofactor"):
        ranks = [row.get(f"rank_{relation}") for row in rankings]
        present_ranks = [int(rank) for rank in ranks if rank is not None]
        for k in (1, 3, 5, 10):
            hits = sum(1 for rank in ranks if rank is not None and int(rank) <= k)
            metrics[f"{relation}_top{k}_any_rate"] = _round_rate(hits, count)
        metrics[f"{relation}_top1_rate"] = metrics[f"{relation}_top1_any_rate"]
        metrics[f"mrr_{relation}"] = _round_rate(
            sum((1.0 / rank) for rank in present_ranks),
            count,
        )
        metrics[f"median_rank_{relation}"] = (
            float(statistics.median(present_ranks)) if present_ranks else None
        )
    return metrics


def _per_fingerprint_metrics(rankings: list[dict[str, Any]]) -> dict[str, Any]:
    by_fingerprint: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rankings:
        by_fingerprint[str(row.get("fingerprint_id") or "")].append(row)
    summary: dict[str, Any] = {}
    for fingerprint_id, rows in sorted(by_fingerprint.items()):
        count = len(rows)
        summary[fingerprint_id] = {
            "query_count": count,
            "exact_top1_rate": _round_rate(
                sum(1 for row in rows if row.get("rank_exact") == 1), count
            ),
            "family_top3_any_rate": _round_rate(
                sum(
                    1
                    for row in rows
                    if row.get("rank_family") is not None and row["rank_family"] <= 3
                ),
                count,
            ),
            "cofactor_top3_any_rate": _round_rate(
                sum(
                    1
                    for row in rows
                    if row.get("rank_cofactor") is not None
                    and row["rank_cofactor"] <= 3
                ),
                count,
            ),
        }
    return summary


def _samples(rankings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in rankings[:12]:
        rows.append(
            {
                "entry_id": row["entry_id"],
                "true_fingerprint_id": row["fingerprint_id"],
                "ranks": {
                    "exact": row.get("rank_exact"),
                    "family": row.get("rank_family"),
                    "cofactor": row.get("rank_cofactor"),
                },
                "top5_neighbors": row["top5_neighbors"],
            }
        )
    return rows


def _robust_scaler(vectors: list[list[float]]) -> dict[str, list[float]]:
    if not vectors:
        return {"median": [], "scale": []}
    dimension = len(vectors[0])
    medians = []
    scales = []
    for index in range(dimension):
        values = [vector[index] for vector in vectors]
        median = statistics.median(values)
        sorted_values = sorted(values)
        q1 = sorted_values[int((len(sorted_values) - 1) * 0.25)]
        q3 = sorted_values[int((len(sorted_values) - 1) * 0.75)]
        scale = q3 - q1
        medians.append(float(median))
        scales.append(float(scale) if abs(scale) > 1e-12 else 1.0)
    return {"median": medians, "scale": scales}


def _apply_scaler(vector: list[float], scaler: dict[str, list[float]]) -> list[float]:
    medians = scaler["median"]
    scales = scaler["scale"]
    return [
        (float(value) - medians[index]) / scales[index]
        for index, value in enumerate(vector)
    ]


def _cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def _l2(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(left, right)))


def _round_rate(numerator: float, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(float(numerator) / float(denominator), 6)


def _tuning_adjacent_ids(previous_eval: dict[str, Any] | None) -> set[str]:
    if not previous_eval:
        return set()
    rows = previous_eval.get("tuning_adjacent_rows", {}).get("row_examples", [])
    return {
        str(row.get("entry_id"))
        for row in rows
        if isinstance(row, dict) and row.get("tuning_adjacent") and row.get("entry_id")
    }


def _headline(
    baseline_surface: dict[str, Any],
    augmented_surface: dict[str, Any],
    augmented_non_tuning: dict[str, Any],
) -> dict[str, Any]:
    baseline_cosine = baseline_surface["metrics_by_variant"]["cosine"]
    augmented_cosine = augmented_surface["metrics_by_variant"]["cosine"]
    augmented_non_tuning_cosine = augmented_non_tuning["metrics_by_variant"]["cosine"]
    delta_family_top3 = _delta(
        augmented_cosine.get("family_top3_any_rate"),
        baseline_cosine.get("family_top3_any_rate"),
    )
    delta_exact_top1 = _delta(
        augmented_cosine.get("exact_top1_rate"),
        baseline_cosine.get("exact_top1_rate"),
    )
    return {
        "status": "real_d11_cofactor_augmented_rerun_complete",
        "interpretation": (
            "The row-level sidecar blocker is cleared for a bounded D11 rerun. "
            "This artifact evaluates a cofactor-augmented predicted-geometry query "
            "representation using fixed persisted sidecar scores, without refitting "
            "models or tuning thresholds on heldout rows."
        ),
        "baseline_predicted_score_cosine_family_top3_any_rate": baseline_cosine.get(
            "family_top3_any_rate"
        ),
        "augmented_predicted_score_cosine_family_top3_any_rate": augmented_cosine.get(
            "family_top3_any_rate"
        ),
        "augmented_non_tuning_cosine_family_top3_any_rate": (
            augmented_non_tuning_cosine.get("family_top3_any_rate")
        ),
        "delta_family_top3_any_rate": delta_family_top3,
        "delta_exact_top1_rate": delta_exact_top1,
        "caveat": (
            "Organic cofactor scores are the documented ESM2-150M fallback source, "
            "not a strict reproduction of the missing original t6/t12 selected heads."
        ),
    }


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return round(float(left) - float(right), 6)


def _source_artifacts(source_paths: dict[str, Path | None]) -> dict[str, Any]:
    artifacts: dict[str, Any] = {}
    for name, path in sorted(source_paths.items()):
        if path is None:
            continue
        artifacts[name] = {
            "path": str(path),
            "exists": path.exists(),
            "sha256": _sha256(path) if path.exists() and path.is_file() else None,
        }
    return artifacts


def _report(audit: dict[str, Any]) -> str:
    lines = [
        "# D11 Mechanism Relationship Evaluation Cofactor Augmented",
        "",
        f"Run created: `{audit['created_utc']}`",
        "",
        "## Decision",
        "",
        audit["headline"]["interpretation"],
        "",
        "No labels, registries, ontologies, imports, production scoring, global "
        "thresholds, heldout splits, or model weights were changed.",
        "",
        "## Sidecar Gate",
        "",
        (
            f"- Row-class records: "
            f"{audit['selected_organic_cofactor_sidecar']['row_class_records']}."
        ),
        (
            f"- Entries with flavin/heme/PLP scores: "
            f"{audit['selected_organic_cofactor_sidecar']['entries_with_all_scores']}."
        ),
        (
            f"- Source counts: "
            f"{audit['selected_organic_cofactor_sidecar']['selected_source_counts']}."
        ),
        f"- Caveat: {audit['headline']['caveat']}",
        "",
        "## Relationship Rank Metrics",
        "",
        "| Surface | Variant | Queries | Exact top1 | Family top3 any | Family MRR | Notes |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for surface in audit["relationship_rank_metrics"].values():
        for variant in RANK_VARIANTS:
            metrics = surface["metrics_by_variant"][variant]
            lines.append(
                f"| {surface['display_name']} | `{variant}` | "
                f"{surface['relationship_query_count']} | "
                f"{metrics.get('exact_top1_rate')} | "
                f"{metrics.get('family_top3_any_rate')} | "
                f"{metrics.get('mrr_family')} | "
                f"{surface['notes']} |"
            )
    lines.extend(
        [
            "",
            "## Headline Delta",
            "",
            (
                "- Cosine family top3 any rate changed from "
                f"{audit['headline']['baseline_predicted_score_cosine_family_top3_any_rate']} "
                "to "
                f"{audit['headline']['augmented_predicted_score_cosine_family_top3_any_rate']} "
                f"(delta {audit['headline']['delta_family_top3_any_rate']})."
            ),
            (
                "- Non-tuning-adjacent augmented cosine family top3 any rate: "
                f"{audit['headline']['augmented_non_tuning_cosine_family_top3_any_rate']}."
            ),
            "",
            "## Next Gate",
            "",
            (
                "Use this artifact as the first cofactor-augmented D11 rerun. "
                "A stricter reproduction still requires the original t6/t12 sidecars, "
                "but the row-level blocker is no longer blocking D11 iteration."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _load_json(path: Path | None) -> Any:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
