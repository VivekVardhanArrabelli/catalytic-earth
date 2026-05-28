# Active-Site Train/Cal Leakage Audit - 2026-05-28
Review-only preflight audit. No model training, labels, registries, thresholds, or production scoring changed.

## Status
- `training_preflight_status`: `pass`
- `blocker_count`: `0`
- `readiness_row_count`: `547`
- `cache_row_count`: `547`

## Support
- `None`: total 363, train 290, calibration 73
- `flavin_dehydrogenase_reductase`: total 40, train 32, calibration 8
- `heme_peroxidase_oxidase`: total 16, train 13, calibration 3
- `metal_dependent_hydrolase`: total 66, train 53, calibration 13
- `plp_dependent_enzyme`: total 25, train 20, calibration 5
- `ser_his_acid_hydrolase`: total 34, train 27, calibration 7

## Checks
- PASS `cache_rows_match_readiness_rows_exactly`
- PASS `feasibility_rows_match_readiness_rows_exactly`
- PASS `all_rows_are_in_distribution_in_sequence_split`
- PASS `train_cal_eligible_rows_have_only_train_or_calibration_assignment`
- PASS `excluded_rows_absent`
- PASS `secondary_ood_probe_rows_are_canary_only`
- PASS `predictive_features_have_no_forbidden_key_fragments`
- PASS `cache_records_have_metadata_and_predictive_features_separated`
- PASS `train_cal_split_is_sequence_cluster_consistent_within_target_group`
- PASS `primary_and_oos_targets_have_train_and_calibration_support`
- PASS `cache_summary_guardrails_zero`

This pass does not authorize training by itself; it only says the train/cal cache clears leakage preflight if the user later approves a supervised smoke.
