"""Fold-NN nearest-neighbour mechanism recovery readout (reusable harness).

Given a set of positive rows (each with a true mechanism fingerprint) and their
``foldseek`` alignment scores against the M-CSA train in-scope atlas, this reports
how often the fold-NN nearest neighbour in the atlas carries the true fingerprint
(recovery), and a recovery/abstention threshold curve. It is the recovery
counterpart of the off-M-CSA abstention readout.

The harness is surface-agnostic: pointed at the M-CSA calibration in-scope rows
(the existing recompute inputs) it yields the in-distribution recovery baseline;
pointed at a trusted non-M-CSA positive set with structures (once one exists) and
its foldseek TSV, the same code yields the off-M-CSA recovery readout. It trains
nothing, selects no threshold on heldout, and changes no registry.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ATLAS_MANIFEST_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_FOLDSEEK_TSV_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_current702_20260628_results/"
    "calibration_vs_current57_train_atlas.tsv"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_fold_nn_mechanism_recovery_mcsa_baseline_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/fold_nn_mechanism_recovery_mcsa_baseline_current702_20260628.md"
)

DEFAULT_FOLD_THRESHOLD_GRID: tuple[float, ...] = (
    0.0,
    0.50,
    0.566,
    0.60,
    0.65,
    0.70,
    0.74,
)

_ACCESSION_RE = re.compile(r"afdb_(.+?)(?:_v6)?$")


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


def _accession(name: str) -> str:
    match = _ACCESSION_RE.match(name)
    return match.group(1) if match else name


def best_nn_by_query(tsv_text: str) -> dict[str, dict[str, Any]]:
    """Best alntmscore target per query accession."""

    best: dict[str, dict[str, Any]] = {}
    for line in tsv_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        query = _accession(parts[0])
        target = _accession(parts[1])
        aln = float(parts[4])
        current = best.get(query)
        if current is None or aln > current["alntmscore"]:
            best[query] = {"target_accession": target, "alntmscore": aln}
    return best


def atlas_fingerprints_from_manifest(manifest: dict[str, Any]) -> dict[str, str | None]:
    mapping: dict[str, str | None] = {}
    for row in manifest.get("rows", {}).get("train_in_scope_targets", []) or []:
        accession = row.get("accession")
        if accession:
            mapping[str(accession)] = row.get("true_fingerprint_id")
    return mapping


def positives_from_manifest_group(
    manifest: dict[str, Any], group: str, row_class: str
) -> list[dict[str, Any]]:
    rows = manifest.get("rows", {}).get(group, []) or []
    positives = []
    for row in rows:
        if row.get("row_class") != row_class:
            continue
        if not row.get("accession") or not row.get("true_fingerprint_id"):
            continue
        positives.append(
            {
                "entry_id": row.get("entry_id"),
                "accession": row.get("accession"),
                "true_fingerprint_id": row.get("true_fingerprint_id"),
            }
        )
    return positives


def build_fold_nn_mechanism_recovery_readout(
    *,
    positives: list[dict[str, Any]],
    best_nn: dict[str, dict[str, Any]],
    atlas_fingerprints: dict[str, str | None],
    surface_label: str,
    fold_threshold_grid: tuple[float, ...] = DEFAULT_FOLD_THRESHOLD_GRID,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for positive in positives:
        accession = str(positive.get("accession"))
        true_fp = positive.get("true_fingerprint_id")
        hit = best_nn.get(accession)
        if hit is None:
            rows.append(
                {
                    "entry_id": positive.get("entry_id"),
                    "accession": accession,
                    "true_fingerprint_id": true_fp,
                    "fold_nn_scored": False,
                    "fold_nn_alntmscore": None,
                    "fold_nn_target_accession": None,
                    "fold_nn_target_fingerprint_id": None,
                    "recovered": None,
                }
            )
            continue
        target = hit["target_accession"]
        target_fp = atlas_fingerprints.get(target)
        rows.append(
            {
                "entry_id": positive.get("entry_id"),
                "accession": accession,
                "true_fingerprint_id": true_fp,
                "fold_nn_scored": True,
                "fold_nn_alntmscore": round(hit["alntmscore"], 4),
                "fold_nn_target_accession": target,
                "fold_nn_target_fingerprint_id": target_fp,
                "recovered": bool(true_fp and target_fp == true_fp),
            }
        )

    scored = [r for r in rows if r["fold_nn_scored"]]
    recovered = [r for r in scored if r["recovered"]]
    fold_scores = [r["fold_nn_alntmscore"] for r in scored]

    curve = []
    for threshold in fold_threshold_grid:
        retained = [r for r in scored if r["fold_nn_alntmscore"] >= threshold]
        retained_recovered = [r for r in retained if r["recovered"]]
        curve.append(
            {
                "fold_threshold": round(threshold, 4),
                "retained": len(retained),
                "abstained": len(scored) - len(retained),
                "retained_recovered": len(retained_recovered),
                "precision_on_retained": (
                    round(len(retained_recovered) / len(retained), 4)
                    if retained
                    else None
                ),
                "recovery_of_all_positives": (
                    round(len(retained_recovered) / len(scored), 4) if scored else None
                ),
            }
        )

    return {
        "artifact_id": "v3_fold_nn_mechanism_recovery_readout_current702_20260628",
        "schema_version": "fold_nn_mechanism_recovery_readout.v1",
        "created_utc": _utc_now_iso(),
        "status": "fold_nn_mechanism_recovery_readout_complete",
        "result_class": (
            "heldout_excluded_fold_nn_retrieval_recovery_readout_no_training_no_threshold_change"
        ),
        "surface_label": surface_label,
        "guardrails": {
            "heldout_rows_scored": False,
            "supervised_model_trained": False,
            "threshold_selected_on_heldout": False,
            "labels_used_as_evaluation_targets_only": True,
            "production_threshold_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
        },
        "coverage": {
            "positives_total": len(positives),
            "positives_with_fold_hit": len(scored),
            "coverage_fraction": (
                round(len(scored) / len(positives), 4) if positives else None
            ),
        },
        "recovery": {
            "fold_nn_recovered": len(recovered),
            "fold_nn_scored": len(scored),
            "recovery_rate_no_abstention": (
                round(len(recovered) / len(scored), 4) if scored else None
            ),
            "fold_nn_score_median": (
                round(statistics.median(fold_scores), 4) if fold_scores else None
            ),
        },
        "recovery_abstention_curve": curve,
        "rows": rows,
        "interpretation": {
            "headline": (
                f"On surface '{surface_label}', fold-NN nearest-neighbour retrieval "
                f"against the M-CSA train atlas recovers the true mechanism fingerprint "
                f"for {len(recovered)}/{len(scored)} scored positives "
                f"(no abstention)."
            ),
            "note": (
                "Raising the fold gate trades recovered coverage for precision on the "
                "retained set; compare against the off-M-CSA abstention frontier when a "
                "non-M-CSA positive surface becomes available."
            ),
        },
    }


def _report(readout: dict[str, Any]) -> str:
    cov = readout["coverage"]
    rec = readout["recovery"]
    lines = [
        "# Fold-NN Mechanism Recovery Readout",
        "",
        f"Run: {readout['created_utc']}",
        f"Surface: `{readout['surface_label']}`",
        f"Status: `{readout['status']}`",
        "",
        "## Coverage",
        "",
        f"- Positives with a fold hit: {cov['positives_with_fold_hit']}/"
        f"{cov['positives_total']} ({cov['coverage_fraction']}).",
        "",
        "## Recovery (no abstention)",
        "",
        f"- Fold-NN recovered true fingerprint: {rec['fold_nn_recovered']}/"
        f"{rec['fold_nn_scored']} ({rec['recovery_rate_no_abstention']}).",
        f"- Fold-NN score median: {rec['fold_nn_score_median']}.",
        "",
        "## Recovery / Abstention Curve",
        "",
    ]
    for point in readout["recovery_abstention_curve"]:
        lines.append(
            f"- fold >= {point['fold_threshold']}: retained {point['retained']} "
            f"(abstained {point['abstained']}); recovered {point['retained_recovered']}; "
            f"precision-on-retained {point['precision_on_retained']}; "
            f"recovery-of-all {point['recovery_of_all_positives']}."
        )
    lines += [
        "",
        "## Notes",
        "",
        f"- {readout['interpretation']['note']}",
        "",
        "## Guardrails",
        "",
        "- Labels are evaluation targets only, never model features.",
        "- No heldout row scored; no model trained; no threshold selected on heldout; "
        "no registry/ontology/label/threshold/fingerprint change.",
    ]
    return "\n".join(lines) + "\n"


def write_fold_nn_mechanism_recovery_readout(
    *,
    atlas_manifest_path: Path,
    foldseek_tsv_path: Path,
    positives_path: Path | None = None,
    positives_group: str = "calibration_queries",
    positives_row_class: str = "inscope",
    surface_label: str = "mcsa_calibration_inscope_baseline",
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    manifest = _load_json(atlas_manifest_path)
    atlas_fingerprints = atlas_fingerprints_from_manifest(manifest)
    if positives_path is not None:
        positives = _load_json(positives_path).get("rows", [])
    else:
        positives = positives_from_manifest_group(
            manifest, positives_group, positives_row_class
        )
    best_nn = best_nn_by_query(
        Path(foldseek_tsv_path).read_text(encoding="utf-8")
    )
    readout = build_fold_nn_mechanism_recovery_readout(
        positives=positives,
        best_nn=best_nn,
        atlas_fingerprints=atlas_fingerprints,
        surface_label=surface_label,
    )
    readout["source_artifacts"] = {
        "atlas_manifest": {
            "path": str(atlas_manifest_path),
            "artifact_id": manifest.get("artifact_id"),
            "sha256": _sha256(Path(atlas_manifest_path)),
        },
        "foldseek_tsv": {
            "path": str(foldseek_tsv_path),
            "sha256": _sha256(Path(foldseek_tsv_path)),
        },
        "positives_path": str(positives_path) if positives_path else None,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(readout, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(readout), encoding="utf-8")
    return readout
