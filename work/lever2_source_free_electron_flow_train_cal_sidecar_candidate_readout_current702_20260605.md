# Lever 2 Source-Free Electron-Flow Train/Cal Sidecar Candidate Readout - current702

Run: 2026-06-05T16:47:53Z

Lever 2 measured candidate-sidecar readout for direct source-free electron-flow fields. It remaps the candidate train/cal bundle into sidecar-shaped row-specific event features, audits explicit train/cal split coverage and manifest containment, and reruns the fixed operating point. It does not edit approved sidecars, imports, labels, registries, ontologies, thresholds, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout_research_only_train_cal_sidecar_candidate_measured_pending_protected_import
- Result class: research_only_train_cal_sidecar_candidate_measured_pending_protected_import
- Candidate sidecar rows: 78
- Complete source-free rows: 78/78
- Manifest or explicit train/cal-contained rows: 78/78
- Explicit train/cal split rows: 76/78
- Current primary/OOS positives: 0/3
- Primary retain recall: 1.0
- Incremental OOS recall vs current geometry/fold: 0.04
- Union OOS recall: 0.506667
- Forbidden row-feature key hits: 0

## Fixed Operating Point

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 |

## Split Discipline

- Support rows missing explicit train/cal split: m_csa:127, m_csa:281
- Selected Fe-S support rows missing explicit train/cal split: m_csa:127, m_csa:281
- Selected Fe-S support rows blocked by predictive gate/import: m_csa:127, m_csa:281

## Approved Sidecar Gap

- Direct component fields present: none
- Direct component fields missing: has_source_free_pqq_donor_acceptor_contact, source_free_pqq_donor_acceptor_contact_count, has_source_free_nad_family_donor_acceptor_distance, source_free_nad_family_donor_acceptor_distance_count, has_source_free_iron_sulfur_or_iron_donor_acceptor_distance, source_free_iron_sulfur_or_iron_donor_acceptor_distance_count
- Support rows present: m_csa:59, m_csa:256
- Current positive rows present: none
- Approved sidecar current-split rows present: 1/74
- Approved sidecar current-split rows with direct components complete: 0/74

## Decision

- Sidecar candidate shape complete: True
- Manifest or explicit train/cal-contained: True
- All rows have explicit train/cal split: False
- Preserves primary retention: True
- Adds OOS abstention: True
- Train/cal-disciplined candidate readout available: True
- Approved-sidecar-only route measurable now: False
- Deployable now: False
- Remaining gap: approved_train_cal_feature_sidecar_direct_component_field_import; predictive_use_allowed_true_for_selected_fe_s_support_rows:m_csa:127,m_csa:281; explicit_train_cal_split_assignment_for_selected_fe_s_support_rows:m_csa:127,m_csa:281; approved_sidecar_rows_for_current_positive_direct_electron_flow_rows:m_csa:104,m_csa:119,m_csa:464
- Smallest next experiment: Perform the protected approval/import step for the candidate direct source-free component fields, set predictive_use_allowed=true for m_csa:127 and m_csa:281, assign those Fe-S support rows to explicit train/cal splits, then rerun this fixed sidecar candidate gate without threshold changes or heldout use.

## Interpretation

- The sidecar-shaped candidate keeps the direct source-free electron-flow gate measurable on 74/74 current-split rows, preserves primary retention, and catches 3 current-retained OOS rows.
- The remaining work is protected approval/import plus explicit split assignment, not another operating-point search route.
