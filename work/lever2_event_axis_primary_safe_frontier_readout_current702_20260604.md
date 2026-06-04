# Lever 2 Event-Axis Primary-Safe Frontier Readout

- Artifact: `v3_lever2_event_axis_primary_safe_frontier_readout_current702_20260604`
- Status: `lever2_event_axis_primary_safe_frontier_readout_research_only_primary_safe_marginal_axis_negative`
- Created UTC: `2026-06-04T20:56:52Z`

## Measured Result

- Baseline projected subset catches 5/13 current-retained overlap rows under strict LOO selection.
- Best marginal pair before primary control: `source_free_projected_proton_role_subset+bond_change` catches 7/13 current-retained rows, with 2 marginal catches.
- Its primary LOO control retains 3/4 rows; abstained controls: m_csa:133.
- Best primary-safe pair: none.

## Primary-Safe Frontier

| added axis | retained OOS caught | marginal caught | primary LOO retained | primary-safe | marginal rows |
| --- | ---: | ---: | ---: | --- | --- |
| bond_change | 7/13 | 2 | 3/4 | False | m_csa:256, m_csa:312 |
| electron_flow | 6/13 | 1 | 3/4 | False | m_csa:256 |
| proton_transfer | 5/13 | 0 | 2/4 | False | none |
| event_topology | 5/13 | 0 | 2/4 | False | none |
| active_site_locator_count | 5/13 | 0 | 2/4 | False | none |
| confidence_metadata | 5/13 | 0 | 2/4 | False | none |
| all_priority_event_axes | 5/13 | 0 | 2/4 | False | none |

## Primary-Retention Floor Sensitivity

| min primary retain | primary-safe surfaces | best marginal axis | best marginal catches | best primary-safe axis | primary-safe marginal catches | rows |
| ---: | ---: | --- | ---: | --- | ---: | --- |
| 1.0 | 0 | source_free_projected_proton_role_subset+bond_change | 2 | none | 0 | none |
| 0.9 | 0 | source_free_projected_proton_role_subset+bond_change | 2 | none | 0 | none |
| 0.75 | 2 | source_free_projected_proton_role_subset+all_priority_event_axes | 2 | source_free_projected_proton_role_subset+electron_flow | 1 | m_csa:256 |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_axis_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free row-specific mechanism/event-axis features before any deployable Lever 2 claim. |
| current_retained_oos_source_free_event_axis_rows | 132 | 0 | 132 | These are rows retained by geometry/fold where event-axis mechanism evidence can add abstention value. |
| best_marginal_axis_source_free_fields | 9 | 4 | 5 | The best marginal event-axis fields must exist as source-free deployment-valid row features on the current split, not only as M-CSA train/cal research fields. |

## Priority Rows

| row | current score | baseline score | added-axis score | marginal |
| --- | ---: | ---: | ---: | --- |
| m_csa:17 | 0.45885 | 4.0 | 9.0 | False |
| m_csa:59 | 0.60775 | 5.0 | 0.0 | False |
| m_csa:85 | 0.49955 | 4.0 | 0.0 | False |
| m_csa:194 | 0.4559 | 4.0 | 5.0 | False |
| m_csa:222 | 0.52675 | 5.0 | 5.0 | False |
| m_csa:256 | 0.61925 | 0.0 | 0.0 | True |
| m_csa:312 | 0.5714 | 3.0 | 0.0 | True |

- Best marginal primary-control rows requiring explicit control treatment: m_csa:133

| control row | baseline score | added-axis score | baseline rule | added rule |
| --- | ---: | ---: | --- | --- |
| m_csa:133 | 3.0 | 3.0 | high 3.0 | low 3.0 |

## Decision

- Genuinely new axis adds beyond projected subset before primary control: True
- Genuinely new axis adds beyond projected subset under primary-safe control: False
- Best marginal axis primary LOO control passes: False
- Primary-safe marginal signal requires below-90% primary floor: True
- Adds integrated operating-point value beyond current surface: False
- Source-free current split operating point measurable: False
- Deployable now: False
- Research-only: True
- Next gate: Treat the current bond-change marginal signal as research-only until a source-free current-split event-axis surface preserves all primary controls. The smallest smoke tranche remains the 34 current primary rows plus the best marginal current-retained OOS rows, with the primary-control abstained rows explicitly checked as controls.

## Interpretation

- Best marginal axis source_free_projected_proton_role_subset+bond_change adds 2 current-retained OOS catches before primary control, while the best primary-safe axis adds 0.
- Research-only primary-safe negative: a genuinely new event axis has local marginal signal before the primary control, but no projected-subset-plus-axis surface keeps the primary leave-one-out control while adding marginal current-retained OOS catches beyond the projected subset.
- Do not promote the bond-change marginal axis yet. Materialize source-free current-split event-axis evidence for the current primary rows, the marginal OOS rows, and the primary-control abstained rows, then rerun this primary-safe frontier.
