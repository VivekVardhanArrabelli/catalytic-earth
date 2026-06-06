# Fold-Augmented Lever 3 Deployment Contract Reproducibility Audit - current702

Run: 2026-06-05T11:24:33Z

Reproducibility audit for the new Lever 3 deployment-contract readiness and lineage artifacts. It rebuilds both artifacts from their recorded source artifacts, normalizes only created_utc, and checks source-hash currency plus operating-point metric agreement.

## Status

- fold_augmented_lever3_deployment_contract_reproducibility_audit_passed
- Deployment contract reproducible: True
- Deployment contract ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Artifact Rebuilds

- Readiness artifact normalized rebuild matches stored: True
- Readiness normalized SHA-256: 98b63cdd14bad20d62e240f5130ce183589cd5f8c6258652bf69dfbacc6c4d8c
- Lineage artifact normalized rebuild matches stored: True
- Lineage normalized SHA-256: 528600debd66ee884a6a396a00d98c1a03cfb57a4746eb704feb23ed0a82cd38

## Counts

- Readiness source hashes current: 1/1
- Lineage source hashes current: 1/1
- Rebuild difference count: 0
- Application rows abstain/route: 21/21
- Retained residual rows after all counteraxes: 0

## Reproducibility Checks

| check | passed |
| --- | ---: |
| readiness_artifact_source_hashes_current | True |
| lineage_artifact_source_hashes_current | True |
| readiness_rebuild_matches_stored_after_created_utc_normalization | True |
| lineage_rebuild_matches_stored_after_created_utc_normalization | True |
| readiness_contract_passed | True |
| lineage_contract_passed | True |
| operating_point_metrics_match_between_contract_artifacts | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use the reproducible deployment contract as the current Lever 3 abstain/route readout; keep scoring closure fail-closed pending exact P07658 coordinate/provenance evidence.

## Guardrails

- Measured readout only. Existing readiness and lineage artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 deployment contract artifacts are reproducible.
- Readiness and lineage artifacts rebuild after created_utc normalization with 0 reproducibility violations.
- Use the reproducible deployment contract as the operating readout; keep fixed-threshold scoring fail-closed.
