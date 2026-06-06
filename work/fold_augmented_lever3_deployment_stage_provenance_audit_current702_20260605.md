# Fold-Augmented Lever 3 Deployment Stage Provenance Audit - current702

Run: 2026-06-05T12:18:38Z

Stage-provenance audit for the current Lever 3 operator manifest. It verifies that every row-level stage source artifact referenced by the manifest is present in the bounded, guardrail-clean deployment-contract lineage.

## Status

- fold_augmented_lever3_deployment_stage_provenance_audit_passed
- Stage provenance clean: True
- Stage sources covered: True
- Fixed-threshold scoring closure available now: False
- Stage provenance violations: []

## Counts

- Manifest rows abstain/route: 21/21
- Stage-source artifacts covered: 5/5
- Stage-source artifacts guardrail-clean: 5/5
- Direct source hashes current: 2/2
- Lineage source hashes current: 43/43
- Unsafe action rows: 0
- Forced mechanism-label rows: 0
- Forbidden-field rows: 0
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204

## Stage Sources

| stage source artifact | manifest rows | lineage depth | guardrail violations |
| --- | ---: | ---: | --- |
| v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | 10 | 3 | [] |
| v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | 7 | 3 | [] |
| v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605 | 1 | 3 | [] |
| v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 | 2 | 3 | [] |
| v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605 | 1 | 3 | [] |

## Stage Provenance Checks

| check | passed |
| --- | ---: |
| operator_manifest_audit_passed | True |
| deployment_contract_lineage_audit_passed | True |
| direct_source_hashes_current | True |
| lineage_source_hashes_current | True |
| all_manifest_stage_sources_present | True |
| all_manifest_stage_sources_guardrail_clean | True |
| stage_source_row_counts_match_manifest | True |
| manifest_has_no_unsafe_actions | True |
| manifest_has_no_forbidden_fields_or_rule_selection_rows | True |
| operating_point_metrics_match_lineage | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use the operator manifest with its lineage-covered stage sources for abstain/route actions only; keep fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing operator manifest and lineage artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 manifest stage provenance is lineage-covered.
- 5 unique stage-source artifacts cover 21 manifest rows with 0 missing lineage artifacts.
- Use the manifest only for abstain/route actions; stage sources are covered by clean lineage.
