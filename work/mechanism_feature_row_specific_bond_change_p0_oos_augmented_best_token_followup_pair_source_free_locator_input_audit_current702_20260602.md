# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Input Audit - current702

Run: 2026-06-03T20:06:48Z

Input audit for priority-1 source-free locator queue rows. It checks whether the predicted-geometry artifact already contains source-free local ligand/cofactor anchors, and whether the selected-PDB coordinate anchor candidate audit has staged coordinate-local ligand/metal contact anchors, without M-CSA heldout mechanism text, heldout labels, source IDs, target names, or EC/Rhea IDs.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_input_audit_blocked
- Priority-1 queue rows: 126
- Rows with source-free ligand/cofactor anchor: 0
- Rows with source-free coordinate-local anchor candidate: 102
- Coordinate-anchor preflight rows: 55
- Preflight-passed pending explicit approval: 55
- Preflight rows with warnings: 6
- Approved locator rewrites now: 0
- Rows without source-free anchor: 24
- Auto-create locator sidecars now: False
- Source-free locator schema available: 1
- Required residue locators per approved sidecar: 2
- Allowed locator evidence classes: 4
- Blockers: priority1_rows_lack_source_free_contact_or_coordinate_anchor, source_free_coordinate_anchor_preflight_passed_requires_explicit_approval, source_free_coordinate_anchor_candidates_need_review, source_free_event_axis_missing_for_pair_token

## Decision

- Next gate: Use the preflight-passed coordinate-anchor rows as the explicit-approval queue. Do not copy locator sidecars or apply the frozen threshold until approved rewrites exist in the audited locator directory and this audit is rerun.
- Heldout read once performed: False

## Interpretation

- The priority-1 queue rows have predicted-geometry coordinates, 102 now expose review-only coordinate-local anchor candidates, 55 pass rewrite preflight pending explicit approval, and none are approved locator sidecars for scoring.
- Approve only reviewed locator rewrites, copy those sidecars into the audited locator directory, rerun strict/input/surface audits, and keep the event-axis blocker separate before any heldout read.
