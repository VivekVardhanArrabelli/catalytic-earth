# Label Factory Work Notes

## Current Plan

The 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, and 700-slice
label-factory batches have been processed through countable import and
acceptance checks. The canonical registry has 624 countable labels. Do not
open another tranche until the accepted-700 review-debt surface is repaired:
81 rows remain `needs_more_evidence`, and the latest remediation artifacts show
that structure-wide cofactor-family hits still lack local active-site support.

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
- `artifacts/v3_family_propagation_guardrails_700.json`
- `artifacts/v3_label_scaling_quality_audit_700_preview.json`
- `artifacts/v3_sequence_cluster_proxy_700.json`

Current export behavior: expert-review artifacts include top-ranked review rows
plus every unlabeled queue row, so label expansion cannot skip a lower-ranked
unlabeled candidate.

Current gate state: 11/11 factory checks pass on the 624-label countable
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
17 labeled propagation blocks and 7 unlabeled pending-review blocks. The batch
summary reports 9/9 accepted batches with 0 blockers.
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
