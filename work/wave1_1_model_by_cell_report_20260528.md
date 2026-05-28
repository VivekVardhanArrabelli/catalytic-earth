# Wave 1.1 Model-by-Cell Report - 2026-05-28

Review-only report from existing Wave 1 predictions/exports and closed Packet 2/Packet 3 plus m_csa:497/m_csa:750 impact artifacts. No labels, registries, ontology files, imports, production scoring, model outputs, or thresholds were changed.

## Direct Answer

Learned representations add limited, non-decision-grade value where Foldseek is weak. The clearest learned signal is the 4-row wrong-Foldseek-transfer cell: ESM-C corrected logistic rescues 2/4 and ESM-2 plus ESM-C cosine each rescue 1/4, while Foldseek is wrong on all 4. But geometry rescues 4/4, and in the larger 17-row near-orphan cell ESM-2 reaches 9/17 versus Foldseek 13/17 and geometry 17/17.

Decision gate: prioritize external panels/features/labels and the Foldseek-plus-geometry atlas over running larger models now. Larger models should wait until row-aligned standardized exports and child-label targets exist, without threshold tuning.

## Count Scope

- `correct`, `wrong`, and `abstain` are parent-v1 counts unless a row is marked aggregate-only; Packet 3 cells are not child-label metrics.
- `missing` includes absent standardized exports; for Packet 3 representative rows absent from Wave 1 audit, those representatives are counted as missing.
- `OOS FP` is nonabstaining primary-family prediction on OOS/secondary rows; the primary read-through cell uses the closed m_csa:497/m_csa:750 impact readout where available.

## Diagnostic Cell Tables

### Primary v1 after m_csa:497/m_csa:750 read-through

Use: `review_only_diagnostic_summary_only`. Countable metric: `false`.

Takeaway: ESM-2 is close to Foldseek on primary accuracy and safer on the two excluded boundary rows, but it does not beat Foldseek overall and has more OOS false positives.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 27 | 4 | 12 | 0 | 11 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 8 | 7 | 28 | 1 | 18 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| geometry_baseline | 38 | 0 | 0 | 5 | 97 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 7 | 5 | 31 | 0 | 27 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| esm2_150m | 26 | 0 | 17 | 0 | 16 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| esm_c_300m | 17 | 3 | 23 | 0 | 17 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| esm_c_cosine_nn | 4 | 10 | 29 | 0 | 34 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| prott5 | 17 | 6 | 18 | 8 | 23 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| saprot | 15 | 6 | 22 | 0 | 20 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| prostt5_3di | 8 | n/a | n/a | 1 | 18 | no | no | Aggregate primary readthrough; compare correct primary calls and OOS false positives after 497/750 are OOS. |
| foldseek_pocket | n/a | n/a | n/a | 140 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

### Near-orphan geometry rescue

Use: `review_only_diagnostic_slice_only`. Countable metric: `false`.

Takeaway: Geometry is 17/17 and Foldseek is 13/17 with 4 abstentions; learned reps do not add over Foldseek or geometry in this largest weak-Foldseek cell.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 13 | 0 | 4 | 0 | 0 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 4 | 2 | 11 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| geometry_baseline | 17 | 0 | 0 | 0 | 0 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 4 | 2 | 11 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| esm2_150m | 9 | 0 | 8 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| esm_c_300m | 5 | 2 | 10 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| esm_c_cosine_nn | 1 | 4 | 12 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| prott5 | 7 | 3 | 7 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| saprot | 6 | 4 | 7 | 0 | 0 | no | no | Near-orphan parent-v1 rescue slice; learned value requires more true-family calls than Foldseek and geometry. |
| prostt5_3di | n/a | n/a | n/a | 17 | n/a | unavailable | unavailable | No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or representation_tracks directory. |
| foldseek_pocket | n/a | n/a | n/a | 17 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

### Wrong-Foldseek transfer

Use: `review_only_diagnostic_slice_only`. Countable metric: `false`.

Takeaway: ESM-C corrected logistic rescues 2/4 and ESM-2/ESM-C cosine rescue 1/4, so learned reps show limited signal where Foldseek is actively wrong, but geometry rescues 4/4.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 0 | 4 | 0 | 0 | 0 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 0 | 3 | 1 | 0 | 0 | safer_not_more_correct | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| geometry_baseline | 4 | 0 | 0 | 0 | 0 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 0 | 0 | 4 | 0 | 0 | safer_not_more_correct | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| esm2_150m | 1 | 0 | 3 | 0 | 0 | yes | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| esm_c_300m | 2 | 0 | 2 | 0 | 0 | yes | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| esm_c_cosine_nn | 1 | 0 | 3 | 0 | 0 | yes | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| prott5 | 0 | 1 | 3 | 0 | 0 | safer_not_more_correct | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| saprot | 0 | 1 | 3 | 0 | 0 | safer_not_more_correct | no | Wrong-Foldseek-transfer slice; any correct nonabstaining true-family call is a limited rescue, but geometry is the benchmark. |
| prostt5_3di | n/a | n/a | n/a | 4 | n/a | unavailable | unavailable | No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or representation_tracks directory. |
| foldseek_pocket | n/a | n/a | n/a | 4 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

### v2 child pilot strata

Use: `pilot_only_review_slice_not_canonical_metric`. Countable metric: `false`.

Takeaway: ESM-2 parent support is useful but still below Foldseek and geometry; this is not evidence to promote child labels or run larger models first.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 15 | 1 | 3 | 48 | 0 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 6 | 2 | 11 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| geometry_baseline | 18 | 0 | 0 | 49 | 0 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 5 | 2 | 12 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| esm2_150m | 14 | 0 | 5 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| esm_c_300m | 6 | 2 | 11 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| esm_c_cosine_nn | 3 | 3 | 13 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| prott5 | 10 | 3 | 5 | 49 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| saprot | 7 | 2 | 10 | 48 | 0 | no | no | Pilot child strata have no child-label predictions; counts are parent-v1 projection on mapped representatives. |
| prostt5_3di | n/a | n/a | n/a | 67 | n/a | unavailable | unavailable | No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or representation_tracks directory. |
| foldseek_pocket | n/a | n/a | n/a | 67 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

### Unresolved bucket abstention

Use: `abstention_probe_only_not_accuracy_metric`. Countable metric: `false`.

Takeaway: Parent projections do not answer unresolved child abstention; prioritize labels/features before any larger-model claim.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 4 | 0 | 5 | 18 | 0 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 0 | 1 | 8 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| geometry_baseline | 6 | 0 | 0 | 21 | 0 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 0 | 1 | 8 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm2_150m | 6 | 0 | 3 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm_c_300m | 4 | 1 | 4 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm_c_cosine_nn | 1 | 3 | 5 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| prott5 | 3 | 2 | 3 | 19 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| saprot | 3 | 1 | 5 | 18 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| prostt5_3di | n/a | n/a | n/a | 27 | n/a | unavailable | unavailable | No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or representation_tracks directory. |
| foldseek_pocket | n/a | n/a | n/a | 27 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

### Canaries and mixed chemistry

Use: `canary_only_or_do_not_use_not_countable_metric`. Countable metric: `false`.

Takeaway: No learned channel creates decision-grade value here; m_csa:750 is removed from canary use and mixed chemistry stays blocked.

| model/channel | correct | wrong | abstain | missing | OOS FP | value vs Foldseek | value vs geometry | notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| foldseek_structural_nn | 4 | 1 | 0 | 23 | 0 | reference | compare-to-geometry | Foldseek reference for this diagnostic cell. |
| foldseek_3di_token_nn | 1 | 1 | 3 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| geometry_baseline | 5 | 0 | 0 | 23 | 0 | yes | reference | Geometry reference; not a learned representation. |
| sequence_nn | 1 | 0 | 4 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm2_150m | 1 | 0 | 4 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm_c_300m | 1 | 0 | 4 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| esm_c_cosine_nn | 0 | 1 | 4 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| prott5 | 2 | 0 | 3 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| saprot | 3 | 1 | 1 | 23 | 0 | not_assessable | not_assessable | Child-level targets are unresolved/blocked; parent projection only, so this does not create model value. |
| prostt5_3di | n/a | n/a | n/a | 28 | n/a | unavailable | unavailable | No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or representation_tracks directory. |
| foldseek_pocket | n/a | n/a | n/a | 28 | n/a | unavailable | unavailable | No standardized Foldseek-pocket per-row or aggregate prediction export is present locally. |

## Decision Gate

Run larger models now: `false`.

- The strongest learned improvement is confined to 2/4 wrong-Foldseek-transfer rescues by ESM-C, while geometry resolves 4/4.
- Near-orphan coverage favors geometry and still favors Foldseek over learned reps on correct parent-v1 calls.
- Child-level and mixed-chemistry questions are label/feature-definition limited, not model-size limited, in the current exports.

Next priority:

- Build the Foldseek-plus-geometry atlas/features for near-orphan and wrong-transfer diagnostics.
- Acquire external panels and targeted labels for v2 child strata, unresolved buckets, and mixed chemistry splits.
- Only run larger models after row-aligned standardized exports and child-label targets exist, without threshold tuning.

## Guardrails

- This report does not edit labels, registries, ontology files, production scoring, imports, thresholds, or model outputs.
- Counts are review-only diagnostic readouts, not production metrics or validation claims.
- Packet 3 child-label rows remain proposal-only, abstention-probe-only, canary-only, future-acquisition, or blocked as already closed.
