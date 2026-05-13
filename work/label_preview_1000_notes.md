# 1000 Label-Factory Notes

The 1,000-entry gated pass accepted four clean automation-curated bronze labels:
`m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`.
`artifacts/v3_label_batch_acceptance_check_1000.json` records the batch as
accepted for counting. The canonical registry moved from 675 to 679 labels.

The 1,000 preview initially exposed `m_csa:986` as a low-score heme boundary
negative with local heme support. The provisional decision rule now defers
below-threshold cofactor-sensitive rows when local ligand evidence and
mechanism text match the top family, so `m_csa:986` remains review-state and is
not counted as a clean out-of-scope negative.

The accepted 1,000 state has 326 review-state rows. The 21 new preview
review-debt rows are classified by
`artifacts/v3_label_scaling_quality_audit_1000_preview.json`, and
`artifacts/v3_accepted_review_debt_deferral_audit_1000.json` keeps all 326
review-state rows non-countable with 0 accepted-label overlap and 0 countable
label candidates.

`artifacts/v3_label_factory_gate_check_1000.json` passes all 21 gates. The
post-1,000 queue retains all 321 active expert-label decision lanes, the
review-only import safety audit still adds 0 countable labels, and the batch
summary reports 21/21 accepted batches with 679 countable labels.

Next bounded work is a gated 1,025-entry preview only while these 1,000 gates
remain clean. Stop count growth if hard negatives, false non-abstentions,
actionable in-scope failures, accepted review debt, ontology/family-boundary
drift, or queue truncation appear.
