# Fold-Augmented Lever 3 Deployment Stage Provenance Reproducibility Audit - current702

Run: 2026-06-05T12:22:59Z

Reproducibility audit for the current Lever 3 stage-provenance readout. It rebuilds the stage-provenance audit from its recorded operator-manifest and lineage artifacts, normalizes only created_utc, and checks source-hash and metric stability.

## Status

- fold_augmented_lever3_deployment_stage_provenance_reproducibility_audit_passed
- Stage provenance reproducible: True
- Stage provenance clean: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: 5d76a1f1a68e356ad8b737d3112bc72d594a5bde8be16d1b85309e2c964a4386
- Rebuilt normalized SHA-256: 5d76a1f1a68e356ad8b737d3112bc72d594a5bde8be16d1b85309e2c964a4386
- Rebuild error: None

## Counts

- Source hashes current: 2/2
- Rebuild difference count: 0
- Manifest rows abstain/route: 21/21
- Stage-source artifacts covered: 5/5
- Stage-source artifacts guardrail-clean: 5/5
- Lineage source hashes current: 43/43
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204

## Reproducibility Checks

| check | passed |
| --- | ---: |
| stage_provenance_audit_passed | True |
| stage_provenance_source_hashes_current | True |
| stage_provenance_rebuild_matches_stored_after_created_utc_normalization | True |
| stage_source_coverage_metrics_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use the reproducible stage-provenance readout and operator manifest for abstain/route actions only; keep fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing stage-provenance artifact only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 stage provenance is reproducible.
- Stage-provenance audit rebuilds after created_utc normalization with 0 reproducibility violations.
- Use the reproducible manifest/stage-provenance readouts for abstain/route actions only.
