# 750 Label-Factory Preview Notes

## Preview Countable Candidates

The 750-entry preview generated seven clean automation-curated bronze candidates
without promoting them into the canonical registry:

- `m_csa:728`
- `m_csa:733`
- `m_csa:735`
- `m_csa:739`
- `m_csa:740`
- `m_csa:742`
- `m_csa:750`

`artifacts/v3_label_batch_acceptance_check_750_preview.json` records the
preview as mechanically acceptable with 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and 0
accepted review-gap labels. If promoted later, the countable registry would
move from 630 to 637 labels.

## Review Debt

The 750 preview raises review-state debt from 100 to 118 rows. The 18 new
review-debt rows are `m_csa:729`, `m_csa:730`, `m_csa:731`, `m_csa:732`,
`m_csa:734`, `m_csa:736`, `m_csa:737`, `m_csa:738`, `m_csa:741`, `m_csa:743`,
`m_csa:744`, `m_csa:745`, `m_csa:746`, `m_csa:747`, `m_csa:748`,
`m_csa:749`, `m_csa:751`, and `m_csa:752`.

`artifacts/v3_label_scaling_quality_audit_750_preview.json` classifies all
new-debt rows and recommends `review_before_promoting`. The dominant failure
classes are ontology scope pressure, cofactor-family ambiguity,
family-propagation boundaries, reaction/substrate mismatch, active-site mapping
gaps, and multi-domain or mixed-evidence rows.

## Current Gate State

`artifacts/v3_label_factory_gate_check_750_preview.json` passes 19/19 preview
gates after retaining all 120 expert-label decision rows in the repair-candidate
table. This is a preview gate only. Do not copy
`artifacts/v3_countable_labels_batch_750_preview.json` into
`data/registries/curated_mechanism_labels.json` until the 18 new review-debt
rows are repaired or explicitly deferred and the promotion decision is
documented.
