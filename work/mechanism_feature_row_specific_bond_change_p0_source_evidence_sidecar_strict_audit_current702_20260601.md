# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar Strict Audit - current702

Run: 2026-06-02T05:15:15Z

Strict audit for the P0 source-evidence sidecar. It checks row alignment, schema fields, forbidden predictive fields, and the approved-row evidence gate without authorizing feature-contract consumption.

## Status

- p0_source_evidence_sidecar_strict_audit_passed_reviewed_consumable
- Worksheet rows: 15
- Sidecar rows: 15
- Draft rows: 12
- Approved rows: 3
- Rows with events: 15
- Rows with source spans: 15
- Strict critical violations: 0
- Violation counts: {}
- Feature-contract refresh allowed: False

## Interpretation

- The source-evidence sidecar is row-aligned and schema-valid; reviewer-approved rows are consumable only by a future split-filtered feature-contract materialization.
- Use approved rows only after train/cal split filtering; continue manual review for remaining draft rows before any full P0 feature-contract refresh.
