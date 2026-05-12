# 850 Label-Factory Notes

## Accepted Labels

The 850-entry gated pass accepted three clean automation-curated bronze labels:
`m_csa:837`, `m_csa:839`, and `m_csa:852`.

`artifacts/v3_label_batch_acceptance_check_850.json` records the batch as
accepted for counting. The canonical registry moved from 649 to 652 labels
with 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0
actionable in-scope failures, 0 accepted review-gap labels, and 0 accepted
reaction/substrate mismatch labels.

## Deferred Review Debt

The 850 preview raises review-state debt from 181 to 203 rows. The 22 new
review-debt rows are `m_csa:828`, `m_csa:829`, `m_csa:830`, `m_csa:831`,
`m_csa:832`, `m_csa:833`, `m_csa:834`, `m_csa:835`, `m_csa:836`, `m_csa:838`,
`m_csa:840`, `m_csa:841`, `m_csa:842`, `m_csa:843`, `m_csa:844`, `m_csa:845`,
`m_csa:846`, `m_csa:847`, `m_csa:848`, `m_csa:849`, `m_csa:850`, and
`m_csa:851`.

`artifacts/v3_accepted_review_debt_deferral_audit_850.json` explicitly keeps
all 203 review-state rows non-countable, with 0 accepted-label overlap and 0
countable label candidates. `m_csa:836` is the current regression row: a
role-inferred metal-hydrolase candidate without local ligand support is
deferred as `needs_more_evidence` rather than accepted.

## Gate State

`artifacts/v3_label_factory_gate_check_850.json` passes all 20 gates. The
post-850 queue retains all 198 expert-label decision rows, the mismatch export
covers all 29 family-guardrail reaction/substrate mismatch lanes, the
nine-family ATP/phosphoryl-transfer expansion remains guardrail-clean with 0
countable candidates, and review-only import safety prevents mismatch,
expert-decision, and local-evidence review artifacts from adding labels.

Next bounded work is a gated 875 preview only while these 850 gates remain
clean.
