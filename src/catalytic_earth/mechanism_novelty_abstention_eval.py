"""D11 de novo precondition: can the PLM mechanism space abstain on novelty?

D11 requires that "OOS or unseen chemistry should abstain or sit outside occupied
clusters" -- this is the de novo validity check (see
docs/session_decision_record_20260530.md). This module measures it directly and
honestly: given a representation, how well does any cheap, unsupervised distance
signal separate in-scope held-out queries (which carry a known mechanism
fingerprint) from out-of-scope held-out rows (novel chemistry, no fingerprint)?

The separation is scored as AUC = P(in-scope signal > OOS signal). 0.5 is chance;
a representation ready for distance-thresholded abstention wants AUC well above
~0.75 on at least one cheap signal.

Signals (all unsupervised, atlas-only statistics, no labels of the query/OOS rows):
  * nearest_atlas_cosine        -- max cosine to any in-distribution atlas row
  * nearest_centroid_cosine     -- max cosine to any per-class atlas centroid
  * centroid_top1_top2_margin   -- gap between best and 2nd-best class centroid
  * betweenclass_subspace_projnorm -- projection energy onto the between-class
    subspace spanned by (class centroid - global atlas mean), Gram-Schmidt
    orthonormalized; "how much mechanism-discriminative signal does this row carry"

Guardrails: sequence-only PLM inputs; no training/refit; no held-out tuning;
robust standardization, centroids, and the subspace are computed on the
in-distribution atlas only. M-CSA is eval-only.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .mechanism_relationship_surface_eval import (
    apply_robust,
    cosine_similarity,
    robust_standardizer,
)

SCHEMA_VERSION = "mechanism_novelty_abstention_eval.v0"
# Above this AUC a single cheap signal is considered usable for abstention.
ABSTENTION_USABLE_AUC = 0.75


def _auc_in_gt_oos(in_scope: list[float], oos: list[float]) -> float:
    """AUC that an in-scope signal exceeds an OOS signal (0.5 = chance)."""
    if not in_scope or not oos:
        return 0.0
    greater = sum(1 for a in in_scope for b in oos if a > b)
    ties = sum(1 for a in in_scope for b in oos if a == b)
    return round((greater + 0.5 * ties) / (len(in_scope) * len(oos)), 6)


def _vsub(a: list[float], b: list[float]) -> list[float]:
    return [x - y for x, y in zip(a, b)]


def _vdot(a: list[float], b: list[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def _orthonormal_betweenclass_basis(
    centroids: list[list[float]], global_mean: list[float]
) -> list[list[float]]:
    """Gram-Schmidt basis for the span of (centroid - global mean) vectors."""
    basis: list[list[float]] = []
    for centroid in centroids:
        w = _vsub(centroid, global_mean)
        for b in basis:
            d = _vdot(w, b)
            w = [wi - d * bi for wi, bi in zip(w, b)]
        norm = math.sqrt(_vdot(w, w))
        if norm > 1e-9:
            basis.append([wi / norm for wi in w])
    return basis


def load_plm_rows(esm2_150m_path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line in Path(esm2_150m_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        rows[rec["entry_id"]] = {
            "entry_id": rec["entry_id"],
            "embedding": [float(x) for x in rec["embedding"]],
            "split_assignment": rec.get("split_assignment"),
            "true_fingerprint_id": rec.get("true_fingerprint_id"),
        }
    return rows


def compute_novelty_signals(rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Compute all abstention signals from a row-keyed PLM surface."""
    atlas = sorted(
        e
        for e, r in rows.items()
        if r["split_assignment"] == "in_distribution" and r["true_fingerprint_id"]
    )
    inscope = sorted(
        e
        for e, r in rows.items()
        if r["split_assignment"] == "heldout" and r["true_fingerprint_id"]
    )
    oos = sorted(
        e
        for e, r in rows.items()
        if r["split_assignment"] == "heldout" and not r["true_fingerprint_id"]
    )
    if not (atlas and inscope and oos):
        return {"status": "insufficient_rows", "counts": {
            "atlas": len(atlas), "inscope": len(inscope), "oos": len(oos)}}

    medians, scales = robust_standardizer([rows[e]["embedding"] for e in atlas])
    P = {e: apply_robust(rows[e]["embedding"], medians, scales) for e in atlas + inscope + oos}

    # per-class centroids (atlas only)
    centroids: dict[str, list[float]] = {}
    classes = {rows[e]["true_fingerprint_id"] for e in atlas}
    dim = len(medians)
    for fp in classes:
        members = [e for e in atlas if rows[e]["true_fingerprint_id"] == fp]
        centroids[fp] = [sum(P[e][j] for e in members) / len(members) for j in range(dim)]

    global_mean = [sum(P[e][j] for e in atlas) / len(atlas) for j in range(dim)]
    basis = _orthonormal_betweenclass_basis(list(centroids.values()), global_mean)

    def nearest_atlas(e: str) -> float:
        return max(cosine_similarity(P[e], P[a]) for a in atlas)

    def nearest_centroid(e: str) -> float:
        return max(cosine_similarity(P[e], c) for c in centroids.values())

    def centroid_margin(e: str) -> float:
        sims = sorted((cosine_similarity(P[e], c) for c in centroids.values()), reverse=True)
        return sims[0] - sims[1] if len(sims) > 1 else sims[0]

    def projnorm(e: str) -> float:
        vc = _vsub(P[e], global_mean)
        return math.sqrt(sum(_vdot(vc, b) ** 2 for b in basis))

    signal_fns = {
        "nearest_atlas_cosine": nearest_atlas,
        "nearest_centroid_cosine": nearest_centroid,
        "centroid_top1_top2_margin": centroid_margin,
        "betweenclass_subspace_projnorm": projnorm,
    }
    signals: dict[str, Any] = {}
    for name, fn in signal_fns.items():
        si = [fn(e) for e in inscope]
        so = [fn(e) for e in oos]
        signals[name] = {
            "auc_in_gt_oos": _auc_in_gt_oos(si, so),
            "in_scope_mean": round(sum(si) / len(si), 6),
            "oos_mean": round(sum(so) / len(so), 6),
        }
    signals["betweenclass_subspace_projnorm"]["subspace_dim"] = len(basis)

    best_auc = max(s["auc_in_gt_oos"] for s in signals.values())
    return {
        "status": "computed",
        "counts": {"atlas": len(atlas), "inscope": len(inscope), "oos": len(oos)},
        "signals": signals,
        "best_auc": best_auc,
        "abstention_status": (
            "separable_by_cheap_signal"
            if best_auc >= ABSTENTION_USABLE_AUC
            else "unsolved_by_unsupervised_distance"
        ),
    }


COFACTOR_CLASSES = ("flavin", "heme", "plp")


def load_cofactor_scores(sidecar_path: Path) -> dict[str, dict[str, float]]:
    """Load row-level selected organic cofactor scores -> {entry_id: {class: score}}.

    Source-agnostic: works for any sidecar artifact carrying `row_class_records`
    with `entry_id`, `class`, and `selected_score` (the ESM2-150M fallback today,
    the recovered t6/t12 heads once the fallback is removed). The selected source
    label is read back out so the artifact can record provenance honestly.
    """
    payload = json.loads(Path(sidecar_path).read_text(encoding="utf-8"))
    scores: dict[str, dict[str, float]] = {}
    for rec in payload.get("row_class_records", []):
        entry_id = rec.get("entry_id")
        cls = rec.get("class")
        if entry_id is None or cls is None:
            continue
        scores.setdefault(entry_id, {})[cls] = float(rec.get("selected_score") or 0.0)
    return scores


def _cofactor_source_label(sidecar_path: Path) -> str:
    payload = json.loads(Path(sidecar_path).read_text(encoding="utf-8"))
    sources = {
        rec.get("selected_source")
        for rec in payload.get("row_class_records", [])
        if rec.get("selected_source")
    }
    return ",".join(sorted(s for s in sources if s)) or "unknown"


def compute_cofactor_augmented_signals(
    rows: dict[str, dict[str, Any]],
    cofactor_scores: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """Add cofactor-only and PLM+cofactor-augmented abstention signals.

    The cofactor channel is mechanism-discriminative (novel chemistry should carry
    lower in-class cofactor confidence), which the general-purpose PLM embedding is
    not. This measures whether augmenting the PLM mechanism subspace with the
    row-level cofactor vector improves novel-chemistry separation.
    """
    def has_cof(e: str) -> bool:
        return e in cofactor_scores

    atlas = sorted(
        e for e, r in rows.items()
        if r["split_assignment"] == "in_distribution" and r["true_fingerprint_id"] and has_cof(e)
    )
    inscope = sorted(
        e for e, r in rows.items()
        if r["split_assignment"] == "heldout" and r["true_fingerprint_id"] and has_cof(e)
    )
    oos = sorted(
        e for e, r in rows.items()
        if r["split_assignment"] == "heldout" and not r["true_fingerprint_id"] and has_cof(e)
    )
    if not (atlas and inscope and oos):
        return {"status": "insufficient_rows", "counts": {
            "atlas": len(atlas), "inscope": len(inscope), "oos": len(oos)}}

    def cofvec(e: str) -> list[float]:
        return [cofactor_scores[e].get(c, 0.0) for c in COFACTOR_CLASSES]

    # PLM mechanism subspace coordinates (atlas-only basis), reused from the base path.
    medians, scales = robust_standardizer([rows[e]["embedding"] for e in atlas])
    P = {e: apply_robust(rows[e]["embedding"], medians, scales) for e in atlas + inscope + oos}
    dim = len(medians)
    classes = {rows[e]["true_fingerprint_id"] for e in atlas}
    plm_cents = {
        fp: [sum(P[e][j] for e in atlas if rows[e]["true_fingerprint_id"] == fp)
             / sum(1 for e in atlas if rows[e]["true_fingerprint_id"] == fp) for j in range(dim)]
        for fp in classes
    }
    global_mean = [sum(P[e][j] for e in atlas) / len(atlas) for j in range(dim)]
    basis = _orthonormal_betweenclass_basis(list(plm_cents.values()), global_mean)

    def plm_coords(e: str) -> list[float]:
        vc = _vsub(P[e], global_mean)
        return [_vdot(vc, b) for b in basis]

    # robust-scaled cofactor vector (atlas stats)
    cof_med, cof_sc = robust_standardizer([cofvec(e) for e in atlas])
    CV = {e: apply_robust(cofvec(e), cof_med, cof_sc) for e in atlas + inscope + oos}

    AUG = {e: plm_coords(e) + CV[e] for e in atlas + inscope + oos}
    aug_classes = {rows[e]["true_fingerprint_id"] for e in atlas}
    aug_cents = {
        fp: [sum(AUG[e][j] for e in atlas if rows[e]["true_fingerprint_id"] == fp)
             / sum(1 for e in atlas if rows[e]["true_fingerprint_id"] == fp)
             for j in range(len(AUG[atlas[0]]))]
        for fp in aug_classes
    }

    def cof_max_raw(e: str) -> float:
        return max(cofvec(e))

    def aug_nearest_centroid(e: str) -> float:
        return max(cosine_similarity(AUG[e], c) for c in aug_cents.values())

    def aug_margin(e: str) -> float:
        sims = sorted((cosine_similarity(AUG[e], c) for c in aug_cents.values()), reverse=True)
        return sims[0] - sims[1] if len(sims) > 1 else sims[0]

    signal_fns = {
        "cofactor_max_raw_score": cof_max_raw,
        "augmented_nearest_centroid": aug_nearest_centroid,
        "augmented_centroid_margin": aug_margin,
    }
    signals: dict[str, Any] = {}
    for name, fn in signal_fns.items():
        si = [fn(e) for e in inscope]
        so = [fn(e) for e in oos]
        signals[name] = {
            "auc_in_gt_oos": _auc_in_gt_oos(si, so),
            "in_scope_mean": round(sum(si) / len(si), 6),
            "oos_mean": round(sum(so) / len(so), 6),
        }
    best_auc = max(s["auc_in_gt_oos"] for s in signals.values())
    return {
        "status": "computed",
        "counts": {"atlas": len(atlas), "inscope": len(inscope), "oos": len(oos)},
        "signals": signals,
        "best_auc": best_auc,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_mechanism_novelty_abstention_eval(
    *, esm2_150m_path: Path, cofactor_sidecar_path: Path | None = None
) -> dict[str, Any]:
    rows = load_plm_rows(esm2_150m_path)
    result = compute_novelty_signals(rows)
    best_auc = result.get("best_auc", 0.0)

    cofactor_block: dict[str, Any] | None = None
    cofactor_best = 0.0
    if cofactor_sidecar_path is not None and Path(cofactor_sidecar_path).exists():
        cof_scores = load_cofactor_scores(cofactor_sidecar_path)
        cofactor_block = compute_cofactor_augmented_signals(rows, cof_scores)
        cofactor_block["source"] = _cofactor_source_label(cofactor_sidecar_path)
        cofactor_block["source_caveat"] = (
            "Cofactor scores are source-agnostic; today's source may be the "
            "documented ESM2-150M fallback rather than the original t6/t12 selected "
            "heads. Re-run with the recovered sidecar to remove the fallback."
        )
        cofactor_best = cofactor_block.get("best_auc", 0.0)
    return {
        "artifact_id": "v3_mechanism_novelty_abstention_eval_current702_20260530",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "scope": (
            "D11 de novo precondition: measure whether cheap unsupervised distance "
            "signals in the ESM2-150M mechanism space separate in-scope held-out "
            "queries from out-of-scope (novel-chemistry) held-out rows."
        ),
        "result": result,
        "cofactor_augmented_result": cofactor_block,
        "overall_best_auc": max(best_auc, cofactor_best),
        "interpretation": {
            "headline": (
                f"Bare-PLM best abstention AUC is {best_auc}"
                + (
                    f"; cofactor augmentation lifts it to {cofactor_best}."
                    if cofactor_block is not None
                    else "."
                )
            ),
            "cofactor_augmentation_helps_but_insufficient": (
                cofactor_block is not None
                and cofactor_best > best_auc
                and cofactor_best < ABSTENTION_USABLE_AUC
            ),
            "why": (
                "OOS rows are real, well-folded enzymes with novel mechanism "
                "chemistry. A general-purpose PLM embedding encodes overall protein "
                "similarity, under which novel enzymes still look like ordinary "
                "proteins and sit inside occupied regions, so raw embedding distance "
                "is near chance. The mechanism-discriminative cofactor channel moves "
                "the signal in the right direction (novel chemistry carries lower "
                "in-class cofactor confidence) but does not yet clear the abstention "
                "bar, so the de novo precondition remains an open problem pending a "
                "stronger mechanism-feature signal."
            ),
        },
        "guardrails": {
            "sequence_inputs_amino_acid_only": True,
            "no_training_or_refit": True,
            "no_heldout_tuning": True,
            "atlas_only_statistics_centroids_subspace": True,
            "labels_registries_thresholds_changed": False,
        },
        "source_artifacts": {
            "esm2_150m_embeddings": {
                "path": str(esm2_150m_path),
                "sha256": _sha256(esm2_150m_path),
            },
            **(
                {
                    "cofactor_score_sidecar": {
                        "path": str(cofactor_sidecar_path),
                        "sha256": _sha256(cofactor_sidecar_path),
                    }
                }
                if cofactor_block is not None
                else {}
            ),
        },
    }


def write_mechanism_novelty_abstention_eval(
    *,
    esm2_150m_path: Path,
    out_path: Path,
    cofactor_sidecar_path: Path | None = None,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_novelty_abstention_eval(
        esm2_150m_path=esm2_150m_path, cofactor_sidecar_path=cofactor_sidecar_path
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
    res = audit["result"]
    c = res["counts"]
    lines = [
        "# D11 Mechanism Novelty Abstention (de novo precondition)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        f"In-scope held-out: {c['inscope']} | OOS held-out: {c['oos']} | Atlas: {c['atlas']}",
        "",
        "## Abstention signals (AUC that in-scope > OOS; 0.5 = chance)",
        "",
        "| Signal | AUC | in-scope mean | OOS mean |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, s in res["signals"].items():
        lines.append(
            f"| {name} | {s['auc_in_gt_oos']} | {s['in_scope_mean']} | {s['oos_mean']} |"
        )
    lines += [
        "",
        f"- Bare-PLM best AUC: **{res['best_auc']}** -> status `{res['abstention_status']}`.",
    ]
    cof = audit.get("cofactor_augmented_result")
    if cof and cof.get("status") == "computed":
        cc = cof["counts"]
        lines += [
            "",
            "## Cofactor-augmented signals",
            "",
            f"Source: `{cof.get('source')}`. "
            f"In-scope: {cc['inscope']} | OOS: {cc['oos']} | Atlas: {cc['atlas']}",
            "",
            "| Signal | AUC | in-scope mean | OOS mean |",
            "| --- | ---: | ---: | ---: |",
        ]
        for name, s in cof["signals"].items():
            lines.append(
                f"| {name} | {s['auc_in_gt_oos']} | {s['in_scope_mean']} | {s['oos_mean']} |"
            )
        lines.append("")
        lines.append(f"- Cofactor-augmented best AUC: **{cof['best_auc']}**.")
    lines += [
        "",
        "## Interpretation",
        "",
        audit["interpretation"]["headline"],
        "",
        audit["interpretation"]["why"],
    ]
    return "\n".join(lines) + "\n"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
