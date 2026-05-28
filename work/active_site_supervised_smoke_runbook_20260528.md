# Active-Site Supervised Smoke Runbook - 2026-05-28
No training was run. This is an approval-gated runbook for a tiny supervised active-site encoder smoke.

## Approval Status
- `user_approval_required_before_training`: True
- `training_preflight_status_from_audit`: pass
- `blocker_count_from_audit`: 0
- `may_run_now_without_user_approval`: False

## Why It Is Worth Testing
- Wave 1.1 showed learned representations are not decision-grade against Foldseek/geometry on current broad labels, but it did not test a feature set restricted to active-site geometry/cofactor/pocket descriptors.
- The new 547-row cache gives an in-distribution train/cal pool that clears leakage preflight; this lets a tiny supervised smoke ask whether active-site-local features learn anything beyond the hand-built geometry scorer.
- The 41-row diagnostic cache contains near-orphan, fold-conflict, OOS, external-priority, and local-tail stress rows that can be held out entirely from training and used only for qualitative diagnostics.
- A negative result is valuable: if this active-site feature smoke fails, it argues for external label acquisition and geometry/Foldseek routing before spending compute on larger neural models.

## Dataset Contract
- `train_cal_cache`: artifacts/v3_active_site_encoder_cache_train_cal_547_20260528.jsonl
- `train_cal_feasibility`: artifacts/v3_active_site_train_cal_cache_feasibility_20260528.json
- `diagnostic_eval_caches`: ['artifacts/v3_active_site_encoder_cache_wave1_2_31_20260528.jsonl', 'artifacts/v3_active_site_encoder_cache_local_tail_extension_10_20260528.jsonl']
- `train_rows`: metadata.split_assignment == in_distribution_train_cal_candidate and proposed_train_cal_split == train from feasibility artifact
- `calibration_rows`: metadata.split_assignment == in_distribution_train_cal_candidate and proposed_train_cal_split == calibration from feasibility artifact
- `canary_only_rows`: metadata.split_assignment == in_distribution_secondary_canary_only; never train/calibrate
- `evaluation_only_rows`: all 31+10 diagnostic rows; never train/calibrate or tune threshold
- `excluded_rows`: ['m_csa:497', 'm_csa:750', 'all heldout rows', 'all review_only_not_training rows', 'all secondary OOD probe rows from train/calibration']
- `support_from_leakage_audit`: [{'calibration': 73, 'target_group': 'None', 'total': 363, 'train': 290}, {'calibration': 8, 'target_group': 'flavin_dehydrogenase_reductase', 'total': 40, 'train': 32}, {'calibration': 3, 'target_group': 'heme_peroxidase_oxidase', 'total': 16, 'train': 13}, {'calibration': 13, 'target_group': 'metal_dependent_hydrolase', 'total': 66, 'train': 53}, {'calibration': 5, 'target_group': 'plp_dependent_enzyme', 'total': 25, 'train': 20}, {'calibration': 7, 'target_group': 'ser_his_acid_hydrolase', 'total': 34, 'train': 27}]

## Tiny Models
- `logistic_l2_balanced`: primary tiny supervised smoke | multinomial logistic regression, L2 regularization, class_weight=balanced, max_iter=2000, deterministic seed 20260528
- `nearest_centroid_active_site`: nonparametric sanity baseline on same vectors | train-set class centroids in z-scored feature space; confidence from negative distance margin
- `ridge_one_vs_rest_fallback`: fallback if sklearn is unavailable | closed-form ridge one-vs-rest on train matrix using numpy; calibration from margins

## Exact Command After User Approval
```bash
PYTHONPATH=src python -m catalytic_earth.cli validate
python -m json.tool artifacts/v3_active_site_train_cal_leakage_audit_20260528.json >/dev/null
python - <<'PY'
import json
a=json.load(open("artifacts/v3_active_site_train_cal_leakage_audit_20260528.json"))
assert a["training_preflight_status"] == "pass"
assert a["summary"]["blocker_count"] == 0
PY
PYTHONPATH=src python tools/research_lanes/active_site_supervised_smoke/run_active_site_supervised_smoke.py --train-cal-cache artifacts/v3_active_site_encoder_cache_train_cal_547_20260528.jsonl --train-cal-feasibility artifacts/v3_active_site_train_cal_cache_feasibility_20260528.json --diagnostic-cache artifacts/v3_active_site_encoder_cache_wave1_2_31_20260528.jsonl --diagnostic-cache artifacts/v3_active_site_encoder_cache_local_tail_extension_10_20260528.jsonl --leakage-audit artifacts/v3_active_site_train_cal_leakage_audit_20260528.json --out artifacts/v3_active_site_supervised_smoke_predictions_20260528.jsonl --summary-out artifacts/v3_active_site_supervised_smoke_summary_20260528.json --report-out work/active_site_supervised_smoke_20260528.md --seed 20260528 --no-production-claims
python -m json.tool artifacts/v3_active_site_supervised_smoke_summary_20260528.json >/dev/null
PYTHONPATH=src python -m catalytic_earth.cli validate
git diff --check
```

## Stop Conditions
- Any heldout or review_only_not_training row is selected for train/calibration.
- Any forbidden metadata key appears under predictive_features or flattened feature names.
- m_csa:497 or m_csa:750 appears in train/calibration.
- Calibration threshold is selected using any diagnostic/heldout cell.
- OOS false-positive rate on calibration cannot meet the predeclared gate without abstaining on all rows.
- Disk falls below 10 GiB.
- The run attempts to write labels, registries, thresholds, production scoring, imports, or ontology files.

## Risk Assessment
- `main_risk`: The smoke may mostly rediscover the hand-built geometry features already known to work, so success is not automatically novel.
- `mitigation`: Compare only within the diagnostic report against Wave 1.1 geometry/Foldseek cells; treat the result as a routing/feature feasibility test, not a claim.
- `overfit_risk`: Moderate because train/cal comes from M-CSA and broad parent labels; controlled by heldout diagnostic cells and no threshold tuning outside calibration.
- `value_if_negative`: A negative or abstain-heavy result would justify focusing on external panels, v2 labels, and geometry/Foldseek engine rather than neural scaling.
