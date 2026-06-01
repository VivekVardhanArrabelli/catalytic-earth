# Source-Free Locator Ligand-Specificity Review: external_glycoside_panel

## Summary

This pass reviewed whether the selected coordinate ligand for
`external_glycoside_panel` is acceptable for a source-free active-site locator.
It is not. The selected ligand is acetate (`ACT`) in local structure `7QQF`,
whose title is "Crystal structure of unliganded MYORG". Acetate contacts are
too nonspecific to use as a glycoside-hydrolase active-site locator.

## Result

| Row | Selected ligand | Structure | Result |
| --- | --- | --- | --- |
| `external_glycoside_panel` | `ACT` acetate | `7QQF` | rejected for locator copy |

The candidate extraction also contains NAG contacts, but local mmCIF annotation
shows glycan/N-glycosylation context. Those contacts may be useful for a future
dedicated validator, but they are not an automatic replacement for the rejected
acetate locator.

## Guardrails

- Used frozen local candidate/source-backed sidecars and `pdb_7QQF.cif`.
- Did not copy locator sidecars or score predicted geometry.
- Did not fetch source data or coordinates.
- Did not change labels, registries, ontologies, splits, thresholds, or model
  weights.

## Next Action

Do not copy the acetate-derived locator. Either build a dedicated frozen-7QQF
glycoside/NAG specificity validator or request explicit approval to use a
substrate-complex coordinate such as the already referenced `7QQH` before any
audited locator copy.
