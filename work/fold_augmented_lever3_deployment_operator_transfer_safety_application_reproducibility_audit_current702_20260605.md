# Fold-Augmented Lever 3 Deployment Operator Transfer-Safety Application Reproducibility Audit - current702

Run: 2026-06-05T14:26:28Z

Reproducibility audit for the Lever 3 operator transfer-safety application audit. It rebuilds the application audit from recorded matrix and matrix-reproducibility sources, normalizes only created_utc, and checks source-hash and metric stability.

## Status

- fold_augmented_lever3_deployment_operator_transfer_safety_application_reproducibility_audit_passed
- Transfer-safety application reproducible: True
- Transfer-safety application ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: 7d6f9452b3a49e377c26bc103449e9ab11ee1c0b3c6a2386118fcc160be048f0
- Rebuilt normalized SHA-256: 7d6f9452b3a49e377c26bc103449e9ab11ee1c0b3c6a2386118fcc160be048f0
- Rebuild error: None

## Counts

- Source hashes current: 2/2
- Rebuild difference count: 0
- Application operator rows safe-to-abstain/route: 21/21
- Mechanism-transfer-allowed rows: 0
- Matrix rebuild difference count: 0
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}

## Reproducibility Checks

| check | passed |
| --- | ---: |
| transfer_safety_application_audit_passed | True |
| transfer_safety_application_source_hashes_current | True |
| transfer_safety_application_rebuild_matches_stored_after_created_utc_normalization | True |
| transfer_safety_application_metrics_stable | True |
| operating_point_metrics_stable | True |
| mechanism_transfer_remains_disallowed | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use the reproducible transfer-safety application audit only for abstain/route operator decisions; keep mechanism transfer and fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing transfer-safety application audit and its recorded sources only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 transfer-safety application audit is reproducible.
- Transfer-safety application audit rebuilds after created_utc normalization with 0 reproducibility violations.
- Use the reproducible application audit only for abstain/route decisions.
