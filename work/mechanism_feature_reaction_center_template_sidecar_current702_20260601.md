# Mechanism Feature Reaction-Center Template Sidecar - current702

Run: 2026-06-01T05:08:25Z

Row-level fingerprint-template reaction-center sidecar for mechanism-feature embedding readiness; not row-specific reaction evidence.

## Status

- reaction_center_template_sidecar_ready
- Rows with template: 232 / 702
- Rows by status: {'no_mechanism_fingerprint_oos_or_unlabeled': 470, 'template_available': 232}
- Unique chemical operations: 8
- Unique bond-change templates: 10

## Chemical Operations

- cobalamin_radical_rearrangement: 3
- flavin_mediated_redox_transfer: 50
- flavin_peroxide_oxygen_transfer: 2
- heme_mediated_redox_catalysis: 20
- metal_activated_water_attack: 83
- nucleophilic_acyl_substitution: 42
- plp_stabilized_carbanion_chemistry: 31
- sam_derived_radical_chemistry: 1

## Interpretation

- fingerprint_template_reaction_center_descriptors_are_row_aligned
- row-specific source-backed Rhea/M-CSA bond-change sidecar is still missing
- Use only train/cal rows for any future embedding pilot and add row-specific bond-change evidence before claiming mechanism-level supervision.
