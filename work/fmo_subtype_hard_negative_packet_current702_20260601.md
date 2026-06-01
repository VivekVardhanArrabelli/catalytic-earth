# FMO Subtype And Hard-Negative Packet - current702

Run: 2026-06-01T09:50:41Z

Review-only FMO subtype and hard-negative packet built from frozen current702 family-panel readouts, source checks, and local adjudications. It does not authorize a family promotion.

## Status

- fmo_subtype_hard_negative_packet_ready_review_only
- Rows: 5
- Secondary/future support rows: 4
- Hard-negative or boundary rows: 1
- Geometry/coordinate blocked rows: 1

## Rows

| row | role | subtype lane | research status | combined | decision |
| --- | --- | --- | --- | ---: | --- |
| m_csa:131 | secondary_probe | canonical_phbh_like_single_component_fmo | non_abstained_at_research_threshold | 0.63575 | keep_as_secondary_probe_support |
| m_csa:132 | secondary_probe_geometry_repaired_review_only | two_component_fmnh2_sulfur_monooxygenase | non_abstained_at_research_threshold | 0.53865 | keep_as_secondary_fmo_support_after_geometry_repair_no_primary_promotion |
| m_csa:551 | future_support_review_only | phenol_monooxygenase_future_support | non_abstained_at_research_threshold | 0.60245 | future_support_only_no_registry_change |
| m_csa:973 | future_support_review_only | two_component_fmnh2_sulfur_monooxygenase | abstained_at_research_threshold | 0.41 | mechanism_clean_but_coordinate_blocked_and_threshold_abstained |
| m_csa:750 | oos_boundary_negative | radical_flavin_fe_s_boundary_negative | non_abstained_at_research_threshold | 0.4995 | keep_as_oos_boundary_negative_for_current_fmo_scope |

## Interpretation

- m_csa:132 is now score-complete and source-checked as secondary FMO support, while m_csa:973 remains coordinate/threshold blocked and m_csa:750 remains the radical flavin/Fe-S boundary negative.
- Keep all FMO rows review-only; next clear coordinate/subtype/hard-negative and expert-admission blockers before any primary FMO promotion discussion.

## Guardrails

- Review-only packet. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.
