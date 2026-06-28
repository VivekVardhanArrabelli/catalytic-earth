"""Row-aligned Fold/TM readout for the recomputed current-57 cofactor surface.

The cached Fold/TM contracts were not row-aligned with the expanded current-57
cofactor train/cal surface (calibration in-scope overlap 4/35, OOS 0/26), so
the cofactor/fold alignment audit fail-closed. This module reads the freshly
recomputed ``foldseek easy-search`` output (calibration cofactor queries vs the
current-57 train in-scope fold atlas) staged by
``v3_current57_fold_tm_recompute_input_manifest_current702_20260628`` and emits a
heldout-excluded, calibration-vs-train Fold/TM readout that is row-aligned by
construction.

It does not train a model, does not select any threshold on heldout rows, and
does not read or score heldout rows. It is a diagnostic readout, not a
deployment contract: the separate current-57 cofactor precision contract still
governs whether any cached/fused atlas-engine readout may proceed.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_FOLDSEEK_TSV_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_current702_20260628_results/"
    "calibration_vs_current57_train_atlas.tsv"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/current57_fold_tm_recompute_readout_current702_20260628.md"
)

# Mirror the alignment audit's 0.9 row-overlap requirement.
DEFAULT_MIN_COVERAGE_FRACTION = 0.9
# Minimum in-scope vs OOS median fold-NN TM gap to call an abstention signal.
DEFAULT_ABSTENTION_MARGIN = 0.05

# Cached-surface overlap the alignment audit reported, recorded for contrast.
PRIOR_CACHED_INSCOPE_OVERLAP = "4/35"
PRIOR_CACHED_OOS_OVERLAP = "0/26"

_ACCESSION_RE = re.compile(r"afdb_(.+)_v6")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_summary(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "artifact_id": data.get("artifact_id"),
        "status": data.get("status"),
        "schema_version": data.get("schema_version"),
        "sha256": _sha256(path),
    }


def _accession(name: str) -> str:
    match = _ACCESSION_RE.match(name)
    return match.group(1) if match else name


def parse_foldseek_rows(text: str) -> list[dict[str, Any]]:
    """Parse a ``query,target,qtmscore,ttmscore,alntmscore,prob,bits`` TSV."""

    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        rows.append(
            {
                "query_accession": _accession(parts[0]),
                "target_accession": _accession(parts[1]),
                "qtmscore": float(parts[2]),
                "ttmscore": float(parts[3]),
                "alntmscore": float(parts[4]),
                "prob": float(parts[5]) if len(parts) > 5 else None,
                "bits": float(parts[6]) if len(parts) > 6 else None,
            }
        )
    return rows


def _best_hit_by_query(
    foldseek_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    counts: dict[str, int] = {}
    for row in foldseek_rows:
        query = row["query_accession"]
        counts[query] = counts.get(query, 0) + 1
        current = best.get(query)
        if current is None or row["alntmscore"] > current["alntmscore"]:
            best[query] = row
    for query, hit in best.items():
        hit["targets_scored"] = counts.get(query, 0)
    return best


def _target_fingerprint_by_accession(manifest: dict[str, Any]) -> dict[str, str | None]:
    mapping: dict[str, str | None] = {}
    for row in manifest.get("rows", {}).get("train_in_scope_targets", []) or []:
        accession = row.get("accession")
        if accession:
            mapping[str(accession)] = row.get("true_fingerprint_id")
    return mapping


def _target_entry_by_accession(manifest: dict[str, Any]) -> dict[str, str | None]:
    mapping: dict[str, str | None] = {}
    for row in manifest.get("rows", {}).get("train_in_scope_targets", []) or []:
        accession = row.get("accession")
        if accession:
            mapping[str(accession)] = row.get("entry_id")
    return mapping


def _readout_row(
    *,
    manifest_row: dict[str, Any],
    best_hit: dict[str, Any] | None,
    target_fingerprints: dict[str, str | None],
    target_entries: dict[str, str | None],
) -> dict[str, Any]:
    accession = manifest_row.get("accession")
    if best_hit is None:
        return {
            "entry_id": manifest_row.get("entry_id"),
            "accession": accession,
            "role": manifest_row.get("role"),
            "true_fingerprint_id": manifest_row.get("true_fingerprint_id"),
            "current57_fused_top1_fingerprint_id": manifest_row.get(
                "current57_fused_top1_fingerprint_id"
            ),
            "current57_fused_top1_score": manifest_row.get(
                "current57_fused_top1_score"
            ),
            "fold_nn_scored": False,
            "fold_nn_alntmscore": None,
            "fold_nn_qtmscore": None,
            "fold_nn_target_accession": None,
            "fold_nn_target_entry_id": None,
            "fold_nn_target_true_fingerprint_id": None,
            "fold_nn_fingerprint_match": None,
            "fold_nn_targets_scored": 0,
        }
    target = best_hit["target_accession"]
    target_fp = target_fingerprints.get(target)
    true_fp = manifest_row.get("true_fingerprint_id")
    match: bool | None
    if true_fp is None:
        match = None
    else:
        match = target_fp == true_fp
    return {
        "entry_id": manifest_row.get("entry_id"),
        "accession": accession,
        "role": manifest_row.get("role"),
        "true_fingerprint_id": true_fp,
        "current57_fused_top1_fingerprint_id": manifest_row.get(
            "current57_fused_top1_fingerprint_id"
        ),
        "current57_fused_top1_score": manifest_row.get("current57_fused_top1_score"),
        "fold_nn_scored": True,
        "fold_nn_alntmscore": round(best_hit["alntmscore"], 4),
        "fold_nn_qtmscore": round(best_hit["qtmscore"], 4),
        "fold_nn_target_accession": target,
        "fold_nn_target_entry_id": target_entries.get(target),
        "fold_nn_target_true_fingerprint_id": target_fp,
        "fold_nn_fingerprint_match": match,
        "fold_nn_targets_scored": best_hit.get("targets_scored", 0),
    }


def _distribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [
        row["fold_nn_alntmscore"]
        for row in rows
        if row.get("fold_nn_scored") and row.get("fold_nn_alntmscore") is not None
    ]
    if not scores:
        return {
            "n": 0,
            "alntmscore_median": None,
            "alntmscore_mean": None,
            "alntmscore_min": None,
            "alntmscore_max": None,
        }
    return {
        "n": len(scores),
        "alntmscore_median": round(statistics.median(scores), 4),
        "alntmscore_mean": round(statistics.mean(scores), 4),
        "alntmscore_min": round(min(scores), 4),
        "alntmscore_max": round(max(scores), 4),
    }


def _coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    scored = [row for row in rows if row.get("fold_nn_scored")]
    missing = [
        row.get("entry_id") for row in rows if not row.get("fold_nn_scored")
    ]
    return {
        "rows": total,
        "rows_with_fold_score": len(scored),
        "coverage_fraction": round(len(scored) / total, 4) if total else None,
        "missing_entry_ids": missing,
    }


def build_current57_fold_tm_recompute_readout(
    *,
    manifest: dict[str, Any],
    foldseek_rows: list[dict[str, Any]],
    foldseek_command: str | None = None,
    foldseek_version: str | None = None,
    min_coverage_fraction: float = DEFAULT_MIN_COVERAGE_FRACTION,
    abstention_margin: float = DEFAULT_ABSTENTION_MARGIN,
) -> dict[str, Any]:
    best_hits = _best_hit_by_query(foldseek_rows)
    target_fingerprints = _target_fingerprint_by_accession(manifest)
    target_entries = _target_entry_by_accession(manifest)

    manifest_queries = manifest.get("rows", {}).get("calibration_queries", []) or []
    inscope_rows: list[dict[str, Any]] = []
    oos_rows: list[dict[str, Any]] = []
    for manifest_row in manifest_queries:
        accession = manifest_row.get("accession")
        best_hit = best_hits.get(str(accession)) if accession else None
        readout_row = _readout_row(
            manifest_row=manifest_row,
            best_hit=best_hit,
            target_fingerprints=target_fingerprints,
            target_entries=target_entries,
        )
        if manifest_row.get("row_class") == "inscope":
            inscope_rows.append(readout_row)
        else:
            oos_rows.append(readout_row)

    inscope_coverage = _coverage(inscope_rows)
    oos_coverage = _coverage(oos_rows)
    inscope_distribution = _distribution(inscope_rows)
    oos_distribution = _distribution(oos_rows)

    inscope_median = inscope_distribution.get("alntmscore_median")
    oos_median = oos_distribution.get("alntmscore_median")
    median_gap = (
        round(inscope_median - oos_median, 4)
        if inscope_median is not None and oos_median is not None
        else None
    )
    abstention_signal = bool(median_gap is not None and median_gap >= abstention_margin)

    matched = [
        row
        for row in inscope_rows
        if row.get("fold_nn_scored") and row.get("fold_nn_fingerprint_match")
    ]
    scored_inscope = [row for row in inscope_rows if row.get("fold_nn_scored")]

    inscope_fraction = inscope_coverage.get("coverage_fraction") or 0.0
    oos_fraction = oos_coverage.get("coverage_fraction") or 0.0
    row_aligned = (
        inscope_fraction >= min_coverage_fraction
        and oos_fraction >= min_coverage_fraction
    )
    status = (
        "current57_fold_tm_recompute_readout_row_aligned"
        if row_aligned
        else "blocked_current57_fold_tm_recompute_readout_incomplete_coverage"
    )

    return {
        "artifact_id": "v3_current57_fold_tm_recompute_readout_current702_20260628",
        "schema_version": "current57_fold_tm_recompute_readout.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_recomputed_fold_tm_readout_calibration_vs_train_no_fusion"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "new_foldseek_or_tm_scores_computed": True,
            "scores_are_calibration_vs_train_only": True,
            "threshold_selected_on_heldout": False,
            "supervised_model_trained": False,
            "production_threshold_changed": False,
            "model_weights_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
        },
        "foldseek_provenance": {
            "command": foldseek_command,
            "version": foldseek_version,
            "format_output": "query,target,qtmscore,ttmscore,alntmscore,prob,bits",
            "alignment_rows": len(foldseek_rows),
            "queries_with_at_least_one_hit": len(best_hits),
        },
        "coverage": {
            "min_coverage_fraction": min_coverage_fraction,
            "calibration_inscope": inscope_coverage,
            "calibration_oos": oos_coverage,
        },
        "alignment_resolution": {
            "prior_cached_inscope_overlap": PRIOR_CACHED_INSCOPE_OVERLAP,
            "prior_cached_oos_overlap": PRIOR_CACHED_OOS_OVERLAP,
            "recomputed_inscope_overlap": (
                f"{inscope_coverage['rows_with_fold_score']}/"
                f"{inscope_coverage['rows']}"
            ),
            "recomputed_oos_overlap": (
                f"{oos_coverage['rows_with_fold_score']}/{oos_coverage['rows']}"
            ),
            "resolves_alignment_blocker": row_aligned,
        },
        "fold_nn_distribution": {
            "metric": "best_alntmscore_to_train_in_scope_neighbor",
            "inscope": inscope_distribution,
            "oos": oos_distribution,
            "separation": {
                "inscope_minus_oos_median": median_gap,
                "abstention_margin": abstention_margin,
                "abstention_signal_present": abstention_signal,
                "note": (
                    "Calibration-level diagnostic separation only; not a heldout "
                    "deployment claim and no threshold is selected here."
                ),
            },
        },
        "fold_nn_fingerprint_consistency": {
            "inscope_rows": len(inscope_rows),
            "inscope_rows_with_fold_score": len(scored_inscope),
            "inscope_fold_nn_true_fingerprint_match": len(matched),
            "match_fraction": (
                round(len(matched) / len(scored_inscope), 4)
                if scored_inscope
                else None
            ),
        },
        "rows": {
            "calibration_inscope": inscope_rows,
            "calibration_oos": oos_rows,
        },
        "interpretation": {
            "headline": (
                "Recomputed Fold/TM scores are row-aligned with the current-57 "
                "calibration cofactor surface and show in-scope fold-NN TM above OOS."
                if row_aligned and abstention_signal
                else "Recomputed Fold/TM readout produced; review coverage and "
                "separation before any fusion preregistration."
            ),
            "deployment_decision": (
                "Row alignment is resolved, so the cofactor/fold alignment blocker no "
                "longer applies. This readout does not authorize a fused atlas-engine "
                "readout on its own: the current-57 cofactor precision contract still "
                "governs deployment, and any fold-augmented fusion must be "
                "preregistered with a heldout-final selection rule."
            ),
        },
    }


def _report(readout: dict[str, Any]) -> str:
    coverage = readout["coverage"]
    distribution = readout["fold_nn_distribution"]
    separation = distribution["separation"]
    consistency = readout["fold_nn_fingerprint_consistency"]
    resolution = readout["alignment_resolution"]

    def fmt_cov(item: dict[str, Any]) -> str:
        return (
            f"{item.get('rows_with_fold_score')}/{item.get('rows')} "
            f"({item.get('coverage_fraction')})"
        )

    lines = [
        "# Current-57 Fold/TM Recompute Readout",
        "",
        f"Run: {readout['created_utc']}",
        f"Status: `{readout['status']}`",
        "",
        "## Row Alignment",
        "",
        f"- Cached overlap (prior, alignment audit): in-scope "
        f"{resolution['prior_cached_inscope_overlap']}, OOS "
        f"{resolution['prior_cached_oos_overlap']}.",
        f"- Recomputed overlap: in-scope {resolution['recomputed_inscope_overlap']}, "
        f"OOS {resolution['recomputed_oos_overlap']}.",
        f"- Resolves alignment blocker: {resolution['resolves_alignment_blocker']}.",
        "",
        "## Coverage",
        "",
        f"- Calibration in-scope: {fmt_cov(coverage['calibration_inscope'])}.",
        f"- Calibration OOS: {fmt_cov(coverage['calibration_oos'])}.",
        "",
        "## Fold-NN TM Separation (calibration-only diagnostic)",
        "",
        f"- In-scope best-alntmscore median: "
        f"{distribution['inscope']['alntmscore_median']} "
        f"(mean {distribution['inscope']['alntmscore_mean']}, n "
        f"{distribution['inscope']['n']}).",
        f"- OOS best-alntmscore median: {distribution['oos']['alntmscore_median']} "
        f"(mean {distribution['oos']['alntmscore_mean']}, n "
        f"{distribution['oos']['n']}).",
        f"- In-scope minus OOS median gap: "
        f"{separation['inscope_minus_oos_median']} "
        f"(abstention signal present: {separation['abstention_signal_present']}).",
        "",
        "## Fold-NN Fingerprint Consistency",
        "",
        f"- In-scope fold-NN true-fingerprint match: "
        f"{consistency['inscope_fold_nn_true_fingerprint_match']}/"
        f"{consistency['inscope_rows_with_fold_score']} "
        f"({consistency['match_fraction']}).",
        "",
        "## Decision",
        "",
        f"- {readout['interpretation']['deployment_decision']}",
        "",
        "## Guardrails",
        "",
        "- Scores are calibration-vs-train only; no heldout rows were scored or read.",
        "- No threshold was selected on heldout rows; no supervised model was trained.",
        "- No production threshold, model weight, registry, ontology, label, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_current57_fold_tm_recompute_readout(
    *,
    manifest_path: Path,
    foldseek_tsv_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    foldseek_command: str | None = None,
    foldseek_version: str | None = None,
    min_coverage_fraction: float = DEFAULT_MIN_COVERAGE_FRACTION,
    abstention_margin: float = DEFAULT_ABSTENTION_MARGIN,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    foldseek_rows = parse_foldseek_rows(
        Path(foldseek_tsv_path).read_text(encoding="utf-8")
    )
    if foldseek_command is None:
        foldseek_command = manifest.get("foldseek_command")
    readout = build_current57_fold_tm_recompute_readout(
        manifest=manifest,
        foldseek_rows=foldseek_rows,
        foldseek_command=foldseek_command,
        foldseek_version=foldseek_version,
        min_coverage_fraction=min_coverage_fraction,
        abstention_margin=abstention_margin,
    )
    readout["source_artifacts"] = {
        "recompute_input_manifest": _artifact_summary(manifest_path, manifest),
        "foldseek_results_tsv": {
            "path": str(foldseek_tsv_path),
            "sha256": _sha256(Path(foldseek_tsv_path)),
        },
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(readout), encoding="utf-8")
    return readout
