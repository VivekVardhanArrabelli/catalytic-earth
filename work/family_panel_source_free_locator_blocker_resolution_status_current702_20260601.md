# Source-Free Locator Blocker Resolution Status

## Summary

This status artifact consolidates source-free locator blockers after the `mh_067`/`mh_068` split-safe copy decision, the `external_glycoside_panel` NAG validator, the `mh_065`/`mh_072` accession-equivalence position audit, the `mh_064` alternate-coordinate local-cache preflight, and the Q59490 nonlabel-locator feasibility audit. `mh_067`/`mh_068` now have approved audited locators, source-free predicted-geometry scores, and review-only source-check packets; five rows remain unresolved human/policy locator blockers.

## Current State

| Row | Status | Next action |
| --- | --- | --- |
| `mh_067` | locator approved/scored/source-checked | no locator action; keep review-only until expert import/family decision |
| `mh_068` | locator approved/scored/source-checked | no locator action; keep review-only until expert import/family decision |
| `mh_065` | blocked_accession_mismatch_requested_afdb_position_mismatch | Provide a frozen coordinate whose struct_ref maps to Q79MP6, or an explicitly approved alignment/remapped locator from the selected representative coordinate; do not copy the raw selected-PDB locator. |
| `mh_072` | blocked_accession_mismatch_requested_afdb_position_mismatch | Provide a frozen coordinate whose struct_ref maps to P0A6P9, or an explicitly approved alignment/remapped locator from the selected representative coordinate; do not copy the raw selected-PDB locator. |
| `external_glycoside_panel` | selected_acetate_and_nag_glycan_validator_rejected | Provide an explicit substrate-complex coordinate or expert-approved non-glycan active-site locator; do not copy the 7QQF acetate or NAG glycan-derived locator. |
| `mh_064` | blocked_pending_fetch_policy_no_local_alternates_cached | Approve or reject fetching frozen alternate PDBs 3RKJ/3RKK/3SBL/3SFP/3SPU; no alternate CIF is cached locally. |
| `secondary_probe::cobalamin_radical_rearrangement` | blocked_no_coordinate_anchor_nonlabel_strategy_required | Authorize an alternate source row/coordinate or define an explicit nonlabel strategy with at least two source-free sequence-position locators; current local coordinates provide no non-water/metal anchor. |

## Accession-Equivalence Position Audit

- `mh_065`/`mh_072` selected PDB coordinates map to representative accessions that differ from the requested source accessions.
- Raw selected-PDB candidate positions do not resolve to expected residue codes in the requested UniProt AFDB models: 0/6 matches.
- Matching frozen coordinates or explicit alignment/remapped locator approval is required before any audited locator copy.

## External Glycoside Validator

- The selected 7QQF acetate locator remains rejected.
- The dedicated NAG validator rejects automatic retargeting: 4/4 NAG sites have near-covalent C1-Asn contacts consistent with glycan/N-linked glycosylation context.
- Approved locator-copy rows: 0; ready for predicted-geometry scoring: 0.

## mh_064 Local Cache Preflight

- Selected 3PG4 and AFDB C7C422 coordinates are cached, but no alternate CIF among 3RKJ/3RKK/3SBL/3SFP/3SPU is cached locally.
- Coordinate fetch approval or rejection is still required before any alternate candidate extraction.

## Q59490 Feasibility Audit

- Selected 1L1L has water HETATMs only, AFDB Q59490 has no HETATM anchor, and the candidate sidecar has 0 residue locators.
- A reviewed nonlabel strategy or alternate source row/coordinate is still required; residue locators were not fabricated from panel identity or source prose.

## Counts

- Remaining blocker rows: 5
- Resolved mh_067/mh_068 rows: 2
- No labels, registries, ontologies, imports, thresholds, training data, source fetches, coordinate downloads, or model weights changed.

## Next Action

Do not rerun locator discovery. The remaining unresolved locator/policy blockers are mh_065/mh_072 matching-coordinate or explicitly remapped-locator approval, external_glycoside_panel substrate-complex/non-glycan locator, mh_064 alternate-coordinate fetch approval with 0/5 alternates cached locally, and Q59490 alternate source or explicit nonlabel locator strategy.
