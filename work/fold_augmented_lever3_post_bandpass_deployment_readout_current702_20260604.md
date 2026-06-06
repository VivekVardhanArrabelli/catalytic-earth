# Fold-Augmented Lever 3 Post-Bandpass Deployment Readout - current702

Run: 2026-06-04T21:15:57Z

Lever 3 post-bandpass deployment readout. It composes the accepted cofactor-context high-cofactor counteraxis, the accepted same-family numeric bandpass counteraxis contract, and the P07658 prediction acceptance/dispatch evidence to state whether the fixed-threshold surface can be rerun. It scores no rows, stages no coordinates, and changes no thresholds.

## Status

- fold_augmented_lever3_post_bandpass_deployment_readout_blocked_p07658
- Counteraxis contracts ready: True
- P07658 acceptance passes now: False
- Current evidence sufficient for deployment closure: False

## Operating Point

- Route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_counteraxis_contract
- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- Strict high-cofactor abstained: 1/4
- Strict same-family abstained: 26/59

## P07658 Acceptance

- Status: fold_augmented_p07658_prediction_acceptance_preflight_blocked
- Acceptance checks passed/failed: 1/7
- Candidate coordinate/provenance exists: 0/0
- Provider routes returning coordinate now: 0/6

## Decision

- Fixed-threshold audit ready to rerun now: False
- Remaining missing evidence: ['accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun']
- Next gate: Counteraxis contracts are ready; obtain accepted P07658 full-length predicted-coordinate provenance before rerun.

## Interpretation

- Lever 3 counteraxis contracts are ready; deployment closure still waits on P07658.
- The accepted operating point retains 31/34 calibration in-scope rows and abstains 105/204 train/cal OOS rows; P07658 acceptance still has 7 failed checks.
- Provision or run one approved exact full-length P07658 prediction route and fill coordinate/provenance before rerun.
