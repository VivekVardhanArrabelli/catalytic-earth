# Sequence/Fold Failure Benchmark Queue - 2026-05-28

Review-only benchmark design for the first current702 sequence/fold failure slice. This does not edit labels, registries, ontologies, thresholds, production scoring, imports, or model outputs, and it uses only existing local artifacts/caches.

## Selection Policy

- Primary target: true near-orphans where both sequence-NN and Foldseek/structural-neighborhood evidence lack a useful same-fingerprint/mechanism neighbor.
- Sequence evidence: existing deterministic 3-mer sequence-NN export; no new sequence search was run.
- Fold evidence: Wave 1 full-structure Foldseek nearest-neighbor fields, retained TM orphan-design proxy, and existing targeted Packet 1 TM evidence where available.
- Rows with same-fingerprint Foldseek or sequence support are verification candidates, not the primary new slice.
- Known Packet 1 fold-conflict rows are reference-only to avoid duplicating Packet 1 work.

## Counts

- `verified_true_near_orphan`: 7
- `candidate_needs_tm_or_sequence_verification`: 23
- `label_contested_hold`: 5
- `fold_conflict_reference_only`: 3
- `OOS_router_control`: 9

## Active-Site Encoder Hard Split

Feed now: `m_csa:97`, `m_csa:211`, `m_csa:250`, `m_csa:517`, `m_csa:686`, `m_csa:916`, `m_csa:990`.

Hold out for label/child-cell uncertainty: `m_csa:403`, `m_csa:497`, `m_csa:723`, `m_csa:750`, `m_csa:994`.

Hold out pending TM/Foldseek/coordinate row verification: `m_csa:577`, `m_csa:599`, `m_csa:710`, `m_csa:892`, `m_csa:897`.

Do not promote rows with same-fingerprint sequence or full-structure Foldseek neighbors until targeted TM/sequence verification says the neighbor is not useful: `m_csa:3`, `m_csa:20`, `m_csa:43`, `m_csa:44`, `m_csa:109`, `m_csa:115`, `m_csa:159`, `m_csa:163`, `m_csa:171`, `m_csa:180`, `m_csa:213`, `m_csa:242`, `m_csa:321`, `m_csa:424`, `m_csa:551`, `m_csa:609`, `m_csa:688`, `m_csa:710`, `m_csa:714`.

## Verified True Near-Orphans

| row | current fingerprint | sequence-neighbor support | Foldseek/TM proxy | coordinate | rescue expectation | label cleanliness |
| --- | --- | --- | --- | --- | --- | --- |
| `m_csa:97` | `metal_dependent_hydrolase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:417 / OOS; J=0.0776 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:435 / OOS; bits=15.0; lddt=0.1956 | pdb:1CTT; already_materialized; path=True | geometry=0.6009 (yes); other_success=geometry_baseline | clean_current_registry_parent_label |
| `m_csa:211` | `flavin_dehydrogenase_reductase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:638 / OOS; J=0.0617 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:327 / OOS; bits=24.0; lddt=0.3241 | pdb:1IDT; already_materialized; path=True | geometry=0.5459 (yes); other_success=geometry_baseline | clean_current_registry_parent_label |
| `m_csa:250` | `heme_peroxidase_oxidase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:466 / OOS; J=0.0726 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:28 / metal_dependent_hydrolase; bits=15.0; lddt=0.3015 | pdb:2CPO; already_materialized; path=True | geometry=0.7104 (yes); other_success=geometry_baseline | clean_current_registry_parent_label |
| `m_csa:517` | `metal_dependent_hydrolase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:450 / OOS; J=0.0532 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:519 / ser_his_acid_hydrolase; bits=38.0; lddt=0.33 | pdb:1I6P; already_materialized; path=True | geometry=0.5965 (yes); other_success=geometry_baseline | clean_v1_parent_with_underpowered_v2_child_caveat |
| `m_csa:686` | `metal_dependent_hydrolase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:246 / OOS; J=0.0568 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:360 / OOS; bits=332.0; lddt=0.5647 | pdb:1E1A; already_materialized; path=True | geometry=0.5817 (yes); other_success=geometry_baseline | clean_current_registry_parent_label |
| `m_csa:916` | `metal_dependent_hydrolase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:316 / OOS; J=0.0453 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:110 / flavin_dehydrogenase_reductase; bits=18.0; lddt=0.3588 | pdb:4Z71; already_materialized; path=True | geometry=0.5698 (yes); other_success=geometry_baseline,esm_c_corrected_logistic | clean_current_registry_parent_label |
| `m_csa:990` | `flavin_dehydrogenase_reductase` | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:59 / OOS; J=0.0802 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:762 / plp_dependent_enzyme; bits=53.0; lddt=0.2758 | pdb:5DQR; already_materialized; path=True | geometry=0.7317 (yes); other_success=geometry_baseline,esm2_150m,esm_c_corrected_logistic | clean_v1_parent_with_fe_s_plus_flavin_caveat |

## Verification Candidates

These rows came from the older orphan-design/proxy queues but are not primary true near-orphans today because they have same-fingerprint Foldseek/sequence support, no row-level structure proxy in Wave 1, or a v2/family caveat.

| row | current fingerprint | reason | sequence support | Foldseek/TM proxy | coordinate |
| --- | --- | --- | --- | --- | --- |
| `m_csa:3` | `flavin_dehydrogenase_reductase` | same-fingerprint full-structure Foldseek neighbor exists but retained TM same-fingerprint evidence is absent | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:404 / OOS; J=0.0593 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:117 / flavin_dehydrogenase_reductase; bits=70.0; lddt=0.3608 | pdb:1D4A; already_materialized; path=True |
| `m_csa:20` | `flavin_dehydrogenase_reductase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:304 / flavin_dehydrogenase_reductase; J=0.0971 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:739 / flavin_dehydrogenase_reductase; bits=647.0; lddt=0.6497 | pdb:1QJD; already_materialized; path=True |
| `m_csa:43` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | wrong_or_misleading_sequence_neighbor; nearest m_csa:808 / ser_his_acid_hydrolase; J=0.0657 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:472 / metal_dependent_hydrolase; bits=65.0; lddt=0.2546 | pdb:4KBP; already_materialized; path=True |
| `m_csa:44` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest uniprot:Q3LXA3 / OOS; J=0.0933 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:158 / metal_dependent_hydrolase; bits=110.0; lddt=0.3252 | pdb:1ALK; already_materialized; path=True |
| `m_csa:109` | `flavin_dehydrogenase_reductase` | same-fingerprint full-structure Foldseek neighbor exists; FMO/v2 boundary review needed before mechanism-specific use | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:8 / OOS; J=0.0897 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:800 / flavin_dehydrogenase_reductase; bits=376.0; lddt=0.5247 | pdb:1D3G; already_materialized; path=True |
| `m_csa:115` | `flavin_dehydrogenase_reductase` | same-fingerprint full-structure Foldseek neighbor exists despite no retained TM>=0.70 same-fingerprint row | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:496 / OOS; J=0.1091 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:141 / flavin_dehydrogenase_reductase; bits=338.0; lddt=0.4703 | pdb:1W1O; already_materialized; path=True |
| `m_csa:159` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest uniprot:Q3LXA3 / OOS; J=0.0904 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:172 / metal_dependent_hydrolase; bits=153.0; lddt=0.4349 | pdb:1HZY; already_materialized; path=True |
| `m_csa:163` | `metal_dependent_hydrolase` | no_useful_same_fingerprint_foldseek_neighbor | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:917 / metal_dependent_hydrolase; J=0.0494 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:187 / OOS; bits=34.0; lddt=0.271 | pdb:1RDD; already_materialized; path=True |
| `m_csa:171` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:612 / OOS; J=0.07 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:167 / metal_dependent_hydrolase; bits=112.0; lddt=0.3626 | pdb:1M4L; already_materialized; path=True |
| `m_csa:180` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:59 / OOS; J=0.0718 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:28 / metal_dependent_hydrolase; bits=25.0; lddt=0.2391 | pdb:1HYO; already_materialized; path=True |
| `m_csa:213` | `plp_dependent_enzyme` | PLP racemase/epimerase child stratum is underpowered; Foldseek has same-fingerprint support | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:466 / OOS; J=0.0831 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:937 / plp_dependent_enzyme; bits=179.0; lddt=0.437 | pdb:1L6G; already_materialized; path=True |
| `m_csa:242` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:417 / OOS; J=0.0648 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:300 / metal_dependent_hydrolase; bits=129.0; lddt=0.4511 | pdb:2F9R; already_materialized; path=True |
| `m_csa:321` | `metal_dependent_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | wrong_or_misleading_sequence_neighbor; nearest m_csa:68 / flavin_dehydrogenase_reductase; J=0.0707 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:754 / metal_dependent_hydrolase; bits=60.0; lddt=0.3421 | pdb:1YT3; already_materialized; path=True |
| `m_csa:424` | `plp_dependent_enzyme` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:476 / OOS; J=0.0712 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:855 / plp_dependent_enzyme; bits=367.0; lddt=0.519 | pdb:1BJO; already_materialized; path=True |
| `m_csa:551` | `flavin_dehydrogenase_reductase` | clean FMO secondary/future row, but full-structure Foldseek already has same v1 fingerprint neighbor | wrong_or_misleading_sequence_neighbor; nearest m_csa:808 / ser_his_acid_hydrolase; J=0.0962 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:281 / flavin_dehydrogenase_reductase; bits=253.0; lddt=0.3492 | pdb:1FOH; already_materialized; path=True |
| `m_csa:577` | `metal_dependent_hydrolase` | Wave 1 row lacks reliable Foldseek/geometry proxy although current coordinate readiness is materialized | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:268 / OOS; J=0.0661 | foldseek_proxy_missing_needs_tm_or_row_export_verification; nearest None / OOS; bits=None; lddt=None | pdb:1IMA; materialized; path=True |
| `m_csa:599` | `ser_his_acid_hydrolase` | Wave 1 row lacks reliable Foldseek/geometry proxy although current coordinate readiness is materialized | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:303 / OOS; J=0.0748 | foldseek_proxy_missing_needs_tm_or_row_export_verification; nearest None / OOS; bits=None; lddt=None | pdb:1FY2; materialized; path=True |
| `m_csa:609` | `ser_his_acid_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:608 / ser_his_acid_hydrolase; J=0.0988 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:608 / ser_his_acid_hydrolase; bits=452.0; lddt=0.7275 | pdb:1SSX; already_materialized; path=True |
| `m_csa:688` | `ser_his_acid_hydrolase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:59 / OOS; J=0.0975 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:798 / ser_his_acid_hydrolase; bits=243.0; lddt=0.5057 | pdb:2ODQ; already_materialized; path=True |
| `m_csa:710` | `metal_dependent_hydrolase` | foldseek_proxy_missing_needs_tm_or_row_export_verification | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:447 / metal_dependent_hydrolase; J=0.0765 | foldseek_proxy_missing_needs_tm_or_row_export_verification; nearest None / OOS; bits=None; lddt=None | pdb:1RA0; materialized; path=True |
| `m_csa:714` | `heme_peroxidase_oxidase` | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:124 / heme_peroxidase_oxidase; J=0.1109 | same_fingerprint_full_structure_neighbor_present_tm_unverified_or_below_retained_threshold; nearest m_csa:124 / heme_peroxidase_oxidase; bits=952.0; lddt=0.785 | pdb:1FFT; already_materialized; path=True |
| `m_csa:892` | `flavin_dehydrogenase_reductase` | Wave 1 row lacks reliable Foldseek/geometry proxy although current coordinate readiness is materialized | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:461 / OOS; J=0.0706 | foldseek_proxy_missing_needs_tm_or_row_export_verification; nearest None / OOS; bits=None; lddt=None | pdb:2DOR; materialized; path=True |
| `m_csa:897` | `metal_dependent_hydrolase` | Wave 1 row lacks reliable Foldseek/geometry proxy although current coordinate readiness is materialized | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:308 / OOS; J=0.046 | foldseek_proxy_missing_needs_tm_or_row_export_verification; nearest None / OOS; bits=None; lddt=None | pdb:1PVI; materialized; path=True |

## Label/Child-Cell Holds

| row | current fingerprint | hold reason | sequence support | Foldseek/TM proxy |
| --- | --- | --- | --- | --- |
| `m_csa:403` | `metal_dependent_hydrolase` | clean enough for broad v1 metal hydrolase context, but Packet 2 routes it to unresolved metal-water hydrolase design signal | wrong_or_misleading_sequence_neighbor; nearest m_csa:111 / flavin_dehydrogenase_reductase; J=0.0513 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:622 / OOS; bits=18.0; lddt=0.2579 |
| `m_csa:497` | `out_of_scope/null` | current registry is already out_of_scope after expert review; older orphan/fold-control artifacts that list flavin fingerprint are stale for primary use | oos_abstention_or_no_seed_neighbor; nearest m_csa:268 / OOS; J=0.0772 | oos_false_positive_structural_neighbor; nearest m_csa:16 / metal_dependent_hydrolase; bits=248.0; lddt=0.5562 |
| `m_csa:723` | `ser_his_acid_hydrolase` | clean enough for broad v1 serine hydrolase context, but Packet 2 routes it to unresolved acyl-enzyme design signal | no_same_fingerprint_sequence_neighbor_abstains_to_oos; nearest m_csa:421 / OOS; J=0.0887 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:380 / OOS; bits=234.0; lddt=0.4773 |
| `m_csa:750` | `out_of_scope/null` | current registry is already out_of_scope after expert review; keep only as OOS/boundary control until any future family exists | oos_abstention_or_no_seed_neighbor; nearest m_csa:268 / OOS; J=0.0785 | oos_false_positive_structural_neighbor; nearest m_csa:68 / flavin_dehydrogenase_reductase; bits=284.0; lddt=0.4613 |
| `m_csa:994` | `metal_dependent_hydrolase` | sequence-NN has same-fingerprint support and Packet 2 routes it to unresolved metal-water hydrolase design signal | same_fingerprint_sequence_nn_support_but_low_3mer_proxy; nearest m_csa:626 / metal_dependent_hydrolase; J=0.0879 | no_useful_same_fingerprint_foldseek_neighbor; nearest m_csa:262 / OOS; bits=28.0; lddt=0.2465 |

## Reference And Controls

| row | tier | current fingerprint | use | Foldseek/TM proxy | sequence support |
| --- | --- | --- | --- | --- | --- |
| `m_csa:217` | `fold_conflict_reference_only` | `out_of_scope/null` | reference_only_do_not_count_as_new_slice | oos_targeted_tm_reference; nearest m_csa:733 / ser_his_acid_hydrolase; bits=245.0; lddt=0.578 | oos_abstention_or_no_seed_neighbor; nearest m_csa:179 / OOS; J=0.056 |
| `m_csa:428` | `fold_conflict_reference_only` | `out_of_scope/null` | reference_only_do_not_count_as_new_slice | oos_targeted_tm_reference; nearest m_csa:11 / metal_dependent_hydrolase; bits=113.0; lddt=0.4049 | oos_abstention_or_no_seed_neighbor; nearest m_csa:421 / OOS; J=0.0584 |
| `m_csa:477` | `fold_conflict_reference_only` | `out_of_scope/null` | reference_only_do_not_count_as_new_slice | oos_targeted_tm_reference; nearest m_csa:608 / ser_his_acid_hydrolase; bits=155.0; lddt=0.4993 | oos_abstention_or_no_seed_neighbor; nearest m_csa:59 / OOS; J=0.1664 |
| `m_csa:10` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_router_abstention; nearest m_csa:461 / OOS; bits=58.0; lddt=0.4499 | oos_abstention_or_no_seed_neighbor; nearest m_csa:476 / OOS; J=0.0519 |
| `m_csa:30` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_false_positive_structural_neighbor; nearest m_csa:124 / heme_peroxidase_oxidase; bits=25.0; lddt=0.2834 | oos_abstention_or_no_seed_neighbor; nearest m_csa:268 / OOS; J=0.0928 |
| `m_csa:31` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_false_positive_structural_neighbor; nearest m_csa:160 / metal_dependent_hydrolase; bits=16.0; lddt=0.2744 | oos_false_positive_sequence_neighbor; nearest m_csa:935 / heme_peroxidase_oxidase; J=0.0547 |
| `m_csa:116` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_router_abstention; nearest m_csa:496 / OOS; bits=566.0; lddt=0.8904 | oos_abstention_or_no_seed_neighbor; nearest m_csa:496 / OOS; J=0.0996 |
| `m_csa:191` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_router_abstention; nearest m_csa:398 / OOS; bits=28.0; lddt=0.331 | oos_abstention_or_no_seed_neighbor; nearest m_csa:207 / OOS; J=0.0968 |
| `m_csa:369` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_router_abstention; nearest m_csa:457 / OOS; bits=533.0; lddt=0.5767 | oos_abstention_or_no_seed_neighbor; nearest m_csa:221 / OOS; J=0.0848 |
| `m_csa:440` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_targeted_tm_reference; nearest m_csa:697 / flavin_dehydrogenase_reductase; bits=76.0; lddt=0.3326 | oos_abstention_or_no_seed_neighbor; nearest m_csa:421 / OOS; J=0.0854 |
| `m_csa:634` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_false_positive_structural_neighbor; nearest m_csa:114 / flavin_dehydrogenase_reductase; bits=29.0; lddt=0.2127 | oos_abstention_or_no_seed_neighbor; nearest m_csa:59 / OOS; J=0.0838 |
| `m_csa:651` | `OOS_router_control` | `out_of_scope/null` | router_abstention_control | oos_false_positive_structural_neighbor; nearest m_csa:123 / flavin_dehydrogenase_reductase; bits=30.0; lddt=0.2952 | oos_abstention_or_no_seed_neighbor; nearest m_csa:496 / OOS; J=0.0837 |

## Source Artifacts

- `data/registries/curated_mechanism_labels.json`
- `artifacts/v1_graph_1025.json`
- `artifacts/v3_sequence_nn_predictions_current702_20260525.jsonl`
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`
- `artifacts/v3_mechanism_prediction_orphan_eval_design_702_20260525.json`
- `artifacts/v3_wave1_structure_neighborhood_audit_20260526.json`
- `artifacts/v3_near_orphan_geometry_support_review_packet_702_20260526.json`
- `artifacts/v3_packet2_near_orphan_geometry_support_decision_closure_702_20260527.json`
- `artifacts/v3_targeted_mechanism_evidence_acquisition_queue_702_20260526.json`
- `artifacts/v3_wave1_tm_pair_signal_expansion_result_702_20260527.json`
- `artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json`
- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_flavin_fe_s_population_expert_disposition_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json`

## Non-Claims

- This artifact is not a label import and does not make any row countable for validation by itself.
- Retained-TM absence is a local proxy, not a full all-vs-all TM proof except where targeted Packet 1 TM evidence already exists.
- Current out-of-scope states for `m_csa:497` and `m_csa:750` are read from the existing registry; this run did not edit labels.
- Full mechanism prediction claims still require expert approval and a frozen evaluation contract.
