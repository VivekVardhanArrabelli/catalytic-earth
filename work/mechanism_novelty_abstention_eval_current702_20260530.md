# D11 Mechanism Novelty Abstention (de novo precondition)

Run: 2026-05-31T02:06:52Z

D11 de novo precondition: measure whether cheap unsupervised distance signals in the ESM2-150M mechanism space separate in-scope held-out queries from out-of-scope (novel-chemistry) held-out rows.

In-scope held-out: 48 | OOS held-out: 92 | Atlas: 184

## Abstention signals (AUC that in-scope > OOS; 0.5 = chance)

| Signal | AUC | in-scope mean | OOS mean |
| --- | ---: | ---: | ---: |
| nearest_atlas_cosine | 0.547101 | 0.519064 | 0.495441 |
| nearest_centroid_cosine | 0.596467 | 0.294294 | 0.253897 |
| centroid_top1_top2_margin | 0.566576 | 0.140771 | 0.10748 |
| betweenclass_subspace_projnorm | 0.52423 | 7.963788 | 7.489623 |

- Bare-PLM best AUC: **0.596467** -> status `unsolved_by_unsupervised_distance`.

## Cofactor-augmented signals

Source: `trained:esm2_t12_35m,trained:esm2_t6_8m`. In-scope: 48 | OOS: 92 | Atlas: 184

| Signal | AUC | in-scope mean | OOS mean |
| --- | ---: | ---: | ---: |
| cofactor_max_raw_score | 0.636209 | 0.379595 | 0.164706 |
| augmented_nearest_centroid | 0.693614 | 0.716278 | 0.579234 |
| augmented_centroid_margin | 0.603487 | 0.405319 | 0.285022 |

- Cofactor-augmented best AUC: **0.693614**.

## Interpretation

Bare-PLM best abstention AUC is 0.596467; cofactor augmentation lifts it to 0.693614.

OOS rows are real, well-folded enzymes with novel mechanism chemistry. A general-purpose PLM embedding encodes overall protein similarity, under which novel enzymes still look like ordinary proteins and sit inside occupied regions, so raw embedding distance is near chance. The mechanism-discriminative cofactor channel moves the signal in the right direction (novel chemistry carries lower in-class cofactor confidence) but does not yet clear the abstention bar, so the de novo precondition remains an open problem pending a stronger mechanism-feature signal.
