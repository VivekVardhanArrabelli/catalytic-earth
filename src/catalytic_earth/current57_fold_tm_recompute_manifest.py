"""Input manifest for recomputing Fold/TM on current-57 train/cal rows."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CURRENT57_OPERATING_POINT_PATH = (
    "artifacts/"
    "v3_cofactor_fusion_operating_point_train_cal_oos_current702_"
    "20260628_current57_rerun.json"
)
DEFAULT_LABEL_MANIFEST_PATH = "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
DEFAULT_COORDINATE_ROOT = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/current57_fold_tm_recompute_input_manifest_current702_20260628.md"
)

TRAIN_CAL_SAFE_DIRS: tuple[str, ...] = (
    "confounded_proxy_train_cal_tranche_queries",
    "atlas_in_distribution",
)
HELDOUT_EXCLUDED_DIRS: tuple[str, ...] = (
    "queries_all_heldout",
    "queries_cofactor_confounded_oos",
)


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


def _label_rows_by_entry(label_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("entry_id")): row
        for row in label_manifest.get("rows", []) or []
        if row.get("entry_id")
    }


def _accessions(label_row: dict[str, Any]) -> list[str]:
    values = []
    if label_row.get("sequence_id"):
        values.append(label_row["sequence_id"])
    values.extend(label_row.get("real_sequence_accessions") or [])
    return list(dict.fromkeys(str(value) for value in values if value))


def _current_rows(
    current57_operating_point: dict[str, Any], *, split: str, row_class: str
) -> list[dict[str, Any]]:
    details = current57_operating_point.get("row_details_by_split", {}).get(split, {})
    key = "inscope_rows" if row_class == "inscope" else "oos_rows"
    return list(details.get(key, []) or [])


def _find_cif(accessions: list[str], coordinate_root: Path) -> dict[str, Any]:
    searched = []
    for accession in accessions:
        for dirname in TRAIN_CAL_SAFE_DIRS:
            path = coordinate_root / dirname / f"afdb_{accession}_v6.cif"
            searched.append(str(path))
            if path.exists():
                return {
                    "status": "staged_train_cal_safe_cif_found",
                    "accession": accession,
                    "source_cif_path": str(path),
                    "source_coordinate_dir": dirname,
                    "searched_paths": searched,
                }
    return {
        "status": "missing_train_cal_safe_cif",
        "accession": accessions[0] if accessions else None,
        "source_cif_path": None,
        "source_coordinate_dir": None,
        "searched_paths": searched,
    }


def _manifest_row(
    *,
    row: dict[str, Any],
    label_rows: dict[str, dict[str, Any]],
    coordinate_root: Path,
    split: str,
    row_class: str,
    role: str,
    staging_dir: str,
) -> dict[str, Any]:
    entry_id = str(row.get("entry_id"))
    label_row = label_rows.get(entry_id, {})
    accessions = _accessions(label_row)
    cif = _find_cif(accessions, coordinate_root)
    accession = cif.get("accession")
    expected_name = f"afdb_{accession}_v6.cif" if accession else None
    return {
        "entry_id": entry_id,
        "split": split,
        "row_class": row_class,
        "role": role,
        "label_type": label_row.get("label_type"),
        "true_fingerprint_id": row.get("true_fingerprint_id"),
        "current57_fused_top1_fingerprint_id": row.get("fused", {}).get(
            "top1_fingerprint_id"
        ),
        "current57_fused_top1_score": row.get("fused", {}).get("top1_score"),
        "accession_candidates": accessions,
        **cif,
        "expected_staged_path": str(Path(staging_dir) / expected_name)
        if expected_name
        else None,
    }


def _rows_for_role(
    *,
    current57_operating_point: dict[str, Any],
    label_rows: dict[str, dict[str, Any]],
    coordinate_root: Path,
    split: str,
    row_class: str,
    role: str,
    staging_dir: str,
) -> list[dict[str, Any]]:
    return [
        _manifest_row(
            row=row,
            label_rows=label_rows,
            coordinate_root=coordinate_root,
            split=split,
            row_class=row_class,
            role=role,
            staging_dir=staging_dir,
        )
        for row in _current_rows(
            current57_operating_point, split=split, row_class=row_class
        )
    ]


def _coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    missing = [
        row["entry_id"]
        for row in rows
        if row.get("status") != "staged_train_cal_safe_cif_found"
    ]
    unsafe = [
        row["entry_id"]
        for row in rows
        if row.get("source_coordinate_dir") in HELDOUT_EXCLUDED_DIRS
    ]
    return {
        "rows": len(rows),
        "staged_train_cal_safe_cif_found": len(rows) - len(missing),
        "missing_train_cal_safe_cif": len(missing),
        "missing_entry_ids": missing,
        "heldout_excluded_dir_hits": len(unsafe),
        "heldout_excluded_entry_ids": unsafe,
    }


def _foldseek_command(*, query_dir: str, target_dir: str, result_root: str) -> str:
    return (
        "foldseek easy-search "
        f"{query_dir} {target_dir} "
        f"{result_root}/calibration_vs_current57_train_atlas.tsv "
        f"{result_root}/tmp_calibration_vs_current57_train_atlas "
        "--format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits "
        "--exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 "
        "--exact-tmscore 1 --threads 4 -v 1"
    )


def build_current57_fold_tm_recompute_manifest(
    *,
    current57_operating_point: dict[str, Any],
    label_manifest: dict[str, Any],
    coordinate_root: Path,
    staging_root: str = (
        "artifacts/v3_current57_fold_tm_recompute_current702_20260628_coordinates"
    ),
    result_root: str = (
        "artifacts/v3_current57_fold_tm_recompute_current702_20260628_results"
    ),
) -> dict[str, Any]:
    labels = _label_rows_by_entry(label_manifest)
    calibration_query_dir = str(Path(staging_root) / "calibration_queries")
    train_target_dir = str(Path(staging_root) / "train_in_scope_atlas")
    train_reference_query_dir = str(Path(staging_root) / "train_reference_queries")

    calibration_queries = (
        _rows_for_role(
            current57_operating_point=current57_operating_point,
            label_rows=labels,
            coordinate_root=coordinate_root,
            split="calibration",
            row_class="inscope",
            role="calibration_query_in_scope_primary",
            staging_dir=calibration_query_dir,
        )
        + _rows_for_role(
            current57_operating_point=current57_operating_point,
            label_rows=labels,
            coordinate_root=coordinate_root,
            split="calibration",
            row_class="oos",
            role="calibration_query_oos_negative",
            staging_dir=calibration_query_dir,
        )
    )
    train_targets = _rows_for_role(
        current57_operating_point=current57_operating_point,
        label_rows=labels,
        coordinate_root=coordinate_root,
        split="train",
        row_class="inscope",
        role="train_in_scope_fold_target",
        staging_dir=train_target_dir,
    )
    train_reference_queries = (
        _rows_for_role(
            current57_operating_point=current57_operating_point,
            label_rows=labels,
            coordinate_root=coordinate_root,
            split="train",
            row_class="inscope",
            role="train_reference_query_in_scope_self_exclusion_required",
            staging_dir=train_reference_query_dir,
        )
        + _rows_for_role(
            current57_operating_point=current57_operating_point,
            label_rows=labels,
            coordinate_root=coordinate_root,
            split="train",
            row_class="oos",
            role="train_reference_query_oos_negative",
            staging_dir=train_reference_query_dir,
        )
    )

    coverage = {
        "calibration_queries": _coverage(calibration_queries),
        "train_in_scope_targets": _coverage(train_targets),
        "train_reference_queries": _coverage(train_reference_queries),
    }
    ready = (
        coverage["calibration_queries"]["missing_train_cal_safe_cif"] == 0
        and coverage["train_in_scope_targets"]["missing_train_cal_safe_cif"] == 0
        and coverage["calibration_queries"]["heldout_excluded_dir_hits"] == 0
        and coverage["train_in_scope_targets"]["heldout_excluded_dir_hits"] == 0
    )
    return {
        "artifact_id": "v3_current57_fold_tm_recompute_input_manifest_current702_20260628",
        "schema_version": "current57_fold_tm_recompute_input_manifest.v1",
        "created_utc": _utc_now_iso(),
        "status": (
            "current57_fold_tm_recompute_input_manifest_ready_foldseek_missing"
            if ready
            else "blocked_current57_fold_tm_recompute_input_manifest_missing_inputs"
        ),
        "result_class": (
            "heldout_excluded_fold_tm_recompute_input_manifest_no_new_scores"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "heldout_coordinate_dirs_excluded": list(HELDOUT_EXCLUDED_DIRS),
            "new_foldseek_or_tm_scores_computed": False,
            "production_threshold_changed": False,
            "model_weights_changed": False,
            "registry_or_ontology_changed": False,
            "fingerprint_family_growth": False,
        },
        "staging_plan": {
            "staging_root": staging_root,
            "calibration_query_dir": calibration_query_dir,
            "train_in_scope_target_dir": train_target_dir,
            "train_reference_query_dir": train_reference_query_dir,
            "materialization_rule": (
                "Symlink or copy each source_cif_path to expected_staged_path. "
                "Do not include queries_all_heldout or queries_cofactor_confounded_oos."
            ),
        },
        "foldseek_command": _foldseek_command(
            query_dir=calibration_query_dir,
            target_dir=train_target_dir,
            result_root=result_root,
        ),
        "coverage": coverage,
        "rows": {
            "calibration_queries": calibration_queries,
            "train_in_scope_targets": train_targets,
            "train_reference_queries": train_reference_queries,
        },
        "interpretation": {
            "headline": (
                "The exact current-57 calibration cofactor rows and train in-scope "
                "fold targets all have staged train/cal-safe CIFs; scoring remains "
                "blocked only by the missing foldseek executable."
                if ready
                else "Current-57 Fold/TM recompute inputs are incomplete."
            ),
            "next_action": (
                "Install/expose foldseek, materialize the staging plan, then run "
                "the recorded easy-search command before any cached atlas-engine "
                "fusion readout."
            ),
        },
    }


def _report(manifest: dict[str, Any]) -> str:
    coverage = manifest["coverage"]
    lines = [
        "# Current-57 Fold/TM Recompute Input Manifest",
        "",
        f"Run: {manifest['created_utc']}",
        f"Status: `{manifest['status']}`",
        "",
        "## Coverage",
        "",
        f"- Calibration queries: "
        f"{coverage['calibration_queries']['staged_train_cal_safe_cif_found']}/"
        f"{coverage['calibration_queries']['rows']} staged train/cal-safe CIFs.",
        f"- Train in-scope targets: "
        f"{coverage['train_in_scope_targets']['staged_train_cal_safe_cif_found']}/"
        f"{coverage['train_in_scope_targets']['rows']} staged train/cal-safe CIFs.",
        f"- Train reference queries: "
        f"{coverage['train_reference_queries']['staged_train_cal_safe_cif_found']}/"
        f"{coverage['train_reference_queries']['rows']} staged train/cal-safe CIFs.",
        "",
        "## Foldseek Command",
        "",
        f"```bash\n{manifest['foldseek_command']}\n```",
        "",
        "## Guardrails",
        "",
        "- No heldout rows were scored or read.",
        "- No new Foldseek/TM scores were computed by this manifest.",
        "- No production threshold, model weight, registry, ontology, label, or "
        "fingerprint-family change was made.",
    ]
    return "\n".join(lines) + "\n"


def write_current57_fold_tm_recompute_manifest(
    *,
    current57_operating_point_path: Path,
    label_manifest_path: Path,
    coordinate_root: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    current57 = _load_json(current57_operating_point_path)
    labels = _load_json(label_manifest_path)
    manifest = build_current57_fold_tm_recompute_manifest(
        current57_operating_point=current57,
        label_manifest=labels,
        coordinate_root=coordinate_root,
    )
    manifest["source_artifacts"] = {
        "current57_cofactor_operating_point": _artifact_summary(
            current57_operating_point_path, current57
        ),
        "label_manifest": _artifact_summary(label_manifest_path, labels),
        "coordinate_root": str(coordinate_root),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(manifest), encoding="utf-8")
    return manifest
