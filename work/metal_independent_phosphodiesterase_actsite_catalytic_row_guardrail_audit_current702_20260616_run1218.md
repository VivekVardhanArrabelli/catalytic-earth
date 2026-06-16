# Bronze Preview Row Guardrail Audit

Run: 2026-06-16T12:35:59Z
Preview: `artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_preview_size40_current702_20260616_run1218.json`

## Result

- Status: `row_guardrail_audit_passed`.
- Preview applied rows audited: 2.
- Problem rows: 0.
- Fingerprints: {'metal_independent_phosphodiesterase': 2}.
- Source tiers: {'source_tier_0': 2}.
- Mechanism axes: {'active_site_motif_or_residue_role': 2, 'cofactor_or_cosubstrate': 2, 'domain_or_family_profile': 2, 'rhea_reaction_or_participant_pattern': 2}.

## Guardrails

- Registry written: False.
- Frozen current702 written: False.
- Predictive evidence required empty: True.

## Next Action

- Apply is allowed only if this audit has 0 problem rows and the preview also passes dedup, novelty, cap, source-trust, leakage, and batch-size gates.
