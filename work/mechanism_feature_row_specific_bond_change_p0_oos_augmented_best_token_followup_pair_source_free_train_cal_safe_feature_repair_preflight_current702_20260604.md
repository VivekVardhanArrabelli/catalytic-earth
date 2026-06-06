# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Train/Cal-Safe Feature Repair Preflight - current702

Run: 2026-06-04T02:11:48Z

Train/cal-safe post-readout diagnosis for the source-free pair surface. It consumes the already-spent heldout readout only as a fixed failure set, compares its populated source-free model features to the frozen train/cal residual feature contract, and does not rescore heldout rows, refit models, retune thresholds, or authorize another heldout read.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_train_cal_safe_feature_repair_preflight_ready_deployment_blocked
- Feature-complete readout rows: 53
- Feature-complete primary abstentions: 32
- Primary abstentions with projection gap: 32
- Frozen feature fields: 19
- Source-free projected feature fields: 2
- Missing frozen feature fields: 17
- Priority repair feature fields: 11
- Priority fields with direct existing source-free axis: 2
- Priority fields requiring new source-free axis: 9
- Repair categories: {'bond_change': 5, 'electron_flow': 2, 'event_topology': 2, 'proton_transfer': 2}
- Source-free event-axis materialized rows: 14
- Source-free event-axis types: {'proton_transfer': 14}
- Blockers: source_free_projection_missing_frozen_train_cal_event_fields, feature_complete_primary_residual_abstentions_remain

## Decision

- Deployable claim blocked: True
- Train/cal-safe feature repair required: True
- Coverage repair alone sufficient: False
- Projection gap is current primary failure gate: True
- Rerun or retune heldout authorized: False
- Next gate: Do not rerun or retune the heldout read. Materialize a source-free projection for the priority frozen train/cal event fields first, especially bond-change, proton-transfer, electron-flow, and event-topology counts; then validate only through train/cal guardrails before any deployable Lever 2 claim.

## Missing Frozen Fields

| field | category | train/cal positives | source-free status | priority |
| --- | --- | ---: | --- | --- |
| bond_broken_count | bond_change | 20 | missing_source_free_axis | True |
| bond_change_event_count | bond_change | 35 | missing_source_free_axis | True |
| bond_formed_count | bond_change | 24 | missing_source_free_axis | True |
| bond_order_changed_count | bond_change | 6 | missing_source_free_axis | True |
| has_bond_change_event | bond_change | 35 | missing_source_free_axis | True |
| electron_transfer_count | electron_flow | 15 | missing_source_free_axis | True |
| has_electron_transfer_event | electron_flow | 15 | missing_source_free_axis | True |
| event_count | event_topology | 43 | requires_multi_axis_source_free_projection | True |
| multi_event_mechanism_flag | event_topology | 41 | requires_multi_axis_source_free_projection | True |
| has_proton_transfer_event | proton_transfer | 32 | partial_existing_source_free_event_axis_support | True |
| proton_transfer_count | proton_transfer | 32 | partial_existing_source_free_event_axis_support | True |
| mapped_active_site_residue_count | active_site_locator_count | 43 | not_a_priority_event_axis_repair | False |
| unique_mapped_active_site_residue_count | active_site_locator_count | 43 | not_a_priority_event_axis_repair | False |
| high_confidence_event_count | confidence_metadata | 0 | not_a_priority_event_axis_repair | False |
| low_confidence_event_count | confidence_metadata | 1 | not_a_priority_event_axis_repair | False |
| medium_confidence_event_count | confidence_metadata | 43 | not_a_priority_event_axis_repair | False |
| unknown_confidence_event_count | confidence_metadata | 0 | not_a_priority_event_axis_repair | False |

## Failure Profiles

| rows | profile |
| ---: | --- |
| 10 | event_residue_role:proton_transfer\|electrostatic_stabiliser=False;residue_code_count:his=0;residue_code_count:his=3=False |
| 6 | event_residue_role:proton_transfer\|electrostatic_stabiliser=True;residue_code_count:his=1;residue_code_count:his=3=False |
| 4 | event_residue_role:proton_transfer\|electrostatic_stabiliser=False;residue_code_count:his=1;residue_code_count:his=3=False |
| 4 | event_residue_role:proton_transfer\|electrostatic_stabiliser=True;residue_code_count:his=0;residue_code_count:his=3=False |
| 3 | event_residue_role:proton_transfer\|electrostatic_stabiliser=False;residue_code_count:his=2;residue_code_count:his=3=False |
| 2 | event_residue_role:proton_transfer\|electrostatic_stabiliser=False;residue_code_count:his=3;residue_code_count:his=3=True |
| 2 | event_residue_role:proton_transfer\|electrostatic_stabiliser=True;residue_code_count:his=2;residue_code_count:his=3=False |
| 1 | event_residue_role:proton_transfer\|electrostatic_stabiliser=True;residue_code_count:his=3;residue_code_count:his=3=True |

## Interpretation

- All feature-complete primary residual abstentions share the same contract gap: the source-free readout populated only 2/19 frozen model fields, leaving the train/cal event-count surface zero-filled at application time.
- Repair feature projection before locator coverage: source-free locators alone cannot make the frozen pair channel deployable. Existing source-free event-axis rows can only partially support the proton-transfer fields; bond-change, electron-flow, and event-topology fields need a new source-free projection packet.
