# Glycoside hydrolase mechanism-handle scout

Run: 2026-06-13T16:07:13Z

Entries examined: 240.
Fetch failures: 0.
Wire next lane: True.

| Handle | Count |
| --- | ---: |
| acid_base_or_nucleophile_context | 221 |
| active_or_binding_site_context | 230 |
| boundary_signal | 6 |
| glycosidase_family_text | 239 |
| glycoside_hydrolysis_reaction | 240 |
| likely_wireable_by_non_ec_handles | 178 |
| non_scope_ec_boundary | 7 |
| registry_new | 194 |
| rhea_cross_reference | 83 |

## Guardrails

- EC/name/keyword/Rhea/feature handles were used only for scope/admission scouting.
- `predictive_evidence` remains empty; no labels or registry writes were emitted.
- Hold transferase, transglycosylase, phosphorylase, lyase, isomerase, esterase/peptidase/nuclease, side-EC, EC-only, and multi-fingerprint rows.

## Next action

- If wire_next_lane is true, add glycoside_hydrolase fingerprint/ontology node, disambiguation guards/tests, 35fp OOS preregistration, non-destructive preview, and gated apply with cap 150.
