# Lever 2 Source-Free Electron-Flow Approval Import Dry-Run Readout - current702

Run: 2026-06-05T17:50:09Z

Lever 2 measured approval/import dry-run for direct source-free electron-flow fields. It overlays the train/cal sidecar candidate onto the approved sidecar shape in memory, assigns the selected Fe-S support rows an explicit calibration split for measurement, and reruns the fixed current-split operating point. It does not edit labels, registries, ontologies, imports, production thresholds, approved sidecars, predictive-use flags, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_approval_import_dry_run_readout_research_only_approval_import_dry_run_closes_measurability_gap
- Result class: research_only_approval_import_dry_run_closes_measurability_gap
- Approved current-split direct rows before dry run: 0/74
- Dry-run current-split direct rows complete: 74/74
- Dry-run explicit train/cal split rows: 78/78
- Dry-run primary/OOS positives: 0/3
- Primary retain recall: 1.0
- Incremental OOS recall vs current geometry/fold: 0.04
- Union OOS recall: 0.506667
- Forbidden row-feature key hits: 0

## Fixed Operating Point After Dry Run

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 |

## Dry-Run Overlay

- Rows imported by dry run: 78
- Rows new to approved sidecar: 75
- Existing approved rows updated by dry run: 3
- Current-split rows added to approved sidecar: 73
- Current positive rows added: m_csa:104, m_csa:119, m_csa:464
- Selected Fe-S proposed splits: {'m_csa:127': 'calibration', 'm_csa:281': 'calibration'}
- Selected Fe-S manifest in-distribution rows: m_csa:127, m_csa:281
- Selected Fe-S role-graph-ok rows: m_csa:127, m_csa:281

## Fe-S Split Sensitivity

| policy | proposed splits | explicit rows | fixed gate matches primary dry run |
| --- | --- | ---: | --- |
| all_selected_fe_s_calibration | {'m_csa:127': 'calibration', 'm_csa:281': 'calibration'} | 78 | True |
| all_selected_fe_s_train | {'m_csa:127': 'train', 'm_csa:281': 'train'} | 78 | True |

## Component Ablation

| ablation | components | retained-OOS positives | primary positives | incremental OOS recall |
| --- | --- | --- | ---: | ---: |
| pqq_only | pqq | m_csa:104 | 0 | 0.013333 |
| nad_family_only | nad | m_csa:464 | 0 | 0.013333 |
| iron_sulfur_only | iron_sulfur | m_csa:119 | 0 | 0.013333 |
| pqq_plus_nad_family | nad, pqq | m_csa:104, m_csa:464 | 0 | 0.026667 |
| pqq_plus_nad_family_plus_iron_sulfur | iron_sulfur, nad, pqq | m_csa:104, m_csa:119, m_csa:464 | 0 | 0.04 |

## Decision

- Dry-run closes approved-sidecar direct component gap: True
- Dry-run closes explicit split gap: True
- Dry-run preserves primary retention: True
- Dry-run adds OOS abstention: True
- Approved-sidecar route measurable after dry run: True
- Selected Fe-S split policy affects operating point: False
- Fe-S adds a row beyond PQQ+NAD after dry-run import: True
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: human_or_protected approval of direct source-free component field contract; protected import/materialization of the 78 dry-run feature rows; predictive_use_allowed=true for selected Fe-S support rows m_csa:127 and m_csa:281; explicit train/cal split assignment for selected Fe-S support rows m_csa:127 and m_csa:281
- Smallest next experiment: Run the protected sidecar materialization/review step using the 78 dry-run rows, assign m_csa:127 and m_csa:281 to the explicit calibration split, set predictive_use_allowed=true for those two Fe-S support rows, then rerun the approved sidecar-only gate unchanged.

## Interpretation

- The dry-run approved-sidecar overlay closes the 74-row direct component measurability gap, preserves current primary retention, and catches m_csa:104, m_csa:119, and m_csa:464 at the fixed current-split gate.
- The remaining work is the protected materialization/review step. This artifact supplies the exact row set, component fields, proposed Fe-S split assignments, and fixed-gate readout to rerun after approval.
