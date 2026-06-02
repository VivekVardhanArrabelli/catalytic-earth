# Predicted-Structure Fold Channel Carryover Resolution - current702

Run: 2026-06-02T16:13:09Z

Validation-only resolution of the carryover request to build or stage the AlphaFoldDB-predicted Foldseek/TM channel from frozen current702 inputs.

## Status

- fold_channel_carryover_resolved_no_rerun_needed
- Requested outputs present: True
- Scored scope complete: True
- Foldseek rerun required: False
- Remaining blockers: none

## Counts

- Atlas in-distribution ok rows: 168
- Heldout ok rows: 126
- Priority cofactor-confounded OOS rows: 6
- All-heldout nearest hits: 126
- Priority nearest hits: 6
- Contract critical violations: 0
- Missing persistent coordinate files: 0

## Input Status

- predicted_geometry_atlas_status: complete
- fold_level_signal_status: computed_from_existing_selected_pdb_foldseek_proxy
- predicted_structure_fold_channel_status: computed_all_heldout_foldseek_scores
- contract_audit_status: fold_channel_contract_passed_current702
- coordinate_provenance_status: coordinate_provenance_complete
- reproduction_manifest_status: fold_channel_byte_reproduction_ready

## Interpretation

- The requested fold-channel build/stage task is already satisfied by the existing scored artifact and its passing strict contract audit.
- Treat the fold channel as downstream-ready for review-only diagnostics; persistent AFDB-v6 CIF provenance is only needed for byte-level reproduction.

## Next Actions

- 1. Do not rerun the predicted-structure fold channel unless the contract audit fails; continue from current handoff review gates.
- 2. If mechanism-feature work resumes, start with reviewer provenance for m_csa:11, m_csa:169, and m_csa:5 before refreshing any no-template feature contract.
- 3. If the run must remain automation-only, use docs/artifact index cleanup and focused validation rather than mutating labels, thresholds, or registries.
