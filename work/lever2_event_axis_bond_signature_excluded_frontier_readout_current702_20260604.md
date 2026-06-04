# Lever 2 Event-Axis Signature-Excluded Frontier Readout

- Artifact: `v3_lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604`
- Status: `lever2_event_axis_signature_excluded_frontier_readout_research_only_signature_excluded_marginal_axis_signal_source_free_gap`
- Created UTC: `2026-06-04T23:02:41Z`

## Measured Result

- Baseline projected subset catches 5/13 current-retained overlap rows under signature-excluded selection.
- Best signature-excluded pair: `source_free_projected_proton_role_subset+electron_flow` catches 6/13 current-retained rows, with 1 marginal catches.
- Same-signature OOS exclusions for the best pair: 66 rows across 18 targets.

## Signature-Excluded Frontier

| added axis | retained OOS caught | marginal caught | rules passing primary control | same-signature rows excluded | marginal rows |
| --- | ---: | ---: | ---: | ---: | --- |
| electron_flow | 6/13 | 1 | 21/21 | 66 | m_csa:256 |
| bond_change | 5/13 | 0 | 21/21 | 66 | none |
| proton_transfer | 5/13 | 0 | 21/21 | 66 | none |
| event_topology | 5/13 | 0 | 21/21 | 66 | none |
| active_site_locator_count | 5/13 | 0 | 21/21 | 66 | none |
| confidence_metadata | 5/13 | 0 | 21/21 | 66 | none |
| all_priority_event_axes | 5/13 | 0 | 21/21 | 66 | none |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_axis_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free row-specific mechanism/event-axis features before any deployable Lever 2 claim. |
| current_retained_oos_source_free_event_axis_rows | 132 | 0 | 132 | These are rows retained by geometry/fold where event-axis mechanism evidence can add abstention value. |
| best_signature_excluded_axis_source_free_fields | 6 | 4 | 2 | The best signature-excluded event-axis fields must exist as source-free deployment-valid row features on the current split, not only as M-CSA train/cal research fields. |

## Priority Rows

| row | current score | baseline score | added-axis score | marginal | same-signature OOS excluded |
| --- | ---: | ---: | ---: | --- | --- |
| m_csa:17 | 0.45885 | 4.0 | 0.0 | False | none |
| m_csa:59 | 0.60775 | 5.0 | 3.0 | False | m_csa:49, m_csa:85, m_csa:224, m_csa:256, m_csa:312 |
| m_csa:85 | 0.49955 | 4.0 | 0.0 | False | m_csa:49, m_csa:59, m_csa:224, m_csa:256, m_csa:312 |
| m_csa:194 | 0.4559 | 4.0 | 2.0 | False | m_csa:70, m_csa:78, m_csa:101, m_csa:263, m_csa:317 |
| m_csa:222 | 0.52675 | 5.0 | 0.0 | False | m_csa:2 |
| m_csa:256 | 0.61925 | 0.0 | 4.0 | True | m_csa:49, m_csa:59, m_csa:85, m_csa:224, m_csa:312 |

- Signature-excluded marginal rows: m_csa:256

## Decision

- Genuinely new axis adds beyond projected subset after signature exclusion: True
- Adds train/cal signature-excluded local value beyond current surface: True
- Adds integrated operating-point value beyond current surface: False
- Source-free current split operating point measurable: False
- Deployable now: False
- Research-only: True
- Next gate: Do not promote yet. Materialize source-free current-split event-axis rows for the current primary controls and the signature-excluded marginal OOS rows, then rerun this signature-excluded readout before any heldout or deployment claim.

## Interpretation

- Signature-excluded source_free_projected_proton_role_subset+electron_flow catches 6/13 current-retained overlap rows, with 1 marginal catches beyond the projected subset.
- Research-only signal: the new event axis still adds marginal current-retained OOS catches after excluding same-signature calibration OOS neighbors, but source-free current-split event-axis rows are still missing.
- Use the signature-excluded marginal rows as the next smoke target only if they remain nonzero; otherwise prioritize new source-free evidence rather than tuning this surface.
