# Bronze Preview Row Guardrail Audit

Run: 2026-06-16T13:17:49Z
Preview: `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset90_size30_current702_20260616_run1302.json`

## Result

- Status: `row_guardrail_audit_passed`.
- Preview applied rows audited: 30.
- Problem rows: 0.
- Fingerprints: {'metal_independent_phosphodiesterase': 30}.
- Source tiers: {'source_tier_2': 30}.
- Mechanism axes: {'cofactor_or_cosubstrate': 30, 'domain_or_family_profile': 30, 'rhea_reaction_or_participant_pattern': 30}.

## Guardrails

- Registry written: False.
- Frozen current702 written: False.
- Predictive evidence required empty: True.

## Next Action

- Apply is allowed only if this audit has 0 problem rows and the preview also passes dedup, novelty, cap, source-trust, leakage, and batch-size gates.
