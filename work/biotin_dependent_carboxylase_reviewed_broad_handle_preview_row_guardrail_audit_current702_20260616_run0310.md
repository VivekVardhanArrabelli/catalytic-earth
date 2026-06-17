# Bronze Preview Row Guardrail Audit

Run: 2026-06-17T03:17:27Z
Preview: `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_current702_20260616_run0310.json`

## Result

- Status: `row_guardrail_audit_passed`.
- Preview applied rows audited: 41.
- Problem rows: 0.
- Fingerprints: {'biotin_dependent_carboxylase': 41}.
- Source tiers: {'source_tier_0': 41}.
- Mechanism axes: {'active_site_motif_or_residue_role': 39, 'cofactor_or_cosubstrate': 41, 'domain_or_family_profile': 41, 'rhea_reaction_or_participant_pattern': 41}.

## Guardrails

- Registry written: False.
- Frozen current702 written: False.
- Predictive evidence required empty: True.

## Next Action

- Apply is allowed only if this audit has 0 problem rows and the preview also passes dedup, novelty, cap, source-trust, leakage, and batch-size gates.
