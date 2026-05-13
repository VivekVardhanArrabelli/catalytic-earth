# Label Factory Work Notes

## Current Plan

The 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-, 725-, 750-, 775-,
800-, 825-, 850-, 875-, 900-, 925-, 950-, 975-, and 1000-slice label-factory batches
have been processed through countable import and acceptance checks. The
canonical registry has 679 countable labels. The bounded 1,025 preview is
cleanly non-promotable with 0 accepted labels; 329 rows remain
`needs_more_evidence` and are explicitly non-countable under the 1,025 preview
deferral audit. Next work should build the external-source transfer path rather
than opening another M-CSA-only tranche. The current external path is
review-only: candidate manifest, lane-balance audit, evidence plan/export,
active-site evidence queue, active-site feature sample, structure-control
mapping sample, heuristic-control score audit, failure-mode audit,
control-repair plan, representation-control manifest, binding-context repair
artifacts, sequence-holdout audit, 33/33 transfer gate, and full 30-candidate
Rhea reaction context all keep `countable_label_candidate_count=0`.

## Current Generated Artifacts

- `artifacts/v3_label_factory_audit_500.json`
- `artifacts/v3_label_factory_applied_labels_500.json`
- `artifacts/v3_adversarial_negative_controls_500.json`
- `artifacts/v3_active_learning_review_queue_500.json`
- `artifacts/v3_expert_review_export_500.json`
- `artifacts/v3_expert_review_import_preview_500.json`
- `artifacts/v3_family_propagation_guardrails_500.json`
- `artifacts/v3_label_factory_gate_check_500.json`
- `artifacts/v3_expert_review_decision_batch_500.json`
- `artifacts/v3_imported_labels_batch_500.json`
- `artifacts/v3_countable_labels_batch_500.json`
- `artifacts/v3_label_batch_acceptance_check_500.json`
- `artifacts/v3_expert_review_decision_batch_494.json`
- `artifacts/v3_label_review_resolution_check_500.json`
- `artifacts/v3_review_evidence_gaps_500.json`
- `artifacts/v3_label_batch_acceptance_check_525.json`
- `artifacts/v3_label_batch_acceptance_check_550.json`
- `artifacts/v3_imported_labels_batch_550.json`
- `artifacts/v3_countable_labels_batch_550.json`
- `artifacts/v3_label_factory_gate_check_550.json`
- `artifacts/v3_label_batch_acceptance_check_575.json`
- `artifacts/v3_label_batch_acceptance_check_600.json`
- `artifacts/v3_imported_labels_batch_600.json`
- `artifacts/v3_countable_labels_batch_600.json`
- `artifacts/v3_label_factory_gate_check_600.json`
- `artifacts/v3_label_batch_acceptance_check_625.json`
- `artifacts/v3_imported_labels_batch_625.json`
- `artifacts/v3_countable_labels_batch_625.json`
- `artifacts/v3_label_factory_gate_check_625.json`
- `artifacts/v3_label_batch_acceptance_check_650.json`
- `artifacts/v3_imported_labels_batch_650.json`
- `artifacts/v3_countable_labels_batch_650.json`
- `artifacts/v3_label_factory_gate_check_650.json`
- `artifacts/v3_label_factory_batch_summary.json`
- `artifacts/v3_label_batch_acceptance_check_675_preview.json`
- `artifacts/v3_imported_labels_batch_675_preview.json`
- `artifacts/v3_countable_labels_batch_675_preview.json`
- `artifacts/v3_label_factory_gate_check_675_preview_batch.json`
- `artifacts/v3_label_factory_preview_summary_675.json`
- `artifacts/v3_label_preview_promotion_readiness_675.json`
- `artifacts/v3_review_evidence_gaps_675_preview.json`
- `artifacts/v3_review_debt_summary_675_preview.json`
- `artifacts/v3_label_batch_acceptance_check_675.json`
- `artifacts/v3_label_batch_acceptance_check_700.json`
- `artifacts/v3_review_evidence_gaps_700.json`
- `artifacts/v3_review_debt_summary_700.json`
- `artifacts/v3_review_debt_remediation_700.json`
- `artifacts/v3_review_debt_remediation_700_all.json`
- `artifacts/v3_review_debt_alternate_structure_scan_700.json`
- `artifacts/v3_review_debt_remap_local_lead_audit_700.json`
- `artifacts/v3_reaction_substrate_mismatch_audit_700.json`
- `artifacts/v3_reaction_substrate_mismatch_review_export_700.json`
- `artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json`
- `artifacts/v3_expert_label_decision_review_export_700.json`
- `artifacts/v3_expert_label_decision_decision_batch_700.json`
- `artifacts/v3_expert_label_decision_repair_candidates_700.json`
- `artifacts/v3_expert_label_decision_repair_candidates_700_all.json`
- `artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json`
- `artifacts/v3_mechanism_ontology_gap_audit_700.json`
- `artifacts/v3_learned_retrieval_manifest_700.json`
- `artifacts/v3_sequence_similarity_failure_sets_700.json`
- `artifacts/v3_family_propagation_guardrails_700.json`
- `artifacts/v3_label_scaling_quality_audit_700_preview.json`
- `artifacts/v3_sequence_cluster_proxy_700.json`
- `artifacts/v3_label_batch_acceptance_check_850.json`
- `artifacts/v3_label_factory_gate_check_850.json`
- `artifacts/v3_accepted_review_debt_deferral_audit_850.json`
- `artifacts/v3_label_scaling_quality_audit_850_preview.json`
- `artifacts/v3_active_learning_review_queue_850.json`
- `artifacts/v3_reaction_substrate_mismatch_review_export_850.json`
- `artifacts/v3_expert_label_decision_review_export_850.json`
- `artifacts/v3_expert_label_decision_local_evidence_gap_audit_850.json`
- `artifacts/v3_mechanism_ontology_gap_audit_850.json`
- `artifacts/v3_learned_retrieval_manifest_850.json`
- `artifacts/v3_sequence_similarity_failure_sets_850.json`
- `artifacts/v3_label_batch_acceptance_check_950.json`
- `artifacts/v3_label_factory_gate_check_950.json`
- `artifacts/v3_accepted_review_debt_deferral_audit_950.json`
- `artifacts/v3_label_scaling_quality_audit_950_preview.json`
- `artifacts/v3_active_learning_review_queue_950.json`
- `artifacts/v3_reaction_substrate_mismatch_review_export_950.json`
- `artifacts/v3_expert_label_decision_review_export_950.json`
- `artifacts/v3_expert_label_decision_local_evidence_gap_audit_950.json`
- `artifacts/v3_mechanism_ontology_gap_audit_950.json`
- `artifacts/v3_learned_retrieval_manifest_950.json`
- `artifacts/v3_sequence_similarity_failure_sets_950.json`
- `artifacts/v3_label_batch_acceptance_check_975.json`
- `artifacts/v3_label_factory_gate_check_975.json`
- `artifacts/v3_accepted_review_debt_deferral_audit_975.json`
- `artifacts/v3_label_scaling_quality_audit_975_preview.json`
- `artifacts/v3_active_learning_review_queue_975.json`
- `artifacts/v3_reaction_substrate_mismatch_review_export_975.json`
- `artifacts/v3_expert_label_decision_review_export_975.json`
- `artifacts/v3_expert_label_decision_local_evidence_gap_audit_975.json`
- `artifacts/v3_mechanism_ontology_gap_audit_975.json`
- `artifacts/v3_learned_retrieval_manifest_975.json`
- `artifacts/v3_sequence_similarity_failure_sets_975.json`

Current export behavior: expert-review artifacts include top-ranked review rows
plus every unlabeled queue row, so label expansion cannot skip a lower-ranked
unlabeled candidate.

Current gate state: 21/21 factory checks pass on the 679-label countable
registry. The latest accepted batch-acceptance check passes: 4 additional
labels were accepted for counting in the 1000 batch (`m_csa:978`, `m_csa:988`,
`m_csa:990`, and `m_csa:994`), 326 review-state
decisions remain pending, and the countable subset has 0 hard negatives,
0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
in-scope failures. `m_csa:836` and `m_csa:865` are regression guardrail rows:
role-inferred or review-marked evidence gaps remain `needs_more_evidence`
rather than counted. The 1000 active-learning queue retains all 321
expert-label decision rows, the 1000 deferral audit keeps every review-state
row non-countable, and the batch summary reports 21/21 accepted batches with
0 blockers.

Current 1,025 preview state: 21/21 factory checks pass, but the preview is not
accepted for counting because it adds 0 clean countable labels. Review debt
rises from 326 to 329 rows, with new rows `m_csa:1003`, `m_csa:1004`, and
`m_csa:1005`, all explicitly deferred as non-countable. The M-CSA source-scale
audit records only 1,003 observed source records for a requested 1,025 tranche,
so the next scaling step is external-source transfer rather than another
M-CSA-only batch. `artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_lane_balance_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_transfer_gate_check_1025.json`, and
`artifacts/v3_external_source_reaction_evidence_sample_1025.json` are
review-only discovery artifacts with 0 countable label candidates.

Historical 700 gate state: 20/20 factory checks pass on the 624-label countable
registry. The latest accepted batch-acceptance check passes: 5 additional
labels were accepted for counting in the 700 batch, 81 review-state decisions
remain pending, and the countable subset has 0 hard negatives, 0 near misses,
0 out-of-scope false non-abstentions, and 0 actionable in-scope failures. The
post-700 active-learning queue retains all 76 unlabeled candidate rows; the
factory gate fails if a capped queue omits any unlabeled row. The queue now
includes reaction/substrate mismatch ranking, and the 700 mismatch audit routes
18 hydrolase-top1 kinase or ATP phosphoryl-transfer rows to expert review. The
700 family-propagation guardrail separately retains 24 reaction/substrate
mismatch blockers, including 14 rows kept beyond `max_rows`; these split into
17 labeled propagation blocks and 7 unlabeled pending-review blocks. The
dedicated mismatch review export now carries all 24 lanes together, records
17 current out-of-scope labels plus 7 unlabeled rows, and now drives the
expert-reviewed nine-family ontology expansion: ePK, ASKHA, ATP-grasp, GHKL,
dNK, NDK, PfkA, PfkB, and GHMP. The generated decision batch preserves all 24
lanes through a review-only decision batch; reviewed out-of-scope repairs
remain non-countable and countable import refuses the artifact. The
expert-label decision repair-candidate summary now covers all 76 active
expert-decision rows with 0 countable candidates, so the gate also fails if
that non-countable repair plan is incomplete. Countable review import also
refuses accepted reaction/substrate mismatch rows unless they are explicitly
expert-reviewed, carry a non-`needs_more_evidence` reaction/substrate
resolution, and do not come from a review-only decision artifact. The batch
summary reports 9/9 accepted batches with 0 blockers. The dedicated
expert-label decision export now carries all 76 active-queue
`expert_label_decision_needed` rows as review-only `no_decision` items, records
0 countable candidates, confirms 0 missing expert-decision export rows, and
keeps the 7 overlapping reaction/substrate mismatch rows tied to the mismatch
export.
The paired repair guardrail audit covers 21 priority expert-decision repair
lanes, including 14 active-site mapping/structure-gap rows and 9
text-leakage/nonlocal-evidence risk rows. The only local expected-family leads
(`m_csa:577`, `m_csa:592`, and `m_csa:641`) come from conservative remaps and
remain review-only with strict remap, family-boundary, or reaction/substrate
blockers. The mechanism ontology gap audit records 115 non-countable
scope-pressure rows, the learned-retrieval manifest defines 562 eligible rows
for a future representation path while preserving heuristic controls, and the
sequence-similarity failure-set audit keeps the 2 exact-reference duplicate
clusters as non-countable propagation controls.
The local-evidence gap audit and review export now cover all 21 priority
repair lanes as review-only/no-decision items, and countable import refuses
accepted decisions from that export type. The local-evidence repair plan keeps
all rows non-countable and prioritizes 4 reaction/substrate expert-review
lanes, 3 explicit alternate-residue-position sourcing lanes, 3 active-site
mapping or structure-selection lanes, and 11 family-boundary review lanes.
The follow-up local-evidence repair resolution artifact consumes the existing
reviewed reaction/substrate mismatch decision batch and closes `m_csa:592`,
`m_csa:643`, `m_csa:654`, and `m_csa:662` as reviewed out-of-scope repair
lanes while keeping them non-countable. The explicit alternate residue-position
request artifact now makes `m_csa:567`, `m_csa:578`, and `m_csa:667`
sourceable across 34 alternate PDB structures. The review-only import-safety
audit covers the mismatch, expert-label decision, and local-evidence decision
batches and confirms they add 0 countable labels through countable import.
The 675 preview initially exposed accepted out-of-scope rows that still carried
review debt, so the provisional decision rule now defers below-threshold,
evidence-limited negatives instead of counting them. The regenerated preview
would add 1 clean countable label (`m_csa:666`) and leave 61 review-state
decisions pending while preserving 0 hard negatives, 0 near misses,
0 out-of-scope false non-abstentions, and 0 actionable in-scope failures. Its
review-debt summary still ranks 61 evidence-gap rows before any promotion
decision. Its preview summary records 11/11 passing gates, 1 attached
scaling-quality audit, and 0 blockers, and
`artifacts/v3_label_scaling_quality_audit_675_preview.json` records 0 accepted
labels with review debt, and the diversity-aware review export retains all
underrepresented ontology-family rows despite hydrolysis-dominated queue
composition. The scaling-quality audit now also warns when no sequence-cluster
artifact is attached for a stronger paralog/near-duplicate audit. Promotion
should inspect the review-debt and scaling-quality artifacts first. The
promotion-readiness check is mechanically ready but recommends
`review_before_promoting` because review debt increases by 8 rows and
needs-more-evidence decisions increase by 24 rows relative to the accepted 650
state; the preview debt metadata lists all 37 carried and 24 new debt entry ids.
See `work/label_preview_675_notes.md` before any promotion.

The accepted 700 remediation pass should be the next repair focus. The focused
new-debt plan covers all 20 new rows; the full plan covers all 81 debt rows.
The alternate-structure scan covers all 13 structure-scan rows and 152
candidate PDB structures with 0 fetch failures. It found structure-wide
expected-family hits for `m_csa:679`, `m_csa:696`, and `m_csa:698`, but 0 local
active-site expected-family hits, so those rows remain review-only. The full
plan also records 69 review-debt rows with alternate PDBs but no alternate-PDB
M-CSA residue-position support.

Remaining-time plan from the 2026-05-10 reaction-mismatch repair run: after
the dedicated mismatch export and gate wiring were in place, keep count growth
stopped and use the remaining productive window to make the export
expert-only, regenerate the 700 gate/scaling/batch artifacts, and document the
new 12th gate before handoff. Completed: the export is no-decision only, the
countable import path now requires explicit expert reaction/substrate
resolution for mismatch-export accepts, and the committed 700 gate/scaling
artifacts retain all 24 mismatch lanes with 0 missing entries.

Do not derive that countable subset by filtering the review-state registry: the
review-state artifact intentionally marks several baseline boundary controls as
`needs_expert_review`. Use `import-countable-label-review` against the baseline
registry and the decision batch so baseline labels are preserved.

Remaining review-state candidates:

- `m_csa:494`: likely cobalamin radical rearrangement, but B12 evidence is
  structure-wide only (`8.349 A` from the selected active-site residues), so it
  remains a documented non-countable evidence gap.
- `m_csa:510`, `m_csa:529`, `m_csa:534`, `m_csa:650`, and later boundary rows:
  tranche candidates marked `needs_expert_review` by the provisional batch
  rules.
- Five carried boundary-control rows (`m_csa:4`, `m_csa:13`, `m_csa:54`,
  `m_csa:140`, and `m_csa:222`) remain review-state only.

Accepted but audit-visible:

- `m_csa:486`: accepted as a bronze automation-curated
  `metal_dependent_hydrolase` after the scorer recognized metal-phosphate
  hydrolysis text context and raised the score to `0.5051`. It remains
  structure-only for local metal evidence, so it must stay visible in cofactor
  coverage audits.
- `m_csa:519`: accepted as a Ser-His-Asp/Glu hydrolase after the provisional
  batch builder was fixed to trust strong Ser-His triad text despite metal-rich
  local context that otherwise looked like counterevidence.

## Automation Lock Hardening

`src/catalytic_earth/automation.py` now contains the atomic directory-lock
logic used by the automation prompt, and
`PYTHONPATH=src python -m catalytic_earth.cli automation-lock` exposes acquire,
status, and guarded release operations. The release command can require a clean
worktree, no merge in progress, and local `HEAD` synchronized with `origin/main`
before deleting `.git/catalytic-earth-automation.lock`.
