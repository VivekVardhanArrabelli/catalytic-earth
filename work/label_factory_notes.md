# Label Factory Work Notes

## Remaining-Time Plan

The first vertical label-factory slice is implemented and generating artifacts.
Use the remaining productive time before wrap-up to harden the slice rather than
start bulk label scaling:

1. Verify validation and full tests against migrated labels and new artifacts.
2. Add documentation that makes label scaling contingent on factory gates.
3. Inspect generated queue, adversarial-negative, and propagation artifacts for
   obvious stale or misleading metadata.
4. Leave the next run focused on using the 500-entry queue through the factory
   workflow instead of counting labels directly.

## Current Generated Artifacts

- `artifacts/v3_label_factory_audit_475.json`
- `artifacts/v3_label_factory_applied_labels_475.json`
- `artifacts/v3_adversarial_negative_controls_475.json`
- `artifacts/v3_active_learning_review_queue_500.json`
- `artifacts/v3_expert_review_export_500.json`
- `artifacts/v3_expert_review_import_preview_500.json`
- `artifacts/v3_family_propagation_guardrails_500.json`
- `artifacts/v3_label_factory_gate_check_500.json`

Current export behavior: the expert-review artifact includes the top-ranked
review rows plus all 25 unlabeled 500-slice candidates so label expansion cannot
skip lower-ranked unlabeled rows.

Current gate state: 9/9 checks pass, including explicit schema, ontology,
promotion, applied actions, adversarial negatives, active-learning ranking,
expert-review export, family-propagation guardrails, and abstention/review
demonstration.

## Automation Lock Hardening

`src/catalytic_earth/automation.py` now contains the atomic directory-lock
logic used by the automation prompt, and
`PYTHONPATH=src python -m catalytic_earth.cli automation-lock` exposes acquire,
status, and guarded release operations. The release command can require a clean
worktree, no merge in progress, and local `HEAD` synchronized with `origin/main`
before deleting `.git/catalytic-earth-automation.lock`.
