# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Projection Repair Candidate Surface - current702

Run: 2026-06-04T02:14:40Z

Partial candidate projection surface for the source-free pair feature repair path. It materializes only direct fields supported by already-approved source-free event-axis linkers, keeps missing bond-change/electron/event-topology axes explicit, and does not apply the frozen residual threshold or rescore heldout rows.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_projection_repair_candidate_surface_partial_not_scoreable
- Candidate rows: 53
- Direct proton-transfer projection rows: 14
- Pair-only rows: 39
- Full frozen projection ready rows: 0
- Threshold-scoring ready rows: 0
- Direct existing source-free fields: ['has_proton_transfer_event', 'proton_transfer_count']
- New source-free axis required fields: ['bond_broken_count', 'bond_change_event_count', 'bond_formed_count', 'bond_order_changed_count', 'electron_transfer_count', 'event_count', 'has_bond_change_event', 'has_electron_transfer_event', 'multi_event_mechanism_flag']
- Blockers: projection_candidate_surface_partial_missing_new_source_free_axes, heldout_read_already_spent_no_threshold_application_authorized

## Decision

- Candidate surface ready for threshold scoring: False
- Direct proton projection materialized: True
- New source-free axis review packet required: True
- Rerun or retune heldout authorized: False
- Next gate: Use this partial candidate only as repair evidence. Build a source-free bond-change/electron-flow/event-topology axis review packet for the 9 priority fields still lacking direct source-free support; do not score or rerun heldout from this partial projection.

## Candidate Rows

| row | status | direct fields | missing frozen fields |
| --- | --- | --- | ---: |
| m_csa:3 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:9 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:32 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:43 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:44 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:45 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:46 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:56 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:97 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:109 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:115 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:121 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:131 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:159 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:163 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:171 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:180 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:188 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:199 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:211 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:220 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:239 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:242 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:250 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:311 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:321 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:323 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:333 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:352 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:356 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:370 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:384 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:392 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:397 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:403 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:418 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:419 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:480 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:497 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:517 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:526 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:541 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:545 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:551 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:709 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:710 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:714 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:750 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:853 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:854 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:916 | pair_only_projection_missing_priority_fields | [] | 17 |
| m_csa:990 | partial_direct_proton_projection | ['has_proton_transfer_event', 'proton_transfer_count'] | 15 |
| m_csa:994 | pair_only_projection_missing_priority_fields | [] | 17 |

## Interpretation

- Existing approved source-free event-axis evidence can fill the direct proton-transfer projection for 14 rows, but no row has the full frozen 19-field projection.
- Create the missing source-free bond/electron/event-topology axis packet before any scoring surface or deployable Lever 2 claim is considered.
