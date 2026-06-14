# Cohesion Threshold Calibration - post Ser/Thr runner

Source preview: `artifacts/v3_bronze_silver_promotion_preview_current702_20260614_post_ser_thr_runner.json`

No threshold was changed and no registry mutation was made.

## Counts

- Total hold_low_chemistry_cohesion: 1779.
- Fingerprints with low-cohesion holds: 33.

## Largest Buckets

- `non_heme_iron_2og_dioxygenase`: 134
- `molybdopterin_oxidoreductase`: 127
- `copper_oxidoreductase`: 125
- `sam_methyltransferase`: 121
- `class_ii_metal_aldolase`: 120
- `cobalamin_radical_rearrangement`: 96
- `flavin_dehydrogenase_reductase`: 91
- `plp_dependent_enzyme`: 88
- `ser_his_acid_hydrolase`: 79
- `coa_acyltransferase`: 73
- `cofactor_independent_isomerase`: 61
- `cytochrome_p450_monooxygenase`: 61

## Decision

- Keep thresholds unchanged. Any per-family relaxation needs a fresh leakage-safe calibration design before use.
