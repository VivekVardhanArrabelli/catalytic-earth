from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from .labels import MechanismLabel


FORBIDDEN_REPRESENTATION_FEATURES = [
    "mechanism_text",
    "entry_name",
    "ec_labels",
    "rhea_identifiers",
    "source_entry_ids",
    "expert_notes",
    "review_decision_text",
    "mechanism_prose",
]


def build_representation_baseline_shootout_plan(
    labels: list[MechanismLabel],
    *,
    learned_manifest: dict[str, Any] | None = None,
    sequence_holdout_eval: dict[str, Any] | None = None,
    learning_signal_manifest: dict[str, Any] | None = None,
    rejected_signal_taxonomy: dict[str, Any] | None = None,
    exact_true_reject_signal: dict[str, Any] | None = None,
    external_kmer_sample: dict[str, Any] | None = None,
    external_esm_sample: dict[str, Any] | None = None,
    sequence_fasta_text: str | None = None,
    kmer_size: int = 3,
    max_smoke_heldout: int = 160,
) -> dict[str, Any]:
    """Build a leakage-aware representation baseline plan without training a model."""
    registry_role_rows = [_registry_role_row(label) for label in labels]
    registry_role_counts = Counter(row["benchmark_role"] for row in registry_role_rows)
    label_scope_counts = Counter(_label_scope(label.entry_id) for label in labels)
    registry_label_type_counts = Counter(label.label_type for label in labels)
    registry_review_status_counts = Counter(label.review_status for label in labels)
    registry_tier_counts = Counter(label.tier for label in labels)
    registry_fingerprint_counts = Counter(
        label.fingerprint_id or "out_of_scope" for label in labels
    )

    manifest_rows = (
        learned_manifest.get("rows", [])
        if isinstance(learned_manifest, dict)
        else []
    )
    manifest_entry_ids = {
        str(row.get("entry_id"))
        for row in manifest_rows
        if isinstance(row, dict) and row.get("entry_id")
    }
    label_entry_ids = [label.entry_id for label in labels]
    missing_from_manifest = sorted(set(label_entry_ids) - manifest_entry_ids)

    review_signal_summary = _review_signal_summary(
        learning_signal_manifest=learning_signal_manifest,
        rejected_signal_taxonomy=rejected_signal_taxonomy,
        exact_true_reject_signal=exact_true_reject_signal,
    )
    sequence_summary = _sequence_holdout_summary(
        sequence_holdout_eval,
        current_label_count=len(labels),
    )
    kmer_smoke = _kmer_nearest_neighbor_smoke(
        sequence_holdout_eval=sequence_holdout_eval,
        sequence_fasta_text=sequence_fasta_text,
        kmer_size=kmer_size,
        max_smoke_heldout=max_smoke_heldout,
        current_label_count=len(labels),
    )
    heuristic_baseline = _heuristic_geometry_baseline(
        sequence_holdout_eval,
        current_label_count=len(labels),
    )
    external_representation_controls = _external_representation_controls(
        external_kmer_sample=external_kmer_sample,
        external_esm_sample=external_esm_sample,
    )

    stale_sources = []
    for source_name, artifact in (
        ("learned_manifest", learned_manifest),
        ("sequence_holdout_eval", sequence_holdout_eval),
    ):
        if not isinstance(artifact, dict):
            stale_sources.append(f"{source_name}_missing")
            continue
        artifact_count = artifact.get("metadata", {}).get("label_registry_count")
        if artifact_count is not None and artifact_count != len(labels):
            stale_sources.append(
                f"{source_name}_label_count_{artifact_count}_vs_current_{len(labels)}"
            )

    benchmark_spec = {
        "registry_scope": {
            "current_label_count": len(labels),
            "entry_scope_counts": dict(sorted(label_scope_counts.items())),
            "label_type_counts": dict(sorted(registry_label_type_counts.items())),
            "review_status_counts": dict(sorted(registry_review_status_counts.items())),
            "tier_counts": dict(sorted(registry_tier_counts.items())),
            "fingerprint_or_scope_counts": dict(sorted(registry_fingerprint_counts.items())),
            "learned_manifest_covered_entry_count": len(manifest_entry_ids),
            "labels_missing_from_learned_manifest_entry_ids": missing_from_manifest,
        },
        "role_counts": dict(sorted(registry_role_counts.items())),
        "role_definitions": {
            "high_trust_evaluation_calibration_anchor": (
                "expert-reviewed silver/gold labels are held for calibration or "
                "evaluation anchors, not weak-supervision bulk training"
            ),
            "weak_supervision_only": (
                "automation-curated bronze seed-fingerprint positives may be used "
                "only as weak supervision after split and leakage controls"
            ),
            "negative_ood_calibration": (
                "countable out-of-scope labels and review-derived hard negatives "
                "calibrate abstention/OOD behavior; they are not global negatives"
            ),
            "abstention_ood_review_hold": (
                "future-family, unresolved, or review-only rows are OOD/abstention "
                "cases until explicit import gates pass"
            ),
        },
        "split_policy": {
            "training": (
                "use only weak-supervision rows assigned to train after whole-sequence "
                "or family-aware holdout assignment"
            ),
            "calibration": (
                "use expert anchors, hard negatives, rejects, and out-of-scope rows "
                "to tune abstention without using review prose as features"
            ),
            "evaluation": (
                "reserve expert-reviewed anchors and sequence/family held-out rows; "
                "do not train on all 702 labels"
            ),
            "abstention_ood": (
                "future-family backlog and unresolved holds remain abstention/OOD "
                "cases, not positive labels"
            ),
        },
        "review_signal_roles": review_signal_summary,
        "sequence_holdout_controls": sequence_summary,
    }

    baseline_matrix = [
        heuristic_baseline,
        {
            "baseline_id": "ec_or_family_prior_review_only",
            "status": "planned_review_only_not_predictive_input",
            "predictive_inputs": [],
            "review_context_inputs": ["ec_labels", "family_names"],
            "forbidden_for_learned_input": True,
            "comparison_role": (
                "sanity-check leakage and family imbalance; not eligible as a "
                "learned representation feature"
            ),
        },
        kmer_smoke,
        external_representation_controls["kmer_control"],
        external_representation_controls["esm_control"],
        {
            "baseline_id": "hybrid_representation_plus_geometry",
            "status": "blocked_until_current_split_and_embeddings_exist",
            "blockers": [
                "full_current_702_embedding_artifact_missing",
                "hybrid_must_be_compared_against_geometry_and_sequence_baselines",
                "no_leakage_audit_for_hybrid_feature_join_yet",
            ],
            "allowed_future_inputs": [
                "sequence_embeddings",
                "active_site_geometry_features",
            ],
            "forbidden_inputs": FORBIDDEN_REPRESENTATION_FEATURES,
        },
    ]

    return {
        "metadata": {
            "artifact_id": "v3_representation_baseline_shootout_plan_20260525",
            "schema_version": "representation_baseline_shootout_plan.v1",
            "method": "representation_baseline_shootout_plan",
            "current_label_registry_count": len(labels),
            "review_only": True,
            "label_import_performed": False,
            "canonical_registry_import_performed": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "large_model_training_performed": False,
            "learned_superiority_claimed": False,
            "stale_or_missing_source_flags": stale_sources,
        },
        "prediction_leakage_contract": {
            "forbidden_for_prediction_fields": FORBIDDEN_REPRESENTATION_FEATURES,
            "allowed_representation_inputs": [
                "amino_acid_sequence",
                "sequence_embedding_vectors",
                "active_site_geometry_features",
                "local_ligand_context",
            ],
            "review_only_context_fields": [
                "entry_id",
                "entry_name",
                "ec_labels",
                "expert_review_notes",
                "review_decision",
                "target_fingerprint_for_evaluation",
            ],
            "rule": (
                "mechanism prose, entry names, EC labels, source ids, and expert "
                "notes may define evaluation strata or review context but must not "
                "enter learned/representation predictive features"
            ),
        },
        "benchmark_spec": benchmark_spec,
        "baseline_matrix": baseline_matrix,
        "success_criteria": [
            "current-registry split artifact covers all 702 labels or records exact missing rows",
            "held-out metrics are reported separately from weak-supervision training rows",
            "geometry, EC/family-prior review context, deterministic sequence, and ESM controls are compared before any model-training claim",
            "hard negatives and future-family holds are calibrated as current-target/OOD cases, not global labels",
            "no mechanism prose, entry names, EC labels, Rhea ids, or expert notes are used as predictive representation inputs",
        ],
        "next_exact_compute_step": _next_exact_compute_step(
            sequence_holdout_eval,
            current_label_count=len(labels),
        ),
    }


def _registry_role_row(label: MechanismLabel) -> dict[str, Any]:
    if label.review_status == "expert_reviewed" or label.tier in {"silver", "gold"}:
        role = "high_trust_evaluation_calibration_anchor"
    elif label.label_type == "out_of_scope":
        role = "negative_ood_calibration"
    elif label.review_status == "automation_curated" and label.tier == "bronze":
        role = "weak_supervision_only"
    else:
        role = "abstention_ood_review_hold"
    return {
        "entry_id": label.entry_id,
        "label_type": label.label_type,
        "fingerprint_id": label.fingerprint_id,
        "review_status": label.review_status,
        "tier": label.tier,
        "benchmark_role": role,
    }


def _next_exact_compute_step(
    sequence_holdout_eval: dict[str, Any] | None,
    *,
    current_label_count: int,
) -> dict[str, Any]:
    sequence_command = (
        "PYTHONPATH=src python -m catalytic_earth.cli "
        "build-sequence-distance-holdout-eval --slice-id 1025_current702 "
        "--retrieval artifacts/v3_geometry_retrieval_1025.json "
        "--labels data/registries/curated_mechanism_labels.json "
        "--sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json "
        "--geometry artifacts/v3_geometry_features_1025.json "
        "--sequence-fasta artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta "
        "--sequence-identity-backend mmseqs "
        "--out artifacts/v3_sequence_distance_holdout_eval_1025_current702_20260525.json"
    )
    if not isinstance(sequence_holdout_eval, dict):
        return {
            "status": "build_current_702_sequence_split",
            "command": sequence_command,
            "then": (
                "build full current-registry representation sidecars or record exact "
                "backend/cache blockers; only after that compare a hybrid against "
                "geometry and deterministic sequence baselines"
            ),
        }
    metadata = sequence_holdout_eval.get("metadata", {})
    if metadata.get("label_registry_count") != current_label_count:
        return {
            "status": "refresh_stale_sequence_split_before_full_702_claim",
            "command": sequence_command,
            "then": (
                "rerun the shootout plan against the current split and only then "
                "attempt full embedding sidecars"
            ),
        }
    missing_entry_ids = metadata.get("sequence_missing_entry_ids", []) or []
    if missing_entry_ids or not metadata.get("sequence_identity_target_achieved"):
        return {
            "status": "blocked_by_current_sequence_coverage_gap",
            "missing_sequence_entry_count": len(missing_entry_ids),
            "missing_sequence_entry_ids": missing_entry_ids,
            "rerun_after_sequence_supplement_command": sequence_command,
            "then": (
                "after the sequence split has complete current-label coverage, build "
                "full current-registry representation sidecars or record exact "
                "embedding backend/cache blockers"
            ),
        }
    return {
        "status": "build_full_current_embedding_sidecar_or_record_backend_blocker",
        "command": (
            "PYTHONPATH=src python -m catalytic_earth.cli "
            "build-representation-baseline-shootout-plan "
            "--learned-manifest artifacts/v3_learned_retrieval_manifest_1025_current702_full_20260525.json "
            "--sequence-holdout-eval artifacts/v3_sequence_distance_holdout_eval_1025_current702_20260525.json "
            "--out artifacts/v3_representation_baseline_shootout_plan_20260525.json"
        ),
        "then": (
            "replace the placeholder with a bounded full-current embedding sidecar "
            "command once that backend is implemented for the M-CSA registry"
        ),
    }


def _label_scope(entry_id: str) -> str:
    return "m_csa" if entry_id.startswith("m_csa:") else "external"


def _review_signal_summary(
    *,
    learning_signal_manifest: dict[str, Any] | None,
    rejected_signal_taxonomy: dict[str, Any] | None,
    exact_true_reject_signal: dict[str, Any] | None,
) -> dict[str, Any]:
    learning_rows = (
        learning_signal_manifest.get("rows", [])
        if isinstance(learning_signal_manifest, dict)
        else []
    )
    learning_partitions = Counter(
        str(row.get("learning_signal_partition"))
        for row in learning_rows
        if isinstance(row, dict) and row.get("learning_signal_partition")
    )
    hard_negative_entry_ids: set[str] = set()
    hold_entry_ids: set[str] = set()
    future_family_entry_ids: set[str] = set()
    for row in learning_rows:
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id") or "")
        partition = str(row.get("learning_signal_partition") or "")
        if not entry_id:
            continue
        if partition == "current_target_hard_negative":
            hard_negative_entry_ids.add(entry_id)
        elif partition == "unresolved_review_hold":
            hold_entry_ids.add(entry_id)
        elif partition == "positive_review_signal_review_only":
            future_family_entry_ids.add(entry_id)

    for artifact, key in (
        (rejected_signal_taxonomy, "rejected_signal_taxonomy"),
        (exact_true_reject_signal, "exact_true_reject_signal"),
    ):
        rows = artifact.get("rows", []) if isinstance(artifact, dict) else []
        for row in rows:
            if not isinstance(row, dict) or not row.get("entry_id"):
                continue
            if key == "rejected_signal_taxonomy":
                hard_negative_entry_ids.add(str(row["entry_id"]))
            else:
                hard_negative_entry_ids.add(str(row["entry_id"]))

    return {
        "learning_signal_partition_counts": dict(sorted(learning_partitions.items())),
        "review_derived_current_target_hard_negative_count": len(
            hard_negative_entry_ids
        ),
        "review_derived_current_target_hard_negative_sample_entry_ids": sorted(
            hard_negative_entry_ids
        )[:12],
        "unresolved_hold_count": len(hold_entry_ids),
        "unresolved_hold_sample_entry_ids": sorted(hold_entry_ids)[:12],
        "positive_review_signal_review_only_count": len(future_family_entry_ids),
        "positive_review_signal_review_only_sample_entry_ids": sorted(
            future_family_entry_ids
        )[:12],
        "prediction_feature_status": (
            "review-derived signals define evaluation/calibration roles only; "
            "review text and target decisions are forbidden as direct model inputs"
        ),
    }


def _sequence_holdout_summary(
    sequence_holdout_eval: dict[str, Any] | None,
    *,
    current_label_count: int,
) -> dict[str, Any]:
    if not isinstance(sequence_holdout_eval, dict):
        return {
            "status": "missing",
            "blocker": "sequence_holdout_eval_artifact_missing",
        }
    metadata = sequence_holdout_eval.get("metadata", {})
    return {
        "status": (
            "current_label_count_mismatch"
            if metadata.get("label_registry_count") != current_label_count
            else "available_for_current_label_count"
        ),
        "artifact_label_registry_count": metadata.get("label_registry_count"),
        "current_label_registry_count": current_label_count,
        "evaluated_count": metadata.get("evaluated_count"),
        "heldout_count": metadata.get("heldout_count"),
        "in_distribution_count": metadata.get("in_distribution_count"),
        "sequence_identity_backend_available": metadata.get(
            "sequence_identity_backend_available"
        ),
        "sequence_identity_target_achieved": metadata.get(
            "sequence_identity_target_achieved"
        ),
        "max_observed_train_test_identity": metadata.get(
            "max_observed_train_test_identity"
        ),
        "real_tm_score_computed": metadata.get("real_tm_score_computed"),
        "limitations": metadata.get("limitations", []),
    }


def _heuristic_geometry_baseline(
    sequence_holdout_eval: dict[str, Any] | None,
    *,
    current_label_count: int,
) -> dict[str, Any]:
    if not isinstance(sequence_holdout_eval, dict):
        return {
            "baseline_id": "current_heuristic_geometry",
            "status": "missing_sequence_holdout_eval_artifact",
        }
    metadata = sequence_holdout_eval.get("metadata", {})
    metrics = sequence_holdout_eval.get("metrics", {})
    heldout_metrics = metrics.get("heldout", {}) if isinstance(metrics, dict) else {}
    return {
        "baseline_id": "current_heuristic_geometry",
        "status": (
            "computed_on_existing_sequence_holdout_but_stale_for_current_registry"
            if metadata.get("label_registry_count") != current_label_count
            else "computed_on_current_sequence_holdout"
        ),
        "source_artifact_method": metadata.get("method"),
        "artifact_label_registry_count": metadata.get("label_registry_count"),
        "current_label_registry_count": current_label_count,
        "heldout_metrics": {
            "evaluated_count": heldout_metrics.get("evaluated_count"),
            "in_scope_count": heldout_metrics.get("in_scope_count"),
            "out_of_scope_count": heldout_metrics.get("out_of_scope_count"),
            "top1_accuracy_in_scope": heldout_metrics.get("top1_accuracy_in_scope"),
            "top3_accuracy_in_scope": heldout_metrics.get("top3_accuracy_in_scope"),
            "out_of_scope_false_non_abstentions": heldout_metrics.get(
                "out_of_scope_false_non_abstentions"
            ),
            "out_of_scope_abstention_rate": heldout_metrics.get(
                "out_of_scope_abstention_rate"
            ),
        },
        "predictive_inputs": [
            "active_site_residue_identity",
            "active_site_residue_roles",
            "local_ligand_cofactor_context",
            "substrate_pocket_descriptors",
            "active_site_compactness",
        ],
        "forbidden_inputs_used": [],
    }


def _external_representation_controls(
    *,
    external_kmer_sample: dict[str, Any] | None,
    external_esm_sample: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    return {
        "kmer_control": _external_control_row(
            "existing_external_deterministic_kmer_control",
            external_kmer_sample,
        ),
        "esm_control": _external_control_row(
            "existing_external_esm2_sample_control",
            external_esm_sample,
        ),
    }


def _external_control_row(
    baseline_id: str,
    artifact: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(artifact, dict):
        return {
            "baseline_id": baseline_id,
            "status": "missing",
            "blocker": "source_artifact_not_supplied",
        }
    metadata = artifact.get("metadata", {})
    return {
        "baseline_id": baseline_id,
        "status": "external_sample_only_not_full_702_registry",
        "embedding_backend": metadata.get("embedding_backend"),
        "embedding_status": metadata.get("embedding_status"),
        "candidate_count": metadata.get("candidate_count"),
        "backend_status_counts": metadata.get("backend_status_counts", {}),
        "representation_near_duplicate_alert_count": metadata.get(
            "representation_near_duplicate_alert_count"
        ),
        "ready_for_label_import": metadata.get("ready_for_label_import"),
        "predictive_feature_policy": metadata.get("predictive_feature_policy"),
        "review_only_rule": metadata.get("review_only_rule"),
    }


def _kmer_nearest_neighbor_smoke(
    *,
    sequence_holdout_eval: dict[str, Any] | None,
    sequence_fasta_text: str | None,
    kmer_size: int,
    max_smoke_heldout: int,
    current_label_count: int,
) -> dict[str, Any]:
    baseline_id = f"deterministic_{kmer_size}mer_jaccard_nearest_neighbor_smoke"
    if not isinstance(sequence_holdout_eval, dict):
        return {
            "baseline_id": baseline_id,
            "status": "not_computed",
            "blockers": ["sequence_holdout_eval_artifact_missing"],
        }
    if not sequence_fasta_text:
        return {
            "baseline_id": baseline_id,
            "status": "not_computed",
            "blockers": ["sequence_fasta_missing"],
        }

    sequences_by_accession = _parse_fasta_by_accession(sequence_fasta_text)
    rows = [
        row
        for row in sequence_holdout_eval.get("rows", [])
        if isinstance(row, dict)
        and row.get("partition") in {"in_distribution", "heldout"}
        and row.get("label_group")
    ]
    prepared: list[dict[str, Any]] = []
    missing_sequence_entry_ids: list[str] = []
    for row in rows:
        sequence = _sequence_for_row(row, sequences_by_accession)
        if sequence is None:
            if row.get("entry_id"):
                missing_sequence_entry_ids.append(str(row["entry_id"]))
            continue
        prepared.append(
            {
                "entry_id": str(row.get("entry_id")),
                "partition": str(row.get("partition")),
                "label_group": str(row.get("label_group")),
                "target_fingerprint_id": row.get("target_fingerprint_id"),
                "kmers": _kmers(sequence, kmer_size),
            }
        )

    train_rows = [row for row in prepared if row["partition"] == "in_distribution"]
    heldout_rows = [row for row in prepared if row["partition"] == "heldout"]
    if max_smoke_heldout > 0:
        heldout_rows = heldout_rows[:max_smoke_heldout]
    if not train_rows or not heldout_rows:
        return {
            "baseline_id": baseline_id,
            "status": "not_computed",
            "blockers": ["train_or_heldout_sequence_rows_missing"],
            "train_sequence_count": len(train_rows),
            "heldout_sequence_count": len(heldout_rows),
        }

    comparisons: list[dict[str, Any]] = []
    for heldout in heldout_rows:
        nearest = max(
            train_rows,
            key=lambda train: (
                _jaccard(heldout["kmers"], train["kmers"]),
                train["entry_id"],
            ),
        )
        similarity = _jaccard(heldout["kmers"], nearest["kmers"])
        comparisons.append(
            {
                "entry_id": heldout["entry_id"],
                "label_group": heldout["label_group"],
                "nearest_train_entry_id": nearest["entry_id"],
                "nearest_train_label_group": nearest["label_group"],
                "jaccard_similarity": round(similarity, 4),
                "exact_label_match": heldout["label_group"] == nearest["label_group"],
                "true_in_scope": heldout["label_group"] != "out_of_scope",
                "out_of_scope_false_positive": (
                    heldout["label_group"] == "out_of_scope"
                    and nearest["label_group"] != "out_of_scope"
                ),
            }
        )

    in_scope = [row for row in comparisons if row["true_in_scope"]]
    out_of_scope = [row for row in comparisons if not row["true_in_scope"]]
    similarities = [row["jaccard_similarity"] for row in comparisons]
    metadata = sequence_holdout_eval.get("metadata", {})
    return {
        "baseline_id": baseline_id,
        "status": (
            "computed_existing_sequence_holdout_but_stale_for_current_registry"
            if metadata.get("label_registry_count") != current_label_count
            else "computed_current_sequence_holdout"
        ),
        "predictive_inputs": ["amino_acid_sequence_only"],
        "forbidden_inputs_used": [],
        "training_mode": "none_nearest_neighbor_lookup_only",
        "artifact_label_registry_count": metadata.get("label_registry_count"),
        "current_label_registry_count": current_label_count,
        "train_sequence_count": len(train_rows),
        "heldout_sequence_count": len(heldout_rows),
        "missing_sequence_entry_count": len(missing_sequence_entry_ids),
        "missing_sequence_entry_ids_sample": missing_sequence_entry_ids[:12],
        "metrics": {
            "exact_label_accuracy_all": _fraction(
                sum(1 for row in comparisons if row["exact_label_match"]),
                len(comparisons),
            ),
            "exact_label_accuracy_in_scope": _fraction(
                sum(1 for row in in_scope if row["exact_label_match"]),
                len(in_scope),
            ),
            "out_of_scope_false_positive_rate_no_threshold": _fraction(
                sum(1 for row in out_of_scope if row["out_of_scope_false_positive"]),
                len(out_of_scope),
            ),
            "mean_nearest_jaccard_similarity": round(mean(similarities), 4)
            if similarities
            else None,
            "max_nearest_jaccard_similarity": max(similarities)
            if similarities
            else None,
        },
        "comparison_sample": comparisons[:12],
        "limitations": [
            "deterministic k-mer Jaccard is a smoke baseline, not a trained representation model",
            "nearest-neighbor labels are assigned from existing split partitions only",
            "no threshold calibration or hard-negative OOD calibration is claimed here",
        ],
    }


def _parse_fasta_by_accession(fasta_text: str) -> dict[str, str]:
    sequences: dict[str, str] = {}
    current_accession: str | None = None
    current_chunks: list[str] = []
    for raw_line in fasta_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_accession and current_chunks:
                sequences[current_accession] = "".join(current_chunks)
            current_accession = _accession_from_fasta_header(line[1:])
            current_chunks = []
        else:
            current_chunks.append(line)
    if current_accession and current_chunks:
        sequences[current_accession] = "".join(current_chunks)
    return sequences


def _accession_from_fasta_header(header: str) -> str:
    token = header.split()[0]
    parts = token.split("|")
    if len(parts) >= 2 and parts[1]:
        return parts[1]
    return token


def _sequence_for_row(
    row: dict[str, Any],
    sequences_by_accession: dict[str, str],
) -> str | None:
    for accession in row.get("real_sequence_accessions", []) or []:
        sequence = sequences_by_accession.get(str(accession))
        if sequence:
            return sequence
    for accession in row.get("reference_uniprot_ids", []) or []:
        sequence = sequences_by_accession.get(str(accession))
        if sequence:
            return sequence
    return None


def _kmers(sequence: str, kmer_size: int) -> set[str]:
    clean = "".join(character for character in sequence.upper() if character.isalpha())
    if len(clean) <= kmer_size:
        return {clean} if clean else set()
    return {clean[index : index + kmer_size] for index in range(len(clean) - kmer_size + 1)}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _fraction(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)
