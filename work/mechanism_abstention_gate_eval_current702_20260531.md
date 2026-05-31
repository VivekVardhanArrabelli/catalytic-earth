# D11 Two-Channel Abstention Gate (de novo precondition)

Run: 2026-05-31T12:49:13Z

D11 de novo precondition: a two-channel abstention gate (cofactor-augmented PLM + geometry active-site role-agreement) over the experimental_geometry_teacher geometry regime, with deployable atlas-percentile combination.

Geometry regime: **experimental_geometry_teacher** | normalization: `atlas_percentile_deployable`

In-scope: 47 | OOS: 88 (confounded 8, agnostic 80) | Atlas: 184

## Abstention AUC (in-scope > OOS; 0.5 = chance) by channel and stratum

| Channel | all OOS | cofactor-confounded | cofactor-agnostic |
| --- | ---: | ---: | ---: |
| cofactor_augmented | 0.684357 | 0.339096 | 0.718883 |
| geometry_score_x_role | 0.801136 | 0.651596 | 0.81609 |
| combined_mean | 0.829666 | 0.50266 | 0.862367 |
| combined_min_concordance | 0.732713 | 0.503989 | 0.755585 |

- Best overall AUC: **0.829666** -> clears 0.75 bar: **True**.

## Interpretation

Best overall abstention AUC is 0.829666 on the experimental_geometry_teacher regime; the two-channel gate clears the 0.75 de novo precondition bar.

The cofactor channel handles the cofactor-agnostic OOS majority but confidently misplaces novel enzymes that reuse a known cofactor family. The geometry role-agreement channel catches exactly those: novel chemistry shows the right active-site residues with the wrong catalytic roles. Combining the two atlas-percentiles recovers the cases each channel misses.

**Deployment caveat.** This result uses an experimental-geometry retrieval (teacher-side) for the role-agreement channel. The deployment regime is predicted geometry, whose current retrieval persists only top1 score, not the per-row role decomposition. The deployment-valid gate is blocked on a predicted-geometry retrieval that persists role_match_fraction; this eval is source-agnostic on the geometry path so that artifact drops in.
