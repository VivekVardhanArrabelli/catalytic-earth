# Lever 2 Event-Axis Leave-One-Out Current-Extended Frontier Readout

- Artifact: `v3_lever2_event_axis_loo_current_extended_frontier_readout_current702_20260604`
- Status: `lever2_event_axis_loo_current_extended_frontier_readout_research_only_loo_marginal_axis_signal_primary_control_caveat`
- Created UTC: `2026-06-04T19:57:55Z`

## Measured Result

- Baseline projected subset: `source_free_projected_proton_role_subset` catches 5/13 current-retained overlap rows under leave-one-out selection.
- Best projected-subset-plus-axis frontier: `source_free_projected_proton_role_subset+bond_change` catches 7/13 current-retained overlap rows.
- Marginal catches beyond projected subset: 2 (m_csa:256, m_csa:312).
- Current primary retention on the active split remains unmeasurable: 0/34 valid current-primary rows have calibration-split mechanism features.

## Leave-One-Out Single-Axis Frontier

| axis | source-free status | LOO rows | retained OOS caught | OR abstained | caught rows |
| --- | --- | ---: | ---: | ---: | --- |
| source_free_projected_proton_role_subset | source_free_compatible_proxy | 21 | 5/13 | 13/21 | m_csa:17, m_csa:59, m_csa:85, m_csa:194, m_csa:222 |
| bond_change | requires_new_source_free_axis | 21 | 4/13 | 12/21 | m_csa:59, m_csa:85, m_csa:256, m_csa:312 |
| proton_transfer | partially_supported_by_event_axis_linkers | 21 | 2/13 | 10/21 | m_csa:59, m_csa:222 |
| electron_flow | requires_new_source_free_axis | 21 | 1/13 | 9/21 | m_csa:256 |
| event_topology | requires_new_source_free_axis | 21 | 0/13 | 8/21 | none |
| active_site_locator_count | requires_source_free_locator_coverage | 21 | 2/13 | 10/21 | m_csa:59, m_csa:194 |
| confidence_metadata | research_only_metadata_axis | 21 | 0/13 | 8/21 | none |
| all_priority_event_axes | requires_multi_axis_source_free_materialization | 21 | 0/13 | 8/21 | none |

## Projected Subset Plus Added Axis

| added axis | source-free status | retained OOS caught | marginal caught | primary LOO retained | OR abstained | marginal rows |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bond_change | requires_source_free_materialization | 7/13 | 2 | 3/4 | 15/21 | m_csa:256, m_csa:312 |
| electron_flow | requires_source_free_materialization | 6/13 | 1 | 3/4 | 14/21 | m_csa:256 |
| proton_transfer | requires_source_free_materialization | 5/13 | 0 | 3/4 | 13/21 | none |
| event_topology | requires_source_free_materialization | 5/13 | 0 | 2/4 | 13/21 | none |
| active_site_locator_count | requires_source_free_materialization | 5/13 | 0 | 2/4 | 13/21 | none |
| confidence_metadata | requires_source_free_materialization | 5/13 | 0 | 2/4 | 13/21 | none |
| all_priority_event_axes | requires_source_free_materialization | 5/13 | 0 | 2/4 | 13/21 | none |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_axis_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free row-specific mechanism/event-axis features before any deployable Lever 2 claim. |
| current_retained_oos_source_free_event_axis_rows | 132 | 0 | 132 | These are rows retained by geometry/fold where event-axis mechanism evidence can add abstention value. |
| best_loo_projection_plus_axis_source_free_fields | 9 | 4 | 5 | The best leave-one-out marginal axis must exist as source-free deployment-valid row features on the current split, not only as M-CSA train/cal research fields. |

## Priority Current-Retained Overlap Rows

| row | current score | baseline score | added-axis score | added rule | source-free row exists | marginal |
| --- | ---: | ---: | ---: | --- | --- | --- |
| m_csa:17 | 0.45885 | 4.0 | 9.0 | low 0.0 | False | False |
| m_csa:59 | 0.60775 | 5.0 | 0.0 | low 0.0 | False | False |
| m_csa:85 | 0.49955 | 4.0 | 0.0 | low 0.0 | False | False |
| m_csa:194 | 0.4559 | 4.0 | 5.0 | low 0.0 | False | False |
| m_csa:222 | 0.52675 | 5.0 | 5.0 | low 0.0 | False | False |
| m_csa:256 | 0.61925 | 0.0 | 0.0 | low 0.0 | False | True |
| m_csa:312 | 0.5714 | 3.0 | 0.0 | low 0.0 | False | True |

## Decision

- Leave-one-out projected subset signal beyond current surface: True
- Genuinely new axis adds beyond projected subset: True
- Best new axis: `bond_change`
- Best projected-subset-plus-axis primary LOO control passes: False
- Any projected-subset-plus-axis primary LOO control passes: False
- Adds integrated operating-point value beyond current surface: False
- Source-free current split operating point measurable: False
- Deployable now: False
- Research-only: True
- Next gate: Materialize source-free current-split event-axis rows for source_free_projected_proton_role_subset+bond_change, starting with 34 primary retention-gate rows and 132 current-retained OOS rows; then rerun this leave-one-out frontier before any deployment or heldout claim.

## Interpretation

- Leave-one-out projected-subset plus bond_change catches 7/13 current-retained overlap rows, with 2 marginal catches beyond the projected subset.
- Research-only leave-one-out marginal signal with a primary control caveat: the best new axis adds local current-overlap catches beyond the projected subset, but the same projected-subset-plus-axis rule retains only 3/4 mechanism primaries under leave-one-primary-out control.
- Build split-aligned source-free event-axis evidence for the best leave-one-out marginal axis on the current primary and current-retained OOS rows before any deployment or heldout claim.
