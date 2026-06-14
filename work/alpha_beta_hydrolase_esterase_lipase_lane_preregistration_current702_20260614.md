# Alpha/beta Hydrolase Esterase/Lipase Lane Preregistration - 2026-06-14

Status: design_only_no_labels_no_registry_write.

Source artifact:
`artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_aldehyde_dehydrogenase_apply.json`.

Preregistration artifact:
`artifacts/v3_alpha_beta_hydrolase_esterase_lipase_lane_preregistration_current702_20260614_post_aldehyde_dehydrogenase_apply.json`.

Why this lane is next:
- The post-ALDH high-yield factory reports no existing runner with >=150 cap room.
- The top remaining lane is `alpha_beta_hydrolase_esterase_lipase`: 6160 reviewed EC 3.1.1 scope rows, 1352 reviewed non-EC corroborated rows, 0.219 estimated non-EC corroboration rate, and 150 projected clean admits under the chemistry-confusable cap.

Mechanism-first contract:
- EC 3.1.1 is scope/admission context only and must never count as a mechanism corroborator.
- Required non-EC handles: esterase/lipase family/name context, Ser-His-Asp/Glu catalytic triad active-site or binding-site context, and Rhea ester hydrolysis participant/equation where available.
- `predictive_evidence` must remain `[]` unless a future leakage-tested source-free feature is explicitly implemented.
- All admission handles stay in `excluded_context`.

Required OOS holds before any apply:
- Protease/amidase rows.
- Glycoside hydrolase/transglycosylase rows.
- Metal hydrolase rows.
- EC-only ester hydrolase rows without active-site, binding-site, family, or Rhea corroboration.
- Multi-fingerprint Ser-His or metal hydrolase rows where the evidence does not resolve the esterase/lipase split.

Next safe action:
Build `scripts/source_alpha_beta_hydrolase_esterase_lipase_family.py`, a fingerprint, ontology node, disambiguation rule, and offline tests from this preregistration. Preview first, then row-audit before any apply.
