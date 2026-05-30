"""D11 mechanism relationship surface evaluation.

This module measures how faithfully a row-keyed representation places mechanism
*relationships* (not just held-out rows): held-out queries are ranked against an
in-distribution atlas and scored under rank-based, scale-free metrics for three
pre-registered relationship types -- exact fingerprint, shared ontology family,
and shared normalized cofactor.

It exists to extend the D11 hygiene tier with a *real protein language model*
sequence surface (persisted ESM2-150M whole-sequence embeddings) alongside the
deterministic k-mer control, under one identical pipeline. The comparison is the
deliverable: does a faithful sequence representation organize the mechanism
relationship space better than a bag-of-k-mer control?

Scope guardrails (see docs/session_decision_record_20260530.md):
  * Sequence inputs are amino-acid-sequence-only. No geometry-derived cofactor
    evidence enters a sequence surface.
  * Nothing here trains, refits, or tunes on held-out rows. Robust standardization
    statistics are derived from the in-distribution atlas only, never from queries.
  * This is a hygiene/feasibility surface comparison. It does NOT constitute the
    real D11 pass, which remains blocked on row-level selected organic-cofactor
    scores (flavin/heme/PLP). That gate is preserved in the emitted artifact.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .sequence_cofactor_channel import FINGERPRINT_REQUIRED_COFACTOR_FAMILY

SCHEMA_VERSION = "mechanism_relationship_surface_eval.v0"
DEFAULT_K_VALUES = (1, 3, 5, 10)
DEFAULT_VARIANTS = ("cosine", "l2", "robust_cosine", "robust_l2")
RELATIONSHIP_TYPES = ("exact", "family", "cofactor")
# Floor for per-dimension robust scale so near-constant dimensions cannot explode.
ROBUST_IQR_FLOOR = 1e-6


# --------------------------------------------------------------------------- #
# Registries
# --------------------------------------------------------------------------- #
def load_fingerprint_family_map(ontology_path: Path) -> dict[str, str]:
    """Map fingerprint_id -> ontology family id from the mechanism ontology."""
    ontology = json.loads(Path(ontology_path).read_text(encoding="utf-8"))
    family_map: dict[str, str] = {}
    for family in ontology.get("families", []):
        family_id = str(family.get("id"))
        for fingerprint_id in family.get("fingerprint_ids", []):
            family_map[str(fingerprint_id)] = family_id
    return family_map


def relationship_type(
    query_fp: str | None,
    candidate_fp: str | None,
    family_map: dict[str, str],
    cofactor_map: dict[str, str] | None = None,
) -> str:
    """Classify the strongest pre-registered relationship between two rows.

    Order of strength: exact fingerprint > shared ontology family > shared
    normalized cofactor family. Returns "unrelated" when none apply. The cofactor
    map defaults to the canonical fingerprint->required-cofactor mapping.
    """
    if cofactor_map is None:
        cofactor_map = FINGERPRINT_REQUIRED_COFACTOR_FAMILY
    if not query_fp or not candidate_fp:
        return "unrelated"
    if query_fp == candidate_fp:
        return "exact"
    if (
        query_fp in family_map
        and candidate_fp in family_map
        and family_map[query_fp] == family_map[candidate_fp]
    ):
        return "family"
    q_cof = cofactor_map.get(query_fp)
    c_cof = cofactor_map.get(candidate_fp)
    if q_cof and c_cof and q_cof == c_cof:
        return "cofactor"
    return "unrelated"


def _relationship_satisfies(observed: str, target: str) -> bool:
    """Whether an observed relationship counts as a hit for a target type.

    Relationships are nested: an exact match is also a family and cofactor match
    when those broader registries agree, but to keep the three metric families
    independent and interpretable we score each target by its own predicate using
    the nesting exact => family => cofactor only where the registries imply it.
    Here `observed` is already the *strongest* type, so we expand it.
    """
    if observed == "unrelated":
        return False
    strength = {"exact": 3, "family": 2, "cofactor": 1}
    # exact implies the rows share a fingerprint; family/cofactor are broader bands.
    # For target "exact" only an exact observation counts. For "family" an exact or
    # family observation counts. For "cofactor" exact/family/cofactor all count only
    # when they actually share a cofactor; since `observed` is the strongest single
    # band we treat the bands as a monotone ladder for hit-counting.
    return strength.get(observed, 0) >= strength.get(target, 99)


# --------------------------------------------------------------------------- #
# Vector operations (pure stdlib)
# --------------------------------------------------------------------------- #
def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def _norm(a: Sequence[float]) -> float:
    return math.sqrt(math.fsum(x * x for x in a))


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    na, nb = _norm(a), _norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return _dot(a, b) / (na * nb)


def negative_l2(a: Sequence[float], b: Sequence[float]) -> float:
    """Return -||a-b|| so that, like cosine, larger is nearer."""
    return -math.sqrt(math.fsum((x - y) * (x - y) for x, y in zip(a, b)))


def robust_standardizer(atlas_vectors: list[list[float]]) -> tuple[list[float], list[float]]:
    """Per-dimension median and IQR computed on the atlas only (no query leakage)."""
    if not atlas_vectors:
        return [], []
    dim = len(atlas_vectors[0])
    medians: list[float] = []
    scales: list[float] = []
    for j in range(dim):
        column = [vec[j] for vec in atlas_vectors]
        med = statistics.median(column)
        ordered = sorted(column)
        q1 = _quantile(ordered, 0.25)
        q3 = _quantile(ordered, 0.75)
        iqr = max(q3 - q1, ROBUST_IQR_FLOOR)
        medians.append(med)
        scales.append(iqr)
    return medians, scales


def _quantile(ordered: list[float], q: float) -> float:
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return ordered[0]
    pos = q * (len(ordered) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def apply_robust(vec: Sequence[float], medians: list[float], scales: list[float]) -> list[float]:
    return [(x - m) / s for x, m, s in zip(vec, medians, scales)]


# --------------------------------------------------------------------------- #
# Ranking + metrics
# --------------------------------------------------------------------------- #
def _query_metrics(
    ranked: list[str],
    k_values: tuple[int, ...],
    pool_count: int,
) -> dict[str, dict[str, Any]]:
    """Per-query, per-relationship-type rank outcomes."""
    out: dict[str, dict[str, Any]] = {}
    for target in RELATIONSHIP_TYPES:
        hits = [i for i, observed in enumerate(ranked) if _relationship_satisfies(observed, target)]
        first_rank = (hits[0] + 1) if hits else None
        out[target] = {
            "first_rank": first_rank,
            "reciprocal_rank": (1.0 / first_rank) if first_rank else 0.0,
            "top1": bool(hits and hits[0] == 0),
            "topk_any": {k: bool(any(i < k for i in hits)) for k in k_values},
            "rank_for_median": first_rank if first_rank else pool_count + 1,
        }
    return out


def evaluate_relationship_surface(
    *,
    surface_id: str,
    display_name: str,
    surface_kind: str,
    queries: list[dict[str, Any]],
    atlas: list[dict[str, Any]],
    family_map: dict[str, str],
    variants: tuple[str, ...] = DEFAULT_VARIANTS,
    k_values: tuple[int, ...] = DEFAULT_K_VALUES,
    note: str = "",
) -> dict[str, Any]:
    """Evaluate one representation surface across distance variants.

    `queries` and `atlas` are lists of {entry_id, vector, true_fingerprint_id}.
    Robust variants standardize with atlas-only statistics, so held-out queries
    never influence the representation scaling.
    """
    atlas_vectors = [row["vector"] for row in atlas]
    medians, scales = robust_standardizer(atlas_vectors)
    robust_atlas = [
        {**row, "vector": apply_robust(row["vector"], medians, scales)} for row in atlas
    ]

    metrics_by_variant: dict[str, Any] = {}
    for variant in variants:
        if variant == "cosine":
            sim, use_atlas, transform = cosine_similarity, atlas, None
        elif variant == "l2":
            sim, use_atlas, transform = negative_l2, atlas, None
        elif variant == "robust_cosine":
            sim, use_atlas, transform = cosine_similarity, robust_atlas, (medians, scales)
        elif variant == "robust_l2":
            sim, use_atlas, transform = negative_l2, robust_atlas, (medians, scales)
        else:
            raise ValueError(f"unknown variant: {variant}")

        per_query: list[dict[str, Any]] = []
        for q in queries:
            qvec = q["vector"] if transform is None else apply_robust(q["vector"], medians, scales)
            ranked = _ranked_relationships_excluding(qvec, q, use_atlas, family_map, sim)
            per_query.append(_query_metrics(ranked, k_values, len(use_atlas)))

        metrics_by_variant[variant] = _aggregate(per_query, k_values)

    return {
        "surface_id": surface_id,
        "display_name": display_name,
        "surface_kind": surface_kind,
        "status": "computed",
        "relationship_query_count": len(queries),
        "candidate_pool_count": len(atlas),
        "feature_dimension": len(atlas_vectors[0]) if atlas_vectors else 0,
        "note": note,
        "metrics_by_variant": metrics_by_variant,
    }


def _ranked_relationships_excluding(
    query_vec: list[float],
    query_row: dict[str, Any],
    atlas: list[dict[str, Any]],
    family_map: dict[str, str],
    similarity,
) -> list[str]:
    query_id = query_row["entry_id"]
    query_fp = query_row["true_fingerprint_id"]
    scored = [
        (similarity(query_vec, row["vector"]), row)
        for row in atlas
        if row["entry_id"] != query_id
    ]
    scored.sort(key=lambda item: (-item[0], item[1]["entry_id"]))
    return [relationship_type(query_fp, row["true_fingerprint_id"], family_map) for _, row in scored]


def _aggregate(per_query: list[dict[str, Any]], k_values: tuple[int, ...]) -> dict[str, Any]:
    n = len(per_query) or 1
    out: dict[str, Any] = {}
    for target in RELATIONSHIP_TYPES:
        rows = [pq[target] for pq in per_query]
        out[f"{target}_top1_rate"] = round(sum(r["top1"] for r in rows) / n, 6)
        for k in k_values:
            rate = sum(r["topk_any"][k] for r in rows) / n
            out[f"{target}_top{k}_any_rate"] = round(rate, 6)
        out[f"mrr_{target}"] = round(sum(r["reciprocal_rank"] for r in rows) / n, 6)
        out[f"median_rank_{target}"] = float(
            statistics.median([r["rank_for_median"] for r in rows])
        )
    return out


# --------------------------------------------------------------------------- #
# Surface loaders
# --------------------------------------------------------------------------- #
def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def load_dense_surface(
    jsonl_path: Path,
    *,
    vector_key: str = "embedding",
) -> dict[str, dict[str, Any]]:
    """Load a dense per-row embedding surface keyed by entry_id."""
    surface: dict[str, dict[str, Any]] = {}
    for row in _read_jsonl(jsonl_path):
        entry_id = str(row.get("entry_id") or "")
        if not entry_id:
            continue
        surface[entry_id] = {
            "entry_id": entry_id,
            "vector": [float(x) for x in row[vector_key]],
            "split_assignment": row.get("split_assignment"),
            "true_fingerprint_id": row.get("true_fingerprint_id"),
        }
    return surface


def load_sparse_kmer_surface(
    jsonl_path: Path,
    *,
    metadata_by_entry: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Load the sparse deterministic k-mer control and densify to a fixed key order.

    The k-mer sidecar does not carry split/fingerprint, so those are joined from
    `metadata_by_entry` (the ESM2-150M surface) by entry_id. Densification uses the
    union of all sparse keys in a fixed sorted order so every row shares a basis.
    """
    raw_rows = _read_jsonl(jsonl_path)
    key_union: set[str] = set()
    for row in raw_rows:
        key_union.update((row.get("raw_embedding") or {}).keys())
    keys = sorted(key_union)
    surface: dict[str, dict[str, Any]] = {}
    for row in raw_rows:
        entry_id = str(row.get("entry_id") or "")
        if not entry_id:
            continue
        sparse = row.get("raw_embedding") or {}
        meta = metadata_by_entry.get(entry_id, {})
        surface[entry_id] = {
            "entry_id": entry_id,
            "vector": [float(sparse.get(k, 0.0)) for k in keys],
            "split_assignment": meta.get("split_assignment"),
            "true_fingerprint_id": meta.get("true_fingerprint_id"),
        }
    return surface


def _split_into_query_atlas(
    surface: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Held-out rows carrying a fingerprint are queries; in-distribution ones are the atlas."""
    queries = [
        row
        for row in surface.values()
        if row["split_assignment"] == "heldout" and row["true_fingerprint_id"]
    ]
    atlas = [
        row
        for row in surface.values()
        if row["split_assignment"] == "in_distribution" and row["true_fingerprint_id"]
    ]
    queries.sort(key=lambda r: r["entry_id"])
    atlas.sort(key=lambda r: r["entry_id"])
    return queries, atlas


# --------------------------------------------------------------------------- #
# Build + write
# --------------------------------------------------------------------------- #
def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_mechanism_relationship_surface_eval(
    *,
    esm2_150m_path: Path,
    ontology_path: Path,
    kmer_path: Path | None = None,
    variants: tuple[str, ...] = DEFAULT_VARIANTS,
    k_values: tuple[int, ...] = DEFAULT_K_VALUES,
) -> dict[str, Any]:
    family_map = load_fingerprint_family_map(ontology_path)
    esm_surface = load_dense_surface(esm2_150m_path, vector_key="embedding")
    esm_queries, esm_atlas = _split_into_query_atlas(esm_surface)

    surfaces: list[dict[str, Any]] = []
    surfaces.append(
        evaluate_relationship_surface(
            surface_id="esm2_150m_whole_sequence",
            display_name="ESM2-150M whole-sequence pooled embedding (real PLM)",
            surface_kind="sequence_plm",
            queries=esm_queries,
            atlas=esm_atlas,
            family_map=family_map,
            variants=variants,
            k_values=k_values,
            note=(
                "high-information sequence-only PLM representation; "
                "amino-acid-sequence-only, no geometry-derived inputs"
            ),
        )
    )

    if kmer_path is not None and Path(kmer_path).exists():
        kmer_surface = load_sparse_kmer_surface(kmer_path, metadata_by_entry=esm_surface)
        kmer_queries, kmer_atlas = _split_into_query_atlas(kmer_surface)
        surfaces.append(
            evaluate_relationship_surface(
                surface_id="sequence_kmer_control",
                display_name="Deterministic sequence k-mer control vector",
                surface_kind="sequence_only_control",
                queries=kmer_queries,
                atlas=kmer_atlas,
                family_map=family_map,
                variants=variants,
                k_values=k_values,
                note="known-weak deterministic bag-of-k-mer control under the same pipeline",
            )
        )

    comparison = _surface_comparison(surfaces)
    source_artifacts = {
        "esm2_150m_embeddings": {
            "path": str(esm2_150m_path),
            "sha256": _sha256(esm2_150m_path),
        },
        "mechanism_ontology": {
            "path": str(ontology_path),
            "sha256": _sha256(ontology_path),
        },
    }
    if kmer_path is not None and Path(kmer_path).exists():
        source_artifacts["sequence_kmer_sidecar"] = {
            "path": str(kmer_path),
            "sha256": _sha256(kmer_path),
        }

    return {
        "artifact_id": "v3_mechanism_relationship_plm_surface_current702_20260530",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 hygiene-tier relationship faithfulness: add a real PLM sequence "
            "surface alongside the k-mer control under one identical rank-based "
            "pipeline. Comparative claim only."
        ),
        "pre_registered_relationships": {
            "exact": "identical mechanism fingerprint_id",
            "family": "shared mechanism ontology family id",
            "cofactor": "shared normalized required cofactor family",
            "defined_before_reading_predictions": True,
        },
        "split_definition": {
            "query": "held-out rows carrying a known mechanism fingerprint",
            "atlas": "in-distribution rows carrying a known mechanism fingerprint",
            "robust_scaling_statistics": "atlas_only_no_query_leakage",
        },
        "surfaces": surfaces,
        "surface_comparison": comparison,
        "real_d11_pass": {
            "status": "blocked_missing_row_level_cofactor_channel_scores",
            "reason": (
                "This adds a sequence-PLM hygiene surface. The real D11 pass still "
                "requires row-level selected organic-cofactor scores (flavin/heme/PLP) "
                "and a cofactor-augmented predicted-geometry query representation."
            ),
        },
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "no_geometry_derived_cofactor_inputs": True,
            "no_training_or_refit": True,
            "no_heldout_tuning": True,
            "labels_registries_thresholds_changed": False,
        },
        "source_artifacts": source_artifacts,
    }


def _surface_comparison(surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    """Headline comparative read across surfaces on the robust_cosine variant."""
    by_id = {s["surface_id"]: s for s in surfaces}
    plm = by_id.get("esm2_150m_whole_sequence")
    kmer = by_id.get("sequence_kmer_control")
    if not plm or not kmer:
        return {"status": "single_surface_only"}
    deltas: dict[str, Any] = {}
    for variant in plm["metrics_by_variant"]:
        if variant not in kmer["metrics_by_variant"]:
            continue
        p = plm["metrics_by_variant"][variant]
        k = kmer["metrics_by_variant"][variant]
        deltas[variant] = {
            metric: round(p[metric] - k[metric], 6)
            for metric in (
                "exact_top1_rate",
                "exact_top3_any_rate",
                "family_top3_any_rate",
                "mrr_family",
                "mrr_exact",
                "cofactor_top3_any_rate",
            )
            if metric in p and metric in k
        }
    plm_better = sum(
        1 for v in deltas.values() for val in v.values() if val > 0
    )
    plm_worse = sum(1 for v in deltas.values() for val in v.values() if val < 0)
    return {
        "headline_variant": "robust_cosine",
        "plm_minus_kmer_deltas": deltas,
        "plm_better_metric_count": plm_better,
        "plm_worse_metric_count": plm_worse,
        "verdict": (
            "plm_organizes_relationship_space_better"
            if plm_better > plm_worse
            else "no_clear_plm_advantage"
        ),
    }


def write_mechanism_relationship_surface_eval(
    *,
    esm2_150m_path: Path,
    ontology_path: Path,
    out_path: Path,
    kmer_path: Path | None = None,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_relationship_surface_eval(
        esm2_150m_path=esm2_150m_path,
        ontology_path=ontology_path,
        kmer_path=kmer_path,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_report(audit), encoding="utf-8")
    return audit


def _render_report(audit: dict[str, Any]) -> str:
    lines = [
        "# D11 Mechanism Relationship PLM Surface",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Relationship Rank Metrics (robust_cosine)",
        "",
        "| Surface | Queries | Exact top1 | Family top3 any | Family MRR | Cofactor top3 any |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for surface in audit["surfaces"]:
        m = surface["metrics_by_variant"].get("robust_cosine", {})
        lines.append(
            f"| {surface['display_name']} | {surface['relationship_query_count']} | "
            f"{m.get('exact_top1_rate')} | {m.get('family_top3_any_rate')} | "
            f"{m.get('mrr_family')} | {m.get('cofactor_top3_any_rate')} |"
        )
    comp = audit.get("surface_comparison", {})
    lines += [
        "",
        "## PLM vs k-mer",
        "",
        f"- Verdict: `{comp.get('verdict')}`.",
        f"- PLM-better metrics: {comp.get('plm_better_metric_count')}; "
        f"PLM-worse: {comp.get('plm_worse_metric_count')}.",
        "",
        "## Real D11 pass",
        "",
        f"- Status: `{audit['real_d11_pass']['status']}`.",
        f"- {audit['real_d11_pass']['reason']}",
    ]
    return "\n".join(lines) + "\n"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
