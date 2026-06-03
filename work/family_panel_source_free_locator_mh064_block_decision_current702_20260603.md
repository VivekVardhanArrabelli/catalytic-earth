# Family-Panel Source-Free Locator mh_064 Block Decision - current702

Run: 2026-06-03T01:18:04Z

Review-only block decision for the Lever 4 `mh_064` alternate-coordinate
locator blocker. It composes the policy blocker packet and local-cache preflight
without fetching coordinates, copying locators, scoring predicted geometry, or
changing any countable label surface.

## Decision

- `source_free_locator_mh064_block_decision_rejected_review_only`
- Leave `mh_064` blocked.
- Do not fetch alternate coordinates in this automation run.
- Do not copy locator sidecars or score predicted geometry.

## Evidence

- Alternate PDB IDs checked: 5
- Alternate coordinate files cached: 0
- Alternate coordinate files missing: 5
- Requested AFDB coordinate cached: 1
- Selected coordinate cached: 1
- Ready for predicted-geometry scoring: 0

## Rationale

- The local-cache preflight found 0/5 bounded alternate coordinate files cached
  for `3RKJ`, `3RKK`, `3SBL`, `3SFP`, and `3SPU`.
- The selected `3PG4` coordinate and requested AFDB coordinate are cached but do
  not clear the no-ligand alternate-coordinate blocker.
- Fetching new coordinates is a policy action and is not authorized by this
  automation run.

## Next Gate

- Unblock only after explicit approval to fetch one or more bounded alternate
  coordinates (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, `3SPU`), then rerun candidate
  extraction and locator schema/integrity review before predicted-geometry
  scoring.

## Guardrails

- No network fetch was attempted.
- No locator sidecars were copied, created, or marked scoring-ready.
- No labels, registries, ontologies, imports, thresholds, training data, or
  model weights changed.
