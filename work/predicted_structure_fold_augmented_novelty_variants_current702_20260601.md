# Predicted-Structure Fold-Augmented Novelty Variants - current702

Review-only diagnostic combining existing predicted-atlas geometry novelty rows with the already-scored AlphaFoldDB predicted-structure nearest-atlas TM channel. No Foldseek rerun, coordinate fetch, threshold selection, label import, or split change was performed.

## Counts

- overlap_rows: 126
- inscope: 47
- oos: 79
- confounded_predicted_geometry_oos: 6
- signals: 11

## Signal Summary

| Signal | AUC all OOS | AUC confounded OOS | 90% retain OOS abstain | 85% retain OOS abstain |
|---|---:|---:|---:|---:|
| `mean_top1_raw_and_tm` | 0.907622 | 0.911348 | 0.7215 | 0.7722 |
| `harmonic_top1_raw_and_tm` | 0.899542 | 0.911348 | 0.7468 | 0.8354 |
| `mean_top1_atlas_percentile_and_tm` | 0.898196 | 0.914894 | 0.7722 | 0.7848 |
| `mean_top1_role_atlas_percentile_and_tm` | 0.875842 | 0.85461 | 0.7468 | 0.8228 |
| `mean_cofactor_context_atlas_percentile_and_tm` | 0.838944 | 0.893617 | 0.6203 | 0.7342 |
| `nearest_atlas_tm_score` | 0.814301 | 0.829787 | 0.4177 | 0.5063 |
| `mean_role_atlas_percentile_and_tm` | 0.775518 | 0.783688 | 0.519 | 0.519 |
| `min_top1_raw_and_tm` | 0.764745 | 0.840426 | 0.2152 | 0.3038 |
| `min_top1_atlas_percentile_and_tm` | 0.759628 | 0.842199 | 0.1899 | 0.2532 |
| `top1_score_raw` | 0.756935 | 0.840426 | 0.2152 | 0.3038 |
| `top1_score_atlas_percentile` | 0.756396 | 0.842199 | 0.1899 | 0.2532 |

## Best Signal

- name: `mean_top1_raw_and_tm`
- all-OOS AUC: 0.907622
- confounded-OOS AUC: 0.911348

## Interpretation

- Best fold-augmented variant is mean_top1_raw_and_tm with all-OOS AUC 0.907622.
- yes_for_rank_auc_vs_geometry_only; combined variants improve over the prior geometry-only best all-OOS AUC while remaining diagnostic only
- Retention operating points are reported for diagnosis only; no deployment threshold is selected or promoted.
- If this diagnostic is useful, re-express the strongest combined variant as a train/cal-only threshold contract before any heldout-facing claim.

## Source Artifacts

| Artifact | SHA256 |
|---|---|
| `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json` | `1c09f7cad3bec0da694e03ac1d60f9c6bc96e9208d13bbb06a90095170a2ef13` |
| `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json` | `565266bfd8379c75104e1d7a74457ef40846563ea71988c4946d16c92f733582` |
| `artifacts/v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.json` | `a22edd41f2bc88a38dd52e76f24094d34e567422b3ced15c626314fadc05d2c6` |
