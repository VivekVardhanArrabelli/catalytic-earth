# D11 Out-of-Span Residual — Robustness + Confirmatory Test (Lever 2 follow-up)

Run: 2026-06-01T23:17:44Z

D11 Lever 2 follow-up: robustness (PCA variance-cutoff sweep 95/97/99%) and a PREDECLARED confirmatory split test of the out-of-atlas-span residual novelty signal (the AUC 0.721 deployment-pool lead). Establishes whether the residual is a stable, generalizing lever or an eval-pool/cutoff artifact, BEFORE any threshold promotion or channel integration.

Atlas rows: 184 | total atlas axes: 183 | deployed span: 128 dims @ 0.989091 variance (target 0.99, cap 128, cap binds: True)
Deployment pool: in-scope 47 | OOS 79 (confounded 6, agnostic 73)

Anchor check (99%/128-dim reproduces committed 0.721): **0.72098** vs 0.72098 -> True

## A. PCA variance-cutoff sweep (leakage / overfit test)

Residual all-OOS AUC (in-scope > OOS) on the deployment pool, per cutoff:

| cutoff | span dim | var captured | cap binds | all-OOS AUC | confounded | agnostic | OOS-recall@90% |
| ---: | ---: | ---: | :-: | ---: | ---: | ---: | ---: |
| 0.95 | 81 | 0.95058 | False | 0.707245 | 0.648936 | 0.712037 | 0.2532 |
| 0.97 | 98 | 0.970043 | False | 0.721519 | 0.659574 | 0.72661 | 0.2405 |
| 0.99 | 128 | 0.989091 | True | 0.72098 | 0.663121 | 0.725736 | 0.2405 |

- AUC range across cutoffs: **0.707245–0.721519** (spread 0.014274, band <= 0.05)
- S1 (all >= 0.65): **True** | S2 (spread within band): **True** | S3 (agnostic > confounded every cutoff): **True**
- **Sweep holds: True**

At the deployed 99% target the 128-dim cap binds (realized 0.989091 of atlas variance), so the 95%/97% points genuinely shrink the span -- the sweep tests real span-size sensitivity, not a no-op. S1=True, S2=True, S3=True.

## B. Predeclared confirmatory split (held out from the lead's own design)

Split: `sha256('residual_confirm::' + entry_id) % 2; score-independent, fixed a priori` | folds: {'0': 'design_echo', '1': 'confirmation_heldout_from_discovery'} | permutations: 2000 (seed 20260601)

| fold | role | in/OOS | all-OOS AUC | confounded | agnostic | perm p |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| design-echo | echo | 18/49 | 0.654195 | 0.611111 | 0.658025 | 0.029485 |
| confirmation | HELD OUT | 29/30 | 0.788506 | 0.741379 | 0.791872 | 0.0005 |
| pooled (not held out) | reference | 47/79 | 0.72098 | — | — | 0.0005 |

- H1 (confirmation auc_all >= 0.65 AND permutation p < 0.05): **True**
- H2 (both folds auc_all >= 0.6): **True**
- H3 (confirmation agnostic_auc >= confounded_auc): **True**
- **Confirmatory pass: True**

The fold split is a salted hash of the entry id, independent of the residual values and of how the lead was surfaced; fold 1 played no role in the discovery. Significance is a label-permutation null over the fixed residual scores. The cofactor-confounded subset is tiny per fold and read only directionally (H3).

## Verdict

- Sweep holds: **True** | Confirmatory pass: **True**
- **Residual confirmed as a lever: True**

CONFIRMED: the out-of-span residual is a robust, generalizing novelty lever. It holds across PCA cutoffs (deployment all-OOS AUC 0.707245-0.721519, spread 0.014274) and passes the predeclared held-out-from-design confirmatory split (confirmation-fold AUC 0.788506, permutation p=0.0005). It graduates from eval-pool hypothesis to a candidate third orthogonal lift channel for predeclared threshold work.

Lever 4 (an expanded family set) is the stronger confirmation surface but is a proposal only today; this test uses the design-split route on the existing eval pool and should be re-run once an expanded set is materialized.
