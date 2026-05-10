# Label Factory Work Notes

## Current Plan

The 500-, 525-, and 550-slice label-factory batches have been processed through
countable import and acceptance checks. The next bounded block should either
open the 575-entry scaffold from the 550 review-state registry or work on the
remaining evidence-limited/pending-review rows; do not reprocess accepted 525 or
550 batches.

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

Current export behavior: expert-review artifacts include top-ranked review rows
plus every unlabeled queue row, so label expansion cannot skip a lower-ranked
unlabeled candidate.

Current gate state: 9/9 factory checks pass on the 546-label countable
registry. The latest batch-acceptance check passes: 23 additional labels were
accepted for counting in the 550 batch, 9 review-state decisions remain
pending, and the countable subset has 0 hard negatives, 0 near misses,
0 out-of-scope false non-abstentions, and 0 actionable in-scope failures.

Do not derive that countable subset by filtering the review-state registry: the
review-state artifact intentionally marks several baseline boundary controls as
`needs_expert_review`. Use `import-countable-label-review` against the baseline
registry and the decision batch so baseline labels are preserved.

Remaining review-state candidates:

- `m_csa:494`: likely cobalamin radical rearrangement, but B12 evidence is
  structure-wide only (`8.349 A` from the selected active-site residues), so it
  remains a documented non-countable evidence gap.
- `m_csa:510`, `m_csa:529`, and `m_csa:534`: tranche candidates marked
  `needs_expert_review` by the provisional batch rules.
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
