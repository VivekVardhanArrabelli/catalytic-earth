# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Event-Axis Linker Schema - current702

Run: 2026-06-02T20:20:12Z

Schema and acceptance contract for materializing the missing source-free event-axis linker for the calibrated row-specific feature pair. This stages the contract only; it creates no linker rows, copies no locators, and applies no heldout threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_ready_no_linkers_materialized
- Event token: event_residue_role:proton_transfer|electrostatic_stabiliser
- Event type: proton_transfer
- Residue role: electrostatic_stabiliser
- Materialized linker rows: 0
- Blockers to clear: source_free_current702_heldout_locator_surface_missing, source_free_proton_transfer_event_axis_missing, source_free_event_residue_role_linker_missing

## Acceptance Criteria

- row has an approved source-free current702 heldout locator sidecar
- residue position is accession-compatible and UniProt-validated
- residue role assignment is derived without M-CSA heldout mechanism text or curated heldout role labels
- proton-transfer event axis is derived from source-free structural or chemistry evidence, not EC/Rhea/source IDs/target names
- guardrail audit confirms labels, source text, source IDs, target names, EC/Rhea IDs, and heldout outcomes are excluded as predictive inputs

## Decision

- Event-axis linker schema ready: True
- Event-axis linkers materialized: False
- Heldout-safe event-axis surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Fill this schema only after approved source-free current702 heldout locator sidecars exist; then rerun the event-linker blocker audit, source-free application surface, and heldout-safe surface plan before any heldout threshold read.

## Interpretation

- The missing event-axis linker now has an explicit source-free schema and acceptance contract. No linker rows are materialized yet because current702 heldout locators and source-free event axis evidence remain blocked.
- Approve/copy current702 heldout locator sidecars or provide another source-free locator path, then fill this schema for the proton-transfer/electrostatic-stabiliser token.
