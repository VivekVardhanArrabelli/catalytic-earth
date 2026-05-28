# Active-Site Train/Calibration Cache Feasibility - 2026-05-28
Review-only feasibility artifact. No model training, label edits, threshold changes, or registry changes were made.

## Summary
- `scanned_current702_rows`: 702
- `in_distribution_rows`: 562
- `geometry_ok_pocket_descriptor_rows_after_exclusions`: 547
- `train_cal_eligible_rows`: 544
- `secondary_canary_only_rows`: 3
- `missing_local_coordinate_count`: 0
- `coordinate_status_counts`: {'already_materialized_primary_cache': 532, 'already_materialized_alternate_cache': 15}
- `target_group_counts`: {'None': 363, 'ser_his_acid_hydrolase': 34, 'flavin_dehydrogenase_reductase': 40, 'metal_dependent_hydrolase': 66, 'heme_peroxidase_oxidase': 16, 'cobalamin_radical_rearrangement': 2, 'plp_dependent_enzyme': 25, 'flavin_monooxygenase': 1}
- `train_cal_eligible_target_group_counts`: {'None': 363, 'ser_his_acid_hydrolase': 34, 'flavin_dehydrogenase_reductase': 40, 'metal_dependent_hydrolase': 66, 'heme_peroxidase_oxidase': 16, 'plp_dependent_enzyme': 25}
- `proposed_split_counts`: {'train': 435, 'calibration': 109, 'canary_only_not_train_or_calibration': 3}
- `excluded_rows`: ['m_csa:497', 'm_csa:750']
- `interpretation`: There is enough in-distribution, geometry-ok, locally materialized current702 support to build a parent-v1/OOS train/cal active-site cache for a future supervised smoke. This artifact and cache remain review-only and perform no training.

## Split Plan
- `None`: eligible 363, train 290, calibration 73, clusters 338
- `flavin_dehydrogenase_reductase`: eligible 40, train 32, calibration 8, clusters 36
- `heme_peroxidase_oxidase`: eligible 16, train 13, calibration 3, clusters 15
- `metal_dependent_hydrolase`: eligible 66, train 53, calibration 13, clusters 64
- `plp_dependent_enzyme`: eligible 25, train 20, calibration 5, clusters 21
- `ser_his_acid_hydrolase`: eligible 34, train 27, calibration 7, clusters 28

## Cache Command Run
A review-only label-blind cache command is allowed because all selected rows have local coordinates and geometry-ok pocket descriptors.
