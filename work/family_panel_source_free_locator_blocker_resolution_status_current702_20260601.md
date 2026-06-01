# Source-Free Locator Blocker Resolution Status

## Summary

This status artifact consolidates the seven family-panel rows still missing
approved source-free active-site locators. Automation discovery is complete for
all seven, but none is ready for predicted-geometry scoring because every row
now requires a human or policy decision.

## Current State

| Row | Status | Next action |
| --- | --- | --- |
| `mh_065` | accession mismatch | approve equivalence or matching coordinate |
| `mh_072` | accession mismatch | approve equivalence or matching coordinate |
| `mh_067` | split-safe check passed | human approval to copy locator |
| `mh_068` | split-safe check passed | human approval to copy locator |
| `external_glycoside_panel` | acetate locator rejected | validator or substrate-complex coordinate |
| `mh_064` | no ligand/metal in selected coordinate | decide alternate-coordinate fetches |
| `secondary_probe::cobalamin_radical_rearrangement` | no ligand/metal and no alternate PDB | nonlabel strategy or alternate source |

No locator sidecars were copied and no predicted-geometry scoring was run.

## Next Action

Do not rerun locator discovery. Pick one policy decision: approve
`mh_067`/`mh_068` locator copy, decide `mh_065`/`mh_072` accession equivalence,
reject or approve `mh_064` alternate-coordinate fetches, or define the Q59490
nonlabel locator strategy.
