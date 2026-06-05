# Lever 2 Event-Axis Primary-Controlled Null Readout

- Artifact: `v3_lever2_event_axis_primary_controlled_null_readout_current702_20260604`
- Status: `lever2_event_axis_primary_controlled_null_readout_research_only_null_controlled_marginal_signal_not_distinguishable_from_null`
- Created UTC: `2026-06-04T23:47:01Z`

## Measured Result

- Observed best pair: `source_free_projected_proton_role_subset+bond_change` with 7/13 current-retained catches and 2 marginal catches beyond the projected subset.
- Observed marginal rows: m_csa:256, m_csa:312.
- Null distribution over 128 deterministic permutations and 6 added axes: min 0, median 4, p90 6, p95 6, max 8.
- Priority event-axis null p95: 6 with empirical p-value 0.844961.
- Empirical p-value for null max marginal catches >= observed: 0.96124 (123 permutations).

## Top Null Permutations

| permutation | best null axis | total catches | marginal catches | marginal rows |
| ---: | --- | ---: | ---: | --- |
| 34 | source_free_projected_proton_role_subset+active_site_locator_count | 13 | 8 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 103 | source_free_projected_proton_role_subset+event_topology | 12 | 7 | m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 20 | source_free_projected_proton_role_subset+bond_change | 12 | 7 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:312 |
| 118 | source_free_projected_proton_role_subset+bond_change | 12 | 7 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256 |
| 27 | source_free_projected_proton_role_subset+confidence_metadata | 11 | 6 | m_csa:25, m_csa:70, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 46 | source_free_projected_proton_role_subset+confidence_metadata | 11 | 6 | m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256 |
| 48 | source_free_projected_proton_role_subset+confidence_metadata | 11 | 6 | m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:312 |
| 68 | source_free_projected_proton_role_subset+confidence_metadata | 11 | 6 | m_csa:23, m_csa:25, m_csa:221, m_csa:253, m_csa:256, m_csa:312 |
| 71 | source_free_projected_proton_role_subset+confidence_metadata | 11 | 6 | m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 14 | source_free_projected_proton_role_subset+all_priority_event_axes | 11 | 6 | m_csa:23, m_csa:25, m_csa:221, m_csa:246, m_csa:253, m_csa:256 |

## Decision

- Observed marginal signal: True
- Observed marginal exceeds null p95: False
- Null control supports genuinely new axis signal: False
- Priority event-axis null supports signal: False
- Adds integrated operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Negative: True
- Next gate: Do not promote Lever 2 from this result. If source-free event-axis rows are materialized, rerun the primary-controlled frontier plus this null control and require an observed marginal count above the empirical null p95 before any heldout or deployment claim.

## Interpretation

- Observed primary-controlled marginal catches: 2; empirical null p95: 6; empirical p-value: 0.96124; priority-event null p95: 6.
- Research-only measured negative: the observed primary-controlled marginal signal is not distinguishable from deterministic added-axis assignment nulls under the same split and primary-control discipline.
- Use this as the promotion gate for future source-free materialization: rerun on materialized current-split rows and require null-controlled marginal signal before heldout or deployment work.
