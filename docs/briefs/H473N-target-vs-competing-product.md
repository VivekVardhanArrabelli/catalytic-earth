# Does H473N transketolase's competing-product nondetection imply improved target accumulation?

Generated from a real query run. Source commit `57d688af01b3edfbe69c35258ddf6d61b089b18d`.

## Question

*E. coli* transketolase H473N accumulates no detectable erythrulose, the
competing donor-route product. Does that nondetection imply the variant
accumulates more of the target product?

## Source-scoped answer

**No — the opposite direction is what the source reports.** In the same
purified-enzyme glycolaldehyde/pyruvate mixture, H473N accumulated **less**
target DHB than wild type after 24 hours: 5.5 mM versus 10.5 mM, a descriptive
central-value ratio of about 0.52. The erythrulose nondetection is recorded as
**context only**; it does not make the target route better.

Losing a competing product and gaining target product are separate claims. This
comparison supports neither improvement nor a selectivity ratio.

## Decisive observations

Comparison `tk_2020:H473N:DHB_accumulation`, operation `ratio`, study `tk_2020`.

| Role | Observation | Construct | Endpoint | Value |
|---|---|---|---|---|
| numerator | `tk2020-dhb-product:H473N:product_concentration` | `tk_2020:H473N` | DHB after 24 h | **5.5 mM** |
| denominator | `tk2020-dhb-product:WT:product_concentration` | `tk_2020:WT` | DHB after 24 h | **10.5 mM** |
| context | `tk2020-ery-product:WT:product_concentration` | `tk_2020:WT` | erythrulose after 24 h | 10.5 mM |
| context | `tk2020-ery-product:H473N:product_concentration` | `tk_2020:H473N` | erythrulose after 24 h | **not detected** |

Conditions as reported: 50 mM glycolaldehyde and 50 mM sodium pyruvate,
purified enzyme, HPLC at 24 hours.

The erythrulose nondetection carries the source token "no byproduct detected",
**no numeric detection limit**, and is explicitly flagged `is_zero_rate: false`.
The erythrulose route is measured in a mixture that also contains pyruvate, and
nondetection of the product does not establish absent flux.

These are **accumulated concentrations at a fixed time point**, not rates and
not microscopic selectivity.

## Structure context

None. This comparison is bound to source-reported product concentrations only.
No structure, no assayed sequence, and no mutant model is part of it.

## Sources and artifacts

- Study `tk2020`, bound by exact source identity (not by a study-id prefix).
- Retained primary files for this comparison, and only this study's:
  `https://discovery.ucl.ac.uk/id/eprint/10084395/` and its accepted-version PDF.
- Sibling transketolase studies `tk2024` and `tktf` are **not** sources of this
  comparison and are correctly excluded.
- Query output sha256: `620755f51c6032992efc43b80cbbf9eb9e55f6292a6e6044dec47d29234c75d8`

## Unresolved

- Any erythrulose ratio, DHB/erythrulose selectivity ratio, or propagated
  uncertainty — the comparison's own scope excludes all of them.
- Significance, zero flux, or infinite selectivity.
- Donor-half rate, pyruvate affinity, or isolated H473N mechanism.
- Transfer to another construct or study.

## Reproduce

```sh
python scripts/query_atlas_perturbations.py --comparison tk_2020:H473N:DHB_accumulation
```

**Source checkout required.** This script derives its root from its own file
location and shells out to `git`, so it does not run from an installed wheel.

*A curated demonstration case, not held-out validation and not a benchmark.*
