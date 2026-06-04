# Fold-Augmented Confounded Proxy Current-Evidence Blocker After Input Preflight - current702

Run: 2026-06-04T09:13:41Z

Consolidated Lever 3 current-evidence blocker after local deployment-input preflight. It records the exact row-level evidence missing for surface completeness and the remaining train/cal calibration shortfalls. It does not approve sources, stage coordinates, rescore rows, rerun thresholds, or use heldout rows for calibration.

## Status

- fold_augmented_confounded_proxy_current_evidence_blocker_blocked_after_input_preflight
- Surface-completeness blocker rows: 5
- Coordinate-source blocker rows: 4
- Coordinate rows ready now: 0
- Disallowed experimental shortcut rows: 3
- Q43088 additional locator positions needed: 2
- High-cofactor new abstained rows needed: 16
- Same-family structural new abstained rows needed: 170
- Blockers: ['current_local_evidence_cannot_clear_surface_completeness', 'four_rows_need_approved_predicted_structure_coordinates', 'q43088_two_source_free_locator_positions_missing', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Surface Rows

| row | accession | blocker | missing evidence | smallest next experiment |
| --- | --- | --- | --- | --- |
| m_csa:416 | P07071 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate with provider/model/version/path/checksum provenance | approve a provider-neutral predicted-structure coordinate source and stage one local predicted coordinate for this accession |
| m_csa:562 | P07658 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate with provider/model/version/path/checksum provenance | approve a provider-neutral predicted-structure coordinate source and stage one local predicted coordinate for this accession |
| m_csa:586 | P00806 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate with provider/model/version/path/checksum provenance | approve a provider-neutral predicted-structure coordinate source and stage one local predicted coordinate for this accession |
| m_csa:637 | P04531 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate with provider/model/version/path/checksum provenance | approve a provider-neutral predicted-structure coordinate source and stage one local predicted coordinate for this accession |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | two additional approved source-free locator positions or approved source-free geometry sidecar | approve two additional Q43088 locator positions from source-free evidence, or approve an equivalent geometry sidecar |

## Calibration Rows

| axis | minimum new abstained rows | smallest next experiment |
| --- | ---: | --- |
| high_cofactor_signature_proxy | 16 | Acquire exactly 16 new non-heldout train/cal OOS rows with source-free high-cofactor signatures and deployment-valid predicted structures, then score them at unchanged threshold 0.44155. |
| same_family_structural_proxy | 170 | Acquire the frozen same-family structural train/cal OOS row set under the existing contract; this remains the larger calibration blocker after the high-cofactor probe. |

## Decision

- Current evidence can solve surface completeness: False
- Current evidence can solve confounded-safe calibration: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Smallest surface-completeness experiment: Approve and stage predicted coordinates for P07071, P07658, P00806, and P04531 with provider/model/version/path/checksum provenance, and approve two Q43088 source-free locator positions or an equivalent geometry sidecar.
- Smallest calibration experiment: Run the frozen 16-row high-cofactor train/cal OOS acquisition first; it is the smaller calibration blocker, but the same-family structural 170-row blocker remains after it.
- Next gate: Do not rerun or retune threshold 0.44155. Clear the five surface-completeness rows through deployment-valid evidence, then score at the fixed operating point; separately acquire the frozen train/cal OOS proxy rows for calibration closure.

## Interpretation

- Current local evidence cannot make Lever 3 deployment-valid or confounded-safe: all four coordinate-source rows still lack approved predicted coordinates, Q43088 still lacks two approved source-free locator positions, and the train/cal proxy calibration shortfalls remain 16 and 170 rows.
- The smallest concrete next experiment is an approval/staging manifest for the four predicted-coordinate rows plus a Q43088 locator review packet; the smallest calibration experiment is the frozen 16-row high-cofactor probe.
