# Source-Free Locator Human Decision Matrix - current702

Run: 2026-06-02T23:22:16Z

Compact decision matrix for the 5 source-free locator blockers after automation discovery completed. This summarizes existing blocker artifacts only and authorizes no locator copy, coordinate fetch, or predicted-geometry scoring.

## Status

- source_free_locator_human_decision_matrix_ready_review_only
- Blocked rows tracked: 5
- Decision classes: 4
- Ready for predicted-geometry scoring: 0

## Decision Classes

| priority | class | rows | decision needed |
| ---: | --- | --- | --- |
| 2 | accession_equivalence_or_matching_coordinate_required | mh_065, mh_072 | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| 3 | ligand_specificity_validator_or_substrate_coordinate_required | external_glycoside_panel | No cached same-accession substrate-like coordinate clears external_glycoside_panel; provide an explicit substrate-complex coordinate or expert-approved non-glycan locator before rerunning schema/scoring. |
| 4 | alternate_coordinate_fetch_approval_required | mh_064 | Approve or reject fetching mh_064 frozen alternate coordinates 3RKJ/3RKK/3SBL/3SFP/3SPU. |
| 5 | nonlabel_locator_strategy_or_alternate_source_required | secondary_probe::cobalamin_radical_rearrangement | No eligible alternate source row is available for Q59490; authorize an alternate source row/coordinate or define an explicit nonlabel strategy with at least two source-free sequence-position locators. |

## Interpretation

- All 5 source-free locator blockers are now policy or human-review decisions, not automation-discovery tasks.
- No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy.
- Pick the highest-priority remaining decision class, record the approval/rejection, then rerun the relevant locator schema or candidate audit before any scoring.
