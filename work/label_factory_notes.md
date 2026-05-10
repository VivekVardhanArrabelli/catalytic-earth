# Label Factory Work Notes

## Current Plan

The first two 500-slice label-factory decision batches have been accepted for
counting. Use the next bounded block to resolve the one remaining 500-slice
review candidate rather than opening a new bulk tranche.

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

Current export behavior: the expert-review artifact includes the top-ranked
review rows plus the remaining unlabeled 500-slice candidate so label expansion
cannot skip a lower-ranked unlabeled row.

Current gate state: 9/9 factory checks pass on the 499-label countable
registry. The latest batch-acceptance check also passes: 1 additional label was
accepted for counting, 6 review-state decisions remain pending, and the
countable subset has
0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, and
0 actionable in-scope failures.

Do not derive that countable subset by filtering the review-state registry: the
review-state artifact intentionally marks several baseline boundary controls as
`needs_expert_review`. Use `import-countable-label-review` against the baseline
registry and the decision batch so baseline labels are preserved.

Remaining review candidates:

- `m_csa:494`: likely cobalamin radical rearrangement, but B12 evidence is
  structure-wide only (`8.349 A` from the selected active-site residues), so it
  should stay out of the countable registry until the cofactor/structure
  evidence is resolved.

Accepted but audit-visible:

- `m_csa:486`: accepted as a bronze automation-curated
  `metal_dependent_hydrolase` after the scorer recognized metal-phosphate
  hydrolysis text context and raised the score to `0.5051`. It remains
  structure-only for local metal evidence, so it must stay visible in cofactor
  coverage audits.

## Automation Lock Hardening

`src/catalytic_earth/automation.py` now contains the atomic directory-lock
logic used by the automation prompt, and
`PYTHONPATH=src python -m catalytic_earth.cli automation-lock` exposes acquire,
status, and guarded release operations. The release command can require a clean
worktree, no merge in progress, and local `HEAD` synchronized with `origin/main`
before deleting `.git/catalytic-earth-automation.lock`.
