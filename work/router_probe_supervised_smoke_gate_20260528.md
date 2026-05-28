# Router Probe Supervised Smoke Gate - 2026-05-28
Review-only gate decision. No model training, label edits, threshold changes, or registry changes were made.

## Decision
- `is_supervised_active_site_encoder_smoke_scientifically_justified_now`: yes_with_strict_preconditions
- `is_training_allowed_from_current_41_row_cache`: no
- `why_not_current_41_cache`: The 41-row cache contains 22 heldout rows, 10 review_only_not_training rows, and only 9 in_distribution rows. Training directly on it would either be underpowered or create heldout leakage.
- `minimum_safe_next_step`: Build a full in-distribution train/calibration active-site cache from current702 geometry-ok rows, then run any supervised smoke only against frozen diagnostic cells. This gate itself does not train.
- `decision_grade_claim_allowed_after_smoke`: False

## Why
- Current 41-row cache split counts: `{'heldout': 22, 'in_distribution': 9, 'review_only_not_training': 10}`
- In-distribution geometry-ok train candidate pool from current702: `547` rows.
- In-distribution geometry-ok support by fingerprint: `{'None': 363, 'cobalamin_radical_rearrangement': 2, 'flavin_dehydrogenase_reductase': 40, 'flavin_monooxygenase': 1, 'heme_peroxidase_oxidase': 16, 'metal_dependent_hydrolase': 66, 'plp_dependent_enzyme': 25, 'ser_his_acid_hydrolase': 34}`
- Wave 1.1 says learned reps have limited non-decision-grade value; geometry remains stronger in near-orphan/wrong-transfer cells.
- The 31/41 active-site caches are structurally valid for diagnostics, but the current 41-row cache is not a training set.

## Smallest Safe Contract
- `phase_0_required_before_training`: Build and validate a train/calibration cache from in_distribution current702 rows only.
- `train_pool_rule`: partition == in_distribution AND geometry status ok AND local coordinate/materialized geometry available AND label/fingerprint IDs metadata-only until target extraction.
- `excluded_from_train`: ['partition == heldout', 'split_assignment == review_only_not_training', 'external_router_priority rows without approved train partition', 'quarantined rows', 'm_csa:497', 'm_csa:750', 'any row marked canary-only or OOS diagnostic-only']
- `target_policy`: Use frozen parent-v1 primary fingerprints plus explicit OOS/none target only for training-smoke diagnostics; secondary OOD probes and proposed child labels are evaluation/canary-only until separately approved.
- `calibration_rule`: Split only within in_distribution train pool by sequence cluster where possible; use calibration to choose abstention threshold. Never tune on heldout, near-orphan, fold-conflict, OOS router controls, or local-tail diagnostic rows.
- `evaluation_cells`: ['clean_near_orphan_anchor', 'fold_conflict_reference_anchor', 'oos_router_control', 'current702_local_tail_extension', 'secondary_ood_probe rows where present']
- `required_metrics`: ['coverage', 'risk on non-abstained predictions', 'OOS false-positive rate by cell', 'wrong-Foldseek-transfer rescue count', 'near-orphan rescue count', 'canary failures', 'ECE only if n>=50 for the evaluated bin']
- `stop_conditions`: ['any heldout row appears in train/calibration', 'any target label or entry/source id appears in predictive_features', 'OOS false-positive rate exceeds geometry/Foldseek reference in the same cell', 'canary failure on quarantined rows', 'disk below 10 GiB', 'metric generated without row-aligned prediction export']
- `non_claims`: ['no production metric', 'no label promotion', 'no ontology update', 'no threshold update', 'no claim that learned reps beat Foldseek/geometry from this smoke alone']

## Next Automation
- `id_suggestion`: active-site-train-cal-cache-feasibility
- `task`: Build the exact in-distribution train/calibration cache feasibility artifact and optional label-blind cache, without training. Use the 547 geometry-ok in_distribution rows as the candidate pool and report per-fingerprint support before any model run.
- `run_training_after_this_gate`: False
