# Mechanism Feature Row-Specific Bond-Change Feature Contract Gap Audit - current702

Run: 2026-06-01T17:13:08Z

Validation-only audit that the staged row-specific bond-change schema remains outside the no-fit mechanism-feature embedding contract until source evidence is materialized and explicitly authorized.

## Status

- row_specific_bond_change_gap_not_consumed_by_feature_contract
- Feature contract rows: 524
- Rows requiring row-specific bond-change evidence: 232
- Unexpected bond-change feature rows: 0
- Heldout feature rows: 0
- Strict audit critical violations: 0

## Interpretation

- The row-specific bond-change schema is staged as a future feature gap and is not currently consumed by the no-fit feature contract.
- Materialize and audit source-backed row-specific bond-change sidecars before regenerating the train/cal feature contract.
