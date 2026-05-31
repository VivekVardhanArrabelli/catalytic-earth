# Predicted-Geometry Confidence Is The Strongest Novelty-Abstention Signal

Run: 2026-05-31 (deployment-valid: predicted / AlphaFold geometry)

## Question

The cofactor-augmented novelty signal plateaus at AUC 0.694 and is *confidently
wrong* on the cofactor-confounded OOS rows (AUC 0.443). Does the geometry
channel's own confidence flag those rows where the cofactor channel fails — on
predicted (deployment) geometry, not experimental teacher geometry?

## Method (honest)

- Signal: `top1_score` from `hand_router_on_predicted_geometry.rows` in
  `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`.
  This is the geometry seed-fingerprint retrieval score computed on **predicted**
  AlphaFold structure (apo; cofactor context deleted — the D5 deployment regime).
- NOT `v3_geometry_retrieval_1025.json`: that one is experimental/teacher-side
  (pdb_id like 1B73, retains `local_ligand_cofactor_context`), so it trivially
  scores AUC 1.0 in vs OOS and is NOT deployment-valid. That trap was checked and
  rejected.
- Split: heldout rows with a known fingerprint = in-scope; heldout rows without =
  OOS. Score is an existing per-row artifact value, nothing fit here.
- AUC = P(in-scope top1_score > OOS top1_score). 0.5 = chance.

## Result (predicted geometry, deployment-valid)

| Comparison | AUC | n |
| --- | ---: | ---: |
| in-scope vs all OOS | **0.757** | 47 vs 79 |
| in-scope vs cofactor-confounded OOS | **0.840** | 47 vs 6 |

Means: in-scope 0.516, all-OOS 0.376, confounded-OOS 0.347.

Caveat: only 6 of the 8 cofactor-confounded rows have usable predicted geometry
(m_csa:549 predicted-structure fetch failed; m_csa:563 excluded from the predicted
rows), so the confounded comparison is n=6.

Per-confounded predicted-geometry top1 score: m_csa:30 0.262, m_csa:31 0.347,
m_csa:80 0.349, m_csa:191 0.372, m_csa:267 0.397, m_csa:448 0.358
(all well below the in-scope mean 0.516).

## Comparison to prior signals (same heldout split, predicted/deployment regime)

| Signal | in vs all-OOS AUC |
| --- | ---: |
| bare PLM nearest-centroid | 0.596 |
| cofactor-augmented nearest-centroid | 0.694 |
| **predicted-geometry top1 score** | **0.757** |

The predicted-geometry confidence is the first single signal at/above the 0.75
usability bar on the aggregate, and it is *strongest exactly where the cofactor
channel is weakest*: on the cofactor-confounded OOS it reaches 0.840 while the
cofactor channel is worse than chance (0.443). The two channels are complementary.

## Interpretation / forward

The de novo abstention gate should be **geometry-confidence-led**, with the
cofactor channel complementary rather than primary. Next steps:
1. Combine predicted-geometry confidence with cofactor agreement (weakest-channel
   / min-z gate) and measure aggregate AUC and in-scope retention.
2. Fold the predicted-geometry top1 signal into
   `mechanism_novelty_abstention_eval` as a first-class signal so the artifact
   reports it directly.
3. Recover predicted geometry for m_csa:549 / m_csa:563 to complete the confounded
   set.

## Guardrails

Predicted (not experimental) geometry; existing per-row scores, nothing fit on
heldout; no labels/registries/thresholds changed; M-CSA eval-only.
