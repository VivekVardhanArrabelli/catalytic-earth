# June 9 Router + Fold-NN Fusion Readout

Run: 2026-06-28T12:24:19Z
Status: `june9_router_fold_gate_no_pareto_improvement_precision_recall_tradeoff_only`

## June 9 Baseline (fold gate off)

- Frozen threshold: cofactor 0.4115 + fold 0.0: recovery 30/35 · OOS FP 9/26.
- 0.44 dial: cofactor 0.44 + fold 0.0: recovery 30/35 · OOS FP 8/26.
- Exact recovery ceiling: 30/35.

## Fold Gate Assessment

- Rule: retained := fused.top1_score >= cofactor_threshold AND fold_nn_alntmscore >= fold_threshold (June 9 exact correctness).
- Fold gate Pareto-improves the dial baseline: False.
- Pareto-improving point: none.

### Precision/Recall Frontier (recovery -> min OOS FP)

- recovery 30/35 -> OOS FP 8/26 (cofactor 0.44, fold 0.0)
- recovery 29/35 -> OOS FP 7/26 (cofactor 0.44, fold 0.4376)
- recovery 28/35 -> OOS FP 6/26 (cofactor 0.44, fold 0.4673)
- recovery 27/35 -> OOS FP 5/26 (cofactor 0.569, fold 0.4376)
- recovery 26/35 -> OOS FP 5/26 (cofactor 0.5662, fold 0.4673)
- recovery 25/35 -> OOS FP 5/26 (cofactor 0.5662, fold 0.4701)
- recovery 24/35 -> OOS FP 5/26 (cofactor 0.4115, fold 0.55)
- recovery 23/35 -> OOS FP 1/26 (cofactor 0.4115, fold 0.65)
- recovery 22/35 -> OOS FP 1/26 (cofactor 0.4115, fold 0.663)
- recovery 21/35 -> OOS FP 1/26 (cofactor 0.4115, fold 0.6647)
- recovery 20/35 -> OOS FP 1/26 (cofactor 0.4115, fold 0.6782)
- recovery 19/35 -> OOS FP 1/26 (cofactor 0.4115, fold 0.6935)
- recovery 18/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.7399)
- recovery 17/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.74)
- recovery 16/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.7454)
- recovery 15/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.7789)
- recovery 14/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.7939)
- recovery 13/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.7959)
- recovery 12/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.8121)
- recovery 11/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.8402)
- recovery 10/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.8571)
- recovery 9/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.872)
- recovery 8/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.8819)
- recovery 7/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9089)
- recovery 6/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.914)
- recovery 5/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9167)
- recovery 4/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9184)
- recovery 3/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9261)
- recovery 2/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9623)
- recovery 1/35 -> OOS FP 0/26 (cofactor 0.4115, fold 0.9792)
- recovery 0/35 -> OOS FP 0/26 (cofactor 0.574, fold 0.9792)

### Residual OOS False Positives at the 0.44 dial

- m_csa:488: fold 0.7306, cofactor 0.5982 (called metal_dependent_hydrolase)
- m_csa:59: fold 0.6497, cofactor 0.5658 (called metal_dependent_hydrolase)
- m_csa:256: fold 0.6411, cofactor 0.5974 (called metal_dependent_hydrolase)
- m_csa:500: fold 0.6409, cofactor 0.5978 (called metal_dependent_hydrolase)
- m_csa:451: fold 0.6341, cofactor 0.589 (called metal_dependent_hydrolase)
- m_csa:312: fold 0.5451, cofactor 0.5977 (called metal_dependent_hydrolase)
- m_csa:253: fold 0.4654, cofactor 0.5662 (called metal_dependent_hydrolase)
- m_csa:398: fold 0.4343, cofactor 0.7359 (called flavin_dehydrogenase_reductase)

## Deployment Decision

- The deployable path remains the June 9 router at its dial operating point (30/35 recovery, 8/26 OOS FP). The fold-NN channel is a tunable precision/recall dial on this router (e.g., trading recovery for a near-zero-OOS-FP regime), not a free precision booster: its large marginal value was specific to rescuing the drifted current-57 router. Any chosen operating point still requires a single heldout-final read before deployment; no production threshold is changed here.

## Guardrails

- The live 57-fingerprint registry was never mutated; the June 9 surface is an isolated registry-pin row-detail reconstruction.
- Fold scores are calibration-vs-train only; no heldout row was scored or read.
- No threshold was selected on heldout rows; no supervised model was trained.
- No production threshold, model weight, registry, ontology, label, or fingerprint-family change was made.
