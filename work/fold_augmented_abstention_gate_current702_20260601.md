# Fold-Augmented Abstention Gate - current702

Run: 2026-06-01T03:13:12Z

Fold-augmented deployment abstention diagnostic over heldout rows with ok predicted geometry: raw predicted-geometry top1 confidence, sequence-only selected organic cofactor max score, and real predicted-structure nearest-atlas Foldseek/TM score.

## Counts

- Heldout rows scored: 126
- In-scope: 47
- OOS: 79
- Cofactor-confounded OOS: 6

## Best Channel

- combined_mean_geometry_fold: AUC all OOS 0.907622; confounded AUC 0.911348
- Best >=90% retention diagnostic: {'threshold': 0.48945, 'inscope_retain_recall': 0.9149, 'oos_abstain_recall': 0.7215, 'confounded_abstain_recall': 0.8333}
- Best >=85% retention diagnostic: {'threshold': 0.503, 'inscope_retain_recall': 0.8511, 'oos_abstain_recall': 0.7722, 'confounded_abstain_recall': 0.8333}

## Channels

| Channel | all OOS AUC | confounded AUC | agnostic AUC |
| --- | ---: | ---: | ---: |
| geometry_top1_score | 0.756935 | 0.840426 | 0.750073 |
| cofactor_max_score | 0.628064 | 0.280142 | 0.65666 |
| fold_nearest_atlas_tm_score | 0.814301 | 0.829787 | 0.813028 |
| combined_mean_geometry_cofactor_fold | 0.887961 | 0.464539 | 0.922763 |
| combined_mean_geometry_fold | 0.907622 | 0.911348 | 0.907316 |
| combined_min_geometry_fold | 0.764745 | 0.840426 | 0.758525 |

## Interpretation

- Best fold-augmented diagnostic channel is combined_mean_geometry_fold with AUC 0.907622 overall.
- This is a no-fit diagnostic over heldout rows, not a selected deployment threshold or production scoring change.
