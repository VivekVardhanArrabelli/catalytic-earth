# Overnight Decision Dashboard - 2026-05-28
Refreshed after the active-site supervised-smoke scaffold. Review-only: no labels, registries, thresholds, production scoring, imports, or real model outputs changed.

## Repo
- HEAD: `47f4d6b`
- Working tree clean at dashboard write: `True`
- Disk available: `32Gi`

## Current User Decision Needed
- Whether to run the real supervised active-site smoke. Recommendation: Wait until user is awake; do not run automatically. Reason: It trains a model on CE data. Guardrails pass, but the user explicitly required approval before training.

## Gates
- `user_approval_for_real_supervised_smoke`: waiting_for_user | Approve or reject running the real active-site supervised smoke on the 547-row train/cal cache using the committed runbook. Without approval, do not train.
- `larger_representation_models`: do_not_run_now | None overnight; Wave 1.1 says larger models should wait.
- `external_panels_and_v2_labels`: next_safe_non_training_lane | No user decision needed for read-only prioritization; label changes still need approval.
- `geometry_foldseek_atlas_engine`: safe_to_prepare_read_only | No user decision for read-only design or feature consolidation.
- `disk_and_dirty_worktree`: pass | None

## Completed Lanes
- `active_site_cache_cli` [completed] commit `26387e4`: Built label-blind active-site cache CLI and smoke cache primitives. Next: done
- `external_identifier_resolution` [completed] commit `8e25029`: Resolved external/current702 identifiers and first materialization tranche. Next: done
- `wave1_2_cache_31` [completed] commit `e6bbd1d`: Materialized 31-row active-site cache for near-orphan/fold-conflict/OOS/external diagnostics. Next: done
- `cache_consistency_and_materialization` [completed] commit `7f80984`: Audited 31-row cache and prepared external fetch/materialization pack. Next: done
- `cache31_router_probe` [completed] commit `6bf2681`: Ran label-blind unsupervised 31-row router diagnostic; sufficient for future supervised smoke but not performance evidence. Next: done
- `local_tail_extension_pack` [completed] commit `3870b75`: Identified 10 local current702 tail rows for safe active-site cache extension. Next: done
- `local_tail_cache_extension` [completed] commit `b0e5605`: Built review-only readiness matrix and 10-row label-blind local-tail cache extension. Next: done
- `cache41_router_stress` [completed] commit `14c719f`: Stress-tested combined 31+10 cache; all 10 local-tail expected-pattern checks passed; still diagnostic only. Next: done
- `supervised_smoke_gate` [completed] commit `a804ff6`: Gate says supervised smoke is justified only with strict preconditions; current 41-row cache cannot be trained on. Next: done
- `train_cal_cache_feasibility` [completed] commit `7e5c405`: Built 547-row in-distribution train/cal feasibility and label-blind cache; no training. Next: done
- `train_cal_leakage_audit` [completed] commit `e12acff`: Leakage preflight passed: 547 cache rows, 0 blockers, 544 train/cal eligible and 3 canary-only. Next: done
- `supervised_smoke_runbook` [completed] commit `0edb5ec`: Wrote user-approval-gated runbook for real supervised smoke; no training. Next: user approval needed before execution
- `supervised_smoke_scaffold` [completed] commit `47f4d6b`: Implemented runner scaffold and toy tests only; did not run on real CE caches. Next: await user approval for real run or continue non-training feature/atlas work

## Key Metrics
- `train_cal_leakage_status`: pass
- `train_cal_blockers`: 0
- `train_cal_support_table`: [{'calibration': 73, 'target_group': 'None', 'total': 363, 'train': 290}, {'calibration': 8, 'target_group': 'flavin_dehydrogenase_reductase', 'total': 40, 'train': 32}, {'calibration': 3, 'target_group': 'heme_peroxidase_oxidase', 'total': 16, 'train': 13}, {'calibration': 13, 'target_group': 'metal_dependent_hydrolase', 'total': 66, 'train': 53}, {'calibration': 5, 'target_group': 'plp_dependent_enzyme', 'total': 25, 'train': 20}, {'calibration': 7, 'target_group': 'ser_his_acid_hydrolase', 'total': 34, 'train': 27}]
- `cache41_local_tail_expected_pattern_failures`: 0
- `wave1_1_learned_value_answer`: limited_not_decision_grade
- `runbook_requires_user_approval`: True

## Safe Next Launches
- `Foldseek Geometry Atlas Feature Prep` allowed `True`: read-only feature/engine design for near-orphan and wrong-transfer diagnostics; no labels/training/thresholds.
- `External V2 Acquisition Priority Pack` allowed `True`: read-only prioritization of external panels and label acquisition needs; no label imports.
- `Supervised Smoke Real Run` allowed `False`: requires user approval despite preflight pass.

## No-Go Conditions
- Do not train real models without user approval.
- Do not edit labels, registries, ontologies, thresholds, production scoring, or imports.
- Do not tune abstention thresholds on heldout/diagnostic rows.
- Do not use m_csa:497 or m_csa:750 in train/calibration.
- Stop expensive compute if disk falls below 10 GiB.
- Do not claim learned reps beat Foldseek/geometry from smoke scaffolding or diagnostics.
