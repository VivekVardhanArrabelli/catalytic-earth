# Source-Free Locator Accession-Equivalence Position Audit: mh_065/mh_072 - current702

Run: 2026-06-02T19:32:42Z

Evidence-only audit for the highest-priority remaining source-free locator decision class. It authorizes no representative equivalence, locator copy, coordinate fetch, scoring, label, or import action.

## Status

- source_free_locator_accession_equivalence_position_audit_blocked_review_only
- Target rows: 2
- Candidate locator positions checked: 6
- Requested-AFDB expected-code matches: 0
- Approved locator-copy rows: 0

## Row Checks

| row | selected PDB | requested accession | PDB struct_ref accession | AFDB locator-code matches | decision |
| --- | --- | --- | --- | ---: | --- |
| mh_065 | 1DDK | uniprot:Q79MP6 | Q932P5 | 0/3 | raw locator copy blocked; matching coordinate or approved remap required |
| mh_072 | 1E9I | uniprot:P0A6P9 | P08324 | 0/3 | raw locator copy blocked; matching coordinate or approved remap required |

## Interpretation

- The selected PDB coordinates still map to representative accessions that differ from the requested source accessions.
- The raw candidate sequence positions do not resolve to the expected residue codes in the requested UniProt AFDB models (0/6 matches).
- Representative-accession equivalence alone is not sufficient for automated locator copy unless it includes explicit residue remapping approval.

## Next Action

For mh_065/mh_072, do not copy the raw 1DDK/1E9I locators. Provide matching frozen coordinates or explicitly approved alignment/remapped locators before rerunning schema/scoring.
