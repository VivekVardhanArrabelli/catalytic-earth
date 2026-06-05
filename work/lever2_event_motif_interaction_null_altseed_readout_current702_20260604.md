# Lever 2 Event-Motif Interaction Null Readout

- Artifact: `v3_lever2_event_motif_interaction_null_altseed_readout_current702_20260604`
- Status: `lever2_event_motif_interaction_null_readout_research_only_event_motif_weak_marginal_not_distinguishable_from_null`
- Created UTC: `2026-06-05T00:48:34Z`

## Measured Result

- Baseline projected subset catches 5/13 current-retained overlap rows.
- Best motif surface: `source_free_projected_proton_role_subset+multi_event_bond_topology` catches 6/13 rows, with 1 marginal catch beyond the projected subset.
- Motif null over 128 permutations and 6 motif axes: p95 6, max 8, empirical p-value 0.992248.

## Motif Frontier

| motif axis | retained OOS caught | marginal caught | marginal rows |
| --- | ---: | ---: | --- |
| multi_event_bond_topology | 6/13 | 1 | m_csa:256 |
| bond_proton_coupling | 6/13 | 1 | m_csa:221 |
| proton_electron_coupling | 5/13 | 0 | none |
| multi_event_electron_topology | 5/13 | 0 | none |
| bond_electron_coupling | 5/13 | 0 | none |
| all_three_event_coupling | 5/13 | 0 | none |

## Top Null Permutations

| permutation | best null motif | total catches | marginal catches | marginal rows |
| ---: | --- | ---: | ---: | --- |
| 84 | source_free_projected_proton_role_subset+multi_event_electron_topology | 13 | 8 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 17 | source_free_projected_proton_role_subset+multi_event_bond_topology | 12 | 7 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:312 |
| 82 | source_free_projected_proton_role_subset+multi_event_bond_topology | 12 | 7 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:256, m_csa:312 |
| 55 | source_free_projected_proton_role_subset+bond_proton_coupling | 12 | 7 | m_csa:23, m_csa:25, m_csa:221, m_csa:246, m_csa:253, m_csa:256, m_csa:312 |
| 50 | source_free_projected_proton_role_subset+proton_electron_coupling | 11 | 6 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:256, m_csa:312 |
| 76 | source_free_projected_proton_role_subset+multi_event_bond_topology | 11 | 6 | m_csa:23, m_csa:70, m_csa:221, m_csa:246, m_csa:253, m_csa:312 |
| 27 | source_free_projected_proton_role_subset+bond_proton_coupling | 11 | 6 | m_csa:23, m_csa:25, m_csa:70, m_csa:221, m_csa:246, m_csa:312 |
| 34 | source_free_projected_proton_role_subset+bond_proton_coupling | 11 | 6 | m_csa:23, m_csa:25, m_csa:70, m_csa:246, m_csa:253, m_csa:312 |
| 61 | source_free_projected_proton_role_subset+proton_electron_coupling | 10 | 5 | m_csa:23, m_csa:70, m_csa:221, m_csa:253, m_csa:256 |
| 26 | source_free_projected_proton_role_subset+multi_event_electron_topology | 10 | 5 | m_csa:25, m_csa:70, m_csa:221, m_csa:253, m_csa:312 |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_event_motif_rows | 34 | 0 | 34 | The current primary retention gate must be measured on source-free event-motif features before any promotable Lever 2 operating-point claim. |
| current_retained_oos_source_free_event_motif_rows | 132 | 0 | 132 | These geometry/fold-retained OOS rows are where source-free mechanism motifs would need to add abstention value beyond the current surface. |
| best_event_motif_source_free_fields | 2 | 0 | 2 | The best motif fields are derived research features here; they must be materialized from source-free event evidence on the current split before deployment use. |

- Best motif marginal rows: m_csa:256

## Decision

- Best event motif: `source_free_projected_proton_role_subset+multi_event_bond_topology`
- Event motif adds beyond projected subset: True
- Observed marginal exceeds motif-null p95: False
- Null control supports event-motif signal: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Negative: True
- Next gate: Do not promote event-motif interactions from this result. If source-free current-split event rows are materialized, rerun this motif-null readout and require marginal catches above the empirical null p95 before heldout or deployment work.

## Interpretation

- Best event motif source_free_projected_proton_role_subset+multi_event_bond_topology catches 6/13 current-retained overlap rows with 1 marginal catch; motif-null p95 is 6.
- Measured research-only negative: coupled event-motif features do not produce marginal current-retained OOS signal distinguishable from deterministic motif-field assignment nulls.
- Do not spend Lever 2 effort on event-motif interactions until source-free current-split event rows exist; then rerun this motif-null readout before any heldout or deployment claim.
