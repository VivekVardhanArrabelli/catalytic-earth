# Lever 2 Source-Free Electron-Flow Candidate Train/Cal Bundle Readout - current702

Run: 2026-06-05T15:59:13Z

Lever 2 train/cal-disciplined candidate bundle readout for direct source-free electron-flow fields. It materializes, as a research-only artifact, the current-split PQQ+NAD+Fe-S component rows plus the smallest measured NAD and Fe-S support rows needed to audit the approved train/cal sidecar gap. It does not approve, import, tune, train, score heldout, edit registries, or promote any feature.

## Status

- lever2_source_free_electron_flow_candidate_train_cal_bundle_readout_research_only_candidate_train_cal_bundle_materialized_pending_approval_import
- Result class: research_only_candidate_train_cal_bundle_materialized_pending_approval_import
- Candidate bundle rows: 78
- Current split complete rows: 74/74
- Current primary/OOS positives: 0/3
- Primary retain recall: 1.0
- Incremental OOS recall vs current geometry/fold: 0.04
- Union OOS recall: 0.506667
- Support rows complete: 4/4
- Forbidden row-feature key hits: 0

## Fixed Operating Point

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 |

## Candidate Support Rows

- PQQ+NAD projection support rows: m_csa:59, m_csa:256
- Selected Fe-S support rows: m_csa:127, m_csa:281
- Support rows with explicit train/cal split: m_csa:59, m_csa:256
- Expected support rows missing from candidate bundle: none
- Selected Fe-S support rows missing explicit train/cal split: m_csa:127, m_csa:281
- Selected Fe-S support rows present in train/cal manifest: m_csa:127, m_csa:281
- Selected Fe-S support rows in distribution: m_csa:127, m_csa:281
- Selected Fe-S support rows with role graph ok: m_csa:127, m_csa:281

## Approved Sidecar Gap

- Approved sidecar rows: 43
- Candidate support rows present: m_csa:59, m_csa:256
- Candidate current positive rows present: none
- Direct component fields present: none
- Direct component fields missing: has_source_free_pqq_donor_acceptor_contact, source_free_pqq_donor_acceptor_contact_count, has_source_free_nad_family_donor_acceptor_distance, source_free_nad_family_donor_acceptor_distance_count, has_source_free_iron_sulfur_or_iron_donor_acceptor_distance, source_free_iron_sulfur_or_iron_donor_acceptor_distance_count

## Decision

- Candidate bundle materialized: True
- Candidate bundle preserves primary retention: True
- Candidate bundle adds OOS abstention: True
- Candidate bundle closes component-field gap: True
- Candidate expected support rows materialized: True
- Train/cal manifest confirms selected Fe-S rows in distribution: True
- Train/cal manifest confirms selected Fe-S role graph ok: True
- Approved sidecar still missing component fields: True
- Selected Fe-S still missing approval/import: True
- Selected Fe-S still missing explicit split assignment: True
- Support-contract gap only: True
- Deployable now: False
- Remaining gap: approved train/cal sidecar lacks direct source-free PQQ/NAD/Fe-S component fields; selected Fe-S support rows need predictive_use_allowed=true plus approved sidecar rows: m_csa:127, m_csa:281; selected Fe-S support rows need explicit train/cal split assignment: m_csa:127, m_csa:281; current positive direct electron-flow rows are not present in the approved sidecar: m_csa:104, m_csa:119, m_csa:464
- Smallest next experiment: Approve/import the candidate direct component fields into the train/cal feature sidecar, set predictive_use_allowed=true for m_csa:127 and m_csa:281, and assign those Fe-S support rows to an explicit train/cal split before rerunning this fixed bundle.

## Interpretation

- The research-only candidate bundle has complete direct source-free PQQ, NAD-family, and Fe-S/iron component fields on 74/74 current-split rows, preserves primary retention, and catches 3 current-retained OOS rows.
- Use the candidate bundle as the minimal import target; the remaining blockers are approval/import and explicit split assignment, not an operating-point failure.
