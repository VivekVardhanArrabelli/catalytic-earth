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
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
`artifacts/v3_external_source_transfer_gate_check_1025.json` define a bounded
UniProtKB/Swiss-Prot transfer path, draft six ontology-pressure query lanes,
fetch a 30-row read-only candidate sample, attach OOD and exact-reference
sequence controls, request active-site/mechanism/heuristic-control evidence,
carry sampled PDB/AlphaFold structure references into the evidence export, queue
25 review-only active-site evidence rows while deferring five rows, and pass the
11/11 external-transfer gate for review-only evidence collection.
Two sample accessions (`O15527` and `P42126`) overlap existing M-CSA reference
accessions and are routed to holdout controls. The lane-balance audit is clean:
six lanes each contribute five candidates, so the initial review sample has not
collapsed to one chemistry. These artifacts are
discovery-facing scaffolds only; they do not create benchmark labels.
`artifacts/v3_external_source_reaction_evidence_sample_1025.json` then fetches
Rhea reaction context for the first six external candidates, yielding 22
reaction records with 0 fetch failures; its guardrail audit is clean, and
those rows remain `reaction_context_only` and non-countable because no
active-site mapping or heuristic-control score exists. The audit also flags
three broad or incomplete EC queries (`1.1.1.-`, `1.11.1.-`, and `1.8.-.-`) as
review-only context, not specific mechanism evidence.

Next bounded work: collect or prototype the external-source active-site and
mechanism evidence requested by the active-site evidence queue, resolve
broad-only EC rows separately, then compare any resulting candidate evidence
against heuristic geometry retrieval as the required control before any
countable external labels can be imported.
