# Lever 2 Event-Axis Current-Extended Frontier Readout

- Artifact: `v3_lever2_event_axis_current_extended_frontier_readout_current702_20260604`
- Status: `lever2_event_axis_current_extended_frontier_readout_research_only_current_extended_axis_signal`
- Created UTC: `2026-06-04T18:52:09Z`

## Measured Result

- Best local event axis: `source_free_projected_proton_role_subset` catches 5/13 current-retained overlap rows beyond the fixed geometry/fold surface.
- The best-axis OR gate abstains 13/21 current-overlap OOS rows.
- Best paired-axis frontier: `source_free_projected_proton_role_subset+bond_change` catches 7/13 current-retained overlap rows.
- Current primary retention on the active 34-row split remains unmeasurable: 0/34 valid current-primary rows have calibration-split mechanism features.

## Axis Frontier

| axis | source-free status | cal primary retained | cal OOS abstained | retained OOS caught | OR abstained |
| --- | --- | ---: | ---: | ---: | ---: |
| source_free_projected_proton_role_subset | source_free_compatible_proxy | 4/4 | 9/28 | 5/13 | 13/21 |
| bond_change | requires_new_source_free_axis | 4/4 | 6/28 | 4/13 | 12/21 |
| proton_transfer | partially_supported_by_event_axis_linkers | 4/4 | 5/28 | 2/13 | 10/21 |
| electron_flow | requires_new_source_free_axis | 4/4 | 1/28 | 1/13 | 9/21 |
| event_topology | requires_new_source_free_axis | 4/4 | 1/28 | 0/13 | 8/21 |
| active_site_locator_count | requires_source_free_locator_coverage | 4/4 | 3/28 | 3/13 | 11/21 |
| confidence_metadata | research_only_metadata_axis | 4/4 | 1/28 | 0/13 | 8/21 |
| all_priority_event_axes | requires_multi_axis_source_free_materialization | 4/4 | 4/28 | 2/13 | 10/21 |

## Axis Pair Frontier

| axis pair | source-free status | cal primary retained | cal OOS abstained | retained OOS caught | OR abstained |
| --- | --- | ---: | ---: | ---: | ---: |
| source_free_projected_proton_role_subset+bond_change | requires_source_free_materialization | 4/4 | 13/28 | 7/13 | 15/21 |
| source_free_projected_proton_role_subset+all_priority_event_axes | requires_source_free_materialization | 4/4 | 12/28 | 6/13 | 14/21 |
| source_free_projected_proton_role_subset+electron_flow | requires_source_free_materialization | 4/4 | 10/28 | 6/13 | 14/21 |
| bond_change+active_site_locator_count | requires_source_free_materialization | 4/4 | 8/28 | 6/13 | 14/21 |
| source_free_projected_proton_role_subset+event_topology | requires_source_free_materialization | 4/4 | 10/28 | 5/13 | 13/21 |
| source_free_projected_proton_role_subset+confidence_metadata | requires_source_free_materialization | 4/4 | 10/28 | 5/13 | 13/21 |
| bond_change+proton_transfer | requires_source_free_materialization | 4/4 | 10/28 | 5/13 | 13/21 |
| source_free_projected_proton_role_subset+proton_transfer | requires_source_free_materialization | 4/4 | 9/28 | 5/13 | 13/21 |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_axis_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free row-specific mechanism/event-axis features before any deployable Lever 2 claim. |
| current_retained_oos_source_free_event_axis_rows | 132 | 0 | 132 | These are rows retained by geometry/fold where event-axis mechanism evidence can add abstention value. |
| best_axis_source_free_materialization_fields | 4 | 4 | 0 | The best local axis fields must exist as source-free deployment-valid row features on the current split, not only as M-CSA train/cal research fields. |

## Decision

- Local event-axis signal beyond current surface: True
- Event-axis pair adds beyond best single axis: True
- Adds integrated operating-point value beyond current surface: False
- Source-free current split operating point measurable: False
- Deployable now: False
- Research-only: True
- Next gate: Materialize source-free event-axis rows on the current split, starting with 34 primary retention-gate rows and 132 current-retained OOS rows; prioritize the best single/pair frontier fields, then rerun this train/cal frontier.

## Interpretation

- Best event axis source_free_projected_proton_role_subset catches 5/13 current-retained overlap rows.
- Research-only local signal: simple mechanism event axes add abstentions on the current extended OOS overlap, but current primary source-free coverage is absent so no integrated operating-point value can be claimed.
- Materialize split-aligned source-free event-axis fields for the current primary and current-retained OOS rows before any deployment or heldout claim.
