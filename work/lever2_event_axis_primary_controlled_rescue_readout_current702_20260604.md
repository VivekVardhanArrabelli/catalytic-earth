# Lever 2 Event-Axis Primary-Controlled Rescue Readout

- Artifact: `v3_lever2_event_axis_primary_controlled_rescue_readout_current702_20260604`
- Status: `lever2_event_axis_primary_controlled_rescue_readout_research_only_primary_controlled_marginal_axis_signal_source_free_gap`
- Created UTC: `2026-06-04T21:59:18Z`

## Measured Result

- Baseline projected subset catches 5/13 current-retained overlap rows under primary-controlled selection.
- Best primary-controlled pair: `source_free_projected_proton_role_subset+bond_change` catches 7/13 current-retained rows, with 2 marginal catches.
- Target selections passing primary control: 21/21.

## Primary-Controlled Frontier

| added axis | retained OOS caught | marginal caught | target rules passing primary control | marginal rows |
| --- | ---: | ---: | ---: | --- |
| bond_change | 7/13 | 2 | 21/21 | m_csa:256, m_csa:312 |
| electron_flow | 6/13 | 1 | 21/21 | m_csa:256 |
| proton_transfer | 5/13 | 0 | 21/21 | none |
| event_topology | 5/13 | 0 | 21/21 | none |
| active_site_locator_count | 5/13 | 0 | 21/21 | none |
| confidence_metadata | 5/13 | 0 | 21/21 | none |
| all_priority_event_axes | 5/13 | 0 | 21/21 | none |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_axis_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free row-specific mechanism/event-axis features before any deployable Lever 2 claim. |
| current_retained_oos_source_free_event_axis_rows | 132 | 0 | 132 | These are rows retained by geometry/fold where event-axis mechanism evidence can add abstention value. |
| best_primary_controlled_axis_source_free_fields | 9 | 4 | 5 | The best primary-controlled event-axis fields must exist as source-free deployment-valid row features on the current split, not only as M-CSA train/cal research fields. |
| best_primary_controlled_axis_mechanism_primary_control_rows | 4 | 0 | 4 | The rescue signal must keep known in-atlas mechanism primary controls, including the prior failed control row, when the event-axis surface is materialized source-free. |

## Priority Rows

| row | current score | baseline score | added-axis score | marginal | added rule |
| --- | ---: | ---: | ---: | --- | --- |
| m_csa:17 | 0.45885 | 4.0 | 9.0 | False | low 0.0 |
| m_csa:59 | 0.60775 | 5.0 | 0.0 | False | low 0.0 |
| m_csa:85 | 0.49955 | 4.0 | 0.0 | False | low 0.0 |
| m_csa:194 | 0.4559 | 4.0 | 5.0 | False | low 0.0 |
| m_csa:222 | 0.52675 | 5.0 | 5.0 | False | low 0.0 |
| m_csa:256 | 0.61925 | 0.0 | 0.0 | True | low 0.0 |
| m_csa:312 | 0.5714 | 3.0 | 0.0 | True | low 0.0 |

- Primary-controlled marginal rows: m_csa:256, m_csa:312
- Mechanism primary-control rows requiring source-free materialization: m_csa:6, m_csa:133, m_csa:147, m_csa:186
- Smallest primary-controlled rescue smoke tranche: 40 rows.
- Existing source-free coverage for that tranche: 1/40 rows; event-axis linker coverage: 0/40.

## Decision

- Genuinely new axis adds beyond projected subset under primary control: True
- Adds train/cal primary-controlled local value beyond current surface: True
- Adds integrated operating-point value beyond current surface: False
- Source-free current split operating point measurable: False
- Deployable now: False
- Research-only: True
- Next gate: Do not promote yet. Materialize source-free current-split event-axis rows for the current primary controls plus the mechanism primary-control rows and primary-controlled marginal OOS rows, then rerun this rescue readout against the current split before any heldout or deployment claim.

## Interpretation

- Primary-controlled source_free_projected_proton_role_subset+bond_change catches 7/13 current-retained overlap rows, with 2 marginal catches beyond the projected subset.
- Research-only signal: stricter primary-control-aware threshold selection recovers a genuine bond-change/event-axis marginal signal while retaining all calibration primary controls, but the current split still lacks source-free event-axis rows for primary retention and retained-OOS measurement.
- Materialize source-free current-split event-axis rows for the 34 current primary rows, the four mechanism primary-control rows, and the primary-controlled marginal OOS rows before making any deployment or heldout claim.
