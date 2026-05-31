# D11 Deployment-Valid Abstention Gate (de novo precondition)

Run: 2026-05-31T20:52:09Z

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

## Operating point (fixed untuned threshold, >=90% in-scope retention)

AUC alone is not a usable gate. At a threshold retaining >=90% of in-scope rows:

| Gate | threshold | OOS abstain-recall | confounded abstain-recall | in-scope retain |
| --- | ---: | ---: | ---: | ---: |
| geometry_led | 0.34 | 0.1392 | 0.1667 | 0.9362 |
| combined_mean | 0.26 | 0.6709 | 0.0 | 0.9149 |

A strong AUC does NOT yield a usable abstention threshold. At a fixed, untuned threshold that retains >=90% of in-scope rows, the geometry-led gate abstains on only ~19% of OOS, and the blind mean-combined gate (~59% OOS) abstains on NONE of the safety-critical cofactor-confounded rows. The score distributions overlap heavily; an AUC-passing gate is not yet a deployable one. The committed operating curve makes this explicit so the gap is not hidden behind the headline AUC.

## Per-channel rule gate (operational architecture)

Rule: `abstain if geometry_score < tg OR (cofactor_max < signature_threshold AND cofactor_max < tc)`.

- No viable operating point at 90% retention (`best_at_90pct_retention` = None); the feature overlap forbids it.
- At a relaxed 85% retention floor the cofactor lift is real: OOS abstain-recall 0.1392 (geometry only) -> 0.3038 (per-channel rule), **+0.1646**, concentrated on the cofactor-agnostic subset (0.3151).

## Interpretation

Deployment-valid best abstention AUC is 0.852141; the de novo precondition is MET on predicted geometry.

combined_mean reaches 0.852141 across all OOS but trades away safety on the cofactor-confounded subset (the cofactor channel is fooled there); geometry top1 score alone is 0.756935 overall and is the single safest channel, strongest exactly on the confounded rows. A deployment gate should lead with geometry confidence and use the cofactor channel as a complementary lift on cofactor-agnostic OOS.
