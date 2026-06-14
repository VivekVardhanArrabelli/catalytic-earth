# Chemistry Disagree Triage - post Ser/Thr runner

Source preview: `artifacts/v3_bronze_silver_promotion_preview_current702_20260614_post_ser_thr_runner.json`

No registry mutation, demotion, threshold change, or predictive feature change was made.

## Counts

- Total review_chemistry_disagrees: 1630.
- Fingerprints with chemistry-disagree holds: 33.
- Review queue sample rows available in source preview: 25.

## Largest Buckets

- `metal_dependent_hydrolase`: 225
- `pfkb_ribokinase_family`: 128
- `molybdopterin_oxidoreductase`: 123
- `alpha_beta_hydrolase_esterase_lipase`: 120
- `metallopeptidase`: 117
- `metallophosphomonoesterase`: 110
- `metal_racemase_epimerase_non_plp`: 101
- `ghmp_small_molecule_kinase`: 100
- `metallophosphoesterase_nuclease`: 93
- `glycosyltransferase`: 84
- `glycoside_hydrolase`: 75
- `nad_p_dehydrogenase`: 68

## Sample-Pair Triage

- `metal_dependent_hydrolase` -> `zinc_lyase_hydratase` (sample 23): neighbor-family representation collision; needs source-free feature or geometry review.
- `metal_dependent_hydrolase` -> `metallopeptidase` (sample 1): legacy umbrella split/representation gap; do not demote from sample alone.
- `metal_dependent_hydrolase` -> `manganese_iron_superoxide_dismutase` (sample 1): manual review candidate; no mutation without row-level provenance.

## Next Action

- Materialize a full row-level chemistry-disagree export before any demotion; prioritize largest buckets and legacy umbrella-to-v2-subfamily collisions as representation/split review.
