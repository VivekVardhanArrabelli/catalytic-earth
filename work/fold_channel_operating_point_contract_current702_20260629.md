# Fold-Channel Operating-Point Contract (Development Surface)

Run: 2026-06-29T13:58:09Z
Status: `fold_channel_operating_point_contract_development_surface_pending_heldout_validation`

## Bottom line

- FOLD-CHANNEL OPERATING-POINT CONTRACT (development surface): the recommended deployable point is fold-NN tau* = 0.65, where the channel recovers 0.7115 of off-M-CSA positives at 0.8952 precision while abstaining on 0.1923 of external non-M-CSA negatives. The recomputed curve reproduces both published readouts exactly. This is a development-surface recommendation; it needs a fresh pre-registered held-out before it is a deployment claim.

## Objective (fixed before reading any number)

- Select the lowest fold-NN threshold whose off-distribution (external non-M-CSA) false-accept rate is <= 0.2; that is the deployable abstaining point.
- Rationale: The 0.2 rejection floor mirrors the project's one validated open-set number -- the held-out OOS false-positive rate (0.19) -- so the point is anchored to a validated operating regime rather than tuned to maximise recovery.
- Selection surface: development only: M-CSA calibration in-scope (35) + OOS (26) + off-M-CSA bronze positives (156) + external non-M-CSA negatives (52). The spent M-CSA held-out one-shot was NOT read.

## Operating-point curve (one grid, all surfaces)

Recovery columns are recovery_of_all_positives (abstentions count against recall); precision is on retained. Rejection columns are false-accept rates on out-of-scope inputs (lower is better).

| fold tau | M-CSA rec | M-CSA prec | offMCSA rec | offMCSA prec | combined rec | OOS f-accept | ext f-accept |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 0.800 | 0.800 | 0.846 | 0.846 | 0.838 | 1.000 | 1.000 |
| 0.5 | 0.743 | 0.867 | 0.782 | 0.884 | 0.775 | 0.692 | 0.731 |
| 0.566 | 0.714 | 0.926 | 0.769 | 0.902 | 0.759 | 0.500 | 0.519 |
| 0.6 | 0.714 | 0.926 | 0.724 | 0.897 | 0.723 | 0.462 | 0.346 |
| 0.65 | 0.686 | 0.960 | 0.712 | 0.895 | 0.707 | 0.192 | 0.192 |
| 0.7 | 0.543 | 0.950 | 0.647 | 0.902 | 0.628 | 0.154 | 0.058 |
| 0.74 | 0.486 | 0.944 | 0.596 | 0.979 | 0.576 | 0.115 | 0.038 |

## Recommended operating point

- **fold-NN tau* = 0.65** (lowest grid threshold with external off-distribution false-accept rate <= 0.2).
- Off-M-CSA recovery 0.712 at precision 0.895.
- Rejection: external non-M-CSA false-accept 0.192; M-CSA OOS false-accept 0.192; in-scope retention 0.714.
- Off-M-CSA recovery by family at tau*:
    - flavin_dehydrogenase_reductase: 82/96 (0.854)
    - metal_dependent_hydrolase: 7/34 (0.206)
    - heme_peroxidase_oxidase: 16/20 (0.800)
    - plp_dependent_enzyme: 6/6 (1.000)

- Alternative (high precision): tau = 0.74 (maximises off-M-CSA precision on retained).

## Family robustness of the global threshold (the key engineering finding)

- a family survives the global threshold if recovery at tau* retains >= 50% of its no-abstention recovery.

| family | n | recovery (tau=0) | recovery (tau*) | survives |
| --- | --- | --- | --- | --- |
| flavin_dehydrogenase_reductase | 96 | 0.865 | 0.854 | yes |
| metal_dependent_hydrolase | 34 | 0.765 | 0.206 | NO -- collapses |
| heme_peroxidase_oxidase | 20 | 0.850 | 0.800 | yes |
| plp_dependent_enzyme | 6 | 1.000 | 1.000 | yes |

- **Implication:** A single global fold threshold is family-dependent: metal_dependent_hydrolase each lose >50% of recall at tau*=0.65 because their true within-family fold-NN scores run lower than the flavin/heme/PLP families. A per-family threshold (or a family-aware calibration) is the bounded next step before a uniform tau* deploys.

## Serving contract (the deployable decision rule)

- input: protein sequence
- 1. predict structure (AlphaFold / equivalent) -> 3D coordinates
- 2. foldseek query vs the M-CSA fold atlas -> top-1 hit (target accession, target fingerprint_id, alntmscore s)
- 3. if s >= tau* (0.65): emit (mechanism = target fingerprint_id, confidence = s)
-    else: ABSTAIN (out-of-scope / novel mechanism)
- Abstain below tau*: the channel is a high-precision retriever with a calibrated open-set reject, not a forced classifier.

## Verification

- recompute_matches_published_mcsa_curve: True
- recompute_matches_published_offmcsa_curve: True
- recomputed_inscope_retention_matches_frontier: True

## Caveats

- Development-surface recommendation, NOT a validated deployment claim: tau* is selected on calibration + bronze + external-negative surfaces.
- Off-M-CSA recovery uses bronze (automation-curated) labels -- it measures fold/sequence concordance, not gold accuracy (non-circular for fold: bronze admission used sequence/cofactor, not structure).
- Coverage is the 4 cofactor atlas families; broader-family behaviour is not measured here.
- n is small (35 M-CSA + 156 off-M-CSA positives; 26 OOS + 52 external negatives); the curve is an estimate, not a precise operating guarantee.

## Required before deployment

- A NEW pre-registered held-out (ideally including non-M-CSA gold rows) that validates tau* once, after it is frozen -- per the standing discipline that every operating-point change needs a fresh unbiased test.
- A gold-labelled off-M-CSA recovery check to replace the bronze concordance estimate.

## Guardrails

- Development-surface synthesis; no held-out read, no training, no registry or production-threshold change. Recovery is recomputed from published per-row scores and verified to reproduce both readouts' curves.
