# Fold-Augmented Lever 3 Deployment Operator Manifest Reproducibility Audit - current702

Run: 2026-06-05T12:13:56Z

Reproducibility audit for the current Lever 3 operator manifest. It rebuilds the manifest audit from its recorded deployment contract sources, normalizes only created_utc, and checks source hash currency plus manifest SHA and metric stability.

## Status

- fold_augmented_lever3_deployment_operator_manifest_reproducibility_audit_passed
- Operator manifest reproducible: True
- Operator manifest ready: True
- Fixed-threshold scoring closure available now: False
- Reproducibility violations: []

## Rebuild

- Normalized rebuild matches stored: True
- Stored normalized SHA-256: 7348b844d6626bc0d26cd4846fdfeb1255c97cc95ad5b3db9d276de56f634d62
- Stored operator manifest SHA-256: e3de25919052c16e5a139ebd950885d3ca8bbc1cbafaa58ba37df5d346578fdf
- Rebuilt operator manifest SHA-256: e3de25919052c16e5a139ebd950885d3ca8bbc1cbafaa58ba37df5d346578fdf
- Rebuild error: None

## Counts

- Source hashes current: 2/2
- Rebuild difference count: 0
- Manifest rows abstain/route: 21/21
- Unsafe action rows: 0
- Forced mechanism-label rows: 0
- Forbidden-field rows: 0
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204

## Reproducibility Checks

| check | passed |
| --- | ---: |
| operator_manifest_audit_passed | True |
| operator_manifest_source_hashes_current | True |
| operator_manifest_rebuild_matches_stored_after_created_utc_normalization | True |
| operator_manifest_sha_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use the reproducible operator manifest only as the abstain/route action table; keep fixed-threshold scoring closure fail-closed pending exact P07658 coordinate/provenance evidence.

## Guardrails

- Measured readout only. Existing operator manifest artifact only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 operator manifest is reproducible.
- Operator manifest audit rebuilds after created_utc normalization with 0 reproducibility violations.
- Use the reproducible manifest for abstain/route actions only; keep scoring closure fail-closed.
