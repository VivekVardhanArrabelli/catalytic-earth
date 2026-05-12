# 725 Label-Factory Notes

## Accepted Countable Labels

The 725-entry gated pass accepted six additional automation-curated bronze
labels for counting:

- `m_csa:705` (`rhamnogalacturonan acetylesterase`) as
  `ser_his_acid_hydrolase`.
- `m_csa:709` (`cytochrome-c peroxidase (mono-heme type)`) as
  `heme_peroxidase_oxidase`.
- `m_csa:714` (`ubiquinol oxidase (H+-transporting)`) as
  `heme_peroxidase_oxidase`.
- `m_csa:716` (`nicotinamidase`) as `metal_dependent_hydrolase`.
- `m_csa:723` (`subtilisin`) as `ser_his_acid_hydrolase`.
- `m_csa:727` (`phosphoserine phosphatase`) as
  `metal_dependent_hydrolase`.

`artifacts/v3_label_batch_acceptance_check_725.json` records these six labels
as accepted for counting and confirms 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, 0 accepted
review-gap labels, and 0 accepted reaction/substrate mismatch labels. The
countable registry now has 630 labels.

## Review Debt

The 725 review-state pass leaves 100 `needs_more_evidence` rows outside the
countable benchmark: 76 carried from the accepted-700 state plus 24 new rows.
The new-debt next actions are 12 alternate-structure or cofactor-source
inspections, 6 expert family-boundary reviews, 5 expert-review decisions, and
1 local cofactor or active-site mapping check.

The 725 scaling-quality audit classifies all 24 new review-debt rows before
promotion. Accepted clean labels have 0 review debt, the sequence-cluster proxy
has no missing assignments, and the audit records 0 near-duplicate hits among
audited rows. The review-only warnings remain active for deferred rows:
active-learning queue concentration, ontology scope pressure, family
propagation boundaries, cofactor ambiguity, reaction/substrate mismatch,
active-site mapping gaps, structure-mapping issues, expert-label decision
review-only rows, and local-evidence gaps.

## Repair Leads

`artifacts/v3_review_debt_alternate_structure_scan_725_preview.json` scanned 12
new-debt candidates across 140 structures with 0 fetch failures. Expected
family hits were found for `m_csa:712`, `m_csa:718`, and `m_csa:724`, but only
`m_csa:712` had local support from a conservative residue-position remap.
`artifacts/v3_review_debt_remap_local_lead_audit_725_preview.json` routes
`m_csa:712` to expert family-boundary review and keeps it non-countable under a
strict remap guardrail. The structure-wide-only hits for `m_csa:718` and
`m_csa:724` remain review debt.

`artifacts/v3_expert_label_decision_local_evidence_gap_audit_725.json`,
`artifacts/v3_expert_label_decision_local_evidence_review_export_725.json`, and
`artifacts/v3_expert_label_decision_local_evidence_repair_plan_725.json` keep
25 priority repair lanes review-only with 0 countable candidates.
`artifacts/v3_explicit_alternate_residue_position_requests_725.json` exports 8
explicit alternate residue-position requests across 73 candidate alternate
structures and also keeps `countable_label_candidate_count=0`.

## Next Review Focus

Do not count the 100 review-state rows unless a later evidence pass removes
their gap reasons and the label-factory gate passes. The highest-value next
bounded work is to repair or explicitly defer the accepted-725 local-evidence
gap lanes, starting with the strict remap-local lead `m_csa:712`, then decide
whether the gate is clean enough to open the 750 tranche.
