# Cofactor-independent isomerase lane-design scout

Run: 2026-06-13T01:25:20Z

Non-destructive lane-design scout for the recommended post-CoA 19fp lane. No registry write, no labels emitted.

## Lane supply

| lane | supply | distinct full ECs in 200-row sample | reaction-poor warning | top ECs |
| --- | ---: | ---: | --- | --- |
| `isomerase_ec_5_3_1_intramolecular_oxidoreductase_like` | 4218 | 32 | True | 5.3.1.1 (61), 5.3.1.9 (40), 4.2.3.3 (24), 5.3.1.24 (17), 4.1.1.48 (14) |
| `isomerase_ec_5_3_2_keto_aldose` | 141 | 10 | True | 5.3.2.5 (27), 5.3.2.2 (25), 5.3.2.1 (17), 5.3.3.12 (17), 5.3.2.6 (9) |
| `isomerase_ec_5_3_3_alkene` | 745 | 26 | True | 5.3.3.8 (112), 4.2.1.17 (102), 1.1.1.35 (97), 5.1.2.3 (91), 5.3.3.2 (20) |
| `isomerase_ec_5_3_4_disulfide` | 116 | 1 | True | 5.3.4.1 (116) |
| `isomerase_ec_5_3_broad_keyword` | 5273 | 51 | False | 5.3.4.1 (47), 5.3.3.8 (25), 4.2.1.17 (16), 5.3.99.3 (12), 1.1.1.35 (12) |

## Proposed guards

- Hold EC 1.11 peroxidase side rows.
- Hold EC 2.5 transferase side rows.
- Separate protein disulfide isomerase / thiol-redox rows from generic cofactor-independent isomerase.
- Require Rhea isomerization text or Isomerase domain plus active-/binding-site/base evidence; EC alone must never admit.

## Next action

- Wire 19fp only after adding fingerprint/ontology, trust-tier/leakage tests, OOS prereg re-freeze, and preview gates; do not admit EC-only rows.
