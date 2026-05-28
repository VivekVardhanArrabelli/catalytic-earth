# Wave 1.1 Diagnostic Benchmark Result - 2026-05-27

This is a review-only diagnostic benchmark readout built from existing Wave 1 and closed Packet 2/3 artifacts. It does not create countable metrics, child labels, model outputs, thresholds, imports, or registry edits.

## Decision Summary

- Foldseek dense-neighbor question: yes. Foldseek remains strong in the existing aggregate readthrough and dense-neighborhood Wave 1 card, but in closed Packet 2 diagnostics it supports 13/17 near-orphan rows and makes 4/4 unsafe wrong-transfer calls.
- Geometry value question: yes. Geometry supports 17/17 near-orphan rows and rescues 4/4 wrong-Foldseek-transfer rows.
- Representation question: limited_and_underpowered. ESM-2 is the strongest available learned comparator in these cells, with 9/17 near-orphan and 1/4 wrong-transfer support. ProtT5 and SaProt add sporadic parent-v1 support but no child-label readout; ProstT5-3Di row-level exports and Foldseek-pocket are unavailable.
- Recommended next move: `targeted_hybrid_foldseek_geometry_atlas_engine_plus_fingerprint_v2_label_acquisition`.

## Diagnostic Cells

### primary_v1_metrics_after_m_csa497_m_csa750_readthrough

Use: `review_only_diagnostic_summary_only`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 43 | 27 | 2 | 0 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 27/43 primary-support calls and 2/2 unsafe predictions on the excluded boundary rows. |
| geometry_baseline | true | 38 | 38 | 1 | 1 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 38/38 primary-support calls and 1/2 unsafe predictions on the excluded boundary rows. |
| sequence_nn | true | 43 | 7 | 0 | 2 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 7/43 primary-support calls and 0/2 unsafe predictions on the excluded boundary rows. |
| esm2_150m | true | 43 | 26 | 0 | 2 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 26/43 primary-support calls and 0/2 unsafe predictions on the excluded boundary rows. |
| esm_c | true | 43 | 17 | 1 | 1 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 17/43 primary-support calls and 1/2 unsafe predictions on the excluded boundary rows. |
| prott5 | true | 41 | 17 | 1 | 1 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 17/41 primary-support calls and 1/2 unsafe predictions on the excluded boundary rows. |
| saprot | true | 43 | 15 | 1 | 1 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 15/43 primary-support calls and 1/2 unsafe predictions on the excluded boundary rows. |
| prostt5_3di | true | 43 | 8 | 0 | 2 | After excluding m_csa:497 and m_csa:750 from primary flavin metrics, the aggregate readthrough has 8/43 primary-support calls and 0/2 unsafe predictions on the excluded boundary rows. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

### packet2_near_orphan_geometry_rescue_behavior

Use: `review_only_diagnostic_slice_only`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 17 | 13 | 0 | 4 | Foldseek is safe but incomplete in near-orphans: 13/17 same-family transfers with 4 abstentions and 0 wrong nonabstentions. |
| geometry_baseline | true | 17 | 17 | 0 | 0 | Geometry supports the expected v1 family on 17/17 near-orphan rows, the clearest rescue signal in this cell. |
| sequence_nn | true | 17 | 4 | 2 | 11 | Available as a row-aligned comparison, but it supports only 4/17 near-orphan rows and leaves 11 abstentions. |
| esm2_150m | true | 17 | 9 | 0 | 8 | Available as a row-aligned comparison, but it supports only 9/17 near-orphan rows and leaves 8 abstentions. |
| esm_c | true | 17 | 5 | 2 | 10 | Available as a row-aligned comparison, but it supports only 5/17 near-orphan rows and leaves 10 abstentions. |
| prott5 | true | 17 | 7 | 3 | 7 | Available as a row-aligned comparison, but it supports only 7/17 near-orphan rows and leaves 7 abstentions. |
| saprot | true | 17 | 6 | 4 | 7 | Available as a row-aligned comparison, but it supports only 6/17 near-orphan rows and leaves 7 abstentions. |
| prostt5_3di | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

### packet2_wrong_foldseek_transfer_diagnostic_behavior

Use: `review_only_diagnostic_slice_only`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 4 | 0 | 4 | 0 | This is the Foldseek failure slice: 4/4 rows are wrong nonabstentions. |
| geometry_baseline | true | 4 | 4 | 0 | 0 | Geometry rescues the true v1 family on 4/4 wrong-transfer rows. |
| sequence_nn | true | 4 | 0 | 0 | 4 | Comparison track only: 0/4 true-family calls, 4 abstentions, and 0 wrong nonabstentions. |
| esm2_150m | true | 4 | 1 | 0 | 3 | Comparison track only: 1/4 true-family calls, 3 abstentions, and 0 wrong nonabstentions. |
| esm_c | true | 4 | 2 | 0 | 2 | Comparison track only: 2/4 true-family calls, 2 abstentions, and 0 wrong nonabstentions. |
| prott5 | true | 4 | 0 | 1 | 3 | Comparison track only: 0/4 true-family calls, 3 abstentions, and 1 wrong nonabstentions. |
| saprot | true | 4 | 0 | 1 | 3 | Comparison track only: 0/4 true-family calls, 3 abstentions, and 1 wrong nonabstentions. |
| prostt5_3di | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

### packet3_eight_pilot_only_child_stratum_readout

Use: `pilot_only_review_slice_not_canonical_metric`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 19 | 15 | 1 | 3 | Parent-v1 projection only: 15/19 mapped representative rows support the parent family. This is not a child-label metric. |
| geometry_baseline | true | 18 | 18 | 0 | 0 | Parent-v1 projection only: 18/18 mapped representative rows support the parent family. This is not a child-label metric. |
| sequence_nn | true | 19 | 5 | 2 | 12 | Parent-v1 projection only: 5/19 mapped representative rows support the parent family. This is not a child-label metric. |
| esm2_150m | true | 19 | 14 | 0 | 5 | Parent-v1 projection only: 14/19 mapped representative rows support the parent family. This is not a child-label metric. |
| esm_c | true | 19 | 6 | 2 | 11 | Parent-v1 projection only: 6/19 mapped representative rows support the parent family. This is not a child-label metric. |
| prott5 | true | 18 | 10 | 3 | 5 | Parent-v1 projection only: 10/18 mapped representative rows support the parent family. This is not a child-label metric. |
| saprot | true | 19 | 7 | 2 | 10 | Parent-v1 projection only: 7/19 mapped representative rows support the parent family. This is not a child-label metric. |
| prostt5_3di | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

### abstention_behavior_on_unresolved_or_underpowered_child_buckets

Use: `abstention_probe_only_not_accuracy_metric`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 9 | n/a | 0 | 9 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 5 parent abstentions and 0 wrong parent nonabstentions. |
| geometry_baseline | true | 6 | n/a | 0 | 6 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 0 parent abstentions and 0 wrong parent nonabstentions. |
| sequence_nn | true | 9 | n/a | 0 | 9 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 8 parent abstentions and 1 wrong parent nonabstentions. |
| esm2_150m | true | 9 | n/a | 0 | 9 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 3 parent abstentions and 0 wrong parent nonabstentions. |
| esm_c | true | 9 | n/a | 0 | 9 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 4 parent abstentions and 1 wrong parent nonabstentions. |
| prott5 | true | 8 | n/a | 0 | 8 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 3 parent abstentions and 2 wrong parent nonabstentions. |
| saprot | true | 9 | n/a | 0 | 9 | No child-label predictions are present, so true unresolved-child abstention is unavailable; the parent projection has 5 parent abstentions and 1 wrong parent nonabstentions. |
| prostt5_3di | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

### canary_behavior_for_underpowered_or_mixed_chemistry_cells

Use: `canary_only_or_do_not_use_not_countable_metric`. Countable metric: `false`.

| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| foldseek_structural_nn | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 4/5 parent-family calls. |
| geometry_baseline | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 5/5 parent-family calls. |
| sequence_nn | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 1/5 parent-family calls. |
| esm2_150m | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 1/5 parent-family calls. |
| esm_c | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 1/5 parent-family calls. |
| prott5 | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 2/5 parent-family calls. |
| saprot | true | 5 | n/a | 0 | 5 | Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use regardless of 3/5 parent-family calls. |
| prostt5_3di | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |
| foldseek_pocket | false | 0 | n/a | n/a | n/a | Unavailable for this diagnostic cell. |

## Guardrails

- No production scoring threshold, ontology, fingerprint, label registry, import, or model-output artifact was changed.
- Packet 2 rows remain review-only diagnostics and do not become countable validation labels.
- Packet 3 child labels remain proposal-only or blocked; no child-label metric is created.
- m_csa:497 and m_csa:750 remain excluded from primary v1 flavin metrics and retained only as OOS/boundary/future-acquisition signals.
- flavin.dehydrogenase_oxidase_hydride_transfer remains blocked as mixed chemistry and is not used as a v2 metric.
