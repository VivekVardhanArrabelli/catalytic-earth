# Gate 1: Router Reconciliation Diagnostic

Run: 2026-06-28T22:17:34Z
Status: `fine_router_drift_includes_genuine_misrouting_not_just_relabeling`

## Question

- Is the current-57 fine router's drift from the validated June 9 router pure taxonomy-version relabeling (cheap to reconcile), or does it include genuine misrouting (a real fix)?

## Calibration Classification (in-scope, threshold 0.4115)

- Exact correct: 13/35.
- Documented-compatible (v2 split, relabeling): 13.
- Incompatible misroute (genuine error): 8.
- Below threshold (abstain): 1.

## Recovery Comparison

- current-57 exact: 13/35.
- current-57 documented-compatible (relabeling ceiling): 26/35.
- June 9 reference: 30/35.
- Reconcilable by documented relabeling alone: False.
- Recovery gap beyond relabeling: 4.

## Drift Mechanism

- The fine-57 metal v2-subclass fingerprints over-claim non-metal (flavin / heme / PLP) enzymes in the fused geometry router; the coarse June 9 router has no metal subclasses and so does not misroute them.
- Non-metal enzymes misrouted into metal subclasses: 7.
- Misroutes:
  - 2x  plp_dependent_enzyme -> metallophosphomonoesterase
  - 1x  flavin_dehydrogenase_reductase -> alpha_beta_hydrolase_esterase_lipase
  - 1x  heme_peroxidase_oxidase -> metallophosphoesterase_nuclease
  - 1x  flavin_dehydrogenase_reductase -> metallophosphoesterase_nuclease
  - 1x  plp_dependent_enzyme -> metallophosphoesterase_nuclease
  - 1x  heme_peroxidase_oxidase -> metallopeptidase
  - 1x  heme_peroxidase_oxidase -> metallo_amidohydrolase_deaminase

## Fork

- **Option A (June 9 coarse router):** validated_baseline_heldout_passed — held-out one-shot PASS: 35/47 recovery, 15/79 OOS FP; coarse (~8 families); no metal subclass distinctions; effort none (deployable now).
- **Option B (repair fine-57):** requires_real_router_fix_then_new_preregistration; root cause: metal v2-subclass fingerprints over-claim non-metal enzymes in the fused geometry router; work: constrain/recalibrate the metal subclass fingerprints so they stop claiming flavin/heme/PLP enzymes, re-verify recovery on calibration, then a NEW pre-registration against a NEW held-out (the M-CSA held-out is spent).

## Recommendation

- Adopt Option A (June 9 coarse router) as the deployable validated baseline now: documented relabeling only reaches 26/35 (< June 9 30/35), because 8 calibration rows are genuine misroutes, not taxonomy splits. Pursue Option B as a scoped follow-up with the identified root cause (metal-subclass over-claiming) only if fine-grained metal subclass calls are required in production.

## Guardrails

- Calibration (development) only; the spent held-out one-shot was not touched.
- No registry, ontology, label, threshold, or model change.
