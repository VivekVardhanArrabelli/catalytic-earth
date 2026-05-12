# 775 Label-Factory Notes

## Accepted Countable Labels

The 775-entry gated pass accepted five clean automation-curated bronze labels
into the canonical registry:

- `m_csa:754`
- `m_csa:758`
- `m_csa:759`
- `m_csa:762`
- `m_csa:776`

`artifacts/v3_label_batch_acceptance_check_775.json` records the batch as
accepted for counting with 0 hard negatives, 0 near misses, 0 out-of-scope
false non-abstentions, 0 actionable in-scope failures, and 0 accepted
review-gap labels. The countable registry moved from 637 to 642 labels.

## Review Debt

The 775 preview raises review-state debt from 118 to 138 rows. The 20 new
review-debt rows are `m_csa:753`, `m_csa:755`, `m_csa:756`, `m_csa:757`,
`m_csa:760`, `m_csa:761`, `m_csa:763`, `m_csa:764`, `m_csa:765`,
`m_csa:766`, `m_csa:767`, `m_csa:768`, `m_csa:769`, `m_csa:770`,
`m_csa:771`, `m_csa:772`, `m_csa:773`, `m_csa:774`, `m_csa:775`, and
`m_csa:777`.

`artifacts/v3_label_scaling_quality_audit_775_preview.json` classifies all
new-debt rows. `m_csa:771` is deliberately deferred as
`mark_needs_more_evidence` because its Ser-His hydrolase text is paired with
counterevidence (`ser_his_seed_missing_triad_coherence`); the provisional
labeler now treats that pattern as a text-leakage risk rather than a clean
countable label. `artifacts/v3_accepted_review_debt_deferral_audit_775.json`
explicitly defers all 138 review-state rows, including those 20 new rows, with
0 countable candidates and 0 accepted-label overlap.

## Current Gate State

`artifacts/v3_label_factory_gate_check_775.json` passes all 20 gates after
retaining 133 post-batch expert-label decision rows in the repair-candidate
table, 38 local-evidence gap rows in review-only export artifacts, and the
nine ATP/phosphoryl-transfer fingerprint families as first-class boundary
controls. Do not open 800 unless this gate and the 775 deferral audit remain
clean.
