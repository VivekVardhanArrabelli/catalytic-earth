# Short-Chain Dehydrogenase/Reductase Row Guardrail Audit

Source preview: `artifacts/v3_short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.json`
Artifact: `artifacts/v3_short_chain_dehydrogenase_reductase_row_guardrail_audit_current702_20260615_run2213.json`

## Result

- Audited labels: 100.
- Problem rows: 0.
- Batch gate passed: True (min 100).
- Source tiers: {'source_tier_0': 100}.
- Mechanism axis counts: {'active_site_motif_or_residue_role': 99, 'cofactor_or_cosubstrate': 100, 'domain_or_family_profile': 100, 'rhea_reaction_or_participant_pattern': 100}.

## Guardrails

- All rows bronze: True.
- All rows automation_curated: True.
- All rows uniprot namespace: True.
- Predictive evidence empty: True.
- All rows source_tier_0: True.
- Three or more non-EC axes: True.
- EC never counted as mechanism axis: True.

## Next Action

- Run the SDR source script with --apply --reuse-preview against the source preview so frozen current702 SHA is printed before/after; then rerun validation, coverage, novelty, and source-contract tests.
