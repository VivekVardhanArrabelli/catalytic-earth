# GHKL histidine kinase mechanism-handle scout

Run: 2026-06-13T16:03:57Z

Entries examined: 2.
Fetch failures: 0.
Wire next lane: False.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 2 |
| atp_adp_phosphate_context | 1 |
| boundary_signal | 1 |
| histidine_family_text | 1 |
| likely_wireable_by_non_ec_handles | 1 |
| mg_or_atp_context | 1 |
| phosphohistidine_context | 1 |
| registry_new | 2 |

## Guardrails

- EC and names were used only for source scope and admission-handle scouting.
- `predictive_evidence` remains empty; no labels or registry writes were emitted.
- ePK production no-go is not reopened; this scouts GHKL/two-component histidine kinase only.

## Next action

- If wire_next_lane is true, add ghkl_histidine_kinase fingerprint, map ontology ghkl child, add disambiguation guards/tests, re-freeze 35fp OOS preregistration, preview, and apply only if novelty/trust/cap gates pass.
