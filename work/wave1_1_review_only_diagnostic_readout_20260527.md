# Wave 1.1 Review-Only Diagnostic Readout - 2026-05-27

This readout packages the closed Packet 2 and Packet 3 decisions into six non-countable diagnostic cells. It does not change registries, ontology IDs, fingerprints, thresholds, imports, model outputs, production scoring, representation artifacts, or artifact migration state.

## Cells

- `primary_v1_metrics_after_m_csa497_m_csa750_readthrough`: 9 items; review_only_diagnostic_summary_only.
- `packet2_near_orphan_geometry_rescue_behavior`: 17 items; review_only_diagnostic_slice_only.
- `packet2_wrong_foldseek_transfer_diagnostic_behavior`: 4 items; review_only_diagnostic_slice_only.
- `packet3_eight_pilot_only_child_stratum_readout`: 8 items; pilot_only_review_slice_not_canonical_metric.
- `abstention_behavior_on_unresolved_or_underpowered_child_buckets`: 3 items; abstention_probe_only_not_accuracy_metric.
- `canary_behavior_for_underpowered_or_mixed_chemistry_cells`: 8 items; canary_only_or_do_not_use_not_countable_metric.

## Key Read-Throughs

- `m_csa:497` and `m_csa:750` are excluded from primary v1 flavin metrics and retained only as OOS/boundary or future acquisition signals.
- Packet 2 contributes 17 near-orphan geometry-rescue rows and 4 wrong-Foldseek-transfer diagnostic rows, all non-countable.
- Packet 3 contributes 8 pilot-only child labels, 3 abstention-probe unresolved buckets, and 7 underpowered canary labels; `flavin.dehydrogenase_oxidase_hydride_transfer` remains blocked as mixed chemistry.
