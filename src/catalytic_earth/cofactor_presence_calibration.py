"""Leakage-safe train/calibration cofactor-presence channel.

This is the leakage-safe sibling of :mod:`sequence_cofactor_channel`. The existing
channel fits one-vs-rest cofactor-presence heads on ``in_distribution`` rows and
then reads the ``heldout`` cofactor labels to report ROC-AUC/AP *and* to pick the
best embedding backend per class. Reading heldout labels (even structural ones)
to score and to select sources entangles the one-shot heldout surface with the
channel design.

This module removes that entanglement. It:

1. fits the one-vs-rest presence heads on the ``train`` split only;
2. selects every per-class operating threshold and the per-class embedding
   backend on the ``calibration`` split only;
3. emits a per-entry prediction surface for *all* rows (train, calibration,
   heldout, and split-uncovered) without ever reading the heldout labels.

Supervision is structural ligand context only (selected-PDB
``ligand_context.cofactor_families``); the mechanism fingerprint, EC, Rhea,
mechanism text, and benchmark labels are never used to fit or threshold the
channel. The emitted prediction rows reuse the schema consumed by
``sequence_cofactor_channel._fused_geometry_features`` so the channel can later
be injected into the router under an explicit one-shot heldout authorization.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_channel_probe import (
    DEFAULT_COFACTOR_CLASSES,
    _cofactor_label_rows,
    _read_jsonl,
)


DEFAULT_EMBEDDING_SPECS = (
    {
        "key": "esm2_t6_8m",
        "sidecar_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl",
    },
    {
        "key": "esm2_t12_35m",
        "sidecar_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl",
    },
)
DEFAULT_SPLIT_MANIFEST_PATH = (
    "artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json"
)
DEFAULT_LABEL_MANIFEST_PATH = "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
DEFAULT_GEOMETRY_FEATURES_PATH = "artifacts/v3_geometry_features_1025.json"

# Calibration positives below this make the per-class operating point report-only:
# a threshold chosen on 3-4 positives is not a deployable calibration.
MIN_CALIBRATION_POSITIVE = 5
PRECISION_FLOOR = 0.9
RECALL_FLOOR = 0.9

# Well-established cofactor-binding sequence motifs, appended as binary features
# to the embedding so the head can pick up folds the pooled embedding misses
# (e.g. flavin-binding Rossmann rows the ESM-2 head scores near zero). Pure
# sequence regexes -- no labels, EC, Rhea, or mechanism text. Leakage-safe.
MOTIF_FEATURE_SPECS = (
    ("rossmann_gxgxxg", r"G.G..G"),       # FAD/NAD dinucleotide-binding beta-alpha-beta
    ("heme_cxxch", r"C..CH"),             # c-type heme attachment site
    ("metal_hexxh", r"HE..H"),            # zinc metallohydrolase active-site motif
    ("metal_his_pair", r"H.{1,3}H"),      # close histidine pair (metal coordination)
)


def _motif_feature_vector(sequence: str) -> list[int]:
    import re

    seq = (sequence or "").upper()
    return [1 if seq and re.search(pattern, seq) else 0 for _name, pattern in MOTIF_FEATURE_SPECS]


def _augment_with_motifs(
    embeddings: dict[str, list[float]], sequences: dict[str, str]
) -> dict[str, list[float]]:
    zero = [0] * len(MOTIF_FEATURE_SPECS)
    augmented: dict[str, list[float]] = {}
    for entry_id, vector in embeddings.items():
        motif = _motif_feature_vector(sequences.get(entry_id, "")) if sequences else zero
        augmented[entry_id] = list(vector) + [float(value) for value in motif]
    return augmented


def write_cofactor_presence_calibration(
    *,
    label_manifest_path: Path,
    geometry_features_path: Path,
    split_manifest_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    embedding_specs: tuple[dict[str, str], ...] = DEFAULT_EMBEDDING_SPECS,
    sequence_manifest_path: Path | None = None,
    fasta_path: Path | None = None,
    use_motif_features: bool = False,
    min_calibration_positive: int = MIN_CALIBRATION_POSITIVE,
    random_state: int = 702,
) -> dict[str, Any]:
    label_manifest = _load_json(label_manifest_path)
    geometry_features = _load_json(geometry_features_path)
    split_manifest = _load_json(split_manifest_path)
    embedding_sidecars: dict[str, list[dict[str, Any]]] = {}
    for spec in embedding_specs:
        path = Path(spec["sidecar_path"])
        if path.exists():
            embedding_sidecars[str(spec["key"])] = _read_jsonl(path)
    sequences: dict[str, str] | None = None
    if use_motif_features and sequence_manifest_path is not None and fasta_path is not None:
        from .sequence_cofactor_channel import _parse_fasta, _sequence_by_entry

        sequences = _sequence_by_entry(
            _load_json(sequence_manifest_path),
            _parse_fasta(Path(fasta_path).read_text(encoding="utf-8")),
        )
    audit = build_cofactor_presence_calibration(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
        split_manifest=split_manifest,
        embedding_sidecars=embedding_sidecars,
        sequences=sequences,
        use_motif_features=use_motif_features,
        min_calibration_positive=min_calibration_positive,
        random_state=random_state,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_calibration_report(audit), encoding="utf-8")
    return audit


def build_cofactor_presence_calibration(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
    split_manifest: dict[str, Any],
    embedding_sidecars: dict[str, list[dict[str, Any]]],
    cofactor_classes: tuple[str, ...] = DEFAULT_COFACTOR_CLASSES,
    sequences: dict[str, str] | None = None,
    use_motif_features: bool = False,
    min_calibration_positive: int = MIN_CALIBRATION_POSITIVE,
    random_state: int = 702,
) -> dict[str, Any]:
    label_rows = _cofactor_label_rows(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
    )
    clean_rows = [row for row in label_rows if row["label_status"] == "clean_geometry_ok"]
    split_by_entry = _split_assignment(split_manifest)

    embeddings_by_backend = {
        key: _dense_embeddings(records) for key, records in sorted(embedding_sidecars.items())
    }
    if use_motif_features:
        embeddings_by_backend = {
            backend: _augment_with_motifs(embeddings, sequences or {})
            for backend, embeddings in embeddings_by_backend.items()
        }

    per_backend: dict[str, dict[str, Any]] = {}
    for backend, embeddings in embeddings_by_backend.items():
        per_backend[backend] = _fit_backend(
            clean_rows=clean_rows,
            split_by_entry=split_by_entry,
            embeddings=embeddings,
            cofactor_classes=cofactor_classes,
            min_calibration_positive=min_calibration_positive,
            random_state=random_state,
        )

    selected_sources = _select_sources_by_calibration(
        per_backend=per_backend,
        cofactor_classes=cofactor_classes,
    )
    channel_predictions = _channel_predictions(
        label_rows=label_rows,
        per_backend=per_backend,
        selected_sources=selected_sources,
        split_by_entry=split_by_entry,
        cofactor_classes=cofactor_classes,
    )

    coverage = _split_coverage(
        clean_rows=clean_rows,
        split_by_entry=split_by_entry,
        embeddings_by_backend=embeddings_by_backend,
    )

    return {
        "artifact_id": "v3_cofactor_presence_calibration_current702_20260604",
        "schema_version": "cofactor_presence_calibration.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "input_is_sequence_embedding_only": True,
            "supervision_is_structural_ligand_context_only": True,
            "mechanism_fingerprint_used_for_labels": False,
            "ec_rhea_or_mechanism_text_used_for_labels": False,
            "benchmark_mechanism_labels_used": False,
            "heads_fit_on_train_split_only": True,
            "thresholds_selected_on_calibration_split_only": True,
            "embedding_backend_selected_on_calibration_split_only": True,
            "heldout_labels_read": False,
            "heldout_used_for_fit_or_threshold": False,
            "global_threshold_changed": False,
            "production_scoring_changed": False,
            "label_registry_edited": False,
            "sequence_motif_features_used": bool(use_motif_features),
            "sequence_motif_features_are_sequence_regexes_only": True,
        },
        "sequence_motif_features": {
            "enabled": bool(use_motif_features),
            "feature_names": [name for name, _pattern in MOTIF_FEATURE_SPECS],
            "note": (
                "binary cofactor-binding sequence motifs appended to the embedding "
                "before fitting; pure sequence regexes, no labels/EC/Rhea/mechanism"
            ),
        },
        "policy": {
            "label_source": (
                "experimental selected-PDB active-site ligand context "
                "(geometry_features ligand_context.cofactor_families); empty means "
                "no local cofactor family observed in the selected structure, not a "
                "guaranteed biological apo assertion"
            ),
            "split_source": (
                "assigned_embedding_split from the frozen mechanism-feature "
                "train/calibration split manifest; heldout rows are scored but their "
                "labels are never read"
            ),
            "threshold_policy": (
                "per-class operating threshold = max-F1 on the calibration split; "
                "precision-floor and recall-floor operating points are also reported "
                "for reference but the channel ships the max-F1 point"
            ),
            "backend_policy": (
                "per-class embedding backend = highest calibration ROC-AUC; ties "
                "broken by average precision then backend name"
            ),
            "low_support_policy": (
                f"classes with fewer than {min_calibration_positive} calibration "
                "positives are flagged low_calibration_support and treated as "
                "report-only operating points"
            ),
        },
        "source_artifacts": {
            "label_manifest": DEFAULT_LABEL_MANIFEST_PATH,
            "geometry_features": DEFAULT_GEOMETRY_FEATURES_PATH,
            "split_manifest": DEFAULT_SPLIT_MANIFEST_PATH,
            "embedding_sidecars": [spec for spec in sorted(embeddings_by_backend)],
        },
        "split_coverage": coverage,
        "trained_calibrated_heads": per_backend,
        "selected_sources": selected_sources,
        "channel_predictions": channel_predictions,
        "channel_prediction_summary": _prediction_summary(channel_predictions, cofactor_classes),
    }


def _fit_backend(
    *,
    clean_rows: list[dict[str, Any]],
    split_by_entry: dict[str, str],
    embeddings: dict[str, list[float]],
    cofactor_classes: tuple[str, ...],
    min_calibration_positive: int,
    random_state: int,
) -> dict[str, Any]:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:  # pragma: no cover - environment dependent
        return {"status": "blocked", "blocker": "sklearn_unavailable", "detail": f"{type(exc).__name__}: {exc}"}

    joined = [row for row in clean_rows if row["entry_id"] in embeddings]
    train_rows = [r for r in joined if split_by_entry.get(r["entry_id"]) == "train"]
    cal_rows = [r for r in joined if split_by_entry.get(r["entry_id"]) == "calibration"]
    if not train_rows or not cal_rows:
        return {
            "status": "blocked",
            "blocker": "missing_train_or_calibration_join",
            "train_row_count": len(train_rows),
            "calibration_row_count": len(cal_rows),
        }

    class_results: dict[str, Any] = {}
    per_entry_scores: dict[str, dict[str, float]] = {row["entry_id"]: {} for row in joined}
    for cofactor_class in cofactor_classes:
        train_y = [int(cofactor_class in row["local_cofactor_families"]) for row in train_rows]
        cal_y = [int(cofactor_class in row["local_cofactor_families"]) for row in cal_rows]
        if len(set(train_y)) < 2:
            class_results[cofactor_class] = {"status": "blocked", "blocker": "single_training_class"}
            continue
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                solver="liblinear",
                random_state=random_state,
            ),
        )
        model.fit([embeddings[r["entry_id"]] for r in train_rows], train_y)
        cal_scores = [
            float(v) for v in model.predict_proba([embeddings[r["entry_id"]] for r in cal_rows])[:, 1]
        ]
        operating_points = _operating_points(cal_y=cal_y, cal_scores=cal_scores)
        cal_positive = int(sum(cal_y))
        # Score every joined entry so the per-entry surface can be emitted later
        # without re-fitting; heldout labels are never consulted here.
        all_scores = model.predict_proba([embeddings[r["entry_id"]] for r in joined])[:, 1]
        for row, score in zip(joined, all_scores):
            per_entry_scores[row["entry_id"]][cofactor_class] = float(score)
        class_results[cofactor_class] = {
            "status": "complete",
            "model": "StandardScaler + class_weight=balanced LogisticRegression(liblinear)",
            "train_positive_count": int(sum(train_y)),
            "train_row_count": len(train_rows),
            "calibration_positive_count": cal_positive,
            "calibration_row_count": len(cal_rows),
            "low_calibration_support": cal_positive < min_calibration_positive,
            "calibration_roc_auc": operating_points["roc_auc"],
            "calibration_average_precision": operating_points["average_precision"],
            "selected_operating_point": operating_points["max_f1"],
            "precision_floor_operating_point": operating_points["precision_floor"],
            "recall_floor_operating_point": operating_points["recall_floor"],
        }
    return {
        "status": "complete",
        "joined_clean_row_count": len(joined),
        "train_row_count": len(train_rows),
        "calibration_row_count": len(cal_rows),
        "class_results": class_results,
        "per_entry_scores": per_entry_scores,
    }


def _operating_points(*, cal_y: list[int], cal_scores: list[float]) -> dict[str, Any]:
    roc_auc = None
    average_precision = None
    if len(set(cal_y)) == 2:
        from sklearn.metrics import average_precision_score, roc_auc_score

        roc_auc = round(float(roc_auc_score(cal_y, cal_scores)), 6)
        average_precision = round(float(average_precision_score(cal_y, cal_scores)), 6)

    candidates = sorted({round(float(s), 6) for s in cal_scores} | {0.5})
    sweep: list[dict[str, Any]] = []
    for threshold in candidates:
        sweep.append(_threshold_metrics(cal_y=cal_y, cal_scores=cal_scores, threshold=threshold))

    max_f1 = _best_by(sweep, key=lambda m: (m["f1"], m["threshold"]))
    precision_floor = _best_by(
        [m for m in sweep if m["precision"] >= PRECISION_FLOOR and m["tp"] > 0],
        key=lambda m: (m["recall"], -m["threshold"]),
    )
    recall_floor = _best_by(
        [m for m in sweep if m["recall"] >= RECALL_FLOOR],
        key=lambda m: (m["precision"], m["threshold"]),
    )
    return {
        "roc_auc": roc_auc,
        "average_precision": average_precision,
        "max_f1": max_f1,
        "precision_floor": precision_floor,
        "recall_floor": recall_floor,
    }


def _threshold_metrics(*, cal_y: list[int], cal_scores: list[float], threshold: float) -> dict[str, Any]:
    tp = fp = fn = tn = 0
    for y, score in zip(cal_y, cal_scores):
        predicted = 1 if score >= threshold else 0
        if predicted and y:
            tp += 1
        elif predicted and not y:
            fp += 1
        elif not predicted and y:
            fn += 1
        else:
            tn += 1
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "threshold": round(float(threshold), 6),
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def _best_by(rows: list[dict[str, Any]], *, key) -> dict[str, Any] | None:
    if not rows:
        return None
    return max(rows, key=key)


def _select_sources_by_calibration(
    *,
    per_backend: dict[str, dict[str, Any]],
    cofactor_classes: tuple[str, ...],
) -> dict[str, Any]:
    selected: dict[str, Any] = {}
    for cofactor_class in cofactor_classes:
        best: dict[str, Any] | None = None
        for backend, probe in sorted(per_backend.items()):
            result = probe.get("class_results", {}).get(cofactor_class, {})
            auc = result.get("calibration_roc_auc")
            if auc is None:
                continue
            ap = result.get("calibration_average_precision") or 0.0
            candidate = {
                "backend": backend,
                "calibration_roc_auc": auc,
                "calibration_average_precision": result.get("calibration_average_precision"),
                "selected_threshold": (result.get("selected_operating_point") or {}).get("threshold"),
                "low_calibration_support": bool(result.get("low_calibration_support")),
            }
            if best is None or (float(auc), float(ap), backend) > (
                float(best["calibration_roc_auc"]),
                float(best.get("calibration_average_precision") or 0.0),
                str(best["backend"]),
            ):
                best = candidate
        selected[cofactor_class] = best or {"backend": None, "status": "unavailable"}
    return selected


def _channel_predictions(
    *,
    label_rows: list[dict[str, Any]],
    per_backend: dict[str, dict[str, Any]],
    selected_sources: dict[str, Any],
    split_by_entry: dict[str, str],
    cofactor_classes: tuple[str, ...],
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    for row in label_rows:
        entry_id = row["entry_id"]
        families: set[str] = set()
        sources: dict[str, list[str]] = {}
        scores: dict[str, float] = {}
        for cofactor_class in cofactor_classes:
            selected = selected_sources.get(cofactor_class, {})
            backend = selected.get("backend")
            threshold = selected.get("selected_threshold")
            if backend is None or threshold is None:
                continue
            score = (
                per_backend.get(backend, {})
                .get("per_entry_scores", {})
                .get(entry_id, {})
                .get(cofactor_class)
            )
            if score is None:
                continue
            scores[f"{backend}:{cofactor_class}"] = round(float(score), 6)
            if float(score) >= float(threshold):
                families.add(cofactor_class)
                sources.setdefault(cofactor_class, []).append(
                    f"{backend}:{cofactor_class}>={round(float(threshold), 6)}"
                )
        predictions.append(
            {
                "entry_id": entry_id,
                "split_assignment": row.get("split_assignment"),
                "embedding_split": split_by_entry.get(entry_id),
                "label_status": row.get("label_status"),
                "predicted_cofactor_families": sorted(families),
                "prediction_sources": {k: sorted(set(v)) for k, v in sources.items() if v},
                "scores": dict(sorted(scores.items())),
            }
        )
    return sorted(predictions, key=lambda item: _entry_sort_key(item["entry_id"]))


def _prediction_summary(
    channel_predictions: list[dict[str, Any]],
    cofactor_classes: tuple[str, ...],
) -> dict[str, Any]:
    by_split: dict[str, Counter[str]] = {}
    for row in channel_predictions:
        split = str(row.get("split_assignment") or "missing")
        counter = by_split.setdefault(split, Counter())
        counter["rows"] += 1
        for family in row.get("predicted_cofactor_families", []):
            counter[family] += 1
        if not row.get("predicted_cofactor_families"):
            counter["none_predicted"] += 1
    return {
        "predicted_family_counts_by_split": {
            split: dict(sorted(counter.items())) for split, counter in sorted(by_split.items())
        }
    }


def _split_coverage(
    *,
    clean_rows: list[dict[str, Any]],
    split_by_entry: dict[str, str],
    embeddings_by_backend: dict[str, dict[str, list[float]]],
) -> dict[str, Any]:
    in_distribution = [r for r in clean_rows if r["split_assignment"] == "in_distribution"]
    covered = [r for r in in_distribution if r["entry_id"] in split_by_entry]
    coverage_by_split = Counter(split_by_entry.get(r["entry_id"]) for r in covered)
    embedding_join = {
        backend: sum(1 for r in clean_rows if r["entry_id"] in embeddings)
        for backend, embeddings in sorted(embeddings_by_backend.items())
    }
    return {
        "clean_row_count": len(clean_rows),
        "in_distribution_clean_count": len(in_distribution),
        "covered_by_split_manifest": len(covered),
        "covered_split_counts": {k: v for k, v in sorted(coverage_by_split.items()) if k},
        "split_uncovered_in_distribution": len(in_distribution) - len(covered),
        "heldout_clean_count": sum(1 for r in clean_rows if r["split_assignment"] == "heldout"),
        "embedding_join_clean_rows": embedding_join,
    }


def _split_assignment(split_manifest: dict[str, Any]) -> dict[str, str]:
    assignment: dict[str, str] = {}
    for record in split_manifest.get("split_records", []):
        if not isinstance(record, dict):
            continue
        entry_id = record.get("entry_id")
        split = record.get("assigned_embedding_split")
        if entry_id and split:
            assignment[str(entry_id)] = str(split)
    return assignment


def _dense_embeddings(records: list[dict[str, Any]]) -> dict[str, list[float]]:
    return {
        str(record.get("entry_id")): record.get("raw_embedding")
        for record in records
        if isinstance(record, dict)
        and record.get("entry_id")
        and isinstance(record.get("raw_embedding"), list)
    }


def _calibration_report(audit: dict[str, Any]) -> str:
    coverage = audit["split_coverage"]
    lines = [
        "# Cofactor Presence Calibration (leakage-safe train/cal)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "## Guardrails",
        "",
        "- Heads fit on the train split only; thresholds and backend selected on the",
        "  calibration split only; heldout labels never read.",
        "- Supervision is structural ligand context only (no mechanism fingerprint, EC,",
        "  Rhea, mechanism text, or benchmark labels).",
        "",
        "## Split Coverage",
        "",
        f"- Clean rows: {coverage['clean_row_count']}; in-distribution clean: "
        f"{coverage['in_distribution_clean_count']}.",
        f"- Covered by split manifest: {coverage['covered_by_split_manifest']} "
        f"({coverage['covered_split_counts']}).",
        f"- Split-uncovered in-distribution: {coverage['split_uncovered_in_distribution']}; "
        f"heldout clean (scored, truth not read): {coverage['heldout_clean_count']}.",
        "",
        "## Per-class calibration operating points (selected backend)",
        "",
        "| Class | Backend | Cal AUC | Cal AP | Thr | Prec | Recall | F1 | Cal pos | Low support |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for cofactor_class, selected in audit["selected_sources"].items():
        backend = selected.get("backend")
        if not backend:
            lines.append(f"| {cofactor_class} | (none) | - | - | - | - | - | - | - | - |")
            continue
        result = audit["trained_calibrated_heads"][backend]["class_results"][cofactor_class]
        op = result.get("selected_operating_point") or {}
        lines.append(
            f"| {cofactor_class} | {backend} | {result.get('calibration_roc_auc')} | "
            f"{result.get('calibration_average_precision')} | {op.get('threshold')} | "
            f"{op.get('precision')} | {op.get('recall')} | {op.get('f1')} | "
            f"{result.get('calibration_positive_count')} | "
            f"{result.get('low_calibration_support')} |"
        )
    summary = audit["channel_prediction_summary"]["predicted_family_counts_by_split"]
    lines.extend(
        [
            "",
            "## Predicted family counts by split",
            "",
            "```json",
            json.dumps(summary, indent=2, sort_keys=True),
            "```",
            "",
            "## Next step (one-shot, not run here)",
            "",
            "- These per-entry predictions are drop-in compatible with the router",
            "  ligand_context injection in sequence_cofactor_channel. Applying them to",
            "  the heldout mechanism router reads the one-shot heldout mechanism labels",
            "  and must be explicitly authorized before it is run.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _entry_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = str(entry_id).partition(":")
    digits = "".join(ch for ch in suffix if ch.isdigit())
    return (prefix, int(digits) if digits else -1, suffix)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
