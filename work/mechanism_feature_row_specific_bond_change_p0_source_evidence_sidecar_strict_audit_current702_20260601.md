# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Sidecar Strict Audit - current702

Run: 2026-06-01T20:06:02Z

Strict audit for the P0 source-evidence sidecar. It checks row alignment, schema fields, forbidden predictive fields, and the approved-row evidence gate without authorizing feature-contract consumption.

## Status

- p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable
- Worksheet rows: 15
- Sidecar rows: 15
- Draft rows: 15
- Approved rows: 0
- Rows with events: 15
- Rows with source spans: 15
- Strict critical violations: 0
- Violation counts: {}
- Feature-contract refresh allowed: False

## Interpretation

- The source-evidence sidecar is row-aligned and schema-valid as draft evidence, but no row is approved and the feature contract must remain unchanged.
- Manually review and, where justified, approve or reject each row's participant mapping and bond-change events; rerun this audit before any no-fit feature-contract refresh.
