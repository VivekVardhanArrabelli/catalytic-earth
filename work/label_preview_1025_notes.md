# 1025 Label-Factory Notes

The 1,025 preview was opened from the accepted 1,000 state, but it is not
promotable. `artifacts/v3_label_factory_gate_check_1025_preview.json` passes
21/21 factory gates, yet
`artifacts/v3_label_batch_acceptance_check_1025_preview.json` records
`accepted_for_counting=false` because the preview adds 0 clean countable labels.
The canonical registry remains at 679 countable labels.

The preview adds three new review-debt rows: `m_csa:1003`, `m_csa:1004`, and
`m_csa:1005`. `artifacts/v3_review_debt_summary_1025_preview.json` and
`artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json` keep all
329 review-state rows non-countable with 0 accepted-review overlap and 0
countable label candidates. The clean guardrails remain intact: 0 hard
negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable
in-scope failures, and 0 accepted review-gap labels.

The preview also exposed a source-scale limit. The 1,025 graph request returned
1,003 M-CSA records, leaving a 22-entry source gap for an M-CSA-only 1,025
tranche and a 9,321-label gap to the 10,000-label public target.
`artifacts/v3_source_scale_limit_audit_1025.json` therefore recommends stopping
M-CSA-only tranche growth and scoping external-source transfer before the next
count-growth attempt.

External-source transfer remains review-only. The new artifacts
`artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`, and
`artifacts/v3_external_source_candidate_sample_audit_1025.json` define a
bounded UniProtKB/Swiss-Prot transfer path, draft six ontology-pressure query
lanes, fetch a 30-row read-only candidate sample, and verify that every row is
non-countable. These artifacts are discovery-facing scaffolds only; they do not
create benchmark labels.

Next bounded work: implement the external-source transfer path as a gated,
review-only candidate manifest with OOD calibration and sequence-similarity
failure controls before any countable external labels can be imported.
