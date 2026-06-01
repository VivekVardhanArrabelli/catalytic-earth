# Family Panel Source-Free Active-Site Locator Manual Review Packet - current702

Run: 2026-06-01T13:19:39Z

Manual review packet for source-free active-site locator candidate sidecars. It combines candidate extraction, file-integrity checks, and review priority without authorizing audited sidecar copies.

## Status

- source_free_active_site_locator_manual_review_packet_ready_review_only
- Review rows: 10
- Integrity-passed rows: 10
- Priority-1 manual forbidden-feature review rows: 3
- Copy to audited locator dir allowed now: 0
- Ready for predicted-geometry scoring: 0

## Review Rows

| priority | row | accession | class | integrity | sidecar sha256 | next action |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | mh_066 | uniprot:P52699 | ready_for_manual_forbidden_feature_review | passed | 81b6e59b8956a4071f82ae84d1275921a90bb68b3a5e8effd662a06eab502a6a | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 1 | mh_073 | uniprot:P01112 | ready_for_manual_forbidden_feature_review | passed | 0e1b8c6c114354c02ed881258b44927cf63198978153c4afd1bfa05b0d616500 | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 1 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | ready_for_manual_forbidden_feature_review | passed | cae625e255aa109edfa330183860bd3ab3a60a73545c2c5cb78eeabfdb50fe3a | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 2 | external_glycoside_panel | uniprot:Q6NSJ0 | needs_ligand_specificity_review | passed | 40f0b1498872808852c57146eb78a0b0255daf619b0fcffbe08701c0ef929c47 | Review whether the selected coordinate ligand is biologically relevant before any audited sidecar copy. |
| 3 | mh_067 | uniprot:P00918 | needs_split_safe_template_check | passed | 4dd8048ad5e72492502f86949758eff6373b85de7ebc76c3717fdb00fcd70bd3 | Verify same-accession train/cal template use is split-safe before any audited sidecar copy. |
| 3 | mh_068 | uniprot:P15289 | needs_split_safe_template_check | passed | b3fe6d9deb6d5d7cebc11d7af11019114b08d2f04a483579d37a3f391f696096 | Verify same-accession train/cal template use is split-safe before any audited sidecar copy. |
| 4 | mh_065 | uniprot:Q79MP6 | needs_uniprot_position_validation | passed | e515c38ce68e00f4dc0657684b75c110635eeb791ab2234eadfd8a3f82ec4ac9 | Validate candidate sequence positions against UniProt mapping before any audited sidecar copy. |
| 4 | mh_072 | uniprot:P0A6P9 | needs_uniprot_position_validation | passed | e354f51dd0328d8dee73173ff54d8a8b535d1c18f72b5d59c11447973b4d58dd | Validate candidate sequence positions against UniProt mapping before any audited sidecar copy. |
| 5 | mh_064 | uniprot:C7C422 | blocked_needs_new_coordinate_or_nonlabel_locator | passed | 445aa8df4af5dae2f76c9600c006c3fd944e5c912ed6c379f190d43710f07c0e | Find an alternate source-free locator path; current selected coordinate has fewer than two candidate locators. |
| 5 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | blocked_needs_new_coordinate_or_nonlabel_locator | passed | e0520c245a8b016b3b457423bc136ceef2e12075aaddee7c780b29b6445d857b | Find an alternate source-free locator path; current selected coordinate has fewer than two candidate locators. |

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-active-site-locator-manual-review-packet
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-candidate-integrity
```

## Interpretation

- 3 rows can start manual forbidden-feature review; no row may be copied or scored yet.
- Review priority-1 rows first, then rewrite only approved source-free locator sidecars into the audited directory and rerun the schema audit.
