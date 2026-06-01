"""Bounded D11/northstar next-lever artifacts.

These writers are intentionally conservative: they read frozen/current702-safe
sidecars, produce reproducible JSON plus reports, and do not edit labels,
registries, ontologies, thresholds, imports, splits, or model weights.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import shlex
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .mechanism_abstention_gate_eval import load_geometry_role_scores
from .mechanism_novelty_abstention_eval import (
    COFACTOR_CLASSES,
    COFACTOR_SIGNATURE_THRESHOLD,
    load_cofactor_scores,
    load_plm_rows,
)
from .geometry_retrieval import run_geometry_retrieval
from .predicted_geometry_robustness import (
    _enriched_predicted_retrieval_results,
    _target_manifest_row_selection,
    build_alphafold_predicted_geometry_features,
)

SCHEMA_VERSION = "northstar_next_levers.v0"
DEFAULT_FOLDSEEK_BINARY = "/private/tmp/catalytic-foldseek-env/bin/foldseek"
PREDICTED_STRUCTURE_FOLD_CHANNEL_ID = (
    "v3_predicted_structure_fold_channel_current702_20260601"
)
FOLD_AUGMENTED_THRESHOLD_CONTRACT_ID = (
    "v3_fold_augmented_abstention_threshold_contract_current702_20260601"
)
FOLD_AUGMENTED_TRAIN_CAL_OOS_NEGATIVE_SURFACE_SCORES_ID = (
    "v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601"
)
FOLD_AUGMENTED_OOS_CALIBRATED_THRESHOLD_CONTRACT_ID = (
    "v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601"
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _auc_in_gt_oos(in_scope: list[float], oos: list[float]) -> float | None:
    if not in_scope or not oos:
        return None
    greater = sum(1 for a in in_scope for b in oos if a > b)
    ties = sum(1 for a in in_scope for b in oos if a == b)
    return round((greater + 0.5 * ties) / (len(in_scope) * len(oos)), 6)


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 6) if values else None


def _pearson(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 2:
        return None
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    da = [x - ma for x in a]
    db = [y - mb for y in b]
    denom = math.sqrt(sum(x * x for x in da) * sum(y * y for y in db))
    if not denom:
        return None
    return round(sum(x * y for x, y in zip(da, db)) / denom, 6)


def _best_threshold_at_retention(
    rows: list[dict[str, Any]],
    score_fn: Callable[[dict[str, Any]], float],
    *,
    min_retain: float,
) -> dict[str, Any] | None:
    inscope = [r for r in rows if r["is_inscope"]]
    oos = [r for r in rows if r["is_oos"]]
    conf = [r for r in rows if r["is_confounded_predicted_geometry_oos"]]
    if not inscope or not oos:
        return None
    candidates = sorted({round(score_fn(r), 6) for r in rows})
    best = None
    for threshold in candidates:
        retain = sum(1 for r in inscope if score_fn(r) >= threshold) / len(inscope)
        if retain < min_retain:
            continue
        oos_abst = sum(1 for r in oos if score_fn(r) < threshold) / len(oos)
        conf_abst = (
            sum(1 for r in conf if score_fn(r) < threshold) / len(conf)
            if conf else None
        )
        item = {
            "threshold": threshold,
            "inscope_retain_recall": round(retain, 4),
            "oos_abstain_recall": round(oos_abst, 4),
            "confounded_abstain_recall": round(conf_abst, 4) if conf_abst is not None else None,
        }
        key = (item["oos_abstain_recall"], item["confounded_abstain_recall"] or 0.0)
        if best is None or key > best[0]:
            best = (key, item)
    return best[1] if best else None


def _fold_scores(row: dict[str, Any]) -> dict[str, float]:
    top3 = row.get("top3_retained_train_neighbors") or []
    primary_top3 = [
        float(n.get("prob") or 0.0)
        for n in top3
        if n.get("fingerprint_id")
    ]
    nearest_primary_prob = (
        float(row.get("nearest_foldseek_prob") or 0.0)
        if row.get("nearest_train_fingerprint_id")
        else 0.0
    )
    high_conf_primary_count = int(row.get("retained_high_confidence_primary_fingerprint_hit_count") or 0)
    return {
        "nearest_primary_foldseek_prob": nearest_primary_prob,
        "top3_primary_foldseek_prob": max(primary_top3) if primary_top3 else 0.0,
        "nearest_primary_indicator": 1.0 if row.get("nearest_train_fingerprint_id") else 0.0,
        "high_conf_primary_hit_indicator": 1.0 if high_conf_primary_count > 0 else 0.0,
        "log1p_high_conf_primary_hit_count": round(math.log1p(high_conf_primary_count), 6),
    }


def build_fold_level_novelty_signal(
    *,
    foldseek_metadata_path: Path,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
    novelty_eval_path: Path,
) -> dict[str, Any]:
    plm = load_plm_rows(esm2_150m_path)
    cofactor = load_cofactor_scores(cofactor_sidecar_path)
    geometry = load_geometry_role_scores(predicted_geometry_audit_path)
    novelty = _read_json(novelty_eval_path)
    eight_confounded = set(
        novelty["cofactor_augmented_result"]["stratified_by_cofactor_signature"][
            "cofactor_confounded_oos_entry_ids"
        ]
    )
    predicted_confounded = {
        entry_id
        for entry_id, row in plm.items()
        if (
            row.get("split_assignment") == "heldout"
            and not row.get("true_fingerprint_id")
            and entry_id in cofactor
            and entry_id in geometry
            and max(cofactor[entry_id].get(c, 0.0) for c in COFACTOR_CLASSES)
            >= COFACTOR_SIGNATURE_THRESHOLD
        )
    }

    scored_rows: list[dict[str, Any]] = []
    for raw in _read_jsonl(foldseek_metadata_path):
        entry_id = raw.get("row_id") or raw.get("entry_id")
        if entry_id not in plm:
            continue
        plm_row = plm[entry_id]
        if plm_row.get("split_assignment") != "heldout":
            continue
        scores = _fold_scores(raw)
        scored_rows.append({
            "entry_id": entry_id,
            "split_assignment": plm_row.get("split_assignment"),
            "true_fingerprint_id": plm_row.get("true_fingerprint_id"),
            "is_inscope": bool(plm_row.get("true_fingerprint_id")),
            "is_oos": not bool(plm_row.get("true_fingerprint_id")),
            "is_cofactor_confounded_oos_any_geometry": entry_id in eight_confounded,
            "is_confounded_predicted_geometry_oos": entry_id in predicted_confounded,
            "nearest_train_entry_id": raw.get("nearest_train_entry_id"),
            "nearest_train_label_group": raw.get("nearest_train_label_group"),
            "nearest_train_fingerprint_id": raw.get("nearest_train_fingerprint_id"),
            "nearest_foldseek_prob": raw.get("nearest_foldseek_prob"),
            "nearest_foldseek_bits": raw.get("nearest_foldseek_bits"),
            "nearest_foldseek_lddt_tm_proxy": raw.get("nearest_foldseek_lddt_tm_proxy"),
            "retained_high_confidence_primary_fingerprint_hit_count": (
                raw.get("retained_high_confidence_primary_fingerprint_hit_count")
            ),
            "structural_neighborhood_bin": raw.get("structural_neighborhood_bin"),
            "fold_signals": scores,
            "top3_retained_train_neighbors": raw.get("top3_retained_train_neighbors") or [],
        })

    inscope = [r for r in scored_rows if r["is_inscope"]]
    oos = [r for r in scored_rows if r["is_oos"]]
    conf_pred = [r for r in scored_rows if r["is_confounded_predicted_geometry_oos"]]
    conf_any = [r for r in scored_rows if r["is_cofactor_confounded_oos_any_geometry"]]

    signal_names = list(scored_rows[0]["fold_signals"]) if scored_rows else []
    signals: dict[str, Any] = {}
    for name in signal_names:
        fn = lambda row, n=name: float(row["fold_signals"][n])
        signals[name] = {
            "auc_in_gt_oos": _auc_in_gt_oos([fn(r) for r in inscope], [fn(r) for r in oos]),
            "auc_in_gt_predicted_geometry_confounded_oos": _auc_in_gt_oos(
                [fn(r) for r in inscope], [fn(r) for r in conf_pred]
            ),
            "auc_in_gt_any_geometry_confounded_oos": _auc_in_gt_oos(
                [fn(r) for r in inscope], [fn(r) for r in conf_any]
            ),
            "in_scope_mean": _mean([fn(r) for r in inscope]),
            "oos_mean": _mean([fn(r) for r in oos]),
            "predicted_geometry_confounded_mean": _mean([fn(r) for r in conf_pred]),
            "best_at_90pct_inscope_retention": _best_threshold_at_retention(
                scored_rows, fn, min_retain=0.90
            ),
            "best_at_85pct_inscope_retention": _best_threshold_at_retention(
                scored_rows, fn, min_retain=0.85
            ),
        }

    primary_signal = "nearest_primary_foldseek_prob"
    overlap = [
        r for r in scored_rows
        if r["entry_id"] in geometry and r["entry_id"] in cofactor
    ]
    fold_values = [r["fold_signals"][primary_signal] for r in overlap]
    geom_values = [float(geometry[r["entry_id"]]["score"]) for r in overlap]
    cofactor_values = [
        max(cofactor[r["entry_id"]].get(c, 0.0) for c in COFACTOR_CLASSES)
        for r in overlap
    ]

    return {
        "artifact_id": "v3_fold_level_novelty_signal_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "computed_from_existing_selected_pdb_foldseek_proxy",
        "scope": (
            "Fold-level novelty diagnostic against the current702 heldout rows, "
            "using the frozen selected-PDB Foldseek/fast-3Di structural-neighborhood "
            "metadata already in the repo. This is a bounded fold proxy, not a new "
            "predicted-geometry Foldseek run."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_threshold_tuning_for_deployment": False,
            "m_csa_eval_only": True,
        },
        "counts": {
            "heldout_fold_rows_scored": len(scored_rows),
            "inscope": len(inscope),
            "oos": len(oos),
            "cofactor_confounded_oos_any_geometry": len(conf_any),
            "cofactor_confounded_oos_predicted_geometry_overlap": len(conf_pred),
            "channel_overlap_rows_for_correlation": len(overlap),
        },
        "confounded_entry_ids": {
            "any_geometry_from_novelty_eval": sorted(eight_confounded),
            "predicted_geometry_overlap_current_gate": sorted(predicted_confounded),
        },
        "signals": signals,
        "orthogonality_to_current_channels": {
            "primary_fold_signal": primary_signal,
            "pearson_fold_vs_predicted_geometry_top1": _pearson(fold_values, geom_values),
            "pearson_fold_vs_cofactor_max": _pearson(fold_values, cofactor_values),
            "pearson_predicted_geometry_top1_vs_cofactor_max": _pearson(geom_values, cofactor_values),
            "interpretation": (
                "The selected-PDB fold proxy is only weakly correlated with both "
                "current deployment channels on overlapping heldout rows, so it is "
                "partly orthogonal. It catches the confounded rows by fold novelty, "
                "but its standalone high-retention operating point remains weak."
            ),
        },
        "confounded_row_details": [
            r for r in scored_rows
            if r["is_confounded_predicted_geometry_oos"] or r["is_cofactor_confounded_oos_any_geometry"]
        ],
        "interpretation": {
            "does_fold_signal_catch_confounded_rows": (
                "yes_as_a_rank_signal; all predicted-geometry confounded rows have "
                "near-zero nearest-primary Foldseek support in the existing selected-PDB proxy"
            ),
            "operating_point_status": (
                "not_deployable_standalone; at >=85% or >=90% in-scope retention the "
                "nearest-primary Foldseek proxy cannot abstain many OOS rows, because "
                "many in-scope rows also lack strong primary structural-neighbor support"
            ),
            "deployment_gap": (
                "A real deployment fold channel still needs predicted-structure "
                "Foldseek/TM scoring against the in-distribution atlas; this artifact "
                "uses selected-PDB structure metadata already frozen in repo."
            ),
        },
        "source_artifacts": {
            "foldseek_metadata": {
                "path": str(foldseek_metadata_path),
                "sha256": _sha256(foldseek_metadata_path),
            },
            "esm2_150m_embeddings": {
                "path": str(esm2_150m_path),
                "sha256": _sha256(esm2_150m_path),
            },
            "cofactor_sidecar": {
                "path": str(cofactor_sidecar_path),
                "sha256": _sha256(cofactor_sidecar_path),
            },
            "predicted_geometry_audit": {
                "path": str(predicted_geometry_audit_path),
                "sha256": _sha256(predicted_geometry_audit_path),
            },
            "novelty_eval": {
                "path": str(novelty_eval_path),
                "sha256": _sha256(novelty_eval_path),
            },
        },
    }


def _render_fold_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    sig = audit["signals"]["nearest_primary_foldseek_prob"]
    ortho = audit["orthogonality_to_current_channels"]
    lines = [
        "# Fold-Level Novelty Signal - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Counts",
        "",
        f"- Heldout fold rows scored: {counts['heldout_fold_rows_scored']}",
        f"- In-scope: {counts['inscope']}",
        f"- OOS: {counts['oos']}",
        f"- Cofactor-confounded OOS from novelty eval: {counts['cofactor_confounded_oos_any_geometry']}",
        f"- Cofactor-confounded OOS overlapping predicted-geometry gate: {counts['cofactor_confounded_oos_predicted_geometry_overlap']}",
        "",
        "## Primary Signal",
        "",
        "`nearest_primary_foldseek_prob` is the top Foldseek probability only when the nearest training neighbor carries a primary fingerprint; otherwise it is 0. Higher means the row sits near the occupied primary atlas.",
        "",
        f"- AUC in-scope > all OOS: {sig['auc_in_gt_oos']}",
        f"- AUC in-scope > predicted-geometry confounded OOS: {sig['auc_in_gt_predicted_geometry_confounded_oos']}",
        f"- Mean in-scope: {sig['in_scope_mean']}; mean OOS: {sig['oos_mean']}; mean confounded: {sig['predicted_geometry_confounded_mean']}",
        f"- Best >=90% retention point: {sig['best_at_90pct_inscope_retention']}",
        f"- Best >=85% retention point: {sig['best_at_85pct_inscope_retention']}",
        "",
        "## Orthogonality",
        "",
        f"- Pearson fold vs predicted-geometry top1: {ortho['pearson_fold_vs_predicted_geometry_top1']}",
        f"- Pearson fold vs cofactor max: {ortho['pearson_fold_vs_cofactor_max']}",
        f"- Pearson predicted-geometry top1 vs cofactor max: {ortho['pearson_predicted_geometry_top1_vs_cofactor_max']}",
        "",
        ortho["interpretation"],
        "",
        "## Confounded Rows",
        "",
        "| Row | nearest primary prob | top3 primary prob | high-conf primary hits | nearest train label |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in audit["confounded_row_details"]:
        fs = row["fold_signals"]
        lines.append(
            f"| {row['entry_id']} | {fs['nearest_primary_foldseek_prob']} | "
            f"{fs['top3_primary_foldseek_prob']} | "
            f"{row['retained_high_confidence_primary_fingerprint_hit_count']} | "
            f"{row['nearest_train_label_group']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['does_fold_signal_catch_confounded_rows']}",
        f"- {audit['interpretation']['operating_point_status']}",
        f"- {audit['interpretation']['deployment_gap']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_level_novelty_signal(
    *,
    foldseek_metadata_path: Path,
    esm2_150m_path: Path,
    cofactor_sidecar_path: Path,
    predicted_geometry_audit_path: Path,
    novelty_eval_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_fold_level_novelty_signal(
        foldseek_metadata_path=foldseek_metadata_path,
        esm2_150m_path=esm2_150m_path,
        cofactor_sidecar_path=cofactor_sidecar_path,
        predicted_geometry_audit_path=predicted_geometry_audit_path,
        novelty_eval_path=novelty_eval_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_fold_report(audit), encoding="utf-8")
    return audit


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    match = re.match(r"^m_csa:(\d+)$", str(entry_id))
    if match:
        return ("m_csa", int(match.group(1)), str(entry_id))
    return (str(entry_id), -1, str(entry_id))


def _foldseek_binary_info(binary: str) -> dict[str, Any]:
    resolved = shutil.which(binary)
    if resolved is None:
        path = Path(binary)
        if path.exists():
            resolved = str(path.resolve())
    version = None
    version_command = None
    error = None
    if resolved:
        version_command = shlex.join([resolved, "version"])
        try:
            proc = subprocess.run(
                [resolved, "version"],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            version = (proc.stdout or proc.stderr).strip() or None
        except (OSError, subprocess.SubprocessError) as exc:
            error = f"{type(exc).__name__}: {exc}"
    return {
        "requested": binary,
        "resolved": resolved,
        "available": bool(resolved and version and not error),
        "version": version,
        "version_command": version_command,
        "error": error,
    }


def _predicted_row_status(row: dict[str, Any]) -> str:
    return str(row.get("predicted_geometry_status") or row.get("status") or "unknown")


def _predicted_row_ok(row: dict[str, Any]) -> bool:
    return _predicted_row_status(row) == "ok"


def _predicted_model_parts(row: dict[str, Any]) -> tuple[str | None, int | None, str | None]:
    pdb_id = str(row.get("predicted_pdb_id") or row.get("pdb_id") or "")
    match = re.match(r"^AF-(?P<accession>.+)-F1-model_v(?P<version>\d+)$", pdb_id)
    accession = str(row.get("accession") or row.get("sequence_id") or "").strip() or None
    version = None
    if match:
        accession = accession or match.group("accession")
        version = int(match.group("version"))
    return accession, version, pdb_id or None


def _afdb_cif_url(accession: str, version: int | None) -> str:
    model_version = int(version or 6)
    return f"https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v{model_version}.cif"


def _safe_path_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "unknown"


def _coordinate_requests(
    rows: list[dict[str, Any]],
    *,
    coordinate_root: Path,
    role: str,
    subdir: str,
) -> list[dict[str, Any]]:
    by_path: dict[str, dict[str, Any]] = {}
    for row in sorted(rows, key=lambda item: _entry_id_sort_key(str(item.get("entry_id")))):
        accession, version, predicted_pdb_id = _predicted_model_parts(row)
        entry_id = str(row.get("entry_id") or "")
        if not accession:
            key = f"missing_accession::{entry_id}"
            by_path[key] = {
                "role": role,
                "status": "missing_accession",
                "accession": None,
                "alphafold_version": version,
                "predicted_pdb_id": predicted_pdb_id,
                "url": None,
                "expected_local_path": None,
                "local_file_exists": False,
                "entry_ids": [entry_id],
                "rows": [
                    {
                        "entry_id": entry_id,
                        "split_assignment": row.get("split_assignment"),
                        "true_fingerprint_id": row.get("true_fingerprint_id"),
                        "benchmark_role": row.get("benchmark_role"),
                    }
                ],
            }
            continue
        token = _safe_path_token(f"{accession}_v{version or 6}")
        local_path = coordinate_root / subdir / f"afdb_{token}.cif"
        key = str(local_path)
        if key not in by_path:
            url = _afdb_cif_url(accession, version)
            by_path[key] = {
                "role": role,
                "status": "ready_to_materialize",
                "accession": accession,
                "alphafold_version": version or 6,
                "predicted_pdb_id": predicted_pdb_id,
                "url": url,
                "expected_local_path": str(local_path),
                "local_file_exists": local_path.exists(),
                "download_command": shlex.join(
                    ["curl", "-fL", "--retry", "3", url, "-o", str(local_path)]
                ),
                "entry_ids": [],
                "rows": [],
            }
        by_path[key]["entry_ids"].append(entry_id)
        by_path[key]["rows"].append(
            {
                "entry_id": entry_id,
                "split_assignment": row.get("split_assignment"),
                "true_fingerprint_id": row.get("true_fingerprint_id"),
                "benchmark_role": row.get("benchmark_role"),
                "top1_fingerprint_id": row.get("top1_fingerprint_id"),
            }
        )
    return sorted(
        by_path.values(),
        key=lambda item: (
            str(item.get("accession") or ""),
            _entry_id_sort_key(str((item.get("entry_ids") or [""])[0])),
        ),
    )


def _missing_coordinate_count(requests: list[dict[str, Any]]) -> int:
    return sum(1 for item in requests if not item.get("local_file_exists"))


def _foldseek_easy_search_command(
    *,
    binary: str,
    query_dir: Path,
    target_dir: Path,
    result_tsv: Path,
    tmp_dir: Path,
    threads: int,
) -> str:
    return shlex.join(
        [
            binary,
            "easy-search",
            str(query_dir),
            str(target_dir),
            str(result_tsv),
            str(tmp_dir),
            "--format-output",
            "query,target,qtmscore,ttmscore,alntmscore,prob,bits",
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
    )


def _request_aliases(request: dict[str, Any]) -> set[str]:
    path_value = request.get("expected_local_path")
    aliases = set()
    if path_value:
        path = Path(str(path_value))
        aliases.update({str(path), path.name, path.stem})
    accession = request.get("accession")
    version = request.get("alphafold_version")
    if accession:
        aliases.add(f"afdb_{_safe_path_token(f'{accession}_v{version or 6}')}")
        aliases.add(f"afdb_{_safe_path_token(f'{accession}_v{version or 6}')}.cif")
    predicted_pdb_id = request.get("predicted_pdb_id")
    if predicted_pdb_id:
        aliases.add(str(predicted_pdb_id))
    return aliases


def _alias_map(requests: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    alias_to_request: dict[str, dict[str, Any]] = {}
    collisions: set[str] = set()
    for request in requests:
        for alias in _request_aliases(request):
            if alias in alias_to_request and alias_to_request[alias] is not request:
                collisions.add(alias)
                continue
            alias_to_request[alias] = request
    for alias in collisions:
        alias_to_request.pop(alias, None)
    return alias_to_request, sorted(collisions)


def _parse_optional_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_foldseek_tsv_hits(
    *,
    result_tsv: Path,
    query_requests: list[dict[str, Any]],
    target_requests: list[dict[str, Any]],
) -> dict[str, Any]:
    if not result_tsv.exists():
        return {
            "status": "result_tsv_missing",
            "path": str(result_tsv),
            "nearest_atlas_hits": [],
            "summary": {
                "mapped_pair_count": 0,
                "unmapped_pair_count": 0,
                "query_entry_count_with_hits": 0,
            },
        }
    query_aliases, query_collisions = _alias_map(query_requests)
    target_aliases, target_collisions = _alias_map(target_requests)
    nearest: dict[str, dict[str, Any]] = {}
    mapped_pair_count = 0
    unmapped_pair_count = 0
    unmapped_names: set[str] = set()
    for line in result_tsv.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if parts[0] == "query":
            continue
        if len(parts) < 5:
            unmapped_pair_count += 1
            continue
        raw_query, raw_target = parts[0], parts[1]
        query_request = query_aliases.get(raw_query)
        target_request = target_aliases.get(raw_target)
        if query_request is None or target_request is None:
            unmapped_pair_count += 1
            if query_request is None:
                unmapped_names.add(raw_query)
            if target_request is None:
                unmapped_names.add(raw_target)
            continue
        qtmscore = _parse_optional_float(parts[2])
        ttmscore = _parse_optional_float(parts[3])
        alntmscore = _parse_optional_float(parts[4])
        scores = [s for s in (qtmscore, ttmscore, alntmscore) if s is not None]
        if not scores:
            unmapped_pair_count += 1
            continue
        mapped_pair_count += 1
        tm_score = max(scores)
        prob = _parse_optional_float(parts[5]) if len(parts) > 5 else None
        bits = _parse_optional_float(parts[6]) if len(parts) > 6 else None
        target_row = (target_request.get("rows") or [{}])[0]
        for query_row in query_request.get("rows") or []:
            entry_id = str(query_row.get("entry_id"))
            candidate = {
                "query_entry_id": entry_id,
                "query_accession": query_request.get("accession"),
                "raw_query_name": raw_query,
                "nearest_atlas_entry_id": target_row.get("entry_id"),
                "nearest_atlas_accession": target_request.get("accession"),
                "nearest_atlas_true_fingerprint_id": target_row.get("true_fingerprint_id"),
                "raw_target_name": raw_target,
                "tm_score": round(tm_score, 6),
                "qtmscore": qtmscore,
                "ttmscore": ttmscore,
                "alntmscore": alntmscore,
                "prob": prob,
                "bits": bits,
            }
            previous = nearest.get(entry_id)
            if previous is None or candidate["tm_score"] > previous["tm_score"]:
                nearest[entry_id] = candidate
    hits = sorted(nearest.values(), key=lambda row: _entry_id_sort_key(row["query_entry_id"]))
    return {
        "status": "parsed" if hits else "parsed_no_mapped_hits",
        "path": str(result_tsv),
        "nearest_atlas_hits": hits,
        "summary": {
            "mapped_pair_count": mapped_pair_count,
            "unmapped_pair_count": unmapped_pair_count,
            "query_entry_count_with_hits": len(hits),
            "max_nearest_atlas_tm_score": (
                round(max(row["tm_score"] for row in hits), 6) if hits else None
            ),
            "min_nearest_atlas_tm_score": (
                round(min(row["tm_score"] for row in hits), 6) if hits else None
            ),
            "alias_collision_count": len(query_collisions) + len(target_collisions),
            "alias_collisions": query_collisions + target_collisions,
            "unmapped_names": sorted(unmapped_names),
        },
    }


def _fold_channel_signal_from_hits(
    *,
    hits: list[dict[str, Any]],
    query_requests: list[dict[str, Any]],
    confounded_ids: set[str],
) -> dict[str, Any] | None:
    row_context = {
        str(row.get("entry_id")): row
        for request in query_requests
        for row in request.get("rows") or []
        if row.get("entry_id")
    }
    scored_rows = []
    for hit in hits:
        entry_id = str(hit.get("query_entry_id"))
        context = row_context.get(entry_id, {})
        if not context:
            continue
        scored_rows.append(
            {
                "entry_id": entry_id,
                "true_fingerprint_id": context.get("true_fingerprint_id"),
                "is_inscope": bool(context.get("true_fingerprint_id")),
                "is_oos": not bool(context.get("true_fingerprint_id")),
                "is_confounded_predicted_geometry_oos": entry_id in confounded_ids,
                "fold_signals": {"nearest_atlas_tm_score": float(hit["tm_score"])},
                "nearest_atlas_entry_id": hit.get("nearest_atlas_entry_id"),
                "nearest_atlas_true_fingerprint_id": hit.get(
                    "nearest_atlas_true_fingerprint_id"
                ),
            }
        )
    if not scored_rows:
        return None
    inscope = [row for row in scored_rows if row["is_inscope"]]
    oos = [row for row in scored_rows if row["is_oos"]]
    conf = [row for row in oos if row["is_confounded_predicted_geometry_oos"]]
    agn = [row for row in oos if not row["is_confounded_predicted_geometry_oos"]]
    fn = lambda row: float(row["fold_signals"]["nearest_atlas_tm_score"])
    return {
        "signal_name": "nearest_atlas_tm_score",
        "direction": "higher_means_nearer_to_in_distribution_predicted_atlas",
        "counts": {
            "heldout_rows_scored": len(scored_rows),
            "inscope": len(inscope),
            "oos": len(oos),
            "confounded_oos": len(conf),
            "agnostic_oos": len(agn),
        },
        "auc_in_gt_oos_all": _auc_in_gt_oos([fn(row) for row in inscope], [fn(row) for row in oos]),
        "auc_in_gt_confounded_oos": _auc_in_gt_oos(
            [fn(row) for row in inscope], [fn(row) for row in conf]
        ),
        "auc_in_gt_agnostic_oos": _auc_in_gt_oos(
            [fn(row) for row in inscope], [fn(row) for row in agn]
        ),
        "in_scope_mean": _mean([fn(row) for row in inscope]),
        "oos_mean": _mean([fn(row) for row in oos]),
        "confounded_mean": _mean([fn(row) for row in conf]),
        "best_at_90pct_inscope_retention": _best_threshold_at_retention(
            scored_rows, fn, min_retain=0.90
        ),
        "best_at_85pct_inscope_retention": _best_threshold_at_retention(
            scored_rows, fn, min_retain=0.85
        ),
        "row_scores": scored_rows,
    }


def build_predicted_structure_fold_channel(
    *,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
    coordinate_root: Path,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    threads: int = 4,
    priority_result_tsv: Path | None = None,
    heldout_result_tsv: Path | None = None,
) -> dict[str, Any]:
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    fold_signal = _read_json(fold_level_signal_path)
    rows = [
        row
        for row in predicted_atlas.get("results", [])
        if isinstance(row, dict)
    ]
    atlas_rows = [
        row
        for row in rows
        if row.get("split_assignment") == "in_distribution" and _predicted_row_ok(row)
    ]
    heldout_ok_rows = [
        row
        for row in rows
        if row.get("split_assignment") == "heldout" and _predicted_row_ok(row)
    ]
    confounded_ids = set(
        fold_signal.get("confounded_entry_ids", {}).get(
            "predicted_geometry_overlap_current_gate", []
        )
    )
    priority_rows = [
        row for row in heldout_ok_rows if str(row.get("entry_id")) in confounded_ids
    ]
    missing_priority_ids = sorted(
        confounded_ids - {str(row.get("entry_id")) for row in priority_rows},
        key=_entry_id_sort_key,
    )

    coordinate_root = Path(coordinate_root)
    atlas_dir = coordinate_root / "atlas_in_distribution"
    priority_query_dir = coordinate_root / "queries_cofactor_confounded_oos"
    heldout_query_dir = coordinate_root / "queries_all_heldout"
    result_root = coordinate_root.parent / f"{coordinate_root.name}_foldseek_results"

    atlas_requests = _coordinate_requests(
        atlas_rows,
        coordinate_root=coordinate_root,
        role="atlas_in_distribution_target",
        subdir="atlas_in_distribution",
    )
    priority_requests = _coordinate_requests(
        priority_rows,
        coordinate_root=coordinate_root,
        role="priority_query_cofactor_confounded_oos",
        subdir="queries_cofactor_confounded_oos",
    )
    heldout_requests = _coordinate_requests(
        heldout_ok_rows,
        coordinate_root=coordinate_root,
        role="all_heldout_query_when_cheap",
        subdir="queries_all_heldout",
    )
    foldseek = _foldseek_binary_info(foldseek_binary)
    resolved_binary = str(foldseek.get("resolved") or foldseek_binary)

    priority_command = _foldseek_easy_search_command(
        binary=resolved_binary,
        query_dir=priority_query_dir,
        target_dir=atlas_dir,
        result_tsv=priority_result_tsv
        or result_root / "cofactor_confounded_oos_vs_atlas.tsv",
        tmp_dir=result_root / "tmp_confounded",
        threads=threads,
    )
    heldout_command = _foldseek_easy_search_command(
        binary=resolved_binary,
        query_dir=heldout_query_dir,
        target_dir=atlas_dir,
        result_tsv=heldout_result_tsv or result_root / "all_heldout_vs_atlas.tsv",
        tmp_dir=result_root / "tmp_all_heldout",
        threads=threads,
    )
    materialization_command = (
        "python - <<'PY'\n"
        "import json\n"
        "import urllib.request\n"
        "from pathlib import Path\n"
        f"artifact = json.loads(Path('artifacts/{PREDICTED_STRUCTURE_FOLD_CHANNEL_ID}.json').read_text())\n"
        "groups = artifact['foldseek_input_manifest']['coordinate_request_groups']\n"
        "for group in groups.values():\n"
        "    for item in group:\n"
        "        path = item.get('expected_local_path')\n"
        "        url = item.get('url')\n"
        "        if not path or not url:\n"
        "            continue\n"
        "        target = Path(path)\n"
        "        target.parent.mkdir(parents=True, exist_ok=True)\n"
        "        if target.exists():\n"
        "            continue\n"
        "        urllib.request.urlretrieve(url, target)\n"
        "PY"
    )

    priority_missing = _missing_coordinate_count(atlas_requests) + _missing_coordinate_count(
        priority_requests
    )
    heldout_missing = _missing_coordinate_count(atlas_requests) + _missing_coordinate_count(
        heldout_requests
    )
    blockers: list[str] = []
    if not foldseek["available"]:
        blockers.append("foldseek_runtime_unavailable")
    if priority_missing:
        blockers.append("predicted_coordinate_files_missing_for_priority_scope")
    if heldout_missing:
        blockers.append("predicted_coordinate_files_missing_for_all_heldout_scope")
    priority_result = _parse_foldseek_tsv_hits(
        result_tsv=priority_result_tsv
        or result_root / "cofactor_confounded_oos_vs_atlas.tsv",
        query_requests=priority_requests,
        target_requests=atlas_requests,
    )
    heldout_result = _parse_foldseek_tsv_hits(
        result_tsv=heldout_result_tsv or result_root / "all_heldout_vs_atlas.tsv",
        query_requests=heldout_requests,
        target_requests=atlas_requests,
    )
    if priority_result["status"] != "parsed":
        blockers.append("priority_foldseek_results_not_computed_or_parsed")
    if heldout_result["status"] != "parsed":
        blockers.append("all_heldout_foldseek_results_not_computed_or_parsed")
    all_heldout_signal = _fold_channel_signal_from_hits(
        hits=heldout_result.get("nearest_atlas_hits", []),
        query_requests=heldout_requests,
        confounded_ids=confounded_ids,
    )
    status = (
        "computed_all_heldout_foldseek_scores"
        if heldout_result["status"] == "parsed"
        else "computed_priority_foldseek_scores"
        if priority_result["status"] == "parsed"
        else (
            "ready_to_run_foldseek_priority_scope"
            if foldseek["available"] and priority_missing == 0
            else "manifest_staged_missing_predicted_coordinate_bundle"
        )
    )
    if heldout_result["status"] == "parsed":
        current_result = (
            "All-heldout Foldseek/TM scores were parsed from the configured result TSV; "
            "the fold channel now has a real nearest-atlas TM signal for every ok "
            "predicted-geometry heldout row."
        )
        next_action = (
            "Use the all-heldout fold-channel signal in the next abstention combiner "
            "diagnostic, or decide whether persistent predicted-CIF coordinate "
            "provenance should be committed."
        )
    elif priority_result["status"] == "parsed":
        current_result = (
            "Priority Foldseek/TM scores for the cofactor-confounded OOS rows were "
            "parsed from the configured result TSV; the full all-heldout sweep remains "
            "uncomputed."
        )
        next_action = (
            "Run the all-heldout Foldseek/TM sweep when cheap, or commit a dedicated "
            "predicted CIF bundle if persistent coordinate provenance is required."
        )
    else:
        current_result = (
            "No Foldseek/TM scores are claimed here because the current repo does not "
            "contain a dedicated predicted AlphaFold CIF bundle for these current702 "
            "atlas/query rows."
        )
        next_action = (
            "Materialize the exact AFDB v6 coordinate requests, run the priority "
            "Foldseek command, then rerun the parser to emit nearest-atlas TM scores "
            "for the six confounded rows before the all-heldout sweep."
        )

    return {
        "artifact_id": PREDICTED_STRUCTURE_FOLD_CHANNEL_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Bounded manifest for a deployment-regime predicted-structure "
            "Foldseek/TM channel: AlphaFoldDB-predicted heldout rows scored "
            "against the current702 in-distribution predicted-structure atlas."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_threshold_tuning_for_deployment": False,
            "large_model_downloads_performed": False,
            "frozen_current702_inputs_only": True,
            "score_fabrication": False,
        },
        "counts": {
            "combined_predicted_retrieval_rows": len(rows),
            "atlas_in_distribution_rows_ok": len(atlas_rows),
            "heldout_rows_ok": len(heldout_ok_rows),
            "priority_cofactor_confounded_oos_rows": len(priority_rows),
            "priority_cofactor_confounded_oos_missing_ids": len(missing_priority_ids),
            "atlas_coordinate_requests": len(atlas_requests),
            "priority_query_coordinate_requests": len(priority_requests),
            "all_heldout_query_coordinate_requests": len(heldout_requests),
            "priority_scope_missing_coordinate_files": priority_missing,
            "all_heldout_scope_missing_coordinate_files": heldout_missing,
        },
        "target_rows": {
            "priority_cofactor_confounded_oos_entry_ids": [
                str(row.get("entry_id"))
                for row in sorted(priority_rows, key=lambda item: _entry_id_sort_key(str(item.get("entry_id"))))
            ],
            "priority_cofactor_confounded_oos_missing_ids": missing_priority_ids,
            "all_heldout_when_cheap_entry_count": len(heldout_ok_rows),
        },
        "runtime": {
            "foldseek": foldseek,
            "threads": max(1, int(threads)),
        },
        "blockers": blockers,
        "parsed_foldseek_results": {
            "priority_cofactor_confounded_oos_vs_atlas": priority_result,
            "all_heldout_vs_atlas": heldout_result,
        },
        "fold_channel_signal": {
            "nearest_atlas_tm_score": all_heldout_signal,
        },
        "foldseek_input_manifest": {
            "coordinate_root": str(coordinate_root),
            "atlas_database_dir": str(atlas_dir),
            "priority_query_dir": str(priority_query_dir),
            "all_heldout_query_dir": str(heldout_query_dir),
            "result_root": str(result_root),
            "coordinate_request_groups": {
                "atlas_in_distribution": atlas_requests,
                "priority_cofactor_confounded_oos_queries": priority_requests,
                "all_heldout_queries_when_cheap": heldout_requests,
            },
        },
        "commands": {
            "materialize_coordinate_bundle": materialization_command,
            "run_priority_cofactor_confounded_oos_vs_atlas": priority_command,
            "run_all_heldout_vs_atlas_when_cheap": heldout_command,
            "expected_foldseek_tsv_columns": [
                "query",
                "target",
                "qtmscore",
                "ttmscore",
                "alntmscore",
                "prob",
                "bits",
            ],
            "scoring_contract": (
                "Per query, score the nearest in-distribution atlas hit by "
                "max(qtmscore, ttmscore, alntmscore); lower nearest-atlas TM "
                "support is the fold-novelty direction."
            ),
        },
        "source_artifacts": {
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "fold_level_signal": {
                "path": str(fold_level_signal_path),
                "sha256": _sha256(fold_level_signal_path),
            },
        },
        "interpretation": {
            "current_result": current_result,
            "next_action": next_action,
        },
    }


def _render_predicted_structure_fold_channel_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    parsed = audit.get("parsed_foldseek_results", {})
    priority_parsed = parsed.get("priority_cofactor_confounded_oos_vs_atlas", {})
    heldout_parsed = parsed.get("all_heldout_vs_atlas", {})
    lines = [
        "# Predicted-Structure Fold Channel - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Foldseek available: {audit['runtime']['foldseek']['available']}",
        f"- Priority scope missing coordinate files: {counts['priority_scope_missing_coordinate_files']}",
        f"- All-heldout scope missing coordinate files: {counts['all_heldout_scope_missing_coordinate_files']}",
        f"- Priority Foldseek TSV parse status: {priority_parsed.get('status')}",
        f"- All-heldout Foldseek TSV parse status: {heldout_parsed.get('status')}",
        "",
        "## Scope Counts",
        "",
        f"- Atlas in-distribution rows with ok predicted geometry: {counts['atlas_in_distribution_rows_ok']}",
        f"- Heldout rows with ok predicted geometry: {counts['heldout_rows_ok']}",
        f"- Priority cofactor-confounded OOS rows: {counts['priority_cofactor_confounded_oos_rows']}",
        "",
        "## Priority Rows",
        "",
    ]
    for entry_id in audit["target_rows"]["priority_cofactor_confounded_oos_entry_ids"]:
        lines.append(f"- {entry_id}")
    lines += [
        "",
        "## Blockers",
        "",
    ]
    if audit["status"].startswith("computed_") and audit["blockers"]:
        lines += [
            "- The scored Foldseek TSVs below were parsed successfully; these blockers track "
            "missing persistent coordinate-file provenance for reproduction.",
        ]
    for blocker in audit["blockers"]:
        lines.append(f"- {blocker}")
    lines += [
        "",
        "## All-Heldout Fold Signal",
        "",
    ]
    fold_signal = (audit.get("fold_channel_signal") or {}).get("nearest_atlas_tm_score")
    if fold_signal:
        lines += [
            f"- AUC in-scope > all OOS: {fold_signal['auc_in_gt_oos_all']}",
            f"- AUC in-scope > confounded OOS: {fold_signal['auc_in_gt_confounded_oos']}",
            f"- Mean in-scope: {fold_signal['in_scope_mean']}; mean OOS: {fold_signal['oos_mean']}; mean confounded: {fold_signal['confounded_mean']}",
            f"- Best >=90% retention diagnostic: {fold_signal['best_at_90pct_inscope_retention']}",
            f"- Best >=85% retention diagnostic: {fold_signal['best_at_85pct_inscope_retention']}",
        ]
    else:
        lines.append("- All-heldout Foldseek/TM scores have not been parsed yet.")
    lines += [
        "",
        "## Priority Parsed Hits",
        "",
    ]
    priority_hits = priority_parsed.get("nearest_atlas_hits", [])
    if priority_hits:
        lines += [
            "| Query | nearest atlas | atlas fingerprint | TM score |",
            "| --- | --- | --- | ---: |",
        ]
        for hit in priority_hits:
            lines.append(
                f"| {hit['query_entry_id']} | {hit['nearest_atlas_entry_id']} | "
                f"{hit['nearest_atlas_true_fingerprint_id']} | {hit['tm_score']} |"
            )
    else:
        lines.append("- No priority Foldseek hits parsed yet.")
    lines += [
        "",
        "## Commands",
        "",
        "Materialize the exact predicted CIF bundle:",
        "",
        "```bash",
        audit["commands"]["materialize_coordinate_bundle"],
        "```",
        "",
        "Run the six-row priority Foldseek/TM pass:",
        "",
        "```bash",
        audit["commands"]["run_priority_cofactor_confounded_oos_vs_atlas"],
        "```",
        "",
        "Run all heldout rows when cheap:",
        "",
        "```bash",
        audit["commands"]["run_all_heldout_vs_atlas_when_cheap"],
        "```",
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['current_result']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_predicted_structure_fold_channel(
    *,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
    coordinate_root: Path,
    out_path: Path,
    report_path: Path | None = None,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    threads: int = 4,
    priority_result_tsv: Path | None = None,
    heldout_result_tsv: Path | None = None,
) -> dict[str, Any]:
    audit = build_predicted_structure_fold_channel(
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        fold_level_signal_path=fold_level_signal_path,
        coordinate_root=coordinate_root,
        foldseek_binary=foldseek_binary,
        threads=threads,
        priority_result_tsv=priority_result_tsv,
        heldout_result_tsv=heldout_result_tsv,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_predicted_structure_fold_channel_report(audit),
            encoding="utf-8",
        )
    return audit


GEOMETRY_VARIANT_FEATURES = (
    "score",
    "role_match_fraction",
    "residue_match_fraction",
    "mechanistic_coherence_score",
    "substrate_pocket_score",
    "compactness_score",
    "cofactor_context_score",
    "counterevidence_penalty",
    "plp_ligand_anchor_score",
)


def _top1_fingerprint(row: dict[str, Any]) -> dict[str, Any] | None:
    top = row.get("top_fingerprints") or []
    if not top or not isinstance(top[0], dict):
        return None
    return top[0]


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    mid = len(sorted_values) // 2
    if len(sorted_values) % 2:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2


def _quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    pos = (len(sorted_values) - 1) * q
    lower = int(math.floor(pos))
    upper = int(math.ceil(pos))
    if lower == upper:
        return sorted_values[lower]
    weight = pos - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def _percentile_rank(value: float, atlas_values: list[float]) -> float:
    if not atlas_values:
        return 0.0
    return sum(1 for item in atlas_values if item <= value) / len(atlas_values)


def _feature_vector(top: dict[str, Any]) -> list[float]:
    return [float(top.get(name) or 0.0) for name in GEOMETRY_VARIANT_FEATURES]


def _robust_center_scale(vectors: list[list[float]]) -> tuple[list[float], list[float]]:
    if not vectors:
        return [], []
    dims = len(vectors[0])
    centers = []
    scales = []
    for idx in range(dims):
        col = [vec[idx] for vec in vectors]
        centers.append(_median(col))
        iqr = _quantile(col, 0.75) - _quantile(col, 0.25)
        scales.append(iqr if abs(iqr) > 1e-9 else 1.0)
    return centers, scales


def _robust_distance(vector: list[float], center: list[float], scale: list[float]) -> float:
    if not center:
        return 0.0
    return math.sqrt(
        sum(((value - center[idx]) / scale[idx]) ** 2 for idx, value in enumerate(vector))
    )


def _signal_metrics(
    rows: list[dict[str, Any]],
    score_name: str,
) -> dict[str, Any]:
    inscope = [r for r in rows if r["is_inscope"]]
    oos = [r for r in rows if r["is_oos"]]
    conf = [r for r in oos if r["is_confounded_predicted_geometry_oos"]]
    agn = [r for r in oos if not r["is_confounded_predicted_geometry_oos"]]
    fn = lambda row: float(row["variant_scores"][score_name])
    return {
        "auc_in_gt_oos_all": _auc_in_gt_oos([fn(r) for r in inscope], [fn(r) for r in oos]),
        "auc_in_gt_confounded_oos": _auc_in_gt_oos([fn(r) for r in inscope], [fn(r) for r in conf]),
        "auc_in_gt_agnostic_oos": _auc_in_gt_oos([fn(r) for r in inscope], [fn(r) for r in agn]),
        "in_scope_mean": _mean([fn(r) for r in inscope]),
        "oos_mean": _mean([fn(r) for r in oos]),
        "confounded_mean": _mean([fn(r) for r in conf]),
        "best_at_90pct_inscope_retention": _best_threshold_at_retention(
            rows, fn, min_retain=0.90
        ),
        "best_at_85pct_inscope_retention": _best_threshold_at_retention(
            rows, fn, min_retain=0.85
        ),
    }


def build_predicted_atlas_geometry_novelty_variants(
    *,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
) -> dict[str, Any]:
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    fold_signal = _read_json(fold_level_signal_path)
    rows = [
        row
        for row in predicted_atlas.get("results", [])
        if isinstance(row, dict) and _predicted_row_ok(row) and _top1_fingerprint(row)
    ]
    atlas_rows = [
        row
        for row in rows
        if row.get("split_assignment") == "in_distribution" and row.get("true_fingerprint_id")
    ]
    heldout_rows = [row for row in rows if row.get("split_assignment") == "heldout"]
    if not atlas_rows or not heldout_rows:
        return {
            "artifact_id": "v3_predicted_atlas_geometry_novelty_variants_current702_20260601",
            "schema_version": SCHEMA_VERSION,
            "created_utc": _utc_now_iso(),
            "status": "insufficient_rows",
            "counts": {"atlas": len(atlas_rows), "heldout": len(heldout_rows)},
        }

    atlas_vectors = [_feature_vector(_top1_fingerprint(row) or {}) for row in atlas_rows]
    center, scale = _robust_center_scale(atlas_vectors)
    class_centers: dict[str, list[float]] = {}
    for fp in sorted({str(row.get("true_fingerprint_id")) for row in atlas_rows}):
        members = [
            _feature_vector(_top1_fingerprint(row) or {})
            for row in atlas_rows
            if str(row.get("true_fingerprint_id")) == fp
        ]
        class_centers[fp] = [
            sum(vec[idx] for vec in members) / len(members)
            for idx in range(len(GEOMETRY_VARIANT_FEATURES))
        ]
    atlas_feature_values = {
        name: [float((_top1_fingerprint(row) or {}).get(name) or 0.0) for row in atlas_rows]
        for name in GEOMETRY_VARIANT_FEATURES
    }
    atlas_score_x_role = [
        float((_top1_fingerprint(row) or {}).get("score") or 0.0)
        * float((_top1_fingerprint(row) or {}).get("role_match_fraction") or 0.0)
        for row in atlas_rows
    ]
    confounded_ids = set(
        fold_signal.get("confounded_entry_ids", {}).get(
            "predicted_geometry_overlap_current_gate", []
        )
    )

    scored_rows: list[dict[str, Any]] = []
    for row in sorted(heldout_rows, key=lambda item: _entry_id_sort_key(str(item.get("entry_id")))):
        top = _top1_fingerprint(row) or {}
        vector = _feature_vector(top)
        global_distance = _robust_distance(vector, center, scale)
        nearest_class_distance = min(
            _robust_distance(vector, class_center, scale)
            for class_center in class_centers.values()
        )
        score = float(top.get("score") or 0.0)
        role = float(top.get("role_match_fraction") or 0.0)
        score_x_role = score * role
        variant_scores = {
            "top1_score_raw": score,
            "top1_score_atlas_percentile": _percentile_rank(
                score, atlas_feature_values["score"]
            ),
            "role_match_fraction_raw": role,
            "role_match_fraction_atlas_percentile": _percentile_rank(
                role, atlas_feature_values["role_match_fraction"]
            ),
            "top1_score_x_role_raw": score_x_role,
            "top1_score_x_role_atlas_percentile": _percentile_rank(
                score_x_role, atlas_score_x_role
            ),
            "cofactor_context_score_raw": float(top.get("cofactor_context_score") or 0.0),
            "cofactor_context_score_atlas_percentile": _percentile_rank(
                float(top.get("cofactor_context_score") or 0.0),
                atlas_feature_values["cofactor_context_score"],
            ),
            "negative_robust_distance_to_atlas_median": -global_distance,
            "negative_nearest_class_centroid_robust_distance": -nearest_class_distance,
        }
        scored_rows.append(
            {
                "entry_id": row.get("entry_id"),
                "split_assignment": row.get("split_assignment"),
                "true_fingerprint_id": row.get("true_fingerprint_id"),
                "is_inscope": bool(row.get("true_fingerprint_id")),
                "is_oos": not bool(row.get("true_fingerprint_id")),
                "is_confounded_predicted_geometry_oos": row.get("entry_id") in confounded_ids,
                "top1_fingerprint_id": top.get("fingerprint_id"),
                "variant_scores": {
                    key: round(value, 6) for key, value in variant_scores.items()
                },
            }
        )

    signal_names = list(scored_rows[0]["variant_scores"]) if scored_rows else []
    signals = {
        name: _signal_metrics(scored_rows, name)
        for name in signal_names
    }
    best_name, best_signal = max(
        signals.items(),
        key=lambda item: item[1]["auc_in_gt_oos_all"] or 0.0,
    )
    return {
        "artifact_id": "v3_predicted_atlas_geometry_novelty_variants_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "computed_predicted_atlas_geometry_variants",
        "scope": (
            "Bounded predicted-geometry atlas novelty rerun using the newly "
            "available in-distribution predicted atlas rows. All atlas statistics "
            "are computed from in-distribution rows only; heldout rows are final "
            "evaluation diagnostics."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_threshold_tuning_for_deployment": False,
            "atlas_statistics_only_for_normalization": True,
        },
        "counts": {
            "atlas_rows": len(atlas_rows),
            "heldout_rows": len(scored_rows),
            "inscope": sum(1 for row in scored_rows if row["is_inscope"]),
            "oos": sum(1 for row in scored_rows if row["is_oos"]),
            "confounded_predicted_geometry_oos": sum(
                1 for row in scored_rows if row["is_confounded_predicted_geometry_oos"]
            ),
            "atlas_true_fingerprint_counts": dict(
                sorted(Counter(str(row.get("true_fingerprint_id")) for row in atlas_rows).items())
            ),
        },
        "signals": signals,
        "best_signal": {
            "name": best_name,
            "auc_in_gt_oos_all": best_signal["auc_in_gt_oos_all"],
            "auc_in_gt_confounded_oos": best_signal["auc_in_gt_confounded_oos"],
            "best_at_90pct_inscope_retention": best_signal[
                "best_at_90pct_inscope_retention"
            ],
            "best_at_85pct_inscope_retention": best_signal[
                "best_at_85pct_inscope_retention"
            ],
        },
        "row_scores": scored_rows,
        "interpretation": {
            "headline": (
                f"Best predicted-atlas geometry variant is {best_name} with "
                f"AUC {best_signal['auc_in_gt_oos_all']}."
            ),
            "operating_point_caveat": (
                "Post-hoc retention rows are diagnostics only; no deployment "
                "threshold is selected or written to production."
            ),
        },
        "source_artifacts": {
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "fold_level_signal": {
                "path": str(fold_level_signal_path),
                "sha256": _sha256(fold_level_signal_path),
            },
        },
    }


def _render_predicted_atlas_geometry_novelty_variants_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    best = audit["best_signal"]
    lines = [
        "# Predicted-Atlas Geometry Novelty Variants - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Counts",
        "",
        f"- Atlas rows: {counts['atlas_rows']}",
        f"- Heldout rows: {counts['heldout_rows']}",
        f"- In-scope: {counts['inscope']}",
        f"- OOS: {counts['oos']}",
        f"- Cofactor-confounded OOS: {counts['confounded_predicted_geometry_oos']}",
        "",
        "## Best Signal",
        "",
        f"- {best['name']}: AUC all OOS {best['auc_in_gt_oos_all']}; confounded AUC {best['auc_in_gt_confounded_oos']}",
        f"- Best >=90% retention diagnostic: {best['best_at_90pct_inscope_retention']}",
        f"- Best >=85% retention diagnostic: {best['best_at_85pct_inscope_retention']}",
        "",
        "## Signals",
        "",
        "| Signal | all OOS AUC | confounded AUC | agnostic AUC |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, sig in audit["signals"].items():
        lines.append(
            f"| {name} | {sig['auc_in_gt_oos_all']} | "
            f"{sig['auc_in_gt_confounded_oos']} | {sig['auc_in_gt_agnostic_oos']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['operating_point_caveat']}",
    ]
    return "\n".join(lines) + "\n"


def write_predicted_atlas_geometry_novelty_variants(
    *,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_predicted_atlas_geometry_novelty_variants(
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        fold_level_signal_path=fold_level_signal_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_predicted_atlas_geometry_novelty_variants_report(audit),
            encoding="utf-8",
        )
    return audit


REQUIRED_SELECTED_COFACTOR_RECORD_KEYS = (
    "entry_id",
    "class",
    "cofactor_class",
    "selected_score",
    "selected_source",
    "selected_source_status",
    "split_assignment",
    "threshold_or_bin",
    "source_artifact",
    "source_channel_artifact",
    "provenance_hashes",
)


def build_selected_organic_cofactor_sidecar_schema_audit(
    *,
    selected_organic_cofactor_sidecar_path: Path,
    label_manifest_path: Path,
) -> dict[str, Any]:
    sidecar = _read_json(selected_organic_cofactor_sidecar_path)
    manifest = _read_json(label_manifest_path)
    records = [
        record
        for record in sidecar.get("row_class_records", [])
        if isinstance(record, dict)
    ]
    manifest_rows = [
        row for row in manifest.get("rows", []) if isinstance(row, dict)
    ]
    split_by_entry = {
        str(row.get("entry_id")): row.get("split_assignment")
        for row in manifest_rows
        if row.get("entry_id")
    }
    expected_entries = set(split_by_entry)
    expected_pairs = {
        (entry_id, cls)
        for entry_id in expected_entries
        for cls in COFACTOR_CLASSES
    }
    seen_pairs: set[tuple[str, str]] = set()
    duplicate_pairs: list[dict[str, Any]] = []
    missing_key_rows: list[dict[str, Any]] = []
    score_range_violations: list[dict[str, Any]] = []
    class_mismatches: list[dict[str, Any]] = []
    split_mismatches: list[dict[str, Any]] = []
    threshold_policy_violations: list[dict[str, Any]] = []
    fallback_source_rows: list[dict[str, Any]] = []
    missing_source_paths: list[dict[str, Any]] = []
    provenance_missing_rows: list[dict[str, Any]] = []

    for record in records:
        entry_id = str(record.get("entry_id") or "")
        cls = str(record.get("class") or "")
        pair = (entry_id, cls)
        if pair in seen_pairs:
            duplicate_pairs.append({"entry_id": entry_id, "class": cls})
        seen_pairs.add(pair)
        missing_keys = [
            key for key in REQUIRED_SELECTED_COFACTOR_RECORD_KEYS if key not in record
        ]
        if missing_keys:
            missing_key_rows.append(
                {"entry_id": entry_id, "class": cls, "missing_keys": missing_keys}
            )
        if cls != record.get("cofactor_class"):
            class_mismatches.append(
                {
                    "entry_id": entry_id,
                    "class": cls,
                    "cofactor_class": record.get("cofactor_class"),
                }
            )
        score = record.get("selected_score")
        if not isinstance(score, (int, float)) or not 0.0 <= float(score) <= 1.0:
            score_range_violations.append(
                {"entry_id": entry_id, "class": cls, "selected_score": score}
            )
        expected_split = split_by_entry.get(entry_id)
        if expected_split is None or record.get("split_assignment") != expected_split:
            split_mismatches.append(
                {
                    "entry_id": entry_id,
                    "class": cls,
                    "record_split": record.get("split_assignment"),
                    "manifest_split": expected_split,
                }
            )
        threshold = record.get("threshold_or_bin") or {}
        if (
            threshold.get("fixed_threshold") != 0.5
            or threshold.get("threshold_policy") != "fixed_0_5_not_tuned_on_heldout"
        ):
            threshold_policy_violations.append(
                {"entry_id": entry_id, "class": cls, "threshold_or_bin": threshold}
            )
        source = str(record.get("selected_source") or "")
        status = str(record.get("selected_source_status") or "")
        if "fallback" in source.lower() or "fallback" in status.lower():
            fallback_source_rows.append(
                {"entry_id": entry_id, "class": cls, "selected_source": source}
            )
        for path_key in ("source_artifact", "source_channel_artifact", "source_summary_artifact"):
            path_value = record.get(path_key)
            if path_value and not Path(str(path_value)).exists():
                missing_source_paths.append(
                    {
                        "entry_id": entry_id,
                        "class": cls,
                        "path_key": path_key,
                        "path": path_value,
                    }
                )
        provenance = record.get("provenance_hashes")
        if not isinstance(provenance, dict) or not provenance:
            provenance_missing_rows.append({"entry_id": entry_id, "class": cls})

    missing_pairs = sorted(
        expected_pairs - seen_pairs,
        key=lambda pair: (_entry_id_sort_key(pair[0]), pair[1]),
    )
    extra_pairs = sorted(
        seen_pairs - expected_pairs,
        key=lambda pair: (_entry_id_sort_key(pair[0]), pair[1]),
    )
    critical_counts = {
        "missing_record_key_rows": len(missing_key_rows),
        "duplicate_entry_class_pairs": len(duplicate_pairs),
        "missing_entry_class_pairs": len(missing_pairs),
        "extra_entry_class_pairs": len(extra_pairs),
        "score_range_violations": len(score_range_violations),
        "class_mismatches": len(class_mismatches),
        "split_mismatches": len(split_mismatches),
        "threshold_policy_violations": len(threshold_policy_violations),
        "fallback_source_rows": len(fallback_source_rows),
        "missing_source_paths": len(missing_source_paths),
        "provenance_missing_rows": len(provenance_missing_rows),
    }
    passed = all(count == 0 for count in critical_counts.values())
    return {
        "artifact_id": "v3_selected_organic_cofactor_sidecar_schema_audit_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": (
            "schema_passed_strict_current702" if passed else "schema_failed_strict_current702"
        ),
        "scope": (
            "Strict schema and lineage audit for the selected organic cofactor "
            "sidecar consumed by the D11 abstention gate and mechanism-feature "
            "embedding scaffold."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_threshold_tuning_for_deployment": False,
            "sidecar_values_changed": False,
        },
        "schema_contract": {
            "required_record_keys": list(REQUIRED_SELECTED_COFACTOR_RECORD_KEYS),
            "required_classes": list(COFACTOR_CLASSES),
            "entry_class_grid": "every current702 entry must have flavin, heme, and plp records",
            "score_range": "[0.0, 1.0]",
            "threshold_policy": "fixed_0_5_not_tuned_on_heldout",
            "fallback_sources_allowed": False,
        },
        "counts": {
            "manifest_rows": len(manifest_rows),
            "expected_entries": len(expected_entries),
            "row_class_records": len(records),
            "expected_row_class_records": len(expected_pairs),
            "class_counts": dict(sorted(Counter(str(r.get("class")) for r in records).items())),
            "split_counts": dict(
                sorted(Counter(str(r.get("split_assignment")) for r in records).items())
            ),
            "selected_source_counts": dict(
                sorted(Counter(str(r.get("selected_source")) for r in records).items())
            ),
            "critical_counts": critical_counts,
        },
        "violations": {
            "missing_record_key_rows": missing_key_rows[:50],
            "duplicate_entry_class_pairs": duplicate_pairs[:50],
            "missing_entry_class_pairs": [
                {"entry_id": entry_id, "class": cls} for entry_id, cls in missing_pairs[:50]
            ],
            "extra_entry_class_pairs": [
                {"entry_id": entry_id, "class": cls} for entry_id, cls in extra_pairs[:50]
            ],
            "score_range_violations": score_range_violations[:50],
            "class_mismatches": class_mismatches[:50],
            "split_mismatches": split_mismatches[:50],
            "threshold_policy_violations": threshold_policy_violations[:50],
            "fallback_source_rows": fallback_source_rows[:50],
            "missing_source_paths": missing_source_paths[:50],
            "provenance_missing_rows": provenance_missing_rows[:50],
        },
        "interpretation": {
            "result": (
                "The selected organic cofactor sidecar satisfies the strict "
                "current702 row-class grid and lineage contract."
                if passed
                else "One or more strict sidecar schema checks failed; treat the sidecar as blocked until repaired."
            ),
            "embedding_gap_relevance": (
                "This closes the organic flavin/heme/PLP sidecar schema risk for "
                "the mechanism-feature embedding scaffold, while metal, cobalamin, "
                "radical, and Fe-S row-level loci remain separate feature gaps."
            ),
        },
        "source_artifacts": {
            "selected_organic_cofactor_sidecar": {
                "path": str(selected_organic_cofactor_sidecar_path),
                "sha256": _sha256(selected_organic_cofactor_sidecar_path),
            },
            "label_manifest": {
                "path": str(label_manifest_path),
                "sha256": _sha256(label_manifest_path),
            },
        },
    }


def _render_selected_organic_cofactor_sidecar_schema_audit_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Selected Organic Cofactor Sidecar Schema Audit - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Row-class records: {counts['row_class_records']} / {counts['expected_row_class_records']}",
        f"- Critical violation counts: {counts['critical_counts']}",
        "",
        "## Contract",
        "",
        f"- Required classes: {', '.join(audit['schema_contract']['required_classes'])}",
        f"- Threshold policy: {audit['schema_contract']['threshold_policy']}",
        f"- Fallback sources allowed: {audit['schema_contract']['fallback_sources_allowed']}",
        "",
        "## Selected Sources",
        "",
    ]
    for source, count in counts["selected_source_counts"].items():
        lines.append(f"- {source}: {count}")
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['result']}",
        f"- {audit['interpretation']['embedding_gap_relevance']}",
    ]
    return "\n".join(lines) + "\n"


def write_selected_organic_cofactor_sidecar_schema_audit(
    *,
    selected_organic_cofactor_sidecar_path: Path,
    label_manifest_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_selected_organic_cofactor_sidecar_schema_audit(
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        label_manifest_path=label_manifest_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_selected_organic_cofactor_sidecar_schema_audit_report(audit),
            encoding="utf-8",
        )
    return audit


def _cofactor_scores_for_entry(sidecar: dict[str, Any], entry_id: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for record in sidecar.get("row_class_records", []):
        if record.get("entry_id") == entry_id and record.get("class"):
            scores[str(record["class"])] = float(record.get("selected_score") or 0.0)
    return scores


def build_family_panel_evidence_packet(
    *,
    family_targets_path: Path,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    predicted_atlas_variants_path: Path,
    predicted_structure_fold_channel_path: Path | None = None,
    panel_id: str = "glycyl_radical_or_thiamine_radical_lyase_boundary",
) -> dict[str, Any]:
    family_targets = _read_json(family_targets_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    fold_signal = _read_json(fold_level_signal_path)
    cofactor_sidecar = _read_json(selected_organic_cofactor_sidecar_path)
    variants = _read_json(predicted_atlas_variants_path)
    predicted_fold_channel = (
        _read_json(predicted_structure_fold_channel_path)
        if predicted_structure_fold_channel_path is not None
        and Path(predicted_structure_fold_channel_path).exists()
        else {}
    )

    panel = None
    for item in family_targets.get("candidate_families", []):
        if item.get("candidate_family") == panel_id:
            panel = item
            break
    if panel is None:
        return {
            "artifact_id": f"v3_family_panel_evidence_packet_{panel_id}_current702_20260601",
            "schema_version": SCHEMA_VERSION,
            "created_utc": _utc_now_iso(),
            "status": "panel_not_found",
            "panel_id": panel_id,
        }

    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in predicted_atlas.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    fold_by_entry = {
        str(row.get("entry_id")): row
        for row in fold_signal.get("confounded_row_details", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    variant_by_entry = {
        str(row.get("entry_id")): row
        for row in variants.get("row_scores", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    predicted_fold_hits = {
        str(row.get("query_entry_id")): row
        for row in (
            predicted_fold_channel.get("parsed_foldseek_results", {})
            .get("priority_cofactor_confounded_oos_vs_atlas", {})
            .get("nearest_atlas_hits", [])
        )
        if isinstance(row, dict) and row.get("query_entry_id")
    }
    rows = []
    for entry_id in panel.get("candidate_rows", []):
        geo = geometry_by_entry.get(entry_id, {})
        top = _top1_fingerprint(geo) or {}
        fold = fold_by_entry.get(entry_id, {})
        cof = _cofactor_scores_for_entry(cofactor_sidecar, entry_id)
        variant = variant_by_entry.get(entry_id, {})
        variant_scores = variant.get("variant_scores", {})
        cofactor_max = max(cof.values()) if cof else None
        rows.append(
            {
                "entry_id": entry_id,
                "split_assignment": geo.get("split_assignment"),
                "benchmark_role": geo.get("benchmark_role"),
                "predicted_geometry_status": _predicted_row_status(geo) if geo else "missing",
                "predicted_geometry_top1": {
                    "fingerprint_id": top.get("fingerprint_id"),
                    "score": top.get("score"),
                    "role_match_fraction": top.get("role_match_fraction"),
                    "cofactor_context_score": top.get("cofactor_context_score"),
                },
                "selected_organic_cofactor_scores": cof,
                "selected_organic_cofactor_max": (
                    round(cofactor_max, 6) if cofactor_max is not None else None
                ),
                "selected_pdb_fold_proxy": {
                    "nearest_primary_foldseek_prob": (
                        (fold.get("fold_signals") or {}).get("nearest_primary_foldseek_prob")
                    ),
                    "top3_primary_foldseek_prob": (
                        (fold.get("fold_signals") or {}).get("top3_primary_foldseek_prob")
                    ),
                    "nearest_train_label_group": fold.get("nearest_train_label_group"),
                    "nearest_train_fingerprint_id": fold.get("nearest_train_fingerprint_id"),
                },
                "predicted_atlas_geometry_variant_scores": {
                    "top1_score_raw": variant_scores.get("top1_score_raw"),
                    "negative_nearest_class_centroid_robust_distance": variant_scores.get(
                        "negative_nearest_class_centroid_robust_distance"
                    ),
                },
                "predicted_structure_fold_channel": {
                    "nearest_atlas_entry_id": (
                        predicted_fold_hits.get(entry_id, {}).get("nearest_atlas_entry_id")
                    ),
                    "nearest_atlas_true_fingerprint_id": (
                        predicted_fold_hits.get(entry_id, {}).get(
                            "nearest_atlas_true_fingerprint_id"
                        )
                    ),
                    "nearest_atlas_tm_score": (
                        predicted_fold_hits.get(entry_id, {}).get("tm_score")
                    ),
                },
                "evidence_role": (
                    "cofactor-confounded OOS control: known organic cofactor-like "
                    "signal with weak/novel fold or geometry support against occupied "
                    "primary mechanisms"
                ),
            }
        )

    missing_geometry = [
        row["entry_id"] for row in rows if row["predicted_geometry_status"] != "ok"
    ]
    artifact_slug = (
        "glycyl_radical_or_thiamine_radical_lyase"
        if panel_id == "glycyl_radical_or_thiamine_radical_lyase_boundary"
        else _safe_path_token(panel_id)
    )
    return {
        "artifact_id": f"v3_family_panel_evidence_packet_{artifact_slug}_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": (
            "evidence_packet_ready_review_only"
            if not missing_geometry else "evidence_packet_ready_with_geometry_gaps"
        ),
        "scope": (
            "Review-only evidence packet for the highest-value family-set expansion "
            f"panel `{panel_id}`: cofactor-confounded OOS boundary rows "
            "that stress the current de novo abstention gate."
        ),
        "guardrails": {
            "proposal_only": True,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_splits_changed": False,
            "heldout_rows_used_for_training": False,
        },
        "panel": panel,
        "counts": {
            "candidate_rows": len(rows),
            "predicted_geometry_ok_rows": sum(
                1 for row in rows if row["predicted_geometry_status"] == "ok"
            ),
            "rows_with_selected_pdb_fold_proxy": sum(
                1
                for row in rows
                if row["selected_pdb_fold_proxy"]["nearest_primary_foldseek_prob"] is not None
            ),
            "rows_with_selected_organic_cofactor_scores": sum(
                1 for row in rows if row["selected_organic_cofactor_scores"]
            ),
            "rows_with_predicted_structure_fold_hits": sum(
                1
                for row in rows
                if row["predicted_structure_fold_channel"]["nearest_atlas_tm_score"]
                is not None
            ),
            "missing_geometry_entry_ids": missing_geometry,
        },
        "row_evidence": rows,
        "review_questions": [
            f"Do these rows share a coherent `{panel_id}` mechanism locus, or should they stay OOS controls?",
            "Which row-level bond-change and cofactor-locus features must be normalized before any countable family addition?",
            "Does the real predicted-structure Foldseek/TM channel keep these rows outside occupied primary atlas folds?",
        ],
        "next_actions": (
            [
                "use the completed all-heldout predicted Foldseek/TM signal in the next abstention combiner diagnostic",
                "source-check mechanism locus and bond-change evidence before any panel promotion discussion",
                "keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized",
            ]
            if predicted_fold_channel.get("status") == "computed_all_heldout_foldseek_scores"
            else (
            [
                "extend the predicted-structure Foldseek/TM sweep from this two-row panel to all priority confounded rows or all heldout rows",
                "source-check mechanism locus and bond-change evidence before any panel promotion discussion",
                "keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized",
            ]
            if predicted_fold_hits
            else [
                "run the predicted-structure Foldseek/TM priority manifest for these rows against the predicted atlas",
                "source-check mechanism locus and bond-change evidence before any panel promotion discussion",
                "keep rows review-only and out of training/calibration until a future frozen split is explicitly authorized",
            ]
            )
        ),
        "source_artifacts": {
            "family_targets": {
                "path": str(family_targets_path),
                "sha256": _sha256(family_targets_path),
            },
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "fold_level_signal": {
                "path": str(fold_level_signal_path),
                "sha256": _sha256(fold_level_signal_path),
            },
            "selected_organic_cofactor_sidecar": {
                "path": str(selected_organic_cofactor_sidecar_path),
                "sha256": _sha256(selected_organic_cofactor_sidecar_path),
            },
            "predicted_atlas_variants": {
                "path": str(predicted_atlas_variants_path),
                "sha256": _sha256(predicted_atlas_variants_path),
            },
            "predicted_structure_fold_channel": (
                {
                    "path": str(predicted_structure_fold_channel_path),
                    "sha256": _sha256(predicted_structure_fold_channel_path),
                }
                if predicted_structure_fold_channel_path is not None
                and Path(predicted_structure_fold_channel_path).exists()
                else None
            ),
        },
    }


def _render_family_panel_evidence_packet_report(audit: dict[str, Any]) -> str:
    panel_id = (audit.get("panel") or {}).get("candidate_family") or "family_panel"
    lines = [
        f"# Family Panel Evidence Packet - {panel_id}",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Candidate rows: {audit['counts']['candidate_rows']}",
        f"- Predicted geometry ok rows: {audit['counts']['predicted_geometry_ok_rows']}",
        "",
        "## Row Evidence",
        "",
        "| Row | geometry top1 | geom score | cofactor max | selected-PDB fold prob | predicted-fold TM | robust atlas distance signal |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in audit["row_evidence"]:
        lines.append(
            f"| {row['entry_id']} | {row['predicted_geometry_top1']['fingerprint_id']} | "
            f"{row['predicted_geometry_top1']['score']} | "
            f"{row['selected_organic_cofactor_max']} | "
            f"{row['selected_pdb_fold_proxy']['nearest_primary_foldseek_prob']} | "
            f"{row['predicted_structure_fold_channel']['nearest_atlas_tm_score']} | "
            f"{row['predicted_atlas_geometry_variant_scores']['negative_nearest_class_centroid_robust_distance']} |"
        )
    lines += [
        "",
        "## Review Questions",
        "",
    ]
    for item in audit["review_questions"]:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Next Actions",
        "",
    ]
    for item in audit["next_actions"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_family_panel_evidence_packet(
    *,
    family_targets_path: Path,
    predicted_geometry_atlas_path: Path,
    fold_level_signal_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    predicted_atlas_variants_path: Path,
    out_path: Path,
    predicted_structure_fold_channel_path: Path | None = None,
    report_path: Path | None = None,
    panel_id: str = "glycyl_radical_or_thiamine_radical_lyase_boundary",
) -> dict[str, Any]:
    audit = build_family_panel_evidence_packet(
        family_targets_path=family_targets_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        fold_level_signal_path=fold_level_signal_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        predicted_atlas_variants_path=predicted_atlas_variants_path,
        predicted_structure_fold_channel_path=predicted_structure_fold_channel_path,
        panel_id=panel_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_family_panel_evidence_packet_report(audit),
            encoding="utf-8",
        )
    return audit


def build_fold_augmented_abstention_gate(
    *,
    predicted_structure_fold_channel_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
) -> dict[str, Any]:
    fold_channel = _read_json(predicted_structure_fold_channel_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    cofactor_sidecar = _read_json(selected_organic_cofactor_sidecar_path)
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in predicted_atlas.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    fold_rows = (
        fold_channel.get("fold_channel_signal", {})
        .get("nearest_atlas_tm_score", {})
        .get("row_scores", [])
    )
    scored_rows = []
    for row in fold_rows:
        entry_id = str(row.get("entry_id"))
        geo = geometry_by_entry.get(entry_id, {})
        top = _top1_fingerprint(geo) or {}
        cofactor_scores = _cofactor_scores_for_entry(cofactor_sidecar, entry_id)
        if not top or not cofactor_scores:
            continue
        geom = float(top.get("score") or 0.0)
        cof = max(cofactor_scores.values())
        fold = float((row.get("fold_signals") or {}).get("nearest_atlas_tm_score") or 0.0)
        scored_rows.append(
            {
                "entry_id": entry_id,
                "true_fingerprint_id": row.get("true_fingerprint_id"),
                "is_inscope": bool(row.get("true_fingerprint_id")),
                "is_oos": not bool(row.get("true_fingerprint_id")),
                "is_confounded_predicted_geometry_oos": bool(
                    row.get("is_confounded_predicted_geometry_oos")
                ),
                "channel_scores": {
                    "geometry_top1_score": round(geom, 6),
                    "cofactor_max_score": round(cof, 6),
                    "fold_nearest_atlas_tm_score": round(fold, 6),
                    "combined_mean_geometry_cofactor_fold": round((geom + cof + fold) / 3, 6),
                    "combined_mean_geometry_fold": round((geom + fold) / 2, 6),
                    "combined_min_geometry_fold": round(min(geom, fold), 6),
                },
            }
        )
    if not scored_rows:
        return {
            "artifact_id": "v3_fold_augmented_abstention_gate_current702_20260601",
            "schema_version": SCHEMA_VERSION,
            "created_utc": _utc_now_iso(),
            "status": "insufficient_rows",
        }
    channel_names = list(scored_rows[0]["channel_scores"])
    channels = {
        name: _signal_metrics(
            [
                {
                    **row,
                    "variant_scores": row["channel_scores"],
                }
                for row in scored_rows
            ],
            name,
        )
        for name in channel_names
    }
    best_name, best = max(
        channels.items(),
        key=lambda item: item[1]["auc_in_gt_oos_all"] or 0.0,
    )
    return {
        "artifact_id": "v3_fold_augmented_abstention_gate_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "computed_no_fit_no_threshold_change",
        "scope": (
            "Fold-augmented deployment abstention diagnostic over heldout rows "
            "with ok predicted geometry: raw predicted-geometry top1 confidence, "
            "sequence-only selected organic cofactor max score, and real "
            "predicted-structure nearest-atlas Foldseek/TM score."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_threshold_tuning_for_deployment": False,
            "model_fit_or_refit": False,
        },
        "counts": {
            "heldout_rows_scored": len(scored_rows),
            "inscope": sum(1 for row in scored_rows if row["is_inscope"]),
            "oos": sum(1 for row in scored_rows if row["is_oos"]),
            "confounded_oos": sum(
                1 for row in scored_rows if row["is_confounded_predicted_geometry_oos"]
            ),
        },
        "channels": channels,
        "best_channel": {
            "name": best_name,
            "auc_in_gt_oos_all": best["auc_in_gt_oos_all"],
            "auc_in_gt_confounded_oos": best["auc_in_gt_confounded_oos"],
            "best_at_90pct_inscope_retention": best["best_at_90pct_inscope_retention"],
            "best_at_85pct_inscope_retention": best["best_at_85pct_inscope_retention"],
        },
        "row_scores": scored_rows,
        "interpretation": {
            "headline": (
                f"Best fold-augmented diagnostic channel is {best_name} with "
                f"AUC {best['auc_in_gt_oos_all']} overall."
            ),
            "caveat": (
                "This is a no-fit diagnostic over heldout rows, not a selected "
                "deployment threshold or production scoring change."
            ),
        },
        "source_artifacts": {
            "predicted_structure_fold_channel": {
                "path": str(predicted_structure_fold_channel_path),
                "sha256": _sha256(predicted_structure_fold_channel_path),
            },
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "selected_organic_cofactor_sidecar": {
                "path": str(selected_organic_cofactor_sidecar_path),
                "sha256": _sha256(selected_organic_cofactor_sidecar_path),
            },
        },
    }


def _render_fold_augmented_abstention_gate_report(audit: dict[str, Any]) -> str:
    best = audit["best_channel"]
    counts = audit["counts"]
    lines = [
        "# Fold-Augmented Abstention Gate - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Counts",
        "",
        f"- Heldout rows scored: {counts['heldout_rows_scored']}",
        f"- In-scope: {counts['inscope']}",
        f"- OOS: {counts['oos']}",
        f"- Cofactor-confounded OOS: {counts['confounded_oos']}",
        "",
        "## Best Channel",
        "",
        f"- {best['name']}: AUC all OOS {best['auc_in_gt_oos_all']}; confounded AUC {best['auc_in_gt_confounded_oos']}",
        f"- Best >=90% retention diagnostic: {best['best_at_90pct_inscope_retention']}",
        f"- Best >=85% retention diagnostic: {best['best_at_85pct_inscope_retention']}",
        "",
        "## Channels",
        "",
        "| Channel | all OOS AUC | confounded AUC | agnostic AUC |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, channel in audit["channels"].items():
        lines.append(
            f"| {name} | {channel['auc_in_gt_oos_all']} | "
            f"{channel['auc_in_gt_confounded_oos']} | {channel['auc_in_gt_agnostic_oos']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['caveat']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_augmented_abstention_gate(
    *,
    predicted_structure_fold_channel_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_fold_augmented_abstention_gate(
        predicted_structure_fold_channel_path=predicted_structure_fold_channel_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_fold_augmented_abstention_gate_report(audit), encoding="utf-8")
    return audit


def _stable_hash_int(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)


def _partition_train_calibration_rows(
    rows: list[dict[str, Any]],
    *,
    calibration_fraction: float = 0.2,
) -> dict[str, str]:
    """Deterministic in-distribution partition for threshold selection."""
    by_fp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        fp = str(row.get("true_fingerprint_id") or "")
        if fp:
            by_fp[fp].append(row)
    partition: dict[str, str] = {}
    for fp, members in by_fp.items():
        ordered = sorted(
            members,
            key=lambda row: (
                _stable_hash_int(f"{fp}::{row.get('entry_id')}"),
                str(row.get("entry_id")),
            ),
        )
        if len(ordered) < 2:
            partition[str(ordered[0].get("entry_id"))] = "train"
            continue
        cal_count = max(1, min(len(ordered) - 1, round(len(ordered) * calibration_fraction)))
        cal_ids = {str(row.get("entry_id")) for row in ordered[:cal_count]}
        for row in ordered:
            entry_id = str(row.get("entry_id"))
            partition[entry_id] = "calibration" if entry_id in cal_ids else "train"
    return partition


def _score_threshold_for_min_retain(
    rows: list[dict[str, Any]],
    score_name: str,
    *,
    min_retain: float,
) -> dict[str, Any] | None:
    if not rows:
        return None
    candidates = sorted({float(row["channel_scores"][score_name]) for row in rows})
    best = None
    for threshold in candidates:
        retained = sum(
            1 for row in rows if float(row["channel_scores"][score_name]) >= threshold
        )
        retain = retained / len(rows)
        if retain >= min_retain:
            candidate = {
                "threshold": round(threshold, 6),
                "min_retain_target": min_retain,
                "calibration_in_scope_retain_recall": round(retain, 4),
                "calibration_in_scope_retained": retained,
                "calibration_in_scope_total": len(rows),
            }
            if best is None or candidate["threshold"] > best["threshold"]:
                best = candidate
    return best


def _evaluate_threshold_on_heldout(
    rows: list[dict[str, Any]],
    score_name: str,
    threshold: float,
) -> dict[str, Any]:
    inscope = [row for row in rows if row["is_inscope"]]
    oos = [row for row in rows if row["is_oos"]]
    conf = [row for row in rows if row["is_confounded_predicted_geometry_oos"]]

    def keep(row: dict[str, Any]) -> bool:
        return float(row["channel_scores"][score_name]) >= threshold

    inscope_kept = sum(1 for row in inscope if keep(row))
    oos_abstained = sum(1 for row in oos if not keep(row))
    conf_abstained = sum(1 for row in conf if not keep(row))
    return {
        "threshold": round(float(threshold), 6),
        "heldout_in_scope_retained": inscope_kept,
        "heldout_in_scope_total": len(inscope),
        "heldout_in_scope_retain_recall": (
            round(inscope_kept / len(inscope), 4) if inscope else None
        ),
        "heldout_oos_abstained": oos_abstained,
        "heldout_oos_total": len(oos),
        "heldout_oos_abstain_recall": (
            round(oos_abstained / len(oos), 4) if oos else None
        ),
        "heldout_confounded_oos_abstained": conf_abstained,
        "heldout_confounded_oos_total": len(conf),
        "heldout_confounded_oos_abstain_recall": (
            round(conf_abstained / len(conf), 4) if conf else None
        ),
    }


def _parse_train_calibration_foldseek_tsv(
    *,
    result_tsv: Path,
    query_requests: list[dict[str, Any]],
    target_requests: list[dict[str, Any]],
    train_entry_ids: set[str],
    calibration_entry_ids: set[str],
) -> dict[str, Any]:
    if not result_tsv.exists():
        return {
            "status": "result_tsv_missing",
            "path": str(result_tsv),
            "nearest_train_atlas_hits": [],
            "summary": {
                "mapped_pair_count": 0,
                "unmapped_pair_count": 0,
                "calibration_entry_count_with_hits": 0,
            },
        }
    query_aliases, query_collisions = _alias_map(query_requests)
    target_aliases, target_collisions = _alias_map(target_requests)
    nearest: dict[str, dict[str, Any]] = {}
    mapped_pair_count = 0
    skipped_non_contract_pair_count = 0
    unmapped_pair_count = 0
    unmapped_names: set[str] = set()
    for line in result_tsv.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if parts[0] == "query":
            continue
        if len(parts) < 5:
            unmapped_pair_count += 1
            continue
        raw_query, raw_target = parts[0], parts[1]
        query_request = query_aliases.get(raw_query)
        target_request = target_aliases.get(raw_target)
        if query_request is None or target_request is None:
            unmapped_pair_count += 1
            if query_request is None:
                unmapped_names.add(raw_query)
            if target_request is None:
                unmapped_names.add(raw_target)
            continue
        qtmscore = _parse_optional_float(parts[2])
        ttmscore = _parse_optional_float(parts[3])
        alntmscore = _parse_optional_float(parts[4])
        scores = [score for score in (qtmscore, ttmscore, alntmscore) if score is not None]
        if not scores:
            unmapped_pair_count += 1
            continue
        tm_score = max(scores)
        prob = _parse_optional_float(parts[5]) if len(parts) > 5 else None
        bits = _parse_optional_float(parts[6]) if len(parts) > 6 else None
        for query_row in query_request.get("rows") or []:
            query_entry_id = str(query_row.get("entry_id"))
            if query_entry_id not in calibration_entry_ids:
                skipped_non_contract_pair_count += 1
                continue
            for target_row in target_request.get("rows") or []:
                target_entry_id = str(target_row.get("entry_id"))
                if target_entry_id not in train_entry_ids:
                    skipped_non_contract_pair_count += 1
                    continue
                if target_entry_id == query_entry_id:
                    skipped_non_contract_pair_count += 1
                    continue
                if (
                    query_request.get("accession")
                    and query_request.get("accession") == target_request.get("accession")
                ):
                    skipped_non_contract_pair_count += 1
                    continue
                mapped_pair_count += 1
                candidate = {
                    "query_entry_id": query_entry_id,
                    "query_accession": query_request.get("accession"),
                    "raw_query_name": raw_query,
                    "nearest_train_atlas_entry_id": target_entry_id,
                    "nearest_train_atlas_accession": target_request.get("accession"),
                    "nearest_train_atlas_true_fingerprint_id": target_row.get(
                        "true_fingerprint_id"
                    ),
                    "raw_target_name": raw_target,
                    "tm_score": round(tm_score, 6),
                    "qtmscore": qtmscore,
                    "ttmscore": ttmscore,
                    "alntmscore": alntmscore,
                    "prob": prob,
                    "bits": bits,
                }
                previous = nearest.get(query_entry_id)
                if previous is None or candidate["tm_score"] > previous["tm_score"]:
                    nearest[query_entry_id] = candidate
    hits = sorted(nearest.values(), key=lambda row: _entry_id_sort_key(row["query_entry_id"]))
    return {
        "status": "parsed" if hits else "parsed_no_mapped_hits",
        "path": str(result_tsv),
        "nearest_train_atlas_hits": hits,
        "summary": {
            "mapped_pair_count": mapped_pair_count,
            "skipped_non_contract_pair_count": skipped_non_contract_pair_count,
            "unmapped_pair_count": unmapped_pair_count,
            "calibration_entry_count_with_hits": len(hits),
            "alias_collision_count": len(query_collisions) + len(target_collisions),
            "alias_collisions": query_collisions + target_collisions,
            "unmapped_names": sorted(unmapped_names),
        },
    }


def _fold_augmented_channel_scores(
    *,
    geometry_score: float,
    cofactor_max_score: float,
    fold_tm_score: float,
) -> dict[str, float]:
    return {
        "geometry_top1_score": round(geometry_score, 6),
        "cofactor_max_score": round(cofactor_max_score, 6),
        "fold_nearest_atlas_tm_score": round(fold_tm_score, 6),
        "combined_mean_geometry_cofactor_fold": round(
            (geometry_score + cofactor_max_score + fold_tm_score) / 3,
            6,
        ),
        "combined_mean_geometry_fold": round((geometry_score + fold_tm_score) / 2, 6),
        "combined_min_geometry_fold": round(min(geometry_score, fold_tm_score), 6),
    }


def _calibration_foldseek_command(
    *,
    foldseek_binary: str,
    result_tsv: Path,
    threads: int,
) -> str:
    root = Path("/private/tmp/catalytic_threshold_train_cal_foldseek")
    result_root = result_tsv.parent
    return _foldseek_easy_search_command(
        binary=foldseek_binary,
        query_dir=root / "calibration_queries",
        target_dir=root / "train_targets",
        result_tsv=result_tsv,
        tmp_dir=result_root / "tmp_in_distribution_atlas_self_vs_atlas",
        threads=threads,
    )


def _atlas_coordinate_materialization_command() -> str:
    return (
        "python - <<'PY'\n"
        "import json\n"
        "import urllib.request\n"
        "from pathlib import Path\n"
        f"artifact = json.loads(Path('artifacts/{PREDICTED_STRUCTURE_FOLD_CHANNEL_ID}.json').read_text())\n"
        "atlas = artifact['foldseek_input_manifest']['coordinate_request_groups']['atlas_in_distribution']\n"
        "for item in atlas:\n"
        "    path = item.get('expected_local_path')\n"
        "    url = item.get('url')\n"
        "    if not path or not url:\n"
        "        continue\n"
        "    target = Path(path)\n"
        "    target.parent.mkdir(parents=True, exist_ok=True)\n"
        "    if target.exists():\n"
        "        continue\n"
        "    urllib.request.urlretrieve(url, target)\n"
        "PY"
    )


def _stage_train_calibration_dirs_command() -> str:
    return (
        "python - <<'PY'\n"
        "import json\n"
        "import shutil\n"
        "from pathlib import Path\n"
        f"contract = json.loads(Path('artifacts/{FOLD_AUGMENTED_THRESHOLD_CONTRACT_ID}.json').read_text())\n"
        f"fold = json.loads(Path('artifacts/{PREDICTED_STRUCTURE_FOLD_CHANNEL_ID}.json').read_text())\n"
        "root = Path('/private/tmp/catalytic_threshold_train_cal_foldseek')\n"
        "if root.exists():\n"
        "    shutil.rmtree(root)\n"
        "query_dir = root / 'calibration_queries'\n"
        "target_dir = root / 'train_targets'\n"
        "query_dir.mkdir(parents=True)\n"
        "target_dir.mkdir(parents=True)\n"
        "cal = set(contract['train_cal_partition']['calibration_entry_ids'])\n"
        "train = set(contract['train_cal_partition']['train_entry_ids'])\n"
        "atlas = fold['foldseek_input_manifest']['coordinate_request_groups']['atlas_in_distribution']\n"
        "for item in atlas:\n"
        "    src = Path(item['expected_local_path'])\n"
        "    if not src.exists():\n"
        "        continue\n"
        "    ids = set(item.get('entry_ids') or [])\n"
        "    if ids & cal:\n"
        "        dst = query_dir / src.name\n"
        "        if not dst.exists():\n"
        "            dst.symlink_to(src.resolve())\n"
        "    if ids & train:\n"
        "        dst = target_dir / src.name\n"
        "        if not dst.exists():\n"
        "            dst.symlink_to(src.resolve())\n"
        "print({'queries': len(list(query_dir.iterdir())), 'targets': len(list(target_dir.iterdir()))})\n"
        "PY"
    )


def build_fold_augmented_abstention_threshold_contract(
    *,
    fold_augmented_gate_path: Path,
    predicted_structure_fold_channel_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    train_cal_foldseek_tsv: Path,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    threads: int = 4,
) -> dict[str, Any]:
    fold_gate = _read_json(fold_augmented_gate_path)
    fold_channel = _read_json(predicted_structure_fold_channel_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    cofactor_sidecar = _read_json(selected_organic_cofactor_sidecar_path)

    atlas_rows = [
        row
        for row in predicted_atlas.get("results", [])
        if (
            isinstance(row, dict)
            and row.get("split_assignment") == "in_distribution"
            and row.get("true_fingerprint_id")
            and _predicted_row_ok(row)
            and _top1_fingerprint(row)
        )
    ]
    partition = _partition_train_calibration_rows(atlas_rows)
    train_entry_ids = {
        entry_id for entry_id, split in partition.items() if split == "train"
    }
    calibration_entry_ids = {
        entry_id for entry_id, split in partition.items() if split == "calibration"
    }
    coordinate_root = Path(
        str(
            (fold_channel.get("foldseek_input_manifest") or {}).get("coordinate_root")
            or "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates"
        )
    )
    atlas_requests = _coordinate_requests(
        atlas_rows,
        coordinate_root=coordinate_root,
        role="in_distribution_train_cal_query_or_target",
        subdir="atlas_in_distribution",
    )
    parsed_train_cal = _parse_train_calibration_foldseek_tsv(
        result_tsv=train_cal_foldseek_tsv,
        query_requests=atlas_requests,
        target_requests=atlas_requests,
        train_entry_ids=train_entry_ids,
        calibration_entry_ids=calibration_entry_ids,
    )
    geometry_by_entry = {str(row.get("entry_id")): row for row in atlas_rows}
    fold_by_entry = {
        str(row.get("query_entry_id")): row
        for row in parsed_train_cal.get("nearest_train_atlas_hits", [])
    }
    calibration_rows = []
    for entry_id in sorted(calibration_entry_ids, key=_entry_id_sort_key):
        geo = geometry_by_entry.get(entry_id, {})
        fold_hit = fold_by_entry.get(entry_id)
        cofactor_scores = _cofactor_scores_for_entry(cofactor_sidecar, entry_id)
        top = _top1_fingerprint(geo) or {}
        if not fold_hit or not top or not cofactor_scores:
            continue
        geom = float(top.get("score") or 0.0)
        cof = max(cofactor_scores.values())
        fold = float(fold_hit.get("tm_score") or 0.0)
        calibration_rows.append(
            {
                "entry_id": entry_id,
                "true_fingerprint_id": geo.get("true_fingerprint_id"),
                "partition": "calibration",
                "nearest_train_atlas_entry_id": fold_hit.get("nearest_train_atlas_entry_id"),
                "nearest_train_atlas_true_fingerprint_id": fold_hit.get(
                    "nearest_train_atlas_true_fingerprint_id"
                ),
                "channel_scores": _fold_augmented_channel_scores(
                    geometry_score=geom,
                    cofactor_max_score=cof,
                    fold_tm_score=fold,
                ),
            }
        )
    heldout_rows = [
        row
        for row in fold_gate.get("row_scores", [])
        if isinstance(row, dict) and row.get("channel_scores")
    ]
    channel_names = list(heldout_rows[0]["channel_scores"]) if heldout_rows else [
        "geometry_top1_score",
        "cofactor_max_score",
        "fold_nearest_atlas_tm_score",
        "combined_mean_geometry_cofactor_fold",
        "combined_mean_geometry_fold",
        "combined_min_geometry_fold",
    ]
    threshold_contract: dict[str, Any] = {}
    for channel_name in channel_names:
        at90 = _score_threshold_for_min_retain(
            calibration_rows,
            channel_name,
            min_retain=0.90,
        )
        at85 = _score_threshold_for_min_retain(
            calibration_rows,
            channel_name,
            min_retain=0.85,
        )
        threshold_contract[channel_name] = {
            "selected_at_90pct_calibration_in_scope_retention": at90,
            "selected_at_85pct_calibration_in_scope_retention": at85,
            "heldout_final_eval_at_90pct_threshold": (
                _evaluate_threshold_on_heldout(
                    heldout_rows,
                    channel_name,
                    float(at90["threshold"]),
                )
                if at90
                else None
            ),
            "heldout_final_eval_at_85pct_threshold": (
                _evaluate_threshold_on_heldout(
                    heldout_rows,
                    channel_name,
                    float(at85["threshold"]),
                )
                if at85
                else None
            ),
        }
    blockers: list[str] = []
    if parsed_train_cal["status"] != "parsed":
        blockers.append("train_cal_foldseek_tsv_missing_or_unparsed")
    if calibration_entry_ids and len(calibration_rows) < len(calibration_entry_ids):
        blockers.append("some_calibration_rows_missing_fold_geometry_or_cofactor_scores")
    if not calibration_rows:
        blockers.append("no_calibration_rows_scored")
    status = (
        "computed_train_cal_threshold_contract"
        if not blockers
        else "blocked_missing_train_cal_fold_scores"
    )
    primary = threshold_contract.get("combined_mean_geometry_fold", {})
    return {
        "artifact_id": FOLD_AUGMENTED_THRESHOLD_CONTRACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Leakage-safe thresholding contract for the fold-augmented abstention "
            "diagnostic. Thresholds are selected on deterministic in-distribution "
            "calibration rows only; heldout rows are final evaluation diagnostics."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "thresholds_selected_on_heldout": False,
            "heldout_used_for_final_eval_only": True,
            "train_cal_oos_negatives_used_for_threshold": False,
            "frozen_current702_inputs_only": True,
        },
        "selection_policy": {
            "partition_source": "deterministic_hash_stratified_by_true_fingerprint_over_in_distribution_predicted_atlas_rows",
            "train_rows_are_foldseek_targets": True,
            "calibration_rows_select_thresholds": True,
            "calibration_objective": "highest_score_threshold_retaining_at_least_target_fraction_of_in_scope_calibration_rows",
            "target_retention_levels": [0.90, 0.85],
            "weights_policy": "no_weights_fit_prespecified_channels_only",
            "heldout_policy": "heldout rows are evaluated after threshold selection and do not affect thresholds",
            "limitation": (
                "The current predicted-geometry atlas contains in-distribution "
                "fingerprint rows, not train/cal OOS negatives. Thresholds therefore "
                "control in-scope retention only; OOS abstain recall remains a final "
                "heldout diagnostic."
            ),
        },
        "counts": {
            "atlas_in_distribution_rows_ok_with_fingerprint": len(atlas_rows),
            "train_rows": len(train_entry_ids),
            "calibration_rows_expected": len(calibration_entry_ids),
            "calibration_rows_scored": len(calibration_rows),
            "heldout_rows_final_eval": len(heldout_rows),
            "heldout_in_scope": sum(1 for row in heldout_rows if row.get("is_inscope")),
            "heldout_oos": sum(1 for row in heldout_rows if row.get("is_oos")),
            "heldout_confounded_oos": sum(
                1 for row in heldout_rows if row.get("is_confounded_predicted_geometry_oos")
            ),
        },
        "blockers": blockers,
        "train_cal_partition": {
            "train_entry_ids": sorted(train_entry_ids, key=_entry_id_sort_key),
            "calibration_entry_ids": sorted(calibration_entry_ids, key=_entry_id_sort_key),
            "fingerprint_counts": dict(
                sorted(
                    Counter(str(row.get("true_fingerprint_id")) for row in atlas_rows).items()
                )
            ),
        },
        "parsed_train_cal_foldseek": parsed_train_cal,
        "threshold_contract": threshold_contract,
        "primary_channel_readout": {
            "channel": "combined_mean_geometry_fold",
            "selected_at_90pct_calibration_in_scope_retention": primary.get(
                "selected_at_90pct_calibration_in_scope_retention"
            ),
            "heldout_final_eval_at_90pct_threshold": primary.get(
                "heldout_final_eval_at_90pct_threshold"
            ),
        },
        "calibration_row_scores": calibration_rows,
        "commands": {
            "materialize_atlas_coordinate_bundle": _atlas_coordinate_materialization_command(),
            "stage_train_calibration_foldseek_dirs": (
                _stage_train_calibration_dirs_command()
            ),
            "run_in_distribution_atlas_self_vs_atlas": _calibration_foldseek_command(
                foldseek_binary=str(
                    _foldseek_binary_info(foldseek_binary).get("resolved")
                    or foldseek_binary
                ),
                result_tsv=train_cal_foldseek_tsv,
                threads=threads,
            ),
            "rerun_contract_parser": (
                "PYTHONPATH=src python -m catalytic_earth.cli "
                "eval-fold-augmented-abstention-threshold-contract "
                f"--train-cal-foldseek-tsv {shlex.quote(str(train_cal_foldseek_tsv))}"
            ),
            "foldseek_tsv_columns": [
                "query",
                "target",
                "qtmscore",
                "ttmscore",
                "alntmscore",
                "prob",
                "bits",
            ],
        },
        "interpretation": {
            "headline": (
                "Train/cal thresholds were selected without heldout threshold tuning."
                if not blockers
                else "Train/cal threshold selection is blocked until the in-distribution Foldseek TSV is available."
            ),
            "production_status": (
                "research_contract_not_production_threshold; no production scorer or global threshold was changed"
            ),
        },
        "source_artifacts": {
            "fold_augmented_gate": {
                "path": str(fold_augmented_gate_path),
                "sha256": _sha256(fold_augmented_gate_path),
            },
            "predicted_structure_fold_channel": {
                "path": str(predicted_structure_fold_channel_path),
                "sha256": _sha256(predicted_structure_fold_channel_path),
            },
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "selected_organic_cofactor_sidecar": {
                "path": str(selected_organic_cofactor_sidecar_path),
                "sha256": _sha256(selected_organic_cofactor_sidecar_path),
            },
        },
    }


def _render_fold_augmented_abstention_threshold_contract_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    primary = audit["primary_channel_readout"]
    lines = [
        "# Fold-Augmented Abstention Threshold Contract - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Blockers: {audit['blockers']}",
        f"- Train rows: {counts['train_rows']}",
        f"- Calibration rows scored: {counts['calibration_rows_scored']} / {counts['calibration_rows_expected']}",
        f"- Heldout final-eval rows: {counts['heldout_rows_final_eval']}",
        "",
        "## Primary Channel",
        "",
        f"- Channel: {primary['channel']}",
        f"- Calibration-selected 90% threshold: {primary['selected_at_90pct_calibration_in_scope_retention']}",
        f"- Heldout final eval at that threshold: {primary['heldout_final_eval_at_90pct_threshold']}",
        "",
        "## Thresholds",
        "",
        "| Channel | cal >=90 threshold | heldout in-scope retain | heldout OOS abstain | heldout confounded abstain |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, row in audit["threshold_contract"].items():
        selected = row.get("selected_at_90pct_calibration_in_scope_retention") or {}
        heldout = row.get("heldout_final_eval_at_90pct_threshold") or {}
        lines.append(
            f"| {name} | {selected.get('threshold')} | "
            f"{heldout.get('heldout_in_scope_retain_recall')} | "
            f"{heldout.get('heldout_oos_abstain_recall')} | "
            f"{heldout.get('heldout_confounded_oos_abstain_recall')} |"
        )
    lines += [
        "",
        "## Contract",
        "",
        f"- {audit['selection_policy']['calibration_objective']}",
        f"- {audit['selection_policy']['limitation']}",
        f"- {audit['interpretation']['production_status']}",
        "",
        "## Commands",
        "",
        "Materialize the atlas coordinate bundle:",
        "",
        "```bash",
        audit["commands"]["materialize_atlas_coordinate_bundle"],
        "```",
        "",
        "Stage the calibration-query and train-target Foldseek directories:",
        "",
        "```bash",
        audit["commands"]["stage_train_calibration_foldseek_dirs"],
        "```",
        "",
        "Run the in-distribution Foldseek pass:",
        "",
        "```bash",
        audit["commands"]["run_in_distribution_atlas_self_vs_atlas"],
        "```",
        "",
        "Rerun the parser:",
        "",
        "```bash",
        audit["commands"]["rerun_contract_parser"],
        "```",
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_augmented_abstention_threshold_contract(
    *,
    fold_augmented_gate_path: Path,
    predicted_structure_fold_channel_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    train_cal_foldseek_tsv: Path,
    out_path: Path,
    report_path: Path | None = None,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    threads: int = 4,
) -> dict[str, Any]:
    audit = build_fold_augmented_abstention_threshold_contract(
        fold_augmented_gate_path=fold_augmented_gate_path,
        predicted_structure_fold_channel_path=predicted_structure_fold_channel_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        train_cal_foldseek_tsv=train_cal_foldseek_tsv,
        foldseek_binary=foldseek_binary,
        threads=threads,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_fold_augmented_abstention_threshold_contract_report(audit),
            encoding="utf-8",
        )
    return audit


def _source_path_record(path: Path) -> dict[str, Any]:
    path = Path(path)
    return {
        "path": str(path),
        "exists": path.exists(),
        "sha256": _sha256(path) if path.exists() else None,
    }


def _train_cal_oos_candidate_ids(surface_manifest: dict[str, Any]) -> list[str]:
    groups = surface_manifest.get("candidate_entry_ids") or {}
    candidates = groups.get("calibration_oos_candidates_hash20pct")
    if candidates is None:
        candidates = surface_manifest.get("calibration_oos_candidate_entry_ids") or []
    return [str(entry_id) for entry_id in candidates if entry_id]


def _empty_predicted_geometry_features() -> dict[str, Any]:
    return {
        "metadata": {
            "artifact": "alphafold_predicted_active_site_geometry_features",
            "schema_version": "predicted_geometry_features.v1",
            "source": "AlphaFoldDB mmCIF by current702 UniProt accession",
            "entry_count": 0,
            "ok_entry_count": 0,
            "entries_with_pairwise_geometry": 0,
            "entries_with_proximal_ligands": 0,
            "entries_with_pocket_context": 0,
            "unique_accession_count": 0,
            "fetch_failure_count": 0,
            "fetch_failures_sample": [],
            "mechanism_text_snippets_used": False,
            "entry_names_used_for_score": False,
        },
        "entries": [],
    }


def _candidate_coordinate_rows(
    candidate_rows: list[dict[str, Any]],
    predicted_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    predicted_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in predicted_rows
        if isinstance(row, dict) and row.get("entry_id")
    }
    out = []
    for row in candidate_rows:
        entry_id = str(row.get("entry_id") or "")
        predicted = predicted_by_entry.get(entry_id, {})
        merged = dict(row)
        if predicted.get("predicted_pdb_id") or predicted.get("pdb_id"):
            merged["predicted_pdb_id"] = predicted.get("predicted_pdb_id") or predicted.get("pdb_id")
        out.append(merged)
    return out


def _materialize_train_cal_oos_coordinates_command(artifact_path: Path) -> str:
    return (
        "python - <<'PY'\n"
        "import json\n"
        "import urllib.request\n"
        "from pathlib import Path\n"
        f"artifact = json.loads(Path({str(artifact_path)!r}).read_text())\n"
        "groups = artifact['foldseek_input_manifest']['coordinate_request_groups']\n"
        "for group in groups.values():\n"
        "    for item in group:\n"
        "        path = item.get('expected_local_path')\n"
        "        url = item.get('url')\n"
        "        if not path or not url:\n"
        "            continue\n"
        "        target = Path(path)\n"
        "        target.parent.mkdir(parents=True, exist_ok=True)\n"
        "        if target.exists():\n"
        "            continue\n"
        "        urllib.request.urlretrieve(url, target)\n"
        "PY"
    )


def build_fold_augmented_train_cal_oos_negative_surface_scores(
    *,
    negative_surface_manifest_path: Path,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    threshold_contract_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    coordinate_root: Path,
    train_cal_oos_foldseek_tsv: Path,
    out_path: Path | None = None,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    alphafold_version: str = "auto",
    threads: int = 4,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    surface_manifest = _read_json(negative_surface_manifest_path)
    label_manifest = _read_json(label_manifest_path)
    graph = _read_json(graph_path)
    experimental_geometry_features = _read_json(experimental_geometry_features_path)
    threshold_contract = _read_json(threshold_contract_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    cofactor_sidecar = _read_json(selected_organic_cofactor_sidecar_path)

    candidate_ids = _train_cal_oos_candidate_ids(surface_manifest)
    candidate_id_set = set(candidate_ids)
    manifest_rows = [
        row for row in label_manifest.get("rows", []) if isinstance(row, dict)
    ]
    manifest_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in manifest_rows
        if row.get("entry_id")
    }
    candidate_manifest_rows = [
        manifest_by_entry[entry_id]
        for entry_id in candidate_ids
        if entry_id in manifest_by_entry
    ]
    missing_manifest_ids = [
        entry_id for entry_id in candidate_ids if entry_id not in manifest_by_entry
    ]
    selected_geometry_rows_all, excluded_geometry_rows_all = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment=None,
        max_rows=0,
    )
    geometry_target_rows = [
        row
        for row in selected_geometry_rows_all
        if str(row.get("entry_id") or "") in candidate_id_set
    ]
    excluded_geometry_rows = [
        row
        for row in excluded_geometry_rows_all
        if str(row.get("entry_id") or "") in candidate_id_set
    ]
    predicted_geometry = (
        build_alphafold_predicted_geometry_features(
            label_manifest_rows=geometry_target_rows,
            graph=graph,
            experimental_geometry_features=experimental_geometry_features,
            alphafold_version=alphafold_version,
            fetcher=fetcher,
        )
        if geometry_target_rows
        else _empty_predicted_geometry_features()
    )
    predicted_retrieval = run_geometry_retrieval(predicted_geometry)
    candidate_predicted_rows = _enriched_predicted_retrieval_results(
        retrieval_results=predicted_retrieval.get("results", []),
        manifest_rows=manifest_rows,
        predicted_entries=predicted_geometry.get("entries", []),
    )
    predicted_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in candidate_predicted_rows
        if row.get("entry_id")
    }

    train_entry_ids = set(
        threshold_contract.get("train_cal_partition", {}).get("train_entry_ids", [])
    )
    train_atlas_rows = [
        row
        for row in predicted_atlas.get("results", [])
        if (
            isinstance(row, dict)
            and str(row.get("entry_id") or "") in train_entry_ids
            and row.get("split_assignment") == "in_distribution"
            and row.get("true_fingerprint_id")
            and _predicted_row_ok(row)
        )
    ]
    coordinate_root = Path(coordinate_root)
    query_requests = _coordinate_requests(
        _candidate_coordinate_rows(candidate_manifest_rows, candidate_predicted_rows),
        coordinate_root=coordinate_root,
        role="train_cal_oos_negative_calibration_query",
        subdir="calibration_oos_queries",
    )
    target_requests = _coordinate_requests(
        train_atlas_rows,
        coordinate_root=coordinate_root,
        role="threshold_contract_train_atlas_target",
        subdir="train_targets",
    )
    parsed_foldseek = _parse_foldseek_tsv_hits(
        result_tsv=train_cal_oos_foldseek_tsv,
        query_requests=query_requests,
        target_requests=target_requests,
    )
    fold_by_entry = {
        str(row.get("query_entry_id") or ""): row
        for row in parsed_foldseek.get("nearest_atlas_hits", [])
    }

    candidate_row_scores: list[dict[str, Any]] = []
    for entry_id in candidate_ids:
        manifest_row = manifest_by_entry.get(entry_id, {})
        geo = predicted_by_entry.get(entry_id, {})
        fold_hit = fold_by_entry.get(entry_id)
        cofactor_scores = _cofactor_scores_for_entry(cofactor_sidecar, entry_id)
        top = _top1_fingerprint(geo) if geo else None
        geom_score = float(top.get("score")) if top and top.get("score") is not None else None
        fold_score = (
            float(fold_hit.get("tm_score"))
            if fold_hit and fold_hit.get("tm_score") is not None
            else None
        )
        cofactor_max = max(cofactor_scores.values()) if cofactor_scores else None
        channel_scores = (
            _fold_augmented_channel_scores(
                geometry_score=geom_score,
                cofactor_max_score=float(cofactor_max),
                fold_tm_score=fold_score,
            )
            if geom_score is not None and fold_score is not None and cofactor_max is not None
            else None
        )
        candidate_row_scores.append(
            {
                "entry_id": entry_id,
                "accession": manifest_row.get("accession") or manifest_row.get("sequence_id"),
                "split_assignment": manifest_row.get("split_assignment"),
                "benchmark_role": manifest_row.get("benchmark_role"),
                "oos_tier": manifest_row.get("oos_tier"),
                "label_type": manifest_row.get("label_type"),
                "is_calibration_oos_negative": True,
                "predicted_geometry_status": _predicted_row_status(geo) if geo else "missing",
                "predicted_geometry_top1": {
                    "fingerprint_id": top.get("fingerprint_id") if top else None,
                    "score": geom_score,
                    "role_match_fraction": top.get("role_match_fraction") if top else None,
                    "cofactor_context_score": top.get("cofactor_context_score") if top else None,
                },
                "selected_organic_cofactor_max_score": cofactor_max,
                "predicted_structure_fold_channel": {
                    "nearest_train_atlas_entry_id": (
                        fold_hit.get("nearest_atlas_entry_id") if fold_hit else None
                    ),
                    "nearest_train_atlas_true_fingerprint_id": (
                        fold_hit.get("nearest_atlas_true_fingerprint_id") if fold_hit else None
                    ),
                    "nearest_train_atlas_tm_score": fold_score,
                    "raw_query_name": fold_hit.get("raw_query_name") if fold_hit else None,
                    "raw_target_name": fold_hit.get("raw_target_name") if fold_hit else None,
                },
                "channel_scores": channel_scores,
            }
        )

    rows_with_geometry = [
        row for row in candidate_row_scores if row["predicted_geometry_status"] == "ok"
    ]
    rows_with_fold = [
        row
        for row in candidate_row_scores
        if row["predicted_structure_fold_channel"]["nearest_train_atlas_tm_score"] is not None
    ]
    rows_with_full_scores = [row for row in candidate_row_scores if row["channel_scores"]]
    foldseek = _foldseek_binary_info(foldseek_binary)
    query_missing = _missing_coordinate_count(query_requests)
    target_missing = _missing_coordinate_count(target_requests)
    blockers: list[str] = []
    if missing_manifest_ids:
        blockers.append("some_calibration_oos_candidates_missing_from_label_manifest")
    if len(rows_with_geometry) < len(candidate_ids):
        blockers.append("some_calibration_oos_candidates_missing_predicted_geometry")
    if parsed_foldseek["status"] != "parsed":
        blockers.append("train_cal_oos_foldseek_tsv_missing_or_unparsed")
    if len(rows_with_fold) < len(candidate_ids):
        blockers.append("some_calibration_oos_candidates_missing_fold_scores")
    if query_missing:
        blockers.append("candidate_query_coordinate_files_missing")
    if target_missing:
        blockers.append("train_atlas_target_coordinate_files_missing")
    if not rows_with_full_scores:
        blockers.append("no_calibration_oos_negative_rows_have_full_channel_scores")

    if rows_with_full_scores and parsed_foldseek["status"] == "parsed":
        status = (
            "computed_train_cal_oos_negative_surface_scores"
            if len(rows_with_full_scores) == len(candidate_ids)
            else "computed_partial_train_cal_oos_negative_surface_scores"
        )
    elif foldseek["available"] and not query_missing and not target_missing:
        status = "ready_to_run_train_cal_oos_negative_foldseek"
    else:
        status = "manifest_staged_train_cal_oos_negative_surface_scoring"

    result_tsv = Path(train_cal_oos_foldseek_tsv)
    result_root = result_tsv.parent
    output_artifact_path = out_path or Path(
        f"artifacts/{FOLD_AUGMENTED_TRAIN_CAL_OOS_NEGATIVE_SURFACE_SCORES_ID}.json"
    )
    return {
        "artifact_id": FOLD_AUGMENTED_TRAIN_CAL_OOS_NEGATIVE_SURFACE_SCORES_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Bounded predicted-geometry plus Foldseek feature surface for the "
            "hash-selected current702 in-distribution OOS calibration negatives "
            "needed by the fold-augmented threshold contract."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_rows_used_for_selection_or_scoring": False,
            "heldout_threshold_tuning_for_deployment": False,
            "frozen_current702_inputs_only": True,
            "large_model_downloads_performed": False,
            "raw_coordinates_committed": False,
            "score_fabrication": False,
        },
        "selection_policy": {
            "candidate_source": str(negative_surface_manifest_path),
            "candidate_selector": surface_manifest.get("selection_policy", {}).get(
                "calibration_negative_selector"
            ),
            "candidate_definition": surface_manifest.get("selection_policy", {}).get(
                "candidate_definition"
            ),
            "train_target_policy": surface_manifest.get("selection_policy", {}).get(
                "train_target_policy"
            ),
            "threshold_use": (
                "These rows may be used as train/cal OOS negatives for threshold "
                "selection in a future contract; no threshold is selected here."
            ),
        },
        "counts": {
            "candidate_ids_requested": len(candidate_ids),
            "candidate_manifest_rows_found": len(candidate_manifest_rows),
            "candidate_geometry_target_rows": len(geometry_target_rows),
            "candidate_geometry_excluded_rows": len(excluded_geometry_rows),
            "candidate_predicted_geometry_rows": len(candidate_predicted_rows),
            "candidate_predicted_geometry_ok_rows": len(rows_with_geometry),
            "train_atlas_target_rows": len(train_atlas_rows),
            "candidate_query_coordinate_requests": len(query_requests),
            "train_atlas_target_coordinate_requests": len(target_requests),
            "candidate_query_coordinate_files_missing": query_missing,
            "train_atlas_target_coordinate_files_missing": target_missing,
            "foldseek_rows_with_nearest_train_hits": len(rows_with_fold),
            "candidate_rows_with_full_channel_scores": len(rows_with_full_scores),
            "missing_manifest_ids": len(missing_manifest_ids),
        },
        "blockers": blockers,
        "candidate_entry_ids": candidate_ids,
        "missing_manifest_entry_ids": missing_manifest_ids,
        "excluded_candidate_geometry_rows": excluded_geometry_rows,
        "predicted_geometry_candidate_retrieval": {
            "metadata": predicted_retrieval.get("metadata", {}),
            "predicted_geometry_metadata": predicted_geometry.get("metadata", {}),
            "results": candidate_predicted_rows,
        },
        "parsed_train_cal_oos_foldseek": parsed_foldseek,
        "candidate_row_scores": candidate_row_scores,
        "foldseek_input_manifest": {
            "coordinate_root": str(coordinate_root),
            "calibration_oos_query_dir": str(coordinate_root / "calibration_oos_queries"),
            "train_atlas_target_dir": str(coordinate_root / "train_targets"),
            "result_root": str(result_root),
            "coordinate_request_groups": {
                "calibration_oos_queries": query_requests,
                "train_atlas_targets": target_requests,
            },
        },
        "runtime": {
            "foldseek": foldseek,
            "threads": max(1, int(threads)),
            "alphafold_version": alphafold_version,
        },
        "commands": {
            "materialize_coordinate_bundle": _materialize_train_cal_oos_coordinates_command(
                output_artifact_path
            ),
            "run_train_cal_oos_negatives_vs_train_atlas": _foldseek_easy_search_command(
                binary=str(foldseek.get("resolved") or foldseek_binary),
                query_dir=coordinate_root / "calibration_oos_queries",
                target_dir=coordinate_root / "train_targets",
                result_tsv=result_tsv,
                tmp_dir=result_root / "tmp_train_cal_oos_negatives_vs_train_atlas",
                threads=threads,
            ),
            "rerun_parser": (
                "PYTHONPATH=src python -m catalytic_earth.cli "
                "score-fold-augmented-train-cal-oos-negative-surface "
                f"--train-cal-oos-foldseek-tsv {shlex.quote(str(result_tsv))}"
            ),
            "foldseek_tsv_columns": [
                "query",
                "target",
                "qtmscore",
                "ttmscore",
                "alntmscore",
                "prob",
                "bits",
            ],
        },
        "source_artifacts": {
            "negative_surface_manifest": _source_path_record(negative_surface_manifest_path),
            "label_manifest": _source_path_record(label_manifest_path),
            "graph": _source_path_record(graph_path),
            "experimental_geometry_features": _source_path_record(experimental_geometry_features_path),
            "threshold_contract": _source_path_record(threshold_contract_path),
            "predicted_geometry_atlas": _source_path_record(predicted_geometry_atlas_path),
            "selected_organic_cofactor_sidecar": _source_path_record(selected_organic_cofactor_sidecar_path),
            "train_cal_oos_foldseek_tsv": _source_path_record(train_cal_oos_foldseek_tsv),
        },
        "interpretation": {
            "headline": (
                "The train/cal OOS negative surface now has predicted-geometry, "
                "cofactor, and nearest-train Foldseek/TM channel scores for the "
                f"{len(rows_with_full_scores)} score-complete candidate rows."
                if rows_with_full_scores
                else "The train/cal OOS negative surface is staged, but no full channel scores are available yet."
            ),
            "next_action": (
                "Extend the fold-augmented threshold contract to consume these "
                "calibration OOS negatives for OOS-aware threshold selection, "
                "while keeping heldout final-only."
                if rows_with_full_scores
                else "Materialize candidate and train-atlas coordinates, run Foldseek, then rerun this parser."
            ),
        },
    }


def _render_fold_augmented_train_cal_oos_negative_surface_scores_report(
    audit: dict[str, Any],
) -> str:
    counts = audit["counts"]
    parsed = audit.get("parsed_train_cal_oos_foldseek", {})
    lines = [
        "# Fold-Augmented Train/Cal OOS Negative Surface Scores - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Candidate IDs requested: {counts['candidate_ids_requested']}",
        f"- Predicted geometry ok rows: {counts['candidate_predicted_geometry_ok_rows']}",
        f"- Foldseek rows with nearest train hits: {counts['foldseek_rows_with_nearest_train_hits']}",
        f"- Full channel score rows: {counts['candidate_rows_with_full_channel_scores']}",
        f"- Foldseek TSV parse status: {parsed.get('status')}",
        "",
        "## Blockers",
        "",
    ]
    if audit["blockers"]:
        lines += [f"- {blocker}" for blocker in audit["blockers"]]
    else:
        lines.append("- None")
    lines += [
        "",
        "## Score Preview",
        "",
        "| Entry | geometry top1 | geometry score | nearest train atlas | fold TM | combined mean geometry/fold |",
        "| --- | --- | ---: | --- | ---: | ---: |",
    ]
    for row in audit["candidate_row_scores"][:25]:
        channel = row.get("channel_scores") or {}
        geo = row.get("predicted_geometry_top1") or {}
        fold = row.get("predicted_structure_fold_channel") or {}
        lines.append(
            f"| {row['entry_id']} | {geo.get('fingerprint_id')} | {geo.get('score')} | "
            f"{fold.get('nearest_train_atlas_entry_id')} | "
            f"{fold.get('nearest_train_atlas_tm_score')} | "
            f"{channel.get('combined_mean_geometry_fold')} |"
        )
    lines += [
        "",
        "## Commands",
        "",
        "Materialize the candidate query and train-atlas target coordinate bundle:",
        "",
        "```bash",
        audit["commands"]["materialize_coordinate_bundle"],
        "```",
        "",
        "Run Foldseek for calibration OOS negatives versus the train atlas:",
        "",
        "```bash",
        audit["commands"]["run_train_cal_oos_negatives_vs_train_atlas"],
        "```",
        "",
        "Rerun the parser:",
        "",
        "```bash",
        audit["commands"]["rerun_parser"],
        "```",
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_augmented_train_cal_oos_negative_surface_scores(
    *,
    negative_surface_manifest_path: Path,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    threshold_contract_path: Path,
    predicted_geometry_atlas_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    coordinate_root: Path,
    train_cal_oos_foldseek_tsv: Path,
    out_path: Path,
    report_path: Path | None = None,
    foldseek_binary: str = DEFAULT_FOLDSEEK_BINARY,
    alphafold_version: str = "auto",
    threads: int = 4,
) -> dict[str, Any]:
    audit = build_fold_augmented_train_cal_oos_negative_surface_scores(
        negative_surface_manifest_path=negative_surface_manifest_path,
        label_manifest_path=label_manifest_path,
        graph_path=graph_path,
        experimental_geometry_features_path=experimental_geometry_features_path,
        threshold_contract_path=threshold_contract_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        coordinate_root=coordinate_root,
        train_cal_oos_foldseek_tsv=train_cal_oos_foldseek_tsv,
        out_path=out_path,
        foldseek_binary=foldseek_binary,
        alphafold_version=alphafold_version,
        threads=threads,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_fold_augmented_train_cal_oos_negative_surface_scores_report(audit),
            encoding="utf-8",
        )
    return audit


def build_fold_only_train_cal_oos_negative_surface(
    *,
    train_cal_oos_surface_path: Path,
) -> dict[str, Any]:
    surface = _read_json(train_cal_oos_surface_path)
    rows = []
    for row in surface.get("candidate_row_scores", []):
        if not isinstance(row, dict) or row.get("channel_scores") is not None:
            continue
        fold = row.get("predicted_structure_fold_channel") or {}
        tm_score = fold.get("nearest_train_atlas_tm_score")
        if tm_score is None:
            continue
        rows.append(
            {
                "entry_id": row.get("entry_id"),
                "accession": row.get("accession"),
                "benchmark_role": row.get("benchmark_role"),
                "predicted_geometry_status": row.get("predicted_geometry_status"),
                "nearest_train_atlas_entry_id": fold.get("nearest_train_atlas_entry_id"),
                "nearest_train_atlas_true_fingerprint_id": fold.get(
                    "nearest_train_atlas_true_fingerprint_id"
                ),
                "nearest_train_atlas_tm_score": float(tm_score),
                "fold_novelty_direction": "lower_nearest_train_tm_is_more_fold_novel",
            }
        )
    values = [float(row["nearest_train_atlas_tm_score"]) for row in rows]
    return {
        "artifact_id": "v3_fold_only_train_cal_oos_negative_surface_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "fold_only_negative_surface_ready" if rows else "no_fold_only_rows_available",
        "scope": (
            "Fold-only salvage surface for train/cal OOS negatives with real "
            "Foldseek/TM hits but missing predicted-geometry channel scores."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_rows_used_for_selection_or_scoring": False,
            "fold_only_not_combined_geometry_threshold": True,
        },
        "counts": {
            "fold_only_rows": len(rows),
            "nearest_train_fingerprint_counts": dict(
                sorted(
                    Counter(
                        str(row.get("nearest_train_atlas_true_fingerprint_id"))
                        for row in rows
                    ).items()
                )
            ),
            "min_nearest_train_tm": round(min(values), 6) if values else None,
            "max_nearest_train_tm": round(max(values), 6) if values else None,
            "mean_nearest_train_tm": round(sum(values) / len(values), 6) if values else None,
        },
        "rows": sorted(rows, key=lambda row: _entry_id_sort_key(str(row.get("entry_id")))),
        "interpretation": {
            "headline": (
                "Calibration OOS candidates with fold evidence but missing geometry "
                "are available for fold-only sensitivity checks."
            ),
            "next_action": (
                "Use these only for fold-only diagnostics or repair active-site "
                "geometry eligibility before combined threshold calibration."
            ),
        },
        "source_artifacts": {
            "train_cal_oos_surface": _source_path_record(train_cal_oos_surface_path),
        },
    }


def _render_fold_only_train_cal_oos_negative_surface_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Fold-Only Train/Cal OOS Negative Surface - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Fold-only rows: {counts['fold_only_rows']}",
        f"- Mean nearest-train TM: {counts['mean_nearest_train_tm']}",
        f"- Nearest train fingerprint counts: {counts['nearest_train_fingerprint_counts']}",
        "",
        "## Rows",
        "",
        "| Entry | geometry status | nearest train atlas | nearest train fingerprint | TM |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for row in audit["rows"]:
        lines.append(
            f"| {row['entry_id']} | {row['predicted_geometry_status']} | "
            f"{row['nearest_train_atlas_entry_id']} | "
            f"{row['nearest_train_atlas_true_fingerprint_id']} | "
            f"{row['nearest_train_atlas_tm_score']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_only_train_cal_oos_negative_surface(
    *,
    train_cal_oos_surface_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_fold_only_train_cal_oos_negative_surface(
        train_cal_oos_surface_path=train_cal_oos_surface_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_fold_only_train_cal_oos_negative_surface_report(audit),
            encoding="utf-8",
        )
    return audit


def build_fold_augmented_train_cal_oos_negative_surface_blocker_resolution(
    *,
    train_cal_oos_surface_path: Path,
) -> dict[str, Any]:
    surface = _read_json(train_cal_oos_surface_path)
    excluded = {
        str(row.get("entry_id")): row
        for row in surface.get("excluded_candidate_geometry_rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    fetch_failures = {
        str(row.get("entry_id")): row
        for row in (
            surface.get("predicted_geometry_candidate_retrieval", {})
            .get("predicted_geometry_metadata", {})
            .get("fetch_failures_sample", [])
        )
        if isinstance(row, dict) and row.get("entry_id")
    }
    blocker_rows = []
    for row in surface.get("candidate_row_scores", []):
        if not isinstance(row, dict) or row.get("channel_scores") is not None:
            continue
        entry_id = str(row.get("entry_id") or "")
        if entry_id in excluded:
            reason = str(excluded[entry_id].get("reason"))
        elif entry_id in fetch_failures:
            reason = "alphafold_db_coordinate_unavailable"
        else:
            reason = "fold_or_cofactor_score_missing"
        if reason == "missing_accession_compatible_sequence_positions":
            action = (
                "repair_or_add accession-compatible catalytic residue "
                "sequence-position mapping before predicted-geometry scoring"
            )
        elif reason.startswith("experimental_geometry_not_ok"):
            action = (
                "repair source geometry evidence or keep row excluded from "
                "geometry-calibrated OOS surface"
            )
        elif reason == "not_m_csa_entry":
            action = (
                "provide an active-site residue sidecar for UniProt-only rows "
                "or score them in a fold-only negative surface"
            )
        elif reason == "alphafold_db_coordinate_unavailable":
            action = (
                "verify replacement accession or alternate local coordinate source; "
                "AFDB has no v1-v6 model for this accession"
            )
        else:
            action = "inspect row-level fold/cofactor availability and rerun scorer after repair"
        fold = row.get("predicted_structure_fold_channel") or {}
        blocker_rows.append(
            {
                "entry_id": entry_id,
                "accession": row.get("accession"),
                "benchmark_role": row.get("benchmark_role"),
                "predicted_geometry_status": row.get("predicted_geometry_status"),
                "fold_tm_available": fold.get("nearest_train_atlas_tm_score") is not None,
                "blocker_reason": reason,
                "recommended_action": action,
                "fetch_failure": fetch_failures.get(entry_id),
            }
        )
    reason_counts = Counter(row["blocker_reason"] for row in blocker_rows)
    action_groups: dict[str, list[str]] = defaultdict(list)
    for row in blocker_rows:
        action_groups[row["recommended_action"]].append(row["entry_id"])
    counts = surface.get("counts", {})
    return {
        "artifact_id": "v3_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "blocker_resolution_packet_ready",
        "scope": (
            "Row-level blocker-resolution packet for calibration OOS negatives "
            "missing full fold-augmented channel scores."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "heldout_rows_used_for_selection_or_scoring": False,
            "frozen_current702_inputs_only": True,
        },
        "counts": {
            "candidate_ids_requested": counts.get("candidate_ids_requested"),
            "score_complete_rows": counts.get("candidate_rows_with_full_channel_scores"),
            "missing_full_score_rows": len(blocker_rows),
            "rows_with_fold_only_no_geometry": sum(
                1 for row in blocker_rows if row["fold_tm_available"]
            ),
            "blocker_reason_counts": dict(sorted(reason_counts.items())),
        },
        "blocker_rows": sorted(
            blocker_rows,
            key=lambda row: _entry_id_sort_key(str(row.get("entry_id"))),
        ),
        "action_groups": {
            action: sorted(ids, key=_entry_id_sort_key)
            for action, ids in sorted(action_groups.items())
        },
        "interpretation": {
            "headline": (
                "The remaining OOS calibration gap is mostly active-site "
                "mapping/geometry eligibility, not Foldseek runtime."
            ),
            "next_action": (
                "Repair accession-compatible active-site mappings for the six "
                "m_csa rows first; then rerun the scorer and OOS-calibrated "
                "threshold contract."
            ),
        },
        "source_artifacts": {
            "score_surface": _source_path_record(train_cal_oos_surface_path),
        },
    }


def _render_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_report(
    audit: dict[str, Any],
) -> str:
    counts = audit["counts"]
    lines = [
        "# Fold-Augmented Train/Cal OOS Negative Surface Blocker Resolution - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Score-complete rows: {counts['score_complete_rows']} / {counts['candidate_ids_requested']}",
        f"- Missing full-score rows: {counts['missing_full_score_rows']}",
        f"- Rows with fold-only but no geometry: {counts['rows_with_fold_only_no_geometry']}",
        f"- Blocker reason counts: {counts['blocker_reason_counts']}",
        "",
        "## Blocker Rows",
        "",
        "| Entry | accession | reason | fold TM available | recommended action |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in audit["blocker_rows"]:
        lines.append(
            f"| {row['entry_id']} | {row.get('accession')} | {row['blocker_reason']} | "
            f"{row['fold_tm_available']} | {row['recommended_action']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_augmented_train_cal_oos_negative_surface_blocker_resolution(
    *,
    train_cal_oos_surface_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_fold_augmented_train_cal_oos_negative_surface_blocker_resolution(
        train_cal_oos_surface_path=train_cal_oos_surface_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_report(audit),
            encoding="utf-8",
        )
    return audit


def _score_threshold_for_min_retain_max_oos(
    calibration_in_scope_rows: list[dict[str, Any]],
    calibration_oos_rows: list[dict[str, Any]],
    channel_name: str,
    *,
    min_retain: float,
) -> dict[str, Any] | None:
    in_scope_scores = [
        float(row["channel_scores"][channel_name])
        for row in calibration_in_scope_rows
        if row.get("channel_scores") and channel_name in row["channel_scores"]
    ]
    oos_scores = [
        float(row["channel_scores"][channel_name])
        for row in calibration_oos_rows
        if row.get("channel_scores") and channel_name in row["channel_scores"]
    ]
    if not in_scope_scores or not oos_scores:
        return None
    candidates = sorted({round(score, 6) for score in in_scope_scores + oos_scores})
    best: tuple[tuple[float, float], dict[str, Any]] | None = None
    for threshold in candidates:
        retained = sum(1 for score in in_scope_scores if score >= threshold)
        retain = retained / len(in_scope_scores)
        if retain < min_retain:
            continue
        abstained = sum(1 for score in oos_scores if score < threshold)
        abstain = abstained / len(oos_scores)
        item = {
            "threshold": threshold,
            "min_retain_target": min_retain,
            "calibration_in_scope_retain_recall": round(retain, 4),
            "calibration_in_scope_retained": retained,
            "calibration_in_scope_total": len(in_scope_scores),
            "calibration_oos_abstain_recall": round(abstain, 4),
            "calibration_oos_abstained": abstained,
            "calibration_oos_total": len(oos_scores),
            "objective": "maximize_calibration_oos_abstain_recall_subject_to_in_scope_retention",
        }
        key = (abstain, threshold)
        if best is None or key > best[0]:
            best = (key, item)
    return best[1] if best else None


def build_fold_augmented_oos_calibrated_threshold_contract(
    *,
    threshold_contract_path: Path,
    train_cal_oos_surface_path: Path,
    fold_augmented_gate_path: Path,
) -> dict[str, Any]:
    threshold_contract = _read_json(threshold_contract_path)
    oos_surface = _read_json(train_cal_oos_surface_path)
    fold_gate = _read_json(fold_augmented_gate_path)
    calibration_in_scope_rows = [
        row
        for row in threshold_contract.get("calibration_row_scores", [])
        if isinstance(row, dict) and row.get("channel_scores")
    ]
    calibration_oos_rows = [
        row
        for row in oos_surface.get("candidate_row_scores", [])
        if isinstance(row, dict) and row.get("channel_scores")
    ]
    heldout_rows = [
        row
        for row in fold_gate.get("row_scores", [])
        if isinstance(row, dict) and row.get("channel_scores")
    ]
    channel_names = sorted(
        {
            name
            for row in calibration_in_scope_rows + calibration_oos_rows + heldout_rows
            for name in (row.get("channel_scores") or {})
        }
    ) or [
        "geometry_top1_score",
        "cofactor_max_score",
        "fold_nearest_atlas_tm_score",
        "combined_mean_geometry_cofactor_fold",
        "combined_mean_geometry_fold",
        "combined_min_geometry_fold",
    ]
    contract: dict[str, Any] = {}
    prior = threshold_contract.get("threshold_contract", {})
    for channel_name in channel_names:
        at90 = _score_threshold_for_min_retain_max_oos(
            calibration_in_scope_rows,
            calibration_oos_rows,
            channel_name,
            min_retain=0.90,
        )
        at85 = _score_threshold_for_min_retain_max_oos(
            calibration_in_scope_rows,
            calibration_oos_rows,
            channel_name,
            min_retain=0.85,
        )
        prior_channel = prior.get(channel_name, {})
        prior90 = prior_channel.get("selected_at_90pct_calibration_in_scope_retention")
        contract[channel_name] = {
            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": at90,
            "selected_at_85pct_calibration_in_scope_retention_max_oos_abstain": at85,
            "prior_in_scope_only_selected_at_90pct": prior90,
            "threshold_changed_from_in_scope_only_90pct": (
                bool(
                    at90
                    and prior90
                    and float(at90["threshold"]) != float(prior90["threshold"])
                )
                if at90 and prior90
                else None
            ),
            "heldout_final_eval_at_90pct_oos_calibrated_threshold": (
                _evaluate_threshold_on_heldout(
                    heldout_rows,
                    channel_name,
                    float(at90["threshold"]),
                )
                if at90
                else None
            ),
            "heldout_final_eval_at_85pct_oos_calibrated_threshold": (
                _evaluate_threshold_on_heldout(
                    heldout_rows,
                    channel_name,
                    float(at85["threshold"]),
                )
                if at85
                else None
            ),
        }
    blockers: list[str] = []
    if not calibration_in_scope_rows:
        blockers.append("no_calibration_in_scope_rows_available")
    if not calibration_oos_rows:
        blockers.append("no_calibration_oos_negative_rows_available")
    if not heldout_rows:
        blockers.append("no_heldout_final_eval_rows_available")
    if oos_surface.get("status") != "computed_train_cal_oos_negative_surface_scores":
        blockers.append("train_cal_oos_negative_surface_is_partial")
    primary = contract.get("combined_mean_geometry_fold", {})
    status = (
        "computed_oos_calibrated_threshold_contract"
        if calibration_in_scope_rows and calibration_oos_rows and heldout_rows
        else "blocked_missing_oos_calibration_surface"
    )
    return {
        "artifact_id": FOLD_AUGMENTED_OOS_CALIBRATED_THRESHOLD_CONTRACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": status,
        "scope": (
            "Leakage-safe OOS-calibrated fold-augmented threshold contract. "
            "Thresholds are selected using deterministic in-distribution calibration "
            "in-scope rows plus hash-selected in-distribution OOS calibration negatives; "
            "heldout rows remain final evaluation only."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "thresholds_selected_on_heldout": False,
            "heldout_used_for_final_eval_only": True,
            "train_cal_oos_negatives_used_for_threshold": True,
            "frozen_current702_inputs_only": True,
        },
        "selection_policy": {
            "objective": "maximize_calibration_oos_abstain_recall_subject_to_in_scope_retention",
            "target_retention_levels": [0.90, 0.85],
            "calibration_in_scope_source": str(threshold_contract_path),
            "calibration_oos_negative_source": str(train_cal_oos_surface_path),
            "heldout_policy": "heldout rows are evaluated after threshold selection and do not affect thresholds",
            "production_status": "research_contract_not_production_threshold",
        },
        "counts": {
            "calibration_in_scope_rows": len(calibration_in_scope_rows),
            "calibration_oos_negative_rows": len(calibration_oos_rows),
            "calibration_oos_negative_candidates_requested": oos_surface.get("counts", {}).get(
                "candidate_ids_requested"
            ),
            "heldout_rows_final_eval": len(heldout_rows),
            "heldout_in_scope": sum(1 for row in heldout_rows if row.get("is_inscope")),
            "heldout_oos": sum(1 for row in heldout_rows if row.get("is_oos")),
            "heldout_confounded_oos": sum(
                1 for row in heldout_rows if row.get("is_confounded_predicted_geometry_oos")
            ),
        },
        "blockers": blockers,
        "threshold_contract": contract,
        "primary_channel_readout": {
            "channel": "combined_mean_geometry_fold",
            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": primary.get(
                "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain"
            ),
            "heldout_final_eval_at_90pct_oos_calibrated_threshold": primary.get(
                "heldout_final_eval_at_90pct_oos_calibrated_threshold"
            ),
            "prior_in_scope_only_selected_at_90pct": primary.get(
                "prior_in_scope_only_selected_at_90pct"
            ),
        },
        "calibration_oos_negative_row_scores": calibration_oos_rows,
        "source_artifacts": {
            "threshold_contract": _source_path_record(threshold_contract_path),
            "train_cal_oos_negative_surface": _source_path_record(train_cal_oos_surface_path),
            "fold_augmented_gate": _source_path_record(fold_augmented_gate_path),
        },
        "interpretation": {
            "headline": (
                "The fold-augmented threshold contract now has an OOS-negative calibration surface."
                if status == "computed_oos_calibrated_threshold_contract"
                else "OOS-calibrated threshold selection remains blocked by missing calibration surfaces."
            ),
            "production_status": "research_contract_not_production_threshold; no production scorer or global threshold was changed",
            "next_action": (
                "Review the primary channel's calibration-OOS and heldout final readout, "
                "then decide whether the partial 65-row OOS calibration surface is enough "
                "or whether to clear the remaining candidate geometry blockers first."
            ),
        },
    }


def _render_fold_augmented_oos_calibrated_threshold_contract_report(
    audit: dict[str, Any],
) -> str:
    counts = audit["counts"]
    primary = audit["primary_channel_readout"]
    lines = [
        "# Fold-Augmented OOS-Calibrated Threshold Contract - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Blockers: {audit['blockers']}",
        f"- Calibration in-scope rows: {counts['calibration_in_scope_rows']}",
        f"- Calibration OOS negative rows: {counts['calibration_oos_negative_rows']}",
        f"- Heldout final-eval rows: {counts['heldout_rows_final_eval']}",
        "",
        "## Primary Channel",
        "",
        f"- Channel: {primary['channel']}",
        f"- OOS-calibrated 90% threshold: {primary['selected_at_90pct_calibration_in_scope_retention_max_oos_abstain']}",
        f"- Prior in-scope-only 90% threshold: {primary['prior_in_scope_only_selected_at_90pct']}",
        f"- Heldout final eval at OOS-calibrated threshold: {primary['heldout_final_eval_at_90pct_oos_calibrated_threshold']}",
        "",
        "## Thresholds",
        "",
        "| Channel | OOS-cal >=90 threshold | cal OOS abstain | heldout in-scope retain | heldout OOS abstain | heldout confounded abstain |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, row in audit["threshold_contract"].items():
        selected = row.get("selected_at_90pct_calibration_in_scope_retention_max_oos_abstain") or {}
        heldout = row.get("heldout_final_eval_at_90pct_oos_calibrated_threshold") or {}
        lines.append(
            f"| {name} | {selected.get('threshold')} | "
            f"{selected.get('calibration_oos_abstain_recall')} | "
            f"{heldout.get('heldout_in_scope_retain_recall')} | "
            f"{heldout.get('heldout_oos_abstain_recall')} | "
            f"{heldout.get('heldout_confounded_oos_abstain_recall')} |"
        )
    lines += [
        "",
        "## Contract",
        "",
        f"- {audit['selection_policy']['objective']}",
        f"- {audit['selection_policy']['heldout_policy']}",
        f"- {audit['interpretation']['production_status']}",
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_fold_augmented_oos_calibrated_threshold_contract(
    *,
    threshold_contract_path: Path,
    train_cal_oos_surface_path: Path,
    fold_augmented_gate_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_fold_augmented_oos_calibrated_threshold_contract(
        threshold_contract_path=threshold_contract_path,
        train_cal_oos_surface_path=train_cal_oos_surface_path,
        fold_augmented_gate_path=fold_augmented_gate_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_fold_augmented_oos_calibrated_threshold_contract_report(audit),
            encoding="utf-8",
        )
    return audit


def _normalize_feature_token(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _catalytic_residue_nodes_by_entry(graph: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("type") != "catalytic_residue":
            continue
        node_id = str(node.get("id") or "")
        parts = node_id.split(":")
        if len(parts) < 3:
            continue
        by_entry[f"{parts[0]}:{parts[1]}"].append(node)
    return {
        entry_id: sorted(nodes, key=lambda item: str(item.get("id") or ""))
        for entry_id, nodes in by_entry.items()
    }


def _has_accession_compatible_sequence_positions(
    residue_nodes: list[dict[str, Any]],
    accession: str,
) -> bool:
    if not residue_nodes:
        return False
    for node in residue_nodes:
        candidates = [
            item
            for item in node.get("sequence_positions", [])
            if isinstance(item, dict) and item.get("is_reference", True) and item.get("resid")
        ]
        usable = [
            item
            for item in candidates
            if not item.get("uniprot_id") or str(item.get("uniprot_id")) == accession
        ]
        if not usable:
            return False
    return True


def build_mechanism_feature_active_site_role_graph_sidecar(
    *,
    label_manifest_path: Path,
    graph_path: Path,
) -> dict[str, Any]:
    manifest = _read_json(label_manifest_path)
    graph = _read_json(graph_path)
    manifest_rows = [
        row for row in manifest.get("rows", []) if isinstance(row, dict)
    ]
    residues_by_entry = _catalytic_residue_nodes_by_entry(graph)
    sidecar_rows: list[dict[str, Any]] = []
    role_counter: Counter[str] = Counter()
    edge_counter: Counter[tuple[str, str]] = Counter()
    status_counter: Counter[str] = Counter()
    split_status_counter: Counter[str] = Counter()
    for row in manifest_rows:
        entry_id = str(row.get("entry_id") or "")
        accession = str(row.get("accession") or row.get("sequence_id") or "")
        residue_nodes = residues_by_entry.get(entry_id, [])
        residue_records = []
        row_roles: list[str] = []
        for node in residue_nodes:
            roles = [
                token
                for token in (_normalize_feature_token(role) for role in node.get("roles", []))
                if token
            ]
            row_roles.extend(roles)
            role_counter.update(roles)
            residue_records.append(
                {
                    "residue_node_id": node.get("id"),
                    "roles": roles,
                    "roles_raw": node.get("roles", []),
                    "sequence_positions": node.get("sequence_positions", []),
                    "structure_positions": node.get("structure_positions", []),
                }
            )
        unique_roles = sorted(set(row_roles))
        role_edges = []
        for index, left in enumerate(unique_roles):
            for right in unique_roles[index + 1:]:
                role_edges.append(
                    {
                        "left_role": left,
                        "right_role": right,
                        "edge_type": "same_entry_active_site_cooccurrence",
                    }
                )
                edge_counter[(left, right)] += 1
        compatible = _has_accession_compatible_sequence_positions(
            residue_nodes,
            accession,
        )
        if not entry_id.startswith("m_csa:"):
            status = "not_m_csa_no_curated_active_site_roles"
        elif not residue_nodes:
            status = "missing_catalytic_residue_nodes"
        elif not compatible:
            status = "missing_accession_compatible_sequence_positions"
        else:
            status = "ok"
        status_counter[status] += 1
        split_status_counter[f"{row.get('split_assignment') or 'unknown'}::{status}"] += 1
        sidecar_rows.append(
            {
                "entry_id": entry_id,
                "accession": accession,
                "split_assignment": row.get("split_assignment"),
                "benchmark_role": row.get("benchmark_role"),
                "fingerprint_id": row.get("fingerprint_id")
                or row.get("mechanism_fingerprint_id"),
                "label_type": row.get("label_type"),
                "status": status,
                "active_site_residue_count": len(residue_records),
                "accession_compatible_sequence_positions": compatible,
                "role_counts": dict(sorted(Counter(row_roles).items())),
                "role_edges": role_edges,
                "residues": residue_records,
            }
        )
    return {
        "artifact_id": "v3_mechanism_feature_active_site_role_graph_sidecar_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "active_site_role_graph_sidecar_ready",
        "scope": (
            "Row-level active-site residue-role graph sidecar for current702 "
            "mechanism-feature embedding gap closure."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "heldout_threshold_tuning_for_deployment": False,
            "feature_sidecar_only": True,
        },
        "counts": {
            "manifest_rows": len(manifest_rows),
            "rows_by_status": dict(sorted(status_counter.items())),
            "rows_with_ok_role_graph": status_counter.get("ok", 0),
            "unique_roles": len(role_counter),
            "unique_role_edges": len(edge_counter),
            "top_roles": role_counter.most_common(20),
            "split_status_counts": dict(sorted(split_status_counter.items())),
        },
        "role_vocabulary": dict(sorted(role_counter.items())),
        "role_edge_vocabulary": [
            {"left_role": left, "right_role": right, "row_count": count}
            for (left, right), count in sorted(edge_counter.items())
        ],
        "rows": sidecar_rows,
        "interpretation": {
            "embedding_gap_closed": "row_level_active_site_residue_role_graph_vocabulary_normalized",
            "remaining_gap": (
                "directed proton-transfer/electron-flow edges and row-specific "
                "bond-change mapping are not inferred here"
            ),
            "next_action": (
                "Use this sidecar as a train/cal-only feature source in a future "
                "mechanism-feature embedding pilot; do not train on heldout rows."
            ),
        },
        "source_artifacts": {
            "label_manifest": _source_path_record(label_manifest_path),
            "graph": _source_path_record(graph_path),
        },
    }


def _render_mechanism_feature_active_site_role_graph_sidecar_report(
    audit: dict[str, Any],
) -> str:
    counts = audit["counts"]
    lines = [
        "# Mechanism Feature Active-Site Role Graph Sidecar - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Manifest rows: {counts['manifest_rows']}",
        f"- Rows with ok role graph: {counts['rows_with_ok_role_graph']}",
        f"- Rows by status: {counts['rows_by_status']}",
        f"- Unique roles: {counts['unique_roles']}",
        f"- Unique role co-occurrence edges: {counts['unique_role_edges']}",
        "",
        "## Top Roles",
        "",
    ]
    for role, count in counts["top_roles"]:
        lines.append(f"- {role}: {count}")
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['embedding_gap_closed']}",
        f"- {audit['interpretation']['remaining_gap']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_mechanism_feature_active_site_role_graph_sidecar(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_feature_active_site_role_graph_sidecar(
        label_manifest_path=label_manifest_path,
        graph_path=graph_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_mechanism_feature_active_site_role_graph_sidecar_report(audit),
            encoding="utf-8",
        )
    return audit


def build_mechanism_feature_reaction_center_template_sidecar(
    *,
    label_manifest_path: Path,
    mechanism_fingerprints_path: Path,
) -> dict[str, Any]:
    manifest = _read_json(label_manifest_path)
    fingerprints = _read_json(mechanism_fingerprints_path)
    fingerprints_by_id = {
        str(fp.get("id")): fp
        for fp in fingerprints
        if isinstance(fp, dict) and fp.get("id")
    }
    manifest_rows = [
        row for row in manifest.get("rows", []) if isinstance(row, dict)
    ]
    sidecar_rows = []
    operation_counter: Counter[str] = Counter()
    bond_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    split_status_counter: Counter[str] = Counter()
    for row in manifest_rows:
        fp_id = row.get("fingerprint_id") or row.get("mechanism_fingerprint_id")
        fp = fingerprints_by_id.get(str(fp_id)) if fp_id else None
        if fp:
            reaction_center = fp.get("reaction_center") or {}
            operation = reaction_center.get("chemical_operation")
            bond_changes = reaction_center.get("bond_changes") or []
            cofactors = fp.get("cofactors") or []
            status = "template_available"
            if operation:
                operation_counter[_normalize_feature_token(operation)] += 1
            bond_counter.update(
                token
                for token in (_normalize_feature_token(item) for item in bond_changes)
                if token
            )
        elif fp_id:
            operation = None
            bond_changes = []
            cofactors = []
            status = "fingerprint_template_missing"
        else:
            operation = None
            bond_changes = []
            cofactors = []
            status = "no_mechanism_fingerprint_oos_or_unlabeled"
        status_counter[status] += 1
        split_status_counter[f"{row.get('split_assignment') or 'unknown'}::{status}"] += 1
        sidecar_rows.append(
            {
                "entry_id": row.get("entry_id"),
                "accession": row.get("accession") or row.get("sequence_id"),
                "split_assignment": row.get("split_assignment"),
                "benchmark_role": row.get("benchmark_role"),
                "label_type": row.get("label_type"),
                "fingerprint_id": fp_id,
                "status": status,
                "reaction_center_template": {
                    "chemical_operation": operation,
                    "chemical_operation_normalized": (
                        _normalize_feature_token(operation) if operation else None
                    ),
                    "bond_changes": bond_changes,
                    "bond_changes_normalized": [
                        token
                        for token in (
                            _normalize_feature_token(item) for item in bond_changes
                        )
                        if token
                    ],
                    "cofactors": cofactors,
                    "active_site_signature_roles": [
                        item.get("role")
                        for item in ((fp or {}).get("active_site_signature") or [])
                    ],
                },
            }
        )
    return {
        "artifact_id": "v3_mechanism_feature_reaction_center_template_sidecar_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "reaction_center_template_sidecar_ready",
        "scope": (
            "Row-level fingerprint-template reaction-center sidecar for "
            "mechanism-feature embedding readiness; not row-specific reaction evidence."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "model_weights_fit_or_refit": False,
            "heldout_threshold_tuning_for_deployment": False,
            "template_features_only_not_row_specific_bond_evidence": True,
        },
        "counts": {
            "manifest_rows": len(manifest_rows),
            "rows_by_status": dict(sorted(status_counter.items())),
            "rows_with_template": status_counter.get("template_available", 0),
            "unique_chemical_operations": len(operation_counter),
            "unique_bond_change_templates": len(bond_counter),
            "chemical_operation_counts": dict(sorted(operation_counter.items())),
            "bond_change_counts": dict(sorted(bond_counter.items())),
            "split_status_counts": dict(sorted(split_status_counter.items())),
        },
        "rows": sidecar_rows,
        "interpretation": {
            "embedding_gap_partially_closed": "fingerprint_template_reaction_center_descriptors_are_row_aligned",
            "remaining_gap": "row-specific source-backed Rhea/M-CSA bond-change sidecar is still missing",
            "next_action": (
                "Use only train/cal rows for any future embedding pilot and add "
                "row-specific bond-change evidence before claiming mechanism-level supervision."
            ),
        },
        "source_artifacts": {
            "label_manifest": _source_path_record(label_manifest_path),
            "mechanism_fingerprints": _source_path_record(mechanism_fingerprints_path),
        },
    }


def _render_mechanism_feature_reaction_center_template_sidecar_report(
    audit: dict[str, Any],
) -> str:
    counts = audit["counts"]
    lines = [
        "# Mechanism Feature Reaction-Center Template Sidecar - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Rows with template: {counts['rows_with_template']} / {counts['manifest_rows']}",
        f"- Rows by status: {counts['rows_by_status']}",
        f"- Unique chemical operations: {counts['unique_chemical_operations']}",
        f"- Unique bond-change templates: {counts['unique_bond_change_templates']}",
        "",
        "## Chemical Operations",
        "",
    ]
    for key, count in counts["chemical_operation_counts"].items():
        lines.append(f"- {key}: {count}")
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['embedding_gap_partially_closed']}",
        f"- {audit['interpretation']['remaining_gap']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_mechanism_feature_reaction_center_template_sidecar(
    *,
    label_manifest_path: Path,
    mechanism_fingerprints_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_mechanism_feature_reaction_center_template_sidecar(
        label_manifest_path=label_manifest_path,
        mechanism_fingerprints_path=mechanism_fingerprints_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_mechanism_feature_reaction_center_template_sidecar_report(audit),
            encoding="utf-8",
        )
    return audit


def _feature_flags_for_fingerprint(fp: dict[str, Any]) -> dict[str, Any]:
    fp_id = fp["id"]
    cofs = [str(c).lower() for c in fp.get("cofactors", [])]
    operation = str(fp.get("reaction_center", {}).get("chemical_operation", "")).lower()
    bond_changes = " ".join(fp.get("reaction_center", {}).get("bond_changes", [])).lower()
    roles = [r.get("role") for r in fp.get("active_site_signature", [])]
    text = " ".join(cofs + [operation, bond_changes, " ".join(roles)]).lower()
    return {
        "fingerprint_id": fp_id,
        "electron_flow_class": (
            "radical" if "radical" in text else
            "redox_or_electron_transfer" if any(x in text for x in ("redox", "electron", "hydride", "oxid")) else
            "nucleophilic_or_polar"
        ),
        "transition_state_stabilization_role_present": any(
            any(tok in str(role).lower() for tok in ("stabilizer", "oxyanion", "metal", "phosphate"))
            for role in roles
        ) or any("stabil" in f.lower() for f in fp.get("evidence_features", [])),
        "proton_transfer_connectivity_present": any(
            any(tok in str(role).lower() for tok in ("acid", "base", "water_activator", "redox_acid_base"))
            for role in roles
        ),
        "bond_making_breaking_descriptor": fp.get("reaction_center", {}).get("bond_changes", []),
        "cofactor_catalytic_locus": fp.get("cofactors", []),
        "metal_flag": any(x in text for x in ("zn", "mg", "mn", "fe2", "fe3", "metal")),
        "covalent_flag": any(x in text for x in ("covalent", "aldimine", "acyl", "nucleophil")),
        "radical_flag": "radical" in text,
        "active_site_residue_role_graph_available": bool(fp.get("active_site_signature")),
        "active_site_roles": roles,
    }


def build_learned_mechanism_feature_embedding_plan(
    *,
    mechanism_fingerprints_path: Path,
    label_manifest_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    predicted_geometry_atlas_path: Path,
    active_site_role_graph_sidecar_path: Path | None = None,
    reaction_center_template_sidecar_path: Path | None = None,
) -> dict[str, Any]:
    fingerprints = _read_json(mechanism_fingerprints_path)
    manifest = _read_json(label_manifest_path)
    cofactor = _read_json(selected_organic_cofactor_sidecar_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)
    active_site_role_graph = (
        _read_json(active_site_role_graph_sidecar_path)
        if active_site_role_graph_sidecar_path is not None
        and Path(active_site_role_graph_sidecar_path).exists()
        else {}
    )
    reaction_center_template = (
        _read_json(reaction_center_template_sidecar_path)
        if reaction_center_template_sidecar_path is not None
        and Path(reaction_center_template_sidecar_path).exists()
        else {}
    )

    rows = manifest.get("labels") or manifest.get("rows") or manifest.get("records") or []
    row_counts = Counter(
        row.get("fingerprint_id") or row.get("true_fingerprint_id") or row.get("mechanism_fingerprint_id")
        for row in rows
        if row.get("split_assignment") in {"train", "calibration", "in_distribution", "heldout"}
    )
    split_counts = Counter(row.get("split_assignment") for row in rows)
    feature_rows = [_feature_flags_for_fingerprint(fp) for fp in fingerprints]
    feature_coverage = {
        "fingerprints_total": len(fingerprints),
        "electron_flow_class": sum(1 for r in feature_rows if r["electron_flow_class"]),
        "transition_state_stabilization_role_present": sum(
            1 for r in feature_rows if r["transition_state_stabilization_role_present"]
        ),
        "proton_transfer_connectivity_present": sum(
            1 for r in feature_rows if r["proton_transfer_connectivity_present"]
        ),
        "bond_making_breaking_descriptor": sum(
            1 for r in feature_rows if r["bond_making_breaking_descriptor"]
        ),
        "cofactor_catalytic_locus": sum(1 for r in feature_rows if r["cofactor_catalytic_locus"]),
        "metal_covalent_radical_flags": sum(
            1 for r in feature_rows
            if r["metal_flag"] or r["covalent_flag"] or r["radical_flag"]
        ),
        "active_site_residue_role_graph_available": sum(
            1 for r in feature_rows if r["active_site_residue_role_graph_available"]
        ),
    }
    primary_fps = [
        fp["fingerprint_id"]
        for fp in feature_rows
        if fp["fingerprint_id"] not in {
            "radical_sam_enzyme",
            "cobalamin_radical_rearrangement",
            "flavin_monooxygenase",
        }
    ]
    row_class_records = cofactor.get("row_class_records", [])
    atlas_counts = predicted_atlas.get("counts", {})

    return {
        "artifact_id": "v3_learned_mechanism_feature_embedding_plan_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "scaffold_ready_train_cal_pilot_deferred_until_row_level_feature_extraction",
        "scope": (
            "Leakage-safe learned mechanism-feature embedding scaffold for the "
            "D11 continuous mechanism-space target. This is a spec plus coverage "
            "audit, not a heldout-trained or threshold-tuned model."
        ),
        "guardrails": {
            "heldout_labels_used_for_training_or_threshold_tuning": False,
            "labels_registries_ontologies_changed": False,
            "production_thresholds_changed": False,
            "imports_or_promotions_performed": False,
            "evaluation_target": "operating_point_novelty_abstention_and_relationship_eval",
        },
        "available_feature_spec": {
            "fingerprint_level_features": feature_rows,
            "feature_coverage": feature_coverage,
            "primary_fingerprint_ids": sorted(primary_fps),
            "secondary_or_probe_fingerprint_ids": sorted(set(r["fingerprint_id"] for r in feature_rows) - set(primary_fps)),
        },
        "pilot_design": {
            "trainable_rows": "train/calibration or current702 in_distribution rows only",
            "forbidden_training_rows": "heldout and OOS rows",
            "input_blocks": [
                "fingerprint-level mechanism chemistry template",
                "sequence-only ESM2 embedding or frozen PLM surface",
                "sequence-only organic cofactor scores when available",
                "predicted-geometry role decomposition for atlas rows when available",
            ],
            "output_head": (
                "small supervised or metric-learning projection trained only on "
                "train/cal rows; calibrate abstention on calibration/in-distribution "
                "atlas statistics, then evaluate heldout once"
            ),
            "required_metrics": [
                "operating-point OOS abstain recall at >=90% and >=85% in-scope retention",
                "cofactor-confounded OOS abstain recall",
                "relationship-rank hygiene: same-chemistry unrelated-fold near; same-fold different-chemistry far",
                "no OOS false positives at the selected operating point",
            ],
        },
        "current_data_readiness": {
            "manifest_split_counts": dict(sorted(split_counts.items())),
            "fingerprint_row_counts_raw": {
                str(k): v for k, v in sorted((k, v) for k, v in row_counts.items() if k)
            },
            "row_level_selected_organic_cofactor_records": len(row_class_records),
            "predicted_geometry_atlas_status": predicted_atlas.get("status"),
            "predicted_geometry_atlas_counts": atlas_counts,
            "active_site_role_graph_sidecar": {
                "status": active_site_role_graph.get("status"),
                "rows_with_ok_role_graph": active_site_role_graph.get("counts", {}).get(
                    "rows_with_ok_role_graph"
                ),
                "unique_roles": active_site_role_graph.get("counts", {}).get("unique_roles"),
                "unique_role_edges": active_site_role_graph.get("counts", {}).get(
                    "unique_role_edges"
                ),
            },
            "reaction_center_template_sidecar": {
                "status": reaction_center_template.get("status"),
                "rows_with_template": reaction_center_template.get("counts", {}).get(
                    "rows_with_template"
                ),
                "unique_chemical_operations": reaction_center_template.get("counts", {}).get(
                    "unique_chemical_operations"
                ),
                "unique_bond_change_templates": reaction_center_template.get("counts", {}).get(
                    "unique_bond_change_templates"
                ),
            },
        },
        "feature_extraction_gaps": [
            {
                "feature": "row_level_electron_flow_class",
                "gap": "available only as fingerprint-level template, not row-level evidence",
                "next_action": "derive row-level labels/features from curated reaction center plus active-site roles for train/cal rows only",
            },
            {
                "feature": "transition_state_stabilization_role",
                "gap": "row-level role graph vocabulary exists, but directed transition-state/proton/electron-flow edges are not inferred",
                "next_action": "consume the role graph sidecar on train/cal rows only, then add directed mechanism-edge features",
            },
            {
                "feature": "proton_transfer_connectivity",
                "gap": "acid/base roles present but no directed donor/acceptor connectivity sidecar",
                "next_action": "extract directed role edges from geometry feature rows where residue mappings exist",
            },
            {
                "feature": "bond_making_breaking",
                "gap": "fingerprint-template reaction-center descriptors are row-aligned, but row-specific Rhea/M-CSA bond-change mapping is not normalized here",
                "next_action": "build a source-backed row-specific bond-change sidecar before any supervised pilot",
            },
            {
                "feature": "cofactor_catalytic_locus",
                "gap": "row-level organic cofactor scores exist for flavin/heme/PLP, but metal/cobalamin/radical/Fe-S loci are incomplete",
                "next_action": "persist row-level metal/cobalamin/radical/Fe-S sidecars or mark unsupported classes as missing",
            },
        ],
        "next_unblocked_command": (
            "PYTHONPATH=src python -m catalytic_earth.cli "
            "build-learned-mechanism-feature-embedding-plan"
        ),
        "source_artifacts": {
            "mechanism_fingerprints": {
                "path": str(mechanism_fingerprints_path),
                "sha256": _sha256(mechanism_fingerprints_path),
            },
            "label_manifest": {
                "path": str(label_manifest_path),
                "sha256": _sha256(label_manifest_path),
            },
            "selected_organic_cofactor_sidecar": {
                "path": str(selected_organic_cofactor_sidecar_path),
                "sha256": _sha256(selected_organic_cofactor_sidecar_path),
            },
            "predicted_geometry_atlas": {
                "path": str(predicted_geometry_atlas_path),
                "sha256": _sha256(predicted_geometry_atlas_path),
            },
            "active_site_role_graph_sidecar": (
                _source_path_record(active_site_role_graph_sidecar_path)
                if active_site_role_graph_sidecar_path is not None
                else None
            ),
            "reaction_center_template_sidecar": (
                _source_path_record(reaction_center_template_sidecar_path)
                if reaction_center_template_sidecar_path is not None
                else None
            ),
        },
    }


def _render_embedding_plan_report(audit: dict[str, Any]) -> str:
    cov = audit["available_feature_spec"]["feature_coverage"]
    lines = [
        "# Learned Mechanism-Feature Embedding Plan - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        "- No heldout labels were used for training, calibration, or threshold tuning.",
        "",
        "## Feature Coverage",
        "",
    ]
    for key, value in cov.items():
        lines.append(f"- {key}: {value}")
    lines += [
        "",
        "## Pilot Design",
        "",
        f"- Trainable rows: {audit['pilot_design']['trainable_rows']}",
        f"- Forbidden rows: {audit['pilot_design']['forbidden_training_rows']}",
        "- Evaluation target: operating-point novelty/abstention and relationship eval, not only AUC.",
        "",
        "## Row-Level Sidecars",
        "",
        f"- Active-site role graph: {audit['current_data_readiness']['active_site_role_graph_sidecar']}",
        f"- Reaction-center template: {audit['current_data_readiness']['reaction_center_template_sidecar']}",
        "",
        "## Extraction Gaps",
        "",
    ]
    for gap in audit["feature_extraction_gaps"]:
        lines.append(f"- {gap['feature']}: {gap['gap']} Next: {gap['next_action']}.")
    return "\n".join(lines) + "\n"


def write_learned_mechanism_feature_embedding_plan(
    *,
    mechanism_fingerprints_path: Path,
    label_manifest_path: Path,
    selected_organic_cofactor_sidecar_path: Path,
    predicted_geometry_atlas_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    active_site_role_graph_sidecar_path: Path | None = None,
    reaction_center_template_sidecar_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_learned_mechanism_feature_embedding_plan(
        mechanism_fingerprints_path=mechanism_fingerprints_path,
        label_manifest_path=label_manifest_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
        active_site_role_graph_sidecar_path=active_site_role_graph_sidecar_path,
        reaction_center_template_sidecar_path=reaction_center_template_sidecar_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_embedding_plan_report(audit), encoding="utf-8")
    return audit


def build_family_set_expansion_targets(
    *,
    prior_expansion_path: Path,
    prediction_contract_path: Path,
) -> dict[str, Any]:
    prior = _read_json(prior_expansion_path)
    contract = _read_json(prediction_contract_path)
    secondary = contract.get("secondary_probe_fingerprints", {})
    targets = [
        {
            "candidate_family": "glycyl_radical_or_thiamine_radical_lyase_boundary",
            "priority_bins": ["cofactor_confounded_oos", "near_orphan", "dark_bin"],
            "candidate_rows": ["m_csa:30", "m_csa:31"],
            "candidate_sources": ["M-CSA current heldout canaries", "Swiss-Prot radical enzyme reviews", "Rhea radical C-C bond cleavage reactions"],
            "expected_eval_bin_impact": "adds confounded-OOS controls that reuse known cofactors but should abstain from occupied hydrolase/redox families",
            "required_human_validation": "expert decision on exact radical/cofactor locus and whether rows remain OOS controls or seed a future family",
        },
        {
            "candidate_family": "thiol_disulfide_oxidoreductase_isomerase_boundary",
            "priority_bins": ["cofactor_confounded_oos", "FMO_flavin_redox_boundary"],
            "candidate_rows": ["m_csa:191"],
            "candidate_sources": ["M-CSA disulfide-isomerase row", "Swiss-Prot protein disulfide-isomerase family", "Rhea thiol-disulfide interchange reactions"],
            "expected_eval_bin_impact": "tests redox chemistry that can look cofactor-like without matching flavin/heme occupied loci",
            "required_human_validation": "confirm row-level bond-change and redox partner before any countable label",
        },
        {
            "candidate_family": "lipoamide_or_sulfur_transfer_redox_boundary",
            "priority_bins": ["cofactor_confounded_oos", "radical_cobalamin_FeS"],
            "candidate_rows": ["m_csa:267", "m_csa:448"],
            "candidate_sources": ["M-CSA current heldout canaries", "Swiss-Prot lipoamide/sulfur-transfer enzymes", "Rhea sulfur-transfer/redox reactions"],
            "expected_eval_bin_impact": "adds hard OOS controls for known-cofactor leakage and Fe-S/sulfur chemistry",
            "required_human_validation": "expert review of catalytic locus and cofactor identity; keep review-only until duplicate and split gates pass",
        },
        {
            "candidate_family": "flavin_monooxygenase_and_flavin_oxygen_transfer",
            "priority_bins": ["FMO_flavin_redox_boundary", "near_orphan", "no_reliable_structure"],
            "candidate_rows": ["m_csa:131", "m_csa:132", "m_csa:551", "m_csa:973"],
            "candidate_sources": ["M-CSA FMO-like rows", "Swiss-Prot FMO/BVMO reviewed proteins", "Rhea oxygen insertion and Baeyer-Villiger reactions"],
            "expected_eval_bin_impact": "separates flavin oxygen-transfer from flavin dehydrogenase/reductase without promoting FMO prematurely",
            "required_human_validation": "subtype panel, hard-negative separation, ligand/coordinate materialization, and expert admission decision",
        },
        {
            "candidate_family": "cobalamin_and_radical_rearrangement_panel",
            "priority_bins": ["radical_cobalamin_FeS", "dark_bin", "no_reliable_structure"],
            "candidate_rows": ["secondary_probe::cobalamin_radical_rearrangement", "secondary_probe::radical_sam_enzyme", "m_csa:750"],
            "candidate_sources": ["existing secondary probe definitions", "Swiss-Prot B12/radical-SAM reviewed families", "Rhea radical rearrangement reactions"],
            "expected_eval_bin_impact": "widens the 8-fingerprint bound into radical/cobalamin/Fe-S chemistry where current labels are sparse",
            "required_human_validation": "keep current probes secondary until enough support exists; m_csa:750 remains OOS/boundary under current decision log",
        },
        {
            "candidate_family": "no_reliable_structure_metal_hydrolase_controls",
            "priority_bins": ["no_reliable_structure", "dark_bin"],
            "candidate_rows": ["mh_064", "mh_065", "mh_066", "mh_067", "mh_068", "mh_072"],
            "candidate_sources": ["prior targeted expansion proposal", "Swiss-Prot metal hydrolase candidates", "Rhea hydrolysis reactions with metal cofactors"],
            "expected_eval_bin_impact": "increases no_reliable_structure positive and hard-negative support without padding dense structural neighborhoods",
            "required_human_validation": "external duplicate screen, Foldseek/TM screen, geometry materialization, expert review, label-factory gates, future frozen split",
        },
        {
            "candidate_family": "near_orphan_glycoside_or_nucleoside_hydrolase_controls",
            "priority_bins": ["near_orphan", "confounded_OOS", "dark_bin"],
            "candidate_rows": ["m_csa:10", "m_csa:116", "mh_073", "external_glycoside_panel"],
            "candidate_sources": ["prior targeted expansion proposal", "external glycoside/carbohydrate panel", "Rhea glycosidic bond hydrolysis reactions"],
            "expected_eval_bin_impact": "adds near-orphan OOS controls that stress hydrolase boundary calls without dense-neighborhood padding",
            "required_human_validation": "source-backed substrate/bond-change adjudication and strict no-training use for current heldout canaries",
        },
    ]
    bin_counts = Counter(bin_name for t in targets for bin_name in t["priority_bins"])
    return {
        "artifact_id": "v3_family_set_expansion_targets_current702_20260601",
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "proposal_only_no_imports",
        "scope": (
            "Targeted family-set expansion proposal to de-risk the current "
            "8-fingerprint bound by increasing no_reliable_structure, near_orphan, "
            "confounded-OOS, FMO/flavin-redox boundary, radical/cobalamin/Fe-S, "
            "and dark-bin support without padding dense structural neighborhoods."
        ),
        "guardrails": {
            "labels_edited": False,
            "registries_edited": False,
            "ontologies_edited": False,
            "imports_or_promotions_performed": False,
            "heldout_splits_changed": False,
            "proposal_only": True,
        },
        "target_summary": {
            "candidate_family_count": len(targets),
            "priority_bin_coverage": dict(sorted(bin_counts.items())),
            "prior_smallest_batch_size": len(prior.get("smallest_next_acquisition_batch", [])),
            "secondary_probe_fingerprints_in_contract": sorted(secondary) if isinstance(secondary, dict) else secondary,
        },
        "candidate_families": targets,
        "global_human_validation_required": [
            "expert mechanism-locus review",
            "source-backed M-CSA/Swiss-Prot/Rhea provenance",
            "duplicate and train/test leakage screen",
            "coordinate or predicted-structure materialization feasibility",
            "label-factory gate and future frozen split before any countable use",
        ],
        "source_artifacts": {
            "prior_targeted_expansion_proposal": {
                "path": str(prior_expansion_path),
                "sha256": _sha256(prior_expansion_path),
            },
            "mechanism_prediction_contract": {
                "path": str(prediction_contract_path),
                "sha256": _sha256(prediction_contract_path),
            },
        },
    }


def _render_family_expansion_report(audit: dict[str, Any]) -> str:
    lines = [
        "# Family-Set Expansion Targets - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Guardrails",
        "",
        "- Proposal only. No labels, registries, ontologies, imports, promotions, thresholds, or heldout splits changed.",
        "",
        "## Target Families",
        "",
        "| Family | Priority bins | Candidate rows | Expected eval impact |",
        "| --- | --- | --- | --- |",
    ]
    for item in audit["candidate_families"]:
        lines.append(
            f"| {item['candidate_family']} | {', '.join(item['priority_bins'])} | "
            f"{', '.join(item['candidate_rows'])} | {item['expected_eval_bin_impact']} |"
        )
    lines += [
        "",
        "## Human Validation",
        "",
    ]
    for item in audit["global_human_validation_required"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_family_set_expansion_targets(
    *,
    prior_expansion_path: Path,
    prediction_contract_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_family_set_expansion_targets(
        prior_expansion_path=prior_expansion_path,
        prediction_contract_path=prediction_contract_path,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_render_family_expansion_report(audit), encoding="utf-8")
    return audit
