# Fold-Augmented Lever 3 Deployment Operator Transfer-Safety Matrix Reproducibility Audit - current702

Run: 2026-06-05T14:15:56Z

Reproducibility audit for the Lever 3 operator transfer-safety matrix. It rebuilds the matrix from recorded route-class, provenance, and provenance-reproducibility sources, normalizes only created_utc, and checks source-hash and metric stability.

## Status

- fold_augmented_lever3_deployment_operator_transfer_safety_matrix_reproducibility_audit_passed
- Transfer-safety matrix reproducible: True
- Transfer-safety matrix ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: 8b602152effa238842465c1e21173b21a31ced3cddbd4d33ed2831de154c9f59
- Rebuilt normalized SHA-256: 8b602152effa238842465c1e21173b21a31ced3cddbd4d33ed2831de154c9f59
- Rebuild error: None

## Counts

- Source hashes current: 3/3
- Rebuild difference count: 0
- Operator rows safe-to-abstain/route: 21/21
- Mechanism-transfer-allowed rows: 0
- Route-class stage-source links hash-current: 7/7
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}

## Reproducibility Checks

| check | passed |
| --- | ---: |
| transfer_safety_matrix_readout_passed | True |
| transfer_safety_matrix_source_hashes_current | True |
| transfer_safety_matrix_rebuild_matches_stored_after_created_utc_normalization | True |
| transfer_safety_matrix_metrics_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |
| mechanism_transfer_remains_disallowed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use the reproducible transfer-safety matrix for abstain/route operator decisions only; keep mechanism transfer and fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing transfer-safety matrix readout and its recorded sources only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 transfer-safety matrix is reproducible.
- Transfer-safety matrix rebuilds after created_utc normalization with 0 reproducibility violations.
- Use the reproducible matrix only for abstain/route decisions.
