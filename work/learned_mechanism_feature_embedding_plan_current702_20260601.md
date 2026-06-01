# Learned Mechanism-Feature Embedding Plan - current702

Run: 2026-06-01T07:58:19Z

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

## Row-Level Sidecars

- Active-site role graph: {'status': 'active_site_role_graph_sidecar_ready', 'rows_with_ok_role_graph': 656, 'unique_roles': 53, 'unique_role_edges': 669}
- Reaction-center template: {'status': 'reaction_center_template_sidecar_ready', 'rows_with_template': 232, 'unique_chemical_operations': 8, 'unique_bond_change_templates': 10}
- Sidecar schema audit: {'status': 'mechanism_feature_sidecar_schema_passed_current702', 'critical_counts': {'active_site_alignment_violations': 0, 'active_site_extra_entries': 0, 'active_site_missing_entries': 0, 'active_site_required_key_violations': 0, 'active_site_residue_count_violations': 0, 'active_site_role_count_violations': 0, 'active_site_status_violations': 0, 'duplicate_active_site_rows': 0, 'duplicate_reaction_center_rows': 0, 'reaction_center_alignment_violations': 0, 'reaction_center_extra_entries': 0, 'reaction_center_missing_entries': 0, 'reaction_center_required_key_violations': 0, 'reaction_center_status_violations': 0, 'reaction_center_template_violations': 0, 'sidecar_cross_missing_entries': 0, 'source_status_violations': 0}, 'schema_safe_for_train_cal_pilot': True}

## Extraction Gaps

- row_level_electron_flow_class: available only as fingerprint-level template, not row-level evidence Next: derive row-level labels/features from curated reaction center plus active-site roles for train/cal rows only.
- transition_state_stabilization_role: row-level role graph vocabulary exists, but directed transition-state/proton/electron-flow edges are not inferred Next: consume the role graph sidecar on train/cal rows only, then add directed mechanism-edge features.
- proton_transfer_connectivity: acid/base roles present but no directed donor/acceptor connectivity sidecar Next: extract directed role edges from geometry feature rows where residue mappings exist.
- bond_making_breaking: fingerprint-template reaction-center descriptors are row-aligned, but row-specific Rhea/M-CSA bond-change mapping is not normalized here Next: build a source-backed row-specific bond-change sidecar before any supervised pilot.
- cofactor_catalytic_locus: row-level organic cofactor scores exist for flavin/heme/PLP, but metal/cobalamin/radical/Fe-S loci are incomplete Next: persist row-level metal/cobalamin/radical/Fe-S sidecars or mark unsupported classes as missing.
