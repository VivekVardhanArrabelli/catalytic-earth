# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Action Queue - current702

Run: 2026-06-02T13:14:30Z

Queue for materializing approved source-free active-site locator sidecars needed by the best-token follow-up pair heldout application surface. It prioritizes heldout rows by existing coordinate/readiness evidence, does not promote M-CSA active-site roles to deployment features, and does not score heldout.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_action_queue_ready
- Heldout rows: 140
- Approved current702 source-free locators: 0
- Priority-1 coordinate-ready locator candidates: 126
- Priority-2 predicted-geometry missing: 4
- Priority-3 predicted-structure fetch failed: 2
- Accession-compatible position blockers: 8

## Decision

- Locator materialization queue ready: True
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Start with the priority-1 coordinate-ready rows and create approved source-free locator sidecars from coordinate-local evidence only; then rerun the source-free application-surface audit before any frozen-threshold application.

## Interpretation

- The current702 heldout surface has no approved source-free locators yet, but 126 rows already have coordinate-ready predicted-geometry evidence suitable for locator-sidecar review.
- Create approved source-free locator sidecars for the priority-1 rows without using heldout labels, M-CSA heldout mechanism text, EC/Rhea identifiers, source IDs, or target names.
