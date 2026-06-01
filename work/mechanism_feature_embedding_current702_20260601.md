# D11 Learned Mechanism-Feature Embedding (Lever 2)

Run: 2026-06-01T19:17:07Z

D11 Lever 2: a learned, information-preserving mechanism-feature embedding (sequence-only ESM2-150M; atlas-fit within-class whitening over the atlas PCA span). Tests whether its novelty signals separate in-scope from out-of-scope (novel-chemistry) held-out rows better than the predicted-geometry top1_score baseline (AUC 0.757), evaluated at the operating point and stratified by cofactor-confounded vs -agnostic OOS.

## Learned space (atlas-fit, sequence-only)

- Input: `esm2_150m_sequence_only` | atlas rows: 184 | classes: 7
- PCA span dim: **128** capturing 0.989091 of atlas variance (target 0.99, cap 128)
- Within-class whitening shrinkage: 0.1 | metric condition number: 99.3943

Deployment pool: in-scope 47 | OOS 79 (confounded 6, agnostic 73)

## Novelty separation on the deployment pool (AUC in-scope > OOS; 0.5 = chance)

| Signal | all OOS | confounded | agnostic | OOS-recall@90%ret | retain |
| --- | ---: | ---: | ---: | ---: | ---: |
| learned_nearest_prototype | 0.606248 | 0.663121 | 0.601574 | 0.1646 | 0.9362 |
| learned_knn_density | 0.612981 | 0.670213 | 0.608277 | 0.1266 | 0.9787 |
| learned_out_of_span_residual | 0.72098 | 0.663121 | 0.725736 | 0.2405 | 0.9362 |
| learned_combined_primary | 0.61554 | 0.671986 | 0.610901 | 0.1646 | 0.9149 |
| **baseline: geometry_top1_score** | 0.756935 | 0.840426 | 0.750073 | 0.2152 | 0.9149 |

## Verdict

- Primary signal: `learned_combined_primary`
- AUC (deployment): learned **0.61554** vs baseline **0.756935** -> beats: **False**
- OOS-abstain-recall @>=90% retention: learned **0.1646** vs baseline **0.2152** -> beats: **False**
- Overall (predeclared primary): **does_not_beat_baseline**

### Exploratory: best single learned signal (not a predeclared claim)

- Signal: `learned_out_of_span_residual` | AUC all 0.72098 (confounded 0.663121, agnostic 0.725736)
- OOS-abstain-recall @>=90% retention: **0.2405** (baseline 0.2152) -> beats baseline at operating point: **True**
- Confounded-subset abstain-recall: 0.3333 -> safe vs baseline: **False** | role: `complementary_lift_channel_not_replacement_gate`

## Interpretation

NEGATIVE RESULT (clean) on the predeclared signal: the learned sequence-only embedding's primary combined novelty score does NOT beat the predicted-geometry top1_score baseline (AUC 0.61554 vs 0.756935; OOS-abstain-recall 0.1646 vs 0.2152 at >=90% retention). A general-purpose PLM, even reshaped by a supervised mechanism metric, encodes overall protein similarity under which novel chemistry still sits inside occupied regions, while the orthogonal geometry channel sees the active-site mismatch directly.

Lead worth a frozen follow-up: the `learned_out_of_span_residual` view -- a genuinely new, UNSUPERVISED representation signal (sequence-representation mass outside the directions known mechanism chemistry occupies) -- abstains on 0.2405 of OOS at >=90% retention, ABOVE the geometry baseline (0.2152), with AUC 0.72098. It is concentrated on the cofactor-AGNOSTIC OOS majority and is NOT safe on the safety-critical cofactor-confounded subset (confounded abstain-recall 0.3333 vs baseline 0.5), so it is a COMPLEMENTARY LIFT channel for future predeclared confirmatory testing, not a replacement gate. The supervised whitening distances (prototype/kNN) do not help, confirming that discriminative reshaping is the wrong lever for novelty.

The metric whitens out pooled within-mechanism variation (sequence drift that does not change catalysis) and is full-rank/invertible on the atlas span -- it reshapes geometry to answer to mechanism chemistry without collapsing to a rank-(K-1) discriminant (whose linear discriminative-energy novelty signal is already at chance here, AUC 0.524). The out-of-span residual is a genuinely new novelty view -- representation mass outside known mechanism chemistry -- not a recombination of the existing channels.

The predeclared equal-weight percentile combiner washes out the residual: every held-out row sits below the atlas residual distribution, so the residual's atlas-percentile saturates to 0 and contributes no ordering to the mean. The residual carries real signal only in its RAW form and must be used as its own channel -- an instructive reason the naive combination fails.

The cofactor-confounded OOS subset (novel chemistry reusing a known cofactor family) is the hardest; per-stratum AUCs and abstain-recalls are reported so a headline number cannot hide a confounded-subset failure.
