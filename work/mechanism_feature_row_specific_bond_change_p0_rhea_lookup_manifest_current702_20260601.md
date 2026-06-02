# Mechanism Feature Row-Specific Bond-Change P0 Rhea Lookup Manifest - current702

Run: 2026-06-01T23:00:43Z

Manual-only lookup manifest for P0 source-evidence draft rows that lack local EC-to-Rhea equations. It stages exact EC query targets and rerun instructions without fetching source data or approving rows.

## Status

- p0_rhea_lookup_manifest_ready_manual_only
- Rhea lookup rows: 3
- Rows with EC targets: 3
- Lookup targets: 3
- Blocker counts: {'rhea_equation_missing': 3}
- Critical violations: 0

## Lookup Rows

- m_csa:11: ec_targets=['ec:3.1.21.2']; events=4; blockers=rhea_equation_missing
- m_csa:169: ec_targets=['ec:3.4.14.5']; events=4; blockers=rhea_equation_missing
- m_csa:5: ec_targets=['ec:3.4.16.6']; events=1; blockers=rhea_equation_missing

## Interpretation

- 3 P1 review-queue rows have EC targets but still lack local or resolved official Rhea equations. The next blocker-clearing step is bounded Rhea lookup and sidecar update, not feature use.
- Resolve the remaining rows from the staged query URLs, then rerun the sidecar, strict audit, review queue, and feature readiness audit after edits.
