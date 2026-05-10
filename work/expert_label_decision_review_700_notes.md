# 700 Expert-Label Decision Review Export

## Summary

The accepted 700 state still has 76 active-queue rows with
`recommended_action: expert_label_decision_needed`. These are now routed through
`artifacts/v3_expert_label_decision_review_export_700.json` instead of leaving
them as generic review debt.

The export is review-only:

- 76 rows exported.
- 76 `no_decision` decisions in
  `artifacts/v3_expert_label_decision_decision_batch_700.json`.
- 0 countable label candidates.
- 0 missing entries from the export.
- 7 reaction/substrate mismatch lanes are already covered by
  `artifacts/v3_reaction_substrate_mismatch_review_export_700.json`.
- `artifacts/v3_expert_label_decision_repair_candidates_700.json` ranks the
  first 30 non-countable repair candidates and keeps the full 76-row bucket
  counts.

The refreshed 700 label-factory gate now has 14 checks. The
`expert_label_decision_review_export_ready` check passes only when every active
`expert_label_decision_needed` row is present in the dedicated export, all rows
remain `no_decision`, and the export reports 0 countable candidates. The paired
`expert_label_decision_repair_candidates_ready` check requires the repair
summary to cover the same 76 rows with 0 countable candidates.

## Risk Profile

The review-only export records these quality-risk flags across the 76 rows:

- `external_expert_decision_required`: 76
- `cofactor_family_ambiguity`: 50
- `counterevidence_boundary`: 29
- `active_site_mapping_or_structure_gap`: 14
- `text_leakage_or_nonlocal_evidence_risk`: 9
- `reaction_substrate_mismatch`: 7
- `substrate_class_boundary`: 7
- `sibling_mechanism_confusion`: 6
- `ser_his_metal_boundary`: 2

These flags are audit context only. They do not accept, reject, or count labels.
The 700 scaling-quality audit now carries this profile as an explicit
`expert_label_decision_review_only_debt` failure-mode surface.

## Countable Label Policy

Do not import this export into the countable benchmark as an automation decision
batch. It exists to prove that the active-queue expert-decision lane is complete
and non-countable until external expert review supplies a real resolution.

## Repair Leads

The first non-countable repair lane should focus on evidence quality rather than
expert judgment. Candidate subsets:

- Active-site mapping or structure gaps: `m_csa:553`, `m_csa:654`,
  `m_csa:662`, `m_csa:659`, `m_csa:691`, `m_csa:698`, `m_csa:701`,
  `m_csa:667`, `m_csa:692`, `m_csa:677`, `m_csa:664`, `m_csa:592`,
  `m_csa:690`, and `m_csa:567`.
- Text-leakage or nonlocal-evidence risks: `m_csa:553`, `m_csa:643`,
  `m_csa:510`, `m_csa:641`, `m_csa:577`, `m_csa:592`, `m_csa:578`,
  `m_csa:657`, and `m_csa:572`.
- Ser-His/metal-boundary regression rows: `m_csa:529` and `m_csa:650`.

For the next run, prefer a repair artifact that starts with the active-site
mapping/structure-gap subset and records why each row remains non-countable
after any structure or cofactor evidence is inspected.

The repair-candidate summary currently buckets all 76 rows as 14
`active_site_mapping_or_structure_gap_repair`, 7
`text_leakage_or_nonlocal_evidence_guardrail`, 30 `cofactor_evidence_repair`,
1 `ser_his_metal_boundary_review`, 1 `sibling_mechanism_boundary_review`, and
23 `external_expert_label_decision`. It links remediation context for all 76
rows, structure-mapping context for 3 rows, and alternate-structure scan context
for 42 rows; the emitted top 30 rows are prioritization only, while metadata
retains all 76 candidate entry IDs for gate and audit checks. The companion
`artifacts/v3_expert_label_decision_repair_candidates_700_all.json` file emits
all 76 rows for full-table review.
