# Fold-Augmented Lever 3 Retained Descriptor Rescue Readout - current702

Run: 2026-06-05T05:17:22Z

Lever 3 measured readout for retained same-family rows previously marked pocket-descriptor-missing. It inventories existing source-free predicted-geometry artifacts, recovers any pocket descriptor values already present, and applies the selected descriptor counteraxis from the generalization readout without selecting a new rule, changing thresholds, scoring rows, staging coordinates, or using heldout rows for tuning.

## Status

- fold_augmented_lever3_retained_descriptor_rescue_readout_all_recovered
- Descriptor missing gap cleared by existing artifacts: True
- New counteraxis selected now: False

## Counts

- Previously descriptor-missing rows recovered: 9/9
- Retained rows with descriptors after rescue: 11/11
- Selected rule recovered rows fired: 0
- Retained residual rows after selected descriptor counteraxis: 10

## Selected Rule

- Rule: residue_count.LEU <= 1.0

## Recovered Rows

| row | source | selected rule fires | action delta |
| --- | --- | --- | --- |
| m_csa:229 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:89 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:74 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:256 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:638 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:190 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:84 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_tranche2_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:468 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:308 | artifacts/v3_fold_augmented_confounded_proxy_train_cal_scored_extension_current702_20260603.json | False | retain_at_fixed_operating_point_not_scoring_closure |

## Decision

- Zero residual retained-transfer risk available now: False
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Next gate: The descriptor acquisition gap is cleared from existing source-free artifacts; next design a separate train/cal-only counteraxis for the 10 still-retained descriptor-present rows, especially m_csa:52, without retuning on those rows.

## Guardrails

- Measured readout only. Existing artifacts only; no coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- 9/9 previously descriptor-missing retained rows have source-free descriptors in existing artifacts.
- The selected LEU-count counteraxis fires 0 recovered rows, so the retained residual count remains 10 after the prior m_csa:25 abstention.
- Use the recovered descriptor surface for a new train/cal-only counteraxis design; do not claim zero residual risk from the current LEU-count rule.
