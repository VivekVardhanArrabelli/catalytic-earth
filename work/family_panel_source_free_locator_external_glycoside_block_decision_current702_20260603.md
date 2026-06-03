# Family-Panel Source-Free Locator External Glycoside Block Decision - current702

Run: 2026-06-03T01:13:04Z

Review-only block decision for the Lever 4 `external_glycoside_panel`
source-free locator. It composes the NAG validator and local-cache
substrate-coordinate scout without copying locators, fetching coordinates,
scoring predicted geometry, or changing any countable label surface.

## Decision

- `source_free_locator_external_glycoside_block_decision_rejected_review_only`
- Leave `external_glycoside_panel` blocked.
- Do not copy the 7QQF acetate locator, NAG/glycan-derived locator, or any raw
  glycan/buffer retargeting.
- Predicted-geometry scoring is not authorized.

## Evidence

- Local coordinate files scanned: 60
- Same-accession coordinate records: 4
- Same-accession records with rejected glycan/buffer ligands: 1
- Substrate-like coordinate candidates: 0
- Ready for predicted-geometry scoring: 0

## Rationale

- The NAG validator already rejected glycan-context retargeting for the
  `external_glycoside_panel` locator.
- The local-cache substrate-coordinate scout found 4 same-accession coordinate
  records but 0 substrate-like coordinate candidates.
- The only same-accession PDB coordinate with non-water HETATMs carries
  ACT/BMA/FUC/MAN/MLI/NAG glycan or buffer ligands and cannot clear the
  non-glycan substrate-coordinate gate.

## Next Gate

- Unblock only with an explicit substrate-complex coordinate or expert-approved
  non-glycan active-site locator, then rerun locator schema/integrity review
  before predicted-geometry scoring.

## Guardrails

- No locator sidecars were copied, created, or marked scoring-ready.
- No coordinates or source data were fetched.
- No labels, registries, ontologies, imports, thresholds, training data, or
  model weights changed.
