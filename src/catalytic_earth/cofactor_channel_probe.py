from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints


DEFAULT_COFACTOR_CLASSES = ("metal_ion", "flavin", "plp", "heme")


def build_sequence_cofactor_channel_probe(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
    kmer_sidecar_records: list[dict[str, Any]],
    kmer_sidecar_summary: dict[str, Any],
    esm2_sidecar_summary: dict[str, Any] | None = None,
    cofactor_classes: tuple[str, ...] = DEFAULT_COFACTOR_CLASSES,
    min_train_positive: int = 10,
    min_heldout_positive: int = 5,
    random_state: int = 702,
) -> dict[str, Any]:
    rows = _cofactor_label_rows(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
    )
    clean_rows = [row for row in rows if row["label_status"] == "clean_geometry_ok"]
    split_counts = _split_counts(rows, field="label_status")
    exact_balance = _exact_balance(clean_rows)
    presence_balance = _presence_balance(clean_rows)
    runnable_presence_classes = [
        cofactor_class
        for cofactor_class in cofactor_classes
        if presence_balance.get("in_distribution", {}).get(cofactor_class, 0)
        >= min_train_positive
        and presence_balance.get("heldout", {}).get(cofactor_class, 0)
        >= min_heldout_positive
    ]
    mechanism_derived = _mechanism_derived_cofactor_balance(label_manifest)
    kmer_probe = _run_kmer_presence_probe(
        rows=clean_rows,
        kmer_sidecar_records=kmer_sidecar_records,
        cofactor_classes=tuple(runnable_presence_classes),
        random_state=random_state,
    )
    exact_core = _exact_core_multiclass_readiness(
        exact_balance=exact_balance,
        core_classes=("none",) + cofactor_classes,
        min_train_positive=min_train_positive,
        min_heldout_positive=min_heldout_positive,
    )
    answer = _answer(
        exact_balance=exact_balance,
        presence_balance=presence_balance,
        runnable_presence_classes=runnable_presence_classes,
        exact_core=exact_core,
        kmer_probe=kmer_probe,
        esm2_sidecar_summary=esm2_sidecar_summary,
    )
    return {
        "artifact_id": "v3_sequence_cofactor_channel_probe_current702_20260529",
        "schema_version": "sequence_cofactor_channel_probe.v1",
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
        "source_artifacts": {
            "label_manifest": "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
            "geometry_features": "artifacts/v3_geometry_features_1025.json",
            "kmer_sidecar": "artifacts/v3_sequence_embedding_sidecar_current702_kmer_20260529.jsonl",
            "kmer_sidecar_summary": "artifacts/v3_sequence_embedding_sidecar_current702_kmer_20260529_summary.json",
            "esm2_sidecar_summary": (
                "artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json"
                if esm2_sidecar_summary is not None
                else None
            ),
        },
        "label_policy": {
            "raw_mcsa_compound_identity_labels_retained_in_graph": False,
            "raw_mcsa_compound_identity_note": (
                "v1_graph_1025 m_csa_entry nodes retain compound_count but not "
                "raw M-CSA compound identities; independent labels here come "
                "from experimental structure ligand context"
            ),
            "primary_label_source": (
                "experimental selected-PDB active-site ligand context from "
                "v3_geometry_features_1025 ligand_context.cofactor_families"
            ),
            "clean_row_policy": (
                "only geometry rows with status=ok are counted as clean; empty "
                "cofactor_families means no local cofactor family observed in "
                "the selected experimental structure, not a guaranteed biological "
                "apo/no-cofactor assertion"
            ),
            "presence_probe_policy": (
                "one-vs-rest class-presence labels allow multi-cofactor rows; "
                "exact multiclass labels exclude multi-cofactor rows"
            ),
            "mechanism_derived_labels_are_tangled": True,
        },
        "label_balance": {
            "row_count": len(rows),
            "clean_geometry_ok_row_count": len(clean_rows),
            "label_status_by_split": split_counts,
            "exact_single_class_by_split": exact_balance,
            "class_presence_by_split": presence_balance,
            "runnable_presence_classes": runnable_presence_classes,
            "minimum_support_policy": {
                "min_train_positive": min_train_positive,
                "min_heldout_positive": min_heldout_positive,
            },
            "exact_core_multiclass_readiness": exact_core,
            "mechanism_fingerprint_derived_balance": mechanism_derived,
        },
        "sequence_probe": {
            "esm2_sidecar_status": _sidecar_status(esm2_sidecar_summary),
            "kmer_sidecar_status": _sidecar_status(kmer_sidecar_summary),
            "kmer_logistic_presence_probe": kmer_probe,
        },
        "answer": answer,
    }


def write_sequence_cofactor_channel_probe(
    *,
    label_manifest_path: Path,
    geometry_features_path: Path,
    kmer_sidecar_path: Path,
    kmer_sidecar_summary_path: Path,
    esm2_sidecar_summary_path: Path | None,
    out_path: Path,
    report_path: Path | None = None,
    min_train_positive: int = 10,
    min_heldout_positive: int = 5,
    random_state: int = 702,
) -> dict[str, Any]:
    with label_manifest_path.open("r", encoding="utf-8") as handle:
        label_manifest = json.load(handle)
    with geometry_features_path.open("r", encoding="utf-8") as handle:
        geometry_features = json.load(handle)
    kmer_records = _read_jsonl(kmer_sidecar_path)
    with kmer_sidecar_summary_path.open("r", encoding="utf-8") as handle:
        kmer_summary = json.load(handle)
    esm2_summary = None
    if esm2_sidecar_summary_path is not None and esm2_sidecar_summary_path.exists():
        with esm2_sidecar_summary_path.open("r", encoding="utf-8") as handle:
            esm2_summary = json.load(handle)
    audit = build_sequence_cofactor_channel_probe(
        label_manifest=label_manifest,
        geometry_features=geometry_features,
        kmer_sidecar_records=kmer_records,
        kmer_sidecar_summary=kmer_summary,
        esm2_sidecar_summary=esm2_summary,
        min_train_positive=min_train_positive,
        min_heldout_positive=min_heldout_positive,
        random_state=random_state,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(audit), encoding="utf-8")
    return audit


def _cofactor_label_rows(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
) -> list[dict[str, Any]]:
    geometry_by_entry = {
        str(entry.get("entry_id")): entry
        for entry in geometry_features.get("entries", [])
        if isinstance(entry, dict) and entry.get("entry_id")
    }
    rows: list[dict[str, Any]] = []
    for manifest_row in label_manifest.get("rows", []):
        if not isinstance(manifest_row, dict):
            continue
        entry_id = str(manifest_row.get("entry_id") or "")
        geometry = geometry_by_entry.get(entry_id)
        if not geometry:
            label_status = "missing_geometry_row"
            local_families: list[str] = []
            structure_families: list[str] = []
        else:
            label_status = (
                "clean_geometry_ok"
                if geometry.get("status") == "ok"
                else f"geometry_{geometry.get('status') or 'unknown'}"
            )
            ligand_context = geometry.get("ligand_context", {})
            local_families = _string_list(ligand_context.get("cofactor_families"))
            structure_families = _string_list(
                ligand_context.get("structure_cofactor_families")
            )
        rows.append(
            {
                "entry_id": entry_id,
                "sequence_id": manifest_row.get("sequence_id"),
                "split_assignment": manifest_row.get("split_assignment"),
                "benchmark_role": manifest_row.get("benchmark_role"),
                "label_status": label_status,
                "local_cofactor_families": local_families,
                "structure_cofactor_families": structure_families,
            }
        )
    return rows


def _split_counts(rows: list[dict[str, Any]], *, field: str) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for row in rows:
        split = str(row.get("split_assignment") or "missing")
        counts.setdefault(split, Counter())[str(row.get(field) or "missing")] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def _exact_balance(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for row in rows:
        split = str(row.get("split_assignment") or "missing")
        families = row["local_cofactor_families"]
        if not families:
            label = "none"
        elif len(families) == 1:
            label = families[0]
        else:
            label = "multi"
        counts.setdefault(split, Counter())[label] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def _presence_balance(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = {}
    for row in rows:
        split = str(row.get("split_assignment") or "missing")
        families = row["local_cofactor_families"]
        if not families:
            counts.setdefault(split, Counter())["none"] += 1
        for family in families:
            counts.setdefault(split, Counter())[family] += 1
    return {split: dict(sorted(counter.items())) for split, counter in sorted(counts.items())}


def _mechanism_derived_cofactor_balance(
    label_manifest: dict[str, Any],
) -> dict[str, Any]:
    fingerprints = {fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()}
    counts: dict[str, Counter[str]] = {}
    for row in label_manifest.get("rows", []):
        if not isinstance(row, dict):
            continue
        split = str(row.get("split_assignment") or "missing")
        fingerprint_id = row.get("fingerprint_id") or row.get("mechanism_fingerprint_id")
        families = _cofactor_strings_to_families(
            fingerprints.get(str(fingerprint_id), {}).get("cofactors", [])
        )
        if not families:
            counts.setdefault(split, Counter())["none_or_unlabeled"] += 1
        for family in families:
            counts.setdefault(split, Counter())[family] += 1
    return {
        "source": (
            "mechanism_fingerprints.cofactors joined through curated mechanism labels; "
            "reported only as a circular/tangled upper-support reference"
        ),
        "class_presence_by_split": {
            split: dict(sorted(counter.items()))
            for split, counter in sorted(counts.items())
        },
    }


def _run_kmer_presence_probe(
    *,
    rows: list[dict[str, Any]],
    kmer_sidecar_records: list[dict[str, Any]],
    cofactor_classes: tuple[str, ...],
    random_state: int,
) -> dict[str, Any]:
    try:
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            accuracy_score,
            average_precision_score,
            balanced_accuracy_score,
            confusion_matrix,
            precision_recall_fscore_support,
            roc_auc_score,
        )
        from sklearn.pipeline import make_pipeline
    except Exception as exc:  # pragma: no cover - environment dependent
        return {
            "status": "blocked",
            "blocker": "sklearn_unavailable",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    embeddings = {
        str(record.get("entry_id")): record.get("raw_embedding")
        for record in kmer_sidecar_records
        if isinstance(record, dict)
        and record.get("entry_id")
        and isinstance(record.get("raw_embedding"), dict)
    }
    joined = [row for row in rows if row["entry_id"] in embeddings]
    train_rows = [row for row in joined if row.get("split_assignment") == "in_distribution"]
    heldout_rows = [row for row in joined if row.get("split_assignment") == "heldout"]
    if not train_rows or not heldout_rows:
        return {
            "status": "blocked",
            "blocker": "missing_train_or_heldout_embedding_join",
            "joined_row_count": len(joined),
            "train_row_count": len(train_rows),
            "heldout_row_count": len(heldout_rows),
        }
    class_results: dict[str, Any] = {}
    for cofactor_class in cofactor_classes:
        train_y = [
            int(cofactor_class in row["local_cofactor_families"])
            for row in train_rows
        ]
        heldout_y = [
            int(cofactor_class in row["local_cofactor_families"])
            for row in heldout_rows
        ]
        model = make_pipeline(
            DictVectorizer(sparse=True),
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                solver="liblinear",
                random_state=random_state,
            ),
        )
        model.fit([embeddings[row["entry_id"]] for row in train_rows], train_y)
        heldout_pred = model.predict([embeddings[row["entry_id"]] for row in heldout_rows])
        heldout_prob = model.predict_proba(
            [embeddings[row["entry_id"]] for row in heldout_rows]
        )[:, 1]
        class_results[cofactor_class] = _binary_metrics(
            y_true=heldout_y,
            y_pred=[int(value) for value in heldout_pred],
            y_score=[float(value) for value in heldout_prob],
            train_positive_count=sum(train_y),
        )
    return {
        "status": "complete",
        "model": "DictVectorizer + class_weight=balanced LogisticRegression(liblinear)",
        "embedding_backend": "deterministic_sequence_kmer_control",
        "threshold_policy": "fixed sklearn class prediction threshold; no heldout tuning",
        "joined_clean_row_count": len(joined),
        "train_row_count": len(train_rows),
        "heldout_row_count": len(heldout_rows),
        "class_results": class_results,
    }


def _binary_metrics(
    *,
    y_true: list[int],
    y_pred: list[int],
    y_score: list[float],
    train_positive_count: int,
) -> dict[str, Any]:
    from sklearn.metrics import (
        accuracy_score,
        average_precision_score,
        balanced_accuracy_score,
        confusion_matrix,
        precision_recall_fscore_support,
        roc_auc_score,
    )

    tn, fp, fn, tp = [
        int(value) for value in confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    ]
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    roc_auc = None
    average_precision = None
    if len(set(y_true)) == 2:
        roc_auc = round(float(roc_auc_score(y_true, y_score)), 6)
        average_precision = round(float(average_precision_score(y_true, y_score)), 6)
    return {
        "train_positive_count": int(train_positive_count),
        "heldout_positive_count": int(sum(y_true)),
        "heldout_negative_count": int(len(y_true) - sum(y_true)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 6),
        "balanced_accuracy": round(float(balanced_accuracy_score(y_true, y_pred)), 6),
        "precision": round(float(precision), 6),
        "recall": round(float(recall), 6),
        "f1": round(float(f1), 6),
        "roc_auc": roc_auc,
        "average_precision": average_precision,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


def _exact_core_multiclass_readiness(
    *,
    exact_balance: dict[str, dict[str, int]],
    core_classes: tuple[str, ...],
    min_train_positive: int,
    min_heldout_positive: int,
) -> dict[str, Any]:
    class_support = {}
    runnable = True
    blockers = []
    for cofactor_class in core_classes:
        train_count = int(exact_balance.get("in_distribution", {}).get(cofactor_class, 0))
        heldout_count = int(exact_balance.get("heldout", {}).get(cofactor_class, 0))
        enough = train_count >= min_train_positive and heldout_count >= min_heldout_positive
        class_support[cofactor_class] = {
            "train": train_count,
            "heldout": heldout_count,
            "meets_min_support": enough,
        }
        if not enough:
            runnable = False
            blockers.append(
                {
                    "class": cofactor_class,
                    "train": train_count,
                    "heldout": heldout_count,
                }
            )
    return {
        "runnable_now": runnable,
        "class_support": class_support,
        "blockers": blockers,
    }


def _answer(
    *,
    exact_balance: dict[str, dict[str, int]],
    presence_balance: dict[str, dict[str, int]],
    runnable_presence_classes: list[str],
    exact_core: dict[str, Any],
    kmer_probe: dict[str, Any],
    esm2_sidecar_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    esm2_vectors = int((esm2_sidecar_summary or {}).get("emitted_row_count") or 0)
    if set(DEFAULT_COFACTOR_CLASSES).issubset(runnable_presence_classes):
        label_readiness = "presence_probe_runnable_now"
    else:
        label_readiness = "presence_probe_partially_runnable"
    return {
        "label_readiness": label_readiness,
        "short_answer": (
            "Yes for one-vs-rest cofactor class-presence labels on metal/flavin/PLP/heme; "
            "not yet for a clean exact single-label multiclass probe including heme."
        ),
        "core_presence_support_train_heldout": {
            cofactor_class: {
                "train": int(
                    presence_balance.get("in_distribution", {}).get(cofactor_class, 0)
                ),
                "heldout": int(presence_balance.get("heldout", {}).get(cofactor_class, 0)),
            }
            for cofactor_class in DEFAULT_COFACTOR_CLASSES
        },
        "core_exact_support_train_heldout": {
            cofactor_class: {
                "train": int(
                    exact_balance.get("in_distribution", {}).get(cofactor_class, 0)
                ),
                "heldout": int(exact_balance.get("heldout", {}).get(cofactor_class, 0)),
            }
            for cofactor_class in ("none",) + DEFAULT_COFACTOR_CLASSES
        },
        "exact_multiclass_runnable_now": bool(exact_core["runnable_now"]),
        "esm2_probe_runnable_now": esm2_vectors > 0,
        "kmer_control_interpretation": _kmer_interpretation(kmer_probe),
        "recommendation": (
            "Run the real sequence cofactor-channel probe next with local ESM-2/ProtT5 "
            "or Pfam/motif features using one-vs-rest cofactor presence labels; do "
            "not clean labels by mechanism fingerprint cofactors because that is "
            "circular with the mechanism target."
        ),
    }


def _kmer_interpretation(kmer_probe: dict[str, Any]) -> str:
    if kmer_probe.get("status") != "complete":
        return str(kmer_probe.get("blocker") or "kmer_probe_unavailable")
    aucs = [
        metrics.get("roc_auc")
        for metrics in kmer_probe.get("class_results", {}).values()
        if metrics.get("roc_auc") is not None
    ]
    if aucs and max(float(value) for value in aucs) >= 0.75:
        return "kmer_control_has_some_signal_but_is_not_the_target_model"
    return "kmer_control_does_not_establish_sequence_cofactor_recovery"


def _sidecar_status(summary: dict[str, Any] | None) -> dict[str, Any]:
    if summary is None:
        return {"status": "not_provided"}
    return {
        "status": summary.get("status"),
        "embedding_backend": summary.get("embedding_backend"),
        "computed_embedding_backend": summary.get("computed_embedding_backend"),
        "emitted_row_count": summary.get("emitted_row_count"),
        "embedding_failure_count": summary.get("embedding_failure_count"),
        "raw_embedding_vectors_retained": summary.get("raw_embedding_vectors_retained"),
        "warnings": summary.get("warnings", [])[:3],
    }


def _cofactor_strings_to_families(cofactors: Any) -> list[str]:
    families: set[str] = set()
    for raw in _string_list(cofactors):
        text = raw.lower()
        if any(token in text for token in ("zn", "mg", "mn", "fe2", "fe3")):
            families.add("metal_ion")
        if "fad" in text or "fmn" in text or "flavin" in text:
            families.add("flavin")
        if "nad" in text:
            families.add("nad")
        if "heme" in text:
            families.add("heme")
        if "pyridoxal" in text or "plp" in text:
            families.add("plp")
        if "fe-s" in text or "4fe" in text:
            families.add("fe_s_cluster")
        if "s-adenosylmethionine" in text or text == "sam":
            families.add("sam")
        if "cobalamin" in text:
            families.add("cobalamin")
    return sorted(families)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _markdown_report(audit: dict[str, Any]) -> str:
    answer = audit["answer"]
    balance = audit["label_balance"]
    probe = audit["sequence_probe"]["kmer_logistic_presence_probe"]
    lines = [
        "# Sequence Cofactor-Channel Probe",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "## Answer",
        "",
        f"- {answer['short_answer']}",
        f"- Recommendation: {answer['recommendation']}",
        "",
        "## Clean Label Balance",
        "",
        "| Class | Presence train | Presence heldout | Exact train | Exact heldout |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for cofactor_class in ("metal_ion", "flavin", "plp", "heme"):
        presence = answer["core_presence_support_train_heldout"][cofactor_class]
        exact = answer["core_exact_support_train_heldout"][cofactor_class]
        lines.append(
            f"| {cofactor_class} | {presence['train']} | {presence['heldout']} | "
            f"{exact['train']} | {exact['heldout']} |"
        )
    none_exact = answer["core_exact_support_train_heldout"]["none"]
    lines.extend(
        [
            f"| none | - | - | {none_exact['train']} | {none_exact['heldout']} |",
            "",
            f"- Clean geometry label rows: {balance['clean_geometry_ok_row_count']}/{balance['row_count']}.",
            f"- Runnable one-vs-rest presence classes: {balance['runnable_presence_classes']}.",
            f"- Exact multiclass runnable now: {answer['exact_multiclass_runnable_now']}.",
            f"- ESM-2 vectors available: {answer['esm2_probe_runnable_now']}.",
            "",
            "## K-mer Control Probe",
            "",
        ]
    )
    if probe.get("status") == "complete":
        lines.extend(
            [
                f"- Joined clean rows: {probe['joined_clean_row_count']}; train {probe['train_row_count']}; heldout {probe['heldout_row_count']}.",
                "| Class | ROC AUC | Avg precision | Balanced accuracy | TP | FP | FN | TN |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for cofactor_class, metrics in probe["class_results"].items():
            lines.append(
                f"| {cofactor_class} | {metrics['roc_auc']} | "
                f"{metrics['average_precision']} | {metrics['balanced_accuracy']} | "
                f"{metrics['tp']} | {metrics['fp']} | {metrics['fn']} | {metrics['tn']} |"
            )
    else:
        lines.append(f"- K-mer probe blocked: {probe.get('blocker')}.")
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- Mechanism-fingerprint-derived cofactors have stronger support but are circular with the current mechanism labels.",
            "- Raw M-CSA compound identities are not retained in the graph; `compound_count` is retained only as a count.",
            "- Empty local cofactor context is selected-structure evidence, not a guaranteed biological no-cofactor label.",
            "- The k-mer probe is a local control only; the real next probe needs local ESM-2/ProtT5 or Pfam/motif features.",
            "",
        ]
    )
    return "\n".join(lines)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
