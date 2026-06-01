# Mechanism Feature Sidecar Schema Audit - current702

Run: 2026-06-01T07:42:30Z

Strict current702 schema and row-alignment audit for the mechanism-feature active-site role graph and reaction-center template sidecars.

## Status

- mechanism_feature_sidecar_schema_passed_current702
- Manifest rows: 702
- Active-site sidecar rows: 702
- Reaction-center sidecar rows: 702
- Critical violation counts: {'source_status_violations': 0, 'duplicate_active_site_rows': 0, 'duplicate_reaction_center_rows': 0, 'active_site_missing_entries': 0, 'active_site_extra_entries': 0, 'reaction_center_missing_entries': 0, 'reaction_center_extra_entries': 0, 'sidecar_cross_missing_entries': 0, 'active_site_required_key_violations': 0, 'reaction_center_required_key_violations': 0, 'active_site_status_violations': 0, 'reaction_center_status_violations': 0, 'active_site_alignment_violations': 0, 'reaction_center_alignment_violations': 0, 'active_site_residue_count_violations': 0, 'active_site_role_count_violations': 0, 'reaction_center_template_violations': 0}

## Active-Site Status Counts

- missing_accession_compatible_sequence_positions: 42
- missing_catalytic_residue_nodes: 1
- not_m_csa_no_curated_active_site_roles: 3
- ok: 656

## Reaction-Center Status Counts

- no_mechanism_fingerprint_oos_or_unlabeled: 470
- template_available: 232

## Interpretation

- Both mechanism-feature sidecars satisfy the strict current702 row grid, alignment, status, and internal consistency contract.
- This closes a schema-risk layer for the current role-graph and reaction-center template sidecars, but it does not add directed electron/proton-transfer edges or row-specific bond-change evidence.
- Use train/cal-only embedding pilots against these validated sidecars, or add row-specific bond-change/proton-transfer sidecars next.
