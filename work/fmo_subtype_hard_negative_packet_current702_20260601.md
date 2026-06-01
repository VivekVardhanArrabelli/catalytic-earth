# FMO Subtype Hard-Negative Packet - current702

Run: 2026-06-01T09:17:00Z

Review-only FMO subtype and hard-negative packet built from frozen current702
family-panel readouts, source checks, and local adjudications. It does not
authorize a family promotion.

## Status

- fmo_subtype_hard_negative_packet_ready_review_only
- Rows: 5
- Current primary FMO rows: 0
- Secondary or future support rows: 3
- Hard-negative or boundary rows: 2
- Import-ready rows: 0
- Registry-edit-allowed rows: 0
- Geometry or coordinate blocked rows: 2

## Rows

| row | subtype lane | current role | readout | decision | next action |
| --- | --- | --- | --- | --- | --- |
| m_csa:131 | canonical_phbh_like_single_component_fmo | secondary_probe | non_abstained_at_research_threshold; combined=0.63575 | keep_as_secondary_probe_support | Use as source-checked FMO support only after subtype, coordinate, hard-negative, and expert-admission gates are satisfied. |
| m_csa:132 | two_component_fmnh2_sulfur_monooxygenase | current702_m_csa_geometry_gap | not_score_complete_for_primary_channel | repair_geometry_before_fmo_use | Repair or materialize predicted active-site geometry before predicted-fold lookup or FMO subtype evidence use. |
| m_csa:551 | phenol_monooxygenase_future_support | future_support_review_only | non_abstained_at_research_threshold; combined=0.60245 | future_support_only_no_registry_change | Keep as future FMO support and pair with hard negatives before any promotion reconsideration. |
| m_csa:973 | two_component_fmnh2_sulfur_monooxygenase | future_support_review_only | abstained_at_research_threshold; combined=0.41 | mechanism_clean_but_coordinate_blocked_and_threshold_abstained | Carry as mechanism-clean support only; keep coordinate caveat and no label, registry, or import change. |
| m_csa:750 | radical_flavin_fe_s_boundary_negative | oos_boundary_negative | non_abstained_at_research_threshold; combined=0.4995 | keep_as_oos_boundary_negative_for_current_fmo_scope | Use as review-only hard-negative/boundary evidence, not as FMO, cobalamin, radical-SAM, or flavin-family promotion support. |

## Requirements Before FMO Promotion

- Subtype lanes must distinguish PHBH-like single-component monooxygenases from two-component FMNH2 sulfur monooxygenases and phenol monooxygenases.
- Hard negatives must include flavin dehydrogenase/reductase, radical flavin Fe-S, and generic metal/hydrolase false-positive contexts.
- All countable support rows need coordinate-clean active-site materialization and source-backed cofactor/redox-partner evidence.
- Future import requires label-factory gate, duplicate/leakage screen, registry summary refresh, and explicit expert acceptance.

## Interpretation

- The FMO panel remains review-only: no row is import-ready or registry-edit-ready, and current support is subtype- and coordinate-blocked.
- Next action: repair `m_csa:132` geometry and build source-backed subtype/hard-negative sidecars before any FMO promotion reconsideration.

## Guardrails

- Review-only packet. No labels, registries, ontologies, imports, thresholds,
  training data, source fetching, or production scoring changed.
