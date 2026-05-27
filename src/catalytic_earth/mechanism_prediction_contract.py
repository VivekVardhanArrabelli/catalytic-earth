from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from .labels import MechanismLabel
from .models import MechanismFingerprint


PRIMARY_FINGERPRINTS = [
    "ser_his_acid_hydrolase",
    "metal_dependent_hydrolase",
    "plp_dependent_enzyme",
    "flavin_dehydrogenase_reductase",
    "heme_peroxidase_oxidase",
]

SECONDARY_PROBE_ROLES = {
    "radical_sam_enzyme": {
        "probe_role": "far_oos_tail_diagnostic",
        "oos_tier": "far_oos",
        "primary_metric_status": "excluded_from_primary_supervised_metrics",
        "reason": (
            "far-OOD/tail diagnostic; exclude from primary supervised metrics "
            "until additional radical SAM coverage exists"
        ),
    },
    "cobalamin_radical_rearrangement": {
        "probe_role": "ontology_boundary_mixed_ood_diagnostic",
        "oos_tier": "boundary_oos",
        "primary_metric_status": "excluded_from_primary_supervised_metrics",
        "reason": (
            "ontology-boundary/mixed OOD diagnostic; exclude from primary "
            "supervised metrics until split or re-review"
        ),
    },
    "flavin_monooxygenase": {
        "probe_role": "near_oos_against_flavin_redox_diagnostic",
        "oos_tier": "near_oos",
        "primary_metric_status": "excluded_from_primary_supervised_metrics",
        "reason": (
            "near-OOD diagnostic against flavin_dehydrogenase_reductase; "
            "exclude from primary supervised metrics"
        ),
    },
}

OOS_CANARY_ENTRY_IDS_BY_TIER = {
    "far_oos": ["m_csa:1", "m_csa:12", "m_csa:23"],
    "near_oos": ["m_csa:14", "m_csa:32", "m_csa:34"],
    "boundary_oos": ["m_csa:2", "m_csa:19", "m_csa:39"],
    "unknown_oos": ["m_csa:25", "m_csa:96"],
}

BOUNDARY_OOS_EXCLUSION_REASONS = {
    "m_csa:2": {
        "near_primary_fingerprint": "ser_his_acid_hydrolase",
        "exclusion_reason": (
            "Serine beta-lactamase boundary case; lacks the frozen "
            "Ser-His-Asp/Glu triad hydrolase evidence pattern"
        ),
    },
    "m_csa:14": {
        "near_primary_fingerprint": "heme_peroxidase_oxidase",
        "exclusion_reason": (
            "Peroxidase-like chemistry but vanadate dependent, not the frozen "
            "heme-dependent peroxidase/oxidase seed"
        ),
    },
    "m_csa:19": {
        "near_primary_fingerprint": "ser_his_acid_hydrolase",
        "exclusion_reason": (
            "Glycosidase hydrolysis boundary; acid-base glycoside chemistry is "
            "outside the frozen Ser-His-acid hydrolase seed"
        ),
    },
    "m_csa:39": {
        "near_primary_fingerprint": "metal_dependent_hydrolase",
        "exclusion_reason": (
            "Nucleoside hydrolase chemistry is outside the frozen "
            "metal-dependent hydrolase seed scope"
        ),
    },
    "m_csa:47": {
        "near_primary_fingerprint": "metal_dependent_hydrolase",
        "exclusion_reason": (
            "Cysteine phosphatase chemistry is outside the frozen "
            "metal-dependent and Ser-His-acid hydrolase seeds"
        ),
    },
}


def build_mechanism_prediction_oos_and_diversity_eval_contract(
    *,
    labels: list[MechanismLabel],
    fingerprints: list[MechanismFingerprint],
    coherence_audit: dict[str, Any],
    source_artifact_paths: list[Path],
) -> dict[str, Any]:
    """Freeze evaluation policy without training or scoring a model."""
    label_by_entry = {label.entry_id: label for label in labels}
    fingerprint_by_id = {fingerprint.id: fingerprint for fingerprint in fingerprints}
    audit_rows = {
        str(row.get("fingerprint_id")): row
        for row in coherence_audit.get("fingerprints", [])
        if isinstance(row, dict) and row.get("fingerprint_id")
    }
    primary_from_audit = coherence_audit.get("fingerprints_kept_for_primary_metric")
    if primary_from_audit != PRIMARY_FINGERPRINTS:
        raise ValueError("coherence audit primary fingerprints do not match v1 contract")
    secondary_from_audit = [
        row.get("fingerprint_id")
        for row in coherence_audit.get(
            "fingerprints_excluded_or_flagged_for_secondary_only", []
        )
        if isinstance(row, dict)
    ]
    if secondary_from_audit != list(SECONDARY_PROBE_ROLES):
        raise ValueError("coherence audit secondary fingerprints do not match v1 contract")
    if len(labels) != 702:
        raise ValueError("mechanism prediction contract v1 is frozen for 702 labels")

    label_type_counts = Counter(label.label_type for label in labels)
    fingerprint_counts = Counter(
        label.fingerprint_id
        for label in labels
        if label.label_type == "seed_fingerprint"
    )
    source_artifacts = {
        str(path): {
            "sha256": _sha256(path),
            "role": _source_artifact_role(path),
        }
        for path in source_artifact_paths
    }
    primary_details = [
        _primary_fingerprint_detail(
            fingerprint_id,
            support_count=fingerprint_counts[fingerprint_id],
            audit_row=audit_rows[fingerprint_id],
            fingerprint=fingerprint_by_id[fingerprint_id],
        )
        for fingerprint_id in PRIMARY_FINGERPRINTS
    ]
    secondary_probe_fingerprints = [
        _secondary_probe_detail(
            fingerprint_id,
            support_count=fingerprint_counts[fingerprint_id],
            audit_row=audit_rows[fingerprint_id],
        )
        for fingerprint_id in SECONDARY_PROBE_ROLES
    ]

    return {
        "schema_version": "mechanism_prediction_oos_and_diversity_eval_contract.v1",
        "artifact_id": "v3_mechanism_prediction_oos_and_diversity_eval_contract_702",
        "baseline_label_count": len(labels),
        "mechanism_fingerprint_version": "label_factory_v1_8fp",
        "contract_scope": {
            "purpose": (
                "Freeze mechanism-prediction OOS, diversity, support, "
                "abstention, canary, and pooling policy before sequence-NN or "
                "learned-representation results are interpreted"
            ),
            "review_only_contract": True,
            "label_import_performed": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "model_training_or_benchmark_results_created": False,
            "forbidden_predictive_features": [
                "EC labels",
                "entry names",
                "mechanism prose",
                "expert notes",
                "curator rationale text",
                "review decision text",
                "source identifiers as semantic features",
            ],
        },
        "source_artifacts": source_artifacts,
        "registry_scope_summary": {
            "label_type_counts": dict(sorted(label_type_counts.items())),
            "seed_fingerprint_counts": {
                key: fingerprint_counts[key]
                for key in sorted(fingerprint_counts)
            },
            "primary_seed_label_count": sum(
                fingerprint_counts[fingerprint_id]
                for fingerprint_id in PRIMARY_FINGERPRINTS
            ),
            "secondary_probe_seed_label_count": sum(
                fingerprint_counts[fingerprint_id]
                for fingerprint_id in SECONDARY_PROBE_ROLES
            ),
        },
        "primary_fingerprints": PRIMARY_FINGERPRINTS,
        "primary_fingerprint_details": primary_details,
        "secondary_ood_probe_fingerprints": secondary_probe_fingerprints,
        "oos_tiering_policy": _oos_tiering_policy(),
        "frozen_oos_tier_assignments_summary": (
            _frozen_oos_tier_assignments_summary(
                label_by_entry=label_by_entry,
                fingerprint_counts=fingerprint_counts,
            )
        ),
        "diversity_stratified_accuracy_policy": (
            _diversity_stratified_accuracy_policy()
        ),
        "support_threshold_policy": _support_threshold_policy(),
        "abstention_diagnostics_policy": _abstention_diagnostics_policy(),
        "canary_examples": _canary_examples(
            label_by_entry=label_by_entry,
            audit_rows=audit_rows,
            fingerprint_counts=fingerprint_counts,
        ),
        "active_site_pooling_contract": _active_site_pooling_contract(),
        "contract_change_policy": {
            "schema_versioning_rule": (
                "Any future change to tiering, canaries, diversity bins, "
                "support thresholds, abstention diagnostics, or pooling modes "
                "must increment the schema/version"
            ),
            "immutability_rule": (
                "Do not overwrite this v1 artifact; write a new versioned "
                "artifact path for any future contract"
            ),
            "benchmark_result_requirement": (
                "Every benchmark result artifact must record the exact SHA-256 "
                "of this contract artifact before interpretation"
            ),
        },
        "next_allowed_benchmark_step": {
            "status": "contract_frozen_stop_before_model_results",
            "allowed_next_action": (
                "Complete the full per-entry OOS tier assignment artifact or "
                "run the next benchmark only with this contract SHA recorded"
            ),
            "not_allowed_in_this_contract_run": [
                "sequence-NN benchmark execution",
                "PLM embedding computation",
                "model training",
                "learned representation comparison",
                "representation performance claim",
            ],
        },
    }


def _primary_fingerprint_detail(
    fingerprint_id: str,
    *,
    support_count: int,
    audit_row: dict[str, Any],
    fingerprint: MechanismFingerprint,
) -> dict[str, Any]:
    return {
        "fingerprint_id": fingerprint_id,
        "support_count": support_count,
        "audit_evaluation_status": audit_row["evaluation_status"],
        "audit_freeze_decision": audit_row["v1_freeze_decision"],
        "chemical_operation": fingerprint.reaction_center.chemical_operation,
        "cofactors": fingerprint.cofactors,
        "representative_entry_ids": audit_row["representative_entry_ids"],
        "broad_bucket_requires_special_diversity_scrutiny": fingerprint_id
        in {
            "metal_dependent_hydrolase",
            "plp_dependent_enzyme",
            "flavin_dehydrogenase_reductase",
            "heme_peroxidase_oxidase",
        },
        "metric_role": "eligible_for_primary_mechanism_fingerprint_metrics",
    }


def _secondary_probe_detail(
    fingerprint_id: str,
    *,
    support_count: int,
    audit_row: dict[str, Any],
) -> dict[str, Any]:
    probe = SECONDARY_PROBE_ROLES[fingerprint_id]
    return {
        "fingerprint_id": fingerprint_id,
        "support_count": support_count,
        "representative_entry_ids": audit_row["representative_entry_ids"],
        "audit_evaluation_status": audit_row["evaluation_status"],
        "probe_role": probe["probe_role"],
        "oos_tier": probe["oos_tier"],
        "primary_metric_status": probe["primary_metric_status"],
        "reason": probe["reason"],
    }


def _oos_tiering_policy() -> dict[str, Any]:
    return {
        "assignment_scope": (
            "Rows used as OOS diagnostics include label_type=out_of_scope rows "
            "plus the three secondary probe fingerprints listed in this contract"
        ),
        "determinism_rule": (
            "Tiering is assigned from frozen registry, fingerprint, audit, "
            "sequence-neighborhood, and structure-neighborhood evidence; it is "
            "never assigned from a model prediction, confidence, or post-hoc "
            "per-model judgment"
        ),
        "tier_order": [
            "boundary_oos curated-list overrides",
            "near_oos positive-overlap criteria",
            "far_oos negative-overlap criteria",
            "unknown_oos insufficient-evidence fallback",
        ],
        "tier_definitions": {
            "far_oos": {
                "criteria_type": "negative_criteria",
                "deterministic_rule": (
                    "Assign when the row has no cofactor overlap with primary "
                    "fingerprints, no catalytic residue or role-pattern overlap "
                    "with primary fingerprints, and no known close structural or "
                    "sequence neighborhood to primary members when such data "
                    "exists"
                ),
                "primary_metric_role": (
                    "OOS abstention diagnostic only; any primary-fingerprint "
                    "prediction is a false-positive/non-abstention"
                ),
            },
            "near_oos": {
                "criteria_type": "positive_overlap_criteria",
                "deterministic_rule": (
                    "Assign when the row shares a cofactor or metal, catalytic "
                    "residue motif, structural/sequence neighborhood, or "
                    "active-site geometry with a primary fingerprint while "
                    "remaining mechanistically distinct per M-CSA or "
                    "label-factory evidence"
                ),
                "primary_metric_role": (
                    "Hard-negative OOS diagnostic; evaluate abstention and "
                    "which primary fingerprint attracts false positives"
                ),
            },
            "boundary_oos": {
                "criteria_type": "curated_list",
                "deterministic_rule": (
                    "Assign only from explicit audit or review artifacts where "
                    "an entry was considered for inclusion in or near a primary "
                    "fingerprint and explicitly excluded with an exclusion reason"
                ),
                "primary_metric_role": (
                    "Ontology-boundary diagnostic; do not include in primary "
                    "supervised metrics unless a future contract re-reviews it"
                ),
            },
            "unknown_oos": {
                "criteria_type": "fail_closed",
                "deterministic_rule": (
                    "Assign when available evidence is insufficient to choose "
                    "far_oos, near_oos, or boundary_oos deterministically"
                ),
                "primary_metric_role": (
                    "Qualitative diagnostic until evidence resolves the tier"
                ),
            },
        },
        "allowed_assignment_evidence": [
            "mechanism_fingerprints.json structural definitions",
            "curated_mechanism_labels.json label_type, fingerprint_id, tier, and review_status",
            "coherence audit representative ids and exclusion reasons",
            "train-free sequence clusters or MMseqs neighborhoods when available",
            "train-free structure clusters or active-site geometry when available",
        ],
        "forbidden_assignment_evidence": [
            "model predictions",
            "model confidence",
            "benchmark residuals",
            "EC/name/prose/expert-note fields as predictive features",
        ],
    }


def _frozen_oos_tier_assignments_summary(
    *,
    label_by_entry: dict[str, MechanismLabel],
    fingerprint_counts: Counter[str | None],
) -> dict[str, Any]:
    representative_ids_by_tier = {
        tier: [
            _oos_representative_row(entry_id, tier, label_by_entry[entry_id])
            for entry_id in entry_ids
        ]
        for tier, entry_ids in OOS_CANARY_ENTRY_IDS_BY_TIER.items()
    }
    out_of_scope_assigned = sum(len(rows) for rows in representative_ids_by_tier.values())
    secondary_assignments = {
        fingerprint_id: {
            "oos_tier": probe["oos_tier"],
            "probe_role": probe["probe_role"],
            "entry_count": fingerprint_counts[fingerprint_id],
            "entry_ids": _secondary_probe_entry_ids(fingerprint_id, label_by_entry),
            "primary_metric_status": probe["primary_metric_status"],
        }
        for fingerprint_id, probe in SECONDARY_PROBE_ROLES.items()
    }
    secondary_assigned = sum(
        assignment["entry_count"] for assignment in secondary_assignments.values()
    )
    out_of_scope_count = sum(
        1 for label in label_by_entry.values() if label.label_type == "out_of_scope"
    )
    return {
        "assignment_version": "partial_oos_tiers.v1",
        "current_registry_out_of_scope_label_count": out_of_scope_count,
        "secondary_probe_seed_label_count": secondary_assigned,
        "complete_oos_assignment": False,
        "partial_assignment_status": {
            "status": "partial_v1_representatives_and_secondary_probes_only",
            "full_470_out_of_scope_assigned": False,
            "reason": (
                "This contract freezes deterministic rules and representative "
                "tier canaries, but does not run a full per-entry tier pass over "
                "all current out-of-scope registry rows"
            ),
            "next_exact_task": (
                "Apply oos_tiering_policy to all current label_type=out_of_scope "
                "rows using registry/fingerprint/audit evidence plus train-free "
                "sequence or structure neighborhoods, then emit "
                "artifacts/v3_mechanism_prediction_oos_tier_assignments_702.json "
                "with per-entry tier, trigger, evidence source, and exclusion "
                "reason fields before interpreting model results"
            ),
        },
        "partial_representative_assignment_counts": {
            "out_of_scope_label_rows_assigned_in_this_contract": out_of_scope_assigned,
            "secondary_probe_seed_rows_assigned_in_this_contract": secondary_assigned,
            "remaining_out_of_scope_label_rows_pending_assignment": (
                470 - out_of_scope_assigned
            ),
            "counts_by_tier_for_assigned_representatives_only": {
                tier: len(rows) for tier, rows in representative_ids_by_tier.items()
            },
        },
        "representative_entry_ids_by_tier": representative_ids_by_tier,
        "secondary_probe_assignments_by_fingerprint": secondary_assignments,
        "boundary_oos_curated_exclusion_examples": [
            {
                "entry_id": entry_id,
                "near_primary_fingerprint": row["near_primary_fingerprint"],
                "exclusion_reason": row["exclusion_reason"],
                "source_artifact_provenance": (
                    "data/registries/curated_mechanism_labels.json plus "
                    "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json"
                ),
            }
            for entry_id, row in sorted(BOUNDARY_OOS_EXCLUSION_REASONS.items())
        ],
    }


def _oos_representative_row(
    entry_id: str, tier: str, label: MechanismLabel
) -> dict[str, Any]:
    return {
        "entry_id": entry_id,
        "oos_tier": tier,
        "confidence": label.confidence,
        "review_status": label.review_status,
        "assignment_basis": label.rationale,
        "source_artifact_provenance": (
            "data/registries/curated_mechanism_labels.json::" + entry_id
        ),
    }


def _secondary_probe_entry_ids(
    fingerprint_id: str, label_by_entry: dict[str, MechanismLabel]
) -> list[str]:
    return sorted(
        entry_id
        for entry_id, label in label_by_entry.items()
        if label.fingerprint_id == fingerprint_id
    )


def _diversity_stratified_accuracy_policy() -> dict[str, Any]:
    return {
        "headline_rule": (
            "Headline macro-F1 is not sufficient without this diversity report"
        ),
        "required_for_primary_fingerprints": PRIMARY_FINGERPRINTS,
        "special_scrutiny_broad_buckets": [
            "metal_dependent_hydrolase",
            "plp_dependent_enzyme",
            "flavin_dehydrogenase_reductase",
            "heme_peroxidase_oxidase",
        ],
        "default_subfamily_clustering": {
            "method": "MMseqs",
            "sequence_identity": 0.30,
            "coverage": 0.80,
            "applies_where": "amino-acid sequences exist",
            "cluster_source_rule": (
                "Clusters must be generated from train-only data for any split "
                "that uses cluster-derived thresholds or bins"
            ),
        },
        "primary_diversity_axis": {
            "name": "nearest_same_fingerprint_different_subfamily_train_example",
            "distance_basis": (
                "For each evaluation row, find the nearest train row with the "
                "same primary fingerprint but a different MMseqs subfamily; "
                "report the nearest-neighbor similarity or distance used"
            ),
            "missing_neighbor_rule": (
                "If no same-fingerprint different-subfamily train neighbor "
                "exists, mark the row far_open_set and keep it in qualitative "
                "or underpowered reporting"
            ),
        },
        "binning_rule": {
            "threshold_source": "train_only_per_fingerprint_quantiles",
            "similarity_direction": "larger_similarity_is_closer",
            "close": "similarity >= train-only 66.7th percentile",
            "medium": (
                "train-only 33.3rd percentile <= similarity < train-only "
                "66.7th percentile"
            ),
            "far": "similarity < train-only 33.3rd percentile",
            "far_open_set": (
                "no eligible same-fingerprint different-subfamily train neighbor"
            ),
            "quantile_tie_rule": (
                "Use nearest-neighbor similarity sorted ascending with inclusive "
                "lower bin bounds except close, which is inclusive at the upper "
                "quantile threshold"
            ),
        },
        "required_outputs_per_fingerprint": [
            "row_count_by_diversity_bin",
            "accuracy_or_recall_by_diversity_bin",
            "macro_F1_contribution_by_bin_when_powered",
            "subfamily_count_train_vs_eval",
            "underpowered_cell_flags",
        ],
    }


def _support_threshold_policy() -> dict[str, Any]:
    return {
        "quantitative_reporting_thresholds": {
            "accuracy_or_recall_cell_min_n": 30,
            "ece_or_calibration_cell_min_n": 50,
        },
        "inclusion_thresholds": {
            "macro_F1_class_min_n": 5,
            "qualitative_canary_min_n": 1,
        },
        "below_threshold_rule": (
            "Below-threshold cells are qualitative_only and must be flagged; "
            "they are not omitted silently"
        ),
        "metric_artifact_requirement": (
            "Every metric artifact must flag underpowered cells before any "
            "interpretation or win claim"
        ),
    }


def _abstention_diagnostics_policy() -> dict[str, Any]:
    return {
        "required_by_oos_tier": [
            "abstention_rate",
            "false_positive_non_abstention_rate",
            "false_positive_rate_by_predicted_primary_fingerprint",
            "confidence_distribution_on_oos_rows",
            "confidence_distribution_on_correctly_classified_in_scope_rows",
            "overlap_diagnostic_for_any_threshold_separating_oos_from_in_scope",
        ],
        "tier_scope": [
            "far_oos",
            "near_oos",
            "boundary_oos",
            "unknown_oos",
            "secondary_probe_fingerprints",
        ],
        "win_condition": (
            "A model win is conjunctive: improved primary mechanism prediction "
            "and no-worse or better calibrated abstention on tail, near-OOS, "
            "and hard-negative cases"
        ),
        "threshold_selection_rule": (
            "Any abstention threshold must be chosen on train/calibration data "
            "only and then reported unchanged on OOS tiers and primary eval rows"
        ),
    }


def _canary_examples(
    *,
    label_by_entry: dict[str, MechanismLabel],
    audit_rows: dict[str, dict[str, Any]],
    fingerprint_counts: Counter[str | None],
) -> dict[str, Any]:
    examples: list[dict[str, Any]] = []
    for fingerprint_id in PRIMARY_FINGERPRINTS:
        for entry_id in audit_rows[fingerprint_id]["representative_entry_ids"][:5]:
            examples.append(
                {
                    "entry_id": entry_id,
                    "expected_eval_role": (
                        "primary_supervised_metric::" + fingerprint_id
                    ),
                    "expected_behavior": (
                        "predict " + fingerprint_id + " without abstention; "
                        "also report the row in its diversity bin"
                    ),
                    "reason": (
                        "Coherence-audit representative for " + fingerprint_id
                    ),
                    "source_artifact_provenance": (
                        "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json"
                        "::fingerprints[].representative_entry_ids"
                    ),
                }
            )
    for fingerprint_id, probe in SECONDARY_PROBE_ROLES.items():
        for entry_id in _secondary_probe_entry_ids(fingerprint_id, label_by_entry):
            examples.append(
                {
                    "entry_id": entry_id,
                    "expected_eval_role": (
                        "secondary_ood_probe::" + fingerprint_id
                    ),
                    "expected_behavior": (
                        "exclude from primary supervised metrics; evaluate "
                        + probe["probe_role"]
                        + " abstention behavior"
                    ),
                    "reason": probe["reason"],
                    "source_artifact_provenance": (
                        "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json"
                        "::fingerprints_excluded_or_flagged_for_secondary_only"
                    ),
                }
            )
    for tier, entry_ids in OOS_CANARY_ENTRY_IDS_BY_TIER.items():
        for entry_id in entry_ids:
            examples.append(
                {
                    "entry_id": entry_id,
                    "expected_eval_role": "oos_tier::" + tier,
                    "expected_behavior": (
                        "abstain or predict none_of_above; any primary "
                        "fingerprint prediction is a tiered false-positive "
                        "diagnostic"
                    ),
                    "reason": label_by_entry[entry_id].rationale,
                    "source_artifact_provenance": (
                        "data/registries/curated_mechanism_labels.json::"
                        + entry_id
                    ),
                }
            )
    return {
        "canary_expansion_needed": True,
        "expansion_reason": (
            "The v1 list covers 5 examples from each primary fingerprint, all "
            "secondary probe rows, and representative OOS tiers, but the full "
            "470-row OOS tier assignment is still pending"
        ),
        "aggregate_metric_use": (
            "Canaries are not aggregate metrics; inspect them manually on every "
            "benchmark run"
        ),
        "primary_canary_count_by_fingerprint": {
            fingerprint_id: min(
                5, len(audit_rows[fingerprint_id]["representative_entry_ids"])
            )
            for fingerprint_id in PRIMARY_FINGERPRINTS
        },
        "secondary_probe_canary_count_by_fingerprint": {
            fingerprint_id: fingerprint_counts[fingerprint_id]
            for fingerprint_id in SECONDARY_PROBE_ROLES
        },
        "oos_tier_canary_count_by_tier": {
            tier: len(entry_ids)
            for tier, entry_ids in OOS_CANARY_ENTRY_IDS_BY_TIER.items()
        },
        "examples": examples,
    }


def _active_site_pooling_contract() -> dict[str, Any]:
    return {
        "evidence_budget_rule": (
            "Active-site pooling must be consistent across representation "
            "models and must not leak labels"
        ),
        "primary_benchmark_pooling_mode": "whole_sequence",
        "allowed_pooling_modes": [
            "whole_sequence",
            "known_active_site_window_ablation",
            "predicted_or_source_free_pocket",
            "unavailable",
        ],
        "allowed_primary_inputs": [
            "amino-acid sequence",
            "source-free sequence positions",
            "structure-derived pocket residues when available",
        ],
        "controlled_ablation_only_inputs": [
            (
                "pre-existing curated catalytic-residue annotations may be used "
                "only as known_active_site_window_ablation, not as the primary "
                "representation benchmark"
            )
        ],
        "whole_sequence_rule": (
            "Primary benchmark uses whole-sequence embeddings first for every "
            "representation family"
        ),
        "active_site_window_ablation_rule": {
            "window_radius_residues": 64,
            "window_rule": (
                "Use +/-64 residues around allowed residue positions for ESM-C, "
                "ESM-2, ProtT5/local models, and SaProt/3Di variants where "
                "applicable"
            ),
            "merge_rule": "merge overlapping windows before pooling",
            "pooling_rule": "mean-pool residue tokens over merged eligible windows",
            "required_metadata": [
                "allowed_position_source",
                "covered_residue_count",
                "sequence_length",
                "window_coverage_fraction",
                "ineligibility_reason_when_unavailable",
            ],
        },
        "structure_or_pocket_pooling_rule": {
            "radius_angstrom": 10.0,
            "selection_rule": (
                "Pool residues within 10 Angstrom of catalytic or pocket atoms "
                "when coordinates are available from an allowed source"
            ),
            "coordinate_source_values": [
                "selected_pdb",
                "afdb",
                "unavailable",
            ],
            "required_metadata": [
                "coordinate_source",
                "pocket_atom_source",
                "covered_residue_count",
                "ineligibility_reason_when_unavailable",
            ],
        },
        "artifact_requirement": (
            "Every model artifact must state pooling_mode as whole_sequence, "
            "known_active_site_window_ablation, predicted_or_source_free_pocket, "
            "or unavailable"
        ),
        "comparison_rule": (
            "Do not compare active-site-pooled models against whole-sequence "
            "models as if they used the same evidence budget; report them "
            "separately"
        ),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_artifact_role(path: Path) -> str:
    name = str(path)
    roles = {
        "artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json": (
            "primary_and_secondary_fingerprint_freeze"
        ),
        "artifacts/v3_representation_baseline_shootout_plan_20260525.json": (
            "leakage_and_baseline_plan_context"
        ),
        "data/registries/curated_mechanism_labels.json": "current_702_label_registry",
        "data/registries/mechanism_fingerprints.json": (
            "production_fingerprint_registry"
        ),
    }
    return roles.get(name, "additional_source_context")
