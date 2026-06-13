# CoA acyltransferase lane-design scout

Run: 2026-06-13T00:38:44Z

Non-destructive live UniProt scout for the recommended next 18fp lane. No registry write, no labels emitted.

## Counts

- `coa_acyltransferase_broad`: 7728
- `coa_acyltransferase_keyword_only`: 7728
- `coa_acyltransferase_cofactor_only`: 23
- `coa_acyltransferase_broad_ec_only`: 9981

## EC diversity sample

- Sample rows: 500 (with full EC: 457).
- Distinct full ECs in sample: 108.
- Top ECs:
  - `2.3.1.225`: 66
  - `2.3.1.48`: 56
  - `2.3.1.51`: 37
  - `2.3.1.23`: 23
  - `2.3.1.20`: 22
  - `2.3.1.16`: 21
  - `2.3.1.9`: 17
  - `2.3.1.15`: 16
  - `2.3.1.n7`: 16
  - `2.3.1.n6`: 13
  - `2.3.1.50`: 12
  - `2.3.1.22`: 11

## Lane sketches

| lane | supply | role |
| --- | ---: | --- |
| `coa_ec_2_3_1_acyltransferase_keyword` | 7728 | high-recall Acyltransferase keyword scope lane |
| `coa_ec_2_3_1_coa_comment` | 23 | high-precision UniProt cofactor-comment lane |
| `coa_ec_2_3_1_broad_union` | 7728 | union scope lane; must be capped and novelty-gated |

## Next action

- Wire coa_acyltransferase as 18fp with EC 2.3.1 scope-only lanes and counted CoA/acyl-CoA Rhea participant, Acyltransferase/domain keyword, or catalytic His/Cys active-site evidence; preview before apply.
