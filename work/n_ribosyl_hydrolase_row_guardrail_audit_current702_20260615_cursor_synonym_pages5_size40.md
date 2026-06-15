# N-ribosyl hydrolase cursor batch row guardrail audit

Run: 2026-06-15T16:52:06Z

Artifact: `artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_cursor_synonym_pages5_size40.json`
Source preview: `artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_cursor_synonym_pages5_size40_current702_20260615.json`

## Result

- Status: `row_guardrails_pass_and_batch_gate_passed_ready_for_explicit_apply`.
- Audited labels: 150.
- Unique labels: 150.
- Problem rows: 0.
- Batch gate: 150 / 150 clean admits; passed: True.
- Mechanism axes: {'active_site_motif_or_residue_role': 143, 'cofactor_or_cosubstrate': 148, 'domain_or_family_profile': 150, 'rhea_reaction_or_participant_pattern': 150}.

## Guardrails

- EC/name/prose stay excluded/review-only and are not predictive evidence.
- Predictive evidence is empty for every audited row.
- Counted non-EC mechanism axes require domain/family plus Rhea reaction/participant evidence.
- This audit does not mutate registries or authorize apply by itself.
