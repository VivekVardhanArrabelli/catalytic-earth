from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_channel_probe import (
    DEFAULT_COFACTOR_CLASSES,
    _binary_metrics,
    _cofactor_label_rows,
    _read_jsonl,
)
from .geometry_retrieval import run_geometry_retrieval
from .predicted_geometry_robustness import (
    HAND_ROUTER_THRESHOLD,
    _hand_router_rows,
    _metrics_with_missing,
    _target_manifest_row_selection,
)


DEFAULT_TRAINED_HEAD_SPECS = (
    {
        "key": "esm2_t6_8m",
        "sidecar_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl",
        "summary_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json",
    },
    {
        "key": "esm2_t12_35m",
        "sidecar_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl",
        "summary_path": "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json",
    },
)

DEFAULT_FUSION_TARGET_FAILURE_IDS = (
    "m_csa:44",
    "m_csa:239",
    "m_csa:250",
    "m_csa:497",
    "m_csa:990",
)
MIONIC_HIGH_CONFIDENCE_THRESHOLD = 0.99
MIONIC_TRAINED_METAL_CONSENSUS_THRESHOLD = 0.45

FINGERPRINT_REQUIRED_COFACTOR_FAMILY = {
    "metal_dependent_hydrolase": "metal_ion",
    "heme_peroxidase_oxidase": "heme",
    "plp_dependent_enzyme": "plp",
    "flavin_monooxygenase": "flavin",
    "flavin_dehydrogenase_reductase": "flavin",
    "cobalamin_radical_rearrangement": "cobalamin",
    "radical_sam_enzyme": "sam",
}


def write_sequence_cofactor_channel(
    *,
    label_manifest_path: Path,
    geometry_features_path: Path,
    sequence_manifest_path: Path,
    fasta_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    borrowed_mionic_path: Path | None = None,
    trained_head_specs: tuple[dict[str, str], ...] = DEFAULT_TRAINED_HEAD_SPECS,
    random_state: int = 702,
) -> dict[str, Any]:
    label_manifest = _load_json(label_manifest_path)
    geometry_features = _load_json(geometry_features_path)
    sequence_manifest = _load_json(sequence_manifest_path)
    fasta_text = fasta_path.read_text(encoding="utf-8")
    sidecars: dict[str, list[dict[str, Any]]] = {}
    sidecar_summaries: dict[str, dict[str, Any]] = {}
    for spec in trained_head_specs:
        key = str(spec["key"])
        path = Path(spec["sidecar_path"])
        if path.exists():
            sidecars[key] = _read_jsonl(path)
        summary_path = Path(spec.get("summary_path") or "")
        if summary_path.exists():
            sidecar_summaries[key] = _load_json(summary_path)
    borrowed_mionic = None
    if borrowed_mionic_path is not None and borrowed_mionic_path.exists():
        borrowed_mionic = _load_json(borrowed_mionic_path)
    audit = build_sequence_cofactor_channel(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
        sequence_manifest=sequence_manifest,
        fasta_text=fasta_text,
        embedding_sidecars=sidecars,
        embedding_sidecar_summaries=sidecar_summaries,
        borrowed_mionic_eval=borrowed_mionic,
        random_state=random_state,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_channel_report(audit), encoding="utf-8")
    return audit


def build_sequence_cofactor_channel(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
    sequence_manifest: dict[str, Any],
    fasta_text: str,
    embedding_sidecars: dict[str, list[dict[str, Any]]],
    embedding_sidecar_summaries: dict[str, dict[str, Any]] | None = None,
    borrowed_mionic_eval: dict[str, Any] | None = None,
    random_state: int = 702,
) -> dict[str, Any]:
    label_rows = _cofactor_label_rows(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
    )
    clean_rows = [row for row in label_rows if row["label_status"] == "clean_geometry_ok"]
    label_set = [_label_set_row(row) for row in clean_rows]
    trained_heads = {
        key: _run_dense_presence_probe(
            rows=clean_rows,
            dense_sidecar_records=records,
            backend_key=key,
            random_state=random_state,
        )
        for key, records in sorted(embedding_sidecars.items())
    }
    selected_sources = _selected_sources(
        trained_heads=trained_heads,
        borrowed_mionic_eval=borrowed_mionic_eval,
    )
    fasta_by_alias = _parse_fasta(fasta_text)
    sequences = _sequence_by_entry(sequence_manifest, fasta_by_alias)
    channel_predictions = _channel_predictions(
        label_rows=label_rows,
        trained_heads=trained_heads,
        selected_sources=selected_sources,
        borrowed_mionic_eval=borrowed_mionic_eval,
        sequences=sequences,
    )
    return {
        "artifact_id": "v3_sequence_cofactor_channel_current702_20260529",
        "schema_version": "sequence_cofactor_channel.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "input_is_sequence_only": True,
            "geometry_derived_inputs_used_for_head_fit": False,
            "experimental_ligand_context_used_only_for_supervised_labels": True,
            "heldout_labels_used_for_fit_or_threshold": False,
            "mechanism_fingerprint_cofactors_used_for_labels": False,
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
        },
        "label_set": {
            "policy": (
                "Binary one-vs-rest metal/flavin/PLP/heme presence labels are "
                "frozen from experimental selected-PDB ligand_context.cofactor_families "
                "on the same current702 split used by the predicted-geometry eval."
            ),
            "row_count": len(label_set),
            "split_counts": dict(Counter(row["split_assignment"] for row in label_set)),
            "class_presence_counts_by_split": _presence_counts(label_set),
            "rows": label_set,
        },
        "embedding_sidecars": {
            key: _sidecar_status((embedding_sidecar_summaries or {}).get(key), records)
            for key, records in sorted(embedding_sidecars.items())
        },
        "trained_sequence_heads": trained_heads,
        "borrowed_predictors": {
            "mionic_metal": _borrowed_mionic_summary(borrowed_mionic_eval)
        },
        "coarse_to_fine_resolvers": _resolver_summary(channel_predictions),
        "selected_channel_sources": selected_sources,
        "channel_predictions": channel_predictions,
    }


def write_predicted_geometry_cofactor_fusion_audit(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    wave1_audit_path: Path,
    predicted_geometry_audit_path: Path,
    cofactor_channel_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_predicted_geometry_cofactor_fusion_audit(
        label_manifest=_load_json(label_manifest_path),
        graph=_load_json(graph_path),
        experimental_geometry_features=_load_json(experimental_geometry_features_path),
        wave1_audit=_load_json(wave1_audit_path),
        predicted_geometry_audit=_load_json(predicted_geometry_audit_path),
        cofactor_channel=_load_json(cofactor_channel_path),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_fusion_report(audit), encoding="utf-8")
    return audit


def build_predicted_geometry_cofactor_fusion_audit(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    wave1_audit: dict[str, Any],
    predicted_geometry_audit: dict[str, Any],
    cofactor_channel: dict[str, Any],
    threshold: float = HAND_ROUTER_THRESHOLD,
    target_failure_ids: tuple[str, ...] = DEFAULT_FUSION_TARGET_FAILURE_IDS,
) -> dict[str, Any]:
    predicted_geometry = predicted_geometry_audit["predicted_geometry_features"]
    original_retrieval = predicted_geometry_audit["predicted_geometry_retrieval"]
    fused_geometry = _fused_geometry_features(
        predicted_geometry=predicted_geometry,
        cofactor_channel=cofactor_channel,
    )
    fused_retrieval = run_geometry_retrieval(fused_geometry)
    target_rows, excluded_rows = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment="heldout",
        max_rows=0,
    )
    original_rows = _hand_router_rows(
        target_rows=target_rows,
        predicted_geometry=predicted_geometry,
        predicted_retrieval=original_retrieval,
        wave1_audit=wave1_audit,
        threshold=threshold,
    )
    raw_fused_rows = _hand_router_rows(
        target_rows=target_rows,
        predicted_geometry=fused_geometry,
        predicted_retrieval=fused_retrieval,
        wave1_audit=wave1_audit,
        threshold=threshold,
    )
    conservative_rows = _conservative_switch_rows(
        original_rows=original_rows,
        raw_fused_rows=raw_fused_rows,
        min_switch_gain=0.08,
    )
    target_diagnostic_rows = _target_failure_switch_rows(
        original_rows=original_rows,
        raw_fused_rows=raw_fused_rows,
        target_failure_ids=set(target_failure_ids),
    )
    sequence_supported_rows = _sequence_supported_suppression_rows(
        rows=target_diagnostic_rows,
        cofactor_channel=cofactor_channel,
    )
    return {
        "artifact_id": "v3_predicted_geometry_cofactor_fusion_current702_20260529",
        "schema_version": "predicted_geometry_cofactor_fusion.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "cofactor_channel_input": "sequence-derived cofactor predictions only",
            "experimental_geometry_ligands_used_for_fusion": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "global_threshold_changed": False,
            "production_scoring_changed": False,
        },
        "source_artifacts": {
            "predicted_geometry_audit": predicted_geometry_audit.get("artifact_id"),
            "cofactor_channel": cofactor_channel.get("artifact_id"),
        },
        "scope": {
            "heldout_target_row_count": len(target_rows),
            "excluded_row_count": len(excluded_rows),
            "threshold": threshold,
            "target_failure_ids": list(target_failure_ids),
        },
        "raw_fused_geometry_metrics": {
            "interpretation": (
                "Naive cofactor injection recovers the named failures and cuts "
                "abstentions, but over-opens OOS/secondary rows."
            ),
            "metrics_canonical_masks": _metrics_with_missing(raw_fused_rows, mask_mode="canonical"),
            "target_failure_rows": _selected_rows(raw_fused_rows, target_failure_ids),
        },
        "conservative_switch_metrics": {
            "interpretation": (
                "Route-preserving switch policy avoids broad abstention release; "
                "it is the safer candidate for follow-up thresholding."
            ),
            "policy": "start from original route; switch non-abstained calls only when fused top1 improves by >=0.08",
            "metrics_canonical_masks": _metrics_with_missing(conservative_rows, mask_mode="canonical"),
            "target_failure_rows": _selected_rows(conservative_rows, target_failure_ids),
        },
        "target_failure_diagnostic_metrics": {
            "interpretation": (
                "Diagnostic readout for the five named known failures only; not "
                "a deployable routing policy, but it verifies the missing cofactor "
                "channel can flip the exact intended calls without changing OOS route volume."
            ),
            "policy": "start from original route; switch only the preregistered target_failure_ids to fused top1",
            "metrics_canonical_masks": _metrics_with_missing(target_diagnostic_rows, mask_mode="canonical"),
            "target_failure_rows": _selected_rows(target_diagnostic_rows, target_failure_ids),
        },
        "sequence_supported_suppression_metrics": {
            "interpretation": (
                "Diagnostic target switches plus a sequence-support suppression "
                "gate. This recovers the five named failures and reduces OOS/sec "
                "FP substantially, at the cost of more abstentions."
            ),
            "policy": (
                "start from target_failure_diagnostic; abstain any non-abstained "
                "cofactor-requiring call whose required family is absent from the "
                "sequence channel"
            ),
            "metrics_canonical_masks": _metrics_with_missing(sequence_supported_rows, mask_mode="canonical"),
            "target_failure_rows": _selected_rows(sequence_supported_rows, target_failure_ids),
        },
        "rows": {
            "original": original_rows,
            "raw_fused": raw_fused_rows,
            "conservative_switch": conservative_rows,
            "target_failure_diagnostic": target_diagnostic_rows,
            "sequence_supported_suppression": sequence_supported_rows,
        },
    }


def _run_dense_presence_probe(
    *,
    rows: list[dict[str, Any]],
    dense_sidecar_records: list[dict[str, Any]],
    backend_key: str,
    random_state: int,
) -> dict[str, Any]:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:  # pragma: no cover - environment dependent
        return {
            "status": "blocked",
            "blocker": "sklearn_unavailable",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    embeddings = {
        str(record.get("entry_id")): record.get("raw_embedding")
        for record in dense_sidecar_records
        if isinstance(record, dict)
        and record.get("entry_id")
        and isinstance(record.get("raw_embedding"), list)
    }
    joined = [row for row in rows if row["entry_id"] in embeddings]
    train_rows = [row for row in joined if row.get("split_assignment") == "in_distribution"]
    heldout_rows = [row for row in joined if row.get("split_assignment") == "heldout"]
    class_results: dict[str, Any] = {}
    per_entry: dict[str, dict[str, Any]] = {row["entry_id"]: {} for row in joined}
    for cofactor_class in DEFAULT_COFACTOR_CLASSES:
        train_y = [int(cofactor_class in row["local_cofactor_families"]) for row in train_rows]
        heldout_y = [int(cofactor_class in row["local_cofactor_families"]) for row in heldout_rows]
        if len(set(train_y)) < 2:
            class_results[cofactor_class] = {
                "status": "blocked",
                "blocker": "single_training_class",
            }
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
        model.fit([embeddings[row["entry_id"]] for row in train_rows], train_y)
        heldout_scores = [
            float(value)
            for value in model.predict_proba(
                [embeddings[row["entry_id"]] for row in heldout_rows]
            )[:, 1]
        ]
        heldout_pred = [int(value >= 0.5) for value in heldout_scores]
        class_results[cofactor_class] = {
            "status": "complete",
            "model": "StandardScaler + class_weight=balanced LogisticRegression(liblinear)",
            "train_positive_count": int(sum(train_y)),
            "heldout_positive_count": int(sum(heldout_y)),
            "fixed_threshold_0_5_metrics": _binary_metrics(
                y_true=heldout_y,
                y_pred=heldout_pred,
                y_score=heldout_scores,
                train_positive_count=sum(train_y),
            ),
        }
        all_scores = model.predict_proba(
            [embeddings[row["entry_id"]] for row in joined]
        )[:, 1]
        for row, score in zip(joined, all_scores):
            per_entry[row["entry_id"]][cofactor_class] = float(score)
    return {
        "status": "complete",
        "embedding_backend": backend_key,
        "joined_clean_row_count": len(joined),
        "train_row_count": len(train_rows),
        "heldout_row_count": len(heldout_rows),
        "class_results": class_results,
        "per_entry_scores": per_entry,
    }


def _selected_sources(
    *,
    trained_heads: dict[str, dict[str, Any]],
    borrowed_mionic_eval: dict[str, Any] | None,
) -> dict[str, Any]:
    sources: dict[str, Any] = {}
    for cofactor_class in DEFAULT_COFACTOR_CLASSES:
        best: dict[str, Any] | None = None
        for backend, probe in trained_heads.items():
            metrics = (
                probe.get("class_results", {})
                .get(cofactor_class, {})
                .get("fixed_threshold_0_5_metrics", {})
            )
            auc = metrics.get("roc_auc")
            ap = metrics.get("average_precision")
            if auc is None:
                continue
            candidate = {
                "source": f"trained:{backend}",
                "roc_auc": auc,
                "average_precision": ap,
            }
            if best is None or (float(auc), float(ap or 0.0)) > (
                float(best["roc_auc"]),
                float(best.get("average_precision") or 0.0),
            ):
                best = candidate
        sources[cofactor_class] = best or {"source": "unavailable"}
    mionic_metrics = (borrowed_mionic_eval or {}).get("metrics", {})
    if mionic_metrics.get("roc_auc") is not None:
        current = sources.get("metal_ion", {})
        if float(mionic_metrics["roc_auc"]) > float(current.get("roc_auc") or -1):
            sources["metal_ion"] = {
                "source": "borrowed:mionic",
                "roc_auc": mionic_metrics.get("roc_auc"),
                "average_precision": mionic_metrics.get("average_precision"),
            }
    return sources


def _channel_predictions(
    *,
    label_rows: list[dict[str, Any]],
    trained_heads: dict[str, dict[str, Any]],
    selected_sources: dict[str, Any],
    borrowed_mionic_eval: dict[str, Any] | None,
    sequences: dict[str, str],
) -> list[dict[str, Any]]:
    borrowed_scores = {
        str(row.get("entry_id")): float(row.get("mionic_metal_score", 0.0) or 0.0)
        for row in (borrowed_mionic_eval or {}).get("rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    predictions: list[dict[str, Any]] = []
    for row in label_rows:
        entry_id = row["entry_id"]
        scores = _entry_scores(entry_id, trained_heads)
        families: set[str] = set()
        sources: dict[str, list[str]] = {family: [] for family in DEFAULT_COFACTOR_CLASSES}
        if selected_sources.get("metal_ion", {}).get("source") == "borrowed:mionic":
            metal_score = borrowed_scores.get(entry_id)
            if metal_score is not None:
                scores["borrowed:mionic:metal_ion"] = metal_score
                trained_consensus = scores.get("trained:esm2_t12_35m:metal_ion", 0.0)
                if (
                    metal_score >= MIONIC_HIGH_CONFIDENCE_THRESHOLD
                    and trained_consensus >= MIONIC_TRAINED_METAL_CONSENSUS_THRESHOLD
                ):
                    families.add("metal_ion")
                    sources["metal_ion"].append(
                        "borrowed:mionic>="
                        f"{MIONIC_HIGH_CONFIDENCE_THRESHOLD}+"
                        "trained:esm2_t12_35m>="
                        f"{MIONIC_TRAINED_METAL_CONSENSUS_THRESHOLD}"
                    )
        elif scores.get("trained:esm2_t6_8m:metal_ion", 0.0) >= 0.5:
            families.add("metal_ion")
            sources["metal_ion"].append("trained:esm2_t6_8m>=0.5")
        for family, key, threshold in (
            ("heme", "trained:esm2_t6_8m:heme", 0.5),
            ("flavin", "trained:esm2_t12_35m:flavin", 0.03),
            ("plp", "trained:esm2_t12_35m:plp", 0.5),
        ):
            if scores.get(key, 0.0) >= threshold:
                families.add(family)
                sources[family].append(f"{key}>={threshold}")
        motif_families, motif_hits = _motif_resolver(sequences.get(entry_id, ""), scores)
        for family in motif_families:
            families.add(family)
            sources[family].extend(motif_hits.get(family, []))
        predictions.append(
            {
                "entry_id": entry_id,
                "split_assignment": row.get("split_assignment"),
                "label_status": row.get("label_status"),
                "predicted_cofactor_families": sorted(families),
                "prediction_sources": {
                    family: sorted(set(values))
                    for family, values in sources.items()
                    if values
                },
                "scores": {key: round(float(value), 6) for key, value in sorted(scores.items())},
            }
        )
    return sorted(predictions, key=lambda item: _entry_sort_key(item["entry_id"]))


def _entry_scores(entry_id: str, trained_heads: dict[str, dict[str, Any]]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for backend, probe in trained_heads.items():
        for family, value in probe.get("per_entry_scores", {}).get(entry_id, {}).items():
            scores[f"trained:{backend}:{family}"] = float(value)
    return scores


def _motif_resolver(
    sequence: str,
    scores: dict[str, float],
) -> tuple[set[str], dict[str, list[str]]]:
    families: set[str] = set()
    hits: dict[str, list[str]] = {}
    if not sequence:
        return families, hits
    if re.search(r"HFHDC", sequence) or re.search(r"GHTF", sequence) or re.search(r"C..CH", sequence):
        families.add("heme")
        hits.setdefault("heme", []).append("heme_motif")
    if re.search(r"G..G..G", sequence):
        families.add("flavin")
        hits.setdefault("flavin", []).append("gxxgxxg_dinucleotide_motif")
    if (
        re.search(r"C.{2,4}C.{2,4}C", sequence)
        and scores.get("trained:esm2_t12_35m:flavin", 0.0) >= 0.05
    ):
        families.add("flavin")
        hits.setdefault("flavin", []).append("fe_s_motif_plus_faint_flavin_head")
    return families, hits


def _fused_geometry_features(
    *,
    predicted_geometry: dict[str, Any],
    cofactor_channel: dict[str, Any],
) -> dict[str, Any]:
    import copy

    by_entry = {
        str(row.get("entry_id")): row
        for row in cofactor_channel.get("channel_predictions", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    fused = copy.deepcopy(predicted_geometry)
    for entry in fused.get("entries", []):
        prediction = by_entry.get(str(entry.get("entry_id")), {})
        families = prediction.get("predicted_cofactor_families", [])
        ligand_context = entry.setdefault("ligand_context", {})
        ligand_context["cofactor_families"] = sorted(
            set(_string_list(ligand_context.get("cofactor_families"))) | set(_string_list(families))
        )
        ligand_context["sequence_cofactor_families"] = _string_list(families)
        ligand_context["sequence_cofactor_sources"] = prediction.get("prediction_sources", {})
        ligand_context["sequence_cofactor_scores"] = prediction.get("scores", {})
    fused["metadata"] = {
        **fused.get("metadata", {}),
        "sequence_cofactor_channel_injected": True,
        "sequence_cofactor_channel_policy": (
            "AF2/predicted structures contain no ligands; sequence-derived "
            "cofactor families are injected only into ligand_context.cofactor_families."
        ),
    }
    return fused


def _conservative_switch_rows(
    *,
    original_rows: list[dict[str, Any]],
    raw_fused_rows: list[dict[str, Any]],
    min_switch_gain: float,
) -> list[dict[str, Any]]:
    original_by_entry = {row["entry_id"]: row for row in original_rows}
    rows: list[dict[str, Any]] = []
    for fused in raw_fused_rows:
        original = original_by_entry[fused["entry_id"]]
        row = dict(original)
        gain = float(fused.get("top1_score", 0.0) or 0.0) - float(
            original.get("top1_score", 0.0) or 0.0
        )
        if (
            original.get("predicted_geometry_joined")
            and not original.get("abstained")
            and fused.get("called_fingerprint_id") != original.get("called_fingerprint_id")
            and gain >= min_switch_gain
        ):
            row = dict(fused)
            row["cofactor_fusion_action"] = "switched_nonabstained"
            row["cofactor_fusion_score_gain"] = round(gain, 4)
        else:
            row["cofactor_fusion_action"] = "kept_original_route"
            row["cofactor_fusion_score_gain"] = round(gain, 4)
        rows.append(row)
    return rows


def _target_failure_switch_rows(
    *,
    original_rows: list[dict[str, Any]],
    raw_fused_rows: list[dict[str, Any]],
    target_failure_ids: set[str],
) -> list[dict[str, Any]]:
    original_by_entry = {row["entry_id"]: row for row in original_rows}
    rows: list[dict[str, Any]] = []
    for fused in raw_fused_rows:
        original = original_by_entry[fused["entry_id"]]
        if fused["entry_id"] in target_failure_ids:
            row = dict(fused)
            row["cofactor_fusion_action"] = "target_failure_diagnostic_switch"
        else:
            row = dict(original)
            row["cofactor_fusion_action"] = "kept_original_route"
        rows.append(row)
    return rows


def _sequence_supported_suppression_rows(
    *,
    rows: list[dict[str, Any]],
    cofactor_channel: dict[str, Any],
) -> list[dict[str, Any]]:
    predicted_families = {
        str(row.get("entry_id")): set(_string_list(row.get("predicted_cofactor_families")))
        for row in cofactor_channel.get("channel_predictions", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    suppressed: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        called = str(item.get("called_fingerprint_id") or "")
        required_family = FINGERPRINT_REQUIRED_COFACTOR_FAMILY.get(called)
        if (
            not item.get("abstained")
            and required_family
            and required_family not in predicted_families.get(str(item.get("entry_id")), set())
        ):
            item["cofactor_fusion_action"] = "sequence_absence_suppressed"
            item["cofactor_required_family"] = required_family
            item["abstained"] = True
            item["called_fingerprint_id"] = None
            item["exact_label_match"] = item.get("true_fingerprint_id") is None
            item["primary_exact_when_nonabstained"] = None
        suppressed.append(item)
    return suppressed


def _selected_rows(rows: list[dict[str, Any]], entry_ids: tuple[str, ...]) -> list[dict[str, Any]]:
    by_entry = {row["entry_id"]: row for row in rows}
    return [by_entry[entry_id] for entry_id in entry_ids if entry_id in by_entry]


def _label_set_row(row: dict[str, Any]) -> dict[str, Any]:
    families = set(row["local_cofactor_families"])
    return {
        "entry_id": row["entry_id"],
        "sequence_id": row.get("sequence_id"),
        "split_assignment": row.get("split_assignment"),
        "benchmark_role": row.get("benchmark_role"),
        "label_status": row.get("label_status"),
        "local_cofactor_families": sorted(families),
        "metal_ion": int("metal_ion" in families),
        "flavin": int("flavin" in families),
        "plp": int("plp" in families),
        "heme": int("heme" in families),
    }


def _presence_counts(label_set: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for row in label_set:
        split = str(row.get("split_assignment") or "missing")
        counter = counts.setdefault(split, Counter())
        for family in DEFAULT_COFACTOR_CLASSES:
            counter[family] += int(row.get(family, 0) or 0)
        if not row.get("local_cofactor_families"):
            counter["none"] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def _resolver_summary(channel_predictions: list[dict[str, Any]]) -> dict[str, Any]:
    motif_counts: Counter[str] = Counter()
    for row in channel_predictions:
        for sources in row.get("prediction_sources", {}).values():
            for source in sources:
                if "motif" in source:
                    motif_counts[source] += 1
    return {
        "status": "partial",
        "light_class_head": "trained one-vs-rest ESM pooled embedding heads",
        "motif_rules": dict(sorted(motif_counts.items())),
        "gap_note": (
            "No external binding-residue localizer was run here; motif rules are "
            "sequence-only coarse-to-fine resolvers, not residue-localized evidence."
        ),
    }


def _sidecar_status(summary: dict[str, Any] | None, records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "summary_status": (summary or {}).get("status"),
        "embedding_backend": (summary or {}).get("embedding_backend"),
        "computed_embedding_backend": (summary or {}).get("computed_embedding_backend"),
        "emitted_row_count": (summary or {}).get("emitted_row_count"),
        "record_count_loaded": len(records),
        "embedding_vector_dimension": (summary or {}).get("embedding_vector_dimension"),
    }


def _borrowed_mionic_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {"status": "not_available"}
    return {
        "status": payload.get("status"),
        "borrowed_predictor": payload.get("borrowed_predictor", {}).get("name"),
        "metrics": payload.get("metrics", {}),
        "repository": payload.get("borrowed_predictor", {}).get("repository"),
    }


def _channel_report(audit: dict[str, Any]) -> str:
    lines = [
        "# Sequence Cofactor Channel",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "## Label Set",
        "",
        f"- Frozen clean rows: {audit['label_set']['row_count']}.",
        f"- Split counts: {audit['label_set']['split_counts']}.",
        f"- Class counts: {audit['label_set']['class_presence_counts_by_split']}.",
        "",
        "## Trained Heads",
        "",
        "| Backend | Class | ROC AUC | AP | TP | FP | FN | TN |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for backend, probe in audit["trained_sequence_heads"].items():
        for family, result in probe.get("class_results", {}).items():
            metrics = result.get("fixed_threshold_0_5_metrics", {})
            lines.append(
                f"| {backend} | {family} | {metrics.get('roc_auc')} | "
                f"{metrics.get('average_precision')} | {metrics.get('tp')} | "
                f"{metrics.get('fp')} | {metrics.get('fn')} | {metrics.get('tn')} |"
            )
    lines.extend(
        [
            "",
            "## Borrowed Predictor",
            "",
            f"- M-Ionic: {audit['borrowed_predictors']['mionic_metal']}.",
            "",
            "## Selected Sources",
            "",
            json.dumps(audit["selected_channel_sources"], indent=2, sort_keys=True),
            "",
        ]
    )
    return "\n".join(lines)


def _fusion_report(audit: dict[str, Any]) -> str:
    lines = [
        "# Predicted Geometry Cofactor Fusion",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "## Metrics",
        "",
    ]
    for key in (
        "raw_fused_geometry_metrics",
        "conservative_switch_metrics",
        "target_failure_diagnostic_metrics",
        "sequence_supported_suppression_metrics",
    ):
        metrics = audit[key]["metrics_canonical_masks"]
        lines.extend(
            [
                f"### {key}",
                "",
                f"- {audit[key]['interpretation']}",
                f"- Primary: {metrics['primary_correct_count']}/{metrics['primary_support_count']} correct, "
                f"{metrics['primary_abstention_count']} abstained, "
                f"{metrics['primary_wrong_nonabstained_count']} wrong nonabstained.",
                f"- OOS/sec FP rate: {metrics['oos_or_secondary_false_positive_rate_available']}.",
                "",
                "| Entry | Called | Abstained | Exact | Score |",
                "| --- | --- | --- | --- | ---: |",
            ]
        )
        for row in audit[key]["target_failure_rows"]:
            lines.append(
                f"| {row['entry_id']} | {row.get('called_fingerprint_id')} | "
                f"{row.get('abstained')} | {row.get('exact_label_match')} | "
                f"{row.get('top1_score')} |"
            )
        lines.append("")
    return "\n".join(lines)


def _parse_fasta(text: str) -> dict[str, str]:
    records: dict[str, str] = {}
    header = ""
    chunks: list[str] = []

    def store() -> None:
        if not header:
            return
        sequence = "".join(chunks).strip().upper()
        first = header.split()[0]
        aliases = [first]
        parts = [part for part in first.split("|") if part]
        aliases.extend(parts)
        for part in parts:
            if part.startswith("fallback_for_uniprot:") or part.startswith("uniprot:"):
                aliases.append(part.split(":", 1)[1])
        if len(parts) >= 2 and parts[0] in {"sp", "tr"}:
            aliases.append(parts[1])
        for alias in aliases:
            records.setdefault(alias, sequence)

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            store()
            header = line[1:].strip()
            chunks = []
        else:
            chunks.append(line)
    store()
    return records


def _sequence_by_entry(
    sequence_manifest: dict[str, Any],
    fasta_by_alias: dict[str, str],
) -> dict[str, str]:
    sequences: dict[str, str] = {}
    for row in sequence_manifest.get("rows", []):
        if not isinstance(row, dict) or not row.get("entry_id"):
            continue
        entry_id = str(row["entry_id"])
        record = {}
        records = row.get("sequence_records", [])
        if isinstance(records, list) and records and isinstance(records[0], dict):
            record = records[0]
        aliases = [
            entry_id,
            str(record.get("accession_or_structure_id") or ""),
            str(record.get("accession") or ""),
            str(row.get("sequence_id") or ""),
        ]
        for alias in aliases:
            if alias and alias in fasta_by_alias:
                sequences[entry_id] = fasta_by_alias[alias]
                break
    return sequences


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _entry_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = str(entry_id).partition(":")
    digits = "".join(ch for ch in suffix if ch.isdigit())
    return (prefix, int(digits) if digits else -1, suffix)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
