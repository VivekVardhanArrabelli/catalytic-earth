# Selected Organic Cofactor Sidecar Schema Audit - current702

Run: 2026-06-01T02:49:40Z

Strict schema and lineage audit for the selected organic cofactor sidecar consumed by the D11 abstention gate and mechanism-feature embedding scaffold.

## Status

- schema_passed_strict_current702
- Row-class records: 2106 / 2106
- Critical violation counts: {'missing_record_key_rows': 0, 'duplicate_entry_class_pairs': 0, 'missing_entry_class_pairs': 0, 'extra_entry_class_pairs': 0, 'score_range_violations': 0, 'class_mismatches': 0, 'split_mismatches': 0, 'threshold_policy_violations': 0, 'fallback_source_rows': 0, 'missing_source_paths': 0, 'provenance_missing_rows': 0}

## Contract

- Required classes: flavin, heme, plp
- Threshold policy: fixed_0_5_not_tuned_on_heldout
- Fallback sources allowed: False

## Selected Sources

- trained:esm2_t12_35m: 702
- trained:esm2_t6_8m: 1404

## Interpretation

- The selected organic cofactor sidecar satisfies the strict current702 row-class grid and lineage contract.
- This closes the organic flavin/heme/PLP sidecar schema risk for the mechanism-feature embedding scaffold, while metal, cobalamin, radical, and Fe-S row-level loci remain separate feature gaps.
