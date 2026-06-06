# Fold-Augmented Lever 3 Deployment Operator Route-Class Reproducibility Audit - current702

Run: 2026-06-05T13:12:40Z

Reproducibility audit for the Lever 3 operator route-class readout. It rebuilds the route-class readout from recorded stage-provenance and operator-manifest sources, normalizes only created_utc, and checks source-hash and metric stability.

## Status

- fold_augmented_lever3_deployment_operator_route_class_reproducibility_audit_passed
- Route-class readout reproducible: True
- Route-class readout ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: da473b93ecf12404e4f5bd04e5a850e17da1a307b567b867443293f50341d425
- Rebuilt normalized SHA-256: da473b93ecf12404e4f5bd04e5a850e17da1a307b567b867443293f50341d425
- Rebuild error: None

## Counts

- Source hashes current: 2/2
- Rebuild difference count: 0
- Operator rows abstain/route: 21/21
- Route classes with rows: 5
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204

## Reproducibility Checks

| check | passed |
| --- | ---: |
| operator_route_class_readout_passed | True |
| operator_route_class_source_hashes_current | True |
| operator_route_class_rebuild_matches_stored_after_created_utc_normalization | True |
| route_class_metrics_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use the reproducible route-class readout for operator abstain/route explanations only; keep fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing route-class readout and its recorded sources only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 route-class readout is reproducible.
- Route-class readout rebuilds after created_utc normalization with 0 reproducibility violations.
- Use route-class explanations only for abstain/route actions.
