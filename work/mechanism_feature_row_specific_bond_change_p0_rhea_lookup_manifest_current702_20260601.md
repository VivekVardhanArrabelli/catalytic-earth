# Mechanism Feature Row-Specific Bond-Change P0 Rhea Lookup Manifest - current702

Run: 2026-06-01T20:08:21Z

Manual-only lookup manifest for P0 source-evidence draft rows that lack local EC-to-Rhea equations. It stages exact EC query targets and rerun instructions without fetching source data or approving rows.

## Status

- p0_rhea_lookup_manifest_ready_manual_only
- Rhea lookup rows: 4
- Rows with EC targets: 4
- Lookup targets: 4
- Blocker counts: {'rhea_equation_missing': 4}
- Critical violations: 0

## Lookup Rows

- m_csa:124: ec_targets=['ec:1.9.3.1']; events=5; blockers=rhea_equation_missing
- m_csa:11: ec_targets=['ec:3.1.21.2']; events=4; blockers=rhea_equation_missing
- m_csa:169: ec_targets=['ec:3.4.14.5']; events=4; blockers=rhea_equation_missing
- m_csa:5: ec_targets=['ec:3.4.16.6']; events=1; blockers=rhea_equation_missing

## Interpretation

- The four P1 review-queue rows all have EC targets but no local Rhea equations. The next blocker-clearing step is manual Rhea lookup and sidecar update, not feature use.
- Resolve `m_csa:124`, `m_csa:11`, `m_csa:169`, then `m_csa:5` from the staged query URLs; rerun the sidecar strict audit and review queue after edits.
