# Fold-Augmented Lever 3 Deployment Operator Route-Class Provenance Reproducibility Audit - current702

Run: 2026-06-05T13:28:20Z

Reproducibility audit for the Lever 3 operator route-class provenance readout. It rebuilds the class-level provenance readout from recorded route-class and stage-provenance sources, normalizes only created_utc, and checks source-hash and metric stability.

## Status

- fold_augmented_lever3_deployment_operator_route_class_provenance_reproducibility_audit_passed
- Route-class provenance reproducible: True
- Route-class provenance ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: b6c097a3b50b89eee0e9b18eb262b040a183aa3d656900e1d9ec4b41adfdb8f6
- Rebuilt normalized SHA-256: b6c097a3b50b89eee0e9b18eb262b040a183aa3d656900e1d9ec4b41adfdb8f6
- Rebuild error: None

## Counts

- Source hashes current: 2/2
- Rebuild difference count: 0
- Route-class stage-source links lineage-covered: 7/7
- Route-class stage-source links guardrail-clean: 7/7
- Route-class stage-source counts: {'cofactor_or_same_family_confound': 2, 'fold_similarity_confound': 1, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 2, 'protein_descriptor_counteraxis': 1}
- Operator rows abstain/route: 21/21

## Reproducibility Checks

| check | passed |
| --- | ---: |
| operator_route_class_provenance_readout_passed | True |
| operator_route_class_provenance_source_hashes_current | True |
| operator_route_class_provenance_rebuild_matches_stored_after_created_utc_normalization | True |
| route_class_provenance_metrics_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use the reproducible class-level provenance audit trail for abstain/route explanations only; keep fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing route-class provenance readout and its recorded sources only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 route-class provenance is reproducible.
- Route-class provenance readout rebuilds after created_utc normalization with 0 reproducibility violations.
- Use reproducible class-level provenance only for abstain/route explanations.
