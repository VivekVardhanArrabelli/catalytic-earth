# Fold Channel Deployment-Readiness Summary

Run: 2026-06-28T21:54:53Z
Status: `deployment_claim_made_mcsa_heldout_passed_offmcsa_generalizes`

## Deployment Claim

- Made: **True** (scope: M-CSA mechanism recovery (the held-out split is M-CSA)).
- On the never-touched held-out M-CSA split (frozen, content-hashed, pre-registered), the June 9 cofactor-fusion router at the 0.44 dial recovers 35/47 (0.7447) in-scope mechanisms at 15/79 (0.1899) OOS false positives, PASSING the pre-committed bar (recovery >= 0.70, OOS-FP rate <= 0.40). Off the M-CSA distribution, the fold (structural) channel generalizes on both recovery and rejection.

## Question

- Is the fold (structural nearest-neighbour) channel a deployment-grade mechanism signal -- does it both recover correct mechanisms and abstain on out-of-scope inputs -- beyond the M-CSA development distribution?

## Off-M-CSA Generalization (the deployment question)

- **Recovery half** (offmcsa_bronze_high_confidence): 132/156 (0.8462) (M-CSA baseline 28/35 (0.8)); generalizes True.
  - Per family:
    - flavin_dehydrogenase_reductase: 83/96 (0.86)
    - metal_dependent_hydrolase: 26/34 (0.76)
    - heme_peroxidase_oxidase: 17/20 (0.85)
    - plp_dependent_enzyme: 6/6 (1.0)
- **Rejection half**: external-negative fold-NN median 0.5737 vs M-CSA OOS 0.5661 (in-scope 0.743); generalizes True.
- **Both halves generalize off M-CSA: True.**

## Deployable Operating Point

- June 9 router (registry pin d567ee0d) at the 0.44 cofactor dial: {'cofactor_threshold': 0.44, 'fold_threshold': 0.0, 'inscope_correct': 30, 'inscope_total': 35, 'oos_false_positives': 8, 'oos_total': 26}.
- Fold gate: tunable precision/recall + OOS-rejection dial; on the healthy June 9 router it does not Pareto-improve the dial point (residual OOS FPs are high-fold-similar), but it is the off-M-CSA abstention lever.

## Validated Claims

- HELD-OUT (M-CSA) PASS: June 9 router @ 0.44 dial recovers 35/47 (0.7447) at 15/79 OOS FP (0.1899) on the frozen pre-registered held-out split.
- Fold-NN recovers off-M-CSA bronze positives at 0.8462 across all 4 cofactor families (non-circular: bronze admission used sequence/cofactor, not structure).
- Fold-NN rejects off-M-CSA negatives: external-negative fold-NN median 0.5737 tracks the M-CSA OOS median 0.5661, far below the in-scope median 0.743.
- The June 9 router operating point is reproducible and clears the calibration recovery bar (30/35 @ 8 FP).

## Not Yet Validated

- No gold-truth off-M-CSA evaluation: bronze labels are automation-curated, so off-M-CSA recovery measures fold/sequence concordance, not gold accuracy.
- The validated held-out claim certifies M-CSA only; a SwissProt-wide gold deployment claim is not yet established.
- Coverage is scoped to the cofactor atlas families; broader-family recovery is not yet measured.
- All calibration operating points are development figures (calibration reused across readouts), not unbiased estimates.

## Remaining Gates For A Deployment Claim

- A gold-labelled off-M-CSA evaluation (or a curated subset) for recovery.
- Broaden the M-CSA atlas beyond the cofactor families and re-run recovery.

## Bottom Line

- DEPLOYMENT CLAIM (M-CSA): the pre-registered held-out one-shot PASSED -- June 9 router @ 0.44 dial recovers 35/47 at 15/79 OOS FP on the frozen held-out split. Off M-CSA, the fold (structural) channel generalises on both recovery and rejection. The validated claim is scoped to M-CSA; a SwissProt-wide gold claim still needs a gold off-M-CSA eval.

## Guardrails

- Read-only synthesis; no new scoring, no held-out read, no registry change.
