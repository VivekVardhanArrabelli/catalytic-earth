# Serine Beta-lactamase Tier-2 Row Guardrail Audit

Run: 2026-06-16T00:32:20Z

- Source preview: `artifacts/v3_serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.json`.
- Audited labels: 106.
- Problem rows: 0.
- Batch gate passed: True.
- Required axes: active_site_motif_or_residue_role, domain_or_family_profile, rhea_reaction_or_participant_pattern.
- Source tiers: {'source_tier_2': 106}.
- Mechanism axis counts: {'active_site_motif_or_residue_role': 106, 'domain_or_family_profile': 106, 'rhea_reaction_or_participant_pattern': 106}.

## Next action

- Run the serine beta-lactamase source script with --apply --reuse-preview against the source preview so frozen current702 SHA is printed before/after; then rerun validation, coverage, novelty, and source-contract tests.
