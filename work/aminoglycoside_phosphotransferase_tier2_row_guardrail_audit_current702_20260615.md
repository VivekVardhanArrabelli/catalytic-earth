# Aminoglycoside Phosphotransferase Tier-2 Row Guardrail Audit

Source preview: `artifacts/v3_aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.json`
Artifact: `artifacts/v3_aminoglycoside_phosphotransferase_tier2_row_guardrail_audit_current702_20260615.json`

## Result

- Audited labels: 150.
- Problem rows: 0.
- Batch gate passed: True (min 150).
- Source tiers: {'source_tier_2': 150}.
- Mechanism axis counts: {'active_site_motif_or_residue_role': 150, 'cofactor_or_cosubstrate': 150, 'domain_or_family_profile': 150, 'rhea_reaction_or_participant_pattern': 150}.

## Guardrails

- All rows bronze: True.
- All rows automation_curated: True.
- All rows uniprot namespace: True.
- Predictive evidence empty: True.
- All rows source_tier_2: True.
- Three or more non-EC mechanism axes: True.
- EC never counted as mechanism axis: True.

## Next Action

- Run the APH source script with --apply --reuse-preview against the source preview so frozen current702 SHA is printed before/after; then rerun validation, coverage, novelty, and source-contract tests.
