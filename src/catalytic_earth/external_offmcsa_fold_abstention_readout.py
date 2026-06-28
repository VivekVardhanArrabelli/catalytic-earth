"""Off-M-CSA generalization test for the fold-NN abstention signal.

The entire current702 mechanism benchmark (train/calibration/heldout) is M-CSA
(699/702), so an M-CSA heldout read only certifies sequence-distant M-CSA
generalization, not deployment-distribution behavior. The cofactor channel was
already shown to carry no abstention signal off M-CSA (the gold eval). This
readout tests whether the row-aligned fold-NN TM abstention separation (M-CSA
in-scope median ~0.74 vs OOS ~0.57) survives on a genuinely non-M-CSA negative
surface: external hard negatives fold-scored against the same M-CSA train
in-scope atlas.

If the external negatives' fold-NN distribution tracks the M-CSA OOS
distribution (low) rather than the in-scope distribution (high), the fold
channel provides a real off-M-CSA abstention signal. It is heldout-excluded and
trains nothing; the external negatives are non-M-CSA rows scored only against the
M-CSA train atlas.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_EXTERNAL_TSV_PATH = (
    "artifacts/v3_external_offmcsa_fold_abstention_current702_20260628_results/"
    "external_negatives_vs_mcsa_train_atlas.tsv"
)
DEFAULT_MCSA_FOLD_READOUT_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_external_offmcsa_fold_abstention_readout_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/external_offmcsa_fold_abstention_readout_current702_20260628.md"
)

# Fold-NN gate grid for the abstention/recovery frontier.
FOLD_THRESHOLD_GRID: tuple[float, ...] = (
    0.50,
    0.566,
    0.60,
    0.65,
    0.70,
    0.74,
)
# Tolerance for "external median tracks the M-CSA OOS median".
DEFAULT_OOS_TRACKING_TOLERANCE = 0.05

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


def best_fold_nn_by_query(tsv_text: str) -> dict[str, float]:
    """Best alntmscore per external query accession."""

    best: dict[str, float] = {}
    for line in tsv_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        query = _accession(parts[0])
        aln = float(parts[4])
        if query not in best or aln > best[query]:
            best[query] = aln
    return best


def _distribution(scores: list[float]) -> dict[str, Any]:
    if not scores:
        return {
            "n": 0,
            "median": None,
            "mean": None,
            "min": None,
            "max": None,
        }
    return {
        "n": len(scores),
        "median": round(statistics.median(scores), 4),
        "mean": round(statistics.mean(scores), 4),
        "min": round(min(scores), 4),
        "max": round(max(scores), 4),
    }


def _mcsa_fold_scores(
    mcsa_fold_readout: dict[str, Any], group: str
) -> list[float]:
    rows = mcsa_fold_readout.get("rows", {}).get(group, []) or []
    return [
        float(row["fold_nn_alntmscore"])
        for row in rows
        if row.get("fold_nn_scored") and row.get("fold_nn_alntmscore") is not None
    ]


def build_external_offmcsa_fold_abstention_readout(
    *,
    external_best_fold_nn: dict[str, float],
    mcsa_fold_readout: dict[str, Any],
    fold_threshold_grid: tuple[float, ...] = FOLD_THRESHOLD_GRID,
    oos_tracking_tolerance: float = DEFAULT_OOS_TRACKING_TOLERANCE,
) -> dict[str, Any]:
    external_scores = sorted(external_best_fold_nn.values())
    inscope_scores = _mcsa_fold_scores(mcsa_fold_readout, "calibration_inscope")
    oos_scores = _mcsa_fold_scores(mcsa_fold_readout, "calibration_oos")

    external_dist = _distribution(external_scores)
    inscope_dist = _distribution(inscope_scores)
    oos_dist = _distribution(oos_scores)

    external_median = external_dist["median"]
    inscope_median = inscope_dist["median"]
    oos_median = oos_dist["median"]

    tracks_oos = bool(
        external_median is not None
        and oos_median is not None
        and abs(external_median - oos_median) <= oos_tracking_tolerance
    )
    below_inscope = bool(
        external_median is not None
        and inscope_median is not None
        and external_median < inscope_median
    )
    abstention_generalizes = tracks_oos and below_inscope

    n_ext = len(external_scores) or 1
    n_in = len(inscope_scores) or 1
    n_oos = len(oos_scores) or 1
    frontier = []
    for threshold in fold_threshold_grid:
        ext_accept = sum(1 for s in external_scores if s >= threshold)
        in_keep = sum(1 for s in inscope_scores if s >= threshold)
        oos_accept = sum(1 for s in oos_scores if s >= threshold)
        frontier.append(
            {
                "fold_threshold": round(threshold, 4),
                "external_negatives_not_abstained": ext_accept,
                "external_negatives_total": len(external_scores),
                "external_false_accept_rate": round(ext_accept / n_ext, 4),
                "mcsa_inscope_retained": in_keep,
                "mcsa_inscope_total": len(inscope_scores),
                "mcsa_inscope_retention_rate": round(in_keep / n_in, 4),
                "mcsa_oos_not_abstained": oos_accept,
                "mcsa_oos_total": len(oos_scores),
                "mcsa_oos_false_accept_rate": round(oos_accept / n_oos, 4),
            }
        )

    status = (
        "fold_nn_abstention_signal_generalizes_off_mcsa"
        if abstention_generalizes
        else "fold_nn_abstention_signal_does_not_generalize_off_mcsa"
    )

    return {
        "artifact_id": (
            "v3_external_offmcsa_fold_abstention_readout_current702_20260628"
        ),
        "schema_version": "external_offmcsa_fold_abstention_readout.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "heldout_excluded_off_mcsa_generalization_probe_no_training_no_threshold_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "external_negatives_are_non_mcsa": True,
            "external_scored_against_mcsa_train_atlas_only": True,
            "supervised_model_trained": False,
            "threshold_selected_on_heldout": False,
            "production_threshold_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
        },
        "inputs": {
            "mcsa_fold_readout_artifact_id": mcsa_fold_readout.get("artifact_id"),
            "external_negative_query_count": len(external_scores),
        },
        "distributions": {
            "external_offmcsa_negatives": external_dist,
            "mcsa_calibration_inscope": inscope_dist,
            "mcsa_calibration_oos": oos_dist,
        },
        "generalization_test": {
            "external_median": external_median,
            "mcsa_oos_median": oos_median,
            "mcsa_inscope_median": inscope_median,
            "oos_tracking_tolerance": oos_tracking_tolerance,
            "external_tracks_mcsa_oos": tracks_oos,
            "external_below_mcsa_inscope": below_inscope,
            "abstention_signal_generalizes_off_mcsa": abstention_generalizes,
            "external_negatives_at_or_above_inscope_median": sum(
                1 for s in external_scores if inscope_median is not None and s >= inscope_median
            ),
        },
        "abstention_recovery_frontier": frontier,
        "interpretation": {
            "headline": (
                "The fold-NN abstention separation generalizes off M-CSA: external "
                "non-M-CSA negatives track the M-CSA OOS fold-NN distribution and sit "
                "well below the in-scope distribution, so a strict fold gate rejects "
                "most of them."
                if abstention_generalizes
                else "The fold-NN abstention separation does not clearly generalize off "
                "M-CSA: external non-M-CSA negatives do not track the M-CSA OOS "
                "distribution as expected."
            ),
            "caveats": (
                "This probes off-M-CSA OOS rejection only, not off-M-CSA in-scope "
                "recovery (which would need non-M-CSA positives with known mechanism "
                "and structure). The external set is a curated negative panel, not a "
                "random deployment sample, and a strict abstention threshold also lowers "
                "in-scope recovery (see the frontier). No threshold is selected here."
            ),
        },
    }


def _report(readout: dict[str, Any]) -> str:
    dist = readout["distributions"]
    test = readout["generalization_test"]
    lines = [
        "# Off-M-CSA Fold-NN Abstention Generalization Readout",
        "",
        f"Run: {readout['created_utc']}",
        f"Status: `{readout['status']}`",
        "",
        "## Fold-NN Distributions (best alntmscore to the M-CSA train atlas)",
        "",
        f"- External off-M-CSA negatives: median "
        f"{dist['external_offmcsa_negatives']['median']} "
        f"(mean {dist['external_offmcsa_negatives']['mean']}, n "
        f"{dist['external_offmcsa_negatives']['n']}).",
        f"- M-CSA calibration in-scope: median "
        f"{dist['mcsa_calibration_inscope']['median']} "
        f"(n {dist['mcsa_calibration_inscope']['n']}).",
        f"- M-CSA calibration OOS: median {dist['mcsa_calibration_oos']['median']} "
        f"(n {dist['mcsa_calibration_oos']['n']}).",
        "",
        "## Generalization Test",
        "",
        f"- External median {test['external_median']} vs M-CSA OOS median "
        f"{test['mcsa_oos_median']} (tracks OOS within "
        f"{test['oos_tracking_tolerance']}: {test['external_tracks_mcsa_oos']}).",
        f"- External median below M-CSA in-scope median "
        f"{test['mcsa_inscope_median']}: {test['external_below_mcsa_inscope']}.",
        f"- External negatives at/above the in-scope median: "
        f"{test['external_negatives_at_or_above_inscope_median']}.",
        f"- Abstention signal generalizes off M-CSA: "
        f"{test['abstention_signal_generalizes_off_mcsa']}.",
        "",
        "## Abstention / Recovery Frontier",
        "",
    ]
    for point in readout["abstention_recovery_frontier"]:
        lines.append(
            f"- fold >= {point['fold_threshold']}: external false-accept "
            f"{point['external_negatives_not_abstained']}/"
            f"{point['external_negatives_total']} "
            f"({point['external_false_accept_rate']}); M-CSA in-scope retained "
            f"{point['mcsa_inscope_retained']}/{point['mcsa_inscope_total']} "
            f"({point['mcsa_inscope_retention_rate']}); M-CSA OOS false-accept "
            f"{point['mcsa_oos_not_abstained']}/{point['mcsa_oos_total']}."
        )
    lines += [
        "",
        "## Caveats",
        "",
        f"- {readout['interpretation']['caveats']}",
        "",
        "## Guardrails",
        "",
        "- External negatives are non-M-CSA, scored only against the M-CSA train atlas.",
        "- No heldout row was scored or read; no model was trained; no threshold was "
        "selected on heldout.",
        "- No production threshold, model weight, registry, ontology, label, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_external_offmcsa_fold_abstention_readout(
    *,
    external_tsv_path: Path,
    mcsa_fold_readout_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    external_best = best_fold_nn_by_query(
        Path(external_tsv_path).read_text(encoding="utf-8")
    )
    mcsa_fold_readout = _load_json(mcsa_fold_readout_path)
    readout = build_external_offmcsa_fold_abstention_readout(
        external_best_fold_nn=external_best,
        mcsa_fold_readout=mcsa_fold_readout,
    )
    readout["source_artifacts"] = {
        "external_negatives_vs_mcsa_train_atlas_tsv": {
            "path": str(external_tsv_path),
            "sha256": _sha256(Path(external_tsv_path)),
        },
        "mcsa_fold_recompute_readout": {
            "path": str(mcsa_fold_readout_path),
            "artifact_id": mcsa_fold_readout.get("artifact_id"),
            "sha256": _sha256(Path(mcsa_fold_readout_path)),
        },
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
