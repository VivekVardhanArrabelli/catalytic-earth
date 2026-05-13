# 975 Label-Factory Notes

## Accepted Labels

The 975-entry gated pass accepted two clean automation-curated bronze labels
after the accepted 950 state: `m_csa:956` and `m_csa:973`.

`artifacts/v3_label_batch_acceptance_check_975.json` records the batch as
accepted for counting. The canonical registry moved from 673 to 675 labels,
with 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions,
0 actionable in-scope failures, 0 accepted review-gap labels, and 0 accepted
reaction/substrate mismatch labels.

## Deferred Review Debt

The accepted 975 state has 305 review-state rows. The 23 new 975-preview
review-debt rows are classified in
`artifacts/v3_label_scaling_quality_audit_975_preview.json`, and
`artifacts/v3_accepted_review_debt_deferral_audit_975.json` keeps all 305
review-state rows non-countable with 0 accepted-label overlap and 0 countable
label candidates.

## Gate State

`artifacts/v3_label_factory_gate_check_975.json` passes all 21 gates. The
post-975 queue retains all 300 active expert-label decision lanes after a
queue-retention repair raised the active-learning cap; the mismatch export
covers all 30 family-guardrail reaction/substrate mismatch lanes, the
nine-family ATP/phosphoryl-transfer expansion remains guardrail-clean with
0 countable candidates, and review-only import safety prevents mismatch,
expert-decision, and local-evidence review artifacts from adding labels.

Next bounded work is a gated 1,000-entry preview only while these 975 gates
remain clean.
