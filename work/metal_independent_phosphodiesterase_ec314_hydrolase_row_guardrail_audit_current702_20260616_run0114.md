# Bronze Preview Row Guardrail Audit

Run: 2026-06-16T01:28:58Z
Preview: `artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window0_120_current702_20260616_run0114.json`

## Result

- Status: `row_guardrail_audit_passed`.
- Preview applied rows audited: 17.
- Problem rows: 0.
- Fingerprints: {'metal_independent_phosphodiesterase': 17}.
- Source tiers: {'source_tier_0': 17}.
- Mechanism axes: {'active_site_motif_or_residue_role': 2, 'cofactor_or_cosubstrate': 13, 'domain_or_family_profile': 17, 'rhea_reaction_or_participant_pattern': 17}.

## Guardrails

- Registry written: False.
- Frozen current702 written: False.
- Predictive evidence required empty: True.

## Next Action

- Apply is allowed only if this audit has 0 problem rows and the preview also passes dedup, novelty, cap, source-trust, leakage, and batch-size gates.
