# D11 Two-Channel Abstention Gate (de novo precondition)

Run: 2026-06-01T02:04:11Z

D11 de novo precondition: a two-channel abstention gate (cofactor-augmented PLM + geometry active-site role-agreement) over the predicted_geometry_deployment geometry regime, with deployable atlas-percentile combination.

Geometry regime: **predicted_geometry_deployment** | normalization: `atlas_percentile_deployable`

In-scope: 47 | OOS: 79 (confounded 6, agnostic 73) | Atlas: 168

## Abstention AUC (in-scope > OOS; 0.5 = chance) by channel and stratum

| Channel | all OOS | cofactor-confounded | cofactor-agnostic |
| --- | ---: | ---: | ---: |
| cofactor_augmented | 0.697953 | 0.363475 | 0.725444 |
| geometry_score_x_role | 0.748047 | 0.748227 | 0.748033 |
| combined_mean | 0.847697 | 0.62766 | 0.865783 |
| combined_min_concordance | 0.664288 | 0.524823 | 0.675751 |

- Best overall AUC: **0.847697** -> clears 0.75 bar: **True**.

## Interpretation

Best overall abstention AUC is 0.847697 on the predicted_geometry_deployment regime; the two-channel gate clears the 0.75 de novo precondition bar.

The cofactor channel handles the cofactor-agnostic OOS majority but confidently misplaces novel enzymes that reuse a known cofactor family. The geometry role-agreement channel catches exactly those: novel chemistry shows the right active-site residues with the wrong catalytic roles. Combining the two atlas-percentiles recovers the cases each channel misses.

**Deployment caveat.** Deployment-regime (predicted geometry) gate evaluated directly.
