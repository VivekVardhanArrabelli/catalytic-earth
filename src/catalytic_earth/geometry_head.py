from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


PRIMARY_PREFIX = "primary_supervised_metric::"
SECONDARY_PREFIX = "secondary_ood_probe::"


def build_geometry_nonlinear_head_audit(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
    geometry_retrieval: dict[str, Any],
    wave1_audit: dict[str, Any] | None = None,
    random_state: int = 702,
    cal_fraction: float = 0.2,
    hidden_layer_size: int = 32,
) -> dict[str, Any]:
    """Train a fixed small MLP geometry head and evaluate heldout once.

    The train/cal split is made only from in-distribution rows. The classifier
    is fitted on train primary rows, while the abstention threshold is selected
    on calibration rows using nonprimary/OOS rows. Heldout rows are final-only.
    """
    try:
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:  # pragma: no cover - environment dependent
        return _blocked_audit(
            reason="sklearn_unavailable",
            detail=f"{type(exc).__name__}: {exc}",
            label_manifest=label_manifest,
        )

    import warnings

    manifest_rows = [
        row for row in label_manifest.get("rows", []) if isinstance(row, dict)
    ]
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in geometry_features.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    retrieval_by_entry = {
        str(row.get("entry_id")): row
        for row in geometry_retrieval.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    wave_masks = _wave_masks_by_entry(wave1_audit or {})

    model_rows: list[dict[str, Any]] = []
    missing_feature_rows: list[dict[str, str]] = []
    for row in manifest_rows:
        entry_id = str(row.get("entry_id") or "")
        geometry_row = geometry_by_entry.get(entry_id)
        retrieval_row = retrieval_by_entry.get(entry_id)
        if not entry_id:
            continue
        if geometry_row is None:
            missing_feature_rows.append(
                {
                    "entry_id": entry_id,
                    "reason": "geometry_features_missing",
                }
            )
            continue
        features = _geometry_feature_vector(geometry_row, retrieval_row or {})
        model_rows.append(
            {
                "entry_id": entry_id,
                "benchmark_role": row.get("benchmark_role"),
                "split_assignment": row.get("split_assignment"),
                "true_fingerprint_id": row.get("fingerprint_id")
                or row.get("mechanism_fingerprint_id"),
                "features": features,
                "structural_neighborhood_bin": (
                    wave_masks.get(entry_id, {}).get("structural_neighborhood_bin")
                    or "unbinned"
                ),
            }
        )

    in_distribution = [
        row for row in model_rows if row.get("split_assignment") == "in_distribution"
    ]
    heldout = [row for row in model_rows if row.get("split_assignment") == "heldout"]
    heldout_missing_ids = sorted(
        {
            str(row.get("entry_id"))
            for row in manifest_rows
            if row.get("split_assignment") == "heldout"
        }
        - {row["entry_id"] for row in heldout}
    )

    train_all, cal_rows = _split_train_cal(
        in_distribution,
        cal_fraction=cal_fraction,
        random_state=random_state,
        train_test_split=train_test_split,
    )
    train_primary = [row for row in train_all if _is_primary_role(row["benchmark_role"])]
    classes = sorted({str(row["true_fingerprint_id"]) for row in train_primary})
    if len(classes) < 2 or not train_primary or not cal_rows or not heldout:
        return _blocked_audit(
            reason="insufficient_rows_for_geometry_head",
            detail=(
                f"train_primary={len(train_primary)} cal={len(cal_rows)} "
                f"heldout={len(heldout)} classes={len(classes)}"
            ),
            label_manifest=label_manifest,
        )

    logistic = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=random_state),
    )
    mlp = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(hidden_layer_size,),
            activation="relu",
            alpha=0.001,
            max_iter=2000,
            random_state=random_state,
        ),
    )
    mlp_oos_aware = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(hidden_layer_size,),
            activation="relu",
            alpha=0.001,
            max_iter=2000,
            random_state=random_state,
        ),
    )

    train_x = [row["features"] for row in train_primary]
    train_y = [str(row["true_fingerprint_id"]) for row in train_primary]
    train_all_x = [row["features"] for row in train_all]
    train_all_y = [_training_label_with_none(row) for row in train_all]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        logistic.fit(train_x, train_y)
        mlp.fit(train_x, train_y)
        mlp_oos_aware.fit(train_all_x, train_all_y)

    logistic_result = _evaluate_head(
        track_id="geometry_feature_logistic_rerun",
        display_name="Geometry-feature logistic rerun",
        model=logistic,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
    )
    mlp_result = _evaluate_head(
        track_id="geometry_feature_mlp_32",
        display_name=f"Geometry-feature MLP-{hidden_layer_size}",
        model=mlp,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
    )
    mlp_oos_aware_result = _evaluate_head(
        track_id="geometry_feature_mlp_32_oos_aware",
        display_name=f"Geometry-feature OOS-aware MLP-{hidden_layer_size}",
        model=mlp_oos_aware,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
        abstain_class="__none_of_above__",
    )

    hand_metrics = (
        (wave1_audit or {})
        .get("geometry_baseline_reexport", {})
        .get("metrics_canonical_masks", {})
    )
    wave1_geometry_logistic_metrics = (
        (wave1_audit or {})
        .get("geometry_feature_logistic_head", {})
        .get("heldout_metrics", {})
    )
    hand_primary = hand_metrics.get("primary_accuracy_available")
    hand_oos = hand_metrics.get("oos_or_secondary_false_positive_rate_available")
    mlp_primary = mlp_oos_aware_result["heldout_metrics"][
        "primary_accuracy_available"
    ]
    logistic_primary = logistic_result["heldout_metrics"]["primary_accuracy_available"]
    wave1_geometry_logistic_primary = wave1_geometry_logistic_metrics.get(
        "primary_accuracy_available"
    )

    vectorizer = logistic.named_steps.get("dictvectorizer")
    feature_names = (
        list(vectorizer.get_feature_names_out())
        if hasattr(vectorizer, "get_feature_names_out")
        else []
    )
    return {
        "artifact_id": "v3_geometry_nonlinear_head_audit_702_20260529",
        "schema_version": "geometry_nonlinear_head_audit.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "large_downloads_performed": False,
        },
        "protocol": {
            "split_source": "frozen current702 split from label manifest",
            "train_rows": "in_distribution primary rows only",
            "calibration_rows": "in_distribution rows only; includes nonprimary/OOS for threshold selection",
            "threshold_policy": (
                "lowest max-probability threshold with zero nonprimary/OOS "
                "false positives on calibration rows; no heldout tuning"
            ),
            "heldout_policy": "heldout evaluated once after fit and calibration",
            "random_state": random_state,
            "cal_fraction": cal_fraction,
            "mlp_architecture": {
                "hidden_layer_sizes": [hidden_layer_size],
                "activation": "relu",
                "alpha": 0.001,
                "max_iter": 2000,
            },
        },
        "feature_source": {
            "description": (
                "label-blind active-site geometry descriptors plus read-only "
                "per-fingerprint geometry retrieval score components"
            ),
            "feature_count": len(feature_names),
            "feature_names_sample": feature_names[:40],
            "forbidden_inputs_used": [],
            "excluded_predictive_fields": [
                "entry_name",
                "mechanism_text",
                "EC",
                "Rhea",
                "labels",
                "review notes",
                "heldout labels for threshold selection",
            ],
        },
        "row_counts": {
            "manifest_rows": len(manifest_rows),
            "feature_joined_rows": len(model_rows),
            "missing_feature_rows": missing_feature_rows,
            "train_all_row_count": len(train_all),
            "train_primary_row_count": len(train_primary),
            "cal_row_count": len(cal_rows),
            "heldout_row_count": len(heldout),
            "heldout_missing_feature_entry_ids": heldout_missing_ids,
            "train_primary_class_counts": dict(
                sorted(Counter(train_y).items())
            ),
        },
        "models": {
            "logistic_rerun": logistic_result,
            "mlp_32": mlp_result,
            "mlp_32_oos_aware": mlp_oos_aware_result,
        },
        "hand_router_reference": {
            "primary_accuracy_available": hand_primary,
            "oos_or_secondary_false_positive_rate_available": hand_oos,
            "source": (
                "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json"
            ),
        },
        "wave1_2_geometry_logistic_reference": {
            "primary_accuracy_available": wave1_geometry_logistic_primary,
            "primary_correct_count": wave1_geometry_logistic_metrics.get(
                "primary_correct_count"
            ),
            "primary_abstention_count": wave1_geometry_logistic_metrics.get(
                "primary_abstention_count"
            ),
            "primary_wrong_nonabstained_count": wave1_geometry_logistic_metrics.get(
                "primary_wrong_nonabstained_count"
            ),
            "oos_or_secondary_false_positive_rate_available": (
                wave1_geometry_logistic_metrics.get(
                    "oos_or_secondary_false_positive_rate_available"
                )
            ),
            "source": (
                "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json"
            ),
        },
        "learnability_answer": _learnability_answer(
            hand_primary=hand_primary,
            logistic_primary=logistic_primary,
            wave1_geometry_logistic_primary=wave1_geometry_logistic_primary,
            mlp_primary=mlp_primary,
            logistic_result=logistic_result,
            mlp_result=mlp_result,
            mlp_oos_aware_result=mlp_oos_aware_result,
        ),
    }


def write_geometry_nonlinear_head_audit(
    *,
    label_manifest_path: Path,
    geometry_features_path: Path,
    geometry_retrieval_path: Path,
    wave1_audit_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    random_state: int = 702,
    cal_fraction: float = 0.2,
    hidden_layer_size: int = 32,
) -> dict[str, Any]:
    with label_manifest_path.open("r", encoding="utf-8") as handle:
        label_manifest = json.load(handle)
    with geometry_features_path.open("r", encoding="utf-8") as handle:
        geometry_features = json.load(handle)
    with geometry_retrieval_path.open("r", encoding="utf-8") as handle:
        geometry_retrieval = json.load(handle)
    with wave1_audit_path.open("r", encoding="utf-8") as handle:
        wave1_audit = json.load(handle)
    audit = build_geometry_nonlinear_head_audit(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
        geometry_retrieval=geometry_retrieval,
        wave1_audit=wave1_audit,
        random_state=random_state,
        cal_fraction=cal_fraction,
        hidden_layer_size=hidden_layer_size,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(audit), encoding="utf-8")
    return audit


def _split_train_cal(
    rows: list[dict[str, Any]],
    *,
    cal_fraction: float,
    random_state: int,
    train_test_split: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    strata = [_stratify_label(row) for row in rows]
    counts = Counter(strata)
    stratify = strata if rows and min(counts.values()) >= 2 else None
    train_rows, cal_rows = train_test_split(
        rows,
        test_size=cal_fraction,
        random_state=random_state,
        stratify=stratify,
    )
    return list(train_rows), list(cal_rows)


def _evaluate_head(
    *,
    track_id: str,
    display_name: str,
    model: Any,
    cal_rows: list[dict[str, Any]],
    heldout_rows: list[dict[str, Any]],
    wave_masks: dict[str, dict[str, Any]],
    abstain_class: str | None = None,
) -> dict[str, Any]:
    cal_predictions = _predict_rows(model, cal_rows)
    threshold = _select_threshold(cal_rows, cal_predictions, abstain_class=abstain_class)
    heldout_predictions = _predict_rows(model, heldout_rows)
    scored_rows = [
        _score_prediction(row, prediction, threshold, wave_masks, abstain_class)
        for row, prediction in zip(heldout_rows, heldout_predictions)
    ]
    cal_scored_rows = [
        _score_prediction(row, prediction, threshold, wave_masks, abstain_class)
        for row, prediction in zip(cal_rows, cal_predictions)
    ]
    return {
        "track_id": track_id,
        "display_name": display_name,
        "decoder_type": "mlp_head" if "mlp" in track_id else "logistic_head",
        "calibration": {
            "selected_threshold": threshold,
            "cal_metrics": _metrics(cal_scored_rows, mask_mode="manifest"),
        },
        "heldout_metrics": _metrics(scored_rows, mask_mode="canonical"),
        "heldout_metrics_wave1_readthrough_masks": _metrics(
            scored_rows, mask_mode="wave1_readthrough"
        ),
        "per_bin_results": _per_bin_metrics(scored_rows),
        "heldout_rows": scored_rows,
    }


def _predict_rows(model: Any, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    probabilities = model.predict_proba([row["features"] for row in rows])
    classes = [str(label) for label in model.classes_]
    predictions: list[dict[str, Any]] = []
    for row_probs in probabilities:
        values = [float(value) for value in row_probs]
        best_index = max(range(len(values)), key=lambda index: values[index])
        predictions.append(
            {
                "top1_fingerprint_id": classes[best_index],
                "max_probability": values[best_index],
                "class_probabilities": dict(zip(classes, values)),
            }
        )
    return predictions


def _select_threshold(
    cal_rows: list[dict[str, Any]],
    cal_predictions: list[dict[str, Any]],
    *,
    abstain_class: str | None = None,
) -> float:
    thresholds = sorted(
        {
            float(prediction["max_probability"])
            for prediction in cal_predictions
            if not math.isnan(float(prediction["max_probability"]))
        }
    )
    for threshold in thresholds:
        false_positive_count = sum(
            1
            for row, prediction in zip(cal_rows, cal_predictions)
            if not _is_primary_role(row.get("benchmark_role"))
            and prediction["top1_fingerprint_id"] != abstain_class
            and float(prediction["max_probability"]) >= threshold
        )
        if false_positive_count == 0:
            return round(threshold, 6)
    return 1.000001


def _score_prediction(
    row: dict[str, Any],
    prediction: dict[str, Any],
    threshold: float,
    wave_masks: dict[str, dict[str, Any]],
    abstain_class: str | None,
) -> dict[str, Any]:
    entry_id = str(row["entry_id"])
    max_probability = float(prediction["max_probability"])
    abstained = (
        max_probability < threshold
        or prediction["top1_fingerprint_id"] == abstain_class
    )
    true_fingerprint = row.get("true_fingerprint_id")
    called = None if abstained else prediction["top1_fingerprint_id"]
    masks = wave_masks.get(entry_id, {})
    is_primary = bool(
        masks.get("canonical_primary_support_mask")
        if masks
        else _is_primary_role(row.get("benchmark_role"))
    )
    exact = (
        called == true_fingerprint
        if true_fingerprint
        else called is None
    )
    if is_primary and abstained:
        exact = False
    return {
        "entry_id": entry_id,
        "benchmark_role": row.get("benchmark_role"),
        "split_assignment": row.get("split_assignment"),
        "structural_neighborhood_bin": row.get("structural_neighborhood_bin"),
        "true_fingerprint_id": true_fingerprint,
        "top1_fingerprint_id": prediction["top1_fingerprint_id"],
        "called_fingerprint_id": called,
        "max_probability": round(max_probability, 6),
        "abstained": abstained,
        "exact_label_match": exact,
        "primary_top1_correct_if_applicable": (
            (called == true_fingerprint) if is_primary and not abstained else None
        ),
        "canonical_primary_support_mask": is_primary,
        "canonical_oos_or_secondary_support_mask": bool(
            masks.get("canonical_oos_or_secondary_support_mask")
            if masks
            else not is_primary
        ),
        "wave1_readthrough_primary_support_mask": bool(
            masks.get("wave1_readthrough_primary_support_mask", is_primary)
        ),
        "wave1_readthrough_nonprimary_or_oos_mask": bool(
            masks.get("wave1_readthrough_nonprimary_or_oos_mask", not is_primary)
        ),
        "pure_oos_support_mask": true_fingerprint is None,
        "secondary_probe_support_mask": str(row.get("benchmark_role") or "").startswith(
            SECONDARY_PREFIX
        ),
    }


def _metrics(rows: list[dict[str, Any]], *, mask_mode: str) -> dict[str, Any]:
    available = rows
    if mask_mode == "canonical":
        primary_rows = [row for row in rows if row["canonical_primary_support_mask"]]
        nonprimary_rows = [
            row for row in rows if row["canonical_oos_or_secondary_support_mask"]
        ]
    elif mask_mode == "wave1_readthrough":
        primary_rows = [
            row for row in rows if row["wave1_readthrough_primary_support_mask"]
        ]
        nonprimary_rows = [
            row for row in rows if row["wave1_readthrough_nonprimary_or_oos_mask"]
        ]
    else:
        primary_rows = [
            row for row in rows if _is_primary_role(row.get("benchmark_role"))
        ]
        nonprimary_rows = [row for row in rows if row not in primary_rows]

    pure_oos_rows = [row for row in nonprimary_rows if row["pure_oos_support_mask"]]
    secondary_rows = [
        row for row in nonprimary_rows if row["secondary_probe_support_mask"]
    ]
    primary_correct = [
        row
        for row in primary_rows
        if not row["abstained"]
        and row["called_fingerprint_id"] == row["true_fingerprint_id"]
    ]
    primary_wrong = [
        row
        for row in primary_rows
        if not row["abstained"]
        and row["called_fingerprint_id"] != row["true_fingerprint_id"]
    ]
    nonprimary_fp = [row for row in nonprimary_rows if not row["abstained"]]
    pure_oos_fp = [row for row in pure_oos_rows if not row["abstained"]]
    exact_matches = [row for row in rows if row["exact_label_match"]]
    return {
        "row_count": len(rows),
        "available_count": len(available),
        "missing_count": 0,
        "abstention_count": sum(1 for row in rows if row["abstained"]),
        "abstention_rate_available": _rate(
            sum(1 for row in rows if row["abstained"]), len(available)
        ),
        "exact_label_match_count": len(exact_matches),
        "exact_label_accuracy_all_rows": _rate(len(exact_matches), len(rows)),
        "exact_label_accuracy_available": _rate(len(exact_matches), len(available)),
        "primary_support_count": len(primary_rows),
        "primary_available_count": len(primary_rows),
        "primary_correct_count": len(primary_correct),
        "primary_abstention_count": sum(1 for row in primary_rows if row["abstained"]),
        "primary_wrong_nonabstained_count": len(primary_wrong),
        "primary_accuracy_all_rows": _rate(len(primary_correct), len(primary_rows)),
        "primary_accuracy_available": _rate(len(primary_correct), len(primary_rows)),
        "primary_missing_count": 0,
        "oos_or_secondary_support_count": len(nonprimary_rows),
        "oos_or_secondary_available_count": len(nonprimary_rows),
        "oos_or_secondary_abstention_count": sum(
            1 for row in nonprimary_rows if row["abstained"]
        ),
        "oos_or_secondary_false_positive_count": len(nonprimary_fp),
        "oos_or_secondary_false_positive_rate_available": _rate(
            len(nonprimary_fp), len(nonprimary_rows)
        ),
        "pure_oos_support_count": len(pure_oos_rows),
        "pure_oos_false_positive_count": len(pure_oos_fp),
        "pure_oos_false_positive_rate_available": _rate(
            len(pure_oos_fp), len(pure_oos_rows)
        ),
        "secondary_probe_support_count": len(secondary_rows),
        "secondary_probe_nonabstained_count": sum(
            1 for row in secondary_rows if not row["abstained"]
        ),
        "secondary_probe_exact_count": sum(
            1 for row in secondary_rows if row["exact_label_match"]
        ),
    }


def _per_bin_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    bins: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        bins.setdefault(str(row.get("structural_neighborhood_bin") or "unbinned"), []).append(row)
    return {
        bin_name: {
            "row_ids": [row["entry_id"] for row in bin_rows],
            "metrics": _metrics(bin_rows, mask_mode="canonical"),
        }
        for bin_name, bin_rows in sorted(bins.items())
    }


def _geometry_feature_vector(
    geometry_row: dict[str, Any],
    retrieval_row: dict[str, Any],
) -> dict[str, float]:
    features: dict[str, float] = {}
    _set_numeric(features, "residue_count", geometry_row.get("residue_count"))
    _set_numeric(
        features, "resolved_residue_count", geometry_row.get("resolved_residue_count")
    )
    _set_numeric(features, "missing_positions", geometry_row.get("missing_positions"))
    residues = [
        residue for residue in geometry_row.get("residues", []) if isinstance(residue, dict)
    ]
    for residue in residues:
        code = str(residue.get("code") or "UNK").upper()
        features[f"residue_code_count:{code}"] = features.get(
            f"residue_code_count:{code}", 0.0
        ) + 1.0
        for role in residue.get("roles", []) or []:
            role_key = str(role).strip().lower().replace(" ", "_")
            if role_key:
                features[f"role_count:{role_key}"] = features.get(
                    f"role_count:{role_key}", 0.0
                ) + 1.0
    distances = [
        float(edge.get("distance"))
        for edge in geometry_row.get("pairwise_distances_angstrom", [])
        if isinstance(edge, dict) and _is_number(edge.get("distance"))
    ]
    _distance_features(features, distances)
    ligand = geometry_row.get("ligand_context", {}) or {}
    pocket = geometry_row.get("pocket_context", {}) or {}
    pocket_descriptors = pocket.get("descriptors", {}) if isinstance(pocket, dict) else {}
    if not isinstance(pocket_descriptors, dict):
        pocket_descriptors = {}
    for name, value in pocket_descriptors.items():
        _set_numeric(features, f"pocket:{name}", value)
    for family in ligand.get("cofactor_families", []) or []:
        features[f"cofactor_family:{family}"] = 1.0
    for family in ligand.get("structure_cofactor_families", []) or []:
        features[f"structure_cofactor_family:{family}"] = 1.0
    for code in ligand.get("ligand_codes", []) or []:
        features[f"ligand_code:{code}"] = 1.0
    _set_numeric(
        features,
        "proximal_ligand_count",
        len(ligand.get("proximal_ligands", []) or []),
    )
    top_fingerprints = retrieval_row.get("top_fingerprints", [])
    if isinstance(top_fingerprints, list):
        for index, item in enumerate(top_fingerprints[:8], start=1):
            if not isinstance(item, dict):
                continue
            score = item.get("score")
            fp = item.get("fingerprint_id")
            if fp and _is_number(score):
                features[f"geometry_retrieval_score:{fp}"] = float(score)
                if index == 1:
                    features["geometry_retrieval_top1_score"] = float(score)
                features[f"geometry_retrieval_rank_{index}_score"] = float(score)
    return features


def _distance_features(features: dict[str, float], distances: list[float]) -> None:
    features["pairwise_distance_count"] = float(len(distances))
    if not distances:
        return
    features["pairwise_distance_min"] = min(distances)
    features["pairwise_distance_max"] = max(distances)
    features["pairwise_distance_mean"] = mean(distances)
    features["pairwise_distance_std"] = pstdev(distances) if len(distances) > 1 else 0.0
    bins = [3.0, 4.5, 6.0, 8.0, 12.0, 16.0, 24.0, 40.0]
    for distance in distances:
        for upper in bins:
            if distance <= upper:
                features[f"pairwise_distance_le_{upper:g}"] = features.get(
                    f"pairwise_distance_le_{upper:g}", 0.0
                ) + 1.0
                break


def _wave_masks_by_entry(wave1_audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = (
        wave1_audit.get("geometry_baseline_reexport", {}).get("rows", [])
        if isinstance(wave1_audit, dict)
        else []
    )
    return {
        str(row.get("entry_id")): row
        for row in rows
        if isinstance(row, dict) and row.get("entry_id")
    }


def _stratify_label(row: dict[str, Any]) -> str:
    if _is_primary_role(row.get("benchmark_role")):
        return str(row.get("true_fingerprint_id"))
    if str(row.get("benchmark_role") or "").startswith(SECONDARY_PREFIX):
        return "secondary_ood_probe"
    return "out_of_scope"


def _training_label_with_none(row: dict[str, Any]) -> str:
    if _is_primary_role(row.get("benchmark_role")):
        return str(row.get("true_fingerprint_id"))
    return "__none_of_above__"


def _is_primary_role(role: Any) -> bool:
    return str(role or "").startswith(PRIMARY_PREFIX)


def _set_numeric(features: dict[str, float], name: str, value: Any) -> None:
    if _is_number(value):
        features[name] = float(value)


def _is_number(value: Any) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return not math.isnan(float(value))


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 6)


def _learnability_answer(
    *,
    hand_primary: Any,
    logistic_primary: Any,
    wave1_geometry_logistic_primary: Any,
    mlp_primary: Any,
    logistic_result: dict[str, Any],
    mlp_result: dict[str, Any],
    mlp_oos_aware_result: dict[str, Any],
) -> dict[str, Any]:
    answer = {
        "hand_primary_accuracy": hand_primary,
        "local_logistic_control_primary_accuracy": logistic_primary,
        "wave1_2_geometry_logistic_primary_accuracy": (
            wave1_geometry_logistic_primary
        ),
        "mlp_primary_accuracy": mlp_primary,
        "mlp_minus_local_logistic_control_primary_accuracy": (
            round(float(mlp_primary) - float(logistic_primary), 6)
            if mlp_primary is not None and logistic_primary is not None
            else None
        ),
        "mlp_minus_wave1_2_geometry_logistic_primary_accuracy": (
            round(float(mlp_primary) - float(wave1_geometry_logistic_primary), 6)
            if mlp_primary is not None and wave1_geometry_logistic_primary is not None
            else None
        ),
        "hand_edge_closed_by_mlp_fraction_vs_local_logistic_control": None,
        "hand_edge_closed_by_mlp_fraction_vs_wave1_2_geometry_logistic": None,
        "interpretation": "not_available",
    }
    if hand_primary is not None and logistic_primary is not None and mlp_primary is not None:
        edge = float(hand_primary) - float(logistic_primary)
        if edge > 0:
            answer["hand_edge_closed_by_mlp_fraction_vs_local_logistic_control"] = round(
                (float(mlp_primary) - float(logistic_primary)) / edge, 6
            )
    if (
        hand_primary is not None
        and wave1_geometry_logistic_primary is not None
        and mlp_primary is not None
    ):
        wave_edge = float(hand_primary) - float(wave1_geometry_logistic_primary)
        if wave_edge > 0:
            answer[
                "hand_edge_closed_by_mlp_fraction_vs_wave1_2_geometry_logistic"
            ] = round(
                (float(mlp_primary) - float(wave1_geometry_logistic_primary))
                / wave_edge,
                6,
            )
    if hand_primary is not None and mlp_primary is not None:
        wrong = mlp_oos_aware_result["heldout_metrics"][
            "primary_wrong_nonabstained_count"
        ]
        abstained = mlp_oos_aware_result["heldout_metrics"]["primary_abstention_count"]
        if wrong == 0 and abstained > 0:
            answer["interpretation"] = (
                "remaining MLP gap is abstention-dominated under the frozen "
                "calibration policy"
            )
        elif wrong > 0:
            answer["interpretation"] = (
                "remaining MLP gap includes wrong nonabstained primary calls, "
                "so nonlinear separation is not sufficient by itself"
            )
        else:
            answer["interpretation"] = "MLP closed the primary hand-router gap"
    return answer


def _blocked_audit(
    *,
    reason: str,
    detail: str,
    label_manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_id": "v3_geometry_nonlinear_head_audit_702_20260529",
        "schema_version": "geometry_nonlinear_head_audit.v1",
        "created_utc": _utc_now_iso(),
        "status": "blocked",
        "blocker": reason,
        "detail": detail,
        "row_count": len(label_manifest.get("rows", []) or []),
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "large_downloads_performed": False,
        },
    }


def _markdown_report(audit: dict[str, Any]) -> str:
    if audit.get("status") != "complete":
        return (
            "# Geometry Nonlinear Head Audit\n\n"
            f"Status: `{audit.get('status')}`\n\n"
            f"Blocker: `{audit.get('blocker')}`\n\n"
            f"Detail: {audit.get('detail')}\n"
        )
    logistic = audit["models"]["logistic_rerun"]["heldout_metrics"]
    mlp = audit["models"]["mlp_32"]["heldout_metrics"]
    mlp_oos = audit["models"]["mlp_32_oos_aware"]["heldout_metrics"]
    answer = audit["learnability_answer"]
    lines = [
        "# Geometry Nonlinear Head Audit",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "No labels, registries, ontologies, imports, production scoring, or global thresholds were edited. The abstention threshold was selected on calibration rows only.",
        "",
        "## Headline",
        "",
        f"- Logistic rerun primary: {logistic['primary_correct_count']}/{logistic['primary_support_count']} correct, {logistic['primary_abstention_count']} abstained, {logistic['primary_wrong_nonabstained_count']} wrong nonabstained.",
        f"- Primary-only MLP-32 primary: {mlp['primary_correct_count']}/{mlp['primary_support_count']} correct, {mlp['primary_abstention_count']} abstained, {mlp['primary_wrong_nonabstained_count']} wrong nonabstained.",
        f"- OOS-aware MLP-32 primary: {mlp_oos['primary_correct_count']}/{mlp_oos['primary_support_count']} correct, {mlp_oos['primary_abstention_count']} abstained, {mlp_oos['primary_wrong_nonabstained_count']} wrong nonabstained.",
        f"- OOS-aware MLP OOS/sec false-positive rate: {mlp_oos['oos_or_secondary_false_positive_rate_available']}.",
        f"- Hand edge closed versus Wave 1.2 geometry-logistic: {answer['hand_edge_closed_by_mlp_fraction_vs_wave1_2_geometry_logistic']}.",
        f"- Hand edge closed versus local logistic control: {answer['hand_edge_closed_by_mlp_fraction_vs_local_logistic_control']}.",
        f"- Interpretation: {answer['interpretation']}.",
        "",
        "## Per-bin MLP",
        "",
        "| Bin | Primary support | Primary abstain | Primary acc | OOS/sec support | OOS/sec FP |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for bin_name, payload in audit["models"]["mlp_32_oos_aware"]["per_bin_results"].items():
        metrics = payload["metrics"]
        lines.append(
            "| "
            + " | ".join(
                [
                    bin_name,
                    str(metrics["primary_support_count"]),
                    str(metrics["primary_abstention_count"]),
                    str(metrics["primary_accuracy_available"]),
                    str(metrics["oos_or_secondary_support_count"]),
                    str(metrics["oos_or_secondary_false_positive_rate_available"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
