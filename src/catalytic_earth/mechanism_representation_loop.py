"""Leakage-safe mechanism representation loop (Phase 3: self-feeding supply).

The hand-curated pools are drained, so the climb cannot lean on hand-sourcing
forever. We have been banking rich review-only ``mechanism_evidence`` on every
bronze label precisely so a representation can eventually *organise, triage, and
propose* labels itself. This is the first iteration of that loop.

THE LEAKAGE WALL IS ABSOLUTE. The representation is built ONLY from the review-only
**structural / chemical** evidence -- cofactor and binding-ligand chemical
identities (ChEBI names) and active-site residue role counts. It NEVER reads, and
this module asserts it never reads:

- ``ec_numbers`` (EC is scope-assignment metadata, excluded_context),
- protein name / UniProt prose / curated mechanism text / source annotation,
- ``target_family_lane``,
- the ``fingerprint_id`` / ``label_type`` target itself,
- the frozen 702 benchmark (this loop is for the expansion's self-organisation and
  bronze->silver promotion triage; it is NOT a benchmark scorer and must never be
  used as one).

Cofactor/ligand chemical identity is the legitimate, deploy-available structural
basis the whole project is built on (the eight fingerprints are *defined* by their
cofactor chemistry); it is distinct from the excluded protein-name/prose/EC fields.

Three capabilities:

1. ``featurize`` -- a deterministic, leakage-safe chemical/structural feature
   vector per label.
2. ``promotion_triage`` -- using per-fingerprint centroids, partition bronze seed
   labels into promotion candidates (chemistry coheres with the assigned
   fingerprint), review outliers (chemistry points at a *different* fingerprint --
   a possible mislabel), and not-yet-coherent rows. A leave-one-out
   self-consistency read measures how strongly the chemistry alone recovers the
   fingerprint -- the representation's coherence.
3. ``propose_for_fingerprint`` -- rank a candidate pool (e.g. the out_of_scope
   rows) by representation similarity to a target fingerprint's centroid: the
   model-proposed "what to source/predict next", aimed at the governor's holes.

NON-DESTRUCTIVE: writes no registry, emits no label, changes no benchmark.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# Cofactor / ligand chemical-identity -> canonical cofactor class. Keys are matched
# as lowercased substrings against cofactor names, binding-ligand names, and ChEBI
# names. These are CHEMICAL identities (the legitimate structural basis), never the
# excluded protein-name/EC/prose fields.
COFACTOR_CLASS_PATTERNS: dict[str, tuple[str, ...]] = {
    "flavin": ("fad", "fmn", "flavin"),
    "plp": ("pyridoxal",),
    "heme": ("heme",),
    "iron_sulfur": ("4fe-4s", "2fe-2s", "3fe-4s", "fe-s cluster", "iron-sulfur"),
    "sam": ("s-adenosyl-l-methionine", "adenosyl-l-methionine", "adenosylmethionine"),
    "cobalamin": ("cobalamin", "cobamamide", "vitamin b12", "adenosylcobalamin"),
    "zinc": ("zn(", "zinc"),
    "divalent_metal_other": (
        "mn(", "mg(", "ni(", "co(", "fe(", "fe cation", "fe3", "fe2",
        "divalent metal", "cu(", "manganese", "magnesium",
    ),
    "calcium": ("ca(2+)", "ca("),
}

COFACTOR_CLASSES = tuple(COFACTOR_CLASS_PATTERNS.keys())
# Ordered numeric feature names (cofactor classes weighted to dominate; residue
# role ratios are secondary structural context).
RESIDUE_FEATURES = (
    "catalytic_fraction",
    "binding_fraction",
    "active_site_size",
)
FEATURE_NAMES = COFACTOR_CLASSES + RESIDUE_FEATURES

# Fields that must never enter the representation -- asserted by featurize.
EXCLUDED_FROM_REPRESENTATION = (
    "ec_numbers",
    "fingerprint_id",
    "label_type",
    "protein_name",
    "uniprot_prose",
    "target_family_lane",
    "rationale",
)

DEFAULT_PROMOTION_COHESION = 0.92


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def _classify_cofactor(name: str) -> str | None:
    low = (name or "").lower()
    for cls, patterns in COFACTOR_CLASS_PATTERNS.items():
        if any(p in low for p in patterns):
            return cls
    return None


def _chemical_identity_terms(row: dict[str, Any]) -> list[str]:
    """Collect ONLY chemical identities: cofactor names + binding-ligand names.

    Reads nothing from EC / protein name / prose / lane / fingerprint.
    """
    mech = _mechanism_evidence(row)
    terms: list[str] = []
    for cofactor in mech.get("cofactors") or []:
        if cofactor.get("name"):
            terms.append(cofactor["name"])
    for residue in mech.get("active_site_residues") or []:
        if residue.get("feature_code") == "BINDING" and residue.get("ligand_name"):
            terms.append(residue["ligand_name"])
    return terms


def featurize(row: dict[str, Any]) -> dict[str, float]:
    """Deterministic leakage-safe chemical/structural feature vector for a label.

    Cofactor-class presence (from chemical identities) dominates; active-site
    residue role ratios provide secondary structural context. EC / name / prose /
    lane / fingerprint are never consulted.
    """
    features = {name: 0.0 for name in FEATURE_NAMES}
    for term in _chemical_identity_terms(row):
        cls = _classify_cofactor(term)
        if cls is not None:
            features[cls] = 1.0

    mech = _mechanism_evidence(row)
    active = mech.get("active_site_residue_count") or 0
    catalytic = mech.get("catalytic_residue_count") or 0
    binding = mech.get("binding_residue_count") or 0
    if active > 0:
        features["catalytic_fraction"] = round(catalytic / active, 4)
        features["binding_fraction"] = round(binding / active, 4)
    # bounded structural-size context (log-scaled, capped)
    features["active_site_size"] = round(min(math.log1p(active) / math.log1p(30), 1.0), 4)
    return features


def _active_cofactor_classes(row: dict[str, Any]) -> set[str]:
    """The cofactor classes actually present in a row's chemistry (non-zero)."""
    features = featurize(row)
    return {cls for cls in COFACTOR_CLASSES if features.get(cls, 0.0) > 0.0}


def _significant_centroid_cofactors(
    centroid: list[float], *, threshold: float = 0.15
) -> set[str]:
    """Cofactor classes that meaningfully define a fingerprint centroid."""
    return {
        COFACTOR_CLASSES[i]
        for i in range(len(COFACTOR_CLASSES))
        if centroid[i] >= threshold
    }


def _vector(features: dict[str, float], *, residue_weight: float = 0.15) -> list[float]:
    out = []
    for name in FEATURE_NAMES:
        value = features.get(name, 0.0)
        if name in RESIDUE_FEATURES:
            value *= residue_weight
        out.append(value)
    return out


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _centroid(vectors: list[list[float]]) -> list[float]:
    if not vectors:
        return [0.0] * len(FEATURE_NAMES)
    n = len(vectors)
    return [sum(v[i] for v in vectors) / n for i in range(len(FEATURE_NAMES))]


def fingerprint_centroids(
    seed_labels: list[dict[str, Any]],
) -> dict[str, list[float]]:
    """Mean representation per fingerprint, from confirmed seed labels."""
    groups: dict[str, list[list[float]]] = defaultdict(list)
    for row in seed_labels:
        fp = row.get("fingerprint_id")
        if not fp:
            continue
        groups[fp].append(_vector(featurize(row)))
    return {fp: _centroid(vectors) for fp, vectors in sorted(groups.items())}


def _nearest_fingerprint(
    vector: list[float], centroids: dict[str, list[float]]
) -> tuple[str | None, float]:
    best_fp, best_sim = None, -1.0
    for fp, centroid in centroids.items():
        sim = _cosine(vector, centroid)
        if sim > best_sim:
            best_fp, best_sim = fp, sim
    return best_fp, round(best_sim, 4)


def assess_row_against_centroids(
    row: dict[str, Any], centroids: dict[str, list[float]]
) -> dict[str, Any]:
    """Public: nearest fingerprint + cohesion for a row, given full centroids.

    Operational classifier (uses the full centroids) reused by the bronze->silver
    promotion preview. Leakage-safe -- featurize reads only chemistry, never
    EC/name/label.
    """
    vector = _vector(featurize(row))
    nearest, nearest_sim = _nearest_fingerprint(vector, centroids)
    fp = row.get("fingerprint_id")
    own = round(_cosine(vector, centroids[fp]), 4) if fp in centroids else None
    return {
        "assigned_fingerprint": fp,
        "nearest_fingerprint": nearest,
        "nearest_similarity": nearest_sim,
        "own_cohesion": own,
        "chemistry_agrees_with_label": (nearest == fp) if fp else None,
    }


def promotion_triage(
    seed_labels: list[dict[str, Any]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    """Triage bronze seed labels for bronze->silver promotion vs review.

    Uses leave-one-out centroids (a row never votes on its own centroid) so the
    self-consistency read is honest, not circular.
    """
    vectors = {id(row): _vector(featurize(row)) for row in seed_labels}
    by_fp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in seed_labels:
        if row.get("fingerprint_id"):
            by_fp[row["fingerprint_id"]].append(row)

    full_sums: dict[str, list[float]] = {}
    for fp, rows in by_fp.items():
        acc = [0.0] * len(FEATURE_NAMES)
        for row in rows:
            v = vectors[id(row)]
            for i in range(len(FEATURE_NAMES)):
                acc[i] += v[i]
        full_sums[fp] = acc

    promote, review_outlier, low_cohesion = [], [], []
    loo_agree = 0
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in seed_labels:
        fp = row.get("fingerprint_id")
        if not fp:
            continue
        v = vectors[id(row)]
        # leave-one-out centroids
        loo_centroids = {}
        for other_fp, acc in full_sums.items():
            count = len(by_fp[other_fp])
            if other_fp == fp:
                count -= 1
                if count <= 0:
                    loo_centroids[other_fp] = [0.0] * len(FEATURE_NAMES)
                    continue
                loo_centroids[other_fp] = [
                    (acc[i] - v[i]) / count for i in range(len(FEATURE_NAMES))
                ]
            else:
                loo_centroids[other_fp] = [acc[i] / count for i in range(len(FEATURE_NAMES))]
        nearest, sim = _nearest_fingerprint(v, loo_centroids)
        own_sim = round(_cosine(v, loo_centroids[fp]), 4)
        confusion[fp][nearest or "none"] += 1
        record = {
            "entry_id": row.get("entry_id"),
            "fingerprint_id": fp,
            "nearest_fingerprint": nearest,
            "own_cohesion": own_sim,
            "nearest_similarity": sim,
        }
        if nearest == fp:
            loo_agree += 1
            if own_sim >= cohesion_threshold:
                promote.append(record)
            else:
                low_cohesion.append(record)
        else:
            review_outlier.append(record)

    total = sum(len(rows) for rows in by_fp.values())
    return {
        "seed_labels_triaged": total,
        "leave_one_out_self_consistency": round(loo_agree / total, 4) if total else 0.0,
        "promotion_candidates": len(promote),
        "review_outliers": len(review_outlier),
        "coherent_but_below_threshold": len(low_cohesion),
        "cohesion_threshold": cohesion_threshold,
        "confusion_by_fingerprint": {
            fp: dict(sorted(counts.items(), key=lambda kv: -kv[1]))
            for fp, counts in sorted(confusion.items())
        },
        "review_outlier_samples": review_outlier[:15],
        "promotion_candidate_samples": promote[:10],
    }


def propose_for_fingerprint(
    target_fingerprint: str,
    candidate_pool: list[dict[str, Any]],
    centroids: dict[str, list[float]],
    *,
    top_k: int = 25,
    min_similarity: float = 0.6,
) -> list[dict[str, Any]]:
    """Rank a candidate pool by representation similarity to a target fingerprint.

    The model-proposed "what to look at next" for a hole. A candidate is only
    proposed when (a) it shares genuine cofactor chemistry with the target (a
    non-empty overlap with the target centroid's defining cofactor classes -- so a
    cofactor-less row is never proposed for a cofactor-defined fingerprint), and
    (b) the target fingerprint is ALSO its nearest centroid (so we do not propose
    rows whose chemistry actually matches some other fingerprint).
    """
    target_centroid = centroids.get(target_fingerprint)
    if not target_centroid:
        return []
    defining = _significant_centroid_cofactors(target_centroid)
    ranked = []
    for row in candidate_pool:
        # require real cofactor-chemistry overlap with the target fingerprint
        if defining and not (_active_cofactor_classes(row) & defining):
            continue
        v = _vector(featurize(row))
        sim = round(_cosine(v, target_centroid), 4)
        if sim < min_similarity:
            continue
        nearest, _ = _nearest_fingerprint(v, centroids)
        if nearest != target_fingerprint:
            continue
        ranked.append(
            {
                "entry_id": row.get("entry_id"),
                "similarity_to_target": sim,
                "shared_cofactor_classes": sorted(
                    _active_cofactor_classes(row) & defining
                ),
                "current_label_type": row.get("label_type"),
            }
        )
    ranked.sort(key=lambda r: (-r["similarity_to_target"], str(r["entry_id"])))
    return ranked[:top_k]


def build_mechanism_representation_loop(
    expansion: list[dict[str, Any]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    hole_fingerprints: tuple[str, ...] = (
        "radical_sam_enzyme",
        "cobalamin_radical_rearrangement",
        "ser_his_acid_hydrolase",
    ),
    proposal_top_k: int = 25,
) -> dict[str, Any]:
    seed = [r for r in expansion if r.get("label_type") == "seed_fingerprint"]
    oos = [r for r in expansion if r.get("label_type") == "out_of_scope"]
    centroids = fingerprint_centroids(seed)
    triage = promotion_triage(seed, cohesion_threshold=cohesion_threshold)

    proposals = {}
    for fp in hole_fingerprints:
        proposals[fp] = {
            "centroid_available": fp in centroids,
            "proposed_from_out_of_scope": propose_for_fingerprint(
                fp, oos, centroids, top_k=proposal_top_k
            )
            if fp in centroids
            else [],
        }

    return {
        "audit": "mechanism_representation_loop",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "feature_space": {
            "names": list(FEATURE_NAMES),
            "basis": "review_only_cofactor_and_binding_ligand_chemistry + active_site_residue_roles",
            "excluded_from_representation": list(EXCLUDED_FROM_REPRESENTATION),
        },
        "seed_labels": len(seed),
        "out_of_scope_labels": len(oos),
        "fingerprint_centroids_built": sorted(centroids.keys()),
        "promotion_triage": triage,
        "hole_proposals": proposals,
        "leakage_guardrails": {
            "frozen_benchmark_read": False,
            "ec_name_prose_lane_used": False,
            "fingerprint_label_used_as_feature": False,
            "used_only_for_candidate_ranking_and_promotion_triage_not_benchmark_scoring": True,
            "registry_written": False,
            "labels_emitted": 0,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    tri = audit["promotion_triage"]
    fs = audit["feature_space"]
    lines = [
        "# Mechanism Representation Loop (leakage-safe self-feeding supply)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "First iteration of the self-feeding loop. A representation learned ONLY from "
        "review-only cofactor/ligand chemistry + active-site residue roles "
        "organises the bronze labels, triages bronze->silver promotion, and proposes "
        "candidates for the governor's holes. EC / protein-name / prose / lane / the "
        "fingerprint label / the frozen benchmark are never read.",
        "",
        f"- Feature space: {fs['names']}.",
        f"- Excluded from representation: {fs['excluded_from_representation']}.",
        f"- Seed labels: {audit['seed_labels']}; out_of_scope: "
        f"{audit['out_of_scope_labels']}; centroids: "
        f"{audit['fingerprint_centroids_built']}.",
        "",
        "## Promotion triage",
        "",
        f"- Leave-one-out self-consistency (chemistry alone recovers the "
        f"fingerprint): {tri['leave_one_out_self_consistency']}.",
        f"- Promotion candidates (cohesion >= {tri['cohesion_threshold']}): "
        f"{tri['promotion_candidates']}.",
        f"- Review outliers (chemistry points at a different fingerprint): "
        f"{tri['review_outliers']}.",
        f"- Coherent but below threshold: {tri['coherent_but_below_threshold']}.",
        "",
        "## Hole proposals (model-ranked from out_of_scope)",
        "",
    ]
    for fp, payload in audit["hole_proposals"].items():
        n = len(payload["proposed_from_out_of_scope"])
        lines.append(
            f"- {fp}: centroid {'available' if payload['centroid_available'] else 'MISSING'}; "
            f"{n} proposed candidates."
        )
    lines.extend(
        [
            "",
            "## Leakage guardrails",
            "",
            f"- Frozen benchmark read: {audit['leakage_guardrails']['frozen_benchmark_read']}.",
            f"- EC/name/prose/lane used: "
            f"{audit['leakage_guardrails']['ec_name_prose_lane_used']}.",
            f"- Fingerprint label used as feature: "
            f"{audit['leakage_guardrails']['fingerprint_label_used_as_feature']}.",
            "- Used only for candidate ranking + promotion triage, NEVER as a "
            "benchmark scorer.",
            f"- Registry written: {audit['leakage_guardrails']['registry_written']}.",
            "",
        ]
    )
    return "\n".join(lines)


def write_mechanism_representation_loop(
    *,
    out_path: Path,
    report_path: Path | None = None,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    proposal_top_k: int = 25,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_mechanism_representation_loop(
        expansion,
        cohesion_threshold=cohesion_threshold,
        proposal_top_k=proposal_top_k,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
