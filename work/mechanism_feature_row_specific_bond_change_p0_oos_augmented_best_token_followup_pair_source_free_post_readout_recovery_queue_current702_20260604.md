# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Post-Readout Recovery Queue - current702

Run: 2026-06-04T01:28:43Z

Post-readout recovery queue for the already-spent source-free heldout threshold read. It classifies primary-retention and coverage failures without rescoring rows, changing the frozen threshold, refitting models, or authorizing another heldout read.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_post_readout_recovery_queue_ready_deployment_blocked
- Queue rows: 119
- Feature-complete primary residual abstentions: 32
- Primary missing-locator abstentions: 16
- OOS missing-locator abstentions: 71
- Feature-complete OOS retained by residual: 0
- Outcome counts: {'oos_abstained_by_residual': 21, 'oos_abstained_missing_locator': 71, 'primary_abstained_by_residual': 32, 'primary_abstained_missing_locator': 16}
- Queue classes: {'feature_complete_primary_abstained_by_residual': 32, 'oos_missing_source_free_locator': 71, 'primary_missing_source_free_locator': 16}
- Blockers: source_free_partial_surface_retains_zero_heldout_primaries_at_frozen_threshold

## Decision

- Deployable claim blocked: True
- Coverage repair alone sufficient: False
- Feature-complete primary failure is blocking: True
- Source-free locator coverage repair still needed: True
- Rerun or retune heldout authorized: False
- Next gate: Do not rerun or retune the heldout read. First explain the 32 feature-complete primary residual abstentions from train/cal-safe feature evidence, then repair the 16 missing primary source-free locator rows before any deployable Lever 2 claim.

## Priority Rows

| row | priority | class | outcome | residual | threshold | next action |
| --- | ---: | --- | --- | ---: | ---: | --- |
| m_csa:3 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:43 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:44 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:97 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:109 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:115 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:131 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:159 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:163 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:171 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:180 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:211 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:239 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:242 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:250 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:321 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:403 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 6.47719266 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:418 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:419 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:497 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:517 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:545 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:551 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:709 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:710 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 6.47719266 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:714 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 6.78139794 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:750 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:853 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:854 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:916 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:990 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.82128492 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:994 | 1 | feature_complete_primary_abstained_by_residual | primary_abstained_by_residual | 5.46388369 | 3.21469422 | Investigate source-free feature materialization or train/cal-only feature design; do not lower or retune the frozen threshold from heldout. |
| m_csa:20 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:213 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:372 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:407 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:424 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:431 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:453 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:577 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:599 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:609 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:686 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:688 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:723 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:866 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:892 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:897 | 2 | primary_missing_source_free_locator | primary_abstained_missing_locator |  |  | Repair the source-free locator/application surface so the row is not lost to deterministic missing-locator abstention. |
| m_csa:10 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:12 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:14 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:30 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:31 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:34 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:67 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:71 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:73 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:79 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:80 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:86 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:116 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:118 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:125 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:129 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:144 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:155 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:185 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:191 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:192 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:193 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:197 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:198 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:201 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:217 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:219 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:225 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:230 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:254 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:255 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:267 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:297 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:313 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:334 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:346 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:355 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:363 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:369 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:375 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:388 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:396 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:402 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:409 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:423 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:428 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:438 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:440 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:444 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:448 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:474 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:477 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:484 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:493 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:509 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:511 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:536 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:549 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:563 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:566 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:590 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:594 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:606 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:614 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:617 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:620 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:627 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:628 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:634 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:647 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |
| m_csa:651 | 3 | oos_missing_source_free_locator | oos_abstained_missing_locator |  |  | Deprioritize behind primary-retention failures; repair only as coverage-expansion evidence, not as heldout threshold tuning. |

## Interpretation

- The frozen source-free partial surface is not deployable: 32 feature-complete primaries abstain by residual and 16 additional primaries abstain because their source-free locators are missing.
- Treat the heldout readout as final evidence for this surface; continue Lever 2 with train/cal-only feature repair plus source-free locator coverage recovery.
