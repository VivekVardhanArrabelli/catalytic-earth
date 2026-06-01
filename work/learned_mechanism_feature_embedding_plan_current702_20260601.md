# Learned Mechanism-Feature Embedding Plan - current702

Run: 2026-06-01T02:15:51Z

Leakage-safe learned mechanism-feature embedding scaffold for the D11 continuous mechanism-space target. This is a spec plus coverage audit, not a heldout-trained or threshold-tuned model.

## Status

- scaffold_ready_train_cal_pilot_deferred_until_row_level_feature_extraction
- No heldout labels were used for training, calibration, or threshold tuning.

## Feature Coverage

- fingerprints_total: 8
- electron_flow_class: 8
- transition_state_stabilization_role_present: 3
- proton_transfer_connectivity_present: 5
- bond_making_breaking_descriptor: 8
- cofactor_catalytic_locus: 7
- metal_covalent_radical_flags: 6
- active_site_residue_role_graph_available: 8

## Pilot Design

- Trainable rows: train/calibration or current702 in_distribution rows only
- Forbidden rows: heldout and OOS rows
- Evaluation target: operating-point novelty/abstention and relationship eval, not only AUC.

## Extraction Gaps

- row_level_electron_flow_class: available only as fingerprint-level template, not row-level evidence Next: derive row-level labels/features from curated reaction center plus active-site roles for train/cal rows only.
- transition_state_stabilization_role: role text exists in fingerprints but not as normalized row-level graph edges Next: normalize active_site_signature roles into residue-role graph vocabulary.
- proton_transfer_connectivity: acid/base roles present but no directed donor/acceptor connectivity sidecar Next: extract directed role edges from geometry feature rows where residue mappings exist.
- bond_making_breaking: fingerprint reaction-center descriptors exist; row-specific Rhea/M-CSA bond-change mapping is not normalized here Next: build a source-backed bond-change sidecar before any supervised pilot.
- cofactor_catalytic_locus: row-level organic cofactor scores exist for flavin/heme/PLP, but metal/cobalamin/radical/Fe-S loci are incomplete Next: persist row-level metal/cobalamin/radical/Fe-S sidecars or mark unsupported classes as missing.
