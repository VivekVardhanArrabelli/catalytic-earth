# D11 Deployment-Valid Abstention Gate (de novo precondition)

Run: 2026-05-31T19:15:26Z

D11 de novo precondition, DEPLOYMENT-VALID: combine predicted-geometry fingerprint-retrieval confidence with the organic-cofactor head confidence directly over the held-out pool (both already calibrated [0,1]); no atlas, no eval-pool leakage.

Combination: `raw_calibrated_confidence_no_atlas_no_leakage` | regime: **predicted_geometry_deployment**

In-scope: 47 | OOS: 79 (confounded 6, agnostic 73)

## Abstention AUC (in-scope > OOS; 0.5 = chance) by channel and stratum

| Channel | all OOS | cofactor-confounded | cofactor-agnostic |
| --- | ---: | ---: | ---: |
| geometry_top1_score | 0.756935 | 0.840426 | 0.750073 |
| cofactor_max_score | 0.628064 | 0.280142 | 0.65666 |
| combined_mean | 0.852141 | 0.329787 | 0.895074 |
| combined_min_concordance | 0.608672 | 0.251773 | 0.638006 |

- Best overall AUC: **0.852141** -> clears 0.75 bar: **True**.
- Safest single channel (no stratum below chance): `geometry_top1_score`.

## Interpretation

Deployment-valid best abstention AUC is 0.852141; the de novo precondition is MET on predicted geometry.

combined_mean reaches 0.852141 across all OOS but trades away safety on the cofactor-confounded subset (the cofactor channel is fooled there); geometry top1 score alone is 0.756935 overall and is the single safest channel, strongest exactly on the confounded rows. A deployment gate should lead with geometry confidence and use the cofactor channel as a complementary lift on cofactor-agnostic OOS.
