# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Input Audit - current702

Run: 2026-06-02T13:40:22Z

Input audit for priority-1 source-free locator queue rows. It checks whether the predicted-geometry artifact already contains source-free local ligand/cofactor anchors that could support locator sidecar creation without M-CSA heldout mechanism text, heldout labels, source IDs, target names, or EC/Rhea IDs.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_input_audit_blocked
- Priority-1 queue rows: 126
- Rows with source-free ligand/cofactor anchor: 0
- Rows without source-free anchor: 126
- Auto-create locator sidecars now: False
- Source-free locator schema available: 1
- Required residue locators per approved sidecar: 2
- Allowed locator evidence classes: 4
- Blockers: priority1_rows_lack_source_free_contact_anchor, source_free_event_axis_missing_for_pair_token

## Decision

- Next gate: Do not create locator sidecars from predicted-geometry rows alone. Add a source-free coordinate-local anchor policy or source-free structure-local ligand/contact evidence, then rerun this audit before sidecar materialization.
- Heldout read once performed: False

## Interpretation

- The priority-1 queue rows have predicted-geometry coordinates, but none currently expose source-free ligand/cofactor contact anchors for approved locator sidecar creation.
- Define or materialize a source-free local anchor evidence path before copying or approving any current702 heldout locator sidecars.
