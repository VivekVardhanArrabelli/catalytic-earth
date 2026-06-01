# Mechanism-Feature Embedding Feature Contract Strict Audit - current702

Run: 2026-06-01T14:01:09Z

Strict no-fit audit for the mechanism-feature embedding feature contract. It validates row alignment, split discipline, forbidden label/outcome field exclusion, and no-model-fit guardrails.

## Status

- mechanism_feature_embedding_feature_contract_strict_audit_passed_no_model_fit
- Feature rows: 524
- Split manifest rows: 524
- Row audits passed: 524
- Row audits blocked: 0
- Train rows: 418
- Calibration rows: 106
- Heldout excluded rows: 140
- Critical violation total: 0
- Critical counts: {}

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-mechanism-feature-embedding-feature-contract
```

## Interpretation

- 524/524 feature rows pass strict label-exclusion and train/cal alignment checks; no model was fit.
- Keep model fitting blocked until explicitly authorized; a future materializer must consume only the audited feature groups, fit on train rows, select on calibration rows, and evaluate heldout once.
