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
`artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_1025.json`,
`artifacts/v3_external_source_failure_mode_audit_1025.json`,
`artifacts/v3_external_source_control_repair_plan_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
`artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
`artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
`artifacts/v3_external_source_transfer_gate_check_1025.json` define a bounded
UniProtKB/Swiss-Prot transfer path, draft six ontology-pressure query lanes,
fetch a 30-row read-only candidate sample, attach OOD and exact-reference
sequence controls, request active-site/mechanism/heuristic-control evidence,
carry sampled PDB/AlphaFold structure references into the evidence export, queue
25 review-only active-site evidence rows while deferring five rows, sample
UniProtKB active-site features, map all 12 heuristic-ready AlphaFold controls,
score the mapped controls with the current heuristic retrieval path, add a
bounded sequence-neighborhood screen and import-readiness audit, and pass the
60/60 external-transfer gate for review-only evidence collection with
sequence-search export, active-site sourcing export/resolution,
representation-backend planning/sample, a candidate blocker matrix, lineage-
checked pilot priority, and no-decision pilot review packets. The
active-site sourcing resolution finds 0 explicit active-site residue sources in
the 10 gap rows, the deterministic k-mer baseline flags one representation
near-duplicate holdout, and the canonical ESM-2 representation sample flags
three representation near-duplicate holdouts while keeping all rows
non-countable.
Two sample accessions (`O15527` and `P42126`) overlap existing M-CSA reference
accessions and are routed to holdout controls. The lane-balance audit is clean:
six lanes each contribute five candidates, so the initial review sample has not
collapsed to one chemistry. These artifacts are
discovery-facing scaffolds only; they do not create benchmark labels.
`artifacts/v3_external_source_reaction_evidence_sample_1025.json` then fetches
Rhea reaction context for all 30 external candidates, yielding 64 reaction
records with 0 fetch failures; its guardrail audit is clean, and those rows
remain `reaction_context_only` and non-countable because they have not been
converted into a reviewed decision artifact or full label-factory gate. The
audit also flags 16 broad-EC context rows across `1.1.1.-`, `1.11.1.-`,
`1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-` as review-only
context, not specific mechanism evidence.
`artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json` finds
specific reaction context for all 3 broad-only repair rows, but those rows
remain non-countable and still need active-site evidence and a future decision
artifact.

Next bounded work: repair the external-source control findings before any label
import. The active-site feature sample leaves 10 feature-gap rows, now covered
by source requests; the expanded heuristic-control score sample collapses 9/12
mapped candidates to `metal_dependent_hydrolase` top1 with 9 scope/top1
mismatches; and the sequence-neighborhood plan still requires near-duplicate
search for 28 rows. The bounded sequence screen finds 0 high-similarity alerts
against 733 current countable M-CSA reference sequences but still requires
complete near-duplicate search before import. The bounded alignment check
verifies 90 top-hit pairs and confirms the 2 exact-reference holdouts while
remaining non-countable. The import-readiness audit keeps
0 rows import-ready and records 10 active-site gaps, 9 heuristic scope/top1
mismatches, and 29 representation-control issues. The active-site sourcing
queue prioritizes the 10 active-site gaps into 7 mapped-binding-context rows
and 3 primary-source rows. The active-site sourcing export carries 72 source
targets, the sequence-search export keeps all 30 rows as no-decision sequence
controls, and the transfer blocker matrix joins the rows into a non-countable
next-action worklist. The control-repair plan records 25 non-countable repair
rows, the representation comparison exposes 12 mapped controls for future
learned or structure-language comparison, the representation-backend plan keeps
those controls unembedded, and the binding-context mapping sample maps 7/7
active-site-gap rows as repair context only. These are review-only failure
modes, not countable labels.
