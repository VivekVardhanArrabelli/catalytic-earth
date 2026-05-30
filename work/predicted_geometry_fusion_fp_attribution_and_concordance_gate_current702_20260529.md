# Predicted-Geometry Fusion FP Attribution and Concordance Gate

Run: 2026-05-30T03:21:29Z

## Scope and Caveat

- Scope: current702 predicted-geometry heldout rows, read-only over existing geometry/cofactor artifacts.
- No labels, registries, ontologies, imports, production scoring, global thresholds, or model weights were changed.
- Raw-fusion aggregate metrics are available, but the committed audit does not contain the full raw_fused row table; row-level raw-fusion FP attribution is therefore marked aggregate-only in JSON.

## Regime Metrics

| Regime | Coverage | Primary accepted | Primary correct | Primary accuracy | Accepted primary precision | Wrong primary | OOS/sec FP | OOS/sec FP rate | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| predicted_geometry_hand_router_reference | 38 | 28 | 23 | 0.511111 | 0.821429 | 5 | 10 | 0.123457 | 88 |
| raw_fusion_existing_summary | 90 | 44 | 31 | 0.688889 | 0.704545 | 13 | 46 | 0.567901 | 36 |
| target_failure_diagnostic_existing_summary | 38 | 28 | 28 | 0.622222 | 1.0 | 0 | 10 | 0.123457 | 88 |
| sequence_supported_suppression_existing_summary | 18 | 16 | 16 | 0.355556 | 1.0 | 0 | 2 | 0.024691 | 108 |
| concordance_gate | 20 | 20 | 20 | 0.444444 | 1.0 | 0 | 0 | 0.0 | 106 |

## FP Attribution

- Existing raw fusion: 46 OOS/sec false positives and 13 wrong-primary calls; row-level raw-fused FP bins were not persisted.
- Predicted-geometry hand-router reference: 10 OOS/sec FPs and 5 wrong-primary calls.
- Concordance gate: 0 OOS/sec FPs and 0 wrong-primary calls.

Top reference FP bins:

| FP type | Called fingerprint | Source | Cofactor bin | Geometry bin | Structural bin | Count |
| --- | --- | --- | --- | --- | --- | ---: |
| oos_row_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_high_ge_0.95 | medium_0.4115_0.55 | broad_bucket_ambiguous | 4 |
| oos_row_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_high_ge_0.95 | high_0.55_0.70 | broad_bucket_ambiguous | 2 |
| oos_row_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_mid_0.90_0.95 | high_0.55_0.70 | broad_bucket_ambiguous | 1 |
| oos_row_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_mid_0.90_0.95 | medium_0.4115_0.55 | broad_bucket_ambiguous | 1 |
| oos_row_false_positive | ser_his_acid_hydrolase | geometry_only_predicted_hand_router | not_required_geometry_only | high_0.55_0.70 | broad_bucket_ambiguous | 1 |
| oos_row_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_low_0.50_0.90 | medium_0.4115_0.55 | broad_bucket_ambiguous | 1 |
| wrong_primary_call_false_positive | ser_his_acid_hydrolase | geometry_only_predicted_hand_router | not_required_geometry_only | medium_0.4115_0.55 | low_structure_neighborhood_near_orphan | 1 |
| wrong_primary_call_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_high_ge_0.95 | medium_0.4115_0.55 | dense_same_mechanism_structural_neighborhood | 1 |
| wrong_primary_call_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_low_0.50_0.90 | medium_0.4115_0.55 | low_structure_neighborhood_near_orphan | 1 |
| wrong_primary_call_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_high_ge_0.95 | high_0.55_0.70 | low_structure_neighborhood_near_orphan | 1 |
| wrong_primary_call_false_positive | metal_dependent_hydrolase | geometry_only_predicted_hand_router | mionic_high_ge_0.95 | medium_0.4115_0.55 | low_structure_neighborhood_near_orphan | 1 |

## Concordance Gate

- Fixed rule: predicted geometry must be confident, cofactor evidence must be trusted for the class, and broad OOS structural-neighborhood bins are hard-abstained.
- Metal trust: M-Ionic >= 0.95; weak heme/PLP/flavin calls are discounted unless already present in the persisted raw-fusion target-recovery rows or backed by motif plus local/role support.
- Accepted primary calls: 20 versus suppression 16.
- OOS/sec FP leak: 0 versus raw fusion 46.

## Per-Class Concordance Readout

| Class | Support | Accepted | Correct | Wrong | Abstained | Accepted precision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| flavin_dehydrogenase_reductase | 10 | 2 | 2 | 0 | 8 | 1.0 |
| heme_peroxidase_oxidase | 4 | 2 | 2 | 0 | 2 | 1.0 |
| metal_dependent_hydrolase | 17 | 15 | 15 | 0 | 2 | 1.0 |
| plp_dependent_enzyme | 6 | 0 | 0 | 0 | 6 | N/A |
| ser_his_acid_hydrolase | 8 | 1 | 1 | 0 | 7 | 1.0 |

## Done Bar

- Raw leak OOS-concentrated: True (0.779661 of raw nonabstained errors are OOS/sec FPs).
- More accepted primary calls than suppression: True (20 > 16).
- Fewer OOS/sec FPs than raw fusion: True (0 < 46).
- OOS/sec FP at experimental-geometry zero target: True.
- Stop condition: met.
