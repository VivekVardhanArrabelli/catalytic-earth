# Mechanism Feature Row-Specific Bond-Change P0 Rhea Lookup Resolution - current702

Run: 2026-06-01T23:00:33Z

Official Rhea lookup resolution for P0 draft source-evidence rows that lacked local graph Rhea equations. This may add review-only Rhea equation evidence to the draft sidecar, but does not approve rows or refresh feature contracts.

## Status

- p0_rhea_lookup_resolution_partial_review_only
- Lookup rows: 4
- Resolved rows: 1
- Resolved by exact EC rows: 0
- Resolved by accession rows: 1
- Unresolved rows: 3

## Row Resolutions

| row | accession | status | Rhea | EC | equation |
| --- | --- | --- | --- | --- | --- |
| m_csa:5 | P08819 | unresolved_no_rhea_record_for_ec_or_accession | None | None |  |
| m_csa:11 | P0A6C1 | unresolved_no_rhea_record_for_ec_or_accession | None | None |  |
| m_csa:124 | P00396 | resolved_accession_query_with_ec_reclassification | RHEA:11436 | EC:7.1.1.9 | 4 Fe(II)-[cytochrome c] + O2 + 8 H(+)(in) = 4 Fe(III)-[cytochrome c] + 2 H2O + 4 H(+)(out) |
| m_csa:169 | P27487 | unresolved_no_rhea_record_for_ec_or_accession | None | None |  |

## Interpretation

- 1/4 Rhea lookup rows resolved to an official Rhea equation; unresolved rows remain manual review blockers.
- Rebuild the draft P0 source-evidence sidecar with this resolution artifact, rerun the strict audit, then keep remaining unresolved rows in the Rhea lookup manifest.
