# Source-Free Locator UniProt Position Validation: mh_065/mh_072

## Summary

This pass attempted the least ambiguous remaining locator blocker class from the
review queue: sequence-position validation for `mh_065` and `mh_072`. Both
rows remain review-only and blocked. Their candidate locators have valid local
coordinate contacts, but the frozen selected PDB `struct_ref` accessions do not
match the source-row UniProt accessions.

## Result

| Row | Source accession | Selected PDB | PDB `struct_ref` accession | Result |
| --- | --- | --- | --- | --- |
| `mh_065` | `Q79MP6` | `1DDK` | `Q932P5` | blocked accession mismatch |
| `mh_072` | `P0A6P9` | `1E9I` | `P08324` | blocked accession mismatch |

The candidate residue contacts are still useful review evidence, but they are
not approved source-free active-site locator sidecars. No locator was copied
into the audited locator directory, and no predicted-geometry scoring was run.

## Guardrails

- Used frozen local sidecars and coordinate files only.
- Did not fetch source data or coordinates.
- Did not change labels, registries, ontologies, splits, thresholds, or model
  weights.
- Did not use source text, panel IDs, labels, or EC identifiers as predictive
  features.
- Did not train on heldout rows.

## Next Action

Run split-safe same-accession template checks for `mh_067` and `mh_068`. For
`mh_065` and `mh_072`, require either an explicit representative-accession
equivalence policy (`Q79MP6` -> `Q932P5`, `P0A6P9` -> `P08324`) or frozen
coordinates whose `struct_ref` mappings match the requested source accessions
before any locator copy or predicted-geometry scoring.
