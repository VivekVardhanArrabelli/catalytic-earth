# 950 Label-Factory Notes

## Accepted Labels

The 875-, 900-, 925-, and 950-entry gated passes accepted 21 clean
automation-curated bronze labels after the accepted 850 state:

- 875: `m_csa:853`, `m_csa:854`, `m_csa:855`, `m_csa:856`, `m_csa:860`,
  `m_csa:862`, and `m_csa:866`
- 900: `m_csa:879`, `m_csa:895`, `m_csa:900`, and `m_csa:901`
- 925: `m_csa:903`, `m_csa:912`, `m_csa:916`, and `m_csa:922`
- 950: `m_csa:933`, `m_csa:935`, `m_csa:937`, `m_csa:941`, `m_csa:942`,
  and `m_csa:944`

`artifacts/v3_label_batch_acceptance_check_950.json` records the latest batch
as accepted for counting. The canonical registry moved from 652 to 673 labels
across these four bounded batches, with 0 hard negatives, 0 near misses,
0 out-of-scope false non-abstentions, 0 actionable in-scope failures,
0 accepted review-gap labels, and 0 accepted reaction/substrate mismatch
labels.

## Deferred Review Debt

The 950 accepted state has 282 review-state rows. The 19 new 950-preview
review-debt rows are explicitly classified in
`artifacts/v3_label_scaling_quality_audit_950_preview.json`, and
`artifacts/v3_accepted_review_debt_deferral_audit_950.json` keeps all 282
review-state rows non-countable with 0 accepted-label overlap and 0 countable
label candidates.

## Gate State

`artifacts/v3_label_factory_gate_check_950.json` passes all 21 gates. The
post-950 queue retains all active expert-label decision lanes, the mismatch
export covers all 30 family-guardrail reaction/substrate mismatch lanes, the
nine-family ATP/phosphoryl-transfer expansion remains guardrail-clean with
0 countable candidates, and review-only import safety prevents mismatch,
expert-decision, and local-evidence review artifacts from adding labels.

Next bounded work is a gated 975 preview only while these 950 gates remain
clean.
