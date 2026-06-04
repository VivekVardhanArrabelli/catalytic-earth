# Fold-Augmented Lever 3 Operating-Point Deployment Readout - current702

Run: 2026-06-04T23:09:39Z

Lever 3 measured operating-point deployment readout. It composes the accepted cofactor-context counteraxis, accepted same-family bandpass counteraxis contract, post-bandpass deployment readout, and exact P07658 route attempts. It confirms the train/cal hard-confounded residual separation at fixed threshold 0.44155 and separately reports whether the remaining P07658 predicted-coordinate provenance gate is closed.

## Status

- fold_augmented_lever3_operating_point_deployment_readout_ready_p07658_gap
- Deployment-valid operating-point readout available: True
- Hard-confounded residuals closed at operating point: True
- P07658 coordinate gap cleared now: False
- Current evidence sufficient for deployment closure: False

## Operating Point

- Route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_counteraxis_contract
- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- Retention floor met: True

## Confounded Axes

- Strict high-cofactor proxy abstained: 1/4
- Strict same-family proxy abstained: 26/59
- Residual high-cofactor rows resolved: 1/1
- Same-family shortfall before/after contract: 9/0

## P07658

- Exact routes attempted: 6
- Coordinates returned: 0
- Deployment-valid predicted-coordinate rows: 0
- Exact sequence submitted routes: 5

## Decision

- Fixed-threshold audit ready to rerun now: False
- Remaining missing evidence: ['accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun', 'credentialed or local exact full-length P07658 predicted coordinate with provider/model/version/path/checksum and U140 provenance']
- Smallest next experiment: Provision a credentialed or local full-length predictor route that accepts the frozen 715-residue P07658 sequence with U140 preserved or explicitly documented, then rerun acceptance preflight before any fixed-threshold scoring.
- Next gate: Rerun fixed-threshold surface only after P07658 acceptance preflight passes with accepted coordinate/provenance.

## Guardrails

- Measured readout only. No labels, registries, ontologies, imports, thresholds, heldout tuning, scoring, or coordinate staging changed.
- Critical violations: 0

## Interpretation

- Lever 3 has a measured fixed-threshold operating point for hard-confounded train/cal routing, but deployment closure still needs P07658 provenance.
- Retains 31/34 calibration in-scope rows and abstains 105/204 train/cal OOS rows; residual hard confounded closure is True.
- P07658 exact route attempts returned 0 coordinates and 0 deployment-valid predicted-coordinate rows.
- Stop route-equivalent no-credential retries; use a credentialed or local exact full-length predictor route, then rerun P07658 acceptance preflight before any scoring rerun.
