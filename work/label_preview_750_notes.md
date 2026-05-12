# 750 Label-Factory Notes

## Accepted Countable Labels

The 750-entry gated pass accepted seven clean automation-curated bronze labels
into the canonical registry:

- `m_csa:728`
- `m_csa:733`
- `m_csa:735`
- `m_csa:739`
- `m_csa:740`
- `m_csa:742`
- `m_csa:750`

`artifacts/v3_label_batch_acceptance_check_750.json` records the
batch as accepted for counting with 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and 0
accepted review-gap labels. The countable registry moved from 630 to 637
labels.

## Review Debt

The 750 preview raises review-state debt from 100 to 118 rows. The 18 new
review-debt rows are `m_csa:729`, `m_csa:730`, `m_csa:731`, `m_csa:732`,
`m_csa:734`, `m_csa:736`, `m_csa:737`, `m_csa:738`, `m_csa:741`, `m_csa:743`,
`m_csa:744`, `m_csa:745`, `m_csa:746`, `m_csa:747`, `m_csa:748`,
`m_csa:749`, `m_csa:751`, and `m_csa:752`.

`artifacts/v3_label_scaling_quality_audit_750_preview.json` classifies all
new-debt rows. `artifacts/v3_accepted_review_debt_deferral_audit_750.json`
explicitly defers all 118 review-state rows, including those 18 new rows, with
0 countable candidates and 0 accepted-label overlap. The dominant failure
classes remain ontology scope pressure, cofactor-family ambiguity,
family-propagation boundaries, reaction/substrate mismatch, active-site mapping
gaps, and multi-domain or mixed-evidence rows.

## Current Gate State

`artifacts/v3_label_factory_gate_check_750.json` passes 20/20 gates after
retaining all 113 post-batch expert-label decision rows in the repair-candidate
table. Do not open 775 unless this gate and the 750 deferral audit remain clean.
