# Bronze Preview Row Guardrail Audit

Run: 2026-06-17T01:48:42Z
Preview: `artifacts/v3_biotin_dependent_carboxylase_tier2_source_handle_scout_current702_20260616_run0009.json`

## Result

- Status: `row_guardrail_audit_passed`.
- Preview applied rows audited: 9.
- Problem rows: 0.
- Fingerprints: {'biotin_dependent_carboxylase': 9}.
- Source tiers: {'source_tier_2': 9}.
- Mechanism axes: {'active_site_motif_or_residue_role': 9, 'cofactor_or_cosubstrate': 9, 'domain_or_family_profile': 9, 'rhea_reaction_or_participant_pattern': 9}.

## Guardrails

- Registry written: False.
- Frozen current702 written: False.
- Predictive evidence required empty: True.

## Next Action

- Apply is allowed only if this audit has 0 problem rows and the preview also passes dedup, novelty, cap, source-trust, leakage, and batch-size gates.
