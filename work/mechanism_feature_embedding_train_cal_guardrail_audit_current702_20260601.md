# Mechanism-Feature Embedding Train/Cal Guardrail Audit

## Summary

This no-fit audit checks the existing mechanism-feature embedding input
manifest, train/cal split manifest, and feature contract for split consistency
and leakage guardrails. It passes: 524 feature rows exactly match the 524
train/cal split rows, with 418 train rows and 106 calibration rows.

## Findings

- 140 heldout rows remain excluded from feature rows.
- 38 input rows are not split-ready, all explained by role-graph readiness
  reasons.
- No feature row carries heldout status.
- Fingerprint ID, label type, and stratum remain excluded as features.
- No model fitting, threshold selection, import, label change, or production
  scoring occurred.

## Next Action

If a model-fit pilot is explicitly authorized later, fit only on the 418 train
rows, select any operating point only on the 106 calibration rows, and evaluate
heldout once.
