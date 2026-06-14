# Cohesion Threshold Calibration - post silver apply

Run: 2026-06-14T18:34:04Z

Non-destructive calibration review over the current bronze-seed promotion surface. No threshold was changed, no tier was changed, and no registry was written.

## Counts

- Bronze seed labels reviewed: 5608.
- Low-cohesion holds: 1759.
- Near-threshold low-cohesion holds (>=0.90 and <0.92): 232.
- Recommendation counts: {'do_not_lower_threshold_representation_or_scope_gap_first': 9, 'keep_default_threshold_no_current_relaxation_signal': 21, 'near_threshold_but_hold_until_family_separation_review': 2, 'near_threshold_family_candidate_for_preregistered_calibration_design_only': 5}.

## Top Low-Cohesion Families

| fingerprint | low holds | near >=0.90 | self-consistency | recommendation |
| --- | ---: | ---: | ---: | --- |
| non_heme_iron_2og_dioxygenase | 134 | 17 | 0.972 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| molybdopterin_oxidoreductase | 127 | 109 | 0.508 | do_not_lower_threshold_representation_or_scope_gap_first |
| copper_oxidoreductase | 125 | 0 | 0.8214 | keep_default_threshold_no_current_relaxation_signal |
| sam_methyltransferase | 121 | 0 | 0.964 | keep_default_threshold_no_current_relaxation_signal |
| class_ii_metal_aldolase | 120 | 0 | 0.8133 | keep_default_threshold_no_current_relaxation_signal |
| cobalamin_radical_rearrangement | 96 | 11 | 0.825 | near_threshold_but_hold_until_family_separation_review |
| flavin_dehydrogenase_reductase | 91 | 1 | 0.901 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| plp_dependent_enzyme | 88 | 0 | 0.9224 | keep_default_threshold_no_current_relaxation_signal |
| ser_his_acid_hydrolase | 79 | 0 | 0.908 | keep_default_threshold_no_current_relaxation_signal |
| coa_acyltransferase | 73 | 0 | 0.984 | keep_default_threshold_no_current_relaxation_signal |
| cofactor_independent_isomerase | 61 | 46 | 0.7933 | near_threshold_but_hold_until_family_separation_review |
| cytochrome_p450_monooxygenase | 61 | 0 | 0.952 | keep_default_threshold_no_current_relaxation_signal |
| metallophosphoesterase_nuclease | 57 | 0 | 0.38 | do_not_lower_threshold_representation_or_scope_gap_first |
| atp_amide_ligase | 56 | 0 | 0.8667 | keep_default_threshold_no_current_relaxation_signal |
| thiamine_diphosphate_enzyme | 56 | 0 | 0.7867 | keep_default_threshold_no_current_relaxation_signal |

## Top Near-Threshold Families

| fingerprint | near >=0.90 | very near >=0.91 | low max | self-consistency | recommendation |
| --- | ---: | ---: | ---: | ---: | --- |
| molybdopterin_oxidoreductase | 109 | 0 | 0.909 | 0.508 | do_not_lower_threshold_representation_or_scope_gap_first |
| cofactor_independent_isomerase | 46 | 30 | 0.9111 | 0.7933 | near_threshold_but_hold_until_family_separation_review |
| flavin_monooxygenase | 19 | 10 | 0.9112 | 0.9474 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| heme_peroxidase_oxidase | 18 | 10 | 0.9108 | 0.8889 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| non_heme_iron_2og_dioxygenase | 17 | 0 | 0.9071 | 0.972 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| biotin_dependent_carboxylase | 11 | 0 | 0.909 | 1.0 | near_threshold_family_candidate_for_preregistered_calibration_design_only |
| cobalamin_radical_rearrangement | 11 | 11 | 0.9175 | 0.825 | near_threshold_but_hold_until_family_separation_review |
| flavin_dehydrogenase_reductase | 1 | 0 | 0.9064 | 0.901 | near_threshold_family_candidate_for_preregistered_calibration_design_only |

## Guardrails

- Thresholds changed: False.
- Registry written: False.
- EC/Rhea/names/source text used as predictive features: False.
- Low-self-consistency families are treated as representation/scope gaps, not as candidates for threshold relaxation.

## Next Action

- Review near-threshold high-self-consistency families only through a pre-registered calibration split; handle low-self-consistency families as representation/scope gaps, not threshold relaxations.
