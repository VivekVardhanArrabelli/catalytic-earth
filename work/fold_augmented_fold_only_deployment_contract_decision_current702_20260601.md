# Fold-Augmented Fold-Only Deployment Contract Decision - current702

Run: 2026-06-02T08:14:11Z

Decision audit for the Lever 3 fold-only escape hatch. It copies the existing OOS-calibrated fold-only operating point and evaluates only the blocker rows that already have Foldseek/TM evidence; it does not select or tune thresholds.

## Status

- fold_only_deployment_contract_no_go_fixed_threshold_insufficient
- Fold-only deployment contract authorized: False
- Fold-only blocker rows: 4
- Rows abstained at 90% threshold: 0
- Heldout confounded abstain recall at 90% threshold: 0.3333
- Heldout in-scope retain recall at 90% threshold: 0.9574
- Critical violations: 5

## Rows At 90% Threshold

| row | TM score | threshold | abstains | nearest train |
| --- | ---: | ---: | --- | --- |
| m_csa:204 | 0.5651 | 0.4325 | False | m_csa:337 |
| m_csa:531 | 0.611 | 0.4325 | False | m_csa:862 |
| uniprot:P78549 | 0.4411 | 0.4325 | False | m_csa:83 |
| uniprot:Q3LXA3 | 0.6028 | 0.4325 | False | m_csa:518 |

## Decision

- Do not use a fold-only escape hatch for production-like closure at the fixed operating point. Clear the geometry/source blockers for m_csa:204, m_csa:531, uniprot:P78549, and uniprot:Q3LXA3, and resolve the missing AlphaFoldDB coordinate for m_csa:78.

## Interpretation

- The explicit fold-only contract is a no-go at the fixed 90% operating point: 0/4 fold-only blocker rows abstain and the heldout fold-only confounded abstain recall is 0.3333.
- Continue Lever 3 by clearing source-geometry or coordinate blockers rather than defining a separate fold-only deployment contract.
