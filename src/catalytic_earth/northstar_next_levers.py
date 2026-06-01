"""Bounded D11/northstar next-lever artifacts.

These writers are intentionally conservative: they read frozen/current702-safe
sidecars, produce reproducible JSON plus reports, and do not edit labels,
registries, ontologies, thresholds, imports, splits, or model weights.
"""

from __future__ import annotations

import hashlib
import json
import math
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

SCHEMA_VERSION = "northstar_next_levers.v0"


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
) -> dict[str, Any]:
    fingerprints = _read_json(mechanism_fingerprints_path)
    manifest = _read_json(label_manifest_path)
    cofactor = _read_json(selected_organic_cofactor_sidecar_path)
    predicted_atlas = _read_json(predicted_geometry_atlas_path)

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
        },
        "feature_extraction_gaps": [
            {
                "feature": "row_level_electron_flow_class",
                "gap": "available only as fingerprint-level template, not row-level evidence",
                "next_action": "derive row-level labels/features from curated reaction center plus active-site roles for train/cal rows only",
            },
            {
                "feature": "transition_state_stabilization_role",
                "gap": "role text exists in fingerprints but not as normalized row-level graph edges",
                "next_action": "normalize active_site_signature roles into residue-role graph vocabulary",
            },
            {
                "feature": "proton_transfer_connectivity",
                "gap": "acid/base roles present but no directed donor/acceptor connectivity sidecar",
                "next_action": "extract directed role edges from geometry feature rows where residue mappings exist",
            },
            {
                "feature": "bond_making_breaking",
                "gap": "fingerprint reaction-center descriptors exist; row-specific Rhea/M-CSA bond-change mapping is not normalized here",
                "next_action": "build a source-backed bond-change sidecar before any supervised pilot",
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
) -> dict[str, Any]:
    audit = build_learned_mechanism_feature_embedding_plan(
        mechanism_fingerprints_path=mechanism_fingerprints_path,
        label_manifest_path=label_manifest_path,
        selected_organic_cofactor_sidecar_path=selected_organic_cofactor_sidecar_path,
        predicted_geometry_atlas_path=predicted_geometry_atlas_path,
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
