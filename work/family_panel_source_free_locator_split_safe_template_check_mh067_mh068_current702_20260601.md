# Source-Free Locator Split-Safe Template Check: mh_067/mh_068

## Summary

This pass checked whether the same-accession template basis for `mh_067` and
`mh_068` would leak heldout evidence before any source-free locator copy. Both
rows pass the split-safety check as review-only evidence: their same-accession
current702 matches are in-distribution seed rows, not heldout rows, and the
candidate sidecars contain no forbidden predictive source/label fields.

## Result

| Row | Source accession | Same-accession current702 row | Split | Result |
| --- | --- | --- | --- | --- |
| `mh_067` | `P00918` | `m_csa:216` | `in_distribution` | split check passed |
| `mh_068` | `P15289` | `m_csa:158` | `in_distribution` | split check passed |

This is not a locator-copy authorization. The candidates remain outside the
audited locator directory, and manual copy approval is still required before
source-free predicted-geometry scoring.

## Guardrails

- Used frozen local candidate sidecars, source-backed sidecars, and the
  current702 sequence manifest only.
- Did not copy locator sidecars or score predicted geometry.
- Did not fetch source data or coordinates.
- Did not change labels, registries, ontologies, splits, thresholds, or model
  weights.
- Did not use heldout rows as templates.

## Next Action

Review ligand specificity for `external_glycoside_panel`, then refresh the
remaining-locator blocker state. For `mh_067` and `mh_068`, the remaining
action is human approval to copy the vetted candidate locators into the audited
source-free locator directory.
