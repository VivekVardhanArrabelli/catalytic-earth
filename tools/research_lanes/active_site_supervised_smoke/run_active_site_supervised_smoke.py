from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

try:
    from sklearn.linear_model import LogisticRegression
except Exception:  # pragma: no cover - exercised only when sklearn is absent.
    LogisticRegression = None  # type: ignore[assignment]


FORBIDDEN_PREDICTIVE_KEY_FRAGMENTS = [
    "ec_label",
    "ec_number",
    "entry",
    "expert",
    "fingerprint",
    "label",
    "mechanism",
    "name",
    "note",
    "pdb",
    "rationale",
    "review",
    "rhea",
    "source",
    "uniprot",
]

TRAIN_CAL_ELIGIBLE = "train_cal_eligible_parent_v1_or_oos"
SECONDARY_CANARY_ONLY = "secondary_canary_only_not_train"
OOS_TARGET = "None"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the approval-gated active-site supervised smoke."
    )
    parser.add_argument("--train-cal-cache", required=True)
    parser.add_argument("--train-cal-feasibility", required=True)
    parser.add_argument("--diagnostic-cache", action="append", default=[])
    parser.add_argument("--leakage-audit", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary-out", required=True)
    parser.add_argument("--report-out", required=True)
    parser.add_argument("--seed", type=int, default=20260528)
    parser.add_argument("--no-production-claims", action="store_true", required=True)
    args = parser.parse_args(argv)

    result = run_smoke(
        train_cal_cache_path=Path(args.train_cal_cache),
        train_cal_feasibility_path=Path(args.train_cal_feasibility),
        diagnostic_cache_paths=[Path(path) for path in args.diagnostic_cache],
        leakage_audit_path=Path(args.leakage_audit),
        seed=args.seed,
    )
    write_jsonl(Path(args.out), result["predictions"])
    write_json(Path(args.summary_out), result["summary"])
    Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_out).write_text(markdown_report(result["summary"]), encoding="utf-8")
    return 0


def run_smoke(
    *,
    train_cal_cache_path: Path,
    train_cal_feasibility_path: Path,
    diagnostic_cache_paths: list[Path],
    leakage_audit_path: Path,
    seed: int,
) -> dict[str, Any]:
    audit = read_json(leakage_audit_path)
    if audit.get("training_preflight_status") != "pass":
        raise ValueError("leakage audit did not pass")
    if audit.get("summary", {}).get("blocker_count") != 0:
        raise ValueError("leakage audit has blockers")

    feasibility = read_json(train_cal_feasibility_path)
    train_cal_rows = read_jsonl(train_cal_cache_path)
    diagnostic_rows = [
        row
        for path in diagnostic_cache_paths
        for row in read_jsonl(path)
    ]
    all_rows = train_cal_rows + diagnostic_rows

    assert_no_forbidden_predictive_keys(all_rows)
    row_context = feasibility_context(feasibility)
    train_rows, cal_rows, canary_rows = split_train_cal_rows(train_cal_rows, row_context)

    vectorizer = FeatureVectorizer()
    train_matrix = vectorizer.fit_transform([row["predictive_features"] for row in train_rows])
    cal_matrix = vectorizer.transform([row["predictive_features"] for row in cal_rows])

    model = fit_model(train_matrix, [target_for_row(row, row_context) for row in train_rows], seed)
    cal_scores = score_rows(model, cal_matrix)
    threshold = choose_threshold(
        scores=cal_scores,
        true_targets=[target_for_row(row, row_context) for row in cal_rows],
        max_risk=0.20,
        max_oos_false_positive_rate=0.05,
    )

    predictions: list[dict[str, Any]] = []
    predictions.extend(
        prediction_records(
            rows=train_rows,
            row_context=row_context,
            split="train",
            scores=score_rows(model, train_matrix),
            threshold=threshold,
        )
    )
    predictions.extend(
        prediction_records(
            rows=cal_rows,
            row_context=row_context,
            split="calibration",
            scores=cal_scores,
            threshold=threshold,
        )
    )
    if canary_rows:
        canary_matrix = vectorizer.transform(
            [row["predictive_features"] for row in canary_rows]
        )
        predictions.extend(
            prediction_records(
                rows=canary_rows,
                row_context=row_context,
                split="canary_only",
                scores=score_rows(model, canary_matrix),
                threshold=threshold,
            )
        )
    if diagnostic_rows:
        diag_matrix = vectorizer.transform(
            [row["predictive_features"] for row in diagnostic_rows]
        )
        predictions.extend(
            prediction_records(
                rows=diagnostic_rows,
                row_context=row_context,
                split="diagnostic_eval_only",
                scores=score_rows(model, diag_matrix),
                threshold=threshold,
            )
        )

    summary = build_summary(
        predictions=predictions,
        train_count=len(train_rows),
        calibration_count=len(cal_rows),
        canary_count=len(canary_rows),
        diagnostic_count=len(diagnostic_rows),
        threshold=threshold,
        model_id=model["model_id"],
        feature_count=len(vectorizer.feature_names),
        seed=seed,
    )
    return {"predictions": predictions, "summary": summary}


class FeatureVectorizer:
    def __init__(self) -> None:
        self.feature_names: list[str] = []
        self.mean: np.ndarray | None = None
        self.scale: np.ndarray | None = None

    def fit_transform(self, feature_rows: list[dict[str, Any]]) -> np.ndarray:
        flattened = [flatten_features(row) for row in feature_rows]
        self.feature_names = sorted({key for row in flattened for key in row})
        matrix = self._matrix(flattened)
        self.mean = matrix.mean(axis=0)
        scale = matrix.std(axis=0)
        scale[scale == 0.0] = 1.0
        self.scale = scale
        return (matrix - self.mean) / self.scale

    def transform(self, feature_rows: list[dict[str, Any]]) -> np.ndarray:
        if self.mean is None or self.scale is None:
            raise ValueError("vectorizer is not fitted")
        matrix = self._matrix([flatten_features(row) for row in feature_rows])
        return (matrix - self.mean) / self.scale

    def _matrix(self, flattened: list[dict[str, float]]) -> np.ndarray:
        if not flattened:
            return np.zeros((0, len(self.feature_names)), dtype=float)
        return np.array(
            [[row.get(name, 0.0) for name in self.feature_names] for row in flattened],
            dtype=float,
        )


def flatten_features(value: Any, prefix: str = "") -> dict[str, float]:
    features: dict[str, float] = {}
    _flatten_into(features, value, prefix)
    return features


def _flatten_into(features: dict[str, float], value: Any, prefix: str) -> None:
    if isinstance(value, bool):
        features[prefix] = 1.0 if value else 0.0
    elif isinstance(value, (int, float)) and math.isfinite(float(value)):
        features[prefix] = float(value)
    elif isinstance(value, str):
        features[f"{prefix}={value}"] = 1.0
    elif isinstance(value, list):
        primitive_counts = Counter(
            str(item)
            for item in value
            if item is not None and not isinstance(item, (dict, list))
        )
        for item, count in primitive_counts.items():
            features[f"{prefix}={item}"] = float(count)
        for index, item in enumerate(item for item in value if isinstance(item, dict)):
            _flatten_into(features, item, f"{prefix}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            _flatten_into(features, item, next_prefix)


def fit_model(matrix: np.ndarray, targets: list[str], seed: int) -> dict[str, Any]:
    if len(set(targets)) < 2:
        raise ValueError("at least two target classes are required")
    if LogisticRegression is not None:
        classifier = LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=seed,
        )
        classifier.fit(matrix, targets)
        return {
            "model_id": "logistic_l2_balanced",
            "classes": list(classifier.classes_),
            "classifier": classifier,
        }
    return fit_nearest_centroid(matrix, targets)


def fit_nearest_centroid(matrix: np.ndarray, targets: list[str]) -> dict[str, Any]:
    centroids = {}
    for target in sorted(set(targets)):
        centroids[target] = matrix[[idx for idx, y in enumerate(targets) if y == target]].mean(
            axis=0
        )
    return {
        "model_id": "nearest_centroid_active_site",
        "classes": sorted(centroids),
        "centroids": centroids,
    }


def score_rows(model: dict[str, Any], matrix: np.ndarray) -> list[dict[str, Any]]:
    if matrix.shape[0] == 0:
        return []
    if model["model_id"] == "logistic_l2_balanced":
        probabilities = model["classifier"].predict_proba(matrix)
        classes = list(model["classifier"].classes_)
        scores = []
        for row_probs in probabilities:
            top_index = int(np.argmax(row_probs))
            scores.append(
                {
                    "predicted_target": classes[top_index],
                    "confidence": float(row_probs[top_index]),
                    "class_scores": {
                        classes[index]: float(prob) for index, prob in enumerate(row_probs)
                    },
                }
            )
        return scores
    return centroid_scores(model, matrix)


def centroid_scores(model: dict[str, Any], matrix: np.ndarray) -> list[dict[str, Any]]:
    scores = []
    classes = model["classes"]
    for row in matrix:
        distances = {
            target: float(np.linalg.norm(row - model["centroids"][target]))
            for target in classes
        }
        ordered = sorted(distances.items(), key=lambda item: item[1])
        best, best_distance = ordered[0]
        second_distance = ordered[1][1] if len(ordered) > 1 else best_distance + 1.0
        margin = max(0.0, second_distance - best_distance)
        confidence = margin / (1.0 + margin)
        scores.append(
            {
                "predicted_target": best,
                "confidence": confidence,
                "class_scores": {target: -distance for target, distance in distances.items()},
            }
        )
    return scores


def choose_threshold(
    *,
    scores: list[dict[str, Any]],
    true_targets: list[str],
    max_risk: float,
    max_oos_false_positive_rate: float,
) -> float:
    thresholds = sorted({0.0, 1.01, *(score["confidence"] for score in scores)})
    best_threshold: float | None = None
    best_coverage = -1
    for threshold in thresholds:
        accepted = [
            (score, true)
            for score, true in zip(scores, true_targets, strict=True)
            if score["confidence"] >= threshold
        ]
        if not accepted:
            risk = 0.0
            oos_fp_rate = 0.0
        else:
            wrong = sum(1 for score, true in accepted if score["predicted_target"] != true)
            risk = wrong / len(accepted)
            oos_rows = [(score, true) for score, true in accepted if true == OOS_TARGET]
            oos_fp = sum(
                1
                for score, true in oos_rows
                if score["predicted_target"] != OOS_TARGET
            )
            oos_fp_rate = oos_fp / len(oos_rows) if oos_rows else 0.0
        if risk <= max_risk and oos_fp_rate <= max_oos_false_positive_rate:
            coverage = len(accepted)
            if coverage > best_coverage:
                best_coverage = coverage
                best_threshold = threshold
    return float(best_threshold if best_threshold is not None else 1.01)


def prediction_records(
    *,
    rows: list[dict[str, Any]],
    row_context: dict[str, dict[str, Any]],
    split: str,
    scores: list[dict[str, Any]],
    threshold: float,
) -> list[dict[str, Any]]:
    records = []
    for row, score in zip(rows, scores, strict=True):
        entry_id = str(row["metadata"]["entry_id"])
        true_target = target_for_row(row, row_context)
        abstained = score["confidence"] < threshold
        records.append(
            {
                "entry_id": entry_id,
                "split": split,
                "source_group": row["metadata"].get("source_group"),
                "true_target_metadata_only": true_target,
                "predicted_target": None if abstained else score["predicted_target"],
                "raw_predicted_target": score["predicted_target"],
                "confidence": round(float(score["confidence"]), 6),
                "abstained": abstained,
                "correct_if_nonabstained": (
                    None if abstained else score["predicted_target"] == true_target
                ),
            }
        )
    return records


def build_summary(
    *,
    predictions: list[dict[str, Any]],
    train_count: int,
    calibration_count: int,
    canary_count: int,
    diagnostic_count: int,
    threshold: float,
    model_id: str,
    feature_count: int,
    seed: int,
) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    for split in sorted({row["split"] for row in predictions}):
        rows = [row for row in predictions if row["split"] == split]
        nonabstained = [row for row in rows if not row["abstained"]]
        wrong = [
            row
            for row in nonabstained
            if row["correct_if_nonabstained"] is False
        ]
        oos_rows = [
            row
            for row in nonabstained
            if row["true_target_metadata_only"] == OOS_TARGET
        ]
        oos_fp = [
            row for row in oos_rows if row["predicted_target"] != OOS_TARGET
        ]
        by_split[split] = {
            "row_count": len(rows),
            "coverage": round(len(nonabstained) / len(rows), 6) if rows else 0.0,
            "risk": round(len(wrong) / len(nonabstained), 6) if nonabstained else 0.0,
            "oos_false_positive_rate": (
                round(len(oos_fp) / len(oos_rows), 6) if oos_rows else 0.0
            ),
            "nonabstained_count": len(nonabstained),
        }
    return {
        "artifact_id": "v3_active_site_supervised_smoke_summary_20260528",
        "schema_version": "active_site_supervised_smoke_summary.v1",
        "review_only": True,
        "no_production_claims": True,
        "training_executed": True,
        "labels_changed": False,
        "registries_changed": False,
        "ontologies_changed": False,
        "production_scoring_changed": False,
        "thresholds_changed": False,
        "model_id": model_id,
        "seed": seed,
        "feature_count": feature_count,
        "abstention_threshold": threshold,
        "train_count": train_count,
        "calibration_count": calibration_count,
        "canary_count": canary_count,
        "diagnostic_count": diagnostic_count,
        "metrics_by_split": by_split,
        "non_claims": [
            "review-only smoke",
            "not a production benchmark",
            "not label promotion evidence",
            "not a claim that learned representations beat Foldseek or geometry",
        ],
    }


def markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Active-Site Supervised Smoke\n\n",
        "Review-only smoke output. This report is not a production benchmark or label decision.\n\n",
        "## Summary\n",
    ]
    for key in [
        "model_id",
        "train_count",
        "calibration_count",
        "canary_count",
        "diagnostic_count",
        "abstention_threshold",
        "feature_count",
    ]:
        lines.append(f"- `{key}`: {summary.get(key)}\n")
    lines.append("\n## Metrics By Split\n")
    for split, metrics in summary.get("metrics_by_split", {}).items():
        lines.append(f"- `{split}`: {metrics}\n")
    return "".join(lines)


def feasibility_context(feasibility: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["entry_id"]): row for row in feasibility.get("rows", [])}


def split_train_cal_rows(
    cache_rows: list[dict[str, Any]],
    row_context: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    train_rows = []
    cal_rows = []
    canary_rows = []
    for row in cache_rows:
        entry_id = str(row["metadata"]["entry_id"])
        context = row_context.get(entry_id)
        if context is None:
            raise ValueError(f"cache row missing from feasibility context: {entry_id}")
        if context.get("train_cal_use_group") == SECONDARY_CANARY_ONLY:
            canary_rows.append(row)
            continue
        if context.get("train_cal_use_group") != TRAIN_CAL_ELIGIBLE:
            raise ValueError(f"row is not train/cal eligible: {entry_id}")
        split = context.get("proposed_train_cal_split")
        if split == "train":
            train_rows.append(row)
        elif split == "calibration":
            cal_rows.append(row)
        else:
            raise ValueError(f"invalid train/cal split for {entry_id}: {split}")
    if not train_rows or not cal_rows:
        raise ValueError("both train and calibration rows are required")
    return train_rows, cal_rows, canary_rows


def target_for_row(row: dict[str, Any], row_context: dict[str, dict[str, Any]]) -> str:
    entry_id = str(row["metadata"]["entry_id"])
    context = row_context.get(entry_id)
    if context is not None:
        return str(context.get("target_group_metadata_only") or OOS_TARGET)
    return str(row.get("metadata", {}).get("current_fingerprint_id") or OOS_TARGET)


def assert_no_forbidden_predictive_keys(rows: list[dict[str, Any]]) -> None:
    hits = []
    for row in rows:
        entry_id = row.get("metadata", {}).get("entry_id")
        hits.extend(
            {
                "entry_id": entry_id,
                **hit,
            }
            for hit in forbidden_predictive_key_hits(row.get("predictive_features", {}))
        )
    if hits:
        raise ValueError(f"forbidden predictive keys found: {hits[:10]}")


def forbidden_predictive_key_hits(value: Any, path: str = "predictive_features") -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            for fragment in FORBIDDEN_PREDICTIVE_KEY_FRAGMENTS:
                if fragment in lowered:
                    hits.append({"path": f"{path}.{key}", "fragment": fragment})
            hits.extend(forbidden_predictive_key_hits(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(forbidden_predictive_key_hits(item, f"{path}[{index}]"))
    return hits


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
